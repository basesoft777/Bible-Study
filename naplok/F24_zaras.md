# F24 — zárójelentés (tervezet, az orkesztrátor véglegesíti)

*Ág: `claude/f24-licenc` · 2026.10.01 · `adat/licencek.tsv`, `adat/SEMA.md` 2.19, `DONTESEK.md` DT-F24.*

- **Leltár = sorszám (K1):** datasetek.tsv 21 egyedi dataset ∪ szerepmátrix (22 sor, 18 forráskulcs) ∪ a `konkordancia/` 153 bejegyzése (133 adatfájl/alkönyvtár, 20 dokumentáció/segédszkript, 0 lefedetlen) = **39** azonosító; a `licencek.tsv` **39** sor; mindkét irányú eltérés 0.
- A `BDB_etimologia_kezi_hatarok.tsv` a BDB sorhoz, a `Strongs bővítés` jegyzetfájl a `projekt_adat` sorhoz tartozik (nem adatkészlet).
- **Állapot:** 22 `tisztazott` (mindnek van `forras_hely`-e: K2), 17 `tisztazatlan`; kilenc `tisztazott` sorban `javaslat:` is áll.
- `kereskedelmi` és `share_alike` a `tisztazatlan` értéket is felveszi: minden `tisztazatlan` sorban `tisztazatlan/tisztazatlan`; a másodkézből vett állítás a `licenc` oszlopban marad.
- `share_alike=igen`: SDBH, SDGNT, UBS_DBH, UBS_DNTG, SDBH_SDGNT_segedtablak, tW_szocikkek, LSJ (az utóbbi `tisztazatlan`); mindnél SHARE-ALIKE jelzés a megjegyzésben.
- **Mérés:** a K1-ellenőrzés a szerkesztésen kívüli (nem repóba kerülő) szkripttel futott; `forras=manual`, a forrásrepók LICENSE-fájlját nem töltöttük le újra.
- **Nyitott:** DT-F24 (nyilvános nézetből kihagyandó források, kimeneti licenc, SEMA-bővítés jóváhagyása, N9 kód-oldali lezárása, LXX_kivonat–LEXV2_1 G6 ütközés).
- **K4:** `naplok/ELLENOR_F24.md` (javítókör után újraellenőrzendő).
