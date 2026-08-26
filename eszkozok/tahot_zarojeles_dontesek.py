#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. lepes (v2): pontosabb csoportositas.
Minden (konyv, primary-fejezet) egy csomopont. Ha egy fejezetben van olyan
sor, aminek secondary fejezete MAS mint a primary fejezet, azt a ket
fejezetet osszekapcsoljuk (union-find) - ez a "hatarelotolodas" eset.
Ha egy fejezetben minden secondary-fejezet == primary-fejezet (csak
vers-szam elteres, pl zsoltarcimek), az onallo csomopont marad.

Minden vegso csoportra (egy vagy tobb fejezet) ket hipotezist teszteluk:
  - primary hipotezis: minden erintett primary-fejezet Karoli-hossza = az adott
    fejezet primary-max-verse-e
  - secondary hipotezis: minden erintett (secondary-fejezetszam alapján
    ujracsoportositott) fejezet Karoli-hossza = a hozzarendelt secondary-max-verse

Kiirja a dontest / NYITOTT-at egy TSV-be, tovabba egy human-readable logot.
"""
import re, csv, sys, os
from collections import defaultdict, OrderedDict

SCRATCH = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = SCRATCH + "/tahot"
RAW_FILES = ["GenDeu.txt", "JosEst.txt", "JobSng.txt", "IsaMal.txt"]
REPO = r"C:\Users\bases\Desktop\Bible-Study"
KAROLI_PATH = REPO + r"\konkordancia\Karoli_1908.tsv"
NORM_PATH = REPO + r"\konkordancia\Konyv_normalizalo_tabla.tsv"

REF_RE = re.compile(r'^([A-Za-z0-9]+)\.(\d+)\.(\d+)(\((\d+)\.(\d+)\))?#(\d+)=')


def load_norm():
    m = {}
    with open(NORM_PATH, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            step, hu, full = row
            m[step] = hu
    return m


def load_karoli_verses():
    verses_seen = defaultdict(set)
    with open(KAROLI_PATH, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            if len(row) < 2:
                continue
            ref = row[0]
            m = re.match(r'^(\S+)\s+(\d+):(\d+)$', ref)
            if not m:
                continue
            book, chap, verse = m.group(1), int(m.group(2)), int(m.group(3))
            verses_seen[(book, chap)].add(verse)
    return verses_seen


def parse_raw_units():
    units = []
    seen = set()
    for fn in RAW_FILES:
        path = os.path.join(RAW_DIR, fn)
        with open(path, encoding='utf-8') as f:
            for line in f:
                fields = line.rstrip('\n').split('\t')
                if not fields:
                    continue
                m = REF_RE.match(fields[0])
                if not m:
                    continue
                book, chap, verse = m.group(1), int(m.group(2)), int(m.group(3))
                chap2, verse2 = m.group(5), m.group(6)
                s_chap = int(chap2) if chap2 else chap
                s_verse = int(verse2) if verse2 else verse
                key = (book, chap, verse, s_chap, s_verse)
                if key in seen:
                    continue
                seen.add(key)
                units.append((book, chap, verse, s_chap, s_verse))
    return units


class DSU:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def main():
    norm = load_norm()
    karoli_verses = load_karoli_verses()
    units = parse_raw_units()

    by_book = defaultdict(list)
    for u in units:
        by_book[u[0]].append(u)

    all_decisions = []  # rows for output tsv

    for book, ulist in by_book.items():
        hu = norm.get(book)
        if hu is None:
            print("HIANYZO KONYV NORMALIZALAS:", book, file=sys.stderr)
            continue

        # per (primary chapter) adatok
        p_chap_data = defaultdict(list)  # p_chap -> list of (p_verse, s_chap, s_verse, has_shift)
        for b, pchap, pverse, schap, sverse in ulist:
            has_shift = (schap != pchap) or (sverse != pverse)
            p_chap_data[pchap].append((pverse, schap, sverse, has_shift))

        # csak azok a fejezetek erdekesek, ahol van tenyleges eltolodas
        shifted_chaps = set(pc for pc, lst in p_chap_data.items() if any(x[3] for x in lst))
        if not shifted_chaps:
            continue

        dsu = DSU()
        for pc in shifted_chaps:
            dsu.find((book, pc))
        # union: ha egy fejezetben van olyan sor, aminek s_chap != p_chap, kosd ossze
        for pc in list(shifted_chaps):
            for pverse, schap, sverse, has_shift in p_chap_data[pc]:
                if schap != pc:
                    dsu.union((book, pc), (book, schap))
                    shifted_chaps.add(schap)
                    if schap not in p_chap_data:
                        # ez a fejezet nem szerepel onallo primary-kent ebben a konyvben
                        # (pl. Hebrew-only tobbfejezetes eltolodas) - ritka, kezeljuk ures listaval
                        p_chap_data[schap] = p_chap_data.get(schap, [])

        groups = defaultdict(set)
        for pc in shifted_chaps:
            groups[dsu.find((book, pc))].add(pc)

        for root, chap_set in groups.items():
            chap_list = sorted(chap_set)
            # primary hipotezis: minden fejezet karoli-max = sajat primary-max-verse
            primary_ok = True
            primary_detail = {}
            for pc in chap_list:
                lst = p_chap_data.get(pc, [])
                if not lst:
                    # ez a fejezet csak secondary-kent letezik (pl. Jol.4) - primary
                    # hipotezis alatt egyszeruen nem letezik, nem bukas
                    continue
                pmax = max(x[0] for x in lst)
                kmax = max(karoli_verses.get((hu, pc), set()), default=None)
                primary_detail[pc] = (pmax, kmax)
                if kmax is None or kmax != pmax:
                    primary_ok = False

            # secondary hipotezis: verseket a SECONDARY fejezetszam szerint csoportositva,
            # az adott secondary fejezet karoli-max-a egyezzen a secondary-max-verse-el
            s_chap_verses = defaultdict(list)
            for pc in chap_list:
                for pverse, schap, sverse, has_shift in p_chap_data.get(pc, []):
                    s_chap_verses[schap].append(sverse)
            secondary_ok = True
            secondary_detail = {}
            for sc, vlist in s_chap_verses.items():
                smax = max(vlist)
                kmax = max(karoli_verses.get((hu, sc), set()), default=None)
                secondary_detail[sc] = (smax, kmax)
                if kmax is None or kmax != smax:
                    secondary_ok = False

            if primary_ok and not secondary_ok:
                decision = "ELSODLEGES"
            elif secondary_ok and not primary_ok:
                decision = "MASODLAGOS"
            elif primary_ok and secondary_ok:
                decision = "TARTALMI_ELLENORZES_SZUKSEGES(mindketto_egyezik)"
            else:
                decision = "TARTALMI_ELLENORZES_SZUKSEGES(egyik_sem_egyezik)"

            all_decisions.append({
                'book': book, 'hu': hu, 'chapters': chap_list,
                'decision': decision,
                'primary_detail': primary_detail,
                'secondary_detail': secondary_detail,
            })

    # kiiras
    with open(SCRATCH + "/step1_decisions.tsv", 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['Konyv', 'Magyar', 'Fejezetek', 'Dontes', 'Primary_reszletek', 'Secondary_reszletek'])
        for d in all_decisions:
            w.writerow([
                d['book'], d['hu'], ','.join(map(str, d['chapters'])), d['decision'],
                str(d['primary_detail']), str(d['secondary_detail'])
            ])

    n_auto = sum(1 for d in all_decisions if d['decision'] in ('ELSODLEGES', 'MASODLAGOS'))
    n_manual = len(all_decisions) - n_auto
    print(f"Osszes eltolodasi csoport: {len(all_decisions)}  auto-eldontott: {n_auto}  kezi/NYITOTT: {n_manual}", file=sys.stderr)


if __name__ == '__main__':
    main()
