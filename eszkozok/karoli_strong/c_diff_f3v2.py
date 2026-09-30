#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.14 — az F3V2 C-diffjének váza: gépi diff az arany v2-höz és a (c) esetek
összevetése az F3 (v1 prompt) (c) hibáival.

Hívás: python eszkozok/karoli_strong/c_diff.py --f3v2 [--sablon] [--szigoru] [--onteszt]
(vagy közvetlenül ez a modul). Nincs API-hívás.

Gépi rész (most kész, a futás előtt):
  * az F3V2 és az F3 eltérései az arany v2-höz (befagyasztott, sha256-ellenőrzés);
    a meres.py linkhalmazaival és kizárásával;
  * az F3 (c) esetei az F3 v2-diffjéből (a v1-besorolás öröklődik: a v2-diff a
    v1-diff részhalmaza, új eltérés nem keletkezett, l. F21P_C_diff.md 7. pont);
  * állapot eltérésenként:
      maradt       — F3 (c) eset, az F3V2-nél is ugyanaz az eltérés;
      megszunt     — F3 (c) eset, az F3V2-nél nincs (a vers az F3V2-nél kapun átment);
      nem_merheto  — F3 (c) eset, de a vers az F3V2-nél kapuhibás;
      uj           — F3V2-eltérés, amely az F3-nál nem volt eltérés;
      oroklott     — F3V2-eltérés, amely az F3-nál (a)/(b) osztályú volt.
Kézi rész (a futás után, Opus): a f21p/c_diff_f3v2_osszevetes.tsv osztály- és
konvencióoszlopai. A --sablon a gépi oszlopokkal megírja a fájlt (a kézi
oszlopok üresek); a --szigoru ellenőrzés (a futás utáni zárás) megköveteli,
hogy minden F3V2-eltérésnek legyen osztálya (a/b/c), és minden megszűnt és új
esetnek legyen változás-konvenciója (K1–K10, vagy „nincs”).

Kimenet: naplok/F21P_C_diff_F3V2.md (generált). F3V2.jsonl nélkül 2-es kód.
"""

import os
import shutil
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_diff  # noqa: E402
import meres  # noqa: E402
import meres_v2  # noqa: E402
import tokenek  # noqa: E402

OSSZEVETES_UT = os.path.join(tokenek.ROOT, 'f21p', 'c_diff_f3v2_osszevetes.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_C_diff_F3V2.md')
OSZLOPOK = ['igehely', 'reteg', 'irany', 'k_poz', 'e_poz', 'statusz', 'f3_osztaly',
            'f3v2_osztaly', 'konvencio_vagy_jegyzetpont', 'valtozas_konvencio', 'indok']
GEPI = OSZLOPOK[:7]
STATUSZOK = ('maradt', 'megszunt', 'nem_merheto', 'uj', 'oroklott')
KONVENCIOK = tuple('K%d' % i for i in range(1, 11)) + ('nincs',)


def elteresek(adat, f, g_fn):
    """{(ig, irany, k, e): reteg} a kapun átment aranyversekre."""
    ki = {}
    for ig in adat.versek:
        if ig not in adat.arany or not adat.ok(f, ig):
            continue
        c, g = adat.linkek(f, ig), g_fn(ig)
        for k, e in g - c:
            ki[(ig, 'hianyzo', k, e)] = adat.reteg[ig]
        for k, e in c - g:
            ki[(ig, 'tobblet', k, e)] = adat.reteg[ig]
    return ki


def gepi_osszevetes(adat, g2, kezi_f3):
    """[(kulcs, reteg, statusz, f3_osztaly)] determinisztikus sorrendben."""
    el3 = elteresek(adat, 'F3', g2)
    el32 = elteresek(adat, 'F3V2', g2)
    sor = []
    for kk, ret in el3.items():
        o = kezi_f3[kk]['osztaly']
        if o != 'c':
            continue
        if not adat.ok('F3V2', kk[0]):
            st = 'nem_merheto'
        elif kk in el32:
            st = 'maradt'
        else:
            st = 'megszunt'
        sor.append((kk, ret, st, o))
    for kk, ret in el32.items():
        if kk in el3:
            o = kezi_f3[kk]['osztaly']
            if o != 'c':
                sor.append((kk, ret, 'oroklott', o))
        else:
            sor.append((kk, ret, 'uj', ''))
    rend = {ig: i for i, ig in enumerate(adat.versek)}
    sor.sort(key=lambda x: (rend[x[0][0]], x[0][1], x[0][2], x[0][3], STATUSZOK.index(x[2])))
    return sor


def f3_besorolas():
    """Az F3 v1-besorolása (f21p/c_diff_besorolas.tsv) kulcs szerint."""
    return {(r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz'])): r
            for r in c_diff._tsv(c_diff.BESOROLAS_UT, c_diff.BES_OSZLOPOK)}


def sablon_ir(gepi, ut):
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(OSZLOPOK) + '\n')
        for (ig, irany, k, e), ret, st, o in gepi:
            fh.write('\t'.join([ig, ret, irany, str(k), str(e), st, o, '', '', '', '']) + '\n')


def ellenoriz(gepi, ut, szigoru=False):
    hibak = []
    if not os.path.exists(ut):
        return ['nincs összevetés-fájl: %s (--sablon írja meg)' % ut] if szigoru else []
    sorok = c_diff._tsv(ut, OSZLOPOK)
    gep = {(kk, st): (ret, o) for kk, ret, st, o in gepi}
    kez = {}
    for r in sorok:
        kk = (r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))
        kulcs = (kk, r['statusz'])
        if kulcs in kez:
            hibak.append('kétszer: %s' % (kulcs,))
        kez[kulcs] = r
        if kulcs in gep and (r['reteg'], r['f3_osztaly']) != gep[kulcs]:
            hibak.append('a gépi oszlopok eltérnek: %s' % (kulcs,))
        if r['f3v2_osztaly'] and r['f3v2_osztaly'] not in c_diff.OSZTALYOK:
            hibak.append('érvénytelen F3V2-osztály: %s' % (kulcs,))
        if r['valtozas_konvencio'] and r['valtozas_konvencio'] not in KONVENCIOK:
            hibak.append('érvénytelen változás-konvenció (K1–K10 vagy nincs): %s' % (kulcs,))
        if szigoru:
            if r['statusz'] in ('maradt', 'uj', 'oroklott') and not r['f3v2_osztaly']:
                hibak.append('F3V2-eltérés osztály nélkül: %s' % (kulcs,))
            if r['statusz'] in ('megszunt', 'uj') and not r['valtozas_konvencio']:
                hibak.append('megszűnt/új eset változás-konvenció nélkül: %s' % (kulcs,))
            if r['f3v2_osztaly'] in ('a', 'b') and not r['konvencio_vagy_jegyzetpont']:
                hibak.append('(a)/(b) konvenció/jegyzetpont nélkül: %s' % (kulcs,))
            if (r['f3v2_osztaly'] or r['valtozas_konvencio']) and not r['indok'].strip():
                hibak.append('üres indok: %s' % (kulcs,))
    for kulcs in sorted(set(gep) - set(kez)):
        hibak.append('gépi eset a fájlban nincs: %s' % (kulcs,))
    for kulcs in sorted(set(kez) - set(gep)):
        hibak.append('a fájl esete gépileg nem létezik: %s' % (kulcs,))
    return hibak


PELDAK = [   # jellemző példák (kulcs, állapot) — kézi válogatás; az új és a megszűnt (c) esetek mind listázódnak
    (('Jer 46:21', 'hianyzo', 2, 3), 'megszunt'),
    (('Ez 46:12', 'tobblet', 25, 27), 'megszunt'),
    (('Mt 11:18', 'tobblet', 4, 5), 'uj'),
    (('Péld 23:19', 'hianyzo', 3, 4), 'maradt'),
    (('2Móz 21:26', 'hianyzo', 8, 13), 'uj'),
    (('2Móz 26:13', 'tobblet', 23, 26), 'uj'),
    (('Péld 25:24', 'tobblet', 4, 4), 'uj'),
    (('Mt 5:34', 'tobblet', 3, 3), 'uj'),
    (('Mt 27:18', 'tobblet', 4, 1), 'uj'),
    (('Zsolt 18:3', 'tobblet', 7, 4), 'uj'),
    (('1Pét 5:12', 'tobblet', 22, 21), 'uj'),
    (('2Móz 21:6', 'hianyzo', 6, 5), 'oroklott'),
    (('Jer 51:3', 'tobblet', 2, 4), 'uj'),
]
HATAS = [('segített (v1 (c) megszűnt)', 'megszunt', None), ('nem segített (v1 (c) maradt)', 'maradt', 'c'),
         ('ártott (új (c))', 'uj', 'c'), ('új (a)', 'uj', 'a'), ('új (b)', 'uj', 'b')]


def _sor(adat, kk, st, r):
    return '| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        kk[0], kk[1], c_diff._magyar(adat, kk[0], kk[2]), c_diff._eredeti(adat, kk[0], kk[3]), st,
        r.get('f3v2_osztaly') or '—', r.get('konvencio_vagy_jegyzetpont') or '—',
        r.get('valtozas_konvencio') or '—', r.get('indok') or '—')


def zaro_szakasz(adat, g, gepi, kezi):
    """A kitöltött (szigorúan ellenőrzött) összevetés összegző szakaszai (F21.16)."""
    ret_lista = meres.RETEGEK + [meres.OSSZES]
    f3b = f3_besorolas()

    def van(ret, r):
        return ret == meres.OSSZES or r == ret

    ki = ['## A (c) hibák: F3 (v1 prompt) és F3V2 (prompt v2), az arany v2-höz', '',
          'A mért értékek (pontosság, lefedettség, küszöb-viszony) a naplok/F21P_meres_v2.md a)–e) pontjában; a küszöb '
          'szempontjából csak azok számítanak. Az alábbi osztályok és a korrigált értékek **az Opus besorolása, nem mérés**.', '',
          '| réteg | F3 (c) | F3V2 (c) | ebből maradt | ebből új | F3 megszűnt (c) | F3V2 (a) | F3V2 (b) |',
          '|---|---|---|---|---|---|---|---|']
    el3 = elteresek(adat, 'F3', g['v2'])
    for ret in ret_lista:
        f3c = sum(1 for kk, r in el3.items() if van(ret, r) and f3b[kk]['osztaly'] == 'c')
        c2 = [(kk, r, st) for kk, r, st, _ in gepi if van(ret, r) and st in ('maradt', 'uj', 'oroklott')]
        n = {o: sum(1 for kk, r, st in c2 if kezi[(kk, st)]['f3v2_osztaly'] == o) for o in ('a', 'b', 'c')}
        mar = sum(1 for kk, r, st in c2 if st == 'maradt')
        uj = sum(1 for kk, r, st in c2 if st == 'uj' and kezi[(kk, st)]['f3v2_osztaly'] == 'c')
        megsz = sum(1 for kk, r, st, _ in gepi if van(ret, r) and st == 'megszunt')
        ki.append('| %s | %d | %d | %d | %d | %d | %d | %d |' % (ret, f3c, n['c'], mar, uj, megsz, n['a'], n['b']))
    ki += ['', '### Korrigált pontosság és lefedettség — az Opus besorolása, nem mérés', '',
           'Az (a) és (b) eltérést nem-hibának véve (F3: a v1-besorolás öröklődik; F3V2: a fenti kézi besorolás). A küszöb '
           'szempontjából csak a mért érték számít.', '',
           '| réteg | mérőszám | F3 × v2 mért | F3 × v2 korrigált (Opus, nem mérés) | F3V2 × v2 mért | F3V2 × v2 korrigált (Opus, nem mérés) |',
           '|---|---|---|---|---|---|']
    el32 = {(kk, st): r for kk, r, st, _ in gepi if st in ('maradt', 'uj', 'oroklott')}
    for ret in ret_lista:
        vals = []
        for f, oszt in (('F3', lambda kk: f3b[kk]['osztaly']), ('F3V2', None)):
            p = meres_v2.pont_lef(adat, f, g['v2'], ret)
            if f == 'F3':
                tab = sum(1 for kk, r in el3.items() if van(ret, r) and kk[1] == 'tobblet' and oszt(kk) in ('a', 'b'))
                hab = sum(1 for kk, r in el3.items() if van(ret, r) and kk[1] == 'hianyzo' and oszt(kk) in ('a', 'b'))
            else:
                tab = sum(1 for (kk, st), r in el32.items() if van(ret, r) and kk[1] == 'tobblet'
                          and kezi[(kk, st)]['f3v2_osztaly'] in ('a', 'b'))
                hab = sum(1 for (kk, st), r in el32.items() if van(ret, r) and kk[1] == 'hianyzo'
                          and kezi[(kk, st)]['f3v2_osztaly'] in ('a', 'b'))
            vals.append((p, tab, hab))
        (p3, t3, h3), (p32, t32, h32) = vals
        ki.append('| %s | pontosság | %s | %s | %s | %s |' % (
            ret, meres_v2._pct(p3['talalat'], p3['modell']), meres_v2._pct(p3['talalat'] + t3, p3['modell']),
            meres_v2._pct(p32['talalat'], p32['modell']), meres_v2._pct(p32['talalat'] + t32, p32['modell'])))
        ki.append('| %s | lefedettség | %s | %s | %s | %s |' % (
            ret, meres_v2._pct(p3['talalat'], p3['arany']), meres_v2._pct(p3['talalat'] + h3, p3['arany']),
            meres_v2._pct(p32['talalat'], p32['arany']), meres_v2._pct(p32['talalat'] + h32, p32['arany'])))
    ki += ['', '## A változás konvenciónként (kézi besorolás)', '',
           'segített = a v1 (c) eset megszűnt, és a megnevezett konvenció (prompt-szabály) magyarázza; nem segített = a v1 (c) '
           'eset maradt, pedig a konvenció rá vonatkozik; ártott = új (c) eset, amelyet a konvenció szabálya váltott ki; '
           'új (a)/(b) = új konvenciókülönbség vagy az arany vitatható döntése. „nincs” = nem konvenció, modell-ingadozás.', '',
           '| konvenció | ' + ' | '.join(h for h, _, _ in HATAS) + ' |', '|---|' + '---|' * len(HATAS)]
    konvok = sorted({r['valtozas_konvencio'] for r in kezi.values() if r['valtozas_konvencio']},
                    key=lambda x: (x == 'nincs', int(x[1:]) if x != 'nincs' else 0))
    for kv in konvok:
        cell = []
        for _, st, o in HATAS:
            cell.append(str(sum(1 for (kk, s), r in kezi.items() if s == st and r['valtozas_konvencio'] == kv
                                and (o is None or r['f3v2_osztaly'] == o))))
        ki.append('| %s | %s |' % (kv, ' | '.join(cell)))
    fej = ['| vers | irány | magyar szó | eredeti szó | állapot | F3V2-osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |',
           '|---|---|---|---|---|---|---|---|---|']
    ki += ['', '## Jellemző példák (kézi válogatás)', ''] + fej
    ki += [_sor(adat, kk, st, kezi[(kk, st)]) for kk, st in PELDAK if (kk, st) in kezi]
    ki += ['', '## Minden új (c) eset', ''] + fej
    ki += [_sor(adat, kk, st, kezi[(kk, st)]) for kk, r, st, _ in gepi if st == 'uj' and kezi[(kk, st)]['f3v2_osztaly'] == 'c']
    ki += ['', '## Minden megszűnt (c) eset (a v1 F3 (c) hibái, amelyek az F3V2-nél nem eltérések)', ''] + fej
    ki += [_sor(adat, kk, st, kezi[(kk, st)]) for kk, r, st, _ in gepi if st == 'megszunt']
    ki += ['', '## Minden maradt (c) eset', ''] + fej
    ki += [_sor(adat, kk, st, kezi[(kk, st)]) for kk, r, st, _ in gepi if st == 'maradt']
    ki.append('')
    return ki


def jelentes(adat, gepi, ut_osszevetes, ut, g=None):
    kezi = {}
    if os.path.exists(ut_osszevetes):
        for r in c_diff._tsv(ut_osszevetes, OSZLOPOK):
            kezi[((r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz'])), r['statusz'])] = r
    ki = ['# F21P_C_diff_F3V2.md — az F3V2 eltérései az arany v2-höz és a (c) esetek összevetése az F3-mal', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/c_diff_f3v2.py (c_diff.py --f3v2) | forras=f21p/valaszok/F3.jsonl, '
          'f21p/valaszok/F3V2.jsonl, f21p/arany_opus_v2.jsonl (befagyasztva), f21p/c_diff_besorolas.tsv, '
          'f21p/c_diff_f3v2_osszevetes.tsv | kézzel szerkeszteni tilos -->', '',
          'A megszűnt/maradt/új/örökölt állapot gépi; az F3V2-osztály és a változást magyarázó konvenció '
          '(K1–K10) **kézi ítélet (Opus), nem mérés**, és a futás után kerül a f21p/c_diff_f3v2_osszevetes.tsv-be.', '',
          '| réteg | ' + ' | '.join(STATUSZOK) + ' |', '|---|' + '---|' * len(STATUSZOK)]
    for ret in meres.RETEGEK + [meres.OSSZES]:
        cell = [sum(1 for kk, r, st, _ in gepi if st == s and (ret == meres.OSSZES or r == ret)) for s in STATUSZOK]
        ki.append('| %s | %s |' % (ret, ' | '.join(map(str, cell))))
    ki.append('')
    if g is not None and kezi and not ellenoriz(gepi, ut_osszevetes, szigoru=True):
        ki += zaro_szakasz(adat, g, gepi, kezi)
    ki += ['## Minden eltérés (gépi állapot, kézi besorolás)', '',
           '| vers | irány | magyar szó | eredeti szó | állapot | F3-osztály | F3V2-osztály (kézi) | '
           'konvenció / jegyzetpont (kézi) | változás-konvenció (kézi) | indok (kézi) |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for kk, ret, st, o in gepi:
        r = kezi.get((kk, st), {})
        ki.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            kk[0], kk[1], c_diff._magyar(adat, kk[0], kk[2]), c_diff._eredeti(adat, kk[0], kk[3]), st, o or '—',
            r.get('f3v2_osztaly') or '—', r.get('konvencio_vagy_jegyzetpont') or '—',
            r.get('valtozas_konvencio') or '—', r.get('indok') or '—'))
    ki.append('')
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(ki) + '\n')


def fut(forras_dir=None, osszevetes=OSSZEVETES_UT, jelentes_ut=JELENTES_UT, sablon=False, szigoru=False):
    try:
        adat, g = meres_v2.betolt(forras_dir)
    except meres_v2.HianyzoFutas as e:
        print('HIBA: %s; az F3V2-diff a futás után indítható' % e, file=sys.stderr)
        return 2, None
    gepi = gepi_osszevetes(adat, g['v2'], f3_besorolas())
    if sablon:
        if os.path.exists(osszevetes):
            print('HIBA: az összevetés-fájl már létezik, a sablon nem írja felül: %s' % osszevetes, file=sys.stderr)
            return 1, gepi
        sablon_ir(gepi, osszevetes)
    hibak = ellenoriz(gepi, osszevetes, szigoru)
    if hibak:
        print('HIBA (a jelentés nem íródott):')
        for h in hibak:
            print('  ' + h)
        return 1, gepi
    jelentes(adat, gepi, osszevetes, jelentes_ut, g)
    print('F3V2-összevetés: %s -> %s' % (', '.join('%s %d' % (s, sum(1 for x in gepi if x[2] == s)) for s in STATUSZOK),
                                         jelentes_ut))
    return 0, gepi


def onteszt():
    hibak = []
    mappa = tempfile.mkdtemp(prefix='f21p_cdiff_f3v2_onteszt_')
    try:
        osz = os.path.join(mappa, 'osszevetes.tsv')
        jel = os.path.join(mappa, 'jelentes.md')
        kod, _ = fut(mappa, osz, jel)
        if kod != 2:
            hibak.append('F3V2 nélkül nem 2-es kód: %d' % kod)
        adat0 = meres.Adat(futasok=['F3'])
        v2 = {o['vers']: o for o in meres._jsonl(tokenek.ARANY_V2)}
        el3 = elteresek(adat0, 'F3', lambda ig: adat0._szur(ig, {(p[0], e) for p in v2[ig]['parok'] for e in p[1]}))
        info = meres_v2.mock_forras(mappa, elkerul=set(el3))
        # a mock F3V2 az arany v2 az aranyverseken, egy elhagyott linkkel: minden F3 (c) megszűnik,
        # egyetlen új eltérés az elhagyott link (hiányzó)
        kod, gepi = fut(mappa, osz, jel, sablon=True)
        st = {s: [x for x in gepi if x[2] == s] for s in STATUSZOK}
        f3c = [kk for kk, r in f3_besorolas().items() if r['osztaly'] == 'c']
        if kod != 0:
            hibak.append('a sablonos futás kódja %d' % kod)
        if len(st['megszunt']) != len(f3c) or st['maradt'] or st['nem_merheto'] or st['oroklott']:
            hibak.append('mock: nem minden F3 (c) szűnt meg (%s)' % {s: len(v) for s, v in st.items()})
        ig, k, e = info['hianyzo']
        if [x[0] for x in st['uj']] != [(ig, 'hianyzo', k, e)]:
            hibak.append('mock: az új eltérés nem az elhagyott link: %s' % st['uj'])
        if not os.path.exists(osz) or not os.path.exists(jel):
            hibak.append('mock: a sablon vagy a jelentés nem íródott')
        kod, _ = fut(mappa, osz, jel, szigoru=True)
        if kod != 1:
            hibak.append('mock: a szigorú ellenőrzés az üres kézi oszlopokkal nem bukott el')
        kod, _ = fut(mappa, osz, jel, sablon=True)
        if kod != 1:
            hibak.append('mock: a sablon felülírta a meglévő összevetés-fájlt')
        # kitöltött kézi oszlopokkal a szigorú ellenőrzés átmegy
        sorok = c_diff._tsv(osz, OSZLOPOK)
        with open(osz, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\t'.join(OSZLOPOK) + '\n')
            for r in sorok:
                if r['statusz'] in ('maradt', 'uj', 'oroklott'):
                    r['f3v2_osztaly'] = 'c'
                if r['statusz'] in ('megszunt', 'uj'):
                    r['valtozas_konvencio'] = 'nincs'
                r['indok'] = 'mock'
                fh.write('\t'.join(r[c] for c in OSZLOPOK) + '\n')
        kod, _ = fut(mappa, osz, jel, szigoru=True)
        if kod != 0:
            hibak.append('mock: a kitöltött összevetés szigorú ellenőrzése nem ment át')
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('c_diff_f3v2 önteszt rendben (mock: minden F3 (c) megszűnt, 1 új eltérés; sablon, szigorú ellenőrzés, felülírás-védelem)')
    return 0


def main():
    if '--onteszt' in sys.argv:
        return onteszt()
    return fut(sablon='--sablon' in sys.argv, szigoru='--szigoru' in sys.argv)[0]


if __name__ == '__main__':
    sys.exit(main())
