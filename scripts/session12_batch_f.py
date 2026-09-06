#!/usr/bin/env python3
"""Session 12 batch F (2026-09-06): 6 verified adds (W-2026-147..152).
NWSL roster tail: midfielders/defenders/goalkeepers. Same schema/helpers as
batch E; dup-guard passed at write time (names grep-checked before authoring).
Written as an archive copy of the exact inline build that ran.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

RANGES = [(1000,"Under 1K"),(5000,"1K–4.9K"),(10000,"5K–9.9K"),(25000,"10K–24.9K"),
          (50000,"25K–49.9K"),(100000,"50K–99.9K"),(250000,"100K–249.9K"),
          (500000,"250K–499.9K"),(1000000,"500K–999.9K"),(5000000,"1M–4.9M")]
def sr(n):
    if n is None: return "FOLLOWER_RANGE_UNKNOWN"
    for l, lab in RANGES:
        if n < l: return lab
    return "5M+"

def acct(p, u, url, note):
    return {"platform": p, "username": u, "profileUrl": url,
            "followerCountDisplay": "FOLLOWER_COUNT_UNKNOWN", "followerCountNumeric": None,
            "countType": "unknown", "checkedAt": CHECKED,
            "followerSizeRange": "FOLLOWER_RANGE_UNKNOWN", "sourceNote": note}

def big(accounts):
    return {"platform": None, "username": None, "display": None, "numeric": None,
            "sizeRange": "FOLLOWER_RANGE_UNKNOWN", "checkedAt": CHECKED}

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

def ent(i, n, a, g, s, flags, notes, accts):
    return {"id": i, "displayName": n, "categories": ["Athlete", "Soccer", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts, "largestPublicFollowing": big(accts),
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-147", "Savannah DeMelo",
    ev("Born March 26, 1998 in Bellflower, California — age 28 in 2026 — per HollywoodLife (b. Mar. 26, 1998) and Wikipedia (born March 26, 1998).",
       "HollywoodLife — Savannah DeMelo (b. Mar. 26, 1998)", "https://hollywoodlife.com/feature/who-is-savannah-demelo-5144942/"),
    ev("Identified as a woman via USWNT women's national-team career — 2023 FIFA Women's World Cup squad (HollywoodLife/Wikipedia) and Racing Louisville FC midfielder.",
       "Wikipedia — Savannah DeMelo (2023 World Cup squad)", "https://en.wikipedia.org/wiki/Savannah_DeMelo"),
    [src("Wikipedia — Savannah DeMelo (DOB 1998-03-26; 2023 World Cup debut)", "Website", "https://en.wikipedia.org/wiki/Savannah_DeMelo", "age-evidence"),
     src("HollywoodLife — Savannah DeMelo profile (b. Mar. 26, 1998; World Cup squad)", "Website", "https://hollywoodlife.com/feature/who-is-savannah-demelo-5144942/", "other-trusted")],
    [], "USWNT midfielder and 2023 World Cup squad member (USC Trojans; 2022 NWSL fourth pick) — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-148", "Haley Hopkins",
    ev("Born December 21, 1998 in Newport Beach, California — age 27 in 2026 — per Wikipedia (born December 21, 1998).",
       "Wikipedia — Haley Hopkins (born December 21, 1998)", "https://en.wikipedia.org/wiki/Haley_Hopkins"),
    ev("Identified as a woman via NWSL women's pro career (Kansas City Current forward) and role as NWSL Players Association president since 2025 (Wikipedia).",
       "Wikipedia — Haley Hopkins (NWSLPA president since 2025)", "https://en.wikipedia.org/wiki/Haley_Hopkins"),
    [src("Wikipedia — Haley Hopkins (DOB 1998-12-21; NWSLPA president)", "Website", "https://en.wikipedia.org/wiki/Haley_Hopkins", "age-evidence")],
    [], "Two-time All-American (Vanderbilt/Virginia), 2023 NWSL first-round pick and NWSLPA president — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-149", "Aubrey Kingsbury (née Bledsoe)",
    ev("Born November 20, 1991 in Cincinnati, Ohio — age 34 in 2026 — per Wikipedia (born November 20, 1991), ESPN structured birthDate 11/20/1991 and Wikiwand replication.",
       "Wikipedia — Aubrey Kingsbury (born November 20, 1991)", "https://en.wikipedia.org/wiki/Aubrey_Kingsbury"),
    ev("Identified as a woman via NWSL women's pro career — two-time NWSL Goalkeeper of the Year, MVP of the Washington Spirit's 2021 NWSL Championship (Wikipedia/Wikiwand).",
       "Wikipedia — Aubrey Kingsbury (2x NWSL GK of the Year)", "https://en.wikipedia.org/wiki/Aubrey_Kingsbury"),
    [src("Wikipedia — Aubrey Kingsbury (DOB 1991-11-20)", "Website", "https://en.wikipedia.org/wiki/Aubrey_Kingsbury", "age-evidence"),
     src("ESPN — Aubrey Kingsbury player page (birthDate 11/20/1991 structured)", "Website", "https://www.espn.com/soccer/player/bio/_/id/290259/aubrey-kingsbury", "other-trusted"),
     src("Wikiwand — Aubrey Kingsbury (DOB 1991-11-20; career honors)", "Website", "https://wikiwand.com/en/articles/Aubrey_Kingsbury", "other-trusted")],
    [], "Two-time NWSL Goalkeeper of the Year and 2021 championship MVP (birth name Aubrey Renee Bledsoe) — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-150", "Jane Campbell",
    ev("Born February 17, 1995 in Kennesaw, Georgia — age 31 in 2026 — per US Soccer official profile (Date of Birth Feb 17 1995), Wikipedia (born February 17, 1995), ESPN structured birthDate 2/17/1995 and Houston Dash official page (2.17.1995).",
       "US Soccer — Jane Campbell official profile (DOB Feb 17 1995)", "https://www.ussoccer.com/players/c/jane-campbell"),
    ev("Identified as a woman via USWNT women's national-team goalkeeper career — 2021 Olympic bronze medalist, youngest goalkeeper ever called into a Senior WNT camp (US Soccer official).",
       "US Soccer — Jane Campbell official profile ('2021 Olympic Bronze Medalist')", "https://www.ussoccer.com/players/c/jane-campbell"),
    [src("US Soccer — Jane Campbell official player profile (DOB Feb 17 1995; Olympic bronze 2021)", "Website", "https://www.ussoccer.com/players/c/jane-campbell", "official"),
     src("Houston Dash — Jane Campbell official bio (DOB 2.17.1995)", "Website", "https://www.houstondynamofc.com/houstondash/players/jane-campbell/", "official"),
     src("Wikipedia — Jane Campbell (soccer) (DOB 1995-02-17)", "Website", "https://en.wikipedia.org/wiki/Jane_Campbell_(soccer)", "other-trusted")],
    [], "2021 Olympic bronze medalist and 2023 NWSL Goalkeeper of the Year — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-151", "Tara Rudd (née McKeown)",
    ev("Born July 2, 1999 in Newbury Park, California — age 27 in 2026 — per FBref (Born: July 2, 1999, structured birthDate 1999-07-02), Wikipedia under Tara Rudd (born July 2, 1999), playmakerstats structured record and famousbirthdays (Birthday July 2, 1999).",
       "FBref — Tara McKeown (born July 2, 1999; birthDate structured)", "https://fbref.com/en/players/2d8ec240/Tara-McKeown"),
    ev("Identified as a woman via USWNT women's national-team center-back career and Washington Spirit NWSL play (FBref/Wikipedia; USWNT call-up January 2025 per famousbirthdays).",
       "Wikipedia — Tara Rudd (USWNT center back)", "https://en.wikipedia.org/wiki/Tara_Rudd"),
    [src("FBref — Tara McKeown (DOB 1999-07-02; Instagram handle)", "Website", "https://fbref.com/en/players/2d8ec240/Tara-McKeown", "age-evidence"),
     src("Wikipedia — Tara Rudd (DOB 1999-07-02; married name; USC All-American)", "Website", "https://en.wikipedia.org/wiki/Tara_Rudd", "other-trusted"),
     src("Famous Birthdays — Tara McKeown (July 2, 1999; USWNT call-up)", "Website", "https://www.famousbirthdays.com/people/tara-mckeown.html", "other-trusted"),
     src("Instagram — @taraaamckeown (fbref displayed handle)", "Instagram", "https://www.instagram.com/taraaamckeown/", "verified-platform")],
    [], "USWNT center back (2019 Pac-12 Forward of the Year at USC) — objective athlete category. IG handle via fbref; count not captured — UNKNOWN.",
    [acct("Instagram", "@taraaamckeown", "https://www.instagram.com/taraaamckeown/", "Handle via fbref player page; count not captured.")]))

NEW.append(ent("W-2026-152", "Michelle Cooper",
    ev("Born December 4, 2002 in Detroit, Michigan — age 23 in 2026 — per FBref (Born: December 4, 2002), fotmob structured birthDate 2002-12-04, ESPN structured birthDate 12/4/2002 and Wikipedia (born December 4, 2002).",
       "FBref — Michelle Cooper (born December 4, 2002)", "https://fbref.com/en/players/5f97ae2e/Michelle-Cooper"),
    ev("Identified as a woman via fotmob structured data ('gender: https://schema.org/Female') and USWNT women's national-team forward career with Kansas City Current (Wikipedia/fotmob).",
       "FotMob — Michelle Cooper (gender schema.org/Female structured)", "https://www.fotmob.com/players/1451722/michelle-cooper"),
    [src("FBref — Michelle Cooper (DOB 2002-12-04)", "Website", "https://fbref.com/en/players/5f97ae2e/Michelle-Cooper", "age-evidence"),
     src("FotMob — Michelle Cooper (birthDate 2002-12-04; gender Female JSON-LD)", "Website", "https://www.fotmob.com/players/1451722/michelle-cooper", "gender-evidence"),
     src("Wikipedia — Michelle Cooper (soccer) (DOB 2002-12-04; 2022 Hermann Trophy)", "Website", "https://en.wikipedia.org/wiki/Michelle_Cooper_(soccer)", "other-trusted")],
    [], "2022 Mac Hermann Trophy winner and Kansas City Current/USWNT forward — objective athlete category; verified 23 years old. No handle captured this pass — follower range UNKNOWN.", []))


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
