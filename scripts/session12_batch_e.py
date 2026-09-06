#!/usr/bin/env python3
"""Session 12 batch E (2026-09-06): 8 verified adds (W-2026-139..146).
NWSL/USWNT roster run: marriedbiography JSON-LD (DOB+gender+sameAs handles),
ussoccer.com/Wikipedia/ESPN cross-checks. Dup-guard protocol: all 8 names
grep-checked against catalog displayName before authoring (none present).
"""
import json
from pathlib import Path

CATALOG = Path("data/catalog.json")
CHECKED = "2026-09-06"

RANGES = [(1000,"Under 1K"),(5000,"1K–4.9K"),(10000,"5K–9.9K"),(25000,"10K–24.9K"),
          (50000,"25K–49.9K"),(100000,"50K–99.9K"),(250000,"100K–249.9K"),
          (500000,"250K–499.9K"),(1000000,"500K–999.9K"),(5000000,"1M–4.9M")]
def size_range(n):
    if n is None: return "FOLLOWER_RANGE_UNKNOWN"
    for limit, label in RANGES:
        if n < limit: return label
    return "5M+"

def account(platform, username, url, note):
    return {"platform": platform, "username": username, "profileUrl": url,
            "followerCountDisplay": "FOLLOWER_COUNT_UNKNOWN", "followerCountNumeric": None,
            "countType": "unknown", "checkedAt": CHECKED,
            "followerSizeRange": "FOLLOWER_RANGE_UNKNOWN", "sourceNote": note}

def largest(accounts):
    known = [a for a in accounts if a["followerCountNumeric"] is not None]
    if not known:
        return {"platform": None, "username": None, "display": None, "numeric": None,
                "sizeRange": "FOLLOWER_RANGE_UNKNOWN", "checkedAt": CHECKED}
    top = max(known, key=lambda a: a["followerCountNumeric"])
    return {"platform": top["platform"], "username": top["username"],
            "display": top["followerCountDisplay"], "numeric": top["followerCountNumeric"],
            "sizeRange": top["followerSizeRange"], "checkedAt": CHECKED}

def entry(rid, name, adult, gender, sources, flags, notes, accounts):
    big = largest(accounts)
    return {"id": rid, "displayName": name,
            "categories": ["Athlete", "Soccer", "Creator"],
            "legalAdultEvidence": adult, "genderEvidence": gender,
            "sources": sources, "verificationStatus": "verified",
            "lastReviewed": CHECKED, "flags": flags, "notes": notes,
            "socialAccounts": accounts, "largestPublicFollowing": big,
            "overallFollowerSizeRange": big["sizeRange"]}

def ev(summary, label, url):
    return {"summary": summary, "sourceLabel": label, "sourceUrl": url, "checkedAt": CHECKED}

def src(label, platform, url, rel):
    return {"label": label, "platform": platform, "url": url, "relationship": rel}

NEW = []

NEW.append(entry("W-2026-139", "Lynn Biyendolo (née Williams)",
    ev("Born May 21, 1993 in Fresno, California — age 33 in 2026 — per marriedbiography structured record (JSON-LD birthDate 1993-05-21), Wikipedia (born May 21, 1993 under both Lynn Williams and Lynn Biyendolo pages) and Gotham FC official bio (DATE OF BIRTH: May 21, 1993).",
       "Married Biography — Lynn Williams (birthDate 1993-05-21)", "https://marriedbiography.com/lynn-williams-biography/"),
    ev("Identified as a woman via marriedbiography structured data (JSON-LD 'gender: https://schema.org/Female') and USWNT/NWSL women's forward career — NWSL all-time leading scorer (Wikipedia/Gotham FC).",
       "Married Biography — Lynn Williams structured record (gender schema.org/Female)", "https://marriedbiography.com/lynn-williams-biography/"),
    [
        src("Married Biography — Lynn Williams (birthDate/gender Female JSON-LD; sameAs IG/X handles)", "Website", "https://marriedbiography.com/lynn-williams-biography/", "age-evidence"),
        src("Wikipedia — Lynn Biyendolo (DOB 1993-05-21; NWSL all-time leading scorer)", "Website", "https://en.wikipedia.org/wiki/Lynn_Biyendolo", "other-trusted"),
        src("Gotham FC — Lynn Williams official player page (DOB May 21, 1993)", "Website", "https://www.gothamfc.com/10-williams", "official"),
        src("Instagram — @lynnwilliams9 (marriedbiography structured sameAs)", "Instagram", "https://www.instagram.com/lynnwilliams9/", "verified-platform"),
        src("X — @lynnraenie (marriedbiography structured sameAs)", "X", "https://x.com/lynnraenie", "verified-platform"),
    ],
    [], "NWSL all-time leading scorer and USWNT forward — objective athlete category. Married name Biyendolo per Wikipedia redirect (birth name Lynn Raenie Williams). Handles via marriedbiography structured sameAs; counts not captured — UNKNOWN.",
    [account("Instagram", "@lynnwilliams9", "https://www.instagram.com/lynnwilliams9/",
             "Handle via marriedbiography.com structured sameAs; count not captured."),
     account("X", "@lynnraenie", "https://x.com/lynnraenie",
             "Handle via marriedbiography.com structured sameAs; count not captured.")]))

NEW.append(entry("W-2026-140", "Catarina Macario",
    ev("Born October 4, 1999 in São Luís, Brazil — age 26 in 2026 — per Wikipedia (born October 4, 1999), US Soccer official player profile (Date of Birth Oct 04 1999) and San Diego Wave FC official signing release ('Macario, 26 ... Date of Birth: Oct. 4, 1999'). ESPN structured birthDate 10/4/1999 matches.",
       "US Soccer — Catarina Macario official profile (DOB Oct 04 1999)", "https://www.ussoccer.com/players/m/catarina-macario"),
    ev("Identified as a woman via USWNT women's national-team and Chelsea FC Women / San Diego Wave FC career (US Soccer official profile; San Diego Wave acquisition release).",
       "US Soccer — Catarina Macario official profile (USWNT)", "https://www.ussoccer.com/players/m/catarina-macario"),
    [
        src("US Soccer — Catarina Macario official player profile (DOB Oct 4 1999)", "Website", "https://www.ussoccer.com/players/m/catarina-macario", "official"),
        src("San Diego Wave FC — Macario signing release (Age 26; DOB Oct. 4, 1999)", "Website", "https://sandiegowavefc.com/catarina-macario-signing-release/", "official"),
        src("Wikipedia — Catarina Macario (DOB 1999-10-04)", "Website", "https://en.wikipedia.org/wiki/Catarina_Macario", "other-trusted"),
    ],
    [], "USWNT forward, 2021 Mac Hermann Trophy winner and Stanford alum — objective athlete category. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-141", "Ashley Sanchez",
    ev("Born March 16, 1999 in Pasadena, California — age 27 in 2026 — per US Soccer official profile (Date of Birth Mar 16 1999), Wikipedia (born March 16, 1999), soccerdonna.de (Date of birth 16.03.1999) and ESPN structured birthDate 3/16/1999.",
       "US Soccer — Ashley Sanchez official profile (DOB Mar 16 1999)", "https://www.ussoccer.com/players/s/ashley-sanchez"),
    ev("Identified as a woman via USWNT women's national-team midfielder career — 2016 U.S. Soccer Young Female Player of the Year (US Soccer official), NC Courage/UCLA women's soccer track (Wikipedia/ESPN).",
       "US Soccer — Ashley Sanchez official profile (Young Female Player of the Year 2016)", "https://www.ussoccer.com/players/s/ashley-sanchez"),
    [
        src("US Soccer — Ashley Sanchez official player profile (DOB Mar 16 1999)", "Website", "https://www.ussoccer.com/players/s/ashley-sanchez", "official"),
        src("Wikipedia — Ashley Sanchez (DOB 1999-03-16)", "Website", "https://en.wikipedia.org/wiki/Ashley_Sanchez", "other-trusted"),
        src("ESPN — Ashley Sanchez player page (birthDate 3/16/1999 structured)", "Website", "https://www.espn.com/soccer/player/_/id/279297/ashley-sanchez", "other-trusted"),
    ],
    [], "USWNT attacking midfielder, 2021 NWSL champion and UCLA all-time assist leader — objective athlete category. No handle captured this pass — follower range UNKNOWN. (soccerdonna's non-English '16.03.1999' date style matches Wikipedia.)",
    []))

NEW.append(entry("W-2026-142", "Alyssa Thompson",
    ev("Born November 7, 2004 in Los Angeles, California — age 21 in 2026 — per Wikipedia (born November 7, 2004), US Soccer official profile (Date of Birth Nov 07 2004), ESPN structured birthDate 11/7/2004 and broadbiography (Birth Date November 7, 2004).",
       "US Soccer — Alyssa Thompson official profile (DOB Nov 07 2004)", "https://www.ussoccer.com/players/t/alyssa-thompson"),
    ev("Identified as a woman via USWNT women's national-team career (US Soccer official profile; youngest-teen debut milestones) and Chelsea FC Women forward role (ESPN/Grokipedia career record).",
       "US Soccer — Alyssa Thompson official profile (USWNT debut record)", "https://www.ussoccer.com/players/t/alyssa-thompson"),
    [
        src("US Soccer — Alyssa Thompson official player profile (DOB Nov 07 2004)", "Website", "https://www.ussoccer.com/players/t/alyssa-thompson", "official"),
        src("Wikipedia — Alyssa Thompson (DOB 2004-11-07)", "Website", "https://en.wikipedia.org/wiki/Alyssa_Thompson", "other-trusted"),
        src("ESPN — Alyssa Thompson player page (birthDate 11/7/2004 structured)", "Website", "https://www.espn.com/soccer/player/_/id/351658/alyssa-thompson", "other-trusted"),
    ],
    [], "2023 NWSL first-overall pick (at 18) and USWNT forward now with Chelsea — objective athlete category; verified 21 years old. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-143", "Jaedyn Shaw",
    ev("Born November 20, 2004 in Frisco, Texas — age 21 in 2026 — per US Soccer official profile (Date of Birth Nov 20 2004), Red Bull athlete profile (Date of birth: November 20, 2004 / '20 November 2004' on int-en) and Wikipedia (born November 20, 2004).",
       "US Soccer — Jaedyn Shaw official profile (DOB Nov 20 2004)", "https://www.ussoccer.com/players/s/jaedyn-shaw"),
    ev("Identified as a woman via USWNT women's national-team forward career — 2022 U.S. Soccer Young Female Player of the Year (san diegowavefc.com signing release; US Soccer profile).",
       "San Diego Wave FC — Jaedyn Shaw contract release ('2022 U.S. Soccer Young Female Player of the Year')", "https://sandiegowavefc.com/san-diego-wave-fc-signs-jaedyn-shaw-to-new-contract/"),
    [
        src("US Soccer — Jaedyn Shaw official player profile (DOB Nov 20 2004)", "Website", "https://www.ussoccer.com/players/s/jaedyn-shaw", "official"),
        src("Red Bull — Jaedyn Shaw athlete profile (Date of birth November 20, 2004)", "Website", "https://www.redbull.com/us-en/athlete/jaedyn-shaw", "age-evidence"),
        src("Wikipedia — Jaedyn Shaw (DOB 2004-11-20)", "Website", "https://en.wikipedia.org/wiki/Jaedyn_Shaw", "other-trusted"),
    ],
    ["CONFLICTING_INFORMATION"], "USWNT forward and Gotham FC attacking midfielder — objective athlete category; verified 21 years old. Flag: San Diego Wave's 2023 signing release printed 'Date of Birth: Oct. 20, 2004' — an outlier vs US Soccer + Red Bull + Wikipedia (all Nov 20, 2004); majority/official value recorded, minor logged via flag. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-144", "Midge Purce",
    ev("Born September 18, 1995 in Silver Spring, Maryland — age 30 in 2026 — per US Soccer official profile (Date of Birth Sep 18 1995), sportslib profile (September 18, 1995), Kiddle/Wikiwand Wikipedia replication (born September 18, 1995) and ESPN structured birthDate 9/18/1995.",
       "US Soccer — Midge Purce official profile (DOB Sep 18 1995)", "https://www.ussoccer.com/players/p/midge-purce"),
    ev("Identified as a woman via USWNT women's national-team forward career and Gotham FC — MVP of Gotham's 2023 NWSL Championship (Wikiwand/Wikipedia).",
       "US Soccer — Midge Purce official profile (USWNT)", "https://www.ussoccer.com/players/p/midge-purce"),
    [
        src("US Soccer — Midge Purce official player profile (DOB Sep 18 1995)", "Website", "https://www.ussoccer.com/players/p/midge-purce", "official"),
        src("Wikiwand — Midge Purce (DOB 1995-09-18; 2023 NWSL Championship MVP)", "Website", "https://www.wikiwand.com/en/articles/Midge_Purce", "other-trusted"),
        src("ESPN — Midge Purce player page (birthDate 9/18/1995 structured)", "Website", "https://www.espn.com/soccer/player/_/id/226566/midge-purce", "other-trusted"),
    ],
    [], "2023 NWSL Championship MVP and USWNT forward (full name Margaret Melinda Williams-Purce) — objective athlete category. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-145", "Andi Sullivan",
    ev("Born December 20, 1995 in Honolulu, Hawaii — age 30 in 2026 — per Wikiwand/Wikipedia (born December 20, 1995), baike replication (December 20, 1995) and ESPN structured birthDate 12/20/1995.",
       "Wikiwand — Andi Sullivan (born December 20, 1995)", "https://www.wikiwand.com/en/articles/Andi_Sullivan"),
    ev("Identified as a woman via USWNT women's national-team midfielder career — 2023 FIFA Women's World Cup squad (Wikipedia/baike) and Washington Spirit 2021 NWSL championship.",
       "Wikiwand — Andi Sullivan (USWNT/Washington Spirit career)", "https://www.wikiwand.com/en/articles/Andi_Sullivan"),
    [
        src("Wikiwand — Andi Sullivan (DOB 1995-12-20)", "Website", "https://www.wikiwand.com/en/articles/Andi_Sullivan", "age-evidence"),
        src("ESPN — Andi Sullivan player page (birthDate 12/20/1995 structured)", "Website", "https://www.espn.com/soccer/player/bio/_/id/212209/andi-sullivan", "other-trusted"),
        src("Baike — Andi Sullivan (Date of Birth December 20, 1995)", "Website", "https://baike.baidu.com/en/item/Andi%20Sullivan/1773414", "other-trusted"),
    ],
    [], "2021 NWSL champion and former USWNT midfielder (Stanford All-American) — objective athlete category. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-146", "Casey Murphy",
    ev("Born April 25, 1996 in Bridgewater, New Jersey — age 30 in 2026 — per US Soccer official profile (Date of Birth Apr 25 1996), ESPN structured birthDate 4/25/1996 and NJ Sports profile ('Casey Grace Murphy was born April 25, 1996 in Bridgewater, NJ').",
       "US Soccer — Casey Murphy official profile (DOB Apr 25 1996)", "https://www.ussoccer.com/players/m/casey-murphy"),
    ev("Identified as a woman via USWNT women's national-team goalkeeper career — 2024 Olympic gold medalist (US Soccer official profile heading) and tallest goalkeeper in USWNT history.",
       "US Soccer — Casey Murphy official profile ('2024 OLYMPIC GOLD MEDALIST')", "https://www.ussoccer.com/players/m/casey-murphy"),
    [
        src("US Soccer — Casey Murphy official player profile (DOB Apr 25 1996; 2024 Olympic gold)", "Website", "https://www.ussoccer.com/players/m/casey-murphy", "official"),
        src("ESPN — Casey Murphy player page (birthDate 4/25/1996 structured)", "Website", "https://www.espn.com/soccer/player/_/id/209771/Casey-Murphy", "other-trusted"),
        src("NJ Sports — Casey Murphy profile ('born April 25, 1996 in Bridgewater')", "Website", "https://njsports.com/casey-murphy/", "other-trusted"),
    ],
    [], "2024 Olympic gold-medalist goalkeeper (North Carolina Courage; Montpellier D1 Féminine top GK) — objective athlete category. Note: US Soccer page JSON-LD inline birthDate shows '1996-04-23' — a two-day serialized-field artifact vs its own displayed 'Apr 25 1996' (matching ESPN + njsports); displayed/majority value recorded. No handle captured this pass — follower range UNKNOWN.",
    []))


def build():
    data = json.loads(CATALOG.read_text())
    entries = data["entries"]
    existing_ids = {e["id"] for e in entries}
    existing_names = {e["displayName"].lower() for e in entries}
    existing_urls = {s["url"] for e in entries for s in e["sources"]}
    for rec in NEW:
        assert rec["id"] not in existing_ids, f"dup id {rec['id']}"
        assert rec["displayName"].lower() not in existing_names, f"dup name {rec['displayName']}"
        overlap = {s["url"] for s in rec["sources"]} & existing_urls
        assert not overlap, f"dup urls {overlap}"
    entries.extend(NEW)

    irr_ids = {i["id"] for i in data["irregularities"]}
    if "IRR-2026-09-06-015" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-015",
            "severity": "resolved-mild",
            "summary": "Session-12 batch-E: two DOB source conflicts resolved to majority/official values.",
            "detail": (
                "(1) Jaedyn Shaw — sandiegowavefc.com 2023 signing release printed Oct. 20, 2004; US Soccer + Red Bull + Wikipedia all say Nov. 20, 2004 → recorded Nov 20, 2004, entry flagged CONFLICTING_INFORMATION. "
                "(2) Casey Murphy — US Soccer inline JSON-LD birthDate reads 1996-04-23 while the same page displays 'Date of Birth Apr 25 1996'; ESPN and njsports corroborate Apr 25 → recorded 1996-04-25, artifact noted in entry notes (same class of machine-field artifact as Sophia Smith's 08-09-vs-08-10 from batch A)."
            ),
            "reviewStatus": "no-action-required",
        })
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)}) irr={len(data['irregularities'])}")

if __name__ == "__main__":
    build()
