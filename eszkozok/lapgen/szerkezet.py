"""lapgen.szerkezet — a pozitív szerkezeti kapu a kész lapon (GK-25 futásidejű része; a GK-26 mutációs próba
kapuja a fajta-térkép nélkül felismerhető hibákra).

Három szabály, a kész sorok látható szövegén (a megjegyzés, a horgony és a szerkezeti jelölés kívül esik):
- a 2.1 pontban minden igehely alatt áll a „Funkció:” sor (a tétel a horgonytól a következő horgonyig tart);
- a táblajegyzet nem ismétli a sora celláját (a jegyzet = cella hiba: a régi `tablajegyzet.ismetlo_jegyzet` esete);
- a táblacella „Címke: indoklás” alakjában az indoklás eleje nem ismétli a címkét (HN-02: „A formula nincs a
  versben: Nincs meg a formula …”; a régi `cimke_ismetles` szabálya).
A szakaszrendet a szakaszmodell adja (GK-10), a kapu csak azt nézi, hogy a számozott címsorok sorszáma folytonos.
"""
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.megjelenites.md.iro import JELOLES, MEGJEGYZES
from lapgen.szoveg import Fajta

_SZAMOZOTT_CIM_RX = re.compile(r'^## (\d+)\. ')
_TETEL_RX = re.compile(r'^<a id="ige-')
_FUNKCIO = 'Funkció: '
_JEGYZET_RX = re.compile(r'^- <span class="lj-szam" id="j-(\d+-\d+)">')
_HIVATKOZAS_RX = re.compile(r'<sup class="lj"><a href="#j-(\d+-\d+)">')
_SZO_RX = re.compile(r'\w+')
_CIMKE_TILTOTT_RX = re.compile(r'[\d\[\]→#(]')
_CELLA_CIMKE_RX = re.compile(r'^([^:|]{3,90}): (.+)$')
_FORRAS_ELOTAG = 'Forrás: '


class SzerkezetHiba(BemenetHiba):
    """BUKÁS: a kész lap szerkezete hibás. A lap nem íródik ki."""


def _lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f not in (MEGJEGYZES, Fajta.HORGONY, JELOLES))


def _cellak(sor):
    """A táblasor celláinak látható szövege (a cellahatár szerkezeti jelölés: a látható darabok közt áll)."""
    cellak, akt, hol = [], [], 0
    for k, v, f in sorted(sor.tartomanyok):
        if f is JELOLES and '|' in sor.szoveg[k:v]:
            if akt:
                cellak.append(''.join(akt).strip())
                akt = []
            continue
        if f not in (MEGJEGYZES, Fajta.HORGONY, JELOLES):
            akt.append(sor.szoveg[k:v])
        hol = v
    if akt:
        cellak.append(''.join(akt).strip())
    return cellak


def _ismetli(cimke, szoveg):
    """Igaz, ha a szöveg eleje (az első nyolc szó) a címke tartalmas szavait ismétli (a régi `cimke_ismetles`)."""
    cim = cimke.strip().lower()
    if not cim or _CIMKE_TILTOTT_RX.search(cim):
        return False
    tobbi = _SZO_RX.findall(szoveg.lower())
    if len(tobbi) < 4:
        return False
    cim_szavai = _SZO_RX.findall(cim)
    if len(cim_szavai) >= 2 and tobbi[:2] == cim_szavai[:2]:
        return True
    # a kimeneti kapu szigorúbb a régi szabálynál: egyetlen közös szó (pl. a címke kulcsszava a meghatározásban)
    # nem ismétlés; legalább két tartalmas szónak kell visszatérnie (a kalibrálás a második mintalap 3. szakaszán)
    szavak = [w for w in cim_szavai if len(w) > 3]
    eleje = ' '.join(tobbi[:8])
    return len(szavak) >= 2 and sum(w in eleje for w in szavak) >= max(2, len(szavak) - 1)


def _normal(szoveg):
    return ' '.join(_SZO_RX.findall(szoveg.lower()))


def hibak(sorok):
    """A szerkezeti hibák a kész sorokon: [(sorszám, szabály, részlet)]."""
    ki = []
    # a számozott címsorok sorszáma folytonos
    szamok = [(n, int(m.group(1))) for n, s in enumerate(sorok, 1) for m in [_SZAMOZOTT_CIM_RX.match(s.szoveg)] if m]
    for i, (n, szam) in enumerate(szamok):
        if szam != i + 1:
            ki.append((n, 'szakaszrend', 'a(z) %d. számozott címsor sorszáma %d' % (i + 1, szam)))
    # a 2.1 pont tételei: minden igehely alatt „Funkció:” sor
    tetel = None
    for n, s in enumerate(sorok, 1):
        if _TETEL_RX.match(s.szoveg) or s.szoveg.startswith('#') or s.szoveg.startswith('<!-- GENERÁLT-VÉGE'):
            if tetel is not None and not tetel[1]:
                ki.append((tetel[0], 'Funkció', 'az igehely alatt nincs „Funkció:” sor'))
            tetel = [n, False] if _TETEL_RX.match(s.szoveg) else None
        elif tetel is not None and _lathato(s).startswith(_FUNKCIO):
            tetel[1] = True
    # a táblajegyzet és a sora; a cella címkéje és indoklása
    hivatkozok = {}
    for n, s in enumerate(sorok, 1):
        if not s.szoveg.startswith('|'):
            continue
        cellak = _cellak(s)
        for azon in _HIVATKOZAS_RX.findall(s.szoveg):
            hivatkozok.setdefault(azon, []).append(cellak)
        for cella in cellak:
            m = _CELLA_CIMKE_RX.match(cella)
            if m and len(_SZO_RX.findall(m.group(1))) <= 12 and _ismetli(m.group(1), m.group(2)):
                ki.append((n, 'ismételt címke', cella[:80]))
    for n, s in enumerate(sorok, 1):
        m = _JEGYZET_RX.match(s.szoveg)
        if not m:
            continue
        szoveg = _lathato(s)
        szoveg = szoveg[len(_FORRAS_ELOTAG):] if szoveg.startswith(_FORRAS_ELOTAG) else szoveg
        jegyzet = _normal(szoveg)
        if any(jegyzet and jegyzet == _normal(c) for cellak in hivatkozok.get(m.group(1), ()) for c in cellak):
            ki.append((n, 'jegyzet = cella', szoveg[:80]))
    return ki


def kapu(nezetek):
    """A kapu a lap minden nézetén. Hibánál SzerkezetHiba a hibák felsorolásával."""
    osszes = []
    for nezet, sorok in nezetek.items():
        osszes.extend((nezet,) + h for h in hibak(sorok))
    if osszes:
        raise SzerkezetHiba('szerkezeti hiba a kész lapon (GK-25): %s' % '; '.join(
            '%s %d. sor, %s: %s' % h for h in osszes[:10]))
    return nezetek
