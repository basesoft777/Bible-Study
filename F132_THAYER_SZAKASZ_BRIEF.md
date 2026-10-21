---
feladat: 132
cim: A Thayer jelölt szövegrétege, szeletelője és szakaszonkénti fordítása a görög gerincszavakra (pilot: G1941)
kod: THAYER_SZAKASZ
tipus: feladat
fazis: 2
munka: adat
modell: opus
allapot: nem_indult
ad: a Thayer szakaszonként, adatként (thayer_szakaszok.tsv) és igehelyenként jelentésponthoz kötve (thayer_vers_jelentes.tsv); a motívumok 13 görög gerincszava szakaszonként magyarul, szakasz-kapun átengedve — a #131 görög része erre épül
kovetkezo: "Te: a #128 eszközlánca után /kovetkezo; első lépés ⛔ M0 (DT-F132a–e: forrás, kulcs, a 14 kész sor sorsa, a fordítás modellje és lánca, a #131 viszonya)"
olvas: [konkordancia/lexikonok_nyers/Thayer.lexicon, konkordancia/lexikonok_nyers/README.md, konkordancia/Thayer_teljes.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/Karoli_1908.tsv, adat/licencek.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/elofordulasok.tsv, adat/SEMA.md, eszkozok/bdb_jelolt/, eszkozok/emeles.py, eszkozok/forditas_kapuk.py, "forditas/prompt_v*.md", F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md, F131_SZOTARI_GERINC_BRIEF.md, F07_THAYER_ELES_BRIEF.md, F27_FP3_BRIEF.md]
ir: [eszkozok/thayer_jelolt/, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/forditasok.tsv, adat/SEMA.md, naplok/F132_THAYER_SZAKASZ_naplo.md]
fugg: [128]
nem_fugg: [7, 27, 38, 67, 121, 123]
---

# F132_THAYER_SZAKASZ_BRIEF.md — A Thayer jelölt szövegrétege, szeletelője és szakaszonkénti fordítása

*FELADATOK #132 · Modell: opus · v1 · 2026.10.21*

## 1. Cél

A DT272 (DT-F121a) szerint a motívumblokk szótári gerince a BDB (héber) és a **Thayer (görög)**: a
motívumot hordozó szakaszok részletesen, magyarul, a szó jelentése és a hely motívumbeli funkciója két
rétegben. A BDB-re ehhez megvan a jelölt szövegréteg (`bdb_szakaszok.tsv`, #107), az igehely →
jelentéspont tábla (`bdb_vers_jelentes.tsv`, #99) és készül a szakaszonkénti fordítás (#128). **A
Thayerre egyik sincs.** A felhasználó kérése (2026-10-20, chat): „Már most meg kellene tervezni a thayer
forditását és a szeletelőt. Már szeletelővel jelenne meg athayer” — vagyis a #131 görög része már
szeletelt Thayerrel jelenjen meg.

A feladat három dolgot ad: (1) a Thayer jelölt szövegrétege szakaszonként, a teljes szótárra; (2) a
Thayer igehely-hivatkozásai jelentésponthoz kötve; (3) a motívumok 13 görög gerincszava szakaszonként
magyarul. A teljes Thayer fordítása **nem** része (az a #7, halasztva, D46).

## 2. Felmérés (2026-10-21, a brief írásakor; csak olvasva)

*(proveniencia: scope=konkordancia/lexikonok_nyers/Thayer.lexicon (SQLite, `Lexicon(Topic, Definition)`), adat/elofordulasok.tsv (`strong`), adat/forditasok.tsv | forras=eseti olvasó szkript (a brief írójának scratchpadjében) | ts=2026-10-21)*

- **Forrás.** A `Thayer.lexicon` SQLite, 5 427 sor (5 426 `G…` + 1 egyéb), a `Definition` HTML. A
  `Thayer_teljes.tsv` (5 426 sor) ugyanennek lapított szövege jelölők nélkül; a #28 ebből fordított.
- **Tagolás a forrásban.** Bekezdés (`<p>`) 17 093; jelentéspont-fej a bekezdés elején (`<p><b>1.</b>`,
  betű, római) 1 685 szócikkben; a többi szócikk tagolatlan (egy vagy néhány bekezdés).
- **Igehelyek a forrásban: gépileg jelölve.** `<ref onclick="bcv(könyv,fejezet,vers)">…</ref>`, összesen
  **63 953**: ÚSZ (40–66) 58 266, ÓSZ (1–39) 5 687. A BDB-vel szemben nem kell szövegből visszafejteni
  (`bdb_vers_jelentes.tsv` okkódjai, öröklött könyvnevek): az igehely egy attribútum.
- **Kulcsalak.** A `Topic` kitöltés nélküli (`G12`, `G1941`), az adatréteg `Strong_padded`-et használ
  (`G0012`). Normalizálás nélkül 4 gerincszó (G0012, G0086, G0282, G0813) **néma nem-találat** (a
  CLAUDE.md „Igehely-formátum” csapdájának Strong-megfelelője).
- **Licenc.** `adat/licencek.tsv` Thayer-sor: közkincs (a mű kora miatt; DT-F33g); a formázási réteg
  (Tim Morton / Bible Analyzer, Eliran Wong) a sor szerint engedéllyel. Hogy a HTML-szerkezet (fejek,
  `bcv`) kiadható-e adatként, az M0-ban a forrásmondattal (`konkordancia/lexikonok_nyers/README.md`
  Thayer-sora) rögzítendő — a BDB.lexicon tisztázatlan licence miatt csak azonosítót adott (DT225), ez
  itt eltérhet.
- **Magyarul ma:** 14 `teljes` Thayer-sor a `forditasok.tsv`-ben (#28), szakaszjelölő nélkül — ugyanaz a
  helyzet, mint a BDB-nél az utólagos illesztés (#107) előtt.
- **A 13 görög gerincszó** (az `elofordulasok.tsv` szerint): G0012 (1 141 kar.), G0086 (1 770), G0282
  (701), G0813 (341), G1311 (786), G1941 (3 745; 5 fej, 7 bekezdés, 43 `bcv`), G1944 (334), G2671 (803),
  G4151 (23 726; 15 fej, 497 `bcv`), G5010 (945), G5351 (1 393), G5356 (974), G5590 (5 949) — összesen
  ≈ 42 600 karakter HTML nélkül.

## 3. Hatókör

**Benne van:** a bontó a teljes Thayerre (determinisztikus, olcsó); az igehely → jelentéspont tábla a
teljes Thayerre; a 13 gerincszó szakaszonkénti fordítása; a SEMA új szakaszai; a mérés és a napló.

**Nincs benne:** a teljes Thayer fordítása (#7, D46); a lexikonlap renderje (#131); a szónézet
(olvasói szerver); a BDB-lánc (#128, #38) módosítása — a közös, szótárfüggetlen láncot ez a feladat a
#128 eredményére építi, de a #128 fájljait nem írja át, csak ha az M0 ⛔ ezt kifejezetten eldönti.

## 4. Lépések (⛔ a kötelező megállások)

### M0 — felmérés és ⛔ döntések (csak olvas)

A felmérés megismétlése a futás napján, majd helyőrzős döntések a felhasználó elé, opcióval és
javaslattal:

1. **DT-F132a — forrás:** (a) a `Thayer.lexicon` HTML-je (szerkezet + `bcv`), a szöveg is innen ·
   (b) a szerkezet és a `bcv` a lexikonból, a szöveg a `Thayer_teljes.tsv`-ből illesztéssel (a #107
   mintája) · (c) csak a TSV. Javaslat: (a), ha a licencmondat a formázási réteg adatkénti használatát
   megengedi; különben (b).
2. **DT-F132b — kulcs és séma:** `adat/thayer_szakaszok.tsv` (`strong` = `Strong_padded`, `sorszam`,
   `utvonal`, `jel`, `szoveg`, `forras`, `forras_hash`, `proveniencia`; a SEMA 2.30 mintájára) és
   `adat/thayer_vers_jelentes.tsv` (`strong`, `sorszam`, `konyv`, `fejezet`, `vers`, `karoli_vers`,
   `utvonal`, `proveniencia`; a SEMA 2.29 mintájára). A `G12` → `G0012` normalizálás helye (bontó,
   egyetlen függvény).
3. **DT-F132c — a 14 kész magyar Thayer-sor sorsa:** (a) a 13 gerincszó szakaszonként újrafordítva, a
   régi `teljes` sor archív `megjegyzes`-sel marad · (b) utólagos illesztés a `hu_illeszt.py` mintájára ·
   (c) mindkettő, összevetéssel. Javaslat: (a) — ≈ 42 600 karakter, olcsó, és megkerüli az utólagos
   illesztés elakadásait (a BDB-n 606 szakasz, N-F107b).
4. **DT-F132d — a fordítás modellje és lánca:** a #128 szakaszonkénti lánca (határtoken, prompt v5,
   szakasz-kapu) **szótárfüggetlenül**, Thayer-ággal (javaslat), vagy külön Thayer-lánc. Modell: Sonnet a
   DT-F38e mintájára, vagy Opus. A választást a #128 M0-ja (tárolási kulcs, `forras_hash`) befolyásolja,
   ezért ez a feladat a #128 után fut (`fugg: [128]`).
5. **DT-F132e — viszony a #131-hez:** (a) a #131 görög része erre vár (`fugg` + 132 a #131 fejlécében;
   a felhasználó jóváhagyásával, a befogadáskor vagy a #131 menetében) · (b) a #131 előbb csak a héber
   BDB-réteggel készül, a görög a #132 után kerül be (újragenerálás). Javaslat: (a), ha a #128 és a #132
   időben a #131 előtt elkészül; különben (b).

**⛔ M0:** a felhasználó dönt az 1–5. pontról. A döntésig nincs kódírás.

### M1 — bontó: `eszkozok/thayer_jelolt/bont.py`

A forrás bekezdései és fejei adatként (a `bdb_jelolt/bont.py` mintájára, de a Thayer jelölőire:
`<p>`, `<b>1.</b>`, betű- és római fej, `<b><i>…</i></b>` jelentés-címke). Determinisztikus, `--ts`,
`--ellenoriz`; a `# GENERÁLT:` és `# forras:` fejlécsor (a bemenet és a kód hash-e). Teszt
(`teszt_bont.py`): minden szócikk minden bekezdése pontosan egy sorban; a sorok szövegének
összefűzése a szócikk HTML nélküli szövegét adja; a G1941 aranymintája (5 fej, 7 bekezdés) kézzel
ellenőrizve a naplóban.

### M2 — igehely → jelentéspont: `eszkozok/thayer_jelolt/vers_jelentes.py`

Minden `bcv(k,f,v)` egy sor: a könyvszám → Károli-rövidítés a `Konyv_normalizalo_tabla.tsv`-n át, a
`karoli_vers` a `Karoli_1908.tsv` kulcsa szerint (üres, ha nincs: kitöltés nélkül), az `utvonal` a
hivatkozást tartalmazó szakaszé. ÚSZ-helyeken a számozás egyezik; az ÓSZ-hivatkozások (5 687, főleg
LXX-utalás) számozási eltérését a naplóban mérni, nem kitölteni. Teszt: a 63 953 `bcv` mind a táblában;
a G1941 a motívum 10 ÚSZ-helyéből melyiket idézi, és melyik jelentéspont alatt (a naplóba).

### M3 — a 13 gerincszó szakaszonkénti fordítása

A DT-F132c–d szerint, a terminológia aktuális verziójával és a fordítási elvekkel (nyelvközi egység,
rangsor: szójegyzék > Károli > BDB > szótár). Kapuk, köztük a szakasz-kapu (a tokenek száma és
sorrendje egyezik); bukás esetén önújrapróba, utána `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`.
Rögzítés a `forditasok.tsv`-be a DT-F132b/d szerinti kulccsal; írás előtt az eszköz a táblát összeveti
az eredetivel (csak új sor, a meglévők bájtra azonosak). `modell` = a saját környezetből vett tényleges
név. Commit adagonként.

### Mz — zárás

Mérés a naplóba (sorok, `bcv`-lefedés, a 13 szó kapueredménye, a G1941 motívumhelyeinek
jelentéspontja); `adat/SEMA.md` két új szakasza; `fuggetlen-ellenor` a base..head diffen; draft PR.
Push és merge csak a felhasználótól.

## 5. Elfogadási feltételek

1. A bontó és a vers-tábla determinisztikus (azonos bemenet és `--ts` → bájtra azonos kimenet), a
   `--ellenoriz` zöld, a tesztek zöldek.
2. Minden Thayer-szócikk minden bekezdése a `thayer_szakaszok.tsv`-ben; a 63 953 `bcv` a
   `thayer_vers_jelentes.tsv`-ben; a Strong-kulcs mindenhol `Strong_padded`.
3. A 13 gerincszó minden szakasza magyarul a `forditasok.tsv`-ben, a gátoló kapukon átment; a régi
   `teljes` sorok a DT-F132c szerint kezelve.
4. A TSV-ket `split('\t')` olvassa és `'\t'.join()` írja (a `csv` modul tilos, CLAUDE.md).
5. Lekérdezésből származó állítás mellett proveniencia-sor; hiány explicit, nem kitöltve.
6. `python eszkozok/ellenoriz.py` SÉRTÉS 0; `python eszkozok/feladatok.py ellenoriz` 0 hiba.

## 6. Döntésnapló

| Azonosító | Kérdés | Opciók | Javaslat |
|---|---|---|---|
| DT-F132a | A forrás (szöveg és szerkezet) | (a) Thayer.lexicon HTML · (b) szerkezet a lexikonból, szöveg a TSV-ből · (c) csak TSV | (a), ha a licenc engedi; különben (b) |
| DT-F132b | Kulcs, séma, a `G12` → `G0012` normalizálás | l. M0 2. | `Strong_padded`, a SEMA 2.29–2.30 mintájára |
| DT-F132c | A 14 kész `teljes` sor sorsa | (a) újrafordítás szakaszonként · (b) utólagos illesztés · (c) mindkettő | (a) |
| DT-F132d | A fordítás lánca és modellje | a #128 lánca szótárfüggetlenül / külön lánc; Sonnet / Opus | közös lánc; Sonnet (DT-F38e mintája) |
| DT-F132e | Viszony a #131-hez | (a) a #131 görög része vár · (b) a #131 héberrel indul, a görög később | (a), ha időben elkészül; különben (b) |
