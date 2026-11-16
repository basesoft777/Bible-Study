"""lapgen.hash_or_kapu — a regressziós mérce hash-őre a push előtti kapuban és a CI-ben (F218a, 6. ellenőrzés E1).

    python eszkozok/lapgen/hash_or_kapu.py --valtozott-lista <fájl>

A `<fájl>` a változott fájlok listája, soronként egy útvonal (a CI `valtozott_fajlok.txt`-je, illetve a
`push_elott.py` saját listája). Ha a lista az új lapgenerátort vagy a mércéjét érinti (`ERINTO_MINTA`), a
`naplok/F218_referencia.tsv` minden sorának hash-e összevetődik a fájl mai tartalmával (`regresszio.hash_or`); eltérésnél
HIBA (kilépési kód 1), a megváltozott bemenetek listájával. Így a mérce bemenetének változása nem maradhat rejtve
addig, amíg valaki a regressziót le nem futtatja. Ha a lista nem érinti a generátort, a kapu nem fut (0).

A javítás: a regresszió futtatása (`eszkozok/lapgen/regresszio.py`), és ha a lap bájtra egyezik, a hash-sorok
frissítése külön commitban, okkal (a brief 8.1 pontja).
"""
import argparse
import os
import re
import sys

import regresszio

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ERINTO_MINTA = re.compile(r'^(?:eszkozok/lapgen/|adat/lapgen_|naplok/F218_(?:referencia|elteres_engedely)\.tsv$)')


def erintett(utvonalak):
    """A lista azon útvonalai, amelyek az új lapgenerátort vagy a mércéjét érintik."""
    return [u for u in utvonalak if ERINTO_MINTA.match(u.strip().replace('\\', '/'))]


def main(argv=None):
    p = argparse.ArgumentParser(description='A regressziós mérce hash-őre (csak ha a változás a lapgenerátort érinti)')
    p.add_argument('--valtozott-lista', required=True, help='a változott fájlok listája, soronként egy útvonal')
    args = p.parse_args(argv)
    with open(args.valtozott_lista, encoding='utf-8') as f:
        utvonalak = [s.strip() for s in f if s.strip()]
    talalat = erintett(utvonalak)
    if not talalat:
        print('RENDBEN  F218 mérce hash-őr: a változás nem érinti a lapgenerátort, nem fut')
        return 0
    if not os.path.isfile(os.path.join(regresszio.GYOKER, *regresszio.REFERENCIA_TSV.split('/'))):
        print('HIBA     F218 mérce hash-őr: a változás a lapgenerátort érinti (%s), de a %s hiányzik'
              % (talalat[0], regresszio.REFERENCIA_TSV))
        return 1
    try:
        db = regresszio.hash_or()
    except regresszio.MerceHiba as exc:
        print('HIBA     F218 mérce hash-őr: %s' % exc)
        print('         Javítás: a regresszió futtatása, majd bájtra egyező lapnál a hash-sorok frissítése külön '
              'commitban (a brief 8.1 pontja).')
        return 1
    print('RENDBEN  F218 mérce hash-őr: %d sor egyezik (érintett: %d változott fájl)' % (db, len(talalat)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
