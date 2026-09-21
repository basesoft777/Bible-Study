# -*- coding: utf-8 -*-
"""
N14.1 -- a HAMART-001 retroaktiv betoltesenek egyszeri jegyzokonyv-szkriptje
(N14_BRIEF.md G1-G6, az f3_1_betoltes.py mintajara).

A study (`tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md`) 1.
pontjanak A/B/C tablazatat a G2-G4 dontesek szerint dolgozza fel: soronkent
`gerinc_elem`-et rendel (G2), `,`/`/` menten sorokra bont (G3), `fo_elofordulas`
csoportkulcsot ad (G4), es a `motivumok.tsv`/`jeloltek.tsv` sorat epiti (G5-G6).

Minden sor eloszor memoriaban all ossze es hossz-ellenorzesen at kell mennie,
csak utana irodik lemezre a harom munkalapra -- igy egyetlen elgepelt
mezoszam sem torhet el csendben egy TSV-oszlopot (f3_1_betoltes.py elve).

Ez a szkript NEM resze a lekerdez.py/betolt.py/ellenoriz.py eszkoztarnak --
csak ennek az N14 menetnek a jegyzokonyve. `--ir` nelkul (1. menet) soha
nem ir eles `adat/`-at, csak a harom munkalapot es a jelentest. `--ir`-rel
(N14.2, 2. menet) a `motivumok.tsv` es a `jeloltek.tsv` sorait fuzi az eles
`adat/` vegehez -- az `elofordulasok.tsv`-t ez a szkript SOHA nem irja,
azt a `betolt.py beepit --ir` vegzi kulon lepesben (F8 atjaro).

CLI:
    python eszkozok/n14_hamart_betoltes.py --naplok DIR             # proba
    python eszkozok/n14_hamart_betoltes.py --ir --adat DIR          # eles iras
"""

import argparse
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import lekerdez as L  # noqa: E402 -- csak import, nem sajat parse_range/scan (K5)
import general as G  # noqa: E402 -- csak import, nem sajat TSV-olvaso (K5)

ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')

STUDY = 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md'
PROV = 'scope=manual | forras=%s | ts=2026-09-11' % STUDY

ELOFORDULASOK_FEJLEC = [
    'id', 'igehely', 'kapcsolodas', 'pardes_szint', 'funkcio', 'gerinc_elem',
    'strong', 'lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam',
    'jelentes_en', 'jelentes_hu', 'karoli_szo', 'azonositas_modja',
    'megbizhatosag', 'proveniencia', 'igazolas', 'fo_elofordulas',
    'felmerult_tanulmany',
]

# ---------------------------------------------------------------------------
# G4 -- fo_elofordulas csoportok (a napló ⭐ bekezdésének négy szó szerinti
# szakasz-megnevezése)
# ---------------------------------------------------------------------------

FO_ELOFORDULAS_CSOPORTOK = ['1Móz 3:7-19', '1Móz 4:1-24', '1Móz 6:1-8', '1Móz 6:9-22']


def fo_elofordulas(igehely):
    rng = L.parse_range(igehely)
    for csoport in FO_ELOFORDULAS_CSOPORTOK:
        crng = L.parse_range(csoport)
        book, ch, v = rng[1], rng[2], rng[3]
        if L.in_range(crng, book, ch, v):
            return csoport
    return ''


# ---------------------------------------------------------------------------
# G2 -- gerinc_elem / strong származtatása
# ---------------------------------------------------------------------------

TEMATIKUS_HORGONY = {
    'Ézs 24:5-6': '1Móz 3:17',
    'Hós 4:1-3': '1Móz 3:17',
    'Mt 15:19': '1Móz 6:5',
    'Mk 7:21-23': '1Móz 6:5',
    '2Pét 3:6-7': '1Móz 6:13',
}

C_GERINC_KESZLET = ['G1944', 'G2671', 'G5356', 'G1311', 'G5351']


def gerinc_es_strong_ab(igehely, strong_oszlop, bdb_entry_id):
    """(gerinc_elem, strong) egy A/B-táblás sorhoz -- G2 1-3. szabály."""
    if igehely in TEMATIKUS_HORGONY:
        return 'tematikus:%s' % TEMATIKUS_HORGONY[igehely], ''
    strongok = {s.strip() for s in strong_oszlop.split(',')}
    if 'H4390' in strongok and 'H2555' in strongok and bdb_entry_id == 'H2555':
        return 'málé+chámász', 'H2555'
    if 'H8085' in strongok and 'H2555' in strongok and bdb_entry_id == 'H2555':
        return 'sámá+chámász', 'H2555'
    entry = bdb_entry_id.replace(' / ', '+').replace('/', '+').strip()
    if '+' in entry:
        return entry, entry.split('+')[0]
    return entry, entry


def gerinc_es_strong_c(igehely, strong_oszlop):
    """(gerinc_elem, strong) egy C-táblás sorhoz -- G2 4. szabály."""
    if igehely in TEMATIKUS_HORGONY:
        return 'tematikus:%s' % TEMATIKUS_HORGONY[igehely], ''
    strongok = [s.strip() for s in strong_oszlop.split(',')]
    for s in strongok:
        if s in C_GERINC_KESZLET:
            return s, s
    raise ValueError('C-táblás sor gerinc-elem nélkül: %s (%s)' % (igehely, strong_oszlop))


# ---------------------------------------------------------------------------
# PaRDeS-szint / felmerült tanulmány szétválasztása (SEMA 2.2 / G2)
# ---------------------------------------------------------------------------

def split_pardes(cell):
    cell = cell.strip()
    if ' — ' in cell:
        szint, rest = cell.split(' — ', 1)
    elif ' (' in cell:
        i = cell.index(' (')
        szint, rest = cell[:i], cell[i + 1:]
    else:
        szint, rest = cell, ''
    szint = szint.strip()
    rest = rest.strip().strip('()').replace('**', '').replace('`', '').strip()
    return szint, rest


def split_jelentes(cell):
    """(jelentes_en, jelentes_hu) -- a 【NAPLO: ...】 megjegyzés nélkül."""
    cell = re.sub(r'【NAPLO:.*?】', '', cell).strip()
    if not cell or cell == '—':
        return '', ''
    m = re.match(r'^"(.*)"\s*—\s*magyarul:\s*"(.*)"$', cell)
    if m:
        return m.group(1), m.group(2)
    m2 = re.match(r'^"(.*)"$', cell)
    if m2:
        return m2.group(1), ''
    m3 = re.match(r'^magyarul:\s*"(.*)"$', cell)
    if m3:
        return '', m3.group(1)
    return cell, ''


def strip_kapcsolodas_markdown(szoveg):
    """A `kapcsolodas` mező markdown-jelölése (`*`, backtick) eltávolítva --
    N14.1a 3. pont: a meglévő 201 elofordulasok-sor egyike sem hordoz
    ilyen jelölést, adatréteg-konzisztencia."""
    return szoveg.replace('*', '').replace('`', '')


# N14.1a -- a fuggetlen ellenorzes ket elemzesi hibaja a szkriptben javitva
# (nem kezzel a munkalapon, D13): a split_jelentes() ketszeres BDB-cellat
# (1Moz 3:18) es zarojeles binyan-megjegyzest (1Moz 8:21) nem tud tisztan
# szetvalasztani -- ezt a ket sort a study szovege alapjan explicit iras
# feluliraja, a `gerinc_elem` valtozatlan marad.
JELENTES_FELULIRAS = {
    '1Móz 3:18': {
        'lexikon_entry_id': 'H6975',
        'jelentes_szam': '1',
        'jelentes_en': 'thornbush, thorn ... Gen 3:18',
        'jelentes_hu': 'tövisbokor, tövis',
    },
    '1Móz 8:21': {
        'jelentes_en': "be slight, of water, be abated; Pi'él: curse",
        'jelentes_hu': "csekélynek lenni, vízről: apadni; Pi'él: megátkozni",
    },
}


SENSE_ERVENYES = {
    "Qal pass. ptc.", "Pi'él", "Qal impf.", "Nif'ál", "Hif'íl",
    "Nif'ál / Hif'íl",
}


def sense_ervenyes(ertek):
    ertek = ertek.strip()
    if not ertek or ertek == '—':
        return True  # üres -- nem kihagyás, csak nincs sense
    if ertek in SENSE_ERVENYES:
        return True
    if re.match(r'^\d+[a-z]?$', ertek):
        return True
    return False


# ---------------------------------------------------------------------------
# A study 1. pontjának A/B/C táblázata -- a study szövegéből szó szerint
# átvéve (tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md,
# 1. pont). Minden mezőt a study saját cellája ad; nincs generált/kitalált
# érték. Oszlopsorrend a study fejléce szerint.
# ---------------------------------------------------------------------------

# (igehely_lista, kapcsolodas, pardes_cella, strong_oszlop, bdb_entry_id,
#  sense, jelentes_cella)
# igehely_lista: G3 szerint a ','/'/' mentén szétbontott igehelyek (a
# kötőjeles tartomány EGY elemű listaként marad).

TABLA_A = [
    (['1Móz 3:14'],
     'אָרוּר (*árúr*) — az átok első kimondása, a kígyóra',
     'Peshat (`1Moz_3v7-24_bovitett.md`)', 'H0779', 'H0779', 'Qal pass. ptc.',
     '"curse ... chiefly as exclamation, || בָּרוּךְ" — magyarul: "átkozott — jellemzően felkiáltásként, ellentétpárja: áldott"'),
    (['1Móz 3:16'],
     'עִצְּבוֹנֵךְ (*itzevónékh*) — a fájdalom az asszonyra',
     'Peshat (`1Moz_3v7-24_bovitett.md`)', 'H6093', 'H6093', '—',
     '"pain, toil ... suffix עִצְּבוֹנֵךְ 3:16 (of travail)" — magyarul: "fájdalom, gyötrelmes fáradság — birtokos raggal, vajúdás értelemben"'),
    (['1Móz 3:17'],
     "אֲרוּרָה הָאֲדָמָה בַּעֲבוּרֶךָ (*arúrá há'adamá ba'avúrekhá*) — nem az ember átkoztatik meg, hanem a **föld** miatta; a következmény az elkövetőn kívülre lép",
     'Peshat/Drash (`1Moz_3v7-24_bovitett.md`)', 'H0779, H0127, H6093', 'H0127', '1',
     '"ground (as tilled, yielding sustenance)" — magyarul: "föld (mint megművelt, terményt adó talaj)"'),
    (['1Móz 3:18'],
     "קוֹץ וְדַרְדַּר (*kóc vedardar*) — tövis és bogáncs mint az átkozott föld terméke",
     'Peshat (`1Moz_3v7-24_bovitett.md`)', 'H6975, H1863', 'H6975 / H1863', '1 / —',
     '"thornbush, thorn ... Gen 3:18" — magyarul: "tövisbokor, tövis" / "thistles (collective) ... Gen 3:18" — magyarul: "bogáncsok (gyűjtőnév), a vadon/puszta jelképe"'),
    (['1Móz 3:19', '1Móz 3:23'],
     "אֲדָמָה (*adamá*) — a föld, amelybe visszatér, és amelyhez kiűzetve odaköttetik",
     'Peshat (`1Moz_3v7-24_bovitett.md`)', 'H0127', 'H0127', '3',
     '"earth as material substance; of which man is made" — magyarul: "föld mint anyagi szubsztancia; amelyből az ember lett"'),
    (['1Móz 4:2-3'],
     'אֲדָמָה (*adamá*) — Kain "földmívelő", és a földből hozza áldozatát: az átkozott föld a testvéri konfliktus színtere',
     'Peshat (`1Moz_4v1-24_bovitett.md`)', 'H0127', 'H0127', '1',
     '"ground (as tilled, yielding sustenance)" — magyarul: "föld (mint megművelt, terményt adó talaj)"'),
    (['1Móz 4:7'],
     'חַטָּאת — a "bűn" szó **első előfordulása** a Szentírásban, nem áldozatként, hanem az ajtóban leselkedő hatalomként',
     'Peshat/Drash (`1Moz_4v1-24_bovitett.md`)', 'H2403', 'H2403', '1',
     '"רבץ חטאת לפתח Gen 4:7 (J) at the door (of Cain) sin is a crouching beast" — magyarul: "a bűn az ajtóban (Kainénál) leselkedő vadállat"'),
    (['1Móz 4:10-11'],
     "אָרוּר אַתָּה מִן־הָאֲדָמָה (*árúr attá min-há'adamá*) — **fokozás**: most már nem a föld, hanem a személy az átok alanya, és éppen a föld felől; ugyanaz a két szó, felcserélt szereposztásban",
     'Peshat/Remez (`1Moz_4v1-24_bovitett.md`)', 'H0779, H0127', 'H0779', 'Qal pass. ptc.',
     '"curse ... Gen 3:14, 17; 4:11; 9:25" — magyarul: "átkozott — l. Gen 3:14, 17; 4:11; 9:25"'),
    (['1Móz 4:12', '1Móz 4:14'],
     "אֲדָמָה (*adamá*) — a föld megtagadja termőerejét, és Kain elűzetik róla: a 3:17-19 büntetés megismételve, szigorítva",
     'Peshat (`1Moz_4v1-24_bovitett.md`)', 'H0127', 'H0127', '1',
     '"ground (as tilled, yielding sustenance)" — magyarul: "föld (mint megművelt, terményt adó talaj)"'),
    (['1Móz 5:29'],
     "A lánc forgópontja: Lámek Noé névadásában egyetlen mondatban idézi vissza mindhárom kulcsszót — עִצְּבוֹן (*itzevón*) + אֲדָמָה (*adamá*) + אֵרְרָהּ יְהוָה (*érerá JHVH*, Pi'él) —, és vigasztalást vár alóla",
     'Remez — **új lexikai lelet, l. 2. pont**', 'H6093, H0127, H0779', 'H6093', '—',
     '"construct יָדֵינוּ עִצָּבוֹן 5:29 (both of agriculture)" — magyarul: "szerkezetes forma: ’kezünk fáradsága’ 5:29 (mindkettő a földműveléshez kötődik)"'),
    (['1Móz 6:5'],
     "רָעָה / רַע (*rá'á* / *ra*) — a diagnózis kiterjesztése: a gonoszság nem tettekben, hanem a szív minden gondolat-alkotásában",
     'Peshat/Drash (`1Moz_6v1-8_bovitett.md`)', 'H7451', 'H7451', '1',
     '"bad, evil" — magyarul: "rossz, gonosz"'),
    (['1Móz 6:7'],
     "אֲדָמָה (*adamá*) — \"eltörlöm az embert a **föld színéről**\": a következmény visszatér ahhoz a szóhoz, amellyel 3:17-ben elindult",
     'Peshat (`1Moz_6v1-8_bovitett.md`)', 'H0127', 'H0127', '4',
     '"ground as earth\'s visible surface" — magyarul: "föld mint a föld látható felszíne"'),
    (['1Móz 6:11'],
     "וַתִּשָּׁחֵת הָאָרֶץ (*vattissáchét há'árec*, Nif'ál) + וַתִּמָּלֵא הָאָרֶץ חָמָס — a föld megromlott **és** megtelt erőszakkal",
     'Peshat (`1Moz_6v9-22_bovitett.md`)', 'H7843, H2555, H4390', 'H7843', "Nif'ál",
     '"be corrupted, corrupt, in morals and rel., of earth ... Gen 6:12 ... 6:11" — magyarul: "megromlani, erkölcsi/vallási értelemben megromlott — a földről, Gen 6:11-12"'),
    (['1Móz 6:12'],
     "נִשְׁחָתָה (*nishcháta*, Nif'ál) + הִשְׁחִית כָּל־בָּשָׂר (*hishchít kol-bászár*, Hif'íl) — a romlás nem baleset: **minden test aktívan megrontotta** a maga útját",
     'Peshat/Drash (`1Moz_6v9-22_bovitett.md`)', 'H7843', 'H7843', "Nif'ál / Hif'íl",
     '"be corrupted, corrupt, in morals and rel." — magyarul: "megromlani; erkölcsi/vallási értelemben megromlott"'),
    (['1Móz 6:13'],
     "מָלְאָה הָאָרֶץ חָמָס + מַשְׁחִיתָם (*mashchítám*) — Isten **ugyanazzal az igével** felel, amellyel az ember vétkezett",
     'Peshat/Drash/Sod (`1Moz_6v9-22_bovitett.md`)', 'H2555, H7843', 'H2555', '—',
     '"violence, wrong ... compare Gen 6:11, 13 (P)" — magyarul: "erőszak, jogtalanság — vö. Gen 6:11, 13"'),
    (['1Móz 6:17'],
     "לְשַׁחֵת כָּל־בָּשָׂר (*lesachét*, Pi'él) — az özönvíz célja szó szerint ugyanaz az ige, mint a 6:12 emberi cselekvése",
     'Peshat (`1Moz_6v9-22_bovitett.md`)', 'H7843', 'H7843', "Pi'él",
     '"spoil, ruin ... destroy ... כָּל־בָּשָׂר Gen 6:17" — magyarul: "elrontani, tönkretenni... elpusztítani ’minden testet’, Gen 6:17"'),
    (['1Móz 8:21'],
     "לֹא אֹסִף לְקַלֵּל (*ló oszíf lekallél*) עוֹד אֶת־הָאֲדָמָה — **lexikai finomság**: az ígéret nem a 3:17 *arar*-t vonja vissza, hanem egy másik igét (קָלַל, *kalal*, H7043) tagad meg; az emberi szív állapotára adott indoklás (רַע) változatlan marad",
     'Remez — **új lexikai lelet, l. 2. pont**', 'H7043, H0127, H7451', 'H7043', '1',
     '"be slight, of water, be abated" (Pi\'élben "curse") — magyarul: "csekélynek lenni, vízről: apadni" (Pi\'él-ben: "megátkozni")'),
    (['1Móz 9:11', '1Móz 9:15'],
     "לְשַׁחֵת (*lesachét*, Pi'él) tagadva — a szövetség pontosan azt az igét zárja ki a jövőből, amellyel a 6:13,17 ítélet megtörtént",
     'Remez', 'H7843', 'H7843', "Pi'él",
     '"earth Gen 9:11 (P)" — magyarul: "föld, Gen 9:11"'),
    (['1Móz 9:25'],
     "אָרוּר כְּנָעַן (*árúr Kenáan*) — az átok-lánc az özönvíz **után** azonnal újraindul, immár egy leszármazottra",
     'Peshat (`1Moz_9v18-29_bovitett.md`)', 'H0779', 'H0779', 'Qal pass. ptc.',
     '"curse ... Gen 3:14, 17; 4:11; 9:25" — magyarul: "átkozott — l. Gen 3:14, 17; 4:11; 9:25"'),
    (['1Móz 12:3'],
     "וּמְקַלֶּלְךָ אָאֹר ... וְנִבְרְכוּ בְךָ כֹּל מִשְׁפְּחֹת הָאֲדָמָה (*umkalelkhá á'ór ... venivrekhú vekhá kol mispechót há'adamá*) — a lánc **megfordítása**: ugyanaz az ige (*arar*) és ugyanaz a főnév (*adamá*), de most az áldás keretében",
     'Remez/Drash (`1Moz_12v1-20_bovitett.md`)', 'H0779, H7043, H1288, H0127', 'H0779', 'Qal impf.',
     '"curse || בֵּרֵךְ bless ... 12:3" — magyarul: "megátkozni — ellentétpárja: megáldani, 12:3"'),
]

TABLA_B = [
    (['5Móz 27:15-26'],
     "Tizenkét egymást követő אָרוּר (*árúr*) — a genezisi kimondás-formula törvényi, liturgikus rendszerré szervezve",
     'Remez', 'H0779', 'H0779', 'Qal pass. ptc.',
     '"curse ... chiefly as exclamation, || בָּרוּךְ ... Deut 27:15-26" — magyarul: "átkozott — jellemzően felkiáltásként, ellentétpárja: áldott — 5Móz 27:15-26"'),
    (['5Móz 28:16-19'],
     "Négy אָרוּר (*árúr*) a szövetségszegés következményeiként, a 28:3-6 négy בָּרוּךְ (*bárúkh*) tükörképeként",
     'Remez', 'H0779', 'H0779', 'Qal pass. ptc.',
     '"curse || בֵּרֵךְ bless" — magyarul: "átkozott — ellentétpárja: áldott"'),
    (['Jer 17:5'],
     "אָרוּר הַגֶּבֶר אֲשֶׁר יִבְטַח בָּאָדָם (*árúr haggever aser jivtach bá'ádám*) — a próféta az átok-formulát egyéni bizalmi döntésre alkalmazza",
     'Drash', 'H0779', 'H0779', 'Qal pass. ptc.',
     '"curse ... chiefly as exclamation, || בָּרוּךְ ... Jer 11:3; 17:5" — magyarul: "átkozott — jellemzően felkiáltásként, ellentétpárja: áldott — Jer 11:3; 17:5"'),
    (['Zsolt 14:1', 'Zsolt 53:2'],
     "הִשְׁחִיתוּ (*hishchítú*) — **pontosan a 1Móz 6:12 Hif'íl alakja**, az emberiség egyetemes romlásának diagnózisaként",
     "Remez — **új lexikai lelet**, TSK-val is megerősítve", 'H7843', 'H7843', "Hif'íl",
     '"pervert, corrupt, morally ... עֲלִילָה הִתְעִיבוּ ׳הִשׁ Psa 14:1 = 53:2" — magyarul: "megrontani, erkölcsi értelemben megrontani — ’utálatos tettet követtek el’, Zsolt 14:1 = 53:2"'),
    (['Ez 7:23'],
     "מָלְאָה ... חָמָס (*málá ... chámász*) — a 1Móz 6:11,13 kollokáció (megtelni + erőszak) Jeruzsálemre alkalmazva",
     'Remez', 'H2555, H4390', 'H2555', '—',
     '"violence, wrong ... ח מָלְאָה ׳הָעִיר Ezek 7:23; 28:16" — magyarul: "erőszak, jogtalanság — ’megtelt a város [erőszakkal]’, Ez 7:23; 28:16"'),
    (['Ez 8:17'],
     "מָלְאוּ אֶת־הָאָרֶץ חָמָס (*málú et-há'árec chámász*) — a **legközelebbi** ószövetségi párhuzam: ugyanaz az ige+tárgy szerkezet, mint 1Móz 6:11,13-ban, Júda házára",
     'Remez — TSK-val is megerősítve', 'H2555, H4390', 'H2555', '—',
     '"violence, wrong ... compare Gen 6:11, 13 (P), Ezek 8:17" — magyarul: "erőszak, jogtalanság — vö. 1Móz 6:11, 13; Ez 8:17"'),
    (['Ez 28:16'],
     "מָלְאוּ תוֹכְךָ חָמָס (*málú tókhekhá chámász*) — a kollokáció Tírusz fejedelmére",
     'Remez', 'H2555, H4390', 'H2555', '—',
     '"violence, wrong ... ח מָלְאָה ׳הָעִיר Ezek 7:23; 28:16" — magyarul: "erőszak, jogtalanság — ’megtelt a város [erőszakkal]’, Ez 7:23; 28:16"'),
    (['Zsolt 74:20'],
     "מָלְאוּ ... נְאוֹת חָמָס (*málú ... ne'ót chámász*) — a kollokáció panasz-imában",
     'Remez', 'H2555, H4390', 'H2555', '—',
     '"violence, wrong ... ח נְאוֹת ׳מַחֲשַׁכֵּי־אֶרֶץ מָלְאוּ Psa 74:20" — magyarul: "erőszak, jogtalanság — ’a föld sötét helyei megteltek [erőszakkal]’, Zsolt 74:20"'),
    (['Mik 6:12'],
     "מָלְאוּ חָמָס (*málú chámász*) — a kollokáció Izráel gazdagjaira",
     'Remez', 'H2555, H4390', 'H2555', '—',
     '"in general of rude wickedness of men, their noisy, wild, ruthlessness ... Micah 6:12" — magyarul: "általában az emberek durva gonoszsága, zajos, vad kíméletlensége — Mik 6:12"'),
    (['Sof 1:9'],
     "הַמְמַלְאִים ... חָמָס וּמִרְמָה (*hamemal'ím ... chámász umirmá*) — a kollokáció az úr házának megtöltésére",
     'Remez', 'H2555, H4390', 'H2555', '—',
     '"in general of rude wickedness of men, their noisy, wild, ruthlessness ... Zeph 1:9" — magyarul: "általában az emberek durva gonoszsága, zajos, vad kíméletlensége — Sof 1:9"'),
    (['Hab 2:8', 'Hab 2:17'],
     "מֵחֲמַס אָדָם (*méchamasz ádám*) — az erőszak **visszatér** elkövetőjére: a gyűrűzés mint megtorlási elv, explicit kimondva",
     'Drash', 'H2555', 'H2555', '—',
     '"violence, specifically of physical violence ... Hab 2:8, 17 (twice in verse)" — magyarul: "erőszak, kifejezetten fizikai erőszak — Hab 2:8, 17 (kétszer a versben)"'),
    (['Jón 3:8'],
     "וְיָשֻׁבוּ ... מִן־הֶחָמָס אֲשֶׁר בְּכַפֵּיהֶם (*vejásúvú ... min-hechámász aser bekhappéhem*) — az **egyetlen** hely, ahol egy nép a *chámász*-ból megtérve elkerüli a már kimondott pusztulást: a gyűrűzés megszakítható",
     'Drash — **új lexikai lelet**', 'H2555', 'H2555', '—',
     '"׳ח בְּיָדַיִם Jonah 3:8" — magyarul: "erőszak a kezeikben — Jón 3:8"'),
    (['Ézs 60:18'],
     "לֹא־יִשָּׁמַע עוֹד חָמָס בְּאַרְצֵךְ (*ló-jissámá ód chámász be'arcékh*) — eszkatológiai visszavonás: a *chámász* eltűnik a földről",
     'Sod', 'H2555, H8085', 'H2555', '—',
     '"|| שֹׁד ... Isa 60:18" — magyarul: "’pusztítás’ szó párjaként — Ézs 60:18"'),
    (['Jer 6:7'],
     "חָמָס וָשֹׁד יִשָּׁמַע בָּהּ (*chámász vásód jissámá báh*) — a \"hallatszik az erőszak\" kollokáció (H8085+H2555) Jeruzsálemre",
     'Remez — TSK-val is megerősítve', 'H2555, H8085', 'H2555', '—',
     '"|| שֹׁד ... Jer 6:7" — magyarul: "’pusztítás’ szó párjaként — Jer 6:7"'),
    (['Jer 51:46'],
     "חָמָס בָּאָרֶץ (*chámász bá'árec*) — \"erőszakosság van a földön\": a *chámász* + *erec* párosítás, Babilon összeomlásának előjeleként",
     'Remez', 'H2555, H8085', 'H2555', '—',
     '"׳ח בארץ Jer 51:46, compare Gen 6:11, 13 (P)" — magyarul: "erőszak a földön — Jer 51:46, vö. 1Móz 6:11, 13"'),
    (['Hab 1:2'],
     "אֶזְעַק אֵלֶיךָ חָמָס וְלֹא תוֹשִׁיעַ (*ez'ak élekhá chámász veló tósía*) — a **megfordított** irány: a *chámász* miatt kiáltó próféta panasza arról, hogy Isten nem hallja",
     'Drash — TSK-val is megerősítve', 'H2555, H8085', 'H2555', '—',
     '"in general of rude wickedness of men, their noisy, wild, ruthlessness ... Hab 1:2" — magyarul: "általában az emberek durva gonoszsága, zajos, vad kíméletlensége — Hab 1:2"'),
    (['Ézs 24:5-6'],
     "\"A föld megfertőztetett lakosai alatt... ezért **átok** emészti meg a földet\" — a föld/átok/lakosok hármas szerkezete azonos a 1Móz 3:17-tel, **de más szóval**: אָלָה (*álá*, H0423), nem *arar* ⇒ **tematikus, nem lexikai**",
     'Drash — TSK-eredetű', 'H0423, H2610', 'H0423', '3',
     '"curse (a) from God ... Isa 24:6" — magyarul: "átok (a) Istentől — Ézs 24:6"'),
    (['Hós 4:1-3'],
     "\"Nincs igazság... azért gyászol a föld\" — a lakosok bűne és a föld sorvadása közti okozati kapcsolat; *chámász* nélkül ⇒ **tematikus, nem lexikai**",
     'Drash — TSK-eredetű', '', '', '', ''),
]

TABLA_C = [
    (['Róm 8:20-22'],
     "ἡ κτίσις ... τῇ ματαιότητι ὑπετάγη (*hé ktiszisz ... té mataiotéti hüpetagé*), majd ἡ δουλεία τῆς φθορᾶς (*hé dúleia tész fthorász*) — a teremtett világ továbbra is a 1Móz 3:17 átok alatt áll, és a φθορά ugyanabból a φθείρω-szócsaládból való, amellyel a LXX a 1Móz 6:11-13 *sáchat*-ját fordítja",
     'Drash/Sod', 'G3153, G5356, G2937'),
    (['Gal 3:10'],
     "ἐπικατάρατος πᾶς ὃς οὐκ ἐμμένει (*epikatáratosz pász hosz úk emmenei*) — az 5Móz 27:26 idézete; a LXX ott **ugyanazt** a szót használja, amelyet a 1Móz 3:17-ben",
     'Drash', 'G1944, G2671'),
    (['Gal 3:13'],
     "γενόμενος ὑπὲρ ἡμῶν κατάρα (*genomenosz hüper hémón katara*) — Krisztus **átokká lesz**; Pál itt az 5Móz 21:23-at idézi, de nem a LXX κεκατηραμένος (*kekatéraménosz*, G2672) szavával, hanem ἐπικατάρατος-szal — vagyis a két idézetet (27:26 és 21:23) **ugyanarra a szóra hangolja**, amely a 1Móz 3:17 átok-szava is",
     'Drash/Sod — **új lexikai lelet**', 'G1944, G2671'),
    (['Zsid 6:7-8'],
     "γῆ ... ἐκφέρουσα ἀκάνθας καὶ τριβόλους ... κατάρας ἐγγύς (*gé ... ekferúsza akanthász kai tribolúsz ... katarász engüsz*) — **háromszavas lexikai egyezés** a LXX 1Móz 3:17-18-cal: γῆ + ἄκανθα + τρίβολος, a κατάρα-szócsaláddal",
     'Remez/Drash — **új lexikai lelet**', 'G1093, G0173, G5146, G2671'),
    (['Jel 11:18'],
     "διαφθεῖραι τοὺς διαφθείροντας τὴν γῆν (*diaftheirai túsz diaftheirontász tén gén*) — \"elpusztítani azokat, akik a földet pusztítják\": a 1Móz 6:12-13 szerkezete (ember megrontja → Isten megrontja) görögül, ugyanazzal az igével mindkét oldalon",
     'Sod — **új lexikai lelet**', 'G1311, G1093'),
    (['Jel 19:2'],
     "ἥτις ἔφθειρεν τὴν γῆν ἐν τῇ πορνείᾳ αὐτῆς (*hétisz eftheiren tén gén en té porneia autész*) — \"a mely a földet megrontotta az ő paráznaságával\": **ugyanaz az ige+tárgy szerkezet, mint a LXX 1Móz 6:11-ben** (ἐφθάρη … ἡ γῆ)",
     'Remez/Sod — **új lexikai lelet**', 'G5351, G1093'),
    (['Mt 15:19', 'Mk 7:21-23'],
     '"a szívből származnak a gonosz gondolatok" — a 1Móz 6:5 szív-diagnózisának újszövetségi megismétlése ⇒ **tematikus, nem lexikai**',
     'Drash — TSK-eredetű', ''),
    (['2Pét 3:6-7'],
     "az özönvíz-világ elpusztulása és a jelenlegi világ tűzre tartatása — a 1Móz 6:13 ítélet-logikájának eszkatológiai kiterjesztése ⇒ **tematikus, nem lexikai**",
     'Drash — TSK-eredetű', ''),
]

UJSZOVETSEGI_TOKENEK = {
    '1Kor', '1Pét', '1Thessz', '2Pét', '2Tim', 'ApCsel', 'Jel', 'Júd',
    'Luk', 'Mt', 'Róm', 'Zsid', 'Gal', 'Mk',
}


def konyv_token(igehely):
    m = re.match(r'^(\d*[^\d\s]+)', igehely)
    return m.group(1) if m else igehely


def oszovetsegi(igehely):
    return konyv_token(igehely) not in UJSZOVETSEGI_TOKENEK


# ---------------------------------------------------------------------------
# A/B/C tábla -> elofordulasok-sorok (G2-G4 alkalmazása + igazolás)
# ---------------------------------------------------------------------------

def epit_sorok(tahot_ellenoriz_fn):
    sorok = []
    jelentes_szam_kihagyva = []

    for igehelyek, kapcsolodas, pardes_cella, strong_oszlop, bdb_entry_id, sense, jelentes_cella in TABLA_A:
        szint, felmerult = split_pardes(pardes_cella)
        jel_en, jel_hu = split_jelentes(jelentes_cella)
        for igehely in igehelyek:
            gerinc_elem, strong = gerinc_es_strong_ab(igehely, strong_oszlop, bdb_entry_id)
            sense_ok = sense_ervenyes(sense)
            if not sense_ok:
                jelentes_szam_kihagyva.append((igehely, sense))
            sor = {
                'id': 'HAMART-001', 'igehely': igehely, 'kapcsolodas': strip_kapcsolodas_markdown(kapcsolodas),
                'pardes_szint': szint, 'funkcio': '', 'gerinc_elem': gerinc_elem,
                'strong': strong, 'lexikon_szotar': 'BDB' if bdb_entry_id else '',
                'lexikon_entry_id': bdb_entry_id.replace(' / ', '+') if bdb_entry_id else '',
                'jelentes_szam': sense.strip() if sense_ok and sense.strip() != '—' else '',
                'jelentes_en': jel_en, 'jelentes_hu': jel_hu,
                'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': '',
                'proveniencia': PROV,
                'igazolas': tahot_ellenoriz_fn(igehely, strong) if oszovetsegi(igehely) else 'TAHOT-hatokoron-kivul',
                'fo_elofordulas': fo_elofordulas(igehely),
                'felmerult_tanulmany': felmerult,
            }
            sorok.append(sor)

    for igehelyek, kapcsolodas, pardes_cella, strong_oszlop, bdb_entry_id, sense, jelentes_cella in TABLA_B:
        szint, felmerult = split_pardes(pardes_cella)
        jel_en, jel_hu = split_jelentes(jelentes_cella) if jelentes_cella else ('', '')
        for igehely in igehelyek:
            tematikus = igehely in TEMATIKUS_HORGONY
            gerinc_elem, strong = gerinc_es_strong_ab(igehely, strong_oszlop, bdb_entry_id) if strong_oszlop else (
                'tematikus:%s' % TEMATIKUS_HORGONY[igehely], '')
            sense_ok = sense_ervenyes(sense)
            if sense and not sense_ok:
                jelentes_szam_kihagyva.append((igehely, sense))
            if tematikus:
                igazolas = 'nincs'
            elif oszovetsegi(igehely):
                igazolas = tahot_ellenoriz_fn(igehely, strong)
            else:
                igazolas = 'TAHOT-hatokoron-kivul'
            sor = {
                'id': 'HAMART-001', 'igehely': igehely, 'kapcsolodas': strip_kapcsolodas_markdown(kapcsolodas),
                'pardes_szint': szint, 'funkcio': '', 'gerinc_elem': gerinc_elem,
                'strong': strong, 'lexikon_szotar': 'BDB' if bdb_entry_id else '',
                'lexikon_entry_id': bdb_entry_id.replace(' / ', '+') if bdb_entry_id else '',
                'jelentes_szam': sense.strip() if sense and sense_ok and sense.strip() != '—' else '',
                'jelentes_en': jel_en, 'jelentes_hu': jel_hu,
                'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': '',
                'proveniencia': PROV,
                'igazolas': igazolas,
                'fo_elofordulas': '',
                'felmerult_tanulmany': felmerult,
            }
            sorok.append(sor)

    for igehelyek, kapcsolodas, pardes_cella, strong_oszlop in TABLA_C:
        szint, felmerult = split_pardes(pardes_cella)
        for igehely in igehelyek:
            tematikus = igehely in TEMATIKUS_HORGONY
            if tematikus:
                gerinc_elem, strong, igazolas = 'tematikus:%s' % TEMATIKUS_HORGONY[igehely], '', 'nincs'
            else:
                gerinc_elem, strong = gerinc_es_strong_c(igehely, strong_oszlop)
                igazolas = 'TAHOT-hatokoron-kivul'
            sor = {
                'id': 'HAMART-001', 'igehely': igehely, 'kapcsolodas': strip_kapcsolodas_markdown(kapcsolodas),
                'pardes_szint': szint, 'funkcio': '', 'gerinc_elem': gerinc_elem,
                'strong': strong, 'lexikon_szotar': '', 'lexikon_entry_id': '',
                'jelentes_szam': '', 'jelentes_en': '', 'jelentes_hu': '',
                'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': '',
                'proveniencia': PROV,
                'igazolas': igazolas,
                'fo_elofordulas': '',
                'felmerult_tanulmany': felmerult,
            }
            sorok.append(sor)

    # N14.1a -- a study szövege alapján explicit felülírás a két hibás sorra
    # (D13: a szkriptben javítva, nem a munkalapon kézzel).
    for sor in sorok:
        felulir = JELENTES_FELULIRAS.get(sor['igehely'])
        if felulir:
            sor.update(felulir)
            if 'jelentes_szam' in felulir:
                jelentes_szam_kihagyva = [
                    (ig, s) for ig, s in jelentes_szam_kihagyva if ig != sor['igehely']]

    # N14.1a 4. pont -- általános őr: "magyarul" szó a jelentes_en-ben, vagy
    # csak az egyik jelentes-mező üres -- mindkettő a split_jelentes()
    # elcsúszásának jele (1Móz 3:18/8:21 esete), nem hallgatható el.
    for sor in sorok:
        en, hu = sor['jelentes_en'], sor['jelentes_hu']
        if 'magyarul' in en.lower():
            raise SystemExit(
                'HIBA: %s jelentes_en mezője a "magyarul" szót tartalmazza -- '
                'a split_jelentes() valószínűleg elcsúszott: %r' % (sor['igehely'], en))
        if bool(en) != bool(hu):
            raise SystemExit(
                'HIBA: %s -- csak az egyik jelentés-mező üres (en=%r, hu=%r)'
                % (sor['igehely'], en, hu))

    return sorok, jelentes_szam_kihagyva


# ---------------------------------------------------------------------------
# TAHOT-igazolás -- a lekerdez.py betöltőjét/parse_range-ét HÍVJA (import),
# saját scan-logikát NEM definiál (K5).
# ---------------------------------------------------------------------------

def tahot_ellenoriz(igehely, strong):
    if not strong:
        return 'nincs'
    rng = L.parse_range(igehely)
    tahot = L.load_tahot()
    hits = [r for r in tahot if r['Strong-szám'] == strong]
    igehelyek_talalt = {r['Igehely'] for r in hits}
    talalt = any(L.in_range(rng, *L.parse_igehely(ig)) for ig in igehelyek_talalt)
    return 'TAHOT-igazolt' if talalt else 'nincs'


# ---------------------------------------------------------------------------
# G5 -- motivumok.tsv sora
# ---------------------------------------------------------------------------

MOTIVUMOK_FEJLEC = [
    'id', 'cim', 'ui_cimke', 'tema', 'pardes_szint', 'statusz',
    'statusz_verzio', 'statusz_datum', 'azonossag_tipusa', 'negativ_kriterium',
    'folerendelt_fogalom', 'sablon_verzio', 'forras_study',
]

MOTIVUM_SOR = {
    'id': 'HAMART-001',
    'cim': 'A bűn következményeinek gyűrűzése — átok, föld és romlás',
    'ui_cimke': 'Bűn gyűrűzése',
    'tema': 'Hamartológia',
    'pardes_szint': 'Remez/Drash',
    'statusz': 'publikálható',
    'statusz_verzio': 'v1',
    'statusz_datum': '2026.09.11',
    'azonossag_tipusa': 'strukturális',
    'negativ_kriterium': (
        'az igehelynek a gerinc valamelyik elemén (arar, adamá, itzávón, chattát, '
        'chámász, sáchat; ἐπικατάρατος, κατάρα, φθείρω-család) vagy megnevezett '
        'kollokációján (málé+chámász, sámá+chámász) át kell a genezisi átok→föld→romlás '
        'láncra visszautalnia; a bűn, a büntetés vagy az átok puszta említése e lexémák '
        'nélkül csak explicit „tematikus, nem lexikai” jelöléssel kerülhet be'
    ),
    'folerendelt_fogalom': 'a bűn / hamartológia általában',
    'sablon_verzio': 'v14',
    'forras_study': 'tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md',
}

# ---------------------------------------------------------------------------
# G6 -- jeloltek.tsv sorai: minden elofordulasok-sorhoz egy "beépítve" sor
# ---------------------------------------------------------------------------

JELOLTEK_FEJLEC = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas',
                    'karoli_szo', 'azonositas_modja', 'megbizhatosag', 'datum']

FORRAS_KERESES = 'négyforrásos audit a napló §7 szerint, retroaktív N14 betöltés'


def jeloltek_sorok(elof_sorok):
    ki = []
    for sor in elof_sorok:
        ki.append({
            'id': sor['id'], 'igehely': sor['igehely'],
            'forras_kereses': FORRAS_KERESES, 'dontes': 'beépítve',
            'indoklas': sor['kapcsolodas'],
            'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': '',
            'datum': '2026.09.11',
        })
    return ki


# ---------------------------------------------------------------------------
# Írás + jelentés
# ---------------------------------------------------------------------------

def sor_tsv(mezok_sorrend, sor):
    return '\t'.join((sor.get(m) or '') for m in mezok_sorrend)


def ir_tsv(path, fejlec_komment, mezok_sorrend, sorok):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec_komment + '\n')
        f.write('\t'.join(mezok_sorrend) + '\n')
        for sor in sorok:
            f.write(sor_tsv(mezok_sorrend, sor) + '\n')


def jelentes(elof_sorok, motivum_sor, jel_sorok, jelentes_szam_kihagyva, kivul_gerincen):
    ki = []
    ki.append('# N14.1 -- HAMART-001 munkalap-jelentés (próba, nem ír az adat/-ba)')
    ki.append('')
    ki.append('## §5 -- mért számok')
    ki.append('')
    ki.append('- study-táblasor -> elofordulasok-sor: %d (a study 46 sorából G3 szerint bontva)' % len(elof_sorok))

    gerinc_eloszlas = {}
    for s in elof_sorok:
        gerinc_eloszlas[s['gerinc_elem']] = gerinc_eloszlas.get(s['gerinc_elem'], 0) + 1
    ki.append('- gerinc_elem eloszlás:')
    for g, n in sorted(gerinc_eloszlas.items(), key=lambda kv: (-kv[1], kv[0])):
        ki.append('  - `%s`: %d' % (g, n))
    ki.append('- legnagyobb elem: %d sor' % max(gerinc_eloszlas.values()))

    fo_csoportok = {}
    for s in elof_sorok:
        if s['fo_elofordulas']:
            fo_csoportok.setdefault(s['fo_elofordulas'], 0)
            fo_csoportok[s['fo_elofordulas']] += 1
    ki.append('- fo_elofordulas: %d sor, %d csoport (%s)' % (
        sum(fo_csoportok.values()), len(fo_csoportok),
        ' · '.join('%s: %d' % (k, v) for k, v in
                   sorted(fo_csoportok.items(), key=lambda kv: FO_ELOFORDULAS_CSOPORTOK.index(kv[0])))))

    igazolas_eloszlas = {}
    for s in elof_sorok:
        igazolas_eloszlas[s['igazolas']] = igazolas_eloszlas.get(s['igazolas'], 0) + 1
    ki.append('- igazolás eloszlás: %s' % ', '.join(
        '%s=%d' % (k, v) for k, v in sorted(igazolas_eloszlas.items())))

    ki.append('')
    ki.append('## Gerincen kívüli horgony (G2, három sor a study szándéka szerint)')
    for igehely, gerinc_elem in kivul_gerincen:
        ki.append('- %s -- `%s`' % (igehely, gerinc_elem))

    ki.append('')
    ki.append('## `jelentes_szam` kihagyások')
    if jelentes_szam_kihagyva:
        for igehely, sense in jelentes_szam_kihagyva:
            ki.append('- %s -- Sense-cella: %r (nem illik az egyértékű SEMA 2.2.2 keszletbe)' % (igehely, sense))
    else:
        ki.append('(nincs kihagyás)')

    ki.append('')
    ki.append('## TAHOT-eltérések (K3)')
    elteresek = [s for s in elof_sorok if oszovetsegi(s['igehely'])
                 and s['gerinc_elem'] and not s['gerinc_elem'].startswith('tematikus:')
                 and s['igazolas'] == 'nincs']
    if elteresek:
        for s in elteresek:
            ki.append('- %s (`%s`) -- a scan nem erősítette meg' % (s['igehely'], s['strong']))
    else:
        ki.append('0 eltérés -- minden ÓSZ lexikai sort a TAHOT megerősített.')

    ki.append('')
    ki.append('## `motivumok.tsv` sora')
    ki.append('```')
    for k in MOTIVUMOK_FEJLEC:
        ki.append('%s: %s' % (k, motivum_sor.get(k, '')))
    ki.append('```')

    ki.append('')
    ki.append('## Összegzés')
    ki.append('elofordulasok munkalap-sor: %d' % len(elof_sorok))
    ki.append('jeloltek munkalap-sor: %d (mind `beépítve`)' % len(jel_sorok))

    return '\n'.join(ki) + '\n'


def eles_ir(adat_dir, path_nev, mezok_sorrend, sorok):
    """A sorok vegehez fuzese az eles TSV-hez, a fajl mai sorveget megtartva
    (betolt.py elofordulasok_ir() mintaja) -- CSAK motivumok.tsv/jeloltek.tsv-hez,
    az elofordulasok.tsv-t ez a szkript soha nem irja (azt a betolt.py beepit
    vegzi, F8 atjaro)."""
    path = os.path.join(adat_dir, path_nev)
    sorszovegek = [sor_tsv(mezok_sorrend, sor) for sor in sorok]
    if not sorszovegek:
        return
    dominans, _, _ = G.sorveg_elemez(path)
    with open(path, 'rb') as f:
        nyers = f.read()
    vegzodik_sorveggel = nyers.endswith(b'\n')
    dominans_b = dominans.encode('utf-8')
    with open(path, 'ab') as f:
        if not vegzodik_sorveggel:
            f.write(dominans_b)
        f.write(dominans_b.join(s.encode('utf-8') for s in sorszovegek))
        f.write(dominans_b)


def main():
    parser = argparse.ArgumentParser(description='N14.1 -- HAMART-001 munkalapok')
    parser.add_argument('--naplok', default=os.path.join(ROOT, 'naplok'),
                         help='hova írja a három munkalapot + a jelentést')
    parser.add_argument('--ir', action='store_true',
                         help='N14.2: a motivumok.tsv és a jeloltek.tsv sorait '
                              'az éles adat/ végéhez fűzi (az elofordulasok.tsv-t NEM)')
    parser.add_argument('--adat', default=ALAPERTELMEZETT_ADAT,
                         help='az adat/ könyvtár (--ir esetén ide ír)')
    args = parser.parse_args()

    elof_sorok, jelentes_szam_kihagyva = epit_sorok(tahot_ellenoriz)
    jel_sorok = jeloltek_sorok(elof_sorok)

    kivul_gerincen = [(s['igehely'], s['gerinc_elem']) for s in elof_sorok
                       if s['gerinc_elem'] in ('H6975+H1863', 'H7451', 'H7043')]

    # Hossz-ellenőrzés minden sorra, MIELŐTT bármit is írnánk.
    for s in elof_sorok:
        hianyzo = [m for m in ('id', 'igehely', 'kapcsolodas', 'gerinc_elem',
                                'proveniencia', 'igazolas') if not s.get(m)]
        if hianyzo:
            raise SystemExit('HIBA: elofordulasok sor hiányos mezőkkel (%s): %r'
                              % (', '.join(hianyzo), s))
    if len(elof_sorok) != 52:
        raise SystemExit('HIBA: %d elofordulasok-sor a várt 52 helyett' % len(elof_sorok))
    if len(jel_sorok) != len(elof_sorok):
        raise SystemExit('HIBA: jeloltek-sorok száma (%d) != elofordulasok-sorok száma (%d)'
                          % (len(jel_sorok), len(elof_sorok)))

    os.makedirs(args.naplok, exist_ok=True)

    ir_tsv(os.path.join(args.naplok, 'N14_hamart_elofordulasok_munkalap.tsv'),
           '# N14.1 munkalap -- betolt.py beepit formátumában. Sema: adat/SEMA.md 2.2',
           ELOFORDULASOK_FEJLEC, elof_sorok)
    ir_tsv(os.path.join(args.naplok, 'N14_hamart_jeloltek_munkalap.tsv'),
           '# N14.1 munkalap -- adat/jeloltek.tsv alakjában. Sema: adat/SEMA.md 2.4',
           JELOLTEK_FEJLEC, jel_sorok)
    ir_tsv(os.path.join(args.naplok, 'N14_hamart_motivum_munkalap.tsv'),
           '# N14.1 munkalap -- adat/motivumok.tsv alakjában. Sema: adat/SEMA.md 2.1',
           MOTIVUMOK_FEJLEC, [MOTIVUM_SOR])

    jelentes_szoveg = jelentes(elof_sorok, MOTIVUM_SOR, jel_sorok, jelentes_szam_kihagyva, kivul_gerincen)
    jelentes_path = os.path.join(args.naplok, 'N14_hamart_jelentes.md')
    with io.open(jelentes_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(jelentes_szoveg)

    print(jelentes_szoveg)
    print('megírva: %s' % args.naplok, file=sys.stderr)

    if args.ir:
        eles_ir(args.adat, 'motivumok.tsv', MOTIVUMOK_FEJLEC, [MOTIVUM_SOR])
        eles_ir(args.adat, 'jeloltek.tsv', JELOLTEK_FEJLEC, jel_sorok)
        print('  --ir: 1 motivumok.tsv sor + %d jeloltek.tsv sor íródott az élesbe (%s).'
              % (len(jel_sorok), args.adat), file=sys.stderr)


if __name__ == '__main__':
    main()
