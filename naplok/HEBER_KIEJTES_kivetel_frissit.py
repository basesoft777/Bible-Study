"""Egyszeri adatjavítás a DT-F131y szerint (N-F131w, 2026-10-30): az
`adat/kiejtes_kivetelek.tsv` héber sorai.

- R1 (ס = sz): H3678 כִּסֵּא kissé -> kisszé; H2555 חָמָס hámás -> chámász (R8: ח = ch, a H2555-nél is)
- új kivételsorok (R2, R7): H3605 כֹּל -> kol, H2451 חׇכְמָה -> chochmá, H3389 Jeruzsálem -> jerúsálajim

A kulcs a TBESH-lemma NFC-alakja (SEMA 2.17), a konkordancia/TBESH.txt-ből
véve (nem begépelve). Olvasás split('\\t'), írás '\\t'.join(); írás előtt
összeveti a sorokat az eredetivel, és csak a várt eltérésnél ír (CLAUDE.md).
Másodszori futtatásra nem változtat (már megvan minden sor).
"""

import os
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'adat', 'kiejtes_kivetelek.tsv')
TBESH = os.path.join(ROOT, 'konkordancia', 'TBESH.txt')
DT = 'DT-F131y (2026-10-30)'

JAVITAS = {  # strong: (régi kiejtés, új kiejtés, indok)
    'H3678': ('kissé', 'kisszé', 'R1: ס = sz'),
    'H2555': ('hámás', 'chámász', 'R1: ס = sz; R8: ח = ch a H2555-nél is (a D36 „h” kivétele megszűnik)'),
}
UJ = {  # strong: (kiejtés, indok)
    'H3605': ('kol', 'R2 kivétellista: kámec kátán (כָּל); a lemma holamos alakja is „kol”'),
    'H2451': ('chochmá', 'R2 kivétellista: kámec kátán (חָכְמָה)'),
    'H3389': ('jerúsálajim', 'R7: Jeruzsálem lexikai kivétel (qere perpetuum), minden alakjával'),
}


def tbesh_lemma(strong):
    with open(TBESH, encoding='utf-8') as f:
        for sor in f:
            c = sor.rstrip('\r\n').split('\t')
            if len(c) > 4 and c[0] == strong:
                return unicodedata.normalize('NFC', c[3])
    raise SystemExit('nincs TBESH-sor: %s' % strong)


def main():
    with open(TABLA, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorvege = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(sorvege)
    if sorok and sorok[-1] == '':
        sorok = sorok[:-1]
        zaro = True
    else:
        zaro = False
    fej_i = next(i for i, s in enumerate(sorok) if s.startswith('nyelv\t'))
    fej = sorok[fej_i].split('\t')
    uj_sorok = list(sorok)
    valtozott = []
    meglevo = set()
    for i in range(fej_i + 1, len(sorok)):
        r = dict(zip(fej, sorok[i].split('\t')))
        if r.get('nyelv') != 'heber':
            continue
        meglevo.add(unicodedata.normalize('NFC', r['alak']))
        for strong, (regi, uj, indok) in JAVITAS.items():
            if strong in r['megjegyzes'] and unicodedata.normalize('NFC', r['alak']) == tbesh_lemma(strong):
                if r['kiejtes'] == uj:
                    continue
                if r['kiejtes'] != regi:
                    raise SystemExit('%s: váratlan kiejtés %r (várt: %r)' % (strong, r['kiejtes'], regi))
                r['kiejtes'] = uj
                r['megjegyzes'] += '; %s: %s -> %s (%s); manual' % (DT, regi, uj, indok)
                uj_sorok[i] = '\t'.join(r[k] for k in fej)
                valtozott.append((strong, regi, uj))
    for strong, (kiejt, indok) in UJ.items():
        lemma = tbesh_lemma(strong)
        if lemma in meglevo:
            continue
        uj_sorok.append('\t'.join(['heber', lemma, kiejt,
                                   '%s, %s, %s; kulcs: TBESH-lemma; manual' % (DT, strong, indok)]))
        valtozott.append((strong, '', kiejt))
    prov = ('# %s: R1/R8 javítás (H3678, H2555) és R2/R7 kivételsorok (H3605, H2451, H3389). '
            'scope=adat/kiejtes_kivetelek.tsv | forras=naplok/HEBER_KIEJTES_kivetel_frissit.py (manual döntés) | ts=2026-10-30' % DT)
    if valtozott and prov not in uj_sorok:
        uj_sorok.insert(fej_i, prov)
    # összevetés: csak a várt sorok változhattak
    elter = [s for s in uj_sorok if s not in sorok]
    eltunt = [s for s in sorok if s not in uj_sorok]
    if len(eltunt) != len([v for v in valtozott if v[1]]):
        raise SystemExit('váratlan eltérés: %d eltűnt sor' % len(eltunt))
    for v in valtozott:
        print('változott: %s %r -> %r' % v)
    print('új/módosult sor: %d, eltűnt (felülírt) sor: %d' % (len(elter), len(eltunt)))
    if not valtozott:
        print('nincs teendő')
        return
    with open(TABLA, 'w', encoding='utf-8', newline='') as f:
        f.write(sorvege.join(uj_sorok) + (sorvege if zaro else ''))


if __name__ == '__main__':
    main()
