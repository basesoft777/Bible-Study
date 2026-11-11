"""F182 (3. menet; A05, A06, A22 — `sablonok/KESZ_LAP_KOVETELMENY.md` K47, K48, K07): a HAMART-001 jelöltjeinek
indoklás-mezője (`adat/jeloltek.tsv`) olvasói alakra.

- A05 (K47): az indoklás nem hivatkozik más sorra („Ugyanaz az indok, mint …”), a „tanulmány”-ra / „study”-ra és a
  „napló”-ra; a belső jel („Q4”, „napló 4/c”) kimarad.
- A06 (K48, F4 és kiegészítése; B08 döntése): helyes névelő, a héber szó írással és zárójeles kiejtéssel
  („az אָרַר (árar)”), csupasz átírás nélkül.
- A22 (K07): egy szónak egy kiejtése (adámá, árar, chámász; a ragozott alak a saját kiejtésével).

Csak a HAMART-001 sorai; csak az `indoklas` mező; szövegcsere a lenti táblával (a teljes régi részlet → az új). Az
`adat/elutasitasi_okok.tsv` mintái a szöveg mellett frissülnek (az elutasítási ok besorolása nem változhat — a generátor
`BeNemSorolhato` hibája őrzi). TSV: split('\\t') / '\\t'.join(); írás előtt soronkénti összevetés: a HAMART-001 indoklás-
mezőin kívül egyetlen bájt sem változhat.

Futtatás: python naplok/F182_indoklas_javitas.py [--ir]
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JELOLTEK = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
OKOK = os.path.join(GYOKER, 'adat', 'elutasitasi_okok.tsv')

CSERE = [
    # A06/A22: az átok-kimondás csoport (29 sor) — a felhasználó javasolt mondata (F4 kiegészítés)
    ('Az arar itt rituális, jogi vagy indulati átok-kimondás',
     'Az אָרַר (árar) itt rituális, jogi vagy indulati átok-kimondás'),
    ('A arar önmagában nem a motívum, csak annak egyik eszköze; a motívum a arar + adamá együttállásán és a fokozási '
     'soron áll',
     'Az אָרַר (árar) önmagában nem a motívum, csak egyik eszköze: a motívumot az אָרַר (árar) és az אֲדָמָה (adámá) '
     'együttállása és a fokozás sora hordozza'),
    ('Szövetségi átok-szakaszok, amelyek nem az arar igét használják (a H0779-scan szerint az 5Móz-ből',
     'Szövetségi átok-szakaszok, amelyek nem az אָרַר (árar) igét használják (a Strong-keresés szerint az 5Móz-ből'),
    ('semleges, narratív adamá-használat, nem az átok-szerkezetben (napló 4/c, H0127 sor: genezisen belüli határeset)',
     'semleges, elbeszélő használat: az אֲדָמָה (adámá) itt nem az átok-szerkezetben áll (genezisen belüli határeset)'),
    ('Bujdosás/száműzetés mint büntetés; a adamá kulcsszó nélkül',
     'Bujdosás/száműzetés mint büntetés; az אֲדָמָה (adámá) szava nélkül'),
    ('אֲדָמָה (adamá)', 'אֲדָמָה (adámá)'),
    ("(arúrá há'adamá ba'avúrekhá)", "(arúrá háadámá baavúrechá)"),
    ("(árúr attá min-há'adamá)", '(árúr attá min-háadámá)'),
    ('עִצְּבוֹן (itzevón)', 'עִצְּבוֹן (iccevón)'),
    # A05: más motívumra / a naplóra / a tanulmányra hivatkozó indoklás
    ('"Természet szerint a harag fiai" — az öröklött bűnösség kérdése, amelyet a study explicit módon NEM dönt el '
     '(l. ⚠️ Vitatott pontok)',
     '„Természet szerint a harag fiai” — az öröklött bűnösség kérdése, amelyet a lap nem dönt el (l. a 9. Értelmezés '
     'vitatott pontjait)'),
    ('Nimród, ill. Sodoma — a naplóban mindkettő önálló motívum ("vadász gyök", "Sodoma bűnössége")',
     'Nimród, ill. Sodoma — mindkettő egy másik, önálló motívum tárgya („vadász gyök”, „Sodoma bűnössége”)'),
    ('A Jer 4:23 a naplóban már rögzített "תהו/בהו — teremtés-visszavonás" motívum ([ID: TEREMT-002]) tagja — '
     'kereszt-motívum szennyeződés elkerülése (Q4)',
     'A Jer 4:23 a „תהו/בהו — teremtés-visszavonás” motívum ([ID: TEREMT-002]) tagja: egy másik motívum tárgya'),
    ('genezisi chámász-előfordulás, de az 1Móz 16:5-ben személyközi sérelem, az 1Móz 49:5-ben fegyverjelző; egyik sem a '
     'föld megtelésének szerkezete (napló 4/c, H2555 sor megjegyzése)',
     'a חָמָס (chámász) genezisi előfordulása, de az 1Móz 16:5-ben személyközi sérelem, az 1Móz 49:5-ben fegyverjelző; '
     'egyik sem a föld megtelésének szerkezete'),
    ('lexikai finomság: az ígéret nem a 3:17 arar-t vonja vissza, hanem egy másik igét (קָלַל, kalal, H7043) tagad meg',
     'lexikai finomság: az ígéret nem a 3:17 átok-igéjét, az אָרַר (árar) igét vonja vissza, hanem egy másik igét, a '
     'קָלַל (kálal) igét tagadja meg'),
    ('"A föld megfertőztetett lakosai alatt... ezért átok emészti meg a földet" — a föld/átok/lakosok hármas szerkezete '
     'azonos a 1Móz 3:17-tel, de más szóval: אָלָה (álá, H0423), nem arar ⇒ tematikus, nem lexikai',
     '„A föld megfertőztetett lakosai alatt... ezért átok emészti meg a földet” — a föld, az átok és a lakosok hármas '
     'szerkezete azonos az 1Móz 3:17-tel, de más szóval: az אָלָה (álá), nem az אָרַר (árar); ezért tematikus, nem '
     'lexikai'),
    ('"Csalárdabb a szív mindennél" — a szív romlottsága a "jetzer — a szív romlott hajlama" motívum tárgya, amely a '
     'naplóban önálló tételként szerepel. Kereszt-motívum szennyeződés elkerülése (Q4)',
     '„Csalárdabb a szív mindennél” — a szív romlottsága a „jécer — a szív romlott hajlama” motívum tárgya, amely önálló '
     'tétel: egy másik motívum tárgya'),
    ('Ugyanaz az indok, mint Jer 17:9-nél',
     'A szív romlottsága a „jécer — a szív romlott hajlama” motívum tárgya, amely önálló tétel: egy másik motívum tárgya'),
    ('az erőszak (chámász, a Károliban „álnokság”), a föld (adamá)', 'az erőszak (chámász, a Károliban „álnokság”), a föld '
     '(adámá)'),
    ('az אֲדָמָה (adamá, föld, talaj) szava', 'az אֲדָמָה (adámá: föld, talaj) szava'),
]

# második menet (`--masodik`): a lapon az ok címkéje („egy másik motívum tárgya”) a mondat előtt áll, a mondat végén nem
# ismétlődik
CSERE2 = [
    (', amely önálló tétel: egy másik motívum tárgya', ', amely önálló tétel'),
    ('([ID: TEREMT-002]) tagja: egy másik motívum tárgya', '([ID: TEREMT-002]) tagja'),
]

# az elutasítási okok mintái (a régi minta → az új): a besorolás nem változik
OK_CSERE = [
    ('HAMART-001', 'arar itt rituális', r'\(árar\) itt rituális'),
    ('HAMART-001', 'nem az arar igét', r'\(árar\) igét'),
    ('HAMART-001', '^ugyanaz az indok, mint jer 17:9', 'romlott hajlama” motívum tárgya'),
]
OK_CIMKE_CSERE = [
    ('HAMART-001', 'az öröklött bűnösség kérdése, amelyet a tanulmány nem dönt el',
     'az öröklött bűnösség kérdése, amelyet a lap nem dönt el'),
]


def javit(ir, csere=None, okok_is=True):
    csere = CSERE if csere is None else csere
    szoveg = io.open(JELOLTEK, encoding='utf-8', newline='').read()
    sorok = szoveg.split('\n')
    fej = next(s for s in sorok if s and not s.startswith('#')).split('\t')
    i_id, i_ind = fej.index('id'), fej.index('indoklas')
    uj_sorok, valtozott, hasznalt = [], 0, set()
    for s in sorok:
        if not s or s.startswith('#'):
            uj_sorok.append(s)
            continue
        c = s.split('\t')
        if c[i_id] != 'HAMART-001' or len(c) <= i_ind:
            uj_sorok.append(s)
            continue
        ind = c[i_ind]
        for a, b in csere:
            if a in ind:
                ind = ind.replace(a, b)
                hasznalt.add(a)
        if ind != c[i_ind]:
            valtozott += 1
            c[i_ind] = ind
        uj_sorok.append('\t'.join(c))
    nem = [a for a, _b in csere if a not in hasznalt]
    if nem:
        sys.exit('HIBA: nem használt csere: %r' % nem)
    # összevetés: csak a HAMART-001 indoklás-mezője változhat
    assert len(uj_sorok) == len(sorok)
    for regi, uj in zip(sorok, uj_sorok):
        if regi == uj:
            continue
        r, u = regi.split('\t'), uj.split('\t')
        assert len(r) == len(u) and r[i_id] == 'HAMART-001'
        assert [x for k, x in enumerate(r) if k != i_ind] == [x for k, x in enumerate(u) if k != i_ind]
    print('jeloltek.tsv: %d HAMART-001 indoklás változik' % valtozott)
    if not okok_is:
        if ir:
            io.open(JELOLTEK, 'w', encoding='utf-8', newline='').write('\n'.join(uj_sorok))
            print('kiírva')
        return

    okok = io.open(OKOK, encoding='utf-8', newline='').read()
    ok_sorok = okok.split('\n')
    okfej = next(s for s in ok_sorok if s and not s.startswith('#')).split('\t')
    j_id, j_minta, j_cimke = okfej.index('id'), okfej.index('minta'), okfej.index('cimke')
    uj_ok, db = [], 0
    for s in ok_sorok:
        c = s.split('\t')
        if s and not s.startswith('#') and len(c) > j_cimke:
            for mid, a, b in OK_CSERE:
                if c[j_id] == mid and c[j_minta] == a:
                    c[j_minta] = b
                    db += 1
            for mid, a, b in OK_CIMKE_CSERE:
                if c[j_id] == mid and c[j_cimke] == a:
                    c[j_cimke] = b
                    db += 1
        uj_ok.append('\t'.join(c))
    if db != len(OK_CSERE) + len(OK_CIMKE_CSERE):
        sys.exit('HIBA: az elutasítási okok cseréje %d, várt %d' % (db, len(OK_CSERE) + len(OK_CIMKE_CSERE)))
    print('elutasitasi_okok.tsv: %d mező változik' % db)
    if ir:
        io.open(JELOLTEK, 'w', encoding='utf-8', newline='').write('\n'.join(uj_sorok))
        io.open(OKOK, 'w', encoding='utf-8', newline='').write('\n'.join(uj_ok))
        print('kiírva')


if __name__ == '__main__':
    if '--masodik' in sys.argv:
        javit('--ir' in sys.argv, CSERE2, okok_is=False)
    else:
        javit('--ir' in sys.argv)
