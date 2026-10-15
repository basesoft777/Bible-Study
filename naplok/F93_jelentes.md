# F93 jelentés — a TIPNR token nélküli alapszámai

*FELADATOK #93 · Modell: claude-sonnet-5-5 · állapot: az M0–M3 kész, a zárás (független ellenőr, draft PR) hátra van · döntések: DT-F93a, DT-F93b · lista: `naplok/F93_alapszamok.tsv` · szkript: `eszkozok/f93_tipnr_token_hiany.py`*

## 1. Eredmény

A `pardes.db` `tipnr` tábla 35 522 sorából 89 sor `strong` értéke nem szerepel a `token_strong`-ban; ebből 1 a #88 levágott utótagos sora (`G6202`, az F88 jelentésében jelölve), **88 utótag nélküli sor, 62 különböző alapszám**. Mind a 62 alapszám pontosan egy osztályt kapott (a lista 62 sor, a mögötte álló TIPNR-sorok száma 88). A jelölés (DT-F93a (a)) csak a listában és ebben a jelentésben áll: sem a TIPNR/TAGNT/TAHOT, sem a `pardes.db`, sem a kód nem változott.
`proveniencia: scope=tipnr(utótag nélkül) ∖ token_strong; token_eredeti (TAGNT/TAHOT) | forras=pardes.db (epites_ts=2026-10-14T09:35:00Z), konkordancia/TIPNR_kivonat.tsv, TAGNT_kivonat.tsv, TAHOT_kivonat.tsv | ts=2026-10-14T09:35:00Z`

### Osztályonkénti darabszám (alapszám / TIPNR-sor; egyezik a listával)

| osztály | görög (alapszám / sor) | héber (alapszám / sor) | összesen |
|---|---|---|---|
| szövegváltozat | 5 / 6 | 0 | 5 / 6 |
| alak-/névhasítás | 3 / 5 | 10 / 22 | 13 / 27 |
| fordítási névalak | 0 | 15 / 21 | 15 / 21 |
| ketiv/qere | 0 | 0 | 0 / 0 |
| adathiány | 1 / 1 | 0 | 1 / 1 |
| nincs Károli-vers | 5 / 9 | 0 | 5 / 9 |
| nem eldönthető | 2 / 2 | 21 / 22 | 23 / 24 |
| **összesen** | **16 / 23** | **46 / 65** | **62 / 88** |

Az alapszámok osztályonként:

- szövegváltozat, görög (5): G0300, G0962, G2179, G2499, G4668
- alak-/névhasítás, görög (3): G3018, G4315, G4566
- alak-/névhasítás, héber (10): H0704, H2680, H3074, H3159, H3482, H3571, H3762, H5827, H5985, H7741
- fordítási névalak, héber (15): H0382, H0885, H1184, H1857, H2126, H2316, H3070, H3071, H3072, H3073, H4663, H5757, H5886, H5904, H6549
- adathiány, görög (1): G3496
- nincs Károli-vers, görög (5): G9825, G9826, G9829, G9831, G9832
- nem eldönthető, görög (2): G2568, G3535
- nem eldönthető, héber (21): H0071, H0415, H1006, H1023, H1045, H1136, H1181, H2072, H2699, H3108, H3274, H3328, H3889, H4319, H5993, H7802, H7864, H8053, H8073, H8351, H8445

Az osztályok: **szövegváltozat** (csak görög: a névhez illő token `Kritikai kiadás` mezője a TR-t nem tartalmazza); **alak-/névhasítás** (nincs kiadás-/fordítás-jelölés, a versen a névhez illő token megvan, a TIPNR a névalaknak külön Strong-számot ad); **fordítási névalak** (csak héber: csak ESV/KJV/NIV/ASV jelölés, a versen a névhez illő token áll); **ketiv/qere** (LK/LQ/Mss jelölés, ha a TAHOT a versen ketiv/qere-jelölést hordoz); **adathiány** (nincs jelölés, és a versen nincs a névhez illő token); **nincs Károli-vers** (`LXX.*` hely, a TIPNR-sor igehelye üres); **nem eldönthető** (a repó adatából nem dönthető el; explicit jelölve, nem kitöltve). A szabályok részletei az M1 szakaszban.

### A „nem eldönthető” alapszámok teljes listája (23 alapszám: 2 görög + 21 héber)

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

**(2) A versen nincs a névhez illő token, vagy csak névcímke-alapú társ van, nem egyező glosszával — 2 görög + 9 héber alapszám:**

- `G2568` (Fair_Havens, görög) — ApCsel 27:8
- `G3535` (Nineveh, görög) — Luk 11:32
- `H0415` (LORD, héber) — 1Móz 33:20
- `H1006` (Bajith, héber) — Ézs 15:2
- `H1023` (Beth-merhak, héber) — 2Sám 15:17
- `H1045` (Beth-Ashtoreth, héber) — 1Sám 31:10
- `H1136` (Ben-hesed, héber) — 1Kir 4:10
- `H1181` (Bamoth-baal, héber) — 4Móz 21:28
- `H2699` (Hazerim, héber) — 5Móz 2:23
- `H5993` (Amminadib, héber) — Én 6:12
- `H7802` (Shushan_Eduth, héber) — Zsolt 60:1

(Ebből: nincs jelölés, gyenge társ — G2568, G3535, H0415; fordítás-jelölés, de a versen nincs a névhez illő token — H1006, H1023, H1045, H1136, H1181, H2699, H7802; a versen és a szomszéd versben sincs token — H5993.)

### A ketiv/qere osztály üres — miért

A „ketiv/qere” osztály feltétele, hogy a TAHOT az adott versen ketiv/qere-jelölést hordozzon. A `TAHOT_kivonat.tsv` egyetlen sorában sincs ilyen jelölés: a `TAHOT_TAGNT_README.md` szerint a ketiv/qere-illesztési üres helyőrzőket (Strong-szám nélküli `/  /` szegmenseket) a kivonat kihagyja, és a kivonat oszlopai (`Igehely`, `Strong-szám`, `Ragozott alak`, `Kiejtés`, `Szótő`, `Rövid jelentés`, `Angol tükörfordítás`) nem hordoznak kiadás- vagy ketiv/qere-mezőt. A szkript ellenőrzi az `alak` mezőt `(K)`/`(Q)`/ketiv/qere mintákra: nincs találat. Ezért a 12 LK/LQ/Mss alapszám „nem eldönthető”, azzal az indoklással, hogy az LK/LQ jelentését a repó nem rögzíti (N-F93a).

## 2. Egyeztetett eltérés

A brief a hatókört „62 token nélküli *görög* alapszám”-ként írta le. Az M0 mérése szerint a 62 alapszám 88 sora nem mind görög: 16 görög alapszám (23 sor; ebből 5 alapszám / 9 sor `LXX.*`, igehely nélkül) és 46 héber (65 sor, a TAHOT-oldalon hiányzó alapszámok). Az egyeztetett (felhasználói, 2026-10-15, chat) hatókör a DT-F93a (iii) szerint **mind a 62 alapszám** (a görög a TAGNT-ből, a héber a TAHOT-ból). Ezzel járó eltérések a briefhez képest:

- az osztálylista a brief négy osztályáról (szövegváltozat / számozási eltérés / adathiány / nem eldönthető) bővült: **alak-/névhasítás**, **nincs Károli-vers**, **fordítási névalak**, **ketiv/qere**; a „számozási eltérés” osztály megmaradt, de üres (0 alapszám);
- a **héber „szövegváltozat” osztály megszűnt** (DT-F93b): a TAHOT-nak nincs `Kritikai kiadás` mezője, így a brief definíciója héberre nem teljesülhet; a G3 (a TAGNT-oldali Strong-szám és a `Kritikai kiadás` mező megnevezése) csak a görög „szövegváltozat” sorokra vonatkozik;
- az `ir` mezőből kikerült az `eszkozok/sqlite_epit.py`, az `eszkozok/teszt_sqlite_epit.py` és az `adat/SEMA.md`, mert a DT-F93a (a) szerint a #93 nem ír a `pardes.db`-be (a brief 3. pontjának M2 (a) ága); a G5 emiatt nem alkalmazható;
- az `olvas` mezőbe bekerült a `konkordancia/TAHOT_kivonat.tsv` (a héber alapszámok forrása);
- a névegyeztetés nem csak a TIPNR névcímkén, hanem a token glosszáján is múlik (M1), és a „gyenge társ” szabály mindkét nyelvre egységes.

## 3. Döntések és nyitott tételek

- **DT-F93a** (🟢, a felhasználó döntése, 2026-10-15, chat): (1) a jelölés csak a `naplok/F93_alapszamok.tsv`-ben és a jelentésben áll; (2) hatókör (iii): mind a 62 alapszám, az osztálylista kiegészítésével.
- **DT-F93b** (🟢, a felhasználó döntése, 2026-10-15, chat): a héber „szövegváltozat” osztály megszűnik; „fordítási névalak” és „ketiv/qere” osztály.
- **N-F93a** (helyőrző, `NYITOTT_FELADATOK.md`): a ketiv/qere (LK/LQ/Mss) jelölés jelentése és hiánya a TAHOT-kivonatban; eldöntendő, kell-e a nyers STEPBible TAHOT vagy a TIPNR kiadás-jelmagyarázata a jelöléshez (12 alapszám érintett).
- **N-F93b** (helyőrző, `NYITOTT_FELADATOK.md`): a `lekerdez.py scan` néma nem-találata a 62 alapszámra (pl. `scan G0300` → `n=0`); eldöntendő, jelezze-e a lekérdezés vagy az olvasói felület (#92) a hiányt a lista alapján. A #93 a `lekerdez.py`-t nem érinti.

Végleges `DT`/`N` számot ágon nem írtam; a számot a `main`-en a `szamkiosztas` Action adja.

## 4. Elfogadási feltételek

- **G1** A diff nem érint `konkordancia/`, `motivumok/`, `lexikon/` fájlt és `adat/*.tsv`-t; a `pardes.db` nincs a repóban.
- **G2** 62 alapszám, mindegyik pontosan egy osztályban; 62 listasor, 88 TIPNR-sor.
- **G3** Minden görög „szövegváltozat” sor megnevezi a TAGNT-oldali Strong-számot és a `Kritikai kiadás` mezőt; minden sor proveniencia-sort hordoz; ahol a repó adata nem dönt, „nem eldönthető”.
- **G4** Két futás kimenete bájtazonos (a lista sha256-ja: `e61ec321155a0751ce4c3f932beee9f0833545026baa39a91d0df65d6b7e2c0d`).
- **G5** nem alkalmazható (DT-F93a (a): nincs `pardes.db`-változás).
- `python eszkozok/feladatok.py ellenoriz`: 0 hiba. A független ellenőrzés (`fuggetlen-ellenor`) a zárás része, még nem futott.

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

**Névegyeztetés** (a versen lévő token megkeresése): (1) TIPNR-azonosság: azonos névcímkéjű másik TIPNR-sor Strong-száma a vers tokenjei között; (2) glossz-egyezés: a token `Rövid jelentés` vagy `Angol tükörfordítás` mezője egyezik a névcímkével vagy a `Névváltozat` nagybetűs névalakjával. A két bizonyíték együtt adja a társ-tokenek listáját, nyelvtől függetlenül egységesen. Egy találat „gyenge”, ha a token glosszája nem egyezik a névalakkal (pl. H0415 `LORD` ↔ H0410 `God`/`El`; G2568 ↔ G2570 `good`/`Fair`; G3535 ↔ G3536 `Ninevite`). **Szabály, mindkét nyelvre:** ha a sorban nincs kiadás-/fordítás-jelölés, és a versen csak gyenge társ van, az osztály „nem eldönthető” (jelölés nélküli „szövegváltozat” vagy „alak-/névhasítás” csak egyező glosszával lehet, mint a G2179); jelölés mellett a glossz eltérése maga a jelzés (a görög TR-jelölésű sorokban a szövegváltozat, a héber fordítás-jelölésű sorokban a fordítási névalak). A G2568 és a G3535 ezért „nem eldönthető”. Az, hogy a versen más nevű token van, nem bizonyíték.

**Vegyes sorú alapszám:** ha egy alapszám több TIPNR-sora versenként eltérő osztályba esik (pl. a H3482, H3159 típusú népnévi alakok), az alapszám „nem eldönthető”, és az indoklás felsorolja a sorok osztályait; csak az azonos osztályú sorok alapszáma kapja azt az osztályt. (A javított futásban nincs ilyen alapszám.)

**A javított M0/M1 esetek.**
- G4566 (Satan, 2Kor 12:7): a versen G4567 σατανᾶ token áll, glosszája `Satan`; a korábbi „adathiány” a TIPNR-sorokra épült (G4567 nincs a vers TIPNR-soraiban). Új osztály: alak-/névhasítás.
- G2179 (Ephesus, Jel 2:1): G2181 token, `Kritikai kiadás` NA28+NA27+Tyn+SBL+WH+Treg+Byz (TR nélkül) → szövegváltozat, jelölés nélkül is.
- H3072 (LORD): a korábbi „azonos nevű” állítás hamis volt (H6664 `[is] righteousness`); most az indoklás azonos *névcímkéről* beszél, és kimondja, hogy a token glosszája nem egyezik a névalakkal.

**DT-F93b (a felhasználó döntése, 2026-10-15, chat).** A TAHOT-nak nincs `Kritikai kiadás` mezője, ezért a héber „szövegváltozat” osztály megszűnt. Új osztályok héberre: „fordítási névalak” (csak ESV/KJV/NIV/ASV jelölés, a versen a névhez illő token), „ketiv/qere” (LK/LQ/Mss jelölés, ha a TAHOT a versen ketiv/qere-jelölést hordoz). A TAHOT-kivonat egy sorában sincs ketiv/qere-jelölés (a `TAHOT_TAGNT_README.md` szerint a ketiv/qere-illesztési üres helyőrzőket a kivonat kihagyja), ezért a „ketiv/qere” osztály üres, és az LK/LQ/Mss sorok „nem eldönthető”-k: az LK/LQ jelentését a repó nem rögzíti. A G3 (`Kritikai kiadás` mező) csak a görög „szövegváltozat” sorokra vonatkozik.
