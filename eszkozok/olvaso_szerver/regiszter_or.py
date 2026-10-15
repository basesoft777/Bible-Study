"""A regiszter-őr (#98 M2): a felület minden CSS-osztálya vagy a regiszterben, vagy a kizárt listán áll.

A szerver sablonjaiban (`sablonok/*.html`) és blokkjaiban (`blokkok.py`, `oldalak.py`) használt minden CSS-osztályt összevet
a regiszterrel (`konfig/elemek.toml` [[elem]] szelektorainak osztályai) és a kizárt listával ([kizart]). Az ismeretlen osztály
hiba, az osztály és a hely megnevezésével. Így új elem csak regisztrálva vagy tudatosan kizárva kerülhet a felületre
(a #76 M3-tól elfogadási feltétel).

Olvasás:
- **sablonok:** a `class="…"` attribútumok; a `{% … %}` címkék közti szöveg osztály, a `{{ … }}` kifejezés szöveg-literáljai
  osztályok; a dinamikus előtag (`nezet-{{ nezet }}`, `' par-' ~ w.biz`) az értékkészletből bomlik ki: `nezet-` →
  `oldalak.NEZETEK`, `par-` → a `token_par` bizonyosság-értékei (a `lekerdezesek.bizonyossag_ertekek`-ből, az adatbázisból).
- **Python-modulok** (`ast`): a `class="…"`-t tartalmazó szöveg-literálok; a `%s` helyére kerülő operandus kibontva: literál,
  feltételes kifejezés literál-ágakkal, függvényparaméter (az alapértéke és a hívási helyek literál-argumentumai), vagy egy
  modulszintű szótár-literál értékeinek eleme (`JELLEG[j][1]`).
A ki nem bontható kifejezés is hiba (az őr nem találgat).

Futtatás: python regiszter_or.py [--db pardes.db]
"""
import argparse
import ast
import itertools
import os
import re
import sys
import tomllib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
SABLON_DIR = os.path.join(D, 'sablonok')
PY_FAJLOK = (os.path.join(D, 'blokkok.py'), os.path.join(D, 'oldalak.py'))
ELEMEK_UT = os.path.join(D, 'konfig', 'elemek.toml')
OSZTALY = re.compile(r'^[A-Za-z_][A-Za-z0-9_-]*$')
NEZETEK = ('olvaso', 'interlinearis', 'munkaasztal')          # = oldalak.NEZETEK (a teszt összeveti)
BIZONYOSSAG_TARTALEK = ('magas', 'alacsony')                  # csak adatbázis nélkül; a kimenet ezt jelzi


class Kibonthatatlan(ValueError):
    pass


class Elofordulas:
    __slots__ = ('osztaly', 'fajl', 'sor', 'dinamikus')

    def __init__(self, osztaly, fajl, sor, dinamikus=False):
        self.osztaly, self.fajl, self.sor, self.dinamikus = osztaly, fajl, sor, dinamikus

    def hely(self):
        return '%s:%d' % (self.fajl, self.sor)

    def __repr__(self):
        return 'Elofordulas(%r, %r)' % (self.osztaly, self.hely())


def _ervenyes(o, fajl, sor):
    if not OSZTALY.match(o):
        raise Kibonthatatlan('nem érvényes osztálynév: %r (%s:%d)' % (o, fajl, sor))
    return o


# =====================================================================================================================
# sablonok
# =====================================================================================================================
def _class_attributumok(szoveg):
    """[(érték, eltolás)] a `class="…"` attribútumokra; a Jinja-kifejezésen belüli idézőjel nem zárja az attribútumot."""
    ki = []
    for m in re.finditer(r'(?<![\w-])class="', szoveg):
        i = m.end()
        j = i
        while j < len(szoveg):
            if szoveg.startswith('{{', j):
                j = szoveg.index('}}', j) + 2
            elif szoveg.startswith('{%', j):
                j = szoveg.index('%}', j) + 2
            elif szoveg[j] == '"':
                break
            else:
                j += 1
        ki.append((szoveg[i:j], m.start()))
    return ki


def sablon_ertek(ertek, dinamikus, fajl, sor):
    """Egy `class` attribútum értékéből az osztályok: [(osztály, dinamikus-e)]."""
    ki = []
    ertek = re.sub(r'\{%.*?%\}', ' ', ertek, flags=re.S)
    poz = 0
    statikus = []
    for m in re.finditer(r'\{\{(.*?)\}\}', ertek, flags=re.S):
        elotte = ertek[poz:m.start()]
        kif = m.group(1)
        literalok = [a if a is not None else b for a, b in re.findall(r"'([^']*)'|\"([^\"]*)\"", kif)]
        if not literalok:
            szavak = elotte.split()
            if elotte and not elotte[-1].isspace() and szavak and szavak[-1].endswith('-') and szavak[-1] in dinamikus:
                elo = szavak[-1]
                statikus.append(' '.join(szavak[:-1]))
                ki += [(_ervenyes(elo + v, fajl, sor), True) for v in dinamikus[elo]]
            else:
                raise Kibonthatatlan('kibonthatatlan kifejezés a class attribútumban: {{%s}} (%s:%d)' % (kif.strip(), fajl, sor))
        else:
            statikus.append(elotte)
            for i, lit in enumerate(literalok):
                elo = lit.strip()
                if elo.endswith('-') and re.search(re.escape(lit) + r"['\"]\s*~", kif):
                    if elo not in dinamikus:
                        raise Kibonthatatlan('ismeretlen dinamikus előtag: %r (%s:%d)' % (elo, fajl, sor))
                    ki += [(_ervenyes(elo + v, fajl, sor), True) for v in dinamikus[elo]]
                else:
                    ki += [(_ervenyes(o, fajl, sor), True) for o in lit.split()]
        poz = m.end()
    statikus.append(ertek[poz:])
    ki += [(_ervenyes(o, fajl, sor), False) for o in ' '.join(statikus).split()]
    return ki


def sablon_osztalyok(sablon_dir, dinamikus):
    ki = []
    for n in sorted(os.listdir(sablon_dir)):
        if not n.endswith('.html'):
            continue
        with open(os.path.join(sablon_dir, n), encoding='utf-8') as f:
            szoveg = f.read()
        for ertek, eltolas in _class_attributumok(szoveg):
            sor = szoveg.count('\n', 0, eltolas) + 1
            for o, dyn in sablon_ertek(ertek, dinamikus, 'sablonok/' + n, sor):
                ki.append(Elofordulas(o, 'sablonok/' + n, sor, dyn))
    return ki


# =====================================================================================================================
# Python-modulok
# =====================================================================================================================
def _modul_szotarak(fa):
    """{név: ast.Dict} a modulszintű szótár-literálokra."""
    ki = {}
    for n in fa.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Dict):
            ki[n.targets[0].id] = n.value
    return ki


def _fuggvenyek(faak):
    """{függvénynév: ast.FunctionDef} az összes vizsgált modulból."""
    ki = {}
    for fa in faak:
        for n in ast.walk(fa):
            if isinstance(n, ast.FunctionDef):
                ki[n.name] = n
    return ki


def _hivasok(faak, nev):
    for fa in faak:
        for n in ast.walk(fa):
            if isinstance(n, ast.Call) and ((isinstance(n.func, ast.Name) and n.func.id == nev) or (isinstance(n.func, ast.Attribute) and n.func.attr == nev)):
                yield n


def _parameter_ertekek(fv, param, faak, fajl, sor):
    """Egy függvényparaméter lehetséges értékei: az alapértéke és a hívási helyek literál-argumentumai."""
    a = fv.args
    nevek = [x.arg for x in a.args]
    idx = nevek.index(param)
    ertekek = []
    alap_kezd = len(nevek) - len(a.defaults)
    if idx >= alap_kezd:
        d = a.defaults[idx - alap_kezd]
        if not (isinstance(d, ast.Constant) and isinstance(d.value, str)):
            raise Kibonthatatlan('a(z) %s paraméter alapértéke nem szöveg-literál (%s:%d)' % (param, fajl, sor))
        ertekek.append(d.value)
    for h in _hivasok(faak, fv.name):
        arg = None
        if idx < len(h.args):
            arg = h.args[idx]
        for kw in h.keywords:
            if kw.arg == param:
                arg = kw.value
        if arg is None:
            if idx < alap_kezd:
                raise Kibonthatatlan('a(z) %s hívása a(z) %s paraméter nélkül (%s:%d)' % (fv.name, param, fajl, sor))
            continue
        if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
            raise Kibonthatatlan('a(z) %s(%s=…) hívása nem szöveg-literállal (%s:%d)' % (fv.name, param, fajl, h.lineno))
        ertekek.append(arg.value)
    return ertekek


def _operandus(op, fv, faak, szotarak, fajl, sor):
    """Egy `%s`-operandus lehetséges szöveg-értékei."""
    if isinstance(op, ast.Constant) and isinstance(op.value, str):
        return [op.value]
    if isinstance(op, ast.IfExp):
        return _operandus(op.body, fv, faak, szotarak, fajl, sor) + _operandus(op.orelse, fv, faak, szotarak, fajl, sor)
    if isinstance(op, ast.Name) and fv is not None and op.id in [x.arg for x in fv.args.args]:
        return _parameter_ertekek(fv, op.id, faak, fajl, sor)
    # NÉV[x][i]: modulszintű szótár-literál értékeinek i-edik eleme (pl. JELLEG[j][1])
    if (isinstance(op, ast.Subscript) and isinstance(op.value, ast.Subscript) and isinstance(op.value.value, ast.Name)
            and op.value.value.id in szotarak and isinstance(op.slice, ast.Constant) and isinstance(op.slice.value, int)):
        ki = []
        for v in szotarak[op.value.value.id].values:
            if not isinstance(v, (ast.Tuple, ast.List)) or not isinstance(v.elts[op.slice.value], ast.Constant):
                raise Kibonthatatlan('a(z) %s értéke nem literál-sor (%s:%d)' % (op.value.value.id, fajl, sor))
            ki.append(v.elts[op.slice.value].value)
        return ki
    raise Kibonthatatlan('kibonthatatlan osztály-kifejezés: %s (%s:%d)' % (ast.unparse(op), fajl, sor))


def py_osztalyok(utak):
    faak, nevek = [], []
    for ut in utak:
        with open(ut, encoding='utf-8') as f:
            faak.append(ast.parse(f.read(), ut))
        nevek.append(os.path.basename(ut))
    fvek = _fuggvenyek(faak)
    ki = []
    for fa, fajl in zip(faak, nevek):
        szotarak = _modul_szotarak(fa)
        for n in ast.walk(fa):
            for ch in ast.iter_child_nodes(n):
                ch._szulo = n
        for n in ast.walk(fa):
            if isinstance(n, ast.JoinedStr) and any(isinstance(v, ast.Constant) and 'class="' in str(v.value) for v in n.values):
                raise Kibonthatatlan('f-string a class attribútumban (%s:%d)' % (fajl, n.lineno))
            if not (isinstance(n, ast.Constant) and isinstance(n.value, str) and 'class="' in n.value):
                continue
            if isinstance(getattr(n, '_szulo', None), ast.Expr) or isinstance(getattr(n, '_szulo', None), ast.JoinedStr):
                continue                                                              # docstring
            # az operandusok: Markup('…') % (…) vagy '…' % (…)
            fel = n._szulo
            if isinstance(fel, ast.Call):
                fel = fel._szulo
            operandusok = None
            if isinstance(fel, ast.BinOp) and isinstance(fel.op, ast.Mod):
                operandusok = fel.right.elts if isinstance(fel.right, ast.Tuple) else [fel.right]
            fv = n
            while fv is not None and not isinstance(fv, ast.FunctionDef):
                fv = getattr(fv, '_szulo', None)
            for m in re.finditer(r'class="([^"]*)"', n.value):
                ertek = m.group(1)
                helyek = re.findall(r'%[sd]', ertek)
                if not helyek:
                    for o in ertek.split():
                        ki.append(Elofordulas(_ervenyes(o, fajl, n.lineno), fajl, n.lineno))
                    continue
                if operandusok is None:
                    raise Kibonthatatlan('%%s a class attribútumban, %%-operandus nélkül (%s:%d)' % (fajl, n.lineno))
                alap = len(re.findall(r'%[sd]', n.value[:m.start(1)]))
                valasztek = [_operandus(operandusok[alap + k], fv, faak, szotarak, fajl, n.lineno) for k in range(len(helyek))]
                for kombi in itertools.product(*valasztek):
                    s = ertek
                    for v in kombi:
                        s = s.replace('%s', v, 1)
                    for o in s.split():
                        ki.append(Elofordulas(_ervenyes(o, fajl, n.lineno), fajl, n.lineno, True))
    return ki


# =====================================================================================================================
# az összevetés
# =====================================================================================================================
def regiszter_adat(ut=ELEMEK_UT):
    """(a regiszter szelektorainak osztályai, a kizárt lista) — közvetlenül a TOML-ból (Flask és adatbázis nélkül)."""
    with open(ut, 'rb') as f:
        adat = tomllib.load(f)
    reg = set()
    for e in adat.get('elem', []):
        s = re.sub(r'"[^"]*"|\'[^\']*\'', '""', e['szelektor'])
        reg |= set(re.findall(r'\.([A-Za-z_][\w-]*)', s))
    return reg, dict(adat.get('kizart', {}))


def bizonyossag_ertekek(db_ut):
    """A `token_par` bizonyosság-értékei az adatbázisból (a `lekerdezesek`-en át); None, ha nincs adatbázis."""
    if not db_ut or not os.path.exists(db_ut):
        return None
    import sqlite3
    sys.path.insert(0, D)
    import lekerdezesek
    con = sqlite3.connect('file:%s?mode=ro' % db_ut, uri=True)
    try:
        return lekerdezesek.bizonyossag_ertekek(con)
    finally:
        con.close()


def felmeres(sablon_dir=SABLON_DIR, py_fajlok=PY_FAJLOK, biz=None):
    """A felület osztály-előfordulásai: [Elofordulas]."""
    dinamikus = {'nezet-': list(NEZETEK), 'par-': list(biz if biz is not None else BIZONYOSSAG_TARTALEK)}
    ki, latott = [], set()
    for e in sablon_osztalyok(sablon_dir, dinamikus) + py_osztalyok(py_fajlok):
        if (e.osztaly, e.fajl, e.sor) not in latott:                 # egy helyen egy osztály egyszer (a kibontás ismételheti)
            latott.add((e.osztaly, e.fajl, e.sor))
            ki.append(e)
    return ki


def ellenoriz(elofordulasok, regiszter_osztalyok, kizart):
    """A hibák listája (üres = rendben): ismeretlen osztály a felületen; a kizárt lista elavult (a felületen nem fordul elő)
    vagy fölösleges (az osztály a regiszterben is áll) eleme."""
    hibak = []
    ismert = regiszter_osztalyok | set(kizart)
    latott = set()
    for e in elofordulasok:
        latott.add(e.osztaly)
        if e.osztaly not in ismert:
            hibak.append('ismeretlen CSS-osztály: %s (%s) — vedd fel az elemek.toml [[elem]] vagy [kizart] részébe' % (e.osztaly, e.hely()))
    for o in sorted(set(kizart) - latott):
        hibak.append('elavult kizárt osztály: %s — a felületen nem fordul elő; töröld az elemek.toml [kizart] részéből' % o)
    for o in sorted(set(kizart) & regiszter_osztalyok):
        hibak.append('a(z) %s osztály a regiszter szelektoraiban és a [kizart] listán is áll — a kizárt listáról töröld' % o)
    return hibak


def main():
    ap = argparse.ArgumentParser(description='A regiszter-őr: a felület CSS-osztályai a regiszterben vagy a kizárt listán')
    ap.add_argument('--db', default=os.environ.get('PARDES_DB') or os.path.join(os.path.dirname(os.path.dirname(D)), 'pardes.db'))
    ap.add_argument('--lista', action='store_true', help='az összes előfordulás kiírása')
    a = ap.parse_args()
    biz = bizonyossag_ertekek(a.db)
    if biz is None:
        print('figyelem: nincs adatbázis (%s); a par- értékkészlet a tartalék lista: %s' % (a.db, ', '.join(BIZONYOSSAG_TARTALEK)))
    elof = felmeres(biz=biz)
    reg, kizart = regiszter_adat()
    if a.lista:
        for e in sorted(elof, key=lambda x: (x.osztaly, x.fajl, x.sor)):
            print('%-22s %s%s' % (e.osztaly, e.hely(), ' (dinamikus)' if e.dinamikus else ''))
    hibak = ellenoriz(elof, reg, kizart)
    osztalyok = {e.osztaly for e in elof}
    print('osztály a felületen: %d (előfordulás: %d; dinamikus: %d) · a regiszterben: %d · kizárva: %d' % (
        len(osztalyok), len(elof), len({e.osztaly for e in elof if e.dinamikus}), len(osztalyok & reg), len(osztalyok & set(kizart))))
    for h in hibak:
        print(h)
    print('hiba: %d' % len(hibak))
    return 1 if hibak else 0


if __name__ == '__main__':
    sys.exit(main())
