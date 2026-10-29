"""F123 (ALVIL-001, a felhasználó döntése 2026-10-29: a két BDB-adathibát a #123 javítja): a szeletelő számjelölő-mintájának
hatásmérése a teljes angol BDB-n. A hiba: a `bdb_szelet._szam_minta` a jelentés-sorszám előtt csak `. ; : )` + szóközt fogad el
(`(?<=[.;:)]\\s)`), a szögletes zárójellel záruló szakasz utáni számot („… post-Biblical Judaism and NT.] 4 ׳שׁ figurative …”, H7585)
nem — a 4. pont ezért nem jön létre, és a példái a 3/b alá kerülnek.

A szkript a `bdb_vers_jelentes.general()`-t kétszer futtatja a memóriában (a mai mintával és a `]`-vel bővített mintával), és
szócikkenként összeveti a sorokat. Fájlt nem ír a `adat/`-ba; a kimenet `naplok/F123_bdb_szelet_meres.tsv` (a változó sorok).

    python naplok/F123_bdb_szelet_meres.py
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

import bdb_szelet as B  # noqa: E402
import bdb_vers_jelentes as V  # noqa: E402

KI = os.path.join(REPO, 'naplok', 'F123_bdb_szelet_meres.tsv')


def futtat():
    sorok, _ = V.general('meres')
    return {(s[0], s[2]): s for s in sorok}


def main():
    eredeti = B._szam_minta
    minta = eredeti().pattern
    # a javítás után (F123) a modul már a bővített mintát hordozza: a „régi” futás a visszacserélt mintával megy
    if '(?<=[.;:)\\]]\\s)' in minta:
        regi_minta, uj_minta = minta.replace('(?<=[.;:)\\]]\\s)', '(?<=[.;:)]\\s)'), minta
    else:
        assert '(?<=[.;:)]\\s)' in minta, 'a minta megváltozott: a mérés újraírandó'
        regi_minta, uj_minta = minta, minta.replace('(?<=[.;:)]\\s)', '(?<=[.;:)\\]]\\s)')
    try:
        B._szam_minta = lambda: re.compile(regi_minta)
        regi = futtat()
        B._szam_minta = lambda: re.compile(uj_minta)
        uj = futtat()
    finally:
        B._szam_minta = eredeti
    assert set(regi) == set(uj), 'a hivatkozás-sorok halmaza eltér'
    i_ut, i_vers, i_nyers = 11, 7, 4
    valt = [(k, regi[k], uj[k]) for k in sorted(regi) if regi[k][i_ut] != uj[k][i_ut]]
    strongok = sorted({k[0] for k, _, _ in valt})
    with open(KI, 'w', encoding='utf-8', newline='') as f:
        f.write('# F123: a `]`-bővítés hatása a bdb_vers_jelentes utvonal-mezőjére (csak a változó sorok) | készítő: naplok/F123_bdb_szelet_meres.py\n')
        f.write('\t'.join(['strong', 'sorszam', 'nyers', 'karoli_vers', 'utvonal_regi', 'utvonal_uj']) + '\n')
        for k, a, b in valt:
            f.write('\t'.join([k[0], k[1], a[i_nyers], a[i_vers], a[i_ut], b[i_ut]]) + '\n')
    print('ÖSSZES_SOR\t%d' % len(regi))
    print('VÁLTOZÓ_SOR\t%d' % len(valt))
    print('ÉRINTETT_SZÓCIKK\t%d' % len(strongok))
    print('SZÓCIKKEK\t%s' % ' '.join(strongok[:80]))


if __name__ == '__main__':
    main()
