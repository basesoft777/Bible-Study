# SZOTARI_GERINC_zaras.md — F131 zárójelentés

*Proveniencia: scope=F131 (`F131_SZOTARI_GERINC_BRIEF.md`, ág `ccr-6dc5ac47-lksrko`, F131.0–F131.34; PR #497) | forras=`gh pr view 497` (MERGED 2026-10-28T19:51:32Z, merge-commit `7e102a73`), `DONTESEK.md` (DT371–DT385 sorai), `naplok/F131_SZOTARI_GERINC_naplo.md` 6., 7., 10.5, `NYITOTT_FELADATOK.md` | ts=2026-11-02 | modell: claude-opus-5-5 (a zárás; a végrehajtás modelljét a napló rögzíti)*

A zárás oka: a munka a PR #497-tel 2026-10-28-án bekerült a main-be, de a brief fejléce `megallt` maradt, ezért a Feed (#156) az ISTENTISZT-001-en függő munkának mutatta. A zárás csak a fejlécet, ezt a jelentést és az át nem vezetett N-tételeket írja. Lexikont, adatot és kódot nem változtat.

## Mit hozott a #497

- **Szótári gerinc az arany lapon** (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`, „2. Szótári háttér”). A H7121 és a H8034 a BDB, a G1941 a Thayer tagolásában áll, magyarul. A motívumot hordozó szakaszok kibontva, a többi összecsukva; a görög szónál UBS-doménsor áll. A kapcsoló a `lexikon_general.py` `SZOTARI_GERINC_MOTIVUMOK`; a leírás a `RENDER_BRIEF.md`-ben és a `sablonok/6_PaRDeS_lexikon_oldal_sablon.md`-ben van.
- **Két réteg az előfordulás-táblában.** A „Jelentés (a szó)” és a „Funkció (a motívumban)” két oszlop, a címke forrása az ⓘ-ben áll. A címkéket az `adat/szotar_szakasz_cimke.tsv` tartja (SEMA 2.40).
- **Lekerült a lapról** a tW, a TBESH, a teljes UBS és a Mounce; a helyükön a szónézet-mutató áll. A tW forrásmegjelölése a DT383 szerint az Irodalomban és a kolofonban maradt.
- **Forrásjavítások:**
  - `adat/bdb_forras_javitas.tsv`: kézi `hivatkozas_kezi` sor, H8034 1Móz 26:35 → 26:25 (DT381 (a)).
  - `bdb_szelet.py`: a tartomány utáni folytatás (DT382 (A)).
  - `thayer_jelolt/vers_jelentes.py`: a `</ref>` utáni jelöletlen folytatás (DT384 (A)).
  - A ≥2 tokenes BDB-példa nem ad címkét (DT385 (a)).
  - Az ÓSZ-sorok UBS-jelentése a DBH-ból (DT380 (a)).
- **Ellenőrzés:**
  - Négy független ellenőri kör (`naplok/ELLENOR_SZOTARI_GERINC.md`, `_2`, `_3`, `_4`); a 4. kör után nem maradt ELTÉRÉS.
  - A merge előtt az `ellenoriz.py` 15 RENDBEN / 0 SÉRTÉS volt, a CI kilépési kódja 0 (napló 10.5).
  - A 7 többi lap diffje üres volt (napló 7.).

## A ⛔ pontok

| Pont | Döntés | Állapot |
|---|---|---|
| 0.3 — DT371–DT375, DT376 | a felhasználó, 2026-10-26 („elfogadta az összes javaslatot”) | 🟢 alkalmazva (F131.0.6–F131.4) |
| 3.1 — DT377, elfogadási próba | 1. kör: javítással újra (a felhasználó, 2026-10-28); 2. kör: elfogadva (az orkesztrátor a felhasználó felhatalmazásával, a felhasználó megerősítésével) | 🟢 |
| 4. — DT378, az éles lap felülírása | felülír (ugyanígy) | 🟢 lefutott (F131.4) |
| Az ellenőri körök döntései: DT379–DT385 | — | mind 🟢 |

A `DONTESEK.md`-ben nincs nyitott (🟡) #131-tétel. A DT190 🟡 (a BDB-tagolás közös kulcsa) a #9/#107 tétele; a brief szerint nyitva marad, és a #131 megoldása mindkét fő opciójával összefér.

Az ismert maradék hiányként van jelölve a lapon (DT377):
- a H8034 1Móz 12:8 fejsora (BDB-kiemelés 17/18);
- 46 `(fordításra vár)` (#121);
- a Jóel 2:32 DBH-hiánya (#146).

## Mi maradt N-tételként

**A brief 6. szakaszából.** Ezeket a #497 nem vezette át, a zárás most felvette őket a `NYITOTT_FELADATOK.md`-be:

| Jel | Tárgy | Kié |
|---|---|---|
| N-F131c | Thayer-tagolás, a G1941 görög előfordulásainak Thayer-hozzárendelése (DT373 (b)) | kutatói döntés |
| N-F131d | a #121 M1 mintája: az arany lap már nem minta a glosszafordításra | #121 |
| N-F131e | a szónézet ága (DT272 (1), (e)) | olvasó-szerver |
| N-F131h (a briefben `N-F131f`) | a szakaszbontás mértéke („nagyobb bontást szeretnék majd”) | felhasználói döntés |
| N-F131i (a briefben `N-F131g`) | a gerinc vizuális elkülönítése („formázással jobban elkülönülőt”) | felhasználói döntés |

A brief `N-F131f` és `N-F131g` jele ütközött a 2026-10-29-i utómunka azonos jelű, más tartalmú tételeivel. Ezért kapott itt a két tétel `h` és `i` jelet; a brief 6. szakasza rögzíti a megfeleltetést.

A zárás nem mérte újra, hogy a c, e és i tételt a későbbi munka (#142/#153 Thayer, #134 olvasó, DT425/DT427 olvasói forma) részben lefedte-e. Ezt az átvevő feladat dönti el.

**Számot már kapott.** Az N62 és az N63 a DT406-tal lezárult (2026-10-29).

**Az arany lap utómunkájából, „F131” jellel.** Ezek nem a brief hatókörei, és már a `NYITOTT_FELADATOK.md`-ben vannak:
- N-F131f: a `bdb_szakasz_hu.tsv` elavult;
- N-F131g: csoporthatár-illesztés;
- N-F131u: elutasítási okok;
- N-F131v: görög glossza-tábla;
- N-F131w: héber kiejtések;
- N-F131y: alkalmazva, DT445;
- N77: a BDB-fordítás elavulás-jele, döntésre vár.

A brief lezárása ezektől nem függ.
