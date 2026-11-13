"""A lapgen tesztjeinek közös segédei: útvonalak, a kódfájlok listája, ideiglenes mini-repó."""
import ast
import os
import shutil
import sys
import tempfile

ITT = os.path.dirname(os.path.abspath(__file__))
LAPGEN = os.path.dirname(ITT)
ESZKOZOK = os.path.dirname(LAPGEN)
GYOKER = os.path.dirname(ESZKOZOK)

if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)

MINTALAPOK = ('HAMART-001', 'ISTENTISZT-001')
REGRESSZIO_DATUM = '2026-11-13'


def kodfajlok(alkonyvtar=None, tesztek_nelkul=True):
    """A lapgen Python-fájljai repó-relatív, `/` elválasztós útvonallal (a lapgen gyökeréhez képest)."""
    ki = []
    kezdo = os.path.join(LAPGEN, alkonyvtar) if alkonyvtar else LAPGEN
    for gyoker, konyvtarak, fajlok in os.walk(kezdo):
        konyvtarak[:] = [k for k in konyvtarak if k != '__pycache__']
        for fajl in sorted(fajlok):
            if not fajl.endswith('.py'):
                continue
            rel = os.path.relpath(os.path.join(gyoker, fajl), LAPGEN).replace(os.sep, '/')
            if tesztek_nelkul and rel.startswith('tesztek/'):
                continue
            ki.append(rel)
    return sorted(ki)


def forras(rel):
    with open(os.path.join(LAPGEN, *rel.split('/')), encoding='utf-8') as f:
        return f.read()


def fa(rel):
    return ast.parse(forras(rel), filename=rel)


def szovegliteralok(rel):
    """A fájl szövegliterál-értékei a docstringek nélkül: [(sorszám, érték)]."""
    gyoker = fa(rel)
    docstringek = set()
    for csomo in ast.walk(gyoker):
        if isinstance(csomo, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            torzs = csomo.body
            if torzs and isinstance(torzs[0], ast.Expr) and isinstance(torzs[0].value, ast.Constant) \
                    and isinstance(torzs[0].value.value, str):
                docstringek.add(id(torzs[0].value))
    return [(c.lineno, c.value) for c in ast.walk(gyoker)
            if isinstance(c, ast.Constant) and isinstance(c.value, str) and id(c) not in docstringek]


class MiniRepo:
    """Ideiglenes könyvtár a megadott fájlokkal (repó-relatív útvonal → szöveg), a tesztek bemenetéhez."""

    def __init__(self, fajlok):
        self.gyoker = tempfile.mkdtemp(prefix='lapgen_teszt_')
        for rel, tartalom in fajlok.items():
            ut = os.path.join(self.gyoker, *rel.split('/'))
            os.makedirs(os.path.dirname(ut), exist_ok=True)
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(tartalom)

    def torol(self):
        shutil.rmtree(self.gyoker, ignore_errors=True)


def tsv(*sorok):
    """TSV-szöveg a sorokból; egy sor mezők sora (tuple) vagy megjegyzéssor (str)."""
    return '\n'.join(s if isinstance(s, str) else '\t'.join(s) for s in sorok) + '\n'


JEGYZEK_FEJLEC = ('id', 'utvonal', 'leiras', 'kotelezo', 'javitas', 'frissesseg', 'allapot',
                  'licenc_kulcs', 'olvasoi_nev_kulcs', 'forras')
NEVTABLA_FEJLEC = ('tipus', 'kulcs', 'olvasoi_nev', 'eredet')
SABLON_FEJLEC = ('kulcs', 'mondat', 'parameterek', 'szakasz', 'eredet', 'dontes')


def alap_minirepo(nevek=(), sablonok=(), tovabbi=None, jegyzek_sorok=()):
    """Mini-repó a három lapgen-táblával és a befagyasztás-jegyzékkel."""
    jegyzek = [JEGYZEK_FEJLEC,
               ('B59', 'adat/lap_befagyasztas.tsv', 'befagyasztott', 'igen', '-', '-', 'aktiv', '-', '-', 'manual'),
               ('B65', 'adat/olvasoi_nevtabla.tsv', 'nevtabla', 'igen', '-', '-', 'aktiv', '-', '-', 'manual'),
               ('B66', 'adat/lapgen_sablonok.tsv', 'sablonok', 'igen', '-', '-', 'aktiv', '-', '-', 'manual'),
               ('B68', 'adat/lapgen_bemenetek.tsv', 'jegyzek', 'igen', '-', '-', 'aktiv', '-', '-', 'manual')]
    jegyzek.extend(jegyzek_sorok)
    fajlok = {
        'adat/lapgen_bemenetek.tsv': tsv('# teszt', *jegyzek),
        'adat/lap_befagyasztas.tsv': tsv(('id', 'ok', 'dontes', 'datum'), ('FAGYOTT-001', 'ok', 'd', '2026-11-12')),
        'adat/olvasoi_nevtabla.tsv': tsv(NEVTABLA_FEJLEC, *nevek),
        'adat/lapgen_sablonok.tsv': tsv(SABLON_FEJLEC, *sablonok),
    }
    fajlok.update(tovabbi or {})
    return MiniRepo(fajlok)
