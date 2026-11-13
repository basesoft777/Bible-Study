"""lapgen.fo — az új lapgenerátor belépési pontja.

    python eszkozok/general.py --cel lexikon2 --id <ID> --kimenet <repón kívüli könyvtár> [--mod munka|kiadas]

A menet: bemenet megnyitása → szakaszonként számítás (lapmodell) → megjelenítés → fájl. A 218a alatt a
generátor a `lexikon/` alá nem ír: a kimenet repón kívüli könyvtár. Befagyasztott motívum `--kimenet`
nélkül kimondva kimarad; repón kívüli próbakimenetbe befagyasztott motívum is generálható (GK-30).
"""
import datetime
import enum
import hashlib
import os
import sys

from lapgen import bemenet, konfig
from lapgen.megjelenites.md.iro import Lapiro, lap_szoveg
from lapgen.szakaszok import Szakaszrend
from lapgen.szoveg import MotivumId, SzovegHiba, prov


class Mod(enum.Enum):
    MUNKA = 'munka'
    KIADAS = 'kiadas'


class Kornyezet:
    """A számítás környezete: a bemeneti munkamenet, a motívum és a mód. Állapotot nem hordoz."""
    __slots__ = ('b', 'motivum', 'mod')

    def __init__(self, b, motivum, mod):
        self.b, self.motivum, self.mod = b, motivum, mod


class Keret:
    """A megjelenítés kerete: a szókészlet, a motívum, a szakaszrend és a `ts` proveniencia."""
    __slots__ = ('ny', 'motivum', 'rend', 'ts', 'mod', 'b')

    def __init__(self, ny, motivum, rend, ts, mod, b):
        self.ny, self.motivum, self.rend, self.ts, self.mod, self.b = ny, motivum, rend, ts, mod, b


class Eredmeny:
    __slots__ = ('nezetek', 'naplo', 'festo')

    def __init__(self, nezetek, naplo, festo):
        self.nezetek, self.naplo, self.festo = nezetek, naplo, festo


def szakaszrend():
    """A szakaszrend a kész szakaszok bekötésével. Itt áll, melyik szakaszt mely modul adja."""
    rend = Szakaszrend()
    from lapgen import bekotes
    bekotes.bekot(rend)
    return rend


def _ts(datum, naplo):
    if datum is not None:
        return prov('ts={}', datum)
    h = hashlib.sha256()
    for olvasas in sorted(naplo, key=lambda o: (o.b_id, o.utvonal)):
        h.update(('%s\t%s\t%s\n' % (olvasas.b_id, olvasas.utvonal, olvasas.sha256)).encode('utf-8'))
    return prov('ts=b:{}', h.hexdigest()[:konfig.TS_HASH_JEGY])


def lap_keszit(gyoker, motivum, mod=Mod.MUNKA, datum=None, festek=False):
    """Egy motívum lapjának nézetei: {nézet: kész sorok}. Fájlt nem ír."""
    if not isinstance(motivum, MotivumId):
        raise SzovegHiba('lap_keszit(): a motívum MotivumId legyen')
    b = bemenet.Bemenet(gyoker, festek=festek)
    ny = bemenet.nyelv(b)
    rend = szakaszrend()
    korny = Kornyezet(b, motivum, mod)
    modellek = {}
    for leiro in rend.mind():
        if leiro.szamit is None:
            continue
        with b.figyel() as forrasok:
            modellek[leiro.azonosito] = (leiro.szamit(korny), frozenset(forrasok))
    keret = Keret(ny, motivum, rend, _ts(datum, b.olvasasi_naplo()), mod, b)
    nezetek = {}
    for nezet in (konfig.NEZET_TUDOMANYOS, konfig.NEZET_KIZARASOK):
        keszek = rend.keszek(nezet)
        if not keszek:
            continue
        iro = Lapiro()
        for leiro in keszek:
            modell, forrasok = modellek[leiro.azonosito]
            leiro.megjelenit(iro, modell, keret, forrasok)
        nezetek[nezet] = iro.kesz()
    return Eredmeny(nezetek, b.olvasasi_naplo(), b.festo)


def _repon_kivul(gyoker, konyvtar):
    gy = os.path.normcase(os.path.realpath(gyoker))
    k = os.path.normcase(os.path.realpath(konyvtar))
    return k != gy and not k.startswith(gy.rstrip(os.sep) + os.sep)


def _datum(szoveg):
    if not szoveg:
        return None
    return datetime.date.fromisoformat(szoveg)


def futtat(gyoker, azonosito, kimenet, mod='munka', datum=None, ki=sys.stdout):
    """A `--cel lexikon2` törzse. Kilépési kód: 0 rendben vagy kimondott kihagyás, 1 BUKÁS, 2 hívási hiba."""
    if not azonosito:
        print('  HIBA: a --cel lexikon2 --id-t kér.', file=ki)
        return 2
    try:
        motivum = MotivumId(azonosito)
        mod_ertek = Mod(mod)
    except (SzovegHiba, ValueError) as hiba:
        print('  HIBA: %s' % hiba, file=ki)
        return 2
    kivul = bool(kimenet) and _repon_kivul(gyoker, kimenet)
    if not kivul:
        if motivum in bemenet.b59_befagyasztott(bemenet.Bemenet(gyoker)):
            print('  %s: kihagyva (befagyasztott motívum; próbageneráláshoz adj repón kívüli --kimenet könyvtárat)'
                  % azonosito, file=ki)
            return 0
        print('  HIBA: a lexikon2 cél csak repón kívüli --kimenet könyvtárba ír.', file=ki)
        return 2
    try:
        eredmeny = lap_keszit(gyoker, motivum, mod_ertek, _datum(datum or os.environ.get(konfig.DATUM_VALTOZO)))
    except bemenet.BemenetHiba as hiba:
        print('  BUKÁS (%s): %s' % (azonosito, hiba), file=ki)
        return 1
    cel = os.path.join(kimenet, konfig.CEL_NEV)
    os.makedirs(cel, exist_ok=True)
    for nezet, sorok in eredmeny.nezetek.items():
        ut = os.path.join(cel, '%s_%s.md' % (azonosito, nezet))
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(lap_szoveg(sorok))
        print('  megírva: %s (%d sor)' % (ut, len(sorok)), file=ki)
    if not eredmeny.nezetek:
        print('  %s: nincs kész szakasz, fájl nem készült' % azonosito, file=ki)
    return 0
