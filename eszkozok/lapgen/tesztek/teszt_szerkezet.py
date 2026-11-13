"""Statikus (AST-) tesztek a lapgen kódján: GK-01, GK-02, GK-05, GK-08a, GK-08c, GK-12 és a rétegrend.

Ezek a tesztek a kódot olvassák, nem futtatják: azt őrzik, hogy a szabályt megkerülő kód be se kerülhessen.
"""
import ast
import re
import unittest

import kozos
from kozos import fa, forras, kodfajlok, szovegliteralok

# Adat-útvonal a kódban: csak a jegyzék saját útvonala és a regresszió két naplófájlja állhat literálként.
_UTVONAL_RX = re.compile(r'(?:^|[^A-Za-z_])(adat|konkordancia|naplok|motivumok|lexikon|tematikus_lezart|sablonok|'
                         r'motivumlog|genezis|ujszovetseg|melyelemzesek)/')
UTVONAL_KIVETEL = {
    'bemenet/jegyzek.py': {'adat/lapgen_bemenetek.tsv'},
    'regresszio.py': {'naplok/F218_referencia.tsv', 'naplok/F218_elteres_engedely.tsv'},
}
# Fájlt nyitó hívások: olvasás csak a bemeneti rétegben és a regresszióban, írás a belépési pontban.
FAJLNYITO = {'open', 'glob', 'iglob', 'listdir', 'walk', 'scandir', 'read_text', 'read_bytes', 'isfile', 'exists'}
FAJLNYITAS_ENGEDETT = {'bemenet/jegyzek.py', 'regresszio.py', 'fo.py'}

RETEGEK = ('szoveg', 'bemenet', 'szamitas', 'megjelenites')
# melyik réteg mit importálhat a lapgenből (a konfig mindenkié)
IMPORT_ENGEDETT = {
    'szoveg': set(),
    'bemenet': {'szoveg', 'bemenet'},
    'szamitas': {'szoveg', 'bemenet', 'szamitas'},
    'megjelenites': {'szoveg', 'szamitas', 'megjelenites'},
}

# A burkolók és a látható típusok konstruktorhívása csak az otthonukban állhat.
KONSTRUKTOR_OTTHON = {
    'Lathato': ('szoveg.py',), 'Proveniencia': ('szoveg.py',), 'SablonSor': ('szoveg.py', 'bemenet/'),
    'Kezi': ('bemenet/',), 'Forrasszoveg': ('bemenet/',), 'Belso': ('bemenet/',), 'Kulcs': ('bemenet/',),
    'Utvonal': ('bemenet/',), 'Nev': ('bemenet/',), 'Jel': ('megjelenites/md/iro.py',),
}
KIIRO_FUGGVENYEK = {'kiiras', 'prov_szoveg'}
KIIRAS_ENGEDETT = {'szoveg.py', 'megjelenites/md/iro.py'}
IRO = 'megjelenites/md/iro.py'
TILTOTT_METODUS = {'replace', 'translate', 'format', 'join', 'split', 'rsplit', 'splitlines', 'expandtabs',
                   'removeprefix', 'removesuffix', 'strip', 'lstrip', 'rstrip', 'partition', 'rpartition',
                   'capitalize', 'title', 'upper', 'lower', 'swapcase', 'center', 'ljust', 'rjust', 'zfill'}
TILTOTT_RE = {'sub', 'subn'}
MODELL_ALAPTIPUSOK = {'int', 'float', 'bool', 'tuple', 'frozenset', 'Optional', 'Tuple', 'FrozenSet',
                      'Lathato', 'Nev', 'Igehely', 'Proveniencia', 'Kulcs', 'Strong', 'MotivumId', 'Horgony',
                      'date', 'datetime', 'None'}


def _reteg(rel):
    elso = rel.split('/')[0]
    return elso[:-3] if elso.endswith('.py') else elso


def _lapgen_importok(rel):
    """A fájl lapgen-en belüli importjainak első szintű csomagnevei."""
    ki = set()
    for csomo in ast.walk(fa(rel)):
        if isinstance(csomo, ast.ImportFrom) and csomo.module and csomo.module.split('.')[0] == 'lapgen':
            reszek = csomo.module.split('.')
            if len(reszek) > 1:
                ki.add((reszek[1], csomo.lineno))
            else:
                ki.update((nev.name, csomo.lineno) for nev in csomo.names)
        elif isinstance(csomo, ast.Import):
            for nev in csomo.names:
                reszek = nev.name.split('.')
                if reszek[0] == 'lapgen' and len(reszek) > 1:
                    ki.add((reszek[1], csomo.lineno))
    return ki


def _hivasnev(csomo):
    f = csomo.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


class Utvonalak(unittest.TestCase):
    def test_gk01_adat_utvonal_csak_a_jegyzekbol(self):
        """GK-01: `adat/`, `konkordancia/`, `naplok/` útvonalat a kód nem tartalmaz; az útvonal a jegyzéktáblából
        jön. Kivétel a jegyzék saját útvonala és a regresszió két naplófájlja."""
        hibak = []
        for rel in kodfajlok():
            for sorszam, ertek in szovegliteralok(rel):
                if _UTVONAL_RX.search(ertek) and ertek not in UTVONAL_KIVETEL.get(rel, ()):
                    hibak.append('%s:%d %r' % (rel, sorszam, ertek[:80]))
        self.assertEqual(hibak, [])

    def test_gk01_fajlt_csak_a_bemeneti_reteg_nyit(self):
        """GK-01: fájlt nyitó hívás csak a bemeneti réteg magjában, a regresszióban és a belépési pontban áll."""
        hibak = []
        for rel in kodfajlok():
            if rel in FAJLNYITAS_ENGEDETT:
                continue
            for csomo in ast.walk(fa(rel)):
                if isinstance(csomo, ast.Call) and _hivasnev(csomo) in FAJLNYITO:
                    hibak.append('%s:%d %s()' % (rel, csomo.lineno, _hivasnev(csomo)))
        self.assertEqual(hibak, [])

    def test_gk12_a_generalt_lap_nem_bemenet(self):
        """GK-12: a jegyzék egyetlen bemenete sem mutat a `lexikon/` alá; a referenciát csak a regresszió olvassa
        (a `lexikon/` literált a GK-01 teszt őrzi a többi modulban)."""
        from lapgen.bemenet import Bemenet
        b = Bemenet(kozos.GYOKER)
        rosszak = [a for a in b.jegyzek_azonositok()
                   if any(u.strip().startswith('lexikon/') for u in b.jegyzek_sor(a).utvonal.split(';'))]
        self.assertEqual(rosszak, [])


class Jegyzek(unittest.TestCase):
    def test_gk01_bemenetenkent_egy_fuggveny(self):
        """GK-01: a jegyzék minden sorához pontosan egy `b<nn>_…` függvény tartozik a bemeneti rétegben, és
        minden ilyen függvényhez van sor; a függvény a saját B-azonosítóját használja."""
        fuggvenyek = {}
        for rel in kodfajlok('bemenet'):
            for csomo in ast.walk(fa(rel)):
                if isinstance(csomo, ast.FunctionDef) and re.match(r'^b\d\d+_', csomo.name):
                    azonosito = 'B' + re.match(r'^b(\d+)_', csomo.name).group(1)
                    self.assertNotIn(azonosito, fuggvenyek, 'két függvény ugyanarra a bemenetre: %s' % azonosito)
                    literalok = {c.value for c in ast.walk(csomo)
                                 if isinstance(c, ast.Constant) and isinstance(c.value, str)}
                    self.assertIn(azonosito, literalok, '%s nem a saját azonosítóját olvassa' % csomo.name)
                    fuggvenyek[azonosito] = csomo.name
        from lapgen.bemenet import Bemenet
        jegyzek = set(Bemenet(kozos.GYOKER).jegyzek_azonositok())
        self.assertEqual(set(fuggvenyek), jegyzek)


class NyersHozzaferes(unittest.TestCase):
    def test_gk02_nyers_fuggveny_a_bemeneten_kivul_nem_hivhato(self):
        """GK-02: a bemeneti rétegen kívül nincs `_` kezdetű (nyers) hozzáférés más objektumon, és nincs ilyen
        import. A nyers függvény így csak a bemeneti rétegből érhető el."""
        sajat = {(IRO, '_szoveg')}
        hibak = []
        for rel in kodfajlok():
            if rel.startswith('bemenet/') or rel == 'szoveg.py':
                continue
            for csomo in ast.walk(fa(rel)):
                if isinstance(csomo, ast.Attribute) and csomo.attr.startswith('_') and not csomo.attr.startswith('__'):
                    alany = csomo.value
                    if isinstance(alany, ast.Name) and alany.id in ('self', 'cls'):
                        continue
                    if (rel, csomo.attr) in sajat:
                        continue
                    hibak.append('%s:%d .%s' % (rel, csomo.lineno, csomo.attr))
                if isinstance(csomo, ast.ImportFrom) and csomo.module and csomo.module.startswith('lapgen'):
                    hibak.extend('%s:%d import %s' % (rel, csomo.lineno, n.name)
                                 for n in csomo.names if n.name.startswith('_'))
        self.assertEqual(hibak, [])


class Motivumazonosito(unittest.TestCase):
    def test_gk05_nincs_motivumazonosito_a_kodban(self):
        """GK-05: a lapgen kódjában (a tesztek kivételével) nincs motívumazonosító-alakú szöveg."""
        rx = re.compile(r'[A-Z]+-\d{3}')
        hibak = []
        for rel in kodfajlok():
            for n, sor in enumerate(forras(rel).split('\n'), start=1):
                if rx.search(sor):
                    hibak.append('%s:%d %s' % (rel, n, sor.strip()[:80]))
        self.assertEqual(hibak, [])


class Retegrend(unittest.TestCase):
    def test_retegek_egyiranyu_fuggese(self):
        """A rétegek egyirányúak: szoveg ← bemenet ← szamitas ← megjelenites. A megjelenítő a bemeneti réteget
        nem importálja (adatot nem olvas), a számítás a megjelenítőt nem."""
        hibak = []
        for rel in kodfajlok():
            reteg = _reteg(rel)
            if reteg not in IMPORT_ENGEDETT:
                continue
            for cel, sorszam in _lapgen_importok(rel):
                if cel in RETEGEK and cel not in IMPORT_ENGEDETT[reteg]:
                    hibak.append('%s:%d → %s' % (rel, sorszam, cel))
        self.assertEqual(hibak, [])


class LathatoSzabaly(unittest.TestCase):
    def test_gk08a_konstruktorhivas_csak_az_otthonaban(self):
        """GK-08a: a burkolók, a `Nev`, a `Lathato`, a `Proveniencia` és a `Jel` osztály közvetlen példányosítása
        csak az otthonában áll (a látható szöveg így csak a három konstruktoron át készülhet)."""
        hibak = []
        for rel in kodfajlok():
            for csomo in ast.walk(fa(rel)):
                if isinstance(csomo, ast.Call) and _hivasnev(csomo) in KONSTRUKTOR_OTTHON:
                    otthon = KONSTRUKTOR_OTTHON[_hivasnev(csomo)]
                    if not any(rel == o or (o.endswith('/') and rel.startswith(o)) for o in otthon):
                        hibak.append('%s:%d %s()' % (rel, csomo.lineno, _hivasnev(csomo)))
        self.assertEqual(hibak, [])

    def test_gk08a_kiiras_csak_az_iroban(self):
        """GK-08a: a `Lathato` és a `Proveniencia` szöveggé alakítása (`kiiras`, `prov_szoveg`) csak az író
        modulban áll."""
        hibak = []
        for rel in kodfajlok():
            if rel in KIIRAS_ENGEDETT:
                continue
            for csomo in ast.walk(fa(rel)):
                if isinstance(csomo, ast.Name) and csomo.id in KIIRO_FUGGVENYEK:
                    hibak.append('%s:%d %s' % (rel, csomo.lineno, csomo.id))
                if isinstance(csomo, ast.Attribute) and csomo.attr in KIIRO_FUGGVENYEK:
                    hibak.append('%s:%d .%s' % (rel, csomo.lineno, csomo.attr))
                if isinstance(csomo, ast.ImportFrom):
                    hibak.extend('%s:%d import %s' % (rel, csomo.lineno, n.name)
                                 for n in csomo.names if n.name in KIIRO_FUGGVENYEK)
        self.assertEqual(hibak, [])

    def test_gk08a_nincs_szovegatiras_a_szamitasban_es_a_megjelenitesben(self):
        """GK-08a: a `szamitas/` és a `megjelenites/` rétegben nincs szövegátíró művelet: f-string, `%`-formázás,
        `+` szövegliterállal, `format`, `replace`, `translate`, `join`, `split`, `re.sub`. Kivétel az író modul
        szerkezeti jelölése (összefűzés és `join`); átíró hívás ott sincs."""
        hibak = []
        for rel in kodfajlok('szamitas') + kodfajlok('megjelenites'):
            iro = rel == IRO
            gyoker = fa(rel)
            for csomo in ast.walk(gyoker):
                if isinstance(csomo, ast.JoinedStr):
                    hibak.append('%s:%d f-string' % (rel, csomo.lineno))
                elif isinstance(csomo, ast.BinOp) and isinstance(csomo.op, ast.Mod) \
                        and isinstance(csomo.left, ast.Constant) and isinstance(csomo.left.value, str):
                    if not _hibauzenet(csomo, gyoker):   # a kivétel üzenete nem a lap szövege
                        hibak.append('%s:%d %%-formázás' % (rel, csomo.lineno))
                elif isinstance(csomo, ast.BinOp) and isinstance(csomo.op, ast.Add) and not iro and any(
                        isinstance(o, ast.Constant) and isinstance(o.value, str) for o in (csomo.left, csomo.right)):
                    hibak.append('%s:%d szöveg-összefűzés' % (rel, csomo.lineno))
                elif isinstance(csomo, ast.Call) and isinstance(csomo.func, ast.Attribute):
                    nev = csomo.func.attr
                    alany = csomo.func.value
                    if nev in TILTOTT_RE and isinstance(alany, ast.Name) and alany.id == 're':
                        hibak.append('%s:%d re.%s' % (rel, csomo.lineno, nev))
                    elif nev in TILTOTT_METODUS and not (iro and nev == 'join'):
                        hibak.append('%s:%d .%s()' % (rel, csomo.lineno, nev))
        self.assertEqual(hibak, [])

    def test_gk08c_nincs_csere_a_megjelenitesben(self):
        """GK-08c (grep-kiegészítés): a `megjelenites/` alatt 0 `re.sub` és 0 `.replace(`."""
        hibak = []
        for rel in kodfajlok('megjelenites'):
            for n, sor in enumerate(forras(rel).split('\n'), start=1):
                if 're.sub' in sor or '.replace(' in sor:
                    hibak.append('%s:%d' % (rel, n))
        self.assertEqual(hibak, [])

    def test_gk08a_a_lapmodellben_nincs_szabad_szovegmezo(self):
        """GK-08a: a `szamitas/` adatosztályainak mezői kötött típusúak: szám, logikai, felsorolás, a `szoveg`
        modul típusai és a réteg saját osztályai. Szabad `str` mező nincs."""
        sajat = set()
        for rel in kodfajlok('szamitas'):
            sajat.update(c.name for c in ast.walk(fa(rel)) if isinstance(c, ast.ClassDef))
        hibak = []
        for rel in kodfajlok('szamitas'):
            for osztaly in ast.walk(fa(rel)):
                if not isinstance(osztaly, ast.ClassDef):
                    continue
                for mezo in osztaly.body:
                    if not isinstance(mezo, ast.AnnAssign):
                        continue
                    nevek = {n.id for n in ast.walk(mezo.annotation) if isinstance(n, ast.Name)}
                    nevek |= {n.attr for n in ast.walk(mezo.annotation) if isinstance(n, ast.Attribute)}
                    idegen = nevek - MODELL_ALAPTIPUSOK - sajat - {'datetime', 'typing'}
                    if idegen:
                        hibak.append('%s:%d %s.%s: %s' % (rel, mezo.lineno, osztaly.name,
                                                           ast.unparse(mezo.target), ', '.join(sorted(idegen))))
        self.assertEqual(hibak, [])


def _hibauzenet(csomo, gyoker):
    """Igaz, ha a `%`-formázás egy kivétel üzenete (`raise X('…' % …)`): az nem a lap szövege."""
    for szulo in ast.walk(gyoker):
        if isinstance(szulo, ast.Raise) and szulo.exc is not None:
            if any(c is csomo for c in ast.walk(szulo.exc)):
                return True
    return False


if __name__ == '__main__':
    unittest.main(verbosity=1)
