"""lapgen.bemenet.kolofon — a Kolofon saját bemenetei (S8d): a lap kiadásai, átnézései és javításai (B48), a modell-
lektor kérdéslistája (B49), a közel-keleti határ motívumai (B50) és a közel-keleti összehasonlító réteg állapota (B75).

A kiadás, az átnézés és a javítás dátuma a táblában `ÉÉÉÉ.HH.NN` (vagy `ÉÉÉÉ-HH-NN`) alakú; a réteg dátumként adja
tovább, a lap alakját a sablon adja. A változás leírása és a próza modellje kézi szöveg. A lektor kérdéslistájából
(napló, nem adattábla; az adattáblába költözése a 218c-ben, a brief B49-e) csak szerkezet jön: a lektor modellje (a
„Lektor:” sor `claude-…` neve), a kérdések száma (a „Lektor kérdései” szakasz számozott tételei) és a szakasz első
dátuma.
"""
import datetime
import re

from lapgen import konfig
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import ForrasAllapot

_KIADAS_OSZLOPOK = ('id', 'kiadas', 'datum', 'valtozas', 'proza_modell')
_ATNEZES_OSZLOPOK = ('id', 'lap_commit', 'datum', 'ki')
_JAVITAS_OSZLOPOK = ('id', 'jovahagyta', 'datum')
_KOZEL_KELETI_OSZLOPOK = ('id', 'proza_emlites')
_DATUM_RX = re.compile(r'^(20\d\d)[.-](\d\d)[.-](\d\d)$')
_LEKTOR_MODELL_RX = re.compile(r'(?m)^Lektor:.*?`(claude-[\w.-]+)`')
_LEKTOR_SZAKASZ = '## Lektor kérdései'
_SZAKASZ_HATAR = '\n## '
_LEKTOR_TETEL_RX = re.compile(r'(?m)^\*\*\d+\. ')
_LEKTOR_DATUM_RX = re.compile(r'(20\d\d)-(\d\d)-(\d\d)')


def datum_ertek(b_id, ertek, hol):
    """A tábla `ÉÉÉÉ.HH.NN` (vagy `ÉÉÉÉ-HH-NN`) dátuma; BemenetHiba, ha értelmezhetetlen."""
    return _datum(b_id, ertek, hol)


def _datum(b_id, ertek, hol):
    m = _DATUM_RX.match(ertek.strip())
    if not m:
        raise BemenetHiba('%s: értelmezhetetlen dátum (%s): %r' % (b_id, hol, ertek))
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


class Kiadas:
    """Egy kiadás: a sorszáma, a dátuma, a változás leírása (kézi) és a próza modellje (kézi; None, ha a kiadás nem
    rögzíti modellnévvel)."""
    __slots__ = ('szam', 'datum', 'valtozas', 'modell')

    def __init__(self, szam, datum, valtozas, modell):
        self.szam, self.datum, self.valtozas, self.modell = szam, datum, valtozas, modell


class KiadasiAdatok:
    """A motívum kiadásai sorszám szerint, a szerzői átnézések és a szerző által jóváhagyott javítások dátumai (rendezve,
    ismétlés nélkül)."""
    __slots__ = ('kiadasok', 'atnezesek', 'javitasok')

    def __init__(self, kiadasok, atnezesek, javitasok):
        self.kiadasok, self.atnezesek, self.javitasok = tuple(kiadasok), tuple(atnezesek), tuple(javitasok)


def b48_kiadasi_adatok(b, motivum):
    """B48 — a lap kiadásai (`kiadasok.tsv`), vizuális átnézései (`lap_atnezesek.tsv`) és javításai
    (`lap_javitasok.tsv`). Az átnézésből csak a szerző átnézésének dátuma, a javításból csak a szerző által
    jóváhagyott sor dátuma jön; az átnézés `idezet` mezője (a szerző szavai) belső nyilvántartás, nem kerül ki."""
    kiadas_ut, atnezes_ut, javitas_ut = b._utvonalak('B48')
    kiadasok, latott = [], set()
    for sor in b._tabla('B48', utvonal=kiadas_ut, oszlopok=_KIADAS_OSZLOPOK).szotarak():
        if sor['id'] != motivum.kod:
            continue
        try:
            szam = int(sor['kiadas'])
        except ValueError:
            raise BemenetHiba('B48: a kiadás száma nem egész (%s: %r)' % (motivum.kod, sor['kiadas'])) from None
        if szam in latott:
            raise BemenetHiba('B48: ismétlődő kiadásszám (%s: %d)' % (motivum.kod, szam))
        latott.add(szam)
        valtozas, modell = sor['valtozas'].strip(), sor['proza_modell'].strip()
        if not valtozas:
            raise BemenetHiba('B48: a(z) %d. kiadás változásleírása üres (%s)' % (szam, motivum.kod))
        kiadasok.append(Kiadas(szam, _datum('B48', sor['datum'], 'kiadás %d' % szam),
                               b.kezi('B48', 'valtozas', valtozas),
                               b.kezi('B48', 'proza_modell', modell)
                               if modell and modell != konfig.PROZA_MODELL_KEZI else None))
    atnezesek = {_datum('B48', sor['datum'], 'átnézés')
                 for sor in b._tabla('B48', utvonal=atnezes_ut, oszlopok=_ATNEZES_OSZLOPOK).szotarak()
                 if sor['id'] == motivum.kod and sor['ki'] == konfig.SZERZO_ATNEZES}
    javitasok = {_datum('B48', sor['datum'], 'javítás')
                 for sor in b._tabla('B48', utvonal=javitas_ut, oszlopok=_JAVITAS_OSZLOPOK).szotarak()
                 if sor['id'] == motivum.kod and sor['jovahagyta'] == konfig.SZERZO_ATNEZES and sor['datum'].strip()}
    return KiadasiAdatok(sorted(kiadasok, key=lambda k: k.szam), sorted(atnezesek), sorted(javitasok))


class Lektor:
    """A modell-lektor kérdéslistája: a lektor modellje (kézi), a jelzett helyek száma és a szakasz első dátuma (None,
    ha nincs)."""
    __slots__ = ('modell', 'db', 'datum')

    def __init__(self, modell, db, datum):
        self.modell, self.db, self.datum = modell, db, datum


def b49_lektor(b, motivum):
    """B49 — a `/kiadas` lektorának kérdéslistája. Opcionális: fájl nélkül, a „Lektor:” sor modellneve vagy a „Lektor
    kérdései” szakasz nélkül, vagy kérdés nélkül None (a Kolofonban a sor nem áll)."""
    if not b._van('B49', motivum):
        return None
    szoveg = b._szoveg('B49', motivum)
    modell = _LEKTOR_MODELL_RX.search(szoveg)
    if modell is None or _LEKTOR_SZAKASZ not in szoveg:
        return None
    resz = szoveg.split(_LEKTOR_SZAKASZ, 1)[1].split(_SZAKASZ_HATAR, 1)[0]
    db = len(_LEKTOR_TETEL_RX.findall(resz))
    if not db:
        return None
    d = _LEKTOR_DATUM_RX.search(resz)
    return Lektor(b.kezi('B49', 'lektor', modell.group(1)), db,
                  datetime.date(int(d.group(1)), int(d.group(2)), int(d.group(3))) if d else None)


class KozelKeleti:
    """A motívum sora a közel-keleti határ táblájában: az értelmező szöveg közel-keleti említése (kézi; None, ha nincs)."""
    __slots__ = ('emlites',)

    def __init__(self, emlites):
        self.emlites = emlites


def b50_kozel_keleti(b, motivum):
    """B50 — a közel-keleti határ motívumai: a motívum sora, vagy None (a motívum nem érintett)."""
    for sor in b._tabla('B50', oszlopok=_KOZEL_KELETI_OSZLOPOK).szotarak():
        if sor['id'] == motivum.kod:
            emlites = sor['proza_emlites'].strip()
            return KozelKeleti(b.kezi('B50', 'proza_emlites', emlites) if emlites else None)
    return None


def b75_kozel_keleti_reteg(b):
    """B75 — az ókori közel-keleti összehasonlító réteg állapota (fájl nélküli forrás, GK-28). A Kolofon hatókör-
    mondata és a módszertani elvek bekezdése („ilyen réteg a munkában nincs”) csak „nem vizsgált” állapotban áll;
    más állapotnál a mondat hamis volna, és a Kolofon még nem olvas közel-keleti réteget: BemenetHiba."""
    try:
        allapot = ForrasAllapot(b.jegyzek_sor('B75').allapot)
    except ValueError:
        raise BemenetHiba('B75: ismeretlen jegyzék-állapot: %r' % b.jegyzek_sor('B75').allapot) from None
    if allapot is not ForrasAllapot.NEM_VIZSGALT:
        raise BemenetHiba('B75: a közel-keleti réteg állapota %s; a Kolofon hatókör-mondata csak „nem vizsgált” '
                          'állapotban igaz, más állapothoz nincs mondat' % allapot.value)
    return allapot
