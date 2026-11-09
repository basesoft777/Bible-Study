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
