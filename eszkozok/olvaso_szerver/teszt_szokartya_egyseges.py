"""F231 (olvasó egyben, 2026-11-22): az egységes szókártya és a hibalista kapui.

1. `szokartya_szoveg`: a szótári szöveg olvasói alakja (rövidítőjel, ‖, „szemben”, tanú-jel, &, +, felső index) a mérce példáin
   (a H0430 „b” pontja, H1242, H7837; a felhasználó 2026-11-22-i jelzései).
2. A kapu (F231 brief 2.6): a mérési minta látható szövegében (a csukott lenyílók nélkül) nincs `||`/`‖`, `^`, 12 jegynél hosszabb
   számsor, héber szóra ragasztott magyar rag, és nincs könyvnév nélküli igehely-chip (a chipek megszűntek: a hely a szövegben áll).
3. A fordítótábla-kapu (DT897): az F231 által írt vagy átírt megjelenítő függvényekben nincs magyar betűs szövegliterál a táblán kívül.
4. Az egyezési teszt (DT-F231a (b)): a jelentések rendje a kártyán ugyanaz, mint a HAMART-001 lexikonlap 4.2-jében (a lapgen
   kártyamodellje), és a motívumot hordozó jelentés ugyanaz.
5. A héber szócsoport (`szocsoport.py`, a JOHD-validáció szabálya): a tartalék szabály a Macula-csoportosítással egyezik a teljes
   ószövetségi korpuszon.

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_szokartya_egyseges`. Adatbázis nélkül a 2., 4. és 5. pont kimarad.
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
sys.path.insert(0, D)

import szokartya_szoveg as S  # noqa: E402
import szocsoport  # noqa: E402
from feliratok import TABLA  # noqa: E402

DB = os.environ.get('PARDES_DB') or os.path.join(GY, 'pardes.db')
VAN_DB = os.path.exists(DB)
try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

MINTA = ('H1242', 'H7451', 'H3615', 'H0251', 'H7837', 'H2398', 'H0430', 'G0264', 'G3056', 'G1311', 'G2671')
HEB = 'א-תיִ-ﭏ֑-ׇ'


class SzovegAtalakitas(unittest.TestCase):
    def test_potcim_zarojele_ep(self):
        """F231.17 (az integrátori main-összevetés hibája, H8415 2.): a pótcím zárójele nem csonkul, a félbevágott zárójel kimarad."""
        self.assertEqual(S.elso_tagmondat('(mély) tenger, amely elborítja Tírust Ez 26:19 (párhuzamban: הַמַּיִם הָרַבִּים), a teofániánál'),
                         '(mély) tenger, amely elborítja Tírust')
        for be in ('x (párhuzamban: y)', '(a versben kétszer) valami: más', 'a) b (c: d'):
            t = S.elso_tagmondat(be)
            self.assertEqual(t.count('('), t.count(')'), (be, t))

    def test_rovidito_jel_a_helyen(self):
        for be, ki in (('holnap reggel ׳הַבּ Bír 6:31', 'holnap reggel הַבּ׳ Bír 6:31'),
                       ('továbbá ׳לַבּ ׳לַבּ, ugyanebben', 'továbbá לַבּ׳ לַבּ׳, ugyanebben'),
                       ('A א ׳אדני צבאות', 'A א׳ אדני צבאות'),
                       ('י׳ ׳הא הקדוש‎ 1Sám 6:20', 'י׳ הא׳ הקדוש‎ 1Sám 6:20'),
                       ('א׳ א לכמוש ׳צדנים מואב', 'א׳ א׳ לכמוש צדנים מואב'),
                       ('Num 9:21 & עַדבּֿ ׳בָּעֶרֶב‎ 9:15', 'Num 9:21 & עַד־בּ׳ בָּעֶרֶב‎ 9:15')):
            self.assertEqual(S.geresh_javit(be), ki)
            self.assertEqual(S.geresh_javit(ki), ki)                     # idempotens

    def test_parhuzam_es_ellentet(self):
        self.assertEqual(S.parhuzam('(nem || Zsolt 18:3), || שֹׁד Ámós 3:10'),
                         '(nem párhuzamos hely: Zsolt 18:3), párhuzamban: שֹׁד Ámós 3:10')
        self.assertEqual(S.szemben('és szemben לֵילוֺת-val'), 'és ellentétben: לֵילוֺת')
        self.assertEqual(S.szemben('1Sám 9:19 (szemben הַיּוֺם ma)'), '1Sám 9:19 (ellentétben: הַיּוֺם ma)')    # F231 #5: rag nélkül
        self.assertEqual(S.szemben('vele szemben áll'), 'vele szemben áll')                                   # magyar szó előtt marad

    def test_tanu_takaritas_felso_index(self):
        self.assertEqual(S.nemi_tanu('főnév hímnemű^2Móz 10:13 reggel'), 'főnév hímnemű 2Móz 10:13 reggel')
        self.assertEqual(S.nemi_tanu('főnév_79 ^2Móz 4:8'), 'főnév_79 2Móz 4:8')
        self.assertEqual(S.takarit_hu('1Sám 9:26 +, Bír 19:25 +; Ez 22:27 + stb.; a & b'),
                         '1Sám 9:26 és máshol, Bír 19:25 és máshol; Ez 22:27 és máshol; a és b')
        self.assertEqual(S.tudosjel_html('Dl^HWB, Ézs^2, <abbr title="x">LXX</abbr>^L'),
                         'Dl<sup>HWB</sup>, Ézs<sup>2</sup>, <abbr title="x">LXX</abbr><sup>L</sup>')

    def test_tagolasi_jelzo(self):
        self.assertTrue(S.paradigma('perfectum כ׳ 1Kir 6:38 és máshol'))
        self.assertTrue(S.paradigma('1. egyes szám כָּלִיתִי Zsolt 39:11'))
        self.assertFalse(S.paradigma('status constructus אֱלֹהֵי (a) személyekkel'))      # névszói jelentéspont, nem ragozási sor
        self.assertFalse(S.paradigma('uralkodók, bírák'))


class Forditotabla(unittest.TestCase):
    """DT897: az F231 által írt vagy átírt megjelenítő függvényekben nincs magyar betűs szövegliterál a fordítótáblán kívül (a
    HTML-címkék, az osztálynevek és a nem látható attribútumok nem számítanak)."""
    FUGGVENYEK = ('_ebben_html', '_szk_lxx', '_szk_mot_cimkek', '_szk_szamozas', '_szk_angol', '_szk_glossza', '_szk_meta',
                  '_szk_torzs_egyben', '_szk_torzsek', '_szakasz_cim', '_r_bdb_egyszeru', '_r_bdb_apparatus', '_r_magyar_gorog',
                  '_r_usz', '_r_ubs_dntg', '_r_par', 'par_pontossag', '_r_versszamozas', '_r_lxx_versszam', '_r_tsk', '_r_motivum',
                  '_ures_bsb', 'osszefuz', 'blokk_html', '_r_karoli_alakok', '_hu_en', '_heber_szocsoportok', '_csukva', '_r_ubs_dbh', '_r_sdbh')
    EKEZET = re.compile(r'[áéíóöőúüűÁÉÍÓÖŐÚÜŰ]')
    SZO = re.compile(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{3,}')

    def lathato(self, s):
        """A literál látható szövege: címkék nélkül, a látható attribútumok (title, aria-label) értékével; a %-helyőrzők nélkül."""
        attr = ' '.join(re.findall(r'(?:title|aria-label|alt)="([^"]*)"', s))
        t = re.sub(r'<[^>]*>', ' ', s) + ' ' + attr
        return re.sub(r'%\(?\w*\)?[sd]', ' ', t)

    def magyar_felirat(self, s):
        """Látható magyar szöveg: ékezetes betűs szó, vagy HTML-sablon látható szavakkal (az adatkulcs, a CSS-osztály és a fordítótábla
        kulcsa nem az)."""
        t = self.lathato(s)
        if '<' in s:
            return bool(self.SZO.search(t))
        return bool(self.EKEZET.search(t)) and ' ' in s.strip()

    def test_nincs_magyar_literal(self):
        src = open(os.path.join(D, 'blokkok.py'), encoding='utf-8').read()
        fa = ast.parse(src)
        hiba = []
        for node in ast.walk(fa):
            if not (isinstance(node, ast.FunctionDef) and node.name in self.FUGGVENYEK):
                continue
            kihagy = set()
            for n in ast.walk(node):
                if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant):
                    kihagy.add(id(n.value))                              # docstring, megjegyzés-literál
                if isinstance(n, ast.Raise):
                    kihagy.update(id(x) for x in ast.walk(n))           # a hibaüzenet nem felirat
            for n in ast.walk(node):
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in kihagy and self.magyar_felirat(n.value):
                    hiba.append('%s:%d %r' % (node.name, n.lineno, n.value[:60]))
        self.assertEqual(hiba, [])

    def test_minden_kulcs_a_tablaban(self):
        src = open(os.path.join(D, 'blokkok.py'), encoding='utf-8').read() + open(os.path.join(D, 'szokartya_szoveg.py'), encoding='utf-8').read()
        src += open(os.path.join(D, 'oldalak.py'), encoding='utf-8').read()
        for d in ('sablonok',):
            for f in os.listdir(os.path.join(D, d)):
                src += open(os.path.join(D, d, f), encoding='utf-8').read()
        kulcsok = set(re.findall(r"\bF\('([a-z_.]+)'", src))
        self.assertTrue(kulcsok)
        self.assertEqual(sorted(kulcsok - set(TABLA)), [])


def _latszo(html):
    """A lap látható szövege (a F232 normalizálójával), a csukott lenyílók nélkül."""
    import teszt_olvasoi_merce as M
    return '\n'.join(s for s in M.pillanatkep(html).split('\n') if not s.startswith(M.CSUKOTT_JEL))


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class Kapu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from teszt_olvaso_szerver import app_keszit
        cls.c = app_keszit('belso').test_client()

    def test_kapu_a_mintan(self):
        rag = re.compile('szemben [%s]+-v?[ae]l\\b' % HEB)              # a „szemben X-val” fordulat (a „ב-val” helyes magyar)
        for st in MINTA:
            h = self.c.get('/szo/' + st).get_data(as_text=True)
            t = _latszo(h)
            self.assertNotIn('||', t, st)
            self.assertNotIn('‖', t, st)
            self.assertNotIn('^', t, st)
            # F231.17 (DT-F231e): a doménkód és az UBS-azonosító a main szerint látható, ezért a hosszú számsor nem tiltott
            self.assertIsNone(rag.search(t), st)
            self.assertNotIn('szk-helyek', h, st)                       # a könyvnév nélküli chipek megszűntek
            # F231.17: a jelleg-címke („forrásadat”, „gépi feldolgozás”, „modell-kimenet”) a szerkesztő szabálya szerint a blokkcím
            # mellett látszik, ahogy a main-en (kapu: teszt_blokkfej.py); itt csak a belső nevek tiltottak
            for belso in ('lxx_os_etalon', 'PaRDeS olvasó'):
                self.assertNotIn(belso, t, (st, belso))

    def test_leading_geres_nincs_a_mintan(self):
        """A H0430 „b” pontjának mércéje: a rövidítőjel nem áll héber szó elején a kártya szövegében."""
        h = self.c.get('/szo/H0430').get_data(as_text=True)
        i = h.index('data-blokk="szo.bdb_apparatus"')
        kartya = _latszo(h[i:h.index('</section>', i)])
        self.assertIsNone(re.search('(?<![%s׳])׳[א-ת]' % HEB, kartya))
        self.assertIn('a Krónikák (31-szer); Dán 11:37', re.sub(r'\s+', ' ', kartya))   # a felsorolás egyben
        # a Biblia által igazolt sorrend-javítás a rövidítőjel áthelyezése előtt fut (forrás: „׳א אברהם אדני”, 1Móz 24:12)
        self.assertIn('א׳ אדני אברהם', kartya)
        self.assertNotIn('א׳ אברהם אדני', kartya)
        self.assertIn('Di', kartya)
        self.assertIn('<abbr title="A. Dillmann">Di</abbr>', h)


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class EgyezesALexikonlappal(unittest.TestCase):
    """DT-F231a (b): a kártya a lapgen modelljét a saját adatából építi; a jelentések rendje (a pontok jele) és a hordozó jelentés
    (a lapon félkövér, a kártyán `szk-van-mot`) a HAMART-001 lexikonlap 4.2-jével egyezik."""

    @classmethod
    def setUpClass(cls):
        from teszt_olvaso_szerver import app_keszit
        cls.c = app_keszit('belso').test_client()
        md = open(os.path.join(GY, 'lexikon', 'HAMART-001_TUDOMANYOS.md'), encoding='utf-8').read()
        cls.lap = {}
        for blokk in re.split(r'\n##### ', md)[1:]:
            m = re.match(r'(H\d{4}) — .* · BDB', blokk.split('\n', 1)[0])
            if not m or '**A jelentések rendje a BDB szerint**' not in blokk:
                continue
            r = blokk.split('**A jelentések rendje a BDB szerint**', 1)[1].split('**A motívum helyein', 1)[0]
            sorok, felkover = [], set()
            for sor in r.split('\n'):
                mm = re.match(r'- (\*\*)?([^\s*]+?)\\?\.?(\*\*)?(?:\s|$)', sor.strip())
                if not mm:
                    continue
                jel = mm.group(2).replace('\\', '')
                fo = jel.split('.')[0]
                if not re.fullmatch(r'\d+', fo):
                    continue
                if re.fullmatch(r'\d+', jel):
                    if sorok and int(jel) <= int(sorok[-1][0]):
                        break                                            # a következő BDB-szócikk: a kártya első szócikkével vetjük össze
                    sorok.append((jel, False))
                if mm.group(1):
                    felkover.add(fo)                                     # a hordozó alpont (10.c) a jelentését (10.) jelöli
            sorok = [(j, j in felkover) for j, _ in sorok]
            if sorok:
                cls.lap.setdefault(m.group(1), sorok)

    def kartya(self, st):
        h = self.c.get('/r/szo/' + st).get_data(as_text=True)
        tj = re.search(r'<nav class="szk-tj".*?</nav>', h, re.S)
        if not tj:
            return []
        return [(j.rstrip('.'), 'szk-van-mot' in osz) for osz, j in
                re.findall(r'<li class="szk-tj-sor([^"]*)"><a href="#bdb-0-[^"]*"><span class="szk-jelszam">([^<]*)</span>', tj.group(0))]

    def test_jelentesek_rendje_es_hordozo(self):
        self.assertGreaterEqual(len(self.lap), 3)
        for st, sorok in self.lap.items():
            k = [x for x in self.kartya(st) if re.fullmatch(r'\d+', x[0])]
            if not k:
                continue                                                 # tagolatlan vagy egyben álló törzs: nincs számozott rend
            self.assertEqual([j for j, _ in k][:len(sorok)], [j for j, _ in sorok], st)
            self.assertEqual({j for j, b in k if b} & {j for j, _ in sorok}, {j for j, b in sorok if b}, st)


@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class Szocsoport(unittest.TestCase):
    def test_tartalek_egyezik_a_maculaval(self):
        """A JOHD-validáció szabálya: a TAHOT-kiejtésből számolt tartalék csoportosítás a Macula szóazonosítóival egyezik."""
        con = sqlite3.connect('file:%s?mode=ro' % DB, uri=True)
        versek, tok, kiej, akt = [], [], [], None
        sorok = con.execute("SELECT e.igehely, e.sorszam, e.strong_nyers, e.kiejtes FROM token_eredeti e WHERE e.nyelv='H' "
                            "ORDER BY e.igehely, e.sorszam").fetchall()
        mac = {}
        for ig, xml, st in con.execute('SELECT igehely, xml_id, strong FROM token_macula ORDER BY igehely, rowid'):
            mac.setdefault(ig, []).append(xml)
        for ig, _n, st, k in sorok:
            if ig != akt:
                if akt and len(tok) == len(mac.get(akt, [])):
                    versek.append((akt, [dict(t, w=szocsoport.macula_szo(x)) for t, x in zip(tok, mac[akt])], kiej))
                akt, tok, kiej = ig, [], []
            tok.append({'s': st or ''})
            kiej.append(k or '')
        db, elter = szocsoport.szocsoport_ellenoriz(versek)
        self.assertGreater(db, 15000)
        # mért (2026-11-22): a tartalék szabály a versek 2,77%-ában tér el a Maculától (a JOHD-validáció mintáján 0); a csempe a Macula
        # azonosítóját használja, ahol van (az egész Ószövetségben), a tartalék csak a Macula-sor híján lép be
        self.assertLessEqual(len(elter) / db, 0.03, elter[:10])


if __name__ == '__main__':
    unittest.main(verbosity=2)
