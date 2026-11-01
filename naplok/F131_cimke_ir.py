"""F131.1 / F131.3.6: az `adat/szotar_szakasz_cimke.tsv` írása (DT-F131b 2., DT-F131c 1.+(a), DT-F131d (a)).

A tábla kézi (manual proveniencia); ez a szkript a kézzel rögzített sorokat írja ki.
A címkék szövege a végrehajtó javaslata (DT-F131d (a)); jóváhagyásuk a DT-F131f-nél;
a Thayer 1. rész címkéje „elnevezni” (a felhasználó döntése, DT-F131i).

F131.3.6: a Thayer G1941 átmeneti kézi szakaszhatárai (a `teljes` magyar sor szeletei,
`hu_kezdet`/`hu_hossz`/`forditas_hash`) kivezetve: a magyar Thayer-szöveg a #142
szakaszsoraiból jön (`forditasok.tsv` `sz<n>`, DT-F131c 1.); a táblában csak a két
Thayer-címke marad.

Ha a tábla már létezik, írás előtt összeveti a sorokat az újonnan előállítottakkal,
és eltérésnél megáll (CLAUDE.md TSV-szabály; minta: eszkozok/igazolas_migracio.py).
`--felulir` csak akkor ír eltérő tartalmat.

Olvasás `split('\\t')`, írás `'\\t'.join()`; a `csv` modul nem használható.

    python naplok/F131_cimke_ir.py [--felulir]
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CEL = os.path.join(GYOKER, 'adat', 'szotar_szakasz_cimke.tsv')
TS = '2026-10-26'
FEJLEC = ['szotar', 'strong', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu', 'proveniencia', 'megjegyzes']
PROV = 'scope=manual | forras=F131 (DT-F131b–d, a végrehajtó javaslata; jóváhagyás: DT-F131f) | ts=%s' % TS
PROV_ELNEVEZNI = 'scope=manual | forras=F131 (DT-F131i, a felhasználó döntése) | ts=2026-10-27'

# (szotar, strong, szakasz, lexikon_jelentes_szam, cimke_hu, proveniencia, megjegyzes)
KEZI = [
    ('BDB', 'H7121', 'Qal/2/c', '2.c', 'segítségül hívni', PROV, ''),
    ('BDB', 'H7121', 'Qal/3/-', '3', 'kihirdetni', PROV, ''),
    ('BDB', 'H7121', 'Qal/3/b', '', 'a nevet kihirdetni', PROV, ''),
    ('BDB', 'H8034', '-/3/-', '', 'név: Isten megjelölése', PROV, ''),
    ('BDB', 'H8034', '-/4/-', '', 'név: hamis istenekről', PROV, ''),
    ('TBESG', 'G1941', '2', '2', 'segítségül hívni, folyamodni valakihez', PROV,
     'a TBESG tagolása (a lexikon_hivatkozasok.tsv kulcsa); DT-F131c (a)'),
    ('Thayer', 'G1941', '-/1/-', '', 'elnevezni', PROV_ELNEVEZNI, 'DT-F131i'),
    ('Thayer', 'G1941', '-/5/-', '', 'segítségül hívni a név kimondásával', PROV, ''),
]


def main():
    felulir = '--felulir' in sys.argv[1:]
    sorok = [list(s) for s in KEZI]
    for s in sorok:
        if any('\t' in x or '\n' in x for x in s):
            sys.exit('HIBA: tab vagy sortörés egy mezőben: %r' % s)
    szoveg = '\t'.join(FEJLEC) + '\n' + ''.join('\t'.join(s) + '\n' for s in sorok)
    if os.path.exists(CEL):
        with open(CEL, encoding='utf-8') as f:
            regi = f.read()
        if regi == szoveg:
            print('változatlan: %s (%d sor)' % (CEL, len(sorok)))
            return
        regi_sorok = regi.split('\n')
        uj_sorok = szoveg.split('\n')
        for i in range(max(len(regi_sorok), len(uj_sorok))):
            a = regi_sorok[i] if i < len(regi_sorok) else '<nincs>'
            b = uj_sorok[i] if i < len(uj_sorok) else '<nincs>'
            if a != b:
                print('eltérés a(z) %d. sorban:\n  régi: %s\n  új:   %s' % (i + 1, a, b))
        if not felulir:
            sys.exit('MEGÁLL: a tábla eltér; --felulir nélkül nem írok.')
    with open(CEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('megírva: %s (%d sor)' % (CEL, len(sorok)))


if __name__ == '__main__':
    main()
