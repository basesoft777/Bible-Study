#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F27 (FP3) M0 — felmérés a teljes Thayerre (csak olvas és mér; a repóba csak a naplok/FP3_* fájlokat írja).

  python naplok/FP3_M0.py sorrend      naplok/FP3_sorrend.tsv + adagterv (stdout)
  python naplok/FP3_M0.py szaraz       a kérések összeállítása minden fordítandó Strongra (hiba-lista, kérés-, csoportszám)
  python naplok/FP3_M0.py kapu         a kész szakaszsorok (sonnet, kezi) újrakapuzása
  python naplok/FP3_M0.py konyv        könyv-/hivatkozásfedés, Sir, Kelemen, klasszikusok
  python naplok/FP3_M0.py sigla        sigla-fedés (jelolt / besorolt) a teljes Thayerben és az M1-adagban
  python naplok/FP3_M0.py term         terminológia-fedés (javaslatlista)

Megjegyzés: a `sorrend` és a `szaraz` a futás pillanatának listáját használja (kész Strongok kimaradnak); az M1 beírása (28 Strong) után a `sorrend` újrafuttatása más, rövidebb sorrendet írna, ezért a commitolt `FP3_sorrend.tsv` az M0 pillanatának állapota. A `szaraz` a `naplok/FP3_szaraz_hibak.tsv`-be is ír (hibalista). A `minta` a fájl végén fut.
TSV: split('\\t'), '\\t'.join(); csv modul nincs. Számok csak innen (proveniencia: scope=teljes Thayer | forras=ez a szkript).
"""
import collections
import datetime
import os
import re
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(ITT)
ESZK = os.path.join(GYOKER, 'eszkozok')
for u in (ESZK, os.path.join(ESZK, 'thayer_jelolt'), os.path.join(ESZK, 'karoli_strong')):
    if u not in sys.path:
        sys.path.insert(0, u)

import thayer_api_koteg as TK  # noqa: E402
import thayer_bemenet as TB  # noqa: E402

PAROK = os.path.join(GYOKER, 'adat', 'karoli_strong')
USZ = ['1Jan', '1Kor', '1Pet', '1Thessz', '1Tim', '2Jan', '2Kor', '2Pet', '2Thessz', '2Tim', '3Jan', 'ApCsel', 'Ef', 'Fil',
       'Filem', 'Gal', 'Jak', 'Jan', 'Jel', 'Jud', 'Kol', 'Luk', 'Mk', 'Mt', 'Rom', 'Tit', 'Zsid']
M1_CEL = 150000
ADAG_CEL = 500000


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n')]
    sorok = [s for s in sorok if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def lista():
    return TK.teljes_lista(datetime.date.today().isoformat())


def gyakorisag():
    """Strong_padded -> a Károli ÚSZ-ben hozzá párosított magyar szavak száma (parok_<ÚSZ-könyv>.tsv sorai)."""
    c = collections.Counter()
    for k in USZ:
        with open(os.path.join(PAROK, 'parok_%s.tsv' % k), encoding='utf-8', newline='') as f:
            for l in f.read().split('\n'):
                if not l or l.startswith('#') or l.startswith('vers\t'):
                    continue
                m = l.rstrip('\r').split('\t')
                if len(m) > 5 and re.match(r'^G\d{4}', m[5]):
                    c['G' + m[5][1:5]] += 1
    return c


def strong_alap(sp):
    return sp[:5]


def sorrend():
    gy = gyakorisag()
    sorok = [r for r in lista() if r['statusz'] == 'forditando']
    sorok.sort(key=lambda r: (-gy.get(strong_alap(r['strong']), 0), r['strong']))
    ki = []
    adag, kum, hatar = 1, 0, M1_CEL
    for i, r in enumerate(sorok, 1):
        kar = int(r['karakter'])
        if kum >= hatar and adag >= 1:
            adag += 1
            kum = 0
            hatar = ADAG_CEL
        kum += kar
        ki.append([str(i), r['strong'], str(gy.get(strong_alap(r['strong']), 0)), str(kar), r['szakasz'], str(adag)])
    ut = os.path.join(ITT, 'FP3_sorrend.tsv')
    fej = '# GENERÁLT: naplok/FP3_M0.py sorrend (F27 M0) — Károli ÚSZ Strong-gyakoriság szerint csökkenő, egyenlőségnél a Strong-szám; a kész Strongok kimaradnak | scope=teljes Thayer | forras=adat/karoli_strong/parok_<ÚSZ>.tsv + thayer_api_koteg.py lista | ts=%s\n' % datetime.date.today().isoformat()
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + '\t'.join(['sorszam', 'strong', 'gyakorisag', 'karakter', 'szakasz', 'adag']) + '\n')
        for r in ki:
            f.write('\t'.join(r) + '\n')
    c = collections.defaultdict(lambda: [0, 0, 0])
    for r in ki:
        a = c[int(r[5])]
        a[0] += 1
        a[1] += int(r[3])
        a[2] += int(r[4])
    print('fordítandó Strong: %d, karakter %d, szakasz %d' % (len(ki), sum(int(r[3]) for r in ki), sum(int(r[4]) for r in ki)))
    print('adag\tStrong\tkarakter\tszakasz')
    for k in sorted(c):
        print('%d\t%d\t%d\t%d' % (k, c[k][0], c[k][1], c[k][2]))
    nulla = sum(1 for r in ki if r[2] == '0')
    print('nulla ÚSZ-gyakoriságú Strong (a sorrend végén, Strong-szám szerint): %d' % nulla)


def szaraz():
    sorok = [r for r in lista() if r['statusz'] == 'forditando']
    hibak, kerelem, csoport, prompt_kar, forras_kar, t0 = [], 0, 0, 0, 0, time.time()
    tobb = 0
    nagy = []
    for i, r in enumerate(sorok, 1):
        try:
            ker = TK.kerelmek_strongra(r['strong'])
        except BaseException as e:  # noqa: BLE001  (SystemExit is)
            hibak.append((r['strong'], '%s: %s' % (type(e).__name__, str(e)[:200])))
            continue
        kerelem += len(ker)
        csoport += len(ker)
        tobb += 1 if len(ker) > 1 else 0
        prompt_kar += sum(len(k['prompt']) for k in ker)
        forras_kar += sum(k['forras_kar'] for k in ker)
        nagy += [len(k['prompt']) for k in ker if len(k['prompt']) > 20000]
        if i % 500 == 0:
            print('... %d/%d (%.0f mp)' % (i, len(sorok), time.time() - t0), file=sys.stderr)
    print('Strong: %d; hibás előkészítés: %d; kérés (csoport): %d; többcsoportos Strong: %d' % (len(sorok), len(hibak), kerelem, tobb))
    print('prompt-karakter összesen %d, forrás-karakter (tokenes) %d; 20 000 karakter fölötti prompt: %d; idő %.0f mp' % (
        prompt_kar, forras_kar, len(nagy), time.time() - t0))
    for h in hibak[:50]:
        print('HIBA\t%s\t%s' % h)
    ut = os.path.join(ITT, 'FP3_szaraz_hibak.tsv')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('strong\tok\n' + ''.join('%s\t%s\n' % h for h in hibak))


def forras_szovegek():
    """Strong_padded -> a forrásnézet szövege (javított forrás; a szakaszok `szoveg`-e egymás után)."""
    return {sp: [x['szoveg'] for x in TB.szakaszok(sp)] for sp in sorted(TB.tabla_olvas())}


def kesz_sorok():
    """A kész szakaszsorok: Thayer, forditas_hu, nem elavult -> {strong: {allapot: [sor]}}."""
    ki = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in tsv(os.path.join(GYOKER, 'adat', 'forditasok.tsv')):
        if r['szotar'] == 'Thayer' and r['mezo'] == 'forditas_hu' and r['jelentes_szam'].startswith('sz') and r['allapot'] != 'elavult':
            ki[r['strong']][r['allapot']].append(r)
    return ki


def kapu():
    import forditas as F
    import forditas_kapuk as K
    import thayer_kapuk as TKP
    ks = kesz_sorok()
    osszes = collections.Counter()
    jelzes = collections.Counter()
    sorok = []
    for sp in sorted(ks):
        szak = TB.szakaszok(sp)
        for allapot, rs in ks[sp].items():
            by = {int(r['jelentes_szam'][2:]): r for r in rs}
            if sorted(by) != [x['sorszam'] for x in szak]:
                sorok.append((sp, allapot, 'nem_teljes', 'szakaszsor-hiány: van %s, kell %s' % (sorted(by), [x['sorszam'] for x in szak])))
                continue
            f_tok = TB.tokenes(szak)
            fordit = TB.tokenes([dict(x, szoveg=by[x['sorszam']]['forditas_hu']) for x in szak])
            eredm = TKP.kapuk_futtat_thayer(f_tok, fordit)
            ok = TKP.atment(eredm)
            osszes[(allapot, 'atment' if ok else 'bukott')] += 1
            for n, e, rsz in eredm:
                if e != 'RENDBEN':
                    jelzes[(allapot, n, e)] += 1
                    sorok.append((sp, allapot, '%s %s' % (n, e), rsz[:200]))
    print('Strong × állapot: %s' % dict(osszes))
    for k, v in sorted(jelzes.items()):
        print('jelzés	%s	%d' % ('	'.join(k), v))
    for x in sorok[:60]:
        print('	'.join(x))


def konyv():
    import forditas_kapuk as K
    lek, fm, _ = K._konyv_mintak()
    sz = forras_szovegek()
    teljes = '\n'.join(t for ts in sz.values() for t in ts)
    minta = re.compile(r'(?<![A-Za-zÀ-ÿ0-9])((?:[1-3]|I{1,3})\s?[A-Z][A-Za-z]{1,14}\.?|[A-Z][A-Za-z]{1,14}\.?)\s+\d{1,3}[:,]\s?\d')
    c = collections.Counter(m.group(1) for m in minta.finditer(teljes))
    kozos = collections.Counter(m.group(1) for m in fm.finditer(teljes))
    print('c:v előtti szó összesen %d (%d különböző); a leképpezett könyvnevek találata %d' % (sum(c.values()), len(c), sum(kozos.values())))
    nem = [(k, n) for k, n in c.most_common() if k not in lek and k.rstrip('.') not in lek]
    print('nem leképezett c:v előtti alakok: %d különböző, %d előfordulás; első 60:' % (len(nem), sum(n for _, n in nem)))
    for k, n in nem[:60]:
        print('  %s	%d' % (k, n))
    sir = len(re.findall(r'(?<![A-Za-z])Sir\.?\s+\d{1,3}[:,]', teljes))
    kel = len(re.findall(r'[1-3]?\s?Cor\.?\s+\d{1,3},\s?\d', teljes))
    print('Sir c:v: %d; Cor. c, v (vessző-alak): %d' % (sir, kel))
    for nev in ('Hom.', 'Xen.', 'Plat.', 'Arist.', 'Plut.', 'Thuc.', 'Herod.', 'Joseph.', 'Josephus', 'Philo', 'Diod.', 'Eur.', 'Soph.', 'Aeschyl.', 'Polyb.', 'Demosth.', 'Epict.', 'Lucian', 'Antoninus'):
        print('klasszikus %s	%d' % (nev, teljes.count(nev)))


def sigla():
    import thayer_kapuk as TKP
    sg = tsv(os.path.join(GYOKER, 'adat', 'thayer_sigla.tsv'))
    sz = forras_szovegek()
    ordered = [r['strong'] for r in tsv(os.path.join(ITT, 'FP3_sorrend.tsv')) if r['adag'] == '1']
    m1 = '\n'.join(t for sp in ordered for t in sz[sp])
    teljes = '\n'.join(t for ts in sz.values() for t in ts)
    c = collections.Counter()
    for r in sg:
        if not r.get('forrasalak'):
            continue
        re_ = TKP._re(r['forrasalak'])
        c[('teljes', r['allapot'])] += len(re_.findall(teljes))
        c[('m1', r['allapot'])] += len(re_.findall(m1))
        if re_.search(m1) and r['allapot'] != 'besorolt':
            c[('m1_jelolt_sigla_sor', r['allapot'])] += 1
    print('sigla sorok: %s' % dict(collections.Counter(r['allapot'] for r in sg)))
    for k, v in sorted(c.items()):
        print('%s	%s	%d' % (k[0], k[1], v))


def term():
    import emeles as E
    tt = tsv(os.path.join(GYOKER, 'adat', 'terminologia.tsv'))
    sz = forras_szovegek()
    teljes = ' '.join(t for ts in sz.values() for t in ts).lower()
    szavak = collections.Counter(re.findall(r"[a-z][a-z'-]{3,}", teljes))
    angol = {r['angol'].lower() for r in tt}
    print('terminológia-sorok: %d' % len(tt))
    print('leggyakoribb angol szavak (>=4 betű), amelyeknek nincs terminológia-sora (első 80; javaslatlista, a fájl nem változik):')
    ki = [(w, n) for w, n in szavak.most_common(3000) if w not in angol and w not in STOP][:80]
    for w, n in ki:
        print('  %s	%d' % (w, n))
    print('Thayer-releváns sorok (angol, magyar): %s' % ', '.join('%s=%s' % (r['angol'], r['magyar']) for r in tt)[:600])


STOP = set("that with from this which have their also used were been into than they there when other these what those such only about after more some them will would being under upon between before said through both most where while very over".split())


if __name__ == '__main__':
    {'sorrend': sorrend, 'szaraz': szaraz, 'kapu': kapu, 'konyv': konyv, 'sigla': sigla, 'term': term}.get(sys.argv[1] if len(sys.argv) > 1 else '', lambda: print(__doc__))()


def minta_valaszt():
    """M1 rétegzett kiegészítés (orkesztrátori döntés, 2026-11-02): seed 27, hosszkategóriánként véletlen, +legfeljebb 30 000 karakter."""
    import random
    r = [l.rstrip('\n').split('\t') for l in open(os.path.join(ITT, 'FP3_sorrend.tsv'), encoding='utf-8') if not l.startswith('#')][1:]
    alap = [x for x in r if x[5] == '1']
    pool = [x for x in r if x[5] != '1']
    kat = lambda k: 'kicsi' if k < 500 else ('kozepes' if k < 3000 else 'nagy')   # noqa: E731
    rnd = random.Random(27)
    cel = [('kicsi', 11), ('kozepes', 9), ('nagy', 5)]
    ki, kum = [], 0
    for nev, db in cel:
        jel = [x for x in pool if kat(int(x[3])) == nev]
        rnd.shuffle(jel)
        n = 0
        for x in jel:
            if n == db:
                break
            if kum + int(x[3]) > 30000:
                continue
            ki.append((nev, x))
            kum += int(x[3])
            n += 1
    ut = os.path.join(ITT, 'FP3_m1_strongok.tsv')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/FP3_M0.py minta (F27 M1; seed=27; kicsi <500, közepes 500–2999, nagy ≥3000 karakter; +≤30 000) | scope=teljes Thayer, M1 | forras=naplok/FP3_sorrend.tsv\n')
        f.write('strong\tkategoria\tkarakter\tszakasz\n')
        for x in alap:
            f.write('%s\tfunkciószó\t%s\t%s\n' % (x[1], x[3], x[4]))
        for nev, x in ki:
            f.write('%s\t%s\t%s\t%s\n' % (x[1], nev, x[3], x[4]))
    print('alap %d Strong %d kar; minta %d Strong %d kar' % (len(alap), sum(int(x[3]) for x in alap), len(ki), kum))
    print(collections.Counter(n for n, _ in ki))


if len(sys.argv) > 1 and sys.argv[1] == 'minta':
    minta_valaszt()
