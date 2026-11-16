"""lapgen.bemenet — a bemeneti réteg: az egyetlen hely, amely adatfájlt nyit.

Szerződés (F218a brief 4. pont):
- B-azonosítónként egy nyilvános függvény (`b<nn>_<név>`); az útvonal a jegyzéktáblából jön.
- Betöltéskor kapu: létezés, oszlopnév szerinti fejléc, a javítótábla alkalmazva, frissesség.
- Hiányzó kötelező bemenet: `BemenetHiba`. Opcionális hiánya: kimondott hiány a lapmodellben.
- A kimenet változtathatatlan; gyorsítótár csak itt van, a fájl hash-ére kulcsolva.
- Minden olvasás a naplóba kerül (`Bemenet.olvasasi_naplo()`).

A nyers szöveg csak burkolóban hagyja el a réteget (`Kezi`, `Forrasszoveg`, `Belso`, `Kulcs`,
`Utvonal`; l. `lapgen.szoveg`), a nyilvános azonosítók saját típusban (`Igehely`, `Strong`, `MotivumId`).
"""
from lapgen.bemenet.alap import b01_licencek, b51_dontesek, b59_befagyasztott
from lapgen.bemenet.elofordulas import b03_elofordulasok, b07_karoli
from lapgen.bemenet.jegyzek import Bemenet, BemenetHiba
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.bemenet.nyelv import NevHiba, Nyelv, b65_nevtabla, b66_sablonok, nyelv

__all__ = ['Bemenet', 'BemenetHiba', 'NevHiba', 'Nyelv', 'nyelv',
           'b01_licencek', 'b03_elofordulasok', 'b07_karoli', 'b51_dontesek', 'b59_befagyasztott',
           'b63_konyvek', 'b65_nevtabla', 'b66_sablonok']
