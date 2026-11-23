"""F235: tervellenőr — az olvasó kéréskor futó lekérdezései nem olvashatnak végig index nélkül nagy táblát.

A `lekerdezesek.py` az olvasó egyetlen SQL-helye (Semgrep: N-F76c). Ez a teszt az `ast`-tal kigyűjti belőle az összes SELECT-et (a modul szintű
szövegállandókat és az összefűzéseket feloldva; az `IN`-listás darabok `IN (?)`-re egészülnek ki), minden lekérdezésre `EXPLAIN QUERY PLAN`-t futtat egy
azonos sémájú adatbázison, és megállapítja, mely táblát olvassa végig (`SCAN`). A határ: 1000 sornál nagyobb táblán a `SCAN` tilos, ha a lekérdezés
kéréskor fut (az induláskor egyszer futók listája: `EGYSZERI`).

A vizsgált adatbázis a `teszt_adat/pardes_sema.sql` (a valódi pardes.db táblái és indexei, adat nélkül; a teszt memóriában építi fel), a táblák
sorszáma a `teszt_adat/pardes_meretek.tsv` (a valódi adatbázisból): az index megléte dönt, nem az adat mérete, ezért az üres séma elég, és a teszt a
CI-ben is fut (Python szabványkönyvtár, Flask nélkül, ezredmásodpercek). A két fájl generált: `python teszt_tervor.py --sema-ment` a PARDES_DB-ből
írja újra (az `sqlite_epit.py` indexváltozása után kötelező; a helyi `test_sema_egyezik_az_adatbazissal` ezt őrzi, ha van PARDES_DB).

A séma-egyezés (N246) csak az olvasó tábláira szigorú: azokra, amelyek neve a `lekerdezesek.py`-ban (az olvasó egyetlen SQL-helyén) előfordul, és az
ezekre épülő indexekre. Ezeknél a hiány, a más definíció és a többlet (pl. egy új index `--sema-ment` nélkül) bukás: ez a tervellenőr terveit
érinti. A többi tábla és index eltérése csak `SÉMA-TÁJÉKOZTATÓ` sor. Ok: minden új `adat/*.tsv` táblát kap (`sqlite_epit.py` `_adat_tablak`), és az
olvasó tesztje nem pirosodhat egy olyan táblától, amelyet az olvasó nem olvas (2026-11-23: 12 ilyen tábla a tárolt séma óta, egyiket sem olvassa az
olvasó). Az olvasó új táblája a `test_a_lekerdezesek_elemezhetok`-on bukik, amíg a tárolt séma nem frissül.

Ismert korlátok (F235, független ellenőr): az `ELFOGADOTT` függvényszintű (egy elfogadott függvényben ugyanarra a táblára írt új, végigolvasó lekérdezés átmegy,
amíg a függvény a listán áll); a `SEARCH ... USING AUTOMATIC INDEX` sort a teszt nem jelzi (az is teljes olvasás); az SQLite-verziók tervei eltérhetnek
(ezért a tábla-halmaz tagjai többesek, pl. `ubs_dbh`).

A kivételek (`ELFOGADOTT`) kimondott és megszámolt lista: minden tétel egy kéréskor futó, ma indexet nem használó lekérdezés, megnevezett célfeladattal.
A teszt bukik, ha (a) egy lekérdezés a listán kívül olvas végig nagy táblát, vagy (b) a lista egy tétele már nem olvas végig (a javítás után a tételt
törölni kell: a lista nem hízhat el), vagy (c) a lista darabszáma eltér a `ELFOGADOTT_DB`-től.

Használat:  python teszt_tervor.py [--listaz | --sema-ment]     (`--listaz`: a végigolvasó lekérdezések listája; `--sema-ment`: a tárolt séma újraírása)
"""
import ast
import os
import re
import sqlite3
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D))
LEK = os.path.join(D, 'lekerdezesek.py')
SEMA = os.path.join(D, 'teszt_adat', 'pardes_sema.sql')
MERETEK = os.path.join(D, 'teszt_adat', 'pardes_meretek.tsv')
HATAR_SOR = 1000

# A lekerdezesek.py függvényei, amelyek folyamatonként egyszer (indulásnál, a `Kozos` felépítésekor) futnak, nem kéréskor.
EGYSZERI = {
    'konyvek', 'tabla_licencek', 'licenc_share_alike', 'morf_kulcs', 'nyelvtani_strongok', 'karoli_strong_konyvek', 'meta', 'meta_sorok',
    'vers_sorrendek', 'fejezetek', 'bizonyossag_ertekek',
}

# Kéréskor (vagy az első kérésen) futó, ma végigolvasó lekérdezések: (függvény, tábla) -> célfeladat. A második részben (az `sqlite_epit.py` indexei és az
# előre számolt elérhetőségi tábla, a #101 merge-e után) mind megszűnik; a teszt (b) pontja akkor kéri a tétel törlését.
_F2 = 'F235 2. rész: index az sqlite_epit.py-ban (a #101 merge-e után)'
# függvény -> ({a végigolvasott táblák}, célfeladat). A táblák halmaza a különböző SQLite-verziók különböző tervei miatt több tagú lehet (pl. `ubs_dbh`).
ELFOGADOTT = {
    # a `forditasok` (szotar, strong) indexe: az 1. részben a lapszintű `IN (...)` lekérdezés egy végigolvasásra vonta össze a strongonkénti hívásokat
    'elotolt_strongok': ({'forditasok'}, _F2),
    '_bdb_magyar_sorok': ({'forditasok'}, _F2),
    'magyar_gorog': ({'forditasok'}, _F2),
    'glossza_gorog_hu': ({'forditasok'}, _F2),
    'ubs_dbh_hu': ({'forditasok'}, _F2),
    'ubs_dbh_szo': ({'forditasok'}, _F2),
    'forditas_bejegyzesek': ({'forditasok'}, _F2),
    'aramai_xml': ({'morf_nyelv_aramai'}, _F2 + ' (xml_id)'),
    'ubs_dbh': ({'ubs_dbh_referenciak', 'ubs_dbh_jelentesek'}, _F2 + ' (ubs_dbh_referenciak.igehely)'),
    'ubs_d2': ({'ubs_dbh_referenciak', 'ubs_dbh_jelentesek'}, _F2 + ' (lexid)'),
    'kjv_karoli_terkep': ({'vers_szamozas'}, _F2 + ' (a `substr` helyett tartomány-feltétel)'),
    'nave_fejezet': ({'nave_basokant'}, _F2 + ' (hely_tipus, igehely)'),
    'bdb_szakasz_sorok': ({'bdb_szakaszok'}, _F2 + ' (strong)'),
    'bdb_szakasz_hu_sorok': ({'bdb_szakasz_hu'}, _F2 + ' (strong)'),
    'bdb_vers_jelentes': ({'bdb_vers_jelentes'}, _F2 + ' (strong)'),
    'tbesh_lemma': ({'tbesh'}, _F2 + ' (a `GLOB ? || [a-zA-Z]` helyett tartomány-feltétel)'),
    'lxx_bridge_g': ({'lxx_bridge'}, _F2 + ' (greek_strong)'),
    'thayer_szakasz_sorok': ({'thayer_szakaszok'}, _F2 + ' (strong)'),
    'glossza_heber_hu': ({'glosszak_heber_hu'}, _F2 + ' (strong)'),
    'glosszak_heber_hu_angol': ({'glosszak_heber_hu'}, _F2 + ' (strong)'),
    'thayer_vers_pontok': ({'thayer_vers_jelentes'}, _F2 + ' (strong)'),
    # az első kérésen futó hat összesítő lekérdezés (`bibliak.Tar`): az előre számolt elérhetőségi tábla váltja ki
    'biblia_fejezetek_karoli_kulcs': ({'vers'}, _F2 + ' (elérhetőségi tábla)'),
    # a frázis-kereső önillesztése: a terv a helyőrző-értékekkel egy generikus terv, a mért idő 8–11 ms; külön vizsgálat kell
    '_frazis_sql': ({'token_karoli'}, 'külön tétel: a frázis-kereső terve (a `nyitott/uj/` alatt)'),
}
ELFOGADOTT_DB = 23     # a lista rögzített darabszáma (függvények): a második rész ezt csökkenti (a törölt tétellel együtt)


# ---------------------------------------------------------------------------------------------------------------------
def _folyik(node, env):
    """Egy kifejezés szövege, ha összefűzött szövegállandókból és modulszintű állandókból áll; különben None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _folyik(node.left, env), _folyik(node.right, env)
        return a + b if a is not None and b is not None else None
    return None


def sql_lista(ut=LEK):
    """[(függvény, sql)]: a modul összes feloldható SELECT/WITH szövege."""
    with open(ut, encoding='utf-8') as f:
        fa = ast.parse(f.read())
    env = {}
    for n in fa.body:                                             # modulszintű szövegállandók, sorrendben (egymásra épülhetnek)
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            v = _folyik(n.value, env)
            if v is not None:
                env[n.targets[0].id] = v
    ki = []

    def jar(node, fv):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fv = node.name
        v = _folyik(node, env) if isinstance(node, (ast.Constant, ast.BinOp)) else None
        if v is not None:
            ki.append((fv, v))
            return
        for gy in ast.iter_child_nodes(node):
            jar(gy, fv)
    for n in fa.body:
        if isinstance(n, ast.Assign) and isinstance(n.value, (ast.Constant, ast.BinOp)) and _folyik(n.value, env) is not None:
            continue                                              # a modulszintű állandó: ott használják, ahol hivatkozzák
        jar(n, '<modul>')
    # a hivatkozott modulszintű SQL-állandók a használó függvényhez
    nevek = {k: v for k, v in env.items() if re.match(r'\s*(SELECT|WITH)\b', v, re.I)}
    for fn in [x for x in ast.walk(fa) if isinstance(x, ast.FunctionDef)]:
        for nm in ast.walk(fn):
            if isinstance(nm, ast.Name) and nm.id in nevek:
                ki.append((fn.name, nevek[nm.id]))
    egyedi, lat = [], set()
    for f, s in ki:
        s = re.sub(r'\s+', ' ', s).strip()
        if not re.match(r'(SELECT|WITH)\b', s, re.I):
            continue
        s = re.sub(r'^(SELECT )%s(%s)?', r'\1*', s, flags=re.I).replace('%%', '%').replace('%s', '')      # `'...' % (...)` sablonok
        if re.search(r'\bIN\s*$', s, re.I):
            s += ' (?)'                                           # az `_in` előtag-darabja: a helyőrző-lánc a hívásnál áll össze
        if (f, s) not in lat:
            lat.add((f, s))
            egyedi.append((f, s))
    return egyedi


def tablameretek():
    """{tábla: sorszám} a `pardes_meretek.tsv`-ből."""
    m = {}
    with open(MERETEK, encoding='utf-8') as f:
        for sor in f:
            p = sor.rstrip('\n').split('\t')
            if len(p) == 2 and p[1].isdigit():
                m[p[0]] = int(p[1])
    return m


def _alias_tabla(sql):
    """{alias vagy táblanév: táblanév} a FROM és JOIN tagokból."""
    ki = {}
    for t, al in re.findall(r'\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z_0-9]*)(?:\s+(?:AS\s+)?([A-Za-z_][A-Za-z_0-9]*))?', sql, re.I):
        ki[t] = t
        if al and al.upper() not in ('WHERE', 'JOIN', 'LEFT', 'INNER', 'ON', 'GROUP', 'ORDER', 'LIMIT', 'UNION', 'USING', 'CROSS', 'NATURAL'):
            ki[al] = t
    return ki


def tervek(con, sql):
    """[(művelet, tábla vagy alias, részlet)] az EXPLAIN QUERY PLAN-ból; hiba esetén ('HIBA', '', üzenet)."""
    db = sql.count('?')
    try:
        sorok = con.execute('EXPLAIN QUERY PLAN ' + sql, ('x',) * db).fetchall()
    except sqlite3.Error as ex:
        return [('HIBA', '', str(ex))]
    ki = []
    for _id, _szulo, _n, r in sorok:
        m = re.match(r'(SCAN|SEARCH)\s+(?:TABLE\s+)?(\S+)(.*)', r)
        if m:
            ki.append((m.group(1), m.group(2), r))
    return ki


def vegigolvasasok(con, meretek=None):
    """[(függvény, tábla, sql, terv)]: azok a lekérdezések, amelyek HATAR_SOR-nál nagyobb táblát végigolvasnak."""
    meretek = meretek or tablameretek()
    ki = []
    for f, sql in sql_lista():
        al = _alias_tabla(sql)
        for muv, nev, r in tervek(con, sql):
            if muv != 'SCAN':
                continue
            tabla = al.get(nev, nev)
            if tabla.startswith('SUBQUERY') or tabla.startswith('CONSTANT'):
                continue
            if meretek.get(tabla, 0) > HATAR_SOR:
                ki.append((f, tabla, sql, r))
    return ki


FTS_VARAZS = re.compile(r'^fts_[a-z_]+_(data|idx|content|docsize|config)$')


def sema_adatbazis():
    """Üres, a valódi sémával megegyező memória-adatbázis a `pardes_sema.sql`-ből (a virtuális táblák árnyéktáblái kimaradnak: azokat az SQLite hozza létre)."""
    con = sqlite3.connect(':memory:')
    with open(SEMA, encoding='utf-8') as f:
        szoveg = f.read()
    for tagok in szoveg.split('\n-- ;;\n'):
        tagok = '\n'.join(l for l in tagok.split('\n') if not l.startswith('-- ')).strip()
        if not tagok:
            continue
        try:
            con.execute(tagok)
        except sqlite3.OperationalError as ex:
            if 'fts5' not in str(ex):                            # az FTS5 hiánya nem a séma hibája; a virtuális tábla kimarad
                raise
    return con


def sema_objektumok(con):
    """{(típus, név): (tábla, normalizált SQL)} a táblákra és indexekre, az FTS5 árnyéktáblái nélkül."""
    lek = "SELECT type, name, tbl_name, sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%'"
    return {(t, n): (tb, re.sub(r'\s+', ' ', q)) for t, n, tb, q in con.execute(lek) if not FTS_VARAZS.match(n)}


def olvaso_tablak(nevek, ut=LEK):
    """A `nevek` közül azok, amelyek szóként előfordulnak a `lekerdezesek.py`-ban (a dinamikusan összerakott táblanév is: a teljes forrást nézi)."""
    with open(ut, encoding='utf-8') as f:
        szavak = set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', f.read()))
    return {n for n in nevek if n in szavak}


def sema_osszevet(valodi, tarolt, olvaso):
    """(bukás, tájékoztató): [(fajta, típus, név)] listák, fajta: 'hiány' (a tárolt sémában van, a valódi adatbázisban nincs), 'eltérés' (más
    definíció), 'többlet' (a valódi adatbázisban van, a tárolt sémában nincs). Bukás az olvasó tábláin (`olvaso`) és az azokra épülő indexeken,
    a többi csak tájékoztató (N246). Az `fts_motivum` virtuális tábla az FTS5 hiányában kimaradhat: nem vizsgáljuk."""
    v = {k: x for k, x in valodi.items() if k != ('table', 'fts_motivum')}
    t = {k: x for k, x in tarolt.items() if k != ('table', 'fts_motivum')}
    elter = [('hiány',) + k for k in sorted(set(t) - set(v))] + \
            [('eltérés',) + k for k in sorted(k for k in t if k in v and v[k][1] != t[k][1])] + \
            [('többlet',) + k for k in sorted(set(v) - set(t))]
    bukas = [e for e in elter if (t.get(e[1:]) or v.get(e[1:]))[0] in olvaso]
    return bukas, [e for e in elter if e not in bukas]


def sema_ment(db_ut):
    """A pardes_sema.sql és a pardes_meretek.tsv újraírása a valódi adatbázisból (a `--sema-ment` hívja)."""
    con = sqlite3.connect('file:%s?mode=ro' % db_ut.replace('\\', '/'), uri=True)
    sorok = con.execute("SELECT type, name, sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' "
                        "ORDER BY CASE type WHEN 'table' THEN 0 ELSE 1 END, name").fetchall()
    sorok = [r for r in sorok if not FTS_VARAZS.match(r[1])]
    os.makedirs(os.path.dirname(SEMA), exist_ok=True)
    fej = ('-- GENERÁLT: python eszkozok/olvaso_szerver/teszt_tervor.py --sema-ment (PARDES_DB=<a valódi pardes.db>) — kézzel nem szerkesztendő (F235).\n'
           '-- A pardes.db táblái és indexei adat nélkül; a tervellenőr (teszt_tervor.py) ebből építi a memória-adatbázist. A tagokat a `-- ;;` sor választja el.\n')
    with open(SEMA, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + '\n-- ;;\n'.join(r[2] for r in sorok) + '\n')
    tablak = [r[1] for r in sorok if r[0] == 'table']
    with open(MERETEK, 'w', encoding='utf-8', newline='\n') as f:
        for t in tablak:
            try:
                n = con.execute('SELECT COUNT(*) FROM "%s"' % t.replace('"', '""')).fetchone()[0]
            except sqlite3.Error:
                continue
            f.write('%s\t%d\n' % (t, n))
    con.close()
    return len(sorok), len(tablak)


# ---------------------------------------------------------------------------------------------------------------------
class TestTervor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = sema_adatbazis()

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_a_lekerdezesek_elemezhetok(self):
        """Minden kigyűjtött lekérdezés előkészíthető a mintán (a séma egyezik); a hiba a lekérdezés vagy a séma hibája."""
        rossz = [(f, sql[:90], t[0][2]) for f, sql in sql_lista() for t in [tervek(self.con, sql)] if t and t[0][0] == 'HIBA']
        self.assertEqual(rossz, [], 'nem elemezhető lekérdezések (a pardes_sema.sql elavult? `--sema-ment`)')

    @unittest.skipUnless(os.environ.get('PARDES_DB') and os.path.isfile(os.environ.get('PARDES_DB', '')), 'nincs PARDES_DB: a séma-egyezés helyben ellenőrzendő (nem zöld, kimarad)')
    def test_sema_egyezik_az_adatbazissal(self):
        """A tárolt séma (a fa saját objektumai) megvan a valódi adatbázisban, azonos definícióval: egy indexváltozás után a `--sema-ment` nélkül
        a tervellenőr elavult tervet néz. A valódi adatbázis többlete csak kiírás (N246: a közös adatbázist több ág építi)."""
        c = sqlite3.connect('file:%s?mode=ro' % os.environ['PARDES_DB'].replace('\\', '/'), uri=True)
        valodi = sema_objektumok(c)
        c.close()
        tarolt = sema_objektumok(self.con)
        olvaso = olvaso_tablak({x[0] for x in list(valodi.values()) + list(tarolt.values())})
        bukas, tajek = sema_osszevet(valodi, tarolt, olvaso)
        for e in tajek:
            print('SÉMA-TÁJÉKOZTATÓ (nem bukás, N246: az olvasó nem olvassa): %s: %s %s' % e)
        # az oszlopok és az index-oszlopok is: egy azonos nevű, de más oszlopú index nem maradhat észrevétlen
        self.assertEqual(bukas, [], 'az olvasó tábláinak sémája eltér a valódi adatbázisétól (--sema-ment; hiánynál régebbi adatbázis is lehet)')

    def test_sema_osszevetes_a_tobbletre_nem_bukik(self):
        """N246 (DB nélkül): az olvasó tábláján (és az arra épülő indexen) minden eltérés bukás, a többi tábláé csak tájékoztató."""
        tarolt = {('table', 'a'): ('a', 'CREATE TABLE a (x)'), ('index', 'ix_a'): ('a', 'CREATE INDEX ix_a ON a (x)'),
                  ('table', 'fts_motivum'): ('fts_motivum', 'V'), ('table', 'b'): ('b', 'CREATE TABLE b (z)')}
        valodi = dict(tarolt)
        valodi.pop(('table', 'fts_motivum'))
        valodi.update({('table', 'uj_adat'): ('uj_adat', 'CREATE TABLE uj_adat (y)'), ('index', 'ix_b'): ('b', 'CREATE INDEX ix_b ON b (z)')})
        self.assertEqual(sema_osszevet(valodi, tarolt, {'a'}), ([], [('többlet', 'index', 'ix_b'), ('többlet', 'table', 'uj_adat')]))
        valodi[('index', 'ix_uj')] = ('a', 'CREATE INDEX ix_uj ON a (x)')        # új index az olvasó tábláján: bukás
        valodi[('index', 'ix_a')] = ('a', 'CREATE INDEX ix_a ON a (x, y)')       # más oszlopú index: bukás
        self.assertEqual(sema_osszevet(valodi, tarolt, {'a'})[0], [('eltérés', 'index', 'ix_a'), ('többlet', 'index', 'ix_uj')])
        valodi.pop(('table', 'a'))
        self.assertIn(('hiány', 'table', 'a'), sema_osszevet(valodi, tarolt, {'a'})[0])
        self.assertEqual(olvaso_tablak({'vers', 'otlettar_nem_letezo_nev'}), {'vers'})

    def test_minden_tabla_szerepel_a_meretek_kozott(self):
        """Egy hiányzó tábla 0 sornak számítana, és a tervellenőr nem jelezné a végigolvasását: minden séma-tábla szerepeljen a `pardes_meretek.tsv`-ben."""
        tablak = {n for (n,) in self.con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'") if not FTS_VARAZS.match(n)}
        self.assertEqual(sorted(tablak - set(tablameretek()) - {'fts_motivum'}), [], 'hiányzik a méretek közül (--sema-ment)')

    def test_nincs_ervenytelen_kivetel_es_a_kivetelek_szama_rogzitett(self):
        self.assertEqual(len(ELFOGADOTT), ELFOGADOTT_DB, 'az ELFOGADOTT lista nem hízhat el: új tétel nem vehető fel a célfeladat megnevezése nélkül')
        self.assertTrue(all(cel.strip() for _, cel in ELFOGADOTT.values()), 'minden kivételnek megnevezett célfeladat kell')

    def test_kereskor_futo_lekerdezes_nem_olvas_vegig_nagy_tablat(self):
        # (a) a listán kívüli végigolvasás; (b) a listán lévő, de már nem végigolvasó függvény
        talalat = [(f, t, r) for f, t, sql, r in vegigolvasasok(self.con) if f not in EGYSZERI]
        uj = [(f, t, r) for f, t, r in talalat if t not in ELFOGADOTT.get(f, (set(), ''))[0]]
        self.assertEqual(uj, [], 'kéréskor futó lekérdezés végigolvas egy %d sornál nagyobb táblát (hiányzó index?)' % HATAR_SOR)
        elavult = sorted(set(ELFOGADOTT) - {f for f, _, _ in talalat})
        self.assertEqual(elavult, [], 'az ELFOGADOTT függvény már nem olvas végig: töröld a listáról (és az ELFOGADOTT_DB-t csökkentsd)')

    def test_a_tervor_pirosat_ad_szandekosan_index_nelkuli_probalekerdezesre(self):
        """A kapu valóban jelez: egy index nélküli, nagy táblára kimondott lekérdezés a tervellenőrön piros ."""
        con = sqlite3.connect(':memory:')
        con.execute('CREATE TABLE proba_nagy (kulcs TEXT, ertek TEXT)')
        con.execute('CREATE TABLE proba_indexelt (kulcs TEXT, ertek TEXT)')
        con.execute('CREATE INDEX ix_proba ON proba_indexelt(kulcs)')
        rossz = tervek(con, 'SELECT ertek FROM proba_nagy WHERE kulcs=?')
        jo = tervek(con, 'SELECT ertek FROM proba_indexelt WHERE kulcs=?')
        con.close()
        self.assertTrue(any(m == 'SCAN' for m, _, _ in rossz), 'az index nélküli próbalekérdezés SCAN-t kell mutasson: %r' % (rossz,))
        self.assertTrue(all(m == 'SEARCH' for m, _, _ in jo), 'az indexelt próbalekérdezés SEARCH: %r' % (jo,))


if __name__ == '__main__':
    if '--sema-ment' in sys.argv:
        db = os.environ.get('PARDES_DB')
        if not db or not os.path.isfile(db):
            sys.exit('PARDES_DB kell (a valódi pardes.db)')
        print('kiírva: %d séma-tag, %d tábla' % sema_ment(db))
        sys.exit(0)
    if '--listaz' in sys.argv:
        sys.argv.remove('--listaz')
        con = sema_adatbazis()
        meret = tablameretek()
        lista = sql_lista()
        print('%d lekérdezés' % len(lista))
        for f, sql in lista:
            al = _alias_tabla(sql)
            for muv, nev, r in tervek(con, sql):
                tabla = al.get(nev, nev)
                jel = 'SCAN!' if muv == 'SCAN' and meret.get(tabla, 0) > HATAR_SOR else muv
                if muv in ('SCAN', 'HIBA'):
                    print('%-6s %-9s %-28s %6d  %s | %s' % (jel, 'EGYSZERI' if f in EGYSZERI else '', f, meret.get(tabla, 0), r[:70], sql[:90]))
        sys.exit(0)
    unittest.main()
