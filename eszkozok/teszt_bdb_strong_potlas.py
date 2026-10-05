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


ELSO_BEOLVAS = b.tabla_beolvas
POTOLTAK = ('H4725', 'H4123', 'H0747')


def tabla_m2_elott():
    """A tábla az M2 előtti állapotban (a pótolt sorok nélkül): a párosítás újrafuttatható."""
    t = ELSO_BEOLVAS()
    return {k: v for k, v in t.items() if k not in POTOLTAK}


def teszt_h4725_parosul():
    eredeti = b.tabla_beolvas
    b.tabla_beolvas = tabla_m2_elott
    try:
        _h4725_ellenorzes()
    finally:
        b.tabla_beolvas = eredeti


def _h4725_ellenorzes():
    eredmeny, prov, _ = b.parosit('2026-10-05')
    sor = [r for r in eredmeny if r[0]['id'] == 'BDB7372']
    assert len(sor) == 1
    assert sor[0][2] == 'H4725' and sor[0][4] == 'egyertelmu'
    assert 'ts=2026-10-05' in prov


def teszt_kizaras_tablabeli_strong():
    """Nincs egyertelmu pár olyan Strongra, amelynek sora van a táblában vagy H-kulcsa."""
    eredeti = b.tabla_beolvas
    b.tabla_beolvas = tabla_m2_elott
    try:
        bdb, htop, tabla, oshl, un, cim, os_ = b.adatok()
        eredmeny, _, _ = b.parosit('t')
    finally:
        b.tabla_beolvas = eredeti
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


def teszt_tabla_potolt_sorok():
    """A jóváhagyott párok sorai a táblában vannak, kulcsok egyediek, a fej H####. alakú."""
    tabla = b.tabla_beolvas()
    for strong in ('H4725', 'H4123', 'H0747'):
        assert strong in tabla, strong
        assert tabla[strong].split('\t')[2].startswith('H%d. ' % int(strong[1:]))
    with open(b.TABLA, encoding='utf-8', newline='') as f:
        kulcsok = [l.split('\t')[0] for l in f.read().split('\n')[1:] if l]
    assert len(kulcsok) == len(set(kulcsok))
    assert len(kulcsok) == 8090 + 3


def teszt_m2_ujrafuttatas_nem_ir():
    elotte = open(b.TABLA, 'rb').read()
    b.m2()
    assert open(b.TABLA, 'rb').read() == elotte


def _tsv(utvonal):
    with open(utvonal, encoding='utf-8') as f:
        return [l.split('\t') for l in f.read().split('\n') if l][1:]


def teszt_alias():
    sorok = _tsv(b.ALIAS)
    d = {r[0]: r for r in sorok}
    assert d['H0136'][1] == 'H0113' and d['H0136'][2] == 'BDB125'
    assert d['H0341'][1] == 'H0340'
    tabla = b.tabla_beolvas()
    bdb, htop = b.bdb_beolvas()
    for r in sorok:
        assert r[0] not in tabla and r[1].split(',')[0] in tabla
        assert r[6].startswith('scope=') and 'ts=' in r[6]
        # bdb_id-feltétel: a testvér-sor ugyanabból a BDB-szócikkből származik
        assert htop[r[1].split(',')[0]][0] == r[2], r[0]
        assert float(r[5]) >= b.HASONLOSAG_KUSZOB
    assert len(sorok) == 290


def teszt_aramai_nem_kerul_aliasba():
    """H0399 (BDB9297, arámi) testvére a héber H0398: nem alias, hanem elvetett, nyelv=aram."""
    alias = {r[0] for r in _tsv(b.ALIAS)}
    elv = {r[0]: r for r in _tsv(b.ELVETETT)}
    assert 'H0399' not in alias
    assert elv['H0399'][2] == 'aram' and elv['H0399'][1] == 'BDB9297'
    assert 'bdb_id' not in elv['H0399'][5] or 'nem ebből' in elv['H0399'][5]
    # minden másodlagos címke pontosan egy listán áll
    assert alias.isdisjoint(elv)
    assert len(alias) + len(elv) == 529
    # az aliasban az arámi szócikkek csak olyanok, amelyeknek a testvérsora is ugyanabból a szócikkből való
    bdb, htop = b.bdb_beolvas()
    for r in _tsv(b.ALIAS):
        if r[3] == 'aram':
            assert htop[r[1].split(',')[0]][0] == r[2]


def teszt_hatsav_kezi_ellenorzesre():
    elv = {r[0]: r for r in _tsv(b.ELVETETT)}
    for s in ('H3292', 'H3347', 'H5761', 'H6978', 'H8284'):
        assert elv[s][5].startswith('kezi_ellenorzesre'), s
    # a küszöb alatti, de nem határsávos sor továbbra is sima elvetés
    assert elv['H3606'][5].startswith('a bdb_id egyezik, de')
    assert sum(1 for r in elv.values() if r[5].startswith('kezi_ellenorzesre')) == 5
    assert b.HASONLOSAG_KUSZOB == 0.6


def teszt_alias_nincs_tobb_testveres():
    assert all(',' not in r[1] for r in _tsv(b.ALIAS))


def teszt_elvetett_oszlopok():
    for r in _tsv(b.ELVETETT):
        assert r[2] in ('aram', 'heber') and r[5] and r[6].startswith('scope=')


def teszt_stilus_igazit():
    t = '( Exod 29:31 , etc.)^ 1Kgs 8:1 ; Ps 2:1 , Hos 1:1 .'
    u = b.stilus_igazit(t)
    assert u == '(Exod 29:31, etc.)^1Kin 8:1; Psa 2:1, Hosea 1:1.', u


def teszt_potolt_sorok_stilusa():
    tabla = b.tabla_beolvas()
    for strong in ('H4725', 'H4123', 'H0747'):
        sor = tabla[strong]
        for rossz in (' ,', ' ;', ' .', ' )', '( ', '1Kgs', '2Kgs', ' Ps ', 'Hos ', ' Mic ', ' Esth '):
            assert rossz not in sor.split('\t', 2)[2], (strong, rossz)


if __name__ == '__main__':
    n = 0
    for nev, f in sorted(globals().items()):
        if nev.startswith('teszt_') and callable(f):
            f()
            n += 1
            print('OK', nev)
    print('Mind zöld:', n, 'teszt')
