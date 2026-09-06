#!/usr/bin/env python3
"""Session 11 batch 1 (2026-09-06): 23 verified adds across fitness, volleyball,
esports, surfing, basketball, beach volleyball, SI-modeling and swimming.

Every row was verified this session against URLs returned by live searches:
DOB/age evidence (>=2 independent sources, or a Tier-1 official/encyclopedic
source), gender evidence, identity/handle chain, objective category, and
publicly displayed follower counts recorded verbatim (never estimated, never
summed). IB-batch assertion blocks prevent duplicate ids/names/URLs.
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

NEW.append(entry("W-2026-056", "Anllela Sagra",
    ["Fitness", "Fitness Model", "Creator"],
    ev("Born October 6, 1993 in Medellín, Colombia — age 32 in 2026. DOB recorded identically by NewsUnzip, JustBiography, Swagsy, CliveHealth and VrGyani biographies.",
       "NewsUnzip — Anllela Sagra (born October 6, 1993)", "https://www.newsunzip.com/wiki/anllela-sagra/"),
    ev("Identified as a woman via consistent she/her biographies — described as 'Colombia's first female fitness model' (Swagsy); sister Laura Sagra.",
       "Swagsy — Anllela Sagra fitness-model biography (she/her)", "https://swagsy.in/fitness-models/anllela-sagra-fitness-model/"),
    [
        src("CliveHealth — Anllela Sagra bio (DOB 1993-10-06; IG 27.1M, YT 400K+)", "Website", "https://www.clivehealth.com/anllela-sagra-biography-age-net-worth-married-salary-height-weight-dating-and-fitness-journey/", "age-evidence"),
        src("NewsUnzip — Anllela Sagra wiki (DOB October 6, 1993, Medellín)", "Website", "https://www.newsunzip.com/wiki/anllela-sagra/", "other-trusted"),
        src("Swagsy — Anllela Sagra: Colombia's first female fitness model", "Website", "https://swagsy.in/fitness-models/anllela-sagra-fitness-model/", "other-trusted"),
        src("Instagram — @anllela_sagra (fitness model)", "Instagram", "https://www.instagram.com/anllela_sagra/", "verified-platform"),
    ],
    [], "Discovered via famousbio.net Instagram-fitness-model directory this session. Category fitness/model — objective (personal trainer, 1Up Nutrition athlete, YouTube workouts). DOB and identity consistent across 5 independent biographies.",
    [account("Instagram", "@anllela_sagra", "https://www.instagram.com/anllela_sagra/", "27.1M", 27100000, "rounded",
             "CliveHealth biography social-media table: Instagram 27.1M followers (checked 2026-09-06)."),
     account("YouTube", "Anllela Sagra", "https://www.youtube.com/@anllela_sagra", "400K+", 400000, "rounded",
             "CliveHealth/Swagsy biographies: 400K+ YouTube subscribers.")]))

NEW.append(entry("W-2026-057", "Katya Elise Henry",
    ["Fitness", "Fitness Model", "Creator", "Fashion"],
    ev("Born June 14, 1994 in Minneapolis, Minnesota — age 32 in 2026. DOB recorded identically by TheFamousPeople, UpdatesTM, Legit.ng, MetroBiography and NBAwags.",
       "TheFamousPeople — Katya Elise Henry (birthday June 14, 1994)", "https://www.thefamouspeople.com/profiles/katya-elise-henry-32504.php"),
    ev("Identified as a woman via structured bio data 'Gender: Female' (Legit.ng) and consistent she/her fitness-model profiles across five sources.",
       "Legit.ng — Katya Elise Henry profile (Gender: Female)", "https://www.legit.ng/ask-legit/biographies/1473942-katya-elise-henrys-biography-tyler-herros-girlfriend/"),
    [
        src("TheFamousPeople — Katya Elise Henry (DOB June 14, 1994; family details)", "Website", "https://www.thefamouspeople.com/profiles/katya-elise-henry-32504.php", "age-evidence"),
        src("UpdatesTM — Katya Elise Henry (DOB 1994-06-14; IG @katyaelisehenry 7.8M)", "Website", "https://updatestm.com/katya-elise-henry/", "other-trusted"),
        src("Legit.ng — Katya Elise Henry (Gender: Female; IG 7.5M+ June 2025)", "Website", "https://www.legit.ng/ask-legit/biographies/1473942-katya-elise-henrys-biography-tyler-herros-girlfriend/", "press"),
        src("Instagram — @katyaelisehenry (workouts, WBK FIT)", "Instagram", "https://www.instagram.com/katyaelisehenry/", "verified-platform"),
    ],
    [], "Discovered via fitness-creator directory this session. Category fitness/model — objective: Workouts by Katya / WBK FIT founder, EHPlabs ambassador; also founded Kiss My Peach Swimwear (Fashion noted). Secondary IG @workouts_by_her (~497K) listed by UpdatesTM but not separately catalogued.",
    [account("Instagram", "@katyaelisehenry", "https://www.instagram.com/katyaelisehenry/", "7.8M", 7800000, "rounded",
             "UpdatesTM biography (May 2026): 'over 7.8 million followers on her main account @katyaelisehenry' (Legit.ng listed 7.5M+ June 2025).")]))

NEW.append(entry("W-2026-058", "Amanda Elise Lee",
    ["Fitness", "Fitness Model", "Creator", "Modeling"],
    ev("Born December 13, 1986 in Canada — age 39 in 2026. DOB recorded identically by BiographyPedia, Dreshare, WomanMagazine and the famousbio.net directory.",
       "BiographyPedia — Amanda Elise Lee (born December 13, 1986)", "https://biographypedia.org/who-is-amanda-lee-wiki-age-height-boyfriend-family-facts/"),
    ev("Identified as a woman via structured bio data 'Gender: Female' (BiographyPedia profile table) and consistent she/her fitness-model biographies.",
       "BiographyPedia — Amanda Lee profile table (Gender: Female)", "https://biographypedia.org/who-is-amanda-lee-wiki-age-height-boyfriend-family-facts/"),
    [
        src("BiographyPedia — Amanda Elise Lee (DOB 1986-12-13; Gender: Female; IG 11M+)", "Website", "https://biographypedia.org/who-is-amanda-lee-wiki-age-height-boyfriend-family-facts/", "age-evidence"),
        src("Dreshare — Amanda Elise Lee wiki (DOB December 13, 1986)", "Website", "https://www.dreshare.com/amanda-elise-lee-wiki/", "other-trusted"),
        src("WomanMagazine — Amanda Elise Lee (@amandaeliselee 12M snapshot; FB @amandaleefit 775K+)", "Website", "https://www.womanmagazine.com/who-is-amanda-elise-lee-instagram-dating-bio/", "other-trusted"),
        src("Instagram — @amandaeliselee (trainer/Pilates instructor)", "Instagram", "https://www.instagram.com/amandaeliselee/", "verified-platform"),
    ],
    [], "Discovered via famousbio.net Instagram-fitness-model directory. Certified personal trainer and Pilates instructor — objective fitness category. IG count 11M+ (BiographyPedia 2024) recorded; older 12M snapshot (WomanMagazine 2021) cited.",
    [account("Instagram", "@amandaeliselee", "https://www.instagram.com/amandaeliselee/", "11M+", 11000000, "rounded",
             "BiographyPedia (2024): 'more than 11 million followers' on Instagram; WomanMagazine (2021) listed 12M — snapshots differ."),
     account("Facebook", "@amandaleefit", "https://www.facebook.com/amandaleefit", "775K+", 775000, "rounded",
             "WomanMagazine biography: Facebook @amandaleefit over 775,000 followers.")]))

NEW.append(entry("W-2026-059", "Mia Sand (Miss Mia Fit)",
    ["Fitness", "Fitness Model", "Creator"],
    ev("Born October 11, 1987 in Copenhagen, Denmark — age 38 in 2026 — per BiographyTribune and TheCityCeleb (structured birthDate 1987-10-11). Note: Ithy article cites 1988 as an alternative year — conflict logged, adult either way.",
       "TheCityCeleb — Mia Sand bio (born October 11, 1987)", "https://www.thecityceleb.com/biography/personality/model/mia-sand-biography-age-husband-children-net-worth-height-career-instagram/"),
    ev("Identified as a woman via consistent she/her fitness-model biographies — Danish fitness model and personal trainer, mother of two (TheCityCeleb structured family data).",
       "BiographyTribune — Mia Sand wiki (she/her, Miss Mia Fit)", "https://biographytribune.com/mia-sands-wiki-biography-age-height-pregnant-husband/"),
    [
        src("TheCityCeleb — Mia Sand bio (DOB 1987-10-11; @missmiafit; 2.5M+ IG)", "Website", "https://www.thecityceleb.com/biography/personality/model/mia-sand-biography-age-husband-children-net-worth-height-career-instagram/", "age-evidence"),
        src("BiographyTribune — Mia Sand wiki (DOB 11 October 1987, Denmark)", "Website", "https://biographytribune.com/mia-sands-wiki-biography-age-height-pregnant-husband/", "other-trusted"),
        src("Pinterest-captured Instagram display — Mia Sand @missmiafit (2M followers, Oct 2024)", "Website", "https://www.pinterest.com/pin/miss-mia-sand--922956517379143270/", "other-trusted"),
        src("Instagram — @missmiafit ('Bodybuilding, Health nerd')", "Instagram", "https://www.instagram.com/missmiafit/", "verified-platform"),
    ],
    ["CONFLICTING_INFORMATION"],
    "Discovered via famousbio.net Instagram-fitness-model directory. Objective fitness category (online fitness school, Sand Fitness coaching). DOB-year conflict 1987 (two structured bios) vs 1988 (Ithy) recorded but adult unaffected.",
    [account("Instagram", "@missmiafit", "https://www.instagram.com/missmiafit/", "2M", 2000000, "rounded",
             "Instagram public display captured Oct 2024 (Pinterest mirror): '2M Followers, 167 Following, 1,478 Posts'; TheCityCeleb biography states 2.5M+ — latest bio higher; both cited.")]))

NEW.append(entry("W-2026-060", "Dee Marie Ditt",
    ["Fitness", "Fitness Model", "Creator"],
    ev("Born October 10, 1994 — age 31 in 2026 — per FamousBirthdays structured profile (birthDate 1994-10-10; WBFF titles dated 2023–2025 corroborate an adult competition timeline).",
       "FamousBirthdays — Dee Marie Ditt (birthDate 1994-10-10)", "https://www.famousbirthdays.com/people/dee-ditt.html"),
    ev("Identified as a woman via she/her biography ('She is an entrepreneur and businesswoman… founder of DMD Coaching') and WBFF women's division titles (Miss Bikini USA 2023).",
       "FamousBirthdays — Dee Marie Ditt biography (she/her)", "https://www.famousbirthdays.com/people/dee-ditt.html"),
    [
        src("FamousBirthdays — Dee Marie Ditt (DOB 1994-10-10; IG @deemariedi 470K+)", "Website", "https://www.famousbirthdays.com/people/dee-ditt.html", "age-evidence"),
        src("IDCrawl — TikTok @deemariedi (WBFF MISS FITNESS WORLDS '24 / MISS BIKINI USA '23; 41K)", "Website", "https://www.idcrawl.com/dee-marie", "other-trusted"),
        src("Instagram — @deemariedi (linked via FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/deemariedi", "verified-platform"),
        src("TikTok — @deemariedi (WBFF title in bio, links IG)", "TikTok", "https://www.tiktok.com/@deemariedi", "verified-platform"),
    ],
    [], "Discovered via FamousBirthdays WBFF fitness creator profile. Objective category: WBFF Miss Bikini USA 2023, Miss Fitness World Champion 2024; DMD Coaching founder. Identity: FamousBirthdays sameAs ↔ TikTok bio title string match.",
    [account("Instagram", "@deemariedi", "https://www.instagram.com/deemariedi", "470K+", 470000, "rounded",
             "FamousBirthdays: 'over 470,000 followers' on her Instagram page."),
     account("TikTok", "@deemariedi", "https://www.tiktok.com/@deemariedi", "41K", 41000, "rounded",
             "IDCrawl snapshot of TikTok bio: 41K followers, bio lists WBFF MISS FITNESS WORLDS '24 / MISS BIKINI USA '23.")]))

NEW.append(entry("W-2026-061", "Clara Felicia Lindblom",
    ["Fitness", "Fitness Model", "Creator", "Modeling"],
    ev("Born January 10, 1994 in Stockholm, Sweden — age 32 in 2026 — recorded identically by FamousBirthdays (birthDate 1994-01-10), Mabumbe, GreatestPhysiques, Listal and WikiBirthday.",
       "FamousBirthdays — Clara Felicia Lindblom (birthDate 1994-01-10)", "https://www.famousbirthdays.com/people/clara-lindblom.html"),
    ev("Identified as a woman via consistent she/her fitness-model profiles (Mabumbe: 'her journey… she rose to prominence'; bikini competitor).",
       "Mabumbe — Clara Lindblom biography (she/her)", "https://mabumbe.com/people/clara-lindblom-age-net-worth-biography-career/"),
    [
        src("FamousBirthdays — Clara Lindblom (DOB 1994-01-10; IG @clara_lindblom 1.5M+)", "Website", "https://www.famousbirthdays.com/people/clara-lindblom.html", "age-evidence"),
        src("Listal — Clara Felicia Lindblom (DOB 10 Jan 1994; IG follower count 1.8m)", "Website", "https://www.listal.com/clara-felicia-lindblom", "other-trusted"),
        src("Mabumbe — Clara Lindblom bio (over two million followers; real-estate 2025)", "Website", "https://mabumbe.com/people/clara-lindblom-age-net-worth-biography-career/", "other-trusted"),
        src("Instagram — @clara_lindblom (linked via FamousBirthdays sameAs + Listal)", "Instagram", "https://www.instagram.com/clara_lindblom", "verified-platform"),
    ],
    [], "Discovered via famousbio.net Instagram-fitness-model directory. Swedish fitness model and bikini competitor; Workout Empire/Lounge Underwear model — objective categories. Follower snapshots 1.5M+ (FamousBirthdays), 1.8M (Listal), 2M+ (Mabumbe) — latest-bio value used with notes.",
    [account("Instagram", "@clara_lindblom", "https://www.instagram.com/clara_lindblom", "1.8M", 1800000, "rounded",
             "Listal: 'Instagram follower count: 1.8m' (FamousBirthdays 1.5M+; Mabumbe 2M+ snapshots also cited).")]))

NEW.append(entry("W-2026-062", "Yovanna Ventura",
    ["Modeling", "Fashion", "Swimwear", "Creator"],
    ev("Born November 24, 1995 in Miami, Florida — age 30 in 2026 — recorded identically by TheBiography, NaiBuzz, HollywoodLife, TheNewsGod and BookingAgentInfo.",
       "TheBiography — Yovanna Ventura (born 24 November 1995)", "https://thebiography.org/who-is-yovanna-ventura-age-height-relationships-parents-wiki/"),
    ev("Identified as a woman via consistent she/her model/actress biographies (TheNewsGod profile lists Gender: Female; IMG/Wilhelmina/Next women's boards).",
       "TheNewsGod — Yovanna Ventura bio (Gender: Female)", "https://thenewsgod.com/yovanna-ventura-biography-wiki-net-worth-personal-life-and-more/"),
    [
        src("TheBiography — Yovanna Ventura (DOB 1995-11-24; IG @yoventura 5.3M+)", "Website", "https://thebiography.org/who-is-yovanna-ventura-age-height-relationships-parents-wiki/", "age-evidence"),
        src("BookingAgentInfo — Yovanna Ventura (DOB 24/11/1995; 5M+ IG)", "Website", "https://bookingagentinfo.com/celebrity/yovanna-ventura/", "other-trusted"),
        src("NaiBuzz — Yovanna Ventura (Wilhelmina LA/UK; 5.3M+ IG)", "Website", "https://naibuzz.com/yovanna-ventura-inside-the-life-of-the-instagram-star/", "other-trusted"),
        src("Instagram — @yoventura (model, ISHINE365 swimwear line)", "Instagram", "https://www.instagram.com/yoventura/", "verified-platform"),
    ],
    [], "Discovered via famousbio.net Instagram-fitness-model directory. Objective categories: runway model (Milan/NYFW) and swimwear designer (ISHINE365 Miami Swim Week collection). Alternative handle @yoventuraventura cited by TheNewsGod — primary @yoventura per TheBiography/NaiBuzz.",
    [account("Instagram", "@yoventura", "https://www.instagram.com/yoventura/", "5.3M+", 5300000, "rounded",
             "TheBiography/NaiBuzz biographies: official Instagram over 5.3 million followers; BookingAgentInfo 5M+.")]))

NEW.append(entry("W-2026-063", "Kathryn Plummer",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born October 16, 1998 in Long Beach, California — age 27 in 2026 — per Wikipedia encyclopedic biography (Kathryn Plummer Boden, US national team outside hitter).",
       "Wikipedia — Kathryn Plummer (born October 16, 1998)", "https://en.wikipedia.org/wiki/Kathryn_Plummer"),
    ev("Identified as a woman via US women's national volleyball team and Stanford women's volleyball career documented in the encyclopedia entry (she/her).",
       "Wikipedia — Kathryn Plummer (US women's national team)", "https://en.wikipedia.org/wiki/Kathryn_Plummer"),
    [
        src("Wikipedia — Kathryn Plummer (DOB 1998-10-16; Eczacıbaşı Dynavit)", "Website", "https://en.wikipedia.org/wiki/Kathryn_Plummer", "age-evidence"),
        src("HypeAuditor — @kathrynplummer IG stats (42.4K; Pro Volley | Team USA | Stanford)", "Website", "https://hypeauditor.com/instagram/kathrynplummer/", "other-trusted"),
        src("Instagram — @kathrynplummer (Pro Volley | Team USA)", "Instagram", "https://www.instagram.com/kathrynplummer/", "verified-platform"),
    ],
    [], "Discovered via female-volleyball-player research this session. Objective athlete category (2020 Olympic gold team, pro Eczacıbaşı). Mid-size creator (42.4K) — supports follower-size diversity.",
    [account("Instagram", "@kathrynplummer", "https://www.instagram.com/kathrynplummer/", "42.4K", 42400, "rounded",
             "HypeAuditor account page: @kathrynplummer audience 42.4K followers (checked 2026-09-06).")]))

NEW.append(entry("W-2026-064", "Andrea \"Annie\" Drews",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born December 25, 1993 in Muncie, Indiana — age 32 in 2026 — per Tier-1 FIVB volleyballworld.com player bio ('Birth date 25/12/1993', age 32) and Wikipedia-derived biography.",
       "Volleyball World (FIVB) — Drews Andrea player bio (birth date 25/12/1993)", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/155307"),
    ev("Identified as a woman via United States women's national volleyball team roster (Tier-1 FIVB) and consistent she/her coverage (Sportskeeda: married Tanner Schumacher 2021).",
       "Sportskeeda — Andrea Drews profile (US women's national team)", "https://www.sportskeeda.com/us/olympics/andrea-drews-husband"),
    [
        src("Volleyball World — Andrea Drews bio (DOB 25/12/1993; opposite spiker, USA)", "Website", "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/players/155307", "official"),
        src("Grokipedia (Wikipedia-derived) — Andrea Drews biography", "Website", "https://grokipedia.com/page/Andrea_Drews", "other-trusted"),
        src("Women.volleybox — Andrea Drews page linking Instagram @adrews04", "Website", "https://women.volleybox.net/top-15-powerful-volleyball-spikes-by-andrea-drews-lefty-m23906", "other-trusted"),
        src("Instagram — @adrews04 (linked via volleybox)", "Instagram", "https://www.instagram.com/adrews04", "verified-platform"),
    ],
    [], "Olympic gold (Tokyo 2020) and silver (Paris 2024) opposite — objective athlete category. IG handle verified via volleybox page ('Her instagram: adrews04'); no public follower count displayed in available snippets — recorded UNKNOWN, never estimated.",
    [account("Instagram", "@adrews04", "https://www.instagram.com/adrews04", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle confirmed via women.volleybox.net page ('Her instagram: https://www.instagram.com/adrews04'); count not publicly displayed in captured snippets.")]))

NEW.append(entry("W-2026-065", "Justine Wong-Orantes",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born October 6, 1995 in Torrance, California — age 30 in 2026 — per Wikipedia/Wikiwand biography, volleybox structured birthDate 1995-10-06, and USA Volleyball athlete page (born 1995).",
       "Wikiwand — Justine Wong-Orantes (born October 6, 1995)", "https://www.wikiwand.com/en/articles/Justine_Wong-Orantes"),
    ev("Identified as a woman via volleybox structured gender 'Female' and US women's national-team libero role (Wikipedia; USA Volleyball).",
       "volleybox — Justine Wong-Orantes player data (gender: Female)", "https://women.volleybox.net/justine-wong-orantes-p5966/movies"),
    [
        src("USA Volleyball — Justine Wong-Orantes athlete page (born 1995; national team libero)", "Website", "https://usavolleyball.org/athlete/justine-wong-orantes/", "official"),
        src("Women.volleybox — Justine Wong-Orantes (birthDate 1995-10-06; gender Female; LOVB)", "Website", "https://women.volleybox.net/justine-wong-orantes-p5966/movies", "age-evidence"),
        src("Wikiwand — Justine Wong-Orantes biography (DOB 1995-10-06)", "Website", "https://www.wikiwand.com/en/articles/Justine_Wong-Orantes", "other-trusted"),
        src("Instagram — @jwongorantes (volleybox sameAs)", "Instagram", "https://www.instagram.com/jwongorantes/", "verified-platform"),
    ],
    [], "Olympic gold (Tokyo 2020, Best Libero) + silver (Paris 2024). Objective athlete category; LOVB pro. IG public display recorded from instagram.com search snippet 2026-09-06.",
    [account("Instagram", "@jwongorantes", "https://www.instagram.com/jwongorantes/", "55K", 55000, "rounded",
             "Instagram public profile page display via search snippet: '55K followers, 681 following, 480 posts' (bio: 2x Olympic Medalist, pro volley LOVB).")]))

NEW.append(entry("W-2026-066", "Winifer Fernández",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born January 6, 1995 in Santiago de los Caballeros, Dominican Republic — age 31 in 2026 — recorded by CelebsAges and TheFamousPeople (structured), consistent across both.",
       "CelebsAges — Winifer Fernandez (born January 6, 1995)", "https://www.celebsages.com/winifer-fernandez/"),
    ev("Identified as a woman via Dominican Republic women's national volleyball team career (2016 Pan-American Cup gold) and she/her biography.",
       "TheFamousPeople — Famous female volleyball players (Winifer Fernandez, she/her)", "https://www.thefamouspeople.com/women-volleyball-players.php"),
    [
        src("CelebsAges — Winifer Fernandez (DOB 1995-01-06; 280K+ IG historical)", "Website", "https://www.celebsages.com/winifer-fernandez/", "age-evidence"),
        src("TheFamousPeople — female volleyball players (birthdate January 6, 1995)", "Website", "https://www.thefamouspeople.com/women-volleyball-players.php", "other-trusted"),
        src("Instagram — @winifer.fernandezofficial (current public profile)", "Instagram", "https://www.instagram.com/winifer.fernandezofficial/", "verified-platform"),
    ],
    [], "Dominican national-team volleyball player — objective athlete category. Current public IG @winifer.fernandezofficial displays 24K (2026-09-06 snippet); CelebsAges historically cited 280K+ on a prior account — both recorded, not summed.",
    [account("Instagram", "@winifer.fernandezofficial", "https://www.instagram.com/winifer.fernandezofficial/", "24K", 24000, "rounded",
             "Instagram public profile page display via search snippet (2026-09-06): '24K seguidores, 238 siguiendo, 9 publicaciones'. CelebsAges cited 280K+ historically — separate snapshot.")]))

NEW.append(entry("W-2026-067", "Petra Stoker (Petra)",
    ["Entertainment", "Creator", "Athlete"],
    ev("Born June 1, 1993 — age 33 in 2026 — per Liquipedia professional player profile (born June 1, 1993; years active 2020–2025; retired 2025-12-08).",
       "Liquipedia — Petra player profile (born June 1, 1993)", "https://liquipedia.net/valorant/Petra"),
    ev("Identified as a woman via esports press: G2 Gozen founding roster — 'the first women to win World Championships in two different games' (Esports Insider) alongside mimi and juliano.",
       "Esports Insider — Petra moves to G2 Gozen bench (women's championship roster)", "https://esportsinsider.com/2025/04/g2-gozen-valorant-benches-petra"),
    [
        src("Liquipedia — Petra (DOB 1993-06-01; G2 Gozen 2021–2025)", "Website", "https://liquipedia.net/valorant/Petra", "age-evidence"),
        src("Esports Insider — Petra benched article (GC Championship 2022 winner)", "Website", "https://esportsinsider.com/2025/04/g2-gozen-valorant-benches-petra", "press"),
        src("bo3.gg — Top 10 female Valorant players (Petra, G2 Gozen)", "Website", "https://bo3.gg/valorant/articles/top-10-female-players-in-valorant", "other-trusted"),
    ],
    [], "Discovered via women's-esports research this session. Dutch retired pro Valorant/CS:GO player (G2 Gozen founding roster; inaugural Game Changers Championship 2022 winner per press). Objective esports/entertainment category. No social handles with observed public counts captured in snippets — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-068", "Sarah \"sarahcat\" Simpson",
    ["Entertainment", "Creator", "Athlete"],
    ev("Born September 30, 2002 — age 23 in 2026 — per Liquipedia professional player profile (born September 30, 2002; years active 2022–2026; retired).",
       "Liquipedia — sarah player profile (born September 30, 2002)", "https://liquipedia.net/valorant/Sarah"),
    ev("Identified as a woman via career on women's Game Changers rosters — Shopify Rebellion Gold and G2 Gozen (Liquipedia female-team history; bo3 female-player list context).",
       "Liquipedia — G2 Gozen team history (sarah roster entries)", "https://liquipedia.net/valorant/G2_Gozen"),
    [
        src("Liquipedia — sarah (DOB 2002-09-30; Shopify Rebellion Gold)", "Website", "https://liquipedia.net/valorant/Sarah", "age-evidence"),
        src("Liquipedia — G2 Gozen (sarah stand-in → player, 2023)", "Website", "https://liquipedia.net/valorant/G2_Gozen", "other-trusted"),
    ],
    [], "Canadian retired pro Valorant player (alternate ID sarahcat). Objective esports/entertainment category. No social handles with observed public counts captured — follower range UNKNOWN.",
    []))

NEW.append(entry("W-2026-069", "Caroline Marks",
    ["Athlete", "Creator", "Sports"],
    ev("Born February 14, 2002 in Boca Raton, Florida — age 24 in 2026 — per Tier-1 WSL official athlete bio ('Age 24, Feb 14, 2002') and Wikipedia.",
       "World Surf League — Caroline Marks surfer bio (Feb 14, 2002)", "https://www.worldsurfleague.com/athletes/4688/caroline-marks"),
    ev("Identified as a woman via women's Championship Tour career and Olympic women's shortboard gold (Paris 2024) — 'youngest woman to compete in a World Surf League event' (Wikipedia).",
       "Wikipedia — Caroline Marks (women's shortboard, she/her)", "https://en.wikipedia.org/wiki/Caroline_Marks"),
    [
        src("World Surf League — Caroline Marks official athlete bio", "Website", "https://www.worldsurfleague.com/athletes/4688/caroline-marks", "official"),
        src("Wikipedia — Caroline Marks (DOB 2002-02-14; 2023 world champion)", "Website", "https://en.wikipedia.org/wiki/Caroline_Marks", "age-evidence"),
        src("Instagram — @caroline_markss (WSL-linked handle)", "Instagram", "https://www.instagram.com/caroline_markss/", "verified-platform"),
    ],
    [], "2023 WSL world champion and 2024 Olympic gold medalist — objective athlete category. IG count 16K recorded exactly as displayed on the WSL-mirror wavereport.org follow widget; may be stale vs main-tour fame — variance logged in IRR-2026-09-06-009.",
    [account("Instagram", "@caroline_markss", "https://www.instagram.com/caroline_markss/", "16K", 16000, "rounded",
             "wavereport.org mirror of WSL athlete profile: '16k Followers @caroline_markss' follow widget (snapshot; possible staleness — see IRR-2026-09-06-009).")]))

NEW.append(entry("W-2026-070", "Tatiana Weston-Webb",
    ["Athlete", "Creator", "Sports"],
    ev("Born May 9, 1996 in Porto Alegre, Brazil — age 30 in 2026 — per Tier-1 WSL official athlete bio ('Age 29 May 9, 1996' snapshot) and Wikipedia (1996-05-09).",
       "World Surf League — Tatiana Weston-Webb surfer bio (May 9, 1996)", "https://origin.worldsurfleague.com/athletes/2026/tatiana-weston-webb"),
    ev("Identified as a woman via women's Championship Tour and Olympic women's shortboard silver (Paris 2024) — 'first Brazilian woman surfer to win an Olympic medal' (Wikipedia/Kiddle).",
       "Wikipedia — Tatiana Weston-Webb (women's surfing, she/her)", "https://en.wikipedia.org/wiki/Tatiana_Weston-Webb"),
    [
        src("World Surf League — Tatiana Weston-Webb official athlete bio", "Website", "https://origin.worldsurfleague.com/athletes/2026/tatiana-weston-webb", "official"),
        src("Wikipedia — Tatiana Weston-Webb (DOB 1996-05-09)", "Website", "https://en.wikipedia.org/wiki/Tatiana_Weston-Webb", "age-evidence"),
        src("SurfersOfBali YouTube — description linking instagram.com/tatiwest", "YouTube", "https://www.youtube.com/shorts/OHaKV4P6Ws8", "other-trusted"),
        src("Instagram — @tatiwest (pro surfer)", "Instagram", "https://www.instagram.com/tatiwest/", "verified-platform"),
    ],
    [], "Brazilian women's CT surfer, 2024 Olympic silver — objective athlete category; handle @tatiwest confirmed via surfersofbali video description. IG 'over one million followers' per Grokipedia biography statement.",
    [account("Instagram", "@tatiwest", "https://www.instagram.com/tatiwest/", "1M+", 1000000, "rounded",
             "Grokipedia biography: 'over one million followers on Instagram' (checked 2026-09-06); handle via surfersofbali description link.")]))

NEW.append(entry("W-2026-071", "Kysre Gondrezick",
    ["Athlete", "Basketball", "Creator", "Fashion"],
    ev("Born July 27, 1997 in Benton Harbor, Michigan — age 29 in 2026 — recorded by SportsDunia, Sportskeeda, ProBallers and Basketball-Reference (structured birthDate + IG handle).",
       "Basketball-Reference — Kysre Gondrezick (born July 27, 1997)", "https://www.basketball-reference.com/wnba/players/g/gondrky01w/gamelog-playoffs/"),
    ev("Identified as a woman via women's basketball career — 'Michigan Miss Basketball', WNBA guard (Indiana Fever/Chicago Sky), she/her throughout.",
       "Sportskeeda — Kysre Gondrezick player profile (WNBA women's basketball)", "https://www.sportskeeda.com/us/wnba/kysre-gondrezick"),
    [
        src("SportsDunia — Kysre Gondrezick bio (DOB 1997-07-27; IG @kysrerae 598K; X 170.7K)", "Website", "https://www.sportsdunia.com/wnba-players/kysre-gondrezick-biography-net-worth-height-age-contract-career", "age-evidence"),
        src("Sportskeeda — Kysre Gondrezick (DOB July 27, 1997; IG 550K+)", "Website", "https://www.sportskeeda.com/us/wnba/kysre-gondrezick", "press"),
        src("Basketball-Reference — Kysre Gondrezick WNBA page (lists Instagram: kysrerae)", "Website", "https://www.basketball-reference.com/wnba/players/g/gondrky01w/gamelog-playoffs/", "other-trusted"),
        src("Instagram — @kysrerae (WNBA guard; model/brand work)", "Instagram", "https://www.instagram.com/kysrerae/", "verified-platform"),
        src("X — @KysreRae", "X", "https://x.com/KysreRae", "verified-platform"),
    ],
    [], "WNBA guard (2021 #4 pick) and Adidas athlete — objective athlete category; fashion/model activity noted objectively per SportsDunia (Vogue ramp-walk content).",
    [account("Instagram", "@kysrerae", "https://www.instagram.com/kysrerae/", "598K", 598000, "rounded",
             "SportsDunia biography: 598K Instagram followers (Sportskeeda snapshot: 550K+) — recorded as published."),
     account("X", "@KysreRae", "https://x.com/KysreRae", "170.7K", 170700, "rounded",
             "SportsDunia biography: X following 170.7K.")]))

NEW.append(entry("W-2026-072", "Deauzya \"DiDi\" Richards",
    ["Athlete", "Basketball", "Creator"],
    ev("Born February 8, 1999 in Houston/Cypress, Texas — age 27 in 2026 — structured birthDate on Basketball-Reference plus Eurobasket and ProBallers records.",
       "Basketball-Reference — DiDi Richards (born February 8, 1999)", "https://www.basketball-reference.com/wnba/players/r/richadi01w.html"),
    ev("Identified as a woman via WNBA women's basketball career (New York Liberty 2021 draft; Washington Mystics) and she/her college/pro coverage.",
       "Eurobasket — Didi Richards player profile (USA basketball, WNBA draft)", "https://basketball.eurobasket.com/player/Didi-Richards/447315"),
    [
        src("Basketball-Reference — Deauzya Richards WNBA page (DOB 1999-02-08; Instagram: didirich2)", "Website", "https://www.basketball-reference.com/wnba/players/r/richadi01w.html", "age-evidence"),
        src("CelebsFact — DiDi Richards bio (IG @didirich2 146K; X @Deauzya 35.6K)", "Website", "https://celebsfact.net/didi-richards/", "other-trusted"),
        src("Instagram — @didirich2 (basketball creator)", "Instagram", "https://www.instagram.com/didirich2/", "verified-platform"),
        src("X — @Deauzya", "X", "https://x.com/Deauzya", "verified-platform"),
    ],
    [], "WNBA 2021 All-Rookie; 2020 Naismith Defensive Player of the Year at Baylor — objective athlete category; fashion/creator crossover noted by coverage.",
    [account("Instagram", "@didirich2", "https://www.instagram.com/didirich2/", "146K", 146000, "rounded",
             "CelebsFact biography: @didirich2 currently has 146K followers (Nov 2022 snapshot; checked 2026-09-06)."),
     account("X", "@Deauzya", "https://x.com/Deauzya", "35.6K", 35600, "rounded",
             "CelebsFact biography: Twitter @Deauzya 35.6K followers.")]))

NEW.append(entry("W-2026-073", "Dani Danielle \"Elle\" Speegle",
    ["Fitness", "Athlete", "Creator"],
    ev("Born January 10, 1993 in Conifer, Colorado — age 33 in 2026 — per Legit.ng, WikiBioStar, MuscleHustles and Grokipedia. NextBiography lists 1994/Houston — year/place conflict logged; adult either way.",
       "Grokipedia — Dani Speegle (born January 10, 1993)", "https://grokipedia.com/page/dani_speegle"),
    ev("Identified as a woman via women's CrossFit division career and she/her biographies; #GirlsWhoEat body-positivity founder; Titan Games season 2 women's winner.",
       "Legit.ng — Dani Speegle biography (she/her)", "https://www.legit.ng/ask-legit/biographies/1565515-dani-speegles-age-height-net-worth-married/"),
    [
        src("Legit.ng — Dani Speegle (DOB 10 January 1993; IG @dellespeegle 1.8M+)", "Website", "https://www.legit.ng/ask-legit/biographies/1565515-dani-speegles-age-height-net-worth-married/", "age-evidence"),
        src("Grokipedia — Dani Speegle (DOB 1993-01-10; IG 2M+; TikTok ~372K; YT ~180K)", "Website", "https://grokipedia.com/page/dani_speegle", "other-trusted"),
        src("Instagram — @dellespeegle (CrossFit athlete)", "Instagram", "https://www.instagram.com/dellespeegle/", "verified-platform"),
    ],
    ["CONFLICTING_INFORMATION"],
    "Six-time CrossFit Games athlete and Titan Games S2 women's winner — objective fitness/athlete category. DOB-year conflict (1993 across 4 sources vs 1994 NextBiography) logged; adult unaffected.",
    [account("Instagram", "@dellespeegle", "https://www.instagram.com/dellespeegle/", "1.8M+", 1800000, "rounded",
             "Legit.ng biography: 'over 1.8 million followers' on Instagram (Grokipedia snapshot: 2M+, late 2024)."),
     account("TikTok", "@dellespeegle", "https://www.tiktok.com/@dellespeegle", "372K", 372000, "rounded",
             "Grokipedia biography: TikTok @dellespeegle approximately 372,000 followers."),
     account("YouTube", "@dellespeegle", "https://www.youtube.com/@dellespeegle", "180K", 180000, "rounded",
             "Grokipedia biography: YouTube channel around 180,000 subscribers.")]))

NEW.append(entry("W-2026-074", "Demi Bagby",
    ["Fitness", "Athlete", "Creator"],
    ev("Born January 10, 2001 in San Diego, California — age 25 in 2026 — recorded identically by TheFamousPeople, FactCeleb, Dreshare, Gymless and Spreadthoughts (plus her public IG bio lists age 25).",
       "TheFamousPeople — Demi Bagby (birthday January 10, 2001)", "https://www.thefamouspeople.com/profiles/demi-bagby-43857.php"),
    ev("Identified as a woman via structured bio data 'Gender: Female' (FactCeleb) and she/her CrossFit/fitness coverage.",
       "FactCeleb — Demi Bagby biography (Gender: Female)", "https://factceleb.com/biography/demi-bagby-bio-wiki-parents-weight-height-ethnicity-boyfriend-school-app-siblings/"),
    [
        src("TheFamousPeople — Demi Bagby (DOB 2001-01-10; IG 2.7M)", "Website", "https://www.thefamouspeople.com/profiles/demi-bagby-43857.php", "age-evidence"),
        src("Spreadthoughts — Demi Bagby bio (DOB 2001-01-10; IG ~2.7M; YT ~1.77M)", "Website", "https://www.spreadthoughts.com/demi-bagby-biography/", "other-trusted"),
        src("Instagram — @demibagby (calisthenics/CrossFit creator)", "Instagram", "https://www.instagram.com/demibagby/", "verified-platform"),
        src("YouTube — Demi Bagby channel", "YouTube", "https://www.youtube.com/@demibagby", "verified-platform"),
    ],
    [], "CrossFit/calisthenics creator, DemiBagbyFit app founder — objective fitness category. YouTube subscriber figure (~1.77M) recorded from SocialBlade citation in Spreadthoughts (counts change frequently).",
    [account("Instagram", "@demibagby", "https://www.instagram.com/demibagby/", "2.7M", 2700000, "rounded",
             "TheFamousPeople/Spreadthoughts biographies: ~2.7 million Instagram followers (HypeAuditor historical Jan–Feb 2026)."),
     account("YouTube", "@demibagby", "https://www.youtube.com/@demibagby", "1.77M", 1770000, "rounded",
             "Spreadthoughts biography citing SocialBlade: ~1.77M YouTube subscribers (counts change frequently).")]))

NEW.append(entry("W-2026-075", "Sara Hughes",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born February 14, 1995 in Long Beach, California — age 31 in 2026 — per NBC Olympics bio and Sportskeeda coverage; Olympics.com lists year of birth 1995 (Tier-1).",
       "NBC Olympics — Kelly Cheng and Sara Hughes athlete bios (born February 14, 1995)", "https://www.nbcolympics.com/news/kelly-cheng-and-sara-hughes-meet-athletes"),
    ev("Identified as a woman via US beach volleyball women's national team — Olympics.com athlete profile and Team USA bio (Sara Elizabeth Hughes).",
       "Team USA — Sara Hughes athlete profile (Olympian 2024)", "https://www.teamusa.com/profiles/sara-hughes"),
    [
        src("NBC Olympics — Sara Hughes bio (DOB Feb 14, 1995; USC champion)", "Website", "https://www.nbcolympics.com/news/kelly-cheng-and-sara-hughes-meet-athletes", "press"),
        src("USA Volleyball — Sara Hughes athlete page (beach national team)", "Website", "https://usavolleyball.org/athlete/sara-hughes/", "official"),
        src("AVP — Sara Hughes official player page (lists @sarahughesbeach)", "Website", "https://avp.com/player/sara-hughes/", "official"),
        src("Instagram — @sarahughesbeach (linked by USAV embed + AVP)", "Instagram", "https://www.instagram.com/sarahughesbeach/", "verified-platform"),
    ],
    [], "2023 FIVB beach volleyball world champion (with Kelly Cheng), Paris 2024 Olympian — objective athlete category. Handle verified via Tier-1 USAV/AVP pages; no public follower count in captured snippets — recorded UNKNOWN.",
    [account("Instagram", "@sarahughesbeach", "https://www.instagram.com/sarahughesbeach/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle confirmed by usavolleyball.org embedded post and avp.com player page; count not captured in public snippets.")]))

NEW.append(entry("W-2026-076", "Kelly Cheng (née Claes)",
    ["Athlete", "Volleyball", "Creator"],
    ev("Born September 18, 1995 in Fullerton, California — age 30 in 2026 — per Tier-1 volleyballworld.com Olympic player bio ('Birth date 18/09/1995', age 30) and NBC Olympics bio.",
       "Volleyball World (FIVB) — Kelly Cheng player bio (birth date 18/09/1995)", "https://en.volleyballworld.com/beachvolleyball/competitions/beach-volleyball-olympic-games-paris-2024/players/140066"),
    ev("Identified as a woman via volleybox structured gender 'Female' and US women's beach national-team career (USC women's beach volleyball championships 2016–17).",
       "Beach.volleybox — Kelly Cheng player data (gender: Female)", "https://beach.volleybox.net/kelly-cheng-p19093"),
    [
        src("Volleyball World — Kelly Cheng Olympic player bio (DOB 18/09/1995)", "Website", "https://en.volleyballworld.com/beachvolleyball/competitions/beach-volleyball-olympic-games-paris-2024/players/140066", "official"),
        src("NBC Olympics — Kelly Cheng bio (born September 18, 1995)", "Website", "https://www.nbcolympics.com/news/kelly-cheng-and-sara-hughes-meet-athletes", "press"),
        src("Beach.volleybox — Kelly Cheng (Claes; gender Female; sameAs @kellycheng)", "Website", "https://beach.volleybox.net/kelly-cheng-p19093", "other-trusted"),
        src("Instagram — @kellycheng (linked via Olympics.com embed + volleybox sameAs)", "Instagram", "https://www.instagram.com/kellycheng/", "verified-platform"),
    ],
    [], "2023 FIVB beach volleyball world champion (with Sara Hughes), Paris 2024 Olympian — objective athlete category; maiden name Claes per volleybox. IG handle verified via Olympics.com embed; count not captured — UNKNOWN.",
    [account("Instagram", "@kellycheng", "https://www.instagram.com/kellycheng/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
             "Handle confirmed via Olympics.com article embed and volleybox sameAs; count not captured in public snippets.")]))

NEW.append(entry("W-2026-077", "Brooks Nader",
    ["Modeling", "Swimwear", "Fashion", "Creator"],
    ev("Born February 7, 1997 in Baton Rouge, Louisiana — age 29 in 2026 — per NewYorkStyleGuide and BiographyKind. Dreshare lists 1996 — year conflict logged; adult either way.",
       "NewYorkStyleGuide — Brooks Nader profile (born February 7, 1997)", "https://newyorkstyleguide.com/brooks-nader-50-lifestyle-swimsuit-photos/"),
    ev("Identified as a woman via Sports Illustrated Swimsuit model career (2019 Swim Search winner; 2023 cover) and she/her coverage.",
       "BiographyKind — Brooks Nader bio (model, she/her; IG @brooksnader)", "https://en.biographykind.com/brooks-nader/"),
    [
        src("NewYorkStyleGuide — Brooks Nader (DOB 1997-02-07; IG ~1.8M late-2025; TikTok 269.1K)", "Website", "https://newyorkstyleguide.com/brooks-nader-50-lifestyle-swimsuit-photos/", "age-evidence"),
        src("Yahoo Entertainment — Brooks Nader (1.4M IG, Dec 2024 snapshot)", "Website", "https://www.yahoo.com/entertainment/sports-illustrated-swimsuit-model-brooks-191502838.html", "press"),
        src("Dreshare — Brooks Nader wiki (DOB listed 1996 — conflict logged)", "Website", "https://www.dreshare.com/brooks-nader/", "other-trusted"),
        src("Instagram — @brooksnader (SI Swimsuit model)", "Instagram", "https://www.instagram.com/brooksnader/", "verified-platform"),
    ],
    ["CONFLICTING_INFORMATION"],
    "2019 SI Swim Search winner and 2023 SI Swimsuit cover model — objective swimwear/modeling categories (activity-based, never an appearance rating). DOB-year conflict 1997 (most sources) vs 1996 (Dreshare) logged.",
    [account("Instagram", "@brooksnader", "https://www.instagram.com/brooksnader/", "1.8M", 1800000, "rounded",
             "NewYorkStyleGuide (June 2026): roughly 1.8 million Instagram followers as of late 2025; Yahoo (Dec 2024) listed 1.4M."),
     account("TikTok", "@brooksnader", "https://www.tiktok.com/@brooksnader", "269.1K", 269100, "rounded",
             "NewYorkStyleGuide: 269.1k TikTok followers as of late 2025.")]))

NEW.append(entry("W-2026-078", "Regan Smith",
    ["Athlete", "Creator", "Sports"],
    ev("Born February 9, 2002 in Lakeville, Minnesota — age 24 in 2026 — per Olympedia Tier-1 record ('Born: 9 February 2002') and EssentiallySports feature.",
       "Olympedia — Regan Smith (born 9 February 2002; 8 Olympic medals)", "https://www.olympedia.org/athletes/147282"),
    ev("Identified as a woman via Olympedia structured 'Sex: Female' and women's backstroke/butterfly Olympic events.",
       "Olympedia — Regan Smith record (Sex: Female)", "https://www.olympedia.org/athletes/147282"),
    [
        src("Olympedia — Regan Smith (DOB 2002-02-09; Sex: Female; medals record)", "Website", "https://www.olympedia.org/athletes/147282", "official"),
        src("EssentiallySports — Regan Smith family feature (born February 9, 2002)", "Website", "https://www.essentiallysports.com/olympics-swimming-news-who-are-regan-smiths-parents-and-siblings-meet-the-family-behind-usas-backstroke-star/", "press"),
        src("Grokipedia (Wikipedia-derived) — Regan Smith swimmer biography", "Website", "https://grokipedia.com/page/Regan_Smith_(swimmer)", "other-trusted"),
    ],
    [], "Two-time Olympic gold medalist (Paris 2024) and world-record holder in the 100m backstroke — objective athlete category. No public social handles captured in snippets — follower range UNKNOWN (not a disqualifier).",
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
    if "IRR-2026-09-06-009" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-009",
            "severity": "needs-review",
            "summary": "Session-11 batch-1 flags: follower snapshot variances + three DOB conflicts recorded verbatim for manual review.",
            "detail": (
                "(1) DOB conflicts (adult unaffected in all): Mia Sand 1987 vs 1988; Dani Speegle 1993 vs 1994; Brooks Nader 1997 vs 1996. "
                "(2) Caroline Marks IG @caroline_markss 16K comes from a WSL-mirror (wavereport.org) follow widget and may be stale or a secondary account — primary-platform re-check recommended. "
                "(3) Amanda Elise Lee IG 11M+ (BiographyPedia 2024) vs 12M (WomanMagazine 2021) — snapshots differ. "
                "(4) Winifer Fernández: current IG @winifer.fernandezofficial (24K) vs CelebsAges historic 280K+ account — recorded as separate snapshots, not merged. "
                "(5) Mia Sand IG 2M (Oct-2024 display) vs 2.5M+ (TheCityCeleb 2026 bio) — latest-bio cited in note, display value used. "
                "(6) Handful of pro athletes (Sara Hughes, Kelly Cheng, Andrea Drews, Regan Smith, Petra, sarahcat) have Tier-1-verified handles with no publicly captured follower displays — recorded FOLLOWER_COUNT_UNKNOWN, never estimated."
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
