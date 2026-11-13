"""lapgen.konfig — a generátor küszöbei, szűrő-halmazai és kiadási azonosítói egy helyen.

Ide nevesített konstans kerül, teszttel (`tesztek/teszt_konfig.py`). Látható mondat nem áll itt:
az a sablontáblában van; a mondatban álló szám innen jön, formázott sablonparaméterként.
"""

# A generált blokkok jelölőjében álló célnév. A termék célneve `lexikon`; az új generátor a 218a
# alatt `--cel lexikon2` néven hívható, de a lapon a végleges célnevet írja (a jelölőket más eszközök
# is olvassák, és a regresszió bájtra mér).
CEL_NEV = 'lexikon'
GENERATOR_JELOLO = 'general.py --cel ' + CEL_NEV

# A nézetek fájlnév-utótagjai.
NEZET_TUDOMANYOS = 'TUDOMANYOS'
NEZET_KIZARASOK = 'KIZARASOK'

# Az olvasási napló fájlja a lap mellett (`<ID>_olvasasi_naplo.tsv`): a regresszió bemenet-hash őre olvassa.
NAPLO_FAJLNEV = '%s_olvasasi_naplo.tsv'
NAPLO_OSZLOPOK = ('b_id', 'utvonal', 'sha256')

# A dátum környezeti változója (YYYY-MM-DD); nélküle a `ts=` a bemenetek hash-éből képződik (GK-29).
DATUM_VALTOZO = 'PARDES_DATUM'
TS_HASH_JEGY = 12

# --- 2. Előfordulások: az összegző mondat küszöbei --------------------------------------------------------------
SULYPONT_KUSZOB = 0.40      # egy könyvben a helyek legalább ekkora hányada: a motívum súlypontja
SZOVETSEG_KUSZOB = 0.20     # ennél kisebb arányú szövetség: „főként ószövetségi / újszövetségi”
BIZONYTALAN_KUSZOB = 0.67   # a magas megbízhatóságú helyek aránya ez alatt: „sok a bizonytalan azonosítás”

KOZOS_PROVENIENCIA_KUSZOB = 2   # ennyi jegyzetben álló proveniencia-hármas kap közös jelet (‹E1› …)

# --- Döntési út és a kizárások melléklete ----------------------------------------------------------------------
CSOPORT_PELDA_DB = 5            # a csoportos ok alatt ennyi példavers áll a Károli-szöveggel
KIZARASOK_NYITVA_HATAR = 10     # a melléklet verslistája ennyi versig nyitva áll, fölötte lenyíló

# az ismétlés kapui (lapgen.ismetles): a szavak száma az ablakban
KRITERIUM_ABLAK = 12            # a kritérium ekkora szósora a látható lapon legfeljebb egyszer állhat (BUKÁS)
ISMETLES_ABLAK = 16             # ekkora azonos szósor kétszer: figyelmeztetés (15 szónál hosszabb ismétlés)
ISMETLES_IDEZET_LEGFELJEBB = 4  # az ablakban legfeljebb ennyi idézett szó állhat (a bibliai idézet nem ismétlés)
ISMETLES_SZAMOS_LEGFELJEBB = 8  # az ablakban legfeljebb ennyi számjegyes szó állhat (az igehely-felsorolás nem próza)

# --- Döntések, amelyeknek a dátuma a lapon áll (a szám nem) -----------------------------------------------------
DONTES_JELENTES_FUNKCIO = 'DT272'   # a „Jelentés (a szó)” és a „Funkció (a motívumban)” oszlop szétválasztása
DONTES_UBS_SZONEZET = 'DT393'       # az UBS-jelentés cellája: rövid glossza, a teljes szócikk a szónézetben

# --- UBS-jelentés: a fordítástábla kulcsai ---------------------------------------------------------------------
SZOTAR_UBS_DNTG = 'UBS_DNTG'
SZOTAR_UBS_DBH = 'UBS_DBH'
UBS_GLOSSZA_MEZO = 'glosszak_hu'
NINCS_JELENTESSZAM = '—'            # a fordítástábla kulcsában a jelentésszám nélküli szócikk jele

# --- A futás módja ------------------------------------------------------------------------------------------------
MOD_MUNKA, MOD_KIADAS = 'munka', 'kiadas'

# --- 4. Szótári háttér: a szótári pontok sorszáma (a szótári pontok táblájának `sorrend` értéke) -------------------
PONT_ALAPJELENTES = 1
PONT_MELYSEGI = 2
PONT_TEOLOGIAI = 3
PONT_DOMEN = 4
PONT_TOMOR = 5
PONT_LXX_HID = 6
PONT_MASIK_NYELV = 7
PONT_NYELVI_HATTER = 8
PONT_VERSENKENT = 9
PONT_KIEJTES = 10
PONT_VISSZHANG = 11     # nincs a táblában: egysoros mutató a Hatástörténet szakaszára (a számozás nem mozdul)
PONT_TEMATIKUS = 12
PONT_KAROLI = 13
PONT_PARHUZAM = 14

FO_SZOTAR_HEBER, FO_SZOTAR_GOROG = 'BDB', 'Thayer'   # a fő szótár nyelvenként (a névtábla `szotar` kulcsa)

# A Septuaginta-megfelelő: a versszintű társulás (Dice-mérték) küszöbe és a társlista hossza
LXX_TARS_KUSZOB = 0.05
LXX_PAROK_TOP = 10

# A fordítástábla kulcsai a szótári pontokhoz
SZOTAR_ROVID = 'rovid_szotar'          # a rövid jelentés (héber glosszatábla, illetve a görög rövid szótár)
MEZO_ROVID_JELENTES = 'rovid_jelentes'
SZOTAR_TW = 'tW_szocikkek'
TW_CIM_KULCS = 'cim'
SZOTAR_SDBH, SZOTAR_SDGNT = 'SDBH', 'SDGNT'
DOMEN_KULCS = 'domen'

# A lapon megnevezett forrás licence a licencleltár kulcsa szerint (a licenc szövege a leltárból jön)
LICENC_ROVID_SZOTAR = {'gorog': 'TBESG', 'heber': 'TBESH'}
LICENC_TW = 'tW_szocikkek'

# Az arány fokozatai a következtetés mondatához: (alsó határ, fokozat), csökkenő rendben
FOKOK = ((0.90, 'szinte'), (0.67, 'tobbseg'), (0.50, 'fele'), (0.0, 'keves'))
VERSENKENTI_KIS = 2     # ha minden szó legfeljebb ennyi helyen áll, a versenkénti pont nem von le következtetést

# 4.12 (tematikus index): a régi `szerep_nave.py` küszöbei
NAVE_MIN_VERS = 2              # a téma legalább ennyi motívumverset érint
NAVE_MIN_SZAZALEK = 1          # a motívumversek aránya a téma összes verséhez legalább ennyi százalék
NAVE_MIN_ARANY = NAVE_MIN_SZAZALEK / 100

# 4.13–4.14 (a Károli-fordítás magyar szavai): a régi `szerep_karoli.py` és `lexikon_general.py` küszöbei
KAROLI_MIN_HELY = 3            # ennyi helytől von le következtetést a 4.13 egy szóról
KAROLI_ALLANDO = 0.67          # a leggyakoribb magyar szó aránya ettől: a szó magyarul is követhető
KAROLI_KULCS_MIN_SOR = 3       # kulcsszava a legalább ennyi helyen álló szónak lehet
KAROLI_KULCS_ARANY = 0.5       # a kulcsszó a szó helyeinek legalább ekkora hányadában áll
KAROLI_ELOTAG_MARADEK = 3      # a kulcsszóval kezdődő szóalak egyezik, ha utána legfeljebb ennyi betű áll
KAROLI_OLVADAS_MIN = 3         # a ritkább szótári alak a legalább ennyi betűs gyakoribb alakba olvad
KAROLI_CSALAD_MIN = 5          # a ragozott maradék a legalább ennyi betűs szótári alakba olvad (szócsalád)
KAROLI_REJTETT_PELDA = 3       # a bevezető ennyi rejtett párhuzamot nevez meg példaként
KAROLI_HAMIS_NYITVA = 10       # a hamis párhuzam listája ennyi versig nyitva áll, fölötte lenyíló

# 4.7 (Megfelelők a másik nyelven): a híd mondatában ennyi igehely áll; a görög szócsalád előtagjai és a tő hossza
HID_HELYEK = 4
GOROG_ELOTAGOK = ('επι', 'κατα', 'κατ', 'δια', 'δι', 'συν', 'εκ', 'απο', 'προ')
GOROG_TO_HOSSZ = 3
GOROG_ELOTAG_MARADEK = 2    # az előtag csak akkor válik le, ha utána ennél több betű marad

# A görög szó betűnkénti latin átírása (a forrásban kiírt, a szótári alaktól eltérő alak kiejtéséhez)
GOROG_BETU_ATIRAS = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'ē', 'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l',
    'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'y', 'φ': 'ph',
    'χ': 'ch', 'ψ': 'ps', 'ω': 'ō',
}
GOROG_KETTOSHANGZO_ELOTAG = 'αεηο'   # ezek után az υ kettőshangzó része: „u”
