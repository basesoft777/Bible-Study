#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
keret_meres.py -- a heti keret fogyásának mérése sávonként a session-átiratokból (F222).

Forrás: a Claude Code session-átiratok (`~/.claude/projects/*/*.jsonl`, és a session-ek alatti `subagents/*.jsonl`).
Minden asszisztens-üzenetnek van `message.model` és `message.usage` mezője. A szkript:
  1. csak a keret-hét kezdete (szombat 14:00 UTC) óta keletkezett üzeneteket számolja, és ugyanazt az üzenetet
     (azonos `message.id`) csak egyszer (a session-elágaztatás a szülő üzeneteit másolja);
  2. az üzenetet súlyozza: modellenként és tokenfajtánként a nyilvános listaár (`adat/keret_sulyok.tsv`) szerint;
     az érték „ár-egyenérték” (USD a listaáron), amelynek csak az ARÁNYA számít;
  3. sávhoz rendeli (`adat/keret_munkamappa.tsv` kézi leképezés → a session címének előtagja → az ág briefjének `sav`
     mezője → ISMERETLEN; a gyökér-orkesztrátor az ORKESZTRACIO sorba kerül; ami nem rendelhető, az ISMERETLEN és
     nem vész el);
  4. a kalibrációs pontokból (`adat/heti_keret_meres.tsv`: időpont, heti %, Fable %) szorzót számol: az ár-egyenérték
     hány százalék. Mérési pont nélkül csak az arányokat adja, százalék nélkül.

A Fable a saját keretéből is fogy: az „összes” érték minden modellt tartalmaz (a közös heti keretet méri), a „Fable”
érték csak a Fable-üzeneteket (a Fable-keretet méri), külön összegként.

Pontosság: az ARÁNY megbízható (ugyanaz a súlyozás minden sávra), a SZÁZALÉK becslés: a keretet az Anthropic nem
a listaár szerint számolja, és a kalibrációs pontok kevesek. A nyers átiratot a szkript nem írja ki, csak az összesítést.

Használat:
    python eszkozok/keret_meres.py [--het ÉÉÉÉ-HH-NN] [--gyokerek <mappa> ...] [--gyoker <repó>] [--json <fájl>]
Kilépési kód: 0 = rendben, 2 = hiba.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime, time, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402

REPO = F.REPO
SULY_FEJ = ['modell', 'csalad', 'input', 'cache_5m', 'cache_1h', 'cache_olvasas', 'output', 'forras']
MUNKAMAPPA_FEJ = ['munkamappa', 'sav', 'megjegyzes']
MERES_FEJ = ['ts', 'heti_szazalek', 'fable_szazalek', 'forras']
TOKENFAJTAK = ('input', 'cache_5m', 'cache_1h', 'cache_olvasas', 'output')
CSALADOK = ('opus', 'sonnet', 'haiku', 'fable')
SAVOK = ('SYSTEMS', 'CONTENT', 'SERVER', 'USER', 'BUSINESS', 'DESIGN', 'FELMERES', 'ORKESZTRACIO')
ISMERETLEN = 'ISMERETLEN'
TS_MINTA = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$')
CIM_ELOTAG = re.compile(r'^\s*([A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű_]+)\s*[·:\-–—]')
CIM_SAV = {'SYSTEMS': 'SYSTEMS', 'CONTENT': 'CONTENT', 'SERVER': 'SERVER', 'USER': 'USER', 'BUSINESS': 'BUSINESS', 'DESIGN': 'DESIGN',
           'FELMÉRÉS': 'FELMERES', 'FELMERES': 'FELMERES', 'ORKESZTRÁTOR': 'ORKESZTRACIO', 'ORKESZTRATOR': 'ORKESZTRACIO'}
KERET_HATAR = time(14, 0)


# ---------------------------------------------------------------------------
# táblák (TSV: split('\t'), a csv modul nem használható)
# ---------------------------------------------------------------------------

def tsv_olvas(ut, fejlec):
    """(sorok, hibak): dict-sorok; a fejlécsor egyezését ellenőrzi."""
    nev = os.path.basename(ut)
    try:
        with open(ut, encoding='utf-8', newline='') as f:
            nyers = f.read().replace('\r\n', '\n').split('\n')
    except OSError as e:
        return [], ['%s: nem olvasható (%s)' % (nev, e)]
    if nyers and nyers[-1] == '':
        nyers.pop()
    if not nyers or nyers[0].lstrip('﻿').split('\t') != fejlec:
        return [], ['%s: a fejlécsor eltér a SEMA-tól (várt: %s)' % (nev, '|'.join(fejlec))]
    sorok, hibak = [], []
    for i, sor in enumerate(nyers[1:], start=2):
        if not sor.strip():
            continue
        mezok = sor.split('\t')
        if len(mezok) != len(fejlec):
            hibak.append('%s:%d: %d mező %d helyett' % (nev, i, len(mezok), len(fejlec)))
            continue
        d = dict(zip(fejlec, mezok))
        d['_sor'] = i
        sorok.append(d)
    return sorok, hibak


def _szam(szoveg):
    try:
        return float(szoveg)
    except ValueError:
        return None


def suly_ellenoriz(sorok):
    hibak = []
    for s in sorok:
        h = 'keret_sulyok.tsv:%d' % s['_sor']
        if s['csalad'] not in CSALADOK:
            hibak.append('%s: ismeretlen `csalad` (%s; kapott: %r)' % (h, ' | '.join(CSALADOK), s['csalad']))
        for t in TOKENFAJTAK:
            v = _szam(s[t])
            if v is None or v < 0:
                hibak.append('%s: a `%s` nem negatív szám kell (kapott: %r)' % (h, t, s[t]))
        if not s['forras'].strip():
            hibak.append('%s: üres `forras` (honnan van az ár, mikor)' % h)
    return hibak


def munkamappa_ellenoriz(sorok):
    hibak = []
    for s in sorok:
        if s['sav'] not in SAVOK:
            hibak.append('keret_munkamappa.tsv:%d: ismeretlen `sav` (%s; kapott: %r)' % (s['_sor'], ' | '.join(SAVOK), s['sav']))
        if not s['munkamappa'].strip():
            hibak.append('keret_munkamappa.tsv:%d: üres `munkamappa`' % s['_sor'])
    return hibak


def meres_ellenoriz(sorok):
    hibak = []
    for s in sorok:
        h = 'heti_keret_meres.tsv:%d' % s['_sor']
        if not TS_MINTA.match(s['ts']):
            hibak.append('%s: a `ts` alakja ÉÉÉÉ-HH-NNTÓÓ:PP, UTC (kapott: %r)' % (h, s['ts']))
        for k in ('heti_szazalek', 'fable_szazalek'):
            v = _szam(s[k])
            if v is None or not 0 <= v <= 100:
                hibak.append('%s: a `%s` 0–100 közötti szám kell (kapott: %r)' % (h, k, s[k]))
        if not s['forras'].strip():
            hibak.append('%s: üres `forras`' % h)
    return hibak


def tablak_olvas(gyoker):
    adat = os.path.join(gyoker, 'adat')
    suly, h1 = tsv_olvas(os.path.join(adat, 'keret_sulyok.tsv'), SULY_FEJ)
    mm, h2 = tsv_olvas(os.path.join(adat, 'keret_munkamappa.tsv'), MUNKAMAPPA_FEJ)
    pontok, h3 = tsv_olvas(os.path.join(adat, 'heti_keret_meres.tsv'), MERES_FEJ)
    hibak = h1 + h2 + h3 + suly_ellenoriz(suly) + munkamappa_ellenoriz(mm) + meres_ellenoriz(pontok)
    return suly, mm, pontok, hibak


# ---------------------------------------------------------------------------
# súlyozás
# ---------------------------------------------------------------------------

def modell_ar(modell, suly):
    """(sor, pontos): a modellnév leghosszabb egyező előtagú sora; ha nincs, a család neve szerinti legújabb (legelső) sor."""
    nev = (modell or '').lower().replace('.', '-')
    legjobb = None
    for s in suly:
        e = s['modell'].lower().replace('.', '-')
        if nev.startswith(e) and (legjobb is None or len(e) > len(legjobb['modell'])):
            legjobb = s
    if legjobb is not None:
        return legjobb, True
    for csalad in CSALADOK:
        if csalad in nev:
            for s in suly:
                if s['csalad'] == csalad:
                    return s, False
    return None, False


def tokenek(usage):
    """{tokenfajta: db} a `usage` mezőből; a gyorsítótár-írás 5 perces / 1 órás bontása, ha megvan."""
    u = usage or {}
    bontas = u.get('cache_creation') or {}
    c5 = bontas.get('ephemeral_5m_input_tokens')
    c1 = bontas.get('ephemeral_1h_input_tokens')
    if c5 is None and c1 is None:
        c5, c1 = u.get('cache_creation_input_tokens') or 0, 0
    return {'input': u.get('input_tokens') or 0, 'cache_5m': c5 or 0, 'cache_1h': c1 or 0,
            'cache_olvasas': u.get('cache_read_input_tokens') or 0, 'output': u.get('output_tokens') or 0}


def egyseg(usage, ar_sor):
    """Az üzenet ár-egyenértéke (USD a listaáron): a tokenfajtánkénti darabszám × ár / 1 000 000."""
    t = tokenek(usage)
    return sum(t[k] * float(ar_sor[k]) for k in TOKENFAJTAK) / 1e6


# ---------------------------------------------------------------------------
# átiratok beolvasása
# ---------------------------------------------------------------------------

def het_kezdet_ts(het):
    """A hét kezdete ISO-szövegként (`ÉÉÉÉ-HH-NNT14:00`), a `timestamp` mező előtagjához hasonlítható."""
    return '%sT%s' % (het.isoformat(), KERET_HATAR.strftime('%H:%M'))


def session_azonosito(ut):
    """A session azonosítója: a fő átirat fájlneve, vagy a `<session>/subagents/…` útvonal szülő-mappája."""
    ut = ut.replace('\\', '/')
    if '/subagents/' in ut:
        return ut.split('/subagents/')[0].rsplit('/', 1)[-1]
    return os.path.splitext(os.path.basename(ut))[0]


def atiratok(gyokerek, het):
    """A hét kezdete óta módosult átirat-fájlok (a régebbieknek nem lehet újabb üzenete)."""
    kezdet = datetime.strptime(het.isoformat(), '%Y-%m-%d') + timedelta(hours=14)
    korlat = kezdet.timestamp() - 3600
    kimenet = []
    for gy in gyokerek:
        for ut in glob.glob(os.path.join(gy, '**', '*.jsonl'), recursive=True):
            try:
                if os.path.getmtime(ut) >= korlat:
                    kimenet.append(ut)
            except OSError:
                continue
    return sorted(kimenet)


def beolvas(fajlok, het):
    """(uzenetek, meta): az üzenetek {azonosító: rekord} (deduplikálva), a session-metaadatok {session: dict}.

    Rekord: modell, usage, ts, session. Metaadat: cwd, ag, cim. A nyers sorokat nem őrzi meg."""
    kezdet = het_kezdet_ts(het)
    uzenetek, meta = {}, {}
    for ut in fajlok:
        sid = session_azonosito(ut)
        m = meta.setdefault(sid, {'cwd': None, 'ag': None, 'cim': None})
        try:
            f = open(ut, encoding='utf-8', errors='replace')
        except OSError:
            continue
        with f:
            for sor in f:
                if '"customTitle"' in sor and '"type":"custom-title"' in sor:
                    try:
                        m['cim'] = json.loads(sor).get('customTitle') or m['cim']
                    except ValueError:
                        pass
                    continue
                if '"type":"assistant"' not in sor:
                    continue
                try:
                    d = json.loads(sor)
                except ValueError:
                    continue
                msg = d.get('message') or {}
                usage = msg.get('usage')
                ts = d.get('timestamp') or ''
                if not usage or ts[:16] < kezdet or msg.get('model') in (None, '<synthetic>'):
                    continue
                if d.get('cwd') and not m['cwd']:
                    m['cwd'] = d['cwd']
                if d.get('gitBranch') and not m['ag']:
                    m['ag'] = d['gitBranch']
                kulcs = msg.get('id') or d.get('uuid')
                if not kulcs:
                    continue
                uj = {'modell': msg.get('model'), 'usage': usage, 'ts': ts, 'session': sid}
                regi = uzenetek.get(kulcs)
                # ugyanaz az üzenet több blokkra bontva is szerepelhet: a legteljesebb `usage` marad
                if regi is None or (sum(tokenek(usage).values()) > sum(tokenek(regi['usage']).values())):
                    uzenetek[kulcs] = uj
    return uzenetek, meta


# ---------------------------------------------------------------------------
# sávhoz rendelés
# ---------------------------------------------------------------------------

def ag_sav_terkep(briefek):
    """{ágnév: sav} a brief-fejlécekből (`ag` és `sav` mező), és {brief-szám: sav} az `F<nn>` ág-jelzéshez."""
    ag, szam = {}, {}
    for b in briefek:
        sav = (b.fej or {}).get('sav')
        if not sav:
            continue
        a = (b.fej.get('ag') or '').strip('"\'')
        if a:
            ag[a] = sav
        if b.szam is not None:
            szam[b.szam] = sav
    return ag, szam


def cim_sav(cim):
    m = CIM_ELOTAG.match(cim or '')
    if not m:
        return None
    return CIM_SAV.get(m.group(1).upper())


def hozzarendel(meta, munkamappak, ag_terkep):
    """(sav, honnan): a session sávja. Sorrend: kézi munkamappa-tábla → a cím előtagja → az ág briefjének `sav`-ja."""
    cwd = (meta.get('cwd') or '').replace('\\', '/')
    for s in munkamappak:
        if s['munkamappa'].replace('\\', '/').lower() in cwd.lower():
            return s['sav'], 'munkamappa-tábla'
    sav = cim_sav(meta.get('cim'))
    if sav:
        return sav, 'a session címe'
    ag = meta.get('ag') or ''
    ag_sav, szam_sav = ag_terkep
    if ag in ag_sav:
        return ag_sav[ag], 'az ág briefje'
    m = re.search(r'(?:^|/)f(\d+)(?:[-_.]|$)', ag)
    if m and int(m.group(1)) in szam_sav:
        return szam_sav[int(m.group(1))], 'az ág F-száma'
    return ISMERETLEN, 'nem rendelhető'


# ---------------------------------------------------------------------------
# összesítés és kalibrálás
# ---------------------------------------------------------------------------

def egysegek(uzenetek, suly):
    """{üzenet-kulcs: (egység, fable?, pontos?)}; az ismeretlen modell a család szerinti sort kapja, és megjelölt."""
    kimenet, ismeretlen = {}, {}
    for k, u in uzenetek.items():
        sor, pontos = modell_ar(u['modell'], suly)
        if sor is None:
            ismeretlen[u['modell']] = ismeretlen.get(u['modell'], 0) + 1
            continue
        if not pontos:
            ismeretlen[u['modell']] = ismeretlen.get(u['modell'], 0) + 1
        kimenet[k] = (egyseg(u['usage'], sor), sor['csalad'] == 'fable')
    return kimenet, ismeretlen


def kalibral(pontok, uzenetek, egys, het):
    """{'heti': szorzó|None, 'fable': szorzó|None, 'pontok': n}: a legkisebb négyzetek módszere az origón át.

    Egy pont: a `ts`-ig keletkezett üzenetek egysége (összes, illetve csak Fable) és a megadott százalék. A szorzó a
    százalék / egység. Nulla egységű (vagy 0%-os Fable) pont nem ad szorzót."""
    kezdet = het_kezdet_ts(het)
    veg = (datetime.strptime(het.isoformat(), '%Y-%m-%d') + timedelta(days=7, hours=14)).strftime('%Y-%m-%dT%H:%M')
    szamlalo = {'heti': 0.0, 'fable': 0.0}
    nevezo = {'heti': 0.0, 'fable': 0.0}
    n = 0
    for p in pontok:
        if not (kezdet <= p['ts'] < veg):
            continue
        n += 1
        osszes = sum(e for k, (e, _) in egys.items() if uzenetek[k]['ts'][:16] <= p['ts'])
        fable = sum(e for k, (e, f) in egys.items() if f and uzenetek[k]['ts'][:16] <= p['ts'])
        for kulcs, szazalek, u in (('heti', float(p['heti_szazalek']), osszes), ('fable', float(p['fable_szazalek']), fable)):
            if u > 0 and szazalek > 0:
                szamlalo[kulcs] += szazalek * u
                nevezo[kulcs] += u * u
    return {'heti': szamlalo['heti'] / nevezo['heti'] if nevezo['heti'] else None,
            'fable': szamlalo['fable'] / nevezo['fable'] if nevezo['fable'] else None, 'pontok': n}


def session_nev(sid, meta):
    m = meta.get(sid) or {}
    return m.get('cim') or m.get('ag') or sid[:8]


def osszesit(uzenetek, meta, suly, munkamappak, pontok, het, ag_terkep=None, top=3):
    """A mérés eredménye (a tesztelhető mag: nincs benne fájlolvasás)."""
    ag_terkep = ag_terkep or ({}, {})
    egys, ismeretlen_modell = egysegek(uzenetek, suly)
    sav_session = {}
    for sid, m in meta.items():
        sav_session[sid] = hozzarendel(m, munkamappak, ag_terkep)
    savok = OrderedDict((s, {'egyseg': 0.0, 'fable_egyseg': 0.0, 'uzenet': 0, 'session': {}}) for s in SAVOK + (ISMERETLEN,))
    session_egyseg = {}
    for k, (e, fable) in egys.items():
        sid = uzenetek[k]['session']
        sav = sav_session.get(sid, (ISMERETLEN, ''))[0]
        a = savok[sav]
        a['egyseg'] += e
        a['uzenet'] += 1
        if fable:
            a['fable_egyseg'] += e
        a['session'][sid] = a['session'].get(sid, 0.0) + e
        session_egyseg[sid] = session_egyseg.get(sid, 0.0) + e
    osszes = sum(a['egyseg'] for a in savok.values())
    fable_osszes = sum(a['fable_egyseg'] for a in savok.values())
    kal = kalibral(pontok, uzenetek, egys, het)
    for sav, a in savok.items():
        a['arany'] = a['egyseg'] / osszes if osszes else 0.0
        a['szazalek'] = a['egyseg'] * kal['heti'] if kal['heti'] is not None else None
        a['fable_szazalek'] = a['fable_egyseg'] * kal['fable'] if kal['fable'] is not None else None
        a['top'] = [(session_nev(sid, meta), e, sav_session[sid][1] if sid in sav_session else '')
                    for sid, e in sorted(a['session'].items(), key=lambda x: -x[1])[:top]]
    sessionok = [{'sid': sid, 'nev': session_nev(sid, meta), 'sav': sav_session.get(sid, (ISMERETLEN, ''))[0], 'egyseg': e}
                 for sid, e in sorted(session_egyseg.items(), key=lambda x: (-x[1], x[0]))]
    return {'het': het, 'sessionok': sessionok, 'savok': savok, 'osszes': osszes, 'fable_osszes': fable_osszes,
            'osszes_szazalek': osszes * kal['heti'] if kal['heti'] is not None else None,
            'fable_osszes_szazalek': fable_osszes * kal['fable'] if kal['fable'] is not None else None,
            'kalibralas': kal, 'uzenet_db': len(egys), 'session_db': len({uzenetek[k]['session'] for k in egys}),
            'ismeretlen_modell': ismeretlen_modell}


def meres(gyoker, het, gyokerek=None):
    """(eredmény, hibak): a teljes mérés; a táblák hibája esetén nincs eredmény."""
    suly, munkamappak, pontok, hibak = tablak_olvas(gyoker)
    if hibak:
        return None, hibak
    gyokerek = gyokerek or [os.path.join(os.path.expanduser('~'), '.claude', 'projects')]
    fajlok = atiratok(gyokerek, het)
    uzenetek, meta = beolvas(fajlok, het)
    ag_terkep = ag_sav_terkep(F.briefek_beolvas(gyoker))
    eredmeny = osszesit(uzenetek, meta, suly, munkamappak, pontok, het, ag_terkep)
    eredmeny['fajl_db'] = len(fajlok)
    return eredmeny, []


def szoveg(e):
    """Olvasható összesítő (a CLI kimenete)."""
    kal = e['kalibralas']
    sorok = ['hét: %s; %d üzenet, %d session, %d átirat-fájl' % (e['het'].isoformat(), e['uzenet_db'], e['session_db'], e.get('fajl_db', 0))]
    sorok.append('kalibrálás: %d pont; heti szorzó: %s; Fable szorzó: %s' % (
        kal['pontok'], 'nincs' if kal['heti'] is None else '%.4g %%/egység' % kal['heti'],
        'nincs' if kal['fable'] is None else '%.4g %%/egység' % kal['fable']))
    for sav, a in e['savok'].items():
        if not a['uzenet']:
            continue
        sz = '' if a['szazalek'] is None else ' ≈ %.1f%%' % a['szazalek']
        fz = '' if not a['fable_egyseg'] else ' (ebből Fable %.2f egység%s)' % (
            a['fable_egyseg'], '' if a['fable_szazalek'] is None else ' ≈ %.1f%%' % a['fable_szazalek'])
        sorok.append('%-13s arány %5.1f%%  %8.2f egység%s%s' % (sav, a['arany'] * 100, a['egyseg'], sz, fz))
        for nev, eg, honnan in a['top']:
            sorok.append('    - %s: %.2f egység (%s)' % (nev, eg, honnan))
    sorok.append('összesen: %.2f egység%s' % (e['osszes'], '' if e['osszes_szazalek'] is None else ' ≈ %.1f%%' % e['osszes_szazalek']))
    if e['ismeretlen_modell']:
        sorok.append('FIGYELEM: a listaárban nem szereplő modell (a család szerinti ár): %s' % e['ismeretlen_modell'])
    return '\n'.join(sorok)


def main(argv=None):
    ap = argparse.ArgumentParser(description='A heti keret fogyásának mérése sávonként a session-átiratokból.')
    ap.add_argument('--gyoker', default=REPO)
    ap.add_argument('--het', help='a hét kezdete (szombat, ÉÉÉÉ-HH-NN); alapértelmezés: a mostani hét')
    ap.add_argument('--gyokerek', nargs='*', help='az átiratok gyökérmappái (alap: ~/.claude/projects)')
    ap.add_argument('--json', help='az összesítés JSON-fájlba (a repón kívülre)')
    a = ap.parse_args(argv)
    if a.het:
        try:
            het = datetime.strptime(a.het, '%Y-%m-%d').date()
        except ValueError:
            print('HIBA: a --het alakja ÉÉÉÉ-HH-NN', file=sys.stderr)
            return 2
    else:
        import heti_beosztas as B
        het = B.het_kezdete(datetime.utcnow())
    e, hibak = meres(a.gyoker, het, a.gyokerek)
    if hibak:
        for h in hibak:
            print('HIBA: %s' % h, file=sys.stderr)
        return 2
    print(szoveg(e))
    if a.json:
        kiir = {'het': het.isoformat(), 'osszes': e['osszes'], 'kalibralas': e['kalibralas'],
                'savok': {s: {k: v for k, v in x.items() if k != 'session'} for s, x in e['savok'].items()}}
        with open(a.json, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(kiir, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
