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
kiolvashato tobblet van megadva (CSOPORTOS_KIZARAS; a KOLLOKACIO csak megjegyzes), megjegyzessel es
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

# --- kezi kiegeszitesek (DT-F63a (2) szerint a kodba irva, megjegyzessel es naplo-hivatkozassal) ---
NAPLO_DIR = 'tematikus_lezart/naplok/'
# Napló-hivatkozas a kollokaciokhoz. FIGYELEM: a ket kollokacio (H7121+H8034, H1121+H0430) az
# `elofordulasok.strong` osszetett ertekekent KIOLVASHATO, a scan_halmaz maga is levezeti; ez a
# bejegyzes csak a megjegyzest (naplo-hivatkozas) adja a levezetett helyett. (A korabbi H2403
# EXTRA-bejegyzes torolve: az `elofordulasok.tsv` HAMART-001 1Moz 4:7 sora hordozza.)
KOLLOKACIO = {  # (A, B, megjegyzes)
    'ISTENTISZT-001': [('H7121', 'H8034',
                        'formulaikus azonossag: H7121+H8034 egy versben; ' + NAPLO_DIR +
                        'Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md, Vizsgalt kulcsszavak')],
    'MENNY-001': [('H1121', 'H0430',
                   'בְּנֵי (הָ)אֱלֹהִים szorendi minta: H1121+H0430 egy versben; ' + NAPLO_DIR +
                   'Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md')],
}
EXTRA = {}  # (Strong, megjegyzes): jelenleg nincs olyan Strong, amely az elofordulasok-bol ne lenne kiolvashato
# Strong-szintu csoportos kizaras: a HAMART-001 naplo 4/c tablajanak csoport-sorai (igehelyek
# nelkul). KEZI, a naploból: a G2672, G2671, G5351, G5356, G1311, G0093 NINCS az
# `elofordulasok.strong`-ban, a H2555, H7843, H0127, H2403 igen. Maradek talalataik kulon kategoria.
CSOPORTOS_KIZARAS = {
    'HAMART-001': ({'H2555', 'H7843', 'H0127', 'H2403', 'G2672', 'G2671', 'G5351',
                    'G5356', 'G1311', 'G0093'},
                   'Strong-szintű csoportos kizárás, napló 4/c (' + NAPLO_DIR +
                   'Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md)'),
}

# ---------------------------------------------------------------------------


# --- a zajos korok kategorizalasa (DT-F63c): EGY logika a `lista`-nak es a lelet-merésnek ---
# Az `elofordulasok.gerinc_elem` a zajos Strongokat is gerinc-elemkent tartja nyilvan,
# ezert a szukites tartalmi dontes; itt kategoria, nem torles. A kategoria-bejegyzes
# kezi, a DT-F63c (A)/(B)/(C) szerint.
# FORRAS: DONTESEK.md DT-F63c (felhasznaloi dontes, 2026-10-11); DT-F63a (2) szerint a kodba
# irt kezi kiegeszites. (A) pontatlan: az N-F63d-re var; (B)/(C) szukitendo: az N-F63e-re var
# (a gerinc tartalmi felulvizsgalata). A kategoria NEM torles es NEM "megvizsgalt": a
# szukitendo/pontatlan versek vizsgalata nyitott, ezert egy motivum 0 "meg nem vizsgalt"
# erteke nem teljesseget jelent.
KOR_KATEGORIA = {
    # (A) formula a gerinc, de a versszintu lekerdezes pontatlan
    'ISTENTISZT-001': {'H7121+H8034': 'pontatlan'},
    'MENNY-001': {'H1121+H0430': 'pontatlan'},
    # (B) gyakori Strong onalloan; az azonossagot a kollokacio hordozza
    'KIRALY-001': {'H3548': 'szukitendo'},
    # (C) gyakori Strong, amely az adatban gerinc; a gerinc tartalmi felulvizsgalata kulon tetel
    'HAMART-001': {'H7451': 'szukitendo', 'H7043': 'szukitendo', 'H6975': 'szukitendo'},
}
KATEGORIA_FELIRAT = {
    'csoportos': 'Strong-szintű csoportos kizárás (napló 4/c)',
    'pontatlan': 'versszintű kollokáció, pontatlan',
    'szukitendo': 'tematikus horgony / szűkítendő',
}
KATEGORIA_SORREND = ['csoportos', 'pontatlan', 'szukitendo']


def kor_kategoria(mid, nev):
    """'normal' | 'csoportos' | 'pontatlan' | 'szukitendo' egy kor-nevre."""
    k = KOR_KATEGORIA.get(mid, {}).get(nev)
    if k:
        return k
    if nev in CSOPORTOS_KIZARAS.get(mid, (set(), ''))[0]:
        return 'csoportos'
    return 'normal'


def horgony_ertekek(mid):
    """Az `elofordulasok.strong` azon ertekei, amelyeknek MINDEN sora a sajat `kapcsolodas`
    mezojeben 'NEM lexikai'-nak minositi magat (DT-F63b: tematikus horgony)."""
    fej, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    i_id, i_s, i_k = fej.index('id'), fej.index('strong'), fej.index('kapcsolodas')
    sorok = {}
    for r in elo:
        if r[i_id] == mid and r[i_s].strip():
            sorok.setdefault(r[i_s], []).append(r)
    return {e for e, rs in sorok.items() if all('NEM lexikai' in r[i_k] for r in rs)}


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
    """Futaskor levezetett halmaz: (egyes Strongok, kollokaciok [(A, B, honnan)]).
    Az `elofordulasok.strong` osszetett erteke (2 nem nyelvtani elem) KOLLOKACIO (egy versben),
    az egyszeru ertek scan; a tematikus horgony ertekei kimaradnak (DT-F63b)."""
    fej, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    i_id, i_strong = fej.index('id'), fej.index('strong')
    gramm = L.load_grammatikai_strongok()
    horg = horgony_ertekek(mid)
    strongok, kollok = {}, []
    for r in elo:
        if r[i_id] != mid or not r[i_strong].strip() or r[i_strong] in horg:
            continue
        resz = [x.strip() for x in r[i_strong].split('+') if x.strip() and x.strip() not in gramm]
        if len(resz) == 1:
            strongok.setdefault(resz[0], 'elofordulasok.strong')
        elif len(resz) == 2 and not any(k[0] == resz[0] and k[1] == resz[1] for k in kollok):
            kollok.append((resz[0], resz[1], 'elofordulasok.strong'))
    for a, b, megj in KOLLOKACIO.get(mid, []):  # kezi megjegyzes a levezetett helyett
        kollok = [(x, y, m) for x, y, m in kollok if (x, y) != (a, b)] + [(a, b, megj)]
    for s, megj in EXTRA.get(mid, []):
        if s not in gramm:
            strongok.setdefault(s, 'kézi: ' + megj)
    csop = CSOPORTOS_KIZARAS.get(mid)
    if csop:
        for s in csop[0]:
            strongok.setdefault(s, 'kézi: csoportos kizárás (napló 4/c)')
    return strongok, kollok


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
    """Visszaad: {'nem_vizsgalt': {kor: [versek]}, 'kategoriak': {kategoria: {kor: [versek]}},
    'csoportos': ..., 'lekerdezesek': [..]}. Egy logika (kor_kategoria) a lelet-merésssel."""
    kezelt = vizsgalt_versek(mid, munkalapokkal)
    strongok, kollok = scan_halmaz(mid)
    nv, kat, lek = {}, {k: {} for k in KATEGORIA_SORREND}, []

    def tarol(nev, hi):
        k = kor_kategoria(mid, nev)
        (nv if k == 'normal' else kat[k])[nev] = hi

    for s in sorted(strongok):
        versek, prov = futtat(L.cmd_scan, strong=s, szakasz=None)
        lek.append((s, strongok[s], len(versek), prov))
        tarol(s, sorted({v for v in versek if v not in kezelt}))
    for a, b, megj in kollok:
        versek, prov = futtat(L.cmd_kollokacio, strong_a=a, strong_b=b)
        nev = a + '+' + b
        lek.append((nev, megj, len(versek), prov))
        tarol(nev, sorted({v for v in versek if v not in kezelt}))
    # a "nem vizsgalt" dominal: a kategoriakbol kikerul, ami normal korben is nem vizsgalt
    mas = set()
    for v in nv.values():
        mas |= set(v)
    kat = {k: {n: [v for v in vs if v not in mas] for n, vs in d.items()} for k, d in kat.items()}
    horg = horgony_kor(mid)
    for nev, (versek, pr, _) in horg.items():
        lek.append((nev, 'tematikus horgony (a sor saját minősítése: NEM lexikai)', len(versek), pr))
    return {'nem_vizsgalt': nv, 'kategoriak': kat, 'csoportos': kat['csoportos'],
            'horgony': {n: len(v[0]) for n, v in horg.items()},
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
    for k in KATEGORIA_SORREND:
        if e['kategoriak'][k]:
            sor += ['', '### %s' % KATEGORIA_FELIRAT[k], '']
            for s, vs in e['kategoriak'][k].items():
                sor.append('- %s: %d vers (se „még nem vizsgált”, se `elutasítva`)' % (s, len(vs)))
    if e['horgony']:
        sor += ['', '### Tematikus horgony, nem lexikai kör (DT-F63b)', '']
        for n, db in e['horgony'].items():
            sor.append('- %s: %d vers (se „még nem vizsgált”, se `elutasítva`; a sor saját minősítése: NEM lexikai)' % (n, db))
    sor.append('')
    return '\n'.join(sor), len(ossz)


def cmd_lista(args):
    azonositok = args.id or MOTIVUMOK
    reszek = []
    for mid in azonositok:
        e = elemez(mid, args.munkalapokkal)
        szoveg, n = jelentes(mid, e)
        kat = ', '.join('%s: %d' % (k, sum(len(v) for v in e['kategoriak'][k].values()))
                        for k in KATEGORIA_SORREND if e['kategoriak'][k])
        if e['horgony']:
            kat = (kat + '; ' if kat else '') + 'tematikus horgony: %d' % sum(e['horgony'].values())
        print('%s: még nem vizsgált egyedi vers: %d%s' % (mid, n, ('; ' + kat) if kat else ''))
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


def horgony_kor(mid):
    """Tematikus horgony (DT-F63b) korei: {nev: (versek, proveniencia, [(igehely, kapcsolodas)])};
    a lekerdez.py kimenete, nevesitett kategoria (se csillag, se "meg nem vizsgalt")."""
    fej, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    i_id, i_s, i_k = fej.index('id'), fej.index('strong'), fej.index('kapcsolodas')
    gramm = L.load_grammatikai_strongok()
    ki = {}
    for e in sorted(horgony_ertekek(mid)):
        resz = [x for x in e.split('+') if x and x not in gramm]
        if len(resz) == 2:
            versek, pr = futtat(L.cmd_kollokacio, strong_a=resz[0], strong_b=resz[1])
        elif len(resz) == 1:
            versek, pr = futtat(L.cmd_scan, strong=resz[0], szakasz=None)
        else:
            continue
        ki['+'.join(resz)] = (versek, pr, [(r[1], r[i_k]) for r in elo if r[i_id] == mid and r[i_s] == e])
    return ki


def lexikai_kor(mid):
    """A motivum lexikai kore: a scan_halmaz egy logikaja (a `lista` is ezt hasznalja),
    lekerdez.py kimenet + proveniencia. Tematikus horgony (DT-F63b): az az osszetett
    ertek, amelynek MINDEN elofordulasok-sora a sajat `kapcsolodas` mezojeben "NEM lexikai"-nak
    minositi magat; versei nevesitett kategoriaba kerulnek (nem lexikai kor, nem csillag).
    Visszaad: (kor, prov, horgony); horgony = {nev: (versek, [(igehely, kapcsolodas)])}."""
    fej, elo = tabla(os.path.join(ADAT, 'elofordulasok.tsv'))
    i_id, i_s, i_k = fej.index('id'), fej.index('strong'), fej.index('kapcsolodas')
    gramm = L.load_grammatikai_strongok()
    strongok, kollok = scan_halmaz(mid)
    kor, prov, horgony = {}, [], {}
    for s in sorted(strongok):
        versek, pr = futtat(L.cmd_scan, strong=s, szakasz=None)
        prov.append((s, pr))
        for v in versek:
            kor.setdefault(v, []).append(s)
    for a, b, _ in kollok:
        versek, pr = futtat(L.cmd_kollokacio, strong_a=a, strong_b=b)
        nev = a + '+' + b
        prov.append((nev, pr))
        for v in versek:
            kor.setdefault(v, []).append(nev)
    for nev, (versek, pr, forrasok) in horgony_kor(mid).items():
        prov.append((nev, pr))
        horgony[nev] = (versek, forrasok)
    return kor, prov, horgony


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


def lelet_adat(mid):
    """A lelet-lap adata egy motivumra (ADATVAGYON_TERV 5., 12-es lap).
    csillag = normal lexikai kor - TSK-kor; a nem normal korok (csoportos kizaras,
    pontatlan kollokacio, szukitendo) versei kulon kategoria (kor_kategoria)."""
    kor, lex_prov, horgony = lexikai_kor(mid)
    tsk, tsk_prov = tsk_kor(mid)
    jel = jeloltek_versenkent(mid)
    csillag = []
    kat = {k: [] for k in KATEGORIA_SORREND}
    for v in sorted(v for v in kor if v not in tsk):
        ks = {kor_kategoria(mid, n) for n in kor[v]}
        if 'normal' in ks:
            csillag.append(v)
        else:
            kat[[k for k in KATEGORIA_SORREND if k in ks][0]].append(v)
    sorok = []
    for v in csillag:
        gerinc = ', '.join(sorted(n for n in set(kor[v]) if kor_kategoria(mid, n) == 'normal'))
        if v in jel:
            d = ' / '.join(sorted({x[0] for x in jel[v]}))
            i = ' / '.join(x[1] for x in jel[v])
        else:
            d, i = 'még nem vizsgált', '(nincs jeloltek-sor)'
        sorok.append((v, gerinc, d, i))
    hv = set()
    for versek, _ in horgony.values():
        hv |= set(versek)
    return {'kor': kor, 'tsk': tsk, 'lex_prov': lex_prov, 'tsk_prov': tsk_prov,
            'sorok': sorok, 'kategoriak': kat, 'csoportos': kat['csoportos'], 'horgony': horgony,
            'horgony_versek': sorted(hv), 'kozos': sorted(v for v in kor if v in tsk)}


def zajos(a):
    """Zajos a motivum, ha van nem normal kategoriaju (csoportos/pontatlan/szukitendo) vers."""
    return any(a['kategoriak'][k] for k in KATEGORIA_SORREND)


def osszesit(a):
    """(csillag, nyitva, elutasitva, beepitve, meg nem vizsgalt, csoportos, pontatlan kollokacio,
    szukitendo, tematikus horgony-vers, TSK-val jelzett)"""
    sorok = a['sorok']
    nyitva = sum(1 for s in sorok if s[2] == 'nyitva')
    elut = sum(1 for s in sorok if s[2] == 'elutasítva')
    beep = sum(1 for s in sorok if s[2] == 'beépítve')
    nincs = sum(1 for s in sorok if s[2] == 'még nem vizsgált')
    k = a['kategoriak']
    return (len(sorok), nyitva, elut, beep, nincs, len(k['csoportos']), len(k['pontatlan']),
            len(k['szukitendo']), len(a['horgony_versek']), len(a['kozos']))


def lelet_md(mid, a):
    sor = ['# Lelet-lap adata -- %s' % mid, '',
           '*Származtatott (eszkozok/nem_vizsgalt.py lelet); a ★ = a lexikai kör (%d vers) mínusz a TSK-kör (%d vers); '
           'ezek a projekt saját lexikai leletei, amelyeket a TSK nem jelez.*' % (len(a['kor']), len(a['tsk'])), '',
           '## Lekérdezések', '']
    for nev, pr in a['lex_prov']:
        sor.append('- kör `%s`: `%s`' % (nev, pr))
    sor += ['- TSK-kör: `%s`' % a['tsk_prov'], '',
            '## ★ sorok (%d)' % len(a['sorok']), '',
            '| ★ vers | gerinc-elem | dontes | indoklas (jeloltek.tsv) |', '|---|---|---|---|']
    for v, g, d, i in a['sorok']:
        sor.append('| %s | %s | %s | %s |' % (v, g, d, i.replace('|', '/')))
    sor += ['', '## A lexikai kör TSK-val is jelzett része (%d vers; nem ★)' % len(a['kozos']), '']
    for v in a['kozos']:
        sor.append('- %s (TSK Votes max %d)' % (v, max(a['tsk'][v])))
    for k in KATEGORIA_SORREND:
        if a['kategoriak'][k]:
            sor += ['', '## %s: %d vers (nem ★, nem „még nem vizsgált”)' % (KATEGORIA_FELIRAT[k], len(a['kategoriak'][k]))]
    for nev, (versek, forrasok) in a['horgony'].items():
        sor += ['', '## Tematikus horgony, nem lexikai kör: `%s` (%d vers; se ★, se „még nem vizsgált”)' % (nev, len(versek)), '']
        for ig, kap in forrasok:
            sor.append('- a `%s` sor saját minősítése (`elofordulasok.kapcsolodas`): „%s”' % (ig, kap))
    o = osszesit(a)
    sor += ['', '## Összesítés', '',
            '- ★ sor: %d; ebből `nyitva` %d, `elutasítva` %d, `beépítve` %d, „még nem vizsgált” %d; jelöletlen: 0' %
            (o[0], o[1], o[2], o[3], o[4]),
            '- csoportos kizárás: %d vers; versszintű kollokáció, pontatlan: %d vers; szűkítendő: %d vers; '
            'tematikus horgony: %d vers; TSK-val is jelzett: %d vers' % o[5:], '']
    return '\n'.join(sor)


def cmd_lelet(args):
    a = lelet_adat(args.id)
    szoveg = lelet_md(args.id, a)
    print(szoveg.split('## Összesítés')[-1].strip())
    if args.md:
        if zajos(a):
            print('Zajos motívum (DT-F63c (2)): olvasói lelet-lap nem készül, csak mérés (meres).')
            return 0
        with open(args.md, 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)
    return 0


def cmd_meres(args):
    """Csak meres: minden motivumra az osszesito tabla; adatot nem ir."""
    sor = ['| motívum | ★ | ebből nyitva | elutasítva | beépítve | még nem vizsgált | csoportos kizárás | '
           'versszintű kollokáció, pontatlan | szűkítendő | tematikus horgony | TSK-val jelzett | lelet-lap |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|']
    reszek = []
    for mid in (args.id or MOTIVUMOK):
        a = lelet_adat(mid)
        o = osszesit(a)
        sor.append('| %s | %s | %s |' % (mid, ' | '.join(str(x) for x in o),
                                          'nem készül (zajos)' if zajos(a) else 'készíthető'))
        reszek.append((mid, a))
    print('\n'.join(sor))
    if args.md:
        ki = ['# Lelet-mérés (csak mérés, adatírás nélkül; eszkozok/nem_vizsgalt.py meres)', '',
              'Kör = az `elofordulasok.strong` értékeinek kollokációja/scanje (lekerdez.py); ★ = normál lexikai kör − TSK-kör '
              '(a motívum ismert verseinek TSK-szomszédsága). Kategóriák: DT-F63c (A) pontatlan kollokáció, (B)/(C) szűkítendő, '
              'csoportos kizárás (napló 4/c), DT-F63b tematikus horgony. A kategorizálás kézi (`KOR_KATEGORIA`), a szűkítés tartalmi döntés.', '',
              '**FIGYELEM: a tábla nem teljességi jelentés.** A „még nem vizsgált” oszlop 0 értéke NEM jelenti, '
              'hogy a motívum végig van vizsgálva: HAMART-001-nél azért 0, mert 501 vers ideiglenesen „szűkítendő” '
              'lett, amíg az N-F63e el nem dől (és 537 vers csoportos kizárás); MENNY-001-nél 0 mellett 269 '
              '„pontatlan” vers áll (az N-F63d-re vár); ISTENTISZT-001 és KIRALY-001 is hasonló.', '',
              'Oszlopok: ★ = normál lexikai kör − TSK-kör; „csoportos kizárás” = napló 4/c Strong-szintű kizárása; '
              '„versszintű kollokáció, pontatlan” = a formula a gerinc, de az egy-versű lekérdezés pontatlan (DT-F63c (A)); '
              '„szűkítendő” = gyakori Strong, tartalmi felülvizsgálatra vár (DT-F63c (B)/(C)); „tematikus horgony” = a sor '
              'saját minősítése szerint NEM lexikai (DT-F63b). A kategóriák versei se ★, se „még nem vizsgált”, se '
              '`elutasítva`: a vizsgálatuk nyitott.', '',
              '\n'.join(sor), '', '## Körök mérete és proveniencia', '']
        for mid, a in reszek:
            ki.append('### %s' % mid)
            ki.append('')
            for nev, pr in a['lex_prov']:
                k = kor_kategoria(mid, nev)
                cimke = 'tematikus horgony, nem lexikai kör' if nev in a['horgony'] else KATEGORIA_FELIRAT.get(k, 'normál')
                ki.append('- `%s` [%s]: `%s`' % (nev, cimke, pr))
            ki.append('- TSK: `%s`' % a['tsk_prov'])
            for nev, (versek, forrasok) in a['horgony'].items():
                ki.append('- tematikus horgony `%s`: %d vers (a sor saját minősítése: NEM lexikai)' % (nev, len(versek)))
            ki.append('')
        with open(args.md, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(ki))
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
    sp = sub.add_parser('meres')
    sp.add_argument('--id', nargs='+')
    sp.add_argument('--md')
    sp.set_defaults(func=cmd_meres)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
