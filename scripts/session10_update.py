#!/usr/bin/env python3
"""Session 10 (2026-09-06) update: second-pass verification + new activity-first adds.

- Promotes 5 REVIEW_REQUIRED candidates whose second-pass public-web research produced
  sufficient gender + adult + identity evidence (Melissa Bender, Kahdia, Olivia Vance,
  Emersen "Emmy" Schrom, Jade Haliburton nee Jones).
- Adds 4 newly discovered verified creators (Jen Selter, Paige Hathaway, Joan MacDonald,
  Sarah Stevenson "Sarah's Day") discovered via fitness-activity searches.
- Enriches 4 remaining review-queue items with newly found evidence (nothing guessed).
- Adds Tier-1 USC roster source to W-2026-033 (Victoria Garrick Browne).
- Logs IRR-2026-09-06-008 with session-10 irregularity flags for manual review.
Every field is backed by a URL returned by this session's web searches; counts are
recorded verbatim as publicly displayed (never estimated, never summed across platforms).
"""

import json
from pathlib import Path

CATALOG = Path("data/catalog.json")
CHECKED = "2026-09-06"

RANGES = [
    (1000, "Under 1K"),
    (5000, "1K–4.9K"),
    (10000, "5K–9.9K"),
    (25000, "10K–24.9K"),
    (50000, "25K–49.9K"),
    (100000, "50K–99.9K"),
    (250000, "100K–249.9K"),
    (500000, "250K–499.9K"),
    (1000000, "500K–999.9K"),
    (5000000, "1M–4.9M"),
]


def size_range(n):
    if n is None:
        return "FOLLOWER_RANGE_UNKNOWN"
    for limit, label in RANGES:
        if n < limit:
            return label
    return "5M+"


def account(platform, username, url, display, numeric, count_type, note):
    return {
        "platform": platform,
        "username": username,
        "profileUrl": url,
        "followerCountDisplay": display,
        "followerCountNumeric": numeric,
        "countType": count_type,
        "checkedAt": CHECKED,
        "followerSizeRange": size_range(numeric),
        "sourceNote": note,
    }


def largest(accounts):
    known = [a for a in accounts if a["followerCountNumeric"] is not None]
    if not known:
        return {
            "platform": None,
            "username": None,
            "display": None,
            "numeric": None,
            "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
            "checkedAt": CHECKED,
        }
    top = max(known, key=lambda a: a["followerCountNumeric"])
    return {
        "platform": top["platform"],
        "username": top["username"],
        "display": top["followerCountDisplay"],
        "numeric": top["followerCountNumeric"],
        "sizeRange": top["followerSizeRange"],
        "checkedAt": CHECKED,
    }


def entry(rid, name, categories, adult, gender, sources, flags, notes, accounts):
    big = largest(accounts)
    return {
        "id": rid,
        "displayName": name,
        "categories": categories,
        "legalAdultEvidence": adult,
        "genderEvidence": gender,
        "sources": sources,
        "verificationStatus": "verified",
        "lastReviewed": CHECKED,
        "flags": flags,
        "notes": notes,
        "socialAccounts": accounts,
        "largestPublicFollowing": big,
        "overallFollowerSizeRange": big["sizeRange"],
    }


def adult_ev(summary, label, url):
    return {"summary": summary, "sourceLabel": label, "sourceUrl": url, "checkedAt": CHECKED}


def src(label, platform, url, relationship):
    return {"label": label, "platform": platform, "url": url, "relationship": relationship}


def build():
    data = json.loads(CATALOG.read_text())
    queue = data["reviewQueue"]
    entries = data["entries"]

    # ---------------- duplicate guard ----------------
    existing_ids = {e["id"] for e in entries}
    existing_names = {e["displayName"].lower() for e in entries}
    existing_urls = {s["url"] for e in entries for s in e["sources"]}
    new_records = []

    # ---------------- W-2026-047 Melissa Bender (promotes R-2026-007) ----------------
    mb_accounts = [
        account(
            "YouTube", "Melissa Bender",
            "https://www.youtube.com/channel/UCW6EhFcuDNhi9XWMYlxTw5g",
            "110,000+", 110000, "rounded",
            "CelebsAges biography: 'amassed more than 110,000 YouTube subscribers'; FamousBirthdays sameAs lists this channel ID.",
        ),
        account(
            "Instagram", "@benderfitness",
            "https://www.instagram.com/benderfitness/",
            "20,000+", 20000, "rounded",
            "CelebsAges biography: 'more than 20,000 followers to her benderfitness Instagram account' (StackInfluence Oct-2025 snapshot listed 23K).",
        ),
        account(
            "X", "@BenderFitness",
            "https://x.com/benderfitness",
            "3,044", 3044, "exact",
            "X public profile page display observed via search snippet: 3,044 followers, joined October 2011.",
        ),
    ]
    new_records.append(entry(
        "W-2026-047", "Melissa Bender",
        ["Fitness", "Creator", "Wellness"],
        adult_ev(
            "Born March 22, 1983 — age 43 in 2026. DOB recorded independently by CelebsAges and FamousBirthdays biographies (Point Park University class of 2007; Chatham College master's 2012).",
            "CelebsAges — Melissa Bender (born March 22, 1983)",
            "https://www.celebsages.com/melissa-bender/",
        ),
        adult_ev(
            "Identified as a woman via biographies using she/her throughout ('The 43-year-old youtuber… She graduated…'); FamousBirthdays 'Social media star… her fitness tips'.",
            "FamousBirthdays — Melissa Bender biography",
            "https://www.famousbirthdays.com/people/melissa-bender.html",
        ),
        [
            src("CelebsAges — Melissa Bender (DOB March 22, 1983; 110K+ YouTube, 20K+ IG)", "Website", "https://www.celebsages.com/melissa-bender/", "age-evidence"),
            src("FamousBirthdays — Melissa Bender (DOB March 22, 1983; fitness creators listing)", "Website", "https://www.famousbirthdays.com/people/melissa-bender.html", "other-trusted"),
            src("X — @BenderFitness (Fitness Blogger, Occupational Therapist; links benderfitness.com)", "X", "https://x.com/benderfitness", "verified-platform"),
            src("Instagram — @benderfitness (benderfitness public profile)", "Instagram", "https://www.instagram.com/benderfitness/", "verified-platform"),
            src("BenderFitness.com — official site linked from her X bio", "Website", "https://benderfitness.com", "official"),
        ],
        [],
        "Discovered via 'female fitness micro influencer' activity (StackInfluence), promoted from REVIEW_REQUIRED R-2026-007 after second-pass research found DOB (1983-03-22) on two independent biographies and consistent she/her identity across official X/IG ↔ CelebsAges ↔ FamousBirthdays. Category: Fitness/Wellness — occupational therapist turned fitness blogger (free workout library). Promoted 2026-09-06.",
        mb_accounts,
    ))

    # ---------------- W-2026-048 Kahdia (promotes R-2026-006) ----------------
    kahdia_accounts = [
        account(
            "Instagram", "@kahdiaaa",
            "https://www.instagram.com/kahdiaaa/",
            "6,604", 6604, "exact",
            "Instagram public profile page display via search snippet (checked 2026-09-06): '6,604 Followers, 472 Following, 246 Posts'. StackInfluence Oct-2025 article listed ~28K — variance recorded verbatim in IRR-2026-09-06-008.",
        ),
    ]
    new_records.append(entry(
        "W-2026-048", "Kahdia",
        ["Fitness", "Creator", "Lifestyle"],
        adult_ev(
            "Explicit age statement in published profile: '25-year-old Kahdia' (StackInfluence, Top Female Fitness Influencers) — 25 > 18.",
            "StackInfluence — Top Female Fitness Influencers (Kahdia, 25)",
            "https://stackinfluence.com/top-10-female-fitness-influencers-of-2025/",
        ),
        adult_ev(
            "Identified as a woman via the profile article's consistent she/her biography ('She creates content around workouts… her audience… she especially resonates with young women').",
            "StackInfluence — Kahdia profile (she/her)",
            "https://stackinfluence.com/top-10-female-fitness-influencers-of-2025/",
        ),
        [
            src("StackInfluence — Kahdia: 25-year-old Miami fitness/lifestyle micro creator (she/her)", "Website", "https://stackinfluence.com/top-10-female-fitness-influencers-of-2025/", "age-evidence"),
            src("Instagram — @kahdiaaa (K A H D I A; 6,604 followers observed)", "Instagram", "https://www.instagram.com/kahdiaaa/", "verified-platform"),
        ],
        [],
        "Discovered via fitness micro-influencer activity, promoted from REVIEW_REQUIRED R-2026-006. Adult via explicit '25-year-old' statement; woman via she/her profile text; ownership via @kahdiaaa public profile matching the profiled creator (workouts, gym fits, Miami). Follower display 6,604 recorded exactly as publicly shown; prior third-party 28K snapshot noted for review (IRR-2026-09-06-008). Promoted 2026-09-06.",
        kahdia_accounts,
    ))

    # ---------------- W-2026-049 Olivia Vance (promotes R-2026-003) ----------------
    ov_accounts = [
        account(
            "TikTok", "@oliviafvance",
            "https://www.tiktok.com/@oliviafvance",
            "106K", 106000, "rounded",
            "Collabstr volleyball-creator listing: 106K TikTok (observed in Session 07 discovery; re-confirmed against same creator this session).",
        ),
        account(
            "Instagram", "@oliviafvance",
            "https://www.instagram.com/oliviafvance/",
            "25K", 25000, "rounded",
            "Collabstr listing recorded 25K Instagram; volleybox sameAs links this same handle to her player profile.",
        ),
    ]
    new_records.append(entry(
        "W-2026-049", "Olivia Vance",
        ["Athlete", "Volleyball", "Creator"],
        adult_ev(
            "Born March 2, 2001 (women.volleybox.net player profile) — age 25 in 2026; OpenSponsorship athlete profile independently lists age 25; Opendorse lists 24 (snapshot older).",
            "volleybox — Olivia Vance (born 2 March 2001)",
            "https://women.volleybox.net/olivia-vance-p93444",
        ),
        adult_ev(
            "Identified as a woman via volleybox structured data (gender: Female) plus OpenSponsorship '👩 Female' and Opendorse 'Professional athlete • Female'.",
            "OpenSponsorship — Olivia Vance (Female, 25, volleyball)",
            "https://opensponsorship.com/profiles/olivia-vance-1",
        ),
        [
            src("volleybox — Olivia Vance, outside hitter (born 2001-03-02; sameAs @oliviafvance)", "Website", "https://women.volleybox.net/olivia-vance-p93444", "age-evidence"),
            src("OpenSponsorship — Olivia Vance athlete profile (Female, 25)", "Website", "https://opensponsorship.com/profiles/olivia-vance-1", "other-trusted"),
            src("Opendorse — Olivia Vance, professional athlete (Female, 24 snapshot)", "Website", "https://opendorse.com/profile/olivia-vance", "other-trusted"),
            src("TikTok — @oliviafvance (pro volleyball creator)", "TikTok", "https://www.tiktok.com/@oliviafvance", "verified-platform"),
            src("Instagram — @oliviafvance (volleybox sameAs link)", "Instagram", "https://www.instagram.com/oliviafvance/", "verified-platform"),
        ],
        [],
        "Discovered via volleyball-creator activity, promoted from REVIEW_REQUIRED R-2026-003 after independent DOB (2001-03-02, volleybox) + two independent gender/age athlete profiles (OpenSponsorship 25 / Opendorse 24) were found; volleybox sameAs links the @oliviafvance Instagram handle. Category: professional volleyball (played in Portugal) — objective. Promoted 2026-09-06.",
        ov_accounts,
    ))

    # ---------------- W-2026-050 Emersen "Emmy" Schrom (promotes R-2026-004) ----------------
    es_accounts = [
        account(
            "TikTok", "@emmyschrom",
            "https://www.tiktok.com/@emmyschrom",
            "FOLLOWER_COUNT_UNKNOWN", None, "unknown",
            "Profile identified via Collabstr D1-volleyball listing; platform does not expose a public count in available search snippets — never estimated.",
        ),
    ]
    new_records.append(entry(
        "W-2026-050", "Emersen \"Emmy\" Schrom",
        ["College Athlete", "Volleyball", "Creator"],
        adult_ev(
            "Tier-1 university athletics biography states: 'Was born on March 21, 2006' — age 20 in 2026 (Duquesne University official roster).",
            "Duquesne University Athletics — Emersen Schrom roster bio (born March 21, 2006)",
            "https://goduquesne.com/sports/womens-volleyball/roster/emersen-schrom/13197",
        ),
        adult_ev(
            "Identified as a woman via Tier-1 women's volleyball roster biography: 'Daughter of Jennifer and Andrew Schrom — has one sister' on the official Duquesne women's athletics site.",
            "Duquesne University Athletics — Emersen Schrom, Women's Volleyball #11",
            "https://goduquesne.com/sports/womens-volleyball/roster/emersen-schrom/13197",
        ),
        [
            src("Duquesne Athletics — Emersen Schrom #11 (born March 21, 2006; marketing major; Atlantic 10 All-Rookie 2024)", "Website", "https://goduquesne.com/sports/womens-volleyball/roster/emersen-schrom/13197", "official"),
            src("Duquesne Athletics — Dukes Extend Streak With Win (Schrom #11 match report)", "Website", "https://goduquesne.com/news/2025/11/1/womens-volleyball-dukes-extend-streak-with-win-over-saint-louis.aspx", "press"),
            src("TikTok — @emmyschrom (Emmy Schrom creator profile)", "TikTok", "https://www.tiktok.com/@emmyschrom", "verified-platform"),
        ],
        [],
        "Promoted from REVIEW_REQUIRED R-2026-004. Identity chain: Collabstr listing described 'Emmy', a 20-year-old D1 volleyball marketing major at Duquesne with handle @emmyschrom; the official Duquesne roster lists Emersen Schrom — women's volleyball #11, marketing major, born March 21, 2006 (20 in 2026). Unique surname + school + sport + major + age triangulation links the handle; adult/gender/identity rest on the Tier-1 roster. Promoted 2026-09-06.",
        es_accounts,
    ))

    # ---------------- W-2026-051 Jade Haliburton (promotes R-2026-011) ----------------
    jh_accounts = [
        account(
            "Instagram", "@jadehaliburton",
            "https://www.instagram.com/jadehaliburton/",
            "170K+", 170000, "rounded",
            "FamousBirthdays: 'gained over 170,000 followers to her jadehaliburton Instagram account'; SoapCentral (June 2026) reports 160K+ — recorded as publicly stated, rounded.",
        ),
    ]
    new_records.append(entry(
        "W-2026-051", "Jade Haliburton",
        ["Fashion", "Lifestyle", "Creator"],
        adult_ev(
            "Born January 30, 1998 in Iowa — age 28 in 2026 — per FamousBirthdays, WealthySpy and NewsBritania biographies (StarsUnfolded lists January 31, 1998; birth year consistent across all sources).",
            "FamousBirthdays — Jade Haliburton (born January 30, 1998)",
            "https://www.famousbirthdays.com/people/jade-jones-instagramstar.html",
        ),
        adult_ev(
            "Identified as a woman via consistent press/biography language: fiancée of NBA player Tyrese Haliburton, she/her throughout (SoapCentral, WealthySpy, StarsUnfolded).",
            "SoapCentral — Who is Jade Jones? (fiancée profile, she/her)",
            "https://www.soapcentral.com/entertainment/who-jade-jones-all-tyrese-haliburton-s-fiancee-friend-dies-bachelorette-party",
        ),
        [
            src("FamousBirthdays — Jade Haliburton (DOB Jan 30, 1998; sameAs @jadehaliburton)", "Website", "https://www.famousbirthdays.com/people/jade-jones-instagramstar.html", "age-evidence"),
            src("WealthySpy — Jade Jones biography (born Jan 30, 1998, Iowa City; teacher/model)", "Website", "https://wealthyspy.com/jade-jones/", "other-trusted"),
            src("NewsBritania — Jade Jones profile (DOB Jan 30, 1998; lifestyle influencer)", "Website", "https://newsbritania.co.uk/jade-jones/", "press"),
            src("SoapCentral — Jade Jones, Tyrese Haliburton's fiancée (June 2026)", "Website", "https://www.soapcentral.com/entertainment/who-jade-jones-all-tyrese-haliburton-s-fiancee-friend-dies-bachelorette-party", "press"),
            src("Instagram — @jadehaliburton (fashion/lifestyle creator, 170K+)", "Instagram", "https://www.instagram.com/jadehaliburton/", "verified-platform"),
        ],
        ["CONFLICTING_INFORMATION"],
        "Promoted from REVIEW_REQUIRED R-2026-011: surname RESOLVED — née Jade Jones (Davenport West HS; Iowa State cheerleader/elementary teacher), engaged to Tyrese Haliburton July 28, 2025; she now publishes as Jade Haliburton and the FamousBirthdays sameAs confirms @jadehaliburton is the same person. Minor open conflict: birth day listed as Jan 30 (FamousBirthdays/WealthySpy/NewsBritania) vs Jan 31 (StarsUnfolded) — year 1998 consistent; adult status unaffected. Flag retained for transparency. Promoted 2026-09-06.",
        jh_accounts,
    ))

    # ---------------- W-2026-052 Jen Selter (new, fitness-activity discovery) ----------------
    js_accounts = [
        account(
            "Instagram", "@jenselter",
            "https://www.instagram.com/jenselter/",
            "13.6M", 13600000, "rounded",
            "Published biographies (Mabumbe / Washington Morning): 13.6 million Instagram followers as of February 2023; famousbio lists 'more than 12 million'. Recorded as public snapshot, rounded.",
        ),
    ]
    new_records.append(entry(
        "W-2026-052", "Jen Selter",
        ["Fitness", "Fitness Model", "Creator", "Modeling"],
        adult_ev(
            "Born August 8, 1993 in Roslyn, New York — age 33 in 2026 — recorded identically by Mabumbe, Generation Iron, FamousBio, Washington Morning and Dreshare biographies.",
            "Mabumbe — Jennifer Leigh 'Jen' Selter (born August 8, 1993)",
            "https://mabumbe.com/people/jen-selter-age-net-worth-relationships-biography/",
        ),
        adult_ev(
            "Identified as a woman via structured biography data 'Gender: Female' (FamousBio) and consistent she/her fitness-model biographies across five independent sources.",
            "FamousBio — Jen Selter (Gender: Female; fitness model)",
            "https://famousbio.net/jen-selter-8777.html",
        ),
        [
            src("Mabumbe — Jen Selter biography (DOB Aug 8, 1993; IG 13.6M Feb-2023)", "Website", "https://mabumbe.com/people/jen-selter-age-net-worth-relationships-biography/", "age-evidence"),
            src("Generation Iron — Jen Selter profile (DOB 8/8/1993, Roslyn NY)", "Website", "https://generationiron.com/jen-selter-profile-bio-stats/", "press"),
            src("FamousBio — Jen Selter (Gender: Female; socials IG @jenselter / X @jenselter / FB jenLselter)", "Website", "https://famousbio.net/jen-selter-8777.html", "other-trusted"),
            src("Instagram — @jenselter (fitness creator)", "Instagram", "https://www.instagram.com/jenselter/", "verified-platform"),
            src("jenselter.com — official website per biography listings", "Website", "https://jenselter.com", "official"),
        ],
        [],
        "Discovered via female-fitness-creator activity article (GoTeamUp fitness-influencer list) this session; DOB and identity consistent across 5 independent biographies. Category fitness/fitness-model — objective (workout programs, BlendJet partnership). No attractiveness classification applied.",
        js_accounts,
    ))

    # ---------------- W-2026-053 Paige Hathaway (new, fitness-activity discovery) ----------------
    ph_accounts = [
        account(
            "Instagram", "@paigehathaway",
            "https://www.instagram.com/paigehathaway/",
            "3.6M", 3600000, "rounded",
            "Famecop profile (updated 2026): 'over 3.6 million followers on her Instagram account'; CelebrityBorns listed ~4 million as of July 2020 — historical snapshots differ, recorded verbatim in IRR-2026-09-06-008.",
        ),
    ]
    new_records.append(entry(
        "W-2026-053", "Paige Hathaway",
        ["Fitness", "Fitness Model", "Creator"],
        adult_ev(
            "Born July 31, 1987 in Minnesota — age 39 in 2026 — recorded identically by CelebrityBorns, TheFamousPeople, TheCityCeleb, Famecop and MarriedCeleb biographies.",
            "TheFamousPeople — Paige Hathaway (birthday July 31, 1987)",
            "https://www.thefamouspeople.com/profiles/paige-hathaway-31518.php",
        ),
        adult_ev(
            "Identified as a woman via structured data 'Gender Identity: Female' (MarriedCeleb), TheCityCeleb occupation/children schema, and consistent she/her fitness-model biographies.",
            "MarriedCeleb — Paige Hathaway (Gender Identity: Female)",
            "https://marriedceleb.com/paige-hathaway",
        ),
        [
            src("TheFamousPeople — Paige Hathaway (DOB July 31, 1987; FLEX 2013 Bikini Model Search Winner)", "Website", "https://www.thefamouspeople.com/profiles/paige-hathaway-31518.php", "age-evidence"),
            src("CelebrityBorns — Paige Hathaway (DOB 31-07-1987; ~4M IG July 2020)", "Website", "https://celebrityborns.com/biography/paige-hathaway/8618", "other-trusted"),
            src("Famecop — Paige Hathaway (born 31 July 1987; 3.6M IG)", "Website", "https://famecop.com/paige-hathaway/", "other-trusted"),
            src("MarriedCeleb — Paige Hathaway (Gender Identity: Female; DOB)", "Website", "https://marriedceleb.com/paige-hathaway", "other-trusted"),
            src("Instagram — @paigehathaway (Fitin5 / LIV Body fitness creator)", "Instagram", "https://www.instagram.com/paigehathaway/", "verified-platform"),
        ],
        [],
        "Discovered via female-fitness-creator activity article (GoTeamUp) this session. Objective category evidence: 2nd place 2012 Ronnie Coleman Classic bikini division; FLEX August 2013 Bikini Model Search winner; Fitin5 coaching program and LIV Body founder. Five independent biographies agree on DOB (1987-07-31).",
        ph_accounts,
    ))

    # ---------------- W-2026-054 Joan MacDonald (new, fitness-activity discovery) ----------------
    jm_accounts = [
        account(
            "Instagram", "@trainwithjoan",
            "https://www.instagram.com/trainwithjoan/",
            "1.7M+", 1700000, "rounded",
            "KPRC Click2Houston (Sept 2023): '77-year-old fitness influencer with over 1.7 million Instagram followers'; TheCityCeleb (2026) states 'over 2 million' — recorded as published snapshots.",
        ),
    ]
    new_records.append(entry(
        "W-2026-054", "Joan MacDonald",
        ["Fitness", "Wellness", "Creator"],
        adult_ev(
            "Born March 31, 1946 (TheCityCeleb biography) — age 80 in 2026; consistent press age statements: 74 (Business Insider, Aug 2020), 75 (Good Morning America, Mar 2023), 77 (KPRC, Sept 2023).",
            "Good Morning America — 75-year-old fitness influencer Joan MacDonald (Mar 2023)",
            "https://www.goodmorningamerica.com/wellness/story/75-year-woman-lost-60-pounds-fitness-influencer-82655773",
        ),
        adult_ev(
            "Identified as a woman via reputable press: GMA 'How this 75-year-old woman lost over 60 pounds'; daughter Michelle MacDonald; Penguin Random House author bio (she/her).",
            "GMA / Penguin Random House author bio — Joan MacDonald (@trainwithjoan)",
            "https://www.penguinrandomhouse.com/authors/2266784/joan-macdonald/",
        ),
        [
            src("Good Morning America — 75-year-old fitness influencer (Mar 2023)", "Website", "https://www.goodmorningamerica.com/wellness/story/75-year-woman-lost-60-pounds-fitness-influencer-82655773", "press"),
            src("TheCityCeleb — Joan MacDonald bio (born March 31, 1946; 2M+ IG)", "Website", "https://www.thecityceleb.com/biography/personality/content-creator/joan-macdonald-bio-age-height-husband-daughter-net-worth-book-transformation-youtube-instagram/", "age-evidence"),
            src("KPRC Click2Houston — 77-year-old influencer, 1.7M+ IG (Sept 2023)", "Website", "https://www.click2houston.com/houston-life/2023/09/15/age-is-just-a-number-meet-the-77-year-old-fitness-influencer-joan-mcdonald/", "press"),
            src("Penguin Random House — Joan MacDonald author page (Flex Your Age)", "Website", "https://www.penguinrandomhouse.com/authors/2266784/joan-macdonald/", "official"),
            src("Instagram — @trainwithjoan (Train With Joan)", "Instagram", "https://www.instagram.com/trainwithjoan/", "verified-platform"),
        ],
        [],
        "Discovered via fitness-influencer discovery search this session (GMA feature). Canadian creator who began strength training at 70 and co-authored 'Flex Your Age' (Penguin Random House) — senior-creator diversity in the dataset. Category Fitness/Wellness — objective.",
        jm_accounts,
    ))

    # ---------------- W-2026-055 Sarah Stevenson "Sarah's Day" (new, fitness-activity discovery) ----------------
    sd_accounts = [
        account(
            "YouTube", "@SarahsDay",
            "https://www.youtube.com/@SarahsDay",
            "1.54M", 1540000, "rounded",
            "National Today profile: 'accumulated 1.54 million subscribers on her YouTube channel'; Wikitia confirms 1.5M+ as of 2025.",
        ),
        account(
            "Instagram", "@sarahs_day",
            "https://www.instagram.com/sarahs_day/",
            "1.2M", 1200000, "rounded",
            "Famecop profile: 'over 1.2 million followers on her Instagram account' (GossipsDiary snapshot listed 1.1M).",
        ),
    ]
    new_records.append(entry(
        "W-2026-055", "Sarah Stevenson (Sarah's Day)",
        ["Fitness", "Lifestyle", "Wellness", "Creator"],
        adult_ev(
            "Born August 30, 1992 in Sydney, Australia — age 34 in 2026 — recorded identically by Famecop, FamousPeople.io, National Today, Wikitia and GossipsDiary.",
            "National Today — Sarah Stevenson birthday (born August 30, 1992)",
            "https://nationaltoday.com/birthday/sarah-stevenson/",
        ),
        adult_ev(
            "Identified as a woman via structured bio data 'Gender: Female' (GossipsDiary) and consistent she/her biographies (Wikitia: 'professionally known as Sarah's Day'; mother of three).",
            "Wikitia — Sarah's Day (Sarah Stevenson, born August 30, 1992)",
            "https://wikitia.com/wiki/Sarah's_Day",
        ),
        [
            src("National Today — Sarah Stevenson (DOB Aug 30, 1992; 1.54M YouTube subscribers)", "Website", "https://nationaltoday.com/birthday/sarah-stevenson/", "age-evidence"),
            src("Wikitia — Sarah's Day encyclopedia entry (DOB 1992-08-30; Sunee app founder)", "Website", "https://wikitia.com/wiki/Sarah's_Day", "other-trusted"),
            src("Famecop — Sarah's Day (born 30 Aug 1992; IG @sarahs_day 1.2M; YouTube @SarahsDay)", "Website", "https://famecop.com/fitness/sarahs-day/", "other-trusted"),
            src("GossipsDiary — Sarah's Day (Gender: Female; socials @sarahs_day 1.1M)", "Website", "https://gossipsdiary.com/sarahs-day-wiki-bio/", "other-trusted"),
            src("YouTube — @SarahsDay (Sarah's Day channel)", "YouTube", "https://www.youtube.com/@SarahsDay", "verified-platform"),
            src("Instagram — @sarahs_day (fitness/lifestyle creator)", "Instagram", "https://www.instagram.com/sarahs_day/", "verified-platform"),
        ],
        [],
        "Discovered via FamousBirthdays fitness-creator directory this session. Australian fitness/lifestyle creator: YouTube since 2013, Sunee app founder, The Health Code podcast co-host, White Fox activewear collaborations — objective categories only.",
        sd_accounts,
    ))

    # ---------------- duplicate check before appending ----------------
    for rec in new_records:
        assert rec["id"] not in existing_ids, f"duplicate id {rec['id']}"
        assert rec["displayName"].lower() not in existing_names, f"duplicate name {rec['displayName']}"
        overlapping = {s["url"] for s in rec["sources"]} & existing_urls
        assert not overlapping, f"source URL already in catalog: {overlapping}"
    entries.extend(new_records)

    # ---------------- enrich W-2026-033 with Tier-1 USC roster source ----------------
    for e in entries:
        if e["id"] == "W-2026-033":
            urls = {s["url"] for s in e["sources"]}
            usc = "https://usctrojans.com/sports/womens-volleyball/roster/victoria-garrick/8539"
            if usc not in urls:
                e["sources"].insert(0, src(
                    "USC Athletics — Victoria Garrick 2018 women's volleyball roster ('Victoria Lane Garrick was born on April 30, 1997')",
                    "Website", usc, "age-evidence"))
                e["notes"] = (e.get("notes", "") + " Session-10 backfill: Tier-1 USC Athletics roster added as direct DOB/gender source.").strip()

    # ---------------- remove promoted queue items & enrich the rest ----------------
    promoted = {"R-2026-003", "R-2026-004", "R-2026-006", "R-2026-007", "R-2026-011"}
    queue = [q for q in queue if q["id"] not in promoted]

    for q in queue:
        if q["id"] == "R-2026-001":
            q["evidenceFound"] = {
                "summary": "URI women's volleyball setter; 2026 roster: Redshirt Junior, Saint Charles, Ill. (St. Charles North HS; transferred from Elon where she made the CAA All-Rookie Team); holds St. Charles North assist record (1,637); HS regional titles 2021/2022.",
                "sourceLabel": "URI Athletics — 2026 women's volleyball roster, Jessica Parker #1",
                "sourceUrl": "https://gorhody.com/sports/womens-volleyball/roster",
            }
            q["lastChecked"] = CHECKED
            q["notes"] += " Second-pass 2026-09-06: full bio retrieved (redshirt junior; Elon transfer; HS class ~2022) — college/career timeline suggests early 20s but per protocol adult status is never inferred from college attendance; no explicit DOB/age statement found, stays AGE_UNVERIFIED. Namesake caution: UWSP volleyball's Jessica Parker (born 5/19/82, athletics.uwsp.edu) is a DIFFERENT person — do not merge."
        elif q["id"] == "R-2026-005":
            q["evidenceFound"] = {
                "summary": "IFBB Pro bodybuilder (El Paso, TX); official site lizzieifbbpro.com; public X profile @LizzieIfbbpro lists 'Born May 30' (no year), 1,444 followers, joined Nov 2016; ~49K Instagram per StackInfluence.",
                "sourceLabel": "X — @LizzieIfbbpro (lizzieifbbpro.com; born May 30 — year not public)",
                "sourceUrl": "https://x.com/lizzieifbbpro",
            }
            q["lastChecked"] = CHECKED
            q["notes"] += " Second-pass 2026-09-06: X profile found (El Paso; own domain; 'Born May 30' without year). Partial birthday is not an age — stays AGE_UNVERIFIED. Next: NPC/IFBB competitor records or reputable interview with age."
        elif q["id"] == "R-2026-008":
            q["evidenceFound"] = {
                "summary": "TheOrg professional profile: Master Trainer at Technogym since Sept 2023; Amazon Influencer since May 2020; Fitness Instructor at Apawamis Club since May 2014; B.A. (Early Childhood Education) Long Island University 2004–2007.",
                "sourceLabel": "TheOrg — Rachel Cooper, Master Trainer at Technogym",
                "sourceUrl": "https://theorg.com/org/technogym/org-chart/rachel-cooper",
            }
            q["lastChecked"] = CHECKED
            q["notes"] += " Second-pass 2026-09-06: documented 2004–2007 bachelor's degree and 12-year professional career strongly indicate an adult, but the profile contains no explicit DOB/age/'18+' statement and no she/her biography; per protocol (no inference from career timeline) stays AGE_UNVERIFIED + GENDER_UNVERIFIED pending explicit source."
        elif q["id"] == "R-2026-012":
            q["evidenceFound"] = {
                "summary": "Zaver.one creator profile: @getfitwith.val 'Valentina Villa | Fitness & Lifestyle Coach', 5,686 Instagram followers, 204 posts (fitness/wellness/weight-loss); bio offers 1:1 online coaching and Pilates at @pilattestudio.nj & @ilcorpo.clifton; TikTok presence (prior snapshot 2,768 followers).",
                "sourceLabel": "Zaver.one — @getfitwith.val (Valentina Villa, 5,686 IG followers)",
                "sourceUrl": "https://zaver.one/creators/instagram/getfitwith.val",
            }
            q["followerCountDisplay"] = "5,686"
            q["followerCountNumeric"] = 5686
            q["followerCountCheckedAt"] = CHECKED
            q["followerSizeRange"] = "5K–9.9K"
            q["lastChecked"] = CHECKED
            q["notes"] += " Second-pass 2026-09-06: Instagram count 5,686 recorded from Zaver.one public snapshot (TikTok snapshot earlier: 2,768). Still no public DOB/age statement → AGE_UNVERIFIED; bio 'Helping women…' describes the audience, not the creator → GENDER_UNVERIFIED. Creator's contact email visible in bio deliberately NOT collected (out of scope)."

    data["reviewQueue"] = queue

    # ---------------- irregularity log ----------------
    irr_ids = {i["id"] for i in data["irregularities"]}
    if "IRR-2026-09-06-008" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-008",
            "severity": "needs-review",
            "summary": "Session-10 verification flags: follower-display variances and one DOB-day conflict, all recorded verbatim for manual review.",
            "detail": (
                "(1) Kahdia (W-2026-048): StackInfluence (Oct 2025) listed ~28K Instagram followers; public Instagram profile snippet checked 2026-09-06 displays 6,604 — both recorded; catalog uses the first-party platform display. "
                "(2) Jade Haliburton (W-2026-051): birth day Jan 30 (3 sources) vs Jan 31 (StarsUnfolded); year 1998 consistent, adult status unaffected — identity (née Jones) now resolved. "
                "(3) Paige Hathaway (W-2026-053): IG 3.6M (Famecop 2026 snapshot) vs ~4M (CelebrityBorns July 2020) — historical snapshots differ; latest used. "
                "(4) Namesake caution recorded in R-2026-001: URI setter Jessica Parker ≠ UWSP's Jessica Parker (born 5/19/82). "
                "(5) Joan MacDonald IG 1.7M+ (KPRC 2023) vs 2M+ (TheCityCeleb 2026) — both cited. "
                "(6) The 1,000-creator figure remains a target, not a quota: 55 verified / 4 review after this session; unverifiable candidates stay REVIEW_REQUIRED rather than being guessed."
            ),
            "reviewStatus": "requires-owner-review",
        })

    # ---------------- metadata ----------------
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["reviewQueueCount"] = len(queue)
    data["metadata"]["generatedAt"] = CHECKED
    data["metadata"]["summary"] = (
        "Women-only directory of adult (18+) public creators: 55 verified adult women (W-2026-001..055) spanning professional and college athletes, fitness/fitness-model creators, swimwear/bikini-fashion models, fashion and lifestyle/wellness creators, plus 4 REVIEW_REQUIRED candidates. "
        "Session 10 promoted 5 queue candidates after second-pass research (Melissa Bender, Kahdia, Olivia Vance, Emersen 'Emmy' Schrom, Jade Haliburton née Jones) and added 4 newly discovered verified creators (Jen Selter, Paige Hathaway, Joan MacDonald, Sarah Stevenson 'Sarah's Day'); per-platform follower counts are publicly observed displays only — never estimated, never summed across platforms; unknown counts recorded as FOLLOWER_COUNT_UNKNOWN."
    )

    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} queue={len(queue)} irregularities={len(data['irregularities'])}")


if __name__ == "__main__":
    build()
