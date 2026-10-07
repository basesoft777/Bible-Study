#!/usr/bin/env python
"""Tesztek a BDB arámi beemeléshez (F72). Futtatás: python eszkozok/teszt_bdb_aram_beemeles.py

A teszt a beemelés előtti és utáni állapotban is fut: az előtti állapotban a szárazfutás
számait és az ütközés-mentességet, az utáni állapotban a 164 + 6 új sort és a bájtazonosságot
(a régi tartalom prefixként egyezik: a `git show origin/main:<fájl>` változattal) ellenőrzi."""
import sys
import os
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_aram_beemeles as M  # noqa: E402
import bdb_strong_potlas as B  # noqa: E402

TS = '2026-10-07'
JELOLT = {'H0004', 'H3769', 'H5013'}


def olvas_bajt(path):
    with open(path, 'rb') as f:
        return f.read()


def main():
    fej, aramok = M.olvas(B.ALIAS)
    assert fej == B.ALIAS_FEJLEC, fej
    fo = olvas_bajt(B.TABLA)
    assert b'\r' not in fo and fo.endswith(b'\n')
    fo_kulcsok = {l.split('\t')[0] for l in fo.decode('utf-8').split('\n')[1:] if l}
    alias_kulcsok = {r[0]: r for r in aramok}
    beemelve = 'H0007' in alias_kulcsok and 'H1753' in fo_kulcsok

    if not beemelve:
        alias, potlas, kimarad, fok = M.szamol(TS)
        assert len(alias) == 164, len(alias)
        assert len(potlas) == 6, len(potlas)
        assert {s for s, _ in kimarad} == JELOLT, kimarad
        assert M.ellenoriz(alias, potlas, kimarad, fok) == []
        assert {p['s'] for p in potlas} == {'H1753', 'H3367', 'H3848', 'H6433', 'H7560', 'H8065'}
        print('szárazfutási számok rendben (164 / 6 / 3); az éles írás még nem történt')
        return

    # utáni állapot
    uj_alias = [r for r in aramok if r[3] == 'aram' and r[6].startswith('scope=konkordancia/BDB_aram_potlas.tsv')]
    assert len(uj_alias) == 164, len(uj_alias)
    assert len(aramok) == 296 + 164, len(aramok)
    for r in uj_alias:
        assert len(r) == 7 and r[2].startswith('BDB') and r[6] and 'ellenorizve' not in r[6].lower()
        assert r[1] in fo_kulcsok, r
        assert r[0] not in fo_kulcsok, r
        assert 0.8 <= float(r[5]) <= 1.0, r
    assert not (JELOLT & (set(alias_kulcsok) | fo_kulcsok)), 'jelölt a táblákban'
    for s in ('H1753', 'H3367', 'H3848', 'H6433', 'H7560', 'H8065'):
        assert s in fo_kulcsok
    sorok = fo.decode('utf-8').split('\n')[:-1]
    assert [l.split('\t')[0] for l in sorok[-6:]] == ['H1753', 'H3367', 'H3848', 'H6433', 'H7560', 'H8065']
    assert all(l.count('\t') == 2 for l in sorok[-6:])
    for path, rel in ((B.TABLA, 'konkordancia/BDB_teljes_unabridged.tsv'), (B.ALIAS, 'konkordancia/BDB_strong_alias.tsv')):
        regi = subprocess.run(['git', 'show', 'origin/main:' + rel], capture_output=True, cwd=B.GYOKER)
        if regi.returncode != 0:
            print('FIGYELEM: az origin/main nem érhető el, a bájtazonosság nem ellenőrizve:', rel)
            continue
        assert olvas_bajt(path).startswith(regi.stdout), 'a régi tartalom nem prefix: ' + rel
    # az elvetett tábla változatlan
    regi = subprocess.run(['git', 'show', 'origin/main:konkordancia/BDB_strong_alias_elvetett.tsv'], capture_output=True, cwd=B.GYOKER)
    if regi.returncode == 0:
        assert olvas_bajt(B.ELVETETT) == regi.stdout
    print('beemelés utáni állapot rendben (164 alias, 6 pótlás, prefix-azonosság)')


if __name__ == '__main__':
    main()
    print('TESZT OK')
