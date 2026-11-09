#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_szuro.py -- a Károli-KH fogyasztók közös szűrője (N-F156a, DT-F156q; F177-től a javított táblából).

A `konkordancia/Karoli_kereszthivatkozasok.tsv` a forráshoz hű (nyers) tábla, de a forrásverseinek egy része másik vers
listáját hordozta (N-F156a). Az F177 óta a MEK 00161 kiadással mint második tanúval összevetett, háromszintű
`konkordancia/Karoli_KH_javitott.tsv` az irányadó: a fogyasztók ezen a modulon át csak a `megerositett` szintű sort
veszik át; a `kiesik` és a `jelolt` nem jut a lapra / az indexbe (a `jelolt` a jelöltlistán marad).

  `elfogad(forras, cel)`: igaz, ha a HunKar-tábla (forras, cel) sora `megerositett`. A `cel` a HunKar-tábla
      `Kapcsolódó igehely` oszlopának alakja (pl. `Gen.2.4-Gen.2.5`), a `forras` STEP-alakú (pl. `Gen.1.1`).
  `szint(forras, cel)`: `megerositett` | `kiesik` | `jelolt` | None (a táblában nincs ilyen sor).
  `gyanus_forrasok()`: ARCHÍV — a megszűnt karantén (`Karoli_kereszthivatkozasok_gyanus.tsv`) forrásversei; szűrésre NEM
      használandó (a karantén megszűnt, DT-F177a), csak az archívum tesztjéhez és a történeti hivatkozáshoz marad.
"""
import os

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GYANUS = os.path.join(GYOKER, 'konkordancia', 'Karoli_kereszthivatkozasok_gyanus.tsv')
JAVITOTT = os.path.join(GYOKER, 'konkordancia', 'Karoli_KH_javitott.tsv')
_CACHE = None
_SZINT = None
_RANG = {'megerositett': 0, 'jelolt': 1, 'kiesik': 2}


def _javitott():
    """{(forras, kapcsolodo): szint} a javított táblából; azonos kulcs többször (HunKar-duplikátum): a legjobb szint."""
    global _SZINT
    if _SZINT is None:
        ki = {}
        if os.path.exists(JAVITOTT):
            with open(JAVITOTT, encoding='utf-8', newline='') as f:
                for s in f:
                    if s.startswith('#') or s.startswith('igehely\t'):
                        continue
                    m = s.rstrip('\n').rstrip('\r').split('\t')
                    if len(m) < 3 or not m[0]:
                        continue
                    k = (m[0], m[1])
                    if k not in ki or _RANG.get(m[2], 9) < _RANG.get(ki[k], 9):
                        ki[k] = m[2]
        _SZINT = ki
    return _SZINT


def szint(forras, cel):
    return _javitott().get((forras, cel))


def elfogad(forras, cel):
    """Igaz, ha a (forrásvers, hivatkozás) sor a javított táblában `megerositett`."""
    return _javitott().get((forras, cel)) == 'megerositett'


def gyanus_forrasok():
    """ARCHÍV: a megszűnt karantén forrásversei (l. a modul docstringjét); szűrésre ne használd."""
    global _CACHE
    if _CACHE is None:
        ki = set()
        if os.path.exists(GYANUS):
            with open(GYANUS, encoding='utf-8') as f:
                for s in f:
                    if s.startswith('#') or s.startswith('forras\t'):
                        continue
                    m = s.rstrip('\n').rstrip('\r').split('\t')
                    if m and m[0]:
                        ki.add(m[0])
        _CACHE = ki
    return _CACHE


_MEK_SOROK = None
_STEP_HU = None


def _step_hu():
    """STEP-kód -> magyar rövidítés (Konyv_normalizalo_tabla.tsv 1. és 2. oszlopa)."""
    global _STEP_HU
    if _STEP_HU is None:
        ki = {}
        ut = os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
        if os.path.exists(ut):
            with open(ut, encoding='utf-8', newline='') as f:
                next(f, None)
                for s in f:
                    m = s.rstrip('\n').rstrip('\r').split('\t')
                    if len(m) > 1 and m[0]:
                        ki[m[0]] = m[1]
        _STEP_HU = ki
    return _STEP_HU


def mek_sorok(forras=None):
    """F181 (a jelölt szint beemelése): a javított tábla csak a MEK-ben álló, `megerositett` sorai a HunKar-tábla
    soraival azonos kulcsokkal (`Igehely`, `Kapcsolódó igehely`, `Kapcsolódó igehely magyar megjelenítése`), hogy a
    fogyasztók a HunKar-sorok mellett ezeket is láthassák. A `kiesik` és a `jelolt` sor nem szerepel. A magyar
    megjelenítés a HunKar-tábla alakját követi (pl. `1Móz 18,10`). `forras`: csak az adott forrásvers (STEP-alak)."""
    global _MEK_SOROK
    if _MEK_SOROK is None:
        hu = _step_hu()
        ki = []
        if os.path.exists(JAVITOTT):
            with open(JAVITOTT, encoding='utf-8', newline='') as f:
                for s in f:
                    if s.startswith('#') or s.startswith('igehely\t'):
                        continue
                    m = s.rstrip('\n').rstrip('\r').split('\t')
                    if len(m) < 4 or m[2] != 'megerositett' or m[3] != 'MEK':
                        continue
                    r = m[1].split('.')
                    if len(r) != 3 or r[0] not in hu:
                        continue
                    ki.append({'Igehely': m[0], 'Kapcsolódó igehely': m[1],
                               'Kapcsolódó igehely magyar megjelenítése': '%s %s,%s' % (hu[r[0]], r[1], r[2])})
        _MEK_SOROK = ki
    return [r for r in _MEK_SOROK if forras is None or r['Igehely'] == forras]
