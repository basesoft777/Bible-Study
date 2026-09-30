#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.14 — a v2-mérés váza: F3 (v1 prompt) és F3V2 (prompt_v2) az arany v1/v2-höz.

Hívás: python eszkozok/karoli_strong/meres.py --v2   (vagy közvetlenül ez a modul).
A meres.py függvényeit és definícióit használja (meres.Adat, linkek, kizárás,
regi_egyezik halmaz-definíció, regi_hibas, hibatipusok), tehát a számok a P4-gyel
azonos definíciójúak.

Összeállítások (oszlopok):
  * F3 × arany v1   — a P4 C-száma (kontroll; egyeznie kell a meres_eredmeny.tsv-vel);
  * F3 × arany v2   — a C-diff 7. pontjának mért száma;
  * F3V2 × arany v2 — az új futás (f21p/valaszok/F3V2.jsonl).
Az arany v2 befagyasztott: betöltéskor a sha256 ellenőrzése
(tokenek.arany_v2_befagyasztas_ellenoriz), eltérésnél hibával megáll.

Mérőszámok rétegenként (R1–R4, Összes): pontosság, lefedettség (a kapun átment
aranyversekre), régi arany egyezés (halmaz-definíció; kizárás nélkül és a hibás
hármasok nélkül); kapuhiba-arány első próbára és végleg; költség (cost, tokenek,
gondolkodási token a futásnaplóból és — ahol a jsonl tárolja — a nyers usage-ból);
hibatípusok kapupont szerint.

Küszöb-viszonyítás (a brief „Döntési szabály”-a, P2-n rögzítve): lefedettség ≥ 95%,
régi arany ≥ 95%; a `magas` pontosság ≥ 98% egymodelles összeállításra NEM
értelmezhető (PD6), ezért az összpontosság csak tájékoztatásul áll a 98% mellett.
Egymodelles összeállítás (C egyedül) nem kaphat „megfelelt” minősítést (PD6): a
jelentés csak a mért számot és a küszöbhöz való viszonyát írja, minősítést nem.

Kimenet: naplok/F21P_meres_v2.md és f21p/meres_v2_eredmeny.tsv (generált).
Ha az F3V2 még nem futott (nincs f21p/valaszok/F3V2.jsonl), hibaüzenettel
(kilépési kód 2) áll meg, és nem ír.

Önteszt (mock-adattal, éles adat nélkül; ideiglenes könyvtárba ír):
    python eszkozok/karoli_strong/meres_v2.py --onteszt
"""

import json
import os
import shutil
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meres  # noqa: E402
import tokenek  # noqa: E402

V2_FUTASOK = ['F3', 'F3V2']
OSSZEALLITASOK = [('F3 × arany v1', 'F3', 'v1'), ('F3 × arany v2', 'F3', 'v2'), ('F3V2 × arany v2', 'F3V2', 'v2')]
FUTAS_OSZLOPOK = [('F3 (prompt v1)', 'F3'), ('F3V2 (prompt v2)', 'F3V2')]
RETEGEK = meres.RETEGEK + [meres.OSSZES]
KUSZOB_LEFEDETTSEG = 0.95
KUSZOB_REGI = 0.95
KUSZOB_MAGAS = 0.98
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_meres_v2.md')
EREDMENY_UT = os.path.join(tokenek.ROOT, 'f21p', 'meres_v2_eredmeny.tsv')


class HianyzoFutas(Exception):
    pass


def betolt(forras_dir=None):
    forras_dir = forras_dir or meres.F21P
    for f in V2_FUTASOK:
        ut = os.path.join(forras_dir, 'valaszok', '%s.jsonl' % f)
        if not os.path.exists(ut):
            raise HianyzoFutas('nincs %s (a futás még nem történt meg)' % ut)
    adat = meres.Adat(futasok=V2_FUTASOK, forras_dir=forras_dir)
    tokenek.arany_v2_befagyasztas_ellenoriz()
    v2 = {o['vers']: o for o in meres._jsonl(tokenek.ARANY_V2)}
    g = {'v1': adat.arany_linkek,
         'v2': lambda ig: adat._szur(ig, {(p[0], e) for p in v2[ig]['parok'] for e in p[1]})}
    return adat, g


def _retegben(adat, ig, ret):
    return ret == meres.OSSZES or adat.reteg[ig] == ret


def pont_lef(adat, f, g_fn, ret):
    arany_versek = [ig for ig in adat.versek if ig in adat.arany and _retegben(adat, ig, ret)]
    vs = [ig for ig in arany_versek if adat.ok(f, ig)]
    c = g = t = 0
    for ig in vs:
        cl, gl = adat.linkek(f, ig), g_fn(ig)
        c += len(cl)
        g += len(gl)
        t += len(cl & gl)
    return {'versek_ok': len(vs), 'versek': len(arany_versek), 'talalat': t, 'modell': c, 'arany': g}


def regi(adat, f, ret):
    hibas = meres.regi_hibas()
    hb = e = hb_k = e_k = 0
    for ig, szo, strong in adat.regi:
        if not _retegben(adat, ig, ret) or not adat.ok(f, ig):
            continue
        _, egy = meres.regi_egyezik(adat, ig, szo, strong, adat.linkek(f, ig))
        hb += 1
        e += egy
        if (ig, szo, strong) not in hibas:
            hb_k += 1
            e_k += egy
    return {'hb': hb, 'egyezik': e, 'hb_k': hb_k, 'egyezik_k': e_k}


def kapuhiba(adat, f, ret):
    _, _, elso_hibas = meres.hibatipusok(adat, f)
    vs = [ig for ig in adat.versek if ig in adat.futas[f] and _retegben(adat, ig, ret)]
    return {'versek': len(vs), 'elso': sum(1 for ig in vs if ig in elso_hibas),
            'vegleg': sum(1 for ig in vs if adat.futas[f][ig]['allapot'] != 'ok')}


def koltseg(adat, f):
    import futtat
    sor = [r for r in adat.naplo if r['futas'] == f]
    usage_gond = None
    kotegek = adat.kotegsorok[f]
    if kotegek and all('hivasok' in s for s in kotegek):
        usage_gond = sum(futtat.gondolkodas_token(h.get('usage') or {}) for s in kotegek for h in s['hivasok'])
    return {
        'hivas': len(sor),
        'hivas_p2': sum(1 for r in sor if r['probalkozas'] == '2'),
        'bemenet': sum(int(r['bemenet_token']) for r in sor),
        'kimenet': sum(int(r['kimenet_token']) for r in sor),
        'gond_naplo': sum(int(r['gondolkodas_token']) for r in sor),
        'gond_usage': usage_gond,
        'cost': round(sum(float(r['koltseg_usd']) for r in sor), 6),
        'forras': ','.join(sorted({r['koltseg_forras'] for r in sor})),
        'mod': '; '.join(sorted({r['gondolkodas_mod'] for r in sor})),
        'prompt': ','.join(sorted({r['prompt_sha256_12'] for r in sor})),
    }


def szamol(adat, g):
    ki = {'pont': {}, 'regi': {}, 'kapu': {}, 'koltseg': {}, 'tipus': {}}
    for nev, f, a in OSSZEALLITASOK:
        for ret in RETEGEK:
            ki['pont'][(nev, ret)] = pont_lef(adat, f, g[a], ret)
    for _, f in FUTAS_OSZLOPOK:
        for ret in RETEGEK:
            ki['regi'][(f, ret)] = regi(adat, f, ret)
            ki['kapu'][(f, ret)] = kapuhiba(adat, f, ret)
        ki['koltseg'][f] = koltseg(adat, f)
        elso, vegleg, _ = meres.hibatipusok(adat, f)
        ki['tipus'][f] = (elso, vegleg, len(adat.futas[f]))
    return ki


def _pct(x, n, wilson=False):
    if not n:
        return '— (0/0)'
    s = '%.1f%% (%d/%d)' % (100.0 * x / n, x, n)
    if wilson:
        w = meres.wilson(x, n)
        s += ' [%.0f–%.0f]' % (100 * w[0], 100 * w[1])
    return s


def _viszony(x, n, kuszob):
    if not n:
        return 'n.é.'
    return 'elérve (≥ %.0f%%)' % (100 * kuszob) if x / n >= kuszob else 'küszöb alatt (< %.0f%%)' % (100 * kuszob)


def md_ir(ki, ut=JELENTES_UT):
    fej = ['# F21P_meres_v2.md — F3 (prompt v1) és F3V2 (prompt v2) az arany v1/v2-höz', '',
           '<!-- GENERÁLT: eszkozok/karoli_strong/meres_v2.py (meres.py --v2) | scope=f21p F3, F3V2 | '
           'forras=f21p/valaszok/F3.jsonl, f21p/valaszok/F3V2.jsonl, f21p/arany_opus.jsonl, '
           'f21p/arany_opus_v2.jsonl (befagyasztva, sha256 ellenőrizve), f21p/meres_kizaras.tsv, '
           'f21p/regi_arany_hibas.tsv, f21p/futasnaplo.tsv | kézzel szerkeszteni tilos -->', '',
           'Kizárólag szkriptkimenet, a meres.py definícióival. **Egymodelles összeállítás (a C egyedül) nem '
           'kaphat „megfelelt” minősítést (PD6):** a táblák a mért számot és a rögzített küszöbhöz való '
           'viszonyát adják, minősítést nem. A `magas` pontosság (≥ 98%) egymodelles összeállításra nem '
           'értelmezhető; az összpontosság a 98% mellett csak tájékoztató. A korrigált (Opus-besorolásos) érték '
           'nem része ennek a jelentésnek (l. naplok/F21P_C_diff.md; az „az Opus besorolása, nem mérés”).', '']
    ki_s = fej
    ki_s += ['## a) Pontosság és lefedettség (kapun átment aranyversek)', '',
             '| réteg | mérőszám | ' + ' | '.join(n for n, _, _ in OSSZEALLITASOK) + ' |',
             '|---|---|' + '---|' * len(OSSZEALLITASOK)]
    for ret in RETEGEK:
        p = [ki['pont'][(n, ret)] for n, _, _ in OSSZEALLITASOK]
        ki_s.append('| %s | aranyversek kapun átment | %s |' % (ret, ' | '.join(_pct(x['versek_ok'], x['versek']) for x in p)))
        ki_s.append('| %s | pontosság (tájékoztató a 98%% mellett, PD6) | %s |' % (ret, ' | '.join(_pct(x['talalat'], x['modell'], True) for x in p)))
        ki_s.append('| %s | lefedettség | %s |' % (ret, ' | '.join(_pct(x['talalat'], x['arany'], True) for x in p)))
        ki_s.append('| %s | lefedettség vs küszöb 95%% | %s |' % (ret, ' | '.join(_viszony(x['talalat'], x['arany'], KUSZOB_LEFEDETTSEG) for x in p)))
    ki_s.append('')
    ki_s += ['## b) Régi arany egyezés (halmaz-definíció; kapun átment versek, 200 verses minta)', '',
             '| réteg | mérőszám | ' + ' | '.join(n for n, _ in FUTAS_OSZLOPOK) + ' |', '|---|---|' + '---|' * len(FUTAS_OSZLOPOK)]
    for ret in RETEGEK:
        r = [ki['regi'][(f, ret)] for _, f in FUTAS_OSZLOPOK]
        ki_s.append('| %s | egyezés, kizárás nélkül | %s |' % (ret, ' | '.join(_pct(x['egyezik'], x['hb'], True) for x in r)))
        ki_s.append('| %s | egyezés, a hibás hármasok nélkül | %s |' % (ret, ' | '.join(_pct(x['egyezik_k'], x['hb_k'], True) for x in r)))
        ki_s.append('| %s | (hibás nélkül) vs küszöb 95%% | %s |' % (ret, ' | '.join(_viszony(x['egyezik_k'], x['hb_k'], KUSZOB_REGI) for x in r)))
    ki_s.append('')
    ki_s += ['## c) Kapuhiba-arány', '',
             '| réteg | mérőszám | ' + ' | '.join(n for n, _ in FUTAS_OSZLOPOK) + ' |', '|---|---|' + '---|' * len(FUTAS_OSZLOPOK)]
    for ret in RETEGEK:
        k = [ki['kapu'][(f, ret)] for _, f in FUTAS_OSZLOPOK]
        ki_s.append('| %s | első próbára | %s |' % (ret, ' | '.join(_pct(x['elso'], x['versek']) for x in k)))
        ki_s.append('| %s | végleg | %s |' % (ret, ' | '.join(_pct(x['vegleg'], x['versek']) for x in k)))
    ki_s.append('')
    ki_s += ['## d) Költség (futásnapló; a gondolkodási token külön oszlop)', '',
             '| futás | hívás (ebből újrakérés) | bemeneti token | kimeneti token | gondolkodási token (napló) | '
             'gondolkodási token (jsonl nyers usage) | cost USD | cost-forrás | gondolkodási mód | prompt sha256[:12] |',
             '|---|---|---|---|---|---|---|---|---|---|']
    for n, f in FUTAS_OSZLOPOK:
        c = ki['koltseg'][f]
        ki_s.append('| %s | %d (%d) | %d | %d | %d | %s | %.6f | %s | %s | %s |' % (
            n, c['hivas'], c['hivas_p2'], c['bemenet'], c['kimenet'], c['gond_naplo'],
            'n.é. (a futás nem tárolta a nyers usage-ot)' if c['gond_usage'] is None else c['gond_usage'],
            c['cost'], c['forras'], c['mod'], c['prompt']))
    ki_s.append('')
    ki_s += ['## e) Hibatípusok kapupont szerint (hibás versek száma)', '',
             '| kapupont | ' + ' | '.join('%s első próbára | %s végleg' % (n, n) for n, _ in FUTAS_OSZLOPOK) + ' |',
             '|---|' + '---|---|' * len(FUTAS_OSZLOPOK)]
    pontok = sorted({p for _, f in FUTAS_OSZLOPOK for d in ki['tipus'][f][:2] for p in d})
    for p in pontok:
        cellak = []
        for _, f in FUTAS_OSZLOPOK:
            elso, vegleg, n = ki['tipus'][f]
            cellak += [_pct(elso.get(p, 0), n), _pct(vegleg.get(p, 0), n)]
        ki_s.append('| %s | %s |' % (p, ' | '.join(cellak)))
    ki_s.append('')
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(ki_s) + '\n')


def tsv_ir(ki, ut=EREDMENY_UT):
    sorok = ['# GENERÁLT: eszkozok/karoli_strong/meres_v2.py | scope=f21p F3, F3V2 | kézzel szerkeszteni tilos',
             '\t'.join(['szakasz', 'osszeallitas', 'reteg', 'mero', 'szamlalo', 'nevezo'])]
    for (n, ret), x in ki['pont'].items():
        sorok += ['\t'.join(['pontossag_lefedettseg', n, ret, 'pontossag', str(x['talalat']), str(x['modell'])]),
                  '\t'.join(['pontossag_lefedettseg', n, ret, 'lefedettseg', str(x['talalat']), str(x['arany'])])]
    for (f, ret), x in ki['regi'].items():
        sorok += ['\t'.join(['regi_arany', f, ret, 'egyezes', str(x['egyezik']), str(x['hb'])]),
                  '\t'.join(['regi_arany', f, ret, 'egyezes_hibas_kizarva', str(x['egyezik_k']), str(x['hb_k'])])]
    for (f, ret), x in ki['kapu'].items():
        sorok += ['\t'.join(['kapuhiba', f, ret, 'elso_probara', str(x['elso']), str(x['versek'])]),
                  '\t'.join(['kapuhiba', f, ret, 'vegleg', str(x['vegleg']), str(x['versek'])])]
    for f, c in ki['koltseg'].items():
        for k in ('hivas', 'bemenet', 'kimenet', 'gond_naplo', 'gond_usage', 'cost'):
            sorok.append('\t'.join(['koltseg', f, '-', k, str(c[k]), '']))
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(sorok) + '\n')


def fut(forras_dir=None, jelentes=JELENTES_UT, eredmeny=EREDMENY_UT):
    try:
        adat, g = betolt(forras_dir)
    except HianyzoFutas as e:
        print('HIBA: %s; a v2-mérés a F3V2 futás után indítható' % e, file=sys.stderr)
        return 2, None
    ki = szamol(adat, g)
    md_ir(ki, jelentes)
    tsv_ir(ki, eredmeny)
    print('kész -> %s, %s' % (jelentes, eredmeny))
    return 0, ki


# ---------------------------------------------------------------------------
# mock F3V2 (önteszt; a c_diff.py --f3v2 --onteszt is ezt használja)
# ---------------------------------------------------------------------------

MOCK_HIANYZO_VERS = None   # az első R1-es aranyvers (a mock egy linket elhagy)
MOCK_KAPUHIBA_VERS = None  # egy nem-arany vers (a mock kapuhibásnak jelöli)
MOCK_GOND = 100            # mock gondolkodási token hívásonként


def mock_forras(mappa, elkerul=()):
    """Ideiglenes forrás: a valódi F3 (jsonl + napló-sorok) és egy mock F3V2.

    A mock F3V2 = az arany v2 minden aranyversre (egy link elhagyásával az R1-es
    aranyversek közül, az `elkerul` kulcsokat kerülve), a többi versre a valódi F3 kapun átment válasza; egy
    nem-arany vers végleges kapuhiba (első és második próba is hibás). Visszaad:
    {'hianyzo': (ig, k, e), 'kapuhiba': ig, 'hivas': n, 'cost': x}."""
    tokenek.arany_v2_befagyasztas_ellenoriz()
    v2 = {o['vers']: o for o in meres._jsonl(tokenek.ARANY_V2)}
    os.makedirs(os.path.join(mappa, 'valaszok'), exist_ok=True)
    shutil.copy(os.path.join(meres.F21P, 'valaszok', 'F3.jsonl'), os.path.join(mappa, 'valaszok', 'F3.jsonl'))
    with open(os.path.join(meres.F21P, 'futasnaplo.tsv'), encoding='utf-8') as fh:
        naplo = [s.rstrip('\n').rstrip('\r') for s in fh if s.strip()]
    fej = naplo[0].split('\t')
    i_f = fej.index('futas')
    f3_sorok = [s for s in naplo[1:] if s.split('\t')[i_f] == 'F3']
    minta = meres._tsv(meres.MINTA_UT)
    f3 = {}
    for s in meres._jsonl(os.path.join(meres.F21P, 'valaszok', 'F3.jsonl')):
        f3.update(s['versek'])
    # az elhagyandó link: az első R1-es aranyvers első többelemű párjának utolsó eleme,
    # amely nincs az `elkerul` kulcsok között ((igehely, 'hianyzo', k, e))
    hianyzo = next((m['igehely'], p[0], p[1][-1]) for m in minta if m['reteg'] == 'R1' and m['igehely'] in v2
                   for p in v2[m['igehely']]['parok']
                   if len(p[1]) >= 2 and (m['igehely'], 'hianyzo', p[0], p[1][-1]) not in set(elkerul))
    kapuhiba_ig = next(m['igehely'] for m in minta if m['igehely'] not in v2 and f3[m['igehely']]['allapot'] == 'ok')
    ki_sorok = []
    uj_naplo = []
    osszcost = 0.0
    for kno, i in enumerate(range(0, len(minta), 10), 1):
        igk = [m['igehely'] for m in minta[i:i + 10]]
        versek = {}
        objok = []
        for ig in igk:
            if ig in v2:
                o = json.loads(json.dumps(v2[ig]))
                if ig == hianyzo[0]:
                    for p in o['parok']:
                        if p[0] == hianyzo[1] and p[1] and p[1][-1] == hianyzo[2] and len(p[1]) >= 2:
                            e = p[1].pop()
                            if not any(e in q[1] for q in o['parok']):
                                o['forditatlan'] = sorted(o['forditatlan'] + [e])
                            break
            else:
                o = f3[ig]['obj'] if f3[ig]['allapot'] == 'ok' else None
            if ig == kapuhiba_ig:
                versek[ig] = {'allapot': 'kapuhiba', 'probalkozas': 2, 'hibak': ['1. a válaszból hiányzik ez a vers'], 'obj': None}
                continue
            if o is None:
                versek[ig] = {'allapot': 'kapuhiba', 'probalkozas': 2, 'hibak': ['1. mock'], 'obj': None}
                continue
            objok.append(o)
            versek[ig] = {'allapot': 'ok', 'probalkozas': 1, 'hibak': [], 'obj': o}
        rossz = [ig for ig in igk if versek[ig]['allapot'] != 'ok']
        nyers = [json.dumps(objok, ensure_ascii=False)]
        hivasok = [{'probalkozas': 1, 'usage': {'completion_tokens_details': {'reasoning_tokens': MOCK_GOND}}}]
        if rossz:
            for ig in rossz:
                versek[ig]['probalkozas'] = 2
            nyers.append('[]')
            hivasok.append({'probalkozas': 2, 'usage': {'completion_tokens_details': {'reasoning_tokens': MOCK_GOND}}})
        for pr in range(1, len(nyers) + 1):
            cost = 0.001 * pr
            osszcost += cost
            sor = dict(zip(fej, ['2026-10-01T00:00:00+00:00', 'F3V2', str(kno), str(pr), 'google/gemini-3.8-flash',
                                 'kotelezo_effort=low', str(len(igk) if pr == 1 else len(rossz)), 'igen', '1000', '500',
                                 str(MOCK_GOND), '%.6f' % cost, 'openrouter', str(len(rossz)), '1', '1.00', 'stop',
                                 'mockprompt02', '0']))
            uj_naplo.append('\t'.join(sor[k] for k in fej))
        ki_sorok.append({'futas': 'F3V2', 'modell': 'google/gemini-3.8-flash', 'koteg': kno, 'igehelyek': igk,
                         'nyers': nyers, 'hivasok': hivasok, 'versek': versek})
    with open(os.path.join(mappa, 'valaszok', 'F3V2.jsonl'), 'w', encoding='utf-8', newline='\n') as fh:
        for s in ki_sorok:
            fh.write(json.dumps(s, ensure_ascii=False) + '\n')
    with open(os.path.join(mappa, 'futasnaplo.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join([naplo[0]] + f3_sorok + uj_naplo) + '\n')
    return {'hianyzo': hianyzo, 'kapuhiba': kapuhiba_ig, 'hivas': len(uj_naplo), 'cost': round(osszcost, 6)}


def onteszt():
    hibak = []
    mappa = tempfile.mkdtemp(prefix='f21p_meres_v2_onteszt_')
    try:
        # hiányzó F3V2: 2-es kód, nem ír
        kod, _ = fut(mappa, os.path.join(mappa, 'x.md'), os.path.join(mappa, 'x.tsv'))
        if kod != 2 or os.path.exists(os.path.join(mappa, 'x.md')):
            hibak.append('hiányzó F3V2 mellett nem 2-es kóddal állt meg, vagy írt')
        info = mock_forras(mappa)
        kod, ki = fut(mappa, os.path.join(mappa, 'v2.md'), os.path.join(mappa, 'v2.tsv'))
        if kod != 0:
            hibak.append('a mock-mérés kilépési kódja %d' % kod)
        else:
            p1 = ki['pont'][('F3 × arany v1', meres.OSSZES)]
            p2 = ki['pont'][('F3 × arany v2', meres.OSSZES)]
            p3 = ki['pont'][('F3V2 × arany v2', meres.OSSZES)]
            if (p1['talalat'], p1['modell'], p1['arany']) != (989, 1061, 1051):
                hibak.append('F3 × arany v1 nem a P4 száma (989/1061, 989/1051): %s' % p1)
            if (p2['talalat'], p2['modell'], p2['arany']) != (990, 1061, 1051):
                hibak.append('F3 × arany v2 nem a C-diff 7. pontjának száma (990/1061, 990/1051): %s' % p2)
            if not (p3['talalat'] == p3['modell'] == p3['arany'] - 1 and p3['versek_ok'] == 60):
                hibak.append('F3V2 mock: a pontosság nem 100%% vagy a lefedettség nem arany−1: %s' % p3)
            k = ki['kapu'][('F3V2', meres.OSSZES)]
            if k['vegleg'] < 1 or k['elso'] < k['vegleg']:
                hibak.append('F3V2 mock: a kapuhiba nem látszik: %s' % k)
            c = ki['koltseg']['F3V2']
            if c['hivas'] != info['hivas'] or abs(c['cost'] - info['cost']) > 1e-9:
                hibak.append('F3V2 mock: a költség/hívásszám eltér: %s vs %s' % (c, info))
            if c['gond_usage'] != MOCK_GOND * info['hivas'] or c['gond_naplo'] != MOCK_GOND * info['hivas']:
                hibak.append('F3V2 mock: a gondolkodási token (usage/napló) eltér: %s' % c)
            if ki['koltseg']['F3']['gond_usage'] is not None:
                hibak.append('F3: a régi futás usage-a nem n.é.')
            r = ki['regi'][('F3', meres.OSSZES)]
            if (r['egyezik'], r['hb'], r['egyezik_k'], r['hb_k']) != (30, 32, 30, 30):
                hibak.append('F3 régi arany nem 30/32 és 30/30: %s' % r)
            with open(os.path.join(mappa, 'v2.md'), encoding='utf-8') as fh:
                md = fh.read()
            if 'megfelelt' in md.replace('„megfelelt”', ''):
                hibak.append('a jelentés „megfelelt” minősítést ad')
            if 'PD6' not in md or 'vs küszöb 95%' not in md:
                hibak.append('a jelentésből hiányzik a PD6-jelölés')
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('meres_v2 önteszt rendben (mock F3V2: 1 elhagyott link, 1 kapuhibás vers; F3 × v1 = P4, F3 × v2 = C-diff 7. pont)')
    return 0


def main():
    if '--onteszt' in sys.argv:
        return onteszt()
    kod, _ = fut()
    return kod


if __name__ == '__main__':
    sys.exit(main())
