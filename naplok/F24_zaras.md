# F24 — zárójelentés (tervezet, az orkesztrátor véglegesíti)

*Ág: `claude/f24-licenc` · 2026.10.01 · `adat/licencek.tsv`, `adat/SEMA.md` 2.19, `DONTESEK.md` DT-F24.*

- **Leltár = sorszám (K1):** `datasetek.tsv` 21 egyedi dataset ∪ szerepmátrix (22 sor) ∪ `konkordancia/` (153 bejegyzés: 133 adatfájl/alkönyvtár, 20 dokumentáció/segédszkript, 0 lefedetlen) = **39** azonosító; a `licencek.tsv` **39** sor; mindkét irányú eltérés 0 (a leltár-ellenőrző szkript futtatásával mérve, nem a repóban).
- A `BDB_etimologia_kezi_hatarok.tsv` a BDB sorhoz, a `Strongs bővítés` jegyzetfájl a `projekt_adat` sorhoz tartozik (nem adatkészlet).
- **Állapot (a táblából számolva):** 21 `tisztazott` (mindnek van `forras_hely`-e: K2), 18 `tisztazatlan`; nyolc `tisztazott` sorban `javaslat:` is áll (Karoli_KH, TAGNT, TAHOT, TIPNR, Macula_heber, TBESH, TBESG, KJV_Strongs_teljes).
- `kereskedelmi`/`share_alike`: mind a 18 `tisztazatlan` sorban `tisztazatlan/tisztazatlan` (a másodkézből vett állítás a `licenc` oszlopban); a TBESH, TBESG, TAGNT, TAHOT, TIPNR `kereskedelmi=feltetelesen` (a STEPBible-fejléc terjesztési kérése, TBESH-nál az Online Bible engedélye).
- `share_alike=igen`: SDBH, SDGNT, UBS_DBH, UBS_DNTG, SDBH_SDGNT_segedtablak, tW_szocikkek (`tisztazott`), LSJ (`tisztazatlan`); mindnél SHARE-ALIKE jelzés a megjegyzésben.
- **Mérés:** a forrásrepók LICENSE-fájljait nem töltöttük le újra; a licencek a repó READMEiből, naplóiból és a repóban lévő forrásfájlok fejlécéből (TBESH.txt, TBESG.txt) valók, `forras=manual`.
- **Nyitott:** DT-F24 (nyilvános nézetből kihagyandó források, TBESH/Online Bible-engedély és a STEPBible-terjesztési kérés, kimeneti licenc, SEMA-bővítés jóváhagyása, N9 kód-oldali lezárása, LXX_kivonat–LEXV2_1 G6 ütközés).
