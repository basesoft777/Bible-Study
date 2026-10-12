---
feladat: 79
cim: SQLite-építő — a pardes.db a SEMA szerint, integritási tesztekkel (az olvasói konkordancia adatbázisa)
kod: SQLITE_EPIT
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: lezarva
ag: claude/f79-sqlite-epit
ad: eszkozok/sqlite_epit.py — az adat/ és a konkordancia/ kanonikus tábláiból determinisztikusan épített, nem commitolt pardes.db (SEMA-típusok, KK-alapú vers-kulcs, normalizált igehely és Strong, licenc_allapot és kereskedelmi minden táblán, strong_parok és frázis-pozíció előszámolva, FTS a motivumok/ fölött); a SEMA 3. integritási szabályai az ellenoriz.py függvényein át futnak, sértésnél megáll; mért méret és lekérdezés-próba a 26 pontból az 1–6., 13–15. pontra
kovetkezo: "merge a felhasználótól; nyitott: N-F79a, N-F79b, N-F79c (NYITOTT_FELADATOK.md)"
olvas: [adat/SEMA.md, adat/, konkordancia/Karoli_1908.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/BSB_Strongs.tsv, konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, motivumok/, tematikus_lezart/, genezis/, ujszovetseg/, eszkozok/strong_util.py, eszkozok/ellenoriz.py, eszkozok/gate.py, MUNKATERV.md, ADATVAGYON_TERV.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, .gitignore]
fugg: [62]
nem_fugg: [38, 52]
pr: 300
lezarva_osszegzes: pardes.db építő kész (eszkozok/sqlite_epit.py, 37 teszt zöld; teljes építés 63 tábla, 845 MB, a licenc_* oszlopok 250 MB; kis minta próbája 9/9; javító kör: Karoli_Strong_kivonat, KJV_Strongs_teljes, TBESG/H, morf_* licenc, TAGNT-jelentés, táblánkénti méret); zárás: naplok/F79_zaras.md, mérés: naplok/SQLITE_EPIT_meres.md; draft PR #300
---

# F79_SQLITE_EPIT_BRIEF.md — SQLite-építő (pardes.db)

*FELADATOK #79 · Modell: sonnet · v1 · 2026.10.12 · a csonk-briefet váltja fel · döntés: DT77 (12), DT-M1 · forrás: `MUNKATERV.md` 4. szakasz (SQLITE_EPIT sor), `ADATVAGYON_TERV.md` 7., 19., 21. (3. lépcső), 22.4*

## 1. Cél

Egyetlen, újraépíthető SQLite-fájl (`pardes.db`), amely a repó kanonikus adatát (`adat/*.tsv`)
és a szükséges konkordancia-táblákat egy lekérdezhető helyre teszi. Erre épül a #76 olvasói
konkordanciája (#25a), és ebből mérhető a #86 csomagmérete (N-F86b). A `pardes.db` **generált
nézet**, nem adat: nem commitolt, kézzel nem írható, és nem ír vissza semmit (DT28; ADATVAGYON 21.,
2. szabály). Ami számítás, az építéskor fut Pythonban; a lekérdező csak kész táblákat olvas
(ADATVAGYON 7.).

## 2. Hatókör

**Benne van**

- `eszkozok/sqlite_epit.py`: a SEMA 2. szakaszának táblái a SEMA 1. szakasz típusaival
  (`IGEHELY`, `STRONG`, `PROVENIENCIA`, `IGAZOLAS` külön mező); TSV-olvasás `split('\t')`-vel, a
  `#` kezdetű fejléc-megjegyzéssorok (pl. `adat/karoli_strong/*`) átugrásával.
- **Igehely-normalizálás:** a STEPBible-alakú datasetek (`Karoli_kereszthivatkozasok.tsv`,
  `Karoli_Strong_kivonat.tsv`, `TIPNR_kivonat.tsv`) a `Konyv_normalizalo_tabla.tsv`-n át; a
  nem normalizálható sor **nem némán esik ki**, hanem a jelentésbe kerül (CLAUDE.md: normalizálás
  nélkül néma nem-találat).
- **Vers-kulcs:** KK-alapú (Károli-vers); a TAHOT `Igehely`-kulcsa az F85.6 óta maga a Károli-vers
  (CLAUDE.md „Adat-tár”); a `szamozas` jelző értékkészlete a `BSB_Strongs.tsv` 7. oszlopáé
  (`mt` | `ellenorizetlen` | `kjv`), kiegészítve az N46 44 eltolódás-gyanús versével
  (ADATVAGYON 22.1; N17, N46, N-F41a/d).
- **Strong:** egyetlen normalizáló, az `eszkozok/strong_util.py` `strong_normalizal()`-ja (#62);
  saját normalizáló nem készül.
- **Licenc:** `licenc_allapot` és `kereskedelmi` oszlop minden táblán, az `adat/licencek.tsv`
  (SEMA 2.19) és az `adat/datasetek.tsv` (2.6) alapján; a CC BY-SA-származék (SDBH/SDGNT,
  Louw–Nida) jelölve (ADATVAGYON 22.4).
- **Előszámolt táblák:** token-tábla pozícióval (`vers, sorszam, strong, karoli_szo`) az
  `adat/karoli_strong/parok_*.tsv`-ből (az 5. pont frázis-keresése); `strong_parok(a, b, n)`
  a `grammatikai_strongok.tsv` szűrővel (a 23. pont); FTS5 a `motivumok/*.md` fölött (16. pont).
- **Átmeneti FTS a régi tanulmányokra (DT109 (5), a felhasználó iránya, 2026.10.12):** amíg a
  #11 nem migrálta őket, a régi tanulmányok prózája (`tematikus_lezart/`, `genezis/`,
  `ujszovetseg/`) is az FTS-indexbe kerül, soronként `regi_forras` jelöléssel (a találat
  megmondja, hogy nem egyforrású, migrált szöveg). Egy motívum régi tanulmánya kiesik az
  indexből, amint a `motivumok/[ID].md` migrált forrása megvan (a két szöveg nem kereshető
  egyszerre). Csak olvasás: az index nem ír vissza, és nem kinyerés — adat a régi prózából
  továbbra is csak a `jeloltek.tsv`-n át, döntéssel kerül az adatrétegbe (DT28).
- **Integritás:** a SEMA 3. szakasz szabályai **az `eszkozok/ellenoriz.py` meglévő
  `szabaly1…8` függvényein át** futnak a betöltött adaton (egy szabály, egy implementáció);
  sértésnél az építés nem ír kész fájlt, és nem nulla kóddal lép ki.
- `.gitignore`: `pardes.db` (és az ideiglenes építési fájl).
- Kimenetek: `naplok/SQLITE_EPIT_integritas.md` (szabályonkénti eredmény), `naplok/SQLITE_EPIT_meres.md`
  (táblánkénti sorszám, fájlméret, építési idő, a lekérdezés-próba eredménye, proveniencia-sorral).

**Nincs benne**

- írás az `adat/`-ba vagy bármely forrásfájlba (a #79 csak olvas);
- olvasói felület, HTML, hosting (#76; a hosting ⛔ ott van);
- MCP-burok (feltételes, DT-M7; előbb a #61);
- a freemium/prémium mezőszintű szint-tábla (#86 3.1) és a közös szint-szűrő (N-F23b) — a #79
  csak a licenc-oszlopokat adja, amelyekre ezek épülnek;
- az ÚSZ Károli–Strong (nincs még ilyen adat; a görög oldal a TAGNT-kivonatból jön, a Károli-szóalak
  nélkül — jelölve, nem pótolva).

## 3. Lépések

- **M0 — felmérés (csak olvas).** Táblaleltár: mely `adat/*.tsv` és `konkordancia/*.tsv` kerül
  be, soronként a kulcs alakja (magyar vagy STEPBible igehely), a sorszám, a licencsor. A
  normalizálhatóság próbája a három STEPBible-datasetre (hány sor nem képezhető le). A
  `ellenoriz.py` szabályfüggvényeinek bemenete: TSV-sorlisták — ellenőrizni, hogy az építő
  ugyanazt a bemenetet adja-e. Séma-terv táblánként (oszlop, típus, index). ⛔ **A séma-terv és a
  nyitott pontok a felhasználónak (DT109):** (1) a vers-kulcs a KK (Károli-vers) — megerősítés;
  (2) a `kereskedelmi` oszlop forrása és értékkészlete (a `licencek.tsv` meglévő mezője vagy
  levezetett érték); (3) az integritás-ellenőrzés a betöltés előtt (TSV-n) vagy után (az
  adatbázisból visszaolvasva) fut — javaslat: előtte, a meglévő függvényekkel; (4) mely
  konkordancia-táblák kerülnek a kis mintába; (5) az átmeneti FTS a régi tanulmányokra
  (irány eldöntve: igen, `regi_forras` jelöléssel): a fájlkör pontos listája (a generált
  `lexikon/` és a `naplok/` nem), és a kiesés szabálya (motívumonként, a migrált forrás
  megjelenésekor).
- **M1 — építő, kis mintán.** A 8 lexikonoldalas motívum és az 1Mózes (ADATVAGYON 21., 3. szabály).
  Determinisztikus: kétszeri építés azonos tartalmat ad (táblánkénti rendezett tartalom-hash; a
  fájl bájtazonossága nem követelmény). Commit tételenként (`F79.1:` …).
- **M2 — tesztek** (`eszkozok/teszt_sqlite_epit.py`): pozitív (a mai adat zöld); negatív
  (szándékosan rontott ideiglenes másolaton minden SEMA 3. szabály sértése megállítja az építést);
  normalizálás (egy STEPBible-alakú sor a magyar kulcson érhető el; a nem leképezhető sor a
  jelentésben); `split('\t')`-körút: a `kapcsolodas` idézőjelei megmaradnak (CLAUDE.md, 79 mező).
- **M3 — lekérdezés-próba a kis mintán.** A 26 pontból az 1–6. és a 13–15. pont egy-egy SQL-je;
  a várt eredmény a tanulmányok és lexikonoldalak ismert tényeiből (pl. a 4. pont: H8414 + H0922 →
  1Móz 1:2, Jer 4:23, Ézs 34:11), a forrással megnevezve. Üres eredmény elfogadható, ha az adat
  üres — jelölve, nem pótolva (CLAUDE.md 3. szabály). ⛔ **A próba eredménye a felhasználónak,
  a teljes építés előtt.**
- **M4 — teljes építés.** A teljes ÓSZ Károli–Strong (az összes `parok_*`), minden `adat/` tábla;
  méret, idő és táblánkénti sorszám a `naplok/SQLITE_EPIT_meres.md`-be (a #86 N-F86b és a #76
  hosting ⛔ bemenete).
- **Zárás.** `fuggetlen-ellenor` (a diff és a G-pontok); `python eszkozok/feladatok.py ellenoriz`
  0; fejléc `lezarva`, `lezarva_osszegzes`; draft PR.

## 4. Elfogadási feltételek

- **G1** A `pardes.db` nincs a repóban (`.gitignore`), és a #79 diffje nem érint `adat/`,
  `konkordancia/`, `motivumok/`, `lexikon/` fájlt.
- **G2** Az építés determinisztikus: két egymás utáni futás táblánkénti tartalom-hash-e azonos.
- **G3** Minden TSV-olvasás `split('\t')`; a `csv` modul nem szerepel az építőben.
- **G4** A SEMA 3. szabályainak bármelyik sértése megállítja az építést (negatív teszt
  szabályonként), és a szabályok kódja az `ellenoriz.py`-ból jön, nem másolat.
- **G5** Nincs néma nem-találat: minden STEPBible-alakú sor vagy normalizálva bekerül, vagy név
  szerint a jelentésben áll; a darabszám a mérésben.
- **G6** Minden tábla `licenc_allapot` és `kereskedelmi` oszlopa kitöltött; ismeretlen licenc
  nem kap alapértéket, hanem a tábla nem épül be, és a jelentésben áll.
- **G7** A lekérdezés-próba (1–6., 13–15.) minden pontja a forrással megnevezett várt eredményt
  adja, vagy az eltérés indokolva a mérésben.
- **G8** A mért fájlméret és építési idő a `naplok/SQLITE_EPIT_meres.md`-ben, proveniencia-sorral.

## 5. Döntésnapló

| Tétel | Kérdés | Javaslat | Állapot |
|---|---|---|---|
| D1 | Az integritás egy implementációban | az `ellenoriz.py` függvényei, nem új kód | javaslat (M0 ⛔-nél megerősítve) |
| D2 | A `pardes.db` helye | helyben, `.gitignore`; a #76 dönti el a terjesztését | rögzítve (MUNKATERV 4.) |
| D3 | Az FTS a régi tanulmányokra is, átmenetileg | igen, `regi_forras` jelöléssel, a #11 migrációjáig; a fájlkör és a kiesés szabálya: DT109 (5) | a felhasználó iránya (2026.10.12) |
| DT109 | Az M0 öt nyitott pontja (vers-kulcs, `kereskedelmi` forrása, az integritás ideje, a kis minta táblái, az átmeneti FTS fájlköre és kiesési szabálya) | M0 ⛔; az (5) iránya eldöntve: a régi tanulmányok a #11-ig `regi_forras` jelöléssel kereshetők (felhasználó, 2026.10.12), hogy a #76 indulástól kereshető legyen | eldöntve (mind a nyolc pont a javaslat szerint, a felhasználó, 2026.10.12; az (5)-nél a `melyelemzesek/` és a kézi naplók is bekerültek) |
