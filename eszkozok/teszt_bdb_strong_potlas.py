#!/usr/bin/env python
"""Tesztek: eszkozok/bdb_strong_potlas.py (F57, K4)."""
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_strong_potlas as b


def szocikk(bid, cim, gl, nyelv='heber', stub=False):
    return {'id': bid, 'cimkek': [], 'nyelv': nyelv, 'cimszavak': [cim], 'homonima': '',
            'szofaj': 'noun', 'glosszak': gl, 'gyokstub': stub}


def jelolt(strong, lemma, defen, nyelv='heber'):
    return {'strong': strong, 'nyelv': nyelv, 'lemma': lemma, 'def_en': defen, 'bdb_id': 'x'}


def teszt_norm_holem_waw():
    assert b.norm('מָקוֺם') == b.norm('מָקוֹם')


def teszt_norm_kantillacio():
    assert b.norm('אֲבִיָּ֫הוּ') == b.norm('אֲבִיָּהוּ')


def teszt_h4725_parosul():
    eredmeny, prov, _ = b.parosit('2026-10-05')
    sor = [r for r in eredmeny if r[0]['id'] == 'BDB7372']
    assert len(sor) == 1
    assert sor[0][2] == 'H4725' and sor[0][4] == 'egyertelmu'
    assert 'ts=2026-10-05' in prov


def teszt_kizaras_tablabeli_strong():
    """Nincs egyertelmu pár olyan Strongra, amelynek sora van a táblában vagy H-kulcsa."""
    bdb, htop, tabla, oshl, un, cim, os_ = b.adatok()
    eredmeny, _, _ = b.parosit('t')
    for e, cs, s, lem, st, ind in eredmeny:
        for x in [y for y in s.split(',') if y]:
            assert x not in tabla and x not in htop, x
        assert not e['cimkek'], e['id']
    assert 'H0136' not in {r[2] for r in eredmeny}


def teszt_homonimia_glossza_dont():
    bdb = {}
    un = [szocikk('BDB1', 'אֵב', ['freshness']), szocikk('BDB2', 'אֵב', ['fruit'])]
    jel = {'H0003': jelolt('H0003', 'אֵב', 'freshness'), 'H0004': jelolt('H0004', 'אֵב', 'fruit')}
    for e in un:
        bdb[e['id']] = e
    er = {r[0]['id']: r for r in b.parosit_mag(bdb, un, jel)}
    assert er['BDB1'][2] == 'H0003' and er['BDB1'][4] == 'egyertelmu'
    assert er['BDB2'][2] == 'H0004' and er['BDB2'][4] == 'egyertelmu'


def teszt_homonimia_marad_jelolt():
    bdb = {}
    un = [szocikk('BDB1', 'אֵב', ['thing']), szocikk('BDB2', 'אֵב', ['stuff'])]
    jel = {'H0003': jelolt('H0003', 'אֵב', 'item'), 'H0004': jelolt('H0004', 'אֵב', 'object')}
    for e in un:
        bdb[e['id']] = e
    er = b.parosit_mag(bdb, un, jel)
    assert all(r[4] == 'tobb_jelolt' for r in er), [r[4] for r in er]


def teszt_nincs_par_es_gyokstub():
    bdb = {}
    un = [szocikk('BDB1', 'אֵב', ['x'], stub=True), szocikk('BDB2', 'זזז', ['y'])]
    jel = {'H0003': jelolt('H0003', 'אֵב', 'x')}
    for e in un:
        bdb[e['id']] = e
    er = {r[0]['id']: r for r in b.parosit_mag(bdb, un, jel)}
    assert er['BDB1'][4] == 'nincs_par' and er['BDB2'][4] == 'nincs_par'


def teszt_nyelv_kulonvalik():
    bdb = {}
    un = [szocikk('BDB1', 'אֵב', ['fruit'], nyelv='arameus')]
    jel = {'H0003': jelolt('H0003', 'אֵב', 'fruit', nyelv='heber')}
    bdb['BDB1'] = un[0]
    assert b.parosit_mag(bdb, un, jel)[0][4] == 'nincs_par'


if __name__ == '__main__':
    n = 0
    for nev, f in sorted(globals().items()):
        if nev.startswith('teszt_') and callable(f):
            f()
            n += 1
            print('OK', nev)
    print('Mind zöld:', n, 'teszt')
