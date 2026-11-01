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
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZOK = ['kerdes_id', 'forras', 'motivum', 'hely', 'kerdes', 'valaszlehetosegek', 'proveniencia', 'allapot', 'valasz', 'atvezetes']
MEGORZOTT = ['allapot', 'valasz', 'atvezetes']
ALLAPOTOK = ('nyitva', 'megvalaszolva', 'atvezetve')
FORRASOK = ('lektor', 'hatar', 'proza_lefedettseg', 'proza_javaslat', 'kiejtes_kalibracio', 'artifact_komment')
# proza_javaslat: a lektor olvasás közben kérdez ("az adatból ez következik, de a lap nem mondja ki -- legyen róla mondat?").
# A lektor prózát NEM ír (DT-F32b); az "igen" válasz a forrásfájl prózai feladata, a mondatot a próza írója írja.
PROZA_VALASZLEHETOSEGEK = 'legyen mondat; nem kell; később'
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
                       hely=hely_keres(sz), kerdes=sz, valaszlehetosegek='', proveniencia=gepi_prov))
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
                       kerdes=sz, valaszlehetosegek='', proveniencia=mod_prov, _besorolas=besorolas.get(kod, '')))
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
    if fej != MEZOK:
        raise ValueError('%s: váratlan fejléc %r' % (ut, fej))
    ki = {}
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
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
    eltunt = [i for i, o in regi.items() if i not in uj_idk and _van_valasz(o)]
    return ki, eltunt


def proza_javaslat_sor(motivum, azon, hely, kerdes, adatsor, proveniencia):
    """Egy `proza_javaslat` kérdés-sor. Kötelező: a forrás adatsor megnevezése (`fájl:sor`) és az adat saját proveniencia-sora;
    a kérdés szövege csak kérdez, mondatot nem javasol."""
    if not adatsor.strip() or not proveniencia.strip():
        raise ValueError('proza_javaslat: adatsor és proveniencia kötelező (%s)' % azon)
    r = {m: '' for m in MEZOK}
    r.update(kerdes_id='proza_javaslat:%s:%s' % (motivum, azon), forras='proza_javaslat', motivum=motivum, hely=hely,
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


def general(motivum, root=ROOT, kimenet=None, ir=True):
    """-> (szöveg, sorok száma, megjegyzés). ValueError (nem ír), ha válaszolt sor veszne el."""
    kim = kimenet or os.path.join(root, 'naplok')
    ut = os.path.join(kim, 'LEKTOR_%s.tsv' % motivum)
    sz = forras_szoveg(motivum, root)
    uj = hatar_kerdesek(sz, motivum) if sz is not None else []
    regi = beolvas(ut)
    sorok, eltunt = osszefesul(uj, regi)
    if eltunt:
        raise ValueError('%s: megválaszolt/átvezetett sor tűnne el a forrásból: %s -- nem írok' % (ut, ', '.join(eltunt)))
    for r in sorok:
        if r['forras'] not in FORRASOK:
            raise ValueError('%s: ismeretlen forrás %r' % (r['kerdes_id'], r['forras']))
        if r['allapot'] not in ALLAPOTOK:
            raise ValueError('%s: ismeretlen állapot %r' % (r['kerdes_id'], r['allapot']))
    szoveg = tsv_szoveg(motivum, sorok)
    if ir:
        os.makedirs(kim, exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
    return szoveg, len(sorok), ('nincs forrásfájl' if sz is None else '')


def main():
    ap = argparse.ArgumentParser(description='F157 -- közös lektor-kérdéslista motívumonként')
    ap.add_argument('--motivum', nargs='+', required=True)
    ap.add_argument('--kimenet', default=None, help='alapértelmezés: naplok/')
    args = ap.parse_args()
    for m in args.motivum:
        _sz, n, megj = general(m, ROOT, args.kimenet)
        print('  LEKTOR_%s.tsv: %d kérdés%s' % (m, n, (' (%s)' % megj) if megj else ''), file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
