"""F152.15: az ISTENTISZT-001 kapcsolatai a K1/K2, a DT-F152b és a DT-F152c (b) után.

- törlődik: Róm 10:13 → 10:14; Róm 10:14 → 2Tim 2:22, 1Pét 1:17 (DT-F152c (b), K1/K2);
  Zsolt 105:1 → 1Krón 16:8, Ézs 12:4; Jer 10:25 → Zsolt 79:6; Sof 3:9 → Zak 13:9 (DT-F152b);
- áthorgonyoz a Róm 10:13-ra: Róm 10:14 → 1Kor 1:2, ApCsel 9:14, ApCsel 22:16 (DT-F152c (b)).
A tábla nem tart proveniencia-mezőt: a `manual` proveniencia az indoklás végén áll.
Írás előtt: mindkét végponton az ὄνομα (G3686) meglétét a TAGNT-ből ellenőrizzük. split('\t') / '\t'.join().
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
UT = 'adat/kapcsolatok.tsv'
TOROL = {('Róm 10:13', 'Róm 10:14'), ('Róm 10:14', '2Tim 2:22'), ('Róm 10:14', '1Pét 1:17'),
         ('Zsolt 105:1', '1Krón 16:8'), ('Zsolt 105:1', 'Ézs 12:4'), ('Jer 10:25', 'Zsolt 79:6'),
         ('Sof 3:9', 'Zak 13:9')}
ATHORGONY = {'1Kor 1:2': 'a mi Urunk Jézus Krisztus nevét', 'ApCsel 9:14': 'a te nevedet',
             'ApCsel 22:16': 'az Úrnak nevét'}

tagnt = {}
with open('konkordancia/TAGNT_kivonat.tsv', encoding='utf-8') as f:
    for s in f:
        m = s.rstrip('\r\n').split('\t')
        tagnt.setdefault(m[0], []).append(m[1])
for h in ['Róm 10:13'] + list(ATHORGONY):
    assert 'G1941' in tagnt[h] and 'G3686' in tagnt[h], h
print('ellenőrizve: a Róm 10:13, 1Kor 1:2, ApCsel 9:14, 22:16 mindegyikében G1941 és G3686 áll')

with open(UT, encoding='utf-8', newline='') as f:
    S = f.read().split('\n')

uj, torolt, at = [], [], []
for s in S:
    m = s.split('\t')
    if len(m) > 3 and m[2] == ID:
        k = (m[0], m[1])
        if k in TOROL:
            torolt.append(k)
            continue
        if m[0] == 'Róm 10:14' and m[1] in ATHORGONY:
            assert ('Róm 10:13', m[1]) not in {(x.split('\t')[0], x.split('\t')[1]) for x in S if '\t' in x}
            m[0] = 'Róm 10:13'
            m[4] = 'azonos görög ige és név (ἐπικαλέομαι τὸ ὄνομα), egyházi azonosító-formulává válás — nincs szó szerinti idézés' \
                if m[1] == '1Kor 1:2' else m[4].replace('azonos görög ige', 'azonos görög ige és név')
            m[7] = ('Azonos görög ige és név: a Róm 10:13-ban „τὸ ὄνομα κυρίου” (ἐπικαλέσηται), itt „%s” '
                    '(ἐπικαλέομαι + ὄνομα); szó szerinti idézési kapcsolat nincs, a kapcsolat lexikai, innen a '
                    'közepes bizonyosság. Áthorgonyozva a Róm 10:14-ről (DT-F152c, a felhasználó, 2026-11-01: '
                    '„Igen, (b)”) | scope=manual | forras=DONTESEK.md DT-F152c | ts=2026-11-01' % ATHORGONY[m[1]])
            at.append(m[1])
            s = '\t'.join(m)
    uj.append(s)

assert sorted(torolt) == sorted(TOROL), torolt
assert sorted(at) == sorted(ATHORGONY), at
assert len(uj) == len(S) - 7
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(uj))
print('kapcsolatok.tsv: 7 sor törölve, 3 áthorgonyozva; ISTENTISZT-001: %d sor'
      % sum(1 for s in uj if s.split('\t')[2:3] == [ID]))
