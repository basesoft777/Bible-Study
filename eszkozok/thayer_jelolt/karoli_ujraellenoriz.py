#!/usr/bin/env python
"""A kész Thayer-sorok Károli-ellenőrzése régi és teljes mankóval (F153, M0).

A „régi” mankó a #22 párosításából a Mt, Mk, Luk, Ján és ApCsel sorai nélkül (a #132/#142 futásakor ez volt a lefedettség);
a „teljes” a mai `adat/karoli_strong/parok_*.tsv`. Soronként (az `adat/forditasok.tsv` nem `elavult`, `szotar = Thayer`,
`mezo = forditas_hu` sorai): a fordítás magyar szavainak négybetűs tövei (`glossza_lexikon_forditas.tovek`) egyeznek-e a Strong
Károli-alakjainak tövével. Nem értelmez és nem tölt ki: üres Károli-alaklistánál `nincs_adat` (CLAUDE.md 3. szabály).

  python eszkozok/thayer_jelolt/karoli_ujraellenoriz.py --meres [--ki naplok/THAYER_KAROLI_TELJES_meres.tsv]

TSV: split('\\t'), csv modul nélkül.
"""
import argparse
import collections
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
PAROK_MAPPA = os.path.join(GYOKER, 'adat', 'karoli_strong')
FORDITASOK_UT = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
HIANYZO_KONYVEK = ('Mt', 'Mk', 'Luk', 'Ján', 'ApCsel')
KOTOSZO_UT_ELO = 3


def tovek(szoveg):
    """A tartalmas magyar szavak négybetűs tövei (a Károli-összevetéshez; a görög/héber írás kimarad)."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
    import glossza_lexikon_forditas as G
    return G.tovek(szoveg)


def strong_kulcs(s):
    return s[0] + str(int(s[1:5]))


def parok_alakok(strong, mappa=PAROK_MAPPA):
    """(teljes, régi): Counter(kisbetűs Károli-alak) a Strongra; a régi a HIANYZO_KONYVEK sorai nélkül."""
    cel = strong_kulcs(strong)
    teljes, regi = collections.Counter(), collections.Counter()
    for fn in sorted(os.listdir(mappa)):
        if not re.match(r'^parok_.+\.tsv$', fn):
            continue
        with open(os.path.join(mappa, fn), encoding='utf-8', newline='') as f:
            for l in f.read().split('\n'):
                if not l or l.startswith('#') or l.startswith('vers\t'):
                    continue
                m = l.rstrip('\r').split('\t')
                if len(m) > 5 and len(m[5]) >= 5 and m[5][1:5].isdigit() and m[5][0] + str(int(m[5][1:5])) == cel:
                    alak = m[2].lower()
                    teljes[alak] += 1
                    if m[0].rsplit(' ', 1)[0] not in HIANYZO_KONYVEK:
                        regi[alak] += 1
    return teljes, regi


def egyezes(sor_tovek, alakok):
    """('egyezik', {tő: n}) | ('nem_talal', {}) | ('nincs_adat', {}) | ('nincs_ellenorzendo', {})."""
    if not sor_tovek:
        return 'nincs_ellenorzendo', {}
    if not alakok:
        return 'nincs_adat', {}
    t = collections.Counter()
    for alak, n in alakok.items():
        if alak[:4] in sor_tovek:
            t[alak[:4]] += n
    return ('egyezik', dict(t)) if t else ('nem_talal', {})


def uralkodo(alakok):
    """A leggyakoribb négybetűs tő (a toldalékolt alakok összevonva); a névszó/igealak váltása nem számít váltásnak."""
    c = collections.Counter()
    for a, n in alakok.items():
        c[a[:4]] += n
    return c.most_common(1)[0][0] if c else ''


def thayer_sorok():
    with open(FORDITASOK_UT, encoding='utf-8', newline='') as f:
        ls = f.read().split('\n')
    ki = []
    fej = ls[1].split('\t') if ls[0].startswith('#') else ls[0].split('\t')
    for l in ls:
        if not l or l.startswith('#'):
            continue
        m = l.rstrip('\r').split('\t')
        if m[0] == 'szotar':
            fej = m
            continue
        d = dict(zip(fej, m))
        if d['szotar'] == 'Thayer' and d['mezo'] == 'forditas_hu' and d['allapot'] != 'elavult':
            ki.append(d)
    return ki


def meres(ts=None):
    ts = ts or datetime.date.today().isoformat()
    cache = {}
    sorok = []
    for d in thayer_sorok():
        s = d['strong']
        if s not in cache:
            cache[s] = parok_alakok(s)
        teljes, regi = cache[s]
        t = tovek(d['forditas_hu'])
        er, _ = egyezes(t, regi)
        et, tt = egyezes(t, teljes)
        ur_r, ur_t = uralkodo(regi), uralkodo(teljes)
        uj = [a for a, _n in teljes.most_common(10) if a not in regi]
        if er == 'nem_talal' and et == 'egyezik':
            osszegzes = 'megerosites'
        elif et == 'nem_talal':
            osszegzes = 'nem_talal_teljes' + ('+uralkodo_valt' if ur_r != ur_t else '')
        elif ur_r != ur_t:
            osszegzes = 'uralkodo_valt' + ('' if ur_t[:4] in t else '+nincs_a_forditasban')
        else:
            osszegzes = 'valtozatlan' if er == et else 'egyezik_bovult'
        sorok.append([s, d['jelentes_szam'], d['allapot'], er, et, ur_r, ur_t,
                      ','.join(uj), '%d>%d' % (sum(regi.values()), sum(teljes.values())), osszegzes])
    prov = ('# proveniencia: scope=adat/forditasok.tsv (szotar=Thayer, mezo=forditas_hu, allapot!=elavult), '
            'adat/karoli_strong/parok_*.tsv (régi = Mt, Mk, Luk, Ján, ApCsel nélkül) | forras=eszkozok/thayer_jelolt/'
            'karoli_ujraellenoriz.py --meres (négybetűs tő egyezés) | ts=%s' % ts)
    fej = ['strong', 'szakasz', 'allapot', 'regi', 'teljes', 'uralkodo_regi', 'uralkodo_teljes',
           'uj_alakok_top10', 'link_regi>teljes', 'osszegzes']
    return prov, fej, sorok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ki')
    a = ap.parse_args()
    if not a.meres:
        ap.error('--meres kell')
    prov, fej, sorok = meres()
    szoveg = prov + '\n' + '\t'.join(fej) + '\n' + '\n'.join('\t'.join(r) for r in sorok) + '\n'
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
    else:
        sys.stdout.write(szoveg)
    c = collections.Counter(r[-1] for r in sorok)
    print('%d sor; %s' % (len(sorok), ', '.join('%s=%d' % x for x in sorted(c.items()))), file=sys.stderr)


if __name__ == '__main__':
    main()
