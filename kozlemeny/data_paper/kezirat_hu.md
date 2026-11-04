<!-- Forrásréteg, kézi szöveg (F167.2, helyőrző tételszám). A data paper magyar kézirata a Digitális Bölcsészet (ELTE) „Labor” rovatára igazítva; nem az angol kézirat fordítása, hanem eltérő hangsúlyú adatközlés (a módszerre és a magyar olvasói rétegre). Szöveg: claude-opus-5-5, 2026-11-04. Minden szám a `kozlemeny/data_paper/szamok.py` kimenetéből (l. „A számok forrása”); a beküldött változatból a „BEKÜLDÉSI SZÖVEG VÉGE” jelölő utáni rész kivehető. A <…> helyőrzőket a szerző tölti ki; amíg helyőrző áll benne, a szöveg nem nyilvános. A rovat követelményeinek forrása: `folyoirat_lehetosegek.md` (PR #632), 2. szakasz és a rangsor 4. pontja; ami ott nem ellenőrzött, itt is ❓-lel jelölve. -->

# Kizárási döntések bibliai motívumkutatásban: motívum-indexelt nyílt adatkészlet a héber és görög szövegről, a Károli-fordítás szavaival

**Szerző:** `<SZERZO>` (`<INTEZMENY>`; ORCID `<ORCID>`) — *kettős vak bírálatra a beküldött példányból törlendő, l. a végi jegyzetet*

## Rövid leírás

Kilenc bibliai motívum nyílt adatkészletét mutatjuk be. Minden motívumot a héber vagy a görög szöveg egy ellenőrizhető jegye határoz meg: egy szó, egy állandó szókapcsolat vagy több szó visszatérő együttállása. Az adatkészlet 255 előfordulást és 3 509 versszintű kizárási döntést tartalmaz. Minden előfordulás megnevezi azt az eredeti nyelvű szót vagy szópárt, amelyen áll; minden megvizsgált, de elutasított hely okkal együtt megmarad. Az előfordulások mellett ott áll a Károli-fordítás megfelelő szava is, a párosítás módjával és bizonyosságával. A közlemény a módszer kizárási eszközeit és a magyar olvasói réteg szerepét írja le.

## Abstract (angol)

We present an open dataset of nine biblical motifs, each defined by a verifiable feature of the Hebrew or Greek text, with 255 occurrences and 3,509 verse-level exclusion decisions, every rejected candidate kept with its reason. Each occurrence also records the corresponding word of the Hungarian Károli translation, with the method and confidence of the alignment. This paper focuses on the exclusion devices of the method (negative criterion, broader concept, three-net completeness test) and on the Hungarian reader layer. A companion English data paper describes the dataset itself (`<ANGOL_KOZLEMENY_HIVATKOZAS>`).

**Kulcsszavak:** bibliai motívumok; intertextualitás; Károli-fordítás; Septuaginta; negatív lelet; nyílt adat

## 1. Az adatkészlet és a kérdés

Az adatkészlet egy hosszú távú, magyar nyelvű motívumlexikon nyílt adatrétege. A motívum itt olyan visszatérő bibliai téma, amelynek azonosságát az eredeti nyelvű szöveg ellenőrizhető jegye hordozza: egy szó (hat motívum, például a Seol/Hádész), egy állandó szókapcsolat (kettő, például „segítségül hívni az Úr nevét”, héberül *qārāʾ bĕšēm YHWH*) vagy több szó visszatérő mintázata (egy).

A motívumkutatás jellemző hibája nem az, hogy egy helyet nem vesz észre, hanem az, hogy túl sokat vesz fel: a hasonlóságot felnagyítja, és a motívum határa a tágabb téma felé szétfolyik. Samuel Sandmel ezt „parallelomániának” nevezte (Sandmel, 1962). Ez a közlemény arra a kérdésre felel, hogyan lehet a kizárást ugyanolyan dokumentált adattá tenni, mint a felvételt. Az elutasított helyek ezért itt nem munkaközi szemét, hanem az adatkészlet része: a motívum határát a kizárások rajzolják meg, nem a meghatározás.

Az értelmező szócikkek, a szótárak magyar fordítása és a kötet külön termékréteget alkotnak; ez a közlemény nem foglalkozik velük.

## 2. Módszer: a felvétel és a kizárás eszközei

**A hét lépés.** Minden motívum hét lépésben készül: (1) a törzshelyek közös Strong-számai, a nyelvtani szavak kiszűrésével; (2) a szemantikai mező feltevése, az egyetlen generatív lépés, naplózva; (3) a teljes ó- és újszövetségi szöveg átvizsgálása a STEPBible címkézett szövegén (TAHOT, TAGNT); (4) szópár egy versen belül; (5) az igealak ellenőrzése; (6) a Septuaginta-megfelelés; (7) a nevesített magyarázók egyezése (ez a termékréteg része). Az 1. és a 3–6. lépés determinisztikus program.

**Nincs közvetlen út.** Keresési találat nem kerülhet közvetlenül az adatkészletbe. Minden jelölt egy jelölttáblán megy át, ahol döntés és indoklás születik róla; az üres eredményt üresként rögzítjük, és nem töltjük ki asszociatív anyaggal.

**Négy kérdés az azonosító előtt.** Mielőtt egy motívum azonosítót kap, négy kérdésre kell felelni: mi hordozza az azonosságát; mi az a legkisebb jegy, amely nélkül egy hely nem tartozik ide (a negatív kritérium); ha egy hely két motívumhoz is tartozik, különbözik-e a funkciója; és nem részhalmaza-e egy másik motívumnak.

**A fölérendelt fogalom.** Minden motívum megnevezi azt a tágabb fogalmat, amely felé hígulna. A bűn következményeinek továbbgyűrűzése motívumnál ez maga a „bűn”: ha egy hely csak a bűn általános leírásán át kapcsolódik, kimarad. Mind a kilenc motívumnál ki van töltve a negatív kritérium és a fölérendelt fogalom. A motívumok a kutatási programot követik, nem reprezentatív mintái a Bibliának.

**A kizárási okok.** A kizárás 418 sorban áll: 394 egyedi vers és 24 összesítő sor, amely 3 115, azonos okból elutasított verset képvisel; összesen 3 509 döntés, 54 okkategóriában. Versszám szerint a leggyakoribb okok: a két szóból csak az egyik áll a versben (1 713), más lexéma (651), és az, hogy a Károli ugyanazzal a szóval más héber vagy görög szót fordít (295). Soronként a leggyakoribb: „a formula nincs a versben” (58), „a tohu és bohu szópár nincs a versben” (40), „átok-kimondás, a következmény továbbterjedése nélkül” (29). Az utóbbi két példa jól mutatja a negatív kritérium munkáját: a szó önmagában nem elég, a motívum szerkezete hiányzik.

**Teljesség-mérés három hálóval.** Négy motívum előfordulás-listáját három, egymástól független hálóval vetettük össze a teljes kánonon: a Strong-számokkal (TAHOT, TAGNT), a Károli-szóval és a Brown–Driver–Briggs-, illetve a Thayer-szótárban a motívum szavainál idézett versekkel. A Seol/Hádész és a „segítségül hívás” motívumnál egyik háló sem hozott olyan verset, amelyben a motívum jegye áll, és az adatból hiányzik. A pneuma/pszükhé megkülönböztetésnél a görög szópár minden verse benne van az adatban, előfordulásként vagy eldöntött jelöltként. A bűn továbbgyűrűzésénél a Strong-háló 1 233 verset hozott az adaton kívül: 651-et blokkban elutasítottunk (a negatív kritérium listáján kívüli szó), 582 kézi átnézésre vár, és 12 előfordulás-verset egyik háló sem talál meg (tematikus kapcsolat, vagy a szó a verstartomány másik versében áll). Ez a motívum tehát nem bizonyítottan teljes, és a hálók általában is csak a lexikai jegyekhez mért visszahívást mérik, nem a teljességet.

## 3. A magyar olvasói réteg: a Károli-szó

Az előfordulás bizonyítéka mindig a héber vagy a görög szöveg. Az előfordulásoknál azonban ott áll a Károli-fordítás megfelelő szava is (255 sorból 203-ban), a párosítás módjával: a szerkesztő a Károli-szöveget olvasva rendelte a szót a Strong-számhoz (176 sor), gépi szópárosítás (25), következtetés (2); a bizonyosság magas (192) vagy közepes (11). A Károli-szó tehát megjelenítési adat: az az ablak, amelyen át a magyar olvasó a helyet látja. Nemzetközi exegetikai érvelésben nem érv; a magyar fordítástörténetnek viszont önálló adat.

Három példa mutatja, mit lát és mit nem lát a magyar olvasó:

- **A seól szava.** A Károli a seólt és a hádészt nem egy szóval adja vissza: a 74 előfordulás-sorban „sír” (29), „Seol” (19), „pokol” (17), „koporsó” (5), „mélység” (2) és „alvilág” (2) alak áll (egy sorban több is lehet). A magyar olvasó ezért a motívumot nem ismeri fel a szóról; a Károli-háló 298 olyan verset is hozott, amelyben ezek a magyar szavak más héber vagy görög szót fordítanak (köztük a sírás igéjét).
- **Lélek és szellem.** A Károli a πνεῦμα (pneuma) és a ψυχή (pszükhé) szót nem választja szét: a Lukács 1:46–47-ben mindkettő „az én lelkem”, az 1Thessz 5:23-ban a pneuma „valótok”, a Zsid 4:12-ben a pszükhé „szívnek” áll, „szellem” csak az 1Kor 15:45-ben („megelevenítő szellemmé”). A megkülönböztetés, amely a motívum lényege, a magyar szövegben nem látszik, csak az eredetiben.
- **A formula.** A „segítségül hívni az Úr nevét” a Károliban állandó fordulat („segítségűl hívá az Úrnak nevét”), ezért a Károli-háló itt szűkebb, mint a Strong-háló (96 és 204 vers). A „hív” és a „kiált” szó viszont a Károlinál elnevezést és meghívást is fordít, ezért a háló csak a „név” társaságában számol velük.

A kizárási döntések egy része éppen a Károli-szóból fakad: a seól-motívumnál 295, a „segítségül hívás” motívumnál 51 vers azért esik ki, mert a magyar szó mögött más héber vagy görög szó áll.

## 4. Az adatkészlet

| | |
|---|---|
| Név és kiadás | PaRDeS nyílt mag, kiadás 2026-11-04-c737a4cc40428d86 |
| Hely | `<DOI>` (kanonikus közzétételi hely: `<KANONIKUS_FORRAS_URL>`) |
| Formátum | UTF-8 TSV (tabulátorral tagolt, idézőjelezés nélkül), Markdown, SHA-256 ellenőrzőösszeg; 17 fájl, 436 294 bájt |
| Táblák | motívumok (9), előfordulások (255), felvételi döntések (257), kizárások (418) és a csoportok tagjai (1 402), igehely-kapcsolatok (32), motívumok közötti kapcsolatok (3), döntésnapló (8), források és licencek (54), kódkönyv (210 bejegyzés, magyarul és angolul) |
| Létrehozás | 2026-08-22 – 2026-11-04 |
| Nyelv | magyar oszlopnevek és értékek, héber és görög szavakkal; a kódkönyv kétnyelvű |
| Licenc | CC BY 4.0; a szemantikai domének külön rétege (UBS SDBH/SDGNT, 237 sor) CC BY-SA 4.0 |
| Készítő | `<SZERZO>` |

A 11 összesítő sor (1 713 vers) tagjainak listája még nincs a csomagban.

A sorok a TAHOT és a TAGNT (CC BY 4.0; STEPBible, é. n.), az OpenBible.info Treasury of Scripture Knowledge alapú kereszthivatkozásai (CC BY; OpenBible.info, é. n.) és az 1908-as Károli-szöveg (a mű kora miatt közkincs) adataira épülnek. 25 forrás kimaradt: kilenc a projekt zárt, származtatott rétege, kilencnek tisztázatlan a licence, háromnál korlátozott a kereskedelmi használat, négy CC BY-SA forrást a csomag nem használ.

A PaRDeS-szint (Peshat, Remez, Drash, Sod) recepciós címke: azt osztályozza, hogyan kapcsolódik egy hely a motívumhoz a középkori zsidó négyes olvasási séma nyelvén, nem azt, mit szándékolt a bibliai szerző. Az adatkészlet a bibliai korpuszon belül marad; ókori közel-keleti összevető réteg nincs benne, és egy párhuzam hiánya nem lelet.

## 5. Minőségellenőrzés és korlátok

**Az ellenőrzési lánc.** (a) A csomag kapuja a belső jelölést, a kódkönyv lefedését, a licencszűrést, a hivatkozások feloldását és a bájtazonos újragenerálást ellenőrzi (ebben a kiadásban 0 bukás, 9 figyelmeztetés); az olvasói kapu minden kiadott lexikonlapon nulla olvasói hibát követel. (b) Friss kontextusú MI-ellenőr minden változást saját lekérdezéssel újraellenőriz; egy második modell a motívum határát vizsgálja. (c) Három motívum ment át a hivatalos kiadási eljáráson; ezekről nyolc rögzített vizuális átnézés és 29, a szerző által jóváhagyott javítás van.

**Korlátok.** A szerzőn kívül minden ellenőr program vagy nyelvi modell; független szakmai lektorálás és annotátorok közötti egyezésmérés nem volt. A 255 előfordulás-sorból 251 szerkesztői döntésként van rögzítve, nem egyetlen lekérdezés kimeneteként; a Strong-hozzárendelésből 183-at igazoltunk a TAHOT héber szövegén, 36 kívül esik a hatókörén, 36 nincs igazolva. A Károli-kiadás kereszthivatkozás-táblájában más versek listájának másolatai állnak (5 078 gyanús forrásvers); az adatkészlet ebből adatot nem tartalmaz, de 28 kizárás-sort ezen át találtunk. A minta kicsi (kilenc motívum, ebből három kiadott).

## 6. Újrahasznosítás

Az előfordulás- és kapcsolattáblák közös héber és görög szavak mentén összekötött igehely-hálózatot adnak, kifejezett negatív lelettel; ez a Hays-féle kritériumokra épülő intertextualitás-vizsgálatok (Hays, 1989) mellé dokumentált döntési nyomot ad. Az indokolt felvételek és kizárások visszakeresési vagy osztályozási próbakészletként használhatók: például az, hogy egy rendszer szétválasztja-e az Úr nevének segítségül hívását az elnevezéstől. A Károli-szó a párosítás módjával és bizonyosságával a magyar fordítástörténet és a magyar nyelvű bibliai korpuszok adata. A negatív kritérium, a fölérendelt fogalom és a háromhálós teljesség-mérés más korpuszra is átvihető.

## Nyilatkozat a mesterséges intelligencia használatáról

A lekérdezések determinisztikus programok. A felvételi és kizárási döntések az Anthropic Claude nyelvi modelljeivel segített munkamenetekben születtek (a modellnevek munkamenetenként a projekt naplóiban), mindegyik indoklással; az adatkészlet döntéseket és rövid indoklásokat tartalmaz, modell írta értelmező prózát nem. A Károli-szó párosításának egy része gépi, és így van jelölve. A fent leírt MI-ellenőrzések modellfutások. A kézirat szövegét claude-opus-5-5 fogalmazta a repó adataiból. MI-eszköz nem szerző; az adatokért és a szövegért `<SZERZO>` felel. `<SZERZOI_NYILATKOZAT>`

## Összeférhetetlenség

A szerző az adatokra épülő fizetős terméket (értelmező szócikkeket és kötetet) is kiad. `<OSSZEFERHETETLENSEG_MEGFOGALMAZAS>`

## Támogatás

`<TAMOGATO>`

## Hivatkozások

Hays, R. B. (1989). *Echoes of Scripture in the letters of Paul*. Yale University Press.

OpenBible.info. (é. n.). *Cross references* [adatkészlet]. https://www.openbible.info/labs/cross-references/

Sandmel, S. (1962). Parallelomania. *Journal of Biblical Literature, 81*(1), 1–13. https://doi.org/10.2307/3264821

STEPBible. (é. n.). *STEPBible data: Translators Amalgamated Hebrew OT (TAHOT) and Greek NT (TAGNT)* [adatkészlet]. Tyndale House, Cambridge. https://github.com/STEPBible/STEPBible-Data

United Bible Societies. (2023). *UBS Dictionary of Biblical Hebrew* (v0.9.2) és *UBS Dictionary of New Testament Greek* (v1.1) [adatkészlet]. https://github.com/ubsicap/ubs-open-license

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi részek a beküldött változatból kivehetők. -->

---

## A számok forrása

Minden szám a `python kozlemeny/data_paper/szamok.py` egy futásából jön, a zárt `nyilt_mag/` csomagon, ugyanazokkal a kulcsokkal, mint az angol kézirat „Number provenance” melléklete (`kezirat_en.md`); ahol a forrás más, az alább áll.

| Szám a szövegben | Kulcs | Forrás |
|---|---|---|
| 9 motívum; 6 lexikai, 2 formulaikus, 1 strukturális; mindkét mező kitöltve | P1.motivum, P1.azonossag, P1.ures_negativ_kriterium, P1.ures_folerendelt | `nyilt_mag/motivumok.tsv` |
| 255 előfordulás; 251 kézi döntés; 183 / 36 / 36 | P2.elofordulas_sor, P2.kezi_dontes, P2.igazolas | `nyilt_mag/elofordulasok.tsv` |
| 203 kitöltött Károli-szó; 176 / 25 / 2; 192 / 11 | P2.karoli_szo_kitoltve, P2.azonositas_modja, P2.megbizhatosag | `nyilt_mag/elofordulasok.tsv`, `karoli_szo`, `azonositas_modja`, `megbizhatosag` |
| 74 seól-sor; sír 29, Seol 19, pokol 17, koporsó 5, mélység 2, alvilág 2 | P2.motivumonkent, P9.alvil_karoli | `nyilt_mag/elofordulasok.tsv`, ALVIL-001, `karoli_szo` (kisbetűs részszöveg-egyezés; egy sor több alakot is tartalmazhat) |
| a „lélek/szellem” Károli-alakjai | — | `nyilt_mag/elofordulasok.tsv`, ANTROP-001, `karoli_szo` (Luk 1:46, 1:47, 1Thessz 5:23, Zsid 4:12, 1Kor 15:45) |
| „segítségűl hívá az Úrnak nevét” | — | `nyilt_mag/elofordulasok.tsv`, ISTENTISZT-001, `karoli_szo` |
| 298 „sír”-vers a Károli-hálóban | P8.ALVIL-001 | `naplok/F123_teljesseg_ALVIL-001.md`, 1. és 2. szakasz |
| 96 és 204 vers (formula) | P8.ISTENTISZT-001 | `naplok/F123_teljesseg_ISTENTISZT-001.md`, 1. Összegzés |
| 418 / 394 / 24 / 3 115 / 3 509; 54 okkategória; 1 713 / 651 / 295; 58 / 40 / 29 | P3.* | `nyilt_mag/kizarasok.tsv` |
| 295 (seól) és 51 („segítségül hívás”) vers: a Károli-szó más szót fordít | P3.ok | `nyilt_mag/kizarasok.tsv`, „más szó a Károli-fordításban” (ALVIL-001, 5 sor), „a Károli-szó más szót fordít” (ISTENTISZT-001, 1 sor) |
| 28 kizárás-sor a Károli-kereszthivatkozásból | P3.keresesi_mod | `nyilt_mag/kizarasok.tsv`, `keresesi_mod` |
| 11 összesítő sor tag nélkül (1 713 vers); 1 402 tag | P3.osszesito_tag_nelkul, P3.csoport_tabla_sor | `nyilt_mag/kizarasok.tsv`, `nyilt_mag/kizaras_csoportok.tsv` |
| 257 / 32 / 3 / 8 / 210 / 237 sor | P4.* | a csomag azonos nevű fájljai |
| 54 forrás; 25 kizárt (9 / 9 / 3 / 4) | P5.forras_sor, P5.kizart_ok | `nyilt_mag/forrasok_es_licencek.tsv` |
| 17 fájl, 436 294 bájt; dátumtartomány; kiadás-azonosító | P6.fajl, P6.meret_bajt, P6.datum_tartomany, P0.kiadas | `nyilt_mag/` |
| 0 bukás, 9 figyelmeztetés | — | `python eszkozok/nyilt_mag_kapu.py`, 2026-11-04 |
| 3 kiadott motívum, 8 átnézés, 29 javítás | P7.* | `adat/kiadasok.tsv`, `adat/lap_atnezesek.tsv`, `adat/lap_javitasok.tsv` |
| teljesség-mérés (1 233 / 651 / 582 / 12 stb.) | P8.* | `naplok/F123_teljesseg_<ID>.md`, 1. Összegzés (az 582 a HAMART-001 napló „Eredmény” 1. pontjából) |
| 5 078 gyanús forrásvers | — | `nyilt_mag/ISMERT_HIBAK.md`, 1. szakasz |

## Jegyzet: kettős közlés

Ugyanaz a mű nem lehet egyszerre két folyóiratnál elbírálás alatt; a JDMDH és az RDJ beküldési feltétele ezt ki is mondja, és a Digitális Bölcsészet is korábban nem közölt művet vár (❓, a „Labor” rovatra nem ellenőrzött). A magyar és az angol kézirat ezért **két külön mű** csak akkor, ha a hangsúlyuk valóban eltér, és egymásra kölcsönösen hivatkoznak:

- **az angol** (`kezirat_en.md`) az adatkészletet írja le (data paper: szerkezet, formátum, újrahasznosítás);
- **a magyar** (ez a kézirat) a módszer kizárási eszközeire és a magyar olvasói rétegre (a Károli-szó) helyezi a hangsúlyt; az adatkészlet leírása itt csak egy táblázat.

A számok és a mondatok egy része szükségszerűen közös (ugyanaz az adat). Ha a szerkesztőség ezt átfedésnek tekinti, a másodközlés csak a két folyóirat tudtával, a második közlésben az elsőre való hivatkozással lehetséges.

**Javasolt sorrend** (a döntés a felhasználóé): (1) a nyílt mag letétele (DOI); (2) az angol data paper beküldése a fő csatornára; (3) a magyar kézirat beküldése **az angol elfogadása után**, a kísérőlevélben a két közlés viszonyának kimondásával, és a magyar szövegben az angolra hivatkozva (`<ANGOL_KOZLEMENY_HIVATKOZAS>`). Párhuzamos beküldés csak akkor, ha mindkét szerkesztőség előzetesen hozzájárul.

## Jegyzet: a „Labor” rovat (Digitális Bölcsészet)

Forrás: `folyoirat_lehetosegek.md` (PR #632), ✅ = a folyóirat oldaláról lekérve, ❓ = nem ellenőrzött.

- A rovat kódot, adatkészletet és vizualizációt közöl, **rövid magyar és angol leírással és dokumentációval** ✅. A kézirat ezért magyar rövid leírással, angol absztrakttal és dokumentáló szakaszokkal készült. A rovat szerkezeti és terjedelmi előírását nem találtuk ❓; a „Műhely” rovat határa 5 000 szó ✅, ez a kézirat ennél jóval rövidebb.
- **Kettős vak bírálat** ✅: a beküldött példányból a szerző neve, az ORCID és az intézmény törlendő. Mivel az adatkészlet nyilvános, a szerzőt nevesítő DOI-val létezik, az anonimizálás csak részleges lehet: a `<DOI>` helyén a bírálati példányban `<ANONIMIZALT_DOI>` álljon, és az angol közleményre való hivatkozás is anonimizálandó. A rovat anonimizálási szabályát nem találtuk ❓: a szerkesztőségtől meg kell kérdezni.
- **A cikk licence CC BY-NC-SA 4.0** (a lap láblécében 2.5 HU: ellentmondás) 🔶. Ez a cikkre vonatkozik, nem az adatkészletre (CC BY 4.0); a kettő nem ütközik, de a kísérőlevélben érdemes kimondani.
- Díj nincs ✅; MI-szabály nincs kimondva ✅ — a nyilatkozat ennek ellenére benne marad.
- Hivatkozási stílus: a kézirat APA-t használ, a lap előírását nem ellenőriztük ❓.

## Kitöltendő helyőrzők (a szerző)

| Helyőrző | Mi kell |
|---|---|
| `<SZERZO>`, `<INTEZMENY>`, `<ORCID>` | szerzői adatok (a bírálati példányból törlendők) |
| `<DOI>`, `<KANONIKUS_FORRAS_URL>` | a letét DOI-ja és a kanonikus közzétételi hely (nem GitHub) |
| `<ANONIMIZALT_DOI>` | a bírálati példányban a DOI helyén |
| `<ANGOL_KOZLEMENY_HIVATKOZAS>` | az angol data paper hivatkozása (ha már megjelent vagy elbírálás alatt áll) |
| `<SZERZOI_NYILATKOZAT>` | a szerző felelősségvállaló mondata, vagy törlendő |
| `<OSSZEFERHETETLENSEG_MEGFOGALMAZAS>` | a fizetős termék és a nyílt adat viszonyának végleges megfogalmazása |
| `<TAMOGATO>` | finanszírozó, vagy „A kutatás külső támogatás nélkül készült.” |

## Nyitott kérdések

1. A kettős közlés sorrendje és a két folyóirat tájékoztatása (fent).
2. A „Labor” rovat szerkezete, terjedelme, anonimizálási szabálya és hivatkozási stílusa: a szerkesztőségtől kérdezendő.
3. A 11 tag nélküli összesítő sor: a #635 merge-e után a mondat törlendő, a szám frissítendő.
4. A HAMART-001 582 nyitott verse, a Károli 1908 licence, a hivatkozások ellenőrzése: mint az angol kéziratnál.
