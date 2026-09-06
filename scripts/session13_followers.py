#!/usr/bin/env python3
"""
Session 13 — publicly observed follower counts for the volleyball batch.

Instagram/TikTok/X block automated retrieval of profile pages from this environment, so the
only follower figures recorded here are the ones actually published by a public analytics
page (HypeAuditor) on 2026-09-06, each with its own snapshot date. Everything else in the
batch stays FOLLOWER_COUNT_UNKNOWN / FOLLOWER_RANGE_UNKNOWN — never estimated.

Each patch is asserted by entry id AND displayName AND username before it is applied.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "catalog.json")
TODAY = "2026-09-06"

PATCHES = [
    {
        "id": "W-2026-464",
        "displayName": "Arina Fedorovtseva",
        "platform": "Instagram",
        "username": "@a.fed.10",
        "display": "346.3K",
        "numeric": 346337,
        "sizeRange": "250K\u2013499.9K",
        "snapshot": "30 Aug 2026",
        "note": ("HypeAuditor public analytics page for @a.fed.10 (retrieved 2026-09-06): current follower "
                 "count 346,337, displayed as 346.3K; its historical table dates that figure 30 Aug'26 "
                 "(+1,959 on the day). Instagram's own profile page blocks automated retrieval from this "
                 "environment, so this publicly displayed analytics figure is recorded verbatim \u2014 not "
                 "estimated and not summed with any other platform."),
    },
    {
        "id": "W-2026-498",
        "displayName": "Mhicaela Belen",
        "platform": "Instagram",
        "username": "@mhicaelabelen",
        "display": "431.9K",
        "numeric": 431914,
        "sizeRange": "250K\u2013499.9K",
        "snapshot": "29 Aug 2026",
        "note": ("HypeAuditor public analytics page for @mhicaelabelen (retrieved 2026-09-06): current "
                 "follower count 431,914, displayed as 431.9K; historical table dated 29 Aug'26. Account "
                 "country rank listed as Philippines. Instagram's own profile page blocks automated "
                 "retrieval here, so the publicly displayed analytics figure is recorded verbatim \u2014 not "
                 "estimated. HypeAuditor's own AI content tags for this account (Travel/Swimwear) are NOT "
                 "used as categories: this directory classifies her objectively as a volleyball athlete "
                 "(Philippine women's volleyball, per the cited records)."),
    },
    {
        "id": "W-2026-333",
        "displayName": "Elena Scott",
        "platform": "Instagram",
        "username": "@elenaascott",
        "display": "93.6K",
        "numeric": 93568,
        "sizeRange": "50K\u201399.9K",
        "snapshot": "03 Sep 2026",
        "note": ("HypeAuditor public analytics page for @elenaascott (retrieved 2026-09-06): current "
                 "follower count 93,568, displayed as 93.6K; historical table dated 03 Sep'26 (94,082 on "
                 "08 Aug'26, i.e. -0.58% over 30 days). Instagram's own profile page blocks automated "
                 "retrieval here, so the publicly displayed analytics figure is recorded verbatim \u2014 not "
                 "estimated."),
    },
]


def main():
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)
    by_id = {e["id"]: e for e in catalog["entries"]}

    for patch in PATCHES:
        entry = by_id.get(patch["id"])
        assert entry is not None, f"missing entry {patch['id']}"
        assert entry["displayName"] == patch["displayName"], (
            f"id/name mismatch for {patch['id']}: {entry['displayName']} != {patch['displayName']}")
        account = next((a for a in entry.get("socialAccounts", [])
                        if a["platform"] == patch["platform"] and a.get("username") == patch["username"]), None)
        assert account is not None, f"no {patch['platform']} {patch['username']} on {patch['id']}"

        account["followerCountDisplay"] = patch["display"]
        account["followerCountNumeric"] = patch["numeric"]
        account["countType"] = "exact"
        account["checkedAt"] = TODAY
        account["followerSizeRange"] = patch["sizeRange"]
        account["sourceNote"] = patch["note"]

        # largest single-platform following (never a cross-platform sum)
        best = max(entry["socialAccounts"],
                   key=lambda a: a.get("followerCountNumeric") or -1)
        if best.get("followerCountNumeric"):
            entry["largestPublicFollowing"] = {
                "platform": best["platform"],
                "username": best.get("username"),
                "display": best["followerCountDisplay"],
                "numeric": best["followerCountNumeric"],
                "sizeRange": best["followerSizeRange"],
                "checkedAt": best["checkedAt"],
            }
            entry["overallFollowerSizeRange"] = best["followerSizeRange"]

        entry["notes"] = entry["notes"].replace(
            f"Follower counts: none publicly observed for the listed account(s) \u2014 recorded as "
            f"FOLLOWER_COUNT_UNKNOWN / FOLLOWER_RANGE_UNKNOWN (never estimated, never summed across platforms).",
            f"Follower counts: {patch['platform']} {patch['username']} observed publicly at "
            f"{patch['display']} ({patch['numeric']:,}; {patch['sizeRange']}, snapshot {patch['snapshot']}) "
            f"via a public analytics page \u2014 see socialAccounts sourceNote. Any other listed account keeps "
            f"FOLLOWER_COUNT_UNKNOWN (never estimated, never summed across platforms).")
        print(f"patched {patch['id']} {patch['displayName']} {patch['platform']} "
              f"{patch['username']} -> {patch['display']} ({patch['numeric']:,}) {patch['sizeRange']}")

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("catalog written")


if __name__ == "__main__":
    main()
