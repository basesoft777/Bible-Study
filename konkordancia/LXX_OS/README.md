# LXX_OS — Rahlfs-LXX kivonat (lxx-morph + GreekWordList)

Ez a könyvtár a Rahlfs-Septuaginta (1935) szó-szintű kivonatát tartalmazza,
könyvenként (a lxx-morph 59 műve — protokanonikus ÓSZ + deuterokanonikus +
Salamon zsoltárai). **A `konkordancia/LXX_kivonat_*.tsv` (a régi, studybible.info
alapú kivonat) továbbra is megmarad** — a generátor egyelőre azt használja
(l. `LEXV2_1_BRIEF.md` G6). Ez a kivonat a lexikon-oldal v2 (2. menet)
előkészítése, és a régi LXX-kivonat licenc-tisztázatlanságát (N15) oldja fel.

## 1. Forrás

### Szöveg + morfológia + lemma: lxx-morph

- **Repó:** `github.com/OpenScriptorium/lxx-morph` (GitHub-tükör:
  `git.sr.ht/~sethkush/lxx-morph`)
- **Rögzített commit:** `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`
- **Fájlok:** `db/seeds/lxx_morph/<könyv-slug>.json` (59 könyv), egyenként a
  könyv minden versére: `{"ref": "Fejezet:Vers", "words": [{"surface",
  "lemma", "parsing", "pos", ...}]}`.
- **Károli-vers-megfeleltetéshez:** `db/seeds/mt_alignment/verse_pairs.jsonl`
  — a görög (LXX) vers és a héber/angol-KJV megfelelője, TVTMS-alapú, ~99,57%
  auditált pontossággal (a forrás saját auditja). sha256 (ezen a rögzített
  commiton letöltve): `3a91c571f1f32545f78397a256fdfa5124bcbcbc42902411a8a93209dcb2e985`
- **Licenc:** a `db/seeds/lxx_morph/` és `db/seeds/mt_alignment/` adat **CC BY
  4.0** (a kód ISC, de az adatra nem vonatkozik). A Rahlfs LXX (1935) szövege
  maga közkincs.
- **Forrásmegjelölés:** *lxx-morph, © Seth Kushniryk, CC BY 4.0,
  github.com/OpenScriptorium/lxx-morph.*

### Strong-szám: GreekWordList (Open Scriptures Septuagint Project)

- **Repó:** `github.com/openscriptures/GreekResources`
- **Rögzített commit:** `dd5a2fd530ab3c6b748c174cec38966c356d8111`
- **Fájl:** `GreekWordList.js` (JS-objektum, ékezet nélküli lemma-kulcs →
  `{lemma, strong, pos, ...}`). sha256: `84703d5de9fae423c141ff374ffab73fcda288d0a400fcd500445302a5dbe483`
- **Licenc:** CC BY 4.0.
- **Korlát (a forrás saját dokumentációja szerint):** „The Strong number is
  noted, for New Testament words" — csak azoknak a lemmáknak van
  Strong-száma, amelyek az ÚSZ-ben is előfordulnak. Sok tisztán LXX-only
  lemmának nincs — ez **nem hiba**, a forrás korlátja (l. `strong_ok`
  oszlop).

### Ellenőrző forrás (nem adatforrás): Open Scriptorium bulk SQLite

- **URL:** `https://openscriptorium.org/downloads/openscriptorium.sqlite3`
- **Letöltés dátuma:** 2026-09-22 · **Last-Modified (szerver):** 2026-04-11
- **sha256:** `a00a290e800231b91c0ee1a680fa1957fcb98eb48b86120ff7ab1002aaa9174a`
- **Licenc:** a `rahlfs-lxx` mű a benne lévő `licenses` tábla szerint Public
  Domain (`CC-PDDC`).
- **A repóba nem kerül** (339 MB). Kizárólag a `--sqlite-ellenoriz` opció
  használja, versenkénti szószám-összevetésre az lxx-morph adat ellen — nem
  adatforrás, csak kereszt-ellenőrzés. **Fontos korlát, ami a G4 v3
  módosítását kiváltotta:** ez az SQLite **nem tartalmaz lemma-táblát**, és a
  `words.strongs_number` mezője a teljes `rahlfs-lxx` műre üres (0/288 471
  sor) — emiatt nem használható elsődleges forrásként a lemma/Strong-adathoz,
  l. `LEXV2_1_BRIEF.md` döntésnapló v3.

## 2. Károli-vers-megfeleltetés (G5)

Az `igehely_karoli` oszlop **elsődleges forrása a repóban már meglévő
versifikációs infrastruktúra**, nem a `verse_pairs.jsonl`:

1. `konkordancia/LXX_versificacios_terkep.tsv` — a `Gorog_LXX_vers` (elsőként)
   és `Heber_vers` (másodikként) oszlop szerinti (fejezet,vers) → Károli-cél
   megfeleltetés (betöltve az `eszkozok/lxx_kivonat_fetch.py`
   `load_versifikacios_terkep()` függvényével — **ugyanaz a függvény, amit a
   régi `LXX_kivonat_*.tsv` is használ**).
2. `eszkozok/lxx_kivonat_fetch_v2.py` `KEZI_ELTOLASOK` — a Dániel 3/4,
   Numeri 12/13, Jób 38–40 és Prédikátor tartalmilag egyeztetett,
   dokumentált kézi eltolás-táblái (l. `LXX_kivonat_README.md` 4. szakasz).
3. **Identitás** — ha sem (1), sem (2) nem ad célt, és a nyers fejezet:vers
   Károli-címként létezik a `Karoli_1908.tsv`-ben, azt használjuk.
4. Ha egyik sem ad érvényes célt: `igehely_karoli` üres, `karoli_ok=szamozas_elteres`.

A `karoli_ok` oszlop egyéb értékei: `nincs_mt_parositas` (a `verse_pairs.jsonl`
szerint `method=unpaired`, azaz nincs héber/MT megfelelő — LXX-plusz),
`nincs_karoli_konyv` (deuterokanonikus/pszeudepigráf könyv, aminek nincs
Károli-szövege).

**A `verse_pairs.jsonl` `mt_refs` mezője csak az `igehely_kjv` oszlopba kerül**
(változtatás nélkül, angol/KJV-számozásban) és a `nincs_mt_parositas`
jelöléshez — **nem forrása** az `igehely_karoli`-nak.

### G5 ⛔ küszöb-mérés (a szükséges verseken)

A küszöb az `elofordulasok.tsv` ÓSZ-sorainak verseire vonatkozik (tartományoknál
minden versre kibontva), **nem a teljes korpuszra**:

| | Érték |
|---|---|
| szükséges vers | 229 |
| `igehely_karoli`-val | 214 |
| hiányzik | 15 (6,55%) |

A 15 hiányzó közül 12 Zsoltár (116, 42, 78, 107, 31, 55, 86, 89, 74 —
számozási eltérés, amit sem a térkép, sem a kézi táblák nem dokumentálnak),
1 Jób 17:16 (a `LXX_kivonat_README.md` szerint dokumentált, genuin LXX-plusz),
1 Péld 27:20, 1 Jer 51:46. **≤10% — a küszöb teljesül.**

A teljes korpuszon (nem a küszöb tárgya, csak tájékoztató): 30 186 vers,
ebből 21 952 `karoli_ok`, 1 167 `szamozas_elteres` (~5,1%), 146
`nincs_mt_parositas`, 7 071 `nincs_karoli_konyv` (deuterokanon/pszeudepigráf).

## 3. Fájlok és oszlopok

`konkordancia/LXX_OS/<könyv-slug>.tsv`, 59 fájl (a lxx-morph könyvlistája —
alternatív szövegtanúk külön fájlban: `joshua`/`joshua-vaticanus-b`,
`judges`/`judges-vaticanus-b`, `daniel`/`daniel-theodotion`,
`susanna`/`susanna-theodotion`, `bel-and-the-dragon`/`bel-and-the-dragon-theodotion`,
`tobit`/`tobit-sinaiticus`).

Fejléc: `igehely_lxx | igehely_kjv | igehely_karoli | karoli_ok | pozicio | szoalak | normalizalt | lemma | morf | strong | strong_ok | proveniencia`

- `igehely_lxx` — a könyv angol címe + a lxx-morph saját fejezet:vers címe.
- `igehely_kjv` — `verse_pairs.jsonl` `mt_refs`, `;`-vel, ha több.
- `igehely_karoli` / `karoli_ok` — l. 2. szakasz.
- `pozicio` — a szó 1-alapú sorszáma a versen belül.
- `szoalak` / `normalizalt` — az lxx-morph `surface`, illetve ékezet nélkülire
  normalizált (Unicode NFD + kombináló jelek eltávolítva, kisbetűs) alakja.
- `lemma` / `morf` — az lxx-morph `lemma`, illetve `pos`+`parsing` összefűzve.
- `strong` / `strong_ok` — a GreekWordList szerint; `strong_ok` üres, ha van
  Strong; `nincs_uszbeli_megfelelo`, ha a lemma megvan a GreekWordList-ben,
  de nincs Strong-száma; `lemma_nem_talalhato`, ha a lemma (ékezet nélküli
  alakja) egyáltalán nincs a GreekWordList-ben.
- `proveniencia` — `forras=lxx-morph@<commit> | forras=GreekWordList@<commit> | ts=<dátum>`.

### Sorszámok könyvenként (fejléc nélkül)

| Könyv | Sor |
|---|---|
| genesis | 32 566 |
| exodus | 24 763 |
| leviticus | 19 082 |
| numbers | 25 059 |
| deuteronomy | 22 990 |
| joshua | 1 034 |
| joshua-vaticanus-b | 14 439 |
| judges | 15 947 |
| judges-vaticanus-b | 15 580 |
| ruth | 2 072 |
| 1-samuel | 20 115 |
| 2-samuel | 17 914 |
| 1-kings | 18 688 |
| 2-kings | 18 781 |
| 1-chronicles | 16 247 |
| 2-chronicles | 21 040 |
| job-lxx | 13 291 |
| psalms-lxx | 34 951 |
| proverbs | 10 572 |
| ecclesiastes | 4 546 |
| song-of-solomon | 2 025 |
| isaiah | 27 076 |
| jeremiah-lxx | 28 952 |
| lamentations | 2 369 |
| ezekiel | 29 658 |
| daniel | 10 190 |
| daniel-theodotion | 10 453 |
| hosea | 3 933 |
| joel | 1 580 |
| amos | 3 210 |
| obadiah | 472 |
| jonah | 1 090 |
| micah | 2 368 |
| nahum | 937 |
| habakkuk | 1 105 |
| zephaniah | 1 223 |
| haggai | 947 |
| zechariah | 4 963 |
| malachi | 1 416 |
| tobit | 5 503 |
| tobit-sinaiticus | 7 233 |
| judith | 9 174 |
| esther-greek | 3 757 |
| wisdom | 6 943 |
| sirach | 18 658 |
| baruch | 2 608 |
| letter-of-jeremiah | 1 261 |
| susanna | 762 |
| susanna-theodotion | 1 134 |
| bel-and-the-dragon | 892 |
| bel-and-the-dragon-theodotion | 871 |
| 1-maccabees | 18 292 |
| 2-maccabees | 11 917 |
| 3-maccabees | 5 110 |
| 4-maccabees | 7 859 |
| 1-esdras | 8 996 |
| 2-esdras | 13 266 |
| psalms-of-solomon | 4 846 |
| odes | 4 147 |

Legnagyobb fájl: `psalms-lxx.tsv`, 8,8 MB (a K4 50 MB-os korlátja alatt).

## 4. Reprodukáló parancs

```bash
python eszkozok/lxx_os_import.py --letolt
```

(vagy `--forras <könyvtár>` egy már letöltött lxx-morph/GreekWordList/
verse_pairs.jsonl készletre; `--sqlite-ellenoriz` opcionálisan bekapcsolja a
bulk SQLite letöltését és a kereszt-ellenőrzést; `--konyvek <slug,slug,...>`
egy részhalmazra szűkít.)

## 5. Ismert korlátok

- A `strong` oszlop csak azoknál a szavaknál töltött ki, amelyek lemmája az
  ÚSZ-ben is előfordul (a GreekWordList forrás saját korlátja) — **üres
  `strong` nem hibás lelet**, a legtöbb tisztán ÓSZ-i lemmánál várt.
- A `karoli_ok=szamozas_elteres` fejezetek (teljes lista a szkript
  futásnaplójában) nem javítottak — ahol a `LXX_versificacios_terkep.tsv`
  vagy a `KEZI_ELTOLASOK` nem dokumentál megfeleltetést, a menet nem talál ki
  újat (`LEXV2_1_BRIEF.md` G5).
- A `Karoli_1908.tsv`-ben nem szereplő igehelyek (pl. deuterokanonikus
  toldalékok) `igehely_karoli`-ja mindig üres — ez a Károli-kánon
  szerkezetéből következik, nem hiba.
- Az SQLite-ellenőrzés 61 eltérést talált a teljes korpuszon (61/288 471 szó,
  ~0,02%) — túlnyomórészt kisebb tokenizálási különbségek és a Sirach előszó
  (`sirach 0:x`, amit a bulk SQLite egyáltalán nem tartalmaz), plusz néhány
  vers, ami a két forrás eltérő regenerálási dátuma miatt (SQLite:
  2026-04-11, lxx-morph commit: 2026-08-22) átmenetileg eltér. Nem blokkoló.
