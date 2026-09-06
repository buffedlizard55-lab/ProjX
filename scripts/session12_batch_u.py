#!/usr/bin/env python3
"""Session 12 batch U (2026-09-06): 2 verified adds (W-2026-198..199).
Freestyle skiing + women's cricket wave: redbull JSON-LD (gender female +
birthDate + sameAs IG eileen_gu_), olympics.com + Britannica (Gu);
espncricinfo official + cricket.com.au structured (Mandhana).
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

NEW.append(ent("W-2026-198", "Eileen Gu (Gu Ailing)", ["Athlete", "Skiing", "Creator"],
    ev("Born September 3, 2003 in San Francisco, California — age 23 in 2026 — per Britannica ('Born: September 3, 2003... (age 23)'), Red Bull athlete page structured record (birthDate 2003-09-03), olympics.com official profile ('Born on 3 September, 2003') and Wikipedia (born September 3, 2003).",
       "Britannica — Eileen Gu (born September 3, 2003)", "https://www.britannica.com/biography/Eileen-Gu"),
    ev("Identified as a woman via Red Bull structured record ('gender: female') and women's freestyle skiing career — six Olympic medals (3 gold) in women's halfpipe/slopestyle/big air, the most decorated freestyle skier in Olympic history (Wikipedia/Britannica/olympics.com).",
       "Red Bull — Eileen Gu athlete page (JSON-LD gender female + birthDate + sameAs)", "https://www.redbull.com/us-en/athlete/eileen-gu"),
    [src("Britannica — Eileen Gu (born September 3, 2003; Olympic medals)", "Website", "https://www.britannica.com/biography/Eileen-Gu", "age-evidence"),
     src("Red Bull — Eileen Gu athlete page (birthDate 2003-09-03; gender female; sameAs IG)", "Website", "https://www.redbull.com/us-en/athlete/eileen-gu", "official"),
     src("Olympics.com — Eileen Gu official athlete profile (Born 3 September 2003)", "Website", "https://www.olympics.com/en/athletes/gu-ailing-eileen", "official"),
     src("Instagram — @eileen_gu_ (Red Bull structured sameAs)", "Instagram", "https://www.instagram.com/eileen_gu_", "verified-platform")],
    "Six-time Olympic medalist (3 gold) in women's freeski halfpipe/slopestyle/big air — most decorated freestyle skier in Olympic history — and Stanford graduate/model — objective athlete category; verified 23 years old. IG handle via Red Bull structured sameAs; count not captured — UNKNOWN.",
    [acct("Instagram", "@eileen_gu_", "https://www.instagram.com/eileen_gu_", "Handle via Red Bull athlete page structured sameAs (instagram.com/eileen_gu_); count not captured.")]))

NEW.append(ent("W-2026-199", "Smriti Mandhana", ["Athlete", "Cricket", "Creator"],
    ev("Born July 18, 1996 in Mumbai (Bombay), Maharashtra, India — age 30 in 2026 — per ESPNcricinfo official player profile (Born July 18, 1996), cricket.com.au structured record (birthDate 1996-07-18, Age 30), simple.wikipedia (18 July 1996) and sportsdunia structured record (birthDate 1996-07-18).",
       "ESPNcricinfo — Smriti Mandhana official profile (Born July 18, 1996)", "https://www.espncricinfo.com/cricketers/smriti-mandhana-597806"),
    ev("Identified as a woman via sportsdunia structured record ('gender: Female') and India women's national cricket team career — first India women's player to score hundreds in all three international formats; RCB Women WPL (ESPNcricinfo/simple.wikipedia).",
       "SportsDunia — Smriti Mandhana biography (structured gender Female + birthDate)", "https://www.sportsdunia.com/cricket-players/smriti-mandhana-biography"),
    [src("ESPNcricinfo — Smriti Mandhana profile (Born July 18, 1996; India women)", "Website", "https://www.espncricinfo.com/cricketers/smriti-mandhana-597806", "official"),
     src("cricket.com.au — Smriti Mandhana (birthDate 1996-07-18 structured)", "Website", "https://www.cricket.com.au/players/CA:418/smriti-mandhana", "official"),
     src("SportsDunia — Smriti Mandhana biography (birthDate + gender Female structured)", "Website", "https://www.sportsdunia.com/cricket-players/smriti-mandhana-biography", "other-trusted")],
    "India women's vice-captain/ace opening batter — first India woman with centuries in all three international formats; ICC Women's Cricketer of the Year 2021 — objective athlete category; verified 30 years old. No social handle captured this pass — follower range UNKNOWN.", []))


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
