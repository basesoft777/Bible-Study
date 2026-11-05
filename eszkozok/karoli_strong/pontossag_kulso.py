#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a független Strong-forrással (Bible-Discovery, Strong-os Károli) való
összevetés versadagjainak kijelölése.

A forrás zárt licencű: a bemásolt szövege csak a repón kívül, mérésre áll
(DT32-elv, DT-F172a). Ez a szkript csak az adagok VERSLISTÁJÁT írja (igehely,
a forrás valószínű számozása), a forrás szövegét nem.

A bemásolás egysége a teljes fejezet (Károli: „rész”), rétegenként egy
(DT-F172a (4″), a felhasználó: „max egy teljes rész tudok másolni”, „8 fejezet”).

--fejezetek : rétegenként az a fejezet, amelyben a legtöbb célpár van (a
              rétegzett minta párjai: előbb az Opus-eltérések, utána az összes
              célpár száma; döntetlennél a fejezet neve). Feltétel: a fejezet
              minden versének Károli- és KJV-száma azonos, és más Károli-vers nem
              esik a KJV-fejezetbe (ÚSZ: a tábla nem fedi, azonosnak vesszük);
              15–40 vers; nincs `kezi` (fuggoben) tokenje; a fejezetek
              különbözők. -> f172/kulso/fejezetek.tsv (a párok száma: összes és
              tartalmi, azaz nem morféma)

--osszevet <fájl> --fejezet "3Móz 3" : egy bemásolt fejezet (a REPÓN KÍVÜLI
              fájl; soronként igehely-fejléc, alatta a vers szövege, a szó UTÁN
              a Strong-szám(ok) H/G előtag nélkül) összevetése a gépi párokkal.
              A 0 és az igealak-kód (héber > 8674, görög > 5624) eldobva; a
              sorvégi „*( … )” megjegyzés figyelmen kívül. A szóalak csak
              igazítási támasz (difflib a helyesírásilag normalizált szavakon; az
              „a mely” ↔ „amely” típusú összevonás összefűzéssel). A gépi pár
              tartalmi (nem morféma) párjaira: `egyezik` (a pár Strongja a
              forrás szavának Strongjai közt) · `masodlagos` (nincs köztük, de
              ugyanannak a Károli-szónak egy másik gépi párja egyezik: a forrás
              szavanként a fő Strongot jelöli, a ragban/elöljáróban álló
              mellékszót nem; vitatható, nem hiba) · `elter` (a Károli-szó
              egyik gépi párja sem egyezik a forrással) · `forrasban_nincs` (a
              szónak nincs Strong-száma a forrásban) · `szovegforma` (a szó nem
              igazítható). Szószinten is: a forrás Strong-halmaza része-e a
              gépi partnerhalmaznak (a régi arany halmaz-definíciója). Kimenet:
              f172/kulso/osszevetes.tsv (a fejezet sorai felülírva; CSAK a mi
              adatunk és az osztály, a forrás Strong-száma és szövege nem), és az
              eltérések vak Opus-ítéletének bemenete:
              f172/ellenor/bemenet/kulso_<könyv>_<fejezet>.txt.

Használat: python eszkozok/karoli_strong/pontossag_kulso.py --fejezetek
           python eszkozok/karoli_strong/pontossag_kulso.py --osszevet <fájl> --fejezet "3Móz 3"
"""

import argparse
import difflib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import pontossag_minta as pm  # noqa: E402
import tokenek  # noqa: E402

KULSO = os.path.join(pm.GYOKER, 'f172', 'kulso')


def kjv_szam():
    """{Károli-igehely: KJV 'fejezet:vers'} a KJV-osztályú sorokból."""
    d = {}
    with open(tokenek.VERSMEGF, encoding='utf-8') as f:
        fej = None
        for s in f:
            if s.startswith('#'):
                continue
            m = s.rstrip('\n').rstrip('\r').split('\t')
            if fej is None:
                fej = m
                continue
            r = dict(zip(fej, m))
            d[r['igehely_karoli']] = r['igehely_kjv']
    return d


def azonos_szamozas(v, kjv, usz=False):
    """A versmegfeleltetési tábla csak az ÓSZ-t fedi; az ÚSZ-ben a Károli- és a
    KJV-számozás versszinten azonos (a tábla hiánya nem eltérés)."""
    if v not in kjv:
        return usz
    return kjv[v] == v.rsplit(' ', 1)[1]


def fejezet_of(v):
    konyv, hely = v.rsplit(' ', 1)
    return '%s %s' % (konyv, hely.split(':')[0])


def fejezetek():
    karoli, _ = bemenet._adatok()
    kjv = kjv_szam()
    _, itelet = pm._tabla(os.path.join(pm.KIMENET, 'itelet_par.tsv'))
    # Károli-versek fejezetenként
    fej_versek = {}
    for v in karoli:
        fej_versek.setdefault(fejezet_of(v), []).append(v)
    # KJV-fejezetbe eső Károli-versek (ÓSZ)
    kjv_be = {}
    for v, k in kjv.items():
        if k and ':' in k:
            kjv_be.setdefault('%s %s' % (v.rsplit(' ', 1)[0], k.split(':')[0]), set()).add(v)
    # párok és kezi fejezetenként
    par, tart, kezi = {}, {}, set()
    for k in pm.konyvek():
        _, sorok = pm._tabla(os.path.join(pm.ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            f = fejezet_of(r['vers'])
            par[f] = par.get(f, 0) + 1
            s = r['strong']
            if not (s.startswith('H90') and len(s) == 5):
                tart[f] = tart.get(f, 0) + 1
        _, sz = pm._tabla(os.path.join(pm.ADAT, 'szavak_%s.tsv' % k))
        for r in sz:
            if r['allapot'] == 'fuggoben':
                kezi.add(fejezet_of(r['vers']))
    h2s = tokenek.konyv_hu_to_step()

    def alkalmas(f, usz):
        vv = fej_versek.get(f, [])
        if not (15 <= len(vv) <= 40) or f in kezi:
            return False
        if usz:
            return True
        if any(not azonos_szamozas(v, kjv) for v in vv):
            return False
        return kjv_be.get(f, set()) <= set(vv)

    valasztott, sorok = set(), []
    for rt in pm.RETEGEK:
        usz = rt.startswith('USZ')
        cel = {}
        for r in itelet:
            if r['reteg'] != rt:
                continue
            f = fejezet_of(r['vers'])
            d = cel.setdefault(f, [0, 0, 0])
            d[0] += r['helyes'] == '0' and r['morfema'] == '0'
            d[1] += r['helyes'] == '0'
            d[2] += 1
        jel = [f for f in cel if f not in valasztott and alkalmas(f, usz)]
        if not jel:
            raise SystemExit('nincs alkalmas fejezet: %s' % rt)
        f = sorted(jel, key=lambda f: (-cel[f][0], -cel[f][1], -cel[f][2], f))[0]
        valasztott.add(f)
        konyv, fe = f.rsplit(' ', 1)
        sorok.append([rt, f, '%s.%s' % (h2s[konyv], fe), str(len(fej_versek[f])), str(cel[f][2]), str(cel[f][1]),
                      str(cel[f][0]), str(par.get(f, 0)), str(tart.get(f, 0))])
    os.makedirs(KULSO, exist_ok=True)
    head = pm.git_head()
    with open(os.path.join(KULSO, 'fejezetek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 külső összevetés fejezetei (Bible-Discovery, Strong-os Károli, régies) | '
                'forras=f172/itelet_par.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, adat/karoli_strong/ @ git:%s | '
                'ts=git:%s | manual (determinisztikus kiválasztás); a forrás szövege nem kerül ide\n' % (head, head))
        f.write('\t'.join(['reteg', 'fejezet', 'step', 'versek', 'celpar', 'celpar_elteres', 'celpar_elteres_tartalmi',
                           'par_osszes', 'par_tartalmi']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    for s in sorok:
        print('\t'.join(s))
    print('összes pár: %d, tartalmi: %d' % (sum(int(s[7]) for s in sorok), sum(int(s[8]) for s in sorok)))


_BD_TOK = re.compile(r'[^\W\d_]+|\d+(?:\s*,\s*\d+)*', re.UNICODE)
_BD_MEGJ = re.compile(r'\*\([^)]*\)')
_BD_REF = re.compile(r'^\s*(\d?\s?[^\W\d_]+)\.?\s+(\d+):(\d+)\s*$')
_DUPLA = [('nyny', 'nny'), ('lyly', 'lly'), ('gygy', 'ggy'), ('tyty', 'tty'), ('szsz', 'ssz'),
          ('zszs', 'zzs'), ('cscs', 'ccs'), ('dzdz', 'ddz'), ('cz', 'c')]
OSZTALYOK = ['egyezik', 'masodlagos', 'elter', 'forrasban_nincs', 'szovegforma']
USZ_KONYVEK = ('Mt', 'Mk', 'Luk', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef', 'Fil', 'Kol',
               '1Thessz', '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak', '1Pét', '2Pét',
               '1Ján', '2Ján', '3Ján', 'Júd', 'Jel')


def norm(szo):
    s = szo.casefold()
    for a, b in _DUPLA:
        s = s.replace(a, b)
    return s


def bd_elemez(ut, usz):
    """{igehely: [(szó, {strong int, ...}), ...]} + a sorvégi megjegyzések száma.
    A szó UTÁNI számcsoport a szóhoz tartozik; 0 és igealak-kód eldobva."""
    felso = 5624 if usz else 8674
    versek, akt, megj = {}, None, 0
    with open(ut, encoding='utf-8-sig') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            m = _BD_REF.match(sor)
            if m:
                akt = '%s %s:%s' % (m.group(1).replace(' ', ''), m.group(2), m.group(3))
                versek.setdefault(akt, [])
                continue
            if akt is None or not sor.strip():
                continue
            megj += len(_BD_MEGJ.findall(sor))
            sor = _BD_MEGJ.sub(' ', sor)
            for t in _BD_TOK.findall(sor):
                if t[0].isdigit():
                    if versek[akt]:
                        for x in re.split(r'\s*,\s*', t):
                            n = int(x)
                            if 0 < n <= felso:
                                versek[akt][-1][1].add(n)
                else:
                    versek[akt].append((t, set()))
    return versek, megj


def igazit(sajat, bd):
    """{saját sorszám (1-től): set(strong)}; a nem igazítható szó hiányzik."""
    a = [norm(t) for t in sajat]
    b = [norm(w) for w, _ in bd]
    ki = {}
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1):
                ki[i1 + k + 1] = set(bd[j1 + k][1])
        elif op == 'replace':
            if ''.join(a[i1:i2]) == ''.join(b[j1:j2]):
                u = set()
                for j in range(j1, j2):
                    u |= bd[j][1]
                for i in range(i1, i2):
                    ki[i + 1] = set(u)
            elif i2 - i1 == j2 - j1:
                for k in range(i2 - i1):
                    ki[i1 + k + 1] = set(bd[j1 + k][1])
    return ki


def _strong_int(s):
    return int(s[1:]) if len(s) > 1 and s[1:].isdigit() else None


def _fejezet_parok(fejezet):
    konyv = fejezet.rsplit(' ', 1)[0]
    for k in pm.konyvek():
        _, sorok = pm._tabla(os.path.join(pm.ADAT, 'parok_%s.tsv' % k))
        if sorok and sorok[0]['vers'].rsplit(' ', 1)[0] == konyv:
            return [r for r in sorok if r['vers'].rsplit(':', 1)[0] == fejezet]
    raise SystemExit('nincs pártábla: %s' % konyv)


def osszevet(ut, fejezet):
    ut = os.path.abspath(ut)
    gy = os.path.abspath(pm.GYOKER)
    try:
        belul = os.path.commonpath([ut, gy]) == gy
    except ValueError:
        belul = False
    if belul:
        raise SystemExit('a forrás-fájl a repón belül van: a zárt forrás szövege nem kerülhet a repóba')
    karoli, _ = bemenet._adatok()
    konyv, fsz = fejezet.rsplit(' ', 1)
    bd, megj = bd_elemez(ut, konyv in USZ_KONYVEK)
    versek = sorted((v for v in karoli if v.rsplit(':', 1)[0] == fejezet), key=lambda v: int(v.rsplit(':', 1)[1]))
    hiany = [v for v in versek if v not in bd]
    tobblet = [v for v in bd if v not in set(versek)]
    parok = _fejezet_parok(fejezet)
    sorok_ki, elteres = [], {}
    szam = {o: 0 for o in OSZTALYOK}
    tartalmi_hu = {}
    igazitatlan_szo = nalunk_nincs = 0
    szo = {'reszhalmaz': 0, 'reszben': 0, 'diszjunkt': 0}
    for v in versek:
        tl = tokenek.tokenizal(karoli[v])
        m = igazit(tl, bd[v]) if v in bd else {}
        igazitatlan_szo += sum(1 for i in range(1, len(tl) + 1) if i not in m)
        vp = [r for r in parok if r['vers'] == v and not (r['strong'].startswith('H90') and len(r['strong']) == 5)]
        gepi = {}
        for r in vp:
            gepi.setdefault(int(r['hu_sorszam']), set()).add(_strong_int(r['strong']))
        for r in vp:
            s = r['strong']
            h = int(r['hu_sorszam'])
            tartalmi_hu.setdefault(v, set()).add(h)
            if h not in m:
                o = 'szovegforma'
            elif not m[h]:
                o = 'forrasban_nincs'
            elif _strong_int(s) in m[h]:
                o = 'egyezik'
            elif gepi[h] & m[h]:
                o = 'masodlagos'
            else:
                o = 'elter'
                elteres.setdefault(v, set()).add(h)
            szam[o] += 1
            sorok_ki.append([fejezet, v, r['hu_sorszam'], r['hu_szo'], r['er_sorszam'], s, r['bizonyossag'], o])
        for h, g in gepi.items():
            if m.get(h):
                if m[h] <= g:
                    szo['reszhalmaz'] += 1
                elif m[h] & g:
                    szo['reszben'] += 1
                else:
                    szo['diszjunkt'] += 1
        nalunk_nincs += sum(1 for h, ss in m.items() if ss and h not in tartalmi_hu.get(v, set()))
    os.makedirs(KULSO, exist_ok=True)
    kut = os.path.join(KULSO, 'osszevetes.tsv')
    fej = ['fejezet', 'vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'strong', 'bizonyossag', 'osztaly']
    regi = []
    if os.path.exists(kut):
        _, rr = pm._tabla(kut)
        regi = [[r[k] for k in fej] for r in rr if r['fejezet'] != fejezet]
    head = pm.git_head()
    with open(kut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 külső összevetés (Bible-Discovery, Strong-os Károli HUN modul; zárt licenc, csak '
                'mérésre, a forrás szövege és Strong-számai nem kerülnek ide) | forras=adat/karoli_strong/parok_*.tsv, '
                'a felhasználó repón kívüli bemásolása | ts=git:%s | manual (determinisztikus összevetés; a gépi pár '
                'modell-kimenet, a forrás független címkézés, nem arany)\n' % head)
        f.write('\t'.join(fej) + '\n')
        for x in sorted(regi + sorok_ki, key=lambda x: (x[0], x[1].rsplit(':', 1)[0], int(x[1].rsplit(':', 1)[1]),
                                                       int(x[2]), int(x[4]))):
            f.write('\t'.join(x) + '\n')
    nev = 'kulso_%s_%s' % (konyv, fsz)
    if elteres:
        blokk = [bemenet.versblokk(v, kjv=False) + '\nCÉL (Károli-sorszámok): ' + ', '.join(map(str, sorted(elteres[v])))
                 for v in sorted(elteres, key=lambda v: int(v.rsplit(':', 1)[1]))]
        with open(os.path.join(pm.GYOKER, 'f172', 'ellenor', 'bemenet', nev + '.txt'), 'w', encoding='utf-8',
                  newline='\n') as f:
            f.write('KÖTEG: %s\n\n' % nev + '\n\n'.join(blokk) + '\n')
    n = sum(szam.values())
    print('%s: %d vers (a forrásban: %d; hiányzik: %s; többlet: %s); sorvégi megjegyzés: %d; nem igazított Károli-szó: %d'
          % (fejezet, len(versek), len(bd), hiany or '-', tobblet or '-', megj, igazitatlan_szo))
    print('tartalmi pár %d: ' % n + ', '.join('%s %d' % (o, szam[o]) for o in OSZTALYOK))
    ossz = szam['egyezik'] + szam['masodlagos'] + szam['elter']
    if ossz:
        print('pár: egyezik vagy másodlagos %.2f%% (%d/%d), elter %d; a forrásban Strongos, nálunk tartalmi pár nélküli Károli-szó: %d'
              % (100.0 * (ossz - szam['elter']) / ossz, ossz - szam['elter'], ossz, szam['elter'], nalunk_nincs))
    sz = sum(szo.values())
    if sz:
        print('szó (a forrás Strong-halmaza vs a gépi partnerhalmaz): része %d, részben %d, diszjunkt %d; része: %.2f%% (%d/%d)'
              % (szo['reszhalmaz'], szo['reszben'], szo['diszjunkt'], 100.0 * szo['reszhalmaz'] / sz, szo['reszhalmaz'], sz))
    print('eltérés: %d vers, %d Károli-szó -> f172/ellenor/bemenet/%s.txt' % (len(elteres), sum(len(x) for x in elteres.values()), nev))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fejezetek', action='store_true')
    ap.add_argument('--osszevet')
    ap.add_argument('--fejezet')
    a = ap.parse_args()
    if a.fejezetek:
        fejezetek()
    elif a.osszevet and a.fejezet:
        osszevet(a.osszevet, a.fejezet)
    else:
        ap.error('--fejezetek, vagy --osszevet <fájl> --fejezet "<könyv> <fejezet>"')


if __name__ == '__main__':
    main()
