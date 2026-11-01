# F121.8: a jóváhagyott 44 UBS-sor rögzítése + a G1941 33.131 definicio_hu sor cseréje (DT-F121h).
# Írás előtt a tábla sorainak összevetése: csak az 1 megnevezett sor változhat, 44 új sor kerül a végére.
import sys, hashlib
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, 'eszkozok'); sys.path.insert(0, 'naplok')
import forditas_kapuk as K
from F121_ubs_csomag_tervezet import rows
T = '\t'; MODELL = 'claude-sonnet-5-5'; DATUM = '2026.10.29'
MEGJ = 'F121 (DT-F121g): ISTENTISZT-001 UBS-csomag; D1 1. opció (CC BY-SA 4.0 forrás); proveniencia: scope=konkordancia/UBS_DBH_jelentesek.tsv, UBS_DNTG_jelentesek.tsv | forras=naplok/F121_ubs_csomag_tervezet.tsv | ts=2026-10-29'
p = 'adat/forditasok.tsv'
regi = open(p, 'rb').read(); assert regi.endswith(b'\n')
L = regi.decode('utf-8').split('\n')
# 1. a G1941 33.131 definicio_hu
UJ_3313 = 'valakiről szólva megnevezést alkalmazni'
forras_3313 = 'to use an attribution in speaking of a person'
n = 0; regi_szoveg = None
for i, l in enumerate(L):
    c = l.split(T)
    if len(c) > 10 and c[:5] == ['UBS_DNTG', 'G1941', '001957001001000', '33.131', 'definicio_hu']:
        assert hashlib.sha1(forras_3313.encode()).hexdigest() == c[5]
        er = K.kapuk_futtat('UBS_DNTG', forras_3313, UJ_3313); assert K.atment(er), er
        regi_szoveg = c[6]; c[6] = UJ_3313; c[7] = 'sonnet'; c[8] = MODELL; c[9] = DATUM; c[10] = 'v4'
        c[11] = 'F121.8: régi kézi sor (2026.09.22) cserélve a felhasználó döntésére (DT-F121h); régi szöveg: ' + regi_szoveg
        L[i] = T.join(c); n += 1
assert n == 1
# 2. a 44 új sor
uj = []
bukott = []
have = {tuple(l.split(T)[:5]) for l in L[1:] if l}
for r in rows:
    assert tuple(r[:5]) not in have, r[:5]
    er = K.kapuk_futtat(r[0], r[5], r[6])
    if not K.atment(er):
        # kézi ítélet: a felhasználó a szöveget kifejezetten jóváhagyta (DT-F121h); a bukás a bukottak.tsv-be kerül
        assert (r[2], r[4]) == ('006562002003000', 'glosszak_hu'), (r[2], r[4])
        bukott.append(T.join([r[0], r[1], r[2], r[4], '4_formazas', '; '.join(d for n_, e_, d in er if e_ == 'SERTES'), r[6], 'kézi ítélet: a felhasználó jóváhagyta (DT-F121h), 2026-10-29']))
    uj.append(T.join([r[0], r[1], r[2], r[3], r[4], hashlib.sha1(r[5].encode('utf-8')).hexdigest(), r[6], 'sonnet', MODELL, DATUM, 'v4', MEGJ]))
assert len(uj) == 44
tartalom = '\n'.join(L)
open(p, 'wb').write(tartalom.encode('utf-8') + ''.join(s + '\n' for s in uj).encode('utf-8'))
if bukott:
    with open('naplok/F121_GLOSSZA_FORDITAS_bukottak.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write(T.join(['szotar', 'strong', 'entry_id', 'mezo', 'kapu', 'reszlet', 'szoveg', 'itelet']) + '\n')
        for b in bukott: f.write(b + '\n')
print('regi 33.131:', regi_szoveg); print('+44 sor')
