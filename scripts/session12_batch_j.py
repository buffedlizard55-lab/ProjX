#!/usr/bin/env python3
"""Session 12 batch J (2026-09-06): 4 verified adds (W-2026-169..172).
USWNT legacy tier: ussoccer.com official profiles, ESPN, Wikipedia/Kiddle,
athlonsports (Ertz handles), fbref. Dup-guard pre-checked.
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
    return {"id": i, "displayName": n, "categories": ["Athlete", "Soccer", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-169", "Becky Sauerbrunn",
    ev("Born June 6, 1985 in St. Louis, Missouri — age 41 in 2026 — per US Soccer official profile (Date of Birth Jun 06 1985), ESPN structured birthdate 6/6/1985 and mysuite biodata (Date of Birth June 6, 1985).",
       "US Soccer — Becky Sauerbrunn official profile (DOB Jun 06 1985)", "https://www.ussoccer.com/players/s/becky-sauerbrunn"),
    ev("Identified as a woman via USWNT women's national-team career — three NWSL Defender of the Year awards, 200+ USWNT caps (US Soccer official; mysuite biodata).",
       "US Soccer — Becky Sauerbrunn official profile (3x NWSL Defender of the Year)", "https://www.ussoccer.com/players/s/becky-sauerbrunn"),
    [src("US Soccer — Becky Sauerbrunn official player profile (DOB Jun 06 1985)", "Website", "https://www.ussoccer.com/players/s/becky-sauerbrunn", "official"),
     src("ESPN — Becky Sauerbrunn player page (birthdate 6/6/1985)", "Website", "https://www.espn.com/soccer/player/bio/_/id/158780/becky-sauerbrunn", "other-trusted"),
     src("MySuite — Becky Sauerbrunn biodata (DOB June 6, 1985)", "Website", "https://mysuite.wild.com/trendingentertainment-wolf57/becky-sauerbrunn-partner/", "other-trusted")],
    [], "Two-time World Cup champion and 200+ cap USWNT defender (Portland Thorns) — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-170", "Julie Ertz (née Johnston)",
    ev("Born April 6, 1992 in Mesa, Arizona — age 34 in 2026 — per Wikipedia (born April 6, 1992), Kiddle replication, US Soccer official profile (Date of Birth Apr 06 1992) and Athlon Sports quick facts (Born: April 6, 1992).",
       "US Soccer — Julie Ertz official profile (DOB Apr 06 1992)", "https://www.ussoccer.com/players/e/julie-ertz"),
    ev("Identified as a woman via USWNT women's national-team career — two-time FIFA Women's World Cup champion (2015, 2019), twice named U.S. Soccer Female Player of the Year (US Soccer official/ebiographypost).",
       "US Soccer — Julie Ertz official profile ('a two-time Women’s World Cup Champion')", "https://www.ussoccer.com/players/e/julie-ertz"),
    [src("US Soccer — Julie Ertz official player profile (DOB Apr 06 1992)", "Website", "https://www.ussoccer.com/players/e/julie-ertz", "official"),
     src("Wikipedia — Julie Ertz (DOB 1992-04-06; née Johnston)", "Website", "https://en.wikipedia.org/wiki/Julie_Ertz", "other-trusted"),
     src("Athlon Sports — Julie Ertz fast facts (Born April 6, 1992; IG julieertz; Twitter @julieertz)", "Website", "https://athlonsports.com/soccer/julie-ertz-usnwt", "other-trusted"),
     src("Instagram — @julieertz (athlonsports displayed handle)", "Instagram", "https://www.instagram.com/julieertz/", "verified-platform"),
     src("X — @julieertz (athlonsports displayed handle)", "X", "https://x.com/julieertz", "verified-platform")],
    [], "Two-time World Cup champion (2015/2019) and 2x U.S. Soccer Female Player of the Year — objective athlete category. Handles via Athlon Sports quick-facts; counts not captured — UNKNOWN.",
    [acct("Instagram", "@julieertz", "https://www.instagram.com/julieertz/", "Handle via athlonsports.com quick-facts; count not captured."),
     acct("X", "@julieertz", "https://x.com/julieertz", "Handle via athlonsports.com quick-facts; count not captured.")]))

NEW.append(ent("W-2026-171", "Ali Krieger",
    ev("Born July 28, 1984 in Dumfries, Virginia — age 42 in 2026 — per Wikipedia (born July 28, 1984), Kiddle replication, ESPN structured birthdate 7/28/1984 and richathletes biodata.",
       "Wikipedia — Ali Krieger (born July 28, 1984)", "https://en.wikipedia.org/wiki/Ali_Krieger"),
    ev("Identified as a woman via USWNT women's national-team career — two FIFA Women's World Cup titles, 100+ caps (Wikipedia/Kiddle; 2015 record 540-minute shutout streak on defense).",
       "Wikipedia — Ali Krieger (2x FIFA Women's World Cup winner)", "https://en.wikipedia.org/wiki/Ali_Krieger"),
    [src("Wikipedia — Ali Krieger (DOB 1984-07-28; 2x World Cup winner)", "Website", "https://en.wikipedia.org/wiki/Ali_Krieger", "age-evidence"),
     src("ESPN — Ali Krieger player page (birthdate 7/28/1984)", "Website", "https://www.espn.com/soccer/player/bio/_/id/158777/ali-krieger", "other-trusted"),
     src("Rich Athletes — Ali Krieger bio (DOB 28 July 1984)", "Website", "https://richathletes.com/ali-krieger-bio-soccer-career-relationship-with-ashlyn-harris-other-facts/", "other-trusted")],
    [], "Two-time World Cup champion and 100+ cap USWNT defender ('The Warrior Princess') — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-172", "Ashlyn Harris",
    ev("Born October 19, 1985 in Satellite Beach, Florida — age 40 in 2026 — per FBref (Born: October 19, 1985), Wikipedia (born October 19, 1985), Kiddle replication and sportslib profile.",
       "FBref — Ashlyn Harris (born October 19, 1985)", "https://fbref.com/en/players/4c7ad183/Ashlyn-Harris"),
    ev("Identified as a woman via USWNT women's national-team goalkeeper career — FIFA Women's World Cup titles 2015 and 2019, UNC three NCAA titles (Wikipedia/FBref/Kiddle).",
       "Wikipedia — Ashlyn Harris (2015 & 2019 World Cup champion)", "https://en.wikipedia.org/wiki/Ashlyn_Harris"),
    [src("FBref — Ashlyn Harris (DOB 1985-10-19)", "Website", "https://fbref.com/en/players/4c7ad183/Ashlyn-Harris", "age-evidence"),
     src("Wikipedia — Ashlyn Harris (DOB 1985-10-19; World Cup medal record)", "Website", "https://en.wikipedia.org/wiki/Ashlyn_Harris", "other-trusted"),
     src("Kiddle — Ashlyn Harris (DOB October 19, 1985; career summary)", "Website", "https://kids.kiddle.co/Ashlyn_Harris", "other-trusted")],
    [], "Two-time World Cup-champion goalkeeper (196 UNC/USWNT career games documented) — objective athlete category. Birthplace Satellite Beach per Wikipedia/Kiddle vs Cocoa Beach per fbref — both captured, Wikipedia value recorded in evidence. No handle captured this pass — follower range UNKNOWN.", []))


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
