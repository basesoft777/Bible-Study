"""Az olvasó bekötési leltára: milyen adatunk van, és ebből mi nincs még a versnézeten vagy a szónézeten.

Gépi előállítású, kézi tábla nincs: a `naplok/OLVASO_BEKOTESI_leltar.md` fájlt generálja, ezért nem avulhat el. A szkript
CSAK OLVAS: a `pardes.db`-t csak olvasható módban nyitja (`mode=ro`), a blokk-regisztert és a lekérdező modulokat
a forráskódjukból elemzi (`ast`), NEM importálja (így nem fut le bennük semmi, és nem kell hozzá a szerver környezete).
Blokkot, sablont, adatot nem módosít, szervert nem indít és nem állít le.

Az egyik oldal az adat: az `adat/datasetek.tsv` adatkészletei és a `pardes.db` táblái (a tábla kulcsa az oszlopaiból:
versre szól-e, Strong-számra szól-e). A másik oldal a bekötés: a blokk-regiszter (`blokkok.py` `REGISZTER`, `B(...)` bejegyzések
`tablak` mezője, és a blokk adatlekérőjéből a kódban ténylegesen olvasott táblák), a fejezetlap közvetlen hívásai (`oldalak.py`,
`bibliak.py`) és a keresés blokkjai.

Futtatás (a repó gyökeréből):
    python eszkozok/olvaso_szerver/bekotesi_leltar.py [--db pardes.db] [--kimenet naplok/OLVASO_BEKOTESI_leltar.md]
Összevető mód (a push előtti kapu futtatja, `push_elott.py`): ami az alapon (`git merge-base origin/main HEAD`) az olvasóban látszott
(blokk, tábla, adatkészlet; vers-, szó-, fejezetlap-nézet és keresés), az az ágon is látsszon:
    python eszkozok/olvaso_szerver/bekotesi_leltar.py --osszevet [ALAP]      # HIBA-kilépés (1), ha valami eltűnt, feltételhez kötődött vagy másik fülre került
A kivételek (szándékos változás): `merce/bekotes_kivetel.tsv`, soronként egy indokkal. A „látszik” a blokk szintjén áll (kiadás, hozzáférési szint,
feltételek, fül); a blokkon belüli lenyílót és a jelleg-címkét nem látja (az a renderelt HTML-ben van: `teszt_blokkfej.py`, #810).
A DB útvonala: `--db`, majd a `PARDES_DB` környezeti változó, majd a `konfig/szerver.toml` `db` mezője, majd a repó gyökerének
`pardes.db`-je, végül (linkelt munkafában) a fő checkout `pardes.db`-je.
"""
import argparse
import ast
import os
import re
import sqlite3
import subprocess
import sys
import tomllib
from collections import OrderedDict, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(D))
KONFIG = os.path.join(D, 'konfig')
# A kód és a konfiguráció helye, amelyet a szkript elemez. Alapból a munkafa; az összevető mód ideiglenesen az alap (merge-base) kinyert másolatára állítja.
KOD_DIR = D
KONFIG_DIR = KONFIG
ALAP_KIMENET = os.path.join(GYOKER, 'naplok', 'OLVASO_BEKOTESI_leltar.md')

# A fogyasztó-csoportok: melyik függvények számítanak a fejezetlap közvetlen hívásainak. Ha a kód átnevezi őket, a szkript hibát jelez
# (nem csendben hagyja ki), ezért itt kell követni. A `*` a modul minden függvénye.
FEJEZETLAP_FUGGVENYEK = {'oldalak.py': ('OldalGyar.fejezet_lap', 'OldalGyar._biblia_fejezet_lap'), 'bibliak.py': ('*',)}
KERESES_MODUL = 'kereses.py'
# A hívásokat elemzett modulok (a blokkok a `blokkok.py`-ban vannak, külön elemezve).
FOGYASZTO_MODULOK = ('oldalak.py', 'bibliak.py', 'kereses.py', 'alkalmazas.py', 'allapot.py', 'tanulmany_oldal.py', 'frissesseg.py',
                     'gyorsitotar.py', 'export.py', 'kiejtes_szolg.py', 'arculat.py')

# A tábla kulcsának gépi besorolása az oszlopnevekből. Csak ott van kivétel, ahol az oszlopnév nem árulja el a kulcsot.
VERS_OSZLOP = re.compile(r'(^|_)igehely($|_)|(^|_)vers$|^cel_ig$|^kezdo$|^veg$')
STRONG_OSZLOP = re.compile(r'strong')
KULCS_KIVETEL = {'strong_parok': ('szó', 'az a/b oszlop Strong-szám (a pár két tagja); az oszlopnév ezt nem mutatja')}
KULCS_KIVETEL_OSZLOP = {'strong_parok': 'a'}
# szöveges tartalomra utaló oszlopnevek (a „van-e magyar fordítás” csak ilyen táblánál értelmes)
SZOVEGES_OSZLOP = re.compile(r'szocikk|szoveg|jelentes|glossza|gloss$|definicio|(^|_)tema$|angol|leiras|tukorford|forditas')
FORDITO_TABLAK = ('forditasok', 'glosszak_heber_hu', 'nave_tema_hu', 'bdb_szakasz_hu')
KIADAS_NEV = {'belso': 'belső', 'nyilvanos': 'nyilvános', 'kereskedelmi': 'kereskedelmi'}
BELSO_TABLAK = re.compile(r'^(sqlite_|fts_motivum_)')
SQL_TABLA = re.compile(r'\b(?:FROM|JOIN)\s+"?([A-Za-z_][A-Za-z0-9_]*)"?', re.I)

NEZET_NEV = {'vers': 'versnézet', 'szo_h': 'szónézet (héber)', 'szo_g': 'szónézet (görög)', 'kereses': 'keresés'}


def szam(n):
    return '{:,}'.format(n).replace(',', ' ')


def szazalek(resz, egesz):
    if not egesz:
        return '—'
    p = 100.0 * resz / egesz
    return ('%.1f%%' % p).replace('.', ',') if p < 99.95 or resz < egesz else '100%'


def olvas_tsv(ut):
    """`split('\\t')`-es olvasás (a `csv` modul nem használható ezeken a táblákon, CLAUDE.md). A `#` sorok és a fejléc kezelve."""
    with open(ut, encoding='utf-8') as f:
        sorok = [l.rstrip('\r\n') for l in f if l.strip() and not l.startswith('#')]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


# ---------------------------------------------------------------------------------------------------------------------
# a DB megtalálása és megnyitása (csak olvasás)
# ---------------------------------------------------------------------------------------------------------------------
def db_utvonal(arg):
    jeloltek = [('--db', arg), ('PARDES_DB', os.environ.get('PARDES_DB'))]
    try:
        with open(os.path.join(KONFIG, 'szerver.toml'), 'rb') as f:
            jeloltek.append(('konfig/szerver.toml', tomllib.load(f).get('db') or None))
    except OSError:
        pass
    jeloltek.append(('a repó gyökere', os.path.join(GYOKER, 'pardes.db')))
    try:
        kozos = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=GYOKER, capture_output=True, text=True, timeout=20).stdout.strip()
        if kozos:
            jeloltek.append(('a fő checkout', os.path.join(os.path.dirname(os.path.abspath(os.path.join(GYOKER, kozos))), 'pardes.db')))
    except (OSError, subprocess.SubprocessError):
        pass
    for forras, ut in jeloltek:
        if ut and os.path.isfile(ut):
            return os.path.abspath(ut), forras
    raise SystemExit('nincs pardes.db (próbált helyek: %s); add meg a --db vagy a PARDES_DB értékét' % ', '.join(f for f, u in jeloltek if u))


def megnyit(ut):
    kapcsolat = sqlite3.connect('file:%s?mode=ro' % ut.replace('\\', '/'), uri=True)
    kapcsolat.execute('PRAGMA query_only=1')
    return kapcsolat


# ---------------------------------------------------------------------------------------------------------------------
# a forráskód elemzése (ast): blokk-regiszter, lekérdezések táblái, a fogyasztók hívásai
# ---------------------------------------------------------------------------------------------------------------------
def _parse(fajl):
    with open(os.path.join(KOD_DIR, fajl), encoding='utf-8') as f:
        return ast.parse(f.read(), fajl)


def _lit(csomo, alap=None):
    try:
        return ast.literal_eval(csomo)
    except (ValueError, SyntaxError):
        return alap


def _fv_nev(csomo):
    return csomo.id if isinstance(csomo, ast.Name) else None


def feliratok_hu():
    """{kulcs: magyar felirat} a `konfig/feliratok.tsv`-ből (`split('\t')`, a `csv` modul nélkül); hiányzó fájl: üres. Az `F('kulcs')` blokkcímek feloldásához."""
    ut = os.path.join(KONFIG_DIR, 'feliratok.tsv')
    if not os.path.isfile(ut):
        return {}
    ki = {}
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\r\n')
            if not sor or sor.startswith('#'):
                continue
            r = sor.split('\t')
            if len(r) >= 2 and r[0] != 'kulcs':
                ki[r[0]] = r[1].replace('\\n', '\n')
    return ki


def blokk_cim(csomo):
    """A blokk címe a regiszterből: szöveg-literál, vagy `F('kulcs')` hívás (a `feliratok.tsv` magyar szövege). Ha a kulcs nincs a táblában, a
    cím a nyers `F('kulcs')` jelzés (a leltár nem találgat); más alakú kifejezésnél `?`."""
    szoveg = _lit(csomo)
    if isinstance(szoveg, str):
        return szoveg
    if isinstance(csomo, ast.Call) and isinstance(csomo.func, ast.Name) and csomo.func.id == 'F' and csomo.args:
        kulcs = _lit(csomo.args[0])
        if isinstance(kulcs, str):
            return feliratok_hu().get(kulcs) or "F('%s')" % kulcs
    return '?'


def _blokk(hivas, csoport):
    """Egy `B(...)` hívás a regiszterből: a literál mezők kiolvasva, a függvény-argumentumok neve."""
    a = hivas.args
    b = {'id': _lit(a[0]), 'oldal': _lit(a[1]), 'cim': blokk_cim(a[2]), 'jelleg': _lit(a[3]), 'tablak': tuple(_lit(a[4], ()) or ()),
         'fetch': _fv_nev(a[5]) if len(a) > 5 else None, 'render': _fv_nev(a[6]) if len(a) > 6 else None,
         'jelleg_megj': _lit(a[7], '') if len(a) > 7 else '', 'csoport': csoport,
         'opcionalis': False, 'vers_kell': False, 'ures_rejt': False, 'kovet': (), 'forras_szoveg': '', 'jelleg_fn': False}
    for k in hivas.keywords:
        if k.arg in ('opcionalis', 'vers_kell', 'ures_rejt'):
            b[k.arg] = bool(_lit(k.value, False))
        elif k.arg == 'kovet':
            b['kovet'] = tuple(_lit(k.value, ()) or ())
        elif k.arg == 'forras_szoveg':
            b['forras_szoveg'] = _lit(k.value, '')
        elif k.arg == 'jelleg_fn':
            b['jelleg_fn'] = True
        elif k.arg == 'ures_html':
            b['ures_html'] = True
    if len(a) > 8:
        b['forras_szoveg'] = b['forras_szoveg'] or _lit(a[8], '')
    return b


def regiszter_beolvas(fa):
    """A `blokkok.py` blokkjai: REGISZTER (vers, szó), SZOVEG_FORRAS/SZOVEG_PAR (a fejezetlap szövegoszlopa), KERESES (keresési módok)."""
    ki = []
    for csomo in fa.body:
        if not isinstance(csomo, ast.Assign) or len(csomo.targets) != 1 or not isinstance(csomo.targets[0], ast.Name):
            continue
        nev, ertek = csomo.targets[0].id, csomo.value
        if nev == 'REGISZTER' and isinstance(ertek, ast.List):
            ki += [_blokk(e, 'regiszter') for e in ertek.elts if isinstance(e, ast.Call)]
        elif nev in ('SZOVEG_FORRAS', 'SZOVEG_PAR') and isinstance(ertek, ast.Call):
            ki.append(_blokk(ertek, 'szoveg'))
        elif nev == 'KERESES' and isinstance(ertek, ast.Dict):
            ki += [_blokk(e, 'kereses') for e in ertek.values if isinstance(e, ast.Call)]
    if not [b for b in ki if b['csoport'] == 'regiszter']:
        raise SystemExit('a blokkok.py REGISZTER-e nem olvasható ki (a szkript elavult?)')
    return ki


def modul_fuggvenyek(fa):
    """{minősített név: FunctionDef} (osztályok metódusai `Osztaly.metodus` alakban)."""
    ki = {}

    def be(csomo, elo):
        for gy in ast.iter_child_nodes(csomo):
            if isinstance(gy, (ast.FunctionDef, ast.AsyncFunctionDef)):
                ki['.'.join(elo + [gy.name])] = gy
                be(gy, elo + [gy.name])
            elif isinstance(gy, ast.ClassDef):
                be(gy, elo + [gy.name])
    be(fa, [])
    return ki


def _sajat_tablak(fv, tablak):
    """A függvény törzsének szöveg-literáljaiban (SQL) FROM/JOIN után álló, létező táblák."""
    ki = set()
    for n in ast.walk(fv):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and ('FROM' in n.value.upper() or 'JOIN' in n.value.upper()):
            ki.update(t for t in SQL_TABLA.findall(n.value) if t in tablak)
    return ki


def _hivasok(fv, helyi_nevek, q_nevek):
    """A függvény hívásai: (helyi függvények, a `q.`-n át hívott lekérdezések)."""
    helyi, q = set(), set()
    for n in ast.walk(fv):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name) and n.func.id in helyi_nevek:
                helyi.add(n.func.id)
            elif isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'q' and n.func.attr in q_nevek:
                q.add(n.func.attr)
    return helyi, q


class Tablazo:
    """Függvény → olvasott táblák, tranzitívan (a lekerdezesek.py és a blokkok.py függvényein át)."""

    def __init__(self, tablak):
        self.tablak = tablak
        self.q_fv = {k: v for k, v in modul_fuggvenyek(_parse('lekerdezesek.py')).items() if '.' not in k}
        self.q_memo = {}

    def q_tablak(self, nev, lanc=()):
        if nev in self.q_memo:
            return self.q_memo[nev]
        if nev in lanc or nev not in self.q_fv:
            return set()
        fv = self.q_fv[nev]
        ki = set(_sajat_tablak(fv, self.tablak))
        helyi, _ = _hivasok(fv, set(self.q_fv), set())
        for h in helyi:
            ki |= self.q_tablak(h, lanc + (nev,))
        self.q_memo[nev] = ki
        return ki

    def fv_tablak(self, fv, helyi_fv, helyi_memo, lanc=()):
        """Egy modul-függvény táblái: saját SQL + `q.`-hívások + a modul helyi függvényei."""
        ki = set(_sajat_tablak(fv, self.tablak))
        helyi, q = _hivasok(fv, set(helyi_fv), set(self.q_fv))
        for qn in q:
            ki |= self.q_tablak(qn)
        for h in helyi:
            if h in lanc or h == fv.name:
                continue
            if h not in helyi_memo:
                helyi_memo[h] = self.fv_tablak(helyi_fv[h], helyi_fv, helyi_memo, lanc + (fv.name,))
            ki |= helyi_memo[h]
        return ki


def blokk_kod_tablak(blokkok, tablazo, blokk_fa):
    """Blokkonként a kódban ténylegesen olvasott táblák (az adatlekérő és a megjelenítő függvény tranzitív hívásaiból)."""
    helyi = {k: v for k, v in modul_fuggvenyek(blokk_fa).items() if '.' not in k}
    memo = {}
    for b in blokkok:
        ki = set()
        for nev in (b['fetch'], b['render']):
            if nev and nev in helyi:
                ki |= tablazo.fv_tablak(helyi[nev], helyi, memo)
        b['kod_tablak'] = ki
    return blokkok


def fogyasztok(tablazo):
    """A blokkokon kívüli fogyasztók: {csoport: {tábla: set(hely)}}. Csoport: fejezetlap | keresés (kód) | egyéb."""
    csoportok = defaultdict(lambda: defaultdict(set))
    hianyzo = []
    for modul in FOGYASZTO_MODULOK:
        ut = os.path.join(KOD_DIR, modul)
        if not os.path.isfile(ut):
            continue
        fv = modul_fuggvenyek(_parse(modul))
        helyi = {k.split('.')[-1]: v for k, v in fv.items()}
        memo = {}
        keresett = FEJEZETLAP_FUGGVENYEK.get(modul, ())
        for nev in keresett:
            if nev != '*' and nev not in fv:
                hianyzo.append('%s: %s' % (modul, nev))
        for nev, f in fv.items():
            t = tablazo.fv_tablak(f, helyi, memo)
            if not t:
                continue
            if '*' in keresett or nev in keresett:
                cs = 'fejezetlap'
            elif modul == KERESES_MODUL:
                cs = 'keresés (kód)'
            else:
                cs = 'egyéb'
            for tabla in t:
                csoportok[cs][tabla].add('%s:%s' % (modul[:-3], nev))
    if hianyzo:
        raise SystemExit('a fejezetlap-függvények átneveződtek, a szkript FEJEZETLAP_FUGGVENYEK listája elavult: ' + '; '.join(hianyzo))
    return csoportok


def literal_valtozo(fajl, nev):
    for csomo in _parse(fajl).body:
        if isinstance(csomo, ast.Assign) and len(csomo.targets) == 1 and isinstance(csomo.targets[0], ast.Name) and csomo.targets[0].id == nev:
            return ast.literal_eval(csomo.value)
    raise SystemExit('%s: nincs %s' % (fajl, nev))


# ---------------------------------------------------------------------------------------------------------------------
# az adat oldala: DB-táblák, kulcs, lefedettség
# ---------------------------------------------------------------------------------------------------------------------
def tablak_listaja(con):
    virtualis = [n for n, s in con.execute("SELECT name, sql FROM sqlite_master WHERE type='table'") if s and 'VIRTUAL TABLE' in s.upper()]
    ki = []
    for (n,) in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') ORDER BY name"):
        if BELSO_TABLAK.match(n) or any(n.startswith(v + '_') for v in virtualis):
            continue
        ki.append(n)
    return ki


def kulcs_besorolas(nev, oszlopok):
    if nev in KULCS_KIVETEL:
        k = KULCS_KIVETEL[nev]
        vers = [o for o in oszlopok if VERS_OSZLOP.search(o)]
        return k[0] if not vers else 'mindkettő', k[1], vers, [KULCS_KIVETEL_OSZLOP[nev]]
    vers = [o for o in oszlopok if VERS_OSZLOP.search(o)]
    strong = [o for o in oszlopok if STRONG_OSZLOP.search(o)]
    if vers and strong:
        return 'mindkettő', '', vers, strong
    if vers:
        return 'vers', '', vers, []
    if strong:
        return 'szó', '', [], strong
    return 'egyik sem', '', [], []


def vers_oszlop(oszlopok, vers_cols):
    for o in ('igehely', 'karoli_igehely', 'forras_igehely'):
        if o in vers_cols:
            return o
    return vers_cols[0] if vers_cols else None


def strong_oszlop(strong_cols, nev):
    if nev in KULCS_KIVETEL_OSZLOP:
        return KULCS_KIVETEL_OSZLOP[nev]
    for o in ('strong', 'strong_szam', 'strong_padded', 'heber_strong', 'hebrew_strong', 'gorog_strong', 'greek_strong'):
        if o in strong_cols:
            return o
    return strong_cols[0] if strong_cols else None


def lefedettseg(con, nev, oszlopok, vers_cols, strong_cols, ossz):
    """{'vers': (egyezo, nyers, osszes) | None, 'strong': (h, g, nyers) | None, 'frakcio': float} a tábla lefedettsége."""
    ki = {'vers': None, 'strong': None, 'frakcio': 0.0, 'tartomany': False}
    if vers_cols:
        if nev == 'tanulmany_tartomany':
            n = con.execute('SELECT COUNT(*) FROM vers v WHERE EXISTS (SELECT 1 FROM tanulmany_tartomany t WHERE v.sorrend BETWEEN t.kezdo_sorrend AND t.veg_sorrend)').fetchone()[0]
            ki['vers'] = (n, n, ossz['vers'])
            ki['tartomany'] = True
        else:
            o = vers_oszlop(oszlopok, vers_cols)
            if o == 'vers' and 'fejezet' in oszlopok and 'konyv' in oszlopok and nev != 'vers':
                nyers = con.execute('SELECT COUNT(*) FROM (SELECT DISTINCT konyv, fejezet, vers FROM "%s")' % nev).fetchone()[0]
                ki['vers'] = (nyers, nyers, ossz['vers'])        # a könyvkód nem Károli-kulcs: a versek száma becslés
                ki['becsles'] = True
            else:
                nyers, egyezo = con.execute(
                    'WITH k AS (SELECT DISTINCT "%s" AS v FROM "%s" WHERE "%s" IS NOT NULL) '
                    'SELECT (SELECT COUNT(*) FROM k), (SELECT COUNT(*) FROM vers WHERE igehely IN (SELECT v FROM k))' % (o, nev, o)).fetchone()
                ki['vers'] = (egyezo, nyers, ossz['vers'])
        ki['frakcio'] = max(ki['frakcio'], ki['vers'][0] / ossz['vers'] if ossz['vers'] else 0)
    if strong_cols:
        o = strong_oszlop(strong_cols, nev)
        if o:
            nyers, h, g = con.execute(
                'WITH k AS (SELECT DISTINCT "%s" AS v FROM "%s" WHERE "%s" IS NOT NULL) '
                "SELECT (SELECT COUNT(*) FROM k), "
                "(SELECT COUNT(*) FROM strong_szotar WHERE strong IN (SELECT v FROM k) AND strong LIKE 'H%%'), "
                "(SELECT COUNT(*) FROM strong_szotar WHERE strong IN (SELECT v FROM k) AND strong LIKE 'G%%')" % (o, nev, o)).fetchone()
            ki['strong'] = (h, g, nyers)
            ki['frakcio'] = max(ki['frakcio'], (h + g) / ossz['strong'] if ossz['strong'] else 0)
    return ki


def lefedettseg_szoveg(l, ossz):
    reszek = []
    if l['vers']:
        egyezo, nyers, o = l['vers']
        s = '%s vers (%s)' % (szam(egyezo), szazalek(egyezo, o))
        if l.get('becsles'):
            s += ', becslés: a kulcs nem Károli-igehely'
        elif l['tartomany']:
            s += ' (tartományok lefedése)'
        elif nyers and egyezo < 0.5 * nyers:
            s += ', figyelem: a kulcsok csak %s/%s egyezik a Károli-igehellyel' % (szam(egyezo), szam(nyers))
        reszek.append(s)
    if l['strong']:
        h, g, nyers = l['strong']
        s = 'H %s · G %s szó (%s)' % (szam(h), szam(g), szazalek(h + g, ossz['strong']))
        if nyers and h + g < 0.5 * nyers:
            s += ', figyelem: a kulcsok csak %s/%s egyezik a Strong-szótárral' % (szam(h + g), szam(nyers))
        reszek.append(s)
    return ' · '.join(reszek) or '—'


# ---------------------------------------------------------------------------------------------------------------------
# a bekötés oldala: blokkok láthatósága, nézetek
# ---------------------------------------------------------------------------------------------------------------------
class Hozzaferes:
    def __init__(self):
        with open(os.path.join(KONFIG_DIR, 'hozzaferes.toml'), 'rb') as f:
            c = tomllib.load(f)
        self.szintek = c['szintek']
        self.alap = c['alapertelmezett_szint']
        b = dict(c.get('blokk', {}))
        self.default = b.pop('default', self.szintek[0])
        self.blokk = b

    def min_szint(self, blokk_id):
        return self.blokk.get(blokk_id, self.default)

    def lathato(self, blokk_id):
        return self.szintek.index(self.alap) >= self.szintek.index(self.min_szint(blokk_id))


def blokk_allapot(b, hozz, kizaras, uresek, kiadas):
    """(látszik-e a konfigurált kiadásban és alapszinten, [megjegyzések]). A megjegyzések a feltételek és a kizárások."""
    jegyzet, latszik = [], True
    if not hozz.lathato(b['id']):
        latszik = False
        jegyzet.append('szinthez kötve: %s' % hozz.min_szint(b['id']))
    ki = sorted({k for t in b['tablak'] for k in kizaras.get(t, ())})
    if ki:
        if kiadas in ki:
            latszik = False
        jegyzet.append('kizárva a(z) %s kiadásból' % ' és '.join(KIADAS_NEV.get(k, k) for k in ki))
    if b['opcionalis']:
        jegyzet.append('a régebbi adatbázisból hiányozhat')
    if b['vers_kell']:
        jegyzet.append('csak vers-kontextussal')
    if b['ures_rejt']:
        jegyzet.append('üres eredménynél rejtve')
    if b['kovet']:
        jegyzet.append('követi: %s' % ', '.join(b['kovet']))
    if b['tablak'] and all(uresek.get(t) for t in b['tablak']):
        latszik = False
        jegyzet.append('a tábla üres')
    if not b['tablak'] and not b['forras_szoveg'] and b['csoport'] == 'regiszter':
        jegyzet.append('az adat még nem érhető el')
    return latszik, jegyzet


def nezet_kod(b):
    """A blokk nézete: vers | szó | fejezetlap | keresés."""
    if b['csoport'] == 'szoveg':
        return 'fejezetlap'
    if b['csoport'] == 'kereses':
        return 'keresés'
    return 'vers' if b['oldal'] == 'vers' else 'szó'


# ---------------------------------------------------------------------------------------------------------------------
# a leltár összeállítása
# ---------------------------------------------------------------------------------------------------------------------
def osszeallit(con, ut_db, db_forras, gyors=False):
    """`gyors`: az összevető módhoz: a lefedettség (a lassú, táblánkénti lekérdezések) kimarad; a láthatóság és a kötés ugyanaz."""
    tablak = tablak_listaja(con)
    tabla_set = set(tablak)
    sorok = {t: con.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0] for t in tablak}
    meta = dict(con.execute('SELECT kulcs, ertek FROM meta WHERE kulcs IN (\'epites_ts\', \'mod\')'))
    ossz = {'vers': con.execute('SELECT COUNT(*) FROM vers').fetchone()[0],
            'strong': con.execute('SELECT COUNT(*) FROM strong_szotar').fetchone()[0]}
    ossz['strong_h'] = con.execute("SELECT COUNT(*) FROM strong_szotar WHERE strong LIKE 'H%'").fetchone()[0]
    ossz['strong_g'] = con.execute("SELECT COUNT(*) FROM strong_szotar WHERE strong LIKE 'G%'").fetchone()[0]
    licenc = {t: dict(zip(('allapot', 'kereskedelmi', 'dataset', 'cimke'), r)) for t, *r in
              con.execute('SELECT tabla, licenc_allapot, kereskedelmi, licenc_dataset, cimke FROM tabla_licenc')}
    share_alike = dict(con.execute('SELECT dataset, share_alike FROM licencek'))
    forditasok = dict(((sz, mezo), n) for sz, mezo, n in con.execute('SELECT szotar, mezo, COUNT(*) FROM forditasok GROUP BY 1, 2'))
    forditas_szotar = defaultdict(int)
    for (sz, mezo), n in forditasok.items():
        forditas_szotar[sz] += n

    blokk_fa = _parse('blokkok.py')
    blokkok = regiszter_beolvas(blokk_fa)
    tablazo = Tablazo(tabla_set)
    blokk_kod_tablak(blokkok, tablazo, blokk_fa)
    fogy = fogyasztok(tablazo)
    hozz = Hozzaferes()
    kizaras = literal_valtozo('adatbazis.py', 'TABLA_KIZARAS')
    with open(os.path.join(KONFIG_DIR, 'szerver.toml'), 'rb') as f:
        kiadas = tomllib.load(f).get('kiadas', 'belso')
    ful_nev = dict(literal_valtozo('oldalak.py', 'VERS_FULEK'))
    fulblokk = literal_valtozo('oldalak.py', 'FULBLOKK')
    uresek = {t: n == 0 for t, n in sorok.items()}

    for b in blokkok:
        b['latszik'], b['jegyzet'] = blokk_allapot(b, hozz, kizaras, uresek, kiadas)
        b['nezet'] = nezet_kod(b)
        b['hely'] = ''
        if b['csoport'] == 'regiszter':
            b['hely'] = ('%s fül' % ful_nev[fulblokk.get(b['id'], 'vers')]) if b['oldal'] == 'vers' else 'szó-panel'
        elif b['csoport'] == 'szoveg':
            b['hely'] = 'fejezetlap szövegoszlopa'
        else:
            b['hely'] = 'keresőlap'
        b['nem_deklaralt'] = sorted(b['kod_tablak'] - set(b['tablak']))

    # olvasói nevek: a lapgen bemenet-jegyzék (adat/lapgen_bemenetek.tsv) névkulcsa -> adat/olvasoi_nevtabla.tsv „forras” sorai
    _, nevsorok = olvas_tsv(os.path.join(GYOKER, 'adat', 'olvasoi_nevtabla.tsv'))
    forras_nev = {s['kulcs']: s['olvasoi_nev'] for s in nevsorok if s['tipus'] == 'forras'}
    _, bem = olvas_tsv(os.path.join(GYOKER, 'adat', 'lapgen_bemenetek.tsv'))
    nev_tabla, nev_dataset = {}, {}
    for s in bem:
        n = forras_nev.get(s.get('olvasoi_nev_kulcs', ''))
        if not n:
            continue
        for ut in s['utvonal'].split(';'):
            torzs = os.path.splitext(os.path.basename(ut.strip()))[0].lower()
            if torzs in tabla_set:
                nev_tabla[torzs] = n
        if s['licenc_kulcs'] and s['licenc_kulcs'] != 'projekt_adat':
            nev_dataset[s['licenc_kulcs']] = n
    feliratok_van = os.path.isfile(os.path.join(KONFIG, 'feliratok.tsv'))

    # blokkok táblánként
    tab_blokk = defaultdict(list)
    for b in blokkok:
        for t in sorted(set(b['tablak']) | b['kod_tablak']):
            tab_blokk[t].append(b)

    sorlista = []
    for t in tablak:
        oszlopok = [r[1] for r in con.execute('PRAGMA table_info("%s")' % t)]
        kulcs, kulcs_megj, vers_cols, strong_cols = kulcs_besorolas(t, oszlopok)
        lic = licenc.get(t)
        ds = lic['dataset'] if lic else ''
        tokenek = [x for x in ds.split('+') if x]
        bl = tab_blokk.get(t, [])
        nezetek = defaultdict(list)
        for b in bl:
            nezetek[b['nezet']].append(b)
        if t in fogy['fejezetlap']:
            nezetek['fejezetlap_hivas'] = sorted(fogy['fejezetlap'][t])
        # olvasói név: tábla szerint, ennek híján az adatkészlet szerint (csak nem projekt_adat adatkészletnél)
        nev = nev_tabla.get(t)
        nev_eredet = 'tábla'
        if not nev:
            for tok in tokenek:
                if tok != 'projekt_adat' and tok in nev_dataset:
                    nev, nev_eredet = nev_dataset[tok], 'adatkészlet'
                    break
        # magyar fordítás
        szoveges = bool([o for o in oszlopok if SZOVEGES_OSZLOP.search(o)])
        hu_oszlop = [o for o in oszlopok if re.search(r'_hu$|^magyar$', o)]
        # a fordító-tábla és a tábla közös, szűk (legfeljebb 4 táblás) blokkban áll: a blokk a magyar fordítással együtt mutatja
        parok = sorted({x for b in bl for x in b['tablak'] if t in b['tablak'] and len(b['tablak']) <= 4 and x in FORDITO_TABLAK and x != t})
        elso = tokenek[0].lower() if tokenek else ''
        if t in FORDITO_TABLAK or t.endswith('_hu'):
            magyar = 'maga a fordítás-tábla (%s sor)' % szam(sorok[t])
        elif elso.startswith('karoli') and (szoveges or any(re.search(r'(^|_)szo$|^alak$', o) for o in oszlopok)):
            magyar = 'magyar eredetű (Károli)'
        elif hu_oszlop:
            magyar = 'magyar oszlop a táblában (%s)' % ', '.join(hu_oszlop)
        elif not szoveges:
            magyar = '—'
        elif ds in forditas_szotar and parok:
            magyar = 'igen: %s fordított mező (%s)' % (szam(forditas_szotar[ds]), ', '.join(parok))
        elif ds in forditas_szotar:
            magyar = 'van fordítás (%s mező), de ez a blokk nem mutatja' % szam(forditas_szotar[ds])
        elif parok:
            magyar = 'a blokk magyar fordítással együtt mutatja (%s)' % ', '.join(parok)
        else:
            magyar = 'nincs'
        l = lefedettseg(con, t, oszlopok, vers_cols, strong_cols, ossz) if (sorok[t] and (vers_cols or strong_cols) and not gyors) else \
            {'vers': None, 'strong': None, 'frakcio': 0.0, 'tartomany': False}
        sorlista.append({'tabla': t, 'sor': sorok[t], 'oszlopok': oszlopok, 'kulcs': kulcs, 'kulcs_megj': kulcs_megj, 'vers_cols': vers_cols,
                         'strong_cols': strong_cols, 'licenc': lic, 'dataset': ds, 'tokenek': tokenek, 'blokkok': bl, 'nezetek': nezetek,
                         'nev': nev, 'nev_eredet': nev_eredet, 'magyar': magyar, 'lef': l, 'lef_szoveg': lefedettseg_szoveg(l, ossz),
                         'kod_egyeb': sorted(fogy['egyéb'].get(t, ())), 'kod_keres': sorted(fogy['keresés (kód)'].get(t, ()))})
    return {'tablak': sorlista, 'blokkok': blokkok, 'ossz': ossz, 'meta': meta, 'db': ut_db, 'db_forras': db_forras, 'hozz': hozz, 'kiadas': kiadas,
            'licenc': licenc, 'share_alike': share_alike, 'kizaras': kizaras, 'feliratok_van': feliratok_van, 'fogy': fogy, 'forditas_szotar': forditas_szotar}


def licenc_szoveg(t, share_alike):
    l = t['licenc']
    if not l:
        return '**nincs licencsor**'
    cimke = l['cimke'] or ''
    jel = []
    if l['allapot'] == 'tisztazatlan' and 'tisztázatlan' not in cimke.lower():
        jel.append('tisztázatlan')
    if l['kereskedelmi'] == 'nem' and 'nem kereskedelmi' not in cimke.lower():
        jel.append('nem kereskedelmi')
    elif l['kereskedelmi'] == 'feltetelesen':
        jel.append('feltételesen kereskedelmi')
    if any(share_alike.get(d) == 'igen' for d in l['dataset'].split('+')) or 'BY-SA' in cimke:
        jel.append('share-alike')
    return '%s%s' % (cimke, ' [' + ', '.join(jel) + ']' if jel else '')


def latszik_szoveg(t, L):
    """A tábla láthatósága az olvasóban (a konfigurált kiadásban és alapszinten). A kiadási kizárás a táblára vonatkozik; a feltételek
    csak akkor kerülnek ide, ha a tábla minden látható blokkja feltételes (különben a tábla feltétel nélkül is látszik)."""
    bl = [b for b in t['blokkok'] if b['nezet'] in ('vers', 'szó', 'keresés')]
    fejezetlapon = bool(t['nezetek'].get('fejezetlap') or t['nezetek'].get('fejezetlap_hivas'))
    if not bl and not fejezetlapon:
        return 'nincs blokk'
    kizart = sorted(L['kizaras'].get(t['tabla'], ()))
    lathato = [b for b in bl if b['latszik']]
    feltetelek = lambda b: [j for j in b['jegyzet'] if not j.startswith('kizárva')]
    if not lathato and not (fejezetlapon and not bl):
        alap = 'nem látszik'
        jegyek = sorted({j for b in bl for j in b['jegyzet'] if not j.startswith('kizárva')})
    elif lathato and all(feltetelek(b) for b in lathato) and not fejezetlapon:
        alap = 'feltételhez kötve'
        jegyek = sorted({j for b in lathato for j in feltetelek(b)})
    else:
        alap = 'látszik' if (lathato or fejezetlapon) else 'nem látszik'
        if not bl:
            alap = 'látszik (csak a fejezetlapon)'
        jegyek = []
    if kizart:
        jegyek.append('kizárva a(z) %s kiadásból' % ' és '.join(KIADAS_NEV.get(k, k) for k in kizart))
    return alap + (' — ' + '; '.join(jegyek) if jegyek else '')


def kotes_allapot(t):
    """A tábla kötése: (versnézeten, szónézeten, fejezetlapon, keresésben, csak kód olvassa)."""
    nz = t['nezetek']
    return (bool(nz.get('vers')), bool(nz.get('szó')), bool(nz.get('fejezetlap') or nz.get('fejezetlap_hivas')), bool(nz.get('keresés')),
            bool(t['kod_egyeb'] or t['kod_keres']))


def be_nem_kotott(L):
    """Versre vagy szóra szóló tábla, amely sem blokkban, sem a fejezetlapon, sem a keresésben nem szerepel. Lefedettség szerint csökkenő."""
    lista = []
    for t in L['tablak']:
        if t['kulcs'] == 'egyik sem' or not t['sor']:
            continue
        v, s, f, k, _ = kotes_allapot(t)
        if not (v or s or f or k):
            lista.append(t)
    lista.sort(key=lambda t: (-t['lef']['frakcio'], -t['sor'], t['tabla']))
    return lista


def egyik_nezeten_hianyzik(L):
    """Mindkét nézetre szóló (vagy a másik nézetre is értelmezhető) tábla, amely csak az egyik nézeten van kötve."""
    lista = []
    for t in L['tablak']:
        if t['kulcs'] != 'mindkettő' or not t['sor']:
            continue
        v, s, f, k, _ = kotes_allapot(t)
        if (v or f) != s and (v or f or s):
            lista.append((t, 'a versnézeten nincs' if not (v or f) else 'a szónézeten nincs'))
    lista.sort(key=lambda x: (-x[0]['lef']['frakcio'], -x[0]['sor'], x[0]['tabla']))
    return lista


# ---------------------------------------------------------------------------------------------------------------------
# a Markdown
# ---------------------------------------------------------------------------------------------------------------------
def cella(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def blokk_lista_szoveg(t, hossz=6):
    kodok = []
    for nez in ('vers', 'szó', 'fejezetlap', 'keresés'):
        for b in t['nezetek'].get(nez, ()):
            kodok.append('`%s`%s' % (b['id'], '*' if b['nem_deklaralt'] and t['tabla'] in b['nem_deklaralt'] else ''))
    if t['nezetek'].get('fejezetlap_hivas'):
        kodok.append('fejezetlap-hívás')
    if len(kodok) > hossz:
        kodok = kodok[:hossz] + ['… (+%d)' % (len(kodok) - hossz)]
    return ', '.join(kodok) or '—'


def kod_hely_szoveg(t):
    reszek = []
    if t['kod_egyeb']:
        reszek.append('máshol: ' + ', '.join(sorted(set(x.split(':')[0] for x in t['kod_egyeb']))))
    if t['kod_keres'] and not t['nezetek'].get('keresés'):
        reszek.append('keresés kódja')
    return '; '.join(reszek)


def olvasoi_nev_szoveg(t):
    if not t['nev']:
        return '—'
    return t['nev'] + (' (adatkészlet-szinten)' if t['nev_eredet'] == 'adatkészlet' else '')


def kiir_szakasz_be_nem_kotott(L, ki):
    lista = be_nem_kotott(L)
    ki.append('## 1. Be nem kötött, de versre vagy szóra szóló adat (lefedettség szerint csökkenő)')
    ki.append('')
    ki.append('Ebből választ a szerkesztő; a választás lesz a blokk-jegyzék (`konfig/blokk_jegyzek.tsv`) első feltöltése. '
              'Ide az a tábla kerül, amelyet sem blokk (a regiszter `tablak` mezője vagy az adatlekérő kódja), sem a fejezetlap közvetlen hívása, '
              'sem a keresés nem olvas, és amelynek a kulcsa versre vagy Strong-számra szól. A tábla utolsó oszlopa jelzi, ha a szerver kódja '
              'máshol mégis olvassa (akkor a tábla támaszadat, nem feltétlenül kötendő blokk).')
    ki.append('')
    for cim, szuro in (('1/a. Külső adatkészlet adata', lambda t: t['tokenek'] and any(x != 'projekt_adat' for x in t['tokenek'])),
                       ('1/b. Saját (projekt) adat és munkatáblák', lambda t: not t['tokenek'] or all(x == 'projekt_adat' for x in t['tokenek']))):
        reszlista = [t for t in lista if szuro(t)]
        ki.append('### %s (%d tábla)' % (cim, len(reszlista)))
        ki.append('')
        if not reszlista:
            ki.append('Nincs ilyen tábla.')
            ki.append('')
            continue
        ki.append('| # | Tábla | Adatkészlet | Kulcs | Sor | Lefedettség | Olvasói név | Magyar fordítás | Licenc | A kód máshol |')
        ki.append('|--:|---|---|---|--:|---|---|---|---|---|')
        for i, t in enumerate(reszlista, 1):
            ki.append('| %d | `%s` | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                i, t['tabla'], cella(t['dataset'] or '—'), t['kulcs'], szam(t['sor']), cella(t['lef_szoveg']), cella(olvasoi_nev_szoveg(t)),
                cella(t['magyar']), cella(licenc_szoveg(t, L['share_alike'])), cella(kod_hely_szoveg(t))))
        ki.append('')
    reszleges = egyik_nezeten_hianyzik(L)
    ki.append('### 1/c. Mindkét nézetre szóló adat, amely csak az egyik nézeten kötött (%d tábla)' % len(reszleges))
    ki.append('')
    ki.append('A kulcsa versre is és szóra is szól (például a vers és a Strong-szám együtt), de az egyik nézeten nincs blokkja. '
              'Nem minden ilyen adat kötendő mindkét helyre; a szerkesztő dönt.')
    ki.append('')
    if reszleges:
        ki.append('| # | Tábla | Adatkészlet | Hiány | Kötött helyen | Lefedettség | Olvasói név | Licenc |')
        ki.append('|--:|---|---|---|---|---|---|---|')
        for i, (t, hiany) in enumerate(reszleges, 1):
            ki.append('| %d | `%s` | %s | %s | %s | %s | %s | %s |' % (
                i, t['tabla'], cella(t['dataset'] or '—'), hiany, cella(blokk_lista_szoveg(t, 4)), cella(t['lef_szoveg']),
                cella(olvasoi_nev_szoveg(t)), cella(licenc_szoveg(t, L['share_alike']))))
        ki.append('')


def kiir_adatkeszletek(L, ki, ds_sorok):
    ki.append('## 2. Adatkészletek (`adat/datasetek.tsv` + a licenc-leltár adatkészlet-nevei)')
    ki.append('')
    ki.append('Az adatkészlet a `datasetek.tsv` sora (a `fajl` mezővel), illetve a `tabla_licenc` adatkészlet-neve. A DB-táblák a licenc-adatkészlet '
              'neve szerint kapcsolódnak (egy tábla több adatkészletből is épülhet, `+` jellel). Ahol az adatkészletnek nincs táblája, a '
              '`sqlite_epit.py` nem építi be a `pardes.db`-be.')
    ki.append('')
    ki.append('| Adatkészlet | `datasetek.tsv` (kötelezőség · állapot) | DB-táblák | Blokkban | Látszik | Licenc | Magyar fordítás |')
    ki.append('|---|---|---|--:|--:|---|---|')
    for nev, info in ds_sorok:
        ts = info['tablak']
        kotott = [t for t in ts if any(kotes_allapot(t)[:4])]
        lat = [t for t in ts if latszik_szoveg(t, L).startswith('látszik')]
        magyar = list(OrderedDict.fromkeys(t['magyar'].split(' (')[0].split(':')[0] for t in ts if t['magyar'] not in ('—', 'nincs')))
        lic = sorted({(t['licenc'] or {}).get('cimke', '') for t in ts} - {''})
        ki.append('| %s | %s | %s | %d/%d | %d/%d | %s | %s |' % (
            nev, cella(info['policy'] or '—'), cella(', '.join('`%s`' % t['tabla'] for t in ts[:6]) + (' … (+%d)' % (len(ts) - 6) if len(ts) > 6 else '') if ts else '**nincs DB-tábla**'),
            len(kotott), len(ts), len(lat), len(ts), cella('; '.join(lic[:2]) + (' …' if len(lic) > 2 else '') if lic else '—'),
            cella('; '.join(magyar[:2]) if magyar else '—')))
    ki.append('')


def kiir_tablak(L, ki):
    ki.append('## 3. Minden DB-tábla (%d)' % len(L['tablak']))
    ki.append('')
    ki.append('Blokk-oszlop: a regiszter `tablak` mezőjében szereplő blokk-azonosító; csillag (`*`): a blokk adatlekérője olvassa a táblát, de a `tablak` mező '
              'nem sorolja fel (így a blokk forrás- és licencsora sem mutatja). A „Látszik” a konfigurált kiadásra (`%s`) és az alapszintre (`%s`) értendő.' % (
                  L['kiadas'], L['hozz'].alap))
    ki.append('')
    ki.append('| Tábla | Adatkészlet | Kulcs | Sor | Blokk (vers · szó · fejezetlap · keresés) | Látszik | Olvasói név | Licenc | Magyar fordítás | Lefedettség |')
    ki.append('|---|---|---|--:|---|---|---|---|---|---|')
    for t in L['tablak']:
        kulcs = {'vers': 'vers → versnézet', 'szó': 'Strong → szónézet', 'mindkettő': 'vers + Strong → mindkettő', 'egyik sem': 'egyik sem'}[t['kulcs']]
        ki.append('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            t['tabla'], cella(t['dataset'] or '—'), kulcs, szam(t['sor']), cella(blokk_lista_szoveg(t)), cella(latszik_szoveg(t, L)), cella(olvasoi_nev_szoveg(t)),
            cella(licenc_szoveg(t, L['share_alike'])), cella(t['magyar']), cella(t['lef_szoveg'])))
    ki.append('')


def kiir_blokkok(L, ki):
    ki.append('## 4. A blokk-regiszter (a blokk-jegyzék kiindulása)')
    ki.append('')
    ki.append('Minden blokk egy sor: azonosító, nézet, hely, látszik-e, a `tablak` mező és a kódban ténylegesen olvasott többlet-táblák.')
    ki.append('')
    ki.append('| Blokk | Cím | Nézet | Hely | Látszik | `tablak` | Kódban olvasott többlet | Jelzések |')
    ki.append('|---|---|---|---|---|---|---|---|')
    for b in L['blokkok']:
        ki.append('| `%s` | %s | %s | %s | %s | %s | %s | %s |' % (
            b['id'], cella(b['cim']), b['nezet'], b['hely'], 'igen' if b['latszik'] else 'NEM', cella(', '.join(b['tablak']) or '—'),
            cella(', '.join(b['nem_deklaralt']) or '—'), cella('; '.join(b['jegyzet']) or '—')))
    ki.append('')


def osszefoglalo(L, ds_sorok):
    tl = L['tablak']
    adat = [t for t in tl if t['kulcs'] != 'egyik sem']
    be = be_nem_kotott(L)
    kotott = [t for t in adat if any(kotes_allapot(t)[:4])]
    lat = [t for t in adat if latszik_szoveg(t, L).startswith('látszik')]
    blokk_lat = [b for b in L['blokkok'] if b['latszik']]
    ds_kulso = [(n, i) for n, i in ds_sorok if n != 'projekt_adat']
    ds_db = [(n, i) for n, i in ds_kulso if i['tablak']]
    ds_kotott = [(n, i) for n, i in ds_db if any(any(kotes_allapot(t)[:4]) for t in i['tablak'])]
    ds_lat = [(n, i) for n, i in ds_db if any(latszik_szoveg(t, L).startswith('látszik') for t in i['tablak'])]
    return {'tabla_ossz': len(tl), 'tabla_adat': len(adat), 'kotott': len(kotott), 'latszik': len(lat), 'be_nem_kotott': len(be),
            'blokk_ossz': len(L['blokkok']), 'blokk_latszik': len(blokk_lat), 'ds_ossz': len(ds_kulso), 'ds_db': len(ds_db), 'ds_kotott': len(ds_kotott),
            'ds_latszik': len(ds_lat), 'ds_db_nelkul': [n for n, i in ds_kulso if not i['tablak']]}


def dataset_sorok(L):
    """[(adatkészlet-név, {'policy', 'tablak'})]: a datasetek.tsv egyedi nevei + a licenc-leltár nevei (projekt_adat külön, utolsónak)."""
    _, sorok = olvas_tsv(os.path.join(GYOKER, 'adat', 'datasetek.tsv'))
    info = OrderedDict()
    for s in sorok:
        n = s['dataset']
        if n == 'dataset':
            continue
        p = info.setdefault(n, {'policy': set(), 'tablak': []})
        p['policy'].add('%s · %s' % (s['kotelezoseg'], s['allapot']))
    kisbetus = {n.lower(): n for n in info}
    for t in L['tablak']:
        nevek = list(t['tokenek'])
        if t['tabla'] in kisbetus and kisbetus[t['tabla']] not in nevek:
            nevek.append(kisbetus[t['tabla']])               # a datasetek.tsv neve a tábla neve (kisbetűvel), a licenc-adatkészlet más
        for tok in nevek:
            info.setdefault(tok, {'policy': set(), 'tablak': []})['tablak'].append(t)
    ki = []
    for n, i in info.items():
        i['policy'] = ' / '.join(sorted(i['policy']))
        ki.append((n, i))
    ki.sort(key=lambda x: (x[0] == 'projekt_adat', x[0].lower()))
    return ki


def generalt_szoveg(L):
    ds = dataset_sorok(L)
    os_ = osszefoglalo(L, ds)
    ossz = L['ossz']
    ki = []
    ki.append('# GENERÁLT: eszkozok/olvaso_szerver/bekotesi_leltar.py — kézzel szerkeszteni tilos; a forrás (adat, regiszter, kód) javul, és újragenerálódik')
    ki.append('')
    ki.append('# Az olvasó bekötési leltára')
    ki.append('')
    ki.append('A leltár azt mutatja meg, milyen adatunk van, és ebből mi nincs még a versnézeten vagy a szónézeten. '
              'Nem azonos az alak-kapu hibalistájával: az a meglévő blokkok hibáit méri, ez a még be nem kötött adatot. '
              'A blokk-jegyzék (`konfig/blokk_jegyzek.tsv`) első feltöltéséhez ad választási alapot; azt ez a leltár nem írja.')
    ki.append('')
    ki.append('- Adatbázis: `%s` (építés: %s, mód: %s; a DB útvonala a(z) %s szerint)' % (
        os.path.basename(L['db']), L['meta'].get('epites_ts', '?'), L['meta'].get('mod', '?'), L['db_forras']))
    ki.append('- Lefedettség nevezője: %s vers (a `vers` tábla), %s Strong-szám (a `strong_szotar`: H %s, G %s)' % (
        szam(ossz['vers']), szam(ossz['strong']), szam(ossz['strong_h']), szam(ossz['strong_g'])))
    ki.append('- Kiadás és szint, amelyre a „látszik” értendő: `%s`, `%s`' % (L['kiadas'], L['hozz'].alap))
    ki.append('')
    ki.append('## Összefoglaló')
    ki.append('')
    ki.append('- Adatkészlet: **%d** (a `projekt_adat` saját táblái nélkül); ebből **%d** áll a `pardes.db`-ben, **%d** van legalább egy blokkban vagy a fejezetlapon, '
              '**%d** látszik legalább egy táblájával.' % (os_['ds_ossz'], os_['ds_db'], os_['ds_kotott'], os_['ds_latszik']))
    ki.append('- Nincs DB-táblája (a `sqlite_epit.py` nem építi be): %s.' % (', '.join('`%s`' % n for n in os_['ds_db_nelkul']) or 'nincs ilyen'))
    ki.append('- DB-tábla: **%d**, ebből versre vagy Strong-számra szóló: **%d**; ebből kötött (blokk, fejezetlap vagy keresés): **%d**, látszik: **%d**, '
              '**be nem kötött: %d**.' % (os_['tabla_ossz'], os_['tabla_adat'], os_['kotott'], os_['latszik'], os_['be_nem_kotott']))
    ki.append('- Blokk a regiszterben (a keresési módokkal és a szövegoszloppal együtt): **%d**, ebből látszik: **%d**.' % (os_['blokk_ossz'], os_['blokk_latszik']))
    ki.append('')
    ki.append('## Hogyan olvasd, és mit nem tud')
    ki.append('')
    ki.append('- **Kulcs** (az oszlopnevekből, gépileg): `igehely`-jellegű oszlop (vagy `konyv`+`fejezet`+`vers`) → versnézet; `strong`-jellegű oszlop → szónézet; '
              'mindkettő → mindkettő; különben egyik sem. Egy kivétel van, a `KULCS_KIVETEL` a szkriptben (`strong_parok`).')
    ki.append('- **Bekötött**: a tábla szerepel egy blokk `tablak` mezőjében, vagy a blokk adatlekérője/megjelenítője (a `lekerdezesek.py` hívásain át) olvassa, '
              'vagy a fejezetlap közvetlen hívása (`oldalak.py`: `fejezet_lap`, `_biblia_fejezet_lap`; `bibliak.py`) olvassa, vagy keresési blokk. '
              'Ha csak a kód olvassa máshol (fejléc, számlálók, ellenőrzések), az a „máshol” jelzés; ez nem kötés.')
    ki.append('- **Látszik**: a konfigurált kiadásban (`konfig/szerver.toml`) és az alapszinten (`konfig/hozzaferes.toml`) a blokk látszik-e. A „feltételhez kötve” '
              'azt jelenti, hogy a blokk csak bizonyos feltétellel áll a lapon (vers-kontextus, üres eredménynél rejtve, a régebbi DB-ből hiányozhat, másik blokkot követ). '
              'A **csukva** állapotot a regiszter nem rögzíti (a lenyílók a blokkok belsejében vannak), ezért ez a leltár nem mutatja.')
    ki.append('- **Olvasói név**: az `adat/olvasoi_nevtabla.tsv` `forras` sorai a lapgenerátor bemenet-jegyzékén (`adat/lapgen_bemenetek.tsv`) át, tábla- (a fájlnév azonos a táblanévvel) '
              'vagy adatkészlet-szinten. A blokkcímek (4. szakasz) az olvasón látható magyar címek: a regiszter szöveg-literálja, vagy az `F("kulcs")` hívás a `konfig/feliratok.tsv`-ből; %s.' % (
                  'a tábla olvasói neve (3. szakasz) nem a feliratokból jön' if L['feliratok_van'] else 'a `konfig/feliratok.tsv` nem létezik, ezért az `F(...)` címek nyers kulcsként állnak'))
    ki.append('- **Magyar fordítás**: a `forditasok` tábla mezői (szótár szerint), a magyar glosszák/Nave/BDB-bontás táblái, és a blokk, amely a táblát a fordítással együtt olvassa. '
              'A `—` azt jelenti, hogy a táblában nincs szöveges oszlop. A `nincs` szöveges táblára gépileg nem talált fordítást.')
    ki.append('- **Licenc**: a `tabla_licenc` (cimke, jelzések) és a `licencek` (share-alike).')
    ki.append('- **Lefedettség**: hány versre vagy Strong-számra van legalább egy sor. Verseknél a Károli-igehellyel egyező kulcsok, Strong-számnál a `strong_szotar`-ral egyezők.')
    ki.append('- A leltár nem ítél arról, mi *kötendő*: egy támaszadat (például egy szóalak-tábla) lehet, hogy sosem lesz önálló blokk.')
    ki.append('')
    kiir_szakasz_be_nem_kotott(L, ki)
    kiir_adatkeszletek(L, ki, ds)
    kiir_tablak(L, ki)
    kiir_blokkok(L, ki)
    return '\n'.join(ki) + '\n', os_


# ---------------------------------------------------------------------------------------------------------------------
# az összevető mód: ami az alapon (a `git merge-base origin/main HEAD`) látszott, az az ágon is látsszon (adatkészlet-, tábla- és blokkszint)
# ---------------------------------------------------------------------------------------------------------------------
KIVETEL_UT = os.path.join(D, 'merce', 'bekotes_kivetel.tsv')
KIVETEL_SZINTEK = ('blokk', 'tabla')
NEZETEK = ('vers', 'szó', 'fejezetlap', 'keresés')
RANG_SZOVEG = {2: 'látszik', 1: 'feltételhez kötve', 0: 'nem látszik'}


def _feltetelek(b):
    return [j for j in b['jegyzet'] if not j.startswith('kizárva')]


def blokk_rang(b):
    """2: feltétel nélkül látszik; 1: feltételhez kötve (vers-kontextus, üres eredménynél rejtve, hiányozhat, követ); 0: nem látszik."""
    if not b['latszik']:
        return 0
    return 1 if _feltetelek(b) else 2


def latszo(L, ds_sorok=None):
    """A „látszik” halmaz: {(szint, kulcs, nézet): {'rang', 'hely', 'blokkok'}}. Szint: blokk | tabla | adatkeszlet. A tábla rangja a nézetben a
    legjobb blokkjáé (a fejezetlap közvetlen hívása feltétel nélküli); az adatkészleté a legjobb tábláé. A kiadás és a hozzáférési szint
    a blokk állapotában már benne van (konfigurált kiadás és alapszint)."""
    ki = {}
    for b in L['blokkok']:
        ki[('blokk', b['id'], b['nezet'])] = {'rang': blokk_rang(b), 'hely': b['hely'], 'blokkok': frozenset([b['id']])}
    tabla_rang = {}
    for t in L['tablak']:
        for nez in NEZETEK:
            bl = [b for b in t['nezetek'].get(nez, ()) if blokk_rang(b) > 0]
            rang = max([blokk_rang(b) for b in bl] + [2 if (nez == 'fejezetlap' and t['nezetek'].get('fejezetlap_hivas')) else 0])
            if rang:
                ki[('tabla', t['tabla'], nez)] = {'rang': rang, 'hely': '', 'blokkok': frozenset(b['id'] for b in bl)}
                tabla_rang[(t['tabla'], nez)] = rang
    for nev, info in (ds_sorok if ds_sorok is not None else dataset_sorok(L)):
        for nez in NEZETEK:
            rangok = [tabla_rang.get((t['tabla'], nez), 0) for t in info['tablak']]
            if rangok and max(rangok):
                ki[('adatkeszlet', nev, nez)] = {'rang': max(rangok), 'hely': '', 'blokkok': frozenset()}
    return ki


def osszevet(alap, ag):
    """Az alap és az ág `latszo` halmazának összevetése. Kimenet: [{'szint', 'kulcs', 'nezet', 'alap', 'ag', 'ok', 'magyarazott'}].
    A tábla- és adatkészlet-szintű eltérés `magyarazott`, ha a láthatóságot adó blokkok mind eltérnek (az ok a blokk-szintű sor), illetve
    ha az adatkészlet egy táblája eltér (az ok a tábla-szintű sor): ezek csak következmények, a hibát az ok adja."""
    ki = []
    blokk_elt = set()
    for k, a in sorted(alap.items()):
        if k[0] != 'blokk' or a['rang'] == 0:
            continue
        g = ag.get(k)
        rang_ag = g['rang'] if g else 0
        if rang_ag < a['rang']:
            ok = 'a blokk hiányzik a regiszterből' if g is None else 'a blokk %s' % RANG_SZOVEG[rang_ag]
        elif a['hely'].startswith('Vers') and g and not g['hely'].startswith('Vers') and rang_ag > 0:
            ok = 'a blokk másik fülre került (%s → %s)' % (a['hely'], g['hely'])
        else:
            continue
        blokk_elt.add(k[1])
        ki.append({'szint': 'blokk', 'kulcs': k[1], 'nezet': k[2], 'alap': RANG_SZOVEG[a['rang']] + (' (%s)' % a['hely'] if a['hely'] else ''),
                   'ag': ok, 'ok': ok, 'magyarazott': False})
    tabla_elt = set()
    for k, a in sorted(alap.items()):
        if k[0] != 'tabla' or a['rang'] == 0:
            continue
        rang_ag = ag.get(k, {'rang': 0})['rang']
        if rang_ag < a['rang']:
            tabla_elt.add((k[1], k[2]))
            ki.append({'szint': 'tabla', 'kulcs': k[1], 'nezet': k[2], 'alap': RANG_SZOVEG[a['rang']], 'ag': RANG_SZOVEG[rang_ag],
                       'ok': 'a tábla ebben a nézetben %s' % RANG_SZOVEG[rang_ag],
                       'magyarazott': bool(a['blokkok']) and a['blokkok'] <= blokk_elt})
    for k, a in sorted(alap.items()):
        if k[0] != 'adatkeszlet' or a['rang'] == 0:
            continue
        rang_ag = ag.get(k, {'rang': 0})['rang']
        if rang_ag < a['rang']:
            ki.append({'szint': 'adatkeszlet', 'kulcs': k[1], 'nezet': k[2], 'alap': RANG_SZOVEG[a['rang']], 'ag': RANG_SZOVEG[rang_ag],
                       'ok': 'az adatkészlet ebben a nézetben %s' % RANG_SZOVEG[rang_ag], 'magyarazott': True})
    return ki


def kivetelek_beolvas(ut=KIVETEL_UT):
    """[(szint, kulcs, nézet, indok)]. A `*` bármire illik. Ismeretlen szint vagy 20 karakternél rövidebb indok: hiba (egy sor indok kötelező)."""
    ki = []
    if not os.path.isfile(ut):
        return ki
    with open(ut, encoding='utf-8') as f:
        sorok = [l.rstrip('\r\n') for l in f if l.strip() and not l.startswith('#')]
    for s in sorok[1:]:                                   # az első sor a fejléc
        r = s.split('\t')
        if len(r) != 4 or r[0] not in KIVETEL_SZINTEK or len(r[3].strip()) < 20:
            raise ValueError('bekotes_kivetel.tsv: négy oszlop (szint, kulcs, nezet, indok), a szint %s, az indok legalább 20 karakter: %r'
                             % ('/'.join(KIVETEL_SZINTEK), s))
        ki.append(tuple(r))
    return ki


def kivetel_szerint(elteresek, kivetelek):
    """(hibák, kivételesek): a nem magyarázott eltérés hiba, kivéve, ha egy kivétel-sor illik rá (szint, kulcs, nézet; `*` bármi)."""
    hibak, kivetelesek = [], []
    for e in elteresek:
        if e['magyarazott']:
            continue
        k = next((k for k in kivetelek if k[0] == e['szint'] and k[1] in ('*', e['kulcs']) and k[2] in ('*', e['nezet'])), None)
        (kivetelesek if k else hibak).append((e, k))
    return [e for e, _ in hibak], kivetelesek


def alap_kinyer(alap):
    """Az alap (git-hivatkozás) `eszkozok/olvaso_szerver/*.py` és `konfig/*.toml` fájljainak kinyerése ideiglenes könyvtárba. A tar tagjainak
    útját nem használja közvetlenül: a fájlnév alapján, a célkönyvtáron belülre ír. Visszaad: a kinyert olvaso_szerver könyvtár útja."""
    import io
    import tarfile
    import tempfile
    p = subprocess.run(['git', 'archive', '--format=tar', alap, '--', 'eszkozok/olvaso_szerver/*.py', 'eszkozok/olvaso_szerver/konfig/*.toml',
                        'eszkozok/olvaso_szerver/konfig/feliratok.tsv'],
                       cwd=GYOKER, capture_output=True, timeout=300)
    if p.returncode != 0:
        raise SystemExit('git archive %s: %s' % (alap, p.stderr.decode('utf-8', 'replace').strip()))
    tmp = tempfile.mkdtemp(prefix='bekotes_alap_')
    cel = os.path.join(tmp, 'eszkozok', 'olvaso_szerver')
    os.makedirs(os.path.join(cel, 'konfig'))
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as t:
        for m in t.getmembers():
            if not m.isfile():
                continue
            reszek = m.name.split('/')
            if reszek[:2] != ['eszkozok', 'olvaso_szerver'] or '..' in reszek:
                continue
            if len(reszek) == 3 and reszek[2].endswith('.py'):
                ut = os.path.join(cel, reszek[2])
            elif len(reszek) == 4 and reszek[2] == 'konfig' and (reszek[3].endswith('.toml') or reszek[3] == 'feliratok.tsv'):
                ut = os.path.join(cel, 'konfig', reszek[3])
            else:
                continue
            with open(ut, 'wb') as f:
                f.write(t.extractfile(m).read())
    return cel


def merge_base(ref='origin/main'):
    p = subprocess.run(['git', 'merge-base', ref, 'HEAD'], cwd=GYOKER, capture_output=True, text=True, timeout=60)
    if p.returncode != 0 or not p.stdout.strip():
        raise SystemExit('nincs merge-base (%s): %s' % (ref, p.stderr.strip()))
    return p.stdout.strip()


def osszevet_futtat(db_arg, alap_ref):
    """A teljes összevetés: (alap sha, eltérések, hibák, kivételesek, a vizsgált alap-elemek száma). A munkafa állapota az „ág”."""
    global KOD_DIR, KONFIG_DIR
    alap = merge_base(alap_ref) if alap_ref in (None, 'origin/main') else alap_ref
    ut, forras = db_utvonal(db_arg)
    con = megnyit(ut)
    try:
        ag = latszo(osszeallit(con, ut, forras, gyors=True))
        cel = alap_kinyer(alap)
        regi = (KOD_DIR, KONFIG_DIR)
        KOD_DIR, KONFIG_DIR = cel, os.path.join(cel, 'konfig')
        try:
            ma = latszo(osszeallit(con, ut, forras, gyors=True))
        except SystemExit as e:
            raise SystemExit('az alap (%s) elemzése nem sikerült, a leltár-szkript elavult lehet: %s' % (alap[:8], e))
        finally:
            KOD_DIR, KONFIG_DIR = regi
    finally:
        con.close()
    elteresek = osszevet(ma, ag)
    hibak, kivetelesek = kivetel_szerint(elteresek, kivetelek_beolvas())
    return alap, elteresek, hibak, kivetelesek, sum(1 for v in ma.values() if v['rang'])


def osszevet_kiir(alap, elteresek, hibak, kivetelesek, vizsgalt):
    print('bekotesi_leltar --osszevet: alap %s, %d látszó elem vizsgálva (blokk, tábla, adatkészlet; nézetenként)' % (alap[:8], vizsgalt))
    kovetkezmeny = [e for e in elteresek if e['magyarazott']]
    for e, k in kivetelesek:
        print('KIVÉTEL  %s %s (%s): %s -> %s; indok: %s' % (e['szint'], e['kulcs'], e['nezet'], e['alap'], e['ag'], k[3]))
    for e in hibak:
        print('HIBA     %s %s (%s): a main-en %s, az ágon %s' % (e['szint'], e['kulcs'], e['nezet'], e['alap'], e['ag']))
    if kovetkezmeny:
        print('(%d tábla- vagy adatkészlet-szintű következmény a fenti blokk-, illetve táblaszintű okok miatt; külön nem hiba)' % len(kovetkezmeny))
    if hibak:
        print('HIBA: %d elem látszott az alapon, az ágon nem látszik vagy rosszabb. Szándékos változás: egy sor kivétel a '
              '`eszkozok/olvaso_szerver/merce/bekotes_kivetel.tsv`-ben (szint, kulcs, nézet, indok), a szerkesztő döntésével.' % len(hibak))
    else:
        print('0 HIBA: ami az alapon látszott, az az ágon is látszik%s.' % (' (%d kivétellel)' % len(kivetelesek) if kivetelesek else ''))
    return 1 if hibak else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--db', default=None, help='a pardes.db útvonala (alapból: PARDES_DB, szerver.toml, repó, fő checkout)')
    ap.add_argument('--kimenet', default=ALAP_KIMENET, help='a Markdown kimenet útvonala')
    ap.add_argument('--osszevet', nargs='?', const='origin/main', default=None, metavar='ALAP',
                    help='összevetés: ami az alapon (alap: git merge-base origin/main HEAD; vagy a megadott git-hivatkozáson) látszott, az az ágon is látsszon; HIBA-kilépés (1), ha nem')
    a = ap.parse_args()
    if a.osszevet is not None:
        sys.exit(osszevet_kiir(*osszevet_futtat(a.db, a.osszevet)))
    ut, forras = db_utvonal(a.db)
    con = megnyit(ut)
    try:
        L = osszeallit(con, ut, forras)
    finally:
        con.close()
    szoveg, os_ = generalt_szoveg(L)
    os.makedirs(os.path.dirname(os.path.abspath(a.kimenet)), exist_ok=True)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('kész: %s' % a.kimenet)
    for k, v in os_.items():
        print('  %s: %s' % (k, v))


if __name__ == '__main__':
    main()
