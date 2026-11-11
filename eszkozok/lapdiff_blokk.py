#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/lapdiff_blokk.py -- F203 (N-F184a): a lexikonlap két változatának blokkszintű összevetése, a DT665 (b) gépi feltétele.

Az `adat/SEMA.md` 2.48 (DT554, DT665) szerint a lap átnézése a lap commitjához kötött; kivétel: a **gépi** szótári és Károli-KH
forrásadat-javítás nem érvényteleníti az átnézést, ha (a) a próza, a minősítés és a határ nem változik, (b) a lapdiff csak a
generált szótári/KH blokkokat érinti, és (c) a változást a kolofon vagy a jelentés felsorolja. Ez a modul a (b)-t méri: a lapot
blokkokra bontja, és megmondja, melyik blokk változott.

Blokk:
  * a generált blokk (`<!-- GENERÁLT-KEZDET: general.py --cel lexikon#<ID>#<név> … -->` … `<!-- GENERÁLT-VÉGE: … -->`): a neve
    a `<név>` (`szocikkek`, `kereszthivatkozasok`, `kolofon`, `elofordulasok`, …);
  * a generált blokkon kívüli szöveg (a kézi forrásból generált rések, a próza, a címsorok): `kivul:<az előző ## címsor>`
    (a lap eleje: `kivul:fej`).
A blokk tartalmát a futásonként változó mezőktől megtisztítva vetjük össze: a jelölősorok `ts=<nap>` mezője nem számít.

A DT665 (b) szerint megengedett blokkok (`DT665_BLOKKOK`): `szocikkek` (4. Szótári háttér), `kereszthivatkozasok` (6.
Kereszthivatkozások: a Károli-KH és a TSK) és `kolofon` (a (c) helye: a kolofon sorolja fel a változást). Minden más blokk
változása (a próza, a minősítés, a határ, az előfordulások, a tartalomjegyzék is) érvényteleníti az átnézést.

A (a) a (b)-ből következik a lap szintjén (a próza, a minősítés és a határ a `kivul:*`, a `dontesi_ut`, a `kizart` és az
`elofordulasok` blokkban áll); a (c) a kolofon vagy a jelentés szövege — a kapu a kolofon változását jelzi, a jelentést nem
olvassa (a reszletben áll).

    python eszkozok/lapdiff_blokk.py --id HAMART-001 --tol <commit> [--ig <commit>]

Olvasás git show-val; a TSV-szabály itt nem érintett (Markdown).
"""
import collections
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DT665_BLOKKOK = frozenset({'szocikkek', 'kereszthivatkozasok', 'kolofon'})
KEZDET = re.compile(r'^<!-- GENERÁLT-KEZDET: \S+ --cel lexikon#[^#\s]+#(\S+?)(?:\s|\|)')
VEGE = re.compile(r'^<!-- GENERÁLT-VÉGE: ')
CIMSOR = re.compile(r'^## (.+?)\s*$')
TS = re.compile(r'\bts=\S+')


def _normal(sor):
    """A jelölősor futásonként változó `ts=` mezője nélkül; a sorvégi szóköz és a CR nem számít."""
    sor = sor.rstrip('\r').rstrip()
    return TS.sub('ts=', sor) if sor.startswith('<!--') else sor


def blokkok(szoveg):
    """-> OrderedDict: blokknév -> a blokk normalizált sorai (lista). A generált blokk neve a jelölő `#<név>` része, a kívüli
    szövegé `kivul:<az előző ## címsor>`; egy név többször is előfordulhat — ekkor a sorok összefűződnek."""
    ki = collections.OrderedDict()
    aktiv, kivul = None, 'kivul:fej'
    for sor in (szoveg or '').split('\n'):
        if aktiv is None:
            m = KEZDET.match(sor)
            if m:
                aktiv = m.group(1)
                ki.setdefault(aktiv, []).append(_normal(sor))
                continue
            c = CIMSOR.match(sor)
            if c:
                kivul = 'kivul:' + c.group(1)
            ki.setdefault(kivul, []).append(_normal(sor))
        else:
            ki[aktiv].append(_normal(sor))
            if VEGE.match(sor):
                aktiv = None
    return ki


def valtozott_blokkok(regi, uj):
    """A két lapszöveg között megváltozott (vagy csak az egyikben álló) blokkok nevei, a lap sorrendjében."""
    a, b = blokkok(regi), blokkok(uj)
    nevek = list(b) + [n for n in a if n not in b]
    return [n for n in nevek if a.get(n) != b.get(n)]


def dt665_b(regi, uj, megengedett=DT665_BLOKKOK):
    """-> (teljesül, változott blokkok, nem megengedett blokkok). Teljesül, ha minden változott blokk megengedett (a csak `ts=`-ben
    eltérő lap is: a tartalma azonos)."""
    v = valtozott_blokkok(regi, uj)
    tilos = [n for n in v if n not in megengedett]
    return not tilos, v, tilos


def lap_valtozat(motivum, commit, gyoker=GYOKER):
    """A `lexikon/<ID>_TUDOMANYOS.md` a `commit`-ban; None, ha nem olvasható (pl. sekély klón, nincs ilyen commit)."""
    o = subprocess.run(['git', 'show', '%s:lexikon/%s_TUDOMANYOS.md' % (commit, motivum)], cwd=gyoker, capture_output=True)
    return o.stdout.decode('utf-8') if o.returncode == 0 else None


def os_e(regi_commit, uj_commit, gyoker=GYOKER):
    """Igaz, ha a `regi_commit` az `uj_commit` őse (vagy azonos vele)."""
    return subprocess.run(['git', 'merge-base', '--is-ancestor', regi_commit, uj_commit], cwd=gyoker,
                          capture_output=True).returncode == 0


def atnezes_dt665(motivum, atnezett_commit, lap_commit, gyoker=GYOKER):
    """Az átnézett lapváltozatról a mai lapváltozatra a DT665 (b) feltétele. -> dict: `ervenyes` (bool), `valtozott`, `tilos`,
    `kolofon` (a kolofon változott-e: a (c) jele), `ok` (szöveg)."""
    if not os_e(atnezett_commit, lap_commit, gyoker):
        return {'ervenyes': False, 'valtozott': [], 'tilos': [], 'kolofon': False,
                'ok': 'az átnézett változat (%s) nem őse a mai lapnak' % atnezett_commit[:12]}
    regi, uj = lap_valtozat(motivum, atnezett_commit, gyoker), lap_valtozat(motivum, lap_commit, gyoker)
    if regi is None or uj is None:
        return {'ervenyes': False, 'valtozott': [], 'tilos': [], 'kolofon': False, 'ok': 'a lapváltozat nem olvasható'}
    ok, v, tilos = dt665_b(regi, uj)
    return {'ervenyes': ok, 'valtozott': v, 'tilos': tilos, 'kolofon': 'kolofon' in v,
            'ok': (('csak generált szótári/KH blokk változott: %s' % ', '.join(v)) if v else 'a tartalom azonos (csak a ts= változott)')
                  if ok else 'nem szótári/KH blokk is változott: %s' % ', '.join(tilos)}


def main():
    a = sys.argv[1:]

    def opt(nev, alap=None):
        return a[a.index(nev) + 1] if nev in a else alap
    mid, tol = opt('--id'), opt('--tol')
    if not mid or not tol:
        raise SystemExit('hasznalat: lapdiff_blokk.py --id <ID> --tol <commit> [--ig <commit>]')
    ig = opt('--ig', 'HEAD')
    regi, uj = lap_valtozat(mid, tol), lap_valtozat(mid, ig)
    if regi is None or uj is None:
        raise SystemExit('a lap nem olvasható (%s / %s)' % (tol, ig))
    ok, v, tilos = dt665_b(regi, uj)
    print('%s %s..%s: változott blokk %d: %s' % (mid, tol[:12], ig[:12], len(v), ', '.join(v) or '—'))
    print('DT665 (b): %s%s' % ('teljesül' if ok else 'NEM teljesül', (' — nem megengedett: %s' % ', '.join(tilos)) if tilos else ''))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
