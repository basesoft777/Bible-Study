#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_gyanus_general.py -- a `konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv` előállítása (N-F156a, DT-F156q).

Az ok (a forrás hibája): a HunKar OSIS XML jegyzetei a szentiras.hu/KG-ből származnak, és sok vershez egy másik vers
jegyzete van kötve (pl. Acts.2.18–2.47 = Acts.7.5–7.34 listái, `naplok/N_F156a_jelentes.md`). A főtábla a forráshoz hű
(`eszkozok/karoli_kh_osis_konverzio.py --osszevet`: 0 eltérés), ezért nem javítjuk: ez a fájl a gyanús forrásverseket
sorolja fel; a fogyasztók (`karoli_kh_szuro.py`) kihagyták őket.

ARCHÍV (F177, DT-F177a): a karantén megszűnt. A fogyasztók a MEK 00161 kiadással összevetett, háromszintű
`konkordancia/Karoli_KH_javitott.tsv`-ből szűrnek (`eszkozok/karoli_kh_mek.py osszevet`; a `megerositett` szint jut a
lapra, a `kiesik` és a `jelolt` nem). Ez a szkript és a kimenete archívum: a gyanú-szabály történeti mérése
(a javított tábla `kiesik` szintje a gyanús versek 4 773 / 5 078 részét lefedi); szűrésre nem használandó.

Gyanú-szabály: `eszkozok/karoli_kh_epseg.py` (`gyanus_forrasok`). Ez a szkript a gyanús verseket két osztályba sorolja:
  - `blokk`: legalább 3 gyanús vers azonos könyvben, a gazdájukkal azonos, konstans verssorszám-eltolással (a Karoli_1908.tsv
    kanonikus sorrendjében) — a legerősebb bizonyíték, a véletlen egybeesés elhanyagolható;
  - `egyedi`: nem blokk-tag; a hamis-pozitív kockázat nagyobb.

Használat:
    python eszkozok/karoli_kh_gyanus_general.py [--ki konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv] [--jelentes <md>]
"""
import argparse
import collections
import datetime
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_kh_epseg as E  # noqa: E402

GYOKER = E.GYOKER
KI = 'konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv'
VERS = 'konkordancia/Karoli_1908.tsv'
MIN_BLOKK = 3


def sorszamok():
    """{STEP-vers: kanonikus sorszám} a Karoli_1908.tsv sorrendjéből (a fájl kanonikus sorrendű)."""
    norm = E.hu_step()
    ki = {}
    import re
    for m in E.sorok(VERS):
        r = re.match(r'(\S+) (\d+):(\d+)$', m[0])
        if r and r.group(1) in norm:
            ki.setdefault('%s.%s.%s' % (norm[r.group(1)], r.group(2), r.group(3)), len(ki))
    return ki


def osztalyoz(kh=None, tsk=None):
    """[(forrás, osztály, eltolás, [gazdák])] a kanonikus sorrendben; osztály: 'blokk' | 'egyedi'."""
    if kh is None:
        kh, tsk = E.betolt()
    gy = E.gyanus_forrasok(kh, tsk, reszlista=False)   # archív: a régi (teljes egyezéses) szabály
    sz = sorszamok()
    elt = {}
    for k, gazdak in gy.items():
        ds = sorted({sz[k] - sz[g] for g in gazdak if k in sz and g in sz})
        elt[k] = ds
    csop = collections.defaultdict(set)  # (könyv, gazda-könyv, eltolás) -> {gyanús versek}
    for k, ds in elt.items():
        for g in gy[k]:
            if k in sz and g in sz:
                csop[(E.step_ref(k)[0], E.step_ref(g)[0], sz[k] - sz[g])].add(k)
    blokkos = {}
    for (kk, gk, d), tagok in csop.items():
        if len(tagok) >= MIN_BLOKK:
            for k in tagok:
                blokkos.setdefault(k, d)
    ki = []
    for k in kh:
        if k in gy:
            ki.append((k, 'blokk' if k in blokkos else 'egyedi', blokkos.get(k), gy[k]))
    return ki, csop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki', help='kimeneti TSV (a repó gyökeréhez képest)')
    ap.add_argument('--jelentes', help='blokk-lista Markdown (a repó gyökeréhez képest)')
    a = ap.parse_args()
    kh, tsk = E.betolt()
    lista, csop = osztalyoz(kh, tsk)
    ts = datetime.date.today().isoformat()
    prov = ('scope=konkordancia/Karoli_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_gyanus_general.py'
            ' (karoli_kh_epseg.py szabály, RITKA_STRONG=%d) | ts=%s' % (E.RITKA_STRONG, ts))
    n_blokk = sum(1 for x in lista if x[1] == 'blokk')
    print('gyanús forrásvers: %d; blokk-tag: %d; egyedi: %d; KH-sor: %d'
          % (len(lista), n_blokk, len(lista) - n_blokk, sum(len(kh[x[0]]) for x in lista)))
    if a.ki:
        with open(os.path.join(GYOKER, a.ki), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT: eszkozok/karoli_kh_gyanus_general.py — kézzel szerkeszteni tilos; ok: N-F156a '
                    '(a forrás-XML jegyzetei másik versé), a főtábla nyers-hű\n')
            f.write('# ARCHÍV (F177): a karantén megszűnt; az irányadó tábla a konkordancia/Karoli_KH_javitott.tsv '
                    '(eszkozok/karoli_kh_mek.py osszevet), a karoli_kh_szuro.py abból szűr — ez a fájl csak történeti\n')
            f.write('\t'.join(['forras', 'osztaly', 'blokk_eltolas', 'ok', 'vele_azonos_lista_tamogatott',
                               'kh_lista', 'proveniencia']) + '\n')
            for k, o, d, g in lista:
                f.write('\t'.join([k, o, '' if d is None else str(d),
                                   'masolt_lista_a_forrasban', ' '.join(g), ' '.join(kh[k]), prov]) + '\n')
    if a.jelentes:
        with open(os.path.join(GYOKER, a.jelentes), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT: eszkozok/karoli_kh_gyanus_general.py — kézzel szerkeszteni tilos\n\n')
            f.write('# Konstans eltolású másolat-blokkok (≥%d gyanús vers, azonos könyvpár és eltolás)\n\n' % MIN_BLOKK)
            f.write('*%s*\n\n| gyanús könyv | gazda könyv | eltolás | gyanús versek | tartomány |\n|---|---|---|---|---|\n' % prov)
            sz = sorszamok()
            for (kk, gk, d), tagok in sorted(csop.items(), key=lambda x: -len(x[1])):
                if len(tagok) < MIN_BLOKK:
                    continue
                t = sorted(tagok, key=lambda v: sz[v])
                f.write('| %s | %s | %d | %d | %s – %s |\n' % (kk, gk, d, len(t), t[0], t[-1]))


if __name__ == '__main__':
    main()
