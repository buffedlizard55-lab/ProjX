#!/usr/bin/env python3
"""Session 24 — High precision expansion script for Volleyball, Fitness, Swimwear, and Modeling.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"
TODAY = date(2026, 9, 6)

sys.path.insert(0, str(ROOT / "scripts"))
import session24_build as s24

# Raw candidate lists
VOLLEYBALL_WEB_CANDIDATES = [
    {
        "name": "Anna DeBeer",
        "dob": date(2001, 9, 25),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "anna.debeer", "X": "annadebeer14"},
        "dobSourceLabel": "University of Louisville Athletics — Anna DeBeer Roster & Bio (Born Sept. 25, 2001)",
        "dobSourceUrl": "https://gocards.com/sports/womens-volleyball/roster/anna-debeer/15178",
        "genderSourceLabel": "University of Louisville Women's Volleyball Official Roster",
        "genderSourceUrl": "https://gocards.com/sports/womens-volleyball/roster/anna-debeer/15178",
        "notes": "University of Louisville standout outside hitter, 3x AVCA All-American, national finalist. Pro Volleyball player (Indy Ignite). Official athletic bio records date of birth September 25, 2001 and parents Sara and Jeff DeBeer.",
        "followerInfo": {
            "Instagram": {
                "display": "54K",
                "numeric": 54000,
                "countType": "rounded",
                "sizeRange": "50K–99.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '54K followers, 1,615 following, 122 posts – @anna.debeer'."
            }
        }
    },
    {
        "name": "Anna Smrek",
        "dob": date(2003, 10, 11),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "annasmrek", "TikTok": "annasm_2"},
        "dobSourceLabel": "University of Wisconsin Badgers — Anna Smrek Bio & Wikipedia (Born October 11, 2003)",
        "dobSourceUrl": "https://en.wikipedia.org/wiki/Anna_Smrek",
        "genderSourceLabel": "Wisconsin Badgers Women's Volleyball Official Roster & Canada National Team",
        "genderSourceUrl": "https://uwbadgers.com/sports/womens-volleyball/roster/anna-smrek/13291",
        "notes": "Wisconsin Badgers NCAA National Champion & Tournament Most Outstanding Player (2021), Canada women's national volleyball team, Aras Kargo / Eczacıbaşı in Turkish Sultanlar Ligi. Birth date documented via official NCAA bio and English Wikipedia.",
        "followerInfo": {
            "Instagram": {
                "display": "83K",
                "numeric": 83000,
                "countType": "rounded",
                "sizeRange": "50K–99.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '83K followers, 2,135 following, 105 posts – @annasmrek'."
            }
        }
    },
    {
        "name": "Devyn Robinson",
        "dob": date(2002, 7, 9),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "devvrobinson", "TikTok": "devynnrobinson"},
        "dobSourceLabel": "Women Volleybox — Devyn Robinson profile (Birthdate 2002-07-09)",
        "dobSourceUrl": "https://women.volleybox.net/devyn-robinson-p30122",
        "genderSourceLabel": "Wisconsin Badgers Women's Volleyball Official Roster",
        "genderSourceUrl": "https://uwbadgers.com/sports/womens-volleyball/roster/devyn-robinson/13120",
        "notes": "Wisconsin Badgers NCAA National Champion middle blocker/opposite, Grand Rapids Rise (PVF) and SSC Palmberg Schwerin (German Bundesliga). Documentary DOB recorded in Volleybox database.",
        "followerInfo": {
            "Instagram": {
                "display": "27K",
                "numeric": 27000,
                "countType": "rounded",
                "sizeRange": "25K–49.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '27K Followers, 1,375 Following, 250 Posts - @devvrobinson'."
            }
        }
    },
    {
        "name": "Kendall Kipp",
        "dob": date(2000, 12, 12),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "kendallkipp", "X": "kippkendall"},
        "dobSourceLabel": "Women Volleybox — Kendall Kipp profile (Birthdate 2000-12-12)",
        "dobSourceUrl": "https://women.volleybox.net/kendall-kipp-p25194",
        "genderSourceLabel": "Stanford Women's Volleyball Roster & Volley Bergamo (Italian Serie A1)",
        "genderSourceUrl": "https://women.volleybox.net/kendall-kipp-p25194",
        "notes": "Stanford University standout opposite, 3x AVCA All-American, Pac-12 Player of the Year, Volley Bergamo (Italian Serie A1), Columbus Fury (PVF).",
        "followerInfo": {
            "Instagram": {
                "display": "26K",
                "numeric": 26000,
                "countType": "rounded",
                "sizeRange": "25K–49.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '26K seguidores, 1,339 siguiendo, 347 publicaciones - @kendallkipp'."
            }
        }
    },
    {
        "name": "Rachel Fairbanks",
        "dob": date(2003, 7, 5),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "rachel_fairbanks"},
        "dobSourceLabel": "Women Volleybox — Rachel Fairbanks profile (Birthdate 2003-07-05)",
        "dobSourceUrl": "https://women.volleybox.net/rachel-fairbanks-p73845",
        "genderSourceLabel": "Pittsburgh Panthers Women's Volleyball Official Roster",
        "genderSourceUrl": "https://pittsburghpanthers.com/sports/womens-volleyball/roster",
        "notes": "University of Pittsburgh setter, AVCA First-Team All-American, ACC Setter of the Year, LOVB Los Angeles professional.",
        "followerInfo": {}
    },
    {
        "name": "Zoe Fleck",
        "dob": date(2000, 9, 29),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "zfleckk"},
        "dobSourceLabel": "Women Volleybox — Zoe Jarvis (Fleck) profile (Birthdate 2000-09-29)",
        "dobSourceUrl": "https://women.volleybox.net/zoe-jarvis-p44990",
        "genderSourceLabel": "Texas Longhorns Women's Volleyball Official Roster & LOVB Austin",
        "genderSourceUrl": "https://women.volleybox.net/zoe-jarvis-p44990",
        "notes": "Texas Longhorns NCAA National Champion libero, 2x AVCA All-American, Big 12 Libero of the Year, LOVB Austin.",
        "followerInfo": {
            "Instagram": {
                "display": "14.3K",
                "numeric": 14300,
                "countType": "rounded",
                "sizeRange": "10K–24.9K",
                "sourceNote": "Public Instagram profile analytics snippet: '14.3K Followers - @zfleckk'."
            }
        }
    },
    {
        "name": "Kristen Nuss",
        "dob": date(1997, 12, 16),
        "categories": ["Athlete", "Beach Volleyball", "Creator"],
        "handles": {"Instagram": "kristen_nuss"},
        "dobSourceLabel": "BVB Info — Kristen Nuss Cruz Career & Vital Statistics (Birth Date December 16, 1997)",
        "dobSourceUrl": "http://www.bvbinfo.com/player.asp?ID=17607",
        "genderSourceLabel": "BVB Info / FIVB Women's Beach Volleyball Tour & USA Olympic Team",
        "genderSourceUrl": "http://www.bvbinfo.com/player.asp?ID=17607",
        "notes": "LSU Beach Volleyball all-time wins leader, USA Beach Volleyball Olympian (Paris 2024), multiple FIVB / BPT Elite16 gold medalist with partner Taryn Kloth.",
        "followerInfo": {
            "Instagram": {
                "display": "61K",
                "numeric": 61000,
                "countType": "rounded",
                "sizeRange": "50K–99.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '61K followers, 1,927 following, 894 posts – @kristen_nuss'."
            }
        }
    },
    {
        "name": "Betsi Flint",
        "dob": date(1992, 8, 13),
        "categories": ["Athlete", "Beach Volleyball", "Creator"],
        "handles": {"Instagram": "betsiflint"},
        "dobSourceLabel": "BVB Info — Betsi Metter Flint Vital Statistics (Birth Date August 13, 1992)",
        "dobSourceUrl": "http://www.bvbinfo.com/player.asp?ID=12974",
        "genderSourceLabel": "BVB Info & AVP Pro Beach Volleyball Tour (Women's Division)",
        "genderSourceUrl": "http://www.bvbinfo.com/player.asp?ID=12974",
        "notes": "Loyola Marymount University All-American, 7x AVP Champion, 5x International Beach Volleyball champion, official site betsiflint.com.",
        "followerInfo": {}
    },
    {
        "name": "Hailey Harward",
        "dob": date(1998, 3, 19),
        "categories": ["Athlete", "Beach Volleyball", "Creator"],
        "handles": {"Instagram": "haileyharward"},
        "dobSourceLabel": "Women Volleybox — Hailey Harward profile (Birthdate 1998-03-19)",
        "dobSourceUrl": "https://women.volleybox.net/hailey-harward-p30967/partners",
        "genderSourceLabel": "USA Beach Volleyball National Team & Long Beach State Athletics",
        "genderSourceUrl": "https://women.volleybox.net/hailey-harward-p30967/partners",
        "notes": "Long Beach State indoor/beach standout, USA Beach Volleyball National Team professional, AVP tour competitor.",
        "followerInfo": {
            "Instagram": {
                "display": "24K",
                "numeric": 24000,
                "countType": "rounded",
                "sizeRange": "10K–24.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '24K followers, 2,320 following, 608 posts – @haileyharward'."
            }
        }
    },
    {
        "name": "Taryn Kloth",
        "dob": date(1997, 4, 10),
        "categories": ["Athlete", "Beach Volleyball", "Creator"],
        "handles": {"Instagram": "tkloth10", "Facebook": "taryn.kloth"},
        "dobSourceLabel": "Women Volleybox — Taryn Brasher (Kloth) profile (Birthdate 1997-04-10)",
        "dobSourceUrl": "https://women.volleybox.net/taryn-kloth-p29408",
        "genderSourceLabel": "LSU Beach Volleyball / Creighton Athletics & USA Olympic Team",
        "genderSourceUrl": "https://women.volleybox.net/taryn-kloth-p29408",
        "notes": "Creighton and LSU Beach Volleyball All-American, USA Beach Volleyball Olympian (Paris 2024), FIVB Elite16 champion with Kristen Nuss.",
        "followerInfo": {
            "Instagram": {
                "display": "46K",
                "numeric": 46000,
                "countType": "rounded",
                "sizeRange": "25K–49.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '46K seguidores, 1,392 seguidos, 729 publicaciones - @tkloth10'."
            }
        }
    },
    {
        "name": "Eleonora Fersino",
        "dob": date(2000, 1, 24),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "eleonora_fersino"},
        "dobSourceLabel": "Women Volleybox — Eleonora Fersino profile (Birthdate January 24, 2000)",
        "dobSourceUrl": "https://women.volleybox.net/eleonora-fersino-p11848",
        "genderSourceLabel": "Italian Volleyball League (Lega Volley Femminile Serie A1) & Vero Volley Milano",
        "genderSourceUrl": "https://women.volleybox.net/eleonora-fersino-p11848",
        "notes": "Italian professional volleyball libero for Vero Volley Milano and Italian national team, former Imoco Volley Conegliano player.",
        "followerInfo": {
            "Instagram": {
                "display": "32K",
                "numeric": 32000,
                "countType": "rounded",
                "sizeRange": "25K–49.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '32K seguidores, 813 siguiendo, 303 publicaciones - @eleonora_fersino'."
            }
        }
    },
    {
        "name": "Federica Squarcini",
        "dob": date(2000, 9, 24),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "federicasquarcini4"},
        "dobSourceLabel": "Women Volleybox — Federica Squarcini profile (Birthdate 2000-09-24)",
        "dobSourceUrl": "https://women.volleybox.net/federica-squarcini-p11850",
        "genderSourceLabel": "Italian Serie A1 (Igor Gorgonzola Novara / Imoco Conegliano) & Italy National Team",
        "genderSourceUrl": "https://women.volleybox.net/federica-squarcini-p11850",
        "notes": "Italian professional volleyball middle blocker for Igor Gorgonzola Novara and Imoco Conegliano, Italian national team.",
        "followerInfo": {
            "Instagram": {
                "display": "84K",
                "numeric": 84000,
                "countType": "rounded",
                "sizeRange": "50K–99.9K",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '84K followers, 1,125 following, 737 posts – @federicasquarcini4'."
            }
        }
    },
    {
        "name": "Martina Armini",
        "dob": date(2002, 9, 19),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "martina_armini"},
        "dobSourceLabel": "Women Volleybox — Martina Armini profile (Birthdate 2002-09-19)",
        "dobSourceUrl": "https://women.volleybox.net/martina-armini-p19315",
        "genderSourceLabel": "Lega Volley Femminile (Italian Serie A1) & Chieri '76",
        "genderSourceUrl": "https://women.volleybox.net/martina-armini-p19315",
        "notes": "Italian volleyball libero playing for Reale Mutua Fenera Chieri '76 in Serie A1, World U20 Champion (2021) and Best Libero.",
        "followerInfo": {}
    },
    {
        "name": "Ayça Aykaç",
        "dob": date(1996, 2, 27),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "aycaaykac"},
        "dobSourceLabel": "Women Volleybox — Ayça Aykaç profile (Birthdate 1996-02-27)",
        "dobSourceUrl": "https://women.volleybox.net/ayca-aykac-p3678",
        "genderSourceLabel": "Turkish Sultanlar Ligi (VakıfBank) & Turkey Women's National Volleyball Team",
        "genderSourceUrl": "https://women.volleybox.net/ayca-aykac-p3678",
        "notes": "Turkish volleyball libero for VakıfBank Istanbul and Turkey women's national volleyball team, CEV Champions League and VNL champion.",
        "followerInfo": {}
    },
    {
        "name": "Zuzanna Górecka",
        "dob": date(2000, 4, 10),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "gurkowa"},
        "dobSourceLabel": "Women Volleybox — Zuzanna Górecka profile (Birthdate 2000-04-10)",
        "dobSourceUrl": "https://women.volleybox.net/zuzanna-gorecka-p10173",
        "genderSourceLabel": "Polish Tauron Liga (ŁKS Commercecon Łódź) & Poland Women's National Team",
        "genderSourceUrl": "https://women.volleybox.net/zuzanna-gorecka-p10173",
        "notes": "Polish volleyball outside hitter for ŁKS Commercecon Łódź and Poland national team, former Igor Gorgonzola Novara player in Italy.",
        "followerInfo": {}
    },
    {
        "name": "Aleksandra Gryka",
        "dob": date(2000, 2, 6),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "olagryka"},
        "dobSourceLabel": "Women Volleybox — Aleksandra Gryka profile (Birthdate 2000-02-06)",
        "dobSourceUrl": "https://women.volleybox.net/aleksandra-gryka-p11578",
        "genderSourceLabel": "USC Trojans Women's Volleyball & Poland National Team",
        "genderSourceUrl": "https://women.volleybox.net/aleksandra-gryka-p11578",
        "notes": "USC Trojans collegiate volleyball player and Polish national team middle blocker for ŁKS Commercecon Łódź.",
        "followerInfo": {}
    },
    {
        "name": "Weronika Centka",
        "dob": date(2000, 9, 6),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "weronikacentka"},
        "dobSourceLabel": "Women Volleybox — Weronika Centka profile (Birthdate 2000-09-06)",
        "dobSourceUrl": "https://women.volleybox.net/weronika-centka-p11574",
        "genderSourceLabel": "Polish Tauron Liga (DevelopRes Rzeszów) & Poland National Team",
        "genderSourceUrl": "https://women.volleybox.net/weronika-centka-p11574",
        "notes": "Polish volleyball middle blocker playing for DevelopRes Rzeszów and the Poland women's national volleyball team.",
        "followerInfo": {}
    },
    {
        "name": "Kisy Nascimento",
        "dob": date(2000, 1, 28),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "kisynascimento"},
        "dobSourceLabel": "Women Volleybox — Kisy Nascimento profile (Birthdate 2000-01-28)",
        "dobSourceUrl": "https://women.volleybox.net/kisy-nascimento-p15444",
        "genderSourceLabel": "Brazilian Superliga (Gerdau/Minas) & Brazil Women's National Team",
        "genderSourceUrl": "https://women.volleybox.net/kisy-nascimento-p15444",
        "notes": "Brazilian volleyball opposite for Gerdau/Minas and Brazil national team, South American Championship MVP and VNL medalist.",
        "followerInfo": {}
    },
    {
        "name": "Nyeme Costa",
        "dob": date(1998, 10, 11),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "nyemecosta"},
        "dobSourceLabel": "Women Volleybox — Nyeme Costa profile (Birthdate 1998-10-11)",
        "dobSourceUrl": "https://women.volleybox.net/nyeme-costa-p8772",
        "genderSourceLabel": "Brazilian Superliga (Gerdau/Minas) & Brazil Women's National Team",
        "genderSourceUrl": "https://women.volleybox.net/nyeme-costa-p8772",
        "notes": "Brazilian volleyball libero for Gerdau/Minas and Brazil women's national team, Olympic bronze medalist (Paris 2024).",
        "followerInfo": {}
    },
    {
        "name": "Lorenne Teixeira",
        "dob": date(1996, 1, 8),
        "categories": ["Athlete", "Volleyball", "Creator"],
        "handles": {"Instagram": "lorenneteixeira"},
        "dobSourceLabel": "Women Volleybox — Lorenne Teixeira profile (Birthdate 1996-01-08)",
        "dobSourceUrl": "https://women.volleybox.net/lorenne-teixeira-p5238",
        "genderSourceLabel": "Brazilian Superliga / V.League Japan & Brazil National Team",
        "genderSourceUrl": "https://women.volleybox.net/lorenne-teixeira-p5238",
        "notes": "Brazilian volleyball opposite for SESI Vôlei Bauru, Ageo Medics (Japan), Lokomotiv Kaliningrad, and Brazil national team.",
        "followerInfo": {}
    },
    {
        "name": "Julia Bergmann",
        "dob": date(2001, 2, 21),
        "categories": ["Athlete", "Volleyball", "College Athlete", "Creator"],
        "handles": {"Instagram": "juliabergmann6"},
        "dobSourceLabel": "Women Volleybox — Julia Bergmann profile (Birthdate 2001-02-21)",
        "dobSourceUrl": "https://women.volleybox.net/julia-bergmann-p14502",
        "genderSourceLabel": "Georgia Tech Athletics & Brazil Women's National Team",
        "genderSourceUrl": "https://women.volleybox.net/julia-bergmann-p14502",
        "notes": "Georgia Tech standout outside hitter, AVCA First-Team All-American, Brazil national team Olympic bronze medalist (Paris 2024), Türk Hava Yolları (Turkish Sultanlar Ligi).",
        "followerInfo": {}
    },
    {
        "name": "Yarishna Ayala",
        "dob": date(1991, 5, 9),
        "categories": ["Fitness", "Fitness Model", "Modeling", "Creator"],
        "handles": {"Instagram": "yarishna"},
        "dobSourceLabel": "Alpha Bodybuilders — Yarishna Ayala profile (Date of Birth May 9, 1991)",
        "dobSourceUrl": "https://alphabodybuilders.com/bodybuilders/yarishna-ayala/",
        "genderSourceLabel": "IFBB Pro League (Women's Wellness Division) & Official Profile",
        "genderSourceUrl": "https://alphabodybuilders.com/bodybuilders/yarishna-ayala/",
        "notes": "Puerto Rican 3x IFBB Pro Wellness Champion, fitness model, certified trainer and digital creator.",
        "followerInfo": {
            "Instagram": {
                "display": "3M",
                "numeric": 3000000,
                "countType": "rounded",
                "sizeRange": "1M–4.9M",
                "sourceNote": "Public Instagram profile snippet retrieved 2026-09-06: '3M Followers, 1,762 Following, 6,038 Posts - @Yarishna', SocialPruf analytics 3.45M followers."
            }
        }
    }
]

print(f"Loaded {len(VOLLEYBALL_WEB_CANDIDATES)} web discovery candidates.")
