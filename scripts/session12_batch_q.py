#!/usr/bin/env python3
"""Session 12 batch Q (2026-09-06): 2 verified adds (W-2026-191..192).
PWHL + WSL wave: thepwhl.com official athlete bio (Fillier, exact birthdate),
worldsurfleague.com official athlete page + redbull.com JSON-LD
(gender female + birthDate, Picklum). Fillier has one fan-blog DOB outlier
(2000-08-31) vs official/Wikipedia/eliteprospects/hockeydb June 9 — resolved
to official, noted. Dup-guard pre-checked clean.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

def ent(i, n, cats, a, g, s, notes):
    return {"id": i, "displayName": n, "categories": cats,
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": [],
            "notes": notes, "socialAccounts": [],
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-191", "Sarah Fillier", ["Athlete", "Ice Hockey", "Creator"],
    ev("Born June 9, 2000 in Georgetown, Ontario, Canada — age 26 in 2026 — per the OFFICIAL PWHL athlete page (Birthdate: 2000-06-09), Wikipedia (born June 9, 2000), Elite Prospects structured record (birthDate 2000-06-09) and hockeydb (Born Jun 9 2000).",
       "PWHL — official Sarah Fillier athlete page (Birthdate: 2000-06-09)", "https://www.thepwhl.com/en/olympics/athlete/sarah-fillier"),
    ev("Identified as a woman via Canada women's national ice hockey team and PWHL career — 2024 PWHL first-overall draft pick (New York Sirens), Olympic gold medalist (Beijing 2022) with Canada women's hockey per Wikipedia and the official PWHL page.",
       "PWHL — official Sarah Fillier athlete page (Team Canada forward)", "https://www.thepwhl.com/en/olympics/athlete/sarah-fillier"),
    [src("PWHL — official Sarah Fillier athlete page (Birthdate 2000-06-09; New York Sirens)", "Website", "https://www.thepwhl.com/en/olympics/athlete/sarah-fillier", "official"),
     src("Elite Prospects — Sarah Fillier (structured birthDate 2000-06-09)", "Website", "https://www.eliteprospects.com/player/431721/sarah-fillier", "other-trusted"),
     src("hockeydb — Sarah Fillier (Born Jun 9 2000)", "Website", "https://www.hockeydb.com/ihdb/stats/pdisplay.php?pid=276083", "other-trusted"),
     src("Wikipedia — Sarah Fillier (born June 9, 2000)", "Website", "https://en.wikipedia.org/wiki/Sarah_Fillier", "other-trusted")],
    "Olympic gold medalist (Beijing 2022) and 2024 PWHL first-overall draft pick — objective athlete category; verified 26 years old. Note: a fan blog roster page (pwhl.blog) lists DOB 2000-08-31 — outlier vs official PWHL + Wikipedia + Elite Prospects + hockeydb (all 2000-06-09); official value recorded. No social handle captured this pass — follower range UNKNOWN."))

NEW.append(ent("W-2026-192", "Molly Picklum", ["Athlete", "Surfing", "Creator"],
    ev("Born November 26, 2002 in Gosford, New South Wales, Australia — age 23 in 2026 — per Red Bull athlete page structured record (birthDate 2002-11-26), the OFFICIAL World Surf League athlete bio (Age 23, Nov 26, 2002) and Wikipedia (born 26 November 2002).",
       "World Surf League — official Molly Picklum athlete bio (Age 23, Nov 26, 2002)", "https://www.worldsurfleague.com/athletes/10979/molly-picklum"),
    ev("Identified as a woman via Red Bull structured record ('gender: female') and WSL Women's Championship Tour career — 2025 WSL World Champion ('first Australian woman to claim the world title since 2022') per Red Bull and Wikipedia.",
       "Red Bull — Molly Picklum athlete page (JSON-LD gender female; 2025 world title)", "https://www.redbull.com/au-en/athlete/molly-picklum"),
    [src("World Surf League — official Molly Picklum athlete bio (Age 23, Nov 26, 2002)", "Website", "https://www.worldsurfleague.com/athletes/10979/molly-picklum", "official"),
     src("Red Bull — Molly Picklum athlete page (birthDate 2002-11-26; gender female structured)", "Website", "https://www.redbull.com/au-en/athlete/molly-picklum", "official"),
     src("Wikipedia — Molly Picklum (born 26 November 2002; 2025 WSL World Champion)", "Website", "https://en.wikipedia.org/wiki/Molly_Picklum", "other-trusted")],
    "2025 WSL Women's World Champion — the first Australian woman to win the world title since Stephanie Gilmore in 2022 — objective athlete category; verified 23 years old. No social handle captured this pass — follower range UNKNOWN."))


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
