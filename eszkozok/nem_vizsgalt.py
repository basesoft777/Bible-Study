#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nem_vizsgalt.py -- F63 (JELOLTEK_RETRO): a "meg nem vizsgalt" lista generatora
es a retroaktiv jelolt-sorok egyszeri hozzafuzese.

A "meg nem vizsgalt" lista SZARMAZTATOTT, nem tarolt adat (nem a `dontes`
erteke): a motivum scan-lekerdezeseinek talalatai MINUS a `jeloltek.tsv`
(es az `elofordulasok.tsv`) igehelyei. A lekerdezeseket a `lekerdez.py`
futtatja ujra (cmd_scan / cmd_kollokacio, a sajat proveniencia-soraval).

A scan-halmaz FUTASKOR vezetodik le az `adat/elofordulasok.tsv` `strong`
oszlopabol (osszetett ertek elemeire bontva, a nyelvtani Strongok --
`adat/grammatikai_strongok.tsv` -- nelkul). Kezzel csak a tablabol nem
kiolvashato tobblet van megadva (KOLLOKACIO, EXTRA), megjegyzessel es
napló-hivatkozassal (DT-F63a (2)). Az `auditok.tsv`-ba nem iras tortenik.

Strong-szintu csoportos kizaras (DT-F63a (3)): a HAMART-001 naploja (4/c)
egyes Strongok minden maradek elofordulasat csoportosan elutasitja, igehelyek
nelkul. Ezek kulon kategoriaban jelennek meg, nem "meg nem vizsgalt", nem
`elutasitva`.

Alparancsok:
    python eszkozok/nem_vizsgalt.py lista [--id ID ...] [--munkalapokkal] [--md FILE]
    python eszkozok/nem_vizsgalt.py hozzafuz [--id ID ...] [--ir]

`hozzafuz`: a `naplok/JELOLTEK_RETRO_<ID>_sorok.tsv` munkalapok sorait fuzi a
`adat/jeloltek.tsv` vegere. Alapbol szaraz futas; `--ir` nelkul nem ir.
Csak hozzafuz, meglevo sor bajtra azonos marad; elteresnel megall. I/O:
split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md).
"""

import argparse
import contextlib
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lekerdez as L  # noqa: E402

ROOT = os.path.dirname(HERE)
ADAT = os.path.join(ROOT, 'adat')
NAPLOK = os.path.join(ROOT, 'naplok')

MOTIVUMOK = ['ALVIL-001', 'ANTROP-001', 'HAMART-001', 'HODIT-001',
             'ISTENTISZT-001', 'KIRALY-001', 'MENNY-001', 'TEREMT-001']

JELOLTEK_FEJLEC = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas',
                   'karoli_szo', 'azonositas_modja', 'megbizhatosag', 'datum']
DONTES_ERTEKEK = {'beépítve', 'elutasítva', 'nyitva'}

# --- kezi tobblet: csak ami az elofordulasok.strong-bol nem olvashato ki ---
NAPLO_DIR = 'tematikus_lezart/naplok/'
KOLLOKACIO = {  # (A, B, megjegyzes)
    'ISTENTISZT-001': [('H7121', 'H8034',
                        'formulaikus azonossag: H7121+H8034 egy versben; ' + NAPLO_DIR +
                        'Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md, Vizsgalt kulcsszavak')],
    'MENNY-001': [('H1121', 'H0430',
                   'בְּנֵי (הָ)אֱלֹהִים szorendi minta: H1121+H0430 egy versben; ' + NAPLO_DIR +
                   'Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md')],
}
EXTRA = {  # (Strong, megjegyzes)
    'HAMART-001': [('H2403', 'gerinc-elem (chattat); ' + NAPLO_DIR +
                    'Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md, 2. Vizsgalt kulcsszavak')],
}
# a kollokacio tagjait nem szkenneljuk kulon (zajos); a kollokacio fedi
KOLLOKACIO_TAGOK = {'ISTENTISZT-001': {'H7121', 'H8034'}, 'MENNY-001': {'H1121', 'H0430'}}
# Strong-szintu csoportos kizaras (napló 4/c): ezek maradek talalatai kulon kategoria
CSOPORTOS_KIZARAS = {
    'HAMART-001': ({'H2555', 'H7843', 'H0127', 'H2403', 'G2672', 'G2671', 'G5351',
                    'G5356', 'G1311'},
                   'Strong-szintű csoportos kizárás, napló 4/c (' + NAPLO_DIR +
                   'Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md)'),
}

# ---------------------------------------------------------------------------


def olvas(path):
    with open(path, encoding='utf-8', newline='') as f:
        szoveg = f.read()
    return [l.rstrip('\r') for l in szoveg.split('\n')]


def tabla(path):
    """(fejlec, sorok-listak); '#' kezdetu sorok kimaradnak."""
    sorok = [l for l in olvas(path) if l and not l.startswith('#')]
    return sorok[0].split('\t'), [l.split('\t') for l in sorok[1:]]


_IG = re.compile(r'^(.+?) (\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$')


def kibont(igehely):
    """'Zsid 7:1-28' -> {'Zsid 7:1', ..., 'Zsid 7:28'}; egyszeru vers -> {vers}."""
    m = _IG.match(igehely.strip())
    if not m:
        return {igehely.strip()}
    konyv, ch, v1, ch2, v2 = m.groups()
    if v2 is None:
        return {'%s %s:%s' % (konyv, ch, v1)}
    if ch2 and ch2 != ch:
        return {'%s %s:%s' % (konyv, ch, v1), '%s %s:%s' % (konyv, ch2, v2)}
    a, z = int(v1), int(v2)
    if z < a or z - a > 200:
        return {igehely.strip()}
    return {'%s %s:%d' % (konyv, ch, x) for x in range(a, z + 1)}


def vizsgalt_versek(mid, munkalapokkal=False):
    """A motivum mar kezelt versei: jeloltek + elofordulasok (+ opcionalisan a munkalap)."""
    vers = set()
    _, jel = tabla(os.path.join(ADAT, 'jeloltek.tsv'))
    for r in jel:
        if r[0] == mid:
            vers |= kibont(r[1])
    _, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    for r in elo:
        if r[0] == mid:
            vers |= kibont(r[1])
    if munkalapokkal:
        p = os.path.join(NAPLOK, 'JELOLTEK_RETRO_%s_sorok.tsv' % mid)
        if os.path.exists(p):
            _, sorok = tabla(p)
            for r in sorok:
                vers |= kibont(r[1])
    return vers


def scan_halmaz(mid):
    """Futaskor levezetett halmaz: (egyes Strongok, kollokaciok, extra-megjegyzesek)."""
    fej, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    i_id, i_strong = fej.index('id'), fej.index('strong')
    gramm = L.load_grammatikai_strongok()
    tagok = KOLLOKACIO_TAGOK.get(mid, set())
    strongok = {}
    for r in elo:
        if r[i_id] != mid or not r[i_strong].strip():
            continue
        for s in r[i_strong].split('+'):
            s = s.strip()
            if not s or s in gramm or s in tagok:
                continue
            strongok.setdefault(s, 'elofordulasok.strong')
    for s, megj in EXTRA.get(mid, []):
        if s not in gramm:
            strongok.setdefault(s, 'kézi: ' + megj)
    csop = CSOPORTOS_KIZARAS.get(mid)
    if csop:
        for s in csop[0]:
            strongok.setdefault(s, 'kézi: csoportos kizárás (napló 4/c)')
    return strongok, KOLLOKACIO.get(mid, [])


def futtat(fn, **kw):
    """A lekerdez.py parancs kimenetenek elkapasa: (versek, proveniencia-sor)."""
    puf = io.StringIO()
    with contextlib.redirect_stdout(puf):
        fn(argparse.Namespace(**kw))
    versek, prov = [], ''
    for l in puf.getvalue().split('\n'):
        if l.startswith('proveniencia:'):
            prov = l[len('proveniencia:'):].strip()
        elif l and not l.startswith('#'):
            versek.append(l.strip())
    return versek, prov


def elemez(mid, munkalapokkal=False):
    """Visszaad: {'nem_vizsgalt': {forras: [versek]}, 'csoportos': {strong: [versek]}, 'lekerdezesek': [..]}."""
    kezelt = vizsgalt_versek(mid, munkalapokkal)
    strongok, kollok = scan_halmaz(mid)
    csop_set, csop_felirat = CSOPORTOS_KIZARAS.get(mid, (set(), ''))
    nv, csop, lek = {}, {}, []
    for s in sorted(strongok):
        versek, prov = futtat(L.cmd_scan, strong=s, szakasz=None)
        lek.append((s, strongok[s], len(versek), prov))
        hi = sorted({v for v in versek if v not in kezelt})
        (csop if s in csop_set else nv)[s] = hi
    for a, b, megj in kollok:
        versek, prov = futtat(L.cmd_kollokacio, strong_a=a, strong_b=b)
        lek.append((a + '+' + b, 'kézi: ' + megj, len(versek), prov))
        nv[a + '+' + b] = sorted({v for v in versek if v not in kezelt})
    # a "nem vizsgalt" dominal: csoportos-kategoriabol kikerul, ami mashol is nem vizsgalt
    mas = set()
    for k, v in nv.items():
        mas |= set(v)
    csop = {s: [v for v in vs if v not in mas] for s, vs in csop.items()}
    return {'nem_vizsgalt': nv, 'csoportos': csop, 'csoportos_felirat': csop_felirat,
            'lekerdezesek': lek, 'kezelt': len(kezelt)}


def jelentes(mid, e):
    sor = ['## %s' % mid, '',
           'Már kezelt vers (jeloltek + elofordulasok): %d.' % e['kezelt'], '',
           '### Lekérdezések (a `lekerdez.py` kimenete)', '',
           '| scan | honnan | n | proveniencia |', '|---|---|---|---|']
    for s, honnan, n, prov in e['lekerdezesek']:
        sor.append('| %s | %s | %d | `%s` |' % (s, honnan, n, prov))
    ossz = set()
    for vs in e['nem_vizsgalt'].values():
        ossz |= set(vs)
    sor += ['', '### Még nem vizsgált (egyedi vers: %d)' % len(ossz), '']
    for s, vs in e['nem_vizsgalt'].items():
        sor.append('- %s: %d vers' % (s, len(vs)))
    if e['csoportos']:
        sor += ['', '### %s' % e['csoportos_felirat'], '']
        for s, vs in e['csoportos'].items():
            sor.append('- %s: %d vers (se „még nem vizsgált”, se `elutasítva`)' % (s, len(vs)))
    sor.append('')
    return '\n'.join(sor), len(ossz)


def cmd_lista(args):
    azonositok = args.id or MOTIVUMOK
    reszek = []
    for mid in azonositok:
        e = elemez(mid, args.munkalapokkal)
        szoveg, n = jelentes(mid, e)
        print('%s: még nem vizsgált egyedi vers: %d; csoportos kizárás: %d' %
              (mid, n, sum(len(v) for v in e['csoportos'].values())))
        reszek.append(szoveg)
    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='') as f:
            f.write('# Még nem vizsgált lista (származtatott; eszkozok/nem_vizsgalt.py)\n\n' +
                    '\n'.join(reszek))
    return 0


# ---------------------------------------------------------------------------
# hozzafuzes
# ---------------------------------------------------------------------------

def munkalap_sorok(mid):
    p = os.path.join(NAPLOK, 'JELOLTEK_RETRO_%s_sorok.tsv' % mid)
    if not os.path.exists(p):
        return []
    sorok = [l for l in olvas(p) if l]
    if sorok[0].split('\t') != JELOLTEK_FEJLEC:
        raise SystemExit('Hibás fejléc: ' + p)
    ki = []
    for l in sorok[1:]:
        mezok = l.split('\t')
        if len(mezok) != len(JELOLTEK_FEJLEC):
            raise SystemExit('Hibás mezőszám (%d) a %s fájlban: %s' % (len(mezok), p, l[:80]))
        if mezok[0] != mid:
            raise SystemExit('Idegen id a %s fájlban: %s' % (p, mezok[0]))
        if mezok[3] not in DONTES_ERTEKEK:
            raise SystemExit('Érvénytelen dontes: %s (%s)' % (mezok[3], mezok[1]))
        if not mezok[2] or not mezok[4] or not mezok[8]:
            raise SystemExit('Üres kötelező mező: %s %s' % (mezok[0], mezok[1]))
        ki.append(mezok)
    return ki


def cmd_hozzafuz(args):
    path = os.path.join(ADAT, 'jeloltek.tsv')
    with open(path, 'rb') as f:
        regi = f.read()
    crlf = b'\r\n' in regi
    nl = b'\r\n' if crlf else b'\n'
    szoveg = regi.decode('utf-8')
    fej, jel = tabla(path)
    if fej != JELOLTEK_FEJLEC:
        raise SystemExit('A jeloltek.tsv fejléce eltér a várttól.')
    letezo = {(r[0], r[1]) for r in jel}
    uj, ismetlodo = [], []
    for mid in (args.id or MOTIVUMOK):
        for mezok in munkalap_sorok(mid):
            kulcs = (mezok[0], mezok[1])
            if kulcs in letezo:
                ismetlodo.append(kulcs)
            else:
                letezo.add(kulcs)
                uj.append(mezok)
    if ismetlodo:
        raise SystemExit('Már létező kulcs (megállás): %s' % ismetlodo[:5])
    if not regi.endswith(b'\n'):
        raise SystemExit('A jeloltek.tsv nem újsorral végződik; megállás.')
    uj_bajt = b''.join(('\t'.join(m)).encode('utf-8') + nl for m in uj)
    ossz = regi + uj_bajt
    # --- ellenorzes: a regi bajtok valtozatlanok, a sorszam-novekmeny pontos ---
    assert ossz[:len(regi)] == regi
    uj_sorszam = len([l for l in ossz.decode('utf-8').split('\n') if l])
    regi_sorszam = len([l for l in szoveg.split('\n') if l])
    assert uj_sorszam - regi_sorszam == len(uj), 'sorszám-növekmény eltér'
    for mid in (args.id or MOTIVUMOK):
        n = sum(1 for m in uj if m[0] == mid)
        print('%s: +%d sor' % (mid, n))
    print('Összesen: +%d sor (a jeloltek.tsv: %d -> %d nem üres sor)' %
          (len(uj), regi_sorszam, uj_sorszam))
    if not args.ir:
        print('Száraz futás (--ir nélkül nem írok).')
        return 0
    with open(path, 'wb') as f:
        f.write(ossz)
    with open(path, 'rb') as f:
        ellen = f.read()
    assert ellen[:len(regi)] == regi and len(ellen) == len(ossz)
    print('Megírva.')
    return 0

# ---------------------------------------------------------------------------
# lelet-lap adata (ADATVAGYON_TERV 5., 12-es lap): lexikai kor - TSK-kor
# ---------------------------------------------------------------------------

def jeloltek_versenkent(mid):
    """vers -> [(dontes, indoklas, igehely-sor)] a jeloltek.tsv-bol."""
    _, jel = tabla(os.path.join(ADAT, 'jeloltek.tsv'))
    ki = {}
    for r in jel:
        if r[0] == mid:
            for v in kibont(r[1]):
                ki.setdefault(v, []).append((r[3], r[4], r[1]))
    return ki


def lexikai_kor(mid):
    """A motivum lexikai kore: az elofordulasok.strong osszetett ertekeinek kollokacioja
    (egy versben), az egyes ertekek scanje; lekerdez.py kimenet + proveniencia."""
    _, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    fej = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))[0]
    i_id, i_s = fej.index('id'), fej.index('strong')
    gramm = L.load_grammatikai_strongok()
    ertekek = []
    for r in elo:
        if r[i_id] == mid and r[i_s].strip() and r[i_s] not in ertekek:
            ertekek.append(r[i_s])
    kor, prov = {}, []
    for e in ertekek:
        resz = [x for x in e.split('+') if x and x not in gramm]
        if len(resz) == 2:
            versek, pr = futtat(L.cmd_kollokacio, strong_a=resz[0], strong_b=resz[1])
            nev = '+'.join(resz)
        elif len(resz) == 1:
            versek, pr = futtat(L.cmd_scan, strong=resz[0], szakasz=None)
            nev = resz[0]
        else:
            continue
        prov.append((nev, pr))
        for v in versek:
            kor.setdefault(v, []).append(nev)
    return kor, prov


def tsk_kor(mid):
    """A motivum ismert versein kiindulo TSK-szomszedsag (minden Votes-ertek)."""
    ismert = vizsgalt_versek(mid)
    kiindulo = set()
    for v in ismert:
        kiindulo.add(v)
    cel = {}
    for r in L.load_tsk():
        if r['Igehely'] in kiindulo:
            for v in kibont(r['Kapcsolódó igehely']):
                cel.setdefault(v, []).append(int(r['Votes']))
    prov = ('scope=TSK-teljes | forras=TSK_kereszthivatkozasok.tsv | kiindulo_vers=%d | n=%d | ts=%s' %
            (len(kiindulo), len(cel), L.ts()))
    return cel, prov


def cmd_lelet(args):
    mid = args.id
    kor, lex_prov = lexikai_kor(mid)
    tsk, tsk_prov = tsk_kor(mid)
    jel = jeloltek_versenkent(mid)
    csillag = sorted(v for v in kor if v not in tsk)
    sor = ['# Lelet-lap adata -- %s' % mid, '',
           '*Származtatott (eszkozok/nem_vizsgalt.py lelet); a ★ = a lexikai kör (%d vers) mínusz a TSK-kör (%d vers); '
           'ezek a projekt saját lexikai leletei, amelyeket a TSK nem jelez.*' % (len(kor), len(tsk)), '',
           '## Lekérdezések', '']
    for nev, pr in lex_prov:
        sor.append('- lexikai kör `%s`: `%s`' % (nev, pr))
    sor += ['- TSK-kör: `%s`' % tsk_prov, '',
            '## ★ sorok (%d)' % len(csillag), '',
            '| ★ vers | gerinc-elem | dontes | indoklas (jeloltek.tsv) |', '|---|---|---|---|']
    nincs = 0
    for v in csillag:
        gerinc = ', '.join(sorted(set(kor[v])))
        if v in jel:
            d = ' / '.join(sorted({x[0] for x in jel[v]}))
            i = ' / '.join(x[1] for x in jel[v])
        else:
            d, i = 'még nem vizsgált', '(nincs jeloltek-sor)'
            nincs += 1
        sor.append('| %s | %s | %s | %s |' % (v, gerinc, d, i.replace('|', '/')))
    kozos = sorted(v for v in kor if v in tsk)
    sor += ['', '## A lexikai kör TSK-val is jelzett része (%d vers; nem ★)' % len(kozos), '']
    for v in kozos:
        sor.append('- %s (TSK Votes max %d)' % (v, max(tsk[v])))
    sor += ['', '## Összesítés', '',
            '- ★ sor: %d, ebből jeloltek-sorral (dontes + indoklas): %d; „még nem vizsgált”: %d; jelöletlen: 0' %
            (len(csillag), len(csillag) - nincs, nincs), '']
    szoveg = '\n'.join(sor)
    print(szoveg.split('## Összesítés')[-1].strip())
    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    sub = ap.add_subparsers(dest='parancs', required=True)
    sp = sub.add_parser('lista')
    sp.add_argument('--id', nargs='+')
    sp.add_argument('--munkalapokkal', action='store_true',
                    help='a munkalapok sorait is kezeltnek veszi (pótlás utáni állapot)')
    sp.add_argument('--md')
    sp.set_defaults(func=cmd_lista)
    sp = sub.add_parser('hozzafuz')
    sp.add_argument('--id', nargs='+')
    sp.add_argument('--ir', action='store_true')
    sp.set_defaults(func=cmd_hozzafuz)
    sp = sub.add_parser('lelet')
    sp.add_argument('--id', default='ANTROP-001')
    sp.add_argument('--md')
    sp.set_defaults(func=cmd_lelet)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
