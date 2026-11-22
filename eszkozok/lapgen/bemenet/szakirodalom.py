"""lapgen.bemenet.szakirodalom — a vitatott pontok lektorált szakirodalma (B40, `adat/vitatott_forrasok.tsv`).

Csak az ellenőrzött sor számít (üres `ellenorzes`: a lapon nem áll, a régi `vitatott_forrasok` szabálya). Az
összefoglaló kézi próza (saját szavas összefoglalás, idézet nincs). A szerző a lap mondatában a vezetéknevével áll: a
réteg ezt a mező szerkezetéből bontja (az első szerző neve, annak utolsó tagja; a régi `szakirodalom_beszur`), a
szöveget nem írja át. A 12. szakasz teljes hivatkozása (S8c) a cím, a megjelenés, a DOI és a webcím mezőt idézetként adja (a mű saját
adatai, változatlanul); a szerző teljes neve kézi, mint a vezetékneve.
"""
import datetime

from lapgen.bemenet.jegyzek import BemenetHiba

_OSZLOPOK = ('motivum', 'pont', 'szerzo', 'cim', 'megjelenes', 'ev', 'doi', 'url', 'osszefoglalo', 'lekerdezve',
             'ellenorzes')
_SZERZO_ELVALASZTO = ','


class VitatottForras:
    """Egy vitatott pont szakirodalom-sora: a pont címe (kulcs), a szerző vezetékneve (kézi; None: hiány-sor), az év,
    az összefoglaló (kézi) és a lekérdezés dátuma; a szerzős sornál a teljes hivatkozás mezői (idézet; a DOI és a
    webcím közül legalább az egyik áll)."""
    __slots__ = ('pont', 'szerzo', 'ev', 'osszefoglalo', 'lekerdezve', 'szerzo_teljes', 'cim', 'megjelenes', 'doi', 'url')

    def __init__(self, pont, szerzo, ev, osszefoglalo, lekerdezve, szerzo_teljes=None, cim=None, megjelenes=None,
                 doi=None, url=None):
        self.pont, self.szerzo, self.ev, self.osszefoglalo, self.lekerdezve = pont, szerzo, ev, osszefoglalo, lekerdezve
        self.szerzo_teljes, self.cim, self.megjelenes, self.doi, self.url = szerzo_teljes, cim, megjelenes, doi, url


def b40_vitatott_forrasok(b, motivum):
    """B40 — a motívum ellenőrzött szakirodalom-sorai, a tábla rendjében."""
    tabla = b._tabla('B40', oszlopok=_OSZLOPOK)
    ki = []
    for r in tabla.szotarak():
        if r['motivum'] != motivum.kod or not r['ellenorzes'].strip():
            continue
        try:
            lekerdezve = datetime.date.fromisoformat(r['lekerdezve'].strip())
            ev = int(r['ev']) if r['ev'].strip() else None
        except ValueError as hiba:
            raise BemenetHiba('B40: hibás dátum vagy év (%s, %s): %s' % (motivum.kod, r['pont'], hiba))
        szerzo = r['szerzo'].strip()
        if szerzo and ev is None:
            raise BemenetHiba('B40: szerzővel álló sor év nélkül (%s, %s)' % (motivum.kod, r['pont']))
        vezeteknev = szerzo.split(_SZERZO_ELVALASZTO)[0].split()[-1] if szerzo else None
        biblio = {}
        if szerzo:
            for mezo in ('cim', 'megjelenes'):
                if not r[mezo].strip():
                    raise BemenetHiba('B40: szerzővel álló sor üres `%s` mezővel (%s, %s)' % (mezo, motivum.kod, r['pont']))
            if not r['doi'].strip() and not r['url'].strip():
                raise BemenetHiba('B40: szerzővel álló sor DOI és webcím nélkül (%s, %s)' % (motivum.kod, r['pont']))
            biblio = {mezo: b.forrasszoveg('B40', mezo, r[mezo].strip(), None) if r[mezo].strip() else None
                      for mezo in ('cim', 'megjelenes', 'doi', 'url')}
            biblio['szerzo_teljes'] = b.kezi('B40', 'szerzo', szerzo)   # a vezetéknévvel egy kategória (kézi)
        ki.append(VitatottForras(
            pont=b.kulcs('B40', 'pont', r['pont'].strip()),
            szerzo=b.kezi('B40', 'szerzo', vezeteknev) if vezeteknev else None,
            ev=ev, osszefoglalo=b.kezi('B40', 'osszefoglalo', r['osszefoglalo'].strip()), lekerdezve=lekerdezve,
            **biblio))
    return tuple(ki)
