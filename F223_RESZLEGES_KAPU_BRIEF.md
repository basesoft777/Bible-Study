---
feladat: 223
cim: A push előtti kapu részleges futtatása és a nyílt csomag-exportálók „csak szövegek” módja
kod: RESZLEGES_KAPU
tipus: feladat
fazis: folyamat
sav: SYSTEMS
modell: sonnet
allapot: fut
ad: a `push_elott.py` változott fájlok alapján csak az érintett lépéseket futtató módja (egy helyen definiált lépés → útvonalminta leképezéssel; bizonytalanságnál a teljes kapu); az (a) rész, a csomag-exportálók „csak szövegek” módja, a nyílt Károli-csomagok PR-ja után
kovetkezo: "Folytatás: a (b) rész kész és mért; az (a) rész várja a nyílt Károli-csomagok exportálóinak mergelését (local_be6e01b0)"
munka: folyamat
olvas: [eszkozok/ellenorzes/futtat.py, .github/workflows/ellenorzes.yml]
ir: [eszkozok/push_elott.py, eszkozok/teszt_push_elott.py, .claude/commands/kovetkezo.md, naplok/F223_jelentes.md]
fugg: []
nem_fugg: [216]
---

# F223_RESZLEGES_KAPU_BRIEF.md — Részleges kapu és „csak szövegek” export

*FELADATOK #223 · Modell: sonnet · v1 · 2026.11.15 · forrás: a felhasználó jóváhagyása (2026-11-15, „igen”, „mehet”), az orkesztrátor feladatleírása*

## 1. Cél

Két feladat, ugyanaz a hibatípus: **kis változásra teljes újrafutás**. A push előtti kapu minden futása a teljes helyi CI-t futtatja, és minden main-behozás után újra kell futtatni; a nyílt csomag-exportáló egy mondat javítására is a teljes adatot újragenerálja.

## 2. Tartalom

**(b) Részleges kapu** (`eszkozok/push_elott.py`). Új mód: a változott fájlok (`alap..HEAD`) alapján csak az érintett lépések futnak. A lépés → útvonalminta leképezés egy helyen áll (`RESZLEGES_LEKEPEZES`). Biztonsági szabály: ha egy változott fájl egyik mintára sem illeszkedik, vagy a leképezés bizonytalan, a teljes kapu fut. A CI teljes futása marad; a `--ci-egyezes` szabály nem gyengül. Teszt: brief-fejléc-változásnál a csomaglépések kimaradnak; ismeretlen fájlnál a teljes kapu fut. A futási időt előtte és utána, ugyanazon a változáson mérjük.

**(a) „Csak szövegek” mód** a nyílt csomag-exportálókban (MODSZER, README, KODKONYV, ISMERT_HIBAK és angol párjaik; az ellenőrzőösszeg-fájl rájuk vonatkozó sorai; fájlonkénti E35-összevetés). **Ütközés-korlát:** a nyílt Károli-csomagok exportálóit (`eszkozok/karoli_strong/…`, `eszkozok/nyilt_mag_export.py`, `nyilt_mag_szovegek.py`) a `local_be6e01b0` session írja; az (a)-hoz csak akkor nyúlunk, ha annak a PR-ja a main-en van.

## 3. Hatókör

`ir`: l. a fejléc. Az ellenőrzések (E1–E39) tartalmához és a workflow-hoz nem nyúl. A brief-fejlécekhez (a sajátján kívül) és a `NYITOTT_FELADATOK.md`-hez nem nyúl.

## 4. Kész, ha

- a részleges mód a leképezésből dolgozik, bizonytalanságnál a teljes kapu fut, a teszt zöld;
- a jelentés a (b) mért futási idejét előtte és utána, valamint az (a) állapotát tartalmazza;
- `feladatok.py ellenoriz` 0 hiba, draft PR.
