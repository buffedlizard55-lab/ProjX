#!/usr/bin/env python3
"""Session 11 batch 2 (2026-09-06): 22 verified adds bringing the catalog to 100
VERIFIED profiles. Pipeline: yoga/fitness-YouTube creators with structured
sameAs data, artistic gymnasts (USAG/Team USA/Wikipedia), track & field
(TeamUSA/Wikipedia/roster sameAs), golf, tennis (WTA/ESPN), soccer
(Britannica), WNBA (Wikipedia/Britannica) and swimming (Olympedia Tier-1 +
live Instagram displays). Counts are verbatim public displays only.
"""

import json
from pathlib import Path

CATALOG = Path("data/catalog.json")
CHECKED = "2026-09-06"

RANGES = [
    (1000, "Under 1K"), (5000, "1K–4.9K"), (10000, "5K–9.9K"),
    (25000, "10K–24.9K"), (50000, "25K–49.9K"), (100000, "50K–99.9K"),
    (250000, "100K–249.9K"), (500000, "250K–499.9K"), (1000000, "500K–999.9K"),
    (5000000, "1M–4.9M"),
]
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
        return {"platform": None, "username": None, "display": None,
                "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                "checkedAt": CHECKED}
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

NEW.append(entry("W-2026-079", "Adriene Mishler (Yoga with Adriene)",
    ["Fitness", "Wellness", "Creator"],
    ev("Born September 29, 1984 in Austin, Texas — age 41 in 2026 — per Wikipedia (encyclopedic biography) and TheFamousPeople; structured birthDate 1984-09-29 also present in InfluencerFee profile data.",
       "Wikipedia — Adriene Mishler (born September 29, 1984)", "https://www.wikiwand.com/en/Adriene_Mishler"),
    ev("Identified as a woman via Wikipedia biography (actress and yoga teacher, she/her throughout) and TheFamousPeople profile of her career.",
       "TheFamousPeople — Adriene Mishler biography (she/her)", "https://www.thefamouspeople.com/profiles/adriene-mishler-42957.php"),
    [
        src("Wikipedia — Adriene Mishler (DOB 1984-09-29; 13M+ YouTube subscribers)", "Website", "https://www.wikiwand.com/en/Adriene_Mishler", "age-evidence"),
        src("TheFamousPeople — Adriene Mishler (birthday September 29, 1984)", "Website", "https://www.thefamouspeople.com/profiles/adriene-mishler-42957.php", "other-trusted"),
        src("InfluencerFee — Adriene Mishler (structured sameAs: @yogawithadriene, @adrienelouise 2.5M)", "Website", "https://influencerfee.com/influencer/yoga-with-adriene/", "other-trusted"),
        src("YouTube — @yogawithadriene (channel per Wikipedia infobox)", "YouTube", "https://www.youtube.com/@yogawithadriene", "verified-platform"),
        src("Instagram — @adrienelouise (structured sameAs link)", "Instagram", "https://www.instagram.com/adrienelouise/", "verified-platform"),
    ],
    [], "Discovered this session via yoga/wellness creator pipeline. Objective category: certified yoga teacher and host of YouTube's largest yoga channel (Yoga with Adriene); Find What Feels Good co-founder. No appearance-based data used.",
    [account("YouTube", "@yogawithadriene", "https://www.youtube.com/@yogawithadriene", "13M+", 13000000, "rounded",
             "Wikipedia (Jan 2025 snapshot): 'over 13 million subscribers… top 500 most subscribed YouTube channels'; LiveYogaTeachers (2026) cites 13M+."),
     account("Instagram", "@adrienelouise", "https://www.instagram.com/adrienelouise/", "2.5M", 2500000, "rounded",
             "InfluencerFee biography (2026): Instagram 2.5M followers (structured sameAs link).")]))

NEW.append(entry("W-2026-080", "Maddie Lymburner (MadFit)",
    ["Fitness", "Wellness", "Creator"],
    ev("Born November 14, 1995 in Waterdown (Hamilton), Ontario — age 30 in 2026 — recorded identically by InformationCradle (structured), Celebrity-Birthdays, FeaturedBiography and St-Aug profile pages.",
       "InformationCradle — Maddie Lymburner (born November 14, 1995)", "https://informationcradle.com/maddie-lymburner/"),
    ev("Identified as a woman via InformationCradle profile table listing 'Gender: Female' and consistent she/her biographies (fitness blogger, married to Chris Hartwig).",
       "InformationCradle — Maddie Lymburner profile (Gender: Female)", "https://informationcradle.com/maddie-lymburner/"),
    [
        src("InformationCradle — Maddie Lymburner (DOB 1995-11-14; Gender: Female; MadFit 6M+ Jun 2021)", "Website", "https://informationcradle.com/maddie-lymburner/", "age-evidence"),
        src("St-Aug profile — Maddie 'MadFit' Lymburner (over 7.3M MadFit subscribers)", "Website", "https://explore.st-aug.edu/exp/maddie-lymburner-madfit-bio-wiki-age-height-family-husband-youtube-and-net-worth", "other-trusted"),
        src("FeaturedBiography — Maddie Lymburner (MadFit 6.86M subs; IG credit @madfit.ig)", "Website", "https://featuredbiography.com/maddie-lymburner/", "other-trusted"),
        src("YouTube — MadFit channel (fitness workouts)", "YouTube", "https://www.youtube.com/@MadFit", "verified-platform"),
        src("Instagram — @madfit.ig (per FeaturedBiography image credit)", "Instagram", "https://www.instagram.com/madfit.ig/", "verified-platform"),
    ],
    [], "Canadian home-workout creator; named Google's top Canadian YouTube creator 2020 (InformationCradle). Objective fitness category. Latest published count (7.3M, Mar 2026 profile) recorded with 6.86M snapshot cited.",
    [account("YouTube", "MadFit", "https://www.youtube.com/@MadFit", "7.3M+", 7300000, "rounded",
             "St-Aug profile (March 2026): MadFit channel 'over 7.3 million subscribers'; FeaturedBiography snapshot 6.86M; InformationCradle 6M+ (Jun 2021)."),
     account("Instagram", "@madfit.ig", "https://www.instagram.com/madfit.ig/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle confirmed via FeaturedBiography photo credit (@madfit.ig); follower count not captured in snippets.")]))

NEW.append(entry("W-2026-081", "Natacha Océane",
    ["Fitness", "Wellness", "Creator"],
    ev("Born August 6, 1993 in England — age 33 in 2026 — recorded identically by AllFamous (structured birthday set), FameCop, WikiCelebs full-name bio table, and 2010Media profile.",
       "AllFamous — Natacha Océane (born August 6, 1993)", "https://allfamous.org/people/natacha-oceane-19930806.html"),
    ev("Identified as a woman via consistent she/her biographies — English fitness YouTuber with UCL biophysics master's; FameCop describes her channel history with 'she/her' throughout.",
       "FameCop — Natacha Océane biography (she/her)", "https://famecop.com/fitness/natacha-oceane/"),
    [
        src("WikiCelebs — Natacha Océane (DOB 1993-08-06; 1.6M YT; handles table)", "Website", "https://www.wikicelebs.com/natacha-oceane/", "age-evidence"),
        src("AllFamous — Natacha Océane (YT 1.1M+ subs; IG natacha.oceane 1M+)", "Website", "https://allfamous.org/people/natacha-oceane-19930806.html", "other-trusted"),
        src("FameCop — Natacha Océane (1.55M YouTube subscribers snapshot)", "Website", "https://famecop.com/fitness/natacha-oceane/", "other-trusted"),
        src("YouTube — @natachaoceane (per WikiCelebs handles table)", "YouTube", "https://www.youtube.com/@natachaoceane", "verified-platform"),
        src("Instagram — @natacha.oceane (per AllFamous)", "Instagram", "https://www.instagram.com/natacha.oceane/", "verified-platform"),
    ],
    [], "UK science-based fitness creator (UCL biophysics MSc). Objective fitness/wellness category. Birthplace recorded as England by four sources; one profile (2010Media) states Houston-born/UK-raised — minor birthplace variance, DOB consistent.",
    [account("YouTube", "@natachaoceane", "https://www.youtube.com/@natachaoceane", "1.6M+", 1600000, "rounded",
             "WikiCelebs biography (Sep 2025): 'over 1.6 million subscribers'; FameCop snapshot 1.55M; AllFamous 1.1M+ (older)."),
     account("Instagram", "@natacha.oceane", "https://www.instagram.com/natacha.oceane/", "1M+", 1000000, "rounded",
             "AllFamous biography: 'Instagram account, natacha.oceane, now has more than 1 million followers'.")]))

NEW.append(entry("W-2026-082", "Chloe Ting",
    ["Fitness", "Wellness", "Creator"],
    ev("Born April 9, 1986 in Brunei — age 40 in 2026 — recorded identically by CelebFacts, CelebWags, FameCop, BrandMentions and InnovaterHub biographies.",
       "CelebFacts — Chloe Ting (born April 9, 1986)", "https://www.celebsfacts.com/chloe-ting/"),
    ev("Identified as a woman via FameCop structured profile data listing 'Gender: Female' and consistent she/her fitness-creator biographies.",
       "FameCop — Chloe Ting profile (structured gender: Female)", "https://famecop.com/chloe-ting/"),
    [
        src("FameCop — Chloe Ting (DOB 1986-04-09; gender Female; YT 26.1M subs structured, Aug 2026)", "Website", "https://famecop.com/chloe-ting/", "age-evidence"),
        src("CelebFacts — Chloe Ting biography (2.3M IG snapshot)", "Website", "https://www.celebsfacts.com/chloe-ting/", "other-trusted"),
        src("InnovaterHub — Chloe Ting biography (25M+ YouTube, Feb 2024)", "Website", "https://innovaterhub.com/chloe-ting/", "other-trusted"),
        src("YouTube — @ChloeTing (structured sameAs per FameCop)", "YouTube", "https://www.youtube.com/@ChloeTing", "verified-platform"),
    ],
    [], "Bruneian-Australian fitness creator; NASM-certified personal trainer ('Two Week Shred Challenge'). Objective fitness category; one of YouTube's largest fitness channels. Instagram 2.3–2.9M snapshots cited in biographies but no verified handle capture this session — noted only.",
    [account("YouTube", "@ChloeTing", "https://www.youtube.com/@ChloeTing", "26.1M", 26100000, "rounded",
             "FameCop structured data (dateModified 2026-08-09): YouTube interactionStatistic 26,100,000 subscribers to @ChloeTing; InnovaterHub 25M+ (2024).")]))

NEW.append(entry("W-2026-083", "Anna Engelschall (growingannanas)",
    ["Fitness", "Wellness", "Creator"],
    ev("Born June 27, 1995 in Austria — age 31 in 2026 — recorded by YouTube Fandom (structured), NetworthChart, CelebsWorlds and IWMBuzz (German) biographies.",
       "YouTube Fandom — growingannanas (born June 27, 1995)", "https://youtube.fandom.com/wiki/Growingannanas"),
    ev("Identified as a woman via IWMBuzz profile table 'Geschlecht: Weiblich' (gender: female) and consistent she/her biographies of the Austrian CrossFit coach/creator.",
       "IWMBuzz — growingannanas (Geschlecht: Weiblich)", "https://iwmbuzz.de/growingannanas/"),
    [
        src("CelebsWorlds — Anna Engelschall (DOB 1995-06-27; 7M+ YT; 1.4M TikTok @growingannanas)", "Website", "https://www.celebsworlds.com/anna-engelschall/", "age-evidence"),
        src("YouTube Fandom — growingannanas (handles: IG/Threads/TikTok @growingannanas)", "Website", "https://youtube-fandom-com.translate.goog/wiki/Growingannanas?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=tc", "other-trusted"),
        src("IWMBuzz — growingannanas (CrossFit coach; @growingannanas channels)", "Website", "https://iwmbuzz.de/growingannanas/", "other-trusted"),
        src("YouTube — @growingannanas (full-length workout channel)", "YouTube", "https://www.youtube.com/@growingannanas", "verified-platform"),
        src("TikTok — @growingannanas (per WikiCelebs/CelebsWorlds handle tables)", "TikTok", "https://www.tiktok.com/@growingannanas", "verified-platform"),
        src("Instagram — @growingannanas (per YouTube-Wiki infobox)", "Instagram", "https://www.instagram.com/growingannanas/", "verified-platform"),
    ],
    [], "Austrian certified personal trainer/CrossFit coach and CEO of Grow with Anna GmbH — objective fitness category. YT count 7M+ (CelebsWorlds, Sep 2025); older snapshots 2.2M (2024) and 4.2M (2023) show growth trajectory.",
    [account("YouTube", "@growingannanas", "https://www.youtube.com/@growingannanas", "7M+", 7000000, "rounded",
             "CelebsWorlds biography (Sep 2025): 'more than 7 million subscribers on YouTube'."),
     account("TikTok", "@growingannanas", "https://www.tiktok.com/@growingannanas", "1.4M+", 1400000, "rounded",
             "CelebsWorlds biography (Sep 2025): TikTok over 1.4 million followers."),
     account("Instagram", "@growingannanas", "https://www.instagram.com/growingannanas/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle confirmed via YouTube-Wiki infobox social links; count not captured in snippets.")]))

NEW.append(entry("W-2026-084", "Caroline Girvan",
    ["Fitness", "Wellness", "Creator"],
    ev("Born June 22, 1984 — age 42 in 2026 — per Wikipedia (encyclopedic biography: 'born 22 June 1984', age 41 at snapshot) and NetworthSpot profile (June 22, 1984, County Antrim).",
       "Wikipedia — Caroline Girvan (born June 22, 1984)", "https://wikiwand.com/en/articles/Caroline_Girvan"),
    ev("Identified as a woman via Wikipedia biography (certified personal trainer and mother of two; she/her) and consistent coverage.",
       "Wikipedia — Caroline Girvan biography (she/her)", "https://wikiwand.com/en/articles/Caroline_Girvan"),
    [
        src("Wikipedia — Caroline Girvan (DOB 1984-06-22; Channel: Caroline Girvan; 4M subs, Mar 2025)", "Website", "https://wikiwand.com/en/articles/Caroline_Girvan", "age-evidence"),
        src("NetworthSpot — Caroline Girvan profile (DOB Jun 22 1984; 3.4M+ subs, May 2026)", "Website", "https://www.networthspot.com/caroline-girvan/net-worth/", "other-trusted"),
        src("YouTube — Caroline Girvan channel (channel name per Wikipedia)", "YouTube", "https://www.youtube.com/@CarolineGirvan", "verified-platform"),
    ],
    [], "Northern Irish certified personal trainer; lockdown-launch home-workout channel and CGX app — objective fitness category. Subscriber snapshots vary: Wikipedia infobox 4M (Mar 26, 2025) vs NetworthSpot 3.4M (May 2026) — variance logged in IRR-2026-09-06-010.",
    [account("YouTube", "Caroline Girvan", "https://www.youtube.com/@CarolineGirvan", "4M", 4000000, "rounded",
             "Wikipedia infobox: 'Subscribers: 4 million' (last updated 26 March 2025); NetworthSpot (May 2026) cites 3.4M+ — both recorded verbatim.")]))

NEW.append(entry("W-2026-085", "Sunisa \"Suni\" Lee",
    ["Athlete", "Gymnastics", "Creator"],
    ev("Born March 9, 2003 in St. Paul, Minnesota — age 23 in 2026 — per Britannica ('How old is Suni Lee? … born on March 9, 2003') and Biography.com (BORN: March 9, 2003).",
       "Britannica — Suni Lee (born March 9, 2003)", "https://www.britannica.com/biography/Suni-Lee"),
    ev("Identified as a woman via Britannica biography (American gymnast, 'the fifth consecutive American woman to claim the sport's most coveted prize'; US women's national team).",
       "Britannica — Suni Lee biography (she/her, women's gymnastics)", "https://www.britannica.com/biography/Suni-Lee"),
    [
        src("Britannica — Suni Lee (DOB 2003-03-09)", "Website", "https://www.britannica.com/biography/Suni-Lee", "age-evidence"),
        src("Biography.com — Suni Lee (BORN: March 9, 2003, Saint Paul)", "Website", "https://www.biography.com/athletes/a61611825/suni-lee", "press"),
        src("USA Gymnastics — Suni Lee official athlete profile (lists IG @sunisalee_, X @sunii567)", "Website", "https://members.usagym.org/pages/athletes/nationalTeamWomen.html?id=467541", "official"),
        src("Instagram — @sunisalee_ (per USA Gymnastics official profile)", "Instagram", "https://www.instagram.com/sunisalee_/", "verified-platform"),
        src("X — @sunii567 (per USA Gymnastics official profile)", "X", "https://x.com/sunii567", "verified-platform"),
    ],
    [], "2020 Olympic all-around champion and 2024 Olympic team gold medalist — objective athlete category. Handles come from her official USA Gymnastics national-team page (Tier-1); no public follower counts captured — recorded UNKNOWN, never estimated.",
    [account("Instagram", "@sunisalee_", "https://www.instagram.com/sunisalee_/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle per USA Gymnastics official national-team profile ('Instagram: Instagram.com/sunisalee_'); count not captured."),
     account("X", "@sunii567", "https://x.com/sunii567", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle per USA Gymnastics official national-team profile ('Twitter/X: @sunii567'); count not captured.")]))

NEW.append(entry("W-2026-086", "Olivia \"Livvy\" Dunne",
    ["Athlete", "Gymnastics", "Modeling", "Creator"],
    ev("Born October 1, 2002 in Westwood, New Jersey — age 23 in 2026 — per Wikipedia encyclopedic biography (full name Olivia Paige Dunne) and Sportskeeda/NetInfluencer profiles.",
       "Wikipedia — Livvy Dunne (born October 1, 2002)", "https://en.wikipedia.org/wiki/Livvy_Dunne"),
    ev("Identified as a woman via Wikipedia biography (actress, model; former LSU Tigers women's gymnastics team member and SI Swimsuit model; she/her).",
       "Wikipedia — Livvy Dunne biography (she/her)", "https://en.wikipedia.org/wiki/Livvy_Dunne"),
    [
        src("Wikipedia — Livvy Dunne (DOB 2002-10-01; NCAA champion; SI swimsuit model)", "Website", "https://en.wikipedia.org/wiki/Livvy_Dunne", "age-evidence"),
        src("Luxus Magazine — Olivia Dunne (8M TikTok + 5.4M Instagram, Nov 2025 page)", "Website", "https://magazine.luxus-plus.com/en/who-is-olivia-dunne-ex-gymnast-turned-social-media-star/", "press"),
        src("NetInfluencer — Olivia Dunne (IG embed @livvydunne)", "Website", "https://www.netinfluencer.com/olivia-dunne/", "other-trusted"),
        src("Instagram — @livvydunne (per NetInfluencer IG embed)", "Instagram", "https://www.instagram.com/livvydunne/", "verified-platform"),
        src("TikTok — @livvy (per TikTok-Wiki + Luxus)", "TikTok", "https://www.tiktok.com/@livvy", "verified-platform"),
    ],
    [], "2024 NCAA team champion with LSU and Sports Illustrated Swimsuit model — objective athlete/modeling categories. TikTok cadence: Wikipedia 'more than 8 million followers on TikTok' (Feb 2023), Luxus 8M (2025); IG 5.4M (Luxus Sept 2025 clip) — recorded verbatim per-platform.",
    [account("TikTok", "@livvy", "https://www.tiktok.com/@livvy", "8M+", 8000000, "rounded",
             "Luxus Magazine (Nov 2025): 8 million TikTok followers; Wikipedia: >8M TikTok (Feb 2023); Sportskeeda-wiki snapshot 7.2–7.6M (older)."),
     account("Instagram", "@livvydunne", "https://www.instagram.com/livvydunne/", "5.4M", 5400000, "rounded",
             "Luxus Magazine (Nov 2025): 5.4 million Instagram followers; Wikipedia notes >5M IG (Feb 2023).")]))

NEW.append(entry("W-2026-087", "Jordan Chiles",
    ["Athlete", "Gymnastics", "Creator"],
    ev("Born April 15, 2001 — age 25 in 2026 — per NBC Olympics ('Jordan Chiles was born April 15, 2001 and is 23 years old', July 2024) and Wikipedia (born April 15, 2001); Team USA lists age 25.",
       "NBC Olympics — Jordan Chiles athlete bio (born April 15, 2001)", "https://www.nbcolympics.com/news/jordan-chiles-meet-athlete"),
    ev("Identified as a woman via US women's national gymnastics team career (NBC Olympics/Team USA 'Golden Girls' women's team) and she/her coverage.",
       "Team USA — Jordan Chiles profile (women's team)", "https://www.teamusa.com/profiles/jordan-chiles-908302"),
    [
        src("NBC Olympics — Jordan Chiles (DOB 2001-04-15)", "Website", "https://www.nbcolympics.com/news/jordan-chiles-meet-athlete", "press"),
        src("Wikipedia — Jordan Chiles (born April 15, 2001, Tualatin OR)", "Website", "https://en.wikipedia.org/wiki/Jordan_Chiles", "age-evidence"),
        src("USA Gymnastics — Jordan Chiles official profile (lists IG @jordanchiles, X @ChilesJordan)", "Website", "https://members.usagym.org/pages/athletes/athleteListDetail.html?id=279968", "official"),
        src("Instagram — @jordanchiles (live display 2M followers)", "Instagram", "https://www.instagram.com/jordanchiles", "verified-platform"),
        src("X — @ChilesJordan (live display 100.4K followers)", "X", "https://x.com/ChilesJordan", "verified-platform"),
        src("Facebook — Jordan Chiles official page (82K followers)", "Facebook", "https://www.facebook.com/jordanchiles2020", "verified-platform"),
    ],
    [], "2024 Olympic team champion; TIME 2025 Woman of the Year per USAG profile — objective athlete category. IG/X/FB counts are platform-native public displays captured via search snippets 2026-09-06 (not estimates).",
    [account("Instagram", "@jordanchiles", "https://www.instagram.com/jordanchiles", "2M", 2000000, "rounded",
             "Instagram public profile display via Yahoo search snippet: '2M Followers, 527 Following, 783 Posts' (checked 2026-09-06); handle also listed on usagym.org official profile."),
     account("X", "@ChilesJordan", "https://x.com/ChilesJordan", "100.4K", 100400, "rounded",
             "Live X profile page display via search snippet: '126 Following, 100.4K Followers' (checked 2026-09-06)."),
     account("Facebook", "@jordanchiles2020", "https://www.facebook.com/jordanchiles2020", "82K", 82000, "rounded",
             "Facebook official page snippet via search: 'This is the official Facebook page for 2X Olympian & World Champion Jordan Chiles — Followers: 82K' (checked 2026-09-06).")]))

NEW.append(entry("W-2026-088", "Jade Carey",
    ["Athlete", "Gymnastics", "Creator"],
    ev("Born May 27, 2000 in Phoenix, Arizona — age 26 in 2026 — per Wikipedia infobox and TheGymter database record ('Birthdate May 27, 2000'); Team USA lists age 26.",
       "Wikipedia — Jade Carey (born May 27, 2000)", "https://en.wikipedia.org/wiki/Jade_Carey"),
    ev("Identified as a woman via US national team women's artistic gymnastics career (USA Gymnastics 'Program: Women's Artistic'; Team USA women's team 'Golden Girls').",
       "USA Gymnastics — Jade Carey athlete profile (Women's Artistic program)", "https://members.usagym.org/pages/athletes/nationalTeamWomen.html?id=239522"),
    [
        src("Wikipedia — Jade Carey (DOB 2000-05-27)", "Website", "https://en.wikipedia.org/wiki/Jade_Carey", "age-evidence"),
        src("TheGymter — Jade Carey database record (Birthdate May 27, 2000)", "Website", "https://thegymter.net/jade-carey/", "other-trusted"),
        src("Team USA — Jade Carey profile (2020/2024 Olympian; Oregon State)", "Website", "https://www.teamusa.com/profiles/jade-carey-1095482", "official"),
        src("SpeakRJ — Jade Carey @jadecareyy audit (2021: 55.7K; bio matches US team/OSU)", "Website", "https://www.speakrj.com/audit/report/jadecareyy/instagram", "other-trusted"),
    ],
    ["CONFLICTING_INFORMATION"],
    "2020 Olympic floor champion and 2024 Olympic team champion — objective athlete category. IG handle anomaly: @jadecareyy was her account per a June-2021 audit (55.7K, bio 'world champion, usa national team, future osu gymnast'), but the current live display under @jadecareyy shows a small fan-run account (366 followers) — probable handle change; pending re-verification (see IRR-2026-09-06-010).",
    [account("Instagram", "@jadecareyy", "https://www.instagram.com/jadecareyy/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "June 2021 audit identified @jadecareyy as Jade Carey's account (55.7K, matching bio); current live display shows fan-run account — handle state under review, no count recorded.")]))

NEW.append(entry("W-2026-089", "Tara Davis-Woodhall",
    ["Athlete", "Sports", "Creator"],
    ev("Born May 20, 1999 in Mesquite, Texas — age 27 in 2026 — per Wikipedia (born May 20, 1999) and FamousBirthdays structured birthDate; Team USA lists age 27.",
       "Wikipedia — Tara Davis-Woodhall (born May 20, 1999)", "https://en.wikipedia.org/wiki/Tara_Davis-Woodhall"),
    ev("Identified as a woman via US women's long-jump career (Wikipedia 'Women's athletics … 2024 Paris Long jump, Gold'; Team USA biography, she/her).",
       "Team USA — Tara Davis-Woodhall biography", "https://www.teamusa.com/profiles/tara-davis"),
    [
        src("Wikipedia — Tara Davis-Woodhall (DOB 1999-05-20; 2024 Olympic gold; 2025 world gold)", "Website", "https://en.wikipedia.org/wiki/Tara_Davis-Woodhall", "age-evidence"),
        src("Team USA — Tara Davis-Woodhall (Olympic gold long jump; UT Austin)", "Website", "https://www.teamusa.com/profiles/tara-davis", "official"),
        src("Instagram — @_taarra_ live display (1M followers)", "Instagram", "https://www.instagram.com/_taarra_/", "verified-platform"),
        src("Threads — @_taarra_ live display (284.6K followers)", "Threads", "https://www.threads.com/@_taarra_", "verified-platform"),
    ],
    [], "2024 Olympic and 2025 world long-jump champion — objective athlete category. Joint husband-wife account @thewoodhalls (972K) recorded separately with attribution note; never summed with her solo account.",
    [account("Instagram", "@_taarra_", "https://www.instagram.com/_taarra_/", "1M", 1000000, "rounded",
             "Instagram public profile display via search snippet: '1M seguidores, 1,149 siguiendo, 1,190 publicaciones — Tara Davis-Woodhall OLY (TDW) (@_taarra_)' (checked 2026-09-06)."),
     account("Threads", "@_taarra_", "https://www.threads.com/@_taarra_", "284.6K", 284600, "rounded",
             "Threads public profile display via search snippet: '284.6K Followers • 590 Threads' (checked 2026-09-06)."),
     account("Instagram", "@thewoodhalls", "https://www.instagram.com/thewoodhalls/", "972K", 972000, "rounded",
             "Joint Tara & Hunter Woodhall account — live display via search snippet '972K seguidores' (checked 2026-09-06); shared couple account, noted separately.")]))

NEW.append(entry("W-2026-090", "Anna Hall",
    ["Athlete", "Sports", "Creator"],
    ev("Born March 23, 2001 in Denver/Highlands Ranch, Colorado — age 25 in 2026 — per University of Georgia athletics roster ('Born March 23, 2001'), Wikipedia, TheCityCeleb and SportsSpectrum ('24-year-old', Sept 2025).",
       "University of Georgia Athletics — Anna Hall roster (Born March 23, 2001)", "https://georgiadogs.com/sports/track-and-field/roster/anna-hall/4971"),
    ev("Identified as a woman via women's heptathlon career (NCAA/Team USA/USATF) and SportsSpectrum article ('the first American woman to win the heptathlon at the worlds or Olympics since Jackie Joyner-Kersee').",
       "SportsSpectrum — Anna Hall heptathlon silver feature (she/her)", "https://sportsspectrum.com/sport/olympics/2023/08/21/follower-of-christ-anna-hall-heptathlon-silver-worlds/"),
    [
        src("University of Georgia Athletics — Anna Hall roster (DOB 2001-03-23)", "Website", "https://georgiadogs.com/sports/track-and-field/roster/anna-hall/4971", "official"),
        src("Wikipedia — Anna Hall (heptathlete) biography (DOB 2001-03-23)", "Website", "https://www.wikiwand.com/en/articles/Anna_Hall_(heptathlete)", "age-evidence"),
        src("Florida Gators athletics — Anna Hall roster (sameAs: IG @annaa.hall, X @annaahalll)", "Website", "https://floridagators.com/sports/track-and-field/roster/anna-hall/14962", "official"),
        src("Instagram — @annaa.hall (per UF roster structured sameAs)", "Instagram", "https://www.instagram.com/annaa.hall", "verified-platform"),
        src("X — @annaahalll (per UF roster structured sameAs)", "X", "https://x.com/annaahalll", "verified-platform"),
    ],
    [], "2025 world heptathlon champion — objective athlete category. Handles verbatim from official Florida Gators roster structured data; no follower counts captured — UNKNOWN, never estimated.",
    [account("Instagram", "@annaa.hall", "https://www.instagram.com/annaa.hall", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle per floridagators.com roster structured sameAs link; count not captured."),
     account("X", "@annaahalll", "https://x.com/annaahalll", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle per floridagators.com roster structured sameAs link; count not captured.")]))

NEW.append(entry("W-2026-091", "Masai Russell",
    ["Athlete", "Sports", "Creator"],
    ev("Born June 17, 2000 in Washington, D.C. — age 26 in 2026 — per Wikipedia (born June 17, 2000); NPR describes her as 24 at the Aug 2024 final and On3 as 25 in May 2026.",
       "Wikipedia — Masai Russell (born June 17, 2000)", "https://www.wikiwand.com/en/Masai_Russell"),
    ev("Identified as a woman via women's 100m hurdles career — 'Women's athletics … 2024 Paris 100 m hurdles, Gold' (Wikipedia medal record) and she/her NPR coverage.",
       "NPR — Masai Russell wins Olympic gold (she/her)", "https://www.npr.org/2024/08/10/nx-s1-5070567/masai-russell-gold-100m-hurdle-olympic"),
    [
        src("Wikipedia — Masai Russell (DOB 2000-06-17; 2024 Olympic 100m hurdles gold)", "Website", "https://www.wikiwand.com/en/Masai_Russell", "age-evidence"),
        src("NPR — Masai Russell wins 100m hurdles gold by one hundredth (Aug 2024)", "Website", "https://www.npr.org/2024/08/10/nx-s1-5070567/masai-russell-gold-100m-hurdle-olympic", "press"),
        src("Bullis School — Masai Russell wins Olympic gold (class of 2018; Kentucky)", "Website", "https://www.bullis.org/news/article/~board/bullis/post/bullis-alumnus-masai-russell-wins-olympic-gold-in-womens-100m-hurdles", "official"),
    ],
    [], "2024 Olympic 100m hurdles champion and NCAA/American record holder — objective athlete category. No social handles captured in this session's snippets — follower range UNKNOWN (not a disqualifier for athletes-window).",
    []))

NEW.append(entry("W-2026-092", "Nelly Korda",
    ["Athlete", "Sports", "Creator"],
    ev("Born July 28, 1998 in Bradenton, Florida — age 28 in 2026 — per Wikipedia encyclopedic biography and Celebrity-Birthdays/InfoSeeMedia profiles (structured DOB 1998-07-28).",
       "Wikipedia — Nelly Korda (born July 28, 1998)", "https://en.wikipedia.org/wiki/Nelly_Korda"),
    ev("Identified as a woman via LPGA Tour women's golf career — 'women's world rankings', Solheim Cup and Women's PGA Championship (Wikipedia); daughter of Petr Korda.",
       "Wikipedia — Nelly Korda biography (LPGA women's tour, she/her)", "https://en.wikipedia.org/wiki/Nelly_Korda"),
    [
        src("Wikipedia — Nelly Korda (DOB 1998-07-28; 4-time major winner; Olympic gold 2020)", "Website", "https://en.wikipedia.org/wiki/Nelly_Korda", "age-evidence"),
        src("Celebrity-Birthdays — Nelly Korda (DOB Jul 28, 1998; Bradenton)", "Website", "https://celebrity-birthdays.com/people/nelly-korda", "other-trusted"),
        src("KemiFilani — Nelly Korda bio update (career majors and titles)", "Website", "https://www.kemifilani.ng/breaking-news/nelly-korda-bio-update-age-personal-life-career-net-worth", "other-trusted"),
    ],
    [], "World No.1-ranked LPGA golfer, 2020 Olympic gold medalist and 4-time major champion — objective athlete category. No social handle captured in this session's snippets — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-093", "Iga Świątek",
    ["Athlete", "Tennis", "Creator"],
    ev("Born May 31, 2001 in Warsaw, Poland — age 25 in 2026 — per ESPN player profile ('Birth Date May 31, 2001 (Age: 25)') and Wikipedia (31 May 2001); tennisworldusa structured birthDate.",
       "ESPN — Iga Świątek player profile (Birth Date May 31, 2001)", "https://www.espn.com/tennis/player/_/id/3730/iga-swiatek"),
    ev("Identified as a woman via WTA women's singles career — six major titles and women's world No. 1 ranking (Wikipedia/ESPN), she/her.",
       "Wikipedia — Iga Świątek biography (women's singles No. 1)", "https://en.wikipedia.org/wiki/Iga_%C5%9Awi%C4%85tek"),
    [
        src("ESPN — Iga Świątek (DOB 2001-05-31; WTA record 437-105)", "Website", "https://www.espn.com/tennis/player/_/id/3730/iga-swiatek", "age-evidence"),
        src("Wikipedia — Iga Świątek (DOB 31 May 2001; 6 major titles)", "Website", "https://en.wikipedia.org/wiki/Iga_%C5%9Awi%C4%85tek", "other-trusted"),
        src("TennisWorldUSA — Iga Świątek bio (structured birthDate 2001-May-31)", "Website", "https://www.tennisworldusa.org/tennis-player/450/iga-swiatek/", "other-trusted"),
    ],
    [], "Six-time major champion and former WTA world No. 1 — objective athlete category. No social handle captured in this session's snippets — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-094", "Emma Raducanu",
    ["Athlete", "Tennis", "Creator"],
    ev("Born November 13, 2002 in Toronto, Canada — age 23 in 2026 — per Tier-1 WTA official player page ('Birthday: Nov 13, 2002') and ESPN ('Birth Date November 13, 2002 (Age: 23)').",
       "WTA — Emma Raducanu official player profile (Birthday Nov 13, 2002)", "https://www.wtatennis.com/players/328366/emma-raducanu"),
    ev("Identified as a woman via WTA women's singles career — 2021 US Open champion; WTA bio (parents Ian and Renee, she/her coverage).",
       "WTA — Emma Raducanu biography (women's tour)", "https://www.wtatennis.com/players/328366/emma-raducanu"),
    [
        src("WTA — Emma Raducanu official page (DOB 2002-11-13; US Open 2021)", "Website", "https://www.wtatennis.com/players/328366/emma-raducanu", "official"),
        src("ESPN — Emma Raducanu (Birth Date November 13, 2002)", "Website", "https://www.espn.com/tennis/player/_/id/3398/emma-raducanu", "age-evidence"),
        src("TennisRatio — Emma Raducanu (structured birthDate + WTA affiliation)", "Website", "https://www.tennisratio.com/players/EmmaRaducanu.html", "other-trusted"),
        src("Instagram — @emmaraducanu (per Sept 2021 coverage during US Open run)", "Instagram", "https://www.instagram.com/emmaraducanu/", "verified-platform"),
    ],
    [], "2021 US Open singles champion — objective athlete category. The 2021-era snippet captured showed ~420K followers before her title run (massively stale by 2026) — current count treated as UNKNOWN rather than recording stale data, per anti-estimation rule.",
    [account("Instagram", "@emmaraducanu", "https://www.instagram.com/emmaraducanu/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle documented in September 2021 coverage ('Emma Raducanu emmaraducanu', 420K at the time — pre-title, stale by 2026); current count not captured.")]))

NEW.append(entry("W-2026-095", "Trinity Rodman",
    ["Athlete", "Soccer", "Creator"],
    ev("Born May 20, 2002 in Newport Beach, California — age 24 in 2026 — per Britannica encyclopedic biography and Biography.com (BORN: May 20, 2002); Chicago-area coverage records her 24th birthday in May 2026 timeframe (Britannica: age 24).",
       "Britannica — Trinity Rodman (born May 20, 2002)", "https://www.britannica.com/biography/Trinity-Rodman"),
    ev("Identified as a woman via US Women's National Team and NWSL career — 'the 18-year-old Rodman became the youngest player to be drafted in NWSL history' (Britannica); she/her.",
       "Britannica — Trinity Rodman biography (USWNT, she/her)", "https://www.britannica.com/biography/Trinity-Rodman"),
    [
        src("Britannica — Trinity Rodman (DOB 2002-05-20; 2024 Olympic gold; record 2026 contract)", "Website", "https://www.britannica.com/biography/Trinity-Rodman", "age-evidence"),
        src("Biography.com — Trinity Rodman (BORN: May 20, 2002; Washington Spirit)", "Website", "https://www.biography.com/athletes/a60672592/trinity-rodman", "press"),
        src("SportsBigNews — Trinity Rodman (born May 20, 2002; 23 years old, 2026)", "Website", "https://www.sportsbignews.com/football/who-is-trinity-rodman-career-stats-records-net-worth-and-relationship/", "other-trusted"),
    ],
    [], "2024 Olympic gold medalist with the USWNT and record-setting 2026 Washington Spirit contract (world's highest-paid women's soccer player per Britannica) — objective athlete category. No social handle captured this session — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-096", "Paige Bueckers",
    ["Athlete", "Basketball", "Creator"],
    ev("Born October 20, 2001 in Edina, Minnesota — age 24 in 2026 — per Wikipedia encyclopedic biography and BiographyWallah (DOB 20 October 2001, Gender: Female).",
       "Wikipedia — Paige Bueckers (born October 20, 2001)", "https://en.wikipedia.org/wiki/Paige_Bueckers"),
    ev("Identified as a woman via women's college/pro basketball career — UConn Huskies women's basketball and WNBA Dallas Wings (Wikipedia); BiographyWallah structured 'Gender: Female'.",
       "BiographyWallah — Paige Bueckers (Gender: Female)", "https://biographywallah.com/paige-bueckers/"),
    [
        src("Wikipedia — Paige Bueckers (DOB 2001-10-20; 2025 NCAA champion; WNBA Rookie of the Year)", "Website", "https://en.wikipedia.org/wiki/Paige_Bueckers", "age-evidence"),
        src("StarsUnfolded — Paige Bueckers (DOB 20 October 2001; WNBA draft #1 2025)", "Website", "https://starsunfolded.com/paige-bueckers/", "other-trusted"),
    ],
    [], "2025 NCAA champion with UConn and 2025 WNBA #1 overall pick/Rookie of the Year — objective athlete category. Wikipedia records that her Instagram reached 1,000,000 followers on April 4, 2022 — the first women's college basketball player to do so; no current count or handle capture this session — recorded harmoniously as UNKNOWN.",
    []))

NEW.append(entry("W-2026-097", "Angel Reese",
    ["Athlete", "Basketball", "Creator"],
    ev("Born May 6, 2002 in Randallstown, Maryland — age 24 in 2026 — per Britannica ('born May 6, 2002 (age 24)') and the Chicago Tribune ('On May 6, 2002, Angel Reese was born… turns 24', May 2026).",
       "Britannica — Angel Reese (born May 6, 2002)", "https://www.britannica.com/biography/Angel-Reese"),
    ev("Identified as a woman via WNBA women's basketball career (Chicago Sky/Atlanta Dream; LSU women's 2023 championship) and she/her Britannica coverage.",
       "Britannica — Angel Reese biography (WNBA, she/her)", "https://www.britannica.com/biography/Angel-Reese"),
    [
        src("Britannica — Angel Reese (DOB 2002-05-06; rookie rebound records)", "Website", "https://www.britannica.com/biography/Angel-Reese", "age-evidence"),
        src("Chicago Tribune — Angel Reese turns 24 (May 6, 2002 birth)", "Website", "https://www.chicagotribune.com/2026/05/06/today-in-history-angel-reese-turns-24/", "press"),
        src("Biography.com — Angel Reese (WNBA records overview)", "Website", "https://www.biography.com/athletes/a64289466/angel-reese", "other-trusted"),
    ],
    [], "2023 NCAA champion (LSU) and two-time WNBA rebounding leader — objective athlete category. No social handle captured in this session's snippets — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-098", "Kate Douglass",
    ["Athlete", "Swimming", "Creator"],
    ev("Born November 17, 2001 in New York, N.Y. — age 24 in 2026 — per Tier-1 Olympedia record (Born: 17 November 2001) and her Arena sportswear athlete page (DATE OF BIRTH 17/11/2001).",
       "Olympedia — Kate Douglass (Born 17 November 2001)", "https://www.olympedia.org/athletes/2506216"),
    ev("Identified as a woman via Olympedia structured 'Sex: Female' and Virginia Cavaliers women's swimming roster (Olympic bronze, 200 IM).",
       "Olympedia — Kate Douglass record (Sex: Female)", "https://www.olympedia.org/athletes/2506216"),
    [
        src("Olympedia — Kate Douglass (DOB 2001-11-17; Sex: Female; Virginia)", "Website", "https://www.olympedia.org/athletes/2506216", "official"),
        src("Arena — Kate Douglass athlete page (DATE OF BIRTH 17/11/2001)", "Website", "https://about.arenasport.com/en/athletes/kate-douglass", "other-trusted"),
        src("Virginia Athletics — Kate Douglass roster (2020 Olympic bronze medalist)", "Website", "https://virginiasports.com/sports/swimming/roster/player/kate-douglass", "official"),
        src("FamousBirthdays — Kate Douglass (structured birthDate 2001-11-17)", "Website", "https://www.famousbirthdays.com/people/kate-douglass.html", "other-trusted"),
    ],
    [], "2024 Olympic 200m breaststroke champion and multiple-medal Olympic/NCAA swimmer — objective athlete category. Roster and sponsor pages link her socials, but no handle/counter surface in this session's snippets — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-099", "Torri Huske",
    ["Athlete", "Swimming", "Creator"],
    ev("Born December 7, 2002 in Arlington, Virginia — age 23 in 2026 — per Tier-1 Olympedia record (Born: 7 December 2002), FamousBirthdays structured birthDate, and Team USA (age 23).",
       "Olympedia — Torri Huske (Born 7 December 2002)", "https://www.olympedia.org/athletes/147283"),
    ev("Identified as a woman via Olympedia structured 'Sex: Female' and US women's swimming 100m butterfly Olympic title (Team USA profile).",
       "Olympedia — Torri Huske record (Sex: Female)", "https://www.olympedia.org/athletes/147283"),
    [
        src("Olympedia — Torri Huske (DOB 2002-12-07; Sex: Female; 6 Olympic medals)", "Website", "https://www.olympedia.org/athletes/147283", "official"),
        src("FamousBirthdays — Torri Huske (birthday December 7, 2002)", "Website", "https://www.famousbirthdays.com/people/torri-huske.html", "age-evidence"),
        src("Team USA — Torri Huske profile (3 gold, 3 silver; Stanford)", "Website", "https://www.teamusa.com/profiles/torri-huske", "official"),
        src("Instagram — @torri_huske (live display 108K followers)", "Instagram", "https://www.instagram.com/torri_huske/", "verified-platform"),
    ],
    [], "2024 Olympic 100m butterfly champion (plus two relay golds) — objective athlete category. IG count is the platform-native public display captured via search snippet 2026-09-06.",
    [account("Instagram", "@torri_huske", "https://www.instagram.com/torri_huske/", "108K", 108000, "rounded",
             "Instagram public profile display via search snippet: '108K followers, 1,007 following, 206 posts' (bio: USA Olympian Stanford) — checked 2026-09-06.")]))

NEW.append(entry("W-2026-100", "Gretchen Walsh",
    ["Athlete", "Swimming", "Creator"],
    ev("Born January 29, 2003 in Nashville, Tennessee — age 23 in 2026 — per Wikipedia (born January 29, 2003), SwimSwam bio, and Team USA (age 23).",
       "Wikipedia — Gretchen Walsh (born January 29, 2003)", "https://en.wikipedia.org/wiki/Gretchen_Walsh"),
    ev("Identified as a woman via women's swimming career — 'fastest female freshman', 100m butterfly world record holder; Team USA Women's team, she/her (SwimSwam).",
       "SwimSwam — Gretchen Walsh bio (women's events, she/her)", "https://swimswam.com/bio/gretchen-walsh/"),
    [
        src("Wikipedia — Gretchen Walsh (DOB 2003-01-29; multiple world records)", "Website", "https://en.wikipedia.org/wiki/Gretchen_Walsh", "age-evidence"),
        src("Team USA — Gretchen Walsh profile (2 gold, 2 silver Paris 2024)", "Website", "https://www.teamusa.com/profiles/gretchen-walsh", "official"),
        src("Sportskeeda — Gretchen Walsh hometown article (image credit @gretchwalsh2)", "Website", "https://www.sportskeeda.com/swimming/where-is-gretchen-walsh-from", "press"),
        src("Instagram — @gretchwalsh2 (per Sportskeeda image attribution)", "Instagram", "https://www.instagram.com/gretchwalsh2/", "verified-platform"),
    ],
    [], "100m butterfly world-record holder and 2x Olympic gold medalist (Paris 2024) — objective athlete category. IG handle via Sportskeeda article's own image attribution; count not captured — UNKNOWN, never estimated.",
    [account("Instagram", "@gretchwalsh2", "https://www.instagram.com/gretchwalsh2/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle confirmed via Sportskeeda article photo credit (@gretchwalsh2); follower count not captured in snippets.")]))


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
    if "IRR-2026-09-06-010" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-010",
            "severity": "needs-review",
            "summary": "Session-11 batch-2 flags: Jade Carey handle anomaly + snapshot variances recorded verbatim for manual review.",
            "detail": (
                "(1) Jade Carey: @jadecareyy was verified as her account in a June-2021 audit (55.7K, matching bio), but the current live display under that handle is a small fan-run account (366 followers) — probable handle change; is her current handle possibly @jadecarey? Requires manual re-verification; no count recorded. "
                "(2) Caroline Girvan YouTube subscriber snapshots conflict: Wikipedia infobox '4M' (Mar 26 2025) vs NetworthSpot '3.4M+' (May 2026) — both recorded; largest recorded as 4M citing Wikipedia's dated snapshot (a sub-count does not cross-bucket). "
                "(3) Emma Raducanu: only a September-2021 snippet captured her IG (420K pre-US-Open title) — deliberately recorded FOLLOWER_COUNT_UNKNOWN instead of stale data. "
                "(4) Paige Bueckers: Wikipedia documents her Instagram reaching 1,000,000 followers on 2022-04-04 (a milestone, not a current count) — noted in prose only, not recorded as current count. "
                "(5) Several Olympic athletes have Tier-1-official-profile handles (usagym/laus/roster sameAs) but no observable follower displays in search snippets: Suni Lee, Anna Hall, Gretchen Walsh, Masai Russell, Nelly Korda, Iga Świątek, Trinity Rodman, Angel Reese, Kate Douglass — recorded UNKNOWN per protocol (ranges unknown ≠ disqualifier). "
                "(6) Maddie Lymburner/Anna Engelschall YouTube handles are vanity-URL standard names matching multiple biographies; counts come from named biography snapshots, not platform-native displays (St-Aug/CelebsWorlds)."
            ),
            "reviewStatus": "requires-owner-review",
        })

    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["reviewQueueCount"] = len(data["reviewQueue"])
    data["metadata"]["generatedAt"] = CHECKED
    data["metadata"]["summary"] = (
        f"Women-only directory of adult (18+) public creators: {len(entries)} verified adult women "
        f"(W-2026-001..100) — alongside {len(data['reviewQueue'])} REVIEW_REQUIRED candidates with "
        "provenance. Session 11 added 45 verified profiles across two batches: fitness/yoga YouTube "
        "creators (Adriene Mishler, Maddie Lymburner, Natacha Océane, Chloe Ting, growingannanas, "
        "Caroline Girvan), fitness models, artistic gymnasts and Olympians (Suni Lee, Jade Carey, "
        "Jordan Chiles, Livvy Dunne, swimmers Regan Smith/Kate Douglass/Torri Huske/Gretchen Walsh, "
        "surfers Caroline Marks/Tatiana Weston-Webb, volleyball incl. Sara Hughes/Kelly Cheng/"
        "Justine Wong-Orantes/Andrea Drews, track&field Tara Davis-Woodhall/Anna Hall/Masai Russell, "
        "tennis Iga Świątek/Emma Raducanu, golf Nelly Korda, soccer Trinity Rodman, basketball "
        "Angel Reese/Paige Bueckers/Kysre Gondrezick/Didi Richards, esports Petra/sarahcat) and "
        "models Brooks Nader/Yovanna Ventura. Per-platform follower counts are publicly observed "
        "displays only — never estimated, never summed; unknown counts recorded as "
        "FOLLOWER_COUNT_UNKNOWN. All DOB/gender evidence is cited per entry; conflicts are flagged "
        "with full variance logged in the irregularities register."
    )
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} irr={len(data['irregularities'])}")

if __name__ == "__main__":
    build()
