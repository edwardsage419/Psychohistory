#!/usr/bin/env python3
"""Analyze GDELT GKG V1THEMES against the Psychohistory topic mapping.

This is an analysis-only tool. It never writes to data/gdelt.json and never
changes production indicators.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_MAPPING = HERE / "gkg_theme_mapping.json"
DEFAULT_REPORT = HERE / "gkg_theme_analysis_report.json"
LOOKUP_URL = "https://data.gdeltproject.org/api/v2/guides/LOOKUP-GKGTHEMES.TXT"
LASTUPDATE_URL = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

TOPIC_KEYS = ["Economic", "Geopolitics", "Technology", "Energy", "War & Conflict", "Inflation", "AI"]


def download_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Psychohistory/0.2.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Psychohistory/0.2.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def discover_latest_gkg_url() -> str:
    text = download_text(LASTUPDATE_URL)
    candidates = []
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[-1].endswith(".gkg.csv.zip"):
            url = parts[-1]
            if url.startswith("http://") or url.startswith("https://"):
                candidates.append(url)
    if not candidates:
        raise RuntimeError("No GKG .gkg.csv.zip URL found in lastupdate.txt")
    return candidates[-1]


def parse_lookup(text: str) -> dict[str, dict]:
    """Parse the official lookup conservatively.

    The lookup has changed presentation over time, so accept common TSV/space
    layouts. The code is always the first non-empty token. Remaining columns
    are preserved as raw fields for auditability.
    """
    result: dict[str, dict] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) == 1:
            parts = line.split(None, 1)
        code = parts[0].strip()
        if not code or code.upper() in {"THEME", "THEMES", "CODE"}:
            continue
        count = None
        description = ""
        if len(parts) > 1:
            description = parts[1].strip()
        if len(parts) > 2:
            try:
                count = int(parts[-1].replace(",", ""))
            except ValueError:
                pass
        result[code] = {"code": code, "description": description, "lookup_count": count, "raw": parts}
    return result


def iter_gkg_rows(blob: bytes):
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        members = [n for n in zf.namelist() if not n.endswith("/")]
        if len(members) != 1:
            raise RuntimeError(f"Expected one GKG member, found {len(members)}")
        with zf.open(members[0], "r") as fh:
            for raw in fh:
                yield raw.decode("utf-8", errors="replace").rstrip("\r\n")


def analyze_rows(lines, mapping: dict) -> tuple[Counter, int, Counter, list[str]]:
    freq = Counter()
    rows = 0
    bad_rows = 0
    dates = Counter()
    samples = []
    for line in lines:
        if not line:
            continue
        fields = line.split("\t")
        if len(fields) < 8:
            bad_rows += 1
            continue
        rows += 1
        date = fields[1][:8]
        if date.isdigit():
            dates[date] += 1
        themes = [x.strip() for x in fields[7].split(";") if x.strip()]
        # Count documents mentioning a theme once, not repeated theme mentions.
        unique_themes = set(themes)
        freq.update(unique_themes)
        if len(samples) < 3:
            samples.append(line[:2000])
    return freq, rows, dates, samples, bad_rows


def topic_sets(mapping: dict):
    result = {}
    for topic, cfg in mapping["topics"].items():
        primary = [x["code"] for x in cfg.get("primary_themes", [])]
        secondary = [x["code"] for x in cfg.get("secondary_themes", [])]
        excluded = [x["code"] for x in cfg.get("excluded_themes", [])]
        result[topic] = {"primary": primary, "secondary": secondary, "excluded": excluded}
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gkg-url", help="Specific GKG zip URL")
    ap.add_argument("--gkg-file", help="Local GKG zip file")
    ap.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    ap.add_argument("--lookup-url", default=LOOKUP_URL)
    ap.add_argument("--report", default=str(DEFAULT_REPORT))
    ap.add_argument("--top-themes", type=int, default=100)
    args = ap.parse_args()

    mapping_path = Path(args.mapping)
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))

    if args.gkg_file:
        gkg_blob = Path(args.gkg_file).read_bytes()
        gkg_source = str(Path(args.gkg_file))
    else:
        gkg_source = args.gkg_url or discover_latest_gkg_url()
        gkg_blob = download_bytes(gkg_source)

    lookup = {}
    lookup_error = None
    try:
        lookup = parse_lookup(download_text(args.lookup_url))
    except Exception as exc:
        lookup_error = f"{type(exc).__name__}: {exc}"

    freq, rows, dates, samples, bad_rows = analyze_rows(iter_gkg_rows(gkg_blob), mapping)
    sets = topic_sets(mapping)

    topic_report = {}
    for topic, groups in sets.items():
        all_codes = groups["primary"] + groups["secondary"]
        matches = []
        for code in all_codes:
            matches.append({
                "code": code,
                "role": "primary" if code in groups["primary"] else "secondary",
                "document_count": freq.get(code, 0),
                "lookup_description": lookup.get(code, {}).get("description", ""),
                "lookup_count": lookup.get(code, {}).get("lookup_count"),
            })
        topic_report[topic] = {
            "primary_matches": [x for x in matches if x["role"] == "primary"],
            "secondary_matches": [x for x in matches if x["role"] == "secondary"],
            "excluded_observed": [{"code": c, "document_count": freq.get(c, 0)} for c in groups["excluded"] if freq.get(c, 0)],
        }

    report = {
        "analysis_version": "V0.2.1-B",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"gkg": gkg_source, "lookup_url": args.lookup_url, "lookup_error": lookup_error},
        "dataset": {"rows": rows, "bad_rows": bad_rows, "dates": dict(dates), "top_themes": [{"code": c, "document_count": n, "description": lookup.get(c, {}).get("description", "")} for c, n in freq.most_common(args.top_themes)]},
        "topics": topic_report,
        "samples": samples,
        "method": {
            "frequency_definition": "document_count: each V1THEMES code counts at most once per GKG document",
            "production_status": "analysis_only",
            "ai_status": "proxy_only_not_for_production",
        },
    }
    out = Path(args.report)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] GKG source: {gkg_source}")
    print(f"[OK] Rows: {rows}; bad rows: {bad_rows}")
    print(f"[OK] Distinct themes: {len(freq)}")
    print(f"[OK] Lookup themes parsed: {len(lookup)}")
    if lookup_error:
        print(f"[WARN] Lookup unavailable: {lookup_error}")
    print(f"[OK] Report written: {out}")
    print("[OK] Analysis only; production data unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
