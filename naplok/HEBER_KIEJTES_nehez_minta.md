# Gépi héber kiejtés — nehéz esetek mintája a bekötés előtt (DT-F131y ⛔)

*A DT-F131y bekötés előtti feltétele. Csak napló: adat (`adat/`) nem változott, lexikonlap nem generálódott újra, a kivételtábla ס-sorai még nincsenek javítva. A javaslat-oszlop a felhasználó jóváhagyására vár.*

- **Modell:** `claude-opus-5-5`
- **Proveniencia (gépi oszlopok):** `scope=adat/elofordulasok.tsv (a 8 lexikonlap motívumai: ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001; héber Strongok) + konkordancia/TAHOT_kivonat.tsv | forras=naplok/HEBER_KIEJTES_nehez_minta.py (seed=20261030) | ts=2026-10-30`
- **Proveniencia (javaslat-oszlop):** `manual` — a session saját héber nyelvtani ítélete, nem lekérdezés; a STEP-átírás csak támasz.
- **Kimenet:** `naplok/HEBER_KIEJTES_nehez_minta.tsv`. Újrafuttatás: `python naplok/HEBER_KIEJTES_nehez_minta.py`.

## 1. Röviden

| | egyezik a javaslattal |
|---|---|
| gépi, a DT-F131y szerint (kámec-heurisztika: meteg nélküli zárt szótag → o) | **41/49 (84%)** |
| gépi, alternatív kámec-szabállyal (a kámec alapból gádol, kátán csak pozitív jelre; a hosszú magánhangzó utáni sevá kiejtett) | **44/49 (90%)** |

A hibák két helyen vannak:
- a **kámec kátán gyanús** szavakban (10-ből 6, illetve az alternatívával 10-ből 3);
- a **Jeruzsálem** qere-alakjában (2), amely a kivétellistára tartozik.

A sevá, a dáges forte, a furtív patah és a makkef csoportjának 34 sora hibátlan.

## 2. A minta

- **Szóösszerakás.** A TAHOT-sorokból teljes szó készül (DT-F131y (5)): az előtag H9001–H9009 (vav, elöljárók, ‑ש, kérdő hé, névelő); a toldalék H9010-től (irányjelölő hé, paragogikus nun, névmási toldalékok). A makkef jele, ha a szó utolsó elemének STEP-átírása `-`-re végződik.
- **Jelöltek.** Az összes szó a 8 lexikonlap motívumainak héber verseiben: 2 567 szó, 1 460 egyedi pontozott alak. A motívum Strongján álló szó (*motívumszó*) mindig előre kerül. A motívumszavak készlete kicsi: 88 egyedi alak, és köztük nincs furtív patah vagy ketiv/qere. Ezért a minta a versek többi szavából egészül ki.
- **Kategóriák** (egyedi alak; ebből motívumszó / összes):
  - kámec kátán gyanú (kámec után sevás betű, hátef-kámec, U+05C7 vagy makkef): 2 / 57
  - nem szókezdő sevá: 36 / 439
  - furtív patah: 0 / 17
  - dáges forte: 15 / 391
  - ketiv/qere (JHVH, Jeruzsálem): 0 / 5
  - makkef: 3 / 91
- **Kvóta** 10 / 10 / 8 / 8 / 6 / 8, seed 20261030. A ketiv/qere csak 5 alakot adott, ezért 49 a mintaméret.
- **Konvenciók a gépi oszlopban** (DT-F131y):
  - ס és שׂ = sz;
  - a szókezdő begadkefatról a pontozás dönt;
  - a szókezdő kötőszói וּ = ú, utána a sevá kiejtett (új szabály);
  - makkef előtt a zárt szótag kámece = o (új szabály).

  A két új szabály a mért A/B halmazt nem érinti; a `naplok/HEBER_KIEJTES_meres.py` újrafuttatása bájtra azonos kimenetet adott.

## 3. Táblázat

A „=” azt jelzi, hogy az alternatív szabály ugyanazt adja. A javaslat oszlop csak eltérésnél kitöltött.

| # | kategória | motívumszó | igehely | Strong | alak | STEP | gépi (DT-F131y) | gépi (alternatív kámec-szabály) | javaslat, ha eltér | megjegyzés |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | kámec kátán gyanú | igen | 1Krón 20:4 | H7497 | הָרְפָאִים | `ha. + re.fa.'Im` | horfáím | hárefáím | **hárefáím** | névelő + ר előtti pótlónyújtás: kámec gádol, utána kiejtett sevá; meteg nincs a szövegben |
| 2 | kámec kátán gyanú | igen | Józs 17:15 | H7497 | וְהָרְפָאִים | `ve. + ha. + re.fa.'Im` | vehárefáím | = |  |  |
| 3 | kámec kátán gyanú | nem | Jón 3:8 | H2394 | בְּחָזְקָה | `be. + cha.ze.Kah` | bechozká | becházeká |  | kámec kátán helyes (bəḥozqāh); az alternatív szabály elrontaná |
| 4 | kámec kátán gyanú | nem | 1Móz 1:2 | H1961 | הָיְתָה | `ha.ye.Tah` | hojtá | hájetá | **hájetá** | Qal perf. 3fs (hājəṯāh): kámec gádol + kiejtett sevá |
| 5 | kámec kátán gyanú | nem | Ézs 17:5 | H7641 | שִׁבֳּלִים | `shi.bo.Lim` | sibbolím | = |  |  |
| 6 | kámec kátán gyanú | nem | 1Móz 12:8 | H0168 | אָהְָלוֹ | `'o.ho.L + o` | áháló | = | **oholó** | ʾohŏlô: kámec kátán + a hé alatt sevá+kámec (hátef-kámec más kódolással) |
| 7 | kámec kátán gyanú | nem | Ézs 28:15 | H5641 | נִסְתָּרְנוּ | `nis.Ta.re.nu` | nisztárenú | = | **nisztárnú (?)** | pauzális alak, hangsúlyos zárt szótag: a sevá néma (a STEP kiejtettnek írja) — bizonytalan |
| 8 | kámec kátán gyanú | nem | 4Móz 16:30 | H1104 | וּבָלְעָה | `u. + val.'Ah` | úvolá | úváleá | **úváleá** | Qal perf. 3fs (bāləʿāh): kámec gádol + kiejtett sevá |
| 9 | kámec kátán gyanú | nem | 5Móz 2:11 | H2803 | יֵחָשְׁבוּ | `ye.cha.she.Vu` | jéchosvú | jéchásevú | **jéchásevú** | Nif. impf. 3mp (yēḥāšəḇû): kámec gádol + kiejtett sevá |
| 10 | kámec kátán gyanú | nem | 1Móz 3:16 | H4910 | יִמְשָׁל | `yim.shol-` | jimsol | = |  | makkef előtti zárt szótag: kámec kátán (új szabály) |
| 11 | nem szókezdő sevá | igen | Ézs 64:6 | H8034 | בְשִׁמְךָ | `ve. + shim. + Kha` | vesimchá | = |  |  |
| 12 | nem szókezdő sevá | igen | Ámós 9:2 | H7585 | בִשְׁאוֹל | `vi + sh.'ol` | visól | = |  |  |
| 13 | nem szókezdő sevá | igen | 1Kir 18:25 | H7121 | וְקִרְאוּ | `ve. + kir.'U` | vekirú | = |  |  |
| 14 | nem szókezdő sevá | igen | 1Móz 6:12 | H7843 | נִשְׁחָתָה | `nish.Cha.tah` | nischátá | = |  |  |
| 15 | nem szókezdő sevá | igen | Zsolt 78:15 | H8415 | כִּתְהֹמוֹת | `ki + t.ho.Mot` | kithómót | = |  |  |
| 16 | nem szókezdő sevá | igen | 4Móz 13:34 | H5303 | הַנְּפִילִים | `ha. + ne.fi.Lim` | hannefílím | = |  |  |
| 17 | nem szókezdő sevá | igen | 1Móz 6:12 | H7843 | הִשְׁחִית | `hish.Chit` | hischít | = |  |  |
| 18 | nem szókezdő sevá | igen | 1Móz 4:26 | H7121 | לִקְרֹא | `li + k.Ro'` | likró | = |  |  |
| 19 | nem szókezdő sevá | igen | 1Kir 18:26 | H7121 | וַיִּקְרְאוּ | `va + i.yik.re.'U` | vajjikreú | = |  |  |
| 20 | nem szókezdő sevá | igen | 1Kir 18:24 | H7121 | וּקְרָאתֶם | `u. + ke.ra.Tem` | úkerátem | = |  |  |
| 21 | furtív patah | nem | Józs 17:15 | H3091 | יְהוֹשֻׁעַ | `ye.ho.Shu.a'` | jehósua | = |  |  |
| 22 | furtív patah | nem | 1Kir 18:26 | H4196 | הַמִּזְבֵּחַ | `ha. + miz.Be.ach` | hammizbéach | = |  |  |
| 23 | furtív patah | nem | 1Móz 3:18 | H6779 | תַּצְמִיחַ | `tatz.Mi.ach` | tacmíach | = |  |  |
| 24 | furtív patah | nem | 1Móz 12:8 | H4196 | מִזְבֵּחַ | `miz.Be.ach` | mizbéach | = |  |  |
| 25 | furtív patah | nem | Péld 21:16 | H5117 | יָנוּחַ | `ya.Nu.ach` | jánúach | = |  |  |
| 26 | furtív patah | nem | 1Móz 8:21 | H7381 | רֵיחַ | `Rei.ach` | réach | = |  |  |
| 27 | furtív patah | nem | 1Móz 6:17 | H7307 | רוּחַ | `Ru.ach` | rúach | = |  |  |
| 28 | furtív patah | nem | Hab 1:2 | H3467 | תוֹשִׁיעַ | `to.Shi.a'` | tósía | = |  |  |
| 29 | dáges forte | igen | Jób 11:8 | H7585 | מִשְּׁאוֹל | `mi. + she.'ol` | misseól | = |  |  |
| 30 | dáges forte | igen | 1Móz 2:7 | H2416 | חַיָּה | `chai.Yah` | chajjá | = |  |  |
| 31 | dáges forte | igen | 1Móz 2:7 | H2416 | חַיִּים | `chai.Yim` | chajjím | = |  |  |
| 32 | dáges forte | igen | 1Móz 3:16 | H6093 | עִצְּבוֹנֵךְ | `i.tze.vo.Ne + kh` | iccevónéch | = |  |  |
| 33 | dáges forte | igen | Zsolt 106:9 | H8415 | בַּתְּהֹמוֹת | `ba. + te.ho.Mot` | battehómót | = |  |  |
| 34 | dáges forte | igen | 1Móz 5:29 | H6093 | וּמֵעִצְּבוֹן | `u. + me. + 'i.tze.Von` | úméiccevón | = |  |  |
| 35 | dáges forte | igen | 1Móz 4:7 | H2403 | חַטָּאת | `cha.Tat` | chattát | = |  |  |
| 36 | dáges forte | igen | 1Móz 8:21 | H7043 | לְקַלֵּל | `le. + ka.Lel` | lekallél | = |  |  |
| 37 | ketiv/qere | nem | Jóel 2:32 | H3389 | וּבִירוּשָׁלִַם | `u. + vi. + ru.sha.Lim` | úvírúsálim | = | **úvírúsálajim** | qere perpetuum (Jerúsálajim): kivétellista |
| 38 | ketiv/qere | nem | Józs 15:8 | H3389 | יְרוּשָׁלִָם | `ye.ru.sha.Lim` | jerúsálim | = | **jerúsálajim** | qere perpetuum: kivétellista |
| 39 | ketiv/qere | nem | Ez 26:19 | H3069 | יְהוִה | `Yah.weh` | JHVH | = |  | Adonáj JHVH (qere: Elóhím); a JHVH-konvenció szerint |
| 40 | ketiv/qere | nem | 1Móz 3:14 | H3068 | יְהֹוָה | `Yah.weh` | JHVH | = |  |  |
| 41 | ketiv/qere | nem | 1Kir 18:24 | H3068 | יְהוָה | `Yah.weh` | JHVH | = |  |  |
| 42 | makkef | igen | 1Móz 6:2 | H1121 | בְנֵי | `ve.nei-` | vené | = |  |  |
| 43 | makkef | igen | 1Kir 18:24 | H8034 | בְשֵׁם | `ve. + shem-` | vesém | = |  |  |
| 44 | makkef | igen | Hab 2:17 | H2555 | וַחֲמַס | `va. + cha.mas-` | vachamasz | = |  | a lemma kivétele „hámás” (D36, ח → h); a ragozott gépi alak ch + sz — l. 4. pont |
| 45 | makkef | nem | 1Móz 44:29 | H1571 | גַּם | `gam-` | gam | = |  |  |
| 46 | makkef | nem | Zsolt 74:20 | H4285 | מַחֲשַׁכֵּי | `ma.cha.sha.kei-` | machasakké | = |  |  |
| 47 | makkef | nem | Józs 15:8 | H1516 | גֵי | `gei-` | gé | = |  |  |
| 48 | makkef | nem | Jer 51:46 | H6435 | וּפֶן | `u. + fen-` | úfen | = |  | szókezdő kötőszói וּ → ú (új szabály) |
| 49 | makkef | nem | 1Móz 3:16 | H0413 | וְאֶל | `ve. + 'el-` | veel | = |  |  |

## 4. Jóváhagyásra (⛔ — a felhasználó dönt)

1. **A javaslat-oszlop 8 alakja** (1, 4, 6, 7, 8, 9, 37, 38) és a többi 41 sor gépi alakja, amelyet változatlanul elfogadhatónak tartok. A 7. sor (נִסְתָּרְנוּ) bizonytalan: a pauzális alakban a sevát némának tartom, a STEP kiejtettnek írja.
2. **A kámec-szabály.** Javaslatom az alternatíva: a kámec alapból gádol (á); kátán (o) csak pozitív jelre:
   - kifejezett kámec kátán (U+05C7);
   - hátef-kámec előtt;
   - makkef előtti zárt szótagban;
   - a kivétellistán (pl. כָּל → kol, חָכְמָה → chochmá).

   A hosszú magánhangzó utáni sevá kiejtett. Indok: a TAHOT-ban a meteg gyakran hiányzik, ezért a mostani heurisztika gádol helyett kátánt ad. A mintában ez 6 → 3 hibát jelent. A proxyban (`naplok/HEBER_KIEJTES_meres.md` 4.4) is kettőt javít a korábbi ötből (יֹּאמְרוּ, אָכְלוּ). A maradék kátán-esetek (3. sor בְּחָזְקָה, 6. sor אָהֳלוֹ) a kivétellistára kerülnének.
3. **Kivétellista-jelöltek** (a `adat/kiejtes_kivetelek.tsv`-be, kézi jóváhagyással, DT-F131y (6)):
   - יְרוּשָׁלִַם → jerúsálajim (minden előtaggal);
   - כָּל → kol;
   - a kámec-kátán gyakori szavai, amelyek a lapokon előfordulnak (a 3. és a 6. sor).
4. **A H2555 következetessége.** A lemma kézi kivétele „hámás” (D36, ח → h). A DT-F131y (3) szerint a ס = sz, így a lemma alakja „hámász” lesz. A ragozott gépi alak viszont ch-t ad (44. sor: וַחֲמַס → „vachamasz”). Kérdés: a D36 h-ja a ragozott alakokra is vonatkozzon-e (pl. „vahamasz”), vagy csak a lemmára?
