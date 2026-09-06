#!/usr/bin/env python3
"""Session 12 batch V (2026-09-06): 1 verified add (W-2026-200) — 200 milestone.
PV Sindhu: DOB 1995-07-05 x5 (Wikimedia Commons/Wikidata record,
freepressjournal, sportskeeda, jagranjosh, skchildrenfoundation); women's
badminton career (Olympic silver 2016 + bronze 2020, world champion 2019).
Faith Kipyegon + Femke Bol dup-caught pre-script.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

NEW = [dict(
    id="W-2026-200", displayName="PV Sindhu (Pusarla Venkata Sindhu)",
    categories=["Athlete", "Badminton", "Creator"],
    legalAdultEvidence=ev(
        "Born July 5, 1995 in Hyderabad, India — age 31 in 2026 — per the Wikimedia Commons/Wikidata record (Date of birth 5 July 1995), Free Press Journal ('born July 5, 1995'), Sportskeeda player profile (Date of Birth July 5, 1995; age 31) and Jagran Josh (Date and Place of Birth 5 July 1995, Hyderabad).",
        "Sportskeeda — PV Sindhu player profile (Date of Birth July 5, 1995)", "https://www.sportskeeda.com/player/p-v-sindhu"),
    genderEvidence=ev(
        "Identified as a woman via women's singles badminton career — 'the first-ever Indian woman to win two Olympic medals' (silver Rio 2016, bronze Tokyo 2020 in women's singles) and 2019 BWF women's world champion (Free Press Journal/Sportskeeda).",
        "Free Press Journal — PV Sindhu birthday special ('first-ever Indian woman to win two Olympic medals')", "https://www.freepressjournal.in/sports/pv-sindhu-birthday-special-all-you-need-to-know-about-the-badminton-star"),
    sources=[
        src("Sportskeeda — PV Sindhu player profile (DOB July 5, 1995; women's singles)", "Website", "https://www.sportskeeda.com/player/p-v-sindhu", "other-trusted"),
        src("Wikimedia Commons — PV Sindhu authority record (Date of birth 5 July 1995; awards incl. Olympic silver/bronze)", "Website", "https://commons.wikimedia.org/wiki/P._V._Sindhu", "other-trusted"),
        src("Free Press Journal — PV Sindhu birthday special (born July 5, 1995; Olympic medals)", "Website", "https://www.freepressjournal.in/sports/pv-sindhu-birthday-special-all-you-need-to-know-about-the-badminton-star", "other-trusted"),
        src("Jagran Josh — PV Sindhu records (Date of birth 5 July 1995, Hyderabad)", "Website", "https://www.jagranjosh.com/general-knowledge/pv-sindhu-records-1566803790-1", "other-trusted")],
    verificationStatus="verified", lastReviewed=CHECKED, flags=[],
    notes=("Two-time Olympic medalist in women's badminton (Rio 2016 silver, Tokyo 2020 bronze — first Indian woman with two Olympic medals across two Games) and 2019 BWF world champion — objective athlete category; verified 31 years old. No social handle captured this pass — follower range UNKNOWN."),
    socialAccounts=[],
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
