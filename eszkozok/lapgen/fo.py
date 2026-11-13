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

from lapgen import bemenet, ismetles, konfig
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet.jegyzek import NEM_FAJL
from lapgen.megjelenites.md.iro import Lapiro, lap_szoveg
from lapgen.szakaszok import Szakaszrend
from lapgen.szoveg import MotivumId, SzovegHiba, prov, prov_fuz


FEJ = 'fej'   # a lap eleje: a kritérium egyetlen teljes helye (a szakaszrend azonosítója)
ISMETLES_KIIR = 20   # ennyi ismétlődő szósort ír ki a futás; a többit megszámolja


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
    __slots__ = ('ny', 'motivum', 'rend', 'ts', 'mod', 'b', 'datum')

    def __init__(self, ny, motivum, rend, ts, mod, b, datum=None):
        self.ny, self.motivum, self.rend, self.ts, self.mod, self.b = ny, motivum, rend, ts, mod, b
        self.datum = datum   # a generálás megadott dátuma; None, ha a `ts` a bemenetek hash-éből képződik


class Eredmeny:
    """A generálás eredménye. A `figyelmeztetesek` az ismétlés-figyelő találatai a fő nézeten (nem BUKÁS)."""
    __slots__ = ('nezetek', 'naplo', 'festo', 'figyelmeztetesek')

    def __init__(self, nezetek, naplo, festo, figyelmeztetesek=()):
        self.nezetek, self.naplo, self.festo = nezetek, naplo, festo
        self.figyelmeztetesek = figyelmeztetesek


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
            modell = leiro.szamit(korny)
            if leiro.kapu is not None:
                leiro.kapu(modell)   # a szakasz kapuja a modellen fut, a megjelenítés előtt
            modellek[leiro.azonosito] = (modell, frozenset(forrasok))
    # a kritérium szövege a kapujához (a szakaszok forrásfigyelésén kívül: nem a szakasz olvasása)
    kriterium = motivum_be.kriterium_szoveg(b, motivum) if modellek and not festek else None
    keret = Keret(ny, motivum, rend, _ts(datum, b.olvasasi_naplo()), mod, b, datum)
    licencek = bemenet.b01_licencek(b) if modellek else None
    nezetek = {}
    for nezet in (konfig.NEZET_TUDOMANYOS, konfig.NEZET_KIZARASOK):
        keszek = rend.keszek(nezet)
        if not keszek:
            continue
        iro = Lapiro()
        for leiro in keszek:
            modell, forrasok = modellek[leiro.azonosito]
            leiro.megjelenit(iro, modell, keret, _forrasok(b, licencek, forrasok))
        nezetek[nezet] = iro.kesz()
    figyelmeztetesek = ()
    if not festek and konfig.NEZET_TUDOMANYOS in nezetek:
        # az ismétlés kapui a kész lap látható szövegén (festett futásban a szöveg helyén jelzőszó áll)
        lap = nezetek[konfig.NEZET_TUDOMANYOS]
        ismetles.kriterium_kapu(lap, kriterium, teljes=rend.kesz(FEJ))
        figyelmeztetesek = tuple(ismetles.ismetlesek(lap))
    return Eredmeny(nezetek, b.olvasasi_naplo(), b.festo, figyelmeztetesek)


class Forrasok:
    """Egy szakasz forrásai a valódi olvasásból (GK-07): az útvonalak és a licenccímkék, provenienciaként."""
    __slots__ = ('azonositok', 'utvonalak', 'licencek')

    def __init__(self, azonositok, utvonalak, licencek):
        self.azonositok, self.utvonalak, self.licencek = azonositok, utvonalak, licencek


def _forrasok(b, licencek, azonositok):
    utvonalak, cimkek = [], {}
    for b_id in sorted(azonositok):
        sor = b.jegyzek_sor(b_id)
        # a nem fájl-bemenet (szabálymodul) nem adatforrás: a forráslistában nem áll
        utvonalak.extend(b.utvonal_ertek(b_id, u.strip()) for u in sor.utvonal.split(';')
                         if u.strip() != NEM_FAJL)
        if sor.licenc_kulcs != '-':
            cimke = licencek.cimke(sor.licenc_kulcs)
            cimkek[cimke.ertek] = cimke
    return Forrasok(tuple(sorted(azonositok)), prov_fuz(', ', utvonalak),
                    prov_fuz(', ', [cimkek[k] for k in sorted(cimkek)]))


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
    if eredmeny.nezetek:
        # az olvasási napló a lap mellé: ebből veti össze a regresszió az olvasott bemeneteket a mércével
        with open(os.path.join(cel, konfig.NAPLO_FAJLNEV % azonosito), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\t'.join(konfig.NAPLO_OSZLOPOK) + '\n')
            for olvasas in sorted(eredmeny.naplo, key=lambda o: (o.b_id, o.utvonal)):
                f.write('%s\t%s\t%s\n' % (olvasas.b_id, olvasas.utvonal, olvasas.sha256))
    if not eredmeny.nezetek:
        print('  %s: nincs kész szakasz, fájl nem készült' % azonosito, file=ki)
    if eredmeny.figyelmeztetesek:
        print('  FIGYELMEZTETÉS (%s): %d ismétlődő szósor a látható lapon (legalább %d szó, idézeten kívül)'
              % (azonosito, len(eredmeny.figyelmeztetesek), konfig.ISMETLES_ABLAK), file=ki)
        for talalat in eredmeny.figyelmeztetesek[:ISMETLES_KIIR]:
            print('    sor %s (%d szó): %s …' % (', '.join(str(n) for n, _hol in talalat.helyek), len(talalat.szavak),
                                               ' '.join(talalat.szavak[:10])), file=ki)
    return 0
