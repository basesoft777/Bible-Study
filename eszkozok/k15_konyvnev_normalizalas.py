#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
k15_konyvnev_normalizalas.py -- F4 K15/D14: egyseges igehely-alak az
adat/elofordulasok.tsv-ben.

A tabla ma ugyanazt a konyvet ket alakban tarolja (`Luk 1:46` ES
`Lukacs 16:23`; `Rom 10:14` ES `Roma 10:7`), tovabba 8 sor `Jelenesek ...`
es 1 sor `Mate 11:23` hosszu konyvnevet hasznal. A tabla kulcsa id + igehely,
tehat a ket alak KET KULCS -- a renderelo-oldali alias (general.py
KONYV_ALIAS) csak a generatort javitja meg, a gate.py-t, a lekerdez.py-t es
minden jovobeli, igehelyre epulo joint nem. Ezert a normalizalas a TABLABAN
tortenik (D14, ugyanaz az eset, mint a D5: Pshat -> Peshat).

A celalakot a konkordancia/Konyv_normalizalo_tabla.tsv "Magyar rovidites"
oszlopa adja -- nem beegetve: a szkript onnan olvassa ki, es megall, ha a
tabla nem azt mondja, amit a lekepezes var.

KET TABLAT ERINT. A javitas az adat/jeloltek.tsv 13 soran is elvegzendo,
ugyanazokon az igehelyeken: a SEMA 2. szabalya szerint "minden elofordulasok
sorhoz tartozik jeloltek sor AZONOS KULCCSAL", es a karoli_szo a jeloltek.tsv
azonos kulcsu sorabol oroklodik. Merve: ha csak az elofordulasok.tsv javul,
a 13 sor elveszti a jeloltek-beli parjat (13 arva kulcs); mindket tabla
javitasa utan a join 0 hiannyal all helyre. A tobbi adat/*.tsv nem tartalmaz
hosszu konyvnev-alakot (merve).

Amit NEM erint: a fo_elofordulas mezo csoportkulcsai (pl. "Luk 10:15/Mat
11:23") a naplo sajat szovegenek idezetei, nem igehely-kulcsok -- a "Mat"
ott szandekos (D10). A szkript kizarolag az `igehely` oszlopot irja, a
szabad szoveges mezoket (indoklas, kapcsolodas) nem.

I/O: split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md). Iras elott
bajt-szintu korut-ellenorzes: minden mas mezoertek es a sorveg (LF)
valtozatlan; eltere0snel megall.

Futtatas a repo gyokerebol:
    python eszkozok/k15_konyvnev_normalizalas.py            # szarazon, csak jelent
    python eszkozok/k15_konyvnev_normalizalas.py --ir       # tenylegesen ir
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
NORM_TABLA = os.path.join(ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

# (relativ_ut, vart_adatsor, {varians: vart_db}) -- a vart darabszamok az
# F4_GENERATOR_BRIEF.md 1.6 merese (elofordulasok), illetve a jeloltek.tsv
# sajat merese; elteresnel a szkript MEGALL, nem ir.
TABLAK = [
    ('adat/elofordulasok.tsv', 201,
     {'Jelenések': 8, 'Lukács': 3, 'Máté': 1, 'Róma': 1}),
    ('adat/jeloltek.tsv', 221,
     {'Jelenések': 8, 'Lukács': 3, 'Máté': 1, 'Róma': 1}),
]

# hosszu (vagy nem-kanonikus) alak -> a normalizalo tabla "Teljes magyar
# konyvnev" oszlopa, amelybol a cel-rovidites KIOLVASANDO.
VARIANS_TELJES_NEV = {
    'Jelenések': 'Jelenések könyve',
    'Lukács': 'Lukács evangéliuma',
    'Máté': 'Máté evangéliuma',
    'Róma': 'Rómabeliekhez írt levél',
}


def szoveg_beolvas(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        return f.read()


def celalakok():
    """{varians: magyar_rovidites} -- a normalizalo tablabol kiolvasva."""
    nyers = szoveg_beolvas(NORM_TABLA)
    sorok = nyers.replace('\r\n', '\n').split('\n')
    fejlec = sorok[0].split('\t')
    i_rov = fejlec.index('Magyar rövidítés')
    i_teljes = fejlec.index('Teljes magyar könyvnév')
    teljes_szerint = {}
    for s in sorok[1:]:
        if not s.strip():
            continue
        mezok = s.split('\t')
        teljes_szerint[mezok[i_teljes]] = mezok[i_rov]
    terkep = {}
    for varians, teljes in VARIANS_TELJES_NEV.items():
        if teljes not in teljes_szerint:
            raise SystemExit('MEGALLAS: a normalizalo tabla nem ismeri: %r' % teljes)
        terkep[varians] = teljes_szerint[teljes]
    return terkep


def kulcsok(rel_ut):
    """{(id, igehely)} -- a tabla mai kulcshalmaza (SEMA: kulcs = id + igehely)."""
    nyers = szoveg_beolvas(os.path.join(ROOT, rel_ut))
    sorok = [s for s in nyers.split('\n') if s.strip() and not s.startswith('#')]
    fejlec = sorok[0].split('\t')
    i_ig = fejlec.index('igehely')
    return {(s.split('\t')[0], s.split('\t')[i_ig]) for s in sorok[1:]}


def join_ellenoriz(cimke):
    """SEMA 2. szabaly: minden elofordulasok-sorhoz tartozik azonos kulcsu
    jeloltek-sor. A K15 ezt a kulcsot irja at, tehat a szabalyt a javitas
    elott ES utan is merni kell."""
    elof = kulcsok('adat/elofordulasok.tsv')
    jel = kulcsok('adat/jeloltek.tsv')
    arva = sorted(elof - jel)
    print('%s join (elofordulasok -> jeloltek, kulcs=id+igehely): %d arva kulcs'
          % (cimke, len(arva)))
    for azon, ig in arva[:20]:
        print('    arva: %s | %s' % (azon, ig))
    return arva


def tabla_javit(rel_ut, vart_adatsor, vart_db, terkep, ir):
    path = os.path.join(ROOT, rel_ut)
    print('\n=== %s ===' % rel_ut)
    nyers = szoveg_beolvas(path)
    if '\r\n' in nyers:
        raise SystemExit('MEGALLAS: a tabla CRLF-et tartalmaz, LF-et vartunk.')
    sorok = nyers.split('\n')
    zaro_ures = bool(sorok) and sorok[-1] == ''
    if zaro_ures:
        sorok = sorok[:-1]

    fejlec_idx = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fejlec = sorok[fejlec_idx].split('\t')
    i_igehely = fejlec.index('igehely')

    uj_sorok = list(sorok)
    valtozott = []
    szamlalo = {}
    for i in range(fejlec_idx + 1, len(sorok)):
        s = sorok[i]
        if not s.strip() or s.startswith('#'):
            continue
        mezok = s.split('\t')
        if len(mezok) != len(fejlec):
            raise SystemExit('MEGALLAS: oszlopszam-elteres a %d. sorban' % (i + 1))
        igehely = mezok[i_igehely]
        m = re.match(r'^(\d*[^\d\s]+)(\s.*)$', igehely)
        if not m:
            continue
        token, maradek = m.group(1), m.group(2)
        if token not in terkep:
            continue
        uj_igehely = terkep[token] + maradek
        mezok_uj = list(mezok)
        mezok_uj[i_igehely] = uj_igehely
        uj_sorok[i] = '\t'.join(mezok_uj)
        valtozott.append((i + 1, mezok[0], igehely, uj_igehely))
        szamlalo[token] = szamlalo.get(token, 0) + 1

    print('\nJavitando sorok: %d' % len(valtozott))
    for sorszam, azon, regi, uj in valtozott:
        print('  %4d. sor  %-14s %-18s -> %s' % (sorszam, azon, regi, uj))
    print('\nVariansonkent: %s' % ', '.join('%s=%d' % (k, szamlalo.get(k, 0))
                                            for k in sorted(vart_db)))
    for varians, vart in vart_db.items():
        if szamlalo.get(varians, 0) != vart:
            raise SystemExit('MEGALLAS: %r -- %d sor talalva, %d vart.'
                             % (varians, szamlalo.get(varians, 0), vart))

    # --- korut-ellenorzes: minden MAS mezo valtozatlan
    if len(uj_sorok) != len(sorok):
        raise SystemExit('MEGALLAS: sorszam-valtozas.')
    elteres_mas_mezoben = 0
    for i, (regi, uj) in enumerate(zip(sorok, uj_sorok)):
        if regi == uj:
            continue
        r, u = regi.split('\t'), uj.split('\t')
        for j, (rm, um) in enumerate(zip(r, u)):
            if rm != um and j != i_igehely:
                elteres_mas_mezoben += 1
                print('  ELTERES a %d. sor %r mezojeben: %r -> %r'
                      % (i + 1, fejlec[j], rm, um), file=sys.stderr)
    if elteres_mas_mezoben:
        raise SystemExit('MEGALLAS: %d elteres az igehely oszlopon kivul.'
                         % elteres_mas_mezoben)

    # --- kulcsutkozes: a javitas nem olvaszthat ossze ket letezo kulcsot
    uj_kulcsok = {}
    for i in range(fejlec_idx + 1, len(uj_sorok)):
        s = uj_sorok[i]
        if not s.strip() or s.startswith('#'):
            continue
        mezok = s.split('\t')
        k = (mezok[0], mezok[i_igehely])
        uj_kulcsok[k] = uj_kulcsok.get(k, 0) + 1
    utkozes = sorted(k for k, v in uj_kulcsok.items() if v > 1)
    if utkozes:
        raise SystemExit('MEGALLAS: kulcsutkozes a javitas utan: %r' % utkozes)
    print('Kulcsok (id + igehely): %d, utkozes nelkul' % len(uj_kulcsok))

    uj_nyers = '\n'.join(uj_sorok) + ('\n' if zaro_ures else '')
    adatsor = sum(1 for i, s in enumerate(uj_sorok)
                  if i > fejlec_idx and s.strip() and not s.startswith('#'))
    regi_bajt = len(nyers.encode('utf-8'))
    uj_bajt = len(uj_nyers.encode('utf-8'))
    print('Adatsorok: %d (vart: %d)' % (adatsor, vart_adatsor))
    if adatsor != vart_adatsor:
        raise SystemExit('MEGALLAS: adatsor-szam valtozott.')
    print('Bajt: %d -> %d (kulonbseg: %+d)' % (regi_bajt, uj_bajt, uj_bajt - regi_bajt))
    print('Idezojel-szamlalo az egesz fajlban: %d -> %d'
          % (nyers.count('"'), uj_nyers.count('"')))
    if nyers.count('"') != uj_nyers.count('"'):
        raise SystemExit('MEGALLAS: az idezojel-szamlalo valtozott.')

    if not ir:
        print('(szaraz futas -- iras nem tortent; --ir kapcsoloval ir)')
        return len(valtozott)

    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(uj_nyers)
    with io.open(path, 'rb') as f:
        vissza = f.read()
    if vissza != uj_nyers.encode('utf-8'):
        raise SystemExit('MEGALLAS: a visszaolvasott fajl nem egyezik a szandekolt tartalommal.')
    if b'\r\n' in vissza:
        raise SystemExit('MEGALLAS: CRLF kerult a fajlba.')
    print('Megirva: %s (%d bajt, LF)' % (rel_ut, len(vissza)))
    return len(valtozott)


def main():
    ir = '--ir' in sys.argv[1:]
    terkep = celalakok()
    print('Celalakok a Konyv_normalizalo_tabla.tsv "Magyar rövidítés" oszlopabol:')
    for v in sorted(terkep):
        print('  %-12s -> %s' % (v, terkep[v]))

    print()
    join_ellenoriz('JAVITAS ELOTT --')

    osszesen = 0
    for rel_ut, vart_adatsor, vart_db in TABLAK:
        osszesen += tabla_javit(rel_ut, vart_adatsor, vart_db, terkep, ir)

    print('\nOsszesen javitott sor: %d (%d tablaban)' % (osszesen, len(TABLAK)))
    print()
    arva = join_ellenoriz('JAVITAS UTAN --' if ir else 'IRAS NELKUL (valtozatlan) --')
    if ir and arva:
        raise SystemExit('MEGALLAS: a javitas utan %d arva kulcs maradt.' % len(arva))
    return 0


if __name__ == '__main__':
    sys.exit(main())
