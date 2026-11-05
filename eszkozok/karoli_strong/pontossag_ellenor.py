#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a vak Opus-ellenőrzés bemenete és kapuja.

--kotegek : a rétegzett minta (f172/minta.tsv) és a régi arany
            (konkordancia/Karoli_Strong_kivonat.tsv, tokenek.regi_arany) versei
            versblokkokká (a #22 bemenetének formája, bemenet.versblokk, KJV nélkül);
            versenként a CÉL Károli-szavak sorszámai (a gépi pár NEM látszik);
            a versek rögzített maggal megkeverve, KOTEG versenként egy fájlba:
              f172/ellenor/bemenet/koteg_NNN.txt
            és a céltábla: f172/ellenor/celok.tsv (melyik cél honnan jött).
            Előtte ellenőrzi, hogy a minta minden pára a mai bemenetből levezethető
            (hu_szo a Károli-tokenből, er_szo/strong a TAHOT/TAGNT-tokenből).
--kapu N  : a koteg_NNN válaszfájl (f172/ellenor/valasz/koteg_NNN.json) ellenőrzése:
            érvényes JSON, a fejlécben modellnév, minden vers és minden cél pontosan
            egyszer, csak létező eredeti sorszám. Kilépési kód 1 hibánál.
--allapot : melyik köteg kész / hibás / hiányzik.

Az adat/karoli_strong/ nem olvasott (csak a minta, amely a pár-kulcsot hordozza).
Olvasás split('\\t'), írás '\\t'.join() (a csv modul tilos, CLAUDE.md).

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong/pontossag_ellenor.py --kotegek
    python eszkozok/karoli_strong/pontossag_ellenor.py --kapu 7
    python eszkozok/karoli_strong/pontossag_ellenor.py --allapot
"""

import argparse
import json
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import pontossag_minta as pm  # noqa: E402
import tokenek  # noqa: E402

GYOKER = pm.GYOKER
ELLENOR = os.path.join(GYOKER, 'f172', 'ellenor')
BEMENET_DIR = os.path.join(ELLENOR, 'bemenet')
VALASZ_DIR = os.path.join(ELLENOR, 'valasz')
CELOK = os.path.join(ELLENOR, 'celok.tsv')
MAG = 20261105
KOTEG = 25
TILTOTT_MODELL = ('sonnet', 'gemini')


def _kifejezes_helyek(tl, kif):
    n = len(kif)
    kif = [t.casefold() for t in kif]
    tl = [t.casefold() for t in tl]
    return [i for i in range(len(tl) - n + 1) if n and tl[i:i + n] == kif]


def celok_gyujt():
    """{vers: {hu_sorszam: [forras-azonosító, ...]}} + az arany kimaradt hármasai."""
    karoli, ered = bemenet._adatok()
    _, minta = pm._tabla(os.path.join(pm.KIMENET, 'minta.tsv'))
    cel = {}
    hibak = []
    for r in minta:
        v = r['vers']
        tl = tokenek.tokenizal(karoli[v])
        h, e = int(r['hu_sorszam']), int(r['er_sorszam'])
        if tl[h - 1] != r['hu_szo']:
            hibak.append('%s hu %d: %s != %s' % (v, h, tl[h - 1], r['hu_szo']))
        w = ered[v][e - 1]
        if w['sorsz'] != e or w['alak'] != r['er_szo'] or w['strong'] != r['strong']:
            hibak.append('%s er %d: %s/%s != %s/%s' % (v, e, w['alak'], w['strong'], r['er_szo'], r['strong']))
        cel.setdefault(v, {}).setdefault(h, []).append(r['minta_id'])
    kimaradt = []
    for i, (ig, szo, strong) in enumerate(tokenek.regi_arany(), 1):
        aid = 'ARANY-%03d' % i
        if ig not in karoli or ig not in ered:
            kimaradt.append((aid, ig, 'nincs vers'))
            continue
        tl = tokenek.tokenizal(karoli[ig])
        helyek = _kifejezes_helyek(tl, tokenek.tokenizal(szo))
        if not helyek:
            kimaradt.append((aid, ig, 'a kifejezés nincs a versben'))
            continue
        n = len(tokenek.tokenizal(szo))
        for p in helyek:
            for j in range(n):
                cel.setdefault(ig, {}).setdefault(p + j + 1, []).append(aid)
    return cel, hibak, kimaradt


def utasitas():
    """A szabályrész a f21p/prompt_v3.md-ből (A–L), változatlanul."""
    s = bemenet.prompt_utasitas(bemenet.PROMPT_V3_UT)
    a = s.index('Párosítási szabályok')
    b = s.index('Kötelező szabályok')
    return s[a:b].strip()


FELADAT = """Feladat (F172, vak ellenőrzés): bibliaversek Károli (1908) szavaihoz kell megjelölnöd a megfelelő eredeti (héber vagy görög) szavakat.

Minden versnél kapod a VERS igehelyét, a KÁROLI számozott szavait, az EREDETI számozott szavait (sorszám, ragozott alak, Strong-szám, angol tükörfordítás [szögletes zárójelben]; a héber elöljárók, kötőszavak, névelők és toldalékok, H9xxx, külön szónak számítanak), és a CÉL sort: a Károli-szavak sorszámait, amelyekről döntened kell. Csak a CÉL szavakról dönts, de a vers egészét olvasd el.

Minden CÉL Károli-szóhoz add meg az összes eredeti szó sorszámát, amelynek megfelel (egy vagy több), vagy üres listát, ha a szónak nincs eredeti megfelelője (betoldás: pl. az önálló magyar névelő, a segédige, Károli magyarázó betoldása). A vitás eseteket az alábbi szabályok döntik el; ezek ugyanazok, amelyek szerint a párosítás készült.

{SZABALYOK}

Kimenet: egyetlen JSON-objektum a megadott fájlba, semmi más:
{"modell": "<a saját tényleges modellazonosítód, pl. claude-opus-5-5>", "koteg": <köteg száma>, "versek": [{"vers": "<igehely>", "jeloles": [[<Károli-sorszám>, [<eredeti sorszám>, ...]], ...]}, ...]}
- a versek sorrendje a bemeneté; minden vers minden CÉL sorszáma pontosan egyszer szerepel a `jeloles`-ben;
- csak létező eredeti sorszámot írj; Strong-számot ne írj;
- ha bizonytalan vagy, a legvalószínűbb, szövegből megalapozott jelölést add; a bizonytalanságot ne írd a fájlba.
"""


def kotegek_epit():
    cel, hibak, kimaradt = celok_gyujt()
    if hibak:
        print('HIBA: a minta párjai nem vezethetők le a mai bemenetből (%d):' % len(hibak))
        for h in hibak[:20]:
            print('  ' + h)
        raise SystemExit(1)
    versek = sorted(cel)
    rnd = random.Random(MAG)
    rnd.shuffle(versek)
    os.makedirs(BEMENET_DIR, exist_ok=True)
    os.makedirs(VALASZ_DIR, exist_ok=True)
    with open(os.path.join(ELLENOR, 'utasitas.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(FELADAT.replace('{SZABALYOK}', utasitas()))
    sorok = []
    nk = 0
    for k in range(0, len(versek), KOTEG):
        nk += 1
        blokk = []
        for v in versek[k:k + KOTEG]:
            celok = sorted(cel[v])
            blokk.append(bemenet.versblokk(v, kjv=False) + '\nCÉL (Károli-sorszámok): ' +
                         ', '.join(str(c) for c in celok))
            for c in celok:
                sorok.append([str(nk), v, str(c), ','.join(cel[v][c])])
        with open(os.path.join(BEMENET_DIR, 'koteg_%03d.txt' % nk), 'w', encoding='utf-8', newline='\n') as f:
            f.write('KÖTEG: %d\n\n' % nk + '\n\n'.join(blokk) + '\n')
    with open(CELOK, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 vak ellenőrzés céljai (minta + régi arany) | forras=f172/minta.tsv, '
                'konkordancia/Karoli_Strong_kivonat.tsv, konkordancia/Karoli_1908.tsv, TAHOT/TAGNT_kivonat.tsv | '
                'ts=git:%s | manual (determinisztikus, mag=%d, köteg=%d vers)\n' % (pm.git_head(), MAG, KOTEG))
        f.write('koteg\tvers\thu_sorszam\tforras_id\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
        for aid, ig, ok in kimaradt:
            f.write('\t'.join(['-', ig, '-', aid + ' (kimaradt: %s)' % ok]) + '\n')
    print('%d vers, %d cél, %d köteg; arany kimaradt: %d' % (len(versek), len(sorok), nk, len(kimaradt)))


def _celtabla():
    _, sorok = pm._tabla(CELOK)
    d = {}
    for r in sorok:
        if r['koteg'] == '-':
            continue
        d.setdefault(int(r['koteg']), {}).setdefault(r['vers'], set()).add(int(r['hu_sorszam']))
    return d


def kapu(n, celtabla=None):
    """Hibalista (üres = rendben)."""
    celtabla = celtabla or _celtabla()
    ut = os.path.join(VALASZ_DIR, 'koteg_%03d.json' % n)
    if not os.path.exists(ut):
        return ['nincs válaszfájl']
    try:
        with open(ut, encoding='utf-8') as f:
            d = json.load(f)
    except Exception as ex:  # noqa: BLE001
        return ['érvénytelen JSON: %s' % ex]
    hib = []
    m = str(d.get('modell', ''))
    if not m or any(t in m.lower() for t in TILTOTT_MODELL) or 'opus' not in m.lower():
        hib.append('modell: %r (Opus kell, nem Sonnet/gemini)' % m)
    if d.get('koteg') != n:
        hib.append('koteg: %r != %d' % (d.get('koteg'), n))
    _, ered = bemenet._adatok()
    var = celtabla.get(n, {})
    kapott = {}
    for x in d.get('versek', []):
        v = x.get('vers')
        if v in kapott:
            hib.append('%s kétszer' % v)
        kapott[v] = x.get('jeloles', [])
    for v in var:
        if v not in kapott:
            hib.append('%s hiányzik' % v)
            continue
        ne = len(ered[v])
        seen = []
        for el in kapott[v]:
            if not (isinstance(el, list) and len(el) == 2 and isinstance(el[0], int) and isinstance(el[1], list)):
                hib.append('%s rossz elem: %r' % (v, el))
                continue
            seen.append(el[0])
            for e in el[1]:
                if not isinstance(e, int) or e < 1 or e > ne:
                    hib.append('%s nem létező eredeti sorszám: %r' % (v, e))
        if sorted(seen) != sorted(var[v]):
            hib.append('%s célok: %s != %s' % (v, sorted(seen), sorted(var[v])))
    for v in kapott:
        if v not in var:
            hib.append('%s nem ebben a kötegben' % v)
    return hib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kotegek', action='store_true')
    ap.add_argument('--kapu', type=int)
    ap.add_argument('--allapot', action='store_true')
    a = ap.parse_args()
    if a.kotegek:
        kotegek_epit()
    if a.kapu is not None:
        h = kapu(a.kapu)
        print('köteg %d: %s' % (a.kapu, 'RENDBEN' if not h else '%d hiba' % len(h)))
        for x in h[:30]:
            print('  ' + x)
        if h:
            raise SystemExit(1)
    if a.allapot:
        ct = _celtabla()
        kesz, hibas, hiany = [], [], []
        for n in sorted(ct):
            if not os.path.exists(os.path.join(VALASZ_DIR, 'koteg_%03d.json' % n)):
                hiany.append(n)
            elif kapu(n, ct):
                hibas.append(n)
            else:
                kesz.append(n)
        print('kész %d, hibás %s, hiányzik %d (%s)' % (len(kesz), hibas, len(hiany),
                                                       ','.join(map(str, hiany[:40]))))


if __name__ == '__main__':
    main()
