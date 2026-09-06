#!/usr/bin/env python3
"""Session 12 batch A (2026-09-06): 14 verified adds (W-2026-101..114).
Wave 1 pipeline: US women's volleyball (Wikipedia/Grokipedia/volleybox structured
birthDate+gender+sameAs) + USWNT/NWSL soccer (Wikipedia/FotMob structured
gender/birthDate, fbref player pages with Instagram handles, live IG display).
Follower counts verbatim only; absent handles recorded as UNKNOWN per protocol.
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

NEW.append(entry("W-2026-101", "Kelsey Robinson Cook",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born June 25, 1992 in Elmhurst, Illinois — age 34 in 2026 — per Wikipedia (born June 25, 1992) plus HollywoodLife, Grokipedia, PeoplePill structured (Birth 25 June 1992) and CelebsAges (age 33 at snapshot).",
       "Wikipedia — Kelsey Robinson (born June 25, 1992)", "https://en.wikipedia.org/wiki/Kelsey_Robinson"),
    ev("Identified as a woman via PeoplePill structured data ('Gender: female') and US women's national volleyball team career (three-time Olympian: gold 2020, silver 2024, bronze 2016).",
       "PeoplePill — Kelsey Robinson (Gender: female)", "https://peoplepill.com/people/kelsey-robinson/"),
    [
        src("Wikipedia — Kelsey Robinson (DOB 1992-06-25; LOVB Atlanta)", "Website", "https://en.wikipedia.org/wiki/Kelsey_Robinson", "age-evidence"),
        src("Grokipedia — Kelsey Robinson Cook biography (DOB Jun 25 1992)", "Website", "https://grokipedia.com/page/Kelsey_Robinson", "other-trusted"),
        src("CelebsAges — Kelsey Robinson (born 25 June 1992, volleyball)", "Website", "https://www.celebsages.com/kelsey-robinson/", "other-trusted"),
    ],
    [], "S11 follow-up/pending staged earlier — cleared this session. Three-medal volleyball Olympian; married Brian Cook (Robinson Cook per Wikipedia). No public follower counts captured — social data UNKNOWN, never estimated.",
    []))

NEW.append(entry("W-2026-102", "Michelle Bartsch-Hackley",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born February 12, 1990 in Kansas City, Kansas — age 36 in 2026 — per volleybox structured birthDate 1990-02-12 and IMDb biography (born February 12, 1990).",
       "Women.volleybox — Michelle Bartsch-Hackley (birthDate 1990-02-12)", "https://women.volleybox.net/michelle-bartsch-hackley-p1735"),
    ev("Identified as a woman via volleybox structured gender 'Female' and US women's national-team outside hitter career (2020 Olympic gold).",
       "Women.volleybox — Michelle Bartsch-Hackley player data (gender: Female)", "https://women.volleybox.net/michelle-bartsch-hackley-p1735"),
    [
        src("Women.volleybox — Michelle Bartsch-Hackley (DOB 1990-02-12; gender Female; sameAs IG/X)", "Website", "https://women.volleybox.net/michelle-bartsch-hackley-p1735", "age-evidence"),
        src("IMDb — Michelle Bartsch-Hackley biography (born Feb 12, 1990; Olympic gold Tokyo 2020)", "Website", "https://www.imdb.com/name/nm12804490/bio/", "other-trusted"),
        src("Instagram — @bartschhackley14 (volleybox sameAs)", "Instagram", "https://www.instagram.com/bartschhackley14", "verified-platform"),
        src("X — @bartschy (volleybox sameAs)", "X", "https://twitter.com/bartschy", "verified-platform"),
    ],
    [], "2020 Olympic gold medalist (Tokyo) — objective athlete category; now Ohio State assistant coach per volleybox. Handles verbatim from volleybox structured sameAs; no follower counts captured — UNKNOWN.",
    [account("Instagram", "@bartschhackley14", "https://www.instagram.com/bartschhackley14", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via women.volleybox.net structured sameAs; count not captured."),
     account("X", "@bartschy", "https://twitter.com/bartschy", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via women.volleybox.net structured sameAs; count not captured.")]))

NEW.append(entry("W-2026-103", "Naomi Girma",
    ["Athlete", "Soccer", "Creator"],
    ev("Born June 14, 2000 in San Jose, California — age 26 in 2026 — per Wikipedia (born June 14, 2000), Grokipedia, and Team USA profile (age 26).",
       "Wikipedia — Naomi Girma (born June 14, 2000)", "https://en.wikipedia.org/wiki/Naomi_Girma"),
    ev("Identified as a woman via USWNT women's national team career — 2024 Olympic gold (played every minute); U.S. Soccer Female Player of the Year 2023 (Wikipedia/Chelsea FC release).",
       "Chelsea FC — Welcome Naomi Girma (women's US national team defender)", "https://www.chelseafc.com/en/news/article/welcome-to-chelsea-naomi-girma"),
    [
        src("Wikipedia — Naomi Girma (DOB 2000-06-14; Chelsea WSL)", "Website", "https://en.wikipedia.org/wiki/Naomi_Girma", "age-evidence"),
        src("Team USA — Naomi Girma profile (2024 Olympic gold, San Jose)", "Website", "https://www.teamusa.com/profiles/naomi-girma", "official"),
        src("Grokipedia — Naomi Girma biography (world-record $1M+ transfer)", "Website", "https://grokipedia.com/page/Naomi_Girma", "other-trusted"),
    ],
    [], "2024 Olympic gold medalist and world-record women's soccer signing (Chelsea) — objective athlete category. No social handle captured this session — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-104", "Mallory Swanson (née Pugh)",
    ["Athlete", "Soccer", "Creator"],
    ev("Born April 29, 1998 in Littleton, Colorado — age 28 in 2026 — per Wikipedia (born April 29, 1998) and FotMob structured birthDate 1998-04-29 (Age 28).",
       "Wikipedia — Mallory Swanson (born April 29, 1998)", "https://en.wikipedia.org/wiki/Mallory_Swanson"),
    ev("Identified as a woman via FotMob structured data ('gender: Female') and USWNT women's national team career (2019 World Cup, 2024 Olympic gold in the final vs Brazil).",
       "FotMob — Mallory Swanson player record (gender: Female)", "https://www.fotmob.com/players/773387/mallory-swanson"),
    [
        src("Wikipedia — Mallory Swanson (DOB 1998-04-29; Chicago Stars)", "Website", "https://en.wikipedia.org/wiki/Mallory_Swanson", "age-evidence"),
        src("FotMob — Mallory Swanson (birthDate + gender Female structured)", "Website", "https://www.fotmob.com/players/773387/mallory-swanson", "other-trusted"),
        src("Kiddle — Mallory Swanson (DOB 1998-04-29; married name info)", "Website", "https://kids.kiddle.co/Mallory_Swanson", "other-trusted"),
    ],
    [], "2019 FIFA Women's World Cup champion and scorer of the 2024 Olympic gold-medal goal — objective athlete category. Married name Swanson (née Pugh) per Wikipedia. No follower counts captured — UNKNOWN.",
    []))

NEW.append(entry("W-2026-105", "Sophia Smith",
    ["Athlete", "Soccer", "Creator"],
    ev("Born August 10, 2000 in Windsor, Colorado — age 26 in 2026 — per Britannica (born August 10, 2000) and the official ussoccer.com player page (visible text 'Date of Birth Aug 10 2000').",
       "Britannica — Sophia Smith (born August 10, 2000)", "https://www.britannica.com/biography/Sophia-Smith-footballer"),
    ev("Identified as a woman via TheFameCrowd structured 'Gender: Female' and USWNT/NWSL women's soccer career (2022 NWSL MVP, 2024 Olympic gold).",
       "TheFameCrowd — Sophia Smith profile (Gender: Female)", "https://thefamecrowd.com/celebrity/sophia-smith/"),
    [
        src("Britannica — Sophia Smith (DOB 2000-08-10; 2024 Olympic gold)", "Website", "https://www.britannica.com/biography/Sophia-Smith-footballer", "age-evidence"),
        src("US Soccer — Sophia Smith official player profile (DOB Aug 10 2000)", "Website", "https://qa-8733871.ussoccer.com/players/s/sophia-smith", "official"),
        src("Mountaintop University profile — verified-age explainer (born Aug 10, 2000)", "Website", "https://ir.mountaintopuniversity.edu.ng/article/how-old-is-sophia-smith-verified-age-birthday-and-career-timeline", "other-trusted"),
    ],
    [], "2022 NWSL MVP and 2022 US Soccer Female Player of the Year, 2024 Olympic gold — objective athlete category. Note: ussoccer structured JSON shows 2000-08-09 (UTC-offset artifact) while the page's true display text and Britannica agree on Aug 10 — variance logged in IRR-2026-09-06-011.",
    []))

NEW.append(entry("W-2026-106", "Lindsey Heaps (née Horan)",
    ["Athlete", "Soccer", "Creator"],
    ev("Born May 26, 1994 in Golden, Colorado — age 32 in 2026 — per Wikipedia (born May 26, 1994; name Lindsey Michelle Heaps née Horan), Kiddle (age 32), sportsmanbio (DOB 1994-05-26) and richathletes.",
       "Wikipedia — Lindsey Horan/Heaps (born May 26, 1994)", "https://en.wikipedia.org/wiki/Lindsey_Horan"),
    ev("Identified as a woman via USWNT captaincy and women's national team career — US Women's National Team captain (Wikipedia/Kiddle), sportsmanbio 'Gender: Female'.",
       "SportsManBio — Lindsey Horan profile (Gender: Female)", "https://sportsmanbio.com/lindsey-horan/"),
    [
        src("Wikipedia — Lindsey Heaps (DOB 1994-05-26; OL Lyonnes; USWNT captain)", "Website", "https://en.wikipedia.org/wiki/Lindsey_Horan", "age-evidence"),
        src("Instagram — @lindseyhoran10 live display ('Lindsey Horan Heaps', 406K)", "Instagram", "https://www.instagram.com/lindseyhoran10/", "verified-platform"),
        src("Kiddle — Lindsey Horan (DOB 1994-05-26; 2024 Olympic gold captain)", "Website", "https://kids.kiddle.co/Lindsey_Horan", "other-trusted"),
    ],
    [], "USWNT captain and 2024 Olympic gold medalist — objective athlete category. Live Instagram display captured verbatim 2026-09-06. Maiden name Horan (Wikipedia records married name Heaps).",
    [account("Instagram", "@lindseyhoran10", "https://www.instagram.com/lindseyhoran10/", "406K", 406000, "rounded",
             "Instagram public profile display via search snippet: '406K followers, 465 following, 792 posts' (Lindsey Horan Heaps) — checked 2026-09-06.")]))

NEW.append(entry("W-2026-107", "Alyssa Naeher",
    ["Athlete", "Soccer", "Creator"],
    ev("Born April 20, 1988 in Bridgeport, Connecticut — age 38 in 2026 — per the official Chicago Stars roster page (DOB 04/20/88), fbref structured birthDate 1988-04-20, and MarriedBiography structured data.",
       "Chicago Stars FC — Alyssa Naeher official roster page (DOB 04/20/88)", "https://chicagostars.com/roster/alyssa-naeher/"),
    ev("Identified as a woman via MarriedBiography structured data ('gender: Female' in JSON-LD) and USWNT women's national team goalkeeping career (2019 World Cup, 2024 Olympic gold).",
       "MarriedBiography — Alyssa Naeher (gender: Female structured)", "https://marriedbiography.com/alyssa-naeher-biography/"),
    [
        src("Chicago Stars FC — Alyssa Naeher roster (DOB 04/20/88)", "Website", "https://chicagostars.com/roster/alyssa-naeher/", "official"),
        src("FBref — Alyssa Naeher (DOB 1988-04-20; lists Instagram @alyssanaeher)", "Website", "https://fbref.com/en/players/4c1ee572/Alyssa-Naeher", "age-evidence"),
        src("MarriedBiography — Alyssa Naeher (DOB 1988-04-20; gender Female; sameAs IG/X)", "Website", "https://marriedbiography.com/alyssa-naeher-biography/", "other-trusted"),
        src("Instagram — @alyssanaeher (fbref + sameAs)", "Instagram", "https://www.instagram.com/alyssanaeher/", "verified-platform"),
        src("X — @AlyssaNaeher (marriedbiography sameAs)", "X", "https://x.com/AlyssaNaeher", "verified-platform"),
    ],
    [], "Two-time World Cup champion and 2024 Olympic gold goalkeeper, The Best FIFA Women's Goalkeeper 2024 — objective athlete category. Handles via fbref header and sameAs; no follower counts captured — UNKNOWN.",
    [account("Instagram", "@alyssanaeher", "https://www.instagram.com/alyssanaeher/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via fbref player page header ('Instagram: @alyssanaeher') + MarriedBiography sameAs; count not captured."),
     account("X", "@AlyssaNaeher", "https://x.com/AlyssaNaeher", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via MarriedBiography structured sameAs; count not captured.")]))

NEW.append(entry("W-2026-108", "Rose Lavelle",
    ["Athlete", "Soccer", "Creator"],
    ev("Born May 14, 1995 in Cincinnati, Ohio — age 31 in 2026 — per Wikipedia (born May 14, 1995) and fbref structured record (Born: May 14, 1995, Age 31).",
       "Wikipedia — Rose Lavelle (born May 14, 1995)", "https://en.wikipedia.org/wiki/Rose_Lavelle"),
    ev("Identified as a woman via USWNT women's national team and NWSL career — 2019 World Cup Bronze Ball, 2024 Olympic gold; Gotham FC midfielder (Wikipedia/fbref/Kiddle).",
       "Kiddle — Rose Lavelle (women's national team midfielder)", "https://kids.kiddle.co/Rose_Lavelle"),
    [
        src("Wikipedia — Rose Lavelle (DOB 1995-05-14; Gotham FC; 2025 NWSL champion)", "Website", "https://en.wikipedia.org/wiki/Rose_Lavelle", "age-evidence"),
        src("FBref — Rose Lavelle (DOB 1995-05-14; lists Instagram @lavellerose)", "Website", "https://fbref.com/en/players/dcd6a67e/Rose-Lavelle", "other-trusted"),
        src("NewsInBollywood — Rose Lavelle bio (DOB May 14, 1995; IG handle @lavellerose)", "Website", "https://www.newsinbollywood.com/wiki/rose-lavelle/", "other-trusted"),
        src("Instagram — @lavellerose (fbref header)", "Instagram", "https://www.instagram.com/lavellerose/", "verified-platform"),
    ],
    [], "2019 World Cup winner (scored in the final), 2024 Olympic gold, 2025 NWSL champion MVP — objective athlete category. Handle via fbref; count not captured — UNKNOWN.",
    [account("Instagram", "@lavellerose", "https://www.instagram.com/lavellerose/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via fbref player page header ('Instagram: @lavellerose') and NewsInBollywood bio table; count not captured.")]))

NEW.append(entry("W-2026-109", "Crystal Dunn (Soubrier)",
    ["Athlete", "Soccer", "Creator"],
    ev("Born July 3, 1992 in New Hyde Park, New York — age 34 in 2026 — per RotoWire player page (DOB 7/3/1992), fbref structured (Born: July 3, 1992), Kiddle and richathletes.",
       "FBref — Crystal Dunn (born July 3, 1992)", "https://fbref.com/en/players/a20c6459/Crystal-Dunn"),
    ev("Identified as a woman via USWNT women's national team career — 2019 World Cup, 2024 Olympic gold; married Pierre Soubrier, has a son (Kiddle).",
       "Kiddle — Crystal Dunn/Soubrier (women's soccer career)", "https://kids.kiddle.co/Crystal_Dunn"),
    [
        src("FBref — Crystal Dunn (DOB 1992-07-03; lists Instagram @cdunn19)", "Website", "https://fbref.com/en/players/a20c6459/Crystal-Dunn", "age-evidence"),
        src("RotoWire — Crystal Dunn player page (DOB 7/3/1992; Gotham FC)", "Website", "https://www.rotowire.com/soccer/player/crystal-dunn-27926", "other-trusted"),
        src("Contents101 — Crystal Dunn bio (DOB 3 July 1992; IG handle https://instagram.com/cdunn19)", "Website", "https://contents101.com/2025/03/11/crystal-dunn-biography-education-career-controversies-and-net-worth/", "other-trusted"),
        src("Instagram — @cdunn19 (fbref + Contents101 handle link)", "Instagram", "https://www.instagram.com/cdunn19/", "verified-platform"),
    ],
    [], "2019 World Cup champion, 2015 NWSL MVP, 2024 Olympic gold — objective athlete category. Full name Crystal Alyssia Soubrier (née Dunn) per Kiddle; club: Paris Saint-Germain (2025).",
    [account("Instagram", "@cdunn19", "https://www.instagram.com/cdunn19/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via fbref player page header ('Instagram: @cdunn19') and Contents101 social-handle section; count not captured.")]))

NEW.append(entry("W-2026-110", "Tierna Davidson",
    ["Athlete", "Soccer", "Creator"],
    ev("Born September 19, 1998 in Menlo Park, California — age 27 in 2026 — per Wikipedia (born September 19, 1998), Wikiwand (age 27), broadbiography and SportsLib infobox. fbref shows September 18 — day conflict logged, adult either way.",
       "Wikipedia — Tierna Davidson (born September 19, 1998)", "https://www.wikiwand.com/en/Tierna_Davidson"),
    ev("Identified as a woman via USWNT women's national team career — 2019 World Cup, 2024 Olympic gold, Stanford national championship (Wikipedia/fbref).",
       "Wikipedia — Tierna Davidson (women's national team career)", "https://www.wikiwand.com/en/Tierna_Davidson"),
    [
        src("Wikipedia — Tierna Davidson (DOB 1998-09-19; Gotham FC)", "Website", "https://www.wikiwand.com/en/Tierna_Davidson", "age-evidence"),
        src("BroadBiography — Tierna Davidson (DOB September 19, 1998)", "Website", "https://broadbiography.com/biography/sports/tierna-davidson-biography/", "other-trusted"),
        src("FBref — Tierna Davidson (shows Sep 18 1998 — variance noted; IG @tierna_davidson)", "Website", "https://fbref.com/en/players/543614ff/Tierna-Davidson", "other-trusted"),
        src("Instagram — @tierna_davidson (fbref header)", "Instagram", "https://www.instagram.com/tierna_davidson/", "verified-platform"),
    ],
    ["CONFLICTING_INFORMATION"],
    "2019 World Cup champion and 2024 Olympic gold center back — objective athlete category. DOB-day variance: Wikipedia/Wikiwand/broadbiography/SportsLib say Sept 19; fbref says Sept 18 — recorded majority value, variance in IRR-2026-09-06-011.",
    [account("Instagram", "@tierna_davidson", "https://www.instagram.com/tierna_davidson/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via fbref player page header ('Instagram: @tierna_davidson'); count not captured.")]))

NEW.append(entry("W-2026-111", "Emily Fox",
    ["Athlete", "Soccer", "Creator"],
    ev("Born July 5, 1998 in Ashburn, Virginia — age 28 in 2026 — per Wikipedia (born July 5, 1998) and FotMob structured JSON-LD birthDate 1998-07-05 (Age 28).",
       "Wikipedia — Emily Fox (born July 5, 1998)", "https://en.wikipedia.org/wiki/Emily_Fox"),
    ev("Identified as a woman via FotMob structured data ('gender: Female' JSON-LD) and USWNT women's national team career (2024 Olympic gold; Arsenal UEFA Women's Champions League 2025).",
       "FotMob — Emily Fox player record (gender: Female)", "https://www.fotmob.com/players/1266128/emily-fox"),
    [
        src("Wikipedia — Emily Fox (DOB 1998-07-05; Arsenal WSL)", "Website", "https://en.wikipedia.org/wiki/Emily_Fox", "age-evidence"),
        src("FotMob — Emily Fox (birthDate + gender Female structured)", "Website", "https://www.fotmob.com/players/1266128/emily-fox", "other-trusted"),
        src("FBref — Emily Fox (DOB 1998-07-05; lists Instagram @___emilyfox)", "Website", "https://fbref.com/en/players/2eb9f54a/Emily-Fox", "other-trusted"),
        src("Instagram — @___emilyfox (fbref header)", "Instagram", "https://www.instagram.com/___emilyfox/", "verified-platform"),
    ],
    [], "2024 Olympic gold medalist and 2025 UEFA Women's Champions League winner (Arsenal) — objective athlete category. Handle via fbref; count not captured — UNKNOWN.",
    [account("Instagram", "@___emilyfox", "https://www.instagram.com/___emilyfox/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle via fbref player page header ('Instagram: @___emilyfox'); count not captured.")]))

NEW.append(entry("W-2026-112", "Emily Sonnett",
    ["Athlete", "Soccer", "Creator"],
    ev("Born November 25, 1993 in Marietta, Georgia — age 32 in 2026 — per BroadBiography, Grokipedia, SportsLib infobox (1993-11-25), SportsBrief (DOB + Gender: Female) and SoccerWizdom.",
       "SportsLib — Emily Sonnett profile (born November 25, 1993)", "https://www.sportslib.net/football/feed_fbvods.php?idx_no=2905"),
    ev("Identified as a woman via SportsBrief structured profile ('Gender: Female') and USWNT women's national team career (2019 World Cup, 2024 Olympic gold).",
       "SportsBrief — Emily Sonnett profile (Gender: Female)", "https://sportsbrief.com/football/58772-who-emily-sonnett-united-states-soccer-player/"),
    [
        src("SportsLib — Emily Sonnett (DOB 1993-11-25; Gotham FC)", "Website", "https://www.sportslib.net/football/feed_fbvods.php?idx_no=2905", "age-evidence"),
        src("Grokipedia — Emily Sonnett biography (born Nov 25, 1993; UVA Hermann Trophy)", "Website", "https://grokipedia.com/page/Emily_Sonnett", "other-trusted"),
        src("SportsBrief — Emily Sonnett (DOB 1993-11-25; Gender: Female)", "Website", "https://sportsbrief.com/football/58772-who-emily-sonnett-united-states-soccer-player/", "other-trusted"),
    ],
    [], "2019 World Cup champion, 2024 Olympic gold, three-time NWSL champion — objective athlete category. No social handle captured this session — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-113", "Korbin Shrader (née Albert)",
    ["Athlete", "Soccer", "Creator"],
    ev("Born October 13, 2003 in Grayslake, Illinois — age 22 in 2026 — per Wikipedia under married name Korbin Shrader (born October 13, 2003), Facts.net, MBGBPatna and TheSportsGrail.",
       "Wikipedia — Korbin Shrader/Albert (born October 13, 2003)", "https://en.wikipedia.org/wiki/Korbin_Shrader"),
    ev("Identified as a woman via USWNT women's national team career — 2024 Olympic gold (scored vs Australia); 'she plays as a midfielder for OL Lyonnes and the United States national team' (Wikipedia).",
       "Wikipedia — Korbin Shrader (women's national team career)", "https://en.wikipedia.org/wiki/Korbin_Shrader"),
    [
        src("Wikipedia — Korbin Shrader (DOB 2003-10-13; OL Lyonnes)", "Website", "https://en.wikipedia.org/wiki/Korbin_Shrader", "age-evidence"),
        src("TheSportsGrail — Korbin Albert bio (DOB 2003-10-13; IG @korbin.rose_ 100K+)", "Website", "https://thesportsgrail.com/who-is-uwsnt-soccer-player-korbin-albert-bio-age-height-parents-boyfriend-salary-and-college/", "other-trusted"),
        src("Instagram — @korbin.rose_ (per TheSportsGrail 'Instagram' section)", "Instagram", "https://www.instagram.com/korbin.rose_/", "verified-platform"),
    ],
    [], "2024 Olympic gold medalist (PSG → OL Lyonnes) — objective athlete category. Wikipedia page under married name 'Korbin Shrader' per August 2026 snapshot. IG count 100K+ per August 2024 article (dated snapshot, recorded verbatim).",
    [account("Instagram", "@korbin.rose_", "https://www.instagram.com/korbin.rose_/", "100K+", 100000, "rounded",
             "TheSportsGrail article (Aug 2024): 'Instagram account with the handle @korbin.rose_, where she has over 100K followers' — dated snapshot verbatim.")]))

NEW.append(entry("W-2026-114", "Sam Coffey",
    ["Athlete", "Soccer", "Creator"],
    ev("Born December 31, 1998 — age 27 in 2026 — per the official ussoccer.com player page ('Date of Birth Dec 31 1998'), fbref (Born: December 31, 1998, age 27) and Pantheon (born December 31, 1998).",
       "US Soccer — Sam Coffey official player profile (DOB Dec 31 1998)", "https://www.ussoccer.com/players/c/sam-coffey"),
    ev("Identified as a woman via USWNT women's national team career (2024 Olympic gold) and NWSL Portland Thorns captaincy — she/her bios (Pantheon, AthletesHistory).",
       "Pantheon — Sam Coffey (Portland Thorns/USWNT women's midfielder)", "https://pantheon.world/profile/person/Sam_Coffey"),
    [
        src("US Soccer — Sam Coffey official player profile (DOB Dec 31 1998; Manchester City)", "Website", "https://www.ussoccer.com/players/c/sam-coffey", "official"),
        src("FBref — Sam Coffey (DOB 1998-12-31; Portland Thorns rounds)", "Website", "https://fbref.com/en/players/4d28a90a/Sam-Coffey", "age-evidence"),
        src("Pantheon — Sam Coffey (born December 31, 1998 biography)", "Website", "https://pantheon.world/profile/person/Sam_Coffey", "other-trusted"),
    ],
    [], "2024 Olympic gold defensive midfielder — objective athlete category. Minority source (AthletesHistory) states Dec 12 — logged as variance in IRR-2026-09-06-011; majority (official US Soccer + fbref + Pantheon) agree Dec 31. No social handle captured — UNKNOWN.",
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
    if "IRR-2026-09-06-011" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-011",
            "severity": "needs-review",
            "summary": "Session-12 batch-A flags: DOB day-level variances + name changes recorded verbatim for manual review.",
            "detail": (
                "(1) Tierna Davidson: Wikipedia/BroadBiography/SportsLib = 1998-09-19 vs fbref 1998-09-18 — majority recorded, adult unaffected. "
                "(2) Sophia Smith: ussoccer.com page display text says 'Date of Birth Aug 10 2000' while its embedded JSON-LD says 2000-08-09 (UTC-offset artifact pattern); Britannica agrees Aug 10 — recorded Aug 10. "
                "(3) Sam Coffey: minority source AthletesHistory.com says 1998-12-12 — official US Soccer + fbref + Pantheon all say 1998-12-31 — recorded Dec 31. "
                "(4) Name changes recorded as outgrown/maiden notes: Korbin Albert -> Korbin Shrader (Wikipedia, Aug 2026), Lindsey Horan -> Lindsey Heaps (Wikipedia + live IG display 'Lindsey Horan Heaps'), Kelsey Robinson -> Robinson Cook, Crystal Dunn -> Soubrier. "
                "(5) Korbin Shrader IG count 100K+ comes from an Aug-2024 article (stale-ish; kept verbatim with date). "
                "(6) Most USWNT accounts have sourced handles but unobserved displays — recorded FOLLOWER_COUNT_UNKNOWN per protocol (bartschhackley14, alyssanaeher, lavellerose, cdunn19, tierna_davidson, ___emilyfox)."
            ),
            "reviewStatus": "requires-owner-review",
        })
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["reviewQueueCount"] = len(data["reviewQueue"])
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)}) irr={len(data['irregularities'])}")

if __name__ == "__main__":
    build()
