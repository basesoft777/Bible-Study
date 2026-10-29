"""F123 (ALVIL-001, DT-F123i): a 11 címkézetlen előfordulás-sor kutatói hozzárendelése.

Döntés: orkesztrátor, a felhasználó felhatalmazásával (2026-10-29: „vedd át a döntéseket”), a végrehajtó javaslata szerint
(`naplok/F123_M1_ALVIL-001.md` 5.): Hós 13:14 → BDB `-/4/-`; Zsolt 49:15, Ez 31:16 → BDB `-/2/a` (az Ez 31:16 értelmező
ítélet); a 8 ÚSZ-hely → Thayer `-/2/-`. Az út a Jób 17:12-éval azonos (`naplok/F123_cimke_ir.py`):

1. `adat/lexikon_hivatkozasok.tsv`: BDB H7585 `2.a`, `4` (a szeletelő sávja a `BDB_teljes_unabridged.tsv` szövegéből) és
   Thayer G0086 `2` (a `adat/thayer_szakaszok.tsv` 2. pontja; az `entry_id` a Strong-token, mert a kutatói hozzárendelés a
   `lexikon_entry_id` tokenjéé);
2. `adat/szotar_szakasz_cimke.tsv`: a három szakasz `lexikon_jelentes_szam`-a;
3. `adat/elofordulasok.tsv`: a 11 sor `lexikon_szotar`, `lexikon_entry_id`, `jelentes_szam` mezője.

Minden írás előtt összevetés: csak a felsorolt sorok/mezők változnak, a meglévő érték üres; eltérésnél megáll.

    python naplok/F123_kutatoi_ir.py [--proba]
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))

CIMKE = os.path.join(GY, 'adat', 'szotar_szakasz_cimke.tsv')
LEXHIV = os.path.join(GY, 'adat', 'lexikon_hivatkozasok.tsv')
ELOF = os.path.join(GY, 'adat', 'elofordulasok.tsv')
THSZ = os.path.join(GY, 'adat', 'thayer_szakaszok.tsv')

# igehely → (lexikon_szotar, lexikon_entry_id, jelentes_szam)
HOZZA = {'Hós 13:14': ('BDB', 'H7585', '4'), 'Zsolt 49:15': ('BDB', 'H7585', '2.a'), 'Ez 31:16': ('BDB', 'H7585', '2.a')}
for _v in ('Mt 11:23', 'Luk 10:15', 'Luk 16:23', 'ApCsel 2:27', 'ApCsel 2:31', 'Jel 1:18', 'Jel 6:8', 'Jel 20:13-14'):
    HOZZA[_v] = ('Thayer', 'G0086', '2')
# (szotar, strong, szakasz) → lexikon_jelentes_szam
CIMKE_KULCS = {('BDB', 'H7585', '-/2/a'): '2.a', ('BDB', 'H7585', '-/4/-'): '4', ('Thayer', 'G0086', '-/2/-'): '2'}


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()


def nl_of(s):
    return '\r\n' if '\r\n' in s else '\n'


def bdb_sav(ut):
    import bdb_szelet as B
    import bdb_vers_jelentes as V
    en, lem, *_ = V.betolt()
    s = en['H7585']
    sav = [x for x in B.csomopont_savok(s, B.szeletel(s, lem.get('H7585', ''))) if x[3] == ut]
    assert len(sav) == 1, (ut, sav)
    return s[int(sav[0][0]):int(sav[0][1])].strip()


def thayer_2():
    for l in olvas(THSZ).split('\n'):
        m = l.rstrip('\r').split('\t')
        if m[0] == 'G0086' and len(m) > 4 and m[2] == '-/2/-':
            return ('%s %s' % (m[3], m[4])).strip()
    sys.exit('MEGÁLL: a Thayer G0086 -/2/- szakasza nincs meg')


def valtoztat(ut, fn, proba):
    regi = olvas(ut)
    nl = nl_of(regi)
    uj = fn(regi.split(nl), nl)
    szoveg = nl.join(uj)
    if not proba:
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)
    a, b = regi.split(nl), uj
    print('%s: %d sor változik, %d új' % (os.path.basename(ut), sum(1 for x, y in zip(a, b) if x != y), len(b) - len(a)))


def lexhiv(sorok, nl):
    fi = next(i for i, s in enumerate(sorok) if s.startswith('strong\t'))
    fej = sorok[fi].split('\t')
    kulcsok = {tuple(s.split('\t')[:4]) for s in sorok[fi + 1:] if s}
    ujak = [('H7585', 'BDB', 'H7585', '2.a', bdb_sav('-/2/a'), 'konkordancia/BDB_teljes_unabridged.tsv'),
            ('H7585', 'BDB', 'H7585', '4', bdb_sav('-/4'), 'konkordancia/BDB_teljes_unabridged.tsv'),
            ('G0086', 'Thayer', 'G0086', '2', thayer_2(), 'adat/thayer_szakaszok.tsv')]
    assert fej == ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forrasfajl'], fej
    for u in ujak:
        if u[:4] in kulcsok:
            sys.exit('MEGÁLL: a kulcs már létezik: %r' % (u[:4],))
        assert all('\t' not in x and '\n' not in x for x in u)
    while sorok and sorok[-1] == '':
        sorok.pop()
    return sorok + ['\t'.join(u) for u in ujak] + ['']


def cimke(sorok, nl):
    fej = sorok[0].split('\t')
    ix = {m: i for i, m in enumerate(fej)}
    talalt = 0
    for i in range(1, len(sorok)):
        m = sorok[i].split('\t')
        k = tuple(m[:3])
        if k in CIMKE_KULCS:
            if m[ix['lexikon_jelentes_szam']]:
                sys.exit('MEGÁLL: kitöltött lexikon_jelentes_szam: %r' % (k,))
            m[ix['lexikon_jelentes_szam']] = CIMKE_KULCS[k]
            sorok[i] = '\t'.join(m)
            talalt += 1
    if talalt != len(CIMKE_KULCS):
        sys.exit('MEGÁLL: %d címke-sor a %d helyett' % (talalt, len(CIMKE_KULCS)))
    return sorok


def elof(sorok, nl):
    fi = next(i for i, s in enumerate(sorok) if s.startswith('id\t'))
    ix = {m: i for i, m in enumerate(sorok[fi].split('\t'))}
    talalt = set()
    for i in range(fi + 1, len(sorok)):
        m = sorok[i].split('\t')
        if m and m[0] == 'ALVIL-001' and m[ix['igehely']] in HOZZA:
            for mezo in ('lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam'):
                if m[ix[mezo]]:
                    sys.exit('MEGÁLL: %s %s kitöltött' % (m[ix['igehely']], mezo))
            sz, e, j = HOZZA[m[ix['igehely']]]
            m[ix['lexikon_szotar']], m[ix['lexikon_entry_id']], m[ix['jelentes_szam']] = sz, e, j
            sorok[i] = '\t'.join(m)
            talalt.add(m[ix['igehely']])
    if talalt != set(HOZZA):
        sys.exit('MEGÁLL: hiányzó sor: %s' % sorted(set(HOZZA) - talalt))
    return sorok


def main():
    proba = '--proba' in sys.argv[1:]
    valtoztat(LEXHIV, lexhiv, proba)
    valtoztat(CIMKE, cimke, proba)
    valtoztat(ELOF, elof, proba)
    print('próba: nem írtam' if proba else 'kész')


if __name__ == '__main__':
    main()
