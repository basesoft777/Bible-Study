#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
heti_attekinto.py -- a heti áttekintő oldal generátora.

A brief-fejlécekből (az `eszkozok/feladatok.py` beolvasó függvényeivel, csak olvasva) és a
GitHub PR-állapotokból (`gh pr list`) sávonként csoportosított, önálló HTML-oldalt készít a
felhasználónak: fent „A te teendőid”, utána öt sáv (fejlesztői infrastruktúra, tartalomkészítés,
olvasó, felhasználók, üzleti oldal), mindegyikben három blokk: folyamatban / vár / kész a héten.

A sávot a brief `sav` fejlécmezője adja (SYSTEMS / CONTENT / SERVER / USER / BUSINESS). Ha a mező hiányzik
vagy ismeretlen értékű, a brief a „besorolatlan” csoportba kerül; a szkript ettől függetlenül működik.

A kimenet generált nézet: a `--kimenet` a repón kívülre mutasson (CLAUDE.md: a kimeneti próbák a
repón kívülre mennek), a szkript a repón belüli útvonalat elutasítja.

Használat:
    python eszkozok/heti_attekinto.py --kimenet <út.html>
        [--gyoker <repó>] [--ma ÉÉÉÉ-HH-NN] [--nap 7] [--pr-json <fájl>]

`--pr-json`: a `gh` helyett a fájlból olvassa a PR-listát (egy JSON-tömb: number, title, state,
isDraft, mergedAt, headRefName, url); teszthez és kapcsolat nélküli futtatáshoz.

Kilépési kód: 0 = rendben, 2 = hiba.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402

REPO = F.REPO

# ---------------------------------------------------------------------------
# Címkék: az olvasói szöveg egyetlen helye (belső kulcs nem kerül az oldalra)
# ---------------------------------------------------------------------------

SAVOK = (
    ('SYSTEMS', 'Fejlesztői infrastruktúra'),
    ('CONTENT', 'Tartalomkészítés'),
    ('SERVER', 'Olvasó'),
    ('USER', 'Felhasználók, előfizetés, jogok'),
    ('BUSINESS', 'Üzleti oldal'),
)
BESOROLATLAN = 'BESOROLATLAN'
BESOROLATLAN_CIMKE = 'Besorolatlan'
SAV_CIMKE = dict(SAVOK)
SAV_CIMKE[BESOROLATLAN] = BESOROLATLAN_CIMKE

ALLAPOT_CIMKE = {
    'nem_indult': 'nem indult',
    'brief_kell': 'feladatleírás kell',
    'fut': 'folyamatban',
    'dontesre_var': 'döntésre vár',
    'megallt': 'megállt',
    'lezarva': 'lezárva',
    'pr': 'átnézésre vár (nincs egyesítve)',
    'felbemaradt': 'félbemaradt, folytatható',
    'halasztva': 'halasztva',
}
# a három blokk (oszlop) a sávokon belül
FUT, VAR, KESZ = 'fut', 'var', 'kesz'
BLOKK_CIM = {FUT: 'Folyamatban', VAR: 'Vár', KESZ: 'Kész a héten'}
BLOKK_URES = {FUT: 'Nincs folyamatban lévő munka.', VAR: 'Nincs várakozó feladat.',
              KESZ: 'Ezen a héten nem zárult le semmi.'}
TEENDO_MAX = 230     # a „te teendőid” sor szövegének legfeljebb ennyi karaktere látszik
CIM_MAX = 120

PR_TITLE_ELOTAG = re.compile(r'^\s*\[[^\]]*\]\s*')            # „[ELLENŐRZŐ] ” a PR-címek elején
PR_SZAM_A_CIMBEN = re.compile(r'\bF(\d+)')
PR_SZAM_AZ_AGBAN = re.compile(r'(?:^|/)f(\d+)(?:[-_.]|$)')
SAV_SOR = re.compile(r'^sav:\s*([A-Za-z_]+)\s*$')
VAR_ELOTAG = re.compile(r'^\s*Te\s*(?:\(⛔\))?\s*:\s*')


# ---------------------------------------------------------------------------
# bemenet
# ---------------------------------------------------------------------------

def sav_olvas(gyoker, b):
    """A brief sávja (SYSTEMS/CONTENT/SERVER/USER/BUSINESS) vagy BESOROLATLAN.

    Az elemző `sav` kulcsot ismer (az átmenet után a `feladatok.py` KULCSOK-jában), ezért a mező
    a `b.fej`-ben van; amíg a kulcs nincs a listában, az elemző `ismeretlen kulcs: sav` hibát
    jelez és eldobja az értéket -- ilyenkor a fejlécsort innen olvassuk ki."""
    ertek = b.fej.get('sav')
    if ertek is None and any('ismeretlen kulcs: sav' in h for h in b.hibak):
        ertek = _sav_a_fejlecbol(os.path.join(gyoker, b.fajl))
    ertek = (ertek or '').strip().strip('"\'').upper()
    return ertek if ertek in SAV_CIMKE and ertek != BESOROLATLAN else BESOROLATLAN


def _sav_a_fejlecbol(ut):
    try:
        with open(ut, encoding='utf-8', newline='') as f:
            sorok = f.read().replace('\r\n', '\n').split('\n')
    except OSError:
        return None
    if not sorok or sorok[0].lstrip('﻿').strip() != '---':
        return None
    for sor in sorok[1:]:
        if sor.strip() == '---':
            break
        m = SAV_SOR.match(sor)
        if m:
            return m.group(1)
    return None


def lezaras_datumok(gyoker, ma, nap):
    """{brief-fájlnév: dátum}: az `allapot: lezarva` sor az ablakban mergelt commitból (first-parent)."""
    tol = (ma - timedelta(days=nap + 3)).isoformat()
    ki = F._git(gyoker, 'log', '--first-parent', '--merges', '--since=%s' % tol,
                '-G', '^allapot: lezarva$', '--format=@%cs', '--name-only', '--', '*_BRIEF.md')
    eredmeny = {}
    if not ki:
        return eredmeny
    akt = None
    for sor in ki.split('\n'):
        sor = sor.strip()
        if not sor:
            continue
        if sor.startswith('@'):
            try:
                akt = datetime.strptime(sor[1:], '%Y-%m-%d').date()
            except ValueError:
                akt = None
        elif akt and sor.endswith('_BRIEF.md') and '/' not in sor:
            if sor not in eredmeny or akt > eredmeny[sor]:
                eredmeny[sor] = akt
    return eredmeny


def pr_lista_gh(gyoker, ma, nap):
    """(prok, hiba): a nyitott és az ablakban mergelt PR-ok a `gh pr list`-ből."""
    tol = (ma - timedelta(days=nap)).isoformat()
    mezok = 'number,title,state,isDraft,mergedAt,headRefName,url'
    prok = []
    for argok in (['--state', 'open', '--limit', '200'],
                  ['--state', 'merged', '--limit', '200', '--search', 'merged:>=%s' % tol]):
        try:
            p = subprocess.run(['gh', 'pr', 'list'] + argok + ['--json', mezok], cwd=gyoker,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as e:
            return [], 'a gh nem futott: %s' % e
        if p.returncode != 0:
            return [], 'a gh hibával állt le: %s' % p.stderr.decode('utf-8', 'replace').strip()[:200]
        try:
            prok.extend(json.loads(p.stdout.decode('utf-8')))
        except ValueError as e:
            return [], 'a gh kimenete nem JSON: %s' % e
    return prok, None


def pr_lista_fajl(ut):
    with open(ut, encoding='utf-8') as f:
        return json.load(f), None


def pr_brief_szamok(pr, by_szam):
    """A PR-hoz tartozó brief-számok: a brief `pr` mezője, `ag` mezője, majd a cím / ág `F<nn>` jelzése."""
    szamok = []
    szam = str(pr.get('number'))
    for n, b in by_szam.items():
        pr_mezo = str(b.fej.get('pr', '')).strip().strip('"\'').rstrip('/').split('/')[-1]
        if pr_mezo == szam or (b.fej.get('ag') and b.fej['ag'].strip('"\'') == pr.get('headRefName')):
            szamok.append(n)
    if szamok:
        return sorted(set(szamok))
    cim = PR_TITLE_ELOTAG.sub('', pr.get('title', ''))
    elol = cim.split(':', 1)[0] if ':' in cim else ''
    for m in PR_SZAM_A_CIMBEN.finditer(elol):
        if int(m.group(1)) in by_szam:
            szamok.append(int(m.group(1)))
    if not szamok:
        m = PR_SZAM_AZ_AGBAN.search(pr.get('headRefName', ''))
        if m and int(m.group(1)) in by_szam:
            szamok.append(int(m.group(1)))
    return sorted(set(szamok))


# ---------------------------------------------------------------------------
# csoportosítás (a tesztelhető mag: nincs benne git, gh vagy fájlírás)
# ---------------------------------------------------------------------------

def tisztit(szoveg):
    """Egy fejlécszöveg olvasható alakja: jelölőnyelv nélkül, belső azonosító-töredékek nélkül."""
    s = szoveg.replace('`', '').replace('**', '')
    s = re.sub(r'^\[[^\]]*\]\s*', '', s.strip())                         # [elteres_kor 2/2] stb.
    s = re.sub(r'\bELLENOR_[A-Za-z0-9_]+', 'az ellenőrzési jelentés', s)
    return re.sub(r'\s+', ' ', s).strip()


def szep_cim(szoveg):
    """A fejléc `cim` értéke a körülvevő idézőjelek és a jelölőnyelv nélkül."""
    c = str(szoveg).strip()
    if len(c) >= 2 and c[0] == c[-1] and c[0] in ('"', "'"):
        c = c[1:-1]
    return re.sub(r'\s+', ' ', c.replace('`', '').replace('**', '')).strip()


def vag(szoveg, max_hossz):
    if len(szoveg) <= max_hossz:
        return szoveg
    return szoveg[:max_hossz].rsplit(' ', 1)[0].rstrip(' ,;:—-') + ' …'


def teendo_szoveg(b):
    """A felhasználói teendő szövege, ha a brief nyitott és a felhasználóra vár; különben None.

    Teendő: a `kovetkezo` „Te:” előtaggal kezdődik, vagy az állapot `dontesre_var`, vagy a
    `kovetkezo` ⛔ jelet tartalmaz és a feladat már megkezdődött. A „Halasztva:” kezdetű, még nem esedékes tétel nem teendő."""
    if b.allapot == 'lezarva' or b.fej.get('tipus') not in ('feladat', 'naplozas'):
        return None
    kov = F._kov_szoveg(b)
    if kov.lower().startswith('halasztva'):
        return None
    if VAR_ELOTAG.match(kov) or b.allapot == 'dontesre_var':
        return tisztit(VAR_ELOTAG.sub('', kov, count=1))
    # a ⛔ (megállási pont) csak a már megkezdett munkánál esedékes; a még el nem indult feladat
    # későbbi ⛔ pontja nem mai teendő
    if '⛔' in kov and b.allapot not in ('nem_indult', 'brief_kell'):
        return tisztit(kov)
    return None


def allapot_kulcs(b, main_all):
    """A megjelenített állapot kulcsa (az ALLAPOT_CIMKE-ben)."""
    st = F.statusz(b, main_all)
    if st == 'kesz':
        return 'lezarva'
    if st == 'fut' and F.felbemaradt(b):
        return 'felbemaradt'
    if st == 'nem_indult' and F._kov_szoveg(b).lower().startswith('halasztva'):
        return 'halasztva'
    return st


def csoportosit(briefek, prok, main_all, ma, nap, lezarasok, sav_fv):
    """{sav: {FUT/VAR/KESZ: [elem,…]}} és a „te teendőid” lista.

    Elem: dict(fajta='brief'|'pr', ...). A `sav_fv(b)` adja a brief sávját; `lezarasok` a
    {fájlnév: dátum} git-adat (a lezárás napja), `prok` a PR-ek listája."""
    tol = ma - timedelta(days=nap)
    szamozott = [b for b in briefek if b.szam is not None and b.fej
                 and b.fej.get('tipus') in ('feladat', 'naplozas')]
    by_szam = {b.szam: b for b in szamozott}
    fugg = F.fuggesek(briefek, main_all)[0]

    pr_by_brief = {}
    pr_brief = {}
    for pr in prok:
        szamok = pr_brief_szamok(pr, by_szam)
        pr_brief[pr['number']] = szamok
        for n in szamok:
            pr_by_brief.setdefault(n, []).append(pr)

    def pr_datum(pr):
        if not pr.get('mergedAt'):
            return None
        return datetime.strptime(pr['mergedAt'][:10], '%Y-%m-%d').date()

    def pr_kep(pr):
        return {'szam': pr['number'], 'cim': PR_TITLE_ELOTAG.sub('', pr.get('title', '')),
                'url': pr.get('url', ''), 'piszkozat': bool(pr.get('isDraft')),
                'mergelt': bool(pr.get('mergedAt')), 'datum': pr_datum(pr)}

    sav_ures = lambda: {FUT: [], VAR: [], KESZ: []}  # noqa: E731
    sorok = {s: sav_ures() for s, _ in SAVOK}
    sorok[BESOROLATLAN] = sav_ures()
    teendok = []
    kirakott = set()

    for b in sorted(szamozott, key=lambda x: x.szam):
        sav = sav_fv(b)
        ak = allapot_kulcs(b, main_all)
        st = F.statusz(b, main_all)
        elem = {'fajta': 'brief', 'szam': b.szam, 'cim': szep_cim(b.fej.get('cim', '')), 'allapot': ak,
                'sav': sav, 'prok': [pr_kep(p) for p in pr_by_brief.get(b.szam, [])
                                     if not p.get('mergedAt')]}
        if st == 'kesz':
            datum = lezarasok.get(b.fajl) or F._osszegzes_datum(b.fej.get('lezarva_osszegzes', ''), ma)
            if datum is None or not (tol <= datum <= ma):
                continue
            elem['datum'] = datum
            elem['prok'] = [pr_kep(p) for p in pr_by_brief.get(b.szam, []) if p.get('mergedAt')]
            sorok[sav][KESZ].append(elem)
            kirakott.add(b.szam)
            continue
        if st in ('fut', 'megallt', 'dontesre_var', 'pr'):
            blokk = FUT
        else:
            blokk = VAR
            fugg_n = sorted(n for n in fugg.get(b.szam, {})
                            if n in by_szam and F.statusz(by_szam[n], main_all) != 'kesz')
            elem['varakozas'] = [(n, szep_cim(by_szam[n].fej.get('cim', ''))) for n in fugg_n]
        sorok[sav][blokk].append(elem)
        kirakott.add(b.szam)
        t = teendo_szoveg(b)
        if t is not None:
            teendok.append({'szam': b.szam, 'cim': elem['cim'], 'allapot': ak, 'sav': sav,
                            'teendo': t, 'prok': elem['prok']})

    # PR-ok, amelyeket egy brief sora még nem mutat: önálló sor (a nyitottak „folyamatban”, az ablakban
    # mergeltek „kész a héten” blokkba, a briefjük sávjában; briefje nélkül a besorolatlanba)
    mutatott = {q['szam'] for s in sorok.values() for blokk in s.values() for el in blokk for q in el['prok']}
    for pr in prok:
        if pr['number'] in mutatott:
            continue
        szamok = pr_brief_szamok(pr, by_szam)
        sav = sav_fv(by_szam[szamok[0]]) if szamok else BESOROLATLAN
        kep = pr_kep(pr)
        elem = {'fajta': 'pr', 'szam': None, 'cim': kep['cim'], 'allapot': None, 'sav': sav, 'prok': [kep]}
        if pr.get('mergedAt'):
            d = kep['datum']
            if d is None or not (tol <= d <= ma):
                continue
            elem['datum'] = d
            sorok[sav][KESZ].append(elem)
        else:
            sorok[sav][FUT].append(elem)

    for sav in sorok:
        sorok[sav][KESZ].sort(key=lambda e: (e['datum'], e['szam'] or 0), reverse=True)
    return sorok, teendok


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

HONAP = ('január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus',
         'szeptember', 'október', 'november', 'december')


def datum_szoveg(d):
    return '%d. %s %d.' % (d.year, HONAP[d.month - 1], d.day)


def e(szoveg):
    return html.escape(str(szoveg), quote=True)


def _pr_html(prok):
    if not prok:
        return ''
    reszek = []
    for p in prok:
        if p['mergelt']:
            jel = 'egyesítve'
        elif p['piszkozat']:
            jel = 'piszkozat'
        else:
            jel = 'nyitott'
        cimke = 'PR %d · %s' % (p['szam'], jel)
        if p['url']:
            reszek.append('<a class="pr" href="%s" title="%s">%s</a>' % (e(p['url']), e(p['cim']), e(cimke)))
        else:
            reszek.append('<span class="pr">%s</span>' % e(cimke))
    return ' '.join(reszek)


def _szam_html(szam):
    return '<span class="szam">#%d</span>' % szam if szam is not None else ''


def _elem_html(el, blokk):
    reszek = ['<li class="elem">']
    fej = []
    if el['fajta'] == 'brief':
        fej.append(_szam_html(el['szam']))
        fej.append('<span class="cim">%s</span>' % e(vag(el['cim'], CIM_MAX)))
    else:
        fej.append('<span class="cim">%s</span>' % e(vag(el['cim'], CIM_MAX)))
    reszek.append(' '.join(x for x in fej if x))
    meta = []
    if el['allapot']:
        meta.append('<span class="allapot a-%s">%s</span>' % (e(el['allapot']), e(ALLAPOT_CIMKE[el['allapot']])))
    if el.get('datum'):
        meta.append('<span class="datum">%s</span>' % e(datum_szoveg(el['datum'])))
    pr = _pr_html(el['prok'])
    if pr:
        meta.append(pr)
    if blokk == VAR and el.get('varakozas'):
        szamok = ', '.join('<span title="%s">#%d</span>' % (e(c), n) for n, c in el['varakozas'])
        meta.append('<span class="fugg">vár erre: %s</span>' % szamok)
    if meta:
        reszek.append('<div class="meta">%s</div>' % ' '.join(meta))
    reszek.append('</li>')
    return ''.join(reszek)


def _blokk_html(blokk, elemek):
    ures = '' if elemek else '<p class="ures">%s</p>' % e(BLOKK_URES[blokk])
    lista = '<ul>%s</ul>' % ''.join(_elem_html(x, blokk) for x in elemek) if elemek else ''
    return ('<div class="blokk b-%s"><h3>%s <span class="db">%d</span></h3>%s%s</div>'
            % (blokk, e(BLOKK_CIM[blokk]), len(elemek), lista, ures))


def _teendo_html(t):
    return ('<li class="teendo"><div class="fej">%s <span class="cim">%s</span></div>'
            '<div class="szoveg">%s</div><div class="meta"><span class="allapot a-%s">%s</span>'
            ' <span class="sav">%s</span> %s</div></li>'
            % (_szam_html(t['szam']), e(vag(t['cim'], CIM_MAX)), e(vag(t['teendo'], TEENDO_MAX)),
               e(t['allapot']), e(ALLAPOT_CIMKE[t['allapot']]), e(SAV_CIMKE[t['sav']]),
               _pr_html(t['prok'])))


CSS = """
:root{--bg:#f6f5f1;--felulet:#ffffff;--szoveg:#1d1d1b;--halk:#5e5d57;--vonal:#dedbd2;--kiemel:#2f5d8a;
--kiemel-bg:#e6eef6;--figy:#8a4b00;--figy-bg:#fbeedb;--jo:#2d6a3e;--jo-bg:#e3f1e6;--rossz:#9b2c2c;--rossz-bg:#f8e3e3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171716;--felulet:#222220;--szoveg:#ecebe6;
--halk:#a5a39a;--vonal:#3a3935;--kiemel:#8fb8e0;--kiemel-bg:#22313f;--figy:#f0b872;--figy-bg:#3a2d1b;--jo:#8fd0a0;
--jo-bg:#1f3325;--rossz:#f0a0a0;--rossz-bg:#3b2222}}
:root[data-theme="dark"]{--bg:#171716;--felulet:#222220;--szoveg:#ecebe6;--halk:#a5a39a;--vonal:#3a3935;--kiemel:#8fb8e0;
--kiemel-bg:#22313f;--figy:#f0b872;--figy-bg:#3a2d1b;--jo:#8fd0a0;--jo-bg:#1f3325;--rossz:#f0a0a0;--rossz-bg:#3b2222}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--szoveg);font:16px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:1.6rem;margin:0 0 4px}h2{font-size:1.25rem;margin:0 0 12px}h3{font-size:1rem;margin:0 0 8px}
.alcim{color:var(--halk);margin:0 0 20px}
.osszesito{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 28px;padding:0;list-style:none}
.osszesito a{display:block;padding:6px 12px;border:1px solid var(--vonal);border-radius:999px;background:var(--felulet);
color:var(--szoveg);text-decoration:none;font-size:.9rem}
.osszesito b{color:var(--kiemel)}
section{margin:0 0 32px;padding:16px;background:var(--felulet);border:1px solid var(--vonal);border-radius:12px}
ul{list-style:none;margin:0;padding:0}
.sorok{display:grid;gap:16px;grid-template-columns:1fr}
@media (min-width:900px){.sorok{grid-template-columns:repeat(3,minmax(0,1fr))}}
.db{display:inline-block;min-width:1.5em;padding:0 6px;border-radius:999px;background:var(--kiemel-bg);color:var(--kiemel);
font-size:.8rem;text-align:center;font-weight:600}
.elem,.teendo{padding:8px 0;border-top:1px solid var(--vonal);overflow-wrap:anywhere}
.elem:first-child,.teendo:first-child{border-top:0}
.szam{color:var(--halk);font-variant-numeric:tabular-nums;margin-right:4px}
.cim{font-weight:600}
.szoveg{margin:2px 0}
.meta{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:.85rem;color:var(--halk);margin-top:2px}
.allapot,.sav{padding:0 8px;border-radius:999px;background:var(--kiemel-bg);color:var(--kiemel);font-size:.8rem}
.a-megallt,.a-dontesre_var,.a-pr{background:var(--figy-bg);color:var(--figy)}
.a-lezarva{background:var(--jo-bg);color:var(--jo)}
.a-halasztva,.a-nem_indult,.a-brief_kell{background:var(--bg);color:var(--halk);border:1px solid var(--vonal)}
a.pr,.pr{color:var(--kiemel)}
.ures{color:var(--halk);font-style:italic;margin:0}
.teendok{border-color:var(--figy)}
.forras{color:var(--halk);font-size:.85rem;margin-top:24px}
.forras code{display:block;margin-top:6px;font:12px/1.4 ui-monospace,Consolas,monospace;overflow-wrap:anywhere}
"""


def html_keszit(sorok, teendok, ma, nap, forras_szoveg, ts):
    reszek = ['<!doctype html><html lang="hu"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>Heti áttekintő</title>'
              '<link rel="preconnect" href="https://fonts.googleapis.com">'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap">'
              '<style>%s</style></head><body><main>' % CSS]
    reszek.append('<h1>Heti áttekintő</h1><p class="alcim">%s állapota; „kész” = az elmúlt %d napban lezárult.</p>'
                  % (e(datum_szoveg(ma)), nap))
    sav_sorrend = [s for s, _ in SAVOK] + [BESOROLATLAN]
    reszek.append('<ul class="osszesito"><li><a href="#teendok">A te teendőid <b>%d</b></a></li>' % len(teendok))
    for sav in sav_sorrend:
        if sav == BESOROLATLAN and not any(sorok[sav].values()):
            continue
        db = sum(len(v) for v in sorok[sav].values())
        reszek.append('<li><a href="#sav-%s">%s <b>%d</b></a></li>' % (sav.lower(), e(SAV_CIMKE[sav]), db))
    reszek.append('</ul>')

    reszek.append('<section id="teendok" class="teendok"><h2>A te teendőid <span class="db">%d</span></h2>' % len(teendok))
    if teendok:
        reszek.append('<ul>%s</ul>' % ''.join(_teendo_html(t) for t in sorted(teendok, key=lambda x: x['szam'])))
    else:
        reszek.append('<p class="ures">Jelenleg nincs rád váró teendő.</p>')
    reszek.append('</section>')

    for sav in sav_sorrend:
        blokkok = sorok[sav]
        if sav == BESOROLATLAN and not any(blokkok.values()):
            continue
        reszek.append('<section id="sav-%s"><h2>%s</h2><div class="sorok">%s</div></section>'
                      % (sav.lower(), e(SAV_CIMKE[sav]),
                         ''.join(_blokk_html(b, blokkok[b]) for b in (FUT, VAR, KESZ))))
    reszek.append('<p class="forras">Összeállítva: %s.<br>Forrás: %s<code>%s</code></p>'
                  % (e(ts.strftime('%Y. %m. %d. %H:%M')), e(forras_szoveg[0]), e(forras_szoveg[1])))
    reszek.append('</main></body></html>')
    return ''.join(reszek)


# ---------------------------------------------------------------------------
# összeállítás és CLI
# ---------------------------------------------------------------------------

def osszeallit(gyoker, ma, nap, pr_json=None, ts=None):
    """(html, darabszamok, hibak): a teljes folyamat; a `darabszamok` {sav: {blokk: n}} + a teendők száma."""
    ts = ts or datetime.now()
    briefek = F.briefek_beolvas(gyoker)
    main_ref = F.main_ref(gyoker)
    main_all = F.main_allapotok(gyoker, main_ref) if main_ref else {}
    lezarasok = lezaras_datumok(gyoker, ma, nap)
    if pr_json:
        prok, pr_hiba = pr_lista_fajl(pr_json)
        pr_forras = 'fájl: %s' % os.path.basename(pr_json)
    else:
        prok, pr_hiba = pr_lista_gh(gyoker, ma, nap)
        pr_forras = 'gh pr list --state open | --state merged --search merged:>=%s' % (ma - timedelta(days=nap)).isoformat()
    sorok, teendok = csoportosit(briefek, prok, main_all, ma, nap, lezarasok,
                                 lambda b: sav_olvas(gyoker, b))
    olvashato = ('a feladatleírások fejlécei%s és a GitHub-ról lekért PR-ok (nyitottak és az elmúlt %d napban egyesítettek)'
                 % (' (az egyesített ággal egyeztetve)' if main_ref else '', nap))
    if pr_hiba:
        olvashato += '; FIGYELEM: a PR-adat nem érhető el (%s), a PR-hivatkozások hiányoznak' % pr_hiba
    ref_hash = (F._git(gyoker, 'rev-parse', '--short', main_ref) or '').strip() if main_ref else ''
    gepi = 'scope=%d brief-fejléc, %d PR | forras=%s%s | ts=%s' % (
        len(briefek), len(prok), 'feladatok.py (briefek_beolvas, main_allapotok%s), %s' % (
            ' @ %s %s' % (main_ref, ref_hash) if main_ref else '', pr_forras),
        '', ts.strftime('%Y-%m-%dT%H:%M:%S'))
    oldal = html_keszit(sorok, teendok, ma, nap, (olvashato, gepi), ts)
    szamok = {sav: {b: len(v) for b, v in blokkok.items()} for sav, blokkok in sorok.items()}
    return oldal, szamok, len(teendok), pr_hiba


def _repon_belul(ut, gyoker):
    ut = os.path.normcase(os.path.realpath(ut))
    gy = os.path.normcase(os.path.realpath(gyoker))
    return ut == gy or ut.startswith(gy + os.sep)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Heti áttekintő oldal generálása a brief-fejlécekből és a PR-okból.')
    ap.add_argument('--kimenet', required=True, help='a HTML útja (a repón kívül)')
    ap.add_argument('--gyoker', default=REPO)
    ap.add_argument('--ma', help='ÉÉÉÉ-HH-NN; alapértelmezés: ma')
    ap.add_argument('--nap', type=int, default=7, help='a „kész a héten” ablak napjai (alap: 7)')
    ap.add_argument('--pr-json', help='a gh helyett: PR-lista JSON-fájlból')
    a = ap.parse_args(argv)
    if _repon_belul(a.kimenet, a.gyoker):
        print('HIBA: a --kimenet a repón belülre mutat; a generált nézet a repón kívülre kerül.', file=sys.stderr)
        return 2
    ma = datetime.strptime(a.ma, '%Y-%m-%d').date() if a.ma else date.today()
    oldal, szamok, teendok_db, pr_hiba = osszeallit(a.gyoker, ma, a.nap, pr_json=a.pr_json)
    os.makedirs(os.path.dirname(os.path.abspath(a.kimenet)), exist_ok=True)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(oldal)
    print('kimenet: %s' % os.path.abspath(a.kimenet))
    print('a te teendőid: %d' % teendok_db)
    for sav in [s for s, _ in SAVOK] + [BESOROLATLAN]:
        b = szamok[sav]
        print('%s: folyamatban %d, vár %d, kész a héten %d' % (SAV_CIMKE[sav], b[FUT], b[VAR], b[KESZ]))
    if pr_hiba:
        print('FIGYELEM: %s' % pr_hiba, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
