#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp3/prompt_epit.py -- F27_FP3_BRIEF.md P0: fp3/prompt_v4.md epitese.
Az fp2/prompt_v3.md szo szerinti masolata + a v4 kiegeszito szabalyok + G26 peldapar.
A peldapar forrasreszlete a Thayer_teljes.tsv-bol jon (nem kezzel masolt).

    python fp3/prompt_epit.py
"""

import difflib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V3 = os.path.join(REPO, 'fp2', 'prompt_v3.md')
V4 = os.path.join(REPO, 'fp3', 'prompt_v4.md')
DIFF = os.path.join(REPO, 'fp3', 'prompt_v3_v4.diff')
THAYER = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')

BLOKK = """## Kiegészítő szabályok (v4)

1. Az idézőjeleket és az idézett szerzőt tartsd meg. Ha a forrás mást idéz (pl.
   Bretschneidert), az idézet a fordításban is idézőjelben álljon, a hivatkozással együtt.
2. A jelentésszám (1., 2.) előtt álló bevezető mondat legyen teljes magyar mondat
   („Jelentése … eszerint:”), ne csonka szerkezet.
3. Az *equivalent to* fordítása „=” vagy „vagyis”, ne „megegyezik …-val”.
4. A könyvneveket a folyó szövegben írd ki („Márk evangéliuma”, „a Zsidókhoz írt levél”).
   Rövidítés csak igehelyben álljon, Károli-rövidítéssel.
5. Az *ff* / *f* magyarul „kk.” / „k.”
6. Az elosztó értelmű számokat tedd egyértelművé: *once in Matthew and Luke* →
   „egyszer-egyszer”.
7. A szerzőnevek egységes alakban álljanak (Philón, Josephus, Tertullianus, Plutarkhosz).
   Ha van szerzőnév-sor a terminológiai listában, az az irányadó.
8. Magyar mondatszerkezetet használj: az angol mellékmondat-láncot bontsd magyar
   mondatokra, de tartalmat ne hagyj el, és ne told be.

### Példapár (G26, részlet) — a fenti szabályok alkalmazása

Forrás (angol):

{PELDA_FORRAS}

Célfordítás:

{PELDA_CEL}

"""

PELDA_CEL = (
    'G26 — ἀγάπη, -ης, ἡ; tisztán bibliai és egyházi szó. (Plutarkhosznál, a Sympos. quaest. '
    '7, 6, 3 helyén, Reiske-kiadás VIII. kötet, 835. o., ugyanis Wyttenbach már régen, Reiske '
    'sejtését követve, az ἀγάπης, ὧν olvasat helyére ἀγαπήσων alakot állított vissza.) A világi '
    'szerzők (Arisztotelésztől), Plutarkhosztól kezdve az ἀγάπησις alakot használták. „A '
    'Septuaginta az ἀγάπη szóval adja vissza az אַהֲבָה szót: Én 2:4, 5, 7; Én 3:5, 10; Én 5:8; '
    'Én 7:6; Én 8:4, 6, 7 (»Figyelemre méltó, hogy a szó bevett kifejezésként először az '
    'Énekek énekében bukkan fel. Ez bizonyosan nem véletlen, és elárulja, hogyan értették az '
    'alexandriai Septuaginta-fordítók az Énekben megénekelt szeretetet.« [Zezschwitz, '
    'Profangraec. u. bibl. Sprachgeist, 63. o.]); Jer 2:2; Préd 9:1, Préd 9:6; (2Sám 13:15). '
    'Előfordul még a Bölcs 3:9 és a Bölcs 6:19 helyen. Philónnál és Josephusnál nem emlékszem, '
    'hogy találkoztam volna vele. Az Újszövetségben az Apostolok cselekedetei, Márk evangéliuma '
    'és Jakab levele nem használja. Máté és Lukács evangéliumában egyszer-egyszer, a Zsidókhoz '
    'írt levélben és a Jelenések könyvében kétszer-kétszer fordul elő, Pál, János, Péter és '
    'Júdás írásaiban viszont gyakori.” (Bretschneider, Lexikon, a címszónál); (Philón, Deus '
    'immut. 14. §). Jelentése az ἀγαπάω igét követi, eszerint:'
)


def main():
    v3 = open(V3, encoding='utf-8').read()
    forras = None
    with open(THAYER, encoding='utf-8', newline='') as fh:
        for sor in fh:
            if sor.startswith('G0026\t'):
                forras = sor.rstrip('\r\n').split('\t')[2]
                break
    veg = forras.index('consequently it denotes')
    pelda_forras = forras[:veg + len('consequently it denotes')]

    blokk = BLOKK.replace('{PELDA_FORRAS}', pelda_forras).replace('{PELDA_CEL}', PELDA_CEL)
    marker = '## Ideiglenes terminológia'
    assert v3.count(marker) == 1
    v4 = v3.replace(marker, blokk + marker, 1)
    with open(V4, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(v4)
    d = ''.join(difflib.unified_diff(v3.splitlines(True), v4.splitlines(True), 'prompt_v3.md', 'prompt_v4.md'))
    with open(DIFF, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(d)
    torolt = [l for l in d.splitlines() if l.startswith('-') and not l.startswith('---')]
    print('v3 torolt/modositott sor:', torolt)
    print('irva', V4, len(v4))


if __name__ == '__main__':
    main()
