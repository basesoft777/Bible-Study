"""F185 P5: a seed-103 vak mérés összevetése (a naplok/F185_jelentes.md 4. szakasza szerint; az összevetés szabálya az
`m2_minta_osszevet.py`-é: `bont`, `bont_kitoltott`, `fo`).

- könyv/vers: a kulcs `mt_vers`-e = a kitöltés `konyv_mt`-je; szűrt (nem bibliai) kulcssornál a kitöltés „alhivatkozás”;
- jelentéspont: szakasz (római; a `h:` címke üres) + rész + a fő mutató (a zárójeles, nagybetűs és görög szint nélkül;
  „fej” = „tagolatlan” = „<törzs>”);
- arany: ahol A = B (mindkét mutatón külön), az; ahol A ≠ B, az ITELET szótár (a forrás alapján, idézettel a naplóban).
Kiírja a nyers számokat Wilson-CI-vel, A-ra és B-re külön, és a `bizonyossag` szerint.
Használat (a repó gyökeréből): python naplok/F185_seed103_osszevet.py [--reszlet]"""
import math
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'eszkozok', 'olvaso_szerver'))
import m2_minta_osszevet as M2  # noqa: E402

N = os.path.join(R, 'naplok', 'BDB_SZELETELO_M2_')
# az A ≠ B sorok ítélete: azon -> {'vers': <arany konyv_mt>, 'jp': (<arany jelentespont>, <arany resz>)} (a napló 8. szakasza)
ITELET = {
    # H3318 „— 1 go or come out or forth: … c. …”: a „Qal” név a digitális forrásban az első törzs előtt hiányzik (2.31 kézi
    # `jelolo_hianyzik`, DT-F107g (b)); a szócikk később Hiph`il / Hoph`al törzset nyit, tehát az 1. pont a Qal-é: B helyes
    'N182': {'jp': ('Qal/1/c', '')},
}


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)


def vers_kulcs(e):
    return e['konyv_mt'].split(' (')[0].strip()


def vers_ok(k, v):
    if k['szurt'] == '1':
        return v.startswith('alhiv')
    return k['mt_vers'] == v


def jp_ok(k, jp, resz):
    ksz, kseg = M2.bont(k['szakasz'], k['utvonal'])
    esz, eresz, eseg = M2.bont_kitoltott(jp, resz)
    return ksz == esz and (k['resz'] or '') == eresz and M2.fo(kseg) == M2.fo(eseg)


def jp_egyezik(a, b):
    """A két kitöltés ugyanazt mondja-e (ugyanazzal a normálással)."""
    asz, ar, aseg = M2.bont_kitoltott(a['jelentespont'], a.get('resz', ''))
    bsz, br, bseg = M2.bont_kitoltott(b['jelentespont'], b.get('resz', ''))
    return asz == bsz and ar == br and M2.fo(aseg) == M2.fo(bseg)


def main():
    kulcs = {r['azon']: r for r in M2.olvas(N + 'minta_seed103_kulcs.tsv')}
    A = {r['azon']: r for r in M2.olvas(N + 'seed103_kitoltott_A.tsv')}
    B = {r['azon']: r for r in M2.olvas(N + 'seed103_kitoltott_B.tsv')}
    n = len(kulcs)
    sz = {'vers': 0, 'jp': 0, 'vers_A': 0, 'jp_A': 0, 'vers_B': 0, 'jp_B': 0}
    biz = {}
    elter_ab, gep_hiba = [], []
    for az in sorted(kulcs):
        k, a, b = kulcs[az], A[az], B[az]
        va, vb = vers_kulcs(a), vers_kulcs(b)
        sz['vers_A'] += vers_ok(k, va)
        sz['vers_B'] += vers_ok(k, vb)
        sz['jp_A'] += jp_ok(k, a['jelentespont'], a.get('resz', ''))
        sz['jp_B'] += jp_ok(k, b['jelentespont'], b.get('resz', ''))
        ab_v = va == vb or (va.startswith('alhiv') and vb.startswith('alhiv'))
        ab_j = jp_egyezik(a, b)
        it = ITELET.get(az, {})
        if ab_v:
            okv = vers_ok(k, va)
        elif 'vers' in it:
            okv = vers_ok(k, it['vers'])
        else:
            okv = None
        if ab_j:
            okj = jp_ok(k, a['jelentespont'], a.get('resz', ''))
        elif 'jp' in it:
            okj = jp_ok(k, *it['jp'])
        else:
            okj = None
        if not ab_v or not ab_j:
            elter_ab.append((az, k['strong'], 'vers' if not ab_v else '', 'jp' if not ab_j else '',
                             '%s | %s %s' % (va, a['jelentespont'], a.get('resz', '')),
                             '%s | %s %s' % (vb, b['jelentespont'], b.get('resz', '')),
                             '%s | %s %s %s' % (k['mt_vers'] or ('szurt' if k['szurt'] == '1' else '—'), k['szakasz'], k['resz'],
                                                k['utvonal'])))
        sz['vers'] += bool(okv)
        sz['jp'] += bool(okj)
        bk = k['bizonyossag'].split(':')[0]
        biz.setdefault(bk, [0, 0])
        biz[bk][0] += bool(okj)
        biz[bk][1] += 1
        if okj is False or okv is False:
            gep_hiba.append((az, k['strong'], 'vers' if okv is False else '', 'jp' if okj is False else '', k['bizonyossag'],
                             '%s %s %s %s' % (k['mt_vers'], k['szakasz'], k['resz'], k['utvonal']),
                             '%s | %s %s' % (va, a['jelentespont'], a.get('resz', ''))))
    for m in ('vers', 'jp'):
        lo, hi = wilson(sz[m], n)
        print('%s\t%d / %d\t%.1f%%\tWilson 95%%: %.1f–%.1f' % (m, sz[m], n, 100.0 * sz[m] / n, lo, hi))
    print('A: vers %d, jp %d; B: vers %d, jp %d (a gépivel)' % (sz['vers_A'], sz['jp_A'], sz['vers_B'], sz['jp_B']))
    for bk, (j, t) in sorted(biz.items()):
        print('bizonyossag %s: jp %d / %d' % (bk, j, t))
    nyitott = [e for e in elter_ab if (e[2] and 'vers' not in ITELET.get(e[0], {})) or (e[3] and 'jp' not in ITELET.get(e[0], {}))]
    print('A ≠ B: %d sor; ítélet nélkül: %d' % (len(elter_ab), len(nyitott)))
    if '--reszlet' in sys.argv:
        for e in elter_ab:
            print('AB\t' + '\t'.join(e))
        for e in gep_hiba:
            print('GEP\t' + '\t'.join(e))


if __name__ == '__main__':
    main()
