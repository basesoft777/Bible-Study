"""lapgen.bemenet.irodalom — a 12. szakasz (Irodalom és idézés) forráslistájának bemeneti oldala (S8c).

A lista a számozott szakaszok valódi olvasásaiból áll (GK-07; DT-F a forráslistáról): a hívó a B-azonosítókat adja, a
réteg a jegyzékből fájlonként felsorolja őket, a jegyzék `irodalom` oszlopa szerint (`-`: a generátor saját
infrastruktúrája, a listán nem áll). A fájl olvasói neve a névtáblából jön, kulcsa a fájl jegyzékbeli útvonala:
szótárfájlnál az `irod_szotar` (a szótár teljes neve) és az `irod_szotar_forras` (a fájl neve névelővel), adatfájlnál
az `irod_adat` (listaelem-alak). Név híján a generálás megáll (GK-23). A licenc a jegyzék `licenc_kulcs`-a szerint a
licencleltárból (B01) jön, idézetként.

A generátor által nem olvasott, de az adatsorokban megnevezett külső forrás (az ókori fordítások táblájának Vulgata-
sorai, a tanúk forrása) a `kulso_forrasok` adja: csak az ellenőrzött sorokból, és csak ha a tábla a lap valamelyik
számozott szakaszának olvasásai között áll.
"""
from lapgen import konfig
from lapgen.bemenet import hatastortenet as ht_be
from lapgen.bemenet.alap import b01_licencek
from lapgen.bemenet.jegyzek import IRODALOM_NINCS, NEM_FAJL, BemenetHiba
from lapgen.bemenet.nyelv import b65_nevtabla
from lapgen.ertekek import IrodLicenc, TanuForras

NEV_SZOTAR, NEV_SZOTAR_FORRAS, NEV_ADAT, NEV_KULSO = 'irod_szotar', 'irod_szotar_forras', 'irod_adat', 'irod_kulso'
_JEGYZEK_ELVALASZTO = ';'
B_OKORI, B_TANUK = 'B38', 'B39'


class IrodFajl:
    """Egy listázandó fájl. A `rend`, a `csoport` és a `forras_csoport` belső érték (sorrend; a sor összevonása a név
    szerint; a szótárfájl névelős nevének egyszeri kiírása), a lapra nem kerül."""
    __slots__ = ('b_id', 'kulcs', 'szotar', 'licenc', 'cimke', 'rend', 'csoport', 'forras_csoport')

    def __init__(self, b_id, kulcs, szotar, licenc, cimke, rend, csoport, forras_csoport=None):
        self.b_id, self.kulcs, self.szotar, self.licenc, self.cimke = b_id, kulcs, szotar, licenc, cimke
        self.rend, self.csoport, self.forras_csoport = rend, csoport, forras_csoport


def irodalom_fajlok(b, azonositok):
    """A megadott B-azonosítók listázandó fájljai, az útvonal szerinti rendben."""
    nyers = b65_nevtabla(b)
    szotarnev = nyers.nyers_nevek(NEV_SZOTAR)
    szotarforras = nyers.nyers_nevek(NEV_SZOTAR_FORRAS)
    adatnev = nyers.nyers_nevek(NEV_ADAT)
    licencek = b01_licencek(b)
    ki = []
    for b_id in sorted(azonositok):
        sor = b.jegyzek_sor(b_id)
        if sor.irodalom == IRODALOM_NINCS:
            continue
        if sor.licenc_kulcs == '-':
            raise BemenetHiba('%s: a 12. szakasz listáján álló bemenet licenc-kulcs nélkül' % b_id)
        cimke = licencek.cimke(sor.licenc_kulcs)
        for ut in (u.strip() for u in sor.utvonal.split(_JEGYZEK_ELVALASZTO)):
            if ut == NEM_FAJL:
                continue
            szotar = ut in szotarnev
            if szotar == (ut in adatnev) or (szotar and ut not in szotarforras):
                raise BemenetHiba('%s: a(z) %s fájlnak a névtáblában pontosan egy neve legyen: szótárként (%s és %s) '
                                  'vagy adatforrásként (%s)' % (b_id, ut, NEV_SZOTAR, NEV_SZOTAR_FORRAS, NEV_ADAT))
            ki.append(IrodFajl(b_id, b.kulcs(b_id, 'utvonal', ut), szotar, IrodLicenc(sor.irodalom), cimke,
                               rend=ut, csoport=szotarnev[ut] if szotar else adatnev[ut],
                               forras_csoport=szotarforras[ut] if szotar else None))
    return sorted(ki, key=lambda f: f.rend)


class KulsoForras:
    """A generátor által nem olvasott külső forrás: a kulcs (névtábla `irod_kulso`) és a licenc."""
    __slots__ = ('kulcs', 'licenc', 'cimke')

    def __init__(self, kulcs, licenc, cimke):
        self.kulcs, self.licenc, self.cimke = kulcs, licenc, cimke


def kulso_forrasok(b, motivum, azonositok):
    """A külső források a kulcsuk rendjében: a Vulgata az ókori fordítások ellenőrzött soraiból (B38), a tanúk forrásai
    a tanúk ellenőrzött soraiból (B39), ha a tábla az `azonositok` között áll."""
    kulcsok = set()
    if B_OKORI in azonositok:
        kulcsok.update(s.forras for s in ht_be.okori_sorok(b, motivum)
                       if s.ellenorzott and s.forras in konfig.IROD_KULSO_LICENC)
    if B_TANUK in azonositok:
        for t in ht_be.b39_tanuk(b, motivum):
            if not t.ellenorzott:
                continue
            if t.forras.value not in konfig.IROD_KULSO_LICENC:
                raise BemenetHiba('B39: a(z) %r tanú-forrásnak nincs licenckulcsa (konfig.IROD_KULSO_LICENC)'
                                  % t.forras.value)
            kulcsok.add(t.forras.value)
    nevek = b65_nevtabla(b).nyers_nevek(NEV_KULSO)
    licencek = b01_licencek(b)
    ki = []
    for k in sorted(kulcsok):
        if k not in nevek:
            raise BemenetHiba('a(z) %r külső forrásnak nincs `%s` névtábla-sora' % (k, NEV_KULSO))
        lk = konfig.IROD_KULSO_LICENC[k]
        ki.append(KulsoForras(b.kulcs(B_TANUK if k in {f.value for f in TanuForras} else B_OKORI, 'forras', k),
                              IrodLicenc.LICENC if lk else IrodLicenc.CHAIN_LINEAGE,
                              licencek.cimke(lk) if lk else None))
    return ki
