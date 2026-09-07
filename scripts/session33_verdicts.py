#!/usr/bin/env python3
"""Session 33 — verdict table for the Japanese-Wikipedia slice of the Wikidata model pool
(female, occupation model / fashion model / personal trainer / bodybuilder / fitness model,
born 1985-2008, Instagram or TikTok handle, ja-wiki article, NO en-wiki article; page 4,
ORDER BY ?p LIMIT 150 OFFSET 450 -> 150 unique people -> 139 new after Q-ID/name/handle dedup).

Input : data/research/s33_raw/model_ja4_checked.json  (rows + ja-wiki lead extracts + labels)
Output: data/research/verification_s33_log.tsv       (qid|name|dob|verdict|category-or-flags|evidence|url)
        data/research/s33_verify_buckets.json        (handles for scripts/session33_apply.py)

Verdict rules (Session 27-32 precedent, applied to ja-wiki leads):
  PROMOTE        lead states the full birth date (YYYY年M月D日) matching Wikidata AND documents modeling /
                 gravure (swimsuit magazine) modeling / race-queen / fitness-model / influencer / creator
                 activity (a former modeling career counts when the lead documents a current public
                 career); adult on 2026-09-06.
  REVIEW         scope-ambiguous (idol / singer / actress / tarento / announcer / entrepreneur only, or
                 every listed occupation former with no current activity), AGE_PARTIAL (no full birth
                 date on the page), DOB_CONFLICT (page date differs from Wikidata), WIKI_REDIRECT
                 (title redirects to a group / show article).
  MINOR_UNDERAGE under 18 on 2026-09-06 -> review queue without handles, re-evaluate at 18.
  REJECT         deceased or not an individual person.
Nothing is invented: names come from the Wikidata labels / ja-wiki lead readings (Hepburn romanisation
of the documented kana when Wikidata has no English label), handles from Wikidata P2003 / P7085,
dates from the ja-wiki lead cross-checked against Wikidata P569.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_catalog import find_years  # noqa: E402  (same year-parser the validator applies)

rows = json.load(open(ROOT / 'data/research/s33_raw/model_ja4_checked.json'))
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


def M(q, note, name=None):
    V[q] = ('MINOR_UNDERAGE', 'MINOR_UNDERAGE', note, name, None, None, None, None)


def X(q, note, name=None):
    V[q] = ('REJECT', 'excluded', note, name, None, None, None, None)


SA = 'no modeling / creator activity documented in the lead; adult (DOB matches Wikidata)'
GR = 'gravure idol = swimsuit / magazine model (objective Japanese occupational category)'
FM = ('all listed occupations are former and the lead documents no current public activity, so current '
      'creator status and handle currency cannot be confirmed from the lead; adult (DOB matches Wikidata)')
NOEN = 'no English Wikidata label - display name is the Hepburn romanisation of the lead reading'

# ---- batch 0 (jawiki_b0.json)
R('Q11651010', 'scope-ambiguous', 'JP actress (Tokyo; Enchante); ' + SA)
P('Q11651826', 'Modeling/acting', 'JP fashion model, actor and voice actress (Hokkaido; formerly Stardust); DOB matches Wikidata')
P('Q11653770', 'Modeling', 'JP fashion model (Mie); ja-wiki title disambiguated as 長谷川唯 (モデル); DOB matches Wikidata', name='Yui Hasegawa (model)')
R('Q11654103', 'scope-ambiguous', 'JP voice actress and tarento, former Idoling!!! member; ' + SA)
R('Q11656168', 'scope-ambiguous', 'JP former teen-magazine model (Nico Puchi, Pichi Lemon exclusive) whose page records a 2016 retirement announcement; page has no prose lead, the infobox birth fields match Wikidata; ' + FM,
  quote='(no prose lead) infobox 女性モデル: 生年 1998 / 生月 3 / 生日 27; デビュー 2008年『ニコ☆プチ』冬号; 活動備考 元『ピチレモン』専属モデル; 略歴: 2016年12月20日、本人のTwitter内で芸能界引退を発表。')
P('Q11657915', 'Modeling/acting/TV', 'JP fashion model, actress and tarento (Tokyo; Sign); DOB matches Wikidata')
P('Q11657934', 'Modeling/acting', 'JP fashion model and actress (Chiba; TENCARAT); DOB matches Wikidata')
X('Q11658933', 'deceased: ja-wiki lead records death on 2020-08-28 (階戸瑠李, actress / model / former gravure idol) - not eligible for a living-creator catalog')
P('Q11659518', 'Modeling', 'JP fashion model (Hyogo); lead gives legal name 難波沙樹 for the stage name 難波サキ; DOB matches Wikidata')
R('Q11661297', 'scope-ambiguous', 'JP former model, former actress, former tarento (Hokkaido; formerly Platinum Production); ' + FM)
P('Q11661846', 'Modeling/TV', 'JP fashion model and tarento (Stardust Promotion); DOB matches Wikidata')
P('Q11667778', 'Modeling/TV/acting', 'JP fashion model (non-no exclusive), tarento and actress active under the mononym 香音 Kanon (legal name 野々村香音 per lead); DOB matches Wikidata', name='Kanon (香音, model)')
P('Q11669521', 'Gravure modeling/swimwear/acting', 'JP gravure idol and actress (Tokyo); ' + GR + '; DOB matches Wikidata')
P('Q11669837', 'Gravure modeling/swimwear/TV', 'JP gravure idol and tarento (Osaka; Name Management); ' + GR + '; DOB matches Wikidata')
P('Q11670083', 'Modeling/acting/TV/music', 'JP actress, tarento and model, LOVEACE member (Shizuoka); lead name 高嶋莉子 Riko Takashima, article title / Wikidata label 高木李湖 Riko Takagi (name alias noted); DOB matches Wikidata', name='Riko Takashima (formerly Riko Takagi)')
P('Q11670272', 'Modeling', 'JP casino dealer and fashion model (Risera); former stage names 高松リナ / 高松チェルシーリナ (name alias noted); DOB matches Wikidata')
R('Q11670852', 'scope-ambiguous', 'JP tarento and radio DJ (Stardust Promotion); ' + SA)
P('Q11671065', 'Modeling/TV', 'JP model and tarento (Yamagata; formerly Excel Human Agency); DOB matches Wikidata')
P('Q11671443', 'Modeling/acting', 'JP fashion model and actress (Niigata; Reneo Management); DOB matches Wikidata')
P('Q11671466', 'Modeling/TV/music', 'JP fashion model, tarento and singer (Saitama); DOB matches Wikidata')
# ---- batch 1 (jawiki_b1.json)
P('Q11671520', 'Modeling/acting', 'JP actress and fashion model (Hiroshima; Idea); DOB matches Wikidata')
R('Q11672806', 'scope-ambiguous', 'JP multi-tarento, former Baby Raids JAPAN member (Mie); ' + SA)
P('Q11676238', 'Modeling/TV', 'JP reader model and tarento (Tokyo; Hosei University graduate); DOB matches Wikidata')
P('Q11677225', 'Modeling/TV/acting', 'JP fashion model, tarento and actress (Fukui; HONEST); DOB matches Wikidata')
P('Q11677444', 'Gravure modeling/swimwear/acting', 'JP actress, model and former gravure idol (Kanagawa; One Eight Promotion); ' + GR + '; DOB matches Wikidata')
P('Q11677632', 'Fitness model/TV', 'fitness model, tarento and backline stylist described by the lead as Japanese; Wikidata records citizenship of the Kingdom of the Netherlands; DOB matches Wikidata')
P('Q11677645', 'Modeling/acting/TV', 'JP actress, model and tarento active under the mononym 麻衣愛 Maia (Tokyo; Japan Music Entertainment); DOB matches Wikidata', name='Maia (麻衣愛, model)')
P('Q11678327', 'Modeling/acting', 'JP fashion model (non-no exclusive after the 37th non-no model grand prix) and actress; lead name 永野桃子 Momoko Nagano, Wikidata label / former stage name 黒木桃子 Momoko Kuroki (name alias noted); DOB matches Wikidata', name='Momoko Nagano (formerly Momoko Kuroki)')
P('Q11678517', 'Modeling', 'JP fashion model (Hokkaido); DOB matches Wikidata')
R('Q11678612', 'scope-ambiguous', 'JP tarento, CEO of Antares Inc. and PD AeroSpace planning liaison; ' + SA)
P('Q11678637', 'Modeling/TV/acting', 'JP fashion model, tarento and actress (Saitama; Booth, Horipro group); DOB matches Wikidata')
P('Q11678657', 'Modeling', 'JP fashion model (Hyogo); DOB matches Wikidata')
P('Q116890349', 'Modeling', 'JP model (Hyogo); DOB matches Wikidata')
P('Q116936128', 'Modeling/TV/acting/creator', 'JP model, tarento, actress, YouTuber and TikToker (Kanagawa; MR8); legal name 水戸由菜 per lead; DOB matches Wikidata')
P('Q116936183', 'Gravure modeling/swimwear/acting/TV', 'JP gravure idol, actress and tarento (Tokyo; seju); ' + GR + '; DOB matches Wikidata')
P('Q116936412', 'Modeling/acting/creator', 'JP model, actress, YouTuber and TikToker (seju); DOB matches Wikidata')
P('Q116936466', 'Modeling/acting/music', 'JP idol, actress and model (nickname Kotorin); DOB matches Wikidata')
P('Q116937343', 'Modeling/TV/creator', 'JP fashion model, tarento and TikToker active under the mononym うたな Utana (Saitama); DOB matches Wikidata', name='Utana (うたな, model)')
P('Q117090150', 'Modeling/music/acting', 'JP idol (Shiritsu Ebisu Chugaku member), singer, model and actress (Kanagawa); adult - turned nineteen on 2026-09-05; DOB matches Wikidata')
P('Q118338408', 'Modeling/acting/creator', 'JP actress, model and streamer (Shizuoka; freelance); DOB matches Wikidata')
P('Q118338437', 'Modeling/acting', 'JP actress and model (Hiroshima; Cent Force); DOB matches Wikidata')
# ---- batch 2 (jawiki_b2.json)
P('Q118338438', 'Modeling/acting/pageant', 'JP model and actress, Miss Nippon 2021 grand prix winner (Osaka; Kwansei Gakuin University graduate); DOB matches Wikidata')
R('Q118338485', 'scope-ambiguous', 'JP actress (Horipro Digital Entertainment); the lead itself gives 1 January as the birth date; ' + SA)
P('Q118611481', 'Modeling/acting', 'JP model and actress (Hyogo; 4C LLC); DOB matches Wikidata')
P('Q118696192', 'Modeling/race queen', 'JP model and race queen (Aichi; nickname Akarin); ' + NOEN + '; country of citizenship not recorded in Wikidata; DOB matches Wikidata', name='Akari Miyamoto')
R('Q118696640', 'scope-ambiguous', 'JP idol and tarento, FRUITS ZIPPER member (Kanagawa); ' + SA)
R('Q1189839', 'scope-ambiguous', 'JP businesswoman, tarento, novelist and producer, former AKB48 member; ' + SA)
P('Q119338691', 'Modeling', 'JP fashion model (Bon Image); DOB matches Wikidata')
P('Q119343112', 'Modeling/TV', 'JP fashion model and tarento (Osaka; Churros); DOB matches Wikidata')
R('Q119921265', 'AGE_PARTIAL', 'JP fashion model (N.F.B); the lead gives no birth date at all, so the Wikidata date cannot be confirmed on the page', dob='UNKNOWN')
P('Q121354543', 'Modeling/music/TV', 'JP idol (Magical Punchline leader), tarento and model; ' + NOEN + '; DOB matches Wikidata', name='Haruka Yoshizawa')
P('Q121355260', 'Modeling/acting', 'JP fashion model and actress, former Smile Kaizokudan member (Tokyo; Appoint Inc.); DOB matches Wikidata')
P('Q122354454', 'Modeling/music/TV', 'JP tarento, model and idol, CUTIE STREET member (Nagoya); DOB matches Wikidata')
P('Q123405030', 'Modeling/acting', 'JP actress and model, also performs as 白雪リンゴ in the group 純文学少女歌劇団; ' + NOEN + '; DOB matches Wikidata', name='Konatsu Wada')
P('Q123405208', 'Modeling/influencer/acting/TV', 'JP model, influencer, actress and tarento (Tokyo; freelance); ' + NOEN + '; country of citizenship not recorded in Wikidata; DOB matches Wikidata', name='Yukina Matsuoka')
P('Q123405212', 'Creator/TV', 'JP tarento and YouTuber, member of the bis-magazine influencer unit bis LEADERS, MISS CIRCLE CONTEST 2021 grand prix; DOB matches Wikidata')
P('Q123405456', 'Modeling/acting/TV/music', 'JP actress, tarento, singer and model (Saitama; OOO Entertainment); DOB matches Wikidata')
P('Q123405597', 'Modeling/music', 'JP idol and model, FRUITS ZIPPER member (Asobisystem); DOB matches Wikidata')
P('Q123405796', 'Modeling/business', 'JP model (JJ magazine, advertising, TV commercials) and businesswoman, CEO of CELFISH Inc.; ' + NOEN + '; DOB matches Wikidata', name='Yuna Kawaguchi')
P('Q123406187', 'Modeling/TV/acting', 'JP model, tarento and actress (Aichi; Alice in Wonderland); DOB matches Wikidata')
# ---- batch 3 (jawiki_b3.json)
P('Q123415080', 'Modeling/creator/influencer', 'Netherlands-born, Japan-based YouTuber, influencer and model (legal name Elizabeth Freya per lead); country of citizenship not recorded in Wikidata; DOB matches Wikidata')
P('Q123562807', 'Modeling/music/acting', 'JP artist, actress, fashion model and singer, former Wednesday Campanella vocalist; DOB matches Wikidata', name='Komuai (コムアイ)')
P('Q124097059', 'Modeling/creator', 'JP model and YouTuber (Fukuoka; Beaile); DOB matches Wikidata')
P('Q124097461', 'Modeling', 'JP model and round girl active as RISA BOOO; DOB matches Wikidata', name='RISA BOOO (りさぶー)')
P('Q124363992', 'Modeling/acting', 'IT actress and model (Wikidata citizenship Italy); DOB matches Wikidata')
P('Q124479796', 'Modeling/music/TV', 'JP idol, model, tarento and voice actress, FRUITS ZIPPER member (Asobisystem; legal name not public); DOB matches Wikidata')
P('Q124480052', 'Modeling/acting', 'JP actress and model (Akita; A-Plus); DOB matches Wikidata')
P('Q125080582', 'Gravure modeling/swimwear/acting', 'JP actress, gravure model and former race queen (Fukui; Eyes); ' + GR + '; DOB matches Wikidata')
R('Q125926338', 'WIKI_REDIRECT+AGE_PARTIAL', 'JP model / PureGi member per Wikidata sitelink; the ja-wiki title redirects to the Popteen girls-unit project article 7+ME Link, so there is no standalone biography and the Wikidata birth date is unconfirmed on the page',
  name='An Yamamoto (山本杏, model)', quote='ja-wiki title 山本杏 (モデル) REDIRECTs to 7+ME Link#PureGi (Popteen girls-unit project article); no standalone biography')
R('Q12594739', 'scope-ambiguous', 'JP choreographer, former PASSPO☆ member (NRC Production); ' + SA)
R('Q126874946', 'scope-ambiguous', 'JP actress and dancer (Matsue; MKz square); ' + SA)
P('Q126875538', 'Modeling/acting', 'JP actress and model (Kagoshima; formerly O-Pure); DOB matches Wikidata')
P('Q128838991', 'Modeling/music', 'JP idol and model, former NMB48 member (Oscar Promotion); ' + NOEN + '; DOB matches Wikidata', name='Mikana Yamamoto')
P('Q128840654', 'Modeling/TV', 'JP tarento and fashion model (Tokyo; Platinum Production, then Bon Image); DOB matches Wikidata')
P('Q128840734', 'Modeling/music', 'JP idol and model, Shinsekai Hero member and former Cerisier WEST member (Nara); ' + NOEN + '; DOB matches Wikidata', name='Suzuna Amemiya')
P('Q129007170', 'Modeling/TV/acting', 'JP tarento, model and actress (Aichi; Pearl); DOB matches Wikidata')
P('Q130220488', 'Modeling/TV/acting', 'JP model, tarento and actress (Mie; Rhythmedia); adult - turned eighteen on 2026-03-16; DOB matches Wikidata')
P('Q130220489', 'Modeling/TV', 'JP tarento and Popteen exclusive model (seju / GROVE); adult - nineteen on the check date; DOB matches Wikidata')
P('Q130260977', 'Modeling/music/creator', 'JP idol, fashion model and YouTuber, CUTIE STREET member; DOB matches Wikidata')
P('Q130336927', 'Modeling/race queen', 'JP model and race queen (Fukuoka; nickname Erenan); DOB matches Wikidata')
P('Q130384632', 'Modeling/music/TV', 'JP idol, model and tarento, CANDY TUNE and KAWAII CARAVAN Cho-Kyushu member; DOB matches Wikidata')
# ---- batch 4 (jawiki_b4.json)
P('Q130725990', 'Modeling', 'JP model (Saitama); DOB matches Wikidata')
P('Q130726029', 'Modeling/acting/dance', 'JP butoh dancer, actress, stage director and model active as カナキティ Kana Kitty (Tokyo; KM Cinema Kikaku); DOB matches Wikidata', name='Kana Kitty (カナキティ)')
P('Q130726528', 'Modeling/TV', 'JP tarento, model, reporter and radio personality (Gifu; Giotto); DOB matches Wikidata')
P('Q130726680', 'Modeling', 'JP model (Accessi Beauty Management); DOB matches Wikidata')
P('Q130728636', 'Modeling/acting', 'JP actress and fashion model (Tokyo; Oscar Promotion); DOB matches Wikidata')
P('Q131010510', 'Modeling/TV', 'JP tarento, model, reporter and radio personality (Toyohashi); lead name 城所杏由音; DOB matches Wikidata')
P('Q131148501', 'Modeling/race queen/gravure/swimwear/TV/acting', 'JP tarento and actress who the lead documents as a former race queen and gravure idol (retired from both by November 2024); current TV / acting career documented; ' + GR + '; DOB matches Wikidata')
P('Q131193501', 'Modeling/acting', 'JP actress and model (Osaka; Sticker); DOB matches Wikidata')
P('Q132431756', 'Modeling/TV', 'JP fashion model and tarento (Miyagi; Asia Promotion); adult - turned eighteen on 2026-02-19; DOB matches Wikidata')
P('Q132431838', 'Modeling/acting/TV', 'JP actress, tarento, model and round girl (Yamagata); DOB matches Wikidata')
P('Q132432016', 'Modeling/acting', 'JP model and actor (Michelle Entertainment); DOB matches Wikidata')
P('Q132432044', 'Modeling/music/TV', 'JP idol, model and tarento, captain of the local idol group Hokuriku Idol-bu; DOB matches Wikidata')
P('Q132432544', 'Modeling/influencer', 'JP model and influencer (Hokkaido; OOO Entertainment); DOB matches Wikidata')
P('Q132461974', 'Modeling/TV', 'JP model, tarento and former idol; ja-wiki title disambiguated by birth year; DOB matches Wikidata', name='Nagisa Sano (佐野なぎさ, model)')
M('Q134507843', 'JP tarento, actress and model (Tokyo; Contents Three); ja-wiki lead birth date 2008年10月10日 agrees with Wikidata - age 17 on 2026-09-06; not eligible until 2026-10-10 (no handles recorded)')
P('Q134508515', 'Modeling/TV', 'JP model, wadaiko (Japanese drum) performer and tarento; ja-wiki title disambiguated as 富田安紀子 (和太鼓パフォーマー); DOB matches Wikidata')
P('Q135689525', 'Modeling', 'JP fashion model (Kanagawa); adult - nineteen on the check date; DOB matches Wikidata')
R('Q137525397', 'WIKI_REDIRECT+scope-ambiguous', 'the ja-wiki title redirects to the comedy-duo article 紅しょうが (Yoshimoto Kogyo), so there is no standalone biography, no birth date on the page and no modeling activity documented',
  quote='ja-wiki title 稲田美紀 REDIRECTs to 紅しょうが (お笑い)#メンバー (comedy-duo article); no standalone biography')
P('Q137798657', 'Modeling/TV/acting', 'JP fashion model, tarento and actor (Kanagawa; Stardust Promotion); DOB matches Wikidata')
P('Q138606560', 'Modeling/TV/acting', 'JP weather caster (Weathernews), actress and model; DOB matches Wikidata')
# ---- batch 5 (jawiki_b5.json)
P('Q15618700', 'Modeling/acting', 'JP actress and fashion model (Takasaki; Ken-On); DOB matches Wikidata', name='Karen Otomo')
P('Q16263582', 'Modeling/acting/TV', 'JP fashion model, actor and tarento (Asobi Production); DOB matches Wikidata')
P('Q16263583', 'Modeling/TV', 'JP fashion model and tarento (Hyogo; legal name 青山亜美 per lead); DOB matches Wikidata')
R('Q16263610', 'DOB_CONFLICT', 'JP model and former race queen (Yokohama); the ja-wiki lead states 1986年9月22日 while Wikidata records 1988-09-22 - same month and day, different year; no value chosen (adult under either value)', dob='UNKNOWN')
P('Q16263806', 'Race queen/TV', 'JP tarento and race queen (Tatebayashi; Can Promotion); DOB matches Wikidata')
P('Q16263846', 'Modeling/acting/TV/race queen', 'JP model, actress, tarento and race queen (Aichi; Three Rise); DOB matches Wikidata')
P('Q16264211', 'Gravure modeling/swimwear/music/TV', 'JP idol, tarento, model and gravure idol, former #2i2 member (Tokyo); the Wikidata TikTok value is an opaque account identifier rather than a handle and was not recorded; ' + GR + '; DOB matches Wikidata')
P('Q16264327', 'Modeling/acting', 'JP actress and fashion model (Osaka; Avex Management); lead spelling 井元まほ, Wikidata label 井元麻帆; DOB matches Wikidata')
P('Q16264372', 'Modeling', 'JP model (nickname Akkochi); ja-wiki title disambiguated as 岩田明子 (モデル); DOB matches Wikidata', name='Akiko Iwata (model)')
R('Q16264601', 'scope-ambiguous', 'JP tarento and actress (Mito; based in Kobe); ' + SA)
P('Q16264719', 'Modeling/TV', 'JP fashion model, tarento and MC of Japanese-Swiss parentage (Tokyo); lead gives the romanisation Amy Ota, Wikidata label Eimi Ōta (name alias noted); DOB matches Wikidata', name='Amy Ota (太田エイミー)')
P('Q16264932', 'Modeling/acting/TV', 'JP tarento, actress and model (formerly Mammoth Pro until January 2018); DOB matches Wikidata')
P('Q16265004', 'Modeling/acting', 'JP fashion model and actor, former Le Lien member (Tokyo); DOB matches Wikidata')
P('Q16265095', 'Modeling/acting', 'JP model and actress (Osaka; formerly Booze, Horipro group); DOB matches Wikidata')
P('Q16265129', 'Gravure modeling/swimwear/acting', 'JP gravure idol, model and actress, former G☆Girls member; ' + GR + '; DOB matches Wikidata')
R('Q16265200', 'scope-ambiguous', 'the ja-wiki lead documents her only as a photographer (片岡三果, Hokkaido) although Wikidata lists a model occupation; ' + SA)
P('Q16769676', 'Modeling/acting', 'JP model and actress (Audick Holdings); lead name 夢野いづみ Izumi Yumeno, former stage name and Wikidata label IZUMI (name alias noted); DOB matches Wikidata', name='Izumi Yumeno (夢野いづみ)')
P('Q16770295', 'Modeling/acting/photography', 'JP actress, model and photographer (Takasaki; Ricoron / BRUTUS); DOB matches Wikidata')
P('Q17128951', 'Gravure modeling/swimwear/acting/TV', 'JP actress, fashion model, gravure model and tarento (Tochigi; Musashino University graduate); ' + GR + '; DOB matches Wikidata')
P('Q17129638', 'Modeling/fashion design/creator', 'JP Kawaii Ambassador (Ministry of Foreign Affairs pop-culture envoy, Harajuku fashion), fashion designer, producer, model (KERA, Gothic & Lolita Bible) and voice actress; DOB matches Wikidata', name='Yu Kimura')
# ---- batch 6 (jawiki_b6.json)
P('Q17157992', 'Modeling/music', 'JP idol and model, former Hachihachi Kita Girls / Mirai Skirt leader now active solo as ミライスカート⁺; DOB matches Wikidata')
P('Q17158261', 'Modeling/TV', 'JP fashion model and tarento (Tokyo; Aoyama Gakuin University graduate); DOB matches Wikidata')
P('Q17158392', 'Gravure modeling/swimwear/TV', 'JP model, gravure idol and multi-tarento (Kanagawa); ' + GR + '; DOB matches Wikidata')
P('Q17158444', 'Gravure modeling/swimwear/music', 'JP idol and gravure idol (Hyogo; Bambina); ' + GR + '; DOB matches Wikidata', name='Asami Kondo')
P('Q17158503', 'Creator/music', 'JP musician (singer, guitarist) and video creator (legal name Alina Diana Saito per lead); DOB matches Wikidata', name='Alina Saito')
R('Q17158593', 'scope-ambiguous', 'JP actress (Fukuoka; legal name identical); a different woman from review-queue candidate Saori Seto R-2026-433 (瀬戸サオリ), hence the hiragana disambiguator; ' + SA, name='Saori Seto (瀬戸さおり)')
P('Q17158630', 'Modeling', 'JP fashion model (Nara; ENCANTO); ja-wiki DOB 18 Aug 1989 preferred over Wikidata 1989-01-01 (year-precision)', dob='1989-08-18')
R('Q17158665', 'DOB_CONFLICT', 'JP fashion model, tarento, actress and former gravure idol (Tokyo; freelance); the ja-wiki lead states 1993年9月10日 while Wikidata records 1991-09-10 - same month and day, different year; no value chosen (adult under either value)', dob='UNKNOWN')
R('Q17158908', 'scope-ambiguous', 'JP former race queen, former model, former tarento (Gifu); ' + FM)
R('Q17158965', 'DOB_CONFLICT+scope-ambiguous', 'JP former fashion model (Kanagawa; formerly J BOX) with no current activity documented; the ja-wiki lead states 2003年12月31日 while Wikidata records 1997-02-16; no value chosen (adult under either value)', name='Aoi Sato (佐藤葵, model)', dob='UNKNOWN')
P('Q17159728', 'Gravure modeling/swimwear/TV/acting', 'JP model, gravure idol, tarento and actress (Kyoto-born, Osaka-raised; Incubation); the Wikidata kana value does not match the lead reading わだ なな (data-quality note, kana not used); ' + GR + '; DOB matches Wikidata')
P('Q17159745', 'Modeling/acting', 'JP actress, model and former child actress (Tokyo; Top Coat); DOB matches Wikidata')
P('Q17159914', 'Modeling', 'JP fashion model, former Happiness / E-girls member (Osaka); DOB matches Wikidata')
R('Q17160163', 'scope-ambiguous', 'JP former model (legal name identical); ' + FM)
R('Q17160166', 'AGE_PARTIAL+scope-ambiguous', 'the ja-wiki page has no lead sentence and no birth date (only a 1992-births category) and documents an armour-art company founder / GIA diamond graduate, not modeling; Wikidata date unconfirmed', dob='UNKNOWN',
  quote='(no prose lead, no birth date; page carries Category:1992年生) 略歴: 老舗人形店に生まれ…GIAではDiamond鑑定士（GD）のディプロマを取得…伝統的な甲冑をアートとして世界に発信している。')
P('Q17160509', 'Modeling', 'JP fashion model (Chiba; Oscar Promotion); DOB matches Wikidata', name='Fuka Takashima')
P('Q17160526', 'Modeling/TV', 'JP fashion model and tarento (Ebetsu; maxim, formerly LesPros); DOB matches Wikidata')
R('Q17160781', 'scope-ambiguous', 'JP former fashion model (former stage name 立花舞, legal name 山内舞 per lead); ' + FM)

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
    if verdict == 'PROMOTE':
        # the validator parses birth years out of the evidence text: anything it finds must equal the DOB year
        yrs = find_years(ev)
        assert yrs <= {int(d[:4])}, ('DATE_RE risk', q, yrs, ev)
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
                        ja=r.get('ja', ''), kana=r.get('kana', ''), file='model_ja4_chunk*.txt'))

Path(ROOT / 'data/research/verification_s33_log.tsv').write_text('\n'.join(lines) + '\n')
json.dump({'model': buckets}, open(ROOT / 'data/research/s33_verify_buckets.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter  # noqa: E402
print(Counter(v[0] for v in V.values()))
print(Counter(v[1] for v in V.values() if v[0] == 'REVIEW'))
