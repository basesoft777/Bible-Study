"""dontes_allapot.py — a döntések érvényessége a `DONTESEK.md` (és az ági `dontesek/uj/*.md`) soraiból (F182, F27).

A szabály (a jelölés) egy helyen áll: a `DONTESEK.md` fejének „Állapot” sorában. Röviden: a sor érvénytelen, ha az
„Állapot” cellája ⛔-vel kezdődik; a „Döntés” cella elején a jelölés `**FELÜLÍRVA → DT<n>**` (a felülíró döntés
azonosítójával), `**VISSZAVONVA**` vagy `**OKAFOGYOTT**`. A lapgenerátor érvénytelen döntést nem ír a lapra (a felülíró
döntés jelenik meg), az `ellenoriz.py` 21. szabálya pedig SÉRTÉS, ha a lap érvénytelen döntésre hivatkozik.

Csak standard könyvtár; a táblát `split('|')`-szal olvassa (a cellák szabad szövegét nem értelmezi).
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERVENYTELEN_JEL = '⛔'
UTOD_RX = re.compile(r'\*\*FELÜLÍRVA\s*→\s*(DT-?F?\d+[a-z]{0,2})\*\*')
OK_RX = re.compile(r'\*\*(FELÜLÍRVA|VISSZAVONVA|OKAFOGYOTT)\b')
SOR_RX = re.compile(r'^\|\s*(DT-?F?\d+[a-z]{0,2})\s*\|')


def _sorok(gyoker):
    ut = os.path.join(gyoker, 'DONTESEK.md')
    fajlok = [ut] if os.path.exists(ut) else []
    uj = os.path.join(gyoker, 'dontesek', 'uj')
    if os.path.isdir(uj):
        fajlok += [os.path.join(uj, n) for n in sorted(os.listdir(uj)) if n.endswith('.md')]
    for f in fajlok:
        with open(f, encoding='utf-8') as be:
            for sor in be:
                if SOR_RX.match(sor):
                    yield sor.rstrip('\r\n')


def betolt(gyoker=GYOKER):
    """{azonosító: {'ervenyes': bool, 'utod': azonosító vagy None, 'ok': str}} minden DT-sorra."""
    ki = {}
    for sor in _sorok(gyoker):
        cellak = [c.strip() for c in sor.strip().strip('|').split(' | ')]
        azon = cellak[0]
        allapot = cellak[5] if len(cellak) > 5 else ''
        dontes = cellak[6] if len(cellak) > 6 else ''
        ervenytelen = allapot.startswith(ERVENYTELEN_JEL)
        m = UTOD_RX.search(dontes)
        o = OK_RX.search(dontes)
        ki[azon] = {'ervenyes': not ervenytelen, 'utod': m.group(1) if (ervenytelen and m) else None,
                    'ok': (o.group(1).lower() if o else ('érvénytelen' if ervenytelen else ''))}
    return ki


def ervenyes_utod(azon, allapot):
    """Az érvényes döntés azonosítója: maga, ha érvényes vagy ismeretlen; a felülíró lánc vége, ha felülírt; None, ha
    érvénytelen és nincs érvényes utódja."""
    latott = set()
    while azon in allapot and not allapot[azon]['ervenyes']:
        if azon in latott:
            return None
        latott.add(azon)
        azon = allapot[azon]['utod']
        if azon is None:
            return None
    return azon
