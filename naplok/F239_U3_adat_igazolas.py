"""F239 U3 — adat-igazolás a próza előtt.

Összeveti a TEREMT-001 adatsorait a szerkesztő döntéseivel (DT-F239a–d,
`dontesek/uj/nervous-kare-9d2361.md`). Csak olvas; eltérésnél nem javít,
hanem kiírja. Futtatás: python naplok/F239_U3_adat_igazolas.py
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GYOKER = Path(__file__).resolve().parent.parent
ADAT = GYOKER / 'adat'
ID = 'TEREMT-001'


def olvas(nev):
    sorok = (ADAT / nev).read_text(encoding='utf-8').split('\n')
    fej = None
    ki = []
    for s in sorok:
        if not s or s.startswith('#'):
            continue
        mezok = s.split('\t')
        if fej is None:
            fej = mezok
            continue
        ki.append(dict(zip(fej, mezok + [''] * (len(fej) - len(mezok)))))
    return ki


hibak = []


def ell(felt, uzenet):
    print(('OK   ' if felt else 'HIBA ') + uzenet)
    if not felt:
        hibak.append(uzenet)


# 1. jeloltek.tsv
jel = [r for r in olvas('jeloltek.tsv') if r['id'] == ID]
elof_j = [r for r in jel if r['jelolt_tipus'] == 'elofordulas']
mk_j = [r for r in jel if r['jelolt_tipus'] == 'motivumkozi']
dontesek = {}
for r in elof_j:
    dontesek[r['dontes']] = dontesek.get(r['dontes'], 0) + 1
ell(dontesek.get('beépítve', 0) == 43, f"jeloltek: beépítve = {dontesek.get('beépítve', 0)} (várt 43)")
ell(dontesek.get('elutasítva', 0) == 32, f"jeloltek: elutasítva = {dontesek.get('elutasítva', 0)} (várt 32)")
ell(dontesek.get('nyitva', 0) == 0, f"jeloltek: nyitva = {dontesek.get('nyitva', 0)} (várt 0)")
egyeb = {k: v for k, v in dontesek.items() if k not in ('beépítve', 'elutasítva', 'nyitva')}
ell(not egyeb, f"jeloltek: más döntésérték nincs ({egyeb})")
jh = {r['igehely']: r['dontes'] for r in elof_j}
ell(jh.get('Jel 20:1') == 'beépítve', f"jeloltek: Jel 20:1 = {jh.get('Jel 20:1')}")
ell(jh.get('Jel 20:3') == 'beépítve', f"jeloltek: Jel 20:3 = {jh.get('Jel 20:3')}")
ell('Jel 20:1-3' not in jh and 'Jel 20:1–3' not in jh, "jeloltek: Jel 20:1-3 tartomány nincs")
kulcsok = [(r['igehely'], r['jelolt_tipus'], r['cel_id']) for r in jel]
ell(len(kulcsok) == len(set(kulcsok)), "jeloltek: kulcs-duplikátum nincs")
ell(len(mk_j) == 1, f"jeloltek: motívumközi sor = {len(mk_j)} (várt 1)")
if mk_j:
    m = mk_j[0]
    ell(m['cel_id'] == 'ALVIL-001' and m['igehely'] == 'Ez 31:15' and m['dontes'] == 'beépítve',
        f"jeloltek: motívumközi = {m['cel_id']} {m['igehely']}→{m['cel_igehely']} {m['dontes']}")
# a másik irányú motívumközi sorok (cel_id = TEREMT-001) ALVIL-lel
mk_be = [r for r in olvas('jeloltek.tsv') if r['cel_id'] == ID and r['id'] == 'ALVIL-001']
print(f"info jeloltek: ALVIL-001 → TEREMT-001 irányú sor: {len(mk_be)}")

# 2. elofordulasok.tsv
elo = [r for r in olvas('elofordulasok.tsv') if r['id'] == ID]
ell(len(elo) == 43, f"elofordulasok: {len(elo)} sor (várt 43)")
eh = [r['igehely'] for r in elo]
ell(len(eh) == len(set(eh)), "elofordulasok: igehely-duplikátum nincs")


def versszam(ih):
    hely = ih.rsplit(' ', 1)[1]
    fej, v = hely.split(':')
    if '-' in v or '–' in v:
        a, b = v.replace('–', '-').split('-')
        return int(b) - int(a) + 1
    return 1


vers = sum(versszam(i) for i in eh)
ell(vers == 44, f"elofordulasok: {vers} vers (várt 44)")
ell('Jel 20:1' in eh and 'Jel 20:3' in eh and 'Jel 20:1-3' not in eh, "elofordulasok: Jel 20:1 és 20:3 külön, tartomány nincs")
ell(set(eh) == {r['igehely'] for r in elof_j if r['dontes'] == 'beépítve'},
    "elofordulasok = jeloltek beépített igehelyei")
tartomany = [i for i in eh if '-' in i.rsplit(':', 1)[1]]
print(f"info elofordulasok: tartományok: {tartomany}")
ures_funkcio = [r['igehely'] for r in elo if not r['funkcio'].strip()]
print(f"info elofordulasok: üres funkcio: {ures_funkcio}")

# 3. motivum_kapcsolatok.tsv
mk = [r for r in olvas('motivum_kapcsolatok.tsv') if ID in (r['id_a'], r['id_b'])]
ell(len(mk) == 1, f"motivum_kapcsolatok: {len(mk)} TEREMT-001 sor (várt 1)")
for r in mk:
    ell(r['id_a'] == 'ALVIL-001' and r['id_b'] == ID and r['igehely_a'] == 'Ez 31:15'
        and r['igehely_b'] == 'Ez 31:15' and r['tipus'] == 'közös_igehely',
        f"motivum_kapcsolatok: {r['id_a']} {r['igehely_a']} – {r['id_b']} {r['igehely_b']} {r['tipus']}")

# 4. tematikus_temak.tsv
tt = [r for r in olvas('tematikus_temak.tsv') if r['id'] == ID]
ell(len(tt) == 11, f"tematikus_temak: {len(tt)} sor (várt 11)")
tk = [(r['forras'], r['tema_id']) for r in tt]
ell(len(tk) == len(set(tk)), "tematikus_temak: duplikátum nincs")
kiv = {r['tema'] for r in tt if r['dontes'] == 'kivalasztott'}
kiz = {r['tema'] for r in tt if r['dontes'] == 'kizart'}
til = {r['tema'] for r in tt if r['dontes'] == 'tiltott'}
ell(kiv == {'PIT', 'EARTH', 'DEW', 'PSALMS'}, f"tematikus_temak: kiválasztott = {sorted(kiv)}")
ell(kiz == {'EPIC', 'SONG', 'POETRY', 'ANIMALS', 'CONTINENTS', 'MANASSEH', 'EPHRAIM'},
    f"tematikus_temak: kizárt = {sorted(kiz)}")
ell(not til, f"tematikus_temak: tiltott = {sorted(til)}")
print("info tematikus_temak forras:", sorted({r['forras'] for r in tt}))

# 5. motivumok.tsv
mot = [r for r in olvas('motivumok.tsv') if r['id'] == ID]
ell(len(mot) == 1, f"motivumok: {len(mot)} sor")
UJ = 'az Újszövetségben a görög ἄβυσσος (abüsszosz) szót, a Septuaginta tehóm-fordításának szavát'
if mot:
    nk = mot[0]['negativ_kriterium']
    ell(UJ in nk, "motivumok: a kizárási szabály új szövege benne van")
    ell('LXX-közvetített' not in nk, "motivumok: a régi „LXX-közvetített” fordulat nincs")
    print("info negativ_kriterium:", nk)

print()
print('ÖSSZESEN:', 'nincs eltérés' if not hibak else f'{len(hibak)} eltérés')
sys.exit(1 if hibak else 0)
