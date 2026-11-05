# -*- coding: utf-8 -*-
"""F123 HAMART-001 U3b: a 7 kiválasztott Nave-téma és altételeinek magyar neve az adat/nave_tema_hu.tsv-be.
A tervezet: Sonnet (claude-sonnet-5-5, a cikk menetében), a glossza_lexikon_forditas.py nave kapui és mankói után;
három név a lap szóhasználatára simítva (claude-opus-5-5). Bemenet: a tervezet TSV-je (argumentum)."""
import hashlib
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SIMIT = {('NAVE-2090', ''): 'a föld', ('NAVE-0312', ''): 'az özönvíz előtti nemzedék', ('NAVE-0586', ''): 'kiűzetés'}
PROV_S = ('scope=manual | forras=a Sonnet tervezete (claude-sonnet-5-5, a cikk menetében), a glossza_lexikon_forditas.py '
          'nave kapui és mankói után | ts=2026-11-05')
PROV_O = ('scope=manual | forras=a Sonnet tervezete a lap szóhasználatára simítva (claude-opus-5-5; a nave mankó '
          'kezi_iteletre jelzése után) | ts=2026-11-05')
ter = [l.rstrip('\n').split('\t') for l in io.open(sys.argv[1], encoding='utf-8')][1:]
ut = 'adat/nave_tema_hu.tsv'
nyers = io.open(ut, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
meglevo = {tuple(s.split('\t')[:2]) for s in nyers.split(nl)}
uj = []
for tid, cim, angol, magyar in ter:
    assert (tid, cim) not in meglevo, (tid, cim)
    simitott = SIMIT.get((tid, cim))
    uj.append('\t'.join([tid, cim, angol, simitott or magyar, hashlib.sha1(angol.encode('utf-8')).hexdigest(), 'kezi',
                         'claude-opus-5-5' if simitott else 'claude-sonnet-5-5', '2026-11-05',
                         PROV_O if simitott else PROV_S]))
io.open(ut, 'w', encoding='utf-8', newline='').write(nyers.rstrip(nl) + nl + nl.join(uj) + nl)
print('nave_tema_hu.tsv: +%d' % len(uj))
