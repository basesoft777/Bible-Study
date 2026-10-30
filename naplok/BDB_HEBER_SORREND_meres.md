# A BDB héber kifejezéseinek sorrend- és geres-hibája — mérés és javítási-szabály javaslat (N-F131y)

*2026-10-30. Csak mérés és javaslat: adat, forrás és lexikonlap nem változott. A javításról a felhasználó dönt (⛔).
Modell: `claude-opus-5-5`. Mérőszkript: `naplok/BDB_HEBER_SORREND_meres.py` (futás kb. 1,5 perc; a kézi mintát a
`--minta-ki <fájl>` kapcsolóval TSV-be is kiírja).*

*proveniencia: scope=DictBDB.json összes <heb> kifejezése (107 600) | forras=naplok/BDB_HEBER_SORREND_meres.py;
DictBDB.json@5d826c580a4d, BDB.lexicon@c998a70b432f, TAHOT_kivonat.tsv@4c876f570aad, bdb_szakaszok.tsv@66bd24b9abb6,
bdb_szakasz_hu.tsv@e2cb5e21e0c0, forditasok.tsv@8d3bc51a3690 | ts=2026-10-30*

## 1. Röviden

- **Hol keletkezik a hiba?** Már a nyers `DictBDB.json`-ban, két rétegben. A mi konverziónk (`_convert_bdb.py`, `bont.py`,
  `hu_illeszt.py`) a héber szöveget változatlanul továbbviszi, új hibát nem tesz hozzá.
  1. **Alsó réteg, a `BDB.lexicon` (ugyanannak a digitalizálásnak a régebbi alakja):** a héber kifejezést `<bdbheb>`
     darabokra bontva tárolja, a geres külön darab, és a darabok sorrendje gyakran a vizuális (jobbról balra olvasott)
     sorrend. Példa (H7121, Qal 2.c): `׳` · `בְּשֵׁם י` · ` ` · `׳` · `ק`. Ezt visszafelé olvasva kapjuk a nyomtatott BDB
     alakját: `ק׳ בְּשֵׁם י׳`.
  2. **Felső réteg, a `DictBDB.json`:** a készítője minden `<heb>` futam szóköz szerinti tokenjeit megfordította. A
     H1 hipotézis (*a JSON-kifejezés = a lexikon-darabok összefűzésének tokenjei fordított sorrendben*) a párosított
     99 262 tételből **99 262-n igaz** (100%). Ez a lépés a geres nélküli, több szavas kifejezéseket is megfordította,
     tehát **minden** több szavas héber kifejezés érintett, nem csak a rövidítést tartalmazók. Mellékes bizonyíték: a
     H8104 egyik lezáratlan `<heb>` eleménél az angol szöveg és a HTML is megfordult („Samuel 2 16:21; … concubines)
     David's (of”).
- **Az `entry` attribútum nem hordozza a helyes alakat:** a 107 600 tételből 1 kivételével betűre azonos a látható
  szöveggel (az egy kivétel a hibás H8104-elem).
- **Független, helyes sorrendű BDB-szöveg a repóban nincs.** A `BDB_teljes_unabridged.tsv` a `DictBDB.json` sima
  szövegű változata, az `OSHL_BDB_igehelyek.tsv` csak igehelyeket tartalmaz, maga az OpenScriptures-XML pedig nincs a
  repóban. Ellenőrzésre ezért a **héber Bibliát** (TAHOT) használom: a BDB kifejezései többnyire szó szerinti idézetek, így
  a két szórend közül az a helyes, amelyik a bibliai szövegben egymás után áll. Mellé egy 50 tételes, véletlen
  (seed 131) **kézi mintát** is adok (6. szakasz).
- **A javasolt szabály (R_hib)** a „tiszta” tételeken (írásjel és sziglum nélkül; 32 587 tétel) **98,5%-ban helyes** ott,
  ahol a Biblia dönteni tud (14 976 helyes, 224 rontott). 17 343 tételnél a Biblia nem dönt. A geres a javítás után
  32 584 tételben áll a betű után, 3-ban nem. Az írásjelet vagy sziglumot tartalmazó tételeken (3 713) a pontosság csak 62%,
  ezért **ezeket ne javítsuk gépileg**.
- **Hatás:** 34 279 változó kifejezés 5 880 Strongban. A `bdb_szakaszok.tsv` 13 738 / 36 621 sora, a
  `bdb_szakasz_hu.tsv` 4 359 / 9 664 sora és a `forditasok.tsv` 7 531 / 18 603 BDB-sora érintett (3 397 / 4 006
  lefordított Strong). A fordítás **szó szerint örökölte** a hibás héber alakot: a változó kifejezések 99,0%-a
  (29 480 / 29 789) betű szerint megvan a magyarban. **Újrafordítás nem kell**, elég a héber részlet cseréje.

## 2. Módszer

1. **Census a JSON-on.** A `<heb><ref0 entry="…">…</ref0></heb>` tételek: 107 600. A geres helye **csak a látható
   szövegben** (az `entry` attribútum nélkül): 15 298-szor áll a betű előtt, 173-szor utána, 1 213-szor máshol (szóköz
   vagy írásjel mellett). *Az N-F131x-ben szereplő 30 886 / 342 a teljes HTML-t számolta: ott az `entry` attribútum
   miatt minden kifejezés kétszer szerepel.*
2. **Párosítás a `BDB.lexicon`-nal.** Strongonként a `bdb_szakaszok.tsv` `bdb_id`-jai szerint, a szócikkek
   `<bdbheb>` csoportjaival (egymás utáni `<bdbheb>` elemek, köztük csak szóköz). A kulcs a tokenek mássalhangzó-vázának
   rendezett listája. A váz a pe/mem forráshibát (SEMA 2.31) egybeveszi. Eredmény: 99 262 párosított, 8 338 párosítatlan
   tétel; 17 223 tétel több darabból áll. **A lexikonból csak a darabhatár jön, szöveg nem** (DT225); a javított alak
   betűi mindig a JSON-éi.
3. **Szabályok** (a szkript docstringjében rögzítve):
   - `R0`: a JSON tokenfordításának visszacsinálása (a tokenek megfordítása);
   - `R_lex`: R0, majd a lexikon darabhatárai szerint a darabok megfordítása;
   - `R_str`: R0, majd darabolás csak a szöveg alapján (a geres, a geres melletti szóköz és a geres nélküli futam egy-egy
     darab), és a darabok megfordítása;
   - `R_lap`: a mai lapjavítás (`lexikon_general.bdb_rovidites_jelol`, PR #521): csak az önálló, egybetűs `׳X → X׳`;
   - **`R_hib` (javasolt):** geres nélküli kifejezésnél R0; geresnél R_lex, ha a lexikon szerkezete átvihető, különben
     R_str.
4. **Próba a héber Biblián.** A jelölt alakot mássalhangzó-vázra bontjuk (a teljes szavak egymás után, a rövidítés a
   betűi után legfeljebb 8 betűnyi réssel, az ellipszis legfeljebb 60 betűnyi réssel). Utána megnézzük, hogy egy TAHOT-vers
   vázfolyamában előfordul-e. Ítélet: `helyes` (a jelölt alak előfordul, a JSON-alak nem), `rontott` (fordítva),
   `eldonthetetlen` (mindkettő vagy egyik sem fordul elő, vagy nincs elég anyag: legalább egy teljes szó és még egy egység
   kell).
5. **Ortográfiai próba.** A geres a héberben mindig a rövidített betű (betűsor) után áll. Megnézzük, hogy a javítás után
   minden geres betű vagy pontozás után áll-e.

## 3. A hiba keletkezése egy példán (H7121, Qal 2.c)

| Réteg | Alak |
|---|---|
| a nyomtatott BDB (a felhasználó szerint) | `ק׳ בְּשֵׁם י׳` („hívni Jahve nevével”) |
| `BDB.lexicon` darabjai | `׳` · `בְּשֵׁם י` · ` ` · `׳` · `ק` (vizuális darabsorrend) |
| ezek összefűzve | `׳בְּשֵׁם י ׳ק` |
| `DictBDB.json` (szöveg és `entry` is) | `׳ק י ׳בְּשֵׁם` (az előző tokenjei megfordítva) |
| `bdb_szakaszok.tsv`, `forditasok.tsv` | `׳ק י ׳בְּשֵׁם` (változatlanul átvéve; a magyarban: „hívni ׳י nevével”) |
| R_hib | `ק׳ בְּשֵׁם י׳` ✔ |

A lap egyik példája (H8034): JSON `שׁ ׳לְמֵעַן` → R_hib `לְמֵעַן שׁ׳` („lemaʿan š.”, „az ő nevéért”). A `׳לְשׁ` típusú
egytokenes alakot (prefixum + rövidítés) az R_str/R_hib `לְשׁ׳`-re fordítja.

## 4. A mérés táblázata

### 4.1 Kategóriánként (R_hib; a Biblia ítélete)

| Kategória (a JSON-alak szerint) | Tétel | helyes | rontott | eldönthetetlen | pontosság (h / h+r) |
|---|---:|---:|---:|---:|---:|
| egy szó, geres nélkül (nem érintett) | 71 300 | — | — | — | változatlan |
| egybetűs rövidítés (`׳י`) | 4 288 | — | — | 4 288 | a Biblia nem dönt; ortográfiailag mind helyes |
| egy token geressel, több betű (`׳לְשׁ`) | 1 301 | — | — | 1 297 | a Biblia nem dönt; ortográfiai próba |
| rövidítés + szó | 6 796 | 1 314 | 39 | 5 443 | 97,1% |
| három+ token geressel | 3 506 | 1 729 | 30 | 1 747 | 98,3% |
| két szó, geres nélkül | 13 587 | 7 611 | 229 | 5 733 | 97,1% |
| három+ szó, geres nélkül | 6 822 | 4 460 | 10 | 2 322 | 99,8% |

Összesítve (a nem érintett egyszavas tételek nélkül): **tiszta** (írásjel és sziglum nélkül) 32 587 tétel: 14 976
helyes, 224 rontott (**98,5%**), 17 343 eldönthetetlen, rossz helyen maradt geres 3. **Írásjellel vagy sziglummal**
(`,;.:`, `ᵐ5`, `ᵑ7`, számok) 3 713 tétel: 138 helyes, 84 rontott (**62%**), rossz helyen maradt geres 86.

### 4.2 A szabályok összevetése

| Szabály | rövidítés + szó: h / r | három+ token geressel: h / r | két szó: h / r | geres a betű után (15 891 geres tétel) |
|---|---|---|---|---|
| R_lap (a mai lap) | szórendhez nem nyúl | szórendhez nem nyúl | szórendhez nem nyúl | 7 909 jó / 7 982 rossz |
| R0 | 1 530 / 1 046 | 910 / 130 | 7 611 / 229 | 142 / 15 749 |
| R_lex | 1 277 / 34 (+32 nem átvihető) | 1 671 / 20 (+56) | 6 733 / 135 (+910) | 15 132 / 2 (nem átvihető kimarad) |
| R_str | 1 321 / 51 | 1 733 / 33 | 7 611 / 229 | 15 801 / 90 |
| **R_hib** | **1 314 / 39** | **1 729 / 30** | **7 611 / 229** | **15 802 / 89** |

Ahol az R_str és az R_lex eltér (2 410 párosított tétel):
- **geres nélkül:** az R0 / R_str 1 455 helyes / 18 rontott, az R_lex 9 / 1, és 829 esetben a JSON-alakot hagyja. A
  lexikon geres nélküli, szóközzel tagolt darabjai tehát logikai sorrendben állnak, a megfordításuk ront (pl. H6
  `לִנְתוֺשׁ וְלִנְתוֺץ`, Jer 1:10). Ezért geres nélkül az R_hib R0-t használ.
- **geresnél** a lexikon darabhatára a jobb: pl. H6 `א׳ חָסִיד מִןהָֿאָרֶץ` (Mik 7:2; az R_str szerint
  `א׳ מִןהָֿאָרֶץ חָסִיד`), H60 `בּ׳ מִשְׁתֶּה` (R_str: `בּ מִשְׁתֶּה׳`). A geres helye R_lex-szel 2 kivétellel jó, R_str-rel 90-nél rossz.

### 4.3 Jelzők (átfedő csoportok; R_hib, h / r / eldönthetetlen)

| Jelző | Tétel | R_hib |
|---|---:|---|
| makkef U+05BE | 11 | 0 / 0 / 6 (5 változatlan) |
| **rafe U+05BF mint makkef-pótló** (két szó egybeírva, pl. `מִןהָֿאָרֶץ` = מִן־הָאָרֶץ) | 5 589 | 1 902 / 21 / 1 382 |
| névelő (`הַ`, `הָ`, `הֶ` szókezdet) | 5 615 | 2 292 / 27 / 1 408 |
| ellipszis (`֗֗֗`, a forrás „…”-je) | 396 | 92 / 2 / 246 |
| írásjel a futamban (`,;.:`) | 2 434 | 94 / 79 / 2 257 |
| szám vagy latin betű (sziglum: `ᵐ5`, `ᵑ7`) | 5 395 | 51 / 8 / 1 354 (3 982 változatlan) |

### 4.4 Hibatípusok, amelyeket a szabály nem old meg

1. **A forrás eredendő következetlensége (kb. 1,5%).** A lexikon egyes kifejezéseket már logikai sorrendben tárolt, ezeket
   a JSON készítője „rontotta el” a megfordítással, mi pedig visszafordítjuk. A Biblia szerint ilyen a 224 tiszta
   `rontott` tétel, pl. H205 `בֵּית אָוֶן`, H314 `הַיָּם הָאַחֲרוֺן`: ezeknél a JSON-alak a helyes. Determinisztikusan csak a
   Biblia-próbával szűrhetők. A Biblia által nem látott ilyen hibák aránya ismeretlen; a kézi minta 12. sora ilyen
   (`מִלֵּא בָתֵּיהֶם ט׳`, Jób 22:18, az R_hib szerint `בָתֵּיהֶם ט׳ מִלֵּא`).
2. **Írásjel és sziglum a futamban.** Egy `<heb>` futam több, vesszővel elválasztott kifejezést vagy a latin
   sziglumot is tartalmazza (pl. H430: tíz istennév-formula egy futamban; H374 `מֹאזְנֵי צ׳, אַבְנֵי־צ׳, הִין צ׳`, Lev 19:36).
   A tokenfordítás itt az írásjelet is áthelyezte, a vessző a rossz kifejezéshez tapad. Pontosság 62%: kézi javítás kell.
3. **Rafe mint makkef (5 589 tétel)** — külön forráshiba, nem sorrendi: a makkef helyén a két szó egybe van írva, a rafe
   (U+05BF) a második szó első betűjén áll. A szórend-javítás nem nyúl hozzá; a megjelenítésben `־`-re kellene bontani.
   Külön mérendő.

## 5. Hatás

| Tábla | Érintett | Megjegyzés |
|---|---|---|
| `DictBDB.json` → változó kifejezés (R_hib ≠ JSON) | 34 279 kifejezés, 5 880 Strong | Strongonként egyedi alakok |
| `adat/bdb_szakaszok.tsv` | 13 738 / 36 621 sor (5 880 Strong) | a `szoveg` a nyers JSON-szöveget hordozza |
| `adat/bdb_szakasz_hu.tsv` | 4 359 / 9 664 sor | a hibás héber alak szó szerint áll a `szoveg_hu`-ban |
| `adat/forditasok.tsv` (BDB) | 7 531 / 18 603 sor; 3 397 / 4 006 Strong; 34 792 szó szerinti előfordulás | a változó kifejezések 99,0%-a (29 480 / 29 789) betű szerint megvan a magyarban |

**A fordítást a javítás érinti, de újrafordítást nem igényel.** A fordító a héber részletet változatlanul bemásolta
(„hívni ׳י nevével”), a magyar mondat pedig az angol glosszát követi, nem a héber szórendet. A csere tehát
determinisztikus: a régi héber alak helyére az új kerül. A maradék 1% (309 kifejezés) nem található meg szó szerint a
magyarban: ott a fordító átírta vagy szétszedte, ezeket kézzel kell átnézni.

Mellékhatások, amelyekről dönteni kell:
- **Elavulás-jel:** a `forditas_forras_hash` a forrásnézet hash-e. Ha a nézet a javítással együtt hash-elődik, minden
  érintett fordítás „elavult” lesz. Javaslat: a héber csere a nézetben és a fordítás megjelenítésében egyformán fusson,
  és a hash az eddigi nézetet kövesse (vagy legyen külön, verziózott).
- **A pe/mem javítás kulcsa** (`bdb_forras_javitas.tsv`, `szo_sorszam`) a héber szavak sorszáma a `szoveg`-ben. A
  szórend-csere ezt eltolná, ezért a pe/mem javítást **előbb** kell alkalmazni, a sorrendet utána.
- **A lap rövidítés-jelölője** (`bdb_rovidites_jelol`, PR #521) a `׳X` alakot keresi. A javítás után `X׳` alakot kell
  keresnie (és az N-F131x olvasó-szerveri változata is így készüljön).

## 6. Kézi minta (seed 131; 50 tétel a 36 300 geres- vagy több tokenes tételből)

A „kézi ítélet” oszlop a felhasználóé (helyes / rossz / nem tudom). A „héber Biblia” oszlop a 2.4 próba ítélete az
R_hib-alakra; a „lexikon” azt mutatja, hogy a tétel párosult-e a `BDB.lexicon`-nal. Újragenerálás:
`python naplok/BDB_HEBER_SORREND_meres.py --minta-ki <fájl>` (a minta a seed miatt azonos).

| # | Strong | kategória | jelzők | JSON-alak | javasolt (R_hib) | héber Biblia | lexikon | kézi ítélet |
|---|---|---|---|---|---|---|---|---|
| 1 | H5051 | ket_szo |  | חִצֶּיךָ אוֺר | אוֺר חִצֶּיךָ | helyes | igen |  |
| 2 | H5869 | ket_szo |  | יַעֲקֹב עֵין | עֵין יַעֲקֹב | eldonthetetlen | igen |  |
| 3 | H8076 | egybetus_rovidites |  | ׳שׁ | שׁ׳ | eldonthetetlen | igen |  |
| 4 | H1755 | harom_plusz_szo |  | וָדוֺר דּוֺר שְׁנֵי | שְׁנֵי דּוֺר וָדוֺר | helyes | igen |  |
| 5 | H6098 | ket_szo | irasjel | תּוֺרָה דָּבָר, | דָּבָר, תּוֺרָה | eldonthetetlen | nem |  |
| 6 | H4591 | harom_plusz_szo |  | יִמְעָ֑ט מֵהֶבֶל הוֺן | הוֺן מֵהֶבֶל יִמְעָ֑ט | helyes | igen |  |
| 7 | H389 | ket_szo | nevelo | הַמַּעַם אַךְ | אַךְ הַמַּעַם | helyes | igen |  |
| 8 | H6059 | harom_plusz_szo | nevelo | לוֺ תַּעֲנִיק הַעֲנֵיק | הַעֲנֵיק תַּעֲנִיק לוֺ | helyes | igen |  |
| 9 | H2119 | egybetus_rovidites |  | ׳י | י׳ | eldonthetetlen | igen |  |
| 10 | H5578 | ket_szo |  | סוּסָה חֲצַר | חֲצַר סוּסָה | helyes | igen |  |
| 11 | H1931 | ket_szo |  | פְרָת הוּא | הוּא פְרָת | eldonthetetlen | igen |  |
| 12 | H2896 | harom_plusz_token_geressel |  | ט ׳בָתֵּיהֶם מִלֵּא | בָתֵּיהֶם ט׳ מִלֵּא | eldonthetetlen | igen |  |
| 13 | H3629 | ket_szo | irasjel | כְּלוּלָה כַּלָּה, | כַּלָּה, כְּלוּלָה | eldonthetetlen | nem |  |
| 14 | H9009 | ket_szo |  | מֵאֲרֻבָּה כְּעָשָׁן | כְּעָשָׁן מֵאֲרֻבָּה | helyes | igen |  |
| 15 | H6999 | ket_szo |  | הגבעות על | על הגבעות | helyes | igen |  |
| 16 | H7754 | ket_szo |  | עֵצִים שׂוֺכַת | שׂוֺכַת עֵצִים | helyes | igen |  |
| 17 | H3368 | ket_szo |  | וְקָרוֺת חוֺם | חוֺם וְקָרוֺת | eldonthetetlen | igen |  |
| 18 | H3651 | ket_szo |  | יַאֲרִיךְ כֵּן | כֵּן יַאֲרִיךְ | helyes | igen |  |
| 19 | H9004 | ket_szo |  | חֳדָשִׁים כְּמִשְׁלשׁ | כְּמִשְׁלשׁ חֳדָשִׁים | helyes | igen |  |
| 20 | H1004 | harom_plusz_token_geressel | nevelo | ׳בּ הַיַּיִן מִשְׁתֵּה | בּ׳ מִשְׁתֵּה הַיַּיִן | helyes | igen |  |
| 21 | H2834 | rovidites_es_szo |  | ׳ח יְעָרוֺת | ח׳ יְעָרוֺת | eldonthetetlen | igen |  |
| 22 | H7161 | harom_plusz_szo |  | לוֺ מִיָּדוֺ קַרְנַיִם | קַרְנַיִם מִיָּדוֺ לוֺ | helyes | igen |  |
| 23 | H3458 | harom_plusz_token_geressel |  | י ׳שָׁמַע ׳רגו | שָׁמַע י׳ רגו׳ | eldonthetetlen | igen |  |
| 24 | H6873 | egybetus_rovidites |  | ׳י | י׳ | eldonthetetlen | igen |  |
| 25 | H1288 | rovidites_es_szo |  | ׳ב צוּרִי | ב׳ צוּרִי | eldonthetetlen | igen |  |
| 26 | H227 | harom_plusz_szo |  | לוֺ טוֺב אָז | אָז טוֺב לוֺ | helyes | igen |  |
| 27 | H7919 | ket_szo |  | חָכָם לֵב | לֵב חָכָם | eldonthetetlen | igen |  |
| 28 | H4285 | egybetus_rovidites |  | ׳מ | מ׳ | eldonthetetlen | igen |  |
| 29 | H6921 | rovidites_es_szo |  | (הַ)קּ ׳רוּחַ | רוּחַ (הַ)קּ׳ | helyes | igen |  |
| 30 | H1755 | harom_plusz_szo |  | וָדוֺר דּוֺר מְשׂוֺשׂ | מְשׂוֺשׂ דּוֺר וָדוֺר | helyes | igen |  |
| 31 | H2568 | egybetus_rovidites |  | ׳ח | ח׳ | eldonthetetlen | igen |  |
| 32 | H1288 | ket_szo |  | ברוך מברכך | מברכך ברוך | eldonthetetlen | igen |  |
| 33 | H2786 | harom_plusz_token_geressel |  | ׳ח על שׁניו | ח׳ שׁניו על | eldonthetetlen | igen |  |
| 34 | H1818 | harom_plusz_szo | nevelo | יְכַמֵּר בַּנֶּפֶשׁ הוּא הַדָּם | הַדָּם הוּא בַּנֶּפֶשׁ יְכַמֵּר | helyes | igen |  |
| 35 | H5892 | ket_szo | szam_latin,nevelo | ᵐ5 הַשֵּׁעַר | הַשֵּׁעַר ᵐ5 | eldonthetetlen | igen |  |
| 36 | H2094 | rovidites_es_szo |  | י ׳מִשְׁמְּטֵי | מִשְׁמְּטֵי י׳ | eldonthetetlen | igen |  |
| 37 | H9003 | ket_szo |  | בְּ חָלַק | חָלַק בְּ | eldonthetetlen | igen |  |
| 38 | H5920 | ket_szo |  | בֵּין עַל | עַל בֵּין | eldonthetetlen | igen |  |
| 39 | H3427 | harom_plusz_szo | rafe_makkef,nevelo | הַחֲמוֺר עִםֿ מֹּה לָכֶם שְׁבוּ | שְׁבוּ לָכֶם מֹּה עִםֿ הַחֲמוֺר | helyes | igen |  |
| 40 | H2689 | rovidites_es_szo |  | ׳ח התרועה | ח׳ התרועה | eldonthetetlen | igen |  |
| 41 | H7832 | rovidites_es_szo |  | י ׳לִפְנֵי | לִפְנֵי י׳ | eldonthetetlen | igen |  |
| 42 | H5360 | rovidites_es_szo |  | נ ׳עשׂה | עשׂה נ׳ | eldonthetetlen | igen |  |
| 43 | H615 | rovidites_es_szo | nevelo | ׳א הַתִּקְוָה | א׳ הַתִּקְוָה | eldonthetetlen | igen |  |
| 44 | H2873 | ket_szo | irasjel | טִבְחָה טֶבַח, | טֶבַח, טִבְחָה | eldonthetetlen | nem |  |
| 45 | H7218 | ket_szo | nevelo | הַכֹּהֲנִים רָאשֵׁי | רָאשֵׁי הַכֹּהֲנִים | helyes | igen |  |
| 46 | H4500 | ket_szo |  | אֹרְגִים כִּמְנוֺר | כִּמְנוֺר אֹרְגִים | helyes | igen |  |
| 47 | H249 | ket_szo | nevelo | הָאָרֶץ אֶזְרַח | אֶזְרַח הָאָרֶץ | helyes | igen |  |
| 48 | H58 | ket_szo |  | מִצְרַיִם אָבֵל | אָבֵל מִצְרַיִם | helyes | igen |  |
| 49 | H6946 | rovidites_es_szo |  | ׳ק בַּרְנֵעַ | ק׳ בַּרְנֵעַ | eldonthetetlen | igen |  |
| 50 | H2506 | harom_plusz_token_geressel |  | בְּח ׳הַשָּׂדֶה ׳יִזְ | הַשָּׂדֶה בְּח׳ יִזְ׳ | helyes | igen |  |

*Megfigyelés a mintán (értelmezés, nem lekérdezés):* a 12. sor (H2896) az R_hib szerint `בָתֵּיהֶם ט׳ מִלֵּא`, a Jób 22:18
szerint viszont `מִלֵּא בָתֵּיהֶם ט׳` a helyes, és a Biblia-próba ezt nem látta (eldönthetetlen). Ez a 4.4/1. típusba tartozik.

## 7. Javaslat (döntés: a felhasználóé, ⛔)

1. **Ne írjuk át a nyers forrást és a `bdb_szakaszok.tsv`-t.** A javítás a meglévő javítótábla-minta szerint menjen
   (DT231 (d), SEMA 2.31): új hibaosztály, pl. `heber_sorrend`, a `bdb_forras_javitas.tsv`-ben (generált,
   `forras_javit.py`), `forras_alak` → `javitott_alak` párokkal. A szöveg-nézet (`nezet_general.py`,
   `szakasz_bemenet.py`) a pe/mem után alkalmazza.
2. **Gépi javítás (`javitva`) csak a tiszta tételekre**, R_hib szerint, **Biblia-vétóval**: ahol a Biblia szerint a
   JSON-alak a helyes (`rontott`), ott a JSON-alak marad (`valodi_sorrend`). A Biblia-próba determinisztikus, a sor
   indoklásába beírható. Az írásjeles és sziglumos tételek (3 713) `jelolt_marad`, ezeket kézzel kell átnézni.
3. **A fordításon** ugyanez a csere megjelenítéskor fusson (a magyar szövegben betű szerint keresve, 99,0% lefedés),
   újrafordítás nélkül. A 309 nem talált kifejezés kézi lista legyen. A hash kérdéséről (5. szakasz) külön kell dönteni.
4. **A `bdb_rovidites_jelol` átállítása** a javított `X׳` alakra, a lap újragenerálásával együtt (N-F131x-szel közösen).
5. **Előtte:** a 6. szakasz kézi mintájának átnézése. Ha a kézi pontosság a tiszta tételeken eléri a mért kb. 98%-ot,
   mehet a gépi javítás; ha nem, a mintán talált hibatípus szerint pontosítani kell a szabályt.
6. A rafe mint makkef (4.4/3.) külön, kisebb tétel legyen.
