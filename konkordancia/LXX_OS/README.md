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

## 2. Károli-vers-megfeleltetés (G5, V1.3b)

**V1.3a (2026.09.22) — a V1.3 első változata a régi
`LXX_versificacios_terkep.tsv`-t használta elsődleges forrásként; ez hibás
volt.** A térkép a studybible.info saját belső oldal-verzőszámozására épült
(pl. a Zsoltár-feliratoknál más granularitással bontja a LXX-verseket, mint
az lxx-morph), ezért a raw (fejezet,vers) kulcsai NEM esnek egybe az
lxx-morph saját `ref`-jeivel — a két forrás összekeverése rendszeresen rossz
Károli-célt adott (pl. LXX(Zsolt) 50:3 → hibásan "Zsolt 50:3" a helyes
"Zsolt 51:3" helyett). A térkép ezért **teljesen kikerült** az
`igehely_karoli` számításából (l. `LEXV2_1_BRIEF.md` döntésnapló v4).

**V1.3b (2026.09.25, `KAROLI_KULCS_BRIEF.md` KK4) — a KK1/KK1b-menet
(`claude/karoli-kulcs-35158` ág) feltárta, hogy a V1.3a algoritmus két
ponton rendszeresen elvesztette a valódi Károli-célt** (l.
`naplok/KAROLI_KK1_jelentes.md`, `naplok/KAROLI_KK1b_hatas.md`):

- **H1 — a `KEZI_ELTOLASOK`-függvény `None`-ja tévesen "nem az én
  hatáskörömbe tartozik"-ként lett kezelve**, a fejezet-szintű
  versszám-őrre esett vissza, ami a teljes fejezetet elvesztette akkor
  is, ha csak a fejezet VÉGE volt eltolva (pl. Jób 38:1–38 valójában
  változatlan, csak a 38:39–41 tolódik át a 39. fejezetbe — a régi kód
  emiatt Jób 38:1–38-at is `szamozas_elteres`-nek jelölte).
- **H2 — a Károli sok könyvben/fejezetben a héber (MT) versszámozást
  követi, nem a KJV-t** (pl. egész Jónás könyve, Ézsaiás 63, Józsué 13),
  amit a régi algoritmus egyáltalán nem ismert fel — csak a KJV-egyezést
  és a Zsoltár-cím speciális esetét vizsgálta.

Az új (V1.3b) algoritmus egy külön, **`konkordancia/Karoli_versmegfeleltetes.tsv`**
kulcstáblára épül (939 fejezet-osztályozás alapján generálva — l.
`naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv` és `naplok/KAROLI_KK4_tabla_veglegesit.py`):

1. **A kulcstábla raw-alapú (KEZI-osztályú) sorai** — a `KEZI_ELTOLASOK`
   ténylegesen érintett fejezeteinek MINDEN verse (a shiftelt ÉS a
   változatlan is), elsőbbséget élveznek.
2. **`eszkozok/lxx_kivonat_fetch_v2.py` `KEZI_ELTOLASOK`** — közvetlen
   hívás tartalék, ha a fenti táblában nincs a nyers (fejezet,vers)-hez
   sor, de a fejezet a függvény tényleges hatáskörében van, a `None` most
   már **identitást** jelent (H1 javítása), nem továbblépést.
3. **A kulcstábla KJV/MT-alapú sorai** — mind a `KJV`-osztályú (Károli =
   KJV), mind az **új `MT`-osztályú** (Károli = héber/MT-számozás, H2
   javítása) fejezetek soraira, elsőbbséget kapnak a régi fejezet-szintű
   versszám-őrrel szemben. Az `MT`-osztályú sikeres sorok `karoli_ok`
   értéke `mt_szamozas_kovetes` (megkülönböztetve a sima sikertől, de a
   lexikon-generátor szempontjából ugyanúgy "kitöltött" sor).
4. **Régi fejezet-szintű versszám-egyezés/Zsoltár cím-eltolás** — csak a
   kulcstábla által NEM fedett fejezetekre marad tartalék (elsősorban a
   13 `EGYIK_SEM`-osztályú fejezetre, amiket a KK1b szándékosan üresen
   hagyott, F3 szerint — ezek a KK2b menet tárgyai).
5. Minden más eltérés: `igehely_karoli` üres, `karoli_ok=szamozas_elteres`.

A `karoli_ok` oszlop egyéb értékei: `nincs_mt_parositas` (a `verse_pairs.jsonl`
szerint `method=unpaired`, azaz nincs héber/MT megfelelő — LXX-plusz),
`nincs_karoli_konyv` (deuterokanonikus/pszeudepigráf könyv, aminek nincs
Károli-szövege).

**Automatikus ellenőrzés** (a szkript minden futáskor lefuttatja): minden
kitöltött sorban a Károli-fejezet-szám egyezik a KJV-fejezet-számmal, kivéve
a `KEZI_ELTOLASOK` dokumentált eseteit — eltérés esetén a szkript figyelmeztet
(`K6-ELLENORZES`).

**Tartalmi szúrópróba** (a 4, korábban hibásan felismert eset + egy minta
könyvenként a szükséges versek közül — görög kezdőszavak / Károli-szöveg):

| Károli-igehely | LXX-igehely | Görög (részlet) | Károli-szöveg (részlet) |
|---|---|---|---|
| Zsolt 51:3 | Psalms (LXX) 50:3 | Ἐλέησόν με… | Könyörülj rajtam én Istenem… |
| Zsolt 3:2 | Psalms (LXX) 3:2 | Κύριε… | Uram! mennyire megsokasodtak ellenségeim!… |
| Jóel 2:1 | Joel 2:1 | σαλπίσατε… | (2:1, harsonaszó — egyezik) |
| Jer 9:24 | Jeremiah (LXX) 9:23 | ἀλλ᾿… | (9:24 — egyezik) |
| 1Móz 14:18 | Genesis 14:18 | Μελχισεδεκ βασιλεὺς Σαλημ… | Melkhisédek pedig Sálem királya… |
| 2Móz 19:6 | Exodus 19:6 | βασίλειον ἱεράτευμα… | papok birodalma és szent nép… |
| 4Móz 16:30 | Numbers 16:30 | ἐν φάσματι δείξει κύριος… | ha az Úr valami új dolgot cselekszik… |
| 5Móz 8:7 | Deuteronomy 8:7 | ὁ κύριος ὁ θεός σου εἰσάγει σε… | az Úr, a te Istened jó földre visz be… |
| Józs 12:4 | Joshua (Vaticanus B) 12:4 | Ωγ βασιλεὺς Βασαν… | Ógnak, a Básán királyának… |
| 1Sám 2:6 | 1 Samuel 2:6 | κύριος θανατοῖ καὶ ζωογονεῖ… | Az Úr öl és elevenít… |
| 2Sám 22:6 | 2 Samuel 22:6 | ὠδῖνες θανάτου ἐκύκλωσάν με… | A pokol kötelei vettek körül… |
| 1Kir 18:24 | 1 Kings 18:24 | βοᾶτε ἐν ὀνόματι θεῶν ὑμῶν… | hívjátok segítségül a ti istenteknek nevét… |
| 2Kir 5:11 | 2 Kings 5:11 | ἐθυμώθη Ναιμαν… | megharaguvék Naámán… |
| 1Krón 16:8 | 1 Chronicles 16:8 | ἐπικαλεῖσθε αὐτὸν ἐν ὀνόματι αὐτοῦ… | hívjátok segítségül az ő nevét… |
| Jób 28:14 | Job (LXX) 28:14 | ἄβυσσος εἶπεν οὐκ ἔστιν ἐν ἐμοί… | A mélység azt mondja: Nincsen az bennem… |
| Péld 3:20 | Proverbs 3:20 | ἐν αἰσθήσει ἄβυσσοι ἐρράγησαν… | tudománya által fakadtak ki a mélységből a vizek… |
| Préd 9:10 | Ecclesiastes 9:8 (kézi eltolás) | ἱμάτιά σου λευκά… | ruháid mindenkor legyenek fejérek… |
| Én 8:6 | Song of Solomon 8:6 | θές με ὡς σφραγῖδα… | Tégy engem mintegy pecsétet… |
| Ézs 12:4 | Isaiah 12:4 | ὑμνεῖτε κύριον… | magasztaljátok az Ő nevét… |
| Jer 10:25 | Jeremiah (LXX) 10:25 | ἔκχεον τὸν θυμόν σου ἐπὶ ἔθνη… | Öntsd ki haragodat ama nemzetekre… |
| Ez 26:19 | Ezekiel 26:19 | τάδε λέγει κύριος κύριος… | azt mondja az Úr Isten… |
| Hós 4:1 | Hosea 4:1 | ἀκούσατε λόγον κυρίου… | Halljátok meg az Úrnak beszédét… |
| Ámós 7:4 | Amos 7:4 | ἔδειξέν μοι κύριος καὶ ἰδοὺ… | Ily dolgot láttatott velem az Úr Isten… |
| Mik 6:12 | Micah 6:12 | τὸν πλοῦτον αὐτῶν ἀσεβείας ἔπλησαν… | a gazdagok megtöltöztek köztök ragadománynyal… |
| Jón 3:8 | Jonah 3:8 | περιεβάλοντο σάκκους οἱ ἄνθρωποι… | öltözzenek zsákba az emberek és barmok… |
| Hab 3:10 | Habakkuk 3:10 | ὄψονταί σε καὶ ὠδινήσουσιν λαοί… | Látnak téged és megrendülnek a hegyek… |
| Sof 3:9 | Zephaniah 3:9 | μεταστρέψω ἐπὶ λαοὺς γλῶσσαν… | változtatom majd a népek ajkát tisztává… |
| Zak 6:13 | Zechariah 6:13 | λήμψεται ἀρετὴν καὶ καθίεται… | megépíteni az Úrnak templomát… |

Mind a 27 minta tartalmilag egyezik (tulajdonnevek és kulcsszavak: Μελχισεδεκ
= Melkhisédek, Σαλημ = Sálem, Ναιμαν = Naámán, Ωγ βασιλεὺς Βασαν = Ógnak, a
Básán királyának stb.).

**A `verse_pairs.jsonl` `mt_refs` mezője csak az `igehely_kjv` oszlopba kerül**
(változtatás nélkül, angol/KJV-számozásban) és a `nincs_mt_parositas`
jelöléshez — **nem forrása** az `igehely_karoli`-nak.

### G5 ⛔ küszöb-mérés (a szükséges verseken)

A küszöb az `elofordulasok.tsv` ÓSZ-sorainak verseire vonatkozik (tartományoknál
minden versre kibontva), **nem a teljes korpuszra**:

| | Érték |
|---|---|
| szükséges vers | 229 |
| `igehely_karoli`-val | 218 |
| hiányzik | 11 (4,80%) |

A 11 hiányzó: Jób 17:13, 17:16, 38:7, 38:16, 38:30 (5 — az itt is dokumentált,
genuin LXX-plusz/számozás-eltérés, l. `LXX_kivonat_README.md`), Ézs 63:13,
Jón 2:3, 2:6, Hós 13:14, Józs 13:12, Jer 51:46 — mindegyik egyedi, könyv-
specifikus eltérés, amit a `KEZI_ELTOLASOK` nem fed le. **≤10% — a küszöb
teljesül.** (A V1.3 első, hibás verziójában 15/229 = 6,55% volt — a javítás
után a Zsoltár-verseknél teljes lefedettség lett.)

A teljes korpuszon (nem a küszöb tárgya, csak tájékoztató, `testament=ot`
könyvekre): 23 119 vers, ebből 21 121 `karoli_ok` + 983
`zsolt_felirat_eltolas` (össz. 22 104, ~95,6%), 1 015 `szamozas_elteres`
(~4,4%), 146 `nincs_mt_parositas`. A deuterokanonikus/pszeudepigráf könyvek
(7 071 vers) mindig `nincs_karoli_konyv`.

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
  futásnaplójában) nem javítottak — ahol sem a `KEZI_ELTOLASOK`, sem a
  KJV-fejezet-egyezés (sem a Zsoltár cím-eltolás), a menet nem talál ki újat
  (`LEXV2_1_BRIEF.md` G5, V1.3a).
- A `Karoli_1908.tsv`-ben nem szereplő igehelyek (pl. deuterokanonikus
  toldalékok) `igehely_karoli`-ja mindig üres — ez a Károli-kánon
  szerkezetéből következik, nem hiba.
- Az SQLite-ellenőrzés 61 eltérést talált a teljes korpuszon (61/288 471 szó,
  ~0,02%) — túlnyomórészt kisebb tokenizálási különbségek és a Sirach előszó
  (`sirach 0:x`, amit a bulk SQLite egyáltalán nem tartalmaz), plusz néhány
  vers, ami a két forrás eltérő regenerálási dátuma miatt (SQLite:
  2026-04-11, lxx-morph commit: 2026-08-22) átmenetileg eltér. Nem blokkoló.
