# OLVASOI_PILOT — a BDB-szeletelő F60.25-ös javításának átnézése (F60.35–F60.38)

*A felhasználó kérése (chat, 2026-10-12): „nézd át most” a F60.25 által megváltoztatott 19 szócikket. Háttér: `OLVASOI_PILOT_naplo.md` 4., 5., 9. és 11. pont. A szeletelő: `eszkozok/olvaso_pilot/bdb_szelet.py`. „Régi”: az F60.25 előtti változat (`18a927f6^`), „új”: az F60.25 (`18a927f6`), „végleges”: a mostani (F60.35).*

## 1. Eredmény egy bekezdésben

A 19 szócikk közül **11 javult, 5 romlott, 3 mindkét változatban hibás** (a H7121 külön, az F60.25 célszócikke: javult). A három „mindkettő hibás” közül a H1869 és a H0157 a végleges bontásban helyes; a H0834-nél a számsorrend helyes, de az 1. jelentés eleje pontatlan: ismert hiba. A romlás oka nem a H7121-javítás volt, hanem két mellékhatása: (a) a „— 1” utáni külön ág nem-igéknél a szócikk egy későbbi „— 1”-ére ugrott és a számozás összeomlott (H9003, H3588, H3027, H5973, H2896); (b) a személyszám-jelölők („1. egyes szám אֵהָ֑ב”) továbbra is jelentés-sorszámnak számítottak, ha a szócikkben bármi más megzavarta a külön ágat. Az átnézés közben kiderült, hogy a 19-es lista **alulszámlált**: a naplóbeli mérték (azonos törzsnevek, csak a jelentés-jelek listája) a szócikkeket kihagyta, amelyekben a törzsnevek is változtak (96 szócikk) vagy a jelek listája azonos, a szövege nem (v. 4. pont). Ezeket is besoroltam (4. pont); egyenként a 19-et és a kiemelt eseteket olvastam végig, a többit automatikus ellenőrzéssel és szúrópróbával soroltam be, ezt a 4. pont külön jelzi.

## 2. A 19 szócikk és a H7121

Jelölés: `Törzs [jelentés-jelek]`; „–” a sorszám nélküli fej (alakok), a zárójelben az alpontok. A „végleges” az F60.35 utáni állapot.

| Strong | régi bontás | új bontás (F60.25) | végleges bontás | kategória (új a régihez képest) | indoklás (a szócikk szövegéből) |
|---|---|---|---|---|---|
| H9003 | [1,2(abc),3,4,5,6,7(abcde),8(abcde)] | [–,1,2,3,4(abcde),5,6,7,8(abcde)] | = régi | **romlott**; végleges = a régi (helyes) | „I. Benne: 1 szoros értelemben, valamely helyen való elhelyezkedésről … 2 sokaság közepén való jelenlétről: között … 3 a teret körülzáró határokra …” — a számozás helyes volt; az új ág egy későbbi „— 1 valaminél, mellett” (II. szakasz) elé vitte a határt. |
| H0834 | [1,2,3,4(abcd),5,6,7(abc),8(abcdef)] | [–,1(abcde),2,3(ab),4(abcd)] | [1,2,3,4(abcd),5,6,7(abc),8(abcdef)] | **mindkettő hibás**; végleges: javult, **ismert hiba** | A régi 1. és 2. „jelentése” bibliográfia: „(eredete kétséges: 1 Tsepreghi^Diss. Lugd. 171. o.” és „2 Phi^St. C. 73”. Az új a כַּאֲשֶׁר al-szócikk „— 1 aszerint, ami” számozását vette főnek. Végleges: a sigla (`^`) előtti szám nem jelölő; a 2–8. jelentés helyes („2 a אֲשֶׁר névmási affixummal …”, „8 A אֲשֶׁר … kötőszóvá válik”), az 1. jelentés viszont a „… 1 tűnik előnyösebbnek” mondatnál indul, a valódi „Közelebbről 1 magában foglalja” helyett. |
| H3588 | [1(abcdefg),2(abc),3(abcde)] | [–,1(abc)] | = régi | **romlott**; végleges = régi (helyes) | „— 1 hogy (ὅτι, német dass): a. … 2. a. Időről: amikor … 3 Mert, mivel ὅτι —”; az új ág a IV. szakasz „— 1 mindkét partikula megtartja” jelentésére ugrott. |
| H0935 | Qal [–,1,2,3(a–g),4]; Hiph [–,1,2(a–g)]; Hoph [–(abc)] | Qal [–,1(ab),2(a–g),3,4]; Hiph [–,1(a–g),2(a–e)]; Hoph [–(abc)] | = új | **javult** | A régi „1”, „2” jelölői az alakok személyszámai („1. egyes szám הֵבֵאתִי”, „hímnemű többes szám הֲבֵאתֶם”); az új: Qal „1 bemenni, אֶל követi”, „2 jönni (közeledni, megérkezni)”, „3 járni, azaz jár valakivel”, „4 menni (vö. הלך) a beszélőtől el”; Hiph „1 bejönni engedni, bevinni”, „2 eljönni engedni, hozni”. |
| H3027 | [1(ab),2,3(a–i)] | [–,1,2] | = régi | **romlott**; végleges = régi (helyes) | „1 az ember keze … 2 Képletesen = erő, hatalom … 3 Képletesen = oldal”; az új ág a későbbi „— 1” után indult és a 3. jelentést elvesztette. |
| H5973 | [1(a–g),2,3(a–e),4(ab),5(a–d)] | [–,1(ab),2] | = régi | **romlott**; végleges = régi (helyes) | „1 közösségről és társaságról (latin cum) … 2 Helyről: közel, mellett … 3 Személyekről a עִם különösen … 5 Metaforikusan: együtt = valami ellenére”; az új ág 5 helyett 2 jelentést hagyott. |
| H2896 | [1(abcd),2(abcde),3(abcde),4(ab),5…8,9(ab),10(ab)] | [–,1,2,3,4(ab)] | = régi | **romlott**; végleges = régi (helyes) | „1 kellemes, az érzékeknek tetsző … 10 jó (erkölcsileg), helyes”; az új ág 10 helyett 4 jelentést hagyott. |
| H3205 | Qal [–,1,2,3(abc)]; … Hiph [–,1,2] | Qal [–,1(abc),2(ab),3]; … | = új | **javult** | A régi Qal „1”, „2” = „egyes szám suffixummal יְלִדְתִּ֫י” személyszámok, az alpontok a 3-hoz tapadtak. Új: „1 szülni, világra hozni: a–c”, „2 ritkábban nemzeni: a–b”, „3 Zak 13:3 … mindkét szülőről”. |
| H3772 | Qal [–,1,2,3(ab),4]; Niph [–,1(abc),2,3,4]; … | Qal [–,1(ab),2,3,4]; … | = új | **javult** | A régi Qal „1” = „egyes szám כָּרַתִּי” személyszám; új: „1 levágni: a–b”, „2 kivágni … fákat”, „3 faragni, épületfát”, „4 ׳כ בְּרִית szövetséget vágni”. |
| H3559 | Niph [–,1(a–d),2]; Hiph […]; Hoph […] | Niph [–,1(a–d),2,3,4]; … | = új | **javult** | A régi Niph`al 3. és 4. jelentése („3 felkészülni, készen lenni, személyről Ámós 4:12”, „4 passzívan: előkészíttetni, ítéletekről Péld 19:29”) a Hiph`il fej elejére került („3); helyesen megállapodni …”). |
| H5800 | Qal [–,1,2(a–k),3]; … | Qal [–,1(a–k),2(a–g),3]; … | = új | **javult** | A régi „1” = „egyes szám suffixummal עֲזַבְתִּיךָ”; új: „1 elhagyni, tárgyesettel (a–k)”, „2 elhagyni, otthagyni, cserbenhagyni: (a–g)”, „3 elereszteni”. |
| H0157 | Qal [–,1,2,3,4,5]; … | Qal [–,1]; … | Qal [–,1,2,3,4,5]; … | **mindkettő hibás**; végleges **javítva** | Régi: az 1., 2. „jelentés” személyszám („1. egyes szám אֵהָ֑ב”, „2. hímnemű többes szám תְּאֵהֲבוּ”), az igazi 1. és 2. egybeolvadt. Új: a valódi „2” előtt nincs írásjel („… l. különösen lent a participiumot 2 ritkábban az étvágyról …”), ezért 2–5 elveszett. Végleges: „1 emberi szeretet …”, „2 ritkábban az étvágyról”, „3 szeretet Isten iránt”, „4 különösen a participium”, „5 az isteni szeretetről”. |
| H3201 | Qal [–,1,2(a–i),3] | Qal [–,1(a–i),2(abc),3] | = új | **javult** | Régi „1” = „egyes szám יָכֹלְתִּי”; új: „1 képesnek lenni … (a–i)”, „2 felülkerekedni: (abc)”, „3 abszolút használatban”. |
| H7812 | Hiph [–,1,2(abcd),3] | Hiph [–,1(abc),2(abcd),3] | = új | **javult** | Régi „1” = „egyes szám הִשְׁתַּחֲוֵ֫יתִי”; új: „1 meghajol, leborul uralkodó vagy felsőbbrendű előtt (abc)”, „2 Isten előtt, imádatban”, „3 más istenek előtt”. |
| H7931 | Qal [–]; Pi`el [–,1(abc),2(a–e)]; Hiph […] | Qal [–,1(abc),2(a–e)]; Pi`el [–,1,2]; Hiph […] | = új | **javult** | A régi a Qal jelentéseit („1 letelepedik, hogy ott lakjon: a–c”, „2 megmarad, lakik: a–e”) a Pi`el alá tette; új: Pi`el „1 letelepít, megalapít”, „2 lakoztat”. |
| H3498 | Hiph [–,1,2(abc),3] | Hiph [–,1(abc),2,3] | = új | **javult** | Régi „1” = „egyes szám suffixummal אוֺתִיר”; új: Hiph`il „1” (a–c alponttal; a magyar szöveg itt csak az alpontokat hozza), „2 kitűnik, kiválóságot mutat”, „3 felesleget mutat”. |
| H3885 | Qal [–,1,2(a–d)] | Qal [–,1(a–d),2] | = új | **javult** | Régi „1” = „többes szám וְלַנּוּ”; új: „1 megszáll, éjszakázik (a–d)”, „2 átvitt értelemben megmarad”. |
| H0560 | [1,2,3] | [–,1,2,3] | [1,2,3] (az alaklista a fej előtti szöveg) | **javult** | Régi 1., 2. = „egyes szám אַמְרֵת”, „hímnemű többes szám תֵּאמְרוּן”; helyes: „— 1 mond (gyakran a felel és mond kifejezésben) … 2 elbeszél, elmond … 3 parancsol”. |
| H1869 | Qal [–,1,2,3,4]; Hiph [–,1,2,3] | Qal [–,1,2]; Hiph […] | Qal [–,1,2,3,4]; Hiph […] | **mindkettő hibás**; végleges **javítva** | Régi: a Qal „1”, „2” személyszám („1. egyes szám דָּרַכְתִּי”). Új: a „3” előtt nincs írásjel („Szakmai értelemben 3 présben (bor- vagy olajprésben) tapos”). Végleges: „1 tapos, menetel”, „2 rálép (földre)”, „3 présben tapos”, „4 feszíti (azaz hajlítja) az íjat”; Hiph`il „1 tapos, letipor”, „2 feszíti az íjat (= Qal 4)”, „3 műveltető”. |
| H7121 | Qal [–,1,2(abcd),3(abcd),4(abc),5(abcdef),6(a–i)] | Qal […]; Niph`al [–,1,2(abcd)]; Pu`al [–] | = új | **javult** (az F60.25 célja) | Niph`al: „1 visszaható … a szent városról nevezik magukat”, „2 szenvedő: hívatni, neveztetni”; Pu`al: „(Ezékiel és Ézs^2) perfectum 3. hímnemű egyes szám קֹרָא”. A H7121 javítása megmaradt (teszt: `BdbSzeletelesAtnezes`). |

**Összesítés (a 19):** javult 11 (H0935, H3205, H3772, H3559, H5800, H3201, H7812, H7931, H3498, H3885, H0560), romlott 5 (H9003, H3588, H3027, H5973, H2896), mindkettő hibás 3 (H0834, H0157, H1869), egyenértékű 0. A H7121 (az F60.25 célszócikke, nem a 19 része) javult. A végleges bontás a 19-ből 18-ban helyes, a H0834-nél részben (ismert hiba).

## 3. A szabályváltozások (F60.35)

1. **A „— 1” külön ág megszűnt** (`_jelentesek`): az alaklista előtti szöveg az első valódi jelölőig a fej; nem-igéknél a későbbi „— 1” nem vihet a számozás elé.
2. **A személyszám-jelölő kizárva**: a pont után álló „N. [hímnemű|nőnemű|közös] egyes|többes szám <héber alak | suffixummal | consecutivummal | cohortativus | jussivus>” nem jelentés-sorszám (1615 pontos és 5 pont nélküli előfordulás a táblán; a pont nélküli „3 többes szám מִשְׁכָּנוֺת, lakóhelyek” H4908 jelentés, ezért marad jelölő).
3. **Sigla előtti szám nem jelölő** („1 Tsepreghi^Diss.”, H0834): a szám utáni szó tartalmaz `^`-t.
4. **Laza jelölő**: ha a várt sorszám a szigorú mintával nincs meg, kisbetűs, csupa betűs szó után és kisbetűs szó előtt álló szám is jelölő (a magyar fordítás elhagyta az írásjelet); az „1”-re csak igetörzsben (H0157 „participiumot 2”, H1869 „értelemben 3”, H4191 „adni 1 abszolút”).
5. **A „Név alakcsoport” törzsfejléc** csak igében, és csak gondolatjel, mondatvég, pontosvessző vagy zárójel-vég után; rövidítés után („olv. Qal, vö.”, „l. Niph`al”) nem; főnévben (H4908, H4735, H4720) az etimológiában álló „Pe`al imperfectum” nem fejléc.
6. A H7121 szerkezete mindegyik lépés után változatlan (teszt).

## 4. Újramérés az egész magyar BDB-táblán

Eljárás: `adat/forditasok.tsv`, BDB, nem üres `forditas_hu`; mindhárom szeletelő-változat (`18a927f6^`, `18a927f6`, mostani) minden soron; összevetés (a) a jelentés-jelek listájával (törzsenként, alpontokkal), ez a naplóbeli mérték; (b) a jelekkel és a jelentés szövegének első 30 karakterével. Egy szócikk egyszer számít.

| Összevetés | (a) jelek listája | (b) jelek + szövegkezdet |
|---|---|---|
| régi → új (F60.25) | 115 | 147 |
| új (F60.25) → végleges | 81 | 103 |
| régi → végleges | 107 (ebből azonos törzsnevekkel 32, a törzsnevek is változnak 75) | 147 |

A naplóbeli „19” az (a) mérték régi → új összevetése volt, az **azonos törzsnevű** sorokra (19 a 115-ből; a többi 96 szócikkben a törzsnevek is változtak, ezeket nem néztem át). A személyszám-jelölők száma a jelentés-sorszámok között: régi 177, új (F60.25) 56, **végleges 3** (H4908 és H2706: valódi jelentés; H1157: ismert hiba).

`scope=adat/forditasok.tsv BDB (678 magyar sor) | forras=bdb_szelet.py régi 18a927f6^, F60.25 18a927f6, végleges 31e51419 | ts=2026-10-12T18:09`

**A 19-en és a H7121-en kívüli változott szócikkek (régi → végleges, (b) mérték: 147 − 15 = 132)** és besorolásuk:

- **Javult — a régi bontásban az alakok személyszáma jelentés-sorszám volt (85):** H7843 H0559 H1961 H6213 H5414 H1980 H7200 H4480 H3427 H7725 H3947 H3045 H7971 H2009 H4191 H0398 H6965 H7760 H5674 H5975 H5221 H4672 H5307 H3381 H6485 H5493 H2388 H2421 H7126 H2142 H3423 H3789 H8354 H5186 H3254 H3615 H3467 H0622 H7311 H7650 H0006 H6942 H7592 H2026 H2930 H5437 H5608 H3680 H5060 H5265 H2583 H7291 H5117 H2076 H2803 H5012 H3034 H3847 H5162 H7323 H3722 H5922 H7911 H2891 H4422 H5462 H3925 H6419 H5641 H3384 H4376 H5782 H2470 H2199 H0270 H7495 H5341 H7167 H8552 H3335 H7919 H3001 H3198 H2308 H5193. *Módszer:* automatikus (a régi bontásban van jelentés-jelű elem, amelynek szövege személyszámmal kezdődik, a véglegesben nincs), szúrópróba olvasással (H1961, H7760, H3427, H0622: a jelentések a szövegnek megfelelnek). Nem minden szócikkről olvastam végig a szöveget.
- **Törzsek bővültek vagy átrendeződtek (37):** H7043 H8085 H1696 H3318 H8104 H5046 H4427 H1288 H3372 H5647 H4390 H5337 H1540 H3898 H8055 H7665 H8130 H2490 H7122 H6437 H6912 H7604 H6908 H7993 H5066 H6999 H7999 H3513 H7489 H7646 H7891 H7069 H5324 H2790 H7364 H6743 H6299. A régi csak az egyetlen, „_N” jelű (előfordulás-számmal jelölt) törzset találta; az új a „Név alakcsoport” fejléceket is. Szúrópróba: H7043 (Qal, Niph`al, Pi`el, Pu`al, Hiph`il, Pilpel, Hithpalpel: mind valódi törzs), H5337 (a fej „Qal nincs; Pi`el …; Niph`al …”, a Niph`al/Pi`el/Hiph`il sorrend a szövegé), H8085 (Aramaic Pe`al, Hithpe`el). **Javult**, kivéve az „ismert hibák” alatt felsoroltakat (H3318, H2490, H2790, H6743, H6299).
- **Egy-két jelentés-jelzéssel több (10):** H1121 H1323 H3967 H5002 H5127 H5387 H3920 H2822 H1892 H4116. A laza jelölő hozta a hiányzó sorszámokat („fiatal nők, asszonyok”, „isteni nevek előtt (kivéve Jer 23:31 …)”, „átvitt értelemben a mulandóról”); H3920: a Niph`al fej már nem a „3). Niph`al perfectum” szövegtöredékkel kezdődik. **Javult.**
- A 19-ből a H9003, H3588, H3027, H5973, H2896 és a H0834 sorszám-szerkezete a régi felé tért vissza (a fenti táblázat); H0834 ismert hibával.

## 5. Ismert hibák

| Strong | Hiba | Miért nem általánosan javítható |
|---|---|---|
| H0834 | az 1. jelentés a „… 1 tűnik előnyösebbnek” mondatnál indul (az etimológiai bekezdés része), a valódi 1. a „Közelebbről 1 magában foglalja” | a „— 1 …” és „. 1 …” alakú jelölők közül az elsőt veszi; a valódi jelölő kisbetűs szó után áll (laza), de a szigorú minta előbb talál |
| H3318 | a Qal fejléc a szövegben nincs (a Qal jelentései a „Hiph`il_278” törzs alá kerülnek), a Hoph`al külön áll | a törzs nevét a szöveg nem tartalmazza |
| H1157 | az „1 többes szám בַּעֲדֵנוּ” (pont nélküli személyszám egy elöljárószónál) jelentés-sorszámnak számít | ugyanaz az alak H4908-ban valódi jelentés (H4908: „3 többes szám מִשְׁכָּנוֺת, lakóhelyek”); a különbség csak az igei szövegkörnyezet |
| H2009 | az alpontok (a–d) nem látszanak, ha a szócikkben nincs számozott jelentés (a régi bontás ezt egy személyszám-„1”-gyel véletlenül megtalálta) | az alpont-keresés csak számozott jelentésen belül fut |
| H2490, H2790, H3384, H6299, H6743, H6965 | ismétlődő törzsnév (Qal / Hiph`il kétszer): valószínűleg a II. szócikk (homonima) törzsei, amelynek „II.” fejlécét a címszó-felismerő nem ismeri fel (vagy hivatkozás: H6299 „infinitivus absolutus l. Niph`al”) | a homonima-határ felismerése külön szabály (a `CIM` címszó-minta héber szót és szófajt vár) |

Szócikkenkénti kivételtáblát nem vezettem be.

## 6. Tesztek és újragenerálás

- `python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py`: 85 teszt, OK (1 kihagyva). Új osztály: `BdbSzeletelesAtnezes` (23 szócikk várt törzs- és jelentés-szerkezete: a 19, a H7121, a H4908, H4191 és H0622; a személyszám-, laza-jelölő- és alakcsoport-fejléc szabályok egységtesztjei). A H7121-re az F60.25 nem hagyott tesztet; ez most van meg.
- `python eszkozok/feladatok.py ellenoriz`: 110 brief, 0 hiba, 0 figyelmeztetés.
- Újragenerált HTML (`adat.py` + `epit.py`, gzip+base64): 1Móz 1–25 `…\scratchpad\f60_egyesitett\1moz\karoli_konkordancia_proba.html` 10 209 602 bájt; Zsolt 22 `…\zsolt22\karoli_konkordancia_proba.html` 2 544 178 bájt. U+FFFD a HTML szövegében 0; a kibontott JSON-ban 1 a 1Móz-ban (a `tW_szocikkek.tsv` ismert forrásadat-hibája, `OLVASOI_PILOT_ertekeles.md` 6.), 0 a Zsolt 22-ben.
- A `OLVASOI_PILOT_meres.md` és az `OLVASOI_PILOT_ertekeles.md` 2. pontja a mért HTML-méretet az F60.31 állapotról közli (10 204 234 és 2 538 866 bájt); a mérést nem futtattam újra, a különbség a két fájlban 5 és 5 ezer bájt körüli (BDB-szerkezet).
