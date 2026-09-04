import io
import zipfile
import tempfile
from validate_gkg import validate_zip


def make_fixture():
    rows = [
        ["20260904081500-1", "20260904080000", "1", "example.com", "https://example.com/a", "", "", "ECON_INFLATION;ECON_PRICES", "", "", "", "-1,2,0,0,0,0,0,0,0,0"],
        ["20260904081500-2", "20260904080000", "1", "example.org", "https://example.org/b", "", "", "ARMED_CONFLICT;ECON_INFLATION", "", "", "", "1,1,0,0,0,0,0,0,0,0"],
    ]
    payload = "".join("\t".join(row) + "\n" for row in rows).encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("20260904081500.gkg.csv", payload)
    return buf.getvalue()


def test_fixture():
    report = validate_zip(make_fixture())
    assert report["rows"] == 2
    assert report["bad_rows"] == 0
    assert report["theme_counts"]["ECON_INFLATION"] == 2
    assert report["theme_counts"]["ARMED_CONFLICT"] == 1
    assert report["field_count_distribution"][12] == 2
    print("test_validate_gkg: PASS")


if __name__ == "__main__":
    test_fixture()
