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


HTML_SABLON = r'''<!doctype html>
<html lang="hu" data-tema="dark">
<script>try{var t=localStorage.getItem("pardes-tema");if(t)document.documentElement.setAttribute("data-tema",t)}catch(e){}</script>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- GENERÁLT: eszkozok/feladatterkep.py — kézzel ne szerkeszd -->
<title>PaRDeS feladattérkép</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Elrendezés: munkanapló-lap — fent az állapot, alatta a sorrend, a hullámok, az állapot szerinti oszlopok, a függési térkép és a döntések */
:root{
  --bg:#f5f6f8; --surface:#ffffff; --ink:#1b2333; --muted:#5d6678; --rule:#dde1e8;
  --accent:#27508f; --accent-soft:#e3ebf7;
  --stop:#b3261e; --stop-soft:#fcdcd8;
  --run:#1f7a4d; --run-soft:#d2f0de;
  --ready:#27508f; --ready-soft:#d6e4fb;
  --wait:#8a6a12; --wait-soft:#fdecc0;
  --plan:#6b4fa0; --plan-soft:#ead9f5;
  --idle:#6c7383; --idle-soft:#eceef2;
  --stop-solid:#d93025; --run-solid:#1e8e3e; --ready-solid:#1a73e8; --wait-solid:#f9ab00; --plan-solid:#8e44ad; --idle-solid:#80868b; --dt:#c25100; --dt-soft:#ffe8d6;
  --f-display:"Literata", Georgia, serif;
  --f-body:"IBM Plex Sans", system-ui, sans-serif;
  --f-mono:"IBM Plex Mono", ui-monospace, Consolas, monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-tema="light"]){
  --bg:#12161f; --surface:#1a202c; --ink:#e4e8f0; --muted:#9aa3b5; --rule:#2c3445;
  --accent:#8fb3ec; --accent-soft:#1f2c44;
  --stop:#f28b82; --stop-soft:#3a1f1f; --run:#7fd1a4; --run-soft:#163126;
  --ready:#8fb3ec; --ready-soft:#1f2c44; --wait:#e2c06a; --wait-soft:#3a3018;
  --plan:#c3a8f0; --plan-soft:#2c2340; --idle:#a1a8b8; --idle-soft:#252b38; --stop-solid:#c5221f; --run-solid:#188038; --ready-solid:#1967d2; --wait-solid:#e8a000; --plan-solid:#7b3a98; --idle-solid:#6b7177; --dt:#ff9e4a; --dt-soft:#3d2614; color-scheme:dark}}
:root[data-tema="dark"]{
  --bg:#12161f; --surface:#1a202c; --ink:#e4e8f0; --muted:#9aa3b5; --rule:#2c3445;
  --accent:#8fb3ec; --accent-soft:#1f2c44;
  --stop:#f28b82; --stop-soft:#3a1f1f; --run:#7fd1a4; --run-soft:#163126;
  --ready:#8fb3ec; --ready-soft:#1f2c44; --wait:#e2c06a; --wait-soft:#3a3018;
  --plan:#c3a8f0; --plan-soft:#2c2340; --idle:#a1a8b8; --idle-soft:#252b38; --stop-solid:#c5221f; --run-solid:#188038; --ready-solid:#1967d2; --wait-solid:#e8a000; --plan-solid:#7b3a98; --idle-solid:#6b7177; --dt:#ff9e4a; --dt-soft:#3d2614; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--f-body);margin:0}
.wrap{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:28px 64px;display:grid;gap:40px}
h1,h2{font-family:var(--f-display);font-weight:650;text-wrap:balance;margin:0}
h1{font-size:clamp(26px,4vw,36px);line-height:1.15}
h2{font-size:22px}
.eyebrow{font:500 12px/1 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.lede{color:var(--muted);max-width:68ch;margin:8px 0 0}
section{display:grid;gap:14px;min-width:0}
.sechead{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px}
.sechead p{margin:0;color:var(--muted);font-size:13.5px;max-width:70ch}
.mono{font-family:var(--f-mono);font-size:.92em}

/* összesítő */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.stat{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:12px 14px;display:grid;gap:2px}
.stat b{font:600 26px/1.1 var(--f-display);font-variant-numeric:tabular-nums}
.stat span{font-size:12.5px;color:var(--muted)}
.stat.stop{background:var(--stop-soft);border-color:var(--stop)} .stat.run{background:var(--run-soft);border-color:var(--run)} .stat.ready{background:var(--ready-soft);border-color:var(--ready)}
.stat.plan{background:var(--plan-soft);border-color:var(--plan)} .stat.wait{background:var(--wait-soft);border-color:var(--wait)} .stat.dt{background:var(--dt-soft);border-color:var(--dt)} .stat.dt b{color:var(--dt)}
.stat.stop b{color:var(--stop)} .stat.run b{color:var(--run)} .stat.ready b{color:var(--ready)}
.stat.plan b{color:var(--plan)} .stat.wait b{color:var(--wait)}

/* sorrend */
.seq{display:flex;flex-wrap:wrap;gap:8px;align-items:stretch}
.step{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:10px 12px;display:grid;gap:4px;flex:1 1 180px;min-width:0}
.step .n{font:600 11px var(--f-mono);color:#fff;background:var(--accent);justify-self:start;padding:2px 7px;border-radius:999px}
.step{border-top:3px solid var(--plan-solid)}
.step strong{font-weight:600}
.step small{color:var(--muted);font-size:12.5px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.step.par{border-style:dashed}
.arrow{align-self:center;color:var(--muted);font-family:var(--f-mono)}

/* hullámok */
.waves{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}
.wave{background:var(--surface);border:1px solid var(--rule);border-top:5px solid var(--accent);border-radius:8px;padding:14px;display:grid;gap:8px;align-content:start}
.wave h3{margin:0;font:600 15px var(--f-body)}
.wave .gate{font-size:12.5px;color:var(--muted);border-top:1px dashed var(--rule);padding-top:8px}
.wave .gate::before{content:"⛔ ";}
.chips{display:flex;flex-wrap:wrap;gap:6px}

/* chip */
.chip{display:inline-flex;align-items:center;gap:6px;font:500 12px/1.2 var(--f-mono);padding:4px 8px;border-radius:999px;border:1px solid transparent;white-space:nowrap}
.chip i{font-style:normal;opacity:.75}
.s-stop{background:var(--stop-soft);color:var(--stop);border-color:color-mix(in srgb,var(--stop) 30%,transparent)}
.s-run{background:var(--run-soft);color:var(--run);border-color:color-mix(in srgb,var(--run) 30%,transparent)}
.s-ready{background:var(--ready-soft);color:var(--ready);border-color:color-mix(in srgb,var(--ready) 30%,transparent)}
.s-wait{background:var(--wait-soft);color:var(--wait);border-color:color-mix(in srgb,var(--wait) 30%,transparent)}
.s-plan{background:var(--plan-soft);color:var(--plan);border-color:color-mix(in srgb,var(--plan) 30%,transparent);border-style:dashed}
.s-idle{background:var(--idle-soft);color:var(--idle);border-color:color-mix(in srgb,var(--idle) 25%,transparent)}
.s-done{background:transparent;color:var(--run);border-color:color-mix(in srgb,var(--run) 40%,transparent)}
.s-nincs{background:transparent;color:var(--muted);border-color:var(--rule);border-style:dotted}

/* szűrő */
.filters{display:flex;flex-wrap:wrap;gap:6px}
.filters button{font:500 13px var(--f-body);background:var(--surface);color:var(--ink);border:1px solid var(--rule);border-radius:999px;padding:6px 12px;cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.filters button:focus-visible,.legend button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* oszlopok */
.board{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;align-items:start}
.col{display:grid;gap:8px;min-width:0}
.colhead{display:flex;align-items:center;justify-content:space-between;font:600 13px var(--f-body);padding:6px 10px;border-radius:6px;color:#fff;background:var(--idle)}
.colhead .count{color:inherit!important;opacity:.85}
.colhead.h-stop{background:var(--stop-solid)} .colhead.h-run{background:var(--run-solid)} .colhead.h-ready{background:var(--ready-solid)} .colhead.h-wait{background:var(--wait-solid);color:#2b1d00} .colhead.h-plan{background:var(--plan-solid)} .colhead.h-idle{background:var(--idle-solid)}
.colhead .count{font:500 12px var(--f-mono);color:var(--muted)}
.card{background:var(--surface);border:1px solid var(--rule);border-left:6px solid var(--idle);border-radius:6px;padding:10px 12px;display:grid;gap:5px;min-width:0}
.card.k-stop{border-left-color:var(--stop);background:var(--stop-soft)} .card.k-run{border-left-color:var(--run);background:var(--run-soft)} .card.k-ready{border-left-color:var(--ready);background:var(--ready-soft)}
.card.k-wait{border-left-color:var(--wait);background:var(--wait-soft)} .card.k-plan{border-left-color:var(--plan);background:var(--plan-soft);border-style:dashed;border-left-style:solid} .card.k-idle{border-left-color:var(--idle);background:var(--idle-soft)}
.card .top{display:flex;gap:8px;align-items:baseline;justify-content:space-between}
.card .id{font:500 12px var(--f-mono);color:var(--muted);white-space:nowrap}
.card .name{font-weight:600;font-size:14px;line-height:1.3}
.card .kod{font:500 11.5px var(--f-mono);color:var(--muted);overflow-wrap:anywhere}
.card .next{font-size:12.5px;color:var(--muted);line-height:1.4}
.card .deps{font:12px var(--f-mono);color:var(--muted);overflow-wrap:anywhere}
.card .detail{font-size:13px;line-height:1.45;color:var(--ink)}
.card .detail.nincs{color:var(--muted);font-style:italic}
.card .next b{font-weight:600;color:var(--ink)}
.card .sum{font-size:13px;line-height:1.4;font-weight:600;color:var(--ink);border-top:1px dashed color-mix(in srgb,var(--ink) 25%,transparent);padding-top:6px;margin-top:2px}

/* térkép */
.mapbox{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:12px;overflow-x:auto}
.legend{display:flex;flex-wrap:wrap;gap:6px}
.wrap{zoom:1.1}

/* döntések */
.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;align-items:start}
.dlist{background:var(--surface);border:1px solid var(--rule);border-radius:8px;overflow:hidden}
.dlist h3{margin:0;padding:10px 14px;font:600 14px var(--f-body);border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;gap:8px}
.dlist h3 span{font:500 12px var(--f-mono);color:var(--muted)}
.drow{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;padding:10px 14px;border-bottom:1px solid var(--rule)}
.drow:last-child{border-bottom:0}
.drow .did{font:500 12.5px var(--f-mono);white-space:nowrap}
.drow .dq{font-size:13.5px;line-height:1.4}
.drow .dfor{grid-column:2;font:12px var(--f-mono);color:var(--muted)}
.drow .dell{grid-column:2;font:12px var(--f-mono);color:var(--dt)}
.note{font-size:13px;color:var(--muted);background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:12px 14px;max-width:none}
.note strong{color:var(--ink)}
footer{font:12px var(--f-mono);color:var(--muted)}
header{position:relative}
.tema{position:absolute;top:0;right:0;font:500 13px var(--f-body);background:var(--surface);color:var(--ink);border:1px solid var(--rule);border-radius:999px;padding:6px 12px;cursor:pointer}
.tema:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.eyebrow{padding-right:110px}
@media (prefers-reduced-motion:no-preference){.card,.step{transition:border-color .15s}}
</style>
</head>
<body>

<div class="wrap">

<header>
  <button type="button" id="tema" class="tema" aria-label="Téma váltása"></button>
  <div class="eyebrow" id="eyebrow"></div>
  <h1>PaRDeS feladattérkép</h1>
  <p class="lede">A <span class="mono">FELADATOK.md</span>, a <span class="mono">DONTESEK.md</span> és a <span class="mono">MUNKATERV.md</span> egy lapon, a források alapján generálva. A szaggatott keretes tételek tervezettek: még nincsenek a FELADATOK-ban, sorszámot a <span class="mono">/befogad</span> ad nekik.</p>
</header>

<section aria-labelledby="h-stat">
  <h2 id="h-stat" class="eyebrow" style="font-family:var(--f-mono);font-size:12px">Összkép</h2>
  <div class="stats" id="stats"></div>
</section>

<section aria-labelledby="h-seq">
  <div class="sechead">
    <h2 id="h-seq">Most induló sor</h2>
    <p>Az 1. fázis indítható feladatai: a <span class="mono">feladatok.py jeloltek</span> kimenete, a <span class="mono">/kovetkezo</span> választási sorrendjében (a felbemaradt előre, utána a kisebb sorszám). Szaggatott keret: egy csomagban párhuzamosan futtatható.</p>
  </div>
  <div class="seq" id="seq"></div>
</section>

<section aria-labelledby="h-waves">
  <div class="sechead">
    <h2 id="h-waves">Munkaterv hullámai</h2>
    <p>A MUNKATERV 5. szakasza; a ⛔ a hullám végi megállás. A chip színe a feladat mai állapota.</p>
  </div>
  <div class="waves" id="waves"></div>
</section>

<section aria-labelledby="h-board">
  <div class="sechead">
    <h2 id="h-board">Feladatok állapot szerint</h2>
    <div class="filters" role="group" aria-label="Fázis szűrő" id="filters"></div>
  </div>
  <div class="board" id="board"></div>
</section>

<section aria-labelledby="h-map">
  <div class="sechead">
    <h2 id="h-map">Függési térkép</h2>
    <p>A nyíl a függőtől a feltételig mutat. Kész feladatok nem szerepelnek; a döntések (DT) hatszögek. Forrás: <span class="mono">feladatok.py fuggesek</span> + a MUNKATERV függései + a DONTESEK „Feladat” oszlopa.</p>
  </div>
  <div class="legend" id="legend"></div>
  <div class="mapbox">
<pre class="terkep-forras">
@@TERKEP@@
</pre>
  </div>
</section>

<section aria-labelledby="h-dt">
  <div class="sechead">
    <h2 id="h-dt">Döntések</h2>
    <p>A <span class="mono">DONTESEK.md</span> nem alkalmazott tételei, és a MUNKATERV által javasolt, még fel nem vett DT-k. Az „ellenőrizendő” sor oszlopszáma eltér a táblafejlécétől, ezért az állapotát a generátor nem találgatja.</p>
  </div>
  <div class="dgrid" id="dgrid"></div>
</section>

<footer id="lablec"></footer>
</div>

<script>
const D = @@ADAT@@;
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const clip = (s,n) => { s = String(s).split("**").join("").split(String.fromCharCode(96)).join(""); s = s.split(" ").filter(Boolean).join(" "); if(s.length<=n) return s; const v=s.slice(0,n); const i=v.lastIndexOf(" "); return (i>n*0.6?v.slice(0,i):v).replace(/[ ,;:—-]+$/,"")+"…"; };
const ST = {}; D.cimkek.allapot.forEach(([k,l])=>{ST[k]={l:l,c:"s-"+k};});
ST.kesz = {l:"Kész",c:"s-done"}; ST.nincs = {l:"nincs a térképen",c:"s-nincs"};
const PH = {}; D.cimkek.fazis.forEach(([k,l])=>{PH[k]=l;});
const chip = (t,s) => { const k = ST[s]?s:"nincs"; return `<span class="chip ${ST[k].c}">${esc(t)}${s==="kesz"?" ✓":""}</span>`; };
const B = D.meta.belyeg;
$("#eyebrow").textContent = "Bible-Study · források állapota " + (B.datum||"?") + " · commit " + (B.commit||"?");
$("#lablec").textContent = "Forrás: a *_BRIEF.md fejlécek (feladatok.py) · MUNKATERV.md · DONTESEK.md · eszkozok/feladatterkep_kartyak.tsv · bélyeg: " + (B.datum||"?") + " " + (B.commit||"?") + " · generálta: " + D.meta.generator + " — kézzel ne szerkeszd.";

$("#stats").innerHTML = D.csempek.map(c=>`<div class="stat ${c.kulcs}"><b>${c.db}</b><span>${esc(c.cimke)}</span></div>`).join("");

$("#seq").innerHTML = D.sor.length ? D.sor.map((s,i)=>
  (i?`<span class="arrow" aria-hidden="true">${s.parhuzamos&&D.sor[i-1].parhuzamos?"∥":"→"}</span>`:"")+
  `<div class="step${s.parhuzamos?" par":""}"><span class="n">#${s.szam}${s.felbemaradt?" · folytatás":""}</span><strong class="mono">${esc(s.kod||s.cim)}</strong><small title="${esc(s.most)}">${esc(clip(s.most,160))}</small></div>`).join("")
  : '<p class="note">Nincs indítható 1. fázisú feladat.</p>';

const WC=["var(--run-solid)","var(--ready-solid)","var(--plan-solid)","var(--wait-solid)","var(--idle-solid)"];
$("#waves").innerHTML = D.hullamok.map((w,i)=>`<div class="wave" style="border-top-color:${WC[i%WC.length]}"><h3>${esc(w.nev)}</h3><div class="chips">${w.elemek.map(e=>chip(e.szoveg,e.allapot)).join("")}</div><div class="gate">${esc(w.kapu)}</div></div>`).join("");

$("#legend").innerHTML = D.cimkek.allapot.map(([k,l])=>chip(l,k)).join("");

let phase = "all";
try { phase = localStorage.getItem("pardes-fazis") || "all"; } catch(e) {}
const fazisok = ["all"].concat(D.cimkek.fazis.map(f=>f[0]).filter(f=>D.kartyak.some(k=>k.fazis===f)));
if (fazisok.indexOf(phase)<0) phase="all";
const F = fazisok.map(v=>[v, v==="all"?"Mind":PH[v]]);
function renderFilters(){
  $("#filters").innerHTML = F.map(([v,l])=>`<button type="button" id="f-${v}" data-v="${v}" aria-pressed="${phase===v}">${esc(l)}</button>`).join("");
  $("#filters").querySelectorAll("button").forEach(b=>b.onclick=()=>{phase=b.dataset.v;try{localStorage.setItem("pardes-fazis",phase)}catch(e){};renderFilters();renderBoard();});
}
function renderBoard(){
  const order=["stop","run","ready","plan","wait","idle"];
  const list = D.kartyak.filter(t=>phase==="all"||t.fazis===phase);
  $("#board").innerHTML = order.map(s=>{
    const items=list.filter(t=>t.allapot===s); if(!items.length) return "";
    return `<div class="col"><div class="colhead h-${s}"><span>${ST[s].l}</span><span class="count">${items.length}</span></div>`+
      items.map(t=>`<article class="card k-${s}"><div class="top"><span class="name">${esc(t.cim)}</span><span class="id">${t.szam!==null?"#"+t.szam:"tervezett"}</span></div>
        <span class="kod">${esc(t.kulcs)} · ${esc(t.fazis?PH[t.fazis]:"fázis ?")}</span>
        ${t.leiras_hiany?`<span class="detail nincs">nincs leírás</span>`:`<span class="detail">${esc(t.reszletes)}</span>`}
        <span class="next" title="${esc(t.most)}"><b>Most:</b> ${esc(clip(t.most,220))}</span>
        <span class="deps">függ: ${esc(t.fugg)}</span>${t.roviden?`<span class="sum">Röviden: ${esc(t.roviden)}</span>`:""}</article>`).join("")+`</div>`;
  }).join("");
}
renderFilters(); renderBoard();
(function(){var b=$("#tema"),r=document.documentElement;
 function lbl(){b.textContent=r.getAttribute("data-tema")==="dark"?"☀ Világos":"☾ Sötét";}
 lbl(); b.onclick=function(){var n=r.getAttribute("data-tema")==="dark"?"light":"dark";
  r.setAttribute("data-tema",n); try{localStorage.setItem("pardes-tema",n)}catch(e){}
  lbl(); if(window.rajzolTerkep) window.rajzolTerkep();};})();

const DG = D.dontesek;
const dsor = (d,mod) => `<div class="drow"><span class="did">${esc(d.id)}</span><span class="dq">${esc(clip(d.kerdes,230))}</span><span class="dfor">${mod==="javasolt"?"javasolt irány: "+esc(clip(d.irany||"—",90))+" · → ":"→ "}${esc(clip(d.feladat||"—",90))}</span>${mod==="ell"?`<span class="dell">ellenőrizendő: ${d.oszlopszam} oszlop a fejléc ${d.fejlec_oszlopszam} oszlopa helyett — az állapotot nézd meg a DONTESEK.md ${d.sor}. sorában</span>`:""}</div>`;
const dlista = (cim,k,rows,mod) => `<div class="dlist"><h3>${chip(cim,k)}<span>${rows.length}</span></h3>${rows.length?rows.map(d=>dsor(d,mod)).join(""):'<div class="drow"><span class="dq">—</span></div>'}</div>`;
$("#dgrid").innerHTML = dlista("Nyitott","stop",DG.nyitott)
  + dlista("Eldöntve, alkalmazásra vár","run",DG.alkalmazasra_var)
  + dlista("Javasolt, még nincs felvéve","plan",DG.javasolt,"javasolt")
  + (DG.ellenorizendo.length?dlista("Ellenőrizendő sor","wait",DG.ellenorizendo,"ell"):"");
</script>

<script src="https://cdn.jsdelivr.net/npm/mermaid@11.16.1/dist/mermaid.min.js"></script>
<script>
/* Ugyanaz a Mermaid-beállítás, amellyel a claude.ai artifact rajzol (base téma, a lap háttere); témaváltáskor újrarajzol */
(function(){
var pre=document.querySelector("pre.terkep-forras"); if(!pre||typeof mermaid==="undefined") return;
var src=pre.textContent, hely=document.createElement("div"); pre.parentNode.insertBefore(hely,pre); pre.style.display="none";
var n=0;
window.rajzolTerkep=function(){
 var dark=document.documentElement.getAttribute("data-tema")==="dark";
 var pal=dark?{surface:"#262b34",text:"#f2f3f5",line:"#a8adb8",border:"#9aa4b8"}:{surface:"#f4efe4",text:"#42392e",line:"#8a7f6d",border:"#7a6c52"};
 var bg=getComputedStyle(document.body).backgroundColor;
 mermaid.initialize({startOnLoad:false,securityLevel:"strict",theme:"base",flowchart:{useMaxWidth:false},
  themeVariables:{background:bg,mainBkg:pal.surface,primaryColor:pal.surface,primaryTextColor:pal.text,lineColor:pal.line,
   primaryBorderColor:pal.border,nodeBorder:pal.border,edgeLabelBackground:bg,darkMode:dark,fontSize:"10px",
   fontFamily:getComputedStyle(document.body).fontFamily},
  themeCSS:".node rect, .node circle, .node polygon, .node path { stroke-width: 2px; }"});
 mermaid.render("terkep-"+(n++),src).then(function(r){hely.innerHTML=r.svg;},function(){pre.style.display="";});
};
window.rajzolTerkep();
})();
</script>
</body>
</html>
'''


def html_szoveg(adat):
    """Az onallo lap: a JSON beagyazva (a `<` jel \\u003c-vel, hogy a script ne zarodjon le)."""
    adat_js = json.dumps(adat, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    terkep = (adat['terkep'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    return (HTML_SABLON.replace('@@ADAT@@', adat_js, 1)
            .replace('@@TERKEP@@', terkep, 1))


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
