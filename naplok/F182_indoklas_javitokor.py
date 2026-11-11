"""F182 javítókör (ELLENOR_F182 #8; `sablonok/KESZ_LAP_KOVETELMENY.md` A05, A06, B08): a HAMART-001 jelölt-indoklásainak
(`adat/jeloltek.tsv` `indoklas`) és egy 1/a prózájának (`adat/elofordulasok.tsv` `kapcsolodas`, Jel 22:3) maradék hibái.

- A06 / B08: a héber és a görög írás mellé zárójeles kiejtés. A kiejtés a generátor szabályából jön
  (`lexikon_general.lemma_kiejtes`: jóváhagyott alak, különben a pontozott lemma szabályos kiejtése; a ragozott és a
  szókapcsolati alaknál `heber_gepi` / `gorog_magyaros(gepi_atiras(…))`), nem emlékezetből; a felmérő:
  a scratchpad `indoklas_felmer.py`-ja, a kapu: `olvasoi_kapu.INDOKLAS`.
- A05: az indoklás nem hivatkozik más sorra („az Ez 28:16 sorának folytatása”): a szomszédos verset nevezi meg; az
  elutasítási ok mintája (`adat/elutasitasi_okok.tsv`, HAMART-001, 123) a szöveggel együtt változik, a besorolás nem.
- A05: munkajavaslat nincs az olvasói szövegben („önálló motívum-jelöltként érdemes lehet külön vizsgálatra”); a
  javaslat a nyitott tételek közé került (N-F182l).

Csak a HAMART-001 sorai; szövegcsere a lenti táblával. Minden csere-pár legalább egyszer használt, a változott sorok
száma a várt. TSV: split('\\t') / '\\t'.join(); írás előtt soronkénti összevetés: a célmezőn kívül egyetlen bájt sem
változhat.

Futtatás: python naplok/F182_indoklas_javitokor.py [--ir]
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JELOLTEK = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
ELOFORDULASOK = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
OKOK = os.path.join(GYOKER, 'adat', 'elutasitasi_okok.tsv')

# (régi részlet, új részlet, várt sorszám)
CSERE_JELOLT = [
    # A06/B08: kiejtés (lemma_kiejtes: H6089 ecev, H2336 chóach, H0890 bosá, H7093 kéc, H8414/H0922 tóhú/bóhú,
    # G0173 akantha, G5146 tribolosz, G5351 ftheiró, G5356 fthora, H7451 ra; a szókapcsolati alak: heber_gepi)
    ('rokon H6089 עֶצֶב szót', 'rokon H6089 עֶצֶב (ecev) szót', 16),
    ('(ἄκανθα + τρίβολος együtt)', '(ἄκανθα (akantha) és τρίβολος (tribolosz) együtt)', 11),
    ('(חוֹחַ, בָּאְשָׁה)', '(חוֹחַ (chóach) és בָּאְשָׁה (bosá))', 11),
    ('(קֵץ)', '(קֵץ, kéc)', 4),
    ('(לִפְנֵי)', '(לִפְנֵי, lifné)', 3),
    ('A φθείρω-szócsalád tagja', 'A φθείρω (ftheiró) szócsalád tagja', 1),
    ('ugyanabból a φθείρω-szócsaládból', 'ugyanabból a φθείρω (ftheiró) szócsaládból', 1),
    ('„תהו/בהו — teremtés-visszavonás”', '„תהו/בהו (tóhú/bóhú) — teremtés-visszavonás”', 2),
    ('חַטָּאת — a "bűn" szó', 'חַטָּאת (chattát) — a "bűn" szó', 1),
    ("(vattissáchét há'árec, Nif'ál) + וַתִּמָּלֵא הָאָרֶץ חָמָס —",
     "(vattissáchét háárec, Nif'ál) + וַתִּמָּלֵא הָאָרֶץ חָמָס (vattimmálé háárec chámász) —", 1),
    ('לֹא אֹסִף לְקַלֵּל (ló oszíf lekallél) עוֹד אֶת־הָאֲדָמָה —',
     'לֹא אֹסִף לְקַלֵּל עוֹד אֶת־הָאֲדָמָה (ló oszíf lekallél ód et-háadámá) —', 1),
    ('indoklás (רַע) változatlan', 'indoklás (רַע, ra) változatlan', 1),
    ('a föld (γῆ), ott áll', 'a föld (γῆ, gé), ott áll', 1),
    ('(ἐφθάρη … ἡ γῆ)', '(ἐφθάρη … ἡ γῆ, eftharé … hé gé)', 1),
    ('rokon alak (ἐπάρατος)', 'rokon alak (ἐπάρατος, eparatosz)', 1),
    ('a romlás szava (φθορά) a 8:21-ben', 'a romlás szava (φθορά, fthora) a 8:21-ben', 2),
    # A05: munkajavaslat ki (a javaslat: N-F182l)
    ('— valódi prófétai visszautalás lehet a 6:13-ra, de más kulcsszóval; önálló motívum-jelöltként érdemes lehet külön '
     'vizsgálatra, a motívum jelenlegi lexikai magjához nem tartozik',
     '— prófétai visszautalás lehet az 1Móz 6:13-ra, de más kulcsszóval, ezért a motívum lexikai magjához nem tartozik', 4),
    # A05: nem más sorra, hanem a szomszédos versre hivatkozik
    ('A hely az Ez 28:16 sorának folytatása:', 'A hely a szomszédos vers, az Ez 28:16 folytatása:', 1),
    ('A hely a Mik 6:12 sorának folytatása:', 'A hely a szomszédos vers, a Mik 6:12 folytatása:', 1),
    ('A hely a Róm 8:21 sorának folytatása:', 'A hely a szomszédos vers, a Róm 8:21 folytatása:', 2),
]

CSERE_ELOFORDULAS = [
    ('egyes kiadásaiban κατανάθεμα)', 'egyes kiadásaiban κατανάθεμα, katanathema)', 1),
]

# az elutasítási ok mintája (régi → új), a címke és a besorolás nem változik
OK_CSERE = [('HAMART-001', '^a hely az? .* sorának folytatása', '^a hely a szomszédos vers, az? .* folytatása')]


def mezo_javit(ut, mezo, csere, ir):
    szoveg = io.open(ut, encoding='utf-8', newline='').read()
    sorok = szoveg.split('\n')
    fej = next(s for s in sorok if s and not s.startswith('#')).rstrip('\r').split('\t')
    i_id, i_m = fej.index('id'), fej.index(mezo)
    db = {a: 0 for a, _b, _n in csere}
    uj_sorok, valtozott = [], 0
    for s in sorok:
        if not s or s.startswith('#'):
            uj_sorok.append(s)
            continue
        c = s.split('\t')
        if c[i_id] != 'HAMART-001' or len(c) <= i_m:
            uj_sorok.append(s)
            continue
        ertek = c[i_m]
        for a, b, _n in csere:
            if a in ertek:
                ertek = ertek.replace(a, b)
                db[a] += 1
        if ertek != c[i_m]:
            valtozott += 1
            c[i_m] = ertek
        uj_sorok.append('\t'.join(c))
    rossz = [(a[:50], db[a], n) for a, _b, n in csere if db[a] != n]
    if rossz:
        sys.exit('HIBA (%s): a csere-párok használata eltér a várttól: %r' % (os.path.basename(ut), rossz))
    assert len(uj_sorok) == len(sorok)
    for regi, uj in zip(sorok, uj_sorok):
        if regi == uj:
            continue
        r, u = regi.split('\t'), uj.split('\t')
        assert len(r) == len(u) and r[i_id] == 'HAMART-001'
        assert [x for k, x in enumerate(r) if k != i_m] == [x for k, x in enumerate(u) if k != i_m]
    print('%s: %d HAMART-001 %s-mező változik' % (os.path.basename(ut), valtozott, mezo))
    if ir:
        io.open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(uj_sorok))


def ok_javit(ir):
    okok = io.open(OKOK, encoding='utf-8', newline='').read()
    ok_sorok = okok.split('\n')
    okfej = next(s for s in ok_sorok if s and not s.startswith('#')).split('\t')
    j_id, j_minta = okfej.index('id'), okfej.index('minta')
    uj_ok, db = [], 0
    for s in ok_sorok:
        c = s.split('\t')
        if s and not s.startswith('#') and len(c) > j_minta:
            for mid, a, b in OK_CSERE:
                if c[j_id] == mid and c[j_minta] == a:
                    c[j_minta] = b
                    db += 1
        uj_ok.append('\t'.join(c))
    if db != len(OK_CSERE):
        sys.exit('HIBA: az elutasítási okok cseréje %d, várt %d' % (db, len(OK_CSERE)))
    for regi, uj in zip(ok_sorok, uj_ok):
        if regi != uj:
            r, u = regi.split('\t'), uj.split('\t')
            assert [x for k, x in enumerate(r) if k != j_minta] == [x for k, x in enumerate(u) if k != j_minta]
    print('elutasitasi_okok.tsv: %d minta változik' % db)
    if ir:
        io.open(OKOK, 'w', encoding='utf-8', newline='').write('\n'.join(uj_ok))


if __name__ == '__main__':
    ir = '--ir' in sys.argv
    mezo_javit(JELOLTEK, 'indoklas', CSERE_JELOLT, ir)
    mezo_javit(ELOFORDULASOK, 'kapcsolodas', CSERE_ELOFORDULAS, ir)
    ok_javit(ir)
    print('kiírva' if ir else '(száraz futás; --ir írja)')
