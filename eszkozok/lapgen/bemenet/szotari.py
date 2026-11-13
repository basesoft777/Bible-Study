"""lapgen.bemenet.szotari — a „Szótári háttér” szakasz kisebb bemenetei.

Bemenetek: B52 (a szótári pontok rendje), B29 (a translationWords szócikkei), B30 (a TWOT-számok az OSHL lexikális
indexéből), B31 (a szemantikai domének: SDBH, SDGNT, és az elemzetlen bejegyzések listája), B36 (a héber szavak
versszintű görög társai a Septuagintában), B35 (a Septuaginta szavai versenként: a társulás mértékének nevezője).

A nagy szövegkiadás (B35, B36) soraiból csak az index marad meg (`Bemenet._nagy_index`).
"""
import json
import re
import unicodedata

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Strong

NYELV_GOROG, NYELV_HEBER = 'gorog', 'heber'
_SZEREP_OSZLOPOK = ('nyelv', 'sorrend', 'szerep', 'forras', 'allapot')
_NINCS = '—'
_STRONG_ELVALASZTO = '+'
_STRONG_RESZ_RX = re.compile(r'^([HAG])(\d{4})([a-f]?)$')
_ANOMALIA_TIPUS = 'jelentes_nelkul'


def nyelv_kulcs(strong):
    """A szó nyelvének kulcsa a Strong-számból."""
    return NYELV_HEBER if strong.heber else NYELV_GOROG


class Szerepek:
    """A szótári pontok rendje: nyelvenként a saját pontok, és a két nyelv közös (nyelvfüggetlen) pontjai."""

    def __init__(self, nyelvi, kozos):
        self._nyelvi, self._kozos = nyelvi, kozos

    def nyelvi(self, nyelv):
        """A nyelv saját pontjainak sorszámai, növekvő rendben."""
        return self._nyelvi.get(nyelv, ())

    def kozos(self):
        """A nyelvfüggetlen pontok sorszámai, növekvő rendben."""
        return self._kozos


def b52_szerepek(b):
    """B52 — a szótári pontok táblája. Közös (nyelvfüggetlen) az a pont, amelynek a két nyelven ugyanaz a neve, a
    forrása és az állapota; a többi a nyelv saját pontja."""
    tabla = b._tabla('B52', oszlopok=_SZEREP_OSZLOPOK)
    sorok = {}
    for sor in tabla.szotarak():
        if sor['nyelv'] not in (NYELV_GOROG, NYELV_HEBER) or not sor['sorrend'].isdigit():
            raise BemenetHiba('B52: érvénytelen sor: %s / %s' % (sor['nyelv'], sor['sorrend']))
        kulcs = (sor['nyelv'], int(sor['sorrend']))
        if kulcs in sorok:
            raise BemenetHiba('B52: ismétlődő pont: %s / %s' % kulcs)
        sorok[kulcs] = (sor['szerep'], sor['forras'], sor['allapot'])
    kozos = tuple(sorted(n for (nyelv, n), adat in sorok.items()
                         if nyelv == NYELV_GOROG and sorok.get((NYELV_HEBER, n)) == adat))
    nyelvi = {nyelv: tuple(sorted(n for (ny, n) in sorok if ny == nyelv and n not in kozos))
              for nyelv in (NYELV_GOROG, NYELV_HEBER)}
    return Szerepek(nyelvi, kozos)


class TwCikk:
    """A translationWords egy szócikke: az azonosítója, az angol címe és a kötés első Strong-száma (a fordítástábla
    kulcsa)."""
    __slots__ = ('azonosito', 'cim', 'elso_strong')

    def __init__(self, azonosito, cim, elso_strong):
        self.azonosito, self.cim, self.elso_strong = azonosito, cim, elso_strong


def b29_tw(b):
    """B29 — a translationWords szócikkei Strong-szám szerint: {Strong kódja: (TwCikk, …)}, a tábla rendjében."""
    def betolt():
        tabla = b._tabla('B29', oszlopok=('tw_id', 'cim', 'strong'))
        i, c, s = tabla.oszlop('tw_id'), tabla.oszlop('cim'), tabla.oszlop('strong')
        index = {}
        for sor in tabla.sorok:
            strongok = [x for x in sor[s].split(_STRONG_ELVALASZTO) if x]
            for strong in strongok:
                index.setdefault(strong, []).append(
                    TwCikk(sor[i], b.forrasszoveg('B29', 'cim', sor[c], sor[i]), strongok[0]))
        return {k: tuple(v) for k, v in index.items()}
    return b.egyszer('B29', betolt)


def b30_twot(b):
    """B30 — a héber szavak TWOT-számai: {Strong kódja: (szám, …)}, rendezve, ismétlés nélkül; idézhető
    forrásszövegként (a szám a forrás saját jelölése, pl. `638c`)."""
    def betolt():
        tabla = b._tabla('B30', oszlopok=('strong', 'twot'))
        s, t = tabla.oszlop('strong'), tabla.oszlop('twot')
        index = {}
        for sor in tabla.sorok:
            if sor[t] and sor[t] != _NINCS:
                index.setdefault(sor[s], set()).add(sor[t])
        return {k: tuple(b.forrasszoveg('B30', 'twot', szam, k) for szam in sorted(v)) for k, v in index.items()}
    return b.egyszer('B30', betolt)


class Domenek:
    """A szemantikai domének szavanként (a domén kódja és angol neve), és az elemzetlen bejegyzések."""

    def __init__(self, b, domenek, anomaliak):
        self._b, self._domenek, self._anomaliak = b, domenek, anomaliak

    def domenek(self, strong):
        """[(domén kódja, angol név)] a kód rendjében; a név a kód első sorából."""
        return tuple((kod, self._b.forrasszoveg('B31', 'domen', nev, strong))
                     for kod, nev in self._domenek.get(strong.kod, ()))

    def anomaliak(self, strong):
        """A szóhoz illő elemzetlen (jelentés nélküli) szótári bejegyzések belső leírása."""
        return tuple(self._b.belso('B31', 'anomalia', leiras) for leiras in self._anomaliak.get(strong.kod, ()))


def _anomalia_strongok(nyers_ertek):
    """Az elemzetlen bejegyzés Strong-részei a betűutótag nélkül, a `H`/`G` előtagra hozva (az arámi `A` előtag a
    héber szótár része)."""
    try:
        lista = json.loads(nyers_ertek)
    except (ValueError, TypeError):
        return set()
    ki = set()
    for elem in lista if isinstance(lista, list) else ():
        for resz in (elem.split(_STRONG_ELVALASZTO) if isinstance(elem, str) else ()):
            m = _STRONG_RESZ_RX.match(resz)
            if m:
                ki.add(('G' if m.group(1) == 'G' else 'H') + m.group(2))
    return ki


def b31_domenek(b):
    """B31 — a szemantikai domének (a héber és a görög UBS-szótár doménjei) és az elemzetlen bejegyzések."""
    def betolt():
        heber_ut, gorog_ut, anomalia_ut = b._utvonalak('B31')
        domenek = {}
        for utvonal in (heber_ut, gorog_ut):
            tabla = b._tabla('B31', utvonal=utvonal, oszlopok=('strong', 'domen_kod', 'domen'))
            s, k, d = tabla.oszlop('strong'), tabla.oszlop('domen_kod'), tabla.oszlop('domen')
            for sor in tabla.sorok:
                if sor[k] and sor[k] != _NINCS:
                    domenek.setdefault(sor[s], {}).setdefault(sor[k], sor[d])
        tabla = b._tabla('B31', utvonal=anomalia_ut, oszlopok=('szotar', 'entry_id', 'lemma', 'tipus', 'nyers_ertek'))
        anomaliak = {}
        for sor in tabla.szotarak():
            if sor['tipus'] != _ANOMALIA_TIPUS:
                continue
            for strong in _anomalia_strongok(sor['nyers_ertek']):
                anomaliak.setdefault(strong, []).append(
                    '%s %s %s %s' % (sor['szotar'], sor['entry_id'], sor['lemma'], sor['nyers_ertek']))
        return Domenek(b, {s: tuple(sorted(kodok.items())) for s, kodok in domenek.items()},
                       {s: tuple(v) for s, v in anomaliak.items()})
    return b.egyszer('B31', betolt)


class LxxParok:
    """A héber szavak versszintű görög társai a Septuagintában: szavanként a versek, és versenként az ott álló
    görög tartalmi szavak."""

    def __init__(self, b, szavak, proveniencia):
        self._b, self._szavak, self._proveniencia = b, szavak, proveniencia

    def versek(self, strong):
        """{vers: (görög Strong-kód, …)} a héber szóra; None, ha a táblában a szónak nincs sora."""
        return self._szavak.get(strong.kod)

    def proveniencia(self, strong):
        """A szó sorainak proveniencia-sora (az első soré), belső szövegként; None, ha nincs sora."""
        nyers = self._proveniencia.get(strong.kod)
        return self._b.belso('B36', 'proveniencia', nyers) if nyers is not None else None


def _parok_index(fajlok):
    szavak, proveniencia = {}, {}
    for utvonal, fejlec, sorok in fajlok:
        try:
            h, i, g, p = (fejlec.index(o) for o in ('heber_strong', 'igehely', 'gorog_strong', 'proveniencia'))
        except ValueError:
            raise BemenetHiba('B36 (%s): hiányzó oszlop (heber_strong, igehely, gorog_strong, proveniencia)'
                              % utvonal) from None
        for sor in sorok:
            versek = szavak.setdefault(sor[h], {})
            proveniencia.setdefault(sor[h], sor[p] if len(sor) > p else '')
            gorogok = versek.setdefault(sor[i], [])
            if sor[g]:
                gorogok.append(sor[g])
    return {s: {v: tuple(gs) for v, gs in versek.items()} for s, versek in szavak.items()}, proveniencia


def b36_lxx_parok(b):
    """B36 — a héber szavak versszintű görög társai (generált tábla a Septuaginta szövegéből)."""
    def betolt():
        szavak, proveniencia = b._nagy_index('B36', b._utvonalak('B36'), _parok_index)
        return LxxParok(b, szavak, proveniencia)
    return b.egyszer('B36', betolt)


def _versszam_index(fajlok):
    versek = {}
    for utvonal, fejlec, sorok in fajlok:
        if 'igehely_lxx' not in fejlec:
            continue   # a könyvtár segédtáblája (fejezet- és versdöntések), nem a szöveg egy könyve
        try:
            s, lxx, karoli = (fejlec.index(o) for o in ('strong', 'igehely_lxx', 'igehely_karoli'))
        except ValueError:
            raise BemenetHiba('B35 (%s): hiányzó oszlop (strong, igehely_lxx, igehely_karoli)' % utvonal) from None
        for sor in sorok:
            if len(sor) > s and sor[s].isdigit():
                versek.setdefault(int(sor[s]), set()).add(sor[lxx] or sor[karoli])
    return {Strong('G%04d' % szam).kod: len(v) for szam, v in versek.items()}


def b35_lxx_szo_versszam(b):
    """B35 — a Septuaginta minden görög szavára: hány versben áll ({görög Strong-kód: versszám}). Ez a társulás
    mértékének nevezője. A szövegkiadás könyvenkénti fájljaiból csak ez a szám marad meg."""
    def betolt():
        utvonalak = b._utvonalak('B35')
        if not utvonalak:
            raise BemenetHiba('B35: a Septuaginta szövegkiadásának egyetlen fájlja sincs meg')
        return b._nagy_index('B35', utvonalak, _versszam_index)
    return b.egyszer('B35', betolt)


_SECE_OSZLOPOK = ('Strong_padded', 'Teljes_szocikk')
_SECE_MEZO_RX = {'G': re.compile(r'\sHebrew:\s(.*?)\sDerivation:'), 'H': re.compile(r'\sGreek:\s(.*?)\sDerivation:')}
_SECE_CIMSZO_VEG = ' ('
_ALAP_HOSSZ = 5
_SZARMAZAS_RX = re.compile(r'\((G\d{4})\)')


def nfc(szoveg):
    return unicodedata.normalize('NFC', szoveg.strip())


class Sece:
    """A kétnyelvű szótár (SECE): szavanként a másik nyelvi megfelelők listája, és a szócikkek címszavai."""

    def __init__(self, b, megfelelok, cimszavak):
        self._b, self._megfelelok, self.cimszavak = b, megfelelok, cimszavak

    def megfelelok(self, strong):
        """A szó másik nyelvi megfelelői a szótár rendjében, ismétlés nélkül, idézhető forrásszövegként; None, ha a
        szótárnak nincs szócikke a szóra, vagy a szócikkben nincs megfelelő-lista."""
        lista = self._megfelelok.get(strong.kod)
        if not lista:
            return None
        return tuple(self._b.forrasszoveg('B28', 'megfelelo', szo, strong) for szo in lista)


def b28_sece(b):
    """B28 — a kétnyelvű szótár (SECE) görög és héber kötete: a görög szócikk `Hebrew:`, a héber szócikk `Greek:`
    mezőjének szólistája, és a szócikkek címszava (a szócikk szövegének eleje az első zárójelig)."""
    def betolt():
        megfelelok, cimszavak = {}, []
        for utvonal in b._utvonalak('B28'):
            tabla = b._tabla('B28', utvonal=utvonal, oszlopok=_SECE_OSZLOPOK)
            st, sz = (tabla.oszlop(o) for o in _SECE_OSZLOPOK)
            for sor in tabla.sorok:
                cimszavak.append((sor[sz].split(_SECE_CIMSZO_VEG)[0], sor[st]))
                m = _SECE_MEZO_RX[sor[st][0]].search(sor[sz]) if sor[st][:1] in _SECE_MEZO_RX else None
                if not m:
                    continue
                lista = []
                for elem in m.group(1).split(','):
                    if elem.strip() and elem.strip() not in lista:
                        lista.append(elem.strip())
                if lista:
                    megfelelok[sor[st]] = tuple(lista)
        return Sece(b, megfelelok, tuple(cimszavak))
    return b.egyszer('B28', betolt)


def b42_szarmazas(b):
    """B42 — a Strong-szótár származtatás-mezőjében hivatkozott görög Strong-szám: {Strong kódja: a hivatkozott
    Strong kódja} (a szócsalád megállapításához)."""
    def betolt():
        tabla = b._tabla('B42', oszlopok=('Strong-szám', 'Gyök/Származtatás'))
        s, g = tabla.oszlop('Strong-szám'), tabla.oszlop('Gyök/Származtatás')
        ki = {}
        for sor in tabla.sorok:
            m = _SZARMAZAS_RX.search(sor[g])
            if m:
                ki[sor[s]] = m.group(1)
        return ki
    return b.egyszer('B42', betolt)


def lemma_strong_index(b, lemmak):
    """A szóalak → Strong-számok index: a rövid szótárak lemmáiból (`lemmak`: {Strong kódja: (lemma, átírás)}) és a
    kétnyelvű szótár címszavaiból; a kulcs az alak NFC-alakja, az érték a betűutótag nélküli Strong-kódok rendezve.
    A kétnyelvű szótár megfelelő-listája csak a szóalakot adja: a Strong-szám ebből párosul (több találatnál mind)."""
    def epit():
        index = {}
        for strong, (lemma, _atiras) in lemmak.items():
            index.setdefault(nfc(lemma), set()).add(strong[:_ALAP_HOSSZ])
        for cimszo, strong in b28_sece(b).cimszavak:
            if nfc(cimszo):
                index.setdefault(nfc(cimszo), set()).add(strong[:_ALAP_HOSSZ])
        return {alak: tuple(sorted(strongok)) for alak, strongok in index.items()}
    return b.egyszer('lemma_strong_index', epit)
