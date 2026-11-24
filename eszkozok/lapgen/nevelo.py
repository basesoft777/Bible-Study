"""lapgen.nevelo — a lista- és táblaelem névelő-kapuja, a cella típusa szerint (F241.5b, D16 (c)).

A szabály (LISTA_NEVELO) egy helyen áll, itt: a forrásnév a listában és a táblacellában névelő nélkül áll („BDB-szótár
(közkincs)”, nem „a BDB-szótár (közkincs)”); a névelőt csak a folyó szöveg teszi elé. A kisbetűs „a”/„az” a
névtöredék jele; a nagybetűs „A”/„Az” mondatkezdő elem, az megengedett. Az `olvasoi_kapu.ell_lista_nevelo` a
Markdown-szövegen ugyanezt a mintát és ugyanezt az elembontást használja.

A lapgen a kész lap fajta-térképén méri (`iro.KeszSor.tartomanyok`), mert a cella típusa ott látszik, a
Markdown-szövegen nem. A névelő karakterének fajtája dönt (D16 (c)):
- idézet (`Forrasszoveg`, pl. a Károli-szó a Kulcsszó oszlopban): nem mérődik, a forrásszöveg nem írható át;
- kézi próza (`Kezi`, a szerkesztő jóváhagyott kifejezése, GK-27): nem mérődik;
- sablon (a sablonmondat, a névtábla neve, a sablon által tett névelő): BUKÁS, a lap nem íródik ki.
A kivétel a cella típusából jön, nem oszlopnév-listából.
"""
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Fajta

# a minta: a lista- vagy táblaelem (kiemelés, link vagy kód nyitójele után) kisbetűs „a”/„az” névelővel kezdődik
NEVELO_ELEM_RX = re.compile(r'^(?:\*\*|\*|\[|`)?(?:a|az)\s')
_NYITOJEL_RX = re.compile(r'(?:\*\*|\*|\[|`)?')
NEVELO_LISTA_RX = re.compile(r'^(\s*(?:[-*]|\d+\.)\s+)(.*)$')
_MEGJEGYZES_RX = re.compile(r'<!--.*?-->')
_ELVALASZTO_RX = re.compile(r'^\|[\s:|-]+\|$')
_CELLAHATAR_RX = re.compile(r'(?<!\\)\|')

# a névelő fajtája, amelyet a kapu nem mér (D16 (c))
MENTES = (Fajta.IDEZET, Fajta.PROZA)


def elemek(sor):
    """A sor lista- és táblaelemei a sorbeli kezdőhelyükkel: [(elem, kezdet)]. A HTML-megjegyzés nem része a
    látható szövegnek (a helyét szóköz tölti ki, a kezdőhelyek a nyers sorra érvényesek); a táblázat elválasztósora
    nem elem."""
    t = _MEGJEGYZES_RX.sub(lambda m: ' ' * len(m.group(0)), sor)
    eleje = len(t) - len(t.lstrip())
    s = t.strip()
    if not s:
        return []
    ki = []
    if s.startswith('|'):
        if _ELVALASZTO_RX.match(s):
            return []
        hatarok = [m.start() for m in _CELLAHATAR_RX.finditer(s)]
        if not s.endswith('|') or s.endswith('\\|'):
            hatarok.append(len(s))
        for a, b in zip(hatarok, hatarok[1:]):
            cella = s[a + 1:b]
            elem = cella.strip()
            if elem:
                ki.append((elem, eleje + a + 1 + len(cella) - len(cella.lstrip())))
        return ki
    m = NEVELO_LISTA_RX.match(t)
    if m:
        elem = m.group(2).strip()
        if elem:
            ki.append((elem, m.start(2) + len(m.group(2)) - len(m.group(2).lstrip())))
    return ki


def nevelos(elem):
    """Igaz, ha az elem kisbetűs névelővel kezdődik."""
    return bool(NEVELO_ELEM_RX.match(elem))


def nevelo_helye(elem, kezdet):
    """A névelő első betűjének helye a sorban (a nyitójel után)."""
    return kezdet + _NYITOJEL_RX.match(elem).end()


def _fajta_itt(sor, hol):
    for kezdet, veg, fajta in sor.tartomanyok:
        if kezdet <= hol < veg:
            return fajta
    return None


def mentes(sor, hol):
    """Igaz, ha a kész sor `hol` helyén álló karakter idézet vagy kézi próza (a kapu nem méri)."""
    return _fajta_itt(sor, hol) in MENTES


def mentes_fv(sorok):
    """A kész sorokból a Markdown-mérő (`olvasoi_kapu.lap_meres(..., mentes=...)`) hívható alakja: (1-től számolt
    sorszám, hely) → igaz, ha a hely idézet vagy kézi próza. A lap szövege `iro.lap_szoveg(sorok)`."""
    return lambda n, hol: 1 <= n <= len(sorok) and mentes(sorok[n - 1], hol)


def talalatok(sorok):
    """A névelős lista- és táblaelemek a kész sorokon, a mentes fajták nélkül: [(sorszám, elem)]."""
    ki = []
    for n, sor in enumerate(sorok, start=1):
        for elem, kezdet in elemek(sor.szoveg):
            if nevelos(elem) and not mentes(sor, nevelo_helye(elem, kezdet)):
                ki.append((n, elem[:80]))
    return ki


class NeveloHiba(BemenetHiba):
    """BUKÁS: sablon-eredetű lista- vagy táblaelem kisbetűs névelővel. A lap nem íródik ki."""


def kapu(nezetek):
    """A kapu a lap minden nézetén. Találatnál NeveloHiba a találatok felsorolásával."""
    hibak = ['%s %d. sor: %s' % (nezet, n, elem) for nezet, sorok in nezetek.items() for n, elem in talalatok(sorok)]
    if hibak:
        raise NeveloHiba('a lista- vagy táblaelem névelővel kezdődik (a név névelő nélkül álljon, a névelőt csak a '
                         'folyó szöveg teszi elé; D16 (c)):\n  ' + '\n  '.join(hibak))
