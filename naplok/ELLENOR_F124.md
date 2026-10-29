# ELLENOR_F124 — F124_GERINC_KARTYA_BRIEF.md · `origin/main..HEAD` (0e607b2f..f75515b4)

*A `fuggetlen-ellenor` jelentése (modell: `claude-opus-5-5`, a kért `opus`; fájlíró eszköze nem volt, a jelentést a végrehajtó mentette, tömörítve, tartalom-hűen). A javítókör: F124.6 (c1cebea1), a javítások állapota a 3. szakaszban. Az ellenőr a teszteket nem futtatta (nem volt joga); a végrehajtó futtatta (14 + 25 + 20 teszt OK).*

## 1. Eltérések (10) és a javítás állapota

| # | Lelet | Súly | Javítás |
|---|---|---|---|
| 1 | **E16**: a workflow-t érintő PR címe `[ELLENŐRZŐ]` előtagot kíván; a zárás nem jelezte | magas | a PR címe `[ELLENŐRZŐ]`-val; zárás, napló 9. |
| 2 | A zárás 4. sora („lásd lent”) tesztkimenet nélkül állt | magas | a zárásban konkrét kimenet |
| 3 | A kártya nem importálja a `jelolt.py` függvényeit (a brief technikai döntése), a docstring ezt tévesen állította | közepes | docstring javítva; eltérés a napló 9. pontjában; az egyezést a `Egyezes` teszt őrzi |
| 4 | A térkép `ts`-e a tanulmánymappák teljes tartalmára érzékeny; a `general.py`, `lekerdez.py` nincs a bemenetben/`paths:`-ban; a git-azonosítót teszt nem mérte | közepes | `ts`: mappáknál csak A/D/R (`--diff-filter=ADR`); `general.py`, `lekerdez.py`, `strong_util.py` a bemenetben és a `paths:`-ban; új teszt (`GitAzonosito`) |
| 5 | DT-F124b, N-F124a/c és a napló 8/4., 8/7. pontja nincs felvéve; a brief `kovetkezo:` mezője elavult | közepes | felvéve (`DONTESEK.md`, `NYITOTT_FELADATOK.md`); `kovetkezo:` frissítve |
| 6 | Kiszűrt `nyitva` jelölt kiesett a `nyitva_db`-ből | enyhe | javítva + teszt |
| 7 | A `Sir` (Siralmak) 999-es rangot kapott a kanonikus sorrendben | enyhe | `konyv_index` alias + teszt |
| 8 | A napló próbaszámai mellől hiányzik a proveniencia | enyhe | a számok a `futtat()`/`gerinc_terkep.py` kimenetéből származnak (a futtatási parancsok a naplóban); külön proveniencia-sor nem készült — **elfogadott, nem javított** |
| 9 | Napló: „262 sor” (261), „24 értelmezhető” (23), „23+” (26) | enyhe | javítva |
| 10 | A DT-F124a forrása (a felhasználó szava) csak az orkesztrátor közvetítésében áll | információ | a `DONTESEK.md` az idézetet és a forrás-megjelölést rögzíti; a repóból nem igazolható, az orkesztrátor üzenete a forrás |

## 2. OK-ként igazolt pontok (az ellenőr saját lekérdezésével)

- Modell, törölt sorok (csak a brief `allapot`/`ir` sora), a `TAG_STRONGOK` = a brief listája, nulladiff a `jelolt.py`/`f110_szuro.py`/`adat`/`MUNKAMENET.md`/sablonok felé, a 3. és 7. ⛔ betartása, proveniencia 0 találatnál (Mt 24:37-39: mind a 8 Strong `n=0`), az 1Móz 6:4 K0-besorolása (`scan H8034`/`H7121`), a szűrő soronkénti egyezése az `f110_szuro.py`-val, a `--ir` csak `új`/`nyitva`, nincs írás az `elofordulasok.tsv`-be, tartomány-igehelyek (nincs `,;–—` az igehely oszlopokban), fájlnév-lefedettség (23 + 1, 401 vers), a workflow a `feladatok.yml` mintáján (hurokmentes), E12–E15 0 találat, CLAUDE.md-szabályok (nincs `csv`, wrapper a stdlib-importok után).

## 3. Nem ellenőrizhető az ellenőr által

- A tesztek és a `feladatok.py ellenoriz` futtatása (a végrehajtó futtatta: lásd `naplok/GERINC_KARTYA_zaras.md`).
- A „189 sor reprodukálva” állítás (teszt: `teszt_gerinc_szuro.py` `F110Egyezes`).
- A `--ir` viselkedése valós `jeloltek.tsv`-n (csak szintetikus teszt).
