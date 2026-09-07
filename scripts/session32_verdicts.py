#!/usr/bin/env python3
"""Session 32 — verdict table for the Japanese-Wikipedia slice of the Wikidata model pool
(female, occupation model / fashion model / personal trainer / bodybuilder / fitness model,
born 1985-2008, Instagram or TikTok handle, ja-wiki article, NO en-wiki article; page 3,
ORDER BY ?p LIMIT 150 OFFSET 300 -> 150 unique people -> 140 new after Q-ID/name/handle dedup).

Input : data/research/s32_raw/model_ja3_checked.json  (rows + ja-wiki lead extracts + labels)
Output: data/research/verification_s32_log.tsv       (qid|name|dob|verdict|category-or-flags|evidence|url)
        data/research/s32_verify_buckets.json        (handles for scripts/session32_apply.py)

Verdict rules (Session 27-31 precedent, applied to ja-wiki leads):
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
rows = json.load(open(ROOT / 'data/research/s32_raw/model_ja3_checked.json'))
by = {r['qid']: r for r in rows}

V = {}


QUOTE = {}


def P(q, cat, note, name=None, dob=None, ig=None, ig2=None, tt=None, quote=None):
    V[q] = ('PROMOTE', cat, note, name, dob, ig, ig2, tt)
    if quote:
        QUOTE[q] = quote


def R(q, flags, note, name=None, ig=None, ig2=None, tt=None, dob=None, quote=None):
    V[q] = ('REVIEW', flags, note, name, dob, ig, ig2, tt)
    if quote:
        QUOTE[q] = quote


def X(q, note, name=None):
    V[q] = ('REJECT', 'excluded', note, name, None, None, None, None)



SA = 'no modeling / creator activity documented in the lead; adult (DOB matches Wikidata)'
GR = 'gravure idol = swimsuit / magazine model (objective Japanese occupational category)'
FM = 'all listed occupations are former and the lead documents no current public activity, so current creator status and handle currency cannot be confirmed from the lead; adult (DOB matches Wikidata)'

# ---- batch 0 (jawiki_b0.json)
R('Q11536025', 'AGE_PARTIAL+scope-ambiguous', 'JP stage actress and singer (Nagano); the lead gives only the month and day of birth (no year) and documents no modeling activity; Wikidata year unconfirmed on the page', dob='UNKNOWN')
P('Q11536385', 'Modeling', 'JP gyaru fashion model; DOB matches Wikidata')
P('Q11537647', 'Modeling/acting', 'JP fashion model and actress (Guns Management), active under the mononym 桔花 Kikka; DOB matches Wikidata', name='Kikka (桔花, model)')
P('Q11537870', 'Gravure modeling/swimwear/music', 'JP live idol and gravure idol (Chiba); ' + GR + '; DOB matches Wikidata')
R('Q11538252', 'scope-ambiguous', 'JP actress (former stage names Ako Masuki / Ako Masuki 桝木亜子); ' + SA)
P('Q11539214', 'Gravure modeling/swimwear', 'JP gravure idol (Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11539715', 'Modeling', 'JP gyaru fashion model; DOB matches Wikidata')
P('Q11540371', 'Modeling/acting', 'JP fashion model and actor (Fujiidera, Osaka); DOB matches Wikidata')
P('Q11541155', 'Modeling/TV/music/acting', 'JP tarento, model, singer and actress, also active as SELEN; DOB matches Wikidata')
P('Q11541727', 'Modeling/acting', 'JP fashion model and actress (Tokyo); DOB matches Wikidata')
P('Q11544103', 'Modeling', 'JP fashion model (Miyagi); DOB matches Wikidata')
P('Q11544338', 'Modeling', 'JP model and former tarento (Osaka); article title 橘ちえよ, lead name 橘知衣代; DOB matches Wikidata')
P('Q11546014', 'Modeling/acting', 'JP model and actress (Osaka; Asobisystem); DOB matches Wikidata')
P('Q11546193', 'Gravure modeling/swimwear/music/TV', 'JP flautist, model, tarento and gravure model active under the mononym arisa (article 武田有彩; name alias noted); ' + GR + '; DOB matches Wikidata')
P('Q11546260', 'Modeling', 'JP fashion model known from the gyaru magazine Happie nuts; DOB matches Wikidata')
P('Q11546537', 'Modeling/fashion design', 'JP gyaru fashion model and fashion designer; DOB matches Wikidata')
P('Q11547413', 'Modeling/TV', 'Peru-raised JP fashion model and tarento (formerly Amuse); lead gives the full name 比嘉バーバラ Barbara Higa, stage name Barby (name alias noted); DOB matches Wikidata')
P('Q11547473', 'Modeling', 'JP fashion model (Yokohama); DOB matches Wikidata')
P('Q11548328', 'Modeling/TV', 'US-citizen fashion model and tarento active mainly in Japan (legal name Ashley Yuka Daniel per lead); DOB matches Wikidata')
R('Q11548833', 'scope-ambiguous', 'JP tarento and businesswoman (Tokyo); ' + SA)
# ---- batch 1 (jawiki_b1.json)
P('Q11549347', 'Modeling/music', 'JP former reader model and singer (Rikkyo University graduate); DOB matches Wikidata')
R('Q11549855', 'scope-ambiguous', 'JP politician, former Saitama city councillor; the lead documents politics only; ' + SA)
P('Q11549863', 'Modeling/TV/music', 'JP model, tarento and singer active in Japan and Korea (Aomori); DOB matches Wikidata')
P('Q11550028', 'Gravure modeling/swimwear/acting', 'JP former actress, gravure idol and model (Chiba); ' + GR + '; DOB matches Wikidata')
P('Q11550153', 'Modeling/acting', 'JP actress and model, freelance since 2025 per lead; DOB matches Wikidata')
P('Q11551373', 'Modeling/acting/TV', 'JP fashion model, actress and tarento, former exclusive model for non-no, Seventeen and Pichi Lemon; DOB matches Wikidata')
P('Q11551988', 'Modeling', 'JP model, nickname SAYOPI; DOB matches Wikidata')
P('Q11551989', 'Modeling', 'JP fashion model (Kagoshima); DOB matches Wikidata')
P('Q11552128', 'Modeling/music/acting', 'JP model, idol and actress (Yokohama); DOB matches Wikidata')
R('Q11552222', 'scope-ambiguous', 'JP actress (Kushiro, Hokkaido); ' + SA)
P('Q11552519', 'Modeling/fashion design', 'JP fashion model and designer (Tokyo); DOB matches Wikidata')
P('Q115529388', 'Modeling/TV', 'JP model and tarento (Himi, Toyama); DOB matches Wikidata')
P('Q115529608', 'Modeling/race queen', 'JP model and race queen (Hyogo); DOB matches Wikidata')
P('Q115529785', 'Modeling/acting', 'JP model and actress; adult (age nineteen on the check date); DOB matches Wikidata')
P('Q115530086', 'Modeling/Creator/influencer', 'JP fashion model and influencer (Hiroshima); distinct from the review-queue idol Risa Watanabe (a different woman, Sakurazaka46) - katakana added to the display name to disambiguate; DOB matches Wikidata', name='Risa Watanabe (渡辺リサ)')
P('Q11553116', 'Gravure modeling/swimwear/acting/TV', 'JP actress, tarento and gravure idol (Kobe; Excel Human Agency); ' + GR + '; DOB matches Wikidata', quote='沢井 彩華（さわい あやか、1986年10月14日2時頃生まれ。芸名の彩華は本名でもある。）は、日本の女優、タレント、グラビアアイドル。')
R('Q11553888', 'scope-ambiguous', 'JP newscaster (Aichi); ' + SA)
P('Q11554682', 'Modeling/acting', 'JP fashion model and actress (Tokyo); DOB matches Wikidata')
P('Q11557112', 'Modeling/TV', 'JP fashion model and tarento (Asia Promotion); DOB matches Wikidata')
P('Q11557177', 'Modeling/TV/music', 'JP fashion model, tarento and singer (Tokyo); DOB matches Wikidata')
# ---- batch 2 (jawiki_b2.json)
P('Q11557988', 'Gravure modeling/swimwear/music', 'JP former gravure idol and singer; ' + GR + '; DOB matches Wikidata')
P('Q11558284', 'Modeling/acting', 'JP fashion model and actress (former stage name 浦浜亜理沙); DOB matches Wikidata')
R('Q11558750', 'DOB_CONFLICT', 'JP singer, rapper, dancer, fashion model and actress (Hawaii-raised); the ja-wiki lead gives a birth year three years earlier than the Wikidata value (same month and day) - trusted sources conflict, no value chosen; both values are adult', dob='UNKNOWN')
R('Q11560089', 'scope-ambiguous', 'JP former fashion model (former stage name 深沢明莉); ' + FM)
P('Q11560557', 'Modeling/TV', 'JP fashion model and tarento (Sakura, Chiba); DOB matches Wikidata')
P('Q11561027', 'Modeling/music', 'JP model and singer (Kyoto); DOB matches Wikidata')
P('Q11561628', 'Gravure modeling/swimwear/TV/business', 'JP tarento, gravure idol, businesswoman and producer (CEO of ENTAME GIG); ' + GR + '; DOB matches Wikidata')
P('Q11561806', 'Modeling/TV/acting', 'JP tarento, actress and model; DOB matches Wikidata')
P('Q11561981', 'Modeling/sports', 'JP professional bowler and voice actress, former model, tarento and actress (JPBA licence holder); DOB matches Wikidata')
P('Q11562009', 'Modeling', 'JP model (Fukuoka); DOB matches Wikidata')
P('Q11562300', 'Modeling/TV/acting', 'JP tarento, model, actress and reporter (Tokyo); DOB matches Wikidata')
P('Q11562326', 'Gravure modeling/swimwear/TV', 'JP model and tarento, former gravure idol (Iwate); ' + GR + '; DOB matches Wikidata')
P('Q11562513', 'Modeling/TV/acting', 'JP model, tarento and actress; DOB matches Wikidata')
R('Q11562718', 'scope-ambiguous', 'JP former idol, former tarento and former novelist (Kanagawa); ' + SA)
R('Q11562742', 'scope-ambiguous', 'JP actress (Office Yumin); Wikidata label 渡部みずき, article 渡部瑞貴; ' + SA)
P('Q11563553', 'Modeling/TV', 'JP model, tarento and pachinko writer (Kanagawa); DOB matches Wikidata')
P('Q11564060', 'Modeling/acting', 'JP fashion model and actress (Tokyo; Horipro-affiliated agency Booth); DOB matches Wikidata')
P('Q11564455', 'Modeling/acting', 'JP fashion model and actress (formerly Ito Company); DOB matches Wikidata')
R('Q11564490', 'scope-ambiguous', 'JP idol, tarento and actress, former TiiiMO / Tiiigirl member; ' + SA)
R('Q11566521', 'scope-ambiguous', 'JP tarento (Fukuoka; former stage name 安藤徠愛羽); ' + SA, quote='瀬戸 サオリ（せと サオリ、（1988年1月2日 - ）は、日本の女性。タレント。以前の芸名は安藤 徠愛羽（あんどう くれは）。')
# ---- batch 3 (jawiki_b3.json)
R('Q11566688', 'DOB_CONFLICT', 'JP gravure idol, event companion and angling personality (Tokyo); the ja-wiki lead gives a birth year four years later than the Wikidata value (same month and day) - trusted sources conflict, no value chosen; both values are adult', dob='UNKNOWN')
P('Q11568651', 'Modeling', 'JP fashion model (Hyogo); DOB matches Wikidata')
P('Q11575163', 'Modeling/acting/TV', 'JP actress, tarento and fashion model (Sun Music); DOB matches Wikidata')
P('Q11575329', 'Modeling/acting', 'JP actress and fashion model (Tokyo); DOB matches Wikidata')
P('Q11576314', 'Modeling/acting', 'JP fashion model and actress, former child actress (ABP inc.); DOB matches Wikidata')
R('Q115766646', 'scope-ambiguous', 'JP actress, former Sakura Gakuin member (Osaka); adult (age nineteen on the check date); ' + SA)
P('Q11577063', 'Modeling/writing', 'JP fashion model and columnist; DOB matches Wikidata')
P('Q11577327', 'Modeling', 'JP model (Niigata); DOB matches Wikidata')
P('Q11577355', 'Modeling/acting', 'JP actor and fashion model (Kanagawa); DOB matches Wikidata')
P('Q11578315', 'Gravure modeling/swimwear', 'JP gravure idol; ' + GR + '; DOB matches Wikidata')
R('Q11579321', 'AGE_PARTIAL', 'JP model (Seven-Promotion); the lead gives no birth date at all, so the Wikidata value is unconfirmed on the page', dob='UNKNOWN')
P('Q11580778', 'Modeling/music', 'JP fashion model, singer and topliner (Hiroshima; legal name Yuki Mizutani per lead); DOB matches Wikidata')
R('Q11581929', 'scope-ambiguous', 'JP former gravure idol and former tarento (Tokyo); ' + FM)
P('Q11583031', 'Gravure modeling/swimwear', 'JP gravure idol active under the mononym 真奈 Mana (legal name undisclosed per lead); ' + GR + '; DOB matches Wikidata', name='Mana (真奈, model)')
P('Q11584392', 'Modeling', 'JP fashion model, nickname Mikko; DOB matches Wikidata')
R('Q11584646', 'scope-ambiguous', 'JP former fashion model active under the mononym 知華 Tomoka (Setagaya, Tokyo); ' + FM, name='Tomoka (知華)')
P('Q11585071', 'Modeling', 'JP fashion model (Ibaraki); DOB matches Wikidata')
P('Q11585347', 'Modeling/acting', 'JP fashion model and actress (Tokyo; Be Natural); DOB matches Wikidata')
P('Q11589440', 'Modeling/motorsport/TV', 'JP racing driver, fashion model and tarento (Kokubunji, Tokyo); DOB matches Wikidata')
P('Q11589512', 'Modeling', 'JP fashion model (Tokyo; ECP); DOB matches Wikidata')
# ---- batch 4 (jawiki_b4.json)
P('Q11591249', 'Modeling/business', 'JP businesswoman (beauty-salon chain owner, founder and CEO of Hollywood Brow Lift) who worked as a tarento and model before retiring from entertainment per lead; DOB matches Wikidata')
P('Q11594248', 'Modeling/TV', 'JP model and tarento (formerly DIVINE); DOB matches Wikidata')
R('Q11594855', 'scope-ambiguous', 'JP freelance announcer, formerly TV Tokyo; ' + SA)
R('Q11596529', 'scope-ambiguous', 'JP former idol and former tarento (former child actress); ' + SA)
R('Q11598105', 'scope-ambiguous', 'JP singer and tarento (Sun Music; Kanagawa); ' + SA)
R('Q11598742', 'scope-ambiguous', 'JP actress (Kobe); Wikidata English label Rinana, lead name 卯内里奈 Rina Unai; ' + SA, name='Rina Unai (卯内里奈)')
P('Q11599065', 'Modeling/motorsport', 'JP drag racer, former actress and former fashion model, now active under the mononym 春花 Haruka (former stage name 竹富聖花; name alias noted); DOB matches Wikidata')
R('Q11602555', 'scope-ambiguous', 'JP former actress, tarento and fashion model (formerly LesPros Entertainment); ' + FM)
P('Q11603856', 'Modeling/acting', 'JP model and actress (Tokyo); DOB matches Wikidata')
P('Q11605962', 'Modeling', 'JP fashion model; DOB matches Wikidata')
P('Q11606133', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata')
P('Q11606239', 'Modeling', 'JP fashion model (Aichi); DOB matches Wikidata')
P('Q11607835', 'Modeling/acting/TV', 'JP actress, tarento and fashion model; DOB matches Wikidata')
P('Q11608119', 'Modeling/acting', 'JP actress and model (Hirakata, Osaka); DOB matches Wikidata')
P('Q11608349', 'Modeling/radio', 'JP model and radio personality (Minato, Tokyo); DOB matches Wikidata')
P('Q11608774', 'Modeling', 'JP fashion model active under the mononym 美優 Miyu (Tokyo); DOB matches Wikidata', name='Miyu (美優, model)')
R('Q11609105', 'DOB_CONFLICT', 'JP tarento and former gravure idol (Iizuka, Fukuoka; former stage name 美月あかり); the ja-wiki lead gives a birth year two years earlier than the Wikidata value (same month and day) - trusted sources conflict, no value chosen; both values are adult', dob='UNKNOWN')
P('Q11612159', 'Modeling', 'JP fashion model (Tokyo); DOB matches Wikidata')
P('Q11613623', 'Modeling/photography/TV', 'JP fashion model, photographer and tarento (naturalised, Taiwanese-born per lead); DOB matches Wikidata')
P('Q11614041', 'Gravure modeling/swimwear/acting', 'JP actress and gravure idol, former fashion model (Oscar Promotion); ' + GR + '; DOB matches Wikidata')
# ---- batch 5 (jawiki_b5.json)
R('Q11614874', 'scope-ambiguous', 'JP former boat racer and tarento (Shimonoseki); ' + SA)
P('Q11616852', 'Modeling', 'JP fashion model (Aomori); DOB matches Wikidata')
P('Q11618083', 'Modeling/acting', 'JP actress and fashion model (Tokyo); DOB matches Wikidata')
P('Q11618382', 'Modeling/acting/music', 'JP actress, idol and fashion model, former SUPER GiRLS member; DOB matches Wikidata')
P('Q11619198', 'Modeling', 'JP fashion model (Idea); DOB matches Wikidata')
P('Q11619260', 'Modeling/acting', 'JP actress and fashion model (Saitama); DOB matches Wikidata')
P('Q11619956', 'Modeling/acting/TV', 'JP model, actress and tarento (Tokyo; Horipro-affiliated agency Booth); DOB matches Wikidata')
R('Q11619974', 'scope-ambiguous', 'JP underground idol; ' + SA)
P('Q11620080', 'Modeling/writing', 'JP essayist and model; lead gives the full name 矢部華恵 Hanae Yabe, article title and Wikidata label are the mononym 華恵 Hanae (name alias noted); DOB matches Wikidata', name='Hanae Yabe')
P('Q11621922', 'Modeling', 'JP fashion model (Aichi); DOB matches Wikidata')
P('Q11622216', 'Modeling/TV/acting/pageant', 'JP fashion model, tarento and actress, Miss Universe Japan Saitama representative (Tokorozawa); DOB matches Wikidata')
P('Q11624159', 'Modeling', 'JP fashion model (Fukuoka); DOB matches Wikidata')
R('Q11624414', 'AGE_PARTIAL', 'JP fashion model and actress (Kagawa); the lead gives no birth date at all, so the Wikidata value is unconfirmed on the page', dob='UNKNOWN')
P('Q11624439', 'Modeling/acting/TV', 'JP actress, tarento and fashion model (Tokyo); DOB matches Wikidata')
P('Q11624827', 'Modeling/TV', 'JP fashion model and tarento (Tokyo); DOB matches Wikidata')
P('Q11625277', 'Modeling/music/TV/acting', 'JP fashion model, singer, tarento and actress, former SOUL TIGER vocalist and Fudanjuku member; DOB matches Wikidata')
P('Q11627886', 'Modeling', 'JP fashion model (Nagoya); DOB matches Wikidata')
P('Q11628017', 'Gravure modeling/swimwear/acting/TV', 'JP actress, gravure idol and tarento (Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11628956', 'Gravure modeling/swimwear/editorial', 'JP magazine editor and former gravure idol (Okayama); ' + GR + '; DOB matches Wikidata')
P('Q11629251', 'Modeling/TV', 'JP fashion model and tarento (Gifu; formerly Avex Management); DOB matches Wikidata')
# ---- batch 6 (jawiki_b6.json)
P('Q11629279', 'Gravure modeling/swimwear/TV', 'JP tarento, former model and former gravure idol; ' + GR + '; DOB matches Wikidata')
P('Q11630174', 'Modeling/TV', 'JP fashion model, tarento and reporter (Osaka); DOB matches Wikidata')
P('Q11632646', 'Modeling/acting/music', 'JP fashion model, actress and singer-songwriter (Tokyo); DOB matches Wikidata')
P('Q11632740', 'Modeling', 'JP fashion model (Hasuda, Saitama); DOB matches Wikidata')
R('Q11632741', 'scope-ambiguous', 'JP tarento (Osaka; legal name Sachiyo Kuniyoshi per lead); ' + SA)
P('Q11633974', 'Modeling/acting', 'JP actress and model; DOB matches Wikidata')
P('Q11635982', 'Modeling', 'JP fashion model (TENCARAT Plume); DOB matches Wikidata')
P('Q11636473', 'Modeling', 'JP gyaru fashion model; DOB matches Wikidata')
P('Q11638147', 'Modeling/acting/art', 'JP fashion model, actress and artist (Kyoto); DOB matches Wikidata')
R('Q11639000', 'scope-ambiguous', 'JP actress and tarento (Niihama, Ehime); ' + SA)
P('Q11642312', 'Modeling/acting', 'JP fashion model and actor (Ibaraki); DOB matches Wikidata')
P('Q11642422', 'Gravure modeling/swimwear/race queen/TV', 'JP tarento and gravure idol, former race queen (Hokkaido); ' + GR + '; DOB matches Wikidata')
P('Q11644608', 'Modeling', 'JP fashion model active under the mononym 里海 Satoumi (Tokyo); DOB matches Wikidata', name='Satoumi (里海, model)')
P('Q11644674', 'Modeling/yoga', 'JP fashion model and yoga instructor (Tokyo); DOB matches Wikidata')
P('Q11645258', 'Modeling/TV', 'JP model-tarento (otaku senryu personality); DOB matches Wikidata')
P('Q11645416', 'Modeling/TV/acting', 'JP fashion model, tarento and actress (Tokyo); DOB matches Wikidata')
P('Q11645988', 'Gravure modeling/swimwear/TV', 'JP tarento and former gravure idol (Saitama); ' + GR + '; DOB matches Wikidata')
R('Q11646286', 'scope-ambiguous', 'JP tarento, actress, reporter, narrator and instructor; ' + SA)
P('Q11646397', 'Modeling/acting', 'JP model and actress (Gunma); DOB matches Wikidata')
P('Q11648411', 'Modeling/TV', 'JP fashion model and tarento (A-Light); DOB matches Wikidata')

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
    if q in QUOTE:
        quote = QUOTE[q]
    d = dob or r['dob']
    ev = f'ja-wiki lead: 「{quote}」 - {note}'
    if verdict == 'REJECT':
        ev = note
    assert '|' not in ev, q
    assert not re.search(r'(?:born|Born|DOB|date of birth|birthday)[^\d]{0,45}?\d', ev), ('DATE_RE risk', q, ev)
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
                        ja=r.get('ja', ''), kana=r.get('kana', ''), file='model_ja3_chunk*.txt'))

Path(ROOT / 'data/research/verification_s32_log.tsv').write_text('\n'.join(lines) + '\n')
json.dump({'model': buckets}, open(ROOT / 'data/research/s32_verify_buckets.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(v[0] for v in V.values()))
print(Counter(v[1] for v in V.values() if v[0] == 'REVIEW'))
