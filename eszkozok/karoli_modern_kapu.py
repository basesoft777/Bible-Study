#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_modern_kapu.py -- a modernizált Károli – Strong nyílt mag (`nyilt_karoli_modern/`) kapuja (F174, FELADATOK #174).

A brief 2. lépésének pontjai, a csomagon (a lemezen vagy egy `export()` kimenetén):
    TELJESSEG   (a) minden régi pár átvetítve (multihalmaz-egyezés a `parok_*.tsv`-vel), új nem keletkezett; minden
                Strongos token kulcsa megvan, azonos 1908-as alakkal; minden modern token szerepel, azonos modern
                alakkal, kieső-jelöléssel és gazdaszóval; a #96 zárásakor mért 61 könyves K3b-szám (418 633)
                ugyanazon a 61 könyvön ma is kijön                                                        — BUKÁS
    LICENC      (b) CC BY 4.0 a LICENSE-ben; a TAHOT/TAGNT-attribúció szó szerint; nincs nem kompatibilis licenc
                (NC, SA, GPL, „minden jog fenntartva”)                                                    — BUKÁS
    HARMADIK    (c) nincs export-kód és nem engedett fájltípus; nincs héber/görög írásjel (a TAHOT/TAGNT nyers
                szövege); nincs zárt külső forrás neve                                                    — BUKÁS
    UJRA        (d) az export újrafuttatva bájtazonos a lemezen állóval                                    — BUKÁS
    NYILVANOS   (e) nyilvános szövegben nincs belső jelölés (DT/N/F-szám, belső útvonal, proveniencia-kulcs,
                `manual`), „orkesztrátor”, „felhasználó…”, „termék”, GitHub, helyőrző; a „PaRDeS” nem áll benne
                (így nem is központi keretezés)                                                           — BUKÁS
    KOZLEMENY   a `kozlemeny/` hu/en tervezete megvan, nincs az ellenőrző összegben, a `.gitattributes`
                kihagyja a kiadásból (export-ignore)                                                       — BUKÁS
    OSSZEG      az `ELLENORZO_OSSZEG.sha256` minden kiadott fájlt helyes összeggel listáz; a `KIADAS.txt`
                tartalmi hash-e egyezik                                                                    — BUKÁS
    VALTOZATLAN a `nyilt_mag/` és a gyökérbeli `CITATION.cff` változatlan a main-hez képest            — BUKÁS
                (FIGYELEM, ha a main nem érhető el)

Kilépési kód: 0, ha nincs BUKÁS. TSV-olvasás `split('\\t')`.

Használat:
    python eszkozok/karoli_modern_kapu.py [--konyvtar nyilt_karoli_modern] [--gyors]
    (--gyors: az UJRA pont nélkül)
"""
import argparse
import collections
import glob
import hashlib
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_modern_export as E  # noqa: E402

GYOKER = E.GYOKER
BUKAS, FIGYELEM, OK = 'BUKÁS', 'FIGYELEM', 'OK'
K3B_96 = 418633                                   # naplok/KAROLI_MODERN_zaras.md: a #96 zárásakor, 61 könyv
K3B_96_NELKUL = {'Mt', 'Mk', 'Luk', 'Ján', 'ApCsel'}  # a #96 zárásakor még nem párosított könyvek

Talalat = collections.namedtuple('Talalat', 'azon suly uzenet')

ENGEDETT_NEV = re.compile(r'^(?:konyvek/\d{2}_[1-3]?[A-Z][A-Za-z]+\.tsv|versek\.tsv|kodkonyv\.tsv|[A-Z_]+\.md|'
                          r'LICENSE|CITATION\.cff|\.gitattributes|ELLENORZO_OSSZEG\.sha256|KIADAS\.txt|RELEASE\.txt|'
                          r'kozlemeny/kozlemeny_(?:hu|en)\.md)$')
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
    # az angol „manual exception list / decision” megengedett; a belső proveniencia-érték nem
    (re.compile(r'\bmanual\b(?!\s+(?:exception|alignment|decision))'), 'belső érték (manual)'),
    (re.compile(r'[Oo]rkesztr|[Oo]rchestrat'), '„orkesztrátor”'),
    (re.compile(r'[Ff]elhasználó'), '„felhasználó”'),
    (re.compile(r"user's decision|the user\b", re.I), '„user” mint döntéshozó'),
    (re.compile(r'termék', re.I), '„termék”'),
    (re.compile(r'github', re.I), 'GitHub'),
    (re.compile(r'PaRDeS', re.I), '„PaRDeS”'),
    (re.compile(r'HELYŐRZŐ|<[A-Z_]+_URL>|\[A LEXIKON CÍME\]'), 'helyőrző'),
    (re.compile(r'\bgerinc', re.I), 'belső fogalom (gerinc)'),
]
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

_OSIS = {}


def osis(ig):
    """Az igehely OSIS-kulcsa, gyorsítótárral (a tokenenkénti hívás a 600 ezer soron lassú)."""
    if ig not in _OSIS:
        _OSIS[ig] = E.NM.osis(ig)
    return _OSIS[ig]


def forras_beolvas():
    """Független beolvasás a forrástáblákból (nem az export függvényeivel)."""
    parok = collections.Counter()
    for rel in E.relglob(E.PAROK):
        _, ps = E.tsv(rel)
        for p in ps:
            parok[(osis(p['vers']), p['hu_sorszam'], p['er_sorszam'], p['strong'])] += 1
    strongos = {}
    for rel in E.relglob(E.SZAVAK):
        _, ss = E.tsv(rel)
        for s in ss:
            if s['oldal'] == 'hu' and s['allapot'] == 'parositva':
                strongos[(s['vers'], s['sorszam'])] = s['szo']
    _, modern = E.tsv(E.MODERN)
    return parok, strongos, modern


_FORRAS = None


def forras():
    global _FORRAS
    if _FORRAS is None:
        _FORRAS = forras_beolvas()
    return _FORRAS


def teljesseg(fajlok):
    ki = []
    parok, strongos, modern = forras()
    csomag_par = collections.Counter()
    token = {}
    for rel in sorted(f for f in fajlok if f.startswith('konyvek/')):
        fej, sorok = adatsorok(fajlok[rel])
        if fej != E.FEJ:
            ki.append(Talalat('TELJESSEG', BUKAS, '%s: eltérő oszlopfejléc' % rel))
            continue
        for s in sorok:
            k = (s['osis'], s['token'])
            t = (s['alak_1908'], s['alak_modern'], s['kieso'], s['gazda_token'])
            if token.setdefault(k, t) != t:
                ki.append(Talalat('TELJESSEG', BUKAS, '%s %s: a token sorai ellentmondanak' % k))
            if s['strong']:
                if s['allapot'] != 'javaslat':
                    ki.append(Talalat('TELJESSEG', BUKAS, '%s %s: a pár állapota nem „javaslat”' % k))
                csomag_par[(s['osis'], s['token'], s['eredeti_token'], s['strong'])] += 1
    if csomag_par != parok:
        hiany = parok - csomag_par
        tobblet = csomag_par - parok
        ki.append(Talalat('TELJESSEG', BUKAS, 'a párok nem egyeznek: %d hiányzik, %d új (pl. %s)' % (
            sum(hiany.values()), sum(tobblet.values()), (sorted(hiany) or sorted(tobblet))[0])))
    # modern tokenek
    hibas = 0
    for t in modern:
        k = (osis(t['igehely']), t['sorszam'])
        if token.get(k) != (t['alak_1908'], t['alak_modern'], t['kieso'], t['kieso_gazda']):
            hibas += 1
    if hibas or len(token) != len(modern):
        ki.append(Talalat('TELJESSEG', BUKAS, 'a modern tokenek: %d eltér, a csomagban %d, a forrásban %d' % (
            hibas, len(token), len(modern))))
    # Strongos tokenek kulcsa és 1908-as alakja
    nincs = [k for k, szo in strongos.items() if token.get((osis(k[0]), k[1]), ('',))[0] != szo]
    if nincs:
        ki.append(Talalat('TELJESSEG', BUKAS, '%d Strongos token kulcsa vagy alakja hiányzik (pl. %s %s)' % (
            (len(nincs),) + nincs[0])))
    k61 = sum(1 for k in strongos if k[0].rsplit(' ', 1)[0] not in K3B_96_NELKUL)
    if k61 != K3B_96:
        ki.append(Talalat('TELJESSEG', BUKAS, 'a #96-os 61 könyvön a Strongos token %d, nem %d' % (k61, K3B_96)))
    if not ki:
        ki.append(Talalat('TELJESSEG', OK, '%d pár, %d Strongos token (ebből a 61 könyvön %d), %d modern token' % (
            sum(parok.values()), len(strongos), k61, len(modern))))
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
    return ki or [Talalat('NYILVANOS', OK, 'nincs belső jelölés a nyilvános szövegben')]


def kozlemeny(fajlok):
    ki = []
    for n in ('kozlemeny_hu.md', 'kozlemeny_en.md'):
        if E.KOZLEMENY_DIR + n not in fajlok:
            ki.append(Talalat('KOZLEMENY', BUKAS, 'hiányzik: %s%s' % (E.KOZLEMENY_DIR, n)))
    if 'kozlemeny/ export-ignore' not in fajlok.get('.gitattributes', ''):
        ki.append(Talalat('KOZLEMENY', BUKAS, 'a .gitattributes nem hagyja ki a kozlemeny/ mappát'))
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
            d = subprocess.run(['git', 'diff', '--name-only', ref, '--', 'nyilt_mag', 'CITATION.cff'], cwd=GYOKER,
                               capture_output=True, text=True, encoding='utf-8')
            if d.stdout.strip():
                return [Talalat('VALTOZATLAN', BUKAS, 'változott a %s-hoz képest: %s' % (ref, d.stdout.split()))]
            return [Talalat('VALTOZATLAN', OK, 'a nyilt_mag/ és a CITATION.cff változatlan (%s)' % ref)]
    return [Talalat('VALTOZATLAN', FIGYELEM, 'a main nem érhető el, nem mérve')]


def mer(fajlok, ujra_is=True, git_is=True):
    t = teljesseg(fajlok) + licenc(fajlok) + harmadik(fajlok) + nyilvanos(fajlok) + kozlemeny(fajlok) + osszeg(fajlok)
    if ujra_is:
        t += ujra(fajlok)
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
