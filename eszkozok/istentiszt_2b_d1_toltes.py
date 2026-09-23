#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
istentiszt_2b_d1_toltes.py -- ISTENTISZT_2B_ADATOSITAS.md D1 tetel.

Hat uj sort ir az `adat/lexikon_hivatkozasok.tsv`-be, a
`lexikon/ISTENTISZT-001_TUDOMANYOS.md` 2/b szakaszabol szkriptesen
kinyert, szo szerinti `szoveg_en`/`forditas_hu` ertekekkel (a szoveget
NEM gepeljuk at). A 4. sor (Thayer G0994) `szoveg_en` mezoje kivetel:
az a `konkordancia/Thayer_teljes.tsv` G0994 sorabol jon, szo szerint
(nem a 2/b roviditett idezetebol).

I/O -- sima split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md).

Futtatas a repo gyokerebol:
    python eszkozok/istentiszt_2b_d1_toltes.py         # szarazon
    python eszkozok/istentiszt_2b_d1_toltes.py --ir    # tenylegesen ir
"""

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
LEXIKON = os.path.join(ROOT, 'lexikon')

LEXIKON_HIVATKOZASOK = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
THAYER_FAJL = os.path.join(KONKORDANCIA, 'Thayer_teljes.tsv')
OLDAL_FAJL = os.path.join(LEXIKON, 'ISTENTISZT-001_TUDOMANYOS.md')

HEADER = ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forditas_hu', 'forrasfajl']


def oldal_sorai():
    with io.open(OLDAL_FAJL, encoding='utf-8') as f:
        return f.read().split('\n')


def blokkot_kivag(sorok, kezdet_minta, veg_minta):
    """[kezdet_minta, veg_minta) kozotti sorok -- kezdet_minta azon sora,
    amely azzal a szoveggel KEZDODIK; veg_minta az elso olyan sor, amely
    azzal kezdodik, es a kezdet UTAN all."""
    kezdet_idx = None
    for i, s in enumerate(sorok):
        if s.startswith(kezdet_minta):
            kezdet_idx = i
            break
    if kezdet_idx is None:
        raise ValueError('nincs ilyen kezdet a lexikon-oldalon: %r' % kezdet_minta)
    veg_idx = None
    for i in range(kezdet_idx + 1, len(sorok)):
        if sorok[i].startswith(veg_minta):
            veg_idx = i
            break
    if veg_idx is None:
        raise ValueError('nincs ilyen veg a lexikon-oldalon %r utan: %r' % (kezdet_minta, veg_minta))
    return sorok[kezdet_idx:veg_idx]


def idezet_kivon(blokk_sorok):
    """A `>` kezdetu sorok, a jel es az egy-szokoz nelkuli osszefuzes:
    minden sor `> ` (vagy `>`) levagva, majd szokozzel osszefuzve."""
    idezet_sorok = [s for s in blokk_sorok if s.startswith('>')]
    if not idezet_sorok:
        raise ValueError('nincs `>` idezet a blokkban')
    darabok = []
    for s in idezet_sorok:
        d = s[1:]
        if d.startswith(' '):
            d = d[1:]
        darabok.append(d)
    return ' '.join(darabok).strip()


def magyarul_kivon(blokk_sorok, cimke_minta):
    """A `**🇭🇺 Magyarul (...):**` (vagy `**🇭🇺**`) kezdetu sor, a cimke
    levagva."""
    for s in blokk_sorok:
        if s.startswith(cimke_minta):
            return s[len(cimke_minta):].strip()
    raise ValueError('nincs %r kezdetu sor a blokkban' % cimke_minta)


def thayer_teljes_szocikk(strong_eredeti):
    with io.open(THAYER_FAJL, encoding='utf-8') as f:
        header = f.readline().rstrip('\n').split('\t')
        idx_eredeti = header.index('Strong_eredeti')
        idx_szocikk = header.index('Teljes_szocikk')
        for sor in f:
            cols = sor.rstrip('\n').split('\t')
            if cols[idx_eredeti] == strong_eredeti:
                return cols[idx_szocikk]
    raise ValueError('nincs Thayer-sor: %s' % strong_eredeti)


def epit_sorok():
    oldal = oldal_sorai()
    sorok = []

    # 1. BDB H8034 -- "3. TELJES BDB szocikk -- H8034" blokk
    blokk = blokkot_kivag(oldal, '#### 3. TELJES BDB szócikk', '---')
    szoveg_en = idezet_kivon(blokk)
    forditas_hu = magyarul_kivon(blokk, '**🇭🇺 Magyarul (BDB):** ')
    sorok.append({
        'strong': 'H8034', 'szotar': 'BDB', 'entry_id': 'H8034', 'jelentes_szam': 'részlet',
        'szoveg_en': szoveg_en, 'forditas_hu': forditas_hu,
        'forrasfajl': 'konkordancia/BDB_teljes_unabridged.tsv',
    })

    # 2. TBESG G2564 -- "##### G2564 καλέω (kaleō)" blokk
    blokk = blokkot_kivag(oldal, '##### G2564 καλέω', '##### G0994')
    szoveg_en = idezet_kivon(blokk)
    forditas_hu = magyarul_kivon(blokk, '**🇭🇺 Magyarul (Abbott-Smith):** ')
    sorok.append({
        'strong': 'G2564', 'szotar': 'TBESG', 'entry_id': 'G2564', 'jelentes_szam': 'részlet',
        'szoveg_en': szoveg_en, 'forditas_hu': forditas_hu,
        'forrasfajl': 'konkordancia/TBESG.txt',
    })

    # 3. TBESG G0994 -- "##### G0994 βοάω (boaō)" blokk, a "TBESG (Abbott-Smith):" alblokkja
    blokk = blokkot_kivag(oldal, '##### G0994 βοάω', "**Thayer's Greek-English Lexicon (2026.09.07")
    szoveg_en = idezet_kivon(blokk)
    forditas_hu = magyarul_kivon(blokk, '**🇭🇺 Magyarul (Abbott-Smith):** ')
    sorok.append({
        'strong': 'G0994', 'szotar': 'TBESG', 'entry_id': 'G0994', 'jelentes_szam': 'részlet',
        'szoveg_en': szoveg_en, 'forditas_hu': forditas_hu,
        'forrasfajl': 'konkordancia/TBESG.txt',
    })

    # 4. Thayer G0994 -- szoveg_en a Thayer_teljes.tsv-bol, forditas_hu ures
    szoveg_en = thayer_teljes_szocikk('G994')
    sorok.append({
        'strong': 'G0994', 'szotar': 'Thayer', 'entry_id': 'G994', 'jelentes_szam': 'teljes',
        'szoveg_en': szoveg_en, 'forditas_hu': '',
        'forrasfajl': 'konkordancia/Thayer_teljes.tsv',
    })

    # 5. TBESH H7121 -- "TBESH.lexicon (SQLite, konszolidalt verzio)" blokk
    blokk = blokkot_kivag(oldal, '**TBESH.lexicon', '**SECE H7121')
    szoveg_en = idezet_kivon(blokk)
    forditas_hu = magyarul_kivon(blokk, '**🇭🇺 Magyarul (TBESH):** ')
    sorok.append({
        'strong': 'H7121', 'szotar': 'TBESH', 'entry_id': 'H7121', 'jelentes_szam': 'részlet',
        'szoveg_en': szoveg_en, 'forditas_hu': forditas_hu,
        'forrasfajl': 'konkordancia/TBESH.txt',
    })

    # 6. LSJ G2564 -- "LSJ (Liddell-Scott-Jones) -- kaleo (kaleo) teljes klasszikus szocikke" blokk
    blokk = blokkot_kivag(oldal, '**LSJ (Liddell-Scott-Jones)', '**Jelentősége:**')
    szoveg_en = idezet_kivon(blokk)
    forditas_hu = magyarul_kivon(blokk, '**🇭🇺 Magyarul (LSJ):** ')
    sorok.append({
        'strong': 'G2564', 'szotar': 'LSJ', 'entry_id': 'G2564', 'jelentes_szam': 'részlet',
        'szoveg_en': szoveg_en, 'forditas_hu': forditas_hu,
        'forrasfajl': 'konkordancia/LSJ_teljes.tsv',
    })

    for sor in sorok:
        for mezo in HEADER:
            if '\t' in sor[mezo] or '\n' in sor[mezo]:
                raise ValueError('%s %s %s mező tab/newline karaktert tartalmaz' % (sor['strong'], sor['szotar'], mezo))

    return sorok


def main():
    ir = '--ir' in sys.argv

    with io.open(LEXIKON_HIVATKOZASOK, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    nyers_sorok = nyers.split(sorveg)
    if nyers_sorok and nyers_sorok[-1] == '':
        nyers_sorok = nyers_sorok[:-1]

    komment_sor = nyers_sorok[0]
    fejlec = nyers_sorok[1].split('\t')
    if fejlec != HEADER:
        print('HIBA: a fejléc nem egyezik a várttal.', file=sys.stderr)
        return 1

    meglevo_kulcsok = set()
    for s in nyers_sorok[2:]:
        if not s.strip():
            continue
        cols = s.split('\t')
        meglevo_kulcsok.add((cols[1], cols[0], cols[2], cols[3]))

    uj_sorok = epit_sorok()

    for sor in uj_sorok:
        kulcs = (sor['szotar'], sor['strong'], sor['entry_id'], sor['jelentes_szam'])
        if kulcs in meglevo_kulcsok:
            print('HIBA: a sor már létezik: %r' % (kulcs,), file=sys.stderr)
            return 1

    print('Új adatsorok: %d' % len(uj_sorok))
    for sor in uj_sorok:
        print('  %s %s %s %s — szoveg_en %d kar., forditas_hu %s'
              % (sor['strong'], sor['szotar'], sor['entry_id'], sor['jelentes_szam'],
                 len(sor['szoveg_en']), ('%d kar.' % len(sor['forditas_hu'])) if sor['forditas_hu'] else 'üres (fordítás függőben)'))

    if not ir:
        print('Szárazon futott. Tényleges íráshoz: --ir')
        return 0

    uj_tabla_sorok = nyers_sorok + ['\t'.join(sor[mezo] for mezo in HEADER) for sor in uj_sorok]
    with io.open(LEXIKON_HIVATKOZASOK, 'w', encoding='utf-8', newline='\n') as f:
        for sor in uj_tabla_sorok:
            f.write(sor + '\n')
    print('Megírva: adat/lexikon_hivatkozasok.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
