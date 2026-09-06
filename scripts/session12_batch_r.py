#!/usr/bin/env python3
"""Session 12 batch R (2026-09-06): 2 verified adds (W-2026-193..194).
Motorsport + skateboarding wave: Wikipedia/autosport/motorsport.com (Pulling),
Britannica/Wikipedia/olympics.com (Leal, explicit 'age 18' + published DOB
2008-01-04 -> adult 18+ as of 2026 per Britannica). Dup-guard pre-checked.
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

NEW.append(ent("W-2026-193", "Abbi Pulling", ["Athlete", "Motorsport", "Creator"],
    ev("Born March 21, 2003 in Gosberton, Lincolnshire, UK — age 23 in 2026 — per Wikipedia (born 21 March 2003), motorsport.com official driver profile (Date of birth 2003-03-21), Autosport ('born in Lincolnshire on 21 March 2003') and SCMP ('21-year-old', Dec 2024).",
       "Motorsport.com — Abbi Pulling driver profile (Date of birth 2003-03-21)", "https://www.motorsport.com/driver/abbi-pulling/947570/"),
    ev("Identified as a woman via her career in the all-woman F1 Academy series (2024 F1 Academy drivers' champion), W Series and Formula E women's test sessions — Autosport/SCMP/Wikipedia.",
       "Autosport — 'Who is Abbi Pulling? An insight into the F1 Academy star'", "https://www.autosport.com/F1-Academy/news/who-is-abbi-pulling-an-insight-into-the-f1-academy-star/10610763/"),
    [src("Motorsport.com — Abbi Pulling driver profile (DOB 2003-03-21)", "Website", "https://www.motorsport.com/driver/abbi-pulling/947570/", "other-trusted"),
     src("Wikipedia — Abbi Pulling (born 21 March 2003; 2024 F1 Academy champion)", "Website", "https://en.wikipedia.org/wiki/Abbi_Pulling", "other-trusted"),
     src("Autosport — Abbi Pulling feature (born 21 March 2003)", "Website", "https://www.autosport.com/F1-Academy/news/who-is-abbi-pulling-an-insight-into-the-f1-academy-star/10610763/", "other-trusted")],
    "2024 F1 Academy drivers' champion (all-woman series) and Nissan Formula E team rookies/simulator driver — objective athlete category; verified 23 years old. No social handle captured this pass — follower range UNKNOWN."))

NEW.append(ent("W-2026-194", "Rayssa Leal", ["Athlete", "Skateboarding", "Creator"],
    ev("Born January 4, 2008 in Imperatriz, Maranhão, Brazil — EXPLICITLY 'age 18' per Britannica (published DOB + age) — adult 18+ as of 2026; corroborated by Wikipedia (born 4 January 2008), olympics.com official profile (Year of Birth 2008) and surfertoday.",
       "Britannica — Rayssa Leal (born January 4, 2008; 'age 18')", "https://www.britannica.com/biography/Rayssa-Leal"),
    ev("Identified as a woman via women's street skateboarding career — Olympic silver (Tokyo 2020, women's street) and bronze (Paris 2024), youngest-ever Brazilian double Olympic medalist (Wikipedia/Britannica/olympics.com).",
       "Wikipedia — Rayssa Leal (women's street skateboarding medals)", "https://en.wikipedia.org/wiki/Rayssa_Leal"),
    [src("Britannica — Rayssa Leal (DOB Jan 4 2008; explicit 'age 18'; bio)", "Website", "https://www.britannica.com/biography/Rayssa-Leal", "age-evidence"),
     src("Olympics.com — Rayssa Leal official athlete profile (Year of Birth 2008)", "Website", "https://www.olympics.com/en/athletes/rayssa-leal", "official"),
     src("Wikipedia — Rayssa Leal (born 4 January 2008; medal record)", "Website", "https://en.wikipedia.org/wiki/Rayssa_Leal", "other-trusted")],
    "Two-time Olympic medalist in women's street skateboarding (Tokyo 2020 silver, Paris 2024 bronze) — objective athlete category; verified 18 years old via published DOB (2008-01-04) plus Britannica's explicit current age. No social handle captured this pass — follower range UNKNOWN; a third-party reports a post-Tokyo follower surge but no verified current count is recorded."))


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
