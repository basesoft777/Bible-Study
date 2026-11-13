# Hibanapló mechanizmus szerint

*Kézi napló (DT-F212f). Ide minden olyan hiba bekerül, amelyet a felhasználó talált meg a kapuk, a lektor és a független ellenőrzés után. A bejegyzés a **mechanizmust** rögzíti (honnan jön a szöveg vagy az adat, melyik kódrész rakja össze), nem a tünetet.*

**Szabály.** Ha egy új eset már szereplő mechanizmushoz tartozik, nem készül példányjavítás. Helyette gyökérok-elemzés és szerkezeti védelem jön (pozitív szabály, egyetlen hozzáférési pont, kapu), és a jelzés kimondja, hányadik esetről van szó. Lapkiadás előtt (`/kiadas` 3/b. lépés) a lapot érintő nyitott mechanizmusokat ellenőrizni kell.

Oszlopok: mechanizmus · esetek (dátum, hely) · állapot · szerkezeti védelem.

## M-CSERE — a látható szöveg belső adatszövegből, utólagos cserével készül

- **Mechanizmus.** A `eszkozok/lexikon_general.py` `olvasoi_atiras` → `_olvasoi_resz` függvénye kb. 50 regex-cserével alakítja a belső szöveget (proveniencia-sor, fájlnév, mezőnév, döntésszám, munkaszó) olvasói szöveggé. A fájlban 102 `re.sub`/`replace` áll. A tábla alatti jegyzet a proveniencia átírt változata, ezért ismétli a cellát. Az indoklás-mezők a címkével kezdődnek, a generátor pedig még egyszer kiteszi a címkét. Minden új adatalak (új motívum, szópár, új mező) új szivárgást vagy tört írásjelet hoz, és minden eddigi javítás egy újabb csere volt.
- **Esetek.**
  - HAMART-001 1. kiadás: a lap önmagára utaló szavai.
  - #178: „felhasználó”, „orkesztrátor” a lapon és a nyílt magban.
  - F182 (K05, A08): nyers proveniencia, mezőnév és fájlnév a lapon.
  - „gerinc” a látható szövegben.
  - 2026-11-13, ISTENTISZT-001 2. kiadás (a 2·5, a 3·10 és a 3·13 blokk): a jegyzet ismétli a cellát; címke-ismétlés („A formula nincs a versben: Nincs meg a formula a versben…”); forrásnév a mondat közepén („(a BDB-szótár)”); „hivatkozas_kezi,;”, „kollokacio … szerkesztő-chat … negativ_kriterium”. Ugyanez a kiadott HAMART-001-en is, kisebb számban.
- **Állapot.** Nyitott. Átmeneti védelem: minta-kapu a régi generátoron (ISTENTISZT 2. kiadás, #709). Szerkezeti megoldás: DT-F212e (az újraírt generátor alapszabálya).

## M-NYERS — a javított adat új fájlként jön, a nyers marad a bemenet

- **Mechanizmus.** A javítás új fájlként vagy hozzáférési pontként érkezik, a nyers fájl neve és helye változatlan, így minden fogyasztó, amelyet nem kötöttek át, és minden állapotot leíró sablon a nyerset olvassa tovább. A generált pillanatképek (mérés, napló) a lap bemenetei, de nincsenek a mai adathoz kötve.
- **Esetek.**
  - Károli-kereszthivatkozás: háromszor (a lapgenerátor és a nyílt mag szövege; F177 → F212, E40).
  - Teljesség-mérés pillanatképe (HAMART-001 1.2; F212, teljesség-kapu).
  - Angol Thayer nyersen a lapgenerátorban (N-F215a).
  - Szótári fordítás rossz bekötése az olvasóban (F213).
- **Állapot.** Részben védett (E40, teljesség-kapu). Szerkezeti megoldás: bemeneti jegyzék egyetlen hozzáférési ponttal (F217 és a generátor-újraírás).

## M-ZOLD — a zöld jelzést minőségnek vettük

- **Mechanizmus.** A kapu vagy a CI zöldje azt méri, hogy az ismert hibák hiányoznak, nem a lap minőségét, és nem mindig a pusholt commitra vonatkozik.
- **Esetek.**
  - #696: a CI zöldje egy régi commitra vonatkozott (F211: `headSha`-szabály).
  - 2026-11-13: a „0 BUKÁS” lapminőségként továbbítva, a lap olvasói átolvasás nélkül ment a felhasználóhoz.
- **Állapot.** Védve: F211 (`headSha`), F216 (`push_elott.py`), DT-F212f (olvasói átolvasás a `/kiadas` 3/b. lépésében).
