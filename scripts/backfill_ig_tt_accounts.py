#!/usr/bin/env python3
"""Copy already-stored Instagram/TikTok source URLs into socialAccounts.

Does not invent handles or follower counts. Only used when a catalog row already
records an Instagram or TikTok source URL but has no matching socialAccounts row
(early Session 08-style entries). Follower fields stay FOLLOWER_COUNT_UNKNOWN.

Usage: python3 scripts/backfill_ig_tt_accounts.py [--dry-run]
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "catalog.json")
TODAY = date.today().isoformat()
UNKNOWN_COUNT = "FOLLOWER_COUNT_UNKNOWN"
UNKNOWN_RANGE = "FOLLOWER_RANGE_UNKNOWN"


def handle_from(platform: str, url: str) -> str | None:
    parsed = urlparse(url)
    path = (parsed.path or "").strip("/")
    if not path:
        return None
    first = path.split("/")[0]
    if platform == "TikTok":
        handle = first.lstrip("@")
        if handle and handle.lower() not in {"foryou", "tag", "music", "video", "discover"}:
            return "@" + handle
        return None
    if platform == "Instagram":
        if first.lower() in {"p", "reel", "reels", "stories", "tv", "explore", "accounts"}:
            return None
        if first:
            return "@" + first.lstrip("@")
    return None


def main() -> int:
    dry = "--dry-run" in sys.argv
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    changed = []
    for entry in catalog["entries"]:
        accounts = list(entry.get("socialAccounts") or [])
        existing_urls = {(a.get("platform"), (a.get("profileUrl") or "").rstrip("/").lower()) for a in accounts}
        existing_users = {
            (a.get("platform"), (a.get("username") or "").lstrip("@").lower()) for a in accounts
        }
        added = []
        for source in entry.get("sources") or []:
            platform = source.get("platform")
            url = source.get("url") or ""
            if platform not in {"Instagram", "TikTok"} or not url:
                continue
            key = (platform, url.rstrip("/").lower())
            if key in existing_urls:
                continue
            handle = handle_from(platform, url)
            if not handle:
                continue
            user_key = (platform, handle.lstrip("@").lower())
            if user_key in existing_users:
                continue
            added.append(
                {
                    "platform": platform,
                    "username": handle,
                    "profileUrl": url,
                    "followerCountDisplay": UNKNOWN_COUNT,
                    "followerCountNumeric": None,
                    "countType": "unknown",
                    "checkedAt": TODAY,
                    "followerSizeRange": UNKNOWN_RANGE,
                    "sourceNote": (
                        "Handle copied from an already-stored official/source URL on this catalog "
                        f"row. No follower count was publicly observed on {TODAY}, so it is "
                        f"recorded as {UNKNOWN_COUNT} rather than estimated."
                    ),
                }
            )
            existing_urls.add(key)
            existing_users.add(user_key)
        if added:
            entry["socialAccounts"] = accounts + added
            if not entry.get("overallFollowerSizeRange"):
                entry["overallFollowerSizeRange"] = UNKNOWN_RANGE
            changed.append((entry["id"], entry["displayName"], [a["username"] for a in added]))

    print(f"rows with new socialAccounts: {len(changed)}")
    for row_id, name, handles in changed:
        print(f"  {row_id} {name}: {', '.join(handles)}")

    if dry or not changed:
        return 0

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
