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
    a Károli-versre (N-F117b, l. az ISMERT KORLÁTOK-at).
  * Két Károli-vers egy KJV-versen (DT-F117c (3) (a)): mindkét Károli-vers
    ugyanazt a KJV-verset kapja; a kjv_to_karoli() mindkettőt adja (1Kir 22:43–44
    = KJV 22:43; 1Sám 20:42–43 = KJV 20:42).

ÚSZ — KIMONDOTT KORLÁT (DT-F114b (b), N-F114a): a megfeleltetés-tábla csak az
ÓSZ-t fedi. Az ÚSZ-könyvekre az átváltó AZONOSSÁGOT ad (KJV-vers = Károli-vers).
A mért eltérés (naplok/F114_USZ_meres.md): 5 csak-KJV vers (1Kor 3:23, 2Kor
13:14, ApCsel 19:41, Róm 3:31, Róm 8:39) és 5 csak-Károli vers (3Ján 1:15, Jel
12:18, Luk 6:41, Luk 17:36, Mk 9:43), valamint a nem mért tartalmi eltolódás
(pl. Jel 12:18/13:1). A TSK ÚSZ-oldala nem ellenőrzött; a lezárás N-F114a.

ÜRES igehely_kjv (DT-F114d (b), Felhasználó 2026-10-18): az `osztaly=MT` és `forras=szamlalas` sorokra
(LXX-hiány) a KJV-kulcs az `igehely_mt` (MT-tartalék). Minden más üres-KJV sor, és minden Károli-vers, amelynek
nincs sora a táblában (`nincs_sor`), "nincs pár" marad: a számegyezés hibás párt adhatna.
F117 (DT-F117a–e): a tábla A–D′ osztályú hibái (13 hiányzó fejezet, a KEZI-, Dán 3- és eltolt párok) a
`konkordancia/Karoli_versmegfeleltetes_javitas.tsv` szerint javítva (versenkénti szöveg-összevetés,
naplok/F117_itelet.tsv), ezért a NINCS_PAR_KIVETEL (F114, DT200) üres: a kivétel oka megszűnt.

ISMERT KORLÁTOK (F114.10, naplok/ELLENOR_TSK_VERSSZAM.md; F117):
  * Körkörösség: az átváltó és a tábla-alapú „helyes” halmaz ugyanabból a táblából jön. A nem körkörös
    mérés referenciája a versenkénti szöveg-összevetés (naplok/F117_itelet.tsv): tsk_versszam_felmeres.py G. rész.
  * Egy-a-többhöz (DT-F117c (3) (a)): a KJV 1Kir 22:43 két Károli-versre (22:43, 22:44), a KJV 1Sám 20:42 két
    Károli-versre (20:42, 20:43) mutat; a TSK-sor mindkét Károli-versre rákerül (a KJV-vers mindkét felét fedi).
  * Visszairányú veszteség (N-F117b): ahol a Károli-vers két KJV-verset von össze (Hós 1:11, Jób 16:22,
    Péld 11:31, Jób 36:33, Ézs 64:1, és a régi Préd 2:26, Zsolt 13:6), a második KJV-vers (pl. KJV Hós 2:1,
    Jób 17:1, Péld 12:1, Jób 37:1, Ézs 64:2) kjv_to_karoli()-ja üres: a TSK-sorai elvesznek.
  * Versfél-korlát (N-F117c): a szöveg-összevetés a KJV-oldalt csak a Strong-címkézett szavakból olvasta; a
    versfélen, mondathatáron vagy fejezetváltón múló 28 pár a teljes KJV-szövegen újraellenőrizendő.
  * Tábla-lyuk az F117 halmazán kívül: a Préd 9:1–2 és a Jób 39:1–3 Károli-versnek nincs sora (nincs pár);
    l. naplok/F117_javitas_jelentes.md 5. pont.

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

# Explicit "nincs pár" kivételek (scope=manual). Az F114 (DT200) kivételei (1Kir 22:46–49, Ézs 3:1–26,
# Jón 2:2–10, 1Sám 24:1–22) az F117-ben megszűntek: a tábla ott a versenkénti szöveg-összevetés szerinti párt
# adja (DT-F117a–e, konkordancia/Karoli_versmegfeleltetes_javitas.tsv). Új kivétel csak döntéssel kerülhet ide.
NINCS_PAR_KIVETEL = frozenset()


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
        if kk in NINCS_PAR_KIVETEL:
            k2j[kk] = ''   # explicit "nincs pár" (scope=manual), a tábla értékétől függetlenül
            continue
        # DT-F114d (b): MT-tartalék KIZÁRÓLAG az osztaly=MT, forras=szamlalas sorokra, ahol az
        # igehely_kjv üres (LXX-hiány; a KJV-vers létezik, számozása az MT-vel azonos).
        # Más üres-KJV sor (MT|lxx_os_etalon_f91 felirat, KEZI, KJV|lxx felirat) "nincs pár" marad.
        if not kj and m[io_] == 'MT' and m[ifo] == 'szamlalas' and m[im].strip():
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
