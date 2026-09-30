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

F21.12 (felhasználói döntések):
  * a régi arany egyezése a meres.regi_egyezik halmaz-definíciójával (az
    összetett Strong minden összetevője); a f21p/c_regi_arany_besorolas.tsv a
    korábbi (összetett Strong nélküli) definíció 8 eltérését kontrollként őrzi,
    a jelentés mindkét definíció szerinti állapotot és a
    f21p/regi_arany_hibas.tsv kizárását mutatja;
  * v2-arany (f21p/arany_opus_v2.jsonl, ha létezik): a C diffje a v2-höz is; a
    v2-ben is meglévő eltérés a v1-besorolást örökli, az új eltérés a
    f21p/c_diff_besorolas_v2_uj.tsv-ben kap besorolást (a szkript ellenőrzi);
    a v1-es P4 és a v1-es C-diff nem íródik felül; a naplok/F21P_arany_v2_diff.md
    is innen generálódik (az arany_v2.JAVITASOK és a diff alapján).
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
ARANY_V2_UT = os.path.join(tokenek.ROOT, 'f21p', 'arany_opus_v2.jsonl')
V2_BESOROLAS_UJ_UT = os.path.join(tokenek.ROOT, 'f21p', 'c_diff_besorolas_v2_uj.tsv')
V2_DIFF_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_arany_v2_diff.md')
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

def arany_v2(adat):
    """{igehely: v2-objektum} vagy None, ha nincs v2."""
    if not os.path.exists(ARANY_V2_UT):
        return None
    tokenek.arany_v2_befagyasztas_ellenoriz(ARANY_V2_UT)   # F21.14: eltérésnél hibával megáll
    return {o['vers']: o for o in meres._jsonl(ARANY_V2_UT)}


def arany_fn(adat, arany):
    """Linkhalmaz-függvény egy arany-változatra (a meres.Adat kizárásával)."""
    if arany is None:
        return adat.arany_linkek
    return lambda ig: adat._szur(ig, {(p[0], e) for p in arany[ig]['parok'] for e in p[1]})


def gepi_elteresek(adat, g_fn=None):
    """[(igehely, reteg, irany, k, e)] versenként rendezve (minta-sorrend)."""
    g_fn = g_fn or adat.arany_linkek
    ki = []
    for ig in adat.versek:
        if ig not in adat.arany or not adat.ok(FUTAS, ig):
            continue
        c, g = adat.linkek(FUTAS, ig), g_fn(ig)
        for k, e in sorted(g - c):
            ki.append((ig, adat.reteg[ig], 'hianyzo', k, e))
        for k, e in sorted(c - g):
            ki.append((ig, adat.reteg[ig], 'tobblet', k, e))
    return ki


def regi_elteresek(adat):
    """A C régi-arany-hármasai a kapun átment versekben:
    [(ig, szo, strong, egyezik_korabbi, egyezik_halmaz, hibas_ok, c_szavak)].

    egyezik_korabbi: a korábbi (F21.10) definíció (összetett Strong nélkül,
    kontroll); egyezik_halmaz: a meres.regi_egyezik halmaz-definíciója (F21.12);
    hibas_ok: a f21p/regi_arany_hibas.tsv oka, ha a hármas hibásnak jelölt.
    """
    hibas = meres.regi_hibas()
    ki = []
    for ig, szo, strong in adat.regi:
        if not adat.ok(FUTAS, ig):
            continue
        lk = adat.linkek(FUTAS, ig)
        _, e_korabbi = meres.regi_egyezik(adat, ig, szo, strong, lk, halmaz=False)
        _, e_halmaz = meres.regi_egyezik(adat, ig, szo, strong, lk, halmaz=True)
        tl = tokenek.tokenizal(adat.karoli[ig])
        kif = tokenek.tokenizal(szo)
        helyek = meres._kifejezes_helyek(tl, kif)
        poz = sorted({i + j + 1 for i in helyek for j in range(len(kif))})
        c_szavak = {p: sorted(e for k, e in lk if k == p) for p in poz}
        ki.append((ig, szo, strong, e_korabbi, e_halmaz, hibas.get((ig, szo, strong), ''), c_szavak))
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
    print('## régi arany (C, kapun átment versek; a korábbi definíció szerint nem egyezők)')
    for ig, szo, strong, egyezik, e_halmaz, hibas_ok, c_szavak in regi_elteresek(adat):
        if egyezik:
            continue
        print('%s | %s | %s | halmaz: %s%s | C: %s' % (ig, szo, strong, 'egyezik' if e_halmaz else 'NEM',
                                                     ' | HIBÁS-jelölt' if hibas_ok else '', '; '.join(
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
    rgepi = {x[:3] for x in regi}
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
    # a halmaz-definíció szerint nem egyező hármas (d) osztályú és hibás-jelölt
    # kell legyen; minden hibás-jelölt hármas (d)
    for x in regi_elteresek(adat):
        kulcs, e_halmaz, hibas_ok = x[:3], x[4], x[5]
        if not e_halmaz and (kulcs not in rkezi or rkezi[kulcs]['osztaly'] != 'd' or not hibas_ok):
            hibak.append('régi arany: a halmaz-definíció szerint nem egyező hármas nem (d)/hibás-jelölt: %s' % (kulcs,))
        if hibas_ok and (kulcs not in rkezi or rkezi[kulcs]['osztaly'] != 'd'):
            hibak.append('régi arany: hibás-jelölt hármas nem (d) osztályú: %s' % (kulcs,))
    # v2: a v2-höz mért eltérés vagy örökli a v1-besorolást, vagy a v2_uj fájlban van
    v2 = arany_v2(adat)
    kezi_v2 = None
    el_v2 = []
    if v2 is not None:
        el_v2 = gepi_elteresek(adat, arany_fn(adat, v2))
        uj = {}
        if os.path.exists(V2_BESOROLAS_UJ_UT):
            for r in _tsv(V2_BESOROLAS_UJ_UT, BES_OSZLOPOK):
                uj[(r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))] = r
        kezi_v2 = {}
        for ig, ret, irany, k, e in el_v2:
            kulcs = (ig, irany, k, e)
            if kulcs in uj:
                kezi_v2[kulcs] = uj[kulcs]
            elif kulcs in kezi:
                kezi_v2[kulcs] = kezi[kulcs]
            else:
                hibak.append('v2: besorolás nélküli új eltérés: %s' % (kulcs,))
        for kulcs in sorted(set(uj) - {(x[0], x[2], x[3], x[4]) for x in el_v2}):
            hibak.append('v2: gépi eltérés nélküli v2-besorolás: %s' % (kulcs,))
    return hibak, el, kezi, regi, rkezi, el_v2, kezi_v2, v2


# ---------------------------------------------------------------------------
# jelentés
# ---------------------------------------------------------------------------

def _pct(x, n):
    return '%.1f%% (%d/%d)' % (100.0 * x / n, x, n) if n else '— (0/0)'


def jelentes(adat, el, kezi, regi, rkezi, el_v2=None, kezi_v2=None, v2=None):
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
          'f21p/arany_opus_v2.jsonl, f21p/regi_arany_hibas.tsv, konkordancia/Karoli_Strong_kivonat.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
          'kézzel szerkeszteni tilos -->' % tokenek.generalas_ts(), '',
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
           '| réteg | mérőszám | P4 (mérés) | korrigált (az Opus besorolása, nem mérés) |', '|---|---|---|---|']
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

    osszes_regi = regi_elteresek(adat)
    n_regi = len(osszes_regi)
    korabbi_ok = sum(1 for x in osszes_regi if x[3])
    halmaz_ok = sum(1 for x in osszes_regi if x[4])
    hibas_n = sum(1 for x in osszes_regi if x[5])
    halmaz_ok_k = sum(1 for x in osszes_regi if x[4] and not x[5])
    ki += ['## 6. A régi arany (C, kapun átment versek)', '',
           '**Definíció (F21.12, meres.regi_egyezik):** a régi Strong mezőt „+” mentén összetevőkre '
           'bontjuk; a hármas egyezik, ha a Károli-szó (kifejezés) valamelyik előfordulásához linkelt '
           'eredeti szavak Strongjai között MINDEN összetevő ott van. A korábbi (F21.10) definíció a '
           'Strong mezőt egész karakterláncként hasonlította, ezért összetett Strong sosem egyezhetett; '
           'az itt csak kontroll.', '',
           '| mérőszám | érték |', '|---|---|',
           '| egyezés — korábbi, összetett Strong nélkül (kontroll) | %s |' % _pct(korabbi_ok, n_regi),
           '| egyezés — halmaz-definíció, kizárás nélkül | %s |' % _pct(halmaz_ok, n_regi),
           '| kizárva: a régi arany hibás (f21p/regi_arany_hibas.tsv) | %d hármas |' % hibas_n,
           '| egyezés — halmaz-definíció, a hibás hármasok nélkül | %s |' % _pct(halmaz_ok_k, n_regi - hibas_n),
           '',
           'A korábbi definíció szerint nem egyező %d hármas (kontroll). Az osztály kézi ítélet; '
           '(d) = a régi arany (konkordancia/Karoli_Strong_kivonat.tsv) maga a hibás.' % len(regi), '',
           '| vers | Károli-szó | régi Strong | a C linkje(i) ehhez a szóhoz | halmaz-definíció | hibás-jelölés | osztály | indok (kézi) |',
           '|---|---|---|---|---|---|---|---|']
    for ig, szo, strong, _, e_halmaz, hibas_ok, c_szavak in regi:
        r = rkezi[(ig, szo, strong)]
        clink = '; '.join('%s -> %s' % (_magyar(adat, ig, p), ', '.join(_eredeti(adat, ig, e) for e in es) or '—')
                          for p, es in c_szavak.items())
        ki.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
            ig, szo, strong, clink, 'egyezik' if e_halmaz else 'nem egyezik',
            'kizárva (hibás)' if hibas_ok else '—', r['osztaly'], r['indok']))
    rsz = {}
    for r in rkezi.values():
        rsz[r['osztaly']] = rsz.get(r['osztaly'], 0) + 1
    ki += ['', '(e) = mérési műtermék (F21.12-ben elfogadva, a meres.py-ban javítva): a '
           'Karoli_Strong_kivonat.tsv összetett Strongja („H5128+H5110”) a korábbi egyezésvizsgálatban egész '
           'karakterláncként szerepelt. A halmaz-definícióval mind a 6 (e) hármas egyezik.',
           '', 'Osztályonként (kézi): %s.' % ', '.join('(%s) %d' % (o, rsz.get(o, 0)) for o in REGI_OSZTALYOK), '']
    if v2 is not None:
        ki += v2_szakasz(adat, el, kezi, el_v2, kezi_v2, v2)
    with open(JELENTES_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    return alap, szam


def _merok(adat, g_fn, kezi, ret):
    """(versek, C, arany, közös, többlet_ab, hiányzó_ab) egy rétegre."""
    vs = [ig for ig in adat.versek if ig in adat.arany and adat.ok(FUTAS, ig)
          and (ret == meres.OSSZES or adat.reteg[ig] == ret)]
    c = g = t = tab = hab = 0
    for ig in vs:
        cl, gl = adat.linkek(FUTAS, ig), g_fn(ig)
        c += len(cl)
        g += len(gl)
        t += len(cl & gl)
        for k, e in cl - gl:
            tab += kezi[(ig, 'tobblet', k, e)]['osztaly'] in ('a', 'b')
        for k, e in gl - cl:
            hab += kezi[(ig, 'hianyzo', k, e)]['osztaly'] in ('a', 'b')
    return len(vs), c, g, t, tab, hab


def v2_szakasz(adat, el, kezi, el_v2, kezi_v2, v2):
    ret_lista = meres.RETEGEK + [meres.OSSZES]
    g1, g2 = adat.arany_linkek, arany_fn(adat, v2)
    ki = ['## 7. A C diffje az arany v2-höz (f21p/arany_opus_v2.jsonl; jóváhagyásig nem befagyasztott)', '',
          'A v1-es P4 (naplok/F21P_meres_v1.md) és a fenti 1–6. pont változatlanul a v1-re vonatkozik. A '
          '**mért** érték a meres.py definíciója a megadott aranyhoz; a **korrigált** érték **az Opus '
          'besorolása, nem mérés** (az (a)/(b) eltérést nem-hibának veszi). A küszöb szempontjából csak a '
          'mért érték számít.', '',
          '| réteg | mérőszám | v1 mért | v2 mért | v1 korrigált (Opus besorolása, nem mérés) | v2 korrigált (Opus besorolása, nem mérés) |',
          '|---|---|---|---|---|---|']
    for ret in ret_lista:
        n1, c1, a1, t1, tab1, hab1 = _merok(adat, g1, kezi, ret)
        n2, c2, a2, t2, tab2, hab2 = _merok(adat, g2, kezi_v2, ret)
        ki.append('| %s | pontosság | %s | %s | %s | %s |' % (ret, _pct(t1, c1), _pct(t2, c2),
                                                              _pct(t1 + tab1, c1), _pct(t2 + tab2, c2)))
        ki.append('| %s | lefedettség | %s | %s | %s | %s |' % (ret, _pct(t1, a1), _pct(t2, a2),
                                                                _pct(t1 + hab1, a1), _pct(t2 + hab2, a2)))
    k1 = {(x[0], x[2], x[3], x[4]) for x in el}
    k2 = {(x[0], x[2], x[3], x[4]) for x in el_v2}
    ki += ['', 'Eltérések a v1-hez képest: %d eltérés megszűnt, %d új (összes v1: %d, v2: %d).' % (
        len(k1 - k2), len(k2 - k1), len(k1), len(k2)), '',
        '| vers | irány | magyar szó | eredeti szó | v1-osztály | v2 |', '|---|---|---|---|---|---|']
    for kk in sorted(k1 - k2):
        ki.append('| %s | %s | %s | %s | %s | egyező |' % (kk[0], kk[1], _magyar(adat, kk[0], kk[2]),
                                                          _eredeti(adat, kk[0], kk[3]), kezi[kk]['osztaly']))
    for kk in sorted(k2 - k1):
        ki.append('| %s | %s | %s | %s | — (egyező volt) | %s |' % (kk[0], kk[1], _magyar(adat, kk[0], kk[2]),
                                                                   _eredeti(adat, kk[0], kk[3]), kezi_v2[kk]['osztaly']))
    ki.append('')
    return ki


def v2_diff_jelentes(adat, el, kezi, el_v2, kezi_v2, v2):
    """naplok/F21P_arany_v2_diff.md: versenkénti v1 -> v2 diff, a C-diffre gyakorolt hatással."""
    import arany_v2 as av2
    k1 = {(x[0], x[2], x[3], x[4]) for x in el}
    k2 = {(x[0], x[2], x[3], x[4]) for x in el_v2}
    ki = ['# F21P_arany_v2_diff.md — az Opus-arany v1 -> v2 változásai', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/c_diff.py (az arany_v2.JAVITASOK és a két arany alapján) | '
          'scope=f21p/arany_opus.jsonl -> f21p/arany_opus_v2.jsonl (60 vers) | forras=f21p/arany_opus.jsonl, '
          'f21p/arany_opus_v2.jsonl, f21p/arany_opus_v2.sha256, eszkozok/karoli_strong/arany_v2.py (JAVITASOK), '
          'f21p/valaszok/F3.jsonl, f21p/c_diff_besorolas.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->'
          % tokenek.generalas_ts(), '',
          'A v2 a v1 másolata, csak a f21p/arany_opus_jegyzetek.md 2. szakaszának konvencióival ütköző '
          'versek javultak (felhasználói döntés, F21.12). A v1 érintetlen. **A v2 jóváhagyásig nem fagy be.** '
          'A konvenció-azonosítás és az indok kézi ítélet (Opus).', '',
          '| vers | régi link (v1) | új link (v2) | sértett konvenció | indok | hatás a C diffre |',
          '|---|---|---|---|---|---|']
    for ig, j in av2.JAVITASOK.items():
        l1 = {(p[0], e) for p in adat.arany[ig]['parok'] for e in p[1]}
        l2 = {(p[0], e) for p in v2[ig]['parok'] for e in p[1]}
        regi = ', '.join('%s -> %s' % (_magyar(adat, ig, k), _eredeti(adat, ig, e)) for k, e in sorted(l1 - l2)) or '—'
        uj = ', '.join('%s -> %s' % (_magyar(adat, ig, k), _eredeti(adat, ig, e)) for k, e in sorted(l2 - l1)) or '—'
        tv = []
        if adat.arany[ig]['betoldas'] != v2[ig]['betoldas']:
            tv.append('betoldas: %s -> %s' % (adat.arany[ig]['betoldas'], v2[ig]['betoldas']))
        if adat.arany[ig]['forditatlan'] != v2[ig]['forditatlan']:
            tv.append('forditatlan: %s -> %s' % (adat.arany[ig]['forditatlan'], v2[ig]['forditatlan']))
        megszunt = [kk for kk in sorted(k1 - k2) if kk[0] == ig]
        ujel = [kk for kk in sorted(k2 - k1) if kk[0] == ig]
        hatas = '; '.join(['(%s) %s %d->%d -> egyező' % (kezi[kk]['osztaly'], kk[1], kk[2], kk[3]) for kk in megszunt] +
                          ['egyező -> (%s) %s %d->%d' % (kezi_v2[kk]['osztaly'], kk[1], kk[2], kk[3]) for kk in ujel]) or 'nincs'
        ki.append('| %s | %s | %s | %s | %s | %s |' % (ig, regi + ('; ' + '; '.join(tv) if tv else ''), uj,
                                                      j['konvencio'], j['indok'], hatas))
    osszesit = {}
    for kk in k1 - k2:
        osszesit[kezi[kk]['osztaly']] = osszesit.get(kezi[kk]['osztaly'], 0) + 1
    ki += ['', 'Összesen: %d vers változott; a C diffjében %d eltérés szűnt meg (%s), %d új keletkezett.' % (
        len(av2.JAVITASOK), len(k1 - k2), ', '.join('(%s)->egyező: %d' % kv for kv in sorted(osszesit.items())) or '—',
        len(k2 - k1)), '']
    ki += NEM_JAVITOTT
    if os.path.exists(tokenek.ARANY_V2_SHA):
        ki += ['**Befagyasztva 2026.09.30, felhasználói jóváhagyással** (F21.14). sha256 (LF-normalizált '
               'tartalom): `%s` — f21p/arany_opus_v2.sha256; az arany_ellenoriz.py, a meres.py és a c_diff.py '
               'eltérésnél hibával megáll.' % tokenek.arany_v2_befagyasztas_ellenoriz(ARANY_V2_UT), '']
    with open(V2_DIFF_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


NEM_JAVITOTT = [
    '## Nem javított esetek (kérdések, felhasználói döntésre)', '',
    '- **Tárgyragok (a döntés K3-at nevezett meg).** A K3 csak a tárgyjelölő *\'et* + névmási rag esetét '
    'szabályozza (az *\'et* forditatlan, a magyar névmás a ragra megy). A kérdéses eset más: tárgyi rag az '
    'igén, külön magyar névmás nélkül (a határozott ragozás jelöli). Az aranyban 4 ilyen van: 2Móz 21:6 #11 '
    '(*állítsa*) forditatlan; 2Móz 21:26 #16 (*elpusztul*), Péld 30:17 #11 (*kivágják*) és #16 (*megeszik*) '
    'az igéhez kötve. Egyik konvenció sem mondja ki ezt az esetet (a K4 a birtokos személyragról szól), ezért '
    'nincs megnevezhető konvenciósértés; nem javítottam. Opció: (a) az igéhez kötni mind a négyet (a 2Móz 21:6 '
    '#11 -> *állítsa*); (b) forditatlan mind a négy; mindkettőhöz új konvenció kell a jegyzetbe.',
    '- **„való” (2Pét 1:7 kötve, Péld 30:17 *iránt való* betoldas).** Nincs rá konvenció a 2. szakaszban (a K2 '
    'a kettéírt kötőszókról és a vonatkozó névmásokról szól); nem javítottam. Opció: új konvenció a „való” '
    'melléknévi szerkezetre (kötve a főnévhez, vagy betoldas).',
    '- **Ez 39:13 *megdicsőítem*.** A -י (H9040) rag a *magamat*-hoz kötött; a K4 a „birtokos személyragot '
    'viselő magyar szóhoz” köt, a *megdicsőítem* igei személyrag, nem birtokos. Nem megnevezett K4-sértés; '
    'nem javítottam. Kérdés: kiterjed-e a K4 az igei személyragra.',
    '- **2Móz 26:13 *is* (23, 25).** A K9 szerint a *ve-* az *is*-hez is köthető volna, de az *is* betoldas '
    'a 6. táblázat dokumentált döntése; a v2 a minimális javítást alkalmazta (forditatlan). Kérdés: az '
    '*is*-hez kerüljön-e.',
    '',
]


def main():
    if '--f3v2' in sys.argv:
        # F21.14: az F3V2 diffje az arany v2-höz és a (c) esetek összevetése az F3-mal (c_diff_f3v2.py)
        import c_diff_f3v2
        return c_diff_f3v2.main()
    adat = meres.Adat()
    if '--lista' in sys.argv:
        lista(adat)
        return 0
    hibak, el, kezi, regi, rkezi, el_v2, kezi_v2, v2 = ellenoriz(adat)
    if hibak:
        print('HIBA (a jelentés nem íródott):')
        for h in hibak:
            print('  ' + h)
        return 1
    alap, szam = jelentes(adat, el, kezi, regi, rkezi, el_v2, kezi_v2, v2)
    if v2 is not None:
        v2_diff_jelentes(adat, el, kezi, el_v2, kezi_v2, v2)
        print('v2: eltérés %d (v1: %d) -> %s' % (len(el_v2), len(el), V2_DIFF_UT))
    n, c, g, t = alap[meres.OSSZES]
    print('gépi eltérés: %d (hiányzó %d, többlet %d); besorolva: %d; régi arany nem egyező (korábbi definíció, kontroll): %d/%d, besorolva: %d'
          % (len(el), g - t, c - t, len(kezi), len(regi), len(regi_elteresek(adat)), len(rkezi)))
    for irany in IRANYOK:
        print('%s: %s' % (irany, ', '.join('(%s) %d' % (o, szam.get((meres.OSSZES, irany, o), 0)) for o in OSZTALYOK)))
    print('-> %s' % JELENTES_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
