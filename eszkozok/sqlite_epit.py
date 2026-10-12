#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/sqlite_epit.py -- F79: a `pardes.db` (olvasoi konkordancia adatbazisa) epitoje.

A `pardes.db` GENERALT nezet (DT28; ADATVAGYON_TERV 21.): nem commitolt, kezzel nem
irhato, es nem ir vissza semmit az `adat/`-ba vagy a `konkordancia/`-ba. Ami szamitas
(strong_parok, frazis-pozicio), az epiteskor fut Pythonban; a lekerdezo csak kesz
tablakat olvas (ADATVAGYON 7.).

Lepesek:
  1. Integritas (a betoltes ELOTT, a TSV-sorlistakon): az `ellenoriz.py` szabaly1..8
     fuggvenyei + a SERTES-kepes 9., 10., 11., 13. (DT-F79a (3), (7)). Egy szabaly, egy
     implementacio: nincs masolat. Sertesnel az epites NEM ir kesz fajlt, kilepesi kod 1.
  2. Betoltes `split('\\t')`-vel (general.tsv_beolvas); a `csv` modul nem hasznalhato.
  3. Igehely-normalizalas: a STEPBible-alaku datasetek a `Konyv_normalizalo_tabla.tsv`-n at,
     a Siralmak kulcsa `Sir` (a normalizalo tabla `JSir`-je explicit alias; DT-F79a (6)).
     A nem leKepezheto / nem Karoli-versre mutato sor a `normalizalas_jelentes` tablaba kerul.
  4. Licenc: minden tablan `licenc_allapot`, `kereskedelmi`, `licenc_dataset` (az
     `adat/licencek.tsv`-bol). Alapertek nincs: licencsor nelkuli tabla kimarad, es a
     jelentesben all. Szarmaztatott tabla licence a forrasaie kozul a legszigorubb.

CLI:
    python eszkozok/sqlite_epit.py [--mod minta|teljes] [--kimenet FAJL] [--proba] [--naplo]

A `--mod minta` (alapertelmezes) az 1Mozest es a motivumok altal hivatkozott verseket
tolti be (ADATVAGYON 21., 3. szabaly). A `--mod teljes` a M4 lepes; a felhasznalo
jovahagyasa elott nem futtatando.

Kilepesi kod: 0 = rendben, 1 = integritas-sertes, 2 = hiba.
"""

import argparse
import datetime
import glob
import hashlib
import os
import re
import sqlite3
import sys
import time
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G  # noqa: E402
import ellenoriz as E  # noqa: E402
from strong_util import strong_normalizal  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A normalizalo tabla `Lam` -> `JSir` (DT24), az adat-kulcsok viszont `Sir` (Siralmak).
KONYV_ALIAS = {'JSir': 'Sir'}

# N46: a Karoli-kulcs 44 eltolodas-gyanus verse (NYITOTT_FELADATOK.md N46).
N46_TARTOMANYOK = [('Préd', 5, 1, 20), ('4Móz', 30, 1, 16), ('Zsolt', 13, 1, 6),
                   ('4Móz', 26, 1, 1), ('Zak', 3, 1, 1)]

RESERVALT_OSZLOP = {'licenc_allapot', 'kereskedelmi', 'licenc_dataset'}

# Tabla -> a licencek.tsv `dataset` kulcsai. Szarmaztatott tablanal tobb kulcs: a
# legszigorubb ertek ervenyes (DT-F79a (2c)).
SZARMAZTATOTT_LICENC = {
    'token_par': ['Karoli_1908', 'TAHOT', 'projekt_adat'],
    'token_karoli': ['Karoli_1908', 'TAHOT', 'projekt_adat'],
    'frazis_pozicio': ['Karoli_1908', 'TAHOT', 'projekt_adat'],
    'karoli_variancia': ['Karoli_1908', 'TAHOT', 'projekt_adat'],
    'token_eredeti': ['TAHOT', 'TAGNT'],
    'token_strong': ['TAHOT', 'TAGNT'],
    'strong_parok': ['TAHOT', 'TAGNT', 'projekt_adat'],
    'vers': ['Karoli_1908'],
    'vers_szamozas': ['Karoli_versmegfeleltetes', 'BSB_Strongs'],
    'konyv': ['Konyv_nevtablak'],
    'tsk': ['TSK'], 'kh': ['Karoli_KH'], 'tipnr': ['TIPNR'], 'bsb': ['BSB_Strongs'],
    'kjv': ['KJV_Strongs_teljes'],
    'lxx_bridge': ['lxx_bridge'], 'lxx_versszintu_parok': ['LXX_versszintu_parok'],
    'igehely_tartomany': ['projekt_adat'], 'normalizalas_jelentes': ['projekt_adat'],
    'meta': ['projekt_adat'], 'fts_motivum': ['projekt_adat'],
    'oshl_bdb_igehelyek': ['OSHL_BDB'], 'oshl_lexikalis_index': ['OSHL'],
}

# Altalanos (oszlopait valtozatlanul atvevo) konkordancia-tablak:
# (tabla, relativ fajl, strong-oszlop, igehely-oszlop (HU), licenc-kulcsok, csak_teljes)
KONKORDANCIA_ALTALANOS = [
    ('bdb', 'konkordancia/BDB_teljes_unabridged.tsv', 'Strong_padded', None, ['BDB'], False),
    ('strong_szotar', 'konkordancia/Strong_szotar.tsv', 'Strong-szám', None, ['Strong_szotar'], False),
    ('lxx_versszintu_parok', 'konkordancia/LXX_versszintu_parok.tsv', 'heber_strong', 'igehely',
     ['LXX_versszintu_parok'], False),
    ('thayer', 'konkordancia/Thayer_teljes.tsv', 'Strong_padded', None, ['Thayer'], True),
    ('lsj', 'konkordancia/LSJ_teljes.tsv', 'Strong_padded', None, ['LSJ'], True),
    ('sece_g', 'konkordancia/SECE_G_teljes.tsv', 'Strong_padded', None, ['SECE_G'], True),
    ('sece_h', 'konkordancia/SECE_H_teljes.tsv', 'Strong_padded', None, ['SECE_H'], True),
    ('mcged', 'konkordancia/MCGED_teljes.tsv', 'strong', None, ['MCGED'], True),
    ('sdbh_domenek', 'konkordancia/SDBH_domenek.tsv', 'strong', None, ['SDBH'], True),
    ('sdgnt_domenek', 'konkordancia/SDGNT_domenek.tsv', 'strong', None, ['SDGNT'], True),
    ('ubs_dbh_jelentesek', 'konkordancia/UBS_DBH_jelentesek.tsv', 'strong', None, ['UBS_DBH'], True),
    ('ubs_dntg_jelentesek', 'konkordancia/UBS_DNTG_jelentesek.tsv', 'strong', None, ['UBS_DNTG'], True),
    ('ubs_dbh_referenciak', 'konkordancia/UBS_DBH_referenciak.tsv', 'strong', 'igehely', ['UBS_DBH'], True),
    ('ubs_dntg_referenciak', 'konkordancia/UBS_DNTG_referenciak.tsv', 'strong', 'igehely', ['UBS_DNTG'], True),
    ('tw_szocikkek', 'konkordancia/tW_szocikkek.tsv', None, None, ['tW_szocikkek'], True),
    ('nave_basokant', 'konkordancia/Nave_basokant.tsv', None, None, ['Nave_basokant'], True),
    ('oshl_bdb_igehelyek', 'konkordancia/OSHL_BDB_igehelyek.tsv', 'strong', None, ['OSHL_BDB'], True),
    ('oshl_lexikalis_index', 'konkordancia/OSHL_lexikalis_index.tsv', 'strong', None, ['OSHL'], True),
    ('lxx_bridge', 'adat/kulso/lxx_bridge.tsv', 'hebrew_strong', None, ['lxx_bridge'], False),
]

ADAT_KIHAGYOTT = {'karoli_variancia'}  # külön kezelve (szarmaztatott licenc)

STRONG_RE = re.compile(r'^[HG]\d{4,5}$')
HU_IGEHELY_RE = re.compile(r'^(\S+) (\d+):(\d+)[a-z]?(?:-(?:(\d+):)?(\d+)[a-z]?)?$')
STEP_IGEHELY_RE = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)[a-z]?$')

SZIGOR_ALLAPOT = {'tisztazatlan': 0, 'tisztazott': 1, 'kozkincs': 2}
SZIGOR_KERESKEDELMI = {'nem': 0, 'tisztazatlan': 1, 'feltetelesen': 2, 'igen': 3}


class LicencHiany(Exception):
    pass


def azonosito(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[^a-z0-9]+', '_', s).strip('_')
    return s or 'oszlop'


def oszlopnevek(fejlec):
    ki = []
    for f in fejlec:
        n = azonosito(f)
        if n in RESERVALT_OSZLOP:
            n = 'forras_' + n
        while n in ki:
            n += '_'
        ki.append(n)
    return ki


def ts_most():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


# ---------------------------------------------------------------------------
# 1. Integritas -- az ellenoriz.py fuggvenyein at (nincs masolat)
# ---------------------------------------------------------------------------

def integritas(adat_dir):
    """(sorok:list[ellenoriz.Sor], sertesek:list[Sor]). A betoltes ELOTT, TSV-sorlistakon."""
    def be(nev):
        return G.tsv_beolvas(os.path.join(adat_dir, nev))[1]
    motivumok = be('motivumok.tsv')
    elofordulasok = be('elofordulasok.tsv')
    jeloltek = be('jeloltek.tsv')
    kapcsolatok = be('kapcsolatok.tsv')
    datasetek = be('datasetek.tsv')
    auditok = be('auditok.tsv')
    lexikon_hivatkozasok = be('lexikon_hivatkozasok.tsv')
    id_halmaz = {m['id'] for m in motivumok}
    sorok = [
        E.szabaly1_hivatkozasi_epseg(id_halmaz, elofordulasok, kapcsolatok, jeloltek, auditok),
        E.szabaly2_nincs_kozvetlen_ut(elofordulasok, jeloltek),
        E.szabaly3_proveniencia(elofordulasok, auditok),
        E.szabaly4_gerinc_elem(elofordulasok),
        E.szabaly5_karoli_triplet(elofordulasok),
        E.szabaly6_gate_kenyszer(motivumok),
        E.szabaly7_gate_jelentes(motivumok, elofordulasok),   # jelentes, nem kenyszer
        E.szabaly8_dataset_lefedettseg_gepi(motivumok, elofordulasok, auditok, datasetek)[0],
        E.szabaly9_teljes_jelentes_szam(elofordulasok, lexikon_hivatkozasok),
        E.szabaly10_v22_tablak(adat_dir),
        E.szabaly11_res_forras_egyezes(adat_dir),
        E.szabaly13_forditasi_gyorsitotar(adat_dir),
    ]
    sertesek = [s for s in sorok if s.verdict.split(' ', 1)[0] == 'SÉRTÉS']
    return sorok, sertesek


def integritas_md(sorok, adat_dir, mod):
    ki = ['# SQLITE_EPIT -- integritás-ellenőrzés (F79)', '',
          '*Proveniencia: `scope=manual | forras=%s | ts=%s`; az ellenőrzés a betöltés ELŐTT, '
          'a TSV-sorlistákon fut, az `eszkozok/ellenoriz.py` függvényeivel (DT-F79a (3), (7)); '
          'építési mód: %s.*' % (os.path.relpath(adat_dir, ROOT).replace(os.sep, '/') + '/*.tsv',
                                  ts_most(), mod), '']
    for s in sorok:
        ki.append(s.sor_szoveg())
        ki.append('')
    ki.append('A 7. szabály (gate.py ütközés/részhalmaz) jelentés, nem kényszer (a CLI sem '
              'számolja sértésnek); a 8/b és 8/c KÉZI sorok az `ellenoriz.py` kimenetében állnak.')
    return '\n'.join(ki) + '\n'


# ---------------------------------------------------------------------------
# 2. Igehely-segedek
# ---------------------------------------------------------------------------

class Konyvek(object):
    """Konyvkulcs-leKepezes: STEPBible-kod -> KK (Karoli) kod, alias-szal."""

    def __init__(self, konyv_tabla_sorok):
        self.step_hu = {}
        for r in konyv_tabla_sorok:
            hu = KONYV_ALIAS.get(r['Magyar rövidítés'], r['Magyar rövidítés'])
            self.step_hu[r['STEPBible-rövidítés']] = hu
            for a in r['Forrás-alakok'].split(','):
                a = a.strip()
                if a:
                    self.step_hu.setdefault(a, hu)
        self.sorok = konyv_tabla_sorok

    def hu(self, kod):
        return KONYV_ALIAS.get(kod, kod)

    def step_igehely(self, ertek):
        """'Gen.1.1' -> '1Móz 1:1'; None, ha nem leKepezheto."""
        m = STEP_IGEHELY_RE.match(ertek.strip())
        if not m:
            return None
        b = self.step_hu.get(m.group(1))
        if not b:
            return None
        return '%s %d:%d' % (b, int(m.group(2)), int(m.group(3)))

    def step_tartomany(self, ertek):
        """'Gen.2.4-Gen.2.5' vagy 'Gen.2.4' -> (tol, ig) KK-kulcsok; None, ha nem leKepezheto."""
        reszek = ertek.strip().split('-')
        if len(reszek) == 1:
            t = self.step_igehely(reszek[0])
            return (t, t) if t else None
        if len(reszek) == 2:
            t = self.step_igehely(reszek[0])
            i = self.step_igehely(reszek[1])
            return (t, i) if t and i else None
        return None


def hu_igehely_parse(ertek, konyvek=None):
    """'1Móz 14:18-20' -> (konyv, f1, v1, f2, v2); None, ha nem ertelmezheto."""
    m = HU_IGEHELY_RE.match(ertek.strip())
    if not m:
        return None
    k = KONYV_ALIAS.get(m.group(1), m.group(1))
    f1, v1 = int(m.group(2)), int(m.group(3))
    if m.group(5) is None:
        return (k, f1, v1, f1, v1)
    f2 = int(m.group(4)) if m.group(4) else f1
    return (k, f1, v1, f2, int(m.group(5)))


class VersIndex(object):
    def __init__(self, karoli_sorok):
        self.lista = []         # KK-kulcsok Karoli-sorrendben
        self.konyv_versei = {}  # konyv -> [(f, v, kulcs)]
        self.konyv_sorrend = {}
        for r in karoli_sorok:
            kulcs = r['Igehely']
            p = hu_igehely_parse(kulcs)
            if p is None or p[3:] != p[1:3]:
                raise ValueError('Karoli_1908: nem egy vers: %r' % kulcs)
            self.lista.append(kulcs)
            self.konyv_sorrend.setdefault(p[0], len(self.konyv_sorrend))
            self.konyv_versei.setdefault(p[0], []).append((p[1], p[2], kulcs))
        self.halmaz = set(self.lista)

    def kibont(self, ertek):
        """Igehely vagy tartomany -> [KK-versek] (a Karoli-ban letezok). None: nem ertelmezheto."""
        p = hu_igehely_parse(ertek)
        if p is None:
            return None
        k, f1, v1, f2, v2 = p
        return [kulcs for (f, v, kulcs) in self.konyv_versei.get(k, [])
                if (f1, v1) <= (f, v) <= (f2, v2)]


# ---------------------------------------------------------------------------
# 3. Az epito
# ---------------------------------------------------------------------------

class Epito(object):
    def __init__(self, gyoker, kimenet, mod):
        self.gyoker = gyoker
        self.adat = os.path.join(gyoker, 'adat')
        self.konk = os.path.join(gyoker, 'konkordancia')
        self.kimenet = kimenet
        self.mod = mod
        self.tmp = kimenet + '.epit'
        self.con = None
        self.licencek = {}
        self.tablak = {}          # nev -> sorszam
        self.kihagyott = []       # (tabla, ok)
        self.norm_jelentes = {}   # (tabla, nyers, ok) -> darab
        self.megjegyzesek = []

    # -- licenc ----------------------------------------------------------
    def licenc_feloldas(self, kulcsok):
        allapotok, ker = [], []
        for k in kulcsok:
            sor = self.licencek.get(k)
            if sor is None:
                raise LicencHiany('nincs licencek.tsv-sor: %s' % k)
            if not sor['allapot'] or not sor['kereskedelmi']:
                raise LicencHiany('üres licenc-mező: %s' % k)
            allapotok.append(sor['allapot'])
            ker.append(sor['kereskedelmi'])
        a = min(allapotok, key=lambda x: SZIGOR_ALLAPOT[x])
        c = min(ker, key=lambda x: SZIGOR_KERESKEDELMI[x])
        return a, c, '+'.join(kulcsok)

    def jelent_norm(self, tabla, nyers, ok):
        k = (tabla, nyers, ok)
        self.norm_jelentes[k] = self.norm_jelentes.get(k, 0) + 1

    # -- tabla-letrehozas -------------------------------------------------
    def tabla(self, nev, oszlopok, sorok, lic, indexek=()):
        """oszlopok: [(nev, tipus)]; sorok: iteralhato tuple-ok. Licenc nelkul nem epul."""
        try:
            a, c, ds = self.licenc_feloldas(lic)
        except LicencHiany as exc:
            self.kihagyott.append((nev, str(exc)))
            return False
        cols = list(oszlopok) + [('licenc_allapot', 'TEXT'), ('kereskedelmi', 'TEXT'),
                                 ('licenc_dataset', 'TEXT')]
        self.con.execute('CREATE TABLE "%s" (%s)' % (nev, ', '.join(
            '"%s" %s' % (n, t) for n, t in cols)))
        ph = ','.join('?' * len(cols))
        n = 0
        extra = (a, c, ds)

        def gen():
            nonlocal n
            for s in sorok:
                n += 1
                yield tuple(s) + extra
        self.con.executemany('INSERT INTO "%s" VALUES (%s)' % (nev, ph), gen())
        for i, ix in enumerate(indexek):
            self.con.execute('CREATE INDEX "ix_%s_%d" ON "%s" (%s)' % (nev, i, nev, ix))
        self.tablak[nev] = n
        return True

    def licenc_ellenorzes(self, nev, lic):
        try:
            self.licenc_feloldas(lic)
            return True
        except LicencHiany as exc:
            self.kihagyott.append((nev, str(exc)))
            return False

    # -- betoltes -----------------------------------------------------------
    def epit(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)
        self.con = sqlite3.connect(self.tmp)
        self.con.execute('PRAGMA journal_mode=OFF')
        self.con.execute('PRAGMA synchronous=OFF')
        try:
            self._epit()
            self.con.commit()
        except Exception:
            self.con.close()
            if os.path.exists(self.tmp):
                os.remove(self.tmp)
            raise
        self.con.close()
        if os.path.exists(self.kimenet):
            os.remove(self.kimenet)
        os.replace(self.tmp, self.kimenet)

    def _epit(self):
        _, licencsorok = G.tsv_beolvas(os.path.join(self.adat, 'licencek.tsv'))
        self.licencek = {r['dataset']: r for r in licencsorok}
        konyv_sorok = G.tsv_beolvas(os.path.join(self.konk, 'Konyv_normalizalo_tabla.tsv'))[1]
        self.konyvek = Konyvek(konyv_sorok)
        karoli = G.tsv_beolvas(os.path.join(self.konk, 'Karoli_1908.tsv'))[1]
        self.vi = VersIndex(karoli)
        self.minta = self._minta_versek() if self.mod == 'minta' else None
        self._konyv_vers(karoli)
        self._eredeti_tokenek()
        self._karoli_strong()
        self._kereszthivatkozasok()
        self._bsb_szamozas()
        self._altalanos()
        self._adat_tablak()
        self._tartomanyok()
        self._fts()
        self._jelentes_tabla()
        self._meta()

    # -- minta ---------------------------------------------------------------
    def _minta_versek(self):
        """1Moz + a motivumok adat-tablainak hivatkozott versei (elofordulasok, kapcsolatok,
        jeloltek, auditok `range:` scope-ja)."""
        halmaz = {k for (f, v, k) in self.vi.konyv_versei.get('1Móz', [])}
        ertekek = []
        for nev, oszlopok in (('elofordulasok.tsv', ['igehely']),
                              ('kapcsolatok.tsv', ['forras_igehely', 'cel_igehely']),
                              ('jeloltek.tsv', ['igehely'])):
            for r in G.tsv_beolvas(os.path.join(self.adat, nev))[1]:
                for o in oszlopok:
                    ertekek.append(r[o])
        for r in G.tsv_beolvas(os.path.join(self.adat, 'auditok.tsv'))[1]:
            sc = E.proveniencia_parse(r['proveniencia']).get('scope', '')
            if sc.startswith('range:'):
                ertekek.extend(x for x in sc[len('range:'):].split('+'))
        for e in ertekek:
            v = self.vi.kibont(e)
            if v:
                halmaz.update(v)
        return halmaz

    def _benne(self, kulcs):
        return self.minta is None or kulcs in self.minta

    # -- konyv, vers ---------------------------------------------------------
    def _konyv_vers(self, karoli):
        sorok = []
        for r in self.konyvek.sorok:
            hu = KONYV_ALIAS.get(r['Magyar rövidítés'], r['Magyar rövidítés'])
            if hu not in self.vi.konyv_sorrend:
                self.megjegyzesek.append('könyv a normalizáló táblában, Károli-vers nélkül: %s' % hu)
            sorok.append((hu, self.vi.konyv_sorrend.get(hu, 999), r['STEPBible-rövidítés'],
                          r['Teljes magyar könyvnév'], r['Magyar rövidítés']))
        self.tabla('konyv', [('kk_kod', 'TEXT'), ('sorrend', 'INTEGER'), ('step_kod', 'TEXT'),
                             ('teljes_nev', 'TEXT'), ('normalizalo_kod', 'TEXT')],
                   sorok, SZARMAZTATOTT_LICENC['konyv'], ['kk_kod'])
        sorok = []
        for i, r in enumerate(karoli):
            k = r['Igehely']
            if not self._benne(k):
                continue
            p = hu_igehely_parse(k)
            sorok.append((k, p[0], p[1], p[2], i, r['Károli-szöveg (teljes vers)']))
        self.tabla('vers', [('igehely', 'TEXT'), ('konyv', 'TEXT'), ('fejezet', 'INTEGER'),
                            ('vers', 'INTEGER'), ('sorrend', 'INTEGER'), ('karoli_szoveg', 'TEXT')],
                   sorok, SZARMAZTATOTT_LICENC['vers'], ['igehely', 'konyv, fejezet, vers'])

    # -- TAHOT / TAGNT tokenek, strong_parok --------------------------------------
    def _eredeti_tokenek(self):
        grammatikai = {r['strong'] for r in G.tsv_beolvas(
            os.path.join(self.adat, 'grammatikai_strongok.tsv'))[1]}
        tokenek, strongok = [], []
        vers_strongok = {}   # igehely -> set (strong_parok-hoz, a TELJES TAHOT/TAGNT-bol)
        for nyelv, fajl in (('H', 'TAHOT_kivonat.tsv'), ('G', 'TAGNT_kivonat.tsv')):
            fej, sorok = G.tsv_beolvas(os.path.join(self.konk, fajl))
            szamlalo = {}
            for r in sorok:
                ig = r['Igehely']
                szamlalo[ig] = szamlalo.get(ig, 0) + 1
                try:
                    lanc = strong_normalizal(r['Strong-szám'])
                except ValueError:
                    self.jelent_norm(fajl, r['Strong-szám'], 'Strong-szám nem normalizálható')
                    lanc = None
                elemek = lanc.split('+') if lanc else []
                for s in elemek:
                    if s in grammatikai or ('H9001' <= s <= 'H9049'):
                        continue
                    vers_strongok.setdefault(ig, set()).add(s)
                if not self._benne(ig):
                    continue
                n = szamlalo[ig]
                tokenek.append((ig, n, nyelv, lanc, r['Strong-szám'], r['Ragozott alak'],
                                r['Kiejtés'], r['Szótő'], r['Rövid jelentés'],
                                r['Angol tükörfordítás'], r.get('Kritikai kiadás', ''), fajl))
                for s in elemek:
                    strongok.append((ig, n, s))
        self.tabla('token_eredeti',
                   [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('nyelv', 'TEXT'),
                    ('strong_lanc', 'TEXT'), ('strong_nyers', 'TEXT'), ('alak', 'TEXT'),
                    ('kiejtes', 'TEXT'), ('szoto', 'TEXT'), ('rovid_jelentes', 'TEXT'),
                    ('angol_tukorford', 'TEXT'), ('kritikai_kiadas', 'TEXT'), ('forras_fajl', 'TEXT')],
                   tokenek, SZARMAZTATOTT_LICENC['token_eredeti'],
                   ['igehely, sorszam', 'strong_lanc'])
        self.tabla('token_strong', [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('strong', 'TEXT')],
                   strongok, SZARMAZTATOTT_LICENC['token_strong'], ['strong', 'igehely, sorszam'])
        # strong_parok: a TELJES TAHOT+TAGNT-bol (minta modban is), egyszer, epiteskor
        szamlalo = {}
        for ig, halmaz in vers_strongok.items():
            lista = sorted(halmaz)
            for i in range(len(lista)):
                for j in range(i + 1, len(lista)):
                    k = (lista[i], lista[j])
                    szamlalo[k] = szamlalo.get(k, 0) + 1
        self.tabla('strong_parok', [('a', 'TEXT'), ('b', 'TEXT'), ('n', 'INTEGER')],
                   ((a, b, n) for (a, b), n in sorted(szamlalo.items())),
                   SZARMAZTATOTT_LICENC['strong_parok'], ['a, b', 'n'])
        self.megjegyzesek.append('strong_parok: a teljes TAHOT+TAGNT-ból (%d vers, grammatikai_strongok '
                                 'és H9001-H9049 nélkül), mód-független' % len(vers_strongok))

    # -- Karoli-Strong -------------------------------------------------------------
    def _karoli_strong(self):
        if not self.licenc_ellenorzes('token_par', SZARMAZTATOTT_LICENC['token_par']):
            return
        pare, szav, poz = [], [], set()
        for f in sorted(glob.glob(os.path.join(self.adat, 'karoli_strong', 'parok_*.tsv'))):
            for r in G.tsv_beolvas(f)[1]:
                if not self._benne(r['vers']):
                    continue
                pare.append((r['vers'], int(r['hu_sorszam']), r['hu_szo'], int(r['er_sorszam']),
                             r['er_szo'], r['strong'], r['bizonyossag'], r['forras']))
                poz.add((r['vers'], 'hu', int(r['hu_sorszam']), r['strong'], r['hu_szo']))
                poz.add((r['vers'], 'er', int(r['er_sorszam']), r['strong'], r['er_szo']))
        for f in sorted(glob.glob(os.path.join(self.adat, 'karoli_strong', 'szavak_*.tsv'))):
            for r in G.tsv_beolvas(f)[1]:
                if not self._benne(r['vers']):
                    continue
                szav.append((r['vers'], r['oldal'], int(r['sorszam']), r['szo'], r['allapot'],
                             r['partner_sorszam'], r['strong'], r['bizonyossag'], r['forras']))
        lic = SZARMAZTATOTT_LICENC['token_par']
        self.tabla('token_par', [('igehely', 'TEXT'), ('hu_sorszam', 'INTEGER'), ('hu_szo', 'TEXT'),
                                 ('er_sorszam', 'INTEGER'), ('er_szo', 'TEXT'), ('strong', 'TEXT'),
                                 ('bizonyossag', 'TEXT'), ('forras', 'TEXT')],
                   pare, lic, ['strong', 'hu_szo', 'igehely, hu_sorszam'])
        self.tabla('token_karoli', [('igehely', 'TEXT'), ('oldal', 'TEXT'), ('sorszam', 'INTEGER'),
                                    ('szo', 'TEXT'), ('allapot', 'TEXT'), ('partner_sorszam', 'TEXT'),
                                    ('strong', 'TEXT'), ('bizonyossag', 'TEXT'), ('forras', 'TEXT')],
                   szav, SZARMAZTATOTT_LICENC['token_karoli'], ['igehely, oldal, sorszam', 'strong'])
        self.tabla('frazis_pozicio', [('igehely', 'TEXT'), ('oldal', 'TEXT'), ('sorszam', 'INTEGER'),
                                      ('strong', 'TEXT'), ('szo', 'TEXT')],
                   sorted(poz), SZARMAZTATOTT_LICENC['frazis_pozicio'],
                   ['igehely, oldal, sorszam', 'strong'])

    # -- TSK, Karoli-KH, TIPNR ---------------------------------------------------
    def _kereszthivatkozasok(self):
        tsk = []
        for r in G.tsv_beolvas(os.path.join(self.konk, 'TSK_kereszthivatkozasok.tsv'))[1]:
            if self._benne(r['Igehely']):
                tsk.append((r['Igehely'], r['Kapcsolódó igehely'], int(r['Votes'])))
        self.tabla('tsk', [('igehely', 'TEXT'), ('cel_igehely', 'TEXT'), ('votes', 'INTEGER')],
                   tsk, SZARMAZTATOTT_LICENC['tsk'], ['igehely', 'cel_igehely'])
        kh = []
        for r in G.tsv_beolvas(os.path.join(self.konk, 'Karoli_kereszthivatkozasok.tsv'))[1]:
            fo = self.konyvek.step_igehely(r['Igehely'])
            cel = self.konyvek.step_tartomany(r['Kapcsolódó igehely'])
            if fo is None:
                self.jelent_norm('kh', r['Igehely'], 'nem leképezhető')
            elif fo not in self.vi.halmaz:
                self.jelent_norm('kh', fo, 'nincs ilyen Károli-vers (forrás-oldal)')
            if cel is None:
                self.jelent_norm('kh', r['Kapcsolódó igehely'], 'nem leképezhető (cél-oldal)')
            else:
                for x in set(cel):
                    if x not in self.vi.halmaz:
                        self.jelent_norm('kh', x, 'nincs ilyen Károli-vers (cél-oldal)')
            if fo is not None and not self._benne(fo):
                continue
            if fo is None and self.minta is not None:
                continue
            kh.append((fo, r['Igehely'], cel[0] if cel else None, cel[1] if cel else None,
                       r['Kapcsolódó igehely'], 1 if (fo in self.vi.halmaz) else 0))
        self.tabla('kh', [('igehely', 'TEXT'), ('step_nyers', 'TEXT'), ('cel_tol', 'TEXT'),
                          ('cel_ig', 'TEXT'), ('cel_step_nyers', 'TEXT'), ('van_vers', 'INTEGER')],
                   kh, SZARMAZTATOTT_LICENC['kh'], ['igehely', 'cel_tol'])
        tip = []
        for r in G.tsv_beolvas(os.path.join(self.konk, 'TIPNR_kivonat.tsv'))[1]:
            ig = self.konyvek.step_igehely(r['Igehely'])
            if ig is None:
                self.jelent_norm('tipnr', r['Igehely'], 'nem leképezhető')
            elif ig not in self.vi.halmaz:
                self.jelent_norm('tipnr', ig, 'nincs ilyen Károli-vers')
            if self.minta is not None and (ig is None or ig not in self.minta):
                continue
            try:
                s = strong_normalizal(r['Strong-szám'])
            except ValueError:
                self.jelent_norm('tipnr', r['Strong-szám'], 'Strong-szám nem normalizálható')
                s = None
            tip.append((r['Név (normalizált)'], r['Névváltozat'], s, r['Strong-szám'], r['Nyelv'], ig, r['Igehely']))
        self.tabla('tipnr', [('nev', 'TEXT'), ('nevvaltozat', 'TEXT'), ('strong', 'TEXT'),
                             ('strong_nyers', 'TEXT'), ('nyelv', 'TEXT'), ('igehely', 'TEXT'), ('step_nyers', 'TEXT')],
                   tip, SZARMAZTATOTT_LICENC['tipnr'], ['igehely', 'strong'])

    # -- BSB + szamozas ------------------------------------------------------------
    def _bsb_szamozas(self):
        vm = G.tsv_beolvas(os.path.join(self.konk, 'Karoli_versmegfeleltetes.tsv'))[1]
        mt_kk = {}
        for r in vm:
            if r['igehely_mt']:
                p = hu_igehely_parse(r['igehely_karoli'])
                if p:
                    mt_kk[(p[0], r['igehely_mt'])] = r['igehely_karoli']
        # BSB: MT-szamozas; a KK-ra a versmegfeleltetes MT-oszlopan at, kulonben azonos szam
        # (feltetelezett -- jelolve a `kk_leképezés` oszlopban)
        bsb, szamozas_vers = [], {}
        rang = {'mt': 0, 'kjv': 1, 'ellenorizetlen': 2}
        szamlalo = {}
        for r in G.tsv_beolvas(os.path.join(self.konk, 'BSB_Strongs.tsv'))[1]:
            m = STEP_IGEHELY_RE.match(r['Igehely'])
            if not m:
                self.jelent_norm('bsb', r['Igehely'], 'nem leképezhető')
                continue
            konyv = self.konyvek.step_hu.get(m.group(1))
            if konyv is None:
                self.jelent_norm('bsb', r['Igehely'], 'könyv nem leképezhető')
                continue
            mtkulcs = '%d:%d' % (int(m.group(2)), int(m.group(3)))
            if (konyv, mtkulcs) in mt_kk:
                kk, mod = mt_kk[(konyv, mtkulcs)], 'mt_tabla'
            else:
                kk, mod = '%s %s' % (konyv, mtkulcs), 'azonos_feltetelezett'
            if kk not in self.vi.halmaz:
                self.jelent_norm('bsb', kk, 'nincs ilyen Károli-vers')
                continue
            sz = r['Számozás']
            prev = szamozas_vers.get(kk)
            if prev is None or rang.get(sz, 2) > rang.get(prev, 2):
                szamozas_vers[kk] = sz
            if not self._benne(kk):
                continue
            szamlalo[kk] = szamlalo.get(kk, 0) + 1
            try:
                s = strong_normalizal(r['Strong-szám'])
            except ValueError:
                s = None
                self.jelent_norm('bsb', r['Strong-szám'], 'Strong-szám nem normalizálható')
            bsb.append((kk, szamlalo[kk], s, r['Angol szó'], r['Morfológiai kód'],
                        r['Angol szó állapota'], sz, r['Igehely'], mod))
        self.tabla('bsb', [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('strong', 'TEXT'),
                           ('angol_szo', 'TEXT'), ('morf', 'TEXT'), ('angol_szo_allapot', 'TEXT'),
                           ('szamozas', 'TEXT'), ('step_nyers', 'TEXT'), ('kk_leképezés', 'TEXT')],
                   bsb, SZARMAZTATOTT_LICENC['bsb'], ['igehely, sorszam', 'strong'])
        n46 = set()
        for (k, f, v1, v2) in N46_TARTOMANYOK:
            for (ff, vv, kulcs) in self.vi.konyv_versei.get(k, []):
                if ff == f and v1 <= vv <= v2:
                    n46.add(kulcs)
        sorok = []
        for r in vm:
            k = r['igehely_karoli']
            if not self._benne(k):
                continue
            if k in n46:
                sz, fo = 'eltolodas_gyanu_N46', 'NYITOTT_FELADATOK.md N46'
            elif k in szamozas_vers:
                sz, fo = szamozas_vers[k], 'BSB_Strongs.tsv 7. oszlop'
            else:
                sz, fo = 'nincs_adat', ''
            sorok.append((k, r['osztaly'], r['igehely_kjv'], r['igehely_mt'], sz, fo, r['forras']))
        self.tabla('vers_szamozas', [('igehely', 'TEXT'), ('osztaly', 'TEXT'), ('kjv_igehely', 'TEXT'),
                                     ('mt_igehely', 'TEXT'), ('szamozas', 'TEXT'),
                                     ('szamozas_forras', 'TEXT'), ('megfeleltetes_forras', 'TEXT')],
                   sorok, SZARMAZTATOTT_LICENC['vers_szamozas'], ['igehely'])

    # -- altalanos konkordancia-tablak, adat-tablak ------------------------------------
    def _altalanos_betolt(self, nev, relfajl, strong_o, igehely_o, lic):
        if not self.licenc_ellenorzes(nev, lic):
            return
        fej, sorok = G.tsv_beolvas(os.path.join(self.gyoker, relfajl))
        nevek = oszlopnevek(fej)
        strong_idx = fej.index(strong_o) if strong_o and strong_o in fej else None
        ig_idx = fej.index(igehely_o) if igehely_o and igehely_o in fej else None
        oszlopok = [(n, 'TEXT') for n in nevek]
        if strong_idx is not None:
            oszlopok.append(('strong', 'TEXT')) if 'strong' not in nevek else None
        ki = []
        for r in sorok:
            vals = [r[f] for f in fej]
            if ig_idx is not None and self.minta is not None:
                v = self.vi.kibont(vals[ig_idx])
                if not v or not (set(v) & self.minta):
                    continue
            if strong_idx is not None:
                try:
                    s = strong_normalizal(vals[strong_idx], utotag='megtart')
                except ValueError:
                    s = None
                    self.jelent_norm(nev, vals[strong_idx], 'Strong-szám nem normalizálható')
                if 'strong' in nevek:
                    vals[strong_idx] = s
                else:
                    vals.append(s)
            ki.append(vals)
        ix = ['strong'] if strong_idx is not None else []
        if ig_idx is not None:
            ix.append(nevek[ig_idx])
        self.tabla(nev, oszlopok, ki, lic, ix)

    def _altalanos(self):
        for (nev, rel, so, io, lic, csak_teljes) in KONKORDANCIA_ALTALANOS:
            if csak_teljes and self.mod != 'teljes':
                continue
            self._altalanos_betolt(nev, rel, so, io, lic)

    def _adat_tablak(self):
        for f in sorted(glob.glob(os.path.join(self.adat, '*.tsv'))):
            nev = os.path.splitext(os.path.basename(f))[0]
            if nev in ADAT_KIHAGYOTT:
                continue
            self._altalanos_betolt(nev, 'adat/%s.tsv' % nev, None, None, ['projekt_adat'])
        # karoli_variancia: szarmaztatott licenc, csak teljes modban (42 ezer sor)
        if self.mod == 'teljes':
            self._altalanos_betolt('karoli_variancia', 'adat/karoli_variancia.tsv', None, None,
                                   SZARMAZTATOTT_LICENC['karoli_variancia'])

    # -- igehely_tartomany ---------------------------------------------------------------
    def _tartomanyok(self):
        sorok = []
        forrasok = (('elofordulasok', ['igehely'], ['id']),
                    ('kapcsolatok', ['forras_igehely', 'cel_igehely'], ['id']),
                    ('jeloltek', ['igehely'], ['id']))
        for tabla, oszl, kulcs in forrasok:
            for r in G.tsv_beolvas(os.path.join(self.adat, tabla + '.tsv'))[1]:
                for o in oszl:
                    v = self.vi.kibont(r[o])
                    sk = '|'.join([r[k] for k in kulcs] + [r[x] for x in oszl])
                    if v is None:
                        self.jelent_norm('igehely_tartomany', r[o], 'nem értelmezhető igehely (%s.%s)' % (tabla, o))
                        continue
                    for x in v:
                        sorok.append((tabla, sk, o, r[o], x))
        self.tabla('igehely_tartomany', [('forras_tabla', 'TEXT'), ('forras_kulcs', 'TEXT'),
                                         ('oszlop', 'TEXT'), ('ertek', 'TEXT'), ('igehely', 'TEXT')],
                   sorok, SZARMAZTATOTT_LICENC['igehely_tartomany'], ['igehely', 'forras_tabla, forras_kulcs'])

    # -- FTS -----------------------------------------------------------------------------
    def _fts(self):
        if not self.licenc_ellenorzes('fts_motivum', SZARMAZTATOTT_LICENC['fts_motivum']):
            return
        a, c, ds = self.licenc_feloldas(SZARMAZTATOTT_LICENC['fts_motivum'])
        self.con.execute(
            'CREATE VIRTUAL TABLE fts_motivum USING fts5(szoveg, motivum_id UNINDEXED, rovat UNINDEXED, '
            'forras_fajl UNINDEXED, regi_forras UNINDEXED, licenc_allapot UNINDEXED, '
            'kereskedelmi UNINDEXED, licenc_dataset UNINDEXED, tokenize="unicode61 remove_diacritics 2")')
        motivumok = G.tsv_beolvas(os.path.join(self.adat, 'motivumok.tsv'))[1]
        regi_id = {}
        for m in motivumok:
            for p in m['forras_study'].split(';'):
                p = p.strip().replace('\\', '/')
                if p:
                    regi_id[p] = m['id']
        migralt = set()
        fajlok = []
        for f in sorted(glob.glob(os.path.join(self.gyoker, 'motivumok', '*.md'))):
            mid = os.path.splitext(os.path.basename(f))[0]
            with open(f, encoding='utf-8', newline='') as fh:
                fej = ''.join(fh.readlines()[:40])
            if re.search(r'^\s*(<!--\s*)?migralt:\s*igen', fej, re.M):
                migralt.add(mid)
            fajlok.append((f, mid, 0))
        mintak = ['tematikus_lezart/*_tematikus.md', 'tematikus_lezart/naplok/*_kereszthivatkozas_naplo.md',
                  'genezis/1Moz_*_bovitett.md', 'genezis/naplok/*.md', 'ujszovetseg/*_bovitett.md',
                  'melyelemzesek/*.md']
        kiesett = []
        for minta in mintak:
            for f in sorted(glob.glob(os.path.join(self.gyoker, minta))):
                rel = os.path.relpath(f, self.gyoker).replace(os.sep, '/')
                mid = regi_id.get(rel, '')
                if not mid and '/naplok/' in rel:
                    # a napló a tanulmány motívumához tartozik (fájlnév-előtag egyezés)
                    alap = os.path.basename(rel).replace('_kereszthivatkozas_naplo.md', '')
                    for p, i in regi_id.items():
                        if os.path.basename(p).startswith(alap):
                            mid = i
                            break
                if mid and mid in migralt:
                    kiesett.append(rel)
                    continue
                fajlok.append((f, mid, 1))
        n = 0
        for f, mid, regi in fajlok:
            rel = os.path.relpath(f, self.gyoker).replace(os.sep, '/')
            with open(f, encoding='utf-8', newline='') as fh:
                szoveg = fh.read().replace('\r\n', '\n')
            for rovat, torzs in _rovatok(szoveg):
                if not torzs.strip():
                    continue
                self.con.execute('INSERT INTO fts_motivum VALUES (?,?,?,?,?,?,?,?)',
                                 (torzs, mid, rovat, rel, regi, a, c, ds))
                n += 1
        self.tablak['fts_motivum'] = n
        self.megjegyzesek.append('FTS: %d fájl, %d rovat; átmeneti régi tanulmányok `regi_forras=1`; '
                                 'a #11 `migralt: igen` jelzője miatt kiesett: %s'
                                 % (len(fajlok), n, ', '.join(kiesett) if kiesett else 'nincs (a jelző még nem létezik)'))

    # -- jelentes, meta -----------------------------------------------------------------------
    def _jelentes_tabla(self):
        if self.mod == 'teljes':
            self.megjegyzesek.append(
                'Nem betöltött konkordancia-táblák (a DT-F79a és a brief hatóköre nem nevezi őket): '
                'Macula_heber_*/Macula_gorog, LXX_OS/*, KJV_Strongs_teljes és KJV_/ASV_Strongs_* (a #48 vezeti ki), '
                'TBESG/TBESH, Karoli_Strong_kivonat, a BDB_*/aram/alias segédtáblák, SDBH_SDGNT_domenfa; '
                'a licenc-sor hiánya miatt kimaradt táblák száma: %d' % len(self.kihagyott))
        sorok = [(t, nyers, ok, d) for (t, nyers, ok), d in sorted(self.norm_jelentes.items())]
        self.tabla('normalizalas_jelentes', [('tabla', 'TEXT'), ('nyers', 'TEXT'), ('ok', 'TEXT'),
                                             ('darab', 'INTEGER')],
                   sorok, SZARMAZTATOTT_LICENC['normalizalas_jelentes'], ['tabla'])

    def _meta(self):
        self.tabla('meta', [('kulcs', 'TEXT'), ('ertek', 'TEXT')],
                   [('mod', self.mod), ('epites_ts', ts_most()),
                    ('forras', 'adat/*.tsv, konkordancia/*.tsv (eszkozok/sqlite_epit.py, F79)'),
                    ('kihagyott_tablak', '; '.join('%s (%s)' % k for k in self.kihagyott))],
                   SZARMAZTATOTT_LICENC['meta'])


def _rovatok(szoveg):
    """Markdown `#`-fejlecek szerinti rovatok: [(fejlec, torzs)]."""
    ki, fej, buf = [], '(bevezető)', []
    for sor in szoveg.split('\n'):
        if re.match(r'^#{1,4} ', sor):
            ki.append((fej, '\n'.join(buf)))
            fej, buf = sor.lstrip('#').strip(), []
        else:
            buf.append(sor)
    ki.append((fej, '\n'.join(buf)))
    return ki


# ---------------------------------------------------------------------------
# 4. Tartalom-hash (G2), meres
# ---------------------------------------------------------------------------

def tablak_hash(db_path):
    """{tabla: (sorszam, sha256)} -- a rendezett tartalomra; a `meta` kimarad."""
    con = sqlite3.connect(db_path)
    try:
        nevek = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "AND name NOT LIKE 'fts_motivum_%' AND name != 'meta' ORDER BY name")]
        ki = {}
        for n in nevek:
            oszlopszam = len(con.execute('PRAGMA table_info("%s")' % n).fetchall())
            order = ','.join(str(i + 1) for i in range(oszlopszam))
            h = hashlib.sha256()
            db = 0
            for row in con.execute('SELECT * FROM "%s" ORDER BY %s' % (n, order)):
                h.update(('\t'.join('' if v is None else str(v) for v in row) + '\n').encode('utf-8'))
                db += 1
            ki[n] = (db, h.hexdigest())
        return ki
    finally:
        con.close()


# ---------------------------------------------------------------------------
# 5. Lekerdezes-proba (M3): az ADATVAGYON 26 pontjabol az 1-6., 13-15.
# ---------------------------------------------------------------------------

def _be(gyoker, rel):
    return G.tsv_beolvas(os.path.join(gyoker, rel))[1]


def probak(db_path, gyoker):
    con = sqlite3.connect(db_path)
    vi = VersIndex(_be(gyoker, 'konkordancia/Karoli_1908.tsv'))
    ki = []

    def q(sql, par=()):
        return con.execute(sql, par).fetchall()

    def rogzit(pont, cim, sql, eredmeny, elvart, ok, forras, megj=''):
        ki.append({'pont': pont, 'cim': cim, 'sql': sql, 'eredmeny': eredmeny, 'elvart': elvart,
                   'ok': ok, 'forras': forras, 'megj': megj})

    # 1: Strong -> osszes vers (H0922 az OT-ben 3 helyen: a TEREMT-002 auditjabol)
    sql = "SELECT DISTINCT igehely FROM token_strong WHERE strong='H0922' ORDER BY igehely"
    er = [r[0] for r in q(sql)]
    elv = set()
    for r in _be(gyoker, 'adat/elofordulasok.tsv'):
        if r['id'] == 'TEREMT-002':
            elv.update(vi.kibont(r['igehely']) or [])
    rogzit(1, 'H0922 -> összes vers', sql, er, sorted(elv), set(er) == elv,
           'adat/elofordulasok.tsv TEREMT-002 (H8414+H0922, 3 sor), ADATVAGYON 4. pont mintaképe')
    # 2: magyar szo -> Strong-lista
    sql = ("SELECT strong, COUNT(*) FROM token_par WHERE hu_szo='mélység' GROUP BY strong "
           "ORDER BY COUNT(*) DESC")
    er = q(sql)
    rogzit(2, '„mélység” -> Strong-lista', sql, er, ['H8415 szerepel'],
           any(s == 'H8415' for s, _ in er),
           'adat/elofordulasok.tsv TEREMT-001 1Móz 1:2 (karoli_szo=mélység, strong=H8415)')
    # 3: Strong -> Karoli-szoalakok
    sql = ("SELECT hu_szo, COUNT(*) FROM token_par WHERE strong='H3548' GROUP BY hu_szo "
           "ORDER BY COUNT(*) DESC")
    er = q(sql)
    rogzit(3, 'H3548 -> Károli-szóalakok', sql, er, ['papja szerepel'],
           any(s.lower() == 'papja' for s, _ in er),
           'adat/elofordulasok.tsv KIRALY-001 1Móz 14:18-20 (karoli_szo=papja, strong=H3548)')
    # 4: ket Strong egy versben
    sql = ("SELECT DISTINCT a.igehely FROM token_strong a JOIN token_strong b ON a.igehely=b.igehely "
           "WHERE a.strong='H8414' AND b.strong='H0922' ORDER BY a.igehely")
    er = [r[0] for r in q(sql)]
    rogzit(4, 'H8414 + H0922 egy versben', sql, er, sorted(elv), set(er) == elv,
           'adat/elofordulasok.tsv TEREMT-002 (1Móz 1:2, Jer 4:23, Ézs 34:11)')
    # 5: fraziskeres: H7121 utan legfeljebb 6 tokenre H8034 (ISTENTISZT-001)
    sql = ("SELECT DISTINCT a.igehely FROM token_strong a JOIN token_strong b ON a.igehely=b.igehely "
           "AND b.sorszam<>a.sorszam AND ABS(b.sorszam-a.sorszam)<=6 "
           "WHERE a.strong='H7121' AND b.strong='H8034' ORDER BY a.igehely")
    er = {r[0] for r in q(sql)}
    sorok5 = []
    for r in _be(gyoker, 'adat/elofordulasok.tsv'):
        if r['id'] == 'ISTENTISZT-001' and r['gerinc_elem'] == 'H7121+H8034':
            sorok5.append((r['igehely'], set(vi.kibont(r['igehely']) or [])))
    hianyzik = [ig for ig, v in sorok5 if not (v & er)]
    elv5 = set().union(*[v for _, v in sorok5])
    extra = sorted(er - elv5)
    rogzit(5, 'frázis: H7121 és H8034 (±6 token)', sql, sorted(er),
           '%d elofordulasok-sor mindegyike szerepel (ISTENTISZT-001, gerinc H7121+H8034)' % len(sorok5),
           not hianyzik,
           'adat/elofordulasok.tsv ISTENTISZT-001 (gerinc_elem=H7121+H8034)',
           'hiányzó sor: %s | az elvárt listán kívüli találat: %d vers (a puszta Strong-pár a névadó '
           '„hívta a nevét” fordulatot is fogja; ez keresési találat, nem study-sor: CLAUDE.md 2. szabály) %s'
           % (', '.join(hianyzik) or '-', len(extra), ', '.join(extra[:12])))
    # 6: gyok es szarmazek
    sql = "SELECT strong, gyok_szarmaztatas FROM strong_szotar WHERE strong IN ('H0922','H8414')"
    er = q(sql)
    forr = {r['Strong-szám']: r['Gyök/Származtatás'] for r in _be(gyoker, 'konkordancia/Strong_szotar.tsv')}
    rogzit(6, 'gyök (H0922, H8414)', sql, er, ['unused root mindkettőnél'],
           all('unused root' in (forr.get(s) or '') and g == forr.get(s) for s, g in er) and len(er) == 2,
           'konkordancia/Strong_szotar.tsv (Gyök/Származtatás)')
    # 13: szocikk + motivum-tartomany
    sql = ("SELECT l.strong, l.szotar, l.jelentes_szam, length(b.teljes_szocikk), "
           "(SELECT COUNT(*) FROM elofordulasok e WHERE e.jelentes_szam=l.jelentes_szam AND e.strong LIKE '%'||l.strong||'%' AND e.id='ISTENTISZT-001') "
           "FROM lexikon_hivatkozasok l JOIN bdb b ON b.strong=l.strong "
           "WHERE l.strong='H7121' AND l.szotar='BDB' ORDER BY l.jelentes_szam")
    er = q(sql)
    jsz = {r['jelentes_szam'] for r in _be(gyoker, 'adat/lexikon_hivatkozasok.tsv')
           if r['strong'] == 'H7121' and r['szotar'] == 'BDB'}
    rogzit(13, 'BDB H7121: jelentés-sorok és a motívum tartománya', sql, er,
           'jelentes_szam: %s; a 2.c-hez ISTENTISZT-001 sorok' % ', '.join(sorted(jsz)),
           {r[2] for r in er} == jsz and all((r[3] or 0) > 0 for r in er)
           and any(r[2] == '2.c' and r[4] > 0 for r in er),
           'adat/lexikon_hivatkozasok.tsv, adat/elofordulasok.tsv (jelentes_szam=2.c)')
    # 14: LXX-hid: H8415 -> G0012 -> USZ
    sql = "SELECT greek_strong, count FROM lxx_bridge WHERE hebrew_strong='H8415' ORDER BY CAST(count AS INTEGER) DESC"
    er = q(sql)
    hid = [(r['greek_strong'], r['count']) for r in _be(gyoker, 'adat/kulso/lxx_bridge.tsv')
           if r['hebrew_strong'] == 'H8415']
    sql2 = "SELECT DISTINCT igehely FROM token_strong WHERE strong='G0012' ORDER BY igehely"
    usz = {r[0] for r in q(sql2)}
    sorok14 = []
    for r in _be(gyoker, 'adat/elofordulasok.tsv'):
        if r['id'] == 'TEREMT-001' and r['gerinc_elem'] == 'G0012':
            sorok14.append((r['igehely'], set(vi.kibont(r['igehely']) or [])))
    hiany14 = [ig for ig, v in sorok14 if not (v & usz)]
    rogzit(14, 'LXX-híd H8415 -> G0012 -> ÚSZ', sql + ' ; ' + sql2, {'hid': er, 'usz': sorted(usz)},
           'híd: %s; az ÚSZ-találat lefedi mind a %d elofordulasok-sort' % (hid, len(sorok14)),
           sorted(er) == sorted(hid) and not hiany14,
           'adat/kulso/lxx_bridge.tsv; adat/elofordulasok.tsv TEREMT-001 (G0012)',
           'nem lefedett elofordulasok-sor: %s (a tartomány-sorok, pl. Jel 20:1-3, egy versen kapnak találatot)'
           % (', '.join(hiany14) or '-'))
    # 15: kiejtes
    sql = ("SELECT DISTINCT kiejtes FROM token_eredeti WHERE igehely='1Móz 1:2' AND strong_lanc='H8415'")
    er = [r[0] for r in q(sql)]
    sz = {r['Strong-szám']: r['Kiejtés'] for r in _be(gyoker, 'konkordancia/Strong_szotar.tsv')}
    rogzit(15, 'kiejtés (H8415, 1Móz 1:2)', sql, er, [sz.get('H8415')], er == [sz.get('H8415')],
           'konkordancia/Strong_szotar.tsv H8415 Kiejtés')
    con.close()
    return ki


def proba_md(eredmenyek):
    ki = []
    for p in eredmenyek:
        ki.append('### %d. pont -- %s: **%s**' % (p['pont'], p['cim'], 'MEGEGYEZIK' if p['ok'] else 'ELTÉRÉS'))
        ki.append('')
        ki.append('- SQL: `%s`' % p['sql'].replace('|', '\\|'))
        ki.append('- eredmény: `%s`' % str(p['eredmeny'])[:600].replace('|', '\\|'))
        ki.append('- várt: %s' % (p['elvart'],))
        ki.append('- forrás: %s' % p['forras'])
        if p['megj']:
            ki.append('- megjegyzés: %s' % p['megj'])
        ki.append('')
    return '\n'.join(ki)


def licenc_helyfoglalas(db_path):
    """{tabla: (sorszam, licenc_oszlopok_bajtja)} -- a 3 licenc_* oszlop tartalmanak bajtjai
    (a rekord-fejlec nelkul; alsó becslés), a #86 N-F86b bemenete."""
    con = sqlite3.connect(db_path)
    try:
        ki = {}
        for (n,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                                "AND name NOT LIKE 'fts_motivum_%' ORDER BY name").fetchall():
            db, b = con.execute('SELECT COUNT(*), IFNULL(SUM(LENGTH(CAST(licenc_allapot AS BLOB))+'
                                'LENGTH(CAST(kereskedelmi AS BLOB))+LENGTH(CAST(licenc_dataset AS BLOB))),0) '
                                'FROM "%s"' % n).fetchone()
            ki[n] = (db, b)
        return ki
    finally:
        con.close()


def meres_md(epito, hashek, ido, meret, mod, proba=None, licenc_hely=None):
    ki = ['# SQLITE_EPIT -- mérés (%s) (F79)' % ('kis minta' if mod == 'minta' else 'teljes építés'), '',
          '*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod %s) | ts=%s`*' % (mod, ts_most()),
          '', '- fájl: `%s`, **%.1f MB**; építési idő (integritás nélkül): **%.1f s**'
          % (os.path.basename(epito.kimenet), meret / 1048576.0, ido), '']
    if mod == 'minta':
        ki.append('- minta: %d Károli-vers (1Móz + a motívumok hivatkozott versei)' % len(epito.minta))
        ki.append('')
    ki += ['## Táblánkénti sorszám és tartalom-hash', '', '| tábla | sor | sha256 (rendezett tartalom) |', '|---|---:|---|']
    for n, (db, h) in sorted(hashek.items()):
        ki.append('| `%s` | %d | `%s` |' % (n, db, h[:16]))
    ki.append('')
    if licenc_hely:
        osszes_b = sum(b for _, b in licenc_hely.values())
        ki += ['## A `licenc_*` oszlopok helyfoglalása (a #86 N-F86b bemenete)', '',
               'A három oszlop (`licenc_allapot`, `kereskedelmi`, `licenc_dataset`) minden sorban ismétlődik. '
               'Az alábbi bájtszám az oszlopok tartalma (rekord-fejléc és index nélkül, alsó becslés).', '',
               '- összesen: **%.1f MB** a **%.1f MB**-os fájlból (%.1f%%)' % (
                   osszes_b / 1048576.0, meret / 1048576.0, 100.0 * osszes_b / meret),
               '', '| tábla | sor | licenc_* bájt | MB |', '|---|---:|---:|---:|']
        for n, (db, b) in sorted(licenc_hely.items(), key=lambda x: -x[1][1])[:12]:
            ki.append('| `%s` | %d | %d | %.2f |' % (n, db, b, b / 1048576.0))
        ki.append('')
    if epito.kihagyott:
        ki += ['## Kimaradt táblák (licencsor hiánya, G6)', '']
        ki += ['- `%s`: %s' % k for k in epito.kihagyott]
        ki.append('')
    osszes = {}
    for (t, nyers, ok), d in epito.norm_jelentes.items():
        osszes.setdefault((t, ok), []).append((nyers, d))
    if osszes:
        ki += ['## Normalizálási jelentés (G5: nincs néma nem-találat)', '',
               '| tábla | ok | darab (különböző érték / előfordulás) | példák |', '|---|---|---|---|']
        for (t, ok), lista in sorted(osszes.items()):
            ki.append('| %s | %s | %d / %d | %s |' % (t, ok, len(lista), sum(d for _, d in lista),
                      ', '.join('`%s`' % n for n, _ in sorted(lista)[:6])))
        ki.append('')
    if epito.megjegyzesek:
        ki += ['## Megjegyzések', ''] + ['- %s' % m for m in epito.megjegyzesek] + ['']
    if proba is not None:
        ki += ['## Lekérdezés-próba (M3: ADATVAGYON 4. pont, 1–6., 13–15.)', '', proba_md(proba)]
    return '\n'.join(ki) + '\n'


def irj(path, szoveg):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)


def main(argv=None):
    ap = argparse.ArgumentParser(description='F79 -- pardes.db építő')
    ap.add_argument('--mod', choices=('minta', 'teljes'), default='minta')
    ap.add_argument('--gyoker', default=ROOT, help='a repó gyökere (tesztekhez)')
    ap.add_argument('--kimenet', default=None)
    ap.add_argument('--proba', action='store_true', help='lekérdezés-próba a kész adatbázison')
    ap.add_argument('--naplo', action='store_true', help='naplok/SQLITE_EPIT_*.md megírása')
    args = ap.parse_args(argv)
    kimenet = args.kimenet or os.path.join(args.gyoker, 'pardes_minta.db' if args.mod == 'minta' else 'pardes.db')
    adat = os.path.join(args.gyoker, 'adat')

    try:
        sorok, sertesek = integritas(adat)
    except Exception as exc:
        print('HIBA (integritás): %s' % exc, file=sys.stderr)
        return 2
    if args.naplo:
        irj(os.path.join(args.gyoker, 'naplok', 'SQLITE_EPIT_integritas.md'), integritas_md(sorok, adat, args.mod))
    if sertesek:
        print('INTEGRITÁS-SÉRTÉS: az építés nem ír fájlt.', file=sys.stderr)
        for s in sertesek:
            print(s.sor_szoveg(), file=sys.stderr)
        return 1

    t0 = time.time()
    ep = Epito(args.gyoker, kimenet, args.mod)
    try:
        ep.epit()
    except Exception as exc:
        print('HIBA (építés): %r' % (exc,), file=sys.stderr)
        raise
    ido = time.time() - t0
    hashek = tablak_hash(kimenet)
    con = sqlite3.connect(kimenet)
    for n, (db, h) in hashek.items():
        con.execute('INSERT INTO meta VALUES (?,?,?,?,?)', ('hash:' + n, '%d|%s' % (db, h),
                    'projekt_adat', 'tisztazatlan', 'projekt_adat'))
    con.commit()
    con.close()
    proba = probak(kimenet, args.gyoker) if args.proba else None
    meret = os.path.getsize(kimenet)
    if args.naplo:
        nev = 'SQLITE_EPIT_meres_minta.md' if args.mod == 'minta' else 'SQLITE_EPIT_meres.md'
        irj(os.path.join(args.gyoker, 'naplok', nev), meres_md(ep, hashek, ido, meret, args.mod, proba, licenc_helyfoglalas(kimenet)))
    print('kész: %s (%.1f MB, %.1f s, %d tábla)' % (kimenet, meret / 1048576.0, ido, len(hashek)))
    if proba is not None:
        for p in proba:
            print('%2d. pont: %s' % (p['pont'], 'MEGEGYEZIK' if p['ok'] else 'ELTÉRÉS'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
