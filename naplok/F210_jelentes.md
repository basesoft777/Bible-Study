# F210 — Bibliaválasztó az olvasóban: jelentés

*FELADATOK #210 · modell: claude-opus-5-5 · 2026-11-12 · ág: `claude/f210-bibliavalaszto-b8d821`*

**Hatókör-szűkítés menet közben** (a felhasználó szava az orkesztrátoron át, 2026-11-12): „meggondoltam ahol nincs stronf kapcsolat olyan szöveg ne kerüljön be”. A választóba csak szószintű Strong-kapcsolatú szöveg kerül: a Targum és a Vulgata (és a „versenként olvasható” ág) kimaradt; az első változat (F210.1–F210.3) ezeket még tartalmazta, az F210.4 vette ki őket az építőből és a szerverből.

## 1. Felmérés: mi van a `pardes.db`-ben

*proveniencia: scope=pardes.db (a főcheckout példánya, építve 2026-11-02T12:55:43Z), sqlite_master + COUNT(*) | forras=eszkozok/sqlite_epit.py | ts=2026-11-12*

| Biblia | a `pardes.db`-ben | kulcs |
|---|---|---|
| Károli 1908 | `vers`, `token_karoli`, `token_par` | Károli-vers |
| Modernizált Károli | **nincs** (csak `adat/karoli_modern/`) | Károli-vers; a Strong a `token_karoli` sorszámán át a `token_par`-ból |
| Héber ÓSZ (TAHOT) | `token_eredeti` (nyelv=H) | Károli-vers (F85) |
| Görög ÚSZ (TAGNT) | `token_eredeti` (nyelv=G) | Károli-vers |
| Septuaginta | `lxx_token` (`karoli_igehely`, `lxx_igehely`) | leképezve |
| KJV | `kjv`: **csak a Strong-címkés szavak**, a teljes szöveg nincs | leképezve; a `kjv` tábla a `nyilvanos`/`kereskedelmi` kiadásban kizárt (DT124) |
| BSB | `bsb` (szavanként, angol szórendben) | Károli-vers |
| Targum, Vulgata | nincs (csak `konkordancia/`) | — Strong-kapcsolat nincs: a választóba nem kerül (szűkítés) |

## 2. Strong-lefedettség (mérés)

*proveniencia: scope=a felépített pardes.db (worktree, sqlite_epit.py --mod teljes) | forras=scratchpad lefedettseg.py, kjv_illeszt.py (a bibliak._kjv_szavak szabályával) | ts=2026-11-12*

| Szöveg | token | Strong-os token | vers (a vonatkozó szövetség verseinek aránya) | Strong-os vers |
|---|---|---|---|---|
| Károli 1908 (viszonyítás) | 599 367 | 488 659 (81,5%) | 31 158 (100%) | 31 125 (99,9%) |
| Modernizált Károli | 585 621 | 481 936 (82,3%) | 31 158 (100%) | 31 125 (99,9%) |
| TAHOT | 469 300 | 469 300 (100%) | 23 204 (az ÓSZ 100%-a) | 100% |
| TAGNT | 142 096 | 142 096 (100%) | 7 957 (az ÚSZ 100%-a) | 100% |
| Septuaginta | 496 240 | 454 232 (91,5%) | 22 821 (az ÓSZ 98,3%-a) | 22 799 (99,9%) |
| BSB | 244 337 | 244 337 (100%) | 21 424 (az ÓSZ 92,3%-a) | 100% |
| KJV | 789 255 szó; 348 705 címke | a nem nyelvtani címkék 99,99%-a illeszkedik a szövegbe (310 155 / 310 183) | 31 078 | 31 075 (100%) |

A Károli és a modern Károli tokenarányát a betoldott (fordítói) szavak és a nyelvtani elemek adják; ez a Károli alapnézet szintje. **Részleges, jelezve:** (a) a BSB forrásfájljából (`BSB_Strongs.tsv`) hiányzik a 2Sám, az Ezsd és a Dán (N-F210a); (b) a Septuaginta 383 ÓSZ-versnél nem rendelhető Károli-vershez, és a Károli-vers nélküli LXX-szakaszok nem olvashatók; (c) a KJV Strong-rétege a `nyilvanos` és a `kereskedelmi` kiadásban kizárt: ott a KJV nem jelenik meg (a teljes szöveg Strong nélkül nem kerül be). Ezeken túl nincs részleges lefedettségű szöveg; a lista az orkesztrátor által megnevezett hét szöveg.

## 3. Építő (`eszkozok/sqlite_epit.py`, `_bibliak`)

*proveniencia: scope=sqlite_epit.py --mod teljes (a worktree adataiból) | forras=a futás kimenete | ts=2026-11-12*

Új táblák (licenc a `licencek.tsv` meglévő soraiból, táblaszinten): `szoveg_modern` 31 158 vers, `token_modern` 585 621 token (a kieső „vala” és társai nélkül), `szoveg_kjv` 31 085 vers. Az építés 120,6 s, 1110 MB, 108 tábla. A KJV teljes szövegéből 133 vers nem képezhető Károli-versre (`normalizalas_jelentes`, „nincs ilyen Károli-vers”; ugyanez a leképezés, mint a `kjv` táblánál).

## 4. Szerver

- `bibliak.py`: a regiszter (Magyar, Eredeti nyelv, Angol), az elérhetőség (lustán, könyvenként a fejezetek; a Biblia csak akkor választható, ha a szöveg- és a Strong-táblái megvannak, és a kiadás nem zárja ki őket), és a fejezet szövegoszlopa. A TAHOT előtagja (H9001–H9010) a következő szóhoz, a szuffixuma (H9011–H9049) az előzőhöz tapad; a nyelvtani elemre nincs koppintás. A KJV-szövegbe a Strong-címkés szavak sorrendben, szóhatáron illeszkednek. Az LXX-ben versenként egy szövegforma (a `-theodotion`, `-vaticanus-b` változat helyett az alap, ahol van).
- A cím: `?biblia=<kód>`; a Károli 1908 az alap, paraméter nélkül (a meglévő útvonalak és tesztek változatlanok); ismeretlen kód (pl. a régi `targum`, `vulgata`) az alapra esik. A gyorsítótár kulcsában a Biblia is benne van.
- A választó (`alap.html`): „Biblia és könyv kiválasztása”, Biblia → Könyv → Fejezet; a morzsa „Károli 1908 · 1Móz 1 ▾”. A könyvrács csak a választott Biblia könyveit mutatja; minden hivatkozás (fejezetrács, lapozó, kánon-sáv, ‹ ›, a JS-ben rajzolt fejezetrács és a címsor) a Bibliában marad.
- A nem Károli Biblia lapjának tetején jegy: mi ez, hogyan olvasható, a számozása; az üres állapotban a forrás- és licencsor. Az eltérő forrásszám a vers elején („LXX 22:1”, „KJV 3:1”).

## 5. Tesztek és böngészős próba

- `teszt_bibliavalaszto.py` (11 teszt): a választó szerkezete és sorrendje, Targum/Vulgata/„versenként” nincs; a Károli-útvonal változatlan; a hat nem Károli Biblia egy fejezete (1Móz 1; Mt 1 a modern Károlival, TAGNT-vel, KJV-vel); a szólinkek a Bibliában maradnak; a régi Targum/Vulgata cím az alapra esik; a BSB könyvrácsa (36); a `nyilvanos` kiadásban a KJV nincs a választóban.
- Élő szerver (WSL, 8790-es port, az új adatbázis másolatával): a választó a mockup szerint; a TAHOT-szóra koppintva a szópanel (H0430) nyílik, a cím `?biblia=tahot`-tal marad; a KJV (Zsolt 3) és az LXX (Zsolt 23) lapja helyes.
- A teljes tesztkör: l. a Zárást.

## 6. Zárás

A teljes tesztkör eredménye, a PR és a nyitott pontok (N-F210a–c): a PR leírásában és a `nyitott/uj/` fájlban. ⛔ A merge előtt a felhasználó a böngészőben átnézi.
