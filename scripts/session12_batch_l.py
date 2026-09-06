#!/usr/bin/env python3
"""Session 12 batch L (2026-09-06): 4 verified adds (W-2026-177..180); Kelsey Robinson Cook excluded — dup-guard caught her pre-existing batch-A entry.
US women's volleyball wave: women.volleybox.net JSON-LD (gender Female +
birthDate + sameAs handles), volleyballworld.com official bios, redbull
JSON-LD (Skinner: gender female + sameAs IG), usavolleyball.org official,
utsports official. Dup-guard pre-checked all five.
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
    return {"id": i, "displayName": n, "categories": ["Athlete", "Volleyball", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-177", "Madisen Skinner",
    ev("Born July 1, 2001 in Katy, Texas — age 25 in 2026 — per Red Bull athlete profile (structured birthDate 2001-07-01), volleyballworld.com official VNL bio (Birth date 01/07/2001), famousbirthdays (July 1, 2001) and Wikipedia (born July 1, 2001).",
       "Red Bull — Madisen Skinner athlete profile (birthDate 2001-07-01)", "https://www.redbull.com/sg-en/athlete/madisen-skinner"),
    ev("Identified as a woman via Red Bull structured data ('gender: female'), volleybox structured data ('gender: Female') and US women's national-team opposite career — 3x NCAA champion (Kentucky 2020, Texas 2022/2023), 2023 Honda Sports Award.",
       "Red Bull — Madisen Skinner profile ('gender: female'; NCAA titles record)", "https://www.redbull.com/sg-en/athlete/madisen-skinner"),
    [src("Red Bull — Madisen Skinner (DOB 2001-07-01; gender female; sameAs IG)", "Website", "https://www.redbull.com/sg-en/athlete/madisen-skinner", "age-evidence"),
     src("Volleyball World — Madisen Skinner VNL official bio (birth date 01/07/2001)", "Website", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/210604", "official"),
     src("Women.volleybox — Madisen Skinner (birthDate/gender Female; sameAs IG/X)", "Website", "https://women.volleybox.net/madisen-skinner-p46025", "other-trusted"),
     src("Instagram — @madisenskinner (redbull + volleybox structured sameAs)", "Instagram", "https://www.instagram.com/madisenskinner/", "verified-platform"),
     src("X — @madiskinnerr (volleybox structured sameAs)", "X", "https://x.com/madiskinnerr", "verified-platform")],
    [], "Three-time NCAA champion and 2023 Honda Sports Award winner (LOVB Austin) — objective athlete category. Handles via redbull/volleybox structured sameAs; counts not captured — UNKNOWN.",
    [acct("Instagram", "@madisenskinner", "https://www.instagram.com/madisenskinner/", "Handle via redbull + women.volleybox.net structured sameAs; count not captured."),
     acct("X", "@madiskinnerr", "https://x.com/madiskinnerr", "Handle via women.volleybox.net structured sameAs; count not captured.")]))

NEW.append(ent("W-2026-178", "Dana Rettke",
    ev("Born January 21, 1999 in Riverside, Illinois — age 27 in 2026 — per women.volleybox.net structured record (birthDate 1999-01-21) and Wikipedia (born January 21, 1999).",
       "Women.volleybox — Dana Rettke (birthDate 1999-01-21)", "https://women.volleybox.net/dana-rettke-p21214"),
    ev("Identified as a woman via volleybox structured data ('gender: Female') and US women's national-team middle-blocker career — first five-time AVCA First Team All-American (Wikipedia).",
       "Women.volleybox — Dana Rettke ('gender: Female' structured record)", "https://women.volleybox.net/dana-rettke-p21214"),
    [src("Women.volleybox — Dana Rettke (DOB 1999-01-21; gender Female; sameAs IG/TikTok/FB)", "Website", "https://women.volleybox.net/dana-rettke-p21214", "age-evidence"),
     src("Wikipedia — Dana Rettke (DOB 1999-01-21; Wisconsin 5x All-American)", "Website", "https://en.wikipedia.org/wiki/Dana_Rettke", "other-trusted"),
     src("Instagram — @dana_rettke (volleybox structured sameAs)", "Instagram", "https://www.instagram.com/dana_rettke/", "verified-platform"),
     src("TikTok — @dana_rettke (volleybox structured sameAs)", "TikTok", "https://www.tiktok.com/@dana_rettke", "verified-platform")],
    [], "USWNT middle blocker, first five-time AVCA First Team All-American (Wisconsin), now at Eczacıbaşı — objective athlete category. Handles via volleybox structured sameAs; counts not captured — UNKNOWN.",
    [acct("Instagram", "@dana_rettke", "https://www.instagram.com/dana_rettke/", "Handle via women.volleybox.net structured sameAs; count not captured."),
     acct("TikTok", "@dana_rettke", "https://www.tiktok.com/@dana_rettke", "Handle via women.volleybox.net structured sameAs; count not captured.")]))

NEW.append(ent("W-2026-179", "Lauren Carlini",
    ev("Born February 28, 1995 in Geneva/Aurora, Illinois — age 31 in 2026 — per Wikipedia (born February 28, 1995), USA Volleyball official athlete page (Born in 1995) and volleycrafters (Date of Birth February 28, 1995).",
       "Wikipedia — Lauren Carlini (born February 28, 1995)", "https://en.wikipedia.org/wiki/Lauren_Carlini"),
    ev("Identified as a woman via US women's national volleyball team career — 2016 Sullivan Award winner as America's best amateur athlete (Wikipedia/usavolleyball.org official athlete page).",
       "USA Volleyball — Lauren Carlini official athlete page", "https://usavolleyball.org/athlete/lauren-carlini/"),
    [src("USA Volleyball — Lauren Carlini official athlete page (Born in 1995; bio)", "Website", "https://usavolleyball.org/athlete/lauren-carlini/", "official"),
     src("Wikipedia — Lauren Carlini (DOB 1995-02-28; 2016 Sullivan Award)", "Website", "https://en.wikipedia.org/wiki/Lauren_Carlini", "age-evidence"),
     src("VolleyCrafters — Lauren Carlini bio (DOB February 28, 1995)", "Website", "https://volleycrafters.com/lauren-carlini/", "other-trusted")],
    [], "2016 Sullivan Award winner and U.S. women's national-team setter (Wisconsin All-American) — objective athlete category. Birthplace: Wikipedia says Geneva, volleycrafters says Aurora — both recorded. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-180", "Jordyn Poulter",
    ev("Born July 31, 1997 in Naperville, Illinois — age 29 in 2026 — per volleyballworld.com official player bio (Birth date 31/07/1997 across VNL and 2025 World Championship pages), women.volleybox.net structured birthDate 1997-07-31 and grokipedia (born July 31, 1997).",
       "Volleyball World — Jordyn Poulter official bio (birth date 31/07/1997)", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/143517"),
    ev("Identified as a woman via volleybox structured data ('gender: Female') and US women's national-team setter career — Tokyo 2020 Olympic gold (named Best Setter) and Paris 2024 silver (grokipedia/volleyballworld).",
       "Women.volleybox — Jordyn Poulter ('gender: Female' structured record)", "https://women.volleybox.net/jordyn-poulter-p4851/indoor_tournaments"),
    [src("Volleyball World — Jordyn Poulter official player bio (birth date 31/07/1997)", "Website", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/143517", "official"),
     src("Women.volleybox — Jordyn Poulter (DOB 1997-07-31; gender Female; sameAs IG/FB)", "Website", "https://women.volleybox.net/jordyn-poulter-p4851/indoor_tournaments", "gender-evidence"),
     src("Grokipedia — Jordyn Poulter (DOB July 31, 1997; Tokyo 2020 gold Best Setter)", "Website", "https://grokipedia.com/page/Jordyn_Poulter", "other-trusted"),
     src("Instagram — @jordyn_poulter (volleybox structured sameAs)", "Instagram", "https://www.instagram.com/jordyn_poulter/", "verified-platform")],
    [], "Tokyo 2020 Olympic gold medalist and Best Setter (LOVB Salt Lake) — objective athlete category. IG handle via volleybox structured sameAs; count not captured — UNKNOWN.",
    [acct("Instagram", "@jordyn_poulter", "https://www.instagram.com/jordyn_poulter/", "Handle via women.volleybox.net structured sameAs; count not captured.")]))


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
