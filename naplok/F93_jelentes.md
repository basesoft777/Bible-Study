# F93 jelentés — a TIPNR token nélküli alapszámai

*FELADATOK #93 · Modell: claude-sonnet-5-5 · állapot: lezárva · döntések: DT-F93a–d · nyitott tételek: N-F93a–c · lista: `naplok/F93_alapszamok.tsv` · szkript: `eszkozok/f93_tipnr_token_hiany.py`*

## 1. Eredmény

A `pardes.db` `tipnr` tábla 35 522 sorából 89 sor `strong` értéke nem szerepel a `token_strong`-ban; ebből 1 a #88 levágott utótagos sora (`G6202`, az F88 jelentésében jelölve), **88 utótag nélküli sor, 62 különböző alapszám**. Mind a 62 alapszám pontosan egy osztályt kapott (a lista 62 sor, a mögötte álló TIPNR-sorok száma 88). A jelölés (DT-F93a (a)) csak a listában és ebben a jelentésben áll: sem a TIPNR/TAGNT/TAHOT, sem a `pardes.db`, sem a kód nem változott.
`proveniencia: scope=tipnr(utótag nélkül) ∖ token_strong; token_eredeti (TAGNT/TAHOT) | forras=pardes.db (tipnr, token_strong, token_eredeti, meta; epites_ts=2026-10-14T09:35:00Z), konkordancia/Karoli_1908.tsv, konkordancia/Karoli_versmegfeleltetes.tsv | ts=2026-10-14T09:35:00Z` (a `ts` az adatállapot időpontja, l. az M1 szakaszt)

### Osztályonkénti darabszám (alapszám / TIPNR-sor; egyezik a listával)

| osztály | görög (alapszám / sor) | héber (alapszám / sor) | összesen |
|---|---|---|---|
| szövegváltozat | 5 / 6 | 0 | 5 / 6 |
| alak-/névhasítás | 4 / 6 | 11 / 23 | 15 / 29 |
| fordítási névalak | 0 | 19 / 25 | 19 / 25 |
| ketiv/qere | 0 | 0 | 0 / 0 |
| adathiány | 0 | 0 | 0 / 0 |
| nincs Károli-vers | 5 / 9 | 1 / 1 | 6 / 10 |
| nem eldönthető | 2 / 2 | 15 / 16 | 17 / 18 |
| **összesen** | **16 / 23** | **46 / 65** | **62 / 88** |

Az alapszámok osztályonként:

- szövegváltozat, görög (5): G0300, G0962, G2179, G2499, G4668
- alak-/névhasítás, görög (4): G2568, G3018, G4315, G4566
- alak-/névhasítás, héber (11): H0415, H0704, H2680, H3074, H3159, H3482, H3571, H3762, H5827, H5985, H7741
- fordítási névalak, héber (19): H0382, H0885, H1045, H1136, H1184, H1857, H2126, H2316, H2699, H3070, H3071, H3072, H3073, H4663, H5757, H5886, H5904, H6549, H7802
- nincs Károli-vers, görög (5): G9825, G9826, G9829, G9831, G9832
- nincs Károli-vers, héber (1): H5993
- nem eldönthető, görög (2): G3496, G3535
- nem eldönthető, héber (15): H0071, H1006, H1023, H1181, H2072, H3108, H3274, H3328, H3889, H4319, H7864, H8053, H8073, H8351, H8445

Az osztályok: **szövegváltozat** (csak görög: a névhez illő token `Kritikai kiadás` mezője a TR-t nem tartalmazza; jelölés nélkül csak egyező glosszával, DT-F93c); **alak-/névhasítás** (nincs kiadás-/fordítás-jelölés, a versen a névhez illő token megvan, a TIPNR a névalaknak külön Strong-számot ad); **fordítási névalak** (csak héber: csak ESV/KJV/NIV/ASV jelölés, a versen a névhez illő token vagy tokensor áll); **ketiv/qere** (LK/LQ/Mss jelölés, ha a TAHOT a versen ketiv/qere-jelölést hordoz); **adathiány** (nincs jelölés, és a versen nincs a névhez illő token); **nincs Károli-vers** (`LXX.*` hely, vagy nem létező Károli-vers, N-F79b); **nem eldönthető** (a repó adatából nem dönthető el; explicit jelölve, nem kitöltve). A „névhez illő token” szigorú: TIPNR-azonosság, glossz-egyezés, vagy egymást követő tokenek glosszáinak együttes egyenlősége a névalakkal (az M1 szakasz). A számozási eltérés és az adathiány osztály üres.

### A „nem eldönthető” alapszámok teljes listája (17 alapszám: 2 görög + 15 héber)

**(1) LK/LQ/Mss jelölés, ketiv/qere-jelölés nélkül a TAHOT-kivonatban — 12 héber alapszám.** Az LK/LQ/Mss jelentését a repó nem rögzíti, és a `TAHOT_kivonat.tsv` a versen nem hordoz ketiv/qere-jelölést:

- `H0071` (Abana, héber) — 2Kir 5:12
- `H2072` (Zaccur, héber) — Ezsd 8:14
- `H3108` (Jozacar, héber) — 2Kir 12:21
- `H3274` (Jeush, héber) — 1Móz 36:14 ; 1Móz 36:5
- `H3328` (Izhar, héber) — 1Krón 4:7
- `H3889` (Laish, héber) — 2Sám 3:15
- `H4319` (Micaiah, héber) — 2Krón 18:8
- `H7864` (Seraiah, héber) — 2Sám 20:25
- `H8053` (Shamir, héber) — 1Krón 24:24
- `H8073` (Shalmai, héber) — Ezsd 2:46
- `H8351` (Seth, héber) — 4Móz 24:17
- `H8445` (Tikvah, héber) — 2Krón 34:22

**(2) A versen nincs a névhez illő token, vagy csak névcímke-alapú társ van, nem egyező glosszával — 5 alapszám:**

(2a) fordítás-jelölés mellett a versen sem egy token, sem egymást követő tokenek sora nem adja glosszáival együtt a névcímkét vagy a Névváltozat egyik névalakját (szigorú egyenlőség) — 3 héber alapszám:

- `H1006` (Bajith, héber) — Ézs 15:2
- `H1023` (Beth-merhak, héber) — 2Sám 15:17
- `H1181` (Bamoth-baal, héber) — 4Móz 21:28

(2b) jelölés nélkül csak névcímke-alapú társ van, amelynek glosszája nem egyezik a névalakkal (DT-F93c) — 1 alapszám:

- `G3535` (Nineveh, görög) — Luk 11:32

(2c) a névhez illő tokenek `Kritikai kiadás` mezőjének „»1” jelölése nem alapkiadás, jelentését a repó nem rögzíti (N-F93c) — 1 alapszám:

- `G3496` (Neapolis, görög) — ApCsel 16:11

### A ketiv/qere osztály üres — miért

A „ketiv/qere” osztály feltétele, hogy a TAHOT az adott versen ketiv/qere-jelölést hordozzon. A `TAHOT_kivonat.tsv` egyetlen sorában sincs ilyen jelölés: a `TAHOT_TAGNT_README.md` szerint a ketiv/qere-illesztési üres helyőrzőket (Strong-szám nélküli `/  /` szegmenseket) a kivonat kihagyja, és a kivonat oszlopai (`Igehely`, `Strong-szám`, `Ragozott alak`, `Kiejtés`, `Szótő`, `Rövid jelentés`, `Angol tükörfordítás`) nem hordoznak kiadás- vagy ketiv/qere-mezőt. A szkript ellenőrzi az `alak` mezőt `(K)`/`(Q)`/ketiv/qere mintákra: nincs találat. Ezért a 12 LK/LQ/Mss alapszám „nem eldönthető”, azzal az indoklással, hogy az LK/LQ jelentését a repó nem rögzíti (N-F93a).

### A H5993 (Amminadib): nem létező Károli-vers

A TIPNR a `Sng.6.12`-re mutat (`Én 6:12`). A `konkordancia/Karoli_1908.tsv`-ben az Én 6-nak 10 verse van (6:1–6:10), a 6:12 nem létezik; a `konkordancia/Karoli_versmegfeleltetes.tsv`-ben nincs `igehely_karoli` sor erre a versre (sőt az Én 5–6 fejezetei sem szerepelnek benne). A név elemei a TAHOT Én 6:9 versén állnak, de a 6:12 → 6:9 átváltást a repó versmegfeleltetése nem igazolja, és emlékezetből nem képezünk átváltást. Az osztály ezért „nincs Károli-vers” (a brief a nem létező Károli-versre mutató sorokat kizárja: N-F79b, DT114). A `LXX_versificacios_terkep.tsv` `Én 6:12` sora KJV-kulcsú számozási térkép (DT143), nem Károli-megfeleltetés; nem használtam fel.

## 2. Egyeztetett eltérés

A brief a hatókört „62 token nélküli *görög* alapszám”-ként írta le. Az M0 mérése szerint a 62 alapszám 88 sora nem mind görög: 16 görög alapszám (23 sor; ebből 5 alapszám / 9 sor `LXX.*`, igehely nélkül) és 46 héber (65 sor, a TAHOT-oldalon hiányzó alapszámok). Az egyeztetett (felhasználói, 2026-10-15, chat) hatókör a DT-F93a (iii) szerint **mind a 62 alapszám** (a görög a TAGNT-ből, a héber a TAHOT-ból). Ezzel járó eltérések a briefhez képest:

- az osztálylista a brief négy osztályáról (szövegváltozat / számozási eltérés / adathiány / nem eldönthető) bővült: **alak-/névhasítás**, **nincs Károli-vers**, **fordítási névalak**, **ketiv/qere**; a „számozási eltérés” osztály megmaradt, de üres (0 alapszám);
- a **héber „szövegváltozat” osztály megszűnt** (DT-F93b): a TAHOT-nak nincs `Kritikai kiadás` mezője, így a brief definíciója héberre nem teljesülhet; a G3 (a TAGNT-oldali Strong-szám és a `Kritikai kiadás` mező megnevezése) csak a görög „szövegváltozat” sorokra vonatkozik;
- az `ir` mezőből kikerült az `eszkozok/sqlite_epit.py`, az `eszkozok/teszt_sqlite_epit.py` és az `adat/SEMA.md`, mert a DT-F93a (a) szerint a #93 nem ír a `pardes.db`-be (a brief 3. pontjának M2 (a) ága); a G5 emiatt nem alkalmazható;
- az `olvas` mezőbe bekerült a `konkordancia/TAHOT_kivonat.tsv` (a héber alapszámok forrása);
- a névegyeztetés nem csak a TIPNR névcímkén, hanem a token glosszáján is múlik (M1), és a „gyenge társ” szabály mindkét nyelvre egységes.
- **több tokenre bontott nevek (ELLENOR_F93):** a névegyeztetés a versen egymást követő tokenek glosszáinak szigorú, együttes egyenlőségét is elfogadja a névvel vagy a Névváltozat névalakjával (pl. `Nea`+`Polis` = Neapolis); asszociatív vagy jelentésbeli egyezés nem elég;
- a **„nincs Károli-vers”** osztály a brief szerinti kizáráshoz igazodva a nem létező Károli-versre mutató sort (H5993, `Én 6:12`) is magában foglalja (N-F79b, DT114); az `olvas` mező ezért a `Karoli_1908.tsv`-vel és a `Karoli_versmegfeleltetes.tsv`-vel bővült;
- a **proveniencia** `forras` mezője csak a szkript által olvasott forrásokat sorolja (a `pardes.db` táblái és a két Károli-fájl); a `pardes.db` tábláit a TIPNR-, TAGNT- és TAHOT-kivonatból építi az `eszkozok/sqlite_epit.py`, de azokat a #93 szkriptje közvetlenül nem olvassa;
- **jelölés nélküli görög szövegváltozat (DT-F93c):** a brief szerint a szövegváltozathoz kiadás-jelölés kell a `Névváltozat`-ban; jelölés nélkül akkor lehet szövegváltozat, ha a versen álló token glosszája egyezik a névvel, és a token `Kritikai kiadás` mezője nem tartalmazza a TR-t (így a G2179); nem egyező glosszával „nem eldönthető” (G3535).

## 3. Döntések és nyitott tételek

- **DT-F93a** (🟢, a felhasználó döntése, 2026-10-15, chat): (1) a jelölés csak a `naplok/F93_alapszamok.tsv`-ben és a jelentésben áll; (2) hatókör (iii): mind a 62 alapszám, az osztálylista kiegészítésével.
- **DT-F93b** (🟢, a felhasználó döntése, 2026-10-15, chat): a héber „szövegváltozat” osztály megszűnik; „fordítási névalak” és „ketiv/qere” osztály.
- **DT-F93c** (🟢, a felhasználó döntése, 2026-10-15, chat): jelölés nélküli görög szövegváltozat csak egyező glosszájú, a TR-t nem tartalmazó kiadás-mezejű tokennel lehet (G2179); nem egyező glosszával „nem eldönthető” (G3535).
- **DT-F93d** (🟢, a felhasználó döntése, 2026-10-15, chat): a proveniencia `ts` mezője a `pardes.db` `meta.epites_ts` értéke (az adatállapot időpontja), nem a futásé; a szkript rögzített adatállapotot olvas, és a G4 (bájtazonos futás) ezt kívánja.
- **N-F93a** (helyőrző, `NYITOTT_FELADATOK.md`): a ketiv/qere (LK/LQ/Mss) jelölés jelentése és hiánya a TAHOT-kivonatban; eldöntendő, kell-e a nyers STEPBible TAHOT vagy a TIPNR kiadás-jelmagyarázata a jelöléshez (12 alapszám érintett).
- **N-F93c** (helyőrző, `NYITOTT_FELADATOK.md`): a TAGNT `Kritikai kiadás` mezőjének „»N” jelölése (pl. `TR»1`); a jelentését a repó nem rögzíti, ezért a G3496 (Neapolis) „nem eldönthető”.
- **N-F93b** (helyőrző, `NYITOTT_FELADATOK.md`): a `lekerdez.py scan` néma nem-találata a 62 alapszámra (pl. `scan G0300` → `n=0`); eldöntendő, jelezze-e a lekérdezés vagy az olvasói felület (#92) a hiányt a lista alapján. A #93 a `lekerdez.py`-t nem érinti.

Végleges `DT`/`N` számot ágon nem írtam; a számot a `main`-en a `szamkiosztas` Action adja.

## 4. Elfogadási feltételek

- **G1** A diff nem érint `konkordancia/`, `motivumok/`, `lexikon/` fájlt és `adat/*.tsv`-t; a `pardes.db` nincs a repóban.
- **G2** 62 alapszám, mindegyik pontosan egy osztályban; 62 listasor, 88 TIPNR-sor.
- **G3** Minden görög „szövegváltozat” sor megnevezi a TAGNT-oldali Strong-számot és a `Kritikai kiadás` mezőt; minden sor proveniencia-sort hordoz; ahol a repó adata nem dönt, „nem eldönthető”.
- **G4** Két futás kimenete bájtazonos (a lista sha256-ja: `0c7946c1b40de82e54e684f4292fb369263784f93aaad936770f68819a5ed5a0`).
- **G5** nem alkalmazható (DT-F93a (a): nincs `pardes.db`-változás).
- `python eszkozok/feladatok.py ellenoriz`: 0 hiba. Független ellenőrzés (`fuggetlen-ellenor`), négy kör: `naplok/ELLENOR_F93.md` — 6 eltérés, javítva (F93.13–F93.16); `naplok/ELLENOR_F93_2.md` — 3 eltérés, javítva (F93.18–F93.20); `naplok/ELLENOR_F93_3.md` — 1 eltérés, javítva (ef55c97a); `naplok/ELLENOR_F93_4.md` — 2 nem tartalmi eltérés (elavult meta-sorok a jelentésben; kettős F93.21 előtag), a zárás commitjában rendezve.
- Megjegyzés: az `F93.21` előtag két commiton áll (`cc7f41db`: a 3. kör jelentése; `ef55c97a`: a kódjavítás). A history nem íródik át, mert az ág már fent van; a `git log --grep="F93.21"` ezért két tételt ad vissza.

## Munkanapló (M0–M1)

*Az M0 próbaosztályozása előzetes volt, a végleges osztályozást az M1 adja (l. fent); a szakaszok a mérés és a szabályok nyomát őrzik.*

## M0 — felmérés (csak olvas)

**Módszer.** A kész `pardes.db` (a repón kívüli build, csak olvasásra nyitva; a `tipnr`, a `token_strong` és a `token_eredeti` tábla) lekérdezése: `tipnr` sorai, amelyek `strong` értéke a `token_strong.strong`-ban nem szerepel. A mérőszkript ideiglenes, a repón kívül futott; az M1 hozza létre az `eszkozok/f93_tipnr_token_hiany.py`-t.
`proveniencia: scope=pardes.db tipnr∖token_strong | forras=pardes.db (2026-10-14 11:35) | ts=2026-10-15T09:40Z`

### 1. Újramérés

| | érték |
|---|---|
| `tipnr` sora, `strong` ∉ `token_strong` | **89** |
| ebből utótagos (`G6202`, `Millo`/`Akra`, LXX.Isa.22.9; #88, a jelentésben jelölt) | 1 |
| utótag nélküli sor | **88** |
| ezek különböző alapszáma | **62** |

A brief számai (88 sor / 62 alapszám) egyeznek az F88 mérésével. **Eltérés a brief leírásától:** a 88 sor nem mind görög.

| nyelv | sor | alapszám | ebből igehely nélküli (`LXX.*`) |
|---|---|---|---|
| görög | 23 | 16 | 9 sor, 5 alapszám (G9825, G9826, G9829, G9831, G9832; pl. `Agag`/`Bougeon`, `LXX.Est.3.1`) |
| héber | 65 | 46 | 0 |

A héber sorok a TAHOT-oldalon hiányzó alapszámok (pl. `H0704` Arba, `H3159` Jezreelitess, `H6549` Neco, a `LORD` összetett nevek `H3070`–`H3073`, `H0415`). A brief 2. pontja csak a TAGNT-kivonatot nevezi meg; a héber sorokhoz a TAHOT-kivonat (`token_eredeti`, `forras_fajl` ≠ TAGNT) kellene.

### 2. A `Névváltozat` kiadás-jelöléseinek eloszlása (a 88 soron)

Jelölés: a `=` utáni kiadás-rövidítések (egy sor több kiadást is hordozhat; `-` = nincs `=` jelölés).

| kiadás | görög sor | héber sor |
|---|---|---|
| `-` (nincs jelölés) | 18 | 23 |
| KJV | 4 | 39 |
| TR | 5 | – |
| NIV | 2 | 37 |
| ESV | – | 38 |
| LK | – | 12 |
| LQ | – | 7 |
| ASV / Mss | – | 1 / 1 |

Megfigyelés: a görög sorok TR/KJV/NIV jelölése a briefnek megfelelő (`Amon =NIV,KJV,TR`, `G0300`). A jelöletlen 41 sor (18 + 23) nagyrészt nem kiadás-eltérés, hanem a TIPNR névváltozat-szétbontása (pl. `Jezreel` → `Jezreelitess` `H3159`, `Ammon` → `Ammonitess` `H5985`, `Cush` → `Cushitess`), ahol a TIPNR a nemű/népnévi alaknak külön Strong-számot ad.

### 3. Próbaosztályozás (előzetes, nem a végleges; a brief osztályaival)

Szempont: (i) van-e kiadás-jelölés a `Névváltozat`-ban; (ii) van-e a sor igehelyén (Károli-kulcs, `tipnr.igehely`) `token_eredeti`-sor; (iii) a versen szerepel-e a TIPNR más neve olyan Strong-számmal, amely a `token_strong`-ban a versen megvan. A „szövegváltozat” végső besorolásához a TAGNT/TAHOT-oldali Strong-szám és `Kritikai kiadás` ellenőrzése még kell (M1).

| próbaosztály | görög sor / alapszám | héber sor / alapszám |
|---|---|---|
| kiadás-jelölés + a versen van más név-token → szövegváltozat-jelölt | 5 / 4 (G0300, G0962, G2499, G4668) | 40 / 33 |
| kiadás-jelölés, de a versen nincs más név-token | 0 / 0 | 1 / 1 (H1023) |
| nincs jelölés + a versen van más név-token (alak-/névhasítás, nem kiadás) | 7 / 5 (G2568, G3018, G3496, G3535, G4315) | 23 / 11 |
| nincs jelölés, nincs más név-token → adathiány-jelölt | 2 / 2 (G2179, G4566) | 0 / 0 |
| nincs Károli-vers (`LXX.*`, igehely üres) → nem a brief osztályainak egyike | 9 / 5 | 0 / 0 |
| nincs token a versen | 0 / 0 | 1 / 1 (H5993, Én 6:12) |
| **összesen** | **23 / 16** | **65 / 46** (88 sor / 62 alapszám) |

(Az alapszám-összegek: görög 4 + 5 + 2 + 5 = 16, héber 33 + 1 + 11 + 1 = 46; egy alapszám egy osztályba esik.)

Nem eldönthető, mert hiányzó osztály: az `LXX.*` 9 sor (5 alapszám) nem kapcsolható Károli-versre, tehát TAGNT-versre sem (#92/DT134 versifikációs terület); a „nincs jelölés + más név-token” 34 sor (16 alapszám) a brief négy osztályába nem illik tisztán (a TIPNR és a token-forrás eltérő Strong-hasítása).

### 4. Megállás

(A megállás feloldva: DT-F93a és DT-F93b 🟢, 2026-10-15.)

## M1 — a lista és az osztályozás szabályai

*(A szabályok rögzítése az M1 javításai után.)*

**Névegyeztetés** (a versen lévő token megkeresése): (1) TIPNR-azonosság: azonos névcímkéjű másik TIPNR-sor Strong-száma a vers tokenjei között; (2) glossz-egyezés: a token `Rövid jelentés` vagy `Angol tükörfordítás` mezője egyezik a névcímkével vagy a `Névváltozat` nagybetűs névalakjával. A két bizonyíték együtt adja a társ-tokenek listáját, nyelvtől függetlenül egységesen. Egy találat „gyenge”, ha a token glosszája nem egyezik a névalakkal (pl. H0415 `LORD` ↔ H0410 `God`/`El`; G2568 ↔ G2570 `good`/`Fair`; G3535 ↔ G3536 `Ninevite`). **Szabály, mindkét nyelvre:** ha a sorban nincs kiadás-/fordítás-jelölés, és a versen csak gyenge társ van, az osztály „nem eldönthető” (jelölés nélküli „szövegváltozat” vagy „alak-/névhasítás” csak egyező glosszával lehet, mint a G2179); jelölés mellett a glossz eltérése maga a jelzés (a görög TR-jelölésű sorokban a szövegváltozat, a héber fordítás-jelölésű sorokban a fordítási névalak). A G3535 ezért „nem eldönthető”. A G2568-nál a gyenge névcímke-alapú társ (G2570) mellett a G2570+G3040 egymást követő tokenek glosszái (`Fair`+`Havens`) együtt szigorúan egyenlők a „Fair Havens” névvel, ezért a G2568 alak-/névhasítás. Az, hogy a versen más nevű token van, nem bizonyíték.

**Több tokenre bontott név (3. bizonyíték).** A versen egymást követő tokenek (legfeljebb 5) glosszái (mind a Rövid jelentés, vagy mind az Angol tükörfordítás; a `[..]` és `<..>` betoldások nélkül, írásjel- és kisbetű-különbség nélkül) együtt szigorúan egyenlők a névcímkével vagy a Névváltozat valamelyik névalakjával (pl. `Nea`+`Polis` = Neapolis; `Ben-`+`Hesed` = Ben-hesed; `Shushan-`+`eduth`; `house of`+`Ashtaroth`). Minden tokennek ki kell tennie a névalak egy részét. Az egyetlen tokenes, kisbetűs névalak (pl. `villages`) is csak pontos egyenlőséggel számít.

**A `ts` jelentése.** A lista `proveniencia` mezőjének `ts` értéke a `pardes.db` `meta.epites_ts` értéke, vagyis az adatállapot időpontja, nem a szkript futásáé. Ez tudatos: a G4 (két futás bájtazonos) csak így teljesül, mert a futás ideje minden futásnál más volna; az adatállapot időpontja a lekérdezett adat tényleges keletkezési ideje. Döntés: DT-F93d (🟢, a felhasználó döntése, 2026-10-15, chat).

**Vegyes sorú alapszám:** ha egy alapszám több TIPNR-sora versenként eltérő osztályba esik (pl. a H3482, H3159 típusú népnévi alakok), az alapszám „nem eldönthető”, és az indoklás felsorolja a sorok osztályait; csak az azonos osztályú sorok alapszáma kapja azt az osztályt. (A javított futásban nincs ilyen alapszám.)

**A javított M0/M1 esetek.**
- G4566 (Satan, 2Kor 12:7): a versen G4567 σατανᾶ token áll, glosszája `Satan`; a korábbi „adathiány” a TIPNR-sorokra épült (G4567 nincs a vers TIPNR-soraiban). Új osztály: alak-/névhasítás.
- G2179 (Ephesus, Jel 2:1): G2181 token, `Kritikai kiadás` NA28+NA27+Tyn+SBL+WH+Treg+Byz (TR nélkül) → szövegváltozat, jelölés nélkül is.
- H3072 (LORD): a korábbi „azonos nevű” állítás hamis volt; az indoklás most azonos *névcímkéről* beszél. A TAHOT a H6664 Rövid jelentését `LORD`-nak adja (Angol tükörfordítás: `[is] righteousness`), tehát a glossz-egyezés a névvel teljesül; a H3068 (`LORD`, `Yahweh`) is társ-token. Az osztály („fordítási névalak”) nem változott. (Az M1 korábbi változatának az a mondata, hogy a H6664 glosszája nem egyezik a névalakkal, téves volt.)

**DT-F93b (a felhasználó döntése, 2026-10-15, chat).** A TAHOT-nak nincs `Kritikai kiadás` mezője, ezért a héber „szövegváltozat” osztály megszűnt. Új osztályok héberre: „fordítási névalak” (csak ESV/KJV/NIV/ASV jelölés, a versen a névhez illő token), „ketiv/qere” (LK/LQ/Mss jelölés, ha a TAHOT a versen ketiv/qere-jelölést hordoz). A TAHOT-kivonat egy sorában sincs ketiv/qere-jelölés (a `TAHOT_TAGNT_README.md` szerint a ketiv/qere-illesztési üres helyőrzőket a kivonat kihagyja), ezért a „ketiv/qere” osztály üres, és az LK/LQ/Mss sorok „nem eldönthető”-k: az LK/LQ jelentését a repó nem rögzíti. A G3 (`Kritikai kiadás` mező) csak a görög „szövegváltozat” sorokra vonatkozik.
