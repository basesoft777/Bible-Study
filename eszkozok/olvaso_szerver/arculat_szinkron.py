"""Szinkron-kimenet a design systemhez (#98 M2, M0 2.4): a token-fájlból a „PaRDeS olvasó” design system `tokens.json`-ja.

A token-fájl (`konfig/arculat.json`) és az elem-regiszter (`konfig/elemek.toml`) alapján előállítja a design system
`tokens.json` szerkezetét: `color.themes/tokens`, `type.fonts/families/groups/styles`, `spacing.tokens`, `radius.tokens`,
`name`, `meta`. Feltöltés nincs: azt a felhasználó kérésére az ügynök végzi (Artifact eszköz). A kimenetet a repón kívülre
tedd (`--kimenet`).

- Az értékek (szín világos/sötét, betűméret, sorköz, térköz, lekerekítés) a token-fájlból jönnek, mindig.
- A `usage` a regiszterből: „Használja: <elem magyar neve>, …”; ha `--alap` (a design system mostani `tokens.json`-ja) meg
  van adva, és ott a tokennek van leírása, az marad.
- A betűvastagság és a betűcsalád a stíluslap (`statikus/olvaso.css`) első, a tokent használó szabályából (a szerver értéke;
  pl. az `oldalcim` 600, M0 5. szakasz 2.).
- `--alap` nélkül a betűstílusok betűcsaládonként csoportosulnak; `--alap`-pal a design system csoportjai maradnak (a
  stílusok értéke frissül), a többi betűméret-token egy új csoportba kerül („Szerver: további stílusok”).
- A design system térköz-skálája (`space-1` … `space-6`) helyére a szerver térköz-tokenjei kerülnek (DT-F98b).

Használat:  python arculat_szinkron.py --kimenet <tokens.json> [--alap <a design system mostani tokens.json-ja>] [--datum ÉÉÉÉ-HH-NN]
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import arculat as arculat_modul
import tervezo

D = os.path.dirname(os.path.abspath(__file__))
REPO = 'basesoft777/Bible-Study'
CSOMAG = 'eszkozok/olvaso_szerver'
# a design system stílusneve → a szerver betűméret-tokenje, ahol eltér
DS_NEV = {'interlinearis-heber': 'il-heber'}
CSALAD_CSOPORT = (('text', 'Olvasószöveg'), ('he', 'Eredeti nyelvek'), ('gr', 'Görög'), ('ui', 'Felület'), ('mono', 'Kód'))
UJ_CSOPORT = 'Szerver: további stílusok'


def hasznalat(regiszter):
    """{token: [elem magyar neve, …]} a regiszter sorrendjében."""
    ki = {}
    for e in regiszter.elemek:
        for t in e['tulajdonsag']:
            lista = ki.setdefault(t['token'], [])
            if e['nev'] not in lista:
                lista.append(e['nev'])
    return ki


def stilus_jegyek(css):
    """{betűméret-kulcs: (vastagság, betűcsalád-kulcs)} a stíluslap első, a tokent használó szabályából."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'@media[^{]*\{((?:[^{}]*\{[^{}]*\})*)\s*\}', r'\1', css)
    ki = {}
    for torzs in re.findall(r'\{([^{}]*)\}', css):
        for nev in re.findall(r'var\(--fs-([a-z0-9-]+)\)', torzs):
            if nev in ki:
                continue
            suly, csalad = '400', ''
            m = re.search(r'(?<![\w-])font\s*:\s*([^;]*var\(--fs-%s\)[^;]*)' % re.escape(nev), torzs)
            if m and re.match(r'\s*(\d00)\b', m.group(1)):
                suly = re.match(r'\s*(\d00)\b', m.group(1)).group(1)
            m2 = re.search(r'font-weight\s*:\s*(\d00)', torzs)
            if m2:
                suly = m2.group(1)
            m3 = re.search(r'var\(--font-([a-z]+)\)', torzs)
            if m3:
                csalad = m3.group(1)
            ki[nev] = (suly, csalad)
    return ki


def git_ref():
    try:
        ag = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=D, capture_output=True, text=True, check=True).stdout.strip()
        fej = subprocess.run(['git', 'rev-parse', '--short=8', 'HEAD'], cwd=D, capture_output=True, text=True, check=True).stdout.strip()
        return '%s@%s' % (ag, fej)
    except (OSError, subprocess.CalledProcessError):
        return 'ismeretlen'


def _leiras(token, alap_usage, hasz, megj=''):
    if alap_usage:
        return alap_usage
    nevek = hasz.get(token, [])
    s = ('Használja: ' + ', '.join(nevek) + '.') if nevek else 'A regiszterben nincs elemhez rendelve (a tervező mód tartalékán át állítható).'
    return s + megj


def tokens_json(arc, regiszter, css, alap=None, datum=None, ref=None):
    """A design system `tokens.json`-ja (szótár)."""
    adat = arc.adat
    hasz = hasznalat(regiszter)
    jegyek = stilus_jegyek(css)
    alap = alap or {}

    # -- színek
    alap_szin = {t['name']: t for t in (alap.get('color') or {}).get('tokens', [])}
    sorrend = [n for n in alap_szin if n in adat['szin']] + sorted(n for n in adat['szin'] if n not in alap_szin)
    szinek = [{'name': n, 'value': {'light': adat['szin'][n]['light'], 'dark': adat['szin'][n]['dark']},
               'usage': _leiras(n, alap_szin.get(n, {}).get('usage'), hasz)} for n in sorrend]
    temak = (alap.get('color') or {}).get('themes') or [{'id': 'light', 'name': 'Világos'}, {'id': 'dark', 'name': 'Sötét'}]

    # -- betűstílusok
    def stilus(kulcs, ds_nev=None, regi=None, csoport_csalad=''):
        suly, csalad = jegyek.get(kulcs, ('400', ''))
        meret = adat['betumeret'][kulcs]
        megj = ' Relatív érték: %s (a környezet betűméretéhez).' % meret if meret.endswith('em') and not meret.endswith('rem') else ''
        s = dict(regi or {})
        s.update({'name': ds_nev or kulcs, 'fontSize': meret, 'lineHeight': adat['sorkoz'].get(kulcs, (regi or {}).get('lineHeight', 'normal')),
                  'fontWeight': suly})
        s.setdefault('letterSpacing', '0')
        s.setdefault('fontStyle', 'normal')
        s.setdefault('opticalSize', None)
        s['family'] = (regi or {}).get('family', '') if regi else ('' if csalad in ('', csoport_csalad) else csalad)
        s.setdefault('sample', (hasz.get('fs-' + kulcs) or [''])[0])
        s['usage'] = _leiras('fs-' + kulcs, (regi or {}).get('usage'), hasz, megj)
        return s

    csoportok, lefedett = [], set()
    for cs in (alap.get('type') or {}).get('groups', []):
        uj = dict(cs)
        uj['styles'] = []
        for st in cs.get('styles', []):
            kulcs = DS_NEV.get(st['name'], st['name'])
            if kulcs in adat['betumeret']:
                uj['styles'].append(stilus(kulcs, st['name'], st, cs.get('family', '')))
                lefedett.add(kulcs)
            else:
                uj['styles'].append(st)
        csoportok.append(uj)
    maradek = sorted(k for k in adat['betumeret'] if k not in lefedett)
    if alap.get('type'):
        if maradek:
            csoportok.append({'name': UJ_CSOPORT, 'family': 'ui', 'note': 'A szerver szerep szerinti betűméret-tokenjei (DT-F98a), amelyeknek a design systemben még nincs stílusa.',
                              'styles': [stilus(k, csoport_csalad='ui') for k in maradek]})
    else:
        for csalad, nev in CSALAD_CSOPORT:
            st = [stilus(k, csoport_csalad=csalad) for k in maradek if (jegyek.get(k, ('', 'ui'))[1] or 'ui') == csalad]
            if st:
                csoportok.append({'name': nev, 'family': csalad, 'note': '', 'styles': st})

    # -- térköz és lekerekítés
    terkoz = [{'name': 'space-' + k, 'value': v, 'usage': _leiras('space-' + k, None, hasz)} for k, v in sorted(adat['terkoz'].items())]
    alap_rad = {t['name']: t for t in (alap.get('radius') or {}).get('tokens', [])}
    rad_sor = [n for n in alap_rad if n.startswith('radius-') and n[7:] in adat['lekerekites']]
    rad_sor += sorted(('radius-' + k for k in adat['lekerekites'] if 'radius-' + k not in rad_sor), key=lambda n: float(adat['lekerekites'][n[7:]][:-2]))
    sugar = [{'name': n, 'value': adat['lekerekites'][n[7:]], 'usage': _leiras(n, alap_rad.get(n, {}).get('usage'), hasz)} for n in rad_sor]

    meta = dict(alap.get('meta') or {})
    meta.update({'source': 'github', 'repo': REPO, 'ref': ref or git_ref(), 'package': CSOMAG,
                 'synced': datum or datetime.date.today().isoformat(), 'arculat_hash': arc.hash,
                 'origin': meta.get('origin', 'a #60 pilot tokenjei a szerver változónevein (PR #346)') + '; a szerver token-fájljából szinkronizálva (#98, arculat_szinkron.py)'})
    paths = dict(meta.get('paths') or {})
    paths['tokens'] = [CSOMAG + '/konfig/arculat.json']
    paths['registry'] = [CSOMAG + '/konfig/elemek.toml']
    meta['paths'] = paths
    return {
        'version': 1,
        'color': {'themes': temak, 'tokens': szinek},
        'type': {'fonts': (alap.get('type') or {}).get('fonts', []), 'families': dict(adat['betucsalad']), 'groups': csoportok},
        'spacing': {'note': 'A szerver térköz-tokenjei (konfig/arculat.json, terkoz): csak a regiszterben kitett térközök (DT-F98b); a többi térköz literál.',
                    'tokens': terkoz},
        'radius': {'note': (alap.get('radius') or {}).get('note', ''), 'tokens': sugar},
        'name': alap.get('name', 'PaRDeS olvasó'),
        'meta': meta,
    }


def main():
    ap = argparse.ArgumentParser(description='A design system tokens.json-ja a szerver token-fájljából (feltöltés nélkül)')
    ap.add_argument('--kimenet', required=True, help='a kimeneti tokens.json (a repón kívül)')
    ap.add_argument('--alap', help='a design system mostani tokens.json-ja (a leírások és a csoportok megtartásához)')
    ap.add_argument('--datum', help='a meta.synced értéke (alap: a mai nap)')
    a = ap.parse_args()
    arc = arculat_modul.Arculat.betolt()
    reg = tervezo.Regiszter.betolt(arc.adat)
    alap = None
    if a.alap:
        with open(a.alap, encoding='utf-8') as f:
            alap = json.load(f)
    ki = tokens_json(arc, reg, tervezo.css_beolvas(), alap, a.datum)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(ki, ensure_ascii=False, indent=2) + '\n')
    print('kiírva: %s (szín %d, betűstílus %d, térköz %d, lekerekítés %d; arculat %s)' % (
        a.kimenet, len(ki['color']['tokens']), sum(len(g['styles']) for g in ki['type']['groups']), len(ki['spacing']['tokens']),
        len(ki['radius']['tokens']), arc.hash))


if __name__ == '__main__':
    main()
