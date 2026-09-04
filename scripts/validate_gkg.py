#!/usr/bin/env python3
"""
Psychohistory V0.2.1-A: GDELT GKG acquisition/format validator.

This stage deliberately does NOT modify data/gdelt.json and does NOT build
production topic indicators. It downloads one GKG 2.1 batch, validates the
file structure, streams the rows, and reports the observed V1THEMES codes.

Usage:
  python scripts/validate_gkg.py
  python scripts/validate_gkg.py --url https://data.gdeltproject.org/gdeltv2/....gkg.csv.zip
  python scripts/validate_gkg.py --date 2026-09-04

The script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone

BASE_URL = "https://data.gdeltproject.org/gdeltv2/"
LASTUPDATE_URL = BASE_URL + "lastupdate.txt"
USER_AGENT = "Psychohistory-GKG-Validator/0.2.1"
TIMEOUT = 60
EXPECTED_MIN_FIELDS = 8
V1THEMES_INDEX = 7  # zero-based: GKG 2.1 field 8


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return response.read()


def discover_latest_url() -> tuple[str, str]:
    raw = fetch_bytes(LASTUPDATE_URL).decode("utf-8", errors="replace")
    for line in raw.splitlines():
        parts = line.split()
        for token in parts:
            if token.endswith(".gkg.csv.zip"):
                return token, line
    raise RuntimeError("Could not find a GKG .zip URL in lastupdate.txt")


def parse_theme_field(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def validate_zip(blob: bytes) -> dict:
    result = {
        "zip_bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "members": [],
        "rows": 0,
        "bad_rows": 0,
        "field_count_distribution": Counter(),
        "theme_counts": Counter(),
        "date_counts": Counter(),
        "sample_rows": [],
    }

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        members = [info for info in zf.infolist() if not info.is_dir()]
        result["members"] = [
            {"name": info.filename, "compressed": info.compress_size, "uncompressed": info.file_size}
            for info in members
        ]
        if len(members) != 1:
            raise ValueError(f"Expected exactly one data member, found {len(members)}")

        info = members[0]
        with zf.open(info, "r") as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline="")
            reader = csv.reader(text, delimiter="\t")
            for row in reader:
                result["rows"] += 1
                field_count = len(row)
                result["field_count_distribution"][field_count] += 1
                if field_count < EXPECTED_MIN_FIELDS:
                    result["bad_rows"] += 1
                    continue

                date_value = row[1]
                result["date_counts"][date_value] += 1
                themes = parse_theme_field(row[V1THEMES_INDEX])
                result["theme_counts"].update(themes)
                if len(result["sample_rows"]) < 3:
                    result["sample_rows"].append({
                        "gkg_record_id": row[0],
                        "date": row[1],
                        "source_collection": row[2],
                        "source_common_name": row[3],
                        "document_identifier": row[4],
                        "v1themes_sample": themes[:20],
                    })

    if result["rows"] == 0:
        raise ValueError("GKG archive contains no rows")
    if result["bad_rows"]:
        raise ValueError(f"Found {result['bad_rows']} rows with fewer than {EXPECTED_MIN_FIELDS} fields")

    return result


def serializable_counter(counter: Counter, limit: int | None = None) -> dict:
    items = counter.most_common(limit)
    return {key: value for key, value in items}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Specific GDELT GKG .gkg.csv.zip URL")
    parser.add_argument("--date", help="YYYY-MM-DD; currently used only for reporting")
    parser.add_argument("--top-themes", type=int, default=100)
    args = parser.parse_args()

    run_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.url:
        url = args.url
        discovery_line = None
    else:
        url, discovery_line = discover_latest_url()

    print(f"[GKG] URL: {url}")
    print("[GKG] Downloading...")
    try:
        blob = fetch_bytes(url)
    except urllib.error.HTTPError as exc:
        print(f"[ERROR] HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except urllib.error.URLError as exc:
        print(f"[ERROR] Network error: {exc.reason}", file=sys.stderr)
        return 2

    print(f"[GKG] Downloaded: {len(blob):,} bytes")
    try:
        report = validate_zip(blob)
    except (zipfile.BadZipFile, ValueError, UnicodeError) as exc:
        print(f"[ERROR] Validation failed: {exc}", file=sys.stderr)
        return 3

    report_out = {
        "validator_version": "V0.2.1-A",
        "validated_at": run_at,
        "source_url": url,
        "discovery_line": discovery_line,
        "requested_date": args.date,
        "zip_bytes": report["zip_bytes"],
        "sha256": report["sha256"],
        "members": report["members"],
        "rows": report["rows"],
        "bad_rows": report["bad_rows"],
        "field_count_distribution": serializable_counter(report["field_count_distribution"]),
        "date_counts": serializable_counter(report["date_counts"], 10),
        "top_v1themes": serializable_counter(report["theme_counts"], args.top_themes),
        "sample_rows": report["sample_rows"],
    }

    print(f"[OK] Rows: {report['rows']:,}")
    print(f"[OK] Bad rows: {report['bad_rows']}")
    print(f"[OK] Field counts: {serializable_counter(report['field_count_distribution'])}")
    print("[OK] Top V1THEMES:")
    for theme, count in report["theme_counts"].most_common(args.top_themes):
        print(f"  {theme}\t{count}")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gkg_validation_report.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"[OK] Report written: {output_path}")
    print("[OK] V0.2.1-A validation passed. No production data was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
