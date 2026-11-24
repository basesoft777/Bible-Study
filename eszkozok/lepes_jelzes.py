#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lepes_jelzes.py -- F0.33 (DT952): a szerkesztő 2026-11-24-i munkarendjének gépi jelzése. Csak jelzés, nem bukás.

Munkarend: minden kész lépés saját kis PR-ként megy a main-be; a menet közben talált hiba külön tétel (a pár soros
javítás kivétel). Két jelzés őrzi, mindkettő PR-komment, egyszer (a komment frissül, nem szaporodik):

  1. `pr`    -- több lépéses PR: a PR commit-üzenetei egynél több lépés tételazonosítóját hordják ugyanabból a
               feladatból (pl. `F241.4:` és `F241.5:`, vagy `F240.L1` és `F240.L7`).
  2. `allo` -- álló draft: egy draft PR két napnál régebben nyitott, és a feladatának egyetlen lépése sem került a
               main-be (napi ütemezett Action).

A lépés a tételazonosító első alpontja (`F241.4` -> `4`; `F240.L7` -> `L7`). Szűkítések (a mérés indoka: `naplok/`
nincs; a mérés a PR leírásában áll):
  * `F0.<n>` (gépi/apró tételek), a `FELADATOK.md frissítés (gép)`, a `szamkiosztas` és a merge-commitok nem számítanak;
  * a `.0` lépés a brief befogadása (minden PR-nak van), nem számít lépésnek;
  * a számmal kezdődő alpont betűs utótagja (`5b`) a számhoz tartozik: az `F241.5` és az `F241.5b` egy lépés.

Használat:
    python eszkozok/lepes_jelzes.py pr --uzenetek commit_uzenetek.txt      # CI: PR-komment, ha több lépés van
    python eszkozok/lepes_jelzes.py pr --alap origin/main --fej HEAD       # helyi mérés (nem ír kommentet)
    python eszkozok/lepes_jelzes.py allo                                   # CI (napi): a két napnál régebbi, álló draftok
    python eszkozok/lepes_jelzes.py allo --proba                           # helyi mérés (GITHUB_TOKEN, GITHUB_REPOSITORY kell; nem ír)
Kilépési kód: mindig 0 (jelzés); 2 = hibás használat.
Környezet (CI): GITHUB_TOKEN, GITHUB_REPOSITORY, PR_SZAM (a `pr` módhoz).
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARKER_LEPES = '<!-- lepes-jelzes -->'
MARKER_ALLO = '<!-- allo-draft-jelzes -->'
ALLO_NAP = 2

# `F241.4: ...`, `F240.L7 — ...`, `F218a.S8c: ...`; a feladat az `F<szám>[kisbetű]`, az alpont az első `.` utáni szó.
TETEL = re.compile(r'^(F\d+[a-z]?)\.([A-Za-z0-9]+)(?![A-Za-z0-9])')
SZAMOS = re.compile(r'^(\d+)[a-z]*$')


def lepes_kulcs(alpont):
    """Az első alpont lépés-azonosítója: `5b` -> `5`, `L7` -> `L7`."""
    m = SZAMOS.match(alpont)
    return m.group(1) if m else alpont


def tetelek(uzenetek):
    """Az üzenetek (sorok; csak az első sor, a tárgy számít) lépései feladatonként: {feladat: [lépés, ...]}, első előfordulás sorrendjében.
    A `.0`, az `F0` és a nem tételazonosítós tárgyak kimaradnak."""
    feladatok = {}
    for sor in uzenetek:
        m = TETEL.match(sor.strip())
        if not m:
            continue
        feladat, alpont = m.group(1), m.group(2)
        if feladat == 'F0':
            continue
        kulcs = lepes_kulcs(alpont)
        if kulcs == '0':
            continue
        lista = feladatok.setdefault(feladat, [])
        if kulcs not in lista:
            lista.append(kulcs)
    return feladatok


def tobb_lepes(uzenetek):
    """{feladat: [lépések]} azokra a feladatokra, amelyeknek egynél több lépése van."""
    return {f: l for f, l in tetelek(uzenetek).items() if len(l) > 1}


def lepes_szoveg(tobb):
    sorok = [MARKER_LEPES, '',
             '**Több lépéses PR (jelzés, nem bukás).** A munkarend: minden kész lépés saját kis PR, '
             'a menet közben talált hiba külön tétel (a pár soros javítás kivétel).', '']
    for feladat, lepesek in sorted(tobb.items()):
        sorok.append('- `%s`: %d lépés (%s)' % (feladat, len(lepesek), ', '.join('`.%s`' % l for l in lepesek)))
    sorok += ['', 'Ha ez a PR tényleg egy lépés (pl. egy lépés több commitja), nincs teendő; különben a kész lépéseket '
              'érdemes külön PR-ként a main-be vinni.']
    return '\n'.join(sorok)


def allo_szoveg(nap):
    return '\n'.join([MARKER_ALLO, '',
                      '**Álló draft (jelzés, nem bukás).** A PR %d napja nyitott, és a feladatának egyetlen lépése sem került '
                      'a main-be. A munkarend: minden kész lépés saját kis PR-ként rögtön a main-be megy; ha van kész lépés, '
                      'érdemes külön PR-ba vinni, ha nincs, az Állapot sorban (PR első sora) álljon az akadály.' % nap])


# --- GitHub REST (csak a standard library) ----------------------------------------------------------------------

def _kerds(url, token, method='GET', adat=None):
    fejlecek = {'Authorization': 'Bearer %s' % token, 'Accept': 'application/vnd.github+json',
                'User-Agent': 'bible-study-lepes-jelzes'}
    torzs = json.dumps(adat).encode('utf-8') if adat is not None else None
    req = urllib.request.Request(url, data=torzs, headers=fejlecek, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))


def komment_ir(repo, pr_szam, token, marker, szoveg):
    """Egy komment PR-onként: ha van már a markerrel, frissíti (a szöveg változatlansága esetén nem ír), különben újat ír."""
    api = 'https://api.github.com/repos/%s' % repo
    kommentek = _kerds('%s/issues/%s/comments?per_page=100' % (api, pr_szam), token)
    meglevo = next((k for k in kommentek if marker in (k.get('body') or '')), None)
    if meglevo:
        if (meglevo.get('body') or '').strip() == szoveg.strip():
            return 'változatlan'
        _kerds('%s/issues/comments/%s' % (api, meglevo['id']), token, 'PATCH', {'body': szoveg})
        return 'frissítve'
    _kerds('%s/issues/%s/comments' % (api, pr_szam), token, 'POST', {'body': szoveg})
    return 'megírva'


def van_komment(repo, pr_szam, token, marker):
    api = 'https://api.github.com/repos/%s' % repo
    kommentek = _kerds('%s/issues/%s/comments?per_page=100' % (api, pr_szam), token)
    return any(marker in (k.get('body') or '') for k in kommentek)


# --- git ---------------------------------------------------------------------------------------------------------

def git(*args):
    r = subprocess.run(['git'] + list(args), cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(args), r.stderr.strip()))
    return r.stdout


def targyak(alap, fej):
    return [s for s in git('log', '--no-merges', '--format=%s', '%s..%s' % (alap, fej)).splitlines() if s.strip()]


# --- módok -------------------------------------------------------------------------------------------------------

def mod_pr(args):
    if args.uzenetek:
        with open(args.uzenetek, encoding='utf-8') as f:
            # a fájl commitonként egy sort (a tárgyat) tartalmaz: `git log --no-merges --format=%s`
            uzenetek = f.read().splitlines()
    else:
        uzenetek = targyak(args.alap, args.fej)
    tobb = tobb_lepes(uzenetek)
    if not tobb:
        print('Egy lépés (vagy nincs tételazonosító): nincs jelzés.')
        szoveg = None
    else:
        szoveg = lepes_szoveg(tobb)
        print(szoveg)
    token, repo, pr_szam = (os.environ.get(k) for k in ('GITHUB_TOKEN', 'GITHUB_REPOSITORY', 'PR_SZAM'))
    if not (token and repo and pr_szam):
        return 0
    if szoveg is None:
        # a korábbi jelzés megszűnt (pl. a lépések külön PR-ba kerültek): a meglévő komment frissül, újat nem írunk
        api = 'https://api.github.com/repos/%s' % repo
        meglevo = next((k for k in _kerds('%s/issues/%s/comments?per_page=100' % (api, pr_szam), token)
                        if MARKER_LEPES in (k.get('body') or '')), None)
        if meglevo:
            _kerds('%s/issues/comments/%s' % (api, meglevo['id']), token, 'PATCH',
                   {'body': MARKER_LEPES + '\n\nA jelzés megszűnt: a PR már egy lépés.'})
        return 0
    print('PR-komment: ' + komment_ir(repo, pr_szam, token, MARKER_LEPES, szoveg))
    return 0


def feladat_a_mainben(feladat, main='origin/main'):
    """Van-e a main-en olyan commit, amelynek tárgya ezzel a feladat-előtaggal kezdődik (`F241.`)."""
    ki = git('log', main, '--no-merges', '-E', '--grep=^%s\\.' % re.escape(feladat), '-n', '1', '--format=%H')
    return bool(ki.strip())


def mod_allo(args):
    token, repo = os.environ.get('GITHUB_TOKEN'), os.environ.get('GITHUB_REPOSITORY')
    if not (token and repo):
        print('Nincs GITHUB_TOKEN/GITHUB_REPOSITORY: nem fut.', file=sys.stderr)
        return 2
    api = 'https://api.github.com/repos/%s' % repo
    ma = datetime.datetime.now(datetime.timezone.utc)
    jelzett = 0
    for pr in _kerds('%s/pulls?state=open&per_page=100' % api, token):
        if not pr.get('draft'):
            continue
        nyitva = datetime.datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
        nap = (ma - nyitva).days
        if nap < ALLO_NAP:
            continue
        commitok = _kerds('%s/pulls/%s/commits?per_page=100' % (api, pr['number']), token)
        feladatok = set(tetelek([c['commit']['message'].splitlines()[0] for c in commitok if len(c.get('parents', [])) < 2]))
        feladatok |= {m.group(1) for m in [TETEL.match(pr.get('title', ''))] if m and m.group(1) != 'F0'}
        if any(feladat_a_mainben(f) for f in feladatok):
            print('#%s: %d napos, de a feladatának (%s) van a main-ben lépése: nincs jelzés.' % (pr['number'], nap, ', '.join(sorted(feladatok))))
            continue
        if not args.proba and van_komment(repo, pr['number'], token, MARKER_ALLO):
            print('#%s: %d napos, a jelzés már megvan.' % (pr['number'], nap))
            continue
        if args.proba:
            print('#%s: %d napos álló draft: jelzés lenne (próba, nem ír).' % (pr['number'], nap))
        else:
            print('#%s: %d napos álló draft: jelzés (%s).' % (pr['number'], nap, komment_ir(repo, pr['number'], token, MARKER_ALLO, allo_szoveg(nap))))
        jelzett += 1
    print('Új jelzés: %d.' % jelzett)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    al = ap.add_subparsers(dest='mod', required=True)
    p = al.add_parser('pr')
    p.add_argument('--uzenetek', help='a PR commit-tárgyainak fájlja, soronként egy (CI)')
    p.add_argument('--alap', default='origin/main')
    p.add_argument('--fej', default='HEAD')
    a = al.add_parser('allo')
    a.add_argument('--proba', action='store_true', help='nem ír kommentet, csak kiírja, mit jelezne (helyi mérés)')
    args = ap.parse_args(argv)
    return mod_pr(args) if args.mod == 'pr' else mod_allo(args)


if __name__ == '__main__':
    sys.exit(main())
