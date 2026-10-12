#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F77 — a vakpróba összevetése: effort-szintek (és a zajszint-alap, ha van) a meglévő
`f22/valaszok/sonnet/Jozs.jsonl` ugyanazon kötegeihez képest.

Bemenet (csak olvas): f22/valaszok/sonnet/<könyv>.jsonl, f22/vakproba/<effort>/<könyv>.jsonl,
f22/vakproba/subagent/<könyv>.jsonl (zajszint-alap, ha már megvan), f22/vakproba/futasnaplo.tsv.
Kimenet: stdout (táblák proveniencia-sorral) és f22/vakproba/elteresek_minta.tsv (20 sor).

Használat:
    python eszkozok/karoli_strong/api_vakproba_osszevet.py --konyv Józs [--gondolkodas-becsles]
    python eszkozok/karoli_strong/api_vakproba_osszevet.py --onteszt

A `--gondolkodas-becsles` count_tokens-hívásokkal (ingyenes) megméri a válaszszöveg tokenjeit,
és a kimeneti tokenből levonja: ez a gondolkodási token BECSLÉSE (a batch usage-ben a
gondolkodás nem külön mező).
"""

import argparse
import json
import os
import random
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_koteg  # noqa: E402
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

REF = os.path.join(tokenek.ROOT, 'f22', 'valaszok', 'sonnet')
EFFORTOK = ['low', 'medium', 'high']


def sorok(fajl):
    if not os.path.exists(fajl):
        return []
    with open(fajl, encoding='utf-8') as f:
        return [json.loads(s) for s in f if s.strip()]


def kotegek_szerint(lista):
    return {tuple(s['igehelyek']): s for s in lista}


def linkek(obj):
    return {(k, e) for k, es in obj['parok'] for e in es}


def vers_hely(v):
    return v['obj'] if v and v.get('allapot') == 'ok' else None


def hasonlit(ref, uj, kotegek):
    """A két változat összevetése a megadott kötegekre (igehelyek-tuple-ök).
    Visszaad: dict mérőszámokkal és az eltérő linkek listájával."""
    r = {'vers': 0, 'vers_osszevetett': 0, 'ref_link': 0, 'uj_link': 0, 'metszet': 0, 'unio': 0,
         'beto_metszet': 0, 'beto_unio': 0, 'ford_metszet': 0, 'ford_unio': 0,
         'elso_proba_kapuhiba_vers': 0, 'vegleges_kapuhiba_vers': 0, 'elteres': []}
    for kt in kotegek:
        a, b = ref.get(kt), uj.get(kt)
        if not b:
            continue
        for ig in kt:
            r['vers'] += 1
            vb = b['versek'].get(ig)
            if vb is None or vb['probalkozas'] != 1 or vb['allapot'] != 'ok':
                r['elso_proba_kapuhiba_vers'] += 1
            if vb is None or vb['allapot'] != 'ok':
                r['vegleges_kapuhiba_vers'] += 1
            oa, ob = vers_hely(a['versek'].get(ig)) if a else None, vers_hely(vb)
            if not oa or not ob:
                continue
            r['vers_osszevetett'] += 1
            la, lb = linkek(oa), linkek(ob)
            r['ref_link'] += len(la)
            r['uj_link'] += len(lb)
            r['metszet'] += len(la & lb)
            r['unio'] += len(la | lb)
            for kulcs, pre in (('betoldas', 'beto'), ('forditatlan', 'ford')):
                sa, sb = set(oa.get(kulcs) or []), set(ob.get(kulcs) or [])
                r[pre + '_metszet'] += len(sa & sb)
                r[pre + '_unio'] += len(sa | sb)
            for l in sorted(la - lb):
                r['elteres'].append((ig, l, 'csak_ref'))
            for l in sorted(lb - la):
                r['elteres'].append((ig, l, 'csak_uj'))
    return r


def szazalek(a, b):
    return '%.2f%%' % (100.0 * a / b) if b else '-'


def naplo_sorok():
    return api_koteg.tsv_olvas(api_koteg.ut('futasnaplo.tsv'))


def tokenek_tabla(konyv):
    k = tokenek.betolt_karoli()
    e = tokenek.betolt_eredeti()
    return k, e


def kivetites(usd_vers_effort):
    """Hátralevő ÓSZ-versek: az eredeti-oldal H-Strongos versei, a kész könyvek (f22/valaszok/sonnet) nélkül."""
    kesz = set()
    for f in os.listdir(REF):
        if f.endswith('.jsonl') and 'javito' not in f:
            for s in sorok(os.path.join(REF, f)):
                kesz.update(s['igehelyek'])
    ered = tokenek.betolt_eredeti()
    osz = [ig for ig, t in ered.items() if t and str(t[0].get('strong', '')).startswith('H')]
    hatra = [ig for ig in osz if ig not in kesz]
    return len(osz), len(kesz), len(hatra)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', default='Józs')
    ap.add_argument('--gondolkodas-becsles', action='store_true')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        return onteszt()
    ref = kotegek_szerint(sorok(os.path.join(REF, '%s.jsonl' % sonnet_koteg.ascii_nev(a.konyv))))
    ts = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime())
    prov = 'scope=f22/valaszok/sonnet/%s.jsonl vs f22/vakproba/<változat>/ | forras=api_vakproba_osszevet.py | ts=%s' % (
        sonnet_koteg.ascii_nev(a.konyv), ts)
    valtozatok = {}
    for e in EFFORTOK:
        valtozatok['api-' + e] = kotegek_szerint(sorok(api_koteg.jsonl_ut(a.konyv, e)))
    sub = kotegek_szerint(sorok(os.path.join(api_koteg.VAKPROBA, 'subagent', '%s.jsonl' % sonnet_koteg.ascii_nev(a.konyv))))
    if sub:
        valtozatok['subagent (zajszint-alap)'] = sub
    kotegek = sorted(set().union(*[set(v) for v in valtozatok.values()]) & set(ref), key=lambda t: t[0])
    print('# F77 vakpróba — összevetés (%s, %d köteg a referenciában közös)\n' % (a.konyv, len(kotegek)))
    eredm = {}
    for nev, v in valtozatok.items():
        eredm[nev] = hasonlit(ref, v, [k for k in kotegek if k in v])
    print('## 1. Egyezés a meglévő futással\n')
    print('| változat | vers | link-egyezés (metszet/unió) | ref-link lefedés | betoldas-egyezés | forditatlan-egyezés |')
    print('|---|---|---|---|---|---|')
    for nev, r in eredm.items():
        print('| %s | %d | %s (%d/%d) | %s | %s | %s |' % (
            nev, r['vers_osszevetett'], szazalek(r['metszet'], r['unio']), r['metszet'], r['unio'],
            szazalek(r['metszet'], r['ref_link']), szazalek(r['beto_metszet'], r['beto_unio']),
            szazalek(r['ford_metszet'], r['ford_unio'])))
    if not sub:
        print('\n*Zajszint-alap (subagent): hiányzik, orkesztrátorra vár.*')
    print('\n*proveniencia: %s*\n' % prov)
    print('## 2. Kapuhiba (versszinten)\n')
    print('| változat | vers | első próbára hibás | végleges kapuhiba |')
    print('|---|---|---|---|')
    for nev, r in eredm.items():
        print('| %s | %d | %d | %d |' % (nev, r['vers'], r['elso_proba_kapuhiba_vers'], r['vegleges_kapuhiba_vers']))
    print('\n*proveniencia: %s*\n' % prov)

    naplo = [s for s in naplo_sorok() if s['probalkozas'] == '1' or True]
    print('## 3. Token és költség (Batch-áron, f22/vakproba/futasnaplo.tsv)\n')
    becsl = {}
    if a.gondolkodas_becsles:
        for e in EFFORTOK:
            for s in sorok(api_koteg.jsonl_ut(a.konyv, e)):
                for i, ny in enumerate(s['nyers']):
                    becsl[(e, s['koteg'], i + 1)] = api_koteg.http('POST', '/v1/messages/count_tokens', {
                        'model': api_koteg.MODELL, 'messages': [{'role': 'user', 'content': ny or ' '}]})['input_tokens']
    print('| effort | hívás | bemenet/hívás (átl.) | kimenet/hívás (átl.) | kimenet max. | gondolkodás becsült (átl./max.) | USD összesen | vers | USD/vers |')
    print('|---|---|---|---|---|---|---|---|---|')
    usd_vers = {}
    for e in EFFORTOK:
        rs = [s for s in naplo if s['futas'].split('/')[1] == e]
        if not rs:
            continue
        ki = [int(s['kimenet_token']) for s in rs]
        be = [int(s['bemenet_token']) for s in rs]
        usd = sum(float(s['koltseg_usd']) for s in rs)
        vers = sum(int(s['igehely_db']) for s in rs if s['probalkozas'] == '1')
        g = ['%d' % (int(s['kimenet_token']) - (becsl.get((e, int(s['koteg']), int(s['probalkozas'])), 0) or 0))
             for s in rs] if becsl else []
        gt = '%.0f / %d' % (sum(map(int, g)) / len(g), max(map(int, g))) if g else 'nem mért (--gondolkodas-becsles)'
        usd_vers[e] = usd / vers if vers else None
        print('| %s | %d | %.0f | %.0f | %d | %s | %.4f | %d | %.5f |' % (
            e, len(rs), sum(be) / len(be), sum(ki) / len(ki), max(ki), gt, usd, vers, usd / vers))
    osszes = sum(float(s['koltseg_usd']) for s in naplo)
    print('\nA teljes próba költsége: %.4f USD (plafon %.2f USD).' % (osszes, api_koteg.PLAFON_USD))
    print('\n*proveniencia: scope=f22/vakproba/futasnaplo.tsv | forras=api_koteg.py (Batch-ár: %.2f/%.2f USD/MTok be/ki) | ts=%s*\n' % (
        api_koteg.AR_BE, api_koteg.AR_KI, ts))
    osz, kesz, hatra = kivetites(usd_vers)
    print('## 4. Kivetítés a hátralevő ÓSZ-versekre\n')
    print('ÓSZ-vers (eredeti-oldal, H-Strong): %d; kész (f22/valaszok/sonnet): %d; hátralevő: %d.\n' % (osz, kesz, hatra))
    print('| effort | USD/vers | hátralevő ÓSZ (USD) | hány ilyen mennyiség fér a havi 100 USD-be |')
    print('|---|---|---|---|')
    for e, u in usd_vers.items():
        if u:
            print('| %s | %.5f | %.2f | %.1f |' % (e, u, u * hatra, 100.0 / (u * hatra)))
    print('\n*proveniencia: scope=tokenek.betolt_eredeti + f22/valaszok/sonnet/*.jsonl | forras=api_vakproba_osszevet.py | ts=%s*\n' % ts)

    # eltérés-minta: 20 sor, effortonként arányosan, rögzített maggal
    k, e_t = tokenek_tabla(a.konyv)
    pool = []
    for nev, r in eredm.items():
        for ig, l, irany in r['elteres']:
            pool.append((nev, ig, l, irany))
    rnd = random.Random(77)
    minta = rnd.sample(pool, min(20, len(pool)))
    fajl = api_koteg.ut('elteresek_minta.tsv')
    os.makedirs(os.path.dirname(fajl), exist_ok=True)
    with open(fajl, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['valtozat', 'vers', 'karoli_token', 'karoli_szo', 'eredeti_token', 'eredeti_alak', 'irany']) + '\n')
        for nev, ig, (kt, et), irany in sorted(minta):
            tk = tokenek.tokenizal(k[ig])
            ed = e_t.get(ig, [])
            szo = tk[kt - 1] if 1 <= kt <= len(tk) else '?'
            al = next((x['alak'] for x in ed if x['sorsz'] == et), '?')
            f.write('\t'.join([nev, ig, str(kt), szo, str(et), al,
                               'csak a meglévő futásban' if irany == 'csak_ref' else 'csak az új változatban']) + '\n')
    print('## 5. Eltérő linkek\n\nÖsszes eltérő link (minden változat): %d; 20-as minta kézi átnézésre: %s' % (len(pool), fajl))
    print('\n*proveniencia: scope=%s | forras=api_vakproba_osszevet.py (random.Random(77)) | ts=%s*' % (fajl, ts))
    return 0


def onteszt():
    hibak = []

    def sor(igek, parok, allap='ok', pr=1):
        return {'igehelyek': igek, 'versek': {i: {'allapot': allap, 'probalkozas': pr, 'hibak': [],
                                                  'obj': {'vers': i, 'parok': parok, 'betoldas': [1], 'forditatlan': []}} for i in igek}}
    ref = {('a', 'b'): sor(['a', 'b'], [[1, [1]], [2, [2]]])}
    uj = {('a', 'b'): sor(['a', 'b'], [[1, [1]], [2, [3]]])}
    r = hasonlit(ref, uj, [('a', 'b')])
    # versenként 2 ref-link, 1 közös, unió 3 -> 2 vers: metszet 2, unió 6
    if (r['metszet'], r['unio'], r['ref_link'], len(r['elteres'])) != (2, 6, 4, 4):
        hibak.append('link-egyezés %s' % [r['metszet'], r['unio'], r['ref_link'], len(r['elteres'])])
    if r['beto_metszet'] != 2 or r['beto_unio'] != 2:
        hibak.append('betoldas')
    uj2 = {('a', 'b'): sor(['a', 'b'], [], 'kapuhiba', 2)}
    r2 = hasonlit(ref, uj2, [('a', 'b')])
    if r2['elso_proba_kapuhiba_vers'] != 2 or r2['vegleges_kapuhiba_vers'] != 2 or r2['vers_osszevetett'] != 0:
        hibak.append('kapuhiba-számlálás')
    if szazalek(1, 4) != '25.00%' or szazalek(1, 0) != '-':
        hibak.append('százalék')
    for h in hibak:
        print('ÖNTESZT HIBA: ' + h, file=sys.stderr)
    print('önteszt: %s' % ('HIBA' if hibak else 'rendben'))
    return 1 if hibak else 0


if __name__ == '__main__':
    sys.exit(main())
