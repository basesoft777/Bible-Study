"""lapgen.szamitas.szotari_tipusok — a „Szótári háttér” szakasz pontjainak közös adatosztályai (a szó, a rövid
jelentés, a fordítás-állapottal jelölt rövid szöveg)."""
import dataclasses
from typing import Optional

from lapgen.szoveg import Lathato, Strong


@dataclasses.dataclass(frozen=True)
class Szo:
    """A motívum egy szava: a szótári alak és a kiejtés. Az `alak` hiánya: a szó nincs a rövid szótárban (a lapon
    ilyenkor a Strong-száma áll); a `kiejtes` hiánya kimondott hiány."""
    strong: Strong
    alak: Optional[Lathato]
    kiejtes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class Jelentes:
    """Rövid jelentés: a magyar szöveg, vagy magyar híján az angol eredeti (fordításra vár); mindkettő hiánya: a
    szótár nem ad rövid jelentést."""
    magyar: Optional[Lathato]
    angol: Optional[Lathato]
    elavult: bool = False


@dataclasses.dataclass(frozen=True)
class Szoveg:
    """Egy rövid forrásszöveg magyarul vagy (fordításra várva) angolul."""
    szoveg: Lathato
    forditasra_var: bool
    elavult: bool = False
