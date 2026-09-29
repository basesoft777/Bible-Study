#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kiejtes.py -- SZOTAR_BRIEF.md S1.3: gorog SBL-atirat -> magyaros kiejtes.

Bemenet: a TAGNT_kivonat.tsv/TBESG.txt "Kiejtes" oszlopaban mar meglevo,
SBL-stilusu (Unicode makronos: ē ō ā ī ū) akademiai atirat -- ezt a
lexikon_general.py/torzscikk_general.py ma valtozatlanul jeleniti meg; ez
a szkript alakitja at magyaros formara.

Ket adatforras (mindketto adat/SEMA.md-ben dokumentalva):
  - adat/kiejtes_szabalyok.tsv (2.16): sorszam szerinti, szekvencialis
    literalis csereszabalyok.
  - adat/kiejtes_kivetelek.tsv (2.17): nyelv=gorog egesz-alak kivetelek,
    amelyek FELULIRJAK a szabalyalapu eredmenyt (masking-gal, hogy a
    kesobbi szabalyok ne dolgozzak fel meg egyszer a mar kesz kivetel-
    szoveget).

CLI:
    python eszkozok/kiejtes.py --atir "kaleō"
    python eszkozok/kiejtes.py --ellenoriz
    python eszkozok/kiejtes.py --onteszt

--ellenoriz: a naplok/SZOTAR_S1_kiejtes_arany_sbl.tsv 26 parjan futtatja
az atir()-t, es reszletes jelentest ad (sorra bontott talalat, szabaly-
lefedettseg, 1-part-lefedo szabalyok, kihagyasos/leave-one-out proba) --
NEM ir semmit, es a kilepokod mindig 0, kiveve hasznalati hibat (fajl
hianyzik stb, kilepokod 1). A 100%-os egyezes onmagaban NEM elegendo
elfogadasi erv (SZOTAR_BRIEF.md D31-mintajara) -- a jelentes mindig
kiirja a lefedettsegi es kihagyasos reszletet is, fuggetlenul az
osszesitett eredmenytol.

TSV-olvasas kizarolag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')
NAPLOK = os.path.join(ROOT, 'naplok')

SZABALYOK_TSV = os.path.join(ADAT, 'kiejtes_szabalyok.tsv')
KIVETELEK_TSV = os.path.join(ADAT, 'kiejtes_kivetelek.tsv')
ARANY_TSV = os.path.join(NAPLOK, 'SZOTAR_S1_kiejtes_arany_sbl.tsv')

_PLACEHOLDER_MINTA = '%03d'
_SS_MASK_UPPER = ''
_SS_MASK_LOWER = ''
# αυ/ευ diftongusok -- a bennuk levo "u" NEM allo upsilon, tehat nem
# valhat "u"->"ü"-ve (l. καύχημα -> kauchēma, ahol az "au" valtozatlanul
# marad "au", nem "aü"). Csak a ket leggyakoribb, gold-adattal igazolt
# esetet maszkoljuk (D32-vizsgalat, kiejtes.py --ellenoriz); az "ēu"
# (eta+upsilon) ritka, nincs ra adat, egyelore nem maszkolt.
_DIFTONGUS_MASZK = {'au': '', 'Au': '', 'eu': '', 'Eu': ''}


# ---------------------------------------------------------------------------
# TSV betoltes
# ---------------------------------------------------------------------------

def _tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def _tsv_dict_sorok(ut):
    fejlec = None
    for mezok in _tsv_sorok(ut):
        if mezok[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = mezok
            continue
        yield dict(zip(fejlec, mezok))


def szabalyok_betolt(ut=SZABALYOK_TSV):
    sorok = sorted(_tsv_dict_sorok(ut), key=lambda r: int(r['sorszam']))
    return [(r['minta'], r['csere']) for r in sorok]


def kivetelek_betolt(ut=KIVETELEK_TSV, nyelv='gorog'):
    return {r['alak']: r['kiejtes'] for r in _tsv_dict_sorok(ut) if r['nyelv'] == nyelv}


# ---------------------------------------------------------------------------
# Atiras
# ---------------------------------------------------------------------------

def atir(szoveg, szabalyok=None, kivetelek=None):
    """A fo fuggveny, harom lepesben:
    1) az egesz-alak kivetelek maszkolasa (hogy a kesz kivetel-szoveget a
       kesobbi szabalyok ne dolgozzak fel ujra -- pl. a 'sém' kivetel
       's'-je ne valjon 'sz'-sze);
    2) a sigma-sigma (σσ) geminacio maszkolasa -- ez NEM szerepel a
       szabalytablaban, mert az altalanos 's'->'sz' szabaly a maszkolas
       nelkul letrejovo 'ssz'-ben BENNE MARADO ket bar 's' betut ujra
       feldolgozna ('kérüsszó' helyett 'kérüszszó'/rosszabb lenne);
    2b) az αυ/ευ diftongusok maszkolasa -- a bennuk levo 'u' nem allo
       upsilon, nem valhat 'u'->'ü'-ve (l. καύχημα -> kauchēma marad
       'au', nem 'aü');
    3) a kiejtes_szabalyok.tsv szekvencialis, literalis cserei."""
    if szabalyok is None:
        szabalyok = szabalyok_betolt()
    if kivetelek is None:
        kivetelek = kivetelek_betolt()

    maszkok = {}
    for i, (alak, cel) in enumerate(kivetelek.items()):
        if alak and alak in szoveg:
            placeholder = _PLACEHOLDER_MINTA % i
            szoveg = szoveg.replace(alak, placeholder)
            maszkok[placeholder] = cel

    szoveg = szoveg.replace('SS', _SS_MASK_UPPER).replace('ss', _SS_MASK_LOWER)
    for minta, maszk in _DIFTONGUS_MASZK.items():
        szoveg = szoveg.replace(minta, maszk)

    for minta, csere in szabalyok:
        szoveg = szoveg.replace(minta, csere)

    szoveg = szoveg.replace(_SS_MASK_UPPER, 'SSZ').replace(_SS_MASK_LOWER, 'ssz')
    for minta, maszk in _DIFTONGUS_MASZK.items():
        szoveg = szoveg.replace(maszk, minta)

    for placeholder, cel in maszkok.items():
        szoveg = szoveg.replace(placeholder, cel)

    return szoveg


# ---------------------------------------------------------------------------
# --ellenoriz: aranykeszlet-proba, szabaly-lefedettseg, leave-one-out
# ---------------------------------------------------------------------------

def _celkiejtes_tisztit(cel):
    """A tesztkeszlet nehany cellaja ', G####' utotagot visel (Strong-
    hivatkozas, nem a kiejtes resze) -- levagja."""
    if ', G' in cel:
        return cel.split(', G')[0]
    return cel


def ellenoriz_futtat(szabalyok=None, kivetelek=None, arany_ut=ARANY_TSV):
    szabalyok = szabalyok if szabalyok is not None else szabalyok_betolt()
    kivetelek = kivetelek if kivetelek is not None else kivetelek_betolt()
    parok = list(_tsv_dict_sorok(arany_ut))

    print('=== S1.3 kiejtes.py --ellenoriz ===')
    print('Aranykeszlet (naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv, gorog, arany): '
          '30 egyedi par, ebbol 26 "tiszta" (szo-/kifejezes-szintu, toldas nelkuli) '
          'par tesztelheto itt automatikusan; 4 kontextus-fuggo (nevelo-/rovidites-'
          'toldassal) par nem, l. a %s fejleceben es a jelentes vegen.' % arany_ut)
    print('Ebben a futasban vizsgalt parok szama: %d' % len(parok))
    print()

    # --- fo proba: minden par az EGESZ szabalytabla + kivetelek mellett ---
    talalatok = []
    hasznalt_szabaly_parhoz = {}  # sorszam(int-kent nem all rendelkezesre kulon, index szerint) -> {par_idx,...}
    szabaly_hasznalat = [set() for _ in szabalyok]

    for i, sor in enumerate(parok):
        forras = sor['sbl_forras']
        cel = _celkiejtes_tisztit(sor['cel_kiejtes'])
        eredmeny = atir(forras, szabalyok, kivetelek)
        ok = eredmeny == cel
        talalatok.append((sor, eredmeny, ok))
        for j, (minta, _csere) in enumerate(szabalyok):
            if minta in forras:
                szabaly_hasznalat[j].add(i)

    sikeres = sum(1 for _, _, ok in talalatok if ok)
    print('Fo proba: %d/%d par egyezik pontosan.' % (sikeres, len(parok)))
    for sor, eredmeny, ok in talalatok:
        if not ok:
            print('  ELTER: %r -> %r (vart: %r)' % (
                sor['sbl_forras'], eredmeny, _celkiejtes_tisztit(sor['cel_kiejtes'])))
    print()

    # --- szabalyonkenti lefedettseg ---
    print('Szabalyonkenti lefedettseg (hany par forrasa tartalmazza a mintat):')
    egypart_lefedo = []
    for j, (minta, csere) in enumerate(szabalyok):
        n = len(szabaly_hasznalat[j])
        cimke = ' <-- 1 part fed le, KIVETEL-JELOLT, nem mozgatva' if n == 1 else ''
        print('  #%d %r -> %r: %d par%s' % (j + 1, minta, csere, n, cimke))
        if n == 1:
            par_idx = next(iter(szabaly_hasznalat[j]))
            egypart_lefedo.append((j, minta, csere, par_idx))
    print()

    if not egypart_lefedo:
        print('Egyetlen szabaly sem fed le pontosan 1 part -- nincs kivetel-jelolt.')
    else:
        print('1 part lefedo szabalyok (kivetel-jeloltek, %d db):' % len(egypart_lefedo))
        for j, minta, csere, par_idx in egypart_lefedo:
            print('  #%d %r -> %r -- egyedul a(z) %r par hasznalja (forras: %r)'
                  % (j + 1, minta, csere, parok[par_idx]['szo_gorog'], parok[par_idx]['sbl_forras']))
    print()

    # --- kihagyasos (leave-one-out) proba ---
    print('Kihagyasos (leave-one-out) proba: minden 1-part-lefedo szabalyt '
          'egyenkent eltavolitva ujrafuttatjuk a TELJES 26 paros keszletet -- '
          'elvart eredmeny: PONTOSAN a sajat parja bukik el, semmi mas nem '
          'valtozik. (Ez nem klasszikus per-pelda leave-one-out, mert a '
          'szabalyok nem par-specifikusan "tanultak", hanem kezzel, a teljes '
          'aranykeszletre egyszerre levezetett altalanos fonetikai szabalyok -- '
          'igy az egyetlen mechanikusan ismetelheto valtozat az, hogy egy '
          'szabaly KIVETELET elhagyva izolaltan bukik-e csak a sajat parja.)')
    if not egypart_lefedo:
        print('  Nincs 1-part-lefedo szabaly, a proba nem alkalmazhato -- kihagyva.')
    else:
        for j, minta, csere, par_idx in egypart_lefedo:
            csokkentett = szabalyok[:j] + szabalyok[j + 1:]
            uj_hibak = []
            for i, sor in enumerate(parok):
                forras = sor['sbl_forras']
                cel = _celkiejtes_tisztit(sor['cel_kiejtes'])
                eredmeny = atir(forras, csokkentett, kivetelek)
                if eredmeny != cel:
                    uj_hibak.append(i)
            if uj_hibak == [par_idx]:
                print('  #%d %r kihagyva: RENDBEN -- kizarolag a sajat parja '
                      '(%r) bukik, semmi mas' % (j + 1, minta, parok[par_idx]['szo_gorog']))
            elif par_idx not in uj_hibak:
                print('  #%d %r kihagyva: GYANUS -- a sajat parja (%r) NEM '
                      'bukott el kihagyas utan (masik szabaly is fedezi?)'
                      % (j + 1, minta, parok[par_idx]['szo_gorog']))
            else:
                tobbi = [parok[k]['szo_gorog'] for k in uj_hibak if k != par_idx]
                print('  #%d %r kihagyva: GYANUS -- a sajat parjan kivul mas '
                      'par(ok) is elbuktak: %r' % (j + 1, minta, tobbi))
    print()

    print('MEGJEGYZES: a fenti 100%%-os (vagy annal alacsonyabb) egyezes '
          'ONMAGABAN NEM elfogadasi erv -- a lefedettsegi es kihagyasos '
          'reszlet egyutt ertekelendo (SZOTAR_BRIEF.md D31 mintajara).')

    return sikeres, len(parok), talalatok


# ---------------------------------------------------------------------------
# Onteszt
# ---------------------------------------------------------------------------

def _onteszt_maszkolas():
    szabalyok = [('s', 'sz')]
    kivetelek = {'shem': 'sém'}
    # 'shem' -> kivetel 'sém'; az utana futo s->sz szabaly NEM erintheti
    # a mar behelyettesitett 'sém' szot ujra (nem valhat 'szém'-me).
    eredmeny = atir('shem', szabalyok, kivetelek)
    assert eredmeny == 'sém', eredmeny
    print('onteszt: maszkolas (kivetel utani szabaly nem dolgozza fel ujra) -- RENDBEN')


def _onteszt_sorrend():
    szabalyok = szabalyok_betolt()
    # ou elott u: "ou" ne alakuljon "oü"-ve
    assert atir('kaloumenos', szabalyok, {}) == 'kalúmenosz', atir('kaloumenos', szabalyok, {})
    # ss elott s: "kērussō" -> "kérüsszó", nem "kérüszszó"
    assert atir('kērussō', szabalyok, {}) == 'kérüsszó', atir('kērussō', szabalyok, {})
    print('onteszt: szabaly-sorrend (ou/u, ss/s) -- RENDBEN')


def onteszt_futtat():
    _onteszt_maszkolas()
    _onteszt_sorrend()
    print('minden onteszt RENDBEN')


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--atir', metavar='SZOVEG', help='egyetlen SBL-atiratu szoveg atirasa es kiirasa')
    ap.add_argument('--ellenoriz', action='store_true', help='aranykeszlet-proba, nem ir')
    ap.add_argument('--onteszt', action='store_true', help='halozat/fajl nelkuli onellenorzes')
    args = ap.parse_args()

    if args.onteszt:
        onteszt_futtat()
        return 0

    if args.atir is not None:
        print(atir(args.atir))
        return 0

    if args.ellenoriz:
        ellenoriz_futtat()
        return 0

    ap.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
