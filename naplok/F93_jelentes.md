# F93 jelentés — a TIPNR token nélküli alapszámai

*FELADATOK #93 · Modell: claude-sonnet-5-5 · állapot: az M0 kész, ⛔ DT-F93a (a jelölés helye és a hatókör)*

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

### 4. ⛔ Megállás

A DT-F93a a `DONTESEK.md`-ben nyitott (a jelölés helye és a hatókör). Az M1 (szkript, lista) nem indult.

## M1 — a lista és az osztályozás szabályai

*(A végleges jelentés az M3-ban készül; ez a szakasz az M1 javítása után a szabályokat rögzíti. A lista: `naplok/F93_alapszamok.tsv`, a szkript: `eszkozok/f93_tipnr_token_hiany.py`.)*

**Névegyeztetés** (a versen lévő token megkeresése): (1) TIPNR-azonosság: azonos névcímkéjű másik TIPNR-sor Strong-száma a vers tokenjei között; (2) glossz-egyezés: a token `Rövid jelentés` vagy `Angol tükörfordítás` mezője egyezik a névcímkével vagy a `Névváltozat` nagybetűs névalakjával. Az (1) csak akkor erős, ha a token glosszája a névalakot is támogatja; ha nem (pl. H0415 `LORD` ↔ H0410 `God`/`El`), az indoklás ezt kimondja, és jelölés nélküli sorban az eredmény „nem eldönthető”. Az, hogy a versen más nevű token van, nem bizonyíték.

**Vegyes sorú alapszám:** ha egy alapszám több TIPNR-sora versenként eltérő osztályba esik (pl. a H3482, H3159 típusú népnévi alakok), az alapszám „nem eldönthető”, és az indoklás felsorolja a sorok osztályait; csak az azonos osztályú sorok alapszáma kapja azt az osztályt. (A javított futásban nincs ilyen alapszám.)

**A javított M0/M1 esetek.**
- G4566 (Satan, 2Kor 12:7): a versen G4567 σατανᾶ token áll, glosszája `Satan`; a korábbi „adathiány” a TIPNR-sorokra épült (G4567 nincs a vers TIPNR-soraiban). Új osztály: alak-/névhasítás.
- G2179 (Ephesus, Jel 2:1): G2181 token, `Kritikai kiadás` NA28+NA27+Tyn+SBL+WH+Treg+Byz (TR nélkül) → szövegváltozat, jelölés nélkül is.
- H3072 (LORD): a korábbi „azonos nevű” állítás hamis volt (H6664 `[is] righteousness`); most az indoklás azonos *névcímkéről* beszél, és kimondja, hogy a token glosszája nem egyezik a névalakkal.

**DT-F93b (a felhasználó döntése, 2026-10-15, chat).** A TAHOT-nak nincs `Kritikai kiadás` mezője, ezért a héber „szövegváltozat” osztály megszűnt. Új osztályok héberre: „fordítási névalak” (csak ESV/KJV/NIV/ASV jelölés, a versen a névhez illő token), „ketiv/qere” (LK/LQ/Mss jelölés, ha a TAHOT a versen ketiv/qere-jelölést hordoz). A TAHOT-kivonat egy sorában sincs ketiv/qere-jelölés (a `TAHOT_TAGNT_README.md` szerint a ketiv/qere-illesztési üres helyőrzőket a kivonat kihagyja), ezért a „ketiv/qere” osztály üres, és az LK/LQ/Mss sorok „nem eldönthető”-k: az LK/LQ jelentését a repó nem rögzíti. A G3 (`Kritikai kiadás` mező) csak a görög „szövegváltozat” sorokra vonatkozik.
