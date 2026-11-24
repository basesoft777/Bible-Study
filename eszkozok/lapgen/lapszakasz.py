"""lapgen.lapszakasz — egy kész lap címsorának szakaszazonosítója a lapmodell szerint (F241.3, N243 (3)).

A lapszövegre kereső kapuk (`olvasoi_kapu.py`, `proza_1a.py`) a szakaszt ezzel azonosítják, nem a szakasz
számával: a számot a szakaszrend adja (GK-10), és az új lapon más, mint a régi generátor lapján („3. LXX” →
„5. LXX”, HN-17; „1/a.” → „2.1.”; „8. Irodalom” → „12. Irodalom”). Az azonosító a szakaszrendé (`szakaszok.py`), a
cím a B66 sablontábla `cim.<azonosító>` sora, az alrészé a `cim.<azonosító>.<alrész>` sora (pl.
`elofordulasok.szoveg`). A régi generátor lapjainak (befagyasztott lapok; a visszaút) eltérő címei a `REGI_CIMEK`
táblában állnak: ezek a régi szerkezet szakaszai, az új szakaszrendben nincsenek.
"""
import os
import re

from lapgen.szakaszok import Szakaszrend

# A címsor eleji szám: „5. ”, „1/b. ”, „2.1. ”, „4.11. ”, „1/a. ”.
SZAM_RX = re.compile(r'^\d+(?:[./]\d*[a-z]?)*\.?\s+')
# A régi lapok szerzőségi jelölése a címben: „Kivonat *(kézi)*”.
SZERZOSEG_RX = re.compile(r'\s*\*\((?:kézi|generált)\)\*\s*$')

# A cím → azonosító térkép kiegészítése az új szakaszrendben nem létező, régi szakaszokkal és alrészekkel.
REGI_CIMEK = {
    'Alkalmazás és tanítói egyezés': 'alkalmazas',   # a régi 6/b. (DT756: kivezetve)
}
# Az alrészek sablonkulcsai, amelyeket a kapuk azonosítanak (az azonosító a kulcs `cim.` utáni része).
ALRESZ_KULCSOK = ('cim.elofordulasok.szoveg',)

_TERKEP = {}


def cim_alap(cim):
    """A címsor szövege szám és szerzőségi jelölés nélkül („5. LXX-fordítói döntések” → „LXX-fordítói döntések”)."""
    return SZERZOSEG_RX.sub('', SZAM_RX.sub('', (cim or '').strip())).strip()


def terkep(gyoker):
    """{cím (szám nélkül): azonosító} a szakaszrendből és a B66 sablontáblából; gyökérkönyvtáranként egyszer épül."""
    gyoker = os.path.abspath(gyoker)
    if gyoker not in _TERKEP:
        from lapgen import bemenet
        sablonok = bemenet.b66_sablonok(bemenet.Bemenet(gyoker))
        rend = Szakaszrend()
        t = dict(REGI_CIMEK)
        for leiro in rend.mind():
            kulcs = rend.cim_kulcs(leiro.azonosito)
            if sablonok.van(kulcs):
                t[sablonok.sor(kulcs).mondat] = leiro.azonosito
        for kulcs in ALRESZ_KULCSOK:
            t[sablonok.sor(kulcs).mondat] = kulcs[len('cim.'):]
        _TERKEP[gyoker] = t
    return _TERKEP[gyoker]


def azonosito(cim, gyoker):
    """A címsor szakaszazonosítója (pl. `lxx`, `idezes`, `elofordulasok.szoveg`); ismeretlen címre ''."""
    return terkep(gyoker).get(cim_alap(cim), '')
