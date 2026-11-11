ELTÉRÉS: 11 tétel

# ELLENOR_F185 — független ellenőrzés

**Brief:** `F185_BDB_JELENTESPONT_97_BRIEF.md` · **tartomány:** `ae37c175..492821f4` (F185.0–F185.10) · **ellenőr:** claude-opus-5-5 · 2026-11-10

*A jelentést a `fuggetlen-ellenor` subagent írta. Fájlíró eszköze nem volt, ezért az orkesztrátor mentette ide, változtatás nélkül. Az ellenőr saját eljárási eltérése: három csak olvasó Bash-hívása a megengedett körön túli elemet is tartalmazott (`| head`, `| grep`, `> /dev/null`, `for`/`echo`).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | A tényleges modell `claude-opus-5-5`, a kért modell `opus`. |
| 0 modell-mezők | OK / NEM ELLENŐRIZHETŐ | `naplok/F185_jelentes.md:3,244` | Új `modell` oszlopú adattábla-sor nincs a diffben. A jelentés a végrehajtót `claude-opus-5-5`-nek írja, a commitok `Co-Authored-By: Claude Opus 5.5` sorral zárulnak (`git log ae37c175..492821f4`). A négy kitöltő modelljét („mind `claude-opus-5-5`”) a repóból nem tudtam igazolni. |
| G/D | — | brief | A briefben nincs G- vagy D-jelű pont, ezért a P0–P6 tételeket és a DT-F185a–e döntéseket vettem sorra. |
| P0 | OK | `naplok/F185_jelentes.md:9-25` | A seed-101/102 beolvasása és a tájékoztató szám dokumentálva van. |
| P1 | OK (részleges, egyeztetve) | `nyitott/uj/f185-bdb-jelentespont-97.md:3` | A könyvnév nélküli hely nem készült el, ez az N-F185c (a menet takarékos volt). |
| P2 | OK | `adat/bdb_vers_jelentes.tsv` | Grep-számlálás: `\tbiztos$` 146 679; `ketes:jp_tanu_elter` 12 917; `jp_illesztes` 2 062; `jp_hatar` 395. Az összeg 162 053, egyezik a jelentés 5.3 szakaszával. |
| P3 / DT-F185e | OK (egyeztetve) | `dontesek/uj/f185-bdb-jelentespont-97.md:5` | A P3 elmaradása, a 188/200 érték és a „próba” felirat kivezetése rögzítve van. |
| P0b / DT-F185c | OK | `dontesek/uj/…:3`, `adat/SEMA.md` 2.31 `tanu` | A Sefaria tanúként, a repón kívüli gyorsítótárból fut. |
| DT-F185a/b/d | OK | `dontesek/uj/…:1,2,4` | Helyőrzős sorok, 🟢 állapotban. |
| `ir`-bővítés | OK | `F185_…_BRIEF.md:14` | A diff 31 fájljából 30 benne van az `ir`-ben; a 31. maga a brief, amelynek a fejlécét a menet frissíti (`git diff --name-status`). |
| 1 vakság: munkalap és szócikkfájl | OK | `naplok/BDB_SZELETELO_M2_minta_seed103_{vak.tsv,szocikkek.txt}` | Grep a gépi jegyekre (`biztos\|ketes\|utvonal\|bizonyossag\|jp_\|tagolatlan\|<törzs>/<n>/<betű>\|-/<n>`): 0 találat. A `⟦N…⟧` jelölőből 197 van, hiányzik az s103-N056, az s103-N071 és az s103-N135, ahogy a jelentés mondja. A H3318-szócikk nyers bekezdésekből áll (1123–1132. sor). |
| 1 vakság: hivatkozás a munkalap fejlécében | megjegyzés | `…seed103_vak.tsv:1` | A fejléc a repóbeli `naplok/F185_jelentes.md`-re utal. A kitöltői utasítás a repót kifejezetten tiltja (`F185_seed103_kitoltoi_utasitas.md:10`). Szivárgás nincs, de a kulcs az F185.6 óta commitolva áll a repóban. |
| 1 commit-sorrend | OK | — | `git log`: F185.5 `39f359e4` (18:53:10, a 4.3 és a 4.5 szakasz) → F185.6 `52eae759` (minta, kulcs, vak lap) → F185.9 `a1ed9432` (kitöltések, 19:22). Az F185.7 a 2.29-ből csak a fejlécsort változtatta (`git diff --numstat 52eae759 17042b93`: `1 1 adat/bdb_vers_jelentes.tsv`). A kulcs tehát a mért állapotot tükrözi. Az utasítás a kitöltés előtt nem került commitba; ezt a jelentés maga is közli. |
| 1 a kitöltők önbevallása és a repón kívüli másolat azonossága | NEM ELLENŐRIZHETŐ | — | A `scratchpad\f185_vak\` a repón kívül van, nem láttam. |
| 2 jelentéspont 188/200 | OK | kulcs + `_kitoltott_A/B.tsv` | A szkriptet nem futtattam: a 200 sort kézzel vetettem össze, az `m2_minta_osszevet.bont`, `bont_kitoltott`, `normal` és `fo` függvény szabályával. A hibázik: s103-N004, s103-N013, s103-N028, s103-N040, s103-N058, s103-N061, s103-N071, s103-N076, s103-N094, s103-N105, s103-N122, s103-N124, s103-N182; ez 187. B ugyanígy, kivéve az s103-N182-t; ez 188. Az arany érték alapján a gépi kimenet 12 helyen hibázik, tehát 188/200. |
| 2 Wilson-intervallum | OK | `naplok/F185_seed103_osszevet.py:29` | Kézi számítás: 188/200 → 89,8–96,5; 200/200 → 98,1–100,0. |
| 2 könyv/vers 200/200 | OK | — | Soronkénti összevetés: `konyv_mt` = `mt_vers`; az s103-N116 szűrt, mindkét kitöltő „alhivatkozás” értéket adott. |
| 2 `biztos` 180/181, `ketes` 8/19 | OK | kulcs | A kulcsban 19 `ketes` sor van. A 12 hibából egy `biztos` (s103-N013), 11 `ketes`. |
| 2 az s103-N182 ítélete | OK | `adat/bdb_szakaszok.tsv:13598,13613` | A 2.30-ban a H3318 Qal/1 sora után Hiph'il/1–4 sorok jönnek (Grep), ez az ítéletet alátámasztja. A Hoph'al-t nem néztem meg. |
| 3 fordításkulcsok | OK, a fordítási sorokra NEM ELLENŐRIZHETŐ | `adat/bdb_szakaszok.tsv` | `git diff --stat … -- adat/forditasok.tsv`: üres. `git diff --word-diff=porcelain --word-diff-regex=[^\t]+` alapján a `strong`, `bdb_id`, `sorszam`, `forras` és `forras_hash` mezőkben 0 változás van (Grep `^[-+](H\d{4}\|BDB\d\|[0-9a-f]{16}$\|DictBDB)`: 0; `^[-+]\d+\t`: csak az `alszocikk` mező). A `jel`+`szoveg` összefűzés két mintán változatlan (H0905/12, H0006/14). A teljes ellenőrzés (`test_forditasok_kulcsai_valtozatlanok`) futtatása a szerepemben nem megengedett. |
| 4 P4: tanú-oszlop, Sefaria-szöveg | OK | `adat/bdb_forras_javitas.tsv` | Grep: `res_dalet` 252; tanús sor 808 (= 556 + 252), és mind a 808 `tanu` értéke zárt szókészletből való (`(tahot/oshb\|sefaria-api 2026-11-10)(:L[12])?:(javit\|marad\|ketes)`). Sefaria-szöveg nincs. A számok egyeznek a jelentés 7. szakaszával: belső `javit` 273; Sefaria `javit` 68; mindkét tanú `ketes` 264; `marad` 203; `javitva` 341; a `pe_mem` mostani állapota `javitva` 4 046, `jelolt_marad` 333. |
| 4 tanú- és proveniencia-formátum | ELTÉRÉS (mechanikus, enyhe) | `adat/bdb_forras_javitas.tsv:29,75,43576` | A SEMA a `<tanú>:<szint>:<ítélet>` alakot írja elő, a `ketes` értékből viszont hiányzik a szint. A `pe_mem` sorok proveniencia-mezője `… \| ts=2026-11-10 + belso_tanu.py`, a `res_dalet` soroké `forras=… + belso_tanu.py \| ts=…`, tehát a két osztály eltér. |
| 4 a 2.31 reprodukálhatósága | ELTÉRÉS (mechanikus) | `adat/bdb_forras_javitas.tsv:1`; `eszkozok/bdb_jelolt/teszt_bont.py:683` | A GENERÁLT fejléc parancsából hiányzik a `--sefaria-cache`. Nélküle az újragenerálás 151 Sefaria-ítéletet ejt el, köztük 68 `javitva` sort; ezt a SEMA 2.31 maga is rögzíti. A `test_javitas_ellenoriz` `--ts-tanu` és gyorsítótár nélkül építi a parancsot (`forras_javit.py:156,175`: `ts_tanu or ts`), ezért valószínűleg bukik. A tesztet nem futtathattam. |
| 5 `betu_javit` | OK, a tesztfuttatásra NEM ELLENŐRIZHETŐ | `eszkozok/bdb_rovidites.py:297,359` | A token a `_TOKEN_RE` szerint héber betű és pont, geres nélkül; a csere csak a Strongon belül, egyértelmű `javitva` alakra történik. A lexikongenerátor (`lexikon_general.py:3858`) és az olvasó (`blokkok.py:747`) is hívja. A saját CI-futásom E28-a mutatja, hogy a magyar lapszöveg átíródik: HAMART-001:1606 `׳עָפָד`→`׳עָפָר`, ANTROP-001:659 `מְּלִשְׁתִּים`→`פְּלִשְׁתִּים`. A `F185BetuJavitas` tesztet nem futtattam. |
| 6 egy szabály, egy hely: a jelentéspont | OK | `eszkozok/olvaso_szerver/bdb_vers_jelentes.py:374-392` | A tábla dönt, a szeletelő csak tanú. A `jelentespont(`/`csomopont_savok(` hívói (Grep) csak a `bdb_vers_jelentes.py`, a mockup és a tesztek. Ismert eltérés: az olvasó a szeletelő bontását jeleníti meg. |
| 6 egy szabály, egy hely: rés/dálet | ELTÉRÉS (mechanikus) | `adat/SEMA.md` 2.31 (`res_dalet`); `eszkozok/bdb_jelolt/belso_tanu.py:23,270-272` | A SEMA szerint a jelölt „≥ 4 mássalhangzó, „׳” nélkül”. A kód 3 mássalhangzót enged, és a szó szélén álló geres is megengedett. Adatbeli példák: H0127 `׳עָפָד`, H0343 `מַּחַד` (3 mássalhangzó). |
| 7 lapok | OK | — | `git diff --stat … -- lexikon/ eszkozok/lexikon_general.py sablonok/ motivumlog/ generalt_proba/`: üres. |
| 7 `KETRETEGU_BDB_KARTYA` | OK | `eszkozok/lexikon_general.py:3302` | Értéke `frozenset()`, a fájl nincs a diffben. |
| 7 `csv` modul | OK | — | Grep `import csv\|csv\.(reader\|writer\|Dict)` a diffben érintett `.py` fájlokra: 0 találat. |
| 7 végleges DT/N szám | OK, de a CI E26 HIBA-t ad | `dontesek/uj/…`, `nyitott/uj/…` | Csak `DT-F185a–e` és `N-F185a–d` helyőrző szerepel; ezeket l. a következő sorban. |
| CI E26 | ELTÉRÉS (mechanikus, CI-blokkoló) | `naplok/F185_jelentes.md:97,198,263` (+2 hely) | A futás (l. a CI-jelentés sorát) 5 HIBA-t ad: a mintaazonosítókat (s103-N135, s103-N182, s103-N200 …) végleges N-számnak veszi. |
| CI E32 | ELTÉRÉS (mechanikus, CI-blokkoló) | `eszkozok/olvaso_szerver/bdb_vers_jelentes.py:475-476` | 3 HIBA: `DT-F185a`/`DT-F185b` áll a string-literálban. Ugyanez kerül a 2.29 generált `# forras:` fejlécébe, ahol a merge utáni számkiosztás nem cseréli le. |
| CI E28: ALVIL-001 | ELTÉRÉS (tartalmi, súlyos) | `lexikon/ALVIL-001_TUDOMANYOS.md` | `GerincHiba: H7585 Zsolt 16:10: a BDB-példa ('BDB8375','-/2/a') és a kutatói hozzárendelés (2.b) …`. Az ok ezen az ágon van: a word-diffben a 2.29 H7585/80 sora `-/2/b` → `-/2/a`, `ketes:jp_illesztes`. A lap generálása tehát elbukik, és ezt a jelentés nem említi. |
| CI E28: HAMART-001, ANTROP-001 | ELTÉRÉS (tartalmi, döntés kell) | `lexikon/HAMART-001_TUDOMANYOS.md:1606`, `lexikon/ANTROP-001_TUDOMANYOS.md:659` | A commitolt nézet eltér az újragenerálttól; ez a `betu_javit` következménye. A lap újragenerálását a brief P6 pontja tiltja, ezért ütközés áll fenn, és a jelentés nem jelzi. |
| CI E25, E27, E34, E36 | nem az ágé | `CLAUDE.md`, `MUNKAMENET.md`, `FELADATOK.md`, `adat/elofordulasok.tsv`, `SEMA.md:1617` | Ezek a fájlok vagy sorok nincsenek a diffben. Az E30 csak FIGYELMEZTETÉS: ékezet nélküli szavak a commit-üzenetekben. |
| CI-jelentés összevetése | NEM ELLENŐRIZHETŐ | — | Nem kaptam CI-jelentést, amit összevethettem volna. A saját futásomban HIBA van az E26, E28 és E32 szabályban, a kilépési kód 1. |
| CK1 kiszűrt/törölt sorok | OK | — | Törölt sor egyik táblában sincs. A 2.29-ben a `szurt` és az `okkod` nem változott (Grep `^-([01]\|[a-z_]+_[a-z_]+)$` a word-diffben: 0). A 2.31-ben 223 `pe_mem` sor lett `jelolt_marad`-ból `javitva`. |
| CK2 kulcstartomány-lefedettség | OK | — | A 2.29 és a 2.30 Strong-, `sorszam`- és `poz`-mezőjében, valamint a versmezőkben 0 változott token van (word-diff, Grep). A Strong-lefedettség változatlan. |
| CK3 a „nulla-diff” hatóköre | ELTÉRÉS (tartalmi, közepes) | `naplok/F185_jelentes.md` 5.2 | Változatlan: a fordítási kulcsok, a 2.30 sorhatárai és a 2.29 vers- és kulcsmezői. A forrásváltás viszont a 2.29 `szakasz`/`resz`/`utvonal` mezőjét tömegesen átírta: a word-diff bal oldalán ≥ 20 086 ilyen mezőcsoport változott (Grep `^-(fej\|tagolatlan\|[IVX]+\|[^\t]*/)`). Ezt a jelentés nem számszerűsíti, pedig a lapok következő generálásakor ez jelenik meg. |
| CK4 sorszám-változás (E17) | OK | — | `git diff --numstat`: `bdb_forras_javitas.tsv` Δ +252 (bontás: 252 `res_dalet`; a jelentés 7. szakasza és a Grep is ennyit ad). `bdb_szakaszok.tsv` Δ 0, `bdb_szakasz_hu.tsv` Δ 0, `bdb_vers_jelentes.tsv` Δ 0. A `konkordancia/` alatt nincs változás. |
| CK5 ⛔ pontok | OK | brief | A briefben nincs ⛔ pont. A P3 feltételét és a „97% fölött” feltételt a DT-F185e váltja ki (egyeztetve). |
| A1 memória vs. lekérdezés | OK | `naplok/F185_jelentes.md` 5.4, 6–8 | A mért számok mellett ott a proveniencia-sor; az s103-N182 ítélete idézettel áll. |
| A2 nyitott tételek | ELTÉRÉS (mechanikus) | `nyitott/uj/f185-bdb-jelentespont-97.md:1` | Az N-F185a nyitottként szerepel, pedig a DT-F185b eldöntötte és a `belso_fejek` oszlop megvalósította. Az N-F185b, -c és -d valóban nyitott. |
| A3–A5 | nem alkalmazható | — | A diffben nincs párhuzam, PaRDeS-réteg vagy tanító. |
| A6 E12–E15 | OK | — | A CI-futásban mind a négy szabály 0 találatot adott. |
| a jelentés belső ellentmondásai | ELTÉRÉS (mechanikus) | `naplok/F185_jelentes.md:5-7, 261-262, 285` | Az „Állapot” sor szerint „a P2 nem indult … a seed-103 mintát nem húztam ki”, ami elavult. A 8. és a 9. szakasz szerint a „`BDB_MERT_PONTOSSAG` változatlan”, ezzel szemben a 10. szakasz és a `bdb_pontossag.toml` már 188-at ír. |
| SEMA 2.31 állapot | ELTÉRÉS (mechanikus) | `adat/SEMA.md` 2.31 „Állapot” | Még a `pe_mem` `javitva` 3 823 és `jelolt_marad` 556 értéket írja, és a `res_dalet` nem szerepel benne. A tényleges értékek 4 046 / 333, illetve 252 sor, ebből 118 `javitva` (Grep). |
| tesztek | NEM ELLENŐRIZHETŐ | — | A jelentés szerinti „104 OK” és a `teszt_bont`/`teszt_szotari_gerinc` futtatása a szerepemben nem megengedett. |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. **ALVIL-001 (tartalmi).** A forrásváltás a H7585 Zsolt 16:10 pontját `-/2/a`-ra teszi (`ketes`), ettől a lexikongenerátor GerincHiba miatt leáll.
2. **HAMART-001 és ANTROP-001 (tartalmi).** A `betu_javit` miatt a commitolt lapok elavultak. A lap újragenerálása tilos, ezért döntés kell.
3. **E32 (mechanikus).** DT-helyőrző áll a kód string-literáljában és a 2.29 fejlécében.
4. **E26 (mechanikus).** A CI végleges N-számnak veszi a mintaazonosítókat (s103-N135/s103-N182/s103-N200 …).
5. **A 2.29 jelentéspont-változásai (tartalmi).** A jelentés nem számszerűsíti őket (≥ 20 086 mezőcsoport).
6. **Rés/dálet-szabály (mechanikus).** A SEMA és a kód kétféleképpen írja le.
7. **A 2.31 reprodukálhatósága (mechanikus).** A fejlécből hiányzik a `--sefaria-cache`, és a `test_javitas_ellenoriz` valószínűleg bukik.
8. **SEMA 2.31 (mechanikus).** Az állapotszámok elavultak.
9. **N-F185a (mechanikus).** Nyitottként szerepel, pedig már megoldott.
10. **A jelentés belső ellentmondásai (mechanikus).** Az „Állapot” sor és a 8–9. szakasz elavult.
11. **Tanú- és proveniencia-formátum (mechanikus, enyhe).** A két osztály eltér egymástól és a SEMA-tól.
