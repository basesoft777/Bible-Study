"""lapgen.bemenet.nave — a tematikus index (Nave, 1897) bemenetei a 4.12 ponthoz.

Bemenetek: B57 (a Nave-tárgymutató témái és igehelyei), B70 (a motívum döntései a témákról), B71 (a témák és
altételek magyar neve). A Nave hivatkozásai KJV-számozásúak: Károli-versekre a közös bontási szabály bontja
(`eszkozok/nave_bontas.py`), amelyhez a Septuaginta-kiadás KJV-megfeleltetése (B35) és a Károli-versmegfeleltetés
(B34) kell.

A téma angol neve a forrás szövege; a lapon csak a magyar név mögött, rámutatásra látszik. A forrás hibás
karakterkódjait (pontosvessző nélküli `&#8221`) a réteg feloldja: a szöveg betűi nem változnak, csak a kódolásuk.
"""
import collections
import hashlib
import html
import re

import nave_bontas   # közös, tiszta bontási szabály: fájlt nem olvas

from lapgen.bemenet.elofordulas import b07_karoli
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Igehely

_NAVE_OSZLOPOK = ('tema_id', 'tema', 'cimke', 'igehely')
_DONTES_OSZLOPOK = ('id', 'forras', 'tema_id', 'dontes')
_NEV_OSZLOPOK = ('tema_id', 'cimke_en', 'magyar', 'forras_hash', 'allapot')
_MEGFELELTETES_OSZLOPOK = ('igehely_karoli', 'igehely_kjv')
_LXX_OSZLOPOK = ('igehely_karoli', 'igehely_kjv', 'karoli_ok')
_LXX_SZOVEG_OSZLOP = 'szoalak'
_FELIRAT_ELTOLAS = 'zsolt_felirat_eltolas'
_FORRAS_NAVE = 'Nave'
_ELAVULT = 'elavult'
DONTES_TILTOTT, DONTES_KIVALASZTOTT, DONTES_KIZART = 'tiltott', 'kivalasztott', 'kizart'
_DONTESEK = (DONTES_TILTOTT, DONTES_KIVALASZTOTT, DONTES_KIZART)
_HTML_KOD_RX = re.compile(r'&#(\d+)(?![\d;])')


def _lxx_kjv_index(fajlok):
    """{Károli-vers: KJV-fejezet:vers} a Septuaginta-kiadás könyvfájljaiból (a Károli-versre az első sor; a
    zsoltárfelirat-eltolás sorai nélkül)."""
    index = {}
    for _utvonal, fejlec, sorok in fajlok:
        if _LXX_SZOVEG_OSZLOP not in fejlec:
            continue
        ik, ij, ok = (fejlec.index(o) for o in _LXX_OSZLOPOK)
        for mezok in sorok:
            if len(mezok) > max(ik, ij, ok) and mezok[ik] and mezok[ok] != _FELIRAT_ELTOLAS:
                index.setdefault(mezok[ik], mezok[ij])
    return index


class TemaNev:
    """Egy téma vagy altétel neve: az angol eredeti (idézhető forrásszöveg) és a magyar név (idézhető fordítás);
    a magyar név hiánya (`magyar` None): a név fordításra vár."""
    __slots__ = ('angol', 'magyar')

    def __init__(self, angol, magyar):
        self.angol, self.magyar = angol, magyar


class Nave:
    """A tematikus index a motívumhoz: a témák soronként Károli-versekre bontva, a motívum döntései és a nevek."""

    def __init__(self, b, sorok, dontesek, nevek):
        self._b, self.sorok, self.dontesek, self._nevek = b, sorok, dontesek, nevek

    def nev(self, tema_id, cimke, angol):
        """A téma (üres `cimke`) vagy az altétel neve. A magyar név csak akkor áll, ha a fordítás az angol név mai
        szövegéből készült (a tábla forrás-hash-e egyezik)."""
        feloldott = html.unescape(_HTML_KOD_RX.sub(r'&#\1;', angol or ''))
        magyar = self._nevek.get((tema_id, cimke))
        van = magyar is not None and magyar[1] == hashlib.sha1(angol.encode('utf-8')).hexdigest()
        return TemaNev(
            # magyar név mellett az angol a `title` attribútumba kerül: ott az idézőjel és a kacsacsőr kódolva áll
            self._b.forrasszoveg('B57', 'tema', html.escape(feloldott, quote=True) if van else feloldott, tema_id),
            self._b.forrasszoveg('B71', 'magyar', magyar[0], tema_id) if van else None)


def b57_nave_sorok(b):
    """B57 — a Nave-tárgymutató sorai Károli-versekre bontva: [(téma-azonosító, témanév, altétel, [Károli-vers])],
    a forrás sorrendjében; a fejezet-szintű és az értelmezhetetlen hely nem bomlik."""
    def betolt():
        megfeleltetes = b._tabla('B34', oszlopok=_MEGFELELTETES_OSZLOPOK)
        k, j = (megfeleltetes.oszlop(o) for o in _MEGFELELTETES_OSZLOPOK)
        lxx_utvonalak = b._utvonalak('B35')
        if not lxx_utvonalak:
            raise BemenetHiba('B35: a Septuaginta szövegkiadásának egyetlen fájlja sincs meg')
        racs = nave_bontas.KjvRacs([kod for kod, _szoveg in b07_karoli(b).mind()],
                                   b._nagy_index('B35', lxx_utvonalak, _lxx_kjv_index),
                                   {sor[k]: sor[j] for sor in megfeleltetes.sorok})
        nave = b._tabla('B57', oszlopok=_NAVE_OSZLOPOK).szotarak()
        bontott, _kihagyott, _n = nave_bontas.nave_bont(nave, racs)
        sorok = collections.OrderedDict()
        for i, r, vers, _tartomanyos in bontott:
            sorok.setdefault(i, (r['tema_id'], r['tema'], r.get('cimke', ''), []))[3].append(vers)
        return tuple(sorok.values())
    return b.egyszer('B57', betolt)


def b70_tema_dontesek(b, motivum):
    """B70 — a motívum döntései a tematikus index témáiról: {téma-azonosító: döntés}."""
    ki = {}
    for r in b._tabla('B70', oszlopok=_DONTES_OSZLOPOK).szotarak():
        if r['id'] == motivum.kod and r['forras'] == _FORRAS_NAVE:
            if r['dontes'] not in _DONTESEK:
                raise BemenetHiba('B70: ismeretlen döntés: %r (%s, %s)' % (r['dontes'], motivum.kod, r['tema_id']))
            ki[r['tema_id']] = r['dontes']
    return ki


def b71_tema_nevek(b):
    """B71 — a témák és altételek magyar neve: {(téma-azonosító, angol altétel): (magyar név, a forrás hash-e)}; a
    témanév sorában az altétel üres. Az elavult sor nem számít."""
    def betolt():
        return {(r['tema_id'], r['cimke_en']): (r['magyar'], r['forras_hash'])
                for r in b._tabla('B71', oszlopok=_NEV_OSZLOPOK).szotarak() if r['allapot'] != _ELAVULT}
    return b.egyszer('B71', betolt)


def nave(b, motivum):
    """A tematikus index a motívumhoz."""
    return Nave(b, b57_nave_sorok(b), b70_tema_dontesek(b, motivum), b71_tema_nevek(b))


def vers(kod):
    """A bontott Károli-vers igehelyként."""
    return Igehely(kod)
