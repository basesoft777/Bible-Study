#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dontes_nezet.py -- PR-onkenti dontes- es nyitott-tetel-fajlok: az egyesitett
nezet es a beolvasztas kozos logikaja.

Miert: minden PR a `DONTESEK.md` vegere es a `NYITOTT_FELADATOK.md`-be irt, a
merge utan a `szamkiosztas` Action ugyanazokat a sorokat irta at, ezert minden
nyitott PR ututkozott. Mostantol az ag SAJAT fajlba ir; ket PR soha nem ir
ugyanabba a fajlba.

  dontesek/uj/<ag>.md   a PR uj dontesei: `DONTESEK.md`-beli tablazatsorok
                        (`| DT-F<nn> | ... |`), semmi mas (fejlec- es
                        elvalasztosor nem kell, de nem baj)
  nyitott/uj/<ag>.md    a PR uj nyitott tetelei: `* **N-F<nn> ...` felsorolasi
                        tetelek (tobbsorosak is), szabad sorkoz; tovabba
                        `Utolsó frissítés: …` sor (a fo fajl azonos sora ele
                        fuzodik `; előtte`-lanccal) es `### <datum> (…)` lezart-
                        blokkok a fajl vegen (a `## Lezárva` ala kerulnek)

`<ag>`: az agnev a `claude/` elotag nelkul, a `/` helyett `_` (pl.
`utkozesmentes-dontesek-5643ac`). Veglegesszam (DT<n>, N<n>) ezekben a fajlokban
TILOS (E26); csak helyorzo.

A `szamkiosztas` Action a main-en ELOSZOR beolvasztja oket (a fajlnevek
sorrendjeben) a `DONTESEK.md` tablazatanak vegere, illetve a
`NYITOTT_FELADATOK.md` `<!-- NYITOTT-UJ-HELY -->` jelolesehez, torli a kis
fajlokat, es csak azutan oszt szamot -- egy commitban. A fo fajlok sorvege
(CRLF) megmarad.

Az olvasok (feladatok.py, muhely_allapot.py, feladatterkep.py, emeles.py,
terv_atnezes.py, E27) az EGYESITETT nezetet latjak: `dontesek_szoveg()`,
`nyitott_szoveg()`.
"""

import glob
import os

DONTES_MAPPA = 'dontesek/uj'
NYITOTT_MAPPA = 'nyitott/uj'
NYITOTT_JELOLES = '<!-- NYITOTT-UJ-HELY -->'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _olvas(ut):
    with open(ut, 'rb') as f:
        return f.read().decode('utf-8')


def uj_fajlok(gyoker, mappa):
    """A mappa .md fajljai, fajlnev szerint rendezve (relativ, '/'-es utak)."""
    ki = sorted(glob.glob(os.path.join(gyoker, *mappa.split('/'), '*.md')))
    return [os.path.relpath(f, gyoker).replace(os.sep, '/') for f in ki]


def _eol(szoveg):
    """A fo fajl sorvege (a repo .md fajljai CRLF-esek): ehhez igazodik a beszurt szoveg."""
    return '\r\n' if '\r\n' in szoveg else '\n'


def _fej_vagy_elvalaszto(sor):
    """A tablazat fejlec- es elvalasztosora (a beolvasztas kihagyja)."""
    s = sor.strip()
    if not s.startswith('|'):
        return False
    return s.startswith('| #') or set(s.replace(' ', '')) <= set('|-:')


def dontes_sorok(szoveg):
    """Az uj-fajl tablazatsorai (a fejlec- es elvalasztosor nelkul)."""
    return [s.rstrip('\r') for s in szoveg.splitlines()
            if s.lstrip().startswith('|') and not _fej_vagy_elvalaszto(s)]


def beolvaszt_dontesek(foszoveg, uj_szovegek):
    """A DONTESEK.md szovege + az uj-fajlok sorai: az utolso tablazatsor utan."""
    sorok = [s for sz in uj_szovegek for s in dontes_sorok(sz)]
    if not sorok:
        return foszoveg
    eol = _eol(foszoveg)
    eredeti = foszoveg.splitlines(keepends=True)
    utolso = max((i for i, s in enumerate(eredeti) if s.lstrip().startswith('|')), default=None)
    uj = [s + eol for s in sorok]
    if utolso is None:
        veg = foszoveg if (foszoveg.endswith('\n') or not foszoveg) else foszoveg + eol
        return veg + ''.join(uj)
    if not eredeti[utolso].endswith('\n'):
        eredeti[utolso] += eol
    return ''.join(eredeti[:utolso + 1] + uj + eredeti[utolso + 1:])


FRISSITES_ELOTAG = 'Utolsó frissítés:'
LEZARVA_FEJLEC = '## Lezárva'


def _nyitott_reszek(szoveg):
    """Egy nyitott/uj fajl hardom resze: (frissites-sorok, tetelek, lezart-blokkok).
    `Utolsó frissítés: …` sor: a fo fajl azonos sora el kerul (elotte-lanc). `### …` sortol a fajl vege:
    a `## Lezárva` fejlec ala kerulo lezart-blokkok. Ami kozte van: a tetelek (a jeloles helyere)."""
    frissites, tetel, lezart = [], [], []
    cel = tetel
    for sor in szoveg.splitlines():
        sor = sor.rstrip('\r')
        if sor.startswith(FRISSITES_ELOTAG):
            frissites.append(sor[len(FRISSITES_ELOTAG):].strip())
        elif sor.startswith('### ') and cel is tetel:
            cel = lezart
            cel.append(sor)
        else:
            cel.append(sor)
    return frissites, '\n'.join(tetel).strip('\n'), '\n'.join(lezart).strip('\n')


def beolvaszt_nyitott(foszoveg, uj_szovegek):
    """A NYITOTT_FELADATOK.md szovege + az uj-fajlok (fajlnev szerinti sorrendben):
      - a tetelek a `<!-- NYITOTT-UJ-HELY -->` jeloles ele (a jeloles sora megmarad; jeloles nelkul az elso
        `## Lezárva` fejlec elo, ennek hianyaban a fajl vegere),
      - a `### …` lezart-blokkok a `## Lezárva` fejlec ala (a regi blokkok ele),
      - az `Utolsó frissítés: X` sorok a fo fajl `Utolsó frissítés:` sorara: `X; előtte <regi>`."""
    eol = _eol(foszoveg)
    frissitesek, tetelek, lezartak = [], [], []
    for sz in uj_szovegek:
        f, t, l = _nyitott_reszek(sz)
        frissitesek += f
        if t:
            tetelek.append(t)
        if l:
            lezartak.append(l)
    if not (frissitesek or tetelek or lezartak):
        return foszoveg
    sorok = foszoveg.splitlines(keepends=True)

    def blokk(szovegek):
        return ''.join(x.replace('\n', eol) + eol for x in szovegek)

    def fejlec_utan(lista, i, szovegek):          # a lista[i] sor UTAN
        if not lista[i].endswith('\n'):
            lista[i] += eol
        lista[i + 1:i + 1] = [blokk(szovegek)]

    if tetelek:
        hely = next((i for i, s in enumerate(sorok) if s.strip() == NYITOTT_JELOLES), None)
        if hely is None:
            hely = next((i for i, s in enumerate(sorok) if s.startswith(LEZARVA_FEJLEC)), len(sorok))
        sorok[hely:hely] = [blokk(tetelek)]
    if lezartak:
        hely = next((i for i, s in enumerate(sorok) if s.startswith(LEZARVA_FEJLEC)), None)
        if hely is None:
            sorok += [eol + LEZARVA_FEJLEC + eol, blokk(lezartak)]
        else:
            fejlec_utan(sorok, hely, lezartak)
    if frissitesek:
        # a kesobbi fajl frissitese kerul elore (mint a kezi „előtte"-lanc)
        uj = '; előtte '.join(reversed(frissitesek))
        hely = next((i for i, s in enumerate(sorok) if s.startswith(FRISSITES_ELOTAG)), None)
        if hely is not None:
            vege = sorok[hely][len(sorok[hely].rstrip('\r\n')):]
            regi = sorok[hely][len(FRISSITES_ELOTAG):].strip()
            sorok[hely] = '%s %s; előtte %s%s' % (FRISSITES_ELOTAG, uj, regi, vege)
    return ''.join(sorok)


def dontesek_szoveg(gyoker=ROOT):
    """A DONTESEK.md egyesitett nezete (a fo fajl + a dontesek/uj/*.md sorai); None, ha nincs fo fajl."""
    ut = os.path.join(gyoker, 'DONTESEK.md')
    if not os.path.exists(ut):
        return None
    uj = [_olvas(os.path.join(gyoker, f)) for f in uj_fajlok(gyoker, DONTES_MAPPA)]
    return beolvaszt_dontesek(_olvas(ut), uj)


def nyitott_szoveg(gyoker=ROOT):
    """A NYITOTT_FELADATOK.md egyesitett nezete; None, ha nincs fo fajl."""
    ut = os.path.join(gyoker, 'NYITOTT_FELADATOK.md')
    if not os.path.exists(ut):
        return None
    uj = [_olvas(os.path.join(gyoker, f)) for f in uj_fajlok(gyoker, NYITOTT_MAPPA)]
    return beolvaszt_nyitott(_olvas(ut), uj)
