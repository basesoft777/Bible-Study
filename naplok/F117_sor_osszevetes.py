"""F117.3: írás előtti sor-összevetés (eszkozok/igazolas_migracio.py-minta) — a mai tábla és a KK4 új kimenete.

Használat: python naplok/F117_sor_osszevetes.py <uj_tabla.tsv> [<regi_tabla.tsv>]
(alapérték a régihez: konkordancia/Karoli_versmegfeleltetes.tsv). Osztályonként (A, B, C, D, D′ és „kívül”):
változott / hozzáadott / törölt / változatlan adatsor; a fejléc-sorok külön. HALMAZ-ŐR: az A–D′ halmazon kívül
0 változás; ha nem, kilépési kód 2. Csak olvas.
"""
import os
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def beolvas(path):
    fej, adat = [], {}
    with open(path, encoding='utf-8', newline='') as f:
        for s in f.read().split('\n'):
            if s.startswith('#'):
                fej.append(s)
            elif s and not s.startswith('igehely_karoli\t'):
                k = s.split('\t')[0]
                assert k not in adat
                adat[k] = s
    return fej, adat


def main():
    uj_p = sys.argv[1]
    regi_p = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
    cel = {}
    with open(os.path.join(ROOT, 'naplok', 'F117_szoveg_osszevetes.tsv'), encoding='utf-8') as f:
        for s in f:
            p = s.rstrip('\n').split('\t')
            if not s.startswith('#') and p[0] != 'igehely_karoli' and p[1] != 'kontextus':
                cel[p[0]] = p[1]
    rf, ra = beolvas(regi_p)
    uf, ua = beolvas(uj_p)
    stat = Counter()
    kivul = []
    for k in sorted(set(ra) | set(ua)):
        o = cel.get(k, 'kívül')
        if k in ra and k in ua:
            t = 'változatlan' if ra[k] == ua[k] else 'változott'
        elif k in ua:
            t = 'hozzáadott'
        else:
            t = 'törölt'
        stat[(o, t)] += 1
        if o == 'kívül' and t != 'változatlan':
            kivul.append((k, t))
    print('régi: %s (%d adatsor) | új: %s (%d adatsor)' % (regi_p, len(ra), uj_p, len(ua)))
    for o in ['A', 'C', 'B', 'D', 'D′', 'kívül']:
        print('  %-6s változott %4d | hozzáadott %4d | törölt %4d | változatlan %6d' % (
            o, stat[(o, 'változott')], stat[(o, 'hozzáadott')], stat[(o, 'törölt')], stat[(o, 'változatlan')]))
    print('fejléc-sorok: régi %d, új %d; új fejléc-sor: %s' % (
        len(rf), len(uf), [s[:70] for s in uf if s not in rf]))
    print('célhalmaz a táblában (új): %d / %d' % (sum(1 for k in cel if k in ua), len(cel)))
    # kiegészítő: a célfejezetek kontextus-versei (nem célversek) — a szöveg-összevetés párja egyezik-e a táblával
    ktx = Counter()
    ktx_elt = []
    with open(os.path.join(ROOT, 'naplok', 'F117_szoveg_osszevetes.tsv'), encoding='utf-8') as f:
        for s in f:
            p = s.rstrip('\n').split('\t')
            if s.startswith('#') or p[0] == 'igehely_karoli' or p[1] != 'kontextus':
                continue
            t = ua.get(p[0])
            kjv_t = t.split('\t')[1] if t else None
            if kjv_t == p[2]:
                ktx['egyezik'] += 1
            else:
                ktx['eltér'] += 1
                ktx_elt.append((p[0], 'szöveg: %s' % p[2], 'tábla: %s' % kjv_t))
    print('kontextus-versek (a célfejezetek nem célversei): %s %s' % (dict(ktx), ktx_elt[:20]))
    if kivul:
        print('HALMAZ-ŐR: az A–D′ halmazon kívüli változás: %d' % len(kivul))
        for x in kivul[:50]:
            print('   ', x)
        sys.exit(2)
    print('HALMAZ-ŐR: az A–D′ halmazon kívül 0 változás')


if __name__ == '__main__':
    main()
