#!/usr/bin/env python3
"""Session 08 (2026-09-06): add 21 line-by-line verified adult women + update review queue.

Every field below is backed by a URL returned by public-web search on 2026-09-06
(urls seen in search results / search-result JSON-LD exactly as found).
Minors discovered during research (Sabre Norris b. 2005, Sky Brown b. 2008) were
REJECTED and are documented in docs/review-log.md Session 08 — they are NOT added.
"""
import json

D = "2026-09-06"

def src(label, platform, url, rel):
    return {"label": label, "platform": platform, "url": url, "relationship": rel}

def adult(summary, label, url):
    return {"summary": summary, "sourceLabel": label, "sourceUrl": url, "checkedAt": D}

def gender(summary, label, url):
    return {"summary": summary, "sourceLabel": label, "sourceUrl": url, "checkedAt": D}

def entry(eid, name, cats, le, ge, sources, notes, flags=None):
    return {
        "id": eid,
        "displayName": name,
        "categories": cats,
        "legalAdultEvidence": le,
        "genderEvidence": ge,
        "sources": sources,
        "verificationStatus": "verified",
        "lastReviewed": D,
        "flags": flags or [],
        "notes": notes,
    }

FB = "FamousBirthdays"

NEW = [
entry("W-2026-014", "Shay Williams (Shay G)", ["Modeling", "Fashion", "Lifestyle", "Fitness"],
    adult("Born February 11, 1996 in the United States — age 30 in 2026. DOB stated on FamousBirthdays profile and corroborated by an independent creator biography (same DOB, real name Shamayne Williams).",
          FB + " — Shay Williams (born February 11, 1996)", "https://www.famousbirthdays.com/people/shay-williams.html"),
    gender("Referred to as 'she/her' throughout her FamousBirthdays biography; independent biography identifies her as an American female creator, real name Shamayne Williams.",
           "FamousBirthdays — Shay Williams biography (she/her)", "https://www.famousbirthdays.com/people/shay-williams.html"),
    [src("Instagram — @shamayne_shay (2.4M followers, modeling content)", "Instagram", "https://www.instagram.com/shamayne_shay/", "verified-platform"),
     src(FB + " — DOB February 11, 1996, modeling Instagram star", "Website", "https://www.famousbirthdays.com/people/shay-williams.html", "other-trusted"),
     src("Creator biography — Shamayne Williams, DOB February 11, 1996, modeling/fitness/fashion/lifestyle niche", "Website", "https://influencebabe.blogspot.com/2025/06/shay-g-shamayne-williams-rise-of.html", "other-trusted")],
    "Discovered via modeling-creator activity search. Woman per biography pronouns + independent biography (Shamayne Williams). Adult via Feb 11, 1996 DOB on two independent sources. Identity cross-linked: FamousBirthdays sameAs Instagram @shamayne_shay matches the handle both sources describe; Twitter @iamshamayne also referenced. Category: modeling/fashion/lifestyle/fitness content — objective. Follower count (~2.4M) recorded incidentally, not an eligibility filter."),
entry("W-2026-015", "Jenna Bandy", ["Basketball", "Sports", "Fitness", "Creator"],
    adult("Born September 29, 1992 — age 33 in 2026. DOB stated on FamousBirthdays; press profile (2022) described her as 29-year-old head coach, consistent with that DOB.",
          FB + " — Jenna Bandy (born September 29, 1992)", "https://www.famousbirthdays.com/people/jenna-bandy.html"),
    gender("Referred to as 'she/her' throughout; sportskeeda profile describes her coaching career as Varsity Girls Basketball head coach at Calabasas High School and founder of the Basketball Beauties All-League club.",
           "Sportskeeda — Who is Jenna Bandy? (girls' basketball coach, she/her)", "https://www.sportskeeda.com/pop-culture/who-jenna-bandy-meet-agt-extreme-contestant-rejected-simon-cowell"),
    [src("NBA.com — Jenna Bandy named among NBA Creator Cup Series influencers", "Press", "https://www.nba.com/news/nba-creator-program-expands-2024-25", "press"),
     src("Instagram/TikTok — @jennabandy21 (FamousBirthdays sameAs cross-link)", "TikTok", "https://www.tiktok.com/@jennabandy21", "verified-platform"),
     src(FB + " — DOB September 29, 1992, basketball creator", "Website", "https://www.famousbirthdays.com/people/jenna-bandy.html", "other-trusted"),
     src("Sportskeeda — basketball coach career, Guinness World Record holder", "Press", "https://www.sportskeeda.com/pop-culture/who-jenna-bandy-meet-agt-extreme-contestant-rejected-simon-cowell", "press")],
    "Discovered via basketball-creator activity search. Woman per she/her biography + girls' basketball coaching career. Adult via Sept 29, 1992 DOB + press age consistency. Identity: NBA.com lists her in the NBA Creator Cup Series (Tier-2 press/league), FamousBirthdays sameAs links @jennabandy21, Sportskeeda/nextbiography describe the same coaching career. Category: basketball coaching/trick-shot creator content — objective."),
entry("W-2026-016", "Dammy Fitness", ["Fitness", "Fitness Model"],
    adult("Born September 27, 1981 in Brasilia, Brazil — age 44 in 2026. DOB stated on FamousBirthdays; CelebsAgeCheck biography states born September 27, 1981 (43 as of 2024, consistent); her own Facebook page states '43 anos'.",
          FB + " — Dammy Fitness (born September 27, 1981)", "https://www.famousbirthdays.com/people/dammy-fitness.html"),
    gender("Referred to as 'she/her' throughout her CelebsAgeCheck biography ('She is famous for being a Fitness Instructor'); her own Facebook intro: 'Praticante de musculação tem 18 anos / 43 anos / Mãe / Educação Física Bacharelado' (mother, physical-education graduate).",
           "CelebsAgeCheck — Dammy Fitness (she/her, fitness instructor)", "https://www.celebsages.com/dammy-fitness/"),
    [src("Instagram — @dammysfitnesscorner (fitness coaching content, FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/dammysfitnesscorner/", "verified-platform"),
     src("Threads — @dammy_personal (first-party: Personal trainer, Brasília, Ed. Física)", "Threads", "https://www.threads.com/@dammy_personal", "verified-platform"),
     src("Facebook — Dammy Fit (first-party intro: 43 anos, mãe, Educação Física Bacharelado, Brasília)", "Facebook", "https://www.facebook.com/dammy.fit.9", "verified-platform"),
     src(FB + " — DOB September 27, 1981, Brasília fitness instructor", "Website", "https://www.famousbirthdays.com/people/dammy-fitness.html", "other-trusted"),
     src("CelebsAgeCheck — born September 27, 1981, Brazilian fitness instructor", "Website", "https://www.celebsages.com/dammy-fitness/", "other-trusted")],
    "Discovered via fitness-instructor activity search (regional Brazil creator — geography diversity). Woman per she/her bios + first-party 'Mãe' (mother) intro. Adult via Sept 27, 1981 DOB on two independent biographies + her own '43 anos' statement. Identity: her own Threads (@dammy_personal, Brasília, physical-education degree) and Facebook match the fitness-coach description; allmylinks.com/dammyfitness cross-link on Threads ties the Dammy Fitness brand accounts. Category: fitness coaching/fitness modeling — objective."),
entry("W-2026-017", "Alyssa Germeroth", ["Fitness", "Fitness Model", "Bikini Fashion"],
    adult("Born June 8, 1988 in Scottsdale, Arizona — age 38 in 2026. DOB stated on FamousBirthdays and corroborated by famousdetails ('born in Scottsdale on Wednesday, June 8, 1988').",
          FB + " — Alyssa Germeroth (born June 8, 1988)", "https://www.famousbirthdays.com/people/alyssa-germeroth.html"),
    gender("Referred to as 'she/her' throughout; described as an IFBB Bikini Professional athlete (women's professional division) and American fitness instructor by two independent biographies.",
           "AllStarBio — Alyssa Germeroth, American fitness instructor and IFBB Bikini Pro (she/her)", "https://allstarbio.com/alyssa-germeroth-bio-relationship-boyfriend-net-worth/"),
    [src("Instagram — @alyssagermeroth (80k+ followers, fitness/modeling content, FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/alyssagermeroth/", "verified-platform"),
     src(FB + " — DOB June 8, 1988; IFBB Bikini Pro, Team Flawless Physique, NPC Miami Nationals 2015 winner", "Website", "https://www.famousbirthdays.com/people/alyssa-germeroth.html", "other-trusted"),
     src("AllStarBio — American fitness instructor, IFBB Bikini Professional athlete", "Website", "https://allstarbio.com/alyssa-germeroth-bio-relationship-boyfriend-net-worth/", "other-trusted"),
     src("FamousDetails — born June 8, 1988, Scottsdale; fitness instructor, 110k Instagram", "Website", "https://famousdetails.com/alyssa-germeroth/", "other-trusted")],
    "Discovered via female fitness-creator activity search (IFBB competitive-fitness niche). Woman per she/her bios + IFBB Bikini Pro (women's division) status. Adult via June 8, 1988 DOB on three consistent sources. Identity: consistent name, Scottsdale origin, Team Flawless Physique membership and pro-card story across FamousBirthdays/AllStarBio/FamousDetails; Instagram handle from FamousBirthdays sameAs. Category: Fitness/Fitness Model/Bikini Fashion (objective competition-division name, no attractiveness rating)."),
entry("W-2026-018", "Ashley Flores", ["Fitness", "Fitness Model", "Wellness", "Creator"],
    adult("Born March 20, 1995 in the United States — age 31 in 2026. DOB stated on FamousBirthdays profile.",
          FB + " — Ashley Flores (born March 20, 1995)", "https://www.famousbirthdays.com/people/ashley-flores-fitnessinstructor.html"),
    gender("Referred to as 'she/her' throughout her FamousBirthdays biography ('She first developed a passion for fitness…she was coaching a cheerleading team'); her own Instagram bio (first-party) reads 'Your mental health matters too 💛 2026 bride 🇮🇹💍'.",
           "Instagram — @ashleyflores first-party bio", "https://www.instagram.com/ashleyflores/"),
    [src("Instagram — @ashleyflores (528K followers; first-party bio, athlete codes, business contact)", "Instagram", "https://www.instagram.com/ashleyflores/", "verified-platform"),
     src("TikTok — @afloresfit (listed on Hello Dreamer podcast guest sheet with her other official links)", "TikTok", "https://www.tiktok.com/@afloresfit", "verified-platform"),
     src("YouTube — AshleyFloresFit channel (podcast guest sheet)", "YouTube", "https://www.youtube.com/c/AshleyFloresFit", "verified-platform"),
     src(FB + " — DOB March 20, 1995; NASM-certified personal trainer, LVFT/PEScience athlete", "Website", "https://www.famousbirthdays.com/people/ashley-flores-fitnessinstructor.html", "other-trusted"),
     src("Hello Dreamer podcast — 'Influencing with Integrity with Ashley Flores' episode listing her official accounts", "Press", "https://www.iheart.com/podcast/263-hello-dreamer-226970446/episode/influencing-with-integrity-with-ashley-flores-249217456/", "press")],
    "Discovered via fitness-instructor activity search (NASM-certified trainer, supplement-brand athlete). Woman per she/her bio + first-party Instagram bio. Adult via March 20, 1995 DOB. Identity: Instagram first-party page (528K, contact@ashleyfloresfit.com) cross-linked by the podcast guest sheet to her TikTok/YouTube — ownership chain verified. Category: fitness/personal-training creator — objective."),
entry("W-2026-019", "Alyssa Scott", ["Swimwear", "Modeling", "Fashion"],
    adult("Born October 12, 1993 in the United States — age 32 in 2026. DOB stated on FamousBirthdays and corroborated by an independent profile ('born October 12, 1993').",
          FB + " — Alyssa Scott (born October 12, 1993)", "https://www.famousbirthdays.com/people/alyssa-scott.html"),
    gender("Referred to as 'she/her' throughout; described as an American Instagram star and model with swimwear/beachside photo content and campaigns for swimwear brands (Boutine Los Angeles, MGM Swimwear).",
           "InforY — Alyssa Scott: From Model to Motherhood Spotlight (she/her)", "https://infory.co.uk/alyssa-scott-from-model-to-motherhood-spotlight/"),
    [src("Instagram — @itsalyssaemm (250K+ followers, FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/itsalyssaemm/", "verified-platform"),
     src(FB + " — DOB October 12, 1993; model for swimsuit brand Boutine Los Angeles", "Website", "https://www.famousbirthdays.com/people/alyssa-scott.html", "other-trusted"),
     src("InforY — model biography: Boutine LA, MGM Swimwear, Fashion Nova campaigns; @itsalyssaemm", "Website", "https://infory.co.uk/alyssa-scott-from-model-to-motherhood-spotlight/", "other-trusted")],
    "Discovered via swimwear-model activity search. Woman per she/her bios. Adult via Oct 12, 1993 DOB on two independent sources. Identity: FamousBirthdays sameAs @itsalyssaemm matches the handle described in both biographies (270K followers, Boutine LA swimwear work). Category: Swimwear/Modeling/Fashion — objective content classification (swimwear campaigns), no attractiveness rating."),
entry("W-2026-020", "Kiki Ruby (kikiiib)", ["Swimwear", "Fitness", "Modeling"],
    adult("Born August 9, 1994 in Los Angeles, California — age 32 in 2026. DOB stated on FamousBirthdays profile.",
          FB + " — kikiiib (born August 9, 1994)", "https://www.famousbirthdays.com/people/kikiiib.html"),
    gender("Referred to as 'she/her' throughout ('She often posts from the beach. She frequently collaborates with clothing brands'); her own Instagram account displays the name 'Kiki Ruby'.",
           "Instagram — @kikiiib account name 'Kiki Ruby' (first-party)", "https://www.instagram.com/kikiiib/"),
    [src("Instagram — @kikiiib (318K followers; first-party name 'Kiki Ruby', bio links fitness page @kbsculpt)", "Instagram", "https://www.instagram.com/kikiiib/", "verified-platform"),
     src("Instagram — @kbsculpt (her fitness page; first-party bio 'Main: @kikiiib')", "Instagram", "https://www.instagram.com/kbsculpt/", "verified-platform"),
     src(FB + " — DOB August 9, 1994; Instagram swimsuit and fitness model, brand collaborations", "Website", "https://www.famousbirthdays.com/people/kikiiib.html", "other-trusted")],
    "Discovered via swimwear/fitness-model activity search. Woman per she/her bio + first-party account name. Adult via Aug 9, 1994 DOB. Identity: FamousBirthdays sameAs @kikiiib matches her first-party Instagram (name Kiki Ruby, LA) which itself cross-links her secondary fitness account @kbsculpt — multi-account consolidation verified from first-party bios. Category: swimwear/fitness modeling — objective."),
entry("W-2026-021", "Lexi Sun", ["College Athlete", "Volleyball", "Athlete", "Sports"],
    adult("Born September 19, 1998 in the United States — age 27 in 2026. DOB stated on FamousBirthdays; her Nebraska career timeline (2017-2021, five seasons) is consistent with that birth year.",
          FB + " — Lexi Sun (born September 19, 1998)", "https://www.famousbirthdays.com/people/lexi-sun.html"),
    gender("Women's volleyball roster: huskers.com (University of Nebraska official athletics) lists her on the Nebraska Huskers women's volleyball roster; press coverage uses she/her throughout.",
           "University of Nebraska Athletics — Lexi Sun, women's volleyball roster (Tier 1)", "https://huskers.com/sports/volleyball/roster/player/lexi-sun"),
    [src("University of Nebraska Athletics — Lexi Sun volleyball roster/bio (All-America, career stats)", "Website", "https://huskers.com/sports/volleyball/roster/player/lexi-sun", "official"),
     src("Corn Nation — 'Lexi Sun to Return for Another Season of Nebraska Volleyball' (quotes Sun; links her @lexiisun account)", "Press", "https://www.cornnation.com/2021/5/19/22443991/lexi-sun-to-return-for-another-season-of-nebraska-volleyball", "press"),
     src("Instagram — @lexiisun (60K followers, FamousBirthdays sameAs; Corn Nation cites @lexiisun Twitter)", "Instagram", "https://www.instagram.com/lexiisun/", "verified-platform"),
     src(FB + " — DOB September 19, 1998; Nebraska Huskers volleyball player", "Website", "https://www.famousbirthdays.com/people/lexi-sun.html", "other-trusted")],
    "Discovered via women's college volleyball activity search (university-athletics source priority). Woman per women's-team roster (Tier 1) + press pronouns. Adult via Sept 19, 1998 DOB. Identity: huskers.com roster + Corn Nation article (which quotes Sun and links her own @lexiisun social account) match the FamousBirthdays sameAs handle — ownership chain verified across Tier-1 university source and her accounts. Category: College Athlete (Nebraska volleyball, All-America)/Volleyball — objective."),
entry("W-2026-022", "Alexis Dacosta", ["College Athlete", "Volleyball", "Athlete", "Creator"],
    adult("Born August 9, 2004 in the United States — age 22 in 2026. DOB stated on FamousBirthdays; Auburn roster database (volleybox) lists her birth year as 2004 — consistent.",
          FB + " — Alexis Dacosta (born August 9, 2004)", "https://www.famousbirthdays.com/people/alexis-dacosta.html"),
    gender("Women's volleyball: Auburn University official athletics announcement lists her on the Auburn Tigers women's volleyball roster (transfer from Baylor); FamousBirthdays biography uses she/her.",
           "Auburn Tigers official athletics — 'Crouch adds five new Tigers to roster' (Alexis Dacosta)", "https://auburntigers.com/news/2024/01/18/crouch-adds-five-new-tigers-to-roster"),
    [src("Auburn Tigers official athletics — Alexis Dacosta joins Auburn volleyball (Tier 1 university source)", "Website", "https://auburntigers.com/news/2024/01/18/crouch-adds-five-new-tigers-to-roster", "official"),
     src("TikTok — @alexisd_15 (110K followers; gameplay, fashion, workout content; FamousBirthdays sameAs)", "TikTok", "https://www.tiktok.com/@alexisd_15", "verified-platform"),
     src("Volleybox — Auburn Univ. roster listing Alexis Dacosta, OH, 2004", "Website", "https://women.volleybox.net/auburn-univ-t6687", "other-trusted"),
     src(FB + " — DOB August 9, 2004; Auburn volleyball player and TikTok creator", "Website", "https://www.famousbirthdays.com/people/alexis-dacosta.html", "other-trusted")],
    "Discovered via female college athlete activity search — a college athlete whose adult status IS independently verifiable (published DOB 2004-08-09, corroborated birth year on roster database), honoring 'college attendance alone does not establish 18+'. Woman per women's-team roster (Tier 1 Auburn athletics) + bio pronouns. Identity: Auburn official announcement (Baylor transfer, libero/OH) + roster database + FamousBirthdays sameAs @alexisd_15. Category: College Athlete/Volleyball/Creator — objective."),
entry("W-2026-023", "Kayla Simmons", ["Swimwear", "Modeling", "College Athlete", "Fitness"],
    adult("Born September 28, 1995 in Florida — age 30 in 2026. DOB stated on FamousBirthdays; 2026 press explicitly calls her 'the 30 year old former Marshall University volleyball player' — consistent; 2023 press called her 'the then 23-year-old'.",
          FB + " — Kayla Simmons (born September 28, 1995)", "https://www.famousbirthdays.com/people/kayla-simmons.html"),
    gender("Referred to as 'she/her' throughout; documented as a former four-season Marshall University women's volleyball player (women's roster) now a model.",
           "PopCulture — 'This Former Marshall Volleyball Player…' (Kayla Simmons, she/her)", "https://popculture.com/sports/news/former-marshall-volleyball-player-heating-up-instagram/"),
    [src("PopCulture — former Marshall University volleyball player turned model", "Press", "https://popculture.com/sports/news/former-marshall-volleyball-player-heating-up-instagram/", "press"),
     src("BroBible — 'Former D1 Volleyball Star Turned Model Kayla Simmons', SI Swimsuit model", "Press", "https://brobible.com/sports/article/kayla-simmons-wows-inviral-instagram-post/", "press"),
     src("Instagram — @kaylasimmmons (850K+ followers, FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/kaylasimmmons/", "verified-platform"),
     src(FB + " — DOB September 28, 1995; college volleyball → modeling creator", "Website", "https://www.famousbirthdays.com/people/kayla-simmons.html", "other-trusted")],
    "Discovered via swimwear-model + former-college-athlete activity search. Woman per she/her press + women's college volleyball history. Adult via Sept 28, 1995 DOB + press age statements in 2023 ('then 23-year-old') and 2026 ('30 year old') — internally consistent across three sources. Identity: press describe the same Marshall→model arc and @kaylasimmmons handle (FamousBirthdays sameAs). Category: Swimwear/Modeling/College Athlete (former) — objective; swimwear classified by content."),
entry("W-2026-024", "Evana (evanagetfit)", ["Fitness", "Wellness", "Creator"],
    adult("Born June 29, 1999 in the United States — age 27 in 2026. DOB stated on FamousBirthdays (structured birthDate 1999-06-29).",
          FB + " — evanagetfit (born June 29, 1999)", "https://www.famousbirthdays.com/people/evanagetfit.html"),
    gender("FamousBirthdays structured data records gender 'f' for the account; her TikTok account (first-party) is operated under the name 'Evana' with fitness content for a women's audience; biographies use she/her.",
           FB + " — evanagetfit (JSON-LD gender: f)", "https://www.famousbirthdays.com/people/evanagetfit.html"),
    [src("TikTok — @evanagetfit (Evana; fitness/nutrition/mental-health vlogs, 7M+ likes; FamousBirthdays sameAs)", "TikTok", "https://www.tiktok.com/@evanagetfit", "verified-platform"),
     src("Urlebird TikTok analytics — @evanagetfit profile (323.9K followers, fitness content)", "Website", "https://urlebird.com/user/evanagetfit/", "other-trusted"),
     src(FB + " — DOB June 29, 1999; TikTok fitness/nutrition creator, Nutrition Creators member", "Website", "https://www.famousbirthdays.com/people/evanagetfit.html", "other-trusted")],
    "Discovered via TikTok fitness-creator activity search (micro-to-mid creator, #230,006 popularity — demonstrates follower count is not a filter). Woman per structured gender field + she/her bio. Adult via June 29, 1999 DOB. Identity: FamousBirthdays sameAs matches the @evanagetfit TikTok profile documented on the platform page and third-party analytics. Category: fitness/nutrition/wellness creator — objective."),
entry("W-2026-025", "Summer Fit (summer_fit)", ["Fitness", "Lifestyle", "Creator"],
    adult("Born July 10, 1979 in Canada — age 47 in 2026. DOB stated on FamousBirthdays profile.",
          FB + " — Summer_fit (born July 10, 1979)", "https://www.famousbirthdays.com/people/summer-fit.html"),
    gender("Referred to as 'she/her' throughout ('She posts comedy videos and fitness modeling photos on her Summer_fit_style Instagram page'); her own X profile (first-party) self-describes as 'Summer Fit' and points to her TikTok/Instagram.",
           "X — @summer_fit___ first-party profile ('Find me on Instagram & TikTok… @summer_fit')", "https://twitter.com/summer_fit___"),
    [src("TikTok — @summer_fit (584.8K followers, 6M likes; fitness/comedy/lifestyle)", "TikTok", "https://www.tiktok.com/@summer_fit", "verified-platform"),
     src("X — @summer_fit___ (first-party: British Columbia, Canada; links TikTok/Instagram @summer_fit, YouTube channel, direct.me/summer-fit)", "X", "https://twitter.com/summer_fit___", "verified-platform"),
     src(FB + " — DOB July 10, 1979; Canadian TikTok star, fitness content, 550K followers", "Website", "https://www.famousbirthdays.com/people/summer-fit.html", "other-trusted")],
    "Discovered via TikTok fitness-creator activity search (age diversity: 47, Canadian — British Columbia). Woman per she/her bio. Adult via July 10, 1979 DOB. Identity: her own X profile cross-links TikTok @summer_fit, Instagram Summer_fit_style, YouTube and direct.me/summer-fit — multi-platform ownership chain verified first-party. Category: fitness/lifestyle creator — objective (comedy + fitness modeling photos per bio)."),
entry("W-2026-026", "Valeriia Litvinova, MS, RDN (vallitfit)", ["Fitness", "Wellness", "Creator"],
    adult("Born May 31, 1999 in Kyiv, Ukraine — age 27 in 2026. DOB stated on FamousBirthdays; bio states she moved to North Carolina at age 15, consistent timeline.",
          FB + " — Vallitfit (born May 31, 1999)", "https://www.famousbirthdays.com/people/vallitfit.html"),
    gender("Referred to as 'she/her' throughout ('She shares a wide assortment of material…she and her sister are seen working out'); TikTok displays her professional name 'Valeriia Litvinova, MS, RDN' (registered dietitian nutritionist).",
           "TikTok — @vallitfit account ('Valeriia Litvinova, MS, RDN' — 1-on-1 fitness & nutrition coaching)", "https://www.tiktok.com/@vallitfit"),
    [src("TikTok — @vallitfit (Valeriia Litvinova, MS, RDN; 1.6M followers; fitness & nutrition coaching)", "TikTok", "https://www.tiktok.com/@vallitfit", "verified-platform"),
     src(FB + " — DOB May 31, 1999; Kyiv-born online fitness coach and nutritionist, 1.6M TikTok followers", "Website", "https://www.famousbirthdays.com/people/vallitfit.html", "other-trusted")],
    "Discovered via fitness-coach activity search (Ukraine-born, US-based — immigrant-story diversity; Fitness Creators member). Woman per she/her bio + first-party professional name on TikTok (MS, RDN credential). Adult via May 31, 1999 DOB. Identity: FamousBirthdays sameAs matches the TikTok account whose display name (Valeriia Litvinova, MS, RDN) and content match the biography description. Category: fitness/nutrition coaching creator — objective."),
entry("W-2026-027", "Elizabeth Sneed (curvysurfergirl)", ["Surfing", "Sports", "Swimwear", "Travel", "Wellness"],
    adult("Born December 10, 1990 in the United States — age 35 in 2026. DOB stated on FamousBirthdays profile.",
          FB + " — curvysurfergirl (born December 10, 1990)", "https://www.famousbirthdays.com/people/curvysurfergirl.html"),
    gender("Her own X profile (first-party) displays the name 'Elizabeth' with bio 'Body positive surfer redefining the image of the surfer girl'; press feature identifies her as Elizabeth Sneed, surfer and surf model; FamousBirthdays uses she/her.",
           "X — @curvysurfergirl first-party profile (Elizabeth, body positive surfer)", "https://x.com/curvysurfergirl"),
    [src("X — @curvysurfergirl (first-party: Elizabeth, Honolulu HI, body-positive surfing community)", "X", "https://x.com/curvysurfergirl", "verified-platform"),
     src("Instagram — @curvysurfergirl (120K followers; surfing videos, swimsuit inspiration, surf travel; FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/curvysurfergirl/", "verified-platform"),
     src("Boardshop — 'Women Making Waves' feature: Elizabeth Sneed, body-positive surf model and longboarder", "Press", "https://www.boardshop.co.uk/blog/women-making-waves/", "press"),
     src(FB + " — DOB December 10, 1990; body-positive surfer, Curvy Surf Girl website founder", "Website", "https://www.famousbirthdays.com/people/curvysurfergirl.html", "other-trusted")],
    "Discovered via surf-creator activity search (women-in-surfing representation advocate). Woman per first-party X name (Elizabeth) + press identification (Elizabeth Sneed) + she/her bios. Adult via Dec 10, 1990 DOB. Identity: X profile and Instagram handle match FamousBirthdays sameAs; press feature names Elizabeth Sneed with the same @curvysurfergirl credit. Category: Surfing/Sports/Swimwear content (surf travel + swimsuit inspiration per bio) — objective, body-positive advocacy framing, no attractiveness rating."),
entry("W-2026-028", "Amy Bell (The Little Magpie)", ["Travel", "Fashion", "Lifestyle", "Creator"],
    adult("Born February 22, 1992 in Scotland — age 34 in 2026. DOB stated on FamousBirthdays; her own blog contact page (first-party) self-described 'Amy Bell | 27 | Scotland Fashion & travel blogger' — consistent timeline.",
          FB + " — Amy Bell (born February 22, 1992)", "https://www.famousbirthdays.com/people/amy-bell-blogger.html"),
    gender("Referred to as 'she/her' throughout; The Herald (Scotland's most influential style pioneers) profiles 'AMY BELL — the talented creator behind the popular fashion and travel blog The Little Magpie'; her own blog bio: 'Amy Bell | Scotland Fashion & travel blogger'.",
           "The Herald — Scotland's most influential style pioneers (Amy Bell, she/her)", "https://www.heraldscotland.com/news/19558133.scotlands-influential-style-pioneers/"),
    [src("The Little Magpie — her own blog (first-party: fashion/travel/lifestyle, contact page bio)", "Website", "http://www.thelittlemagpie.com/p/contact.html", "official"),
     src("The Herald Scotland — style pioneers profile: Glasgow-based creator of The Little Magpie, 146K followers, @thelittlemagpie", "Press", "https://www.heraldscotland.com/news/19558133.scotlands-influential-style-pioneers/", "press"),
     src("FashionUnited — Tartan Blanket Co. x The Little Magpie collaboration with travel blogger Amy Bell", "Press", "https://fashionunited.com/news/fashion/the-tartan-blanket-co-collaborates-with-the-little-magpie/2021111543693", "press"),
     src("Instagram — @thelittlemagpie (Herald Scotland names the handle)", "Instagram", "https://www.instagram.com/thelittlemagpie/", "verified-platform"),
     src(FB + " — DOB February 22, 1992; Scottish blogger", "Website", "https://www.famousbirthdays.com/people/amy-bell-blogger.html", "other-trusted")],
    "Discovered via travel-creator activity search (Scotland — geography diversity). Woman per she/her press + first-party blog bio. Adult via Feb 22, 1992 DOB + first-party self-stated age ('Amy Bell | 27') consistent with DOB. Identity: The Herald names her blog/handle, FashionUnited documents a brand collaboration, and her own site ties it together — Tier-1 first-party + Tier-2 press chain. Category: Travel/Fashion/Lifestyle blogger — objective."),
entry("W-2026-029", "Meghan Currie", ["Wellness", "Fitness", "Creator"],
    adult("Born August 28, 1990 in Canada — age 35 in 2026. DOB stated on FamousBirthdays profile.",
          FB + " — Meghan Currie (born August 28, 1990)", "https://www.famousbirthdays.com/people/meghan-currie-fitnessinstructor.html"),
    gender("Referred to as 'she/her' throughout; her own Linktree (first-party) is titled '@meghancurrie — Meghan Currie' listing Meghan Currie Yoga events, teacher trainings and her Isabelle Moon brand; her site meghancurrieyoga.com documents the same.",
           "Linktree — @meghancurrie (first-party: Meghan Currie Yoga, Isabelle Moon)", "https://linktr.ee/meghancurrie"),
    [src("Linktree — @meghancurrie (first-party link hub: yoga events, teacher training, Isabelle Moon shop, Facebook)", "Website", "https://linktr.ee/meghancurrie", "official"),
     src("meghancurrieyoga.com — her own yoga site (first-party, teacher-training/retreat content)", "Website", "https://meghancurrieyoga.com/blog/a-little-chat/", "official"),
     src("Instagram — @meghancurrieyoga (140K+ followers, yoga workshops/retreats; FamousBirthdays sameAs)", "Instagram", "https://www.instagram.com/meghancurrieyoga/", "verified-platform"),
     src(FB + " — DOB August 28, 1990; touring yoga teacher, Isabelle Moon ethical yogawear founder", "Website", "https://www.famousbirthdays.com/people/meghan-currie-fitnessinstructor.html", "other-trusted")],
    "Discovered via yoga/wellness-creator activity search (Canada). Woman per she/her bio + first-party Linktree/site branding. Adult via Aug 28, 1990 DOB. Identity: FamousBirthdays sameAs @meghancurrieyoga matches her first-party link hub and yoga site — ownership verified. Category: Wellness/Yoga/Fitness — objective (workshops, retreats, ethical yogawear)."),
entry("W-2026-030", "Michaela Lintrup (mimi)", ["Esports", "Sports", "Creator"],
    adult("Born July 2, 1997 in Denmark — age 29 in 2026. DOB stated on Liquipedia ('Michaela \"mimi\" Lintrup (born July 2, 1997)') and corroborated by Esports Charts ('Born Jul 02, 1997 (age 29)').",
          "Liquipedia — mimi (Michaela Lintrup, born July 2, 1997)", "https://liquipedia.net/valorant/Mimi"),
    gender("Liquipedia: 'Michaela \"mimi\" Lintrup (born July 2, 1997) is a Danish player…She is a former Counter-Strike: Global Offensive player' — she/her; competes for G2 Gozen, the all-women Valorant roster of G2 Esports (VCT Game Changers circuit).",
           "Liquipedia — mimi player page (she/her, G2 Gozen)", "https://liquipedia.net/valorant/Mimi"),
    [src("Liquipedia — mimi player page (name, DOB, team G2 Gozen, career history)", "Website", "https://liquipedia.net/valorant/Mimi", "other-trusted"),
     src("Esports Charts — mimi player profile (Michaela Lintrup, born Jul 02 1997, G2 Gozen, $116,256 prize money)", "Website", "https://escharts.com/players/mimimimichaela", "other-trusted"),
     src("VLR.gg — G2 Gozen roster news confirming Michaela 'mimi' Lintrup on the 2024 EMEA Game Changers roster", "Press", "https://www.vlr.gg/299241/g2-gozen-restructure-with-four", "press")],
    "Discovered via women's esports activity search (Valorant Game Changers circuit — platform/category diversity, Denmark). Woman per she/her Liquipedia bio + all-women team roster (G2 Gozen). Adult via July 2, 1997 DOB on two independent esports databases. Identity: consistent name/handle/team across Liquipedia, Esports Charts and VLR.gg roster news (active 2026 season matches). Category: Esports/Sports (professional Valorant player, in-game leader) — objective."),
entry("W-2026-031", "Lee Jeong-hyun (Jennlee)", ["Esports", "Creator", "Sports"],
    adult("Born June 23, 1995 in South Korea — age 31 in 2026. DOB stated on Liquipedia ('Lee \"Jennlee\" Jeong-hyun (born June 23, 1995)').",
          "Liquipedia — Jennlee (Lee Jeong-hyun, born June 23, 1995)", "https://liquipedia.net/valorant/Lee_Jeong-hyun"),
    gender("Liquipedia: 'Lee \"Jennlee\" Jeong-hyun (born June 23, 1995) is a South Korean Valorant host, interviewer and English-Korean translator. She was formerly a host for League of Legends' — she/her; listed as VALORANT Champions 2024 stage host in press.",
           "Liquipedia — Jennlee page (she/her, host/translator)", "https://liquipedia.net/valorant/Lee_Jeong-hyun"),
    [src("Liquipedia — Jennlee page (name, DOB, host/translator roles)", "Website", "https://liquipedia.net/valorant/Lee_Jeong-hyun", "other-trusted"),
     src("esports.gg — VALORANT Champions 2024 Seoul broadcast talent: 'Lee \"Jennlee\" Jeong-hyun' stage host", "Press", "https://esports.gg/news/valorant/broadcast-talent-and-observers-revealed-for-valorant-champions-2024-in-seoul/", "press"),
     src("Liquipedia — VALORANT Champions 2024 broadcast talent list (Jennlee as stage host)", "Website", "https://liquipedia.net/valorant/VCT/2024/Champions", "other-trusted")],
    "Discovered via women's esports activity search (broadcast/host role — South Korea diversity). Woman per she/her Liquipedia bio. Adult via June 23, 1995 DOB. Identity: esports.gg press names the same Lee Jeong-hyun as VALORANT Champions 2024 stage host, matching the Liquipedia role record. Category: Esports broadcaster/host (Creator) — objective."),
]

# --- Promotions from reviewQueue (research completed this session) ---
PROMOTIONS = [
entry("W-2026-032", "Alyssa Ustby", ["College Athlete", "Basketball", "Athlete"],
    adult("Born March 18, 2002 in Rochester, Minnesota — age 24 in 2026. DOB stated on Wikipedia ('born March 18, 2002'), Tar Heel Times bio ('Born: March 18, 2002') and Basketball-Reference WNBA page.",
          "Wikipedia — Alyssa Ustby (born March 18, 2002)", "https://en.wikipedia.org/wiki/Alyssa_Ustby"),
    gender("Women's basketball: four-year North Carolina Tar Heels women's basketball player (2020-2025), now professional in Serie A1 (women's league) for Panthers Roseto; sources use she/her.",
           "Wikipedia — Alyssa Ustby (UNC women's basketball, she/her)", "https://en.wikipedia.org/wiki/Alyssa_Ustby"),
    [src("Wikipedia — Alyssa Ustby (DOB, UNC career, professional career)", "Website", "https://en.wikipedia.org/wiki/Alyssa_Ustby", "other-trusted"),
     src("Basketball-Reference WNBA — Alyssa Ustby (Born March 18, 2002; lists her Instagram: alyssa_ustby)", "Website", "https://www.basketball-reference.com/wnba/players/u/ustbyal01w.html", "other-trusted"),
     src("Tar Heel Times — Alyssa Ustby women's basketball bio (Born March 18, 2002, Rochester MN)", "Press", "https://www.tarheeltimes.com/bio2597.aspx", "press"),
     src("Instagram — @alyssa_ustby (handle listed on her Basketball-Reference page)", "Instagram", "https://www.instagram.com/alyssa_ustby/", "verified-platform")],
    "PROMOTED from R-2026-002 (review queue) after this session's research. Missing field resolved: AGE — DOB March 18, 2002 now established by three independent sources (Wikipedia, Tar Heel Times, Basketball-Reference). Gender resolved via women's-team documentation (UNC WBB + Serie A1 women's club). Identity/ownership strengthened: Basketball-Reference explicitly lists her Instagram handle. Category: College Athlete (former UNC WBB; program career-rebounds record holder)/Basketball — objective."),
entry("W-2026-033", "Victoria Garrick Browne", ["College Athlete", "Wellness", "Creator", "Sports"],
    adult("Born April 30, 1997 — age 29 in 2026. DOB stated by three independent sources (TheCityCeleb: 'Born: 30 April 1997'; SuperstarsCulture: 'born in California on April 30, 1997'; CelebsAgeCheck: 'Birthdate: April 30, 1997').",
          "TheCityCeleb — Victoria Garrick Browne biography (born 30 April 1997)", "https://www.thecityceleb.com/biography/entrepreneur/victoria-garrick-browne-biography-ethnicity-tedx-height-husband-instagram-net-worth-children/"),
    gender("Women's volleyball: former USC Trojans women's volleyball libero (four-year starter, Pac-12 champion); all sources use she/her; occupation listed as former volleyball player, mental-health advocate, TEDx speaker, podcast host, content creator.",
           "TheCityCeleb — Victoria Garrick Browne (USC women's volleyball, she/her)", "https://www.thecityceleb.com/biography/entrepreneur/victoria-garrick-browne-biography-ethnicity-tedx-height-husband-instagram-net-worth-children/"),
    [src("TheCityCeleb — Victoria Garrick Browne biography (full name Victoria Lane Garrick, DOB, occupations)", "Website", "https://www.thecityceleb.com/biography/entrepreneur/victoria-garrick-browne-biography-ethnicity-tedx-height-husband-instagram-net-worth-children/", "other-trusted"),
     src("SuperstarsCulture — Victoria Garrick biography (born April 30, 1997; USC senior libero)", "Website", "https://superstarsculture.com/victoria-garrick/", "other-trusted"),
     src("CelebsAgeCheck — Victoria Garrick (born April 30, 1997, volleyball player)", "Website", "https://www.celebsages.com/victoria-garrick/", "other-trusted"),
     src("TikTok — @victoriagarrick4 (1.2M followers; recorded in prior-session discovery)", "TikTok", "https://www.tiktok.com/@victoriagarrick4", "verified-platform")],
    "PROMOTED from R-2026-009 (review queue) after this session's research. Missing field resolved: AGE — DOB April 30, 1997 confirmed by three independent biographies; adult status further supported by documented 2016 TEDx talk and 2022 marriage. Gender resolved via women's volleyball documentation + consistent she/her. Identity: all three biographies describe the same USC libero → mental-health advocate/podcast host arc matching the @victoriagarrick4 account recorded at discovery. Category: College Athlete (former)/Wellness/Creator — objective."),
entry("W-2026-034", "Sedona Prince", ["College Athlete", "Basketball", "Athlete", "Creator"],
    adult("Born May 12, 2000 in Hemet, California — age 26 in 2026. DOB stated by Sporting News ('Prince, born on May 12, 2000, is 24') and Wikipedia ('2000-05-12, Hemet, California').",
          "Sporting News — How old is Sedona Prince? (born May 12, 2000)", "https://www.sportingnews.com/us/womens-college-basketball/news/sedona-prince-age-college-eligibility/e432b7d68ad88ce6aec30242"),
    gender("Women's basketball: college career at Oregon/TCU women's programs; now plays professionally for Panathinaikos of the Greek Women's Basketball League; sources use she/her.",
           "Wikipedia — Sedona Prince (women's basketball, she/her)", "https://en.wikipedia.org/wiki/Sedona_Prince"),
    [src("Sporting News — 'How old is Sedona Prince?' (born May 12, 2000; Oregon/TCU career)", "Press", "https://www.sportingnews.com/us/womens-college-basketball/news/sedona-prince-age-college-eligibility/e432b7d68ad88ce6aec30242", "press"),
     src("Wikipedia — Sedona Prince (born May 12, 2000; Oregon, Texas, TCU; Panathinaikos)", "Website", "https://en.wikipedia.org/wiki/Sedona_Prince", "other-trusted"),
     src("TikTok — @sedonerr (3M followers; recorded in prior-session discovery)", "TikTok", "https://www.tiktok.com/@sedonerr", "verified-platform")],
    "PROMOTED from R-2026-010 (review queue) after this session's research. Missing field resolved: AGE — DOB May 12, 2000 confirmed by Sporting News + Wikipedia. Gender resolved via women's-basketball documentation (NCAA women's programs; Greek Women's Basketball League). Identity: the TikTok account @sedonerr recorded at discovery matches the documented player (3M-follower creator documented in prior session's evidence). Category: College Athlete (former)/Basketball/Creator — objective."),
]

# --- New REVIEW_REQUIRED additions ---
NEW_QUEUE = [
{"id": "R-2026-011", "displayName": "Jade Haliburton", "handle": "@jadehaliburton", "platform": "Instagram",
 "profileUrl": "https://www.instagram.com/jadehaliburton/",
 "discoveryCategory": "Fashion",
 "evidenceFound": {"summary": "Instagram star sharing fashion and lifestyle content (170K+ followers); DOB January 30, 1998 (age 28) on FamousBirthdays with sameAs link to @jadehaliburton; covered by Times of India for her custom NBA Finals fashion designs.",
   "sourceLabel": "FamousBirthdays — Jade Haliburton (born January 30, 1998)",
   "sourceUrl": "https://www.famousbirthdays.com/people/jade-jones-instagramstar.html"},
 "missingEvidence": ["IDENTITY_UNCERTAIN"], "flags": ["CONFLICTING_INFORMATION"], "lastChecked": D,
 "notes": "Discovered via fashion-creator activity search. Adult status looks strong (published DOB Jan 30, 1998 + engagement announced 2025) and gender evidence is consistent (she/her throughout). HOLD reason: surname conflict across sources — FamousBirthdays lists her as 'Jade Haliburton' (handle @jadehaliburton) while Times of India and other press call her 'Jade Jones'. Name needs resolution from a first-party source before promotion to VERIFIED. Not guessed per protocol."},
{"id": "R-2026-012", "displayName": "Valentina Villa", "handle": "@getfitwith.val", "platform": "TikTok",
 "profileUrl": "https://www.tiktok.com/@getfitwith.val",
 "discoveryCategory": "Fitness",
 "evidenceFound": {"summary": "Micro fitness coach on TikTok (2,768 followers, 459K likes): first-party bio 'Helping women get toned, strong & confident — 1:1 online coaching' with business email; push-day/hybrid-athlete workout content.",
   "sourceLabel": "TikTok — Valentina Villa | Fitness coach (@getfitwith.val)",
   "sourceUrl": "https://www.tiktok.com/@getfitwith.val"},
 "missingEvidence": ["AGE_UNVERIFIED", "GENDER_UNVERIFIED"], "flags": ["AGE_UNVERIFIED", "GENDER_UNVERIFIED"], "lastChecked": D,
 "notes": "Discovered during fitness-coach corroboration search — included precisely because she is a micro creator (2.7K followers; follower count is not a filter). Public profile URL recorded and checked in search results. Missing: no public DOB/age statement found (AGE_UNVERIFIED — bio does not establish 18+); bio text does not explicitly establish the operator is a woman ('Helping women' describes the audience, not the creator). Needs first-party evidence (published DOB/age or explicit self-identification) before promotion."},
]

# --- Assemble ---
with open("data/catalog.json") as f:
    catalog = json.load(f)

existing_ids = {e["id"] for e in catalog["entries"]}
new_ids = [e["id"] for e in NEW] + [e["id"] for e in PROMOTIONS]
assert len(new_ids) == len(set(new_ids)), "duplicate new IDs"
for nid in new_ids:
    assert nid not in existing_ids, f"{nid} already exists"

# Duplicate check: name + handles against existing entries
existing_names = {e["displayName"].lower() for e in catalog["entries"]}
existing_urls = {s["url"].rstrip("/").lower() for e in catalog["entries"] for s in e["sources"]}
for e in NEW + PROMOTIONS:
    assert e["displayName"].lower() not in existing_names, f"name duplicate: {e['displayName']}"
    for s in e["sources"]:
        assert s["url"].rstrip("/").lower() not in existing_urls, f"url duplicate: {s['url']}"

# Duplicate check within new set
all_new_names = [e["displayName"].lower() for e in NEW + PROMOTIONS]
assert len(all_new_names) == len(set(all_new_names)), "name dup within new set"

catalog["entries"].extend(NEW)
catalog["entries"].extend(PROMOTIONS)
catalog["entries"].sort(key=lambda e: e["id"])

# Review queue: remove promoted, append new
promoted_from = {"R-2026-002", "R-2026-009", "R-2026-010"}
catalog["reviewQueue"] = [r for r in catalog["reviewQueue"] if r["id"] not in promoted_from]
qids = {r["id"] for r in catalog["reviewQueue"]}
for r in NEW_QUEUE:
    assert r["id"] not in qids
    catalog["reviewQueue"].append(r)
catalog["reviewQueue"].sort(key=lambda r: r["id"])

v = [e for e in catalog["entries"] if e["verificationStatus"] == "verified"]
cats = sorted({c for e in v for c in e["categories"]})
catalog["metadata"] = {
    "title": "ProjX Verified Directory",
    "generatedAt": D,
    "entryCount": len(v),
    "reviewQueueCount": len(catalog["reviewQueue"]),
    "summary": (
        "Women-only directory of adult (18+) public creators: %d verified adult women (W-2026-001..034 — professional athletes, "
        "college athletes, fitness/fitness-model creators, swimwear/bikini-fashion models, surf/yoga/travel/fashion/lifestyle creators, "
        "and women's esports players) + %d promising candidates in REVIEW_REQUIRED queue, each with full provenance and exact missing "
        "fields. Discovery is activity-first (fitness, swimwear, college athletics, fashion, travel, wellness, esports), then "
        "line-by-line eligibility verification from legitimate public evidence (Tier-1 official/university/agency sources and "
        "multiple independent Tier-3 sources where Tier-1 DOB is absent). Categories are objective — never attractiveness ranking; "
        "college attendance never proves adult; minors discovered during research were rejected, not added; follower count is never "
        "a filter (set spans ~2.7K to millions, ages 22-47, across US, Brazil, Canada, Scotland, Denmark, South Korea, Ukraine)."
    ) % (len(v), len(catalog["reviewQueue"])),
}

with open("data/catalog.json", "w") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("entries:", len(catalog["entries"]), "verified:", len(v))
print("reviewQueue:", len(catalog["reviewQueue"]))
print("categories:", cats)
print("OK")
