# -*- coding: utf-8 -*-
"""F194.37 — a minta-ellenőrzés (az orkesztrátor, 2026-11-13) adatszintű találata a HAMART-001-en: a 7. Kapcsolatok
egy funkció-cellája a címkéje szavát ismétli („az erőszak: … hallatszó erőszak”). Az adat javul, a generátor nem.
Kulcs: (forras_igehely, cel_igehely, id). Írás előtt a nem érintett sorok összevetése (CLAUDE.md).
Futtatás a repó gyökeréből: python naplok/F194_minta_adat.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
P = 'adat/kapcsolatok.tsv'
KULCS = ('1Móz 6:11', 'Jer 6:7', 'HAMART-001')
REGI = 'az erőszak: a megtelt föld és a városban hallatszó erőszak'
UJ = 'az erőszak: a föld megtelik vele, a városban hallatszik'
raw = open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
sorok = raw.split(nl)
fej = [s for s in sorok if s and not s.startswith('#')][0].split('\t')
ix = {n: i for i, n in enumerate(fej)}
uj = list(sorok)
talalt = 0
for k, s in enumerate(sorok):
    m = s.split('\t')
    if len(m) < len(fej) or (m[ix['forras_igehely']], m[ix['cel_igehely']], m[ix['id']]) != KULCS:
        continue
    if m[ix['funkcio']] != REGI:
        sys.exit('ELTÉRÉS: a funkció nem a várt szöveg: %r' % m[ix['funkcio']])
    m[ix['funkcio']] = UJ
    uj[k] = '\t'.join(m)
    talalt += 1
if talalt != 1:
    sys.exit('ELTÉRÉS: %d sor a kulcsra' % talalt)
if sum(a != b for a, b in zip(sorok, uj)) != 1:
    sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')
print('változott: 1 sor (%s → %s)' % KULCS[:2])
if '--ir' in sys.argv:
    open(P, 'w', encoding='utf-8', newline='').write(nl.join(uj))
    print('írva:', P)
