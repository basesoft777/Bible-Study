#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wlc_versek.py -- F41 (FELADATOK #41): a WLC (masszoreta) versszamozas gepi forrasa: a konkordancia/Macula_heber_*.tsv tablak (Macula Hebrew,
`ref` oszlop = 'GEN 1:1!1', a Macula (MT/WLC) szamozas; a `karoli` oszlopot NEM hasznaljuk, az KK-alapu Karoli-megfeleltetes).

Kozos modul: a bsb_import.py (a Pred/Ezs fejezethatar-igazolasa) es a bsb_wlc_versszam_ellenorzes.py hasznalja. Csak olvas; csv nelkul (split('\\t')).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# A Macula-kodok a Konyv_normalizalo_tabla elso 39 sorának (OSZ, kanonikus) sorrendjeben (a fajlnevek: eszkozok/f17/macula_import.py HEBER_KONYV_FAJL)
MACULA_KODOK = ['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA', '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB',
                'PSA', 'PRO', 'ECC', 'SNG', 'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP',
                'HAG', 'ZEC', 'MAL']
MACULA_FAJL = {'GEN': 'Genezis', 'EXO': 'Exodus', 'LEV': 'Leviticus', 'NUM': 'Numeri', 'DEU': 'Deuteronomium',
               'JOS': 'Jozsue', 'JDG': 'Birak', 'RUT': 'Ruth', '1SA': 'Samuel_1', '2SA': 'Samuel_2',
               '1KI': 'Kiralyok_1', '2KI': 'Kiralyok_2', '1CH': 'Kronikak_1', '2CH': 'Kronikak_2',
               'EZR': 'Ezsdras', 'NEH': 'Nehemias', 'EST': 'Eszter', 'JOB': 'Job', 'PSA': 'Zsoltarok',
               'PRO': 'Peldabeszedek', 'ECC': 'Predikator', 'SNG': 'Enekek_Eneke', 'ISA': 'Ezsaias',
               'JER': 'Jeremias', 'LAM': 'Siralmak', 'EZK': 'Ezekiel', 'DAN': 'Daniel', 'HOS': 'Hoseas',
               'JOL': 'Joel', 'AMO': 'Amos', 'OBA': 'Abdias', 'JON': 'Jonas', 'MIC': 'Mikeas', 'NAM': 'Nahum',
               'HAB': 'Habakuk', 'ZEP': 'Sofonias', 'HAG': 'Aggeus', 'ZEC': 'Zakarias', 'MAL': 'Malakias'}

_REF = re.compile(r'(\w+) (\d+):(\d+)')


def macula_kod(step):
    """A Konyv_normalizalo_tabla STEP-kodjabol (pl. 'Gen', '1Sa') a Macula-kod (pl. 'GEN', '1SA'), az OSZ-konyvek kanonikus sorrendje szerint."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'))
    lista = [s[0] for s in sorok[:39]]
    return MACULA_KODOK[lista.index(step)]


def wlc_konyv(kod):
    """{(fejezet, vers): set(Strong-szam int)}: a Macula-tabla `strong` oszlopa (H-szamok, a 9000-es prefixkodok nelkul). Az ures Strongu
    morfemak (pl. 'וְ' kotoszo) nem szamitanak, de a vers akkor is bekerul (ures halmazzal), ha minden szava ilyen."""
    ut = os.path.join(kozos.KONKORDANCIA, 'Macula_heber_%s.tsv' % MACULA_FAJL[kod])
    ki = {}
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#') or sor.startswith('xml_id'):
                continue
            p = sor.rstrip('\n').split('\t')
            if len(p) < 8:
                continue
            m = _REF.match(p[1])
            if not m or m.group(1) != kod:
                continue
            kulcs = (int(m.group(2)), int(m.group(3)))
            h = ki.setdefault(kulcs, set())
            if p[7].startswith('H'):
                n = kozos.strong_szam(p[7])
                if n is not None and n < 9000:
                    h.add(n)
    return ki


def wlc_fejezet_max(wlc):
    """{fejezet: max vers}."""
    ki = {}
    for (f, v) in wlc:
        ki[f] = max(ki.get(f, 0), v)
    return ki


def atfedes(wlc_halmaz, bsb_halmaz):
    """A WLC-vers (nem ures) Strong-halmazanak hanyad resze van a BSB-halmazban (a 9000-es prefixkodok nem szamitanak); ures WLC-halmaz: 0."""
    if not wlc_halmaz:
        return 0.0
    b = {n for n in bsb_halmaz if n < 9000}
    return len(wlc_halmaz & b) / len(wlc_halmaz)


def vers_egyezik(wlc_halmaz, bsb_halmaz):
    """Egyvers-kuszob (SZUKSEGES, nem elegseges feltetel): a WLC-vers atfedese a BSB-halmazzal > 0,5. Formulas szomszed versekkel is teljesul, ezert a
    szamozas-igazolashoz a vers_igazolt kell."""
    return atfedes(wlc_halmaz, bsb_halmaz) > 0.5


MARGO = 0.0  # (b)/(c): a WLC-vers atfedese legalabb MARGO-val legyen jobb a tobbinel (0 = szigoruan jobb); az alapertek a DT-F41g szerint 0; a bsb_parameter_erzekenyseg.py valtoztatja
D_ARANY = 0.5  # (d): a BSB-vers marad (nem magyarazott) Strongjainak e hanyadanal tobb a szomszed WLC-versben -> nem igazolt (DT-F41g; erzekenyseg: bsb_parameter_erzekenyseg.py)
D_DB = 2  # (d): es legalabb ennyi kozos Strong (DT-F41g)
ABLAK = 20  # a szomszed fejezetek elso/utolso ennyi verse is a kornyezethez tartozik (a fejezethatar-eltolas legnagyobb esete: 15 vers, 4Moz 16/17, 1Kron 5/6, 1Kir 4/5)


def wlc_index(wlc):
    """{fejezet: rendezett versszam-lista} a wlc_konyv eredmenyebol."""
    ki = {}
    for (f, v) in wlc:
        ki.setdefault(f, []).append(v)
    return {f: sorted(vs) for f, vs in ki.items()}


def kornyezet(idx, c):
    """A `c` = (fejezet, vers) WLC-vers kornyezete: a fejezet MINDEN verse + a szomszed fejezetek ABLAK elso/utolso verse (ez a lista c-t is tartalmazza)."""
    f = c[0]
    ki = [(f, v) for v in idx.get(f, [])]
    ki += [(f - 1, v) for v in idx.get(f - 1, [])[-ABLAK:]]
    ki += [(f + 1, v) for v in idx.get(f + 1, [])[:ABLAK]]
    return ki


def szomszedok(idx, c):
    """A `c` WLC-vers kozvetlen szomszedai (v-1, v+1), a fejezethataron atlepve (az elozo fejezet utolso / a kovetkezo fejezet elso verse)."""
    f, v = c
    vs = idx.get(f, [])
    ki = []
    if v > 1 and (f, v - 1) in {(f, x) for x in vs}:
        ki.append((f, v - 1))
    elif v == 1 and idx.get(f - 1):
        ki.append((f - 1, idx[f - 1][-1]))
    if vs and v == vs[-1] and idx.get(f + 1):
        ki.append((f + 1, idx[f + 1][0]))
    elif (f, v + 1) in {(f, x) for x in vs}:
        ki.append((f, v + 1))
    return ki


def bsb_kornyezet(fejezetek, f, v):
    """A BSB-vers (f, v) kornyezete: a fejezet TOBBI verse + a szomszed fejezetek ABLAK elso/utolso verse (fejezetek: {fej: {vers: set(Strong)}}); halmazok listaja."""
    ki = [h for u, h in fejezetek.get(f, {}).items() if u != v]
    ki += [fejezetek[f - 1][u] for u in sorted(fejezetek.get(f - 1, {}))[-ABLAK:]]
    ki += [fejezetek[f + 1][u] for u in sorted(fejezetek.get(f + 1, {}))[:ABLAK]]
    return ki


def vers_igazolt(wlc, idx, cel_versek, bsb_halmaz, bsb_tobbi, szomszed_parok=()):
    """Versszintu szamozas-igazolas (F41, DT-F41f; az F41_3 ellenorzes nyoman szigoritva). A BSB-vers (bsb_halmaz) igazolt MT-szamu, ha a `cel_versek` MINDEN WLC-versere
    (cel_versek: [(fejezet, vers)], egy vagy ket vers; wlc: {(fej, vers): set}; idx: wlc_index(wlc)):
      (a) az atfedes (a WLC-vers halmazanak hanyada a BSB-halmazban) > 0,5 (vers_egyezik), ES
      (b) szigoruan nagyobb, mint a WLC-kornyezet (kornyezet: a fejezet MINDEN mas verse + a szomszed fejezetek ABLAK elso/utolso verse) barmelyik masik versenek atfedese
          ugyanazzal a BSB-halmazzal (a ket cel-vers egymast nem szamit), ES
      (c) szigoruan nagyobb, mint ugyanazon WLC-vers atfedese a BSB-kornyezet (bsb_tobbi: a BSB-fejezet tobbi verse + a szomszed fejezetek szeleinek versei) barmelyik
          halmazaval, ES
      (d) reszvers-szuro: a BSB-halmaz azon Strong-szamai, amelyek nincsenek a cel-versekben, legfeljebb a felenek (es legfeljebb 1 szamnak) szabad valamelyik KOZVETLEN
          szomszed WLC-versben lenni; azaz ha a BSB-vers jelentos resze a szomszed WLC-veree (BSB-vers ⊋ WLC-vers), nem igazolt, ES
      (e) szomszed-egyezes: a szamozas vers-futamokra igaz, ezert a kozvetlen szomszed BSB-vers (v-1 / v+1, a fejezeten belul) es a megfelelo szomszed WLC-vers
          (a cel-vers elotti / utani) parjai (`szomszed_parok`: [(WLC-halmaz, BSB-halmaz)]) kozul legalabb egynek az atfedese > 0,5 (izolalt egyezes nem igazolt);
          ha nincs szomszed-par (egyversos fejezet), ez a pont nem szuri ki.
    Dontetlen (formulas ismetlodes), hibrid reszvers vagy izolalt egyezes -> False (a hivo `ellenorizetlen`-nek jeloli)."""
    if not cel_versek:
        return False
    cel = set(cel_versek)
    b = {n for n in bsb_halmaz if n < 9000}
    for c in cel_versek:
        w = wlc.get(c)
        a = atfedes(w, bsb_halmaz) if w else 0.0
        if a <= 0.5:
            return False
        for k in kornyezet(idx, c):
            if k in cel or k not in wlc:
                continue
            if atfedes(wlc[k], bsb_halmaz) + MARGO >= a:
                return False
        for bs in bsb_tobbi:
            if atfedes(w, bs) + MARGO >= a:
                return False
    magyarazott = set()
    for c in cel_versek:
        magyarazott |= wlc.get(c, set())
    marad = b - magyarazott
    if marad:
        for c in cel_versek:
            for k in szomszedok(idx, c):
                if k in cel or k not in wlc:
                    continue
                kozos_db = len(marad & wlc[k])
                if kozos_db >= D_DB and kozos_db > len(marad) * D_ARANY:
                    return False
    if szomszed_parok and not any(atfedes(w, h) > 0.5 for w, h in szomszed_parok):
        return False
    return True
