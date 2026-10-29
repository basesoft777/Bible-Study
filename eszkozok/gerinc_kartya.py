#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerinc_kartya.py -- F124: gerinc-kartya egy igeszakaszra (a tanulmany A3b
lepese, a vak olvasas UTAN) es a kartya <-> kulcsszo-tablazat osszevetes.

A kartya megmutatja, mely meglevo motivumok gerinc-elemei fordulnak elo a
szakaszban (TAHOT + TAGNT, a grammatikai Strongok kiszurve), mi van ezek
kozul mar az adatretegben, es soronkent megnevezi, melyik gerinc-elemen
log. A `jelolt.py` fuggvenyeire epit (annak sorhalmazat tartalmazza), de
azt nem modositja; ujdonsagok: kollokacio-jelzes (osszetett gerinc-elem
minden tagja egy versben), allapot-bovites (tartomany-igehelyek, a jelolt
dontese), a #110 szuro (gerinc_szuro.py) es a `szuretlen_tag` jeloles a
tag gerinc-Strongokon, valamint a lekerdezesenkenti proveniencia-sor, 0
talalatnal is (CLAUDE.md 1. szabaly).

A kartya CSAK JELOLTET ad: nem ir tablat. `--ir` csak az `uj` allapotu,
nem kiszurt, nem `szuretlen_tag` sorokat irja a jeloltek.tsv vegere
`dontes=nyitva`-val (CLAUDE.md 2. szabaly; DT184: a szuretlen tag bevetel
elvetve); `beepitve`/`elutasitva` erteket SOHA.

`--osszevet <tanulmany-utvonal>`: a kartya (igehely, Strong) parjait a
kulcsszavak.tsv ugyanazon tanulmanyhoz tartozo soraival veti ossze.
Mindket lista kiirodik, ures eredmenynel is explicit "üres" jelolessel.

CLI:
    python eszkozok/gerinc_kartya.py --szakasz "1Móz 17:1-27" [--osszevet genezis/X.md]
                                      [--md FILE] [--ir] [--adat DIR]

Kilepesi kod: 0 = lefutott, 2 = hiba.
"""

import argparse
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G
import lekerdez as L
import gerinc_szuro as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')

FORRAS = 'TAHOT_kivonat.tsv+TAGNT_kivonat.tsv'

# A #108 altal tagnak mert gerinc-Strongok (naplok/F108_MOTIVUM_UJRASCAN_naplo.md,
# F108_ujrascan_elteresek.tsv): H3548, H7451, H2403, H0127, H1121+H0430,
# H7121+H8034, H7843, H7043, H5315+H2416, H2555 -- az osszetetteknel a tagok.
TAG_STRONGOK = {'H3548', 'H7451', 'H2403', 'H0127', 'H1121', 'H0430', 'H7121', 'H8034',
                'H7843', 'H7043', 'H5315', 'H2416', 'H2555'}

STRONG_RE = re.compile(r'^[HG]\d+[A-Za-z]*(\+[HG]\d+[A-Za-z]*)*$')

DONTES_RANG = {'beépítve': 0, 'nyitva': 1, 'elutasítva': 2}

JELOLTEK_FEJLEC = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas',
                   'karoli_szo', 'azonositas_modja', 'megbizhatosag', 'datum']


# ---------------------------------------------------------------------------
# Bemenet
# ---------------------------------------------------------------------------

def versek_betolt():
    """{(konyv, fej, vers): {'tahot': [tok], 'tagnt': [tok]}} -- tok = {'strong', 'gloss'}."""
    versek = {}
    for nev, sorok in (('tahot', L.load_tahot()), ('tagnt', L.load_tagnt())):
        for r in sorok:
            v = versek.setdefault(r['_parsed'], {'tahot': [], 'tagnt': []})
            v[nev].append({'strong': r['Strong-szám'], 'gloss': r.get('Angol tükörfordítás', '')})
    return versek


def konyv_index():
    """{magyar_rovidites: sorszam} a Konyv_normalizalo_tabla sorrendjeben."""
    step2hu, _ = L.book_tables()
    return {hu: i for i, hu in enumerate(step2hu.values())}


def igehely_str(kulcs):
    return '%s %d:%d' % kulcs


def kulcs_rendezo(kulcs, kidx):
    return (kidx.get(kulcs[0], 999), kulcs[1], kulcs[2])


def konyvenkent(versek):
    """{konyv: [kulcs, ...]}"""
    by_book = {}
    for k in versek:
        by_book.setdefault(k[0], []).append(k)
    return by_book


def igehely_kulcsok(igehely, by_book):
    """Az igehely (vers, tartomany, fejezet) versei az adott versindexben; ha az
    igehely nem elemezheto, ures halmaz."""
    try:
        rng = L.scope_range(igehely)
    except ValueError:
        return set()
    return {k for k in by_book.get(rng[1], ()) if L.in_range(rng, *k)}


# ---------------------------------------------------------------------------
# Gerinc-tabla, allapot
# ---------------------------------------------------------------------------

def gerinc_tabla(elofordulasok):
    """{tag: {id: {'elemek': {strong-ertek}, 'cimkek': {gerinc_elem}}}} -- az
    osszetett `strong` ertekek ('+') tagjaira bontva (mint a jelolt.py)."""
    tabla = {}
    for sor in elofordulasok:
        strong = (sor.get('strong') or '').strip()
        if not strong:
            continue
        gerinc = (sor.get('gerinc_elem') or '').strip()
        cimke = gerinc if STRONG_RE.match(gerinc) else strong
        for tag in strong.split('+'):
            tag = tag.strip()
            if not tag:
                continue
            e = tabla.setdefault(tag, {}).setdefault(sor['id'], {'elemek': set(), 'cimkek': set()})
            e['elemek'].add(strong)
            e['cimkek'].add(cimke)
    return tabla


class Allapot:
    """Egy (id, igehely) allapota: mar elofordulas / mar jelolt: <dontes> / uj.
    A tartomany-igehelyeket (pl. `1Móz 14:18-20`) verseikre bontja."""

    def __init__(self, elofordulasok, jeloltek, by_book):
        self.elof_pontos = {(s['id'], s['igehely']) for s in elofordulasok}
        self.elof_vers = {}
        for s in elofordulasok:
            self.elof_vers.setdefault(s['id'], set()).update(igehely_kulcsok(s['igehely'], by_book))
        self.jelolt_pontos = {}
        self.jelolt_vers = {}
        for j in G.elofordulas_jeloltek(jeloltek):
            d = j.get('dontes', '')
            self._bejegyez(self.jelolt_pontos, (j['id'], j['igehely']), d)
            for k in igehely_kulcsok(j['igehely'], by_book):
                self._bejegyez(self.jelolt_vers, (j['id'], k), d)

    @staticmethod
    def _bejegyez(szotar, kulcs, dontes):
        regi = szotar.get(kulcs)
        if regi is None or DONTES_RANG.get(dontes, 9) < DONTES_RANG.get(regi, 9):
            szotar[kulcs] = dontes

    def allapot(self, motivum_id, igehely, kulcs):
        if (motivum_id, igehely) in self.elof_pontos or kulcs in self.elof_vers.get(motivum_id, ()):
            return 'már előfordulás'
        d = self.jelolt_pontos.get((motivum_id, igehely)) or self.jelolt_vers.get((motivum_id, kulcs))
        if d:
            return 'már jelölt: %s' % d
        return 'új'


# ---------------------------------------------------------------------------
# Mag: soronkenti kartya
# ---------------------------------------------------------------------------

def kartya_sorok(versek, gramm, motivumok, elofordulasok, jeloltek, kulcsok=None):
    """[sor-dict] a megadott versekre (kulcsok=None: minden vers). Sor mezoi:
    id, igehely, kulcs, strong (tag), gerinc_elem, kollokacio ('' | 'kollokáció' |
    'egy_tag'), allapot, szures ('' | 'atjutott' | 'kiszurve' | 'szuretlen_tag'),
    szures_ok, szures_indoklas, pozicionalis."""
    by_book = konyvenkent(versek)
    kidx = konyv_index()
    tabla = gerinc_tabla(elofordulasok)
    allapot = Allapot(elofordulasok, jeloltek, by_book)
    formulaikus = {m['id'] for m in motivumok if m.get('azonossag_tipusa') == 'formulaikus'}
    if kulcsok is None:
        kulcsok = versek.keys()
    sorok = []
    for kulcs in sorted(kulcsok, key=lambda k: kulcs_rendezo(k, kidx)):
        v = versek.get(kulcs)
        if v is None:
            continue
        strongok = {t['strong'] for t in v['tahot']} | {t['strong'] for t in v['tagnt']}
        igehely = igehely_str(kulcs)
        for tag in sorted(t for t in strongok if t in tabla and t not in gramm):
            for mid in sorted(tabla[tag]):
                e = tabla[tag][mid]
                if any('+' not in x for x in e['elemek']):
                    kolloc = ''
                else:
                    kolloc = 'kollokáció' if any(
                        all(t in strongok for t in x.split('+')) for x in e['elemek']) else 'egy_tag'
                sz = S.szur(mid, tag, v['tahot'], v['tagnt'])
                if sz:
                    szures = 'kiszurve' if sz[0] == 'K' else 'atjutott'
                    szures_ok, szures_ind = sz[1], sz[2]
                elif tag in TAG_STRONGOK:
                    szures, szures_ok, szures_ind = 'szuretlen_tag', '', ''
                else:
                    szures, szures_ok, szures_ind = '', '', ''
                sorok.append({
                    'id': mid, 'igehely': igehely, 'kulcs': kulcs, 'strong': tag,
                    'gerinc_elem': ' | '.join(sorted(e['cimkek'])),
                    'kollokacio': kolloc,
                    'allapot': allapot.allapot(mid, igehely, kulcs),
                    'szures': szures, 'szures_ok': szures_ok, 'szures_indoklas': szures_ind,
                    'pozicionalis': mid in formulaikus,
                })
    sorok.sort(key=lambda s: (s['id'], kulcs_rendezo(s['kulcs'], kidx), s['strong']))
    return sorok


def jelolt_parok(sorok):
    """A jelolt.py-val osszevetheto halmaz: {(id, igehely, strong)}."""
    return {(s['id'], s['igehely'], s['strong']) for s in sorok}


# ---------------------------------------------------------------------------
# Proveniencia
# ---------------------------------------------------------------------------

def proveniencia(szakasz, versek, gramm, elofordulasok, sorok, ts):
    """[proveniencia-sor] -- a szakasz-lekerdezes, minden kollokacio-lekerdezes
    (osszetett gerinc-elem, amelynek valamelyik tagja a szakaszban all) es a
    szuro futasa tagonkent; 0 talalatnal is."""
    rng = L.scope_range(szakasz)
    kulcsok = [k for k in versek if L.in_range(rng, *k)]
    sor_n = len({(s['id'], s['igehely'], s['strong']) for s in sorok})
    ki = ['scope=range:%s | forras=%s | strong=gerinc-halmaz | n=%d | ts=%s' % (szakasz, FORRAS, sor_n, ts)]
    tabla = gerinc_tabla(elofordulasok)
    strongok_szakasz = set()
    for k in kulcsok:
        strongok_szakasz |= {t['strong'] for t in versek[k]['tahot']} | {t['strong'] for t in versek[k]['tagnt']}
    osszetett = sorted({x for ids in tabla.values() for e in ids.values() for x in e['elemek'] if '+' in x})
    for x in osszetett:
        tagok = x.split('+')
        if not any(t in strongok_szakasz for t in tagok):
            continue
        n = sum(1 for k in kulcsok
                if all(t in ({q['strong'] for q in versek[k]['tahot']} | {q['strong'] for q in versek[k]['tagnt']})
                       for t in tagok))
        ki.append('scope=range:%s | forras=%s | strong=%s | n=%d | ts=%s' % (szakasz, FORRAS, x, n, ts))
    for (mid, tag), tipus in sorted(S.SZURT_TAGOK.items()):
        n = len({s['kulcs'] for s in sorok if s['id'] == mid and s['strong'] == tag})
        ki.append('scope=range:%s | forras=%s | strong=%s | szuro=DT283(%s, %s) | n=%d | ts=%s' % (
            szakasz, FORRAS, tag, mid, tipus, n, ts))
    return ki


# ---------------------------------------------------------------------------
# Osszevetes: kartya <-> kulcsszo-tablazat
# ---------------------------------------------------------------------------

def tanulmany_norm(ut):
    ut = ut.strip().replace('\\', '/')
    while ut.startswith('./'):
        ut = ut[2:]
    return ut


def osszevet(sorok, kulcsszavak, tanulmany, by_book):
    """{'van_kulcsszo': bool, 'kartya_nem_olvasas': [sor], 'olvasas_nem_kartya': [kulcsszo-sor]}.
    Ha a kulcsszavak.tsv-ben nincs sor a tanulmanyhoz, az osszevetes nem
    vegezheto el (van_kulcsszo=False): a listak nem toltendok ki (CLAUDE.md 3. szabaly)."""
    tn = tanulmany_norm(tanulmany)
    ks = [k for k in kulcsszavak if tanulmany_norm(k['tanulmany']) == tn]
    if not ks:
        return {'van_kulcsszo': False, 'kartya_nem_olvasas': [], 'olvasas_nem_kartya': []}
    kartya = [s for s in sorok if s['szures'] != 'kiszurve']
    kartya_parok = {(s['kulcs'], s['strong']) for s in kartya}
    olvasas_parok = set()
    ks_ertelmezve = []
    for k in ks:
        vk = igehely_kulcsok(k['igehely'], by_book)
        tagok = {t.strip() for t in k['strong'].split('+') if t.strip()}
        ks_ertelmezve.append((k, vk, tagok))
        for v in vk:
            for t in tagok:
                olvasas_parok.add((v, t))
    a = [s for s in kartya if (s['kulcs'], s['strong']) not in olvasas_parok]
    b = [k for k, vk, tagok in ks_ertelmezve
         if not any((v, t) in kartya_parok for v in vk for t in tagok)]
    return {'van_kulcsszo': True, 'kartya_nem_olvasas': a, 'olvasas_nem_kartya': b}


# ---------------------------------------------------------------------------
# Kimenet
# ---------------------------------------------------------------------------

def _megjegyzes(s):
    m = []
    if s['pozicionalis']:
        m.append('pozicionális ellenőrzés kell')
    if s['szures'] == 'szuretlen_tag':
        m.append('szuretlen_tag')
    if s['szures'] == 'atjutott':
        m.append('szűrő: %s — kézi olvasás' % s['szures_ok'])
    return '; '.join(m)


def jelentes_szoveg(szakasz, sorok, prov, ts, osszev=None, tanulmany=None):
    fo = [s for s in sorok if s['szures'] != 'kiszurve']
    ki_sz = [s for s in sorok if s['szures'] == 'kiszurve']
    ki = ['# GENERÁLT: gerinc_kartya.py --szakasz "%s" | scope=range:%s | forras=%s | ts=%s' % (
        szakasz, szakasz, FORRAS, ts),
        '', '# Gerinc-kártya — %s' % szakasz, '',
        'A kártya csak jelölt; minden sor a `jeloltek.tsv`-n át, döntéssel kerülhet be (CLAUDE.md 2. szabály).', '',
        '| Motívum-ID | Igehely | Strong | Gerinc-elem | Kollokáció | Állapot | Megjegyzés |',
        '|---|---|---|---|---|---|---|']
    for s in fo:
        ki.append('| %s | %s | %s | %s | %s | %s | %s |' % (
            s['id'], s['igehely'], s['strong'], s['gerinc_elem'], s['kollokacio'] or '—',
            s['allapot'], _megjegyzes(s)))
    if not fo:
        ki.append('| *(üres: a szakaszban nincs meglévő motívum gerinc-eleme)* | | | | | | |')
    ki += ['', '## Összesítő', '']
    ki.append('- Sorok a fő táblában: %d (ebből új: %d, már előfordulás: %d, már jelölt: %d)' % (
        len(fo), sum(1 for s in fo if s['allapot'] == 'új'),
        sum(1 for s in fo if s['allapot'] == 'már előfordulás'),
        sum(1 for s in fo if s['allapot'].startswith('már jelölt'))))
    ki.append('- Kiszűrt sor a mellékletben: %d' % len(ki_sz))
    szt = [s for s in fo if s['szures'] == 'szuretlen_tag']
    ki.append('- `szuretlen_tag` sor (tág gerinc-Strong, nincs gépi szűrő): %d (ebből új: %d)' % (
        len(szt), sum(1 for s in szt if s['allapot'] == 'új')))
    if szt:
        per = {}
        for s in szt:
            per[s['id']] = per.get(s['id'], 0) + 1
        ki.append('  - motívumonként: ' + ', '.join('%s %d' % (k, v) for k, v in sorted(per.items())))
    ki += ['', '## Melléklet: a #110 szűrője által kiszűrt sorok', '']
    if ki_sz:
        ki += ['| Motívum-ID | Igehely | Strong | Szűrő-ok | Indoklás |', '|---|---|---|---|---|']
        for s in ki_sz:
            ki.append('| %s | %s | %s | kiszurve: %s | %s |' % (
                s['id'], s['igehely'], s['strong'], s['szures_ok'], s['szures_indoklas']))
    else:
        ki.append('*(üres: a szűrő nem zárt ki sort ebben a szakaszban)*')
    if osszev is not None:
        ki += ['', '## Összevetés: kártya ↔ kulcsszó-táblázat (`%s`)' % tanulmany, '']
        if not osszev['van_kulcsszo']:
            ki.append('*Az összevetés nem végezhető el: a `kulcsszavak.tsv`-ben nincs sor ehhez a tanulmányhoz '
                      '(az A3 `betolt.py kulcsszo` lépés még nem futott). A két lista nem tölthető ki.*')
        else:
            ki += ['### Kártya talált, olvasás nem (elmulasztott ismert motívum-előfordulás gyanúja)', '']
            a = osszev['kartya_nem_olvasas']
            if a:
                ki += ['| Motívum-ID | Igehely | Strong | Állapot |', '|---|---|---|---|']
                ki += ['| %s | %s | %s | %s |' % (s['id'], s['igehely'], s['strong'], s['allapot']) for s in a]
            else:
                ki.append('*(üres: a kártya minden sora szerepel a kulcsszó-táblázatban)*')
            ki += ['', '### Olvasás talált, kártya nem (új motívum gyanúja → A4 ⛔)', '']
            b = osszev['olvasas_nem_kartya']
            if b:
                ki += ['| Igehely | Szó | Strong |', '|---|---|---|']
                ki += ['| %s | %s | %s |' % (k['igehely'], k['szo'], k['strong']) for k in b]
            else:
                ki.append('*(üres: minden kulcsszó egy meglévő gerinc-elemen áll)*')
    ki += ['', '## Proveniencia', '']
    ki += ['- `%s`' % p for p in prov]
    return '\n'.join(ki) + '\n'


# ---------------------------------------------------------------------------
# --ir
# ---------------------------------------------------------------------------

def ir_sorok(sorok):
    """A jeloltek.tsv-be irhato sorok: allapot=uj, nem kiszurt, nem szuretlen_tag;
    (id, igehely) szerint egyedi."""
    lattuk = set()
    ki = []
    for s in sorok:
        if s['allapot'] != 'új' or s['szures'] in ('kiszurve', 'szuretlen_tag'):
            continue
        k = (s['id'], s['igehely'])
        if k in lattuk:
            continue
        lattuk.add(k)
        ki.append(s)
    return ki


def jeloltek_ir(adat_dir, szakasz, sorok, forras_prov, ma=None):
    """Az `uj` sorok a jeloltek.tsv vegere, dontes=nyitva. Irás elott sorosszevetes:
    a tabla minden meglevo sora split/join korutra azonos kell legyen; eltereskor
    megall (ValueError). Visszaadja az irt (id, igehely) parokat."""
    path = os.path.join(adat_dir, 'jeloltek.tsv')
    fejlec, meglevo = G.tsv_beolvas(path)
    domin, _, _ = G.sorveg_elemez(path)
    with open(path, 'rb') as f:
        nyers = f.read()
    szoveg = nyers.decode('utf-8')
    adat_sorok = [s for s in szoveg.split(domin) if s.strip() and not s.startswith('#')][1:]
    ujra = ['\t'.join(r[m] for m in fejlec) for r in meglevo]
    if adat_sorok != ujra:
        raise ValueError('a jeloltek.tsv sorosszevetese eltert az eredetitol -- az iras megall')
    jelolt_kulcs = {(j['id'], j['igehely']) for j in G.elofordulas_jeloltek(meglevo)}
    ma = ma or datetime.date.today().isoformat()
    uj = []
    irt = []
    for s in ir_sorok(sorok):
        if (s['id'], s['igehely']) in jelolt_kulcs:
            continue
        indok = 'automatikus jelölt (gerinc-kártya, A3b), minősítendő'
        if s['kollokacio']:
            indok += '; %s' % s['kollokacio']
        if s['szures'] == 'atjutott':
            indok += '; szűrő: %s' % s['szures_ok']
        mezok = {
            'id': s['id'], 'igehely': s['igehely'],
            'forras_kereses': 'gerinc_kartya.py %s | %s' % (szakasz, forras_prov),
            'dontes': 'nyitva', 'indoklas': indok, 'karoli_szo': '', 'azonositas_modja': '',
            'megbizhatosag': '', 'datum': ma, 'jelolt_tipus': 'elofordulas',
            'cel_id': '', 'cel_igehely': '', 'cel_alpont': '',
        }
        uj.append('\t'.join(mezok.get(m, '') for m in fejlec))
        irt.append((s['id'], s['igehely']))
    if not uj:
        return []
    db = domin.encode('utf-8')
    with open(path, 'ab') as f:
        if not nyers.endswith(b'\n'):
            f.write(db)
        f.write(db.join(u.encode('utf-8') for u in uj))
        f.write(db)
    return irt


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def futtat(szakasz, adat_dir, versek=None, ts=None, tanulmany=None):
    ts = ts or L.ts()
    versek = versek if versek is not None else versek_betolt()
    gramm = L.load_grammatikai_strongok()
    _, motivumok = G.tsv_beolvas(os.path.join(adat_dir, 'motivumok.tsv'))
    _, elofordulasok = G.tsv_beolvas(os.path.join(adat_dir, 'elofordulasok.tsv'))
    _, jeloltek = G.tsv_beolvas(os.path.join(adat_dir, 'jeloltek.tsv'))
    rng = L.scope_range(szakasz)
    kulcsok = [k for k in versek if L.in_range(rng, *k)]
    sorok = kartya_sorok(versek, gramm, motivumok, elofordulasok, jeloltek, kulcsok)
    prov = proveniencia(szakasz, versek, gramm, elofordulasok, sorok, ts)
    osszev = None
    if tanulmany:
        kpath = os.path.join(adat_dir, 'kulcsszavak.tsv')
        _, kulcsszavak = G.tsv_beolvas(kpath)
        osszev = osszevet(sorok, kulcsszavak, tanulmany, konyvenkent(versek))
    szoveg = jelentes_szoveg(szakasz, sorok, prov, ts, osszev, tanulmany)
    return sorok, prov, szoveg


def main():
    ap = argparse.ArgumentParser(description='F124 -- gerinc-kártya egy igeszakaszra')
    ap.add_argument('--szakasz', required=True, help='igeszakasz, pl. "1Móz 17:1-27"')
    ap.add_argument('--osszevet', default=None, help='a tanulmány útvonala (kulcsszavak.tsv összevetés)')
    ap.add_argument('--adat', default=ALAPERTELMEZETT_ADAT, help='az adat/ könyvtár')
    ap.add_argument('--md', default=None, help='a kártya Markdown fájlba is')
    ap.add_argument('--ir', action='store_true',
                    help='az "új" sorok írása a jeloltek.tsv végére (nyitva); kiszűrt és szűretlen tág sor nem')
    args = ap.parse_args()
    try:
        sorok, prov, szoveg = futtat(args.szakasz, args.adat, tanulmany=args.osszevet)
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
    print(szoveg)
    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('  megírva: %s' % args.md, file=sys.stderr)
    if args.ir:
        try:
            irt = jeloltek_ir(args.adat, args.szakasz, sorok, prov[0])
        except Exception as exc:
            print('HIBA: %s' % exc, file=sys.stderr)
            sys.exit(2)
        print('  --ir: %d új jeloltek.tsv sor íródott.' % len(irt), file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
