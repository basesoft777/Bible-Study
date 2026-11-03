"""F123 ANTROP-001 új cikk, U4 javítókör (DT-F123r): az ellenőr 12 ELTÉRÉS-ének adatrésze.

Érintett táblák: adat/motivumok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv,
adat/elutasitasi_okok.tsv, adat/szotar_szakasz_cimke.tsv, adat/forditasok.tsv.
Olvasás split('\t'), írás '\t'.join(); minden cél-sort kulccsal azonosít, és
megáll, ha a kulcs nem pontosan egyszer található, vagy a sorok száma változna.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = Path(__file__).resolve().parent.parent
TS = '2026-11-03'

KIVETEL = ('Név szerinti kivétel az 1Kor 2:14–15 ellentétpárja (ψυχικὸς ἄνθρωπος ↔ ὁ πνευματικός), '
           'amely egy érvelés két versben: a 2:15-ben csak a πνευματικός áll, de a mondat a 2:14 '
           'kifejezett szembeállítását közvetlenül folytatja; a kivétel csak ezt a párt engedi, a többi, '
           'csak az egyik szót hordozó vers kint marad.')


def betolt(nev):
    p = GYOKER / 'adat' / nev
    sorok = p.read_text(encoding='utf-8').split('\n')
    return p, sorok


def ment(p, sorok, eredeti_db):
    if len(sorok) != eredeti_db:
        sys.exit(f'HIBA: {p.name} sorszáma változna ({eredeti_db} → {len(sorok)})')
    p.write_text('\n'.join(sorok), encoding='utf-8')


def egy(sorok, felt, leiras):
    talalt = [i for i, s in enumerate(sorok) if s and not s.startswith('#') and felt(s.split('\t'))]
    if len(talalt) != 1:
        sys.exit(f'HIBA: {leiras}: {len(talalt)} találat')
    return talalt[0]


def mezo_csere(sorok, i, j, regi_resz, uj_resz, leiras):
    m = sorok[i].split('\t')
    if regi_resz not in m[j]:
        sys.exit(f'HIBA: {leiras}: a régi szövegrész nincs a mezőben')
    m[j] = m[j].replace(regi_resz, uj_resz)
    sorok[i] = '\t'.join(m)


valtozas = []

# 1. motivumok.tsv — a negatív kritérium név szerinti kivétele (DT-F123r (1))
p, s = betolt('motivumok.tsv'); n0 = len(s)
i = egy(s, lambda m: m[0] == 'ANTROP-001', 'motivumok ANTROP-001')
m = s[i].split('\t')
if KIVETEL not in m[9]:
    m[9] = m[9] + ' ' + KIVETEL
s[i] = '\t'.join(m)
ment(p, s, n0); valtozas.append('motivumok.tsv: negativ_kriterium + kivétel')

# 2. jeloltek.tsv — a mérce szavai (DT-F123r (2)) és a DT28-nyom (DT-F123r (4))
p, s = betolt('jeloltek.tsv'); n0 = len(s)


def jelolt(igehely):
    return egy(s, lambda m: m[0] == 'ANTROP-001' and m[1] == igehely and m[9] == 'elofordulas',
               f'jeloltek ANTROP-001 {igehely}')


i = jelolt('Fil 1:27')
mezo_csere(s, i, 4,
           'A két szó nem megkülönböztető szerepben áll: az „egy lélekben, egy érzéssel” két párhuzamos tagja a közösség egységét fejezi ki, nem az ember két belső rétegét különbözteti meg.',
           'A két szó nem megkülönböztető szerepben áll: a mondat nem szembeállítja, hanem párhuzamos tagként említi egymás mellett; az „egy lélekben, egy érzéssel” két tagja együtt a közösség egységét mondja ki.',
           'Fil 1:27 indoklás')
i = jelolt('1Pét 1:22')
mezo_csere(s, i, 4,
           'A két szó nem megkülönböztető szerepben áll: a lelket Isten Lelke tisztítja meg, a görögben a ψυχή a megtisztított lélek, a πνεῦμα a tisztító Lélek, nem az ember két belső összetevője.',
           'A két szó nem megkülönböztető szerepben áll: a mondat nem szembeállítja, hanem eszközként említi egymás mellett; a lelket Isten Lelke tisztítja meg, a görögben a ψυχή a megtisztított lélek, a πνεῦμα a tisztító Lélek.',
           '1Pét 1:22 indoklás')
i = jelolt('1Pét 3:19-20')
mezo_csere(s, i, 4,
           'A két szó nem megkülönböztető szerepben áll: a „tömlöczben lévő lelkek” (πνεῦμα) és a bárkában megmenekült „nyolcz lélek” (ψυχή) két külön csoport, a mondat nem az ember belső életét tagolja.',
           'A két szó nem megkülönböztető szerepben áll: a mondat nem szembeállítja őket, hanem két külön csoportot nevez meg, a „tömlöczben lévő lelkeket” (πνεῦμα) és a bárkában megmenekült „nyolcz lelket” (ψυχή).',
           '1Pét 3:19-20 indoklás')

REGI8 = ['1Móz 2:7', 'Luk 1:46', 'Luk 1:47', '1Kor 2:14', '1Kor 2:15', '1Kor 15:45', '1Thessz 5:23', 'Zsid 4:12']
NYOM_FK = (' · F123 ANTROP-001 új cikk, U3: a kapcsolodas és a funkcio mező nulláról újraírva '
           '(az 1/a próza, claude-opus-5-5) | scope=manual | forras=adat/elofordulasok.tsv (kapcsolodas, funkcio) | ts=2026-11-03')
NYOM_IND = (' — 2026-11-03 (F123 ANTROP-001 új cikk, U3; DT-F123r (4)): a sor kapcsolodas és funkcio mezője '
            'nulláról újraírva, a régi szöveg archívumban (archivum/ANTROP-001/ANTROP-001_1a_proza_regi.tsv); '
            'döntés: beépítve, a hely és a gerinc-elem nem változott.')
for ih in REGI8:
    i = jelolt(ih)
    m = s[i].split('\t')
    if m[3] != 'beépítve':
        sys.exit(f'HIBA: {ih}: a jelölt nem beépítve')
    if NYOM_FK not in m[2]:
        m[2] += NYOM_FK
    if NYOM_IND not in m[4]:
        m[4] += NYOM_IND
    if ih == '1Kor 2:15':
        kiv = (' A negatív kritérium név szerinti kivétele (DT-F123r (1)): az 1Kor 2:14–15 ellentétpárja egy '
               'érvelés két versben; a 2:15 a 2:14 kifejezett szembeállítását közvetlenül folytatja.')
        if kiv not in m[4]:
            m[4] += kiv
    s[i] = '\t'.join(m)
ment(p, s, n0); valtozas.append('jeloltek.tsv: 3 indoklás (mérce), 8 DT28-nyom, 1Kor 2:15 kivétel')

# 3. elofordulasok.tsv — a 8 újraírt sor proveniencia-mezője a jelöltsorra mutat (DT-F123r (4))
p, s = betolt('elofordulasok.tsv'); n0 = len(s)
REGI_PROV = 'scope=manual | forras=Pneuma_pszukhe_megkulonboztetes_tematikus.md | ts=2026-08-22'
UJ_PROV = ('scope=manual | forras=F123 ANTROP-001 új cikk, U3: a kapcsolodas és a funkcio nulláról '
           '(DT-F123r (4); jeloltek.tsv beépítve; az eredeti beépítés forrása: Pneuma_pszukhe_megkulonboztetes_tematikus.md, 2026-08-22) | ts=2026-11-03')
for ih in REGI8:
    i = egy(s, lambda m, ih=ih: m[0] == 'ANTROP-001' and m[1] == ih, f'elofordulasok {ih}')
    m = s[i].split('\t')
    if m[15] != REGI_PROV:
        sys.exit(f'HIBA: {ih}: váratlan proveniencia: {m[15]}')
    m[15] = UJ_PROV
    s[i] = '\t'.join(m)
ment(p, s, n0); valtozas.append('elofordulasok.tsv: 8 proveniencia')

# 4. elutasitasi_okok.tsv — az ok megjegyzése a kritérium szavaival (DT-F123r (2))
p, s = betolt('elutasitasi_okok.tsv'); n0 = len(s)
i = egy(s, lambda m: m[1] == 'ANTROP-001' and m[2] == '^a két szó nem megkülönböztető', 'elutasítási ok 2')
mezo_csere(s, i, 4,
           'a két szó egy mondatban áll, de nem az ember két belső összetevőjét különbözteti meg',
           'a két szó egy mondatban áll, de a mondat nem szembeállítja és nem különbözteti meg őket (például eszközként vagy párhuzamos tagként állnak egymás mellett)',
           'elutasítási ok 2 megjegyzés')
ment(p, s, n0); valtozas.append('elutasitasi_okok.tsv: 1 megjegyzés')

# 5. szotar_szakasz_cimke.tsv — a G5590 2. címke a 2.a–2.c-t fedi (E6)
p, s = betolt('szotar_szakasz_cimke.tsv'); n0 = len(s)
i = egy(s, lambda m: m[0] == 'Thayer' and m[1] == 'G5590' and m[2] == '-/2/-', 'cimke G5590 -/2/-')
mezo_csere(s, i, 4, 'a lélek mint az érzelmek és a vágyak székhelye',
           'a lélek: az érzések és a vágyak székhelye, az üdvösségre rendelt, a testtől különböző belső valóság',
           'G5590 címke')
ment(p, s, n0); valtozas.append('szotar_szakasz_cimke.tsv: G5590 -/2/-')

# 6. forditasok.tsv — a G4152 sz7 kézi javítása (E12)
p, s = betolt('forditasok.tsv'); n0 = len(s)
i = egy(s, lambda m: m[0] == 'Thayer' and m[1] == 'G4152' and m[2] == 'G4152' and m[3] == 'sz7' and m[7] != 'elavult',
        'forditas G4152 sz7')
mezo_csere(s, i, 6, 'és ezzel szemben találjuk: σωματικον Plutarkhosznál, mor.,',
           'Plutarkhosznál pedig a σωματικον ellentéteként áll, mor.,', 'G4152 sz7')
m = s[i].split('\t')
m[7] = 'kezi'
m[8] = 'claude-opus-5-5'
m[9] = '2026.11.03'
m[11] = 'a 2026-11-03-i független ellenőrzés E12 tétele szerint javítva; eredeti: Code-session sonnet'
s[i] = '\t'.join(m)
ment(p, s, n0); valtozas.append('forditasok.tsv: G4152 sz7 kezi')

print('\n'.join(valtozas))
