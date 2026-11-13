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


class SzovetsegKod(enum.Enum):
    """Az előfordulások megoszlása a két szövetség között (az összegző mondat következtetés-kódja)."""
    FOKENT_OSZ = 'fokent_osz'
    FOKENT_USZ = 'fokent_usz'
    MINDKETTO = 'mindketto'
    CSAK_OSZ = 'csak_osz'
    CSAK_USZ = 'csak_usz'
