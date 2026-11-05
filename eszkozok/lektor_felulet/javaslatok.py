#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
javaslatok.py -- F165 (LAPJAVIT_ARTIFACT): a lapnézet `db`-jéből kiolvasott, jóváhagyott javaslatok feldolgozásának
segédje a `/lap-javit` artifact-módjához (`.claude/commands/lap-javit.md`, „Artifact-mód”).

A session az `ArtifactData` `list` (gyűjtemény: `javaslatok`) eredményét egy repón kívüli JSON-fájlba menti, és:

    python eszkozok/lektor_felulet/javaslatok.py kiolvas --be <tmp>/javaslatok.json --url <artifact-url> --kimenet <tmp>/jav

  -> `<tmp>/jav/csere.tsv`: a kézi rés alatti (próza-tippű) javaslatok cseréi (`forras	regi	uj`), ha a `regi` a
     forrásfájlban pontosan egyszer áll -- ez a `lap_javit_proba.py --csere` bemenete (előnézet, éles írás nélkül);
  -> `<tmp>/jav/naplo_tervezet.tsv`: minden `jóváhagyva` állapotú javaslat `lap_javitasok.tsv`-sor tervezete
     (SEMA 2.49). A `tipus` próza-tippnél `próza`, egyébként `?`: a session osztályoz (adat / forrás / generátor),
     és az `uj` mezőt adat- és generátor-sornál a jelölt-sor kulcsára / az N-tétel helyőrzőjére cseréli.

    python eszkozok/lektor_felulet/javaslatok.py hozzafuz <tmp>/jav/naplo_vegleges.tsv

  -> a véglegesített sorokat az `adat/lap_javitasok.tsv` végére fűzi: a meglévő sorok változatlanságát és az új sorokat
     az `ellenoriz.py` 30. szabályával (`lap_javitas_hibak`) ellenőrzi, kulcs-ütközésnél (`id`+`hely`+`datum`) megáll.

A szkript a forrást NEM írja: a próza beírása a session Edit-je a `/lap-javit` 3.a szerint. A `db` állapotát
(`beírva` / `külön út` / `elutasítva`) a session `ArtifactData` `update`-tel állítja. Olvasás `split('\\t')`,
írás `'\\t'.join()` (CLAUDE.md).
"""
import argparse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HELY))
sys.path.insert(0, os.path.dirname(HELY))
import ellenoriz as E  # noqa: E402

NAPLO = os.path.join(ROOT, 'adat', 'lap_javitasok.tsv')
FEJLEC = E.LAP_JAVITASOK_FEJLEC
KOTELEZO = ('motivum', 'hely', 'regi', 'uj', 'ok', 'gond', 'allapot', 'ts')


def _egysor(s):
    return ' '.join(str(s or '').replace('\t', ' ').split())


def dokumentumok(nyers):
    """Az `ArtifactData list` mentett eredménye -> [(doc_id, adat)]. Elfogadott alakok: lista {id, data} vagy
    {id, ...mezők} elemekkel; {"docs": [...]} / {"documents": [...]}; vagy {doc_id: adat} szótár."""
    if isinstance(nyers, dict):
        for k in ('docs', 'documents', 'items', 'results'):
            if isinstance(nyers.get(k), list):
                return dokumentumok(nyers[k])
        return [(k, v) for k, v in nyers.items() if isinstance(v, dict)]
    ki = []
    for d in nyers:
        if not isinstance(d, dict):
            raise ValueError('váratlan elem a javaslat-listában: %r' % (d,))
        doc_id = d.get('id') or d.get('doc_id') or str(d.get('path', '')).split('/')[-1]
        adat = d.get('data') if isinstance(d.get('data'), dict) else {k: v for k, v in d.items() if k not in ('id', 'doc_id', 'path')}
        if not doc_id:
            raise ValueError('azonosító nélküli javaslat: %r' % (d,))
        ki.append((doc_id, adat))
    return ki


def ellenoriz_doc(doc_id, d):
    hibak = ['hiányzó mező: %s' % k for k in KOTELEZO if not str(d.get(k, '')).strip()]
    if d.get('gond') and d['gond'] not in E.LAP_JAVITAS_GOND:
        hibak.append('gond=%r nem a zárt készletből' % d['gond'])
    if d.get('bekezdes') and d.get('regi') and d['bekezdes'].count(d['regi']) != 1:
        hibak.append('a régi szöveg nem pontosan egyszer áll a bekezdésben')
    return ['%s: %s' % (doc_id, h) for h in hibak]


def datum(ts):
    return str(ts)[:10].replace('-', '.')


def javasolta(d):
    j = _egysor(d.get('javasolta'))
    if not j or j.startswith('tier='):
        return 'claude (artifact, %s)' % (j or 'modell ismeretlen')
    return j


def naplo_sor(doc_id, d, url, tipus='?'):
    """A `lap_javitasok.tsv` sor tervezete (SEMA 2.49). `jovahagyta`: felhasználó -- a `javaslatok` gyűjteményt
    csak a lap tulajdonosa írhatja (`write: owner`), a sor tehát az ő kattintásából van."""
    hely = '%s („%s”)' % (_egysor(d['hely']), _egysor(d['regi'])[:48])
    return {'id': d['motivum'], 'hely': hely, 'tipus': tipus, 'gond': d['gond'], 'regi': _egysor(d['regi']),
            'uj': _egysor(d['uj']), 'javasolta': javasolta(d), 'jovahagyta': 'felhasználó', 'datum': datum(d['ts']),
            'proveniencia': 'scope=manual | forras=artifact:%s#javaslatok/%s | ts=%s' % (url, doc_id, str(d['ts'])[:10])}


def kiolvas(be, url, kimenet, root=ROOT):
    if os.path.abspath(kimenet).startswith(os.path.abspath(root) + os.sep):
        raise ValueError('a kimenet a repón kívülre menjen')
    with open(be, encoding='utf-8') as f:
        docs = dokumentumok(json.load(f))
    varo = [(i, d) for i, d in docs if d.get('allapot') == 'jóváhagyva']
    hibak = [h for i, d in varo for h in ellenoriz_doc(i, d)]
    if hibak:
        raise ValueError('hibás javaslat(ok):\n  ' + '\n  '.join(hibak))
    os.makedirs(kimenet, exist_ok=True)
    cserek, naplo, jelentes = [], [], []
    for doc_id, d in sorted(varo, key=lambda x: str(x[1].get('ts'))):
        forras = d.get('res') and d.get('forras_tipp') or ''
        tipus = 'próza' if forras else '?'
        megj = ''
        if forras:
            ut = os.path.join(root, forras)
            szoveg = ''
            if os.path.exists(ut):
                with open(ut, encoding='utf-8') as f:
                    szoveg = f.read()
            n = szoveg.count(d['regi'])
            if n == 1 and not any(c in d['regi'] + d['uj'] for c in '\t\n'):
                cserek.append([forras, d['regi'], d['uj']])
                megj = 'csere kész (%s)' % forras
            elif n == 1:
                megj = 'többsoros részlet (%s): a csere.tsv-be nem fér, kézzel kell helyre tenni' % forras
            else:
                megj = 'a régi szöveg %d-szer áll a forrásban (%s): kézzel kell helyre tenni' % (n, forras)
        else:
            megj = 'generált rész: a session osztályoz (adat / forrás / generátor)'
        naplo.append(naplo_sor(doc_id, d, url, tipus))
        jelentes.append('%s · %s · %s · %s → %s · %s' % (doc_id, d['hely'], d['gond'], _egysor(d['regi'])[:60],
                                                       _egysor(d['uj'])[:60], megj))
    for c in cserek:
        if any('\t' in x or '\n' in x for x in c):
            raise ValueError('tab vagy sortörés a cserében (%s): a csere.tsv egysoros mezőket vár' % c[0])
    with open(os.path.join(kimenet, 'csere.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(['\t'.join(['forras', 'regi', 'uj'])] + ['\t'.join(c) for c in cserek]) + '\n')
    with open(os.path.join(kimenet, 'naplo_tervezet.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(['\t'.join(FEJLEC)] + ['\t'.join(r[k] for k in FEJLEC) for r in naplo]) + '\n')
    return {'osszes': len(docs), 'varo': len(varo), 'csere': len(cserek), 'jelentes': jelentes}


def _beolvas_tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    if sorok and sorok[-1] == '':
        sorok.pop()
    return sorok


def hozzafuz(uj_ut, naplo=NAPLO, motivum_id_halmaz=None):
    """Az új sorok hozzáfűzése a naplóhoz: a meglévő sorok bájtra változatlanok maradnak, az új sorok a 30. szabály
    szerint hibátlanok, és a kulcs (`id`+`hely`+`datum`) nem ütközik."""
    regi = _beolvas_tsv(naplo)
    adat_regi = [s for s in regi if s and not s.startswith('#')]
    if adat_regi[0].split('\t') != FEJLEC:
        raise ValueError('a napló fejléce eltér a sémától')
    ujak = [s for s in _beolvas_tsv(uj_ut) if s.strip() and not s.startswith('#')]
    if ujak and ujak[0].split('\t') == FEJLEC:
        ujak = ujak[1:]
    if not ujak:
        raise ValueError('nincs hozzáfűzendő sor')
    rek = []
    for s in ujak:
        m = s.split('\t')
        if len(m) != len(FEJLEC):
            raise ValueError('%d mező a várt %d helyett: %s' % (len(m), len(FEJLEC), s[:80]))
        rek.append(dict(zip(FEJLEC, m)))
    if any(r['tipus'] == '?' for r in rek):
        raise ValueError('osztályozatlan sor (tipus=?): a session előbb mondja ki az osztályt')
    if motivum_id_halmaz is None:
        motivum_id_halmaz = {r['id'] for r in rek}
    hibak = E.lap_javitas_hibak(FEJLEC, rek, motivum_id_halmaz)
    if hibak:
        raise ValueError('a 30. szabály szerint hibás sor(ok):\n  ' + '\n  '.join(hibak))
    kulcsok = {tuple(s.split('\t')[i] for i in (0, 1, 8)) for s in adat_regi[1:]}
    for r in rek:
        k = (r['id'], r['hely'], r['datum'])
        if k in kulcsok:
            raise ValueError('kulcs-ütközés: %s / %s / %s' % k)
        kulcsok.add(k)
    uj_szoveg = '\n'.join(regi + ['\t'.join(r[k] for k in FEJLEC) for r in rek]) + '\n'
    if not uj_szoveg.startswith('\n'.join(regi)):
        raise ValueError('a meglévő sorok változnának: megállok')
    with open(naplo, 'w', encoding='utf-8', newline='\n') as f:
        f.write(uj_szoveg)
    return len(rek)


def main():
    ap = argparse.ArgumentParser(description='F165 -- a lapnézet jóváhagyott javaslatainak feldolgozása')
    al = ap.add_subparsers(dest='parancs', required=True)
    k = al.add_parser('kiolvas')
    k.add_argument('--be', required=True)
    k.add_argument('--url', required=True)
    k.add_argument('--kimenet', required=True)
    h = al.add_parser('hozzafuz')
    h.add_argument('sorok')
    a = ap.parse_args()
    if a.parancs == 'kiolvas':
        r = kiolvas(a.be, a.url, a.kimenet)
        print('  %d javaslat, %d a sessionre vár, %d csere kész' % (r['osszes'], r['varo'], r['csere']))
        for s in r['jelentes']:
            print('  - ' + s)
    else:
        motivumok = {s.split('\t')[0] for s in _beolvas_tsv(os.path.join(ROOT, 'adat', 'motivumok.tsv'))
                     if s and not s.startswith('#')}
        print('  %d sor hozzáfűzve: %s' % (hozzafuz(a.sorok, motivum_id_halmaz=motivumok), NAPLO))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
