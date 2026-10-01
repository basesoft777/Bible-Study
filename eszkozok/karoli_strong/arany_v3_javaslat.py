#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.41 — az arany v3 JAVASLAT előállítása az arany v2-ből (f21p/arany_opus_v2.jsonl
-> f21p/arany_opus_v3_javaslat.jsonl) és a versenkénti diff (naplok/F21P_arany_v3_diff.md).

A v2 befagyasztott (f21p/arany_opus_v2.sha256): a szkript előbb ellenőrzi, és eltérésnél
hibával megáll; a v2-t nem írja. Csak a jegyzet v2 (f21p/arany_opus_jegyzetek_v2.md 8.
szakasz, a DT-F21j a–e döntések) konvencióival ütköző linkek változnak; minden javításnál a
DT-F21j-pont (a/b/c/e) és a konvenció (K1–K11). A többi sor bájtra azonos a v2-vel (a szkript
ellenőrzi), és minden vers átmegy a kapun.

B változat (F21.44, NEM alkalmazott, döntésre): az A (JAVITASOK) fölé a DT-F21j b) szó
szerinti olvasata (JAVITASOK_B) -> f21p/arany_opus_v3_javaslat_B.jsonl; a diff 5. szakasza.
Az A változat fájlja nem változhat: ha már létezik és eltérne, a szkript hibával megáll.

A JAVASLAT NEM befagyasztott: sha256-fájlt nem ír. ⛔ A felhasználó jóváhagyásáig az
arany v3 nem fagy be, és a mérés nem fut az arany v3-ra (PD13, DT-F21a).

A hatás a C-diffre: a két C-futás (F3V2, F3V2B) eltérései (a meres.py linkhalmazaival,
a f21p/meres_kizaras.tsv tokenjei nélkül) az arany v2-höz és a javaslathoz. A megszűnő
eltérés osztálya a meglévő kézi besorolásból jön (F3V2: f21p/c_diff_f3v2_osszevetes.tsv;
F3V2B: az F3V2-vel közös eltérésnél ugyanaz, különben f21p/c_diff_f3v2b_besorolas.tsv); az
új eltérés osztálya kézi ítélet (UJ_OSZTALY), nem mérés.

Futtatás a repó gyökeréből (hálózat és titok nélkül):
    python eszkozok/karoli_strong/arany_v3_javaslat.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import c_diff  # noqa: E402
import c_diff_f3v2 as cf  # noqa: E402
import kapu  # noqa: E402
import meres  # noqa: E402
import tokenek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

V2 = tokenek.ARANY_V2
JAVASLAT = os.path.join(tokenek.ROOT, 'f21p', 'arany_opus_v3_javaslat.jsonl')
DIFF_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_arany_v3_diff.md')
F3V2B_BESOROLAS = os.path.join(tokenek.ROOT, 'f21p', 'c_diff_f3v2b_besorolas.tsv')
FUTASOK = ('F3V2', 'F3V2B')

# vers -> javítás: párok felülírása {magyar: [eredeti...]} (üres lista: a pár törlődik),
# betoldas-hoz adandó, forditatlan-hoz adandó / törlendő; DT-F21j-pont, konvenció, indok.
JAVITASOK = {
    'Jób 33:13': {
        'parok': {4: []}, 'betoldas_ad': [4], 'forditatlan_ad': [], 'forditatlan_torol': [],
        'szabaly': 'c', 'konvencio': 'K11',
        'indok': 'Azért, hogy ← כִּי: az Azért korrelatív mutató névmásnak nincs külön eredetije, '
                 'ezért betoldas; a hogy (5) marad a כִּי-n',
    },
    'Mt 21:4': {
        'parok': {3: []}, 'betoldas_ad': [3], 'forditatlan_ad': [], 'forditatlan_torol': [],
        'szabaly': 'c', 'konvencio': 'K11',
        'indok': 'azért lett, hogy ← ἵνα: az azért korrelatív mutató névmásnak nincs külön eredetije, '
                 'ezért betoldas; a hogy (5) marad a ἵνα-n',
    },
    'Ez 39:13': {
        'parok': {18: []}, 'betoldas_ad': [18], 'forditatlan_ad': [], 'forditatlan_torol': [],
        'szabaly': 'b', 'konvencio': 'K3 v2',
        'indok': 'ezt mondja ← נְאֻם: az ezt tárgyi mutató névmás, nincs sem \'et + rag, sem más eredeti '
                 'névmási elem, ezért betoldas; a mondja (19) marad a נְאֻם-on (a 6. táblázat sorának '
                 'alternatívája, a sor maga nem változik)',
    },
}

# B változat (F21.44, NEM alkalmazott, döntésre): a DT-F21j b) szó szerinti olvasata — 'et + rag
# nélkül minden magyar tárgyi névmás betoldas, az igei (elöljárós) névmási rag forditatlan.
# Az A változat (JAVITASOK) fölé kerül; a f21p/arany_opus_v3_javaslat_B.jsonl-t adja.
_B_KONV = 'K3 v2, B olvasat'
JAVITASOK_B = {
    '2Móz 20:25': {
        'parok': {19: []}, 'betoldas_ad': [19], 'forditatlan_ad': [21], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'megfertőztetted azt ← -hā az igén (nincs \'et): az azt betoldas, a rag forditatlan',
    },
    '2Móz 21:6': {
        'parok': {3: [], 29: []}, 'betoldas_ad': [3, 29], 'forditatlan_ad': [3, 30], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'vigye őt ← -ô, szolgálja őt ← -ô az igén (nincs \'et): mindkét őt betoldas, a ragok forditatlan',
    },
    '2Móz 21:26': {
        'parok': {16: []}, 'betoldas_ad': [16], 'forditatlan_ad': [20], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'bocsássa azt ← -ennû az igén (nincs \'et): az azt betoldas, a rag forditatlan',
    },
    '2Móz 26:13': {
        'parok': {28: []}, 'betoldas_ad': [28], 'forditatlan_ad': [31], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'befedje azt ← -ô a főnévi igenéven (nincs \'et): az azt betoldas, a rag forditatlan',
    },
    'Péld 28:17': {
        'parok': {14: []}, 'betoldas_ad': [14], 'forditatlan_ad': [11, 12], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'támogassa őt ← bô (elöljáró + rag, nincs \'et): az őt betoldas, az elöljáró és a rag forditatlan '
                 '(elöljárós eset: a B olvasat itt a legvitathatóbb)',
    },
    'Zsolt 6:5': {
        'parok': {9: []}, 'betoldas_ad': [9], 'forditatlan_ad': [9], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'segíts meg engem ← -ní az igén (nincs \'et): az engem betoldas, a rag forditatlan',
    },
    'Zsolt 16:11': {
        'parok': {3: []}, 'betoldas_ad': [3], 'forditatlan_ad': [2], 'forditatlan_torol': [],
        'szabaly': 'b (B)', 'konvencio': _B_KONV,
        'indok': 'tanítasz engem ← -ní az igén (nincs \'et): az engem betoldas, a rag forditatlan',
    },
}
JAVASLAT_B = os.path.join(tokenek.ROOT, 'f21p', 'arany_opus_v3_javaslat_B.jsonl')

# Az új eltérések osztálya (kézi ítélet, Opus, nem mérés): kulcs (futás, vers, irány, k, e).
UJ_OSZTALY = {
    ('F3V2', 'Jób 33:13', 'tobblet', 4, 5): ('a', 'K11', 'az Azért a C-nél a כִּי-hoz kötve; a K11 szerint betoldas'),
    ('F3V2B', 'Jób 33:13', 'tobblet', 4, 5): ('a', 'K11', 'mint az F3V2-nél'),
    ('F3V2', 'Mt 21:4', 'tobblet', 3, 5): ('a', 'K11', 'az azért a C-nél a ἵνα-hoz kötve; a K11 szerint betoldas'),
    ('F3V2', 'Ez 39:13', 'tobblet', 18, 16): ('a', 'K3 v2', 'az ezt a C-nél a נְאֻם-hoz kötve; a K3 v2 szerint betoldas'),
    ('F3V2B', 'Ez 39:13', 'tobblet', 18, 16): ('a', 'K3 v2', 'mint az F3V2-nél'),
}

# A B változat további új eltéréseinek osztálya (kézi ítélet, Opus, nem mérés).
_B_UJ = [('2Móz 20:25', 19, 21), ('2Móz 21:26', 16, 20), ('2Móz 21:6', 3, 3), ('2Móz 21:6', 29, 30),
         ('2Móz 26:13', 28, 31), ('Péld 28:17', 14, 11), ('Péld 28:17', 14, 12), ('Zsolt 16:11', 3, 2),
         ('Zsolt 6:5', 9, 9)]
UJ_OSZTALY_B = {
    (f, ig, 'tobblet', k, e): ('a', _B_KONV, 'a C a névmást a raghoz köti (az A olvasat, K4); a B olvasat szerint '
                                           'a névmás betoldas, a rag forditatlan')
    for f in FUTASOK for ig, k, e in _B_UJ
}


def javit(o, j):
    parok = {m: e for m, e in o['parok']}
    for m, e in j['parok'].items():
        if e:
            parok[m] = e
        else:
            parok.pop(m, None)
    return {
        'vers': o['vers'],
        'parok': [[m, parok[m]] for m in sorted(parok)],
        'betoldas': sorted(set(o['betoldas']) | set(j['betoldas_ad'])),
        'forditatlan': sorted((set(o['forditatlan']) - set(j['forditatlan_torol'])) | set(j['forditatlan_ad'])),
    }


def linkek(o):
    return {(m, e) for m, es in o['parok'] for e in es}


def _link_szoveg(adat_v, o, m):
    toks, ered = adat_v['karoli_tokenek'], adat_v['eredeti']
    p = {k: es for k, es in o['parok']}
    if m in p:
        return '%d %s -> %s' % (m, toks[m - 1], '; '.join('%d %s %s [%s]' % (
            e, ered[e - 1]['alak'], ered[e - 1]['strong'], ered[e - 1]['tukor']) for e in p[m]))
    return '%d %s -> betoldas' % (m, toks[m - 1])


def osztalyok():
    """{futás: {kulcs: osztály}} a meglévő kézi besorolásból (az arany v2-höz)."""
    f3v2 = {}
    for r in c_diff._tsv(cf.OSSZEVETES_UT, cf.OSZLOPOK):
        if r['statusz'] in ('maradt', 'uj', 'oroklott'):
            f3v2[(r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))] = r['f3v2_osztaly']
    f3v2b = {}
    for r in c_diff._tsv(F3V2B_BESOROLAS, c_diff.BES_OSZLOPOK):
        f3v2b[(r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))] = r['osztaly']
    return f3v2, f3v2b


_ADAT = []


def _adat():
    if not _ADAT:
        _ADAT.append(meres.Adat(futasok=list(FUTASOK)))
    return _ADAT[0]


def hatas(v2, v3, uj_osztaly=None):
    """[(futás, kulcs, állapot, osztály, konvenció, indok)] és futásonkénti mért összesítő
    (a v3 itt az A vagy a B változat; az új eltérések kézi osztálya: uj_osztaly)."""
    uj_osztaly = UJ_OSZTALY if uj_osztaly is None else uj_osztaly
    adat = _adat()
    g2 = lambda ig: adat._szur(ig, linkek(v2[ig]))   # noqa: E731
    g3 = lambda ig: adat._szur(ig, linkek(v3[ig]))   # noqa: E731
    k_f3v2, k_f3v2b = osztalyok()
    el = {f: (cf.elteresek(adat, f, g2), cf.elteresek(adat, f, g3)) for f in FUTASOK}
    sorok, osszesito = [], {}
    for f in FUTASOK:
        e2, e3 = el[f]
        for kk in sorted(set(e2) - set(e3)):
            if f == 'F3V2':
                o = k_f3v2.get(kk)
            else:
                o = k_f3v2.get(kk) if kk in el['F3V2'][0] else k_f3v2b.get(kk)
            if o is None:
                raise SystemExit('HIBA: a megszűnő eltérésnek nincs kézi besorolása: %s %s' % (f, kk))
            sorok.append((f, kk, 'megszunik', o, '', 'a meglévő kézi besorolás szerint'))
        hianyzik = []
        for kk in sorted(set(e3) - set(e2)):
            u = uj_osztaly.get((f,) + kk)
            if u is None:
                hianyzik.append((f,) + kk)
                continue
            sorok.append((f, kk, 'uj', u[0], u[1], u[2]))
        if hianyzik:
            raise SystemExit('HIBA: az új eltérésnek nincs kézi osztálya: %s' % hianyzik)
        for kk in uj_osztaly:
            if kk[0] == f and kk[1:] not in set(e3) - set(e2):
                raise SystemExit('HIBA: az UJ_OSZTALY kulcsa nem új eltérés: %s' % (kk,))
        # mért összesítő a 60 aranyversen (a kapun átment versek), v2 és javaslat
        m = {}
        for nev, g in (('v2', g2), ('v3j', g3)):
            c_db = a_db = kozos = 0
            for ig in adat.versek:
                if ig not in v2 or not adat.ok(f, ig):
                    continue
                c, a = adat.linkek(f, ig), g(ig)
                c_db, a_db, kozos = c_db + len(c), a_db + len(a), kozos + len(c & a)
            m[nev] = (c_db, a_db, kozos, len(e2) if nev == 'v2' else len(e3))
        osszesito[f] = m
    return sorok, osszesito


def _pct(x, n):
    return '%.1f%% (%d/%d)' % (100.0 * x / n, x, n) if n else '—'


def _hatas_tabla(sorok, osszesito, cimke):
    ki = ['| futás | megszűnő (a / b / c) | új (a / b / c) | eltérés v2 → %s | '
          'mért pontosság v2 → %s | mért lefedettség v2 → %s |' % (cimke, cimke, cimke),
          '|---|---|---|---|---|---|']
    for f in FUTASOK:
        msz = [o for ff, _, st, o, _, _ in sorok if ff == f and st == 'megszunik']
        uj = [o for ff, _, st, o, _, _ in sorok if ff == f and st == 'uj']
        m2, m3 = osszesito[f]['v2'], osszesito[f]['v3j']
        ki.append('| %s | %d (%d / %d / %d) | %d (%d / %d / %d) | %d → %d | %s → %s | %s → %s |' % (
            f, len(msz), msz.count('a'), msz.count('b'), msz.count('c'),
            len(uj), uj.count('a'), uj.count('b'), uj.count('c'), m2[3], m3[3],
            _pct(m2[2], m2[0]), _pct(m3[2], m3[0]), _pct(m2[2], m2[1]), _pct(m3[2], m3[1])))
    return ki


def b_szakasz(v3, v3b, sorok_a, sorok_b, osszesito, osszesito_b):
    ki = ['## 5. B) változat — a DT-F21j b) szó szerinti olvasata (NEM alkalmazott, döntésre)', '',
          'A felhasználó értelmezése (F21.44): „a névmás a ragra kötődik” — *\'et* + rag esetén a magyar névmás a '
          'ragra megy, az *\'et* `forditatlan` (ez mindkét változatban így van). **Nincs eldöntve** az igén '
          '(főnévi igenéven, elöljárón) álló, *\'et* nélküli névmási rag külön kitett magyar névmása: '
          '**(A)** a K4 szerint a raghoz kötve marad (a jelenlegi javaslat, `f21p/arany_opus_v3_javaslat.jsonl`); '
          '**(B)** szó szerint: a névmás `betoldas`, a rag `forditatlan` (`f21p/arany_opus_v3_javaslat_B.jsonl` = '
          'A + az alábbi linkek; NEM befagyasztott). A B a DT-F21i a) kérdését (tárgyrag az igén) is érinti: a '
          'rag itt `forditatlan`, nem az igéhez kötött. Az osztály és az indok kézi ítélet (Opus), nem mérés.', '',
          '| vers | magyar szó | régi link (A) | új link (B) | konvenció | indok |', '|---|---|---|---|---|---|']
    n = 0
    for ig, j in JAVITASOK_B.items():
        a = bemenet.vers_adat(ig)
        for m in sorted(j['parok']):
            n += len([e for mm, es in v3[ig]['parok'] if mm == m for e in es])
            ki.append('| %s | %d %s | %s | %s | %s | %s |' % (
                ig, m, a['karoli_tokenek'][m - 1], _link_szoveg(a, v3[ig], m), _link_szoveg(a, v3b[ig], m),
                j['konvencio'], j['indok']))
    l3 = sum(len(linkek(o)) for o in v3.values())
    l3b = sum(len(linkek(o)) for o in v3b.values())
    ki += ['', 'A B változat az A-hoz képest: %d vers, %d magyar szó, %d link (a rag `forditatlan`-ba kerül). '
           'Linkek: A %d, B %d. Kapu: **%d/%d vers átmegy** (B).'
           % (len(JAVITASOK_B), sum(len(j['parok']) for j in JAVITASOK_B.values()), n, l3, l3b,
              kapu_ok(v3b), len(v3b)), '',
           '**A B változat további hatása a C-diffre** (a B-nek az arany v2-höz mért eltérései közül azok, amelyek '
           'az A-ban nincsenek; számított, c_diff_f3v2.elteresek):', '',
           '| futás | vers | irány | magyar szó | eredeti szó | állapot | osztály | konvenció |',
           '|---|---|---|---|---|---|---|---|']
    kulcs_a = {(f, kk, st) for f, kk, st, _, _, _ in sorok_a}
    for f, kk, st, o, konv, _ in sorok_b:
        if (f, kk, st) in kulcs_a:
            continue
        ig, ir, k, e = kk
        a = bemenet.vers_adat(ig)
        w = a['eredeti'][e - 1]
        ki.append('| %s | %s | %s | %d %s | %d %s %s [%s] | %s | %s | %s |' % (
            f, ig, ir, k, a['karoli_tokenek'][k - 1], e, w['alak'], w['strong'], w['tukor'],
            'megszűnik' if st == 'megszunik' else 'új', o, konv or '—'))
    ki += ['', '**A két változat hatása a két C-futásra (az arany v2-höz képest):**', '', '*A változat:*', '']
    ki += _hatas_tabla(sorok_a, osszesito, 'A')
    ki += ['', '*B változat:*', '']
    ki += _hatas_tabla(sorok_b, osszesito_b, 'B')
    ki += ['', 'Mindkét C-futás mind a 9 érintett linknél az A olvasatot követte (a névmás a raghoz kötve), ezért a '
           'B minden további linkje új (a) eltérés. A változatválasztás a felhasználóé; az arany nem igazodik a mért '
           'modellhez (PD10).', '']
    return ki


def md(v2, v3, sorok, osszesito, v3b=None, sorok_b=None, osszesito_b=None):
    ts = tokenek.generalas_ts()
    ki = ['# F21P_arany_v3_diff.md — az Opus-arany v2 -> v3 JAVASLAT versenkénti diffje', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/arany_v3_javaslat.py | scope=f21p/arany_opus_v2.jsonl -> '
          'f21p/arany_opus_v3_javaslat.jsonl (60 vers), hatás az F3V2 és F3V2B C-diffjére | '
          'forras=f21p/arany_opus_v2.jsonl (befagyasztva), f21p/arany_opus_v2.sha256, f21p/arany_opus_jegyzetek_v2.md '
          '(8. szakasz), eszkozok/karoli_strong/arany_v3_javaslat.py (JAVITASOK, UJ_OSZTALY), f21p/valaszok/F3V2.jsonl, '
          'f21p/valaszok/F3V2B.jsonl, f21p/meres_kizaras.tsv, f21p/c_diff_f3v2_osszevetes.tsv, '
          'f21p/c_diff_f3v2b_besorolas.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
          'kézzel szerkeszteni tilos -->' % ts, '',
          '> ⛔ **Megállás (PD13, DT-F21a).** Ez JAVASLAT: az `f21p/arany_opus_v3_javaslat.jsonl` nem '
          'befagyasztott, sha256-fájlja nincs. A felhasználó jóváhagyásáig az arany v3 nem fagy be, és a '
          'mérés (F3V3, Sonnet) nem fut az arany v3-ra; a befagyasztás a jóváhagyás után az orkesztrátoré.', '',
          '> **Két változat, a felhasználó választ (F21.44).** **A:** a jelenlegi javaslat, 3 link '
          '(`f21p/arany_opus_v3_javaslat.jsonl`, változatlan). **B:** A + a DT-F21j b) szó szerinti olvasatának '
          'további linkjei (`f21p/arany_opus_v3_javaslat_B.jsonl`, 5. szakasz; NEM alkalmazott, NEM '
          'befagyasztott). A jegyzet v2 és a prompt_v3 C szabálya az A olvasatot követi.', '',
          'A javaslat az arany v2 másolata; csak a jegyzet v2 (`f21p/arany_opus_jegyzetek_v2.md` 8. szakasz, a '
          'DT-F21j a–e döntések) konvencióival ütköző linkek változnak, a többi sor bájtra azonos (a szkript '
          'ellenőrzi). A szabály- és konvenció-azonosítás és az indok **kézi ítélet (Opus), nem mérés**.', '',
          '## 1. A változások (vers, magyar szó, régi link, új link)', '',
          '| vers | magyar szó | régi link (v2) | új link (v3-javaslat) | szabály (DT-F21j) | konvenció | indok |',
          '|---|---|---|---|---|---|---|']
    n_link = 0
    for ig in [o for o in JAVITASOK]:
        j = JAVITASOK[ig]
        a = bemenet.vers_adat(ig)
        for m in sorted(j['parok']):
            regi = _link_szoveg(a, v2[ig], m)
            uj = _link_szoveg(a, v3[ig], m)
            n_link += len({e for mm, es in v2[ig]['parok'] if mm == m for e in es} ^
                          {e for mm, es in v3[ig]['parok'] if mm == m for e in es})
            ki.append('| %s | %d %s | %s | %s | %s | %s | %s |' % (
                ig, m, a['karoli_tokenek'][m - 1], regi, uj, j['szabaly'], j['konvencio'], j['indok']))
    l2 = sum(len(linkek(o)) for o in v2.values())
    l3 = sum(len(linkek(o)) for o in v3.values())
    ki += ['', 'Összesen: %d vers, %d link változik (a link törlődik, a magyar szó `betoldas`-ba kerül; az eredeti '
           'szó a versben más párban marad, tehát `forditatlan` nem változik). Linkek: v2 %d, v3-javaslat %d. '
           'Szabályonként: c (K11) %d, b (K3 v2) %d; a (K7 v2) 0, e (K4 v2) 0, d 0.'
           % (len(JAVITASOK), n_link, l2, l3,
              sum(1 for j in JAVITASOK.values() if j['szabaly'] == 'c'),
              sum(1 for j in JAVITASOK.values() if j['szabaly'] == 'b')), '',
           '## 2. Hatás a v2-es C-diffre (F3V2, F3V2B)', '',
           'Gépi, számított (nem becslés): melyik eltérés szűnik meg és melyik keletkezik (a c_diff_f3v2.elteresek '
           'és a meres.py linkhalmazai, a kizárt tokenek nélkül, a kapun átment aranyverseken). Osztály: a megszűnőé a meglévő kézi besorolás, az újé kézi '
           'ítélet (Opus, nem mérés).', '',
           '| futás | vers | irány | magyar szó | eredeti szó | állapot | osztály | konvenció | indok |',
           '|---|---|---|---|---|---|---|---|---|']
    for f, kk, st, o, konv, ind in sorok:
        ig, ir, k, e = kk
        a = bemenet.vers_adat(ig)
        w = a['eredeti'][e - 1]
        ki.append('| %s | %s | %s | %d %s | %d %s %s [%s] | %s | %s | %s | %s |' % (
            f, ig, ir, k, a['karoli_tokenek'][k - 1], e, w['alak'], w['strong'], w['tukor'],
            'megszűnik (%s → egyező)' % o if st == 'megszunik' else 'új', o, konv or '—', ind))
    ki += ['', '| futás | megszűnő (a / b / c) | új (a / b / c) | eltérés v2 → v3-javaslat | '
               'mért pontosság v2 → v3-javaslat | mért lefedettség v2 → v3-javaslat |',
           '|---|---|---|---|---|---|']
    for f in FUTASOK:
        msz = [o for ff, _, st, o, _, _ in sorok if ff == f and st == 'megszunik']
        uj = [o for ff, _, st, o, _, _ in sorok if ff == f and st == 'uj']
        m2, m3 = osszesito[f]['v2'], osszesito[f]['v3j']
        ki.append('| %s | %d (%d / %d / %d) | %d (%d / %d / %d) | %d → %d | %s → %s | %s → %s |' % (
            f, len(msz), msz.count('a'), msz.count('b'), msz.count('c'),
            len(uj), uj.count('a'), uj.count('b'), uj.count('c'), m2[3], m3[3],
            _pct(m2[2], m2[0]), _pct(m3[2], m3[0]), _pct(m2[2], m2[1]), _pct(m3[2], m3[1])))
    ki += ['', 'A mért pontosság és lefedettség itt csak a 60 aranyversre, a két arany összevetésére szól '
           '(tájékoztató; a küszöb szempontjából a P4-mérés számít, és az a jóváhagyás után az arany v3-ra fut). '
           'A javaslat a C-diffet nem javítja: a három link a mért C-futásokban az arany v2-vel egyezett, a v3 '
           'konvenciója szerint viszont a C (a) konvenciókülönbséget mutat; az arany nem igazodik a mért modellhez '
           '(PD10).', '',
           '## 3. Nem érintett pontok (a–e)', '',
           '- **a (K7 v2):** az arany v2-ben minden segédige `betoldas`, ahol nincs külön eredeti ige; a kivétel '
           'csak a Mt 4:4 *Meg van írva*. A *lészen* (Jak 3:1 ← λημψόμεθα) és a *van* (Mk 2:10, Mt 11:18 ← ἔχει) '
           'külön eredeti igét fordít, nem segédige-betoldás. Nincs változás.',
           '- **b (K3 v2):** a többi magyar tárgyi névmás *\'et* + ragra (K3), igei/elöljárós névmási ragra (K4) '
           'vagy önálló eredeti névmásra kötött, a megfelelő nélküliek (Péld 23:19 *engem*, Zsolt 22:32 *ezt*, '
           'Mt 5:34 *azt*, Mt 11:18 *azt*, Jak 3:1 *azt*, 1Ján 1:10 *azt*) már `betoldas`. A döntés szó szerinti '
           '(szűkebb) olvasatának hatása: a jegyzet v2 8.3 pont 1. kérdése és az 5. szakasz (B változat).',
           '- **c (K11):** a Jak 3:1 és az 1Ján 1:10 *azt … hogy* már a K11 szerinti (*azt* `betoldas`, *hogy* a '
           'ὅτι-n); a 2Móz 21:26 *úgy … hogy* a 6. táblázat szerint szintén.',
           '- **d:** 2Móz 26:13 *is*: marad (a 6. táblázat és az arany v2 szerint).',
           '- **e (K4 v2):** minden birtokos/névmási rag a megfelelő személyragot viselő szón (2Móz 21:26 '
           '*szolgálójának* ← 13 -ô); birtokláncban (Zsolt 18:1 *ellenségének kezéből*, Jer 46:21 *romlásuk napja*, '
           '*megfenyíttetésök ideje*) a rag a megfelelő szón. Nyitott: 2Móz 25:40 *arra*, Ez 39:13 *megdicsőítem* '
           '(jegyzet v2 8.3).', '',
           '## 4. Kapu', '',
           'A javaslat ellenőrzése: `python eszkozok/karoli_strong/arany_ellenoriz.py --arany '
           'f21p/arany_opus_v3_javaslat.jsonl` (a befagyasztás-ellenőrzés csak az arany v2 útvonalára fut; a '
           'javaslatra a kapu öt pontja, a `[nem TR]` és a mérési kizárás ellenőrzése fut). Ez a szkript a '
           'javaslat minden versét a kapun is átengedi (kapu.vers_ellenoriz), különben hibával megáll: '
           '**%d/%d vers átmegy a kapun**, %d link.' % (kapu_ok(v3), len(v3), l3), '']
    if v3b is not None:
        ki += b_szakasz(v3, v3b, sorok, sorok_b, osszesito, osszesito_b)
    return '\n'.join(ki)


def kapu_ok(arany):
    """A kapun (mind az öt pont) átmenő versek száma; hibánál SystemExit."""
    ok = 0
    for ig, o in arany.items():
        h = kapu.vers_ellenoriz(o, bemenet.vers_adat(ig))
        if h:
            raise SystemExit('HIBA: a javaslat verse nem megy át a kapun: %s %s' % (ig, h))
        ok += 1
    return ok


def main():
    tokenek.arany_v2_befagyasztas_ellenoriz(V2)   # eltérésnél SystemExit
    with open(V2, encoding='utf-8') as f:
        v2_szoveg = f.read().replace('\r\n', '\n')
    sorok = v2_szoveg.split('\n')
    ki = []
    for s in sorok:
        if s.strip():
            o = json.loads(s)
            if o['vers'] in JAVITASOK:
                o3 = javit(o, JAVITASOK[o['vers']])
                h = kapu.vers_ellenoriz(o3, bemenet.vers_adat(o['vers']))
                if h:
                    raise SystemExit('HIBA: a javított vers nem megy át a kapun: %s %s' % (o['vers'], h))
                s = json.dumps(o3, ensure_ascii=False, separators=(',', ':'))
                print('%s (%s, %s)' % (o['vers'], JAVITASOK[o['vers']]['szabaly'], JAVITASOK[o['vers']]['konvencio']))
        ki.append(s)
    elteres = {json.loads(a)['vers'] for a, b in zip(sorok, ki) if a != b}
    if elteres != set(JAVITASOK) or len(ki) != len(sorok):
        raise SystemExit('HIBA: váratlan eltérés a v2-től: %s' % sorted(elteres))
    a_szoveg = '\n'.join(ki)
    if os.path.exists(JAVASLAT):
        # F21.44: az A változat (a jelenlegi javaslat) nem változhat
        with open(JAVASLAT, encoding='utf-8') as f:
            if f.read().replace('\r\n', '\n') != a_szoveg:
                raise SystemExit('HIBA: az A változat (%s) eltérne a meglévőtől; nem írom felül' % JAVASLAT)
    else:
        with open(JAVASLAT, 'w', encoding='utf-8', newline='\n') as f:
            f.write(a_szoveg)
    # B változat: az A fölé a JAVITASOK_B (NEM alkalmazott, döntésre)
    ki_b = []
    for s in ki:
        if s.strip():
            o = json.loads(s)
            if o['vers'] in JAVITASOK_B:
                ob = javit(o, JAVITASOK_B[o['vers']])
                h = kapu.vers_ellenoriz(ob, bemenet.vers_adat(o['vers']))
                if h:
                    raise SystemExit('HIBA: a B változat verse nem megy át a kapun: %s %s' % (o['vers'], h))
                s = json.dumps(ob, ensure_ascii=False, separators=(',', ':'))
        ki_b.append(s)
    elteres_b = {json.loads(a)['vers'] for a, b in zip(ki, ki_b) if a != b}
    if elteres_b != set(JAVITASOK_B) or len(ki_b) != len(ki):
        raise SystemExit('HIBA: váratlan eltérés az A változattól: %s' % sorted(elteres_b))
    with open(JAVASLAT_B, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki_b))
    v2 = {json.loads(s)['vers']: json.loads(s) for s in sorok if s.strip()}
    v3 = {json.loads(s)['vers']: json.loads(s) for s in ki if s.strip()}
    v3b = {json.loads(s)['vers']: json.loads(s) for s in ki_b if s.strip()}
    h_sorok, osszesito = hatas(v2, v3)
    uj_b = dict(UJ_OSZTALY)
    uj_b.update(UJ_OSZTALY_B)
    hb_sorok, osszesito_b = hatas(v2, v3b, uj_b)
    with open(DIFF_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(md(v2, v3, h_sorok, osszesito, v3b, hb_sorok, osszesito_b))
    print('javaslat: %d vers változott -> %s (NEM befagyasztott)' % (len(elteres), os.path.relpath(JAVASLAT, tokenek.ROOT)))
    print('B változat: +%d vers -> %s (NEM befagyasztott, NEM alkalmazott)' % (len(elteres_b), os.path.relpath(JAVASLAT_B, tokenek.ROOT)))
    for f in FUTASOK:
        print('%s: eltérés v2 %d -> B %d' % (f, osszesito_b[f]['v2'][3], osszesito_b[f]['v3j'][3]))
    print('diff: %s' % os.path.relpath(DIFF_UT, tokenek.ROOT))
    for f in FUTASOK:
        print('%s: eltérés v2 %d -> v3-javaslat %d' % (f, osszesito[f]['v2'][3], osszesito[f]['v3j'][3]))


if __name__ == '__main__':
    main()
