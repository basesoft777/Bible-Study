#!/usr/bin/env python
"""A BDB sima szöveges nézete a szakasztáblából és a javítótáblából (F107; DT-F107c (d), felhasználó, 2026-10-18).

A nézet Strongonként: a `adat/bdb_szakaszok.tsv` sorainak `jel` + `szoveg` mezője egy szóközzel összefűzve (a `<sub>` gyakoriságszám
nélkül), a `adat/bdb_forras_javitas.tsv` javításaival:
  - `hivatkozas` / `javitva`: a TSV utólagos F34/F46 hivatkozás-javításai — a Strong nézet-szövegében a `forras_alak` `elofordulas`-adik
    egész-token előfordulása → `javitott_alak`;
  - `pe_mem` / `javitva` (csak `--pe-mem`): a táblasor `szoveg`-ének `szo_sorszam`-adik héber szavában az `elofordulas`-adik dagesses mem
    → dagesses pe (a forrás alakjában: a U+FB3E prezentációs formát U+FB44-re, különben a mem betűt pére cserélve);
  - `kezi` (szerkezeti forráshiba): a szöveget nem változtatja.

A kimenet NEM a `konkordancia/BDB_teljes_unabridged.tsv` (az változatlan, DT-F107c (d)), és nem a repó: a `--ki` útvonalra íródik
(a brief `ir` mezője nem ad neki helyet). Formátum: a TSV-é (`Strong_padded`, `Strong_eredeti`, `Teljes_szocikk`).

  --ki PATH       a nézet írása
  --pe-mem        a pe/mem javítás alkalmazása is
  --osszevet      a nézet összevetése a TSV-vel, osztályozva (azonos / sub / szokoz / forras_html / pe_mem / egyeb / nincs_a_nezetben)
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import forras_javit  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
JAV = os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')
TSV = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')

HEBER_EREDETI = re.compile('[֐-׿יִ-ﭏ]+')
MEM, PE, DAG, MEM_DAG, PE_DAG = 'מ', 'פ', 'ּ', 'מּ', 'פּ'
JELOLES_TOREDEK = re.compile(r'href=|class=|<a |<font|<e |</|<p')


def ws(t):
    return re.sub(r'\s+', ' ', t).strip()


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]


def mem_csere_szoban(szo, k):
    """A szó k-adik dagesses memje → dagesses pe, a forrás alakjában."""
    n = 0
    s = list(szo)
    for i, c in enumerate(s):
        if c == MEM_DAG:
            n += 1
            if n == k:
                s[i] = PE_DAG
                return ''.join(s)
        elif c == MEM:
            j = i + 1
            while j < len(s) and '֑' <= s[j] <= 'ׇ':
                if s[j] == DAG:
                    n += 1
                    if n == k:
                        s[i] = PE
                        return ''.join(s)
                    break
                j += 1
    return None


def pe_mem_sorban(szoveg, javitasok):
    """A sor szövegében a (szo_sorszam, elofordulas) helyek cseréje; a sikertelen cserék száma."""
    szavak = list(HEBER_EREDETI.finditer(szoveg))
    hiba = 0
    csere = {}
    # szavanként hátulról előre: egy szó több dagesses memjének cseréje ne tolja el a későbbi előfordulás sorszámát
    for d in sorted(javitasok, key=lambda x: (int(x['szo_sorszam']), -int(x['elofordulas']))):
        si, k = int(d['szo_sorszam']), int(d['elofordulas'])
        if si > len(szavak):
            hiba += 1
            continue
        m = szavak[si - 1]
        alap = csere.get(si, m.group(0))
        uj = mem_csere_szoban(alap, k)
        if uj is None or unicodedata.normalize('NFD', uj).replace('ֺ', 'ֹ') == unicodedata.normalize('NFD', alap):
            hiba += 1
            continue
        csere[si] = uj
    for si in sorted(csere, reverse=True):
        m = szavak[si - 1]
        szoveg = szoveg[:m.start()] + csere[si] + szoveg[m.end():]
    return szoveg, hiba


def general(pe_mem=False):
    tab = collections.OrderedDict()
    for r in olvas(TABLA):
        tab.setdefault(r['strong'], []).append(r)
    jav = collections.defaultdict(list)
    for d in olvas(JAV):
        if d['allapot'] == 'javitva' and (d['hiba'] == 'hivatkozas' or (pe_mem and d['hiba'] == 'pe_mem')):
            jav[(d['strong'], d['hiba'])].append(d)
    ki, stat = collections.OrderedDict(), collections.Counter()
    for st, sorok in tab.items():
        if pe_mem and jav.get((st, 'pe_mem')):
            sorok = [dict(x) for x in sorok]
            szerint = collections.defaultdict(list)
            for d in jav[(st, 'pe_mem')]:
                szerint[d['sorszam']].append(d)
            for x in sorok:
                if x['sorszam'] in szerint:
                    x['szoveg'], h = pe_mem_sorban(x['szoveg'], szerint[x['sorszam']])
                    stat['pe_mem_alkalmazva'] += len(szerint[x['sorszam']]) - h
                    stat['pe_mem_sikertelen'] += h
        szoveg, _ = forras_javit.strong_nezet(sorok)
        # hivatkozás: a k-adik egész-token előfordulás cseréje, hátulról előre (a pozíciók ne csússzanak)
        cserek = []
        for d in jav.get((st, 'hivatkozas'), []):
            poz = forras_javit.token_elofordulas(szoveg, d['forras_alak'])
            k = int(d['elofordulas'])
            if k < 1 or k > len(poz):
                stat['hivatkozas_sikertelen'] += 1
                continue
            cserek.append((poz[k - 1], d['forras_alak'], d['javitott_alak']))
        for p, x, y in sorted(cserek, reverse=True):
            szoveg = szoveg[:p] + y + szoveg[p + len(x):]
            stat['hivatkozas_alkalmazva'] += 1
        ki[st] = szoveg
    return ki, tab, stat


def osszevet(nezet, tab, pe_mem):
    with open(TSV, encoding='utf-8', newline='') as f:
        tsv = [s.split('\t') for s in f.read().split('\n')[1:] if s]
    stat, minta = collections.Counter(), collections.defaultdict(list)
    for s in tsv:
        st, t = s[0], ws(s[2])
        if st not in nezet:
            stat['nincs_a_nezetben'] += 1
            continue
        v = ws(nezet[st])
        if v == t:
            stat['azonos'] += 1
            continue
        # a TSV `_N`-je: a tábla gyakorisag-értékei, egyenként egyszer
        t2 = t
        for x in tab[st]:
            for g in filter(None, x['gyakorisag'].split(',')):
                t2 = t2.replace('_' + g, '', 1)
        t2 = ws(t2)
        if v == t2:
            oszt = 'sub'
        elif re.sub(r'\s', '', v) == re.sub(r'\s', '', t2):
            oszt = 'szokoz'
        elif JELOLES_TOREDEK.search(v):
            oszt = 'forras_html'
        elif pe_mem and re.sub(r'\s', '', v.replace(PE, MEM).replace(PE_DAG, MEM_DAG)) == \
                re.sub(r'\s', '', t2.replace(PE, MEM).replace(PE_DAG, MEM_DAG)):
            oszt = 'pe_mem'
        else:
            oszt = 'egyeb'
        stat[oszt] += 1
        if len(minta[oszt]) < 5:
            n = next((i for i, (a, b) in enumerate(zip(v, t2)) if a != b), min(len(v), len(t2)))
            minta[oszt].append('%s poz %d: nézet «%s» | TSV «%s»' % (st, n, v[max(0, n - 30):n + 30], t2[max(0, n - 30):n + 30]))
    return stat, minta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki')
    ap.add_argument('--pe-mem', action='store_true')
    ap.add_argument('--osszevet', action='store_true')
    a = ap.parse_args()
    nezet, tab, stat = general(a.pe_mem)
    print('NÉZET: %d Strong; %s' % (len(nezet), dict(stat)))
    if a.ki:
        if os.path.abspath(a.ki) == os.path.abspath(TSV):
            raise SystemExit('HIBA: a nézet nem írhatja a BDB_teljes_unabridged.tsv-t (DT-F107c (d))')
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write('Strong_padded\tStrong_eredeti\tTeljes_szocikk\n')
            for st, szoveg in nezet.items():
                ered = tab[st][0]['forras'].split(':')[1].split('#')[0]
                f.write('%s\t%s\t%s\n' % (st, ered, szoveg.replace('\t', ' ')))
        print('írva: %s' % a.ki)
    if a.osszevet:
        s, minta = osszevet(nezet, tab, a.pe_mem)
        print('ÖSSZEVETÉS a TSV-vel (%s): %s' % ('+ pe_mem' if a.pe_mem else 'hivatkozás-javítással', dict(s.most_common())))
        for o, l in minta.items():
            for e in l:
                print('  %s\t%s' % (o, e))
    print('proveniencia: scope=F107 nézet | forras=eszkozok/bdb_jelolt/nezet_general.py%s%s | ts=%s' % (
        ' --pe-mem' if a.pe_mem else '', ' --osszevet' if a.osszevet else '', datetime.date.today().isoformat()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
