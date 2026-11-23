#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_blokkfej.py -- F231.17: a main-összevetés kapuja: ami a main-en a lapon látszott, az az ágon is látsszon.

Miért kell: a #810 közben a main-en látható adat került le a lapról vagy csukott lenyíló mögé (az „Apparátus és szövegkritika”
a szónézetről, a jelleg-címkék és a forrássor a blokkcím mellől, az üres eredményű blokkok), és egyik teszt sem fogta meg. A
szerkesztő szabálya (2026-11-23): amit a main mutatott, az maradjon látható. Ez a teszt a `merce/blokkfej_alap.tsv`-hez (a main
állapota a `blokkfej.py` rögzített oldallistáján) veti az ág élő lapjait, és bukik, ha a main egy látható vagy csukott eleme az
ágon hiányzik vagy rosszabb láthatósággal áll (látható → csukott → rejtett), kivéve, ha a `merce/blokkfej_kivetel.tsv` indokkal
megnevezi.

Az összevetés elemfajtánként (l. `blokkfej.py`):
  * `blokk`, `forras`: a blokk azonosítója szerint (a cím változása nem bukás, a lista kiírja);
  * `jelleg`: blokk és címke szerint, a címsorban (a lenyílóba vitt címke `jelleg-mashol`: bukás);
  * `megj`, `ures`, `fej`, `tabla`: szöveg szerint; ha az azonos fajtájú elem nincs meg, elég, ha a szöveg betűi az ág lapján ugyanolyan
    láthatósággal állnak (más címsorszint vagy tagolás nem eltűnés).
A darabszámot a `blokk`, `jelleg` és `forras` fajtánál is nézi (egy blokk minden jelleg-címkéje).

Futtatás:
    python eszkozok/teszt_futtat.py --fajl teszt_blokkfej                     # a kapu
    python eszkozok/olvaso_szerver/teszt_blokkfej.py --lista                    # az eltérések listája (a kivételekkel együtt)
    python eszkozok/olvaso_szerver/teszt_blokkfej.py --alap-ment <main worktree> # az alapfájl újraírása a main állapotából
Az alapfájlt csak a main worktree-jéből szabad írni (`git worktree add <út> origin/main`); a fejléce a main commitját rögzíti.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)

import blokkfej as B  # noqa: E402

ALAP = os.path.join(D, 'merce', 'blokkfej_alap.tsv')
KIVETEL = os.path.join(D, 'merce', 'blokkfej_kivetel.tsv')
DB = os.environ.get('PARDES_DB') or os.path.join(GY, 'pardes.db')
try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False
ELO = os.path.exists(DB) and VAN_FLASK
KIVETEL_ALLAPOT = ('átalakítva', 'döntésre vár', 'a main-en sem látszott')


def kivetelek():
    """[(url, fajta, blokk, szoveg, allapot, indok)]; a `*` bármire illik. Üres indok vagy ismeretlen állapot: hiba."""
    ki = []
    for s in B.tsv_olvas(KIVETEL):
        if len(s) != 6:
            raise ValueError('blokkfej_kivetel.tsv: hat oszlop kell: %r' % (s,))
        if s[4] not in KIVETEL_ALLAPOT or len(s[5].strip()) < 20:
            raise ValueError('blokkfej_kivetel.tsv: ismeretlen állapot vagy hiányzó indok: %r' % (s,))
        ki.append(s)
    return ki


def _illik(minta, ertek):
    return minta == '*' or minta == ertek


def kivetel_e(elteres, kiv):
    url, _szint, fajta, blokk, szoveg = elteres[:5]
    for k in kiv:
        if _illik(k[0], url) and _illik(k[1], fajta) and _illik(k[2], blokk) and _illik(k[3], szoveg):
            return k
    return None


def pillanat_szoveg(html):
    """(látható betűk, teljes betűk) a lap olvasói pillanatképéből (a csukott sorok `▸ ` jellel)."""
    from teszt_olvasoi_merce import pillanatkep, CSUKOTT_JEL
    kep = pillanatkep(html).split('\n')
    return (B.betuk(' '.join(s for s in kep if not s.startswith(CSUKOTT_JEL))), B.betuk(' '.join(kep)))


def elteresek(alap, ag, ag_szoveg):
    """A main (alap) látható/csukott elemei közül, ami az ágon hiányzik vagy rosszabb láthatósággal áll.
    `ag`: az ág sorai; `ag_szoveg`: {(url, szint): (látható betűk, teljes betűk)}. Kimenet: [(url, szint, fajta, blokk, szoveg,
    main-láthatóság, ág-állapot)]."""
    def kulcs(s):
        url, szint, fajta, blokk, szoveg = s[:5]
        if fajta in ('blokk', 'forras'):
            return (url, szint, fajta, blokk, '')
        if fajta == 'fej':
            return (url, szint, fajta, '', szoveg)       # a fej a blokkon kívülre vagy más blokkba is kerülhet
        return (url, szint, fajta, blokk, szoveg)

    ag_d = defaultdict(list)
    for s in ag:
        ag_d[kulcs(s)].append(B.RANG[s[5]])
    main_d = defaultdict(list)
    peldany = {}
    for s in alap:
        if s[5] == B.REJTETT:
            continue
        k = kulcs(s)
        main_d[k].append(B.RANG[s[5]])
        peldany.setdefault(k, s)
    ki = []
    for k, rangok in main_d.items():
        url, szint, fajta = k[:3]
        van = sorted(ag_d.get(k, []), reverse=True)
        hiany = []
        for i, r in enumerate(sorted(rangok, reverse=True)):
            if i >= len(van) or van[i] < r:
                hiany.append((r, van[i] if i < len(van) else None))
        if not hiany:
            continue
        if fajta in ('megj', 'ures', 'fej', 'tabla'):
            lat, teljes = ag_szoveg.get((url, szint), ('', ''))
            b = B.betuk(k[4])
            if b and all((b in lat) if r == B.RANG[B.LATHATO] else (b in teljes) for r, _v in hiany):
                continue
        p = peldany[k]
        nev = {2: B.LATHATO, 1: B.CSUKOTT, 0: B.REJTETT}
        for r, v in hiany:
            ki.append((url, szint, fajta, p[3], k[4] if fajta != 'blokk' else p[4], nev[r], nev[v] if v is not None else 'hiányzik'))
    return sorted(set(ki))


def cim_valtozasok(alap, ag):
    """[(blokk, main-cím, ág-cím)]: a blokkcímek átnevezése (tájékoztatás, nem bukás)."""
    m = {(s[3]): s[4] for s in alap if s[2] == 'blokk'}
    a = {(s[3]): s[4] for s in ag if s[2] == 'blokk'}
    return sorted((b, m[b], a[b]) for b in m if b in a and m[b] != a[b])


def ag_allapot():
    lh = B.lapok(B.kliens_gyar(GY, DB))
    return B.sorok(lh), {k: pillanat_szoveg(h) for k, h in lh.items()}


class BlokkfejKapu(unittest.TestCase):
    def test_kivetellista(self):
        kivetelek()                                     # a forma (hat oszlop, ismert állapot, indok) offline is ellenőrizhető

    def test_alapfajl(self):
        s = B.tsv_olvas(ALAP)
        self.assertTrue(s, 'üres alapfájl: %s' % ALAP)
        oldalak = {(u, sz or 'alap') for u, sz in B.OLDALAK}
        self.assertEqual({(x[0], x[1]) for x in s}, oldalak, 'az alapfájl oldalai és a rögzített oldallista eltér: --alap-ment')

    @unittest.skipUnless(ELO, 'nincs pardes.db vagy Flask: az élő összevetés kimarad')
    def test_main_elemei_az_agon(self):
        alap, kiv = B.tsv_olvas(ALAP), kivetelek()
        ag, szoveg = ag_allapot()
        hibak, hasznalt = [], set()
        for e in elteresek(alap, ag, szoveg):
            k = kivetel_e(e, kiv)
            if k:
                hasznalt.add(k)
            else:
                hibak.append(e)
        self.assertFalse(hibak, 'a main-en álló elem az ágon hiányzik vagy lenyíló mögé került (%d):\n%s' % (
            len(hibak), '\n'.join('  %s [%s] %s %s „%s”: %s → %s' % e for e in hibak[:40])))
        felesleges = [k for k in kiv if k not in hasznalt]
        self.assertFalse(felesleges, 'a kivétellista sora már nem illik eltérésre (törlendő):\n%s' % '\n'.join('  %r' % (k,) for k in felesleges))


def _commit(repo):
    """A worktree HEAD-je. A WSL-ből a Windows-oldali worktree `.git` fájlja Windows-utat mutat (a `git` ott nem fut): ekkor a
    `gitdir` útját `/mnt/<meghajtó>/`-ra fordítva a HEAD fájlt olvassa."""
    r = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'], capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout.strip()
    with open(os.path.join(repo, '.git'), encoding='utf-8') as f:
        gd = f.read().split('gitdir:', 1)[1].strip().replace('\\', '/')
    if len(gd) > 1 and gd[1] == ':':
        gd = '/mnt/%s%s' % (gd[0].lower(), gd[2:])
    with open(os.path.join(gd, 'HEAD'), encoding='utf-8') as f:
        return f.read().strip()


def alap_ment(main_repo):
    """Az alapfájl a main worktree állapotából: a `blokkfej.py` egy ideiglenes másolata `-I`-vel fut, hogy a main kódja töltődjön."""
    commit = _commit(main_repo)
    with tempfile.TemporaryDirectory() as t:
        shutil.copy(os.path.join(D, 'blokkfej.py'), t)
        subprocess.run([sys.executable, '-I', os.path.join(t, 'blokkfej.py'), '--repo', main_repo, '--ki', ALAP,
                        '--fejlec', 'GENERÁLT: teszt_blokkfej.py --alap-ment (blokkfej.py); kézzel szerkeszteni tilos',
                        '--fejlec', 'a main állapota: %s; adatbázis: PARDES_DB' % commit], check=True,
                       env=dict(os.environ, PARDES_DB=DB))


def lista():
    alap, kiv = B.tsv_olvas(ALAP), kivetelek()
    ag, szoveg = ag_allapot()
    for e in elteresek(alap, ag, szoveg):
        k = kivetel_e(e, kiv)
        print('\t'.join(e) + '\t' + (('KIVÉTEL: %s — %s' % (k[4], k[5])) if k else 'HIBA'))
    for b, m, a in cim_valtozasok(alap, ag):
        print('cím\t%s\t%s\t→ %s' % (b, m, a))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--alap-ment')
    ap.add_argument('--lista', action='store_true')
    a, maradek = ap.parse_known_args()
    if a.alap_ment:
        alap_ment(a.alap_ment)
    elif a.lista:
        lista()
    else:
        unittest.main(argv=[sys.argv[0]] + maradek)
