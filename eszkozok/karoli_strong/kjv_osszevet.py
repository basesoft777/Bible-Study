#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F8V3 (F21.62) — a KJV-támpont két forrásának összevetése és a lefedettség mérése.

A 'regi' forrás: KJV_Strongs_Genesis/Exodus/Proverbs.tsv (tokenek.kjv_tamapont),
a 'teljes' forrás: konkordancia/KJV_Strongs_teljes.tsv (tokenek.kjv_tamapont_teljes).

Mér (hálózat nélkül, csak olvas):
  1. A 200 verses mintán rétegenként (R1–R4): hány versre van KJV-sor a régi / a teljes
     forrásból; hány vers nem kap (a teljes forrásból) KJV-sort, és miért.
  2. A kontroll (az R1 versei, ahol az F3V3 is kapott KJV-t): a két forrásból épített
     sor összevetése versenként: bájtra azonos / csak az angol szó eltér (a Strong-sor
     azonos) / a Strong-sor eltér (üres szavú elemek: a régi tábla {H0853}-szerű, angol
     szó nélküli elemei; egyéb eltérés).
  3. Ugyanez a kontroll a teljes Gen/Exo/Péld Károli-versállományon (a minta nélkül).

Kimenet: stdout és a --tsv fájl (alap: f21p/kjv_osszevet_f8v3.tsv, versenként a mintán).
A TSV-t split/join kezeli (nincs csv).

  python eszkozok/karoli_strong/kjv_osszevet.py [--tsv <út>]
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

MINTA_UT = os.path.join(tokenek.ROOT, 'f21p', 'minta.tsv')
TSV_ALAP = os.path.join(tokenek.ROOT, 'f21p', 'kjv_osszevet_f8v3.tsv')
_ELEM = re.compile(r'\{([HG]\d{4})\}')


def _minta():
    with open(MINTA_UT, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.strip()]


def strongok(sor):
    """A KJV-sor Strong-sorozata (sorrendben)."""
    return _ELEM.findall(sor)


def hianyok_osztaly():
    """naplok/F19_hianyok.tsv: {igehely_kjv_alak 'Mk 9:43' (Károli-igehely) -> osztaly} a KJV-sorokra
    (a 'verzio' = KJV sorai); a fájl fejlécén a '#' sorokat kihagyja."""
    ki = {}
    if not os.path.exists(tokenek.KJV_HIANYOK):
        return ki
    with open(tokenek.KJV_HIANYOK, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if not s.strip() or s.startswith('#') or s.startswith('verzio\t'):
                continue
            r = s.split('\t')
            if r[0] == 'KJV':
                ki[r[1]] = r[6]
    return ki


def osztaly(regi, uj):
    """Egy vers két KJV-sorának (None = nincs) összehasonlítási osztálya."""
    if regi is None and uj is None:
        return 'mindketto_nincs'
    if regi is None:
        return 'csak_teljesben_van'
    if uj is None:
        return 'csak_regiben_van'
    if regi == uj:
        return 'azonos_bajt'
    sr, su = strongok(regi), strongok(uj)
    if sr == su:
        return 'strong_azonos_szo_elter'
    # az üres szavú elemek ('{H0853}' szó nélkül) a régi táblában külön elemek
    if sr and su and [x for x in sr] != [x for x in su]:
        if sorted(sr) == sorted(su):
            return 'strong_sorrend_elter'
        if len(sr) > len(su) and _reszsorozat(su, sr):
            return 'strong_elter_regi_tobb'
        if len(su) > len(sr) and _reszsorozat(sr, su):
            return 'strong_elter_teljes_tobb'
    return 'strong_elter_egyeb'


def _reszsorozat(kicsi, nagy):
    it = iter(nagy)
    return all(x in it for x in kicsi)


def _ures_szavu_elemek(sor):
    """A régi tábla szó nélküli '{Hxxxx}' elemeinek száma a sorban."""
    return len(re.findall(r'(?:^|\s)\{[HG]\d{4}\}', sor))


def meres(minta=None):
    minta = _minta() if minta is None else minta
    sorok = []
    for s in minta:
        ig = s['igehely']
        regi = tokenek.kjv_tamapont(ig)
        uj = tokenek.kjv_tamapont_teljes(ig)
        sorok.append({'igehely': ig, 'reteg': s['reteg'], 'regi': regi, 'uj': uj, 'osztaly': osztaly(regi, uj),
                      'minta_kjv': s.get('kjv_tamapont', '')})
    return sorok


def nincs_ok(igehely, hianyok):
    """Miért nincs KJV-sor a teljes forrásból (a versmegfeleltetés / F19 hiányok szerint)."""
    megf, _ = tokenek._kjv_megfeleltetes()
    kjv = megf.get(igehely)
    if igehely not in megf:
        return 'nincs_a_versmegfeleltetesben'
    if not kjv or not re.match(r'^\d+:\d+$', kjv):
        return 'nincs_KJV_megfelelo (igehely_kjv=%r)' % kjv
    if igehely in hianyok:
        return 'F19_hiany:%s' % hianyok[igehely]
    return 'a_megfelelo_KJV_vers_nincs_a_teljes_tablaban'


def kontroll_teljes_allomany():
    """A teljes Gen/Exo/Péld Károli-versállomány kontrollja (a régi tábla fedi: Gen/Exo/Pro)."""
    karoli = tokenek.betolt_karoli()
    kon = ('1Móz', '2Móz', 'Péld')
    ossz = {}
    n = 0
    for ig in karoli:
        b = tokenek.igehely_bont(ig)
        if not b or b[0] not in kon:
            continue
        n += 1
        o = osztaly(tokenek.kjv_tamapont(ig), tokenek.kjv_tamapont_teljes(ig))
        ossz[o] = ossz.get(o, 0) + 1
    return n, ossz


def kiir(tsv_ut=None, csendes=False):
    sorok = meres()
    hianyok = hianyok_osztaly()
    retegek = sorted({s['reteg'] for s in sorok})
    ki = []
    p = ki.append
    ut, sha = tokenek.kjv_forras_azonosito()
    p('KJV-összevetés (F8V3, F21.62); teljes forrás: %s sha256=%s' % (ut, sha))
    p('')
    p('1. Lefedettség a 200 verses mintán (KJV-sor a versre):')
    p('%-5s %6s %10s %10s %14s' % ('réteg', 'vers', 'régi', 'teljes', 'teljes: nincs'))
    ossz = [0, 0, 0, 0]
    for r in retegek:
        v = [s for s in sorok if s['reteg'] == r]
        a = sum(1 for s in v if s['regi'])
        b = sum(1 for s in v if s['uj'])
        p('%-5s %6d %10d %10d %14d' % (r, len(v), a, b, len(v) - b))
        for i, x in enumerate((len(v), a, b, len(v) - b)):
            ossz[i] += x
    p('%-5s %6d %10d %10d %14d' % ('ossz.', *ossz))
    p('  (a minta.tsv kjv_tamapont=van oszlopa: %d vers; a régi forrás számolt értékével egyezik: %s)' % (
        sum(1 for s in sorok if s['minta_kjv'] == 'van'),
        'igen' if all((s['minta_kjv'] == 'van') == bool(s['regi']) for s in sorok) else 'NEM'))
    nincs = [s for s in sorok if not s['uj']]
    p('  teljes forrásból KJV-sor nélküli versek (%d):' % len(nincs))
    for s in nincs:
        p('    %-5s %-14s %s' % (s['reteg'], s['igehely'], nincs_ok(s['igehely'], hianyok)))
    p('')
    p('2. Kontroll az R1 mintaversein (a régi és a teljes forrásból épített sor):')
    r1 = [s for s in sorok if s['reteg'] == 'R1']
    cnt = {}
    for s in r1:
        cnt[s['osztaly']] = cnt.get(s['osztaly'], 0) + 1
    p('  R1 versek: %d' % len(r1))
    for k in sorted(cnt):
        p('  %-28s %4d' % (k, cnt[k]))
    sz_r = sum(len(s['regi']) for s in r1 if s['regi'])
    sz_u = sum(len(s['uj']) for s in r1 if s['uj'])
    ures = sum(_ures_szavu_elemek(s['regi']) for s in r1 if s['regi'])
    p('  KJV-sor karakterszám az R1-en: régi %d, teljes %d (különbség %+d); a régi sorokban szó nélküli {Hxxxx} elem: %d' % (
        sz_r, sz_u, sz_u - sz_r, ures))
    p('')
    p('3. Kontroll a teljes Gen/Exo/Péld Károli-versállományon (a mintán kívül is):')
    n, c3 = kontroll_teljes_allomany()
    p('  versek: %d' % n)
    for k in sorted(c3):
        p('  %-28s %4d' % (k, c3[k]))
    if not csendes:
        print('\n'.join(ki))
    if tsv_ut:
        with open(tsv_ut, 'w', encoding='utf-8', newline='') as f:
            f.write('# GENERÁLT: eszkozok/karoli_strong/kjv_osszevet.py — kézzel nem szerkesztendő.\n')
            f.write('# proveniencia: scope=a 200 verses minta (f21p/minta.tsv) | forras=%s sha256=%s; régi: KJV_Strongs_Genesis/Exodus/Proverbs.tsv | ts=%s\n'
                    % (ut, sha, tokenek.generalas_ts()))
            f.write('\t'.join(['igehely', 'reteg', 'regi_van', 'teljes_van', 'osztaly', 'regi_kar', 'teljes_kar', 'nincs_ok']) + '\n')
            for s in sorok:
                f.write('\t'.join([s['igehely'], s['reteg'], 'igen' if s['regi'] else 'nem', 'igen' if s['uj'] else 'nem',
                                   s['osztaly'], str(len(s['regi'] or '')), str(len(s['uj'] or '')),
                                   '' if s['uj'] else nincs_ok(s['igehely'], hianyok)]) + '\n')
    return ki


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tsv', default=None, help='versenkénti TSV kimenet (alap: nem ír; javasolt: f21p/kjv_osszevet_f8v3.tsv)')
    a = ap.parse_args()
    kiir(a.tsv)
