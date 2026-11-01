"""F123 (ALVIL-001, DT-F123h): a szótári gerinc adatai az ALVIL-001-re.

Három írás, mindegyik írás előtti összevetéssel (CLAUDE.md TSV-szabály): a meglévő sorok bájtra változatlanok, csak a
felsorolt sorok jönnek hozzá vagy a felsorolt mezők változnak; eltérésnél a szkript megáll.

1. `adat/szotar_szakasz_cimke.tsv` (SEMA 2.40): a BDB H7585 8 és a Thayer G0086 2 címkéje (a végrehajtó javaslata,
   `naplok/F123_cimke_javaslat_ALVIL-001.md`; jóváhagyás: DT-F123h); a `-/1/-` sor `lexikon_jelentes_szam`-a `1`.
2. `adat/lexikon_hivatkozasok.tsv` (SEMA 2.5): a BDB H7585 `1` kulcs (a kutatói jelentésszám, amelyre a két hely képeződik);
   a `szoveg_en` a szeletelő `-/1` sávja a `konkordancia/BDB_teljes_unabridged.tsv` szövegéből (az ISTENTISZT-001 BDB-sorainak
   forrása és alakja).
3. `adat/elofordulasok.tsv`: az ALVIL-001 Jób 17:12 és Zsolt 88:4 sora `lexikon_szotar=BDB`, `lexikon_entry_id=H7585`,
   `jelentes_szam=1` (DT-F123h: a BDB két szakaszban idézi őket; a kutatói hozzárendelés -/1/-).

Olvasás `split('\\t')`, írás `'\\t'.join()`.

    python naplok/F123_cimke_ir.py            # összevet és ír
    python naplok/F123_cimke_ir.py --proba    # csak összevet, nem ír
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

CIMKE = os.path.join(GYOKER, 'adat', 'szotar_szakasz_cimke.tsv')
LEXHIV = os.path.join(GYOKER, 'adat', 'lexikon_hivatkozasok.tsv')
ELOF = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
PROV = ('scope=manual | forras=F123 (naplok/F123_cimke_javaslat_ALVIL-001.md, a végrehajtó javaslata; jóváhagyás: DT-F123h) '
        '| ts=2026-10-29')

# (szotar, strong, szakasz, lexikon_jelentes_szam, cimke_hu, proveniencia, megjegyzes)
UJ_CIMKE = [
    ('BDB', 'H7585', '-/1/-', '1', 'alvilág, ahová a halottak alászállnak', PROV,
     'a Jób 17:12 és a Zsolt 88:4 kutatói hozzárendelése ide (DT-F123h)'),
    ('BDB', 'H7585', '-/2/-', '', 'az igazak és a gonoszok állapota', PROV, ''),
    ('BDB', 'H7585', '-/2/a', '', 'a gonoszok sorsa a Seólban', PROV, ''),
    ('BDB', 'H7585', '-/2/b', '', 'az igaz kiváltása a Seólból', PROV,
     'a jóváhagyott „az igazat nem hagyják a Seólban” tagadás nélkül (ellenoriz.py 17.: a címkében tagadás nem állhat, DT272 (d)); '
     'a BDB „is ransomed from ׳שׁ” fordulata'),
    ('BDB', 'H7585', '-/3/-', '', 'a helyek megkülönböztetése', PROV, ''),
    ('BDB', 'H7585', '-/3/a', '', 'a Seól mélységei', PROV, ''),
    ('BDB', 'H7585', '-/3/b', '', 'Seól és Abaddón; verem', PROV, ''),
    ('BDB', 'H7585', '-/4/-', '', 'átvitt értelem: lealacsonyodás, száműzetés', PROV, ''),
    ('Thayer', 'G0086', '-/1/-', '', 'Hádész, az alvilág istene (tulajdonnév)', PROV, ''),
    ('Thayer', 'G0086', '-/2/-', '', 'az alvilág, a halottak birodalma', PROV, ''),
]
KAPCS = {'Jób 17:12', 'Zsolt 88:4'}


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()


def ir(ut, szoveg, proba):
    if not proba:
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)


def sorveg(szoveg):
    return '\r\n' if '\r\n' in szoveg else '\n'


def cimke(proba):
    regi = olvas(CIMKE)
    nl = sorveg(regi)
    sorok = regi.split(nl)
    fej = sorok[0].split('\t')
    meglevo = {tuple(s.split('\t')[:3]) for s in sorok[1:] if s}
    uj = []
    for s in UJ_CIMKE:
        assert len(s) == len(fej) and all('\t' not in x and '\n' not in x for x in s)
        if tuple(s[:3]) in meglevo:
            sys.exit('MEGÁLL: a kulcs már a táblában: %r' % (s[:3],))
        uj.append('\t'.join(s))
    torzs = regi[:-len(nl)] if regi.endswith(nl) else regi
    szoveg = torzs + nl + nl.join(uj) + nl
    assert szoveg.startswith(torzs) and szoveg.count(nl) == regi.count(nl) + len(uj)
    ir(CIMKE, szoveg, proba)
    print('cimke: +%d sor' % len(uj))


def bdb_1_szoveg():
    import bdb_szelet as B
    import bdb_vers_jelentes as V
    en, lem, *_ = V.betolt()
    s = en['H7585']
    r = B.szeletel(s, lem.get('H7585', ''))
    sav = [x for x in B.csomopont_savok(s, r) if x[3] == '-/1']
    assert len(sav) == 1, sav
    a, b = int(sav[0][0]), int(sav[0][1])
    return s[a:b].strip()


def lexhiv(proba):
    regi = olvas(LEXHIV)
    nl = sorveg(regi)
    sorok = regi.split(nl)
    fej_i = next(i for i, s in enumerate(sorok) if s.startswith('strong\t'))
    fej = sorok[fej_i].split('\t')
    kulcsok = {tuple(s.split('\t')[i] for i in (0, 1, 2, 3)) for s in sorok[fej_i + 1:] if s}
    k = ('H7585', 'BDB', 'H7585', '1')
    if k in kulcsok:
        sys.exit('MEGÁLL: a lexikon_hivatkozasok kulcs már létezik: %r' % (k,))
    szoveg_en = bdb_1_szoveg()
    assert szoveg_en.startswith('1 ') or szoveg_en.startswith('1. ') or szoveg_en.startswith('the underworld'), szoveg_en[:40]
    uj = dict(zip(fej, [''] * len(fej)))
    uj.update({'strong': 'H7585', 'szotar': 'BDB', 'entry_id': 'H7585', 'jelentes_szam': '1', 'szoveg_en': szoveg_en,
               'forrasfajl': 'konkordancia/BDB_teljes_unabridged.tsv'})
    sor = '\t'.join(uj[m] for m in fej)
    assert '\t' not in szoveg_en and '\n' not in szoveg_en
    torzs = regi[:-len(nl)] if regi.endswith(nl) else regi
    ir(LEXHIV, torzs + nl + sor + nl, proba)
    print('lexikon_hivatkozasok: +1 sor (%d karakter szoveg_en)' % len(szoveg_en))


def elof(proba):
    regi = olvas(ELOF)
    nl = sorveg(regi)
    sorok = regi.split(nl)
    fej_i = next(i for i, s in enumerate(sorok) if s.startswith('id\t'))
    fej = sorok[fej_i].split('\t')
    ix = {m: i for i, m in enumerate(fej)}
    valt = 0
    for i in range(fej_i + 1, len(sorok)):
        if not sorok[i]:
            continue
        m = sorok[i].split('\t')
        if m[0] == 'ALVIL-001' and m[ix['igehely']] in KAPCS:
            for mezo in ('lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam'):
                if m[ix[mezo]]:
                    sys.exit('MEGÁLL: %s %s mező már kitöltött: %r' % (m[ix['igehely']], mezo, m[ix[mezo]]))
            m[ix['lexikon_szotar']], m[ix['lexikon_entry_id']], m[ix['jelentes_szam']] = 'BDB', 'H7585', '1'
            uj = '\t'.join(m)
            assert uj.count('\t') == sorok[i].count('\t')
            sorok[i] = uj
            valt += 1
    if valt != len(KAPCS):
        sys.exit('MEGÁLL: %d sor változna, %d helyett' % (valt, len(KAPCS)))
    szoveg = nl.join(sorok)
    eltero = [i for i, (a, b) in enumerate(zip(regi.split(nl), szoveg.split(nl))) if a != b]
    assert len(eltero) == 2 and len(regi.split(nl)) == len(szoveg.split(nl))
    ir(ELOF, szoveg, proba)
    print('elofordulasok: %d sor, 3 mező' % valt)


def main():
    proba = '--proba' in sys.argv[1:]
    cimke(proba)
    lexhiv(proba)
    elof(proba)
    print('próba: nem írtam' if proba else 'kész')


if __name__ == '__main__':
    main()
