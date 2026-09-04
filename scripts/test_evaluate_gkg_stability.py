#!/usr/bin/env python3
"""Offline tests for evaluate_gkg_stability.py."""
from __future__ import annotations

import evaluate_gkg_stability as mod


def batch(timestamp, rate, rows=1000):
    return {
        "analysis_version": "V0.2.1-C",
        "source": {"gkg": f"https://example/{timestamp}.gkg.csv.zip"},
        "dataset": {"rows": rows, "bad_rows": 0, "dates": {timestamp[:8]: rows}},
        "topics": {
            "Economic": {
                "all_rate_per_1000_documents": rate,
                "primary_rate_per_1000_documents": rate / 2,
                "secondary_rate_per_1000_documents": rate / 2,
            }
        },
    }


def main():
    timestamps = [
        "20260901000000",
        "20260902000000",
        "20260903000000",
        "20260904000000",
        "20260905000000",
        "20260906000000",
        "20260907000000",
    ]
    batches = [batch(ts, rate) for ts, rate in zip(timestamps, [10, 12, 11, 9, 10, 13, 11])]
    report = mod.evaluate(batches, target_days=14, minimum_days=7)
    assert report["window"]["valid_batches"] == 7
    assert report["window"]["daily_samples"] == 7
    assert report["window"]["sample_dates_utc"] == [ts[:8] for ts in timestamps]
    assert report["window"]["unique_sources"] == 7
    assert report["window"]["status"] == "minimum_window_reached"
    econ = report["topics"]["Economic"]
    assert econ["samples"] == 7
    assert econ["all_rate_per_1000"]["min"] == 9
    assert econ["all_rate_per_1000"]["max"] == 13
    assert econ["interpretation"] == "ready_for_manual_review"

    # Multiple snapshots on one UTC day must count as one day, using the latest batch.
    duplicate_day = batch("20260907120000", 99)
    report2 = mod.evaluate(batches + [duplicate_day], target_days=14, minimum_days=7)
    assert report2["window"]["valid_batches"] == 8
    assert report2["window"]["daily_samples"] == 7
    assert report2["topics"]["Economic"]["samples"] == 7
    assert report2["topics"]["Economic"]["all_rate_per_1000"]["max"] == 99

    report3 = mod.evaluate(batches[:3], target_days=14, minimum_days=7)
    assert report3["window"]["status"] == "collecting"
    assert report3["topics"]["Economic"]["interpretation"] == "collecting"

    print("test_evaluate_gkg_stability: PASS")


if __name__ == "__main__":
    main()
