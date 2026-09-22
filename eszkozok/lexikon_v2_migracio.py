#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lexikon_v2_migracio.py — LEXV2_2_BRIEF.md V2.5: meglévő lexikon-oldal (v1
szerkezet) migrálása az új v2 vázra.

A régi fájlból kiolvassa a KÉZI szakaszokat a régi címek alapján
(atomikus, a heading sorától a következő azonos-vagy-sekélyebb szintű
headingig terjedő szövegdarabként — HEADING-gel együtt, változatlanul),
majd a `lexikon_general.py` GENERÁLT blokkjaival együtt felépíti az új
vázat, a G1 szerinti helyre illesztve a kézi darabokat.

Önellenőrzés: minden áthelyezett kézi darab bájtra azonos a régi és az
új fájlban — eltérésnél a szkript hibakóddal lép ki, ÍRÁS NÉLKÜL.

`--proba`: a `generalt_proba/lexikon/` alá ír, nem az éles `lexikon/`-ba.

TSV-olvasás kizárólag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import argparse
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import general as G
import lexikon_general as LG

ROOT = G.ROOT
LEXIKON_DIR = os.path.join(ROOT, 'lexikon')
PROBA_DIR = os.path.join(ROOT, 'generalt_proba', 'lexikon')

HEADING_RE = re.compile(r'^(#{1,6})\s')

# (kulcs, cím-minta regex, szint) -- a régi v1 fájl kézi szakaszai, a
# CÍMSOR-ral együtt, VÁLTOZATLANUL emelve át.
KEZI_SZAKASZOK = [
    ('pardes_keretrendszer', re.compile(r'^## 1/b\. PaRDeS keretrendszer \*\(kézi\)\*\s*$'), 2),
    ('teljes_szotari_anyag', re.compile(r'^### 2/b\..*\*\(kézi\)\*\s*$'), 3),
    ('miert_fontos', re.compile(r'^### Miért fontos ez a lelet \*\(kézi\)\*\s*$'), 3),
    ('minosites', re.compile(r'^### Minősítés \*\(kézi\)\*\s*$'), 3),
    ('alatamasztas', re.compile(r'^### Alátámasztás \*\(kézi\)\*\s*$'), 3),
    ('modszertani_naplo', re.compile(r'^## 6\. Módszertani napló \*\(kézi\)\*\s*$'), 2),
    ('uj_felismeres', re.compile(r'^## 7\. ÚJ FELISMERÉS \*\(kézi, ha van\)\*\s*$'), 2),
    ('nyitott_kerdesek', re.compile(r'^## 8\. Nyitott kérdések és séma-korlátok \*\(kézi\)\*\s*$'), 2),
]


def _sorok(szoveg):
    return szoveg.split('\n')


def kezi_darabok_kiolvasasa(regi_szoveg):
    """{kulcs: (cimsor, torzs)} -- a torzs a cimsor UTÁNI szöveg, a
    darab végéig (a cimsor NÉLKÜL); a teljes darab (cimsor+torzs)
    változatlanul rekonstruálható '\\n'.join([cimsor, torzs])-ként, ha
    torzs nem üres, egyébként maga a cimsor."""
    sorok = _sorok(regi_szoveg)
    ki = {}
    for kulcs, cim_re, szint in KEZI_SZAKASZOK:
        kezd = None
        for i, sor in enumerate(sorok):
            if cim_re.match(sor):
                kezd = i
                break
        if kezd is None:
            continue
        veg = len(sorok)
        for j in range(kezd + 1, len(sorok)):
            m = HEADING_RE.match(sorok[j])
            if m and len(m.group(1)) <= szint:
                veg = j
                break
        cimsor = sorok[kezd]
        torzs = '\n'.join(sorok[kezd + 1:veg]).strip('\n')
        ki[kulcs] = (cimsor, torzs)
    return ki


def _darab_szoveg(darab):
    """A (cimsor, torzs) párból a teljes, eredeti darab-szöveg (cimsor +
    üres sor + törzs, ha a törzs nem üres; egyébként csak a cimsor)."""
    if darab is None:
        return None
    cimsor, torzs = darab
    if torzs.strip():
        return cimsor + '\n\n' + torzs
    return cimsor


def _van_tartalom(darab):
    return darab is not None and darab[1].strip() != ''


# V2.6a pont 1: az áthelyezett kézi szakaszok címét a migráció egy
# szinttel lejjebb teszi és a régi számot elhagyja -- csak azoknál a
# szakaszoknál, amelyek egy ÚJ, összevont cím alá kerülnek (6. Értelmezés,
# 7. Módszertan és nyitott kérdések). A G11 a szakasztörzsre vonatkozik
# (bájtra azonos); a CÍM ezeknél a szakaszoknál szándékosan változik.
UJ_CIM = {
    'pardes_keretrendszer': '### PaRDeS keretrendszer',
    'uj_felismeres': '### Új felismerés',
    'modszertani_naplo': '### Módszertani napló',
    'nyitott_kerdesek': '### Nyitott kérdések és séma-korlátok',
}

_KEZI_SUFFIX_RE = re.compile(r'\s*\*\(kézi[^)]*\)\*\s*$')


def demote_body_headings(torzs):
    """Minden # -kezdetű sor eggyel mélyebb szintre kerül (### -> ####,
    stb.) -- az összevont szakasz alá kerülő törzs belső headingjeihez."""
    sorok = torzs.split('\n')
    return '\n'.join(('#' + sor) if HEADING_RE.match(sor) else sor for sor in sorok)


def undemote_body_headings(torzs):
    sorok = torzs.split('\n')
    return '\n'.join((sor[1:] if HEADING_RE.match(sor) else sor) for sor in sorok)


def _darab_uj_cimmel(darabok, kulcs):
    """(uj_szoveg_resz, ellenorzo_fv) -- a demótált cím+törzs darab, és egy
    függvény, ami True-t ad, ha a kapott (regi_torzs) visszaadja a
    demótált törzset (fordítva)."""
    darab = darabok.get(kulcs)
    if not _van_tartalom(darab):
        return None, None
    _regi_cimsor, torzs = darab
    demotalt_torzs = demote_body_headings(torzs)
    uj_cim = UJ_CIM[kulcs]
    resz = uj_cim + '\n\n' + demotalt_torzs
    return resz, demotalt_torzs


def ertelmezes_szoveg(darabok, cimvaltasok):
    reszek = []
    for kulcs in ('pardes_keretrendszer', 'uj_felismeres'):
        resz, demotalt_torzs = _darab_uj_cimmel(darabok, kulcs)
        if resz is None:
            continue
        reszek.append(resz)
        regi_cimsor = darabok[kulcs][0]
        cimvaltasok.append((kulcs, regi_cimsor, UJ_CIM[kulcs]))
    if not reszek:
        return '*Kézzel írandó — a forrás-study PaRDeS keretrendszere, bővítve a lexikai leletekkel.*'
    return '\n\n'.join(reszek)


def modszertan_szoveg(darabok, cimvaltasok):
    reszek = []
    for kulcs in ('modszertani_naplo', 'nyitott_kerdesek'):
        resz, _demotalt_torzs = _darab_uj_cimmel(darabok, kulcs)
        if resz is None:
            continue
        reszek.append(resz)
        regi_cimsor = darabok[kulcs][0]
        cimvaltasok.append((kulcs, regi_cimsor, UJ_CIM[kulcs]))
    if not reszek:
        return '*Kézzel írandó.*'
    return '\n\n'.join(reszek)


def teljesbszotar_szoveg(darabok, alapertelmezett, cimvaltasok):
    """2/b: a generikus '### 2/b *(kézi, ha van)*' helyőrző CSAK akkor
    marad, ha nincs valódi kézi 2/b -- ha van, a régi cím marad, csak a
    '*(kézi...)*' jelölés esik le (nincs számváltás, nincs demótálás,
    mert a szint nem változik)."""
    darab = darabok.get('teljes_szotari_anyag')
    if not _van_tartalom(darab):
        return alapertelmezett
    regi_cimsor, torzs = darab
    uj_cim = _KEZI_SUFFIX_RE.sub('', regi_cimsor)
    cimvaltasok.append(('teljes_szotari_anyag', regi_cimsor, uj_cim))
    return uj_cim + '\n\n' + torzs


def torzs_szoveg(darabok, kulcs, alapertelmezett):
    """Csak a törzs (cím nélkül) -- azokhoz az 1:1 megfeleltetésű
    szakaszokhoz, ahol az új váz saját címe SZÓ SZERINT megegyezik a
    régivel (Miért fontos ez a lelet / Minősítés / Alátámasztás) -- a régi
    cím újra kiírása duplázná a címet."""
    darab = darabok.get(kulcs)
    if darab is None:
        return alapertelmezett
    _cimsor, torzs = darab
    return torzs if torzs.strip() else alapertelmezett


def onellenorzes(regi_szoveg, uj_szoveg, darabok):
    """Szakaszonkénti hitelesség-ellenőrzés: a torzs (cím nélkül) mindig
    bájtra azonosan kell megtaláljon (demótált alakban a demótált
    szakaszoknál, változatlanul a többinél) -- a CÍM ezeknél a
    szakaszoknál szándékosan más (l. UJ_CIM), ezért a cím NEM kerül
    összevetésre. Hibalistát ad vissza."""
    hibak = []
    for kulcs, _cim_re, _szint in KEZI_SZAKASZOK:
        darab = darabok.get(kulcs)
        if not _van_tartalom(darab):
            continue
        _regi_cimsor, torzs = darab

        if kulcs in UJ_CIM:
            elvart_torzs = demote_body_headings(torzs)
            if undemote_body_headings(elvart_torzs) != torzs:
                hibak.append('%s: a demótálás nem fordítható vissza hibátlanul' % kulcs)
        else:
            elvart_torzs = torzs

        if elvart_torzs not in uj_szoveg:
            hibak.append('%s: a kézi szakasztörzs nem található meg (bájtra azonosan) az új fájlban' % kulcs)
        if torzs not in regi_szoveg:
            hibak.append('%s: a kézi szakasztörzs (önellenőrzési hiba: nem is volt a régiben?)' % kulcs)
    return hibak


def epit_uj_fajl_migralva(m, blokkok, darabok):
    """A Kivonat szakaszra a régi v1 fájlban nincs megfelelő -- ott a
    generátor alapértelmezett placeholdere marad (G11: a migráció nem
    talál ki kézi szöveget, ahol nem volt). Visszaad: (uj_szoveg,
    cimvaltasok) -- a cimvaltasok [(kulcs, regi_cim, uj_cim), ...]."""
    cimvaltasok = []
    szoveg = (LG.VAZ_SABLON % {
        'id': m['id'],
        'cim': m.get('cim', ''),
        'tartalom': blokkok['tartalom'],
        'jelmagyarazat': blokkok['jelmagyarazat'],
        'elofordulasok': blokkok['elofordulasok'],
        'kizart': blokkok['kizart'],
        'szocikkek': blokkok['szocikkek'],
        'lxx': blokkok['lxx'],
        'kereszthivatkozasok': blokkok['kereszthivatkozasok'],
        'kapcsolatok': blokkok['kapcsolatok'],
        'idezes': blokkok['idezes'],
        'kolofon': blokkok['kolofon'],
    }).replace(
        '### 2/b *(kézi, ha van)*\n\n*Kézzel írandó, ha van.*',
        teljesbszotar_szoveg(darabok, '### 2/b *(kézi, ha van)*\n\n*Kézzel írandó, ha van.*', cimvaltasok)
    ).replace(
        '### Miért fontos ez a lelet *(kézi)*\n\n*Kézzel írandó.*',
        '### Miért fontos ez a lelet *(kézi)*\n\n' + torzs_szoveg(darabok, 'miert_fontos', '*Kézzel írandó.*')
    ).replace(
        '### Minősítés *(kézi)*\n\n*Kézzel írandó: független megerősítés / új találat / nem releváns.*',
        '### Minősítés *(kézi)*\n\n' + torzs_szoveg(
            darabok, 'minosites', '*Kézzel írandó: független megerősítés / új találat / nem releváns.*')
    ).replace(
        '### Alátámasztás *(kézi)*\n\n*Kézzel írandó.*',
        '### Alátámasztás *(kézi)*\n\n' + torzs_szoveg(darabok, 'alatamasztas', '*Kézzel írandó.*')
    ).replace(
        '## 6. Értelmezés *(kézi)*\n\n*Kézzel írandó — a forrás-study PaRDeS keretrendszere, '
        'bővítve a lexikai leletekkel.*',
        '## 6. Értelmezés *(kézi)*\n\n' + ertelmezes_szoveg(darabok, cimvaltasok)
    ).replace(
        '## 7. Módszertan és nyitott kérdések *(kézi)*\n\n*Kézzel írandó.*',
        '## 7. Módszertan és nyitott kérdések *(kézi)*\n\n' + modszertan_szoveg(darabok, cimvaltasok)
    )
    return szoveg, cimvaltasok


def migral_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek, regi_ut, celkonyvtar):
    with io.open(regi_ut, encoding='utf-8', newline='') as f:
        regi_szoveg = f.read()

    darabok = kezi_darabok_kiolvasasa(regi_szoveg)
    blokkok, _tisztazatlan = LG.render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek)
    uj_szoveg, cimvaltasok = epit_uj_fajl_migralva(m, blokkok, darabok)

    hibak = onellenorzes(regi_szoveg, uj_szoveg, darabok)
    if hibak:
        return None, darabok, cimvaltasok, hibak

    cel_ut = os.path.join(celkonyvtar, '%s_TUDOMANYOS.md' % m['id'])
    os.makedirs(celkonyvtar, exist_ok=True)
    with io.open(cel_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(uj_szoveg)
    return cel_ut, darabok, cimvaltasok, []


def main():
    parser = argparse.ArgumentParser(description='LEXV2_2_BRIEF.md V2.5 -- lexikon-oldal v1 -> v2 migráció')
    parser.add_argument('--proba', action='store_true', help='generalt_proba/lexikon/ alá ír (éles helyett)')
    parser.add_argument('--id', help='csak egy motívum-ID migrálása')
    args = parser.parse_args()

    celkonyvtar = PROBA_DIR if args.proba else LEXIKON_DIR

    _, motivumok = G.tsv_beolvas(G.MOTIVUMOK_TSV)
    _, elofordulasok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
    if args.id:
        motivumok = [x for x in motivumok if x['id'] == args.id]
    konyv_sorrend = G.konyv_sorrend_betolt()
    hianyzo_konyvek = set()
    elof_id_szerint = G.elofordulasok_id_szerint(elofordulasok)

    hiba_volt = False
    for m in motivumok:
        regi_ut = os.path.join(LEXIKON_DIR, '%s_TUDOMANYOS.md' % m['id'])
        if not os.path.exists(regi_ut):
            continue
        sorai = elof_id_szerint.get(m['id'], [])
        if not sorai:
            continue

        cel_ut, darabok, cimvaltasok, hibak = migral_egy_id(
            m, sorai, konyv_sorrend, hianyzo_konyvek, regi_ut, celkonyvtar)
        if hibak:
            hiba_volt = True
            print('  %s: MEGALLAS -- onellenorzes hibaja:' % m['id'])
            for h in hibak:
                print('    - %s' % h)
            continue

        szakaszlista = sorted(darabok.keys())
        print('  %s: %s (%d bájt) -- kézi szakaszok átemelve: %s'
              % (m['id'], os.path.relpath(cel_ut, ROOT), os.path.getsize(cel_ut),
                 ', '.join(szakaszlista) if szakaszlista else '(nincs)'))
        for kulcs, regi_cim, uj_cim in cimvaltasok:
            print('      cím (%s): %r -> %r' % (kulcs, regi_cim, uj_cim))

    if hiba_volt:
        sys.exit(2)
    return 0


if __name__ == '__main__':
    sys.exit(main())
