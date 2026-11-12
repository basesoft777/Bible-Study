#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_strong_kapu.py -- a Károli 1908 – Strong szóillesztés nyílt mag (`nyilt_karoli_strong/`) kapuja (F175,
FELADATOK #175).

A brief 1. lépésének pontjai, a csomagon (a lemezen vagy egy `export()` kimenetén):
    TELJESSEG   (a) minden forrás-pár átjött (multihalmaz-egyezés a `parok_*.tsv`-vel), új nem keletkezett; minden
                forrás-token (magyar és eredeti) pontosan egyszer, azonos állapottal, partnerrel és Stronggal; a magyar
                alak a forrásé; minden Károli-vers szövege a forrásé; a párok száma a #172 keretéé; a `meres.tsv`
                minden mérési sort hordoz                                                             — BUKÁS
    LICENC      (b) CC BY 4.0 a LICENSE-ben; a TAHOT/TAGNT-attribúció szó szerint; nincs nem kompatibilis licenc
                (NC, SA, GPL, „minden jog fenntartva”)                                                 — BUKÁS
    HARMADIK    (c) nincs export-kód és nem engedett fájltípus; nincs héber/görög írásjel (a TAHOT/TAGNT nyers
                szövege); nincs a zárt külső összevetési forrás neve                                   — BUKÁS
    UJRA        (d) az export újrafuttatva bájtazonos a lemezen állóval                                 — BUKÁS
    NYILVANOS   (e) nyilvános szövegben nincs belső jelölés (DT/N/F-szám, belső útvonal, proveniencia-kulcs,
                `manual`), „orkesztrátor”, „felhasználó…”, „termék”, GitHub, helyőrző; a „PaRDeS” nem áll benne
                (így nem is központi keretezés); a README és az OLVASSEL jóváhagyott kiadás-mondata áll — BUKÁS
    NEVELO      a magyar szövegekben a szám előtti névelő a kiejtés szerinti (az 598 715, a 34, az 1. kiadás),
                és nincs el nem döntött „a(z)” alak                                                      — BUKÁS
    KOZLEMENY   a `kozlemeny/` hu/en tervezete (rövid közlemény) megvan, nincs az ellenőrző összegben, a
                `.gitattributes` kihagyja a kiadásból (export-ignore)                                    — BUKÁS
    KEZIRAT     a második data paper kézirata (`kozlemeny/data_paper/karoli_strong_kezirat_hu/en.md`, a repó
                gyökerében, a csomagon kívül; DT-F175b) a generálttal azonos, és a törzse a nyilvános
                szövegszabályok szerint tiszta (az UJRA ponttal fut)                                     — BUKÁS
    OSSZEG      az `ELLENORZO_OSSZEG.sha256` minden kiadott fájlt helyes összeggel listáz; a `KIADAS.txt`
                tartalmi hash-e egyezik                                                                 — BUKÁS
    VALTOZATLAN a `nyilt_mag/` és a gyökérbeli `CITATION.cff` változatlan (a main-nel közös bázishoz képest)                                                         — BUKÁS
                (FIGYELEM, ha a main nem érhető el)

Kilépési kód: 0, ha nincs BUKÁS. TSV-olvasás `split('\\t')`.

Használat:
    python eszkozok/karoli_strong_kapu.py [--konyvtar nyilt_karoli_strong] [--gyors]
    (--gyors: az UJRA pont nélkül)
"""
import argparse
import collections
import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_export as E  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = E.GYOKER
BUKAS, FIGYELEM, OK = 'BUKÁS', 'FIGYELEM', 'OK'

Talalat = collections.namedtuple('Talalat', 'azon suly uzenet')

ENGEDETT_NEV = re.compile(r'^(?:(?:parok|szavak)/\d{2}_[1-3]?[A-Z][A-Za-z]+\.tsv|versek\.tsv|meres\.tsv|'
                          r'kodkonyv\.tsv|[A-Z_]+\.md|LICENSE|CITATION\.cff|\.gitattributes|ELLENORZO_OSSZEG\.sha256|'
                          r'KIADAS\.txt|RELEASE\.txt|kozlemeny/kozlemeny_(?:hu|en)\.md)$')
HEBER_GOROG = re.compile('[֐-׿Ͱ-Ͽἀ-῿יִ-ﭏ]')
ZART_FORRAS = re.compile(r'Bible[- ]?Discovery|Biblia[- ]?Felfedez', re.I)
NEM_KOMPATIBILIS = re.compile(r'\bNC\b|NonCommercial|nem kereskedelmi|BY-SA|ShareAlike|\bGPL|minden jog fenntartva|'
                              r'all rights reserved', re.I)
TILTOTT = [
    (re.compile(r'\bDT-?F?\d+'), 'döntés-azonosító'),
    (re.compile(r'\bN-F?\d+'), 'nyitott tétel azonosítója'),
    (re.compile(r'\bF\d{2,3}(?:\.\d+)?\b'), 'feladat-azonosító'),
    (re.compile(r'#\d{2,3}\b'), 'feladatszám'),
    (re.compile(r'\b(?:naplok|eszkozok|adat|konkordancia|f172|f22|f21p|lexikon|motivumlog)/'), 'belső útvonal'),
    (re.compile(r'\b(?:scope|forras|ts)='), 'proveniencia-kulcs'),
    (re.compile(r'\bmanual\b(?!\s+(?:exception|alignment|decision|review))'), 'belső érték (manual)'),
    (re.compile(r'[Oo]rkesztr|[Oo]rchestrat'), '„orkesztrátor”'),
    (re.compile(r'[Ff]elhasználó'), '„felhasználó”'),
    (re.compile(r"user's decision|the user\b", re.I), '„user” mint döntéshozó'),
    (re.compile(r'termék', re.I), '„termék”'),
    (re.compile(r'github', re.I), 'GitHub'),
    (re.compile(r'PaRDeS', re.I), '„PaRDeS”'),
    (re.compile(r'HELYŐRZŐ|<[A-Z_]+_URL>|\[A LEXIKON CÍME\]|\{[a-z_]+\}'), 'helyőrző'),
    (re.compile(r'\bgerinc', re.I), 'belső fogalom (gerinc)'),
    (re.compile(r'régi arany|old gold', re.I), 'belső fogalom (régi arany)'),
]
KIADAS_MONDAT = {'OLVASSEL.md': 'A csomag minden fájlja a kiadás része.',
                 'README.md': 'Every file of the package is part of the release.'}
MAGYAR = ('OLVASSEL.md', 'MODSZER.md', 'ISMERT_HIBAK.md', 'ATTRIBUCIO.md', 'LICENSE', 'KODKONYV.md', 'kodkonyv.tsv',
          'kozlemeny/kozlemeny_hu.md')
KIHAGYOTT = ('ELLENORZO_OSSZEG.sha256', 'KIADAS.txt', 'RELEASE.txt')


def olvas_csomag(konyvtar):
    abs_k = os.path.join(GYOKER, konyvtar) if not os.path.isabs(konyvtar) else konyvtar
    ki = {}
    for gy, _, nevek in os.walk(abs_k):
        for n in nevek:
            ut = os.path.join(gy, n)
            with open(ut, encoding='utf-8', newline='') as f:
                ki[os.path.relpath(ut, abs_k).replace('\\', '/')] = f.read()
    return ki


def adatsorok(szoveg):
    sorok = [s for s in szoveg.split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def nyilvanos_szoveg(rel, szoveg):
    """A nyilvános szövegnek számító részek: a próza teljesen, a TSV-ből a megjegyzéssorok és a kódkönyv."""
    if rel.endswith('.tsv') and rel != 'kodkonyv.tsv':
        return '\n'.join(s for s in szoveg.split('\n') if s.startswith('#'))
    return szoveg


# ----------------------------------------------------------------------------- (a) teljesség

_FORRAS = None


def forras():
    """Független beolvasás a forrástáblákból (nem az export átalakító függvényével)."""
    global _FORRAS
    if _FORRAS is None:
        parok = collections.Counter()
        for rel in E.relglob(E.PAROK):
            for p in E.tsv(rel)[1]:
                parok[(E.osis(p['vers']), p['hu_sorszam'], p['hu_szo'], p['er_sorszam'], p['strong'])] += 1
        szavak = {}
        for rel in E.relglob(E.SZAVAK):
            for s in E.tsv(rel)[1]:
                k = (E.osis(s['vers']), s['oldal'], s['sorszam'])
                if k in szavak:
                    raise SystemExit('kapu: a forrás-szótábla kulcsa kétszer áll: %s' % (k,))
                szavak[k] = (s['szo'] if s['oldal'] == 'hu' else '', s['allapot'], s['partner_sorszam'], s['strong'])
        versek = {E.osis(v['Igehely']): v['Károli-szöveg (teljes vers)'] for v in E.tsv(E.KAROLI)[1]}
        _, meres = E.tsv(E.F172_MERES)
        _FORRAS = (parok, szavak, versek, len(meres))
    return _FORRAS


def teljesseg(fajlok):
    ki = []
    parok, szavak, versek, meres_db = forras()
    csomag_par = collections.Counter()
    for rel in sorted(f for f in fajlok if f.startswith('parok/')):
        fej, sorok = adatsorok(fajlok[rel])
        if fej != E.PAR_FEJ:
            ki.append(Talalat('TELJESSEG', BUKAS, '%s: eltérő oszlopfejléc' % rel))
            continue
        for s in sorok:
            if s['allapot'] != 'javaslat':
                ki.append(Talalat('TELJESSEG', BUKAS, '%s %s: a pár állapota nem „javaslat”' % (s['osis'], s['token'])))
            if s['kapcsolat'] != E.kapcsolat(s['strong']):
                ki.append(Talalat('TELJESSEG', BUKAS, '%s %s: hibás kapcsolattípus' % (s['osis'], s['token'])))
            csomag_par[(s['osis'], s['token'], s['alak_1908'], s['eredeti_token'], s['strong'])] += 1
    if csomag_par != parok:
        hiany, tobblet = parok - csomag_par, csomag_par - parok
        ki.append(Talalat('TELJESSEG', BUKAS, 'a párok nem egyeznek: %d hiányzik, %d új (pl. %s)' % (
            sum(hiany.values()), sum(tobblet.values()), (sorted(hiany) or sorted(tobblet))[0])))
    csomag_szo = {}
    for rel in sorted(f for f in fajlok if f.startswith('szavak/')):
        fej, sorok = adatsorok(fajlok[rel])
        if fej != E.SZO_FEJ:
            ki.append(Talalat('TELJESSEG', BUKAS, '%s: eltérő oszlopfejléc' % rel))
            continue
        for s in sorok:
            k = (s['osis'], s['oldal'], s['token'])
            if k in csomag_szo:
                ki.append(Talalat('TELJESSEG', BUKAS, 'kétszer álló szó: %s' % (k,)))
            csomag_szo[k] = (s['alak_1908'], s['allapot'], s['partner_token'], s['strong'])
    if csomag_szo != szavak:
        elter = [k for k in set(szavak) | set(csomag_szo) if szavak.get(k) != csomag_szo.get(k)]
        ki.append(Talalat('TELJESSEG', BUKAS, 'a szavak nem egyeznek: %d eltérés (pl. %s)' % (len(elter), sorted(elter)[0])))
    if 'versek.tsv' in fajlok:
        _, vs = adatsorok(fajlok['versek.tsv'])
        if {v['osis']: v['szoveg_1908'] for v in vs} != versek or len(vs) != len(versek):
            ki.append(Talalat('TELJESSEG', BUKAS, 'a versek szövege vagy száma eltér a forrásétól'))
    else:
        ki.append(Talalat('TELJESSEG', BUKAS, 'hiányzik: versek.tsv'))
    keret = int(E._f172(E.F172_KERET, 'reteg', 'OSSZES')['parsor'])
    if sum(parok.values()) != keret:
        ki.append(Talalat('TELJESSEG', BUKAS, 'a forrás párszáma (%d) nem a mért kereté (%d)' % (sum(parok.values()), keret)))
    if 'meres.tsv' in fajlok:
        _, ms = adatsorok(fajlok['meres.tsv'])
        if len([m for m in ms if m['szakasz'] != 'kulso']) != meres_db or len([m for m in ms if m['szakasz'] == 'kulso']) != 6:
            ki.append(Talalat('TELJESSEG', BUKAS, 'a meres.tsv sorszáma nem a mérőtábláé'))
    else:
        ki.append(Talalat('TELJESSEG', BUKAS, 'hiányzik: meres.tsv'))
    if not ki:
        ki.append(Talalat('TELJESSEG', OK, '%d pár, %d szó, %d vers, %d mérési sor' % (
            sum(parok.values()), len(szavak), len(versek), meres_db + 6)))
    return ki


# ----------------------------------------------------------------------------- (b)–(e), összeg

def licenc(fajlok):
    ki = []
    lic = fajlok.get('LICENSE', '')
    if 'CC BY 4.0' not in lic or 'creativecommons.org/licenses/by/4.0' not in lic:
        ki.append(Talalat('LICENC', BUKAS, 'a LICENSE nem CC BY 4.0'))
    att = fajlok.get('ATTRIBUCIO.md', '')
    if E.STEP_ATTRIB not in att or 'TAHOT' not in att or 'TAGNT' not in att:
        ki.append(Talalat('LICENC', BUKAS, 'a TAHOT/TAGNT-attribúció hiányzik vagy nem szó szerinti'))
    for rel, sz in sorted(fajlok.items()):
        m = NEM_KOMPATIBILIS.search(nyilvanos_szoveg(rel, sz))
        if m:
            ki.append(Talalat('LICENC', BUKAS, '%s: nem kompatibilis licenc-említés: %r' % (rel, m.group(0))))
    return ki or [Talalat('LICENC', OK, 'CC BY 4.0, attribúcióval')]


def harmadik(fajlok):
    ki = []
    for rel, sz in sorted(fajlok.items()):
        if not ENGEDETT_NEV.match(rel):
            ki.append(Talalat('HARMADIK', BUKAS, 'nem engedett fájl (export-kód vagy idegen adat?): %s' % rel))
        m = HEBER_GOROG.search(sz)
        if m:
            ki.append(Talalat('HARMADIK', BUKAS, '%s: héber/görög írásjel (%r)' % (rel, m.group(0))))
        m = ZART_FORRAS.search(sz)
        if m:
            ki.append(Talalat('HARMADIK', BUKAS, '%s: zárt külső forrás neve (%r)' % (rel, m.group(0))))
    return ki or [Talalat('HARMADIK', OK, 'nincs export-kód és harmadik fél nyers adata')]


def nyilvanos(fajlok):
    ki = []
    for rel, sz in sorted(fajlok.items()):
        t = nyilvanos_szoveg(rel, sz)
        for rx, nev in TILTOTT:
            for m in rx.finditer(t):
                ki.append(Talalat('NYILVANOS', BUKAS, '%s: %s: %r' % (rel, nev, m.group(0))))
    for rel, minta in KIADAS_MONDAT.items():
        if minta not in fajlok.get(rel, ''):
            ki.append(Talalat('NYILVANOS', BUKAS, '%s: hiányzik a jóváhagyott mondat: %r' % (rel, minta)))
    return ki or [Talalat('NYILVANOS', OK, 'nincs belső jelölés a nyilvános szövegben')]


def nevelo(fajlok):
    """A magyar szövegekben (és minden TSV magyar megjegyzéssorában) a szám előtti névelő a kiejtés szerinti."""
    ki = []
    for rel, sz in sorted(fajlok.items()):
        if rel in MAGYAR or rel.endswith('.tsv'):
            for h in E.nevelo_hibak(nyilvanos_szoveg(rel, sz)):
                ki.append(Talalat('NEVELO', BUKAS, '%s: %r' % (rel, h)))
    return ki or [Talalat('NEVELO', OK, 'a számok előtti névelő a kiejtés szerinti')]


def kozlemeny(fajlok):
    ki = []
    for n in ('kozlemeny_hu.md', 'kozlemeny_en.md'):
        if E.KOZLEMENY_DIR + n not in fajlok:
            ki.append(Talalat('KOZLEMENY', BUKAS, 'hiányzik: %s%s' % (E.KOZLEMENY_DIR, n)))
    if 'kozlemeny/ export-ignore' not in fajlok.get('.gitattributes', ''):
        ki.append(Talalat('KOZLEMENY', BUKAS, 'a .gitattributes nem hagyja ki a kozlemeny/ mappát'))
    if '* text eol=lf' not in fajlok.get('.gitattributes', ''):
        ki.append(Talalat('OSSZEG', BUKAS, 'a .gitattributes nem rögzíti az LF sorvéget'))
    if E.KOZLEMENY_DIR in fajlok.get('ELLENORZO_OSSZEG.sha256', ''):
        ki.append(Talalat('KOZLEMENY', BUKAS, 'a kozlemeny/ az ellenőrző összegben áll'))
    return ki or [Talalat('KOZLEMENY', OK, 'a tervezet megvan, a kiadásból kihagyva')]


def osszeg(fajlok):
    ki = []
    lista = {}
    for s in fajlok.get('ELLENORZO_OSSZEG.sha256', '').split('\n'):
        if s:
            h, rel = s.split('  ', 1)
            lista[rel] = h
    vart = {rel for rel in fajlok if rel not in KIHAGYOTT and not rel.startswith(E.KOZLEMENY_DIR)}
    if set(lista) != vart:
        ki.append(Talalat('OSSZEG', BUKAS, 'a lista eltér a fájloktól: %s' % sorted(set(lista) ^ vart)[:5]))
    for rel in sorted(vart & set(lista)):
        if hashlib.sha256(fajlok[rel].encode('utf-8')).hexdigest() != lista[rel]:
            ki.append(Talalat('OSSZEG', BUKAS, 'eltérő SHA-256: %s' % rel))
    h = hashlib.sha256(fajlok.get('ELLENORZO_OSSZEG.sha256', '').encode('utf-8')).hexdigest()
    if ('tartalmi_hash_sha256: %s' % h) not in fajlok.get('KIADAS.txt', ''):
        ki.append(Talalat('OSSZEG', BUKAS, 'a KIADAS.txt tartalmi hash-e nem egyezik'))
    return ki or [Talalat('OSSZEG', OK, '%d fájl, helyes összegekkel' % len(lista))]


def ujra(fajlok):
    friss, _ = E.export()
    elter = sorted(rel for rel in set(friss) | set(fajlok) if friss.get(rel) != fajlok.get(rel))
    if elter:
        return [Talalat('UJRA', BUKAS, 'az újrafuttatás eltér: %s' % elter[:5])]
    return [Talalat('UJRA', OK, 'bájtazonos (%d fájl)' % len(friss))]


def valtozatlan():
    for ref in ('origin/main', 'main'):
        r = subprocess.run(['git', 'rev-parse', '--verify', '-q', ref], cwd=GYOKER, capture_output=True)
        if r.returncode == 0:
            # a merge-bázishoz képest: a main közben mozoghat (pl. a #710), ez nem ennek az ágnak a változása
            b = subprocess.run(['git', 'merge-base', ref, 'HEAD'], cwd=GYOKER, capture_output=True, text=True)
            alap = b.stdout.strip() or ref
            d = subprocess.run(['git', 'diff', '--name-only', alap, '--', 'nyilt_mag', 'CITATION.cff'], cwd=GYOKER,
                               capture_output=True, text=True, encoding='utf-8')
            if d.stdout.strip():
                return [Talalat('VALTOZATLAN', BUKAS, 'változott a %s-hoz képest: %s' % (ref, d.stdout.split()))]
            return [Talalat('VALTOZATLAN', OK, 'a nyilt_mag/ és a CITATION.cff változatlan (%s)' % ref)]
    return [Talalat('VALTOZATLAN', FIGYELEM, 'a main nem érhető el, nem mérve')]


def kezirat(N, lemez=True):
    """A csomagon kívüli kézirat (DT-F175b): a törzse a nyilvános szövegszabályok szerint tiszta; a lemezen álló
    fájl a generált szöveggel azonos (ha `lemez`)."""
    ki = []
    for rel, (torzs, szoveg) in E.kezirat(N).items():
        for rx, nev in TILTOTT:
            for m in rx.finditer(torzs):
                ki.append(Talalat('KEZIRAT', BUKAS, '%s: %s: %r' % (rel, nev, m.group(0))))
        if rel.endswith('_hu.md'):
            for h in E.nevelo_hibak(torzs):
                ki.append(Talalat('KEZIRAT', BUKAS, '%s: hibás névelő: %r' % (rel, h)))
        for rx, nev in ((HEBER_GOROG, 'héber/görög írásjel'), (ZART_FORRAS, 'zárt külső forrás neve'),
                        (NEM_KOMPATIBILIS, 'nem kompatibilis licenc')):
            m = rx.search(torzs)
            if m:
                ki.append(Talalat('KEZIRAT', BUKAS, '%s: %s: %r' % (rel, nev, m.group(0))))
        if lemez:
            ut = os.path.join(GYOKER, rel)
            if not os.path.exists(ut):
                ki.append(Talalat('KEZIRAT', BUKAS, 'hiányzik: %s' % rel))
            else:
                with open(ut, encoding='utf-8', newline='') as f:
                    if f.read().replace('\r\n', '\n') != szoveg:     # a gyökérben nincs eol=lf (autocrlf)
                        ki.append(Talalat('KEZIRAT', BUKAS, 'a lemezen álló kézirat eltér a generálttól: %s' % rel))
    return ki or [Talalat('KEZIRAT', OK, 'a kézirat (hu/en) generált, a szövegszabályok szerint tiszta')]


def mer(fajlok, ujra_is=True, git_is=True):
    t = (teljesseg(fajlok) + licenc(fajlok) + harmadik(fajlok) + nyilvanos(fajlok) + nevelo(fajlok) + kozlemeny(fajlok)
         + osszeg(fajlok))
    if ujra_is:
        t += ujra(fajlok)
        t += kezirat(E.export()[1])
    if git_is:
        t += valtozatlan()
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--konyvtar', default=E.KIMENET)
    ap.add_argument('--gyors', action='store_true', help='az újrafuttatás (UJRA) nélkül')
    a = ap.parse_args()
    fajlok = olvas_csomag(a.konyvtar)
    if not fajlok:
        print('BUKÁS: üres vagy hiányzó könyvtár: %s' % a.konyvtar)
        return 1
    t = mer(fajlok, ujra_is=not a.gyors)
    for x in t:
        print('%-9s %-12s %s' % (x.suly, x.azon, x.uzenet))
    bukas = sum(1 for x in t if x.suly == BUKAS)
    print('összesen: %d BUKÁS, %d FIGYELEM' % (bukas, sum(1 for x in t if x.suly == FIGYELEM)))
    return 1 if bukas else 0


if __name__ == '__main__':
    sys.exit(main())
