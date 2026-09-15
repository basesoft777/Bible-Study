#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
g7_index_atszervezes.py -- F4 G7 elokeszites: a Lezart_tematikus_tanulmanyok_index.md
fo tablazatanak atszervezese, hogy a generalt blokk BEIRHATO legyen tartalomvesztes
nelkul.

A generalt `index` blokk negy oszlopot hoz (#, Motivum, Fajlnev, Erintett
igehelyek), es HET sort -- a mai tablazat viszont OT oszlopos es NYOLC soros:

  - a `Megjegyzes` oszlop nem generalhato (brief G4), es a dontes szerint a
    marker-blokkon KIVUL marad;
  - a nyolcadik sor a HAMART-001, amely nincs betoltve a motivumok.tsv-be
    (ismert F3-hiany, K8) -- a generalt blokk nem fedi, tehat kezi sorkent kell
    tovabbelnie, kulonben az elesites TARTALMAT VESZITENE.

A szkript ezert a mai tablazatot HAROM reszre bontja, a cellak ujragepelese
nelkul (minden cella a fajlbol olvasva):

  1. a generalt blokk helye (horgony-komment) -- ide irja a general.py --ir;
  2. "Megjegyzesek" tabla: Motivum `[ID]` | Megjegyzes -- a het betoltott ID
     Megjegyzes-cellai, ID-hez kotve (nem sorszamhoz: D12);
  3. "A tablaba meg nem betoltott, lezart tanulmany" tabla: a HAMART-001 mai
     sora teljes egeszeben, mind az ot cellaval.

Az ID-t a Fajlnev cellabol oldja fel az adat/motivumok.tsv forras_study mezoje
alapjan -- nem cimegyezes, nem sorrend.

TARTALOMVEDELEM. A mai `Erintett igehelyek` cella TOBBET mond, mint amit a
generalt blokk hoz (pl. "teljes kanoni mezo: 35 OSZ + 9 USZ, valodi
TAHOT/TAGNT-scannel 2026.09.10-en megerositve") -- ez emberi proza, nem a
tabla kepe. A szkript ezert minden betoltott ID TELJES MAI SORAT elobb
hozzafuzi a motivumok/[ID].md forrasreteghez (archiv szakasz), VISSZAOLVASSA
es bajtra igazolja, es csak azutan szervezi at az indexet -- ugyanaz a
modszertan, mint a G2-nel.

Iras elott korut: minden cella-szoveg, amely a regi tablazatban allt, meg kell
jelenjen az uj indexben VAGY a forrasretegben (bajtra); elteresnel megall.

Futtatas a repo gyokerebol:
    python eszkozok/g7_index_atszervezes.py          # szarazon
    python eszkozok/g7_index_atszervezes.py --ir     # ir
"""

import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'Lezart_tematikus_tanulmanyok_index.md')
MOTIVUMOK_TSV = os.path.join(ROOT, 'adat', 'motivumok.tsv')
MOTIVUMOK_DIR = os.path.join(ROOT, 'motivumok')

ARCHIV_CIM = ('## Lezárt tanulmányok indexe — a mai kézi sor '
              '*(archív: a generált blokk csak a fő előfordulásokat hozza)*')

FEJLEC = '| # | Motívum | Fájlnév | Érintett igehelyek | Megjegyzés |'
ELVALASZTO = '|---|---|---|---|---|'
HORGONY = '<!-- A GENERÁLT BLOKK HELYE: index -->'


def szoveg_beolvas(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        return f.read()


def fajlnev_id_terkep():
    """{fajlnev: id} -- az adat/motivumok.tsv forras_study mezojebol."""
    nyers = szoveg_beolvas(MOTIVUMOK_TSV).replace('\r\n', '\n')
    sorok = [s for s in nyers.split('\n') if s.strip() and not s.startswith('#')]
    fejlec = sorok[0].split('\t')
    i_fs = fejlec.index('forras_study')
    i_cim = fejlec.index('cim')
    terkep = {}
    cimek = {}
    for s in sorok[1:]:
        mezok = s.split('\t')
        cimek[mezok[0]] = mezok[i_cim]
        for ut in mezok[i_fs].split(';'):
            ut = ut.strip()
            if ut:
                terkep[os.path.basename(ut)] = mezok[0]
    return terkep, cimek


def main():
    ir = '--ir' in sys.argv[1:]
    terkep, cimek = fajlnev_id_terkep()

    nyers = szoveg_beolvas(INDEX)
    crlf = nyers.count('\r\n')
    lf = nyers.count('\n') - crlf
    sorveg = '\r\n' if crlf > lf else '\n'
    print('Index sorvég: CRLF=%d, LF=%d -> domináns=%r' % (crlf, lf, sorveg))
    szoveg = nyers.replace('\r\n', '\n')
    sorok = szoveg.split('\n')

    if szoveg.count(FEJLEC) != 1:
        raise SystemExit('MEGALLAS: a fo tablazat fejlece %d helyen all.'
                         % szoveg.count(FEJLEC))
    i_fejlec = sorok.index(FEJLEC)
    if sorok[i_fejlec + 1] != ELVALASZTO:
        raise SystemExit('MEGALLAS: a fejlec utan nem az elvalaszto all: %r'
                         % sorok[i_fejlec + 1])

    i = i_fejlec + 2
    adatsorok = []
    while i < len(sorok) and sorok[i].startswith('|'):
        adatsorok.append(sorok[i])
        i += 1
    i_utolso = i - 1
    print('A fő táblázat %d adatsora: %d-%d. sor' % (len(adatsorok), i_fejlec + 3, i_utolso + 1))

    betoltott = []
    nem_betoltott = []
    teljes_sor = {}
    for sor in adatsorok:
        cellak = [c.strip() for c in sor.strip('|').split('|')]
        if len(cellak) != 5:
            raise SystemExit('MEGALLAS: %d cellas sor: %r' % (len(cellak), sor[:80]))
        szam, motivum, fajlnev, igehelyek, megjegyzes = cellak
        kulcs = fajlnev.strip('`')
        azon = terkep.get(kulcs)
        print('  #%s  %-58s -> %s' % (szam, kulcs, azon or '(NINCS BETÖLTVE)'))
        if azon:
            betoltott.append((azon, motivum, fajlnev, igehelyek, megjegyzes))
            teljes_sor[azon] = sor
        else:
            nem_betoltott.append((motivum, fajlnev, igehelyek, megjegyzes))

    if len(betoltott) != 7:
        raise SystemExit('MEGALLAS: %d betoltott sor, 7 vart.' % len(betoltott))
    if len(nem_betoltott) != 1:
        raise SystemExit('MEGALLAS: %d nem betoltott sor, 1 vart.' % len(nem_betoltott))

    # --- 1. lepes: a teljes mai sor a forrasretegbe, MIELOTT az index atrendezodne
    print('\n=== A mai sorok átmentése a forrásrétegbe ===')
    forrasreteg_uj = {}
    for azon in sorted(teljes_sor):
        path = os.path.join(MOTIVUMOK_DIR, '%s.md' % azon)
        if not os.path.exists(path):
            raise SystemExit('MEGALLAS: hianyzik a forrasreteg-fajl: %s' % path)
        meglevo = szoveg_beolvas(path).replace('\r\n', '\n')
        if ARCHIV_CIM in meglevo:
            print('  %-15s az archív szakasz már megvan — kihagyva' % azon)
            forrasreteg_uj[azon] = meglevo
            continue
        fejlec_sorok = [FEJLEC, ELVALASZTO, teljes_sor[azon]]
        uj_tartalom = (meglevo.rstrip('\n') + '\n\n' + ARCHIV_CIM + '\n\n'
                       + '\n'.join(fejlec_sorok) + '\n')
        forrasreteg_uj[azon] = uj_tartalom
        print('  %-15s +%d bájt' % (azon, len(uj_tartalom.encode('utf-8'))
                                     - len(meglevo.encode('utf-8'))))

    uj = []
    uj.append(HORGONY)
    uj.append('')
    uj.append('### Megjegyzések *(kézi — a generált blokkon kívül, `[ID: …]`-hez kötve)*')
    uj.append('')
    uj.append('*A `#` oszlop a fenti generált blokkban puszta vizuális számláló, amely '
              'minden ID-felvételkor átszámozódik — ezért a megjegyzések ID-hez, nem '
              'sorszámhoz kötve állnak (D12).*')
    uj.append('')
    uj.append('| Motívum | Megjegyzés |')
    uj.append('|---|---|')
    for azon, motivum, _, _, megjegyzes in sorted(betoltott):
        uj.append('| %s `[ID: %s]` | %s |' % (motivum, azon, megjegyzes))
    uj.append('')
    uj.append('### A táblába még nem betöltött, lezárt tanulmány *(kézi)*')
    uj.append('')
    uj.append('*Ez a sor azért áll a generált blokkon kívül, mert az ID nincs betöltve '
              'az `adat/motivumok.tsv`-be (ismert F3-hiány; a generátor ezt a K8 '
              'szerint explicit hibaként jelenti). A sor kézi karbantartásban marad, '
              'amíg az F3 be nem tölti.*')
    uj.append('')
    uj.append('| Motívum | Fájlnév | Érintett igehelyek | Megjegyzés |')
    uj.append('|---|---|---|---|')
    for motivum, fajlnev, igehelyek, megjegyzes in nem_betoltott:
        uj.append('| %s | %s | %s | %s |' % (motivum, fajlnev, igehelyek, megjegyzes))

    uj_sorok = sorok[:i_fejlec] + uj + sorok[i_utolso + 1:]
    uj_szoveg = '\n'.join(uj_sorok)

    # --- korut: minden cella-szoveg megvan-e az uj indexben VAGY a forrasretegben
    hiany = 0
    hol_szamlalo = {'index': 0, 'forrásréteg': 0}
    for sor in adatsorok:
        for cella in [c.strip() for c in sor.strip('|').split('|')][1:]:
            if not cella:
                continue
            if cella in uj_szoveg:
                hol_szamlalo['index'] += 1
            elif any(cella in t for t in forrasreteg_uj.values()):
                hol_szamlalo['forrásréteg'] += 1
            else:
                print('  HIÁNYZÓ CELLA: %r' % cella[:100], file=sys.stderr)
                hiany += 1
    if hiany:
        raise SystemExit('MEGALLAS: %d cella sem az uj indexben, sem a forrasretegben.'
                         % hiany)
    print('\nKörút: mind a %d adatsor minden cellája (a sorszám kivételével) megvan — '
          'index: %d, forrásréteg: %d ✓'
          % (len(adatsorok), hol_szamlalo['index'], hol_szamlalo['forrásréteg']))
    print('Index: %d -> %d bájt' % (len(szoveg.encode('utf-8')),
                                     len(uj_szoveg.encode('utf-8'))))

    if not ir:
        print('\n(száraz futás — írás nem történt; --ir kapcsolóval ír)')
        return 0

    # A forrasreteg eloszor, es visszaolvasva igazolva -- csak azutan az index.
    for azon, tartalom in sorted(forrasreteg_uj.items()):
        path = os.path.join(MOTIVUMOK_DIR, '%s.md' % azon)
        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(tartalom)
    for azon in sorted(teljes_sor):
        path = os.path.join(MOTIVUMOK_DIR, '%s.md' % azon)
        vissza = szoveg_beolvas(path).replace('\r\n', '\n')
        if teljes_sor[azon] not in vissza:
            raise SystemExit('MEGALLAS [%s]: a mai index-sor NINCS meg a forrasretegben '
                             '-- az index erintetlen marad.' % azon)
    print('\nIgazolás: mind a 7 mai index-sor bájtra megvan a forrásrétegben ✓')

    with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(uj_szoveg.split('\n')))
    print('Megírva: Lezart_tematikus_tanulmanyok_index.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
