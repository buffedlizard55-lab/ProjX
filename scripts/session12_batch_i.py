#!/usr/bin/env python3
"""Session 12 batch I (2026-09-06): 4 verified adds (W-2026-165..168).
LPGA women's golf wave: lydiako.co.nz official site, aigwomensopen.com player
JSON-LD birthDate, surprisesports IG handle. Dup-guard pre-checked.
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

def ent(i, n, a, g, s, flags, notes, accts):
    return {"id": i, "displayName": n, "categories": ["Athlete", "Golf", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-165", "Lexi Thompson",
    ev("Born February 10, 1995 in Coral Springs, Florida — age 31 in 2026 — per Wikipedia (born February 10, 1995) with Golf Digest corroboration ('the 31-year-old LPGA Tour star', August 2026).",
       "Wikipedia — Lexi Thompson (born February 10, 1995)", "https://en.wikipedia.org/wiki/Lexi_Thompson"),
    ev("Identified as a woman via LPGA women's golf career — 11 LPGA wins, 2014 Kraft Nabisco major, seven Solheim Cups for the US women's team (Wikipedia).",
       "Wikipedia — Lexi Thompson (LPGA women's career)", "https://en.wikipedia.org/wiki/Lexi_Thompson"),
    [src("Wikipedia — Lexi Thompson (DOB 1995-02-10; LPGA career)", "Website", "https://en.wikipedia.org/wiki/Lexi_Thompson", "age-evidence"),
     src("Golf Digest — Lexi Thompson pregnancy announcement ('the 31-year-old LPGA Tour star', Aug 2026)", "Website", "https://www.golfdigest.com/story/lexi-thompson-announces-pregnancy-lpga-star", "other-trusted")],
    [], "2014 major champion and seven-time US Solheim Cup player — objective athlete category. Announcement coverage corroborates age. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-166", "Lydia Ko",
    ev("Born April 24, 1997 in Seoul, South Korea — age 29 in 2026 — per her official website (Birthdate: April 24, 1997), Wikipedia (born 24 April 1997) and Kiddle replication.",
       "lydiako.co.nz — official personal website (Birthdate: April 24, 1997)", "https://www.lydiako.co.nz/profile/"),
    ev("Identified as a woman via LPGA women's golf career — LPGA Hall of Fame member, Paris 2024 Olympic women's golf champion, 'world's number one female golfer' (official site/Wikipedia).",
       "lydiako.co.nz — official website (women's golf titles record)", "https://www.lydiako.co.nz/"),
    [src("lydiako.co.nz — official profile (Birthdate April 24, 1997)", "Website", "https://www.lydiako.co.nz/profile/", "official"),
     src("lydiako.co.nz — official bio page ('READY TO TAKE ON THE WORLD'; birthdate)", "Website", "https://www.lydiako.co.nz/", "official"),
     src("Wikipedia — Lydia Ko (DOB 1997-04-24; LPGA Hall of Fame)", "Website", "https://en.wikipedia.org/wiki/Lydia_Ko", "other-trusted")],
    [], "LPGA Hall of Fame member, three Olympic medals (gold 2024) and youngest-ever World No.1 (male or female) — objective athlete category. Age evidence from her own official website. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-167", "Jeeno Thitikul",
    ev("Born February 20, 2003 in Ban Pong, Ratchaburi, Thailand — age 23 in 2026 — per AIG Women's Open official player page (structured birthDate 2003-02-20), golfnewsnation structured record, Wikipedia (born 20 February 2003) and madknows (February 20, 2003).",
       "AIG Women's Open — Jeeno Thitikul official player page (birthDate 2003-02-20)", "https://www.aigwomensopen.com/players/jeeno-thitikul"),
    ev("Identified as a woman via LPGA women's golf career — Women's World Golf Rankings No. 1, LPGA money-list leader 2025 (Wikipedia/AIG Women's Open player page).",
       "Wikipedia — Jeeno Thitikul (women's world No. 1 record)", "https://en.wikipedia.org/wiki/Jeeno_Thitikul"),
    [src("AIG Women's Open — Jeeno Thitikul player page (birthDate 2003-02-20)", "Website", "https://www.aigwomensopen.com/players/jeeno-thitikul", "official"),
     src("Wikipedia — Jeeno Thitikul (DOB 2003-02-20; world No. 1 record)", "Website", "https://en.wikipedia.org/wiki/Jeeno_Thitikul", "other-trusted"),
     src("Golf News Nation — Jeeno Thitikul (DOB February 20, 2003)", "Website", "https://golfnewsnation.com/players/jeeno-thitikul-185", "other-trusted")],
    [], "Women's World No. 1, 2022 LPGA Rookie of the Year and youngest-ever professional tournament winner (14) — objective athlete category; verified 23 years old. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-168", "Lilia Vu",
    ev("Born October 14, 1997 in Fountain Valley, California — age 28 in 2026 — per AIG Women's Open official player page (structured birthDate 1997-10-14), Wikipedia (born October 14, 1997), sportskeeda (October 14, 1997) and surprisesports biography table.",
       "AIG Women's Open — Lilia Vu official player page (birthDate 1997-10-14)", "https://www.aigwomensopen.com/players/lilia-vu"),
    ev("Identified as a woman via LPGA women's golf career — two-time major champion (2023 Chevron, 2023 Women's British Open), 2023 LPGA Player of the Year (Wikipedia/AIG Women's Open).",
       "Wikipedia — Lilia Vu (2x major champion; LPGA Player of the Year 2023)", "https://en.wikipedia.org/wiki/Lilia_Vu"),
    [src("AIG Women's Open — Lilia Vu official player page (birthDate 1997-10-14)", "Website", "https://www.aigwomensopen.com/players/lilia-vu", "official"),
     src("Wikipedia — Lilia Vu (DOB 1997-10-14; 2x major champion)", "Website", "https://en.wikipedia.org/wiki/Lilia_Vu", "other-trusted"),
     src("Surprise Sports — Lilia Vu biography (DOB October 14, 1997; Instagram @liliavu)", "Website", "https://surprisesports.com/athletes-biography/lilia-vu-golfer-net-worth/", "other-trusted"),
     src("Instagram — @liliavu (surprisesports biography table)", "Instagram", "https://www.instagram.com/liliavu/", "verified-platform")],
    [], "Two-time major champion and 2023 LPGA Rolex Player of the Year (UCLA record 8 wins) — objective athlete category. IG handle via surprisesports bio; count not captured — UNKNOWN.",
    [acct("Instagram", "@liliavu", "https://www.instagram.com/liliavu/", "Handle via surprisesports.com biography table; count not captured.")]))


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
