"""F194.2 (CLAUDE.md 6. lépés, LXX-híd): az ószövetségi versek, amelyek görög (LXX) szövegében a formula áll —
ἐπικαλέω (G1941) és ὄνομα (G3686) legfeljebb 6 szóra, a név után legfeljebb 6 szón belül κύριος (G2962) vagy θεός
(G2316) —, összevetve az ISTENTISZT-001 előfordulásaival (E) és döntött jelöltjeivel (J).

Forrás: `konkordancia/LXX_OS/*.tsv` (lxx-morph + GreekWordList, CC BY 4.0), a `igehely_karoli` kulcs szerint; minden
könyvfájl (a szövegváltozatok is), igehelyenként egyszer. Csak olvas; a kimenet a `--kimenet` fájl (TSV).
Futtatás: python naplok/F194_lxx_hid_scan.py --kimenet naplok/F194_lxx_hid_ISTENTISZT-001.tsv
"""
import datetime
import glob
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import teljesseg_meres as T  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

MID = 'ISTENTISZT-001'
UR = {'G2962', 'G2316'}


def strong(s):
    s = (s or '').strip()
    return 'G%04d' % int(s) if s.isdigit() else s


def main():
    ki = sys.argv[sys.argv.index('--kimenet') + 1]
    _, e_versek, j_versek, _ = T.motivum_adat(MID, os.path.join(GYOKER, 'adat', 'elofordulasok.tsv'),
                                              os.path.join(GYOKER, 'adat', 'jeloltek.tsv'))
    versek = {}
    fajlok = sorted(glob.glob(os.path.join(GYOKER, 'konkordancia', 'LXX_OS', '*.tsv')))
    for ut in fajlok:
        fej = None
        for s in open(ut, encoding='utf-8'):
            if s.startswith('#'):
                continue
            m = s.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            k = d.get('igehely_karoli')
            if k:
                versek.setdefault((os.path.basename(ut), k), []).append((strong(d.get('strong')), d.get('szoalak', '')))
    talalat = {}
    for (fajl, k), tok in versek.items():
        st = [x for x, _ in tok]
        for i, s in enumerate(st):
            if s != 'G1941':
                continue
            for j in range(max(0, i - 6), min(i + 7, len(st))):
                if st[j] == 'G3686':
                    ur = bool(UR & set(st[j + 1:j + 7]))
                    szoveg = ' '.join(w for _, w in tok[max(0, min(i, j) - 1):max(i, j) + 5])
                    talalat.setdefault(k, (fajl, ur, szoveg))
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    prov = 'scope=LXX_OS-teljes: egy versben G1941+G3686 (≤6 szó) | forras=konkordancia/LXX_OS/*.tsv | n=%d | ts=%s' % (
        len(talalat), ts)
    sorok = []
    for k in sorted(talalat, key=T.kulcs):
        fajl, ur, szoveg = talalat[k]
        all_ = T.allapot(k, e_versek, j_versek)
        sorok.append('\t'.join((k, fajl, 'igen' if ur else 'nem', all_, szoveg, prov)))
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F194.2 LXX-híd: a LXX-ben ἐπικαλέω + ὄνομα (döntés nélkül) | %s\n' % prov)
        f.write('igehely\tlxx_fajl\tur_megnevezve\tallapot\tgorog_reszlet\tproveniencia\n')
        f.write('\n'.join(sorok) + '\n')
    from collections import Counter
    print(prov)
    print(Counter((s.split('\t')[2], s.split('\t')[3].split(':')[0]) for s in sorok))
    for s in sorok:
        m = s.split('\t')
        if m[3] == 'ELTÉRÉS':
            print('ELTÉRÉS', m[0], m[2], m[4])


if __name__ == '__main__':
    main()
