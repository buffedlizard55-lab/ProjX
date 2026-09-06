#!/usr/bin/env python3
"""Session 12 batch M (2026-09-06): 4 verified adds (W-2026-181..184).
WTA women's tennis wave: ESPN tennis pages, leaderbiography (Pegula IG),
tennisworldusa/tennis-infinity, Wikipedia. Dup-guard pre-checked.
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
    return {"id": i, "displayName": n, "categories": ["Athlete", "Tennis", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-181", "Ons Jabeur",
    ev("Born August 28, 1994 in Ksar Hellal, Tunisia — age 32 in 2026 — per Wikipedia (born 28 August 1994), ESPN tennis profile (Birth Date August 28, 1994), tennisworldusa (born in Ksar Hellal on August 28, 1994) and her personal bio site ons-jabeur.com (Date of birth 28 August 1994).",
       "ESPN — Ons Jabeur tennis profile (Birth Date August 28, 1994)", "https://www.espn.com/tennis/player/_/id/1803/ons-jabeur"),
    ev("Identified as a woman via WTA women's singles career — three-time major finalist, highest-ranked African/Arab player in tennis history (Wikipedia/tennisworldusa); 2019 Arab Woman of the Year award.",
       "TennisWorldUSA — Ons Jabeur bio (2019 Arab Woman of the Year)", "https://www.tennisworldusa.org/tennis-player/350/ons-jabeur/"),
    [src("ESPN — Ons Jabeur profile (DOB Aug 28, 1994)", "Website", "https://www.espn.com/tennis/player/_/id/1803/ons-jabeur", "age-evidence"),
     src("Wikipedia — Ons Jabeur (DOB 1994-08-28; career-high No. 2)", "Website", "https://en.wikipedia.org/wiki/Ons_Jabeur", "other-trusted"),
     src("ons-jabeur.com — official bio site (Date of birth 28 August 1994)", "Website", "https://ons-jabeur.com/", "official")],
    [], "Three-time Grand Slam finalist and career-high WTA No. 2 ('Minister of Happiness') — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-182", "Markéta Vondroušová",
    ev("Born June 28, 1999 in Sokolov, Czech Republic — age 27 in 2026 — per tennismajors (born on June 28, 1999 in Sokolov), thecityceleb structured record (birthDate 1999-06-28), grokipedia (born 28 June 1999) and kiddle replication.",
       "Tennis Majors — Markéta Vondroušová profile ('born on June 28, 1999 in Sokolov')", "https://www.tennismajors.com/wta-tour-news/czech-left-handed-roland-garros-everything-you-always-wanted-to-know-about-marketa-vondrousova-but-never-had-time-to-find-out-696380.html"),
    ev("Identified as a woman via thecityceleb structured data ('gender: Female' JSON-LD) and WTA women's singles career — 2023 Wimbledon champion, first unseeded women's champion in the Open Era (grokipedia/tennismajors).",
       "TheCityCeleb — Markéta Vondroušová ('gender: Female' JSON-LD; Wimbledon champion)", "https://www.thecityceleb.com/biography/public-figure/sportsperson/marketa-vondrousova-biography-age-awards-parents-siblings-net-worth-height-boyfriend-team/"),
    [src("Tennis Majors — Markéta Vondroušová (DOB June 28, 1999)", "Website", "https://www.tennismajors.com/wta-tour-news/czech-left-handed-roland-garros-everything-you-always-wanted-to-know-about-marketa-vondrousova-but-never-had-time-to-find-out-696380.html", "age-evidence"),
     src("TheCityCeleb — Markéta Vondroušová (birthDate 1999-06-28; gender Female JSON-LD)", "Website", "https://www.thecityceleb.com/biography/public-figure/sportsperson/marketa-vondrousova-biography-age-awards-parents-siblings-net-worth-height-boyfriend-team/", "gender-evidence"),
     src("Wikipedia mirror Kiddle — Markéta Vondroušová (DOB 1999-06-28)", "Website", "https://kids.kiddle.co/Mark%C3%A9ta_Vondrou%C5%A1ov%C3%A1", "other-trusted")],
    [], "2023 Wimbledon champion and first unseeded women's singles champion (2020 Olympic silver) — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-183", "Jessica Pegula",
    ev("Born February 24, 1994 in Buffalo, New York — age 32 in 2026 — per ESPN tennis profile (Birth Date February 24, 1994), leaderbiography (Date of Birth February 24, 1994), tennisuptodate (born February 24, 1994) and grokipedia.",
       "ESPN — Jessica Pegula tennis profile (Birth Date February 24, 1994)", "https://www.espn.com/tennis/player/photos/_/id/2113/jessica-pegula"),
    ev("Identified as a woman via WTA women's career — career-high No. 3 in singles, world No. 1 in doubles (with Coco Gauff, 2023), per leaderbiography/WTA record.",
       "LeaderBiography — Jessica Pegula bio (No. 1 doubles record with Coco Gauff)", "https://leaderbiography.com/jessica-pegula/"),
    [src("ESPN — Jessica Pegula profile (DOB Feb 24, 1994)", "Website", "https://www.espn.com/tennis/player/photos/_/id/2113/jessica-pegula", "age-evidence"),
     src("LeaderBiography — Jessica Pegula bio (DOB February 24, 1994; Instagram @jpegula)", "Website", "https://leaderbiography.com/jessica-pegula/", "other-trusted"),
     src("Grokipedia — Jessica Pegula (born February 24, 1994; 9 WTA singles titles)", "Website", "https://grokipedia.com/page/Jessica_Pegula", "other-trusted"),
     src("Instagram — @jpegula (leaderbiography socials table)", "Instagram", "https://www.instagram.com/jpegula/", "verified-platform")],
    [], "Career-high WTA No. 3 in singles and former world No. 1 in doubles; Buffalo Bills/Sabres family ownership context noted — objective athlete category. IG handle via leaderbiography; count not captured — UNKNOWN.",
    [acct("Instagram", "@jpegula", "https://www.instagram.com/jpegula/", "Handle via leaderbiography.com socials table; count not captured.")]))

NEW.append(ent("W-2026-184", "Madison Keys",
    ev("Born February 17, 1995 in Rock Island, Illinois — age 31 in 2026 — per ESPN tennis profile (Birth Date February 17, 1995), tennis-infinity (Date of Birth: 17 February 1995), biographyadda (born on February 17, 1995) and mabumbe.",
       "ESPN — Madison Keys tennis profile (Birth Date February 17, 1995)", "https://www.espn.com/tennis/player/_/id/1556/madison-keys"),
    ev("Identified as a woman via WTA women's singles career — 2025 Australian Open champion (biographyadda; 2017 US Open finalist), career-high WTA No. 5/7 documented.",
       "BiographyAdda — Madison Keys biography (2025 Australian Open champion)", "https://biographyadda.com/madison-keys-biography/"),
    [src("ESPN — Madison Keys profile (DOB Feb 17, 1995)", "Website", "https://www.espn.com/tennis/player/_/id/1556/madison-keys", "age-evidence"),
     src("BiographyAdda — Madison Keys (DOB February 17, 1995; 2025 AO champion)", "Website", "https://biographyadda.com/madison-keys-biography/", "other-trusted"),
     src("Tennis Infinity — Madison Keys (Date of Birth 17 February 1995)", "Website", "https://tennis-infinity.com/madison-keys", "other-trusted")],
    [], "2025 Australian Open champion and 11x WTA singles title winner — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))


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
