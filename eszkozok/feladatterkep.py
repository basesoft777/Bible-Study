#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feladatterkep.py -- F53_FELADATTERKEP_BRIEF.md: a feladatok, dontesek es a
munkaterv generalt vizualis attekintese.

Egy futasbol ket kimenet, mindig ugyanazon a neven felulirva:
    feladatterkep.json   a lap osszes adata, kinezet nelkul
    FELADATTERKEP.html   onallo lap, a JSON beagyazva

Bemenetek (a repo adata, nem kezi masolat): a `*_BRIEF.md` fejlecek
(`feladatok.py` fuggvenyei), `MUNKATERV.md`, `DONTESEK.md`, es egyetlen kezi
tabla: `eszkozok/feladatterkep_kartyak.tsv` (kartyaszovegek). Ami a forrasban
nincs, azt a generator nem tolti ki: kartyaszoveg nelkuli feladat „nincs leiras"
jelolessel jelenik meg, oszlopszam-elteres DONTESEK-sor `ellenorizendo`.

Idempotens: a kimenet nem tartalmaz futasi idobelyeget; a belyeg a forrasok
utolso valtozasanak datuma es commitja (`git log -1 -- <forrasok>`).

A `csv` modul nem hasznalhato (CLAUDE.md): olvasas `split('\\t')`, iras
`'\\t'.join()`.

Hasznalat:
    python eszkozok/feladatterkep.py                  # a repo gyokerebe ir
    python eszkozok/feladatterkep.py --kimenet DIR    # DIR-be (repon kivulre)
    python eszkozok/feladatterkep.py --csak-json      # csak a JSON
"""

import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402

REPO = F.REPO
KARTYAK_TSV = 'eszkozok/feladatterkep_kartyak.tsv'   # `/`: a kimenet OS-fuggetlen
JSON_NEV = 'feladatterkep.json'
HTML_NEV = 'FELADATTERKEP.html'

# a belyeg forrasai (git log -1 -- ...): a lap adatanak bemenetei
BELYEG_FORRASOK = (':(glob)*_BRIEF.md', 'MUNKATERV.md', 'DONTESEK.md', KARTYAK_TSV)

NINCS_LEIRAS = 'nincs leírás'

ALLAPOT_CIMKE = (
    ('stop', 'Megállt (⛔)'),
    ('run', 'Fut (▶)'),
    ('ready', 'Indítható'),
    ('wait', 'Függésre vár'),
    ('plan', 'Tervezett, felvehető'),
    ('idle', 'Brief kell / halasztva'),
)
CSEMPE_CIMKE = (
    ('stop', 'Megállt, rád vár'),
    ('run', 'Fut'),
    ('ready', 'Indítható most'),
    ('wait', 'Függésre vár'),
    ('plan', 'Felvehető új sor'),
)
FAZIS_CIMKE = (('1', '1. fázis · adat'), ('2', '2. fázis · render'),
               ('folyamat', 'Folyamat'), ('naplozas', 'Naplózás'))

DT_JELEK = (('🟡', 'nyitott'), ('🟢', 'alkalmazasra_var'), ('✅', 'kesz'))


# ---------------------------------------------------------------------------
# kezi bemenet: kartyaszovegek
# ---------------------------------------------------------------------------

def kartyak_olvas(gyoker):
    """{kod: {'reszletes', 'roviden', 'forras'}}; hianyzo fajl: ures."""
    ut = os.path.join(gyoker, KARTYAK_TSV)
    if not os.path.exists(ut):
        return {}
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().replace('\r\n', '\n').split('\n')
    if not sorok:
        return {}
    fejlec = sorok[0].split('\t')
    eredmeny = {}
    for sor in sorok[1:]:
        if not sor.strip():
            continue
        mezok = sor.split('\t')
        rek = dict(zip(fejlec, mezok))
        kod = rek.get('kod', '').strip()
        if kod and kod not in eredmeny:
            eredmeny[kod] = {'reszletes': rek.get('reszletes', '').strip(),
                             'roviden': rek.get('roviden', '').strip(),
                             'forras': rek.get('forras', '').strip()}
    return eredmeny


# ---------------------------------------------------------------------------
# markdown-tablak olvasasa (split `|`, a `\|` nem hatar)
# ---------------------------------------------------------------------------

CELLA_HATAR = re.compile(r'(?<!\\)\|')


def _tisztit(s):
    return s.replace('\\_', '_').replace('\\|', '|').strip()


def sor_cellak(sor):
    """A `| a | b |` sor cellai (a szelso ures elemek nelkul)."""
    reszek = CELLA_HATAR.split(sor.strip())
    return reszek[1:-1] if len(reszek) >= 2 else reszek


def szakaszok(szoveg):
    """[(cim, [sorok])] a `## ` fejlecek szerint."""
    ki = []
    akt = None
    for sor in szoveg.replace('\r\n', '\n').split('\n'):
        if sor.startswith('## '):
            akt = (sor[3:].strip(), [])
            ki.append(akt)
        elif akt is not None:
            akt[1].append(sor)
    return ki


def tablak(sorok):
    """[(fejlec_cellak, [sor_cellak])]: a szakasz osszes tablaja."""
    ki = []
    i = 0
    while i < len(sorok):
        if sorok[i].startswith('|') and i + 1 < len(sorok) and re.match(
                r'^\|[\s\-|:]+\|?\s*$', sorok[i + 1]):
            fej = [_tisztit(c) for c in sor_cellak(sorok[i])]
            sorok_ = []
            i += 2
            while i < len(sorok) and sorok[i].startswith('|'):
                sorok_.append([_tisztit(c) for c in sor_cellak(sorok[i])])
                i += 1
            ki.append((fej, sorok_))
        else:
            i += 1
    return ki


def _tabla_fejlec_szerint(sorok, *kezdet):
    """Az elso tabla, amelynek fejlece az adott szavakkal kezdodik (kisbetus)."""
    for fej, rows in tablak(sorok):
        kis = [c.lower() for c in fej]
        if all(i < len(kis) and kis[i].startswith(k) for i, k in enumerate(kezdet)):
            return fej, rows
    return None, []


def _oszlop(fej, *kulcsok):
    kis = [c.lower() for c in fej]
    for k in kulcsok:
        for i, c in enumerate(kis):
            if c.startswith(k):
                return i
    return None


def _cella(row, i):
    return row[i] if i is not None and i < len(row) else ''


def munkaterv_olvas(gyoker):
    """A MUNKATERV.md gepi olvasata: {'dt', 'tervezett', 'fazis', 'hullamok'}."""
    ut = os.path.join(gyoker, 'MUNKATERV.md')
    if not os.path.exists(ut):
        return {'dt': [], 'tervezett': [], 'fazis': {}, 'hullamok': []}
    with open(ut, encoding='utf-8', newline='') as f:
        szakaszok_ = szakaszok(f.read())

    def szakasz(elotag):
        for cim, sorok in szakaszok_:
            if cim.startswith(elotag):
                return sorok
        return []

    dt = []
    fej, rows = _tabla_fejlec_szerint(szakasz('2.'), '#', 'döntés')
    for r in rows:
        if r and r[0].startswith('DT'):
            dt.append({'id': r[0], 'kerdes': _cella(r, 1),
                       'irany': _cella(r, _oszlop(fej, 'javasolt')),
                       'feladat': _cella(r, _oszlop(fej, 'melyik'))})

    tervezett = []
    fej, rows = _tabla_fejlec_szerint(szakasz('4.'), '#', 'név', 'cél')
    if fej:
        i_cel, i_fugg = _oszlop(fej, 'cél'), _oszlop(fej, 'függ')
        for r in rows:
            if not r or r[0] not in ('—', '-'):
                continue
            m = re.match(r'[A-Z][A-Z0-9_]+', _cella(r, 1))
            if not m:
                continue
            tervezett.append({'kod': m.group(0), 'cel': _cella(r, i_cel),
                              'fugg': _cella(r, i_fugg)})

    fazis = {}
    fej, rows = _tabla_fejlec_szerint(szakasz('4a'), '#', 'fázis', 'mire')
    for r in rows:
        m = re.match(r'[A-Z][A-Z0-9_]+', r[0]) if r else None
        if m and len(r) > 1:
            fazis[m.group(0)] = r[1]

    hullamok = []
    fej, rows = _tabla_fejlec_szerint(szakasz('5.'), 'hullám', 'feladatok')
    for r in rows:
        if len(r) < 2:
            continue
        hullamok.append({'nev': (r[0] + '. hullám') if r[0].isdigit() else r[0].capitalize(),
                         'elemek_szoveg': _cella(r, 1),
                         'kapu': _cella(r, _oszlop(fej, '⛔'))})
    return {'dt': dt, 'tervezett': tervezett, 'fazis': fazis, 'hullamok': hullamok}


# ---------------------------------------------------------------------------
# DONTESEK.md
# ---------------------------------------------------------------------------

def dontesek_olvas(gyoker):
    """[{'id', 'feladat', 'kerdes', 'allapot', 'jelek', 'ellenorizendo'}].

    Az allapot-oszlop a fejlec szerinti helyen all; ha egy sor oszlopszama
    eltér a fejlecetol (a szabad szoveg `|`-t tartalmaz), a sor
    `ellenorizendo`, az allapotot nem talalgatjuk -- csak a sorban talalt
    ismert jeleket soroljuk fel."""
    ut = os.path.join(gyoker, 'DONTESEK.md')
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().replace('\r\n', '\n').split('\n')
    fej = None
    ki = []
    for i, sor in enumerate(sorok):
        if not sor.startswith('| '):
            continue
        cellak = sor_cellak(sor)
        if fej is None:
            if cellak and cellak[0].strip() == '#':
                fej = [c.strip() for c in cellak]
            continue
        if re.match(r'^\|[\s\-|:]+\|?\s*$', sor):
            continue
        azon = cellak[0].strip() if cellak else ''
        if not azon:
            continue
        jelek = [j for j, _ in DT_JELEK if j in sor]
        rek = {'id': azon, 'jelek': jelek, 'sor': i + 1}
        if len(cellak) != len(fej):
            rek.update({'feladat': _cella([c.strip() for c in cellak], 1),
                        'kerdes': _cella([c.strip() for c in cellak], 2),
                        'allapot': 'ellenorizendo', 'ellenorizendo': True,
                        'oszlopszam': len(cellak), 'fejlec_oszlopszam': len(fej)})
        else:
            i_all = _oszlop(fej, 'állapot')
            cs = [c.strip() for c in cellak]
            jel = cs[i_all]
            allapot = None
            for j, nev in DT_JELEK:
                if jel.startswith(j):
                    allapot = nev
            if jel.lower().startswith('nyitott'):
                allapot = 'nyitott'
            if allapot is None:
                rek.update({'allapot': 'ellenorizendo', 'ellenorizendo': True})
            else:
                rek.update({'allapot': allapot, 'ellenorizendo': False})
            rek.update({'feladat': _cella(cs, _oszlop(fej, 'feladat')),
                        'kerdes': _cella(cs, _oszlop(fej, 'kérdés')),
                        'javaslat': _cella(cs, _oszlop(fej, 'javaslat'))})
        rek['kerdes'] = rek.get('kerdes', '').replace('**', '')
        ki.append(rek)
    return ki


# ---------------------------------------------------------------------------
# allapot-besorolas
# ---------------------------------------------------------------------------

def _kov(b):
    return F._kov_szoveg(b).replace('**', '')


def kartya_allapot(b, fugg, by_szam, main_all):
    """A hat lap-allapot egyike: stop / run / ready / wait / idle (`plan`: tervezett).

    pr (lezarva, de a main-en meg nem) -> run; megallt, dontesre_var, a `Te:`
    kovetkezo lepes -> stop; fut -> run (a felbemaradt, `Folytatás:` kivetel:
    az mint a nem indult); brief_kell, `halasztva` -> idle; egyebkent a
    nem-kesz fuggesek szerint wait / ready."""
    st = F.statusz(b, main_all)
    if st == 'pr':
        return 'run'
    if b.allapot in ('megallt', 'dontesre_var'):
        return 'stop'
    if b.allapot == 'fut' and not F.felbemaradt(b):
        return 'run'
    if b.allapot == 'brief_kell':
        return 'idle'
    kov = F._kov_szoveg(b)
    if kov.startswith(F.VAR_RAD_ELOTAG):
        return 'stop'
    if kov.lower().startswith('halasztva'):
        return 'idle'
    var = [n for n in fugg.get(b.szam, {})
           if n in by_szam and F.statusz(by_szam[n], main_all) != 'kesz'
           and n not in b.fej.get('nem_fugg', [])]
    return 'wait' if var else 'ready'


def _clip(s, n):
    s = ' '.join(s.split())
    if len(s) <= n:
        return s
    vag = s[:n].rsplit(' ', 1)[0]
    return vag.rstrip(' ,;:—-') + '…'


# ---------------------------------------------------------------------------
# a lap adata
# ---------------------------------------------------------------------------

def belyeg(gyoker):
    """A forrasok utolso valtozasanak {'datum', 'commit'} -- nem a HEAD, nem a futas ideje."""
    ki = F._git(gyoker, 'log', '-1', '--format=%h %cs', '--', *BELYEG_FORRASOK)
    if not ki or not ki.strip():
        return {'datum': None, 'commit': None}
    h, d = ki.strip().split()[:2]
    return {'datum': d, 'commit': h}


ID_TOKEN = re.compile(r'#(\d+)(?![\da-z])|(DT-?[A-Za-z]*\d+[a-z]?)|\b([A-Z][A-Z0-9_]{3,})\b')


def epit(gyoker=REPO, main_all=None):
    """A feladatterkep.json tartalma (dict). Nem ir fajlt."""
    briefek = F.briefek_beolvas(gyoker)
    if main_all is None:
        main_all = F.main_allapotok(gyoker)
    szamozottak = [b for b in briefek if b.szam is not None and b.fej]
    by_szam = {b.szam: b for b in szamozottak}
    fugg, _, _, _ = F.fuggesek(briefek, main_all)
    kartya_szoveg = kartyak_olvas(gyoker)
    mt = munkaterv_olvas(gyoker)
    dt_sorok = dontesek_olvas(gyoker)

    kesz_szamok = set(n for n, b in by_szam.items() if F.statusz(b, main_all) == 'kesz')
    kesz_kodok = set(b.fej['kod'] for b in szamozottak
                     if b.szam in kesz_szamok and 'kod' in b.fej)

    kartyak = []
    hasznalt = set()

    def szoveg(kulcs):
        r = kartya_szoveg.get(kulcs)
        if r:
            hasznalt.add(kulcs)
        return r

    nyitott = [b for b in szamozottak
               if b.fej.get('tipus') in ('feladat', 'naplozas')
               and F.statusz(b, main_all) != 'kesz']
    for b in sorted(nyitott, key=lambda x: x.szam):
        kulcs = b.fej.get('kod') or '#%d' % b.szam
        r = szoveg(kulcs)
        fazis = b.fej.get('fazis') if b.fej.get('tipus') == 'feladat' else 'naplozas'
        kartyak.append({
            'kulcs': kulcs, 'szam': b.szam, 'kod': b.fej.get('kod'),
            'cim': b.fej['cim'].strip('"'), 'fazis': fazis,
            'allapot': kartya_allapot(b, fugg, by_szam, main_all),
            'brief_allapot': F.statusz(b, main_all),
            'most': _kov(b),
            'fugg': F._fugg_cella(b, fugg, by_szam, main_all),
            'tervezett': False,
            'reszletes': r['reszletes'] if r else '',
            'roviden': r['roviden'] if r else '',
            'leiras_forras': r['forras'] if r else None,
            'leiras_hiany': r is None,
        })

    brief_kodok = set(k['kod'] for k in kartyak if k['kod'])
    for t in mt['tervezett']:
        if t['kod'] in brief_kodok or t['kod'] in kesz_kodok:
            continue                         # a FELADATOK-sor nyer
        r = szoveg(t['kod'])
        f = mt['fazis'].get(t['kod'], '')
        fazis = '1' if f.startswith('1.') else '2' if f.startswith('2.') else \
            'folyamat' if f else None
        kartyak.append({
            'kulcs': t['kod'], 'szam': None, 'kod': t['kod'],
            'cim': _clip(t['cel'], 90) or t['kod'], 'fazis': fazis,
            'allapot': 'plan', 'brief_allapot': 'tervezett',
            'most': 'még nincs felvéve; a sorszámot a /befogad adja (MUNKATERV 4. szakasz)',
            'fugg': t['fugg'] or '—', 'tervezett': True,
            'reszletes': r['reszletes'] if r else '',
            'roviden': r['roviden'] if r else '',
            'leiras_forras': r['forras'] if r else None,
            'leiras_hiany': r is None,
        })

    # --- csempek
    szamlalo = {}
    for k in kartyak:
        szamlalo[k['allapot']] = szamlalo.get(k['allapot'], 0) + 1
    nyitott_dt = [d for d in dt_sorok if d['allapot'] == 'nyitott']
    csempek = [{'kulcs': k, 'cimke': c, 'db': szamlalo.get(k, 0)} for k, c in CSEMPE_CIMKE]
    csempek.append({'kulcs': 'dt', 'cimke': 'Nyitott döntés', 'db': len(nyitott_dt)})

    # --- most induló sor: a `feladatok.py jeloltek` kimenete
    jel = F.jeloltek(briefek, main_all)
    csomag_tagok = set(F.csomag(briefek, main_all, legfeljebb=10 ** 6))
    sor = []
    for n in sorted((n for n, ok in jel.items() if ok is None),
                    key=lambda n: (not F.felbemaradt(by_szam[n]), n)):
        b = by_szam[n]
        sor.append({'szam': n, 'kod': b.fej.get('kod'), 'cim': b.fej['cim'].strip('"'),
                    'most': _kov(b), 'felbemaradt': F.felbemaradt(b),
                    'parhuzamos': n in csomag_tagok})

    # --- kartya-index a hullamokhoz es a terkephez
    by_kulcs = {k['kulcs']: k for k in kartyak}
    by_kartya_szam = {k['szam']: k for k in kartyak if k['szam'] is not None}

    def elem_allapot(szoveg_):
        m = re.match(r'\s*#(\d+)', szoveg_)
        if m:
            n = int(m.group(1))
            if n in by_kartya_szam:
                return by_kartya_szam[n]['allapot']
            return 'kesz' if n in kesz_szamok else None
        m = re.match(r'[A-Z][A-Z0-9_]+', szoveg_)
        if m:
            kod = m.group(0)
            if kod in by_kulcs:
                return by_kulcs[kod]['allapot']
            if kod in kesz_kodok:
                return 'kesz'
        return 'kesz' if 'kész' in szoveg_ and 'részben' not in szoveg_ else None

    hullamok = []
    for h in mt['hullamok']:
        elemek = []
        for resz in h['elemek_szoveg'].split(';'):
            for e in resz.split('→'):
                e = e.strip()
                if e:
                    elemek.append({'szoveg': e, 'allapot': elem_allapot(e)})
        hullamok.append({'nev': h['nev'], 'elemek': elemek, 'kapu': h['kapu']})

    # --- fuggesi terkep (Mermaid)
    csomopont = {}
    for k in kartyak:
        if k['szam'] is not None:
            csomopont[('szam', k['szam'])] = ('T%d' % k['szam'], k)
        else:
            csomopont[('kod', k['kulcs'])] = ('P_' + k['kulcs'], k)
    dt_csomopont = {}
    for d in dt_sorok:
        if d['allapot'] in ('nyitott', 'alkalmazasra_var', 'ellenorizendo'):
            dt_csomopont[d['id']] = 'D_' + re.sub(r'\W', '_', d['id'])
    elek = set()

    def cel_csomopont(token):
        szam, dt, kod = token
        if szam:
            return csomopont.get(('szam', int(szam)))
        if kod:
            return csomopont.get(('kod', kod)) or next(
                (v for (t, _), v in csomopont.items() if v[1]['kod'] == kod), None)
        return None

    for a, deps in fugg.items():
        if ('szam', a) not in csomopont:
            continue
        for b_ in deps:
            if ('szam', b_) in csomopont:
                elek.add((csomopont[('szam', a)][0], csomopont[('szam', b_)][0]))
    for k in kartyak:
        if not k['tervezett']:
            continue
        src = csomopont[('kod', k['kulcs'])][0]
        for m in ID_TOKEN.finditer(k['fugg']):
            if m.group(2):
                if m.group(2) in dt_csomopont:
                    elek.add((src, dt_csomopont[m.group(2)]))
                continue
            c = cel_csomopont((m.group(1), None, m.group(3)))
            if c and c[0] != src:
                elek.add((src, c[0]))
    for d in dt_sorok:
        if d['id'] not in dt_csomopont:
            continue
        for m in ID_TOKEN.finditer(d.get('feladat', '')):
            if m.group(2):
                continue
            c = cel_csomopont((m.group(1), None, m.group(3)))
            if c:
                elek.add((c[0], dt_csomopont[d['id']]))

    def felirat(k):
        if k['szam'] is not None:
            return ('#%d %s' % (k['szam'], k['kod'] or _clip(k['cim'], 24))).replace('"', "'")
        return k['kulcs']

    sorok = ['flowchart LR']
    for kulcs, szin, extra in (
            ('stop', '#d93025,stroke:#8c1d18,color:#ffffff', ',stroke-width:2px'),
            ('run', '#1e8e3e,stroke:#0d5226,color:#ffffff', ',stroke-width:2px'),
            ('ready', '#1a73e8,stroke:#0b3d91,color:#ffffff', ',stroke-width:2px'),
            ('wait', '#f9ab00,stroke:#a86f00,color:#2b1d00', ',stroke-width:2px'),
            ('plan', '#8e44ad,stroke:#5b2470,color:#ffffff', ',stroke-width:2px,stroke-dasharray:6 3'),
            ('idle', '#80868b,stroke:#4a4f54,color:#ffffff', ''),
            ('dt', '#ff6d00,stroke:#a34500,color:#ffffff', ',stroke-width:2px')):
        sorok.append('  classDef %s fill:%s%s' % (kulcs, szin, extra))
    sorok.append('')
    hasznalt_cs = set(x for e in elek for x in e)
    for (_, _), (azon, k) in sorted(csomopont.items(), key=lambda x: x[1][0]):
        sorok.append('  %s["%s"]:::%s' % (azon, felirat(k), k['allapot']))
    for did in sorted(dt_csomopont):
        if dt_csomopont[did] in hasznalt_cs:
            sorok.append('  %s{{"%s"}}:::dt' % (dt_csomopont[did], did))
    sorok.append('')
    for a, b_ in sorted(elek):
        sorok.append('  %s --> %s' % (a, b_))
    terkep = '\n'.join(sorok)

    # --- dontesek
    def dt_kimenet(d):
        return {'id': d['id'], 'feladat': d.get('feladat', ''),
                'kerdes': d.get('kerdes', ''),
                'allapot': d['allapot'],
                'jelek': d['jelek'], 'sor': d['sor'],
                **({'oszlopszam': d['oszlopszam'], 'fejlec_oszlopszam': d['fejlec_oszlopszam']}
                   if 'oszlopszam' in d else {})}

    dt_idk = set(d['id'] for d in dt_sorok)
    javasolt = [{'id': d['id'], 'kerdes': d['kerdes'], 'irany': d['irany'],
                 'feladat': d['feladat']}
                for d in mt['dt'] if d['id'] not in dt_idk]
    dontesek = {
        'nyitott': [dt_kimenet(d) for d in dt_sorok if d['allapot'] == 'nyitott'],
        'alkalmazasra_var': [dt_kimenet(d) for d in dt_sorok
                             if d['allapot'] == 'alkalmazasra_var'],
        'javasolt': javasolt,
        'ellenorizendo': [dt_kimenet(d) for d in dt_sorok if d['allapot'] == 'ellenorizendo'],
        'kesz_db': sum(1 for d in dt_sorok if d['allapot'] == 'kesz'),
    }

    return {
        'meta': {
            'forrasok': ['*_BRIEF.md', 'MUNKATERV.md', 'DONTESEK.md', KARTYAK_TSV],
            'belyeg': belyeg(gyoker),
            'generator': 'eszkozok/feladatterkep.py',
        },
        'cimkek': {'allapot': [list(x) for x in ALLAPOT_CIMKE],
                   'fazis': [list(x) for x in FAZIS_CIMKE]},
        'csempek': csempek,
        'sor': sor,
        'hullamok': hullamok,
        'kartyak': kartyak,
        'kartya_tabla': {
            'felhasznalatlan': sorted(set(kartya_szoveg) - hasznalt),
            'leiras_nelkul': [k['kulcs'] for k in kartyak if k['leiras_hiany']],
        },
        'terkep': terkep,
        'dontesek': dontesek,
    }


def html_szoveg(adat):
    raise NotImplementedError('FT.2')


def json_szoveg(adat):
    return json.dumps(adat, ensure_ascii=False, indent=1) + '\n'


def ir(utvonal, szoveg):
    with open(utvonal, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--gyoker', default=REPO)
    ap.add_argument('--kimenet', help='a kimeneti konyvtar (alapertelmezett: a repo gyokere)')
    ap.add_argument('--csak-json', action='store_true')
    arg = ap.parse_args(argv)
    kimenet = arg.kimenet or arg.gyoker
    os.makedirs(kimenet, exist_ok=True)
    adat = epit(arg.gyoker)
    ir(os.path.join(kimenet, JSON_NEV), json_szoveg(adat))
    print('%s: %d kártya, %d nyitott döntés' % (
        os.path.join(kimenet, JSON_NEV), len(adat['kartyak']), len(adat['dontesek']['nyitott'])))
    if not arg.csak_json:
        ir(os.path.join(kimenet, HTML_NEV), html_szoveg(adat))
        print(os.path.join(kimenet, HTML_NEV))
    return 0


if __name__ == '__main__':
    sys.exit(main())
