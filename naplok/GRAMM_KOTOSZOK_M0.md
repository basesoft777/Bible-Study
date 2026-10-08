# GRAMM_KOTOSZOK_M0 — felmérés (F68 M0, csak olvas)

*FELADATOK #68 · `F68_GRAMM_KOTOSZOK_BRIEF.md` 3. szakasz M0 · ág: `claude/gramm-kotoszok` · 2026-10-08 · a repó adata nem változott: az `adat/grammatikai_strongok.tsv`-t és a generátort nem érintettem, az „után” oldal memóriabeli (a szkriptek a repón kívül, a scratchpadben futottak).*

**Eredmény egy bekezdésben.** 13 jelölt van (3 nevezett + 10 további `kötőszó` szófajú, a táblán nem szereplő héber Strong; ebből 3 arámi, 1 a TAHOT-ban 0 előfordulású). A negatív próba tiszta: egyik jelölt sem áll `strong`/`gerinc_elem` értékként, a `jeloltek.tsv`-ben pedig 0 találat (egyetlen kivétel a H6435, 3 említés egy bővített tanulmányban, l. 4. szakasz). **Két kritérium-eltérés** van (H6118 főnév, H3651 határozószó), és mindkettőnél a Strong-szám egy számon futtatja a funkciószói és a tartalmi használatot (5. szakasz). A hatás a meglévő gerinc-levezetésekre **nulla** (a négy dokumentált levezetésben és a kilenc motívum teljes metszetében egyetlen jelölt sem áll); a szakaszpárokon mérve csak a H3651 érint 11 párt az 5829-ből. A hatás az F56 LXX-szűrésre **a H3282-nél valós** (G3754 ὅτι és G1223 διά visszakerül, a G1894 ἐπειδή kiesik a legfeljebb 3-ból), a H6118-nál és a H3651-nél **nincs**. A felvételről nem döntök.

**Proveniencia-megjegyzés.** A számszerű állítások a `konkordancia/TAHOT_kivonat.tsv`, a `konkordancia/Strong_szotar.tsv`, az `adat/*.tsv` és az `adat/kulso/lxx_bridge.tsv` olvasásából jönnek; a lekérdezés a `lekerdez.py` függvényein (gerinc) és a `bdb_adatblokk.py` `szakasz_lxx` függvényén át, TSV-olvasás kizárólag `split('\t')`-tel. A `lekerdez.py gerinc` négy dokumentált hívását a CLI-vel is lefuttattam, és a saját számolás egyezik vele (4/4). Az igehely-szintű besorolások (H6118, H3651 mintázatai) az én olvasatom a TAHOT szomszédos szavai alapján: `scope=manual`, nem „ellenőrizve”.

**TAHOT-hiány.** A `TAHOT_kivonat.tsv` nem teljes (hiányzik legalább Jób 40:1–5 és a Jób 41; l. CLAUDE.md), ezért az alábbi ÓSZ-gyakoriságok alsó becslések, és a „0 találat” nem bizonyít. A H2958 (טְרוֹם) a TAHOT-ban 0 előfordulású: ez a kivonat tulajdonsága is lehet.

## 1. Jelöltlista

Szűrő: `Strong_szotar.tsv` szófaj-oszlopa tartalmazza a „kötőszó” szót (vegyes szófajúak is: „kötőszó / határozószó” stb.), és az `adat/grammatikai_strongok.tsv`-ben nincs; plusz a két nevezett, amely nem kötőszó (H3651, H6118).
`proveniencia: scope=OT-full | forras=konkordancia/Strong_szotar.tsv + konkordancia/TAHOT_kivonat.tsv + adat/grammatikai_strongok.tsv | n=13 | ts=2026-10-08T06:08Z`

| Strong | Szótő | Szófaj (Strong_szotar) | Jelentés | Aram. | ÓSZ (TAHOT) szó / vers | TAHOT-glosszák |
|---|---|---|---|---|---|---|
| H0176 | אוֹ | kötőszó | or |  | 321 / 218 | or ×321 |
| H0432 | אִלּוּ | kötőszó | except |  | 2 / 2 | except ×2 |
| H0638 | אַף | kötőszó | also | igen | 4 / 4 | also ×4 |
| H2958 | טְרוֹם | kötőszó | not yet |  | 0 / 0 | — |
| H3282 | יַעַן | kötőszó | because |  | 99 / 94 | because ×99 |
| H3651 | כֵּן | határozószó | so |  | 771 / 737 | so ×739, right ×22, for since ×10 |
| H3860 | לָהֵן | kötőszó | therefore |  | 2 / 1 | therefore ×2 |
| H3861 | לָהֵן | kötőszó | except | igen | 7 / 7 | except ×7 |
| H3863 | לוּ | kötőszó | if |  | 22 / 21 | if ×22 |
| H3884 | לוּלֵא | kötőszó | unless |  | 14 / 14 | unless ×14 |
| H6118 | עֵ֫קֶב | főnév, hímnemű | consequence |  | 15 / 15 | consequence ×15 |
| H6435 | פֶּן־ | kötőszó | lest |  | 133 / 125 | lest ×133 |
| H6903 | קֳבֵל | kötőszó | before | igen | 29 / 29 | before ×29 |

**Kategória-javaslat és ítéletkérés** (a javaslat nem döntés; a generátor kategóriakészlete: `kotoszo`, `partikula`, `eloljaro`, `nevmas`, `targyrag`, `vonatkozo_nevmas`, `tagadoszo`). Minden jelöltről ítélet kell: **F** (felvétel, kategóriával), **E** (elutasítás), **H** (`HATARESET`).

| Strong | Javasolt kategória | Megjegyzés (a kritérium szerint: „önmagában nem hordoz tartalmi jegyet”) | Ítélet |
|---|---|---|---|
| H3282 יַעַן | `kotoszo` | Okhatározói kötőszó; mind a 99 TAHOT-előfordulás „because”, 33 után `אֲשֶׁר` (H0834) áll, 7 után `כִּי` (H3588). Tartalmi használat nincs. Görög párja hiányos (l. 6. szakasz). | ? |
| H6118 עֵקֶב | `kotoszo` (föltételesen) | **Szófaj-eltérés**: a Strong-szótár szerint főnév. 15 előfordulásból 11 funkciószói olvasatú, 4 főnévi („jutalom, végig”). Nem választható szét Strong-számmal (5. szakasz). | ? |
| H3651 כֵּן | `kotoszo`/`hatarozoszo`? (a kategória-készletben nincs határozószó) | **Szófaj-eltérés**: határozószó; a BDB-sor (`forditasok.tsv`) melléknévként is nyitja („helyes”). Egy számon fut az ezért-jelentés, a deiktikus „így/úgy”, az „azután” és a „helyes” (5. szakasz). | ? |
| H0176 אוֹ | `kotoszo` | „vagy”; tartalmi jegy nincs. Görög párjai (G2228 ἤ, G2532 καί) a listán vannak. | ? |
| H6435 פֶּן־ | `kotoszo` | „nehogy”; célhatározói tilt-kötőszó. Az egyetlen jelölt, amely egy tanulmányban elemzett tételként szerepel (4. szakasz). | ? |
| H3863 לוּ, H3884 לוּלֵא | `kotoszo` | Feltételes/óhajtó („ha”, „ha nem”). Görög pár G1487 εἰ (listán). | ? |
| H0432 אִלּוּ, H3860 לָהֵן | `kotoszo` | Kettő, ill. két előfordulás (H3860: 1 vers); a hatás gyakorlatilag 0. | ? |
| H0638 אַף (arámi), H3861 לָהֵן (arámi), H6903 קֳבֵל (arámi) | `kotoszo` | Arámi alakok. A H3861 szótője azonos a H3860-éval. A H6903 szótári jelentése „before”, de szófaja kötőszó (a TAHOT-ban 29 szó). A generátor eddig csak héber H-t és H9xxx-et tartalmaz, arámi tétel még nincs a kézi listán: a felvételük kategória-szempontból új precedens. | ? |
| H2958 טְרוֹם | `kotoszo` | A TAHOT-ban 0 előfordulás; felvétele a gerincszűrésen nem mérhető. | ? |

## 2. Kritérium-eltérések (külön jelölve)

A generátor „ellenőrizhető jele” (`eszkozok/grammatikai_strongok_general.py`, 94–96. sor): a kézi tétel szófaja a `Strong_szotar.tsv`-ben elöljárószó, kötőszó vagy névmás.

| Eltérés | Strong | Strong_szotar szófaj | Mi tér el |
|---|---|---|---|
| E1 | H6118 | `főnév, hímnemű` („consequence”) | nem kötőszó; önálló főnévként is használt |
| E2 | H3651 | `határozószó` („so”) | nem a kritériumban megnevezett három szófaj egyike |
| E3 | H0638, H3861, H6903 | `kötőszó`, de arámi | a kézi lista héber szavakra épül; arámi precedens nincs |
| E4 | H3282 (jelzés, nem eltérés) | `kötőszó` | megfelel a jelnek. A `forditasok.tsv` BDB-sora viszont `elöljárószó`-nak nevezi, ami nem érinti a kritériumot |

Megjegyzés (hatókörön kívüli megfigyelés, nem javaslat): a „jel” szerint további, a táblán nem szereplő elöljárószó/névmás/partikula szófajú szavak is vannak, ÓSZ ≥ 20 szóval; a brief hatóköre a `kötőszó` szófajúakra szól, ezért ezeket nem vizsgáltam és nem tettem a jelöltlistára (36 sor, köztük H0518 אִם „ha” 1069, H4616 מַעַן „mert/hogy” 272, H5973 עִם „-val” 1051, H0859 אַתָּה 1094). Ha a felhasználó e kört is el akarja bírálni, külön tétel kell.
`proveniencia: scope=OT-full | forras=konkordancia/Strong_szotar.tsv + konkordancia/TAHOT_kivonat.tsv + adat/grammatikai_strongok.tsv | n=36 | ts=2026-10-08T06:08Z`

<details><summary>A 36 sor (nem javaslat, csak a kör mérete)</summary>

| Strong | Szótő | Szófaj | Jelentés | Aram. | ÓSZ szó |
|---|---|---|---|---|---|
| H0859 | אַתָּ֫ה | személyes névmás | you(m.s.) |  | 1094 |
| H0518 | אִם | partikula | if |  | 1069 |
| H5973 | עִם | elöljárószó | with |  | 1051 |
| H0854 | אֵת | elöljárószó | with |  | 929 |
| H0589 | אֲנִי, אָֽנֹכִ֫י | személyes névmás | I |  | 874 |
| H2009 | הִנֵּה | mutató partikula | behold |  | 843 |
| H4100 | מָה | kérdő névmás | what? |  | 753 |
| H0428 | אֵ֫לֶּה | mutató névmás | these |  | 746 |
| H2063 | זֹאת | mutató névmás | this |  | 604 |
| H3541 | כֹּה | partikula | thus |  | 577 |
| H1992 | הֵ֫מָּה | személyes névmás | they(masc.) |  | 553 |
| H4310 | מִי | kérdő névmás | who? |  | 418 |
| H0996 | בַּ֫יִן | elöljárószó | between |  | 405 |
| H0595 | אָֽנֹכִ֫י | személyes névmás | I |  | 359 |
| H1768 | דִּי | partikula | that | aram | 345 |
| H2005 | הֵן | partikula | look! |  | 315 |
| H4616 | מַ֫עַן | partikula | because |  | 272 |
| H5048 | נֶ֫גֶד | elöljárószó | before |  | 151 |
| H3644 | כְּמוֹ | partikula | like |  | 142 |
| H3426 | יֵשׁ | partikula | there |  | 140 |
| H0637 | אַף | partikula | also |  | 134 |
| H0587 | אֲנַ֫חְנוּ | személyes névmás | we |  | 120 |
| H4481 | מִן־ | elöljárószó | from | aram | 109 |
| H1157 | בַּ֫עַד | elöljárószó | about|through|for |  | 105 |
| H5922 | עַל | elöljárószó | since | aram | 104 |
| H1836 | דְּנָה | mutató névmás | this | aram | 58 |
| H2962 | טֶ֫רֶם | elöljárószó | before |  | 56 |
| H5668 | עָבוּר | elöljárószó | for the sake of |  | 49 |
| H6925 | קֳדָם | elöljárószó | before | aram | 42 |
| H5978 | עִמָּדִי | elöljárószó | with me |  | 42 |
| H1767 | דַּי | elöljárószó | enough |  | 39 |
| H5705 | עַד | partikula | till | aram | 35 |
| H3972 | מְא֫וּמָה | határozatlan névmás | anything |  | 32 |
| H2007 | הֵנָּה | személyes névmás | they(fem.) |  | 30 |
| H5974 | עִם | elöljárószó | with | aram | 22 |
| H1932 | הוּא | személyes névmás | he;_she;_it | aram | 22 |

</details>

## 3. TILTOLISTA és HATARESET

A 13 jelölt közül egyik sem szerepel a `TILTOLISTA`-n (H3068, H0559, G2316, G3004, H1961, H6213) és a `HATARESET`-ben (H3605). A felvétel a generátor `felvesz()` őrén át menne, amely a tiltólistát hibával ellenőrzi; az M1-ben ez lefut.

## 4. Negatív próba

Hol áll a jelölt Strong-száma a kézi/kereszthivatkozott rétegben? Minta: `\bH0*N\b`, az `adat/elofordulasok.tsv` `strong` és `gerinc_elem` oszlopában (259 sor), a `adat/jeloltek.tsv` minden sorában (342 sor), a forrás-`.md` fájlokban (`motivumok/` 9, `motivumlog/` 13, `tematikus_lezart/` 16, `genezis/` 24, `ujszovetseg/` 3, `melyelemzesek/` 1 fájl) és — kimeneti rétegként, külön oszlopban — a `lexikon/` 16 fájljában.
`proveniencia: scope=manual-run | forras=adat/elofordulasok.tsv + adat/jeloltek.tsv + motivumok,motivumlog,tematikus_lezart,genezis,ujszovetseg,melyelemzesek,lexikon/**/*.md | n=13 | ts=2026-10-08T06:08Z`

| Strong | elofordulasok `strong` | elofordulasok `gerinc_elem` | jeloltek.tsv | forrás-`.md` (motivumok, motivumlog, tematikus_lezart, genezis, ujszovetseg, melyelemzesek) | lexikon `.md` (kimenet) |
|---|---|---|---|---|---|
| H0176 | 0 | 0 | 0 | 0 | 0 |
| H0432 | 0 | 0 | 0 | 0 | 0 |
| H0638 | 0 | 0 | 0 | 0 | 0 |
| H2958 | 0 | 0 | 0 | 0 | 0 |
| H3282 | 0 | 0 | 0 | 0 | 0 |
| H3651 | 0 | 0 | 0 | 0 | 0 |
| H3860 | 0 | 0 | 0 | 0 | 0 |
| H3861 | 0 | 0 | 0 | 0 | 0 |
| H3863 | 0 | 0 | 0 | 0 | 0 |
| H3884 | 0 | 0 | 0 | 0 | 0 |
| H6118 | 0 | 0 | 0 | 0 | 0 |
| H6435 | 0 | 0 | 0 | 3 | 0 |
| H6903 | 0 | 0 | 0 | 0 | 0 |

A három nevezett Strongra 0/0/0, megegyezik a befogadáskor mért értékkel (a két táblában 0). **Egyetlen találat**: a H6435 háromszor áll a `genezis/1Moz_3v1-6_bovitett.md`-ben (az `פֶּן־תְּמֻתוּן`, H6435/H4191 sorában; 1Móz 3:3 „nehogy meghaljatok”). Ez nem gerinc-elem és nem `elofordulasok`-sor, tehát a „nincs közvetlen út” szabályt nem érinti, de a tanulmány lexikai elemzésében a szó tartalmi szerepet kap: a H6435 felvétele a gerincszűrésben (stopword) és a kollokáció-/szóelemzési használata nem ütközik (a SEMA 2.x szerint a tábla a `gerinc` stopword-listája, nem globális kizárás), de a felhasználónak tudnia kell róla.

## 5. A kettős használat vizsgálata (H6118, H3651; a H3282 kontrollként)

**Alapkérdés:** egy Strong-szám szétválasztja-e a funkciószói és a tartalmi használatot? A TAHOT-ban a Strong a szótő szintjén áll (egy H-szám), a „Rövid jelentés” oszlop viszont a szövegkörnyezetből kapja a glosszát; a szomszédos szó Strongja (`H9005` = lə-, `H5921` = ʿal, `H0834`/`H3588` = ʾăšer/kî) a kötőszói szerkezetet jelzi.
`proveniencia: scope=OT-full | forras=konkordancia/TAHOT_kivonat.tsv (a szomszédos sor Strongja) + adat/karoli_strong/parok_*.tsv | strong=H3651,H6118,H3282 | n=771,15,99 | ts=2026-10-08T06:08Z`

### H3282 (kontroll)
99 szó, mind „because”; a szomszédos szó nagyon gyakran `H0834` (33) vagy `H3588` (7). Károli (a `parok_*.tsv` 10 sora, `bizonyossag` vegyes): mivelhogy ×3, mert ×2, azért, miatt, hogy, miért, a. **Nincs tartalmi használat; egy számon egyféle funkció.**

### H6118 עֵקֶב — 15 szó, 15 vers
A TAHOT-glossza végig „consequence”, tehát a Strong **nem választ szét**. A szomszédos szavak és a Károli-megfelelők (a `parok` 11 sora, `bizonyossag` nagyrészt `alacsony`) alapján kétféle használat látszik (olvasatom: `scope=manual`):

| Olvasat | Igehely | Jel a TAHOT-ban / Károli |
|---|---|---|
| kötőszói / elöljárószói (11) | 1Móz 22:18, 26:5; 2Sám 12:6, 12:10; Ámós 4:12 | után `H0834`/`H3588` áll (עֵקֶב אֲשֶׁר / עֵקֶב כִּי) — Károli (1Móz 22:18, 26:5): mivelhogy |
| | 4Móz 14:24; 5Móz 7:12, 8:20; Ézs 5:23 | `עֵקֶב` + ige/főnév — Károli: mivelhogy, ha, azért/mert |
| | Zsolt 40:16, 70:4 | `עַל־עֵקֶב` — Károli: miatt |
| főnévi, tartalmi (4) | Zsolt 19:12 | „jutalma” (Károli) |
| | Zsolt 119:33, 119:112 | „mindvégig” (Károli) |
| | Péld 22:4 | `עֵקֶב עֲנָוָה` (a `parok` nem fedi a Példabeszédeket; az olvasat az enyém, `manual`) |

A felvétel tehát a 15-ből ~4 helyen tartalmi jegyet is elnyomna a gerinc-metszetben (ill. az LXX-szűrésben nem, mert a H6118-nak nincs LXX-párja). **Ezt jelzem, nem döntöm el.** Az ÓSZ-ben mindössze 15 szó, a hatás ennek megfelelően kicsi.

### H3651 כֵּן — 771 szó, 737 vers
A TAHOT glosszája három értéket mutat: „so” ×739, „right” ×22, „for since” ×10 — a Strong tehát **nem választja szét** az adverbiális és a melléknévi („helyes, igaz”) használatot; a TAHOT-glossza a mellékneveset ('right') jelöli, ez az egyetlen szétválasztás. A szomszédos szó szerint (az előző sor Strongja):

| Szerkezet | Előző sor | Szó | Jelentés / megjegyzés |
|---|---|---|---|
| `לָכֵן` (lākēn) | `H9005` | 200 | „ezért” — következtető kötőszói használat; 67 esetben közvetlenül `H3541` (כֹּה) követi (az „ezért így szól” típusú formula, a szomszédság alapján) |
| `עַל־כֵּן` (ʿal-kēn) | `H5921` | 155 | „ezért” (146 „so”, 9 „for since”) — következtető |
| `וַיְהִי כֵן` (és úgy lett) | `H1961` | 14 | „és úgy lett”: 14 szó, 12 vers (1Móz 1:7, 9, 11, 15, 24, 30; 2Móz 10:10, 14; Bír 6:38; 2Kir 15:12; 2Krón 1:12; Ámós 5:14) — a hat 1Móz 1-es hely a teremtési formula, motívumhordozó lehet |
| `אַחֲרֵי־כֵן` (aḥărê-kēn) | `H0310` | 53 | „azután” (időbeli, tartalmi jegy) |
| `עָשָׂה כֵן` | `H6213` | 49 | „így tett” (anaforikus/deiktikus határozószó) |
| `כֵּן` „right” | `H3808` (8), `H3588` (3) stb. | 22 | **melléknév** („helyes, becsületes”; pl. 1Móz 42:11 כֵּנִים, 4Móz 27:7, Péld 11:19, Jer 23:10) — tartalmi |
| egyéb szabadon álló `כֵּן` | többféle | ~278 | „így/úgy” (deiktikus határozószó); a TAHOT-gloss „so” |

Összesen: lākēn + ʿal-kēn = 355 (46%), azaz a szavak közel fele **következtető kötőszó**; a többi határozószói vagy melléknévi. Károli a `parok` 246 sorában (1–5Móz, Józs, Zsolt): úgy 62, azért 47, így 27, azután 15, akképen/aképen 16, ezért 8, **igaz 5**, olyan 5 — tehát a lefedett könyvekben is a tartalmi és a funkciószói alakok vegyesen jelennek meg. **Ítélet nincs.** Két szempont a döntéshez: (1) ha a H3651 felkerül, a `וַיְהִי כֵן` teremtési formula és az „azután”, valamint a „helyes” tartalmi használat is kiesik a metszetből; (2) ha nem kerül fel, a lākēn/ʿal-kēn következtető kötőszó a metszetben marad (a mérés szerint ez ritkán számít, l. 6. szakasz). A generátor kritériumában a **szó** (nem a szerkezet) a döntési egység; a H9005+H3651 szétválasztása (lə-kēn) a TAHOT-ban már megvan, de a Strong-lista nem szerkezetet, hanem számot szűr.

## 6. Hatásmérés

Mérési felállás. **Előtte:** a repó valódi tábla (85 adatsor: 44 H9xxx + 10 `HEBER_KEZI` + 31 `GOROG_KEZI`; a fájl 98 sora a gépi fejléceket is tartalmazza). **Utána:** memóriabeli halmaz (tábla ∪ jelöltek), a repón kívül; a repó táblája nem változott. Forgatókönyvek: **A** = a 3 nevezett (H3282, H6118, H3651); **B** = mind a 13 jelölt; ezen belül külön **csak H3282 / csak H6118 / csak H3651**.

### 6.1 Gerinc-metszet — a dokumentált levezetések

A négy dokumentált `lekerdez.py gerinc` hívás (az F4-alapállapot, a HAMART-001 levezetés, a TEREMT-002 T1-scan és az EMELES-napló) CLI-vel újrafuttatva (a számok egyeznek a saját számolással):

| Levezetés | Szakaszok | Metszet (szűretlen) | Kiszűrve (előtte) | Marad előtte | Marad A után | Marad B után | Új kiszűrt Strong |
|---|---|---|---|---|---|---|---|
| D1 F4-alapállapot | 1Móz 3 × 1Móz 6:1-8 | 40 | 16 | 24 | 24 | 24 | — |
| D2 HAMART-001 | 1Móz 3, 4, 6:1-8, 6:9-22 | 23 | 12 | 11 | 11 | 11 | — |
| D3 TEREMT-002 (T1) | 1Móz 1:2, Jer 4:23, Ézs 34:11 | 3 | 1 | 2 | 2 | 2 | — (üres) |
| D4 EMELES-napló | Sir 2 × Ézs 34 | 54 | 16 | 38 | 38 | 38 | — |

**Eredmény: nulla változás mind a négy levezetésben**: a 13 jelölt egyike sem áll a metszetben. (Az üres eredmény is rögzítve: a B-forgatókönyv sem módosít.)
`proveniencia: scope=range:1Móz 3+1Móz 6:1-8 | forras=TAHOT_kivonat.tsv | n=24 | ts=2026-10-08T06:07Z`
`proveniencia: scope=range:1Móz 3+1Móz 4+1Móz 6:1-8+1Móz 6:9-22 | forras=TAHOT_kivonat.tsv | n=11 | ts=2026-10-08T06:07Z`
`proveniencia: scope=range:1Móz 1:2+Jer 4:23+Ézs 34:11 | forras=TAHOT_kivonat.tsv | n=2 | ts=2026-10-08T06:07Z`
`proveniencia: scope=range:Sir 2+Ézs 34 | forras=TAHOT_kivonat.tsv | n=38 | ts=2026-10-08T06:07Z`

### 6.2 Gerinc-metszet — motívumok `elofordulasok.tsv` szakaszai alapján

Kilenc motívum, mindegyikre az `igehely` oszlop összes különböző szakasza (259 sorból; mind elemezhető). Két mérés: (a) az **összes szakasz** metszete (a „gerinc”), (b) a motívum szakaszainak **minden párja** (5829 pár; a pár-metszet a zajt méri).
`proveniencia: scope=range:elofordulasok.igehely | forras=TAHOT_kivonat.tsv + TAGNT_kivonat.tsv + adat/elofordulasok.tsv | n=9 motívum, 5829 pár | ts=2026-10-08T06:08Z`

| Motívum | szakaszok | metszet (szűretlen) | marad előtte | marad A után | marad B után |
|---|---|---|---|---|---|
| ALVIL-001 | 72 | 0 | 0 | 0 | 0 |
| ANTROP-001 | 8 | 0 | 0 | 0 | 0 |
| HAMART-001 | 52 | 0 | 0 | 0 | 0 |
| HODIT-001 | 33 | 0 | 0 | 0 | 0 |
| ISTENTISZT-001 | 32 | 0 | 0 | 0 | 0 |
| KIRALY-001 | 9 | 0 | 0 | 0 | 0 |
| MENNY-001 | 9 | 0 | 0 | 0 | 0 |
| TEREMT-001 | 41 | 0 | 0 | 0 | 0 |
| TEREMT-002 | 3 | 3 | 2 | 2 | 2 |

Csak a TEREMT-002 metszete nem üres (3 szakasz; ugyanaz, mint D3: 2 marad, nincs változás). A páronkénti mérésben a marad-átlag **1,11 → 1,10** (A és B egyaránt); a **H3651** az egyetlen jelölt, amely szakaszpár-metszetben áll: **11 pár / 5829** (HODIT-001 6, HAMART-001 3, ALVIL-001 1, MENNY-001 1), a többi 12 jelölt 0.

| Strong | szakaszpár-metszetben | motívum-metszetben (összes szakasz) |
|---|---|---|
| H0176 | 0 / 5829 | 0 / 9 |
| H0432 | 0 / 5829 | 0 / 9 |
| H0638 | 0 / 5829 | 0 / 9 |
| H2958 | 0 / 5829 | 0 / 9 |
| H3282 | 0 / 5829 | 0 / 9 |
| H3651 | 11 / 5829 | 0 / 9 |
| H3860 | 0 / 5829 | 0 / 9 |
| H3861 | 0 / 5829 | 0 / 9 |
| H3863 | 0 / 5829 | 0 / 9 |
| H3884 | 0 / 5829 | 0 / 9 |
| H6118 | 0 / 5829 | 0 / 9 |
| H6435 | 0 / 5829 | 0 / 9 |
| H6903 | 0 / 5829 | 0 / 9 |

### 6.3 F56 LXX-szűrés — a BDB-adatblokk LXX-szakasza

A `bdb_adatblokk.szakasz_lxx()` függvényt futtattam a valódi tábla halmazával („előtte”) és a jelölttel bővített memóriabeli halmazzal („utána”, `grammatikai()` felülírva a futás idejére). A szűrő csak a jelölt **saját** blokkjának LXX-szakaszát érinti (a görög nyelvtani találatokat ugyanis a héber szó nyelvtani státusza dönti el); másik szó blokkja nem változik.
`proveniencia: scope=H3282,H3651,... (13 jelölt) | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv + adat/grammatikai_strongok.tsv | n=13 | ts=2026-10-08T06:08Z`

| Strong | LXX-párok (G×db, max 5) | előtte (LXX-szakasz) | utána (LXX-szakasz) | |
|---|---|---|---|---|
| H0176 | G2228×253; G2532×25 | — [kihagyva, nyelvtani görög szó: G2228 ἤ ×253, G2532 καί ×25] | G2228 ἤ ×253, G2532 καί ×25 (a legfeljebb 3 leggyakoribb) | VÁLTOZIK |
| H0432 | nincs LXX-pár | — | — |  |
| H0638 | nincs LXX-pár | — | — |  |
| H2958 | nincs LXX-pár | — | — |  |
| H3282 | G0473×21; G3754×6; G1223×4; G1894×3 | G473 ἀντί ×21, G1894 ἐπειδή ×3 (a legfeljebb 3 leggyakoribb) [kihagyva, nyelvtani görög szó: G3754 ὅτι ×6, G1223 διά ×4] | G473 ἀντί ×21, G3754 ὅτι ×6, G1223 διά ×4 (a legfeljebb 3 leggyakoribb) | VÁLTOZIK |
| H3651 | G3779×300; G5124×279; G5023×39; G5127×16 | G3779 οὕτω, οὕτως ×300, G5124 τοῦτο ×279, G5023 ταῦτα ×39 (a legfeljebb 3 leggyakoribb) | G3779 οὕτω, οὕτως ×300, G5124 τοῦτο ×279, G5023 ταῦτα ×39 (a legfeljebb 3 leggyakoribb) | azonos |
| H3860 | nincs LXX-pár | — | — |  |
| H3861 | nincs LXX-pár | — | — |  |
| H3863 | G1487×10 | — [kihagyva, nyelvtani görög szó: G1487 εἰ ×10] | G1487 εἰ ×10 (a legfeljebb 3 leggyakoribb) | VÁLTOZIK |
| H3884 | G1487×13 | — [kihagyva, nyelvtani görög szó: G1487 εἰ ×13] | G1487 εἰ ×13 (a legfeljebb 3 leggyakoribb) | VÁLTOZIK |
| H6118 | nincs LXX-pár | — | — |  |
| H6435 | G3361×72; G3379×47 | G3379 μήποτε ×47 (a legfeljebb 3 leggyakoribb) [kihagyva, nyelvtani görög szó: G3361 μή ×72] | G3361 μή ×72, G3379 μήποτε ×47 (a legfeljebb 3 leggyakoribb) | VÁLTOZIK |
| H6903 | G2509×4 | G2509 καθάπερ ×4 (a legfeljebb 3 leggyakoribb) | G2509 καθάπερ ×4 (a legfeljebb 3 leggyakoribb) | azonos |

**A H3282 F56-mintabeli eset** (a brief legalább ezt kérte): előtte `G473 ἀντί ×21, G1894 ἐπειδή ×3 [kihagyva: G3754 ὅτι ×6, G1223 διά ×4]`; utána `G473 ἀντί ×21, G3754 ὅτι ×6, G1223 διά ×4`. Egyezik a `naplok/BDB_ADATBLOKK_minta.md` 3. pontjának leírásával (a nyers sorból: a nyelvtani görög találatok száma 2 = G3754, G1223). **Nüansz:** a felvétel a kihagyott G3754/G1223-at visszahozza, de a `LXX_MAX = 3` miatt a **G1894 ἐπειδή** (kötőszó, szintén valódi megfelelő) kiesik a megjelenített háromból — a nyers `lxx_bridge.tsv` mind a négyet tartalmazza. **H6118:** nincs LXX-pár, a hatás üres. **H3651:** az LXX-szakasz **azonos** (G3779 οὕτως ×300, G5124 τοῦτο ×279, G5023 ταῦτα ×39 egyike sincs a G-listán), tehát a felvétel itt az LXX-nézetet nem javítja.

Más blokkokra a javítótábla (`adat/bdb_igehely_javitas.tsv`) sorai nem érintettek: a jelölt Strongokra 0 sor van, tehát a `gramm → jelolt_marad` átbillenés nem fordul elő. A `forditasok.tsv`-ben négy jelöltnek van BDB-fordítása (H3651, H3282, H0176, H6435); a fordítások módosítása nem tartozik ide (#38).

### 6.4 A görög oldal tükrözése (csak jelzés, a brief szerint a bővítés külön döntés)

A jelöltek legfeljebb 4 leggyakoribb LXX-párja, és hogy a `GOROG_KEZI` listán szerepel-e (a Strong-szótár szófajával):

| Héber | Görög | db | szótő | szófaj | G-lista |
|---|---|---|---|---|---|
| H0176 | G2228 | 253 | ἤ | kötőszó / határozószó / partikula | listán |
| H0176 | G2532 | 25 | καί | kötőszó / határozószó / elöljárószó | listán |
| H3282 | G0473 | 21 | ἀντί | elöljárószó / indulatszó | NINCS listán |
| H3282 | G3754 | 6 | ὅτι | kötőszó | listán |
| H3282 | G1223 | 4 | διά | elöljárószó | listán |
| H3282 | G1894 | 3 | ἐπειδή | kötőszó | NINCS listán |
| H3651 | G3779 | 300 | οὕτω, οὕτως | határozószó | NINCS listán |
| H3651 | G5124 | 279 | τοῦτο | névmás | NINCS listán |
| H3651 | G5023 | 39 | ταῦτα |  | NINCS listán |
| H3651 | G5127 | 16 | τοῦτου |  | NINCS listán |
| H3863 | G1487 | 10 | εἰ | kötőszó / határozószó / partikula | listán |
| H3884 | G1487 | 13 | εἰ | kötőszó / határozószó / partikula | listán |
| H6435 | G3361 | 72 | μή | kötőszó / határozószó | listán |
| H6435 | G3379 | 47 | μήποτε | határozószó / partikula | NINCS listán |
| H6903 | G2509 | 4 | καθάπερ | határozószó | NINCS listán |

Hiányzó görög pár: H3282 → G473 ἀντί, G1894 ἐπειδή; H3651 → G3779 οὕτως, G5124 τοῦτο (a G3778 οὗτος alakja, külön Strong-számon), G5023, G5127; H6435 → G3379 μήποτε; H6903 → G2509 καθάπερ. A H6118-nak nincs LXX-párja.

### 6.5 Más fogyasztók (nem mért, csak felsorolt)

A `grammatikai_strongok.tsv`-t olvassa még: `eszkozok/jelolt.py` (jelölt-generálás: a felvett Strong kiszűrődne a jelöltekből), `eszkozok/olvaso_pilot/adat.py` (a nyelvtani Strongok **nem kapnak szó-lapot**, 105/179/186/381/385. sor — a felvett H3282/H3651 szó-lapja az olvasói pilotból kiesne; ezt nem mértem), `eszkozok/lxx_bridge_egyezes.py` (csak G-sorok), `eszkozok/lxx_versszintu_import.py` (G-sorok), `eszkozok/f4_0c_korut_ellenoriz.py` (a generátor sorszámát ellenőrzi: a `231` sor, amely egy bővítéssel eltolódik — az M1-nek erre figyelnie kell), `eszkozok/teszt_bdb_adatblokk.py`.

## 7. Alapállapot-megfigyelés (nem e feladat hibája)

`python eszkozok/teszt_bdb_adatblokk.py` az ágon, változtatás nélkül: 35 teszt, **1 bukás** (`test_pelda_idezet_szo_szerinti`, H2617, 1Móz 24:14). A bukás független a jelöltektől (HEAD `046d081`, a repó nem módosult). Az elfogadási feltétel („zöld”) ezért az M1-ben nem teljesíthető, amíg ezt valaki nem javítja vagy nem indokolja; **jelzem, nem javítom** (nem a feladat hatóköre).

## 8. Döntési javaslat (⛔ a felhasználónak)

Javaslat (nem döntés), a mérés alapján:
- **H3282**: felvétel (`kotoszo`). Tiszta funkciószó, a mérés hatása éppen az F56-ban jelzett hiány megszüntetése; a görög oldal (G473, G1894) külön döntés.
- **H6118, H3651**: **nem vennénk fel automatikusan**; mindkettőnél a Strong-szám nem választja szét a funkciószói és a tartalmi használatot (H6118: 4/15 tartalmi; H3651: melléknévi „helyes”, „azután”, a `וַיְהִי כֵן` teremtési formula, ~54% nem következtető). A gerinc-metszetre a hatás kicsi vagy nulla (H6118 0; H3651 11/5829 pár). Ha mégis a lista, akkor a `HATARESET`-be dokumentálva, nem a táblába — vagy elutasítás.
- **H0176, H6435, H3863, H3884, H0432, H3860**: felvehető `kotoszo`-ként, hatás gyakorlatilag 0 a gerincen; az LXX-nézeten H0176/H3863/H3884/H6435 javul (görög nyelvtani találatok megjelennek). H6435-nál a tanulmánybeli említést tudomásul kell venni.
- **H0638, H3861, H6903 (arámi), H2958 (0 előfordulás)**: külön kérdés (arámi precedens), javaslat: halasztás, amíg nincs mérhető hatás.

A tételt a `DONTESEK.md` `DT-F68a` helyőrzővel rögzíti.
