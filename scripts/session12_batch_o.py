#!/usr/bin/env python3
"""Session 12 batch O (2026-09-06): 2 verified adds (W-2026-187..188); Suni Lee dup-caught by URL guard (already W-2026-085).
US gymnastics wave. Dup-guard pre-checked names; Jade Carey/Jordan Chiles
dup-caught. (Sources list mirrors the applied inline build.)
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

RANGES = [(1000,"Under 1K"),(5000,"1K–4.9K"),(10000,"5K–9.9K"),(25000,"10K–24.9K"),
          (50000,"25K–49.9K"),(100000,"50K–99.9K"),(250000,"100K–249.9K")]
def sr(n):
    if n is None: return "FOLLOWER_RANGE_UNKNOWN"
    for l, lab in RANGES:
        if n < l: return lab
    return "250K–499.9K"

def acct(p, u, url, display, numeric, ctype, note):
    return {"platform": p, "username": u, "profileUrl": url,
            "followerCountDisplay": display, "followerCountNumeric": numeric,
            "countType": ctype, "checkedAt": CHECKED,
            "followerSizeRange": sr(numeric), "sourceNote": note}

def biggest(accts):
    known = [a for a in accts if a["followerCountNumeric"] is not None]
    if not known:
        return {"platform": None, "username": None, "display": None, "numeric": None,
                "sizeRange": "FOLLOWER_RANGE_UNKNOWN", "checkedAt": CHECKED}
    top = max(known, key=lambda a: a["followerCountNumeric"])
    return {"platform": top["platform"], "username": top["username"],
            "display": top["followerCountDisplay"], "numeric": top["followerCountNumeric"],
            "sizeRange": top["followerSizeRange"], "checkedAt": CHECKED}

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

def ent(i, n, a, g, s, flags, notes, accts):
    big = biggest(accts)
    return {"id": i, "displayName": n, "categories": ["Athlete", "Gymnastics", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts, "largestPublicFollowing": big,
            "overallFollowerSizeRange": big["sizeRange"]}

NEW = []

NEW.append(ent("W-2026-187", "Shilese Jones",
    ev("Born July 26, 2002 in Seattle, Washington — age 24 in 2026 — per nbcolympics.com official athlete bio ('was born July 26, 2002'), Wikipedia (born July 26, 2002), Kiddle replication and thecityceleb.",
       "NBColympics — Shilese Jones athlete bio (born July 26, 2002)", "https://www.nbcolympics.com/news/shilese-jones-meet-athlete"),
    ev("Identified as a woman via US women's gymnastics career — team gold at 2022/2023 World Championships, 2022 World all-around silver (Wikipedia/nbcolympics).",
       "Wikipedia — Shilese Jones (2x World team gold; 2022 AA silver)", "https://en.wikipedia.org/wiki/Shilese_Jones"),
    [src("NBColympics — Shilese Jones athlete bio (DOB July 26, 2002)", "Website", "https://www.nbcolympics.com/news/shilese-jones-meet-athlete", "official"),
     src("Wikipedia — Shilese Jones (DOB 2002-07-26; career record)", "Website", "https://en.wikipedia.org/wiki/Shilese_Jones", "other-trusted"),
     src("TheCityCeleb — Shilese Jones biography (Born 26 July, 2002; profile)", "Website", "https://www.thecityceleb.com/biography/public-figure/sportsperson/shilese-jones-biography-age-net-worth-parents-boyfriend-career-height-siblings-instagram/", "other-trusted")],
    [], "2x World Championship team gold medalist and 2022 World all-around silver medalist — objective athlete category. Note: famousbirthdays.com/people/shilese-jones.html displays 'over 110,000 followers on Instagram' but does not show the handle — count kept here in notes only (no account object), per the Manuel precedent. Follower range UNKNOWN on record.",
    []))

NEW.append(ent("W-2026-188", "Konnor McClain",
    ev("Born February 1, 2005 in Las Vegas, Nevada — age 21 in 2026 — per USA Gymnastics OFFICIAL athlete profile (Birthdate: 2/1/2005), Wikipedia (born February 1, 2005), playerswiki (February 1, 2005) and thegymter.net.",
       "USA Gymnastics — Konnor McClain official athlete profile (Birthdate 2/1/2005)",
       "https://members.usagym.org/pages/athletes/nationalTeamWomen.html?id=446354"),
    ev("Identified as a woman via US women's national gymnastics team membership — 2022 U.S. national champion (Wikipedia/USAG official 'Program: Women's Artistic').",
       "USA Gymnastics — Konnor McClain official profile ('Program: Women's Artistic')",
       "https://members.usagym.org/pages/athletes/nationalTeamWomen.html?id=446354"),
    [src("USA Gymnastics — Konnor McClain official athlete profile (Birthdate 2/1/2005; self-registered socials)", "Website", "https://members.usagym.org/pages/athletes/nationalTeamWomen.html?id=446354", "official"),
     src("Wikipedia — Konnor McClain (DOB 2005-02-01; 2022 US national champion)", "Website", "https://en.wikipedia.org/wiki/Konnor_McClain", "other-trusted"),
     src("TheGymter.net — Konnor McClain (Birthdate February 1, 2005)", "Website", "https://thegymter.net/konnor-mcclain/", "other-trusted"),
     src("X — @_KonnorMcClain (live profile; 1,786 followers)", "X", "https://x.com/_KonnorMcClain", "verified-platform"),
     src("Instagram — @konnormcclain_ (USAG official self-registered socials)", "Instagram", "https://www.instagram.com/konnormcclain_/", "verified-platform")],
    [], "2022 US all-around national champion and LSU gymnast — objective athlete category; verified 21 years old. X account count from live profile display (1,786 on 2026-09-06); USAG official bio lists her X as '@Konnormcclain_' — case/underscore variant of the same account, noted. IG handle via USAG self-registration — count not captured.",
    [acct("X", "@_KonnorMcClain", "https://x.com/_KonnorMcClain", "1,786", 1786, "exact",
          "Live X profile display on 2026-09-06 (1,786 followers; bio 'LSU Gymnastics ’27, 5x usa national team member'). USAG official bio registers the variant handle '@Konnormcclain_'."),
     acct("Instagram", "@konnormcclain_", "https://www.instagram.com/konnormcclain_/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
          "Handle via USAG official self-registered socials ('Instagram.com/Konnormcclain_'); count not captured.")]))


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
