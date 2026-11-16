"""lapgen.festek — a festékpróba (GK-08b): bizonyíték arra, hogy belső szöveg nem szivárog a lapra.

    python eszkozok/lapgen/festek.py --id <ID> [--id <ID> …]

Festett futásban a bemeneti réteg minden burkolója jelzőszót kap (`ZZQ<bemenet>_<mező>ZZ`):
- belső mező (`Belso`, `Kulcs`, `Utvonal`): a jelzőszó **csak megjegyzésben** állhat;
- kézi próza (`Kezi`): a jelzőszó csak próza-fajtájú szövegben vagy megjegyzésben;
- idézet (`Forrasszoveg`): a jelzőszó csak idézet-fajtájú szövegben vagy megjegyzésben.

A próba a kész lap fajta-térképén fut (melyik karakter próza, sablon, idézet, megjegyzés, jelölés).
Kilépési kód: 0, ha nincs szivárgás; 1, ha van.
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lapgen import fo  # noqa: E402
from lapgen.megjelenites.md.iro import MEGJEGYZES  # noqa: E402
from lapgen.szoveg import FESTEK_ELOTAG, FESTEK_UTOTAG, Fajta, MotivumId  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# A jelzőszót kis- és nagybetűtől függetlenül keressük: az átalakított (pl. kisbetűsített) jelzőszó is látszik.
_JEL_RX = re.compile(re.escape(FESTEK_ELOTAG) + r'[A-Za-z0-9_]+?' + re.escape(FESTEK_UTOTAG), re.IGNORECASE)
# A horgony (link célja, horgony azonosítója) a címsorból képzett szerkezeti azonosító: a kézi és az idézett szöveg
# jelzőszava ott megengedett (átalakított alakban is); a belső mezőé ott is szivárgás.
_ENGEDETT = {'belso': (MEGJEGYZES,), 'kezi': (MEGJEGYZES, Fajta.PROZA, Fajta.HORGONY),
             'idezet': (MEGJEGYZES, Fajta.IDEZET, Fajta.HORGONY)}
ATALAKITOTT = 'átalakított'


def _fajta_itt(sor, hol):
    for kezdet, veg, fajta in sor.tartomanyok:
        if kezdet <= hol < veg:
            return fajta
    return None


def szivargasok(eredmeny):
    """A festett futás szivárgásai: [(nézet, sorszám, jelzőszó, kategória, fajta)]. A második visszaadott
    érték a lapon látott jelzőszavak száma kategóriánként (a próba ereje: 0 látott jelzőszó üres próba)."""
    kategoriak = eredmeny.festo.kategoriak
    kisbetus = {}
    for jel, kategoria in kategoriak.items():
        # két jelzőszó, amely csak a betűk méretében tér el, nem azonosítható: ismeretlenként szivárgás lesz
        kisbetus[jel.lower()] = kategoria if kisbetus.get(jel.lower(), kategoria) == kategoria else 'ismeretlen'
    ki, latott = [], {}
    for nezet, sorok in eredmeny.nezetek.items():
        for n, sor in enumerate(sorok, start=1):
            for m in _JEL_RX.finditer(sor.szoveg):
                kategoria = kisbetus.get(m.group(0).lower(), 'ismeretlen')
                fajta = _fajta_itt(sor, m.start())
                latott[kategoria] = latott.get(kategoria, 0) + 1
                if fajta is Fajta.HORGONY:
                    latott[Fajta.HORGONY.value] = latott.get(Fajta.HORGONY.value, 0) + 1
                if fajta not in _ENGEDETT.get(kategoria, ()):
                    ki.append((nezet, n, m.group(0), kategoria, fajta))
                elif m.group(0) not in kategoriak and fajta not in (Fajta.HORGONY, MEGJEGYZES):
                    # a jelzőszó átalakítva áll (a szöveget valami átírta): horgonyon kívül ez is szivárgás
                    ki.append((nezet, n, m.group(0), kategoria, ATALAKITOTT))
    return ki, latott


def proba(azonosito, gyoker=GYOKER, datum=None):
    eredmeny = fo.lap_keszit(gyoker, MotivumId(azonosito), datum=datum, festek=True)
    return szivargasok(eredmeny) + (eredmeny,)


def main(argv=None):
    p = argparse.ArgumentParser(description='Festékpróba: belső szöveg nem szivároghat a lapra')
    p.add_argument('--id', action='append', required=True)
    a = p.parse_args(argv)
    bukas = False
    for azonosito in a.id:
        szivargas, latott, _eredmeny = proba(azonosito)
        print('%s: %d szivárgás; látott jelzőszavak: %s' % (
            azonosito, len(szivargas),
            ', '.join('%s=%d' % kv for kv in sorted(latott.items())) or 'nincs'))
        for nezet, n, jel, kategoria, fajta in szivargas[:50]:
            print('  SZIVÁRGÁS %s:%d %s (%s) → %s' % (nezet, n, jel, kategoria, getattr(fajta, 'value', fajta)))
        bukas = bukas or bool(szivargas)
    return 1 if bukas else 0


if __name__ == '__main__':
    sys.exit(main())
