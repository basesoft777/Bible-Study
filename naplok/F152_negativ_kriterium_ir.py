"""F152.16: az ISTENTISZT-001 `negativ_kriterium`-a a DT-F152b, a DT-F151c K2 és K5 után.

A régi szöveg „passzív …” része változatlan; elé kerül a JHVH-feltétel, az ÚSZ-feltétel és a
K5-kivétel. Csak ez az egy mező változik; split('\t') / '\t'.join(), összevetéssel.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/motivumok.tsv'
REGI_ELEJE = ('az igehelynek a קָרָא (kárá) + בְּ (be) (aktív, invokáló szerkezet: "[valaki] hívja segítségül '
              '[Isten nevét]") mintát kell mutatnia — ')
UJ_ELEJE = ('az igehelynek a קָרָא (kárá) + בְּשֵׁם (besém) + יְהוָה (JHVH) mintát kell mutatnia (aktív, invokáló '
            'szerkezet: "[valaki] hívja segítségül az Úr nevét"), a besém után a JHVH szóval; ahol névmási rag '
            'áll a helyén („nevemet”, „nevedet”, „nevét”: Zak 13:9, Zsolt 105:1, Jer 10:25, Ézs 43:1, 45:3) vagy más név '
            '(Ézs 44:5), az nem tartozik ide (DT-F152b, DT-F151c K4). Az Újszövetségben az ἐπικαλέομαι mellett '
            'a névnek (ὄνομα) kell állnia; név nélkül a segítségül hívás a fölérendelt fogalomhoz tartozik '
            '(2Tim 2:22, Róm 10:12, 14; DT-F151c K2). Kivétel: a kontrasztként megtartott 1Kir 18:25–26, ahol a '
            'besém után elohéchem, illetve ha-Báal áll (DT-F151c K5). ')

with open(UT, encoding='utf-8', newline='') as f:
    S = f.read().split('\n')
uj = list(S)
db = 0
for i, s in enumerate(S):
    m = s.split('\t')
    if m[0] == 'ISTENTISZT-001':
        assert m[9].startswith(REGI_ELEJE + 'a passzív'), m[9][:120]
        m[9] = UJ_ELEJE + 'A' + m[9][len(REGI_ELEJE) + 1:]
        uj[i] = '\t'.join(m)
        db += 1
assert db == 1
assert sum(a != b for a, b in zip(S, uj)) == 1 and len(S) == len(uj)
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(uj))
print('motivumok.tsv: ISTENTISZT-001 negativ_kriterium frissítve')
