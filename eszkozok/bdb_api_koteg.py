#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F38 — a BDB-fordítás adagjai az Anthropic Message Batches API-n (a 13. adagtól; DT-F38y).

Az `eszkozok/karoli_strong/api_koteg.py` mintájára: ugyanaz a REST-hívó, költségszámítás, napló és git-mentés
(import, nem másolat); a `PARDES_API_KEY` környezeti változóból jön a kulcs, nem íródik ki, fájlba nem kerül.
A prompt a meglévő kódból épül (`emeles.prompt_epit`, prompt v5, a szakaszok `szakasz_bemenet.csoportok`
szerinti csoportjai; a `szakasz_promptok` párja azzal a különbséggel, hogy a héber–görög szakaszok a
`helyorzo_bont` ⟦n⟧ helyőrzőit kapják, mint a Code-os úton a `_szakasz_hely.txt`; a visszaállítás betűhű).
A szakasztáblán kívüli Strong a régi `teljes` úton megy (prompt v4, `custom_id` `…-c1-…`, mint a többi).

Egység: Strong (a 20 000 karakter fölötti szócikk csoportjai külön kérések). `custom_id` = `<strong>-c<csoport>-p<próba>`.

  szaraz    a kérések összeállítása hálózat nélkül: token- és költségbecslés, csomagolási terv (nem küld)
  bekuld    a következő csomag (chunk) beküldése, a plafon ellenőrzésével
  allapot   a batch-ek állapota
  begyujt   a kész batch-ek nyers válaszai (custom_id szerint) a valaszok.jsonl-be, költségnapló
  kapuz     válasz → JSON → helyőrző-visszaállítás → javítóréteg + kapusor (`emeles.utofeldolgoz_szakasz`);
            kimenet: kapu_eredmeny.jsonl (kesz / javitando / kapuhiba)
  javit     a kapun bukott Strongok 2. batch-e (a kapu hibaüzenetével)
  rogzit    a kapun átment Strongok sorai az EMELES_munka.tsv-be és az adat/forditasok.tsv-be; a kétszer bukott
            Strongok a naplok/BDB_FORDITAS_hibas.tsv-be

Használat:
    python eszkozok/bdb_api_koteg.py --adag 13 szaraz
    python eszkozok/bdb_api_koteg.py --adag 13 bekuld
    python eszkozok/bdb_api_koteg.py --adag 13 allapot|begyujt|kapuz|javit|rogzit
    python eszkozok/bdb_api_koteg.py --onteszt

Kilépési kódok: 0 rendben; 2 hibás paraméter/előfeltétel; 3 a plafon megállít; 4/5 az api_koteg.py szerint.
TSV: split('\\t'), '\\t'.join(); csv modul nincs.
"""

import argparse
import datetime
import gzip
import hashlib
import tempfile
import json
import os
import re
import sys
import time
import types

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
sys.path.insert(0, os.path.join(ITT, 'karoli_strong'))
sys.path.insert(0, os.path.join(ITT, 'bdb_jelolt'))
import api_koteg as AK  # noqa: E402
import emeles as E  # noqa: E402
import szakasz_bemenet as SB  # noqa: E402

ROOT = AK.tokenek.ROOT
MODELL = AK.MODELL                 # claude-sonnet-5-5
EFFORT = 'high'                    # az orkesztrátor rögzítette (2026-11-01)
PLAFON_USD = 15.00                 # kemény plafon az adagra
SORREND = os.path.join(ROOT, 'naplok', 'BDB_FORDITAS_sorrend.tsv')
HIBAS_UT = os.path.join(ROOT, 'naplok', 'BDB_FORDITAS_hibas.tsv')
MUNKA_GYOKER = os.path.join(ROOT, 'forditas', 'bdb_api')
CSOMAG = 450                       # kérés / batch (a plafon csomagonként ellenőrződik)
CACHE_TTL = '1h'
CACHE_GYOKER = os.environ.get('PARDES_BDB_CACHE') or os.path.join(tempfile.gettempdir(), 'bdb_api_cache')   # a repón kívül
PROCESSZEK = 4
TOKEN_KARAKTER = 2.8               # becslés (manual): a prompt karaktere / token; az első csomag után mérttel váltható
KIMENET_ARANY = 0.5                # becslés (manual): kimeneti token / forráskarakter (magyar szöveg)
GONDOLKODAS_BECSLES = 1500         # becslés (manual): gondolkodási token / kérés (effort=high)
# Batch-ár ($/MTok): a claude-sonnet-5-5 normál árának fele (api_koteg.py); 1 órás cache-írás: 2 × a bemeneti ár
AR_BE, AR_KI, AR_CACHE_OLV, AR_CACHE_IR_5M, AR_CACHE_IR_1H = 1.00, 5.00, 0.10, 1.25, 2.00
NAPLO_FEJLEC = ['ts', 'custom_id', 'modell', 'effort', 'bemenet_token', 'cache_olvasas', 'cache_iras', 'kimenet_token',
                'stop_reason', 'koltseg_usd', 'futo_osszeg_usd']
BATCH_FEJLEC = ['ts', 'batch_id', 'cimke', 'kor', 'csomag', 'kerelmek_db']
CID = re.compile(r'^(?P<strong>[GH]\d{4}[a-z]?)-c(?P<csoport>\d+)-p(?P<proba>\d)$')
KOT_JEL = 'Az e forrásban előforduló kulcsok gépi kigyűjtése:\n\n'
BEMENET_JEL = '## Bemenet'

MUNKA = MUNKA_GYOKER      # adagonként: MUNKA/adag<N>/ (a main() állítja)


# ---------- segédek ----------

def ut(*r):
    return os.path.join(MUNKA, *r)


def custom_id(strong, csoport, proba):
    return '%s-c%d-p%d' % (strong, csoport, proba)


def custom_id_bont(cid):
    m = CID.match(cid)
    return (m.group('strong'), int(m.group('csoport')), int(m.group('proba'))) if m else None


def koltseg(usage):
    """USD, Batch-áron. Az output_tokens a gondolkodást is tartalmazza."""
    u = usage or {}
    cc = u.get('cache_creation') or {}
    ir5, ir1 = cc.get('ephemeral_5m_input_tokens', 0), cc.get('ephemeral_1h_input_tokens', 0)
    if not cc:
        ir5 = u.get('cache_creation_input_tokens', 0)
    return (u.get('input_tokens', 0) * AR_BE + u.get('output_tokens', 0) * AR_KI
            + u.get('cache_read_input_tokens', 0) * AR_CACHE_OLV + ir5 * AR_CACHE_IR_5M + ir1 * AR_CACHE_IR_1H) / 1e6


def jsonl_olvas(fajl):
    if not os.path.exists(fajl):
        return []
    with open(fajl, encoding='utf-8') as f:
        return [json.loads(s) for s in f if s.strip()]


def jsonl_hozzaad(fajl, sorok):
    os.makedirs(os.path.dirname(fajl), exist_ok=True)
    with open(fajl, 'a', encoding='utf-8', newline='\n') as f:
        for s in sorok:
            f.write(json.dumps(s, ensure_ascii=False) + '\n')


def futo_osszeg():
    return sum(float(s['koltseg_usd'] or 0) for s in AK.tsv_olvas(ut('futasnaplo.tsv')))


def adag_strongok(adag):
    ki = []
    with open(SORREND, encoding='utf-8') as f:
        for sor in f:
            m = sor.rstrip('\n').rstrip('\r').split('\t')
            if len(m) >= 5 and m[4] == str(adag):
                ki.append(m[1])
    return ki


# ---------- a kérések ----------

def blokkok(prompt):
    """A prompt három szöveg-blokkra bontva (az összefűzésük a prompt): [közös eleje | kötelező-alak lista + állandó farok |
    adatblokk + forrás]; az első kettő cache-pontot kap. A kötelező lista Strongonként változik, ezért a cache-hit a
    azonos listájú kérések között jön (a kérések lista szerint rendezettek)."""
    cut = prompt.rfind(BEMENET_JEL)
    j = prompt.find(KOT_JEL)
    if cut < 0:
        return [prompt]
    if j < 0 or j + len(KOT_JEL) >= cut:
        return [prompt[:cut], prompt[cut:]]
    j += len(KOT_JEL)
    return [prompt[:j], prompt[j:cut], prompt[cut:]]


def uzenet_tartalom(prompt):
    bl = blokkok(prompt)
    ki = []
    for i, b in enumerate(bl):
        d = {'type': 'text', 'text': b}
        if i < len(bl) - 1:
            d['cache_control'] = {'type': 'ephemeral', 'ttl': CACHE_TTL}
        ki.append(d)
    return ki


def kerelmek_strongra(strong):
    """[{strong, csoport, db, prompt, hely, forras_kar, kot}] — a szakaszonkénti út, vagy a régi `teljes` út."""
    sp = E.strong_padded(strong)
    szak = SB.szakaszok(sp)
    if szak is None:
        szoveg = E.forras_szoveg(sp)[1]
        bont, hely = E.helyorzo_bont(szoveg)
        return [{'strong': sp, 'csoport': 1, 'db': 1, 'mod': 'teljes', 'hely': hely, 'forras_kar': len(szoveg),
                 'prompt': E.prompt_epit(sp, bont, '', None), 'kot': E.kotelezo_alakok_szoveg(bont)}]
    cs = SB.csoportok(szak)
    ki = []
    for i, c in enumerate(cs):
        tok = SB.tokenes(c)
        bont, hely = E.helyorzo_bont(tok)
        ki.append({'strong': sp, 'csoport': i + 1, 'db': len(cs), 'mod': 'szakasz', 'hely': hely, 'forras_kar': len(tok),
                   'prompt': E.prompt_epit(sp, bont, E.darab_info_szoveg(i, len(cs)), E.PROMPT_V5_UT),
                   'kot': E.kotelezo_alakok_szoveg(bont)})
    return ki


def max_tokens_kerelemre(forras_kar):
    return int(min(64000, max(16000, 3 * (forras_kar * KIMENET_ARANY + GONDOLKODAS_BECSLES) + 4000)))


def kerelem_params(uzenetek, forras_kar, max_tokens=None):
    return {'model': MODELL, 'max_tokens': max_tokens or max_tokens_kerelemre(forras_kar),
            'thinking': {'type': 'adaptive'}, 'output_config': {'effort': EFFORT}, 'messages': uzenetek}


def _epit(strong):
    return kerelmek_strongra(strong)


def _rendez(ker):
    szamlal = {}
    for k in ker:
        szamlal[k['kot']] = szamlal.get(k['kot'], 0) + 1
    ker.sort(key=lambda k: (-szamlal[k['kot']], k['kot'], k['strong'], k['csoport']))
    return ker


def terv(adag, strongok=None):
    """Az adag összes 1. próbás kérése, a kötelező-lista szerint rendezve (azonos cache-prefix egymás mellett).
    Teljes adagra a felépítés (Strongonként ~0,5 mp, az adatblokk miatt) párhuzamos, és a repón kívüli gyorsítótárba
    kerül: a javító kör és a rögzítés ugyanazt a promptot és helyőrző-listát látja, mint az 1. beküldés."""
    if strongok is not None:
        return _rendez([k for s in strongok for k in kerelmek_strongra(s)])
    lista = adag_strongok(adag)
    cache = os.path.join(CACHE_GYOKER, 'adag%s_terv.jsonl.gz' % adag)
    if os.path.exists(cache):
        with gzip.open(cache, 'rt', encoding='utf-8') as f:
            ker = [json.loads(x) for x in f if x.strip()]
        if {k['strong'] for k in ker} == {E.strong_padded(s) for s in lista}:
            return ker
    import multiprocessing
    with multiprocessing.Pool(PROCESSZEK) as pool:
        ker = [k for r in pool.imap(_epit, lista, chunksize=25) for k in r]
    ker = _rendez(ker)
    os.makedirs(CACHE_GYOKER, exist_ok=True)
    with gzip.open(cache, 'wt', encoding='utf-8') as f:
        for k in ker:
            f.write(json.dumps(k, ensure_ascii=False) + '\n')
    return ker


def ker_index(adag, strongok=None):
    """{strong: [kérések csoport szerint]} a terv(-gyorsítótár)ból."""
    ki = {}
    for k in terv(adag, strongok):
        ki.setdefault(k['strong'], []).append(k)
    for v in ki.values():
        v.sort(key=lambda k: k['csoport'])
    return ki


def prompt_hash(prompt):
    return hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:12]


def becsles(ker):
    """(bemenet_token, kimenet_token, USD cache nélkül, USD a várt cache-találattal) — mind becslés (manual)."""
    be = sum(len(k['prompt']) / TOKEN_KARAKTER for k in ker)
    ki = sum(k['forras_kar'] * KIMENET_ARANY + GONDOLKODAS_BECSLES for k in ker)
    nincs = (be * AR_BE + ki * AR_KI) / 1e6
    # cache: az azonos kötelező-listájú kérések az első után a prompt farkát olvasják
    lista = {}
    for k in ker:
        lista.setdefault(k['kot'], []).append(k)
    cache_be = 0.0
    for cs in lista.values():
        cache = len(cs[0]['prompt'][:cs[0]['prompt'].rfind(BEMENET_JEL)]) / TOKEN_KARAKTER
        ir = cache * AR_CACHE_IR_1H
        olv = (len(cs) - 1) * cache * AR_CACHE_OLV
        valt = sum(len(k['prompt']) / TOKEN_KARAKTER - cache for k in cs) * AR_BE
        cache_be += ir + olv + valt
    return be, ki, nincs, (cache_be + ki * AR_KI) / 1e6


def csomagok(ker, meret=CSOMAG):
    return [ker[i:i + meret] for i in range(0, len(ker), meret)]


# ---------- szaraz ----------

def szaraz(adag):
    t0 = time.time()
    ker = terv(adag)
    strongok = adag_strongok(adag)
    kar = sum(k['forras_kar'] for k in ker)
    be, ki, nincs, cache = becsles(ker)
    csom = csomagok(ker)
    print('adag %s: %d Strong, %d kérés (%d teljes-út, %d többcsoportos Strong), forrás %d karakter (tokenes bemenet)' % (
        adag, len(strongok), len(ker), sum(1 for k in ker if k['mod'] == 'teljes'),
        len({k['strong'] for k in ker if k['db'] > 1}), kar))
    print('promptok: összesen %d karakter, átlag %d; különböző kötelező-listák: %d' % (
        sum(len(k['prompt']) for k in ker), sum(len(k['prompt']) for k in ker) // max(1, len(ker)), len({k['kot'] for k in ker})))
    print('becslés (manual; %.1f karakter/token, kimenet %.2f token/forráskarakter + %d gondolkodási token/kérés): '
          'bemenet %.0f token, kimenet %.0f token' % (TOKEN_KARAKTER, KIMENET_ARANY, GONDOLKODAS_BECSLES, be, ki))
    print('költség Batch-áron: cache nélkül %.2f USD, várt cache-találattal %.2f USD; plafon %.2f USD' % (nincs, cache, PLAFON_USD))
    print('csomagok: %d × ~%d kérés' % (len(csom), CSOMAG))
    print('max_tokens: %d–%d; modell %s, effort %s; (%.1f mp)' % (
        min(max_tokens_kerelemre(k['forras_kar']) for k in ker), max(max_tokens_kerelemre(k['forras_kar']) for k in ker),
        MODELL, EFFORT, time.time() - t0))
    return 0


# ---------- beküldés ----------

def batchek(cimke=None, kor=None):
    return [b for b in AK.tsv_olvas(ut('batchek.tsv'))
            if (cimke is None or b['cimke'] == cimke) and (kor is None or int(b['kor']) == kor)]


def bekuldott_cidek():
    ki = set()
    for f in os.listdir(ut()) if os.path.isdir(ut()) else []:
        if f.startswith('csomag_') and f.endswith('.txt'):
            with open(ut(f), encoding='utf-8') as h:
                ki.update(x.split('	')[0].strip() for x in h if x.strip())
    return ki


def csomag_kiertekelt(cimke):
    """Az eddigi csomagok költsége és kérésszáma → a következő csomag becslése a mért költségből."""
    naplo = AK.tsv_olvas(ut('futasnaplo.tsv'))
    return len(naplo), sum(float(s['koltseg_usd']) for s in naplo)


def bekuld(adag, cimke, hivo=None, strongok=None):
    hivo = hivo or AK.http
    ker = terv(adag, strongok)
    kesz = bekuldott_cidek()
    csom = csomagok(ker)
    index = next((i for i, c in enumerate(csom) if custom_id(c[0]['strong'], c[0]['csoport'], 1) not in kesz), None)
    if index is None:
        print('minden csomag beküldve')
        return 0
    cs = csom[index]
    ncs = len(csom)
    n_ker, eddig = csomag_kiertekelt(cimke)
    if n_ker >= 20:      # mért költségből
        egyseg = eddig / n_ker
        becs = len(cs) * egyseg * 1.25
        forras = 'mért átlag %.5f USD/kérés × 1,25' % egyseg
    else:
        becs = becsles(cs)[2] if index == 0 else becsles(cs)[3]
        forras = 'becslés (manual)%s' % (', cache nélkül' if index == 0 else '')
    ossz = futo_osszeg() + becs
    print('csomag %d/%d: %d kérés; költség-felső %s: %.2f USD; eddig %.4f USD; plafon %.2f USD' % (
        index + 1, ncs, len(cs), forras, becs, futo_osszeg(), PLAFON_USD))
    if ossz > PLAFON_USD:
        print('MEGÁLLÁS: a becsült költség (%.2f USD) a plafon (%.2f USD) fölött lenne' % (ossz, PLAFON_USD), file=sys.stderr)
        return 3
    kerelmek = [{'custom_id': custom_id(k['strong'], k['csoport'], 1),
                 'params': kerelem_params([{'role': 'user', 'content': uzenet_tartalom(k['prompt'])}], k['forras_kar'])}
                for k in cs]
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    os.makedirs(ut(), exist_ok=True)
    with open(ut('csomag_%02d.txt' % (index + 1)), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(k['custom_id'] + '\n' for k in kerelmek))
    AK.tsv_hozzaad(ut('batchek.tsv'), BATCH_FEJLEC, {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'batch_id': b['id'], 'cimke': cimke, 'kor': 1,
        'csomag': index + 1, 'kerelmek_db': len(kerelmek)})
    print('batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


def allapot(cimke, hivo=None):
    hivo = hivo or AK.http
    ki = []
    for b in batchek(cimke):
        r = hivo('GET', '/v1/messages/batches/%s' % b['batch_id'])
        print('%s kör=%s csomag=%s: %s %s' % (b['batch_id'], b['kor'], b['csomag'], r.get('processing_status'),
                                             json.dumps(r.get('request_counts'))))
        ki.append(r.get('processing_status'))
    return ki


# ---------- begyűjtés ----------

def begyujt(cimke, hivo=None):
    hivo = hivo or AK.http
    kesz = {s['custom_id'] for s in jsonl_olvas(ut('valaszok.jsonl'))}
    uj = 0
    for b in batchek(cimke):
        sorok = AK.eredmeny_sorok(b['batch_id'], hivo)
        if sorok is None:
            print('%s: még nem ért véget' % b['batch_id'])
            continue
        rekordok, napl = [], []
        for s in sorok:      # custom_id szerint, soha nem pozíció szerint
            cid = s['custom_id']
            if cid in kesz or not custom_id_bont(cid):
                continue
            res = s.get('result', {})
            msg = res.get('message') or {}
            usage = msg.get('usage', {})
            c = koltseg(usage)
            rekordok.append({'custom_id': cid, 'tipus': res.get('type'), 'modell': msg.get('model', ''),
                             'stop': msg.get('stop_reason'), 'usage': usage, 'szoveg': AK.uzenet_szoveg(msg),
                             'hiba': json.dumps(res.get('error'), ensure_ascii=False) if res.get('error') else '',
                             'batch_id': b['batch_id']})
            napl.append((cid, msg.get('model', ''), usage, msg.get('stop_reason') or res.get('type'), c))
            kesz.add(cid)
        jsonl_hozzaad(ut('valaszok.jsonl'), rekordok)
        futo = futo_osszeg()
        for cid, mod, u, stop, c in napl:
            futo += c
            AK.tsv_hozzaad(ut('futasnaplo.tsv'), NAPLO_FEJLEC, {
                'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'custom_id': cid, 'modell': mod,
                'effort': EFFORT, 'bemenet_token': u.get('input_tokens', 0), 'cache_olvasas': u.get('cache_read_input_tokens', 0),
                'cache_iras': u.get('cache_creation_input_tokens', 0), 'kimenet_token': u.get('output_tokens', 0),
                'stop_reason': stop, 'koltseg_usd': '%.6f' % c, 'futo_osszeg_usd': '%.6f' % futo})
        uj += len(rekordok)
        with open(ut('begyujtve_%s.txt' % b['batch_id']), 'w', encoding='utf-8', newline='\n') as f:
            f.write('%d\n' % len(rekordok))
        print('%s: %d új válasz' % (b['batch_id'], len(rekordok)))
    print('új válasz összesen: %d; futó összeg %.4f USD' % (uj, futo_osszeg()))
    return 0


# ---------- kapuzás ----------

def json_valasz(szoveg):
    """A modell JSON-válasza → (forditas_hu, [bizonytalan]) vagy (None, hibaüzenet)."""
    t = (szoveg or '').strip()
    t = re.sub(r'^```(?:json)?\s*|\s*```$', '', t)
    i = t.find('{')
    if i < 0:
        return None, 'a válasz nem JSON-objektum'
    try:
        d, _ = json.JSONDecoder().raw_decode(t[i:])
    except ValueError as e:
        return None, 'a válasz JSON-ja hibás (%s)' % str(e)[:80]
    fh = d.get('forditas_hu')
    if not isinstance(fh, str) or not fh.strip():
        return None, 'a `forditas_hu` mező hiányzik vagy üres'
    biz = d.get('bizonytalan_feloldasok') or []
    return fh.strip('\n'), [str(x) for x in biz if isinstance(x, str)]


def strong_allapot(strong, kerelmek, valaszok):
    """Egy Strong utolsó próbájának feldolgozása. -> dict {strong, proba, allapot, ...}"""
    sp = strong
    proba = 1
    cidek = {k['csoport']: custom_id(sp, k['csoport'], 1) for k in kerelmek}
    if all(custom_id(sp, k['csoport'], 2) in valaszok for k in kerelmek):
        proba = 2
        cidek = {k['csoport']: custom_id(sp, k['csoport'], 2) for k in kerelmek}
    if not all(c in valaszok for c in cidek.values()):
        return {'strong': sp, 'proba': proba, 'allapot': 'varakozik'}
    reszek, kivetel, nyers, hibak, modellek, stop_hibas = [], [], [], [], set(), False
    for k in kerelmek:
        v = valaszok[cidek[k['csoport']]]
        modellek.add(v['modell'])
        nyers.append(v['szoveg'])
        if v['tipus'] != 'succeeded' or v['stop'] in ('refusal', 'max_tokens'):
            hibak.append('a kérés nem adott használható választ (%s%s)' % (v['tipus'] if v['tipus'] != 'succeeded' else v['stop'],
                                                                           ': ' + v['hiba'][:120] if v['hiba'] else ''))
            stop_hibas = v['stop'] == 'refusal' or v['tipus'] != 'succeeded'
            continue
        fh, biz = json_valasz(v['szoveg'])
        if fh is None:
            hibak.append(biz)
            continue
        vissza, hiany, tobb = E.helyorzo_visszaallit(fh, k['hely'])
        if hiany or tobb:
            hibak.append('helyőrző-hiba: hiányzó %s, többször használt %s' % (hiany, tobb))
        reszek.append(vissza)
        kivetel.extend(x for x in biz if x not in kivetel)
    base = {'strong': sp, 'proba': proba, 'modellek': sorted(modellek), 'nyers': nyers, 'kivetel': kivetel}
    if hibak:
        return dict(base, allapot='kapuhiba' if stop_hibas else 'javitando', hibak=hibak, vegleges='', valtozasok=[])
    szoveg = ' '.join(reszek)
    if '\t' in szoveg or '\n' in szoveg:
        szoveg = re.sub(r'\s*[\t\n]+\s*', ' ', szoveg)
    if kerelmek[0]['mod'] == 'szakasz':
        vegleges, valt, eredm, ok = E.utofeldolgoz_szakasz(sp, szoveg, kivetel)
    else:
        vegleges, valt, eredm, ok = E.utofeldolgoz(sp, szoveg, kivetel)
    bukott = [(n, r) for n, e, r in eredm if e == 'SERTES']
    return dict(base, allapot='kesz' if ok else 'javitando', hibak=['%s: %s' % b for b in bukott], vegleges=vegleges,
                valtozasok=[list(v) for v in valt], kapu_bukott=[n for n, _ in bukott])


def kapuz(adag, strongok=None):
    ker = ker_index(adag, strongok)
    valaszok = {r['custom_id']: r for r in jsonl_olvas(ut('valaszok.jsonl'))}
    ki, szaml = [], {}
    for sp, ks in ker.items():
        r = strong_allapot(sp, ks, valaszok)
        szaml[r['allapot']] = szaml.get(r['allapot'], 0) + 1
        ki.append(r)
    os.makedirs(ut(), exist_ok=True)
    with open(ut('kapu_eredmeny.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for r in ki:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    p1 = [r for r in ki if r['proba'] == 1 and r['allapot'] not in ('varakozik',)]
    print('Strong: %d; %s' % (len(ki), ', '.join('%s %d' % kv for kv in sorted(szaml.items()))))
    print('1. próbán kapuhibás/javítandó: %d / %d feldolgozott' % (sum(1 for r in p1 if r['allapot'] != 'kesz'), len(p1)))
    return 0


# ---------- javító batch ----------

def javito_uzenet(hibak):
    return ('A fordításod a kapuellenőrzésen elbukott. A hibák:\n' + '\n'.join('- ' + h for h in hibak)
            + '\n\nJavítsd ki ezeket a forrás szerint, a fordítás többi részét változatlanul hagyva (a szakaszhatár-tokenek és a ⟦n⟧ '
              'helyőrzők változatlanul, pontosan egyszer, a forrás sorrendjében maradnak). Add vissza a teljes javított választ '
              'ugyanabban a JSON-formában; KIZÁRÓLAG a JSON-t.')


def javit(adag, cimke, hivo=None, strongok=None):
    hivo = hivo or AK.http
    elozo = [r for r in jsonl_olvas(ut('kapu_eredmeny.jsonl')) if r['allapot'] == 'javitando' and r['proba'] == 1]
    if not elozo:
        print('nincs javítandó Strong')
        return 0
    kesz = bekuldott_cidek()
    index = ker_index(adag, strongok)
    kerelmek, ker_meta = [], []
    for r in elozo:
        for k in index[r['strong']]:
            cid = custom_id(k['strong'], k['csoport'], 2)
            if cid in kesz:
                continue
            nyers = r['nyers'][k['csoport'] - 1] if k['csoport'] - 1 < len(r['nyers']) else ''
            msgs = [{'role': 'user', 'content': uzenet_tartalom(k['prompt'])},
                    {'role': 'assistant', 'content': nyers or '(üres válasz)'},
                    {'role': 'user', 'content': javito_uzenet(r['hibak'])}]
            kerelmek.append({'custom_id': cid, 'params': kerelem_params(msgs, k['forras_kar'])})
            ker_meta.append(k)
    if not kerelmek:
        print('a javító kérések már be vannak küldve')
        return 0
    becs = becsles(ker_meta)[3] * 1.3
    print('javító batch: %d kérés; költség-felső %.2f USD; eddig %.4f; plafon %.2f' % (len(kerelmek), becs, futo_osszeg(), PLAFON_USD))
    if futo_osszeg() + becs > PLAFON_USD:
        print('MEGÁLLÁS: a plafon fölött lenne', file=sys.stderr)
        return 3
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    with open(ut('csomag_javito.txt'), 'a', encoding='utf-8', newline='\n') as f:
        f.write(''.join(k['custom_id'] + '\n' for k in kerelmek))
    AK.tsv_hozzaad(ut('batchek.tsv'), BATCH_FEJLEC, {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'batch_id': b['id'], 'cimke': cimke, 'kor': 2,
        'csomag': 'javito', 'kerelmek_db': len(kerelmek)})
    print('javító batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


# ---------- rögzítés ----------

def felulir_lista(fajl):
    """strong\tkapu\tdontes — kézzel jóváhagyott kapu-felülbírálások (DT361 mintájára); fájl nélkül üres."""
    ki = {}
    if fajl and os.path.exists(fajl):
        for s in AK.tsv_olvas(fajl):
            ki[s['strong']] = (s['kapu'], s['dontes'])
    return ki


def modell_allapot(modellek):
    """Az `allapot` és a `modell` mező a tényleges API-válasz modellnevéből."""
    if len(modellek) != 1 or not list(modellek)[0]:
        raise SystemExit('a válaszokban nem egyetlen modellnév áll: %s' % modellek)
    mod = list(modellek)[0]
    if 'sonnet' in mod:
        return 'sonnet', mod
    if 'opus' in mod:
        return 'opus', mod
    raise SystemExit('ismeretlen modellnév: %s' % mod)


def hibas_sor(strong, r):
    kapu = ','.join(r.get('kapu_bukott') or ['api']) if r.get('kapu_bukott') else 'api'
    ok = ' | '.join(r['hibak'])[:600].replace('\t', ' ').replace('\n', ' ')
    return '\t'.join([strong, kapu, 'API Batch, 2. próba', ok])


def rogzit(adag, felulir_fajl=None, datum=None, szaraz_futas=False, strongok=None):
    index = ker_index(adag, strongok)
    eredm = [r for r in jsonl_olvas(ut('kapu_eredmeny.jsonl'))]
    felulir = felulir_lista(felulir_fajl)
    datum = datum or datetime.date.today().strftime('%Y.%m.%d')
    munka = list(E.tsv_dict_sorok(E.MUNKA_UT)) if os.path.exists(E.MUNKA_UT) else []
    _, term_verzio = E.terminologia_szoveg()
    beirando, szakasz_strongok, teljes_strongok, hibas, felulbiralt = [], [], [], [], []
    for r in eredm:
        sp = r['strong']
        if r['allapot'] == 'kesz' or (r['allapot'] == 'javitando' and sp in felulir):
            if r['allapot'] == 'javitando':
                kapu, dontes = felulir[sp]
                ks = index[sp]
                szoveg = ' '.join(E.helyorzo_visszaallit(json_valasz(n)[0], k['hely'])[0] for n, k in zip(r['nyers'], ks))
                if ks[0]['mod'] == 'szakasz':
                    vegl, valt, eredm_k, ok = E.utofeldolgoz_szakasz(sp, szoveg, r['kivetel'])
                else:
                    vegl, valt, eredm_k, ok = E.utofeldolgoz(sp, szoveg, r['kivetel'])
                felulir_megj = E.kapu_felulir(types.SimpleNamespace(kapu_felulir=kapu, dontes=dontes), eredm_k)
                r = dict(r, vegleges=vegl, valtozasok=[list(v) for v in valt])
                felulbiralt.append(sp)
            else:
                felulir_megj = ''
            allapot, mod = modell_allapot(r['modellek'])
            megj = '; '.join(x for x in ('API Batch (effort=%s, %d. próba)' % (EFFORT, r['proba']),
                                          ('terminológia-kivétel (bizonytalan_feloldasok): ' + ', '.join(r['kivetel'])) if r['kivetel'] else '',
                                          felulir_megj) if x)
            beirando.append((sp, r, allapot, mod, megj))
        elif r['allapot'] in ('kapuhiba',) or (r['allapot'] == 'javitando' and r['proba'] == 2):
            hibas.append((sp, r))
    # munkatábla: a Strong korábbi sorai kiesnek, az újak szakaszonként (mint a szakasz_rogzit)
    for sp, r, allapot, mod, megj in beirando:
        ks = index[sp]
        if ks[0]['mod'] == 'szakasz':
            szak = SB.szakaszok(sp)
            uj = E.szakasz_sorok(sp, szak, r['vegleges'], allapot, mod, datum, term_verzio, megj)
            szakasz_strongok.append(sp)
        else:
            forras = E.forras_szoveg(sp)[1]
            uj = [{'szotar': 'BDB', 'strong': sp, 'entry_id': E.strong_eredeti(sp), 'jelentes_szam': 'teljes',
                   'mezo': 'forditas_hu', 'forras_hash': E.forras_hash(forras), 'forditas_hu': r['vegleges'],
                   'allapot': allapot, 'modell': mod, 'datum': datum, 'terminologia_verzio': term_verzio, 'megjegyzes': megj}]
            teljes_strongok.append(sp)
        munka = [x for x in munka if not (x['szotar'] == 'BDB' and x['entry_id'] == E.strong_eredeti(sp))] + uj
        E.kisnagybetu_naplo(sp, [tuple(v) for v in r['valtozasok'] if v[0].startswith('5_kisnagybetu')])
    print('rögzítendő: %d Strong (szakaszos %d, teljes %d), ebből kapu-felülbírálással %d; hibás-listára: %d' % (
        len(beirando), len(szakasz_strongok), len(teljes_strongok), len(felulbiralt), len(hibas)))
    if szaraz_futas:
        return 0
    E.tsv_ir(E.MUNKA_UT, E.FORDITASOK_FEJLEC, munka,
             megjegyzes='F28 munkatabla (adat/forditasok.tsv semaja) -- jovahagyas elott; '
                        'irja: python eszkozok/emeles.py rogzit / szakasz_rogzit')
    for allapot_ertek in sorted({b[2] for b in beirando}):
        lista = [b[0] for b in beirando if b[2] == allapot_ertek]
        if szakasz_strongok:
            ssz = [s for s in lista if s in szakasz_strongok]
            if ssz:
                E.cmd_szakasz_beir(types.SimpleNamespace(
                    strongok=ssz, allapot=allapot_ertek, datum=datum, megjegyzes=None, regi_elavult=True,
                    kezi_felulir=False, kezi_marad=False))
        tl = [s for s in lista if s in teljes_strongok]
        if tl:
            E.cmd_beir(types.SimpleNamespace(strongok=tl, allapot=allapot_ertek, datum=datum, megjegyzes=None,
                                             jelentes_csere=False, kezi_felulir=False))
    if hibas:
        with open(HIBAS_UT, 'a', encoding='utf-8', newline='\n') as f:
            for sp, r in hibas:
                f.write(hibas_sor(sp, r) + '\n')
        print('hibás-listára: %s' % ', '.join(sp for sp, _ in hibas))
    return 0


# ---------- main ----------

def main(argv=None):
    global MUNKA
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('parancs', nargs='?', choices=['szaraz', 'bekuld', 'allapot', 'begyujt', 'kapuz', 'javit', 'rogzit'])
    ap.add_argument('--adag', type=int, default=None)
    ap.add_argument('--cimke', default=None)
    ap.add_argument('--felulir', default=None, help='strong<TAB>kapu<TAB>dontes TSV (kézzel jóváhagyott kapu-felülbírálások)')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        import teszt_bdb_api_koteg
        return teszt_bdb_api_koteg.futtat()
    if not a.parancs or not a.adag:
        print('HIBA: parancs és --adag kell', file=sys.stderr)
        return 2
    MUNKA = os.path.join(MUNKA_GYOKER, 'adag%d' % a.adag)
    cimke = a.cimke or 'adag%d' % a.adag
    kod = 1
    try:
        if a.parancs == 'szaraz':
            kod = szaraz(a.adag)
        elif a.parancs == 'bekuld':
            kod = bekuld(a.adag, cimke)
        elif a.parancs == 'allapot':
            allapot(cimke)
            kod = 0
        elif a.parancs == 'begyujt':
            kod = begyujt(cimke)
        elif a.parancs == 'kapuz':
            kod = kapuz(a.adag)
        elif a.parancs == 'javit':
            kod = javit(a.adag, cimke)
        else:
            kod = rogzit(a.adag, a.felulir)
    finally:
        pass
    return kod


if __name__ == '__main__':
    sys.exit(main())
