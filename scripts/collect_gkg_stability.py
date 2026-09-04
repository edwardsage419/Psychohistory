#!/usr/bin/env python3
"""Collect one immutable GKG batch summary for V0.2.1-C stability validation.

Analysis-only. This script never changes production data. Each batch stores
normalized topic coverage plus the underlying mapped Theme counts so later
runs can measure day-to-day stability without re-downloading old batches.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_MAPPING = HERE / "gkg_theme_mapping.json"
DEFAULT_OUTDIR = HERE / "gkg_stability_history"


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Psychohistory/0.2.1-C"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def discover_latest_gkg_url() -> str:
    url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
    text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8", errors="replace")
    candidates = []
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[-1].endswith(".gkg.csv.zip"):
            if parts[-1].startswith(("http://", "https://")):
                candidates.append(parts[-1])
    if not candidates:
        raise RuntimeError("No GKG .gkg.csv.zip URL found in lastupdate.txt")
    return candidates[-1]


def iter_gkg_rows(blob: bytes):
    with zipfile.ZipFile(__import__("io").BytesIO(blob)) as zf:
        members = [n for n in zf.namelist() if not n.endswith("/")]
        if len(members) != 1:
            raise RuntimeError(f"Expected one GKG member, found {len(members)}")
        with zf.open(members[0], "r") as fh:
            for raw in fh:
                yield raw.decode("utf-8", errors="replace").rstrip("\r\n")


def topic_sets(mapping: dict):
    result = {}
    for topic, cfg in mapping["topics"].items():
        result[topic] = {
            "primary": {x["code"] for x in cfg.get("primary_themes", [])},
            "secondary": {x["code"] for x in cfg.get("secondary_themes", [])},
            "excluded": {x["code"] for x in cfg.get("excluded_themes", [])},
        }
    return result


def analyze_lines(lines, mapping):
    topics = topic_sets(mapping)
    mapped_codes = set().union(*(
        groups["primary"] | groups["secondary"] | groups["excluded"]
        for groups in topics.values()
    ))
    theme_freq = Counter()
    topic_stats = {
        topic: {
            "primary_theme_document_counts": Counter(),
            "secondary_theme_document_counts": Counter(),
            "excluded_theme_document_counts": Counter(),
            "primary_union_documents": 0,
            "secondary_union_documents": 0,
            "all_union_documents": 0,
        }
        for topic in topics
    }
    rows = 0
    bad_rows = 0
    dates = Counter()

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
        themes = {x.strip() for x in fields[7].split(";") if x.strip()}
        theme_freq.update(themes)
        observed_mapped = themes & mapped_codes
        for topic, groups in topics.items():
            p = observed_mapped & groups["primary"]
            s = observed_mapped & groups["secondary"]
            e = observed_mapped & groups["excluded"]
            if p:
                topic_stats[topic]["primary_union_documents"] += 1
            if s:
                topic_stats[topic]["secondary_union_documents"] += 1
            if p or s:
                topic_stats[topic]["all_union_documents"] += 1
            for code in p:
                topic_stats[topic]["primary_theme_document_counts"][code] += 1
            for code in s:
                topic_stats[topic]["secondary_theme_document_counts"][code] += 1
            for code in e:
                topic_stats[topic]["excluded_theme_document_counts"][code] += 1

    return rows, bad_rows, dates, theme_freq, topic_stats


def serialize_topic_stats(stats, rows):
    out = {}
    for topic, value in stats.items():
        primary = dict(sorted(value["primary_theme_document_counts"].items()))
        secondary = dict(sorted(value["secondary_theme_document_counts"].items()))
        excluded = dict(sorted(value["excluded_theme_document_counts"].items()))
        out[topic] = {
            "primary_theme_document_counts": primary,
            "secondary_theme_document_counts": secondary,
            "excluded_theme_document_counts": excluded,
            "primary_union_documents": value["primary_union_documents"],
            "secondary_union_documents": value["secondary_union_documents"],
            "all_union_documents": value["all_union_documents"],
            "primary_rate_per_1000_documents": round(value["primary_union_documents"] / rows * 1000, 4) if rows else 0.0,
            "secondary_rate_per_1000_documents": round(value["secondary_union_documents"] / rows * 1000, 4) if rows else 0.0,
            "all_rate_per_1000_documents": round(value["all_union_documents"] / rows * 1000, 4) if rows else 0.0,
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gkg-url")
    ap.add_argument("--gkg-file")
    ap.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    ap.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    ap.add_argument("--label", help="Stable filename label, e.g. 20260904-111500")
    args = ap.parse_args()

    mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8"))
    if args.gkg_file:
        blob = Path(args.gkg_file).read_bytes()
        source = str(Path(args.gkg_file))
    else:
        source = args.gkg_url or discover_latest_gkg_url()
        blob = download_bytes(source)

    rows, bad_rows, dates, freq, topic_stats = analyze_lines(iter_gkg_rows(blob), mapping)
    if rows == 0 or bad_rows:
        raise RuntimeError(f"Unsafe batch: rows={rows}, bad_rows={bad_rows}")

    generated = datetime.now(timezone.utc)
    label = args.label or generated.strftime("%Y%m%d-%H%M%S")
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"{label}.json"
    report = {
        "analysis_version": "V0.2.1-C",
        "generated_at_utc": generated.isoformat(),
        "source": {"gkg": source},
        "dataset": {
            "rows": rows,
            "bad_rows": bad_rows,
            "dates": dict(dates),
            "distinct_themes": len(freq),
        },
        "topics": serialize_topic_stats(topic_stats, rows),
        "method": {
            "theme_frequency": "each V1THEMES code counts at most once per document",
            "topic_union": "a document counts once for a topic if it contains at least one Theme in that topic group",
            "normalization": "union document counts per 1000 valid GKG documents",
            "production_status": "analysis_only",
            "stability_window_target_days": 14,
        },
    }
    outfile.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] GKG source: {source}")
    print(f"[OK] Rows: {rows}; bad rows: {bad_rows}")
    print(f"[OK] Distinct themes: {len(freq)}")
    print(f"[OK] Batch summary: {outfile}")
    print("[OK] Analysis only; production data unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
