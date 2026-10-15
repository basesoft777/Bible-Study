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
