#!/usr/bin/env python3
"""Evaluate day-to-day stability of collected GKG topic summaries.

Analysis-only. Produces descriptive statistics and a conservative readiness
status. It never changes production data and does not promote any topic to a
production index automatically.

A stability window is measured in distinct UTC calendar days, not raw batch
count. If multiple batches are collected on the same UTC day, only the latest
valid batch for that day is used for the day-level stability statistics. This
prevents manual reruns from falsely satisfying the 7/14-day window.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_HISTORY = Path(__file__).resolve().parent / "gkg_stability_history"
DEFAULT_REPORT = Path(__file__).resolve().parent / "gkg_stability_report.json"
SOURCE_STAMP_RE = re.compile(r"/(\d{14})\.gkg\.csv\.zip(?:$|[?#])")


def mean(values):
    return sum(values) / len(values) if values else 0.0


def stdev(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def source_sort_key(batch):
    source = batch.get("source", {}).get("gkg", "")
    match = SOURCE_STAMP_RE.search(source)
    if match:
        return match.group(1)
    return batch.get("generated_at_utc", "")


def batch_utc_date(batch):
    source = batch.get("source", {}).get("gkg", "")
    match = SOURCE_STAMP_RE.search(source)
    if match:
        return match.group(1)[:8]

    dates = batch.get("dataset", {}).get("dates", {})
    valid_dates = sorted(str(d) for d, count in dates.items() if count)
    if valid_dates:
        return valid_dates[-1]

    generated = batch.get("generated_at_utc")
    if generated:
        try:
            return datetime.fromisoformat(generated.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y%m%d")
        except ValueError:
            pass
    return None


def load_batches(history: Path):
    batches = []
    for path in sorted(history.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("analysis_version") == "V0.2.1-C":
                batches.append(data)
        except (OSError, json.JSONDecodeError):
            continue
    return batches


def valid_batches_by_day(batches):
    """Return one latest valid batch per UTC calendar day."""
    selected = {}
    for batch in batches:
        dataset = batch.get("dataset", {})
        if dataset.get("rows", 0) <= 0 or dataset.get("bad_rows", 1) != 0:
            continue
        day = batch_utc_date(batch)
        if not day:
            continue
        previous = selected.get(day)
        if previous is None or source_sort_key(batch) > source_sort_key(previous):
            selected[day] = batch
    return dict(sorted(selected.items()))


def evaluate(batches, target_days=14, minimum_days=7):
    daily = valid_batches_by_day(batches)
    daily_batches = list(daily.values())
    topics = sorted({topic for b in daily_batches for topic in b.get("topics", {})})
    topic_report = {}
    for topic in topics:
        rates = [b["topics"][topic]["all_rate_per_1000_documents"] for b in daily_batches if topic in b.get("topics", {})]
        primary = [b["topics"][topic]["primary_rate_per_1000_documents"] for b in daily_batches if topic in b.get("topics", {})]
        secondary = [b["topics"][topic]["secondary_rate_per_1000_documents"] for b in daily_batches if topic in b.get("topics", {})]
        if rates:
            m = mean(rates)
            sd = stdev(rates)
            cv = sd / m if m else None
            lo, hi = min(rates), max(rates)
        else:
            m = sd = lo = hi = 0.0
            cv = None
        topic_report[topic] = {
            "samples": len(rates),
            "all_rate_per_1000": {
                "mean": round(m, 4),
                "stdev": round(sd, 4),
                "cv": round(cv, 4) if cv is not None else None,
                "min": round(lo, 4),
                "max": round(hi, 4),
            },
            "primary_rate_mean_per_1000": round(mean(primary), 4),
            "secondary_rate_mean_per_1000": round(mean(secondary), 4),
            "interpretation": "collecting" if len(rates) < minimum_days else "ready_for_manual_review",
        }

    valid_batches = [
        b for b in batches
        if b.get("dataset", {}).get("rows", 0) > 0
        and b.get("dataset", {}).get("bad_rows", 1) == 0
    ]
    unique_sources = len({b.get("source", {}).get("gkg") for b in valid_batches})
    daily_sample_count = len(daily_batches)
    enough = daily_sample_count >= minimum_days
    target_reached = daily_sample_count >= target_days
    status = "target_reached" if target_reached else ("minimum_window_reached" if enough else "collecting")
    return {
        "analysis_version": "V0.2.1-C",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "window": {
            "valid_batches": len(valid_batches),
            "daily_samples": daily_sample_count,
            "sample_dates_utc": list(daily.keys()),
            "unique_sources": unique_sources,
            "minimum_days": minimum_days,
            "target_days": target_days,
            "status": status,
            "selection_rule": "latest valid GKG batch per UTC calendar day",
        },
        "topics": topic_report,
        "method": {
            "normalization": "topic union documents per 1000 valid GKG documents",
            "cv_definition": "sample standard deviation divided by mean; descriptive only",
            "stability_window": "distinct UTC calendar days, not raw batch count",
            "production_decision": "manual review required; no automatic promotion",
            "analysis_only": True,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", default=str(DEFAULT_HISTORY))
    ap.add_argument("--report", default=str(DEFAULT_REPORT))
    ap.add_argument("--target-days", type=int, default=14)
    ap.add_argument("--minimum-days", type=int, default=7)
    args = ap.parse_args()

    if args.minimum_days <= 0 or args.target_days < args.minimum_days:
        raise SystemExit("--target-days must be >= --minimum-days, and --minimum-days must be positive")

    batches = load_batches(Path(args.history))
    report = evaluate(batches, args.target_days, args.minimum_days)
    out = Path(args.report)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Valid batches: {report['window']['valid_batches']}")
    print(f"[OK] Distinct UTC days: {report['window']['daily_samples']}")
    print(f"[OK] Stability status: {report['window']['status']}")
    print(f"[OK] Report written: {out}")
    print("[OK] Analysis only; no production promotion performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
