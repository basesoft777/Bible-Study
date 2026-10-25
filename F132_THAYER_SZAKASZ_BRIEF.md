---
feladat: 132
cim: A Thayer jelölt szövegrétege, szeletelője és szakaszonkénti fordítása a görög gerincszavakra (pilot: G1941)
kod: THAYER_SZAKASZ
tipus: feladat
fazis: 2
munka: adat
modell: opus
allapot: megallt
ag: claude/thayer-szakasz
ad: a Thayer szakaszonként, adatként (thayer_szakaszok.tsv) és igehelyenként jelentésponthoz kötve (thayer_vers_jelentes.tsv); a motívumok aktuális görög gerincszavainak szakaszonkénti fordításához a teljes lánc (betöltő, szólista, javítótábla, adatblokk, kapuk, prompt v5.1, sigla-javaslat); a fordítás maga (az újrafuttatható M3, DT-F132h) a külön Sonnet-feladat (DT-F132g (1), tervezet: beerkezo/Fnn_THAYER_M3_BRIEF.md) — a #131 görög része erre épül
kovetkezo: "Te: [elteres_kor 1/2] /elteres 132 — ELLENOR_F132_2 1. mechanikus, 2. mechanikus (besorolás egyeztetésre vár)"
olvas: [konkordancia/lexikonok_nyers/Thayer.lexicon, konkordancia/lexikonok_nyers/README.md, konkordancia/Thayer_teljes.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/Karoli_1908.tsv, adat/licencek.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/elofordulasok.tsv, adat/SEMA.md, adat/karoli_strong/, eszkozok/bdb_jelolt/, eszkozok/bdb_adatblokk.py, eszkozok/emeles.py, eszkozok/forditas_kapuk.py, "forditas/prompt_v*.md", F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md, F131_SZOTARI_GERINC_BRIEF.md, F07_THAYER_ELES_BRIEF.md, F27_FP3_BRIEF.md]
ir: [eszkozok/thayer_jelolt/, adat/elofordulasok.tsv, adat/datasetek.tsv, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/thayer_sigla.tsv, adat/thayer_forras_javitas.tsv, adat/SEMA.md, adat/tiltott_fordulatok.tsv, forditas/prompt_v5_1.md, beerkezo/Fnn_THAYER_M3_BRIEF.md, eszkozok/forditas_kapuk.py, eszkozok/teszt_forditas_kapuk.py, adat/bdb_szakasz_hu.tsv, naplok/F132_THAYER_SZAKASZ_naplo.md]
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

## 2a. Mankók (a felhasználó kérése, 2026-10-21: „lehet mankót épiteni hozzás mint a bdb hez?” — „igen”)

A fordítás minden adagja ezeket használja; nélkülük adag nem indul. Az 1–4. a #121 négy mankója
(`F121_GLOSSZA_FORDITAS_BRIEF.md` 2a) és a BDB adatblokkja (`eszkozok/bdb_adatblokk.py`, F56) a Thayerre
alkalmazva; az 5–6. csak a Thayernél kell.

1. **Terminológiai szójegyzék kapuval.** `adat/terminologia.tsv` (SEMA 2.15) a `kapu` oszloppal, a
   `forditas_kapuk.py` 5. kapuja; görög sorokkal bővül, az aktuális verzióval.
2. **Tiltott fordulatok.** `adat/tiltott_fordulatok.tsv` és a `14_tiltott` kapu — a #121-ben tervezve,
   **a repóban még nincs megépítve**. Közös a BDB- és a Thayer-láncnak; hogy melyik feladat építi, az M0
   6. pontja (DT-F132f).
3. **Károli-alakok az adatblokkban.** Strongonként a #22 párosításának (`adat/karoli_strong/parok_*.tsv`)
   Károli-alakjai gyakorisággal és proveniencia-sorral, egy `eszkozok/thayer_jelolt/` adatblokk-függvényből
   (a `bdb_adatblokk.py` csak olvasott). **Ismert hiány (2026-10-21):** a párosítás 22 ÚSZ-könyvet fed; a
   **Máté, Márk, Lukács, János és az ApCsel nincs benne** — a G1941 10 motívumhelyéből 4 az ApCsel-ben van.
   A hiány a blokkban és a naplóban explicit, nem pótoljuk (CLAUDE.md 3. szabály); a lefedettséget az M0
   méri.
4. **Igehely-idézet Károli-szövegben.** A `bcv(k,f,v)` gépi, ezért szakaszonként minden idézett vers
   Károli-szövege az adatblokkba kerül (`konkordancia/Karoli_1908.tsv`, a könyvnév a
   `Konyv_normalizalo_tabla.tsv` szerint); a magyarítás ehhez igazodik. A BDB-nél ehhez szövegből kellett
   feloldani a hivatkozást (`bdb_vers_jelentes.tsv`); itt nem.
5. **Sigla- és rövidítéstábla (új: `adat/thayer_sigla.tsv`).** A Thayer apparátusa: kiadás-siglák
   (`G T Tr WH`, `Rec.`, `L`, `Lachmann`), grammatikák (`Winers Grammar`, `Buttmann`), antik szerzők
   (`Xenophon`, `Plato`), rövidítések (`Sept.`, `cf.`). Soronként: forrásalak, mi ez, a magyar kiadásban
   változatlan-e vagy milyen egységes alakot kap, proveniencia. A gyűjtés a forrásból gépi (M1 mellékterméke),
   a besorolás kézi; egy kapu ellenőrzi, hogy a fordítás a táblát követi. A tábla a #129 (BDB-kiadás)
   rövidítésjegyzékének is mintája.
6. **Nyelvközi híd.** A Thayer kiírja a héber megfelelőt (pl. G1941: „the Sept. very often for קָרָא”,
   `ref0` jelöléssel). Az adatblokk ebből a héber szó magyar BDB-jelentését és terminológiai sorát is hozza
   (`forditasok.tsv`, `bdb_szakasz_hu.tsv`), hogy a görög és a héber azonos magyar szót kapjon (a nyelvközi
   egység elve; rangsor: szójegyzék > Károli > BDB > szótár). Ütközésnél soronként kézi ítélet.

## 3. Hatókör

**Benne van:** a bontó a teljes Thayerre (determinisztikus, olcsó); az igehely → jelentéspont tábla a
teljes Thayerre; ~~a 13 gerincszó szakaszonkénti fordítása~~ az M3 előfeltételei (a fordítás lánca, l. M3); a SEMA új
szakaszai; a mérés és a napló.

**Nincs benne:** **az M3 fordítása** (DT-F132g (1), felhasználó, 2026-10-25: külön brief `modell: sonnet`, `fugg: [132]`;
tervezet: `beerkezo/Fnn_THAYER_M3_BRIEF.md`, a befogadás `/befogad`-dal, a felhasználó jóváhagyásával); a teljes Thayer fordítása (#7, D46); a lexikonlap renderje (#131); a szónézet
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
5. **DT282 — viszony a #131-hez: ELDÖNTVE** (felhasználó, 2026-10-21: „már az arany lexikonban is
   szeletelővel akarom látni a görög cikkeket”): (a), a #131 görög része erre vár; a #131 fejléce a
   befogadásban `fugg: [127, 110, 132]` (`DONTESEK.md` DT282). Nem kérdezendő újra.
6. **DT-F132f — a tiltott-fordulat tábla (2a/2) helye:** (a) a #128 építi, a közös lánc részeként ·
   (b) ez a feladat építi (akkor az `ir` a menetben bővül: `adat/tiltott_fordulatok.tsv`,
   `eszkozok/forditas_kapuk.py`) · (c) a #121 terve szerint marad. Javaslat: (a), mert a BDB- és a
   Thayer-lánc közös kapuja.
7. **A mankók felmérése:** a 2a/3 Károli-lefedettsége a 13 gerincszó idézett és motívumhelyein (hány vers
   esik a hiányzó evangéliumokra és az ApCsel-re); a 2a/5 siglák előzetes listája a forrásból (darabszám).

**⛔ M0:** a felhasználó dönt az 1–4. és a 6. pontról. A döntésig nincs kódírás.

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

### M3 — a motívumok aktuális görög gerincszavainak szakaszonkénti fordítása (újrafuttatható, DT-F132h)

*Szándékos címsor-törlés (TÖRLÉS-SZÁNDÉKOS, ELLENOR_F132 1. tétel): a korábbi „### M3 — a 13 gerincszó szakaszonkénti
fordítása” címsor e címsorra cserélődött. Ok: DT-F132h (1), a hatókör nem a rögzített 13 szó, hanem a motívumok aktuális görög
gerincszavai; DT-F132g (1), az M3 külön Sonnet-briefbe került (`beerkezo/Fnn_THAYER_M3_BRIEF.md`). A CI E5 a jelölést a
commit-üzenet sor eleji `TÖRLÉS-SZÁNDÉKOS:` mezőjéből olvassa (`eszkozok/ellenorzes/szabalyok.py` `SZANDEKOS_JELOLES_MINTA`); az
F132.18 commit hordozza.*

**Kikerült e feladat hatóköréből (DT-F132g (1), felhasználó, 2026-10-25).** Az M3 a saját, `modell: sonnet` briefjén fut; a
tervezet: `beerkezo/Fnn_THAYER_M3_BRIEF.md` (a parancssor a napló „M3 indítása” szakaszából; előfeltétel: a sigla-javaslatok
felhasználói jóváhagyása, DT-F132j (3)). E feladat az M3 előfeltételeit adja (F132.4–F132.13); az alábbi leírás a tervezet alapja.

**Hatókör (DT-F132h (1), felhasználó, 2026-10-25):** nem a 2. szakasz rögzített 13 szava, hanem **a motívumok aktuális görög gerincszavai, a futás pillanatában**: az `adat/elofordulasok.tsv` `strong` mezőjének görög Strongjai (`Strong_padded`-re normalizálva). Kimarad, aminek már van érvényes (nem `elavult`, `forras_hash`-egyező) szakaszos fordítása; a többit a Sonnet-lánc adagonként fordítja. A listát minden futás elején az `eszkozok/thayer_jelolt/` listázó eszköze állítja elő (a kihagyottak okkal, proveniencia-sorral); az első futás a mai halmaz. Az M3 újrafuttatható: új motívum görög szava a következő futásban kerül sorra.

A DT-F132c–d szerint, a 2a mankóival (adatblokk: Károli-alakok, idézett versek Károli-szövege, sigla-tábla,
nyelvközi híd; kapuk: terminológia, tiltott fordulatok, sigla), a terminológia aktuális verziójával és a
fordítási elvekkel (nyelvközi egység, rangsor: szójegyzék > Károli > BDB > szótár). Kapuk, köztük a szakasz-kapu (a tokenek száma és
sorrendje egyezik); bukás esetén önújrapróba, utána `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`.
Rögzítés a `forditasok.tsv`-be a DT-F132b/d szerinti kulccsal; a régi `teljes` sorok jelölése (DT-F132c (i)+(ii)) az adott futásban fordított szavakra; írás előtt az eszköz a táblát összeveti
az eredetivel (csak új sor, a meglévők bájtra azonosak). `modell` = a saját környezetből vett tényleges
név. Commit adagonként.

### Mz — zárás

Mérés a naplóba (sorok, `bcv`-lefedés, ~~a 13 szó kapueredménye~~ az M3-lánc próbája fordítás nélkül (DT-F132g (1)), a G1941
motívumhelyeinek jelentéspontja); `adat/SEMA.md` új szakaszai; `fuggetlen-ellenor` a base..head diffen; PR és merge csak a
felhasználótól.

## 5. Elfogadási feltételek

1. A bontó és a vers-tábla determinisztikus (azonos bemenet és `--ts` → bájtra azonos kimenet), a
   `--ellenoriz` zöld, a tesztek zöldek.
2. Minden Thayer-szócikk minden bekezdése a `thayer_szakaszok.tsv`-ben; a 63 953 `bcv` a
   `thayer_vers_jelentes.tsv`-ben; a Strong-kulcs mindenhol `Strong_padded`.
3. *(DT-F132g (1) szerint módosítva)* Az M3 előfeltételei tesztelten megvannak: a futás listája (DT-F132h), a javított
   forrásnézet (DT-F132i (2)), az adatblokk, a kapuk (`14_szakasz`, `15_tiltott`, `16_sigla`), a prompt v5.1 (DT-F132k (2)), a
   sigla-javaslat jóváhagyásra (DT-F132j (3)), és az M3 brief-tervezete a `beerkezo/`-ban. A gerincszavak magyar szakaszai (az
   eredeti 3. feltétel) a külön M3-feladat elfogadási feltétele.
4. A TSV-ket `split('\t')` olvassa és `'\t'.join()` írja (a `csv` modul tilos, CLAUDE.md).
5. Lekérdezésből származó állítás mellett proveniencia-sor; hiány explicit, nem kitöltve.
6. `python eszkozok/ellenoriz.py` SÉRTÉS 0; `python eszkozok/feladatok.py ellenoriz` 0 hiba.

## 6. Döntésnapló

| Azonosító | Kérdés | Opciók | Javaslat |
|---|---|---|---|
| DT-F132a | A forrás (szöveg és szerkezet) | (a) Thayer.lexicon HTML · (b) szerkezet a lexikonból, szöveg a TSV-ből · (c) csak TSV | **eldöntve: (b)** (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132b | Kulcs, séma, a `G12` → `G0012` normalizálás | l. M0 2. | **eldöntve: (1)+(2)+(3)+(4)** (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132c | A 14 kész `teljes` sor sorsa | (a) újrafordítás szakaszonként · (b) utólagos illesztés · (c) mindkettő | **eldöntve: (a)+(i)+(ii)** (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132d | A fordítás lánca és modellje | a #128 lánca szótárfüggetlenül / külön lánc; Sonnet / Opus | **eldöntve: (1)+(S); az M3 külön Sonnet-menetben** (felhasználó, 2026-10-25; `DONTESEK.md`; az indítás: DT-F132g) |
| DT282 | Viszony a #131-hez | (a) a #131 görög része vár · (b) a #131 héberrel indul, a görög később | **eldöntve: (a)** (felhasználó, 2026-10-21; `DONTESEK.md`) |
| DT-F132h | Az M3 hatóköre | (1) újrafuttatható M3 az `elofordulasok.tsv` aktuális görög halmazán · (2) bővített rögzített lista · (3) teljes Thayer | **eldöntve: (1)** (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132g | Az M3 Sonnet-menetének indítása | (1) külön M3-brief `modell: sonnet` · (2) lépésszintű modell-mező · (3) a `modell` átváltása · (4) subagent nélküli session | **eldöntve: (1)**, tervezet `beerkezo/Fnn_THAYER_M3_BRIEF.md` (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132i | A `Thayer_teljes.tsv` szövegvesztése (15 Strong, köztük G4151) | (1) marad · (2) javítótábla · (3) a 15 Strong szövege a lexikonból | **eldöntve: (2)**, `adat/thayer_forras_javitas.tsv` (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132j | A sigla-tábla kézi besorolása | (1) az M3 előtt, a futás szavaira · (2) utólag · (3) gépi javaslat jóváhagyásra | **eldöntve: (3)**, gépi javaslat, jóváhagyás a felhasználóé (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132k | A prompt v5 Thayer-ága | (1) változatlan · (2) új `prompt_v5_1.md` · (3) a v5 helyben | **eldöntve: (2)**, `forditas/prompt_v5_1.md` (felhasználó, 2026-10-25; `DONTESEK.md`) |
| DT-F132f | A tiltott-fordulat tábla (2a/2) helye | (a) a #128 · (b) ez a feladat · (c) a #121 terve szerint | **eldöntve: (b), kapu `15_tiltott`** (felhasználó, 2026-10-25; `DONTESEK.md`) |

**Egyeztetett eltérések (felhasználó, 2026-10-25, chat: „mehet, g(1), i(2), j(3), k(2)” — a kérdés: „… és a két eltérés elfogadva?”):**
(1) az `adat/thayer_vers_jelentes.tsv` a DT-F132b (2) nyolc oszlopán túl egy kilencedik oszlopot hordoz, a `szakasz`-t (a hivatkozást
tartalmazó bekezdés sorszáma, SEMA 2.35); (2) az `adat/bdb_szakasz_hu.tsv` fejlécsorának hash-e újragenerálódott (a `forditas_kapuk.py`
változása miatt; adatsor nem változott), ezért az `ir` mezőben áll. Napló: „Döntések (2026-10-25, második kör)”.
