#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — a Sonnet-oldal kötegkezelője (a Code-session subagentjeinek eszköze).

A Károli–Strong párosítás Sonnet-fele nem API-hívás: a Code-sessionben kötegenként
egy `vegrehajto-sonnet` subagent dolgozik. Ez a szkript API nélkül, determinisztikusan
adja a subagentnek a bemenetet és fogadja a kimenetét:

  minta     az f22/minta_<könyv>.tsv előállítása (a Károli_1908.tsv könyvének minden verse,
            a tokenek.py tokenizálásával; a várt versszámot ellenőrzi)
  allapot   a kötegek állapota (kész / hátralevő), a hátralevők számával
  kovetkezo a következő nem kész köteg(ek) száma
  prompt    egy köteg promptja fájlba (f22/_munka/), a prompt_v3 hash-ellenőrzése után;
            a bemenet ugyanaz, mint a futtat.py-ban (bemenet.kotegszoveg, KJV nélkül)
  mentes    a subagent válaszának beolvasása, kapuellenőrzése és mentése
            f22/valaszok/sonnet/<könyv>.jsonl-be. Hibás válasznál (1. próba) kilép 10-es
            kóddal és kiírja az újrakérés üzenetét; a 2. próba után a még hibás vers
            `kapuhiba`. A köteg-sor formátuma megegyezik a futtat.py koteg_feldolgoz sorával.

A Sonnet-subagent a C válaszait (f22/valaszok/c/) nem olvashatja, és fordítva.

Használat:
    python eszkozok/karoli_strong/sonnet_koteg.py minta --konyv 1Móz --var 1533
    python eszkozok/karoli_strong/sonnet_koteg.py allapot --konyv 1Móz
    python eszkozok/karoli_strong/sonnet_koteg.py prompt --konyv 1Móz --koteg 1
    python eszkozok/karoli_strong/sonnet_koteg.py mentes --konyv 1Móz --koteg 1 --valasz f.json --probalkozas 1
    python eszkozok/karoli_strong/sonnet_koteg.py --onteszt

Kilépési kódok: 0 rendben; 2 hibás paraméter/előfeltétel; 3 a minta versszáma eltér a vártól;
10 a mentésnél az 1. próba hibás (újrakérés kell).
"""

import argparse
import json
import os
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import kapu  # noqa: E402
import tokenek  # noqa: E402

F22 = os.path.join(tokenek.ROOT, 'f22')
PROMPT_SHA = os.path.join(tokenek.ROOT, 'f21p', 'prompt_v3.sha256')
MODELL_CIMKE = 'claude-sonnet (Code-subagent, vegrehajto-sonnet)'
MINTA_FEJLEC = ['sorsz', 'igehely', 'reteg', 'fejezet', 'karoli_szo', 'eredeti_szo']


def ascii_nev(konyv):
    """'1Móz' -> '1Moz' (fájlnévhez)."""
    return ''.join(c for c in unicodedata.normalize('NFD', konyv) if unicodedata.category(c) != 'Mn')


def minta_ut(konyv, f22=None):
    return os.path.join(f22 or F22, 'minta_%s.tsv' % ascii_nev(konyv))


def valasz_ut(konyv, f22=None):
    return os.path.join(f22 or F22, 'valaszok', 'sonnet', '%s.jsonl' % ascii_nev(konyv))


def munka_ut(konyv, koteg, jel, f22=None):
    return os.path.join(f22 or F22, '_munka', 's_%s_k%03d_%s' % (ascii_nev(konyv), koteg, jel))


def minta_epit(konyv, karoli=None, ered=None):
    """A könyv versei a Károli-tábla sorrendjében: [{'sorsz','igehely','reteg','fejezet','karoli_szo','eredeti_szo'}]."""
    karoli = karoli if karoli is not None else tokenek.betolt_karoli()
    ered = ered if ered is not None else tokenek.betolt_eredeti()
    ki = []
    for ig, szoveg in karoli.items():
        b = tokenek.igehely_bont(ig)
        if b is None or b[0] != konyv:
            continue
        if not ered.get(ig):
            continue   # eredeti vers nélkül (versszámozás-eltérés) nincs mit párosítani: l. eredeti_nelkuli_versek
        ki.append({'sorsz': len(ki) + 1, 'igehely': ig, 'reteg': ascii_nev(konyv), 'fejezet': b[1],
                   'karoli_szo': len(tokenek.tokenizal(szoveg)), 'eredeti_szo': len(ered.get(ig, []))})
    return ki


def eredeti_nelkuli_versek(konyv, karoli=None, ered=None):
    """A könyv azon Károli-versei, amelyeknek nincs eredeti (TAHOT) versük (pl. 2Móz 35:36: a Károli-
    számozás kettébontja a héber 35:35-öt). Nem kerülnek modellhez; az egyesítő `kezi` állapotban,
    az átnézési sorral viszi tovább őket (a brief `kezi` ága), hogy minden Károli-token szerepeljen."""
    karoli = karoli if karoli is not None else tokenek.betolt_karoli()
    ered = ered if ered is not None else tokenek.betolt_eredeti()
    ki = []
    for ig in karoli:
        b = tokenek.igehely_bont(ig)
        if b is not None and b[0] == konyv and not ered.get(ig):
            ki.append(ig)
    return ki


def minta_ir(ut, sorok):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(MINTA_FEJLEC) + '\n')
        for s in sorok:
            f.write('\t'.join(str(s[k]) for k in MINTA_FEJLEC) + '\n')


def minta_olvas(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [x.rstrip('\n').rstrip('\r') for x in f]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in sorok[1:] if x.strip()]


def kotegek_listaja(konyv, koteg_meret, f22=None):
    minta = minta_olvas(minta_ut(konyv, f22))
    return bemenet.kotegek([s['igehely'] for s in minta], koteg_meret)


def sorok_beolvas(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        return [json.loads(s) for s in f if s.strip()]


def kesz_szamok(konyv, koteg_meret, f22=None):
    kesz = {tuple(s['igehelyek']) for s in sorok_beolvas(valasz_ut(konyv, f22))}
    return [i for i, k in enumerate(kotegek_listaja(konyv, koteg_meret, f22), 1) if tuple(k) in kesz]


def prompt_hash_hiba():
    return tokenek.hash_hiba(bemenet.PROMPT_V3_UT, PROMPT_SHA, 'f21p/prompt_v3.md')


def prompt_ir(konyv, koteg, koteg_meret, f22=None):
    """A köteg promptja fájlba; visszaad (út, igehelyek)."""
    k = kotegek_listaja(konyv, koteg_meret, f22)
    if not 1 <= koteg <= len(k):
        raise SystemExit('a köteg sorszáma 1–%d lehet' % len(k))
    ig = k[koteg - 1]
    szoveg = bemenet.kotegszoveg(ig, False, bemenet.PROMPT_V3_UT)
    ut = munka_ut(konyv, koteg, 'prompt.txt', f22)
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    return ut, ig


def _sor_epit(konyv, koteg, igehelyek, nyers, versek):
    return {'futas': ascii_nev(konyv), 'modell': MODELL_CIMKE, 'koteg': koteg, 'igehelyek': igehelyek,
            'nyers': nyers,
            'hivasok': [{'probalkozas': i + 1, 'forras': 'subagent'} for i in range(len(nyers))],
            'versek': versek}


def mentes(konyv, koteg, koteg_meret, valasz_szoveg, probalkozas, f22=None):
    """Egy próba feldolgozása. Visszaad: ('kesz'|'ujra', üzenet)."""
    k = kotegek_listaja(konyv, koteg_meret, f22)
    ig = k[koteg - 1]
    if tuple(ig) in {tuple(s['igehelyek']) for s in sorok_beolvas(valasz_ut(konyv, f22))}:
        return 'kesz', 'a köteg már mentve van, nincs teendő'
    allapot_ut = munka_ut(konyv, koteg, '1.json', f22)
    if probalkozas == 1:
        r = kapu.valasz_ellenoriz(valasz_szoveg, ig)
        versek = {i: {'allapot': 'ok' if r[i]['ok'] else 'kapuhiba', 'probalkozas': 1, 'hibak': r[i]['hibak'],
                      'obj': r[i]['obj'] if r[i]['ok'] else None} for i in ig}
        rossz = [i for i in ig if not r[i]['ok']]
        if rossz:
            os.makedirs(os.path.dirname(allapot_ut), exist_ok=True)
            with open(allapot_ut, 'w', encoding='utf-8', newline='\n') as f:
                json.dump({'nyers1': valasz_szoveg, 'versek': versek}, f, ensure_ascii=False)
            return 'ujra', kapu.ujrakeres_uzenet({i: r[i] for i in rossz})
        sor = _sor_epit(konyv, koteg, ig, [valasz_szoveg], versek)
    else:
        if not os.path.exists(allapot_ut):
            raise SystemExit('nincs 1. próba mentve ehhez a köteghez (előbb --probalkozas 1)')
        with open(allapot_ut, encoding='utf-8') as f:
            elozo = json.load(f)
        versek = elozo['versek']
        rossz = [i for i in ig if versek[i]['allapot'] != 'ok']
        r2 = kapu.valasz_ellenoriz(valasz_szoveg, rossz)
        for i in rossz:
            if r2[i]['ok']:
                versek[i] = {'allapot': 'ok', 'probalkozas': 2, 'hibak': [], 'obj': r2[i]['obj']}
            else:
                versek[i] = {'allapot': 'kapuhiba', 'probalkozas': 2, 'hibak': r2[i]['hibak'], 'obj': None}
        sor = _sor_epit(konyv, koteg, ig, [elozo['nyers1'], valasz_szoveg], versek)
    ut = valasz_ut(konyv, f22)
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(sor, ensure_ascii=False) + '\n')
    hibas = sum(1 for v in sor['versek'].values() if v['allapot'] != 'ok')
    return 'kesz', 'köteg %d mentve, kapuhibás vers: %d' % (koteg, hibas)


def onteszt():
    import tempfile
    hibak = []
    tmp = tempfile.mkdtemp()
    karoli = {'1Móz %d:%d' % (c, v): 'Kezdetben teremté Isten az eget és a földet.' for c in (1, 2) for v in (1, 2, 3)}
    karoli['2Móz 1:1'] = 'Ezek'
    ered_proba = {ig: [{'sorsz': 1}] for ig in karoli}
    if len(minta_epit('1Móz', karoli, ered_proba)) != 6 or len(minta_epit('1Móz', karoli, {})) != 0:
        hibak.append('minta_epit versszám')
    if ascii_nev('1Móz') != '1Moz':
        hibak.append('ascii_nev')
    # a teljes folyamat valódi adaton, ideiglenes könyvtárban: az 1Móz 1:1–10 hibátlan "válasza" a
    # kapu szerint nem létezik előre, ezért csak a hibás-válasz ágat és az újrakérést teszteljük
    minta_ir(minta_ut('1Móz', tmp), minta_epit('1Móz')[:20])
    if len(kotegek_listaja('1Móz', 10, tmp)) != 2:
        hibak.append('kötegelés')
    allapot, uzenet = mentes('1Móz', 1, 10, 'nem json', 1, tmp)
    if allapot != 'ujra' or 'VERS: 1Móz 1:1' not in uzenet:
        hibak.append('1. próba hibás válaszra nem kért újra')
    allapot, uzenet = mentes('1Móz', 1, 10, 'még mindig nem json', 2, tmp)
    sorok = sorok_beolvas(valasz_ut('1Móz', tmp))
    if allapot != 'kesz' or len(sorok) != 1 or any(v['allapot'] != 'kapuhiba' for v in sorok[0]['versek'].values()):
        hibak.append('2. próba utáni kapuhiba-mentés')
    if kesz_szamok('1Móz', 10, tmp) != [1]:
        hibak.append('kesz_szamok')
    if mentes('1Móz', 1, 10, 'x', 1, tmp)[0] != 'kesz':
        hibak.append('a kész köteg újramentése nem kimaradás')
    for h in hibak:
        print('ÖNTESZT HIBA: ' + h, file=sys.stderr)
    print('önteszt: %s' % ('HIBA' if hibak else 'rendben'))
    return 1 if hibak else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('parancs', nargs='?', choices=['minta', 'allapot', 'kovetkezo', 'prompt', 'mentes'])
    ap.add_argument('--konyv', default=None, help='magyar rövidítés, pl. 1Móz (nincs alapérték)')
    ap.add_argument('--koteg-meret', type=int, default=10)
    ap.add_argument('--var', type=int, default=None, help='minta: a várt versszám (eltérésnél 3-as kilépési kód)')
    ap.add_argument('--koteg', type=int, default=None)
    ap.add_argument('--valasz', default=None)
    ap.add_argument('--probalkozas', type=int, default=1, choices=[1, 2])
    ap.add_argument('--n', type=int, default=1, help='kovetkezo: ennyi hátralevő köteg száma')
    ap.add_argument('--ig', type=int, default=None, help='kovetkezo: csak a legfeljebb ennyedik kötegig')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        return onteszt()
    if not a.parancs or not a.konyv:
        print('HIBA: parancs és --konyv kell (nincs alapérték)', file=sys.stderr)
        return 2
    if a.parancs == 'minta':
        sorok = minta_epit(a.konyv)
        kimaradt = eredeti_nelkuli_versek(a.konyv)
        print('%s: %d vers (+ %d eredeti nélküli, nem kerül modellhez: %s)' % (a.konyv, len(sorok), len(kimaradt), ', '.join(kimaradt) or '-'))
        if a.var is not None and len(sorok) + len(kimaradt) != a.var:
            print('ELTÉRÉS: a várt %d vers helyett %d; megállás és jelentés' % (a.var, len(sorok) + len(kimaradt)), file=sys.stderr)
            return 3
        minta_ir(minta_ut(a.konyv), sorok)
        print('írva: %s; kötegek (%d vers/köteg): %d' % (minta_ut(a.konyv), a.koteg_meret,
                                                         len(kotegek_listaja(a.konyv, a.koteg_meret))))
        return 0
    if a.parancs in ('allapot', 'kovetkezo'):
        osszes = len(kotegek_listaja(a.konyv, a.koteg_meret))
        kesz = set(kesz_szamok(a.konyv, a.koteg_meret))
        hatra = [i for i in range(1, osszes + 1) if i not in kesz and (a.ig is None or i <= a.ig)]
        if a.parancs == 'allapot':
            print('köteg összesen: %d, kész: %d, hátralevő: %d' % (osszes, len(kesz), osszes - len(kesz)))
        else:
            print(' '.join(str(i) for i in hatra[:a.n]))
        return 0
    if a.parancs == 'prompt':
        h = prompt_hash_hiba()
        if h:
            print('BEFAGYASZTÁS HIBA: %s' % h, file=sys.stderr)
            return 2
        if a.koteg is None:
            print('HIBA: --koteg kell', file=sys.stderr)
            return 2
        ut, ig = prompt_ir(a.konyv, a.koteg, a.koteg_meret)
        print('prompt: %s' % ut)
        print('versek (%d): %s' % (len(ig), ', '.join(ig)))
        return 0
    if a.parancs == 'mentes':
        if a.koteg is None or not a.valasz:
            print('HIBA: --koteg és --valasz kell', file=sys.stderr)
            return 2
        with open(a.valasz, encoding='utf-8') as f:
            szoveg = f.read()
        allapot, uzenet = mentes(a.konyv, a.koteg, a.koteg_meret, szoveg, a.probalkozas)
        print(uzenet)
        return 10 if allapot == 'ujra' else 0
    return 2


if __name__ == '__main__':
    sys.exit(main())
