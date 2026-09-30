#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pr_komment.py -- CI.2: az ellenorzes jelentesenek kiirasa PR-kommentkent.
Kizarolag a standard library-t hasznalja (urllib), nem harmadik feles
csomagot -- l. F02_CI_ELLENORZES_BRIEF.md "Alapelvek": "csak a standard
library-t es a repo sajat szkriptjeit hasznalja, kulso szolgaltatast nem
hiv" (a GitHub sajat REST API-ja nem "kulso szolgaltatas" ebben az
ertelemben -- ez maga a plattform, amelyen a workflow fut).

Ha mar van a PR-en egy korabbi ellenorzes-komment (a MARKER alapjan),
FRISSITI azt (PATCH), nem uj kommentet ir minden futasnal -- igy egy
tobbszor pusholt PR nem szemeteli tele a beszelgetest.

Kornyezeti valtozok (GitHub Actions biztositja):
    GITHUB_TOKEN, GITHUB_REPOSITORY ("tulaj/repo"), PR_SZAM

CLI:
    python eszkozok/ellenorzes/pr_komment.py JELENTES_FAJL [JELENTES_FAJL ...]
"""

import json
import os
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

MARKER = '<!-- ellenorzes-jelentes -->'


def _kerds(url, token, method='GET', adat=None):
    fejlecek = {
        'Authorization': 'Bearer %s' % token,
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'bible-study-ellenorzes',
    }
    torzs = json.dumps(adat).encode('utf-8') if adat is not None else None
    req = urllib.request.Request(url, data=torzs, headers=fejlecek, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    if len(sys.argv) < 2:
        print('Hasznalat: pr_komment.py JELENTES_FAJL [JELENTES_FAJL ...]', file=sys.stderr)
        return 2

    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    pr_szam = os.environ.get('PR_SZAM')
    if not (token and repo and pr_szam):
        print('Nincs GITHUB_TOKEN/GITHUB_REPOSITORY/PR_SZAM -- kihagyva (nem PR-esemeny).', file=sys.stderr)
        return 0

    reszek = [MARKER, '']
    for fajl in sys.argv[1:]:
        if not os.path.exists(fajl):
            continue
        with open(fajl, 'r', encoding='utf-8') as f:
            reszek.append(f.read())
    torzs = '\n'.join(reszek)
    if len(torzs) > 60000:
        torzs = torzs[:60000] + '\n\n... (a jelentes a GitHub Actions log-ban teljes)'

    alap_url = 'https://api.github.com/repos/%s' % repo
    try:
        kommentek = _kerds('%s/issues/%s/comments' % (alap_url, pr_szam), token)
    except urllib.error.URLError as exc:
        print('Nem sikerult lekerni a kommenteket: %s' % exc, file=sys.stderr)
        return 2

    meglevo = None
    for k in kommentek:
        if MARKER in (k.get('body') or ''):
            meglevo = k
            break

    try:
        if meglevo is not None:
            _kerds('%s/issues/comments/%s' % (alap_url, meglevo['id']), token,
                   method='PATCH', adat={'body': torzs})
            print('Frissitve a %s komment.' % meglevo['id'])
        else:
            _kerds('%s/issues/%s/comments' % (alap_url, pr_szam), token,
                   method='POST', adat={'body': torzs})
            print('Uj komment letrehozva.')
    except urllib.error.URLError as exc:
        print('Nem sikerult a kommentet irni: %s' % exc, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
