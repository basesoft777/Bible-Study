# ELLENOR_F79 (2. kör, a javító kör után) — F79_SQLITE_EPIT_BRIEF.md · `origin/main..HEAD` (0351f214 … dad31c86)

*A `fuggetlen-ellenor` jelentése, tömörítve; írási eszköz híján az orchestrator mentette. Az 1. kör: `ELLENOR_F79.md`. Az orchestrator futtatta: `feladatok.py ellenoriz` (107 brief, 0 hiba), `teszt_sqlite_epit.py` (34 teszt, OK).*

**Eredmény: ELTÉRÉS, 3 tétel (mind alacsony súlyú). Az 1. kör 9 eltéréséből 7 javítva (1–5, 8, 9); a 6. (TIPNR) N-F79c-ként a felhasználó döntésére vár, ez helytálló.**

## Eltérések
1. **G5 / TAGNT darabszám** (`sqlite_epit.py:457-461`): a Károli-vers nélküli három TAGNT-kulcs (Róm 3:31, 1Kor 3:23, Róm 8:39) a mérésben `3 / 3` előfordulással áll, a valós tokenszám 40 (`jelent_norm` kulcsonként egyszer fut).
2. **N-F79b hatóköre** (`NYITOTT_FELADATOK.md:55`): a zárónapló szerint a KJV-t is fedi, a tétel szövege nem frissült; kimaradt a KJV 146 érték / 702 sor, a `karoli_strong_kivonat` Jób 17:16-ja és a TAGNT 3 kulcs / 40 token.
3. **G4:** a 10. és 11. szabályra nincs negatív teszt (DT-F79a (7) óta építéskor futnak); a javító kör nem pótolta.

## Megjegyzések (kozmetikai)
- G2: a `--ketszer` azonos processzben épít; a processzek közti bizonyíték: a kódhoz nem nyúló táblák hash-e a 07:42-es és a 08:12-es teljes naplóban azonos.
- Méret: a „szabad lapok” magyarázat fordított; a táblák összege (845,6 MB) > fájl (845,4 MB) többletét a táblánkénti külön adatbázisok fejléc- és séma-lapjai adják.
- N-F79c: „22 érték” helyett a mért szám 22 *sor*; a számok proveniencia nélkül állnak.

## Igazolt OK
G1, G3, G6 (morf_* + új táblák), G7 (proba_minta, szúrópróbák egyeznek: H0922, H8414+H0922, G0012, H8415), G8, KJV (349 308 = 348 606 + 702), TBESG 11 035 / TBESH 11 682, `Karoli_Strong_kivonat` 383, M0 sorszámok, brief DT-F79a, N-F79a/c, CI (`futtat.py` exit 0), Δ = 0 az `adat/` és `konkordancia/` alatt.

## NEM ELLENŐRIZHETŐ
DT-F79b tartalma (a felhasználó chatbeli jóváhagyása a repóból nem igazolható); a ⛔ pontok felhasználói jóváhagyása; a lekérdezés-próba 2., 3., 5., 6., 13. pontja nem futott újra.
