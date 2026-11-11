# #105 BDB_SZOREND — zárójelentés (2026-11-10; `claude-opus-5-5`)

- **Mérés (F105.1):**
  - 29 469 többszavas héber futam, ebből 17 953 ellenőrizhető a hivatkozott versen, és 12 308 eldönthető.
  - A megjelenítés egyezése a verssel 85,2%-ról 99,8%-ra nőtt (`naplok/F105_naplo.md` 3. és 6.).
- **DT710 (a) (F105.7–F105.9, F105.12, F105.14):** a szabály a DT445 útján épült meg, külön olvasói modul nincs.
  - A hivatkozott versen futó próba után 1 778 `jelolt_marad` sor lett `javitva`, 68 új sor került be, és 2 ütközés kézi sor lett. A meglévő `javitva` sorok közül egy sem változott.
  - A rafe-maqqéf feloldása a `bdb_rovidites.py`-ban van, a `kod_hash` a `bdb_szelet.py`-t is fedi.
  - A forrásfájl bájtra változatlan (`d4b15b2faea6…`).
- **⛔ Minták (napló 7. és 8.):** két független, vak Opus-kitöltő; a geres mindkét alakból eltávolítva.
  - Szórend: 50/50, Wilson 0,929–1,000.
  - Maqqéf: 49/50 = 98%, a ≥97%-os kapu teljesül, Wilson 0,895–0,996.
  - Maradék ismert hiba: a Préd 4:2 `עֲדֶנָה` és a `וּלְחֻמֿם`.
- **Lexikonlapok (F105.21, DT711):** 5 lap újragenerálva, 17 sor, csak szórend és maqqéf (a HAMART-001 1616. sorában az átírás-csoportosítással együtt). Az E28 0.
- **Egyeztetett eltérések** (orkesztrátori döntések a felhasználó felhatalmazásával):
  1. a `bdb_szoerend.py` helyett a DT445 útja (DT710);
  2. a mintát két vak kitöltő ítélte meg, nem a felhasználó;
  3. az 5 lap újragenerálása ebben a PR-ban (DT711);
  4. a `/elteres F105` ugyanebben a sessionben futott;
  5. a korlát fölötti 3. kör engedéllyel, újraellenőrzés nélkül (F105.33–F105.37).
- **Ellenőrzés:**
  - ELLENOR_F105: 7 eltérés, mind lezárva.
  - ELLENOR_F105_2: 4 eltérés, mind lezárva.
  - ELLENOR_F105_3: 2 eltérés, mindkettő a korlát fölötti körben lezárva, újraellenőrzés nélkül.
  - Folyamati hibám (F105.30): az ellenőri jelentéshez fűztem hozzá. Javítva: a jelentés visszaállt, a kiegészítés külön fájlban van.
- **Tesztek:** a `teszt_futtat.py --gyors` mind a 11 fájlja és a `teszt_bdb_rovidites.py` 39 tesztje zöld. A `futtat.py` HIBA nélkül fut. Az E36 (`SEMA.md`, két „2.34” cím) a main-ről öröklött.
- **Nyitott:**
  - N119: a csere alak szerint történik.
  - N120/c: OCR-hibák (pe/mem, a `עָפָד`); a pe/mem rendszerszintű, a #185 P4-ben generátor-szinten javítandó.
  - A #186 az ANTROP-001-et is újragenerálja: amelyik ág később kerül be, az olvassza be a main-t, és generáljon újra.
- **A `KETRETEGU_BDB_KARTYA`** kikapcsolva maradt (a #182 kapcsolja be).
