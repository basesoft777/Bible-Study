"""f08_nyitott.py -- F8.8: a DT23 (c) es (e) kulon tetelei a NYITOTT_FELADATOK.md-be, helyorzovel
(F30_SZAMOZAS_BRIEF.md 1. pont: N-F<nn>, tobb eseten a, b betuvel). CRLF-hu iras, sorcsokkenes-orrel.
Futtatas: python eszkozok/f08/f08_nyitott.py
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UT = os.path.join(GYOKER, 'NYITOTT_FELADATOK.md')
HORGONY = '## Migrálva a döntési fájl 8. szakaszából (F1.6, 2026.09.13)'

TETELEK = [
    '- **N-F08a — a Préd 9:10 előfordulás-sor (ALVIL-001) igehelyének javítása',
    '  Préd 9:12-re.** *(ÚJ, F08 (#8), DT23 (c), DT7 (g); `naplok/F08_zaras.md`)*',
    '  A munkalap-igehely MT/KJV-számozású: a Károli Préd 9:10 = MT 9:8 (KK, KEZI),',
    '  a שְׁאוֹל a Károli 9:12-ben (MT 9:10) áll, ahol a Macula ἅδη G0086 és az',
    '  `LXX_OS` ᾅδης egyezik. A javítás az `adat/elofordulasok.tsv` ALVIL-001',
    '  sorát érinti; utána az `adat/lxx_dontesek.tsv` LD008 sora tárgytalan (az',
    '  ALVIL-001 G-tokenje G0086, a 9:12 várhatóan „egyező” lesz, döntési sor',
    '  nélkül). A felvételt a felhasználó a DT23-ban jóváhagyta (2026.09.30).',
    '- **N-F08b — saját címke a `nincs_heber_kulcsszo` sorokra a lexikon-',
    '  generátorban.** *(ÚJ, F08 (#8), DT23 (e); `adat/SEMA.md` 2.11)* Az',
    '  `adat/lxx_dontesek.tsv` 8 `nincs_heber_kulcsszo` / `nem_alkalmazhato` sora',
    '  (ige-tartományú előfordulás-sor kulcsszó nélküli verse, ill. tematikus sor)',
    '  ma „kutatói azonosítás függőben”-ként jelenik meg. A `lexikon_general.py`',
    '  `blokk_lxx` kapjon saját „kulcsszó nincs a versben” címkét (és számlálót),',
    '  a SEMA 2.11 megjelenítési mondata ehhez igazodjon. A felvételt a',
    '  felhasználó a DT23-ban jóváhagyta (2026.09.30).',
]


def main():
    with io.open(UT, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if 'N-F08a' in nyers:
        print('az N-F08a mar szerepel, nem irok')
        return
    sorok = nyers.split('\r\n')
    idx = [i for i, s in enumerate(sorok) if s == HORGONY]
    if len(idx) != 1:
        print('horgony nem egyertelmu: %r' % idx)
        sys.exit(1)
    i = idx[0]
    # a horgony elotti ures sor ele szurunk
    while i > 0 and sorok[i - 1] == '':
        i -= 1
    uj = sorok[:i] + TETELEK + sorok[i:]
    if len(uj) != len(sorok) + len(TETELEK):
        print('sorszam-eltérés')
        sys.exit(1)
    with io.open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write('\r\n'.join(uj))
    print('N-F08a, N-F08b beszurva (%d -> %d sor)' % (len(sorok), len(uj)))


if __name__ == '__main__':
    main()
