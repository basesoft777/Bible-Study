#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f110_ir2.py — F110 javítókör 1. kör: a jeloltek.tsv szándékolt soraiban lépésenkénti módosítás.
Lépések: kiszur (JSir 3:55, 5Móz 32:3 törlése), apcsel (7:59 elutasítva), ezs4125 (vitatott-mondat ki),
karoli (idézetek a Károli szó szerinti szövegére + lekérdezés-proveniencia).
split('\t') / '\t'.join, bájt-szintű írás; írás előtt soronkénti összevetés: csak a szándékolt sorok változnak.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
ID = 'ISTENTISZT-001'
P = lambda ih, n: 'Károli-proveniencia (lekerdez.py karoli): scope=range:%s | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=%d | ts=2026-10-21T10:14Z' % (ih, n)

KISZUR = ['JSir 3:55', '5Móz 32:3']
APCSEL_IND = ('F110 szűrő (DT-F110a), A osztály, kézi olvasás: nincs ὄνομα — invokáció a קָרָא בְשֵׁם / '
              'ἐπικαλέομαι τὸ ὄνομα formulán kívül (motivumok.tsv, fölérendelt fogalom); Károli: „ki imádkozik és ezt mondja vala: '
              'Uram Jézus, vedd magadhoz az én lelkemet!” | ' + P('ApCsel 7:59', 2))
EZS4125_REG = ('; értelmezés vitatott (Círusz hívja-e az Úr nevét). A szabály átengedi; elbírálatlan, a motívum-menet dönt',
               '. A szabály átengedi; elbírálatlan, a motívum-menet dönt')
KAROLI = {
    '2Kor 1:23': [('kézi olvasás: „Istent hívom tanúul a lelkemre”', 'kézi olvasás: Károli: „Én pedig az Istent hívom bizonyságul az én lelkemre”')],
    'Mt 10:25': [('kézi olvasás: „Beelzebubnak hívták a házigazdát”', 'kézi olvasás: Károli: „Ha a házigazdát Belzebubnak hívták”')],
    'Ézs 41:25': [('kézi olvasás: „napkelet felől (az) hívja a nevemet” (TAHOT', 'kézi olvasás: Károli: „hirdeti nevemet” (TAHOT')],
    'Ézs 64:6': [('kézi olvasás: „nincs, aki segítségül hívja a nevedet” (TAHOT', 'kézi olvasás: Károli: „S nem volt, a ki segítségül hívta volna nevedet” (TAHOT')],
}
KAROLI_N = {'2Kor 1:23': 2, 'Mt 10:25': 1, 'Ézs 41:25': 3, 'Ézs 64:6': 1}


def main():
    lepes = sys.argv[1]
    p = ROOT / 'adat/jeloltek.tsv'
    raw = p.read_bytes()
    tail = raw.endswith(b'\n')
    lines = raw.split(b'\n')
    if tail:
        lines = lines[:-1]
    eredeti = list(lines)
    ki, valt = [], set()
    for n, b in enumerate(lines):
        eol = b'\r' if b.endswith(b'\r') else b''
        f = b[:len(b) - len(eol)].decode('utf-8').split('\t')
        if len(f) == 13 and f[0] == ID and f[9] == 'elofordulas':
            ih = f[1]
            if lepes == 'kiszur' and ih in KISZUR:
                valt.add(n)
                continue
            if lepes == 'apcsel' and ih == 'ApCsel 7:59' and f[3] == 'nyitva':
                f[3], f[4] = 'elutasítva', APCSEL_IND
                lines[n] = '\t'.join(f).encode('utf-8') + eol
                valt.add(n)
            if lepes == 'ezs4125' and ih == 'Ézs 41:25':
                assert EZS4125_REG[0] in f[4]
                f[4] = f[4].replace(*EZS4125_REG)
                lines[n] = '\t'.join(f).encode('utf-8') + eol
                valt.add(n)
            if lepes == 'karoli' and ih in KAROLI:
                for a, bb in KAROLI[ih]:
                    assert a in f[4], ih
                    f[4] = f[4].replace(a, bb)
                f[4] += ' | ' + P(ih, KAROLI_N[ih])
                lines[n] = '\t'.join(f).encode('utf-8') + eol
                valt.add(n)
        ki.append(lines[n])
    elv = {'kiszur': 2, 'apcsel': 1, 'ezs4125': 1, 'karoli': 4}[lepes]
    assert len(valt) == elv, (lepes, len(valt))
    # összevetés: a nem érintett sorok bájtra azonosak
    maradek = [x for i, x in enumerate(eredeti) if i not in valt]
    kimaradt = [x for i, x in enumerate(ki) if True]
    if lepes == 'kiszur':
        assert len(ki) == len(eredeti) - 2 and ki == maradek
    else:
        assert len(ki) == len(eredeti)
        for i, (a, b) in enumerate(zip(eredeti, ki)):
            if i not in valt:
                assert a == b, i
    p.write_bytes(b'\n'.join(ki) + (b'\n' if tail else b''))
    print(lepes, 'ok; érintett sorok:', len(valt), 'sorok', len(eredeti), '->', len(ki))


if __name__ == '__main__':
    main()
