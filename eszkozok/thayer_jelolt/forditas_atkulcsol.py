#!/usr/bin/env python
"""A Thayer-fordítássorok átkulcsolása a szakasztábla újraszámozása után (F186, DT-F186b (b), orkesztrátori döntés, 2026-11-10).

Az F186 a bekezdésen belüli fejnél kettévágja a bekezdést (`bont.py`, K1), ezért az érintett szócikkekben a szakaszok
`sorszam`-a eltolódik. Az `adat/forditasok.tsv` Thayer-sorai (`szotar = Thayer`, `mezo = forditas_hu`, `jelentes_szam =
sz<n>`, nem `elavult`) a régi sorszámon állnak. A szabály soronként:

  * **változatlan** — a `forras_hash` a mai `sz<n>` szakasz hash-e (`thayer_bemenet.szakaszok`): nincs teendő;
  * **átkulcsolás** — a `forras_hash` a Strong mai szakaszai között **pontosan egy** szakasz hash-e (bájtazonos
    forrásszöveg, máshol): `jelentes_szam` sz<n> → sz<m>, a `forras_hash` és a fordítás változatlan;
  * **elavult** — különben (a szöveg megváltozott, vagy a hash többértelmű): `allapot = elavult`, és a sor a forrásbekezdés
    új kezdő szakaszának kulcsára kerül (sz<a régi n. bekezdés első mai szakasza>; a régi `sz<n>` a bekezdés sorszáma volt).
    Ezen a kulcson érvényes fordítás nem állhat, mert annak a szakasznak a szövege új, így kulcsütközés nincs.
A `megjegyzes` mindkét változásnál kiegészül (proveniencia). `kezi` sor nem lehet `elavult` (megáll).

Írás bájtőrző (az `eszkozok/igazolas_migracio.py` mintája): a módosított sorokon kívül minden sor bájtra azonos, írás előtt
összevetve; a kulcsok egyedisége az írás előtt ellenőrizve. Alapmódban csak terv (írás nélkül); `--ir` ír.
  python eszkozok/thayer_jelolt/forditas_atkulcsol.py [--ir] [--lista KI.tsv] [--datum 2026.11.10]
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import bont  # noqa: E402
import kulcs  # noqa: E402
import thayer_bemenet as TB  # noqa: E402

FORDITASOK_UT = os.path.join(bont.GYOKER, 'adat', 'forditasok.tsv')
SZ = re.compile(r'^sz(\d+)$')


def bekezdes_elso(strong, lex=None):
    """{régi bekezdés-sorszám: a bekezdés első mai szakaszának sorszáma} a Strongra."""
    lex = lex if lex is not None else bont.lexikon_beolvas()
    ki = {}
    for i, x in enumerate(bont.szerkezet(lex[strong][1]), 1):
        ki.setdefault(x['bekezdes'], i)
    return ki


def terv(sorok, szakaszok, elso):
    """sorok: [(sorindex, {mezők})] — a fájl minden adatsora; szakaszok(sp) -> [{sorszam, hash}]; elso(sp) -> {bekezdés: sorszám}.
    -> [{'i', 'strong', 'regi', 'uj', 'tipus'}] (tipus: atkulcsol | elavult); SystemExit, ha a terv nem végrehajtható."""
    csoport = collections.defaultdict(list)
    for i, r in sorok:
        if r.get('szotar') == 'Thayer' and r.get('mezo') == 'forditas_hu' and SZ.match(r.get('jelentes_szam', '')):
            csoport[kulcs.strong_pad(r['strong'])].append((i, r))
    ki = []
    for sp in sorted(csoport):
        aktiv = [(i, r) for i, r in csoport[sp] if r.get('allapot') != 'elavult']
        if not aktiv:
            continue
        sz = szakaszok(sp) or []
        hash_itt = {x['sorszam']: x['hash'] for x in sz}
        hol = collections.defaultdict(list)
        for x in sz:
            hol[x['hash']].append(x['sorszam'])
        valtozas = []
        for i, r in aktiv:
            n = int(SZ.match(r['jelentes_szam']).group(1))
            fh = r.get('forras_hash', '')
            if hash_itt.get(n) == fh:
                continue
            if len(hol.get(fh, [])) == 1:
                valtozas.append({'i': i, 'strong': sp, 'regi': n, 'uj': hol[fh][0], 'tipus': 'atkulcsol'})
                continue
            e = elso(sp)
            if n not in e:
                raise SystemExit('%s sz%d: a régi sorszám nem bekezdés a mai forrásban — megállok' % (sp, n))
            if r.get('allapot') == 'kezi':
                raise SystemExit('%s sz%d: védett kezi sor lenne elavult — megállok' % (sp, n))
            valtozas.append({'i': i, 'strong': sp, 'regi': n, 'uj': e[n], 'tipus': 'elavult'})
        # a végső kulcsok egyedisége a Strongon belül (az elavult sorokkal együtt)
        mozdul = {v['i']: v['uj'] for v in valtozas}
        vegso = collections.Counter()
        for i, r in csoport[sp]:
            vegso[mozdul.get(i, int(SZ.match(r['jelentes_szam']).group(1)))] += 1
        dupla = sorted(k for k, c in vegso.items() if c > 1)
        if dupla:
            raise SystemExit('%s: kulcsütközés a terv után: %s — megállok' % (sp, ['sz%d' % k for k in dupla]))
        for v in valtozas:
            if v['tipus'] == 'atkulcsol':
                assert hash_itt[v['uj']] == dict(csoport[sp])[v['i']]['forras_hash']  # csak azonos hash-nél
        ki.extend(valtozas)
    return ki


def beolvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        szoveg = f.read()
    assert szoveg.endswith('\n'), 'a forditasok.tsv nem sortöréssel végződik'
    sorok = szoveg.split('\n')[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].split('\t')
    adat = [(i, dict(zip(fej, s.split('\t')))) for i, s in enumerate(sorok) if i > fej_i and s and not s.startswith('#')]
    return szoveg, sorok, fej, adat


def alkalmaz(sorok, fej, valtozasok, datum):
    """-> az új sorlista; csak a `valtozasok` sorai változnak."""
    i_jsz, i_all, i_megj = fej.index('jelentes_szam'), fej.index('allapot'), fej.index('megjegyzes')
    uj = list(sorok)
    for v in valtozasok:
        m = uj[v['i']].split('\t')
        assert m[i_jsz] == 'sz%d' % v['regi']
        m[i_jsz] = 'sz%d' % v['uj']
        # A megjegyzés szövege bájtra az, amit az F186.9 a forditasok.tsv-be írt (ELLENOR_F186 2e): a helyőrzőt az adatban a
        # szamkiosztas merge-kor cseréli, a .py-ban nem; ezért a két sor szándékosan történeti literál (e32-kihagy).
        if v['tipus'] == 'atkulcsol':
            jegy = 'F186 (%s): átkulcsolva sz%d → sz%d, azonos forras_hash (a szakaszok újraszámozása; DT-F186b)' % (datum, v['regi'], v['uj'])  # e32-kihagy
        else:
            m[i_all] = 'elavult'
            jegy = ('F186 (%s): elavult — a forrásbekezdés szövege a szakasztáblában megváltozott (bekezdésen belüli fej vagy hamis '
                    'fej); sz%d → sz%d, a bekezdés új kezdő szakasza (DT-F186b)' % (datum, v['regi'], v['uj']))  # e32-kihagy
        m[i_megj] = '; '.join(x for x in (m[i_megj], jegy) if x)
        uj[v['i']] = '\t'.join(m)
    return uj


def ellenoriz_iras(regi, uj, valtozasok, fej):
    """Írás előtti összevetés: a nem módosított sorok bájtra azonosak, a sorszám és a mezőszám változatlan, a kulcsok egyediek."""
    if len(regi) != len(uj):
        raise SystemExit('a sorok száma változna — megállok')
    erintett = {v['i'] for v in valtozasok}
    for i, (a, b) in enumerate(zip(regi, uj)):
        if i not in erintett and a != b:
            raise SystemExit('váratlan eltérés a %d. sorban — megállok' % (i + 1))
        if i in erintett and len(a.split('\t')) != len(b.split('\t')):
            raise SystemExit('mezőszám-eltérés a %d. sorban — megállok' % (i + 1))
    kulcsok = collections.Counter(tuple(s.split('\t')[:5]) for s in uj if s and not s.startswith('#'))
    dupla = [k for k, c in kulcsok.items() if c > 1]
    if dupla:
        raise SystemExit('duplikált kulcs az írás után: %s — megállok' % dupla[:3])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    ap.add_argument('--lista')
    ap.add_argument('--datum', default='2026.11.10')
    ap.add_argument('--forditasok', default=FORDITASOK_UT)
    a = ap.parse_args()
    szoveg, sorok, fej, adat = beolvas(a.forditasok)
    lex = bont.lexikon_beolvas()
    v = terv(adat, TB.szakaszok, lambda sp: bekezdes_elso(sp, lex))
    db = collections.Counter(x['tipus'] for x in v)
    print('átkulcsolás: %d; elavult: %d; érintett Strong: %d' % (db['atkulcsol'], db['elavult'], len({x['strong'] for x in v})))
    if a.lista:
        with open(a.lista, 'w', encoding='utf-8', newline='\n') as f:
            f.write('strong\tregi\tuj\ttipus\n')
            for x in v:
                f.write('%s\tsz%d\tsz%d\t%s\n' % (x['strong'], x['regi'], x['uj'], x['tipus']))
    uj = alkalmaz(sorok, fej, v, a.datum)
    ellenoriz_iras(sorok, uj, v, fej)
    if not a.ir:
        print('terv (írás nélkül); --ir ír')
        return 0
    with open(a.forditasok, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(uj) + '\n')
    print('írva: %s' % a.forditasok)
    return 0


if __name__ == '__main__':
    sys.exit(main())
