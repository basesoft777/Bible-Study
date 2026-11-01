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
  4. Licenc (F89, DT113): TABLASZINTU, a `tabla_licenc(tabla, licenc_allapot, kereskedelmi,
     licenc_dataset, cimke)` tablaban (az `adat/licencek.tsv`-bol); az adattablak soraiban
     nincs licenc-oszlop. Minden epitett tablanak pontosan egy `tabla_licenc`-sora van.
     Alapertek nincs: licencsor nelkuli tabla kimarad, es a jelentesben all. Szarmaztatott
     tabla licence a forrasaie kozul a legszigorubb (DT109 (2c)). A `cimke` a licencsorok
     `cimke` ertekei (tobb forrasnal `; `-vel), hogy egy zart csomag (#86) a CC BY-SA es az
     MCGED tablakat szurni tudja.

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
import general as G
import nave_bontas as NB  # noqa: E402
import zsolt_felirat_halmaz as ZFH  # noqa: E402
import ellenoriz as E  # noqa: E402
import tsk_kulcs as TK  # noqa: E402
from strong_util import strong_normalizal  # noqa: E402


_TIPNR_UTOTAG_RE = re.compile(r'^(.*\d)([A-Za-z])$')


def tipnr_strong_szetvalaszt(nyers):
    """F88 (DT111): a TIPNR `Strong-szám` mezőjének szétválasztása -> (alapszám, utótag).

    A TIPNR a Strong-számhoz egyértelműsítő betűutótagot fűz (`G2424G` Jézus, `G2424H`
    Barabbás, `H3063N` Júdea; a nagybetű személyt/entitást különböztet meg egy lexémán
    belül, a kisbetű, pl. `H5838z`, ugyanígy). A `pardes.db` TIPNR-betöltőjének
    kifejezett szabálya: a `strong` oszlop az alapszámot (SEMA 1.2 alak) hordozza, az
    utótag az `utotag` oszlopba kerül, a teljes érték a `strong_nyers`-ben marad.
    Utótag nélküli értékre az utótag üres szöveg. Nem értelmezhető értékre ValueError
    (a hívó a normalizálási jelentésbe teszi). A `strong_util.strong_normalizal()`
    alapértéke (`utotag='tilt'`) NEM változik: máshol az utótag hibát jelezhet.
    """
    if isinstance(nyers, str) and '+' not in nyers:
        m = _TIPNR_UTOTAG_RE.match(nyers.strip())
        if m:
            return strong_normalizal(m.group(1)), m.group(2)
    return strong_normalizal(nyers), ''

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
    # F89 (DT-F89a): a Karoli-Strong tablak sajat licencsora van (minden jog fenntartva; a
    # forrasaik, Karoli 1908 es TAHOT/TAGNT, a sor megjegyzeseben es a komponens-sorokban)
    'token_par': ['Karoli_Strong_parok'],
    'token_karoli': ['Karoli_Strong_szavak'],
    'frazis_pozicio': ['Karoli_Strong_parok'],
    'karoli_variancia': ['karoli_variancia'],
    'token_eredeti': ['TAHOT', 'TAGNT'],
    'token_strong': ['TAHOT', 'TAGNT'],
    'strong_parok': ['TAHOT', 'TAGNT', 'projekt_adat'],
    'vers': ['Karoli_1908'],
    'vers_szamozas': ['Karoli_versmegfeleltetes', 'BSB_Strongs'],
    'konyv': ['Konyv_nevtablak'],
    'tsk': ['TSK'], 'kh': ['Karoli_KH'], 'tipnr': ['TIPNR'], 'bsb': ['BSB_Strongs'],
    'kjv': ['KJV_Strongs_teljes'], 'karoli_strong_kivonat': ['Karoli_Strong_kivonat'],
    'tbesg': ['TBESG'], 'tbesh': ['TBESH'],
    'lxx_bridge': ['lxx_bridge'], 'lxx_versszintu_parok': ['LXX_versszintu_parok'],
    'igehely_tartomany': ['projekt_adat'], 'normalizalas_jelentes': ['projekt_adat'],
    'meta': ['projekt_adat'], 'fts_motivum': ['projekt_adat'],
    'oshl_bdb_igehelyek': ['OSHL_BDB'], 'oshl_lexikalis_index': ['OSHL'],
    # F92 (DT-F92a): az olvasoi lapok hiany-tablai
    'token_macula': ['Macula_heber'],
    'lxx_token': ['LXX_OS'],
    'lxx_versszam': ['LXX_OS', 'Versifikacios_tablak', 'Karoli_versmegfeleltetes'],
    'bdb_alias': ['BDB', 'projekt_adat'],
    'nave_vers': ['Nave_basokant', 'Karoli_versmegfeleltetes', 'LXX_OS'],
    # F95 (DT-F95a): a szotari alak tablai (a #94 kimenete); a kotojeles segedtabla a token_karoli-bol is szarmazik
    'szotari_alak': ['szoto_tablak'], 'szotari_kereso': ['szoto_tablak'],
    'szotari_token_kotojeles': ['szoto_tablak', 'Karoli_Strong_szavak'],
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

# Tovabbi indexek az altalanos tablakon (oszlopnev a TSV-fejlec azonosito-alakjaban). F99 M1: a gyokcsalad
# (etym_cel -> oshl_id) feloldasa a szo-lapon oshl_id-n keres.
ALTALANOS_TOVABBI_INDEX = {'oshl_lexikalis_index': ['oshl_id']}

# adat/ tabla, amelynek SAJAT licencek.tsv-sora van (nem projekt_adat); a tobbi adat/ tabla projekt_adat
ADAT_LICENC = {'morf_kulcs_heber': ['morf_kulcs_heber'], 'morf_nyelv_aramai': ['morf_nyelv_aramai'],
               # F99: a BDB-szeletelő táblái a BDB szövegéből (horgony, nyers hivatkozás) és a Macula MT → Károli
               # megfeleltetéséből is származnak: a legszigorúbb érték érvényes (licenc_feloldas). ELLENOR_F99 6.: a `bdb_id` oszlop
               # OSHL-adat (CC BY 4.0), a TAHOT (CC BY 4.0) a szűrésben (DT-F99k) és a Károli-kulcsban (DT-F99h) dönt
               'bdb_aranyminta': ['BDB', 'projekt_adat'], 'bdb_vers_jelentes': ['BDB', 'Macula_heber', 'OSHL', 'TAHOT', 'projekt_adat'],
               # F140 (K8, DT-F140b): a magyar glosszák a TBESH-glosszák fordításai (CC BY 4.0, forrásjelölés kötelező); a `fo` sor
               # kiválasztásában a TAHOT „Rövid jelentés” oszlopának többségi értéke dönt (szöveg nem kerül át), ezért a TAHOT
               # is a listán van (F99-precedens); a fordítás maga projekt_adat
               'glosszak_heber_hu': ['TBESH', 'TAHOT', 'projekt_adat']}

ADAT_KIHAGYOTT = {'karoli_variancia'}  # külön kezelve (szarmaztatott licenc)

STRONG_RE = re.compile(r'^[HG]\d{4,5}$')
HU_IGEHELY_RE = re.compile(r'^(\S+) (\d+):(\d+)[a-z]?(?:-(?:(\d+):)?(\d+)[a-z]?)?$')
STEP_IGEHELY_RE = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)[a-z]?$')

SZIGOR_ALLAPOT = {'tisztazatlan': 0, 'tisztazott': 1, 'kozkincs': 2}
SZIGOR_KERESKEDELMI = {'nem': 0, 'tisztazatlan': 1, 'feltetelesen': 2, 'igen': 3}


class LicencHiany(Exception):
    pass


class VersmegfKeziMt(Exception):
    """F117.5 (DT-F117f (a)): a versmegfeleltető táblában KEZI osztályú sor kitöltött igehely_mt-vel áll."""
    pass


def kezi_mt_or(vm_sorok):
    """F117.5 őr (DT-F117f (a), N-F117a): a `_bsb_szamozas` az igehely_mt-t úgy olvassa, mintha a kitöltött érték a
    Károli-szám volna (MT osztály), és máshol azonosságot vesz; a DT-F117e (c) óta a KEZI osztályú sor kitöltött
    igehely_mt-je a valódi MT-szám (Károli ≠ KJV és ≠ MT), ezért a leképezés ütközne (mért: 6 Károli-vers két
    BSB MT-versen). A javításig (N-F117a) az építés itt érthető hibával leáll; nem kerülhető meg."""
    hibas = [r['igehely_karoli'] for r in vm_sorok
             if (r.get('osztaly') or '').strip() == 'KEZI' and (r.get('igehely_mt') or '').strip()]
    if hibas:
        raise VersmegfKeziMt(
            'a konkordancia/Karoli_versmegfeleltetes.tsv %d KEZI osztályú sora kitöltött igehely_mt-t hordoz '
            '(pl. %s); a sqlite_epit BSB-számozása (_bsb_szamozas) ezt még nem kezeli: az építés leáll. '
            'Javítás: NYITOTT_FELADATOK.md N-F117a (DT-F117f (a)).' % (len(hibas), ', '.join(hibas[:5])))


def szo_kis(s):
    """F92 (v1.1): a magyar szo kisbetus, normalizalt alakja a kereshetosegre: NFC, kisbetu, minden
    nem-betu/szamjegy karakter (Karoli-irasjel, kotojel, aposztrof) nelkul. A kereso oldalon
    ugyanez a fuggveny (vagy azonos szabaly) alkalmazando."""
    s = unicodedata.normalize('NFC', s or '').lower()
    return re.sub(r'[\W_]+', '', s)


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
    jeloltek_fejlec, jeloltek = G.tsv_beolvas(os.path.join(adat_dir, 'jeloltek.tsv'))
    kapcsolatok = be('kapcsolatok.tsv')
    datasetek = be('datasetek.tsv')
    auditok = be('auditok.tsv')
    lexikon_hivatkozasok = be('lexikon_hivatkozasok.tsv')
    id_halmaz = {m['id'] for m in motivumok}
    sorok = [
        E.szabaly1_hivatkozasi_epseg(id_halmaz, elofordulasok, kapcsolatok, jeloltek, auditok),
        E.szabaly2_nincs_kozvetlen_ut(elofordulasok, jeloltek),
        E.szabaly2b_motivumkozi(id_halmaz, jeloltek, jeloltek_fejlec, adat_dir),  # DT-F127b
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
        E.szabaly15_kapcsolatok_fejlec(adat_dir),   # #11 S2: az `indoklas` oszlop (SEMA 2.3)
        E.szabaly16_elofordulasok_fejlec(adat_dir),   # #11 S2 (DT250): a `forras_tanulmany` oszlop (SEMA 2.2)
    ]
    sertesek = [s for s in sorok if s.verdict.split(' ', 1)[0] == 'SÉRTÉS']
    return sorok, sertesek


def integritas_md(sorok, adat_dir, mod):
    ki = ['# SQLITE_EPIT -- integritás-ellenőrzés (F79)', '',
          '*Proveniencia: `scope=manual | forras=%s | ts=%s`; az ellenőrzés a betöltés ELŐTT, '
          'a TSV-sorlistákon fut, az `eszkozok/ellenoriz.py` függvényeivel (DT109 (3), (7)); '
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
        self.tabla_lic = {}       # tabla -> (licenc_allapot, kereskedelmi, licenc_dataset, cimke)
        self.tablak = {}          # nev -> sorszam
        self.kihagyott = []       # (tabla, ok)
        self.norm_jelentes = {}   # (tabla, nyers, ok) -> darab
        self.megjegyzesek = []
        self.olvasoi_meta = []   # F92: (kulcs, ertek) meta-sorok az olvasoi tablakhoz
        self.ot_versek = set()   # F92: a TAHOT-ban heber tokent hordozo Karoli-versek (minta modban is teljes)
        self.token_strong_halmaz = set()   # minden TAHOT/TAGNT-ból kinyert alapszám (minta módban is teljes)

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
        cimkek = []
        for k in kulcsok:
            cim = self.licencek[k].get('cimke', '')
            if not cim:
                raise LicencHiany('üres cimke: %s' % k)
            if cim not in cimkek:
                cimkek.append(cim)
        return a, c, '+'.join(kulcsok), '; '.join(cimkek)

    def jelent_norm(self, tabla, nyers, ok):
        k = (tabla, nyers, ok)
        self.norm_jelentes[k] = self.norm_jelentes.get(k, 0) + 1

    # -- tabla-letrehozas -------------------------------------------------
    def tabla(self, nev, oszlopok, sorok, lic, indexek=()):
        """oszlopok: [(nev, tipus)]; sorok: iteralhato tuple-ok. Licenc nelkul nem epul.
        A licenc tablaszintu (F89, DT113): a `tabla_licenc` egy sora, nem sor-oszlop."""
        try:
            lic_ertek = self.licenc_feloldas(lic)
        except LicencHiany as exc:
            self.kihagyott.append((nev, str(exc)))
            return False
        cols = list(oszlopok)
        self.con.execute('CREATE TABLE "%s" (%s)' % (nev, ', '.join(
            '"%s" %s' % (n, t) for n, t in cols)))
        ph = ','.join('?' * len(cols))
        n = 0

        def gen():
            nonlocal n
            for s in sorok:
                n += 1
                yield tuple(s)
        self.con.executemany('INSERT INTO "%s" VALUES (%s)' % (nev, ph), gen())
        for i, ix in enumerate(indexek):
            self.con.execute('CREATE INDEX "ix_%s_%d" ON "%s" (%s)' % (nev, i, nev, ix))
        self.tablak[nev] = n
        self.tabla_lic[nev] = lic_ertek
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
        self._szotari_alak()
        self._kereszthivatkozasok()
        self._bsb_szamozas()
        self._kjv()
        self._karoli_strong_kivonat()
        self._tbes()
        self._altalanos()
        self._adat_tablak()
        self._olvasoi_tablak()
        self._tartomanyok()
        self._fts()
        self._jelentes_tabla()
        self._meta()
        self._tabla_licenc()

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
                if nev == 'jeloltek.tsv' and not G.jelolt_elofordulas_e(r):
                    continue  # DT-F127b: csak előfordulás-jelölt
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
                if ig not in self.vi.halmaz:   # tokenenként: az előfordulás-szám a valós tokenszám
                    self.jelent_norm(fajl, ig, 'nincs ilyen Károli-vers (token_eredeti.van_vers=0)')
                szamlalo[ig] = szamlalo.get(ig, 0) + 1
                if nyelv == 'H' and ig in self.vi.halmaz:
                    self.ot_versek.add(ig)
                try:
                    lanc = strong_normalizal(r['Strong-szám'])
                except ValueError:
                    self.jelent_norm(fajl, r['Strong-szám'], 'Strong-szám nem normalizálható')
                    lanc = None
                elemek = lanc.split('+') if lanc else []
                self.token_strong_halmaz.update(elemek)
                for s in elemek:
                    if s in grammatikai or ('H9001' <= s <= 'H9049'):
                        continue
                    vers_strongok.setdefault(ig, set()).add(s)
                if not self._benne(ig):
                    continue
                n = szamlalo[ig]
                tokenek.append((ig, n, nyelv, lanc, r['Strong-szám'], r['Ragozott alak'],
                                r['Kiejtés'], r['Szótő'], r['Rövid jelentés'],
                                r['Angol tükörfordítás'], r.get('Kritikai kiadás', ''), fajl, 1 if ig in self.vi.halmaz else 0))
                for s in elemek:
                    strongok.append((ig, n, s))
        self.tabla('token_eredeti',
                   [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('nyelv', 'TEXT'),
                    ('strong_lanc', 'TEXT'), ('strong_nyers', 'TEXT'), ('alak', 'TEXT'),
                    ('kiejtes', 'TEXT'), ('szoto', 'TEXT'), ('rovid_jelentes', 'TEXT'),
                    ('angol_tukorford', 'TEXT'), ('kritikai_kiadas', 'TEXT'), ('forras_fajl', 'TEXT'),
                    ('van_vers', 'INTEGER')],
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
                             r['er_szo'], r['strong'], r['bizonyossag'], r['forras'], szo_kis(r['hu_szo'])))
                poz.add((r['vers'], 'hu', int(r['hu_sorszam']), r['strong'], r['hu_szo']))
                poz.add((r['vers'], 'er', int(r['er_sorszam']), r['strong'], r['er_szo']))
        for f in sorted(glob.glob(os.path.join(self.adat, 'karoli_strong', 'szavak_*.tsv'))):
            for r in G.tsv_beolvas(f)[1]:
                if not self._benne(r['vers']):
                    continue
                szav.append((r['vers'], r['oldal'], int(r['sorszam']), r['szo'], r['allapot'],
                             r['partner_sorszam'], r['strong'], r['bizonyossag'], r['forras'], szo_kis(r['szo'])))
        lic = SZARMAZTATOTT_LICENC['token_par']
        self.tabla('token_par', [('igehely', 'TEXT'), ('hu_sorszam', 'INTEGER'), ('hu_szo', 'TEXT'),
                                 ('er_sorszam', 'INTEGER'), ('er_szo', 'TEXT'), ('strong', 'TEXT'),
                                 ('bizonyossag', 'TEXT'), ('forras', 'TEXT'), ('hu_szo_kis', 'TEXT')],
                   pare, lic, ['strong', 'hu_szo', 'igehely, hu_sorszam', 'hu_szo_kis'])
        self.tabla('token_karoli', [('igehely', 'TEXT'), ('oldal', 'TEXT'), ('sorszam', 'INTEGER'),
                                    ('szo', 'TEXT'), ('allapot', 'TEXT'), ('partner_sorszam', 'TEXT'),
                                    ('strong', 'TEXT'), ('bizonyossag', 'TEXT'), ('forras', 'TEXT'),
                                    ('szo_kis', 'TEXT')],
                   szav, SZARMAZTATOTT_LICENC['token_karoli'],
                   ['igehely, oldal, sorszam', 'strong', 'szo_kis, igehely, oldal, sorszam'])
        self.tabla('frazis_pozicio', [('igehely', 'TEXT'), ('oldal', 'TEXT'), ('sorszam', 'INTEGER'),
                                      ('strong', 'TEXT'), ('szo', 'TEXT')],
                   sorted(poz), SZARMAZTATOTT_LICENC['frazis_pozicio'],
                   ['igehely, oldal, sorszam', 'strong'])

    # -- F95: szotari alak (DT-F95a) -------------------------------------------------------------
    def _szotari_alak(self):
        """A #94 kimenete (adat/szoto/karoli_szotari_alak.tsv, generalt) a pardes.db-be: szotari_alak
        (alakszintu, kulcs: alak), szotari_kereso (NFC kisbetus keresoalak -> alak, mezok), a
        szotari_token_kotojeles segedtabla (a token_karoli altal szetvagott kotojeles alakok darabjai) es
        a token_karoli reszleges indexe a pontos-alak kapcsolasra. A `szoto/` alkonyvtarat az
        _adat_tablak nem olvassa, ezert sajat metodus."""
        lic = SZARMAZTATOTT_LICENC['szotari_alak']
        if not self.licenc_ellenorzes('szotari_alak', lic):
            return
        fej, sorok = G.tsv_beolvas(os.path.join(self.adat, 'szoto', 'karoli_szotari_alak.tsv'))
        oszl = ['alak', 'szotari_alak', 'szotari_alak_mai', 'alapige', 'tovabbi_elfogadhato', 'modszer',
                'szabaly_forras', 'regies_jegy']
        assert fej == oszl, fej
        self.tabla('szotari_alak', [(o, 'TEXT') for o in oszl], (tuple(r[o] for o in oszl) for r in sorok),
                   lic, ['szotari_alak'])
        self.con.execute('CREATE UNIQUE INDEX "ux_szotari_alak_alak" ON "szotari_alak" (alak)')
        # kereso: (NFC kisbetus keresoalak, alak) -> melyik mezo(k)bol szarmazik
        sorrend = ('szotari', 'mai', 'alapige', 'tovabbi')
        kereso = {}
        for r in sorok:
            ertekek = [('szotari', r['szotari_alak']), ('mai', r['szotari_alak_mai']), ('alapige', r['alapige'])]
            if r['tovabbi_elfogadhato']:
                ertekek += [('tovabbi', t) for t in r['tovabbi_elfogadhato'].split('|')]
            for mezo, ertek in ertekek:
                if ertek:
                    kereso.setdefault((unicodedata.normalize('NFC', ertek).lower(), r['alak']), set()).add(mezo)
        self.tabla('szotari_kereso', [('keresoalak', 'TEXT'), ('alak', 'TEXT'), ('mezok', 'TEXT')],
                   ((k, a, ','.join(m for m in sorrend if m in ms)) for (k, a), ms in sorted(kereso.items())),
                   SZARMAZTATOTT_LICENC['szotari_kereso'], ['keresoalak, alak'])
        self.olvasoi_meta.append(('szotari_alak:forras_sor', str(len(sorok))))
        if 'token_karoli' not in self.tablak:
            return
        self.con.execute('CREATE INDEX "ix_token_karoli_szo_hu" ON "token_karoli" (szo, igehely, sorszam) '
                         "WHERE oldal='hu'")
        alakok = {r['alak'] for r in sorok}
        kotojeles = {a for a in alakok if '-' in a}
        versek = {}
        for f in sorted(glob.glob(os.path.join(self.adat, 'karoli_strong', 'szavak_*.tsv'))):
            for r in G.tsv_beolvas(f)[1]:
                if r['oldal'] == 'hu' and self._benne(r['vers']):
                    versek.setdefault(r['vers'], []).append((int(r['sorszam']), r['szo']))
        darabok, hu_db, nem_talal = set(), 0, 0
        for ig, toks in versek.items():
            toks.sort()
            hu_db += len(toks)
            nem_talal += sum(1 for _, sz in toks if sz not in alakok)
            for k in (3, 2):
                for st in range(0, len(toks) - k + 1):
                    ablak = toks[st:st + k]
                    alak = '-'.join(sz for _, sz in ablak)
                    if alak in kotojeles:
                        for n, sz in ablak:
                            darabok.add((ig, n, alak, 1 if sz in alakok else 0))
        tok_kulcs = {(ig, n) for ig, n, _, _ in darabok}
        feloldott = {(ig, n) for ig, n, _, p in darabok if not p}
        self.tabla('szotari_token_kotojeles', [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('alak', 'TEXT'),
                                               ('pontos_talalat', 'INTEGER')],
                   sorted(darabok), SZARMAZTATOTT_LICENC['szotari_token_kotojeles'],
                   ['igehely, sorszam', 'alak'])
        self.olvasoi_meta += [
            ('szotari_token:hu_token', str(hu_db)),
            ('szotari_token:pontos_alak_nem_talal', str(nem_talal)),
            ('szotari_token:kotojeles_darab_token', str(len(tok_kulcs))),
            ('szotari_token:kotojeles_feloldott_nem_pontos', str(len(feloldott))),
            ('szotari_token:nem_oldodik_fel', str(nem_talal - len(feloldott))),
        ]

    # -- TSK, Karoli-KH, TIPNR ---------------------------------------------------
    def _kereszthivatkozasok(self):
        tsk = []
        # F114: a TSK KJV-kulcsú; forrás és cél a tsk_kulcs átváltón át Károli-versszámra váltva
        tsk_nyers = G.tsv_beolvas(os.path.join(self.konk, 'TSK_kereszthivatkozasok.tsv'))[1]
        if self.minta is None:
            tsk_karoli = TK.karoli_sorok(tsk_nyers)
        else:
            tsk_karoli = TK.forras_sorok(tsk_nyers, self.minta)
        for r in tsk_karoli:
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
                s, utotag = tipnr_strong_szetvalaszt(r['Strong-szám'])   # F88, DT111
            except ValueError:
                self.jelent_norm('tipnr', r['Strong-szám'], 'Strong-szám nem normalizálható')
                s, utotag = None, None
            if s is not None and s not in self.token_strong_halmaz and utotag:
                # jelölés, nem javítás: a levágott alapszám a token_strong-ban nem szerepel
                self.jelent_norm('tipnr', s, 'levágott alapszám nincs a token_strong-ban')
            tip.append((r['Név (normalizált)'], r['Névváltozat'], s, utotag, r['Strong-szám'], r['Nyelv'], ig, r['Igehely']))
        self.tabla('tipnr', [('nev', 'TEXT'), ('nevvaltozat', 'TEXT'), ('strong', 'TEXT'), ('utotag', 'TEXT'),
                             ('strong_nyers', 'TEXT'), ('nyelv', 'TEXT'), ('igehely', 'TEXT'), ('step_nyers', 'TEXT')],
                   tip, SZARMAZTATOTT_LICENC['tipnr'], ['igehely', 'strong'])

    # -- BSB + szamozas ------------------------------------------------------------
    def _bsb_szamozas(self):
        vm = G.tsv_beolvas(os.path.join(self.konk, 'Karoli_versmegfeleltetes.tsv'))[1]
        kezi_mt_or(vm)   # F117.5 őr (DT-F117f (a)): KEZI + kitöltött igehely_mt -> leáll (N-F117a)
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
                        r['Angol szó állapota'], sz, r['Igehely'], mod, r['Szósorszám']))
        self.tabla('bsb', [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('strong', 'TEXT'),
                           ('angol_szo', 'TEXT'), ('morf', 'TEXT'), ('angol_szo_allapot', 'TEXT'),
                           ('szamozas', 'TEXT'), ('step_nyers', 'TEXT'), ('kk_leképezés', 'TEXT'),
                           ('szosorszam_nyers', 'TEXT')],
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

    # -- KJV, Karoli_Strong_kivonat, TBESG/TBESH (DT-F79a M0 sema-terv) ---------------------
    def _kjv(self):
        if not self.licenc_ellenorzes('kjv', SZARMAZTATOTT_LICENC['kjv']):
            return
        vm = G.tsv_beolvas(os.path.join(self.konk, 'Karoli_versmegfeleltetes.tsv'))[1]
        kjv_kk = {}
        for r in vm:
            if r['igehely_kjv']:
                p = hu_igehely_parse(r['igehely_karoli'])
                if p:
                    kjv_kk[(p[0], r['igehely_kjv'])] = r['igehely_karoli']
        ki, szamlalo = [], {}
        for r in G.tsv_beolvas(os.path.join(self.konk, 'KJV_Strongs_teljes.tsv'))[1]:
            m = STEP_IGEHELY_RE.match(r['Igehely'])
            konyv = self.konyvek.step_hu.get(m.group(1)) if m else None
            if konyv is None:
                self.jelent_norm('kjv', r['Igehely'], 'nem leképezhető')
                continue
            kulcs = '%d:%d' % (int(m.group(2)), int(m.group(3)))
            if (konyv, kulcs) in kjv_kk:
                kk, mod = kjv_kk[(konyv, kulcs)], 'kjv_tabla'
            else:
                kk, mod = '%s %s' % (konyv, kulcs), 'azonos_feltetelezett'
            if kk not in self.vi.halmaz:
                self.jelent_norm('kjv', kk, 'nincs ilyen Károli-vers')
                continue
            if not self._benne(kk):
                continue
            szamlalo[kk] = szamlalo.get(kk, 0) + 1
            try:
                s = strong_normalizal(r['Strong-szám'])
            except ValueError:
                s = None
                self.jelent_norm('kjv', r['Strong-szám'], 'Strong-szám nem normalizálható')
            ki.append((kk, szamlalo[kk], s, r['Strong-szám'], r['Angol szó'], r['Morfológiai kód'],
                       r['Igehely'], mod, r['Szósorszám']))
        self.tabla('kjv', [('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('strong', 'TEXT'),
                           ('strong_nyers', 'TEXT'), ('angol_szo', 'TEXT'), ('morf', 'TEXT'),
                           ('step_nyers', 'TEXT'), ('kk_leképezés', 'TEXT'), ('szosorszam_nyers', 'TEXT')],
                   ki, SZARMAZTATOTT_LICENC['kjv'], ['igehely, sorszam', 'strong'])

    def _karoli_strong_kivonat(self):
        if not self.licenc_ellenorzes('karoli_strong_kivonat', SZARMAZTATOTT_LICENC['karoli_strong_kivonat']):
            return
        ki = []
        for r in G.tsv_beolvas(os.path.join(self.konk, 'Karoli_Strong_kivonat.tsv'))[1]:
            ig = self.konyvek.step_igehely(r['Igehely'])
            if ig is None:
                self.jelent_norm('karoli_strong_kivonat', r['Igehely'], 'nem leképezhető')
            elif ig not in self.vi.halmaz:
                self.jelent_norm('karoli_strong_kivonat', ig, 'nincs ilyen Károli-vers')
            if self.minta is not None and (ig is None or ig not in self.minta):
                continue
            try:
                st = strong_normalizal(r['Strong-szám'])
            except ValueError:
                st = None
                self.jelent_norm('karoli_strong_kivonat', r['Strong-szám'], 'Strong-szám nem normalizálható')
            ki.append((ig, r['Igehely'], st, r['Strong-szám'], r['Károli-szó'], r['Azonosítás módja'],
                       r['Forrás-tanulmány'], r['Megbízhatóság'], r['Szófaj'], r['Gyök/Származtatás']))
        self.tabla('karoli_strong_kivonat',
                   [('igehely', 'TEXT'), ('step_nyers', 'TEXT'), ('strong', 'TEXT'), ('strong_nyers', 'TEXT'),
                    ('karoli_szo', 'TEXT'), ('azonositas_modja', 'TEXT'), ('forras_tanulmany', 'TEXT'),
                    ('megbizhatosag', 'TEXT'), ('szofaj', 'TEXT'), ('gyok_szarmaztatas', 'TEXT')],
                   ki, SZARMAZTATOTT_LICENC['karoli_strong_kivonat'], ['igehely', 'strong'])

    def _tbes(self):
        for nev, fajl in (('tbesg', 'TBESG.txt'), ('tbesh', 'TBESH.txt')):
            if not self.licenc_ellenorzes(nev, SZARMAZTATOTT_LICENC[nev]):
                continue
            with open(os.path.join(self.konk, fajl), encoding='utf-8-sig', newline='') as f:
                sorok = f.read().split('\n')
            sorok = [x.rstrip('\r') for x in sorok]
            fej = next(i for i, x in enumerate(sorok) if len(x.split('\t')) == 8 and x.startswith('eStrong'))
            ki = []
            for x in sorok[fej + 1:]:
                if not x.strip() or x.startswith('==='):
                    continue
                mezok = x.split('\t')
                if len(mezok) != 8:
                    self.jelent_norm(nev, x[:40], 'nem 8 mezős sor (az adat-szakaszban)')
                    continue
                try:
                    st = strong_normalizal(mezok[0], utotag='megtart')
                except ValueError:
                    st = None
                    self.jelent_norm(nev, mezok[0], 'Strong-szám nem normalizálható')
                ki.append((st, mezok[0], mezok[1], mezok[2], mezok[3], mezok[4], mezok[5], mezok[6], mezok[7]))
            self.tabla(nev, [('strong', 'TEXT'), ('estrong_nyers', 'TEXT'), ('dstrong', 'TEXT'),
                             ('ustrong', 'TEXT'), ('szo', 'TEXT'), ('atiras', 'TEXT'), ('morf', 'TEXT'),
                             ('gloss', 'TEXT'), ('jelentes', 'TEXT')],
                       ki, SZARMAZTATOTT_LICENC[nev], ['strong'])

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
        ix += [o for o in ALTALANOS_TOVABBI_INDEX.get(nev, []) if o in nevek]
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
            self._altalanos_betolt(nev, 'adat/%s.tsv' % nev, None, None, ADAT_LICENC.get(nev, ['projekt_adat']))
        # karoli_variancia: szarmaztatott licenc, csak teljes modban (42 ezer sor)
        if self.mod == 'teljes':
            self._altalanos_betolt('karoli_variancia', 'adat/karoli_variancia.tsv', None, None,
                                   SZARMAZTATOTT_LICENC['karoli_variancia'])

    # -- F92: az olvasoi lapok hiany-tablai (DT-F92a) ----------------------------------------
    def _lxx_os_fajlok(self):
        """A LXX_OS konyvfajlok (`szoalak` oszlop) sorai fajlsorrendben; a 2 nem-konyv fajl
        (karoli_fejezet_dontes.tsv, karoli_vers_felulbiralas.tsv) kimarad. Minden sor `_fajl` kulcsa a
        fajl neve kiterjesztes nelkul: ez a szovegforma (ellenor UJ-1: a Dan, Bir, Jozs parhuzamos
        LXX-szovegformai -- daniel / daniel-theodotion, judges / judges-vaticanus-b, joshua /
        joshua-vaticanus-b -- ugyanarra a Karoli-versre esnek, es nem fesulhetnek ossze)."""
        for f in sorted(glob.glob(os.path.join(self.konk, 'LXX_OS', '*.tsv'))):
            fej, sorok = G.tsv_beolvas(f)
            if 'szoalak' not in fej:
                continue
            forma = os.path.splitext(os.path.basename(f))[0]
            for r in sorok:
                r['_fajl'] = forma
                yield r

    def _olvasoi_tablak(self):
        meta = self.olvasoi_meta
        # -- token_macula
        if self.licenc_ellenorzes('token_macula', SZARMAZTATOTT_LICENC['token_macula']):
            sorok, szam, db_nyers = [], {}, 0
            for f in sorted(glob.glob(os.path.join(self.konk, 'Macula_heber_*.tsv'))):
                for r in G.tsv_beolvas(f)[1]:
                    db_nyers += 1
                    ig = r['karoli']
                    if ig and ig not in self.vi.halmaz:
                        self.jelent_norm('token_macula', ig, 'nincs ilyen Károli-vers')
                    try:
                        st = strong_normalizal(r['strong']) if r['strong'] else None
                    except ValueError:
                        st = None
                        self.jelent_norm('token_macula', r['strong'], 'Strong-szám nem normalizálható')
                    try:
                        lst = strong_normalizal(r['gorog_strong']) if r['gorog_strong'] else None
                    except ValueError:
                        lst = None
                        self.jelent_norm('token_macula', r['gorog_strong'], 'görög Strong-szám nem normalizálható')
                    m = re.search(r'!(\d+)$', r['ref'])
                    poz = None
                    if st and ig:
                        szam[(ig, st)] = szam.get((ig, st), 0) + 1
                        poz = szam[(ig, st)]
                    sorok.append([r['xml_id'], ig, int(m.group(1)) if m else None, r['kk_mod'], r['allapot'],
                                  r['szo'], r['lemma'], st, r['strong'], poz, None, r['morf'], r['szofaj'],
                                  r['gloss'], r['gorog_lxx'], lst, r['gorog_lxx_forras'], r['gorog_lxx_rahlfs']])
            # kétértelmű vers+Strong illesztés (DT-F92a 6.): ugyanaz a Strong egy versben többször
            ketert_csoport = sum(1 for v in szam.values() if v > 1)
            ketert_token = sum(v for v in szam.values() if v > 1)
            for x in sorok:
                if x[7] and x[1]:
                    x[10] = szam[(x[1], x[7])]
            if self.minta is not None:
                sorok = [x for x in sorok if x[1] in self.minta]
            self.tabla('token_macula',
                       [('xml_id', 'TEXT'), ('igehely', 'TEXT'), ('sorszam', 'INTEGER'), ('kk_mod', 'TEXT'),
                        ('allapot', 'TEXT'), ('szo', 'TEXT'), ('lemma', 'TEXT'), ('strong', 'TEXT'),
                        ('strong_nyers', 'TEXT'), ('strong_poz', 'INTEGER'), ('strong_n', 'INTEGER'),
                        ('morf', 'TEXT'), ('szofaj', 'TEXT'), ('gloss', 'TEXT'), ('lxx_szo', 'TEXT'),
                        ('lxx_strong', 'TEXT'), ('lxx_szo_forras', 'TEXT'), ('lxx_szo_rahlfs', 'TEXT')],
                       sorok, SZARMAZTATOTT_LICENC['token_macula'], ['igehely, sorszam', 'strong', 'xml_id'])
            meta.append(('token_macula:forras_sor', str(db_nyers)))
            # F115 / DT-F115a: a gorog_lxx chi<->xi javitasanak Rahlfs-minosegjelolese (osztalyonkent darab; a minta-epiteskor a mintara)
            rahlfs_db = {}
            for x in sorok:
                if x[17]:
                    rahlfs_db[x[17]] = rahlfs_db.get(x[17], 0) + 1
            for k in sorted(rahlfs_db):
                meta.append(('token_macula:lxx_szo_rahlfs:%s' % k, str(rahlfs_db[k])))
            meta.append(('token_macula:ketertelmu_vers_strong_csoport', str(ketert_csoport)))
            meta.append(('token_macula:ketertelmu_vers_strong_token', str(ketert_token)))
            self.norm_jelentes[('token_macula', 'azonos Strong egy versben többször',
                                'kétértelmű vers+Strong illesztés (csoport; feloldás: strong_poz = pozíció-sorrend)')] = ketert_csoport
        # -- lxx_token, lxx_versszam: a LXX_OS egyszer olvasva
        os_sorok = list(self._lxx_os_fajlok())
        if self.licenc_ellenorzes('lxx_token', SZARMAZTATOTT_LICENC['lxx_token']):
            ki = []
            for r in os_sorok:
                ig = r['igehely_karoli']
                if ig and ig not in self.vi.halmaz:
                    self.jelent_norm('lxx_token', ig, 'nincs ilyen Károli-vers')
                if self.minta is not None and ig not in self.minta:
                    continue
                st = ('G%04d' % int(r['strong'])) if r['strong'].isdigit() else None
                ki.append((r['igehely_lxx'], r['igehely_kjv'], ig, r['karoli_ok'],
                           int(r['pozicio']) if r['pozicio'].isdigit() else None,
                           r['szoalak'], r['lemma'], r['morf'], st, r['strong_ok'], r['_fajl']))
            self.tabla('lxx_token',
                       [('lxx_igehely', 'TEXT'), ('kjv_vers', 'TEXT'), ('karoli_igehely', 'TEXT'),
                        ('karoli_ok', 'TEXT'), ('pozicio', 'INTEGER'), ('szoalak', 'TEXT'), ('lemma', 'TEXT'),
                        ('morf', 'TEXT'), ('strong', 'TEXT'), ('strong_ok', 'TEXT'), ('szovegforma', 'TEXT')],
                       ki, SZARMAZTATOTT_LICENC['lxx_token'],
                       ['lxx_igehely, pozicio', 'karoli_igehely, szovegforma, pozicio', 'strong'])
            meta.append(('lxx_token:forras_sor', str(len(os_sorok))))
        self._lxx_versszam(os_sorok)
        # -- bdb_alias
        if self.licenc_ellenorzes('bdb_alias', SZARMAZTATOTT_LICENC['bdb_alias']):
            ki = [(r['masodlagos_strong'], r['tabla_strong'], r['bdb_id'], r['nyelv'], r['cimszo'],
                   r['szoveg_hasonlosag']) for r in G.tsv_beolvas(os.path.join(self.konk, 'BDB_strong_alias.tsv'))[1]]
            self.tabla('bdb_alias',
                       [('masodlagos_strong', 'TEXT'), ('tabla_strong', 'TEXT'), ('bdb_id', 'TEXT'),
                        ('nyelv', 'TEXT'), ('cimszo', 'TEXT'), ('szoveg_hasonlosag', 'TEXT')],
                       ki, SZARMAZTATOTT_LICENC['bdb_alias'], ['masodlagos_strong'])
            meta.append(('bdb_alias:licenc_osszetevok', '+'.join(SZARMAZTATOTT_LICENC['bdb_alias'])))
        self._nave_vers(os_sorok)

    def _lxx_versszam(self, os_sorok):
        if not self.licenc_ellenorzes('lxx_versszam', SZARMAZTATOTT_LICENC['lxx_versszam']):
            return
        meta = self.olvasoi_meta
        os_par = {}
        for r in os_sorok:
            ig = r['igehely_karoli']
            if not ig:
                continue
            if ig not in self.vi.halmaz:
                self.jelent_norm('lxx_versszam', ig, 'nincs ilyen Károli-vers')
                continue
            k = (r['igehely_lxx'], r['igehely_kjv'], r['karoli_ok'], r['_fajl'])
            if k not in os_par.setdefault(ig, []):
                os_par[ig].append(k)
        # F91 (DT-F91b): a térkép `KJV_igehely` oszlopa KJV-kulcs (nem Károli-vers). A builder a KJV-kulcson illeszt:
        # a KJV-kulcs -> Károli-vers(ek) átváltását (1) az LXX_OS sorai (`igehely_kjv`, `os_par`) és (2) a javított
        # A-tábla (`Karoli_versmegfeleltetes.tsv` `igehely_kjv`) adja; a `terkep_ertek` Károli-kulcsos marad.
        kjv_karoli = {}
        felirat = ZFH.felirat_versek()

        def kjv_kulcs(ig, cv):
            return '%s %s' % (ig.rsplit(' ', 1)[0], cv)
        for ig, lista in os_par.items():
            for (lx, kjv, ok, forma) in lista:
                if ig in felirat:
                    continue     # a felirat-versnek nincs KJV-megfelelője; a közös felirat-halmaz (F91 E2, ZFH) a mérvadó, nem a `karoli_ok` jelölés
                for cv in kjv.split(';'):
                    if re.fullmatch(r'\d+:\d+', cv):
                        v_ = kjv_karoli.setdefault(kjv_kulcs(ig, cv), [])
                        if ig not in v_:
                            v_.append(ig)
        for r in G.tsv_beolvas(os.path.join(self.konk, 'Karoli_versmegfeleltetes.tsv'))[1]:
            ig, cv = r['igehely_karoli'], r['igehely_kjv']
            if ig in self.vi.halmaz and re.fullmatch(r'\d+:\d+', cv):
                v_ = kjv_karoli.setdefault(kjv_kulcs(ig, cv), [])
                if ig not in v_:
                    v_.append(ig)
        terkep, nem_meghat, kjv_kulcsok, kjv_karoli_nelkul = {}, 0, set(), set()
        for r in G.tsv_beolvas(os.path.join(self.konk, 'LXX_versificacios_terkep.tsv'))[1]:
            kk_ = r['KJV_igehely']
            if kk_ == 'NEM_MEGHATAROZHATO':
                nem_meghat += 1      # nem KJV-kulcs: a sor nem kerul a tablaba, de szamolt (ellenor UJ-4)
                continue
            kjv_kulcsok.add(kk_)
            if kk_ not in kjv_karoli:
                kjv_karoli_nelkul.add(kk_)
                self.jelent_norm('lxx_versszam', kk_, 'a térkép KJV-kulcsához nincs Károli-vers')
                continue
            for ig in kjv_karoli[kk_]:
                v = terkep.setdefault(ig, [])
                if (r['Gorog_LXX_vers'], r['Elteres_tipusa']) not in v:
                    v.append((r['Gorog_LXX_vers'], r['Elteres_tipusa']))

        def cv_elso(x):
            m = re.search(r'(\d+):(\d+)', x)
            return (int(m.group(1)), int(m.group(2))) if m else None
        sorok, szaml, elteres, csak_terkep = [], {'LXX_OS': 0, 'nincs': 0}, [], 0
        for ig in self.vi.lista:
            if ig not in self.ot_versek:
                continue
            # a versifikációs térkép NEM forrás (DT-F92b): értéke csak a külön, nem kanonikus `terkep_ertek` oszlopban áll
            tv = ' | '.join(g for g, _ in terkep.get(ig, []))
            if ig in os_par:
                tk = {cv_elso(g) for g, _ in terkep.get(ig, [])} - {None}
                for (lx, kjv, ok, forma) in os_par[ig]:
                    if ig in terkep and cv_elso(lx) not in tk:
                        elteres.append(ig)
                    sorok.append((ig, lx, kjv, 'LXX_OS', ok, forma, tv))
                    szaml['LXX_OS'] += 1
            else:
                if tv:
                    csak_terkep += 1
                sorok.append((ig, '', '', 'nincs', '', '', tv))
                szaml['nincs'] += 1
        both = sum(1 for ig in self.ot_versek if ig in os_par and ig in terkep)
        if self.minta is not None:
            sorok = [x for x in sorok if x[0] in self.minta]
        self.tabla('lxx_versszam',
                   [('karoli_igehely', 'TEXT'), ('lxx_igehely', 'TEXT'), ('kjv_vers', 'TEXT'),
                    ('forras', 'TEXT'), ('megjegyzes', 'TEXT'), ('szovegforma', 'TEXT'),
                    ('terkep_ertek', 'TEXT')],
                   sorok, SZARMAZTATOTT_LICENC['lxx_versszam'], ['karoli_igehely', 'lxx_igehely'])
        for k, v in szaml.items():
            meta.append(('lxx_versszam:sor:' + k, str(v)))
        meta.append(('lxx_versszam:ot_vers', str(len(self.ot_versek))))
        meta.append(('lxx_versszam:terkep_nem_meghatarozhato_sor', str(nem_meghat)))
        meta.append(('lxx_versszam:terkep_kjv_kulcs', str(len(kjv_kulcsok))))
        meta.append(('lxx_versszam:terkep_kjv_kulcs_karoli_nelkul', str(len(kjv_karoli_nelkul))))
        meta.append(('lxx_versszam:terkep_karoli_kulcs', str(len(terkep))))
        meta.append(('lxx_versszam:terkep_ot_vers', str(sum(1 for k in terkep if k in self.ot_versek))))
        meta.append(('lxx_versszam:terkep_nem_ot_vers', str(sum(1 for k in terkep if k not in self.ot_versek))))
        self.norm_jelentes[('lxx_versszam', 'NEM_MEGHATAROZHATO',
                            'a térkép sora nem Károli-kulccsal áll (nem kerül a táblába; sor)')] = nem_meghat
        meta.append(('lxx_versszam:mindket_forras_verse', str(both)))
        meta.append(('lxx_versszam:forras_elteres_verse', str(len(set(elteres)))))
        meta.append(('lxx_versszam:nincs_de_van_terkep_ertek_verse', str(csak_terkep)))
        self.norm_jelentes[('lxx_versszam', 'LXX_OS ≠ versifikációs térkép',
                            'a két forrás LXX-versszáma eltér (vers)')] = len(set(elteres))
        self.norm_jelentes[('lxx_versszam', 'nincs LXX-megfelelő',
                            'a LXX_OS nem ad értéket (vers; üres lxx_igehely, kitöltés nélkül; a térkép értéke legfeljebb a nem kanonikus terkep_ertek oszlopban)')] = szaml['nincs']

    def _nave_vers(self, os_sorok):
        if not self.licenc_ellenorzes('nave_vers', SZARMAZTATOTT_LICENC['nave_vers']):
            return
        meta = self.olvasoi_meta
        lxx_kjv = {}
        for r in os_sorok:
            if r['igehely_karoli'] and r['karoli_ok'] != 'zsolt_felirat_eltolas':
                lxx_kjv.setdefault(r['igehely_karoli'], r['igehely_kjv'])
        vm_kjv = {r['igehely_karoli']: r['igehely_kjv'] for r in
                  G.tsv_beolvas(os.path.join(self.konk, 'Karoli_versmegfeleltetes.tsv'))[1]}
        racs = NB.KjvRacs(self.vi.lista, lxx_kjv, vm_kjv)
        nave = G.tsv_beolvas(os.path.join(self.konk, 'Nave_basokant.tsv'))[1]
        ki, kihagyott, bontott = NB.nave_bont(nave, racs)
        assert len(nave) == bontott + sum(kihagyott.values())
        sorok = []
        for (i, r, ig, tart) in ki:
            if self.minta is not None and ig not in self.minta:
                continue
            sorok.append((i, r['tema_id'], r['tema'], r['cimke'], r['kapcsolat'], r['igehely'], ig, tart))
        self.tabla('nave_vers',
                   [('forras_sor', 'INTEGER'), ('tema_id', 'TEXT'), ('tema', 'TEXT'), ('cimke', 'TEXT'),
                    ('kapcsolat', 'TEXT'), ('nave_hely', 'TEXT'), ('igehely', 'TEXT'), ('tartomanyos', 'INTEGER')],
                   sorok, SZARMAZTATOTT_LICENC['nave_vers'], ['igehely', 'tema_id', 'forras_sor'])
        meta.append(('nave_vers:nave_basokant_sor', str(len(nave))))
        meta.append(('nave_vers:bontott_forras_sor', str(bontott)))
        for ok, d in sorted(kihagyott.items()):
            meta.append(('nave_vers:kihagyott:' + ok, str(d)))
            self.norm_jelentes[('nave_vers', ok, 'a forrás-sor nem bomlik versekre (nem kerül a nave_vers-be)')] = d
        meta.append(('nave_vers:kihagyott_osszes', str(sum(kihagyott.values()))))

    # -- igehely_tartomany ---------------------------------------------------------------
    def _tartomanyok(self):
        sorok = []
        forrasok = (('elofordulasok', ['igehely'], ['id']),
                    ('kapcsolatok', ['forras_igehely', 'cel_igehely'], ['id']),
                    ('jeloltek', ['igehely'], ['id']))
        for tabla, oszl, kulcs in forrasok:
            for r in G.tsv_beolvas(os.path.join(self.adat, tabla + '.tsv'))[1]:
                if tabla == 'jeloltek' and not G.jelolt_elofordulas_e(r):
                    continue  # DT-F127b: a forras_kulcs (id|igehely) csak az előfordulás-jelöltre egyértelmű
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
        self.tabla_lic['fts_motivum'] = self.licenc_feloldas(SZARMAZTATOTT_LICENC['fts_motivum'])
        self.con.execute(
            'CREATE VIRTUAL TABLE fts_motivum USING fts5(szoveg, motivum_id UNINDEXED, rovat UNINDEXED, '
            'forras_fajl UNINDEXED, regi_forras UNINDEXED, tokenize="unicode61 remove_diacritics 2")')
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
                self.con.execute('INSERT INTO fts_motivum VALUES (?,?,?,?,?)',
                                 (torzs, mid, rovat, rel, regi))
                n += 1
        self.tablak['fts_motivum'] = n
        self.megjegyzesek.append('FTS: %d fájl, %d rovat; átmeneti régi tanulmányok `regi_forras=1`; '
                                 'a #11 `migralt: igen` jelzője miatt kiesett: %s'
                                 % (len(fajlok), n, ', '.join(kiesett) if kiesett else 'nincs (a jelző még nem létezik)'))

    # -- jelentes, meta -----------------------------------------------------------------------
    def _jelentes_tabla(self):
        if self.mod == 'teljes':
            self.megjegyzesek.append(
                'Szándékosan nem betöltött konkordancia-táblák: Macula_gorog (a Macula_heber_*, LXX_OS/* és a BDB_strong_alias az F92 óta betöltve), '
                'KJV_/ASV_Strongs_{Genesis,Exodus,Proverbs} (a #48 vezeti ki; a KJV_Strongs_teljes betöltve), '
                'a BDB_*/aram segédtáblák (a BDB_strong_alias az F92 óta betöltve: bdb_alias), SDBH_SDGNT_domenfa, a versmegfeleltetési segédtáblák; '
                'a licencsor hiánya miatt kimaradt táblák száma: %d' % len(self.kihagyott))
        sorok = [(t, nyers, ok, d) for (t, nyers, ok), d in sorted(self.norm_jelentes.items())]
        self.tabla('normalizalas_jelentes', [('tabla', 'TEXT'), ('nyers', 'TEXT'), ('ok', 'TEXT'),
                                             ('darab', 'INTEGER')],
                   sorok, SZARMAZTATOTT_LICENC['normalizalas_jelentes'], ['tabla'])

    def _meta(self):
        self.tabla('meta', [('kulcs', 'TEXT'), ('ertek', 'TEXT')],
                   [('mod', self.mod), ('epites_ts', ts_most()),
                    ('forras', 'adat/*.tsv, konkordancia/*.tsv (eszkozok/sqlite_epit.py, F79)'),
                    ('kihagyott_tablak', '; '.join('%s (%s)' % k for k in self.kihagyott))] + self.olvasoi_meta,
                   SZARMAZTATOTT_LICENC['meta'])

    def _tabla_licenc(self):
        """F89 (DT113): a tablaszintu licenc. Minden epitett tablanak (a sajat magat is beleertve)
        pontosan egy sora van; a licenc-oszlopok nem kerulnek az adattablakba."""
        sajat = self.licenc_feloldas(['projekt_adat'])
        sorok = [(n,) + v for n, v in sorted(self.tabla_lic.items()) if n != 'tabla_licenc']
        sorok.append(('tabla_licenc',) + sajat)
        sorok.sort()
        self.tabla('tabla_licenc', [('tabla', 'TEXT'), ('licenc_allapot', 'TEXT'), ('kereskedelmi', 'TEXT'),
                                    ('licenc_dataset', 'TEXT'), ('cimke', 'TEXT')],
                   sorok, ['projekt_adat'], ['tabla'])


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


def tablameret(db_path):
    """{tabla: (sorszam, bajt_indexszel)} -- a Python sqlite3 nem tartalmazza a dbstat modult,
    ezert minden tablat (indexeivel) kulon ideiglenes adatbazisba masolunk, es a lapszam *
    lapmeret adja a bajtot. (F89: a licenc tablaszintu, a sor-szintu licenc_* oszlopok
    reszesedese mar nem merendo.)"""
    import tempfile
    con = sqlite3.connect(db_path)
    ki = {}
    tmpdir = tempfile.mkdtemp()
    try:
        tablak = con.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                             "AND name NOT LIKE 'fts_motivum_%' ORDER BY name").fetchall()
        for nev, sql in tablak:
            sorszam = con.execute('SELECT COUNT(*) FROM "%s"' % nev).fetchone()[0]
            indexek = [r[0] for r in con.execute(
                "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL", (nev,))]
            f = os.path.join(tmpdir, 'x.db')
            con.execute("ATTACH DATABASE ? AS x", (f,))
            try:
                if sql.upper().startswith('CREATE VIRTUAL'):
                    con.execute(sql.replace('CREATE VIRTUAL TABLE ' + nev, 'CREATE VIRTUAL TABLE x.' + nev, 1))
                    con.execute('INSERT INTO x."%s" SELECT * FROM main."%s"' % (nev, nev))
                else:
                    deklar, cols = [], []
                    for r in con.execute('PRAGMA main.table_info("%s")' % nev):
                        cols.append(r[1])
                        deklar.append('"%s" %s' % (r[1], r[2]))
                    con.execute('CREATE TABLE x."%s" (%s)' % (nev, ', '.join(deklar)))
                    con.execute('INSERT INTO x."%s" SELECT %s FROM main."%s"' % (
                        nev, ', '.join('"%s"' % c for c in cols), nev))
                    for isql in indexek:
                        con.execute(isql.replace('INDEX "', 'INDEX x."', 1))  # UNIQUE INDEX is (F95)
                con.commit()
                lap = con.execute('PRAGMA x.page_count').fetchone()[0]
                meret = con.execute('PRAGMA x.page_size').fetchone()[0]
                ki[nev] = (sorszam, lap * meret)
            finally:
                con.execute('DETACH DATABASE x')
                if os.path.exists(f):
                    os.remove(f)
        return ki
    finally:
        con.close()
        shutil_rm(tmpdir)


def shutil_rm(d):
    import shutil
    shutil.rmtree(d, ignore_errors=True)


def meres_md(epito, hashek, ido, meret, mod, tmeret=None, masodik=None):
    ki = ['# SQLITE_EPIT -- mérés (%s) (F79)' % ('kis minta' if mod == 'minta' else 'teljes építés'), '',
          '*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod %s) | ts=%s`*' % (mod, ts_most()),
          '', '- fájl: `%s`, **%.1f MB**; építési idő (integritás nélkül): **%.1f s**'
          % (os.path.basename(epito.kimenet), meret / 1048576.0, ido), '']
    if mod == 'minta':
        ki.append('- minta: %d Károli-vers (1Móz + a motívumok hivatkozott versei)' % len(epito.minta))
        ki.append('- a lekérdezés-próba külön naplóban áll: `naplok/SQLITE_EPIT_proba_minta.md` (nem íródik felül)')
        ki.append('')
    if masodik is not None:
        h2, azonos = masodik
        ki += ['## Táblánkénti sorszám és tartalom-hash (G2: két egymás utáni építés)', '',
               '**%s** -- a második, ideiglenes építés táblánkénti rendezett tartalom-hash-e %s.'
               % ('AZONOS' if azonos else 'ELTÉRŐ', 'mind azonos' if azonos else 'nem azonos'), '',
               '| tábla | sor | sha256 (1. építés) | sha256 (2. építés) |', '|---|---:|---|---|']
        for n, (db, h) in sorted(hashek.items()):
            ki.append('| `%s` | %d | `%s` | `%s` |' % (n, db, h[:16], (h2.get(n) or (0, ''))[1][:16]))
    else:
        ki += ['## Táblánkénti sorszám és tartalom-hash', '', '| tábla | sor | sha256 (rendezett tartalom) |', '|---|---:|---|']
        for n, (db, h) in sorted(hashek.items()):
            ki.append('| `%s` | %d | `%s` |' % (n, db, h[:16]))
    ki.append('')
    if tmeret:
        ossz = sum(v[1] for v in tmeret.values())
        ki += ['## Táblánkénti bájtméret', '',
               'Mérés: minden tábla (indexeivel) külön adatbázisba másolva, lapszám × lapméret (a Python sqlite3-ból '
               'hiányzik a `dbstat`).', '',
               '- a táblák összege: **%.1f MB** (a fájl: %.1f MB; a többlet a táblánkénti külön adatbázisok saját fejléc- és séma-lapjaiból adódik)'
               % (ossz / 1048576.0, meret / 1048576.0),
               '', '| tábla | sor | MB (indexszel) |', '|---|---:|---:|']
        for n, (db, b) in sorted(tmeret.items(), key=lambda x: -x[1][1]):
            ki.append('| `%s` | %d | %.2f |' % (n, db, b / 1048576.0))
        ki.append('')
    if getattr(epito, 'tabla_lic', None):
        ki += ['## Táblaszintű licenc (`tabla_licenc`, F89 / DT113)', '',
               '| tábla | licenc_allapot | kereskedelmi | licenc_dataset | cimke |', '|---|---|---|---|---|']
        for n, (a, c, ds, cim) in sorted(epito.tabla_lic.items()):
            ki.append('| `%s` | %s | %s | %s | %s |' % (n, a, c, ds, cim))
        ki.append('')
        tt = sorted(n for n, v in epito.tabla_lic.items() if v[0] == 'tisztazatlan')
        sa = sorted(n for n, v in epito.tabla_lic.items() if 'CC BY-SA' in v[3] or 'Mounce' in v[3])
        nc = sorted(n for n, v in epito.tabla_lic.items() if 'BY-NC' in v[3])
        ki += ['- `tisztazatlan` állapotú táblák (%d): %s' % (len(tt), ', '.join('`%s`' % n for n in tt) or 'nincs'),
               '- CC BY-SA 4.0 vagy MCGED (`© Mounce 1993`) címkéjű táblák (%d; zárt csomagból kizárandók, DT116): %s'
               % (len(sa), ', '.join('`%s`' % n for n in sa) or 'nincs'),
               '- CC BY-NC címkéjű táblák (%d): %s' % (len(nc), ', '.join('`%s`' % n for n in nc) or 'nincs'), '']
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
                      ', '.join('`%s`' % n for n, _ in sorted(lista)[:8])))
        ki.append('')
    if epito.megjegyzesek:
        ki += ['## Megjegyzések', ''] + ['- %s' % m for m in epito.megjegyzesek] + ['']
    return '\n'.join(ki) + '\n'


def proba_naplo_md(eredmenyek, mod):
    ki = ['# SQLITE_EPIT -- lekérdezés-próba (%s) (F79 M3)' % ('kis minta' if mod == 'minta' else 'teljes'), '',
          '*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py --proba (--mod %s) | ts=%s`; az ADATVAGYON_TERV 4. '
          'pontjának 1–6., 13–15. pontja; a várt eredmény mindig a megnevezett forrásból, nem az adatbázisból. '
          'Ez a fájl külön napló: a `SQLITE_EPIT_meres*.md` újragenerálása nem írja felül.*' % (mod, ts_most()),
          '', 'Összesítés: %d/%d egyezik.' % (sum(1 for p in eredmenyek if p['ok']), len(eredmenyek)), '',
          proba_md(eredmenyek)]
    return '\n'.join(ki) + '\n'


ELOTTE_KEZDET = '<!-- F89-ELOTTE-KEZDET -->'
ELOTTE_VEGE = '<!-- F89-ELOTTE-VEGE -->'


def elotte_blokk_atvesz(mpath, szoveg):
    """F89: a kezzel rogzitett "elotte" meres (a licenc-valtas elotti allapot) a mereslog
    ujrairasakor megmarad: a korabbi fajl jelolt blokkja az uj fajl elejere kerul."""
    if not os.path.exists(mpath):
        return szoveg
    with open(mpath, encoding='utf-8', newline='') as f:
        regi = f.read().replace(chr(13) + chr(10), chr(10))
    if ELOTTE_KEZDET not in regi or ELOTTE_VEGE not in regi:
        return szoveg
    blokk = regi[regi.index(ELOTTE_KEZDET):regi.index(ELOTTE_VEGE) + len(ELOTTE_VEGE)]
    sorok = szoveg.split(chr(10))
    # a fejlec (1. sor), ures sor, proveniencia, ures sor utan, a "- fajl" sor elott
    idx = next(i for i, x in enumerate(sorok) if x.startswith('- fájl:'))
    return chr(10).join(sorok[:idx] + [blokk, ''] + sorok[idx:])


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
    ap.add_argument('--ketszer', action='store_true', help='G2: második, ideiglenes építés és hash-összevetés')
    ap.add_argument('--meret', action='store_true', help='táblánkénti bájtméret mérése (lassú)')
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
        con.execute('INSERT INTO meta VALUES (?,?)', ('hash:' + n, '%d|%s' % (db, h)))
    con.commit()
    con.close()
    masodik = None
    if args.ketszer:
        import tempfile
        k2 = os.path.join(tempfile.gettempdir(), 'pardes_masodik_ellenorzes.db')
        ep2 = Epito(args.gyoker, k2, args.mod)
        ep2.epit()
        h2 = tablak_hash(k2)
        os.remove(k2)
        masodik = (h2, h2 == hashek)
    proba = probak(kimenet, args.gyoker) if args.proba else None
    tmeret = tablameret(kimenet) if args.meret else None
    meret = os.path.getsize(kimenet)
    if args.naplo:
        nev = 'SQLITE_EPIT_meres_minta.md' if args.mod == 'minta' else 'SQLITE_EPIT_meres.md'
        mpath = os.path.join(args.gyoker, 'naplok', nev)
        szoveg = meres_md(ep, hashek, ido, meret, args.mod, tmeret, masodik)
        szoveg = elotte_blokk_atvesz(mpath, szoveg)
        irj(mpath, szoveg)
        if proba is not None:
            irj(os.path.join(args.gyoker, 'naplok', 'SQLITE_EPIT_proba_%s.md' % args.mod), proba_naplo_md(proba, args.mod))
    print('kész: %s (%.1f MB, %.1f s, %d tábla)' % (kimenet, meret / 1048576.0, ido, len(hashek)))
    if masodik is not None:
        print('G2: a második építés hash-táblája %s' % ('azonos' if masodik[1] else 'ELTÉRŐ'))
    if proba is not None:
        for p in proba:
            print('%2d. pont: %s' % (p['pont'], 'MEGEGYEZIK' if p['ok'] else 'ELTÉRÉS'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
