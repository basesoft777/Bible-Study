#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fordit.py -- FORDITAS_PILOT_BRIEF.md v1, FP2-FP3: Thayer-szocikkek forditasa
harom OpenRouter-modellel (G3), a naplok/FORDITAS_P1_minta.tsv 20 szocikkere.
Az OpenRouter-hivas es a koltsegnaplo mintaja: eszkozok/cremer_ocr_javit.py
(0.7. mert).

CLI:
    python eszkozok/fordit.py --szaraz
    python eszkozok/fordit.py
    python eszkozok/fordit.py --modellek m1,m3 --strongok G0012,G1941
    python eszkozok/fordit.py --onteszt

Kimenet (naplok/ ala, --kimenet-dir modosithatja):
  FORDITAS_P3_kimenet.tsv       -- a G1 semaja (szotar, strong, entry_id,
                                    jelentes_szam, mezo, forras_hash,
                                    forditas_hu, allapot, modell, datum,
                                    terminologia_verzio) -- valtozatlanul
                                    atveheto a SZOTAR 4e altal.
  FORDITAS_P3_bizonytalan.tsv   -- strong, modell, darab, bizonytalan_feloldasok
  FORDITAS_P_koltseg.tsv        -- usage-alapu koltsegnaplo, G7 plafonnal

--szaraz: halozati hivas nelkul; csak becsult token- es koltsegigeny
  (naplok/FORDITAS_P3_szaraz_becsles.tsv es osszesito stdoutra). A becsles
  durva (karakter/token aranybol), csak nagysagrend-ellenorzesre.

Az OPENROUTER_API_KEY kulcsot csak kornyezeti valtozobol olvassa; erteke sehova
nem kerul (sem stdoutra, sem naplofajlba, sem a gyorsitotarba).

A gyorsitotar es a hibanaplo a naplok/FORDITAS_P_cache/ es naplok/FORDITAS_P_hibak/
ala kerul -- ezek NEM verziozott munkakonyvtarak (a G1 csak a *kimeneti* TSV-ket
es a prompt/terminologia fajlokat sorolja a pilot irhato koreбe; a nyers
gyorsitotar sosem kerul git add ala, l. FORDITAS_P4_ellenorzes.md K1).

Kilepesi kod: 0 = rendben, 1 = hianyzo kulcs vagy bemenet, 3 = a G7
koltsegplafon miatt korai leallas (a mar kesz sorok mentve).
"""

import argparse
import hashlib
import os
import re
import sys
import time
from datetime import date, datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLOK = os.path.join(REPO, 'naplok')

MINTA_UT = os.path.join(NAPLOK, 'FORDITAS_P1_minta.tsv')
TERMINOLOGIA_UT = os.path.join(NAPLOK, 'FORDITAS_P_terminologia.tsv')
PROMPT_UT = os.path.join(NAPLOK, 'FORDITAS_P_prompt_v1.md')
MODELLEK_UT = os.path.join(NAPLOK, 'FORDITAS_P0_modellek.json')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

CACHE_DIR = os.path.join(NAPLOK, 'FORDITAS_P_cache')
HIBA_DIR = os.path.join(NAPLOK, 'FORDITAS_P_hibak')

KIMENET_UT = os.path.join(NAPLOK, 'FORDITAS_P3_kimenet.tsv')
BIZONYTALAN_UT = os.path.join(NAPLOK, 'FORDITAS_P3_bizonytalan.tsv')
KOLTSEG_UT = os.path.join(NAPLOK, 'FORDITAS_P_koltseg.tsv')
SZARAZ_UT = os.path.join(NAPLOK, 'FORDITAS_P3_szaraz_becsles.tsv')

PROMPT_VERZIO = 'v1'
TERMINOLOGIA_VERZIO = 'v1'
DARAB_HATAR = 4000  # G6

MODELL_JELEK = {
    'm1': 'deepseek/deepseek-v4-flash',
    'm2': 'google/gemini-3.8-flash',
    'm3': 'anthropic/claude-haiku-4.5',
}

KIMENET_FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo',
                   'forras_hash', 'forditas_hu', 'allapot', 'modell', 'datum',
                   'terminologia_verzio']
BIZONYTALAN_FEJLEC = ['strong', 'modell', 'darab', 'bizonytalan_feloldasok']
KOLTSEG_FEJLEC = ['strong', 'csoport', 'modell', 'darab', 'forras',
                   'bemenet_token', 'kimenet_token', 'koltseg_usd',
                   'koltseg_forras', 'futo_osszeg_usd']
SZARAZ_FEJLEC = ['strong', 'csoport', 'modell', 'darabok', 'becsult_bemenet_token',
                  'becsult_kimenet_token', 'becsult_koltseg_usd']


# ---------------------------------------------------------------------------
# TSV I/O (CLAUDE.md: split/join, nem csv modul)
# ---------------------------------------------------------------------------

def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


def tsv_ir(ut, fejlec, sorok):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(fejlec) + '\n')
        for sor in sorok:
            fh.write('\t'.join(str(sor.get(mezo, '')) for mezo in fejlec) + '\n')


# ---------------------------------------------------------------------------
# Bemenetek betoltese
# ---------------------------------------------------------------------------

def minta_betolt(ut=MINTA_UT):
    return list(tsv_dict_sorok(ut))


def terminologia_betolt(ut=TERMINOLOGIA_UT):
    return list(tsv_dict_sorok(ut))


def karoli_tabla_betolt(ut=KAROLI_UT):
    return list(tsv_dict_sorok(ut))


def thayer_betolt(ut=THAYER_UT):
    ki = {}
    for r in tsv_dict_sorok(ut):
        ki[r['Strong_padded']] = r
    return ki


def modell_arak_betolt(ut=MODELLEK_UT):
    with open(ut, encoding='utf-8') as fh:
        adat = json.load(fh)
    return {m['id']: m for m in adat}


def modellek_felold(jelek_str, arak):
    jelek = [j.strip() for j in jelek_str.split(',') if j.strip()]
    eredmeny = []
    for jel in jelek:
        model_id = MODELL_JELEK.get(jel)
        if model_id is None:
            raise SystemExit('ismeretlen modelljel: %s (ismertek: %s)' % (jel, ', '.join(MODELL_JELEK)))
        ar = arak.get(model_id, {})
        eredmeny.append((jel, model_id,
                          ar.get('prompt_usd_per_1M'), ar.get('completion_usd_per_1M')))
    return eredmeny


def terminologia_szoveg(sorok):
    sorok_szoveg = []
    for r in sorok:
        if r['megjegyzes']:
            sorok_szoveg.append('- `%s` = %s (%s)' % (r['angol'], r['magyar'], r['megjegyzes']))
        else:
            sorok_szoveg.append('- `%s` = %s' % (r['angol'], r['magyar']))
    return '\n'.join(sorok_szoveg)


def karoli_tabla_szoveg(sorok):
    return '\n'.join('- `%s` → `%s`' % (r['STEPBible-rövidítés'], r['Magyar rövidítés']) for r in sorok)


# ---------------------------------------------------------------------------
# Daraboles (G6): a forras sajat 1., 2., a., b. jelentes-szamozasanal, ha a
# szocikk hosszabb a DARAB_HATARnal
# ---------------------------------------------------------------------------

NUM_MINTA = re.compile(r'(?<=\s)(\d{1,2})\.(?=\s)')
BETU_MINTA = re.compile(r'(?<=\s)([a-h])\.(?=\s)')
ROMAI_ELOTAG_MINTA = re.compile(r'\b[IVXLC]{1,4}\.\s*$')


def _romai_szamos_elotag_e(szoveg, poz):
    """Kiszuri az olyan alszakasz-jelzest, amely egy MASIK szocikk sajat
    (romai szammal bevezetett) belso tagolasara hivatkozik idezetkent
    (pl. 'lasd baptizo, II. b.') -- ez nem az EPPEN forditott szocikk sajat
    tagolasa, tehat nem daraboljuk ra."""
    return bool(ROMAI_ELOTAG_MINTA.search(szoveg[max(0, poz - 8):poz]))


def _monoton_hatarok(szoveg, minta, elso_ertek, kovetkezo_fn, guard=None):
    hatarok = []
    vart = elso_ertek
    for m in minta.finditer(szoveg):
        if m.group(1) != vart:
            continue
        if guard is not None and guard(szoveg, m.start()):
            continue
        hatarok.append(m.start())  # a szam/betu elejen (a lookbehind a vezeto szokozt nem fogyasztja el)
        vart = kovetkezo_fn(vart)
    return hatarok


def _darabol_hatarnal(szoveg, hatarok):
    pontok = sorted(set([0] + hatarok + [len(szoveg)]))
    return [szoveg[pontok[i]:pontok[i + 1]] for i in range(len(pontok) - 1)
            if szoveg[pontok[i]:pontok[i + 1]].strip()]


def _kemenyen_tordel(szoveg, limit):
    """Utolso mentsvar, ha a szam-/betujeloles nem eleg: mondathataron
    ('. ') tordel limit korul. A G6 nem ir elo ilyen esetet -- a mintaban
    (FP1) egyetlen szocikk sem futott bele --, de a hatart mindenkeppen be
    kell tartani, ha egy jovobeli szocikk sajat tagolas nelkuli, hosszu
    proza lenne."""
    if len(szoveg) <= limit:
        return [szoveg]
    darabok = []
    while len(szoveg) > limit:
        vagas = szoveg.rfind('. ', 0, limit)
        if vagas == -1 or vagas < limit // 2:
            vagas = limit
        else:
            vagas += 2
        darabok.append(szoveg[:vagas])
        szoveg = szoveg[vagas:]
    if szoveg.strip():
        darabok.append(szoveg)
    return darabok


def darabokra_bont(szoveg, limit=DARAB_HATAR):
    if len(szoveg) <= limit:
        return [szoveg]
    szam_hatarok = _monoton_hatarok(szoveg, NUM_MINTA, '1', lambda e: str(int(e) + 1))
    eredmeny = []
    for darab in _darabol_hatarnal(szoveg, szam_hatarok):
        if len(darab) <= limit:
            eredmeny.append(darab)
            continue
        betu_hatarok = _monoton_hatarok(darab, BETU_MINTA, 'a', lambda e: chr(ord(e) + 1),
                                         guard=_romai_szamos_elotag_e)
        for al_darab in _darabol_hatarnal(darab, betu_hatarok):
            if len(al_darab) <= limit:
                eredmeny.append(al_darab)
            else:
                eredmeny.extend(_kemenyen_tordel(al_darab, limit))
    return eredmeny


# ---------------------------------------------------------------------------
# Prompt-epites
# ---------------------------------------------------------------------------

def prompt_epit(sablon, strong, forras_darab, darab_info, terminologia_sz, karoli_sz):
    return (sablon
            .replace('{{TERMINOLOGIA}}', terminologia_sz)
            .replace('{{KAROLI_TABLA}}', karoli_sz)
            .replace('{{STRONG}}', strong)
            .replace('{{DARAB_MEGJEGYZES}}', darab_info)
            .replace('{{FORRAS_SZOVEG}}', forras_darab))


def darab_info_szoveg(i, n):
    if n == 1:
        return ''
    return (' (%d/%d. rész -- csak ezt a részt fordítsd önmagában álló szövegként; '
            'a folytatás külön hívásban érkezik, NE told ki a hiányzó résszel, és '
            'ne jelezd a szöveg részlegességét)') % (i + 1, n)


# ---------------------------------------------------------------------------
# OpenRouter-hivas (a minta: eszkozok/cremer_ocr_javit.py C1-C3, D12, H5)
# ---------------------------------------------------------------------------

class OpenRouterHiba(Exception):
    def __init__(self, uzenet, usage=None):
        super().__init__(uzenet)
        self.usage = usage or {}


def _valodi_http_kuldo(model_id, uzenetek, api_key, extra_parameterek):
    import requests
    return requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'},
        json=dict(model=model_id, messages=uzenetek, temperature=0,
                   usage={'include': True}, **extra_parameterek),
        timeout=60,
    )


def _http_post_nyers(model_id, uzenetek, api_key, extra_parameterek,
                      ujraprobalkozas_http=4, kezdeti_varakozas=2, kuldo=None, alvas=None):
    """Visszalepeses ujraprobalkozas (2, 4, 8, 16 mp) HTTP 429/5xx/halozati
    hiba eseten; 4xx-nel azonnali OpenRouterHiba (ujraprobalkozas nem
    segitene)."""
    kuldo = kuldo or _valodi_http_kuldo
    alvas = alvas or time.sleep
    import requests

    varakozas = kezdeti_varakozas
    utolso_hiba = None
    for kiserlet in range(ujraprobalkozas_http + 1):
        try:
            valasz = kuldo(model_id, uzenetek, api_key, extra_parameterek)
        except requests.exceptions.RequestException as e:
            utolso_hiba = e
            if kiserlet < ujraprobalkozas_http:
                alvas(varakozas)
                varakozas *= 2
                continue
            raise OpenRouterHiba('halozati hiba %d kiserlet utan: %s' % (kiserlet + 1, e))
        if valasz.status_code == 429 or valasz.status_code >= 500:
            utolso_hiba = 'HTTP %d' % valasz.status_code
            if kiserlet < ujraprobalkozas_http:
                alvas(varakozas)
                varakozas *= 2
                continue
            raise OpenRouterHiba('HTTP hiba %d kiserlet utan: %s' % (kiserlet + 1, utolso_hiba))
        if valasz.status_code >= 400:
            szoveg = ''
            try:
                szoveg = valasz.text[:300]
            except Exception:
                pass
            raise OpenRouterHiba('HTTP kliens-hiba %d: %s' % (valasz.status_code, szoveg))
        return valasz.json(), kiserlet + 1
    raise OpenRouterHiba('nem sikerult a hivas: %s' % utolso_hiba)


def _json_sema():
    return {
        'type': 'json_schema',
        'json_schema': {
            'name': 'fordit_kimenet',
            'strict': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'strong': {'type': 'string'},
                    'forditas_hu': {'type': 'string'},
                    'bizonytalan_feloldasok': {'type': 'array', 'items': {'type': 'string'}},
                },
                'required': ['strong', 'forditas_hu', 'bizonytalan_feloldasok'],
                'additionalProperties': False,
            },
        },
    }


def _kimenet_validal(nyers):
    if not isinstance(nyers, dict):
        raise ValueError('a valasz nem JSON objektum')
    for kulcs in ('strong', 'forditas_hu', 'bizonytalan_feloldasok'):
        if kulcs not in nyers:
            raise KeyError(kulcs)
    if not isinstance(nyers['forditas_hu'], str) or not nyers['forditas_hu'].strip():
        raise ValueError('ures vagy nem szoveg forditas_hu')
    if not isinstance(nyers['bizonytalan_feloldasok'], list):
        raise ValueError('a bizonytalan_feloldasok nem lista')
    return nyers


def openrouter_hivas(model_id, prompt_szoveg, api_key, ujraprobalkozas_json=1,
                      ujraprobalkozas_http=4, posztolo=None, ar_bemenet_1m=None,
                      ar_kimenet_1m=None):
    """Egy hivas egy modellhez, egy szocikk-darabhoz. H5 mintajara: minden
    JSON-ujraprobalkozasi kiserlet usage-e osszeadodik (a semasertes miatt
    eldobott elso valasz is szamlazott hivas volt). Visszaad:
    (eredmeny_dict, osszesitett_usage, utolso_nyers_valasz), vagy dobja az
    OpenRouterHiba-t (az addig osszegyult usage-gel)."""
    posztolo = posztolo or _http_post_nyers
    uzenetek = [{'role': 'user', 'content': prompt_szoveg}]
    extra_parameterek = {'response_format': _json_sema()}

    osszes_be = osszes_ki = osszes_gondolkodas = osszes_http_kiserlet = 0
    osszes_koltseg = 0.0
    van_ismeretlen_koltseg = False
    utolso_hiba = None
    osszesitett_usage = {}

    for kiserlet in range(ujraprobalkozas_json + 1):
        nyers_valasz, http_kiserletek = posztolo(model_id, uzenetek, api_key, extra_parameterek, ujraprobalkozas_http)
        osszes_http_kiserlet += http_kiserletek
        usage = nyers_valasz.get('usage') or {}
        be = usage.get('prompt_tokens', 0) or 0
        ki = usage.get('completion_tokens', 0) or 0
        reszletek = usage.get('completion_tokens_details') or {}
        gondolkodas = reszletek.get('reasoning_tokens', 0) or 0
        koltseg = usage.get('cost')
        osszes_be += be
        osszes_ki += ki
        osszes_gondolkodas += gondolkodas
        if koltseg is not None:
            osszes_koltseg += koltseg
        else:
            van_ismeretlen_koltseg = True
            if ar_bemenet_1m is not None:
                osszes_koltseg += be / 1_000_000 * ar_bemenet_1m
            if ar_kimenet_1m is not None:
                osszes_koltseg += ki / 1_000_000 * ar_kimenet_1m
        osszesitett_usage = {
            'prompt_tokens': osszes_be, 'completion_tokens': osszes_ki,
            'completion_tokens_details': {'reasoning_tokens': osszes_gondolkodas},
            'cost': osszes_koltseg,
            'koltseg_forras': 'ar_config' if van_ismeretlen_koltseg else 'openrouter',
            'kiserletek': osszes_http_kiserlet,
        }

        finish_reason = (nyers_valasz.get('choices') or [{}])[0].get('finish_reason')
        if finish_reason in ('length', 'max_tokens'):
            utolso_hiba = 'csonkolt valasz (finish_reason=%s)' % finish_reason
            continue

        tartalom = ((nyers_valasz.get('choices') or [{}])[0].get('message') or {}).get('content')
        if not tartalom:
            utolso_hiba = 'ures valasztartalom'
            continue
        try:
            nyers_json = _kimenet_validal(json.loads(tartalom))
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            utolso_hiba = e
            continue

        return nyers_json, osszesitett_usage, nyers_valasz

    raise OpenRouterHiba('ervenytelen JSON/sema %d kiserlet utan: %s' % (ujraprobalkozas_json + 1, utolso_hiba),
                          usage=osszesitett_usage)


# ---------------------------------------------------------------------------
# Gyorsitotar (G7) -- kulcs: modell + strong + darab + forras_hash + prompt-verzio
# ---------------------------------------------------------------------------

def _modell_slug(model_id):
    return re.sub(r'[^A-Za-z0-9_-]', '_', model_id)


def cache_utvonal(model_id, strong, darab_index, cache_dir=None):
    cache_dir = cache_dir or CACHE_DIR
    return os.path.join(cache_dir, _modell_slug(model_id), '%s_%d.json' % (strong, darab_index))


def cache_olvas(model_id, strong, darab_index, forras_hash, cache_dir=None):
    p = cache_utvonal(model_id, strong, darab_index, cache_dir)
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8') as fh:
        adat = json.load(fh)
    if (adat.get('prompt_verzio') != PROMPT_VERZIO
            or adat.get('terminologia_verzio') != TERMINOLOGIA_VERZIO
            or adat.get('forras_hash') != forras_hash
            or adat.get('model') != model_id):
        return None
    return adat


def cache_ir(model_id, strong, darab_index, forras_hash, eredmeny, usage, cache_dir=None):
    p = cache_utvonal(model_id, strong, darab_index, cache_dir)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    adat = {
        'model': model_id, 'strong': strong, 'darab': darab_index,
        'forras_hash': forras_hash, 'prompt_verzio': PROMPT_VERZIO,
        'terminologia_verzio': TERMINOLOGIA_VERZIO,
        'ts': datetime.now(timezone.utc).isoformat(),
        'usage': usage, 'eredmeny': eredmeny,
    }
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(adat, fh, ensure_ascii=False, indent=1)


def hiba_naplo_ir(model_id, strong, darab_index, uzenet, hiba_dir=None):
    hiba_dir = hiba_dir or HIBA_DIR
    p = os.path.join(hiba_dir, _modell_slug(model_id), '%s_%d.json' % (strong, darab_index))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump({'model': model_id, 'strong': strong, 'darab': darab_index,
                    'ts': datetime.now(timezone.utc).isoformat(), 'hiba': str(uzenet)},
                   fh, ensure_ascii=False, indent=1)
    return p


# ---------------------------------------------------------------------------
# Koltsegnaplo (G7, usage-alapu plafon)
# ---------------------------------------------------------------------------

class KoltsegNaplo:
    def __init__(self, plafon_usd):
        self.plafon_usd = plafon_usd
        self.osszeg_usd = 0.0
        self.sorok = []

    def hozzaad(self, strong, csoport, model_id, darab_index, usage, forras):
        bemenet = usage.get('prompt_tokens', 0) or 0
        kimenet = usage.get('completion_tokens', 0) or 0
        koltseg = usage.get('cost') or 0.0
        koltseg_forras = usage.get('koltseg_forras', 'openrouter')
        self.osszeg_usd += koltseg
        sor = {
            'strong': strong, 'csoport': csoport, 'modell': model_id, 'darab': darab_index,
            'forras': forras, 'bemenet_token': bemenet, 'kimenet_token': kimenet,
            'koltseg_usd': round(koltseg, 6), 'koltseg_forras': koltseg_forras,
            'futo_osszeg_usd': round(self.osszeg_usd, 6),
        }
        self.sorok.append(sor)
        return sor

    def plafon_elerve_e(self):
        return self.plafon_usd is not None and self.osszeg_usd >= self.plafon_usd


# ---------------------------------------------------------------------------
# --szaraz: durva token-/koltsegbecsles, halozat nelkul
# ---------------------------------------------------------------------------

KAR_PER_TOKEN_BECSLES = 3.5  # durva kozelites vegyes (magyar ekezetes + gorog/heber) szovegre
KIMENET_HOSSZARANY_BECSLES = 1.2  # a §1 hosszarany-ellenorzes (0.8-1.6) kozepe fole


def becsles_futtatas(minta, modellek, thayer, sablon_hossz_becsles, csoport_kimenet=SZARAZ_UT):
    sorok = []
    ossz_koltseg = 0.0
    for sor in minta:
        strong = sor['strong']
        t = thayer.get(strong)
        if t is None:
            print('HIBA -- nincs Thayer_teljes sor: %s' % strong, file=sys.stderr)
            continue
        forras_szoveg = t['Teljes_szocikk']
        darabok = darabokra_bont(forras_szoveg)
        for jel, model_id, ar_be, ar_ki in modellek:
            be_kar_ossz = sum(len(d) + sablon_hossz_becsles for d in darabok)
            ki_kar_ossz = sum(len(d) * KIMENET_HOSSZARANY_BECSLES for d in darabok)
            be_token = be_kar_ossz / KAR_PER_TOKEN_BECSLES
            ki_token = ki_kar_ossz / KAR_PER_TOKEN_BECSLES
            koltseg = 0.0
            if ar_be is not None:
                koltseg += be_token / 1_000_000 * ar_be
            if ar_ki is not None:
                koltseg += ki_token / 1_000_000 * ar_ki
            ossz_koltseg += koltseg
            sorok.append({
                'strong': strong, 'csoport': sor['csoport'], 'modell': model_id,
                'darabok': len(darabok),
                'becsult_bemenet_token': int(be_token), 'becsult_kimenet_token': int(ki_token),
                'becsult_koltseg_usd': round(koltseg, 6),
            })
    tsv_ir(csoport_kimenet, SZARAZ_FEJLEC, sorok)
    print('=== --szaraz becsles (durva, karakter/token aranybol) ===')
    print('sorok: %d szocikk x %d modell = %d becsles-sor (soronkent a darabolassal osszegezve)'
          % (len(minta), len(modellek), len(sorok)))
    print('becsult teljes koltseg: %.4f USD' % ossz_koltseg)
    print('irva: %s' % csoport_kimenet)
    return ossz_koltseg


# ---------------------------------------------------------------------------
# Eles futas
# ---------------------------------------------------------------------------

def eles_futtatas(minta, modellek, thayer, sablon, terminologia_sz, karoli_sz,
                   api_key, plafon_usd):
    koltseg = KoltsegNaplo(plafon_usd)
    kimenet_sorok = []
    bizonytalan_sorok = []
    ma = date.today().isoformat()
    leallt = False

    for sor in minta:
        if leallt:
            break
        strong = sor['strong']
        csoport = sor['csoport']
        forras_hash = sor['forras_hash']
        t = thayer.get(strong)
        if t is None:
            print('HIBA -- nincs Thayer_teljes sor: %s -- kihagyva' % strong, file=sys.stderr)
            continue
        forras_szoveg = t['Teljes_szocikk']
        entry_id = t['Strong_eredeti']
        darabok = darabokra_bont(forras_szoveg)

        for jel, model_id, ar_be, ar_ki in modellek:
            if koltseg.plafon_elerve_e():
                print('LEALLAS -- a koltsegplafon (%.2f USD) elerve, %s/%s elott' % (plafon_usd, strong, jel))
                leallt = True
                break

            darab_forditasok = []
            bizonytalan_osszes = []
            hiba_uzenet = None
            for i, darab in enumerate(darabok):
                info = darab_info_szoveg(i, len(darabok))
                prompt = prompt_epit(sablon, strong, darab, info, terminologia_sz, karoli_sz)

                print('... %s %s darab %d/%d' % (model_id, strong, i + 1, len(darabok)), flush=True)
                talalat = cache_olvas(model_id, strong, i, forras_hash)
                if talalat is not None:
                    eredmeny = talalat['eredmeny']
                    usage = talalat['usage']
                    forras_cimke = 'cache'
                    print('    cache-talalat', flush=True)
                else:
                    try:
                        eredmeny, usage, _nyers = openrouter_hivas(
                            model_id, prompt, api_key,
                            ar_bemenet_1m=ar_be, ar_kimenet_1m=ar_ki)
                    except OpenRouterHiba as e:
                        print('HIBA -- %s %s darab %d/%d: %s' % (model_id, strong, i + 1, len(darabok), e), flush=True)
                        hiba_naplo_ir(model_id, strong, i, e)
                        koltseg.hozzaad(strong, csoport, model_id, i, e.usage, 'halozat')
                        hiba_uzenet = str(e)
                        break
                    cache_ir(model_id, strong, i, forras_hash, eredmeny, usage)
                    forras_cimke = 'halozat'
                    print('    kesz (koltseg=%.5f USD)' % (usage.get('cost') or 0.0), flush=True)

                koltseg.hozzaad(strong, csoport, model_id, i, usage, forras_cimke)
                darab_forditasok.append(eredmeny['forditas_hu'])
                bizonytalan_osszes.extend(eredmeny.get('bizonytalan_feloldasok') or [])

                if koltseg.plafon_elerve_e() and i + 1 < len(darabok):
                    print('LEALLAS -- a koltsegplafon (%.2f USD) elerve, %s/%s kozepen (darab %d/%d)'
                          % (plafon_usd, strong, jel, i + 1, len(darabok)))
                    hiba_uzenet = hiba_uzenet or 'koltsegplafon a szocikk kozepen'
                    leallt = True
                    break

            forditas_hu_vegleges = 'HIBA: %s' % hiba_uzenet if hiba_uzenet else ' '.join(darab_forditasok)
            kimenet_sorok.append({
                'szotar': 'Thayer', 'strong': strong, 'entry_id': entry_id,
                'jelentes_szam': 'teljes', 'mezo': 'forditas_hu',
                'forras_hash': forras_hash, 'forditas_hu': forditas_hu_vegleges,
                'allapot': 'pilot', 'modell': model_id, 'datum': ma,
                'terminologia_verzio': TERMINOLOGIA_VERZIO,
            })
            if bizonytalan_osszes:
                bizonytalan_sorok.append({
                    'strong': strong, 'modell': model_id, 'darab': len(darabok),
                    'bizonytalan_feloldasok': '; '.join(bizonytalan_osszes),
                })
            if leallt:
                break

    tsv_ir(KIMENET_UT, KIMENET_FEJLEC, kimenet_sorok)
    tsv_ir(BIZONYTALAN_UT, BIZONYTALAN_FEJLEC, bizonytalan_sorok)
    tsv_ir(KOLTSEG_UT, KOLTSEG_FEJLEC, koltseg.sorok)

    print('=== eles futas kesz ===')
    print('kimeneti sorok: %d -- %s' % (len(kimenet_sorok), KIMENET_UT))
    print('teljes koltseg: %.4f USD -- %s' % (koltseg.osszeg_usd, KOLTSEG_UT))
    return 3 if leallt else 0


# ---------------------------------------------------------------------------
# Onteszt (halozat es kulcs nelkul)
# ---------------------------------------------------------------------------

def _onteszt_darabolas():
    rovid = 'G1 -- rovid szocikk, nincs szukseg darabolasra.'
    assert darabokra_bont(rovid, limit=4000) == [rovid]

    szam_pelda = ('elozmeny szoveg. 1. elso jelentes szovege, tobb mondat. '
                  '2. masodik jelentes szovege. 3. harmadik jelentes.')
    darabok = darabokra_bont(szam_pelda, limit=40)
    assert ''.join(darabok) == szam_pelda, 'a darabolas nem veszthet/ismetelhet karaktert'
    assert any(d.lstrip().startswith('2.') for d in darabok), 'a "2." hatarnal vagnia kell'

    # romai szamos alszakasz-hivatkozas (masik szocikkre mutat) nem szamit sajat
    # betus tagolasnak
    romai_pelda = 'hosszu szoveg eleje. ' * 5 + 'lasd baptizo, II. b. errol. ' + 'vege szoveg. ' * 5
    darabok2 = darabokra_bont(romai_pelda, limit=30)
    assert ''.join(darabok2) == romai_pelda
    print('onteszt: darabolas -- RENDBEN')


def _onteszt_json_validal():
    jo = {'strong': 'G1', 'forditas_hu': 'valami', 'bizonytalan_feloldasok': []}
    _kimenet_validal(jo)
    for rossz in (
        {'strong': 'G1', 'forditas_hu': '', 'bizonytalan_feloldasok': []},
        {'strong': 'G1', 'bizonytalan_feloldasok': []},
        {'strong': 'G1', 'forditas_hu': 'x', 'bizonytalan_feloldasok': 'nem lista'},
        'nem dict',
    ):
        hibazott = False
        try:
            _kimenet_validal(rossz)
        except (ValueError, KeyError):
            hibazott = True
        assert hibazott, 'ennek hibaznia kellett volna: %r' % (rossz,)
    print('onteszt: JSON-validalas -- RENDBEN')


def _onteszt_prompt_epit():
    sablon = 'S={{STRONG}} T={{TERMINOLOGIA}} K={{KAROLI_TABLA}} D={{DARAB_MEGJEGYZES}} F={{FORRAS_SZOVEG}}'
    ki = prompt_epit(sablon, 'G1', 'forras szov', ' (1/2. resz)', 'term', 'karoli')
    assert ki == 'S=G1 T=term K=karoli D= (1/2. resz) F=forras szov'
    print('onteszt: prompt-epites -- RENDBEN')


def onteszt_futtat():
    _onteszt_darabolas()
    _onteszt_json_validal()
    _onteszt_prompt_epit()
    print('minden onteszt RENDBEN')


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--szaraz', action='store_true', help='hivas nelkul, csak becsult token-/koltsegigeny')
    ap.add_argument('--onteszt', action='store_true', help='halozat es kulcs nelkuli onellenorzes')
    ap.add_argument('--modellek', default='m1,m2,m3', help='pl. m1,m2 (alap: mindharom)')
    ap.add_argument('--strongok', default=None, help='vesszovel elvalasztott Strong-lista (alap: mind a 20)')
    ap.add_argument('--plafon', type=float, default=2.0, help='G7: koltsegplafon USD-ben (alap: 2.0)')
    ap.add_argument('--minta', default=MINTA_UT, help='naplok/FORDITAS_P1_minta.tsv')
    args = ap.parse_args()

    if args.onteszt:
        onteszt_futtat()
        return 0

    minta = minta_betolt(args.minta)
    if args.strongok:
        kivalasztott = {s.strip() for s in args.strongok.split(',') if s.strip()}
        minta = [s for s in minta if s['strong'] in kivalasztott]
    if not minta:
        print('HIBA -- ures minta (%s)' % args.minta, file=sys.stderr)
        return 1

    arak = modell_arak_betolt()
    modellek = modellek_felold(args.modellek, arak)
    thayer = thayer_betolt()
    terminologia_sz = terminologia_szoveg(terminologia_betolt())
    karoli_sz = karoli_tabla_szoveg(karoli_tabla_betolt())

    if args.szaraz:
        with open(PROMPT_UT, encoding='utf-8') as fh:
            sablon = fh.read()
        sablon_alap_hossz = len(sablon.replace('{{TERMINOLOGIA}}', terminologia_sz)
                                 .replace('{{KAROLI_TABLA}}', karoli_sz)
                                 .replace('{{STRONG}}', 'G0000')
                                 .replace('{{DARAB_MEGJEGYZES}}', '')
                                 .replace('{{FORRAS_SZOVEG}}', ''))
        becsles_futtatas(minta, modellek, thayer, sablon_alap_hossz)
        return 0

    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print('HIBA -- az OPENROUTER_API_KEY kornyezeti valtozo nincs beallitva', file=sys.stderr)
        return 1

    with open(PROMPT_UT, encoding='utf-8') as fh:
        sablon = fh.read()

    return eles_futtatas(minta, modellek, thayer, sablon, terminologia_sz, karoli_sz,
                          api_key, args.plafon)


if __name__ == '__main__':
    sys.exit(main())
