"""A regiszter-őr (#98 M2): a felület általa olvasott CSS-osztályai vagy a regiszterben, vagy a kizárt listán állnak.

A szerver sablonjaiban (`sablonok/*.html`) és blokkjaiban (`blokkok.py`, `oldalak.py`) használt CSS-osztályokat, valamint a
kliens (`statikus/olvaso.js`, `tervezo_statikus/tervezo.js`) `classList.add/toggle/remove` literál-osztályait összevet
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
- **JavaScript:** a `classList.add/toggle/remove` szöveg-literál argumentumai; a nem literál argumentum, a `className =` és a
  `setAttribute('class', …)` hiba (kivétel a tervező saját paneljét építő `h()` segéd a `tervezo.js`-ben).
A ki nem bontható kifejezés is hiba (az őr nem találgat), és a nem olvasott alak sem marad ki némán: a más alakú `class=`
(egyszeres idézőjel, idézőjel nélkül), a literálon belül le nem zárt attribútum (összefűzés), a Jinja-kifejezés nem literál
ága (`{{ x or 'y' }}` `x`-e) és az előző osztálynévhez tapadó kimenet hiba.
Nem olvassa: a tervező saját panelének osztályait (`tz-…`, a `tervezo.css`-ből formázva, nem az arculatból), és a csak a
stíluslapban szereplő osztályokat.

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
JS_FAJLOK = ((os.path.join(D, 'statikus', 'olvaso.js'), 'statikus/olvaso.js'),
             (os.path.join(D, 'tervezo_statikus', 'tervezo.js'), 'tervezo_statikus/tervezo.js'))
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
def _class_attributumok(szoveg, fajl='?'):
    """[(érték, eltolás)] a `class="…"` attribútumokra; a Jinja-kifejezésen belüli idézőjel nem zárja az attribútumot.
    A más alakú `class=` (egyszeres idézőjel, idézőjel nélkül, szóköz az egyenlőségjel körül) hiba: az őr nem hagyja ki némán."""
    for m in re.finditer(r'(?<![\w.-])class\s*=', szoveg):
        if not szoveg.startswith('class="', m.start()):
            raise Kibonthatatlan('nem olvasható class attribútum (csak a class="…" alak olvasható): %r (%s:%d)' % (
                szoveg[m.start():m.start() + 24], fajl, szoveg.count('\n', 0, m.start()) + 1))
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


def _jinja_alternativak(kif, fajl, sor):
    """Egy `{{ … }}` kifejezés lehetséges kimenetei: [[rész]], ahol a rész szöveg-literál vagy None (nem literál érték).
    A Jinja `~` összefűzését `+`-ként, a többit Python-kifejezésként olvassa (`a if f else b`, `a or b`); a feltétel nem
    kimenet. Ami nem így olvasható, hiba."""
    py = re.sub(r"('[^']*'|\"[^\"]*\")|~", lambda m: m.group(1) or '+', kif.strip())
    try:
        fa = ast.parse(py, mode='eval').body
    except SyntaxError:
        raise Kibonthatatlan('nem olvasható kifejezés a class attribútumban: {{%s}} (%s:%d)' % (kif.strip(), fajl, sor))

    def alt(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            return [[n.value]]
        if isinstance(n, ast.IfExp):
            return alt(n.body) + alt(n.orelse)
        if isinstance(n, ast.BoolOp):                      # `a or b` / `a and b`: bármelyik operandus lehet a kimenet
            return [r for v in n.values for r in alt(v)]
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
            return [x + y for x in alt(n.left) for y in alt(n.right)]
        return [[None]]
    return alt(fa)


def sablon_ertek(ertek, dinamikus, fajl, sor):
    """Egy `class` attribútum értékéből az osztályok: [(osztály, dinamikus-e)].

    A kifejezés nem literál része csak egy ismert dinamikus előtagot (`nezet-`, `par-`) követhet, szóköz nélkül; minden más
    nem literál kimenet (pl. a `{{ x or 'y' }}` `x`-e) hiba. Hiba az is, ha a kifejezés kimenete szóköz nélkül tapadna az előtte
    álló statikus osztálynévhez (`szo{{ 'x' }}`)."""
    ki = []
    ertek = re.sub(r'\{%.*?%\}', ' ', ertek, flags=re.S)
    poz = 0
    statikus = []
    for m in re.finditer(r'\{\{(.*?)\}\}', ertek, flags=re.S):
        elotte = ertek[poz:m.start()]
        kif = m.group(1)
        alternativak = _jinja_alternativak(kif, fajl, sor)
        if all(a == [None] for a in alternativak):
            szavak = elotte.split()
            if elotte and not elotte[-1].isspace() and szavak and szavak[-1].endswith('-') and szavak[-1] in dinamikus:
                elo = szavak[-1]
                statikus.append(' '.join(szavak[:-1]))
                ki += [(_ervenyes(elo + v, fajl, sor), True) for v in dinamikus[elo]]
            else:
                raise Kibonthatatlan('kibonthatatlan kifejezés a class attribútumban: {{%s}} (%s:%d)' % (kif.strip(), fajl, sor))
        else:
            statikus.append(elotte)
            for a in alternativak:
                valtozatok = ['']
                for resz in a:
                    if resz is not None:
                        valtozatok = [v + resz for v in valtozatok]
                        continue
                    uj = []
                    for v in valtozatok:
                        szavak = v.split()
                        elo = szavak[-1] if szavak and not v[-1].isspace() else ''
                        if not elo.endswith('-'):
                            raise Kibonthatatlan('kibonthatatlan (nem literál) ág a class attribútumban: {{%s}} (%s:%d)' % (kif.strip(), fajl, sor))
                        if elo not in dinamikus:
                            raise Kibonthatatlan('ismeretlen dinamikus előtag: %r (%s:%d)' % (elo, fajl, sor))
                        uj += [v + d for d in dinamikus[elo]]
                    valtozatok = uj
                for v in valtozatok:
                    if v and not v[0].isspace() and elotte and not elotte[-1].isspace():
                        raise Kibonthatatlan('a kifejezés kimenete az előtte álló osztálynévhez tapad: {{%s}} (%s:%d)' % (kif.strip(), fajl, sor))
                    ki += [(_ervenyes(o, fajl, sor), True) for o in v.split()]
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
        for ertek, eltolas in _class_attributumok(szoveg, 'sablonok/' + n):
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
            if isinstance(n, ast.JoinedStr) and any(isinstance(v, ast.Constant) and re.search(r'class\s*=', str(v.value)) for v in n.values):
                raise Kibonthatatlan('f-string a class attribútumban (%s:%d)' % (fajl, n.lineno))
            if not (isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search(r'(?<![\w.-])class\s*=', n.value)):
                continue
            if isinstance(getattr(n, '_szulo', None), ast.Expr) or isinstance(getattr(n, '_szulo', None), ast.JoinedStr):
                continue                                                              # docstring
            if isinstance(getattr(n, '_szulo', None), ast.Compare):
                continue                                                              # vizsgálat ('class="x' in html), nem kimenet
            # a néma kihagyás helyett hiba: más alakú class= (egyszeres idézőjel stb.), és a literálon belül le nem zárt
            # attribútum (az összefűzés: '<b class="a ' + x + '">')
            if len(re.findall(r'(?<![\w.-])class\s*=', n.value)) != len(re.findall(r'(?<![\w.-])class="[^"]*"', n.value)):
                raise Kibonthatatlan('nem olvasható vagy le nem zárt class attribútum (csak a teljes class="…" alak olvasható; '
                                     'összefűzés?): %r (%s:%d)' % (n.value[:60], fajl, n.lineno))
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
# JavaScript (a kliens által adott osztályok)
# =====================================================================================================================
_JS_LITERAL = re.compile(r"""\s*(?:'([^'\\]*)'|"([^"\\]*)")\s*""")


def js_osztalyok(utak):
    """A `classList.add/toggle/remove(…)` hívások szöveg-literál osztályai. A nem literál osztály-argumentum hiba; a
    `className =` és a `setAttribute('class', …)` is hiba (az őr nem olvassa, ezért nem hagyja ki némán). Kivétel: a
    tervező saját paneljét építő segédfüggvény (`tervezo.js` `h()`: `e.className = osztaly`), amely a tervező saját,
    `tervezo.css`-ből formázott vezérlőit adja, nem a felület elemeit."""
    ki = []
    for ut, fajl in utak:
        with open(ut, encoding='utf-8') as f:
            szoveg = f.read()
        sor = lambda i: szoveg.count('\n', 0, i) + 1
        for m in re.finditer(r'\bclassName\s*=(?!=)|setAttribute\(\s*[\'"]class[\'"]', szoveg):
            if fajl.endswith('tervezo.js') and szoveg.startswith('className = osztaly;', m.start()):
                continue
            raise Kibonthatatlan('nem olvasható osztály-hozzárendelés (csak a classList.add/toggle/remove literál-argumentuma '
                                 'olvasható): %s (%s:%d)' % (m.group(0), fajl, sor(m.start())))
        for m in re.finditer(r'\.classList\.(add|toggle|remove)\(', szoveg):
            i = m.end()
            while True:
                lm = _JS_LITERAL.match(szoveg, i)
                if not lm:
                    raise Kibonthatatlan('nem literál osztály a classList.%s hívásban (%s:%d)' % (m.group(1), fajl, sor(m.start())))
                for o in (lm.group(1) if lm.group(1) is not None else lm.group(2)).split():
                    ki.append(Elofordulas(_ervenyes(o, fajl, sor(m.start())), fajl, sor(m.start())))
                i = lm.end()
                if m.group(1) == 'toggle' or szoveg[i] == ')':           # a toggle második argumentuma a feltétel
                    break
                if szoveg[i] != ',':
                    raise Kibonthatatlan('nem olvasható classList.%s hívás (%s:%d)' % (m.group(1), fajl, sor(m.start())))
                i += 1
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


def felmeres(sablon_dir=SABLON_DIR, py_fajlok=PY_FAJLOK, biz=None, js_fajlok=None):
    """A felület osztály-előfordulásai: [Elofordulas]."""
    dinamikus = {'nezet-': list(NEZETEK), 'par-': list(biz if biz is not None else BIZONYOSSAG_TARTALEK)}
    ki, latott = [], set()
    for e in sablon_osztalyok(sablon_dir, dinamikus) + py_osztalyok(py_fajlok) + js_osztalyok(JS_FAJLOK if js_fajlok is None else js_fajlok):
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
