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

_TOKEN = re.compile(r'[^\W_]+', re.UNICODE)
_IGEHELY = re.compile(r'^(.+) (\d+):(\d+)$')
_TR_KIADAS = re.compile(r'^TR(?:[»«]\d+)?$')
MERES_KIZARAS = os.path.join(ROOT, 'f21p', 'meres_kizaras.tsv')


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


def betolt_eredeti():
    """igehely -> [eredeti szó dict, ...] a fájlsorrendben, sorszámmal.

    Kulcsok: sorsz, strong, alak, tukor, nem_tr (ÚSZ: nem TR-es sor).
    A TAHOT és a TAGNT Igehely mezője már Károli-natív.

    TR-es a sor, ha a Kritikai kiadás mezőben `TR`, `TR»N` vagy `TR«N` áll
    (a »/« a TR-beli eltérő szórendet jelöli: a szó a TR-ben is megvan, csak
    más helyen; F21.6). Ha a TR eltérő alakot olvas, annak nincs sora a
    kivonatban; ezeket a meres_kizaras() zárja ki a mérésből, itt nincs rájuk
    külön logika.
    """
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
