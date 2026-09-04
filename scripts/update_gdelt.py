#!/usr/bin/env python3
"""
Psychohistory V0.2 — GDELT data acquisition script.

Fetches daily media-coverage-volume for a fixed set of topics from the
GDELT DOC 2.0 API (timelinevol mode) and writes the result to
data/gdelt.json. Runs from .github/workflows/update-gdelt.yml.

IMPORTANT — what "value" means:
    GDELT's timelinevol mode returns, for each time bucket, the
    percentage of ALL articles monitored by GDELT that match the query.
    It is a MEDIA COVERAGE VOLUME metric, not a measure of real-world
    risk, severity, or how much the underlying event is "actually"
    happening. The frontend must not describe it as anything else.

Design goals (see project spec V0.2, sections 15/17/18/24/27):
  - No single topic failure aborts the whole run; other topics still
    get saved.
  - No fabricated data: a failed topic keeps its LAST KNOWN GOOD value
    and is explicitly marked "status": "failed" with an error message.
    The frontend is responsible for showing that to the user.
  - No duplicate history rows for the same UTC calendar day — running
    workflow_dispatch twice in one day updates that day's row in place
    instead of appending a second one.
  - No future data leakage: every history row records its own
    observation date (UTC calendar day) and the UTC timestamp it was
    retrieved at, so later phases (V0.7 backtesting) can trust that a
    row only reflects data available at that point in time.

Why GDELT DOC 2.0 API and not GDELT's raw bulk files (GKG/Events)?
    Bulk GKG/Event files are the most rate-limit-proof option long
    term, but require downloading and parsing ~96 files/day and mapping
    our 7 topics onto GDELT's 275+ official GKG theme codes correctly
    (not guessed), which is a heavier V0.3+ migration.

    A first real run on GitHub-hosted runners (2026-09-03) showed 6 of
    7 topics failing with "HTTP 429: Too Many Requests" and one with an
    SSL handshake timeout, with exactly 1 of 7 succeeding. A rate limit
    that lets through roughly 1 in 7 requests spaced 15s apart, rather
    than blocking all of them, behaves like a sliding-window limiter
    with occasional free slots — not a hard per-IP block. That justifies
    trying a properly rate-limit-aware backoff before abandoning this
    API for the heavier GKG migration:
      - topic-to-topic spacing increased from 15s to 45s + jitter,
      - on HTTP 429 specifically, honor the `Retry-After` response
        header when GDELT sends one, otherwise wait ~60s+jitter,
      - other errors (timeouts, SSL, DNS) use exponential backoff,
      - up to 3 attempts per topic instead of 2.
    If this still fails most of the time, the next step is the GKG
    migration described above — the JSON schema this script writes is
    designed so that migration would not require changing the frontend.
"""


import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data", "gdelt.json")

TREND_THRESHOLD = 10  # percentage points — see spec section 11

TOPICS = [
    {"name": "Economic", "query": "economy OR economic OR recession"},
    {"name": "Geopolitics", "query": "geopolitics OR geopolitical"},
    {"name": "Technology", "query": "technology"},
    {"name": "Energy", "query": "energy crisis OR energy prices OR energy supply"},
    {"name": "War & Conflict", "query": "war OR conflict OR military conflict"},
    {"name": "Inflation", "query": "inflation"},
    {"name": "AI", "query": "\"artificial intelligence\" OR \"AI model\" OR \"AI regulation\""},
]

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
REQUEST_TIMEOUT = 20        # seconds
REQUEST_SPACING = 45        # seconds between topic requests (base; jitter added)
SPACING_JITTER = 15         # up to +N extra random seconds between topics
MAX_ATTEMPTS = 3            # 1 try + 2 retries per topic
DEFAULT_RATE_LIMIT_WAIT = 60   # seconds to wait on HTTP 429 if no Retry-After given
GENERIC_BACKOFF_BASE = 10      # seconds; doubles each retry for non-429 errors
GENERIC_BACKOFF_CAP = 60       # seconds; ceiling for the exponential backoff


def utc_now():
    return datetime.now(timezone.utc)


def today_str():
    return utc_now().strftime("%Y-%m-%d")


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def compute_backoff_seconds(attempt, exc):
    """
    Decides how long to sleep before retrying, based on what just failed.

    - HTTP 429: honor GDELT's `Retry-After` header if it sent one;
      otherwise assume a long cooldown is needed (DEFAULT_RATE_LIMIT_WAIT).
    - Everything else (timeout, SSL, DNS, other HTTP errors): exponential
      backoff, capped, with a little jitter so parallel-ish workflow runs
      don't all retry at the exact same moment.
    """
    if isinstance(exc, urllib.error.HTTPError) and exc.code == 429:
        retry_after = None
        try:
            if exc.headers:
                retry_after = exc.headers.get("Retry-After")
        except Exception:
            retry_after = None
        if retry_after:
            try:
                return min(float(retry_after), 180) + random.uniform(0, 5)
            except ValueError:
                pass
        return DEFAULT_RATE_LIMIT_WAIT + random.uniform(0, 15)

    backoff = min(GENERIC_BACKOFF_BASE * (2 ** (attempt - 1)), GENERIC_BACKOFF_CAP)
    return backoff + random.uniform(0, 5)


def fetch_timeline(query):
    """
    Calls the GDELT DOC 2.0 API in timelinevol mode for the last 8 days.
    Returns a list of (YYYYMMDD_str, value_float) tuples on success.
    Raises on ANY failure — network error, non-200 status, non-JSON
    body, or a JSON body that doesn't have the shape we expect.
    """
    params = {
        "query": query,
        "mode": "timelinevol",
        "format": "json",
        "timespan": "8days",
    }
    url = GDELT_ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        status = resp.status
        raw = resp.read()

    if status != 200:
        raise RuntimeError(f"HTTP {status}")

    text = raw.decode("utf-8", errors="replace").strip()
    if not text or text.lstrip().startswith("<"):
        raise ValueError("Empty or non-JSON response body")

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as e:
        # GDELT is known to return HTTP 200 with a plain-text error
        # sentence (e.g. rate limit messages) instead of JSON.
        raise ValueError(f"Invalid JSON (likely a GDELT text error): {e}") from e

    timeline = payload.get("timeline")
    if not timeline or not isinstance(timeline, list):
        raise ValueError("Unexpected response shape: missing 'timeline'")

    series = timeline[0].get("data")
    if not series or not isinstance(series, list):
        raise ValueError("Unexpected response shape: missing timeline data")

    points = []
    for point in series:
        raw_date = point.get("date")
        raw_value = point.get("value")
        if raw_date is None or raw_value is None:
            continue
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            continue
        if value < 0:
            continue  # a negative "% of coverage" is not physically valid
        day = str(raw_date)[:8]  # GDELT timestamps look like YYYYMMDDHHMMSS
        points.append((day, value))

    if not points:
        raise ValueError("No usable data points in response")

    return points


def daily_averages(points):
    """Collapses sub-daily buckets into one average value per UTC day."""
    by_day = {}
    for day, value in points:
        by_day.setdefault(day, []).append(value)
    return {day: sum(vals) / len(vals) for day, vals in by_day.items()}


def compute_topic_result(points):
    daily = daily_averages(points)
    days_sorted = sorted(daily.keys())
    if not days_sorted:
        raise ValueError("No daily data after aggregation")

    latest_day = days_sorted[-1]
    current = daily[latest_day]

    last7 = days_sorted[-7:]
    seven_day_avg = sum(daily[d] for d in last7) / len(last7)

    if seven_day_avg == 0:
        change_percent = 0.0
    else:
        change_percent = ((current - seven_day_avg) / seven_day_avg) * 100

    if change_percent >= TREND_THRESHOLD:
        trend = "rising"
    elif change_percent <= -TREND_THRESHOLD:
        trend = "falling"
    else:
        trend = "stable"

    return {
        "value": round(current, 4),
        "7_day_average": round(seven_day_avg, 4),
        "change_percent": round(change_percent, 2),
        "trend": trend,
    }


def load_existing():
    if not os.path.exists(DATA_PATH):
        return {"metadata": {}, "current": {}, "history": []}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # Corrupt or unreadable file: start fresh rather than crash,
        # but never fabricate topic values (current stays empty).
        return {"metadata": {}, "current": {}, "history": []}
    data.setdefault("metadata", {})
    data.setdefault("current", {})
    data.setdefault("history", [])
    return data


def save(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    tmp_path = DATA_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp_path, DATA_PATH)  # atomic on POSIX


def main():
    store = load_existing()
    run_time = utc_now()
    today = today_str()

    today_topics = {}
    any_success = False

    for topic in TOPICS:
        name = topic["name"]
        prev = store["current"].get(name, {})
        result_entry = None
        last_error = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                points = fetch_timeline(topic["query"])
                computed = compute_topic_result(points)
                result_entry = {
                    **computed,
                    "status": "ok",
                    "last_success_at": iso(run_time),
                    "error": None,
                }
                any_success = True
                break
            except Exception as e:  # noqa: BLE001 (deliberately broad; see module docstring)
                last_error = f"{type(e).__name__}: {e}"
                if attempt < MAX_ATTEMPTS:
                    delay = compute_backoff_seconds(attempt, e)
                    print(f"[RETRY] {name}: attempt {attempt} failed ({last_error}); waiting {delay:.0f}s")
                    time.sleep(delay)

        if result_entry is None:
            # Every attempt failed for this topic: keep the previous
            # known-good value, mark it clearly as stale/failed.
            result_entry = {
                "value": prev.get("value"),
                "7_day_average": prev.get("7_day_average"),
                "change_percent": prev.get("change_percent"),
                "trend": prev.get("trend"),
                "status": "failed",
                "last_success_at": prev.get("last_success_at"),
                "error": last_error,
            }
            print(f"[WARN] {name}: FAILED — {last_error}")
        else:
            print(f"[OK]   {name}: {result_entry['value']}")

        store["current"][name] = result_entry
        today_topics[name] = {
            "value": result_entry["value"],
            "status": result_entry["status"],
        }

        time.sleep(REQUEST_SPACING + random.uniform(0, SPACING_JITTER))

    # ---- history: one row per UTC calendar day, updated in place ----
    history = store["history"]
    existing_idx = next(
        (i for i, row in enumerate(history) if row.get("date") == today), None
    )
    history_row = {
        "date": today,                 # observation_date: UTC calendar day
        "retrieved_at": iso(run_time), # exact UTC timestamp of this run
        "topics": today_topics,
    }
    if existing_idx is not None:
        history[existing_idx] = history_row
    else:
        history.append(history_row)
    history.sort(key=lambda r: r["date"])

    store["history"] = history
    store["metadata"] = {
        "source": "GDELT DOC 2.0 API (timelinevol mode)",
        "updated_at": iso(run_time),
        "topics": [t["name"] for t in TOPICS],
        "trend_threshold_percent": TREND_THRESHOLD,
        "value_definition": (
            "value 表示该主题查询词匹配到的新闻，占 GDELT 监测的全球新闻总量的"
            "百分比（媒体报道量占比），是媒体关注度的代理指标，"
            "不代表事件真实发生的程度、严重性或风险水平。"
        ),
        "system_version": "V0.2",
        "last_run_status": "ok" if any_success else "all_failed",
    }

    save(store)

    ok_count = sum(1 for t in today_topics.values() if t["status"] == "ok")
    print("\n[GDELT] Fetch Summary")
    for t in TOPICS:
        name = t["name"]
        status = today_topics[name]["status"]
        print(f"  {name}: {'SUCCESS' if status == 'ok' else 'FAILED'}")
    print(f"  Total: {len(TOPICS)}  Success: {ok_count}  Failed: {len(TOPICS) - ok_count}")

    if not any_success:
        # Exit 0 on purpose: a transient GDELT-wide outage shouldn't
        # show as a broken workflow run every single day, and the
        # previous good data is still preserved in data/gdelt.json.
        # The failure is visible in the Action logs and in
        # metadata.last_run_status for the frontend to surface.
        print("[ERROR] All topics failed this run. Previous data preserved.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
