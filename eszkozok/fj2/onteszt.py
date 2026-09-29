#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
onteszt.py -- az F06 szkriptek halozat nelkuli onellenorzese kepzelt (szintetikus) adaton.
A szintetikus adat CSAK a logika tesztelesere szolgal; belole szam a jelentesbe nem kerul.
A kimenetek ideiglenes konyvtarba mennek (kozos.NAPLOK atiranyitva), a repo nem valtozik.

    python eszkozok/fj2/onteszt.py
"""

import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb  # noqa: E402
import licenc  # noqa: E402
import macula  # noqa: E402


def git_repo(mappa):
    subprocess.run(['git', 'init', '-q'], cwd=mappa, check=True)
    subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', 'add', '-A'], cwd=mappa, check=True)
    subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', 't'], cwd=mappa, check=True)


def teszt_kapu():
    szoveg = 'Licensed under\n  CC BY 4.0 by Foo.'
    ok = {'licenc_tipus': 'CC BY 4.0', 'kereskedelmi_hasznalat': 'igen', 'szarmaztatott_mu': 'engedelyezett',
          'forrasmegjeloles_kell': 'igen', 'kozkincs_allitas': 'nincs', 'idezet': 'Licensed under CC BY 4.0'}
    assert licenc.kapu(ok, szoveg)[0]
    rossz = dict(ok, idezet='Licensed under CC BY 3.0')
    assert not licenc.kapu(rossz, szoveg)[0]
    ures = dict(ok, idezet='', licenc_tipus='nincs_adat', kereskedelmi_hasznalat='nem_derul_ki',
                szarmaztatott_mu='nem_derul_ki', forrasmegjeloles_kell='nem_derul_ki')
    assert licenc.kapu(ures, szoveg)[0]
    assert not licenc.kapu(dict(ok, idezet=''), szoveg)[0]
    assert not licenc.kapu({'licenc_tipus': 'x'}, szoveg)[0]


def teszt_bsb_elemzes():
    adat = {'eng': {'1': [['In the beginning', 'H7225'], ['God', 'H430'], ['x', '']], '2': [['a', 'H0001']]}}
    assert bsb.bsb_vers_strongok(adat) == {1: {7225, 430}, 2: {1}}


def teszt_macula(tmp):
    munka = os.path.join(tmp, 'munka')
    repo = os.path.join(munka, 'macula-hebrew')
    lf = os.path.join(repo, 'WLC', 'lowfat')
    os.makedirs(lf)
    # 1Sam-nak megfelelo sorszam (09), szamjegyre kezdodo fajlkod -- az FJ1 mintaja ezt elvesztette
    xml = ('<sentence><w ref="1SA 1:1!1" strongnumberx="H7585" greek="hadou" greekstrong="0086">שְׁאוֹל</w>'
           '<w ref="1SA 1:1!2" strongnumberx="H1234">דבר</w></sentence>')
    with open(os.path.join(lf, '09-1Sam-001-lowfat.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    git_repo(repo)
    naplok = os.path.join(tmp, 'naplok')
    os.makedirs(naplok)
    munkalap = os.path.join(naplok, 'FORRAS_FJ1_lxx_jeloltek.tsv')
    fej = 'motivum\tigehely\theber_kulcsszo\theber_strong\tjavasolt_gorog_lemma\tjavasolt_gorog_strong\tallapot\tbizonyossag\n'
    sorok = ['T-1\t1Sám 1:1\tשְׁאוֹל (sh)\tH7585\t\t\t\t',
             'T-2\t1Sám 1:1\tדבר (d)\t\t\t\t\t',
             'T-3\t1Sám 9:9\tשְׁאוֹל (sh)\tH7585\t\t\t\t',
             'T-4\t2Sám 1:1\tשְׁאוֹל (sh)\tH7585\t\t\t\t']
    with open(munkalap, 'w', encoding='utf-8') as f:
        f.write(fej + '\n'.join(sorok) + '\n')
    eredeti = (kozos.NAPLOK, macula.MUNKALAP)
    kozos.NAPLOK, macula.MUNKALAP = naplok, munkalap
    try:
        macula.fut(munka, 'onteszt')
    finally:
        kozos.NAPLOK, macula.MUNKALAP = eredeti
    _, sorok_ki = kozos.tsv_olvas(os.path.join(naplok, 'F06_macula_87_hely.tsv'))
    allapotok = [s[4] for s in sorok_ki]
    assert allapotok == ['LXX_MEGFELELO', 'HEBER_SZO_GOROG_NELKUL', 'NINCS_VERS', 'NINCS_KONYV_FAJL'], allapotok
    assert sorok_ki[0][5] == 'strong' and sorok_ki[1][5] == 'szoalak'
    _, lef = kozos.tsv_olvas(os.path.join(naplok, 'F06_macula_lefedettseg.tsv'))
    egy = [s for s in lef if s[0] == '1Sám'][0]
    assert egy[3] == '1Sam' and egy[4] == '1' and egy[5] == '1' and egy[11] == 'igen', egy


def teszt_bsb_futas(tmp):
    munka = os.path.join(tmp, 'munka_b')
    repo = os.path.join(munka, 'bsb-data-output')
    mappa = os.path.join(repo, 'base', 'display', 'GEN')
    os.makedirs(mappa)
    tahot = kozos.tahot_strongok()['1Móz 1:1']
    with open(os.path.join(mappa, 'GEN1.json'), 'w', encoding='utf-8') as f:
        json.dump({'eng': {'1': [['x', 'H%d' % n] for n in sorted(tahot)], '2': [['y', 'H1']]}}, f)
    git_repo(repo)
    naplok = os.path.join(tmp, 'naplok_b')
    os.makedirs(naplok)
    kuszob = os.path.join(tmp, 'kuszob.txt')
    with open(kuszob, 'w', encoding='utf-8') as f:
        f.write('kuszob=95\ndefinicio=tahot_resze_bsb\nnevezo=tahot_lefedett_versek\n')
    eredeti = (kozos.NAPLOK, bsb.KUSZOB_UT)
    kozos.NAPLOK, bsb.KUSZOB_UT = naplok, kuszob
    try:
        bsb.fut(munka, 'onteszt')
    finally:
        kozos.NAPLOK, bsb.KUSZOB_UT = eredeti
    _, sorok = kozos.tsv_olvas(os.path.join(naplok, 'F06_bsb_genezis.tsv'))
    assert [s[4] for s in sorok] == ['egyezik', 'elter'], sorok
    _, elt = kozos.tsv_olvas(os.path.join(naplok, 'F06_bsb_elteresek.tsv'))
    assert len(elt) == 1 and elt[0][0] == '1Móz 1:2'


def main():
    kozos.SZARAZ = False
    teszt_kapu()
    teszt_bsb_elemzes()
    with tempfile.TemporaryDirectory() as tmp:
        teszt_macula(tmp)
        teszt_bsb_futas(tmp)
    print('onteszt: rendben')


if __name__ == '__main__':
    main()
