#!/usr/bin/env python3
"""
Session 22 — follower count patches for known public observations.

Uses publicly observable follower counts from Instagram profile snippets
and reputable analytics pages (not estimated). Each patch includes sourceNote.

Usage: python3 scripts/session22_followers.py --apply
"""
import json, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"
TODAY = date(2026, 9, 6).isoformat()

PATCHES = [
    # Soniya Singh Khatri — @fitgirl_08 — 3M followers (Instagram bio + whatainfo + excelebiz)
    {
        "id": "W-2026-008",
        "displayName": "Soniya Singh Khatri",
        "platform": "Instagram",
        "username": "@fitgirl_08",
        "display": "3M",
        "numeric": 3000000,
        "sizeRange": "1M–4.9M",
        "countType": "rounded",
        "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06 via web_search: '3M followers, 50 following, 1,713 posts – @fitgirl_08'. Corroborated by whatainfo.in biography (3M followers as of 2026, born 12 Aug 1995) and excelebiz.in (3M+ @fitgirl_08, 2.9M Feb 2026). Count recorded as rounded 3M (platform displays rounded for large accounts).",
        "profileUrl": "https://www.instagram.com/fitgirl_08/",
    },
    # Elisabeth Rioux — @elisabethrioux — 1.6M followers (SPEAKRJ analytics 2022-08-10)
    {
        "id": "W-2026-009",
        "displayName": "Elisabeth Rioux",
        "platform": "Instagram",
        "username": "@elisabethrioux",
        "display": "1.6M",
        "numeric": 1617362,
        "sizeRange": "1M–4.9M",
        "countType": "exact",
        "sourceNote": "SPEAKRJ public analytics page for @elisabethrioux retrieved 2026-09-06: '1.6M followers count' with historical table 2022-08-10 showing 1,617,362 followers. Instagram profile blocks automated retrieval, so public analytics snapshot is recorded verbatim. Alternative handle @elisabeth.rioux shows 670.3k in older Pinterest snippet (2017), but primary handle @elisabethrioux is 1.6M.",
        "profileUrl": "https://www.instagram.com/elisabethrioux/",
    },
    # Lexi Sun — @lexiisun — 60K followers (FamousBirthdays) + 85K Omaha Magazine 2022
    {
        "id": "W-2026-021",
        "displayName": "Lexi Sun",
        "platform": "Instagram",
        "username": "@lexiisun",
        "display": "60K",
        "numeric": 60000,
        "sizeRange": "50K–99.9K",
        "countType": "rounded",
        "sourceNote": "FamousBirthdays public page for Lexi Sun retrieved 2026-09-06: 'has accrued 60,000 followers' for @lexiisun Instagram account. Omaha Magazine 2022-04-28 article states 'As of presstime, Sun had 85,000 followers on Instagram'. Using 60K as conservative publicly observed rounded figure (FamousBirthdays).",
        "profileUrl": "https://www.instagram.com/lexiisun/",
    },
    # Anna Danesi — @annadanesi — 180K followers (Instagram snippet)
    {
        "id": "W-2026-577",  # placeholder, need to find actual ID for Anna Danesi
        "displayName": "Anna Danesi",
        "platform": "Instagram",
        "username": "@annadanesi",
        "display": "180K",
        "numeric": 180000,
        "sizeRange": "100K–249.9K",
        "countType": "rounded",
        "sourceNote": "Instagram public snippet retrieved 2026-09-06 via web_search: '180K followers, 1,374 following, 240 posts – @annadanesi'. Italian women's volleyball captain, Olympic gold Paris 2024.",
        "profileUrl": "https://www.instagram.com/annadanesi/",
    },
    # Myriam Sylla — @miriamsylla — 402K followers
    {
        "id": "W-2026-578",
        "displayName": "Myriam Sylla",
        "platform": "Instagram",
        "username": "@miriamsylla",
        "display": "402K",
        "numeric": 402000,
        "sizeRange": "250K–499.9K",
        "countType": "rounded",
        "sourceNote": "Instagram public snippet retrieved 2026-09-06: '402K seguidores, 1,149 siguiendo, 595 publicaciones - @miriamsylla'. Italian volleyball player, Olympic champion Paris 2024.",
        "profileUrl": "https://www.instagram.com/miriamsylla/",
    },
    # Valentina Gottardi — @valentinagottardi_ — 133K followers
    {
        "id": "W-2026-579",
        "displayName": "Valentina Gottardi",
        "platform": "Instagram",
        "username": "@valentinagottardi_",
        "display": "133K",
        "numeric": 133000,
        "sizeRange": "100K–249.9K",
        "countType": "rounded",
        "sourceNote": "Instagram public snippet retrieved 2026-09-06: '133K followers, 874 following, 293 posts – @valentinagottardi_'. Italian beach volleyball Olympian.",
        "profileUrl": "https://www.instagram.com/valentinagottardi_/",
    },
]

def find_entry_id(catalog, display_name):
    for e in catalog["entries"]:
        if e["displayName"].lower() == display_name.lower():
            return e["id"]
    return None

def main():
    apply_changes = "--apply" in sys.argv
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in catalog["entries"]}
    # Resolve placeholder IDs for Danesi, Sylla, Gottardi
    for patch in PATCHES:
        if patch["id"].startswith("W-2026-57"):
            # find real id by name
            real_id = find_entry_id(catalog, patch["displayName"])
            if real_id:
                patch["id"] = real_id
            else:
                print(f"WARNING: could not find entry for {patch['displayName']}, skipping")
                continue
        entry = by_id.get(patch["id"])
        if not entry:
            print(f"SKIP: id {patch['id']} not found for {patch['displayName']}")
            continue
        if entry["displayName"] != patch["displayName"]:
            print(f"ID/NAME mismatch: {patch['id']} catalog has {entry['displayName']} vs patch {patch['displayName']}")
            # try to find by name anyway
            real_id = find_entry_id(catalog, patch["displayName"])
            if real_id and real_id != patch["id"]:
                print(f"  -> using real id {real_id}")
                patch["id"] = real_id
                entry = by_id.get(real_id)
        # find account
        acc = None
        for a in entry.get("socialAccounts",[]):
            if a["platform"]==patch["platform"] and a["username"].lower()==patch["username"].lower():
                acc=a
                break
            # also try without @
            if a["platform"]==patch["platform"] and a["username"].lstrip("@").lower()==patch["username"].lstrip("@").lower():
                acc=a
                break
        if not acc:
            print(f"SKIP: no {patch['platform']} {patch['username']} on {patch['id']} {entry['displayName']}")
            print(f"  available: {[ (a['platform'], a['username']) for a in entry.get('socialAccounts',[]) ]}")
            continue
        print(f"PATCH {patch['id']} {patch['displayName']} {patch['platform']} {patch['username']} -> {patch['display']} ({patch['numeric']})")
        if not apply_changes:
            continue
        acc["followerCountDisplay"]=patch["display"]
        acc["followerCountNumeric"]=patch["numeric"]
        acc["countType"]=patch["countType"]
        acc["checkedAt"]=TODAY
        acc["followerSizeRange"]=patch["sizeRange"]
        acc["sourceNote"]=patch["sourceNote"]
        acc["profileUrl"]=patch["profileUrl"]
        # update largestPublicFollowing
        best = None
        best_num = -1
        for a in entry.get("socialAccounts",[]):
            num = a.get("followerCountNumeric")
            if isinstance(num, (int,float)) and num>best_num:
                best_num=num
                best=a
        if best:
            entry["largestPublicFollowing"]={
                "platform": best["platform"],
                "username": best.get("username"),
                "display": best["followerCountDisplay"],
                "numeric": best["followerCountNumeric"],
                "sizeRange": best["followerSizeRange"],
                "checkedAt": best["checkedAt"],
            }
            entry["overallFollowerSizeRange"]=best["followerSizeRange"]

    if not apply_changes:
        print("\n[dry run] re-run with --apply")
        return

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {CATALOG} with {len(catalog['entries'])} entries")

if __name__=="__main__":
    main()
