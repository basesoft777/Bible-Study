#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bizonyiteklap.py -- F224.5: a cikkírás B lépése, a bizonyítéklap: a kulcsversek lánc-szavai, együttállásai és
gépi jelöltjei, gyakorisági (véletlen-) alapvonallal, **ítélet nélkül**.

A menetbeli helye: `MUNKAMENET.md` C) szakasz, C-bl sor (a lépéssor: A igeszakasz-blokkok → **B bizonyítéklap** → C
érvvázlat → D bíráló …). A bíráló (`.claude/agents/biralo.md`) és az író (az érvvázlathoz) ebből dolgozik.

Bemenet:
- a kulcsversek: `--versek "1Móz 3:17; 1Móz 8:21"`, vagy `--motivum <ID>` esetén a motívum `adat/elofordulasok.tsv`-sorai;
- a lánc szavai (Strong): `--lanc H0779,H0127,…`; ha hiányzik és van `--motivum`, a motívum sorainak `strong` mezője.

Kimenet (Markdown; a forma szabálya: `adat/SEMA.md` 2.71, F224.5):
- **Gyakorisági alapvonal:** minden lánc-szó versszáma a korpuszban (ÓSZ: `konkordancia/TAHOT_kivonat.tsv`, ÚSZ:
  `konkordancia/TAGNT_kivonat.tsv`, a Károli-vers a kulcs), és az aránya a korpusz verseihez;
- **versenként:** a vers állapota a motívum adatában (eldöntött: `adat/elofordulasok.tsv`; jelölt: `adat/jeloltek.tsv`
  döntéssel; vagy nem áll az adatban), a Károli-szöveg, a lánc szavai a versben sorrendben (pozíció, alak, szótő,
  glossza), az **együttállások** (minden pár, amely a versben együtt áll: a korpuszban megfigyelt együttes versszám és
  a véletlen-alapvonal szerint várt szám, `n_A · n_B / N`), és a **fordított sorrendű ismétlés** gépi jelöltje (A … B …
  B … A, csak versen belül), a véletlen-alapvonallal: a vers lánc-szavainak összes sorrendje közül hányban áll ilyen
  minta.

Amit az eszköz NEM csinál:
- **nem ítél**: nincs ítélet-, erősség- vagy „szignifikáns” mező; a szám a bíráló és az író bemenete;
- **láncon átívelő „keret” vagy „khiazmus” jelölt nincs**: a fordított ismétlés csak egy versen belül jelölt; a
  „keret”, „khiazmus” megnevezés mindig értelmezés (`.claude/agents/biralo.md` 7. kérdés);
- a tanulmány adatát nem ismétli: a `--tanulmany <fájl>` csak hivatkozásként áll a lap elején;
- jelöltet nem dönt el és nem léptet elő: a cikk és a bizonyítéklap csak **eldöntött** (a `jeloltek.tsv`-n átment,
  az `elofordulasok.tsv`-ben álló) sort vesz át; a többi vers állapota a lapon kimondva áll (CLAUDE.md 2. szabály).

Minden adatsor mellett proveniencia-sor (`scope=… | forras=… | ts=…`, CLAUDE.md 1. szabály). A TSV-k olvasása
`split('\\t')` (CLAUDE.md).

CLI:
    python eszkozok/bizonyiteklap.py --motivum HAMART-001 --versek "1Móz 3:17; 1Móz 8:21; 1Móz 12:3" --lanc H0779,H0127,H7043
    python eszkozok/bizonyiteklap.py --motivum HAMART-001 --kimenet naplok/BIZONYITEK_HAMART-001.md
"""
import argparse
import datetime
import itertools
import os
import random
import re
import sys

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ESZKOZOK)
import proza_allitas as P  # noqa: E402  (Igehelyek, Adat.versek, tsv_dict, strong_norm, Károli)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = P.ROOT
T_JELOLT = os.path.join(P.ADAT, 'jeloltek.tsv')
PERMUTACIO_MAX = 9        # e fölött a fordított ismétlés alapvonala mintavétellel (rögzített maggal)
MINTA_N = 5000
MAG = 224


def tsv_sorok(ut):
    """(sorszám, dict) a TSV adat-sorain; a `#` kezdetű sorok kimaradnak (split('\\t'))."""
    ki, fej = [], None
    with open(ut, 'r', encoding='utf-8') as f:
        for i, sor in enumerate(f, 1):
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            if fej is None:
                fej = sor.split('\t')
                continue
            ki.append((i, dict(zip(fej, sor.split('\t')))))
    return ki


class Korpusz:
    """A lánc-szavak versei a teljes TAHOT/TAGNT táblán, és a kulcsversek szósorai (egy menetben)."""

    def __init__(self, lanc, kulcsversek, tahot=P.T_TAHOT, tagnt=P.T_TAGNT):
        self.lanc = list(lanc)
        lanc_h = set(lanc)
        kell = set(kulcsversek)
        self.versei = {s: set() for s in lanc}       # Strong -> versek
        self.n_vers = {'H': 0, 'G': 0}               # a korpusz versszáma testamentumonként
        self.szavak = {k: [] for k in kulcsversek}   # vers -> [(poz, strong, alak, szoto, glossza)]
        self.szoto = {}                              # Strong -> az első előfordulás szótöve
        for elotag, ut in (('H', tahot), ('G', tagnt)):
            if not os.path.exists(ut):
                continue
            latott = set()
            with open(ut, 'r', encoding='utf-8') as f:
                fej = None
                poz = {}
                for sor in f:
                    sor = sor.rstrip('\n').rstrip('\r')
                    if not sor:
                        continue
                    if fej is None:
                        fej = sor.split('\t')
                        i_ig, i_st = fej.index('Igehely'), fej.index('Strong-szám')
                        i_al = fej.index('Ragozott alak')
                        i_sz, i_gl = fej.index('Szótő'), fej.index('Rövid jelentés')
                        continue
                    p = sor.split('\t')
                    if len(p) <= max(i_ig, i_st):
                        continue
                    k = p[i_ig]
                    latott.add(k)
                    s = P.strong_norm(p[i_st])
                    if k in kell:
                        poz[k] = poz.get(k, 0) + 1
                        if s in lanc_h:
                            self.szavak[k].append((poz[k], s, p[i_al] if len(p) > i_al else '',
                                                   p[i_sz] if len(p) > i_sz else '', p[i_gl] if len(p) > i_gl else ''))
                    if s in lanc_h:
                        self.versei[s].add(k)
                        if s not in self.szoto and len(p) > i_sz:
                            self.szoto[s] = p[i_sz]
            self.n_vers[elotag] = len(latott)

    def testamentum(self, s):
        return 'G' if s.startswith('G') else 'H'

    def egyutt(self, a, b):
        return len(self.versei.get(a, set()) & self.versei.get(b, set()))

    def vart(self, a, b):
        n = self.n_vers[self.testamentum(a)]
        if not n or self.testamentum(a) != self.testamentum(b):
            return None
        return len(self.versei.get(a, ())) * len(self.versei.get(b, ())) / n


def forditott_ismetles(sorozat):
    """A … B … B … A minta (A ≠ B) a sorozatban: az első találat (A, B) párja, vagy None."""
    n = len(sorozat)
    for i in range(n):
        for l in range(n - 1, i + 2, -1):
            if sorozat[l] != sorozat[i]:
                continue
            belso = sorozat[i + 1:l]
            for j in range(len(belso)):
                if belso[j] == sorozat[i]:
                    continue
                if belso[j] in belso[j + 1:]:
                    return sorozat[i], belso[j]
    return None


def forditott_alapvonal(sorozat):
    """A vers lánc-szavainak összes sorrendje közül hányban áll fordított ismétlés: (arány, módszer)."""
    if len(sorozat) < 4:
        return 0.0, 'a versben négynél kevesebb lánc-szó áll: a minta nem állhat elő'
    if len(sorozat) <= PERMUTACIO_MAX:
        egyedi = set(itertools.permutations(sorozat))
        talalt = sum(1 for x in egyedi if forditott_ismetles(list(x)))
        return talalt / len(egyedi), 'teljes felsorolás (%d különböző sorrend)' % len(egyedi)
    rnd = random.Random(MAG)
    talalt = 0
    for _ in range(MINTA_N):
        x = list(sorozat)
        rnd.shuffle(x)
        if forditott_ismetles(x):
            talalt += 1
    return talalt / MINTA_N, 'mintavétel (%d keverés, mag=%d)' % (MINTA_N, MAG)


def vers_allapot(mid, vers, elof, jelolt, adat=None):
    """A vers állapota a motívum adatában: (állapot, hivatkozás). Az adatsor igehelye tartomány is lehet
    (`1Móz 4:10-11`): `adat` megadásakor a tartomány versei is illeszkednek (a független ellenőrzés, 2026-11-16)."""
    if not mid:
        return 'motívum nélkül (csak tájékoztatás)', '–'

    def illik(igehely):
        return igehely == vers or bool(adat and vers in adat.versek(igehely))
    for i, d in elof:
        if d.get('id') == mid and illik(d.get('igehely', '')):
            return 'eldöntött', 'adat/elofordulasok.tsv:%d' % i
    for i, d in jelolt:
        if d.get('id') == mid and illik(d.get('igehely', '')) and d.get('jelolt_tipus', '') in ('', 'elofordulas'):
            return 'jelölt, döntés: %s (nem vehető át)' % (d.get('dontes') or '?'), 'adat/jeloltek.tsv:%d' % i
    return 'nem áll a motívum adatában (nem vehető át)', '–'


def keszit(mid, versek, lanc, tanulmany=None, elof_ut=P.T_ELOF, jelolt_ut=T_JELOLT, tahot=P.T_TAHOT, tagnt=P.T_TAGNT,
           ts=None):
    ts = ts or datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    adat = P.Adat()
    kulcs = []
    for v in versek:
        for k in adat.versek(v) or [v]:
            if k not in kulcs:
                kulcs.append(k)
    korp = Korpusz(lanc, kulcs, tahot, tagnt)
    elof = tsv_sorok(elof_ut) if os.path.exists(elof_ut) else []
    jelolt = tsv_sorok(jelolt_ut) if os.path.exists(jelolt_ut) else []
    forras = 'konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv (kulcs: Károli-vers), konkordancia/Karoli_1908.tsv'
    ki = ['# Bizonyítéklap — %s' % (mid or 'kézi verslista'), '',
          '<!-- GENERÁLT: eszkozok/bizonyiteklap.py — kézzel nem szerkesztendő; újrafuttatással frissül. -->', '',
          '*B lépés (`MUNKAMENET.md` C-bl). Ítélet nélkül: a számok a bíráló és az író bemenetei. A fordított sorrendű '
          'ismétlés csak versen belüli gépi jelölt; láncon átívelő keret-jelölt nincs.*', '',
          '*(proveniencia: scope=%d vers; lánc: %s | forras=%s | ts=%s)*' % (len(kulcs), ', '.join(lanc), forras, ts), '']
    if tanulmany:
        ki += ['A tanulmány adata (nem ismétlődik itt): `%s`.' % tanulmany, '']
    ki += ['## Gyakorisági alapvonal', '',
           '| Strong | szótő | versek a korpuszban | a korpusz versei | arány |', '|---|---|---|---|---|']
    szoto = korp.szoto
    for s in lanc:
        n = korp.n_vers[korp.testamentum(s)]
        db = len(korp.versei.get(s, ()))
        ki.append('| %s | %s | %d | %d | %s |' % (s, szoto.get(s, '–'), db, n, ('%.4f' % (db / n)) if n else '–'))
    ki += ['', '*(proveniencia: scope=a lánc szavai a teljes ÓSZ (H) / ÚSZ (G) táblán, versszám | forras=%s | ts=%s)*'
           % (forras, ts), '', '## Versek', '']
    for k in kulcs:
        allapot, hiv = vers_allapot(mid, k, elof, jelolt, adat)
        ki += ['### %s · %s%s' % (k, allapot, '' if hiv == '–' else ' (%s)' % hiv), '']
        ki += ['Károli: %s' % (adat.karoli.get(k) or '– (a vers nincs a Károli-táblán)'), '']
        sz = korp.szavak.get(k, [])
        if not sz:
            ki += ['A lánc szava nem áll a versben.', '',
                   '*(proveniencia: scope=%s | forras=%s | ts=%s)*' % (k, forras, ts), '']
            continue
        ki += ['| poz. | Strong | alak | szótő | glossza |', '|---|---|---|---|---|']
        for poz, s, al, sz_, gl in sz:
            ki.append('| %d | %s | %s | %s | %s |' % (poz, s, al, sz_, gl))
        ki.append('')
        jelen = []
        for _, s, _, _, _ in sz:
            if s not in jelen:
                jelen.append(s)
        parok = [(a, b) for a, b in itertools.combinations(jelen, 2)]
        if parok:
            ki.append('Együttállás (a korpuszban megfigyelt együttes versszám; a véletlen-alapvonal szerint várt):')
            for a, b in parok:
                v = korp.vart(a, b)
                ki.append('- %s + %s: megfigyelt %d vers; várt %s' % (
                    a, b, korp.egyutt(a, b), ('%.2f' % v) if v is not None else '– (két testamentum)'))
        else:
            ki.append('Együttállás: a versben egy lánc-szó áll.')
        sorozat = [s for _, s, _, _, _ in sz]
        fi = forditott_ismetles(sorozat)
        arany, modszer = forditott_alapvonal(sorozat)
        if fi:
            ki.append('Fordított sorrendű ismétlés (gépi jelölt, versen belül): %s … %s … %s … %s; a sorrend: %s; '
                      'véletlen-alapvonal: %.3f (%s).' % (fi[0], fi[1], fi[1], fi[0], ' '.join(sorozat), arany, modszer))
        else:
            ki.append('Fordított sorrendű ismétlés: nincs (a sorrend: %s).' % ' '.join(sorozat))
        ki += ['', '*(proveniencia: scope=%s, lánc: %s | forras=%s | ts=%s)*' % (k, ', '.join(lanc), forras, ts), '']
    return '\n'.join(ki).rstrip('\n') + '\n'


def lanc_motivumbol(mid, elof_ut=P.T_ELOF):
    ki = []
    for _, d in tsv_sorok(elof_ut):
        if d.get('id') == mid:
            for s in re.split(r'[,;+ ]+', d.get('strong', '')):
                s = P.strong_norm(s)
                if re.match(r'^[HG]\d{4}', s) and s not in ki:
                    ki.append(s)
    return ki


def versek_motivumbol(mid, elof_ut=P.T_ELOF):
    return [d['igehely'] for _, d in tsv_sorok(elof_ut) if d.get('id') == mid and d.get('igehely')]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--motivum', help='motívum-azonosító (a versek állapota és, ha nincs --versek/--lanc, ezek forrása)')
    ap.add_argument('--versek', help='a kulcsversek, „;”-vel elválasztva (pl. "1Móz 3:17; 1Móz 8:21")')
    ap.add_argument('--lanc', help='a lánc szavai, Strong-számok vesszővel (pl. H0779,H0127)')
    ap.add_argument('--tanulmany', help='a tanulmány fájlja, csak hivatkozásként')
    ap.add_argument('--kimenet', help='a kimenet útja (alapértelmezés: stdout)')
    a = ap.parse_args()
    if not a.versek and not a.motivum:
        ap.error('--versek vagy --motivum kell')
    versek = [v.strip() for v in a.versek.split(';') if v.strip()] if a.versek else versek_motivumbol(a.motivum)
    lanc = [P.strong_norm(s.strip()) for s in a.lanc.split(',') if s.strip()] if a.lanc else \
        (lanc_motivumbol(a.motivum) if a.motivum else [])
    if not lanc:
        ap.error('a lánc szavai nem állapíthatók meg: --lanc kell')
    szoveg = keszit(a.motivum, versek, lanc, a.tanulmany)
    if a.kimenet:
        with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('%s: %d vers, %d lánc-szó -> %s' % (a.motivum or 'kézi', len(versek), len(lanc), a.kimenet))
    else:
        sys.stdout.write(szoveg)
    return 0


if __name__ == '__main__':
    sys.exit(main())
