#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feladatok.py -- F20_BEFOGADAS_BRIEF.md (B1): a brief-fejlecekbol generalt
feladatkovetes.

A gyoker `*_BRIEF.md` fajljainak elso blokkja (`---` kozott, soronkent
`kulcs: ertek`) a feladat adata; a `FELADATOK.md` tablai ebbol generalodnak,
a fuggest gep szamolja (`olvas` / `ir` illesztes). A `beerkezo/` mappa minden
parancsbol kimarad. A `csv` modul nem hasznalhato (CLAUDE.md, F4-0).

Parancsok:
    general         a FELADATOK.md jelolt blokkjainak ujrairasa
    ellenoriz       fejlec-ervenyesseg, egyedi szam, fajlnev-szam egyezes,
                    `modell` == regi `Modell:` sor; --pr-alap REF: a
                    generalt blokkot a PR nem modosithatja (E18)
    fuggesek        levezetett/kezi fuggesek, utkozesek, regi fejlecek
    atvetel         a FELADATOK.md tablajabol allapot + kovetkezo lepes a
                    fejlecekbe (--szaraz: csak kiir)
    kovetkezo_szam  a legnagyobb hasznalt feladatszam + 1

Kilepesi kod: 0 = rendben, 1 = szabalysertes, 2 = hiba.
"""

import argparse
import fnmatch
import glob
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TIPUSOK = ('feladat', 'naplozas', 'dontes', 'archiv')
FAZISOK = ('1', '2', 'folyamat')
ALLAPOTOK = ('nem_indult', 'brief_kell', 'fut', 'dontesre_var', 'megallt', 'lezarva')
MODELLEK = ('sonnet', 'opus', 'haiku')
KULCSOK = ('feladat', 'cim', 'kod', 'tipus', 'fazis', 'modell', 'allapot', 'ad',
           'kovetkezo', 'olvas', 'ir', 'fugg', 'nem_fugg', 'helyi_gep', 'ag', 'pr',
           'forras', 'lezarva_osszegzes')
LISTA_KULCSOK = ('olvas', 'ir', 'fugg', 'nem_fugg')
KOTELEZO = {
    'feladat': ('feladat', 'cim', 'tipus', 'fazis', 'modell', 'allapot', 'ad', 'kovetkezo'),
    'naplozas': ('feladat', 'cim', 'tipus', 'modell', 'allapot', 'ad', 'kovetkezo'),
    'dontes': ('cim', 'tipus', 'modell', 'allapot'),
    'archiv': ('cim', 'tipus', 'modell', 'allapot'),
}

# 4. pont: kozos koordinacios fajlok -- sem fuggest, sem utkozest nem okoznak
KOZOS_FAJLOK = ('FELADATOK.md', 'DONTESEK.md', 'NYITOTT_FELADATOK.md',
                'adat/szotar_szerepek.tsv',
                # regiszterfajlok: minden menet csak a sajat sorat irja (rebase)
                'adat/SEMA.md', 'adat/datasetek.tsv', 'adat/licencek.tsv')

# F39 (DT-F39a-c, DT-F39g): a levezetes szabalyai
# kontextus-olvasas: nem ad sorrendet (konyvtar-prefix = `/`-re vegzodo olvas-bejegyzes + ez a lista)
KONTEXTUS_OLVAS = ('CLAUDE.md', 'BRIEF_SABLON.md', 'MUNKAMENET.md')
# menetenkent egyedi fajlt iro minták: az ir-ir utkozesbol kimaradnak
UTKOZES_KIVETEL = ('naplok/ELLENOR_*', 'naplok/*_zaras.md')
# helyettesito minta az `ir`-ben: nem ad kapcsolatot (az `ellenoriz` figyelmeztet)
HELYETTESITO_IR = ('naplok/', 'naplok/*')

MARKER_KEZDET = '<!-- GENERÁLT-KEZDET: feladatok.py --cel %s -->'
MARKER_VEGE = '<!-- GENERÁLT-VÉGE: feladatok.py --cel %s -->'
CELOK = ('fazis1', 'fazis2', 'folyamat', 'naplozas', 'kesz')

KESZ_NAPOK = 14

ALLAPOT_JEL = {
    'nem_indult': '⬜',
    'brief_kell': '⬜ brief kell',
    'fut': '▶ fut',
    'dontesre_var': '⏸ döntésre vár',
    'megallt': '⛔ megállt',
}


# ---------------------------------------------------------------------------
# fejlec beolvasasa
# ---------------------------------------------------------------------------

def _ertek_lista(nyers):
    """`[a, "b*", c/]` -> ['a', 'b*', 'c/']; idezojel csak glob mintanal."""
    tartalom = nyers.strip()[1:-1]
    elemek = []
    akt = ''
    idezo = None
    for ch in tartalom:
        if idezo:
            if ch == idezo:
                idezo = None
            else:
                akt += ch
        elif ch in ('"', "'"):
            idezo = ch
        elif ch == ',':
            elemek.append(akt)
            akt = ''
        else:
            akt += ch
    elemek.append(akt)
    return [e.strip() for e in elemek if e.strip()]


def fejlec_elemez(szoveg):
    """(fejlec_dict, torzs_szoveg, hibak). Fejlec nelkul: ({}, szoveg, [hiba])."""
    sorok = szoveg.replace('\r\n', '\n').split('\n')
    if sorok and sorok[0].startswith('\ufeff'):
        sorok[0] = sorok[0][1:]
    if not sorok or sorok[0].strip() != '---':
        return {}, szoveg, ['nincs fejléc (az első sor nem `---`)']
    vege = None
    for i in range(1, len(sorok)):
        if sorok[i].strip() == '---':
            vege = i
            break
    if vege is None:
        return {}, szoveg, ['a fejléc nincs lezárva (`---`)']
    fej = {}
    hibak = []
    for n, sor in enumerate(sorok[1:vege], 2):
        if not sor.strip() or sor.lstrip().startswith('#'):
            continue
        m = re.match(r'^([a-z_]+):\s*(.*?)\s*$', sor)
        if not m:
            hibak.append('%d. sor: nem `kulcs: érték`' % n)
            continue
        kulcs, nyers = m.group(1), m.group(2)
        if kulcs not in KULCSOK:
            hibak.append('%d. sor: ismeretlen kulcs: %s' % (n, kulcs))
            continue
        if kulcs in fej:
            hibak.append('%d. sor: kettős kulcs: %s' % (n, kulcs))
            continue
        if kulcs in LISTA_KULCSOK:
            if not (nyers.startswith('[') and nyers.endswith(']')):
                hibak.append('%d. sor: %s értéke lista (`[a, b]`)' % (n, kulcs))
                continue
            elemek = _ertek_lista(nyers)
            if kulcs in ('fugg', 'nem_fugg'):
                try:
                    elemek = [int(e) for e in elemek]
                except ValueError:
                    hibak.append('%d. sor: %s csak egész számokat tartalmazhat' % (n, kulcs))
                    continue
            fej[kulcs] = elemek
        elif kulcs == 'feladat':
            if not re.match(r'^\d+$', nyers):
                hibak.append('%d. sor: a feladat egész szám' % n)
                continue
            fej[kulcs] = int(nyers)
        else:
            fej[kulcs] = nyers
    return fej, '\n'.join(sorok[vege + 1:]), hibak


class Brief(object):
    def __init__(self, fajl, fej, torzs, hibak):
        self.fajl = fajl          # gyokerhez viszonyitott nev
        self.fej = fej
        self.torzs = torzs
        self.hibak = hibak

    @property
    def szam(self):
        return self.fej.get('feladat')

    @property
    def allapot(self):
        return self.fej.get('allapot')

    @property
    def regi(self):
        """4.5: `ir` nelkuli brief nem kerulhet csomagba."""
        return 'ir' not in self.fej


def briefek_beolvas(gyoker=REPO):
    """A gyoker `*_BRIEF.md` fajljai; a `beerkezo/` kimarad (nem is gyoker)."""
    eredmeny = []
    for ut in sorted(glob.glob(os.path.join(gyoker, '*_BRIEF.md'))):
        with open(ut, encoding='utf-8', newline='') as f:
            szoveg = f.read()
        fej, torzs, hibak = fejlec_elemez(szoveg)
        eredmeny.append(Brief(os.path.basename(ut), fej, torzs, hibak))
    return eredmeny


# ---------------------------------------------------------------------------
# ellenorzes
# ---------------------------------------------------------------------------

MODELL_SOR = re.compile(r'Modell:\*{0,2}\s*([^\n]*)', re.IGNORECASE)
MODELL_SZO = re.compile(r'(sonnet|opus|haiku|külső:[\w./-]+)', re.IGNORECASE)


KOZVETLEN_BLOKK = re.compile(
    r'<!-- KOZVETLEN_FUTTATAS -->.*?<!-- /KOZVETLEN_FUTTATAS -->', re.DOTALL)


def kozvetlen_blokk_nelkul(torzs):
    """A nyito prompt blokk adat, nem utasitas: az elemzesek atugrjak (D30)."""
    return KOZVETLEN_BLOKK.sub('', torzs)


def regi_modell(torzs):
    """A regi `Modell:` sor elso modellszava, vagy None."""
    for m in MODELL_SOR.finditer(kozvetlen_blokk_nelkul(torzs)):
        sz = MODELL_SZO.search(m.group(1))
        if sz:
            return sz.group(1).lower()
    return None


def ellenoriz(briefek, gyoker=REPO):
    """Hibak listaja: (fajl, uzenet)."""
    hibak = []
    szamok = {}
    for b in briefek:
        for h in b.hibak:
            hibak.append((b.fajl, h))
        fej = b.fej
        if not fej:
            continue
        tipus = fej.get('tipus')
        if tipus not in TIPUSOK:
            hibak.append((b.fajl, 'tipus érvénytelen: %r' % tipus))
            continue
        for k in KOTELEZO[tipus]:
            if k not in fej or fej[k] == '':
                hibak.append((b.fajl, 'hiányzó kötelező mező: %s' % k))
        if fej.get('allapot') not in ALLAPOTOK and 'allapot' in fej:
            hibak.append((b.fajl, 'allapot érvénytelen: %r' % fej['allapot']))
        if tipus == 'feladat' and 'fazis' in fej and fej['fazis'] not in FAZISOK:
            hibak.append((b.fajl, 'fazis érvénytelen: %r' % fej['fazis']))
        if tipus == 'archiv' and fej.get('allapot') not in (None, 'lezarva'):
            hibak.append((b.fajl, 'archív brief állapota csak `lezarva` lehet'))
        if tipus in ('dontes', 'archiv') and 'feladat' in fej:
            hibak.append((b.fajl, '%s típusú briefnek nincs száma' % tipus))
        modell = fej.get('modell')
        if modell is not None and modell not in MODELLEK and not modell.startswith('külső:'):
            hibak.append((b.fajl, 'modell érvénytelen: %r' % modell))
        rm = regi_modell(b.torzs)
        if rm is not None and modell is not None and rm != modell.lower():
            hibak.append((b.fajl, 'a `modell` (%s) nem egyezik a régi `Modell:` sorral (%s)'
                          % (modell, rm)))
        if fej.get('helyi_gep') not in (None, 'igen', 'nem'):
            hibak.append((b.fajl, 'helyi_gep: igen | nem'))
        m = re.match(r'^F(\d\d)_', b.fajl)
        if m:
            if b.szam is None:
                hibak.append((b.fajl, 'F<nn>_ nevű fájl, de nincs `feladat` mező'))
            elif int(m.group(1)) != b.szam:
                hibak.append((b.fajl, 'a fájlnév száma (%s) nem egyezik a `feladat` mezővel (%s)'
                              % (m.group(1), b.szam)))
        elif b.szam is not None:
            hibak.append((b.fajl, 'számozott brief neve F<nn>_…_BRIEF.md kell legyen'))
        if b.szam is not None:
            szamok.setdefault(b.szam, []).append(b.fajl)
        forras = fej.get('forras')
        if forras:
            fajl = forras.split('#')[0]
            if not os.path.exists(os.path.join(gyoker, fajl)):
                hibak.append((b.fajl, 'a `forras` fájl nem létezik: %s' % fajl))
    for szam, fajlok in sorted(szamok.items()):
        if len(fajlok) > 1:
            hibak.append((', '.join(fajlok), 'kettőzött feladatszám: %d' % szam))
    ismert = set(szamok)
    for b in briefek:
        for k in ('fugg', 'nem_fugg'):
            for n in b.fej.get(k, []):
                if n not in ismert:
                    hibak.append((b.fajl, '%s: nincs ilyen feladat: %d' % (k, n)))
    if not hibak:
        for k in fugg_korok(briefek, main_allapotok(gyoker)):
            hibak.append(('feladatok', 'függési kör (a döntés a felhasználóé): %s'
                          % ' ↔ '.join('#%d' % x for x in k)))
    return hibak


# ---------------------------------------------------------------------------
# main-allapot (git)
# ---------------------------------------------------------------------------

def _git(gyoker, *args):
    p = subprocess.run(('git',) + args, cwd=gyoker, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if p.returncode != 0:
        return None
    return p.stdout.decode('utf-8', 'replace')


def main_ref(gyoker=REPO):
    for ref in ('origin/main', 'main'):
        if _git(gyoker, 'rev-parse', '--verify', '-q', ref) is not None:
            return ref
    return None


def main_allapotok(gyoker=REPO, ref=None):
    """{feladat: allapot} a `ref` (alapertelmezett: origin/main) fejleceibol."""
    ref = ref or main_ref(gyoker)
    if not ref:
        return {}
    lista = _git(gyoker, 'ls-tree', '--name-only', ref)
    if lista is None:
        return {}
    eredmeny = {}
    for nev in lista.split('\n'):
        if not nev.endswith('_BRIEF.md'):
            continue
        szoveg = _git(gyoker, 'show', '%s:%s' % (ref, nev))
        if szoveg is None:
            continue
        fej, _, _ = fejlec_elemez(szoveg)
        if 'feladat' in fej and 'allapot' in fej:
            eredmeny[fej['feladat']] = fej['allapot']
    return eredmeny


def statusz(b, main_all):
    """'kesz' (a main-en lezarva), 'pr' (lezarva, de a main-en meg nem), vagy az allapot.

    Ha a main-nek nincs fejlece a feladatrol (torteneti brief, az atallas
    menete), a lezarva allapot keszkent szamit."""
    if b.allapot != 'lezarva':
        return b.allapot
    if b.szam in main_all and main_all[b.szam] != 'lezarva':
        return 'pr'
    return 'kesz'


# ---------------------------------------------------------------------------
# fuggesek
# ---------------------------------------------------------------------------

def _norm(u):
    u = u.replace('\\', '/')
    return u[2:] if u.startswith('./') else u


def utvonal_egyezik(a, b):
    """4.1: azonos; az egyik konyvtar (`/`-re vegzodik) es a masik alatta van; glob illeszkedik."""
    a, b = _norm(a), _norm(b)
    if a == b:
        return True
    if a.endswith('/') and b.startswith(a):
        return True
    if b.endswith('/') and a.startswith(b):
        return True
    if any(c in a for c in '*?[') and fnmatch.fnmatchcase(b, a):
        return True
    if any(c in b for c in '*?[') and fnmatch.fnmatchcase(a, b):
        return True
    return False


def _kod_elotag(b):
    kod = b.fej.get('kod', '')
    return kod.split()[0].upper() if kod.split() else None


def _kozos(b, ut):
    """4.4: kozos koordinacios fajl vagy a feladat sajat fajlja."""
    ut = _norm(ut)
    if ut in KOZOS_FAJLOK or ut == b.fajl:
        return True
    if ut.startswith('naplok/'):
        nev = os.path.basename(ut).upper()
        elotagok = []
        if b.szam is not None:
            elotagok.append('F%02d_' % b.szam)
        kod = _kod_elotag(b)
        if kod:
            elotagok.append(kod + '_')
        if any(nev.startswith(e) for e in elotagok):
            return True
    return False


def _szurt(b, kulcs):
    return [u for u in b.fej.get(kulcs, []) if not _kozos(b, u)]


def kontextus_olvas(ut):
    """DT-F39g: tag kontextus-olvasas (konyvtar-prefix, CLAUDE.md, ...): nem ad sorrendet."""
    ut = _norm(ut)
    return ut.endswith('/') or ut in KONTEXTUS_OLVAS


def _olvas_szurt(b):
    return [u for u in _szurt(b, 'olvas') if not kontextus_olvas(u)]


def _helyettesito(ut):
    return _norm(ut) in HELYETTESITO_IR


def _ir_szurt(b, utkozeshez=False):
    """Az `ir` utvonalai a kapcsolatokhoz; a helyettesito minta kimarad; ir-ir
    utkozesnel a menetenkent egyedi naplok (UTKOZES_KIVETEL) is."""
    ki = []
    for u in _szurt(b, 'ir'):
        if _helyettesito(u):
            continue
        if utkozeshez and any(fnmatch.fnmatchcase(_norm(u), m) for m in UTKOZES_KIVETEL):
            continue
        ki.append(u)
    return ki


def _elso_egyezes(lista_a, lista_b):
    for x in lista_a:
        for y in lista_b:
            if utvonal_egyezik(x, y):
                return y if not any(c in y for c in '*?[') else x
    return None


def _nem_ad_kapcsolatot(a, b):
    """DT-F39d: a halasztott, brief nelkuli es 2. fazisu `b` nem ad levezetett
    kapcsolatot 1. fazisu `a`-nak."""
    if a.fej.get('fazis') != '1':
        return False
    return (b.allapot == 'brief_kell'
            or b.fej.get('kovetkezo', '').lower().startswith('halasztva')
            or b.fej.get('fazis') == '2')


def _szamol(briefek, main_all=None):
    main_all = main_all or {}
    szamozottak = [b for b in briefek if b.szam is not None]
    by_szam = {b.szam: b for b in szamozottak}
    fugg = {}
    explicit = set()
    for a in szamozottak:
        if statusz(a, main_all) == 'kesz':
            continue
        belso = {}
        nem = set(a.fej.get('nem_fugg', []))
        olv = _olvas_szurt(a)
        for b in szamozottak:
            if b is a or b.szam in nem:
                continue
            if statusz(b, main_all) == 'kesz' or _nem_ad_kapcsolatot(a, b):
                continue
            f = _elso_egyezes(olv, _ir_szurt(b))
            if f:
                belso[b.szam] = ('levezetett', f)
        for n in a.fej.get('fugg', []):
            if n in by_szam and n not in nem:
                explicit.add((a.szam, n))
                if n not in belso:
                    belso[n] = ('kezi', 'kezi')
        fugg[a.szam] = belso

    # kolcsonos levezetett fugges = kizaras (DT-F39g)
    kolcsonos = []
    for a in sorted(fugg):
        for b in sorted(fugg[a]):
            if (b > a and fugg[a][b][0] == 'levezetett' and a in fugg.get(b, {})
                    and fugg[b][a][0] == 'levezetett'
                    and (a, b) not in explicit and (b, a) not in explicit):
                kolcsonos.append((a, b, fugg[a][b][1]))
    teljes = {a: dict(fugg[a]) for a in fugg}   # a kolcsonos elekkel egyutt (korkereseshez)
    for a, b, f in kolcsonos:
        del fugg[a][b]
        del fugg[b][a]

    utkozesek = []
    aktiv = [b for b in szamozottak if statusz(b, main_all) != 'kesz']
    for i, a in enumerate(aktiv):
        for b in aktiv[i + 1:]:
            if _nem_ad_kapcsolatot(a, b) or _nem_ad_kapcsolatot(b, a):
                continue
            f = _elso_egyezes(_ir_szurt(a, True), _ir_szurt(b, True))
            if f:
                utkozesek.append((a.szam, b.szam, f))
    for a, b, f in kolcsonos:
        if not any(x == a and y == b for x, y, _ in utkozesek):
            utkozesek.append((a, b, f))
    utkozesek.sort()

    regiek = []
    for b in aktiv:
        hiany = []
        if 'ir' not in b.fej:
            hiany.append('ir')
        if 'olvas' not in b.fej:
            hiany.append('olvas')
        if hiany:
            regiek.append((b.szam, hiany))

    sorrend = []
    for a, b, f in utkozesek:
        if b in fugg.get(a, {}):
            sorrend.append((b, a, 'függésből'))
        elif a in fugg.get(b, {}):
            sorrend.append((a, b, 'függésből'))
        else:
            sorrend.append((min(a, b), max(a, b), 'számból (a kisebb sorszám előre)'))
    return fugg, utkozesek, regiek, sorrend, kolcsonos, teljes


def fuggesek(briefek, main_all=None):
    """(fuggesek, kizarasok, regiek, sorrend).

    fuggesek: {A: {B: (fajta, forras)}}, fajta = levezetett (iras-olvasas, `*`)
    vagy kezi. kizarasok (`utkozesek`): (A, B, fajl) -- kolcsonos kizaras (`×`),
    nem sorrend: nem futhat egyszerre, de barmelyik mehet elobb."""
    return _szamol(briefek, main_all)[:4]


def kolcsonos_fuggesek(briefek, main_all=None):
    return _szamol(briefek, main_all)[4]


def fugg_korok(briefek, main_all=None):
    """A hibas koroket adja: a kolcsonos (kizarassa alakitott) parok kivetelevel minden
    1-nel nagyobb kor, a kolcsonos elekkel egyutt szamolva (A↔B, A→C, C→B is kor)."""
    _, _, _, _, kolcsonos, teljes = _szamol(briefek, main_all)
    koles = set()
    for a, b, _ in kolcsonos:
        koles.add((a, b))
        koles.add((b, a))
    hibas = []
    for k in korok(teljes):
        # a tiszta kolcsonos elekbol allo komponens (par, lanc, csillag) nem kor
        if any((a, b) not in koles for a in k for b in teljes.get(a, {}) if b in k):
            hibas.append(k)
    return hibas


def korok(fugg):
    """A fuggesi graf (levezetett + kezi) 1-nel nagyobb erosen osszefuggo komponensei."""
    g = {a: set(fugg[a]) for a in fugg}
    idx, low, verem, vanon, eredmeny, szamlalo = {}, {}, [], set(), [], [0]

    def be(v):
        idx[v] = low[v] = szamlalo[0]
        szamlalo[0] += 1
        verem.append(v)
        vanon.add(v)
        for w in g.get(v, ()):
            if w not in g:
                continue
            if w not in idx:
                be(w)
                low[v] = min(low[v], low[w])
            elif w in vanon:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            komp = []
            while True:
                w = verem.pop()
                vanon.discard(w)
                komp.append(w)
                if w == v:
                    break
            if len(komp) > 1:
                eredmeny.append(sorted(komp))

    for v in sorted(g):
        if v not in idx:
            be(v)
    return sorted(eredmeny)


def figyelmeztetesek(briefek, main_all=None):
    """[(fajl, uzenet)]: nem hiba, de javitando (DT-F39c, DT-F39d)."""
    main_all = main_all or {}
    by_szam = {b.szam: b for b in briefek if b.szam is not None}
    ki = []
    for b in briefek:
        if b.szam is None or statusz(b, main_all) == 'kesz':
            continue
        for u in b.fej.get('ir', []):
            if _helyettesito(u):
                ki.append((b.fajl, 'az `ir` helyettesítő mintát tartalmaz (%s): adj meg konkrét fájlt'
                           % u))
        if b.fej.get('fazis') == '1':
            for n in b.fej.get('fugg', []):
                c = by_szam.get(n)
                if c is not None and c.fej.get('fazis') == '2' and statusz(c, main_all) != 'kesz':
                    ki.append((b.fajl, 'az 1. fázisú feladat explicit függése 2. fázisúra (#%d): '
                               'a D1 szerint a render nem tarthatja vissza az adatréteget' % n))
    return ki


def jeloltek(briefek, main_all=None):
    """{szam: None | ok}: az 1. fazis feladatai; None = jelolt, kulonben a kihagyas oka.

    Jelolt: nem_indult / dontesre_var, a `kovetkezo` nem `Te:` es nem `halasztva`, nincs
    helyi gep, minden fuggese kesz, es nincs FUTO (▶) kizar-parja."""
    main_all = main_all or {}
    fugg, utk, _, _, _, _ = _szamol(briefek, main_all)
    by_szam = {b.szam: b for b in briefek if b.szam is not None}
    eredmeny = {}
    for b in sorted(by_szam.values(), key=lambda x: x.szam):
        if b.fej.get('tipus') != 'feladat' or b.fej.get('fazis') != '1':
            continue
        if statusz(b, main_all) == 'kesz':
            continue
        kov = b.fej.get('kovetkezo', '')
        ok = None
        if b.allapot not in ('nem_indult', 'dontesre_var'):
            ok = 'állapot: %s' % b.allapot
        elif kov.startswith('Te:'):
            ok = 'a következő lépés a felhasználóé (Te:)'
        elif kov.lower().startswith('halasztva'):
            ok = 'halasztva'
        elif b.fej.get('helyi_gep') == 'igen':
            ok = 'helyi gép kell'
        else:
            var = sorted(n for n in fugg.get(b.szam, {})
                         if n in by_szam and statusz(by_szam[n], main_all) != 'kesz')
            if var:
                ok = 'vár: ' + ', '.join('#%d' % n for n in var)
            else:
                futo = sorted((y if x == b.szam else x) for x, y, _ in utk
                              if b.szam in (x, y)
                              and by_szam[y if x == b.szam else x].allapot == 'fut'
                              and statusz(by_szam[y if x == b.szam else x], main_all) != 'kesz')
                if futo:
                    ok = 'kizár (futó): ' + ', '.join('#%d' % n for n in futo)
        eredmeny[b.szam] = ok
    return eredmeny


def csomag(briefek, main_all=None, legfeljebb=5):
    """A jeloltekbol csomag: a kisebb sorszam elore; kizar-par nem kerul egy csomagba,
    a csomag tagja nem fugg a csomag masik tagjatol; `ir` nelkuli (regi) csak egyedul."""
    main_all = main_all or {}
    fugg, utk, regiek, _, _, _ = _szamol(briefek, main_all)
    regi = set(n for n, _ in regiek)
    kizar = set()
    for a, b, _ in utk:
        kizar.add((a, b))
        kizar.add((b, a))
    tagok = []
    for n, ok in sorted(jeloltek(briefek, main_all).items()):
        if ok is not None:
            continue
        if any((n, t) in kizar or t in fugg.get(n, {}) or n in fugg.get(t, {}) for t in tagok):
            continue
        if n in regi and tagok:
            continue
        tagok.append(n)
        if len(tagok) >= legfeljebb or n in regi:
            break
    return tagok


def fuggesek_szoveg(briefek, main_all=None):
    fugg, utkozesek, regiek, sorrend, kolcsonos, _ = _szamol(briefek, main_all)
    sorok = ['# típus\tfeladat\tmásik\tforrás']
    for a in sorted(fugg):
        for b in sorted(fugg[a]):
            fajta, forras = fugg[a][b]
            sorok.append('FUGGES\t%d\t%d\t%s%s' % (a, b, forras,
                                                    '*' if fajta == 'levezetett' else ''))
    for a, b, f in utkozesek:
        sorok.append('KIZAR\t%d\t%d\t%s\t×' % (a, b, f))
    for a, b, f in kolcsonos:
        sorok.append('FIGYELEM\t%d\t%d\tkölcsönös függés: #%d ↔ #%d, fájl: %s' % (a, b, a, b, f))
    for a, b, ok in sorrend:
        sorok.append('SORREND\t%d\t%d\t%s' % (a, b, ok))
    for k in fugg_korok(briefek, main_all):
        sorok.append('KOR\t%s\t-\tfüggési kör' % ' '.join(str(x) for x in k))
    for a, hiany in regiek:
        sorok.append('REGI\t%d\t-\t%s hiányzik' % (a, ', '.join(hiany)))
    return '\n'.join(sorok) + '\n'


# ---------------------------------------------------------------------------
# generalas
# ---------------------------------------------------------------------------

def _cella(s):
    return str(s).replace('|', '\\|').replace('\n', ' ').strip()


def _fugg_cella(b, fugg, by_szam, main_all):
    jelek = {}
    for n, (fajta, _) in fugg.get(b.szam, {}).items():
        jelek[n] = '#%d*' % n if fajta == 'levezetett' else '#%d' % n
    for n in b.fej.get('fugg', []):
        if n in by_szam and n not in b.fej.get('nem_fugg', []):
            if statusz(by_szam[n], main_all) == 'kesz':
                jelek[n] = '#%d (kész)' % n
    if not jelek:
        return '—'
    return ', '.join(jelek[n] for n in sorted(jelek))


def _hol(b):
    return '`%s`' % b.fej['forras'] if 'forras' in b.fej else '`%s`' % b.fajl


def _allapot_cella(b, main_all):
    st = statusz(b, main_all)
    if st == 'pr':
        return '🔀 PR-ben'
    return ALLAPOT_JEL[st]


def _tabla(briefek, fugg, by_szam, main_all, fejlec):
    if not briefek:
        return '*(nincs nyitott feladat)*'
    sorok = ['| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | %s | Hol |' % fejlec,
             '|---|---|---|---|---|---|---|']
    for b in sorted(briefek, key=lambda x: x.szam):
        cim = b.fej['cim'] + (' (%s)' % b.fej['kod'] if 'kod' in b.fej else '')
        sorok.append('| %d | %s | %s | %s | %s | %s | %s |' % (
            b.szam, _cella(cim), _cella(b.fej['ad']), _allapot_cella(b, main_all),
            _cella(_fugg_cella(b, fugg, by_szam, main_all)),
            _cella(b.fej['kovetkezo']), _hol(b)))
    return '\n'.join(sorok)


def _merge_info(gyoker, b):
    """(rovid_hash, datum) az `allapot: lezarva` fejlecsor bekerulesenek first-parent MERGE-commitjabol."""
    ki = _git(gyoker, 'log', '--first-parent', '--merges', '-G', '^allapot: lezarva$',
              '--format=%h %cs', '--', b.fajl)
    if not ki or not ki.strip():
        return None, None
    utolso = ki.strip().split('\n')[-1].split()
    return utolso[0], utolso[1]


def _osszegzes_datum(szoveg, ma):
    """A `lezarva_osszegzes` elso `HH.NN` alaku, zarojelben allo datuma (a korabban, kezzel
    vezetett tetelek merge-datuma); a `git log` az atallas merge-datumat adna. None, ha nincs."""
    m = re.search(r'\((?:[^()]*, )?(\d{2})\.(\d{2})\)', szoveg)
    if not m:
        return None
    try:
        d = date(ma.year, int(m.group(1)), int(m.group(2)))
    except ValueError:
        return None
    if d > ma:
        d = date(ma.year - 1, d.month, d.day)
    return d


def blokkok(briefek, gyoker=REPO, ma=None, main_all=None):
    """{cel: szoveg} a generalt blokkok tartalma."""
    ma = ma or date.today()
    if main_all is None:
        main_all = main_allapotok(gyoker)
    szamozottak = [b for b in briefek if b.szam is not None and b.fej]
    by_szam = {b.szam: b for b in szamozottak}
    fugg, _, _, _ = fuggesek(briefek, main_all)
    nyitott = [b for b in szamozottak
               if b.fej.get('tipus') == 'feladat' and statusz(b, main_all) != 'kesz']

    def fazis(f):
        return [b for b in nyitott if b.fej.get('fazis') == f]

    kimenet = {
        'fazis1': _tabla(fazis('1'), fugg, by_szam, main_all, 'Következő lépés'),
        'fazis2': _tabla(fazis('2'), fugg, by_szam, main_all, 'Megjegyzés'),
        'folyamat': _tabla(fazis('folyamat'), fugg, by_szam, main_all, 'Következő lépés'),
    }
    napl = [b for b in szamozottak if b.fej.get('tipus') == 'naplozas'
            and statusz(b, main_all) != 'kesz']
    kimenet['naplozas'] = '\n'.join(
        '- #%d %s — %s — %s (`%s`)' % (b.szam, b.fej['cim'], _allapot_cella(b, main_all),
                                      b.fej['kovetkezo'], b.fajl)
        for b in sorted(napl, key=lambda x: x.szam)) or '*(nincs nyitott naplózás)*'

    keszek = []
    for b in szamozottak:
        if b.fej.get('tipus') not in ('feladat', 'naplozas'):
            continue
        if statusz(b, main_all) != 'kesz':
            continue
        h, d = _merge_info(gyoker, b)
        szoveg_datum = _osszegzes_datum(b.fej.get('lezarva_osszegzes', ''), ma)
        if szoveg_datum:
            datum = szoveg_datum
        elif d:
            datum = datetime.strptime(d, '%Y-%m-%d').date()
        else:
            datum = ma
        if ma - datum > timedelta(days=KESZ_NAPOK):
            continue
        szoveg = b.fej.get('lezarva_osszegzes', '').strip()
        if not szoveg:
            szoveg = b.fej['ad']
        if h and 'merge' not in szoveg:
            szoveg += ' (merge `%s`, %s)' % (h, d)
        jel = '#%d' % b.szam + (', %s' % b.fej['kod'] if 'kod' in b.fej else '')
        keszek.append((datum, b.szam, '- %s (%s): %s' % (b.fej['cim'], jel, szoveg)))
    keszek.sort(key=lambda x: (x[0], x[1]), reverse=True)
    kimenet['kesz'] = '\n'.join(k[2] for k in keszek) or '*(nincs a legutóbbi két hétben)*'
    return kimenet


def blokk_csere(szoveg, cel, tartalom):
    kezd = MARKER_KEZDET % cel
    vege = MARKER_VEGE % cel
    i = szoveg.find(kezd)
    j = szoveg.find(vege)
    if i < 0 or j < 0 or j < i:
        raise ValueError('hiányzó jelölő a FELADATOK.md-ben: %s' % cel)
    return szoveg[:i + len(kezd)] + '\n' + tartalom + '\n' + szoveg[j:]


def generalt_blokkok_kivon(szoveg):
    """{cel: tartalom} a meglevo jelolok kozul; ures, ha nincs jelolo."""
    eredmeny = {}
    for cel in CELOK:
        kezd = MARKER_KEZDET % cel
        vege = MARKER_VEGE % cel
        i = szoveg.find(kezd)
        j = szoveg.find(vege)
        if i >= 0 and j > i:
            eredmeny[cel] = szoveg[i + len(kezd):j]
    return eredmeny


def general(gyoker=REPO, ma=None, szaraz=False, main_all=None):
    """Ujrairja a FELADATOK.md generalt blokkjait. Visszaad: True, ha valtozott."""
    briefek = briefek_beolvas(gyoker)
    hibak = ellenoriz(briefek, gyoker)
    if hibak:
        raise ValueError('a fejlécek érvénytelenek, előbb `ellenoriz`: %s: %s' % hibak[0])
    ut = os.path.join(gyoker, 'FELADATOK.md')
    with open(ut, encoding='utf-8', newline='') as f:
        regi = f.read()
    uj = regi
    for cel, tartalom in blokkok(briefek, gyoker, ma, main_all).items():
        uj = blokk_csere(uj, cel, tartalom)
    if uj != regi and not szaraz:
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(uj)
    return uj != regi


# ---------------------------------------------------------------------------
# atvetel
# ---------------------------------------------------------------------------

def _allapot_visszafejt(cella):
    c = cella.strip()
    if c.startswith('✅'):
        return 'lezarva'
    if c.startswith('▶'):
        return 'fut'
    if c.startswith('⏸'):
        return 'dontesre_var'
    if c.startswith('⛔'):
        return 'megallt'
    if c.startswith('⬜'):
        return 'brief_kell' if 'brief kell' in c else 'nem_indult'
    if c.startswith(('🔀', '\U0001F50E', '\U0001F50D')):  # a két nagyító a korábbi jel
        return 'lezarva'
    return None


def tabla_sorok(szoveg):
    """{szam: (allapot, kovetkezo)} a FELADATOK.md tablainak `| # | … |` soraibol."""
    eredmeny = {}
    fej_idx = None
    for sor in szoveg.split('\n'):
        if not sor.startswith('|'):
            fej_idx = None
            continue
        cellak = [c.strip() for c in re.split(r'(?<!\\)\|', sor.strip())[1:-1]]
        if cellak and cellak[0] == '#':
            try:
                fej_idx = (cellak.index('Állapot'),
                           next(i for i, c in enumerate(cellak)
                                if c in ('Következő lépés', 'Megjegyzés')))
            except (ValueError, StopIteration):
                fej_idx = None
            continue
        if fej_idx and cellak and re.match(r'^\d+$', cellak[0]) and len(cellak) > max(fej_idx):
            al = _allapot_visszafejt(cellak[fej_idx[0]])
            if al:
                eredmeny[int(cellak[0])] = (al, cellak[fej_idx[1]].replace('\\|', '|'))
    return eredmeny


def _fej_sor_csere(szoveg, kulcs, ertek):
    """A fejlec `kulcs:` sorat cseréli (vagy a fejlec vegere teszi)."""
    sorok = szoveg.split('\n')
    vege = None
    for i in range(1, len(sorok)):
        if sorok[i].strip() == '---':
            vege = i
            break
    for i in range(1, vege):
        if sorok[i].startswith(kulcs + ':'):
            sorok[i] = '%s: %s' % (kulcs, ertek)
            return '\n'.join(sorok)
    sorok.insert(vege, '%s: %s' % (kulcs, ertek))
    return '\n'.join(sorok)


def atvetel(gyoker=REPO, forras=None, szaraz=False):
    """A tabla allapotat es kovetkezo lepeset a fejlecekbe irja. Visszaad: a valtozasok listaja."""
    ut = forras or os.path.join(gyoker, 'FELADATOK.md')
    with open(ut, encoding='utf-8') as f:
        sorok = tabla_sorok(f.read())
    valtozasok = []
    for b in briefek_beolvas(gyoker):
        if b.szam not in sorok or not b.fej:
            continue
        al, kov = sorok[b.szam]
        with open(os.path.join(gyoker, b.fajl), encoding='utf-8', newline='') as f:
            szoveg = f.read()
        uj = szoveg
        crlf = '\r\n' in szoveg
        if crlf:
            uj = uj.replace('\r\n', '\n')
        if b.fej.get('allapot') != al:
            uj = _fej_sor_csere(uj, 'allapot', al)
            valtozasok.append((b.fajl, 'allapot', b.fej.get('allapot'), al))
        if kov and b.fej.get('kovetkezo') != kov:
            uj = _fej_sor_csere(uj, 'kovetkezo', kov)
            valtozasok.append((b.fajl, 'kovetkezo', b.fej.get('kovetkezo'), kov))
        if crlf:
            uj = uj.replace('\n', '\r\n')
        if uj != szoveg and not szaraz:
            with open(os.path.join(gyoker, b.fajl), 'w', encoding='utf-8', newline='') as f:
                f.write(uj)
    return valtozasok


# ---------------------------------------------------------------------------
# kovetkezo szam, PR-ellenorzes
# ---------------------------------------------------------------------------

def kovetkezo_szam(briefek):
    hasznalt = [b.szam for b in briefek if b.szam is not None]
    for b in briefek:
        m = re.match(r'^F(\d\d)_', b.fajl)
        if m:
            hasznalt.append(int(m.group(1)))
    return (max(hasznalt) if hasznalt else 0) + 1


def extra_hozzaad(briefek, utak):
    """A befogadando brief(ek) javasolt fejlecet a szamitashoz hozzaadja (nem ir semmit).

    Szam nelkuli fejlec a kovetkezo szabad szamot kapja (a tobb extra egymas utan)."""
    briefek = list(briefek)
    for ut in utak:
        with open(ut, encoding='utf-8', newline='') as f:
            fej, torzs, hibak = fejlec_elemez(f.read())
        if not fej:
            raise ValueError('az --extra fájlnak fejléc kell: %s (%s)' % (ut, '; '.join(hibak)))
        if 'feladat' not in fej and fej.get('tipus', 'feladat') in ('feladat', 'naplozas'):
            fej['feladat'] = kovetkezo_szam(briefek)
        if 'feladat' in fej:  # csonk kitoltese: ugyanazon a szamon felvaltja a meglevot
            briefek = [x for x in briefek if x.szam != fej['feladat']]
        briefek.append(Brief(os.path.basename(ut), fej, torzs, hibak))
    return briefek


def pr_blokk_ellenorzes(gyoker, alap_ref):
    """E18: a generalt blokkot a PR nem modosithatja. Hibak listaja.

    Ha az alapon meg nincsenek jelolok (a generalas bevezetese), nincs ellenorzes."""
    alap = _git(gyoker, 'show', '%s:FELADATOK.md' % alap_ref)
    if alap is None:
        return []
    alap_blokkok = generalt_blokkok_kivon(alap)
    if not alap_blokkok:
        return []
    with open(os.path.join(gyoker, 'FELADATOK.md'), encoding='utf-8', newline='') as f:
        fej = generalt_blokkok_kivon(f.read())
    hibak = []
    for cel in CELOK:
        if cel not in fej:
            hibak.append(('FELADATOK.md', 'a generált blokk jelölője hiányzik/törött: %s' % cel))
        elif fej[cel].replace('\r\n', '\n') != alap_blokkok.get(cel, '').replace('\r\n', '\n'):
            hibak.append(('FELADATOK.md', 'a PR módosítja a generált blokkot: %s '
                          '(csak a `main`-re futó Action írhatja)' % cel))
    return hibak


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--gyoker', default=REPO, help='a repó gyökere (teszteléshez)')
    p.add_argument('--ma', help='a mai nap (ÉÉÉÉ-HH-NN), a „Kész” lista kora miatt')
    alp = p.add_subparsers(dest='parancs', required=True)
    alp.add_parser('general', help='a FELADATOK.md jelölt blokkjainak újraírása')
    e = alp.add_parser('ellenoriz', help='fejlécek és blokkok ellenőrzése')
    e.add_argument('--pr-alap', help='az alap ref (pl. origin/main): a generált blokk nem változhat')
    f = alp.add_parser('fuggesek', help='függések, ütközések, régi fejlécek')
    f.add_argument('--extra', action='append', default=[], metavar='FAJL',
                   help='a befogadandó brief javasolt fejléce (a repón kívüli fájl); a számítás '
                        'úgy veszi figyelembe, mintha a repóban lenne; szám nélkül a következő szabad számot kapja')
    alp.add_parser('jeloltek', help='az 1. fázis jelöltjei és a kihagyás okai (nem indít semmit)')
    a = alp.add_parser('atvetel', help='a FELADATOK.md táblájából a fejlécekbe')
    a.add_argument('--szaraz', action='store_true', help='csak kiírja a változásokat')
    alp.add_parser('kovetkezo_szam', help='a következő szabad feladatszám')
    arg = p.parse_args(argv)
    ma = datetime.strptime(arg.ma, '%Y-%m-%d').date() if arg.ma else None

    try:
        if arg.parancs == 'general':
            valtozott = general(arg.gyoker, ma)
            print('FELADATOK.md: %s' % ('frissítve' if valtozott else 'változatlan'))
            return 0
        briefek = briefek_beolvas(arg.gyoker)
        if arg.parancs == 'ellenoriz':
            hibak = ellenoriz(briefek, arg.gyoker)
            if arg.pr_alap:
                hibak += pr_blokk_ellenorzes(arg.gyoker, arg.pr_alap)
            fig = figyelmeztetesek(briefek, main_allapotok(arg.gyoker))
            for fajl, uzenet in hibak:
                print('HIBA\t%s\t%s' % (fajl, uzenet))
            for fajl, uzenet in fig:
                print('FIGYELEM\t%s\t%s' % (fajl, uzenet))
            print('%d brief, %d hiba, %d figyelmeztetés' % (len(briefek), len(hibak), len(fig)))
            return 1 if hibak else 0
        if arg.parancs == 'fuggesek':
            briefek = extra_hozzaad(briefek, arg.extra)
            sys.stdout.write(fuggesek_szoveg(briefek, main_allapotok(arg.gyoker)))
            return 0
        if arg.parancs == 'jeloltek':
            ma_all = main_allapotok(arg.gyoker)
            by = {b.szam: b for b in briefek if b.szam is not None}
            for n, ok in jeloltek(briefek, ma_all).items():
                print('%s\t#%d\t%s' % ('JELOLT' if ok is None else 'KIHAGYVA', n,
                                       by[n].fej.get('cim', '') if ok is None else ok))
            print('CSOMAG\t%s' % ' '.join('#%d' % n for n in csomag(briefek, ma_all)))
            return 0
        if arg.parancs == 'atvetel':
            for fajl, kulcs, regi, uj in atvetel(arg.gyoker, szaraz=arg.szaraz):
                print('%s\t%s\t%s -> %s' % (fajl, kulcs, regi, uj))
            return 0
        if arg.parancs == 'kovetkezo_szam':
            print(kovetkezo_szam(briefek))
            return 0
    except (OSError, ValueError) as ex:
        print('HIBA: %s' % ex, file=sys.stderr)
        return 2
    return 2


if __name__ == '__main__':
    sys.exit(main())
