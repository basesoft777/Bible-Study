"""lapgen.bemenet.olvasoi_indok — B76: a döntésnapló indoklásának kézzel írt olvasói alakja (F241.5b, D15 (1)).

A döntésnapló (B04) `indoklas` mezője döntési nyom (proveniencia): olvasói célból nem íródik át (D13 (b)). Ahol a
lapra kerülő indoklás belső szót („jelölt”) vagy egy fogalom második nevét hordozza („fölérendelt fogalom” a lapon
bevezetett „tágabb kör” helyett, D17 (2)), az olvasó az új tábla kézzel írt, kapuzott mondatát kapja; a kulcs a lapra kerülő indoklás-szöveg hash-e (`indok_hash`), így egy szöveg egyszer
íródik, és ha az indoklás változik, az olvasói alak nem marad elavultan a lapon (árva sor: hiba).

A lapra kerülő szöveg: van olvasói alak → az áll (Kezi, B76); nincs → az indoklás, ha átmegy a szókincs-kapun
(`lapgen.szokincs`); különben a generálás megáll a hiányzó (azonosító, igehely, hash) megnevezésével. Kimeneti
csere nincs.

A tábla kapuja betöltéskor fut: az olvasói alak átmegy a szókincs-kapun; a fölérendelt fogalomra csak a lap fejének
neve („a tágabb kör”, a sablontábla `fej.tagabb` sora) áll; minden sor a döntésnapló egy élő sorára mutat (a
motívum valamely indoklásának hash-ére).
"""
import hashlib
import re

from lapgen import szokincs
from lapgen.bemenet import dontes as dontes_be
from lapgen.bemenet.jegyzek import BemenetHiba

OSZLOPOK = ('id', 'indoklas_hash', 'olvasoi_indoklas', 'proveniencia', 'dontes_ref')
_HASH_RX = re.compile(r'[0-9a-f]{12}')
_MEZO_ELVALASZTO = ' | '
_HASH_HOSSZ = 12
_TAGABB_RX = re.compile(r'(?<!\w)tágabb\s+\w+', re.I)


def indok_hash(szoveg):
    """A lapra kerülő indoklás-szöveg kulcsa: a (két végén levágott) szöveg SHA-1-e, 12 jegy."""
    return hashlib.sha1(szoveg.strip().encode('utf-8')).hexdigest()[:_HASH_HOSSZ]


def lathato_reszek(indoklas_mezo):
    """A döntésnapló `indoklas` mezőjének azon szövegei, amelyek a lapra kerülhetnek: az első ` | ` előtti rész, és
    a 3. szakasz lebontása utáni alakja (az összesítő eleje és a szerkesztői záró mondat nélkül; `vizsgalt`)."""
    from lapgen.bemenet import vizsgalt as vizsgalt_be   # körkörös import ellen
    fo = indoklas_mezo.partition(_MEZO_ELVALASZTO)[0]
    ki = {fo.strip()}
    _n, _zaro, szoveg = vizsgalt_be.indoklas_bontas(fo)
    if szoveg.strip():
        ki.add(szoveg.strip())
    return {s for s in ki if s}


class OlvasoiIndoklasok:
    """A motívum olvasói indoklásai: hash → Kezi szöveg."""

    def __init__(self, b, motivum, alakok):
        self._b, self._motivum, self._alakok = b, motivum, alakok

    def lapra(self, szoveg, igehely):
        """(a lapra kerülő szöveg, bemenet, mező): az olvasói alak, ha van; különben az indoklás, ha átmegy a
        szókincs-kapun; különben BemenetHiba."""
        h = indok_hash(szoveg)
        if h in self._alakok:
            return self._alakok[h], 'B76', 'olvasoi_indoklas'
        talalt = szokincs.talalatok(szoveg)
        if talalt:
            raise BemenetHiba('B76: %s %s: a lapra kerülő indoklásnak nincs olvasói alakja (hash %s), és belső szót '
                              'vagy egy fogalom második nevét hordoz (%s): az adat/olvasoi_indoklasok.tsv-be kell a kézzel írt '
                              'olvasói mondat'
                              % (self._motivum.kod, igehely, h, ', '.join(sorted(set(talalt)))))
        return szoveg, 'B04', 'indoklas_kh'


def b76_olvasoi_indoklasok(b, motivum):
    """B76 — a motívum olvasói indoklásai, a tábla kapujával (l. a modul leírását)."""
    from lapgen.bemenet.nyelv import SABLON_OSZLOPOK   # körkörös import ellen
    tabla = b._tabla('B76', oszlopok=OSZLOPOK)
    fej = next((r['mondat'] for r in b._tabla('B66', oszlopok=SABLON_OSZLOPOK).szotarak() if r['kulcs'] == 'fej.tagabb'),
               None)
    tagabb = szokincs.tagabb_nev(fej)
    if tagabb is None or tagabb not in szokincs.MASODIK_NEV:
        raise BemenetHiba('B76: a fölérendelt fogalom olvasói neve (a sablontábla fej.tagabb sora: %r) nem a '
                          'szókincs-kapu bevezetett neve (lapgen/szokincs.py MASODIK_NEV)' % tagabb)
    elo = {}
    naplo = dontes_be.jeloltnaplo_tabla(b)
    i_id, i_ind = naplo.oszlop('id'), naplo.oszlop('indoklas')
    for sor in naplo.sorok:
        for resz in lathato_reszek(sor[i_ind]):
            elo.setdefault(sor[i_id], set()).add(indok_hash(resz))
    alakok, latott = {}, set()
    for sor in tabla.szotarak():
        azon, h, szoveg = sor['id'], sor['indoklas_hash'], sor['olvasoi_indoklas'].strip()
        if not _HASH_RX.fullmatch(h):
            raise BemenetHiba('B76: %s: az indoklas_hash 12 jegyű kisbetűs hexa legyen (%r)' % (azon, h))
        if (azon, h) in latott:
            raise BemenetHiba('B76: %s: ismétlődő kulcs (%s)' % (azon, h))
        latott.add((azon, h))
        if h not in elo.get(azon, set()):
            raise BemenetHiba('B76: %s: árva sor: a %s hash egyik döntésnapló-indoklásra sem mutat (az indoklás '
                              'változott: az olvasói alak elavult)' % (azon, h))
        if not szoveg:
            raise BemenetHiba('B76: %s %s: üres olvasói indoklás' % (azon, h))
        talalt = szokincs.talalatok(szoveg)
        if talalt:
            raise BemenetHiba('B76: %s %s: az olvasói indoklás belső szót vagy egy fogalom második nevét hordoz: %s'
                              % (azon, h, ', '.join(sorted(set(talalt)))))
        for m in _TAGABB_RX.finditer(szoveg):
            if not m.group(0).lower().startswith(tagabb):
                raise BemenetHiba('B76: %s %s: a fölérendelt fogalom olvasói neve a lapon „%s” (fej.tagabb), itt „%s”'
                                  % (azon, h, tagabb, m.group(0)))
        if azon == motivum.kod:
            alakok[h] = szoveg
    return OlvasoiIndoklasok(b, motivum, alakok)
