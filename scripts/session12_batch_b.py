#!/usr/bin/env python3
"""Session 12 batch B (2026-09-06): 14 verified adds (W-2026-115..128).
Wave 2 pipeline: WNBA (basketball-reference structured birthDate + IG handles,
UConn structured sameAs), WTA tennis (wtatennis.com + landoftennis JSON-LD
sameAs), track&field (Britannica/EBSCO/USATF official Gender: Female+DOB),
golf (LPGA-major sources), surfing (Britannica/WSL), gymnastics (official club
structured DOB + FIG), ice hockey (Wikipedia/PWHL official/eliteprospects).
Counts verbatim; unknown per protocol.
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

NEW.append(entry("W-2026-115", "Caitlin Clark",
    ["Athlete", "Basketball", "Creator"],
    ev("Born January 22, 2002 in Des Moines, Iowa — age 24 in 2026 — per Basketball-Reference WNBA page (structured birthDate 2002-01-22 + 'Born: January 22, 2002'), Biography.com and WNBA Wiki (Miraheze).",
       "Basketball-Reference — Caitlin Clark (born Jan 22, 2002)", "https://www.basketball-reference.com/wnba/players/c/clarkca02w.html"),
    ev("Identified as a woman via WNBA/Iowa women's basketball career — 'regarded as one of the greatest female collegiate players' (WNBA Wiki) and Biography.com 'Who Is Caitlin Clark' profile of the Indiana Fever guard.",
       "WNBA Wiki — Caitlin Clark (women's basketball)", "https://wnba.miraheze.org/wiki/Caitlin_Clark"),
    [
        src("Basketball-Reference — Caitlin Clark (DOB 2002-01-22; Instagram: caitlinclark22)", "Website", "https://www.basketball-reference.com/wnba/players/c/clarkca02w.html", "age-evidence"),
        src("Biography.com — Caitlin Clark (born January 22, 2002, Des Moines)", "Website", "https://www.biography.com/athletes/a64150678/caitlin-clark", "other-trusted"),
        src("BiographyHive — Caitlin Clark bio (Instagram: @caitlinclark22)", "Website", "https://www.biographyhive.com/biography/sportsperson/caitlin-clark-biography-age-height-parents-siblings-ethnicity-boyfriend-net-worth-awards-instagram/", "other-trusted"),
        src("Instagram — @caitlinclark22 (basketball-reference header)", "Instagram", "https://www.instagram.com/caitlinclark22/", "verified-platform"),
    ],
    [], "2024 WNBA Rookie of the Year and NCAA Division I all-time scoring leader (3,951 points) — objective athlete category. Handle verbatim via basketball-reference header; count not captured — UNKNOWN.",
    [ig("@caitlinclark22", "Handle via basketball-reference player page header ('Instagram: caitlinclark22') and BiographyHive bio; count not captured.")]))

NEW.append(entry("W-2026-116", "Coco Gauff",
    ["Athlete", "Tennis", "Creator"],
    ev("Born March 13, 2004 in Delray Beach, Florida — age 22 in 2026 — per Biography.com ('BORN: March 13, 2004'), WTA official profile (JSON-LD birthDate 2004-03-13), LandOfTennis structured data and TennisWorldUSA.",
       "WTA — Coco Gauff official profile (birthDate 2004-03-13)", "https://www.wtatennis.com/players/328560/coco-gauff"),
    ev("Identified as a woman via WTA women's professional tennis career — 2023 US Open and 2025 Roland-Garros women's singles champion (WTA/Biography.com).",
       "Biography.com — Coco Gauff (US Open champion biography)", "https://www.biography.com/athlete/coco-gauff"),
    [
        src("WTA — Coco Gauff official player profile (DOB 2004-03-13)", "Website", "https://www.wtatennis.com/players/328560/coco-gauff", "official"),
        src("Biography.com — Coco Gauff (born March 13, 2004, Delray Beach)", "Website", "https://www.biography.com/athlete/coco-gauff", "age-evidence"),
        src("LandOfTennis — Coco Gauff structured record (sameAs IG @cocogauff, X @CocoGauff)", "Website", "https://www.landoftennis.com/players_women/coco_gauff.htm", "other-trusted"),
        src("Instagram — @cocogauff (landoftennis sameAs)", "Instagram", "https://www.instagram.com/cocogauff/", "verified-platform"),
        src("X — @CocoGauff (landoftennis sameAs)", "X", "https://x.com/CocoGauff", "verified-platform"),
    ],
    [], "2023 US Open and 2025 French Open singles champion — objective athlete category. Handles via LandOfTennis structured sameAs; counts not captured — UNKNOWN.",
    [ig("@cocogauff", "Handle via landoftennis.com structured sameAs; count not captured."),
     xacc("@CocoGauff", "Handle via landoftennis.com structured sameAs; count not captured.")]))

NEW.append(entry("W-2026-117", "Aryna Sabalenka",
    ["Athlete", "Tennis", "Creator"],
    ev("Born May 5, 1998 in Minsk, Belarus — age 28 in 2026 — per TennisWorldUSA structured birthDate 1998-05-05, IMDb bio, TennisArchive Fandom (born May 5, 1998) and CelebsFacts (Date Of Birth: 5 May 1998).",
       "TennisWorldUSA — Aryna Sabalenka (born May 5, 1998, Minsk)", "https://www.tennisworldusa.org/tennis-player/368/aryna-sabalenka/"),
    ev("Identified as a woman via WTA women's tour career — world No. 1 in singles, 2023 Australian Open women's singles champion (TennisWorldUSA/IMDb mini-bio).",
       "IMDb — Aryna Sabalenka biography (WTA No. 1 profile)", "https://www.imdb.com/name/nm9355312/bio/"),
    [
        src("TennisWorldUSA — Aryna Sabalenka (DOB 1998-05-05 structured)", "Website", "https://www.tennisworldusa.org/tennis-player/368/aryna-sabalenka/", "age-evidence"),
        src("IMDb — Aryna Sabalenka biography (born May 5, 1998)", "Website", "https://www.imdb.com/name/nm9355312/bio/", "other-trusted"),
        src("CelebsFacts — Aryna Sabalenka (Date Of Birth 5 May 1998; official site arynasabalenka.com)", "Website", "https://www.celebsfacts.com/aryna-sabalenka/", "other-trusted"),
    ],
    [], "World No. 1 and multi-time Grand Slam singles champion — objective athlete category. No handle value captured this pass (bio sites reference her Twitter/Instagram without verbatim handles) — follower range UNKNOWN, per-honesty protocol.",
    []))

NEW.append(entry("W-2026-118", "Sha'Carri Richardson",
    ["Athlete", "Track and Field", "Creator"],
    ev("Born March 25, 2000 in Dallas, Texas — age 26 in 2026 — per Britannica (born March 25, 2000), Biography.com, biographyhost (DOB Mar 25 2000), biographykind and dreshare.",
       "Britannica — Sha'Carri Richardson (born March 25, 2000)", "https://www.britannica.com/biography/Sha-Carri-Richardson"),
    ev("Identified as a woman via Britannica ('one of the world's fastest female sprinters') and women's 100m/Olympic women's 4x100m career (2024 Olympic gold in women's 4x100m relay).",
       "Britannica — Sha'Carri Richardson ('fastest female sprinters')", "https://www.britannica.com/biography/Sha-Carri-Richardson"),
    [
        src("Britannica — Sha'Carri Richardson (DOB 2000-03-25; 2024 Olympic medals)", "Website", "https://www.britannica.com/biography/Sha-Carri-Richardson", "age-evidence"),
        src("Biography.com — Sha'Carri Richardson (BORN: March 25, 2000, Dallas)", "Website", "https://www.biography.com/athletes/a60383465/shacarri-richardson", "other-trusted"),
        src("BiographyKind — Sha'Carri Richardson (DOB 2000-03-25; Instagram ID @itsshacarri)", "Website", "https://en.biographykind.com/shacarri-richardson/", "other-trusted"),
        src("Instagram — @itsshacarri (biographykind Wiki/Bio table)", "Instagram", "https://www.instagram.com/itsshacarri/", "verified-platform"),
    ],
    ["CONFLICTING_INFORMATION"],
    "2023 world 100m champion and 2024 Olympic 4x100m gold medalist — objective athlete category. Older handle variance: dreshare (2022) listed instagram.com/carririchardson_ while current bios list @itsshacarri — recorded current handle; variance in IRR-2026-09-06-012.",
    [ig("@itsshacarri", "Handle via biographykind Wiki/Bio table ('Instagram ID @itsshacarri'); count not captured.")]))

NEW.append(entry("W-2026-119", "Sydney McLaughlin-Levrone",
    ["Athlete", "Track and Field", "Creator"],
    ev("Born August 7, 1999 in New Brunswick, New Jersey — age 27 in 2026 — per USA Track & Field official athlete bio (Date of Birth: 8/7/1999, Age: 27), EBSCO Research Starter and Tuko (date of birth 7th August 1999).",
       "USA Track & Field — Sydney McLaughlin-Levrone official bio (DOB 8/7/1999)", "https://www.usatf.org/athlete-bios/sydney-mclaughlin-levrone"),
    ev("Identified as a woman via USATF official athlete bio ('Gender: Female') and Tuko profile ('Gender: Female'); women's 400m hurdles world-record career.",
       "USA Track & Field — athlete bio states Gender: Female", "https://www.usatf.org/athlete-bios/sydney-mclaughlin-levrone"),
    [
        src("USA Track & Field — Sydney McLaughlin-Levrone bio (DOB 8/7/1999; Gender: Female)", "Website", "https://www.usatf.org/athlete-bios/sydney-mclaughlin-levrone", "official"),
        src("EBSCO Research Starter — Sydney McLaughlin biography (born August 7, 1999)", "Website", "https://www.ebsco.com/research-starters/biography/sydney-mclaughlin/", "age-evidence"),
        src("Tuko — Sydney McLaughlin profile (Gender: Female; DOB 7th August 1999)", "Website", "https://www.tuko.co.ke/facts-lifehacks/celebrity-biographies/435484-sydney-mclaughlins-family-parents-siblings-husband/", "other-trusted"),
    ],
    [], "Two-time Olympic 400m hurdles champion and world-record holder — objective athlete category. USATF page links her X/Instagram icons without verbatim handles; handles not captured — UNKNOWN.",
    []))

NEW.append(entry("W-2026-120", "Carissa Moore",
    ["Athlete", "Surfing", "Creator"],
    ev("Born August 27, 1992 in Honolulu, Hawaii — age 34 in 2026 — per Britannica (born August 27, 1992), Wikipedia/Wikiwand, Red Bull career portrait and Outrigger profile.",
       "Britannica — Carissa Moore (born August 27, 1992)", "https://www.britannica.com/biography/Carissa-Moore"),
    ev("Identified as a woman via Britannica ('one of the greatest female surfers of all time') and women's shortboard career — first Olympic gold medal in women's surfing (Tokyo 2020).",
       "Britannica — Carissa Moore (women's surfing achievements)", "https://www.britannica.com/biography/Carissa-Moore"),
    [
        src("Britannica — Carissa Moore (DOB 1992-08-27; five-time world champion)", "Website", "https://www.britannica.com/biography/Carissa-Moore", "age-evidence"),
        src("Wikipedia — Carissa Moore (DOB 1992-08-27; 2020 Olympic shortboard gold)", "Website", "https://en.wikipedia.org/wiki/Carissa_Moore", "other-trusted"),
        src("Red Bull — Carissa Moore career portrait (women's surfing champion)", "Website", "https://www.redbull.com/us-en/carissa-moore-career-portrait", "other-trusted"),
    ],
    [], "Five-time WSL world champion and first women's surfing Olympic gold medalist — objective athlete category; W-2026-019 Rebecca Silva is a separate unrelated creator (distinct sport/region). No handle captured — UNKNOWN.",
    []))

NEW.append(entry("W-2026-121", "A'ja Wilson",
    ["Athlete", "Basketball", "Creator"],
    ev("Born August 8, 1996 in Columbia, South Carolina — age 30 in 2026 — per Basketball-Reference (structured birthDate 1996-08-08), Olympics.com athlete profile (Year of Birth 1996), baike and JagranJosh.",
       "Basketball-Reference — A'ja Wilson (born Aug 8, 1996)", "https://www.basketball-reference.com/wnba/players/w/wilsoa01w.html"),
    ev("Identified as a woman via WNBA women's career — four-time WNBA MVP, two-time Olympic gold medalist (basketball-reference/Olympics.com; BecauseOfThemWeCan 'Trailblazers' profile).",
       "Olympics.com — A'ja Wilson athlete biography (women's basketball)", "https://www.olympics.com/en/athletes/a-ja-wilson"),
    [
        src("Basketball-Reference — A'ja Wilson (DOB 1996-08-08; Instagram: aja22wilson)", "Website", "https://www.basketball-reference.com/wnba/players/w/wilsoa01w.html", "age-evidence"),
        src("Olympics.com — A'ja Wilson (Year of Birth 1996; 2 Olympic gold medals)", "Website", "https://www.olympics.com/en/athletes/a-ja-wilson", "official"),
        src("JagranJosh — A'ja Wilson biography (born August 8, 1996; 4x MVP)", "Website", "https://www.jagranjosh.com/us/sports/aja-wilson-biography-1860001257", "other-trusted"),
        src("Instagram — @aja22wilson (basketball-reference header)", "Instagram", "https://www.instagram.com/aja22wilson/", "verified-platform"),
    ],
    [], "Four-time WNBA MVP and three-time WNBA champion center — objective athlete category. Handle via basketball-reference header; count not captured — UNKNOWN.",
    [ig("@aja22wilson", "Handle via basketball-reference player page header ('Instagram: aja22wilson'); count not captured.")]))

NEW.append(entry("W-2026-122", "Hilary Knight",
    ["Athlete", "Ice Hockey", "Creator"],
    ev("Born July 12, 1989 — age 37 in 2026 — per Wikipedia (born July 12, 1989), PWHL official athlete page (Birthdate: 1989-07-12, Age 36→37) and eliteprospects structured record (Date of Birth Jul 12, 1989). Birthplace listed as Palo Alto (Wikipedia) or Sun Valley, Idaho (PWHL/eliteprospects) — variance logged.",
       "PWHL — Hilary Knight official athlete page (birthdate 1989-07-12)", "https://www.thepwhl.com/en/olympics/athlete/hilary-knight"),
    ev("Identified as a woman via captaincy of the United States women's national ice hockey team and PWHL women's league career (Wikipedia/PWHL); 'one of the greatest players in women's hockey history'.",
       "Wikipedia — Hilary Knight (US women's national team captain)", "https://en.wikipedia.org/wiki/Hilary_Knight"),
    [
        src("Wikipedia — Hilary Knight (DOB 1989-07-12; PWHL captain)", "Website", "https://en.wikipedia.org/wiki/Hilary_Knight", "age-evidence"),
        src("PWHL — Hilary Knight official athlete page (birthdate 1989-07-12)", "Website", "https://www.thepwhl.com/en/olympics/athlete/hilary-knight", "official"),
        src("EliteProspects — Hilary Knight (DOB Jul 12, 1989; PWHL record)", "Website", "https://www.eliteprospects.com/player/367043/hilary-knight", "other-trusted"),
        src("NBC Olympics — Hilary Knight athlete profile ('194,000 followers on Instagram')", "Website", "https://www.nbcolympics.com/news/hilary-knight-meet-athlete", "other-trusted"),
    ],
    ["CONFLICTING_INFORMATION"],
    "Five-time Olympic medalist (gold 2018, 2026) and record 10-time world champion — objective athlete category. NBC Olympics (Nov 2025 snapshot) states 194,000 Instagram followers; handle value not captured this pass, so count is recorded in notes rather than an unverified account object. Birthplace variance (Palo Alto vs Sun Valley) and Seattle/Detroit team-snapshot mismatch logged in IRR-2026-09-06-012.",
    []))

NEW.append(entry("W-2026-123", "Kendall Coyne Schofield",
    ["Athlete", "Ice Hockey", "Creator"],
    ev("Born May 25, 1992 in Palos Heights, Illinois — age 34 in 2026 — per Wikipedia (born May 25, 1992, age 33→34), PWHL official athlete page (Birthdate: 1992-05-25, Age 33) and IceHockey Fandom infobox.",
       "PWHL — Kendall Coyne Schofield official athlete page (birthdate 1992-05-25)", "https://www.thepwhl.com/en/olympics/athlete/kendall-coyne-schofield"),
    ev("Identified as a woman via Minnesota Frost and US women's national team captaincy — PWHL Walter Cup championships 2024/2025 and 2018 Olympic gold (PWHL/Wikipedia; 'top female college hockey player' — Patty Kazmaier Award 2016).",
       "Wikipedia — Kendall Coyne Schofield (women's hockey career)", "https://en.wikipedia.org/wiki/Kendall_Coyne_Schofield"),
    [
        src("Wikipedia — Kendall Coyne Schofield (DOB 1992-05-25; Frost captain)", "Website", "https://en.wikipedia.org/wiki/Kendall_Coyne_Schofield", "age-evidence"),
        src("PWHL — Kendall Coyne Schofield official athlete page (birthdate 1992-05-25)", "Website", "https://www.thepwhl.com/en/olympics/athlete/kendall-coyne-schofield", "official"),
        src("kendallcoyne.com — official athlete site (Olympic gold/silver medalist bio)", "Website", "https://kendallcoyne.com/about/", "official"),
    ],
    [], "2018 Olympic gold medalist, three-time Olympian and two-time PWHL Walter Cup champion captain — objective athlete category. No social handle captured this pass — follower range UNKNOWN.",
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
    if "IRR-2026-09-06-012" not in irr_ids:
        data["irregularities"].append({
            "id": "IRR-2026-09-06-012",
            "severity": "needs-review",
            "summary": "Session-12 batch-B flags: press-documented IG handle/count conflicts + place/team snapshot variances; five WNBA/golf/tennis stars found pre-existing in catalog during batch assembly (dup-guard caught).",
            "detail": (
                "(1) Angel Reese, Jordan Chiles, Jade Carey, Nelly Korda and Paige Bueckers were re-verified this wave but then excluded as duplicates — they already exist in the catalog from earlier sessions (the id/name dup check caught them). Reese IG handle variance (@angelreese5 vs @angelreese10 per basketball-reference) noted for a future review of the existing entry. "
                "(2) Sha'Carri Richardson older handle instagram.com/carririchardson_ (dreshare, 2022) vs current @itsshacarri (biographykind) — recorded current. "
                "(3) Hilary Knight: birthplace Palo Alto, CA (Wikipedia) vs Sun Valley, ID (PWHL/eliteprospects); Wikipedia team's snapshot also showed 'PWHL Detroit' while PWHL official page says Seattle Torrent — team-snapshot lag. NBC Olympics states 194,000 IG followers (Nov 2025) — kept in entry notes because handle value wasn't captured. "
                "(4) (Paige Bueckers IG '2 million+' July-2025 claim — entry excluded as pre-existing; noted for its existing record.)"
            ),
            "reviewStatus": "requires-owner-review",
        })
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)}) irr={len(data['irregularities'])}")

if __name__ == "__main__":
    build()
