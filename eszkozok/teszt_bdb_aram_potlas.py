#!/usr/bin/env python
"""Tesztek a BDB_aram_potlas.tsv-hez (F66, K1-K4). Futtatás: python eszkozok/teszt_bdb_aram_potlas.py"""
import sys
import os
import re
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_aram_potlas as A  # noqa: E402
import bdb_strong_potlas as B  # noqa: E402


def olvas(path):
    with open(path, encoding='utf-8', newline='') as f:
        sorok = [l.split('\t') for l in f.read().split('\n') if l]
    return sorok[0], sorok[1:]


def main():
    fej, sorok = olvas(A.KIMENET)
    assert fej == A.FEJLEC, fej
    assert all(len(r) == len(fej) for r in sorok)
    d = {r[0]: dict(zip(fej, r)) for r in sorok}
    assert len(d) == len(sorok), 'duplikált Strong'

    # K1: minden elvetett arámi sor szerepel, érvényes állapottal
    elv = {r['masodlagos_strong']: r for r in A.elvetett_aram()}
    assert len(elv) == 173, len(elv)
    assert set(elv) == set(d), 'a két halmaz eltér'
    for s, r in d.items():
        assert r['allapot'] in A.ALLAPOTOK, (s, r['allapot'])
        assert r['bdb_id'] == elv[s]['bdb_id'] or s in A.KEZI
        assert r['indok'] and r['proveniencia'].startswith(('scope=', 'manual')), s

    # K2: az egyértelmű sor szövege a BDB.lexicon saját szócikkéből jön
    for s, r in d.items():
        if r['allapot'] == 'egyertelmu':
            e = A.szocikk_elemzes(r['bdb_id'])
            assert r['Teljes_szocikk'].endswith(e['szoveg']), s
            assert not e['gyokstub'] and not e['jegyzet'], s

    # K4: H0004 — nem szócikk, jelölt marad, szöveg nincs
    assert d['H0004']['allapot'] == 'cimke_reszleges' and d['H0004']['Teljes_szocikk'] == ''
    # H0007: egyértelmű, fej: "H7. abad ..."
    assert d['H0007']['allapot'] == 'egyertelmu'
    assert d['H0007']['Teljes_szocikk'].startswith('H7. abad '), d['H0007']['Teljes_szocikk'][:20]
    # H3606: a testvérsor más szócikk (H6903), de a BDB9612 saját szócikke
    assert d['H3606']['allapot'] == 'egyertelmu' and d['H3606']['bdb_id'] == 'BDB9612'
    assert d['H3606']['Teljes_szocikk'].startswith('H3606. kol ')
    # csonk szócikk jelöltként marad (gyök-hivatkozás), szöveg megvan, de nem egyertelmu
    assert d['H3769']['allapot'] == 'csonk' and d['H5013']['allapot'] == 'csonk'
    # a címszó/glossza-eltérés nem kerül be egyértelműként
    # H2298: kézi, felhasználó által elfogadott hozzárendelés a BDB9285-höz (חַד); proveniencia manual
    r = d['H2298']
    assert r['allapot'] == 'kezi_elfogadott' and r['bdb_id'] == 'BDB9285'
    assert r['proveniencia'].startswith('manual'), r['proveniencia']
    assert r['indok'].startswith('forráscímke: H259 (téves)')
    assert r['Teljes_szocikk'].startswith('H2298. had ')
    assert A.szocikk_elemzes('BDB9285')['szoveg'] and r['Teljes_szocikk'].endswith(A.szocikk_elemzes('BDB9285')['szoveg'])
    # nincs ütközés: a BDB9285 egyetlen alias/elvetett/más sorban sem szerepel
    for f in ('BDB_strong_alias.tsv', 'BDB_strong_alias_elvetett.tsv', 'BDB_strong_potlas.tsv'):
        assert 'BDB9285' not in open(os.path.join(A.GYOKER, 'konkordancia', f), encoding='utf-8').read(), f
    assert sum(1 for x in d.values() if x['bdb_id'] == 'BDB9285') == 1
    # H0004 továbbra is jelölt
    assert d['H0004']['allapot'] == 'cimke_reszleges'
    # a szúrópróba-kivonat arámi helyszűrője
    assert not A.aram_hely('Jer 48:47') and not A.aram_hely('Jer 51:64') and A.aram_hely('Dan 7:28') and A.aram_hely('Ezra 6:17')

    # a fej formátuma egyezik a fő táblával: "H<n>. <átírás> ..."
    _, fo = olvas(B.TABLA)
    fo_re = re.compile(r'^H\d+[a-z]?\. \S+ ')
    minta = [r[2] for r in fo if r[0] in ('H0002', 'H0001')]
    assert all(fo_re.match(m) for m in minta), minta
    for s, r in d.items():
        if r['allapot'] not in ('nincs_szoveg', 'cimke_reszleges'):
            assert fo_re.match(r['Teljes_szocikk']), (s, r['Teljes_szocikk'][:30])
            assert r['Teljes_szocikk'].startswith('H%d. ' % int(s[1:5])), s
            assert '\t' not in r['Teljes_szocikk']

    # K3: a fő tábla és az alias-táblák nem változtak a git szerint
    gyoker = A.GYOKER
    for f in ('konkordancia/BDB_teljes_unabridged.tsv', 'konkordancia/BDB_strong_alias.tsv',
              'konkordancia/BDB_strong_alias_elvetett.tsv'):
        ki = subprocess.run(['git', 'diff', '--quiet', 'origin/main', '--', f], cwd=gyoker)
        assert ki.returncode == 0, 'változott: ' + f
    print('teszt_bdb_aram_potlas: minden teszt zöld (%d sor)' % len(d))


if __name__ == '__main__':
    main()
