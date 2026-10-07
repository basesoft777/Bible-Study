#!/usr/bin/env python
"""A #38 (BDB_FORDITAS) fordítási sorrendjének újragenerálása a bővült BDB-táblából (F72, ⛔ 4).

A `naplok/BDB_FORDITAS_sorrend.tsv` kész előtagját (a `teljes` fordítású sorok, a sorszámokkal és adagokkal)
változatlanul hagyja; a hátralévő sorokat (a régi hátralék + a fő tábla azon Strongjai, amelyek a sorrendben
még nincsenek és nincs kész fordításuk: az F57 3 pótolt sora és az F72 6 arámi pótlása) a #38 M0 szabálya szerint
rendezi (TAHOT-gyakoriság csökkenő, egyenlőnél Strong-szám), a kész előtag utáni sorszámtól számozza, és az adagokat
az M0 `adagol` logikájával (ADAG_CEL) osztja, a következő adag kezdetétől. Az alias-sorok nem kapnak sort: a
testvérsor fordítása lefedi őket.

  python eszkozok/bdb_sorrend_ujragen.py --nem-ir   # szárazfutás: jelentés
  python eszkozok/bdb_sorrend_ujragen.py            # ír: naplok/BDB_FORDITAS_sorrend.tsv

Önellenőrzés: új sor nélkül a hátralék újrarendezése a meglévő sorrendet kell hogy adja (a gyakoriság és az
adagok változatlanok).
TSV: split('\t') / '\t'.join().
"""
import sys
import os
import argparse
import importlib.util

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = importlib.util.spec_from_file_location('bdb_forditas_m0', os.path.join(REPO, 'naplok', 'BDB_FORDITAS_M0.py'))
M0 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(M0)

FEJ_SOR = ('# F38 M0 -- generalja: python naplok/BDB_FORDITAS_M0.py; gyakorisag: konkordancia/TAHOT_kivonat.tsv '
           '(Strong-cimkenkenti sorszam); kesz sorok kimaradnak')
UJ_FEJ_SOR = FEJ_SOR + ('; ujragenerálva (F72): a kesz elotag valtozatlan, a hatralek a bovult BDB-tablabol '
                        '(eszkozok/bdb_sorrend_ujragen.py)')


def beolvas():
    with open(M0.SORREND_UT, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[1].split('\t')
    rows = [dict(zip(fej, l.split('\t'))) for l in sorok[2:] if l]
    return sorok[0], fej, rows


def szamol():
    _, fej, rows = beolvas()
    kesz = M0.kesz_strongok()
    elotag = []
    for r in rows:
        if r['strong'] in kesz:
            elotag.append(r)
        else:
            break
    hatralek = rows[len(elotag):]
    assert not any(r['strong'] in kesz for r in hatralek), 'kész sor a hátralékban: az előtag nem összefüggő'
    bdb = M0.bdb_betolt()
    tahot = M0.gyakorisag(M0.TAHOT_UT, 'Strong-szám')
    regi = {r['strong'] for r in rows}
    uj = sorted(s for s in bdb if s not in regi and s not in kesz)
    jelenlegi = [{'strong': r['strong'], 'gyakorisag': int(r['gyakorisag']), 'karakter': int(r['karakter'])} for r in hatralek]
    uj_sorok = [{'strong': s, 'gyakorisag': tahot.get(s, 0), 'karakter': len(bdb[s])} for s in uj]
    kezd_adag = int(hatralek[0]['adag']) if hatralek else int(elotag[-1]['adag']) + 1
    return fej, elotag, jelenlegi, uj_sorok, kezd_adag


def rendez(sorok, kezd_sorszam, kezd_adag):
    sorok = sorted(sorok, key=lambda s: (-s['gyakorisag'], s['strong']))
    adag, osszeg = kezd_adag, 0
    for i, s in enumerate(sorok, kezd_sorszam):
        if osszeg > 0 and osszeg + s['karakter'] > M0.ADAG_CEL:
            adag += 1
            osszeg = 0
        s['sorszam'], s['adag'] = i, adag
        osszeg += s['karakter']
    return sorok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nem-ir', action='store_true')
    a = ap.parse_args()
    fej, elotag, jelenlegi, uj_sorok, kezd_adag = szamol()
    kezd = len(elotag) + 1
    _, _, rows = beolvas()
    regi_hatralek = rows[len(elotag):]
    # önellenőrzés: új sor nélkül ugyanazt kell kapni
    proba = rendez([dict(s) for s in jelenlegi], kezd, kezd_adag)
    eltres = [(p['strong'], r['strong']) for p, r in zip(proba, regi_hatralek)
              if (p['strong'], str(p['adag']), str(p['sorszam'])) != (r['strong'], r['adag'], r['sorszam'])]
    print('önellenőrzés (új sor nélkül): %d eltérés a meglévő hátralékhoz képest' % len(eltres))
    if eltres:
        print('  első eltérések:', eltres[:5])
        raise SystemExit('megállok: az újrarendezés nem reprodukálja a meglévő sorrendet')
    uj = rendez(jelenlegi + uj_sorok, kezd, kezd_adag)
    print('kész előtag: %d sor; hátralék: %d + új %d = %d' % (len(elotag), len(jelenlegi), len(uj_sorok), len(uj)))
    for s in uj_sorok:
        t = next(x for x in uj if x['strong'] == s['strong'])
        print('  új: %s gyakoriság %d, karakter %d -> sorszám %d, adag %d' % (s['strong'], s['gyakorisag'], s['karakter'], t['sorszam'], t['adag']))
    print('adagok: ' + '; '.join('%d: %d sor' % (ad, sum(1 for x in uj if x['adag'] == ad)) for ad in sorted({x['adag'] for x in uj})))
    if not a.nem_ir:
        with open(M0.SORREND_UT, 'w', encoding='utf-8', newline='\n') as f:
            f.write(UJ_FEJ_SOR + '\n' + '\t'.join(fej) + '\n')
            for r in elotag:
                f.write('\t'.join(r[m] for m in fej) + '\n')
            for s in uj:
                f.write('\t'.join(str(s[m]) for m in fej) + '\n')
        print('irva: naplok/BDB_FORDITAS_sorrend.tsv (%d sor)' % (len(elotag) + len(uj)))


if __name__ == '__main__':
    main()
