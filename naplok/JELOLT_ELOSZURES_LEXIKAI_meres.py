"""N-F150a M0 mérés — a gépi előszűrő lexikai kiterjesztése (szomszéd vers, rokon alak, nyelv) a meglévő döntéseken.

Mit mér: a `jeloltek.tsv` minden eldöntött (`beépítve` / `elutasítva`), `elofordulas` típusú sorára, a LEXIKAI
hordozójú motívumokon, a `jelolt_eloszures.vizsgal_lexikai` szabály változataival (szomszéd vers / rokon alak /
nyelvszűrés be-ki) megnézi: hány beépített sor kapna `valoszinu_ki`-t (hamis kizárás, a küszöb 0), és hány elutasított
(felismert elutasítás). A változat-azonosító: sz = szomszédos versek, r = rokon alak (Strong_szotar származtatás),
n = nyelvszűrés. Az `alap` a #150 mai szabálya (egy vers, nincs rokon, nincs nyelvszűrés).

Csak olvas. TSV: split('\\t'), csv modul nélkül. Futtatás: python naplok/JELOLT_ELOSZURES_LEXIKAI_meres.py [--reszletes]
"""
import collections
import itertools
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import jelolt_eloszures as J  # noqa: E402
import szerep_karoli as SZK  # noqa: E402

ADAT = os.path.join(GYOKER, 'adat')


def valtozat_nev(sz, r, n):
    return ''.join(c for c, b in (('sz', sz), ('r', r), ('n', n)) if b) or 'alap'


def main():
    reszletes = '--reszletes' in sys.argv
    vers_st = SZK.vers_strongok()
    mot = {r['id']: r for r in J.beolvas(os.path.join(ADAT, 'motivumok.tsv'))}
    komb = J.kombinaciok(J.beolvas(os.path.join(ADAT, 'elofordulasok.tsv')))
    szarm = J.szarmazas()
    jel = [r for r in J.jeloltek_elofordulas(J.beolvas(os.path.join(ADAT, 'jeloltek.tsv')))
           if r['dontes'] in ('beépítve', 'elutasítva')]
    lexikai = sorted(m for m in {r['id'] for r in jel} if mot.get(m, {}).get('azonossag_tipusa') == 'lexikai')
    valtozatok = list(itertools.product((False, True), repeat=3))
    print('motivum\tbeepitve\telutasitva\tvaltozat\thamis_kizaras\tfelismert_elutasitas\thamis_kizart_helyek')
    osszes = collections.defaultdict(lambda: [0, 0, 0, 0])
    for m in lexikai:
        sor_m = [r for r in jel if r['id'] == m]
        be = [r for r in sor_m if r['dontes'] == 'beépítve']
        el = [r for r in sor_m if r['dontes'] == 'elutasítva']
        for sz, ro, ny in valtozatok:
            def ki(r):
                megvan, _ok = J.vizsgal_lexikai(r['igehely'], komb.get(m, []), vers_st, szarm, sz, ro, ny)
                return megvan is False
            hamis = [r['igehely'] for r in be if ki(r)]
            felismert = [r['igehely'] for r in el if ki(r)]
            nev = valtozat_nev(sz, ro, ny)
            o = osszes[nev]
            o[0] += len(be); o[1] += len(el); o[2] += len(hamis); o[3] += len(felismert)
            print('\t'.join([m, str(len(be)), str(len(el)), nev, str(len(hamis)), str(len(felismert)),
                             '; '.join(hamis) if (hamis and (reszletes or True)) else '']))
    print()
    print('ÖSSZESEN (lexikai motívumok)\tbeepitve\telutasitva\tvaltozat\thamis_kizaras\tfelismert_elutasitas')
    for nev, o in osszes.items():
        print('\t'.join(['', str(o[0]), str(o[1]), nev, str(o[2]), str(o[3])]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
