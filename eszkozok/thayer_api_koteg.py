#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F158 — a Thayer szakaszonkénti fordításának Batch-kötegelője (Anthropic Message Batches API; DT-F27a).

A `bdb_api_koteg.py` Thayer-párja. A `thayer_jelolt/forditas.py` függvényeit hívja (prompt v5.1, adatblokk,
javítóréteg + 14–16. kapu, szakaszsorok, beírás), nem másolja; a REST-hívó, a kulcskezelés (`PARDES_API_KEY`), a
`tsv_olvas` / `tsv_hozzaad` az `eszkozok/karoli_strong/api_koteg.py`-ból, a tiszta segédek (költség, JSON-válasz,
javító üzenet, modellnév) a `bdb_api_koteg.py`-ból jönnek. A kulcs nem íródik ki, fájlba nem kerül.

Egység: Strong; a nagy szócikk csoportjai (`thayer_bemenet.csoportok`) külön kérések. `custom_id` = `<strong>-c<csoport>-p<próba>`.
A forrás a csoport `helyorzo_bont` ⟦n⟧ helyőrzőit kapja (a héber/görög szakaszok; csoportonként 1-től), a visszaállítás betűhű.

  lista     [--ki PATH] [--ts NAP]  a teljes Thayer futási listája (a `szolista.allapot` szabályával); repóba nem ír
  szaraz    --adag N --strongok FÁJL   a kérések összeállítása hálózat nélkül: kérés-, csoport-, karakterszám, becslés, csomagolás
  bekuld    a következő csomag beküldése — csak a megadott plafonnal (--plafon USD; alapérték 0 = tilos)
  allapot   a batch-ek állapota
  begyujt   a kész batch-ek nyers válaszai a valaszok.jsonl-be, költségnapló
  kapuz     válasz → JSON → helyőrző-visszaállítás → `forditas.utofeldolgoz` (javítóréteg + kapuk) → kapu_eredmeny.jsonl
  javit     a kapun bukott Strongok 2. batch-e (a kapu hibaüzenetével)
  rogzit    a kapun átment Strongok szakaszsorai a munkatáblába (`naplok/F132_THAYER_SZAKASZ_munka.tsv`); a kétszer
            bukottak a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be
  beir      STRONG… a munkatábla szakaszsorai az `adat/forditasok.tsv`-be (`forditas.beir`; --regi-elavult, --kezi-marad)
  --onteszt a hálózat nélküli öntesztek

Használat:
    python eszkozok/thayer_api_koteg.py lista --ki <repón kívül>/lista.tsv
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt --munka <repón kívül> szaraz
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt --plafon 20 bekuld
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt allapot|begyujt|kapuz|javit|rogzit
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt beir --regi-elavult --allapot sonnet

A `--strongok` fájl soronként egy Strong (G1941 vagy G1941a; üres és `#` sorok kimaradnak; egy sor első tabig számít).
Kilépési kódok: 0 rendben; 2 hibás paraméter/előfeltétel; 3 a plafon megállít; 4/5 az api_koteg.py szerint.
TSV: split('\\t'), '\\t'.join(); csv modul nincs.
"""

import argparse
import datetime
import json
import os
import re
import sys
import time

ITT = os.path.dirname(os.path.abspath(__file__))
THAYER_MAPPA = os.path.join(ITT, 'thayer_jelolt')
for _u in (os.path.join(ITT, 'karoli_strong'), ITT, THAYER_MAPPA):     # a THAYER_MAPPA elöl: kulcs, adatblokk, thayer_bemenet
    if _u not in sys.path:
        sys.path.insert(0, _u)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import api_koteg as AK  # noqa: E402
import emeles as E  # noqa: E402
import forditas as F  # noqa: E402
import kulcs  # noqa: E402
import szolista  # noqa: E402
import thayer_bemenet as TB  # noqa: E402
import bdb_api_koteg as B  # noqa: E402  (csak a tiszta segédei: költség, JSON-válasz, javító üzenet, modellnév)

ROOT = AK.tokenek.ROOT
MODELL = AK.MODELL                 # claude-sonnet-5-5 (a kérésben kért; a rögzítés a válasz tényleges modellnevét írja)
EFFORT = B.EFFORT
PLAFON_USD = 0.0                   # beküldés tilos, amíg a felhasználó plafonja (#27 ⛔ M1) nincs megadva (--plafon)
MUNKA_GYOKER = os.path.join(ROOT, 'forditas', 'thayer_api')
MUNKA_TABLA = F.MUNKA_UT
BUKOTT_UT = os.path.join(ROOT, 'naplok', 'F132_THAYER_SZAKASZ_bukottak.tsv')
BUKOTT_FEJLEC = ['strong', 'kapu', 'ok', 'probalkozas', 'modell', 'datum', 'proveniencia']
CSOMAG = 450                       # kérés / batch (a plafon csomagonként ellenőrződik)
TOKEN_KARAKTER = 2.8               # becslés (manual): prompt-karakter / token
KIMENET_ARANY = 0.5                # becslés (manual): kimeneti token / forráskarakter
GONDOLKODAS_BECSLES = 1500         # becslés (manual): gondolkodási token / kérés (effort=high)
AR_BE, AR_KI = B.AR_BE, B.AR_KI
NAPLO_FEJLEC = B.NAPLO_FEJLEC
BATCH_FEJLEC = B.BATCH_FEJLEC
CID = re.compile(r'^(?P<strong>G\d{4}[a-z]?)-c(?P<csoport>\d+)-p(?P<proba>\d)$')      # csak görög (Thayer)
FORRAS_JEL = 'Forrás (Thayer, angol):'
KIMENET_JEL = '## Kimenet'

MUNKA = MUNKA_GYOKER               # adagonként: MUNKA/adag<N>/ (a main() állítja; --munka felülírja)


# ---------- segédek ----------

def ut(*r):
    return os.path.join(MUNKA, *r)


custom_id = B.custom_id


def custom_id_bont(cid):
    m = CID.match(cid)
    return (m.group('strong'), int(m.group('csoport')), int(m.group('proba'))) if m else None


koltseg = B.koltseg
jsonl_olvas = B.jsonl_olvas
jsonl_hozzaad = B.jsonl_hozzaad
json_valasz = B.json_valasz
javito_uzenet = B.javito_uzenet
modell_allapot = B.modell_allapot
kerelem_params = B.kerelem_params
max_tokens_kerelemre = B.max_tokens_kerelemre


def futo_osszeg():
    return sum(float(s['koltseg_usd'] or 0) for s in AK.tsv_olvas(ut('futasnaplo.tsv')))


def strongok_olvas(fajl):
    """A futási lista Strongjai (Strong_padded), sorrendben, ismétlés nélkül; a thayer_szakaszok.tsv-ben szereplők."""
    ki, lattam = [], set()
    with open(fajl, encoding='utf-8') as f:
        for sor in f:
            s = sor.rstrip('\n').rstrip('\r').split('\t')[0].strip()
            if not s or s.startswith('#'):
                continue
            sp = kulcs.strong_pad(s)
            if not sp:
                raise SystemExit('hibás Strong a listában: %r' % s)
            if sp not in lattam:
                lattam.add(sp)
                ki.append(sp)
    return ki


# ---------- a futási lista ----------

def teljes_lista(ts):
    """Minden thayer_szakaszok.tsv-beli Strong a `szolista.allapot` szabályával (nem csak a motívumok gerincszavai)."""
    fs = szolista.thayer_sorok()
    ki = []
    for sp in sorted(TB.tabla_olvas()):
        szak = TB.szakaszok(sp)
        st, ok, megj = szolista.allapot(sp, szak, fs.get(sp, []))
        ki.append({'strong': sp, 'statusz': st, 'ok': ok, 'szakasz': str(len(szak)), 'karakter': str(len(TB.nezet(szak))),
                   'csoport': str(len(TB.csoportok(szak))), 'illesztes': szak[0]['illesztes'], 'motivumhely': '',
                   'megjegyzes': megj,
                   'proveniencia': 'scope=%s | forras=thayer_api_koteg.py lista (szolista.allapot) | ts=%s' % (sp, ts)})
    return ki


def lista_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/thayer_api_koteg.py lista --ts %s — a teljes Thayer futási listája (F158); kézzel nem szerkesztendő.' % ts,
           '# forras: adat/forditasok.tsv@%s + adat/thayer_szakaszok.tsv@%s' % (szolista.sha12(szolista.FORDITASOK_UT), szolista.sha12(TB.TABLA)),
           '\t'.join(szolista.FEJLEC)]
    return '\n'.join(fej + ['\t'.join(r[m] for m in szolista.FEJLEC) for r in sorok]) + '\n'


def lista_osszesito(sorok):
    import collections
    c = collections.Counter((r['statusz'], r['ok']) for r in sorok)
    return 'Strong %d; %s' % (len(sorok), ', '.join('%s/%s %d' % (s, o, n) for (s, o), n in sorted(c.items())))


def lista(ki=None, ts=None):
    ts = ts or datetime.date.today().isoformat()
    sorok = teljes_lista(ts)
    szoveg = lista_szoveg(sorok, ts)
    if ki:
        with open(ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s' % ki)
    else:
        sys.stdout.write(szoveg)
    print('# összesítő: %s' % lista_osszesito(sorok), file=sys.stderr)
    return 0


# ---------- a kérések ----------

def helyorzos_prompt(sp, csoport, darab_info):
    """A `forditas.prompt_epit` kimenete, a forrás-részben a `helyorzo_bont` ⟦n⟧ helyőrzőivel -> (prompt, hely, forras_kar)."""
    prompt = F.prompt_epit(sp, csoport, darab_info)
    tok = TB.tokenes(csoport)
    bont, hely = E.helyorzo_bont(tok)
    i = prompt.rfind(FORRAS_JEL)
    j = prompt.find(KIMENET_JEL, i)
    if i < 0 or j < 0 or prompt[i + len(FORRAS_JEL):j].strip('\n') != tok.strip('\n'):
        raise SystemExit('%s: a prompt forrás-része nem a várt helyen áll' % sp)
    return prompt[:i + len(FORRAS_JEL)] + '\n\n' + bont + '\n\n' + prompt[j:], hely, len(tok)


def kerelmek_strongra(strong):
    """[{strong, csoport, db, prompt, hely, forras_kar, kot}] csoportonként."""
    sp, szak = F.forras(strong)
    cs = TB.csoportok(szak)
    ki = []
    for i, c in enumerate(cs):
        prompt, hely, kar = helyorzos_prompt(sp, c, E.darab_info_szoveg(i, len(cs)))
        ki.append({'strong': sp, 'csoport': i + 1, 'db': len(cs), 'prompt': prompt, 'hely': hely, 'forras_kar': kar,
                   'kot': E.kotelezo_alakok_szoveg(TB.nezet(c))})
    return ki


def terv(strongok):
    """Az 1. próbás kérések, Strong-szám szerint (a lista sorrendje)."""
    return [k for s in strongok for k in kerelmek_strongra(s)]


def ker_index(strongok):
    ki = {}
    for k in terv(strongok):
        ki.setdefault(k['strong'], []).append(k)
    return ki


def becsles(ker):
    """(bemenet_token, kimenet_token, USD) — Batch-ár, cache nélkül; mind becslés (manual)."""
    be = sum(len(k['prompt']) / TOKEN_KARAKTER for k in ker)
    ki = sum(k['forras_kar'] * KIMENET_ARANY + GONDOLKODAS_BECSLES for k in ker)
    return be, ki, (be * AR_BE + ki * AR_KI) / 1e6


def csomagok(ker, meret=CSOMAG):
    return [ker[i:i + meret] for i in range(0, len(ker), meret)]


def uzenet(prompt):
    return [{'type': 'text', 'text': prompt}]


# ---------- szaraz ----------

def szaraz(strongok):
    t0 = time.time()
    ker = terv(strongok)
    kar = sum(k['forras_kar'] for k in ker)
    be, ki, usd = becsles(ker)
    csom = csomagok(ker)
    print('%d Strong, %d kérés (%d többcsoportos Strong), forrás %d karakter (tokenes bemenet)' % (
        len(strongok), len(ker), len({k['strong'] for k in ker if k['db'] > 1}), kar))
    print('promptok: összesen %d karakter, átlag %d' % (sum(len(k['prompt']) for k in ker), sum(len(k['prompt']) for k in ker) // max(1, len(ker))))
    print('becslés (manual; %.1f karakter/token, kimenet %.2f token/forráskarakter + %d gondolkodási token/kérés): '
          'bemenet %.0f token, kimenet %.0f token' % (TOKEN_KARAKTER, KIMENET_ARANY, GONDOLKODAS_BECSLES, be, ki))
    print('költség Batch-áron, cache nélkül: %.2f USD (becslés, manual); plafon %.2f USD' % (usd, PLAFON_USD))
    print('csomagok: %d × ~%d kérés' % (len(csom), CSOMAG))
    if ker:
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
                ki.update(x.strip() for x in h if x.strip())
    return ki


def ujra_naplo(batch_id, cimke, kor, csomag, db):
    AK.tsv_hozzaad(ut('batchek.tsv'), BATCH_FEJLEC, {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'batch_id': batch_id, 'cimke': cimke, 'kor': kor,
        'csomag': csomag, 'kerelmek_db': db})


def bekuld(strongok, cimke, plafon=None, hivo=None):
    plafon = PLAFON_USD if plafon is None else plafon
    if plafon <= 0:
        print('MEGÁLLÁS: a plafon %.2f USD — beküldés csak a felhasználó által megadott plafonnal (--plafon) lehetséges' % plafon,
              file=sys.stderr)
        return 3
    hivo = hivo or AK.http
    ker = terv(strongok)
    kesz = bekuldott_cidek()
    csom = csomagok(ker)
    index = next((i for i, c in enumerate(csom) if custom_id(c[0]['strong'], c[0]['csoport'], 1) not in kesz), None)
    if index is None:
        print('minden csomag beküldve')
        return 0
    cs = csom[index]
    becs = becsles(cs)[2]
    ossz = futo_osszeg() + becs
    print('csomag %d/%d: %d kérés; költség-felső (becslés, manual, cache nélkül): %.2f USD; eddig %.4f USD; plafon %.2f USD' % (
        index + 1, len(csom), len(cs), becs, futo_osszeg(), plafon))
    if ossz > plafon:
        print('MEGÁLLÁS: a becsült költség (%.2f USD) a plafon (%.2f USD) fölött lenne' % (ossz, plafon), file=sys.stderr)
        return 3
    kerelmek = [{'custom_id': custom_id(k['strong'], k['csoport'], 1),
                 'params': kerelem_params([{'role': 'user', 'content': uzenet(k['prompt'])}], k['forras_kar'])} for k in cs]
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    os.makedirs(ut(), exist_ok=True)
    with open(ut('csomag_%02d.txt' % (index + 1)), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(k['custom_id'] + '\n' for k in kerelmek))
    ujra_naplo(b['id'], cimke, 1, index + 1, len(kerelmek))
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
            rekordok.append({'custom_id': cid, 'tipus': res.get('type'), 'modell': msg.get('model', ''),
                             'stop': msg.get('stop_reason'), 'usage': usage, 'szoveg': AK.uzenet_szoveg(msg),
                             'hiba': json.dumps(res.get('error'), ensure_ascii=False) if res.get('error') else '',
                             'batch_id': b['batch_id']})
            napl.append((cid, msg.get('model', ''), usage, msg.get('stop_reason') or res.get('type'), koltseg(usage)))
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
        print('%s: %d új válasz' % (b['batch_id'], len(rekordok)))
    print('új válasz összesen: %d; futó összeg %.4f USD' % (uj, futo_osszeg()))
    return 0


# ---------- kapuzás ----------

def strong_allapot(sp, kerelmek, valaszok):
    """Egy Strong utolsó próbájának feldolgozása -> dict {strong, proba, allapot, ...} (a bdb_api_koteg szerint)."""
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
        ismeretlen = sorted({int(n) for n in E.HELYORZO.findall(fh) if not 1 <= int(n) <= len(k['hely'])})
        if ismeretlen:
            hibak.append('ismeretlen helyőrző: %s (a csoportban 1–%d van)' % (ismeretlen, len(k['hely'])))
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
    szak = TB.szakaszok(sp)
    try:
        vegleges, valt, eredm, ok = F.utofeldolgoz(sp, szak, szoveg, kivetel)
    except Exception as e:      # pl. a szakasztokenek hibája: javítandó, nem leállás
        return dict(base, allapot='javitando', hibak=['feldolgozási hiba: %s' % str(e)[:200]], vegleges='', valtozasok=[])
    bukott = [(n, r) for n, e, r in eredm if e == 'SERTES']
    return dict(base, allapot='kesz' if ok else 'javitando', hibak=['%s: %s' % b for b in bukott], vegleges=vegleges,
                valtozasok=[list(v) for v in valt], kapu_bukott=[n for n, _ in bukott])


def kapuz(strongok):
    ker = ker_index(strongok)
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
    p1 = [r for r in ki if r['proba'] == 1 and r['allapot'] != 'varakozik']
    print('Strong: %d; %s' % (len(ki), ', '.join('%s %d' % kv for kv in sorted(szaml.items()))))
    print('1. próbán kapuhibás/javítandó: %d / %d feldolgozott' % (sum(1 for r in p1 if r['allapot'] != 'kesz'), len(p1)))
    return 0


# ---------- javító batch ----------

def javit(strongok, cimke, plafon=None, hivo=None):
    plafon = PLAFON_USD if plafon is None else plafon
    hivo = hivo or AK.http
    elozo = [r for r in jsonl_olvas(ut('kapu_eredmeny.jsonl')) if r['allapot'] == 'javitando' and r['proba'] == 1]
    if not elozo:
        print('nincs javítandó Strong')
        return 0
    kesz = bekuldott_cidek()
    index = ker_index(strongok)
    kerelmek, ker_meta = [], []
    for r in elozo:
        for k in index[r['strong']]:
            cid = custom_id(k['strong'], k['csoport'], 2)
            if cid in kesz:
                continue
            nyers = r['nyers'][k['csoport'] - 1] if k['csoport'] - 1 < len(r['nyers']) else ''
            msgs = [{'role': 'user', 'content': uzenet(k['prompt'])},
                    {'role': 'assistant', 'content': nyers or '(üres válasz)'},
                    {'role': 'user', 'content': javito_uzenet(r['hibak'])}]
            kerelmek.append({'custom_id': cid, 'params': kerelem_params(msgs, k['forras_kar'])})
            ker_meta.append(k)
    if not kerelmek:
        print('a javító kérések már be vannak küldve')
        return 0
    becs = becsles(ker_meta)[2] * 1.3
    print('javító batch: %d kérés; költség-felső (becslés, manual) %.2f USD; eddig %.4f; plafon %.2f' % (len(kerelmek), becs, futo_osszeg(), plafon))
    if plafon <= 0 or futo_osszeg() + becs > plafon:
        print('MEGÁLLÁS: a plafon fölött lenne (vagy nincs megadva)', file=sys.stderr)
        return 3
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    with open(ut('csomag_javito.txt'), 'a', encoding='utf-8', newline='\n') as f:
        f.write(''.join(k['custom_id'] + '\n' for k in kerelmek))
    ujra_naplo(b['id'], cimke, 2, 'javito', len(kerelmek))
    print('javító batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


# ---------- rögzítés ----------

def bukott_sor(sp, r, modell, datum):
    kapu = ','.join(r.get('kapu_bukott') or []) or 'api'
    ok = ' | '.join(r['hibak'])[:600].replace('\t', ' ').replace('\n', ' ')
    return '\t'.join([sp, kapu, ok, 'API Batch, %d. próba' % r['proba'], modell, datum,
                      'scope=%s | forras=thayer_api_koteg.py rogzit | ts=%s' % (sp, datum)])


def rogzit(strongok, datum=None, szaraz_futas=False, munka_ut=None, bukott_ut=None):
    """A kapun átment Strongok szakaszsorai a munkatáblába (a többi sor bájtra azonos); a kétszer bukottak a bukottak.tsv-be."""
    munka_ut, bukott_ut = munka_ut or MUNKA_TABLA, bukott_ut or BUKOTT_UT
    index = ker_index(strongok)
    eredm = jsonl_olvas(ut('kapu_eredmeny.jsonl'))
    datum = datum or datetime.date.today().strftime('%Y.%m.%d')
    munka = list(E.tsv_dict_sorok(munka_ut)) if os.path.exists(munka_ut) else []
    _, term_verzio = E.terminologia_szoveg()
    rogzitett, bukottak = [], []
    for r in eredm:
        sp = r['strong']
        if r['allapot'] == 'kesz':
            allapot, mod = modell_allapot(r['modellek'])        # a válasz ténylegesen futott modellnevéből
            megj = '; '.join(x for x in ('API Batch (effort=%s, %d. próba)' % (EFFORT, r['proba']),
                                         ('terminológia-kivétel (bizonytalan_feloldasok): ' + ', '.join(r['kivetel'])) if r['kivetel'] else '') if x)
            szak = TB.szakaszok(sp)
            uj = F.szakasz_sorok(sp, szak, r['vegleges'], allapot, mod, datum, term_verzio, megj)
            munka = [x for x in munka if not (x['szotar'] == F.SZOTAR and x['strong'] == sp)] + uj
            E.kisnagybetu_naplo(sp, [tuple(v) for v in r['valtozasok'] if v[0].startswith('5_kisnagybetu')])
            rogzitett.append(sp)
        elif r['allapot'] == 'kapuhiba' or (r['allapot'] == 'javitando' and r['proba'] == 2):
            bukottak.append((sp, r))
    print('rögzítendő: %d Strong; bukott-listára: %d' % (len(rogzitett), len(bukottak)))
    if szaraz_futas:
        return 0
    if rogzitett:
        E.tsv_ir(munka_ut, F.FEJLEC, munka, megjegyzes='F132 munkatábla (adat/forditasok.tsv sémája) — beírás előtt; '
                                                      'írja: python eszkozok/thayer_api_koteg.py rogzit')
    if bukottak:
        uj_fajl = not os.path.exists(bukott_ut)
        with open(bukott_ut, 'a', encoding='utf-8', newline='\n') as f:
            if uj_fajl:
                f.write('\t'.join(BUKOTT_FEJLEC) + '\n')
            for sp, r in bukottak:
                f.write(bukott_sor(sp, r, ','.join(r.get('modellek') or []), datum) + '\n')
        print('bukott-listára: %s' % ', '.join(sp for sp, _ in bukottak))
    return 0


def beir(strongok, allapot, datum=None, megjegyzes=None, regi_elavult=False, kezi_felulir=False, kezi_marad=False, **kw):
    return F.beir(strongok, allapot, datum, megjegyzes, regi_elavult, kezi_felulir, kezi_marad, **kw)


# ---------- main ----------

def main(argv=None):
    global MUNKA, PLAFON_USD
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('parancs', nargs='?', choices=['lista', 'szaraz', 'bekuld', 'allapot', 'begyujt', 'kapuz', 'javit', 'rogzit', 'beir'])
    ap.add_argument('--adag', type=int, default=None)
    ap.add_argument('--strongok', default=None, help='a futási lista fájlja (soronként egy Strong)')
    ap.add_argument('--cimke', default=None)
    ap.add_argument('--munka', default=None, help='munkamappa (felülírja a forditas/thayer_api/adag<N>/-t; száraz futáshoz a repón kívül)')
    ap.add_argument('--plafon', type=float, default=0.0, help='USD; alapérték 0: a beküldés tilos')
    ap.add_argument('--ki', default=None)
    ap.add_argument('--ts', default=None)
    ap.add_argument('--allapot', default=None, choices=E.ALLAPOTOK)
    ap.add_argument('--datum', default=None)
    ap.add_argument('--megjegyzes', default=None)
    ap.add_argument('--regi-elavult', action='store_true')
    ap.add_argument('--kezi-felulir', action='store_true')
    ap.add_argument('--kezi-marad', action='store_true')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        import teszt_thayer_api_koteg
        return teszt_thayer_api_koteg.futtat()
    if not a.parancs:
        print('HIBA: parancs kell', file=sys.stderr)
        return 2
    if a.parancs == 'lista':
        return lista(a.ki, a.ts)
    if not a.adag or not a.strongok:
        print('HIBA: --adag és --strongok kell', file=sys.stderr)
        return 2
    MUNKA = a.munka or os.path.join(MUNKA_GYOKER, 'adag%d' % a.adag)
    PLAFON_USD = a.plafon
    cimke = a.cimke or 'adag%d' % a.adag
    strongok = strongok_olvas(a.strongok)
    if a.parancs == 'szaraz':
        return szaraz(strongok)
    if a.parancs == 'bekuld':
        return bekuld(strongok, cimke, a.plafon)
    if a.parancs == 'allapot':
        allapot(cimke)
        return 0
    if a.parancs == 'begyujt':
        return begyujt(cimke)
    if a.parancs == 'kapuz':
        return kapuz(strongok)
    if a.parancs == 'javit':
        return javit(strongok, cimke, a.plafon)
    if a.parancs == 'rogzit':
        return rogzit(strongok, a.datum)
    if not a.allapot:
        print('HIBA: beir --allapot kell', file=sys.stderr)
        return 2
    n = beir(strongok, a.allapot, a.datum, a.megjegyzes, a.regi_elavult, a.kezi_felulir, a.kezi_marad)
    print('adat/forditasok.tsv: %d sor változott/új (%d Strong)' % (n, len(strongok)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
