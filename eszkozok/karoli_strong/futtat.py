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

Modellek: A google/gemini-3.1-flash-lite, B deepseek/deepseek-v4-flash,
C google/gemini-3.8-flash. 10 vers / hívás; versenként az ötpontos kapu
(kapu.py), hibánál egy újrakérés; a mintából a f21p/minta.tsv sorrendjében.

Kimenet (alapból a f21p/ alatt):
  valaszok/<futas>.jsonl  köteg-soronként: nyers válaszok + versenkénti állapot
  futasnaplo.tsv          hívásonként: tokenek, cost, modell, futás, köteg,
                          kapuhiba, próbálkozás, időbélyeg, gondolkodási mód

Költségplafon: 3 USD kumulatívan a futasnaplo.tsv koltseg_usd oszlopa alapján,
MINDEN hívás előtt ellenőrizve (a napló összege + a hívás becsült költsége);
túllépésnél leállás, kilépési kód 3, a kész kötegek mentve maradnak. A futás
újraindítható: a kész köteg (a jsonl-ben már szereplő verscsoport) nem hív újra.

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

Nincs alapértelmezett futás: --szaraz, --onteszt, --vezerlo vagy --futas (és ez
utóbbival --koteg-max) nélkül a szkript hibával (kilépési kód 2) áll meg.

VEZÉRLŐFÁJL (f21p/futtatas.txt; a workflow ezt olvassa): egyszerű kulcs=érték sorok,
a # kezdetű sor és az üres sor megjegyzés. KÖTELEZŐ kulcs mindkettő, alapérték
nincs; ismeretlen, hiányzó vagy ismételt kulcs, hibás érték, hiányzó fájl esetén a
futtatás 2-es kilépési kóddal áll meg, és semmit nem hív meg.
    futasok=F1            # vesszővel elválasztva az F1..F6, F3V2 közül, pl. F1,F2,F3,F5,F6;
                          # az F4 csak egyedül (külön trigger: az F1 és F2 kész kell)
    koteg_max=1           # futásonként legfeljebb ennyi ÚJ köteg (10 vers/köteg) fut;
                          # pozitív egész, vagy 'mind' (a kész kötegek kimaradnak)
Példák: az első trigger: futasok=F1, koteg_max=1 (10 vers); a második:
futasok=F1,F2,F3,F5,F6, koteg_max=mind; a harmadik: futasok=F4, koteg_max=mind.
A futások mindig az F1..F6 sorrendben futnak, akárhogy van felsorolva a fájlban.

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


def biro_utasitas():
    """A főprompt utasításrésze + a döntőbírói kiegészítés (prompt_biro_v1.md)."""
    with open(BIRO_PROMPT_UT, encoding='utf-8') as f:
        s = f.read()
    a = s.index(bemenet.KEZDET) + len(bemenet.KEZDET)
    b = s.index(bemenet.VEGE)
    return bemenet.prompt_utasitas() + '\n\n' + s[a:b].strip('\n')


def biro_sha256():
    import hashlib
    return hashlib.sha256(biro_utasitas().encode('utf-8')).hexdigest()


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


def biro_kotegszoveg(igehelyek, a_eredmenyek, b_eredmenyek, kjv=True):
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
        biro_utasitas(), len(igehelyek), '\n\n'.join(blokkok))


def kotegszoveg_futashoz(futas_id, igehelyek, kimenet_dir):
    spec = FUTASOK[futas_id]
    if spec['tipus'] == 'biro':
        a = eredmenyek_betolt(spec['forras'][0], kimenet_dir)
        b = eredmenyek_betolt(spec['forras'][1], kimenet_dir)
        return biro_kotegszoveg(igehelyek, a, b, spec['kjv'])
    return bemenet.kotegszoveg(igehelyek, spec['kjv'], spec.get('prompt'))


def utasitas_sha12(futas_id):
    import hashlib
    if FUTASOK[futas_id]['tipus'] == 'biro':
        return biro_sha256()[:12]
    return hashlib.sha256(bemenet.prompt_utasitas(FUTASOK[futas_id].get('prompt')).encode('utf-8')).hexdigest()[:12]


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
    koteg_ment(futas_id, ctx.kimenet_dir, sor)
    return versek


def futas(ctx, futas_id, minta, koteg_max=None):
    """Egy futás kötegei; visszaad: (kilépési_kód, összegzés_dict).

    koteg_max: legfeljebb ennyi ÚJ köteg fut (a kész kötegek nem számítanak);
    None = az összes."""
    versek = verslista(futas_id, minta, ctx.kimenet_dir)
    kotegek = bemenet.kotegek(versek, KOTEG_MERET)
    kesz = kesz_kotegek(futas_id, ctx.kimenet_dir)
    print('%s: %s, %d vers, %d köteg (kész: %d)' % (
        futas_id, MODELLEK[FUTASOK[futas_id]['modell']], len(versek), len(kotegek),
        sum(1 for k in kotegek if tuple(k) in kesz)), flush=True)
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
    return (1 if hibas_kotegek else 0), {'versek': len(versek), 'kotegek': len(kotegek),
                                          'hibas_kotegek': hibas_kotegek}


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

VEZERLO_KULCSOK = ('futasok', 'koteg_max')


class VezerloHiba(Exception):
    pass


def vezerlo_beolvas(ut):
    """A vezérlőfájl értelmezése: {'futasok': [F-id, ...] (F1..F6 sorrendben),
    'koteg_max': int|None}. Hiba esetén VezerloHiba (nincs alapérték)."""
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
        if kulcs not in VEZERLO_KULCSOK:
            raise VezerloHiba('%d. sor: ismeretlen kulcs: %r (érvényes: %s)'
                              % (i, kulcs, ', '.join(VEZERLO_KULCSOK)))
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
    return {'futasok': [f for f in FUTASOK if f in idk], 'koteg_max': koteg_max}


def vezerlo_futtat(ctx, vezerlo_ut, minta):
    """A vezérlőfájl szerinti futtatás; hibás vezérlésnél 2, hívás nélkül."""
    try:
        v = vezerlo_beolvas(vezerlo_ut)
    except VezerloHiba as e:
        print('VEZÉRLŐFÁJL HIBA (%s): %s' % (vezerlo_ut, e), file=sys.stderr)
        return 2
    print('vezérlés: futások=%s, koteg_max=%s' % (','.join(v['futasok']), v['koteg_max'] or 'mind'), flush=True)
    return futasok_vegrehajt(ctx, v['futasok'], minta, v['koteg_max'])


# ---------------------------------------------------------------------------
# --szaraz: becslés hálózat nélkül
# ---------------------------------------------------------------------------

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
        be = ki = 0
        kotegek = bemenet.kotegek(versek, KOTEG_MERET)
        for k in kotegek:
            szoveg_hossz = len(bemenet.kotegszoveg(k, spec['kjv'], spec.get('prompt')))
            if spec['tipus'] == 'biro':
                # a döntőbírói utasítás hosszabb, és versenként két válasz is jön
                # (A és B, 150-150 token); a válasz-JSON karakterhossza ~ tokenszám * KAR_PER_TOKEN
                szoveg_hossz += len(biro_utasitas()) - len(bemenet.prompt_utasitas())
                szoveg_hossz += int(2 * KIMENET_TOKEN_VERSENKENT * KAR_PER_TOKEN * len(k))
            be += szoveg_hossz / KAR_PER_TOKEN
            ki += KIMENET_TOKEN_VERSENKENT * len(k)
            if spec['modell'] == 'C':
                ki += gondolkodas_c
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
                 koltseg_szorzo=1.0, biro_rossz_elso=(), biro_rossz_mindig=()):
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
            if ig in self.hibas_mindig or (ig in self.hibas_elso and not masodik):
                obj = self._helyes(ig, False)
                obj['megjegyzes'] = 'H1234'   # Strong-minta: az 5. kapupont fogja
            else:
                variacio = (modell_id == MODELLEK['B'] and (hash_stabil(ig) % 4 == 0))
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
    ellen(v == {'futasok': ['F1', 'F3', 'F5'], 'koteg_max': None}, 'vezérlő: hibás értelmezés: %s' % v)
    vez_ir('futasok=F1\nkoteg_max=1\n')
    ellen(vezerlo_beolvas(vez) == {'futasok': ['F1'], 'koteg_max': 1}, 'vezérlő: a koteg_max=1 értelmezése hibás')
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

    for m in (mappa, mappa2, mappa3, mappa4, mappa5):
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
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--vezerlo', default=None, help='vezérlőfájl (f21p/futtatas.txt): futasok=..., koteg_max=...')
    ap.add_argument('--futas', default=None, help='pl. F1,F2 (nincs alapérték; --vezerlo helyett, kézi futtatáshoz)')
    ap.add_argument('--koteg-max', default=None, help='--futas mellett: futásonként legfeljebb ennyi új köteg (pozitív egész vagy mind)')
    ap.add_argument('--szaraz', action='store_true', help='token- és költségbecslés, hálózat nélkül')
    ap.add_argument('--onteszt', action='store_true', help='MOCK küldős önellenőrzés, hálózat és kulcs nélkül')
    ap.add_argument('--eltero-arany', type=float, default=0.30, help='--szaraz: az F4 versei az F1–F2 eltérési aránya szerint')
    ap.add_argument('--plafon', type=float, default=PLAFON_USD, help='kumulatív költségplafon USD (alap: 3.0)')
    ap.add_argument('--kimenet-dir', default=F21P, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    args = ap.parse_args()

    if args.onteszt:
        return onteszt()
    minta = minta_betolt()
    if args.szaraz:
        szaraz_kiir(minta, args.eltero_arany)
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
