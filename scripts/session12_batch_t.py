#!/usr/bin/env python3
"""Session 12 batch T (2026-09-06): 1 verified add (W-2026-197).
USC women's basketball: official usctrojans.com roster page — own bio prose
('was born July 15, 2005') + JSON-LD sameAs IG/X handles. Naomi Osaka
dup-caught as pre-existing via grep. birthdays.fyi 2006-day-year outlier
noted vs official+Wikipedia 2005.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

def acct(p, u, url, note):
    return {"platform": p, "username": u, "profileUrl": url,
            "followerCountDisplay": "FOLLOWER_COUNT_UNKNOWN", "followerCountNumeric": None,
            "countType": "unknown", "checkedAt": CHECKED,
            "followerSizeRange": "FOLLOWER_RANGE_UNKNOWN", "sourceNote": note}

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

NEW = [dict(
    id="W-2026-197", displayName="Judea \"JuJu\" Watkins",
    categories=["Athlete", "Basketball", "Creator"],
    legalAdultEvidence=ev(
        "Born July 15, 2005 in Los Angeles, California — age 21 in 2026 — per the OFFICIAL USC Athletics roster bio ('Judea \"JuJu\" Skies Watkins was born July 15, 2005 in Los Angeles'), Wikipedia (born July 15, 2005), bolavip ('Born in 2005, currently 20 years old in 2025') and celegraphy (Date of Birth July 15, 2005).",
        "USC Athletics — official JuJu Watkins roster bio (born July 15, 2005)",
        "https://usctrojans.com/sports/womens-basketball/roster/juju-watkins/18627"),
    genderEvidence=ev(
        "Identified as a woman via USC women's basketball roster membership — 'USC Women's Basketball' structured affiliation on the official roster page; women's national honors (FIBA U-16/U-17 World Cup golds with US women's youth teams per Wikipedia).",
        "USC Athletics — official roster (memberOf: USC Women's Basketball)",
        "https://usctrojans.com/sports/womens-basketball/roster/juju-watkins/18627"),
    sources=[
        src("USC Athletics — official JuJu Watkins roster bio (born July 15, 2005; sameAs IG/X jujubballin)", "Website", "https://usctrojans.com/sports/womens-basketball/roster/juju-watkins/18627", "official"),
        src("Wikipedia — JuJu Watkins (born July 15, 2005; USC Trojans)", "Website", "https://en.wikipedia.org/wiki/JuJu_Watkins", "other-trusted"),
        src("bolavip — JuJu Watkins profile ('Born in 2005, currently 20 years old in 2025')", "Website", "https://bolavip.com/en/college-basketball/juju-watkins-profile", "other-trusted"),
        src("Instagram — @jujubballin (USC roster structured sameAs)", "Instagram", "https://www.instagram.com/jujubballin", "verified-platform"),
        src("X — @jujubballin (USC roster structured sameAs)", "X", "https://twitter.com/jujubballin", "verified-platform")],
    verificationStatus="verified", lastReviewed=CHECKED, flags=[],
    notes=("USC women's basketball star guard and 2025 consensus National Player of the Year — objective athlete category; verified 21 years old via the official university roster bio. Note: birthdays.fyi lists 'July 15, 2006' — outlier vs the official USC roster ('born July 15, 2005'), Wikipedia and bolavip; official value recorded. Handles via official roster structured sameAs; counts not captured — UNKNOWN."),
    socialAccounts=[
        acct("Instagram", "@jujubballin", "https://www.instagram.com/jujubballin", "Handle via official USC roster structured sameAs (instagram.com/jujubballin); count not captured."),
        acct("X", "@jujubballin", "https://twitter.com/jujubballin", "Handle via official USC roster structured sameAs (twitter.com/jujubballin); count not captured.")],
    largestPublicFollowing={"platform": None, "username": None, "display": None,
                            "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                            "checkedAt": CHECKED},
    overallFollowerSizeRange="FOLLOWER_RANGE_UNKNOWN")]


def build():
    data = json.loads(CATALOG.read_text())
    entries = data["entries"]
    ids = {e["id"] for e in entries}
    names = {e["displayName"].lower() for e in entries}
    urls = {s["url"] for e in entries for s in e["sources"]}
    for r in NEW:
        assert r["id"] not in ids, r["id"]
        assert r["displayName"].lower() not in names, r["displayName"]
        assert not ({s["url"] for s in r["sources"]} & urls), r["displayName"]
    entries.extend(NEW)
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)})")

if __name__ == "__main__":
    build()
