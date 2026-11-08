# -*- coding: utf-8 -*-
"""F123 HAMART-001, /elteres 1. kör (naplok/ELLENOR_F123_HAMART3_javitokor2.md): az adatra vonatkozó tételek.
    python naplok/F123_HAMART3_elteres2.py <tétel> [--ir]
tétel: 2 (Jel 19:2 jelöltsor), 5 (nyilt_angol forrás nélküli sorai), 8 (Gal 3:13-14 mezői, DT-F123he).
Írás előtt soronként összevet: csak a megnevezett sorok változnak."""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, 'eszkozok')


def olvas(ut):
    return open(ut, encoding='utf-8', newline='').read().split('\n')


def ir(ut, sorok, irj):
    if irj:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))


def t2(irj):
    ut = 'adat/jeloltek.tsv'
    s = olvas(ut)
    a = 'ugyanaz az ige+tárgy szerkezet, mint a LXX 1Móz 6:11-ben (ἐφθάρη … ἡ γῆ)'
    b = 'ugyanaz az ige, ugyanarra a földre, mint a LXX 1Móz 6:11-ben, ahol a föld az alany (ἐφθάρη … ἡ γῆ)'
    n = [i for i, l in enumerate(s) if l.startswith('HAMART-001\tJel 19:2\t') and a in l]
    assert len(n) == 1
    s[n[0]] = s[n[0]].replace(a, b)
    ir(ut, s, irj)
    print(ut, ': Jel 19:2')


def t5(irj):
    """A nyilt_angol.tsv HAMART-001-sorai, amelyeknek a kulcsa (tábla + oszlop + sorkulcs) a mai exportban nem áll:
    a forrásszöveg megszűnt (kikerült vagy átkulcsolt sor). Csak ezek törlődnek."""
    import nyilt_mag_angol as A
    regi = A.tar_olvas()
    elo = {(c[0], c[1], c[2]) for c in A.cellak()}
    assert elo, 'a mai exportnak nincs szabad szöveges cellája'
    torol = [r for r in regi if 'HAMART-001' in r['sorkulcs'] and (r['tabla'], r['oszlop'], r['sorkulcs']) not in elo]
    print('forrás nélküli HAMART-001 sor: %d' % len(torol))
    for r in torol:
        print('  ', r['tabla'], r['oszlop'], r['sorkulcs'])
    if irj and torol:
        ut = A.UT
        s = olvas(ut)
        kul = {'\t'.join([r['tabla'], r['oszlop'], r['sorkulcs']]) for r in torol}
        uj = [l for l in s if '\t'.join(l.split('\t')[:3]) not in kul]
        assert len(s) - len(uj) == len(torol)
        ir(ut, uj, irj)


def t8(irj):
    ut = 'adat/elofordulasok.tsv'
    s = olvas(ut)
    fi = next(i for i, l in enumerate(s) if l and not l.startswith('#'))
    ix = {k: i for i, k in enumerate(s[fi].split('\t'))}
    n = [i for i, l in enumerate(s) if l.startswith('HAMART-001\tGal 3:13-14\t')]
    assert len(n) == 1
    r = s[n[0]].split('\t')
    assert r[ix['megbizhatosag']] == 'magas' and r[ix['pardes_szint']] == 'Drash/Sod', (r[ix['megbizhatosag']], r[ix['pardes_szint']])
    r[ix['megbizhatosag']], r[ix['pardes_szint']] = 'közepes', 'Remez'
    r[ix['proveniencia']] = r[ix['proveniencia']].replace('DT-F123hd)', 'DT-F123hd; a bizonyosság és a réteg: DT-F123he, szerkesztői döntés)')
    s[n[0]] = '\t'.join(r)
    ir(ut, s, irj)
    print(ut, ': Gal 3:13-14 (közepes, Remez)')


if __name__ == '__main__':
    {'2': t2, '5': t5, '8': t8}[sys.argv[1]]('--ir' in sys.argv)
