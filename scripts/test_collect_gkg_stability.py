#!/usr/bin/env python3
"""Offline tests for collect_gkg_stability.py."""
from __future__ import annotations

import json
from pathlib import Path

import collect_gkg_stability as mod


def row(date, themes):
    fields = [f"f{i}" for i in range(27)]
    fields[1] = date
    fields[7] = themes
    return "\t".join(fields)


def main():
    mapping = {
        "topics": {
            "Economic": {
                "primary_themes": [{"code": "EPU_ECONOMY"}],
                "secondary_themes": [{"code": "ECON_INFLATION"}],
                "excluded_themes": [{"code": "ARMEDCONFLICT"}],
            }
        }
    }
    lines = [
        row("20260904081500", "EPU_ECONOMY;EPU_ECONOMY;ECON_INFLATION"),
        row("20260904081500", "EPU_ECONOMY;ARMEDCONFLICT"),
        row("20260904083000", "ECON_INFLATION"),
        "bad\trow",
    ]
    rows, bad, dates, freq, stats = mod.analyze_lines(lines, mapping)
    assert rows == 3
    assert bad == 1
    assert freq["EPU_ECONOMY"] == 2
    assert freq["ECON_INFLATION"] == 2
    assert freq["ARMEDCONFLICT"] == 1
    assert dates["20260904"] == 3

    economic = stats["Economic"]
    assert economic["primary_union_documents"] == 2
    assert economic["secondary_union_documents"] == 2
    assert economic["all_union_documents"] == 3
    assert economic["primary_theme_document_counts"]["EPU_ECONOMY"] == 2
    assert economic["secondary_theme_document_counts"]["ECON_INFLATION"] == 2
    assert economic["excluded_theme_document_counts"]["ARMEDCONFLICT"] == 1

    serialized = mod.serialize_topic_stats(stats, rows)
    assert serialized["Economic"]["primary_rate_per_1000_documents"] == 666.6667
    assert serialized["Economic"]["all_rate_per_1000_documents"] == 1000.0

    tmp = Path("stability_test_mapping.json")
    tmp.write_text(json.dumps(mapping), encoding="utf-8")
    try:
        assert json.loads(tmp.read_text(encoding="utf-8"))["topics"]["Economic"]["primary_themes"][0]["code"] == "EPU_ECONOMY"
    finally:
        tmp.unlink(missing_ok=True)

    print("test_collect_gkg_stability: PASS")


if __name__ == "__main__":
    main()
