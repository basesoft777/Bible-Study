# F56 M0 — Felmérés (csak olvas) · BDB_ADATBLOKK

*2026.10.06 · ág: `claude/bdb-adatblokk` · a lekérdezések: `eszkozok/bdb_adatblokk.py` függvényei és a `forditas_kapuk.ellenoriz_fejezetszam`; proveniencia: `scope=manual | forras=a lent megnevezett fájlok | ts=2026-10-06`.*

## 1. Források, oszlopok, Strong-alak

| Forrás | Oszlopok | Strong-alak | Megjegyzés |
|---|---|---|---|
| `adat/karoli_strong/parok_<könyv>.tsv` | `vers`, `hu_sorszam`, `hu_szo`, `er_sorszam`, `er_szo`, `strong`, `bizonyossag`, `forras` | `H2617` (kitöltetlen) | modell-kimenet, javaslat; 1. sor `#` proveniencia |
| `konkordancia/Karoli_1908.tsv` | `Igehely`, `Károli-szöveg (teljes vers)` | — | igehely: `1Móz 1:1` |
| `konkordancia/TAHOT_kivonat.tsv` | `Igehely`, `Strong-szám`, `Ragozott alak`, … | `H7225`, `H9003` (kitöltetlen, homográf-betű nincs) | igehely magyar alak |
| `adat/kulso/lxx_bridge.tsv` | `hebrew_strong`, `greek_strong`, `count` | `H0001`, `G3962` (kitöltött) | |
| `konkordancia/Strong_szotar.tsv` | `Strong-szám`, `Szótő`, `Kiejtés`, `Szófaj`, `Gyök/Származtatás`, `Jelentés` | `H0001` (kitöltött) | **nincs TWOT-oszlopa** (l. 4. pont) |
| `konkordancia/OSHL_lexikalis_index.tsv` | `strong`, `strong_eredeti`, `twot`, `bdb_id`, `nyelv`, … | `H0001` (kitöltött) | a TWOT-szám forrása; CC BY 4.0 |
| `adat/lexikon_hivatkozasok.tsv` | `strong`, `szotar`, `entry_id`, `jelentes_szam`, `szoveg_en`, `forrasfajl` | `H7121` (kitöltetlen) | 24 sor; a magyar szöveg a `forditasok.tsv`-ben |
| `konkordancia/BDB_teljes_unabridged.tsv` | `Strong_padded`, `Strong_eredeti`, `Teljes_szocikk` | `H0001`, homográf: `H0090a` | |

**Normalizálás.** Egyetlen belső kulcs: `strong_norm` (`H2617` / `H02617` / `2617` / `h2617` → `H2617`), a számkulcsú táblák (`TAHOT`, `parok`, `lxx_bridge`, `OSHL`) a számot (`strong_szam`), a kitöltött kulcsúak a 4 jegyre kitöltött alakot (`strong_padded`) használják. A homográf-betű (`H0090a`) a számkulcsú táblákban nem számít. A teszt (`teszt_bdb_adatblokk.py`, `test_nincs_nema_nemtalalat`) három ismert Strong-számon (H2617, H5785, H8057) mindhárom alakban ellenőrzi, hogy van Károli-pár, és a blokk nem ad `[NINCS KÁROLI-ALAK]`-ot (K2).

**Eltérés a briefhez (forrás-fájl).** A brief `olvas`-listája a rokon szavak TWOT-csoportját a `Strong_szotar.tsv`-ből várja; abban nincs TWOT-adat. A TWOT-szám az `OSHL_lexikalis_index.tsv`-ben (és a `SECE_H_teljes.tsv` szövegében) van; a blokk az OSHL-indexet használja (a „TWOT-szám hivatkozás”, a TWOT szövege nem kerül a repóba — OSHL README), a lemmát és jelentést a `Strong_szotar.tsv`-ből veszi. A felhasználó 2026-10-06-án jóváhagyta (DT-F56b): az `OSHL_lexikalis_index.tsv` bekerült a brief `olvas`-mezőjébe és az `adat/datasetek.tsv`-be (`lexikon_oldal` sor).

## 2. Lefedettség

- **Károli–Strong párok kész könyvei:** 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs (`parok_*.tsv`: 137 557 pár-sor, ebből 52 844 `magas` és 84 713 `alacsony`; az 1–2. könyvben két modell, a 3Móz–Józs csak `alacsony`, egy modell). A blokk a lefedett könyveket minden Károli-szakaszban kiírja, és jelzi, hogy az arányok csak ezekre érvényesek.
- **A 6. adag első 50 szócikke** (`BDB_FORDITAS_sorrend.tsv`, 407–456): **48/50-nél** ad a blokk legalább egy Károli-alakot. A két kivétel: **H0426** (arámi, 0 pár) és **H0256** (0 pár, nincs LXX-híd sem) — ezekre a blokk `[NINCS KÁROLI-ALAK]`-ot ad, az előfordulás-számmal együtt (a lefedett könyvekben a TAHOT-ban n előfordulás, 0 Károli-pár). A mintasorok pár-száma szócikkenként 1–95 (pl. H4438: 1 pár, H6098: 1 pár: a példa- és gyakoriság-adat itt vékony).
- **LXX-híd:** az 50-ből 3 szócikknek nincs sora a `lxx_bridge.tsv`-ben (H0123, H0256, H0567): a blokk 3. szakasza ezekre „—”.

## 3. Fejezetszám-hibák (13. kapu)

Mérés: `forditas_kapuk.ellenoriz_fejezetszam` az `adat/forditasok.tsv` minden `BDB`/`teljes` során (`allapot` `sonnet`/`opus`/`kezi`), és külön a forrásszövegen az M2 algoritmus (`bdb_adatblokk.forras_hibas_hivatkozasok`).

- **A fordításokban:** 49 szócikk, **79 különböző hely** jelzett (6 egyértelmű jelöltre javítva, 73 `jelolt_marad`; a 2026-10-06-i felhasználói döntés előtt 18 / 61, l. 4. pont 5.); az 1–5. adagban 47 szócikk, a maradék kettő (H7843, H8034) a korábbi opus/kézi sor, nincs az adagrendben. A kapu által nem látott, könyvnév nélküli láncolt hivatkozások (pl. `1Sám 3:22; 5:26`) kívül esnek.
- **A forrásban (az egész BDB-n):** 93 hely, 9 `javitva`, 84 `jelolt_marad` (a felhasználói döntés előtt 21 / 72) (`adat/bdb_igehely_javitas.tsv`).
- Az alábbi lista a fordításokban jelzett összes hely, az M2 tábla szerinti állapottal. A fordításban és a táblában egyező helyek száma: 79/79 (minden jelzett helyet a tábla lefed).

| adag | strong | a fordításban | a forrásban | állapot | javított |
|---|---|---|---|---|---|
| 1 | H0413 | `5Móz 37:36` | `Deut 37:36` | jelolt_marad | — |
| 1 | H0834 | `Ruth 8:12` | `Ruth 8:12` | jelolt_marad | — |
| 1 | H0834 | `Ruth 8:14` | `Ruth 8:14` | jelolt_marad | — |
| 1 | H0834 | `Ruth 9:1` | `Ruth 9:1` | jelolt_marad | — |
| 1 | H3605 | `1Krón 119:21` | `1Chron 119:21` | jelolt_marad | — |
| 1 | H3605 | `1Krón 145:9` | `1Chron 145:9` | jelolt_marad | — |
| 1 | H9005 | `Hab 41:47` | `Hab 41:47` | jelolt_marad | — |
| 1 | H9005 | `Jóel 9:9` | `Joel 9:9` | jelolt_marad | — |
| 1 | H9009 | `1Kir 45:14` | `1Ki 45:14` | jelolt_marad | — |
| 1 | H9009 | `1Kir 45:16` | `1Ki 45:16` | jelolt_marad | — |
| 1 | H9009 | `1Kir 59:15` | `1Ki 59:15` | jelolt_marad | — |
| 1 | H9009 | `1Kir 61:7` | `1Ki 61:7` | jelolt_marad | — |
| 1 | H9009 | `1Kir 66:6` | `1Ki 66:6` | javitva | `1Kir 6:6` |
| 2 | H0001 | `1Kir 50:1` | `1Ki 50:1` | jelolt_marad | — |
| 2 | H0001 | `1Kir 50:5` | `1Ki 50:5` | jelolt_marad | — |
| 2 | H0001 | `Eszt 11:32` | `Esth 11:32` | jelolt_marad | — |
| 2 | H0854 | `Ján 30:1` | `John 30:1` | jelolt_marad | — |
| 2 | H0854 | `Ján 54:15` | `John 54:15` | jelolt_marad | — |
| 2 | H0854 | `Jón 11:27` | `Jon 11:27` | jelolt_marad | — |
| 2 | H1732 | `2Sám 132:113` | `2Sam 132:113` | jelolt_marad | — |
| 2 | H1931 | `1Krón 93:2` | `1Chron 93:2` | jelolt_marad | — |
| 2 | H1931 | `1Krón 94:2` | `1Chron 94:2` | jelolt_marad | — |
| 2 | H1931 | `2Kir 33:23` | `2Ki 33:23` | jelolt_marad | — |
| 2 | H1931 | `Hós 19:21` | `Hos 19:21` | jelolt_marad | — |
| 2 | H1931 | `Hós 22:9` | `Hos 22:9` | jelolt_marad | — |
| 2 | H1931 | `Hós 24:12` | `Hos 24:12` | jelolt_marad | — |
| 2 | H1931 | `JSir 6:10` | `Lam 6:10` | jelolt_marad | — |
| 2 | H1961 | `1Kir 23:25` | `1Ki 23:25` | jelolt_marad | — |
| 2 | H3117 | `Dán 40:4` | `Dan 40:4` | jelolt_marad | — |
| 2 | H3318 | `Jer 58:8` | `Jer 58:8` | jelolt_marad | — |
| 2 | H3478 | `1Kir 24:10` | `1Ki 24:10` | jelolt_marad | — |
| 2 | H3478 | `1Kir 24:7` | `1Ki 24:7` | jelolt_marad | — |
| 2 | H3588 | `1Kir 32:29` | `1Ki 32:29` | jelolt_marad | — |
| 2 | H3588 | `1Kir 47:18` | `1Ki 47:18` | jelolt_marad | — |
| 2 | H3808 | `2Sám 26:1` | `2Sam 26:1` | jelolt_marad | — |
| 2 | H4428 | `Préd 15:26` | `Eccl 15:26` | jelolt_marad | — |
| 2 | H4480 | `1Kir 32:47` | `1Ki 32:47` | javitva | `1Kir 22:47` |
| 2 | H5973 | `2Sám 26:16` | `2Sam 26:16` | jelolt_marad | — |
| 2 | H6440 | `2Kir 36:12` | `2Ki 36:12` | jelolt_marad | — |
| 2 | H6440 | `Zak 17:3` | `Zech 17:3` | jelolt_marad | — |
| 2 | H6440 | `Zak 17:5` | `Zech 17:5` | jelolt_marad | — |
| 2 | H7200 | `1Sám 32:31` | `1Sam 32:31` | jelolt_marad | — |
| 2 | H7200 | `1Sám 46:30` | `1Sam 46:30` | jelolt_marad | — |
| 2 | H7200 | `1Sám 48:11` | `1Sam 48:11` | jelolt_marad | — |
| 2 | H7725 | `2Sám 26:23` | `2Sam 26:23` | jelolt_marad | — |
| 2 | H9004 | `Dán 23:22` | `Dan 23:22` | jelolt_marad | — |
| 3 | H0251 | `Jóel 7:10` | `Joel 7:10` | jelolt_marad | — |
| 3 | H0398 | `3Móz 28:17` | `Lev 28:17` | jelolt_marad | — |
| 3 | H1870 | `Én 34:2` | `Songs 34:2` | jelolt_marad | — |
| 3 | H2063 | `Eszt 25:12` | `Esth 25:12` | jelolt_marad | — |
| 3 | H4100 | `Bír 33:15` | `Judg 33:15` | jelolt_marad | — |
| 3 | H4196 | `Bír 22:28` | `Judg 22:28` | jelolt_marad | — |
| 3 | H4672 | `Préd 25:8` | `Eccl 25:8` | jelolt_marad | — |
| 3 | H5002 | `Jer 57:57` | `Jer 57:57` | javitva | `Jer 51:57` |
| 3 | H5650 | `Jón 14:25` | `Jonah 14:25` | jelolt_marad | — |
| 3 | H5975 | `2Kir 31:2` | `2Ki 31:2` | jelolt_marad | — |
| 3 | H7760 | `3Móz 40:15` | `Lev 40:15` | jelolt_marad | — |
| 3 | H7760 | `5Móz 45:7` | `Deut 45:7` | jelolt_marad | — |
| 3 | H8478 | `Dán 18:4` | `Dan 18:4` | jelolt_marad | — |
| 3 | H8478 | `Dán 21:15` | `Dan 21:15` | jelolt_marad | — |
| 3 | H8478 | `Dán 24:2` | `Dan 24:2` | jelolt_marad | — |
| 4 | H0595 | `1Móz 81:48` | `Gen 81:48` | jelolt_marad | — |
| 4 | H3881 | `1Krón 34:9` | `1Chron 34:9` | jelolt_marad | — |
| 4 | H4421 | `Bír 22:35` | `Judg 22:35` | jelolt_marad | — |
| 4 | H4427 | `2Kir 33:34` | `2Ki 33:34` | javitva | `2Kir 23:34` |
| 4 | H5046 | `1Kir 29:41` | `1Ki 29:41` | javitva | `1Kir 2:41` |
| 4 | H6240 | `Náh 5:14` | `Nah 5:14` | jelolt_marad | — |
| 5 | H0539 | `Józs 25:16` | `Josh 25:16` | jelolt_marad | — |
| 5 | H1157 | `JSir 9:10` | `Lam 9:10` | jelolt_marad | — |
| 5 | H4908 | `2Móz 46:6` | `Ex 46:6` | jelolt_marad | — |
| 5 | H5158 | `1Kir 23:6` | `1Ki 23:6` | jelolt_marad | — |
| 5 | H6437 | `Náh 47:3` | `Nah 47:3` | jelolt_marad | — |
| 5 | H7223 | `Préd 17:10` | `Eccl 17:10` | javitva | `Préd 7:10` |
| 5 | H7676 | `3Móz 28:8` | `Lev 28:8` | jelolt_marad | — |
| nem a sorrendben (korábbi opus/kézi) | H7843 | `Péld 57:1` | `Prov 57:1` | jelolt_marad | — |
| nem a sorrendben (korábbi opus/kézi) | H7843 | `Péld 58:1` | `Prov 58:1` | jelolt_marad | — |
| nem a sorrendben (korábbi opus/kézi) | H7843 | `Péld 59:1` | `Prov 59:1` | jelolt_marad | — |
| nem a sorrendben (korábbi opus/kézi) | H8034 | `Dán 22:14` | `Dan 22:14` | jelolt_marad | — |
| nem a sorrendben (korábbi opus/kézi) | H8034 | `Dán 22:19` | `Dan 22:19` | jelolt_marad | — |

## 4. Az M2 algoritmus és a küszöb

1. Hibás hivatkozás: a szócikk szövegében `Könyv fej:vers` (a 11. kapu forrás-oldali könyv-leképezésével), ahol a fejezet > a könyv fejezetszáma (`forditas_kapuk.FEJEZETSZAM`, az ÓSZ-ben a Károli/MT nagyobbika).
2. A Strong-szám előfordulásai (`TAHOT_kivonat.tsv` ∪ `parok_*.tsv`, a homográf-betű nélkül) → verslista.
3. Jelöltek: a fejezetszám egy számjegyének elhagyása / betoldása (0–9) / cseréje; a jelölt a könyvben létező fejezet (1..max), és `könyv jelölt:vers` a verslistában van.
4. Pontosan egy jelölt **és nincs FIGYELEM-jelzés** (5. pont) → `javitva`; különben `jelolt_marad`. **Küszöb:** csak a fejezetszám módosul (a versszám nem), csak egy számjegyes eltérés, és csak egy jelölt; több jelöltnél és jelölt nélkül nincs javítás.
5. **Könyvnév-hiba gyanú (a felhasználó döntése, 2026-10-06, DT-F56a):** ha a hibás `fej:vers` más könyvben is létezik, és ott a Strong-szám szerepel (pl. `Ruth 8:14` → `Ez 8:14`, `Jób 8:14`, `2Sám 8:14`, `Neh 8:14`), a hiba nem feltétlenül fejezetszám-elgépelés, hanem a BDB-forrás könyvfeloldási hibája (ismert eset: `H0834 Ruth 8, 9 (Préd)`), ezért **a sor `jelolt_marad`, akkor is, ha egyetlen jelölt van**; a javítás fordítási szöveget érintene az M5-ben. Az `indok` `FIGYELEM:` jelzést kap. Hatás: a korábban 21 `javitva` sorból 12 (mind FIGYELEM-es) `jelolt_marad` lett; a maradék 9 `javitva` marad. FIGYELEM-es sor összesen 60, javitva-FIGYELEM-es 0. Az algoritmus (`bdb_adatblokk.javitas_sorok`) ezt építi be, a `--javitas-epit` újrafuttatása ugyanezt adja (teszt: `test_konyvnev_gyanu_jelolt_marad`, `test_javitva_sorban_nincs_figyelem`).

## 5. M3b — az LXX-szakasz nyelvtani szűrése (a felhasználó döntése, 2026-10-06)

A mintában 7/20 blokk legleggyakoribb LXX-találatai közé névelő/elöljáró került (G3588 ὁ 5 blokkban, H894-nél G1519 εἰς ×18). Javítás: a 3. szakasz az `adat/grammatikai_strongok.tsv` alapján szűr. **Ha a héber szó nem nyelvtani, a nyelvtani görög találatok kimaradnak** a legfeljebb 3 közül (a kihagyás a blokkban `[kihagyva …]` sorral jelölt, nem néma); ha a héber szó maga is nyelvtani (pl. H3588, H0413), a görög nyelvtani találatok maradnak. Teszt: `teszt_bdb_adatblokk.py` `LxxSzures`. A mintát újragenerálta a `naplok/F56_minta.py`, a szúrópróba az LXX-szakaszt a nyers `lxx_bridge.tsv` + `grammatikai_strongok.tsv` fájlokból, a blokk kódjától függetlenül számolja újra (20/20 egyezik). A szűrő a lista alapján működik: a `H3282` (ja'an) nincs a nyelvtani listán, ezért nála a G3754 ὅτι és G1223 διά is kimarad (nyitott kérdés az orkesztrátornak: kerüljön-e a H3282 a listára).
