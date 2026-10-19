#!/usr/bin/env python
"""A szakasztábla szerkezetének ellenőrzése (F107, 4. lépés): aranyminta, seed-101, korpusz (a mai szeletelő).

Útvonal-normalizálás az összevetéshez (a tábla 2.30-as formátuma → a 2.28/2.29 formátuma): a nagybetűs csoport (`.A`) és a
zárójeles 4. szint elhagyva, a záró `-` szintek levágva (`Qal/-/-` → `Qal`, `-/1/-` → `-/1`); a szeletelő `tagolatlan`-ja = `fej`;
a tábla `cim` sora = `fej`.

  --arany     adat/bdb_aranyminta.tsv: a `torzs` / `jelentes` / `alpont` csomópontok (a `csoport` és a `szakasz` szintet a tábla
              nem bontja: a csoport a #103 hatóköre) — van-e a Strongnak olyan táblasora, amelynek a normalizált útvonala és a `resz`-e egyezik
  --seed101   a #99 seed-101 13 szeletelő-hibájának helye (naplok/BDB_SZELETELO_M2_seed101_iteletek.md, a várt útvonallal)
  --korpusz   adat/bdb_vers_jelentes.tsv minden sora: a `nyers` hivatkozás a tábla szövegében, a Strong sorainak sorrendjében
              keresve (kurzorral); a megtalált sor útvonala ↔ a szeletelő útvonala
  --lista N   az első N eltérés kiírása (minden módban)

Csak olvas. TSV: split('\\t').
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
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
ARANY = os.path.join(GYOKER, 'adat', 'bdb_aranyminta.tsv')
BVJ = os.path.join(GYOKER, 'adat', 'bdb_vers_jelentes.tsv')

# (hely, strong, horgony a sorban, hivatkozás, várt resz, várt útvonal) — a seed-101 ítéleti tábla „várt” oszlopa szerint;
# a szakasz-szintű homonimaszám (M117 „I”, M146 „I”) a táblában nem útvonal-elem, ezért itt nem szerepel
SEED101 = [
    ('M028', 'H7379', 'especially dispute', '25:1', '', '-/3'),
    ('M031', 'H5117', 'leave or bequeath', 'Eccl 2:18', '', "Hiph'il/2"),
    ('M043', 'H8057', '(especially Psalms Chronicles) religious', 'Joel 1:16', '', '-/2'),
    ('M102', 'H0559', 'Say (subject', '1Chr 17:4', '', 'Qal/1'),
    ('M117', 'H0539', 'verified, confirmed', '93:5', '', "Niph'al/4"),
    ('M130', 'H8478', 'as preposition', 'Hab 3:16', 'II', '-/2/a'),
    ('M140', 'H7626', 'rod, staff', '2Sam 7:14', '', '-/1/a'),
    ('M146', 'H7227', 'as adverb much', '2Sam 22:15', '', '-/1/g'),
    ('M162', 'H3318', 'go or come out', 'Psa 114:1', '', 'Qal/1/a'),
    ('M203', 'H3068', 'is noteworthy', 'Judg 6:10', 'II', '-/2/a'),
    ('M236', 'H5437', 'make a round', '2Sam 5:23', '', 'Qal/2/c'),
    ('M238', 'H5608', "king's official", 'Isa 36:3', '', '-/1/b'),
    ('M243', 'H1129', '= rebuild', 'Ezra 1:3', '', 'Qal/1/i'),
]


# DT-F107g (b): a nyers forrásban (DictBDB.json ÉS BDB.lexicon) igazolt forráshibás csomópontok — külön számolva; mindegyiknek
# kézi sora van az adat/bdb_forras_javitas.tsv-ben (forras_javit.py KEZI; naplok/F107_BDB_JELOLT_SZOVEG_naplo.md 4.6)
FORRAS_HIBA_ARANY = {
    ('H0559', 'Qal'), ('H0559', 'Qal/1'), ('H0559', 'Qal/2'), ('H0559', 'Qal/3'), ('H0559', 'Qal/4'),   # „Qal” jelöletlen; „1” (JSON)
    ('H4900', 'Qal/6'), ('H4900', 'Qal/7'),                                                            # „Niph`al 6.” hamis fej
    ('H1242', '-/1/g'), ('H1242', '-/1/h'),                                                            # „2. g.” téves „2.”
}
FORRAS_HIBA_SEED = {'M102', 'M117', 'M162'}


def norm(ut):
    if ut in ('cim', 'fej', 'tagolatlan', ''):
        return 'fej'
    resz = ut.split('/')
    resz[0] = resz[0].split('.')[0]
    resz = resz[:3]
    while len(resz) > 1 and resz[-1] == '-':
        resz.pop()
    return '/'.join(resz)


def olvas(ut, fejsorok):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[fejsorok].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[fejsorok + 1:] if s]


def tabla_strongonkent():
    ki = collections.OrderedDict()
    for d in olvas(TABLA, 2):
        ki.setdefault(d['strong'], []).append(d)
    return ki


def arany(tab, lista):
    stat, elter = collections.Counter(), []
    for d in olvas(ARANY, 2):
        if d['szint'] not in ('torzs', 'jelentes', 'alpont'):
            continue
        ut = d['utvonal']
        sorok = tab.get(d['strong'], [])
        # a sor útvonalának minden előtagja csomópont: a kombinált fej („1. a.”) a jelentést és az alpontot is megnyitja
        utak = set()
        for x in sorok:
            n = norm(x['utvonal']).split('/')
            for k in range(1, len(n) + 1):
                elotag = n[:k]
                while len(elotag) > 1 and elotag[-1] == '-':
                    elotag = elotag[:-1]
                utak.add((x['resz'], '/'.join(elotag)))
            if len(n) > 2 and n[1] == '-' and n[2] != '-':
                # SEMA 2.28: a jelentés nélküli alpont az aranymintában `-/a` (`Qal/a`) alakú, a táblában `-/-/a`
                utak.add((x['resz'], '%s/%s' % (n[0], n[2])))
        kulcs = 'szamozatlan' if re.search(r'/-\d', ut) else d['szint']
        if (d['resz'], ut) in utak:
            stat[(kulcs, 'egyezik')] += 1
        else:
            stat[(kulcs, 'hianyzik')] += 1
            elter.append((d['strong'], d['szakasz'], d['resz'], ut, d['szint'], d['jel']))
    ossz = sum(stat.values())
    egy = sum(v for (k, e), v in stat.items() if e == 'egyezik')
    print('ARANY: %d csomópont; egyezik %d (%.1f%%); %s' % (ossz, egy, 100.0 * egy / max(1, ossz), dict(sorted(stat.items()))))
    nsz = sum(v for (k, e), v in stat.items() if k != 'szamozatlan')
    esz = sum(v for (k, e), v in stat.items() if k != 'szamozatlan' and e == 'egyezik')
    print('  a számozatlan jelentés (`-1`, `-2`; a táblában fej nélkül nem bontható) nélkül: %d / %d (%.1f%%)' % (esz, nsz, 100.0 * esz / max(1, nsz)))
    fh = sum(1 for e in elter if (e[0], e[3]) in FORRAS_HIBA_ARANY)
    print('  a forras_hiba csomópontok (%d, mind hiányzó) nélkül: %d / %d (%.1f%%)' % (
        fh, egy, ossz - fh, 100.0 * egy / max(1, ossz - fh)))
    for e in elter[:lista]:
        print('  hiányzik: %s szakasz=%s resz=%s %s (%s, jel %s)' % e)


def seed101(tab):
    jo = 0
    for hely, st, horgony, ref, vresz, vut in SEED101:
        sorok = tab.get(st, [])
        i = next((k for k, x in enumerate(sorok) if horgony in x['szoveg']), None)
        talalt = None
        if i is not None:
            for x in sorok[i:]:
                if ref in x['szoveg']:
                    talalt = x
                    break
        if talalt is None:
            print('  %s %s: a hely nem található (horgony %r, hiv %r)' % (hely, st, horgony, ref))
            continue
        ok = talalt['resz'] == vresz and norm(talalt['utvonal']) == vut
        jo += ok
        print('  %s %s: tábla resz=%s %s (sor %s, %s) | várt resz=%s %s → %s' % (
            hely, st, talalt['resz'] or '-', talalt['utvonal'], talalt['sorszam'], talalt['illesztes'], vresz or '-', vut,
            'EGYEZIK' if ok else 'ELTÉR'))
    print('SEED101: %d / %d egyezik; a forras_hiba helyek (%s) nélkül: %d / %d' % (
        jo, len(SEED101), ', '.join(sorted(FORRAS_HIBA_SEED)), jo, len(SEED101) - len(FORRAS_HIBA_SEED)))


def korpusz(tab, lista):
    bvj = olvas(BVJ, 2)
    stat, minta = collections.Counter(), collections.defaultdict(list)
    kurzor = {}
    szoveg = {}
    for st, sorok in tab.items():
        darabok, hatar, p = [], [], 0
        for x in sorok:
            t = ' '.join(y for y in (x['jel'], x['szoveg']) if y) + ' '
            darabok.append(t)
            hatar.append((p, p + len(t), x))
            p += len(t)
        szoveg[st] = (''.join(darabok), hatar)
    for d in bvj:
        st = d['strong']
        if d['szurt'] == '1':
            stat['szurt_kihagyva'] += 1
            continue
        if st not in szoveg:
            stat['nincs_a_tablaban'] += 1
            continue
        t, hatar = szoveg[st]
        nyers = d['nyers'].strip()
        if nyers.startswith(','):
            nyers = nyers.lstrip(', ').strip()
        k = t.find(nyers, kurzor.get(st, 0))
        if k < 0 or not nyers:
            stat['nem_talalt'] += 1
            minta['nem_talalt'].append((st, d['sorszam'], d['nyers'], d['utvonal'], ''))
            continue
        kurzor[st] = k + len(nyers)
        x = next(h[2] for h in hatar if h[0] <= k < h[1])
        tu, su = norm(x['utvonal']), norm(d['utvonal'])
        if tu == su and x['resz'] == d['resz']:
            stat['egyezik'] += 1
            continue
        if tu == su:
            oszt = 'csak_resz'
        elif su == 'fej':
            oszt = 'szeletelo_fej_tabla_tagolt'
        elif tu == 'fej':
            oszt = 'tabla_fej_szeletelo_tagolt'
        else:
            ta, sa = tu.split('/'), su.split('/')
            if ta[0] != sa[0]:
                oszt = 'torzs_elter'
            elif len(ta) > 1 and len(sa) > 1 and ta[1] != sa[1]:
                oszt = 'jelentes_elter'
            else:
                oszt = 'alpont_elter'
        stat[oszt] += 1
        minta[oszt].append((st, d['sorszam'], d['nyers'], 'szeletelő %s %s' % (d['resz'] or '-', d['utvonal']),
                            'tábla %s %s (%s)' % (x['resz'] or '-', x['utvonal'], x['illesztes'])))
    ossz = sum(v for k, v in stat.items() if k not in ('szurt_kihagyva', 'nincs_a_tablaban'))
    print('KORPUSZ: %d nem szűrt hivatkozás a tábla Strongjain; %s' % (ossz, dict(stat.most_common())))
    print('  egyezik: %.1f%%' % (100.0 * stat['egyezik'] / max(1, ossz)))
    for oszt, l in minta.items():
        for e in l[:lista]:
            print('  %s\t%s' % (oszt, '\t'.join(e)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arany', action='store_true')
    ap.add_argument('--seed101', action='store_true')
    ap.add_argument('--korpusz', action='store_true')
    ap.add_argument('--lista', type=int, default=0)
    a = ap.parse_args()
    tab = tabla_strongonkent()
    if a.arany:
        arany(tab, a.lista)
    if a.seed101:
        seed101(tab)
    if a.korpusz:
        korpusz(tab, a.lista)
    print('proveniencia: scope=F107 4. lépés | forras=eszkozok/bdb_jelolt/szerkezet_osszevet.py%s%s%s | ts=%s' % (
        ' --arany' if a.arany else '', ' --seed101' if a.seed101 else '', ' --korpusz' if a.korpusz else '',
        datetime.date.today().isoformat()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
