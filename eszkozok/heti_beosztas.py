#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
heti_beosztas.py -- a heti beosztás oldalának generátora (F222).

A heti beosztás TERV, nem leltár. A forrása a három kézi tábla:
  - adat/heti_terv.tsv   a hét sorai sávonként: sorrend, cél a hét végére, modell, becsült keret (SEMA 2.60);
  - adat/heti_keret.tsv  az elhasznált keret, kézzel megadva (SEMA 2.61);
  - adat/otlettar.tsv    az ötlettár; a `felmerendo` tételek a „Felmérés / ötlet” sávban látszanak (SEMA 2.62).
A terv sorainak valós állapotát a brief-fejlécekből és a GitHub PR-állapotokból számolja (a heti áttekintő,
`heti_attekinto.py`, beolvasó függvényeivel, csak olvasva); ha van, a valós állapot felülírja a kézi jelölést.

Az oldal: fent a keret-hét, a „javaslat” / „jóváhagyott” jelzés és a felhasználó teendői; utána sávonként a
terv NYITOTT sorai (cél, modell, becsült keret, valós állapot); a keret (tervezett és elhasznált); a végén a
„Visszanézés”. **Lezárt tétel csak a visszanézésben áll, máshol nem.**

A kimenet generált nézet: a `--kimenet` a repón kívülre mutasson (CLAUDE.md), a szkript a repón belüli útvonalat
elutasítja. Ha a táblák hibásak, a szkript hibát ír és nem készít oldalt.

Használat:
    python eszkozok/heti_beosztas.py --kimenet <út.html>
        [--gyoker <repó>] [--ma ÉÉÉÉ-HH-NN] [--het ÉÉÉÉ-HH-NN] [--pr-json <fájl>]
    python eszkozok/heti_beosztas.py --ellenoriz        (csak a három tábla ellenőrzése)

`--ma`: a nap, amelynek végén az oldal készül (alapérték: most, UTC); a keret-hét szombat 14:00 UTC-től tart.
`--het`: a megjelenített hét kezdete (szombat); alapértelmezés: a `--ma` szerinti hét.
`--pr-json`: a `gh` helyett a fájlból olvassa a PR-listát (mint a heti áttekintőnél).

Kilépési kód: 0 = rendben, 2 = hiba.
"""
import argparse
import os
import re
import sys
from collections import OrderedDict
from datetime import date, datetime, time, timedelta, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402
import heti_attekinto as H  # noqa: E402

REPO = F.REPO

# ---------------------------------------------------------------------------
# a táblák sémája (SEMA 2.60–2.62)
# ---------------------------------------------------------------------------

TERV_FEJ = ['het', 'sav', 'sorrend', 'tetel', 'cel_a_het_vegere', 'modell', 'becsult_keret_szazalek',
            'allapot_kezi', 'jovahagyva', 'megjegyzes']
KERET_FEJ = ['het', 'sav', 'elhasznalt_szazalek', 'ts', 'forras']
OTLET_FEJ = ['id', 'sav', 'cim', 'forras', 'allapot', 'megjegyzes']

# a terv sávjai az oldal sorrendjében: a brief `sav` értékei + a két keretsor
SAV_SORREND = ('CONTENT', 'SYSTEMS', 'SERVER', 'USER', 'BUSINESS', 'FELMERES', 'TARTALEK')
SAV_CIMKE = {
    'CONTENT': 'Tartalomkészítés',
    'SYSTEMS': 'Fejlesztői infrastruktúra',
    'SERVER': 'Olvasó',
    'USER': 'Felhasználók, előfizetés, jogok',
    'BUSINESS': 'Üzleti oldal',
    'FELMERES': 'Felmérés / ötlet',
    'TARTALEK': 'Tartalék',
}
OTLET_SAVOK = ('SYSTEMS', 'CONTENT', 'SERVER', 'USER', 'BUSINESS')
KEZI_ALLAPOTOK = ('kesz', 'csuszik', 'blokkolt', 'elhagyva')
KEZI_CIMKE = {'kesz': 'kész', 'csuszik': 'csúszik', 'blokkolt': 'blokkolt', 'elhagyva': 'elhagyva'}
JOVAHAGYVA = ('igen', 'javaslat')
OTLET_ALLAPOTOK = ('otlet', 'felmerendo', 'elvetve', 'briefbe_ment')
OTLET_CIMKE = {'otlet': 'ötlet', 'felmerendo': 'felmérendő', 'elvetve': 'elvetve', 'briefbe_ment': 'feladatba ment'}
HIVATKOZOS_OTLET = ('elvetve', 'briefbe_ment')

TETEL_BRIEF = re.compile(r'^(?:F|#)(\d+)$')
TETEL_PR = re.compile(r'^PR#(\d+)$')
HET_MINTA = re.compile(r'^\d{4}-\d{2}-\d{2}$')
OTLET_ID = re.compile(r'^OT\d{3}$')
TS_MINTA = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$')
TE_ELOTAG = re.compile(r'^\s*Te\s*:\s*')
KERET_HATAR = time(14, 0)           # a heti keret szombaton 14:00 UTC-kor nullázódik
SZOMBAT = 5


# ---------------------------------------------------------------------------
# a keret-hét
# ---------------------------------------------------------------------------

def het_kezdete(dt):
    """A keret-hét kezdő napja (szombat) az `dt` (UTC, naív) időponthoz: az utolsó szombat 14:00 UTC."""
    nap = dt.date()
    kezdet = nap - timedelta(days=(nap.weekday() - SZOMBAT) % 7)
    if kezdet == nap and dt.time() < KERET_HATAR:
        kezdet -= timedelta(days=7)
    return kezdet


def het_szoveg(kezdet):
    veg = kezdet + timedelta(days=7)
    return '%s 14:00 UTC – %s 14:00 UTC' % (H.datum_szoveg(kezdet), H.datum_szoveg(veg))


def datum_olvas(szoveg):
    try:
        return datetime.strptime(szoveg, '%Y-%m-%d').date()
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# beolvasás és ellenőrzés (TSV: split('\t'), a csv modul nem használható)
# ---------------------------------------------------------------------------

def tsv_olvas(ut, fejlec):
    """(sorok, hibak): a táblát dict-sorokká olvassa; a `_sor` a fájl sorszáma."""
    nev = os.path.basename(ut)
    try:
        with open(ut, encoding='utf-8', newline='') as f:
            szoveg = f.read()
    except OSError as e:
        return [], ['%s: nem olvasható (%s)' % (nev, e)]
    sorok_nyers = szoveg.replace('\r\n', '\n').split('\n')
    if sorok_nyers and sorok_nyers[-1] == '':
        sorok_nyers.pop()
    if not sorok_nyers:
        return [], ['%s: üres fájl (a fejlécsor hiányzik)' % nev]
    fej = sorok_nyers[0].lstrip('﻿').split('\t')
    if fej != fejlec:
        return [], ['%s: a fejlécsor eltér a SEMA-tól (kapott: %s; várt: %s)' % (nev, '|'.join(fej), '|'.join(fejlec))]
    sorok, hibak = [], []
    for i, sor in enumerate(sorok_nyers[1:], start=2):
        if not sor.strip():
            continue
        mezok = sor.split('\t')
        if len(mezok) != len(fejlec):
            hibak.append('%s:%d: %d mező %d helyett' % (nev, i, len(mezok), len(fejlec)))
            continue
        d = dict(zip(fejlec, mezok))
        d['_sor'] = i
        sorok.append(d)
    return sorok, hibak


def kezi_allapot(szoveg):
    """(kod, indok): az `allapot_kezi` mező: üres, vagy `kod` / `kod: indok`."""
    szoveg = (szoveg or '').strip()
    if not szoveg:
        return '', ''
    kod, _, indok = szoveg.partition(':')
    return kod.strip(), indok.strip()


def terv_ellenoriz(sorok):
    hibak = []
    kulcsok = set()
    osszeg = {}
    for s in sorok:
        h = 'heti_terv.tsv:%d' % s['_sor']
        het = datum_olvas(s['het']) if HET_MINTA.match(s['het']) else None
        if het is None or het.weekday() != SZOMBAT:
            hibak.append('%s: a `het` szombati ÉÉÉÉ-HH-NN dátum kell (kapott: %r)' % (h, s['het']))
        if s['sav'] not in SAV_SORREND:
            hibak.append('%s: ismeretlen `sav` (%s; kapott: %r)' % (h, ' | '.join(SAV_SORREND), s['sav']))
        if not s['sorrend'].isdigit():
            hibak.append('%s: a `sorrend` egész szám kell (kapott: %r)' % (h, s['sorrend']))
        kulcs = (s['het'], s['sav'], s['sorrend'])
        if kulcs in kulcsok:
            hibak.append('%s: ismétlődő kulcs (het, sav, sorrend): %s' % (h, ' | '.join(kulcs)))
        kulcsok.add(kulcs)
        if not s['tetel'].strip():
            hibak.append('%s: üres `tetel` (a „-” jelzi, ha nincs konkrét tétel)' % h)
        if not s['cel_a_het_vegere'].strip():
            hibak.append('%s: üres `cel_a_het_vegere`' % h)
        if not (s['becsult_keret_szazalek'].isdigit() and 0 <= int(s['becsult_keret_szazalek']) <= 100):
            hibak.append('%s: a `becsult_keret_szazalek` 0–100 közötti egész kell (kapott: %r)'
                         % (h, s['becsult_keret_szazalek']))
        else:
            osszeg[s['het']] = osszeg.get(s['het'], 0) + int(s['becsult_keret_szazalek'])
        kod, indok = kezi_allapot(s['allapot_kezi'])
        if kod and kod not in KEZI_ALLAPOTOK:
            hibak.append('%s: ismeretlen `allapot_kezi` (%s; kapott: %r)' % (h, ' | '.join(KEZI_ALLAPOTOK), kod))
        elif kod in ('csuszik', 'blokkolt', 'elhagyva') and not indok:
            hibak.append('%s: a `%s` állapothoz indok kell (`%s: <indok>`)' % (h, kod, kod))
        if s['jovahagyva'] not in JOVAHAGYVA:
            hibak.append('%s: ismeretlen `jovahagyva` (%s; kapott: %r)' % (h, ' | '.join(JOVAHAGYVA), s['jovahagyva']))
    for het, db in sorted(osszeg.items()):
        if db != 100:
            hibak.append('heti_terv.tsv: a %s hét becsült keretének összege %d, nem 100' % (het, db))
    return hibak


def keret_ellenoriz(sorok):
    hibak = []
    kulcsok = set()
    for s in sorok:
        h = 'heti_keret.tsv:%d' % s['_sor']
        het = datum_olvas(s['het']) if HET_MINTA.match(s['het']) else None
        if het is None or het.weekday() != SZOMBAT:
            hibak.append('%s: a `het` szombati ÉÉÉÉ-HH-NN dátum kell (kapott: %r)' % (h, s['het']))
        if s['sav'] not in SAV_SORREND:
            hibak.append('%s: ismeretlen `sav` (kapott: %r)' % (h, s['sav']))
        if (s['het'], s['sav']) in kulcsok:
            hibak.append('%s: ismétlődő kulcs (het, sav)' % h)
        kulcsok.add((s['het'], s['sav']))
        if not (s['elhasznalt_szazalek'].isdigit() and 0 <= int(s['elhasznalt_szazalek']) <= 100):
            hibak.append('%s: az `elhasznalt_szazalek` 0–100 közötti egész kell (kapott: %r)'
                         % (h, s['elhasznalt_szazalek']))
        if not TS_MINTA.match(s['ts']):
            hibak.append('%s: a `ts` alakja ÉÉÉÉ-HH-NNTÓÓ:PP (kapott: %r)' % (h, s['ts']))
        if not s['forras'].strip():
            hibak.append('%s: üres `forras` (honnan jött az érték)' % h)
    return hibak


def otlet_allapot(szoveg):
    """(kod, hivatkozas) az ötlettár `allapot` mezőjéből: `kod` vagy `kod: hivatkozás`."""
    kod, _, hiv = (szoveg or '').partition(':')
    return kod.strip(), hiv.strip()


def otlet_ellenoriz(sorok):
    hibak = []
    idk = set()
    for s in sorok:
        h = 'otlettar.tsv:%d' % s['_sor']
        if not OTLET_ID.match(s['id']):
            hibak.append('%s: az `id` alakja OT<nnn> (kapott: %r)' % (h, s['id']))
        if s['id'] in idk:
            hibak.append('%s: ismétlődő `id`: %s' % (h, s['id']))
        idk.add(s['id'])
        if s['sav'] not in OTLET_SAVOK:
            hibak.append('%s: ismeretlen `sav` (%s; kapott: %r)' % (h, ' | '.join(OTLET_SAVOK), s['sav']))
        if not s['cim'].strip():
            hibak.append('%s: üres `cim`' % h)
        if not s['forras'].strip():
            hibak.append('%s: üres `forras` (ki, mikor, hol)' % h)
        kod, hiv = otlet_allapot(s['allapot'])
        if kod not in OTLET_ALLAPOTOK:
            hibak.append('%s: ismeretlen `allapot` (%s; kapott: %r)' % (h, ' | '.join(OTLET_ALLAPOTOK), kod))
        elif kod in HIVATKOZOS_OTLET and not hiv:
            hibak.append('%s: a `%s` állapothoz hivatkozás kell (`%s: <hivatkozás>`)' % (h, kod, kod))
        elif kod not in HIVATKOZOS_OTLET and hiv:
            hibak.append('%s: a `%s` állapotnak nincs hivatkozása (kapott: %r)' % (h, kod, hiv))
    return hibak


def tablak_olvas(gyoker):
    """(terv, keret, otlet, hibak): a három tábla beolvasva és ellenőrizve."""
    adat = os.path.join(gyoker, 'adat')
    terv, h1 = tsv_olvas(os.path.join(adat, 'heti_terv.tsv'), TERV_FEJ)
    keret, h2 = tsv_olvas(os.path.join(adat, 'heti_keret.tsv'), KERET_FEJ)
    otlet, h3 = tsv_olvas(os.path.join(adat, 'otlettar.tsv'), OTLET_FEJ)
    hibak = h1 + h2 + h3 + terv_ellenoriz(terv) + keret_ellenoriz(keret) + otlet_ellenoriz(otlet)
    return terv, keret, otlet, hibak


# ---------------------------------------------------------------------------
# a valós állapot (brief-fejléc, PR), a csoportosítás (a tesztelhető mag: nincs benne git, gh, fájl)
# ---------------------------------------------------------------------------

def tetel_hivatkozas(tetel):
    """('brief', n) | ('pr', n) | ('nincs', None) | ('szabad', szöveg)."""
    t = tetel.strip()
    if t == '-':
        return 'nincs', None
    m = TETEL_BRIEF.match(t)
    if m:
        return 'brief', int(m.group(1))
    m = TETEL_PR.match(t)
    if m:
        return 'pr', int(m.group(1))
    return 'szabad', t


def pr_kep(pr):
    return {'szam': pr['number'], 'cim': H.PR_TITLE_ELOTAG.sub('', pr.get('title', '')),
            'url': pr.get('url', ''), 'piszkozat': bool(pr.get('isDraft')), 'mergelt': bool(pr.get('mergedAt'))}


def valos_allapot(sor, kontextus):
    """A terv egy sorának állapota. Kulcsok: `lezart` (bool), `cimke`, `kulcs` (CSS), `forras`
    (`brief` | `pr` | `kezi` | `nincs`), `prok`, `megjegyzes` (pl. a kézi jelölés eltérése), `brief`."""
    kod, indok = kezi_allapot(sor['allapot_kezi'])
    fajta, ertek = tetel_hivatkozas(sor['tetel'])
    kezi_lezart = kod in ('kesz', 'elhagyva')
    eredmeny = {'lezart': kezi_lezart, 'elhagyva': kod == 'elhagyva', 'brief': None, 'prok': [],
                'cimke': KEZI_CIMKE.get(kod, 'nincs jelezve'), 'kulcs': kod or 'nincs', 'forras': 'kezi' if kod else 'nincs',
                'kezi_indok': indok, 'megjegyzes': ''}
    if fajta == 'brief':
        b = kontextus['by_szam'].get(ertek)
        if b is None:
            eredmeny['megjegyzes'] = 'a #%d brief nem található, a kézi jelölés érvényes' % ertek
            return eredmeny
        ak = H.allapot_kulcs(b, kontextus['main_all'])
        prok = [pr_kep(p) for p in kontextus['pr_by_brief'].get(ertek, [])]
        if ak != 'lezarva':
            prok = [p for p in prok if not p['mergelt']]     # a korábbi, egyesített részek nem a nyitott sor állapota
        cimke = H.ALLAPOT_CIMKE[ak]
        if ak in ('nem_indult', 'brief_kell') and prok:
            ak, cimke = 'pr', 'nyitott PR van, a feladatleírás fejléce még „nem indult”'
        eredmeny.update(brief=b, lezart=(ak == 'lezarva'), elhagyva=False, cimke=cimke, kulcs=ak,
                        forras='brief', prok=prok)
    elif fajta == 'pr':
        pr = kontextus['pr_by_szam'].get(ertek)
        if pr is None:
            eredmeny['megjegyzes'] = 'a PR#%d nem látszik a lekérdezésben, a kézi jelölés érvényes' % ertek
            return eredmeny
        kep = pr_kep(pr)
        if kep['mergelt']:
            cimke, kulcs = 'egyesítve', 'lezarva'
        elif kep['piszkozat']:
            cimke, kulcs = 'piszkozat, átnézésre vár', 'pr'
        else:
            cimke, kulcs = 'nyitott PR, átnézésre vár', 'pr'
        eredmeny.update(lezart=kep['mergelt'], elhagyva=False, cimke=cimke, kulcs=kulcs, forras='pr', prok=[kep])
    if eredmeny['forras'] in ('brief', 'pr') and kod:
        if kod in ('kesz', 'elhagyva') and (not eredmeny['lezart'] or kod == 'elhagyva'):
            eredmeny['megjegyzes'] = 'a kézi jelölés („%s”) eltér a valós állapottól; a valós állapot érvényes' % KEZI_CIMKE[kod]
        elif kod in ('csuszik', 'blokkolt') and not eredmeny['lezart']:
            eredmeny['megjegyzes'] = 'kézi jelölés: %s — %s' % (KEZI_CIMKE[kod], indok)
    return eredmeny


def kontextus_keszit(briefek, prok, main_all):
    szamozott = [b for b in briefek if b.szam is not None and b.fej
                 and b.fej.get('tipus') in ('feladat', 'naplozas', 'felmeres')]
    by_szam = {b.szam: b for b in szamozott}
    pr_by_brief = {}
    for pr in prok:
        for n in H.pr_brief_szamok(pr, by_szam):
            pr_by_brief.setdefault(n, []).append(pr)
    return {'by_szam': by_szam, 'main_all': main_all, 'prok': prok, 'pr_by_brief': pr_by_brief,
            'pr_by_szam': {p['number']: p for p in prok}}


def kimenet_szoveg(allapot):
    """A visszanézés kimenete: teljesült / elhagyva / blokkolt / csúszott át."""
    if allapot['lezart']:
        return 'elhagyva' if allapot['elhagyva'] else 'teljesült'
    if allapot['kulcs'] == 'blokkolt':
        return 'blokkolt'
    return 'csúszott át'


def keret_osszesites(terv_het, keret_het):
    """OrderedDict: sav -> {'terv': int, 'elhasznalt': int|None}; a tervezett összeg a hét minden sorából (a
    lezártakból is), az elhasznált a `heti_keret.tsv`-ből."""
    kimenet = OrderedDict()
    for sav in SAV_SORREND:
        sorok = [s for s in terv_het if s['sav'] == sav]
        if not sorok:
            continue
        kimenet[sav] = {'terv': sum(int(s['becsult_keret_szazalek']) for s in sorok), 'elhasznalt': None}
    for k in keret_het:
        if k['sav'] in kimenet:
            kimenet[k['sav']]['elhasznalt'] = int(k['elhasznalt_szazalek'])
    return kimenet


def teendok_keszit(nyitott, osszes_het, kontextus):
    """A felhasználó teendői: a terv jóváhagyása, a `Te:` kezdetű megjegyzések, a nyitott brief-ek `Te:` / ⛔ lépései."""
    teendok = []
    javaslat = [s for s in osszes_het if s['jovahagyva'] == 'javaslat']
    if javaslat:
        teendok.append({'szoveg': 'A heti terv jóváhagyása',
                        'reszlet': '%d sor még javaslat (jóváhagyva: %d); jóváhagyás vagy módosítás után a sorok '
                                   'jóváhagyva-mezője „igen” lesz.' % (len(javaslat), len(osszes_het) - len(javaslat)),
                        'sav': None})
    latott = set()
    for s, allapot in nyitott:
        te = TE_ELOTAG.match(s['megjegyzes'])
        if te:
            teendok.append({'szoveg': s['cel_a_het_vegere'], 'reszlet': s['megjegyzes'][te.end():].strip(), 'sav': s['sav']})
            latott.add(s['tetel'])
            continue
        b = allapot['brief']
        if b is not None and s['tetel'] not in latott:
            t = H.teendo_szoveg(b)
            if t:
                teendok.append({'szoveg': s['cel_a_het_vegere'], 'reszlet': t, 'sav': s['sav']})
    return teendok


def epit(terv, keret, otlet, briefek, main_all, prok, dt, het_arg=None):
    """A teljes modell az oldalhoz (a tesztelhető mag): nincs benne fájlolvasás, git vagy gh."""
    het = het_arg or het_kezdete(dt)
    elozo = het - timedelta(days=7)
    kontextus = kontextus_keszit(briefek, prok, main_all)
    terv_het = sorted((s for s in terv if s['het'] == het.isoformat()),
                      key=lambda s: (SAV_SORREND.index(s['sav']), int(s['sorrend'])))
    terv_elozo = sorted((s for s in terv if s['het'] == elozo.isoformat()),
                        key=lambda s: (SAV_SORREND.index(s['sav']), int(s['sorrend'])))
    nyitott, kesz = [], []
    for s in terv_het:
        a = valos_allapot(s, kontextus)
        (kesz if a['lezart'] else nyitott).append((s, a))
    visszanezes = [(s, a, kimenet_szoveg(a)) for s, a in ((s, valos_allapot(s, kontextus)) for s in terv_elozo)]
    keret_het = [k for k in keret if k['het'] == het.isoformat()]
    keret_elozo = [k for k in keret if k['het'] == elozo.isoformat()]
    return {
        'het': het, 'elozo': elozo, 'terv_het': terv_het, 'nyitott': nyitott, 'kesz': kesz,
        'visszanezes': visszanezes, 'keret': keret_osszesites(terv_het, keret_het),
        'keret_elozo': keret_osszesites(terv_elozo, keret_elozo),
        'teendok': teendok_keszit(nyitott, terv_het, kontextus),
        'otlet': otlet, 'felmerendo': [o for o in otlet if otlet_allapot(o['allapot'])[0] == 'felmerendo'],
    }


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

CSS_TOLDALEK = """
.jelzes{display:inline-block;padding:1px 10px;border-radius:999px;font-size:.85rem;font-weight:600;vertical-align:middle}
.j-javaslat{background:var(--figy-bg);color:var(--figy)}
.j-jovahagyott{background:var(--jo-bg);color:var(--jo)}
.sorok-lista{display:block}
.sor{display:grid;grid-template-columns:2.2em 1fr;gap:2px 8px;padding:10px 0;border-top:1px solid var(--vonal);overflow-wrap:anywhere}
.sor:first-child{border-top:0}
.sorrend{color:var(--halk);font-variant-numeric:tabular-nums;text-align:right}
.chip{padding:0 8px;border-radius:999px;background:var(--bg);border:1px solid var(--vonal);color:var(--halk);font-size:.8rem}
.chip.keret{background:var(--kiemel-bg);border-color:transparent;color:var(--kiemel);font-weight:600}
.te{color:var(--figy);font-weight:600}
.megj{font-size:.9rem;color:var(--halk);margin:2px 0 0}
.savfej{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:0 0 8px}
.savfej h2{margin:0}
.savadat{font-size:.9rem;color:var(--halk)}
table.keret{width:100%;border-collapse:collapse;font-size:.95rem}
table.keret th,table.keret td{text-align:left;padding:6px 8px;border-top:1px solid var(--vonal);vertical-align:middle}
table.keret th{color:var(--halk);font-weight:600;border-top:0}
table.keret td.szam{font-variant-numeric:tabular-nums;white-space:nowrap}
.sav-sav{display:block;height:8px;border-radius:999px;background:var(--bg);border:1px solid var(--vonal);overflow:hidden;min-width:80px}
.sav-sav>i{display:block;height:100%;background:var(--kiemel)}
.sav-sav>i.tobb{background:var(--rossz)}
.kimenet{padding:0 8px;border-radius:999px;font-size:.8rem}
.k-teljesult{background:var(--jo-bg);color:var(--jo)}
.k-csuszott-at,.k-blokkolt{background:var(--figy-bg);color:var(--figy)}
.k-elhagyva{background:var(--bg);color:var(--halk);border:1px solid var(--vonal)}
h3.al{margin:16px 0 4px}
"""


def e(szoveg):
    """HTML-escape; a jelölőnyelv (backtick) nem kerül az oldalra."""
    return H.e(str(szoveg).replace('`', ''))


def _szazalek(db):
    return '%d%%' % db


def _tetel_cimke(s):
    fajta, ertek = tetel_hivatkozas(s['tetel'])
    if fajta == 'brief':
        return '<span class="szam">#%d</span>' % ertek
    if fajta == 'pr':
        return '<span class="szam">PR#%d</span>' % ertek
    if fajta == 'szabad':
        return '<span class="szam">%s</span>' % e(s['tetel'])
    return ''


def _allapot_html(a):
    return '<span class="allapot a-%s">%s</span>' % (e(a['kulcs']), e(a['cimke']))


def _sor_html(s, a, tobb_jovahagyas):
    fejresz = ' '.join(x for x in (_tetel_cimke(s), '<span class="cim">%s</span>' % e(s['cel_a_het_vegere'])) if x)
    meta = [_allapot_html(a)]
    if s['modell'] and s['modell'] != '-':
        meta.append('<span class="chip">modell: %s</span>' % e(s['modell']))
    meta.append('<span class="chip keret">%s keret</span>' % e(_szazalek(int(s['becsult_keret_szazalek']))))
    if tobb_jovahagyas:
        meta.append('<span class="chip">%s</span>' % ('jóváhagyva' if s['jovahagyva'] == 'igen' else 'javaslat'))
    pr = H._pr_html(a['prok'])
    if pr:
        meta.append(pr)
    belso = ['<div>%s</div>' % fejresz, '<div class="meta">%s</div>' % ' '.join(meta)]
    if s['megjegyzes']:
        te = TE_ELOTAG.match(s['megjegyzes'])
        if te:
            belso.append('<p class="megj"><span class="te">Te:</span> %s</p>' % e(s['megjegyzes'][te.end():]))
        else:
            belso.append('<p class="megj">%s</p>' % e(s['megjegyzes']))
    if a['megjegyzes']:
        belso.append('<p class="megj">%s</p>' % e(a['megjegyzes']))
    return '<li class="sor"><span class="sorrend">%s.</span><div>%s</div></li>' % (e(s['sorrend']), ''.join(belso))


def _keret_cimke(adat):
    if adat is None:
        return ''
    el = 'nincs megadva' if adat['elhasznalt'] is None else _szazalek(adat['elhasznalt'])
    return 'terv %s · elhasznált %s' % (_szazalek(adat['terv']), el)


def _otlet_html(o):
    kod, hiv = otlet_allapot(o['allapot'])
    cim = '<span class="szam">%s</span> <span class="cim">%s</span>' % (e(o['id']), e(o['cim']))
    meta = ['<span class="allapot">%s</span>' % e(OTLET_CIMKE[kod]), '<span class="chip">%s</span>' % e(SAV_CIMKE[o['sav']])]
    belso = ['<div>%s</div>' % cim, '<div class="meta">%s</div>' % ' '.join(meta),
             '<p class="megj">Forrás: %s</p>' % e(o['forras'])]
    if o['megjegyzes']:
        belso.append('<p class="megj">%s</p>' % e(o['megjegyzes']))
    return '<li class="sor"><span class="sorrend"></span><div>%s</div></li>' % ''.join(belso)


def _keret_tabla(keret, cim):
    if not keret:
        return ''
    reszek = ['<table class="keret"><thead><tr><th>%s</th><th>Tervezett</th><th>Elhasznált</th><th></th></tr></thead><tbody>' % e(cim)]
    osszes_terv, osszes_el, hianyzik = 0, 0, False
    for sav, a in keret.items():
        osszes_terv += a['terv']
        if a['elhasznalt'] is None:
            hianyzik = True
            el_szoveg, sav_html = 'nincs megadva', ''
        else:
            osszes_el += a['elhasznalt']
            el_szoveg = _szazalek(a['elhasznalt'])
            szel = min(100, a['elhasznalt'] * 100 // a['terv']) if a['terv'] else (100 if a['elhasznalt'] else 0)
            sav_html = '<span class="sav-sav"><i class="%s" style="width:%d%%"></i></span>' % (
                'tobb' if a['terv'] and a['elhasznalt'] > a['terv'] else '', szel)
        reszek.append('<tr><td>%s</td><td class="szam">%s</td><td class="szam">%s</td><td>%s</td></tr>'
                      % (e(SAV_CIMKE[sav]), _szazalek(a['terv']), e(el_szoveg), sav_html))
    osszeg_el = 'nincs teljes adat (összesen eddig megadva: %s)' % _szazalek(osszes_el) if hianyzik else _szazalek(osszes_el)
    reszek.append('<tr><th>Összesen</th><th class="szam">%s</th><th class="szam">%s</th><th></th></tr></tbody></table>'
                  % (_szazalek(osszes_terv), e(osszeg_el)))
    return ''.join(reszek)


def jelzes_html(terv_het):
    if not terv_het:
        return ''
    igen = sum(1 for s in terv_het if s['jovahagyva'] == 'igen')
    if igen == len(terv_het):
        return '<span class="jelzes j-jovahagyott">jóváhagyott terv</span>'
    if igen == 0:
        return '<span class="jelzes j-javaslat">javaslat: még nincs jóváhagyva</span>'
    return '<span class="jelzes j-javaslat">részben jóváhagyva: %d / %d sor</span>' % (igen, len(terv_het))


def html_keszit(m, forras_szoveg, ts):
    het = m['het']
    reszek = ['<!doctype html><html lang="hu"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>Heti beosztás</title>'
              '<link rel="preconnect" href="https://fonts.googleapis.com">'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap">'
              '<style>%s%s</style></head><body><main>' % (H.CSS, CSS_TOLDALEK)]
    reszek.append('<h1>Heti beosztás</h1><p class="alcim">Keret-hét: %s %s</p>' % (e(het_szoveg(het)), jelzes_html(m['terv_het'])))
    nyitott_sav = OrderedDict((sav, [(s, a) for s, a in m['nyitott'] if s['sav'] == sav]) for sav in SAV_SORREND)
    kesz_sav = {sav: sum(1 for s, _ in m['kesz'] if s['sav'] == sav) for sav in SAV_SORREND}
    sav_van = [sav for sav in SAV_SORREND if any(s['sav'] == sav for s in m['terv_het'])]

    reszek.append('<ul class="osszesito"><li><a href="#teendok">A te teendőid <b>%d</b></a></li>' % len(m['teendok']))
    for sav in sav_van:
        reszek.append('<li><a href="#sav-%s">%s <b>%d</b></a></li>' % (sav.lower(), e(SAV_CIMKE[sav]), len(nyitott_sav[sav])))
    reszek.append('<li><a href="#keret">Keret</a></li><li><a href="#visszanezes">Visszanézés</a></li></ul>')

    if not m['terv_het']:
        reszek.append('<section><h2>Nincs terv erre a hétre</h2><p class="ures">A `heti_terv.tsv`-ben nincs `het = %s` sor.</p></section>'
                      % e(het.isoformat()))
    reszek.append('<section id="teendok" class="teendok"><h2>A te teendőid ezen a héten <span class="db">%d</span></h2>' % len(m['teendok']))
    if m['teendok']:
        elemek = []
        for t in m['teendok']:
            savjel = ' <span class="sav">%s</span>' % e(SAV_CIMKE[t['sav']]) if t['sav'] else ''
            elemek.append('<li class="teendo"><div class="fej"><span class="cim">%s</span>%s</div><div class="szoveg">%s</div></li>'
                          % (e(t['szoveg']), savjel, e(t['reszlet'])))
        reszek.append('<ul>%s</ul>' % ''.join(elemek))
    else:
        reszek.append('<p class="ures">Ezen a héten nincs rád váró teendő.</p>')
    reszek.append('</section>')

    tobb_jovahagyas = len({s['jovahagyva'] for s in m['terv_het']}) > 1
    for sav in sav_van:
        sorok = nyitott_sav[sav]
        fej = '<div class="savfej"><h2>%s</h2><span class="savadat">%s · %d nyitott sor%s</span></div>' % (
            e(SAV_CIMKE[sav]), e(_keret_cimke(m['keret'].get(sav))), len(sorok),
            (', %d kész (lent, a visszanézésben)' % kesz_sav[sav]) if kesz_sav[sav] else '')
        torzs = ''.join(_sor_html(s, a, tobb_jovahagyas) for s, a in sorok)
        szoveg = '<ul class="sorok-lista">%s</ul>' % torzs if torzs else '<p class="ures">Nincs nyitott sor.</p>'
        if sav == 'FELMERES':
            szoveg += '<h3 class="al">Az ötlettárból felmérendő <span class="db">%d</span></h3>' % len(m['felmerendo'])
            if m['felmerendo']:
                szoveg += '<ul class="sorok-lista">%s</ul>' % ''.join(_otlet_html(o) for o in m['felmerendo'])
            else:
                szoveg += '<p class="ures">Nincs felmérendő tétel az ötlettárban.</p>'
        reszek.append('<section id="sav-%s">%s%s</section>' % (sav.lower(), fej, szoveg))

    reszek.append('<section id="keret"><h2>Keret</h2>%s</section>' % (_keret_tabla(m['keret'], 'Sáv') or '<p class="ures">Nincs tervezett keret.</p>'))

    reszek.append('<section id="visszanezes"><h2>Visszanézés</h2>')
    reszek.append('<h3 class="al">Ezen a héten már kész <span class="db">%d</span></h3>' % len(m['kesz']))
    if m['kesz']:
        reszek.append('<ul class="sorok-lista">%s</ul>' % ''.join(
            '<li class="sor"><span class="sorrend">%s.</span><div><div>%s <span class="cim">%s</span></div>'
            '<div class="meta">%s <span class="chip">%s</span> <span class="chip keret">%s keret</span> %s</div></div></li>'
            % (e(s['sorrend']), _tetel_cimke(s), e(s['cel_a_het_vegere']), _allapot_html(a), e(SAV_CIMKE[s['sav']]),
               e(_szazalek(int(s['becsult_keret_szazalek']))), H._pr_html(a['prok']))
            for s, a in m['kesz']))
    else:
        reszek.append('<p class="ures">Ezen a héten még nem zárult le terv-sor.</p>')
    reszek.append('<h3 class="al">Az előző hét (%s)</h3>' % e(het_szoveg(m['elozo'])))
    if m['visszanezes']:
        db = {}
        for _, _, k in m['visszanezes']:
            db[k] = db.get(k, 0) + 1
        osszegzes = ', '.join('%s: %d' % (k, db[k]) for k in ('teljesült', 'csúszott át', 'blokkolt', 'elhagyva') if k in db)
        reszek.append('<p class="savadat">%s</p>' % e(osszegzes))
        reszek.append('<ul class="sorok-lista">%s</ul>' % ''.join(
            '<li class="sor"><span class="sorrend">%s.</span><div><div>%s <span class="cim">%s</span></div>'
            '<div class="meta"><span class="kimenet k-%s">%s</span> <span class="chip">%s</span> '
            '<span class="chip keret">%s keret</span></div>%s</div></li>'
            % (e(s['sorrend']), _tetel_cimke(s), e(s['cel_a_het_vegere']), e(k.replace(' ', '-')), e(k),
               e(SAV_CIMKE[s['sav']]), e(_szazalek(int(s['becsult_keret_szazalek']))),
               '<p class="megj">%s</p>' % e(a['kezi_indok']) if a['kezi_indok'] else '')
            for s, a, k in m['visszanezes']))
        keret_tabla = _keret_tabla(m['keret_elozo'], 'Sáv')
        if keret_tabla:
            reszek.append(keret_tabla)
    else:
        reszek.append('<p class="ures">Az előző hétre nincs terv a táblában (ez az első hét).</p>')
    reszek.append('</section>')

    szamlalo = {}
    for o in m['otlet']:
        k = otlet_allapot(o['allapot'])[0]
        szamlalo[k] = szamlalo.get(k, 0) + 1
    otlet_szoveg = ', '.join('%s: %d' % (OTLET_CIMKE[k], szamlalo[k]) for k in OTLET_ALLAPOTOK if k in szamlalo)
    reszek.append('<p class="forras">Összeállítva: %s. Ötlettár: %d tétel (%s).<br>Forrás: %s<code>%s</code></p>'
                  % (e(ts.strftime('%Y. %m. %d. %H:%M')), len(m['otlet']), e(otlet_szoveg), e(forras_szoveg[0]),
                     e(forras_szoveg[1])))
    reszek.append('</main></body></html>')
    return ''.join(reszek)


# ---------------------------------------------------------------------------
# összeállítás és CLI
# ---------------------------------------------------------------------------

def osszeallit(gyoker, dt, het_arg=None, pr_json=None, ts=None):
    """(html, modell, hibak, pr_hiba): a teljes folyamat; `hibak` nem üres, ha a táblák hibásak (akkor nincs oldal)."""
    ts = ts or datetime.now()
    terv, keret, otlet, hibak = tablak_olvas(gyoker)
    if hibak:
        return None, None, hibak, None
    briefek = F.briefek_beolvas(gyoker)
    main_ref = F.main_ref(gyoker)
    main_all = F.main_allapotok(gyoker, main_ref) if main_ref else {}
    if pr_json:
        prok, pr_hiba = H.pr_lista_fajl(pr_json)
        pr_forras = 'fájl: %s' % os.path.basename(pr_json)
    else:
        prok, pr_hiba = H.pr_lista_gh(gyoker, dt.date(), 14)
        pr_forras = 'gh pr list --state open | --state merged (az elmúlt 14 nap)'
    modell = epit(terv, keret, otlet, briefek, main_all, prok, dt, het_arg)
    olvashato = ('a három kézi tábla (heti_terv.tsv, heti_keret.tsv, otlettar.tsv), a feladatleírások fejlécei%s és a GitHub-ról '
                 'lekért PR-ok' % (' (az egyesített ággal egyeztetve)' if main_ref else ''))
    if pr_hiba:
        olvashato += '; FIGYELEM: a PR-adat nem érhető el (%s), a PR-hivatkozások és a PR-ból jövő állapotok hiányoznak' % pr_hiba
    ref_hash = (F._git(gyoker, 'rev-parse', '--short', main_ref) or '').strip() if main_ref else ''
    gepi = 'scope=%d terv-sor, %d keret-sor, %d ötlet, %d brief-fejléc, %d PR | forras=adat/heti_terv.tsv, adat/heti_keret.tsv, ' \
           'adat/otlettar.tsv, feladatok.py (briefek_beolvas, main_allapotok%s), %s | ts=%s' % (
               len(terv), len(keret), len(otlet), len(briefek), len(prok),
               ' @ %s %s' % (main_ref, ref_hash) if main_ref else '', pr_forras, ts.strftime('%Y-%m-%dT%H:%M:%S'))
    return html_keszit(modell, (olvashato, gepi), ts), modell, [], pr_hiba


def _repon_belul(ut, gyoker):
    ut = os.path.normcase(os.path.realpath(ut))
    gy = os.path.normcase(os.path.realpath(gyoker))
    return ut == gy or ut.startswith(gy + os.sep)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Heti beosztás oldal generálása a heti tervből, a brief-fejlécekből és a PR-okból.')
    ap.add_argument('--kimenet', help='a HTML útja (a repón kívül)')
    ap.add_argument('--gyoker', default=REPO)
    ap.add_argument('--ma', help='ÉÉÉÉ-HH-NN: a nap vége (UTC); alapértelmezés: most')
    ap.add_argument('--het', help='a megjelenített hét kezdete (szombat, ÉÉÉÉ-HH-NN); alapértelmezés: a --ma szerinti hét')
    ap.add_argument('--pr-json', help='a gh helyett: PR-lista JSON-fájlból')
    ap.add_argument('--ellenoriz', action='store_true', help='csak a három tábla ellenőrzése')
    a = ap.parse_args(argv)
    if a.ellenoriz:
        terv, keret, otlet, hibak = tablak_olvas(a.gyoker)
        for h in hibak:
            print('HIBA: %s' % h, file=sys.stderr)
        print('heti_terv: %d sor, heti_keret: %d sor, otlettar: %d sor; hiba: %d' % (len(terv), len(keret), len(otlet), len(hibak)))
        return 2 if hibak else 0
    if not a.kimenet:
        ap.error('a --kimenet kötelező (vagy --ellenoriz)')
    if _repon_belul(a.kimenet, a.gyoker):
        print('HIBA: a --kimenet a repón belülre mutat; a generált nézet a repón kívülre kerül.', file=sys.stderr)
        return 2
    if a.ma:
        nap = datum_olvas(a.ma)
        if nap is None:
            print('HIBA: a --ma alakja ÉÉÉÉ-HH-NN', file=sys.stderr)
            return 2
        dt = datetime.combine(nap, time(23, 59))
    else:
        dt = datetime.now(timezone.utc).replace(tzinfo=None)
    het_arg = None
    if a.het:
        het_arg = datum_olvas(a.het)
        if het_arg is None or het_arg.weekday() != SZOMBAT:
            print('HIBA: a --het szombati ÉÉÉÉ-HH-NN dátum kell', file=sys.stderr)
            return 2
    oldal, m, hibak, pr_hiba = osszeallit(a.gyoker, dt, het_arg=het_arg, pr_json=a.pr_json)
    if hibak:
        for h in hibak:
            print('HIBA: %s' % h, file=sys.stderr)
        print('A táblák hibásak, az oldal nem készült el.', file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.kimenet)), exist_ok=True)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(oldal)
    print('kimenet: %s' % os.path.abspath(a.kimenet))
    print('hét: %s; sorok: %d nyitott, %d kész; a te teendőid: %d; felmérendő ötlet: %d'
          % (m['het'].isoformat(), len(m['nyitott']), len(m['kesz']), len(m['teendok']), len(m['felmerendo'])))
    if pr_hiba:
        print('FIGYELEM: %s' % pr_hiba, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
