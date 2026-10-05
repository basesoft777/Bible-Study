# F18 zárójelentés — Nave-import (basokant)

- **Ág / PR:** `claude/nave-import` → draft PR a main-be. Ellenőrzés: `naplok/ELLENOR_F18.md` (2 kör + újramérés).
- **⛔ és döntés:** licencütközés (theonize GPLv3 vs playbook 2. pont) megállította a menetet; DT5 (felhasználó, 2026.09.30): 1. opció — a theonize nem kerül a repóba, helyi elemzésre sem; forrás basokant/nave, saját parszolóval.
- **Kész:** `eszkozok/nave_import.py`; `konkordancia/Nave_basokant.tsv` (85 246 adatsor, 5 322 téma, 77 985 igehely-sor) + README; `naplok/F18_licenc.md`, `naplok/F18_import_naplo.md`; szerepmátrix 2 sor (sorrend 12, `javaslat`); N27 lezárva javaslat-állapotban.
- **Eltérés a brieftől:** a kimenet neve `Nave_basokant.tsv` (nem `Nave_theonize.tsv`); az eredet-ellenőrzés a 4980 témán és a Gemini-lépés nem futott (nincs theonize-oldal), 0 USD.
- **Minőség:** 57 `gyanus_kijelzes` sor (53 töredék + javaslat, `igehely` nem átírva); az egyfejezetes könyvek 246 hivatkozása javítva, 4 jelölt. A jelölés teljessége nem bizonyított.
- **Nyitott (DT29):** teljes független kiadás-összevetés (letöltés-engedély kell); nyers `nave.txt` nincs a repóban, csak hash; SEMA 2.13 és `sorrend=12` (DT29 j); `adat/datasetek.tsv` Nave-sora; `naves-topical-bible.com` lekaparási feltételei (F24); FJ4↔F06 szám-eltérés (+1 fejléc valószínű, 4951↔4980 nem tárható fel, DT5 kizárja).
- **Ismert hiba:** négy korai commit-üzenet ékezet nélküli (nem javítható history-átírás nélkül); E11 (`szotar_szerepek.tsv:5`) base előtti.
- **Folytatási pont:** nincs; a DT29 tételei döntésre várnak.
