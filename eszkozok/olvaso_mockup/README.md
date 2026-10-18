# Olvasói mockupok építő szkriptjei (archív)

Ezek a szkriptek készítették a #76 olvasói szerver továbbfejlesztési mockupjait (2026-10-15): az alap olvasófelület-mockupot, a nyolc változatot (Ez 37) és az olvasói konkordancia-mockupot (H7121). Az eredeti munkamenet ideiglenes könyvtárából kerültek ide, **változtatás nélkül**, hogy a mockupok és a technikai leírás számai visszakereshetők legyenek („PaRDeS olvasó – mockupok technikai leírása”, claude.ai artifact).

A mappa archívum, nem karbantartott eszköz: a szkriptek nem mennek át a repó szokásos ellenőrzésein, és nem futnak a `teszt_futtat.py` alatt.

## Mi nincs itt

- A kész mockup-HTML-ek (fájlonként ~4,8 MB): artifactként élnek, és a szkriptekből újraépíthetők.
- A köztes JSON-adatok (`ez37.json` ~15 MB, `nav.json`, `vadat.json`, `konk*.json`, `bdb.json`, `adat.json`): a `pardes.db`-ből újra előállnak.
- A külső igehely-felismerő próbája (Bible-Passage-Reference-Parser, `bpr/`): külső kód, bevezetéséhez döntés kell (`DONTESEK.md`).

## Ismert korlátok

- **Abszolút utak.** A szkriptek a fejlesztői gép útjait használják (`C:/Users/bases/Desktop/Bible-Study/pardes.db`; az `ez37_export.py` a WSL-ből: `/mnt/c/.../eszkozok/olvaso_szerver`). Más gépen ezeket át kell írni.
- **Saját könyvtár.** A bemenetet és a kimenetet a szkript saját könyvtárában keresik (`os.path.dirname(__file__)`), tehát futtatás előtt ideiglenes könyvtárba kell másolni őket; a repóba generált fájl ne kerüljön.
- **Kódlap.** Nem mindegyik szkript állítja UTF-8-ra a kimenetét; Windowson `PYTHONIOENCODING=utf-8` kell.
- **Adatbázis-állapot.** A mockupok a `pardes.db` 2026-10-14T09:35:00Z építéséből készültek; újabb adatbázisból más számok jöhetnek.

## A fő lánc (az alap és a nyolc változat)

1. `ez37_export.py <kimenet.json>` (WSL-venv): az Ez 37 lapjai a szerver saját lapelőállítójával (`oldalak.OldalGyar`) → `ez37.json`.
2. `nav_kinyer.py <kimenet.json>`: könyvek, fejezetszámok, kereszthivatkozások, Nave, motívumok → `nav.json`.
3. `valtozat_adat.py`: a változatok többletadata (kereszthivatkozott versek szövege, TIPNR-összesítés) → `vadat.json`.
4. `valtozat_epit.py`: az alap és a nyolc változat a `nav2_sablon.html`-ből és a `valt/` CSS/JS-fájljaiból (`v1`–`v8`, `linkek.json`).
5. (`nav2_epit.py`: az alap mockup korábbi, egylapos építője.)

## Az olvasói konkordancia-mockup (H7121)

`konk_kinyer.py konk.json` (adat) és `bdb_kinyer.py bdb.json` (BDB-jelentésszerkezet a szerver szeletelőjével) → `osszefuz.py` (→ `konk2.json`) → `vonzat.py` (vonzat gépi szabállyal, → `konk3.json`) → `epit.py konk3.json konk_sablon.html <kimenet.html>`. A sorrend a fájlok be- és kimeneteiből olvasható ki; az eredeti futtatási napló nincs meg.

## Segéd- és próbaszkriptek

`kinyer.py`, `minta.py`, `sema.py`, `blokk_lista.py`, `blokk_minta.py`, `ez37_minta.py`, `ez37_szerkezet.py`, `bdb_lefedes.py`, `vonzat_felmer.py`: felmérő és ellenőrző kódrészletek a mockupok készítése közben; a kimenetük nem került a mockupokba. `sablon.html`, `nav_sablon.html`: korábbi sablonváltozatok.
