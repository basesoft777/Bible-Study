#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 22.6 — független szúrópróba: összevetés egy REPÓN KÍVÜLI, zárt licencű forrásból kimásolt szöveggel.

A zárt forrás adata nem kerülhet a repóba, és nem lehet a szótár vagy a párosítás forrása; ez a szkript
csak helyi összevetésre való, és kizárólag ÖSSZESÍTETT számot ír ki (egyezés %, n), versenkénti vagy
szavankénti tartalmat soha (a hibaüzenetek sem idéznek a bemenetből: csak sorszámot).

BEMENET (parancssori paraméter, nincs beégetett útvonal): egy UTF-8 szövegfájl, soronként egy vers,
a Károli-szó után inline Strong-számokkal. A szkript elfogadja a leggyakoribb jelöléseket:
    Kezdetben<7225> teremté<1254> Isten<430>      Kezdetben {7225}   Kezdetben (7225)   Kezdetben [7225]
    Kezdetben 7225    Kezdetben H7225 / G3056     teremté 1254, 8799     (vesszővel kapcsolt pár)
A sor elején állhat az igehely (`1Móz 1:1`, vagy `Gen.1.1`; TAB, `|` vagy szóköz után a szöveg). Ha a sorok
nem hordoznak igehelyet, a `--sorrend` kapcsoló a könyv verseit a minta sorrendjében rendeli a sorokhoz.

SZABÁLYOK (a brief szerint):
  * a vesszővel kapcsolt pár MÁSODIK tagja (pl. `5647, 8799` -> `8799`) igealak-kód, eldobjuk;
  * a `--max-strong` (alap: 8674, héber) fölötti számokat eldobjuk — mindkét oldalon (a zárt forrásból és a
    saját táblából is: a TAHOT H9001–H9049 morféma-kódjai nem szerepelnek a zárt forrásban).

KIMENET (csak összesítés):
  versszinten: a Strong-számok halmaza versenként (egyező halmazú versek aránya; elemszintű átfedés
               = a halmazok metszetének és uniójának összege az összes versen);
  szószinten : ahol a magyar szó betűre egyezik (kis/nagybetű nélkül, az előfordulási sorszám szerint
               párosítva), a saját tábla partner-Strongjai tartalmazzák-e a zárt szó összes Strongját
               (a régi arany halmaz-definíciója);
  külön a `magas` és az `alacsony` linkekre/tokenekre: verses szinten a saját tábla `magas`, illetve
  `alacsony` linkjeinek Strongjai közül hány szerepel a zárt vers halmazában (pontosság);
  szószinten a saját `magas`, illetve `alacsony` bizonyosságú Károli-token.

Használat:
    python eszkozok/karoli_strong/zart_osszevet.py --konyv 1Móz --bemenet <repón kívüli fájl> [--sorrend]
    python eszkozok/karoli_strong/zart_osszevet.py --onteszt        # saját, szintetikus mintaadaton

Kilépési kódok: 0 rendben; 2 hibás paraméter/bemenet (a bemenet a repón belül van, ismeretlen igehely, ...).
"""

import argparse
import os
import re
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import egyesit  # noqa: E402
import tokenek  # noqa: E402

MAX_STRONG_ALAP = 8674

_REF_HU = re.compile(r'^\s*(\d?\s?[^\W\d_]+)\.?\s+(\d+):(\d+)\s*(?:[\t|]\s*|\s+)')
_REF_STEP = re.compile(r'^\s*([A-Za-z0-9]{2,4})\.(\d+)\.(\d+)\s*(?:[\t|]\s*|\s+)')
# egy Strong-csoport: [<{([] [HG]szám (, [HG]szám)* []})>]; a szó után közvetlenül vagy szóközzel
_NUM = r'[HG]?\d{1,4}'
_CSOPORT = re.compile(r'[<{\[(]?\s*(%s(?:\s*,\s*%s)*)\s*[>}\])]?' % (_NUM, _NUM))
_TOKEN = re.compile(r'(?P<szo>[^\W\d_]+(?:[’\'-][^\W\d_]+)*)|(?P<szam>[<{\[(]?\s*%s(?:\s*,\s*%s)*\s*[>}\])]?)' % (_NUM, _NUM))


class Hiba(Exception):
    pass


def sor_elemzes(szoveg, max_strong):
    """Egy sor szövegrésze (igehely nélkül) -> [(szo, [strong int, ...]), ...]."""
    ki = []
    for m in _TOKEN.finditer(szoveg):
        if m.group('szo'):
            ki.append([m.group('szo'), []])
        else:
            if not ki:
                continue
            g = _CSOPORT.fullmatch(m.group('szam').strip())
            if not g:
                continue
            reszek = [int(re.sub(r'[HG]', '', x.strip())) for x in g.group(1).split(',')]
            ki[-1][1].append(reszek[0])        # a vesszővel kapcsolt pár második tagja eldobva
    return [(sz, sorted({n for n in ns if 0 < n <= max_strong})) for sz, ns in ki]


def igehely_felismer(sor, step_hu):
    """(igehely|None, maradék szöveg). Támogatott: `1Móz 1:1`, `Gen.1.1`; hibás/ismeretlen: (None, sor)."""
    m = _REF_STEP.match(sor)
    if m and m.group(1) in step_hu:
        return '%s %s:%s' % (step_hu[m.group(1)], m.group(2), m.group(3)), sor[m.end():]
    m = _REF_HU.match(sor)
    if m:
        konyv = re.sub(r'\s+', '', m.group(1))
        return '%s %s:%s' % (konyv, m.group(2), m.group(3)), sor[m.end():]
    return None, sor


def beolvas(ut, konyv, sorrend, minta_versek, max_strong):
    """{igehely: [(szo, [strong,...]), ...]}. Hibánál Hiba (a bemenet tartalmát nem idézi)."""
    ki = {}
    step_hu = tokenek.konyv_step_to_hu()
    with open(ut, encoding='utf-8-sig') as f:
        sorok = [x.rstrip('\n').rstrip('\r') for x in f]
    sorok = [x for x in sorok if x.strip()]
    if sorrend and len(sorok) != len(minta_versek):
        raise Hiba('--sorrend: %d nem üres sor, de a minta %d verses' % (len(sorok), len(minta_versek)))
    for i, sor in enumerate(sorok):
        if sorrend:
            ig, szoveg = minta_versek[i], sor
            ig0, sz0 = igehely_felismer(sor, step_hu)
            if ig0 is not None:
                szoveg = sz0      # a sor elején álló igehelyet levágjuk, de nem használjuk
        else:
            ig, szoveg = igehely_felismer(sor, step_hu)
            if ig is None:
                raise Hiba('a(z) %d. sor nem igehellyel kezdődik (használd a --sorrend kapcsolót, ha nincs igehely)' % (i + 1))
        if not ig.startswith(konyv + ' '):
            continue
        if ig in ki:
            raise Hiba('ismétlődő igehely a(z) %d. sorban' % (i + 1))
        ki[ig] = sor_elemzes(szoveg, max_strong)
    return ki


def sajat_adat(konyv, max_strong, gyoker=None):
    """A saját tábla (parok, szavak) vers szerint: {ig: {'linkek': [(hu, strong, biz)], 'hu': {hu: (set strong, biz)}}}."""
    u = egyesit.utak(konyv, gyoker)
    parok, szavak = egyesit.olvas(u['parok']), egyesit.olvas(u['szavak'])
    ki = {}
    for r in parok:
        s = int(r['strong'][1:])
        d = ki.setdefault(r['vers'], {'linkek': [], 'hu': {}, 'tokenek': []})
        if s <= max_strong:
            d['linkek'].append((int(r['hu_sorszam']), s, r['bizonyossag']))
    for r in szavak:
        d = ki.setdefault(r['vers'], {'linkek': [], 'hu': {}, 'tokenek': []})
        if r['oldal'] == 'hu':
            d['tokenek'].append((int(r['sorszam']), r['szo'], r['bizonyossag']))
    for ig, d in ki.items():
        for hu, s, biz in d['linkek']:
            d['hu'].setdefault(hu, set()).add(s)
    return ki


def pct(a, b):
    return '%.1f%% (%d/%d)' % (100.0 * a / b, a, b) if b else 'n.é. (0/0)'


def osszevet(zart, sajat):
    """Összesítés; csak számok. Visszaad: dict."""
    v = {'versek': 0, 'egyezo_halmaz': 0, 'metszet': 0, 'unio': 0,
         'magas_van': 0, 'magas_talalt': 0, 'alacsony_van': 0, 'alacsony_talalt': 0}
    sz = {'magas': [0, 0, 0], 'alacsony': [0, 0, 0]}   # [n, tartalmazza, azonos halmaz]
    for ig, szavak in zart.items():
        if ig not in sajat:
            continue
        s = sajat[ig]
        zhalmaz = {n for _, ns in szavak for n in ns}
        shalmaz = {x[1] for x in s['linkek']}
        v['versek'] += 1
        v['egyezo_halmaz'] += zhalmaz == shalmaz
        v['metszet'] += len(zhalmaz & shalmaz)
        v['unio'] += len(zhalmaz | shalmaz)
        for biz in ('magas', 'alacsony'):
            hal = {x[1] for x in s['linkek'] if x[2] == biz}
            v[biz + '_van'] += len(hal)
            v[biz + '_talalt'] += len(hal & zhalmaz)
        # szószint: a magyar szó betűre egyezik (az előfordulási sorszám szerint párosítva)
        tok = {}
        for hu, szo, biz in s['tokenek']:
            tok.setdefault(szo.casefold(), []).append((hu, biz))
        szamlalo = {}
        for szo, ns in szavak:
            k = szo.casefold()
            idx = szamlalo.get(k, 0)
            szamlalo[k] = idx + 1
            if not ns or k not in tok or idx >= len(tok[k]):
                continue
            hu, biz = tok[k][idx]
            if biz not in sz:
                continue
            sh = s['hu'].get(hu, set())
            sz[biz][0] += 1
            sz[biz][1] += set(ns) <= sh
            sz[biz][2] += set(ns) == sh
    return {'vers': v, 'szo': sz}


def kiir(r, max_strong):
    v, sz = r['vers'], r['szo']
    print('zart_osszevet összesítés (csak szám; max-strong=%d)' % max_strong)
    print('versszinten (a Strong-számok halmaza versenként): az összevetett versek száma n=%d' % v['versek'])
    print('  azonos halmazú versek: %s' % pct(v['egyezo_halmaz'], v['versek']))
    print('  elemszintű átfedés (metszet/unió az összes versen): %s' % pct(v['metszet'], v['unio']))
    print('  a saját `magas` linkek Strongjai közül a zárt vers halmazában: %s' % pct(v['magas_talalt'], v['magas_van']))
    print('  a saját `alacsony` linkek Strongjai közül a zárt vers halmazában: %s' % pct(v['alacsony_talalt'], v['alacsony_van']))
    print('szószinten (a magyar szó betűre egyezik, a zárt szónak van Strongja):')
    for biz in ('magas', 'alacsony'):
        n, tart, azo = sz[biz]
        print('  saját `%s` Károli-token: n=%d; a partner-Strongok tartalmazzák a zárt szó összes Strongját: %s; azonos halmaz: %s'
              % (biz, n, pct(tart, n), pct(azo, n)))


def onteszt():
    hibak = []
    # a sor_elemzes tűrése a jelölésekre
    sor = 'Kezdetben<7225> teremté {1254, 8799} Isten (430) az 853 eget H8064 és[9002] a'
    eredmeny = sor_elemzes(sor, MAX_STRONG_ALAP)
    var = [('Kezdetben', [7225]), ('teremté', [1254]), ('Isten', [430]), ('az', [853]), ('eget', [8064]), ('és', []), ('a', [])]
    if eredmeny != var:
        hibak.append('sor_elemzes: %s' % (eredmeny,))
    if sor_elemzes('ige<5647, 8799>', 8674) != [('ige', [5647])]:
        hibak.append('a vesszős pár második tagja nincs eldobva')
    if sor_elemzes('x<9003> y<7225>', 8674) != [('x', []), ('y', [7225])]:
        hibak.append('a max-strong fölötti szám nincs eldobva')
    step_hu = tokenek.konyv_step_to_hu()
    if igehely_felismer('Gen.1.1\tKezdetben<7225>', step_hu)[0] != '1Móz 1:1':
        hibak.append('STEP igehely')
    if igehely_felismer('1Móz 1:1 Kezdetben', step_hu)[0] != '1Móz 1:1':
        hibak.append('magyar igehely')
    # szintetikus „zárt” fájl a saját táblából (NEM a zárt forrásból), a repón kívül
    kt = tokenek.betolt_karoli()
    sajat = sajat_adat('1Móz', MAX_STRONG_ALAP)
    versek = [x for x in kt if x.startswith('1Móz 1:')][:5]
    szoveg = []
    for ig in versek:
        tl = tokenek.tokenizal(kt[ig])
        sorok = []
        for i, t in enumerate(tl, 1):
            ss = sorted(sajat[ig]['hu'].get(i, set()))
            sorok.append('%s%s' % (t, ''.join('<%d>' % s for s in ss[:1]) if ss else ''))
        szoveg.append('%s\t%s' % (ig, ' '.join(sorok)))
    tmp = tempfile.mkdtemp()
    ut = os.path.join(tmp, 'minta.txt')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(szoveg) + '\n')
    zart = beolvas(ut, '1Móz', False, versek, MAX_STRONG_ALAP)
    r = osszevet(zart, sajat)
    if r['vers']['versek'] != 5 or r['szo']['magas'][0] == 0:
        hibak.append('összevetés: %s' % (r,))
    # a saját tábla első Strongjait használtuk: a szó-szintű „tartalmazza” aránynak 100% kell legyen
    for biz in ('magas', 'alacsony'):
        n, tart, _ = r['szo'][biz]
        if n and tart != n:
            hibak.append('a szintetikus minta szó-szintű egyezése nem 100%% (%s: %d/%d)' % (biz, tart, n))
    # sorrend mód: igehely nélküli sorok
    ut2 = os.path.join(tmp, 'sorrend.txt')
    with open(ut2, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(x.split('\t', 1)[1] for x in szoveg) + '\n')
    z2 = beolvas(ut2, '1Móz', True, versek, MAX_STRONG_ALAP)
    if osszevet(z2, sajat) != r:
        hibak.append('a --sorrend mód eltérő eredményt ad')
    # hibás bemenet: nincs igehely, --sorrend nélkül
    try:
        beolvas(ut2, '1Móz', False, versek, MAX_STRONG_ALAP)
        hibak.append('igehely nélküli sor nem hibázott')
    except Hiba:
        pass
    # a kimenetben nincs versenkénti/szavankénti tartalom: a kiir csak számot ír (kézi ellenőrzés: l. a kimenet)
    import io
    puf = io.StringIO()
    stdout = sys.stdout
    sys.stdout = puf
    try:
        kiir(r, MAX_STRONG_ALAP)
    finally:
        sys.stdout = stdout
    kimenet = puf.getvalue()
    for ig in versek:
        if ig in kimenet:
            hibak.append('a kimenet igehelyet tartalmaz: %s' % ig)
    for t in tokenek.tokenizal(kt[versek[0]]):
        if len(t) > 3 and t in kimenet:
            hibak.append('a kimenet szót tartalmaz')
            break
    for h in hibak:
        print('ÖNTESZT HIBA: ' + h, file=sys.stderr)
    print('önteszt: %s' % ('HIBA' if hibak else 'rendben'))
    return 1 if hibak else 0


def repon_belul(ut):
    root = os.path.realpath(tokenek.ROOT)
    p = os.path.realpath(ut)
    return os.path.commonpath([root, p]) == root


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', default=None, help='magyar rövidítés, pl. 1Móz (nincs alapérték)')
    ap.add_argument('--bemenet', default=None, help='a zárt forrásból kimásolt, REPÓN KÍVÜLI szövegfájl útvonala')
    ap.add_argument('--sorrend', action='store_true', help='a sorok igehely nélkül, a könyv verseinek sorrendjében')
    ap.add_argument('--max-strong', type=int, default=MAX_STRONG_ALAP, help='e fölötti Strong-számot eldobja (héber: 8674)')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        return onteszt()
    if not a.konyv or not a.bemenet:
        print('HIBA: --konyv és --bemenet kell (nincs alapérték, nincs beégetett útvonal)', file=sys.stderr)
        return 2
    if not os.path.exists(a.bemenet):
        print('HIBA: a bemeneti fájl nem található', file=sys.stderr)
        return 2
    if repon_belul(a.bemenet):
        print('HIBA: a bemeneti fájl a repón belül van; a zárt forrás adata nem kerülhet a repóba (tedd a repón kívülre)', file=sys.stderr)
        return 2
    minta_versek = [s['igehely'] for s in egyesit.sonnet_koteg.minta_olvas(egyesit.utak(a.konyv)['minta'])]
    try:
        zart = beolvas(a.bemenet, a.konyv, a.sorrend, minta_versek, a.max_strong)
    except Hiba as e:
        print('HIBA: %s' % e, file=sys.stderr)
        return 2
    sajat = sajat_adat(a.konyv, a.max_strong)
    kiir(osszevet(zart, sajat), a.max_strong)
    return 0


if __name__ == '__main__':
    sys.exit(main())
