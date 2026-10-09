#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F85.6 — a TAHOT_kivonat.tsv átkulcsolása a jóváhagyott esetlista szerint (DT-F85a; brief 3. tétel).

Csak az `Igehely` (első) oszlop változik, azokon a soron, amelyek verse a `naplok/F85_esetlista.tsv`-ben
`eltolas` vagy `osszevonas_2_1` típusú, és a javasolt Károli-kulcs (`karoli_vers`) eltér a TAHOT-kulcstól
(337 vers). A `bizonytalan` (kulcs = kulcs) és az összevonás-partner (a kulcsa már a közös Károli-kulcs) sorok
változatlanok. A fájlbeli sorrend nem változik: az összevonásnál a második TAHOT-vers sorai közvetlenül az
első után maradnak.

Bájt-szintű munka: a fájlt bájtként olvassa, a sorokat a `\\n`-nél vágja (a sorvég-jelek maradnak), a mezőket a
tabulátornál (split / join, a csv modul tilos). Írás előtt (a memóriában) ellenőriz, eltérésnél LEÁLL és nem ír:
  - a sorok száma azonos;
  - minden sor az Igehely mezőn kívül bájtra egyezik az eredetivel;
  - a nem érintett sorok teljesen bájtazonosak;
  - az átírt kulcsok pontosan a jóváhagyott leképezés szerintiek (régi kulcs -> egyetlen új kulcs);
  - minden új kulcs létező Károli-vers (Karoli_1908.tsv), és az új kulcsok csoportosítása megegyezik az esetlista
    szerinti (csak a 2:1 összevonások osztoznak kulcson);
  - a 2:1 összevonások két TAHOT-versének sorai a fájlban folyamatosan következnek (jelentés), és a Károli-
    sorrend törései (a TAHOT-fájl eleve tartalmaz áthelyezett verseket) régi/új számát kiírja.
Idempotencia-őr: ha a leképezés régi kulcsai már nem szerepelnek a fájlban, leáll.

Kimenet: naplok/F85_kulcsvaltas.tsv (soronként: fájlbeli sorszám, régi -> új kulcs, típus, a sor TAHOT-verse, az
összevonás partnere).

Használat (a repó gyökeréből):
    python eszkozok/tahot_verskulcs_atkulcsolas.py         # szárazon: ellenőriz és jelent
    python eszkozok/tahot_verskulcs_atkulcsolas.py --ir    # ellenőriz, majd ír
"""
import os
import sys
import collections

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAHOT = os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')
KAROLI = os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv')
LISTA = os.path.join(ROOT, 'naplok', 'F85_esetlista.tsv')
NAPLO = os.path.join(ROOT, 'naplok', 'F85_kulcsvaltas.tsv')
VART = 337


def leall(uzenet):
    print('LEÁLL (nem írtam semmit): ' + uzenet)
    sys.exit(1)


def bont(ig):
    k, r = ig.rsplit(' ', 1)
    c, v = r.split(':')
    return k, int(c), int(v)


def leképezés():
    """{régi TAHOT-kulcs: (új Károli-kulcs, típus, partner)} a jóváhagyott sorokra."""
    sorok = []
    with open(LISTA, encoding='utf-8') as fh:
        for s in fh:
            if s.startswith('#') or s.startswith('konyv\t'):
                continue
            p = s.rstrip('\n').split('\t')
            sorok.append(p)
    kar_tahot = collections.defaultdict(list)    # Károli-kulcs -> az esetlista TAHOT-versei
    for p in sorok:
        if p[3] and ';' not in p[3] and p[2]:
            kar_tahot[p[3]].append(p[2])
    ki = {}
    for p in sorok:
        t, k, tip = p[2], p[3], p[4]
        if tip not in ('eltolas', 'osszevonas_2_1'):
            continue
        if not t or not k or ';' in k:
            leall('az esetlista %s sora nem egyetlen Károli-kulcsot ad: %r' % (t, k))
        if t == k:
            continue
        partner = [x for x in kar_tahot[k] if x != t]
        ki[t] = (k, 'osszevonas' if tip == 'osszevonas_2_1' else 'eltolas', ';'.join(partner))
    return ki


def main():
    ir = '--ir' in sys.argv
    kep = leképezés()
    if len(kep) != VART:
        leall('a leképezés %d vers, a jóváhagyott %d' % (len(kep), VART))
    karoli = set()
    with open(KAROLI, encoding='utf-8') as fh:
        next(fh)
        for s in fh:
            karoli.add(s.split('\t', 1)[0])
    if any(k not in karoli for k, _, _ in kep.values()):
        leall('van új kulcs, amely nincs a Karoli_1908.tsv-ben: %s' % [k for k, _, _ in kep.values() if k not in karoli][:5])

    nyers = open(TAHOT, 'rb').read()
    sorok = nyers.split(b'\n')
    vege_ures = sorok[-1] == b''
    if vege_ures:
        sorok = sorok[:-1]
    # idempotencia-őr
    kulcsok_most = set()
    for s in sorok[1:]:
        kulcsok_most.add(s.split(b'\t', 1)[0].decode('utf-8'))
    hianyzo = [t for t in kep if t not in kulcsok_most]
    if hianyzo:
        leall('a leképezés %d régi kulcsa nincs a fájlban (már átkulcsolt?): %s' % (len(hianyzo), hianyzo[:5]))

    uj_sorok = []
    naplo = []
    for i, s in enumerate(sorok, 1):
        if i == 1:
            uj_sorok.append(s)
            continue
        mezok = s.split(b'\t')
        regi = mezok[0].decode('utf-8')
        if regi in kep:
            uj, tip, partner = kep[regi]
            mezok[0] = uj.encode('utf-8')
            naplo.append((i, regi, uj, tip, regi, partner))
            uj_sorok.append(b'\t'.join(mezok))
        else:
            uj_sorok.append(s)

    # --- írás előtti ellenőrzés ---
    if len(uj_sorok) != len(sorok):
        leall('a sorok száma változott')
    valtozott = 0
    for i, (a, b) in enumerate(zip(sorok, uj_sorok), 1):
        if a == b:
            continue
        valtozott += 1
        ma, mb = a.split(b'\t'), b.split(b'\t')
        if len(ma) != len(mb) or ma[1:] != mb[1:]:
            leall('a %d. sor az Igehely mezőn kívül is eltér' % i)
    if valtozott != len(naplo):
        leall('az eltérő sorok száma (%d) nem egyezik a naplóéval (%d)' % (valtozott, len(naplo)))
    # az átírt kulcsok: régi -> pontosan egy új kulcs
    r2u = collections.defaultdict(set)
    for _, regi, uj, *_ in naplo:
        r2u[regi].add(uj)
    if len(r2u) != VART or any(len(v) != 1 for v in r2u.values()):
        leall('a régi->új kulcs leképezés nem egyértelmű vagy nem %d vers' % VART)
    # az új kulcsok csoportosítása: csak a 2:1 összevonások osztoznak kulcson
    uj_kulcs_regi = collections.defaultdict(set)
    for s in uj_sorok[1:]:
        pass
    for a, b in zip(sorok[1:], uj_sorok[1:]):
        uj_kulcs_regi[b.split(b'\t', 1)[0].decode('utf-8')].add(a.split(b'\t', 1)[0].decode('utf-8'))
    ossz = {k: v for k, v in uj_kulcs_regi.items() if len(v) > 1}
    for k, v in ossz.items():
        van_osszevonas = any(kep[t][1] == 'osszevonas' for t in v if t in kep)
        if not van_osszevonas or len(v) != 2:
            leall('váratlan kulcs-ütközés: %s <- %s' % (k, sorted(v)))
    if len(ossz) != 9:
        leall('az összevonó új kulcsok száma %d, várt 9' % len(ossz))
    # a fájlsorrend nem változik (a sorok helye azonos); a Károli-sorrend "törései" (a TAHOT-fájl eleve tartalmaz
    # áthelyezett verseket, pl. Ézs 8:23 a könyv végén) a régi és az új kulcsokon összevetve
    def toresek(listaja):
        elozo, ut, utolso = {}, [], None
        for i, ig in enumerate(listaja, 2):
            if ig == utolso:
                continue
            utolso = ig
            k, c, v = bont(ig)
            if k in elozo and (c, v) < elozo[k]:
                ut.append(i)
            elozo[k] = (c, v)
        return ut

    regi_kulcsok = [x.split(b'	', 1)[0].decode('utf-8') for x in sorok[1:]]
    uj_kulcsok = [x.split(b'	', 1)[0].decode('utf-8') for x in uj_sorok[1:]]
    t_regi, t_uj = toresek(regi_kulcsok), toresek(uj_kulcsok)
    print('Károli-sorrend törései: régi %d, új %d' % (len(t_regi), len(t_uj)))
    # a 2:1 összevonások: a két TAHOT-vers sorai a fájlban szomszédos blokkok
    nem_szomszed = []
    for k, v in ossz.items():
        pozok = sorted(i for i, ig in enumerate(regi_kulcsok) if ig in v)
        blokkok = sorted(set(regi_kulcsok[i] for i in pozok))
        folyamatos = pozok == list(range(pozok[0], pozok[-1] + 1))
        if not folyamatos:
            nem_szomszed.append((k, sorted(v)))
    print('összevonások, amelyeknél a két TAHOT-vers sorai nem folyamatosan következnek: %d %s' % (len(nem_szomszed), nem_szomszed))
    # a közös kulcson belül a sorrend: a Károli-szövegben előbb álló (kisebb TAHOT-kulcsú) vers sorai fájlbeli sorrendben is előbb
    for k, v in ossz.items():
        a, b = sorted(v, key=lambda x: bont(x)[1:])
        elso = {x: min(i for i, ig in enumerate(regi_kulcsok) if ig == x) for x in (a, b)}
        if elso[a] > elso[b]:
            leall('a közös %s kulcson belül a %s sorai a fájlban a(z) %s után állnak' % (k, a, b))

    # --- összegzés ---
    konyv = collections.OrderedDict()
    for _, regi, uj, tip, *_ in naplo:
        b = bont(regi)[0]
        konyv.setdefault(b, {'vers': set(), 'sor': 0, 'eltolas': set(), 'osszevonas': set()})
        konyv[b]['vers'].add(regi)
        konyv[b]['sor'] += 1
        konyv[b][tip].add(regi)
    print('átírandó: %d vers, %d sor (a fájl %d sor)' % (len(r2u), len(naplo), len(sorok)))
    print('könyv\tvers\teltolás\tösszevonás\tsor')
    for b, d in konyv.items():
        print('%s\t%d\t%d\t%d\t%d' % (b, len(d['vers']), len(d['eltolas']), len(d['osszevonas']), d['sor']))
    print('közös új kulcsra kerülő (2:1) kulcsok: %d' % len(ossz))
    print('az ellenőrzések rendben; ' + ('írok.' if ir else 'szárazon, nem írtam (--ir kell).'))
    if not ir:
        return 0

    tartalom = b'\n'.join(uj_sorok) + (b'\n' if vege_ures else b'')
    with open(TAHOT, 'wb') as fh:
        fh.write(tartalom)
    with open(NAPLO, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_atkulcsolas.py | scope=konkordancia/TAHOT_kivonat.tsv, a naplok/F85_esetlista.tsv jóváhagyott (DT-F85a) 337 verse | ts=2026-10-09 | a sorszám a fájlbeli sorszám (a fejléc az 1. sor)\n')
        fh.write('sorszam\tregi_kulcs\tuj_kulcs\ttipus\ttahot_vers\tosszevonas_partner\n')
        for n in naplo:
            fh.write('\t'.join([str(n[0]), n[1], n[2], n[3], n[4], n[5]]) + '\n')
    print('írva: %s (%d sor), %s' % (TAHOT, len(sorok), NAPLO))
    return 0


if __name__ == '__main__':
    sys.exit(main())
