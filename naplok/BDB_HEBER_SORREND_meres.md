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
- **A felhasználó „angol szórend” hipotézise (8. szakasz):** a geres nélküli futamokra igaz (a szavak megfordítása
  98,6%-ban helyes). A geresszel álló futamokra nem igaz: a rendszeres vizuális → logikai konverzió ott csak 67,4%-ban
  helyes. Ezért **forráshibáról van szó, nem megjelenítési különbségről.**
- **A futam utáni igehely (9. szakasz, az olvasó lelete):** ez külön, megjelenítési hiba, és a mi konverziónk okozza. A forrás minden futam után LRM-et tesz, a `sima()` kiveszi; 18 173 futam után áll szám. Ezt nem a sorrend-javítás, hanem a héber futam izolálása oldja meg a megjelenítésben.
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

| # | Strong | kategória | jelzők | JSON-alak | javasolt (R_hib) | héber Biblia | lexikon | R_ang (8. szakasz) | kézi ítélet |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H5051 | ket_szo |  | חִצֶּיךָ אוֺר | אוֺר חִצֶּיךָ | helyes | igen | = R_hib |  |
| 2 | H5869 | ket_szo |  | יַעֲקֹב עֵין | עֵין יַעֲקֹב | eldonthetetlen | igen | = R_hib |  |
| 3 | H8076 | egybetus_rovidites |  | ׳שׁ | שׁ׳ | eldonthetetlen | igen | = R_hib |  |
| 4 | H1755 | harom_plusz_szo |  | וָדוֺר דּוֺר שְׁנֵי | שְׁנֵי דּוֺר וָדוֺר | helyes | igen | = R_hib |  |
| 5 | H6098 | ket_szo | irasjel | תּוֺרָה דָּבָר, | דָּבָר, תּוֺרָה | eldonthetetlen | nem | = R_hib |  |
| 6 | H4591 | harom_plusz_szo |  | יִמְעָ֑ט מֵהֶבֶל הוֺן | הוֺן מֵהֶבֶל יִמְעָ֑ט | helyes | igen | = R_hib |  |
| 7 | H389 | ket_szo | nevelo | הַמַּעַם אַךְ | אַךְ הַמַּעַם | helyes | igen | = R_hib |  |
| 8 | H6059 | harom_plusz_szo | nevelo | לוֺ תַּעֲנִיק הַעֲנֵיק | הַעֲנֵיק תַּעֲנִיק לוֺ | helyes | igen | = R_hib |  |
| 9 | H2119 | egybetus_rovidites |  | ׳י | י׳ | eldonthetetlen | igen | = R_hib |  |
| 10 | H5578 | ket_szo |  | סוּסָה חֲצַר | חֲצַר סוּסָה | helyes | igen | = R_hib |  |
| 11 | H1931 | ket_szo |  | פְרָת הוּא | הוּא פְרָת | eldonthetetlen | igen | = R_hib |  |
| 12 | H2896 | harom_plusz_token_geressel |  | ט ׳בָתֵּיהֶם מִלֵּא | בָתֵּיהֶם ט׳ מִלֵּא | eldonthetetlen | igen | מִלֵּא בָתֵּיהֶם׳ ט |  |
| 13 | H3629 | ket_szo | irasjel | כְּלוּלָה כַּלָּה, | כַּלָּה, כְּלוּלָה | eldonthetetlen | nem | = R_hib |  |
| 14 | H9009 | ket_szo |  | מֵאֲרֻבָּה כְּעָשָׁן | כְּעָשָׁן מֵאֲרֻבָּה | helyes | igen | = R_hib |  |
| 15 | H6999 | ket_szo |  | הגבעות על | על הגבעות | helyes | igen | = R_hib |  |
| 16 | H7754 | ket_szo |  | עֵצִים שׂוֺכַת | שׂוֺכַת עֵצִים | helyes | igen | = R_hib |  |
| 17 | H3368 | ket_szo |  | וְקָרוֺת חוֺם | חוֺם וְקָרוֺת | eldonthetetlen | igen | = R_hib |  |
| 18 | H3651 | ket_szo |  | יַאֲרִיךְ כֵּן | כֵּן יַאֲרִיךְ | helyes | igen | = R_hib |  |
| 19 | H9004 | ket_szo |  | חֳדָשִׁים כְּמִשְׁלשׁ | כְּמִשְׁלשׁ חֳדָשִׁים | helyes | igen | = R_hib |  |
| 20 | H1004 | harom_plusz_token_geressel | nevelo | ׳בּ הַיַּיִן מִשְׁתֵּה | בּ׳ מִשְׁתֵּה הַיַּיִן | helyes | igen | מִשְׁתֵּה הַיַּיִן בּ׳ |  |
| 21 | H2834 | rovidites_es_szo |  | ׳ח יְעָרוֺת | ח׳ יְעָרוֺת | eldonthetetlen | igen | יְעָרוֺת ח׳ |  |
| 22 | H7161 | harom_plusz_szo |  | לוֺ מִיָּדוֺ קַרְנַיִם | קַרְנַיִם מִיָּדוֺ לוֺ | helyes | igen | = R_hib |  |
| 23 | H3458 | harom_plusz_token_geressel |  | י ׳שָׁמַע ׳רגו | שָׁמַע י׳ רגו׳ | eldonthetetlen | igen | רגו׳ שָׁמַע׳ י |  |
| 24 | H6873 | egybetus_rovidites |  | ׳י | י׳ | eldonthetetlen | igen | = R_hib |  |
| 25 | H1288 | rovidites_es_szo |  | ׳ב צוּרִי | ב׳ צוּרִי | eldonthetetlen | igen | צוּרִי ב׳ |  |
| 26 | H227 | harom_plusz_szo |  | לוֺ טוֺב אָז | אָז טוֺב לוֺ | helyes | igen | = R_hib |  |
| 27 | H7919 | ket_szo |  | חָכָם לֵב | לֵב חָכָם | eldonthetetlen | igen | = R_hib |  |
| 28 | H4285 | egybetus_rovidites |  | ׳מ | מ׳ | eldonthetetlen | igen | = R_hib |  |
| 29 | H6921 | rovidites_es_szo |  | (הַ)קּ ׳רוּחַ | רוּחַ (הַ)קּ׳ | helyes | igen | רוּחַ׳ (הַ)קּ |  |
| 30 | H1755 | harom_plusz_szo |  | וָדוֺר דּוֺר מְשׂוֺשׂ | מְשׂוֺשׂ דּוֺר וָדוֺר | helyes | igen | = R_hib |  |
| 31 | H2568 | egybetus_rovidites |  | ׳ח | ח׳ | eldonthetetlen | igen | = R_hib |  |
| 32 | H1288 | ket_szo |  | ברוך מברכך | מברכך ברוך | eldonthetetlen | igen | = R_hib |  |
| 33 | H2786 | harom_plusz_token_geressel |  | ׳ח על שׁניו | ח׳ שׁניו על | eldonthetetlen | igen | שׁניו על ח׳ |  |
| 34 | H1818 | harom_plusz_szo | nevelo | יְכַמֵּר בַּנֶּפֶשׁ הוּא הַדָּם | הַדָּם הוּא בַּנֶּפֶשׁ יְכַמֵּר | helyes | igen | = R_hib |  |
| 35 | H5892 | ket_szo | szam_latin,nevelo | ᵐ5 הַשֵּׁעַר | הַשֵּׁעַר ᵐ5 | eldonthetetlen | igen | = R_hib |  |
| 36 | H2094 | rovidites_es_szo |  | י ׳מִשְׁמְּטֵי | מִשְׁמְּטֵי י׳ | eldonthetetlen | igen | מִשְׁמְּטֵי׳ י |  |
| 37 | H9003 | ket_szo |  | בְּ חָלַק | חָלַק בְּ | eldonthetetlen | igen | = R_hib |  |
| 38 | H5920 | ket_szo |  | בֵּין עַל | עַל בֵּין | eldonthetetlen | igen | = R_hib |  |
| 39 | H3427 | harom_plusz_szo | rafe_makkef,nevelo | הַחֲמוֺר עִםֿ מֹּה לָכֶם שְׁבוּ | שְׁבוּ לָכֶם מֹּה עִםֿ הַחֲמוֺר | helyes | igen | = R_hib |  |
| 40 | H2689 | rovidites_es_szo |  | ׳ח התרועה | ח׳ התרועה | eldonthetetlen | igen | התרועה ח׳ |  |
| 41 | H7832 | rovidites_es_szo |  | י ׳לִפְנֵי | לִפְנֵי י׳ | eldonthetetlen | igen | לִפְנֵי׳ י |  |
| 42 | H5360 | rovidites_es_szo |  | נ ׳עשׂה | עשׂה נ׳ | eldonthetetlen | igen | עשׂה׳ נ |  |
| 43 | H615 | rovidites_es_szo | nevelo | ׳א הַתִּקְוָה | א׳ הַתִּקְוָה | eldonthetetlen | igen | הַתִּקְוָה א׳ |  |
| 44 | H2873 | ket_szo | irasjel | טִבְחָה טֶבַח, | טֶבַח, טִבְחָה | eldonthetetlen | nem | = R_hib |  |
| 45 | H7218 | ket_szo | nevelo | הַכֹּהֲנִים רָאשֵׁי | רָאשֵׁי הַכֹּהֲנִים | helyes | igen | = R_hib |  |
| 46 | H4500 | ket_szo |  | אֹרְגִים כִּמְנוֺר | כִּמְנוֺר אֹרְגִים | helyes | igen | = R_hib |  |
| 47 | H249 | ket_szo | nevelo | הָאָרֶץ אֶזְרַח | אֶזְרַח הָאָרֶץ | helyes | igen | = R_hib |  |
| 48 | H58 | ket_szo |  | מִצְרַיִם אָבֵל | אָבֵל מִצְרַיִם | helyes | igen | = R_hib |  |
| 49 | H6946 | rovidites_es_szo |  | ׳ק בַּרְנֵעַ | ק׳ בַּרְנֵעַ | eldonthetetlen | igen | בַּרְנֵעַ ק׳ |  |
| 50 | H2506 | harom_plusz_token_geressel |  | בְּח ׳הַשָּׂדֶה ׳יִזְ | הַשָּׂדֶה בְּח׳ יִזְ׳ | helyes | igen | יִזְ׳ הַשָּׂדֶה׳ בְּח |  |

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

## 8. A felhasználó hipotézise: „angol” (vizuális, balról jobbra tárolt) szórend (2026-10-30)

**A kérdés:** lehet-e, hogy a `DictBDB.json` a héber futamokat egy bidi nélküli, balról jobbra rajzoló nézőprogramhoz
(pl. MySword / e-Sword) tárolja? Ebben a felfogásban a szavakon belül a betűk jó sorrendben vannak, a szavak sorrendje a
futamban fordított, és a geres is ezért kerül a betű elé. Ha így van, a forrás a saját nézőjében helyes, a hiba pedig a
Unicode logikai megjelenítésben (böngésző, Markdown) keletkezik. Ekkor a javítás egy rendszeres vizuális → logikai
konverzió volna a beolvasáskor.

**A mért szabály (R_ang):** a futam szavainak megfordítása, és tokenenként a betű elé került geres áthelyezése a token
végére. Futam-típusonként mértem (a geres nélküli egyszavas tételek nélkül; Biblia-ítélet a 2.4 szerint):

| Futam-típus | Tétel | R_ang = R_hib | Biblia: R_ang helyes / rontott / eldönthetetlen | Pontosság | Geres a betű után |
|---|---:|---:|---|---:|---|
| **geres nélküli** (tiszta) | 16 987 | 16 987 (100%) | 11 959 / 169 / 4 819 | **98,6%** | — |
| **geresszel** (tiszta) | 15 600 | 5 500 (35%) | 2 399 / 1 160 / 11 954 | **67,4%** | 15 566 / 34 rossz |
| írásjellel vagy sziglummal | 3 713 | 3 422 | 153 / 86 / 3 470 | 64,0% | 3 590 / 123 rossz |

A geresszel álló, tiszta futamok 10 100 eltérésében, ahol a Biblia dönt: az R_ang 413-szor helyes és az R_hib
eldönthetetlen; az R_ang 1 146-szor ront és az R_hib eldönthetetlen; az R_hib 1 031-szer helyes és az R_ang
eldönthetetlen; az R_hib 41-szer ront. A kézi mintában 14 sor tér el, mind geresszel. Jellemző példák (a 6. szakasz
R_ang oszlopa):
- 41. sor, `לִפְנֵי י׳` („Jahve előtt”): R_ang `לִפְנֵי׳ י`;
- 49. sor, `ק׳ בַּרְנֵעַ` (Kádes-Barnea): R_ang `בַּרְנֵעַ ק׳`;
- 43. sor, `א׳ הַתִּקְוָה` (Zak 9:12): R_ang `הַתִּקְוָה א׳`.
A H7121-ből `בְּשֵׁם׳ י ק׳` lesz; a nyomtatott alak `ק׳ בְּשֵׁם י׳`.

**1. Hány futamra igaz a hipotézis?** A **geres nélküli** több szavas futamokra igen: ott a JSON következetesen
szó-vizuális sorrendű, és a szavak megfordítása 98,6%-ban helyes (ez azonos az R0-val és az R_hib-bel). A **geresszel
álló** futamokra nem: a rendszeres konverzió csak 67,4%-ban ad helyes alakot. Az összes eldönthető tiszta futamon
14 358 / 15 687 = **91,5%**, szemben az R_hib 98,5%-ával.

**2. Van-e futam, ahol a hipotézis nem áll?** Igen, rendszeresen: a geresszel álló futamoknál a geres nem a futam
végén, hanem a futamon belül bontja meg a sorrendet. A geresnél kettévágott részfutamok egymáshoz képest nem
fordulnak meg úgy, mint a szavak, ezért a rövidítés más szóhoz kerül (a fenti példák). Ezt a darabolást a `BDB.lexicon`
`<bdbheb>` darabjai mutatják (3. szakasz), és ezt követi az R_lex / R_hib.

**Bidi nélküli néző? (értelmezés, a mért adatból következtetve)**
- A futamok utáni `&#x200E;` (LRM) bidi-vezérlő jel. Csak Unicode bidi-algoritmust futtató megjelenítőben van hatása:
  a héber futam után visszaállítja a balról jobbra irányt. Bidi nélküli, balról jobbra rajzoló nézőben semmit sem
  csinál. A jelenléte tehát arra utal, hogy a JSON **bidi-képes (HTML) megjelenítésre** készült, nem bidi nélküli nézőre.
- A szavakon belül a betűk logikai sorrendben állnak (a mássalhangzó-váz a TAHOT-tal egyezik). Egy tisztán bidi nélküli
  nézőben ezért minden héber szó tükrözve jelenne meg.
- A H7121 egyik megjelenítésben sem adja a nyomtatott alakot. Bidi-képes nézőben, jobbról balra olvasva:
  `׳ק י ׳בְּשֵׁם`. Szó-vizuális nézőben (R_ang): `בְּשֵׁם׳ י ק׳`.
- A MySword és az e-Sword saját megjelenítési módját itt nem ellenőriztem (nincs a repóban): ez nem lekérdezett adat.

**Melyik eset áll fenn?** **Forráshiba, nem megjelenítési különbség.** A forrás nem egy következetes vizuális formátum,
ezért egyetlen vizuális → logikai konverzió nem ad mindenhol helyes eredményt: a geres nélküli futamokon igen
(98,6%), a geresszel állókon nem (67,4%). A minta egy korábbi, vizuális megjelenítésből vett digitalizálásra utal.
Ebben a geres (vagy az eredeti aposztróf) irány nélküli jelként kettévágta a jobbról balra futamot; a JSON készítője
erre még egy egyszerű szómegfordítást tett. *(Ez az eredetre vonatkozó magyarázat következtetés; a mért tény a fenti
táblázat.)* A javaslat (7. szakasz) ezért változatlan: geres nélkül a szavak megfordítása (ez a hipotézis érvényes
része), geresnél a `BDB.lexicon` darabhatára szerint.

## 9. A héber futam és az utána álló igehely határa (az olvasó leletéből, PR #527; 2026-10-30)

**Az eset:** az olvasó szó-lapján a `יִקְרָא 1Móz 2:19` így jelenik meg: `1 יִקְרָאMóz`. Ez **más hiba, mint a
szórend.** A tárolt (logikai) sorrend jó, a hiba a megjelenítéskor keletkezik. A bidi-algoritmus a jobbról balra futam
utáni számot (gyenge iránytípus, EN) és a köztük álló semleges jeleket (szóköz, írásjel) a futamhoz csatolja, ha a
kettőt semmi sem választja el.

**Mérés** (a szkript 3/b. része; minta: héber betű vagy jel, utána semleges jelek, utána számjegy):

| Hely | Futam után szám | LRM a szövegben |
|---|---|---|
| `DictBDB.json` | 18 173 futam a 107 601-ből | **minden futam után van** (107 601 / 107 601: `</heb>&#x200E;`) |
| `adat/bdb_szakaszok.tsv` (`szoveg`) | 16 592 előfordulás, 7 950 sor | 0 |
| `adat/bdb_szakasz_hu.tsv` (`szoveg_hu`) | 13 070 előfordulás, 3 534 sor | 0 |
| `adat/forditasok.tsv` (`forditas_hu`, összes szótár) | 26 013 előfordulás, 5 898 sor | 0 |

**Hol keletkezik?** Ez a rész **nálunk**, a konverzióban keletkezik. A forrás minden héber futam után LRM-et
(U+200E, balról jobbra jel) tesz, és ez épp ezt a csatolást akadályozza meg. A `bont.py` `sima()` függvénye
(`t.replace('\u200e', '')`) és a `konkordancia/_convert_bdb.py` viszont kiveszi. A magyar fordításban a gond
erősebb: a magyar könyvrövidítések számmal kezdődnek (`1Móz`, `2Sám`), az angol forrásban pedig betűvel (`Gen`,
`Exod`). A fordítás tehát új „héber + szám” határokat is teremtett.

**Mi oldja meg?**
- **A vizuális → logikai konverzió (R_hib, R_ang) nem.** A határ a futamon kívül van, a tárolt sorrend ott már
  helyes; a sorrend-javítás ehhez nem nyúl.
- **Az izolálás igen** (szabványismeret, itt nem mértem; a PR #527 a jelölt rövidítéseknél kipróbálta):
  - HTML-ben a héber futam saját elemben: `<bdi>` vagy `<span lang="he" dir="rtl">`. A HTML szabvány alap-stíluslapja
    a `dir` attribútumú elemekre `unicode-bidi: isolate`-et ad, az olvasó szó-csempéi már így készülnek
    (`blokkok.py` `.heb` span). A folyó BDB-szövegben ezt minden héber futamra alkalmazni kell, nem csak a
    rövidítésekre.
  - Sima szövegben és Markdownban, ahol nincs elem: a futam után **LRM** (ahogy a forrás tette), vagy a futam körül
    **RLI … PDI** (U+2067 … U+2069).
- **Javaslat:** a táblák maradjanak LRM nélkül; az LRM eltávolítása a tisztításban önmagában nem hiba, mert a
  `forras_hash`-ek és az illesztés a tisztított szövegre épülnek. Az izolálást **a megjelenítés** tegye hozzá, egy közös függvénnyel, amelyet
  a lexikon-generátor (`lexikon_general.py`) és az olvasó (`blokkok.py`) egyaránt hív. Ez lehet ugyanaz a függvény,
  amely a rövidítéseket jelöli (N-F131x), és a sorrend-javítás (N-F131y) után fusson. A héber futam felismerése
  determinisztikus (`[\u0591-\u05f4\ufb1d-\ufb4f]` betűk és jelek, a köztük álló szóközzel és makkeffel); a futamon
  belüli számok és sziglumok (4.4/2.) külön esetek.
