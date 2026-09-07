#!/usr/bin/env python3
"""Session 31 — verdict table for the Japanese-Wikipedia slice of the Wikidata model pool
(female, occupation model / fashion model / personal trainer / bodybuilder / fitness model,
born 1985-2008, Instagram or TikTok handle, ja-wiki article, NO en-wiki article; page 2,
ORDER BY ?p LIMIT 150 OFFSET 150 -> 150 unique people -> 145 new after Q-ID/name/handle dedup).

Input : data/research/s31_raw/model_ja2_checked.json  (rows + ja-wiki lead extracts + labels)
Output: data/research/verification_s31_log.tsv       (qid|name|dob|verdict|category-or-flags|evidence|url)
        data/research/s31_verify_buckets.json        (handles for scripts/session31_apply.py)

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
rows = json.load(open(ROOT / 'data/research/s31_raw/model_ja2_checked.json'))
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
P('Q11366379', 'Modeling', 'JP fashion model, former child actress (Nagano; incubation); DOB matches Wikidata')
P('Q11366750', 'Modeling/acting', 'JP model, actress and radio personality; DOB matches Wikidata')
P('Q11367531', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata')
P('Q11370992', 'Modeling/TV', 'JP fashion model and tarento, former professional boxer; DOB matches Wikidata')
P('Q11376618', 'Modeling/gravure/comedy', 'JP former comedy actress, former model and former gravure idol (Yoshimoto Osaka); DOB matches Wikidata')
P('Q11376699', 'Modeling/TV', 'JP fashion model and tarento (Nagatoro, Saitama); DOB matches Wikidata')
R('Q11377251', 'scope-ambiguous', 'JP actress (Kagawa); ' + SA)
P('Q11378550', 'Modeling', 'JP fashion model (Fussa, Tokyo); DOB matches Wikidata')
P('Q11378585', 'Modeling', 'JP fashion model (FLOS -> OFFICE RHIZOME); DOB matches Wikidata')
P('Q11379791', 'Modeling', 'JP fashion model (Fukuoka); DOB matches Wikidata', name='Niina Ito')
R('Q11380089', 'scope-ambiguous', 'JP musical actress, former child actress; ' + SA, name='Sayaka Ito')
R('Q11380176', 'scope-ambiguous', 'JP child-actress-turned-actress (Tokyo); the lead documents acting only; ' + SA + '; age 24', name='Sei Ito')
P('Q11381550', 'Modeling/acting', 'JP actress and model, former Takarazuka Revue Cosmos Troupe star; DOB matches Wikidata')
P('Q11382041', 'Gravure modeling/swimwear/music', 'JP idol, gravure idol and producer; ' + GR + '; DOB matches Wikidata', name='Miyu Kusunoki')
P('Q11382397', 'Modeling/race queen/TV', 'JP fashion model, tarento and former race queen (Hokkaido); DOB matches Wikidata')
P('Q11383030', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata')
P('Q11383234', 'Modeling/acting', 'JP fashion model and actress (Iwaki, Fukushima); DOB matches Wikidata')
P('Q11383513', 'Gravure modeling/swimwear/TV', 'JP tarento, gravure idol and actress (office RHIZOME); ' + GR + '; DOB matches Wikidata', name='Sakura Sato')
P('Q11383706', 'Modeling/beauty', 'JP beauty model, former reader model, exclusive model for MAQUIA since 2015; DOB matches Wikidata', name='Yuria Sato')
P('Q11383831', 'Gravure modeling/swimwear', 'JP former gravure idol (Artist House Pyramid); ' + GR + '; DOB matches Wikidata', name='Kazusa Sato')
# ---- batch 1 (jawiki_b1.json)
R('Q11384230', 'scope-ambiguous', 'JP freelance announcer, former TBS announcer; ' + SA, name='Nagisa Sato')
P('Q11384240', 'Modeling', 'JP fashion model; DOB matches Wikidata', name='Sena Sato')
P('Q11384563', 'Modeling', 'JP fashion model (Incent); DOB matches Wikidata', name='Asuka Sato')
P('Q11384956', 'Modeling/TV/acting', 'JP tarento, actress and fashion model (Shinagawa, Tokyo); DOB matches Wikidata')
P('Q11385082', 'Modeling/gravure/swimwear/race queen/TV', 'JP model, tarento, gravure idol, newscaster and reporter, former race queen (Takamatsu); DOB matches Wikidata')
P('Q11385508', 'Modeling', 'JP fashion model (Sony Music Artists; Tokyo); DOB matches Wikidata')
P('Q11387708', 'Modeling/TV', 'JP tarento and model (Kobe); DOB matches Wikidata', name='Emi Yuki')
P('Q11389004', 'Modeling/acting', 'South Korean-national fashion model and actress active in Japan (Akashi, Hyogo); DOB matches Wikidata')
P('Q11391818', 'Modeling/fashion design', 'JP fashion model and designer of the apparel brand michellMacaron (launched 2012); DOB matches Wikidata; the Wikidata TikTok handle michellmacaron.official is her brand account and is recorded as documented, brand-account status noted')
P('Q11396949', 'Modeling/Creator/acting', 'JP influencer, actress, tarento and model (Tokyo); DOB matches Wikidata')
P('Q11397391', 'Modeling', 'JP fashion model (Next Satisfaction; stage name also 前田よしみ); DOB matches Wikidata')
P('Q11399408', 'Modeling', 'JP reader model and former fashion model; DOB matches Wikidata', name='Rubi Kato')
P('Q11399621', 'Modeling/TV', 'JP fashion model and tarento (formerly Front / Esprit Division); DOB matches Wikidata')
P('Q11401614', 'Modeling/acting/TV', 'JP actress, fashion model and tarento (Osaka); article title 北川都喜子 while the Wikidata English label keeps the former stage name 北川富紀子 (same reading Tokiko Kitagawa - name alias noted); DOB matches Wikidata')
P('Q11405418', 'Modeling/acting', 'JP fashion model and actress (Saitama); DOB matches Wikidata')
P('Q11407994', 'Modeling/TV', 'JP fashion model and tarento (Sanda, Hyogo); DOB matches Wikidata', name='Yuka Nanjo')
P('Q11408667', 'Modeling/acting', 'JP fashion model and actress (Okinawa); DOB matches Wikidata')
P('Q11411185', 'Modeling', 'JP fashion model (Chiba; Incent group / Idea); DOB matches Wikidata')
P('Q11412157', 'Modeling/acting/music', 'JP actress, singer, fashion model, tarento and producer (Komaki, Aichi); DOB matches Wikidata')
P('Q11412632', 'Modeling/acting', 'JP fashion model and actress (Kanagawa); DOB matches Wikidata')
# ---- batch 2 (jawiki_b2.json)
P('Q11413075', 'Gravure modeling/swimwear/wellness', 'JP beauty-chiropractic practitioner and former gravure idol (debut 2002); ' + GR + '; DOB matches Wikidata')
P('Q11413809', 'Modeling/music', 'JP singer and fashion model (Yachimata, Chiba); DOB matches Wikidata')
P('Q11423266', 'Modeling', 'JP fashion model (Kanagawa); DOB matches Wikidata')
P('Q11423426', 'Gravure modeling/swimwear/TV', 'JP former tarento and former gravure idol (Aichi); ' + GR + '; DOB matches Wikidata')
P('Q11425081', 'Modeling/acting', 'JP fashion model and actress (formerly Pearl); DOB matches Wikidata')
P('Q11425346', 'Modeling', 'JP fashion model (Nagano); DOB matches Wikidata')
P('Q11425857', 'Modeling/acting', 'JP fashion model and actress (Tokyo); DOB matches Wikidata')
P('Q11428507', 'Modeling/TV/music', 'JP tarento, singer and model, nickname Maipuni; DOB matches Wikidata; ja-wiki article 塚本舞 (タレント)')
P('Q11430100', 'Modeling', 'JP fashion model (Osaka); ja-wiki article 斎藤夏美 while the Wikidata English label is the mononym Natsumi (name alias noted); same romanised name as 斉藤夏海 (also in this batch) - kanji added to disambiguate; DOB matches Wikidata', name='Natsumi Saito (斎藤夏美)')
P('Q11431607', 'Modeling', 'JP model (legal name Catherine Yumeko Oguchi per lead); DOB matches Wikidata', name='Yumeko Catharine')
P('Q11432592', 'Modeling', 'JP fashion model (Tochigi); DOB matches Wikidata', name='Chihiro Oide')
R('Q11434515', 'scope-ambiguous', 'JP freelance announcer (Tokyo); ' + SA, name='Kaori Otera')
P('Q11435190', 'Modeling/race queen/TV', 'JP model, tarento and former race queen (Shiga); DOB matches Wikidata')
P('Q11435296', 'Modeling/acting', 'JP model and actress (Asahi, Toyama); DOB matches Wikidata', name='Arisa Ohira')
P('Q11435943', 'Modeling/TV/acting', 'JP tarento, actress and fashion model (Kanagawa), Mystery Hunter reporter; DOB matches Wikidata', name='Airi Osugi')
P('Q11436534', 'Modeling', 'JP gyaru fashion model (legal name Rina Vanessa Ohashi per lead); DOB matches Wikidata', name='Rina Ohashi')
P('Q11437464', 'Modeling/music/acting', 'JP fashion model, idol, singer and actress (Miss Marine 6th generation, Canary Club member); DOB matches Wikidata', name='Ikuko Oura')
P('Q11438122', 'Modeling/music', 'JP former fashion model, former singer and former tarento (Shiga); DOB matches Wikidata', name='Rikako Oya')
P('Q11438251', 'Modeling/TV', 'JP fashion model and tarento (Setagaya, Tokyo; formerly Platinum Production); DOB matches Wikidata', name='Eri Oishi')
P('Q11439779', 'Modeling', 'JP fashion model (Sun Music Production); DOB matches Wikidata', name='Kelly Ogama')
# ---- batch 3 (jawiki_b3.json)
P('Q114460792', 'Modeling/Creator/TV', 'JP fashion model, tarento, actress and YouTuber, exclusive egg model; DOB matches Wikidata; age 21')
P('Q11446121', 'Gravure modeling/swimwear/business', 'JP former gravure idol, fashion model and tarento, CEO of Balance Style Inc.; ' + GR + '; DOB matches Wikidata')
R('Q11449055', 'AGE_PARTIAL', 'JP gravure idol, tarento and actress (Kyoto) - in scope, but the ja-wiki lead carries no birth date; Wikidata 1985-02-06 unconfirmed on page')
P('Q11449569', 'Gravure modeling/swimwear', 'JP gravure idol (Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11450192', 'Modeling', 'JP fashion model (Fukuoka); DOB matches Wikidata')
R('Q11450598', 'scope-ambiguous', 'JP businesswoman (Tokyo); the lead documents business activity only; ' + SA)
P('Q11450856', 'Modeling/gravure/swimwear/race queen/TV', 'JP model, tarento, former race queen and former gravure idol; DOB matches Wikidata')
P('Q11451114', 'Modeling/TV/acting', 'JP tarento, fashion model and actress (Katagami, Akita); DOB matches Wikidata')
P('Q11455184', 'Modeling/TV', 'JP fashion model and tarento (Vithmic Model Agency); DOB matches Wikidata')
P('Q11457235', 'Modeling/acting', 'JP model and actress (Ina, Nagano); distinct from the already-catalogued actress 小池唯 Yui Koike (a different woman with a different handle, catalogued in Session 26) - kanji added to the display name to disambiguate; DOB matches Wikidata', name='Yui Koike (小池由)')
P('Q11457901', 'Modeling/TV/acting', 'JP fashion model, tarento and actor (Yokohama); DOB matches Wikidata')
R('Q11458293', 'scope-ambiguous', 'JP adult-video actress, former idol and former gravure idol per the ja-wiki lead (Bstar); adult (DOB matches Wikidata) but adult-film work is outside the focus categories - held for a manual scope decision consistent with Session 28 (Annie Knight, R-2026-265) and Session 30 (MINAMO, Sakura Misaki)')
R('Q11458967', 'scope-ambiguous', 'JP freelance announcer; ' + SA)
R('Q11459291', 'scope-ambiguous', 'JP freelance announcer and patissier, former Sendai Broadcasting announcer; ' + SA)
P('Q11460523', 'Modeling/acting/TV', 'JP actress, tarento and fashion model (Chiba); DOB matches Wikidata', name='Ryo Ogawa')
P('Q11461310', 'Modeling', 'JP fashion model (legal name 小林瑤, same reading); DOB matches Wikidata', name='Yo Kobayashi')
P('Q11461990', 'Modeling', 'JP model (Kanazawa, Ishikawa); lead spells the given name アヤカ; DOB matches Wikidata')
P('Q11462092', 'Modeling', 'JP gyaru fashion model; DOB matches Wikidata')
P('Q11462535', 'Modeling', 'JP fashion model (Choshi, Chiba); DOB matches Wikidata')
P('Q11462869', 'Modeling/TV/music', 'JP model, tarento and singer (Muroran, Hokkaido); DOB matches Wikidata', name='Yui Kodama')
# ---- batch 4 (jawiki_b4.json)
P('Q11463294', 'Modeling/acting', 'JP model and actress (Sendai, Miyagi); DOB matches Wikidata')
P('Q11463732', 'Modeling', 'JP fashion model (CV management); DOB matches Wikidata')
P('Q11465345', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata')
P('Q11465417', 'Modeling/gravure/swimwear/acting', 'JP fashion model, actress and former gravure idol (Kanagawa); DOB matches Wikidata')
P('Q11465846', 'Gravure modeling/swimwear/TV', 'JP former gravure idol and tarento (Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11466192', 'Gravure modeling/swimwear', 'JP gravure idol (Adachi, Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11466194', 'Gravure modeling/swimwear/acting', 'JP actress and gravure idol, representative of Fantasy LLC; ' + GR + '; DOB matches Wikidata')
P('Q11466566', 'Gravure modeling/swimwear/TV', 'JP tarento, gravure idol and actress (Hyogo); ' + GR + '; DOB matches Wikidata', name='Yuna Yamasaki')
R('Q11466597', 'AGE_PARTIAL', 'JP model (Yokohama) - in scope, but the ja-wiki lead carries no birth date; Wikidata 1989-04-04 unconfirmed on page')
P('Q11466928', 'Gravure modeling/swimwear/TV', 'JP gravure idol and tarento (Abeno, Osaka); ' + GR + '; DOB matches Wikidata')
R('Q11473249', 'scope-ambiguous', 'JP beauty specialist (biyoka); the lead documents no modeling or creator activity; ' + SA)
P('Q11473426', 'Modeling/TV', 'JP tarento and model, active as 岡田ユリエ with Vithmic since 2012; DOB matches Wikidata')
R('Q11475071', 'scope-ambiguous', 'JP Nippon TV announcer; ' + SA)
P('Q11475425', 'Modeling/race queen/TV', 'JP model and tarento, former race queen; DOB matches Wikidata')
P('Q11476090', 'Modeling', 'JP gyaru fashion model; DOB matches Wikidata')
P('Q11477536', 'Modeling/TV', 'JP fashion model and tarento, nickname Manatii; DOB matches Wikidata')
P('Q11478958', 'Modeling/race queen/acting', 'JP model, actress and former race queen (Chiba; Shuru); DOB matches Wikidata')
P('Q11482335', 'Modeling/gravure/swimwear/TV', 'JP tarento, model and gravure idol (Yonezawa, Yamagata; Saegusa Planning); DOB matches Wikidata')
P('Q11482549', 'Modeling/Creator', 'JP former fashion model, former CanCam exclusive model, now a lifestyle influencer per the lead; DOB matches Wikidata')
P('Q11483031', 'Modeling', 'JP fashion model (HOOK); DOB matches Wikidata')
# ---- batch 5 (jawiki_b5.json)
P('Q11483188', 'Modeling/TV', 'JP fashion model and tarento, reader model turned Happie nuts exclusive model (2010); DOB matches Wikidata')
P('Q11483383', 'Modeling/acting/TV', 'JP actress, model and tarento (Sendai, Miyagi); DOB matches Wikidata; ja-wiki article 平田薫 (タレント)')
R('Q11483959', 'scope-ambiguous', 'JP actress (former stage name 幸元紫世羅); ' + SA)
P('Q11483998', 'Modeling/race queen/acting', 'JP fashion model, actress and race queen (Saitama); DOB matches Wikidata', name='Sae Missho')
P('Q11485448', 'Modeling/acting/TV', 'JP actress, model and tarento (Hita, Oita; married name Hayashi per lead); DOB matches Wikidata')
P('Q11485600', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata')
P('Q11486340', 'Modeling/TV', 'JP tarento and newscaster, former fashion model; DOB matches Wikidata')
P('Q11486417', 'Modeling', 'JP gyaru fashion model (Higashiyamato, Tokyo); DOB matches Wikidata')
P('Q11488018', 'Modeling/acting', 'JP fashion model and actress, former child actress (Platinum Production); DOB matches Wikidata')
P('Q11488218', 'Gravure modeling/swimwear/TV', 'JP tarento and gravure model (Osaka); ' + GR + '; DOB matches Wikidata')
R('Q11491029', 'scope-ambiguous', 'JP former idol, former SUPER GiRLS member and leader; ' + SA)
P('Q11495506', 'Gravure modeling/swimwear', 'JP gravure idol (Miyazaki; Breeze Promotion); ' + GR + '; DOB matches Wikidata; TikTok handle only (no Instagram in Wikidata)')
P('Q11496978', 'Modeling/acting', 'JP actress and model (Box Corporation); DOB matches Wikidata')
R('Q11497949', 'scope-ambiguous', 'JP actress and tarento (Tokyo); ' + SA)
P('Q114981726', 'Modeling/TV', 'JP tarento and model (Saitama; NRC Production); DOB matches Wikidata; age 21')
P('Q11500189', 'Modeling/journalism', 'JP fashion model and journalist (Bark in Style); DOB matches Wikidata', name='Alice Saito')
P('Q11500244', 'Modeling/art', 'JP fashion model and artist (formerly Twin Planet); same romanised name as 斎藤夏美 (also in this batch) - kanji added to disambiguate; DOB matches Wikidata', name='Natsumi Saito (斉藤夏海)')
P('Q11501138', 'Modeling/acting', 'JP actress and model (Saitama); DOB matches Wikidata')
P('Q11501255', 'Modeling', 'JP model (Maromokamiruku); DOB matches Wikidata; ja-wiki article 新井美穂 (モデル)')
R('Q11502723', 'scope-ambiguous', 'JP freelance announcer, former Broadcasting System of Niigata announcer; ' + SA)
# ---- batch 6 (jawiki_b6.json)
P('Q11504169', 'Modeling', 'JP reader model (Dokumo Cafe); DOB matches Wikidata')
P('Q11510112', 'Modeling', 'JP fashion model (Okayama); DOB matches Wikidata')
P('Q11510858', 'Modeling', 'JP fashion model (Kawagoe, Saitama; Front / Esprit Division); DOB matches Wikidata')
P('Q11512834', 'Gravure modeling/swimwear/acting', 'JP gravure idol and actress (Saitama); ' + GR + '; DOB matches Wikidata')
P('Q11513814', 'Modeling', 'JP fashion model, member of the model unit Model Girls; mononym; DOB matches Wikidata', name='Haruki (春輝, model)')
P('Q11516928', 'Modeling/TV/music', 'JP fashion model and tarento, former predia idol-group member (Osaka); DOB matches Wikidata')
P('Q11517050', 'Modeling/race queen/acting', 'JP fashion model, actress, tarento and race queen (Chiba); DOB matches Wikidata')
P('Q11517056', 'Modeling/acting', 'JP model and actress active as the mononym サヤカ (Sayaka); the Wikidata English label keeps the former stage name Ichika Mochizuki (name alias noted); DOB matches Wikidata', name='Sayaka (サヤカ, model)')
P('Q11519250', 'Modeling/music', 'JP fashion model, former E-girls member; DOB matches Wikidata')
P('Q11519363', 'Modeling/race queen', 'JP model and race queen (Takayama, Gifu); DOB matches Wikidata')
P('Q11519621', 'Modeling/TV', 'JP fashion model and tarento (Hokkaido); lead gives the full name 奥田未莉 while the Wikidata English label is the mononym Miri (name alias noted); DOB matches Wikidata', name='Miri Okuda')
P('Q11528588', 'Modeling', 'JP fashion model (Chiba); DOB matches Wikidata; ja-wiki article 東野佑美 (モデル)')
P('Q11528849', 'Modeling/TV', 'JP tarento and model (Ibaraki); DOB matches Wikidata')
P('Q11529043', 'Modeling/music', 'JP former fashion model and former tarento (Hokkaido), member of the idol group Tenko Shojo* 2014-2022; DOB matches Wikidata')
P('Q11529425', 'Modeling', 'JP fashion model (Saitama); DOB matches Wikidata')
R('Q11529752', 'scope-ambiguous', 'JP tarento and actress (Kobe); ' + SA)
P('Q11529869', 'Modeling/acting/TV', 'JP actress, tarento and model (Fukuoka); DOB matches Wikidata')
P('Q11530072', 'Modeling/Creator', 'JP fashion model and blogger; DOB matches Wikidata')
P('Q11530172', 'Modeling/acting', 'JP fashion model and actress (Tokyo); DOB matches Wikidata')
P('Q11531080', 'Modeling/fashion design', 'JP fashion-brand producer and fashion model, former EMODA producer; DOB matches Wikidata')
# ---- batch 7 (jawiki_b7.json)
P('Q11531087', 'Modeling/TV', 'JP fashion model and tarento, regular model for MORE (Saitama); DOB matches Wikidata')
P('Q11532674', 'Modeling', 'JP fashion model (formerly TWIN PLANET ENTERTAINMENT); DOB matches Wikidata')
P('Q11533058', 'Modeling/acting', 'JP fashion model and actress active as the mononym 恵理 (Eri; legal name Eri Maruta per lead; Ueda, Nagano); DOB matches Wikidata')
P('Q11533261', 'Gravure modeling/swimwear/race queen/TV', 'JP tarento, gravure model and race queen (Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11533992', 'Gravure modeling/swimwear', 'JP gravure idol (Niigata); ' + GR + '; DOB matches Wikidata')

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
                        ja=r.get('ja', ''), kana=r.get('kana', ''), file='model_ja2_chunk*.txt'))

Path(ROOT / 'data/research/verification_s31_log.tsv').write_text('\n'.join(lines) + '\n')
json.dump({'model': buckets}, open(ROOT / 'data/research/s31_verify_buckets.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(v[0] for v in V.values()))
print(Counter(v[1] for v in V.values() if v[0] == 'REVIEW'))
