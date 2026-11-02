"""F152.25: a #152 lezárása a felhasználó döntése után („Igen, mindkettő”, 2026-11-02).

1. DONTESEK.md: a DT486 sor kiegészítése a két válasszal (C-w: (a); állapot: publikálható, v4).
2. adat/motivumok.tsv: ISTENTISZT-001 statusz_verzio v3 → v4, statusz_datum 2026.09.22 → 2026.11.02
   (a statusz `publikálható` marad); írás előtt soronkénti összevetés: csak ez az egy sor, csak ez a két mező.
3. F152_ISTENTISZT_TERV_HATRALEK_BRIEF.md: allapot megallt → lezarva, kovetkezo frissítve.
A sorvég a fájlé (newline=''), split('\t') / '\t'.join().
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = f.read()
    nl = '\r\n' if '\r\n' in s else '\n'
    return s.split(nl), nl


def ir(ut, sorok, nl):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write(nl.join(sorok))


# 1. DONTESEK
S, NL = olvas('DONTESEK.md')
i = [k for k, s in enumerate(S) if s.startswith('| DT486 |')]
assert len(i) == 1
REGI = 'A kolofon kiadás-sora ma nem renderelődik (N-F125a), ezért adatba nem került. |'
assert S[i[0]].count(REGI) == 1
S[i[0]] = S[i[0]].replace(REGI, REGI[:-2] + (
    ' **Kiegészítés (2026-11-02):** a zárójelentés két kérdésére a felhasználó a javaslat szerint döntött, szó '
    'szerint: „Igen, mindkettő”. (1) MUNKAMENET C-w: (a) — a K1–K5 utáni prózaátírás (F152.17) elég; az 1Móz 4:26 → '
    'Sof 3:9 pár kimondása a 2. kiadásba kerül, a lektori kérdésekkel együtt. (2) `motivumok.tsv`: az ISTENTISZT-001 '
    '`publikálható` marad, `v4`, 2026.11.02 (a K1–K5 a motívum határát érdemben változtatta; `véglegesített` nem, '
    'mert a 2. kiadás szerkesztői újranyitás). |'))
ir('DONTESEK.md', S, NL)
print('DONTESEK: DT486 kiegészítve')

# 2. motivumok.tsv
M, NLM = olvas('adat/motivumok.tsv')
M0 = list(M)
fej = M[1].split('\t')
assert fej[5:8] == ['statusz', 'statusz_verzio', 'statusz_datum'], fej[5:8]
db = 0
for k, s in enumerate(M):
    m = s.split('\t')
    if m[0] == 'ISTENTISZT-001':
        assert m[5:8] == ['publikálható', 'v3', '2026.09.22'], m[5:8]
        m0 = list(m)
        m[6], m[7] = 'v4', '2026.11.02'
        assert [a != b for a, b in zip(m0, m)].count(True) == 2
        M[k] = '\t'.join(m)
        db += 1
assert db == 1 and len(M) == len(M0)
assert sum(a != b for a, b in zip(M0, M)) == 1
ir('adat/motivumok.tsv', M, NLM)
print('motivumok.tsv: ISTENTISZT-001 publikálható, v3 → v4, 2026.09.22 → 2026.11.02')

# 3. brief fejléce
B, NLB = olvas('F152_ISTENTISZT_TERV_HATRALEK_BRIEF.md')
ia = [k for k, s in enumerate(B[:20]) if s.startswith('allapot:')]
ik = [k for k, s in enumerate(B[:20]) if s.startswith('kovetkezo:')]
assert len(ia) == 1 and len(ik) == 1 and B[ia[0]] == 'allapot: megallt', B[ia[0]]
B[ia[0]] = 'allapot: lezarva'
B[ik[0]] = ('kovetkezo: "Te: merge (a #566 utáni pótló draft PR, claude/f152-lezaras-2); lezárva 2026-11-02 (DT486, zárójelentés: '
            'naplok/ISTENTISZT_TERV_HATRALEK_zaras.md); a 2. kiadás bemenetei: a lektori kérdések, az N-F152c és az '
            '1Móz 4:26 → Sof 3:9 pár; nyitva: N-F152a, b, d–g"')
ir('F152_ISTENTISZT_TERV_HATRALEK_BRIEF.md', B, NLB)
print('brief: allapot lezarva')
