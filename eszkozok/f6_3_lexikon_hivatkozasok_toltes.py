#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f6_3_lexikon_hivatkozasok_toltes.py — F6_BRIEF.md F6.3 tétel.

Öt jelentés-hivatkozás sort ír az `adat/lexikon_hivatkozasok.tsv`-be, a
`konkordancia/BDB_teljes_unabridged.tsv` és a `konkordancia/TBESG.txt`
forrássoraiból kinyert, szó szerinti kivonatokkal. A `szoveg_en` minden
sorban a forrásfájl megfelelő sorának szó szerinti részlete — a szkript
ellenőrzi, hogy valóban részsztring, és megáll, ha nem az.

A három fordítás (`forditas_hu`) a `motivumlog/lexikon_pilot/
ISTENTISZT-001_TUDOMANYOS.md` pilot-sorszámaiból jön (1-alapú, a
`cb4aac3`-beli állapot szerint). A szkript ellenőrzi, hogy a 184. sor
`**🇭🇺 Magyarul:** `-lal, a 232. `**1.**`-gyel, a 234. `**2.`-vel kezdődik,
és eltérésnél megáll.

I/O — sima split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md).

Futtatás a repó gyökeréből:
    python eszkozok/f6_3_lexikon_hivatkozasok_toltes.py         # szárazon
    python eszkozok/f6_3_lexikon_hivatkozasok_toltes.py --ir    # ténylegesen ír
"""

import hashlib
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')

LEXIKON_HIVATKOZASOK = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
BDB_FAJL = os.path.join(KONKORDANCIA, 'BDB_teljes_unabridged.tsv')
TBESG_FAJL = os.path.join(KONKORDANCIA, 'TBESG.txt')
PILOT_FAJL = os.path.join(ROOT, 'motivumlog', 'lexikon_pilot', 'ISTENTISZT-001_TUDOMANYOS.md')

HEADER = ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forditas_hu', 'forrasfajl']


def bdb_teljes_szocikk(strong):
    with io.open(BDB_FAJL, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith(strong + '\t'):
                return sor.rstrip('\n').split('\t')[2]
    raise ValueError('nincs BDB-sor: %s' % strong)


def tbesg_utolso_mezo(strong):
    with io.open(TBESG_FAJL, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith(strong + '\t'):
                return sor.rstrip('\n').split('\t')[-1]
    raise ValueError('nincs TBESG-sor: %s' % strong)


def pilot_sorok():
    with io.open(PILOT_FAJL, encoding='utf-8') as f:
        return f.read().split('\n')


def h7121_2c():
    text = bdb_teljes_szocikk('H7121')
    idx_callwith = text.find('call with name of')
    idx_c = text.rfind('c. ', 0, idx_callwith)
    idx_d_late = text.find(' d. late,')
    if idx_callwith < 0 or idx_c < 0 or idx_d_late < 0:
        raise ValueError('H7121 2.c horgony nem található')
    return text[idx_c:idx_d_late]


def h7121_3():
    text = bdb_teljes_szocikk('H7121')
    idx_3 = text.find('3 proclaim:')
    idx_b = text.find(' b. ', idx_3)
    if idx_3 < 0 or idx_b < 0:
        raise ValueError('H7121 3 horgony nem található')
    return text[idx_3:idx_b]


def h3548_1():
    text = bdb_teljes_szocikk('H3548')
    idx_1 = text.find('1 priest-king:')
    idx_2 = text.find(' 2 ', idx_1)
    if idx_1 < 0 or idx_2 < 0:
        raise ValueError('H3548 1 horgony nem található')
    return text[idx_1:idx_2]


def g1941_szegmensek():
    raw = tbesg_utolso_mezo('G1941')
    cleaned = re.sub(r'<[^>]+>', ' ', raw)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    parts = re.split(r'\s*__(\d+)\.\s*', cleaned)
    szegmensek = {}
    i = 1
    while i < len(parts):
        szam = parts[i]
        szoveg = parts[i + 1] if i + 1 < len(parts) else ''
        szegmensek[szam] = szoveg.strip()
        i += 2
    if '1' not in szegmensek or '2' not in szegmensek:
        raise ValueError('G1941 1/2 szegmens nem található')
    return szegmensek['1'], szegmensek['2']


def pilot_sor_forditas(sorszam_1_alapu, vart_elotag, level_prefix=None):
    sorok = pilot_sorok()
    sor = sorok[sorszam_1_alapu - 1]
    if not sor.startswith(vart_elotag):
        raise ValueError(
            'a pilot %d. sora nem "%s"-lal/vel kezdődik: %r'
            % (sorszam_1_alapu, vart_elotag, sor[:40])
        )
    if level_prefix:
        return sor[len(level_prefix):]
    return sor


def epit_sorok():
    g1_seg1, g1_seg2 = g1941_szegmensek()

    sorok = [
        {
            'strong': 'H7121', 'szotar': 'BDB', 'entry_id': 'H7121', 'jelentes_szam': '2.c',
            'szoveg_en': h7121_2c(),
            'forditas_hu': pilot_sor_forditas(184, '**🇭🇺 Magyarul:** ', level_prefix='**🇭🇺 Magyarul:** '),
            'forrasfajl': 'konkordancia/BDB_teljes_unabridged.tsv',
        },
        {
            'strong': 'H7121', 'szotar': 'BDB', 'entry_id': 'H7121', 'jelentes_szam': '3',
            'szoveg_en': h7121_3(),
            'forditas_hu': '',
            'forrasfajl': 'konkordancia/BDB_teljes_unabridged.tsv',
        },
        {
            'strong': 'H3548', 'szotar': 'BDB', 'entry_id': 'H3548', 'jelentes_szam': '1',
            'szoveg_en': h3548_1(),
            'forditas_hu': '',
            'forrasfajl': 'konkordancia/BDB_teljes_unabridged.tsv',
        },
        {
            'strong': 'G1941', 'szotar': 'TBESG', 'entry_id': 'G1941', 'jelentes_szam': '1',
            'szoveg_en': g1_seg1,
            'forditas_hu': pilot_sor_forditas(232, '**1.**'),
            'forrasfajl': 'konkordancia/TBESG.txt',
        },
        {
            'strong': 'G1941', 'szotar': 'TBESG', 'entry_id': 'G1941', 'jelentes_szam': '2',
            'szoveg_en': g1_seg2,
            'forditas_hu': pilot_sor_forditas(234, '**2.'),
            'forrasfajl': 'konkordancia/TBESG.txt',
        },
    ]

    for sor in sorok:
        forras_szoveg = (
            bdb_teljes_szocikk(sor['entry_id']) if sor['szotar'] == 'BDB'
            else tbesg_utolso_mezo(sor['entry_id'])
        )
        if sor['szotar'] == 'TBESG':
            forras_szoveg_normalizalt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', forras_szoveg)).strip()
        else:
            forras_szoveg_normalizalt = forras_szoveg
        if sor['szoveg_en'] not in forras_szoveg_normalizalt:
            raise ValueError(
                '%s %s %s: a szoveg_en nem részsztringje a forrásnak'
                % (sor['strong'], sor['szotar'], sor['jelentes_szam'])
            )
        for mezo in ('strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forditas_hu', 'forrasfajl'):
            if '\t' in sor[mezo] or '\n' in sor[mezo]:
                raise ValueError('%s mező tab/newline karaktert tartalmaz' % mezo)

    return sorok


def main():
    ir = '--ir' in sys.argv

    with io.open(LEXIKON_HIVATKOZASOK, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    nyers_sorok = nyers.split(sorveg)
    if nyers_sorok and nyers_sorok[-1] == '':
        nyers_sorok = nyers_sorok[:-1]

    komment_sorok = [s for s in nyers_sorok if s.startswith('#')]
    fejlec_idx = next(i for i, s in enumerate(nyers_sorok) if s and not s.startswith('#'))
    fejlec = nyers_sorok[fejlec_idx].split('\t')
    if fejlec != HEADER:
        print('HIBA: a fejléc nem egyezik a várttal.', file=sys.stderr)
        return 1

    meglevo_adatsorok = [
        s for s in nyers_sorok[fejlec_idx + 1:] if s.strip() and not s.startswith('#')
    ]
    if meglevo_adatsorok:
        print('HIBA: a lexikon_hivatkozasok.tsv nem üres — a szkript csak első feltöltésre készült.',
              file=sys.stderr)
        return 1

    uj_sorok = epit_sorok()

    tabla_sorok = [komment_sorok[0], '\t'.join(HEADER)]
    for sor in uj_sorok:
        tabla_sorok.append('\t'.join(sor[mezo] for mezo in HEADER))

    body = '\n'.join(tabla_sorok[1:]) + '\n'
    sha = hashlib.sha256(body.encode('utf-8')).hexdigest()

    print('Új adatsorok: %d' % len(uj_sorok))
    for sor in uj_sorok:
        print('  %s %s %s %s — szoveg_en %d kar., forditas_hu %s'
              % (sor['strong'], sor['szotar'], sor['entry_id'], sor['jelentes_szam'],
                 len(sor['szoveg_en']), 'kitöltve' if sor['forditas_hu'] else 'üres'))
    print('SHA-256 (fejléc + adatsorok, # nélkül):', sha)

    if not ir:
        print('Szárazon futott. Tényleges íráshoz: --ir')
        return 0

    with io.open(LEXIKON_HIVATKOZASOK, 'w', encoding='utf-8', newline='\n') as f:
        for sor in tabla_sorok:
            f.write(sor + '\n')
    print('Megírva: adat/lexikon_hivatkozasok.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
