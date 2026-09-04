#!/usr/bin/env python3
"""Offline tests for evaluate_gkg_stability.py."""
from __future__ import annotations

import evaluate_gkg_stability as mod


def batch(day, rate, rows=1000):
    return {
        "analysis_version": "V0.2.1-C",
        "source": {"gkg": f"https://example/{day}.gkg.csv.zip"},
        "dataset": {"rows": rows, "bad_rows": 0},
        "topics": {
            "Economic": {
                "all_rate_per_1000_documents": rate,
                "primary_rate_per_1000_documents": rate / 2,
                "secondary_rate_per_1000_documents": rate / 2,
            }
        },
    }


def main():
    batches = [batch(i, rate) for i, rate in enumerate([10, 12, 11, 9, 10, 13, 11], start=1)]
    report = mod.evaluate(batches, target_days=14, minimum_days=7)
    assert report["window"]["valid_batches"] == 7
    assert report["window"]["unique_sources"] == 7
    assert report["window"]["status"] == "minimum_window_reached"
    econ = report["topics"]["Economic"]
    assert econ["samples"] == 7
    assert econ["all_rate_per_1000"]["min"] == 9
    assert econ["all_rate_per_1000"]["max"] == 13
    assert econ["interpretation"] == "ready_for_manual_review"

    report2 = mod.evaluate(batches[:3], target_days=14, minimum_days=7)
    assert report2["window"]["status"] == "collecting"
    assert report2["topics"]["Economic"]["interpretation"] == "collecting"

    print("test_evaluate_gkg_stability: PASS")


if __name__ == "__main__":
    main()
