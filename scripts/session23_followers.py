#!/usr/bin/env python3
"""Session 23 — more follower patches from public snippets."""
import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"
TODAY = date(2026, 9, 6).isoformat()

PATCHES = [
    {
        "id": "W-2026-576",
        "displayName": "Paola Egonu",
        "platform": "Instagram",
        "username": "@paolaegonu",
        "display": "632K",
        "numeric": 632000,
        "sizeRange": "500K–999.9K",
        "countType": "rounded",
        "sourceNote": "Instagram public snippet retrieved 2026-09-06 via web_search: '632K seguidores, 2,896 seguidos, 866 publicaciones - Paola Egonu (@paolaegonu)'. Also SPEAKRJ analytics 2022-06-08 shows 259,821 followers, FamousBirthdays states 550,000 followers. Using 632K as most recent rounded public observation.",
        "profileUrl": "https://www.instagram.com/paolaegonu/",
    },
    {
        "id": "W-2026-227",
        "displayName": "Tijana Bošković",
        "platform": "Instagram",
        "username": "@coti_18",
        "display": "353K",
        "numeric": 353000,
        "sizeRange": "250K–499.9K",
        "countType": "rounded",
        "sourceNote": "Instagram public snippet retrieved 2026-09-06: '353K seguidores, 665 seguidos, 786 publicaciones - Tijana Bošković (@coti_18)'. Serbian volleyball player.",
        "profileUrl": "https://www.instagram.com/coti_18/",
    },
    {
        "id": "W-2026-217",
        "displayName": "Isabelle Haak",
        "platform": "Instagram",
        "username": "@isabellehaakofficial",
        "display": "331K",
        "numeric": 331000,
        "sizeRange": "250K–499.9K",
        "countType": "rounded",
        "sourceNote": "Instagram public snippet retrieved 2026-09-06: '331K followers, 988 following, 281 posts – Isabelle Bella Haak (@isabellehaakofficial)'. Swedish volleyball player, Imoco Volley Conegliano.",
        "profileUrl": "https://www.instagram.com/isabellehaakofficial/",
    },
    # Add a few more from earlier search: Ebrar Karakurt, Zehra Gunes, etc. but check if in catalog
]

def main():
    apply = "--apply" in __import__("sys").argv
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in catalog["entries"]}
    for patch in PATCHES:
        entry = by_id.get(patch["id"])
        if not entry:
            print(f"SKIP id {patch['id']} not found")
            continue
        acc = None
        for a in entry.get("socialAccounts",[]):
            if a["platform"]==patch["platform"] and a["username"].lstrip("@").lower()==patch["username"].lstrip("@").lower():
                acc=a
                break
        if not acc:
            print(f"SKIP no {patch['platform']} {patch['username']} on {patch['id']} {entry['displayName']}")
            continue
        print(f"PATCH {patch['id']} {patch['displayName']} -> {patch['display']}")
        if not apply:
            continue
        acc["followerCountDisplay"]=patch["display"]
        acc["followerCountNumeric"]=patch["numeric"]
        acc["countType"]=patch["countType"]
        acc["checkedAt"]=TODAY
        acc["followerSizeRange"]=patch["sizeRange"]
        acc["sourceNote"]=patch["sourceNote"]
        acc["profileUrl"]=patch["profileUrl"]
        # update largest
        best=None
        best_num=-1
        for a in entry.get("socialAccounts",[]):
            num=a.get("followerCountNumeric")
            if isinstance(num,(int,float)) and num>best_num:
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
    if not apply:
        print("[dry run] --apply to write")
        return
    with open(CATALOG,"w",encoding="utf-8") as fh:
        json.dump(catalog,fh,indent=2,ensure_ascii=False)
        fh.write("\n")
    print("wrote catalog")

if __name__=="__main__":
    main()
