#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brief_lezaras.py -- gepi lezaras a merge-kor (DT-F219a; M-GAZDATLAN hibanaplo-mechanizmus).

A gyokerok: a session a draft PR-nal zarja a menetet, a fejlecebe "megallt / Te: merge" kerul, a merge
kesobb, a session nelkul tortenik, es utana semmi nem allitotta `lezarva`-ra a briefet, es nem zarta le a
brief altal teljesitett N-teteleket. Ez a szkript a `feladatok.yml` (main-re futo gepi Action) egy lepese:
a main-en mar mergelt PR briefjet `lezarva`-ra allitja, es a `lezar:` fejlecmezo N-teteleit a
`NYITOTT_FELADATOK.md` meglevo lezarasi formaja szerint lezarja.

A LEZARAS PONTOS FELTETELE (mindegyik egyszerre; a mai fejlecmezokbol levezetve):
  1. tipus: feladat vagy naplozas; allapot: `fut` vagy `megallt` (a `dontesre_var`, `nem_indult`, `brief_kell`
     nem: ott a merge nem az utolso hatralevo lepes);
  2. a `kovetkezo` mezo `Te:`-vel kezdodik (a felhasznalo/orkesztrator van soron, nem egy session), megnevezi a
     merge-et, es nem nevez meg semmi mast: nincs benne `utana`/`utan`, ⛔, dontes/DT-szam, `hatra`, `maradek`,
     `nyitva`, N-tetel, `elteres_kor`, `korlat`, `ujragener`, `meres` (ezek mind „meg van mas teendo” jelek);
  3. a briefnek van `ag:` mezeje, vagy `pr:` mezeje, es a main first-parent tortenetben van olyan PR-merge,
     amelynek az agneve = `ag`, vagy a szama = `pr`;
  4. a brief `allapot`, `kovetkezo` es `lezar` mezoje a merge PR-agan (a merge masodik szuloje; squash-nal a
     commit maga) UGYANAZ, mint ma a main-en: azaz a merge ota senki nem nyult a menet allapotahoz (ha igen, a
     menet folytatodott, a gep nem dont helyette).
Ha barmelyik nem teljesul, a gep NEM nyul a briefhez; az `ellenoriz` kapu JELENTESBEN mutatja (B resz).

A `lezar: [N-F200d, N152]` mezo azoknak az N-tetelnek a listaja, amelyeket a brief teljesit. A lezaraskor a
`NYITOTT_FELADATOK.md` megfelelo felsorolasi sora az N153 mintajara kapja: `**N<n> — LEZÁRVA (<datum>, a #<PR>
merge-evel, F<nn>) — ...`. A helyorzo (`N-F..`) a szamkiosztas utan veglegesszam; a Action a szamkiosztas UTAN
fut. Ismeretlen / mar lezart tetel: nincs valtozas, a jelentes jelzi.

    python eszkozok/brief_lezaras.py --szaraz        # csak a jelentes: mit zarna le (a mai main-en is hasznalhato)
    python eszkozok/brief_lezaras.py --ir            # a fejleceket es a NYITOTT_FELADATOK.md-t irja
    python eszkozok/brief_lezaras.py --ir --uzenet-fajl FAJL   # a commit uzenet torzsenek sorai
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import date

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402

REPO = F.REPO
NYITOTT = 'NYITOTT_FELADATOK.md'

LEZARHATO_ALLAPOT = ('fut', 'megallt')
LEZARHATO_TIPUS = ('feladat', 'naplozas')
# „meg van mas teendo” jelek a `kovetkezo` szovegeben (kisbetus, ekezettel); a merge-en tuli munka
BLOKKOLO = re.compile(
    r'utána|után|⛔|döntés|döntend|\bDT-?F?\d|hátra|maradék|nyitva|nyitott|elteres_kor|korlát|újragener|'
    r'mérés|\bN-?F?\d+|\bM\d\b|Folytatás',
    re.IGNORECASE)
MERGE_SZO = re.compile(r'merge|mergel', re.IGNORECASE)

PR_MERGE = re.compile(r'^Merge pull request #(\d+) from [^/\s]+/(\S+)')
PR_SQUASH = re.compile(r'\(#(\d+)\)\s*$')
N_AZON = re.compile(r'^\s*(?:[-*]|\d+\.)\s*\**\s*(N-F\d+[a-z]*|N\d+)\b')


def _olvas(ut):
    """Fajl szovege (UTF-8, sorvegek valtozatlanul); hianyzo fajl: ures szoveg."""
    if not os.path.exists(ut):
        return ''
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()


def _git(gyoker, *args):
    p = subprocess.run(['git', '-c', 'core.quotepath=false'] + list(args), cwd=gyoker, capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', 'replace')


def pr_merge_terkep(gyoker, ref='HEAD'):
    """A first-parent PR-merge-ek: [(commit, fa_commit, pr_szam, ag)], legfrissebb elol.
    `fa_commit`: a PR agenak tartalma (merge masodik szuloje; squash-nal a commit maga)."""
    rc, ki = _git(gyoker, 'log', '--first-parent', '--format=%H%x09%P%x09%s', ref)
    eredmeny = []
    if rc != 0:
        return eredmeny
    for sor in ki.split('\n'):
        r = sor.split('\t', 2)
        if len(r) < 3:
            continue
        sha, szulok, tema = r[0], r[1].split(), r[2]
        m = PR_MERGE.match(tema)
        if m and len(szulok) >= 2:
            eredmeny.append((sha, szulok[1], int(m.group(1)), m.group(2)))
            continue
        m = PR_SQUASH.search(tema)
        if m:
            eredmeny.append((sha, sha, int(m.group(1)), None))
    return eredmeny


def pr_szam_fejbol(fej):
    """A `pr:` fejlecmezo szama (szam vagy .../pull/N URL), vagy None."""
    nyers = str(fej.get('pr', '')).strip().strip('"\'')
    m = re.search(r'(\d+)\s*$', nyers)
    return int(m.group(1)) if m else None


def lezar_lista(szoveg):
    """A `lezar:` fejlecmezo elemei a brief SZOVEGEBOL (nyersen olvassa: a main-en egy regebbi `feladatok.py`
    is fut, ha a Action egy elavult checkoutot kap; a mezo a KULCSOK-ban a B. resz (F219) ota szerepel)."""
    sorok = szoveg.replace('\r\n', '\n').split('\n')
    if not sorok or sorok[0].lstrip('﻿').strip() != '---':
        return []
    for sor in sorok[1:]:
        if sor.strip() == '---':
            break
        m = re.match(r'^lezar:\s*(.*?)\s*$', sor)
        if m:
            nyers = m.group(1).strip()
            if nyers.startswith('[') and nyers.endswith(']'):
                nyers = nyers[1:-1]
            return [x.strip().strip('"\'') for x in nyers.split(',') if x.strip().strip('"\'')]
    return []


# olyan fejlecmezok, amelyeket egy regebbi fejlec-elemzo meg ismeretlen kulcskent hibaztat (nem akadaly)
UJ_KULCSOK = ('lezar',)


def hibak_akadaly(b):
    """Van-e a briefnek valodi fejlec-hibaja (az `UJ_KULCSOK` ismeretlen-kulcs hibai nem szamitanak)."""
    return any(not any(h.endswith('ismeretlen kulcs: %s' % k) for k in UJ_KULCSOK) for h in b.hibak)


def csak_merge_hatra(b):
    """A feltetel 1-2. pontja: (igen/nem, ok). A `kovetkezo` szovege csak a merge-et nevezi meg."""
    fej = b.fej
    if fej.get('tipus') not in LEZARHATO_TIPUS:
        return False, 'tipus: %s' % fej.get('tipus')
    if b.allapot not in LEZARHATO_ALLAPOT:
        return False, 'allapot: %s' % b.allapot
    kov = F._kov_szoveg(b)
    if not kov.startswith(F.VAR_RAD_ELOTAG):
        return False, 'a kovetkezo nem `Te:`-vel kezdodik'
    if not MERGE_SZO.search(kov):
        return False, 'a kovetkezo nem nevezi meg a merge-et'
    m = BLOKKOLO.search(kov)
    if m:
        return False, 'a kovetkezo mas teendot is jelez (%r)' % m.group(0)
    return True, 'csak a merge volt hatra'


def _fej_ertekek(szoveg):
    fej, _, _ = F.fejlec_elemez(szoveg)
    return (fej.get('allapot'), F._kov_szoveg(F.Brief('', fej, '', [])), tuple(lezar_lista(szoveg)))


def merge_a_brieffel(b, terkep, gyoker, ref='HEAD'):
    """A feltetel 3-4. pontja: a brief merge-elt PR-ja (commit, pr_szam, ag), vagy (None, ok)."""
    ag = b.fej.get('ag', '').strip().strip('"\'')
    pr = pr_szam_fejbol(b.fej)
    if not ag and pr is None:
        return None, 'nincs `ag:` vagy `pr:` mezo'
    jeloltek = [t for t in terkep if (ag and t[3] == ag) or (pr is not None and t[2] == pr)]
    if not jeloltek:
        return None, 'a main-en nincs ilyen PR-merge (ag=%s, pr=%s)' % (ag or '-', pr)
    ma = _fej_ertekek(_olvas(os.path.join(gyoker, b.fajl)))
    for sha, fa, pr_szam, _ag in jeloltek:      # legfrissebb elol
        rc, ki = _git(gyoker, 'show', '%s:%s' % (fa, b.fajl))
        if rc != 0:
            continue
        if _fej_ertekek(ki) == ma:
            return (sha, pr_szam, _ag), 'a PR-agon ugyanez volt az allapot'
    return None, 'a brief allapota a merge ota valtozott (a menet folytatodott)'


def lezarando(gyoker=REPO, ref='HEAD'):
    """[(brief, pr_szam)] a lezarhato briefek, es [(brief, ok)] a nem lezarhatok (csak a merge-elt PR-uak)."""
    briefek = F.briefek_beolvas(gyoker)
    terkep = pr_merge_terkep(gyoker, ref)
    lezar, kihagy = [], []
    for b in briefek:
        if b.szam is None or b.allapot == 'lezarva' or hibak_akadaly(b):
            continue
        mehet, ok = csak_merge_hatra(b)
        mergelve, ok2 = merge_a_brieffel(b, terkep, gyoker, ref) if mehet else (None, None)
        if mehet and mergelve:
            lezar.append((b, mergelve[1]))
        elif mehet:
            kihagy.append((b, ok2))
        else:
            # a merge-elt PR-u, de nem lezarhato: ezt a kapu jelenti (nem merge-elt briefek nem erdekesek)
            if any((b.fej.get('ag', '').strip().strip('"\'') == t[3]) or
                   (pr_szam_fejbol(b.fej) == t[2]) for t in terkep):
                kihagy.append((b, ok))
    return lezar, kihagy


# ---------------------------------------------------------------------------
# a NYITOTT_FELADATOK.md lezarasa
# ---------------------------------------------------------------------------

def nyitott_sor_lezar(sor, azon, datum, pr_szam, feladat):
    """Egy felsorolasi sor lezarasa (az N153 mintajara). Visszaad: (uj_sor, allapot):
    'lezarva' | 'mar_lezart' | 'nem_ez' (a sor nem az `azon` tetel definicioja)."""
    m = N_AZON.match(sor)
    if not m or m.group(1) != azon:
        return sor, 'nem_ez'
    if 'LEZÁRVA' in sor[:m.end() + 160]:
        return sor, 'mar_lezart'
    jel = 'LEZÁRVA (%s, a #%d PR merge-ével, F%d)' % (datum, pr_szam, feladat)
    # a minta: `**N153 — LEZÁRVA (...):** …`; mi a felkover jelolest tarto sorban a kotojel utan szurjuk be
    szunet = ' — '
    i = sor.find(szunet, m.start(1))
    if i < 0:
        szunet = ' -- '
        i = sor.find(szunet, m.start(1))
    if i < 0:
        return sor[:m.end(1)] + ' — ' + jel + ' —' + sor[m.end(1):], 'lezarva'
    return sor[:i] + szunet + jel + szunet + sor[i + len(szunet):], 'lezarva'


def nyitott_lezar(szoveg, azonok, datum, pr_szam, feladat):
    """Az `azonok` N-tetelek lezarasa a szovegben. Visszaad: (uj_szoveg, {azon: allapot}).
    allapot: 'lezarva' | 'mar_lezart' | 'nincs' (a definicios sor nem talalhato)."""
    sorok = szoveg.split('\n')
    jelentes = {}
    for azon in azonok:
        jelentes[azon] = 'nincs'
        for i, sor in enumerate(sorok):
            uj, al = nyitott_sor_lezar(sor, azon, datum, pr_szam, feladat)
            if al == 'nem_ez':
                continue
            sorok[i] = uj
            jelentes[azon] = al
            break
    return '\n'.join(sorok), jelentes


def nyitva_maradt(szoveg, azon):
    """A kapu 2. resze: a definicios sor megvan, es nincs lezarva (True); None, ha a sor nincs meg."""
    for sor in szoveg.split('\n'):
        m = N_AZON.match(sor)
        if m and m.group(1) == azon:
            return 'LEZÁRVA' not in sor[:m.end() + 160]
    return None


def brief_lezar_szoveg(szoveg, pr_szam, datum):
    """A brief szovege `lezarva` allapotra: allapot + kovetkezo (a `lezarva_osszegzes` marad, ha van)."""
    crlf = '\r\n' in szoveg          # a Windows-os munkafa CRLF-es; a fejlec-csere LF-re epul
    szoveg = szoveg.replace('\r\n', '\n')
    szoveg = F._fej_sor_csere(szoveg, 'allapot', 'lezarva')
    szoveg = F._fej_sor_csere(
        szoveg, 'kovetkezo',
        '"lezárva: a PR #%d mergelve (%s, gépi lezárás: eszkozok/brief_lezaras.py)"' % (pr_szam, datum))
    return szoveg.replace('\n', '\r\n') if crlf else szoveg


def kapu_jelentesek(gyoker=REPO, ref='HEAD'):
    """A `feladatok.py ellenoriz` kapuja (B resz; JELENTES, nem HIBA, amig a regi esetek takaritasa tart):
    (1) a brief PR-ja mergelve van a main-en, de a fejlece nem `lezarva`;
    (2) a lezart brief `lezar:` N-tetele nyitva maradt a NYITOTT_FELADATOK.md-ben.
    Visszaad: [(brief_fajl, szoveg)]."""
    briefek = F.briefek_beolvas(gyoker)
    terkep = pr_merge_terkep(gyoker, ref)
    nyitott_ut = os.path.join(gyoker, NYITOTT)
    nyitott = _olvas(nyitott_ut)
    sorok = []
    for b in briefek:
        if b.szam is None or b.fej.get('tipus') not in LEZARHATO_TIPUS:
            continue
        ag = b.fej.get('ag', '').strip().strip('"\'')
        pr = pr_szam_fejbol(b.fej)
        if b.allapot != 'lezarva':
            for t in terkep:
                if (ag and t[3] == ag) or (pr is not None and t[2] == pr):
                    sorok.append((b.fajl, 'a PR #%d mergelve a main-en, de a fejléc `allapot: %s` (nem `lezarva`)'
                                  % (t[2], b.allapot)))
                    break
            continue
        with open(os.path.join(gyoker, b.fajl), encoding='utf-8', newline='') as f:
            azonok = lezar_lista(f.read())
        for azon in azonok:
            if nyitva_maradt(nyitott, azon):
                sorok.append((b.fajl, 'a lezárt brief `lezar:` tétele (%s) nyitva maradt a %s-ben' % (azon, NYITOTT)))
    return sorok


def vegrehajt(gyoker=REPO, szaraz=True, ref='HEAD', datum=None, uzenet_fajl=None):
    datum = datum or date.today().isoformat()
    lezar, kihagy = lezarando(gyoker, ref)
    nyitott_ut = os.path.join(gyoker, NYITOTT)
    nyitott = _olvas(nyitott_ut)
    sorok = []
    ossz_n = 0
    for b, pr_szam in lezar:
        with open(os.path.join(gyoker, b.fajl), encoding='utf-8', newline='') as f:
            azonok = lezar_lista(f.read())
        nyitott, jel = nyitott_lezar(nyitott, azonok, datum, pr_szam, b.szam)
        lezart = [a for a, al in jel.items() if al == 'lezarva']
        ossz_n += len(lezart)
        resz = ', '.join('%s: %s' % kv for kv in jel.items())
        sorok.append('LEZÁR  %s  (PR #%d; N-tételek: %s)' % (b.fajl, pr_szam, resz or '-'))
        if not szaraz:
            ut = os.path.join(gyoker, b.fajl)
            with open(ut, encoding='utf-8', newline='') as f:
                szoveg = f.read()
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write(brief_lezar_szoveg(szoveg, pr_szam, datum))
    if not szaraz and ossz_n:
        with open(nyitott_ut, 'w', encoding='utf-8', newline='') as f:
            f.write(nyitott)
    for b, ok in kihagy:
        sorok.append('KIHAGY %s  (%s)' % (b.fajl, ok))
    sorok.append('Összesen: %d brief %s, %d N-tétel %s.' % (
        len(lezar), 'lezárva' if not szaraz else 'zárna le (--szaraz)', ossz_n,
        'lezárva' if not szaraz else 'zárna le'))
    if uzenet_fajl and lezar and not szaraz:
        with open(uzenet_fajl, 'w', encoding='utf-8', newline='') as f:
            f.write('brief-lezárás: %s\n' % ', '.join('#%d' % b.szam for b, _ in lezar))
    return lezar, kihagy, sorok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--szaraz', action='store_true', help='csak jelentes (alapertelmezett)')
    g.add_argument('--ir', action='store_true', help='a fejleceket es a NYITOTT_FELADATOK.md-t irja')
    g.add_argument('--kapu', action='store_true', help='a ket kapu jelentese (merge-elt, de nem lezart brief; nyitva maradt lezar-tetel)')
    ap.add_argument('--gyoker', default=REPO)
    ap.add_argument('--ref', default='HEAD', help='a PR-merge-ek tortenete (alapertelmezett: HEAD)')
    ap.add_argument('--datum', default=None, help='lezarasi datum (alapertelmezett: ma)')
    ap.add_argument('--uzenet-fajl', default=None)
    a = ap.parse_args()
    if a.kapu:
        for fajl, szoveg in kapu_jelentesek(a.gyoker, a.ref):
            print('JELENTÉS  %s: %s' % (fajl, szoveg))
        return 0
    _, _, sorok = vegrehajt(a.gyoker, szaraz=not a.ir, ref=a.ref, datum=a.datum, uzenet_fajl=a.uzenet_fajl)
    print('\n'.join(sorok))
    return 0


if __name__ == '__main__':
    sys.exit(main())
