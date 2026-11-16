"""lapgen.ertekek — az adattáblák zárt értékkészletei felsorolásként.

A bemeneti réteg a nyers mezőt ezekre alakítja (ismeretlen érték kemény hiba); a számítás ezeken ágazik el;
a megjelenítő a névtáblából veszi az olvasói nevüket (a névtábla típusa az osztály `NEV_TIPUS` mezője).
"""
import enum


class Megbizhatosag(enum.Enum):
    MAGAS = 'magas'
    KOZEPES = 'közepes'
    ALACSONY = 'alacsony'


class Igazolas(enum.Enum):
    TAHOT_IGAZOLT = 'TAHOT-igazolt'
    TAGNT_IGAZOLT = 'TAGNT-igazolt'
    HATOKORON_KIVUL = 'TAHOT-hatokoron-kivul'
    NINCS = 'nincs'


class UbsForras(enum.Enum):
    """Melyik UBS-szótárból jön a cella: a görögből (újszövetségi sor) vagy a héberből (ószövetségi sor)."""
    DNTG = 'dntg'
    DBH = 'dbh'
    NEM_ALKALMAZHATO = 'nem_alkalmazhato'   # tematikus hely a lánc szava nélkül


class DbhOk(enum.Enum):
    """Miért nincs héber UBS-hivatkozás egy versre."""
    NINCS_MEGFELELTETES = 'nincs_megfeleltetes'   # a Károli-vers nincs a versmegfeleltető táblában
    NEM_EGY_VERS = 'nem_egy_vers'                 # a masszoréta megfelelő nem egyetlen vers
    SZAMOZAS_ELTERES = 'szamozas_elteres'         # versszámozás-eltérés, a masszoréta vers nincs megadva
    NINCS_HIVATKOZAS = 'nincs_hivatkozas'         # a szótár a (masszoréta) versre nem hivatkozik


class JelentesFajta(enum.Enum):
    """Miből áll a „Jelentés (a szó)” cella egy szóra."""
    CIMKE = 'cimke'                               # jóváhagyott címke és a szakasz jele
    GLOSSZA = 'glossza'                           # címke híján a szakasz olvasói glosszája és a jel
    SZOCIKK_EGESZE = 'szocikk_egesze'             # tagolatlan szócikk: a szócikk egésze, a fej glosszájával
    NINCS_CIMKE = 'nincs_cimke'                   # van szakasz, de nincs címke és glossza
    NINCS_HOZZARENDELES = 'nincs_hozzarendeles'   # nincs szakasz


class IndokFajta(enum.Enum):
    """Miért ez a címke áll a soron: a jegyzet mondatának és a belső leírásnak a fajtája."""
    BDB_PELDA = 'bdb_pelda'                       # a BDB a szakaszban maga idézi a helyet
    MASUTT_IS = 'masutt_is'                       # a BDB a helyet más szakaszban is idézi; a hozzárendelés dönt
    KUTATOI = 'kutatoi'                           # szerkesztői hozzárendelés a szótár tagolása szerint
    KUTATOI_TAGABB = 'kutatoi_tagabb'             # szerkesztői hozzárendelés; a szótár a tágabb szakaszban idézi
    TAGOLATLAN = 'tagolatlan'                     # a szótár nem tagolja a szócikket számozott jelentésekre
    NINCS_LEKEPEZVE = 'nincs_lekepezve'           # a szerkesztői jelentésszám nincs leképezve a szótárra
    TOBB_TOKEN = 'tobb_token'                     # a szótár idézi a verset, de a szó többször áll benne
    TARTOMANYBAN = 'tartomanyban'                 # a szótár a verset csak verstartomány belsejében idézi
    NEM_AZONOSITHATO = 'nem_azonosithato'         # nem azonosítható, melyik szócikk idézi a helyet
    FORRAS_JAVITAS = 'forras_javitas'             # a szótár szövegében sajtóhiba áll, kézi javítással
    MINOSITO = 'minosito'                         # a jelentésszám minősítője nem a szó jelentése
    THAYER_PELDA = 'thayer_pelda'                 # a Thayer saját példahelye
    THAYER_NEM_IDEZI = 'thayer_nem_idezi'         # a Thayer a helyet nem idézi
    NINCS_HOZZARENDELES = 'nincs_hozzarendeles'   # nincs hozzárendelés és szótári példahely


class JegyzetFajta(enum.Enum):
    SZOKASOS = 'szokasos'                         # igazolás és jelentés
    TEMATIKUS = 'tematikus'                       # tematikus hely a lánc szava nélkül
    TEMATIKUS_SAJAT = 'tematikus_sajat'           # tematikus hely: a vers saját szava nem a lánc szava


class SzovetsegKod(enum.Enum):
    """Az előfordulások megoszlása a két szövetség között (az összegző mondat következtetés-kódja)."""
    FOKENT_OSZ = 'fokent_osz'
    FOKENT_USZ = 'fokent_usz'
    MINDKETTO = 'mindketto'
    CSAK_OSZ = 'csak_osz'
    CSAK_USZ = 'csak_usz'


class MaradtFajta(enum.Enum):
    """Min lóg a motívum egy helycsoportja a Döntési úton (a hordozó elem fajtája)."""
    SZO = 'szo'                       # a lánc szava vagy szavai (Strong-számok)
    NEVES_SZOPAR = 'neves_szopar'     # kézzel elnevezett szópár (a részei nem Strong-számok)
    TEMATIKUS = 'tematikus'           # a lánc szavai nélkül: tematikus, nem lexikai kapcsolat


# --- a 4.2 kártya szegmentált idézetének jelölései (S3b) ---------------------------------------------------
class JelFajta(enum.Enum):
    MARK_NYIT = 'mark_nyit'          # adat: a motívum helye (Igehely)
    MARK_ZAR = 'mark_zar'
    ABBR_NYIT = 'abbr_nyit'          # adat: Feloldas
    ABBR_ZAR = 'abbr_zar'
    LRM = 'lrm'                      # a héber futam utáni irányjel
    KAROLI = 'karoli'                # adat: KaroliSzam (a könyv a forrás részlete, a számok egészek)
    NINCS_KAROLI = 'nincs_karoli'    # a szótár hivatkozása a Károliban nem létező versre
    FELULVIZSGALAT = 'felulvizsgalat'  # az elavult fordítás jele az idézet végén (T5, GK-15)
    KIEJTES = 'kiejtes'              # adat: a kiejtés (Forrasszoveg)
    CSONK = 'csonk'
    IDEZET = 'idezet'                # a lapmodellben: az idézet-darab (a szegmentált idézet szövege)                  # a rövidített vázlatsor jele; adat: tapadt-e (szóköz nélkül)


class FeloldasFajta(enum.Enum):
    CIMSZO = 'cimszo'                # a címszó rövidítése: adat a címszó és a kiejtése
    JAHVE = 'jahve'                  # a י׳ rövidítés
    JAHVE_CIMSZO = 'jahve_cimszo'    # a י׳, ha a címszó is י-vel kezdődik: mindkettő
    ALTALANOS = 'altalanos'          # a feloldás a szócikk szövegéből derül ki


class Dontes(enum.Enum):
    """A döntésnapló döntése egy jelöltről (B04 `dontes`)."""
    BEEPITVE = 'beépítve'
    ELUTASITVA = 'elutasítva'
    NYITVA = 'nyitva'


class Gyujtemeny(enum.Enum):
    """A kereszthivatkozás-gyűjtemény (S5): a Treasury of Scripture Knowledge vagy a Károli-fordítás."""
    TSK = 'tsk'
    KAROLI = 'karoli'


class AjanlasFajta(enum.Enum):
    """A kereszthivatkozásból vizsgált hely jelölésének forrása (B04 `forras_kereses`, S5)."""
    TSK = 'tsk'
    TSK_ALACSONY = 'tsk_alacsony'
    TSK_KAROLI = 'tsk_karoli'
    KAROLI = 'karoli'


class MegerositesFok(enum.Enum):
    """A Minősítés fokozata: a motívum helyeinek mekkora részét köti össze a két gyűjtemény (S5)."""
    EROS = 'eros'
    KOZEPES = 'kozepes'
    GYENGE = 'gyenge'
