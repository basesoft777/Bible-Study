#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.B — külső (nem Anthropic) vak bírálók a #172 mintáján, OpenRouter Batch API-n.

Ugyanaz a bemenet és utasítás, mint a vak Opus-ellenőré (#172): a
f172/ellenor/utasitas.md és a f172/ellenor/bemenet/koteg_NNN.txt (72 köteg, a
1600 mintapár és a régi arany céljai). A gépi pár és az Opus ítélete NEM kerül a
promptba. Egyetlen keretmondat tér el: az Opus fájlba írt, itt a válasz maga a
JSON (KERET).

A kimenet modellenként (rov: gemini | gpt):
  f172/kulso_biralo/<rov>/valasz/koteg_NNN.json  — a #172 válaszformája; a `modell`
      mező az API-válasz tényleges modellazonosítója (nem a modell önbevallása,
      az a `modell_onbevallas` mezőbe kerül);
  f172/kulso_biralo/<rov>/elvetett/              — a kapun elbukott válaszok;
  f172/kulso_biralo/batchek.tsv                  — beküldött batchek;
  f172/kulso_biralo/futasnaplo.tsv               — kérésenként tényleges modell,
      tokenek, költség (a batch-szintű OpenRouter-költség a batch sorában).

Műveletek:
  --bekuld --modell gemini --kotegek 1|mind|hianyzo [--plafon USD]
  --begyujt [--var PERC]      : a nyitott batchek lekérése (várakozással), kapu
  --vezerlo f172/kulso_biralo/futtatas.txt : a workflow belépési pontja
  --onteszt                   : hálózat nélkül (teszt_kulso_biralo.py)

Éles hívás csak GitHub Actionsből (a f22_c_futtat.py mintájára: GITHUB_ACTIONS).
Olvasás split('\\t'), írás '\\t'.join() (CLAUDE.md).
"""

import glob
import json
import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pontossag_ellenor as pe  # noqa: E402

GYOKER = pe.GYOKER
KI = os.path.join(GYOKER, 'f172', 'kulso_biralo')
BATCHEK = os.path.join(KI, 'batchek.tsv')
NAPLO = os.path.join(KI, 'futasnaplo.tsv')
API = 'https://openrouter.ai/api/v1'
# rov -> (OpenRouter-azonosító, batch-ár USD / 1M token: bemenet, kimenet; a /models listából, 2026-11-17)
MODELLEK = {
    'gemini': ('google/gemini-4-argon', 1.0, 5.0),
    'gpt': ('openai/gpt-6.1-sol', 1.0, 5.0),
}
CSALAD = {'gemini': 'gemini', 'gpt': 'gpt'}
TILTOTT = ('claude', 'opus', 'sonnet', 'haiku', 'anthropic')
MAX_TOKENS = 32000
KERET = ('Megjegyzés a kimenethez: a „megadott fájl” itt maga a válaszod. A válaszod egyetlen '
         'JSON-objektum legyen a fenti alakban, semmi más (se magyarázat, se kódblokk-jelölés).')
BATCH_FEJ = ['rov', 'modell_kert', 'batch_id', 'kotegek', 'bekuldve', 'allapot', 'provider',
             'prompt_tokens', 'completion_tokens', 'cost_usd']
NAPLO_FEJ = ['rov', 'batch_id', 'koteg', 'modell_kert', 'modell_valasz', 'modell_onbevallas', 'provider',
             'prompt_tokens', 'completion_tokens', 'reasoning_tokens', 'cost_usd', 'koltseg_forras',
             'eredmeny', 'megjegyzes', 'ts']
VEGALLAPOT = {'completed', 'failed', 'expired', 'cancelled'}


# --------------------------------------------------------------------- TSV
def _olvas(ut, fej):
    if not os.path.exists(ut):
        return []
    sorok = []
    with open(ut, encoding='utf-8') as f:
        for ln in f:
            ln = ln.rstrip('\n')
            if not ln or ln.startswith('#') or ln.split('\t') == fej:
                continue
            sorok.append(dict(zip(fej, ln.split('\t'))))
    return sorok


def _ir(ut, fej, sorok, scope):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=%s | forras=OpenRouter Batch API (/api/v1/batches) | ts=%s | '
                'manual (a modell-kimenet bírálat, nem arany)\n' % (scope, time.strftime('%Y-%m-%d')))
        f.write('\t'.join(fej) + '\n')
        for r in sorok:
            f.write('\t'.join(str(r.get(k, '')).replace('\t', ' ').replace('\n', ' ') for k in fej) + '\n')


# --------------------------------------------------------------------- prompt
def prompt(n):
    with open(os.path.join(pe.ELLENOR, 'utasitas.md'), encoding='utf-8') as f:
        ut = f.read().rstrip('\n')
    with open(os.path.join(pe.BEMENET_DIR, 'koteg_%03d.txt' % n), encoding='utf-8') as f:
        bem = f.read()
    return '%s\n\n%s\n\n%s' % (ut, KERET, bem)


def osszes_koteg():
    return sorted(pe._celtabla())


def batch_keres(rov, kotegek):
    """A POST /batches törzse. Az endpoint és a model a requests ELŐTT (az OpenRouter
    streamként olvassa a törzset)."""
    modell = MODELLEK[rov][0]
    req = [{'custom_id': 'koteg_%03d' % n,
            'body': {'messages': [{'role': 'user', 'content': prompt(n)}],
                     'response_format': {'type': 'json_object'},
                     'max_tokens': MAX_TOKENS, 'usage': {'include': True}}} for n in kotegek]
    return {'endpoint': '/v1/chat/completions', 'model': modell, 'requests': req}


def becsles(rov, kotegek):
    """Felső becslés (USD): bemenet ~ karakter/2,5 token, kimenet kötegenként 20 000 token."""
    _, pb, pk = MODELLEK[rov]
    be = sum(len(prompt(n)) / 2.5 for n in kotegek)
    return be / 1e6 * pb + len(kotegek) * 20000 / 1e6 * pk


# --------------------------------------------------------------------- válasz
def _tartalom_json(tartalom):
    t = (tartalom or '').strip()
    if t.startswith('```'):
        t = t.split('\n', 1)[1] if '\n' in t else ''
        if t.rstrip().endswith('```'):
            t = t.rstrip()[:-3]
    return json.loads(t)


def modell_ok_fn(rov):
    def ok(m):
        ml = m.lower()
        if not m or CSALAD[rov] not in ml or any(t in ml for t in TILTOTT):
            return 'modell: %r (%s kell, Anthropic-modell nem)' % (m, CSALAD[rov])
        return None
    return ok


def eredmeny_feldolgoz(rov, batch, celtabla=None):
    """Egy lezárt batch eredményei -> valasz/ (kapuval) vagy elvetett/; naplósorok."""
    celtabla = celtabla or pe._celtabla()
    vdir = os.path.join(KI, rov, 'valasz')
    edir = os.path.join(KI, rov, 'elvetett')
    os.makedirs(vdir, exist_ok=True)
    naplo = []
    ts = time.strftime('%Y-%m-%dT%H:%M:%S')
    for r in batch.get('results') or []:
        n = int(r['custom_id'].split('_')[1])
        sor = {'rov': rov, 'batch_id': batch['id'], 'koteg': n, 'modell_kert': MODELLEK[rov][0],
               'provider': batch.get('provider') or '', 'ts': ts}
        resp = r.get('response') or {}
        body = resp.get('body') or {}
        u = body.get('usage') or {}
        sor.update(prompt_tokens=u.get('prompt_tokens', ''), completion_tokens=u.get('completion_tokens', ''),
                   reasoning_tokens=(u.get('completion_tokens_details') or {}).get('reasoning_tokens', ''),
                   modell_valasz=body.get('model', ''))
        if u.get('cost') is not None:
            sor.update(cost_usd='%.6f' % u['cost'], koltseg_forras='openrouter')
        elif u.get('prompt_tokens') is not None:
            _, pb, pk = MODELLEK[rov]
            c = u.get('prompt_tokens', 0) / 1e6 * pb + (u.get('completion_tokens') or 0) / 1e6 * pk
            sor.update(cost_usd='%.6f' % c, koltseg_forras='ar_config')
        if r.get('error') or not body:
            sor.update(eredmeny='hiba', megjegyzes=str((r.get('error') or {}).get('message', 'nincs válasz'))[:200])
            naplo.append(sor)
            continue
        ch = (body.get('choices') or [{}])[0]
        try:
            d = _tartalom_json((ch.get('message') or {}).get('content'))
            if not isinstance(d, dict):
                raise ValueError('nem objektum')
        except (ValueError, IndexError) as ex:
            sor.update(eredmeny='rossz_json', megjegyzes='%s; finish_reason=%s' % (str(ex)[:120], ch.get('finish_reason')))
            os.makedirs(edir, exist_ok=True)
            with open(os.path.join(edir, 'koteg_%03d_%s.txt' % (n, batch['id'][-8:])), 'w', encoding='utf-8',
                      newline='\n') as f:
                f.write(str((ch.get('message') or {}).get('content')))
            naplo.append(sor)
            continue
        onb = str(d.get('modell', ''))
        meg = '' if d.get('koteg') == n else 'önbevallott köteg: %r' % d.get('koteg')
        ki = {'modell': body.get('model', ''), 'modell_onbevallas': onb, 'koteg': n,
              'versek': d.get('versek', [])}
        sor['modell_onbevallas'] = onb
        ut = os.path.join(vdir, 'koteg_%03d.json' % n)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(ki, f, ensure_ascii=False)
            f.write('\n')
        hib = pe.kapu(n, celtabla, valasz_dir=vdir, modell_ok=modell_ok_fn(rov))
        if hib:
            os.makedirs(edir, exist_ok=True)
            os.replace(ut, os.path.join(edir, 'koteg_%03d_%s.json' % (n, batch['id'][-8:])))
            meg = '; '.join([meg] + hib[:5]).strip('; ')
        sor.update(eredmeny='kapu_hiba' if hib else 'rendben', megjegyzes=meg[:300])
        naplo.append(sor)
    return naplo


def kesz_kotegek(rov):
    return sorted(int(os.path.basename(p)[6:9]) for p in glob.glob(os.path.join(KI, rov, 'valasz', 'koteg_*.json')))


def osszkoltseg(batchek=None):
    batchek = batchek if batchek is not None else _olvas(BATCHEK, BATCH_FEJ)
    return sum(float(b['cost_usd'] or 0) for b in batchek)


# --------------------------------------------------------------------- hálózat
def _http(modszer, ut, adat=None):
    import requests
    kulcs = os.environ.get('OPENROUTER_API_KEY')
    if not kulcs:
        raise SystemExit('HIBA: nincs OPENROUTER_API_KEY')
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise SystemExit('HIBA: éles API-hívás csak GitHub Actionsből (f22_c_futtat.py-minta)')
    h = {'Authorization': 'Bearer ' + kulcs, 'Content-Type': 'application/json'}
    for kiserlet in range(5):
        v = requests.request(modszer, API + ut, headers=h, data=json.dumps(adat) if adat is not None else None,
                             timeout=300)
        if v.status_code == 429 or v.status_code >= 500:
            time.sleep(30 * (kiserlet + 1))
            continue
        if v.status_code >= 400:
            raise SystemExit('HTTP %d: %s' % (v.status_code, v.text[:400]))
        return v.json()
    raise SystemExit('HTTP: 5 sikertelen kísérlet (%s %s)' % (modszer, ut))


def bekuld(rov, kotegek_arg, plafon, http=_http):
    if kotegek_arg == 'mind':
        kotegek = osszes_koteg()
    elif kotegek_arg == 'hianyzo':
        nyitott = {int(k) for b in _olvas(BATCHEK, BATCH_FEJ) if b['rov'] == rov and b['allapot'] not in VEGALLAPOT
                   for k in b['kotegek'].split(',')}
        kotegek = [n for n in osszes_koteg() if n not in set(kesz_kotegek(rov)) | nyitott]
    else:
        kotegek = [int(x) for x in kotegek_arg.split(',')]
    if not kotegek:
        print('%s: nincs beküldendő köteg' % rov)
        return None
    b = becsles(rov, kotegek)
    eddig = osszkoltseg()
    print('%s: %d köteg, becslés %.2f USD (eddig %.2f, plafon %.2f)' % (rov, len(kotegek), b, eddig, plafon))
    if eddig + b > plafon:
        raise SystemExit('PLAFON: %.2f + %.2f > %.2f USD' % (eddig, b, plafon))
    v = http('POST', '/batches', batch_keres(rov, kotegek))
    sorok = _olvas(BATCHEK, BATCH_FEJ)
    sorok.append({'rov': rov, 'modell_kert': MODELLEK[rov][0], 'batch_id': v['id'],
                  'kotegek': ','.join(map(str, kotegek)), 'bekuldve': time.strftime('%Y-%m-%dT%H:%M:%S'),
                  'allapot': v.get('status', ''), 'provider': v.get('provider') or ''})
    _ir(BATCHEK, BATCH_FEJ, sorok, 'F175.B beküldött batchek')
    print('%s: batch %s (%s)' % (rov, v['id'], v.get('status')))
    return v['id']


def begyujt(var_perc=0, http=_http):
    hatar = time.time() + var_perc * 60
    while True:
        sorok = _olvas(BATCHEK, BATCH_FEJ)
        naplo = _olvas(NAPLO, NAPLO_FEJ)
        nyitott = 0
        for b in sorok:
            if b['allapot'] in VEGALLAPOT:
                continue
            v = http('GET', '/batches/%s' % b['batch_id'])
            b['allapot'] = v.get('status', '')
            b['provider'] = v.get('provider') or b['provider']
            if b['allapot'] not in VEGALLAPOT:
                nyitott += 1
                rc = v.get('request_counts') or {}
                print('%s %s: %s (%s/%s)' % (b['rov'], b['batch_id'], b['allapot'], rc.get('completed'), rc.get('total')))
                continue
            u = v.get('usage') or {}
            b.update(prompt_tokens=u.get('prompt_tokens', ''), completion_tokens=u.get('completion_tokens', ''),
                     cost_usd='%.6f' % u['cost'] if u.get('cost') is not None else '')
            uj = eredmeny_feldolgoz(b['rov'], v)
            naplo.extend(uj)
            print('%s %s: %s; %s USD; %s' % (b['rov'], b['batch_id'], b['allapot'], b['cost_usd'],
                  ', '.join('%s=%d' % (e, sum(x['eredmeny'] == e for x in uj))
                            for e in ('rendben', 'kapu_hiba', 'rossz_json', 'hiba'))))
            if v.get('error'):
                print('  batch-hiba: %s' % v['error'])
        _ir(BATCHEK, BATCH_FEJ, sorok, 'F175.B beküldött batchek')
        _ir(NAPLO, NAPLO_FEJ, naplo, 'F175.B külső bírálók futásnaplója (kérésenként)')
        if not nyitott or time.time() >= hatar:
            print('nyitott batch: %d; összköltség: %.4f USD' % (nyitott, osszkoltseg(sorok)))
            return nyitott
        time.sleep(60)


def vezerlo(ut):
    k = {}
    with open(ut, encoding='utf-8') as f:
        for ln in f:
            ln = ln.strip()
            if ln and not ln.startswith('#') and '=' in ln:
                a, b = ln.split('=', 1)
                k[a.strip()] = b.strip()
    for kell in ('muvelet', 'modellek', 'kotegek', 'plafon_usd', 'var_perc'):
        if kell not in k:
            raise SystemExit('a vezérlőből hiányzik: %s' % kell)
    muv = k['muvelet'].split('+')
    if 'bekuld' in muv:
        for rov in k['modellek'].split(','):
            bekuld(rov.strip(), k['kotegek'], float(k['plafon_usd']))
    if 'begyujt' in muv:
        begyujt(int(k['var_perc']))
    for rov in MODELLEK:
        print('%s: kész kötegek %d/%d' % (rov, len(kesz_kotegek(rov)), len(osszes_koteg())))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--vezerlo')
    ap.add_argument('--bekuld', action='store_true')
    ap.add_argument('--modell', choices=sorted(MODELLEK))
    ap.add_argument('--kotegek', default='1')
    ap.add_argument('--plafon', type=float, default=5.0)
    ap.add_argument('--begyujt', action='store_true')
    ap.add_argument('--var', type=int, default=0)
    ap.add_argument('--becsles', action='store_true')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args()
    if a.onteszt:
        import subprocess
        raise SystemExit(subprocess.call([sys.executable, os.path.join(os.path.dirname(__file__),
                                                                       'teszt_kulso_biralo.py')]))
    if a.becsles:
        ks = osszes_koteg() if a.kotegek == 'mind' else [int(x) for x in a.kotegek.split(',')]
        for rov in MODELLEK:
            print('%s: %d köteg, felső becslés %.2f USD' % (rov, len(ks), becsles(rov, ks)))
    if a.vezerlo:
        vezerlo(a.vezerlo)
    if a.bekuld:
        bekuld(a.modell, a.kotegek, a.plafon)
    if a.begyujt:
        begyujt(a.var)


if __name__ == '__main__':
    main()
