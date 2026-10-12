#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tagnt_zarojeles_potlas.py — a TAGNT-kivonat [..] (KJV) és {..} (egyéb) jelölésű
szó-sorainak pótlása (F90, FELADATOK #90).

A nyers TAGNT a versszámozás-eltérést a hivatkozás-mezőben jelöli
(`Mat.15.6{15.5}#01=k`, `2Co.13.13[13.14]#01=NKO`). A `TAGNT_kivonat.tsv` régi
generátora (a repóban nincs, a `konkordancia/TAHOT_TAGNT_README.md` írja le) csak a
kerek zárójelet (NA) ismerte; a [..] és {..} sorok kimaradtak (48 csoport, 350 sor).

A szkript:
  1. beolvassa a két nyers fájlt (`TAGNT Mat-Jhn …`, `TAGNT Act-Rev …`), és
     ellenőrzi az sha256-ukat (STEPBible-Data, blob 705c1bc1… és 4bbea2c1…;
     `naplok/F90_jelentes.md`);
  2. minden szó-sort a README mezőképzésével vetít (Igehely, Strong, alak, kiejtés,
     szótő, jelentés, angol, kiadás); a kulcs a `Konyv_normalizalo_tabla.tsv`
     könyvcseréje, a 4 NA-esetben a README `KAROLI_DONTES`-e, a [..]/{..}
     csoportokban a jóváhagyott `naplok/F90_karoli_dontesek.tsv` (DT-F90b);
  3. a teljes vetületet a nyers sorrendben, majd kulcs szerint stabilan rendezi
     (könyv a nyers előfordulás sorrendjében, fejezet, vers); a versen belüli
     szórend a nyers sorrend;
  4. ELLENŐRZI, hogy a vetületből a [..]/{..} sorokat elhagyva pontosan a meglévő
     kivonat marad (soronként, sorrendben) — eltérésnél MEGÁLL, nem ír;
  5. `--ir` mellett a kivonatot úgy írja, hogy a meglévő sorok bájtjai változatlanok
     (az eredeti sorokat az eredeti bájtokból másolja), csak sorok szúródnak be.

Újrafuttatható: ha a kivonat már a teljes vetülettel egyezik, nem ír, 0-val lép ki.

I/O: sima split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md, „TSV-olvasás”).
A nyers fájlok nincsenek a repóban (DT-F33a/f); a --nyers a repón kívüli könyvtár.

Futtatás a repó gyökeréből:
    python eszkozok/tagnt_zarojeles_potlas.py --nyers <könyvtár>          # szárazon
    python eszkozok/tagnt_zarojeles_potlas.py --nyers <könyvtár> --ir     # ír
"""

import argparse
import glob
import hashlib
import os
import re
import sys
from collections import Counter, OrderedDict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIVONAT = os.path.join(GYOKER, 'konkordancia', 'TAGNT_kivonat.tsv')
NORM = os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
DONTESEK = os.path.join(GYOKER, 'naplok', 'F90_karoli_dontesek.tsv')

# a nyers fájlok: (névrész, sha256) — a sorrend a nyers könyvsorrend
NYERS_FAJLOK = (
    ('TAGNT Mat-Jhn', 'ab8eaaeb68e17a1dcfa34e1e9350358f22f03bc2a97244d848750ad81044bc8e'),
    ('TAGNT Act-Rev', '524e32375361e6d3fa2f7ef00b87605fdc4317a762f395651a05fdc31ad031b7'),
)

REF = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)(?:([\[({])(\d+)\.(\d+)[\])}])?#(\d+)=')
GOROG = re.compile(r'^(.*?)\s*\((.*)\)\s*$')
SORSZ = re.compile(r'^#(\d+)–#(\d+)$')

# a README „Károli-natív kulcs a 4 kivételre” táblája (NA, kerek zárójel)
KAROLI_DONTES = {
    ('Rom', '3', '25', '3', '26'): ('3', '26'),
    ('Act', '13', '39', '13', '38'): ('13', '39'),
    ('Mrk', '12', '15', '12', '14'): ('12', '14'),
    ('Act', '19', '41', '19', '40'): ('19', '40'),
}


def sha256(ut):
    """sha256 a CRLF -> LF normalizált tartalmon: a forrásblob LF-es, a core.autocrlf=true
    checkout viszont CRLF-et írhat a munkafába (minta: eszkozok/forras_letolt.py)."""
    with open(ut, 'rb') as f:
        adat = f.read()
    return hashlib.sha256(adat.replace(b'\r\n', b'\n')).hexdigest()


def nyers_fajlok(konyvtar):
    ki = []
    for nev, vart in NYERS_FAJLOK:
        talalat = [p for p in glob.glob(os.path.join(konyvtar, '*.txt')) if nev in os.path.basename(p)]
        if len(talalat) != 1:
            raise SystemExit('MEGÁLL: a(z) „%s” nyers fájl nem egyértelmű/hiányzik: %s' % (nev, talalat))
        kapott = sha256(talalat[0])
        if kapott != vart:
            raise SystemExit('MEGÁLL: sha256-eltérés (%s): %s, várt %s' % (talalat[0], kapott, vart))
        ki.append(talalat[0])
    return ki


def norm_tabla():
    t = {}
    with open(NORM, encoding='utf-8') as f:
        for i, s in enumerate(f):
            if i == 0:
                continue
            m = s.rstrip('\n').rstrip('\r').split('\t')
            if len(m) > 1 and m[0]:
                t[m[0]] = m[1]
    return t


def dontesek_betolt():
    """{(csoport, nn) -> Károli-kulcs}; a csoport a nyers hivatkozás '#' előtti része."""
    d = {}
    with open(DONTESEK, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    fej = sorok[0].split('\t')
    ix = {n: i for i, n in enumerate(fej)}
    for s in sorok[1:]:
        if not s.strip():
            continue
        m = s.split('\t')
        if not m[ix['allapot']].startswith('jóváhagyva'):
            raise SystemExit('MEGÁLL: nem jóváhagyott döntés: %s' % m[0])
        r = SORSZ.match(m[ix['nyers_sorszam']])
        if not r:
            raise SystemExit('MEGÁLL: hibás sorszám-tartomány: %s' % m[ix['nyers_sorszam']])
        for nn in range(int(r.group(1)), int(r.group(2)) + 1):
            kulcs = (m[ix['nyers_hivatkozas']], nn)
            if kulcs in d:
                raise SystemExit('MEGÁLL: kétszer döntött sor: %s #%02d' % kulcs)
            d[kulcs] = m[ix['karoli_kulcs']]
    return d


def vetit(mezok):
    """A README „TAGNT (görög)” mezőképzése: a kivonat Igehely utáni 7 oszlopa."""
    g = GOROG.match(mezok[1])
    alak, kiejtes = (g.group(1), g.group(2)) if g else (mezok[1].strip(), '')
    strongok = [s.strip().split('_')[0] for s in mezok[11].split(',') if s.strip()]
    dg = mezok[4]
    reszek = [p.strip() for p in dg.split(' + ')] if ' + ' in dg else [dg]
    tok, glo = [], []
    for p in reszek:
        a, b = (p.split('=', 1) + [''])[:2]
        tok.append(a.strip())
        glo.append(b.strip())
    return ['+'.join(strongok), alak, kiejtes, '+'.join(tok), '+'.join(glo), mezok[2].strip(), mezok[5]]


def teljes_vetulet(fajlok):
    """[(kulcs-sztring, rendezőkulcs, sor, uj)] a nyers sorrendben; uj=True a [..]/{..} soron."""
    norm = norm_tabla()
    dontes = dontesek_betolt()
    hasznalt = set()
    konyv_sorrend = OrderedDict()
    ki = []
    for fn in fajlok:
        with open(fn, encoding='utf-8') as f:
            for sor in f:
                m = REF.match(sor)
                if not m:
                    continue
                mezok = sor.rstrip('\n').rstrip('\r').split('\t')
                k, c, v, zar = m.group(1), m.group(2), m.group(3), m.group(4)
                uj = zar in ('[', '{')
                konyv_hu = norm[k]
                if zar == '(':
                    c, v = KAROLI_DONTES[(k, c, v, m.group(5), m.group(6))]
                    igehely = '%s %s:%s' % (konyv_hu, c, v)
                elif uj:
                    csop = mezok[0].split('#')[0]
                    nn = int(m.group(7))
                    if (csop, nn) not in dontes:
                        raise SystemExit('MEGÁLL: döntés nélküli zárójeles sor: %s' % mezok[0])
                    hasznalt.add((csop, nn))
                    igehely = dontes[(csop, nn)]
                else:
                    igehely = '%s %s:%s' % (konyv_hu, int(c), int(v))
                konyv_sorrend.setdefault(konyv_hu, len(konyv_sorrend))
                kb, cv = igehely.rsplit(' ', 1)
                if kb != konyv_hu:
                    raise SystemExit('MEGÁLL: a döntés könyve eltér a nyers könyvtől: %s -> %s' % (mezok[0], igehely))
                fc, fv = cv.split(':')
                rend = (konyv_sorrend[konyv_hu], int(fc), int(fv))
                ki.append((igehely, rend, '\t'.join([igehely] + vetit(mezok)), uj))
    fel_nem = set(dontes) - hasznalt
    if fel_nem:
        raise SystemExit('MEGÁLL: a döntési tábla %d sora nem illeszkedik nyers sorra: %s' % (len(fel_nem), sorted(fel_nem)[:5]))
    # stabil rendezés kulcs szerint (a versen belül a nyers sorrend marad)
    return [x for _, x in sorted(enumerate(ki), key=lambda p: (p[1][1], p[0]))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nyers', required=True, help='a két nyers TAGNT-fájlt tartalmazó könyvtár (a repón kívül)')
    ap.add_argument('--ir', action='store_true', help='a kivonat írása (nélküle csak jelent)')
    a = ap.parse_args()

    vet = teljes_vetulet(nyers_fajlok(a.nyers))

    with open(KIVONAT, 'rb') as f:
        nyers_bajtok = f.read()
    if b'\r' in nyers_bajtok:
        raise SystemExit('MEGÁLL: a kivonatban CR-bájt van (a .gitattributes LF-et ír elő)')
    if not nyers_bajtok.endswith(b'\n'):
        raise SystemExit('MEGÁLL: a kivonat nem sorvéggel zárul')
    eredeti = nyers_bajtok.split(b'\n')[:-1]          # bájtsorok, sorvég nélkül
    fejlec, adat = eredeti[0], eredeti[1:]
    adat_sz = [b.decode('utf-8') for b in adat]

    teljes = [x[2] for x in vet]
    if adat_sz == teljes:
        print('A kivonat már a teljes vetülettel egyezik (%d sor); nincs teendő.' % len(adat_sz))
        return 0
    regi = [x[2] for x in vet if not x[3]]
    if adat_sz != regi:
        elso = next((i for i, (p, q) in enumerate(zip(adat_sz, regi)) if p != q), min(len(adat_sz), len(regi)))
        raise SystemExit('MEGÁLL: a meglévő kivonat nem a vetület régi része (sor: %d, kivonat %d sor, vetület %d sor)'
                         % (elso + 2, len(adat_sz), len(regi)))

    uj = [x for x in vet if x[3]]
    kulcsok_elotte = set(s.split('\t', 1)[0] for s in adat_sz)
    uj_kulcsok = OrderedDict()
    for x in uj:
        uj_kulcsok[x[0]] = uj_kulcsok.get(x[0], 0) + 1
    print('meglévő sor: %d · beszúrandó: %d · új összesen: %d' % (len(adat_sz), len(uj), len(teljes)))
    print('érintett Károli-kulcs: %d, ebből a kivonatban eddig nem létező: %d'
          % (len(uj_kulcsok), sum(1 for k in uj_kulcsok if k not in kulcsok_elotte)))
    for k, n in uj_kulcsok.items():
        print('  %s\t+%d%s' % (k, n, '\t(új kulcs)' if k not in kulcsok_elotte else ''))

    if not a.ir:
        print('Szárazon futott (--ir nélkül), nem írt.')
        return 0

    # írás: a régi sorok bájtjai az eredetiből, az újak UTF-8-ban
    ki = [fejlec]
    ri = 0
    for x in vet:
        if x[3]:
            ki.append(x[2].encode('utf-8'))
        else:
            ki.append(adat[ri])
            ri += 1
    assert ri == len(adat)
    tartalom = b'\n'.join(ki) + b'\n'
    # visszaellenőrzés: az új sorokat elhagyva bájtra az eredeti
    vissza = [b for b, x in zip(ki[1:], vet) if not x[3]]
    if b'\n'.join([fejlec] + vissza) + b'\n' != nyers_bajtok:
        raise SystemExit('MEGÁLL: a régi sorok nem bájtazonosak, nem ír')
    with open(KIVONAT, 'wb') as f:
        f.write(tartalom)
    print('írva: %s (%d sor + fejléc)' % (os.path.relpath(KIVONAT, GYOKER), len(teljes)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
