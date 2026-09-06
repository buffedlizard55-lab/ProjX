#!/usr/bin/env python3
"""Session 12 batch P (2026-09-06): 2 verified adds (W-2026-189..190).
Women's football wave: players.fcbarcelona.com OFFICIAL club bios (exact DOB +
stats) for both, plus Britannica (Bonmatí), fbref JSON-LD + ESPN (Graham
Hansen). Dup-guard pre-checked (clean). Handles not captured — UNKNOWN counts.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

def ent(i, n, a, g, s, notes):
    return {"id": i, "displayName": n, "categories": ["Athlete", "Soccer", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": [],
            "notes": notes, "socialAccounts": [],
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-189", "Aitana Bonmatí",
    ev("Born January 18, 1998 in Vilanova i la Geltrú, Spain — age 28 in 2026 — per the OFFICIAL FC Barcelona player profile (Date of birth: 18/01/1998), Britannica (Born: January 18, 1998) and Wikipedia (born 18 January 1998).",
       "FC Barcelona — official Aitana Bonmatí player profile (Date of birth 18/01/1998)", "https://players.fcbarcelona.com/en/player/2517-aitana-aitana-bonmati-conca"),
    ev("Identified as a woman via FC Barcelona Femení and Spain women's national team career — three consecutive Ballon d'Or Féminin awards (2023/2024/2025, first in women's football history), 2023 FIFA Women's World Cup champion and 4x UEFA Women's Champions League winner per the official club profile and Britannica.",
       "Britannica — Aitana Bonmatí (3x Ballon d'Or Féminin)", "https://www.britannica.com/biography/Aitana-Bonmati"),
    [src("FC Barcelona — official Aitana Bonmatí player profile (DOB 18/01/1998; titles incl. 4 UWCL)", "Website", "https://players.fcbarcelona.com/en/player/2517-aitana-aitana-bonmati-conca", "official"),
     src("Britannica — Aitana Bonmatí (born January 18, 1998; 3x Ballon d'Or Féminin 2023-25)", "Website", "https://www.britannica.com/biography/Aitana-Bonmati", "other-trusted"),
     src("kiddle/Wikipedia replication — Aitana Bonmatí (DOB 18 January 1998)", "Website", "https://kids.kiddle.co/Aitana_Bonmat%C3%AD", "other-trusted")],
    "Three-time consecutive Ballon d'Or Féminin winner (2023–2025) and FIFA Women's World Cup champion — objective athlete category; verified 28 years old. No social handle captured this pass — follower range UNKNOWN."))

NEW.append(ent("W-2026-190", "Caroline Graham Hansen",
    ev("Born February 18, 1995 in Oslo, Norway — age 31 in 2026 — per the OFFICIAL FC Barcelona player profile (Date of birth: 18/02/1995), fbref.com structured record (birthDate 1995-02-18) and ESPN player bio (Birthdate 2/18/1995).",
       "FC Barcelona — official Caroline Graham Hansen player profile (Date of birth 18/02/1995)", "https://players.fcbarcelona.com/en/player/2799-caroline-graham-caroline-graham-hansen"),
    ev("Identified as a woman via FC Barcelona Femení and Norway women's national team career — 4x UEFA Women's Champions League winner and 7x Spanish league champion with Barcelona per the official club profile; regarded one of the best wingers in women's football.",
       "FC Barcelona — official Caroline Graham Hansen profile (Femení honours list)", "https://players.fcbarcelona.com/en/player/2799-caroline-graham-caroline-graham-hansen"),
    [src("FC Barcelona — official Caroline Graham Hansen player profile (DOB 18/02/1995; 7 Liga, 4 UWCL)", "Website", "https://players.fcbarcelona.com/en/player/2799-caroline-graham-caroline-graham-hansen", "official"),
     src("fbref — Caroline Graham Hansen (birthDate 1995-02-18 structured)", "Website", "https://fbref.com/en/players/e891b7ae/Caroline-Graham-Hansen", "other-trusted"),
     src("ESPN — Caroline Graham Hansen player bio (Birthdate 2/18/1995)", "Website", "https://www.espn.com/soccer/player/matches/_/id/253699/caroline-graham-hansen", "other-trusted")],
    "Seven-time Spanish league champion and 4x UEFA Women's Champions League winner with Barcelona — objective athlete category; verified 31 years old. No social handle captured this pass — follower range UNKNOWN."))


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
