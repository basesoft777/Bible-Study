"""DT-F131q 1–2.: az N-F131a és az N-F131b rendezése az `elofordulasok.tsv` ISTENTISZT-001 során.

Csak a megnevezett 7 sor 10 mezője, a `jelentes_hu`, illetve `jelentes_szam` mezője változhat, a régi értéket ellenőrizve; split('\t') /
'\t'.join(); írás előtt soronkénti összevetés az eredetivel, eltérésnél megáll. Az 1Kir 18:24 új értéke a kész BDB-fordítás
szövege (`adat/forditasok.tsv`, BDB H7121, a Qal 2.c szakasz; a ׳י feloldva, mint a `jelentes_en`-ben).
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/elofordulasok.tsv'
INVOK = 'invokálni, segítségül hívni'
CSERE = {  # igehely: (mező, régi, új)
    ('2Móz 33:19', 'jelentes_hu'): ('kihirdetni, kinyilatkoztatni (NEM invokáció)', 'kihirdetni'),
    ('2Móz 34:5', 'jelentes_hu'): ('kihirdetni, kinyilatkoztatni (NEM invokáció)', 'kihirdetni'),
    ('Jer 10:25', 'jelentes_hu'): ('invokálni — tagadó szerkezetben, a mulasztás vádjaként', INVOK),
    ('Zsolt 79:6', 'jelentes_hu'): ('invokálni — tagadó szerkezetben, a mulasztás vádjaként', INVOK),
    ('Ézs 64:6', 'jelentes_hu'): ('invokálni — tagadó szerkezetben', INVOK),
    ('1Kir 18:24', 'jelentes_hu'): ('Jahve nevével, konkrét felszólítás hatalma megmutatására',
                                    'annak konkrét kérésére, hogy Jahve mutassa meg hatalmát'),
    ('Jer 10:25', 'jelentes_szam'): ('2.c (tagadva)', '2.c'),
    ('Zsolt 79:6', 'jelentes_szam'): ('2.c (tagadva)', '2.c'),
    ('Ézs 64:6', 'jelentes_szam'): ('2.c (tagadva)', '2.c'),
    ('Sof 3:9', 'jelentes_szam'): ('2.c (rokon)', '2.c'),
}

with open(UT, encoding='utf-8', newline='') as f:
    regi = f.read().split('\n')
fej_i = next(i for i, s in enumerate(regi) if s.startswith('id\t'))
fej = regi[fej_i].split('\t')
ix = {n: i for i, n in enumerate(fej)}
uj = list(regi)
kesz = set()
for i, s in enumerate(regi):
    if i <= fej_i or not s:
        continue
    m = s.split('\t')
    if m[ix['id']] != 'ISTENTISZT-001':
        continue
    for (hely, mezo), (r, u) in CSERE.items():
        if m[ix['igehely']] == hely:
            if m[ix[mezo]] != r:
                raise SystemExit('váratlan régi érték: %s %s: %r' % (hely, mezo, m[ix[mezo]]))
            m[ix[mezo]] = u
            kesz.add((hely, mezo))
    uj[i] = '\t'.join(m)
if kesz != set(CSERE):
    raise SystemExit('hiányzó csere: %s' % (set(CSERE) - kesz))
elter = [i for i in range(len(regi)) if regi[i] != uj[i]]
if len(regi) != len(uj) or len(elter) != 7:  # 10 mező 7 sorban (a Jer, a Zsolt és az Ézs sorában kettő)
    raise SystemExit('váratlan eltérés: %d sor' % len(elter))
for i in elter:
    a, b = regi[i].split('\t'), uj[i].split('\t')
    if [n for n in range(len(a)) if a[n] != b[n]] and not all(fej[n] in ('jelentes_hu', 'jelentes_szam')
                                                              for n in range(len(a)) if a[n] != b[n]):
        raise SystemExit('más mező is változna: %d. sor' % (i + 1))
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(uj))
print('kész: %d sor, %d mező' % (len(elter), len(CSERE)))
