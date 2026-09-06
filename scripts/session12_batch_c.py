#!/usr/bin/env python3
"""Session 12 batch C (2026-09-06): 9 verified adds (W-2026-124..132).
Wave 3 pipeline: WWE women's champions (ESPN profile, Britannica, IMDb DOBs,
leaderbiography structured JSON-LD gender/birthDate/sameAs handles) + UFC
women's champions (Wikiwand + reference stats + tuko Gender: Female) + alpine
skiing (Biography.com/Wikipedia). Dup-guard excluded Ledecky/Kim/Rodman
(pre-existing W-2026-006/007/095).
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

def ig(user, note, display="FOLLOWER_COUNT_UNKNOWN", numeric=None, ctype="unknown"):
    return account("Instagram", user, f"https://www.instagram.com/{user.strip('@')}/", display, numeric, ctype, note)

def xacc(user, note, display="FOLLOWER_COUNT_UNKNOWN", numeric=None, ctype="unknown"):
    return account("X", user, f"https://x.com/{user.strip('@')}", display, numeric, ctype, note)

NEW = []

NEW.append(entry("W-2026-124", "Rhea Ripley",
    ["Athlete", "Wrestling", "Creator"],
    ev("Born October 11, 1996 in Adelaide, Australia — age 29 in 2026 — per Britannica (born October 11, 1996), ProWrestling Fandom and LeaderBiography structured JSON-LD (birthDate 1996-10-11).",
       "Britannica — Rhea Ripley (born October 11, 1996)", "https://www.britannica.com/biography/Rhea-Ripley"),
    ev("Identified as a woman via LeaderBiography structured data ('gender: Female') and WWE women's championship career — 2023 Women's Royal Rumble winner and Women's World Champion (Britannica/RingsideNews).",
       "LeaderBiography — Rhea Ripley structured record ('gender: Female')", "https://leaderbiography.com/rhea-ripley/"),
    [
        src("Britannica — Rhea Ripley (DOB 1996-10-11; WWE career)", "Website", "https://www.britannica.com/biography/Rhea-Ripley", "age-evidence"),
        src("LeaderBiography — Rhea Ripley (DOB 1996-10-11; sameAs IG rhearipley_wwe + X RheaRipley_WWE)", "Website", "https://leaderbiography.com/rhea-ripley/", "other-trusted"),
        src("RingsideNews — Rhea Ripley profile (birthDate + sameAs condensed)", "Website", "https://www.ringsidenews.com/rhea-ripley/", "other-trusted"),
        src("Instagram — @rhearipley_wwe (leaderbiography + ringsidenews sameAs)", "Instagram", "https://www.instagram.com/rhearipley_wwe/", "verified-platform"),
        src("X — @RheaRipley_WWE (leaderbiography + ringsidenews sameAs)", "X", "https://x.com/RheaRipley_WWE", "verified-platform"),
    ],
    [], "2023 Women's Royal Rumble winner (from #1) and multi-time WWE women's world champion — objective athlete category. Handles via two independent structured sameAs records; counts not captured — UNKNOWN.",
    [ig("@rhearipley_wwe", "Handle via LeaderBiography + RingsideNews structured sameAs; count not captured."),
     xacc("@RheaRipley_WWE", "Handle via LeaderBiography + RingsideNews structured sameAs; count not captured.")]))

NEW.append(entry("W-2026-125", "Bianca Belair",
    ["Athlete", "Wrestling", "Creator"],
    ev("Born April 9, 1989 in Knoxville, Tennessee — age 37 in 2026 — per ESPN WWE profile ('D.O.B.: April 9, 1989'), ITRWrestling bio, LeaderBiography and Topps Ripped (Birth Date April 9, 1989, Age 37).",
       "ESPN — Bianca Belair WWE profile (D.O.B. April 9, 1989)", "https://www.espn.com/wwe/story/_/id/29125761/wwe-profile-page-bianca-belair"),
    ev("Identified as a woman via WWE women's championship career — 'the EST of WWE… one of the most accomplished female wrestlers in WWE history' (TheSportster) and Raw/SmackDown women's titles (ESPN).",
       "TheSportster — Bianca Belair profile (women's championship career)", "https://www.thesportster.com/tag/bianca-belair/"),
    [
        src("ESPN — Bianca Belair profile (DOB 1989-04-09)", "Website", "https://www.espn.com/wwe/story/_/id/29125761/wwe-profile-page-bianca-belair", "age-evidence"),
        src("ITRWrestling — Bianca Belair 2026 bio (born April 9, 1989)", "Website", "https://itrwrestling.com/bio/bianca-belair/", "other-trusted"),
        src("LeaderBiography — Bianca Belair (DOB 1989-04-09; socials @biancabelairwwe + @BiancaBelairWWE)", "Website", "https://leaderbiography.com/bianca-belair/", "other-trusted"),
        src("Instagram — @biancabelairwwe (thesportster + leaderbiography)", "Instagram", "https://www.instagram.com/biancabelairwwe/", "verified-platform"),
        src("X — @BiancaBelairWWE (thesportster + leaderbiography)", "X", "https://x.com/BiancaBelairWWE", "verified-platform"),
    ],
    [], "2021 Women's Royal Rumble winner and record-setting 420-day Raw Women's Champion — objective athlete category. Handles via two independent profile sources; counts not captured — UNKNOWN.",
    [ig("@biancabelairwwe", "Handle via TheSportster profile sidebar and LeaderBiography socials table; count not captured."),
     xacc("@BiancaBelairWWE", "Handle via TheSportster profile sidebar and LeaderBiography socials table; count not captured.")]))

NEW.append(entry("W-2026-126", "Becky Lynch",
    ["Athlete", "Wrestling", "Creator"],
    ev("Born January 30, 1987 in Limerick, Ireland — age 39 in 2026 — per LeaderBiography (born 30 January 1987, age 39 as of 2026), EverybodyWiki mirror of Wikipedia, wrestling-2017 Fandom and Movies Fandom.",
       "EverybodyWiki — Becky Lynch (born 30 January 1987)", "https://en.everybodywiki.com/Becky_Lynch"),
    ev("Identified as a woman via WWE women's championship career — 'one of the most influential female wrestlers in the history of WWE' (LeaderBiography) and 'The Man' women's title reigns.",
       "LeaderBiography — Becky Lynch profile (female wrestler career)", "https://leaderbiography.com/becky-lynch/"),
    [
        src("EverybodyWiki — Becky Lynch (DOB 1987-01-30; Wikipedia mirror)", "Website", "https://en.everybodywiki.com/Becky_Lynch", "age-evidence"),
        src("LeaderBiography — Becky Lynch (DOB 30 January 1987; socials table)", "Website", "https://leaderbiography.com/becky-lynch/", "other-trusted"),
        src("Movies Fandom — Becky Lynch (born 30 January 1987, Limerick)", "Website", "https://movies.fandom.com/wiki/Becky_Lynch", "other-trusted"),
        src("Instagram — @beckylynchwwe (leaderbiography socials table)", "Instagram", "https://www.instagram.com/beckylynchwwe/", "verified-platform"),
        src("X — @BeckyLynchWWE (leaderbiography socials table)", "X", "https://x.com/BeckyLynchWWE", "verified-platform"),
    ],
    [], "WrestleMania 35 main-event winner ('Becky Two Belts') — objective athlete category. LeaderBiography socials table lists IG 5.5M+ and X 2.4M+ (third-party approximations with '+'; recorded verbatim as rounded floors, dated May-2026 page).",
    [ig("@beckylynchwwe", "LeaderBiography socials table (page dated 2026-05-04): 'Instagram @beckylynchwwe — 5.5M+'; approximation recorded verbatim at stated floor.", "5.5M+", 5500000, "rounded"),
     xacc("@BeckyLynchWWE", "LeaderBiography socials table (page dated 2026-05-04): 'Twitter (X) @BeckyLynchWWE — 2.4M+'; approximation recorded verbatim at stated floor.", "2.4M+", 2400000, "rounded")]))

NEW.append(entry("W-2026-127", "Charlotte Flair",
    ["Athlete", "Wrestling", "Creator"],
    ev("Born April 5, 1986 in Charlotte, North Carolina — age 40 in 2026 — per IMDb biography (Born April 5, 1986), ITRWrestling, Sportskeeda player page and LeaderBiography (born April 5, 1986, age 40 as of 2026).",
       "IMDb — Ashley Fliehr/Charlotte Flair (born April 5, 1986)", "https://www.imdb.com/name/nm4220563/"),
    ev("Identified as a woman via WWE women's championship career — 'the most decorated female wrestler with 14 World Championships' (ITRWrestling) and inaugural WWE Women's Champion 2016 (IMDb bio).",
       "ITRWrestling — Charlotte Flair bio (women's championship career)", "https://itrwrestling.com/bio/charlotte-flair/"),
    [
        src("IMDb — Ashley Fliehr biography (DOB 1986-04-05)", "Website", "https://www.imdb.com/name/nm4220563/", "age-evidence"),
        src("ITRWrestling — Charlotte Flair 2026 bio (born April 5, 1986)", "Website", "https://itrwrestling.com/bio/charlotte-flair/", "other-trusted"),
        src("Sportskeeda — Charlotte Flair player page (Date of Birth April 5, 1986)", "Website", "https://www.sportskeeda.com/player/charlotte-flair", "other-trusted"),
        src("Instagram — @charlottewwe (leaderbiography socials table)", "Instagram", "https://www.instagram.com/charlottewwe/", "verified-platform"),
        src("X — @MsCharlotteWWE (leaderbiography socials table)", "X", "https://x.com/MsCharlotteWWE", "verified-platform"),
    ],
    [], "14-time WWE women's world champion ('The Queen') — objective athlete category. Real name Ashley Fliehr per IMDb. Handles via LeaderBiography socials table; counts not captured — UNKNOWN.",
    [ig("@charlottewwe", "Handle via LeaderBiography socials table; count not captured."),
     xacc("@MsCharlotteWWE", "Handle via LeaderBiography socials table; count not captured.")]))

NEW.append(entry("W-2026-128", "Bayley",
    ["Athlete", "Wrestling", "Creator"],
    ev("Born June 15, 1989 in Newark, California — age 37 in 2026 — per IMDb (Born June 15, 1989 in Newark, California), TheSmackdownHotel profile (Gender: Female shown; born June 15, 1989, age 37) and LeaderBiography (age 37 as of 2026).",
       "IMDb — Pamela Martinez/Bayley (born June 15, 1989)", "https://www.imdb.com/name/nm2077528/bio/"),
    ev("Identified as a woman via TheSmackdownHotel structured profile ('Gender: Female') and WWE women's championship career — first WWE Women's Grand Slam champion.",
       "TheSmackdownHotel — Bayley profile (Gender: Female)", "https://www.thesmackdownhotel.com/wrestlers/bayley"),
    [
        src("IMDb — Pamela Martinez bio (DOB 1989-06-15)", "Website", "https://www.imdb.com/name/nm2077528/bio/", "age-evidence"),
        src("TheSmackdownHotel — Bayley wrestler profile (Gender: Female; born June 15, 1989)", "Website", "https://www.thesmackdownhotel.com/wrestlers/bayley", "other-trusted"),
        src("LeaderBiography — Bayley (DOB June 15, 1989; socials @itsmebayley + @itsBayleyWWE)", "Website", "https://leaderbiography.com/bayley/", "other-trusted"),
        src("Instagram — @itsmebayley (leaderbiography socials table)", "Instagram", "https://www.instagram.com/itsmebayley/", "verified-platform"),
        src("X — @itsBayleyWWE (leaderbiography socials table)", "X", "https://x.com/itsBayleyWWE", "verified-platform"),
    ],
    [], "First WWE Women's Grand Slam champion (real name Pamela Martinez) — objective athlete category. Handles via LeaderBiography socials table; counts not captured — UNKNOWN.",
    [ig("@itsmebayley", "Handle via LeaderBiography socials table; count not captured."),
     xacc("@itsBayleyWWE", "Handle via LeaderBiography socials table; count not captured.")]))

NEW.append(entry("W-2026-129", "Liv Morgan",
    ["Athlete", "Wrestling", "Creator"],
    ev("Born June 8, 1994 in Morristown, New Jersey — age 32 in 2026 — per Wikipedia (born June 8, 1994, age 32), ProWrestling Fandom and TVInsider (Birth Date: June 8, 1994).",
       "Wikipedia — Liv Morgan (born June 8, 1994)", "https://en.wikipedia.org/wiki/Liv_Morgan"),
    ev("Identified as a woman via WWE women's championship career — Women's World Champion (third reign) and 2026 Women's Royal Rumble winner per Wikipedia; she/her bios.",
       "Wikipedia — Liv Morgan (women's championship career)", "https://en.wikipedia.org/wiki/Liv_Morgan"),
    [
        src("Wikipedia — Liv Morgan (DOB 1994-06-08; Women's World Champion)", "Website", "https://en.wikipedia.org/wiki/Liv_Morgan", "age-evidence"),
        src("ProWrestling Fandom — Liv Morgan (born June 8, 1994)", "Website", "https://prowrestling.fandom.com/wiki/Liv_Morgan", "other-trusted"),
        src("TVInsider — Liv Morgan profile (Birth Date June 8, 1994)", "Website", "https://www.tvinsider.com/people/liv-morgan/", "other-trusted"),
    ],
    [], "Three-time WWE Women's World Champion (real name Gionna Daddio) — objective athlete category. No handle value captured this pass (TVInsider's IMDB/Twitter/Instagram icons unlabeled) — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-130", "Alexa Grasso",
    ["Athlete", "MMA", "Creator"],
    ev("Born August 9, 1993 in Guadalajara, Mexico — age 33 in 2026 — per FightOmic stats table (Date of Birth: 9 August 1993, Age 33), Wikiwand/Wikipedia (born August 9, 1993) and CelebsWiki (Birth Date August 9, 1993).",
       "FightOmic — Alexa Grasso profile (DOB 9 August 1993)", "https://fightomic.com/alexa-grasso-profile/"),
    ev("Identified as a woman via UFC women's championship career — 'Mexico's first female UFC champion', UFC Women's Flyweight division (FightOmic/Wikipedia).",
       "Wikipedia — Alexa Grasso (first Mexican female UFC champion)", "https://wikiwand.com/en/articles/Alexa_Grasso"),
    [
        src("FightOmic — Alexa Grasso profile (DOB 1993-08-09; women’s flyweight)", "Website", "https://fightomic.com/alexa-grasso-profile/", "age-evidence"),
        src("Wikipedia — Alexa Grasso (DOB 1993-08-09; UFC career)", "Website", "https://wikiwand.com/en/articles/Alexa_Grasso", "other-trusted"),
        src("CelebsWiki — Alexa Grasso bio (Birth Date August 9, 1993)", "Website", "https://celebswiki.info/alexa-grasso-bio", "other-trusted"),
    ],
    [], "First Mexican-born female UFC champion (2023 Women's Flyweight title vs Shevchenko) — objective athlete category. No handle captured this pass — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-131", "Rose Namajunas",
    ["Athlete", "MMA", "Creator"],
    ev("Born June 29, 1992 in Milwaukee, Wisconsin — age 34 in 2026 — per Sportskeeda player page (Date of Birth June 29, 1992), FightOmic stats (29 June 1992, Age 34), MMA-Blog structured birthDate 1992-06-29 and Reference.org.",
       "Sportskeeda — Rose Namajunas player page (DOB June 29, 1992)", "https://www.sportskeeda.com/player/rose-namajunas"),
    ev("Identified as a woman via UFC women's championship career — former two-time UFC Women's Strawweight Champion (Sportskeeda/Reference.org); Tuko profile 'Gender: Female'.",
       "Tuko — Rose Namajunas profile summary (Gender: Female)", "https://www.tuko.co.ke/facts-lifehacks/celebrity-biographies/486826-rose-namajunas-childhood-ethnicity-controversies-fight-purse/"),
    [
        src("Sportskeeda — Rose Namajunas (Date of Birth June 29, 1992)", "Website", "https://www.sportskeeda.com/player/rose-namajunas", "age-evidence"),
        src("FightOmic — Rose Namajunas profile (DOB 29 June 1992; women's flyweight)", "Website", "https://fightomic.com/rose-namajunas-profile/", "other-trusted"),
        src("MMA-Blog — Rose Namajunas profile (birthDate 1992-06-29; sameAs instagram.com/rosenamajunas)", "Website", "https://www.mma-blog.com/post/rose-namajunas-thug-rose-fighter-profile-career-legacy", "other-trusted"),
        src("Instagram — @rosenamajunas (mma-blog structured sameAs)", "Instagram", "https://www.instagram.com/rosenamajunas/", "verified-platform"),
    ],
    [], "Two-time UFC Women's Strawweight Champion ('Thug Rose') — objective athlete category. Handle via MMA-Blog structured sameAs (which also states '1.55 million Instagram followers' in fun-facts — treat as unverified approximation; count recorded UNKNOWN, not the estimate).",
    [ig("@rosenamajunas", "Handle via mma-blog.com structured sameAs; an approximate '1.55M followers' claim on that page was NOT recorded (not platform-observed).")]))

NEW.append(entry("W-2026-132", "Lindsey Vonn",
    ["Athlete", "Skiing", "Creator"],
    ev("Born October 18, 1984 in St. Paul, Minnesota — age 41 in 2026 — per Biography.com ('BORN: October 18, 1984'), Wikipedia (born October 18, 1984) and TheBiographyBytes/BiographyBrief (age 41 as of 2026).",
       "Biography.com — Lindsey Vonn (born October 18, 1984)", "https://www.biography.com/athletes/lindsey-vonn"),
    ev("Identified as a woman via women's alpine skiing career — 'the first American woman to win Olympic downhill gold' 2010 (Biography.com/Wikipedia); she/her profile.",
       "Wikipedia — Lindsey Vonn (women's alpine skiing career)", "https://en.wikipedia.org/wiki/Lindsey_Vonn"),
    [
        src("Biography.com — Lindsey Vonn (DOB 1984-10-18; Olympic medals)", "Website", "https://www.biography.com/athletes/lindsey-vonn", "age-evidence"),
        src("Wikipedia — Lindsey Vonn (DOB 1984-10-18; 84 World Cup wins)", "Website", "https://en.wikipedia.org/wiki/Lindsey_Vonn", "other-trusted"),
        src("TheBiographyBytes — Lindsey Vonn bio (age 41, born October 18, 1984)", "Website", "https://thebiographybytes.com/lindsey-vonn/", "other-trusted"),
    ],
    [], "2010 Olympic downhill gold medalist and 82-84x World Cup winner (came out of retirement 2024 for Milan Cortina 2026) — objective athlete category. No handle captured this pass — follower range UNKNOWN.",
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
    if "IRR-2026-09-06-013" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-013",
            "severity": "needs-review",
            "summary": "Session-12 batch-C flags: approximated social counts recorded only with '+' verbatim floors; pre-existing athlete duplicates caught.",
            "detail": (
                "(1) Becky Lynch IG 5.5M+ / X 2.4M+: LeaderBiography socials-table approximations (page dated 2026-05-04), recorded verbatim at stated '+' floors her countType 'rounded'. "
                "(2) Rose Namajunas: mma-blog fun-facts claims '1.55 million Instagram followers' — deliberately NOT used (not platform-observed); handle kept, count UNKNOWN. "
                "(3) Re-verified this wave but excluded as pre-existing: Katie Ledecky (W-2026-006), Chloe Kim (W-2026-007), Trinity Rodman (W-2026-095)."
            ),
            "reviewStatus": "requires-owner-review",
        })
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)}) irr={len(data['irregularities'])}")

if __name__ == "__main__":
    build()
