"""F239 U3b — a vitatott_forrasok.tsv három TEREMT-001 sorának `pont` kulcsa a forrásprózabeli félkövér címre
(SEMA 2.58: a `pont` a vitatott pont félkövér címe a forrásprózában, a záró pont nélkül). Csak a kulcs változik;
minden más mező és sor változatlan (írás előtt összevetve)."""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/vitatott_forrasok.tsv'
CSERE = {
    'A Jelenések bezárása (20:3) visszhangozza-e az 1Móz 8:2 bezárását?': 'A Jelenések bezárása és az özönvíz',
    'A Tengeri ének (2Móz 15:5, 8) tudatosan visszautal-e a genezisi özönvízre?': 'A Tengeri ének és az özönvíz',
    'A tehóm és Tiámat: rokon-e, és ha igen, polémia-e az 1Móz 1:2?': 'A tehóm és Tiámat',
}

nyers = open(UT, encoding='utf-8', newline='').read()
sorveg = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(sorveg)
uj, db = [], 0
for s in sorok:
    m = s.split('\t')
    if len(m) > 2 and m[0] == 'TEREMT-001' and m[1] in CSERE:
        m[1] = CSERE[m[1]]
        db += 1
    uj.append('\t'.join(m))
if db != 3:
    sys.exit('ELTÉRÉS: %d sor illeszkedett, 3 kellett' % db)
# összevetés: a kulcson kívül semmi nem változhat
for a, b in zip(sorok, uj):
    ma, mb = a.split('\t'), b.split('\t')
    if len(ma) != len(mb) or [x for i, x in enumerate(ma) if i != 1] != [x for i, x in enumerate(mb) if i != 1]:
        sys.exit('ELTÉRÉS a kulcson kívül: %s' % a[:80])
    if ma != mb and ma[0] != 'TEREMT-001':
        sys.exit('ELTÉRÉS más motívumnál: %s' % a[:80])
open(UT, 'w', encoding='utf-8', newline='').write(sorveg.join(uj))
print('kész: %d kulcs' % db)
