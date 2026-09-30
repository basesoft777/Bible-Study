#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P0.3 — gépi kapu a modell válaszaira (F22 22.1 ötpontos kapu).

Versenként:
  1. érvényes JSON (és a szerkezet: vers, parok, betoldas, forditatlan), a
     `vers` mező egyezik a bemenettel;
  2. minden hivatkozott sorszám létezik;
  3. minden Károli-token pontosan egyszer szerepel (a `parok` bal oldalán vagy
     a `betoldas`-ban);
  4. minden eredeti token szerepel legalább egyszer (a `parok` jobb oldalán vagy
     a `forditatlan`-ban);
  5. nincs `[HG]\\d{3,4}` minta a vers válaszában.

Hibás válasz esetén egy újrakérés a hibaüzenettel (ujrakeres_uzenet); ha
másodszor is hibás, a vers "kapuhiba" jelölést kap (a döntőbíróhoz megy) — ezt
a futtató logika végzi, a kapu csak a hibalistát adja.

A kötegválasz JSON-tömb (versenként egy objektum); a kapu elfogad
{"versek": [...]} burkolót és egyetlen objektumot is, és lehántja a
markdown-kerítést. A kötegből hiányzó vers hibás.

Használat:
    python eszkozok/karoli_strong/kapu.py --onteszt
"""

import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import tokenek  # noqa: E402

STRONG_MINTA = re.compile(r'[HG]\d{3,4}')
_KERITES = re.compile(r'^\s*```[a-zA-Z]*\s*\n(.*?)\n\s*```\s*$', re.DOTALL)


def _egesz(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _egeszlista(x):
    return isinstance(x, list) and all(_egesz(e) for e in x)


def vers_ellenoriz(obj, adat):
    """Egy vers objektumának ötpontos ellenőrzése; hibaüzenetek listája (üres = rendben).

    adat: bemenet.vers_adat(igehely).
    """
    hibak = []
    if not isinstance(obj, dict):
        return ['1. a vers nem JSON-objektum']
    for kulcs in ('vers', 'parok', 'betoldas', 'forditatlan'):
        if kulcs not in obj:
            hibak.append('1. hiányzik a(z) "%s" mező' % kulcs)
    if hibak:
        return hibak
    if obj['vers'] != adat['igehely']:
        hibak.append('1. a "vers" mező (%r) nem egyezik a bemenettel (%r)' % (obj['vers'], adat['igehely']))
    parok = obj['parok']
    szerk_ok = True
    if not isinstance(parok, list):
        hibak.append('1. a "parok" nem lista')
        szerk_ok = False
    else:
        for p in parok:
            if not (isinstance(p, list) and len(p) == 2 and _egesz(p[0]) and _egeszlista(p[1]) and p[1]):
                hibak.append('1. hibás pár (kell: [magyar_sorszam, [eredeti_sorszam, ...]], nem üres): %s'
                             % json.dumps(p, ensure_ascii=False))
                szerk_ok = False
                break
    for kulcs in ('betoldas', 'forditatlan'):
        if not _egeszlista(obj[kulcs]):
            hibak.append('1. a(z) "%s" nem egész számok listája' % kulcs)
            szerk_ok = False
    if not szerk_ok:
        return hibak

    nk = len(adat['karoli_tokenek'])
    ne = len(adat['eredeti'])
    bal = [p[0] for p in parok]
    jobb = [e for p in parok for e in p[1]]
    # 2. létező sorszámok
    rossz_k = sorted({x for x in bal + obj['betoldas'] if not 1 <= x <= nk})
    rossz_e = sorted({x for x in jobb + obj['forditatlan'] if not 1 <= x <= ne})
    if rossz_k:
        hibak.append('2. nem létező magyar sorszám: %s (a versben 1–%d szó van)' % (rossz_k, nk))
    if rossz_e:
        hibak.append('2. nem létező eredeti sorszám: %s (a versben 1–%d szó van)' % (rossz_e, ne))
    # 3. minden Károli-token pontosan egyszer
    szamlalo = {}
    for x in bal + obj['betoldas']:
        szamlalo[x] = szamlalo.get(x, 0) + 1
    hianyzo = [i for i in range(1, nk + 1) if szamlalo.get(i, 0) == 0]
    tobbszor = sorted(i for i, c in szamlalo.items() if c > 1 and 1 <= i <= nk)
    if hianyzo:
        hibak.append('3. ezek a magyar szavak sem a "parok" bal oldalán, sem a "betoldas"-ban nem szerepelnek: %s' % hianyzo)
    if tobbszor:
        hibak.append('3. ezek a magyar szavak többször szerepelnek (a "parok" bal oldalán vagy a "betoldas"-ban): %s' % tobbszor)
    # 4. minden eredeti token legalább egyszer
    lefedett = set(jobb) | set(obj['forditatlan'])
    hianyzo_e = [i for i in range(1, ne + 1) if i not in lefedett]
    if hianyzo_e:
        hibak.append('4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban nem szerepelnek: %s' % hianyzo_e)
    # 5. nincs Strong-minta
    if STRONG_MINTA.search(json.dumps(obj, ensure_ascii=False)):
        hibak.append('5. a válaszban Strong-szám formájú karakterlánc van; csak sorszámot írhatsz')
    return hibak


def _json_tomb(szoveg):
    """(objektumlista, hiba) a nyers válaszból."""
    s = szoveg.strip()
    m = _KERITES.match(s)
    if m:
        s = m.group(1).strip()
    try:
        x = json.loads(s)
    except ValueError as e:
        return None, '1. a válasz nem érvényes JSON: %s' % e
    if isinstance(x, dict) and isinstance(x.get('versek'), list):
        x = x['versek']
    elif isinstance(x, dict):
        x = [x]
    if not isinstance(x, list):
        return None, '1. a válasz nem JSON-tömb'
    return x, None


def valasz_ellenoriz(szoveg, igehelyek):
    """Kötegválasz ellenőrzése.

    Visszaad: {igehely: {'ok': bool, 'hibak': [...], 'obj': dict|None}} a bemeneti
    igehelyek mindegyikére. Ha a teljes válasz nem értelmezhető, minden vers hibás.
    """
    tomb, hiba = _json_tomb(szoveg)
    ki = {}
    if hiba:
        for ig in igehelyek:
            ki[ig] = {'ok': False, 'hibak': [hiba], 'obj': None}
        return ki
    kulcs_szerint = {}
    for o in tomb:
        if isinstance(o, dict) and isinstance(o.get('vers'), str):
            kulcs_szerint.setdefault(o['vers'], o)
    for ig in igehelyek:
        o = kulcs_szerint.get(ig)
        if o is None:
            ki[ig] = {'ok': False, 'hibak': ['1. a válaszból hiányzik ez a vers'], 'obj': None}
            continue
        hibak = vers_ellenoriz(o, bemenet.vers_adat(ig))
        ki[ig] = {'ok': not hibak, 'hibak': hibak, 'obj': o}
    return ki


def ujrakeres_uzenet(eredmeny):
    """Az egyetlen újrakérés üzenete: csak a hibás versek, a hibákkal."""
    sorok = ['A válaszod gépi ellenőrzésen elbukott. Javítsd, és KIZÁRÓLAG a hibás verseket küldd '
             'vissza újra, ugyanabban a JSON-tömb-formában (semmi más szöveg):']
    for ig, r in eredmeny.items():
        if not r['ok']:
            sorok.append('')
            sorok.append('VERS: %s' % ig)
            for h in r['hibak']:
                sorok.append('- %s' % h)
    return '\n'.join(sorok)


def onteszt():
    """A kapu önellenőrzése: a prompt példái átmennek; szintetikus hibák elbuknak."""
    hibak = []
    # 1. a prompt példái: bemenet szó szerint egyezik, kimenet átmegy
    pr = bemenet.prompt_utasitas()
    peldak = {
        '1Móz 1:1': '{"vers":"1Móz 1:1","parok":[[1,[1,2]],[2,[3]],[3,[4]],[5,[7]],[6,[8]],[8,[11]]],'
                    '"betoldas":[4,7],"forditatlan":[5,6,9,10]}',
        'Mt 1:1': '{"vers":"Mt 1:1","parok":[[1,[3]],[2,[4]],[3,[6]],[4,[5]],[5,[8]],[6,[7]],[7,[2]],[9,[1]]],'
                  '"betoldas":[8],"forditatlan":[]}',
    }
    for ig, kimenet in peldak.items():
        if bemenet.versblokk(ig, kjv=True) not in pr:
            hibak.append('a prompt példabemenete nem egyezik a bemenet.versblokk kimenetével: %s' % ig)
        if kimenet not in pr:
            hibak.append('a példakimenet nincs benne a promptban: %s' % ig)
        h = vers_ellenoriz(json.loads(kimenet), bemenet.vers_adat(ig))
        if h:
            hibak.append('a példakimenet nem megy át a kapun (%s): %s' % (ig, h))
    # 2. szintetikus hibák
    adat = bemenet.vers_adat('1Móz 1:1')
    jo = json.loads(peldak['1Móz 1:1'])
    esetek = [
        ('vers-mező', dict(jo, vers='1Móz 1:2'), '1.'),
        ('hiányzó magyar szó', dict(jo, betoldas=[4]), '3.'),
        ('kétszer szereplő magyar szó', dict(jo, betoldas=[4, 7, 1]), '3.'),
        ('hiányzó eredeti szó', dict(jo, forditatlan=[5, 6, 9]), '4.'),
        ('nem létező magyar sorszám', dict(jo, betoldas=[4, 7, 9]), '2.'),
        ('nem létező eredeti sorszám', dict(jo, forditatlan=[5, 6, 9, 10, 12]), '2.'),
        ('Strong-szám', dict(jo, vers='1Móz 1:1', parok=jo['parok'] + [], betoldas=[4, 7],
                             forditatlan=[5, 6, 9, 10], megjegyzes='H7225'), '5.'),
        ('üres eredeti-lista a párban', dict(jo, parok=[[1, []]] + jo['parok'][1:]), '1.'),
    ]
    for nev, obj, pont in esetek:
        h = vers_ellenoriz(obj, adat)
        if not any(x.startswith(pont) for x in h):
            hibak.append('a kapu nem fogta meg: %s (várt pont %s, kapott %s)' % (nev, pont, h))
    # 3. kötegszintű feldolgozás
    kotegvalasz = '```json\n[%s]\n```' % peldak['1Móz 1:1']
    r = valasz_ellenoriz(kotegvalasz, ['1Móz 1:1', '1Móz 1:2'])
    if not r['1Móz 1:1']['ok'] or r['1Móz 1:2']['ok']:
        hibak.append('kötegfeldolgozás: a hiányzó vers nem lett hibás, vagy a jó vers elbukott')
    r = valasz_ellenoriz('ez nem json', ['1Móz 1:1'])
    if r['1Móz 1:1']['ok']:
        hibak.append('kötegfeldolgozás: érvénytelen JSON elfogadva')
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('önteszt rendben (példák: %d, szintetikus hibaesetek: %d)' % (len(peldak), len(esetek)))
    return 0


if __name__ == '__main__':
    if '--onteszt' in sys.argv:
        sys.exit(onteszt())
    print(__doc__)
