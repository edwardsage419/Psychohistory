#!/usr/bin/env python3
"""Offline tests for analyze_gkg_themes.py. No network access required."""
from __future__ import annotations

import io
import json
import tempfile
import zipfile
from pathlib import Path

import analyze_gkg_themes as mod


def make_zip(lines):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("sample.gkg.csv", "\n".join(lines) + "\n")
    return bio.getvalue()


def row(date, themes):
    fields = [f"f{i}" for i in range(27)]
    fields[1] = date
    fields[7] = themes
    return "\t".join(fields)


def main():
    lines = [
        row("20260904081500", "ECON_INFLATION;ECON_INFLATION;EPU_ECONOMY"),
        row("20260904081500", "ARMEDCONFLICT;SCIENCE;UNKNOWN_THEME"),
        row("20260904083000", ""),
        "bad\trow",
    ]
    freq, rows, dates, samples, bad = mod.analyze_rows(lines, {})
    assert rows == 3, rows
    assert bad == 1, bad
    assert freq["ECON_INFLATION"] == 1, freq
    assert freq["EPU_ECONOMY"] == 1, freq
    assert freq["ARMEDCONFLICT"] == 1, freq
    assert freq["UNKNOWN_THEME"] == 1, freq
    assert dates["20260904"] == 3, dates
    assert len(samples) == 3

    mapping = {
        "topics": {
            "Economic": {
                "primary_themes": [{"code": "EPU_ECONOMY"}],
                "secondary_themes": [{"code": "ECON_INFLATION"}],
                "excluded_themes": [{"code": "ARMEDCONFLICT"}],
            }
        }
    }
    sets = mod.topic_sets(mapping)
    assert sets["Economic"]["primary"] == ["EPU_ECONOMY"]
    assert sets["Economic"]["secondary"] == ["ECON_INFLATION"]
    assert sets["Economic"]["excluded"] == ["ARMEDCONFLICT"]

    lookup = mod.parse_lookup("# comment\nEPU_ECONOMY\tEconomy\t123\nECON_INFLATION\tInflation\t456\n")
    assert lookup["EPU_ECONOMY"]["description"] == "Economy"
    assert lookup["EPU_ECONOMY"]["lookup_count"] == 123

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sample.zip"
        p.write_bytes(make_zip(lines[:3]))
        extracted = list(mod.iter_gkg_rows(p.read_bytes()))
        assert len(extracted) == 3
        assert extracted[0].split("\t")[7].count("ECON_INFLATION") == 2

    print("test_analyze_gkg_themes: PASS")


if __name__ == "__main__":
    main()
