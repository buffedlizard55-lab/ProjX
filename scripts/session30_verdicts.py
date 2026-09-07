#!/usr/bin/env python3
"""Session 30 — verdict table for the Japanese-Wikipedia slice of the Wikidata model pool
(female, occupation model / fashion model / personal trainer / bodybuilder / fitness model,
born 1985-2008, Instagram or TikTok handle, ja-wiki article, NO en-wiki article; page 1,
ORDER BY ?p LIMIT 150 OFFSET 0 -> 148 unique people -> 135 new after Q-ID/name/handle dedup).

Input : data/research/s30_raw/model_ja_checked.json  (rows + ja-wiki lead extracts + labels)
Output: data/research/verification_s30_log.tsv       (qid|name|dob|verdict|category-or-flags|evidence|url)
        data/research/s30_verify_buckets.json        (handles for scripts/session30_apply.py)

Verdict rules (Session 27/28/29 precedent, applied to ja-wiki leads):
  PROMOTE  lead states the full birth date (YYYY年M月D日) matching Wikidata AND documents modeling /
           gravure (swimsuit magazine) modeling / race-queen / influencer / creator activity; adult.
  REVIEW   scope-ambiguous (idol / singer / actress / announcer / entrepreneur only), AGE_PARTIAL
           (no full birth date on the page), DOB_CONFLICT (page date differs from Wikidata).
  REJECT   deceased or not an individual person.
Nothing is invented: names come from the Wikidata labels / ja-wiki lead romanisations, handles from
Wikidata P2003 / P7085, dates from the ja-wiki lead cross-checked against Wikidata P569.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = json.load(open(ROOT / 'data/research/s30_raw/model_ja_checked.json'))
by = {r['qid']: r for r in rows}

V = {}


def P(q, cat, note, name=None, dob=None, ig=None, ig2=None, tt=None):
    V[q] = ('PROMOTE', cat, note, name, dob, ig, ig2, tt)


def R(q, flags, note, name=None, ig=None, ig2=None, tt=None):
    V[q] = ('REVIEW', flags, note, name, None, ig, ig2, tt)


def X(q, note, name=None):
    V[q] = ('REJECT', 'excluded', note, name, None, None, None, None)


SA = 'no modeling / creator activity documented in the lead; adult (DOB matches Wikidata)'
GR = 'gravure idol = swimsuit / magazine model (objective Japanese occupational category)'

# ---- batch 0 (jawiki_b0.json)
P('Q100453581', 'Modeling/TV', 'JP former actress, fashion model, tarento and TV reporter; DOB matches Wikidata')
P('Q100453681', 'Modeling/acting', 'JP fashion model, tarento and actor; DOB matches Wikidata; age 20')
P('Q100454882', 'Beauty pageant/modeling', 'JP model and tarento, Japan representative at Miss Supranational 2018; DOB matches Wikidata')
R('Q101103820', 'scope-ambiguous', 'JP singer, idol and actress (Angerme 9th-generation member); ' + SA)
P('Q101199776', 'Modeling', 'JP fashion model (Fukuoka); DOB matches Wikidata; age 21')
P('Q101200026', 'Gravure modeling/swimwear', 'JP gravure idol (Osaka); ' + GR + '; DOB matches Wikidata')
P('Q101200609', 'Gravure modeling/TV', 'JP tarento and gravure idol; ' + GR + '; DOB matches Wikidata')
P('Q102246874', 'Modeling', 'JP fashion model (SANKI Worldwide); age 18 (reached 18 on 2026-01-28, before the check date); DOB matches Wikidata')
R('Q102248153', 'AGE_PARTIAL', 'JP actress and model (Osaka); the ja-wiki lead carries no birth date; Wikidata 1997-07-04 unconfirmed on page')
P('Q102279408', 'Modeling/race queen/music', 'JP tarento, singer and race queen (promotional model; Platinum Production); the Wikidata TikTok statement holds a purely numeric string rather than a username and is not recorded; DOB matches Wikidata', tt='')
R('Q10322210', 'scope-ambiguous', 'BR actress (Livian Taranto Aragao); ' + SA)
P('Q104012733', 'Modeling/Creator', 'JP model, tarento and Instagrammer (Machida, Tokyo); DOB matches Wikidata')
P('Q104012831', 'Modeling/TV', 'JP model and local tarento based in Miyagi Prefecture (Sendai) - regional creator; DOB matches Wikidata')
P('Q104013206', 'Gravure modeling/Creator', 'JP gravure idol, tarento, YouTuber and poker player; ' + GR + '; DOB matches Wikidata')
P('Q104013269', 'Modeling/gravure/swimwear', 'JP fashion model and gravure idol (Sado, Niigata); DOB matches Wikidata')
P('Q104013339', 'Gravure modeling/TV', 'JP gravure idol and tarento (Saitama); ' + GR + '; DOB matches Wikidata', name='Kairi (海里)')
P('Q104013520', 'Modeling/acting', 'JP former fashion model and former actress (Tokyo); DOB matches Wikidata')
P('Q104538599', 'Modeling/race queen', 'JP model and race queen (Ota, Gunma); DOB matches Wikidata')
P('Q104538601', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata; age 19')
R('Q104538695', 'scope-ambiguous', 'JP actress, former Tokimeki Sendenbu member; ' + SA)
# ---- batch 1 (jawiki_b1.json)
P('Q1050727', 'Modeling', 'JP model, former SKE48 Team KII member; DOB matches Wikidata; article title 木下ミシェル (Michelle Kinoshita) while the Wikidata English label keeps the former stage name Yukiko Kinoshita (name alias noted); Wikidata documents two Instagram handles for her (michelle.kinoshita_official and yukiko_____k) - both recorded, current-use status unverified', name='Michelle Kinoshita', ig='michelle.kinoshita_official', ig2='yukiko_____k')
R('Q1050749', 'scope-ambiguous', 'JP entrepreneur, former SKE48 / AKB48 member and tarento; ' + SA)
P('Q105258523', 'Modeling/acting', 'JP fashion model and actress (Hollywood Latte); age 18 (reached 18 on 2026-01-02, before the check date); DOB matches Wikidata', name='Nao Oosato')
P('Q105258667', 'Modeling/music', 'JP fashion model and member of the dance-and-vocal unit MAGICOUR (Kyoto); DOB matches Wikidata')
P('Q105258863', 'Modeling/acting/Creator', 'JP actress, model and influencer, former member of the YouTube channel MelTV (Okinawa); DOB matches Wikidata')
P('Q105258956', 'Modeling', 'JP model (Saga); DOB matches Wikidata')
P('Q105258962', 'Modeling/acting', 'JP fashion model and actress (Kobe); DOB matches Wikidata')
P('Q105258967', 'Modeling', 'JP fashion model (Saitama); DOB matches Wikidata; age 21')
P('Q105258976', 'Modeling/gravure/swimwear/race queen', 'JP fashion model, gravure idol, tarento and race queen, Miss FLASH 2021 grand prix; DOB matches Wikidata')
P('Q105259069', 'Modeling/TV', 'JP tarento and model (Sapporo); DOB matches Wikidata', name='Yuna Naeka')
P('Q105259088', 'Gravure modeling/swimwear/TV', 'JP gravure idol and tarento (Tochigi); ' + GR + '; DOB matches Wikidata', name='Yui Tadenuma')
P('Q105704031', 'Modeling/acting', 'JP actress and fashion model (Sano, Tochigi); DOB matches Wikidata')
P('Q105704046', 'Modeling/race queen', 'JP former race queen and former model (Sky High Promotions; Osaka); DOB matches Wikidata')
P('Q105704105', 'Modeling', 'JP model (Chiba); DOB matches Wikidata')
P('Q105704180', 'Modeling/acting/TV', 'JP actress, model and tarento (Tokyo); DOB matches Wikidata')
P('Q105704206', 'Modeling/acting/business', 'JP entrepreneur, actress, fashion model and tarento (Aoyama Gakuin University law graduate); DOB matches Wikidata')
P('Q105711434', 'Modeling/art', 'JP artist (painter) and model, born in Bordeaux, France; DOB matches Wikidata; Wikidata documents two Instagram handles for her (chan_kotao and tkotao, both with Instagram numeric IDs) - both recorded, current-use status unverified', ig='chan_kotao', ig2='tkotao')
P('Q1057829', 'Modeling/gravure/acting', 'VN model, gravure idol and actress (Elly Tran Ha per lead); DOB matches Wikidata', name='Elly Trần')
P('Q106478565', 'Modeling/entertainment', 'JP tarento, actress, singer and model, member of AND CaaaLL; DOB matches Wikidata; age 21')
P('Q106480268', 'Modeling/music/acting', 'JP singer, actress and model, member of myojou; DOB matches Wikidata; age 21')
# ---- batch 2 (jawiki_b2.json)
R('Q106923586', 'scope-ambiguous', 'JP singer and idol, NiziU member RIO; ' + SA)
R('Q106925309', 'scope-ambiguous', 'JP singer and idol, NiziU member MAYA; ' + SA)
R('Q106940477', 'scope-ambiguous', 'JP singer and idol, NiziU member MAYUKA; ' + SA)
R('Q106958914', 'DOB_CONFLICT', 'PR model and pageant titleholder (Miss Grand Puerto Rico 2020); ja-wiki lead DOB 1988-09-09 vs Wikidata 1999-09-09 - year-level conflict, no value chosen (both adult)')
P('Q106960696', 'Modeling/TV', 'JP model and tarento (Yame, Fukuoka); DOB matches Wikidata')
R('Q106994179', 'scope-ambiguous', 'JP model, adult-video (AV) actress and gravure idol per the ja-wiki lead; adult-film performers are outside the focus categories (pornographic-film actors were excluded at query time; this item lacks the Wikidata occupation tag) - held for manual scope decision, consistent with the Session 28 handling of Annie Knight; adult (DOB matches Wikidata)', name='MINAMO')
P('Q106994755', 'Gravure modeling/Creator', 'JP gravure idol, model, tarento and YouTuber (Hyogo); DOB matches Wikidata')
P('Q108109756', 'Modeling', 'JP fashion model (Avex Management); DOB matches Wikidata', name='Rino Natsume')
P('Q108109824', 'Modeling/acting', 'JP fashion model and actress (Tokyo); DOB matches Wikidata; age 20')
P('Q108109989', 'Modeling/acting', 'JP actress, model and voice actress; DOB matches Wikidata')
R('Q108110163', 'scope-ambiguous', 'JP singer, idol and actress (Tsubaki Factory member); ' + SA)
P('Q108257307', 'Gravure modeling/swimwear/music', 'JP idol and gravure idol, member of NANIMONO; ' + GR + '; DOB matches Wikidata')
P('Q10855007', 'Modeling/entertainment', 'JP idol, actress and fashion model (Tokyo); DOB matches Wikidata')
P('Q108776600', 'Modeling', 'JP fashion model (Hyogo); DOB matches Wikidata; age 21')
P('Q108776663', 'Modeling', 'JP fashion model (AIMS Production); DOB matches Wikidata')
P('Q108776890', 'Modeling/sports/TV', 'JP tarento, fashion model and athlete (Hiroshima); DOB matches Wikidata', name='Mirano Honjo')
P('Q108777179', 'Modeling/acting', 'JP model and actress (Tokyo); DOB matches Wikidata', name='Saaya Mima')
P('Q108777212', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata; age 19')
P('Q10896641', 'Modeling/music', 'JP fashion model and pop singer (FIRST AGENT); DOB matches Wikidata')
P('Q109287897', 'Gravure modeling/acting', 'JP gravure model, actor, tarento and former idol (Ichigo Hime, FUSION); DOB matches Wikidata', name='Yasuyo Saito')
# ---- batch 3 (jawiki_b3.json)
P('Q109287966', 'Modeling/public speaking', 'JP public speaker and model; DOB matches Wikidata')
P('Q109288329', 'Gravure modeling/swimwear', 'JP former gravure idol (formerly Platinum Production); ' + GR + '; DOB matches Wikidata')
P('Q109316383', 'Modeling', 'Japan-based model of Central Asian origin (Diana Kadirkulova Tagirovna); DOB matches Wikidata; country of citizenship not recorded in Wikidata', name='Diana Kadirkulova Tagirovna')
P('Q109591238', 'Modeling/music', 'JP artist, fashion model and singer, vocalist of Wednesday Campanella; DOB matches Wikidata', name='Utaha (詩羽)')
P('Q109594862', 'Modeling', 'JP fashion model (Osaka); age 18 (reached 18 on 2026-07-01, before the check date); DOB matches Wikidata')
P('Q109594909', 'Modeling', 'JP fashion model, former member of the girls unit HUNNY BEE; DOB matches Wikidata; age 19')
R('Q109596290', 'scope-ambiguous', 'JP adult-video (AV) actress, 17LIVE streamer and model per the ja-wiki lead; adult-film performers are outside the focus categories (pornographic-film actors were excluded at query time; this item lacks the Wikidata occupation tag) - held for manual scope decision, consistent with the Session 28 handling of Annie Knight; adult (DOB matches Wikidata)')
P('Q109926306', 'Modeling/TV', 'TW model and tarento (林襄, Lin Xiang per lead; Wikidata English label Mizuki Lin - name alias noted); DOB matches Wikidata', name='Mizuki Lin (林襄)')
P('Q110249348', 'Modeling/TV', 'JP fashion model and tarento (Nerima, Tokyo); DOB matches Wikidata', name='Nanami (菜波)')
P('Q110403042', 'Modeling/Creator', 'JP fashion model, YouTuber, TikToker and influencer (Miyazaki); DOB matches Wikidata; age 21', name='Sakura (さくら, model)')
P('Q110403094', 'Modeling/Creator/business', 'JP entrepreneur; former DJ, fashion model, tarento, artist, lyricist, fashion/beauty PR director, content creator and writer; DOB matches Wikidata')
P('Q110403370', 'Gravure modeling/acting', 'JP gravure idol, fashion model and actress (Isesaki, Gunma); DOB matches Wikidata')
R('Q110403455', 'scope-ambiguous', 'JP singer and idol (Angerme 10th-generation member); ' + SA + '; age 20')
P('Q110403603', 'Modeling/acting', 'JP fashion model and actress (Ehime); DOB matches Wikidata')
P('Q110403675', 'Modeling/acting', 'JP model and actress (Tokyo); DOB matches Wikidata')
P('Q110403801', 'Gravure modeling/Creator', 'JP gravure idol and YouTuber (Okayama); ' + GR + '; DOB matches Wikidata')
P('Q110403834', 'Modeling', 'JP model (Neyagawa, Osaka); DOB matches Wikidata')
P('Q111110042', 'Modeling/Creator/gravure', 'JP fashion model, TikToker, YouTuber, Instagrammer and gravure idol (Osaka); DOB matches Wikidata; age 21')
P('Q111111957', 'Modeling/Creator', 'JP fashion model, tarento, Instagrammer and TikToker (LARME magazine, Mezamashi TV Imadoki Girl); DOB matches Wikidata', name='Kirari')
P('Q111112760', 'Modeling/TV', 'JP fashion model and tarento, 5th editor-in-chief of EMMARY; DOB matches Wikidata')
# ---- batch 4 (jawiki_b4.json)
P('Q111112894', 'Gravure modeling/acting', 'JP gravure idol, model and actress, former #Babababambi member; DOB matches Wikidata')
P('Q111113010', 'Modeling/Creator', 'JP influencer, model, YouTuber and TikToker (Hokkaido); DOB matches Wikidata', name='Ryoka Orita')
P('Q111113077', 'Modeling/acting', 'JP model and actress (real name not disclosed); DOB matches Wikidata', name='Arisa (有咲)')
R('Q111113517', 'scope-ambiguous', 'JP idol active in South Korea (Billlie member); ' + SA)
P('Q111113983', 'Modeling', 'JP fashion model (Elina Saito); DOB matches Wikidata')
X('Q111280247', 'Deceased: the ja-wiki lead records 1999年7月14日 - 2023年8月17日 (YouTuber Hina Gosai, formerly Hina-chan 5-sai); the catalog covers living creators only - not added (Wikidata DOB 1999-07-04 also differs from the page)')
P('Q11189351', 'Modeling/TV', 'JP fashion model and tarento (A-plus); DOB matches Wikidata', name='AMO')
P('Q11190051', 'Modeling/acting', 'JP fashion model and actress (Tokyo; real name Agatha Hamano per lead); DOB matches Wikidata', name='Agatha (吾紗)')
P('Q112238824', 'Modeling', 'JP fashion model (Hyogo); age 18 (reached 18 on 2026-05-25, before the check date); DOB matches Wikidata')
P('Q112239160', 'Modeling/music', 'JP idol, singer and model, FRUITS ZIPPER member; DOB matches Wikidata')
P('Q112239317', 'Modeling/acting', 'JP actress and model (Kumamoto); DOB matches Wikidata')
P('Q11224666', 'Modeling/fashion design', 'JP fashion model and fashion designer (Hokkaido); DOB matches Wikidata', name='Ikumi (いくみ)')
P('Q11229139', 'Modeling', 'JP fashion model (Tokyo; Japanese father, Algerian mother); DOB matches Wikidata; article title 柿木理紗 (Risa Kakinoki) while the Wikidata English label is LISSA (name alias noted)', name='Risa Kakinoki (LISSA)')
P('Q11235241', 'Gravure modeling/acting', 'JP gravure idol and actress; DOB matches Wikidata')
R('Q11242341', 'scope-ambiguous', 'JP entrepreneur per the ja-wiki lead (Wikidata occupation model not reflected in the lead); adult (DOB matches Wikidata)')
P('Q11251442', 'Modeling', 'JP model (Nara; Waseda University commerce graduate); DOB matches Wikidata')
P('Q11268896', 'Yoga instructor/gravure modeling', 'JP tarento, yoga instructor and former gravure idol (Chiba); DOB matches Wikidata; article title しづか while the Wikidata English label is Shizuka Miyazawa (name alias noted)', name='Shizuka (しづか)')
P('Q11275705', 'Modeling/music/acting', 'JP fashion model, singer and actress (Kitty Lights & Entertainment); DOB matches Wikidata')
P('Q11293371', 'Modeling', 'JP fashion model, from Orange County, California; DOB matches Wikidata')
R('Q11304938', 'scope-ambiguous', 'TW tarento per the ja-wiki lead (Sunny Lin, 林采緹); ' + SA)
# ---- batch 5 (jawiki_b5.json)
P('Q11310438', 'Modeling', 'JP-BR fashion model (Brazilian-Japanese); DOB matches Wikidata; article title 湊ジュリアナ while the Wikidata English label is Juriana Minato (name alias noted)', name='Juliana Minato')
P('Q11314520', 'Modeling', 'HK-born model (郭思琳, Wandle Production); DOB matches Wikidata; Wikidata English label Margiela K, ja-wiki title セリーナ・クオック (name alias noted)', name='Margiela K (郭思琳)')
R('Q11316616', 'AGE_PARTIAL', 'JP fashion model and musician (Name Management); the ja-wiki lead gives only the month and day (11月16日); Wikidata 1987-11-16 unconfirmed on page')
P('Q11317810', 'Modeling', 'JP fashion model (Tokyo; Chelsea Maika Thompson per lead); DOB matches Wikidata')
P('Q11319115', 'Modeling', 'JP fashion model from Oahu, Hawaii (Taylor Suzuki per lead); DOB matches Wikidata', name='Taylor Suzuki')
R('Q11322421', 'scope-ambiguous', 'JP freelance announcer (North Production); ' + SA)
P('Q11323478', 'Modeling/TV', 'JP tarento and model based in Aichi Prefecture - regional creator; DOB matches Wikidata')
P('Q11324288', 'Modeling', 'US-born former fashion model in Japan (formerly Stardust Promotion); DOB matches Wikidata', name='Nicole (ニコル, model)')
P('Q11328625', 'Modeling/TV/music', 'JP fashion model, tarento, singer and actress (Emma Burns; active as Emma Asahina from 2022 and, from 2026, as TBS announcer Ema Burns); DOB matches Wikidata', name='Emma Burns')
R('Q11333636', 'AGE_PARTIAL+scope-ambiguous', 'JP actress (Sapporo); the ja-wiki lead gives only the month and day (7月6日); Wikidata 1993-07-06 unconfirmed on page; no modeling / creator activity in the lead')
P('Q11341015', 'Modeling/TV/fashion design', 'JP fashion model, tarento and designer (Marie Pascal); DOB matches Wikidata', name='Marie (Marie Pascal)')
R('Q11345813', 'DOB_CONFLICT', 'JP fashion model, singer and tarento formerly active in Japan (yurisa; real name Yurisa Asama); ja-wiki lead DOB 1984-07-27 vs Wikidata 1985-07-27 - year-level conflict, no value chosen (both adult)')
P('Q11352471', 'Modeling/gravure/acting', 'JP actress, fashion model and gravure idol (Kanazawa); DOB matches Wikidata', name='Maki Isso')
P('Q11353689', 'Modeling', 'JP fashion model (formerly Nanaka Araki); DOB matches Wikidata', name='Nanaka (七菜香)')
P('Q11354928', 'Modeling/acting', 'JP actress (former child actor) and model (Tokyo); DOB matches Wikidata')
P('Q11356507', 'Modeling/acting', 'JP actress and fashion model (Saitama); DOB matches Wikidata')
P('Q113566970', 'Modeling/music', 'JP idol, fashion model and actor (Chiba); age 18 (reached 18 on 2026-01-27, before the check date); DOB matches Wikidata')
P('Q113567066', 'Modeling/gravure/dance', 'JP ballerina, fashion model, actress, gravure idol and member of the idol group Kimi to Miru Sora (Platinum Production); DOB matches Wikidata')
P('Q113567700', 'Modeling/gravure/acting', 'JP model, gravure idol and actress (Nagara Management; Ellie Misumi per lead while the Wikidata English label is Erii Misumi - name alias noted); DOB matches Wikidata', name='Ellie Misumi')
# ---- batch 6 (jawiki_b6.json)
P('Q11357431', 'Modeling/TV', 'JP fashion model and tarento (Tokyo); DOB matches Wikidata')
P('Q11358578', 'Modeling/music', 'JP singer, fashion model and tarento (Tokyo); DOB matches Wikidata')
P('Q11358616', 'Gravure modeling/music', 'JP singer and gravure idol, member of the idol group choice? (formerly Yuna Mochizuki); ' + GR + '; DOB matches Wikidata')
P('Q11359873', 'Modeling/acting', 'JP fashion model and actress (Miyazaki); DOB matches Wikidata')
R('Q11362569', 'DOB_CONFLICT+scope-ambiguous', 'JP entrepreneur, tarento, model, artist and former adult-video actress per the ja-wiki lead; ja-wiki lead DOB 1989-01-11 vs Wikidata 1991-04-10 - conflict, no value chosen (both adult); adult-film history also outside focus categories - manual scope decision')
R('Q11362815', 'scope-ambiguous', 'JP actress (Ladybird); ' + SA)
P('Q11362820', 'Modeling/TV', 'JP tarento and fashion model (Uki, Kumamoto); DOB matches Wikidata')
P('Q11363074', 'Modeling', 'JP fashion model (Sophie Promotion); DOB matches Wikidata')
P('Q11364225', 'Modeling/acting', 'JP model and actress (ESPRIT MODEL AGENCY); DOB matches Wikidata')
P('Q11364507', 'Modeling', 'JP fashion model (Uwajima, Ehime); DOB matches Wikidata')
P('Q11364847', 'Gravure modeling/acting', 'JP actress and former gravure idol (Kumamoto); DOB matches Wikidata')
R('Q11365170', 'scope-ambiguous', 'JP former tarento (Saitama); ' + SA)
P('Q11365665', 'Modeling/TV', 'JP tarento and former fashion model (Kisarazu, Chiba); DOB matches Wikidata')
R('Q11365669', 'scope-ambiguous', 'JP actress (Nanyo, Yamagata); ' + SA)
P('Q11365821', 'Modeling/acting', 'JP actress and fashion model (Fukui); DOB matches Wikidata; article title 瑠璃奈 while the Wikidata English label is Rurina Nakamura (name alias noted)', name='Rurina (瑠璃奈)')
P('Q11365870', 'Modeling/TV/acting', 'JP fashion model, tarento and actress (Shochiku Geino); DOB matches Wikidata')

missing = [r['qid'] for r in rows if r['qid'] not in V]
extra = [q for q in V if q not in by]
print('missing', missing, 'extra', extra)
assert not missing and not extra


def default_name(r):
    en = (r.get('en') or '').strip()
    # catalog convention (English-Wikipedia style): macrons dropped
    return en.translate(str.maketrans('ōūāēīŌŪĀĒĪ', 'ouaeiOUAEI'))


lines = []
buckets = []
for r in rows:
    q = r['qid']
    verdict, cat, note, name, dob, igo, ig2o, tto = V[q]
    name = name or default_name(r)
    assert name, q
    ex = r['extract'].replace('\n', ' ').replace('|', '/')
    first = ex.split('。')[0] + '。'
    quote = first if len(first) <= 200 else first[:200] + '...'
    d = dob or r['dob']
    ev = f'ja-wiki lead: 「{quote}」 - {note}'
    if verdict == 'REJECT':
        ev = note
    assert '|' not in ev, q
    lines.append(f"{q}|{name}|{d}|{verdict}|{cat}|{ev}|{r['wiki']}")
    igs = r['igs']
    tts = r['tts']
    ig = igs[0] if igs else ''
    ig2 = igs[1] if len(igs) > 1 else ''
    tt = tts[0] if tts else ''
    if igo is not None:
        ig = igo
    if ig2o is not None:
        ig2 = ig2o
    if tto is not None:
        tt = tto
    buckets.append(dict(qid=q, name=name, dob=d, ig=ig, ig2=ig2, tt=tt, wiki=r['wiki'],
                        ja=r.get('ja', ''), kana=r.get('kana', ''), file='model_ja_chunk*.txt'))

Path(ROOT / 'data/research/verification_s30_log.tsv').write_text('\n'.join(lines) + '\n')
json.dump({'model': buckets}, open(ROOT / 'data/research/s30_verify_buckets.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(v[0] for v in V.values()))
print(Counter(v[1] for v in V.values() if v[0] == 'REVIEW'))
