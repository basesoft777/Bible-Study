# F227 jelentés — DESIGN sáv

## Menet

A `DESIGN` bekerült a `SAVOK`-ba (`feladatok.py`), a `SAV_SORREND`/`SAV_CIMKE`/`OTLET_SAVOK`-ba (`heti_beosztas.py`), a `BRIEF_SABLON.md`-be és a `SEMA.md` három sáv-értékkészletébe; teszt a `teszt_feladatok.py`-ban és a `test_heti_beosztas.py`-ban. Futtatva: `teszt_feladatok` (232, OK), `test_heti_beosztas`, `test_feladatok_fugges`, `test_heti_attekinto`, `test_keret_meres` OK; `ellenoriz`: 0 hiba. A #123-mal szembeni KIZAR/SORREND átlépése a felhasználó döntése, 2026-11-18; a #123 nem futott.

Jelentendő (nincs az `ir`-ben): `keret_meres.py` (`SAVOK`, `CIM_SAV`) és `heti_attekinto.py` (`SAVOK`) külön sávlistát tart.

## Független ellenőrzés — 1. ellenőrzés

ELTÉRÉS: 3 tétel

F227_DESIGN_SAV_BRIEF.md · `origin/main...HEAD` (merge-base `0eb8a575`, head `207bdab9`), 1. ellenőrzés, szint: teljes

- **CI:** OK — futás 44366833418, headSha 207bdab9…, success (`feladatkovetes`, `ellenorzes`).
- **Teendő 1, 2, 3, 5:** OK (`feladatok.py:69,443-447,1064`; `BRIEF_SABLON.md:37`; `SEMA.md:2394,2436,2469`; tesztek valóban a DESIGN-t fedik; `ellenoriz` 0 hiba).
- **Teendő 4 / ELTÉRÉS** (`heti_beosztas.py:67`): a brief `'DESIGN': 'Design'`-t ír elő, a diffben `'Design (kinézet, arculat)'` áll.
- **Teendő 4, jelentendő külön sávlisták / ELTÉRÉS** (`keret_meres.py:51,55,115-116,364-369`): a `keret_meres.SAVOK` és `CIM_SAV` nem tartalmazza a DESIGN-t. (a) `hozzarendel()` (`:302-306`) `'DESIGN'`-t adhat vissza, az `osszesit()` `savok[sav]` hívása `KeyError`-t dobna egy `sav: DESIGN` briefhez tartozó ágon futott sessionre. (b) A SEMA 2.64 elfogadja a DESIGN-t a `keret_munkamappa.tsv`-ben, a validátor (`:115-116`) hibát jelez rá. A kódot olvasta, futtatással nem próbálta. A `heti_attekinto.py`: nem összeomlás, a DESIGN „Besorolatlan” lesz (jelentve).
- **Ell. 5 / ELTÉRÉS:** a diff az `eszkozok/tesztek/test_heti_beosztas.py`-t is írja, ami nincs az `ir` listán (tartalmilag a teendő 5 része). Tiltott útvonal nem változott.
- Kozmetikai: a commitüzenet „2.61”-et ír, a módosított hely a `heti_otlet`; a `test_sav_ot_elemu_es_business_ervenyes` név már hat elemet takar; a `keret_meres` DESIGN-útját nem fedi teszt.
- Nem ellenőrizhető: `teszt_futtat.py --diff origin/main` végeredménye (CI: `TESZT_KILEPES: 0`).
- A1–A6, Ell. 1–4: OK (nincs tartalmi réteg, TSV-delta 0, generált kimenet nem változott).

## Állapot

A menet a 9. lépés szerint megáll: a javítókör külön sessionben fut (`/elteres 227`).
