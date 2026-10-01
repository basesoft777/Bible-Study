#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 22.5 — ellenőrzés a könyvön: a jelentés 2. szakaszának számai (csak szkriptkimenetből).

Olvas: adat/karoli_strong/parok_<könyv>.tsv, szavak_<könyv>.tsv, f22/valaszok/{sonnet,c}/<könyv>.jsonl,
konkordancia/Karoli_Strong_kivonat.tsv (régi arany), f21p/regi_arany_hibas.tsv, Karoli_1908.tsv, TAHOT.
Nem hív hálózatot, nem ír fájlt; a Markdown a standard kimenetre megy.

  1. Arányok: magas / alacsony / kezi, linkek és szavak szerint, fejezetenként is.
  2. Régi arany: a Karoli_Strong_kivonat.tsv könyv-sorainak egyezése (halmaz-definíció: az összetett Strong
     minden összetevője a Károli-szóhoz linkelt eredeti Strongok között; kizárás nélkül mért érték; az
     f21p/regi_arany_hibas.tsv sorai csak tájékoztatásul), külön a `magas` linkekre.
  3. A leggyakoribb eltérés-típusok az alacsony tokenekből (két modell eltérő partnerhalmaza).

Használat:
    python eszkozok/karoli_strong/f22_elemzes.py --konyv 1Móz
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import egyesit  # noqa: E402
import tokenek  # noqa: E402

TOP = 20


def pct(a, b):
    return '%.1f%% (%d/%d)' % (100.0 * a / b, a, b) if b else 'n.é. (0/0)'


def fejezet(vers):
    return int(vers.split(' ')[1].split(':')[0])


def aranyok(parok, szavak):
    ki = ['### 2.1 Arányok', '']
    ossz = {'magas': 0, 'alacsony': 0, 'kezi': 0}
    for r in parok:
        ossz[r['bizonyossag']] += 1
    szossz = {'magas': 0, 'alacsony': 0, 'kezi': 0}
    for r in szavak:
        szossz[r['bizonyossag']] += 1
    n, sn = sum(ossz.values()), sum(szossz.values())
    ki.append('Összesen: linkek (parok): magas %s, alacsony %s, kezi %s; szavak (tokenek, Károli és eredeti együtt): '
              'magas %s, alacsony %s, kezi %s.' % (pct(ossz['magas'], n), pct(ossz['alacsony'], n), pct(ossz['kezi'], n),
                                                 pct(szossz['magas'], sn), pct(szossz['alacsony'], sn), pct(szossz['kezi'], sn)))
    fl_forras = {}
    for r in parok:
        fl_forras[r['forras']] = fl_forras.get(r['forras'], 0) + 1
    egymodelles = sorted({r['vers'] for r in szavak if r['forras'] in ('S', 'C') and r['bizonyossag'] != 'kezi'} -
                         {r['vers'] for r in szavak if r['forras'] == 'S+C'})
    ki.append('')
    ki.append('Link-forrás megoszlás (parok): %s. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: %d%s.' % (
        ', '.join('%s %d' % (k, v) for k, v in sorted(fl_forras.items())), len(egymodelles),
        (' (' + ', '.join(egymodelles[:10]) + ')') if egymodelles else ''))
    ki += ['', '| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |', '|---|---|---|---|---|---|---|---|---|']
    fl, fs = {}, {}
    for r in parok:
        d = fl.setdefault(fejezet(r['vers']), {'magas': 0, 'alacsony': 0, 'kezi': 0})
        d[r['bizonyossag']] += 1
    for r in szavak:
        d = fs.setdefault(fejezet(r['vers']), {'magas': 0, 'alacsony': 0, 'kezi': 0})
        d[r['bizonyossag']] += 1
    for f in sorted(fs):
        a = fl.get(f, {'magas': 0, 'alacsony': 0, 'kezi': 0})
        b = fs[f]
        la, sb = sum(a.values()), sum(b.values())
        ki.append('| %d | %d | %s | %s | %s | %d | %s | %s | %s |' % (
            f, la, pct(a['magas'], la), pct(a['alacsony'], la), pct(a['kezi'], la), sb,
            pct(b['magas'], sb), pct(b['alacsony'], sb), pct(b['kezi'], sb)))
    return ki


def kifejezes_helyek(tl, kif):
    n = len(kif)
    if n == 0:
        return []
    kif = [t.casefold() for t in kif]
    tl = [t.casefold() for t in tl]
    return [i for i in range(len(tl) - n + 1) if tl[i:i + n] == kif]


def regi_hibas():
    ut = os.path.join(tokenek.ROOT, 'f21p', 'regi_arany_hibas.tsv')
    if not os.path.exists(ut):
        return set()
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return {(d['igehely'], d['karoli_szo'], d['strong']) for d in (dict(zip(fej, s.split('\t'))) for s in sorok[1:])}


def regi_arany(konyv, parok, szavak, karoli, ered):
    ki = ['### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)', '']
    hu_all, hu_mag, tok_mag = {}, {}, {}
    for r in parok:
        ig, h, e = r['vers'], int(r['hu_sorszam']), int(r['er_sorszam'])
        st = ered[ig][e - 1]['strong']
        hu_all.setdefault((ig, h), set()).add(st)
        if r['bizonyossag'] == 'magas':
            hu_mag.setdefault((ig, h), set()).add(st)
    for r in szavak:
        if r['oldal'] == 'hu':
            tok_mag[(r['vers'], int(r['sorszam']))] = r['bizonyossag'] == 'magas'
    versek = {ig for ig in karoli if ig.startswith(konyv + ' ')}
    gold = [t for t in tokenek.regi_arany(versek)]
    hibas = regi_hibas()
    n = nincs = e_all = e_mag = 0
    n_t = e_t = 0           # magas tokenű előfordulásra korlátozva (pontosság a magas halmazon)
    n_k = e_k = 0           # kizárás (tájékoztató)
    for ig, szo, strong in gold:
        n += 1
        tl = tokenek.tokenizal(karoli[ig])
        kif = tokenek.tokenizal(szo)
        helyek = kifejezes_helyek(tl, kif)
        if not helyek:
            nincs += 1
            continue
        osszetevok = set(strong.split('+'))

        def egyezik(halmaz, szuro=None):
            for i in helyek:
                if szuro is not None and not all(szuro((ig, i + j + 1)) for j in range(len(kif))):
                    continue
                linkelt = set()
                for j in range(len(kif)):
                    linkelt |= halmaz.get((ig, i + j + 1), set())
                if osszetevok <= linkelt:
                    return True
            return False
        a = egyezik(hu_all)
        m = egyezik(hu_mag)
        e_all += a
        e_mag += m
        # magas tokenek: van olyan előfordulás, ahol minden érintett Károli-token `magas`
        van_magas = any(all(tok_mag.get((ig, i + j + 1), False) for j in range(len(kif))) for i in helyek)
        if van_magas:
            n_t += 1
            e_t += egyezik(hu_all, lambda k: tok_mag.get(k, False))
        if (ig, szo, strong) not in hibas:
            n_k += 1
            e_k += a
    ki.append('- Minden régi-arany hármas a könyvben: %d; a Károli-szó/kifejezés nem található a vers tokenjei közt: %d.' % (n, nincs))
    ki.append('- **Mért érték (kizárás nélkül, minden link):** %s.' % pct(e_all, n))
    ki.append('- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): %s.' % pct(e_mag, n))
    ki.append('- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a '
              'találat a `magas` token linkjein): %s.' % pct(e_t, n_t))
    ki.append('- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): %s.' % pct(e_k, n_k))
    return ki


def eltérések(konyv, karoli, ered):
    ki = ['### 2.3 A %d leggyakoribb eltérés-típus az alacsony tokenekből' % TOP, '']
    n = egyesit.sonnet_koteg.ascii_nev(konyv)
    sv = egyesit.jsonl_versek(os.path.join(tokenek.ROOT, 'f22', 'valaszok', 'sonnet', '%s.jsonl' % n))
    cv = egyesit.jsonl_versek(os.path.join(tokenek.ROOT, 'f22', 'valaszok', 'c', '%s.jsonl' % n))
    tipusok = {}
    osszes_elteres = 0
    for ig in sv:
        if sv[ig]['allapot'] != 'ok' or cv.get(ig, {}).get('allapot') != 'ok':
            continue
        sn, cn = egyesit.vers_nezet(sv[ig]['obj']), egyesit.vers_nezet(cv[ig]['obj'])
        tl = tokenek.tokenizal(karoli[ig])
        for h, szo in enumerate(tl, 1):
            sp, cp = sn[0].get(h, frozenset()), cn[0].get(h, frozenset())
            if sp == cp:
                continue
            osszes_elteres += 1

            def jel(p):
                if not p:
                    return 'betoldas'
                return '+'.join(sorted({ered[ig][e - 1]['strong'] for e in p}))
            kulcs = (szo.casefold(), jel(sp), jel(cp))
            d = tipusok.setdefault(kulcs, {'db': 0, 'pelda': ig})
            d['db'] += 1
    ki.append('Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: %d; különböző típus (magyar szó, Sonnet-jelölt, '
              'C-jelölt): %d. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.' % (osszes_elteres, len(tipusok)))
    ki += ['', '| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |', '|---|---|---|---|---|---|']
    rend = sorted(tipusok.items(), key=lambda kv: (-kv[1]['db'], kv[0]))
    for i, (k, d) in enumerate(rend[:TOP], 1):
        ki.append('| %d | %s | %s | %s | %d | %s |' % (i, k[0], k[1], k[2], d['db'], d['pelda']))
    return ki


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', required=True)
    a = ap.parse_args(argv)
    u = egyesit.utak(a.konyv)
    parok, szavak = egyesit.olvas(u['parok']), egyesit.olvas(u['szavak'])
    karoli, ered = tokenek.betolt_karoli(), tokenek.betolt_eredeti()
    sor = ['## 2. Ellenőrzés a könyvön (22.5)', '',
           '*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv %s` kimenetéből.*' % a.konyv, '']
    sor += aranyok(parok, szavak) + [''] + regi_arany(a.konyv, parok, szavak, karoli, ered) + [''] + eltérések(a.konyv, karoli, ered)
    print('\n'.join(sor))
    return 0


if __name__ == '__main__':
    sys.exit(main())
