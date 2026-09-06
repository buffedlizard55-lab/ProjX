#!/usr/bin/env python3
"""Session 12 batch K (2026-09-06): 4 verified adds (W-2026-173..176).
WWE women's champions wave 2: thesmackdownhotel (gender + DOB), wrestlingprofiles
JSON-LD (gender Female + birthDate), leaderbiography handles, live X structured
follower count for Iyo Sky. Bayley excluded (pre-existing W-2026-124..132 batch C).
Dup-guard pre-checked all four names.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

RANGES = [(50000,"25K–49.9K"),(100000,"50K–99.9K"),(250000,"100K–249.9K"),
          (500000,"250K–499.9K"),(1000000,"500K–999.9K"),(5000000,"1M–4.9M")]
def sr(n):
    if n is None: return "FOLLOWER_RANGE_UNKNOWN"
    if n < 50000: return "10K–24.9K"
    for l, lab in RANGES:
        if n < l: return lab
    return "5M+"

def acct(p, u, url, display, numeric, ctype, note):
    return {"platform": p, "username": u, "profileUrl": url,
            "followerCountDisplay": display, "followerCountNumeric": numeric,
            "countType": ctype, "checkedAt": CHECKED,
            "followerSizeRange": sr(numeric), "sourceNote": note}

def biggest(accts):
    known = [a for a in accts if a["followerCountNumeric"] is not None]
    if not known:
        return {"platform": None, "username": None, "display": None, "numeric": None,
                "sizeRange": "FOLLOWER_RANGE_UNKNOWN", "checkedAt": CHECKED}
    top = max(known, key=lambda a: a["followerCountNumeric"])
    return {"platform": top["platform"], "username": top["username"],
            "display": top["followerCountDisplay"], "numeric": top["followerCountNumeric"],
            "sizeRange": top["followerSizeRange"], "checkedAt": CHECKED}

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

def ent(i, n, a, g, s, flags, notes, accts):
    big = biggest(accts)
    return {"id": i, "displayName": n, "categories": ["Athlete", "Wrestling", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts, "largestPublicFollowing": big,
            "overallFollowerSizeRange": big["sizeRange"]}

NEW = []

NEW.append(ent("W-2026-173", "Alexa Bliss",
    ev("Born August 9, 1991 in Columbus, Ohio — age 35 in 2026 — per thesmackdownhotel ('was born in Columbus, Ohio on August 9, 1991'), officialwwe.fandom (Born August 9, 1991), dailywikibio (Date of Birth August 9, 1991) and leaderbiography (Date of Birth August 9, 1991).",
       "TheSmackDownHotel — Alexa Bliss profile (born August 9, 1991)", "https://www.thesmackdownhotel.com/wrestlers/alexa-bliss"),
    ev("Identified as a woman via thesmackdownhotel profile field ('Gender Female') and WWE women's championship career — multiple Raw/SmackDown women's titles, Grand Slam Champion (leaderbiography/officialwwe.fandom).",
       "TheSmackDownHotel — Alexa Bliss ('Gender Female' profile field; title history)", "https://www.thesmackdownhotel.com/wrestlers/alexa-bliss"),
    [src("TheSmackDownHotel — Alexa Bliss (DOB 1991-08-09; Gender Female; real name Alexis Cabrera née Kaufman)", "Website", "https://www.thesmackdownhotel.com/wrestlers/alexa-bliss", "age-evidence"),
     src("LeaderBiography — Alexa Bliss bio (DOB August 9, 1991; IG/X handles)", "Website", "https://leaderbiography.com/alexa-bliss/", "other-trusted"),
     src("DailyWikiBio — Alexa Bliss (DOB August 9, 1991; career history)", "Website", "https://dailywikibio.com/sports/alexa-bliss-biography/", "other-trusted"),
     src("Instagram — @alexa_bliss_wwe_ (leaderbiography socials table)", "Instagram", "https://www.instagram.com/alexa_bliss_wwe_/", "verified-platform"),
     src("X — @AlexaBliss_WWE (leaderbiography socials table)", "X", "https://x.com/AlexaBliss_WWE", "verified-platform")],
    [], "Multi-time WWE women's champion and first Grand Slam women's champion era ('Five Feet of Fury') — objective athlete category. Handles via leaderbiography socials table; counts not captured — UNKNOWN.",
    [acct("Instagram", "@alexa_bliss_wwe_", "https://www.instagram.com/alexa_bliss_wwe_/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown", "Handle via leaderbiography.com socials table; count not captured."),
     acct("X", "@AlexaBliss_WWE", "https://x.com/AlexaBliss_WWE", "FOLLOWER_COUNT_UNKNOWN", None, "unknown", "Handle via leaderbiography.com socials table; count not captured.")]))

NEW.append(ent("W-2026-174", "Asuka",
    ev("Born September 26, 1981 in Osaka, Japan — age 44 in 2026 — per thesmackdownhotel (born September 26, 1981), wrestlingprofiles JSON-LD birthDate 1981-09-26, IMDb (born September 26, 1981) and theefed replication.",
       "TheSmackDownHotel — Asuka profile (born September 26, 1981)", "https://www.thesmackdownhotel.com/wrestlers/asuka"),
    ev("Identified as a woman via thesmackdownhotel and wrestlingprofiles structured data ('Gender Female'; JSON-LD 'gender: Female') and WWE women's championship career — women's Triple Crown and Grand Slam Champion.",
       "WrestlingProfiles — Asuka ('gender: Female' JSON-LD; WWE women's titles)", "https://wrestlingprofiles.com/wrestler/asuka/"),
    [src("TheSmackDownHotel — Asuka (DOB 1981-09-26; Gender Female; real name Kanako Urai)", "Website", "https://www.thesmackdownhotel.com/wrestlers/asuka", "age-evidence"),
     src("WrestlingProfiles — Asuka (birthDate 1981-09-26; gender Female JSON-LD)", "Website", "https://wrestlingprofiles.com/wrestler/asuka/", "gender-evidence"),
     src("IMDb — Kanako Urai (born September 26, 1981)", "Website", "https://www.imdb.com/name/nm7542723/", "other-trusted")],
    [], "'The Empress of Tomorrow' — WWE women's Triple Crown + Grand Slam winner, Stardom legend — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-175", "Nia Jax",
    ev("Born May 29, 1984 in Sydney, Australia — age 42 in 2026 — per thesmackdownhotel (born May 29, 1984), wrestlingprofiles JSON-LD birthDate 1984-05-29, Wikipedia (born May 29, 1984) and prowrestling.fandom replication.",
       "TheSmackDownHotel — Nia Jax profile (born May 29, 1984)", "https://www.thesmackdownhotel.com/wrestlers/nia-jax"),
    ev("Identified as a woman via thesmackdownhotel and wrestlingprofiles structured data ('Gender Female'; JSON-LD 'gender: Female') plus WWE women's championship career — former Raw Women's Champion, 2x WWE Women's Champion 'two-time WWE Women's Champion' (Wikipedia).",
       "WrestlingProfiles — Nia Jax ('gender: Female' JSON-LD; women's title record)", "https://wrestlingprofiles.com/wrestler/nia-jax/"),
    [src("TheSmackDownHotel — Nia Jax (DOB 1984-05-29; Gender Female; real name Savelina Fanene)", "Website", "https://www.thesmackdownhotel.com/wrestlers/nia-jax", "age-evidence"),
     src("WrestlingProfiles — Nia Jax (birthDate 1984-05-29; gender Female JSON-LD)", "Website", "https://wrestlingprofiles.com/wrestler/nia-jax/", "gender-evidence"),
     src("Wikipedia — Nia Jax (DOB 1984-05-29; 2x WWE Women's Champion)", "Website", "https://en.wikipedia.org/wiki/Nia_Jax", "other-trusted"),
     src("Instagram — @linafanene (sportskeeda photo credit @linafanene/IG)", "Instagram", "https://www.instagram.com/linafanene/", "verified-platform")],
    [], "Two-time WWE Women's Champion and Queen of the Ring ('The Irresistible Force'); Dwayne Johnson's second cousin once removed — objective athlete category. IG handle via sportskeeda photo credit; count not captured — UNKNOWN.",
    [acct("Instagram", "@linafanene", "https://www.instagram.com/linafanene/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown", "Handle via sportskeeda photo credit @linafanene/IG; count not captured.")]))

NEW.append(ent("W-2026-176", "Iyo Sky",
    ev("Born May 8, 1990 in Kamakura, Kanagawa, Japan — age 36 in 2026 — per wrestlingprofiles JSON-LD birthDate 1990-05-08, sportskeeda (Date of Birth May 8, 1990), trendland (May 8, 1990) and mabumbe replication. Her official X account structured data shows 'Born May 8'.",
       "WrestlingProfiles — Iyo Sky (birthDate 1990-05-08)", "https://wrestlingprofiles.com/wrestler/iyo-sky/"),
    ev("Identified as a woman via wrestlingprofiles structured data ('gender: Female' JSON-LD) and WWE women's championship career — NXT Women's Champion, WWE Women's Championship win at SummerSlam 2023, 2026 Queen of the Ring (wrestlingprofiles career summary).",
       "WrestlingProfiles — Iyo Sky ('gender: Female' JSON-LD; career summary)", "https://wrestlingprofiles.com/wrestler/iyo-sky/"),
    [src("WrestlingProfiles — Iyo Sky (birthDate 1990-05-08; gender Female JSON-LD)", "Website", "https://wrestlingprofiles.com/wrestler/iyo-sky/", "age-evidence"),
     src("Sportskeeda — Iyo Sky player page (DOB May 8, 1990; Damage CTRL bio)", "Website", "https://www.sportskeeda.com/player/io-shirai", "other-trusted"),
     src("X — @Iyo_SkyWWE (official account, 'ONLY Official account'; born May 8; 460.2K followers)", "X", "https://x.com/Iyo_SkyWWE", "verified-platform"),
     src("Instagram — @iyo_sky (linked from her official X bio)", "Instagram", "https://www.instagram.com/iyo_sky/", "verified-platform")],
    [], "WWE Women's Champion and 2026 Queen of the Ring ('The Genius of the Sky'; real name Masami Ōdate) — objective athlete category. X account count is the platform's own structured figure (460,243 FollowAction count, displayed 460.2K) recorded live; IG handle cross-referenced from her official X bio — count UNKNOWN.",
    [acct("X", "@Iyo_SkyWWE", "https://x.com/Iyo_SkyWWE", "460.2K", 460243, "estimated", "Live X structured data on official account: 460,243 FollowAction count displayed as 460.2K on 2026-09-06 (x.com JSON-LD)."),
     acct("Instagram", "@iyo_sky", "https://www.instagram.com/iyo_sky/", "FOLLOWER_COUNT_UNKNOWN", None, "unknown", "Handle cross-referenced from her official X account bio link; count not captured.")]))


def build():
    data = json.loads(CATALOG.read_text())
    entries = data["entries"]
    ids = {e["id"] for e in entries}
    names = {e["displayName"].lower() for e in entries}
    urls = {s["url"] for e in entries for s in e["sources"]}
    for r in NEW:
        assert r["id"] not in ids, r["id"]
        assert r["displayName"].lower() not in names, r["displayName"]
        assert not ({s["url"] for s in r["sources"]} & urls), r["displayName"]
    entries.extend(NEW)
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)})")

if __name__ == "__main__":
    build()
