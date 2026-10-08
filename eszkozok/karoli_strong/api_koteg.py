#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F77 — a Károli–Strong párosítás kötegei az Anthropic Message Batches API-n (vakpróba).

A prompt ugyanabból a kódból jön, mint a subagentes futásnál (`sonnet_koteg.prompt_ir`,
a `prompt_v3` hash-ellenőrzésével). Az SDK helyett REST (`requests`): a pypi.org a
környezetben tiltott (egyeztetett eltérés). A kulcs a `PARDES_API_KEY` környezeti
változóból jön és explicit megy a fejlécbe; nem íródik ki, nem naplózódik, fájlba nem kerül.
Minden kimenet az `f22/vakproba/` alá kerül; a kész adat (`f22/valaszok/`) nem módosul.

  bekuld    egy batch: köteg × effort (custom_id: <könyv>-k<köteg>-<effort>-p<próba>)
  allapot   a batch(ek) állapota
  begyujt   az eredmények letöltése custom_id szerint, kapuellenőrzés, mentés
            <effort>/<könyv>.jsonl (a sonnet_koteg köteg-sor formátumában)
  javit     a kapun bukott kötegek 2. batch-e (a kapu hibaüzenetével)

Használat:
    python eszkozok/karoli_strong/api_koteg.py bekuld --konyv Józs --kotegek 1,6,25,45,53 --effort low,medium,high --cimke vakproba
    python eszkozok/karoli_strong/api_koteg.py allapot
    python eszkozok/karoli_strong/api_koteg.py begyujt --cimke vakproba
    python eszkozok/karoli_strong/api_koteg.py javit --cimke vakproba
    python eszkozok/karoli_strong/api_koteg.py bekuld … --commit [--tetel F77]
    python eszkozok/karoli_strong/api_koteg.py --onteszt

A `--commit` a bekuld / begyujt / javit után commitolja és pusholja az `f22/vakproba/` mappát
(csak azt: `git add -- <út>` és `git commit -- <út>`, soha `-A`), hogy a batch-azonosító és a
begyűjtött kötegek ne vesszenek el egy megszakadt session után. A push hibája nem állítja meg a futást.

Kilépési kódok: 0 rendben; 2 hibás paraméter/előfeltétel; 3 a plafon megállít;
4 hálózati/API-hiba; 5 elfogyott az API-kredit (nincs újrapróbálás).
"""

import argparse
import json
import os
import re
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import kapu  # noqa: E402
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

BASE = 'https://api.anthropic.com'
MODELL = 'claude-sonnet-5-5'
MAX_TOKENS = 32000
PLAFON_USD = 110.00
KULCS_VALTOZO = 'PARDES_API_KEY'
USD_VERS = 0.0074       # `high` szint, Józsué-próba (0,00736 USD/vers, Batch-ár); a könyvplafon alapja
KONYV_SZORZO = 1.5      # a könyvplafon tartaléka
KONYV_MIN_USD = 1.00
VAKPROBA = os.path.join(tokenek.ROOT, 'f22', 'vakproba')
# Batch-ár ($/MTok): a claude-sonnet-5-5 normál ára (2 / 10, cache-olvasás 0,20) fele.
AR_BE, AR_KI, AR_CACHE_OLV, AR_CACHE_IR = 1.00, 5.00, 0.10, 1.25
NAPLO_FEJLEC = ['ts', 'futas', 'koteg', 'probalkozas', 'modell', 'gondolkodas_mod', 'igehely_db', 'kjv',
                'bemenet_token', 'kimenet_token', 'gondolkodas_token', 'koltseg_usd', 'koltseg_forras',
                'kapuhiba_db', 'http_kiserlet', 'idotartam_mp', 'finish_reason', 'prompt_sha256_12',
                'futo_osszeg_usd', 'ok']
BATCH_FEJLEC = ['ts', 'batch_id', 'cimke', 'kor', 'kerelmek_db']
CID = re.compile(r'^(?P<konyv>[A-Za-z0-9]+)-k(?P<koteg>\d+)-(?P<effort>[a-z]+)-p(?P<proba>\d)$')


# ---------- kis segédek ----------

def konyv_nev(ascii_konyv):
    """'Ezs' -> 'Ézs' (a Konyv_normalizalo_tabla magyar rövidítései szerint); ismeretlenre változatlan."""
    f = os.path.join(tokenek.ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
    with open(f, encoding='utf-8') as h:
        for sor in h:
            mezok = sor.rstrip('\n').rstrip('\r').split('\t')
            if len(mezok) > 1 and sonnet_koteg.ascii_nev(mezok[1]) == ascii_konyv:
                return mezok[1]
    return ascii_konyv


def kotegek_tartomany(szoveg):
    """'1,6,25' vagy '1-129' vagy kevert -> [int]."""
    ki = []
    for r in szoveg.split(','):
        if '-' in r:
            a, b = r.split('-')
            ki.extend(range(int(a), int(b) + 1))
        else:
            ki.append(int(r))
    return ki


def custom_id(konyv, koteg, effort, proba):
    return '%s-k%d-%s-p%d' % (sonnet_koteg.ascii_nev(konyv), koteg, effort, proba)


def custom_id_bont(cid):
    m = CID.match(cid)
    if not m:
        return None
    return m.group('konyv'), int(m.group('koteg')), m.group('effort'), int(m.group('proba'))


def koltseg(usage):
    """USD, Batch-áron. A usage.output_tokens a gondolkodást is tartalmazza."""
    u = usage or {}
    return (u.get('input_tokens', 0) * AR_BE + u.get('output_tokens', 0) * AR_KI
            + u.get('cache_read_input_tokens', 0) * AR_CACHE_OLV
            + u.get('cache_creation_input_tokens', 0) * AR_CACHE_IR) / 1e6


def felso_becsles(bemenet_token, kerelmek):
    """A batch költségének felső értéke: minden kérés kimenete a max_tokens-ig megy."""
    return (bemenet_token * AR_BE + kerelmek * MAX_TOKENS * AR_KI) / 1e6


def kulcs():
    k = os.environ.get(KULCS_VALTOZO)
    if not k:
        raise SystemExit('HIBA: a %s környezeti változó nincs beállítva' % KULCS_VALTOZO)
    return k


def kredit_hiba(status, szoveg):
    """Elfogyott-e az API-kredit? (402, vagy 400 'credit balance' / 'billing' üzenettel)"""
    if status == 402:
        return True
    t = (szoveg or '').lower()
    return status == 400 and ('credit balance' in t or 'billing' in t or 'purchase credits' in t)


def http(metodus, ut, torzs=None, nyers=False):
    """Egy REST-hívás. A kulcs csak a fejlécbe kerül; hibaüzenetbe soha."""
    import requests
    fej = {'x-api-key': kulcs(), 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}
    url = ut if ut.startswith('http') else BASE + ut
    for kiserlet in range(3):
        try:
            r = requests.request(metodus, url, headers=fej, data=json.dumps(torzs, ensure_ascii=False).encode('utf-8') if torzs is not None else None, timeout=300)
        except requests.RequestException as e:
            if kiserlet == 2:
                raise SystemExit('HÁLÓZATI HIBA: %s' % type(e).__name__)
            time.sleep(5)
            continue
        if r.status_code in (429, 500, 502, 503, 529) and kiserlet < 2:
            time.sleep(10)
            continue
        if kredit_hiba(r.status_code, r.text):
            print('KREDITHIBA %d: elfogyott az API-kredit. Nem próbálom újra. A kész kötegek a f22/vakproba/ alatt '
                  'maradnak; feltöltés után az `allapot` / `begyujt` mutatja, mi maradt hátra.' % r.status_code, file=sys.stderr)
            raise SystemExit(5)
        if r.status_code >= 400:
            print('API-HIBA %d: %s' % (r.status_code, r.text[:800]), file=sys.stderr)
            raise SystemExit(4)
        return r.text if nyers else r.json()


def uzenet_szoveg(msg):
    return ''.join(b.get('text', '') for b in (msg.get('content') or []) if b.get('type') == 'text')


# ---------- fájlok ----------

def ut(*r):
    return os.path.join(VAKPROBA, *r)


def tsv_hozzaad(fajl, fejlec, sor):
    uj = not os.path.exists(fajl)
    os.makedirs(os.path.dirname(fajl), exist_ok=True)
    with open(fajl, 'a', encoding='utf-8', newline='\n') as f:
        if uj:
            f.write('\t'.join(fejlec) + '\n')
        f.write('\t'.join(str(sor.get(k, '')) for k in fejlec) + '\n')


def tsv_olvas(fajl):
    if not os.path.exists(fajl):
        return []
    with open(fajl, encoding='utf-8') as f:
        s = [x.rstrip('\n').rstrip('\r') for x in f if x.strip()]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def futo_osszeg():
    return sum(float(s['koltseg_usd'] or 0) for s in tsv_olvas(ut('futasnaplo.tsv')))


def allapot_ut(konyv, koteg, effort):
    return ut(effort, '_munka', '%s_k%03d.json' % (sonnet_koteg.ascii_nev(konyv), koteg))


def jsonl_ut(konyv, effort):
    return ut(effort, '%s.jsonl' % sonnet_koteg.ascii_nev(konyv))


# ---------- kérések ----------

def prompt_szoveg(konyv, koteg, koteg_meret=10):
    h = sonnet_koteg.prompt_hash_hiba()
    if h:
        raise SystemExit('BEFAGYASZTÁS HIBA: %s' % h)
    p, ig = sonnet_koteg.prompt_ir(konyv, koteg, koteg_meret)
    with open(p, encoding='utf-8') as f:
        return f.read(), ig


def kerelem_params(uzenetek, effort):
    return {'model': MODELL, 'max_tokens': MAX_TOKENS, 'thinking': {'type': 'adaptive'},
            'output_config': {'effort': effort}, 'messages': uzenetek}


def konyv_versek(konyv, koteg_meret=10):
    return sum(len(x) for x in sonnet_koteg.kotegek_listaja(konyv, koteg_meret))


def konyv_plafon(konyv, koteg_meret=10):
    """Könyvenkénti költségplafon: a könyv versszáma × USD_VERS × 1,5, legalább 1,00 USD (mint a C-nél, DT-F22d)."""
    return max(KONYV_MIN_USD, konyv_versek(konyv, koteg_meret) * USD_VERS * KONYV_SZORZO)


def konyv_koltseg(konyv):
    """A könyv eddigi tényleges API-költsége a futásnaplóban (a `futas` oszlop utolsó tagja a könyv)."""
    n = sonnet_koteg.ascii_nev(konyv)
    return sum(float(x['koltseg_usd'] or 0) for x in tsv_olvas(ut('futasnaplo.tsv')) if x['futas'].split('/')[-1] == n)


def konyv_plafon_ellenorzes(konyv, vers_db, koteg_meret=10):
    """(rendben, üzenet): a könyv eddigi költsége + a most beküldött `vers_db` vers várt költsége a könyvplafon alatt van-e."""
    plafon, eddig, varhato = konyv_plafon(konyv, koteg_meret), konyv_koltseg(konyv), vers_db * USD_VERS
    uz = 'könyvplafon (%s): %.2f USD (%d vers × %.4f × %.1f, min. %.2f); eddig %.4f, most várható %.4f USD' % (
        konyv, plafon, konyv_versek(konyv, koteg_meret), USD_VERS, KONYV_SZORZO, KONYV_MIN_USD, eddig, varhato)
    return eddig + varhato <= plafon, uz


def bekuld(konyv, kotegek, effortok, cimke, koteg_meret=10, hivo=None):
    hivo = hivo or http
    kerelmek, bemenet_db, prompt_szovegek = [], 0, {}
    for k in kotegek:
        szoveg, ig = prompt_szoveg(konyv, k, koteg_meret)
        prompt_szovegek[k] = szoveg
        r = hivo('POST', '/v1/messages/count_tokens', {'model': MODELL, 'messages': [{'role': 'user', 'content': szoveg}]})
        bemenet_db += r['input_tokens'] * len(effortok)
        for e in effortok:
            kerelmek.append({'custom_id': custom_id(konyv, k, e, 1),
                             'params': kerelem_params([{'role': 'user', 'content': szoveg}], e)})
    vers_db = sum(len(prompt_szoveg(konyv, k, koteg_meret)[1]) for k in kotegek) * len(effortok)
    rendben, uz = konyv_plafon_ellenorzes(konyv, vers_db, koteg_meret)
    print(uz)
    if not rendben:
        print('MEGÁLLÁS: a könyvplafon fölött lenne', file=sys.stderr)
        return 3
    becs = felso_becsles(bemenet_db, len(kerelmek))
    ossz = futo_osszeg() + becs
    print('becslés: %d kérés, bemenet %d token, felső költség %.4f USD, eddig %.4f, plafon %.2f USD' % (
        len(kerelmek), bemenet_db, becs, futo_osszeg(), PLAFON_USD))
    if ossz > PLAFON_USD:
        print('MEGÁLLÁS: a felső becslés (%.4f USD) a plafon (%.2f USD) fölött van' % (ossz, PLAFON_USD), file=sys.stderr)
        return 3
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    tsv_hozzaad(ut('batchek.tsv'), BATCH_FEJLEC, {'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()),
                                                  'batch_id': b['id'], 'cimke': cimke, 'kor': 1,
                                                  'kerelmek_db': len(kerelmek)})
    print('batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


def batchek(cimke, kor=None):
    return [b for b in tsv_olvas(ut('batchek.tsv')) if b['cimke'] == cimke and (kor is None or int(b['kor']) == kor)]


def allapot(cimke, hivo=None):
    hivo = hivo or http
    ki = []
    for b in batchek(cimke):
        r = hivo('GET', '/v1/messages/batches/%s' % b['batch_id'])
        print('%s kör=%s: %s %s' % (b['batch_id'], b['kor'], r.get('processing_status'), json.dumps(r.get('request_counts'))))
        ki.append(r.get('processing_status'))
    return ki


# ---------- begyűjtés ----------

def eredmeny_sorok(batch_id, hivo):
    r = hivo('GET', '/v1/messages/batches/%s' % batch_id)
    if r.get('processing_status') != 'ended':
        return None
    szoveg = hivo('GET', r['results_url'], nyers=True)
    return [json.loads(s) for s in szoveg.splitlines() if s.strip()]


def hivas_naplo(konyv, koteg, effort, proba, ig, usage, stop, kapuhiba, ok, ts=None):
    be = (usage.get('input_tokens', 0) + usage.get('cache_read_input_tokens', 0)
          + usage.get('cache_creation_input_tokens', 0))
    c = koltseg(usage)
    tsv_hozzaad(ut('futasnaplo.tsv'), NAPLO_FEJLEC, {
        'ts': ts or time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()),
        'futas': '%s/%s/%s' % (os.path.basename(VAKPROBA), effort, sonnet_koteg.ascii_nev(konyv)), 'koteg': koteg, 'probalkozas': proba,
        'modell': MODELL, 'gondolkodas_mod': 'adaptive,effort=%s' % effort, 'igehely_db': len(ig), 'kjv': 'nem',
        'bemenet_token': be, 'kimenet_token': usage.get('output_tokens', 0), 'gondolkodas_token': '',
        'koltseg_usd': '%.6f' % c, 'koltseg_forras': 'batch_ar_szamolt', 'kapuhiba_db': kapuhiba,
        'http_kiserlet': 1, 'idotartam_mp': '', 'finish_reason': stop,
        'prompt_sha256_12': bemenet.prompt_sha256(bemenet.PROMPT_V3_UT)[:12],
        'futo_osszeg_usd': '%.6f' % (futo_osszeg() + c), 'ok': ok})


def mentes_sor(konyv, koteg, effort, ig, nyersek, versek):
    sor = sonnet_koteg._sor_epit(konyv, koteg, ig, nyersek, versek)
    sor['modell'] = '%s (API, Batch, effort=%s)' % (MODELL, effort)
    sor['hivasok'] = [{'probalkozas': i + 1, 'forras': 'batch_api'} for i in range(len(nyersek))]
    f = jsonl_ut(konyv, effort)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, 'a', encoding='utf-8', newline='\n') as h:
        h.write(json.dumps(sor, ensure_ascii=False) + '\n')


def feldolgoz(sor, koteg_meret=10):
    """Egy batch-eredménysor feldolgozása. Visszaad: (cid, 'kesz'|'javitando'|'kapuhiba', üzenet)."""
    cid = sor['custom_id']
    p = custom_id_bont(cid)
    if not p:
        return cid, 'kapuhiba', 'ismeretlen custom_id'
    ascii_konyv, koteg, effort, proba = p
    konyv = konyv_nev(ascii_konyv)
    ig = sonnet_koteg.kotegek_listaja(konyv, koteg_meret)[koteg - 1]
    res = sor.get('result', {})
    usage, stop, szoveg = {}, res.get('type'), ''
    if res.get('type') == 'succeeded':
        msg = res['message']
        usage, stop, szoveg = msg.get('usage', {}), msg.get('stop_reason'), uzenet_szoveg(msg)
    ak = allapot_ut(konyv, koteg, effort)
    if res.get('type') != 'succeeded' or stop in ('refusal', 'max_tokens'):
        # refusal / hiba / csonkolás: nem újrapróbálandó, a köteg kapuhiba
        hibak = ['1. a kérés nem adott használható választ (%s)' % stop]
        versek = {i: {'allapot': 'kapuhiba', 'probalkozas': proba, 'hibak': hibak, 'obj': None} for i in ig}
        elozo = []
        if proba == 2 and os.path.exists(ak):
            with open(ak, encoding='utf-8') as f:
                elozo = [json.load(f)['nyers1']]
        mentes_sor(konyv, koteg, effort, ig, elozo + [szoveg], versek)
        hivas_naplo(konyv, koteg, effort, proba, ig, usage, stop, len(ig), 'nem')
        return cid, 'kapuhiba', 'stop=%s' % stop
    if proba == 1:
        r = kapu.valasz_ellenoriz(szoveg, ig)
        versek = {i: {'allapot': 'ok' if r[i]['ok'] else 'kapuhiba', 'probalkozas': 1, 'hibak': r[i]['hibak'],
                      'obj': r[i]['obj'] if r[i]['ok'] else None} for i in ig}
        rossz = [i for i in ig if not r[i]['ok']]
        hivas_naplo(konyv, koteg, effort, 1, ig, usage, stop, len(rossz), 'nem' if rossz else 'igen')
        if rossz:
            os.makedirs(os.path.dirname(ak), exist_ok=True)
            with open(ak, 'w', encoding='utf-8', newline='\n') as f:
                json.dump({'nyers1': szoveg, 'versek': versek, 'uzenet': kapu.ujrakeres_uzenet({i: r[i] for i in rossz})},
                          f, ensure_ascii=False)
            return cid, 'javitando', '%d kapuhibás vers' % len(rossz)
        mentes_sor(konyv, koteg, effort, ig, [szoveg], versek)
        return cid, 'kesz', 'ok'
    with open(ak, encoding='utf-8') as f:
        elozo = json.load(f)
    versek = elozo['versek']
    rossz = [i for i in ig if versek[i]['allapot'] != 'ok']
    r2 = kapu.valasz_ellenoriz(szoveg, rossz)
    for i in rossz:
        if r2[i]['ok']:
            versek[i] = {'allapot': 'ok', 'probalkozas': 2, 'hibak': [], 'obj': r2[i]['obj']}
        else:
            versek[i] = {'allapot': 'kapuhiba', 'probalkozas': 2, 'hibak': r2[i]['hibak'], 'obj': None}
    veg = sum(1 for i in ig if versek[i]['allapot'] != 'ok')
    mentes_sor(konyv, koteg, effort, ig, [elozo['nyers1'], szoveg], versek)
    hivas_naplo(konyv, koteg, effort, 2, ig, usage, stop, veg, 'nem' if veg else 'igen')
    return cid, ('kapuhiba' if veg else 'kesz'), '%d végleges kapuhiba' % veg


def kesz_cidek():
    """Már feldolgozott (custom_id) — a futasnaplo (futas, koteg, probalkozas) alapján."""
    ki = set()
    for s in tsv_olvas(ut('futasnaplo.tsv')):
        _, effort, kn = s['futas'].split('/')
        ki.add('%s-k%d-%s-p%s' % (kn, int(s['koteg']), effort, s['probalkozas']))
    return ki


def begyujt(cimke, kor=None, hivo=None):
    hivo = hivo or http
    kesz = kesz_cidek()
    javitando, kapuhiba = [], []
    for b in batchek(cimke, kor):
        sorok = eredmeny_sorok(b['batch_id'], hivo)
        if sorok is None:
            print('%s: még nem ért véget' % b['batch_id'])
            continue
        for s in sorok:           # custom_id szerint, soha nem pozíció szerint
            if s['custom_id'] in kesz:
                continue
            cid, allapot, uz = feldolgoz(s)
            print('%s: %s (%s)' % (cid, allapot, uz))
            (javitando if allapot == 'javitando' else kapuhiba if allapot == 'kapuhiba' else []).append(cid)
    lista = javitando_lista()
    with open(ut('javitando.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(c + '\n' for c in lista))
    print('javítandó (összesen, még nem javított): %d, ebben a körben kapuhiba: %d; futó összeg %.4f USD' % (len(lista), len(kapuhiba), futo_osszeg()))
    return 0


def javitando_lista():
    """Az 1. próbán kapuhibás (állapotfájllal rendelkező), de még nem javított kötegek custom_id-i."""
    kesz = kesz_cidek()
    ki = []
    for c in sorted(kesz):
        p = custom_id_bont(c)
        if p[3] != 1 or c[:-1] + '2' in kesz:
            continue
        konyv = konyv_nev(p[0])
        if os.path.exists(allapot_ut(konyv, p[1], p[2])):
            ki.append(c)
    return ki


def javit(cimke, koteg_meret=10, hivo=None):
    hivo = hivo or http
    jf = ut('javitando.txt')
    cidek = [x.strip() for x in open(jf, encoding='utf-8')] if os.path.exists(jf) else []
    cidek = [c for c in cidek if c]
    if not cidek:
        print('nincs javítandó köteg')
        return 0
    kerelmek, bemenet_db = [], 0
    for cid in cidek:
        ascii_konyv, koteg, effort, _ = custom_id_bont(cid)
        konyv = konyv_nev(ascii_konyv)
        szoveg, _ = prompt_szoveg(konyv, koteg, koteg_meret)
        with open(allapot_ut(konyv, koteg, effort), encoding='utf-8') as f:
            elozo = json.load(f)
        msgs = [{'role': 'user', 'content': szoveg}, {'role': 'assistant', 'content': elozo['nyers1']},
                {'role': 'user', 'content': elozo['uzenet']}]
        bemenet_db += hivo('POST', '/v1/messages/count_tokens', {'model': MODELL, 'messages': msgs})['input_tokens']
        kerelmek.append({'custom_id': custom_id(konyv, koteg, effort, 2), 'params': kerelem_params(msgs, effort)})
    jav_versek = {}
    for k in kerelmek:
        ascii_konyv, kot, _, _ = custom_id_bont(k['custom_id'])
        jav_versek[ascii_konyv] = jav_versek.get(ascii_konyv, 0) + len(sonnet_koteg.kotegek_listaja(konyv_nev(ascii_konyv), koteg_meret)[kot - 1])
    for ak, vdb in jav_versek.items():
        rendben, uz = konyv_plafon_ellenorzes(konyv_nev(ak), vdb, koteg_meret)
        print(uz)
        if not rendben:
            print('MEGÁLLÁS: a könyvplafon fölött lenne', file=sys.stderr)
            return 3
    becs = felso_becsles(bemenet_db, len(kerelmek))
    print('javító becslés: %d kérés, felső költség %.4f USD, eddig %.4f' % (len(kerelmek), becs, futo_osszeg()))
    if futo_osszeg() + becs > PLAFON_USD:
        print('MEGÁLLÁS: a plafon fölött', file=sys.stderr)
        return 3
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    tsv_hozzaad(ut('batchek.tsv'), BATCH_FEJLEC, {'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()),
                                                  'batch_id': b['id'], 'cimke': cimke, 'kor': 2,
                                                  'kerelmek_db': len(kerelmek)})
    print('javító batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


# ---------- önteszt ----------

def onteszt():
    import tempfile
    global VAKPROBA
    hibak = []
    VAKPROBA = tempfile.mkdtemp()
    if custom_id('Józs', 6, 'low', 1) != 'Jozs-k6-low-p1' or custom_id_bont('Jozs-k6-low-p1') != ('Jozs', 6, 'low', 1):
        hibak.append('custom_id')
    if abs(koltseg({'input_tokens': 1000000, 'output_tokens': 1000000}) - 6.0) > 1e-9:
        hibak.append('költség')
    if felso_becsles(0, 1) != MAX_TOKENS * AR_KI / 1e6:
        hibak.append('felső becslés')
    # a prompt és a hash
    szoveg, ig = prompt_szoveg('Józs', 1)
    if len(ig) != 10 or 'Józs 1:1' not in szoveg:
        hibak.append('prompt_ir')
    # hamis hívó: count_tokens, batch-létrehozás, eredmények (köteg 1 helyes válasza a meglévő adatból; köteg 6 hibás)
    kesz = [json.loads(s) for s in open(os.path.join(tokenek.ROOT, 'f22', 'valaszok', 'sonnet', 'Jozs.jsonl'), encoding='utf-8')]
    jo = next(s for s in kesz if s['igehelyek'] == ig)
    jo_szoveg = json.dumps([jo['versek'][i]['obj'] for i in ig], ensure_ascii=False)
    kuldott = {}

    def hamis(met, path, torzs=None, nyers=False):
        if path.endswith('count_tokens'):
            return {'input_tokens': 10000}
        if met == 'POST':
            kuldott['kerelmek'] = torzs['requests']
            return {'id': 'msgbatch_teszt'}
        if path.startswith('/v1/messages/batches/'):
            return {'processing_status': 'ended', 'results_url': 'https://x/r', 'request_counts': {}}
        usage = {'input_tokens': 10000, 'output_tokens': 5000}
        sorok = [
            {'custom_id': custom_id('Józs', 1, 'low', 1), 'result': {'type': 'succeeded', 'message': {
                'content': [{'type': 'thinking', 'thinking': ''}, {'type': 'text', 'text': jo_szoveg}],
                'usage': usage, 'stop_reason': 'end_turn'}}},
            {'custom_id': custom_id('Józs', 6, 'low', 1), 'result': {'type': 'succeeded', 'message': {
                'content': [{'type': 'text', 'text': 'nem json'}], 'usage': usage, 'stop_reason': 'end_turn'}}},
            {'custom_id': custom_id('Józs', 25, 'low', 1), 'result': {'type': 'succeeded', 'message': {
                'content': [], 'usage': usage, 'stop_reason': 'refusal'}}}]
        return '\n'.join(json.dumps(s, ensure_ascii=False) for s in reversed(sorok))   # fordított sorrend: custom_id szerint kell
    if bekuld('Józs', [1, 6], ['low', 'high'], 't', hivo=hamis) != 0:
        hibak.append('bekuld')
    if [k['custom_id'] for k in kuldott.get('kerelmek', [])] != ['Jozs-k1-low-p1', 'Jozs-k1-high-p1', 'Jozs-k6-low-p1', 'Jozs-k6-high-p1']:
        hibak.append('kérések custom_id-ja')
    p = kuldott['kerelmek'][0]['params']
    if p['thinking'] != {'type': 'adaptive'} or p['output_config'] != {'effort': 'low'} or p['model'] != MODELL or p['max_tokens'] != 32000:
        hibak.append('kérés paraméterei')
    begyujt('t', hivo=hamis)
    sorok = tsv_olvas(ut('futasnaplo.tsv'))
    if len(sorok) != 3:
        hibak.append('futásnapló sorai: %d' % len(sorok))
    if not os.path.exists(jsonl_ut('Józs', 'low')) or len(open(jsonl_ut('Józs', 'low'), encoding='utf-8').readlines()) != 2:
        hibak.append('mentett köteg-sorok (1 kész + 1 refusal-kapuhiba)')
    if [x.strip() for x in open(ut('javitando.txt'), encoding='utf-8') if x.strip()] != ['Jozs-k6-low-p1']:
        hibak.append('javítandó lista')
    begyujt('t', hivo=hamis)   # második futás: nem dolgoz fel újra
    if len(tsv_olvas(ut('futasnaplo.tsv'))) != 3:
        hibak.append('idempotencia')
    if not (kredit_hiba(402, '') and kredit_hiba(400, '{"error":{"message":"Your credit balance is too low"}}')
            and not kredit_hiba(400, 'invalid_request') and not kredit_hiba(429, 'rate limit')):
        hibak.append('kredit_hiba felismerés')
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        def g(*x):
            return subprocess.run(['git'] + list(x), cwd=td, capture_output=True, text=True, encoding='utf-8')
        g('init', '-q'); g('config', 'user.email', 't@t'); g('config', 'user.name', 't')
        os.makedirs(os.path.join(td, 'f22', 'vakproba'))
        open(os.path.join(td, 'f22', 'vakproba', 'batchek.tsv'), 'w', encoding='utf-8').write('x\n')
        open(os.path.join(td, 'mas.txt'), 'w', encoding='utf-8').write('nem ide tartozik\n')
        g('add', 'mas.txt')   # előre stage-elt, nem vakproba fájl: nem kerülhet a commitba
        e1 = git_mentes('T: próba ékezetek: árvíztűrő', ['f22/vakproba'], push=False, cwd=td)
        e2 = git_mentes('T: üres', ['f22/vakproba'], push=False, cwd=td)
        fajlok = g('show', '--name-only', '--format=%s', 'HEAD').stdout.split('\n')
        if e1 != 'commit' or e2 != 'nincs_valtozas' or 'f22/vakproba/batchek.tsv' not in fajlok or 'mas.txt' in fajlok \
                or 'árvíztűrő' not in fajlok[0]:
            hibak.append('git_mentes (%s, %s, %s)' % (e1, e2, fajlok))
    if konyv_nev('Ezs') != 'Ézs' or konyv_nev('Jozs') != 'Józs' or kotegek_tartomany('1-3,7') != [1, 2, 3, 7]:
        hibak.append('konyv_nev / kotegek_tartomany')
    if abs(konyv_plafon('Józs') - 658 * USD_VERS * KONYV_SZORZO) > 1e-9 or konyv_plafon_ellenorzes('Józs', 10)[0] is not True \
            or konyv_plafon_ellenorzes('Józs', 10000)[0] is not False:
        hibak.append('könyvplafon')
    for h in hibak:
        print('ÖNTESZT HIBA: ' + h, file=sys.stderr)
    print('önteszt: %s' % ('HIBA' if hibak else 'rendben'))
    return 1 if hibak else 0


def atvezet(konyv, effort):
    """Az API-futás kész köteg-sorait az éles `f22/valaszok/sonnet/<könyv>.jsonl`-be másolja (ami még nincs benne).
    A sorformátum azonos a sonnet_koteg._sor_epit-tel. Kapuhibás (végleges) köteg is átmegy, mint a subagentes futásnál.
    Visszaad: (átvezetett, már bent volt)."""
    forras = jsonl_ut(konyv, effort)
    if not os.path.exists(forras):
        print('HIBA: nincs %s' % forras, file=sys.stderr)
        return 2
    cel = sonnet_koteg.valasz_ut(konyv)
    bent = {tuple(x['igehelyek']) for x in sonnet_koteg.sorok_beolvas(cel)}
    uj = 0
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    with open(forras, encoding='utf-8') as f, open(cel, 'a', encoding='utf-8', newline='\n') as h:
        for sor in f:
            if not sor.strip():
                continue
            d = json.loads(sor)
            if tuple(d['igehelyek']) in bent:
                continue
            h.write(sor if sor.endswith('\n') else sor + '\n')
            bent.add(tuple(d['igehelyek']))
            uj += 1
    print('átvezetve: %d köteg → %s (már bent volt: %d)' % (uj, cel, len(bent) - uj))
    return 0


def git_mentes(uzenet, utak=None, push=True, cwd=None):
    """Az `utak` (alap: f22/vakproba/) commitja és pusholása. Csak a megnevezett utak kerülnek bele.
    Visszaad: 'commit' | 'nincs_valtozas' | 'hiba'. A push hibája csak figyelmeztetés."""
    import subprocess
    import tempfile
    cwd = cwd or tokenek.ROOT
    utak = utak or [os.path.relpath(VAKPROBA, tokenek.ROOT).replace(os.sep, '/')]

    def git(*args):
        return subprocess.run(['git', '-c', 'i18n.commitEncoding=UTF-8'] + list(args), cwd=cwd,
                              capture_output=True, text=True, encoding='utf-8')
    if git('add', '--', *utak).returncode != 0:
        print('GIT-FIGYELMEZTETÉS: a git add nem sikerült', file=sys.stderr)
        return 'hiba'
    if git('diff', '--cached', '--quiet', '--', *utak).returncode == 0:
        return 'nincs_valtozas'
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8', newline='\n') as f:
        f.write(uzenet + '\n')
        uzfajl = f.name
    try:
        r = git('commit', '-q', '-F', uzfajl, '--', *utak)
    finally:
        os.unlink(uzfajl)
    if r.returncode != 0:
        print('GIT-FIGYELMEZTETÉS: a commit nem sikerült: %s' % r.stderr.strip()[:300], file=sys.stderr)
        return 'hiba'
    if push:
        for kiserlet in range(4):
            if git('push', '-q', '-u', 'origin', 'HEAD').returncode == 0:
                break
            time.sleep(2 ** (kiserlet + 1))
        else:
            print('GIT-FIGYELMEZTETÉS: a push nem sikerült (a commit megvan helyben)', file=sys.stderr)
    return 'commit'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('parancs', nargs='?', choices=['bekuld', 'allapot', 'begyujt', 'javit', 'atvezet'])
    ap.add_argument('--konyv', default=None)
    ap.add_argument('--kotegek', default=None)
    ap.add_argument('--effort', default=None)
    ap.add_argument('--cimke', default=None)
    ap.add_argument('--kor', type=int, default=None)
    ap.add_argument('--gyoker', default=None, help='állapot/kimenet gyökere (alap: f22/vakproba; éles futás: pl. f22/api_termeles)')
    ap.add_argument('--commit', action='store_true', help='a művelet után commit + push (f22/vakproba/)')
    ap.add_argument('--tetel', default='F77', help='a commit-üzenet tétel-előtagja')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.gyoker:
        global VAKPROBA
        VAKPROBA = os.path.join(tokenek.ROOT, a.gyoker)
    if a.onteszt:
        return onteszt()
    if not a.parancs or not a.cimke:
        print('HIBA: parancs és --cimke kell', file=sys.stderr)
        return 2
    if a.parancs == 'allapot':
        allapot(a.cimke)
        return 0
    if a.parancs == 'atvezet':
        if not a.konyv:
            print('HIBA: --konyv kell', file=sys.stderr)
            return 2
        kod = atvezet(a.konyv, (a.effort or 'high').split(',')[0])
        if kod == 0 and a.commit:
            git_mentes('%s: api_koteg atvezet (%s) — kész kötegek az f22/valaszok/sonnet-be' % (a.tetel, a.konyv),
                       [os.path.relpath(sonnet_koteg.valasz_ut(a.konyv), tokenek.ROOT).replace(os.sep, '/')])
        return kod
    if a.parancs == 'bekuld' and not (a.konyv and a.kotegek and a.effort):
        print('HIBA: --konyv, --kotegek, --effort kell', file=sys.stderr)
        return 2
    kod = 1
    try:   # a commit hiba/megszakadás esetén is megtörténik: ami addig elkészült, ne vesszen el
        if a.parancs == 'bekuld':
            kod = bekuld(a.konyv, kotegek_tartomany(a.kotegek), a.effort.split(','), a.cimke)
        elif a.parancs == 'begyujt':
            kod = begyujt(a.cimke, a.kor)
        else:
            kod = javit(a.cimke)
    finally:
        if a.commit:
            git_mentes('%s: api_koteg %s (%s)' % (a.tetel, a.parancs, a.cimke))
    return kod

if __name__ == '__main__':
    sys.exit(main())
