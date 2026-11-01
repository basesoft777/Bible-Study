"""F152.14: a K1–K5 (DT476), a DT-F152b és a DT-F152c jelölt-része az adatrétegben.

A felhasználó döntései (2026-11-01; DONTESEK.md DT476, DT-F152b, DT-F152c):
- K1/K2: 1Pét 1:17, 2Tim 2:22, Róm 10:12, Róm 10:14 kikerül;
- DT-F152b („Csak ahol JHVH áll”): a hét névmási ragos sor kikerül;
- K4: az Ézs 43:1, 44:5, 45:3 elutasítási indoka a besém utáni JHVH hiánya;
- K5 („kontrasztként marad”, „Igen, kivételként”): az 1Kir 18:25–26 marad, jelölve, mi áll a besém után;
- DT-F152c (i): a két motívumközi jelölt (Róm 10:12, 10:14 ↔ TEREMT-001) elutasítva.

Út: jeloltek.tsv (beépítve → elutasítva, manual proveniencia, idézettel) → elofordulasok.tsv
(a sor törlődik). Írás előtt a feltételt a TAHOT/TAGNT-ből újramérjük, és a nem érintett sorok
bájtra azonosak maradnak. split('\t') / '\t'.join(), csv modul nélkül.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
DATUM = '2026.11.01'
PROV = 'scope=manual | forras=DONTESEK.md %s | ts=2026-11-01'

NT_K1 = ['1Pét 1:17']
NT_K2 = ['2Tim 2:22', 'Róm 10:12', 'Róm 10:14']
OT_RAG = ['Zak 13:9', 'Zsolt 105:1', '1Krón 16:8', 'Ézs 12:4', 'Jer 10:25', 'Zsolt 79:6', 'Ézs 64:6']
K4_KINT = ['Ézs 43:1', 'Ézs 44:5', 'Ézs 45:3']
K5 = {'1Kir 18:25': ('elohéchem', '„a ti isteneteknek”'), '1Kir 18:26': ('ha-Báal', '„a Baálnak”')}
MOTKOZI = ['Róm 10:12', 'Róm 10:14']


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def ir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok))


def tokenek(ut):
    d = {}
    with open(ut, encoding='utf-8') as f:
        for s in f:
            m = s.rstrip('\r\n').split('\t')
            d.setdefault(m[0], []).append(m)
    return d


# --- újramérés -----------------------------------------------------------
tahot = tokenek('konkordancia/TAHOT_kivonat.tsv')
tagnt = tokenek('konkordancia/TAGNT_kivonat.tsv')


def besem_utan(h):
    t = tahot[h]
    return [t[i + 1][1] for i in range(1, len(t) - 1) if t[i][1] == 'H8034' and t[i - 1][1] == 'H9003']


for h in OT_RAG:
    u = besem_utan(h)
    assert u and 'H3068' not in u, (h, u)
    assert all(x in ('H9020', 'H9021', 'H9023') for x in u), (h, u)
for h in K4_KINT:
    u = [tahot[h][i + 1][1] for i, t in enumerate(tahot[h][:-1]) if t[1] == 'H8034']
    assert u and 'H3068' not in u, (h, u)
for h in K5:
    assert 'H3068' not in besem_utan(h), h
for h in NT_K1 + NT_K2:
    sg = [t[1] for t in tagnt[h]]
    assert 'G1941' in sg and 'G3686' not in sg, (h, sg)
print('újramérés rendben: 7 ragos ÓSZ-sor, 3 Ézs-sor, 2 kontraszt-sor JHVH nélkül; 4 ÚSZ-sor ὄνομα (G3686) nélkül')

# --- jeloltek.tsv ----------------------------------------------------------
UT_J = 'adat/jeloltek.tsv'
J = olvas(UT_J)
J0 = list(J)

IDEZ_K1 = ('DT476 K1 (a felhasználó, 2026-11-01: „az 1Pét 1:17 kerüljön ki”): „Atyának hívjátok” — '
           'megszólítás, nem az Úr nevének segítségül hívása; a versben ὄνομα (G3686) nincs')
IDEZ_K2 = ('DT476 K2 (a felhasználó, 2026-11-01: „a név nélküli görög sorok kerüljenek ki (2Tim 2:22, '
           'Róm 10:12, Róm 10:14)”): ἐπικαλέομαι ὄνομα (G3686) nélkül; a név nélküli segítségül hívás a '
           'tágabb körbe tartozik (`motivumok.tsv` `folerendelt_fogalom`)')
IDEZ_RAG = ('DT-F152b (a felhasználó, 2026-11-01: „Csak ahol JHVH áll”): a besém után nem a JHVH (H3068) szó '
            'áll, hanem névmási rag (%s)')
RAG = {'Zak 13:9': 'bismí, „nevemet”', 'Zsolt 105:1': 'bismó, „nevét”', '1Krón 16:8': 'bismó, „nevét”',
       'Ézs 12:4': 'bismó, „nevét”', 'Jer 10:25': 'bismchá, „nevedet”', 'Zsolt 79:6': 'bismchá, „nevedet”',
       'Ézs 64:6': 'bismchá, „nevedet”'}
IDEZ_K4 = ('DT476 K4 és DT-F152b (a felhasználó, 2026-11-01: „itt ez az elhatárolás”; „Csak ahol JHVH '
           'áll”): a besém után nem JHVH (H3068) áll, hanem %s')
K4_MI = {'Ézs 43:1': 'névmási rag (besimchá, „a te neveden”), amely a megszólított Jákóbra utal',
         'Ézs 44:5': 'Jákób neve (besém Jaakóv)',
         'Ézs 45:3': 'névmási rag (besimchá, „a te neveden”), amely a megszólított Círusra utal'}
IDEZ_MK = ('DT-F152c (a felhasználó, 2026-11-01: „Igen, (b)”; a motívumközi rész az elfogadott javaslat (i) '
           'szerint): a %s a DT476 K2 óta nem ISTENTISZT-001-előfordulás, a motívumközi jelölt pedig az '
           '`id` motívum előfordulásán áll (SEMA 2.4)')

valtozott = {}
for i, s in enumerate(J):
    m = s.split('\t')
    if len(m) < 10 or m[0] != ID:
        continue
    h, tip = m[1], m[9]
    uj = None
    if tip == 'elofordulas' and h in NT_K1 + NT_K2 + OT_RAG:
        assert m[3] == 'beépítve', (h, m[3])
        if h in NT_K1:
            ok, dt = IDEZ_K1, 'DT476'
        elif h in NT_K2:
            ok, dt = IDEZ_K2, 'DT476'
        else:
            ok, dt = IDEZ_RAG % RAG[h], 'DT-F152b'
        m[3] = 'elutasítva'
        m[4] = '%s | %s | korábban (beépítve, %s): %s' % (ok, PROV % dt, m[8], m[4])
        m[8] = DATUM
        uj = m
    elif tip == 'elofordulas' and h in K4_KINT:
        assert m[3] == 'elutasítva', (h, m[3])
        m[4] = '%s | %s | korábbi indok (%s): %s' % (IDEZ_K4 % K4_MI[h], PROV % 'DT476+DT-F152b', m[8], m[4])
        m[8] = DATUM
        uj = m
    elif tip == 'elofordulas' and h in K5:
        assert m[3] == 'beépítve', (h, m[3])
        szo, karoli = K5[h]
        m[4] = m[4] + (' Kontraszt (DT476 K5; a felhasználó, 2026-11-01: „kontrasztként marad”, „Igen, '
                       'kivételként”): a besém után nem JHVH áll, hanem %s (%s).' % (szo, karoli))
        uj = m
    elif tip == 'motivumkozi' and h in MOTKOZI and m[10] == 'TEREMT-001':
        assert m[3] == 'nyitva', (h, m[3])
        m[3] = 'elutasítva'
        m[4] = '%s | %s | korábban (nyitva, %s): %s' % (IDEZ_MK % h, PROV % 'DT-F152c', m[8], m[4])
        m[8] = DATUM
        uj = m
    if uj is not None:
        J[i] = '\t'.join(uj)
        valtozott[(h, tip)] = i

assert len(valtozott) == 4 + 7 + 3 + 2 + 2, sorted(valtozott)
for i, (a, b) in enumerate(zip(J0, J)):
    if i not in valtozott.values():
        assert a == b, i
ir(UT_J, J)
print('jeloltek.tsv: %d sor módosult, sorszám változatlan (%d)' % (len(valtozott), len(J)))

# --- elofordulasok.tsv -----------------------------------------------------
UT_E = 'adat/elofordulasok.tsv'
E = olvas(UT_E)
torol = set(NT_K1 + NT_K2 + OT_RAG)
uj_e, torolt, mod = [], [], 0
for s in E:
    m = s.split('\t')
    if len(m) > 2 and m[0] == ID and m[1] in torol:
        torolt.append(m[1])
        continue
    if len(m) > 2 and m[0] == ID and m[1] in K5:
        szo, karoli = K5[m[1]]
        m[2] = m[2] + (' Kontraszt (DT476 K5): a besém után nem JHVH áll, hanem %s (%s).' % (szo, karoli))
        s = '\t'.join(m)
        mod += 1
    uj_e.append(s)
assert sorted(torolt) == sorted(torol), torolt
assert mod == 2
assert len(uj_e) == len(E) - 11
# a jelölt-sor és az előfordulás-sor kapcsolodas/indoklas mezője a K5-soron együtt mozog
ir(UT_E, uj_e)
n = sum(1 for s in uj_e if s.startswith(ID + '\t'))
print('elofordulasok.tsv: 11 sor törölve, 2 módosult; ISTENTISZT-001: %d sor' % n)
assert n == 22
