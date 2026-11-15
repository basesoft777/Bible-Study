# Hibanapló mechanizmus szerint

*Kézi napló (DT824). Ide minden olyan hiba bekerül, amelyet a felhasználó talált meg a kapuk, a lektor és a független ellenőrzés után. A bejegyzés a **mechanizmust** rögzíti (honnan jön a szöveg vagy az adat, melyik kódrész rakja össze), nem a tünetet.*

**Szabály.** Ha egy új eset már szereplő mechanizmushoz tartozik, nem készül példányjavítás. Helyette gyökérok-elemzés és szerkezeti védelem jön (pozitív szabály, egyetlen hozzáférési pont, kapu), és a jelzés kimondja, hányadik esetről van szó. Lapkiadás előtt (`/kiadas` 3/b. lépés) a lapot érintő nyitott mechanizmusokat ellenőrizni kell.

**Felhasználó által talált hiba (DT852).** Minden hibához, amelyet a felhasználó talált, a javítókörben (`/lap-javit` 5. 3/b., `/kiadas` 4.) kötelező megnevezni a mechanizmust ebben a naplóban (meglévőt vagy újat). Ha a mechanizmus már szerepel, a tétel gyökérok-jelölést kap (hányadik eset), nem csak példányjavítást. Különösen igaz ez arra a hibára, amelyen minden kapu átengedett: az önmagában hibanapló-tétel.

Oszlopok: mechanizmus · esetek (dátum, hely) · állapot · szerkezeti védelem.

## M-CSERE — a látható szöveg belső adatszövegből, utólagos cserével készül

- **Mechanizmus.** A `eszkozok/lexikon_general.py` `olvasoi_atiras` → `_olvasoi_resz` függvénye kb. 50 regex-cserével alakítja a belső szöveget (proveniencia-sor, fájlnév, mezőnév, döntésszám, munkaszó) olvasói szöveggé. A fájlban 102 `re.sub`/`replace` áll. A tábla alatti jegyzet a proveniencia átírt változata, ezért ismétli a cellát. Az indoklás-mezők a címkével kezdődnek, a generátor pedig még egyszer kiteszi a címkét. Minden új adatalak (új motívum, szópár, új mező) új szivárgást vagy tört írásjelet hoz, és minden eddigi javítás egy újabb csere volt.
- **Esetek.**
  - HAMART-001 1. kiadás: a lap önmagára utaló szavai.
  - #178: „felhasználó”, „orkesztrátor” a lapon és a nyílt magban.
  - F182 (K05, A08): nyers proveniencia, mezőnév és fájlnév a lapon.
  - „gerinc” a látható szövegben.
  - 2026-11-13, ISTENTISZT-001 2. kiadás (a 2·5, a 3·10 és a 3·13 blokk): a jegyzet ismétli a cellát; címke-ismétlés („A formula nincs a versben: Nincs meg a formula a versben…”); forrásnév a mondat közepén („(a BDB-szótár)”); „hivatkozas_kezi,;”, „kollokacio … szerkesztő-chat … negativ_kriterium”. Ugyanez a kiadott HAMART-001-en is, kisebb számban.
- **Állapot.** Nyitott. Átmeneti védelem: minta-kapu a régi generátoron (ISTENTISZT 2. kiadás, #709). Szerkezeti megoldás: DT823 (az újraírt generátor alapszabálya).

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
- **Állapot.** Védve: F211 (`headSha`), F216 (`push_elott.py`), DT824 (olvasói átolvasás a `/kiadas` 3/b. lépésében).

## M-RÁRAKÓDÁS — új hely kerül be, a régi nem kerül ki

- **Mechanizmus.** Egy javítás vagy új szerkezet új helyet ad egy tartalomnak, a régi helyét viszont nem szünteti meg, így ugyanaz az állítás több helyen él, és a példányok eltérnek. Minden hely helyben helyesnek látszik; az ismétlés csak a teljes lapot vagy térképet nézve látszik.
- **Esetek.**
  - 2026-11-08, F178 (új lapszerkezet): a kritérium új helyre került, a régi helye megmaradt; a kritérium négyszer áll a HAMART-001 lapon.
  - 2026-11-13: ugyanez a minta a generátor blokkjaiban (két blokk ugyanazt az adatot más-más forrásból olvassa), a teljes bekötési térképen (357 tétel) látszott meg.
- **Állapot.** Nyitott. Szerkezeti megoldás: az újraírt generátorban egy bemeneti réteg, egy hozzáférési pont adatforrásonként (DT-F218; F218a).

## M-GAZDÁTLAN — a lezárás a merge utánra esik, és nincs gazdája

- **Mechanizmus.** A feladat tartalma a merge-gel elkészül, a lezárása (brief állapota, nyitott tételek, jegyzék) a merge utáni lépésre marad, amelyet senki nem vállal, így a lezárás elmarad.
- **Esetek.**
  - 2026-11-15, a gyökérok-jelentés idején: 35+ mergelt, de nyitott brief és 265 nyitott N-sor.
- **Állapot.** Nyitott. Szerkezeti megoldás: a gépi lezárás (PR #731).

## M-VAKFOLT — hatókör-szűkítés után ellenőrizetlen réteg marad

- **Mechanizmus.** Egy ellenőrzés hatókörét szűkítik (teher csökkentése, lektor a prózára), de senki nem mondja ki, mi marad ezzel ellenőrzés nélkül, és mi méri helyette. A kiesett réteget (itt a generált szöveg) olvasóként csak a felhasználó olvasta, és a hibák nála bukkantak fel, a kiadás közelében.
- **Esetek.**
  - 2026-11-10, DT742 (#685): a független ellenőr a generált lapot már nem olvassa; senki nem pótolta.
  - 2026-11-11: a lektor a prózára szűkül, a generált blokkokat a kapukra bízzák; a HAMART v6-on 14 hiba, mind generált blokkban.
  - 2026-11-13: ISTENTISZT-001 2. kiadás, ugyanazok a hibák a kiadott HAMART-001-en is.
- **Állapot.** Védve: a hatókör-szűkítés szabálya (DT852; `BRIEF_SABLON.md`, `/befogad` ellenőrző pont), a pozitív kapuk és a `/kiadas` 3/b. olvasói átolvasása. A nyílt rész: az új generátor olvasói kapuinak mérése a TEREMT-001-en.
