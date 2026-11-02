#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lektor_kerdesek.py -- F157: a lektori és ellenőrző kérdések közös sémája; motívumonként generált
`naplok/LEKTOR_<ID>.tsv`.

Forrás (első lépcső): `hatar` = `naplok/HATAR_<ID>.md` (F151): a Gépi rész K/N pontjai és a Modelles rész K pontjai;
a „Felhasználói besorolás” K-sorai a `valasz` mezőbe kerülnek (nyitva-ból megvalaszolva), ha a sorban még nincs válasz.
A forrásfájlt csak olvassa. Nem létező vagy kérdés nélküli forrás üres eredmény (jelölt), nem hiba.

A `valasz`, `allapot`, `atvezetes` mezőt a meglévő sorból megőrzi (kerdes_id szerint); a többit újraírja. Írás előtt
összevetés az eredetivel: ha egy megválaszolt/átvezetett sor eltűnne, megáll (nem ír).

I/O: split('\\t') / '\\t'.join(), nem a csv modul (CLAUDE.md). A kérdés sortörései ` ⏎ ` jelre cserélődnek.

    python eszkozok/lektor_kerdesek.py --motivum ISTENTISZT-001 HAMART-001
"""
import argparse
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZOK_REGI = ['kerdes_id', 'forras', 'motivum', 'hely', 'kerdes', 'valaszlehetosegek', 'proveniencia', 'allapot', 'valasz', 'atvezetes']
MEZOK_V2 = MEZOK_REGI + ['cimke']
OSSZEFOGLALO_MEZOK = ['gond', 'javaslat', 'javaslat_tipus', 'osszefoglalo_proveniencia']
JAVASLAT_TIPUSOK = ('konkret', 'nincs', 'hiany', 'dontott')
MEZOK = MEZOK_V2 + OSSZEFOGLALO_MEZOK  # cimke: tartalmi | uzleti | technikai | osztalyozatlan (a felület szűrője; a nem-döntés források tartalmiak)
MEGORZOTT = ['allapot', 'valasz', 'atvezetes']
ALLAPOTOK = ('nyitva', 'megvalaszolva', 'atvezetve')
FORRASOK = ('lektor', 'hatar', 'proza_lefedettseg', 'proza_javaslat', 'dontes', 'motivum_jelolt', 'kiejtes_kalibracio', 'artifact_komment')
# proza_javaslat: a lektor olvasás közben kérdez ("az adatból ez következik, de a lap nem mondja ki -- legyen róla mondat?").
# A lektor prózát NEM ír (DT-F32b); az "igen" válasz a forrásfájl prózai feladata, a mondatot a próza írója írja.
PROZA_VALASZLEHETOSEGEK = 'legyen mondat; nem kell; később'
CIMKEK = ('tartalmi', 'uzleti', 'technikai', 'osztalyozatlan')
SORTORES = ' ⏎ '
MODELLES_KEZDET = '<!-- MODELLES-KEZDET -->'
MODELLES_VEGE = '<!-- MODELLES-VEGE -->'
FEJLEC = ('# GENERÁLT: python eszkozok/lektor_kerdesek.py --motivum %s (F157); kézzel ne szerkeszd, a válasz-mezők a '
          'felületről és a beolvasásból jönnek; forrás: naplok/HATAR_%s.md')

_BLOKK = re.compile(r'^\*\*(K\d+) — (.*)\*\*\s*$')
_GEPI = re.compile(r'^- \*\*([KN]\d+)(?: \([^)]*\))?\*\*\s*(.*)$')
_IGEHELY = re.compile(r'jeloltek\.tsv:\d+`? \(((?:[1-3]\s?)?[^\W\d_]+\.? \d+:\d+(?:[–-]\d+)?)')
_PROV = re.compile(r'^\(proveniencia: (.*)\)\s*$')
_PROV_GEPI = re.compile(r'^\*\(proveniencia: (.*)\)\*\s*$')
_BESOROLAS = re.compile(r'^- (K\d+): (.*)$')


def egysor(s):
    return re.sub(r'\s+', ' ', s.replace('\t', ' ')).strip()


def hely_keres(szoveg):
    m = _IGEHELY.search(szoveg)
    return m.group(1) if m else ''


def hatar_kerdesek(szoveg, motivum):
    """A HATAR_<ID>.md szövegéből a kérdés-sorok (dict-ek; a besorolásból jövő válasz `_besorolas` kulccsal)."""
    sorok = szoveg.replace('\r\n', '\n').split('\n')
    gepi_prov = next((_PROV_GEPI.match(s).group(1) for s in sorok if _PROV_GEPI.match(s)), 'manual')
    if MODELLES_KEZDET in sorok:
        mod_s = sorok.index(MODELLES_KEZDET)
        mod_v = sorok.index(MODELLES_VEGE) if MODELLES_VEGE in sorok else len(sorok)
        gep, mod = sorok[:mod_s], sorok[mod_s + 1:mod_v]
    else:
        gep, mod = sorok, []
    ki = []
    # Gépi rész: felső szintű K/N pontok, a behúzott sorok a folytatás
    i = 0
    while i < len(gep):
        m = _GEPI.match(gep[i])
        if not m:
            i += 1
            continue
        reszek = [m.group(2)]
        i += 1
        while i < len(gep) and gep[i].startswith('  '):
            reszek.append(gep[i].strip().lstrip('- ').strip())
            i += 1
        sz = SORTORES.join(egysor(r) for r in reszek if r.strip())
        ki.append(dict(kerdes_id='hatar:%s:g%s' % (motivum, m.group(1)), forras='hatar', motivum=motivum,
                       hely=hely_keres(sz), kerdes=sz, valaszlehetosegek='', proveniencia=gepi_prov, cimke='tartalmi'))
    # Modelles rész: **Kn — cím** blokkok
    mod_prov = next((_PROV.match(s).group(1) for s in mod if _PROV.match(s)), 'manual')
    besorolas = {}
    be = False
    for s in mod:
        if '**Felhasználói besorolás**' in s:
            be = True
            continue
        if be:
            mb = _BESOROLAS.match(s)
            if mb:
                besorolas[mb.group(1)] = egysor(mb.group(2))
    blokkok, akt = [], None
    for s in mod:
        mb = _BLOKK.match(s)
        if mb:
            akt = [mb.group(1), egysor(mb.group(2)), []]
            blokkok.append(akt)
        elif akt is not None:
            if (s.startswith('*Nem kérdés') or s.startswith('**Felhasználói') or _PROV.match(s)
                    or re.match(r'^\*\*\d+ kérdés', s)):
                akt = None
            elif s.strip():
                akt[2].append(egysor(s))
    for kod, cim, resz in blokkok:
        sz = SORTORES.join([cim] + resz)
        ki.append(dict(kerdes_id='hatar:%s:m%s' % (motivum, kod), forras='hatar', motivum=motivum, hely=hely_keres(sz),
                       kerdes=sz, valaszlehetosegek='', proveniencia=mod_prov, _besorolas=besorolas.get(kod, ''), cimke='tartalmi'))
    return ki


def beolvas(ut):
    """{kerdes_id: sor-dict} a meglévő TSV-ből (a # sorok kihagyva); nincs fájl -> {}."""
    if not os.path.exists(ut):
        return {}
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    if not sorok:
        return {}
    fej = sorok[0].split('\t')
    if fej not in (MEZOK, MEZOK_V2, MEZOK_REGI):
        raise ValueError('%s: váratlan fejléc %r' % (ut, fej))
    ki = {}
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        for m in MEZOK:
            r.setdefault(m, '')
        ki[r['kerdes_id']] = r
    return ki


def _van_valasz(o):
    return bool(o['valasz'] or o['allapot'] != 'nyitva' or o['atvezetes'])


def osszefesul(uj, regi):
    """Az új kérdés-sorokra rátölti a megőrzendő mezőket; -> (sorok, eltűnt megválaszolt azonosítók)."""
    ki = []
    for k in uj:
        r = {m: k.get(m, '') for m in MEZOK}
        o = regi.get(r['kerdes_id'])
        besor = k.get('_besorolas', '')
        if o and _van_valasz(o):
            for m in MEGORZOTT:
                r[m] = o[m]
        else:
            r['allapot'] = 'megvalaszolva' if besor else 'nyitva'
            r['valasz'] = besor
            r['atvezetes'] = ''
        for m in MEZOK:
            r[m] = r[m].replace('\t', ' ').replace('\n', ' ')
        ki.append(r)
    uj_idk = {r['kerdes_id'] for r in ki}
    # a lezárult kártya (állapot `atvezetve`) elhagyható; a még nem átvezetett válasz nem veszhet el
    eltunt = [i for i, o in regi.items() if i not in uj_idk and _van_valasz(o) and o['allapot'] != 'atvezetve']
    return ki, eltunt


def proza_javaslat_sor(motivum, azon, hely, kerdes, adatsor, proveniencia):
    """Egy `proza_javaslat` kérdés-sor. Kötelező: a forrás adatsor megnevezése (`fájl:sor`) és az adat saját proveniencia-sora;
    a kérdés szövege csak kérdez, mondatot nem javasol."""
    if not adatsor.strip() or not proveniencia.strip():
        raise ValueError('proza_javaslat: adatsor és proveniencia kötelező (%s)' % azon)
    r = {m: '' for m in MEZOK}
    r.update(cimke='tartalmi', kerdes_id='proza_javaslat:%s:%s' % (motivum, azon), forras='proza_javaslat', motivum=motivum, hely=hely,
             kerdes=SORTORES.join([egysor(kerdes), 'Adatsor: ' + egysor(adatsor)]), valaszlehetosegek=PROZA_VALASZLEHETOSEGEK,
             proveniencia=proveniencia, allapot='nyitva')
    return r


def tsv_szoveg(motivum, sorok):
    ki = [FEJLEC % (motivum, motivum), '\t'.join(MEZOK)]
    ki += ['\t'.join(r[m] for m in MEZOK) for r in sorok]
    return '\n'.join(ki) + '\n'


def forras_szoveg(motivum, root):
    ut = os.path.join(root, 'naplok', 'HATAR_%s.md' % motivum)
    if not os.path.exists(ut):
        return None
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()


def osszefoglalo_beolvas(motivum, root=ROOT):
    """{kerdes_id: (tipus, gond, javaslat, proveniencia)} a kézi `eszkozok/lektor_felulet/osszefoglalo_<ID>.tsv`-ből; nincs fájl -> {}."""
    ut = os.path.join(root, 'eszkozok', 'lektor_felulet', 'osszefoglalo_%s.tsv' % motivum)
    if not os.path.exists(ut):
        return {}
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [x.rstrip('\r') for x in f.read().split('\n') if x.strip() and not x.startswith('#')]
    fej = sorok[0].split('\t')
    if fej != ['kerdes_id', 'tipus', 'gond', 'javaslat', 'proveniencia']:
        raise ValueError('%s: váratlan fejléc %r' % (ut, fej))
    ki = {}
    for x in sorok[1:]:
        r = dict(zip(fej, x.split('\t')))
        if r['tipus'] not in JAVASLAT_TIPUSOK:
            raise ValueError('%s: ismeretlen típus %r (%s)' % (ut, r['tipus'], r['kerdes_id']))
        if not r['gond'].strip() or not r['javaslat'].strip():
            raise ValueError('%s: üres összefoglaló (%s)' % (ut, r['kerdes_id']))
        if r['kerdes_id'] in ki:
            raise ValueError('%s: kétszer szerepel: %s' % (ut, r['kerdes_id']))
        ki[r['kerdes_id']] = (r['tipus'], r['gond'], r['javaslat'], r['proveniencia'] or 'manual')
    return ki


def osszefoglalo_ra(uj, ossz):
    """Rátölti az összefoglalókat a kérdés-sorokra; ismeretlen kerdes_id az összefoglalóban hiba (elavult sor)."""
    idk = {k['kerdes_id'] for k in uj}
    ismeretlen = [i for i in ossz if i not in idk]
    if ismeretlen:
        raise ValueError('összefoglaló olyan kérdéshez, amely nincs a forrásban: %s' % ', '.join(ismeretlen))
    for k in uj:
        if k['kerdes_id'] in ossz:
            k['javaslat_tipus'], k['gond'], k['javaslat'], k['osszefoglalo_proveniencia'] = ossz[k['kerdes_id']]
    return uj


def kiir(nev, uj, root=ROOT, kimenet=None, ir=True, megj=''):
    """A `LEKTOR_<nev>.tsv` összefésülése a megőrzött mezőkkel és kiírása. ValueError (nem ír), ha válaszolt sor veszne el."""
    kim = kimenet or os.path.join(root, 'naplok')
    ut = os.path.join(kim, 'LEKTOR_%s.tsv' % nev)
    regi = beolvas(ut)
    sorok, eltunt = osszefesul(uj, regi)
    if eltunt:
        raise ValueError('%s: megválaszolt/átvezetett sor tűnne el a forrásból: %s -- nem írok' % (ut, ', '.join(eltunt)))
    for r in sorok:
        if r['forras'] not in FORRASOK:
            raise ValueError('%s: ismeretlen forrás %r' % (r['kerdes_id'], r['forras']))
        if r['allapot'] not in ALLAPOTOK:
            raise ValueError('%s: ismeretlen állapot %r' % (r['kerdes_id'], r['allapot']))
        if r['cimke'] not in CIMKEK:
            raise ValueError('%s: ismeretlen címke %r' % (r['kerdes_id'], r['cimke']))
    szoveg = tsv_szoveg(nev, sorok)
    if ir:
        os.makedirs(kim, exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
    return szoveg, len(sorok), megj


# --- lektor és proza_lefedettseg: a /kiadas kimenete (naplok/KIADAS_<ID>_lektor.md és _lista.md) ----------------------
_LEKTOR_TETEL = re.compile(r'^(\d+)\. \*\*\(([^)]*)\)\*\* (.*)$')
_LISTA_ELEM = re.compile(r'^- ([^:]+): (.*)$')
_IGEHELY_ALAK = re.compile(r'(?:[1-3]\s?)?[^\W\d_]+\.? \d+:\d+(?:[–-]\d+)?')
PROZA_LEFEDETTSEG_VALASZLEHETOSEGEK = 'szándékos; legyen mondat; később'


def lektor_kerdesek(szoveg, motivum):
    """A `lektor` subagent kérdéslistájából (`naplok/KIADAS_<ID>_lektor.md`) a `forras=lektor` sorok: egy számozott tétel egy kérdés,
    a szakasz (`## …`) a `hely`. A kérdés szövege változatlan (a lektor nem javít, a lista csak kérdez)."""
    sorok = szoveg.replace('\r\n', '\n').split('\n')
    prov = next((_PROV.match(x).group(1) for x in sorok if _PROV.match(x)), 'manual')
    ki, szakasz = [], ''
    for x in sorok:
        if x.startswith('## '):
            szakasz = x[3:].strip()
            continue
        if x.strip() == '---':
            break
        m = _LEKTOR_TETEL.match(x)
        if not m:
            continue
        n, kat, txt = m.groups()
        ki.append(dict(kerdes_id='lektor:%s:%s' % (motivum, n), forras='lektor', motivum=motivum, hely=szakasz,
                       kerdes=SORTORES.join(['%s — (%s)' % (szakasz or 'lektori kérdés', kat), egysor(txt)]),
                       valaszlehetosegek='', proveniencia=prov, cimke='tartalmi'))
    return ki


def lista_hianyok(szoveg, motivum):
    """A próza-lefedettség listájából (`naplok/KIADAS_<ID>_lista.md`) a „Név nélküli elemek” (a próza nem nevezi meg) sorai:
    `forras=proza_lefedettseg`. Az egyenetlenség-tábla nem kérdés."""
    ki, bent = [], False
    for x in szoveg.replace('\r\n', '\n').split('\n'):
        if x.startswith('Név nélküli elemek'):
            bent = True
            continue
        if bent and (x.startswith('#') or x.startswith('*')):
            break
        m = _LISTA_ELEM.match(x) if bent else None
        if not m:
            continue
        rovat, elem = m.group(1).strip(), egysor(m.group(2))
        azon = hashlib.sha1(('%s|%s' % (rovat, elem)).encode('utf-8')).hexdigest()[:8]
        ig = _IGEHELY_ALAK.search(elem)
        ki.append(dict(kerdes_id='proza_lefedettseg:%s:%s' % (motivum, azon), forras='proza_lefedettseg', motivum=motivum,
                       hely=ig.group(0) if ig else '',
                       kerdes=SORTORES.join(['A próza nem nevezi meg ezt az adatelemet (%s)' % rovat, elem,
                                            'Szándékos, hogy a lapon nem szerepel, vagy legyen róla mondat?']),
                       valaszlehetosegek=PROZA_LEFEDETTSEG_VALASZLEHETOSEGEK,
                       proveniencia='manual', cimke='tartalmi'))
    return ki


def _fajl(root, nev):
    ut = os.path.join(root, 'naplok', nev)
    if not os.path.exists(ut):
        return None
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()


def general(motivum, root=ROOT, kimenet=None, ir=True):
    """-> (szöveg, sorok száma, megjegyzés): `hatar` (HATAR_<ID>.md), `lektor` és `proza_lefedettseg` (KIADAS_<ID>_lektor.md / _lista.md).
    Ami a forrásfájlból hiányzik, az üres eredmény, nem hiba."""
    sz = forras_szoveg(motivum, root)
    uj = hatar_kerdesek(sz, motivum) if sz is not None else []
    lk = _fajl(root, 'KIADAS_%s_lektor.md' % motivum)
    if lk is not None:
        uj += lektor_kerdesek(lk, motivum)
    li = _fajl(root, 'KIADAS_%s_lista.md' % motivum)
    if li is not None:
        uj += lista_hianyok(li, motivum)
    uj = osszefoglalo_ra(uj, osszefoglalo_beolvas(motivum, root))
    return kiir(motivum, uj, root, kimenet, ir, 'nincs forrásfájl' if (sz is None and lk is None and li is None) else '')


# --- dontes: a DONTESEK.md nyitott (🟡) tételei és a megállt briefek -------------------------------------------------
SZURO_UT = os.path.join('eszkozok', 'lektor_felulet', 'dontes_szuro.tsv')
_ALLAPOT_JEL = ('🟡', '🟢', '✅')
_FELADAT = re.compile(r'#\d+ [A-Z0-9_]+')
_LEZART_ISMERTETO = re.compile(r'feloldva|eldöntve|alkalmazva|✅|kötelező megállások')


def vag(s, n):
    s = egysor(s)
    return s if len(s) <= n else s[:n - 1].rstrip() + '…'


def szuro_beolvas(root=ROOT):
    """{azonosító: címke} a kézi szűrőből (`azonosito`, `cimke`, `megjegyzes`); hiányzó fájl -> {}."""
    ut = os.path.join(root, SZURO_UT)
    if not os.path.exists(ut):
        return {}
    ki = {}
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [x.rstrip('\r') for x in f.read().split('\n') if x.strip() and not x.startswith('#')]
    fej = sorok[0].split('\t')
    for x in sorok[1:]:
        r = dict(zip(fej, x.split('\t')))
        if r['cimke'] not in CIMKEK or r['cimke'] == 'osztalyozatlan':
            raise ValueError('%s: ismeretlen címke %r (%s)' % (SZURO_UT, r['cimke'], r['azonosito']))
        ki[r['azonosito']] = r['cimke']
    return ki


def dontesek_kartyak(szoveg, ts, szuro=None):
    """A DONTESEK.md táblázatából a nyitott (🟡) tételek. A táblázat sorai ` | `-t tartalmazhatnak a szövegben, ezért az állapot-oszlopot
    az első, emojival kezdődő cella adja (nem az oszlopszám)."""
    szuro = szuro or {}
    ki = []
    for ln, sor in enumerate(szoveg.replace('\r\n', '\n').split('\n'), 1):
        if not sor.startswith('| DT'):
            continue
        m = [x.strip() for x in sor.strip().strip('|').split(' | ')]
        if len(m) < 4:
            continue
        ai = next((i for i in range(3, len(m)) if m[i].startswith(_ALLAPOT_JEL)), None)
        if ai is None or not m[ai].startswith('🟡'):
            continue
        azon, feladat, kerdes = m[0], m[1], m[2]
        kozep = m[3:ai]
        opciok = kozep[0] if kozep else ''
        javaslat = ' | '.join(kozep[1:]) if len(kozep) > 1 else ''
        szoveg_k = [vag(feladat, 160) + ' — ' + azon, vag(kerdes, 700)]
        if opciok and opciok != '—':
            szoveg_k.append('Lehetőségek: ' + vag(opciok, 500))
        if javaslat and javaslat != '—':
            szoveg_k.append('Javaslat: ' + vag(javaslat, 400))
        mot = _FELADAT.search(feladat)
        ki.append(dict(kerdes_id='dontes:%s' % azon, forras='dontes', motivum=mot.group(0) if mot else 'DONTESEK', hely='',
                       kerdes=SORTORES.join(szoveg_k), valaszlehetosegek=vag(opciok, 300) if opciok != '—' else '',
                       proveniencia='scope=DONTESEK.md:%d | forras=lektor_kerdesek.py | ts=%s' % (ln, ts),
                       cimke=szuro.get(azon, 'osztalyozatlan')))
    return ki


def brief_fejlec(szoveg):
    f = {}
    sorok = szoveg.replace('\r\n', '\n').split('\n')
    if not sorok or sorok[0].strip() != '---':
        return f, sorok
    for x in sorok[1:]:
        if x.strip() == '---':
            break
        if ':' in x and not x.startswith(' '):
            k, v = x.split(':', 1)
            f[k.strip()] = v.strip().strip('"')
    return f, sorok


def megallt_briefek(root, ts, szuro=None):
    """A `megallt` / `dontesre_var` állapotú briefek kártyái: a fejléc `kovetkezo` mezője (aki karbantartja, naprakész) és a ⛔ sorok
    gépi kivonata (nem szűrt: a lezárt pontokat a kulcsszavak alapján kihagyja)."""
    szuro = szuro or {}
    ki = []
    for fn in sorted(os.listdir(root)):
        if not re.match(r'^F\d+_.*_BRIEF\.md$', fn):
            continue
        with open(os.path.join(root, fn), encoding='utf-8', newline='') as f:
            fej, sorok = brief_fejlec(f.read())
        if fej.get('allapot') not in ('megallt', 'dontesre_var'):
            continue
        szam, kod = fej.get('feladat', ''), fej.get('kod', fn)
        azon = 'F%s' % szam
        pontok = []
        for i, x in enumerate(sorok, 1):
            if '⛔' in x and not _LEZART_ISMERTETO.search(x) and not x.startswith(('kovetkezo:', 'ad:', 'olvas:')):
                pontok.append('%s:%d %s' % (fn, i, vag(x.lstrip('-*# 0123456789.'), 200)))
        sz = ['#%s %s — megállt brief (%s)' % (szam, kod, fej.get('allapot')),
              'Következő lépés (a brief fejléce): ' + vag(fej.get('kovetkezo', '(nincs)'), 600)]
        if pontok:
            sz.append('⛔ pontok (gépi kivonat, nem szűrt; %d, az első 4): ' % len(pontok) + ' ¦ '.join(pontok[:4]))
        ki.append(dict(kerdes_id='dontes:%s' % azon, forras='dontes', motivum='#%s %s' % (szam, kod), hely='',
                       kerdes=SORTORES.join(sz), valaszlehetosegek='',
                       proveniencia='scope=%s (fejléc + ⛔ sorok) | forras=lektor_kerdesek.py | ts=%s' % (fn, ts),
                       cimke=szuro.get(azon, 'osztalyozatlan')))
    return ki


def general_dontes(root=ROOT, kimenet=None, ir=True, ts=None):
    ts = ts or datetime.date.today().isoformat()
    szuro = szuro_beolvas(root)
    with open(os.path.join(root, 'DONTESEK.md'), encoding='utf-8', newline='') as f:
        uj = dontesek_kartyak(f.read(), ts, szuro) + megallt_briefek(root, ts, szuro)
    return kiir('DONTESEK', uj, root, kimenet, ir)


def main():
    ap = argparse.ArgumentParser(description='F157 -- közös lektor-kérdéslista motívumonként')
    ap.add_argument('--motivum', nargs='*', default=[])
    ap.add_argument('--dontes', action='store_true', help='naplok/LEKTOR_DONTESEK.tsv: DONTESEK.md 🟡 tételei + megállt briefek')
    ap.add_argument('--kimenet', default=None, help='alapértelmezés: naplok/')
    args = ap.parse_args()
    for m in args.motivum:
        _sz, n, megj = general(m, ROOT, args.kimenet)
        print('  LEKTOR_%s.tsv: %d kérdés%s' % (m, n, (' (%s)' % megj) if megj else ''), file=sys.stderr)
    if args.dontes:
        _sz, n, _m = general_dontes(ROOT, args.kimenet)
        print('  LEKTOR_DONTESEK.tsv: %d kérdés' % n, file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
