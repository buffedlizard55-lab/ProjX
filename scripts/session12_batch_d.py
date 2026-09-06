#!/usr/bin/env python3
"""Session 12 batch D (2026-09-06): 6 verified adds (W-2026-133..138); Cassey Ho excluded as pre-existing mid-build.
Wave 4 pipeline: volleyball (lovb.com + volleybox JSON-LD sameAs + VNL official),
swimming (SwimSwam/playerswiki), fitness creators (Wikipedia/thefamouspeople/
stats approximations recorded as rounded), soccer (Britannica), surfing
(NC Management official handles), climbing (Red Bull structured + official site
sameAs). Dup-guard excluded Regan Smith/Pamela Reif/Iga Świątek (pre-existing).
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

def account(platform, username, url, display, numeric, count_type, note):
    return {"platform": platform, "username": username, "profileUrl": url,
            "followerCountDisplay": display, "followerCountNumeric": numeric,
            "countType": count_type, "checkedAt": CHECKED,
            "followerSizeRange": size_range(numeric), "sourceNote": note}

def largest(accounts):
    known = [a for a in accounts if a["followerCountNumeric"] is not None]
    if not known:
        return {"platform": None, "username": None, "display": None, "numeric": None,
                "sizeRange": "FOLLOWER_RANGE_UNKNOWN", "checkedAt": CHECKED}
    top = max(known, key=lambda a: a["followerCountNumeric"])
    return {"platform": top["platform"], "username": top["username"],
            "display": top["followerCountDisplay"], "numeric": top["followerCountNumeric"],
            "sizeRange": top["followerSizeRange"], "checkedAt": CHECKED}

def entry(rid, name, cats, adult, gender, sources, flags, notes, accounts):
    big = largest(accounts)
    return {"id": rid, "displayName": name, "categories": cats,
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

NEW.append(entry("W-2026-133", "Jordan Larson",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born October 16, 1986 in Fremont, Nebraska — age 39 in 2026 — per PeoplePill structured record ('Birth 16 October 1986'), Wikipedia (born October 16, 1986) and Alchetron replication.",
       "PeoplePill — Jordan Larson (Birth 16 October 1986)", "https://peoplepill.com/people/jordan-larson"),
    ev("Identified as a woman via PeoplePill structured data ('Gender: female') and US women's national team volleyball career — four Olympic medals including Tokyo 2020 gold MVP (peoplepill/Wikipedia/LOVB bio).",
       "PeoplePill — Jordan Larson structured record ('Gender: female')", "https://peoplepill.com/people/jordan-larson"),
    [
        src("PeoplePill — Jordan Larson (DOB 1986-10-16; Gender: female)", "Website", "https://peoplepill.com/people/jordan-larson", "age-evidence"),
        src("Wikipedia — Jordan Larson (DOB 1986-10-16; 4x Olympic medalist)", "Website", "https://en.wikipedia.org/wiki/Jordan_Larson", "other-trusted"),
        src("LOVB — Jordan Larson athlete profile (four-time Olympian bio)", "Website", "https://www.lovb.com/teams/lovb-nebraska-volleyball/athletes/jordan-larson", "official"),
    ],
    [], "Four-time Olympic medalist and Tokyo 2020 indoor volleyball MVP — objective athlete category. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-134", "Jordan Thompson",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born May 5, 1997 — age 29 in 2026 — per volleyballworld.com official VNL player bio (Birth date 05/05/1997, Age 29) and volleybox structured JSON-LD birthDate 1997-05-05.",
       "Volleyball World — Jordan Thompson official VNL player bio (birth date 05/05/1997)", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/172978"),
    ev("Identified as a woman via volleybox structured data ('gender: Female' JSON-LD) and US women's national-team opposite-hitter career — 2020 Olympic gold (volleybox/LOVB).",
       "Women.volleybox — Jordan Thompson player data ('gender: Female')", "https://women.volleybox.net/jordan-thompson-p23201"),
    [
        src("Volleyball World — Jordan Thompson VNL official bio (DOB 1997-05-05)", "Website", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/172978", "official"),
        src("Women.volleybox — Jordan Thompson (birthDate/gender Female; sameAs IG/X @jtomm19)", "Website", "https://women.volleybox.net/jordan-thompson-p23201", "age-evidence"),
        src("LOVB — Jordan Thompson athlete profile (2020 Olympic gold bio)", "Website", "https://www.lovb.com/teams/lovb-houston-volleyball/athletes/jordan-thompson", "official"),
        src("Instagram — @jtomm19 (volleybox structured sameAs)", "Instagram", "https://www.instagram.com/jtomm19/", "verified-platform"),
        src("X — @jtomm19 (volleybox structured sameAs)", "X", "https://x.com/jtomm19", "verified-platform"),
    ],
    [], "2020 Olympic gold and 2024 Olympic silver opposite hitter (Cincinnati kills leader) — objective athlete category. Handles via volleybox structured sameAs; counts not captured — UNKNOWN.",
    [account("Instagram", "@jtomm19", "https://www.instagram.com/jtomm19/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via women.volleybox.net structured sameAs; count not captured."),
     account("X", "@jtomm19", "https://x.com/jtomm19", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via women.volleybox.net structured sameAs; count not captured.")]))

NEW.append(entry("W-2026-135", "Simone Manuel",
    ["Athlete", "Swimming", "Creator"],
    ev("Born August 2, 1996 in Sugar Land, Texas — age 30 in 2026 — per PlayersWiki (born August 2, 1996), BarnesLaw bio replication and BioNewsly (Date of Birth August 2, 1996).",
       "PlayersWiki — Simone Manuel (born August 2, 1996)", "https://playerswiki.com/simone-manuel"),
    ev("Identified as a woman via women's Olympic swimming career — 'first African American woman to win an individual gold medal in Olympic swimming' (Women's Health/PlayersWiki).",
       "Women's Health — Who Is Simone Manuel (woman's swimming profile)", "https://www.womenshealthmag.com/fitness/a37115304/who-is-simone-manuel-olympics-swimming-usa/"),
    [
        src("PlayersWiki — Simone Manuel (DOB 1996-08-02; IG 142k / X 114k counts)", "Website", "https://playerswiki.com/simone-manuel", "age-evidence"),
        src("Women's Health — Simone Manuel Olympic profile", "Website", "https://www.womenshealthmag.com/fitness/a37115304/who-is-simone-manuel-olympics-swimming-usa/", "other-trusted"),
        src("SwimSwam — Simone Manuel bio (two-time Olympic champion record)", "Website", "https://swimswam.com/bio/simone-manuel/", "other-trusted"),
    ],
    [], "Two-time Olympic champion (100m freestyle, medley relay 2016) — objective athlete category. Counts are PlayersWiki's stated IG 142k/Twitter 114k (December-2018 snapshot; recorded verbatim, dated). Handle values were not shown on that page — URLs omitted per handle-evidence rule.",
    []))

NEW.append(entry("W-2026-136", "Sam Kerr",
    ["Athlete", "Soccer", "Creator"],
    ev("Born September 10, 1993 in Fremantle, Western Australia — age 33 in 2026 — per Britannica (born September 10, 1993), Wikiquote bio (born 10 September 1993) and HotSoccerGirls quick-facts (Date of Birth 10 September 1993).",
       "Britannica — Sam Kerr (born September 10, 1993)", "https://www.britannica.com/biography/Sam-Kerr"),
    ev("Identified as a woman via Matildas/Chelsea women's football career — captain of the Australian women's national team and 'the only female football player to have won the Golden Boot in three different leagues' (Wikiquote/Britannica).",
       "Britannica — Sam Kerr (Matildas captain, women's national team)", "https://www.britannica.com/biography/Sam-Kerr"),
    [
        src("Britannica — Sam Kerr (DOB 1993-09-10; Golden Boot record)", "Website", "https://www.britannica.com/biography/Sam-Kerr", "age-evidence"),
        src("Wikiquote — Sam Kerr bio (born 10 September 1993; NWSL scoring record)", "Website", "https://en.wikiquote.org/wiki/Sam_Kerr", "other-trusted"),
        src("HotSoccerGirls — Sam Kerr profile (DOB 1993-09-10; socials list)", "Website", "https://www.hotsoccergirls.com/sam-kerr", "other-trusted"),
        src("Instagram — @samanthakerr20 (hotsoccergirls socials list)", "Instagram", "https://www.instagram.com/samanthakerr20/", "verified-platform"),
        src("X — @samkerr1 (hotsoccergirls socials list)", "X", "https://x.com/samkerr1", "verified-platform"),
    ],
    [], "NWSL and WSL all-time-scoring striker and Matildas captain — objective athlete category. Handles via HotSoccerGirls social-accounts list; counts not captured — UNKNOWN.",
    [account("Instagram", "@samanthakerr20", "https://www.instagram.com/samanthakerr20/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via hotsoccergirls.com social-accounts list; count not captured."),
     account("X", "@samkerr1", "https://x.com/samkerr1", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via hotsoccergirls.com social-accounts list; count not captured.")]))

NEW.append(entry("W-2026-137", "Stephanie Gilmore",
    ["Athlete", "Surfing", "Creator"],
    ev("Born January 29, 1988 in Murwillumbah, NSW, Australia — age 38 in 2026 — per Wikipedia (born 29 January 1988), NextBiography (born January 29, 1988, age 38 as of 2026) and FamousFix.",
       "Wikipedia — Stephanie Gilmore (born 29 January 1988)", "https://en.wikipedia.org/wiki/Stephanie_Gilmore"),
    ev("Identified as a woman via women's WSL career — eight-time world champion, 'the most decorated female surfer in world championship history' (NextBiography/Wikipedia).",
       "NextBiography — Stephanie Gilmore (women's surfing titles count)", "https://www.nextbiography.com/stephanie-gilmore/"),
    [
        src("Wikipedia — Stephanie Gilmore (DOB 1988-01-29; 8x world champion)", "Website", "https://en.wikipedia.org/wiki/Stephanie_Gilmore", "age-evidence"),
        src("NextBiography — Stephanie Gilmore bio (DOB January 29, 1988)", "Website", "https://www.nextbiography.com/stephanie-gilmore/", "other-trusted"),
        src("NC Management — Stephanie Gilmore client profile (official handles @stephaniegilmore + @Steph_gilmore)", "Website", "https://ncmanagement.com.au/clients/stephanie-gilmore/", "official"),
        src("Instagram — @stephaniegilmore (NC Management 'FOLLOW STEPHANIE')", "Instagram", "https://www.instagram.com/stephaniegilmore/", "verified-platform"),
        src("X — @Steph_gilmore (NC Management 'FOLLOW STEPHANIE')", "X", "https://x.com/Steph_gilmore", "verified-platform"),
    ],
    [], "Eight-time WSL women's world champion — objective athlete category. Handles via her official management's client page; counts not captured — UNKNOWN.",
    [account("Instagram", "@stephaniegilmore", "https://www.instagram.com/stephaniegilmore/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via NC Management official client profile; count not captured."),
     account("X", "@Steph_gilmore", "https://x.com/Steph_gilmore", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via NC Management official client profile; count not captured.")]))

NEW.append(entry("W-2026-138", "Janja Garnbret",
    ["Athlete", "Climbing", "Creator"],
    ev("Born March 12, 1999 in Slovenj Gradec, Slovenia — age 27 in 2026 — per Red Bull athlete profile (structured birthDate 1999-03-12), her official website (Date of Birth 12.03.1999) and Wikiwand/Wikipedia (born 12 March 1999, age 27).",
       "Red Bull — Janja Garnbret athlete profile (birthDate 1999-03-12)", "https://www.redbull.com/ca-en/athlete/janja-garnbret-climbing"),
    ev("Identified as a woman via Red Bull structured data ('gender: female') and women's competition climbing career — two-time Olympic gold medalist (Tokyo 2020, Paris 2024).",
       "Red Bull — Janja Garnbret profile ('gender: female')", "https://www.redbull.com/ca-en/athlete/janja-garnbret-climbing"),
    [
        src("Red Bull — Janja Garnbret (DOB 1999-03-12; gender female; 2x Olympic gold)", "Website", "https://www.redbull.com/ca-en/athlete/janja-garnbret-climbing", "age-evidence"),
        src("janja-garnbret.com — official site (DOB 12.03.1999; sameAs IG janja_garnbret)", "Website", "https://janja-garnbret.com/", "official"),
        src("Wikiwand — Janja Garnbret (born 12 March 1999; 10x world champion)", "Website", "https://wikiwand.com/en/articles/Janja_Garnbret", "other-trusted"),
        src("Instagram — @janja_garnbret (official site structured sameAs)", "Instagram", "https://www.instagram.com/janja_garnbret/", "verified-platform"),
        src("Facebook — garnbretjanja (official site sameAs)", "Facebook", "https://www.facebook.com/garnbretjanja", "verified-platform"),
    ],
    [], "Two-time Olympic sport-climbing gold medalist and most-decorated competition climber — objective athlete category. Handles via her official website's structured sameAs records; counts not captured — UNKNOWN.",
    [account("Instagram", "@janja_garnbret", "https://www.instagram.com/janja_garnbret/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via janja-garnbret.com structured sameAs; count not captured."),
     account("Facebook", "garnbretjanja", "https://www.facebook.com/garnbretjanja", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via janja-garnbret.com structured sameAs; count not captured.")]))


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
    if "IRR-2026-09-06-014" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-014",
            "severity": "needs-review",
            "summary": "Session-12 batch-D flags: thirds-party stated counts recorded verbatim; pre-existing duplicate catches.",
            "detail": (
                "(1) Simone Manuel IG 142k/X 114k are PlayersWiki-stated counts from a December-2018 page — recorded verbatim + dated; handles were not shown on that page so no account objects were created. "
                "(2) Cassey Ho was re-verified this wave but excluded — an entry already exists under displayName 'Cassey Ho (Blogilates)' (dup-guard caught). "
                "(3) Other re-verified-but-pre-existing catches: Regan Smith (W-2026-078), Pamela Reif (W-2026-013), Iga Świątek (W-2026-093)."
            ),
            "reviewStatus": "requires-owner-review",
        })
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)}) irr={len(data['irregularities'])}")

if __name__ == "__main__":
    build()
