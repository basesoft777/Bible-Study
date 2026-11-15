#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
heti_attekinto.py -- a heti áttekintő oldal generátora.

A brief-fejlécekből (az `eszkozok/feladatok.py` beolvasó függvényeivel, csak olvasva) és a
GitHub nyitott PR-jaiból sávonként csoportosított, önálló HTML-oldalt készít a felhasználónak: fent
„A te teendőid”, utána öt sáv (fejlesztői infrastruktúra, tartalomkészítés, olvasó, felhasználók, üzleti oldal),
mindegyikben két blokk: folyamatban (`fut`, `megallt`) / vár (`nem_indult`, `brief_kell`,
`dontesre_var`, a függésekkel).

Az oldal csak nyitott tételt mutat: a lezárt brief (`allapot: lezarva`) és a mergelt PR nem szerepel
rajta (a felhasználó döntése, 2026-11-15). Lezárt tétel ezért „kész a héten” blokkba sem kerül.

A sávot a brief `sav` fejlécmezője adja (SYSTEMS / CONTENT / SERVER / USER / BUSINESS). Besorolatlan csoport
nincs: ha egy feladat- vagy naplózás-típusú brief `sav` mezője hiányzik vagy ismeretlen, az hiba (a
szkript 2-es kóddal áll meg, és nem ír oldalt). Kivétel az átmeneti `feladatok.SAV_ATMENET_KIVETEL`
(a saját PR-jukban `sav`-ot kapó briefek): ezek az `ATMENET_SAV` táblából kapnak sávot.

A kimenet generált nézet: a `--kimenet` a repón kívülre mutasson (CLAUDE.md: a kimeneti próbák a
repón kívülre mennek), a szkript a repón belüli útvonalat elutasítja.

Használat:
    python eszkozok/heti_attekinto.py --kimenet <út.html>
        [--gyoker <repó>] [--ma ÉÉÉÉ-HH-NN] [--pr-json <fájl>]

`--pr-json`: a `gh` helyett a fájlból olvassa a PR-listát (egy JSON-tömb: number, title, state,
isDraft, mergedAt, headRefName, url); a mergelt elemeket figyelmen kívül hagyja. Teszthez és
kapcsolat nélküli futtatáshoz.

Kilépési kód: 0 = rendben, 2 = hiba.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime

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
SAV_CIMKE = dict(SAVOK)
# Átmenet: a saját PR-jukban `sav`-ot kapó briefek ideiglenes sávja (l. feladatok.SAV_ATMENET_KIVETEL).
# A PR-ok merge-e után a tuple kiürül, ez a tábla is törölhető. Besorolás: az F217 a generálást futtató
# Action (SYSTEMS), az F218 a lapgenerátor (CONTENT) -- a BRIEF_SABLON `sav` sorának szabálya szerint.
ATMENET_SAV = {217: 'SYSTEMS', 218: 'CONTENT'}

ALLAPOT_CIMKE = {
    'nem_indult': 'nem indult',
    'brief_kell': 'feladatleírás kell',
    'fut': 'folyamatban',
    'dontesre_var': 'döntésre vár',
    'megallt': 'megállt',
    'felbemaradt': 'félbemaradt, folytatható',
    'halasztva': 'halasztva',
}
# a két blokk (oszlop) a sávokon belül
FUT, VAR = 'fut', 'var'
BLOKK_CIM = {FUT: 'Folyamatban', VAR: 'Vár'}
BLOKK_URES = {FUT: 'Nincs folyamatban lévő munka.', VAR: 'Nincs várakozó feladat.'}
FUT_ALLAPOTOK = ('fut', 'megallt')
TEENDO_MAX = 230     # a „te teendőid” sor szövegének legfeljebb ennyi karaktere látszik
CIM_MAX = 120

PR_TITLE_ELOTAG = re.compile(r'^\s*\[[^\]]*\]\s*')            # „[ELLENŐRZŐ] ” a PR-címek elején
PR_SZAM_A_CIMBEN = re.compile(r'\bF(\d+)')
PR_SZAM_AZ_AGBAN = re.compile(r'(?:^|/)f(\d+)(?:[-_.]|$)')
VAR_ELOTAG = re.compile(r'^\s*Te\s*(?:\(⛔\))?\s*:\s*')


# ---------------------------------------------------------------------------
# bemenet
# ---------------------------------------------------------------------------

def sav_olvas(b):
    """A brief sávja (SYSTEMS/CONTENT/SERVER/USER/BUSINESS), vagy None, ha a mező hiányzik vagy ismeretlen."""
    ertek = (b.fej.get('sav') or '').strip().strip('"\'').upper()
    if ertek in SAV_CIMKE:
        return ertek
    if not ertek and b.szam in getattr(F, 'SAV_ATMENET_KIVETEL', ()):
        return ATMENET_SAV.get(b.szam)
    return None


def pr_lista_gh(gyoker):
    """(prok, hiba): a nyitott PR-ok a `gh pr list`-ből."""
    try:
        p = subprocess.run(['gh', 'pr', 'list', '--state', 'open', '--limit', '200', '--json',
                            'number,title,state,isDraft,mergedAt,headRefName,url'], cwd=gyoker,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        return [], 'a gh nem futott: %s' % e
    if p.returncode != 0:
        return [], 'a gh hibával állt le: %s' % p.stderr.decode('utf-8', 'replace').strip()[:200]
    try:
        return json.loads(p.stdout.decode('utf-8')), None
    except ValueError as e:
        return [], 'a gh kimenete nem JSON: %s' % e


def pr_lista_fajl(ut):
    with open(ut, encoding='utf-8') as f:
        return [p for p in json.load(f) if not p.get('mergedAt')], None


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


def allapot_kulcs(b):
    """A megjelenített állapot kulcsa (az ALLAPOT_CIMKE-ben); csak nyitott briefre hívjuk."""
    if b.allapot == 'fut' and F.felbemaradt(b):
        return 'felbemaradt'
    if b.allapot == 'nem_indult' and F._kov_szoveg(b).lower().startswith('halasztva'):
        return 'halasztva'
    return b.allapot


def csoportosit(briefek, prok, main_all, sav_fv):
    """(sorok, teendok, hibak, brief_nelkuli_db): {sav: {FUT/VAR: [elem,…]}}, a „te teendőid” lista,
    a hibák listája és a brief nélküli nyitott PR-ok száma.

    Csak nyitott brief kerül ki: a `lezarva` állapotú (az ág által már lezárt, a main-en még nem lezárt
    is) kimarad. Elem: dict(fajta='brief', ...); a `prok` a brief nyitott PR-jai. A `sav_fv(b)` a brief
    sávját adja, None-t, ha a mező hiányzik vagy ismeretlen: az hiba, nem csoport (a brief ilyenkor
    nem kerül ki). A brief nélküli PR nem kerül az oldalra, csak a számuk jut vissza."""
    szamozott = [b for b in briefek if b.szam is not None and b.fej
                 and b.fej.get('tipus') in ('feladat', 'naplozas')]
    by_szam = {b.szam: b for b in szamozott}
    fugg = F.fuggesek(briefek, main_all)[0]

    pr_by_brief = {}
    brief_nelkuli = []
    for pr in prok:
        if pr.get('mergedAt'):
            continue
        szamok = pr_brief_szamok(pr, by_szam)
        if not szamok:
            brief_nelkuli.append(pr)
        for n in szamok:
            pr_by_brief.setdefault(n, []).append(pr)

    def pr_kep(pr):
        return {'szam': pr['number'], 'cim': PR_TITLE_ELOTAG.sub('', pr.get('title', '')),
                'url': pr.get('url', ''), 'piszkozat': bool(pr.get('isDraft'))}

    sorok = {s: {FUT: [], VAR: []} for s, _ in SAVOK}
    teendok = []
    hibak = []

    for b in sorted(szamozott, key=lambda x: x.szam):
        if b.allapot == 'lezarva':
            continue
        sav = sav_fv(b)
        if sav is None:
            hibak.append('#%d: a `sav` mező hiányzik vagy ismeretlen (%s)'
                         % (b.szam, ' | '.join(s for s, _ in SAVOK)))
            continue
        ak = allapot_kulcs(b)
        elem = {'fajta': 'brief', 'szam': b.szam, 'cim': szep_cim(b.fej.get('cim', '')), 'allapot': ak,
                'sav': sav, 'prok': [pr_kep(p) for p in pr_by_brief.get(b.szam, [])]}
        if b.allapot in FUT_ALLAPOTOK:
            blokk = FUT
        else:
            blokk = VAR
            fugg_n = sorted(n for n in fugg.get(b.szam, {})
                            if n in by_szam and by_szam[n].allapot != 'lezarva')
            elem['varakozas'] = [(n, szep_cim(by_szam[n].fej.get('cim', ''))) for n in fugg_n]
        sorok[sav][blokk].append(elem)
        t = teendo_szoveg(b)
        if t is not None:
            teendok.append({'szam': b.szam, 'cim': elem['cim'], 'allapot': ak, 'sav': sav,
                            'teendo': t, 'prok': elem['prok']})

    return sorok, teendok, hibak, len(brief_nelkuli)


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
        cimke = 'PR %d · %s' % (p['szam'], 'piszkozat' if p['piszkozat'] else 'nyitott')
        if p['url']:
            reszek.append('<a class="pr" href="%s" title="%s">%s</a>' % (e(p['url']), e(p['cim']), e(cimke)))
        else:
            reszek.append('<span class="pr">%s</span>' % e(cimke))
    return ' '.join(reszek)


def _szam_html(szam):
    return '<span class="szam">#%d</span>' % szam if szam is not None else ''


def _elem_html(el, blokk):
    reszek = ['<li class="elem">']
    reszek.append('%s <span class="cim">%s</span>' % (_szam_html(el['szam']), e(vag(el['cim'], CIM_MAX))))
    meta = ['<span class="allapot a-%s">%s</span>' % (e(el['allapot']), e(ALLAPOT_CIMKE[el['allapot']]))]
    pr = _pr_html(el['prok'])
    if pr:
        meta.append(pr)
    if blokk == VAR and el.get('varakozas'):
        szamok = ', '.join('<span title="%s">#%d</span>' % (e(c), n) for n, c in el['varakozas'])
        meta.append('<span class="fugg">vár erre: %s</span>' % szamok)
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
@media (min-width:700px){.sorok{grid-template-columns:repeat(2,minmax(0,1fr))}}
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
.a-halasztva,.a-nem_indult,.a-brief_kell{background:var(--bg);color:var(--halk);border:1px solid var(--vonal)}
a.pr,.pr{color:var(--kiemel)}
.ures{color:var(--halk);font-style:italic;margin:0}
.teendok{border-color:var(--figy)}
.forras{color:var(--halk);font-size:.85rem;margin-top:24px}
.forras code{display:block;margin-top:6px;font:12px/1.4 ui-monospace,Consolas,monospace;overflow-wrap:anywhere}
"""


def html_keszit(sorok, teendok, ma, forras_szoveg, ts, brief_nelkuli_db=0):
    reszek = ['<!doctype html><html lang="hu"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>Heti áttekintő</title>'
              '<link rel="preconnect" href="https://fonts.googleapis.com">'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap">'
              '<style>%s</style></head><body><main>' % CSS]
    reszek.append('<h1>Heti áttekintő</h1><p class="alcim">%s állapota; csak a nyitott tételek.</p>'
                  % e(datum_szoveg(ma)))
    reszek.append('<ul class="osszesito"><li><a href="#teendok">A te teendőid <b>%d</b></a></li>' % len(teendok))
    for sav, cimke in SAVOK:
        db = sum(len(v) for v in sorok[sav].values())
        reszek.append('<li><a href="#sav-%s">%s <b>%d</b></a></li>' % (sav.lower(), e(cimke), db))
    reszek.append('</ul>')

    reszek.append('<section id="teendok" class="teendok"><h2>A te teendőid <span class="db">%d</span></h2>' % len(teendok))
    if teendok:
        reszek.append('<ul>%s</ul>' % ''.join(_teendo_html(t) for t in sorted(teendok, key=lambda x: x['szam'])))
    else:
        reszek.append('<p class="ures">Jelenleg nincs rád váró teendő.</p>')
    reszek.append('</section>')

    for sav, cimke in SAVOK:
        reszek.append('<section id="sav-%s"><h2>%s</h2><div class="sorok">%s</div></section>'
                      % (sav.lower(), e(cimke), ''.join(_blokk_html(b, sorok[sav][b]) for b in (FUT, VAR))))
    megjegyzes = ('<br>%d nyitott PR-hoz nincs feladatleírás; ezek nem szerepelnek az oldalon.' % brief_nelkuli_db
                  if brief_nelkuli_db else '')
    reszek.append('<p class="forras">Összeállítva: %s.%s<br>Forrás: %s<code>%s</code></p>'
                  % (e(ts.strftime('%Y. %m. %d. %H:%M')), megjegyzes, e(forras_szoveg[0]), e(forras_szoveg[1])))
    reszek.append('</main></body></html>')
    return ''.join(reszek)


# ---------------------------------------------------------------------------
# összeállítás és CLI
# ---------------------------------------------------------------------------

def osszeallit(gyoker, ma, pr_json=None, ts=None):
    """(html, darabszamok, hibak, pr_hiba): a teljes folyamat; a `darabszamok` {sav: {blokk: n}}.
    Hiba (hiányzó vagy ismeretlen `sav`) esetén az `html` None."""
    ts = ts or datetime.now()
    briefek = F.briefek_beolvas(gyoker)
    main_ref = F.main_ref(gyoker)
    main_all = F.main_allapotok(gyoker, main_ref) if main_ref else {}
    if pr_json:
        prok, pr_hiba = pr_lista_fajl(pr_json)
        pr_forras = 'fájl: %s' % os.path.basename(pr_json)
    else:
        prok, pr_hiba = pr_lista_gh(gyoker)
        pr_forras = 'gh pr list --state open'
    sorok, teendok, hibak, brief_nelkuli = csoportosit(briefek, prok, main_all, sav_olvas)
    if hibak:
        return None, None, hibak, pr_hiba
    olvashato = ('a feladatleírások fejlécei%s és a GitHub-ról lekért nyitott PR-ok'
                 % (' (az egyesített ággal egyeztetve)' if main_ref else ''))
    if pr_hiba:
        olvashato += '; FIGYELEM: a PR-adat nem érhető el (%s), a PR-hivatkozások hiányoznak' % pr_hiba
    ref_hash = (F._git(gyoker, 'rev-parse', '--short', main_ref) or '').strip() if main_ref else ''
    gepi = 'scope=%d brief-fejléc, %d nyitott PR | forras=feladatok.py (briefek_beolvas, main_allapotok%s), %s | ts=%s' % (
        len(briefek), len(prok), ' @ %s %s' % (main_ref, ref_hash) if main_ref else '', pr_forras,
        ts.strftime('%Y-%m-%dT%H:%M:%S'))
    oldal = html_keszit(sorok, teendok, ma, (olvashato, gepi), ts, brief_nelkuli)
    szamok = {sav: {b: len(v) for b, v in blokkok.items()} for sav, blokkok in sorok.items()}
    szamok['teendok'] = len(teendok)
    return oldal, szamok, [], pr_hiba


def _repon_belul(ut, gyoker):
    ut = os.path.normcase(os.path.realpath(ut))
    gy = os.path.normcase(os.path.realpath(gyoker))
    return ut == gy or ut.startswith(gy + os.sep)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Heti áttekintő oldal generálása a brief-fejlécekből és a nyitott PR-okból.')
    ap.add_argument('--kimenet', required=True, help='a HTML útja (a repón kívül)')
    ap.add_argument('--gyoker', default=REPO)
    ap.add_argument('--ma', help='ÉÉÉÉ-HH-NN; alapértelmezés: ma')
    ap.add_argument('--pr-json', help='a gh helyett: PR-lista JSON-fájlból')
    a = ap.parse_args(argv)
    if _repon_belul(a.kimenet, a.gyoker):
        print('HIBA: a --kimenet a repón belülre mutat; a generált nézet a repón kívülre kerül.', file=sys.stderr)
        return 2
    ma = datetime.strptime(a.ma, '%Y-%m-%d').date() if a.ma else date.today()
    oldal, szamok, hibak, pr_hiba = osszeallit(a.gyoker, ma, pr_json=a.pr_json)
    if hibak:
        for h in hibak:
            print('HIBA: %s' % h, file=sys.stderr)
        print('HIBA: az oldal nem készült el (%d hiba).' % len(hibak), file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.kimenet)), exist_ok=True)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(oldal)
    print('kimenet: %s' % os.path.abspath(a.kimenet))
    print('a te teendőid: %d' % szamok['teendok'])
    for sav, cimke in SAVOK:
        b = szamok[sav]
        print('%s: folyamatban %d, vár %d' % (cimke, b[FUT], b[VAR]))
    if pr_hiba:
        print('FIGYELEM: %s' % pr_hiba, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
