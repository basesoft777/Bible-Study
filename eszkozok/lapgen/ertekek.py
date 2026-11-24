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


class KapcsolatTipus(enum.Enum):
    """A motívumon belüli igehely-pár kapcsolatának típusa (B45 `tipus`, SEMA 2.3; S6)."""
    ELOKEP = 'Előkép'
    PARHUZAM = 'Párhuzam'
    BETELJESEDES = 'Beteljesedés'
    KONTRASZT = 'Kontraszt'
    VARIANS = 'Variáns'


class KapcsolatSzerkezet(enum.Enum):
    """A 7. szakasz következtetése a kapcsolatok típus-megoszlásáról (a régi `olvasoi_kovetkeztetes.kapcsolatok`)."""
    LANC = 'lanc'                    # a beteljesedés a kapcsolatok legalább fele: ígéret–beteljesedés lánc
    TULNYOMO_PARHUZAM = 'tulnyomo_parhuzam'
    TULNYOMO = 'tulnyomo'            # egy típus túlnyomó (nem a párhuzam)
    TOBBFELE = 'tobbfele'


class KapcsolatBiztossag(enum.Enum):
    """A 7. szakasz következtetése a magas bizonyosságú kapcsolatok arányáról."""
    SZINTE_MIND = 'szinte_mind'
    TOBBSEG = 'tobbseg'
    FELE = 'fele'
    KOZEPES_TOBBSEG = 'kozepes_tobbseg'   # a magas aránya fél alatt, a közepeseké fél fölött
    KEVES = 'keves'                       # a magas aránya fél alatt, a közepesek sincsenek többségben


class MotivumKapcsolatTipus(enum.Enum):
    """A motívumközi kapcsolat típusa (B46 `tipus`, SEMA 2.33; S6)."""
    SZOMSZEDOS = 'szomszédos'
    KOZOS_IGEHELY = 'közös_igehely'


class ForrasAllapot(enum.Enum):
    """Egy forrás állapota a bemeneti jegyzékben (B68 `allapot`; T7, GK-28): ebből és az adat tényleges állapotából jön
    a forrás-állapot mondata."""
    AKTIV = 'aktiv'
    KIVEZETVE = 'kivezetve'
    NEM_VIZSGALT = 'nem_vizsgalt'
    RESZLEGES = 'reszleges'


class TanuForras(enum.Enum):
    """A tanú forrása (B39 `forras`, SEMA 2.57; S7)."""
    HCF = 'hcf'                        # HistoricalChristianFaith kommentár-adatbázis
    SEFARIA = 'sefaria'                # Sefaria (rabbinikus források)
    GLOSSA = 'glossa'                  # Glossa Ordinaria (a Vulgata Clementina csomagjában)
    CHAIN_LINEAGE = 'chain_lineage'    # Chain Lineage Browser (verslánc, tényadat)


class ResElemFajta(enum.Enum):
    """A kézi rés elemének fajtája a lapmodellben (S8b)."""
    PROZA = 'proza'
    URES = 'ures'
    FORRAS = 'forras'               # a kézi forrássor helyén az olvasói forrássor
    SZAKIRODALOM = 'szakirodalom'   # a vitatott pont szakirodalom-sora


class IrodLicenc(enum.Enum):
    """A 12. szakasz forrássorának licencalakja (a jegyzék `irodalom` oszlopa, SEMA 2.66; S8c)."""
    LICENC = 'licenc'               # a licencleltár címkéje
    NYILT_MAG = 'nyilt_mag'         # a nyílt adatmagban kiadott saját adat
    ELOFORDULAS = 'elofordulas'     # az előfordulás-tábla: az adatoszlopok a nyílt magban, a magyarázat a projekté
    FORDITAS = 'forditas'           # a fordítástábla: a fordítás a projekté, a szótárszöveg licence a szótárnál
    DOI = 'doi'                     # a Károli–Strong párosítás: a címke és a közlés DOI-ja
    CHAIN_LINEAGE = 'chain_lineage' # tisztázatlan licencű külső forrás (a B01 `allapot`; ma a Chain Lineage Browser)


class VizsgaltCsoport(enum.Enum):
    """A vizsgált hely jelölésének forráscsoportja a 3. szakasz táblájában (a régi `szerep_kizart.CSOPORTOK` rendje;
    S9a)."""
    TSK = 'tsk'                        # TSK-ajánlás
    KAROLI = 'karoli'                  # Károli-kereszthivatkozás (a TSK-val együtt is)
    KERESES = 'kereses'                # a szavak keresése (gépi keresés)
    SZERKESZTOI = 'szerkesztoi'        # szerkesztői felvetés (a tanulmány, a napló, az ellenőrzés)


class JelolesFajta(enum.Enum):
    """A vizsgált hely jelölésének oka a döntésnapló `forras_kereses` mezőjének szerkezetéből (S9a)."""
    AJANLAS = 'ajanlas'                # kereszthivatkozás-ajánlás (TSK, Károli)
    SZO = 'szo'                        # a szó keresése (Strong-számok)
    SZOCSALAD = 'szocsalad'            # a szócsalád keresése
    SZOPAR = 'szopar'                  # két szó együtt egy versben
    LANC = 'lanc'                      # legalább két lánc-szó egy versben vagy a szomszédos versben
    TELJESSEG = 'teljesseg'            # a motívum szavainak teljes bibliai keresése (háló, csoportos kizárás)
    FRAZIS = 'frazis'                  # a kifejezés keresése a szavak helyzete szerint
    AUDIT = 'audit'                    # a motívum korábbi tanulmányának négyforrásos ellenőrzése
    TEMATIKUS = 'tematikus'            # a tematikus tanulmány felvetése
    NAPLO = 'naplo'                    # a kereszthivatkozás-napló minősítése


class VizsgaltJegyzetFajta(enum.Enum):
    """A 3. szakasz táblájának jegyzete: az a jelölési forrás, amelyet a „Miért került a vizsgálatba” cella nem mond
    ki (a cellát ismétlő jegyzet nem áll; a régi `tablajegyzet.ismetlo_jegyzet`). S9a."""
    SZOKERESES = 'szokereses'          # a szó keresése a cellán túli megszorítással (pl. igetörzs)
    KERESES_KORPUSZ = 'kereses_korpusz'    # a szó keresése egy megnevezett szövegkorpuszban
    LANC = 'lanc'                      # a lánc-keresés és a korpuszai
    ADATTABLAK = 'adattablak'          # a motívum adattáblái (a forrásnak nincs olvasói leírása)
    TELJESSEG_EGYENKENT = 'teljesseg_egyenkent'    # a teljes keresés, egyenkénti döntéssel
    NAPLO = 'naplo'                    # a motívum korábbi kereszthivatkozás-naplója


# --- a jóváhagyás frissessége (GK-27, F241.1): a bemenet méri (`bemenet/jovahagyas.py`), a Kolofon modellje hordozza

class Frissesseg(enum.Enum):
    FRISS = 'friss'
    CSAK_GENERALT = 'csak_generalt'
    ELAVULT = 'elavult'
    NINCS_ATNEZES = 'nincs_atnezes'   # nincs érvényes szerzői átnézés-sor (vagy egyik sem őse a HEAD-nek)
    NINCS_LAP = 'nincs_lap'           # a lap nincs a repóban (nincs utolsó commitja)


class Jovahagyas:
    """A frissesség eredménye: az állapot, az összevetett átnézés commitja és dátuma, a lap mai utolsó commitja."""
    __slots__ = ('allapot', 'atnezes_commit', 'atnezes_datum', 'lap_commit')

    def __init__(self, allapot, atnezes_commit=None, atnezes_datum=None, lap_commit=None):
        self.allapot, self.atnezes_commit = allapot, atnezes_commit
        self.atnezes_datum, self.lap_commit = atnezes_datum, lap_commit

    @property
    def kiadhato(self):
        return self.allapot in (Frissesseg.FRISS, Frissesseg.CSAK_GENERALT)
