#!/usr/bin/env python3
"""Session 12 batch S (2026-09-06): 2 verified adds (W-2026-195..196).
Rugby + alpine skiing wave: biographykind JSON-LD sameAs IG (Maher handles),
Wikipedia/EBSCO (Shiffrin). Dup-guard pre-checked clean.
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

def ent(i, n, cats, a, g, s, notes, accts):
    return {"id": i, "displayName": n, "categories": cats,
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": [],
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-195", "Ilona Maher", ["Athlete", "Rugby", "Creator"],
    ev("Born August 12, 1996 in Burlington, Vermont — age 30 in 2026 — per Wikipedia (born August 12, 1996), The Sun ('She was born on August 12, 1996'), Grokipedia and londonlifemagazine (DOB 1996-08-12).",
       "Wikipedia — Ilona Maher (born August 12, 1996)", "https://en.wikipedia.org/wiki/Ilona_Maher"),
    ev("Identified as a woman via US women's rugby sevens career — team captain and bronze medalist at Paris 2024 ('first Olympic medal in the sport' for the US women's sevens), 2025 Women's Rugby World Cup (Wikipedia/grokipedia).",
       "Wikipedia — Ilona Maher (women's rugby sevens bronze 2024)", "https://en.wikipedia.org/wiki/Ilona_Maher"),
    [src("Wikipedia — Ilona Maher (DOB 1996-08-12; Paris 2024 bronze)", "Website", "https://en.wikipedia.org/wiki/Ilona_Maher", "other-trusted"),
     src("The Sun — Ilona Maher profile (born August 12, 1996; US women's rugby)", "Website", "https://www.the-sun.com/sport/12112574/ilona-maher-rugby-usa-olympics-tiktok-instagram-who/", "other-trusted"),
     src("BiographyKind — Ilona Maher (sameAs IG ilonamaher; X ilona_maher)", "Website", "https://en.biographykind.com/ilona-maher/", "other-trusted"),
     src("Instagram — @ilonamaher (biographykind structured sameAs)", "Instagram", "https://www.instagram.com/ilonamaher/", "verified-platform"),
     src("X — @ilona_maher (biographykind social table)", "X", "https://x.com/ilona_maher", "verified-platform")],
    "US women's rugby sevens captain and Paris 2024 bronze medalist; 2025 ESPY Best Breakthrough Athlete — objective athlete category and prolific women's-sports creator. Handles from biographykind structured sameAs/social table; counts not captured — UNKNOWN.",
    [acct("Instagram", "@ilonamaher", "https://www.instagram.com/ilonamaher/", "Handle via biographykind structured sameAs (instagram.com/ilonamaher); count not captured."),
     acct("X", "@ilona_maher", "https://x.com/ilona_maher", "Handle via biographykind social table; count not captured.")]))

NEW.append(ent("W-2026-196", "Mikaela Shiffrin", ["Athlete", "Skiing", "Creator"],
    ev("Born March 13, 1995 in Vail, Colorado — age 31 in 2026 — per Wikipedia (born March 13, 1995), EBSCO research profile (born on March 13, 1995), POWDER (Date of Birth: March 13th, 1995) and Kiddle replication (age 31).",
       "EBSCO — Mikaela Shiffrin research profile (born March 13, 1995)", "https://www.ebsco.com/research-starters/biography/mikaela-shiffrin"),
    ev("Identified as a woman via women's alpine ski racing career — most World Cup wins of any alpine skier in history (100+), two-time Olympic gold medalist in women's events (Wikipedia/EBSCO).",
       "Wikipedia — Mikaela Shiffrin (110 World Cup wins as of Mar 2026)", "https://en.wikipedia.org/wiki/Mikaela_Shiffrin"),
    [src("EBSCO — Mikaela Shiffrin research profile (born March 13, 1995, in Vail)", "Website", "https://www.ebsco.com/research-starters/biography/mikaela-shiffrin", "other-trusted"),
     src("Wikipedia — Mikaela Shiffrin (DOB 1995-03-13; 100 World Cup wins Feb 2025)", "Website", "https://en.wikipedia.org/wiki/Mikaela_Shiffrin", "other-trusted"),
     src("POWDER — Mikaela Shiffrin stats (Date of Birth March 13th, 1995)", "Website", "https://www.powder.com/tag/mikaela-shiffrin", "other-trusted")],
    "The winningest alpine skier in World Cup history (100+ victories; 110 as of March 2026) and two-time Olympic gold medalist — objective athlete category; verified 31 years old. No social handle captured this pass — follower range UNKNOWN.", []))


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
