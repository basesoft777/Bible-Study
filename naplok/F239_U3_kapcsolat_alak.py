"""F239 U3 — az ALVIL-001–TEREMT-001 kapcsolatsor (adat/motivum_kapcsolatok.tsv, Ez 31:15) indoklásának záró
döntés-hivatkozása az új generátor elfogadott alakjára (lapgen/bemenet/kapcsolat.py `_MK_ZARO_DONTES_RX`:
„Döntés: DT<n> (a felhasználó, <dátum>).”; a lapra nem kerül, a generátor leválasztja). Tartalom nem változik; a
helyőrzőt a merge utáni számkiosztás cseréli. Futtatás: python naplok/F239_U3_kapcsolat_alak.py [--ir]"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
UT = 'adat/motivum_kapcsolatok.tsv'
REGI = 'Döntés: DT-F239a (szerkesztői döntés, a felhasználó, 2026-11-23).'
UJ = 'Döntés: DT-F239a (a felhasználó, 2026-11-23).'
nyers = open(UT, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(nl)
n = 0
for i, s in enumerate(sorok):
    m = s.split('\t')
    if len(m) > 10 and m[0] == 'ALVIL-001' and m[3] == 'TEREMT-001' and m[1] == 'Ez 31:15':
        if not m[10].endswith(REGI):
            sys.exit('HIBA: váratlan indoklás-vég: %r' % m[10][-80:])
        m[10] = m[10][:-len(REGI)] + UJ
        sorok[i] = '\t'.join(m)
        n += 1
if n != 1:
    sys.exit('HIBA: %d sor' % n)
if '--ir' in sys.argv:
    open(UT, 'w', encoding='utf-8', newline='').write(nl.join(sorok))
print('1 sor; %s' % ('ÍRVA' if '--ir' in sys.argv else '(próba)'))
