#!/usr/bin/env python3
"""Session 12 batch H (2026-09-06): 6 verified adds (W-2026-159..164).
Track & field wave: worldathletics.org/european-athletics.com official athlete
pages + Roma 2024 official bio + Britannica/Wikipedia corroboration.
Dup-guard: all 6 names grep-checked before authoring.
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
    return {"id": i, "displayName": n, "categories": ["Athlete", "Track and Field", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-159", "Femke Bol",
    ev("Born February 23, 2000 in Amersfoort, Netherlands — age 26 in 2026 — per the Roma 2024 European Championships official athlete feature (Date of birth: February 23, 2000), thecityceleb (February 23, 2000) and sggreek replication.",
       "Roma 2024 (European Athletics Championships official) — Femke Bol athlete feature ('Date of birth February 23, 2000')", "https://www.roma2024.eu/en/meet-the-athletes-femke-bol/"),
    ev("Identified as a woman via women's 400m hurdles career — women's world 400m hurdles title (Budapest 2023), women's Olympic medals, thecityceleb profile 'Gender: Female', and sggreek ('Gender: Female').",
       "Roma 2024 official — Femke Bol (women's hurdles champion bio)", "https://www.roma2024.eu/en/meet-the-athletes-femke-bol/"),
    [src("Roma 2024 — Femke Bol official athlete feature (DOB Feb 23, 2000)", "Website", "https://www.roma2024.eu/en/meet-the-athletes-femke-bol/", "official"),
     src("TheCityCeleb — Femke Bol biography (DOB February 23, 2000; Gender: Female)", "Website", "https://www.thecityceleb.com/biography/public-figure/sportsperson/femke-bol-biography-age-net-worth-parents-career-awards-wikipedia-pictures-boyfriend/", "other-trusted"),
     src("SGGreek — Femke Bol wiki (Date of Birth 23 February 2000; Gender Female)", "Website", "https://sggreek.com/femke-bol-net-worth-wiki-age-height/", "other-trusted")],
    ["CONFLICTING_INFORMATION"],
    "2023 world 400m hurdles champion, Paris 2024 4x400m mixed relay gold medalist and indoor 400m world-record holder — objective athlete category. Flag: two low-tier biographies (mabumbe, unipostwire) list April 23, 2000 — outlier vs Roma 2024 official bio + two others (all Feb 23, 2000); official/majority value recorded. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(ent("W-2026-160", "Gabby Thomas",
    ev("Born December 7, 1996 in Atlanta, Georgia — age 29 in 2026 — per Wikipedia (born December 7, 1996), nbcolympics.com official athlete bio ('She was born December 7, 1996'), Kiddle replication and EssentiallySports (December 7th, 1996).",
       "NBC Olympics — Gabby Thomas athlete bio (born December 7, 1996)", "https://www.nbcolympics.com/news/gabby-thomas-meet-athlete"),
    ev("Identified as a woman via women's sprint career — 2024 Olympic women's 200m champion plus 4x100m/4x400m relay golds; 'first female sprinter sponsored by New Balance' per NewsUnzip; women's Harvard track record (newsunzip handles list).",
       "NBC Olympics — Gabby Thomas bio (women's Olympic sprint medals)", "https://www.nbcolympics.com/news/gabby-thomas-meet-athlete"),
    [src("NBC Olympics — Gabby Thomas athlete bio (DOB Dec 7, 1996)", "Website", "https://www.nbcolympics.com/news/gabby-thomas-meet-athlete", "official"),
     src("Wikipedia — Gabby Thomas (DOB 1996-12-07; 2024 Olympic 200m champion)", "Website", "https://en.wikipedia.org/wiki/Gabrielle_Thomas", "other-trusted"),
     src("NewsUnzip — Gabby Thomas bio (DOB 7th December 1996; IG @gabbythomas; Twitter @ItsGabrielleT)", "Website", "https://www.newsunzip.com/wiki/gabby-thomas/", "other-trusted"),
     src("Instagram — @gabbythomas (newsunzip socials list)", "Instagram", "https://www.instagram.com/gabbythomas/", "verified-platform"),
     src("X — @ItsGabrielleT (newsunzip socials list)", "X", "https://x.com/ItsGabrielleT", "verified-platform")],
    [], "3x gold medalist at Paris 2024 (200m + both relays) and Harvard epidemiology master's grad — objective athlete category. Handles via NewsUnzip social list; counts not captured — UNKNOWN.",
    [acct("Instagram", "@gabbythomas", "https://www.instagram.com/gabbythomas/", "Handle via newsunzip.com socials list; count not captured."),
     acct("X", "@ItsGabrielleT", "https://x.com/ItsGabrielleT", "Handle via newsunzip.com socials list; count not captured.")]))

NEW.append(ent("W-2026-161", "Dina Asher-Smith",
    ev("Born December 4, 1995 in Orpington, Greater London — age 30 in 2026 — per European Athletics official athlete record (structured birthDate 1995-12-04), sportytell (December 4, 1995), thesportsdb profile and thecityceleb (birthDate JSON-LD 1995-12-04).",
       "European Athletics — Dina Asher-Smith athlete record (birthDate 1995-12-04)", "https://www.european-athletics.com/home/historical-data/athletes/14378282"),
    ev("Identified as a woman via European Athletics structured data ('gender: Female') and women's sprint career — 2019 women's world 200m champion, fastest British woman on record (sportytell/thesportsdb).",
       "European Athletics — Dina Asher-Smith ('gender: Female' structured)", "https://www.european-athletics.com/home/historical-data/athletes/14378282"),
    [src("European Athletics — Dina Asher-Smith record (birthDate 1995-12-04; gender Female)", "Website", "https://www.european-athletics.com/home/historical-data/athletes/14378282", "official"),
     src("SportyTell — Dina Asher-Smith biography (DOB December 4, 1995)", "Website", "https://sportytell.com/biography/dina-asher-smith-biography-facts/", "other-trusted"),
     src("TheSportsDB — Dina Asher-Smith profile (born 4 December 1995; career honors)", "Website", "https://www.thesportsdb.com/player/34193279-Dina-Asher-Smith", "other-trusted")],
    [], "2019 world 200m champion and British record holder (100m/200m) — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-162", "Yulimar Rojas",
    ev("Born October 21, 1995 in Caracas, Venezuela — age 30 in 2026 — per World Athletics official athlete profile ('Born 21 OCT 1995'), Britannica (born October 21, 1995), Wikipedia (born 21 October 1995) and Kiddle replication.",
       "World Athletics — Yulimar Rojas official profile ('Born 21 OCT 1995')", "https://worldathletics.org/athletes/venezuela/yulimar-rojas-14436431"),
    ev("Identified as a woman via women's triple jump career — women's triple jump world record holder, first Venezuelan woman to win Olympic gold (World Athletics official/Britannica).",
       "World Athletics — Yulimar Rojas profile ('Woman's triple jump' world record holder)", "https://worldathletics.org/athletes/venezuela/yulimar-rojas-14436431"),
    [src("World Athletics — Yulimar Rojas official profile (Born 21 OCT 1995)", "Website", "https://worldathletics.org/athletes/venezuela/yulimar-rojas-14436431", "official"),
     src("Britannica — Yulimar Rojas (born October 21, 1995)", "Website", "https://www.britannica.com/biography/Yulimar-Rojas", "other-trusted"),
     src("Wikipedia — Yulimar Rojas (DOB 1995-10-21; WR 15.74m)", "Website", "https://en.wikipedia.org/wiki/Yulimar_Rojas", "other-trusted")],
    [], "Women's triple jump world-record holder (15.74m indoor), 2020 Olympic champion and 4x world champion — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-163", "Faith Kipyegon",
    ev("Born January 10, 1994 in Bomet/Kabelo Village, Kenya — age 32 in 2026 — per kenyanheroes.com (Born: January 10, 1994), trendingcelebs profile (January 10, 1994), Wikipedia (born 10 January 1994) and Grokipedia (10 January 1994).",
       "Kenyan Heroes — Faith Kipyegon profile ('Born: January 10, 1994')", "https://kenyanheroes.com/hero/faith-kipyegon/"),
    ev("Identified as a woman via women's middle-distance career — first three-time women's 1500m Olympic champion (Rio/Tokyo/Paris), women's 1500m and mile world-record holder (Wikipedia/Grokipedia).",
       "Wikipedia — Faith Kipyegon (women's 1500m WR; 3x Olympic champion)", "https://en.wikipedia.org/wiki/Faith_Kipyegon"),
    [src("Kenyan Heroes — Faith Kipyegon (DOB January 10, 1994)", "Website", "https://kenyanheroes.com/hero/faith-kipyegon/", "age-evidence"),
     src("Wikipedia — Faith Kipyegon (DOB 1994-01-10; 1500m/mile WRs)", "Website", "https://en.wikipedia.org/wiki/Faith_Kipyegon", "other-trusted"),
     src("Grokipedia — Faith Kipyegon (born 10 January 1994; WR 3:48.68 at 2025 Prefontaine)", "Website", "https://grokipedia.com/page/Faith_Kipyegon", "other-trusted")],
    [], "Three-time Olympic 1500m champion and world-record holder (1500m and Mile) — objective athlete category. Birthplace listed as Bomet County by trendingcelebs/Wikipedia vs 'village near Keringet, Nakuru County' upbringing note — both documented. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-164", "Shelly-Ann Fraser-Pryce",
    ev("Born December 27, 1986 in Kingston, Jamaica — age 39 in 2026 — per Britannica (born December 27, 1986), Wikipedia (born 27 December 1986), Simple English Wikipedia (27 December 1986) and famousbirthdays (Birthday December 27, 1986).",
       "Britannica — Shelly-Ann Fraser-Pryce (born December 27, 1986)", "https://www.britannica.com/biography/Shelly-Ann-Fraser-Pryce"),
    ev("Identified as a woman via women's sprint career — two-time women's Olympic 100m champion, five-time women's world 100m champion; 'first Caribbean woman to win gold in the 100m' (Britannica/Wikipedia).",
       "Britannica — Shelly-Ann Fraser-Pryce (women's 100m titles)", "https://www.britannica.com/biography/Shelly-Ann-Fraser-Pryce"),
    [src("Britannica — Shelly-Ann Fraser-Pryce (DOB 1986-12-27)", "Website", "https://www.britannica.com/biography/Shelly-Ann-Fraser-Pryce", "age-evidence"),
     src("Wikipedia — Shelly-Ann Fraser-Pryce (DOB 1986-12-27; 8x Olympic medals)", "Website", "https://en.wikipedia.org/wiki/Shelly-Ann_Fraser-Pryce", "other-trusted"),
     src("Famous Birthdays — Shelly-Ann Fraser-Pryce (December 27, 1986)", "Website", "https://www.famousbirthdays.com/people/shelly-ann-fraser-pryce.html", "other-trusted")],
    [], "Eight-time Olympic medalist and most decorated 100m sprinter in history ('Pocket Rocket') — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))


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
