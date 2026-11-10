---
feladat: 185
cim: A BDB-hozzárendelés (vers → jelentéspont) pontossága 97% fölé, új vak méréssel igazolva
kod: BDB_JELENTESPONT_97
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: lezarva
ag: claude/f185-bdb-jelentespont-97
pr: https://github.com/basesoft777/Bible-Study/pull/681
ad: a vers → BDB-jelentéspont hozzárendelés a vak mérésen ≥ 97% (seed-103, előre rögzített kapu), gépi bizonyossági jelöléssel; teljesülés esetén a „próba” jelölés lekerül, a szó-lapon az új mért szám CI-vel
kovetkezo: "merge (a felhasználóé). Utána: #187 kártyája a táblára épül; #182 2. fázis: BDB_BETU_JAVIT bekapcsolása a lapokon, biztos/ketes bontás; N-F185b/c/d"
lezarva_osszegzes: "BDB vers → jelentéspont: a forrás a szakasztábla (DT-F185a), sorbelső fejekkel sorvágás nélkül (29 311 fordításkulcs bájtra azonos); seed-103 valóban vak mérés 188/200 = 94,0% (Wilson 89,8–96,5), a ≥ 194 kapu NEM teljesült, P3 elmaradt (DT-F185e); biztos 180/181, ketes 8/19; BDB_MERT_PONTOSSAG 188/200, a dobozban nem jelenik meg (DT-F185h); P4: pe/mem 223 + rés/dálet 118 javítás TAHOT/OSHB és Sefaria-tanúval; betu_javit a generátorban kikapcsolva (DT-F185f); ALVIL H7585 kézi pont (DT-F185g); HAMART-001 egy pontja újragenerálva (H2403, N99, DT-F185i); egy javítókör; nyitott: N-F185b,c,d"
olvas: [eszkozok/olvaso_szerver/, tematikus_lezart/HAMART-001*, tematikus_lezart/naplok/HAMART-001*, eszkozok/bdb_jelolt/, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv, naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv, naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv, naplok/BDB_SZELETELO_M2_seed101_iteletek.md, naplok/BDB_SZELETELO_M2_seed102_iteletek.md, naplok/ELLENOR_F102_2.md, F102_BDB_SZELETELO_JAVITAS_BRIEF.md]
ir: [eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, eszkozok/olvaso_szerver/m2_minta_osszevet.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/bdb_jelolt/bont.py, eszkozok/bdb_jelolt/teszt_bont.py, adat/bdb_szakaszok.tsv, adat/bdb_vers_jelentes.tsv, adat/bdb_forras_javitas.tsv, adat/bdb_aranyminta.tsv, adat/SEMA.md, naplok/BDB_SZELETELO_M2_minta_seed103_kulcs.tsv, naplok/BDB_SZELETELO_M2_minta_seed103_vak.tsv, naplok/BDB_SZELETELO_M2_seed103_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed103_kitoltott_B.tsv, naplok/BDB_SZELETELO_M2_seed103_iteletek.md, naplok/F185_jelentes.md, naplok/ELLENOR_F185.md, adat/bdb_szakasz_hu.tsv, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/bdb_vj_szabaly.py, eszkozok/bdb_jelolt/forras_javit.py, eszkozok/bdb_jelolt/belso_tanu.py, eszkozok/bdb_rovidites.py, eszkozok/lexikon_general.py, lexikon/HAMART-001_TUDOMANYOS.md, eszkozok/olvaso_szerver/konfig/bdb_pontossag.toml, eszkozok/olvaso_szerver/konfig/elemek.toml, eszkozok/teszt_szotari_gerinc.py, naplok/F185_minta103.py, naplok/F185_seed103_osszevet.py, naplok/F185_seed103_kitoltoi_utasitas.md, naplok/F185_vaksag_proba.py, naplok/BDB_SZELETELO_M2_minta_seed103_szocikkek.txt, dontesek/uj/f185-bdb-jelentespont-97.md, nyitott/uj/f185-bdb-jelentespont-97.md]
fugg: [105]
nem_fugg: [138]
---

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
