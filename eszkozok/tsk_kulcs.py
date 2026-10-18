"""TSK-kulcs átváltó: KJV-versszám <-> Károli-versszám (F114, FELADATOK #114).

A `konkordancia/TSK_kereszthivatkozasok.tsv` mindkét kulcsa (`Igehely` és
`Kapcsolódó igehely`) KJV-számozású, a könyvnév viszont magyar. A projekt többi
adata Károli-kulcsú. Minden TSK-fogyasztó ezen a modulon át olvassa a táblát;
a nyers mezőt megkerülni tilos (E1). A dataset nem módosul: az átváltás
olvasáskor történik.

Forrás: `konkordancia/Karoli_versmegfeleltetes.tsv` (igehely_karoli ->
igehely_kjv, a könyvnév nélküli `c:v` alakban; üres KJV-érték = nincs KJV-pár,
pl. zsoltárfelirat).

Visszatérési konvenciók ("nincs pár" explicit, soha nem csendes azonosság):
  * karoli_to_kjv(k)  -> KJV-vers (str) vagy None (nincs pár)
  * kjv_to_karoli(j)  -> Károli-versek listája; üres lista = nincs pár;
                         egy KJV-vers több Károli-versre is mehet.
  * Egy Károli-vers több KJV-versből áll (összevont vers): csak az első
    KJV-vers a pár (a tábla szabálya, F91); a többi KJV-vers TSK-ja nem kerül
    a Károli-versre.

ÚSZ — KIMONDOTT KORLÁT (DT-F114b (b), N-F114a): a megfeleltetés-tábla csak az
ÓSZ-t fedi. Az ÚSZ-könyvekre az átváltó AZONOSSÁGOT ad (KJV-vers = Károli-vers).
A mért eltérés (naplok/F114_USZ_meres.md): 5 csak-KJV vers (1Kor 3:23, 2Kor
13:14, ApCsel 19:41, Róm 3:31, Róm 8:39) és 5 csak-Károli vers (3Ján 1:15, Jel
12:18, Luk 6:41, Luk 17:36, Mk 9:43), valamint a nem mért tartalmi eltolódás
(pl. Jel 12:18/13:1). A TSK ÚSZ-oldala nem ellenőrzött; a lezárás N-F114a.

ÜRES igehely_kjv (DT-F114d (b), Felhasználó 2026-10-18): az `osztaly=MT` és `forras=szamlalas` sorokra
(86 sor, LXX-hiány) a KJV-kulcs az `igehely_mt` (MT-tartalék), az 1Kir 22:46–49 kivételével
(NINCS_PAR_KIVETEL, scope=manual: ott a Károli-tartalom a KJV 22:45–48, az MT-szám eltolt párt adna). Minden más üres-KJV sor, és minden
Károli-vers, amelynek nincs sora a táblában (`nincs_sor`; pl. Hós 13–14, Én 6, 2Móz 35–36), "nincs pár"
marad: a számegyezés ott hibás párt adna (Károli Hós 14 = 10 vers, KJV = 9). A tábla pótlása: N-F54a.

ISMERT KORLÁTOK (F114.10, naplok/ELLENOR_TSK_VERSSZAM.md):
  * Körkörösség: az átváltó és a felmérő „helyes” halmaza ugyanabból a táblából jön, ezért a
    0/0 mérés a tábla hibáit nem fogja meg. A nem körkörös mérés: tsk_versszam_felmeres.py F. rész.
  * Az MT|szamlalas kivételével az üres `igehely_kjv` (75 sor) és a táblában nem szereplő
    Károli-versek „nincs pár”-ok: a main-hez képest elveszett TSK-sorok, tételesen:
    naplok/F114_elveszett_sorok.tsv.
  * Ismert táblahibák (N-F41a, N-F54a bővítés): Jón 2:1 — a Károli 2:1 a KJV 1:17-nek felel meg, a tábla
    KJV 2:1-et ad; Károli 1Kir 22:54 (= KJV 22:53), Jón 2:11 (= KJV 2:10), Ézs 3:27 (= KJV 3:26) az MT-tartalékkal
    eltolt párt kap; a szomszédos tvtms-sorok (1Kir 22:43–45, 50–53; Jón 2:10; Ézs 3:26) azonosságot adnak
    eltolt tartalomra; a KJV-pár létezik, de a tábla nem rögzíti: Károli Préd 9:21–23 = KJV 10:1–3, Jób 39:34–38 =
    KJV 40:1–5, Dán 3:31–33 = KJV 4:1–3 (ezek a KJV-versek „nincs pár”-ok), a Préd 2:26 és a Zsolt 13:6 Károli-összevonás.

A TSK-tartomány-igehelyek kibontása nem része ennek a modulnak (N-F114b).

TSV-olvasás `split('\t')`-tel (CLAUDE.md), a `csv` modul nélkül.
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')

_VERS = re.compile(r'^(.+?) (\d+):(\d+)$')
_K2J = None      # Károli-vers -> KJV-vers ('' = nincs KJV-pár)
_J2K = None      # KJV-vers -> [Károli-versek]
_KONYVEK = None  # a megfeleltetés által fedett (ÓSZ) könyvek

# Explicit "nincs pár" kivételek az MT-tartalék alól (scope=manual, F114, Felhasználó 2026-10-18):
# 1Kir 22:46–49 — a Károli-tartalom a KJV 22:45–48 (pl. Károli 22:46 = Josafát egyéb dolgai), tehát az
# MT-szám (22:46–49) eltolt KJV-párt adna. Ismert táblahiba, N-F54a.
NINCS_PAR_KIVETEL = frozenset('1Kir 22:%d' % v for v in (46, 47, 48, 49))


def _betolt():
    global _K2J, _J2K, _KONYVEK
    if _K2J is not None:
        return
    k2j, j2k, konyvek = {}, {}, set()
    with open(TABLA, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if not s.startswith('#')]
    fej = sorok[0].split('\t')
    ik, ij = fej.index('igehely_karoli'), fej.index('igehely_kjv')
    im, io_, ifo = fej.index('igehely_mt'), fej.index('osztaly'), fej.index('forras')
    for s in sorok[1:]:
        if not s:
            continue
        m = s.split('\t')
        kk = m[ik]
        b = _VERS.match(kk)
        if not b:
            continue
        konyv = b.group(1)
        konyvek.add(konyv)
        kj = m[ij].strip()
        # DT-F114d (b): MT-tartalék KIZÁRÓLAG az osztaly=MT, forras=szamlalas sorokra, ahol az
        # igehely_kjv üres (LXX-hiány; a KJV-vers létezik, számozása az MT-vel azonos).
        # Más üres-KJV sor (MT|lxx_os_etalon_f91 felirat, KEZI, KJV|lxx felirat) "nincs pár" marad.
        if not kj and m[io_] == 'MT' and m[ifo] == 'szamlalas' and m[im].strip() and kk not in NINCS_PAR_KIVETEL:
            kj = m[im].strip()
        if kj:
            kj = '%s %s' % (konyv, kj)
            k2j[kk] = kj
            j2k.setdefault(kj, []).append(kk)
        else:
            k2j[kk] = ''
    _K2J, _J2K, _KONYVEK = k2j, j2k, konyvek


def konyv(vers):
    m = _VERS.match(vers.strip())
    return m.group(1) if m else None


def fedett_konyv(vers):
    """Igaz, ha a megfeleltetés-tábla fedi a vers könyvét (ÓSZ); az ÚSZ-re hamis."""
    _betolt()
    return konyv(vers) in _KONYVEK


def karoli_to_kjv(karoli_vers):
    """Károli-vers -> KJV-vers, vagy None (nincs pár). ÚSZ: azonosság (korlát, l. docstring)."""
    _betolt()
    karoli_vers = karoli_vers.strip()
    k = konyv(karoli_vers)
    if k is None:
        return None
    if k not in _KONYVEK:
        return karoli_vers
    return _K2J.get(karoli_vers) or None


def kjv_to_karoli(kjv_vers):
    """KJV-vers -> a Károli-versek listája; üres lista = nincs pár. ÚSZ: azonosság."""
    _betolt()
    kjv_vers = kjv_vers.strip()
    k = konyv(kjv_vers)
    if k is None:
        return []
    if k not in _KONYVEK:
        return [kjv_vers]
    return list(_J2K.get(kjv_vers, []))


def megjelenites(vers):
    """'Péld 8:22' -> 'Péld 8,22' (a TSK magyar megjelenítési alakja)."""
    return re.sub(r'(\d+):(\d+)$', r'\1,\2', vers)


def forras_kjv_kulcs(karoli_vers):
    """A TSK `Igehely` mezőjében keresendő KJV-kulcs egy Károli-versre (None = nincs pár)."""
    return karoli_to_kjv(karoli_vers)


def karoli_sorok(sorok, nincs_par=None):
    """TSK-sorok (a TSV `Igehely`, `Kapcsolódó igehely`, `Votes` mezőivel) -> Károli-kulcsú sorok.

    Minden bemeneti sor a forrás- és célverse Károli-megfelelőinek szorzatára bomlik
    (általában 1 x 1). Ha a forrásnak vagy a célnak nincs Károli-párja, a sor kimarad;
    ha `nincs_par` lista, abba (sor, 'forras'|'cel') kerül, tételesen.
    A kimeneti dict az eredeti sor másolata Károli-kulccsal; a 'KJV Igehely' és
    'KJV Kapcsolódó igehely' mező az eredeti KJV-kulcsot őrzi (nyom).
    """
    for r in sorok:
        fk = kjv_to_karoli(r['Igehely'])
        if not fk:
            if nincs_par is not None:
                nincs_par.append((r, 'forras'))
            continue
        ck = kjv_to_karoli(r['Kapcsolódó igehely'])
        if not ck:
            if nincs_par is not None:
                nincs_par.append((r, 'cel'))
            continue
        for f in fk:
            for c in ck:
                o = dict(r)
                o['KJV Igehely'] = r['Igehely']
                o['KJV Kapcsolódó igehely'] = r['Kapcsolódó igehely']
                o['Igehely'] = f
                o['Kapcsolódó igehely'] = c
                o['Kapcsolódó igehely magyar megjelenítése'] = megjelenites(c)
                yield o


def karoli_index(sorok):
    """Károli-forrásvers -> [Károli-kulcsú sorok]."""
    idx = {}
    for o in karoli_sorok(sorok):
        idx.setdefault(o['Igehely'], []).append(o)
    return idx


def forras_sorok(sorok, karoli_versek, nincs_par=None):
    """A megadott Károli-forrásversek (str vagy halmaz) TSK-sorai Károli-kulcsra váltva."""
    if isinstance(karoli_versek, str):
        karoli_versek = {karoli_versek.strip()}
    karoli_versek = set(karoli_versek)
    kjv = {karoli_to_kjv(v) for v in karoli_versek}
    kjv.discard(None)
    for o in karoli_sorok((r for r in sorok if r['Igehely'] in kjv), nincs_par):
        if o['Igehely'] in karoli_versek:
            yield o
