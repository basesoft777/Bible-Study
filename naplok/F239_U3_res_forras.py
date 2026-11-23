"""F239 U3 — az adat/res_forras.tsv TEREMT-001 sorai a kézi forrásra (motivumok/TEREMT-001.md), a HAMART-001 migrált
mintája szerint: a négy prózarés a kézi forrásból, a 2b és a minősítés az adatból, az alátámasztás az adatból (a
motívumnak nincs kapcsolatok.tsv-sora); az `alkalmazas` (DT756) és a `tanitoi` (DT643) sor kivezetve. Írás előtt a
többi sort összeveti: csak a TEREMT-001 sorai változnak."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UT = os.path.join(GY, 'adat', 'res_forras.tsv')
nyers = open(UT, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(nl)
K = 'motivumok/TEREMT-001.md'
UJ = {
    'kivonat': ['TEREMT-001', 'kivonat', '## Kivonat', 'tanulmany', K],
    '2b': ['TEREMT-001', '2b', '### 2/b. Kiegészítő szótári adatok', 'adat', ''],
    'miert_fontos': ['TEREMT-001', 'miert_fontos', '### Miért fontos ez a lelet', 'tanulmany', K],
    'minosites': ['TEREMT-001', 'minosites', '### Minősítés', 'adat', ''],
    'alatamasztas': ['TEREMT-001', 'alatamasztas', '### Alátámasztás', 'adat', 'A motívumhoz nincs rögzített kapcsolat.'],
    'ertelmezes': ['TEREMT-001', 'ertelmezes', '## 6. Értelmezés', 'tanulmany', K],
    'modszertan': ['TEREMT-001', 'modszertan', '## 7. Módszertan és nyitott kérdések', 'tanulmany', K],
}
ki, beirt = [], False
for s in sorok:
    m = s.split('\t')
    if m[0] == 'TEREMT-001':
        if not beirt:
            ki.extend('\t'.join(UJ[r]) for r in ['kivonat', '2b', 'miert_fontos', 'minosites', 'alatamasztas',
                                                  'ertelmezes', 'modszertan'])
            beirt = True
        continue
    ki.append(s)
mas_regi = [s for s in sorok if s.split('\t')[0] != 'TEREMT-001']
mas_uj = [s for s in ki if s.split('\t')[0] != 'TEREMT-001']
if mas_regi != mas_uj:
    sys.exit('HIBA: más motívum sora változna; nem írok')
open(UT, 'w', encoding='utf-8', newline='').write(nl.join(ki))
print('TEREMT-001: %d sor → 7 sor' % sum(1 for s in sorok if s.split('\t')[0] == 'TEREMT-001'))
