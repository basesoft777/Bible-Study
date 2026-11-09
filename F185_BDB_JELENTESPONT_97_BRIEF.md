# Brief-tervezet — A BDB-hozzárendelés pontossága 97% fölé (BDB_JELENTESPONT_97)

*Orkesztrátori tervezet, 2026-11-09, a felhasználó jóváhagyásával („mehet”). Befogadásra (`/befogad`, külön sessionben). Cél: a vers → BDB-alpont (jelentéspont) hozzárendelés a vak mérésen ≥ 97% legyen, hogy a régi lapok teljes folyamatában ne kelljen laponkénti kézi BDB-ellenőrzés, és a „próba” jelölés lekerülhessen.*

**Javasolt fejléc [javaslat]:** `tipus: feladat`, `fazis: folyamat`, `modell: opus`, `munka: folyamat`, `fugg: [104, 105]` (a BDB-lánc után; közös fájlok), `olvas`/`ir`: a befogadó vezesse le (fő fájlok: `eszkozok/olvaso_szerver/bdb_szelet.py`, a szakasztábla előállítója (`bont.py`), `adat/bdb_szakaszok.tsv`, `adat/bdb_vers_jelentes.tsv`, `adat/bdb_forras_javitas.tsv`, `adat/bdb_aranyminta.tsv`, `eszkozok/olvaso_szerver/m2_minta_osszevet.py`, `eszkozok/olvaso_szerver/blokkok.py` (BDB_MERT_PONTOSSAG), `adat/SEMA.md`, `naplok/F<nn>_jelentes.md`).

## Kiindulás (mért, #102/#103, 2026-11-09)
- Seed-102 vak mérés, véletlen 200: könyv/vers 199/200; **jelentéspont: szeletelő 183/200 (91,5%, CI 86,7–95,0), szakasztábla 184/200**; ítélet után tájékoztató: szeletelő 184/199, tábla 187/199. Mérce: 97%. A #103 óta a csoporthatár az aranymintán 164/184.
- Ismert hibaosztályok: **N103** (a korábbi N-F102e) — a szakasztábla fejfelismerése (pl. „see 1 above” hamis fej; a H2403 HAMART-eset), a szeletelő 10 nem javult hibájából 6-ot a tábla már helyesen ad; **N106** (N-F102h) — törzsfejléc (pl. „Hiph`il A.”, név nélküli első Qal); könyvnév nélküli hely („but 13:10”), közbeékelt nem létező fejezet; forráshibák (a digitalizálásé, ~1–2/200).
- Döntések: DT-F102d/(ii) (a szeletelő marad, átállás a táblára a fejfelismerés javítása után), DT-F102g.

## Tételek
- **P0** — modell-ellenőrzés; a #104–#105 a main-ben; a seed-101/102 kulcsok és ítéletek beolvasása.
- **P1 — szabályjavítás osztályonként** (determinisztikus): N103 (fejfelismerés a `bont.py`-ban), N106 (törzsfejléc), könyvnév nélküli hely feloldása (a szócikkben utoljára megnevezett könyv), közbeékelt fejezet; minden osztály tesztje a seed-101/102 eseteivel. Utána **döntés a forrásról** (tábla vagy szeletelő) a DT-F102d szabálya szerint, szóráson túli különbséggel.
- **P2 — bizonytalansági jelölés:** a hozzárendelés mellé gépi bizonyosság (`biztos` / `ketes`, a szabály mondja meg, mikor kétes: több jelölt szakasz, hiányzó fej, tartomány-határ).
- **P3 — modelles döntés a kétes esetekre, két kézzel** (csak ha a P1 után a mérés 97% alatt): a modell a BDB-szócikk és a vers alapján választ alpontot, egy másik modell ellenőriz (aki dönt, nem ellenőriz); az eredmény provenienciával (`modell`, `ellenorzes`) az adatban; ellenőrizetlen sor nem renderel (a visszhang-tábla mintájára). Költségbecslés előtte, az orkesztrátor jóváhagyásával.
- **P4 — forráshibák:** a digitalizálás hibái a `bdb_forras_javitas.tsv`-be, tételesen (nem algoritmus).
- **P5 — új vak mérés** (seed-103, friss minta, két független kitöltő, a seed-101/102 eljárásával, a kapu előre rögzítve: nyers szám, ≥ 97%); ha teljesül, a „próba” jelölés lekerül, a szó-lapra az új mért szám CI-vel.
- **P6 — jelentés, független ellenőr, draft PR.** A lapokat nem generálja újra (motívumonként, a teljes folyamatban).

## Nem része
A BDB magyar fordítása (#38), a megjelenítés (#104), a lapgenerátor.
