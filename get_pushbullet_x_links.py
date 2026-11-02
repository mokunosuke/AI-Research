"""Print X links received in Pushbullet yesterday (Asia/Tokyo), using stdlib only."""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, time, timedelta, timezone


def main() -> int:
    token = os.environ.get("PUSHBULLET_ACCESS_TOKEN")
    if not token and os.name == "nt":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                token, _ = winreg.QueryValueEx(key, "PUSHBULLET_ACCESS_TOKEN")
        except OSError:
            token = None
    if not token:
        print("PUSHBULLET_ACCESS_TOKEN is not set.", file=sys.stderr)
        return 1

    # Japan does not use daylight saving time, so a fixed UTC+09:00 is sufficient.
    tz = timezone(timedelta(hours=9), name="Asia/Tokyo")
    yesterday = datetime.now(tz).date() - timedelta(days=1)
    start = datetime.combine(yesterday, time.min, tzinfo=tz)
    end = start + timedelta(days=1)
    start_ts = start.astimezone(timezone.utc).timestamp()
    end_ts = end.astimezone(timezone.utc).timestamp()

    results = []
    cursor = None
    while True:
        params = {"modified_after": str(start_ts - 1), "active": "true", "limit": "500"}
        if cursor:
            params["cursor"] = cursor
        request = urllib.request.Request(
            "https://api.pushbullet.com/v2/pushes?" + urllib.parse.urlencode(params),
            headers={"Access-Token": token, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                page = json.load(response)
        except urllib.error.HTTPError as exc:
            print(f"Pushbullet API error: HTTP {exc.code}", file=sys.stderr)
            return 1
        except urllib.error.URLError as exc:
            print(f"Could not reach Pushbullet API: {exc.reason}", file=sys.stderr)
            return 1

        for push in page.get("pushes", []):
            created = float(push.get("created", 0))
            url = push.get("url", "")
            host = urllib.parse.urlparse(url).netloc.lower().split(":")[0]
            if start_ts <= created < end_ts and host in {
                "x.com", "www.x.com", "twitter.com", "www.twitter.com"
            }:
                results.append((created, push.get("title", ""), url, push.get("body", "")))

        cursor = page.get("cursor")
        if not cursor:
            break

    results.sort(reverse=True)
    print(f"X links received on {yesterday.isoformat()} (Asia/Tokyo): {len(results)}")
    for created, title, url, body in results:
        local_time = datetime.fromtimestamp(created, tz).strftime("%H:%M")
        print(f"\n- {local_time} — {title or '(no title)'}")
        print(f"  {url}")
        if body:
            print(f"  {body}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
