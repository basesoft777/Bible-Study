# -*- coding: utf-8 -*-
"""F123 HAMART-001 U1 — a 12. szótári blokk (Tematikus index, Nave) gépi jelöltlistája.
A jelöltképzés a szerep_nave.py szabálya (legalább 2 motívumvers, legalább 1% arány, `tiltott` kizárva); a döntés
(kivalasztott / kizart / tiltott) az U2-U4 sessioné, az adat/tematikus_temak.tsv-be kerül. Döntés nélküli kimenet:
naplok/F123_U1_HAMART-001_nave_jeloltek.tsv. TSV: split('\t'), '\t'.join(); csv modul nincs."""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import szerep_nave as SN  # noqa: E402

MID = 'HAMART-001'
sorai = []
fej = None
for s in open(os.path.join(GY, 'adat', 'elofordulasok.tsv'), encoding='utf-8'):
    if s.startswith('#'):
        continue
    c = s.rstrip('\r\n').split('\t')
    if fej is None:
        fej = c
        continue
    if c[0] == MID:
        sorai.append(dict(zip(fej, c)))
jel = SN.jeloltek(sorai)
dont = SN.tema_dontesek(MID)
hu = SN.magyar_nevek()
ki = os.path.join(GY, 'naplok', 'F123_U1_%s_nave_jeloltek.tsv' % MID)
with open(ki, 'w', encoding='utf-8', newline='\n') as f:
    f.write("# GENERÁLT: naplok/F123_HAMART2_u1_nave_jeloltek.py | scope=%s adat/elofordulasok.tsv (%d sor) × konkordancia/Nave_basokant.tsv, szabály: eszkozok/szerep_nave.py jeloltek() (min. 2 motívumvers, min. 1%% arány, tiltott kizárva) | forras=split('\t') | ts=2026-11-04 | döntés nincs: az U2-U4 dönti (kivalasztott / kizart / tiltott), adat/tematikus_temak.tsv\n" % (MID, len(sorai)))
    f.write('tema_id\ttema\tmotivumversek_szama\ttemavers_szama\tarany\taltetelek\tmotivumversek\tmeglevo_dontes\n')
    for j in jel:
        cim = '; '.join('%s (%d)' % (c, len(v)) for c, v in j['cimkek'].items())
        f.write('\t'.join([j['tema_id'], j['tema'], str(len(j['motivumversek'])), str(j['temavers']),
                           '%.3f' % j['arany'], cim, ', '.join(j['motivumversek']),
                           dont.get(j['tema_id'], ('', ''))[0]]) + '\n')
print(len(sorai), 'E-sor;', len(jel), 'jelölt;', 'meglévő döntés:', len(dont))
for j in jel[:12]:
    print(j['tema_id'], j['tema'], len(j['motivumversek']), '%.3f' % j['arany'])
