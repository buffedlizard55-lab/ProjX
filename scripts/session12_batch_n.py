#!/usr/bin/env python3
"""Session 12 batch N (2026-09-06): 2 verified adds (W-2026-185, W-2026-186→187); Kate Douglass/Torri Huske/Gretchen Walsh all dup-caught as pre-existing (Session 11 batch 2).
Women's swimming wave: olympics.com/nbcolympics official bios, olympics.com.au
(Australian Olympic Committee) JSON-LD (birthDate + gender Female + IG sameAs),
Wikipedia/Britannica. Walsh DOB conflict (Jan 29 vs Jan 16 fan site) flagged.
Dup-guard pre-checked; Kate Douglass/Simone Manuel batches C/D confirmed new.
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
    return {"id": i, "displayName": n, "categories": ["Athlete", "Swimming", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-185", "Summer McIntosh",
    ev("Born August 18, 2006 in Toronto, Ontario, Canada — age 20 in 2026 — per Wikipedia (born August 18, 2006), EssentiallySports (born on 18th August 2006), ESPN Olympics bio (Date of birth: 2006-08-18) and olympics.com official profile (Year of Birth 2006).",
       "ESPN — Summer McIntosh Olympics bio (Date of birth: 2006-08-18)", "https://www.espn.com/olympics/summer/2024/athletes/_/athlete/64185"),
    ev("Identified as a woman via Canadian women's Olympic swimming career — three-time Olympic champion (Paris 2024), women's 200m butterfly/200m IM/400m IM/400m freestyle world-record holder (Wikipedia/olympics.com).",
       "Olympics.com — Summer McIntosh official athlete profile (3x Olympic gold)", "https://www.olympics.com/en/athletes/summer-mcintosh"),
    [src("Olympics.com — Summer McIntosh official athlete profile (Year of Birth 2006; 3G Paris 2024)", "Website", "https://www.olympics.com/en/athletes/summer-mcintosh", "official"),
     src("ESPN — Summer McIntosh Olympics bio (DOB 2006-08-18)", "Website", "https://www.espn.com/olympics/summer/2024/athletes/_/athlete/64185", "age-evidence"),
     src("Wikipedia — Summer McIntosh (DOB 2006-08-18; world-record list)", "Website", "https://en.wikipedia.org/wiki/Summer_McIntosh", "other-trusted")],
    [], "Three-time Olympic champion and four-time world-record holder — objective athlete category; verified 20 years old. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-186", "Ariarne Titmus",
    ev("Born September 7, 2000 in Launceston, Tasmania — age 25 in 2026 — per the Australian Olympic Committee official Olympian page (structured birthDate 2000-09-07), Wikipedia (born 7 September 2000), Britannica (born September 7, 2000) and playerswiki.",
       "Australian Olympic Committee — Ariarne Titmus Olympian page (birthDate 2000-09-07)", "https://www.olympics.com.au/olympians/ariarne-titmus/"),
    ev("Identified as a woman via the AOC structured record ('gender: Female') and women's Olympic swimming career — back-to-back women's 400m freestyle Olympic champion (2020/2024), 200m freestyle world-record holder (Wikipedia/Britannica).",
       "Australian Olympic Committee — Ariarne Titmus ('gender: Female' structured; Olympic titles)", "https://www.olympics.com.au/olympians/ariarne-titmus/"),
    [src("Australian Olympic Committee — Ariarne Titmus (birthDate 2000-09-07; gender Female; sameAs IG ariarnetitmus_)", "Website", "https://www.olympics.com.au/olympians/ariarne-titmus/", "official"),
     src("Britannica — Ariarne Titmus (born September 7, 2000)", "Website", "https://www.britannica.com/biography/Ariarne-Titmus", "other-trusted"),
     src("Wikipedia — Ariarne Titmus (DOB 2000-09-07; WR 200m freestyle)", "Website", "https://en.wikipedia.org/wiki/Ariarne_Titmus", "other-trusted"),
     src("Instagram — @ariarnetitmus_ (AOC structured sameAs)", "Instagram", "https://www.instagram.com/ariarnetitmus_/", "verified-platform")],
    [], "Back-to-back Olympic 400m freestyle champion and 200m freestyle world-record holder (OAM) — objective athlete category. IG handle via AOC structured sameAs; count not captured — UNKNOWN.",
    [acct("Instagram", "@ariarnetitmus_", "https://www.instagram.com/ariarnetitmus_/", "Handle via olympics.com.au structured sameAs record; count not captured.")]))


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
