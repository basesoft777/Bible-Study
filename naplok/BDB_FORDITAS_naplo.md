# F38 BDB_FORDITAS — futásnapló

*Brief: `F38_BDB_FORDITAS_BRIEF.md` v1 · ág: `claude/admiring-bohr-texair` · indult: 2026.10.01*

## M0 — Felmérés (F38.1)

Parancs: `python naplok/BDB_FORDITAS_M0.py` (csak olvas; egyetlen kimenete a
`naplok/BDB_FORDITAS_sorrend.tsv`). Minden szám ebből a futásból.

### 1. Előfeltétel (F34)

- Az F34 merge-commitja (`fa501c9`) az `origin/main`, a `main` és a `HEAD` őse: **igen**.
- BDB-forrás: 8 090 szócikk, 6 325 071 karakter (a brief 6,40 milliót írt; a különbség a
  brief becslése, a mérés ez).
- **A 13. kapu (fejezetszám) a forráson nem 0 jelzést ad: 91 szócikk jelez.** Mérés: a forrás
  könyvnévvel jelölt igehelyeit a 11. kapu leképezésével (`forditas_kapuk._konyv_mintak`)
  Károli-alakra fordítva, szócikkenként `ellenoriz_fejezetszam`. Ebből 83 szócikk az F34
  maradék-listáján van (`naplok/F34_M2_maradek.tsv`, N-F34: a ψ-hiba B/R maradéka, amelyet az
  F34 a felhasználó döntésével — DT-F34b/c — szándékosan hagyott meg); 8 szócikk nincs rajta
  (nem ψ eredetű könyvfeloldási hibák, az N-F34c köre):

  | Szócikk | Jelzés (Károli-alakban) |
  |---|---|
  | H0854 | Ján 30, Ján 54, Jón 11 |
  | H3117 | Dán 40 |
  | H5750 | 2Krón 43, 2Krón 45 |
  | H6684 | Jón 20 |
  | H6881 | Dán 19 |
  | H8034 | Dán 22 (a brief „Dán 22:14” példája) |
  | H8478 | Dán 18, Dán 21, Dán 24 |
  | H9004 | Dán 23 |

  Az M1 adag négy szócikke érintett: H9009 (1Kir 45, 59, 61, 66), H9005 (Hab 41, Jóel 9),
  H0413 (5Móz 37), H0834 (Ruth 8, 9) — mind az F34 maradék-listáján.

  **Kezelés:** a brief M0.1 szó szerint megállást írna elő („Ha nem, megáll és jelez”); a
  brief „Szabályok” szakasza viszont pontosan erre az esetre ad eljárást („Forráshiba … a
  fordítás hűen átveszi, a 13. kapu jelzése a naplóba kerül; a forrást ez a menet nem
  javítja”), és a maradékot az F34 jóváhagyottan hagyta nyitva. A menet az utóbbi szerint
  haladt tovább az M1-gyel; a kérdés a `DONTESEK.md` DT-F38 (b) pontjában a felhasználóé. A
  13. kapu nem gátoló (JELZES), a forrásbeli hibás igehely a fordításban változatlanul
  (Károli-rövidítéssel) szerepel.

### 2. Gyakoriság — forrásválasztás

A brief „Károli Ószövetségben mért” Strong-gyakoriságot kér. **Strong-címkés teljes Károli-ÓSZ
nincs a `konkordancia/` alatt:** a `Karoli_Strong_kivonat.tsv` 383 adatsor (tanulmányokból
kézzel kigyűjtött kivonat). A brief szerint „közkincs vagy nyílt licencű” Strong-címkés
ószövetségi szövegből kell számolni; a menet a **`konkordancia/TAHOT_kivonat.tsv`**-t
használta (STEPBible TAHOT, CC BY 4.0; a héber/arámi szöveg szavanként Strong-címkével; a
gyakoriság = a Strong-szám sorainak száma). Ok: a héber szavak tényleges előfordulását
számolja, nem egy fordítás címkézését; a versszámozása a Károliéval egyező (magyar kulcs).
Ismert korlát: a `CLAUDE.md` szerint nem teljes (az F34 mérése szerint csak a Jób 41
hiányzik, N-F34b) — a sorrendet ez legfeljebb egy-két helyen mozdítja.

Összevetés: `konkordancia/KJV_Strongs_teljes.tsv` (közkincs, angol szavak Strong-címkéje).

| | Címkézett szó | Különböző H-szám | ebből BDB-szócikk |
|---|---|---|---|
| TAHOT | 468 968 | 8 546 | 8 003 |
| KJV | 227 196 | 8 584 | 8 025 |

A top-N halmazok átfedése (TAHOT ~ KJV): top-50: 31, top-100: 69, top-500: 444. Az eltérés
oka főként, hogy a KJV a fordításban nem megjelenő héber szavakat (névelő, `אֵת`, kötőszó,
prefixumok) nem vagy másként címkézi; a TAHOT ezeket számolja.

**Megjegyzés:** a TAHOT a prefixumokat (névelő `H9009`, `ל` elöljáró `H9005`, `ב` elöljáró
`H9003`) külön STEPBible-számmal címkézi, és a BDB-forrásnak is van ilyen kulcsú szócikke. Ezért
a sorrend élén ezek állnak. 87 BDB-szócikk TAHOT-gyakorisága 0; ezek a lista végén, Strong-szám
szerint.

### 3. Sorrend

`naplok/BDB_FORDITAS_sorrend.tsv` (`sorszam`, `strong`, `gyakorisag`, `karakter`, `adag`):
TAHOT-gyakoriság szerint csökkenő, egyenlőnél Strong-szám. Kimaradt a 26 kész szócikk (az
`adat/forditasok.tsv` BDB `teljes` sorai).

| | Szócikk | Karakter |
|---|---|---|
| Fordítandó | 8 064 | 6 198 682 |
| ebből 2 000 karakter fölött | 606 | – |
| ebből 20 000 karakter fölött | 11 | max. 45 414 (H9005) |

### 4. Szegmenshatárok (20 000 karakter fölött)

Javaslat: a vágás strukturális helyzetű (előtte `— `, `. ` vagy `; `) tagolásjelölő vagy
igetörzs-címke előtt, mohón, legfeljebb kb. 10 000 karakteres szegmensekre. A szegmens a
fordítás vázlatrésze; a kapukra és a táblába a szócikk egyben kerül (a #28 G4151/H1121
gyakorlata). Pozíció = karakter-eltolás a forrásban.

| Strong | Sorszám | Karakter | Határok (pozíció «jelölő») | Szegmenshosszak |
|---|---|---|---|---|
| H9005 | 2 | 45 414 | 8651 «b», 18603 «(β)», 28584 «(γ)», 38449 «b» | 8651/9952/9981/9865/6965 |
| H0834 | 7 | 22 469 | 8742 «c», 16954 «3» | 8742/8212/5515 |
| H3588 | 11 | 23 687 | 9357 «b», 18177 «a» | 9357/8820/5510 |
| H1961 | 12 | 24 992 | 9780 «a», 19560 «b» | 9780/9780/5432 |
| H3117 | 19 | 20 257 | 9162 «b», 16155 «h» | 9162/6993/4102 |
| H6440 | 20 | 21 162 | 9559 «b», 18093 «a» | 9559/8534/3069 |
| H5414 | 22 | 23 371 | 6520 «i», 15098 «b» | 6520/8578/8273 |
| H1980 | 27 | 43 729 | 6260 «(3)», 15367 «3», 25328 «d», 34211 «4» | 6260/9107/9961/8883/9518 |
| H4480 | 32 | 35 799 | 8886 «b», 16784 «b», 25436 «(3)», 35389 «II» | 8886/7898/8652/9953/410 |
| H7725 | 41 | 21 596 | 9957 «i», 19770 «7» | 9957/9813/1826 |
| H5920 | 3785 | 37 656 | 8153 «f», 16712 «c», 24866 «c», 34323 «b» | 8153/8559/8154/9457/3333 |

### 5. Adagok

M1 kb. 150 000 karakter, utána kb. 500 000. Szabály: a szócikk a folyó adagba kerül, ha vele
az adag nem lépi túl a célt (különben új adag nyílik); a sorrend nem változik.

| Adag | Szócikk | Karakter | Sorszám |
|---|---|---|---|
| 1 (M1) | 9 | 148 984 | 1–9 |
| 2 | 37 | 495 907 | 10–46 |
| 3 | 81 | 497 174 | 47–127 |
| 4 | 116 | 498 339 | 128–243 |
| 5 | 163 | 499 783 | 244–406 |
| 6 | 242 | 498 550 | 407–648 |
| 7 | 321 | 499 983 | 649–969 |
| 8 | 423 | 499 276 | 970–1392 |
| 9 | 591 | 499 137 | 1393–1983 |
| 10 | 847 | 499 809 | 1984–2830 |
| 11 | 1 173 | 499 684 | 2831–4003 |
| 12 | 1 693 | 499 602 | 4004–5696 |
| 13 | 2 252 | 499 559 | 5697–7948 |
| 14 | 116 | 62 895 | 7949–8064 |

Az M1 kilenc szócikke (TAHOT-gyakoriság / karakter): H9009 (23 943 / 15 815), H9005
(20 806 / 45 414), H9003 (15 766 / 18 043), H0853 (10 945 / 6 621), H3068 (6 528 / 10 103),
H0413 (5 515 / 10 139), H0834 (5 500 / 22 469), H3605 (5 412 / 12 770), H0559 (5 309 / 7 610).

**Eltérés a brief `ir` listájától:** a `naplok/BDB_FORDITAS_M0.py` mérőszkript nincs a listán
(a #34 `naplok/F34_M0_felmeres.py` mintájára készült, csak olvas).

*Helyesbítés (F38.11):* az F38.1-es szövegben a `H9005` tévesen „`ו` kötőszó” volt; a forrás
szócikke a `ל` elöljárószó („twelfth letter … preposition to, for”). Fent javítva.

## M1 — Mérő adag (F38.2–F38.11)

**Fordító:** a menet maga (Opus, `claude-opus-5-5`), subagent nélkül (brief D7). **Módszer**
(a #28 E4-e szerint, változatlan eszközlánccal): `emeles.py helyorzo` → helyőrzős vázlat →
`emeles.py ellenoriz` (javítóréteg + kapuk) → `emeles.py rogzit` → `emeles.py beir --allapot
opus`. Prompt v4, terminológia v3 (`kapu` oszloppal) — egyik sem változott. A 20 000 karakter
fölötti két szócikk (H0834, H9005) a M0 szegmenshatárai mentén több vázlatrészben készült, és
egyben került a kapukra és a táblába (a #28 G4151/H1121-gyakorlata).

**Írás:** minden szócikk saját commitban került az `adat/forditasok.tsv`-be (`allapot=opus`,
`modell=claude-opus-5-5`, `megjegyzes=F38 BDB_FORDITAS M1 (adag 1)`), utána
`eszkozok/ellenoriz.py`: SÉRTÉS 0. **Eltérés a brief `ir` listájától:** az `emeles.py rogzit`
az F28 munkatáblájába (`naplok/EMELES_munka.tsv`) ír, amely nincs a listán; a menet minden
`beir` után visszaállította (`git checkout`), így a fájl a `main` állapotában maradt. A
nézetszkript (`naplok/BDB_FORDITAS_M1_nezet.py`, csak olvas) szintén a listán kívüli.

**Számok:** 9 szócikk, forrás 148 984 karakter, fordítás 152 298 karakter (arány 1,02). Kész
összesen (BDB `teljes`): 26 + 9 = 35 szócikk; hátra 8 055 szócikk, 6 049 698 karakter.

**Önújrapróba** (a fordítás javult, nem a kapu; kapukalibrálás nem volt):

| Strong | Kapu | Eset | Javítás |
|---|---|---|---|
| H0413 | 3 Károli | „A 31:14-ben” — a nagybetűs „A” rövidítésnek látszott | „Továbbá a 31:14-ben” |
| H0413 | 5 terminológia | a forrás Megjegyzés 2. „in accusative with analogy” részlete az „in accordance with analogy” OCR-hibája; a „tárgyeset” itt hamis fordítás volna | terminológia-kivétel (`--kivetel accusative`, a prompt `bizonytalan_feloldasok` mechanizmusa, a #28 G0282 mintájára), indoklás a sor `megjegyzes` mezőjében |
| H9003 | 11 könyv | „Ex 7:29”: az „Ex” a 11. kapu leképezésében nincs, a forrásban nem számít; a fordítás „2Móz”-a többletnek számított | a forrás alakja maradt („Ex 7:29”) |

**Nem leképezett forrásbeli könyvalakok** (a 11. kapu leképezésében nincsenek, ezért a fordítás
változatlanul hagyta őket, a 3. kapu „forrásbeli szigla igehely előtt” ágon fogadta el): `Ex`
(H9003), `Cant` (H9003), `1Chron`, `2 Chron` (H3605), `Kings`, `Malachi` (H0834), továbbá a
nem bibliai `Qor`, `Ab`, `Aboth`, `Yoma`, `Tariff`. Ezek közül az `Ex`, `Cant`, `1Chron`,
`Kings`, `Malachi` valódi bibliai könyvnév, amely Károli-rövidítést kapna, ha a leképezés
ismerné — kérdés a DT-F38 (c) pontjában.

**Forráshiba a fordításban, hűen átvéve** (13. kapu JELZES, nem gátoló; mind az F34
maradékában vagy az N-F34c körében): H9009 1Kir 45, 59, 61, 66 (Zsolt); H9005 Hab 41 (1Móz),
Jóel 9 (Zsolt); H0413 5Móz 37 (1Móz); H0834 Ruth 8, 9 (Préd). Továbbá a 13. kapu által nem
látott, de nyilvánvaló hibák: H0413 „1Sám 3:22; 5:26; 15:22; 29:19” (Jób-helyek), H3605
„1Chron 119:21; 145:9” (Zsolt), „2 Chron 21:43” (Józs), H3068 „1Móz 21:83” (21:33).

**Gyakoriság és sorrend megjegyzés:** az M1 első három szócikke a TAHOT prefixum-számai
(`H9009` névelő, `H9005` `ל`, `H9003` `ב`), mert a TAHOT ezeket külön számolja. Ha a
felhasználó szerint ezek nem a „legtöbbet használt szavak” közé valók, a sorrend a DT-F38 (d)
szerint módosítható (a kész fordítás ettől nem vész el).

**Keretmérés:** a brief szerint a felhasználó olvassa le a kreditet az adag előtt és után; a
menet nem lát kreditet. Tájékoztató számok a becsléshez: a kimenet kb. 152 ezer karakter magyar
szöveg (helyőrzős vázlatként kb. 120 ezer), a szócikkenkénti munka 1–2 kapufutással.

*Az alábbi két alszakasz a `python naplok/BDB_FORDITAS_M1_nezet.py --adag 1 --minta 5 --seed 38` kimenete (a forrás blockquote-ban, alatta a fordítás, a tagolásjelölőknél igazítva).*

### Kapueredmények (adag 1, 9/9 szócikk kész)

| Strong | Forrás kar. | Fordítás kar. | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 | 11 | 12 | 13 | Átment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H9009 | 15815 | 15892 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H9005 | 45414 | 47276 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H9003 | 18043 | 18016 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0853 | 6621 | 6767 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3068 | 10103 | 10449 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0413 | 10139 | 10387 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H0834 | 22469 | 22332 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.99) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H3605 | 12770 | 12978 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0559 | 7610 | 8201 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |

Összesen: forrás 148984, fordítás 152298 karakter.

13. kapu (JELZES, nem gátoló): H9009 — a könyv fejezetszámánál nagyobb fejezet: 1Kir 45, 1Kir 59, 1Kir 61, 1Kir 66; H9005 — a könyv fejezetszámánál nagyobb fejezet: Hab 41, Jóel 9; H0413 — a könyv fejezetszámánál nagyobb fejezet: 5Móz 37; H0834 — a könyv fejezetszámánál nagyobb fejezet: Ruth 8, Ruth 9.

Terminológia-kivétel: H0413 — accusative.

### Minta (5 szócikk, seed=38, hossz szerinti harmadokból): H0853 (6621), H3068 (10103), H3605 (12770), H0834 (22469), H9005 (45414)

#### H0853 (6621 → 6767 karakter)

`forras_hash=b2c243e9ce120175d4bd61c012ccf80e167fec69` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v3`

**1.** 

> H853. eth I. אֵת, with makk. אֶתֿ, with suffix אֹתִי; אֹתְכָה אֹתְךָ, Num 22:33, אֹתָ֑כָה אֹתָ֑ךְ, Exod 29:35, feminine אֹתָךְ; אֹתוֺ etc.; 2 plural אֶתְכֶם, once אוֺתְכֶם Josh 23:15; 3masculine plural regularly אֹתָם, rarely אֶתְהֶם Gen 32:1; Exod 18:20; Num 21:3; Ezek 34:12; 1Chr 6:50, once אוֺתְהֶם Ezek 23:45; 3feminine plural, on the contrary, regularly אֶתְהֶן (13 t.), once אֹתָן 16:54 (also אוֺתְהֶן 23:47, אֹתָ֖נָה Exod 35:26, אוֺתָ֖נָה Ezek 34:21); forms with cholem also often written plene: — the mark of the accusative, prefixed as a rule only to nouns that are definite (Moabite id., Phoenician אית i.e. אִיַּת (Schröd^p. 213 f.); Aramaic יָת frequently in ᵑ7; Syriac very rare as mark of accusative (for which is preferred), but used often in the sense of substance οὐσία, also in that of self, e.g. per se, reapse, sibi ipsi, PS^1640f., Samaritan ; Arabic , only used with suffix, when it is desired to emphasize the pronoun, e.g. Qor 1:4 W^AG i. § 189. [Ethiopic uses k£y¹ similarly, Di^§ 150 a; but it is dubious if this is etymologically akin.] The primitive form will have been 'iwyath, originally a substantive with following Genitive, Ol^p. 432; whether ultimately a parallel development with אוֺת sign from √ אוה is uncertain: Ol W^AG i. § 188 Lag^M i. 226 affirm, Nö^ZMG 1886, 738 doubts. In Hebrew the ground-form is אוֺת; the forms with ¢, e being abbreviated. In post Biblical Hebrew, used in combination with another preposition: thus הַיּוֺם בְּאוֺתוֺ = Bibl. הַשָּׁעָה בְּאוֺתָהּ הַהוּא, בַּיּוֺם; or as a nomin., e.g. הָאִישׁ אוֺתוֺ = Bibl. הַהוּא הָאִישׁ). 1 As mark of the accusative prefixed to substantives defined either by the article (or כֹּל), or by a Genitive or pronominal affix, or in virtue of being proper names:

H853. eth I. אֵת, makkeffel אֶתֿ, suffixummal אֹתִי; אֹתְכָה אֹתְךָ, 4Móz 22:33, אֹתָ֑כָה אֹתָ֑ךְ, 2Móz 29:35, nőnemű אֹתָךְ; אֹתוֺ stb.; 2. többes szám אֶתְכֶם, egyszer אוֺתְכֶם Józs 23:15; 3. hímnemű többes szám rendszerint אֹתָם, ritkán אֶתְהֶם 1Móz 32:1; 2Móz 18:20; 4Móz 21:3; Ez 34:12; 1Krón 6:50, egyszer אוֺתְהֶם Ez 23:45; a 3. nőnemű többes szám ellenben rendszerint אֶתְהֶן (összesen 13-szor), egyszer אֹתָן 16:54 (továbbá אוֺתְהֶן 23:47, אֹתָ֖נָה 2Móz 35:26, אוֺתָ֖נָה Ez 34:21); a holemes alakokat gyakran plene is írják: — a tárgyeset jele, amely szabály szerint csak határozott főnevek előtt áll (moábi ua., föníciai אית, azaz אִיַּת (Schröd^213. o. k.); arámi יָת, gyakran a ᵑ7-ban; a szírben tárgyesetjelként nagyon ritka (helyette inkább a használatos), de gyakran használják a lényeg, οὐσία értelmében, továbbá önmaga értelmében is, pl. per se, reapse, sibi ipsi, PS^1640k., szamaritánus ; arab , csak suffixummal használják, ha a névmást nyomatékosítani akarják, pl. Qor 1:4 W^AG i. § 189. [Az etióp hasonlóan használja a k£y¹ alakot, Di^§ 150 a; de kétséges, hogy etimológiailag rokon-e vele.] Az ősalak 'iwyath lehetett, eredetileg főnév, amelyet birtokos eset követett, Ol^432. o.; hogy végső soron a √ אוה tőből való אוֺת, jel szóval párhuzamos fejlemény-e, bizonytalan: Ol, W^AG i. § 188 és Lag^M i. 226 állítja, Nö^ZMG 1886, 738 kétli. A héberben az alapalak אוֺת; a ¢, e magánhangzós alakok rövidültek. A Biblia utáni héberben más elöljárószóval együtt használják: így הַיּוֺם בְּאוֺתוֺ = bibl. הַשָּׁעָה בְּאוֺתָהּ הַהוּא, בַּיּוֺם; vagy nominativusként, pl. הָאִישׁ אוֺתוֺ = bibl. הַהוּא הָאִישׁ). 1 A tárgyeset jeleként olyan főnevek előtt áll, amelyeket vagy a névelő (vagy כֹּל), vagy birtokos szó vagy névmási affixum, vagy az tesz határozottá, hogy tulajdonnevek:

**2.** 

> a. with transitive verbs, Gen 1:1, 16, 29, 30; 2:11; 4:1-2, 9:3 (אֶתֿכֹּל׃) etc. Similarly אֶתמִֿי whom (in particular), Josh 24:15; 1Sam 12:3; 28:11; Isa 6:8 and elsewhere (but never אֶתמָֿה); also with זֶה Gen 29:33; 44:29; 1 Samuel 21:16; 1Kin 22:27 +, זֹאת Gen 29:27; 2Sam 13:27 +, אֵלֶּה Gen 46:18; Lev 11:18; Isa 49:21 +. So pretty uniformly in prose; but in poetry את is commonly dispensed with. By the use of את with the pronominal affix, a pronoun can at once, if required, be placed in a position of emphasis; let the order of words from this point of view be carefully noticed in the following passages: Gen 7:1; 24:14; 37:4; Lev 10:17; 11:33; Num 22:32 thee I had slain, and her I had kept alive, Deut 4:14; 6:13, 23; 13:5; Judg 14:3 לִי קַח אוֺתָהּ take for me her, 1Sam 14:35; 15:1; 18:17; 21:10 קָ֔ח תִּקַּחלְֿךָ אִםאֹֿתָהּ if thou wilt take that, take it, 1Kin 1:35; 14:9; Isa 43:22; 57:11; Jer 9:2. So הַאוֺתִי 5:22; 7:19. It also sometimes enables the reflexive sense to be expressed (elsewhere נַפְשָׁם) 7:19; Ezek 34:2. Rarely with a substantive which is undefined (Ew^§ 277 d 2 Ges^§ 117, 1, R. 2), as Exod 21:28; Num 21:9; Lev 20:14; 1Sam 24:6 (but see Dr) 2Sam 4:11; 18:18; 23:21; or which, though definite, is without the article, Gen 21:30; 2Sam 15:16; Lev 26:5; 1Sam 9:3 (so Num 16:15) Isa 33:19; 41:7; Ezek 43:10 (for further examples see Ew 1.c.)

a. tárgyas igékkel, 1Móz 1:1, 16, 29, 30; 2:11; 4:1-2, 9:3 (אֶתֿכֹּל׃) stb. Hasonlóképpen אֶתמִֿי kit (közelebbről), Józs 24:15; 1Sám 12:3; 28:11; Ézs 6:8 és máshol (de soha nem אֶתמָֿה); továbbá זֶה előtt 1Móz 29:33; 44:29; 1Sám 21:16; 1Kir 22:27 és máshol, זֹאת előtt 1Móz 29:27; 2Sám 13:27 és máshol, אֵלֶּה előtt 1Móz 46:18; 3Móz 11:18; Ézs 49:21 és máshol. A prózában tehát meglehetősen egységesen; a költészetben viszont az את rendszerint elmarad. Az את névmási affixummal való használata révén a névmás szükség esetén egyszerre nyomatékos helyre állítható; a szórendet ebből a szempontból gondosan meg kell figyelni a következő helyeken: 1Móz 7:1; 24:14; 37:4; 3Móz 10:17; 11:33; 4Móz 22:32 téged öltelek volna meg, őt pedig életben hagytam volna, 5Móz 4:14; 6:13, 23; 13:5; Bír 14:3 לִי קַח אוֺתָהּ őt vedd el nekem, 1Sám 14:35; 15:1; 18:17; 21:10 קָ֔ח תִּקַּחלְֿךָ אִםאֹֿתָהּ ha azt akarod elvenni, vedd el, 1Kir 1:35; 14:9; Ézs 43:22; 57:11; Jer 9:2. Így הַאוֺתִי 5:22; 7:19. Néha a visszaható értelem kifejezését is lehetővé teszi (máskor נַפְשָׁם) 7:19; Ez 34:2. Ritkán határozatlan főnévvel (Ew^§ 277 d 2 Ges^§ 117, 1, R. 2), mint 2Móz 21:28; 4Móz 21:9; 3Móz 20:14; 1Sám 24:6 (de l. Dr) 2Sám 4:11; 18:18; 23:21; vagy olyannal, amely határozott ugyan, de névelő nélkül áll, 1Móz 21:30; 2Sám 15:16; 3Móz 26:5; 1Sám 9:3 (így 4Móz 16:15) Ézs 33:19; 41:7; Ez 43:10 (további példákat l. Ew 1.c.)

**3.** 

> b. with a passive verb (Ges^§ 121. 1 Ew^§ 295 b) conceived as expressing neutrally the action in question, and construed accordingly with an accusative of that which is its real object: examples occur with tolerable frequency from Gen 4:18 (J) אֶתעֿירָד לַחֲנוֺךְ וַיִּוָּלֵד, 17:5 (P), אַברָם אֶתשִֿׁמְךָ עוֺד יִקָּרֵא לֹא there shall not be called (=one shall not call) thy name Abram, 21:5 (E), 27:42; 2Sam 21:11; 1Kin 18:13; Hosea 10:6 etc., to Jer 35:18; 38:4; 50:20; Ezek 16:4-5, Est 2:13 (compare Dr^JPh xi. 227 f.): also with passive verbs of filling (Ew^§ 281 b), as Exod 1:7 +.

b. szenvedő igével (Ges^§ 121. 1 Ew^§ 295 b), amelyet úgy fognak fel, mint ami semlegesen fejezi ki a szóban forgó cselekvést, és ennek megfelelően annak tárgyesetével szerkesztik, ami valódi tárgya: elég gyakran előfordulnak példák, kezdve 1Móz 4:18-cal (J) אֶתעֿירָד לַחֲנוֺךְ וַיִּוָּלֵד, 17:5 (P), אַברָם אֶתשִֿׁמְךָ עוֺד יִקָּרֵא לֹא nem neveztetik (= nem nevezik) a te neved Abrámnak, 21:5 (E), 27:42; 2Sám 21:11; 1Kir 18:13; Hós 10:6 stb., egészen Jer 35:18; 38:4; 50:20; Ez 16:4-5, Eszt 2:13-ig (vö. Dr^JPh xi. 227 k.): a megtöltés szenvedő igéivel is (Ew^§ 281 b), mint 2Móz 1:7 és máshol.

**4.** 

> c. with neuter verbs or expressions, especially such as involve the idea of regarding, or treating, appy. by a construction κατὰ σύνεσιν (rare), Josh 22:17; 2Sam 11:25; Neh 9:32 (compare 1Sam 20:13 Dr). Once after אֵין, Hag 2:17; אֵלַיָֽ אֶתְכֶם אֵין.

c. tárgyatlan igékkel vagy kifejezésekkel, különösen olyanokkal, amelyekben a tekintés vagy a bánásmód gondolata rejlik, nyilván κατὰ σύνεσιν szerkesztéssel (ritka), Józs 22:17; 2Sám 11:25; Neh 9:32 (vö. 1Sám 20:13 Dr). Egyszer אֵין után, Hag 2:17; אֵלַיָֽ אֶתְכֶם אֵין.

**5.** 

> d. poet. (si vera lectio), after an abstract noun used with a verbal force, Hab 3:13 (Amos 4:11; Isa 13:19; Jer 50:40 מַהְמֵּכָה exerts a verbal force, like the Arabic nom. verbi [see W^AG i. § 196, 43]; and Num 10:2; Ezek 17:9 לְמַשְׂאוֺת לְמַסַּע, are Aramaizing infinitives: compare Ew^§ 239 a). 2 את marks an accusative in other relations than that of direct object to a verb:

d. költőien (si vera lectio), igei erővel használt elvont főnév után, Hab 3:13 (Ámós 4:11; Ézs 13:19; Jer 50:40 a מַהְמֵּכָה igei erővel bír, mint az arab nomen verbi [l. W^AG i. § 196, 43]; a 4Móz 10:2; Ez 17:9 לְמַשְׂאוֺת לְמַסַּע pedig arámaizáló infinitivusok: vö. Ew^§ 239 a). 2 את a tárgyesetet az ige közvetlen tárgyán kívül más viszonyokban is jelöli:

**6.** 

> a. with verbs of motion (very rare) Num 13:17; Deut 1:19; 2:7 (to 'walk the wilderness'); denoting the goal Judg 19:18; Ezek 21:25 (Ew^§ 281 d, n., 282 a 1).

a. mozgást jelentő igékkel (nagyon ritka) 4Móz 13:17; 5Móz 1:19; 2:7 ('bejárni a pusztát'); a célt jelölve Bír 19:18; Ez 21:25 (Ew^§ 281 d, n., 282 a 1).

**7.** 

> b. denoting time (duration), also very rare: Exod 13:7; Lev 25:22; Deut 9:25.

b. időt (időtartamot) jelölve, szintén nagyon ritka: 2Móz 13:7; 3Móz 25:22; 5Móz 9:25.

**8.** 

> c. expressing the accus. of limitation (rare): Gen 17:11, 14; 1Kin 15:23. 3 Chiefly in an inferior or later style, אֵת (or וְאֵת) is used irregularly, partly (α), as it would seem, to give greater definiteness (so especially וְאֵת) at the mention of a new subject (when it may sometimes be rendered as regards), or through the influence of a neighbouring verb (a construct κατὰ σύνεσιν), or by an anacoluthon, partly (β) as resuming loosely some other preposition Thus (α) Exod 1:14; Num 3:26, 46; 5:10 (with הָיָה: so Ezek 35:10) Num 18:21b Deut 11:2 (anacoluthon), 14:13; Josh 17:11; Judg 20:44, 46 (contr. 20:25; 20:35) 1Sam 17:34 (see Dr) 26:16; 2Sam 21:22; 2Kin 6:5; Isa 53:8 (probably), 57:12; Jer 23:33 (but read rather with הַמַּשָּׂא אַתֶּם ᵑ9 ᵐ5) 27:8; 36:22; 38:16 Kt, 45:4 b Ezek 16:22; 17:21; 20:16; 29:4; b 43:7 (ᵐ5 Co prefix הֲרָאִיתָ) 44:3; Zech 8:17; Eccl 4:3; Dan 9:13; Neh 9:19, 34; 1Chr 2:9; 2Chr 31:17. In 1Sam 30:23; Hag 2:5 probably some such word as remember is to be understood.

c. a vonatkozás tárgyesetét kifejezve (ritka): 1Móz 17:11, 14; 1Kir 15:23. 3 Főként alacsonyabb rendű vagy későbbi stílusban az אֵת (vagy וְאֵת) szabálytalanul használatos: részint (α), úgy látszik, nagyobb határozottság kedvéért (így különösen וְאֵת) egy új alany említésekor (ilyenkor néha az ami illeti fordulattal adható vissza), vagy egy szomszédos ige hatására (κατὰ σύνεσιν szerkesztés), vagy anakoluthon révén; részint (β) valamely más elöljárószót lazán felvéve. Így (α) 2Móz 1:14; 4Móz 3:26, 46; 5:10 (הָיָה mellett: így Ez 35:10) 4Móz 18:21b 5Móz 11:2 (anakoluthon), 14:13; Józs 17:11; Bír 20:44, 46 (ellentétben: 20:25; 20:35) 1Sám 17:34 (l. Dr) 26:16; 2Sám 21:22; 2Kir 6:5; Ézs 53:8 (valószínűleg), 57:12; Jer 23:33 (de inkább olv. הַמַּשָּׂא אַתֶּם ᵑ9 ᵐ5 szerint) 27:8; 36:22; 38:16 Kt, 45:4 b Ez 16:22; 17:21; 20:16; 29:4; b 43:7 (ᵐ5 Co prefixummal: הֲרָאִיתָ) 44:3; Zak 8:17; Préd 4:3; Dán 9:13; Neh 9:19, 34; 1Krón 2:9; 2Krón 31:17. Az 1Sám 30:23; Hag 2:5 helyen valószínűleg valami olyan szót kell érteni, mint emlékezz.

**9.** 

> (β) Jer 38:9; Ezek 14:22; b 37:19 b Zech 12:10; אֵת סָבִיב 1Kin 6:5; Ezek 43:17 strangely (in 1Kings ᵐ5 omits the clause: so Sta^ZAW 1883, 135). — In 1Kin 11:1 וְ is merely and also, and especially (see וְ); 11:25 is corrupt (read with הֲדָד עָשָׂה אֲשֶׁר הָרָעָה זֹאת ᵐ5); Ezek 47:17-18, 19 read similarly for זֹאת ואת,: see 47:20. — For some particulars as to the use of את, see A. M. Wilson^Hebraica. vi. 139 ff. 212 ff. (who, however, confuses it sometimes with II. אֵת). For denoting the pronominal object of a verb, את with suffix preponderates relatively much above the verbal affix in P, as compared with J E Deuteronomy Judges Samuel Kings (see Gie^ZAW 1881, 258 f.), — partly, probably, on account of the greater distinctness and precision which P loves. יָת mark of accusative (= Biblical Hebrew I. אֵת; Palmyrene ית; Zinjirli^Had.

(β) Jer 38:9; Ez 14:22; b 37:19 b Zak 12:10; אֵת סָבִיב 1Kir 6:5; Ez 43:17 különös módon (a Királyok első könyvében ᵐ5 kihagyja a mondatrészt: így Sta^ZAW 1883, 135). — Az 1Kir 11:1-ben a וְ egyszerűen és is, és különösen (l. וְ); a 11:25 romlott (olv. ᵐ5 szerint הֲדָד עָשָׂה אֲשֶׁר הָרָעָה זֹאת); az Ez 47:17-18, 19 helyen hasonlóan olv. זֹאת ואת helyett,: l. 47:20. — Az את használatának néhány részletéről l. A. M. Wilson^Hebraica. vi. 139 kk. 212 kk. (aki azonban néha összetéveszti a II. אֵת szóval). Az ige névmási tárgyának jelölésére a P-ben az את suffixummal viszonylag sokkal gyakoribb az igei affixumnál, mint J-ben, E-ben, a Deuteronomiumban, a Bírák, Sámuel és a Királyok könyvében (l. Gie^ZAW 1881, 258 k.), — részben valószínűleg azért, mert a P szereti a nagyobb világosságot és pontosságot. יָת a tárgyeset jele (= bibliai héber I. אֵת; palmürai ית; Zendzsirli^Had.

**10.** 

> 28 with suffix ותה; Nabataean, Palmyrene with suffix יתה (Lzb^263 Cooke^170; compare RÉS^468); ᵑ7 Samaritan יָת; Syriac (rare)); — Dan 3:12 יָָֽתְהוֺן מַנִּיתָ דִּי whom thou hast appointed.

28 suffixummal ותה; nabateus, palmürai suffixummal יתה (Lzb^263 Cooke^170; vö. RÉS^468); ᵑ7, szamaritánus יָת; szír (ritka)); — Dán 3:12 יָָֽתְהוֺן מַנִּיתָ דִּי akit kirendeltél.

#### H3068 (10103 → 10449 karakter)

`forras_hash=b7d5d55c05c62831b0ae5b513a9a399b4166cf3d` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v3`

**1.** 

> H3068. Yhvh יהוה_c. 6823 i.e. יַהְוֶה proper name, of deity Yahweh, the proper name of the God of Israel — ( 1 יְהוָֺה ᵑ0^C518 (Qr אֲדֹנָי), or יֱהוִֺה_305 (Qr אֱלֹהִים), in the combinations יהוה אדני & אדני יהוה (see אֲדֹנֶי), and with preposition מֵיהוָֺה לַיהוָֺה, בַּיהוָֺה, (Qr מֵאדֹנָי לַאדֹנָי, בַּאדֹנָי,), do not give the original form. ᵐ5 and other Vrss follow the Qr. On the basis of Exod 20:7; Lev 24:11 יהוה was regarded as a nomen ineffabile (see Philo^de Vita Mosis iii. 519, 529), called by the Jews הַשֵּׁם and by the Samaritans שׁימא. The pronunciation Jehovah was unknown until 1520, when it was introduced by Galatinus; but it was contested by Le Mercier, J. Drusius, and L. Capellus, as against grammatical and historical propriety (compare Bö^§ 88). The traditional Ἰαβέ of Theodoret and Epiphanius, the יְהוֺֿ יָֿהוּ, of compound proper name and the contracted form יָהּ all favour יַהְוֶךְ (compare יַהֲלֹמ֑וּן Psa 74:6; תַּהֲרוּ Isa 33:11), see Lag^Sym i.14 Baud^Studien i.179 ff.; Dr^Stud.Bib.i.1 ff. For Jeve see Sta^ZAW 1881, 346 De^ib.1882, 173 f. & Gn. Excurs. ii.

H3068. Yhvh יהוה_c. 6823, azaz יַהְוֶה tulajdonnév, istennév: Jahve, Izráel Istenének tulajdonneve — ( 1 A יְהוָֺה ᵑ0^C518 (Qr אֲדֹנָי) vagy יֱהוִֺה_305 (Qr אֱלֹהִים) alak a יהוה אדני és אדני יהוה kapcsolatokban (l. אֲדֹנֶי), valamint elöljárószóval מֵיהוָֺה לַיהוָֺה, בַּיהוָֺה, (Qr מֵאדֹנָי לַאדֹנָי, בַּאדֹנָי,) nem az eredeti alakot adja. A ᵐ5 és más Vrss a Qr-t követik. A 2Móz 20:7; 3Móz 24:11 alapján a יהוה nomen ineffabile-nek számított (l. Philón^de Vita Mosis iii. 519, 529); a zsidók הַשֵּׁם, a szamaritánusok שׁימא néven emlegették. A Jehova kiejtés 1520-ig ismeretlen volt, ekkor Galatinus vezette be; Le Mercier, J. Drusius és L. Capellus azonban vitatta, mint ami ellenkezik a nyelvtani és történeti szabályszerűséggel (vö. Bö^§ 88). Theodorétosz és Epiphaniosz hagyományos Ἰαβέ alakja, az összetett tulajdonnevek יְהוֺֿ יָֿהוּ, eleme és a יָהּ összevont alak mind a יַהְוֶךְ mellett szól (vö. יַהֲלֹמ֑וּן Zsolt 74:6; תַּהֲרוּ Ézs 33:11), l. Lag^Sym i.14 Baud^Studien i.179 kk.; Dr^Stud.Bib.i.1 kk. A Jeve alakról l. Sta^ZAW 1881, 346 De^ib.1882, 173 k. és Gn. Excurs. ii.

**2.** 

> 2 on literature of interpretations see Nes^Eg.67 Dr^l.c. — Many recent scholars explain יַהְוֶה as Hiph`il of היה (=היה) the one bringing into being, life-giver (compare חַוָּה Gen 3:20) Schr HSch; giver of existence, creator, Kue Tiele; he who brings to pass (so already Le Clerc),performer of his promises, Lag, Nes^Eg.88 (but Nes^Eg.91 inclines to Qal as RS^Brit. & For. Ev. Rev see below); or from היה he who causes to fall, rain or lightning RS^OTJC.ed.1, 423; om.ed.2, 245, compare We^Skizzen iii.175; 'Fäller,' destroying foes, Sta^G.i.429 (dubiously). But most take it as Qal of הוה (= היה); the one who is: i.e. the absolute and unchangeable one, Ri; the existing, ever living, as self-consistent and unchangeable, Di; or the one ever coming into manifestation as the God of redemption, De Oehl; compare also RS^Brit. & For. Ev. Rev. 1876, he will be it, i.e all that his servants look for (compare Ew^infr), he will approve himself (give evidence of being, assert his being Dr^l.c.17)). **Theories of non-Hebrew or non-Semitic origin, opposed (in their older forms) by Bau^Rel.

2 az értelmezések irodalmáról l. Nes^Eg.67 Dr^l.c. — Sok újabb tudós a יַהְוֶה alakot a היה (=היה) Hiph`il alakjaként magyarázza: aki létre hív, életadó (vö. חַוָּה 1Móz 3:20) Schr HSch; a létezés adója, teremtő, Kue Tiele; aki véghez visz (így már Le Clerc), ígéreteinek beteljesítője, Lag, Nes^Eg.88 (de Nes^Eg.91 a Qal felé hajlik, mint RS^Brit. & For. Ev. Rev, l. lent); vagy a היה tőből: aki hullani hagyja az esőt vagy a villámot RS^OTJC.ed.1, 423; om.ed.2, 245, vö. We^Skizzen iii.175; 'Fäller,' az ellenségek elpusztítója, Sta^G.i.429 (kétkedve). A legtöbben azonban a הוה (= היה) Qal alakjának tartják: aki van, azaz az abszolút és változatlan, Ri; a létező, örökké élő, mint önmagával azonos és változatlan, Di; vagy aki a megváltás Isteneként mindig újra megnyilvánul, De Oehl; vö. még RS^Brit. & For. Ev. Rev. 1876: ő az lesz, azaz minden, amit szolgái várnak (vö. Ew^infr), igazolni fogja magát (bizonyságot ad létéről, érvényesíti létét Dr^l.c.17)). **A nem héber vagy nem sémi eredetről szóló elméletek; ezeknek (régebbi formájukban) ellentmond Bau^Rel.

**3.** 

> i. 181 ff. (see especially 230); Dl^Pa 162 ff. claimed Babylonian origin for יהו, against this Kue^national Religions, etc., Note iv (Eng. Trans. 329 ff.) Jastr^JBL xiil {1894}, 103 f. compare Hpt^BAS i. 170 N; Dl^Babel u. Bibel, 46 f., 73 f. makes same claim for יהוה, against this see especially Hirsch^ZAW xxiil {1903}, 355 ff. Zim^KATS. 465 ff.; Spiegelb^ZMG:liii {1899}, 633 ff. proposes (improbable) Egyptian etymology for יהוה; further discussions see in Kö^EB NAMES, § 112 and n.3. 'Jehovah' found in Jacob (? Johannes) Wessel († 1480), according to Schw^ThLZ, 1905, col. 612.

i. 181 kk. (l. különösen 230); Dl^Pa 162 kk. babiloni eredetet tulajdonított a יהו alaknak, ez ellen Kue^national Religions stb., Note iv (Eng. Trans. 329 kk.) Jastr^JBL xiil {1894}, 103 k., vö. Hpt^BAS i. 170 N; Dl^Babel u. Bibel, 46 k., 73 k. ugyanezt állítja a יהוה alakról, ez ellen l. különösen Hirsch^ZAW xxiil {1903}, 355 kk. Zim^KATS. 465 kk.; Spiegelb^ZMG:liii {1899}, 633 kk. (valószínűtlen) egyiptomi etimológiát javasol a יהוה számára; további tárgyalások: Kö^EB NAMES, § 112 és n.3. A 'Jehovah' alak Jacob (? Johannes) Wesselnél († 1480) található, Schw^ThLZ, 1905, col. 612 szerint.

**4.** 

> I. יהוה is not used by E in Genesis, but is given Exod 3:12-15 as the name of the God who revealed Himself to Moses at Horeb, and is explained thus : עִמָּ֑ךְ אֶהְיֶה I shall be with thee (3:12), which is then implied in אֶהְיֶה אֲשֶׁר אֶהְיֶה I shall be the one who will be it 3:14a (i.e: with thee 3:12) and then compressed into אֶהְיֶה 3:14b (i.e. with thee 3:12), which then is given in the nominal form יהוה He who will be it 3:15 (i.e. with thee 3:12). compare Ew^BTh ii. 337, 338 RS^l.c., Proph. 385 ff. Other interpretations are: I am he who I am, i.e. it is no concern of yours (Le Clerc Lag^Psalt.Hieron.156); I am (this is my name), inasmuch as I am (אֲשֶׁר = כִּי; AE JDMich We^JD Th xxi, 540 = compare Hexateuch 72); Di and others I am who I am, he who is essentially unnameable, inexplicable, — E uses יהוה sparingly by the side of אלהים and האלהים in his subsequent narrative. The Ephraimitic writers in Judges Samuel Kings use it in similar proportions. P abstains from the use of יהוה until he gives an account of its revelation to Moses 6:3; but subsequently uses it freely. He gives no explanation of its meaning. He represents that שַׁדַּי אֵל was the God of the patriarchs. J uses יהוה from the beginning of his narrative, possibly explaining it, Genesis 21:83 by עולם אל, the evergreen tamarisk being a symbol of the ever-living God; compare De Gen 21:33. Elsewhere יהוה is the common divine name in pre-exilic writers, but in post-exilic writers gradually falls into disuse, and is supplanted by אלהים and אדני. In Job it is used 31 t. in prose parts, and Job 12:9 (a proverb); not elsewhere in the poem. Chronicles apart from his sources prefers אלהים and האלהים. Daniel uses יהוה only in chap. 9 (7 t.); Ecclesiastes not at all. In the Elohistic group of Psalm 42-83 it is used 39 t. (see אלהים) . It occurs as the name of Israel's God MI^18. It is doubtful whether it was used by other branches of the Shemitic family, compare COT Gen 2:4b Dl^Pa 158 ff. Dr^Stud. Bib.

I. A יהוה nevet E a Genezisben nem használja, de a 2Móz 3:12-15 helyen annak az Istennek a neveként adja meg, aki Hórebnél kinyilatkoztatta magát Mózesnek, és így magyarázza: עִמָּ֑ךְ אֶהְיֶה veled leszek (3:12), amit azután a אֶהְיֶה אֲשֶׁר אֶהְיֶה az leszek, aki az lesz 3:14a (azaz: veled 3:12) foglal magában, majd a אֶהְיֶה 3:14b sűrít össze (azaz veled 3:12), és ezt végül a יהוה névszói alak adja vissza: aki az lesz 3:15 (azaz veled 3:12). vö. Ew^BTh ii. 337, 338 RS^l.c., Proph. 385 kk. Más értelmezések: az vagyok, aki vagyok, azaz semmi közöd hozzá (Le Clerc Lag^Psalt.Hieron.156); vagyok (ez a nevem), mivel vagyok (אֲשֶׁר = כִּי; AE JDMich We^JD Th xxi, 540 = vö. Hexateuch 72); Di és mások: az vagyok, aki vagyok, aki lényegénél fogva megnevezhetetlen, megmagyarázhatatlan, — E a későbbi elbeszélésében a יהוה nevet takarékosan használja a אלהים és a האלהים mellett. A Bírák, Sámuel és a Királyok könyvének efraimi írói hasonló arányban használják. P tartózkodik a יהוה használatától, amíg be nem számol a név Mózesnek adott kinyilatkoztatásáról 6:3; azután azonban szabadon használja. Jelentésére nem ad magyarázatot. Úgy ábrázolja, hogy שַׁדַּי אֵל volt az ősatyák Istene. J elbeszélése kezdetétől használja a יהוה nevet, és talán meg is magyarázza, 1Móz 21:83, a עולם אל kifejezéssel, mivel az örökzöld tamariszkusz az örökké élő Isten jelképe; vö. De 1Móz 21:33. Egyébként a יהוה a fogság előtti íróknál a szokásos istennév, a fogság utáni íróknál azonban fokozatosan kiszorul a használatból, és helyét a אלהים és az אדני veszi át. Jóbnál a prózai részekben 31-szer fordul elő, továbbá Jób 12:9 (közmondás); a költeményben máshol nem. A Krónikák írója a forrásain kívül a אלהים és a האלהים nevet részesíti előnyben. Dániel a יהוה nevet csak a 9. fejezetben használja (7-szer); a Prédikátor egyáltalán nem. A Zsoltárok 42-83 elohista csoportjában 39-szer használatos (l. אלהים) . Izráel Istenének neveként előfordul: MI^18. Kétséges, hogy a sémi család más ágai használták-e, vö. COT 1Móz 2:4b Dl^Pa 158 kk. Dr^Stud. Bib.

**5.** 

> i.

i.

**6.** 

> 7 ff.

7 kk.

**7.** 

> II.

II.

**8.** 

> 1. יהוה is used with אלהים and suffixes, especially in D;

1. A יהוה az אלהים szóval és suffixumokkal együtt is használatos, különösen D-ben;

**9.** 

> a. with אֱלֹהֶיךָ in the Ten Words Exod 20:2-12 (5 t.) = Deut 5:6-16; in the law of worship of J E, Exod 23:19; 34:24, 26; in D 234 t.; Josh 1:9, 17; 9:9, 24 (D^2); elsewhere Gen 27:20; Exod 15:26 (JE), Judg 6:26; Samuel & Kings 20 t.; 1Chr 11:2; 22:11-12, 2Chr 9:8 (twice in verse); 16:7; Isa 7:11; 37:4 (twice in verse); 41:13; 43:3; 51:15; 55:5; Jer 40:2 + (3t.); Hosea 12:10; 13:4; 14:2; Amos 9:15; Psa 81:11.

a. אֱלֹהֶיךָ alakkal a Tízigében 2Móz 20:2-12 (5-ször) = 5Móz 5:6-16; J E istentiszteleti törvényében, 2Móz 23:19; 34:24, 26; D-ben 234-szer; Józs 1:9, 17; 9:9, 24 (D^2); máshol 1Móz 27:20; 2Móz 15:26 (JE), Bír 6:26; Sámuel és a Királyok könyvében 20-szor; 1Krón 11:2; 22:11-12, 2Krón 9:8 (a versben kétszer); 16:7; Ézs 7:11; 37:4 (a versben kétszer); 41:13; 43:3; 51:15; 55:5; Jer 40:2 és máshol (3-szor); Hós 12:10; 13:4; 14:2; Ámós 9:15; Zsolt 81:11.

**10.** 

> b. with אֱלֹהֵיכֶם in D 46 t.; D^228t.; H 15 t.; P 15 t.; elsewhere Exod 23:25 (E); 8:24; 10:8, 16, 17 (JE); Judg 6:10; 1Sam 12:12, 14; 2Kin 17:39; 23:21; 1Chr 22:18 + (10 t. Chronicles) Psa 76:12; Jer 13:16 + (5 t.) Ezek 20:5, 7, 19, 20; Joel 2:13 + (6 t.) Zech 6:15.

b. אֱלֹהֵיכֶם alakkal D-ben 46-szor; D^228t.; H-ban 15-ször; P-ben 15-ször; máshol 2Móz 23:25 (E); 8:24; 10:8, 16, 17 (JE); Bír 6:10; 1Sám 12:12, 14; 2Kir 17:39; 23:21; 1Krón 22:18 és máshol (a Krónikákban 10-szer) Zsolt 76:12; Jer 13:16 és máshol (5-ször) Ez 20:5, 7, 19, 20; Jóel 2:13 és máshol (6-szor) Zak 6:15.

**11.** 

> c. with אֱלֹהֵינוּ in D 23 t.; in D^25t.; Exod 8:6 (JE) 3:18; 5:3; 8:22; 8:23; 10:25-26, (E) Judg 11:24; 1Sam 7:8; 1Kin 8:57, 59, 61, 65; 2Kin 18:22; 19:10 = Isa 36:7; 37:20; 1Chr 13:2 + (15 t. Chronicles) Micah 4:5; 7:17; Isa 26:13; Jer 3:22 + (17 t.) Psa 20:8; 90:17 (?;Baer אֲדנָֹי); 94:23; 99:5; 99:8; 99:9 (twice in verse); 105:7; 106:47; 113:5; 122:9; 123:2; Dan 9:10, 13, 14.

c. אֱלֹהֵינוּ alakkal D-ben 23-szor; D^25t.; 2Móz 8:6 (JE) 3:18; 5:3; 8:22; 8:23; 10:25-26, (E) Bír 11:24; 1Sám 7:8; 1Kir 8:57, 59, 61, 65; 2Kir 18:22; 19:10 = Ézs 36:7; 37:20; 1Krón 13:2 és máshol (a Krónikákban 15-ször) Mik 4:5; 7:17; Ézs 26:13; Jer 3:22 és máshol (17-szer) Zsolt 20:8; 90:17 (?;Baer אֲדנָֹי); 94:23; 99:5; 99:8; 99:9 (a versben kétszer); 105:7; 106:47; 113:5; 122:9; 123:2; Dán 9:10, 13, 14.

**12.** 

> d. with אֱלֹהֵיהֶם Exod 10:7 (J) 29:46 (twice in verse); Lev 26:44 (P) Judg 3:7; 8:34; 1Sam 12:9; 1Kin 9:9; 2Kin 17:7, 9, 14, 16, 19; 18:12; 2Chr 31:6; 33:17; 34:33; Neh 9:3 (twice in verse); 9:4; Jer 3:21; 22:9; 30:9; 43:1 (twice in verse); 50:4; Ezek 28:26; 34:30; 39:22, 28; Hosea 1:7; 3:5; 7:10; Zeph 2:7; Hag 1:12 (twice in verse); Zech 9:16; 10:6.

d. אֱלֹהֵיהֶם alakkal 2Móz 10:7 (J) 29:46 (a versben kétszer); 3Móz 26:44 (P) Bír 3:7; 8:34; 1Sám 12:9; 1Kir 9:9; 2Kir 17:7, 9, 14, 16, 19; 18:12; 2Krón 31:6; 33:17; 34:33; Neh 9:3 (a versben kétszer); 9:4; Jer 3:21; 22:9; 30:9; 43:1 (a versben kétszer); 50:4; Ez 28:26; 34:30; 39:22, 28; Hós 1:7; 3:5; 7:10; Sof 2:7; Hag 1:12 (a versben kétszer); Zak 9:16; 10:6.

**13.** 

> e. with אֱלֹהָיו Num 23:21 (E) Exod 32:11 (J) Lev 4:22 (P) Deut 17:19; 18:7; 1Sam 30:6; 1Kin 5:17; 11:4; 15:3-4, 2Kin 5:11; 16:2; 2Chr 1:1 13t. Chronicles; Micah 5:3; Jer 7:28; Psa 33:12; 144:15; 146:5; Jonah 2:2.

e. אֱלֹהָיו alakkal 4Móz 23:21 (E) 2Móz 32:11 (J) 3Móz 4:22 (P) 5Móz 17:19; 18:7; 1Sám 30:6; 1Kir 5:17; 11:4; 15:3-4, 2Kir 5:11; 16:2; 2Krón 1:1, a Krónikákban 13-szor; Mik 5:3; Jer 7:28; Zsolt 33:12; 144:15; 146:5; Jón 2:2.

**14.** 

> f. with אֱלֹהַי Num 22:18 (JE) Deut 4:5; 18:16; 26:14; Josh 14:8-9, 2Sam 24:24; 1Kin 3:7; 5:18; 1 Kings 5:19; 8:28; 17:20-21, 1Chr 21:17; 22:7; 2Chr 2:3; 6:19; Ezra 7:28; 9:5; Psa 7:2; 7:4; 13:4; 18:29; 30:3; Psalm 30:13; 35:24; 40:6; 104:1; 109:26; Isa 25:1; Jer 31:18; Dan 9:4, 20; Jonah 2:7; Hab 1:12; Zech 11:4; 13:9; 14:5.

f. אֱלֹהַי alakkal 4Móz 22:18 (JE) 5Móz 4:5; 18:16; 26:14; Józs 14:8-9, 2Sám 24:24; 1Kir 3:7; 5:18; 1Kir 5:19; 8:28; 17:20-21, 1Krón 21:17; 22:7; 2Krón 2:3; 6:19; Ezsd 7:28; 9:5; Zsolt 7:2; 7:4; 13:4; 18:29; 30:3; Zsolt 30:13; 35:24; 40:6; 104:1; 109:26; Ézs 25:1; Jer 31:18; Dán 9:4, 20; Jón 2:7; Hab 1:12; Zak 11:4; 13:9; 14:5.

**15.** 

> g. with אֱלֹהַיִךְ Isa 60:9; Jer 2:17, 19; 3:13; Micah 7:10; Zeph 3:17.

g. אֱלֹהַיִךְ alakkal Ézs 60:9; Jer 2:17, 19; 3:13; Mik 7:10; Sof 3:17.

**16.** 

> h. with אלהים, probably always due to later editors, or to a Qr which has crept into the text Gen 2:4b — 3:23 (J, 20 t. either אלהים inserted by R^P as Di De; or יהוה inserted by J in an older source); Exod 9:30 (J, but not in ⅏ ᵐ5; Samaritan יהוה אדני; possibly ᵑ0 from earlier Qr, & ⅏ from later Qr); 2Sam 7:22, 25 (יהוה אדני ᵐ5 and 1Chr 17:20-23 only יהוה); 17:16-17, (but 2Sam 7:18-19, יהוה אדני) 1Chr 28:20; 29:1; 2Chr 1:9; 6:41 (twice in verse); 6:42; 26:18 (but in the original Psa 132:8 stood יהוה (so ℌ), or else no divine name); 72:18 (the late doxology) 84:12 (but it makes the line too long); Jonah 4:6. For the combinations with other divine names see those names.

h. אלהים alakkal, valószínűleg mindig későbbi szerkesztők munkájaként, vagy a szövegbe becsúszott Qr révén 1Móz 2:4b — 3:23 (J, 20-szor; vagy a אלהים betoldása R^P-től, mint Di De; vagy a יהוה betoldása J-től egy régebbi forrásba); 2Móz 9:30 (J, de a ⅏ ᵐ5-ben nincs; szamaritánus יהוה אדני; talán a ᵑ0 egy korábbi Qr-ből, a ⅏ pedig egy későbbi Qr-ből); 2Sám 7:22, 25 (יהוה אדני ᵐ5, és az 1Krón 17:20-23 csak יהוה); 17:16-17, (de 2Sám 7:18-19, יהוה אדני) 1Krón 28:20; 29:1; 2Krón 1:9; 6:41 (a versben kétszer); 6:42; 26:18 (de az eredetiben, Zsolt 132:8, יהוה állt (így ℌ), vagy pedig semmilyen istennév); 72:18 (a késői doxológia) 84:12 (de ez túl hosszúvá teszi a sort); Jón 4:6. A más istennevekkel alkotott kapcsolatokat l. azoknál a neveknél.

**17.** 

> 2 the phrase יהוה אֲנִי is noteworthy: —

2 figyelemre méltó a יהוה אֲנִי kifejezés: —

**18.** 

> a. after אמר either alone Exod 6:2, 29 (P) or before relative and other clauses: Gen 28:13 (J) 15:7 (R) Exod 6:6 (P) with אלהיכם Judg 6:10; Ezek 20:5.

a. אמר után, vagy önmagában 2Móz 6:2, 29 (P), vagy vonatkozó és más mellékmondatok előtt: 1Móz 28:13 (J) 15:7 (R) 2Móz 6:6 (P), אלהיכם alakkal Bír 6:10; Ez 20:5.

**19.** 

> b. after כי ידע (α) Exod 7:17; 8:18; 10:2 (J); 7:5; 14:4, 18 (P); 1Kin 20:13, 28; Jer 24:7; Ezek 6:7 48t. Ezekiel;

b. כי ידע után (α) 2Móz 7:17; 8:18; 10:2 (J); 7:5; 14:4, 18 (P); 1Kir 20:13, 28; Jer 24:7; Ez 6:7, Ezékielnél 48-szor;

**20.** 

> (β) with אלהיכם Exod 6:7; 16:12; Deut 29:5 (P) Exod 20:20; Joel 4:17;

(β) אלהיכם alakkal 2Móz 6:7; 16:12; 5Móz 29:5 (P) 2Móz 20:20; Jóel 4:17;

**21.** 

> (γ) with אלהיהם 29:46 (P) Ezek 28:26; 34:30; 39:22, 28;

(γ) אלהיהם alakkal 29:46 (P) Ez 28:26; 34:30; 39:22, 28;

**22.** 

> (δ) before relative and other clauses Isa 45:3; 49:23, 26; 60:16; Ezek 7:9; 17:24; 21:10; 22:22; 35:12; 36:36;

(δ) vonatkozó és más mellékmondatok előtt Ézs 45:3; 49:23, 26; 60:16; Ez 7:9; 17:24; 21:10; 22:22; 35:12; 36:36;

**23.** 

> (ε) with various forms of קדשׁ Exod 31:13 (P) Ezek 20:12; 37:28; 39:7;

(ε) a קדשׁ különböző alakjaival 2Móz 31:13 (P) Ez 20:12; 37:28; 39:7;

**24.** 

> (ζ) with דברתי 5:13; 17:21, compare י אני אשׁר ׳יֵדְעוּ 20:26.

(ζ) דברתי alakkal 5:13; 17:21, vö. י אני אשׁר ׳יֵדְעוּ 20:26.

**25.** 

> c. after כִּי in various combinations Lev 11:44-45, Num 35:34 (P), Lev 20:7, 26; 21:8, 15, 23; 22:16; 24:22; 25:17; 26:1, 44 (all H); Exod 15:26 (R) Isa 41:13; 43:3; 61:8; Jer 9:23; Ezek 12:25; 21:4; Zech 10:6; Mal 3:6.

c. כִּי után különféle kapcsolatokban 3Móz 11:44-45, 4Móz 35:34 (P), 3Móz 20:7, 26; 21:8, 15, 23; 22:16; 24:22; 25:17; 26:1, 44 (mind H); 2Móz 15:26 (R) Ézs 41:13; 43:3; 61:8; Jer 9:23; Ez 12:25; 21:4; Zak 10:6; Mal 3:6.

**26.** 

> d. emphatic Exod 6:8; 12:12; Lev 26:2, 45; Num 3:13, 41, 45 (all P); Lev 18:5-6, 21; 19:12, 14, 16, 18, 28, 30, 32, 37; 21:12; 22:2-3, 8, 30, 31, 33 (all H) Isa 43:15; with אלהיהם Exod 29:46; with אלהיךָ Isa 48:17; with אלהיכם Lev 23:43; 25:38, 55; Num 10:10; 15:41 (twice in verse) (P) Lev 18:2, 4, 30; 19:2-3, 4, 10, 25, 31, 34, 36; 20:24; 23:22; 26:13 (all H) Ezek 20:7, 19; Joel 2:27; with מְקַדֵּשׁ Lev 20:8; 22:9, 32 (H), with דברתי Num 14:35 (P) Ezek 5:15 + (11 t. Ezekiel); with clauses Isa 27:3; 41:4, 17; 42:6, 8; 45:5-6, 7, 8, 18, 19, 21; 60:22; Jer 17:10; 32:27; Ezek 14:4, 7, 9; 34:24; יהוה אָנֹכִי is used in the Ten Words Exod 20:2, 5 = Deut 5:6, 9 cited Psa 81:11; Hosea 12:10; 13:4; elsewhere only Exod 4:11 (J) Isa 43:11; 44:24; 51:15. 3 יהוה is also used with several predicates, to form sacred names of holy places of Yahweh יראה יהוה Gen 22:14 (J); נסי יהוה Exod 17:15 (E) שׁלים יהוה Judg 6:24 צדקנו יהוה Jer 33:16 (compare 23:6 where it is applied to the Messiah); שָׁ֑מָּה יהוה Ezek 48:35. — On combinations such as ׳י צְבָאוֺת י, ׳הַר etc., see צָבָא הַר,, etc. Note. — Bonk^ZAW 1891, 126 ff. seems to shew that as prefix, in compare proper name, יְהוֺ is the oldest and the latest form and that יוֺ is intermediate, belonging to the earlier post-exilic period until the time of Chronicles; occasional copyists' mistakes being taken into the account. ׳יְהוֺ proper name compounded with, see below יהוה above. יהוה proper name, of deity, see below הוה. ׳יו = ׳יְהוֺ proper name compounded with, see below יהוה above: — namely יוֺתָם יוֺרָם, יוֺקִים, יוֺעָשׁ, יוֺעֵד, יוֺיָרִיב, יוֺיָקִים, יוֺיָכִין, יוֺאָשׁ, יוֺאֵל, יוֺאָחָז, יוֺאָח, יוֺאָב,, etc.

d. emphaticus használatban 2Móz 6:8; 12:12; 3Móz 26:2, 45; 4Móz 3:13, 41, 45 (mind P); 3Móz 18:5-6, 21; 19:12, 14, 16, 18, 28, 30, 32, 37; 21:12; 22:2-3, 8, 30, 31, 33 (mind H) Ézs 43:15; אלהיהם alakkal 2Móz 29:46; אלהיךָ alakkal Ézs 48:17; אלהיכם alakkal 3Móz 23:43; 25:38, 55; 4Móz 10:10; 15:41 (a versben kétszer) (P) 3Móz 18:2, 4, 30; 19:2-3, 4, 10, 25, 31, 34, 36; 20:24; 23:22; 26:13 (mind H) Ez 20:7, 19; Jóel 2:27; מְקַדֵּשׁ alakkal 3Móz 20:8; 22:9, 32 (H), דברתי alakkal 4Móz 14:35 (P) Ez 5:15 és máshol (Ezékielnél 11-szer); mellékmondatokkal Ézs 27:3; 41:4, 17; 42:6, 8; 45:5-6, 7, 8, 18, 19, 21; 60:22; Jer 17:10; 32:27; Ez 14:4, 7, 9; 34:24; a יהוה אָנֹכִי a Tízigében használatos 2Móz 20:2, 5 = 5Móz 5:6, 9, idézi Zsolt 81:11; Hós 12:10; 13:4; máshol csak 2Móz 4:11 (J) Ézs 43:11; 44:24; 51:15. 3 A יהוה több állítmánnyal is használatos, Jahve szent helyeinek szent neveit alkotva: יראה יהוה 1Móz 22:14 (J); נסי יהוה 2Móz 17:15 (E) שׁלים יהוה Bír 6:24 צדקנו יהוה Jer 33:16 (vö. 23:6, ahol a Messiásra vonatkozik); שָׁ֑מָּה יהוה Ez 48:35. — Az olyan kapcsolatokról, mint ׳י צְבָאוֺת י, ׳הַר stb., l. צָבָא הַר,, stb. Megjegyzés. — Bonk^ZAW 1891, 126 kk. úgy látszik kimutatja, hogy az összetett tulajdonnevekben prefixummal álló alakként a יְהוֺ a legrégebbi és a legkésőbbi forma, a יוֺ pedig átmeneti, a korábbi fogság utáni időszakhoz tartozik a Krónikák koráig, a másolók alkalmi tévedéseit is számításba véve. ׳יְהוֺ tulajdonnevek összetételi eleme, l. lent יהוה fent. יהוה tulajdonnév, istennév, l. lent הוה. ׳יו = ׳יְהוֺ tulajdonnevek összetételi eleme, l. lent יהוה fent: — tudniillik יוֺתָם יוֺרָם, יוֺקִים, יוֺעָשׁ, יוֺעֵד, יוֺיָרִיב, יוֺיָקִים, יוֺיָכִין, יוֺאָשׁ, יוֺאֵל, יוֺאָחָז, יוֺאָח, יוֺאָב,, stb.

#### H3605 (12770 → 12978 karakter)

`forras_hash=eba9600709916e323c4e9c7df253aeb5a79d12c8` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v3`

**1.** 

> H3605. kol כֹּל once כּוֺל (Jer 33:8 Kt.), noun masculine the whole, all (Moabite, Phoenician, id.; Aramaic כּוֺל, ; Arabic ; Sabean כל, compare DHM^Epigr. Denk. 36-38; Ethiopic Assyrian kullatu) — absolute כֹּל, construct כֹּל Gen 2:5, 16, 20 +?כֹּלֿ Psa 138:2 (see Ba), but more usually כָּלֿ (with makk.: without it, 35:10; Prov 19:7; Kö^i. 84, 95); suffix 2 masculine singular in p. כֻּלָּךְ Micah 2:12; 2feminine singular כֻּלֵּךְ Isa 14:29, 31, כֻּלָּךְ 22:1; Song 4:7 (perhaps for assonance with accompanying בָּךְ לָךְ,); 3 masculine singular כֻּלֹּה 2Sam 2:9 (see Dr) + 17 t. (never in Pentateuch), כֻּלּוֺ Gen 25:25 16t.; 3 feminine singular כֻּלָּהּ 13:10 15t., כֻּלָּא Ezek 36:5; כֻּלָּנּו (16 t.); כֻּלְּכֶם (18 t.); כֻּלָּם (often), כּוּלָּם Jer 31:34, כֻּלָּ֑הַם 2Sam 23:6 (and probably Jer 15:10 כֻּלְּהֶם); 3 feminine plural כֻּלָּ֫נָה Gen 42:36; Prov 31:29; כֻּלָּֽהְנָה׃ 1Kin 7:37: — the whole, 1 with following Genitive (as usually) the whole of, to be rendered, however, often in our idiom, to avoid stiffness, all or every:

H3605. kol כֹּל, egyszer כּוֺל (Jer 33:8 Kt.), hímnemű főnév: az egész, minden (moábi, föníciai ua.; arámi כּוֺל, ; arab ; szabeus כל, vö. DHM^Epigr. Denk. 36-38; etióp asszír kullatu) — status absolutus כֹּל, status constructus כֹּל 1Móz 2:5, 16, 20 és máshol?כֹּלֿ Zsolt 138:2 (l. Ba), de rendszerint כָּלֿ (makkeffel; makkef nélkül 35:10; Péld 19:7; Kö^i. 84, 95); suffixummal 2. hímnemű egyes szám pausában כֻּלָּךְ Mik 2:12; 2. nőnemű egyes szám כֻּלֵּךְ Ézs 14:29, 31, כֻּלָּךְ 22:1; Én 4:7 (talán a kísérő בָּךְ לָךְ, alakkal való összecsengés kedvéért); 3. hímnemű egyes szám כֻּלֹּה 2Sám 2:9 (l. Dr) és még 17-szer (a Pentateuchusban soha), כֻּלּוֺ 1Móz 25:25, összesen 16-szor; 3. nőnemű egyes szám כֻּלָּהּ 13:10, összesen 15-ször, כֻּלָּא Ez 36:5; כֻּלָּנּו (16-szor); כֻּלְּכֶם (18-szor); כֻּלָּם (gyakran), כּוּלָּם Jer 31:34, כֻּלָּ֑הַם 2Sám 23:6 (és valószínűleg Jer 15:10 כֻּלְּהֶם); 3. nőnemű többes szám כֻּלָּ֫נָה 1Móz 42:36; Péld 31:29; כֻּלָּֽהְנָה׃ 1Kir 7:37: — az egész, 1 birtokos szóval (mint rendszerint): valaminek az egésze; nyelvhasználatunkban azonban a merevség elkerülése végett gyakran mind, minden fordítandó:

**2.** 

> a. Gen 2:2 כָּלצְֿבָאָם the whole of their host, 2:13 כּוּשׁ כָּלאֶֿרֶץ the whole of the land of Kush; כָּלהַֿלַּיְלָה the whole of the night; כָּליִֿשְׂרָאֵל the whole of Israel = all Israel; Deut 4:29 בְּכָללְֿבָֽבְךָ with the whole of thy heart = with all thy heart; + very often With a plural noun, usually determined by the article or a Genitive: Gen 5:5 אדם כליֿמי the whole of (= all) the days of Adam, 37:35 כלבֿניו the whole of (= all) his sons, Isa 2:2 כלהֿגוים all the nations; Gen 43:9 +?הימים כל = continually. In poetry, however, the noun may remain undetermined, כָּליָֿדַיִם the whole of hands = every hand, Isa 13:7; Jer 48:37; Ezek 21:12; כלפֿנים i.e. every face Isa 25:8; Joel 2:6; שׁלחנות כל Isa 28:8; חוצות כל 51:20; Lam 2:19 and elsewhere Before an infinitive Gen 30:41; Deut 4:7; 1Kin 8:52; 1Chr 23:31. frequently with suffixes, as כֻּלּוֺ (כֻּלֹּה) the whole of him Gen 25:25; Job 21:23; Song 5:16, the whole of it Lev 13:13; Jer 2:21; Nahum 2:1; Prov 24:31; כֻּלָּהּ the whole of it Gen 13:10; Exod 19:18; 25:36; Amos 8:8; כֻּלָּךְ all of thee Song 4:7 + (see at the beginning); כֻּלָּנוּ the whole of us Gen 42:11; Deut 5:3; Isa 53:6 (twice in verse); כֻּלְּכֶם Deut 1:22; 4:4; 1Sam 22:7 (twice in verse); כֻּלָּם Gen 11:6; 43:34; Josh 8:24 כֻּלָּם ויפלו, Judg 11:6 כֻּלָּם בְּיַד, Isa 7:19; 31:3 + often — Twice, strangely, with hyperb. intensive force, Psa 39:6 כָּלהֶֿבֶל the whole of vanity are all men (? omit כל, as 39:12), 45:14 כָּלכְּֿבוּדָּה the whole of gloriousness is the king's daughter.

a. 1Móz 2:2 כָּלצְֿבָאָם egész seregük, 2:13 כּוּשׁ כָּלאֶֿרֶץ Kús egész földje; כָּלהַֿלַּיְלָה az egész éjszaka; כָּליִֿשְׂרָאֵל egész Izráel = minden Izráel; 5Móz 4:29 בְּכָללְֿבָֽבְךָ egész szíveddel = teljes szívedből; és igen gyakran máshol. Többes számú főnévvel, amelyet rendszerint a névelő vagy birtokos szó tesz határozottá: 1Móz 5:5 אדם כליֿמי Ádám napjainak egésze (= Ádám minden napja), 37:35 כלבֿניו fiainak egésze (= minden fia), Ézs 2:2 כלהֿגוים minden nemzet; 1Móz 43:9 és máshol?הימים כל = folyamatosan. A költészetben azonban a főnév határozatlan maradhat, כָּליָֿדַיִם kezek egésze = minden kéz, Ézs 13:7; Jer 48:37; Ez 21:12; כלפֿנים azaz minden arc Ézs 25:8; Jóel 2:6; שׁלחנות כל Ézs 28:8; חוצות כל 51:20; JSir 2:19 és máshol. Infinitivus előtt 1Móz 30:41; 5Móz 4:7; 1Kir 8:52; 1Krón 23:31. Gyakran suffixumokkal, mint כֻּלּוֺ (כֻּלֹּה) ő egészen 1Móz 25:25; Jób 21:23; Én 5:16, az egésze 3Móz 13:13; Jer 2:21; Náh 2:1; Péld 24:31; כֻּלָּהּ az egésze 1Móz 13:10; 2Móz 19:18; 25:36; Ámós 8:8; כֻּלָּךְ te egészen Én 4:7 és máshol (l. a szócikk elején); כֻּלָּנוּ mi mindnyájan 1Móz 42:11; 5Móz 5:3; Ézs 53:6 (a versben kétszer); כֻּלְּכֶם 5Móz 1:22; 4:4; 1Sám 22:7 (a versben kétszer); כֻּלָּם 1Móz 11:6; 43:34; Józs 8:24 כֻּלָּם ויפלו, Bír 11:6 כֻּלָּם בְּיַד, Ézs 7:19; 31:3 és gyakran máshol — Kétszer, különös módon, túlzó nyomatékkal, Zsolt 39:6 כָּלהֶֿבֶל csupa hiábavalóság minden ember (? hagyd el a כל szót, mint 39:12), 45:14 כָּלכְּֿבוּדָּה csupa dicsőség a király leánya.

**3.** 

> b. followed often by a singular, to be understood collectively, whether with or without the article: Gen 1:21 החיה נפשׁ כל את the whole of living souls = every living soul, 2:9 למראה נחמד עץ כל the whole of trees (every kind of tree) pleasant to view, 6:12 + כָּלבָּֿשָׂר, 7:14 כנף כל צפור כל all birds of every kind of wing (so Ezek 17:23), 17:21 האדם כל the whole of mankind (so Num 12:3; 16:29; Judg 16:17 and elsewhere); in poetry כלאֿדם Psa 39:6; 64:10 +; 1Sam 14:52 וכלבֿןחֿיל גבור אישׁ כל, 17:19, 24 ישׂראל אישׁ כל, 22:2; Isa 9:16 פה כל the whole of mouths = every mouth, 15:2; 24:10 כָּלבַּֿיִת + often (in 2:12-16 the singular and plural interchange); Psa 7:12 + בכליֿום, 10:5 + בכלעֿת = at all seasons. So כלהֿעץ Gen 1:29, כלהֿבן Exod 1:22 = all the sons, כלהֿמקום 20:24; Deut 11:24 = all the places, כלהֿמרכב Lev 15:9, 15:26; Deut 4:3 אשׁר כלהֿאישׁ = all the men who. . ., 15:19 כלהֿבכור, Jer 4:29 עזובה כלהֿעיר all the cities (notice the following בָּהֶן); כלהֿיום = all the days (see יוֺם 7f), etc. In late Hebrew extended to such phrases as וָדוֺר בְּכָלדּֿוֺר Psalm 45:18; Psa 145:13; Est 9:28; ועיר בכלעֿיר2Chr 11:12; 28:25; 31:19; Est 8:11, 17; 9:28; 2Chr 32:28; Est 2:11; 3:14; 4:3; 8:13, 17; 9:21, 27, 28 (3 t. in verse) (compare וְ 1i b).

b. gyakran egyes szám követi, gyűjtőértelemben, akár névelővel, akár anélkül: 1Móz 1:21 החיה נפשׁ כל את az élő lelkek egésze = minden élő lélek, 2:9 למראה נחמד עץ כל a fák egésze (mindenféle fa), amely kívánatos a szemnek, 6:12 és máshol כָּלבָּֿשָׂר, 7:14 כנף כל צפור כל minden madár, mindenféle szárnyas (így Ez 17:23), 17:21 האדם כל az egész emberiség (így 4Móz 12:3; 16:29; Bír 16:17 és máshol); a költészetben כלאֿדם Zsolt 39:6; 64:10 és máshol; 1Sám 14:52 וכלבֿןחֿיל גבור אישׁ כל, 17:19, 24 ישׂראל אישׁ כל, 22:2; Ézs 9:16 פה כל a szájak egésze = minden száj, 15:2; 24:10 כָּלבַּֿיִת és gyakran máshol (a 2:12-16-ban az egyes és a többes szám váltakozik); Zsolt 7:12 és máshol בכליֿום, 10:5 és máshol בכלעֿת = minden időben. Így כלהֿעץ 1Móz 1:29, כלהֿבן 2Móz 1:22 = minden fiú, כלהֿמקום 20:24; 5Móz 11:24 = minden hely, כלהֿמרכב 3Móz 15:9, 15:26; 5Móz 4:3 אשׁר כלהֿאישׁ = minden férfi, aki..., 15:19 כלהֿבכור, Jer 4:29 עזובה כלהֿעיר minden város (figyeld meg az utána álló בָּהֶן alakot); כלהֿיום = minden nap (l. יוֺם 7f), stb. A késői héberben olyan kifejezésekre is kiterjed, mint וָדוֺר בְּכָלדּֿוֺר Zsolt 45:18; Zsolt 145:13; Eszt 9:28; ועיר בכלעֿיר 2Krón 11:12; 28:25; 31:19; Eszt 8:11, 17; 9:28; 2Krón 32:28; Eszt 2:11; 3:14; 4:3; 8:13, 17; 9:21, 27, 28 (a versben 3-szor) (vö. וְ 1i b).

**4.** 

> c. the Genitive after כל is often a relative sentence, introduced by אשׁר: Gen 1:31 עשׂה אשׁר כל את the whole of what he had made, 7:22; 13:1 + very often Sts., with a preposition, אשׁר כל has the force of wheresover, whithersoever, as Josh 1:7 תֵּלֵךְ אֲשֶׁר בְּכֹל wheresoever thou goest, 1:16 אֶלכָּֿלאֲֿשֶׁר whithersoever (see אֲשֶׁר 4b γ). Very rarely in such cases is there ellipse of the rel., as Gen 39:4 בְּיָדִי נָתַן וְכָליֶֿשׁלֿוֺ (contrast 39:5; 39:8), Exod 9:4 ישׂראל מכללֿבני, Isa 38:16 רוּחִי חַיֵּי וּלְכָּלבָּֿהֶן, Psa 71:18 לְכָליָֿבוֺא (74:3, see 2a), 2Chr 32:31; peculiarly also in Chronicles (Dr^Intr 505), 1Chr 29:3 מִכָּלהֲֿכִינוֺתִי, 2Chr 30:18f.; Ezra 1:6; compare with כֹּל (2a) 1Chr 29:11 a 2Chr 30:17; Ezra 1:5.

c. a כל utáni birtokos gyakran vonatkozó mellékmondat, amelyet אשׁר vezet be: 1Móz 1:31 עשׂה אשׁר כל את mindaz, amit alkotott, 7:22; 13:1 és igen gyakran máshol. Néha elöljárószóval a אשׁר כל jelentése: ahol csak, ahová csak, mint Józs 1:7 תֵּלֵךְ אֲשֶׁר בְּכֹל bárhová mégy, 1:16 אֶלכָּֿלאֲֿשֶׁר ahová csak (l. אֲשֶׁר 4b γ). Ilyen esetekben nagyon ritkán marad el a vonatkozó névmás, mint 1Móz 39:4 בְּיָדִי נָתַן וְכָליֶֿשׁלֿוֺ (ellentétben a 39:5; 39:8 helyekkel), 2Móz 9:4 ישׂראל מכללֿבני, Ézs 38:16 רוּחִי חַיֵּי וּלְכָּלבָּֿהֶן, Zsolt 71:18 לְכָליָֿבוֺא (74:3, l. 2a), 2Krón 32:31; sajátosan a Krónikákban is (Dr^Intr 505), 1Krón 29:3 מִכָּלהֲֿכִינוֺתִי, 2Krón 30:18k.; Ezsd 1:6; vö. כֹּל mellett (2a) 1Krón 29:11 a 2Krón 30:17; Ezsd 1:5.

**5.** 

> d. with a suffix two idiomatic uses of כל have to be noticed: (a) כל is often made more independent and emphatic by being placed with a suffix after the word which it qualifies, to which it then stands in apposition (compare in Syriac, Arabic, Ethiopic), as 2Sam 2:9 כֻּלּהֹ יִשְׂרָאֵל, Jer 13:19; 48:31; Isa 9:8; 14:29, 31 כלך פלשׁת Philistia, all of thee ! Micah 2:12; Hab 2:6; Job 34:13; Psa 67:4; 67:6; especially in Ezekiel, as Ezek 14:5; 29:2 כֻּלָּהּ מצרים 32:12, 30; with change of person (compare the idiom in Isa 22:16; 48:1; 54:1 etc.), 1Kin 22:28 = Micah 1:2 כלם עמים שׁמעו Hear, nations, all of them ! Mal 3:9 כֻּלּוֺ הַגּוֺי. So even with כל preceding: Num 16:3 כֻּלָּם כָּלהָֿעֵדָה, Isa 14:18; Jer 30:16; Ezek 11:15 כֻּלֹּה ישׂראל בית כל the whole of the house of Israel, the whole of it (so 20:40; 36:10), 35:15; 36:5; Psa 8:8 (compare Sabean DHM^l.c.); (b) with the suffix of 3 masculine singular, understood as referring to the mass of things or persons meant, כֻּלֹּה or כֻּלּוֺ, literally the whole of it, is equivalent to all of them, every one, Exod 14:7 and captains עַלכֻּֿלּוֺ upon the whole of it (the רֶכֶב collectively) = all of them, Isa 1:23 the whole of it (the people) loveth bribes, 9:16; 15:3; Jer 6:13 (twice in verse); 8:6, 10 (twice in verse); 20:7; Hab 1:9, 15; Psa 29:9 and in his temple כָּבוֺד אֹמֵר כֻּלּוֺ the whole of it (= every one there) says, Glory ! 53:4 (|| 14:3 הַכֹּל); perhaps Isa 16:7; Jer 48:38; + Prov 19:6 Ew Hi (רֵעַ וְכֻלּהֹ): Jer 15:10 read קִלֲלוּנִי כֻּלְּהֶם.

d. suffixummal a כל két idiomatikus használatát kell megfigyelni: (a) a כל gyakran önállóbbá és nyomatékosabbá válik azáltal, hogy suffixummal a meghatározott szó után áll, amellyel ilyenkor értelmezői viszonyban van (vö. a szírben, arabban, etiópban), mint 2Sám 2:9 כֻּלּהֹ יִשְׂרָאֵל, Jer 13:19; 48:31; Ézs 9:8; 14:29, 31 כלך פלשׁת Filiszteus föld, te egészen! Mik 2:12; Hab 2:6; Jób 34:13; Zsolt 67:4; 67:6; különösen Ezékielnél, mint Ez 14:5; 29:2 כֻּלָּהּ מצרים 32:12, 30; személyváltással (vö. az Ézs 22:16; 48:1; 54:1 stb. fordulatát), 1Kir 22:28 = Mik 1:2 כלם עמים שׁמעו Halljátok, népek, mindnyájan! Mal 3:9 כֻּלּוֺ הַגּוֺי. Így még akkor is, ha כל előzi meg: 4Móz 16:3 כֻּלָּם כָּלהָֿעֵדָה, Ézs 14:18; Jer 30:16; Ez 11:15 כֻּלֹּה ישׂראל בית כל Izráel egész háza, egészen (így 20:40; 36:10), 35:15; 36:5; Zsolt 8:8 (vö. szabeus DHM^l.c.); (b) a 3. hímnemű egyes szám suffixumával, amelyet a szóban forgó dolgok vagy személyek tömegére vonatkoztatnak, a כֻּלֹּה vagy כֻּלּוֺ, szó szerint: az egésze, = mindnyájan, mindegyikük, 2Móz 14:7 és tisztek עַלכֻּֿלּוֺ az egészén (a רֶכֶב gyűjtőértelemben) = mindegyiken, Ézs 1:23 az egésze (a nép) szereti a vesztegetést, 9:16; 15:3; Jer 6:13 (a versben kétszer); 8:6, 10 (a versben kétszer); 20:7; Hab 1:9, 15; Zsolt 29:9 és templomában כָּבוֺד אֹמֵר כֻּלּוֺ az egésze (= mindenki ott) mondja: Dicsőség! 53:4 (|| 14:3 הַכֹּל); talán Ézs 16:7; Jer 48:38; továbbá Péld 19:6 Ew Hi (רֵעַ וְכֻלּהֹ): Jer 15:10 olv. קִלֲלוּנִי כֻּלְּהֶם.

**6.** 

> e. Hebrew idiom in certain cases affirms, or denies, of an entire class, where English idiom affirms, or denies, of an individual of the class; thus in a comparative or hypothetical sentence כל is = any, and with a negative = none: (a) Gen 3:1 the serpent was more subtil השׂדה חית מכל than all beasts of the field (in our idiom: than any beast of the field), Deut 7:7; 1Sam 9:2; (b) Lev 4:2 a soul when it sins through ignorance יי֞ מצות מכל in all the commandments of Jehovah (= in any of the commandments, etc.), 19:23 when ye . . . plant מאכל כלעֿץ = any tree for food, Num 35:22 or if he have cast upon him כָּלכְּֿלִי = any weapon, 1Kin 8:37 b; joined with a participle in a hypothetical sense (Dr^§ 121 n. Ges^§ 116. 5 R. 5), Gen 4:14 מצאי כל all my finders (= if any one find me), he will slay me, 4:15 a Num 21:8 כָּלהַֿנָּשׁוּךְ = whosoever (= if any one) is bitten, 1Sam 2:13; (c) with a negative, Gen 2:5 all plants of the field יִהְיֶה טֶרֶם were not as yet = no plant of the field as yet was, 4:15 b כלמֿצאו הכותאֿתו לבלתי for the not-smiting him of all finding him = that none finding him should smite him, Exod 10:15 ירק כל ולאנֿותר = and no green things were left, 12:16 יעשׂה לא כלמֿלאכה all work shall not be done = no work shall be done, Deut 28:14; Judg 13:4 כָּלטָֿמֵא אַלתּֿאֹכְלִי eat not of all that is unclean, 19:19 כָּלדָּֿבָר מַחְסוֺר אֵין there is no lack of all things i.e. of any thing, Psa 143:2 כלחֿי לפניך לאיֿצדק כי, + very often (so οὐ πᾶς, as a Hebraism, in the N.T., e.g. Mark 13:20 οὐκ ἂν ἐσώθη πᾶσα σάρξ, Luke 1:37 οὐκ ἀδυνατήσει . . . πᾶν ρἧμα, as Jer 32:17 כָּלדָּֿבָר מִמְּךָ לֹאיִֿמָּלֵא, Gal 2:16 οὐ δικαιωθήσεται . . . πᾶσα σάρξ, etc.) Usually, in such cases, כל (or its Genitive) is without the article, being left purposely indefinite: in Psa 49:18 ( 2b a) הַכֹּל is emphatic (in Num 23:13 תִרְאֶה לֹא וְכֻלּוֺ the context shews that כֹּל is opposed to a part). feminine very anomalously, severed from its Genitive, 2Sam 1:9 בִי נַפְשִׁי כִּיכָֿלעֿוֺד, Job 27:3 בִי נִשְׁמָתִי כִּיכָֿלעֿוֺד, Hosea 14:3 (si vera lectio) עָוֺן כָּלתִּֿשָּׂא. On Eccl 5:15 ׳כָּלעֻֿמַּתשֶֿׂ see עֻמָּה. Note. — When the Genitive after כל is a noun feminine or plural, the predicate usually agrees with this (as being the really important idea), e.g. Gen 5:5 אדם ימי כל ויהיו, Num 14:1 כָלהָֿעֵדָה וַתִּשָּׂא, Nahum 3:1; Psa 150:6 תְּהַלֵּל הַנְּשָׁמָה כָֹּל exceptions being very rare, Isa 64:10b Prov 16:2 (Ges^§ 141. 1 R. 2). 2 Absolutely:

e. A héber nyelvhasználat bizonyos esetekben egy egész osztályról állít vagy tagad valamit, ahol az angol nyelvhasználat az osztály egy egyedéről állítja vagy tagadja; így összehasonlító vagy feltételes mondatban a כל = bármely, tagadással pedig = semmi, senki: (a) 1Móz 3:1 a kígyó ravaszabb volt השׂדה חית מכל a mező minden vadjánál (a mi nyelvhasználatunk szerint: a mező bármely vadjánál), 5Móz 7:7; 1Sám 9:2; (b) 3Móz 4:2 ha egy lélek tudatlanságból vétkezik יי֞ מצות מכל Jehova minden parancsolatában (= bármelyik parancsolatában stb.), 19:23 ha ... ültettek מאכל כלעֿץ = bármilyen gyümölcsfát, 4Móz 35:22 vagy ha rádobott כָּלכְּֿלִי = bármilyen eszközt, 1Kir 8:37 b; participiummal feltételes értelemben (Dr^§ 121 n. Ges^§ 116. 5 R. 5), 1Móz 4:14 מצאי כל minden megtalálóm (= ha valaki megtalál), megöl engem, 4:15 a 4Móz 21:8 כָּלהַֿנָּשׁוּךְ = bárki (= ha valakit) megmar, 1Sám 2:13; (c) tagadással, 1Móz 2:5 a mező minden növénye יִהְיֶה טֶרֶם még nem volt = a mezőnek még egyetlen növénye sem volt, 4:15 b כלמֿצאו הכותאֿתו לבלתי hogy őt minden megtalálója ne ölje meg = hogy senki, aki megtalálja, meg ne ölje, 2Móz 10:15 ירק כל ולאנֿותר = és semmi zöld nem maradt, 12:16 יעשׂה לא כלמֿלאכה minden munka ne végeztessék = semmi munka ne végeztessék, 5Móz 28:14; Bír 13:4 כָּלטָֿמֵא אַלתּֿאֹכְלִי ne egyél semmi tisztátalant, 19:19 כָּלדָּֿבָר מַחְסוֺר אֵין nincs hiány semmiben, azaz semmiből, Zsolt 143:2 כלחֿי לפניך לאיֿצדק כי, és igen gyakran máshol (így οὐ πᾶς hebraizmusként az Újszövetségben, pl. Mk 13:20 οὐκ ἂν ἐσώθη πᾶσα σάρξ, Luk 1:37 οὐκ ἀδυνατήσει ... πᾶν ρἧμα, mint Jer 32:17 כָּלדָּֿבָר מִמְּךָ לֹאיִֿמָּלֵא, Gal 2:16 οὐ δικαιωθήσεται ... πᾶσα σάρξ, stb.) Ilyen esetekben a כל (vagy birtokosa) rendszerint névelő nélkül áll, szándékosan határozatlanul hagyva: a Zsolt 49:18-ban ( 2b a) a הַכֹּל emphaticus (a 4Móz 23:13-ban תִרְאֶה לֹא וְכֻלּוֺ a szövegösszefüggés mutatja, hogy a כֹּל egy rész ellentéteként áll). Nőnemű alakban egészen rendhagyóan, birtokosától elválasztva, 2Sám 1:9 בִי נַפְשִׁי כִּיכָֿלעֿוֺד, Jób 27:3 בִי נִשְׁמָתִי כִּיכָֿלעֿוֺד, Hós 14:3 (si vera lectio) עָוֺן כָּלתִּֿשָּׂא. A Préd 5:15 ׳כָּלעֻֿמַּתשֶֿׂ helyhez l. עֻמָּה. Megjegyzés. — Ha a כל utáni birtokos nőnemű vagy többes számú főnév, az állítmány rendszerint ezzel egyezik (mint a valóban fontos fogalommal), pl. 1Móz 5:5 אדם ימי כל ויהיו, 4Móz 14:1 כָלהָֿעֵדָה וַתִּשָּׂא, Náh 3:1; Zsolt 150:6 תְּהַלֵּל הַנְּשָׁמָה כָֹּל; kivétel nagyon ritka, Ézs 64:10b Péld 16:2 (Ges^§ 141. 1 R. 2). 2 Önállóan:

**7.** 

> a. without the article, all things, all (mostly neuter, but sometimes masculine), the sense in which 'all' is to be taken being gathered from the context, Gen 9:3 כֹּל את לכם נתתי, 16:12 בּוֺ כֹּל וְיַד, 20:16 ונוכחת כֹּל ואת, 33:11 כֹל לי ישׁ וכי, Num 8:16 ישׂראל מבני כֹּל בכור, 11:6 כֹּל אֵין nought of all things ! = there is nothing (so 2Sam 12:3; Prov 13:7, compare 2Kin 4:2), 13:2 בהם נשׂיא כֹּ֖ל (compare 2Sam 23:28; 1Chr 3:9: usually so הַכֹּל), Deut 28:47 כֹּל מֵרֹב, 28:48; 28:37 כֹּל בְּחֹסֶר (compare Jer 44:18), Isa 30:5 הֹבִאישׁ כֹּל all exhibit shame, 44:24 ׳י עשֶֹׁהכֹּֿל, Jer 44:12 כֹל וְתַמּוּ (unusual), Zeph 1:2; Psa 8:7; 74:3 (read הֵרַע כֹּל), 145:15 כֹל עיני, Prov 16:4; 26:10; 28:5; Job 13:1 עיני ראתה כֹּל הן, 42:2; 1Chr 29:11b 2Chr 32:22 (masculine), Dan 11:37 (see also 1c end); מִכֹּל Gen 6:19-20,b מִכֹּל שְׁנַיִם, 14:20; 27:33; Jer 17:9 מִכֹּל הלב עקוב, Dan 11:2 (masculine) After a negative = anything, Deut 4:25 כֹּל תְּמוּנַת the likeness of anything, 8:9; 28:55; Prov 30:30. In the Genitive also, very rarely, to express the idea of all as comprehensively as possible: Ezek 44:30 כֹּל וְכָלתְּֿרוּמַת כֹל כָּלבִּֿכּוּרֵי; Psa 119:128 (si vera lectio) כֹל כָּלמִּֿקּוּדֵי all the statutes about everthing.

a. névelő nélkül: minden dolog, minden (többnyire semlegesnemű, de néha hímnemű értelemben), és hogy a 'minden' hogyan értendő, az a szövegösszefüggésből derül ki, 1Móz 9:3 כֹּל את לכם נתתי, 16:12 בּוֺ כֹּל וְיַד, 20:16 ונוכחת כֹּל ואת, 33:11 כֹל לי ישׁ וכי, 4Móz 8:16 ישׂראל מבני כֹּל בכור, 11:6 כֹּל אֵין semmi sincs mindenből! = nincs semmi (így 2Sám 12:3; Péld 13:7, vö. 2Kir 4:2), 13:2 בהם נשׂיא כֹּ֖ל (vö. 2Sám 23:28; 1Krón 3:9: rendszerint így הַכֹּל), 5Móz 28:47 כֹּל מֵרֹב, 28:48; 28:37 כֹּל בְּחֹסֶר (vö. Jer 44:18), Ézs 30:5 הֹבִאישׁ כֹּל mindenki szégyent vall, 44:24 ׳י עשֶֹׁהכֹּֿל, Jer 44:12 כֹל וְתַמּוּ (szokatlan), Sof 1:2; Zsolt 8:7; 74:3 (olv. הֵרַע כֹּל), 145:15 כֹל עיני, Péld 16:4; 26:10; 28:5; Jób 13:1 עיני ראתה כֹּל הן, 42:2; 1Krón 29:11b 2Krón 32:22 (hímnemű), Dán 11:37 (l. még 1c végét); מִכֹּל 1Móz 6:19-20,b מִכֹּל שְׁנַיִם, 14:20; 27:33; Jer 17:9 מִכֹּל הלב עקוב, Dán 11:2 (hímnemű). Tagadás után = bármi, 5Móz 4:25 כֹּל תְּמוּנַת bárminek a képmása, 8:9; 28:55; Péld 30:30. Birtokos esetben is, nagyon ritkán, hogy a mindenség fogalmát a lehető legátfogóbban fejezze ki: Ez 44:30 כֹּל וְכָלתְּֿרוּמַת כֹל כָּלבִּֿכּוּרֵי; Zsolt 119:128 (si vera lectio) כֹל כָּלמִּֿקּוּדֵי minden végzés mindenről.

**8.** 

> b. with art. הַכֹּל: (a) where the sense is limited by the context to things (or persons) just mentioned, Exod 29:24 אהרן ביד הַכֹּל ושׂמת, Lev 1:9 הַכֹּל את הכהן והקטיר, 1:13; 8:27; Deut 2:36 י נתן הַכֹּל ׳את לפנינו, Josh 11:19 (compare 2Sam 19:31; 1Kin 14:26 2Chr 12:9), 2 Chron 21:43 בָּא הַכֹּל (compare 23:14), 1Sam 30:19 דוד השׁיב הַכֹּל, 2Sam 17:3 (corrupt: see ᵐ5 Dr), 24:23 (1Chr 21:23), 1Kin 6:18 ארז הַכֹּל (compare 7:33; 2Kin 25:17 = Jer 52:22), 2Kin 24:16 גבורים הַכֹּל, Isa 65:8 הַכֹּל השׁחית לבלתי, Psa 14:3; or implied, Gen 16:12 בַכֹּל יָדוֺ, 24:1 בַּכֹּל אברהם את ברך 2Sam 23:5 (poetry) בַכֹּל עֲרֻכָה, Isa 29:11 (peculiarly) הַכֹּל חָזוּת the vision of the whole, Jer 13:7, 10 לַכֹּל יצלח לא, Ezek 7:14 הַכֹּל וְהָכִין (but Co הָכֵן וְהָכִינוּ), Psa 49:18 הַכֹּל יקח במותו לא: more frequently later, namely 1Chr 7:5 (as regards all), 28:19; 29:19; 2Chr 28:6; 29:28; 31:5; 35:7; 36:17-18, Ezra 1:11; 2:42; 8:34-35, 10:17 (בַכֹּל וַיְכַלּוּ: see BeRy), Eccl 5:8 (בַּכֹּל, apparently = in all respects), 10:19; 12:13. (b) in a wider sense, all, whether of all mankind or of all living things, the universe (τὸ πᾶν), or of all the circumstances of life (chiefly late), Jer 10:16 = 51:19 הוא הַכֹּל יוצר כי, Psa 103:19 (compare 1Chr 29:12), 1Chron 119:21 עֲבָדֶיךָ הַכֹּל, 1Chron 145:9 י ׳טוֺב לַכֹּל, 29:12, 14, 16; Dan 11:2, and especially in Ecclesiastes, as Eccl 1:2, 14; 2:11, 17; 3:19; 12:8 הֶבֶל הַכֹּל, 2:16 נשׁכח הכל, 3:1 זְמָן לַכֹּל, 3:11; 3:19; 3:20; 6:6; 7:15; 9:1-2,(twice in verse); 9:3; 10:3, 19; 11:5. כַּכֹּל, Job 24:24 (si vera lectio) יִקָָּֽפְצוּן כַּכֹּל like all men (i.e. like men in General). כָּלֿ כֹּל,: noun masculine the whole, all (Biblical Hebrew כֹּל); — emphatic כֹּלָּא Dan 2:40 +, construct כֹּל 2:12; 3:2 +, כָּלֿ 2:8 +, suffix 3 masculine plural כָּלְּהוֺן (so Palmyrene Lzb^296 Cooke^No. 117, Tariff ii.c.19 ii b. 18) 2:38; 7:19 (Qr feminine כָּכְּהֵּן); — 1 בָבֶכ חַכִּימֵי כֹּל the whole of ( = all) the wise men of B. Dan 3:2-3, 5, etc.; 6:2 כלמֿלכותא the whole ofthe kingdom, 6:4; with suffix the whole of them, 2:38; 7:19.

b. névelővel הַכֹּל: (a) ahol az értelmet a szövegösszefüggés az imént említett dolgokra (vagy személyekre) korlátozza, 2Móz 29:24 אהרן ביד הַכֹּל ושׂמת, 3Móz 1:9 הַכֹּל את הכהן והקטיר, 1:13; 8:27; 5Móz 2:36 י נתן הַכֹּל ׳את לפנינו, Józs 11:19 (vö. 2Sám 19:31; 1Kir 14:26 2Krón 12:9), 2 Chron 21:43 בָּא הַכֹּל (vö. 23:14), 1Sám 30:19 דוד השׁיב הַכֹּל, 2Sám 17:3 (romlott: l. ᵐ5 Dr), 24:23 (1Krón 21:23), 1Kir 6:18 ארז הַכֹּל (vö. 7:33; 2Kir 25:17 = Jer 52:22), 2Kir 24:16 גבורים הַכֹּל, Ézs 65:8 הַכֹּל השׁחית לבלתי, Zsolt 14:3; vagy ahol odaértendő, 1Móz 16:12 בַכֹּל יָדוֺ, 24:1 בַּכֹּל אברהם את ברך 2Sám 23:5 (költészet) בַכֹּל עֲרֻכָה, Ézs 29:11 (sajátosan) הַכֹּל חָזוּת a mindenről szóló látomás, Jer 13:7, 10 לַכֹּל יצלח לא, Ez 7:14 הַכֹּל וְהָכִין (de Co הָכֵן וְהָכִינוּ), Zsolt 49:18 הַכֹּל יקח במותו לא: később gyakrabban, tudniillik 1Krón 7:5 (ami mindegyiket illeti), 28:19; 29:19; 2Krón 28:6; 29:28; 31:5; 35:7; 36:17-18, Ezsd 1:11; 2:42; 8:34-35, 10:17 (בַכֹּל וַיְכַלּוּ: l. BeRy), Préd 5:8 (בַּכֹּל, láthatólag = minden tekintetben), 10:19; 12:13. (b) tágabb értelemben: minden, akár az egész emberiségről, akár minden élőlényről, a mindenségről (τὸ πᾶν), akár az élet minden körülményéről (főként későn), Jer 10:16 = 51:19 הוא הַכֹּל יוצר כי, Zsolt 103:19 (vö. 1Krón 29:12), 1Chron 119:21 עֲבָדֶיךָ הַכֹּל, 1Chron 145:9 י ׳טוֺב לַכֹּל, 29:12, 14, 16; Dán 11:2, és különösen a Prédikátor könyvében, mint Préd 1:2, 14; 2:11, 17; 3:19; 12:8 הֶבֶל הַכֹּל, 2:16 נשׁכח הכל, 3:1 זְמָן לַכֹּל, 3:11; 3:19; 3:20; 6:6; 7:15; 9:1-2,(a versben kétszer); 9:3; 10:3, 19; 11:5. כַּכֹּל, Jób 24:24 (si vera lectio) יִקָָּֽפְצוּן כַּכֹּל mint minden ember (azaz mint általában az emberek). כָּלֿ כֹּל,: hímnemű főnév: az egész, minden (bibliai héber כֹּל); — status emphaticus כֹּלָּא Dán 2:40 és máshol, status constructus כֹּל 2:12; 3:2 és máshol, כָּלֿ 2:8 és máshol, suffixummal 3. hímnemű többes szám כָּלְּהוֺן (így palmürai Lzb^296 Cooke^No. 117, Tariff ii.c.19 ii b. 18) 2:38; 7:19 (Qr nőnemű כָּכְּהֵּן); — 1 בָבֶכ חַכִּימֵי כֹּל B. bölcseinek egésze ( = minden bölcse) Dán 3:2-3, 5, stb.; 6:2 כלמֿלכותא az egész királyság, 6:4; suffixummal: mindnyájuk, 2:38; 7:19.

**9.** 

> 2 with a singular noun, understood collectively, every, any, or with a negative none (Biblical Hebrew 1b):Dan 3:29 וְלִשָּׁן אֻמָּה כָלעַֿם דִּי that every people, nation, and language, etc., 6:8 מִןכָּֿלאֱֿלָה of any god, Ezra 6:12 וְעַם כָּלמֶֿלֶח; די אנשׁ כל every man who = whoever, Dan 3:10; 5:7; 6:13; Ezra 6:11; Dan 2:10 לא ֗֗֗ מלך כל שׁאל no king hath asked . . ., 2:35; 4:6; 6:5; 6:24; so כָּלדִּֿי (= Hebrew כָּלאְִֿשֶׁר) whoever 6:8; Ezra 7:26, whatever 7:23, בְּכָלדִּֿי wherever Dan 2:38(compare אְִשֶׁר 4b γ).

2 egyes számú főnévvel, gyűjtőértelemben: minden, bármely, tagadással: semmi, senki (bibliai héber 1b): Dán 3:29 וְלִשָּׁן אֻמָּה כָלעַֿם דִּי hogy minden nép, nemzet és nyelv stb., 6:8 מִןכָּֿלאֱֿלָה bármely istentől, Ezsd 6:12 וְעַם כָּלמֶֿלֶח; די אנשׁ כל minden ember, aki = bárki, Dán 3:10; 5:7; 6:13; Ezsd 6:11; Dán 2:10 לא ֗֗֗ מלך כל שׁאל egy király sem kérdezett ..., 2:35; 4:6; 6:5; 6:24; így כָּלדִּֿי (= héber כָּלאְִֿשֶׁר) bárki 6:8; Ezsd 7:26, bármi 7:23, בְּכָלדִּֿי bárhol Dán 2:38 (vö. אְִשֶׁר 4b γ).

**10.** 

> 3 emphatic כֹּלָּא, used absolutely, as Hebrew הַכֹּל (Biblical Hebrew 2b): Dan 2:40 כֹּלָּא חָשֵׁל crushing all things, 4:9; 4:18 לְכֹלָּאבֵֿהּ וּמָזוֺן and food for all was in it, 4:25 מְטָא כֹּלָּא all came upon N. (compare בָּא חַכֹּל Josh 21:43), Ezra 5:7 כֹלָּא שְׁלָמָא all peace (K^§ 83 d;) compare in Hebrew כֻּלּוּ etc., after their noun : Biblical Hebrew 1d a). — For כָּלקְָֿבֵל see קְָבֵל.

3 emphaticus כֹּלָּא, önállóan használva, mint a héber הַכֹּל (bibliai héber 2b): Dán 2:40 כֹּלָּא חָשֵׁל mindent összezúz, 4:9; 4:18 לְכֹלָּאבֵֿהּ וּמָזוֺן és mindenkinek volt benne eledel, 4:25 מְטָא כֹּלָּא mindez rájött N.-re (vö. בָּא חַכֹּל Józs 21:43), Ezsd 5:7 כֹלָּא שְׁלָמָא minden békesség (K^§ 83 d;) vö. a héberben כֻּלּוּ stb., a főnevük után: bibliai héber 1d a). — A כָּלקְָֿבֵל alakhoz l. קְָבֵל.

#### H0834 (22469 → 22332 karakter)

`forras_hash=060513bafff8b49b30b9d557aab282f85f79b8f4` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v3`

**1.** 

> H834. asher אֲשֶׁר particle of relation (Moabite id.; origin dubious:

H834. asher אֲשֶׁר vonatkozást jelölő partikula (moábi ua.; eredete kétséges:

**2.** 

> 1 according to Tsepreghi^Diss. Lugd. p. 171 Mühlau^Bö. Lb. ii.

1 Tsepreghi^Diss. Lugd. 171. o. Mühlau^Bö. Lb. ii.

**3.** 

> 79 n. Sta^Morg. Forsch. 1875, 188; Lb. § 167 Hom^ZMG 1878, 708 ff. Müll^§ 153 Sayce^Hebraica. ii. 51 Lag^M.

79 n. Sta^Morg. Forsch. 1875, 188; Lb. § 167 Hom^ZMG 1878, 708 kk. Müll^§ 153 Sayce^Hebraica. ii. 51 Lag^M.

**4.** 

> i. 255 & especially Krae^Hebraica. vi. 298 ff, originally a substantive 'place' = footstep, mark, (do.), אֲתַר, place, Assyrian ašru, used (see Kraetz.) both as a substantive 'there, where,' and as a relative of place 'where': in Hebrew this development has advanced further, and it has become a relative sign Generally. The chief objection to this explanation is that it would isolate Hebrew from the other Semitic languages, in which pronouns are formed regularly from demonstrative roots (compare also Nö^ZMG 1886, 738).

i. 255 és különösen Krae^Hebraica. vi. 298 kk. szerint eredetileg főnév: 'hely' = lábnyom, nyom, (ua.), אֲתַר, hely, asszír ašru, amelyet (l. Kraetz.) mind főnévként: 'ott, ahol,' mind helyhatározói vonatkozó szóként: 'ahol' használtak: a héberben ez a fejlődés tovább haladt, és általános vonatkozó jellé vált. E magyarázat ellen a fő kifogás az, hogy a hébert elszigetelné a többi sémi nyelvtől, amelyekben a névmások rendszerint mutató tövekből képződnek (vö. még Nö^ZMG 1886, 738).

**5.** 

> 2 according to Phi^St. C. 73 Sperling^Nota Rel. im Hebr. 1876, 15-22 for אֲשֶׁל, developed from the relative שׁ (q. v.) by (1) the prefixing of either a merely prosthetic א, or, better, a pronominal א (giving rise to אש, the form of the relative in Phoenician), and (2) the addition of the demonstrative root ל [found also in הַלָּזֶה אֵלָּה, אֵל, (q. v.), he who, who (plural)]: the main objection to this explanation is the change of ל to ר, which is hardly rendered probable by the compare of Syriac by side of הָלְכָּא ᵑ7.

2 Phi^St. C. 73 Sperling^Nota Rel. im Hebr. 1876, 15-22 szerint אֲשֶׁל helyett áll, és a שׁ vonatkozó szóból (l. ott) fejlődött ki: (1) egy puszta proszthetikus א vagy, ami valószínűbb, egy névmási א elétételével (ebből lett a אש, a vonatkozó szó föníciai alakja), és (2) a ל mutató tő hozzáadásával [ez megvan a הַלָּזֶה אֵלָּה, אֵל, (l. ott) szavakban is: aki, akik (többes szám)]: e magyarázat ellen a fő kifogás a ל ר alakra változása, amelyet aligha tesz valószínűvé a szír összevetése a ᵑ7 הָלְכָּא alakja mellett.

**6.** 

> 1 seems preferable, the primitive root having acquired different significations in the different Semitic languages, and having been weakened in Hebrew to a mere particle of relation). A sign of relation, bringing the clause introduced by it into relation with an antecedent clause. As a rule אֲשֶׁר is a mere connecting link, and requires to be supplemented (see the grammars) by a pronominal affix, or other word, such as שָׁם, defining the nature of the relation more precisely: e.g. Gen 1:11 זַרֵעוֺבֿוֺ אֲשֶׁר literally as to which, its seed is in it = in which is its seed, Psa 1:4 like the chaff רוּחַ אֲשֶׁרתִּֿדְּפֶנּוּ as to which, the wind drives it = which the wind drives, etc.; & so אֲשֶׁרשָׁ֗֗֗ם = where, אֲשֶׁרמִ֗֗֗שָּׁם = whence, Gen 2:11; 3:23; 20:13 etc. Sometimes also (see below) the relation expressed by it is specifically temporal, local causal, etc. More particularly 1 it includes its pronominal antecedent, whether in the nominative or oblique cases, as Num 22:6 יוּאָר תָּאֹר וַאֲשֶׁר and he whom thou cursest is cursed, Exod 4:12 and I will teach thee תְּדַבֵּר אֲשֶׁר that which thou shalt say; and with particles or prepositions, as אֲשֶׁר אֵת (according to the context) him who . . ., those who . . ., that which . . .; לַאֲשֶׁר to him who . . . Gen 43:16, to those who . . . 47:24, to that which 27:8; מֵאֲשֶׁר Judg 16:30; 2Sam 18:18 than those whom; Lev 27:24 מֵאִתּוֺ קָנָהוּ לַאֲשֶׁר to him from whom he bought it, Num 5:7; Isa 24:2 בוֺ נשֶׁא כַּאֲשֶׁר like him against whom there is a creditor.

1 tűnik előnyösebbnek: az ősi tő a különböző sémi nyelvekben különböző jelentéseket vett fel, a héberben pedig puszta vonatkozó partikulává gyengült). Vonatkozást jelölő jel, amely az általa bevezetett mellékmondatot egy előzményként álló mondattal hozza vonatkozásba. A אֲשֶׁר rendszerint puszta összekötő kapocs, és (l. a nyelvtanokat) névmási affixummal vagy más szóval, például שָׁם szóval kell kiegészíteni, amely a vonatkozás természetét pontosabban meghatározza: pl. 1Móz 1:11 זַרֵעוֺבֿוֺ אֲשֶׁר szó szerint: amelynek, a magva benne van = amelyben a magva van, Zsolt 1:4 mint a polyva, רוּחַ אֲשֶׁרתִּֿדְּפֶנּוּ amelyet, a szél hordja azt = amelyet a szél hord, stb.; és így אֲשֶׁרשָׁ֗֗֗ם = ahol, אֲשֶׁרמִ֗֗֗שָּׁם = ahonnan, 1Móz 2:11; 3:23; 20:13 stb. Néha (l. lent) az általa kifejezett vonatkozás kifejezetten időbeli, helyi, okbeli stb. Közelebbről 1 magában foglalja névmási előzményét, akár alanyesetben, akár függő esetekben, mint 4Móz 22:6 יוּאָר תָּאֹר וַאֲשֶׁר és akit te megátkozol, az átkozott, 2Móz 4:12 és megtanítalak תְּדַבֵּר אֲשֶׁר arra, amit mondanod kell; partikulákkal vagy elöljárószókkal is, mint אֲשֶׁר אֵת (a szövegösszefüggés szerint) azt, aki ..., azokat, akik ..., azt, ami ...; לַאֲשֶׁר annak, aki ... 1Móz 43:16, azoknak, akik ... 47:24, annak, ami 27:8; מֵאֲשֶׁר Bír 16:30; 2Sám 18:18 mint azok, akiket; 3Móz 27:24 מֵאִתּוֺ קָנָהוּ לַאֲשֶׁר annak, akitől megvette, 4Móz 5:7; Ézs 24:2 בוֺ נשֶׁא כַּאֲשֶׁר mint az, aki ellen hitelezője van.

**7.** 

> 2 instances of אֲשֶׁר followed by a pronominal affix, or by מִשָּׁם שָֽׁמָּה, שָׁם,, are so common that the examples cited above will be sufficient. Very rarely there occurs the anomalous construction אֲשֶׁר עִם Gen 31:32 for עִמּוֺ אֲשֶׁר (see 44:9), בַּאֲשֶׁר Isa 47:12 for לַאֲשֶׁר בָּהֶם, אֲשֶׁר for אֲשֶׁרלָ֗֗֗הֶם Ezek 23:40: Psa 119:49 see under אשׁר על. It is followed by the pronoun in the nominative, in the following cases: — (a) immediately, mostly before an adjective or participle, Gen 9:3 all moving things הוּאחַֿי אֲשֶׁר which are living, Lev 11:26; Num 9:13; 14:8, 27; 35:31; Deut 20:20; 1Sam 10:19 (see Dr) 2Kin 25:19 (|| Jer 52:25 היה) 27:9; Ezek 43:19; Hag 1:9; Ruth 4:15; Neh 2:18; Eccl 7:26; before a verb 2Kin 22:13 (omitted 2Chr 34:21). (b) in a negative sentence, at the end: Gen 7:2; 17:12; Num 17:5; Deut 17:15 הוּא אָחִיךָ לֹא אֲשֶׁר who is not thy brother, 20:15; Judg 19:12; 1Kin 8:41 || 9:20 ||. N.B. Psa 16:3 הֵ֑מָּה בָּאָרֶץ אֲשֶׁר is an unparalleled expression for 'who are in the land'; read וג אַדִּירֵי הֵמָּה בָּאָ֑רֶץ ׳אֲשֶׁר 'the saints that are in the land, they (המה) are the nobles, in whom,' etc.

2 a אֲשֶׁר névmási affixummal vagy מִשָּׁם שָֽׁמָּה, שָׁם,, szóval követett esetei olyan gyakoriak, hogy a fent idézett példák elegendők. Nagyon ritkán előfordul a rendhagyó אֲשֶׁר עִם szerkezet 1Móz 31:32 עִמּוֺ אֲשֶׁר helyett (l. 44:9), בַּאֲשֶׁר Ézs 47:12 לַאֲשֶׁר בָּהֶם helyett, אֲשֶׁר אֲשֶׁרלָ֗֗֗הֶם helyett Ez 23:40: a Zsolt 119:49-hez l. אשׁר על alatt. Alanyesetű névmás követi a következő esetekben: — (a) közvetlenül, többnyire melléknév vagy participium előtt, 1Móz 9:3 minden mozgó, הוּאחַֿי אֲשֶׁר ami él, 3Móz 11:26; 4Móz 9:13; 14:8, 27; 35:31; 5Móz 20:20; 1Sám 10:19 (l. Dr) 2Kir 25:19 (|| Jer 52:25 היה) 27:9; Ez 43:19; Hag 1:9; Ruth 4:15; Neh 2:18; Préd 7:26; ige előtt 2Kir 22:13 (kihagyva 2Krón 34:21). (b) tagadó mondatban, a végén: 1Móz 7:2; 17:12; 4Móz 17:5; 5Móz 17:15 הוּא אָחִיךָ לֹא אֲשֶׁר aki nem a testvéred, 20:15; Bír 19:12; 1Kir 8:41 || 9:20 ||. N.B. A Zsolt 16:3 הֵ֑מָּה בָּאָרֶץ אֲשֶׁר példa nélküli kifejezés erre: 'akik a földön vannak'; olv. וג אַדִּירֵי הֵמָּה בָּאָ֑רֶץ ׳אֲשֶׁר 'a szentek, akik a földön vannak, ők (המה) a nemesek, akikben,' stb.

**8.** 

> 3 sometimes (though rarely) the defining adjunct is a pronoun of 1 or 2 person as well as of 3 person. In such cases it is strictly to be rendered I who . . ., thou who, etc.; Hosea 14:4 יָתוֺם יְרֻחַם אֲשֶׁרבְּֿךָ thou by whom the fatherless is compassionated ! Jer 31:32 I, whose covenant they brake, 32:19; Isa 49:23; Job 37:17f. thou whose garments are warm . . ., canst thou ? etc., Psa 71:19; 71:20; 144:12 we whose sons, etc., 139:15 my frame was not hidden from thee, בַסֵּתֶר אֲ֯שֶׁרעֻֿשֵּׂיתִי I who was wrought in secret (= though I was wrought in secret), Exod 14:13 for ye who have seen the Egyptians to-day, — ye shall not see them again for ever! (compare Psa 41:9).

3 néha (bár ritkán) a meghatározó járulék nemcsak harmadik, hanem első vagy második személyű névmás is. Ilyenkor szorosan véve így fordítandó: én, aki ..., te, aki stb.; Hós 14:4 יָתוֺם יְרֻחַם אֲשֶׁרבְּֿךָ te, akinél az árva irgalmat talál! Jer 31:32 én, akinek szövetségét megszegték, 32:19; Ézs 49:23; Jób 37:17k. te, akinek ruhái melegek ..., tudod-e? stb., Zsolt 71:19; 71:20; 144:12 mi, akiknek fiai stb., 139:15 csontom nem volt elrejtve előled, בַסֵּתֶר אֲ֯שֶׁרעֻֿשֵּׂיתִי én, akit titokban formáltak (= noha titokban formáltak), 2Móz 14:13 mert ti, akik ma láttátok az egyiptomiakat, — soha többé nem látjátok őket! (vö. Zsolt 41:9).

**9.** 

> 4 the defining pron. adjunct is dispensed with —

4 a meghatározó névmási járulék elmarad —

**10.** 

> a. when אֲשֶׁר represents the simple subject of a sentence, or the direct object of a verb: so constantly, as Gen 2:1 the work עָשָׂה אֲשֶׁר which he made, 3:3 the tree הַגָּן בְּתוֺךְ אֲשֶׁר which is in the midst of the garden, etc.

a. ha a אֲשֶׁר a mondat egyszerű alanyát vagy az ige közvetlen tárgyát képviseli: így állandóan, mint 1Móz 2:1 a mű, עָשָׂה אֲשֶׁר amelyet alkotott, 3:3 a fa, הַגָּן בְּתוֺךְ אֲשֶׁר amely a kert közepén van stb.

**11.** 

> b. after words denoting time, place, or manner, so that אֲשֶׁר then becomes equivalent to when, where, why: (a) Gen 6:4 אֲשֶׁר כֵן אַחֲרֵי afterwards, when, etc. (compare 2Chr 35:20) Gen 45:6 there are still 5 years חָרִישׁ אֵין אֲשֶׁר when there shall be no plowing, Josh 14:10; 1Kin 22:25; after יוֺם or הַיּוֺם Deut 4:10; Judg 4:14; 1Sam 24:5 (see Dr) 2Sam 19:25; Jer 20:14 and elsewhere; similarly Gen 40:13.

b. időt, helyet vagy módot jelentő szavak után, úgyhogy a אֲשֶׁר ilyenkor = amikor, ahol, amiért: (a) 1Móz 6:4 אֲשֶׁר כֵן אַחֲרֵי azután, amikor stb. (vö. 2Krón 35:20) 1Móz 45:6 van még 5 év, חָרִישׁ אֵין אֲשֶׁר amikor nem lesz szántás, Józs 14:10; 1Kir 22:25; יוֺם vagy הַיּוֺם után 5Móz 4:10; Bír 4:14; 1Sám 24:5 (l. Dr) 2Sám 19:25; Jer 20:14 és máshol; hasonlóan 1Móz 40:13.

**12.** 

> (β) 35:13 אִתּוֺ דִּבֶּר אֲשֶׁר בַּמָּקוֺם in the place where he spake with him, 35:14; 39:20; Num 13:27; 22:26; Deut 1:31 in the desert which thou sawest, where (accents Ke Di), 8:15; 1Kin 8:9 (unless הַבְּרִית לוּחוֺת has here fallen out: see ᵐ5 & Deut 9:9) Isa 55:11; 64:10; Psa 84:4. So (γ) in אֲשֶׁר אֶל to (the place) which (or whither) Exod 32:34; Ruth 1:16; אֶלכָּֿלאֲֿשֶׁר to every (place) whither Josh 1:16; Prov 17:8; בַּאֲשֶׁר in (the place) where Judg 5:27; 17:8-9, 1Sam 23:13; 2Kin 8:1; Ruth 1:16-17, Job 39:30, once only with שָׁם Gen 21:17; אֲשֶׁר בְּכֹל wheresoever Josh 1:7, 9; Judg 2:15; 1Sam 14:47; 18:5; 2Sam 7:7; 2Kin 18:7; מֵאֲשֶׁר from (the place) where = whencesoever Exod 5:11; Ruth 2:9; עַלאֲֿשֶׁר to (the place) whither (or which) 2Sam 15:20; 1Kin 18:12; עַלכָּֿלאֲֿשֶׁר Jer 1:7.

(β) 35:13 אִתּוֺ דִּבֶּר אֲשֶׁר בַּמָּקוֺם azon a helyen, ahol beszélt vele, 35:14; 39:20; 4Móz 13:27; 22:26; 5Móz 1:31 a pusztában, amelyet láttál, ahol (a hangsúlyjelek, Ke Di szerint), 8:15; 1Kir 8:9 (hacsak a הַבְּרִית לוּחוֺת itt ki nem esett: l. ᵐ5 és 5Móz 9:9) Ézs 55:11; 64:10; Zsolt 84:4. Így (γ) a אֲשֶׁר אֶל kifejezésben: oda (a helyre), amely (vagy ahová) 2Móz 32:34; Ruth 1:16; אֶלכָּֿלאֲֿשֶׁר minden (helyre), ahová Józs 1:16; Péld 17:8; בַּאֲשֶׁר ott (a helyen), ahol Bír 5:27; 17:8-9, 1Sám 23:13; 2Kir 8:1; Ruth 1:16-17, Jób 39:30, csak egyszer שָׁם szóval 1Móz 21:17; אֲשֶׁר בְּכֹל bárhol Józs 1:7, 9; Bír 2:15; 1Sám 14:47; 18:5; 2Sám 7:7; 2Kir 18:7; מֵאֲשֶׁר onnan (a helyről), ahol = bárhonnan 2Móz 5:11; Ruth 2:9; עַלאֲֿשֶׁר oda (a helyre), ahová (vagy amely) 2Sám 15:20; 1Kir 18:12; עַלכָּֿלאֲֿשֶׁר Jer 1:7.

**13.** 

> (δ) ֗֗֗ אֲשֶׁר הַדָּבָר זֶה this is the reason that or why . . . Josh 5:4; 1Kin 11:27.

(δ) ֗֗֗ אֲשֶׁר הַדָּבָר זֶה ez az oka annak, hogy vagy amiért ... Józs 5:4; 1Kir 11:27.

**14.** 

> c. more extreme instances Lev 14:22, 30, 31; Num 6:21; Deut 7:19 (wherewith), 28:20; 1Sam 2:32 (wherein), 1Kin 2:26; Judg 8:15 (about whom), Isa 8:12 (where יאמר would be followed normally by לוֺ), 31:6 turn ye to (him as to) whom they have deeply rebelled, 47:15; Zeph 3:11; Eccl 3:9; 1Kin 14:19 (= how).

c. szélsőségesebb esetek 3Móz 14:22, 30, 31; 4Móz 6:21; 5Móz 7:19 (amellyel), 28:20; 1Sám 2:32 (amelyben), 1Kir 2:26; Bír 8:15 (akiről), Ézs 8:12 (ahol a יאמר után rendesen לוֺ következnék), 31:6 térjetek vissza (ahhoz), aki ellen mélyen fellázadtak, 47:15; Sof 3:11; Préd 3:9; 1Kir 14:19 (= hogyan).

**15.** 

> d. it is dispensed with only in appearance after וג (אָמַרְתִּי אָמַר ׅ׳אֲשֶׁר followed by the words used, its place being really taken by a pronoun in the speech which follows, as Gen 3:17 the tree as to which I commanded thee saying, Thou shalt not eat from it, Exod 22:8; Deut 28:68; Judg 7:4 (זֶה) 8:15 (where the noun repeated takes the place of the pronoun, compare Deut 9:2) 1Sam 9:17 (זֶה):23 +; compare 2Sam 11:16; 2Kin 17:12; 21:4. 5 אֲשֶׁר sometimes in poetry = one who, a man who (men who), ὅστις, οἵτινες, Psa 24:4; 55:20; 95:4; 95:5; Job 4:19; 5:5; 9:5 (Hi) 15:17. 6 אֲשֶׁר occasionally receives its closer definition by a substantive following it, in other words, its logical antecedent is inserted in the relative clause: (a) in the phrase peculiar to Jeremiah, י דְבַר הָיָה ׳אֲשֶׁר יר ׳אֶל that which came (of) the word of ׳י to Jeremiah Jer 14:1; 46:1; 47:1; 49:34 (compare Ew^§ 334); (b) Exod 25:9; Num 33:4; 1Sam 25:30; 2Kin 8:12; 12:6 בָּֽדֶק׃ שָׁם אֲשֶׁריִֿמָּצֵא לְכֹל Ezek 12:25; compare the Ethiopic usage Di^§ 201; (c) (antecedant repeated) Gen 49:30 = 50:13, 1Sam 25:30 (׳י repeated), Isa 54:9 (probably) as to which I sware that, etc., Amos 5:1 which I take up over you (as) a dirge. 7 ל ׳אֲשֶׁר that (belongs, belong, belonged) to, is used a. either alone or preceded by כָּלֿ to express (all) that (belongs) to, as Gen 14:23 מִכָּלאֲֿשֶׁרלְֿךָ of all that is thine, 31:1 לְאָבִינוּ מֵאֲשֶׁר of that which was our father's, 32:24 & sent over אֶתאֲֿשֶׁרלֿוֺ that which he had, + often b. as a circumlocution of the Genitive, as Gen 29:9 לְאָבִיהָ אֲשֶׁר עִםהַֿצּאֹן with the sheep that were her father's, 40:5; 47:4; Lev 9:8; Judg 6:11; 1Sam 25:7 אֲשֶׁרלְֿךָ הָרֹעִים, 2Sam 14:31 אֲשֶׁרלִֿי אֶתהַֿחֶלְקָה, 23:8; 1Kin 1:8, 33 אֲשֶׁרלִֿי הַמִּרְדָּה עַל upon mine own mule, 1:49; 4:2; 2Kin 11:10; 16:13; Ruth 2:21; and especially in the case of a compound expression depending on a single Genitive, as Gen 23:9; 40:5; 41:43 אֲשֶׁרלֿוֺ הַמִּשְׁנֶה מִרְכֶּבֶת the chariot of the second rank which he had, Exod 38:30; Judg 3:20; 6:25; 1Sam 17:40; 21:8 לְשָׁאוּל אֲשֶׁר הָרֹעִים אֲבִיר the mightiest of Saul's herdmen, 24:5 אֲשֶׁרלְֿשָׁאוּל אֶתכְּֿנַףהַֿמְּעִיל, 2Sam 2:8 Saul's captain of the host, 1Kin 10:28; 15:20; 22:31; Jer 52:17; Ruth 4:3.

d. csak látszólag marad el וג után (אָמַרְתִּי אָמַר ׅ׳אֲשֶׁר, amelyet a használt szavak követnek, mivel helyét valójában egy névmás foglalja el a következő beszédben, mint 1Móz 3:17 a fa, amelyre nézve megparancsoltam neked, mondván: Ne egyél belőle, 2Móz 22:8; 5Móz 28:68; Bír 7:4 (זֶה) 8:15 (ahol a megismételt főnév foglalja el a névmás helyét, vö. 5Móz 9:2) 1Sám 9:17 (זֶה):23 és máshol; vö. 2Sám 11:16; 2Kir 17:12; 21:4. 5 A אֲשֶׁר a költészetben néha = olyan, aki, olyan ember, aki (olyanok, akik), ὅστις, οἵτινες, Zsolt 24:4; 55:20; 95:4; 95:5; Jób 4:19; 5:5; 9:5 (Hi) 15:17. 6 A אֲשֶׁר alkalmanként egy utána következő főnév által kap közelebbi meghatározást, más szóval logikai előzménye a vonatkozó mellékmondatba kerül: (a) a Jeremiásra jellemző kifejezésben: י דְבַר הָיָה ׳אֲשֶׁר יר ׳אֶל ami jött, (tudniillik) ׳י szava Jeremiáshoz Jer 14:1; 46:1; 47:1; 49:34 (vö. Ew^§ 334); (b) 2Móz 25:9; 4Móz 33:4; 1Sám 25:30; 2Kir 8:12; 12:6 בָּֽדֶק׃ שָׁם אֲשֶׁריִֿמָּצֵא לְכֹל Ez 12:25; vö. az etióp használatot Di^§ 201; (c) (az előzmény megismételve) 1Móz 49:30 = 50:13, 1Sám 25:30 (׳י megismételve), Ézs 54:9 (valószínűleg) amire nézve megesküdtem, hogy stb., Ámós 5:1 amelyet (mint) siratóéneket mondok rólatok. 7 A ל ׳אֲשֶׁר ami (tartozik, tartoznak, tartozott) valakihez, használatos a. akár önmagában, akár כָּלֿ után, ennek kifejezésére: (mind)az, ami valakié, mint 1Móz 14:23 מִכָּלאֲֿשֶׁרלְֿךָ semmit abból, ami a tiéd, 31:1 לְאָבִינוּ מֵאֲשֶׁר abból, ami atyánké volt, 32:24 és átküldte, אֶתאֲֿשֶׁרלֿוֺ ami az övé volt, és gyakran máshol b. a birtokos eset körülírásaként, mint 1Móz 29:9 לְאָבִיהָ אֲשֶׁר עִםהַֿצּאֹן a juhokkal, amelyek atyjáé voltak, 40:5; 47:4; 3Móz 9:8; Bír 6:11; 1Sám 25:7 אֲשֶׁרלְֿךָ הָרֹעִים, 2Sám 14:31 אֲשֶׁרלִֿי אֶתהַֿחֶלְקָה, 23:8; 1Kir 1:8, 33 אֲשֶׁרלִֿי הַמִּרְדָּה עַל a saját öszvéremen, 1:49; 4:2; 2Kir 11:10; 16:13; Ruth 2:21; és különösen olyan összetett kifejezés esetén, amely egyetlen birtokostól függ, mint 1Móz 23:9; 40:5; 41:43 אֲשֶׁרלֿוֺ הַמִּשְׁנֶה מִרְכֶּבֶת a második rangú szekér, amely az övé volt, 2Móz 38:30; Bír 3:20; 6:25; 1Sám 17:40; 21:8 לְשָׁאוּל אֲשֶׁר הָרֹעִים אֲבִיר Saul pásztorainak legerősebbje, 24:5 אֲשֶׁרלְֿשָׁאוּל אֶתכְּֿנַףהַֿמְּעִיל, 2Sám 2:8 Saul seregének vezére, 1Kir 10:28; 15:20; 22:31; Jer 52:17; Ruth 4:3.

**16.** 

> c. with names of places (especially such as do not readily admit the stative construct) Judg 18:28; 19:14 לְבִנְיָמִין אֲשֶׁר הַגִּבְעָה Gibeah (the hill) of Benjamin, 20:4; 1Sam 17:1; 1Kin 15:27; 16:15; 17:9; 19:3; 2Kin 14:11. compare שֶׁל (q. v.) which in Rabb, like the Aramaic -דִּיל, , is in habitual use as a mark of the Genitive. — N.B. In Aramaic also דּי, , without ל, expresses the Genitive relation, as דִימַֿלְכָּא מִלְּתָא, literally the word, that of the king = the word of the king. The few apparent cases of a similar use of אשׁר are, however, too foreign to the General usage of the language to be regarded otherwise than as due to textual error: 1Sam 13:8 read אָמַר אֲשֶׁר (or שָׂם Exod 19:5) שְׁמוּאֵל (ᵐ5 εἶπε); 1Kin 11:25 supply עָשָׂה (ᵐ5 ἣν ἐποίησεν); 2Kin 25:10 supply אֵת with (as || Jer 52:14); 2Chr 34:22 read הַמֶּלֶךְ אָמַר וַאֲשֶׁר (compare ᵐ5) and those whom the king appointed (abbreviated from 2Kin 22:14); compare Ew^§ 292 a, b with note. 8 אֲשֶׁר becomes, like Aramaic דּי, , a conjunction approximating in usage to כִּי: thus a. = quod, ὅτι, that, subordinating an entire sentence to a verb of knowing, remembering, etc. (a) with אֵת Deut 9:7 forget not הִקְצַפְתָּ אֲשֶׁר אֵת the fact that (= how) thou provokedst, etc., 29:15; Josh 2:10; 1Sam 24:11; 24:19; 2Sam 11:20 know ye not אֲשֶׁריֹֿרוּ אֵת how they shoot from off the wall ? 2Kin 8:12; Isa 38:3 +? 1Kin 14:19; 2Kin 14:15; 20:20. Of time (peculiarly) 2Sam 14:15 אֲשֶׁר עַתָּה now (is it) that . . . Zech 8:20 (probably) yet (shall it be) that . . . 8:23; compare שֶׁ כִּמְעַט Song 3:4.

c. helynevekkel (különösen olyanokkal, amelyek nehezen állnak status constructusban) Bír 18:28; 19:14 לְבִנְיָמִין אֲשֶׁר הַגִּבְעָה Benjámin Gibeája (halma), 20:4; 1Sám 17:1; 1Kir 15:27; 16:15; 17:9; 19:3; 2Kir 14:11. vö. שֶׁל (l. ott), amely a rabbinikus nyelvben, mint az arámi -דִּיל, , a birtokos eset szokásos jele. — N.B. Az arámiban is a דּי, , ל nélkül fejezi ki a birtokos viszonyt, mint דִימַֿלְכָּא מִלְּתָא, szó szerint: a szó, az, ami a királyé = a király szava. A אשׁר néhány látszólag hasonló használata azonban túlságosan idegen a nyelv általános használatától ahhoz, hogy másnak lehessen tekinteni, mint szöveghibának: 1Sám 13:8 olv. אָמַר אֲשֶׁר (vagy שָׂם 2Móz 19:5) שְׁמוּאֵל (ᵐ5 εἶπε); 1Kir 11:25 pótold: עָשָׂה (ᵐ5 ἣν ἐποίησεν); 2Kir 25:10 pótold אֵת szóval (mint || Jer 52:14); 2Krón 34:22 olv. הַמֶּלֶךְ אָמַר וַאֲשֶׁר (vö. ᵐ5) és azok, akiket a király kirendelt (a 2Kir 22:14-ből rövidítve); vö. Ew^§ 292 a, b a jegyzettel. 8 A אֲשֶׁר, az arámi דּי, alakhoz hasonlóan, kötőszóvá válik, amely használatában a כִּי szóhoz közelít: így a. = quod, ὅτι, hogy, egy egész mondatot rendelve a tudás, emlékezés stb. igéje alá. (a) אֵת szóval 5Móz 9:7 ne felejtsd el הִקְצַפְתָּ אֲשֶׁר אֵת azt, hogy (= hogyan) ingerelted stb., 29:15; Józs 2:10; 1Sám 24:11; 24:19; 2Sám 11:20 nem tudjátok-e, אֲשֶׁריֹֿרוּ אֵת hogyan lőnek le a falról? 2Kir 8:12; Ézs 38:3 és máshol? 1Kir 14:19; 2Kir 14:15; 20:20. Időről (sajátosan) 2Sám 14:15 אֲשֶׁר עַתָּה most (van az,) hogy ... Zak 8:20 (valószínűleg) még (lesz az,) hogy ... 8:23; vö. שֶׁ כִּמְעַט Én 3:4.

**17.** 

> (β) without אֵת (not very common, כִּי being usually employed): after יָדַע Exod 11:7; Ezek 20:26 (very strange in Ezekiel: see Hi) Job 9:5 (Ew De Di) Eccl 8:12, רָאָה Deut 1:31 (RV) 1Sam 18:15, הִתְוַדָּה to confess Lev 5:5; 26:40 b, הִשְׁבִּיעַ 1Kin 22:16 (caused to swear that . . .); after a noun Isa 38:7 אֲשֶׁר הָאוֺת the sign that . . . (|| 2Kin 20:9 כִּי): with growing frequency in late Hebrew, 2Chr 2:7, and especially Nehemiah, Esther: Neh 2:5, 10; 7:65 (= Ezra 2:63) Neh 8:14-15, 10:31; 13:1, 19, 22; Est 1:19; 2:10; 3:4; 4:11; 6:2; 8:11; Eccl 3:22 (מֵאֲשֶׁר) 5:4; 7:18 (with טוֺב: contrast Ruth 2:22) 2:22; Ruth 2:29; Ruth 8:12; Ruth 8:14; Ruth 9:1; Dan 1:8 (twice in verse).

(β) אֵת nélkül (nem nagyon gyakori, mivel rendszerint כִּי használatos): יָדַע után 2Móz 11:7; Ez 20:26 (Ezékielnél nagyon furcsa: l. Hi) Jób 9:5 (Ew De Di) Préd 8:12, רָאָה 5Móz 1:31 (RV) 1Sám 18:15, הִתְוַדָּה megvallani 3Móz 5:5; 26:40 b, הִשְׁבִּיעַ 1Kir 22:16 (megeskette, hogy ...); főnév után Ézs 38:7 אֲשֶׁר הָאוֺת a jel, hogy ... (|| 2Kir 20:9 כִּי): a késői héberben egyre gyakrabban, 2Krón 2:7, és különösen Nehémiás és Eszter könyvében: Neh 2:5, 10; 7:65 (= Ezsd 2:63) Neh 8:14-15, 10:31; 13:1, 19, 22; Eszt 1:19; 2:10; 3:4; 4:11; 6:2; 8:11; Préd 3:22 (מֵאֲשֶׁר) 5:4; 7:18 (טוֺב szóval: szemben a Ruth 2:22-vel) 2:22; Ruth 2:29; Ruth 8:12; Ruth 8:14; Ruth 9:1; Dán 1:8 (a versben kétszer).

**18.** 

> (γ) prefixed to a direct citation, like כִּי q. v. (= ὅτι recitativum) (rare) 1Sam 15:20; 2Sam 1:4; 2:4 (see Dr) Psa 10:6 (probably), Neh 4:6.

(γ) egyenes idézet előtt, mint a כִּי, l. ott, (= ὅτι recitativum) (ritka) 1Sám 15:20; 2Sám 1:4; 2:4 (l. Dr) Zsolt 10:6 (valószínűleg), Neh 4:6.

**19.** 

> b. it is resolvable into so that: Gen 11:7 יִשְׁמְעוּ לֹא אֲשֶׁר so that they understand not, etc., 13:16; 22:14 יֵאָמֵר אֲשֶׁר so that it is said, Exod 20:26; Deut 4:10, 40 לְךָ יִיטַב אֲשֶׁר 6:3; 28:27, 51; 1Kin 3:12-13, 2Kin 9:37; Malachi 3:19.

b. úgyhogy-ra bontható fel: 1Móz 11:7 יִשְׁמְעוּ לֹא אֲשֶׁר úgyhogy ne értsék stb., 13:16; 22:14 יֵאָמֵר אֲשֶׁר úgyhogy mondják, 2Móz 20:26; 5Móz 4:10, 40 לְךָ יִיטַב אֲשֶׁר 6:3; 28:27, 51; 1Kir 3:12-13, 2Kir 9:37; Malachi 3:19.

**20.** 

> c. it has a causal force, forasmuch as, in that, since: Gen 30:18; 31:49 and Mizpah, אָמַר אֲשֶׁר for that he said, 34:13, 27; 42:21 we are guilty, רָאִינוּ אֲשֶׁר we who saw (or, in that we saw), Num 20:13 Meribah, because they strove there, Deut 3:24; Josh 4:7, 23; 22:31; Judg 9:17; 1Sam 2:23; 15:15; 20:42 go in peace, נִשְׁבַּעְנוּ אֲשֶׁר forasmuch as we have sworn, 25:26 thou whom (= or, seeing that) ׳י hath withholden, 2Sam 2:5 blessed are ye of עֲשִׂיתֶם אֲשֶׁר ׳י,, who (οἵτινες) have done (or in that ye have done), 1Kin 3:19; 15:5; 2Kin 12:3; 17:4; 23:26; Jer 16:13; Eccl 8:11-12, (Hi De Now). Here also belongs its use in לָמָּה אֲשֶׁר since why . . . ? (= lest) Dan 1:10: see below לָמָּה. On כֵּן עַל אֲשֶׁר forasmuch as Job 34:27 see below כֵּן עַל כִּי.

c. okhatározói ereje van: mivelhogy, azáltal hogy, mivel: 1Móz 30:18; 31:49 és Micpa, אָמַר אֲשֶׁר mert azt mondta, 34:13, 27; 42:21 bűnösek vagyunk, רָאִינוּ אֲשֶׁר mi, akik láttuk (vagy: azáltal, hogy láttuk), 4Móz 20:13 Meriba, mert ott perlekedtek, 5Móz 3:24; Józs 4:7, 23; 22:31; Bír 9:17; 1Sám 2:23; 15:15; 20:42 menj el békével, נִשְׁבַּעְנוּ אֲשֶׁר mivelhogy megesküdtünk, 25:26 te, akit (= vagy: mivel) ׳י visszatartott, 2Sám 2:5 áldottak vagytok עֲשִׂיתֶם אֲשֶׁר ׳י,, által, akik (οἵτινες) megtettétek (vagy: azáltal, hogy megtettétek), 1Kir 3:19; 15:5; 2Kir 12:3; 17:4; 23:26; Jer 16:13; Préd 8:11-12, (Hi De Now). Ide tartozik a לָמָּה אֲשֶׁר mivel miért ...? (= nehogy) kifejezésbeli használata is Dán 1:10: l. lent לָמָּה. A כֵּן עַל אֲשֶׁר mivelhogy Jób 34:27 kifejezéshez l. lent כֵּן עַל כִּי.

**21.** 

> d. it expresses a condition (rare & peculiar): Lev 4:22 יֶחֱטָא נָשִׂיא אֲשֶׁר in (case) that = when (or if) a ruler sinneth (4:3; 4:13; Leviticus 4:37 אִם), Num 5:29 (explained differently by Ew^§ 334 a), Deut 11:27 and the blessing תִּשְׁמְעוּ אֲשֶׁר if ye hearken (11:28 אִם), 18:22 Ges, Josh 4:21 ֗֗֗ יִשְׁאָלוּן אֲשֶׁר when they ask . . ., then . . . (4:6 כִּי), Isa 31:4. In 1Kin 8:33 (|| 2Chr 6:24 כִּי, compare Kings 6:35; 6:37) אֲשֶׁר may be rendered indifferently because or when. Once, similarly, אֲשֶׁר אֵת 1Kin 8:31 (|| אִם).

d. feltételt fejez ki (ritka és sajátos): 3Móz 4:22 יֶחֱטָא נָשִׂיא אֲשֶׁר abban (az esetben), ha = amikor (vagy ha) egy fejedelem vétkezik (4:3; 4:13; 3Móz 4:37 אִם), 4Móz 5:29 (Ew^§ 334 a másként magyarázza), 5Móz 11:27 és az áldás, תִּשְׁמְעוּ אֲשֶׁר ha hallgattok (11:28 אִם), 18:22 Ges, Józs 4:21 ֗֗֗ יִשְׁאָלוּן אֲשֶׁר amikor kérdezik ..., akkor ... (4:6 כִּי), Ézs 31:4. Az 1Kir 8:33-ban (|| 2Krón 6:24 כִּי, vö. Kings 6:35; 6:37) a אֲשֶׁר egyaránt fordítható mert-nek vagy amikor-nak. Egyszer hasonlóan אֲשֶׁר אֵת 1Kir 8:31 (|| אִם).

**22.** 

> e. perhaps (exceptionally) = כַּאֲשֶׁר, as, Jer 33:22; Isa 54:9 (followed by כֵּן; but כֵּן q. v. sometimes stands without כאשׁר, & אשׁר may in these passages connect with what precedes); according to some also Jer 48:8; Psa 106:34 (in a connection where כַּאֲשֶׁר would be more usual: אֲשֶׁר may however be the object of אָמַר). In 1Sam 16:7 הָאָדָם יִרְאֶה אֲשֶׁר read כַּאֲשֶׁר, see Dr.

e. talán (kivételesen) = כַּאֲשֶׁר, ahogy, Jer 33:22; Ézs 54:9 (כֵּן követi; de a כֵּן, l. ott, néha כאשׁר nélkül áll, és a אשׁר ezeken a helyeken az előzőekhez is kapcsolódhat); egyesek szerint Jer 48:8; Zsolt 106:34 is (olyan összefüggésben, ahol a כַּאֲשֶׁר volna szokásosabb: a אֲשֶׁר azonban lehet a אָמַר tárgya is). Az 1Sám 16:7-ben הָאָדָם יִרְאֶה אֲשֶׁר olv. כַּאֲשֶׁר, l. Dr.

**23.** 

> f. combined with prepositions, אֲשֶׁר converts them into conjunctions: see below, מֵאֲשֶׁר כַּאֲשֶׁר, בַּאֲשֶׁר,. On its use similarly with תַּחַת מִמְּנֵי, עֵקֶב, עַל, עַד, כְּפִי, לְמַעַן, יַעַן, דְּבַר, עַל בַּעֲבוּר, מִבְּלִי, אַחַר, (אַחֲרֵי), see these words. — הַאֲשֶׁר, with ה interrogative, occurs once, 2Kin 6:22. In Deut 15:14 also read כַּאֲשֶׁר: note ברכך before. Note1אֲשֶׁר being a connecting link, without any perfectly corresponding equivalent in English, its force is not unfrequently capable of being represented in more than one way. See e.g. 2Sam 2:5 (above 8c), Isa 28:12 unto whom he said, or for that he said to them. Note 2. The opinion that אֲשֶׁר has an asseverative force (like כִּי, q. v.), or introduces the apodosis, is not probably, being both alien to its General usage & not required by the passages alleged. Render Isa 8:20 either 'Surely according to this word will those speak who have no dawn,' or '. . . will they speak when (compare above 8d Deut 11:27; Josh 4:21) they have no dawn.' בַּאֲשֶׁר_19 a. in (that) which . . . Isa 56:4; 65:12; 66:4 (above 1); Eccl 3:9 in (that, in) which (4c); Isa 47:12 (see 2).

f. elöljárószókkal kapcsolva a אֲשֶׁר kötőszóvá alakítja őket: l. lent מֵאֲשֶׁר כַּאֲשֶׁר, בַּאֲשֶׁר,. Hasonló használatáról תַּחַת מִמְּנֵי, עֵקֶב, עַל, עַד, כְּפִי, לְמַעַן, יַעַן, דְּבַר, עַל בַּעֲבוּר, מִבְּלִי, אַחַר, (אַחֲרֵי) mellett l. e szavakat. — A הַאֲשֶׁר, kérdő ה partikulával egyszer fordul elő, 2Kir 6:22. Az 5Móz 15:14-ben is כַּאֲשֶׁר olvasandó: figyeld meg az előtte álló ברכך alakot. Megjegyzés1 Mivel a אֲשֶׁר összekötő kapocs, amelynek nincs tökéletesen megfelelő angol egyenértékese, ereje nem ritkán többféleképpen is visszaadható. L. pl. 2Sám 2:5 (fent 8c), Ézs 28:12 akiknek azt mondta, vagy: mivel azt mondta nekik. Megjegyzés 2. Az a vélemény, hogy a אֲשֶׁר megerősítő erejű (mint a כִּי, l. ott), vagy az utótagot vezeti be, nem valószínű, mivel általános használatától idegen, és az idézett helyek sem kívánják meg. Az Ézs 8:20 fordítandó vagy így: 'Bizony e szó szerint szólnak majd azok, akiknek nincs hajnaluk,' vagy így: '... akkor szólnak majd, amikor (vö. fent 8d 5Móz 11:27; Józs 4:21) nincs hajnaluk.' בַּאֲשֶׁר_19 a. abban, ami ... Ézs 56:4; 65:12; 66:4 (fent 1); Préd 3:9 abban (azáltal), amiben (4c); Ézs 47:12 (l. 2).

**24.** 

> b. adverb in (the place) where: above 4b (γ).

b. határozószó: ott (a helyen), ahol: fent 4b (γ).

**25.** 

> c. conjunction in that, inasmuch as, Gen 39:9, 23; Eccl 7:2; 8:4; compare .

c. kötőszó: azáltal hogy, mivel, 1Móz 39:9, 23; Préd 7:2; 8:4; vö. .

**26.** 

> d. Jonah 1:8 לְמִי בַּאֲשֶׁר on account of whom ? (לְ בַּאֲשֶׁר on account of, framed on model of Aramaic בְּדִיל: see below שֶׁל). כַּאֲשֶׁר see below כְּ. מֵאֲשֶׁר_17 a. from (or than) that which (him, them, etc., that . . .) Gen 3:11; Exod 29:27 (twice in verse); Num 6:11 (see Lev 4:26; Josh 10:11; Judg 16:30; Isa 47:13 +; than that . . . Eccl 3:22; מֵאֲשֶׁר לְבַד Est 4:11.

d. Jón 1:8 לְמִי בַּאֲשֶׁר ki miatt? (לְ בַּאֲשֶׁר valami miatt, az arámi בְּדִיל mintájára alkotva: l. lent שֶׁל). כַּאֲשֶׁר l. lent כְּ. מֵאֲשֶׁר_17 a. abból (vagy annál), ami (az, aki, azok, akik stb. ...) 1Móz 3:11; 2Móz 29:27 (a versben kétszer); 4Móz 6:11 (l. 3Móz 4:26; Józs 10:11; Bír 16:30; Ézs 47:13 és máshol; mint az, hogy ... Préd 3:22; מֵאֲשֶׁר לְבַד Eszt 4:11.

**27.** 

> b. adverb from (the place) where: above 4a (β).

b. határozószó: onnan (a helyről), ahol: fent 4a (β).

**28.** 

> c. conjunction from (the fact) that . . ., since Isa 43:4. כַּאֲשֶׁר conjunction according as, as, when (compare for the combined Aramaic כַּד כְּדִי,) —

c. kötőszó: abból (a tényből), hogy ..., mivel Ézs 43:4. כַּאֲשֶׁר kötőszó: aszerint, ahogy; ahogy; amikor (vö. az összetett arámi כַּד כְּדִי,) —

**29.** 

> 1 according to that which, according as, as:

1 aszerint, ami; aszerint, ahogy; ahogy:

**30.** 

> a. Gen 34:12 I will give אלי תאמרו כאשׁר according as ye shall (or may) say unto me, 44:1; Exod 8:23; Num 22:8; 1Sam 2:16; Gen 34:22 if we are circumcised נמולים הם כאשׁר; 41:21 בתחלה כאשׁר as at the beginning, so בראשׁונה ׳כ Josh 8:5-6, 2Sam 7:10; Exod 5:13 התבן בהיות ׃כאשׁר Gen 7:9 they came in two by two אלהִים צוה כאשׁר, as God commanded Noah; so, or similarly, very often, especially in P, 7:16; 8:21; 12:4; 17:23; 21:1 (twice in verse); Exod 16:24; 39:1, 5, 7; Num 3:16, 42 etc.; י דבר ׳כאשׁר Deut 1:21; 2:1; 6:3, 19 +? Deuteronomy.

a. 1Móz 34:12 megadom אלי תאמרו כאשׁר aszerint, ahogy mondjátok (vagy mondhatjátok) nekem, 44:1; 2Móz 8:23; 4Móz 22:8; 1Sám 2:16; 1Móz 34:22 ha körülmetélkedünk נמולים הם כאשׁר; 41:21 בתחלה כאשׁר mint kezdetben, úgy בראשׁונה ׳כ Józs 8:5-6, 2Sám 7:10; 2Móz 5:13 התבן בהיות ׃כאשׁר 1Móz 7:9 kettesével jöttek אלהִים צוה כאשׁר, ahogy Isten megparancsolta Noénak; így, vagy hasonlóan, igen gyakran, különösen P-ben, 7:16; 8:21; 12:4; 17:23; 21:1 (a versben kétszer); 2Móz 16:24; 39:1, 5, 7; 4Móz 3:16, 42 stb.; י דבר ׳כאשׁר 5Móz 1:21; 2:1; 6:3, 19 és máshol? Deuteronomium.

**31.** 

> b. answered, for increased emphasis, by כֵּן (compare כְּ 2d), Gen 50:12 צִוָּם כאשׁר כן ויעשׂו, Exod 7:10, 20; Gen 18:5 (J) דברת כאשׁר חעשׂח כן, Exod 10:10 (iron.), Amos 5:14 (do.); in opposed to order, Judg 1:7 לי שׁלם כן עשׂיתי, כאשׁר, Exod 7:6 י צוה ׳כאשׁר עשׂו כן, compare 12:28, 50; 39:43; Num 5:4; Numbers 17:26; 36:10 (all P); with imperfect (frequently) 2:17 (P) יסעו כן יחנו כאשׁר; of degree = the more. . . the more, Exod 1:12 יפרץ וכן ירבה כן אתו יענּו וכאשׁר, compare 17:11 (JE) ישׁר יריםו֗֗֗גבר כאשׁר ׳והיה according as he held up, etc., Israel prevailed; in an oath or solemn promise, Num 14:28 אעשׂה כן דברתם כאשׁר לא אם, Deut 28:63 (Jer 31:28), 1Kin 1:30; Isa 10:11; 14:24; 52:14f. (see כֵּן 2b).

b. nagyobb nyomaték kedvéért כֵּן felel rá (vö. כְּ 2d), 1Móz 50:12 צִוָּם כאשׁר כן ויעשׂו, 2Móz 7:10, 20; 1Móz 18:5 (J) דברת כאשׁר חעשׂח כן, 2Móz 10:10 (ironikusan), Ámós 5:14 (ua.); fordított sorrendben, Bír 1:7 לי שׁלם כן עשׂיתי, כאשׁר, 2Móz 7:6 י צוה ׳כאשׁר עשׂו כן, vö. 12:28, 50; 39:43; 4Móz 5:4; 4Móz 17:26; 36:10 (mind P); imperfectummal (gyakran) 2:17 (P) יסעו כן יחנו כאשׁר; fokról = minél ... annál, 2Móz 1:12 יפרץ וכן ירבה כן אתו יענּו וכאשׁר, vö. 17:11 (JE) ישׁר יריםו֗֗֗גבר כאשׁר ׳והיה amint felemelte stb., Izráel győzött; esküben vagy ünnepélyes ígéretben, 4Móz 14:28 אעשׂה כן דברתם כאשׁר לא אם, 5Móz 28:63 (Jer 31:28), 1Kir 1:30; Ézs 10:11; 14:24; 52:14k. (l. כֵּן 2b).

**32.** 

> c. answered by וַ (Dr^§ 127 γ) Exod 16:34; Num 1:19.

c. וַ felel rá (Dr^§ 127 γ) 2Móz 16:34; 4Móz 1:19.

**33.** 

> d. often in similes (followed by imperfect of habit) Exod 33:11 רעהו אל אישׁ ידבר כאשׁר, Num 11:12; Deut 1:44; Isa 9:2; 66:20 +, answered by כֵּן 31:4; 55:10; 66:22; Amos 3:12 +; a second verb is, in such cases, in the perfect with וְ consecutive (Dr^§ 115) Deut 22:26; Isa 29:8 יחלםו֗֗֗הקיץ כאשׁר, 65:8; Amos 5:19.

d. gyakran hasonlatokban (szokást kifejező imperfectum követi) 2Móz 33:11 רעהו אל אישׁ ידבר כאשׁר, 4Móz 11:12; 5Móz 1:44; Ézs 9:2; 66:20 és máshol, כֵּן felel rá 31:4; 55:10; 66:22; Ámós 3:12 és máshol; ilyen esetekben a második ige וְ consecutivummal álló perfectumban van (Dr^§ 115) 5Móz 22:26; Ézs 29:8 יחלםו֗֗֗הקיץ כאשׁר, 65:8; Ámós 5:19.

**34.** 

> e. כַּאֲשֶׁר הָיָה (compare כְּ הָיָה) to be as if, Job 10:19 אהיה הייתי לא כאשׁר, Zech 10:6 זנחתים לא כאשׁר והיו.

e. כַּאֲשֶׁר הָיָה (vö. כְּ הָיָה) olyan lenni, mintha, Jób 10:19 אהיה הייתי לא כאשׁר, Zak 10:6 זנחתים לא כאשׁר והיו.

**35.** 

> 2 with a casual force, in so far as, since (German demgemäss dass), Gen 26:29 if thou doest us no harm נגענוך לא כאשׁר according as, in so far as, we have not touched thee; Num 27:14 פי מריתם כאשׁר inasmuch as ye have defied my mouth, Judg 6:27; 1Sam 28:18 (answered by כן על), 2Kin 17:26; Micah 3:4.

2 okhatározói erővel: amennyiben, mivel (német demgemäss dass), 1Móz 26:29 ha nem teszel nekünk rosszat, נגענוך לא כאשׁר aszerint, amennyiben mi sem bántottunk téged; 4Móz 27:14 פי מריתם כאשׁר mivelhogy ellenszegültetek parancsomnak, Bír 6:27; 1Sám 28:18 (כן על felel rá), 2Kir 17:26; Mik 3:4.

**36.** 

> 3 with a temporal force, when, Gen 18:33 and Y. went away כלה כאשׁר when he had finished, etc., 32:3; 32:32; 1Sam 8:6; 2Sam 12:21 +; answered by וַּ (Dr^§ 127 β), 1Sam 6:6; 12:8; כאשׁר֗֗ ויהי and it came to pass, when . . . Gen 12:11; 20:13; 24:22, 52; Exod 32:19 + often; Gen 43:14 שׁכלתי שׁכלתי כאשׁר when I am bereaved, I am bereaved ! an expression of resignation, so Est 4:16 אבדתי אבדתי כאשׁר. Josh 2:7 כאשׁר אחרי is a 'conflate' reading, omit either אחרי or כ. Of future time, Gen 27:40; 40:14 לך ייטב כאשׁר, Hosea 7:12; Ecclesiastes 4:17; Eccl 5:3, and without a verb Isa 23:5 למצרים שׁמע כאשׁר. — Micah 3:3 כאשׁר is simply as that which, Job 29:25 as one who. שֶׁ, also ( Gen 6:3 [? see 4a], Judg 5:7 (twice in verse); Song 1:7; Job 19:29 [?]) שָׁ שַּׁ , in שָׁאַתָּה Judg 6:17, and שְׁ in שְׁהוּא Eccl 2:22, שְׁהֵם 3:18 (elsewhere before guttural שֶׁ, as שֶׁאֲנִי Song 1:6; Eccl 2:18, שֶׁאֵין Psa 146:3, שֶׁהֵם Song 6:5; Lam 4:9, שֶׁעַל Judg 7:12; 8:26, שֶׁרּאֹשִׁי Song 5:2), relative particle who, which, that, etc. (constantly in Late Hebrew; Aramaic of Nerab, Ldzb^371, 445; Assyrian sha; Phoenician אש (regularly), also sometimes ש (Ldzb^227f.): according to Ges Ew^§ 181 b Ol^p. 439 Sta^§ 176 e, abbreviated from אֲשֶׁר; more probably (Sperling [see אֲשֶׁר], Kö^ii. 323 f.) an original demonstrative particle), synonym with אֲשֶׁר, but in usage limited to late Hebrew, and passages with north Palestinian colouring, namely Judg 5:7 (twice in verse) [אֲשֶׁר 5:27], 6:17; 7:12; 8:26; 2Kin 6:11 (see 4c), Jonah 1:7, 12; 4:10 [אֲשֶׁר11t.], Psa 122:3; 122:4; 123:2; 124:1; 124:2; 124:6; 129:6; 129:7; 133:2; 133:3; 135:2; 135:8; 135:10; 136:23; 137:8; 137:9; 144:15; 146:3; 146:5; Lam 2:15-16, 4:9; 5:18; Ezra 8:20; 1Chr 5:20; 27:27; Canticles (uniformly, except in title Song 1:1); Ecclesiastes (68 t.; אֲשֶׁא89t.); also (dubious) Gen 6:3; 49:10 (ᵑ7 ᵑ6 ᵐ5 שֶׁלֹּה), Job 19:29; and in the proper name (q. v.) מִישָׁאֵל and מְתוּשָׁאֵל. — In usage, שֶּׁ is in the main parallel with אֲשֶׁר, namely 1 as pronoun who, which, whom, Judg 7:12 הַיָּם שְׂפַת שֶׁעַל כַּהוֺל (compare חוֺל c), Psa 122:3; 124:6 etc.; him whom, that which, etc., Song 1:7; 3:1; 1Chr 27:27; Eccl 1:11; 6:3 חַיָּיו יְמֵי שֶׁיִּהְיוּ וְרַב and much (verb) is that which his days amount to (Hi De and others), 6:10; שֶּׁ הוּא that which 1:9 (twice in verse); in the Genitive, שֶּׁ אַשְׁרֵי Psa 137:8; 137:9; 146:5. — On מַהשֶּּֿׁ in Eccl = whatever, what, see מָה 1e b.

3 időhatározói erővel: amikor, 1Móz 18:33 és J. elment, כלה כאשׁר amikor befejezte stb., 32:3; 32:32; 1Sám 8:6; 2Sám 12:21 és máshol; וַּ felel rá (Dr^§ 127 β), 1Sám 6:6; 12:8; כאשׁר֗֗ ויהי és lőn, amikor ... 1Móz 12:11; 20:13; 24:22, 52; 2Móz 32:19 és gyakran máshol; 1Móz 43:14 שׁכלתי שׁכלתי כאשׁר ha meg kell fosztatnom gyermekeimtől, hát megfosztatom! a megnyugvás kifejezése, így Eszt 4:16 אבדתי אבדתי כאשׁר. A Józs 2:7 כאשׁר אחרי 'összevont' olvasat, hagyd el vagy a אחרי, vagy a כ szót. Jövő időről, 1Móz 27:40; 40:14 לך ייטב כאשׁר, Hós 7:12; Préd 4:17; Préd 5:3, és ige nélkül Ézs 23:5 למצרים שׁמע כאשׁר. — A Mik 3:3 כאשׁר egyszerűen = mint az, ami, Jób 29:25 mint az, aki. שֶׁ, továbbá ( 1Móz 6:3 [? l. 4a], Bír 5:7 (a versben kétszer); Én 1:7; Jób 19:29 [?]) שָׁ שַּׁ , a שָׁאַתָּה alakban Bír 6:17, és שְׁ a שְׁהוּא alakban Préd 2:22, שְׁהֵם 3:18 (máshol torokhang előtt שֶׁ, mint שֶׁאֲנִי Én 1:6; Préd 2:18, שֶׁאֵין Zsolt 146:3, שֶׁהֵם Én 6:5; JSir 4:9, שֶׁעַל Bír 7:12; 8:26, שֶׁרּאֹשִׁי Én 5:2), vonatkozó partikula: aki, amely, ami stb. (a késői héberben állandóan; a nerabi arámiban, Ldzb^371, 445; asszír sha; föníciai אש (rendszerint), néha ש is (Ldzb^227k.): Ges Ew^§ 181 b Ol^439. o. Sta^§ 176 e szerint a אֲשֶׁר rövidülése; valószínűbb, hogy (Sperling [l. אֲשֶׁר], Kö^ii. 323 k.) eredeti mutató partikula), a אֲשֶׁר szinonimája, de használata a késői héberre és az északi palesztinai színezetű helyekre korlátozódik, tudniillik Bír 5:7 (a versben kétszer) [אֲשֶׁר 5:27], 6:17; 7:12; 8:26; 2Kir 6:11 (l. 4c), Jón 1:7, 12; 4:10 [אֲשֶׁר11t.], Zsolt 122:3; 122:4; 123:2; 124:1; 124:2; 124:6; 129:6; 129:7; 133:2; 133:3; 135:2; 135:8; 135:10; 136:23; 137:8; 137:9; 144:15; 146:3; 146:5; JSir 2:15-16, 4:9; 5:18; Ezsd 8:20; 1Krón 5:20; 27:27; az Énekek éneke (egységesen, kivéve a címet, Én 1:1); a Prédikátor (68-szor; אֲשֶׁא89t.); továbbá (kétséges) 1Móz 6:3; 49:10 (ᵑ7 ᵑ6 ᵐ5 שֶׁלֹּה), Jób 19:29; és a מִישָׁאֵל és מְתוּשָׁאֵל tulajdonnévben (l. ott). — Használatában a שֶּׁ nagyjából a אֲשֶׁר párhuzama, tudniillik 1 névmásként: aki, amely, akit, Bír 7:12 הַיָּם שְׂפַת שֶׁעַל כַּהוֺל (vö. חוֺל c), Zsolt 122:3; 124:6 stb.; azt, akit, azt, amit stb., Én 1:7; 3:1; 1Krón 27:27; Préd 1:11; 6:3 חַיָּיו יְמֵי שֶׁיִּהְיוּ וְרַב és sok (ige) az, amennyit napjai kitesznek (Hi De és mások), 6:10; שֶּׁ הוּא az, ami 1:9 (a versben kétszer); birtokos esetben, שֶּׁ אַשְׁרֵי Zsolt 137:8; 137:9; 146:5. — A מַהשֶּּֿׁ = bármi, mi jelentéséhez a Prédikátorban l. מָה 1e b.

**37.** 

> 2 as a connecting link; = where (compare אֲשֶׁר p. 81, and 4b β), שֶּׁ מְקוֺם Eccl 1:7; 11:3 (compare אֲשֶׁר מְקוֺם Gen 39:20 +: Ges^§ 130c), whither Psa 122:4 (֗֗֗ שֶׁשָּׁם), when Song 8:8; Eccl 12:3 שֶּׁ בַּיּוֺם (compare ib. 4b a). 3as a conjunction (compare אֲשֶׁר 8); —

2 összekötő kapocsként; = ahol (vö. אֲשֶׁר 81. o., és 4b β), שֶּׁ מְקוֺם Préd 1:7; 11:3 (vö. אֲשֶׁר מְקוֺם 1Móz 39:20 és máshol: Ges^§ 130c), ahová Zsolt 122:4 (֗֗֗ שֶׁשָּׁם), amikor Én 8:8; Préd 12:3 שֶּׁ בַּיּוֺם (vö. ugyanott 4b a). 3kötőszóként (vö. אֲשֶׁר 8); —

**38.** 

> a. that, after רָאָה Eccl 2:13; 3:18, יָרַע 1:17; 2:14; 9:5; Job 19:19 (?), דִּבֶּר Eccl 2:15, אָמַר 8:14, אוֺת עָשָׂה Judg 6:17; as subject of sentence, Eccl 3:13; 5:15; also in the phrases, (a) what is ... that ? Song 5:9 (usually כִּי; see מָךְ 1d b), שֶּׁ הָיָה מֶה how comes it that ... ? Eccl 7:10; (b) Song 3:4 מֵהֶם שֶׁעָבַרְתּת כִּמְעַט hardly (was it) that (German kaum dass) I had passed, etc., Eccl 7:14 יִמְצָא שֶׁלּאֹ דִּדבְרַת עַל to the intent that ..., 5:15 שֶׁבֶּא כָּלעֻֿמַּת exactly as ..., 12:9 שֶׁ תֵר besides that, שֶּׁ עַד (ּ עַד Judg 5:7) until that Psa 123:2; Song 2:7, 17 + (see III. עַד II 1 a a and b; compare Late Hebrew Yoma 5:1), while 1:12 (ib. 2d); עָשָׂהשֶּׁ to make or cause that ..., Eccl 3:14 (compare Ezek 36:27).

a. hogy, רָאָה után Préd 2:13; 3:18, יָרַע 1:17; 2:14; 9:5; Jób 19:19 (?), דִּבֶּר Préd 2:15, אָמַר 8:14, אוֺת עָשָׂה Bír 6:17; a mondat alanyaként, Préd 3:13; 5:15; a következő kifejezésekben is: (a) mi az ..., hogy? Én 5:9 (rendszerint כִּי; l. מָךְ 1d b), שֶּׁ הָיָה מֶה hogyan van az, hogy ...? Préd 7:10; (b) Én 3:4 מֵהֶם שֶׁעָבַרְתּת כִּמְעַט alig (volt az,) hogy (német kaum dass) elhaladtam stb., Préd 7:14 יִמְצָא שֶׁלּאֹ דִּדבְרַת עַל azért, hogy ..., 5:15 שֶׁבֶּא כָּלעֻֿמַּת éppen úgy, ahogy ..., 12:9 שֶׁ תֵר azonkívül, hogy, שֶּׁ עַד (ּ עַד Bír 5:7) amíg Zsolt 123:2; Én 2:7, 17 és máshol (l. III. עַד II 1 a a és b; vö. késői héber Yoma 5:1), míg 1:12 (ugyanott 2d); עָשָׂהשֶּׁ elérni, hogy ..., Préd 3:14 (vö. Ez 36:27).

**39.** 

> b. involving a reason (compare אֲשֶׁר 8c), because, since, Song 1:6 (twice in verse); 5:2; Eccl 2:18 b. Hence שֵׁלָּמָה Song 1:7 since why ? = lest (see מָה 4d b).

b. okot foglal magában (vö. אֲשֶׁר 8c): mert, mivel, Én 1:6 (a versben kétszer); 5:2; Préd 2:18 b. Innen שֵׁלָּמָה Én 1:7 mivel miért? = nehogy (l. מָה 4d b).

**40.** 

> 4 compounds:

4 összetételek:

**41.** 

> a. בְּשֶּׁ , i. q. בַּאֲשֶׁר c (p. 84a) in that, seeing that, Eccl 2:16; also (according to ᵑ6 ᵐ5 ᵑ0 Hu De) Gen 6:3 בָשָׂר הוּא בְּשַׁגַּם because that he also is flesh; but see שָׁגַג.

a. בְּשֶּׁ , i. q. בַּאֲשֶׁר c (84a. o.) azáltal hogy, mivel, Préd 2:16; továbbá (ᵑ6 ᵐ5 ᵑ0 Hu De szerint) 1Móz 6:3 בָשָׂר הוּא בְּשַׁגַּם mivelhogy ő is test; de l. שָׁגַג.

**42.** 

> b. כּשֶּׁ , i. q. כַּאֲשֶׁר p. 455: — (a) according as Eccl 5:14; 12:7; (b) when (so often in Late Hebrew, as Ab 1:8 (3 t. in verse); 1:14) 9:12; 10:3.

b. כּשֶּׁ , i. q. כַּאֲשֶׁר 455. o.: — (a) aszerint, ahogy Préd 5:14; 12:7; (b) amikor (így gyakran a késői héberben, mint Ab 1:8 (a versben 3-szor); 1:14) 9:12; 10:3.

**43.** 

> c. מִשֶּּׁ , i. q. מֵאֲשֶׁר a (p. 84:a), 2Kin 6:12 מִשֶּׁלָּנוּ מִי who of those that are ours ? (but Klo Kmp^Kau Benz מְגַלֵּנוּ who betrays us ? compare ᵐ5); Eccl 5:4 than that (compare מֵאֲשֶׁר 3:22), + 2:24 (read מִשֶּׁיּאֹכַל with Ew De, etc.; compare 3:22).

c. מִשֶּּׁ , i. q. מֵאֲשֶׁר a (84:a. o.), 2Kir 6:12 מִשֶּׁלָּנוּ מִי ki azok közül, akik a mieink? (de Klo Kmp^Kau Benz מְגַלֵּנוּ ki árul el minket? vö. ᵐ5); Préd 5:4 mint az, hogy (vö. מֵאֲשֶׁר 3:22), és 2:24 (olv. מִשֶּׁיּאֹכַל Ew De stb. szerint; vö. 3:22).

**44.** 

> d. שֶׁל, like אֲשֶׁרלְ (אֲשֶׁר 7b), a mark of the Genitive: thrice, adding slight emphasis to the suffix, Song 1:6 = 8:12 שֶׁלִּי כַּרְמִי my vineyard (literally my vineyard, which is mine), 3:7 שֶׁלִּשְׁלֹמֹה מִטָּתוֺ (so often in Late Hebrew, but without any special emphasis, as Aboth 1:12 שׁלאֿהרן מתלמידיווּ הֲוֵי be of Aaron's disciples, 2:1 שֶׁלמִֿצְוֺת שְׂכָרָן, 2:2; 3:2 שׁלמֿלכות בשׁלומהּ מתפלל הֲוֵי; compare in Syriac, as Luke 6:42 my words, Nö^§ 225). And with בְּשֶׁל בְּ, literally through that which belongs to or concerns, pleonastic for on account of (a late, unidiomatic translation of Aramaic בְּרִיל, from דִּי בְּ,, and לְ, as in Onk Gen 12:13 בדילי on my account, 30:27; 39:5 מָא בְּדִיל יוֺסֵף, בְּדִיל on account of what ? Judg 8:1; 2Sam 9:1; 1Kin 11:12, 39, etc.), Jonah 1:7 בְּשֶׁלְּמִי on account of whom ? (|| 1:8 לְמִי בַּאֲשֶׁר; probably a gloss), 1:12 בְּשֶׁלִּי an account of me (בְּדִילִי מַן, בְּדִיל ᵑ7); Eccl 8:17 לְבַקֵּשׁ הָאָדָם יַעֲמֹל אֲשֶׁר בְּשֶׁל on account of (the fact) that (= seeing that) man labours, etc. (unidiomatic translation of Aramaic דְּ בְּדִיל because that, as Gen 6:3 בִּסְרָא דְּאִינוּן בְּדִיל, 39:9 אִיתְּתֵיהּ דְּאַתְּ בְּרִיל [for Hebrew אִשְׁתּוֺ אַתְּ בַּאֲשֶׁר]; Palmyrene די בדיל Ldzb^233, — in Tariff 1:4 (Cooke^N. Semitic Inscr. 320) = ἐπειδή). [שֹׁא] see [ שׁוֺא].

d. שֶׁל, mint a אֲשֶׁרלְ (אֲשֶׁר 7b), a birtokos eset jele: háromszor, enyhe nyomatékot adva a suffixummal jelölt birtokosnak, Én 1:6 = 8:12 שֶׁלִּי כַּרְמִי az én szőlőm (szó szerint: az én szőlőm, amely az enyém), 3:7 שֶׁלִּשְׁלֹמֹה מִטָּתוֺ (így gyakran a késői héberben, de különösebb nyomaték nélkül, mint Aboth 1:12 שׁלאֿהרן מתלמידיווּ הֲוֵי légy Áron tanítványai közül való, 2:1 שֶׁלמִֿצְוֺת שְׂכָרָן, 2:2; 3:2 שׁלמֿלכות בשׁלומהּ מתפלל הֲוֵי; vö. a szírben, mint Luk 6:42 az én szavaim, Nö^§ 225). A בְּשֶׁל בְּ kapcsolatban pedig, szó szerint: azáltal, ami valakihez tartozik vagy valakit illet, pleonasztikusan = valami miatt (az arámi בְּרִיל késői, nem idiomatikus fordítása, amely a דִּי בְּ,, és a לְ szóból áll, mint Onk 1Móz 12:13 בדילי miattam, 30:27; 39:5 מָא בְּדִיל יוֺסֵף, בְּדִיל mi miatt? Bír 8:1; 2Sám 9:1; 1Kir 11:12, 39 stb.), Jón 1:7 בְּשֶׁלְּמִי ki miatt? (|| 1:8 לְמִי בַּאֲשֶׁר; valószínűleg glossza), 1:12 בְּשֶׁלִּי miattam (בְּדִילִי מַן, בְּדִיל ᵑ7); Préd 8:17 לְבַקֵּשׁ הָאָדָם יַעֲמֹל אֲשֶׁר בְּשֶׁל amiatt (a tény miatt), hogy (= mivel) az ember fáradozik stb. (az arámi דְּ בְּדִיל mivelhogy nem idiomatikus fordítása, mint 1Móz 6:3 בִּסְרָא דְּאִינוּן בְּדִיל, 39:9 אִיתְּתֵיהּ דְּאַתְּ בְּרִיל [a héber אִשְׁתּוֺ אַתְּ בַּאֲשֶׁר helyett]; palmürai די בדיל Ldzb^233, — a Tariff 1:4-ben (Cooke^N. Semitic Inscr. 320) = ἐπειδή). [שֹׁא] l. [ שׁוֺא].

#### H9005 (45414 → 47276 karakter)

`forras_hash=f87cf55ff84a4186ea2b80f5bc01dfc40bddb026` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v3`

**1.** 

> ל ל, twelfth letter; used as numeral 30 in Post-Biblical Hebrew לְ preposition to, for, in regard to (Moabite, Phoenician ל, Aramaic לְ, Arabic Ethiopic Assyrian la in lapân = לִפְנֵי, Dl^HWB 530), before tone-syllables usually לָ (Kö^ii. 276 f.); with suffix לִי; לְכָה לְךָ, Gen 27:37; 2Sam 18:22; Isa 3:6, לָ֑ךְ; feminine לֵכִי לָךְ, 2Kin 4:2; Song 2:13 Kt (probably North Palestinian dialect : compare Syriac ); לוֺ (15 t., according to Masoretes, written incorrectly לֹא: see לֹא note); לָהּ; לָהֿ Num 32:42; Zech 5:11; Ruth 2:14; לָ֫נוּ; לָכֶ֫נָה לָכֶם Ezek 13:18 (לָכֶן does not occur); לָהֶם, in poetry לָ֫מוֺ (55 t., including a few cases where, according to many, it stands for לוֺ: compare Ges^§ 103. 2a, n. Di^Isa 44:15. 53, 8), [also לָהֵ֫מָּה Jer 14:16]; לָהֶן [ לָהֵן (q. v.) Ruth 1:13 (twice in verse), לָהֵ֫נָּה5t., see הֵמָּה]. Preposition denoting direction (not properly motion, as אֶל) towards, or reference to; and hence used in many varied applications, in some of which the idea of direction predominates, in others that of reference (compare Gies^Die Präp. Lamed, 1876): —

ל ל, a tizenkettedik betű; a Biblia utáni héberben a 30-as szám jele לְ elöljárószó: -hoz, -hez, -höz, -nak, -nek, valamire nézve (moábi, föníciai ל, arámi לְ, arab etióp asszír la a lapân = לִפְנֵי szóban, Dl^HWB 530), hangsúlyos szótag előtt rendszerint לָ (Kö^ii. 276 k.); suffixummal לִי; לְכָה לְךָ, 1Móz 27:37; 2Sám 18:22; Ézs 3:6, לָ֑ךְ; nőnemű לֵכִי לָךְ, 2Kir 4:2; Én 2:13 Kt (valószínűleg északi palesztinai nyelvjárás: vö. szír ); לוֺ (15-ször, a maszoréták szerint helytelenül לֹא alakban írva: l. לֹא jegyzet); לָהּ; לָהֿ 4Móz 32:42; Zak 5:11; Ruth 2:14; לָ֫נוּ; לָכֶ֫נָה לָכֶם Ez 13:18 (לָכֶן nem fordul elő); לָהֶם, költészetben לָ֫מוֺ (55-ször, beleértve néhány olyan esetet, ahol sokak szerint לוֺ helyett áll: vö. Ges^§ 103. 2a, n. Di^Ézs 44:15. 53, 8), [továbbá לָהֵ֫מָּה Jer 14:16]; לָהֶן [ לָהֵן (l. ott) Ruth 1:13 (a versben kétszer), לָהֵ֫נָּה5t., l. הֵמָּה]. Elöljárószó, amely valami felé irányulást (tulajdonképpen nem mozgást, mint a אֶל) vagy valamire való vonatkozást jelöl; ennélfogva sokféle alkalmazásban használatos, amelyek közül némelyikben az irány, másokban a vonatkozás gondolata uralkodik (vö. Gies^Die Präp. Lamed, 1876): —

**2.** 

> 1 very often, with various classes of verbs, to, towards, for: namely a. verbs of looking, listening, attending, waiting, etc., as כלה נכסף, הוחיל, יחל, התחֹלל, האמין, (Psa 84:3 + ), שׁמע הקשׁיב, קִוָּה, (נטה, נתן הכין, לב, שׁת) הטה, אזן, (sometimes), צמא to thirst for (Exod 17:3; Psa 42:3), השׁתחוה (to Gen 37:10, towards Psa 99:5); sometimes also with נשׂא נפשׁ, ראה, נִבַּט, הביט, האזין, (see these verbs; many are also construed with other prepositions); Isa 51:6; Psa 44:21; pregnantly Isa 38:14; ל השׁתאה Gen 24:21, החרישׁל Num 30:5; 30:8: sometimes without a verb, as Judg 5:9 לְ לִבִּי, Jer 5:3 ל עיניך, Psa 33:18 (|| אל), 39:8 היא לך תוחלתי, 120:7 למלחמה המה, 130:6 לאדני נפשׁי (compare Isa 26:8), Psa 143:6; Dan 11:27; 2Chr 3:13; 32:2.

1 igen gyakran különféle igecsoportokkal: -hoz, felé, -ért: tudniillik a. a nézés, hallgatás, figyelés, várakozás stb. igéivel, mint כלה נכסף, הוחיל, יחל, התחֹלל, האמין, (Zsolt 84:3 és máshol), שׁמע הקשׁיב, קִוָּה, (נטה, נתן הכין, לב, שׁת) הטה, אזן, (néha), צמא szomjazni valamire (2Móz 17:3; Zsolt 42:3), השׁתחוה (valakihez 1Móz 37:10, valami felé Zsolt 99:5); néha נשׂא נפשׁ, ראה, נִבַּט, הביט, האזין igékkel is (l. ezeket az igéket; sokat más elöljárószóval is szerkesztenek); Ézs 51:6; Zsolt 44:21; praegnans értelemben Ézs 38:14; ל השׁתאה 1Móz 24:21, החרישׁל 4Móz 30:5; 30:8: néha ige nélkül, mint Bír 5:9 לְ לִבִּי, Jer 5:3 ל עיניך, Zsolt 33:18 (|| אל), 39:8 היא לך תוחלתי, 120:7 למלחמה המה, 130:6 לאדני נפשׁי (vö. Ézs 26:8), Zsolt 143:6; Dán 11:27; 2Krón 3:13; 32:2.

**3.** 

> b. with verbs of saying, calling, singing, vowing, sacrificing, etc., as דבר אמר, (chiefly with God as subject = promise, Gen 24:7; 1 Kings 5:26 +, especially in D לְ דבר כאשׁר Deut 1:11 (see Dr), 1:21 etc.; with human subject Gen 49:28; Judg 14:7; 1Kin 2:19 and elsewhere (Gie^42f.: אל דבר is more common), יד נשׂא נדר, הגיד, הודה, זמּר, זבח, (in oath) Ezek 20:5-6, 23; Psa 106:26, שָׁר נשׁבע, הריע, קִטֵר, etc.

b. a mondás, hívás, éneklés, fogadás, áldozás stb. igéivel, mint דבר אמר, (főként Istennel mint alannyal = megígérni, 1Móz 24:7; 1Kir 5:26 és máshol, különösen D-ben לְ דבר כאשׁר 5Móz 1:11 (l. Dr), 1:21 stb.; emberi alannyal 1Móz 49:28; Bír 14:7; 1Kir 2:19 és máshol (Gie^42k.: a אל דבר gyakoribb), יד נשׂא נדר, הגיד, הודה, זמּר, זבח, (esküben) Ez 20:5-6, 23; Zsolt 106:26, שָׁר נשׁבע, הריע, קִטֵר stb.

**4.** 

> c. with verbs of giving, leaving, bringing, offering etc., as הִמִּיל הביא, allot (Josh 13:6), עזב הסגיר, נתן, Psa 16:9 abandon to Sheol Isa 18:6, הקריבּ Lev 17:4, שׁוב = to be returned Deut 28:31, השׁיב = bring back 22:1, = requite 2Sam 16:12, שִׁלַּח, etc.

c. az adás, hagyás, hozás, felajánlás stb. igéivel, mint הִמִּיל הביא, kiosztani (Józs 13:6), עזב הסגיר, נתן, Zsolt 16:9 a Seolnak átengedni Ézs 18:6, הקריבּ 3Móz 17:4, שׁוב = visszaadatni 5Móz 28:31, השׁיב = visszavinni 22:1, = megfizetni 2Sám 16:12, שִׁלַּח stb.

**5.** 

> d. with verbs of dealing, acting towards (whether with friendly or hostile intent), as ל עשׂה Gen 19:8 + often, ל גמל Isa 3:9; so with חָטָא הֵמַר, הֵרַע, הֵייטִב, to sin against (Gen 20:9 +), אָשָׁם to be guilty towards (Lev 5:19), כִּחֵשׁ שַׁקֵּר, to lie to, כִּזֵּב; with verbs of mocking or laughing against, at, as לְ לעג Psa 2:4, לְ שׂחק 37:13, לְ שׂמח to rejoice over 35:19; Ezek 35:15, causative לְ שִׂמַּח Psa 30:2, לְ עלץ 25:2: with other verbs denoting hostility (less common than ב or על), Gen 27:42 להרגך לך מתנחם, 2Kin 5:7; Exod 11:7 (so Josh 10:21: compare Job 16:9), Jer 25:31; 50:9; Psa 7:14; 37:12; 56:3; 106:16 לְ קנא (usually In good sense, 5g c)Job 20:27; 34:37. And with adjectives, as Psa 73:1 ל טוב good to, Gen 13:13 לי וְחַטָּאִים ׳רָעִים towards ׳י 2Sam 22:24 לוֺ תָּמִים (|| Psa 18:24 עִמּוֺ), 89:29 לוֺ נֶאֱמֶנֶת; with substantive (rare) Exod 32:12; Lam 3:60 (synonym V:61 על).

d. a valakivel való bánásmód, a valaki iránti cselekvés igéivel (akár baráti, akár ellenséges szándékkal), mint ל עשׂה 1Móz 19:8 és gyakran máshol, ל גמל Ézs 3:9; így חָטָא הֵמַר, הֵרַע, הֵייטִב igékkel: vétkezni valaki ellen (1Móz 20:9 és máshol), אָשָׁם vétkesnek lenni valaki iránt (3Móz 5:19), כִּחֵשׁ שַׁקֵּר, hazudni valakinek, כִּזֵּב; a gúnyolódás vagy nevetés igéivel: valaki ellen, valakin, mint לְ לעג Zsolt 2:4, לְ שׂחק 37:13, לְ שׂמח örvendezni valakinek a kárán 35:19; Ez 35:15, kauzatív לְ שִׂמַּח Zsolt 30:2, לְ עלץ 25:2: más, ellenségeskedést jelentő igékkel (ritkábban, mint ב vagy על), 1Móz 27:42 להרגך לך מתנחם, 2Kir 5:7; 2Móz 11:7 (így Józs 10:21: vö. Jób 16:9), Jer 25:31; 50:9; Zsolt 7:14; 37:12; 56:3; 106:16 לְ קנא (rendszerint jó értelemben, 5g c) Jób 20:27; 34:37. Melléknevekkel is, mint Zsolt 73:1 ל טוב jó valakihez, 1Móz 13:13 לי וְחַטָּאִים ׳רָעִים valaki iránt ׳י 2Sám 22:24 לוֺ תָּמִים (|| Zsolt 18:24 עִמּוֺ), 89:29 לוֺ נֶאֱמֶנֶת; főnévvel (ritka) 2Móz 32:12; JSir 3:60 (szinonimája V:61 על).

**6.** 

> e. with words denoting what is pleasurable or the reverse, as לְ נעם 2Sam 1:26, ל ערב Hosea 9:4, לְ יֵמַר Isa 24:7, לְ טוֺב (adjective) 1Sam 1:8, לְ נָקֵל 2Kin 20:10, also ל סכן ל הועיל to be profitable to; and with neuter verbs, to denote the subject of a sensation or emotion, as לְ טוֺב to be well to (with), Deut 5:30; 19:13 +, לְ מַר Ruth 1:13, לְ צַר 1Sam 13:6 + often, לְ כְּרֹב Hosea 10:1, לְ רָוַח 1Sam 16:23, לְ חַם to be warm to, 1Kin 1:1, לְ רַע Psa 106:32, לְ חָרָה it was hot (= anger arose) to Gen 4:6 + often, לְ חָֽשְׁכָה Micah 3:6. And with passive Vbs., לוֺ נִסְלַח it is forgiven to him = he is forgiven Lev 4:26 + often; otherwise rare, לְ נִרְצָה 1:4, לָנוּ נִרְמָּא it is healed to us = we are healed Isa 53:5, ל הוּנַח Lam 5:5, לְ יְבֻלַּע 2Sam 17:16 (see Dr).

e. a kellemest vagy ellenkezőjét jelentő szavakkal, mint לְ נעם 2Sám 1:26, ל ערב Hós 9:4, לְ יֵמַר Ézs 24:7, לְ טוֺב (melléknév) 1Sám 1:8, לְ נָקֵל 2Kir 20:10, továbbá ל סכן ל הועיל hasznára lenni valakinek; és tárgyatlan igékkel, az érzet vagy érzelem alanyának jelölésére, mint לְ טוֺב jól lenni valakinek (valakivel), 5Móz 5:30; 19:13 és máshol, לְ מַר Ruth 1:13, לְ צַר 1Sám 13:6 és gyakran máshol, לְ כְּרֹב Hós 10:1, לְ רָוַח 1Sám 16:23, לְ חַם melege lenni valakinek, 1Kir 1:1, לְ רַע Zsolt 106:32, לְ חָרָה forró lett (= harag gerjedt) valakinek 1Móz 4:6 és gyakran máshol, לְ חָֽשְׁכָה Mik 3:6. Szenvedő igékkel is, לוֺ נִסְלַח megbocsáttatik neki = bocsánatot nyer 3Móz 4:26 és gyakran máshol; egyébként ritka, לְ נִרְצָה 1:4, לָנוּ נִרְמָּא gyógyulás lett nekünk = meggyógyultunk Ézs 53:5, ל הוּנַח JSir 5:5, לְ יְבֻלַּע 2Sám 17:16 (l. Dr).

**7.** 

> f. with verbs of reaching to, touching, attaching etc., as ל אסר to bind to, דבק חבשׁ, Psa 44:26, מצא to reach to Isa 10:10, 14; Psa 21:9, הגיע Exod 4:25, נצמד Num 25:5, קרוב (adjective) Ruth 2:20; out of connection with a verb (almost = עַד), Josh 16:1; Psa 59:14; Job 28:3; Neh 3:15; 2Chr 33:14, and correl. to מִן (see מִן 5).

f. a valamihez érés, érintés, kapcsolás stb. igéivel, mint ל אסר valamihez kötni, דבק חבשׁ, Zsolt 44:26, מצא valameddig elérni Ézs 10:10, 14; Zsolt 21:9, הגיע 2Móz 4:25, נצמד 4Móz 25:5, קרוב (melléknév) Ruth 2:20; igétől függetlenül (szinte = עַד), Józs 16:1; Zsolt 59:14; Jób 28:3; Neh 3:15; 2Krón 33:14, és a מִן korrelatívumaként (l. מִן 5).

**8.** 

> g. with verbs of motion,as שָׁב בא הלך, etc. (not so common as אל, or the simple accusative with or without ה locative) — (a) with places, rare in early prose, Josh 1:15; 8:14; Judg 1:34; 20:10 (but see GFM), 1Sam 9:12; 20:25; 2Kin 3:27, except in particular phrases, namely למקומו Gen 18:33, לדרכו 32:2, לאהליו 1Sam 4:10 (also with other suffixes: all these + often, especially with שׂוב and הלך, or preceded by distributive לאהליו(ךׅ אישׁ, also, without verb, as exclamation, 2Sam 20:1; 1Kin 12:16), לארצו Gen 30:25+, לִירֻשָּׁתוֺ אִישׁ Deut 3:20, לנחלתו אישׁ Josh 24:28 +, לעירו אישׁ 1Sam 8:22; Neh 13:10: often In late Hebrew, as Job 4:5; 1Chr 4:39, 42; 5:26; 12:1; 12:9; 22:18; 24:19; 2Chr 1:3; 8:17 + often Chronicles, Ezra 2:68 +, Neh 10:35ff.; Est 6:4; Psa 96:8; 132:7; 146:4: לירושׁלם Jer 3:17b (omitted by ᵐ5), Zech 1:16, and often Chronicles Ezra Nehemiah (as 2Chr 11:14; 19:1; 30:3, 11), לשׁמרון18:2; 28:8-9, לבבל Jer 51:2; Ezra 2:1; 1Chr 9:1; 2Chr 36:7 (but earlier always בבל שׁמרון, ירושׁלם, or בבלה); and in poetry Judg 5:11; Isa 22:1; 23:17; 49:18; 51:14 (pregnantly) לשׁחת ימות, 59:20; 60:4-5, 7; 65:12; Jer 31:17; 48:15; 50:27; Micah 1:12; Zech 9:12; Psa 7:8; 68:19; 74:3; Song 4:16; 5:1; 6:2; 7:13 לכרמים נשׁכימה, Job 10:19; 20:6; לְ הוציא Psa 18:20; 66:12, לאור Micah 7:9; Job 12:22. ל יוּבַל Hosea 10:6 + : without a verb, Isa 23:5; Hosea 7:12. Also לָאָרֶץ, with many verbs, both in sense down to the earth, Isa 14:12; 21:9; 28:2; Amos 3:14; 5:7; Ezek 26:11; Psa 7:6 +, with חִלֵּל (pregnantly) 74:7; 89:40, and idiomatically with ישׁב to sit on the earth, Isa 3:26; 47:1; Job 2:13 +, without verb Isa 26:9: so לֶעָפָר Job 7:21; Psa 7:6, לשׁחת הוריד Ezek 28:8. (b) with persons, not very common, Deut 32:35; Isa 31:6; 57:9; Jer 3:22 לָ֑ךְ אָתָנוּ, Psa 45:15; 119:79; Job 18:14; 1Chr 12:16; Neh 6:19, לְעַמִּי Num 24:14; Ruth 1:10: לְ בא, especially with pronoun לָהּ לְךָ, etc. (friendly) 2Sam 12:4; Zech 9:9; Amos 6:1, (hostile) 2Sam 5:23; Jer 46:22; 49:9; 50:26; 51:48, 53; with athing as subject Deut 33:16 (לראשׁ), 2Sam 24:13; Isa 47:9; Job 3:25 (compare Isa 66:4), Jer 4:12; Jeremiah 22:33 חֲבָלִים לָךְ בְּבאֹ (so Hosea 13:13; Isa 66:7). And with verbs of placing (where עַל would be more usually) Psa 21:4 מָּז עֲטֶרֶת לְראֹשׁוֺ תָּשִׁית, 22:16; 66:12, with לְכִסֵּא 9:5; 132:11; 132:12; Job 36:7: compare הִשְׁתַּחֲוָה לְאַמָּיוּ, נָפַל, Gen 48:12 + (also א ׳עַל).

g. mozgást jelentő igékkel, mint שָׁב בא הלך stb. (nem olyan gyakori, mint a אל vagy az egyszerű tárgyeset helyhatározói ה raggal vagy anélkül) — (a) helyekkel, a korai prózában ritka, Józs 1:15; 8:14; Bír 1:34; 20:10 (de l. GFM), 1Sám 9:12; 20:25; 2Kir 3:27, kivéve bizonyos kifejezéseket, tudniillik למקומו 1Móz 18:33, לדרכו 32:2, לאהליו 1Sám 4:10 (más suffixumokkal is: mindezek gyakran, különösen שׂוב és הלך igével, vagy disztributív לאהליו előzi meg(ךׅ אישׁ, továbbá ige nélkül, felkiáltásként, 2Sám 20:1; 1Kir 12:16), לארצו 1Móz 30:25 és máshol, לִירֻשָּׁתוֺ אִישׁ 5Móz 3:20, לנחלתו אישׁ Józs 24:28 és máshol, לעירו אישׁ 1Sám 8:22; Neh 13:10: a késői héberben gyakran, mint Jób 4:5; 1Krón 4:39, 42; 5:26; 12:1; 12:9; 22:18; 24:19; 2Krón 1:3; 8:17 és gyakran a Krónikákban, Ezsd 2:68 és máshol, Neh 10:35kk.; Eszt 6:4; Zsolt 96:8; 132:7; 146:4: לירושׁלם Jer 3:17b (ᵐ5 kihagyja), Zak 1:16, és gyakran a Krónikákban, Ezsdrásnál, Nehémiásnál (mint 2Krón 11:14; 19:1; 30:3, 11), לשׁמרון18:2; 28:8-9, לבבל Jer 51:2; Ezsd 2:1; 1Krón 9:1; 2Krón 36:7 (de korábban mindig בבל שׁמרון, ירושׁלם vagy בבלה); a költészetben pedig Bír 5:11; Ézs 22:1; 23:17; 49:18; 51:14 (praegnans értelemben) לשׁחת ימות, 59:20; 60:4-5, 7; 65:12; Jer 31:17; 48:15; 50:27; Mik 1:12; Zak 9:12; Zsolt 7:8; 68:19; 74:3; Én 4:16; 5:1; 6:2; 7:13 לכרמים נשׁכימה, Jób 10:19; 20:6; לְ הוציא Zsolt 18:20; 66:12, לאור Mik 7:9; Jób 12:22. ל יוּבַל Hós 10:6 és máshol: ige nélkül, Ézs 23:5; Hós 7:12. Továbbá לָאָרֶץ sok igével, egyrészt a földre le értelemben, Ézs 14:12; 21:9; 28:2; Ámós 3:14; 5:7; Ez 26:11; Zsolt 7:6 és máshol, חִלֵּל igével (praegnans értelemben) 74:7; 89:40, másrészt idiomatikusan ישׁב igével: a földön ülni, Ézs 3:26; 47:1; Jób 2:13 és máshol, ige nélkül Ézs 26:9: így לֶעָפָר Jób 7:21; Zsolt 7:6, לשׁחת הוריד Ez 28:8. (b) személyekkel, nem nagyon gyakori, 5Móz 32:35; Ézs 31:6; 57:9; Jer 3:22 לָ֑ךְ אָתָנוּ, Zsolt 45:15; 119:79; Jób 18:14; 1Krón 12:16; Neh 6:19, לְעַמִּי 4Móz 24:14; Ruth 1:10: לְ בא, különösen לָהּ לְךָ stb. névmással (baráti értelemben) 2Sám 12:4; Zak 9:9; Ámós 6:1, (ellenséges értelemben) 2Sám 5:23; Jer 46:22; 49:9; 50:26; 51:48, 53; dologgal mint alannyal 5Móz 33:16 (לראשׁ), 2Sám 24:13; Ézs 47:9; Jób 3:25 (vö. Ézs 66:4), Jer 4:12; Jer 22:33 חֲבָלִים לָךְ בְּבאֹ (így Hós 13:13; Ézs 66:7). Továbbá a helyezés igéivel (ahol a עַל volna szokásosabb) Zsolt 21:4 מָּז עֲטֶרֶת לְראֹשׁוֺ תָּשִׁית, 22:16; 66:12, לְכִסֵּא igével 9:5; 132:11; 132:12; Jób 36:7: vö. הִשְׁתַּחֲוָה לְאַמָּיוּ, נָפַל, 1Móz 48:12 és máshol (továbbá א ׳עַל).

**9.** 

> h. expressing direction towards (without contact), לאחור backwards Jer 7:24, לַחוּץ outwards Psa 41:7, למעלה upwards, למטה downwards; to scatter רוח לכל Jer 49:32 compare 49:36; Ezek 5:10 +, (רוחות לארבע שׁמים 42:20; Dan 8:8; 11:4; 1Chr 9:24: of the points of the compass (without verb) ֗֗֗ לִפְאַת towards the quarter of (the north, south, etc.) Exod 26:18 + often P (so Ezek 47:15), למזרח לדרום etc. (late: earlier ממזרח, or מזרחה etc.) 40:23; 41:11, 14; 42:4; Neh 3:26; 1Chr 5:9; 6:63; 7:28; 12:15; 26:16-18 2Chr 31:14, למדבר20:24; also (peculiarly) 1Sam 14:40; 1Kin 20:38; 2Kin 11:11.

h. valami felé irányulást kifejezve (érintkezés nélkül), לאחור hátrafelé Jer 7:24, לַחוּץ kifelé Zsolt 41:7, למעלה felfelé, למטה lefelé; szétszórni רוח לכל Jer 49:32, vö. 49:36; Ez 5:10 és máshol, (רוחות לארבע שׁמים 42:20; Dán 8:8; 11:4; 1Krón 9:24: az égtájakról (ige nélkül) ֗֗֗ לִפְאַת valaminek (az északi, déli stb.) oldala felé 2Móz 26:18 és gyakran P-ben (így Ez 47:15), למזרח לדרום stb. (késői; korábban ממזרח vagy מזרחה stb.) 40:23; 41:11, 14; 42:4; Neh 3:26; 1Krón 5:9; 6:63; 7:28; 12:15; 26:16-18 2Krón 31:14, למדבר20:24; továbbá (sajátosan) 1Sám 14:40; 1Kir 20:38; 2Kir 11:11.

**10.** 

> i. expressing addition (rare); Isa 28:10, 13 לָקַו קַו לָצַו צַו, 56:8 (resuming על), Eccl 7:27 לאחת אחת (adding) one to another, Ezra 8:24; Neh 11:17 (על is more usual in this sense). 2 Expressing locality, at, near, idiomatic in the phrases לִפְנֵי = before (sometimes after verbs of motion, as 1Kin 1:23, but very often otherwise), לְעֵינֵי in the sight of, לִשְׂמאֹל לִימִין, לְיַד, (only Eccl 10:2), לפתח at the entrance (of), Gen 4:7; Num 11:10 +; in other, rarer connections, 20:24 ֗֗֗ לְמֵי (usually על), Judg 5:16 (|| 5:15 ב), לְחוֺף Gen 49:13 (twice in verse); Judg 5:17, לְפִי Psa 141:7; Prov 8:3; Hosea 5:1 לְמִצְמָּה, 2Chr 35:15. לִפְנִימָה = within, 1Kin 6:30; Ezek 40:16. 3 To denote the object of a verb —

i. hozzáadást kifejezve (ritka); Ézs 28:10, 13 לָקַו קַו לָצַו צַו, 56:8 (a על szót folytatva), Préd 7:27 לאחת אחת (hozzáadva) egyiket a másikhoz, Ezsd 8:24; Neh 11:17 (ebben az értelemben a על szokásosabb). 2 Helyet kifejezve: -nál, -nél, közel, idiomatikusan a következő kifejezésekben: לִפְנֵי = előtt (néha mozgást jelentő igék után, mint 1Kir 1:23, de igen gyakran másként), לְעֵינֵי valaki szeme láttára, לִשְׂמאֹל לִימִין, לְיַד, (csak Préd 10:2), לפתח (valaminek) a bejáratánál, 1Móz 4:7; 4Móz 11:10 és máshol; más, ritkább kapcsolatokban, 20:24 ֗֗֗ לְמֵי (rendszerint על), Bír 5:16 (|| 5:15 ב), לְחוֺף 1Móz 49:13 (a versben kétszer); Bír 5:17, לְפִי Zsolt 141:7; Péld 8:3; Hós 5:1 לְמִצְמָּה, 2Krón 35:15. לִפְנִימָה = belül, 1Kir 6:30; Ez 40:16. 3 Az ige tárgyának jelölésére —

**11.** 

> a. with the Hiph`il, mostly of intransitive verbs, properly (as it seems) a dativus commodi [dative of benefit], as לְ הֵנִיחַ to give rest to, הִרְחִיב to give width to, לְ הֵצִיק לְ, הֵצַר, exceptionally also with other words, as הִצְדִּיק הוֺכִיחַ, הִרְגִּיוּ, to give righteousness to, Isa 53:11, הֶחֱיָה Gen 45:7, הֵבִין give understanding to (late), הִצְלִיחַ (do.), הִרְבָּה Hosea 10:1, הִשְׂגִּיא Job 12:23, הִפְתָּה Gen 9:27 give breadth to.

a. Hiph`illel, többnyire tárgyatlan igékével, tulajdonképpen (úgy látszik) dativus commodi [érdekeltségi részes eset], mint לְ הֵנִיחַ nyugalmat adni valakinek, הִרְחִיב tágasságot adni valakinek, לְ הֵצִיק לְ, הֵצַר, kivételesen más szavakkal is, mint הִצְדִּיק הוֺכִיחַ, הִרְגִּיוּ, igazságot szerezni valakinek, Ézs 53:11, הֶחֱיָה 1Móz 45:7, הֵבִין értelmet adni valakinek (késői), הִצְלִיחַ (ua.), הִרְבָּה Hós 10:1, הִשְׂגִּיא Jób 12:23, הִפְתָּה 1Móz 9:27 tágasságot adni valakinek.

**12.** 

> b. with other verbs, sporadically early (if the text be sound), but mostly late, in conseq. of Aramaic influence (in Aramaic the accusative being constantly denoted by ל), as אהב Lev 19:18, 34; 2Chr 19:2, הרג 2Sam 3:30; Job 5:2, בוּז (mostly), בזה 2Sam 6:16, sometimes also זכר to remember, עבד to serve (work or do service for), עזר (8:5, and especially late), דרשׁ (especially Chronicles), הִלֵּל (only Chronicles Ezra), רפא (probably the dativus commodi [dative of benefit]), שִׂחֵת 1Sam 23:10; Num 32:15, נִדָּה Amos 6:3, גִּדֵּל Psa 34:4, מִּתַּח 116:16, כִּבֵּד 86:9; Dan 11:38, חִזַּק 1Chr 26:27; 29:12, בֵּרַךְ 29:20; Neh 11:2, חֵרֵף2Chr 32:17; see also 1Sam 22:7; 2Kin 8:6; Jer 16:6; 40:2; Jonah 4:6; Psa 69:6; 73:18; 135:11; 136:19; 136:20; Prov 17:26; Job 12:23b Lam 4:5; 1Chr 16:37; 18:6 (הושׁיע, altered from 2Sam 8:6: so Psa 116:6), 1Chr 25:1; 29:22 (twice in verse); 2Chr 5:11; 6:42; 17:7; 24:5; 34:13 (usually על), Ezra 8:16; at the end of an enumeration, 1Chr 28:1b; 2Chr 24:12b; 26:14b; 28:23; marking the definite object in apposition, 1Chr 29:18; 2Chr 2:12; 23:1; Psa 135:11; 136:19; 136:20 ( = earlier את, Gen 26:34; Judg 3:15; Isa 7:6; 8:2); after a suffix (in Syriac fashion), 1Chr 5:26 ל ׳וַיַּגְלֵם, 23:6; 2Chr 25:5, 10; 28:15, compare Neh 9:32; defining anomalously the suffix of a noun, Num 29:18, 21, 24 etc. 1Chr 7:5 לַכֹּל הִתְיַחֲשָׂם, 2Chr 31:16, 18; Ezra 9:1; 10:14. (But in sentences of the type לְנַפְשִׁי דּוֺרֵשׁ אֵין Psa 142:5; b 72:12; Isa 51:18; Jer 14:16; 49:5; Lam 1:7, 9, 17, 21, the ל belongs probably to ׃אין compare the || types מַכִּיר לִי אֵין Psa 142:5 a Deut 28:31; Jer 50:32; Lam 1:2, לָהּ אֵין דֹּרֵשׁ Jer 30:17; Lam 4:4.) compare Ges^§ 117n. 4 Into (εἰς), of a transition into a new state or condition, or into a new character or office: —

b. más igékkel, szórványosan korán (ha a szöveg ép), de többnyire későn, arámi hatás következtében (az arámiban a tárgyesetet állandóan ל jelöli), mint אהב 3Móz 19:18, 34; 2Krón 19:2, הרג 2Sám 3:30; Jób 5:2, בוּז (többnyire), בזה 2Sám 6:16, néha továbbá זכר emlékezni, עבד szolgálni (dolgozni vagy szolgálatot tenni valakinek), עזר (8:5, és különösen későn), דרשׁ (különösen a Krónikákban), הִלֵּל (csak a Krónikákban és Ezsdrásnál), רפא (valószínűleg dativus commodi [érdekeltségi részes eset]), שִׂחֵת 1Sám 23:10; 4Móz 32:15, נִדָּה Ámós 6:3, גִּדֵּל Zsolt 34:4, מִּתַּח 116:16, כִּבֵּד 86:9; Dán 11:38, חִזַּק 1Krón 26:27; 29:12, בֵּרַךְ 29:20; Neh 11:2, חֵרֵף2Krón 32:17; l. még 1Sám 22:7; 2Kir 8:6; Jer 16:6; 40:2; Jón 4:6; Zsolt 69:6; 73:18; 135:11; 136:19; 136:20; Péld 17:26; Jób 12:23b JSir 4:5; 1Krón 16:37; 18:6 (הושׁיע, a 2Sám 8:6-ból módosítva: így Zsolt 116:6), 1Krón 25:1; 29:22 (a versben kétszer); 2Krón 5:11; 6:42; 17:7; 24:5; 34:13 (rendszerint על), Ezsd 8:16; felsorolás végén, 1Krón 28:1b; 2Krón 24:12b; 26:14b; 28:23; a határozott tárgyat értelmezőként jelölve, 1Krón 29:18; 2Krón 2:12; 23:1; Zsolt 135:11; 136:19; 136:20 ( = korábban את, 1Móz 26:34; Bír 3:15; Ézs 7:6; 8:2); suffixum után (a szír módjára), 1Krón 5:26 ל ׳וַיַּגְלֵם, 23:6; 2Krón 25:5, 10; 28:15, vö. Neh 9:32; egy főnév suffixumát rendhagyó módon meghatározva, 4Móz 29:18, 21, 24 stb. 1Krón 7:5 לַכֹּל הִתְיַחֲשָׂם, 2Krón 31:16, 18; Ezsd 9:1; 10:14. (De az olyan típusú mondatokban, mint לְנַפְשִׁי דּוֺרֵשׁ אֵין Zsolt 142:5; b 72:12; Ézs 51:18; Jer 14:16; 49:5; JSir 1:7, 9, 17, 21, a ל valószínűleg a ׃אין szóhoz tartozik; vö. a || típusokat: מַכִּיר לִי אֵין Zsolt 142:5 a 5Móz 28:31; Jer 50:32; JSir 1:2, לָהּ אֵין דֹּרֵשׁ Jer 30:17; JSir 4:4.) vö. Ges^§ 117n. 4 Valamivé (εἰς), új állapotba vagy helyzetbe, illetve új szerepbe vagy hivatalba való átmenetről: —

**13.** 

> a. Gen 2:22 לְאִשָּׁה אֶתהַֿצֵּלָע וַיִּבֶן into a woman, 12:2 גָּדוֺל לְגוֺי וְאֶעֶשְׂךָ into a great nation, and very often with this and similar verbs, as Exod 26:7; Isa 44:17, 19, שָׂם Gen 46:3; Isa 5:20 make bitter into sweet etc., 28:17, נָתַן 42:6, also in such phrases as לְשַׁמָּהשָׂם to make into a desolation 13:9; Jer 4:7 etc. 19:8; ל הפך to change into Exod 7:15; Deut 23:6 +, to cut or divide into Gen 32:8; Judg 19:29; Isa 11:15 +, לְ שָׂרַף to burn into Amos 2:1; Deut 9:21 פעל לְעָפָר דַּק Psa 7:14 maketh into (or to be) flaming ones; ל היה to become, in many different connections, as Gen 2:7 חיה לנפשׁ האדם ויהי became a living soul (see היה II.

a. 1Móz 2:22 לְאִשָּׁה אֶתהַֿצֵּלָע וַיִּבֶן asszonnyá, 12:2 גָּדוֺל לְגוֺי וְאֶעֶשְׂךָ nagy nemzetté, és igen gyakran ezzel és hasonló igékkel, mint 2Móz 26:7; Ézs 44:17, 19, שָׂם 1Móz 46:3; Ézs 5:20 a keserűt édessé teszik stb., 28:17, נָתַן 42:6, továbbá olyan kifejezésekben, mint לְשַׁמָּהשָׂם pusztasággá tenni 13:9; Jer 4:7 stb. 19:8; ל הפך valamivé változtatni 2Móz 7:15; 5Móz 23:6 és máshol, valamivé vágni vagy osztani 1Móz 32:8; Bír 19:29; Ézs 11:15 és máshol, לְ שָׂרַף valamivé égetni Ámós 2:1; 5Móz 9:21 פעל לְעָפָר דַּק Zsolt 7:14 lángolókká teszi (vagy: lángolóknak készíti); ל היה valamivé lenni, sokféle összefüggésben, mint 1Móz 2:7 חיה לנפשׁ האדם ויהי élő lélekké lett (l. היה II.

**14.** 

> 2 e, p. 226 a); ׅ (לנגיד למלך משׁח to anoint so as to be king, as king (German 'zum Konig': compare Old English to, as Judg 17:13 and 'We have Abraham to our father'), 1Sam 9:16; 15:1 etc., לְ צִוָּה to appoint as 13:14; 25:30; לְ שׁת Psa 45:17; even more freely, as לְמֶלֶךְ עָלַי דִּבֶּר 1Kin 14:2, compare 2Sam 3:17; 1Chr 29:23; ל חשׁב to count for (or as) Gen 38:15 + often; Exod 21:7 when a man sells his daughter לְאָמָה for, as, a female slave, Deut 6:8 to bind לְאוֺת for, as, a sign, לְשָׂטָן (יָצָא) הִתְיַצֵּב so as to be an adversary Num 22:22, 32, לְאֹרֵב (הקים) קום 1Sam 22:8, 13, לְ עמד Isa 11:10; Dan 11:1, לַחָפְשִׁי יצא to go forth into the state of one free Exod 21:2 (compare 21:26; 21:27 after שׁלח), 2Kin 25:12; Isa 14:2; Jer 34:11; Psa 48:4 לְ נודע hath made himself known as, 87:4 לְ הזכיר to mention as, Ezek 13:20; in poetry Job 39:16 לְלֹאלָֿהּ בָּנֶיהָ הִקְשִׁיחַ treats her young ones hardly (turning them) into none of hers: without a verb (poetry, or late prose) Micah 1:14; Nahum 1:7; Hab 1:11 לֵאלֹהוֺ כֹחוֺ זוֺ, Zech 4:7; Lam 4:3; Job 13:12; Hag 1:9; 1Chr 21:12; 26:29; 28:18b 2Chr 23:4.

2 e, 226. o. a); ׅ (לנגיד למלך משׁח felkenni úgy, hogy király legyen, királlyá (németül 'zum Konig': vö. az óangol to, mint Bír 17:13 és 'We have Abraham to our father'), 1Sám 9:16; 15:1 stb., לְ צִוָּה valamivé kinevezni 13:14; 25:30; לְ שׁת Zsolt 45:17; még szabadabban, mint לְמֶלֶךְ עָלַי דִּבֶּר 1Kir 14:2, vö. 2Sám 3:17; 1Krón 29:23; ל חשׁב valaminek vagy valamiként tartani 1Móz 38:15 és gyakran máshol; 2Móz 21:7 ha valaki eladja leányát לְאָמָה szolgálónak, szolgálóként, 5Móz 6:8 odakötni לְאוֺת jelül, jelként, לְשָׂטָן (יָצָא) הִתְיַצֵּב úgy, hogy ellenfél legyen 4Móz 22:22, 32, לְאֹרֵב (הקים) קום 1Sám 22:8, 13, לְ עמד Ézs 11:10; Dán 11:1, לַחָפְשִׁי יצא szabadként kimenni 2Móz 21:2 (vö. 21:26; 21:27 שׁלח után), 2Kir 25:12; Ézs 14:2; Jer 34:11; Zsolt 48:4 לְ נודע valamiként ismertette meg magát, 87:4 לְ הזכיר valamiként említeni, Ez 13:20; a költészetben Jób 39:16 לְלֹאלָֿהּ בָּנֶיהָ הִקְשִׁיחַ keményen bánik fiaival, (úgy tekintve őket,) mintha nem az övéi volnának: ige nélkül (költészetben vagy késői prózában) Mik 1:14; Náh 1:7; Hab 1:11 לֵאלֹהוֺ כֹחוֺ זוֺ, Zak 4:7; JSir 4:3; Jób 13:12; Hag 1:9; 1Krón 21:12; 26:29; 28:18b 2Krón 23:4.

**15.** 

> b. this usage is also combined idiomatically, with great frequency, with a 2nd לְ, of reference ( 5a d), giving rise to such phrases as Gen 1:29 לְאָכְלָה יִהְיֶה לָכֶם to you it shall be for food (see היה II.

b. ez a használat idiomatikusan, igen gyakran, egy második, vonatkozást jelölő לְ elöljárószóval is társul ( 5a d), és ebből olyan kifejezések keletkeznek, mint 1Móz 1:29 לְאָכְלָה יִהְיֶה לָכֶם nektek eledelül lesz (l. היה II.

**16.** 

> 2 f, p. 226 b), Gen 45:8 לְפַרְעֹה לְאָב וַיְשִׂימֵנִי, 47:26; Deut 28:9, 25; Judg 1:33; 1Sam 2:28; Isa 21:4; 28:18b לְמִרְמָס לוֺ וִהְיִיתֶם, 49:5 לוֺ לְעֶבֶד מִבֶּטֶן יֹצְרִי, 63:8, 10; לְאוֺיֵב לָהֶם וַיֵּהָפֵךְ (Job 30:21), Jer 15:4, 20; 20:4; 21:9; Hab 2:7; Psa 33:12; 94:22; 132:13; 139:22; Job 13:24 לך לאויב ותחשׁבני, 16:12 etc. 5 With reference to, namely a. defining those in reference to whom a predicate is affirmed, hence often = belonging to, of: (a) Deut 23:3 לו יבא לא עשׂירי דור, 23:4; 23:9; Lam 1:10; לְ הכרית 1Sam 2:33; 1Kin 14:10 +; לְ השׁבית Jer 48:35; לְ אִישׁ יִכָּרֵת לֹא 1Kin 2:4; 8:25 +; 1Sam 25:34 לְ נוֺתַר אִם, Gen 17:10 בשׂר כל לכם המול, 34:15, 22; Exod 12:48; 1Sam 11:2; 1Kin 14:13; לְ כסא על ישׁב 2Kin 10:30; 15:12; Jer 13:13; 22:4; Psa 132:12 compare 132:11; לְ בנים ראה Gen 50:23; Psa 128:6; לְ אבד to perish belonging to 1Sam 9:3, 20; Isa 26:14; לְ מצא to find belonging to Deut 22:14; 1Sam 13:22; Gen 23:16 money לַסֹּחֵר עֹבֵר current to ( = with) the merchant, Num 9:10; Amos 9:1; Isa 33:14; Job 12:6: note further the pronoun in Exod 10:5 השׂדה מן לכם הַצֹּמֵחַ, 12:2, 5; 26:33; Lev 11:29 הַטָּמֵא לָכֶם וְזֶה (compare 11:4-8), 19:23; 25:30; 26:5, 26 לֶחֶם מַטֵּה לָכֶם בְּשִׁבְרִי (Ezek 14:13), Num 28:19; 32:21; 34:4; Deut 28:66; Josh 2:6 הַגָּג עַל לָהּ הָעֲרֻכוֺת, Judg 16:9; 19:14 (compare לְ זָרַח Gen 32:32 +), 1Sam 5:9; 2Sam 15:30; 2Kin 4:27b מָרָהלָֿהּ נַפְשָׁהּ (compare Isa 15:4; Jer 4:19), Isa 23:7; Jer 2:21; Micah 2:4 לי ימישׁ איך, Ezek 16:14; 29:7; Psa 110:3; also 40:7 ears hast thou digged to (or for) me, 51:12 (compare 1Sam 10:9), Isa 50:4-5, אזן לי יעיר. (b) in such phrases as Num 1:4 לְמַטֶּה אִישׁ אִישׁ a man for (or of) a tribe, 7:11; 31:4, Deut 1:23; Josh 3:12; 18:4; Judg 20:10 ten men לַמֵּאָה of 100, 100 of1000etc.; לְ רִאשׁוֺן = first of Exod 12:2; 2Sam 19:21. (c) specifically of relationship, to define a man's family or tribe, especially in Genealogies, Num 1:6 אליצור לראובן, 1:7; 1:8 etc., 1:22; 1:24 etc., 3:21, 27; 1Chr 24:20-21, etc., 26:23, 25 etc. + often; in the opposite order Exod 31:2; Lev 24:11; Numbers 17:23 לוי לבית אהרן 1Kin 15:27 etc., compare 2Sam 3:2-3, 5, also 9:3 a Gen 20:18; 46:26-27, similarly לְ הנשׁארים 2Kin 10:11, 17, לְ הַמֵּת 1Kin 14:11; 16:4 +. (d) denoting relation (to be to or towards one in a particular regard or capacity) Exod 19:5 סְגֻלָּה לי והייתם ye shall be to me a special possession, 22:30 לי תהיון קדשׁ אנשׁי, 1Sam 18:18; 2Sam 19:29; 1Kin 5:15; 2Kin 19:15; Jer 12:9; 15:8; 22:6 לי אתה גלעד, 51:20; Isa 54:9; Ezek 24:19; Psa 12:5 לָנוּ אָדוֺן מִי, 35:14 לִי כְּאָח כְּרֵעַ, 99:8; Job 24:17; 30:29; Neh 6:18; with a participle Num 10:25; 25:18; 35:23; Deut 4:22; 19:4, 6; Isa 11:9; 14:2 (Dr^§ 135, 7 Obs.); לְ מלך Num 22:4; לָכֶם רַב it is (too) much to you, לְ מְעַט (too) little to . . .; in the phrase לְךָ אֵלֶּה (מָהׅ מִי who (what) are these to thee ? = what meanest thou by these things ? Gen 33:5, 8; 2Sam 16:2; Ezek 37:18, compare Exod 12:26; Josh 4:6; Ezek 12:22; לי חלילה away be it to (or for) me ! לי למה to what purpose to me is . . . ? Gen 27:46; Isa 1:11; Jer 6:20; Job 30:2: often also in such phrases as לְ מָגֵן a shield to Gen 15:1; Psa 18:31, a strength to 28:8, an abomination to Gen 43:32; Isa 1:13 +, a grief to Prov 10:1; 17:21; compare Jer 15:10; Mal 2:9; Psa 89:28 etc.: note also Jonah 3:3 גדולה עיר לאלהים a city great to God (i.e. in his estimation: compare Acts 7:20 ἀστεῖος τῷ θεῷ, and לפני Gen 10:9), Est 10:3. And with כְּ Judg 17:11; 2Sam 12:3 כְּבַת לוֺ וַתְּהִי, Exod 22:24 (compare 4b), Amos 9:7 לי אַתֶּם כֻשִׁיים כבני Hosea 11:4; Isa 29:2; Job 33:6 כְּפִיךָ לָאֵל הֵןאֲֿנִי lo, I am to God as thou art, etc.

2 f, 226. o. b), 1Móz 45:8 לְפַרְעֹה לְאָב וַיְשִׂימֵנִי, 47:26; 5Móz 28:9, 25; Bír 1:33; 1Sám 2:28; Ézs 21:4; 28:18b לְמִרְמָס לוֺ וִהְיִיתֶם, 49:5 לוֺ לְעֶבֶד מִבֶּטֶן יֹצְרִי, 63:8, 10; לְאוֺיֵב לָהֶם וַיֵּהָפֵךְ (Jób 30:21), Jer 15:4, 20; 20:4; 21:9; Hab 2:7; Zsolt 33:12; 94:22; 132:13; 139:22; Jób 13:24 לך לאויב ותחשׁבני, 16:12 stb. 5 Valamire vonatkozóan, tudniillik a. azokat meghatározva, akikre vonatkozóan az állítmány érvényes, ennélfogva gyakran = valakihez tartozó, valakié: (a) 5Móz 23:3 לו יבא לא עשׂירי דור, 23:4; 23:9; JSir 1:10; לְ הכרית 1Sám 2:33; 1Kir 14:10 és máshol; לְ השׁבית Jer 48:35; לְ אִישׁ יִכָּרֵת לֹא 1Kir 2:4; 8:25 és máshol; 1Sám 25:34 לְ נוֺתַר אִם, 1Móz 17:10 בשׂר כל לכם המול, 34:15, 22; 2Móz 12:48; 1Sám 11:2; 1Kir 14:13; לְ כסא על ישׁב 2Kir 10:30; 15:12; Jer 13:13; 22:4; Zsolt 132:12, vö. 132:11; לְ בנים ראה 1Móz 50:23; Zsolt 128:6; לְ אבד elveszni valakitől 1Sám 9:3, 20; Ézs 26:14; לְ מצא valakinél találni 5Móz 22:14; 1Sám 13:22; 1Móz 23:16 a kereskedőnél ( = a kereskedők között) forgalomban levő לַסֹּחֵר עֹבֵר pénz, 4Móz 9:10; Ámós 9:1; Ézs 33:14; Jób 12:6: figyeld meg továbbá a névmást a 2Móz 10:5 השׂדה מן לכם הַצֹּמֵחַ, 12:2, 5; 26:33; 3Móz 11:29 הַטָּמֵא לָכֶם וְזֶה (vö. 11:4-8), 19:23; 25:30; 26:5, 26 לֶחֶם מַטֵּה לָכֶם בְּשִׁבְרִי (Ez 14:13), 4Móz 28:19; 32:21; 34:4; 5Móz 28:66; Józs 2:6 הַגָּג עַל לָהּ הָעֲרֻכוֺת, Bír 16:9; 19:14 (vö. לְ זָרַח 1Móz 32:32 és máshol), 1Sám 5:9; 2Sám 15:30; 2Kir 4:27b מָרָהלָֿהּ נַפְשָׁהּ (vö. Ézs 15:4; Jer 4:19), Ézs 23:7; Jer 2:21; Mik 2:4 לי ימישׁ איך, Ez 16:14; 29:7; Zsolt 110:3 helyeken; továbbá 40:7 füleket vájtál nekem (vagy számomra), 51:12 (vö. 1Sám 10:9), Ézs 50:4-5, אזן לי יעיר. (b) olyan kifejezésekben, mint 4Móz 1:4 לְמַטֶּה אִישׁ אִישׁ egy-egy férfi törzsenként (vagy törzsből), 7:11; 31:4, 5Móz 1:23; Józs 3:12; 18:4; Bír 20:10 tíz férfi לַמֵּאָה százból, száz ezerből stb.; לְ רִאשׁוֺן = valaminek az elseje 2Móz 12:2; 2Sám 19:21. (c) különösen rokonsági viszonyról, valakinek a családja vagy törzse meghatározására, főként a nemzetségtáblákban, 4Móz 1:6 אליצור לראובן, 1:7; 1:8 stb., 1:22; 1:24 stb., 3:21, 27; 1Krón 24:20-21 stb., 26:23, 25 stb. és gyakran máshol; fordított sorrendben 2Móz 31:2; 3Móz 24:11; 4Móz 17:23 לוי לבית אהרן 1Kir 15:27 stb., vö. 2Sám 3:2-3, 5, továbbá 9:3 a 1Móz 20:18; 46:26-27, hasonlóan לְ הנשׁארים 2Kir 10:11, 17, לְ הַמֵּת 1Kir 14:11; 16:4 és máshol. (d) viszonyt jelölve (valaki számára vagy valaki iránt valamilyen tekintetben vagy minőségben lenni) 2Móz 19:5 סְגֻלָּה לי והייתם az én tulajdonom lesztek, 22:30 לי תהיון קדשׁ אנשׁי, 1Sám 18:18; 2Sám 19:29; 1Kir 5:15; 2Kir 19:15; Jer 12:9; 15:8; 22:6 לי אתה גלעד, 51:20; Ézs 54:9; Ez 24:19; Zsolt 12:5 לָנוּ אָדוֺן מִי, 35:14 לִי כְּאָח כְּרֵעַ, 99:8; Jób 24:17; 30:29; Neh 6:18; participiummal 4Móz 10:25; 25:18; 35:23; 5Móz 4:22; 19:4, 6; Ézs 11:9; 14:2 (Dr^§ 135, 7 Obs.); לְ מלך 4Móz 22:4; לָכֶם רַב (túl) sok nektek, לְ מְעַט (túl) kevés valakinek ...; a לְךָ אֵלֶּה (מָהׅ מִי kifejezésben: kik (mik) ezek neked? = mit akarsz ezekkel? 1Móz 33:5, 8; 2Sám 16:2; Ez 37:18, vö. 2Móz 12:26; Józs 4:6; Ez 12:22; לי חלילה távol legyen tőlem! לי למה mire jó nekem ...? 1Móz 27:46; Ézs 1:11; Jer 6:20; Jób 30:2: gyakran olyan kifejezésekben is, mint לְ מָגֵן pajzs valakinek 1Móz 15:1; Zsolt 18:31, erősség valakinek 28:8, utálatosság valakinek 1Móz 43:32; Ézs 1:13 és máshol, bánat valakinek Péld 10:1; 17:21; vö. Jer 15:10; Mal 2:9; Zsolt 89:28 stb.: figyeld meg még Jón 3:3 גדולה עיר לאלהים Isten előtt nagy város (azaz az ő becslése szerint: vö. ApCsel 7:20 ἀστεῖος τῷ θεῷ, és לפני 1Móz 10:9), Eszt 10:3. כְּ igével is Bír 17:11; 2Sám 12:3 כְּבַת לוֺ וַתְּהִי, 2Móz 22:24 (vö. 4b), Ámós 9:7 לי אַתֶּם כֻשִׁיים כבני Hós 11:4; Ézs 29:2; Jób 33:6 כְּפִיךָ לָאֵל הֵןאֲֿנִי íme, én Isten előtt olyan vagyok, mint te stb.

**17.** 

> b. denoting possession, belonging to; — (a) as predicate, in לְ הָיָה (compare Latin est mihi), לְ אֵין לְ יֵשׁ constantly (see these words); also alone, as Gen 31:16, 43 הוּא לִי it is mine, 48:5 הם לי, Exod 19:5b הארץ כל לי כי, 1Kin 20:3-4, Isa 43:1 אתה לי, 44:5 ׳לי אני, Ezek 29:3; Psalm 47:10; Psa 50:10; 50:12; Job 12:13, 16; Song 2:16; 6:3; 1Sam 1:2 נשׁים שׁתי ולו and he had two wives, 25:7, 36; Judg 3:16; 17:5; Job 22:8; 2Sam 17:18; Hosea 6:10, + often; with לאֹ, 1Kin 22:17; Isa 53:2 לו הדר לא, Jer 5:10 +; with a neuter adjective (rare) Isa 63:2; Jer 30:10 לְשִׁבְרֵךְ אָנוּשׁ; note also such phrases as 2Kin 10:19 לבעל לי גדול זבח, Isa 2:12 וג ׳על לי יוֺם ׳כִּי for ׳י hath a day against etc., 22:5; 28:2 ׳י לי וְאַמִּץ חָזָק ׳הִנֵּה hath a strong and mighty one (that is, at his disposal), 34:2 לי וג׳קצף ׳על, 34:6 b. 8; Hosea 4:1 . . . לי רִיב ׳כִּי עם, 12:3; Micah 6:2: וָלָךְ מַהלִּֿי what is there to me and to thee (?) (i.e. what have we to do with each other (?)), see מָה לך שׁלום peace be to thee ! Of that which pertains to one as a right, Lev 25:31, 48; Deut 1:17 הוא לאלהים המשׁפט כי, 21:17; 1Sam 17:47; Jer 10:23; 32:7-8, Ezek 21:32; Psalm 3:9 ׳לי הישׁועה, Jonah 2:10; with an infinitive 1Sam 23:20 הַסְגִּירוֺ וְלָנוּ and it shall be for us (or our place) to deliver him, Micah 3:1 לדעת לכם הלא, Ezra 4:3; 2Chr 13:5; 20:17; 26:18, compare Psa 50:16 לְ מַהלְּֿךָ. (b) here also belongs the so-called Lamed auctoris, Isa 38:9 לְחִזְקִיָּהוּ מִכְתָּב a writing belonging to, of, or by H., Hab 3:1; Psa 3:1 and often לדוד מזמור a Psalm of or by David (but possibly denoting originally, at least in some cases, a Psalm belonging to a collection known as David's: so certainly in קרח לבני 42:1 and elsewhere, and probably also in לאסף 50:1 and elsewhere); so מזמור לדוד 24:1 +, לדוד alone 10:1; 14:1 +. compare on Phoenician coins לצדנם of the Sidonians, i.e. belonging to them, לצור (= Greek Σιδονιων, Τύρου). Hebrew idiom also uses the ל of possession where we should write the simple name, as Ezek 38:16 (written on a stick) ליהּודה, 38:17 ליוסף, in English 'Judah,' 'Joseph,' Isa 8:1 למהרשֿׁללחֿשׁבֿז 'Maher-shalal-hash-baz.' c. as periph. for the stative with — (a) לְ אשׁר, as Exod 29:29; 39:1, 39; Lev 7:20-21, 16:6, 15 (see further examples below אשׁר 7); so שֶׁלִּי Song 1:6; 8:12, שֶׁלָּנוּ 2Kin 6:11. (b) without אשׁר — (a) where it is desired to keep the first noun indeterm., 1Sam 16:18 לישׁי בן ראיתי a son to or of Jesse, 22:20; Gen 41:12; Num 1:4; 7:24; 1Kin 2:39 לשׁמעי עבדים שׁני, 18:22; 2Kin 3:11; Ruth 2:1 etc.;

b. birtoklást jelölve: valakihez tartozó; — (a) állítmányként, a לְ הָיָה (vö. latin est mihi), לְ אֵין לְ יֵשׁ kifejezésekben állandóan (l. e szavakat); önmagában is, mint 1Móz 31:16, 43 הוּא לִי az enyém, 48:5 הם לי, 2Móz 19:5b הארץ כל לי כי, 1Kir 20:3-4, Ézs 43:1 אתה לי, 44:5 ׳לי אני, Ez 29:3; Zsolt 47:10; Zsolt 50:10; 50:12; Jób 12:13, 16; Én 2:16; 6:3; 1Sám 1:2 נשׁים שׁתי ולו és két felesége volt, 25:7, 36; Bír 3:16; 17:5; Jób 22:8; 2Sám 17:18; Hós 6:10, és gyakran máshol; לאֹ szóval, 1Kir 22:17; Ézs 53:2 לו הדר לא, Jer 5:10 és máshol; semleges melléknévvel (ritka) Ézs 63:2; Jer 30:10 לְשִׁבְרֵךְ אָנוּשׁ; figyeld meg még az olyan kifejezéseket is, mint 2Kir 10:19 לבעל לי גדול זבח, Ézs 2:12 וג ׳על לי יוֺם ׳כִּי mert ׳י napja van ... ellen stb., 22:5; 28:2 ׳י לי וְאַמִּץ חָזָק ׳הִנֵּה van egy erős és hatalmas (tudniillik a rendelkezésére), 34:2 לי וג׳קצף ׳על, 34:6 b. 8; Hós 4:1 ... לי רִיב ׳כִּי עם, 12:3; Mik 6:2: וָלָךְ מַהלִּֿי mi van nekem és neked (?) (azaz mi közünk egymáshoz (?)), l. מָה לך שׁלום békesség neked! Arról, ami jog szerint illet meg valakit, 3Móz 25:31, 48; 5Móz 1:17 הוא לאלהים המשׁפט כי, 21:17; 1Sám 17:47; Jer 10:23; 32:7-8, Ez 21:32; Zsolt 3:9 ׳לי הישׁועה, Jón 2:10; infinitivusszal 1Sám 23:20 הַסְגִּירוֺ וְלָנוּ és a mi dolgunk (vagy helyünk) lesz kiszolgáltatni őt, Mik 3:1 לדעת לכם הלא, Ezsd 4:3; 2Krón 13:5; 20:17; 26:18, vö. Zsolt 50:16 לְ מַהלְּֿךָ. (b) ide tartozik az úgynevezett Lamed auctoris is, Ézs 38:9 לְחִזְקִיָּהוּ מִכְתָּב H.-hoz tartozó, H.-é vagy H. által írt irat, Hab 3:1; Zsolt 3:1 és gyakran לדוד מזמור Dávidé vagy Dávid által írt zsoltár (de eredetileg, legalábbis néhány esetben, talán olyan zsoltárt jelölt, amely a Dávidénak ismert gyűjteményhez tartozott: így bizonyosan a קרח לבני esetében 42:1 és máshol, és valószínűleg a לאסף esetében is 50:1 és máshol); így מזמור לדוד 24:1 és máshol, לדוד önmagában 10:1; 14:1 és máshol. vö. a föníciai érméken לצדנם a szidóniaké, azaz hozzájuk tartozó, לצור (= görög Σιδονιων, Τύρου). A héber nyelvhasználat a birtoklás ל elöljárószavát olyankor is alkalmazza, amikor mi az egyszerű nevet írnánk, mint Ez 38:16 (pálcára írva) ליהּודה, 38:17 ליוסף, angolul 'Judah,' 'Joseph,' Ézs 8:1 למהרשֿׁללחֿשׁבֿז 'Maher-shalal-hash-baz.' c. a status constructus körülírásaként — (a) לְ אשׁר, mint 2Móz 29:29; 39:1, 39; 3Móz 7:20-21, 16:6, 15 (további példákat l. lent אשׁר 7); így שֶׁלִּי Én 1:6; 8:12, שֶׁלָּנוּ 2Kir 6:11. (b) אשׁר nélkül — (a) ha az első főnevet határozatlanul akarják hagyni, 1Sám 16:18 לישׁי בן ראיתי Isainak egy fia, 22:20; 1Móz 41:12; 4Móz 1:4; 7:24; 1Kir 2:39 לשׁמעי עבדים שׁני, 18:22; 2Kir 3:11; Ruth 2:1 stb.;

**18.** 

> (β) where the Genitive is a compound term, to avoid a series of nouns in the stative with Num 1:4 אבותיו לבית ראשׂ, 7:24, 30, 36 etc., 1:21 ראובן למטה פקֻדיהם 1:23; 1:25 etc., 2:9, 16 etc., Josh 21:38; 1Chr 9:23 י לְבֵית ׳הַשְּׁעָרִים 27:3 לְ הראשׁ, 2Chr 19:11; Neh 10:39 etc., occas. also besides, as 1Sam 14:16 לשׁאול הצופים, Exod 31:7 (usually העדות ארון);

(β) ha a birtokos összetett kifejezés, hogy elkerüljék a status constructusban álló főnevek láncát 4Móz 1:4 אבותיו לבית ראשׂ, 7:24, 30, 36 stb., 1:21 ראובן למטה פקֻדיהם 1:23; 1:25 stb., 2:9, 16 stb., Józs 21:38; 1Krón 9:23 י לְבֵית ׳הַשְּׁעָרִים 27:3 לְ הראשׁ, 2Krón 19:11; Neh 10:39 stb., alkalmanként más esetben is, mint 1Sám 14:16 לשׁאול הצופים, 2Móz 31:7 (rendszerint העדות ארון);

**19.** 

> (γ) where the regens is a proper name, or a compound term, which does not readily admit of being placed in the stative with as (יהודה) ישׂראל למלכי הימים דברי 1Kin 14:19, 29 + often, 1 Kings 5:30 לְ הנצבים שׂרי, 2Kin 11:4 לְ האבות ראשׁי לְ המאות שׂרי Num 36:1; Josh 19:51; 1Chr 8:13 +? Nehemiah Ezra; in dates, as לחדשׁ באחד Gen 8:5, 14; Exod 12:3, 6; Gen 7:11 נח לחיי ֗֗֗ בשׁנת, 16:3; Exod 19:1 . . . לאסא שׁתים בשׁנת לצאת השׁלישׁי בחדשׁ 1Kin 15:25, 28; 16:8 (all + often); other cases, Exod 20:5-6, Lev 13:48; Num 16:22 ( = 27:16) 18:15; Judg 20:10; 2Kin 5:9; Ezek 45:19; Ruth 2:3; 1Chr 4:43; 9:19, 21; 26:19; 2Chr 22:10; 23:4;

(γ) ha a régens tulajdonnév vagy olyan összetett kifejezés, amely nehezen állhat status constructusban, mint (יהודה) ישׂראל למלכי הימים דברי 1Kir 14:19, 29 és gyakran máshol, 1Kir 5:30 לְ הנצבים שׂרי, 2Kir 11:4 לְ האבות ראשׁי לְ המאות שׂרי 4Móz 36:1; Józs 19:51; 1Krón 8:13 és máshol? Nehémiás, Ezsdrás; keltezésekben, mint לחדשׁ באחד 1Móz 8:5, 14; 2Móz 12:3, 6; 1Móz 7:11 נח לחיי ֗֗֗ בשׁנת, 16:3; 2Móz 19:1 ... לאסא שׁתים בשׁנת לצאת השׁלישׁי בחדשׁ 1Kir 15:25, 28; 16:8 (mind gyakran máshol is); más esetek: 2Móz 20:5-6, 3Móz 13:48; 4Móz 16:22 ( = 27:16) 18:15; Bír 20:10; 2Kir 5:9; Ez 45:19; Ruth 2:3; 1Krón 4:43; 9:19, 21; 26:19; 2Krón 22:10; 23:4;

**20.** 

> (δ) with a negative, Gen 15:13 לכם לא כארץ, Jer 5:19; Prov 26:17; Hab 1:6, poetic even alone, 2:6 who increaseth לוֺ לֹא (that which is) not his, Job 18:15 לוֺ בְּלִי, 39:16 לְאֹלָהּ as ( 4) those which are not hers;

(δ) tagadással, 1Móz 15:13 לכם לא כארץ, Jer 5:19; Péld 26:17; Hab 1:6, a költészetben önmagában is, 2:6 aki gyarapítja לוֺ לֹא (azt, ami) nem az övé, Jób 18:15 לוֺ בְּלִי, 39:16 לְאֹלָהּ mint ( 4) amelyek nem az övéi;

**21.** 

> (ε) in poetry, Isa 16:2; 26:7 לצדיק ארח Jer 47:3; Hosea 9:6; Psa 37:16; 49:14; 55:19 (Hi De Ch), 58:5; 73:6; 105:36; 116:15 לחסידיו המותה, 123:4; Jonah 2:3; Eccl 5:11; compare also לְ מלך Josh 12:18 (but see ᵐ5 Di), 2Kin 19:13 (compare Aramaic Ezra 5:11): see further Ew^§ 292, Ges^§ 129, Gies^§ 19.

(ε) a költészetben, Ézs 16:2; 26:7 לצדיק ארח Jer 47:3; Hós 9:6; Zsolt 37:16; 49:14; 55:19 (Hi De Ch), 58:5; 73:6; 105:36; 116:15 לחסידיו המותה, 123:4; Jón 2:3; Préd 5:11; vö. még לְ מלך Józs 12:18 (de l. ᵐ5 Di), 2Kir 19:13 (vö. az arámi Ezsd 5:11): l. továbbá Ew^§ 292, Ges^§ 129, Gies^§ 19.

**22.** 

> c. attached to adverbs, especially those compounded with מִן, it forms prepositions, as לְ מִקֶּדֶם Gen 3:24 literally off the front with reference to (or of) = in front of: so לְ מִבֵּית = within, לְ מִחוּץ = without, לְ מֵעַל לְ, מִמַּעַל,לְ סָבִֹיב לְ, מִצְּפוֺן לְ, מֵהָֽלְאָה לְ, מֵעֵבֶר (all often); more rarely, לְ וּמִזֶּה מִזֶּה לְ, בֵּינוֺת אֶל לְ, מִבֵּינוֺת לְ, מִבַּעַד לְ, מֵאַחֲרֵי Exod 38:15, לְ הֵנָּה, Dan 12:5 (twice in verse), לְ תַּחַת לְ, מִסָּבִיב לְ, מִנֶּגֶד לְ, מִימִין לְ, מִזְרָח, in poetry לְ נֶגְדָּהנָּֿא, Psa 116:14; 116:18. see חוץ בית,, etc.; and compare Judg 7:1, 8.

c. határozószókhoz, különösen a מִן elöljárószóval összetettekhez kapcsolva elöljárószókat alkot, mint לְ מִקֶּדֶם 1Móz 3:24 szó szerint: elölről valamire vonatkozóan (vagy valaminek) = valami előtt: így לְ מִבֵּית = belül, לְ מִחוּץ = kívül, לְ מֵעַל לְ, מִמַּעַל,לְ סָבִֹיב לְ, מִצְּפוֺן לְ, מֵהָֽלְאָה לְ, מֵעֵבֶר (mind gyakran); ritkábban לְ וּמִזֶּה מִזֶּה לְ, בֵּינוֺת אֶל לְ, מִבֵּינוֺת לְ, מִבַּעַד לְ, מֵאַחֲרֵי 2Móz 38:15, לְ הֵנָּה, Dán 12:5 (a versben kétszer), לְ תַּחַת לְ, מִסָּבִיב לְ, מִנֶּגֶד לְ, מִימִין לְ, מִזְרָח, a költészetben לְ נֶגְדָּהנָּֿא, Zsolt 116:14; 116:18. l. חוץ בית,, stb.; és vö. Bír 7:1, 8.

**23.** 

> d. construed with passive verbs, the ל of reference notifies the agent, as לְ בָּרוּךְ blessed by, Gen 14:17 + often; otherwise not very common, 14:17 + often; otherwise not very common, 31:15 לְ נֶחְשַׁב to be reckoned by (so Isa 40:17), Exod 12:16 לָכם יֵעָשֶׂה לְבַדּוֺ, חוּא לְכָלנֶֿפֶשׁ יֵאָכֵל אֲשֶׁר אַךְ, 1Sam 2:3; 25:7; 2Sam 19:43; Jer 8:3 לְ נִבְחַר (Prov 21:3), 29:22 Psa 73:10; 111:2; Prov 13:13 יֵחָבֶללֿוֺ is pledged by it, 14:20; Neh 6:1, 7 לְ נִשְׁמַע, 13:26 לְ אָהוּב, Est 4:3; 5:12; Eccl 5:12 לְ שָׁמוּר. So with נִרְאָה Exod 13:7 ( = Deut 16:4), נוֺדַע 1Sam 6:3; Ezek 36:32; Neh 4:9 (but usually with these words לְ is rather the dativus commodi [dative of benefit] be known, appear, to), נעתר Gen 25:21 +, נדרשׁ and נמצא Isa 65:1 +?entreated, sought, found, by, נוֺסַר Lev 26:23, נענה Ezek 14:4, 7 (?). (compare in Syriac Nö^§ 247, especially with passive participle:§ 279 (so Talmud, Luz^§ 90), which in Mandean and New Syriac even unites with the ל to form a new tense, see Nö^M § 263; NS § 104.) Analogously Gen 38:15 לוֺ וַתַּהַר and was pregnant by, 38:18 לְ הָרָה (adjective) pregnant by (literally to).

d. szenvedő igékkel szerkesztve a vonatkozás ל elöljárószava a cselekvőt jelöli, mint לְ בָּרוּךְ valaki által áldott, 1Móz 14:17 és gyakran máshol; egyébként nem nagyon gyakori, 14:17 és gyakran máshol; egyébként nem nagyon gyakori, 31:15 לְ נֶחְשַׁב valaki által valaminek tartatni (így Ézs 40:17), 2Móz 12:16 לָכם יֵעָשֶׂה לְבַדּוֺ, חוּא לְכָלנֶֿפֶשׁ יֵאָכֵל אֲשֶׁר אַךְ, 1Sám 2:3; 25:7; 2Sám 19:43; Jer 8:3 לְ נִבְחַר (Péld 21:3), 29:22 Zsolt 73:10; 111:2; Péld 13:13 יֵחָבֶללֿוֺ zálogul lekötötte magát neki, 14:20; Neh 6:1, 7 לְ נִשְׁמַע, 13:26 לְ אָהוּב, Eszt 4:3; 5:12; Préd 5:12 לְ שָׁמוּר. Így נִרְאָה igével 2Móz 13:7 ( = 5Móz 16:4), נוֺדַע 1Sám 6:3; Ez 36:32; Neh 4:9 (de ezekkel a szavakkal a לְ rendszerint inkább dativus commodi [érdekeltségi részes eset]: ismertté lenni, megjelenni valakinek), נעתר 1Móz 25:21 és máshol, נדרשׁ és נמצא Ézs 65:1 és máshol? valaki által kérlelt, keresett, megtalált, נוֺסַר 3Móz 26:23, נענה Ez 14:4, 7 (?). (vö. a szírben Nö^§ 247, különösen passzív participiummal: § 279 (így a Talmud, Luz^§ 90), amely a mandeus és az újszír nyelvben a ל elöljárószóval egyenesen új igeidőt alkot, l. Nö^M § 263; NS § 104.) Ennek mintájára 1Móz 38:15 לוֺ וַתַּהַר és teherbe esett valakitől, 38:18 לְ הָרָה (melléknév) valakitől várandós (szó szerint: valakinek).

**24.** 

> e. regarding, in respect of, namely (a) with verbs of speaking, commanding, hearing, etc.; concerning, about (synonym עַל, which is more usually); so with אָמַר Gen 20:13; Deut 33:12-13, + Judg 9:54; Isa 41:7; Psa 3:3; 41:6 +, דִּבֶּר Ezek 44:5, סִמֵּר Psa 22:31, דרשׁ Deut 12:30; 2Sam 11:3, חָלַם Gen 42:9, הִטִּיף Micah 2:6, צִוָּה Num 8:20; Psa 91:11 +, שָׁמַע Gen 17:20, and often in the adjunct . . . לאשׁר ֗֗֗ אשׁר לכל 27:8; Josh 1:18; 22:2 +; שׁאל Gen 26:7 +, especially in phrase לפ ׳שׁאל לְשָׁלוֺם to ask about any one with reference to (his) welfare; in the phrase הַזֶּה לַדָּבָר in regard to this thing (idiomatic), 19:21; 1Sam 30:24 +, Judg 21:5, 7 לנשׁים, 1Kin 20:7; without a verb, Lev 7:37; 14:54; Deut 33:7, and in titles Jer 23:9; 46:2; 48:1; 49:1, 7, 23, 28. (b) limiting the application of a term, especially with כְּ to denote the tertium comparationis, as Gen 41:19 לָרֹעַ ֗֗֗ כָהֵנָּה רָאִיתִי לאֹ as regards, in respect of (in our idiom, simply in or for) badness, Exod 24:10 לָטֹהַר הַשָּׁמַיִם כְּעֶצֶם in brightness, Deut 34:11-12, Ezek 3:3 (read לְמֹתֶק) Prov 25:3; 1Chr 24:4; with an infinitive, Gen 3:22 לדעת ממנו כאחד היה in respect of knowing etc., 34:15; Isa 21:1 לַחֲלוֺף כַּסּוּפוֺת as whirlwinds in respect of sweeping through, Josh 10:14; 2Sam 14:17, 25; Ezek 38:9, 16; Prov 26:2 לָעוּף כדרור לָנוּד כצפור, 1Chr 12:9 לְמַהֵר כצבאים; with לָרֹב in multitude, Deut 1:10 לרב השׁמים ככוכבי Judg 7:12 (twice in verse) + often; less frequently in comparisons with מִן, 1Kin 10:23 וּלְחָכְמָה לְעשֶׁר ֗֗֗ מִכֹּל ֗֗֗ וַיִּגְדַּל, Song 1:2; Job 30:1 לימים ממני צעירים (compare the accusative 15:10), 32:4, 6, compare 11:6 לְתוּשִׁיָּה כִּפְלַיִם; rarely after substantives, 2Chr 16:8; 21:3; 3:8 לְכִכָּרִים, 3:9; 3:11; Ezra 8:26 (where the earlier language would use apposition, or the accusative of specification, Dr^§ 194). (c) somewhat differently, Lev 5:4b and be guilty מֵאֵלָּה לְאַחַת as regards one of these things, 5:5; 22:5b; Num 18:7 (compare 1Chr 26:32; 27:1; 2Chr 19:11 (twice in verse)) Jer 2:37 (peculiar) thou shalt not prosper להם as regards them, Ezek 44:14, compare Job 9:19; after substantive Gen 47:26 לַחֹמֶשׁ (but compare ᵐ5 Di) with reference to the fifth, Lev 7:26; 11:46b Num 19:11; 29:39; 30:13; Deut 19:15; 23:19; Ezra 8:34; 1Chr 27:1 (ח ׳לכל), 2Chr 8:15; Neh 11:24. (d) ֗֗֗ לְכֹל לְכָלֿׅ), at the close of a description or enumeration, with a Generalizing force, as regards all . . . = namely, in brief (Ew^§ 310 a ), chiefly in P and Chronicles (probably a juristic usage): Gen 9:10b all that go out of the ark הָאָרֶץ חַיַּת לְכֹל as regards ( = namely, even) all beasts of the earth, 23:10b; Exod 14:28 (compare 14:9 וְ), 27:3, 19; 28:38; 30:1b; Lev 5:3-4, (compare 13:51) 11:42; 16:16, 21; 22:18; Num 3:26b (3:31 3:36 וְ), 4:27, 31, 32; 5:9; 18:4, 8, 9, 11 (all P), 2Kin 12:6; Jer 19:13; Ezek 44:9; 1Chr 13:1; 2Chr 5:12 (לְכֻלָּם), 25:5; 31:16; 33:8 b (|| 2Kin 21:8 ולכל) Ezra 1:5. (e) introducing a new subject (rare, and text sometimes dubious; chiefly Chronicles), as regards . . ., Isa 32:1 ולשׂרים (read probably ל וְשָׂרִים by error from following למשׁפט), Lev 11:26; 1Chr 3:2 (read probably אבשׁלום), 5:2 ( ? see Ke), 7:1 (Ke ובני), 7:5 a (?), 24:1; 26:1, 23, 25, 26, 31 a B 2Chr 5:12; 7:21 ישׁרק עליו לְכָלע־ֹבֵר (|| 1Kin 9:8 כָּלעֹֿבֵר), compare Deut 24:5 (peculiar); Eccl 9:4 וג ׳טוב הוא חַי לְכֶלֶב בִּי; compare Psa 17:4 (on 16:3 see Commentaries). In Chronicles sometimes used peculiarly as a periphrase, 1Chr 28:1 b. 21 נדיב לכל as regards every liberal man = every liberal man (compare Ke), 29:5 a.

e. valamire nézve, valami tekintetében, tudniillik (a) a beszéd, parancsolás, hallás stb. igéivel: valakiről, valamiről (szinonimája a עַל, amely szokásosabb); így אָמַר igével 1Móz 20:13; 5Móz 33:12-13, és Bír 9:54; Ézs 41:7; Zsolt 3:3; 41:6 és máshol, דִּבֶּר Ez 44:5, סִמֵּר Zsolt 22:31, דרשׁ 5Móz 12:30; 2Sám 11:3, חָלַם 1Móz 42:9, הִטִּיף Mik 2:6, צִוָּה 4Móz 8:20; Zsolt 91:11 és máshol, שָׁמַע 1Móz 17:20, és gyakran a ... לאשׁר ֗֗֗ אשׁר לכל járulékban 27:8; Józs 1:18; 22:2 és máshol; שׁאל 1Móz 26:7 és máshol, különösen a לפ ׳שׁאל לְשָׁלוֺם kifejezésben: valakinek a (hogy)létéről kérdezősködni; a הַזֶּה לַדָּבָר kifejezésben: ebben a dologban (idiomatikus), 19:21; 1Sám 30:24 és máshol, Bír 21:5, 7 לנשׁים, 1Kir 20:7; ige nélkül, 3Móz 7:37; 14:54; 5Móz 33:7, és címekben Jer 23:9; 46:2; 48:1; 49:1, 7, 23, 28. (b) egy kifejezés alkalmazását korlátozva, különösen כְּ mellett a tertium comparationis jelölésére, mint 1Móz 41:19 לָרֹעַ ֗֗֗ כָהֵנָּה רָאִיתִי לאֹ rosszaság tekintetében, rosszaságra nézve (a mi nyelvhasználatunkban egyszerűen: rosszaságban vagy rosszaság dolgában), 2Móz 24:10 לָטֹהַר הַשָּׁמַיִם כְּעֶצֶם fényességben, 5Móz 34:11-12, Ez 3:3 (olv. לְמֹתֶק) Péld 25:3; 1Krón 24:4; infinitivusszal, 1Móz 3:22 לדעת ממנו כאחד היה a tudás tekintetében stb., 34:15; Ézs 21:1 לַחֲלוֺף כַּסּוּפוֺת mint a forgószelek, átvonulásukat tekintve, Józs 10:14; 2Sám 14:17, 25; Ez 38:9, 16; Péld 26:2 לָעוּף כדרור לָנוּד כצפור, 1Krón 12:9 לְמַהֵר כצבאים; לָרֹב mellett: sokaságban, 5Móz 1:10 לרב השׁמים ככוכבי Bír 7:12 (a versben kétszer) és gyakran máshol; ritkábban מִן melletti összehasonlításokban, 1Kir 10:23 וּלְחָכְמָה לְעשֶׁר ֗֗֗ מִכֹּל ֗֗֗ וַיִּגְדַּל, Én 1:2; Jób 30:1 לימים ממני צעירים (vö. a tárgyesetet 15:10), 32:4, 6, vö. 11:6 לְתוּשִׁיָּה כִּפְלַיִם; ritkán főnevek után, 2Krón 16:8; 21:3; 3:8 לְכִכָּרִים, 3:9; 3:11; Ezsd 8:26 (ahol a korábbi nyelv értelmezői szerkezetet vagy a meghatározás tárgyesetét használná, Dr^§ 194). (c) némileg másként, 3Móz 5:4b és vétkessé lesz מֵאֵלָּה לְאַחַת ezek közül valamelyik dolog tekintetében, 5:5; 22:5b; 4Móz 18:7 (vö. 1Krón 26:32; 27:1; 2Krón 19:11 (a versben kétszer)) Jer 2:37 (sajátos) nem leszel szerencsés להם velük kapcsolatban, Ez 44:14, vö. Jób 9:19; főnév után 1Móz 47:26 לַחֹמֶשׁ (de vö. ᵐ5 Di) az ötödrészre vonatkozóan, 3Móz 7:26; 11:46b 4Móz 19:11; 29:39; 30:13; 5Móz 19:15; 23:19; Ezsd 8:34; 1Krón 27:1 (ח ׳לכל), 2Krón 8:15; Neh 11:24. (d) ֗֗֗ לְכֹל לְכָלֿׅ), leírás vagy felsorolás végén, általánosító erővel: ami mindent illet ... = tudniillik, röviden (Ew^§ 310 a ), főként P-ben és a Krónikákban (valószínűleg jogi szóhasználat): 1Móz 9:10b mindaz, ami kijön a bárkából, הָאָרֶץ חַיַּת לְכֹל ami ( = tudniillik, sőt) a föld minden vadját illeti, 23:10b; 2Móz 14:28 (vö. 14:9 וְ), 27:3, 19; 28:38; 30:1b; 3Móz 5:3-4, (vö. 13:51) 11:42; 16:16, 21; 22:18; 4Móz 3:26b (3:31 3:36 וְ), 4:27, 31, 32; 5:9; 18:4, 8, 9, 11 (mind P), 2Kir 12:6; Jer 19:13; Ez 44:9; 1Krón 13:1; 2Krón 5:12 (לְכֻלָּם), 25:5; 31:16; 33:8 b (|| 2Kir 21:8 ולכל) Ezsd 1:5. (e) új alanyt bevezetve (ritka, és a szöveg néha kétséges; főként a Krónikákban): ami ...-t illeti, Ézs 32:1 ולשׂרים (valószínűleg olv. ל וְשָׂרִים, a következő למשׁפט miatti tévedésből), 3Móz 11:26; 1Krón 3:2 (valószínűleg olv. אבשׁלום), 5:2 ( ? l. Ke), 7:1 (Ke ובני), 7:5 a (?), 24:1; 26:1, 23, 25, 26, 31 a B 2Krón 5:12; 7:21 ישׁרק עליו לְכָלע־ֹבֵר (|| 1Kir 9:8 כָּלעֹֿבֵר), vö. 5Móz 24:5 (sajátos); Préd 9:4 וג ׳טוב הוא חַי לְכֶלֶב בִּי; vö. Zsolt 17:4 (a 16:3-hoz l. a kommentárokat). A Krónikákban néha sajátosan körülírásként használatos, 1Krón 28:1 b. 21 נדיב לכל ami minden készséges embert illet = minden készséges ember (vö. Ke), 29:5 a.

**25.** 

> 6 b; compare Ezra 6:7 (Aramaic), 7:28.

6 b; vö. Ezsd 6:7 (arámi), 7:28.

**26.** 

> f. in connection with terms designating a cause or occasion, with referenceto or in view of (German auf. . .hin) becomes nearly equivalent to on account of, through (not common): so to cut oneself לָנֶפֶשׁ Lev 19:28 on account of a (dead) person, Deut 14:1; Jer 16:6b, Lev 11:24 תִּטַּמָּ֑אוּ לְאֵלֶּה on account of these ye shall become unclean, 21:1-2, 3 +, Ezek 20:31 לְ נִטְמָא, Num 5:2 לָנֶפֶשׁ כָּלטָֿמֵא 9:6-7, 10, compare 2Chr 23:19; י ׳לְשֵׁם in view of (i.e. determined by), because of ׳יs name, Joel 9:9; Jer 3:17; Isa 55:5 (|| לְמַעַן), Ezek 36:22 (do.); Gen 4:23 a I have slain a man לְפִצְעִי because of my wound, 4:23 b Exod 4:26 לַמּוּלוֺת, Num 35:33 לָכֵן לַדָּם = therefore (synonym כֵּן עַל), constantly (see כֵּן); Job 30:24 (si vera lectio) לָהֶן: of the cause of an emotion, Isa 15:5 יִזְעַק לְמוֺאָב לִבִּי because of Moab 16:7, 11; Jer 31:20 לוֺ מֵעַי הָמוּ (עַלּ Song 5:4), Hosea 10:5, לְזֹאת Job 37:1. compare Num 16:34 לקולם נסו fled at the sound of them, Ezek 27:28; Hab 3:16; Psa 42:8.

f. okot vagy alkalmat jelölő kifejezésekkel kapcsolatban a valamire vonatkozóan vagy valamire tekintettel (német auf...hin) jelentés szinte = valami miatt, valami által (nem gyakori): így megvagdosni magát לָנֶפֶשׁ 3Móz 19:28 egy (halott) személy miatt, 5Móz 14:1; Jer 16:6b, 3Móz 11:24 תִּטַּמָּ֑אוּ לְאֵלֶּה ezek miatt lesztek tisztátalanok, 21:1-2, 3 és máshol, Ez 20:31 לְ נִטְמָא, 4Móz 5:2 לָנֶפֶשׁ כָּלטָֿמֵא 9:6-7, 10, vö. 2Krón 23:19; י ׳לְשֵׁם valamire tekintettel (azaz valami által meghatározva), ׳י neve miatt, Jóel 9:9; Jer 3:17; Ézs 55:5 (|| לְמַעַן), Ez 36:22 (ua.); 1Móz 4:23 a megöltem egy férfit לְפִצְעִי sebemért, 4:23 b 2Móz 4:26 לַמּוּלוֺת, 4Móz 35:33 לָכֵן לַדָּם = ezért (szinonimája כֵּן עַל), állandóan (l. כֵּן); Jób 30:24 (si vera lectio) לָהֶן: érzelem okáról, Ézs 15:5 יִזְעַק לְמוֺאָב לִבִּי Moáb miatt 16:7, 11; Jer 31:20 לוֺ מֵעַי הָמוּ (עַלּ Én 5:4), Hós 10:5, לְזֹאת Jób 37:1. vö. 4Móz 16:34 לקולם נסו elmenekültek kiáltásukra, Ez 27:28; Hab 3:16; Zsolt 42:8.

**27.** 

> g. marking the aim, object, or consequence of an action or thing, in view of, for, unto: (a) Gen 1:16 היום לממשׁלת for the rule of the day, 22:7 where is the sheep לְעוֺלָה? 42:25 provision לַדָּ֑רֶךְ for the way; Exod 20:7 לַשָּׁוְא i.e. for a vain or frivolous purpose, similarly לָרִיק and לַשֶּׁקֶר; Lev 1:3 + לִרְצֹּנוֺ for his acceptance; Num 21:23 and often למלחמה יצא for battle; לְ יָשַׁב to sit (wait) for, Exod 24:14; Hosea 3:3; Jer 3:2; 1Sam 8:16 to use לִמְלַאכְתּוֺ for his business; 2Sam 15:2 + לַמִּשְׁמָּט בָּא for judgment; Psa 69:22 לִצְמָאִי for (i.e. to quench) my thirst, Neh 9:15; Exod 29:36 + לַיּוֺם for each day; Isa 4:3 לַחַיִּים כָּלכָּֿתוכ for life; Hosea 9:4 לְנַפְשָׁם לַחְמָם; לרעה and לטובה Jer 21:10 +; Isa 58:4; Psa 63:10 נפשׁי יבקשׁו ׃לְשׁוֺאָה in the sense of to secure, compass, Gen 41:55 cried to Phoenician לַלָּ֑חֶם for bread, 1Sam 2:36; Amos 8:11; Job 15:23; Isa 10:3: so in לִמַעַן for the purpose of; and with an infinitive often (see 7a). (b) corresponding to the Latin dativus commodi [dative of benefit], (a) with verbs, Gen 2:18 לו אעשׂה I will make for him, etc., 2:20; 3:21, etc., absolute לְ עָשָׂה 1Sam 14:6; Isa 64:3, לְ מָּעַל Psa 68:29; לְ מָצָא Gen 8:9; לְ לָקַח 24:3-4, + often; נוּד לְ, סָפַד Jer 16:5-6, לְ בָּכָה 22:10, etc.; Judg 16:25 וִישַׂחֶקלָֿנוּ to sport for us (for our pleasure); Hosea 2:25; Micah 5:1, etc.; with a pronoun of the same person as the verb, as 1Kin 20:34 לך תשׂים, 2Kin 6:7; 10:24; Zech 9:13, leading on to h a, below; often with pronouns and imperative, Num 11:16 אֶסְפָהלִּֿי gather me70men, 22:6 אָרָהלִּֿי curse me this people, 23:1 לִי בְּנֵה, 1Kin 1:28 לבתשֿׁבע לי קראו call me B., 3:24; 13:13; 17:10; Song 2:15 לָנוּ אֶחֱזוּ catch us the foxes, Isa 49:20 גְּשָׁהלִּֿי retire for me, that I may dwell, 2Sam 18:5 לַנַּעַר לִי לְאַט (act) Gently ( 5i b) for my sake towards the young man, 2Kin 4:24 לִרְכֹּב אַלתַּֿעֲצָרלִֿי AV slacken me not the riding;

g. egy cselekvés vagy dolog célját, tárgyát vagy következményét jelölve: valamire tekintettel, valamiért, valamire: (a) 1Móz 1:16 היום לממשׁלת a nappal uralására, 22:7 hol a bárány לְעוֺלָה? 42:25 לַדָּ֑רֶךְ útravaló; 2Móz 20:7 לַשָּׁוְא azaz hiábavaló vagy könnyelmű célra, hasonlóan לָרִיק és לַשֶּׁקֶר; 3Móz 1:3 és máshol לִרְצֹּנוֺ kedves elfogadtatására; 4Móz 21:23 és gyakran למלחמה יצא a harcra; לְ יָשַׁב ülni (várni) valakire, 2Móz 24:14; Hós 3:3; Jer 3:2; 1Sám 8:16 használni לִמְלַאכְתּוֺ a maga munkájára; 2Sám 15:2 és máshol לַמִּשְׁמָּט בָּא ítéletre; Zsolt 69:22 לִצְמָאִי szomjúságomra (azaz szomjúságom oltására), Neh 9:15; 2Móz 29:36 és máshol לַיּוֺם minden napra; Ézs 4:3 לַחַיִּים כָּלכָּֿתוכ életre; Hós 9:4 לְנַפְשָׁם לַחְמָם; לרעה és לטובה Jer 21:10 és máshol; Ézs 58:4; Zsolt 63:10 נפשׁי יבקשׁו ׃לְשׁוֺאָה valaminek a megszerzése, elérése értelmében, 1Móz 41:55 kiáltott a föníciaihoz לַלָּ֑חֶם kenyérért, 1Sám 2:36; Ámós 8:11; Jób 15:23; Ézs 10:3: így a לִמַעַן kifejezésben: azzal a céllal; és infinitivusszal gyakran (l. 7a). (b) a latin dativus commodinak [érdekeltségi részes eset] megfelelően, (a) igékkel, 1Móz 2:18 לו אעשׂה alkotok neki stb., 2:20; 3:21 stb., abszolút használatban לְ עָשָׂה 1Sám 14:6; Ézs 64:3, לְ מָּעַל Zsolt 68:29; לְ מָצָא 1Móz 8:9; לְ לָקַח 24:3-4, és gyakran máshol; נוּד לְ, סָפַד Jer 16:5-6, לְ בָּכָה 22:10 stb.; Bír 16:25 וִישַׂחֶקלָֿנוּ hogy mulattasson minket (a mi kedvünkre); Hós 2:25; Mik 5:1 stb.; az igével azonos személyű névmással, mint 1Kir 20:34 לך תשׂים, 2Kir 6:7; 10:24; Zak 9:13, ami átvezet a lenti h a-hoz; gyakran névmásokkal és imperativusszal, 4Móz 11:16 אֶסְפָהלִּֿי gyűjts nekem 70 férfit, 22:6 אָרָהלִּֿי átkozd meg nekem ezt a népet, 23:1 לִי בְּנֵה, 1Kir 1:28 לבתשֿׁבע לי קראו hívd ide nekem B.-t, 3:24; 13:13; 17:10; Én 2:15 לָנוּ אֶחֱזוּ fogjátok meg nekünk a rókákat, Ézs 49:20 גְּשָׁהלִּֿי húzódj félre nekem, hogy lakhassam, 2Sám 18:5 לַנַּעַר לִי לְאַט (bánjatok) kíméletesen ( 5i b) az én kedvemért az ifjúval, 2Kir 4:24 לִרְכֹּב אַלתַּֿעֲצָרלִֿי AV slacken me not the riding;

**28.** 

> (β) with substantives, e.g. in such phrases as לי ׳הוא פסח Exod 12:11 a passover is it unto ׳י, 13:6 לי ׳חַג, 16:25 לי ׳שַׁבָּת, Isa 23:18 + לי ׳קֹדֶשׁ, Lev 1:9 and often לי נִיחוֺחַ רֵיחַ ׳אִשֵּׂה, 1Sam 1:3 לי ׳כהנים, etc.;

(β) főnevekkel, pl. olyan kifejezésekben, mint לי ׳הוא פסח 2Móz 12:11 páska ez ׳י tiszteletére, 13:6 לי ׳חַג, 16:25 לי ׳שַׁבָּת, Ézs 23:18 és máshol לי ׳קֹדֶשׁ, 3Móz 1:9 és gyakran לי נִיחוֺחַ רֵיחַ ׳אִשֵּׂה, 1Sám 1:3 לי ׳כהנים stb.;

**29.** 

> (γ) also as a dativus incommodi [dative of harm], as to lie in wait, lay snares, dig a pit, etc., for any one, Judg 9:25; 16:2; Psa 35:7; 57:7 etc.; with verbs of withholding or removing (rare), Judg 17:2 לָךְ לֻקַּח 1Sam 21:6 (compare ) Psa 40:11; 84:12; Job 12:20; note also the phrase לְ (הַמַּעְבָּרוֺת) הַמַּיִם לָכַד Judg 3:28 (RV), 7:24; 12:5: ל זכר, in both senses, to remember for (in one's favour) Jer 2:2 +, against Psa 137:7 +, compare לְ גער Mal 3:11; and 2:3. (c) more distinctly on behalf of, as with קִנֵּא to be jealous for, Num 11:29 +, נִלְחַם Deut 3:22 +, שָׁמֶר 7:12 +, לְ רָב to contend for Judg 6:31, יָרֵא Josh 9:24, הִתְמַּלֵּל 1Sam 2:25 +, דִּבֶּר to speak for one 2Kin 4:13; Job 13:7 הַלְאֵל עַוְלָה תְּדַבְּרוּ will ye speak wickedness on God's behalf ? שָׁאַל to ask 1Sam 22:13 +, עָבַר to pass over for ( = to pardon) Amos 7:8; Deut 30:12 לנו יעלה מי, 30:13; Judg 1:1; 20:18; Isa 6:8 יֵלֶךְלָֿנוּ מִי; see also Exod 2:19; 4:16 a Num 35:31; Deut 23:6; Josh 18:6; Judg 5:13; 7:4, 20; 2Sam 15:34b Isa 33:21; Prov 16:26; 31:8, etc.; Psa 94:16 מְרֵעִים עִם לִי יָקוּם מִי; ל ׳היה to be on one's side, Hosea 1:9 לכם אהיה לא ואנכי, Psa 124:1; 124:2, and without היה Gen 31:42; Exodus 32:36, ל ׳מִי אֵלַי who is on ׳יs side ? (let him come) to me ! Josh 5:13b 2Sam 20:11; 2Kin 10:6 אַתֶּם לִי אִם (synonym אִתִּי 9:32), Psa 56:10 י כי ידעתי ׳זה לי, 118:6; 118:7 ׳י לִי.

(γ) dativus incommodiként [kárvallotti részes eset] is, mint leselkedni, csapdát állítani, vermet ásni stb. valakinek, Bír 9:25; 16:2; Zsolt 35:7; 57:7 stb.; a visszatartás vagy elvétel igéivel (ritka), Bír 17:2 לָךְ לֻקַּח 1Sám 21:6 (vö. ) Zsolt 40:11; 84:12; Jób 12:20; figyeld meg még a לְ (הַמַּעְבָּרוֺת) הַמַּיִם לָכַד kifejezést Bír 3:28 (RV), 7:24; 12:5: ל זכר, mindkét értelemben: emlékezni valakinek (javára) Jer 2:2 és máshol, valaki ellen Zsolt 137:7 és máshol, vö. לְ גער Mal 3:11; és 2:3. (c) kifejezettebben: valaki érdekében, mint קִנֵּא buzgólkodni valakiért, 4Móz 11:29 és máshol, נִלְחַם 5Móz 3:22 és máshol, שָׁמֶר 7:12 és máshol, לְ רָב perlekedni valakiért Bír 6:31, יָרֵא Józs 9:24, הִתְמַּלֵּל 1Sám 2:25 és máshol, דִּבֶּר szólni valakiért 2Kir 4:13; Jób 13:7 הַלְאֵל עַוְלָה תְּדַבְּרוּ gonoszságot akartok-e szólni Isten érdekében? שָׁאַל kérdezni 1Sám 22:13 és máshol, עָבַר elnézni valakinek ( = megbocsátani) Ámós 7:8; 5Móz 30:12 לנו יעלה מי, 30:13; Bír 1:1; 20:18; Ézs 6:8 יֵלֶךְלָֿנוּ מִי; l. még 2Móz 2:19; 4:16 a 4Móz 35:31; 5Móz 23:6; Józs 18:6; Bír 5:13; 7:4, 20; 2Sám 15:34b Ézs 33:21; Péld 16:26; 31:8 stb.; Zsolt 94:16 מְרֵעִים עִם לִי יָקוּם מִי; ל ׳היה valaki oldalán lenni, Hós 1:9 לכם אהיה לא ואנכי, Zsolt 124:1; 124:2, és היה nélkül 1Móz 31:42; 2Móz 32:36, ל ׳מִי אֵלַי ki van ׳י oldalán? (jöjjön) hozzám! Józs 5:13b 2Sám 20:11; 2Kir 10:6 אַתֶּם לִי אִם (szinonimája אִתִּי 9:32), Zsolt 56:10 י כי ידעתי ׳זה לי, 118:6; 118:7 ׳י לִי.

**30.** 

> h. used reflexively (the 'ethical' dative, or dative of feeling), throwing the action back upon the subject, and expressing with some pathos the interest, or satisfaction, or completeness, with which it is (or is to be) accomplished, especially (but not exclusively) with imperative and I person imperfect (often not expressible in English, sometimes to be expressed by a paraphrase); — (a) with transitive verbs (a choice idiom, a development of g b a, common, especially with imperative, in best prose), לְךָ עֲשֵׂה Gen 6:14; Num 21:8 + often, לָכֶם עֲשִׂיתֶם Deut 4:16, 23; 9:16; Amos 5:26, לָהֶם וַיַּעֲשׂוּ Gen 3:7; Exod 32:31; Hosea 13:2; Jer 11:17 the evil which להם עשׂו they have loved to do (compare Hi), Gen 11:4; Judg 3:16; 2Sam 15:1, etc.; לָכֶם קְחוּ קַחלְֿךָ, Gen 6:21 + often, לו ויקח 15:10, etc.; לוֺ בָּזַז Deut 2:35; 20:14 +; לָכֶם תְּנוּ Exod 7:9; Josh 20:2; לָכֶם הָבוּ Deut 1:13 (compare Dr) +, לָכֶם שִׂימוּ Judg 19:30, compare 2Kin 10:24; Hosea 2:2; לָכֶם בַּחֲרוּ לוֺ, בָּחַר, etc Gen 13:11; 2Sam 17:1 ᵐ5 (see Dr) + often; לְךָ קְנֵה Jer 32:7 +, לְךָ דַּע Job 5:27, compare Song 1:8; Deut 10:1 (twice in verse); 16:9, 13, 18; 19:2-3, 9, Josh 22:23 לָנוּ לִבְנוֺת, 1Sam 20:20 לְמַטָּרָה לִי לְשַׁלַּח, 2Kin 4:3 לָךְ שַׁאֲלִי (compare Isa 7:11), Isaiah 18:23; 44:7 לָמוֺ יַגִּידוּ, 59:8 לָהֶם עִקְּשׁוּ, Jer 2:13; 22:14 אֶבְנֶהלִּֿי, 31:21; 46:14; Hosea 10:1 יְשַׁוֶּהלּֿוֺ מְּרִי maketh fruit freely, 10:11; 10:12; 10:12; Amos 6:5, 13; Psa 44:11 לָמוֺ שָׁסוּ = plunder at their will, 64:6; 83:13; Prov 1:22; Eccl 8:12 לוֺ מַאֲרִיךְ (denoting satisfaction), Job 7:3 לִי הָנְחַלְתִּי, 12:11 לוֺ יִטְעַם, 13:1 וַתָּבֶןלָֿהּ, 24:16, etc.: rarely separated from the verb, Hosea 12:9; Prov 23:20; Job 3:14. (b) with verbs of motion, Gen 12:1; 22:2 לֶךְלְֿךָ get thee away, 27:43 לְךָ בְרַח Amos 7:12; Num 22:34 לי אשׁובה literally I will return for myself, Deut 1:7 (compare Dr) לָכֶם סְעוּ, 1:40; 2:13 לכם עברו, 5:27 לכם שׁובו, 1Sam 22:5; 26:11 לָנוּ וְנֵָֽלְכָה, 26:12 לָהֶם וַיֵּלְכוּ, 2Sam 2:21 לְךָ נְטֵה, 2:22; 1Kin 17:3; Isa 31:8 לוֺ נָס, 40:9 לָךְ עֲלִי Jer 5:5 לִי ֵאלְכָה, Hosea 8:9 a wild ass לוֺ כֹּדֵד going alone at its pleasure, Micah 1:11; Psa 58:8 למו יתהלכו כמים that run apace, Prov 20:14 לִוֺ אֹזֵל = goeth his way, Job 39:4; Song 1:8; b 2:10-11, 13; 4:6. (c) with neuter verbs, especially those signifying a state of mind or feeling (chiefly in poetry), Psa 66:7 למו ירומו אל, 80:7 למו ילעגו mock as they please, 120:6 נַפְשִׁי לָהּ שָֽׁכְנָה רַבַּת has had her dwelling with, etc., 122:3 לָהּ שֶׁחֻבְּרָה is well compacted, 123:4 לָהּ שָֽׂבְעָה is but too full, Isa 2:22 לָכֶם חִדְלוּ, 2Chr 25:16; 35:21; Jer 7:4 לָכֶם אַלתִּֿבְטְחוּ, 7:8; 2Kin 18:21; Ezek 37:11 לָנוּ נִגְזַרְנוּ we are quite cut off, Job 6:19 לָמוֺ קִוּוּ (implying that they fed themselves on hope), 15:28 לָמוֺ שְׁבוּ יֵ which should not sit (be inhabited), 19:29 לָכֶם גּוּרוּ, Song 2:17; 8:14 לְךָ דְּמֵה, and the frequent הִשָּׁמֶרלְֿךָ take heed to thyself Gen 24:6 +; with an adjective, Amos 2:13 עָמִיר לָהּ הַמְּלֵאָה. (compare Ew^§ 315 a. Very common in Syriac, especially b: Nö^§ 224.)

h. visszahatóan használva (az 'etikai' részes eset, vagy az érzelmi részes eset), amely a cselekvést visszaveti az alanyra, és bizonyos pátosszal kifejezi azt az érdeklődést, elégedettséget vagy teljességet, amellyel a cselekvés végbemegy (vagy végbe kell mennie), különösen (de nem kizárólag) imperativusszal és első személyű imperfectummal (angolul gyakran nem fejezhető ki, néha körülírással adható vissza); — (a) tárgyas igékkel (választékos szólásmód, a g b a továbbfejlődése, gyakori, különösen imperativusszal, a legjobb prózában), לְךָ עֲשֵׂה 1Móz 6:14; 4Móz 21:8 és gyakran máshol, לָכֶם עֲשִׂיתֶם 5Móz 4:16, 23; 9:16; Ámós 5:26, לָהֶם וַיַּעֲשׂוּ 1Móz 3:7; 2Móz 32:31; Hós 13:2; Jer 11:17 a gonoszság, amelyet להם עשׂו szerettek cselekedni (vö. Hi), 1Móz 11:4; Bír 3:16; 2Sám 15:1 stb.; לָכֶם קְחוּ קַחלְֿךָ, 1Móz 6:21 és gyakran máshol, לו ויקח 15:10 stb.; לוֺ בָּזַז 5Móz 2:35; 20:14 és máshol; לָכֶם תְּנוּ 2Móz 7:9; Józs 20:2; לָכֶם הָבוּ 5Móz 1:13 (vö. Dr) és máshol, לָכֶם שִׂימוּ Bír 19:30, vö. 2Kir 10:24; Hós 2:2; לָכֶם בַּחֲרוּ לוֺ, בָּחַר stb. 1Móz 13:11; 2Sám 17:1 ᵐ5 (l. Dr) és gyakran máshol; לְךָ קְנֵה Jer 32:7 és máshol, לְךָ דַּע Jób 5:27, vö. Én 1:8; 5Móz 10:1 (a versben kétszer); 16:9, 13, 18; 19:2-3, 9, Józs 22:23 לָנוּ לִבְנוֺת, 1Sám 20:20 לְמַטָּרָה לִי לְשַׁלַּח, 2Kir 4:3 לָךְ שַׁאֲלִי (vö. Ézs 7:11), Ézs 18:23; 44:7 לָמוֺ יַגִּידוּ, 59:8 לָהֶם עִקְּשׁוּ, Jer 2:13; 22:14 אֶבְנֶהלִּֿי, 31:21; 46:14; Hós 10:1 יְשַׁוֶּהלּֿוֺ מְּרִי bőven hoz gyümölcsöt, 10:11; 10:12; 10:12; Ámós 6:5, 13; Zsolt 44:11 לָמוֺ שָׁסוּ = kedvük szerint fosztogatnak, 64:6; 83:13; Péld 1:22; Préd 8:12 לוֺ מַאֲרִיךְ (elégedettséget jelölve), Jób 7:3 לִי הָנְחַלְתִּי, 12:11 לוֺ יִטְעַם, 13:1 וַתָּבֶןלָֿהּ, 24:16 stb.: ritkán elválasztva az igétől, Hós 12:9; Péld 23:20; Jób 3:14. (b) mozgást jelentő igékkel, 1Móz 12:1; 22:2 לֶךְלְֿךָ menj el, 27:43 לְךָ בְרַח Ámós 7:12; 4Móz 22:34 לי אשׁובה szó szerint: visszatérek magamnak, 5Móz 1:7 (vö. Dr) לָכֶם סְעוּ, 1:40; 2:13 לכם עברו, 5:27 לכם שׁובו, 1Sám 22:5; 26:11 לָנוּ וְנֵָֽלְכָה, 26:12 לָהֶם וַיֵּלְכוּ, 2Sám 2:21 לְךָ נְטֵה, 2:22; 1Kir 17:3; Ézs 31:8 לוֺ נָס, 40:9 לָךְ עֲלִי Jer 5:5 לִי ֵאלְכָה, Hós 8:9 vadszamár לוֺ כֹּדֵד, amely kedve szerint magában jár, Mik 1:11; Zsolt 58:8 למו יתהלכו כמים amelyek sebesen futnak, Péld 20:14 לִוֺ אֹזֵל = elmegy a maga útján, Jób 39:4; Én 1:8; b 2:10-11, 13; 4:6. (c) tárgyatlan igékkel, különösen olyanokkal, amelyek lelkiállapotot vagy érzelmet jelölnek (főként a költészetben), Zsolt 66:7 למו ירומו אל, 80:7 למו ילעגו kedvük szerint gúnyolódnak, 120:6 נַפְשִׁי לָהּ שָֽׁכְנָה רַבַּת lakott ... mellett stb., 122:3 לָהּ שֶׁחֻבְּרָה jól össze van építve, 123:4 לָהּ שָֽׂבְעָה bizony túlságosan is tele van, Ézs 2:22 לָכֶם חִדְלוּ, 2Krón 25:16; 35:21; Jer 7:4 לָכֶם אַלתִּֿבְטְחוּ, 7:8; 2Kir 18:21; Ez 37:11 לָנוּ נִגְזַרְנוּ egészen elvágattunk, Jób 6:19 לָמוֺ קִוּוּ (arra utalva, hogy reménységből táplálkoztak), 15:28 לָמוֺ שְׁבוּ יֵ amelyekben nem kellene lakni (amelyek nem lakottak), 19:29 לָכֶם גּוּרוּ, Én 2:17; 8:14 לְךָ דְּמֵה, és a gyakori הִשָּׁמֶרלְֿךָ vigyázz magadra 1Móz 24:6 és máshol; melléknévvel, Ámós 2:13 עָמִיר לָהּ הַמְּלֵאָה. (vö. Ew^§ 315 a. Nagyon gyakori a szírben, különösen b: Nö^§ 224.)

**31.** 

> i. of reference to a norm or standard, according to, after, by: — (a) Gen 1:11 +?לְמִינוֺ according to its kinds, 8:19 + לְמִשְׁמְּחֹתֵיהֶם according to their families, 10:5 לִלְשֹׁנוֺ נִישׁ, 10:31; 10:32, Exod 30:12 + לִפְפְקֻדֵיהֶם according to them that are numbered of them, Num 1:2 אֲבוֺתָם לְבֵית by their fathers' houses, 1:2 לְגֻלְגְּלֹתָם 1:3 לְצִבְאֹתָם, 1:20 + often, especially in enumerations and classifications; Gen 13:3 Abram went לְמַסָּעָיו by his journeyings (stages), so לְמַסְעֵיהֶם Exod 17:1 +; Gen 13:17 go through the land וּלְרָחְבָּהּ לְאָרְכָּהּ according to (i.e. to the full extent of) its length and breadth (compare Hab 1:6); Hab 41:47 לִקְמָצִים by handfuls, Num 24:2 + לִשְׁבָטָיו by its tribes, 1Sam 29:2 ולאלפים למאות עברים by hundreds and thousands, 2Sam 18:4, לְעָרֶיהָ Num 32:33; Josh 18:9; Judg 19:19 לַעֲצָמֶיהָ according to her bones (i.e. limb by limb), Ezek 24:6 לִנְתָחֶיהָ piece by piece; Psa 140:12 to hunt לְמַדְחֵפוֺת thrust-wise, with thrust upon thrust, Isa 27:12 אֶחָד לְאַחַד (Ges Ew) by one, one (i.e. one by one); hence, especially with plurals, it acquires sometimes a distributive force, as לִבְקָרִים 33:2 by mornings = every morning (compare 6), so לַבְּקָרִים Psa 73:14; 101:8 +, לִרְגָעִים Isa 27:3 + every moment, לֶחֳדָשִׁים 47:13 every month, Ezek 47:12; 1Kin 10:22 שָׁנִים לְשָׁלוֺשׁ אַחַת once every three years, Amos 4:4 ימים לשׁלשׁת every three days (but see We), 1Chr 9:25; in Chronicles ועיר לעיר ושׁער לשׁער, 2Chr 8:14; 19:5; 26:11. (b) denoting the principle, with regard to which an act is done, לְמִסְמַּר according to the number of . . . Deut 32:8; Judg 21:23 +, Isa 11:3 to judge אָזְנָיו לְמִשְׁמַע עֵינָיו לְמַרְאֵה according to that which his eyes see, his ears hear (compare Lev 13:12; Job 42:5), 28:26; 32:1 a king will regin לְצֶדֶק according to justice (|| לְמשׁפט), 42:3 לֶאֱמֶת = faithfully, Jer 9:2 לֶאֱמוּנָה = honestly, 15:15; 30:11 (= 46:28) לַמִּשְׁמָּט וְיִסַּרְתִּיךָ (synonym 10:24 בְּמשׁפט), Hosea 2:12 (|| לְפִי), Joel 2:23 לִצֶדָקָה; Gen 38:24 pregnant לִזְנוּנִים = unchastely, Num 15:24 לשׁגגה by error (elsewhere בשׁגגה), 2Chr 30:3; 35:8; Song 7:10 flowing down למישׁרים straightly (Prov 23:31 ׳ב), לָרֹב Job 26:3; 2Chr 14:14, in poetry לְמַכְבִּיר Job 36:31 in abundance, לְאַט = gently 2Sam 18:5 +; Exod 16:3; Psa 78:25 לָשׂבַע according to satiety; לְרֶגֶל according to the foot (pace) of Gen 33:14 + (see רֶגֶל); 1Sam 23:20 נַפְשְׁךָ לְכָלאַֿוַּת (Deut 12:15 and elsewhere ׳בְּ), 2Sam 15:11 לְתֻמָּם according to their simplicity, i.e. unsuspectingly (so 1Kin 22:34), 9:11 לְכָלחֶֿפְצוֺ, Isa 54:16; Ezek 22:6 לִזְרֹעוֺ, Job 12:5; Psa 119:91; 119:154 לְאִמְִרתְךָ (|| ׳כְּ 119:58; 119:116; 119:170), Eccl 1:10 long ago לְעולמים according to (measured by) the ages etc. (see Hi): so also in the phrase חֶרֶב לְפִי according to a sword's mouth, i.e. as the sword would devour, without quarter, Josh 6:21 + often; ֗֗֗ לְפִי itself also, in various figurative applications, has the force of according to, Gen 47:12, etc. (see מֶּה); and in יָדְךָ לְאֵל (אֵין) יֵשׁ it is (not) according to the power of thy hand. Similarly Deut 11:11 הַשָּׁמַיִם לִמְטַר after the manner of the rain of heaven, i.e. as the rain permits (opposed to the artificial irrigation of 11:10), Judg 21:12 + זָכָר לְמִשְׁכַּב, Ezek 12:12 לַעַיִן i.e. as the eye sees it. j. designating a condition or state: לָבֶטַח in a state of confidence = confidently, Lev 25:18 + often; לְבַד לְבָדָד,, in a state of separation ( = a part), so לְבַדּוֺ (see pp. 94, 95); לְשָׁלוֺם Gen 44:17 +, לְפֶתַע suddenly Isa 29:5; 30:13; לִבְלִי in a condition of no . . . = without, 5:14 + (see בלי), so ֗֗֗ לְאֵין (late), לְלֹא2Chr 15:3; further Isa 1:5 לָחֳלִי in a state of sickness, 50:11 לְמַעֲצֵבָה, Psa 45:15 לִרְקָמוֺת, Ezra 2:63 = Neh 7:65 a priest ולתמים לאורים having relation to (i.e. with) Urim and Thummim, 2Chr 20:21 קֹדֶשׁ לְהַדְרַת = in holy adornment (compare ׳בְּ Psa 29:2; 96:9). And of a concomitant circumstance (German bei), in presence of, at, Job 29:3 לְאוֺרוֺ, Hab 3:11, ֗֗֗ לקול Job 21:12; Ezra 3:13. 6 Of time:

i. normára vagy mércére vonatkozóan: szerint, után, által: — (a) 1Móz 1:11 és máshol?לְמִינוֺ a maga neme szerint, 8:19 és máshol לְמִשְׁמְּחֹתֵיהֶם nemzetségeik szerint, 10:5 לִלְשֹׁנוֺ נִישׁ, 10:31; 10:32, 2Móz 30:12 és máshol לִפְפְקֻדֵיהֶם megszámláltjaik szerint, 4Móz 1:2 אֲבוֺתָם לְבֵית atyáik házai szerint, 1:2 לְגֻלְגְּלֹתָם 1:3 לְצִבְאֹתָם, 1:20 és gyakran máshol, különösen felsorolásokban és osztályozásokban; 1Móz 13:3 Abrám ment לְמַסָּעָיו útjain (szakaszonként), így לְמַסְעֵיהֶם 2Móz 17:1 és máshol; 1Móz 13:17 járd be a földet וּלְרָחְבָּהּ לְאָרְכָּהּ hossza és szélessége szerint (azaz teljes kiterjedésében) (vö. Hab 1:6); Hab 41:47 לִקְמָצִים marékszámra, 4Móz 24:2 és máshol לִשְׁבָטָיו törzsei szerint, 1Sám 29:2 ולאלפים למאות עברים százanként és ezrenként, 2Sám 18:4, לְעָרֶיהָ 4Móz 32:33; Józs 18:9; Bír 19:19 לַעֲצָמֶיהָ csontjai szerint (azaz tagról tagra), Ez 24:6 לִנְתָחֶיהָ darabonként; Zsolt 140:12 vadászni לְמַדְחֵפוֺת taszításról taszításra, Ézs 27:12 אֶחָד לְאַחַד (Ges Ew) egyenként, egyenként (azaz egyenként); innen, különösen többes számmal, néha disztributív erőt kap, mint לִבְקָרִים 33:2 reggelenként = minden reggel (vö. 6), így לַבְּקָרִים Zsolt 73:14; 101:8 és máshol, לִרְגָעִים Ézs 27:3 és máshol minden pillanatban, לֶחֳדָשִׁים 47:13 minden hónapban, Ez 47:12; 1Kir 10:22 שָׁנִים לְשָׁלוֺשׁ אַחַת háromévente egyszer, Ámós 4:4 ימים לשׁלשׁת háromnaponként (de l. We), 1Krón 9:25; a Krónikákban ועיר לעיר ושׁער לשׁער, 2Krón 8:14; 19:5; 26:11. (b) azt az elvet jelölve, amelyre tekintettel egy cselekvés történik, לְמִסְמַּר ... száma szerint 5Móz 32:8; Bír 21:23 és máshol, Ézs 11:3 ítélni אָזְנָיו לְמִשְׁמַע עֵינָיו לְמַרְאֵה aszerint, amit szemei látnak, amit fülei hallanak (vö. 3Móz 13:12; Jób 42:5), 28:26; 32:1 egy király uralkodik לְצֶדֶק igazság szerint (|| לְמשׁפט), 42:3 לֶאֱמֶת = hűségesen, Jer 9:2 לֶאֱמוּנָה = becsületesen, 15:15; 30:11 (= 46:28) לַמִּשְׁמָּט וְיִסַּרְתִּיךָ (szinonimája 10:24 בְּמשׁפט), Hós 2:12 (|| לְפִי), Jóel 2:23 לִצֶדָקָה; 1Móz 38:24 várandós לִזְנוּנִים = paráznaság révén, 4Móz 15:24 לשׁגגה tévedésből (máshol בשׁגגה), 2Krón 30:3; 35:8; Én 7:10 egyenesen למישׁרים lecsorgó (Péld 23:31 ׳ב), לָרֹב Jób 26:3; 2Krón 14:14, a költészetben לְמַכְבִּיר Jób 36:31 bőségben, לְאַט = kíméletesen 2Sám 18:5 és máshol; 2Móz 16:3; Zsolt 78:25 לָשׂבַע jóllakásig; לְרֶגֶל valakinek a lába (lépése) szerint 1Móz 33:14 és máshol (l. רֶגֶל); 1Sám 23:20 נַפְשְׁךָ לְכָלאַֿוַּת (5Móz 12:15 és máshol ׳בְּ), 2Sám 15:11 לְתֻמָּם együgyűségük szerint, azaz gyanútlanul (így 1Kir 22:34), 9:11 לְכָלחֶֿפְצוֺ, Ézs 54:16; Ez 22:6 לִזְרֹעוֺ, Jób 12:5; Zsolt 119:91; 119:154 לְאִמְִרתְךָ (|| ׳כְּ 119:58; 119:116; 119:170), Préd 1:10 régen לְעולמים a korszakok szerint (mérve) stb. (l. Hi): így a חֶרֶב לְפִי kifejezésben is: a kard szája szerint, azaz ahogy a kard fal, kegyelem nélkül, Józs 6:21 és gyakran máshol; maga a ֗֗֗ לְפִי is különféle átvitt alkalmazásokban szerint jelentésű, 1Móz 47:12 stb. (l. מֶּה); és a יָדְךָ לְאֵל (אֵין) יֵשׁ kifejezésben: (nem) kezed ereje szerint való. Hasonlóképpen 5Móz 11:11 הַשָּׁמַיִם לִמְטַר az ég esője módján, azaz ahogy az eső engedi (szemben a 11:10 mesterséges öntözésével), Bír 21:12 és máshol זָכָר לְמִשְׁכַּב, Ez 12:12 לַעַיִן azaz ahogy a szem látja. j. állapotot vagy helyzetet jelölve: לָבֶטַח biztonság állapotában = biztonságban, 3Móz 25:18 és gyakran máshol; לְבַד לְבָדָד,, elkülönítettség állapotában ( = külön), így לְבַדּוֺ (l. 94., 95. o.); לְשָׁלוֺם 1Móz 44:17 és máshol, לְפֶתַע hirtelen Ézs 29:5; 30:13; לִבְלִי a ... hiányának állapotában = nélkül, 5:14 és máshol (l. בלי), így ֗֗֗ לְאֵין (késői), לְלֹא2Krón 15:3; továbbá Ézs 1:5 לָחֳלִי betegség állapotában, 50:11 לְמַעֲצֵבָה, Zsolt 45:15 לִרְקָמוֺת, Ezsd 2:63 = Neh 7:65 egy pap ולתמים לאורים az Urimmal és Tummimmal kapcsolatban (azaz velük), 2Krón 20:21 קֹדֶשׁ לְהַדְרַת = szent ékességben (vö. ׳בְּ Zsolt 29:2; 96:9). Kísérő körülményről is (német bei): valaminek a jelenlétében, valaminél, Jób 29:3 לְאוֺרוֺ, Hab 3:11, ֗֗֗ לקול Jób 21:12; Ezsd 3:13. 6 Időről:

**32.** 

> a. towards, against, sometimes with collateral idea of in view of, much rarer than בְּ, but expressing concurrence (at) rather than duration (in): Gen 3:8 הַיּוֺם לְרוּחַ at the breeze of the day, לְעֵת in various connections, as עֶרֶב לְעֵת 8:11 + (see עֵת); מְזֻמָּנִים לְעִתִּים Ezra 10:14; Neh 10:35; בַּצָּרָה לְעִתּוֺת Psa 9:10; 10:1; ֗֗֗ לְיוֺם at, on the day of, 81:4; Prov 7:20 +, ֗֗֗ לְיוֺם תעשׂו מה Isa 10:3; Hosea 9:5 (compare Jer 5:31); ֗֗֗ אֲשֶׁר לַיָּמִים Ezek 22:14; ֗֗֗ אֲשֶׁר לַיּוֺם Mal 3:17; השׁנה לתשׁובת 2Sam 11:1 +; הימים לתקופת 1Sam 1:20, השׁנה לתקופת2Chr 24:23 (Exod 34:22 without לְ), (יָמִיםׅ שָׁנִים לְקֵץ (late) 2Chr 18:2; Neh 13:6; Dan 11:6, 13 (in early Hebrew יָמִים מִקֵּץ); ֗֗֗ לשׁנת2Chr 15:10; לַבֹּקֶר Psa 30:6; 49:15 + (Exod 34:2 after נָכוֺן הֱיֵה = against, for; compare 19:11; Prov 21:31); (לַבְּקָרִים Isa 33:2, see 5i); לערב Gen 49:27 (|| בבקר) +; לְמָחָר Exod 8:6 (in answer to 8:5 לְמָתַי), 8:19; Est 5:12 (Num 11:18; Josh 7:13 after הִתְקַדְּשׁוּ = against), לַמָּחֳרָת Jonah 4:7 (compare 1Chr 29:21); לָאוֺר Job 24:14; ֗֗֗ לְמוֺעֵד לַמּוֺעֵד,, Gen 17:21; Exod 23:15 +; לְפָנִים and לִפְנֵי before (often); לְאָחוֺר hereafter, Isa 41:23; 42:23; Psa 32:6 b; with infinitive (rare), in the phrase (עֶרֶבׅ (הַ)בֹּקֶר לִפְנוֺת Gen 24:63 +, 2Sam 18:29; Isa 7:15 לְדַעְתּוֺ when he knoweth.

a. valami felé, valamire, néha azzal a mellékgondolattal, hogy valamire tekintettel; sokkal ritkább, mint a בְּ, de inkább egybeesést (-kor) fejez ki, mint tartamot (alatt): 1Móz 3:8 הַיּוֺם לְרוּחַ a nap hűvösén, לְעֵת különféle kapcsolatokban, mint עֶרֶב לְעֵת 8:11 és máshol (l. עֵת); מְזֻמָּנִים לְעִתִּים Ezsd 10:14; Neh 10:35; בַּצָּרָה לְעִתּוֺת Zsolt 9:10; 10:1; ֗֗֗ לְיוֺם valaminek a napján, 81:4; Péld 7:20 és máshol, ֗֗֗ לְיוֺם תעשׂו מה Ézs 10:3; Hós 9:5 (vö. Jer 5:31); ֗֗֗ אֲשֶׁר לַיָּמִים Ez 22:14; ֗֗֗ אֲשֶׁר לַיּוֺם Mal 3:17; השׁנה לתשׁובת 2Sám 11:1 és máshol; הימים לתקופת 1Sám 1:20, השׁנה לתקופת2Krón 24:23 (2Móz 34:22 לְ nélkül), (יָמִיםׅ שָׁנִים לְקֵץ (késői) 2Krón 18:2; Neh 13:6; Dán 11:6, 13 (a korai héberben יָמִים מִקֵּץ); ֗֗֗ לשׁנת2Krón 15:10; לַבֹּקֶר Zsolt 30:6; 49:15 és máshol (2Móz 34:2 נָכוֺן הֱיֵה után = valamire, valamikorra; vö. 19:11; Péld 21:31); (לַבְּקָרִים Ézs 33:2, l. 5i); לערב 1Móz 49:27 (|| בבקר) és máshol; לְמָחָר 2Móz 8:6 (a 8:5 לְמָתַי kérdésre felelve), 8:19; Eszt 5:12 (4Móz 11:18; Józs 7:13 הִתְקַדְּשׁוּ után = valamire), לַמָּחֳרָת Jón 4:7 (vö. 1Krón 29:21); לָאוֺר Jób 24:14; ֗֗֗ לְמוֺעֵד לַמּוֺעֵד,, 1Móz 17:21; 2Móz 23:15 és máshol; לְפָנִים és לִפְנֵי előtt (gyakran); לְאָחוֺר ezután, Ézs 41:23; 42:23; Zsolt 32:6 b; infinitivusszal (ritka), a (עֶרֶבׅ (הַ)בֹּקֶר לִפְנוֺת kifejezésben 1Móz 24:63 és máshol, 2Sám 18:29; Ézs 7:15 לְדַעְתּוֺ amikor tudja.

**33.** 

> b. to denote the close of a period (rare), Gen 7:4 שׁבעה עוד לימים, 7:10; Exod 19:15; 2Sam 13:23; Amos 4:4 ימים לשׁלשׁת (We); Ezra 10:8-9, Neh 6:15; Dan 12:7 (compare עַד 7:25) 2Chr 21:19 (so Syriac: see PS 5).

b. egy időszak végének jelölésére (ritka), 1Móz 7:4 שׁבעה עוד לימים, 7:10; 2Móz 19:15; 2Sám 13:23; Ámós 4:4 ימים לשׁלשׁת (We); Ezsd 10:8-9, Neh 6:15; Dán 12:7 (vö. עַד 7:25) 2Krón 21:19 (így a szír: l. PS 5).

**34.** 

> c. towards, to, Exod 34:25 לַבֹּקֶר ילין לא (usually עַד, as 23:18), Deut 16:4; 1Sam 13:8 (after נוֺחַל), Amos 4:7 לַקָּצִיר חדשׁים שׁלשׁה בעוד to the harvest; often in the expressions דֹּר לְדֹר וָדוֺר, לְדוֺר לָנֶצַח, לְעוֺלָם,; rather differently in לְיוֺם מִיּוֺם Psa 96:2 (|| 1Chr 16:23 אל), Est 3:7 (i.e. passing from day to day), compare 2Sam 14:26 (Gie^30f.).

c. valami felé, valameddig, 2Móz 34:25 לַבֹּקֶר ילין לא (rendszerint עַד, mint 23:18), 5Móz 16:4; 1Sám 13:8 (נוֺחַל után), Ámós 4:7 לַקָּצִיר חדשׁים שׁלשׁה בעוד az aratásig; gyakran a דֹּר לְדֹר וָדוֺר, לְדוֺר לָנֶצַח, לְעוֺלָם, kifejezésekben; kissé másként a לְיוֺם מִיּוֺם kifejezésben Zsolt 96:2 (|| 1Krón 16:23 אל), Eszt 3:7 (azaz napról napra haladva), vö. 2Sám 14:26 (Gie^30k.).

**35.** 

> d. for, during, Isa 63:18 לַמִּצְעָר (si vera lectio), 2Chr 11:17 שׁלושׁ לשׁנים, 29:17. 7 With an infinitive (Ges^§ 114, 2), ל denotes a. most commonly the end or purpose of an action ( = the Latin Gerund with ad, e.g. ad faciendum, to do): Gen 1:17 and he placed them in the firmament וְלִמְשֹׁלוּ֗֗֗לְהַבְדִּיל לְהָאִיר to give light . . ., and to rule . . ., and todivide, etc., 2:15 set him in the garden וּלְשָׁמְרָהּ לְעָבְדָהּ to till it, and to keep it, 2:9 brought them to Adam לִרְאוֺת to see, etc., + very often; 19:20 שָׁ֑מָּה לָנוּס קְרֹבָה near for fleeing thither, Eccl 3:2 לָלֶדֶת עֵת a time for bringing forth. The negative is expressed by לְבִלְתִּי, q. v.

d. valameddig, valami alatt, Ézs 63:18 לַמִּצְעָר (si vera lectio), 2Krón 11:17 שׁלושׁ לשׁנים, 29:17. 7 Infinitivusszal (Ges^§ 114, 2) a ל jelöli a. legtöbbször a cselekvés célját vagy szándékát ( = a latin gerundium ad-dal, pl. ad faciendum, megtenni): 1Móz 1:17 és az ég boltozatára helyezte őket, וְלִמְשֹׁלוּ֗֗֗לְהַבְדִּיל לְהָאִיר hogy világítsanak ..., és uralkodjanak ..., és elválasszanak stb., 2:15 a kertbe helyezte, וּלְשָׁמְרָהּ לְעָבְדָהּ hogy művelje és őrizze, 2:9 Ádámhoz vitte őket, לִרְאוֺת hogy lássa stb., és igen gyakran máshol; 19:20 שָׁ֑מָּה לָנוּס קְרֹבָה közel van, hogy oda meneküljek, Préd 3:2 לָלֶדֶת עֵת ideje a szülésnek. A tagadást לְבִלְתִּי fejezi ki, l. ott.

**36.** 

> b. with reference to, limiting or qualifying the idea expressed by the principal verb, and so resolvable sometimes into so as to, to, sometimes into in respect of, in: — (a) so as to, to, Deut 8:6 and keep the commands of י אֹתוֺ וּלְיִרְאָה בִּדְרָכָיו ׳לָלֶכֶת to walk in his ways, and to fear him, 10:15; 11:22; 19:9; 1Kin 2:3-4, 11:2; 1Sam 20:20, 36; Joel 2:26 לְהַפְלִיא עִמָּכֶם עָשָׂה אֲשֶׁר so as to do wondrously, Ezek 5:6; Judg 5:18 לָמוּת נַפְשׁוֺ חֵרֵף עַם so as to die, for dying [not 'unto death'], 16:16; 2Kin 20:1 לָמוּת חָלָה; Gen 2:3 לַעֲשׂוֺת so as to make (or in making) which, he created; and in the very frequently לֵאמֹר, introducing the words spoken, so as to say = saying (German indem er sagte), 1:22, etc. (b) in respect of, in (compare 5e (b)) 34:7; 1Sam 12:17 your evil is great that ye have done מלך לכם לִשְׁאוֺל in asking for yourselves a king, 1 Samuel 12:29; 14:33 the people sin against J. עלהֿדם לאכל in eating with the blood, 19:5; 2Sam 19:7; 2Kin 4:24; Jer 44:18; Psa 36:3; 63:3; 78:18; 101:8; 103:20; Neh 13:18. And with the tert. compare., above 5e (b). Especially with verbs expressing what with us would be denoted by an adverb adjunct, but in Hebrew idiom forms the principal idea, as 1Sam 1:12 לְהִתְמַּלֵּל הִרְבְּתָה literally did much in respect of praying ( = prayed long or much), Isa 55:7 לִסְלוֺחַ יַרְבֶּה כִּי +; 2Kin 2:10 לִשְׁאוֺל הִקְשִׁיתָ thou hast done hardly in respect of asking ( = asked a hard thing), 1Kin 14:9 לַעֲשׂוֺת הֵרַע; so with הקריב Gen 12:11, מִהַר 27:20, הרחיק Exod 8:24 הֶעְמִּיל Num 14:44, הֵהִין Deut 1:41, בּשֵׁשׁ Judg 5:28, הפליא 13:19; 2Chr 26:15 (with passive verb), שׁוּב 1Kin 13:17; Ezra 9:14, היטיב Jer 1:12 + (without לְ 1Sam 16:17), העמיק Isa 29:15 +, קֵרֵב Ezek 36:9, הגדיל Joel 2:20 +, לִבְרֹחַ קִדַּמְתִּי Jonah 4:2, הגביהּ Psa 113:5, השׁפיל 113:6; Gen 31:27 לִבְרֹחַ נַחְבֵּאתָ hast hidden thyself in regard to fleeing = hast fled secretly, 2Sam 19:4 לָבוֺא וַיִּתְגַּנֵּב = come in stealthily. (c.) by an extension of (b), the infinitive with לְ so forms the complement of a verb that, if the verb be transitive, it becomes virtually its object: so very often with such verbs as הוסיף to add Gen 4:2, 12, הֵחֵל to begin 6:1, חדל 11:8, יכל 13:6, מִהַר 18:7, נתן to permit 20:6, אבה 24:5, בקשׁ Exod 2:15, מֵאֵן 7:14, למד Deut 14:23, חפץ 25:8, ידע 1 Kings 5:20 (these all occur also without לְ); הואיל to undertake, consent, Gen 18:17, 31, כִּלָּה to finish, תָּמַם Deut 2:16 (to come to an end in respect of), קִוָּה Isa 5:2; also צִוָּה Gen 50:2, אָמַר Exod 2:14, דִּמָּה Num 33:56, חשׁב 1Sam 18:25, יעץ Psa 62:5, לִמֵּד Jer 12:16, אָהֵב Hosea 12:8: Deut 10:12 what doth ׳י ask of thee ליראה אם כי except to fear etc. ? (compare Micah 6:8 after דרשׁ without ל). (d) as the subject of a sentence (rare): Isa 10:7 בלבבו להשׁמיד, 1Chr 29:12; with טוב 1Sam 15:22; Psa 118:8; 118:9; Eccl 7:2, 5; Prov 21:9 (usually without לְ, as 21:19; 25:24; Exod 14:12); compare 8:22 כן לעשׂות נכון לא; 2Sam 18:11 לָתֵת וְעָלַי, Neh 13:13; Ezra 10:12; Micah 3:1 לדעת לכם הלא, Ezra 4:3; 2Chr 13:5; 20:17; 26:18. (e) with אֵין יֵשׁ, (late), and (more rarely) לֹא, in sense of it is (not) possible to . . ., or (sometimes) there is no need to . . . : see יֵשׁ 2c c (p. 442); אַיִן 5 (p. 34 b), adding Hag 1:6; Est 8:8; 2Chr 22:9; לֹא 1a b (p. 518): and compare Dr^§ 202 Ges^§ 114l Dav^§ 94 b, 95 b. (f) with הָיָה, to express the idea of destination, as Num 24:22 לְבָעֵר יהיה וקין shall be for consuming, Deut 31:17; Isa 5:5; 6:13; 37:26; Ezek 30:16; Psa 109:13 +. compare לַעֲשׂוֺת מֶה what is (was) to be done? Isa 5:4; 2Kin 4:13; 2Chr 25:9 + (Dr^§ 203). (g) expressing (according to the context) tendency, intention, or obligation (the 'periphrastic' future): — Hosea 9:13 בָּנָיו הוֺרֵג אֶל לְהוֺצִיא וְאֶפְרַיִם is for bringing forth (= must bring forth), Isa 10:32 לעמד בנֹב היום עוד is he for tarrying (must he tarry), 38:20 ׳י ׳י, להושׁיעני is (ready) to save me, 44:14 (si vera lectio), Jer 51:49; Hab 1:17; Psa 32:9; 49:15 שְׁאוֺל לְבַלּוֺת צוּרָם = must Sheol waste away, 62:10 לַעֲלוֺת בְּמאֹזְנַיִם, Prov 18:24; 19:8 טוב למצא תבונה שׁומר will be finding prosperity, 20:25; Job 30:6; 1Chr 22:5 (לִבְנוֺת), Eccl 3:15: of past time, Gen 15:12 לבוא השׁמשׁ ויהי was about to go down, Josh 2:5; 1Sam 14:21b (text dubious: Dr^§ 206 Obs.), 2Chr 26:5 (strangely) אלהים לדרשׁ ויהי RV set himself to seek; usually without היה, 2Sam 4:10 לוֺ לְתִתִּי אֲשֶׁר to whom it was for my giving (I ought to have given), 2Kin 13:19 לְהַכּוֺת percutiendum erat, 1Chr 9:25, and more freely 2Chr 11:22 להמליבו כי for (he was) for making him king, 12:12 להשׁחית ולא and was no longer for destroying him, 36:19 (?): in a question, Gen 30:15 וְלָקַחַת and art thou for taking ? Est 7:8; 2Chr 19:2 לַעְזֹּר הֲלָרָשָׁע wilt thou help the wicked ? compare Dr^§ 204, Ges^158; 114 h-k, Dav^§ 94. (h) with וְ, in contin. (mostly) of a finite verb or participle, Exod 32:29 וְלָתֵת ֗֗֗ יֶדְכֶם מַלְאוּ and be for placing etc. Lev 10:10f. (?), 1Sam 8:12 וְלָשׂוּם ֗֗֗ יִקַּח, Jer 19:12 וְלָתֵת ֗֗֗ אעשׂה, 44:14; Hosea 12:3; Psa 25:14; 109:16; Job 34:8; Eccl 7:25; 9:1 (si vera lectio), Dan 12:11; Neh 8:13; 1Chr 10:13; 2Chr 2:8; 7:17; 8:13; 30:9; Ezek 13:22; Amos 8:4 וג וְלַשְׁבִּית אֶבְיוֺן ׳הַשֹּׁאֲפִים and (that are) for making the poor to cease, Isa 44:28 וְלֵאמֹר ֗֗֗ הָאוֺמֵר, 56:6; Psa 104:21; Jer 17:10; 44:19; 1Chr 6:34 (compare Dr^§ 206 Dav:§ 96 R. 4). — On לְמִן, see מִן. Note. — 1Kin 6:19 שָׁם לְתִתֵּן, the supposition that לְ is a conjunction (= למען) is too alien to Hebrew usage to be justified by the Arabic for , and the view that תִתֵּן here and 17:14 is an anomalous form for תֵת (Ew^§ 238 c Kö^i. 305) is against analogy: read with Ol^§ 224 d, Ges^§ 67 A. 3, Klo, לָתֵת (as 17:14 Qr).

b. vonatkozással, a főige által kifejezett gondolatot korlátozva vagy minősítve, és így néha úgy, hogy-ra, néha valami tekintetében, -ban, -ben jelentésre bontható fel: — (a) úgy, hogy; hogy, 5Móz 8:6 és tartsd meg י אֹתוֺ וּלְיִרְאָה בִּדְרָכָיו ׳לָלֶכֶת parancsolatait, hogy útjain járj, és hogy féld őt, 10:15; 11:22; 19:9; 1Kir 2:3-4, 11:2; 1Sám 20:20, 36; Jóel 2:26 לְהַפְלִיא עִמָּכֶם עָשָׂה אֲשֶׁר úgy, hogy csodásan cselekedett, Ez 5:6; Bír 5:18 לָמוּת נַפְשׁוֺ חֵרֵף עַם úgy, hogy meghaljon, halálra [nem 'unto death'], 16:16; 2Kir 20:1 לָמוּת חָלָה; 1Móz 2:3 לַעֲשׂוֺת amelyet úgy teremtett, hogy megalkossa (vagy: megalkotva); és az igen gyakori לֵאמֹר alakban, amely a kimondott szavakat vezeti be: úgy, hogy mondja = mondván (német indem er sagte), 1:22 stb. (b) valami tekintetében, -ban, -ben (vö. 5e (b)) 34:7; 1Sám 12:17 nagy a ti gonoszságotok, amelyet elkövettetek מלך לכם לִשְׁאוֺל azzal, hogy királyt kértetek magatoknak, 1Sám 12:29; 14:33 a nép vétkezik J. ellen עלהֿדם לאכל azzal, hogy vérével együtt eszik, 19:5; 2Sám 19:7; 2Kir 4:24; Jer 44:18; Zsolt 36:3; 63:3; 78:18; 101:8; 103:20; Neh 13:18. A tertium comparationisszal is, l. fent 5e (b). Különösen olyan igékkel, amelyek azt fejezik ki, amit mi határozói járulékkal jelölnénk, de ami a héber szólásmódban a fő gondolatot alkotja, mint 1Sám 1:12 לְהִתְמַּלֵּל הִרְבְּתָה szó szerint: sokat tett az imádkozás tekintetében ( = sokáig vagy sokat imádkozott), Ézs 55:7 לִסְלוֺחַ יַרְבֶּה כִּי és máshol; 2Kir 2:10 לִשְׁאוֺל הִקְשִׁיתָ nehezet tettél a kérés tekintetében ( = nehéz dolgot kértél), 1Kir 14:9 לַעֲשׂוֺת הֵרַע; így הקריב 1Móz 12:11, מִהַר 27:20, הרחיק 2Móz 8:24 הֶעְמִּיל 4Móz 14:44, הֵהִין 5Móz 1:41, בּשֵׁשׁ Bír 5:28, הפליא 13:19; 2Krón 26:15 (szenvedő igével), שׁוּב 1Kir 13:17; Ezsd 9:14, היטיב Jer 1:12 és máshol (לְ nélkül 1Sám 16:17), העמיק Ézs 29:15 és máshol, קֵרֵב Ez 36:9, הגדיל Jóel 2:20 és máshol, לִבְרֹחַ קִדַּמְתִּי Jón 4:2, הגביהּ Zsolt 113:5, השׁפיל 113:6 igékkel; 1Móz 31:27 לִבְרֹחַ נַחְבֵּאתָ elrejtőztél a menekülés tekintetében = titokban menekültél el, 2Sám 19:4 לָבוֺא וַיִּתְגַּנֵּב = lopva jönni. (c.) a (b) kiterjesztéseként az לְ elöljárós infinitivus úgy egészíti ki az igét, hogy ha az ige tárgyas, gyakorlatilag annak tárgyává válik: így igen gyakran olyan igékkel, mint הוסיף még tenni, hozzáadni 1Móz 4:2, 12, הֵחֵל kezdeni 6:1, חדל 11:8, יכל 13:6, מִהַר 18:7, נתן megengedni 20:6, אבה 24:5, בקשׁ 2Móz 2:15, מֵאֵן 7:14, למד 5Móz 14:23, חפץ 25:8, ידע 1Kir 5:20 (ezek mind előfordulnak לְ nélkül is); הואיל vállalkozni, beleegyezni, 1Móz 18:17, 31, כִּלָּה befejezni, תָּמַם 5Móz 2:16 (valami tekintetében véget érni), קִוָּה Ézs 5:2; továbbá צִוָּה 1Móz 50:2, אָמַר 2Móz 2:14, דִּמָּה 4Móz 33:56, חשׁב 1Sám 18:25, יעץ Zsolt 62:5, לִמֵּד Jer 12:16, אָהֵב Hós 12:8: 5Móz 10:12 mit kér tőled ׳י ליראה אם כי, mint hogy féld stb.? (vö. Mik 6:8 דרשׁ után ל nélkül). (d) a mondat alanyaként (ritka): Ézs 10:7 בלבבו להשׁמיד, 1Krón 29:12; טוב mellett 1Sám 15:22; Zsolt 118:8; 118:9; Préd 7:2, 5; Péld 21:9 (rendszerint לְ nélkül, mint 21:19; 25:24; 2Móz 14:12); vö. 8:22 כן לעשׂות נכון לא; 2Sám 18:11 לָתֵת וְעָלַי, Neh 13:13; Ezsd 10:12; Mik 3:1 לדעת לכם הלא, Ezsd 4:3; 2Krón 13:5; 20:17; 26:18. (e) אֵין יֵשׁ, (késői) és (ritkábban) לֹא mellett, ebben az értelemben: (nem) lehet ..., vagy (néha) nincs szükség arra, hogy ...: l. יֵשׁ 2c c (442. o.); אַיִן 5 (34. o. b), hozzáadva Hag 1:6; Eszt 8:8; 2Krón 22:9; לֹא 1a b (518. o.): és vö. Dr^§ 202 Ges^§ 114l Dav^§ 94 b, 95 b. (f) הָיָה mellett, a rendeltetés gondolatának kifejezésére, mint 4Móz 24:22 לְבָעֵר יהיה וקין pusztulásra lesz, 5Móz 31:17; Ézs 5:5; 6:13; 37:26; Ez 30:16; Zsolt 109:13 és máshol. vö. לַעֲשׂוֺת מֶה mit kell (kellett) tenni? Ézs 5:4; 2Kir 4:13; 2Krón 25:9 és máshol (Dr^§ 203). (g) (a szövegösszefüggés szerint) hajlamot, szándékot vagy kötelezettséget kifejezve (a 'körülírt' jövő idő): — Hós 9:13 בָּנָיו הוֺרֵג אֶל לְהוֺצִיא וְאֶפְרַיִם szülésre van (= szülnie kell), Ézs 10:32 לעמד בנֹב היום עוד késlekedésre van-e (késlekednie kell-e), 38:20 ׳י ׳י, להושׁיעני (kész) megmenteni engem, 44:14 (si vera lectio), Jer 51:49; Hab 1:17; Zsolt 32:9; 49:15 שְׁאוֺל לְבַלּוֺת צוּרָם = a Seolnak el kell sorvasztania, 62:10 לַעֲלוֺת בְּמאֹזְנַיִם, Péld 18:24; 19:8 טוב למצא תבונה שׁומר szerencsét fog találni, 20:25; Jób 30:6; 1Krón 22:5 (לִבְנוֺת), Préd 3:15: múlt időről, 1Móz 15:12 לבוא השׁמשׁ ויהי lenyugvóban volt, Józs 2:5; 1Sám 14:21b (a szöveg kétséges: Dr^§ 206 Obs.), 2Krón 26:5 (furcsán) אלהים לדרשׁ ויהי RV set himself to seek; rendszerint היה nélkül, 2Sám 4:10 לוֺ לְתִתִּי אֲשֶׁר akinek nekem kellett volna adnom (akinek adnom kellett volna), 2Kir 13:19 לְהַכּוֺת percutiendum erat, 1Krón 9:25, és szabadabban 2Krón 11:22 להמליבו כי mert (az volt a szándéka,) hogy királlyá tegye, 12:12 להשׁחית ולא és már nem akarta elpusztítani, 36:19 (?): kérdésben, 1Móz 30:15 וְלָקַחַת és el akarod venni? Eszt 7:8; 2Krón 19:2 לַעְזֹּר הֲלָרָשָׁע segíted-e a gonoszt? vö. Dr^§ 204, Ges^158; 114 h-k, Dav^§ 94. (h) וְ mellett, (többnyire) egy véges igealak vagy participium folytatásaként, 2Móz 32:29 וְלָתֵת ֗֗֗ יֶדְכֶם מַלְאוּ és arra legyen, hogy helyezzen stb. 3Móz 10:10k. (?), 1Sám 8:12 וְלָשׂוּם ֗֗֗ יִקַּח, Jer 19:12 וְלָתֵת ֗֗֗ אעשׂה, 44:14; Hós 12:3; Zsolt 25:14; 109:16; Jób 34:8; Préd 7:25; 9:1 (si vera lectio), Dán 12:11; Neh 8:13; 1Krón 10:13; 2Krón 2:8; 7:17; 8:13; 30:9; Ez 13:22; Ámós 8:4 וג וְלַשְׁבִּית אֶבְיוֺן ׳הַשֹּׁאֲפִים és (akik) a szegényt el akarják pusztítani, Ézs 44:28 וְלֵאמֹר ֗֗֗ הָאוֺמֵר, 56:6; Zsolt 104:21; Jer 17:10; 44:19; 1Krón 6:34 (vö. Dr^§ 206 Dav:§ 96 R. 4). — A לְמִן alakhoz l. מִן. Megjegyzés. — Az 1Kir 6:19 שָׁם לְתִתֵּן helyen az a feltevés, hogy a לְ kötőszó (= למען), túlságosan idegen a héber szóhasználattól ahhoz, hogy az arab igazolhatná, és az a nézet, hogy a תִתֵּן itt és a 17:14-ben a תֵת rendhagyó alakja (Ew^§ 238 c Kö^i. 305), ellenkezik az analógiával: olv. Ol^§ 224 d, Ges^§ 67 A. 3, Klo szerint לָתֵת (mint 17:14 Qr).

## DT-F38 döntés (F38.12) és könyvalak-leképezés (F38.13)

**Döntés (felhasználó, 2026.10.01):** (a) folytatás a 2. adaggal a (c) után; (b) a 13. kapu
jelzései nem állítják meg a futást, a brief M0.1 javítva („a 13. kapu csak a jóváhagyott
F34-maradékon és az N-F34c körén jelezhet”); (c) a könyvalak-leképezés bővítése most; (d) a
TAHOT-sorrend marad; (e) a H0413 kivétele rendben. A ψ-n túli könyvfeloldási hibák (H0413
„only in Job (…)” → „1 Samuel …”; „Deut 37:36” = 1Móz 37:36) nem javítandók, a fordítás hűen
viszi tovább; későbbi gépi csere: `beerkezo/BDB_KONYVFELOLDASI_AUDIT.md`.

### Mérés: a forrás igehely előtti, nem leképezett könyvalakjai

Parancs: `python naplok/BDB_FORDITAS_konyvalakok.py` (csak olvas). Minta: nagybetűs szó
(opcionális `1`–`3` vagy `I`–`III` előtaggal), opcionális pont, `fejezet:vers`; kimarad,
ami a 11. kapu leképezésében (`forditas_kapuk._konyv_mintak`) már kulcs.

- **A bővítés előtt:** 275 alak, 952 előfordulás. A legtöbb nem könyvnév: személy- és
  helynév a szócikk saját igehelye előtt (`God` 28, `Israel` 22, `Jerusalem` 15, `Judah` 11 …),
  nyelvtani címke (`Qal`, `Infinitive`, `Genitive`), szigla és nem bibliai mű (`Qor` 36, `Gi`
  15, `COT` 13, `Qr` 11, `Kt` 9, `Aboth`, `Yoma`, `Iliad`, `Odyssey` …).
- **Bibliai könyvalak, felvéve** a `konkordancia/Konyv_normalizalo_tabla.tsv` új, 4.
  oszlopába (`Forrás-alakok`): **21 alak, 357 előfordulás** (+1: a `3 Cant` a `Cant`-kulccsal
  együtt eltűnik a listáról):

  | Alak | Előfordulás | Szócikk | → Károli |
  |---|---|---|---|
  | `Ezekiel` | 96 | 70 | Ez |
  | `Cant` | 93 | 72 | Én |
  | `Malachi` | 52 | 41 | Mal |
  | `Daniel` | 42 | 30 | Dán |
  | `Proverbs` | 15 | 14 | Péld |
  | `2 Chron` | 13 | 12 | 2Krón |
  | `1Chron` | 12 | 9 | 1Krón |
  | `Ex` | 7 | 7 | 2Móz |
  | `Nah` | 5 | 3 | Náh |
  | `Esther` | 4 | 4 | Eszt |
  | `Songs` | 4 | 4 | Én |
  | `Haggai` | 3 | 3 | Hag |
  | `Paslm` | 2 | 2 | Zsolt (OCR) |
  | `James` | 2 | 2 | Jak |
  | `1 Ki` | 1 | 1 | 1Kir |
  | `1 Sam` | 1 | 1 | 1Sám |
  | `2Che` | 1 | 1 | 2Krón (OCR) |
  | `Plalm` | 1 | 1 | Zsolt (OCR) |
  | `I Chron` | 1 | 1 | 1Krón |
  | `Habakkuk` | 1 | 1 | Hab |
  | `Titus` | 1 | 1 | Tit |

- **Bibliai vagy könyvszerű alak, NEM felvéve** (nem egyértelmű, vagy nem kanonikus):

  | Alak | Előfordulás | Ok |
  |---|---|---|
  | `Kings` | 2 | szám nélkül nem egyértelmű (1Kir/2Kir): H1961 „1 K i1 Kings 12:24” = 1Kir (összeolvadt), H0834 „compare Kings 6:35; 6:37” nem dönthető el. **Eltérés a DT-F38 (c)-től**, l. lent |
  | `Ki`, `Sam`, `Chron`, `Chronicles`, `Samuel` | 1, 4, 1, 1, 2 | szám nélküli vagy összeolvadt alak (`compare1 Sam`, `feminine1 Chronicles`, `2; Chron`), ill. személynév (`of Samuel 12:2`) |
  | `Ze`, `Jes`, `Esc`, `De`, `En` | 2, 1, 1, 1, 1 | a feloldás csak értelmezéssel adható meg (Zak? Ézs? Préd? Zsolt? Dán?) — a lexikai feloldás az audit dolga |
  | `Che`, `Psalmist` | 1, 1 | szerzőnév (Cheyne), ill. „a zsoltáros” |
  | `3 Esdr`, `Psalms of Solomon`, `1Makk`, `2Mace`, `Ecculs` | 2, 1, 1, 1, 1 | apokrif/pszeudepigráf; a tábla a 66 kanonikus könyvé (az apokrif alakok az `APOKRIF_ALIAS`-ban vannak) |

- **A bővítés után:** 253 alak, 594 előfordulás maradt a listán (csak a fenti nem felvett
  alakok és a nem-könyvnév találatok).

**Megvalósítás.** A tábla nem kapott új sort (a `f19_ebible_import.py`, a `fj2/`, `f17/` és a
`general.py` a 66 soros kanonikus sorrendre épül), hanem új, utolsó oszlopot (`Forrás-alakok`,
vesszővel elválasztva). Az `eszkozok/normalizal.py` a tábla betöltésekor ezeket a
`FORRAS_ALIAS`-hoz adja (a kódbeli alias elsőbbségével), így a javítóréteg (`IGE_LEK`) és a
11. kapu (`forditas_kapuk._konyv_mintak`) ugyanazt látja. A prompt v4 Károli-listája
(`emeles.karoli_szoveg`) csak az első két oszlopot használja: **a prompt nem változott.**
Tesztek: `eszkozok/teszt_normalizal.py` (+4: leképezés mind a 21 alakra, csak igehely előtt,
a többértelmű alakok hiánya, a tábla szerkezete) és `eszkozok/teszt_forditas_kapuk.py` (+3: a
11. kapu a forrásalakot Károli-alakkal elfogadja, angolul hagyva sértés, `Kings` nem
leképezett). 26/26 és 23/23 OK.

**A javítóréteg újra** (`python naplok/BDB_FORDITAS_ujranormalizal.py --ir`): mind a 49 szótári
`teljes` soron (35 BDB, 14 Thayer) lefutott; változás csak 3 F38-as sorban, mindhárom a kapukon átment (a régi
szöveg az új leképezéssel a 11. kapun bukna):

| Sor | Strong | Csere | 13. kapu (JELZES, nem gátoló) |
|---|---|---|---|
| 97. | H3605 | `1Chron` ×2, `2 Chron` → 1Krón, 2Krón (3) | 1Krón 119, 1Krón 145 (zsoltárhelyek, forráshiba) |
| 99. | H9003 | `Ex 7:29` → 2Móz, `Cant` → Én (2) | — |
| 100. | H0834 | `Malachi` → Mal (1); a `Kings 6:35; 6:37` marad | Ruth 8, Ruth 9 (F34-maradék) |

A DT-F38 „5 szócikk, 9 hely” száma a mérés szerint 3 szócikk, 7 hely (6 csere + a `Kings`);
a különbség a korábbi számolásé (a könyvnév nélküli folytatólagos igehelyek is beleszámítottak).
A `megjegyzes` mező végére: „F38.13: javítóréteg újra a könyvalak-leképezés bővítése után
(DT-F38 c)”. A teljes kapusor mind a 9 F38-as soron (`python naplok/BDB_FORDITAS_kapuk.py`):
9/9 átment, 5 JELZES (13. kapu). `eszkozok/ellenoriz.py`: SÉRTÉS 0; `futtat.py`: 0 találat.

**A 13. kapu a forráson** (`python naplok/BDB_FORDITAS_M0.py --nem-ir`): a bővítés előtt 91
szócikk (83 F34-maradék), utána **109 szócikk (86 F34-maradék, 23 nem)**. A 18 új jelzés
mind a most láthatóvá vált könyvalakok forrásbeli feloldási hibája (pl. `1Chron 119:21` =
Zsolt, `Ex 43:21`/`46:6`/`51:25`/`45:4`, `Nah 7:5`/`19:12`/`23:8`/`47:3`/`5:14`, `Cant 19`/`26`/`34`,
`2 Chron 105`), tehát az N-F34c körébe (nem ψ eredetű könyvfeloldási hiba) és az audit-csonkba
tartozik; a futást a DT-F38 (b) szerint nem állítja meg. Új jelző szócikk (18): H0457, H1870,
H3289, H3605, H3701, H3782, H3881, H4043, H4603, H4686, H4908, H5000, H5186, H5608, H6240,
H6437, H7131, H8398; a már jelző H1931 két új hellyel (1Krón 93, 94).

**Eltérés a döntéstől:** a `Kings` nincs a leképezésben (szám nélkül 1Kir és 2Kir is lehet;
a forrás 2 helyéből csak az egyik dönthető el). A két hely forrásalakon marad (a 3. kapu
„forrásbeli szigla igehely előtt” ágán), mint eddig. Ha a felhasználó egy könyvhöz rendeli,
egy szó a táblában.

## M2 — 2. adag (F38.15–F38.51)

**Fordító és módszer:** változatlanul az M1 szerint (a menet maga, Opus `claude-opus-5-5`,
subagent nélkül; `emeles.py helyorzo` → helyőrzős vázlat → `emeles.py ellenoriz` → `rogzit` →
`beir --allapot opus`, utána a `naplok/EMELES_munka.tsv` visszaállítása). Prompt v4,
terminológia v3 — egyik sem változott; terminológia-kivétel nem volt. A 20 000 karakter fölötti
nyolc szócikk (H3588, H1961, H3117, H6440, H5414, H1980, H4480, H7725) és négy rövidebb (H3027,
H3045, H3318, H5973) több vázlatrészben készült, és egyben került a kapukra és a táblába. Minden szócikk saját
commitban (`F38.15`–`F38.51`), `megjegyzes=F38 BDB_FORDITAS M2 (adag 2)`.

**Számok:** 37 szócikk (a sorrend 10–46. sora, H3808–H0854), forrás 495 907 karakter,
fordítás 516 929 karakter (arány 1,04). Kész összesen (BDB `teljes`): 26 + 9 + 37 = 72
szócikk; hátra 8 018 szócikk, 5 553 791 forráskarakter. A 3. adag a sorrend 47. sorától
(H5927) indul.

**Ellenőrzés az adag végén:** teljes kapusor mind a 37 soron (`python
naplok/BDB_FORDITAS_kapuk.py --adag 2`): 37/37 átment, 0 bukott, 17 szócikk 13. kapus JELZES-sel.
`eszkozok/ellenoriz.py`: RENDBEN 11, SÉRTÉS 0, KÉZI 2, JELENTÉS 3. `eszkozok/ellenorzes/futtat.py
--valtozott adat/forditasok.tsv`: 0 találat. **Hibás lista:** egy szócikk sem került a
`naplok/BDB_FORDITAS_hibas.tsv`-be.

**Önújrapróba** (mindig a fordítás javult, nem a kapu; kapukalibrálás nem volt). Elsőre átment
14 szócikk: H0776, H6213, H0935, H1004, H5414, H5971, H1697, H7200, H5704, H5892, H1732, H7725,
H5973, H0854. A többi 23-nál egy önújrapróba elég volt:

| Kapu | Strong | Eset és javítás |
|---|---|---|
| 1 görög–héber | H1980 | a forrás `\x8b`, `\x99` vezérlőkaraktere két héber szakasz között kimaradt — visszaállítva |
| 1 görög–héber | H3427 | kimaradt helyőrző (⟦94⟧) — visszaállítva |
| 1 görög–héber | H3947 | két helyőrző egybeírva — a forrás szóköze visszaállítva |
| 3 Károli | H3588, H3478, H3117, H6440, H0376, H1980, H3318 | nagybetűs szó közvetlenül c:v előtt („Isten 23:16”, „Júdáról 12:6”, „A 4:16”, „Isten 33:10”, „Istennel 32:29”, „Dávidén 11:17”, „Sámuelről 12:2”, „Egyiptomból 18:1”, „Áronról 6:13”) — átfogalmazva |
| 4 formázás | H4428, H1931, H0259 | betoldott zárójel — eltávolítva |
| 5 terminológia | H1961 (living soul → lélek), H4428 (accusative), H3117 (proper name, of a location), H1931 (suffix, emphatic, Zinjirli), H8085 (spiritual), H0859 (suffix), H0518 (emphatic) | a kötelező alak pótolva |
| 8 idézőjel | H4480, H0518 | ASCII idézőjel → „ ”, illetve a betoldott „ ” eltávolítva |
| 9 tagolás | H3808, H1961, H3117, H3027, H0001 | „c. 1Móz” → „c. — 1Móz” (a kapu circa-kivétele); a forrás „f. below”, „i. below”, „d.” (day), „f.” (father) jelölőnek számít — a forrás alakja megtartva |
| 10 törzs | H1696 | a forrás „Piel” alakja megtartva |
| 11 könyvek | H9004, H3045 | a forrás összeolvadt alakja („concerning2Chr”, „learnedIsa”, „regardPsa”) a fordításban is összeolvadva („nézve2Krón”, „tanultÉzs”), mert a kapu a forrásban nem látja |

Ugyanígy összeolvadva maradt (elsőre átment): „confront2Chr” (H6440), „gate2Chr” (H5971),
„compareIsaiah” (H3027), „letterEst” (H1697), „unto2Chr” (H1696).

**Forráshiba a fordításban, hűen átvéve** (13. kapu JELZES, nem gátoló; a DT-F38 (b) szerint a
futást nem állítja meg). A jelzések egy része az F34-maradékba (ψ eredetű feloldás), más része az
N-F34c körébe tartozik (pl. H9004 Dán 23, H3117 Dán 40, H0854 „John 5:30; 54:15; 30:1” =
Ézsaiás-helyek, „Jon 11:27” = Bír 11:27, H7725 / H5973 „2Sam 26” = 1Sám 26); a forrást a menet
nem javítja (brief, Nem cél). A teljes lista a lenti táblázat alatt.

**Megjegyzés a 11. kapuhoz:** a DT-F38 (c) leképezés (F38.13) óta a forrás `Malachi`, `Ezekiel`,
`Daniel`, `Cant`, `2 Chron`, `1 Ki` stb. alakja Károli-rövidítést kap; az M2-ben ez rendben
működött (pl. H0859 „Malachi 3:20” → Mal 3:20, H3045 „1 Ki 5:20” → 1Kir 5:20). A szám nélküli
`Kings` továbbra sincs leképezve (DT-F38 eltérés).

*Az alábbi alszakasz a `python naplok/BDB_FORDITAS_M1_nezet.py --adag 2` kimenetének első része
(a minta elhagyva: a brief szerint a hosszabb minta csak az M1-ben kötelező).*

### Kapueredmények (adag 2, 37/37 szócikk kész)

| Strong | Forrás kar. | Fordítás kar. | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 | 11 | 12 | 13 | Átment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H3808 | 13885 | 13980 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H3588 | 23687 | 23654 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H1961 | 24992 | 25859 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H9004 | 11025 | 11188 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H6213 | 12627 | 13995 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.11) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0935 | 14625 | 15373 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4428 | 4551 | 4843 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H3478 | 4038 | 4570 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.13) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H0776 | 4251 | 4555 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3117 | 20257 | 20875 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H6440 | 21162 | 21774 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H1004 | 14503 | 15014 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5414 | 23371 | 24802 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1931 | 12775 | 12651 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.99) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H5971 | 6678 | 7073 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0376 | 3755 | 4028 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3027 | 18079 | 18607 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1980 | 43729 | 44374 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1697 | 11681 | 11936 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H7200 | 16846 | 18395 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H5704 | 9684 | 9927 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0001 | 4836 | 5181 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H4480 | 35799 | 36362 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H8085 | 9153 | 10607 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.16) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1696 | 10705 | 11442 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0859 | 1667 | 1747 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5892 | 3474 | 3690 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3427 | 10978 | 11634 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1732 | 3195 | 3275 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H0518 | 8652 | 8751 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3318 | 19000 | 19862 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H7725 | 21596 | 24018 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.11) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H5973 | 12668 | 13148 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H0259 | 4200 | 4462 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3947 | 10089 | 10596 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3045 | 14746 | 15659 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0854 | 8948 | 9022 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |

Összesen: forrás 495907, fordítás 516929 karakter.

13. kapu (JELZES, nem gátoló): H3808 — a könyv fejezetszámánál nagyobb fejezet: 2Sám 26; H3588 — a könyv fejezetszámánál nagyobb fejezet: 1Kir 32, 1Kir 47; H1961 — a könyv fejezetszámánál nagyobb fejezet: 1Kir 23; H9004 — a könyv fejezetszámánál nagyobb fejezet: Dán 23; H4428 — a könyv fejezetszámánál nagyobb fejezet: Préd 15; H3478 — a könyv fejezetszámánál nagyobb fejezet: 1Kir 24; H3117 — a könyv fejezetszámánál nagyobb fejezet: Dán 40; H6440 — a könyv fejezetszámánál nagyobb fejezet: 2Kir 36, Zak 17; H1931 — a könyv fejezetszámánál nagyobb fejezet: 1Krón 93, 1Krón 94, 2Kir 33, Hós 19, Hós 22, Hós 24, JSir 6; H7200 — a könyv fejezetszámánál nagyobb fejezet: 1Sám 32, 1Sám 46, 1Sám 48; H0001 — a könyv fejezetszámánál nagyobb fejezet: 1Kir 50, Eszt 11; H4480 — a könyv fejezetszámánál nagyobb fejezet: 1Kir 32; H1732 — a könyv fejezetszámánál nagyobb fejezet: 2Sám 132; H3318 — a könyv fejezetszámánál nagyobb fejezet: Jer 58; H7725 — a könyv fejezetszámánál nagyobb fejezet: 2Sám 26; H5973 — a könyv fejezetszámánál nagyobb fejezet: 2Sám 26; H0854 — a könyv fejezetszámánál nagyobb fejezet: Ján 30, Ján 54, Jón 11.

## M2 — önújrapróba-elemzés (F38.54, DT-F38b)

*Csak olvasó elemzés, a 3. adag előtt (DT-F38b döntés, 2026.10.02). Forrás: a fenti
önújrapróba-táblázat, és a példaszegmensek a `konkordancia/BDB_teljes_unabridged.tsv`-ből (F)
és az `adat/forditasok.tsv` végleges `teljes` soraiból (H). Az első, elbukott vázlatok nincsenek
meg (a scratchpadben voltak), ezért a hibás alakot a fenti táblázat leírása adja, a példa a
forrást és a javított végleges alakot mutatja.*

A 23 önújrapróbás szócikk 30 kapujelzést adott (egy szócikk több kapun is bukhatott: H3117 a 3.,
5. és 9. kapun; H1961 az 5. és 9.; H4428, H1931 a 4. és 5.; H0518 az 5. és 8.; H1980 az 1. és 3.).

| Kapu | Darab (szócikk) | Arány a 23-ból | Jelleg | Példa szegmens |
|---|---|---|---|---|
| 3 Károli-rövidítés | 7 (H3588, H3478, H3117, H6440, H0376, H1980, H3318) | 30% | **részben téves riasztás**: a BDB könyvnév nélküli, láncolt igehelye (`of Judah 12:6`) előtt a magyar szórend nagybetűs szót hoz közvetlenül a c:v elé, a kapu ezt ismeretlen könyvrövidítésnek veszi; a fordítás jó, de az „Isten 23:16” olvasható is könyvnévként, így az átfogalmazás nem kár | H3478 F: `of Judah 12:6; 19:8-9t.` → H: „Júdáról pedig 12:6; 19:8-9t.” (elsőre „Júdáról 12:6”) · H3588 F: `(God's hostility 23:16 the cause of his misery …)` → H: „(a 23:16-ban Isten ellenségeskedése nyomorúságának oka …)” (elsőre „Isten 23:16”) · H3318 F: `out of (מִן) Egypt 18:1; 20:2` → H: „(מִן) Egyiptomból, így 18:1; 20:2” |
| 5 terminológia | 7 (H1961, H4428, H3117, H1931, H8085, H0859, H0518) | 30% | **valódi fordítási hiba** (kis súlyú): a kötelező magyar alak hiányzott, más szinonima állt; hét különböző kifejezés, közös minta nélkül (`living soul`, `accusative`, `proper name, of a location`, `suffix`, `emphatic`, `Zinjirli`, `spiritual`) | H1961 F: `and the man became a living soul` → H: „és az ember élő lélekké lett” · H0518 `emphatic` (a kötelező alak pótolva) · H8085 F: `figurative (spiritual power) Jer 5:21` (a kötelező alak pótolva) |
| 9 tagolás | 5 (H3808, H1961, H3117, H3027, H0001) | 22% | **kapu-heurisztika**: a forrás betűjelölője (`c.`, `f.`, `i.`) és a rövidítések (`c.` = circa, `f. below`, `d.` = day, `f.` = father) összetéveszthetők; a megoldás a forrás alakjának megtartása, illetve a circa-kivétel miatt „c. —” | H3808 F: `Zeph 2:1). c. Gen 15:13 להם לא בארץ` → H: „Sof 2:1). c. — 1Móz 15:13 להם לא בארץ” · H0001 H: „f. a szűkölködőké (késői) 68:6 … (tulajdonnévben, f. az egyéné, vö. lent)” · H3117 H: „i. különösen ünnepnap: הַשַּׁבָּת יוֺם a szombatnap” |
| 1 görög–héber | 3 (H1980, H3427, H3947) | 13% | **valódi, mechanikus hiba**: helyőrző-kezelés (kimaradt ⟦94⟧, két helyőrző egybeírva, a `\x8b`/`\x99` vezérlőkarakter elhagyva) | a fenti táblázat leírása szerint; a végleges sor a kapun átmegy |
| 4 formázás | 3 (H4428, H1931, H0259) | 13% | **valódi, kis súlyú**: a fordító zárójeles magyarázatot toldott be | H0259 F: `so also (emphatic) 2Sam 17:3 for ᵐ5 …` (a végleges sorban betoldás nincs) |
| 8 idézőjel | 2 (H4480, H0518) | 9% | **valódi, kis súlyú**: ASCII idézőjel, illetve betoldott „ ” | H4480 F: `either from or for ("zutheilen")` → a végleges sorban „ ” |
| 11 könyvek | 2 (H9004, H3045) | 9% | **forrásból eredő**: a forrás összeolvadt alakja (`concerning2Chr`, `learnedIsa`) a kapu forrásoldalán nem látszik, ezért a fordítás is összeolvasztva viszi | H9004 F: `= as concerning2Chr 32:19` → H: „= mint valamire nézve2Krón 32:19” · H3045 F: `skilled in a book, learnedIsa 29:11-12` → H: „az írásban jártas, tanultÉzs 29:11-12” |
| 10 törzs | 1 (H1696) | 4% | **forrásból eredő**: a forrás `Piel` alakja (a megszokott `Pi`el` helyett) | H1696 F: `for usual Piel) Psa 51:6` → H: „a szokásos Piel helyett) Zsolt 51:6” |

**Következtetés: nincs egyértelmű minta.** Egyetlen kapu sem adja a jelzések többségét: a két
leggyakoribb (3. és 5.) egyenként 7 szócikk (30%), a 30 jelzésből 7–7. A téves riasztás jellegű
kapuk (3., 9.) és a valódi hibát jelző kapuk (1., 4., 5., 8.) nagyjából fele-fele arányban
oszlanak meg (15–15 jelzés, a 10. és 11. kaput a forrásból eredőként a téves oldalra számolva),
és a valódi hibák szétszórtak (az 5. kapunál hét különböző terminus). Kalibrálási vagy
promptpontosítási javaslat ezért **nem** készül; a 3. adag a DT-F38b szerint módosítás nélkül
indul (prompt v4, terminológia v3, a kapuk változatlanok).

**Megfigyelés a zárásra (Mz), nem javaslat:** (1) a 3. kapu a láncolt BDB-igehelyeknél a magyar
szórend miatt jelez; ha a 3. adagban is ez marad a leggyakoribb, a zárásnál mérlegelhető egy
kivétel (nagybetűs, de a könyv-leképezésben nem szereplő szó a láncolt c:v előtt). (2) A 9. kapu
circa-kivétele a fordításba forrásban nem szereplő „—” jelet hoz („c. — 1Móz”). (3) A 11. kapu
nem látja a forrás összeolvadt könyvalakjait (`learnedIsa`), így ezek a fordításban is
összeolvadva maradnak („tanultÉzs”); ez a könyvfeloldási audit (`beerkezo/BDB_KONYVFELOLDASI_AUDIT.md`)
körébe tartozik.

## M3 — 3. adag (F38.55–F38.135)

**Fordító és módszer:** változatlanul az M1/M2 szerint (a menet maga, Opus `claude-opus-5-5`,
subagent nélkül; `emeles.py helyorzo` → helyőrzős vázlat → `emeles.py ellenoriz` → `rogzit` →
`beir --allapot opus`, utána a `naplok/EMELES_munka.tsv` visszaállítása). Prompt v4,
terminológia v3 — egyik sem változott; a kapuk sem (a DT-F38b szerint a 3. adag módosítás
nélkül indult, F38.54). Minden szócikk saját commitban (`F38.55`–`F38.135`, a `F38.121` a hibás
lista), `megjegyzes=F38 BDB_FORDITAS M3 (adag 3)`. A kapufuttatás előtt a vázlatra egy csak
olvasó, scratchpadbeli előellenőrzés futott (zárójelek és vezérlőkarakterek helyőrző-szakaszonként,
„c.” + számjegy, magyar idézőjel, néhány terminológiai kulcs; az adag második felétől a
terminológia-tábla kulcsai és a c:v előtti nagybetűs szó is). Ez nem kapu és nem kalibrálás, a
kapuk ítéletét nem helyettesíti; a fordító saját figyelmeztető listája.

**Terminológia-kivétel (`--kivetel`, a H0413 mintájára, indoklás a sor megjegyzésében):** két
szócikkben, mindkettő forrásbeli OCR-/rövidítés-ütközés: H1419 — a forrás „the h.p.” (high
priest = főpap) rövidítése nem oldalszám, ezért nem „o.” (`p.`); H6310 — a forrás két „accusative
as” részlete (Mal 2:9, 4Móz 9:17) az „according as” OCR-hibája, ezért nem tárgyeset
(`accusative`). Jóváhagyásuk a DT-F38c tétel része.

**Számok:** 81 szócikk a sorrend 47–127. sorából (H5927–H8179), ebből 80 kész, 1 a hibás
listán (H2719). A 80 kész szócikk: forrás 493 209 karakter, fordítás 516 621 karakter (arány
1,05). Kész összesen (BDB `teljes`): 72 + 80 = 152 szócikk; hátra 7 938 szócikk, 5 060 582
forráskarakter. A 4. adag a sorrend 113. sorával (H2719, a hibás listáról) indulna, majd a
128. sortól (H5046) folytatódna — a brief szerint az első olyan sor, amelynek Strong-számához
még nincs `teljes` sor.

**Ellenőrzés az adag végén:** teljes kapusor a 80 kész soron (`python
naplok/BDB_FORDITAS_kapuk.py --adag 3`): 80/80 átment, 0 bukott, 15 szócikk 13. kapus
JELZES-sel. `eszkozok/ellenoriz.py`: RENDBEN 11, SÉRTÉS 0, KÉZI 2, JELENTÉS 3.
`eszkozok/ellenorzes/futtat.py --valtozott adat/forditasok.tsv`: 0 találat. **Hibás lista:**
1 szócikk (H2719, 5. kapu: a `Zinjirli` → Zendzsirli kötelező alak első futásra „zincirli”, az
önújrapróbában kisbetűs „zendzsirli” — a kapu kis- és nagybetűt megkülönböztet), l.
`naplok/BDB_FORDITAS_hibas.tsv`.

**Önújrapróba** (mindig a fordítás javult, nem a kapu; kapukalibrálás nem volt). Elsőre átment
54 szócikk (köztük a H6310, amelynél a terminológia-kivétel előre, indoklással került a
hívásba). 26 szócikknél egy önújrapróba elég volt, egynél (H2719) nem; a 27 szócikk 32
kapujelzést adott:

| Kapu | Darab (szócikk) | Strong | Eset és javítás |
|---|---|---|---|
| 5 terminológia | 13 | H0589 (verb), H0369 (p., suffix), H0428 (suffix), H7218 (proper name, of a location), H7760 (Heb. a sziglában), H4325, H3205 (spiritual), H5307 (spirit), H1992, H6963 (prefix), H1419 (p. — kivétel), H7969 (Sabean), H2719 (Zinjirli — hibás lista) | a kötelező alak hiányzott vagy ragozott/szinonim alak állt („Igéhez”, „suffixumos”, „előtaggal”, „lelki”, „lelke”, „sabeus”, „zincirli”) — pótolva; H1419-nél forrásbeli rövidítés-ütközés, kivétellel |
| 9 tagolás | 6 | H1870, H0251, H4325, H1992, H5221, H4994 | a forrás betűjele a fordításban rossz helyre került (H1870 „fent a.;”); a forrás „Var. 23 compare” jelölőnek számító száma után vessző került (H0251) — a forrás alakja; a „c.” betűjel után számjegy állt, a kapu circa-kivétele miatt nem számított (H1992 „c. 2Móz”, H4994 „c. 3. személyben”) — „c. —”, illetve „c. a 3. személyben”; „e.” előtt „vizei.” (a kapu „i. e.” kivétele); a pont nélküli jelölő után zárójel állt („4 (halálosan)”) |
| 3 Károli | 5 | H5869, H0251, H4672, H8269, H4196 | nagybetűs szó közvetlenül c:v előtt („Benjáminén 18:16”, „Lábáné 29:12”, „alanya Isten 2:34”, „— A 15:22-ben”, „a Hóreben 24:4”) — átfogalmazva, illetve kettősponttal elválasztva |
| 4 formázás | 3 | H2063, H1323, H9008 | betoldott zárójel („kéziratok (MSS.)”, „unokák (leányunokák)”) — eltávolítva |
| 8 idézőjel | 2 | H1571, H4100 | betoldott „ ” (magyar megfelelő idézőjelben) — eltávolítva |
| 2 versszám | 1 | H5869 | elírt igehely (Ézs 37:29 a 37:17 helyett) — javítva |
| 1 görög–héber | 1 | H2063 | a forrás `\x99` vezérlőkaraktere két héber szakasz között kimaradt — visszaállítva |
| 11 könyvek | 1 | H6965 | a forrás „⟦héber⟧2Chr” alakja (a kapu látja) a fordításban latin betűhöz olvadt („vonzattal2Krón”) — szóköz |

*Két megjegyzés a táblához.* (1) H1992-nél a 9. kapu csak az első hiányzó jelölőt jelenti; a
három „c. + számjegy” helyet két futás tárta fel, ezt egy javítási körként kezeltem. (2) A H4994
és a H4196 hibáját a saját előellenőrzés előre jelezte („c.” + számjegy), illetve a bővítése után
jelezte volna; a figyelmeztetést nem vettem figyelembe — ez a fordító figyelmetlensége, nem a kapu
hibája.

**Forráshiba a fordításban, hűen átvéve** (13. kapu JELZES, nem gátoló; a DT-F38 (b) szerint a
futást nem állítja meg): 15 szócikk, a lista a lenti táblázat alatt. Néhány jellemző: H5650
„Jonah 14:25” (személynév + láncolt hely, a fordításban „Jónás Jón 14:25”), H6258 „2Ki 46:34”
(= 1Móz 46:34), H3701 „Ex 43:21” (= 1Móz 43:21), H4196 „Judg 22:28”, H5002 „Jer 57:57”. A forrást
a menet nem javítja (brief, Nem cél).

*Az alábbi alszakasz a `python naplok/BDB_FORDITAS_M1_nezet.py --adag 3` kimenetének első része
(a minta elhagyva: a brief szerint a hosszabb minta csak az M1-ben kötelező).*

### Kapueredmények (adag 3, 80/81 szócikk kész)

| Strong | Forrás kar. | Fordítás kar. | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 | 11 | 12 | 13 | Átment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H5927 | 11993 | 13205 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.10) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5869 | 8186 | 8872 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8141 | 2835 | 3176 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.12) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0589 | 821 | 881 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H7971 | 10177 | 11402 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.12) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H2009 | 4528 | 4522 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4191 | 7576 | 8206 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8033 | 3939 | 3972 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3063 | 2352 | 2469 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0398 | 6538 | 7138 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H5650 | 5720 | 6096 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H0369 | 7009 | 7033 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0802 | 3501 | 3742 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3651 | 11308 | 11517 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8147 | 3139 | 3567 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.14) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1571 | 6184 | 6043 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.98) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4872 | 1924 | 2042 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4100 | 12145 | 11759 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.97) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H9008 | 3964 | 3927 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.99) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0428 | 1881 | 1924 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0408 | 2360 | 2334 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.99) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0310 | 4671 | 4735 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1870 | 11028 | 11360 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H5375 | 431 | 436 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3389 | 2226 | 2337 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4714 | 2660 | 2814 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0251 | 2247 | 2482 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.10) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H6965 | 17763 | 19160 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H2063 | 12696 | 12384 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.98) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H7218 | 5944 | 6167 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3820 | 8365 | 8787 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1323 | 6088 | 6281 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H7760 | 15455 | 16881 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H3967 | 5186 | 5423 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4325 | 5707 | 5929 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3541 | 2226 | 2105 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.95) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0582 | 1210 | 1295 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1471 | 3612 | 3799 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5674 | 15437 | 16274 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1992 | 5032 | 5015 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0120 | 3018 | 3168 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H2022 | 12901 | 13147 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H2896 | 12205 | 12316 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1419 | 3929 | 4068 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5975 | 8714 | 9451 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H0505 | 283 | 315 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.11) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H6963 | 4447 | 4667 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8478 | 6783 | 6870 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H5221 | 11084 | 11893 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3205 | 7093 | 7633 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H6310 | 7429 | 7704 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H6680 | 4989 | 5567 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.12) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5750 | 5725 | 5746 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H6635 | 5222 | 5841 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.12) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8104 | 7813 | 8488 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4672 | 12297 | 13084 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H7227 | 5273 | 5611 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5769 | 7731 | 7951 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5307 | 11203 | 12066 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H6258 | 4010 | 4081 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H7969 | 2265 | 2547 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.12) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4941 | 5653 | 5844 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8269 | 6304 | 6869 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8064 | 5277 | 5624 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4310 | 7941 | 7853 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.99) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H8432 | 2586 | 2769 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H2719 | 3965 | — | — | — | — | — | — | — | — | — | — | — | — | — | nincs fordítás |
| H7586 | 532 | 576 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0996 | 4610 | 4534 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.98) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H4994 | 3007 | 3018 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3701 | 5028 | 5265 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H4196 | 7160 | 7165 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.00) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H3220 | 4410 | 4759 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H7651 | 3533 | 3857 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H2091 | 7474 | 7862 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H3381 | 11208 | 11619 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.04) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H0784 | 4191 | 4281 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H7307 | 10184 | 10402 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H1129 | 7002 | 7542 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |
| H5002 | 1709 | 1843 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.08) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | JELZES | igen |
| H8179 | 4922 | 5234 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.06) | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | igen |

Összesen: forrás 493209, fordítás 516621 karakter.

13. kapu (JELZES, nem gátoló): H0398 — a könyv fejezetszámánál nagyobb fejezet: 3Móz 28; H5650 — a könyv fejezetszámánál nagyobb fejezet: Jón 14; H4100 — a könyv fejezetszámánál nagyobb fejezet: Bír 33; H1870 — a könyv fejezetszámánál nagyobb fejezet: Én 34; H0251 — a könyv fejezetszámánál nagyobb fejezet: Jóel 7; H2063 — a könyv fejezetszámánál nagyobb fejezet: Eszt 25; H7760 — a könyv fejezetszámánál nagyobb fejezet: 3Móz 40, 5Móz 45; H5975 — a könyv fejezetszámánál nagyobb fejezet: 2Kir 31; H8478 — a könyv fejezetszámánál nagyobb fejezet: Dán 18, Dán 21, Dán 24; H5750 — a könyv fejezetszámánál nagyobb fejezet: 2Krón 43, 2Krón 45; H4672 — a könyv fejezetszámánál nagyobb fejezet: Préd 25; H6258 — a könyv fejezetszámánál nagyobb fejezet: 2Kir 46; H3701 — a könyv fejezetszámánál nagyobb fejezet: 2Móz 43; H4196 — a könyv fejezetszámánál nagyobb fejezet: Bír 22; H5002 — a könyv fejezetszámánál nagyobb fejezet: Jer 57.

## DT-F38c alkalmazása (F38.137–)

*A felhasználó döntése (2026.10.02): (a) 4. adag, költség- és vetítési jelentéssel; (b) a
H1419 és H6310 kivétele szócikkszinten; (c) H2719 újrafordítása a 4. adag elején; (d)
promptpontosítás + az 5. kapu kis/nagybetű-gépicseréje; (e) a 3. és a 9. kapu javítása. A
rögzítés: F38.137.*

### (e) Kapujavítás (F38.138)

**3. kapu (`ellenoriz_karoli`).** A c:v előtti nagybetűs szó, amely nem könyvnév, nem hiba.
Könyvnévnek az számít, ami a könyv-leképezés kulcsa (angol/STEPBible/forrásalak, pl. `Gen`,
`Ezek`, `Malachi`), vagy számmal kezdődik (`1Ezék`); ezek továbbra is SÉRTÉS-t adnak. Ami nem
könyvnév (`Isten 23:16`, `Júdáról 12:6`, `A 4:16`, `a Hóreben 24:4`), RENDBEN, a részletben
„nagybetus szo igehely elott, nem konyvnev: …”. A rossz vagy hiányzó Károli-rövidítést
(pl. kiírt „Ézsaiás 3:4”) a 11. kapu fogja meg (a forrás és a fordítás könyvei darabra
egyeznek) — ezt teszt rögzíti.

**9. kapu (`ellenoriz_tagolas`, `tagolas_igazitas`).** (1) A `c.`, `d.`, `f.`, `i.` betűjel a
forrás oldalán nem kötelező (`OPCIONALIS_BETU`), mert a BDB-ben rövidítésként is áll (`c.`
circa, `d.` day, `f.` father/feminine/following, `f. below`, `i. below`): ha a fordításban az
előző és a következő kötelező jelölő között megvan, illeszkedik, ha nincs, a kapu átlépi (a
részletben „atlepett opcionalis betujel (c/d/f/i): n”). Az opcionális jelölő nem nyelheti el a
következő kötelezőt (a keresés a következő kötelező jelölő első találatáig tart). A többi betűjel
(a., b., e., g., h.), a számok, a római és a zárójeles jelölők kötelezők maradnak. (2) A
rövidítés-kivételek (`c. 100` circa, `273 f.`, `i. e.`, `e. g.`) csak a forrás oldalán szűrnek;
a fordítás oldalán a többlet jelölő ártalmatlan (részsorozat-vizsgálat), a kihagyás viszont
hamis hiányt adott (`c. 1Móz`, `vizei. e.`). A „c. —” kerülőalakra ezzel nincs szükség.

**Tesztek:** `eszkozok/teszt_forditas_kapuk.py` +11 (`KaroliNagybetusSzo` 4, `TagolasRovidites`
7), összesen 34, mind RENDBEN; a többi `eszkozok/teszt_*.py` is RENDBEN.

**Regresszió** (`python naplok/BDB_FORDITAS_regresszio.py`, előtte/utána JSON-összevetés): a
152 rögzített BDB `teljes` szócikk (a #28 26 sora és az F38 1–3. adagjának 126 sora) mindegyikén
a teljes kapusor; a javítás előtt 152/152 átment, utána 152/152 átment, **megváltozott
kapueredmény 0, új bukás 0**.

**A korábbi 3. és 9. kapus önújrapróbák** (a 2. és 3. adag napló-táblázatai szerint; az elbukott
első vázlatok nincsenek meg, ezért a hatást a táblázat leírása alapján, az esetek mintájával
becsülöm — tesztesetként rögzítve):

| Adag | 3. kapu (szócikk) | ebből a javított kapun átmenne | 9. kapu (szócikk) | ebből átmenne | önújrapróba összesen | ebből elmaradt volna (csak 3./9. kapus volt) |
|---|---|---|---|---|---|---|
| 2 | 7 | 7 (mind nem könyvnév) | 5 | 5 (H3808 `c. 1Móz`; H1961, H3117, H3027, H0001 `f./i./d.` rövidítés) | 23 | 8 (H3588, H3478, H6440, H0376, H3318, H3808, H3027, H0001) |
| 3 | 5 | 5 (mind nem könyvnév) | 6 | 3 (H1992, H4994 `c.` + számjegy; H4325 `vizei. e.`) | 27 | 4 (H4672, H8269, H4196, H4994) |

A 3. adag 9. kapus maradéka valódi tagolási hiba vagy más heurisztika: H1870 (a forrás `a.`
betűjele rossz helyre került), H0251 (`Var. 23 compare` után vessző), H5221 (pont nélküli
jelölő után zárójel: „4 (halálosan)”).

**Kódolás-ellenőrzés** (az önújrapróba-napló inline echo-s sora; a H2719 sora a
`naplok/BDB_FORDITAS_hibas.tsv`-ben, F38.121): a `naplok/BDB_FORDITAS_*` fájlok, a
`DONTESEK.md` és a brief szigorú UTF-8-dekódolással mind érvényes; U+FFFD, BOM, CR,
vezérlőkarakter és mojibake-gyanú (`Ã`, `Å`, `â€`) 0; a `hibas.tsv` mezőszáma egységes (4). A
napló nem NFC-normalizált, de csak a forrásból betűhűen átvett héber szavaknál (1078 szó; görög
és latin betűs 0) — ez a forrás alakja, nem sérülés. Javítás nem kellett.

### (b) A két szócikkszintű kivétel (F38.139)

Az `adat/forditasok.tsv` H1419 és H6310 sorának `megjegyzes` mezője kiegészült: „szócikkszintű
kivétel, jóváhagyva: DT-F38c (b), 2026.10.02 — a terminológia általános sora nem változik”; a
H6310-nél ezen felül „forráshiba-jelzés (13. kapu, kézi): OCR-hiba, a forrás „accusative as” =
„according as” (Mal 2:9, 4Móz 9:17) …”. A 13. kapu ezt gépileg nem látja (nem fejezetszám-hiba),
ezért a `naplok/BDB_FORDITAS_kapuk.py` a megjegyzés kézi jelzését 13. kapus JELZES-ként listázza
(a 3. adagon így 16 jelző szócikk a korábbi 15 helyett). Más sor és mező nem változott (a szkript
írás előtt bájtra ellenőrizte); az `adat/terminologia.tsv` változatlan. `ellenoriz.py`: SÉRTÉS 0.

### (d) Prompt v4.1 és az 5. kapu kis/nagybetű-gépicseréje (F38.140)

**Prompt v4.1** (`forditas/prompt_v4.md`, a verziónapló v4.1 sora): új blokk a BDB-blokk után,
„Kiegészítő szabály (v4.1) — kötelező terminológiai alakok előgyűjtése”: a vázlat előtt a
forrásban előforduló kapus terminológia-kulcsok kötelező magyar alakja betűhűen, kiemelve a
spirit → szellem, spiritual → szellemi, Sabean → szabeus, Zinjirli → Zendzsirli alakot; az új
`{{KOTELEZO_ALAKOK}}` helyőrzőt az `emeles.py prompt_epit` a forrás(darab) kulcsaival tölti
ki, ugyanazzal a kulcsolással, amit az 5. kapu követel. A menet (egy végrehajtó, a prompt
szabályai szerint) a vázlat előtt az `python eszkozok/emeles.py kotelezo <Strong>` kimenetét
gyűjti ki. A v3 és a v4.0 sorai nem változtak.
Hash-nyom: `forditas/prompt_v4.md` sha256 — v4.0 (F38.139-ig): `6426abdd642561da…e049d4`;
v4.1 (F38.140-től): `aa08b93ce2b3e7d3…8edf32`. A 4. adag sorainak megjegyzése „prompt v4.1”.

**5. kapu kis/nagybetű-gépicsere** (`forditas_kapuk.terminologia_kisnagybetu_csere`, hívja az
`emeles.utofeldolgoz` a javítóréteg után, a kapuk előtt): ha a forrásban a kulcs megvan, a
kötelező alak betűhűen sehol nincs a fordításban, de kis/nagybetű-függetlenül szókezdeten
megvan, a javítóréteg a kötelező alakra cseréli; a csere a változások között (`javitoreteg:
5_kisnagybetu zendzsirli -> Zendzsirli (Zinjirli)=1`) és az `ellenoriz --ki` futásakor a
`naplok/FORDITAS_kisnagybetu_csere.tsv`-ben naplózódik (strong, csere, darab, dátum). Más
eltérés (pl. „zincirli”) továbbra is SÉRTÉS. Tesztek: +8 (`KisNagybetuCsere` 6,
`PromptKotelezoAlakok` 2), összesen 42, mind RENDBEN; regresszió a 152 szócikken: változás 0.
