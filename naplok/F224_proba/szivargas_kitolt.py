# -*- coding: utf-8 -*-
"""F224.11: a két mérőtábla (adat/SEMA.md 2.72) kitöltése az elfogadási próba (F224.13) eredményéből.

A sorok: a lektori listák pontossági és érvelési tételei; a `hol` a menet mostani felállása szerinti próbán
megfogó lépés (F2: Opus — HAMART: naplok/F224_proba.md 7.1, ISTENTISZT: 8.1 és 8.5; D: a bíráló, 2.3; F1: a gépi
kapu), egyébként a lektor (F3), aki a hibát eredetileg megtalálta. A besorolás kézi (a próba naplója szerint),
itt rögzítve; a szkript csak a táblát írja. Használat: python naplok/F224_proba/szivargas_kitolt.py
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.getcwd(), 'eszkozok'))
import proza_allitas as P

FEJ = ['id', 'hely', 'allitas', 'mechanizmus', 'hol', 'sulyos', 'generalt', 'meres', 'forras']
TS = '2026-11-16'

# HAMART-001: lektor-tétel -> (K, mechanizmus, hol, megjegyzés a forráshoz)
HAM = {
    5: ('-', 'K-MIT', 'F1', 'F1 gépi tétel (szópár)'), 6: ('-', 'K-MIT', 'F1', 'F1 gépi tétel (szójelenlét)'),
    8: ('K5', 'K-HANY', 'F2', '7.1'), 9: ('K104', 'K-MIT', 'F2', '7.1'), 10: ('K104, K106', 'K-MASIK', 'F2', '7.1'),
    11: ('K106', 'K-KI', 'F3', '7.1: részben (az F2 más okból jelölte)'), 12: ('K105', 'K-MIT', 'F2', '7.1'),
    13: ('K98', 'K-KI', 'F2', '7.1'), 14: ('K98, K102', 'K-MIT', 'F3', '7.1: részben'),
    15: ('-', 'K-MIT', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    17: ('-', 'K-MASIK', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    18: ('-', 'K-MASIK', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    19: ('-', '-', 'F3', 'generált blokk (önhivatkozó bizonyosság-indok); a próba nem mérte (3/b)'),
    21: ('K14', 'K-CSOPORT', 'F3', '7.1: az F2 (Opus) igazolta'), 22: ('K28', 'K-HANY', 'F2', '7.1'),
    23: ('-', 'K-MIT', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    25: ('-', 'K-HANY', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    26: ('-', 'K-CSOPORT', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    27: ('-', 'K-KVANTOR', 'F3', 'generált blokk; a próba nem mérte (3/b)'),
    28: ('K31', 'K-MIT', 'F2', '7.1'), 29: ('K33, K45', 'K-KI', 'F2', '7.1'),
    30: ('-', 'ERVELES', 'F3', 'nem K-tétel; a bíráló e pontot nem kapta (a próba nem mérte)'),
    31: ('K39', 'K-KVANTOR', 'F2', '7.1'), 32: ('-', 'K-MIT', 'F1', 'F1 gépi tétel'),
    33: ('K41', 'K-MASIK', 'F2', '7.1'), 34: ('K44', 'K-KI', 'F2', '7.1'), 35: ('K47', 'K-KVANTOR', 'F2', '7.1'),
    36: ('K50, K116', 'K-MASIK', 'F2', '7.1 (a 2. körben a bíráló is: 2.3)'),
    37: ('-', 'ERVELES', 'F3', 'nem K-tétel; a bíráló e pontot nem kapta (a próba nem mérte)'),
    38: ('K55', 'K-HANY', 'F2', '7.1'), 40: ('K66', 'K-CSOPORT', 'F3', '7.1: az F2 (Opus) igazolta'),
    41: ('-', 'K-MIT', 'F1', 'F1 gépi tétel'), 42: ('K71', 'K-MIT', 'F2', '7.1'), 43: ('-', 'K-MIT', 'F1', 'F1 gépi tétel'),
}
HAM_GENERALT = {15, 17, 18, 19, 23, 25, 26, 27}

# ISTENTISZT-001, a 2. kiadás lektora (naplok/KIADAS_ISTENTISZT-001_lektor_2kiadas.md): 1–18 (a 19–22. érthetőségi)
IST = {
    1: ('K50, K61', 'Remez és az 1Kir 18:25 funkció-mezője: „a Baál prófétáinak szájában”', 'K-KI', 'F2', 'igen', '8.1'),
    2: ('K60', 'a Kivonat szabálya: „a hívás igéjét (kárá) a név követi”', 'K-SORREND', 'F2', 'igen', '8.1'),
    3: ('K58', 'Drash: „az Újszövetségben a név után álló szó Jézus Krisztus”', 'K-CSOPORT', 'D', 'igen', '2.3 (a 8. szakaszban az F2 is)'),
    4: ('K55', 'Remez: „három kapcsolat erős”', 'K-HANY', 'F1', 'nem', 'F1 JELENTÉS-sor (F224.4, N-F224a); az F2 is (8.1)'),
    5: ('K27', 'Remez: „ugyanaz a szókapcsolat áll” (1Móz 4:26 – 2Kir 5:11)', 'K-MASIK', 'F2', 'nem', '8.1'),
    6: ('K56', 'Vitatott pontok: „A lap a kérdést nem dönti el” (2Móz 33:19, 34:5)', 'ERVELES', 'D', 'nem', '2.3'),
    7: ('-', 'Vitatott pontok: a második olvasat érve csak a 34:5-re szól', 'ERVELES', 'D', 'nem', '2.3'),
    8: ('K52', '2.1, 2Móz 34:5: „megáll Mózes mellett”', 'K-KI', 'F2', 'nem', '8.1'),
    9: ('K57', 'Vitatott pontok, 1Móz 4:26: a pont dönt is', 'ERVELES', 'D', 'nem', '2.3'),
    10: ('K25', 'Peshat: „Mózes könyveinek hét helyéből ötben” (Targum)', 'K-MIT', 'F3', 'nem', '8.1: az F2 igazolta'),
    11: ('-', 'Peshat: „a segítségül hívás jelentését a név és az utána álló Úr neve adja meg”', 'K-MASIK', 'F3', 'nem', 'a próba nem mérte'),
    12: ('K13, K15', 'Miért fontos, H7121: a BDB Qal 2.c', 'K-MASIK', 'F2', 'nem', '8.1'),
    13: ('K22', 'Miért fontos: „12-ben az ἐπικαλέω áll”', 'K-HANY', 'F2', 'nem', '8.1'),
    14: ('-', 'Módszertan ↔ 9. táblázat: a kritikai szöveg eltérése', 'ERVELES', 'F3', 'nem', '2.3: a bíráló nem fogta meg'),
    15: ('K4', 'Kivonat, 1Kor 1:2: „a gyülekezet azok közössége …”', 'K-KI', 'F2', 'nem', '8.1'),
    16: ('K5', 'Kivonat: „öt a Genezisben, a pátriárkák történetében”', 'K-CSOPORT', 'F3', 'nem', '8.1: részben (az F2 más okból jelölte)'),
    17: ('K7', 'Kivonat: „Ahol a név helyén névmási rag áll … Ézs 43:1, 45:3”', 'K-KI', 'F3', 'nem', '8.1: az F2 igazolta'),
    18: ('-', 'Vitatott pontok, Róm 10:13: az első olvasat érve adat nélkül', 'ERVELES', 'D', 'nem', '2.3'),
}


def ir(ut, sorok, megjegyzes):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for m in megjegyzes:
            f.write('# ' + m + '\n')
        f.write('\t'.join(FEJ) + '\n')
        for s in sorok:
            assert len(s) == len(FEJ) and all('\t' not in x and '\n' not in x for x in s), s
            f.write('\t'.join(x if x else '-' for x in s) + '\n')


lektor = {t['szam']: t for t in P.lektor_tetelek('naplok/KIADAS_HAMART-001_lektor.md')}
pont = [n for n, t in lektor.items() if P.lektor_pontossagi(t)]
assert sorted(pont) == sorted(HAM), (sorted(pont), sorted(HAM))
sorok = []
for i, n in enumerate(sorted(HAM), 1):
    k, mech, hol, megj = HAM[n]
    t = lektor[n]
    allitas = re.sub(r'\s+', ' ', t['vonatkozik']).strip()
    allitas = re.sub(r'\s*\(sor [^)]*\)\s*$', '', allitas)
    allitas = allitas if len(allitas) <= 200 else allitas[:197].rsplit(' ', 1)[0] + ' …'
    hely = ('%s · %s' % (k, t['cim'])) if k != '-' else t['cim']
    sulyos = 'nem' if '(kisebb)' in t['gond'] else 'jeloletlen'
    sorok.append(['S%03d' % i, hely, allitas, mech, hol, sulyos, 'igen' if n in HAM_GENERALT else 'nem', 'visszajatszas',
                  'scope=naplok/KIADAS_HAMART-001_lektor.md %d. tétel; a próba: naplok/F224_proba.md %s | '
                  'forras=F224.13 (F2: claude-opus-5-5, C-futás; D: claude-sonnet-5-5) | ts=%s' % (n, megj, TS)])
ir('naplok/SZIVARGAS_HAMART-001.tsv', sorok, [
    'Mérőtábla (adat/SEMA.md 2.72): HAMART-001, az F224.13 elfogadási próbája (visszajátszás a f6da955e-s forráson).',
    'A sorok: a lektor 34 pontossági tétele (1. vagy 4. kérdés; naplok/KIADAS_HAMART-001_lektor.md). A hol: a menet mai',
    'felállása szerinti próbán megfogó lépés (F2 = Opus, 7. szakasz; F1 = a gépi kapu), egyébként a lektor (F3).',
    'Generált blokk 8 tétel, mind F3 (a 3/b-t a próba nem mérte). Kitöltő: naplok/F224_proba/szivargas_kitolt.py.'])

sorok = []
for i, n in enumerate(sorted(IST), 1):
    k, allitas, mech, hol, sulyos, megj = IST[n]
    sorok.append(['S%03d' % i, ('%s · lektor %d. tétel' % (k, n)) if k != '-' else 'lektor %d. tétel' % n, allitas, mech,
                  hol, sulyos, 'nem', 'visszajatszas',
                  'scope=naplok/KIADAS_ISTENTISZT-001_lektor_2kiadas.md %d. tétel; a próba: naplok/F224_proba.md %s | '
                  'forras=F224.13/F224.17 (F2: claude-opus-5-5, az új kinyeréssel; D: claude-sonnet-5-5) | ts=%s' % (n, megj, TS)])
ir('naplok/SZIVARGAS_ISTENTISZT-001.tsv', sorok, [
    'Mérőtábla (adat/SEMA.md 2.72): ISTENTISZT-001, az F224.13 és F224.17 próbája (visszajátszás a b2aea73f-es forráson).',
    'A sorok: a 2. kiadás lektorának 1–18. tétele (pontossági és érvelési); a 19–22. érthetőségi, nem pontossági.',
    'A hol: F2 = Opus az új kinyeréssel (8. szakasz), D = a bíráló (2.3), F1 = a gépi JELENTÉS-sor, egyébként F3.',
    'A mérés nem független (8. szakasz). Kitöltő: naplok/F224_proba/szivargas_kitolt.py.'])

for ut in ('naplok/SZIVARGAS_HAMART-001.tsv', 'naplok/SZIVARGAS_ISTENTISZT-001.tsv'):
    sor = [l.split('\t') for l in open(ut, encoding='utf-8').read().split('\n') if l and not l.startswith('#')][1:]
    db = {}
    for s in sor:
        db[s[4]] = db.get(s[4], 0) + 1
    print(ut, len(sor), 'sor;', db, '; generált:', sum(1 for s in sor if s[6] == 'igen'))
