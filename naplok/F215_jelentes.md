# F215 — az olvasó angol Thayer- és BDB-szövege a javított adatból

*Modell: claude-sonnet-5-5 · 2026-11-12 · alap: `origin/main` (F213, #720) · proveniencia: scope=thayer (5426 sor), thayer_forras_javitas (15 `javitva`), bdb (247 `hivatkozas`-Strong) | forras=pardes.db (epites_ts 2026-11-12T18:53:35Z), `eszkozok/bdb_jelolt/szakasz_bemenet.py` | ts=2026-11-12*

## 1. Thayer (angol): a beszúrás a lekérdezésben

`lekerdezesek.thayer` a `thayer_forras_javitas` `javitva` sorait alkalmazza a `thayer.teljes_szocikk`-re: a beszúrás helye az `elotte` (a lyuk előtti 20 karakter), amely mind a 15 Strongban **pontosan egyszer** áll a teljes szócikkben (mérve); ha nem így lenne, a függvény hibát dob, nem csúszik el némán.

**Miért a lekérdezésben, nem az `sqlite_epit.py`-ban?**
- A javítótábla már a DB-ben van (`thayer_forras_javitas`, 15 sor), nincs új adatfüggés.
- A DB-építés a manifest/frissességi kaput és az 1,1 GB-os WSL-másolatot érinti; a lekérdezés-javítás azonnal él, újraépítés nélkül, és a javítótábla frissítése is rögtön látszik.
- Ugyanez a minta a BDB futásidejű láncában (`blokkok._rovidites`), és a magyar ág is olvasáskor (`thayer_bemenet.javitott_szoveg`) alkalmazza ugyanazt az `elotte` + `javitott_alak` párt.
- Régi/teszt-DB-ben a tábla hiányzik: ott a nyers szöveg marad (`OperationalError`-ág).
- Ára: a nyers `thayer` tábla továbbra is nyers (lásd a 4. pontot).

**Mérés:** **15 Strong** angol szövege változott (G0260, G0575, G0846, G1100, G1909, G2675, G3536, G3563, G4151, G4404, G4405, G4406, G4407, G5132, G5567), összesen **+3291 karakter** (10–748 karakter/sor). A többi Thayer-szócikk azonos (a teszt az első 400-at ellenőrzi).

## 2. BDB (angol): a hivatkozás-javítás a DB szövegében már benne van — nincs teendő

A felmérés feltevése (a 412 `hivatkozas`-javítás az angol ágból hiányzik) **nem igaz**. A javítótábla indoka maga is ezt mondja: „a TSV utólagos hivatkozás-javítása (a nyers JSON-ban nincs)”: a `BDB_teljes_unabridged.tsv` (amelyből a `bdb.teljes_szocikk` jön) a javítást már hordozza; a *nyers JSON-szakaszok* (`bdb_szakaszok.tsv`) nem, ezért kell a javítótábla a magyar ághoz.

Mérés (mind a 247 Strongra):
- H0026: a DB-ben `Kt 1Sam 25:18` áll (a nyers JSON-szakaszban `2Sam`).
- A könyvrövidítések multihalmaza az angol szövegben a javított nézettel egyezik 246/247 Strongnál (a maradék H6981: tokenhatár-zaj, `22Chr` ← `2Chr`; a javított `Judg → 1Chr` ott is benne van); a nyers JSON-nézetével csak 29 Strongnál egyezik (ahol a csere a multihalmazt nem érinti).
- A javítótábla `k`-adik előfordulás-logikáját az angol szövegre engedve 247-ből 214 Strongnál hibát adna (a token-sorszámozás a szakaszösszefűzésre épül), a többinél pedig a már javított szöveget javítaná újra: ezért **nem alkalmaztam**. **0 Strong angol szövege változott.**
- A `teszt_angol_javitott.py` őrzi: H0026 és a 247-Strongos multihalmaz-összevetés.

A felmérés további pontjai (a `betu_javitasok` ~2,4% nem fedett alakja, az előfordulásonkénti pe/mem-ítélet) külön, nem sürgős tétel; ebben a feladatban nem érintettem.

## 3. Tesztek

`teszt_angol_javitott.py` (7 teszt, WSL-natív DB-vel: zöld): a beszúrás-függvény egységesetei; mind a 15 beszúrás a `thayer()` kimenetében van, a nyers szövegben nincs; a javított sorok a magyar ág bemenetével (`thayer_bemenet.szakaszok`) egyeznek; a nem javított Thayer-sorok változatlanok; H0026; a 247 Strong multihalmaz-összevetése.

## 4. Ki olvassa még a nyers `thayer`/`bdb` táblát vagy a nyers TSV-t?

| Fogyasztó | Mit olvas | Szándékos? |
|---|---|---|
| `olvaso_szerver/lekerdezesek.bdb_angol` | `bdb.teljes_szocikk` | igen: a szöveg már javított (2. pont); a pe/mem- és sorrendjavítást a megjelenítési lánc végzi |
| `olvaso_szerver/lekerdezesek.thayer` | `thayer` + `thayer_forras_javitas` | javított (ez a feladat) |
| `thayer_jelolt/*` (bont, forras_javit, thayer_bemenet) | `Thayer_teljes.tsv` | igen: ez a javítás *forrása*; a bemenet a javított szöveget adja a fordításnak |
| `lexikon_general.py` (:3021) | `Thayer_teljes.tsv` | **nem ellenőrzött**: az F212 területe; a lapon idézett angol Thayer-szöveg nyers lehet a 15 Strongon (N-F215a) |
| `fordit.py` (:62), `emeles.py` (:64, :135) | `Thayer_teljes.tsv`, `BDB_teljes_unabridged.tsv` | **nem ellenőrzött**: régi, egész-szócikkes fordítási út; a szakaszos (javított) út a `thayer_jelolt`/`szakasz_bemenet`; nem futtattam, nem döntöttem el, él-e még (N-F215a) |
| `istentiszt_2b_d1_toltes.py` | `Thayer_teljes.tsv` G0994 | igen: G0994 nincs a 15 között |
| `olvaso_pilot/*`, `olvaso_mockup/bdb_kinyer.py` | `thayer`/`bdb` tábla és TSV | igen: nem éles mérő/mockup szkriptek |
| `sqlite_epit.py` (:1570) | `bdb` (hosszmérés, 13. mérés) | igen: csak `length(teljes_szocikk)` |
| `ellenoriz.py`, `bdb_*` javító/mérő szkriptek | nyers TSV | igen: a nyers adat vizsgálata/javítása a feladatuk |

## Zárás

Az angol Thayer a javított szöveget adja (15 Strong, +3291 karakter); az angol BDB-nek nincs teendője (0 Strong változott, a javítás a TSV-ben már benne van), ezt teszt őrzi. A `lexikon_general.py`-hoz és az `sqlite_epit.py`-hoz nem nyúltam. Nyitott: N-F215a (a nem ellenőrzött fogyasztók). A CI-állapot és a PR a PR-leírásban.
