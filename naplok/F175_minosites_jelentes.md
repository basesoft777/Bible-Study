# F175 — a két nyílt Károli-csomag minősítése: a mért pontosság, nem a modell-egyezés (2026-11-14)

*Végrehajtó: claude-opus-5-5. Döntés: DT858 (a felhasználó), DT859 (a végrehajtó, megerősítésre vár). Nyitva: N-F175d.*

## 1. Mi változott

- A `bizonyossag` oszlop kimaradt a `nyilt_karoli_strong/parok/*.tsv`, `szavak/*.tsv`, a `nyilt_karoli_modern/konyvek/*.tsv`
  táblákból és a két kódkönyvből. A belső `adat/karoli_strong/` változatlan.
- Kimaradt minden kétmodelles leírás és a „költségkeret” mondat a MODSZER/METHODS, OLVASSEL/README, ISMERT_HIBAK/KNOWN_ISSUES
  szövegekből, a közlemény-tervezetekből és a data paper kéziratából (`kozlemeny/data_paper/karoli_strong_kezirat_hu/en.md`).
  Az ismert hibák 7. pontja (Bizonyosság) kikerült, a 8. pont 7. lett.
- A minősítés egyetlen helyről jön: a #172 mérése (`f172/meres_eredmeny.tsv`, `naplok/KAROLI_PONTOSSAG_jelentes.md`).
- Gépi védelem: a két kapu NYILVANOS pontja tiltja a modell-egyezést mint minősítést (`MODELL_EGYEZES`: bizonyosság,
  kétmodelles leírás, költségkeret, a második párosító modell neve); a TELJESSEG pont a `bizonyossag` oszlopot (fejléc-egyezés).
- N-F175b: a névelő-szabály közös modulba került (`eszkozok/nevelo.py`); a modernizált csomag TSV-fejléce „a Logosz-lexikon”
  (nem „a(z)”), a magyar szövegei a szám előtti névelőt a kiejtés szerint kapják, a kapuja NEVELO pontot kapott. Javítva a
  szabály hibája is: a tagolás nélküli négyjegyű szám („1908”, kiejtve „ezer…”) „az”-t kap (3k+1 hosszú, 1-gyel kezdődő
  vezető csoport).
- N-F175c: a két csomag CITATION.cff-je a motívum-adatmagot a saját címével hivatkozza („Logosz-lexikon — nyílt adatmag:
  bibliai motívumok / Logosz Lexikon — open data core: biblical motifs”).
- Az olvasó szó-lapja („Károli-alakok és pontosság” blokk): az „ebből M magas bizonyosságú” helyett „A párosítás mért
  pontossága 95%.”, a szám egyetlen forrása `eszkozok/olvaso_szerver/konfig/karoli_pontossag.toml` (proveniencia-sorral;
  a teszt a #172 mérőtáblájával veti össze).

## 2. A módszer mondatának mérése (3. pont)

*scope=adat/karoli_strong/parok_*.tsv, a `forras` × `bizonyossag` megoszlás | forras=adat/karoli_strong/parok_*.tsv @ 37f087cc | ts=2026-11-15*

| forras | bizonyossag | pár |
|---|---|---|
| S | alacsony | 545 871 |
| S+C | magas | 52 844 |
| C | — | **0** |

A közölt 598 715 pár mindegyikét az első modell (Claude Sonnet) javasolta; csak a második modelltől származó pár nincs.
Ezért a mondat: „A szópárosítást nyelvi modell (Claude Sonnet) javasolta …”.

## 3. A rétegek könyvcsoportként (4. pont)

*forras=f172/meres_eredmeny.tsv, f172/reteg_osszevont.tsv (eszkozok/karoli_strong/reteg_osszevonas.py)*

A két Mózes-réteg együtt **Mózes öt könyve**, nem csak az 1–2.: az `OSZ_mozes_magas` az 1–2Móz egyező párjai (52 844), az
`OSZ_mozes` a Mózes-könyvek minden más párja (69 690, ebből 66 434 a 3–5Mózesben). Az összevonás a két részminta pársúlyos
rétegzett becslése (a #172 `retegzett` képlete), új mérés nincs.

| réteg | n | helyes | arány | 95% |
|---|---|---|---|---|
| Mózes öt könyve | 400 | 382 | 95,02% | 92,80–97,24 |
| történeti könyvek | 200 | 190 | 95,00% | 91,04–97,26 |
| költői könyvek | 200 | 190 | 95,00% | 91,04–97,26 |
| próféták | 200 | 186 | 93,00% | 88,59–95,78 |
| evangéliumok és ApCsel | 200 | 196 | 98,00% | 94,97–99,22 |
| levelek | 200 | 191 | 95,50% | 91,67–97,61 |
| Jelenések | 200 | 193 | 96,50% | 92,95–98,29 |
| **összes, súlyozott** | 1 600 | 1 528 | **95,06%** | 93,81–96,32 |

A rétegek tartománya most 93,00–98,00% (korábban, a két Mózes-réteggel, 92,0–99,0%). A független összevetés változatlan:
98,72% (98,22–99,08).

## 4. A tartalmi azonosító változása

| csomag | régi `kiadas_azonosito` | új `kiadas_azonosito` |
|---|---|---|
| `nyilt_karoli_strong/` | 2026-11-01-3bb84301cff7e591 | 2026-11-01-944c082d1796920e |
| `nyilt_karoli_modern/` | 2026-11-12-69f8503b7cf00dbf | 2026-11-12-e78f08aa5a627fde |

Az új tartalmi hash (SHA-256): `944c082d1796920e25487adfc73401d5ac3d7acad3760e418e961076c26a4ff4` (szóillesztés),
`e78f08aa5a627fded24660e81a9510a4c5efaafca821173dd01394d12341b5cb` (modernizált). Az adatállapot dátuma nem változott (a
belső adat változatlan). A Zenodo-piszkozatokba az új csomag kerül.

## 5. Kapuk és tesztek

- `karoli_strong_kapu.py` (teljes, UJRA-val): **0 BUKÁS**, 0 FIGYELEM (TELJESSEG 66 mérési sor, OSSZEG 146 fájl, UJRA bájtazonos
  151 fájl, KEZIRAT, VALTOZATLAN).
- `karoli_modern_kapu.py` (teljes): **0 BUKÁS**, 0 FIGYELEM (új NEVELO pont: OK; OSSZEG 79 fájl; UJRA bájtazonos 84 fájl).
- `reteg_osszevonas.py --ellenoriz`: az `f172/reteg_osszevont.tsv` a mérőtáblákból számolt.
- `teszt_karoli_strong_export.py` 24 teszt OK (új: modell-egyezés tiltása, `bizonyossag` oszlop, névelő 1908/12345);
  `teszt_karoli_modern_export.py` 15 teszt OK.
- Olvasó (`teszt_futtat.py`): `teszt_olvaso_szerver` 112 OK (új: `test_karoli_pontossag_egy_forrasbol`),
  `teszt_pilot_aranymintaval` 22 OK, `teszt_tervezo` 51 OK, a többi gyors fájl zöld. A `teszt_visszhang_kapu` 2 hibája a
  tiszta main-en is megvan (ismert, régi bukás, külön tétel), nem ez az ág okozza.

## 6. Kiegészítés (2026-11-15): a „bizonyosság” jelentése (DT860)

A felhasználó döntése: a nyilvános „bizonyosság” csak a mért pontosság (könyvcsoportonként, 93–98%, összesen 95,06%). A
DT859 („Mózes öt könyve”) jóváhagyva. Ebben a PR-ban, újragenerálás nélkül (a csomagok szövegében a szó nem áll): a SEMA 2.20 rögzíti, hogy a `bizonyossag` mező belső szűrő, nem minősítés. Nyitva: N-F175d (az
olvasó három helye, külön SERVER-javítás), N-F175e (a motívum-mag szövegei, a „csak szövegek” mód után; teljes export
nélkül az E35 miatt nem igazolható; a „magas/alacsony bizonyosság” kaputilalom is ekkor, a mag szövegével együtt kerül
be). Ellenőrzés ebben a körben a felhasználó kérésére szűkítve: a két csomagkapu és a `feladatok.py ellenoriz`; a teljes
`push_elott.py` egyszeri kivételként nem futott, a teljes ellenőrzést a CI végzi.
