#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
betolt.py -- F8.8: study<->adat atjaro, ket iranyban (F8_BRIEF.md G2, G10).

  kulcszo  (A3): a bovitett study `## 2.` pontja alatti elso "Kulcsszavak
    tablazata" tablat irja at az `adat/kulcsszavak.tsv` atmeneti tablaba
    (SEMA 2.8). Osszetett Strong ('H4397+H3068') Strongonkent kulon sorra
    bomlik, azonos `szo`-val.

  beepit  (B6): egy kutato altal kitoltott munkalapot lepteti elo
    `elofordulasok.tsv` sorokka. Csak olyan sor irhato at, amelyhez a
    `jeloltek.tsv`-ben `dontes=beépítve` sor tartozik (SEMA §3/2 -- nincs
    kozvetlen ut). Egyetlen hibas sor eseten a teljes futas megall, semmi
    nem irodik (f3_1_betoltes.py memoria-elobb elve). A `dontes` mezot ez a
    szkript SOHA nem irja. A `kapcsolatok.tsv`-t nem erinti (G10).

Mindket alparancs `--ir` nelkul proba, `--adat DIR` kapcsolot fogad.

CLI:
    python eszkozok/betolt.py kulcsszo --study FILE --konyv "<könyv>" [--ir] [--adat DIR] [--md FILE]
    python eszkozok/betolt.py beepit --munkalap FILE [--ir] [--adat DIR] [--md FILE]

Kilepesi kod: 0 = rendben (irt vagy iras nelkul is hibatlan), 1 = szabalysertes
(semmi nem irodott), 2 = hiba.
"""

import argparse
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G
import lekerdez as L
import ellenoriz as E

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')

KULCSSZAVAK_FEJLEC = ['tanulmany', 'igehely', 'szo', 'strong', 'datum']

ELOFORDULASOK_FEJLEC = [
    'id', 'igehely', 'kapcsolodas', 'pardes_szint', 'funkcio', 'gerinc_elem',
    'strong', 'lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam',
    'jelentes_en', 'jelentes_hu', 'karoli_szo', 'azonositas_modja',
    'megbizhatosag', 'proveniencia', 'igazolas', 'fo_elofordulas',
    'felmerult_tanulmany',
]

ELOFORDULASOK_KOTELEZO = ['id', 'igehely', 'kapcsolodas', 'gerinc_elem',
                           'proveniencia', 'igazolas']


# ---------------------------------------------------------------------------
# kulcsszo (A3)
# ---------------------------------------------------------------------------

FOCIM_2_RE = re.compile(r'^## 2\.', re.M)
FOCIM_ARM_RE = re.compile(r'^## \d+', re.M)
KULCSTABLA_CIM_RE = re.compile(r'^### Kulcsszavak táblázata\s*$', re.M)


def _szakasz_2_szoveg(study_szoveg):
    """A '## 2.' focim torzse a kovetkezo '## N' focimig (vagy a fajl vegeig)."""
    m = FOCIM_2_RE.search(study_szoveg)
    if not m:
        return None
    utana = study_szoveg[m.end():]
    kovetkezo = FOCIM_ARM_RE.search(utana)
    return utana[:kovetkezo.start()] if kovetkezo else utana


def _elso_tablazat(szoveg):
    """[sorok] -- az elso markdown-tablazat sorai (fejleccel egyutt), '|'-vel
    tagolt cellak listajakent soronkent. None, ha nincs tablazat."""
    sorok = szoveg.split('\n')
    tabla_sorok = []
    benne = False
    for sor in sorok:
        s = sor.strip()
        if s.startswith('|'):
            benne = True
            tabla_sorok.append(s)
        elif benne:
            break
    if not tabla_sorok:
        return None
    kimenet = []
    for sor in tabla_sorok:
        cellak = [c.strip() for c in sor.strip('|').split('|')]
        kimenet.append(cellak)
    return kimenet


def kulcsszo_sorok_kiolvas(study_path, konyv):
    """[{tanulmany, igehely, szo, strong}] -- a study '## 2.' pontja alatti
    elso 'Kulcsszavak tablazata' tabla sorai, osszetett Strong Strongonkent
    kulon sorra bontva. Hiba: hianyzo tabla / elemezhetetlen vers -> kivetel."""
    szoveg = G.szoveg_beolvas(study_path)
    szakasz2 = _szakasz_2_szoveg(szoveg)
    if szakasz2 is None:
        raise ValueError('a study-ban nincs "## 2." főcím: %s' % study_path)

    cim_m = KULCSTABLA_CIM_RE.search(szakasz2)
    if not cim_m:
        raise ValueError('a "## 2." pont alatt nincs "### Kulcsszavak táblázata" alcím: %s' % study_path)

    tabla = _elso_tablazat(szakasz2[cim_m.end():])
    if not tabla or len(tabla) < 2:
        raise ValueError('a "Kulcsszavak táblázata" alcím alatt nincs táblázat: %s' % study_path)

    fejlec = tabla[0]
    try:
        idx_vers = fejlec.index('Vers')
    except ValueError:
        raise ValueError('a kulcsszó-táblázat fejléce nem tartalmaz "Vers" oszlopot: %s' % study_path)
    idx_szo = 1
    try:
        idx_strong = fejlec.index('Strong-szám')
    except ValueError:
        raise ValueError('a kulcsszó-táblázat fejléce nem tartalmaz "Strong-szám" oszlopot: %s' % study_path)

    adatsorok = tabla[1:]
    if adatsorok and all(set(c) <= {'-', ':', ' '} for c in adatsorok[0]):
        adatsorok = adatsorok[1:]  # elvalaszto sor ('|---|---|...')

    rel = os.path.relpath(study_path, ROOT).replace(os.sep, '/')
    ki = []
    for sor in adatsorok:
        vers = sor[idx_vers].strip()
        szo = sor[idx_szo].strip()
        strong_ertek = sor[idx_strong].strip()
        if not vers or not strong_ertek:
            continue
        igehely = '%s %s' % (konyv, vers)
        try:
            L.parse_range(igehely)
        except Exception:
            raise ValueError('elemezhetetlen vers: %r (igehely: %r)' % (vers, igehely))
        for strong in strong_ertek.split('+'):
            strong = strong.strip()
            if not strong:
                continue
            ki.append({
                'tanulmany': rel,
                'igehely': igehely,
                'szo': szo,
                'strong': strong,
            })
    return ki


def kulcsszavak_ir(adat_dir, sorok):
    """Csak az uj (tanulmany, igehely, strong) kulcsu sorokat irja a
    kulcsszavak.tsv vegere. Visszaadja a tenylegesen beirt sorok listajat."""
    path = os.path.join(adat_dir, 'kulcsszavak.tsv')
    _, meglevo = G.tsv_beolvas(path)
    meglevo_kulcsok = {(s['tanulmany'], s['igehely'], s['strong']) for s in meglevo}

    ma = datetime.date.today().isoformat()
    uj_sorszovegek = []
    irt = []
    latott = set()
    for s in sorok:
        kulcs = (s['tanulmany'], s['igehely'], s['strong'])
        if kulcs in meglevo_kulcsok or kulcs in latott:
            continue
        latott.add(kulcs)
        mezok = dict(s)
        mezok['datum'] = ma
        uj_sorszovegek.append('\t'.join(mezok[m] for m in KULCSSZAVAK_FEJLEC))
        irt.append(kulcs)

    if not uj_sorszovegek:
        return []

    domináns, _, _ = G.sorveg_elemez(path)
    with open(path, 'rb') as f:
        nyers = f.read()
    vegzodik_sorveggel = nyers.endswith(b'\n')
    domináns_b = domináns.encode('utf-8')
    with open(path, 'ab') as f:
        if not vegzodik_sorveggel:
            f.write(domináns_b)
        f.write(domináns_b.join(s.encode('utf-8') for s in uj_sorszovegek))
        f.write(domináns_b)
    return irt


def kulcsszo_jelentes(study_path, konyv, sorok, irt):
    rel = os.path.relpath(study_path, ROOT).replace(os.sep, '/')
    ki = ['# betolt.py kulcsszo -- A3 study→kulcsszavak.tsv (F8.8)', '',
          'Study: `%s` | Könyv: `%s`' % (rel, konyv), '',
          '| Igehely | Szó | Strong |', '|---|---|---|']
    for s in sorok:
        ki.append('| %s | %s | %s |' % (s['igehely'], s['szo'], s['strong']))
    ki.append('')
    ki.append('Összesen %d sor a táblából; %d új sor íródott (vagy íródna --ir esetén).'
               % (len(sorok), len(irt)))
    return '\n'.join(ki) + '\n'


def fut_kulcsszo(args):
    try:
        sorok = kulcsszo_sorok_kiolvas(args.study, args.konyv)
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    if args.ir:
        try:
            irt = kulcsszavak_ir(args.adat, sorok)
        except Exception as exc:
            print('HIBA: %s' % exc, file=sys.stderr)
            sys.exit(2)
    else:
        path = os.path.join(args.adat, 'kulcsszavak.tsv')
        _, meglevo = G.tsv_beolvas(path)
        meglevo_kulcsok = {(s['tanulmany'], s['igehely'], s['strong']) for s in meglevo}
        irt = []
        latott = set()
        for s in sorok:
            kulcs = (s['tanulmany'], s['igehely'], s['strong'])
            if kulcs in meglevo_kulcsok or kulcs in latott:
                continue
            latott.add(kulcs)
            irt.append(kulcs)

    szoveg = kulcsszo_jelentes(args.study, args.konyv, sorok, irt)
    print(szoveg)
    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('  megírva: %s' % args.md, file=sys.stderr)
    if args.ir:
        print('  --ir: %d új kulcsszavak.tsv sor íródott.' % len(irt), file=sys.stderr)
    sys.exit(0)


# ---------------------------------------------------------------------------
# beepit (B6)
# ---------------------------------------------------------------------------

def munkalap_ellenoriz(munkalap_sorok, jeloltek, elofordulasok):
    """[(sor, hibauzenet_lista)] -- minden munkalap-sorra a feltetelek
    ellenorzese (SEMA §3/2, 2.2 kotelezo mezok, G9 proveniencia). Az
    ervenyes sorok mellett a jeloltek-bol orokolt karoli_szo/azonositas_
    modja/megbizhatosag is bekerul a sor dict-jebe."""
    beepitett = {(j['id'], j['igehely']): j for j in jeloltek if j.get('dontes') == 'beépítve'}
    letezo = {(sor['id'], sor['igehely']) for sor in elofordulasok}

    eredmeny = []
    latott_kulcsok = set()
    for sor in munkalap_sorok:
        hibak = []
        kulcs = (sor.get('id', ''), sor.get('igehely', ''))

        jelolt_sor = beepitett.get(kulcs)
        if jelolt_sor is None:
            hibak.append('elutasítva -- nincs %s / %s kulcsú, dontes=beépítve jeloltek-sor' % kulcs)

        if kulcs in letezo:
            hibak.append('%s / %s már szerepel az elofordulasok.tsv-ben -- felülírás nincs' % kulcs)

        if kulcs in latott_kulcsok:
            hibak.append('%s / %s duplikált sor a munkalapon' % kulcs)
        latott_kulcsok.add(kulcs)

        for mezo in ELOFORDULASOK_KOTELEZO:
            if not (sor.get(mezo) or '').strip():
                hibak.append('%s / %s -- kötelező mező üres: %s' % (kulcs[0], kulcs[1], mezo))

        if (sor.get('proveniencia') or '').strip() and not E.proveniencia_ervenyes(sor.get('proveniencia')):
            hibak.append('%s / %s -- érvénytelen proveniencia: %r' % (kulcs[0], kulcs[1], sor.get('proveniencia')))

        uj_sor = dict(sor)
        if jelolt_sor is not None:
            uj_sor['karoli_szo'] = jelolt_sor.get('karoli_szo', '')
            uj_sor['azonositas_modja'] = jelolt_sor.get('azonositas_modja', '')
            uj_sor['megbizhatosag'] = jelolt_sor.get('megbizhatosag', '')

        eredmeny.append((uj_sor, hibak))
    return eredmeny


def elofordulasok_ir(adat_dir, jo_sorok):
    path = os.path.join(adat_dir, 'elofordulasok.tsv')
    sorszovegek = []
    for sor in jo_sorok:
        mezok = {m: (sor.get(m) or '') for m in ELOFORDULASOK_FEJLEC}
        sorszovegek.append('\t'.join(mezok[m] for m in ELOFORDULASOK_FEJLEC))

    if not sorszovegek:
        return

    domináns, _, _ = G.sorveg_elemez(path)
    with open(path, 'rb') as f:
        nyers = f.read()
    vegzodik_sorveggel = nyers.endswith(b'\n')
    domináns_b = domináns.encode('utf-8')
    with open(path, 'ab') as f:
        if not vegzodik_sorveggel:
            f.write(domináns_b)
        f.write(domináns_b.join(s.encode('utf-8') for s in sorszovegek))
        f.write(domináns_b)


def beepit_jelentes(munkalap_path, ellenorzott):
    rel = os.path.relpath(munkalap_path, ROOT).replace(os.sep, '/') \
        if munkalap_path.startswith(ROOT) else munkalap_path
    osszes_hiba = [h for _, hibak in ellenorzott for h in hibak]
    ki = ['# betolt.py beepit -- B6 munkalap→elofordulasok.tsv (F8.8)', '',
          'Munkalap: `%s`' % rel, '']
    if osszes_hiba:
        ki.append('**SÉRTÉS (%d)** -- semmi nem íródott:' % len(osszes_hiba))
        for h in osszes_hiba:
            ki.append('  - %s' % h)
    else:
        ki.append('**RENDBEN** -- mind a %d sor átmegy.' % len(ellenorzott))
    ki.append('')
    ki.append('Összesen %d munkalap-sor; %d hiba.' % (len(ellenorzott), len(osszes_hiba)))
    return '\n'.join(ki) + '\n'


def fut_beepit(args):
    try:
        _, munkalap_sorok = G.tsv_beolvas(args.munkalap)
        _, jeloltek = G.tsv_beolvas(os.path.join(args.adat, 'jeloltek.tsv'))
        _, elofordulasok = G.tsv_beolvas(os.path.join(args.adat, 'elofordulasok.tsv'))
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    ellenorzott = munkalap_ellenoriz(munkalap_sorok, jeloltek, elofordulasok)
    szoveg = beepit_jelentes(args.munkalap, ellenorzott)
    print(szoveg)
    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('  megírva: %s' % args.md, file=sys.stderr)

    van_hiba = any(hibak for _, hibak in ellenorzott)
    if van_hiba:
        sys.exit(1)

    if args.ir:
        jo_sorok = [sor for sor, _ in ellenorzott]
        try:
            elofordulasok_ir(args.adat, jo_sorok)
        except Exception as exc:
            print('HIBA: %s' % exc, file=sys.stderr)
            sys.exit(2)
        print('  --ir: %d új elofordulasok.tsv sor íródott.' % len(jo_sorok), file=sys.stderr)
    sys.exit(0)


# ---------------------------------------------------------------------------
# Fő futás
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='F8.8 -- study↔adat átjáró')
    sub = parser.add_subparsers(dest='parancs', required=True)

    p1 = sub.add_parser('kulcsszo', help='A3: study kulcsszó-táblázat → kulcsszavak.tsv')
    p1.add_argument('--study', required=True, help='a bővített study fájl útja')
    p1.add_argument('--konyv', required=True, help='a könyv neve, pl. "1Móz"')
    p1.add_argument('--ir', action='store_true', help='írás a kulcsszavak.tsv végére')
    p1.add_argument('--adat', default=ALAPERTELMEZETT_ADAT, help='az adat/ könyvtár')
    p1.add_argument('--md', default=None, help='a jelentés Markdown fájlba is')

    p2 = sub.add_parser('beepit', help='B6: munkalap → elofordulasok.tsv')
    p2.add_argument('--munkalap', required=True, help='a kitöltött munkalap TSV útja')
    p2.add_argument('--ir', action='store_true', help='írás az elofordulasok.tsv végére')
    p2.add_argument('--adat', default=ALAPERTELMEZETT_ADAT, help='az adat/ könyvtár')
    p2.add_argument('--md', default=None, help='a jelentés Markdown fájlba is')

    args = parser.parse_args()

    if args.parancs == 'kulcsszo':
        fut_kulcsszo(args)
    else:
        fut_beepit(args)


if __name__ == '__main__':
    main()
