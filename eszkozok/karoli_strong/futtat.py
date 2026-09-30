#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P3 — a Károli–Strong mérőpilot F1–F6 futtatója (OpenRouter).

Futások (F21 brief P3):
  F1  A modell, 200 vers                  (KJV-támponttal, ahol van)
  F2  B modell, 200 vers
  F3  C modell, 200 vers
  F4  C döntőbíróként: azok a versek, ahol F1 és F2 link-szinten eltér, vagy
      valamelyik kapuhibás maradt (a döntőbíró látja A és B válaszát)
  F5  A modell, KJV-támpont nélkül, az R1 100 verse
  F6  B modell, KJV-támpont nélkül, az R1 100 verse
  F3V2 C modell, 200 vers, a prompt_v2.md-vel (F21.12: a tíz konvenció
      szabályként); kimenet valaszok/F3V2.jsonl; ugyanaz a futasnaplo.tsv, a
      plafon kumulatív. ELŐKÉSZÍTVE: a trigger (futtatas.txt) külön jóváhagyásra.

P3b (F21.25, DT22/PD11; mind a prompt_v2.md-vel, kimenet valaszok/<futas>.jsonl):
  F1V2  A modell, 200 vers (KJV-támponttal, ahol a minta szerint van)
  F2V2  B modell, 200 vers
  F5V2  A modell, KJV nélkül, az R1 100 verse
  F6V2  B modell, KJV nélkül, az R1 100 verse
  F3V2B C modell, 200 vers: a F3V2 MÁSODIK futása (ugyanaz a konfiguráció, külön
        kimenet; az ingadozás méréséhez). A naplóban a futas oszlop F3V2B, a jsonl
        köteg-sorai az 'ismetles_of': 'F3V2' jelölést kapják.
  F4V2  C döntőbíróként az F1V2 és F2V2 eltérő vagy kapuhibás versein. Alapja a
        prompt_v2 utasításrésze + a prompt_biro_v2.md kiegészítése (a biro-fájl
        változatlan; a futtató cseréli az alapot: biro_utasitas(alap_ut)). Csak akkor
        fut, ha az F1V2 és az F2V2 kész (különben kilépési kód 2). Futási sorrend:
        F1V2, F2V2, F5V2, F6V2, F3V2B, F4V2; egy triggerben is mehet (a régi F4
        "csak egyedül" szabálya az F4V2-re nem vonatkozik).

Modellek: A google/gemini-3.1-flash-lite, B deepseek/deepseek-v4-flash,
C google/gemini-3.8-flash. 10 vers / hívás; versenként az ötpontos kapu
(kapu.py), hibánál egy újrakérés; a mintából a f21p/minta.tsv sorrendjében.

Kimenet (alapból a f21p/ alatt):
  valaszok/<futas>.jsonl  köteg-soronként: nyers válaszok + versenkénti állapot
  futasnaplo.tsv          hívásonként: tokenek, cost, modell, futás, köteg,
                          kapuhiba, próbálkozás, időbélyeg, gondolkodási mód

Költségplafon: 3 USD kumulatívan (KEMÉNY korlát) a futasnaplo.tsv koltseg_usd oszlopa
alapján, MINDEN hívás előtt ellenőrizve (a napló összege + a hívás becsült
költsége); túllépésnél leállás, kilépési kód 3, a kész kötegek mentve maradnak. A
futás újraindítható: a kész köteg (a jsonl-ben már szereplő verscsoport) nem hív újra.
Szigorúbb plafon a vezérlőfájl OPCIONÁLIS plafon_usd=<szám> kulcsával adható
(0 < szám <= 3; hiányában 3.0; nem szám, <= 0, > 3 vagy nem véges érték hiba, 2-es
kilépési kód, hívás nélkül). A plafon mindig a NAPLÓ KUMULATÍV összegére vonatkozik (a
korábbi futások költségét is tartalmazza), pl. plafon_usd=2 a 2 USD kumulatív
költségnél megáll (kilépési kód 3).

Befagyasztott bemenetek: a futtató induláskor (éles futás előtt) ellenőrzi a
prompt_v1.md, prompt_v2.md, prompt_biro_v2.md LF-normalizált sha256-ját
(BEFAGYASZTOTT) és az arany_opus_v2.jsonl-ét (tokenek.arany_v2_befagyasztas_ellenoriz);
eltérésnél 2-es kilépési kód, hívás nélkül. A futás végén a mentett válaszokat is
újra ellenőrzi (mentett_valaszok_ellenoriz: ötpontos kapu, K5; F4/F4V2-nél a 6.
pont is); külön: --mentett-ellenoriz F1V2,... .

Gondolkodási mód: A és B kikapcsolva (reasoning.enabled=false, a fordit.py
_valodi_http_kuldo alapja); a C modellnél a gondolkodás kötelező (nem
kapcsolható ki), ezért ott a legalacsonyabb elfogadott szint (minimal, ha az
OpenRouter 400-zal elutasítja: low). A tényleges mód a futásnapló
gondolkodas_mod oszlopában.

Kulcs: csak az OPENROUTER_API_KEY környezeti változóból; soha nem kerül
naplóba, fájlba vagy hibaüzenetbe (a kiírt hibákból kiszűrődik).

F4 (döntőbíró, prompt_biro_v2.md): az A és B EGYEZŐ linkjei rögzítettek; a C csak a
vitatott magyar szavakról dönt (és a kapuhibás maradt versek teljes párosításáról).
A rögzítést gép kényszeríti (biro_kenyszer, hatodik kapupont): a C válaszában
minden A–B-egyező link szerepel, és a nem vitatott magyar szavak állapota
(linkjei, betoldás-e) változatlan; eltérésnél egy újrakérés hibaüzenettel,
másodszor is eltérő válasznál a vers kapuhiba. A kimenet sémája ugyanaz, mint az
A/B-é, és a C sem írhat Strong-számot (ötödik kapupont).

Használat:
    python eszkozok/karoli_strong/futtat.py --szaraz            # becslés, hálózat nélkül
    python eszkozok/karoli_strong/futtat.py --onteszt           # MOCK küldővel
    python eszkozok/karoli_strong/futtat.py --vezerlo f21p/futtatas.txt   # éles (kulccsal)
    python eszkozok/karoli_strong/futtat.py --futas F1 --koteg-max 1      # éles, kézi
    python eszkozok/karoli_strong/futtat.py --mentett-ellenoriz F1V2,F4V2 # mentett válaszok újraellenőrzése

Nincs alapértelmezett futás: --szaraz, --onteszt, --vezerlo vagy --futas (és ez
utóbbival --koteg-max) nélkül a szkript hibával (kilépési kód 2) áll meg.

VEZÉRLŐFÁJL (f21p/futtatas.txt; a workflow ezt olvassa): egyszerű kulcs=érték sorok,
a # kezdetű sor és az üres sor megjegyzés. KÖTELEZŐ kulcs mindkettő, alapérték
nincs; ismeretlen, hiányzó vagy ismételt kulcs, hibás érték, hiányzó fájl esetén a
futtatás 2-es kilépési kóddal áll meg, és semmit nem hív meg.
    futasok=F1            # vesszővel elválasztva: F1..F6, F3V2, F1V2, F2V2, F5V2, F6V2, F3V2B, F4V2;
                          # a régi F4 csak egyedül (külön trigger: az F1 és F2 kész kell);
                          # az F4V2 más futással együtt is állhat (az F1V2 és F2V2 kész kell)
    koteg_max=1           # futásonként legfeljebb ennyi ÚJ köteg (10 vers/köteg) fut;
                          # pozitív egész, vagy 'mind' (a kész kötegek kimaradnak)
    plafon_usd=2          # OPCIONÁLIS: kumulatív (napló-összeg) plafon USD-ben, 0 < x <= 3;
                          # hiányában 3.0 (a kemény korlát)
Példák: az első trigger: futasok=F1, koteg_max=1 (10 vers); a második:
futasok=F1,F2,F3,F5,F6, koteg_max=mind; a harmadik: futasok=F4, koteg_max=mind;
P3b egy triggerben: futasok=F1V2,F2V2,F5V2,F6V2,F3V2B,F4V2, koteg_max=mind,
plafon_usd=2.
A futások mindig a FUTASOK definíciójának sorrendjében futnak (F1,F2,F3,F4,F5,F6,
F3V2,F1V2,F2V2,F5V2,F6V2,F3V2B,F4V2), akárhogy van felsorolva a fájlban.

GONDOLKODÁSI MÓD ÉS A JELENTÉS (F21 P3 döntés): az A és B gondolkodása
KIKAPCSOLVA fut, a C-é kötelező (nem kapcsolható ki), ezért minimal (400-nál low)
szinten. A C költsége a gondolkodási tokennel együtt a valódi ár (a futasnaplo.tsv
gondolkodas_token oszlopa külön vezeti, a koltseg_usd már tartalmazza). A
mérés/jelentés (P4–P6) minden minőség- és költségösszevetésnél jelölje: az A/B és a
C beállítása eltérő (kikapcsolva vs. minimal/low), tehát a C-vel való összevetés nem
azonos beállítású; a gondolkodas_mod oszlop adja a tényleges szintet.

Kilépési kódok: 0 rendben; 1 hiba (pl. hálózati hiba egy kötegnél, a többi
kötegre mentve); 2 előfeltétel hiányzik (pl. F4 az F1/F2 előtt) vagy hibás
vezérlés/paraméter; 3 költségplafon.
"""

import argparse
import json
import math
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ITT)
sys.path.insert(0, os.path.dirname(_ITT))  # eszkozok/ (fordit.py)
import bemenet  # noqa: E402
import fordit  # noqa: E402
import kapu  # noqa: E402
import tokenek  # noqa: E402

F21P = os.path.join(tokenek.ROOT, 'f21p')
MINTA_UT = os.path.join(F21P, 'minta.tsv')
BIRO_PROMPT_UT = os.path.join(F21P, 'prompt_biro_v2.md')   # a v1 megmarad, nem használt

PLAFON_USD = 3.0
KOTEG_MERET = 10
MAX_TOKENS = 12000          # hívásonként; a lefutó gondolkodás se szaladjon el
KILEPES_PLAFON = 3

MODELLEK = {
    'A': 'google/gemini-3.1-flash-lite',
    'B': 'deepseek/deepseek-v4-flash',
    'C': 'google/gemini-3.8-flash',
}

# Tartalék ár (USD / 1M token: bemenet, kimenet), ha a válaszban nincs `cost`;
# forrás: fp2/koltsegbecsles.py ARAK (A, B) és naplok/FORDITAS_P0_modellek.json (C).
# B-nél a magasabb (fp2) ár a konzervatív.
ARAK = {
    'google/gemini-3.1-flash-lite': (0.25, 1.50),
    'deepseek/deepseek-v4-flash': (0.14, 0.28),
    'google/gemini-3.8-flash': (0.75, 3.75),
}

# A C modell kötelező gondolkodásának szintjei, a legalacsonyabbtól; 400-as
# elutasításnál a következő. A sikeres szint a folyamat hátralevő részére marad.
C_REASONING_LANC = [{'effort': 'minimal'}, {'effort': 'low'}]

FUTASOK = {
    'F1': {'modell': 'A', 'tipus': 'parosit', 'kjv': True, 'reteg': None},
    'F2': {'modell': 'B', 'tipus': 'parosit', 'kjv': True, 'reteg': None},
    'F3': {'modell': 'C', 'tipus': 'parosit', 'kjv': True, 'reteg': None},
    'F4': {'modell': 'C', 'tipus': 'biro', 'kjv': True, 'reteg': None, 'forras': ('F1', 'F2')},
    'F5': {'modell': 'A', 'tipus': 'parosit', 'kjv': False, 'reteg': 'R1'},
    'F6': {'modell': 'B', 'tipus': 'parosit', 'kjv': False, 'reteg': 'R1'},
    # F21.12 (előkészítve, a trigger külön jóváhagyásra): C, 200 vers, prompt_v2
    'F3V2': {'modell': 'C', 'tipus': 'parosit', 'kjv': True, 'reteg': None, 'prompt': bemenet.PROMPT_V2_UT},
    # F21.25 (P3b, DT22/PD11): mind a prompt_v2-vel; a dict sorrendje a futási sorrend
    'F1V2': {'modell': 'A', 'tipus': 'parosit', 'kjv': True, 'reteg': None, 'prompt': bemenet.PROMPT_V2_UT},
    'F2V2': {'modell': 'B', 'tipus': 'parosit', 'kjv': True, 'reteg': None, 'prompt': bemenet.PROMPT_V2_UT},
    'F5V2': {'modell': 'A', 'tipus': 'parosit', 'kjv': False, 'reteg': 'R1', 'prompt': bemenet.PROMPT_V2_UT},
    'F6V2': {'modell': 'B', 'tipus': 'parosit', 'kjv': False, 'reteg': 'R1', 'prompt': bemenet.PROMPT_V2_UT},
    'F3V2B': {'modell': 'C', 'tipus': 'parosit', 'kjv': True, 'reteg': None, 'prompt': bemenet.PROMPT_V2_UT,
              'ismetles_of': 'F3V2'},
    'F4V2': {'modell': 'C', 'tipus': 'biro', 'kjv': True, 'reteg': None, 'forras': ('F1V2', 'F2V2'),
             'prompt': bemenet.PROMPT_V2_UT},
}

# Befagyasztott bemenetek: a fájl LF-normalizált sha256-ja (tokenek.sha256_lf). Éles futás
# előtt ellenőrzi a futtató (befagyasztas_ellenoriz); az arany v2-t a
# tokenek.arany_v2_befagyasztas_ellenoriz. A prompt-fájl változtatása új fájl (v3), nem
# ezek módosítása.
BEFAGYASZTOTT = {
    'f21p/prompt_v1.md': '4a02ec8178c921650f113481bf14a26a162e26bff59f9b1cb9c8f3d0474d4d37',
    'f21p/prompt_v2.md': '6c47f2d95fe64e4fbf22597f87b587eafa0c8d26bd35f18fac28b63bb6a944d5',
    'f21p/prompt_biro_v2.md': '9b50267b892a5fe49815b07433dd1aec35c7e0a3ac14fe0d9332d3e18f1f63b6',
}

NAPLO_FEJLEC = ['ts', 'futas', 'koteg', 'probalkozas', 'modell', 'gondolkodas_mod',
                'igehely_db', 'kjv', 'bemenet_token', 'kimenet_token', 'gondolkodas_token',
                'koltseg_usd', 'koltseg_forras', 'kapuhiba_db', 'http_kiserlet',
                'idotartam_mp', 'finish_reason', 'prompt_sha256_12', 'futo_osszeg_usd']

KAR_PER_TOKEN = 3.0           # durva becslés (héber/görög/magyar vegyes szöveg)
KIMENET_TOKEN_VERSENKENT = 150   # F22 költségbecslés
C_GONDOLKODAS_HIVASONKENT = 500  # becslés: a minimal szint tokenje hívásonként


class PlafonLeallas(Exception):
    pass


# ---------------------------------------------------------------------------
# minta, utasítások
# ---------------------------------------------------------------------------

def _tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.strip()]


def minta_betolt(ut=MINTA_UT):
    """A minta.tsv sorai fájlsorrendben: [{'igehely','reteg',...}]."""
    return _tsv(ut)


def verslista(futas_id, minta, kimenet_dir):
    """A futás versei a minta sorrendjében (F4-nél az eltérő versek)."""
    spec = FUTASOK[futas_id]
    if spec['tipus'] == 'biro':
        a = eredmenyek_betolt(spec['forras'][0], kimenet_dir)
        b = eredmenyek_betolt(spec['forras'][1], kimenet_dir)
        ki = []
        for s in minta:
            ig = s['igehely']
            if ig not in a or ig not in b:
                raise ElofeltetelHiany('az %s futás nem teljes: hiányzik a %s vers (előbb az %s és %s kell)'
                                       % ('/'.join(spec['forras']), ig, *spec['forras']))
            if elter(a[ig], b[ig]):
                ki.append(ig)
        return ki
    return [s['igehely'] for s in minta if spec['reteg'] is None or s['reteg'] == spec['reteg']]


class ElofeltetelHiany(Exception):
    pass


def elter(a, b):
    """Az F1–F2 eltérése egy versre: link-szinten különbözik, vagy valamelyik kapuhibás."""
    la, lb = linkek(a), linkek(b)
    return la is None or lb is None or la != lb


def linkek(rekord):
    """Link-halmaz {(k_poz, e_poz)}; kapuhibás vers: None (mindig 'eltérő')."""
    if rekord.get('allapot') != 'ok' or not rekord.get('obj'):
        return None
    return {(p[0], e) for p in rekord['obj']['parok'] for e in p[1]}


def biro_utasitas(alap_ut=None):
    """A főprompt utasításrésze + a döntőbírói kiegészítés (prompt_biro_v2.md).

    alap_ut: az alapprompt fájlja (None = prompt_v1.md, a régi F4; F4V2-nél a
    prompt_v2.md). A döntőbírói fájl tartalma nem változik, a futtató cseréli az
    alapot: a kiegészítés csak a „fenti feladatra” hivatkozik, az alap szövegére nem."""
    with open(BIRO_PROMPT_UT, encoding='utf-8') as f:
        s = f.read()
    a = s.index(bemenet.KEZDET) + len(bemenet.KEZDET)
    b = s.index(bemenet.VEGE)
    return bemenet.prompt_utasitas(alap_ut) + '\n\n' + s[a:b].strip('\n')


def biro_sha256(alap_ut=None):
    import hashlib
    return hashlib.sha256(biro_utasitas(alap_ut).encode('utf-8')).hexdigest()


def _kompakt(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def biro_allapot(obj):
    """Egy válasz magyar szavankénti állapota: {k: (frozenset(eredeti sorszámok), betoldás-e)}."""
    all_ = {}
    for k, es in obj['parok']:
        all_.setdefault(k, [set(), False])[0].update(es)
    for k in obj['betoldas']:
        all_.setdefault(k, [set(), False])[1] = True
    return {k: (frozenset(v[0]), v[1]) for k, v in all_.items()}


def biro_rogzites(a_rek, b_rek):
    """Az F4 rögzített része az A és B (mindkettő kapun átment) válaszából.

    Visszaad: (rogzitett_linkek, rogzitett_betoldas, vitatott_k), mind rendezett
    lista; vagy None, ha A vagy B kapuhibás (nincs mit rögzíteni).

    * rögzített link: (k, e), amely A-ban is és B-ben is szerepel;
    * vitatott magyar szó: amelynek állapota (linkjei, betoldás-e) A-ban és
      B-ben különbözik; a nem vitatott magyar szó állapota rögzített;
    * rögzített betoldás: a nem vitatott, mindkettőben betoldott magyar szavak.
    """
    if a_rek['allapot'] != 'ok' or b_rek['allapot'] != 'ok' or not a_rek['obj'] or not b_rek['obj']:
        return None
    sa, sb = biro_allapot(a_rek['obj']), biro_allapot(b_rek['obj'])
    la = {(k, e) for k, (es, _) in sa.items() for e in es}
    lb = {(k, e) for k, (es, _) in sb.items() for e in es}
    vitatott = sorted(k for k in set(sa) | set(sb) if sa.get(k) != sb.get(k))
    betoldas = sorted(k for k in sa if k not in vitatott and sa[k][1])
    return sorted(la & lb), betoldas, vitatott


def biro_kenyszer(c_obj, a_rek, b_rek):
    """A döntőbíró válaszának ellenőrzése az F4 rögzítése ellen (hatodik kapupont).

    Hibaüzenetek listája (üres = rendben). Szabályok, ha A és B is kapun átment:
      6a. minden A–B-egyező link szerepel a C válaszában;
      6b. minden nem vitatott magyar szó állapota (linkjei, betoldás-e) azonos
          az A–B-egyezővel (nem törölhető, nem kap új linket, nem lesz
          betoldás / betoldásból link).
    Ha A vagy B kapuhibás, nincs rögzítés, a teljes párosítás szabad.
    """
    r = biro_rogzites(a_rek, b_rek)
    if r is None:
        return []
    linkek_r, _, vitatott = r
    sc = biro_allapot(c_obj)
    sa = biro_allapot(a_rek['obj'])
    lc = {(k, e) for k, (es, _) in sc.items() for e in es}
    hibak = []
    hianyzo = sorted(set(linkek_r) - lc)
    if hianyzo:
        hibak.append('6. rögzített (A és B által egyezően adott) link hiányzik a válaszodból: %s; '
                     'a rögzített linkeket változatlanul meg kell tartanod' % json.dumps(hianyzo))
    valtozott = sorted(k for k in sa if k not in vitatott and sc.get(k) != sa[k])
    if valtozott:
        hibak.append('6. ezeknek a nem vitatott magyar szavaknak a párosítása (vagy betoldás-jelölése) '
                     'megváltozott, pedig rögzített: %s; csak a vitatott magyar szavakról '
                     'dönthetsz' % valtozott)
    return hibak


def biro_kotegszoveg(igehelyek, a_eredmenyek, b_eredmenyek, kjv=True, alap_ut=None):
    """A döntőbíró hívásának üzenete: utasítás + versblokkok + A és B válasza
    + a gép által kiszámolt rögzítés és vitatott szavak."""
    blokkok = []
    for ig in igehelyek:
        sorok = [bemenet.versblokk(ig, kjv)]
        for cimke, er in (('A', a_eredmenyek), ('B', b_eredmenyek)):
            r = er[ig]
            sorok.append('%s MODELL VÁLASZA: %s' % (
                cimke, _kompakt(r['obj']) if r['allapot'] == 'ok' and r['obj'] else 'KAPUHIBA'))
        rog = biro_rogzites(a_eredmenyek[ig], b_eredmenyek[ig])
        if rog is None:
            sorok.append('RÖGZÍTETT: nincs (legalább az egyik modell válasza kapuhibás maradt); '
                         'add meg a teljes párosítást.')
        else:
            sorok.append('RÖGZÍTETT LINKEK (A és B egyezik; változatlanul szerepelniük kell): %s'
                         % _kompakt([list(x) for x in rog[0]]))
            sorok.append('RÖGZÍTETT BETOLDÁS (A és B egyezik): %s' % _kompakt(rog[1]))
            sorok.append('VITATOTT MAGYAR SZAVAK (csak ezekről döntesz): %s' % _kompakt(rog[2]))
        blokkok.append('\n'.join(sorok))
    return '%s\n\n=== A FELDOLGOZANDÓ VERSEK (%d) ===\n\n%s\n' % (
        biro_utasitas(alap_ut), len(igehelyek), '\n\n'.join(blokkok))


def kotegszoveg_futashoz(futas_id, igehelyek, kimenet_dir):
    spec = FUTASOK[futas_id]
    if spec['tipus'] == 'biro':
        a = eredmenyek_betolt(spec['forras'][0], kimenet_dir)
        b = eredmenyek_betolt(spec['forras'][1], kimenet_dir)
        return biro_kotegszoveg(igehelyek, a, b, spec['kjv'], spec.get('prompt'))
    return bemenet.kotegszoveg(igehelyek, spec['kjv'], spec.get('prompt'))


def utasitas_sha12(futas_id):
    import hashlib
    if FUTASOK[futas_id]['tipus'] == 'biro':
        return biro_sha256(FUTASOK[futas_id].get('prompt'))[:12]
    return hashlib.sha256(bemenet.prompt_utasitas(FUTASOK[futas_id].get('prompt')).encode('utf-8')).hexdigest()[:12]


def befagyasztas_ellenoriz(tabla=None, gyoker=None, arany=True):
    """A befagyasztott bemenetek ellenőrzése; hibaüzenetek listája (üres = rendben)."""
    tabla = BEFAGYASZTOTT if tabla is None else tabla
    gyoker = tokenek.ROOT if gyoker is None else gyoker
    hibak = []
    for rel, vart in tabla.items():
        ut = os.path.join(gyoker, *rel.split('/'))
        if not os.path.exists(ut):
            hibak.append('hiányzik a befagyasztott fájl: %s' % rel)
            continue
        kapott = tokenek.sha256_lf(ut)
        if kapott != vart:
            hibak.append('a befagyasztott %s sha256-ja %s, a várt %s' % (rel, kapott, vart))
    if arany:
        try:
            tokenek.arany_v2_befagyasztas_ellenoriz()
        except SystemExit as e:
            hibak.append(str(e))
    return hibak


def mentett_valaszok_ellenoriz(futas_id, kimenet_dir):
    """A futás MENTETT (allapot=ok) válaszainak újraellenőrzése a nyers modellhívásoktól
    függetlenül: az ötpontos kapu (a 5. pont a K5: nincs Strong-szám) és F4/F4V2-nél a 6.
    pont (rögzítés). Hibaüzenetek listája (üres = rendben); a kapuhibás versek obj-ja
    None kell legyen."""
    spec = FUTASOK[futas_id]
    hibak = []
    a = b = None
    if spec['tipus'] == 'biro':
        a = eredmenyek_betolt(spec['forras'][0], kimenet_dir)
        b = eredmenyek_betolt(spec['forras'][1], kimenet_dir)
    for sor in koteg_sorok(futas_id, kimenet_dir):
        for ig, v in sor['versek'].items():
            if v['allapot'] != 'ok':
                if v.get('obj') is not None:
                    hibak.append('%s %s: kapuhibás vers obj-ja nem None' % (futas_id, ig))
                continue
            try:
                h = kapu.vers_ellenoriz(v['obj'], bemenet.vers_adat(ig))
            except Exception as e:  # noqa: BLE001
                h = ['a mentett válasz nem ellenőrizhető: %s' % e]
            if not h and a is not None:
                h = biro_kenyszer(v['obj'], a[ig], b[ig])
            for x in h:
                hibak.append('%s %s: %s' % (futas_id, ig, x))
    return hibak


# ---------------------------------------------------------------------------
# fájlkezelés: válaszok, napló
# ---------------------------------------------------------------------------

def valasz_ut(futas_id, kimenet_dir):
    return os.path.join(kimenet_dir, 'valaszok', '%s.jsonl' % futas_id)


def naplo_ut(kimenet_dir):
    return os.path.join(kimenet_dir, 'futasnaplo.tsv')


def koteg_sorok(futas_id, kimenet_dir):
    ut = valasz_ut(futas_id, kimenet_dir)
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        return [json.loads(s) for s in f if s.strip()]


def eredmenyek_betolt(futas_id, kimenet_dir):
    """{igehely: {'allapot','probalkozas','hibak','obj'}} a futás kész kötegeiből."""
    ki = {}
    for sor in koteg_sorok(futas_id, kimenet_dir):
        ki.update(sor['versek'])
    return ki


def kesz_kotegek(futas_id, kimenet_dir):
    return {tuple(s['igehelyek']) for s in koteg_sorok(futas_id, kimenet_dir)}


def koteg_ment(futas_id, kimenet_dir, sor):
    ut = valasz_ut(futas_id, kimenet_dir)
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(sor, ensure_ascii=False) + '\n')
        f.flush()


def naplo_ir(kimenet_dir, sor):
    ut = naplo_ut(kimenet_dir)
    uj = not os.path.exists(ut) or os.path.getsize(ut) == 0
    with open(ut, 'a', encoding='utf-8', newline='\n') as f:
        if uj:
            f.write('\t'.join(NAPLO_FEJLEC) + '\n')
        f.write('\t'.join(str(sor[k]) for k in NAPLO_FEJLEC) + '\n')
        f.flush()


def naplo_osszeg(kimenet_dir):
    """A futasnaplo.tsv koltseg_usd oszlopának összege (a plafon alapja)."""
    ut = naplo_ut(kimenet_dir)
    if not os.path.exists(ut):
        return 0.0
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r').split('\t') for s in f if s.strip()]
    if len(sorok) < 2:
        return 0.0
    i = sorok[0].index('koltseg_usd')
    return sum(float(s[i]) for s in sorok[1:])


# ---------------------------------------------------------------------------
# hívás: költségellenőrzés, küldés, naplózás
# ---------------------------------------------------------------------------

def becsult_koltseg(modell_id, uzenetek, versdb):
    """Egy hívás konzervatív költségbecslése a plafon-ellenőrzéshez."""
    kar = sum(len(m['content']) for m in uzenetek)
    be = kar / KAR_PER_TOKEN
    ki = KIMENET_TOKEN_VERSENKENT * versdb
    if modell_id == MODELLEK['C']:
        ki += C_GONDOLKODAS_HIVASONKENT
    ar_be, ar_ki = ARAK[modell_id]
    return be / 1e6 * ar_be + ki / 1e6 * ar_ki


class Kontextus:
    """A futtatás környezete: küldő, kulcs, kimeneti könyvtár, plafon."""

    def __init__(self, kuldo, api_key, kimenet_dir, plafon=PLAFON_USD, alvas=None):
        self.kuldo = kuldo
        self.api_key = api_key
        self.kimenet_dir = kimenet_dir
        self.plafon = plafon
        self.alvas = alvas
        self.c_reasoning_index = 0   # a C_REASONING_LANC aktuális tagja

    def tiszta(self, szoveg):
        """A kulcs kiszűrése minden kiírt szövegből."""
        s = str(szoveg)
        if self.api_key:
            s = s.replace(self.api_key, '***')
        return s


def _gondolkodas_mod(ctx, modell_kulcs):
    if modell_kulcs != 'C':
        return 'kikapcsolva'
    if ctx.c_reasoning_index >= len(C_REASONING_LANC):
        return 'kotelezo_alap'
    return 'kotelezo_effort=%s' % C_REASONING_LANC[ctx.c_reasoning_index]['effort']


def kuldes(ctx, modell_kulcs, uzenetek):
    """Egy HTTP-hívás a fordit._http_post_nyers visszalépéses újrapróbálásával;
    a C modellnél 400-as elutasításnál a következő gondolkodási szint.
    Visszaad: (nyers_valasz_dict, http_kiserlet, gondolkodas_mod)."""
    modell_id = MODELLEK[modell_kulcs]
    while True:
        extra = {'max_tokens': MAX_TOKENS}
        if modell_kulcs == 'C' and ctx.c_reasoning_index < len(C_REASONING_LANC):
            extra['reasoning'] = dict(C_REASONING_LANC[ctx.c_reasoning_index])
        mod = _gondolkodas_mod(ctx, modell_kulcs)
        try:
            valasz, kiserlet = fordit._http_post_nyers(
                modell_id, uzenetek, ctx.api_key, extra, kuldo=ctx.kuldo, alvas=ctx.alvas)
            return valasz, kiserlet, mod
        except fordit.OpenRouterHiba as e:
            if (modell_kulcs == 'C' and 'HTTP kliens-hiba 400' in str(e)
                    and ctx.c_reasoning_index < len(C_REASONING_LANC)):
                print('  C gondolkodási szint elutasítva (%s), következő szint' % mod, flush=True)
                ctx.c_reasoning_index += 1
                continue
            raise


# A gondolkodási (reasoning) token lehetséges helyei az usage-ban, sorrendben.
# OpenRouter: usage.completion_tokens_details.reasoning_tokens (a completion_tokens
# már tartalmazza); a másik két alak tartalék (Responses-stílusú / lapos mező).
GONDOLKODAS_UTAK = (
    ('completion_tokens_details', 'reasoning_tokens'),
    ('output_tokens_details', 'reasoning_tokens'),
    ('reasoning_tokens',),
)


def gondolkodas_token(usage):
    """A válasz usage mezőjéből a gondolkodási token (az első nem nulla hely); 0, ha nincs."""
    for ut in GONDOLKODAS_UTAK:
        x = usage
        for kulcs in ut:
            x = x.get(kulcs) if isinstance(x, dict) else None
        if isinstance(x, (int, float)) and not isinstance(x, bool) and x:
            return int(x)
    return 0


def hivas(ctx, futas_id, koteg_no, probalkozas, uzenetek, igehelyek, kapuhiba_db_fn):
    """Egy modellhívás plafon-ellenőrzéssel és naplózással.

    Visszaad: (a válasz szövege, hívásrekord). A hívásrekord (nyers usage,
    a reasoning-szöveg hossza, finish_reason) a köteg-sorba, a jsonl-be kerül,
    hogy a naplóoszlopok (pl. gondolkodas_token) utólag ellenőrizhetők legyenek.
    A kapuhiba_db_fn(szoveg) a kapu szerint hibás versek számát adja (a naplóba kerül)."""
    spec = FUTASOK[futas_id]
    modell_kulcs = spec['modell']
    modell_id = MODELLEK[modell_kulcs]
    eddig = naplo_osszeg(ctx.kimenet_dir)
    becs = becsult_koltseg(modell_id, uzenetek, len(igehelyek))
    if eddig + becs > ctx.plafon:
        raise PlafonLeallas('a napló összege %.4f USD + a hívás becsült költsége %.4f USD > plafon %.4f USD'
                            % (eddig, becs, ctx.plafon))
    t0 = time.time()
    valasz, kiserlet, mod = kuldes(ctx, modell_kulcs, uzenetek)
    mp = time.time() - t0

    usage = valasz.get('usage') or {}
    be = usage.get('prompt_tokens', 0) or 0
    ki = usage.get('completion_tokens', 0) or 0
    gond = gondolkodas_token(usage)
    koltseg = usage.get('cost')
    if koltseg is None:
        ar_be, ar_ki = ARAK[modell_id]
        koltseg = be / 1e6 * ar_be + ki / 1e6 * ar_ki
        forras = 'ar_config'
    else:
        forras = 'openrouter'
    valasz_elem = (valasz.get('choices') or [{}])[0]
    szoveg = ((valasz_elem.get('message') or {}).get('content')) or ''
    finish = valasz_elem.get('finish_reason') or ''

    naplo_ir(ctx.kimenet_dir, {
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'futas': futas_id, 'koteg': koteg_no, 'probalkozas': probalkozas,
        'modell': modell_id, 'gondolkodas_mod': mod,
        'igehely_db': len(igehelyek), 'kjv': 'igen' if spec['kjv'] else 'nem',
        'bemenet_token': be, 'kimenet_token': ki, 'gondolkodas_token': gond,
        'koltseg_usd': '%.6f' % koltseg, 'koltseg_forras': forras,
        'kapuhiba_db': kapuhiba_db_fn(szoveg), 'http_kiserlet': kiserlet,
        'idotartam_mp': '%.2f' % mp, 'finish_reason': finish,
        'prompt_sha256_12': utasitas_sha12(futas_id),
        'futo_osszeg_usd': '%.6f' % (eddig + koltseg),
    })
    rekord = {'probalkozas': probalkozas, 'usage': usage, 'finish_reason': finish,
              'reasoning_szoveg_karakter': len(((valasz_elem.get('message') or {}).get('reasoning')) or '')}
    return szoveg, rekord


# ---------------------------------------------------------------------------
# köteg és futás
# ---------------------------------------------------------------------------

def valasz_ellenoriz_futashoz(futas_id, szoveg, igehelyek, kimenet_dir):
    """A kapu (5 pont) + F4-nél a rögzítés kényszerítése (6. pont)."""
    r = kapu.valasz_ellenoriz(szoveg, igehelyek)
    if FUTASOK[futas_id]['tipus'] == 'biro':
        forras = FUTASOK[futas_id]['forras']
        a = eredmenyek_betolt(forras[0], kimenet_dir)
        b = eredmenyek_betolt(forras[1], kimenet_dir)
        for ig in igehelyek:
            if r[ig]['ok']:
                h = biro_kenyszer(r[ig]['obj'], a[ig], b[ig])
                if h:
                    r[ig] = {'ok': False, 'hibak': h, 'obj': r[ig]['obj']}
    return r


def koteg_feldolgoz(ctx, futas_id, koteg_no, igehelyek):
    """Egy köteg: hívás, kapu, egy újrakérés; a köteg-sor mentése."""
    uzenet = kotegszoveg_futashoz(futas_id, igehelyek, ctx.kimenet_dir)
    uzenetek = [{'role': 'user', 'content': uzenet}]
    nyers = []

    def hibak_szama_fn(ig_lista):
        return lambda szoveg: sum(1 for r in valasz_ellenoriz_futashoz(
            futas_id, szoveg, ig_lista, ctx.kimenet_dir).values() if not r['ok'])

    szoveg1, rek1 = hivas(ctx, futas_id, koteg_no, 1, uzenetek, igehelyek, hibak_szama_fn(igehelyek))
    nyers.append(szoveg1)
    hivasrekordok = [rek1]
    kapu1 = valasz_ellenoriz_futashoz(futas_id, szoveg1, igehelyek, ctx.kimenet_dir)
    versek = {}
    for ig in igehelyek:
        r = kapu1[ig]
        versek[ig] = {'allapot': 'ok' if r['ok'] else 'kapuhiba', 'probalkozas': 1,
                      'hibak': r['hibak'], 'obj': r['obj'] if r['ok'] else None}
    rossz = [ig for ig in igehelyek if not kapu1[ig]['ok']]
    if rossz:
        ujra = [{'role': 'user', 'content': uzenet},
                {'role': 'assistant', 'content': szoveg1},
                {'role': 'user', 'content': kapu.ujrakeres_uzenet({ig: kapu1[ig] for ig in rossz})}]
        szoveg2, rek2 = hivas(ctx, futas_id, koteg_no, 2, ujra, rossz, hibak_szama_fn(rossz))
        nyers.append(szoveg2)
        hivasrekordok.append(rek2)
        kapu2 = valasz_ellenoriz_futashoz(futas_id, szoveg2, rossz, ctx.kimenet_dir)
        for ig in rossz:
            r = kapu2[ig]
            if r['ok']:
                versek[ig] = {'allapot': 'ok', 'probalkozas': 2, 'hibak': [], 'obj': r['obj']}
            else:
                versek[ig] = {'allapot': 'kapuhiba', 'probalkozas': 2, 'hibak': r['hibak'], 'obj': None}
    sor = {'futas': futas_id, 'modell': MODELLEK[FUTASOK[futas_id]['modell']], 'koteg': koteg_no,
           'igehelyek': igehelyek, 'nyers': nyers, 'hivasok': hivasrekordok, 'versek': versek}
    if FUTASOK[futas_id].get('ismetles_of'):
        sor['ismetles_of'] = FUTASOK[futas_id]['ismetles_of']
    koteg_ment(futas_id, ctx.kimenet_dir, sor)
    return versek


def futas(ctx, futas_id, minta, koteg_max=None):
    """Egy futás kötegei; visszaad: (kilépési_kód, összegzés_dict).

    koteg_max: legfeljebb ennyi ÚJ köteg fut (a kész kötegek nem számítanak);
    None = az összes."""
    versek = verslista(futas_id, minta, ctx.kimenet_dir)
    kotegek = bemenet.kotegek(versek, KOTEG_MERET)
    kesz = kesz_kotegek(futas_id, ctx.kimenet_dir)
    print('%s: %s, %d vers, %d köteg (kész: %d)%s' % (
        futas_id, MODELLEK[FUTASOK[futas_id]['modell']], len(versek), len(kotegek),
        sum(1 for k in kotegek if tuple(k) in kesz),
        ' [a %s ismétlése, 2. futás]' % FUTASOK[futas_id]['ismetles_of'] if FUTASOK[futas_id].get('ismetles_of') else ''),
        flush=True)
    hibas_kotegek = 0
    uj_kotegek = 0
    for no, k in enumerate(kotegek, 1):
        if tuple(k) in kesz:
            continue
        if koteg_max is not None and uj_kotegek >= koteg_max:
            print('  koteg_max (%d) elérve, a futás megáll; a többi köteg a következő triggerre marad'
                  % koteg_max, flush=True)
            break
        uj_kotegek += 1
        try:
            v = koteg_feldolgoz(ctx, futas_id, no, k)
        except PlafonLeallas as e:
            print('  KÖLTSÉGPLAFON a(z) %d. kötegnél: %s' % (no, ctx.tiszta(e)), flush=True)
            raise
        except fordit.OpenRouterHiba as e:
            hibas_kotegek += 1
            print('  HIBA a(z) %d. kötegnél (kihagyva, újraindításkor újra): %s' % (no, ctx.tiszta(e)),
                  file=sys.stderr, flush=True)
            continue
        print('  köteg %d/%d kész, kapuhiba: %d' % (
            no, len(kotegek), sum(1 for r in v.values() if r['allapot'] != 'ok')), flush=True)
    mentett_hibak = mentett_valaszok_ellenoriz(futas_id, ctx.kimenet_dir)
    if mentett_hibak:
        print('  A MENTETT VÁLASZOK ÚJRAELLENŐRZÉSE HIBÁT TALÁLT (%d):' % len(mentett_hibak), file=sys.stderr, flush=True)
        for x in mentett_hibak[:20]:
            print('    ' + x, file=sys.stderr, flush=True)
    return (1 if (hibas_kotegek or mentett_hibak) else 0), {
        'versek': len(versek), 'kotegek': len(kotegek), 'hibas_kotegek': hibas_kotegek,
        'mentett_hibak': len(mentett_hibak)}


def futasok_vegrehajt(ctx, futas_idk, minta, koteg_max=None):
    kod = 0
    for f in futas_idk:
        try:
            k, _ = futas(ctx, f, minta, koteg_max)
        except PlafonLeallas:
            return KILEPES_PLAFON
        except ElofeltetelHiany as e:
            print('ELŐFELTÉTEL: %s' % e, file=sys.stderr)
            return 2
        kod = max(kod, k)
    return kod


# ---------------------------------------------------------------------------
# vezérlőfájl (f21p/futtatas.txt)
# ---------------------------------------------------------------------------

VEZERLO_KULCSOK = ('futasok', 'koteg_max')          # kötelező
VEZERLO_OPCIONALIS = ('plafon_usd',)                   # opcionális


class VezerloHiba(Exception):
    pass


def vezerlo_beolvas(ut):
    """A vezérlőfájl értelmezése: {'futasok': [F-id, ...] (F1..F6 sorrendben),
    'koteg_max': int|None, 'plafon_usd': float|None} (a futasok a FUTASOK sorrendjében).
    A plafon_usd opcionális (0 < x <= PLAFON_USD); a többi kulcs kötelező, alapérték nincs.
    Hiba esetén VezerloHiba."""
    if not os.path.exists(ut):
        raise VezerloHiba('nincs vezérlőfájl: %s' % ut)
    with open(ut, encoding='utf-8') as f:
        sorok = [x.strip() for x in f.read().split('\n')]
    ertekek = {}
    for i, sor in enumerate(sorok, 1):
        if not sor or sor.startswith('#'):
            continue
        if '=' not in sor:
            raise VezerloHiba('%d. sor: nem kulcs=érték alakú: %r' % (i, sor))
        kulcs, ertek = (x.strip() for x in sor.split('=', 1))
        if kulcs not in VEZERLO_KULCSOK and kulcs not in VEZERLO_OPCIONALIS:
            raise VezerloHiba('%d. sor: ismeretlen kulcs: %r (érvényes: %s)'
                              % (i, kulcs, ', '.join(VEZERLO_KULCSOK + VEZERLO_OPCIONALIS)))
        if kulcs in ertekek:
            raise VezerloHiba('%d. sor: a(z) %s kulcs kétszer szerepel' % (i, kulcs))
        ertekek[kulcs] = ertek
    for kulcs in VEZERLO_KULCSOK:
        if kulcs not in ertekek:
            raise VezerloHiba('hiányzó kötelező kulcs: %s (nincs alapérték)' % kulcs)
    idk = [x.strip() for x in ertekek['futasok'].split(',') if x.strip()]
    if not idk:
        raise VezerloHiba('a futasok üres')
    for f in idk:
        if f not in FUTASOK:
            raise VezerloHiba('ismeretlen futás: %r (érvényes: %s)' % (f, ', '.join(FUTASOK)))
    if len(set(idk)) != len(idk):
        raise VezerloHiba('a futasok ismétlést tartalmaz: %s' % ertekek['futasok'])
    if 'F4' in idk and len(idk) > 1:
        raise VezerloHiba('az F4 külön triggerre való (az F1 és F2 kész kell), nem állhat más futással együtt')
    km = ertekek['koteg_max']
    if km == 'mind':
        koteg_max = None
    elif km.isdigit() and int(km) >= 1:
        koteg_max = int(km)
    else:
        raise VezerloHiba('a koteg_max pozitív egész vagy "mind" lehet, nem %r' % km)
    plafon_usd = None
    if 'plafon_usd' in ertekek:
        try:
            plafon_usd = float(ertekek['plafon_usd'])
        except ValueError:
            raise VezerloHiba('a plafon_usd nem szám: %r' % ertekek['plafon_usd'])
        if not math.isfinite(plafon_usd) or plafon_usd <= 0 or plafon_usd > PLAFON_USD:
            raise VezerloHiba('a plafon_usd 0 és %.1f (kemény korlát) között kell legyen, nem %r'
                              % (PLAFON_USD, ertekek['plafon_usd']))
    return {'futasok': [f for f in FUTASOK if f in idk], 'koteg_max': koteg_max, 'plafon_usd': plafon_usd}


def vezerlo_futtat(ctx, vezerlo_ut, minta):
    """A vezérlőfájl szerinti futtatás; hibás vezérlésnél 2, hívás nélkül."""
    try:
        v = vezerlo_beolvas(vezerlo_ut)
    except VezerloHiba as e:
        print('VEZÉRLŐFÁJL HIBA (%s): %s' % (vezerlo_ut, e), file=sys.stderr)
        return 2
    if v['plafon_usd'] is not None:
        ctx.plafon = min(ctx.plafon, v['plafon_usd'], PLAFON_USD)
    print('vezérlés: futások=%s, koteg_max=%s, plafon (kumulatív, napló-összeg) %.2f USD'
          % (','.join(v['futasok']), v['koteg_max'] or 'mind', ctx.plafon), flush=True)
    return futasok_vegrehajt(ctx, v['futasok'], minta, v['koteg_max'])


# ---------------------------------------------------------------------------
# --szaraz: becslés hálózat nélkül
# ---------------------------------------------------------------------------

def _tokenbecsles(f, versek, gondolkodas_c=C_GONDOLKODAS_HIVASONKENT):
    """Egy futás (f) bemeneti és kimeneti token-becslése a megadott versekre, a valódi
    kötegszövegekből (a futás saját promptjával). Visszaad: (kötegek, bemenet, kimenet)."""
    spec = FUTASOK[f]
    alap = spec.get('prompt')
    kotegek = bemenet.kotegek(versek, KOTEG_MERET)
    be = ki = 0
    for k in kotegek:
        szoveg_hossz = len(bemenet.kotegszoveg(k, spec['kjv'], alap))
        if spec['tipus'] == 'biro':
            # a döntőbírói utasítás hosszabb, és versenként két válasz is jön (A és B,
            # 150-150 token) + a rögzítés-sorok (kb. 40 token/vers); a válasz-JSON
            # karakterhossza ~ tokenszám * KAR_PER_TOKEN
            szoveg_hossz += len(biro_utasitas(alap)) - len(bemenet.prompt_utasitas(alap))
            szoveg_hossz += int((2 * KIMENET_TOKEN_VERSENKENT + 40) * KAR_PER_TOKEN * len(k))
        be += szoveg_hossz / KAR_PER_TOKEN
        ki += KIMENET_TOKEN_VERSENKENT * len(k)
        if spec['modell'] == 'C':
            ki += gondolkodas_c
    return kotegek, be, ki


def szaraz(minta, eltero_arany=0.30, gondolkodas_c=C_GONDOLKODAS_HIVASONKENT):
    """Token- és költségbecslés az F1–F6-ra a valódi kötegszövegekből.

    Bemenet: a tényleges kötegszöveg karakterszáma / KAR_PER_TOKEN. Kimenet:
    150 token/vers (F22 becslés) + a C gondolkodása hívásonként. Az F4
    versszáma az eltero_arany feltevéssel (az F1–F2 még nem létezik);
    az újrakérés költségét a kapuhiba-arány feltevése nélkül nem becsüljük
    (külön sor: +10% tartalék).
    """
    sorok = []
    for f in ('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F3V2'):
        spec = FUTASOK[f]
        modell_id = MODELLEK[spec['modell']]
        ar_be, ar_ki = ARAK[modell_id]
        if spec['tipus'] == 'biro':
            versek = [s['igehely'] for s in minta]
            n = int(round(len(versek) * eltero_arany))
            # reprezentatív részhalmaz: minden (1/arány)-edik vers
            lepes = max(1, int(round(1 / eltero_arany)))
            versek = versek[::lepes][:n]
        else:
            versek = [s['igehely'] for s in minta if spec['reteg'] is None or s['reteg'] == spec['reteg']]
        kotegek, be, ki = _tokenbecsles(f, versek, gondolkodas_c)
        koltseg = be / 1e6 * ar_be + ki / 1e6 * ar_ki
        sorok.append((f, modell_id, len(versek), len(kotegek), be, ki, koltseg))
    return sorok


def szaraz_kiir(minta, eltero_arany):
    print('SZÁRAZ BECSLÉS (hálózat nélkül; bemenet = tényleges kötegszöveg / %.1f karakter/token, '
          'kimenet = %d token/vers, C gondolkodás %d token/hívás, F4 eltérési arány feltevés: %.0f%%)'
          % (KAR_PER_TOKEN, KIMENET_TOKEN_VERSENKENT, C_GONDOLKODAS_HIVASONKENT, eltero_arany * 100))
    print('%-4s %-32s %6s %7s %12s %12s %10s' % ('futás', 'modell', 'vers', 'hívás', 'bemenet_tok', 'kimenet_tok', 'USD'))
    ossz = 0.0
    f3v2 = f3 = 0.0
    for f, m, n, k, be, ki, c in szaraz(minta, eltero_arany):
        print('%-5s %-32s %6d %7d %12d %12d %10.4f' % (f, m, n, k, be, ki, c))
        if f == 'F3V2':
            f3v2 = c
        else:
            ossz += c
        if f == 'F3':
            f3 = c
    print('ÖSSZESEN F1–F6 (újrakérés nélkül): %.4f USD; +10%% újrakérés-tartalékkal: %.4f USD; plafon: %.2f USD'
          % (ossz, ossz * 1.1, PLAFON_USD))
    eddig = naplo_osszeg(F21P)
    print('F3V2 (prompt_v2, előkészítve): becslés %.4f USD, +10%% tartalékkal %.4f USD; a futásnapló eddigi '
          'összege %.4f USD; kumulatívan a F3V2 után ~%.4f USD (plafon %.2f USD, kumulatív)'
          % (f3v2, f3v2 * 1.1, eddig, eddig + f3v2 * 1.1, PLAFON_USD))
    # tényleges F3-költség arányosítva (a becslés F3V2/F3 aránya; újrakéréssel együtt, mert a tényleges tartalmazza)
    ut = naplo_ut(F21P)
    if os.path.exists(ut) and f3:
        tenyl = sum(float(r['koltseg_usd']) for r in _tsv(ut) if r['futas'] == 'F3')
        if tenyl:
            print('F3V2 a tényleges F3-költségből arányosítva: %.4f USD × %.3f = %.4f USD (a tényleges F3 az '
                  'újrakéréseket és a gondolkodási tokent is tartalmazza)' % (tenyl, f3v2 / f3, tenyl * f3v2 / f3))
    return ossz


P3B_FUTASOK = ('F1V2', 'F2V2', 'F5V2', 'F6V2', 'F3V2B', 'F4V2')
P3B_FORRAS = {'F1V2': 'F1', 'F2V2': 'F2', 'F5V2': 'F5', 'F6V2': 'F6', 'F3V2B': 'F3V2'}   # a tényleges költség forrása
P3B_V1 = {'F1V2': 'F1', 'F2V2': 'F2', 'F5V2': 'F5', 'F6V2': 'F6'}    # a v1 megfelelő (a skálázáshoz)
P3B_PLAFON_KUMULATIV = 2.0


def p3b_becsles(minta, kimenet_dir=None):
    """A P3b becslése. Visszaad: dict a sorokkal és az eddigi napló-összeggel (hálózat nélkül).

    Két módszer futásonként: (a) képlet: a valódi kötegszövegek karaktere / KAR_PER_TOKEN,
    150 token/vers kimenet, a C-nél +500 token/hívás gondolkodás; (b) a megfelelő, már
    lefutott futás tényleges költsége (újrakérésekkel és gondolkodással együtt),
    felszorozva a v2- és a v1-prompt képlet szerinti arányával (az F3V2B-nél a F3V2
    tényleges költsége, ugyanaz a konfiguráció). Az F4V2 versszáma: (i) a meglévő F1/F2 (v1)
    mért eltérési aránya (link-szint vagy kapuhibás), (ii) a megengedő felső eset (a minta
    összes verse); az F4V2-nek nincs tényleges költségű megfelelője."""
    kimenet_dir = kimenet_dir or F21P
    ig_all = [s_['igehely'] for s_ in minta]
    arany = None
    try:
        a1 = eredmenyek_betolt('F1', kimenet_dir)
        a2 = eredmenyek_betolt('F2', kimenet_dir)
        if all(ig in a1 and ig in a2 for ig in ig_all):
            arany = (sum(1 for ig in ig_all if elter(a1[ig], a2[ig])), len(ig_all))
    except (OSError, ValueError, KeyError):
        arany = None
    naplo = _tsv(naplo_ut(kimenet_dir)) if os.path.exists(naplo_ut(kimenet_dir)) else []

    def tenyleges(futas_id):
        return sum(float(r['koltseg_usd']) for r in naplo if r['futas'] == futas_id)

    sorok = []
    for f in P3B_FUTASOK:
        spec = FUTASOK[f]
        ar_be, ar_ki = ARAK[MODELLEK[spec['modell']]]
        if spec['tipus'] == 'biro':
            for cimke, n in (('F4V2 (mért v1-arány)', arany[0] if arany else len(ig_all)),
                             ('F4V2 (felső eset: mind a %d vers)' % len(ig_all), len(ig_all))):
                kotegek, be, ki = _tokenbecsles(f, ig_all[:n])
                sorok.append({'futas': cimke, 'versek': n, 'hivasok': len(kotegek), 'be': be, 'ki': ki,
                              'kepletes': be / 1e6 * ar_be + ki / 1e6 * ar_ki, 'skalazott': None, 'f4': True})
            continue
        versek = [s_['igehely'] for s_ in minta if spec['reteg'] is None or s_['reteg'] == spec['reteg']]
        kotegek, be, ki = _tokenbecsles(f, versek)
        kepletes = be / 1e6 * ar_be + ki / 1e6 * ar_ki
        skalazott = None
        t = tenyleges(P3B_FORRAS[f])
        if t:
            if f == 'F3V2B':
                skalazott = t                    # ugyanaz a konfiguráció: a F3V2 tényleges költsége
            else:
                _, be1, ki1 = _tokenbecsles(P3B_V1[f], versek)
                ar1 = be1 / 1e6 * ar_be + ki1 / 1e6 * ar_ki
                skalazott = t * (kepletes / ar1) if ar1 else None
        sorok.append({'futas': f, 'versek': len(versek), 'hivasok': len(kotegek), 'be': be, 'ki': ki,
                      'kepletes': kepletes, 'skalazott': skalazott, 'f4': False})
    return {'sorok': sorok, 'arany': arany, 'eddig': naplo_osszeg(kimenet_dir)}


def p3b_kiir(minta):
    r = p3b_becsles(minta)
    print()
    print('P3b SZÁRAZ BECSLÉS (F1V2, F2V2, F5V2, F6V2, F3V2B, F4V2; mind prompt_v2; hálózat nélkül)')
    if r['arany']:
        print('  a v1 F1/F2 mért eltérési aránya (link-szinten eltér vagy kapuhibás): %d/%d = %.1f%%'
              % (r['arany'][0], r['arany'][1], 100 * r['arany'][0] / r['arany'][1]))
    print('  %-34s %6s %7s %12s %12s %12s %14s' % ('futás', 'vers', 'hívás', 'bemenet_tok', 'kimenet_tok', 'képlet USD', 'skálázott USD'))
    for x in r['sorok']:
        print('  %-34s %6d %7d %12d %12d %12.4f %14s' % (
            x['futas'], x['versek'], x['hivasok'], x['be'], x['ki'], x['kepletes'],
            '%.4f' % x['skalazott'] if x['skalazott'] is not None else '—'))
    nem_f4 = [x for x in r['sorok'] if not x['f4']]
    for f4x in [x for x in r['sorok'] if x['f4']]:
        kep = sum(x['kepletes'] for x in nem_f4) + f4x['kepletes']
        ska = sum((x['skalazott'] if x['skalazott'] is not None else x['kepletes']) for x in nem_f4) + f4x['kepletes']
        for nev, osszeg in (('képlet', kep), ('skálázott (az F4V2: képlet)', ska)):
            tart = osszeg * 1.1
            kum = r['eddig'] + tart
            print('  ÖSSZESEN [%s; %s]: %.4f USD, +10%% újrakérés-tartalékkal %.4f USD; a napló eddigi összege %.4f USD; '
                  'kumulatívan ~%.4f USD (megállási küszöb: %.1f USD kumulatív, kemény korlát %.1f USD)%s'
                  % (f4x['futas'], nev, osszeg, tart, r['eddig'], kum, P3B_PLAFON_KUMULATIV, PLAFON_USD,
                     '  >>> MEGHALADJA a %.1f USD-t' % P3B_PLAFON_KUMULATIV if kum > P3B_PLAFON_KUMULATIV else ''))
    return r


# ---------------------------------------------------------------------------
# --onteszt: MOCK küldővel, hálózat és kulcs nélkül
# ---------------------------------------------------------------------------

class _MockValasz:
    def __init__(self, szoveg_json, status=200):
        self.status_code = status
        self._j = szoveg_json
        self.text = json.dumps(szoveg_json)[:300] if szoveg_json is not None else ''

    def json(self):
        return self._j


class MockKuldo:
    """Hamis OpenRouter: a bemenetből olvassa a verseket, a bemenet-
    tokenszámokból adja az usage-t.

    Viselkedés (determinisztikus):
      * A és C: minden vers helyes (gépi kapun átmenő) párosítás;
      * B: minden 4. vers (az igehely hash-e szerint) egy ponton eltér A-tól
        (link-szintű eltérés, kapun átmenő) -> F4-nek lesz dolga;
      * hibabeállítások: hibas_elso (a 1. próbálkozásra rossz válaszú versek),
        hibas_mindig (a másodikra is rossz), nem_json_elso (a teljes válasz
        nem JSON az adott modellnél az adott hívássorszámon);
      * a C elutasítja az 'effort':'minimal' reasoninget 400-zal (a szint-
        visszalépés ága);
      * cost: a hívások 3.-ik minden hármasán nincs cost mező (tartalék ár ága).
    """

    def __init__(self, hibas_elso=(), hibas_mindig=(), nem_json_hivas=(), c_minimal_400=True,
                 koltseg_szorzo=1.0, biro_rossz_elso=(), biro_rossz_mindig=(),
                 egyedi_hibas_mindig=(), biro_strong_elso=(), biro_strong_mindig=(), b_variacio=None):
        # b_variacio: azok a versek, ahol a B eltér az A-tól (None: az igehely hash%4==0 szabálya)
        self.b_variacio = None if b_variacio is None else set(b_variacio)
        # egyedi_hibas_mindig: {(modell_id, igehely)} - csak az adott modell (és csak nem
        # döntőbírói hívásban) ad mindig Strong-mintás (kapun elbukó) választ az igehelyre;
        # biro_strong_*: a döntőbíró az első / minden próbálkozásra Strong-számot ír (5. pont)
        self.egyedi_hibas_mindig = set(egyedi_hibas_mindig)
        self.biro_strong_elso = set(biro_strong_elso)
        self.biro_strong_mindig = set(biro_strong_mindig)
        self.szovegek = []         # (modell_id, az első felhasználói üzenet szövege)
        # biro_rossz_*: a döntőbíró (F4) az első / minden próbálkozásra megsérti a
        # rögzítést (a nem vitatott 2. magyar szóhoz új linket ad; a kapun átmegy)
        self.biro_rossz_elso = set(biro_rossz_elso)
        self.biro_rossz_mindig = set(biro_rossz_mindig)
        self.hibas_elso = set(hibas_elso)
        self.hibas_mindig = set(hibas_mindig)
        self.nem_json_hivas = set(nem_json_hivas)   # {(modell_id, hivas_sorszam)}
        self.c_minimal_400 = c_minimal_400
        self.koltseg_szorzo = koltseg_szorzo
        self.hivasok = []          # (modell, verslista, van_assistant)
        self.kulcsok = []          # a kapott api_key-ek (ellenőrzéshez)
        self.sorszam = {}

    @staticmethod
    def _versek(uzenet):
        jel = '=== A FELDOLGOZANDÓ VERSEK'
        szoveg = uzenet.split(jel, 1)[1] if jel in uzenet else uzenet
        return [s[len('VERS: '):].strip() for s in szoveg.split('\n') if s.startswith('VERS: ')]

    @staticmethod
    def _helyes(ig, variacio):
        """Kapun átmenő párosítás: k. magyar szó -> min(k, ne). Variáció: az
        1. magyar szó a 2. eredetihez kötve (link-szintű eltérés)."""
        d = bemenet.vers_adat(ig)
        nk, ne = len(d['karoli_tokenek']), len(d['eredeti'])
        parok = [[k, [min(k, ne)]] for k in range(1, nk + 1)]
        if variacio and ne >= 2:
            parok[0] = [1, [2]]
        fedett = {e for p in parok for e in p[1]}
        return {'vers': ig, 'parok': parok, 'betoldas': [],
                'forditatlan': sorted(set(range(1, ne + 1)) - fedett)}

    @staticmethod
    def _rontas(obj):
        """A nem vitatott 2. magyar szóhoz új linket ad (kapun átmegy, a rögzítést sérti)."""
        es = obj['parok'][1][1]
        uj = next(e for e in (1, 3, 2) if e not in es)
        obj['parok'][1] = [obj['parok'][1][0], sorted(es + [uj])]
        obj['forditatlan'] = [e for e in obj['forditatlan'] if e != uj]
        return obj

    def _valasz_versekre(self, modell_id, igehelyek, masodik, biro=False):
        elemek = []
        for ig in igehelyek:
            if (ig in self.hibas_mindig or (ig in self.hibas_elso and not masodik)
                    or (not biro and (modell_id, ig) in self.egyedi_hibas_mindig)
                    or (biro and (ig in self.biro_strong_mindig or (ig in self.biro_strong_elso and not masodik)))):
                obj = self._helyes(ig, False)
                obj['megjegyzes'] = 'H1234'   # Strong-minta: az 5. kapupont fogja
            else:
                variacio = (modell_id == MODELLEK['B'] and ((hash_stabil(ig) % 4 == 0) if self.b_variacio is None else ig in self.b_variacio))
                obj = self._helyes(ig, variacio)
                if biro and (ig in self.biro_rossz_mindig or (ig in self.biro_rossz_elso and not masodik)):
                    obj = self._rontas(obj)
            elemek.append(obj)
        return json.dumps(elemek, ensure_ascii=False)

    def __call__(self, model_id, uzenetek, api_key, extra):
        self.kulcsok.append(api_key)
        if model_id == MODELLEK['C'] and self.c_minimal_400 and (extra.get('reasoning') or {}).get('effort') == 'minimal':
            return _MockValasz({'error': 'reasoning.effort minimal nem támogatott'}, status=400)
        n = self.sorszam[model_id] = self.sorszam.get(model_id, 0) + 1
        van_assistant = any(m['role'] == 'assistant' for m in uzenetek)
        igehelyek = self._versek(uzenetek[-1]['content'])
        self.hivasok.append((model_id, list(igehelyek), van_assistant))
        self.szovegek.append((model_id, uzenetek[0]['content']))
        if (model_id, n) in self.nem_json_hivas:
            tartalom = 'Elnézést, itt a megoldás: ez nem JSON.'
        else:
            tartalom = self._valasz_versekre(model_id, igehelyek, van_assistant,
                                             biro='DÖNTŐBÍRÓI SZEREP' in uzenetek[0]['content'])
        be = sum(len(m['content']) for m in uzenetek) // 3
        ki = len(tartalom) // 3
        ar_be, ar_ki = ARAK[model_id]
        gond = 200 if model_id == MODELLEK['C'] else 0
        usage = {'prompt_tokens': be, 'completion_tokens': ki + gond}
        if n % 2 == 0:
            usage['output_tokens_details'] = {'reasoning_tokens': gond}     # tartalék alak
        else:
            usage['completion_tokens_details'] = {'reasoning_tokens': gond}  # OpenRouter alak
        if n % 3 != 0:
            usage['cost'] = (be / 1e6 * ar_be + usage['completion_tokens'] / 1e6 * ar_ki) * self.koltseg_szorzo
        return _MockValasz({'choices': [{'message': {'content': tartalom}, 'finish_reason': 'stop'}],
                            'usage': usage})


def _hibas(fn):
    """Igaz, ha fn() VezerloHibát dob."""
    try:
        fn()
    except VezerloHiba:
        return True
    return False


def hash_stabil(s):
    """Folyamatok között is stabil hash (a beépített hash() véletlenített)."""
    h = 0
    for c in s:
        h = (h * 131 + ord(c)) % 1000003
    return h


def _onteszt_minta(minta):
    """Kis minta az R1/R2/R3/R4 rétegekből, a minta sorrendjében: 15 + 4 + 2 + 4."""
    darab = {'R1': 15, 'R2': 4, 'R3': 2, 'R4': 4}
    szam = {k: 0 for k in darab}
    ki = []
    for s in minta:
        r = s['reteg']
        if r in darab and szam[r] < darab[r]:
            szam[r] += 1
            ki.append(s)
    return ki


def _blokkok(szoveg):
    """{igehely: [sorok]} a hívás szövegének versblokkjaiból (a '=== A FELDOLGOZANDÓ' jel után)."""
    jel = '=== A FELDOLGOZANDÓ VERSEK'
    ki = {}
    for blokk in szoveg.split(jel, 1)[1].split('\n\n'):
        sorok = blokk.strip('\n').split('\n')
        for x in sorok:
            if x.startswith('VERS: '):
                ki[x[len('VERS: '):].strip()] = sorok
                break
    return ki


def _fuggetlen_rogzites(a_obj, b_obj):
    """A rögzítés függetlenül (nem a biro_rogzites kódjával) számolva, az onteszt bizonyításához."""
    def kmap(o):
        d = {}
        for k, es in o['parok']:
            d.setdefault(k, set()).update(es)
        for k in o['betoldas']:
            d.setdefault(k, set())
        return d, set(o['betoldas'])
    (ma, ba), (mb, bb) = kmap(a_obj), kmap(b_obj)
    la = {(k, e) for k, es in ma.items() for e in es}
    lb = {(k, e) for k, es in mb.items() for e in es}
    vit = sorted(k for k in set(ma) | set(mb)
                 if ma.get(k) != mb.get(k) or ((k in ba) != (k in bb)))
    return sorted(la & lb), vit


def onteszt_p3b(ellen, minta, teszt_kulcs, kimenet):
    """A P3b (F1V2, F2V2, F5V2, F6V2, F3V2B, F4V2) önteszt-ágai MOCK küldővel.

    kimenet: lista, amelybe a bizonyító sorok kerülnek (az önteszt végén kiírva).
    Visszaad: a létrehozott ideiglenes könyvtárak listája."""
    import hashlib
    import re
    mappak = []
    sorrend = ['F1V2', 'F2V2', 'F5V2', 'F6V2', 'F3V2B', 'F4V2']
    ig_all = [s_['igehely'] for s_ in minta]
    r1 = [s_['igehely'] for s_ in minta if s_['reteg'] == 'R1']
    A, B, C = MODELLEK['A'], MODELLEK['B'], MODELLEK['C']

    def mérete(ig):
        d_ = bemenet.vers_adat(ig)
        return len(d_['karoli_tokenek']), len(d_['eredeti'])

    # a B-eltérő (hash%4==0) versek közül a döntőbírói ágakhoz; az A/B-hibás versek NEM ezek közül
    hash4 = [ig for ig in ig_all if min(mérete(ig)) >= 3][::3][:6]     # ezeken a B eltér az A-tól
    ellen(len(hash4) >= 4, 'P3b önteszt-minta: nincs 4 B-eltérő vers a döntőbírói ágakhoz (%d)' % len(hash4))
    rossz_elso, rossz_mindig, strong_elso, strong_mindig = hash4[:4]
    semleges = [ig for ig in ig_all if ig not in hash4 and ig in r1 and min(mérete(ig)) >= 3]
    a_hiba, mind_hiba = semleges[2], semleges[5]          # A egyedül / A és B is kapuhibás marad
    mock = MockKuldo(egyedi_hibas_mindig={(A, a_hiba), (A, mind_hiba), (B, mind_hiba)}, b_variacio=hash4,
                     biro_rossz_elso={rossz_elso}, biro_rossz_mindig={rossz_mindig},
                     biro_strong_elso={strong_elso}, biro_strong_mindig={strong_mindig})
    mappa = tempfile.mkdtemp(prefix='f21p_onteszt_p3b_')
    mappak.append(mappa)
    ctx = Kontextus(mock, teszt_kulcs, mappa)
    vez = os.path.join(mappa, 'futtatas_teszt.txt')

    def vez_ir(tartalom):
        with open(vez, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tartalom)

    # --- a vezérlő: az új azonosítók, a sorrend, az F4/F4V2 szabályai, a plafon_usd ---
    vez_ir('futasok=F4V2,F1V2,F5V2,F6V2,F3V2B,F2V2\nkoteg_max=mind\nplafon_usd=2\n')
    v = vezerlo_beolvas(vez)
    ellen(v['futasok'] == sorrend and v['plafon_usd'] == 2.0 and v['koteg_max'] is None,
          'vezérlő: a P3b sorrendje/értelmezése hibás: %s' % (v,))
    vez_ir('futasok=F1V2,F2V2,F5V2,F6V2,F3V2B\nkoteg_max=mind\n')
    ellen(vezerlo_beolvas(vez)['futasok'] == sorrend[:5] and vezerlo_beolvas(vez)['plafon_usd'] is None,
          'vezérlő: a F4V2 nélküli sor értelmezése hibás')
    vez_ir('futasok=F4V2\nkoteg_max=mind\n')
    ellen(vezerlo_beolvas(vez)['futasok'] == ['F4V2'], 'vezérlő: az egyedül álló F4V2 elutasítva')
    vez_ir('futasok=F1,F4\nkoteg_max=mind\n')
    ellen(_hibas(lambda: vezerlo_beolvas(vez)), 'vezérlő: a régi F4 más futással együtt elfogadva')
    for jo in ('2', '2.0', '3', '3.0', '0.5'):
        vez_ir('futasok=F1V2\nkoteg_max=1\nplafon_usd=%s\n' % jo)
        ellen(vezerlo_beolvas(vez)['plafon_usd'] == float(jo), 'plafon_usd=%s elutasítva' % jo)
    for rossz in ('x', '0', '-1', '3.01', '10', 'nan', 'inf', '', '1,5'):
        vez_ir('futasok=F1V2\nkoteg_max=1\nplafon_usd=%s\n' % rossz)
        ellen(_hibas(lambda: vezerlo_beolvas(vez)), 'plafon_usd=%r elfogadva' % rossz)
    ctx_p = Kontextus(MockKuldo(), teszt_kulcs, mappa)
    vez_ir('futasok=F1V2\nkoteg_max=1\nplafon_usd=0.5\n')
    mappa_p = tempfile.mkdtemp(prefix='f21p_onteszt_p3b_plafonkulcs_')
    mappak.append(mappa_p)
    ctx_p = Kontextus(MockKuldo(), teszt_kulcs, mappa_p)
    vezerlo_futtat(ctx_p, vez, minta)
    ellen(ctx_p.plafon == 0.5, 'a plafon_usd nem érvényesült a kontextusban: %s' % ctx_p.plafon)
    vez_ir('futasok=F1V2\nkoteg_max=1\n')
    ctx_q = Kontextus(MockKuldo(), teszt_kulcs, mappa_p)
    vezerlo_futtat(ctx_q, vez, minta)
    ellen(ctx_q.plafon == PLAFON_USD, 'plafon_usd nélkül a plafon nem a 3.0 kemény korlát: %s' % ctx_q.plafon)

    # --- a teljes P3b egy triggerben, rendezetlenül felsorolva, plafon_usd=2 ------------------
    vez_ir('futasok=F4V2,F1V2,F5V2,F6V2,F3V2B,F2V2\nkoteg_max=mind\nplafon_usd=2\n')
    kod = vezerlo_futtat(ctx, vez, minta)
    ellen(kod == 0 and ctx.plafon == 2.0, 'P3b: kilépési kód %d, plafon %s' % (kod, ctx.plafon))
    with open(naplo_ut(mappa), encoding='utf-8') as f:
        naplo = [dict(zip(NAPLO_FEJLEC, x.rstrip('\n').split('\t'))) for x in list(f)[1:] if x.strip()]
    elso_sor = {}
    for i, r in enumerate(naplo):
        elso_sor.setdefault(r['futas'], i)
    ellen([f_ for f_ in sorted(elso_sor, key=elso_sor.get)] == sorrend,
          'P3b: a futási sorrend a naplóban nem %s: %s' % (sorrend, sorted(elso_sor, key=elso_sor.get)))
    for f_ in sorrend:
        ellen(os.path.exists(valasz_ut(f_, mappa)), 'P3b: nincs kimenet: %s' % f_)
    # prompt-azonosítók a naplóban
    sha_v2 = bemenet.prompt_sha256(bemenet.PROMPT_V2_UT)[:12]
    sha_v1 = bemenet.prompt_sha256()[:12]
    sha_biro_v2 = biro_sha256(bemenet.PROMPT_V2_UT)[:12]
    sha_biro_v1 = biro_sha256()[:12]
    ellen(len({sha_v1, sha_v2, sha_biro_v1, sha_biro_v2}) == 4, 'a prompt-azonosítók nem különböznek')
    ellen(all(r['prompt_sha256_12'] == sha_v2 for r in naplo if r['futas'] != 'F4V2'), 'a V2 futások naplója nem a v2 sha-t viseli')
    ellen(all(r['prompt_sha256_12'] == sha_biro_v2 for r in naplo if r['futas'] == 'F4V2'),
          'F4V2: a napló nem a v2-alapú döntőbírói sha-t viseli')
    # F3V2B: a F3V2 2. futása, jelölve; ugyanazok a kötegek
    f3b = koteg_sorok('F3V2B', mappa)
    ellen(f3b and all(x.get('ismetles_of') == 'F3V2' for x in f3b), 'F3V2B: hiányzik az ismetles_of jelölés')
    ellen([x['igehelyek'] for x in f3b] == bemenet.kotegek(ig_all, KOTEG_MERET), 'F3V2B: nem ugyanazok a kötegek, mint a F3V2-é lenne')
    ellen(all(x['modell'] == C for x in f3b), 'F3V2B: nem a C modell')
    # F5V2/F6V2: csak az R1, KJV nélkül; F1V2/F2V2: 25 vers
    ellen(set(eredmenyek_betolt('F5V2', mappa)) == set(r1) and set(eredmenyek_betolt('F6V2', mappa)) == set(r1),
          'F5V2/F6V2: nem pontosan az R1')
    ellen('KJV-TÁMPONT: ' not in kotegszoveg_futashoz('F5V2', r1[:2], mappa).split('=== A FELDOLGOZANDÓ')[1]
          and 'KJV-TÁMPONT: ' in kotegszoveg_futashoz('F1V2', r1[:2], mappa).split('=== A FELDOLGOZANDÓ')[1],
          'F5V2 KJV nélkül / F1V2 KJV-val hibás')
    ellen(len(eredmenyek_betolt('F1V2', mappa)) == 25 and len(eredmenyek_betolt('F2V2', mappa)) == 25, 'F1V2/F2V2 nem teljes')

    e1, e2, e4 = (eredmenyek_betolt(f_, mappa) for f_ in ('F1V2', 'F2V2', 'F4V2'))
    v4 = verslista('F4V2', minta, mappa)
    ellen(v4 == [ig for ig in ig_all if elter(e1[ig], e2[ig])] and a_hiba in v4 and mind_hiba in v4,
          'F4V2: a versek nem az eltérő/kapuhibás versek')
    ellen(set(e4) == set(v4), 'F4V2: a mentett versek nem egyeznek a versekkel')
    kimenet.append('F4V2 versei: %d/25 (eltérő linkű vagy kapuhibás A/B); ebből A és B is kapun átment: %d, csak egyik ment át: %d, egyik sem: %d'
                   % (len(v4), sum(1 for ig in v4 if e1[ig]['allapot'] == 'ok' and e2[ig]['allapot'] == 'ok'),
                      sum(1 for ig in v4 if (e1[ig]['allapot'] == 'ok') != (e2[ig]['allapot'] == 'ok')),
                      sum(1 for ig in v4 if e1[ig]['allapot'] != 'ok' and e2[ig]['allapot'] != 'ok')))

    # --- (1) RÖGZÍTETT LINKEK = A∩B, a 6. kapupont -------------------------------------------
    c_szovegek = [t for m_, t in mock.szovegek if m_ == C and 'DÖNTŐBÍRÓI SZEREP' in t]
    ellen(c_szovegek, 'F4V2: nem volt döntőbírói hívás')
    ellen(all('Párosítási szabályok' in t for t in c_szovegek), 'F4V2: a C bemenete nem a prompt_v2 alapú (hiányzik a Párosítási szabályok)')
    ellen(all(bemenet.prompt_utasitas(bemenet.PROMPT_V2_UT) in t for t in c_szovegek),
          'F4V2: a C bemenete nem tartalmazza szó szerint a prompt_v2 utasításrészét')
    kiegeszites = biro_utasitas(bemenet.PROMPT_V2_UT)[len(bemenet.prompt_utasitas(bemenet.PROMPT_V2_UT)):]
    with open(BIRO_PROMPT_UT, encoding='utf-8') as f:
        biro_fajl = f.read()
    ellen(kiegeszites.strip() in biro_fajl.replace('\r\n', '\n'), 'F4V2: a döntőbírói kiegészítés nem a prompt_biro_v2.md tartalma')
    blokk_szerint = {}
    for t in c_szovegek:
        for ig, sorok in _blokkok(t).items():
            blokk_szerint.setdefault(ig, sorok)
    ellen(set(blokk_szerint) == set(v4), 'F4V2: a C bemenetében nem pontosan az F4V2 versei vannak')
    egyezo_db = 0
    for ig in v4:
        sorok = blokk_szerint[ig]
        if e1[ig]['allapot'] == 'ok' and e2[ig]['allapot'] == 'ok':
            fix_l, vit = _fuggetlen_rogzites(e1[ig]['obj'], e2[ig]['obj'])
            s_link = [x for x in sorok if x.startswith('RÖGZÍTETT LINKEK (')]
            s_vit = [x for x in sorok if x.startswith('VITATOTT MAGYAR SZAVAK')]
            ok_l = bool(s_link) and sorted(tuple(x) for x in json.loads(s_link[0].split('): ', 1)[1])) == fix_l
            ok_v = bool(s_vit) and json.loads(s_vit[0].split('): ', 1)[1]) == vit
            ellen(ok_l and ok_v, 'F4V2 (1): %s: a RÖGZÍTETT LINKEK nem az A∩B / a VITATOTT nem a független számítás (%s)' % (ig, sorok))
            egyezo_db += 1
            if egyezo_db == 1:
                kimenet.append('(1) példa %s: A∩B független számítása = %s; a C bemenetében: %s; vitatott magyar szavak: %s'
                               % (ig, fix_l, s_link[0].split('): ', 1)[1], vit))
    ellen(egyezo_db > 0, 'F4V2: nincs olyan vers, ahol A és B is átment')
    # a 6. pont eltérésnél hibát ad: a mock-beli sértő válasz első próbája, a nyers válaszból újraellenőrizve
    sor_rossz = next(x for x in koteg_sorok('F4V2', mappa) if rossz_elso in x['igehelyek'])
    r_elso = valasz_ellenoriz_futashoz('F4V2', sor_rossz['nyers'][0], sor_rossz['igehelyek'], mappa)
    ellen(not r_elso[rossz_elso]['ok'] and r_elso[rossz_elso]['hibak']
          and r_elso[rossz_elso]['hibak'][0].startswith('6. ezeknek a nem vitatott'),
          'F4V2 (1): a nem vitatott szó megváltoztatása nem kapott 6. pontos hibát: %s' % (r_elso[rossz_elso]['hibak'],))
    ellen(e4[rossz_elso]['allapot'] == 'ok' and e4[rossz_elso]['probalkozas'] == 2, 'F4V2: a sértő válasz újrakérése nem javított')
    ellen(e4[rossz_mindig]['allapot'] == 'kapuhiba' and e4[rossz_mindig]['probalkozas'] == 2
          and e4[rossz_mindig]['hibak'][0].startswith('6.') and e4[rossz_mindig]['obj'] is None,
          'F4V2 (1): a tartósan sértő válasz nem maradt 6. pontos kapuhiba')
    kimenet.append('(1) 6. pont, a nem vitatott szó átkötése (%s, 1. próba): %s' % (rossz_elso, r_elso[rossz_elso]['hibak'][0][:120]))
    kimenet.append('(1) tartós sértés (%s): állapot=%s, próbálkozás=%d, hiba: %s'
                   % (rossz_mindig, e4[rossz_mindig]['allapot'], e4[rossz_mindig]['probalkozas'], e4[rossz_mindig]['hibak'][0][:100]))
    # a rögzített link elvétele is hibát ad (egységpróba a valódi A/B rekordokon)
    kozos = next(ig for ig in v4 if e1[ig]['allapot'] == 'ok' and e2[ig]['allapot'] == 'ok')
    c_jo = json.loads(json.dumps(e1[kozos]['obj']))
    ellen(biro_kenyszer(c_jo, e1[kozos], e2[kozos]) == [], 'F4V2 (1): az A válasza nem felel meg a rögzítésnek')
    rog_l, _, vit_k = biro_rogzites(e1[kozos], e2[kozos])
    k_fix = next(k for k, _ in rog_l if k not in vit_k)
    c_rossz = json.loads(json.dumps(c_jo))
    c_rossz['parok'] = [p_ for p_ in c_rossz['parok'] if p_[0] != k_fix]
    c_rossz['betoldas'] = sorted(c_rossz['betoldas'] + [k_fix])
    h_l = biro_kenyszer(c_rossz, e1[kozos], e2[kozos])
    ellen(any(x.startswith('6. rögzített') for x in h_l), 'F4V2 (1): az elvett rögzített link nem kapott 6. pontos hibát')
    kimenet.append('(1) 6. pont, elvett rögzített link (%s, k=%d): %s' % (kozos, k_fix, h_l[0][:110]))

    # --- (2) ugyanaz a kapu és séma -------------------------------------------------------------
    ellen(mentett_valaszok_ellenoriz('F4V2', mappa) == [], 'F4V2 (2): a mentett válaszok nem mennek át az ötpontos kapun és a 6. ponton')
    ok4 = [ig for ig in e4 if e4[ig]['allapot'] == 'ok']
    ellen(ok4 and all(set(e4[ig]['obj']) == {'vers', 'parok', 'betoldas', 'forditatlan'} for ig in ok4)
          and all(set(e1[ig]['obj']) == set(e4[ok4[0]]['obj']) for ig in e1 if e1[ig]['allapot'] == 'ok'),
          'F4V2 (2): a séma nem azonos az A/B válaszáéval')
    ellen(all(not kapu.vers_ellenoriz(e4[ig]['obj'], bemenet.vers_adat(ig)) for ig in ok4),
          'F4V2 (2): van mentett válasz, amely a kapu.vers_ellenoriz-en elbukik')
    kimenet.append('(2) %d mentett F4V2-válasz átmegy a kapu.vers_ellenoriz-en (5 pont) és a biro_kenyszer-en (6. pont); '
                   'mezők: vers, parok, betoldas, forditatlan (mint az A/B-é)' % len(ok4))

    # --- (3) K5: nincs Strong-szám -------------------------------------------------------------------
    sor_strong = next(x for x in koteg_sorok('F4V2', mappa) if strong_elso in x['igehelyek'])
    r_s = valasz_ellenoriz_futashoz('F4V2', sor_strong['nyers'][0], sor_strong['igehelyek'], mappa)
    ellen(not r_s[strong_elso]['ok'] and any(x.startswith('5.') for x in r_s[strong_elso]['hibak']),
          'F4V2 (3): a Strong-számot író C-válasz nem kapott 5. pontos hibát')
    ellen(e4[strong_elso]['allapot'] == 'ok' and e4[strong_elso]['probalkozas'] == 2, 'F4V2 (3): a Strong-számos válasz újrakérése nem javított')
    ellen(e4[strong_mindig]['allapot'] == 'kapuhiba' and any(x.startswith('5.') for x in e4[strong_mindig]['hibak'])
          and e4[strong_mindig]['obj'] is None, 'F4V2 (3): a tartósan Strong-számos válasz nem maradt kapuhiba')
    minta_strong = re.compile(r'[HG]\d{3,4}')
    ellen(all(not minta_strong.search(json.dumps(e4[ig]['obj'], ensure_ascii=False)) for ig in ok4),
          'F4V2 (3): mentett válaszban Strong-szám van')
    # a mentett válaszok újraellenőrzése észleli a beírt Strong-számot (manipulált másolaton)
    mappa_t = tempfile.mkdtemp(prefix='f21p_onteszt_p3b_mentett_')
    mappak.append(mappa_t)
    os.makedirs(os.path.join(mappa_t, 'valaszok'))
    for f_ in ('F1V2', 'F2V2', 'F4V2'):
        shutil.copy(valasz_ut(f_, mappa), valasz_ut(f_, mappa_t))
    sorok_t = koteg_sorok('F4V2', mappa_t)
    jel_ig = next(ig for ig in sorok_t[0]['igehelyek'] if sorok_t[0]['versek'][ig]['allapot'] == 'ok')
    sorok_t[0]['versek'][jel_ig]['obj']['megjegyzes'] = 'G1234'
    with open(valasz_ut('F4V2', mappa_t), 'w', encoding='utf-8', newline='\n') as f:
        for x in sorok_t:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    h_t = mentett_valaszok_ellenoriz('F4V2', mappa_t)
    ellen(any('5.' in x and jel_ig in x for x in h_t), 'F4V2 (3): a mentett válaszok újraellenőrzése nem vette észre a beírt Strong-számot: %s' % h_t)
    kimenet.append('(3) K5: a Strong-számot író C-válasz 1. próbája: %s; 2. próbán javul (%s), tartós esetben kapuhiba (%s); '
                   'a mentett válaszok újraellenőrzése a manipulált másolatban jelzi: %s'
                   % (r_s[strong_elso]['hibak'][0][:70], strong_elso, strong_mindig, h_t[0][:80]))

    # --- az A vagy B kapuhibás maradt versek: nincs mit rögzíteni ---------------------------------
    for ig, nev in ((a_hiba, 'csak az A kapuhibás'), (mind_hiba, 'A és B is kapuhibás')):
        ellen(biro_rogzites(e1[ig], e2[ig]) is None, 'F4V2: %s: van rögzítés' % nev)
        ellen('RÖGZÍTETT: nincs' in '\n'.join(blokk_szerint[ig]) and 'RÖGZÍTETT LINKEK' not in '\n'.join(blokk_szerint[ig]),
              'F4V2: %s: a C bemenetében nincs „RÖGZÍTETT: nincs” sor' % nev)
        ellen(e4[ig]['allapot'] == 'ok' and e4[ig]['probalkozas'] == 1, 'F4V2: %s: a C teljes párosítása nem ment át' % nev)
        ellen(biro_kenyszer(e4[ig]['obj'], e1[ig], e2[ig]) == [], 'F4V2: %s: a 6. pont mégis hibát ad' % nev)
        kimenet.append('kapuhibás A/B (%s, %s): rögzítés = None, C teljes párosítást ad (állapot=%s, próbálkozás=%d); a 6. pont nem kényszerít'
                       % (ig, nev, e4[ig]['allapot'], e4[ig]['probalkozas']))

    # --- újraindítás, plafon_usd=2 leállás, folytatás -----------------------------------------------
    db = len(mock.hivasok)
    kod = vezerlo_futtat(ctx, vez, minta)
    ellen(kod == 0 and len(mock.hivasok) == db, 'P3b újraindítás: új hívás történt (%d)' % (len(mock.hivasok) - db))
    mappa_l = tempfile.mkdtemp(prefix='f21p_onteszt_p3b_plafon_')
    mappak.append(mappa_l)
    ctx_l = Kontextus(MockKuldo(), teszt_kulcs, mappa_l)
    vez_ir('futasok=F1V2,F2V2,F5V2,F6V2,F3V2B,F4V2\nkoteg_max=mind\nplafon_usd=0.004\n')
    kod = vezerlo_futtat(ctx_l, vez, minta)
    ossz_l = naplo_osszeg(mappa_l)
    ellen(kod == KILEPES_PLAFON and 0 < ossz_l <= 0.004, 'P3b plafon_usd: kilépési kód %d, napló-összeg %.6f' % (kod, ossz_l))
    kesz_l = sum(len(eredmenyek_betolt(f_, mappa_l)) for f_ in sorrend)
    ellen(kesz_l > 0, 'P3b plafon_usd: nincs mentett sor a leállás előtt')
    vez_ir('futasok=F1V2,F2V2,F5V2,F6V2,F3V2B,F4V2\nkoteg_max=mind\nplafon_usd=2\n')
    ctx_l = Kontextus(MockKuldo(), teszt_kulcs, mappa_l)   # új folyamat: új kontextus
    kod = vezerlo_futtat(ctx_l, vez, minta)
    ellen(kod == 0 and len(eredmenyek_betolt('F4V2', mappa_l)) > 0, 'P3b plafon_usd: a folytatás nem fejeződött be (kód %d)' % kod)
    ellen(all(len({tuple(x['igehelyek']) for x in koteg_sorok(f_, mappa_l)}) == len(koteg_sorok(f_, mappa_l)) for f_ in sorrend),
          'P3b plafon_usd: duplikált köteg a folytatás után')
    kimenet.append('plafon_usd: 0.004 USD-nél leállás (kilépési kód %d, napló %.6f USD, %d kész sor), 2 USD-vel folytatás rendben, nincs duplikált köteg'
                   % (KILEPES_PLAFON, ossz_l, kesz_l))

    # --- F4V2 előfeltétele ---------------------------------------------------------------------------
    mappa_e = tempfile.mkdtemp(prefix='f21p_onteszt_p3b_elofeltetel_')
    mappak.append(mappa_e)
    ctx_e = Kontextus(MockKuldo(), teszt_kulcs, mappa_e)
    vez_ir('futasok=F4V2\nkoteg_max=mind\n')
    ellen(vezerlo_futtat(ctx_e, vez, minta) == 2 and not os.path.exists(valasz_ut('F4V2', mappa_e)),
          'F4V2 előfeltétel nélkül nem 2-es kód')
    vez_ir('futasok=F1V2,F2V2,F4V2\nkoteg_max=1\n')
    kod = vezerlo_futtat(ctx_e, vez, minta)
    ellen(kod == 2 and len(eredmenyek_betolt('F1V2', mappa_e)) == 10 and len(eredmenyek_betolt('F2V2', mappa_e)) == 10
          and not os.path.exists(valasz_ut('F4V2', mappa_e)),
          'F4V2 részleges F1V2/F2V2 mellett: kód %d, F4V2 kimenet van: %s' % (kod, os.path.exists(valasz_ut('F4V2', mappa_e))))
    kimenet.append('F4V2 előfeltétel: F1V2/F2V2 nélkül és részleges (koteg_max=1) F1V2/F2V2 mellett kilépési kód 2, F4V2 nem hív')

    # --- befagyasztás -------------------------------------------------------------------------------
    ellen(befagyasztas_ellenoriz() == [], 'a befagyasztott bemenetek ellenőrzése hibát ad: %s' % befagyasztas_ellenoriz())
    mappa_f = tempfile.mkdtemp(prefix='f21p_onteszt_p3b_fagy_')
    mappak.append(mappa_f)
    os.makedirs(os.path.join(mappa_f, 'f21p'))
    for rel in BEFAGYASZTOTT:
        shutil.copy(os.path.join(tokenek.ROOT, *rel.split('/')), os.path.join(mappa_f, *rel.split('/')))
    ellen(befagyasztas_ellenoriz(gyoker=mappa_f, arany=False) == [], 'befagyasztás: az eredeti másolat hibás')
    ut_v2 = os.path.join(mappa_f, 'f21p', 'prompt_v2.md')
    with open(ut_v2, 'a', encoding='utf-8') as f:
        f.write('\nmódosítás\n')
    ellen(any('prompt_v2.md' in x for x in befagyasztas_ellenoriz(gyoker=mappa_f, arany=False)),
          'befagyasztás: a módosított prompt_v2.md-t nem vette észre')
    kimenet.append('befagyasztás: prompt_v1/v2/biro_v2 és arany v2 sha256 egyezik; a módosított prompt_v2 másolatot észreveszi')
    return mappak


def onteszt():
    """A futtató logika végigfuttatása MOCK küldővel néhány vers fölött.

    Ágak: normál, kapuhiba -> újrakérés sikeres, kapuhiba -> újrakérés is
    hibás (kapuhiba marad), nem-JSON teljes válasz, C 400-as reasoning-
    visszalépés, hiányzó cost (tartalék ár), F4 eltérő versek, újraindítás
    (kész köteg nem hív újra), plafon-leállás (kilépési kód 3) és folytatás,
    kulcs nem szivárog, F5/F6 KJV nélkül.
    """
    hibak = []

    def ellen(feltetel, leiras):
        if not feltetel:
            hibak.append(leiras)

    minta = _onteszt_minta(minta_betolt())
    ellen(len(minta) == 25, 'az önteszt-minta nem 25 vers: %d' % len(minta))
    teszt_kulcs = 'sk-' + 'or-v1-TESZTKULCS0123456789abcdef0123456789'  # a forrásban nem kulcs-szerű
    ossz_futas = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F3V2']

    # --- 1. teljes menet hibaágakkal ---------------------------------------
    mappa = tempfile.mkdtemp(prefix='f21p_onteszt_')
    r1 = [s['igehely'] for s in minta if s['reteg'] == 'R1']
    elso_hibas = {r1[1], r1[12]}                 # 1. próbálkozásra Strong-mintás -> újrakérés sikeres
    mindig_hibas = {r1[3]}                       # a másodikra is -> kapuhiba marad
    # F4-ágak: a B 4. verse (hash) eltér, ezek közül kettőnél a döntőbíró megsérti a rögzítést
    jeloltek = [ig for ig in r1 if hash_stabil(ig) % 4 == 0 and ig not in elso_hibas | mindig_hibas]
    ellen(len(jeloltek) >= 2, 'önteszt-minta: nincs két B-eltérő R1 vers az F4-ágakhoz')
    biro_elso, biro_mindig = jeloltek[0], jeloltek[1]
    mock = MockKuldo(hibas_elso=elso_hibas, hibas_mindig=mindig_hibas,
                     nem_json_hivas={(MODELLEK['B'], 3)},
                     biro_rossz_elso={biro_elso}, biro_rossz_mindig={biro_mindig})
    ctx = Kontextus(mock, teszt_kulcs, mappa, plafon=PLAFON_USD)
    kod = futasok_vegrehajt(ctx, ossz_futas, minta)
    ellen(kod == 0, '1. menet kilépési kódja %d, várt 0' % kod)

    e1 = eredmenyek_betolt('F1', mappa)
    ellen(len(e1) == 25, 'F1: %d vers a várt 25 helyett' % len(e1))
    ellen(e1[r1[1]]['allapot'] == 'ok' and e1[r1[1]]['probalkozas'] == 2, 'F1: újrakérés nem javított')
    ellen(e1[r1[3]]['allapot'] == 'kapuhiba' and e1[r1[3]]['probalkozas'] == 2, 'F1: a tartós hiba nem maradt kapuhiba')
    ellen(all(e1[ig]['probalkozas'] == 1 for ig in r1 if ig not in elso_hibas | mindig_hibas),
          'F1: felesleges újrakérés')
    e2 = eredmenyek_betolt('F2', mappa)
    ellen(all(e2[ig]['allapot'] == 'ok' or ig in mindig_hibas for ig in e2), 'F2: a nem-JSON köteg újrakérése nem mentett')
    ellen(any(e['probalkozas'] == 2 for e in e2.values()), 'F2: nincs újrakérés a nem-JSON válasz után')
    # F4: pontosan az eltérő (vagy kapuhibás) versek
    v4 = verslista('F4', minta, mappa)
    varhato = [s['igehely'] for s in minta
               if elter(e1[s['igehely']], e2[s['igehely']])]
    ellen(v4 == varhato and len(v4) > 0, 'F4: az eltérő versek nem egyeznek (%d vs %d)' % (len(v4), len(varhato)))
    ellen(set(eredmenyek_betolt('F4', mappa)) == set(v4), 'F4: a döntőbírói válasz versei hiányosak')
    ellen(r1[3] in v4, 'F4: a kapuhibás vers nem került a döntőbíróhoz')
    # F4: a rögzítés gépi kényszerítése
    e4 = eredmenyek_betolt('F4', mappa)
    ellen(e4[biro_elso]['allapot'] == 'ok' and e4[biro_elso]['probalkozas'] == 2,
          'F4: a rögzítést sértő döntőbírói válasz újrakérése nem javított')
    ellen(e4[biro_mindig]['allapot'] == 'kapuhiba' and e4[biro_mindig]['probalkozas'] == 2
          and e4[biro_mindig]['hibak'] and e4[biro_mindig]['hibak'][0].startswith('6.'),
          'F4: a tartósan rögzítést sértő válasz nem maradt kapuhiba 6. ponttal')
    ok_v4 = [ig for ig in v4 if e4[ig]['allapot'] == 'ok']
    ellen(all(not biro_kenyszer(e4[ig]['obj'], e1[ig], e2[ig]) for ig in ok_v4),
          'F4: a mentett döntőbírói válaszok nem mind felelnek meg a rögzítésnek')
    # biro_rogzites / biro_kenyszer egységpróbák valódi (mock) rekordokon
    kozos = next(ig for ig in v4 if e1[ig]['allapot'] == 'ok' and e2[ig]['allapot'] == 'ok')
    rog = biro_rogzites(e1[kozos], e2[kozos])
    ellen(rog is not None and rog[2] == [1], 'biro_rogzites: a vitatott szavak nem [1]: %s' % (rog,))
    ellen(biro_kenyszer(e1[kozos]['obj'], e1[kozos], e2[kozos]) == [], 'biro_kenyszer: az A válasza nem felel meg')
    ossz = json.loads(json.dumps(e1[kozos]['obj']))
    ossz['parok'][2] = [ossz['parok'][2][0], [e_ + 100 for e_ in ossz['parok'][2][1]]]   # egy rögzített link módosítva
    ellen(any(h.startswith('6.') for h in biro_kenyszer(ossz, e1[kozos], e2[kozos])),
          'biro_kenyszer: a módosított rögzített linket nem fogta meg')
    tort = json.loads(json.dumps(e1[kozos]['obj']))
    tort['parok'] = [p_ for p_ in tort['parok'] if p_[0] != 2]
    tort['betoldas'] = sorted(tort['betoldas'] + [2])
    ellen(any(h.startswith('6.') for h in biro_kenyszer(tort, e1[kozos], e2[kozos])),
          'biro_kenyszer: a rögzített szó betoldássá tételét nem fogta meg')
    szabad = json.loads(json.dumps(e1[kozos]['obj']))   # a vitatott 1. szó átkötése megengedett
    szabad['parok'][0] = e2[kozos]['obj']['parok'][0]
    szabad['forditatlan'] = e2[kozos]['obj']['forditatlan']
    ellen(biro_kenyszer(szabad, e1[kozos], e2[kozos]) == [],
          'biro_kenyszer: a vitatott szó átkötése tiltott lett: %s' % biro_kenyszer(szabad, e1[kozos], e2[kozos]))
    ellen(biro_kenyszer(tort, e1[r1[3]], e2[r1[3]]) == [], 'biro_kenyszer: kapuhibás A/B mellett is kényszerít')
    szoveg_biro = biro_kotegszoveg([kozos, r1[3]], e1, e2, True)
    ellen('RÖGZÍTETT LINKEK (A és B egyezik' in szoveg_biro and 'VITATOTT MAGYAR SZAVAK (csak ezekről döntesz): [1]' in szoveg_biro,
          'a döntőbírói bemenetben nincs rögzítés / vitatott sor')
    ellen('RÖGZÍTETT: nincs (legalább az egyik modell' in szoveg_biro, 'a kapuhibás versnél nincs "nincs rögzítés" sor')
    ellen('DÖNTŐBÍRÓI SZEREP' in biro_utasitas() and 'RÖGZÍTETT LINKEK' in biro_utasitas(), 'a v2 prompt nincs betöltve')
    # F5/F6: csak az R1, KJV nélkül
    ellen(set(eredmenyek_betolt('F5', mappa)) == set(r1), 'F5: nem pontosan az R1 versei')
    ellen(set(eredmenyek_betolt('F6', mappa)) == set(r1), 'F6: nem pontosan az R1 versei')
    szoveg_kjv = bemenet.kotegszoveg(r1[:2], True)
    szoveg_nokjv = bemenet.kotegszoveg(r1[:2], False)
    ellen('KJV-TÁMPONT: ' in szoveg_kjv.split('=== A FELDOLGOZANDÓ')[1], 'F1: az R1-en nincs KJV-támpont')
    ellen('KJV-TÁMPONT: ' not in szoveg_nokjv.split('=== A FELDOLGOZANDÓ')[1], 'F5/F6: KJV-támpont maradt a bemenetben')
    # F3V2 (F21.12): C, a teljes (önteszt-)minta, prompt_v2, külön kimenet
    e3v2 = eredmenyek_betolt('F3V2', mappa)
    ellen(len(e3v2) == 25 and all(r['allapot'] == 'ok' or ig in mindig_hibas for ig, r in e3v2.items())
          and all(e3v2[ig]['allapot'] == 'kapuhiba' for ig in mindig_hibas),
          'F3V2: a 25 vers állapota nem a várt (a tartós hibás vers kapuhiba, a többi rendben)')
    ellen(os.path.exists(valasz_ut('F3V2', mappa)) and valasz_ut('F3V2', mappa).endswith(os.path.join('valaszok', 'F3V2.jsonl')),
          'F3V2: nincs külön kimenet (valaszok/F3V2.jsonl)')
    ellen(all(s_['modell'] == MODELLEK['C'] for s_ in koteg_sorok('F3V2', mappa)), 'F3V2: nem a C modell futott')
    sha_v1 = bemenet.prompt_sha256()[:12]
    sha_v2 = bemenet.prompt_sha256(bemenet.PROMPT_V2_UT)[:12]
    ellen(sha_v1 != sha_v2, 'a prompt_v2 utasításrésze azonos a v1-ével')
    ellen(utasitas_sha12('F3V2') == sha_v2 and utasitas_sha12('F3') == sha_v1,
          'F3V2/F3: a napló prompt-azonosítója nem a v2 ill. v1 promptot jelöli')
    ellen('Párosítási szabályok' in kotegszoveg_futashoz('F3V2', r1[:1], mappa)
          and 'Párosítási szabályok' not in kotegszoveg_futashoz('F3', r1[:1], mappa),
          'F3V2: a hívás szövege nem a prompt_v2 (vagy az F3 is azt kapja)')
    pr2 = bemenet.prompt_utasitas(bemenet.PROMPT_V2_UT)
    ellen('{{VERSBLOKK' not in pr2 and 'DÖNTŐBÍRÓI SZEREP' not in pr2, 'prompt_v2: helyőrző maradt, vagy döntőbírói jel van benne')
    peldak_v2 = [json.loads(s_) for s_ in pr2.split('\n')
                 if s_.startswith('{"vers":') and not s_.startswith('{"vers":"<')]   # a sémasor nem példa
    ellen(len(peldak_v2) == 2 and all(bemenet.versblokk(o_['vers'], kjv=True) in pr2
                                      and not kapu.vers_ellenoriz(o_, bemenet.vers_adat(o_['vers'])) for o_ in peldak_v2),
          'prompt_v2: a két példa nincs meg, vagy nem megy át a kapun')
    minta_ig = {s_['igehely'] for s_ in minta_betolt()}
    ellen(not any(o_['vers'] in minta_ig for o_ in peldak_v2), 'prompt_v2: a példa a pilotmintából való')
    # F21.14: a példaversekben nincs konvenció nélküli jelenség (való, [nem TR], tárgyrag az igén)
    ellen([o_['vers'] for o_ in peldak_v2] == ['1Móz 1:1', 'Ján 1:1'], 'prompt_v2: a példaversek nem 1Móz 1:1 és Ján 1:1')
    os_sorok = {ig_ for ig_ in (o_['vers'] for o_ in peldak_v2)
                for r_ in tokenek._sorok(tokenek.TAHOT) if r_[0] == ig_ and r_[4].startswith('Os')}
    ellen(not any('való' in [t_.lower() for t_ in bemenet.vers_adat(o_['vers'])['karoli_tokenek']]
                  or any(w_['nem_tr'] for w_ in bemenet.vers_adat(o_['vers'])['eredeti']) for o_ in peldak_v2)
          and not os_sorok,
          'prompt_v2: a példaversben „való”, [nem TR] token vagy tárgyi rag van')
    naplo_f3v2 = []
    with open(naplo_ut(mappa), encoding='utf-8') as f:
        fej_ = f.readline().rstrip('\n').split('\t')
        for s_ in f:
            m_ = dict(zip(fej_, s_.rstrip('\n').split('\t')))
            if m_['futas'] == 'F3V2':
                naplo_f3v2.append(m_)
    ellen(naplo_f3v2 and all(m_['prompt_sha256_12'] == sha_v2 for m_ in naplo_f3v2),
          'F3V2: a futásnapló sorai nem a prompt_v2 sha-ját viselik')
    # a plafon kumulatív: a korábbi futások naplóösszege az F3V2-t is korlátozza
    mappa6 = tempfile.mkdtemp(prefix='f21p_onteszt_f3v2_plafon_')
    ctx6 = Kontextus(MockKuldo(), teszt_kulcs, mappa6)
    futasok_vegrehajt(ctx6, ['F1'], minta)
    ctx6.plafon = naplo_osszeg(mappa6) + 0.00001
    kod6 = futasok_vegrehajt(ctx6, ['F3V2'], minta)
    ellen(kod6 == KILEPES_PLAFON and eredmenyek_betolt('F3V2', mappa6) == {},
          'F3V2: a kumulatív plafon nem állította meg (kód %d)' % kod6)
    shutil.rmtree(mappa6, ignore_errors=True)
    # C reasoning-visszalépés
    ellen(ctx.c_reasoning_index == 1, 'C: a 400-as effort=minimal után nem lépett vissza low-ra')
    # napló
    with open(naplo_ut(mappa), encoding='utf-8') as f:
        naplo = [s.rstrip('\n').split('\t') for s in f if s.strip()]
    ellen(naplo[0] == NAPLO_FEJLEC, 'a futásnapló fejléce hibás')
    i_forras = NAPLO_FEJLEC.index('koltseg_forras')
    ellen({s[i_forras] for s in naplo[1:]} == {'openrouter', 'ar_config'}, 'a tartalék-ár ága nem futott')
    ellen(any(s[NAPLO_FEJLEC.index('gondolkodas_mod')] == 'kotelezo_effort=low' for s in naplo[1:]),
          'a C gondolkodási mód nincs a naplóban')
    ellen(any(int(s[NAPLO_FEJLEC.index('kapuhiba_db')]) > 0 for s in naplo[1:]), 'kapuhiba nincs a naplóban')
    i_gond = NAPLO_FEJLEC.index('gondolkodas_token')
    i_modell = NAPLO_FEJLEC.index('modell')
    c_sorok = [s for s in naplo[1:] if s[i_modell] == MODELLEK['C']]
    ellen(c_sorok and all(int(s[i_gond]) == 200 for s in c_sorok),
          'C: a napló gondolkodas_token oszlopa nem 200 minden C-hívásnál: %s' % [s[i_gond] for s in c_sorok])
    ellen(all(int(s[i_gond]) == 0 for s in naplo[1:] if s[i_modell] != MODELLEK['C']), 'A/B: nem nulla gondolkodási token')
    ellen(gondolkodas_token({'completion_tokens_details': {'reasoning_tokens': 7}}) == 7
          and gondolkodas_token({'output_tokens_details': {'reasoning_tokens': 9}}) == 9
          and gondolkodas_token({'reasoning_tokens': 3}) == 3 and gondolkodas_token({}) == 0
          and gondolkodas_token({'completion_tokens_details': None}) == 0,
          'gondolkodas_token: az usage-alakok értelmezése hibás')
    f3_sorok = koteg_sorok('F3', mappa)
    ellen(all(len(x['hivasok']) == len(x['nyers']) and all('usage' in h_ for h_ in x['hivasok']) for x in f3_sorok),
          'a jsonl nem tárolja hívásonként a nyers usage-ot')
    ellen(sum(gondolkodas_token(h_['usage']) for x in f3_sorok for h_ in x['hivasok'])
          == sum(int(s[i_gond]) for s in c_sorok if s[NAPLO_FEJLEC.index('futas')] == 'F3'),
          'a jsonl usage-ából visszaszámolt gondolkodási token nem egyezik a naplóéval')
    # kulcs nem szivárog
    szivarog = []
    for gyoker, _, fajlok in os.walk(mappa):
        for fn in fajlok:
            with open(os.path.join(gyoker, fn), encoding='utf-8') as f:
                if teszt_kulcs in f.read():
                    szivarog.append(fn)
    ellen(not szivarog, 'a kulcs megjelent a kimenetben: %s' % szivarog)
    ellen(set(mock.kulcsok) == {teszt_kulcs}, 'a küldő nem a megadott kulcsot kapta')

    # --- 2. újraindítás: kész köteg nem hív újra --------------------------
    hivasok_elotte = len(mock.hivasok)
    kod = futasok_vegrehajt(ctx, ossz_futas, minta)
    ellen(kod == 0 and len(mock.hivasok) == hivasok_elotte,
          'újraindításkor új hívás történt (%d)' % (len(mock.hivasok) - hivasok_elotte))

    # --- 3. plafon-leállás és folytatás ------------------------------------
    mappa2 = tempfile.mkdtemp(prefix='f21p_onteszt_plafon_')
    mock2 = MockKuldo(koltseg_szorzo=1.0)
    ctx2 = Kontextus(mock2, teszt_kulcs, mappa2, plafon=0.004)
    kod = futasok_vegrehajt(ctx2, ossz_futas, minta)
    ellen(kod == KILEPES_PLAFON, 'plafon: a kilépési kód %d, várt %d' % (kod, KILEPES_PLAFON))
    ossz = naplo_osszeg(mappa2)
    ellen(0 < ossz <= 0.004, 'plafon: a napló összege %.6f a plafonon (0.004) kívül' % ossz)
    kesz_elotte = sum(len(eredmenyek_betolt(f, mappa2)) for f in ossz_futas)
    ellen(kesz_elotte > 0, 'plafon: nincs mentett kész sor a leállás előtt')
    hivasok_elotte = len(mock2.hivasok)
    ctx2.plafon = PLAFON_USD
    kod = futasok_vegrehajt(ctx2, ossz_futas, minta)
    ellen(kod == 0, 'plafon utáni folytatás kilépési kódja %d' % kod)
    ellen(len(eredmenyek_betolt('F1', mappa2)) == 25, 'folytatás után az F1 nem teljes')
    # a folytatás nem ismétli a kész kötegeket: a hívott versek között nincs F1-köteg, amit már mentettünk
    # (a hívás-szám = a hiányzó kötegek; ellenőrzés: az F1 kötegei pontosan egyszer szerepelnek a jsonl-ben)
    f1_sorok = koteg_sorok('F1', mappa2)
    ellen(len({tuple(s['igehelyek']) for s in f1_sorok}) == len(f1_sorok), 'folytatás: duplikált köteg az F1-ben')

    # --- 4. előfeltétel: F4 az F1/F2 előtt ---------------------------------
    mappa3 = tempfile.mkdtemp(prefix='f21p_onteszt_elofeltetel_')
    ctx3 = Kontextus(MockKuldo(), teszt_kulcs, mappa3)
    kod = futasok_vegrehajt(ctx3, ['F4'], minta)
    ellen(kod == 2, 'F4 előfeltétel nélkül a kilépési kód %d, várt 2' % kod)

    naplo_osszeg_onteszt = naplo_osszeg(mappa)
    # --- 5. vezérlőfájl és koteg_max -------------------------------------------
    mappa4 = tempfile.mkdtemp(prefix='f21p_onteszt_vezerlo_')
    vez = os.path.join(mappa4, 'futtatas.txt')

    def vez_ir(tartalom):
        with open(vez, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tartalom)

    def vez_hiba(tartalom):
        vez_ir(tartalom)
        try:
            vezerlo_beolvas(vez)
        except VezerloHiba:
            return True
        return False

    vez_ir('# megjegyzés\nfutasok = F5, F1 ,F3\nkoteg_max=mind\n')
    v = vezerlo_beolvas(vez)
    ellen(v == {'futasok': ['F1', 'F3', 'F5'], 'koteg_max': None, 'plafon_usd': None}, 'vezérlő: hibás értelmezés: %s' % v)
    vez_ir('futasok=F1\nkoteg_max=1\n')
    ellen(vezerlo_beolvas(vez) == {'futasok': ['F1'], 'koteg_max': 1, 'plafon_usd': None}, 'vezérlő: a koteg_max=1 értelmezése hibás')
    vez_ir('futasok=F4\nkoteg_max=mind\n')
    ellen(vezerlo_beolvas(vez)['futasok'] == ['F4'], 'vezérlő: az egyedül álló F4 elutasítva')
    ellen(vez_hiba(''), 'vezérlő: üres fájl elfogadva (nincs alapérték)')
    ellen(vez_hiba('futasok=F1\n'), 'vezérlő: hiányzó koteg_max elfogadva')
    ellen(vez_hiba('koteg_max=1\n'), 'vezérlő: hiányzó futasok elfogadva')
    ellen(vez_hiba('futasok=F1\nkoteg_max=1\nmodell=A\n'), 'vezérlő: ismeretlen kulcs elfogadva')
    ellen(vez_hiba('futasok=F1\nfutasok=F2\nkoteg_max=1\n'), 'vezérlő: ismételt kulcs elfogadva')
    ellen(vez_hiba('futasok=F7\nkoteg_max=1\n'), 'vezérlő: ismeretlen futás elfogadva')
    ellen(vez_hiba('futasok=F1,F1\nkoteg_max=1\n'), 'vezérlő: ismételt futás elfogadva')
    ellen(vez_hiba('futasok=F1,F4\nkoteg_max=1\n'), 'vezérlő: az F4 más futással együtt elfogadva')
    ellen(vez_hiba('futasok=F1\nkoteg_max=0\n'), 'vezérlő: koteg_max=0 elfogadva')
    ellen(vez_hiba('futasok=F1\nkoteg_max=sok\n'), 'vezérlő: koteg_max=sok elfogadva')
    ellen(vez_hiba('F1\n'), 'vezérlő: nem kulcs=érték sor elfogadva')
    ellen(not os.path.exists(os.path.join(mappa4, 'nincs.txt')) and
          _hibas(lambda: vezerlo_beolvas(os.path.join(mappa4, 'nincs.txt'))), 'vezérlő: a hiányzó fájl nem hiba')
    # vezérlővel vezérelt futás: az első trigger egyetlen köteg (F1, 10 vers)
    mappa5 = tempfile.mkdtemp(prefix='f21p_onteszt_koteg_')
    mock5 = MockKuldo()
    ctx5 = Kontextus(mock5, teszt_kulcs, mappa5)
    vez_ir('futasok=F1\nkoteg_max=1\n')
    kod = vezerlo_futtat(ctx5, vez, minta)
    ellen(kod == 0 and len(mock5.hivasok) == 1 and len(eredmenyek_betolt('F1', mappa5)) == 10,
          'koteg_max=1: nem pontosan egy köteg (10 vers) futott: hívások %d, versek %d'
          % (len(mock5.hivasok), len(eredmenyek_betolt('F1', mappa5))))
    ellen(eredmenyek_betolt('F2', mappa5) == {} and eredmenyek_betolt('F3', mappa5) == {},
          'koteg_max=1: más futás is indult')
    vez_ir('futasok=F1,F2\nkoteg_max=mind\n')
    kod = vezerlo_futtat(ctx5, vez, minta)
    ellen(kod == 0 and len(eredmenyek_betolt('F1', mappa5)) == 25 and len(eredmenyek_betolt('F2', mappa5)) == 25,
          'mind: az F1/F2 nem teljes')
    ellen(len(mock5.hivasok) == 1 + 2 + 3, 'mind: a kész köteg újra hívott (hívások: %d, várt 6)' % len(mock5.hivasok))
    # hibás vezérlés: semmit nem hív
    db = len(mock5.hivasok)
    vez_ir('futasok=F3\n')
    ellen(vezerlo_futtat(ctx5, vez, minta) == 2 and len(mock5.hivasok) == db,
          'hibás vezérlő: nem 2-es kilépési kód, vagy hívás történt')

    p3b_kimenet = []
    p3b_mappak = onteszt_p3b(ellen, minta, teszt_kulcs, p3b_kimenet)
    for m in [mappa, mappa2, mappa3, mappa4, mappa5] + p3b_mappak:
        shutil.rmtree(m, ignore_errors=True)
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    hivas_db = len(naplo) - 1
    print('önteszt rendben: %d mock-hívás az 1. menetben (naplósor: %d, napló-összeg %.6f USD), '
          'F4 versei: %d/25, plafon-leállás összege %.6f USD (plafon 0.004), kész sorok a leállás előtt: %d'
          % (len(mock.hivasok), hivas_db, naplo_osszeg_onteszt, len(v4), ossz, kesz_elotte))
    print('P3b önteszt (F1V2, F2V2, F5V2, F6V2, F3V2B, F4V2) rendben; bizonyító kimenet:')
    for x in p3b_kimenet:
        print('  - ' + x)
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--vezerlo', default=None, help='vezérlőfájl (f21p/futtatas.txt): futasok=..., koteg_max=...')
    ap.add_argument('--futas', default=None, help='pl. F1,F2 (nincs alapérték; --vezerlo helyett, kézi futtatáshoz)')
    ap.add_argument('--koteg-max', default=None, help='--futas mellett: futásonként legfeljebb ennyi új köteg (pozitív egész vagy mind)')
    ap.add_argument('--mentett-ellenoriz', default=None, help='pl. F1V2,F4V2: a mentett válaszok újraellenőrzése (kapu + 6. pont), hálózat nélkül')
    ap.add_argument('--szaraz', action='store_true', help='token- és költségbecslés, hálózat nélkül')
    ap.add_argument('--onteszt', action='store_true', help='MOCK küldős önellenőrzés, hálózat és kulcs nélkül')
    ap.add_argument('--eltero-arany', type=float, default=0.30, help='--szaraz: az F4 versei az F1–F2 eltérési aránya szerint')
    ap.add_argument('--plafon', type=float, default=PLAFON_USD, help='kumulatív költségplafon USD (alap: 3.0)')
    ap.add_argument('--kimenet-dir', default=F21P, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    args = ap.parse_args()

    if args.onteszt:
        return onteszt()
    if args.mentett_ellenoriz:
        ossz_hiba = 0
        for f in (x.strip() for x in args.mentett_ellenoriz.split(',') if x.strip()):
            if f not in FUTASOK:
                print('ismeretlen futás: %s' % f, file=sys.stderr)
                return 2
            h = mentett_valaszok_ellenoriz(f, args.kimenet_dir)
            print('%s: %d mentett vers ellenőrizve, hiba: %d' % (
                f, sum(1 for v in eredmenyek_betolt(f, args.kimenet_dir).values() if v['allapot'] == 'ok'), len(h)))
            for x in h[:20]:
                print('  ' + x)
            ossz_hiba += len(h)
        return 1 if ossz_hiba else 0
    minta = minta_betolt()
    if args.szaraz:
        szaraz_kiir(minta, args.eltero_arany)
        p3b_kiir(minta)
        return 0

    if bool(args.vezerlo) == bool(args.futas):
        print('HIBA: pontosan az egyik kell: --vezerlo <fájl> vagy --futas <lista> --koteg-max <n|mind> '
              '(nincs alapértelmezett futás)', file=sys.stderr)
        return 2
    idk = None
    koteg_max = None
    if args.futas:
        if args.koteg_max is None:
            print('HIBA: a --futas mellé --koteg-max is kell (pozitív egész vagy mind)', file=sys.stderr)
            return 2
        idk = [x.strip() for x in args.futas.split(',') if x.strip()]
        for f in idk:
            if f not in FUTASOK:
                print('ismeretlen futás: %s' % f, file=sys.stderr)
                return 2
        if args.koteg_max != 'mind':
            if not args.koteg_max.isdigit() or int(args.koteg_max) < 1:
                print('HIBA: a --koteg-max pozitív egész vagy mind', file=sys.stderr)
                return 2
            koteg_max = int(args.koteg_max)
    else:
        try:
            vezerlo_beolvas(args.vezerlo)   # kulcs nélkül is hibára fusson, mielőtt bármi indul
        except VezerloHiba as e:
            print('VEZÉRLŐFÁJL HIBA (%s): %s' % (args.vezerlo, e), file=sys.stderr)
            return 2
    if not (0 < args.plafon <= PLAFON_USD):
        print('HIBA: a --plafon 0 és %.1f (kemény korlát) között kell legyen' % PLAFON_USD, file=sys.stderr)
        return 2
    fagy = befagyasztas_ellenoriz()
    if fagy:
        for x in fagy:
            print('BEFAGYASZTÁS HIBA: %s' % x, file=sys.stderr)
        return 2
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print('HIBA: az OPENROUTER_API_KEY környezeti változó nincs beállítva', file=sys.stderr)
        return 2
    ctx = Kontextus(fordit._valodi_http_kuldo, api_key, args.kimenet_dir, plafon=args.plafon)
    if args.vezerlo:
        kod = vezerlo_futtat(ctx, args.vezerlo, minta)
    else:
        kod = futasok_vegrehajt(ctx, idk, minta, koteg_max)
    print('kész; kilépési kód: %d; a napló összege: %.4f USD (plafon %.2f)'
          % (kod, naplo_osszeg(args.kimenet_dir), args.plafon), flush=True)
    return kod


if __name__ == '__main__':
    sys.exit(main())
