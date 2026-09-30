#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.11 — a C (F3) linkjeinek diffje az Opus-aranyhoz és a régi aranyhoz.

Nincs API-hívás, nincs titok. A betöltés, a linkhalmaz, a kizárás és a régi
arany egyezése a meres.py azonosítóival és függvényeivel (meres.Adat,
Adat.linkek, Adat.arany_linkek, meres._kifejezes_helyek,
meres._hivatkozas_szavak) történik, tehát a diff pontosan a P4 számait bontja.

Hatókör (a P4 a) pontja szerint): az F3 kapun átment versei, azon belül az
aranyba eső 60 vers; a f21p/meres_kizaras.tsv tokenjeit érintő linkek mindkét
oldalról kimaradnak.
  * hiányzó = az arany szerint van, a C-nél nincs;
  * többlet = a C-nél van, az aranyban nincs.
Régi arany: a C 200 verses mintájának régi-arany-hármasai (kapun átment
versek); a nem egyezőket listázza.

Módok:
  python eszkozok/karoli_strong/c_diff.py --lista
      versenként a hiányzó/többlet linkek (magyar szó; eredeti alak, tükör,
      Strong) és a nem egyező régi-arany-hármasok — a kézi besorolás alapja.
  python eszkozok/karoli_strong/c_diff.py
      ellenőrzi, hogy a f21p/c_diff_besorolas.tsv és a
      f21p/c_regi_arany_besorolas.tsv pontosan a gépi eltéréseket fedi (minden
      eltérésnek van besorolása és fordítva, érvényes osztállyal), majd megírja a
      naplok/F21P_C_diff.md-t. Eltérésnél kilépési kód 1, és nem ír.

A besorolás (osztály, konvenció/jegyzetpont, indok) kézi ítélet (Opus), nem mérés;
a jelentés ezt jelöli. Osztályok: a = konvenciókülönbség (arany_opus_jegyzetek.md
2. szakasz, 1–10. konvenció), b = az arany vitatható döntése (a jegyzet 6.
szakaszának táblázata), c = a C valódi hibája; a régi aranynál ezeken felül
d = a régi arany hibás; e = mérési műtermék (a régi arany összetett, „+”-os
Strongja, amelyet a meres.py egész karakterláncként hasonlít — ez az osztály a
megadott a–d felosztáson túli, jelzett eltérés).
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meres  # noqa: E402
import tokenek  # noqa: E402

FUTAS = 'F3'
BESOROLAS_UT = os.path.join(tokenek.ROOT, 'f21p', 'c_diff_besorolas.tsv')
REGI_BESOROLAS_UT = os.path.join(tokenek.ROOT, 'f21p', 'c_regi_arany_besorolas.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_C_diff.md')
BES_OSZLOPOK = ['igehely', 'reteg', 'irany', 'k_poz', 'e_poz', 'osztaly', 'konvencio_vagy_jegyzetpont', 'indok']
REGI_OSZLOPOK = ['igehely', 'karoli_szo', 'strong', 'osztaly', 'c_link', 'indok']
OSZTALYOK = ('a', 'b', 'c')
REGI_OSZTALYOK = ('a', 'b', 'c', 'd', 'e')
IRANYOK = ('hianyzo', 'tobblet')

# a jelentés jellemző példái (igehely, irany, k_poz, e_poz); a (c) esetek mind
# listázódnak, ezektől függetlenül
PELDAK = [
    ('2Móz 21:6', 'hianyzo', 6, 5),
    ('2Móz 20:25', 'tobblet', 9, 10),
    ('2Móz 20:25', 'tobblet', 14, 13),
    ('2Móz 21:26', 'tobblet', 1, 1),
    ('2Móz 25:8', 'tobblet', 7, 10),
    ('2Móz 26:13', 'tobblet', 11, 12),
    ('Péld 30:17', 'tobblet', 10, 7),
    ('Zsolt 16:11', 'tobblet', 1, 1),
    ('Zsolt 18:1', 'tobblet', 14, 18),
    ('Zsolt 18:3', 'tobblet', 22, 19),
    ('Jer 51:3', 'tobblet', 2, 2),
    ('Ez 11:3', 'tobblet', 1, 1),
    ('Ez 39:13', 'tobblet', 3, 2),
    ('Mk 2:10', 'tobblet', 10, 13),
    ('1Pét 4:11', 'tobblet', 29, 28),
]
VITATHATO_JEL = '[az arany döntése is vitatható'


# ---------------------------------------------------------------------------
# gépi diff
# ---------------------------------------------------------------------------

def gepi_elteresek(adat):
    """[(igehely, reteg, irany, k, e)] versenként rendezve (minta-sorrend)."""
    ki = []
    for ig in adat.versek:
        if ig not in adat.arany or not adat.ok(FUTAS, ig):
            continue
        c, g = adat.linkek(FUTAS, ig), adat.arany_linkek(ig)
        for k, e in sorted(g - c):
            ki.append((ig, adat.reteg[ig], 'hianyzo', k, e))
        for k, e in sorted(c - g):
            ki.append((ig, adat.reteg[ig], 'tobblet', k, e))
    return ki


def regi_elteresek(adat):
    """A C régi-arany-hármasai a kapun átment versekben: [(ig, szo, strong, egyezik, c_szavak)]."""
    ki = []
    for ig, szo, strong in adat.regi:
        if not adat.ok(FUTAS, ig):
            continue
        tl = tokenek.tokenizal(adat.karoli[ig])
        kif = tokenek.tokenizal(szo)
        helyek = meres._kifejezes_helyek(tl, kif)
        lk = adat.linkek(FUTAS, ig)
        kszavak = meres._hivatkozas_szavak(adat, ig, lk)
        egyezik = bool(helyek) and any(strong in kszavak.get(i + j + 1, set())
                                       for i in helyek for j in range(len(kif)))
        poz = sorted({i + j + 1 for i in helyek for j in range(len(kif))})
        c_szavak = {p: sorted(e for k, e in lk if k == p) for p in poz}
        ki.append((ig, szo, strong, egyezik, c_szavak))
    return ki


def _eredeti(adat, ig, e):
    w = adat.ered[ig][e - 1]
    return '%d %s %s [%s]%s' % (e, w['alak'], w['strong'], w['tukor'], ' [nem TR]' if w['nem_tr'] else '')


def _magyar(adat, ig, k):
    return '%d %s' % (k, tokenek.tokenizal(adat.karoli[ig])[k - 1])


def lista(adat):
    el = gepi_elteresek(adat)
    aktualis = None
    for ig, ret, irany, k, e in el:
        if ig != aktualis:
            aktualis = ig
            c, g = adat.linkek(FUTAS, ig), adat.arany_linkek(ig)
            print('=' * 60)
            print('%s [%s]  C: %d link, arany: %d link, közös: %d' % (ig, ret, len(c), len(g), len(c & g)))
        print('  %-8s %-22s -> %s' % (irany, _magyar(adat, ig, k), _eredeti(adat, ig, e)))
    print()
    print('## régi arany (C, kapun átment versek)')
    for ig, szo, strong, egyezik, c_szavak in regi_elteresek(adat):
        if egyezik:
            continue
        print('%s | %s | %s | C: %s' % (ig, szo, strong, '; '.join(
            '%s -> %s' % (_magyar(adat, ig, p), ', '.join(_eredeti(adat, ig, e) for e in es) or '—')
            for p, es in c_szavak.items())))
    n = len(el)
    print('\nösszesen: %d eltérés (hiányzó %d, többlet %d)' % (
        n, sum(1 for x in el if x[2] == 'hianyzo'), sum(1 for x in el if x[2] == 'tobblet')))


# ---------------------------------------------------------------------------
# besorolás beolvasása és ellenőrzése
# ---------------------------------------------------------------------------

def _tsv(ut, oszlopok):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip()]
    fej = sorok[0].split('\t')
    if fej != oszlopok:
        raise SystemExit('%s: hibás fejléc: %s' % (ut, fej))
    ki = []
    for i, s in enumerate(sorok[1:], 2):
        m = s.split('\t')
        if len(m) != len(oszlopok):
            raise SystemExit('%s %d. sor: %d mező (%d kell)' % (ut, i, len(m), len(oszlopok)))
        ki.append(dict(zip(oszlopok, m)))
    return ki


def ellenoriz(adat):
    hibak = []
    el = gepi_elteresek(adat)
    bes = _tsv(BESOROLAS_UT, BES_OSZLOPOK)
    gepi = {(ig, irany, k, e): ret for ig, ret, irany, k, e in el}
    kezi = {}
    for r in bes:
        kulcs = (r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))
        if kulcs in kezi:
            hibak.append('kétszer besorolva: %s' % (kulcs,))
        kezi[kulcs] = r
        if r['osztaly'] not in OSZTALYOK:
            hibak.append('érvénytelen osztály: %s %s' % (kulcs, r['osztaly']))
        if r['irany'] not in IRANYOK:
            hibak.append('érvénytelen irány: %s' % (kulcs,))
        if kulcs in gepi and r['reteg'] != gepi[kulcs]:
            hibak.append('réteg eltér: %s' % (kulcs,))
        if not r['indok'].strip():
            hibak.append('üres indok: %s' % (kulcs,))
        if r['osztaly'] in ('a', 'b') and not r['konvencio_vagy_jegyzetpont'].strip():
            hibak.append('(a)/(b) osztály konvenció/jegyzetpont nélkül: %s' % (kulcs,))
    for k in sorted(set(gepi) - set(kezi)):
        hibak.append('besorolás nélküli gépi eltérés: %s' % (k,))
    for k in sorted(set(kezi) - set(gepi)):
        hibak.append('gépi eltérés nélküli besorolás: %s' % (k,))
    regi = [x for x in regi_elteresek(adat) if not x[3]]
    rbes = _tsv(REGI_BESOROLAS_UT, REGI_OSZLOPOK)
    rgepi = {(ig, szo, strong) for ig, szo, strong, _, _ in regi}
    rkezi = {}
    for r in rbes:
        kulcs = (r['igehely'], r['karoli_szo'], r['strong'])
        if kulcs in rkezi:
            hibak.append('régi arany: kétszer besorolva: %s' % (kulcs,))
        rkezi[kulcs] = r
        if r['osztaly'] not in REGI_OSZTALYOK:
            hibak.append('régi arany: érvénytelen osztály: %s' % (kulcs,))
    for k in sorted(rgepi - set(rkezi)):
        hibak.append('régi arany: besorolás nélküli eltérés: %s' % (k,))
    for k in sorted(set(rkezi) - rgepi):
        hibak.append('régi arany: eltérés nélküli besorolás: %s' % (k,))
    for p in PELDAK:
        if p not in kezi:
            hibak.append('a példa nem gépi eltérés: %s' % (p,))
    return hibak, el, kezi, regi, rkezi


# ---------------------------------------------------------------------------
# jelentés
# ---------------------------------------------------------------------------

def _pct(x, n):
    return '%.1f%% (%d/%d)' % (100.0 * x / n, x, n) if n else '— (0/0)'


def jelentes(adat, el, kezi, regi, rkezi):
    ret_lista = meres.RETEGEK + [meres.OSSZES]
    # alapszámok (a P4 definíciója szerint, újraszámolva)
    alap = {}
    for ret in ret_lista:
        vs = [ig for ig in adat.versek if ig in adat.arany and adat.ok(FUTAS, ig)
              and (ret == meres.OSSZES or adat.reteg[ig] == ret)]
        c = sum(len(adat.linkek(FUTAS, ig)) for ig in vs)
        g = sum(len(adat.arany_linkek(ig)) for ig in vs)
        t = sum(len(adat.linkek(FUTAS, ig) & adat.arany_linkek(ig)) for ig in vs)
        alap[ret] = (len(vs), c, g, t)
    szam = {}
    for (ig, irany, k, e), r in kezi.items():
        for ret in (adat.reteg[ig], meres.OSSZES):
            kk = (ret, irany, r['osztaly'])
            szam[kk] = szam.get(kk, 0) + 1

    ki = ['# F21P_C_diff.md — a C (F3) eltérései az Opus-aranytól és a régi aranytól', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/c_diff.py | scope=f21p F3, a kapun átment aranyversek '
          '(60) és a C régi-arany-hármasai | forras=f21p/valaszok/F3.jsonl, f21p/arany_opus.jsonl, '
          'f21p/meres_kizaras.tsv, f21p/c_diff_besorolas.tsv, f21p/c_regi_arany_besorolas.tsv, '
          'konkordancia/Karoli_Strong_kivonat.tsv | kézzel szerkeszteni tilos -->', '',
          '**A számok a szkript kimenetei** (a meres.py definícióival: link = (magyar sorszám, '
          'eredeti sorszám), a f21p/meres_kizaras.tsv tokenjei nélkül). **Az osztályba sorolás '
          'kézi ítélet (Opus, F21.11), nem mérés.** Osztályok: (a) konvenciókülönbség — a '
          'f21p/arany_opus_jegyzetek.md 2. szakaszának tíz konvenciója; (b) az arany vitatható '
          'döntése — a jegyzet 6. szakaszának táblázata; (c) a C valódi hibája az arany szerint; '
          'a régi aranynál (d) a régi arany hibás, (e) mérési műtermék (a megadott felosztáson '
          'túli osztály, l. 6. pont).', '']

    ki += ['## 1. Eltérések rétegenként és osztályonként', '',
           '| réteg | versek | C link | arany link | közös | hiányzó (a / b / c) | többlet (a / b / c) |',
           '|---|---|---|---|---|---|---|']
    for ret in ret_lista:
        n, c, g, t = alap[ret]
        h = [szam.get((ret, 'hianyzo', o), 0) for o in OSZTALYOK]
        tb = [szam.get((ret, 'tobblet', o), 0) for o in OSZTALYOK]
        ki.append('| %s | %d | %d | %d | %d | %d (%s) | %d (%s) |' % (
            ret, n, c, g, t, g - t, ' / '.join(map(str, h)), c - t, ' / '.join(map(str, tb))))
    ki.append('')
    ki += ['## 2. Pontosság és lefedettség: a P4 mérés és a korrigált érték', '',
           'A **P4** sor a meres.py definíciója (a f21p/meres_eredmeny.tsv C-sorával azonos kell '
           'legyen). A **korrigált** sor NEM mérés: az (a) és (b) osztályú eltéréseket a '
           '**kézi besorolás (Opus, F21.11)** alapján nem-hibának veszi — a többlet (a)/(b) '
           'linkeket a pontosság, a hiányzó (a)/(b) linkeket a lefedettség számlálójához '
           'adja. A korrekció tehát ítéletfüggő.', '',
           '| réteg | mérőszám | P4 (mérés) | korrigált (kézi besorolás alapján) |', '|---|---|---|---|']
    for ret in ret_lista:
        n, c, g, t = alap[ret]
        tob_ab = sum(szam.get((ret, 'tobblet', o), 0) for o in ('a', 'b'))
        hia_ab = sum(szam.get((ret, 'hianyzo', o), 0) for o in ('a', 'b'))
        ki.append('| %s | pontosság | %s | %s |' % (ret, _pct(t, c), _pct(t + tob_ab, c)))
        ki.append('| %s | lefedettség | %s | %s |' % (ret, _pct(t, g), _pct(t + hia_ab, g)))
    ki.append('')

    # konvenció/jegyzetpont szerinti bontás
    kp = {}
    for r in kezi.values():
        if r['osztaly'] in ('a', 'b'):
            kk = (r['osztaly'], r['konvencio_vagy_jegyzetpont'])
            kp[kk] = kp.get(kk, 0) + 1
    ki += ['## 3. Az (a) és (b) eltérések konvenció, ill. jegyzetpont szerint (kézi besorolás)', '',
           '| osztály | konvenció / jegyzetpont | eltérés (link) |', '|---|---|---|']
    for (o, p), x in sorted(kp.items()):
        ki.append('| %s | %s | %d |' % (o, p, x))
    ki.append('')

    def sor(kulcs):
        ig, irany, k, e = kulcs
        r = kezi[kulcs]
        return '| %s | %s | %s | %s | %s | %s | %s |' % (
            ig, irany, _magyar(adat, ig, k), _eredeti(adat, ig, e), r['osztaly'],
            r['konvencio_vagy_jegyzetpont'] or '—', r['indok'])

    fej = ['| vers | irány | magyar szó | eredeti szó (sorszám, alak, Strong, tükör) | osztály | konvenció / jegyzetpont | indok (kézi) |',
           '|---|---|---|---|---|---|---|']
    c_esetek = [kk for kk in sorted(kezi, key=lambda x: (adat.versek.index(x[0]), x[1], x[2], x[3]))
                if kezi[kk]['osztaly'] == 'c']
    vit = [kk for kk in c_esetek if VITATHATO_JEL in kezi[kk]['indok']]
    ki += ['## 4. A (c) esetek — a C valódi hibái az arany szerint (mind, kézi besorolás)', '',
           'Összesen %d (c) eltérés; ebből %d-nél az indok jelzi, hogy az arany döntése is vitatható, '
           'de a jegyzet 6. szakaszának táblázatában nem szerepel (a (b) definíciója ezért nem '
           'alkalmazható rájuk).' % (len(c_esetek), len(vit)), ''] + fej
    ki += [sor(kk) for kk in c_esetek]
    ki.append('')
    ki += ['## 5. Jellemző példák (a) és (b) osztályból (kézi válogatás)', ''] + fej
    ki += [sor(kk) for kk in PELDAK if kezi[kk]['osztaly'] != 'c']
    ki.append('')

    ki += ['## 6. A régi arany nem egyező hármasai (C, kapun átment versek)', '',
           'A régi arany egyezés a meres.py definíciója: a hármas egyezik, ha a Károli-szó '
           'valamelyik előfordulásához linkelt eredeti szavak között ott a Strong-szám. '
           'Összesen %d hármas, ebből nem egyezik %d. Az osztály kézi ítélet; (d) = a régi arany '
           '(konkordancia/Karoli_Strong_kivonat.tsv) maga a hibás.' % (
               len(regi_elteresek(adat)), len(regi)), '',
           '| vers | Károli-szó | régi Strong | a C linkje(i) ehhez a szóhoz | osztály | indok (kézi) |',
           '|---|---|---|---|---|---|']
    for ig, szo, strong, _, c_szavak in regi:
        r = rkezi[(ig, szo, strong)]
        clink = '; '.join('%s -> %s' % (_magyar(adat, ig, p), ', '.join(_eredeti(adat, ig, e) for e in es) or '—')
                          for p, es in c_szavak.items())
        ki.append('| %s | %s | %s | %s | %s | %s |' % (ig, szo, strong, clink, r['osztaly'], r['indok']))
    rsz = {}
    for r in rkezi.values():
        rsz[r['osztaly']] = rsz.get(r['osztaly'], 0) + 1
    ki += ['', '(e) = mérési műtermék: a Karoli_Strong_kivonat.tsv összetett Strongja („H5128+H5110”) '
           'a meres.py egyezésvizsgálatában egész karakterláncként szerepel, és egyetlen linkelt '
           'eredeti szó Strongjával sem lehet egyenlő. Az osztály a megadott a–d felosztáson túli.',
           '', 'Osztályonként (kézi): %s.' % ', '.join('(%s) %d' % (o, rsz.get(o, 0)) for o in REGI_OSZTALYOK), '']
    with open(JELENTES_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    return alap, szam


def main():
    adat = meres.Adat()
    if '--lista' in sys.argv:
        lista(adat)
        return 0
    hibak, el, kezi, regi, rkezi = ellenoriz(adat)
    if hibak:
        print('HIBA (a jelentés nem íródott):')
        for h in hibak:
            print('  ' + h)
        return 1
    alap, szam = jelentes(adat, el, kezi, regi, rkezi)
    n, c, g, t = alap[meres.OSSZES]
    print('gépi eltérés: %d (hiányzó %d, többlet %d); besorolva: %d; régi arany nem egyező: %d/%d, besorolva: %d'
          % (len(el), g - t, c - t, len(kezi), len(regi), len(regi_elteresek(adat)), len(rkezi)))
    for irany in IRANYOK:
        print('%s: %s' % (irany, ', '.join('(%s) %d' % (o, szam.get((meres.OSSZES, irany, o), 0)) for o in OSZTALYOK)))
    print('-> %s' % JELENTES_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
