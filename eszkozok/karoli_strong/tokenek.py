#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Károli–Strong mérőpilot (F21) — közös adatbetöltés és tokenizálás.

Ugyanez a modul szolgál a promptnál (bemenet.py), a kapunál (kapu.py), a
mintavételnél (minta_general.py) és a mérésnél: egyetlen tokenizáló függvény,
egyetlen sorszámozás.

Szabályok:
  * Károli-token = Unicode betű- és számjegysorozat (az írásjel és az aláhúzás
    nem token). Sorszám versen belül 1-től.
  * Eredeti szó = a TAHOT/TAGNT-kivonat egy sora (a héber elő-/utóragok, H9xxx,
    külön sorok). Sorszám = a sor helye a versen belül, 1-től. Hogy ez a
    szórendnek felel meg, azt a sorrend_ellenoriz.py igazolja a nyers
    #01, #02... sorszámmal (F21 P-K1).
  * TSV-olvasás: split('\\t'), írás: '\\t'.join — a csv modul tilos.

Nem kerül adat az adat/ és konkordancia/ könyvtárba; a modul csak olvas.
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KONK = os.path.join(ROOT, 'konkordancia')

KAROLI = os.path.join(KONK, 'Karoli_1908.tsv')
TAHOT = os.path.join(KONK, 'TAHOT_kivonat.tsv')
TAGNT = os.path.join(KONK, 'TAGNT_kivonat.tsv')
REGI_ARANY = os.path.join(KONK, 'Karoli_Strong_kivonat.tsv')
VERSMEGF = os.path.join(KONK, 'Karoli_versmegfeleltetes.tsv')
NORMTABLA = os.path.join(KONK, 'Konyv_normalizalo_tabla.tsv')
KJV_FAJLOK = {
    'Gen': os.path.join(KONK, 'KJV_Strongs_Genesis.tsv'),
    'Exo': os.path.join(KONK, 'KJV_Strongs_Exodus.tsv'),
    'Pro': os.path.join(KONK, 'KJV_Strongs_Proverbs.tsv'),
}

KJV_TELJES = os.path.join(KONK, 'KJV_Strongs_teljes.tsv')   # F19: 66 könyv, angol (KJV) számozás
KJV_HIANYOK = os.path.join(ROOT, 'naplok', 'F19_hianyok.tsv')

_TOKEN = re.compile(r'[^\W_]+', re.UNICODE)
_IGEHELY = re.compile(r'^(.+) (\d+):(\d+)$')
_TR_KIADAS = re.compile(r'^TR(?:[»«]\d+)?$')
MERES_KIZARAS = os.path.join(ROOT, 'f21p', 'meres_kizaras.tsv')
VERSBEOSZTAS_MEGF = os.path.join(ROOT, 'f22', 'versmegfeleltetes.tsv')   # F22: a versbeosztás-detektor gépi listája
# A lista csak ezekre a könyvekre érvényes a futtatóban (a többi sor javaslat, amíg a felhasználó nem hagyja jóvá):
# (F22) a detektor pontossága csak az 1Móz (üres lista) és a 2Móz (35:36–36:37) esetén volt igazolt; pl. az Ézs 9:17–20 hamis lett volna.
# F85.6 óta a TAHOT_kivonat kulcsai Károli-kulcsok, a detektor-lista az ÓSZ-ben üres, a lista érvényessége már csak az ÚSZ-sorokra számít.
VERSBEOSZTAS_JOVAHAGYOTT = ('2Móz', '3Móz', '4Móz', '5Móz', 'Józs', 'Zsolt', 'Ézs', 'Jer', '1Krón', '2Krón', 'Ezsd', 'Ez', 'Péld', 'Bír', 'Jób', 'Eszt', '2Sám', '1Sám')
VERSMEGF_KEZI = os.path.join(ROOT, 'f22', 'versmegfeleltetes_kezi.tsv')   # F22: kézi javítások a detektor listájához (a regenerálás nem írja felül)
VERSOSSZEVONAS = os.path.join(ROOT, 'f22', 'versosszevonas.tsv')   # F22: kézzel jóváhagyott 1:2 beolvasztások


def tokenizal(szoveg):
    """Károli-szöveg -> tokenlista (sorszám = index + 1)."""
    return _TOKEN.findall(szoveg)


def _sorok(ut):
    """TSV-sorok mezőlistái a fejléc nélkül; csak split('\\t')."""
    with open(ut, encoding='utf-8') as f:
        ossz = [s.rstrip('\n').rstrip('\r') for s in f]
    return [s.split('\t') for s in ossz[1:] if s.strip()]


def igehely_bont(igehely):
    """'1Móz 3:16' -> ('1Móz', 3, 16); hibás alakra None."""
    m = _IGEHELY.match(igehely)
    if not m:
        return None
    return m.group(1), int(m.group(2)), int(m.group(3))


def konyv_step_to_hu():
    """STEPBible-rövidítés -> magyar rövidítés (Konyv_normalizalo_tabla.tsv)."""
    return {r[0]: r[1] for r in _sorok(NORMTABLA)}


def konyv_hu_to_step():
    return {v: k for k, v in konyv_step_to_hu().items()}


def step_igehely_to_hu(igehely):
    """'Gen.1.1' -> '1Móz 1:1' (Konyv_normalizalo_tabla.tsv szerint).

    Normalizálás nélkül néma nem-találatot kapnánk (CLAUDE.md); ismeretlen
    könyvre KeyError, nem néma None.
    """
    k, c, v = igehely.split('.')
    return '%s %s:%s' % (konyv_step_to_hu()[k], c, v)


def betolt_karoli():
    """igehely -> Károli-szöveg, fájlsorrendben (dict megőrzi a sorrendet)."""
    return {r[0]: r[1] for r in _sorok(KAROLI)}


def versmegfeleltetes(ut=None, jovahagyott=None):
    """A versbeosztás-detektor gépi listája (`f22/versmegfeleltetes.tsv`): [(karoli, eredeti, tipus)];
    a `#` kezdetű sorokat átugorja, hiányzó fájlra üres lista."""
    ut = ut or VERSBEOSZTAS_MEGF
    if not os.path.exists(ut):
        return []
    jovahagyott = VERSBEOSZTAS_JOVAHAGYOTT if jovahagyott is None else jovahagyott
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    sor = [tuple(s.split('\t')) for s in sorok[1:]]
    sor = _kezi_javitas(sor)
    if jovahagyott is False:
        return sor
    return [r for r in sor if _IGEHELY.match(r[0] or r[1]) and _IGEHELY.match(r[0] or r[1]).group(1) in jovahagyott]


def _kezi_javitas(sor, ut=None):
    """A detektor listáját javítja az `f22/versmegfeleltetes_kezi.tsv` szerint (`karoli`, `eredeti`, `tipus`):
    `torol` típusú sor törli a detektor azon sorait, amelyeknek a Károli-igehelye egyezik (ha van), illetve az
    `eredeti` nem párosított (`nincs_karoli`) sorát; más típusú sor hozzáadódik, és a vele azonos Károli-igehelyű
    vagy azonos eredetijű `nincs_karoli` detektor-sort kiváltja. A hiányzó fájl nem hiba."""
    ut = ut or VERSMEGF_KEZI
    if not os.path.exists(ut):
        return sor
    with open(ut, encoding='utf-8') as f:
        kezi = [tuple((s.rstrip('\n').rstrip('\r').split('\t') + ['', '', ''])[:3]) for s in f if s.strip() and not s.startswith('#')][1:]
    for k, e, t in kezi:
        if k:
            sor = [r for r in sor if r[0] != k]
        if e:
            sor = [r for r in sor if not (r[0] == '' and r[1] == e)]
    return sor + [(k, e, t) for k, e, t in kezi if t != 'torol']


def versosszevonasok(ut=None):
    """A kézi 1:2 (a TAHOT-átkulcsolás óta: 2:1) versbeolvasztások (`f22/versosszevonas.tsv`):
    [{'karoli', 'hu_tol', 'hu_ig', 'eredeti', 'megj', 'er_tol', 'er_ig'}].

    `er_tol`–`er_ig` (F85.10, opcionális 6. és 7. oszlop): a beolvasztott TAHOT-vers (`eredeti`: a vers
    átkulcsolás előtti TAHOT-címkéje) tokenjeinek 1-alapú helye a közös Károli-kulcs LEKÉPEZETT (a detektor-/kézi tábla szerinti leképezés utáni, az összevonás kiemelése előtti, fájlsorrendű) tokenlistájában (a kulcsok az F85.6 óta Károli-kulcsok, a lista az ÓSZ-ben üres, így ez a nyers lista).
    Ha hiányzik (régi alak), az `eredeti` még létező nyers TAHOT-kulcs, és a tokenjei onnan jönnek."""
    ut = ut or VERSOSSZEVONAS
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    ki = []
    for s in sorok[1:]:
        r = s.split('\t')
        ki.append({'karoli': r[0], 'hu_tol': int(r[1]), 'hu_ig': int(r[2]), 'eredeti': r[3], 'megj': r[4] if len(r) > 4 else '',
                   'er_tol': int(r[5]) if len(r) > 5 and r[5] else None, 'er_ig': int(r[6]) if len(r) > 6 and r[6] else None})
    return ki


def _eredeti_osztva():
    """(Károli-kulcsú lista, beolvasztott extra tokenek). A lista a nyers TAHOT/TAGNT-lista LEKÉPEZETT alakja (`_versmegfeleltet`), az összevonás kiemelése után. Az `er_tol`–`er_ig` sorokra a közös kulcs leképezett
    tokenlistájából kiemeli a beolvasztott TAHOT-vers tokenjeit (extra: sorszám = a fő vers tokenszáma + i), a fő vers
    tokenjei 1-től újraszámozva maradnak a kulcson. Visszafelé kompatibilis: a régi alakú sorokkal (nincs `er_tol`) nem
    foglalkozik, azokat az `osszevont_extra` a nyers kulcsról veszi."""
    ered = _versmegfeleltet(_nyers_eredeti(), versmegfeleltetes())
    extra = {}
    for o in versosszevonasok():
        if o['er_tol'] is None:
            continue
        lista = ered.get(o['karoli'])
        if lista is None or not (1 <= o['er_tol'] <= o['er_ig'] <= len(lista)):
            raise SystemExit('versosszevonas.tsv: %s er_tol–er_ig (%s–%s) nem fér a kulcs %d tokenjébe' % (
                o['karoli'], o['er_tol'], o['er_ig'], len(lista or [])))
        fo = [w for i, w in enumerate(lista, 1) if not (o['er_tol'] <= i <= o['er_ig'])]
        ered[o['karoli']] = [dict(w, sorsz=i) for i, w in enumerate(fo, 1)]
        extra[o['karoli']] = [dict(w, sorsz=len(fo) + i) for i, w in enumerate(lista[o['er_tol'] - 1:o['er_ig']], 1)]
    return ered, extra


def osszevont_extra(nyers=None):
    """{karoli_igehely: [eredeti token, ...]}: a beolvasztott eredeti versek tokenjei, a sorszám a Károli-vers saját
    eredeti szavai utáni folytatás. Az `er_tol`–`er_ig` soroknál a közös Károli-kulcs tokenjeiből (F85.10), a régi alakú
    soroknál a nyers kulcson álló `eredeti` vers tokenjeiből."""
    ered, extra = _eredeti_osztva()
    ki = dict(extra)
    regi = [o for o in versosszevonasok() if o['er_tol'] is None]
    if regi:
        nyers = nyers if nyers is not None else _nyers_eredeti()
        for o in regi:
            alap = len(ered.get(o['karoli'], []))
            ki[o['karoli']] = [dict(w, sorsz=alap + i) for i, w in enumerate(nyers[o['eredeti']], 1)]
    return ki


def _versmegfeleltet(ered, sorok):
    """A nyers (TAHOT/TAGNT-kulcsú) versfolyamot a Károli-kulcsra képezi a detektor listája szerint:
    `eltolt`: a Károli-vers a megfeleltetett eredeti verset kapja; `nincs_eredeti`: a Károli-versnek nincs
    eredeti verse; `nincs_karoli`: az eredeti vers nem tartozik Károli-vershez (a saját kulcsán marad, vagy ha az
    a kulcs már Károli-versé, a versszáma +1000 — ilyenkor a szám nem igehely, csak azonosító).
    Ami a listában nem szerepel, változatlan (azonos kulcs)."""
    if not sorok:
        return ered
    osszev = versosszevonasok()
    # régi alakú sorok (nincs er_tol): az `eredeti` a nyers TAHOT-kulcs, az ilyen eredeti vers nem gazdátlan;
    # új alakú sorok (F85.10): a beolvasztás a közös, ÁTKULCSOLT Károli-kulcson áll (az `eredeti` csak címke),
    # ezért az új kulcs védett: nincs_karoli sor rá nem hagyhatja el a kulcsot a leképezésből
    beolvasztott_regi = {o['eredeti'] for o in osszev if o['er_tol'] is None}
    beolvasztott_uj = {o['karoli'] for o in osszev if o['er_tol'] is not None}
    beolvasztott = beolvasztott_regi | beolvasztott_uj
    erintett_k = {k for k, e, t in sorok if k}
    erintett_e = {e for k, e, t in sorok if e and e not in beolvasztott_uj}
    uj = {ig: v for ig, v in ered.items() if ig not in erintett_k and ig not in erintett_e}
    for k, e, t in sorok:
        if t == 'eltolt':
            uj[k] = ered[e]
    # a nincs_eredeti Károli-vers kulcsán álló, de egyetlen sorban sem szereplő eredeti vers nem veszhet el:
    # gazdátlan eredeti vers lesz (+1000-es azonosító), az egyesítő kezi állapotban viszi tovább
    for ig in sorted(erintett_k - erintett_e):
        if ig in ered:
            b = _IGEHELY.match(ig)
            uj['%s %s:%d' % (b.group(1), b.group(2), int(b.group(3)) + 1000)] = ered[ig]
    for k, e, t in sorok:
        if t == 'nincs_karoli' and e in beolvasztott:
            continue
        if t == 'nincs_karoli':
            b = _IGEHELY.match(e)
            kulcs = e if e not in uj and e not in erintett_k else '%s %s:%d' % (b.group(1), b.group(2), int(b.group(3)) + 1000)
            uj[kulcs] = ered[e]
    return uj


def betolt_eredeti(versmegf=True):
    """igehely -> [eredeti szó dict, ...] a fájlsorrendben, sorszámmal.

    versmegf=True (F22): a `f22/versmegfeleltetes.tsv` (versbeosztás-detektor) szerint a Károli-vers a
    megfeleltetett eredeti verset kapja; versmegf=False: a nyers, fájl szerinti kulcsok (a detektor ezt olvassa).

    Kulcsok: sorsz, strong, alak, tukor, nem_tr (ÚSZ: nem TR-es sor).
    A TAHOT és a TAGNT Igehely mezője már Károli-natív.

    TR-es a sor, ha a Kritikai kiadás mezőben `TR`, `TR»N` vagy `TR«N` áll
    (a »/« a TR-beli eltérő szórendet jelöli: a szó a TR-ben is megvan, csak
    más helyen; F21.6). Ha a TR eltérő alakot olvas, annak nincs sora a
    kivonatban; ezeket a meres_kizaras() zárja ki a mérésből, itt nincs rájuk
    külön logika.
    """
    if versmegf:
        return _eredeti_osztva()[0]
    return _nyers_eredeti()


def _nyers_eredeti():
    """A nyers (fájl szerinti kulcsú) TAHOT/TAGNT versfolyam: igehely -> [eredeti szó dict, ...]."""
    ered = {}
    for ut, nt in ((TAHOT, False), (TAGNT, True)):
        for r in _sorok(ut):
            lista = ered.setdefault(r[0], [])
            nem_tr = False
            if nt:
                kiadasok = r[7].split('+') if len(r) > 7 else []
                nem_tr = not any(_TR_KIADAS.match(k) for k in kiadasok)
            lista.append({
                'sorsz': len(lista) + 1,
                'strong': r[1],
                'alak': r[2],
                'tukor': r[6],
                'nem_tr': nem_tr,
            })
    return ered


def maradek(karoli=None, ered=None):
    """A versmegfeleltetési maradék (F22 22.0/2).

    Visszaad: (karoli_parja_nelkul, eredeti_karoli_nelkul) — két rendezett lista.
    A fő brief szerint 61 + 30 vers; az aktuális szám a jelentésbe kerül.
    """
    karoli = karoli if karoli is not None else betolt_karoli()
    ered = ered if ered is not None else betolt_eredeti()
    a = [k for k in karoli if k not in ered]
    b = [k for k in ered if k not in karoli]
    return a, b


def _strong_nullaz(s):
    """'H430' -> 'H0430' (négyjegyűre nullázva)."""
    m = re.match(r'^([HG])(\d+)$', s)
    return '%s%04d' % (m.group(1), int(m.group(2))) if m else s


def _kjv_verstabla():
    """STEPBible-igehely (Gen.1.1) -> [(angol szó, nullázott Strong), ...]."""
    tabla = {}
    for ut in KJV_FAJLOK.values():
        for r in _sorok(ut):
            tabla.setdefault(r[0], []).append((r[3].strip(), _strong_nullaz(r[2].strip())))
    return tabla


_KJV_CACHE = {}


def kjv_tamapont(igehely_karoli):
    """KJV-támpont a Károli-versre; None, ha nincs (könyv nincs KJV-táblában,
    vagy a versmegfeleltetés nem ad 1:1 KJV-verset).

    Forma: 'In the beginning{H7225} God{H430} ...' (a Strong nullázva).
    A KJV-verset a Karoli_versmegfeleltetes.tsv igehely_kjv oszlopa adja.
    """
    if not _KJV_CACHE:
        _KJV_CACHE['tabla'] = _kjv_verstabla()
        _KJV_CACHE['megf'] = {r[0]: r[1] for r in _sorok_versmegf()}
        _KJV_CACHE['h2s'] = konyv_hu_to_step()
    b = igehely_bont(igehely_karoli)
    if not b:
        return None
    kjv = _KJV_CACHE['megf'].get(igehely_karoli)
    if not kjv or not re.match(r'^\d+:\d+$', kjv):
        return None
    step = _KJV_CACHE['h2s'].get(b[0])
    if step is None:
        return None
    sorok = _KJV_CACHE['tabla'].get('%s.%s' % (step, kjv.replace(':', '.')))
    if not sorok:
        return None
    return ' '.join(('%s{%s}' % (sz, s)) if sz else '{%s}' % s for sz, s in sorok)


_KJV_TELJES_CACHE = {}


def _kjv_teljes_tabla():
    """STEPBible-igehely (Gen.1.1) -> [(angol szó, nullázott Strong), ...] a TELJES
    KJV-táblából (konkordancia/KJV_Strongs_teljes.tsv, F19; eBible).

    A fájl elején '#' kezdetű megjegyzéssorok állnak a fejléc előtt (a _sorok ezeket
    adatnak venné), ezért saját olvasó: a '#' sorokat és az 'Igehely' fejlécet kihagyja.
    A Strong-jelölés normalizálása ugyanaz, mint a régi táblánál (_strong_nullaz:
    'H430' -> 'H0430'). Az eBible-tábla angol szava 'szó' szintű (a régi studybible-tábla
    frázisokat is tartalmaz, és üres szavú {H0853} elemeket); ez a két forrás között
    a bájtazonosságot kizárja, l. kjv_osszevet.py."""
    if 'tabla' not in _KJV_TELJES_CACHE:
        tabla = {}
        with open(KJV_TELJES, encoding='utf-8') as f:
            for s in f:
                s = s.rstrip('\n').rstrip('\r')
                if not s.strip() or s.startswith('#') or s.startswith('Igehely\t'):
                    continue
                r = s.split('\t')
                tabla.setdefault(r[0], []).append((r[3].strip(), _strong_nullaz(r[2].strip())))
        _KJV_TELJES_CACHE['tabla'] = tabla
    return _KJV_TELJES_CACHE['tabla']


def _kjv_sor(sorok):
    return ' '.join(('%s{%s}' % (sz, s)) if sz else '{%s}' % s for sz, s in sorok)


def _kjv_megfeleltetes():
    if not _KJV_CACHE:
        _KJV_CACHE['tabla'] = _kjv_verstabla()
        _KJV_CACHE['megf'] = {r[0]: r[1] for r in _sorok_versmegf()}
        _KJV_CACHE['h2s'] = konyv_hu_to_step()
    return _KJV_CACHE['megf'], _KJV_CACHE['h2s']


def kjv_tamapont_teljes(igehely_karoli):
    """KJV-támpont a Károli-versre a TELJES KJV-táblából (F19); None, ha nincs.

    Ugyanaz a forma, mint a kjv_tamapont-é: 'beginning{H7225} God{H0430} ...'.
    A Károli-vers KJV-megfelelőjét a Karoli_versmegfeleltetes.tsv igehely_kjv oszlopa
    adja (a teljes tábla is angol/KJV-számozású, tehát ugyanaz a kulcs érvényes, mint a
    régi táblánál). Nincs KJV-sor (None), ha
      * a versmegfeleltetésben nincs (vagy nem 'fejezet:vers' alakú) KJV-megfelelő
        (pl. a Károli-vers a KJV-ben nincs meg; a versszámozási eltérések — Zsoltár-
        címek, Jóel, Mal stb. — a megfeleltetési tábla szerint oldódnak fel);
      * a könyv nem szerepel a normalizáló táblában;
      * a megfelelő KJV-vers a teljes táblában nem szerepel (naplok/F19_hianyok.tsv:
        KJV-oldali adathiány: Mk 9:43, Lk 6:41, Lk 17:36).
    A régi kjv_tamapont-ot nem érinti."""
    megf, h2s = _kjv_megfeleltetes()
    b = igehely_bont(igehely_karoli)
    if not b:
        return None
    kjv = megf.get(igehely_karoli)
    if not kjv or not re.match(r'^\d+:\d+$', kjv):
        return None
    step = h2s.get(b[0])
    if step is None:
        return None
    sorok = _kjv_teljes_tabla().get('%s.%s' % (step, kjv.replace(':', '.')))
    if not sorok:
        return None
    return _kjv_sor(sorok)


def kjv_tamapont_forras(igehely_karoli, forras='regi'):
    """A KJV-támpont a megadott forrásból: 'regi' (kjv_tamapont) vagy 'teljes'
    (kjv_tamapont_teljes). Ismeretlen forrásra ValueError."""
    if forras == 'regi':
        return kjv_tamapont(igehely_karoli)
    if forras == 'teljes':
        return kjv_tamapont_teljes(igehely_karoli)
    raise ValueError('ismeretlen KJV-forrás: %r (regi|teljes)' % (forras,))


def kjv_forras_azonosito():
    """A teljes KJV-tábla azonosítása a jsonl kjv_forras mezőjéhez: (relatív út, sha256).
    A sha256 a bájtokra számolt (a *.tsv LF-re rögzített: .gitattributes eol=lf)."""
    import hashlib
    with open(KJV_TELJES, 'rb') as f:
        return 'konkordancia/KJV_Strongs_teljes.tsv', hashlib.sha256(f.read()).hexdigest()


def _sorok_versmegf():
    """A versmegfeleltetési tábla adatsorai (a # kezdetű fejléc-megjegyzések
    és az oszlopfejléc nélkül)."""
    with open(VERSMEGF, encoding='utf-8') as f:
        ossz = [s.rstrip('\n').rstrip('\r') for s in f]
    ossz = [s for s in ossz if s.strip() and not s.startswith('#')]
    return [s.split('\t') for s in ossz[1:]]


def regi_arany(versek=None):
    """A régi arany (Karoli_Strong_kivonat.tsv) hármasai, csak memóriában.

    (igehely_karoli, karoli_szo, strong) — Károli-natív igehellyel, a Strong
    négyjegyűre nullázott (a fájl már így tárolja). Ha versek meg van adva
    (halmaz), arra szűr. A fájl nem módosul.
    """
    k_hu = konyv_step_to_hu()
    ki = []
    for r in _sorok(REGI_ARANY):
        try:
            ig = step_igehely_to_hu(r[0]) if '.' in r[0] else r[0]
        except KeyError:
            continue
        if versek is not None and ig not in versek:
            continue
        ki.append((ig, r[2], r[1]))
    return ki


def meres_kizaras():
    """A pontossági mérésből kizárt eredeti tokenek (f21p/meres_kizaras.tsv).

    Visszaad: {(igehely, eredeti_sorsz): ok}. Oszlopok: igehely,
    eredeti_sorsz, ok (fejléccel; csak split('\\t')). Ha a fájl nincs meg,
    üres szótár.
    """
    if not os.path.exists(MERES_KIZARAS):
        return {}
    return {(r[0], int(r[1])): r[2] for r in _sorok(MERES_KIZARAS)}


ARANY_V2 = os.path.join(ROOT, 'f21p', 'arany_opus_v2.jsonl')
ARANY_V2_SHA = os.path.join(ROOT, 'f21p', 'arany_opus_v2.sha256')


def sha256_lf(ut):
    """A fájl sha256-ja LF-re normalizált sorvéggel (a core.autocrlf=true munkafán
    a checkout CRLF-et adhat; a befagyasztott tartalom a sorvégtől független)."""
    import hashlib
    with open(ut, 'rb') as f:
        return hashlib.sha256(f.read().replace(b'\r\n', b'\n')).hexdigest()


def arany_v2_befagyasztas_ellenoriz(ut=ARANY_V2):
    """Az arany v2 befagyasztásának ellenőrzése (F21.14): a jsonl LF-normalizált
    sha256-ja egyezik a f21p/arany_opus_v2.sha256 első mezőjével. Eltérésnél vagy
    hiányzó hash-fájlnál SystemExit (a hívó szkript hibával áll meg)."""
    if not os.path.exists(ARANY_V2_SHA):
        raise SystemExit('HIBA: nincs befagyasztási hash: %s' % ARANY_V2_SHA)
    with open(ARANY_V2_SHA, encoding='utf-8') as f:
        vart = f.read().split()[0]
    kapott = sha256_lf(ut)
    if kapott != vart:
        raise SystemExit('HIBA: az arany v2 (%s) sha256-ja %s, a befagyasztott %s — a befagyasztott v2 megváltozott'
                         % (ut, kapott, vart))
    return kapott


def legfrissebb_arany(gyoker=None):
    """A legfrissebb befagyasztott arany (F21.42, P3c): (jsonl, sha256-fájl, verzió).

    Ha létezik a f21p/arany_opus_v3.sha256, az arany v3 (a befagyasztás jele a
    hash-fájl megléte); különben az arany v2. A gyoker alapértelmezése a repó gyökere
    (teszthez ideiglenes könyvtár adható)."""
    gyoker = ROOT if gyoker is None else gyoker
    f21p = os.path.join(gyoker, 'f21p')
    v3_sha = os.path.join(f21p, 'arany_opus_v3.sha256')
    if os.path.exists(v3_sha):
        return os.path.join(f21p, 'arany_opus_v3.jsonl'), v3_sha, 'v3'
    return os.path.join(f21p, 'arany_opus_v2.jsonl'), os.path.join(f21p, 'arany_opus_v2.sha256'), 'v2'


def hash_hiba(ut, sha_ut, nev=None):
    """Egy befagyasztott fájl ellenőrzése a sha256-fájl első mezője ellen (LF-normalizált
    sha256). Visszaad: hibaüzenet (str) vagy None, ha rendben."""
    nev = nev or os.path.basename(ut)
    if not os.path.exists(sha_ut):
        return 'hiányzik a befagyasztási hash (%s): %s' % (nev, sha_ut)
    if not os.path.exists(ut):
        return 'hiányzik a befagyasztott fájl (%s): %s' % (nev, ut)
    with open(sha_ut, encoding='utf-8') as f:
        mezok = f.read().split()
    if not mezok:
        return 'üres a befagyasztási hash-fájl (%s): %s' % (nev, sha_ut)
    kapott = sha256_lf(ut)
    if kapott != mezok[0]:
        return 'a befagyasztott %s sha256-ja %s, a várt %s' % (nev, kapott, mezok[0])
    return None


def generalas_ts():
    """A proveniencia-sor ts mezője (F21.20): a generálás ideje, UTC, másodpercre.

    A generált kimenetek ezért ismételt futáskor a fejlécsorban eltérnek; a
    tartalmi sorok bájtra azonosak maradnak (a bájtazonosságot ígérő minta-
    és kiválasztás-fájlok — minta.tsv, opus_arany_kivalasztas.tsv — nem kapnak
    ts-t, azokat ez nem érinti)."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def konyv_rovid(igehely):
    b = igehely_bont(igehely)
    return b[0] if b else None


if __name__ == '__main__':
    kar = betolt_karoli()
    er = betolt_eredeti()
    a, b = maradek(kar, er)
    print('Károli-versek: %d' % len(kar))
    print('Károli-szavak: %d' % sum(len(tokenizal(t)) for t in kar.values()))
    print('eredeti versek: %d, sorok: %d' % (len(er), sum(len(v) for v in er.values())))
    print('Károli-vers eredeti-pár nélkül: %d' % len(a))
    print('eredeti vers Károli-pár nélkül: %d' % len(b))
