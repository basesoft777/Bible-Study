# F210 — Bibliaválasztó az olvasóban: jelentés

*FELADATOK #210 · modell: claude-opus-5-5 · 2026-11-12 · ág: `claude/f210-bibliavalaszto-b8d821`*

## 1. Felmérés: mi van a `pardes.db`-ben

*proveniencia: scope=pardes.db (a főcheckout példánya, építve 2026-11-02T12:55:43Z), sqlite_master + COUNT(*) | forras=eszkozok/sqlite_epit.py | ts=2026-11-12*

| Biblia | a `pardes.db`-ben | kulcs | Strong |
|---|---|---|---|
| Károli 1908 | `vers`, `token_karoli`, `token_par` | Károli-vers | szószintű |
| Modernizált Károli | **nincs** (csak `adat/karoli_modern/`) | Károli-vers | a `token_karoli` sorszámán át a `token_par`-ból |
| Héber ÓSZ (TAHOT) | `token_eredeti` (nyelv=H) | Károli-vers (F85) | szószintű |
| Görög ÚSZ (TAGNT) | `token_eredeti` (nyelv=G) | Károli-vers | szószintű |
| Septuaginta | `lxx_token` (`karoli_igehely`, `lxx_igehely`) | leképezve | szószintű |
| KJV | `kjv`: **csak a Strong-címkés szavak**, a teljes szöveg nincs | leképezve | szószintű (a `kjv` tábla a nyilvanos/kereskedelmi kiadásban kizárt, DT124) |
| BSB | `bsb` (szavanként, angol szórendben) | Károli-vers | szószintű |
| Targum | **nincs** (`konkordancia/Targum_PD.tsv`) | forrás-számozás | nincs |
| Vulgata | **nincs** (`konkordancia/Vulgata_Clementina.tsv`) | forrás-számozás | nincs |

## 2. Építő (`eszkozok/sqlite_epit.py`, `_bibliak`)

*proveniencia: scope=sqlite_epit.py --mod teljes (a worktree adataiból) | forras=a futás kimenete | ts=2026-11-12*

Új táblák (licenc a `licencek.tsv` meglévő soraiból, táblaszinten): `szoveg_modern` 31 158 vers, `token_modern` 585 621 token (a kieső „vala” és társai nélkül), `szoveg_kjv` 31 085 vers, `szoveg_targum` 15 142 vers, `szoveg_vulgata` 31 434 vers. Az építés 132,3 s, 1121 MB, 110 tábla. A KJV teljes szövegéből 133 vers nem képezhető Károli-versre (`normalizalas_jelentes`, „nincs ilyen Károli-vers”; ugyanez a leképezés, mint a `kjv` táblánál).

Elérhetőség könyvenként (mért): modern Károli, KJV, Vulgata 66 könyv; Septuaginta 39 (ÓSZ); Targum 26 (Tóra + Próféták); BSB **36**: a forrásfájlból (`BSB_Strongs.tsv`) hiányzik a 2Sám, az Ezsd és a Dán (N-F210a).

## 3. Szerver

- `bibliak.py`: a regiszter (a mockup négy csoportja), az elérhetőség (lustán, könyvenként a fejezetek), és a fejezet szövegoszlopa. A TAHOT előtagja (H9001–H9010) a következő szóhoz, a szuffixuma (H9011–H9049) az előzőhöz tapad; a nyelvtani elemre nincs koppintás. A KJV-szövegbe a Strong-címkés szavak sorrendben, szóhatáron illeszkednek. Az LXX-ben versenként egy szövegforma (a `-theodotion`, `-vaticanus-b` változat helyett az alap, ahol van).
- A cím: `?biblia=<kód>`; a Károli 1908 az alap, paraméter nélkül (a meglévő útvonalak és tesztek változatlanok). A gyorsítótár kulcsában a Biblia is benne van.
- A választó (`alap.html`): „Biblia és könyv kiválasztása”, Biblia → Könyv → Fejezet; a morzsa „Károli 1908 · 1Móz 1 ▾”. A könyvrács csak a választott Biblia könyveit mutatja; minden hivatkozás (fejezetrács, lapozó, kánon-sáv, ‹ ›, a JS-ben rajzolt fejezetrács és a címsor) a Bibliában marad.
- A nem Károli Biblia lapjának tetején jegy: mi ez, hogyan olvasható (szóra koppintva / versenként), a számozása; az üres állapotban a forrás- és licencsor.
- Targum, Vulgata: a forrás saját fejezete és versszáma, a versszám nem hivatkozás; a † jel: a Károliban ilyen számú vers nincs. Versegyezést nem állítunk (VISSZHANG_README 1.).

## 4. Tesztek és böngészős próba

- `teszt_bibliavalaszto.py` (10 teszt): a választó szerkezete és sorrendje, a Károli-útvonal változatlansága, mind a 8 nem Károli Biblia egy fejezete (1Móz 1; Mt 1 a modern Károlival, TAGNT-vel, KJV-vel, Vulgatával), a szólinkek a Bibliában maradnak, a Strong nélküli szöveg versenként olvasható, a Vulgata Zsolt 22 a forrás számozásával, a BSB könyvrácsa.
- Élő szerver (WSL, 8790-es port, az új adatbázis másolatával): a választó a mockup szerint; a TAHOT-szóra koppintva a szópanel (H0430) nyílik, a cím `?biblia=tahot`-tal marad; a Vulgata, a KJV (Zsolt 3: „KJV 3:1” jelzés) és az LXX (Zsolt 23: „LXX 22:1”) lapja helyes.

## 5. Zárás

Lásd a PR leírását; a teljes tesztkör eredménye és a nyitott pontok (N-F210a–d) ott és a `nyitott/uj/` fájlban. ⛔ A merge előtt a felhasználó a böngészőben átnézi.
