"""F239 U2 — két javaslat adatsorai (egyszeri szkript; DT-F239a, DT-F239b helyőrzővel).

ÁLLAPOT: javaslat, a szerkesztő döntésére vár (naplok/F239_szerkeszto_kerdesek.md). Az F239.5 egyszer lefuttatta,
az F239.6 a sorokat kivette. Csak a szerkesztő szava után futtatandó újra; előtte a FORRAS és a kapcsolat-indoklás
„az integrátor” szava és a dátum a tényleges döntéshez igazítandó.

DT-F239a: az ALVIL-001–TEREMT-001 motívumközi kapcsolat az Ez 31:15-ön (jelölt-sor `beépítve` + kapcsolat-sor).
DT-F239b: a 11 Nave-jelölt döntése (4 kivalasztott, 7 kizart, tiltott nincs).

python naplok/F239_U2_dontesek_ir.py        (száraz)
python naplok/F239_U2_dontesek_ir.py --ir   (hozzáfűzés; a régi rész bájtra azonos marad, ellenőrizve)
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

TS = '2026-11-23'
FORRAS = ('F239 TEREMT-001 új cikk, U2 (a session javaslata, claude-opus-5-5; az integrátor döntése a felhasználó '
          'felhatalmazásával, 2026-11-23: %s)')

NAVE = [
    ('NAVE-3885', 'PIT', 'kivalasztott', 'funkció-téma: a feneketlen mélység, a Jelenések ἄβυσσος-a (Jel 9:11, 11:7, 17:8)'),
    ('NAVE-1502', 'EARTH', 'kivalasztott', 'funkció-téma: a föld teremtés előtti állapota, amelyet a mélység borít (Zsolt 104:6, Péld 8:24)'),
    ('NAVE-1400', 'DEW', 'kivalasztott', 'funkció-téma: a mélység és a harmat mint Isten gondviselő áldása (5Móz 33:13, Péld 3:20)'),
    ('NAVE-3986', 'PSALMS', 'kivalasztott', 'funkció-téma: a vörös-tengeri szabadítás éneke, ahol a mélység az ítélet eszköze (2Móz 15:5, 15:8)'),
    ('NAVE-1682', 'EPIC', 'kizart', 'ugyanannak a két versnek (2Móz 15:5, 15:8) műfaji címkéje; a funkciót a PSALMS-téma nevezi meg'),
    ('NAVE-4643', 'SONG', 'kizart', 'ugyanannak a két versnek (2Móz 15:5, 15:8) műfaji címkéje; a funkciót a PSALMS-téma nevezi meg'),
    ('NAVE-3906', 'POETRY', 'kizart', 'ugyanannak a két versnek (2Móz 15:5, 15:8) műfaji címkéje; a funkciót a PSALMS-téma nevezi meg'),
    ('NAVE-0305', 'ANIMALS', 'kizart', 'a versek az állatok miatt esnek bele, nem a mélység funkciója miatt'),
    ('NAVE-1213', 'CONTINENTS', 'kizart', 'a téma a szárazföldet indexeli; a teremtés-funkciót az EARTH-téma nevezi meg'),
    ('NAVE-3189', 'MANASSEH', 'kizart', 'az áldás címzettjét indexeli, nem a mélység funkcióját'),
    ('NAVE-1676', 'EPHRAIM', 'kizart', 'az áldás címzettjét indexeli, nem a mélység funkcióját'),
]

JELOLT = {
    'id': 'TEREMT-001', 'igehely': 'Ez 31:15',
    'forras_kereses': ('motívumközi mérés: közös vers (naplok/F239_U1_TEREMT-001_felmeres_szomszedok.tsv; kollokáció '
                       'H8415+H7585) | scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv '
                       '| strong=H8415+H7585 | n=1 | ts=2026-11-23T12:24Z'),
    'dontes': 'beépítve',
    'indoklas': ('Egy versben áll a mélység és a seól: a cédrus, vagyis a fáraó a seólba száll, és miatta Isten gyászba '
                 'borítja és visszatartja a mélységet. A két szó két külön motívum, itt érintkeznek: a mélység a halál '
                 'közelségének képe (vö. Jón 2:6, Zsolt 71:20), a seól a holtak helye.'),
    'datum': '2026.11.23', 'jelolt_tipus': 'motivumkozi', 'cel_id': 'ALVIL-001', 'cel_igehely': 'Ez 31:15',
    'dontes_ref': 'DT-F239a · naplok/F239_hatar.md 1. pont, 3. kérdés · naplok/ERVNAPLO_TEREMT-001.md V5',
}

KAPCSOLAT = {
    'id_a': 'ALVIL-001', 'igehely_a': 'Ez 31:15', 'id_b': 'TEREMT-001', 'igehely_b': 'Ez 31:15',
    'tipus': 'közös_igehely',
    'funkcio': 'a cédrus a seólba száll, a mélység gyászba borul: a halál helye és a halál mélye egy versben',
    'bizonyossag': 'magas', 'pardes_szint': 'Peshat',
    'indoklas': ('Mért: közös vers, mindkét motívum szava áll benne (a tehóm és a seól); mindkét vers előfordulás a '
                 'saját motívumában. A két szó funkciója más (a mélység és a holtak helye), ezért két motívum; a vers '
                 'az érintkezésük helye. Döntés: DT-F239a (az integrátor, 2026-11-23).'),
    'dontes_ref': 'jeloltek.tsv;TEREMT-001;Ez 31:15;motivumkozi;ALVIL-001',
    'proveniencia': ('scope=TEREMT-001 Ez 31:15 ↔ ALVIL-001 Ez 31:15 | forras=elofordulasok.tsv+TAHOT_kivonat.tsv '
                     '(kollokáció H8415+H7585) | ts=2026-11-23T12:24Z'),
}


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()


def fejlec(szoveg):
    return next(s for s in szoveg.split('\n') if s and not s.startswith('#')).split('\t')


def sor(fej, d):
    return '\t'.join(d.get(n, '') for n in fej)


def hozzafuz(ut, uj_sorok, kulcs_ell):
    regi = olvas(ut)
    if not regi.endswith('\n'):
        sys.exit('HIBA: %s nem sorvéggel végződik' % ut)
    for s in uj_sorok:
        if kulcs_ell(regi, s):
            sys.exit('HIBA: kulcsütközés (%s): %s' % (ut, s[:80]))
    return regi, regi + ''.join(s + '\n' for s in uj_sorok)


def main():
    ir = '--ir' in sys.argv
    tervek = []
    ut = 'adat/tematikus_temak.tsv'
    fej = fejlec(olvas(ut))
    nave = [sor(fej, {'id': 'TEREMT-001', 'forras': 'Nave', 'tema_id': t, 'tema': n, 'dontes': d, 'indok': i,
                      'proveniencia': 'scope=manual | forras=%s | ts=%s' % (FORRAS % 'DT-F239b', TS)})
            for t, n, d, i in NAVE]
    tervek.append(hozzafuz(ut, nave, lambda r, s: ('\n' + '\t'.join(s.split('\t')[:3]) + '\t') in r) + (ut,))
    ut = 'adat/jeloltek.tsv'
    fej = fejlec(olvas(ut))
    j = sor(fej, JELOLT)
    # a kulcs: id + igehely + jelolt_tipus + cel_id (az Ez 31:15 előfordulás-sora más kulcs)
    tervek.append(hozzafuz(ut, [j], lambda r, s: any(
        x.startswith('TEREMT-001\tEz 31:15\t') and '\tmotivumkozi\tALVIL-001\t' in x for x in r.split('\n'))) + (ut,))
    ut = 'adat/motivum_kapcsolatok.tsv'
    fej = fejlec(olvas(ut))
    k = sor(fej, KAPCSOLAT)
    tervek.append(hozzafuz(ut, [k], lambda r, s: '\nALVIL-001\tEz 31:15\t\tTEREMT-001\tEz 31:15\t' in r) + (ut,))
    for regi, uj, ut in tervek:
        print('%s: +%d sor' % (ut, uj.count('\n') - regi.count('\n')))
        if ir:
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write(uj)
            if not olvas(ut).startswith(regi) or olvas(ut) != uj:
                sys.exit('HIBA: visszaolvasás eltér: %s' % ut)
    print('írva' if ir else 'száraz futás')


if __name__ == '__main__':
    main()
