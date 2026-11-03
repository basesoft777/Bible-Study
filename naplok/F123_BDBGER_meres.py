"""F123.BDBGER mérés: a BDB-gerinc szócikk-összevonása (N-F123m második fele).

(1) A `bdb_szakaszok.tsv` (2.30): hány Strongnak van több BDB-szócikke (`bdb_id`), és hányban ismétlődik útvonal
    több szócikk között (a régi, csak útvonal szerinti összevonás ezeket fűzte egybe), ill. egy szócikken belül
    nem szomszédos sorokban (ez nem e tétel tárgya).
(2) A `bdb_vers_jelentes.tsv` (2.29) sorainak szócikkhez rendelése (`lexikon_general.bdb_vers_szocikk`): útvonalból,
    helyből (`poz`), nem azonosítható; és a helyből adott jelöltek összevetése az útvonalból egyértelmű sorokon.
(3) A 2.32 jelölő nélküli sora, amelynek magyar szövege egy másik szócikk sorában áll (szócikkhatáron át „elnyelt”).
(4) A kilenc lap Strongjai (`elofordulasok.tsv`, H-tokenek; a gerinc aktív-e) és a régi összevonás rajtuk.

    python naplok/F123_BDBGER_meres.py > naplok/F123_BDBGER_meres_kimenet.txt
"""
import collections
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402

LAPOK = ['ALVIL-001', 'ANTROP-001', 'HAMART-001', 'HODIT-001', 'ISTENTISZT-001', 'KIRALY-001', 'MENNY-001',
         'TEREMT-001', 'TEREMT-002']


def main():
    a = LG.gerinc_adat()
    vag = LG.gerinc_utvonal_vag
    # (1)
    tobb = [s for s in a['bdb_sz'] if len(LG.bdb_szocikkek(a, s)) > 1]
    kozott, belul, regi_ossze = [], [], {}
    for s in a['bdb_sz']:
        sorok = sorted(a['bdb_sz'][s], key=lambda r: int(r['sorszam']))
        ut_id = collections.defaultdict(set)
        futam = []
        for r in sorok:
            if r['utvonal'] == 'cim':
                continue
            ut_id[r['utvonal']].add(r['bdb_id'])
            k = (r['bdb_id'], r['utvonal'])
            if not futam or futam[-1] != k:
                futam.append(k)
        osz = sorted(u for u, ids in ut_id.items() if len(ids) > 1)
        if osz:
            regi_ossze[s] = osz
        if any(u != 'fej' for u in osz):
            kozott.append(s)
        szam = collections.Counter(futam)
        if any(n > 1 for (b, u), n in szam.items() if u != 'fej'):
            belul.append(s)
    print('## (1) bdb_szakaszok.tsv')
    print('Strong a táblában: %d' % len(a['bdb_sz']))
    print('több BDB-szócikk (bdb_id): %d' % len(tobb))
    print('régi összevonás (útvonal, a fejet is beleértve, több szócikkből): %d Strong' % len(regi_ossze))
    print('  ebből a fejen kívüli útvonal is: %d Strong' % len(kozott))
    print('szócikken belül nem szomszédos ismétlődő útvonal (nem e tétel tárgya): %d Strong' % len(belul))
    # (2)
    st = collections.Counter()
    nem = []
    for (strong, vers), sorok in a['bdb_vj'].items():
        if strong not in tobb:
            continue
        for r in sorok:
            st['sor'] += 1
            ut = r['utvonal']
            if ut == 'fej':
                ut_j = {x['bdb_id'] for x in a['bdb_sz'][strong] if x['utvonal'] == 'fej'}
            elif ut == 'tagolatlan':
                ut_j = {b for b in LG.bdb_szocikkek(a, strong)
                        if all(x['utvonal'] in ('cim', 'fej') for x in a['bdb_sz'][strong] if x['bdb_id'] == b)}
            else:
                ut_j = LG._utvonal_szocikkei(a, strong, ut)
            try:
                p_j = LG._bdb_poz_szocikkei(a, strong, int(r['poz']))
            except (TypeError, ValueError):
                p_j = set()
            if len(ut_j) == 1:
                st['utvonalbol'] += 1
                if ut not in ('fej', 'tagolatlan'):
                    st['ellenorzo_halmaz'] += 1
                    st['hely_egyezik' if ut_j <= p_j else 'hely_ellentmond'] += 1
                    if not ut_j <= p_j and len(p_j) == 1:
                        st['hely_ellentmond_egyertelmuen'] += 1
            b, ok = LG.bdb_vers_szocikk(a, strong, r)
            if b is None:
                st['nem_azonosithato'] += 1
                if len(nem) < 25:
                    nem.append('%s %s sorszam %s: %s' % (strong, vers, r['sorszam'], ok))
            elif len(ut_j) != 1:
                st['helybol'] += 1
    print()
    print('## (2) bdb_vers_jelentes.tsv sorai a több szócikkű Strongokban (szurt≠1, Károli-verssel)')
    for k in ('sor', 'utvonalbol', 'helybol', 'nem_azonosithato', 'ellenorzo_halmaz', 'hely_egyezik', 'hely_ellentmond',
              'hely_ellentmond_egyertelmuen'):
        print('%s: %d' % (k, st[k]))
    rossz = sorted(s for s in tobb if not LG._bdb_poz_megbizhato(a, s))
    print('Strong, amelyben a hely nem dönt (a 2.29 és a 2.30 szócikkhatára eltér): %d' % len(rossz))
    for x in nem:
        print('  ' + x)
    # (3)
    eln = {}
    for s in tobb:
        _sz, e = LG.bdb_gerinc_szocikkek(a, s)
        if e:
            eln[s] = e
    print()
    print('## (3) szócikkhatáron át elnyelt (jelölő nélküli, magyar szöveg nélküli) szakasz: %d Strong, %d szakasz'
          % (len(eln), sum(len(e) for e in eln.values())))
    # (4)
    _, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
    print()
    print('## (4) a kilenc lap')
    for m in LAPOK:
        tok = sorted({t for r in elo if r['id'] == m for t in (r.get('strong') or '').split('+') if t.startswith('H')})
        reszek = []
        for t in tok:
            ids = LG.bdb_szocikkek(a, t)
            if len(ids) > 1:
                reszek.append('%s (%d szócikk; régi összevonás: %s; elnyelt: %s)'
                              % (t, len(ids), ', '.join(regi_ossze.get(t, [])) or '—',
                                 ', '.join('%s %s → %s %s' % (k + v) for k, v in sorted(eln.get(t, {}).items())) or '—'))
        print('%s | gerinc aktív: %s | H-token: %d | több szócikkű: %s'
              % (m, 'igen' if LG.gerinc_aktiv(m) else 'nem', len(tok), '; '.join(reszek) or '—'))
        for t in tok:
            if len(LG.bdb_szocikkek(a, t)) > 1:
                n = [r for (st_, _v), sorok in a['bdb_vj'].items() if st_ == t for r in sorok]
                nem_az = sum(1 for r in n if LG.bdb_vers_szocikk(a, t, r)[0] is None)
                print('    %s: 2.29-sor %d, nem azonosítható %d, a hely megbízható: %s'
                      % (t, len(n), nem_az, 'igen' if LG._bdb_poz_megbizhato(a, t) else 'nem'))


if __name__ == '__main__':
    main()
