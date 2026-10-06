#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdb_atvezet_m5.py -- F56 M5: a javitotabla `javitva` soranak atvezetese az adat/forditasok.tsv
BDB-fordításain (`Y [BDB: X]`). Szarazon fut; --ir eseten ir. --visszaallit (DT-F56c): a mar atvezetett
`Y [BDB: X]` alakot X-re allitja vissza, ha a javitotablaban az X sora azota nem `javitva`. Iras elott/utan a sorok
soronkenti osszevetese: csak a szandekolt sorok `forditas_hu` mezoje valtozhat, eltereskor megall.
TSV: split('\t') / '\t'.join(), nem a csv modul.
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_adatblokk as B  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'adat', 'forditasok.tsv')
IDX_FORDITAS = 6


def olvas():
    with open(TABLA, encoding='utf-8', newline='') as fh:
        szoveg = fh.read()
    return szoveg.split('\n')  # \r\n eseten a sorveg a vegso mezoben maradna; lent ellenorizve


def main():
    ir = '--ir' in sys.argv
    vissza = '--visszaallit' in sys.argv
    sorok = olvas()
    assert not any('\r' in s for s in sorok), 'CR a tablaban'
    javitva = {}
    for strong, ss in B.javitotabla_olvas().items():
        for s in ss:
            if s['allapot'] == 'javitva':
                javitva.setdefault(strong, []).append(s)
    uj = list(sorok)
    valtozott = []
    osszes = []
    for i, sor in enumerate(sorok):
        if not sor or sor.startswith('#') or sor.startswith('szotar\t'):
            continue
        m = sor.split('\t')
        assert len(m) == 12, (i + 1, len(m))
        if m[0] != 'BDB':
            continue
        sp = B.strong_padded(m[1])
        if vissza:
            if '[BDB: ' not in m[IDX_FORDITAS]:
                continue
            ujszoveg, csere = B.atvezet_vissza(m[IDX_FORDITAS], javitva.get(sp, []))
        elif sp not in javitva:
            continue
        else:
            ujszoveg, csere = B.atvezet_szoveg(m[IDX_FORDITAS], javitva[sp])
        if csere:
            m2 = list(m)
            m2[IDX_FORDITAS] = ujszoveg
            uj[i] = '\t'.join(m2)
            valtozott.append(i)
            osszes.extend((m[1], m[3], r, j, d) for r, j, d in csere)
    for x in osszes:
        if vissza:
            print('visszaallitas: %s jelentes=%s | %s [BDB: %s] -> %s x%d' % (x[0], x[1], x[2], x[3], x[3], x[4]))
        else:
            print('csere: %s jelentes=%s | %s -> %s [BDB: %s] x%d' % (x[0], x[1], x[2], x[3], x[2], x[4]))
    # javitva sorok, amelyek nem fordulnak elo a fordításban (pl. kesobbi adag)
    osszes_strong = {x[0] for x in osszes}
    for strong, ss in ([] if vissza else sorted(javitva.items())):
        for s_ in ss:
            if strong.lstrip('H').lstrip('0') and not any(B.strong_padded(k) == strong for k in osszes_strong):
                print('nincs elofordulas a forditasban: %s %s' % (strong, s_['forras_hivatkozas']))
    # osszevetes: csak a szandekolt sorok, csak a forditas_hu mezo
    assert len(uj) == len(sorok)
    for i, (a, b) in enumerate(zip(sorok, uj)):
        if a == b:
            continue
        assert i in valtozott, 'nem szandekolt sor valtozott: %d' % (i + 1)
        ma, mb = a.split('\t'), b.split('\t')
        assert len(ma) == len(mb) == 12
        assert all(ma[k] == mb[k] for k in range(12) if k != IDX_FORDITAS), 'mas mezo valtozott: %d' % (i + 1)
    print('valtozott sorok: %d; csere osszesen: %d' % (len(valtozott), sum(x[4] for x in osszes)))
    if ir:
        with open(TABLA, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(uj))
        # ujraolvasas + osszevetes
        ellen = olvas()
        assert len(ellen) == len(sorok)
        for i, (a, b) in enumerate(zip(sorok, ellen)):
            if a != b:
                assert i in valtozott
                ma, mb = a.split('\t'), b.split('\t')
                assert all(ma[k] == mb[k] for k in range(12) if k != IDX_FORDITAS)
        print('irva; ujraolvasas utan az osszevetes rendben')
    return 0


if __name__ == '__main__':
    sys.exit(main())
