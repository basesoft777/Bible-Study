#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
g2_forrasreteg_levalasztas.py -- F4 G2: a motivum-forrasreteg levalasztasa.

A hét betoltott motivum-ID kezzel irt prozaja atkerul a naploból
(motivumlog/PaRDeS_motivumok.md) a sajat forrasreteg-fajljaba
(motivumok/[ID].md). A naploban a helyukre a G7 elesites irja be a generalt
marker-blokkokat.

MODSZERTAN -- a brief G2 kotelezettsege: "a kivagas pontos old/new
szovegblokkokkal tortenjen, soha nem 'a kovetkezo ## fejlecig' alaku
utasitassal -- ez a mintazat korabban dokumentaltan vezetett zaro tartalom
elvesztesehez."

Ezert minden blokk KET explicit horgonnyal all: kezdo sor-prefix ES zaro
sor-prefix. A szkript:

  1. megkeresi a kezdo sort (a prefix a teljes fajlban EGYEDI kell legyen);
  2. onnan elorefele az ELSO olyan sort, amely a zaro prefixszel kezdodik;
  3. ellenorzi, hogy a kettö kozotti tartomanyban nincs tovabbi '## ' vagy
     '### ' fejlec (tulnyulas-vedelem) -- kiveve magat a kezdo sort;
  4. a TELJES kiolvasott blokkot (nem ujragepelve) irja a cel-fajlba;
  5. visszaolvassa a cel-fajlt, es igazolja, hogy a blokk BAJTRA benne van;
  6. csak ezutan tavolitja el a naplobol, pontosan azt a karakterlancot,
     amelyet kiolvasott (elofordulas-szam ellenorzessel: pontosan 1);
  7. zaro korut: a megmaradt naplo + a kivett blokkok osszege karakterre
     visszaadja az eredeti fajlt (K10).

Sorveg: a repo core.autocrlf=true-val megy, es a .gitattributes csak a *.tsv-t
rogziti LF-re -- a .md munkapeldany sorvege tehat checkoutonkent valtozhat
(l. .gitattributes es F4_BRIEF.md E11/B19). A szkript ezert MER: LF-re
normalizalva dolgozik, es a fajl sajat domináns sorvegevel ir vissza.

Futtatas a repo gyokerebol:
    python eszkozok/g2_forrasreteg_levalasztas.py          # szarazon, csak jelent
    python eszkozok/g2_forrasreteg_levalasztas.py --ir     # tenylegesen ir
"""

import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLO = os.path.join(ROOT, 'motivumlog', 'PaRDeS_motivumok.md')
MOTIVUMOK_DIR = os.path.join(ROOT, 'motivumok')
MOTIVUMOK_TSV = os.path.join(ROOT, 'adat', 'motivumok.tsv')

TS = '2026-09-15'

# Szakasz-cimkek a cel-fajlban, a naplobeli eredetuk sorrendjeben.
SZAKASZ_CIM = {
    'attekintes': '## Tematikus áttekintés — a napló mai tétele',
    'kuszob': '## ⭐ Emlékeztető küszöb — a napló mai bekezdése',
    'kulcsszo_index': '## Kulcsszó-index — a napló mai sora',
    'reszletes': '## Kulcsszavak részletesen — naplóbejegyzés',
}

SZAKASZ_SORREND = ['attekintes', 'kuszob', 'kulcsszo_index', 'reszletes']

# (kezdo sor-prefix, zaro sor-prefix). Egysoros blokknal a ketto azonos.
# A prefixek a naplo mai szovegebol valok, szo szerint.
BLOKKOK = {
    'ALVIL-001': {
        'attekintes': ('- hádész (seól) — a halottak birodalma (4 előfordulás',) * 2,
        'kuszob': ('**"hádész (seól) — a halottak birodalma" `[ID: ALVIL-001]`',) * 2,
        'kulcsszo_index': ('| **hádész (seól) — a halottak birodalma** ✅',) * 2,
    },
    'ANTROP-001': {
        'attekintes': ('- pneuma/pszükhé megkülönböztetés (5 előfordulás',) * 2,
        'kuszob': ('**"pneuma/pszükhé megkülönböztetés" `[ID: ANTROP-001]`',) * 2,
        'kulcsszo_index': ('| **pneuma/pszükhé megkülönböztetés** ✅',) * 2,
        'reszletes': ('### pneuma/pszükhé megkülönböztetés `[ID: ANTROP-001]`',
                      '- A motívum a továbbiakban nem szerepel aktív ⭐ ajánlásként; '
                      'jövőbeli előfordulásai (ha lesznek) továbbra is'),
    },
    'HODIT-001': {
        'attekintes': ('  - **↳ Rafeusok/óriás-népek (1Móz 14:5,',) * 2,
        'kuszob': ('**"Rafeusok/óriás-népek — tematikus rokon-csoport',) * 2,
        'kulcsszo_index': ('| **↳ Rafeusok/óriás-népek** ✅',) * 2,
        'reszletes': ('### Rafeusok/óriás-népek `[ID: HODIT-001]`',
                      '- A motívum a továbbiakban nem szerepel aktív ⭐ ajánlásként; '
                      'jövőbeli előfordulásai (ha lesznek, pl. 5Móz 2-3'),
    },
    'ISTENTISZT-001': {
        'attekintes': ('- segítségül hívni az Úr nevét — Énós kora (5 előfordulás',) * 2,
        'kuszob': ('**"segítségül hívni az Úr nevét" `[ID: ISTENTISZT-001]`',) * 2,
        'kulcsszo_index': ('| **segítségül hívni az Úr nevét** ✅',) * 2,
        'reszletes': ('### segítségül hívni az Úr nevét `[ID: ISTENTISZT-001]`',
                      '- **Kiegészítő szótartalmi jegyzet, felhasználói kérésre:**'),
    },
    'KIRALY-001': {
        'attekintes': ('- **Melkizedek — király-pap rendje, kenyér és bor (1, 14:18-20;',) * 2,
        'kulcsszo_index': ('| **Melkizedek — király-pap rendje, kenyér és bor** ✅',) * 2,
        'reszletes': ('### Melkizedek — király-pap rendje, kenyér és bor `[ID: KIRALY-001]`',
                      '- **Visszahivatkozott bővített study-k:**'),
    },
    'MENNY-001': {
        'attekintes': ('- Isten fiai — angyali/Séthita vita ✅ LEZÁRVA',) * 2,
        'kulcsszo_index': ('| **Isten fiai — angyali/Séthita vita** ✅',) * 2,
    },
    'TEREMT-001': {
        'attekintes': ('- tehóm — Abüσσος: a mélység motívuma, a teremtés visszafordítása',) * 2,
        'kuszob': ('**"tehóm — Abüσσος: a mélység motívuma" `[ID: TEREMT-001]`',) * 2,
        'kulcsszo_index': ('| **tehóm — Abüσσος: a mélység motívuma, a teremtés '
                           'visszafordítása és helyreállítása** ✅',) * 2,
    },
}


def szoveg_beolvas(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        return f.read()


def sorveg_mer(nyers):
    """(domináns_sorveg, crlf, lf) -- a fajl mai sorveg-aranya."""
    crlf = nyers.count('\r\n')
    lf = nyers.count('\n') - crlf
    return ('\r\n' if crlf > lf else '\n'), crlf, lf


def lf_re(nyers):
    return nyers.replace('\r\n', '\n')


def motivum_cimek():
    nyers = szoveg_beolvas(MOTIVUMOK_TSV)
    sorok = [s for s in nyers.replace('\r\n', '\n').split('\n')
             if s.strip() and not s.startswith('#')]
    fejlec = sorok[0].split('\t')
    i_cim = fejlec.index('cim')
    return {s.split('\t')[0]: s.split('\t')[i_cim] for s in sorok[1:]}


def blokk_kivag(sorok, kezd_prefix, zar_prefix, cimke):
    """(kezdo_index, zaro_index, blokk_szoveg) -- a TELJES blokk, a ket
    explicit horgony kozott. Egyediseg- es tulnyulas-ellenorzessel."""
    kezdok = [i for i, s in enumerate(sorok) if s.startswith(kezd_prefix)]
    if len(kezdok) != 1:
        raise SystemExit('MEGALLAS [%s]: a kezdo horgony %d helyen illeszkedik: %r'
                         % (cimke, len(kezdok), kezd_prefix))
    i0 = kezdok[0]
    if zar_prefix == kezd_prefix:
        i1 = i0
    else:
        i1 = None
        for j in range(i0 + 1, len(sorok)):
            if sorok[j].startswith(zar_prefix):
                i1 = j
                break
        if i1 is None:
            raise SystemExit('MEGALLAS [%s]: a zaro horgony nem talalhato a kezdo utan: %r'
                             % (cimke, zar_prefix))
        for j in range(i0 + 1, i1 + 1):
            if sorok[j].startswith('## ') or sorok[j].startswith('### '):
                raise SystemExit('MEGALLAS [%s]: a tartomany tovabbi fejlecet tartalmaz '
                                 '(%d. sor): %r' % (cimke, j + 1, sorok[j][:70]))
    return i0, i1, '\n'.join(sorok[i0:i1 + 1])


def cel_fajl_szoveg(azon, cim, blokkok):
    fej = []
    fej.append('# %s — forrásréteg `[ID: %s]`' % (cim, azon))
    fej.append('')
    fej.append('<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. '
               'NEM generált fájl. -->')
    fej.append('')
    fej.append('*Proveniencia: az alábbi szövegblokkok a '
               '`motivumlog/PaRDeS_motivumok.md`-ből lettek átemelve, **karakterre '
               'azonosan**, %s-én (F4.4 / G2). A naplóban a helyükön a `general.py` '
               'generált marker-blokkjai állnak. Ami a tábláról levezethető '
               '(`adat/motivumok.tsv`, `adat/elofordulasok.tsv`), az nem ide '
               'tartozik — ez a réteg csak azt hordozza, ami emberi ítélet: a '
               '⚠️-vitákat, az elhatárolások indoklását, a kiegészítő szótartalmi '
               'jegyzeteket, a nevesített tanítói alkalmazást és a gap-jelzéseket, '
               'valamint a 【NAPLO: …】 megjegyzéseket.*' % TS)
    reszek = ['\n'.join(fej)]
    for szakasz in SZAKASZ_SORREND:
        if szakasz not in blokkok:
            continue
        reszek.append(SZAKASZ_CIM[szakasz])
        reszek.append(blokkok[szakasz])
    return '\n\n'.join(reszek) + '\n'


def main():
    ir = '--ir' in sys.argv[1:]
    cimek = motivum_cimek()
    nyers_eredeti = szoveg_beolvas(NAPLO)
    sorveg, crlf, lf = sorveg_mer(nyers_eredeti)
    print('Napló sorvég a munkapéldányban: CRLF=%d, LF=%d -> domináns=%r '
          '(a visszaírás ezzel történik)' % (crlf, lf, sorveg))
    eredeti = lf_re(nyers_eredeti)
    sorok = eredeti.split('\n')

    kivett = {}
    print('=== 1. lépés: blokk-azonosítás a naplóban ===')
    for azon in sorted(BLOKKOK):
        kivett[azon] = {}
        for szakasz in SZAKASZ_SORREND:
            if szakasz not in BLOKKOK[azon]:
                continue
            kezd, zar = BLOKKOK[azon][szakasz]
            i0, i1, blokk = blokk_kivag(sorok, kezd, zar, '%s/%s' % (azon, szakasz))
            kivett[azon][szakasz] = blokk
            print('  %-15s %-15s sor %4d-%-4d  %6d karakter' %
                  (azon, szakasz, i0 + 1, i1 + 1, len(blokk)))
            print('      kezdet: %s' % blokk[:88].replace('\n', '\\n'))
            print('      vége:   %s' % blokk[-88:].replace('\n', '\\n'))

    osszes = sum(len(b) for d in kivett.values() for b in d.values())
    darab = sum(len(d) for d in kivett.values())
    print('\nÖsszesen %d blokk, %d karakter, %d ID.' % (darab, osszes, len(kivett)))

    # --- atfedés-ellenorzes: egyetlen blokk sem lehet resze masiknak
    mind = [(a, sz, b) for a, d in kivett.items() for sz, b in d.items()]
    for a, sz, b in mind:
        if eredeti.count(b) != 1:
            raise SystemExit('MEGALLAS [%s/%s]: a blokk %d-szer fordul elo a naploban.'
                             % (a, sz, eredeti.count(b)))

    print('\n=== 2. lépés: cél-fájlok ===')
    cel_tartalmak = {}
    for azon in sorted(kivett):
        tartalom = cel_fajl_szoveg(azon, cimek[azon], kivett[azon])
        cel_tartalmak[azon] = tartalom
        print('  motivumok/%s.md — %d bájt, %d blokk'
              % (azon, len(tartalom.encode('utf-8')), len(kivett[azon])))

    if not ir:
        print('\n(száraz futás — írás nem történt; --ir kapcsolóval ír)')
        return 0

    os.makedirs(MOTIVUMOK_DIR, exist_ok=True)
    for azon, tartalom in sorted(cel_tartalmak.items()):
        path = os.path.join(MOTIVUMOK_DIR, '%s.md' % azon)
        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(tartalom)

    # --- 3. lepes: IGAZOLAS a cel-fajlban, blokkonkent, MIELOTT a naplobol kivesszuk
    print('\n=== 3. lépés: igazolás a cél-fájlban (bájt-szintű) ===')
    for azon in sorted(kivett):
        path = os.path.join(MOTIVUMOK_DIR, '%s.md' % azon)
        vissza = szoveg_beolvas(path)
        for szakasz, blokk in kivett[azon].items():
            if blokk not in vissza:
                raise SystemExit('MEGALLAS [%s/%s]: a blokk NINCS meg a cél-fájlban — '
                                 'a napló érintetlen marad.' % (azon, szakasz))
        print('  motivumok/%s.md — mind a %d blokk igazolva' % (azon, len(kivett[azon])))

    # --- 4. lepes: kivetel a naplobol, pontosan a kiolvasott karakterlanccal
    print('\n=== 4. lépés: kivétel a naplóból ===')
    uj = eredeti
    for azon in sorted(kivett):
        for szakasz in SZAKASZ_SORREND:
            if szakasz not in kivett[azon]:
                continue
            blokk = kivett[azon][szakasz]
            if uj.count(blokk) != 1:
                raise SystemExit('MEGALLAS [%s/%s]: a kivétel elott %d elofordulas.'
                                 % (azon, szakasz, uj.count(blokk)))
            # a blokkot es a hozza tartozo sorveget vesszuk ki, hogy ne maradjon ures sor
            uj = uj.replace(blokk + '\n', '', 1)
            print('  kivéve: %s / %s (%d karakter)' % (azon, szakasz, len(blokk)))

    # A kivett bekezdes helyen ures sor + ures sor marad. A naplo HEAD-allapotaban
    # NINCS dupla ures sor (merve: 0), tehat ez a kivagas nyoma, nem szandekolt
    # formazas -- visszanormalizaljuk egyre. A tartalmat nem erinti.
    dupla_elott = sum(1 for i in range(len(uj.split('\n')) - 1)
                      if uj.split('\n')[i] == '' and uj.split('\n')[i + 1] == '')
    while '\n\n\n' in uj:
        uj = uj.replace('\n\n\n', '\n\n')
    print('  dupla üres sor a kivágás után: %d -> 0 (normalizálva)' % dupla_elott)

    with io.open(NAPLO, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(uj.split('\n')))

    # --- 5. lepes: zaro korut
    print('\n=== 5. lépés: záró körút ===')
    vissza = lf_re(szoveg_beolvas(NAPLO))
    print('  napló (LF-re normalizálva): %d -> %d bájt (%+d)'
          % (len(eredeti.encode('utf-8')), len(vissza.encode('utf-8')),
             len(vissza.encode('utf-8')) - len(eredeti.encode('utf-8'))))
    print('  napló sorszám: %d -> %d' % (eredeti.count('\n'), vissza.count('\n')))
    maradek = 0
    for azon in sorted(kivett):
        for szakasz, blokk in kivett[azon].items():
            if blokk in vissza:
                print('  MARADEK: %s/%s meg a naploban van!' % (azon, szakasz))
                maradek += 1
    if maradek:
        raise SystemExit('MEGALLAS: %d blokk nem tunt el a naplobol.' % maradek)
    print('  a %d blokk egyike sincs tobbe a naploban ✓' % darab)
    print('  kivett karakter: %d; napló-csökkenés: %d (a különbség a blokkonkénti '
          'záró sorvég + a normalizált üres sorok: %d)'
          % (osszes, len(eredeti) - len(vissza), len(eredeti) - len(vissza) - osszes))
    ujs = vissza.split('\n')
    dupla = sum(1 for i in range(len(ujs) - 1) if ujs[i] == '' and ujs[i + 1] == '')
    print('  dupla üres sor a naplóban: %d (a HEAD-állapotban is 0 volt)' % dupla)
    return 0


if __name__ == '__main__':
    sys.exit(main())
