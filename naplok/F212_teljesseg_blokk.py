"""F212: a HAMART-001 teljesség-mérésének újrafuttatása után a döntés nélküli versek csoportos kizárása.

A 2026-11-12-i mérés (eszkozok/teljesseg_meres.py, a mai Strong-halmazzal) 44 olyan verset ad, amelyről nincs döntés: a
H0056 (ával) 29 és a H0423 (álá) 15 előfordulását. A két szó a motívumba csak a tematikus sorok (Hós 4:1-3, Ézs 24:5-6)
Strong-mezőjével került; a negatív kritérium lexémalistáján (a lánc szavai) nem áll, és a 44 vers egyikében sincs
lánc-lexéma (TAHOT_kivonat.tsv). A meglévő minta szerint (a H7451 és a H7043 blokkja, 2026-11-03) csoportos kizárás:
két blokk-sor a `naplok/F123_teljesseg_HAMART-001_blokkok.tsv`-be, két összesítő sor a `adat/jeloltek.tsv`-be.
Az orkesztrátor döntése (2026-11-12), a felhasználó a változás-nézettel egyben hagyja jóvá.

Írás előtt összevetés: a régi sorok bájtra változatlanok, a blokk versszáma = az összesítő sor versszáma, a vers nem
előfordulás és nem áll már döntéssel a jelölttáblában. Ismételt futásnál nem ír.
Futtatás: python naplok/F212_teljesseg_blokk.py <a 44 vers listája (TSV: strong, igehely, ...)> [--ir]
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOKK = os.path.join(GYOKER, 'naplok', 'F123_teljesseg_HAMART-001_blokkok.tsv')
JEL = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
ELOF = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
HALO = 'f212'
SZO = {'H0056': 'a אָבַל (ával, gyászol, búsul) szava', 'H0423': 'az אָלָה (álá, eskü, átok) szava'}
PROV = ('scope=manual | forras=eszkozok/teljesseg_meres.py (2026-11-12, a mai Strong-halmaz), '
        'naplok/F212_teljesseg_blokk.py | ts=2026-11-12')


def olvas(ut):
    with io.open(ut, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def main():
    lista = [s.split('\t') for s in olvas(sys.argv[1]) if s.strip()]
    blokkok = {}
    for c in lista:
        blokkok.setdefault(c[0], []).append(c[1])
    if sorted(blokkok) != ['H0056', 'H0423'] or sum(len(v) for v in blokkok.values()) != 44:
        raise SystemExit('MEGÁLLÁS: nem a várt 44 vers (H0056, H0423)')
    elof = {s.split('\t')[1] for s in olvas(ELOF) if s.startswith('HAMART-001\t')}
    jel_sorok = olvas(JEL)
    fej = next(s for s in jel_sorok if s and not s.startswith('#')).split('\t')
    meglevo = {(s.split('\t')[0], s.split('\t')[1]) for s in jel_sorok if s and not s.startswith('#')}
    for st, versek in blokkok.items():
        for v in versek:
            if v in elof or ('HAMART-001', v) in meglevo:
                raise SystemExit('MEGÁLLÁS: %s már előfordulás vagy döntött jelölt' % v)
    blokk_sorok = olvas(BLOKK)
    mar = [s for s in blokk_sorok if s.startswith(HALO + '\t')]
    uj_blokk = ['%s\t%s\t%s\tigen' % (HALO, st, v) for st in sorted(blokkok) for v in blokkok[st]]
    uj_jel = []
    for st in sorted(blokkok):
        versek = blokkok[st]
        n = len(versek)
        d = {'id': 'HAMART-001', 'igehely': versek[0],
             'forras_kereses': ('F212 teljesség-mérés, Strong-háló, blokk-sor: %d vers, a sor igehelye a blokk egy verse; '
                                'a lista: naplok/F123_teljesseg_HAMART-001_blokkok.tsv (halo=%s, blokk=%s) | %s'
                                % (n, HALO, st, PROV)),
             'dontes': 'elutasítva',
             'indoklas': ('Összesítő sor %d versre (a sor igehelye a blokk egy verse áll): %s áll bennük, de a negatív '
                          'kritérium lexémalistáján álló lexéma egyik versben sincs; nem a negatív kritérium lexémája. '
                          'A szó a motívumba csak tematikus sorral került (Hós 4:1-3, Ézs 24:5-6), a lánc szavai nélkül; '
                          'a többi előfordulása ezért blokk-kizárás (a H7451 és a H7043 blokkjának mintájára).'
                          % (n, SZO[st])),
             'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': '', 'datum': '2026.11.12',
             'jelolt_tipus': 'elofordulas', 'cel_id': '', 'cel_igehely': '', 'cel_alpont': '',
             'dontes_ref': 'F212 · az orkesztrátor döntése (2026-11-12), a felhasználó jóváhagyására · %s' % PROV}
        uj_jel.append('\t'.join(d[k] for k in fej))
    if mar:
        print('A blokk-sorok már bent vannak (%d); nincs írás.' % len(mar))
        return
    print('blokk-sor: +%d (H0056 %d, H0423 %d); jelölt: +2 összesítő sor' % (
        len(uj_blokk), len(blokkok['H0056']), len(blokkok['H0423'])))
    if '--ir' not in sys.argv:
        print('(próba: --ir nélkül nincs írás)')
        return
    for ut, sorok, uj in ((BLOKK, blokk_sorok, uj_blokk), (JEL, jel_sorok, uj_jel)):
        veg = sorok[-1] == ''
        ki = (sorok[:-1] if veg else sorok) + uj + ([''] if veg else [])
        if ki[:len(sorok) - 1] != sorok[:len(sorok) - 1]:
            raise SystemExit('MEGÁLLÁS: a régi sorok változnának')
        with io.open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(ki))
    print('írva')


if __name__ == '__main__':
    main()
