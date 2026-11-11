# -*- coding: utf-8 -*-
"""F182 HAMART-001, K4 alkalmazása (DT-F182d (A), a felhasználó 2026-11-10: „a”, az orkesztrátor továbbításában).

A szópár (málé + chámász, illetve sámá + chámász) önmagában is elég: a sorok maradnak, és az öt vers (Ez 28:16,
Mik 6:12, Sof 1:9, Jer 6:7, Hab 1:2) indoklása kimondja, hogy a szópár az 1Móz 6:11-13 szava, és maga utal vissza.
A sámá + chámász soroknál a mért tény pontosabb: az 1Móz 6:11 és 6:13-ban a chámász a málé igével áll (TAHOT:
H2555 + H4390), a sámá nem; ezért ott az indoklás azt mondja ki, hogy az erőszak szava az 1Móz 6:11-13 szava, és a
„hallatszik az erőszak” a negatív kritérium szerinti lánc-szópár.

- adat/jeloltek.tsv: az öt sor `indoklas`, `datum`, `dontes_ref` mezője;
- adat/elofordulasok.tsv: az öt sor `kapcsolodas` mezőjének végére egy mondat, a `proveniencia` frissül.
Írás előtt összevetés: csak a megnevezett mezők változnak; a `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F182_k4.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'HAMART-001'
DATUM = '2026.11.10'
DT = 'DT-F182d'
MALE = 'A „megtelt erőszakkal” szópár (מָלֵא + חָמָס, málé + chámász) az 1Móz 6:11 és 6:13 szava, és a szópár maga utal vissza a láncra'
SAMA = ('A „hallatszik az erőszak” szópár (שָׁמַע + חָמָס, sámá + chámász) a lánc szópárja: az erőszak szava (חָמָס, '
        'chámász) az 1Móz 6:11 és 6:13 szava, és a szópár maga utal vissza a láncra')
JEL = {
    'Ez 28:16': 'Beépítve: Tírusz fejedelméről: „belsőd erőszakossággal telt meg”. ' + MALE +
                ', akkor is, ha a megtelt dolog itt nem a föld, hanem egy uralkodó belseje.',
    'Mik 6:12': 'Beépítve: „a gazdagok megtöltöztek köztök ragadománynyal”; a „ragadomány” a héberben az erőszak szava. ' +
                MALE + ', akkor is, ha itt a gazdagok telnek meg vele.',
    'Sof 1:9': 'Beépítve: „a kik erőszakkal és csalárdsággal töltik meg az ő uroknak házát”. ' + MALE +
               ', akkor is, ha itt egy ház telik meg.',
    'Jer 6:7': 'Beépítve: „erőszakosság és önkény hallatszik benne”. ' + SAMA +
               ', akkor is, ha a föld szava a versben nem áll.',
    'Hab 1:2': 'Beépítve: „Meddig kiáltok még oh Uram, és nem hallgatsz meg! Kiáltozom hozzád az erőszak miatt”: a '
               'szópár itt fordított irányban áll, a próféta kiált az erőszak miatt. ' + SAMA +
               ', akkor is, ha a föld szava a versben nem áll.',
}
MONDAT_MALE = ' A szópár az 1Móz 6:11 és 6:13 szava, és maga utal vissza a láncra.'
MONDAT_SAMA = ' Az erőszak szava az 1Móz 6:11 és 6:13 szava, és a szópár maga utal vissza a láncra.'
ELOF = {'Ez 28:16': MONDAT_MALE, 'Mik 6:12': MONDAT_MALE, 'Sof 1:9': MONDAT_MALE,
        'Jer 6:7': MONDAT_SAMA, 'Hab 1:2': MONDAT_SAMA}
PROV = ('scope=manual | forras=F182 HAMART-001, K4 (DT-F182d (A), a felhasználó 2026-11-10: „a”; claude-opus-5-5) '
        '| ts=2026-11-10')


def beolvas(ut):
    sorok = open(ut, encoding='utf-8', newline='').read().split('\n')
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    return sorok, fej_i, sorok[fej_i].split('\t')


def modosit(ut, kulcs_ok, valtoztat, engedett, ir):
    sorok, fej_i, fej = beolvas(ut)
    ix = {k: i for i, k in enumerate(fej)}
    eredeti = list(sorok)
    latott = set()
    for n in range(fej_i + 1, len(sorok)):
        r = sorok[n].split('\t')
        if len(r) < len(fej) or not kulcs_ok(r, ix):
            continue
        assert r[1] not in latott, r[1]
        valtoztat(r, ix)
        latott.add(r[1])
        sorok[n] = '\t'.join(r)
    assert latott == set(JEL), set(JEL) - latott
    for i in range(len(sorok)):
        if sorok[i] != eredeti[i]:
            a, b = eredeti[i].split('\t'), sorok[i].split('\t')
            mezok = {fej[k] for k in range(len(fej)) if a[k] != b[k]}
            assert mezok <= engedett, mezok
    print('%s: %d sor' % (ut, len(latott)))
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))


def main(ir):
    def j_ok(r, ix):
        return r[0] == ID and r[1] in JEL and r[ix['jelolt_tipus']] == 'elofordulas'

    def j_valt(r, ix):
        assert r[ix['dontes']] == 'beépítve'
        r[ix['indoklas']], r[ix['datum']], r[ix['dontes_ref']] = JEL[r[1]], DATUM, DT

    def e_ok(r, ix):
        return r[0] == ID and r[1] in ELOF

    def e_valt(r, ix):
        assert not r[ix['kapcsolodas']].endswith(ELOF[r[1]])
        r[ix['kapcsolodas']] += ELOF[r[1]]
        r[ix['proveniencia']] = PROV

    modosit('adat/jeloltek.tsv', j_ok, j_valt, {'indoklas', 'datum', 'dontes_ref'}, ir)
    modosit('adat/elofordulasok.tsv', e_ok, e_valt, {'kapcsolodas', 'proveniencia'}, ir)
    if not ir:
        print('(próba; írás: --ir)')


if __name__ == '__main__':
    main('--ir' in sys.argv)
