"""F148 0. lépés: mérés a friss main-en (F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md 3. szakasz, 0.1–0.5).

Csak olvas; a lapokat a (iii) ponthoz repón kívüli ideiglenes könyvtárba rendereli.
Futtatás: python naplok/F148_meres.py [--forditas]
"""
import os
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import lexikon_general as LG  # noqa: E402


def tsv(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.strip()]


def fejezet(cim):
    print('\n## %s\n' % cim)


# 0.1 -------------------------------------------------------------------------
fejezet('0.1 A #123 ALVIL-001 PR-ja (#513) a main-en')
log = subprocess.run(['git', 'log', '--oneline', 'origin/main', '--grep=pull request #513'],
                     cwd=GYOKER, capture_output=True, text=True, encoding='utf-8').stdout.strip()
print(log or 'NINCS')

# 0.2 -------------------------------------------------------------------------
fejezet('0.2 Kitöltöttség az adat/elofordulasok.tsv-ben')
elo = tsv('adat/elofordulasok.tsv')
ids = sorted({r['id'] for r in elo})
print('| id | sor | jelentes_szam | karoli_szo | lexikon_entry_id | lexikon_szotar |')
print('|---|---|---|---|---|---|')
for i in ids:
    s = [r for r in elo if r['id'] == i]
    n = lambda m: sum(1 for r in s if r.get(m, '').strip())  # noqa: E731
    print('| %s | %d | %d | %d | %d | %d |' % (i, len(s), n('jelentes_szam'), n('karoli_szo'),
                                              n('lexikon_entry_id'), n('lexikon_szotar')))
print('\nscope=adat/elofordulasok.tsv (%d id, %d sor) | forras=naplok/F148_meres.py | ts=2026-10-29' % (len(ids), len(elo)))

# 0.3 -------------------------------------------------------------------------
fejezet('0.3 Gerincen álló motívumok (main)')
# F148.1 óta a kapcsoló adat (`adat/funkcio_kapcsolok.tsv`, `kivetel` sor); a gerinces kör `LG.gerinc_aktiv`
gerinc = sorted(i for i in ids if LG.gerinc_aktiv(i))
print('gerincen álló motívumok =', gerinc)
kivetel = [i for i in ids if i not in gerinc]
print('várható kivétellista:', kivetel)

# 0.4 -------------------------------------------------------------------------
fejezet('0.4 A négy új szabály próbafutása (kivétellistával)')
adat = LG.gerinc_adat()

print('### 18. gerinc-Strong címkéje (csak gerincen álló motívum)')
s18 = []
for r in elo:
    if r['id'] not in gerinc:
        continue
    kulcs, minosito = LG.kutatoi_kulcs(r.get('jelentes_szam', ''))
    try:
        ut = LG.kutatoi_szakasz(adat, r['lexikon_szotar'], r['lexikon_entry_id'], kulcs) if kulcs else None
    except LG.GerincHiba as e:
        ut = 'HIBA: %s' % e
    if not ut or str(ut).startswith('HIBA'):
        s18.append((r['id'], r['igehely'], r['lexikon_szotar'], r['lexikon_entry_id'], r['jelentes_szam'], ut))
print('SÉRTÉS-jelölt: %d' % len(s18))
for x in s18:
    print('  ', x)

print('\n### 19. kötelező mezők (karoli_szo, lexikon_szotar, lexikon_entry_id, jelentes_szam)')
MEZOK = ['karoli_szo', 'lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam']
for i in ids:
    s = [r for r in elo if r['id'] == i]
    hiany = {m: sum(1 for r in s if not r.get(m, '').strip()) for m in MEZOK}
    hianyos_sor = sum(1 for r in s if any(not r.get(m, '').strip() for m in MEZOK))
    print('  %s [%s]: hiányos sor %d/%d; %s' % (i, 'SÉRTÉS' if i in gerinc else 'JELENTÉS',
                                              hianyos_sor, len(s), hiany))
    if i in gerinc:
        for r in s:
            if any(not r.get(m, '').strip() for m in MEZOK):
                print('     ', r['igehely'], {m: r.get(m, '') for m in MEZOK})

print('\n### 20. jelentes_hu tisztasága (kiinduló minták)')
MINTAK = [
    ('zárójeles tagadó minősítés', r'\(\s*NEM\b'),
    ('tagadó szerkezet', r'(?i)tagadó szerkezet'),
    ('vádjaként', r'(?i)vádjaként'),
    ('motívum', r'(?i)motívum'),
    ('funkció', r'(?i)funkció'),
    ('invokáció', r'(?i)invokáci|invokál'),
]
tiltott = [t for t in tsv('adat/tiltott_fordulatok.tsv') if t.get('minta')]
for t in tiltott:
    MINTAK.append(('tiltott_fordulatok: %s' % t.get('magyar_alak', t['minta']), '(?i)' + t['minta']))
talalat20 = {}
for r in elo:
    for nev, m in MINTAK:
        if r.get('jelentes_hu') and re.search(m, r['jelentes_hu']):
            talalat20.setdefault(r['id'], []).append((r['igehely'], nev, r['jelentes_hu']))
for i in ids:
    t = talalat20.get(i, [])
    print('  %s [%s]: %d' % (i, 'SÉRTÉS' if i in gerinc else 'JELENTÉS', len(t)))
    if i in gerinc:
        for x in t:
            print('     ', x)
kir = [r for r in elo if r['igehely'].startswith('1Kir 18:2')]
print('  kontroll 1Kir 18:2x:', [(r['id'], r['igehely'], r['jelentes_hu']) for r in kir])

# 0.5 -------------------------------------------------------------------------
fejezet('0.5 A 21. szabály mintái a lexikon/ lapjain')
with open(os.path.join(GYOKER, 'DONTESEK.md'), encoding='utf-8') as f:
    dontesek = f.read()
with open(os.path.join(GYOKER, 'NYITOTT_FELADATOK.md'), encoding='utf-8') as f:
    nyitott = f.read()
letezo_dt = set(re.findall(r'^\| DT(\d+) \|', dontesek, re.M))
letezo_n = set(re.findall(r'\*\*N(\d+)\b', nyitott))
print('létező DT-sor: %d, létező N-tétel: %d' % (len(letezo_dt), len(letezo_n)))
lapok = sorted(f for f in os.listdir(os.path.join(GYOKER, 'lexikon')) if f.endswith('.md'))
print('| lap | helyőrző DT-F/N-F | Kézzel írandó | a(z) | fordításra vár | DT ref (nem létező) | N ref (nem létező) |')
print('|---|---|---|---|---|---|---|')
reszlet = []
for lap in lapok:
    with open(os.path.join(GYOKER, 'lexikon', lap), encoding='utf-8') as f:
        sz = f.read()
    hely = re.findall(r'\b(?:DT|N)-F\d+[a-z]?\b', sz)
    kezzel = len(re.findall(r'Kézzel írandó', sz))
    az = len(re.findall(r'\ba\(z\)', sz))
    fv = sz.count(LG.FORDITASRA_VAR)
    dt = re.findall(r'(?<![\w-])DT(\d+)\b', sz)
    nn = re.findall(r'(?<![\w-])N(\d+)\b', sz)
    dt_rossz = sorted({d for d in dt if d not in letezo_dt}, key=int)
    n_rossz = sorted({d for d in nn if d not in letezo_n}, key=int)
    print('| %s | %d | %d | %d | %d | %d (%s) | %d (%s) |' % (lap, len(hely), kezzel, az, fv, len(dt),
                                                          ','.join(dt_rossz), len(nn), ','.join(n_rossz)))
    if hely:
        reszlet.append((lap, sorted(set(hely))))
for x in reszlet:
    print('  helyőrzők:', x)

if '--forditas' in sys.argv:
    fejezet('0.5 (iii) fordítatlan egységek: lista_keszit vs. jelölés a renderelt lapon')
    import glossza_lexikon_forditas as GLF  # noqa: E402
    for i in sorted({l.split('_')[0] for l in lapok}):
        ki = tempfile.mkdtemp(prefix='F148_meres_')
        hivasok = GLF.lista_keszit(i, ki)
        hianyzik = sum(1 for v in hivasok.values() if not v)
        jel = 0
        for gy, _, fs in os.walk(ki):
            for fn in fs:
                if fn.startswith(i) and fn.endswith('_TUDOMANYOS.md'):
                    with open(os.path.join(gy, fn), encoding='utf-8') as f:
                        jel += f.read().count(LG.FORDITASRA_VAR)
        print('  %s: hívás %d, hiányzó egyedi egység %d, jelölés a lapon %d' % (i, len(hivasok), hianyzik, jel))
