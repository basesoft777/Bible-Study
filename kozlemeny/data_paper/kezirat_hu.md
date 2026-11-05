<!-- Forrásréteg, kézi szöveg (F167.2, helyőrző tételszám; átírás: F167.3). A data paper magyar kézirata a Digitális Bölcsészet (ELTE) „Labor” rovatára igazítva; nem az angol kézirat fordítása, hanem eltérő hangsúlyú adatközlés (a módszerre és a magyar olvasói rétegre). Szöveg: claude-opus-5-5, 2026-11-04. Minden szám a `kozlemeny/data_paper/szamok.py` kimenetéből (l. „A számok forrása”); a beküldött változatból a „BEKÜLDÉSI SZÖVEG VÉGE” jelölő utáni rész kivehető. A <…> helyőrzőket a szerző tölti ki; amíg helyőrző áll benne, a szöveg nem nyilvános. A rovat követelményeinek forrása: `folyoirat_lehetosegek.md` (PR #632), 2. szakasz és a rangsor 4. pontja; ami ott nem ellenőrzött, itt is ❓-lel jelölve. -->

# Kizárási döntések bibliai motívumkutatásban: motívum-indexelt nyílt adatkészlet a héber és görög szövegről, a Károli-fordítás szavaival

**Szerző:** `<SZERZO>` (`<INTEZMENY>`; ORCID `<ORCID>`) — *kettős vak bírálatra a beküldött példányból törlendő, l. a végi jegyzetet*

## Kivonat

Ez a közlemény egy nyílt adatkészletet mutat be, amely kilenc bibliai motívum előfordulásait gyűjti a héber és a görög szövegben. Minden motívumot egy ellenőrizhető szöveges jegy határoz meg: egy szó, egy állandó szókapcsolat vagy szavak visszatérő együttállása. Az adatkészlet 255 előfordulást rögzít. Mindegyiknél megnevezi az eredeti nyelvű szót vagy szópárt, és mellé teszi a Károli-fordítás megfelelő szavát, a párosítás módjával és bizonyosságával. Legalább ilyen fontos az, ami kimaradt: 3 509 verset megvizsgáltunk és elutasítottunk, mindegyiket a döntés okával együtt. A kilenc motívumból három teljesen ellenőrzött, lezárt kiadás. A másik hat adatai a projekt korábbi szakaszában, régebbi eljárással készültek; teljes ellenőrzésük még hátravan, és a későbbi változatokban frissülnek. A közlemény bemutatja, hogyan rajzolják meg a kizárások a motívumok határát, és mit ad hozzá a magyar fordítás rétege.

## Abstract (angol)

We present an open dataset of nine biblical motifs, each defined by a verifiable feature of the Hebrew or Greek text. It records 255 occurrences and 3,509 verse-level exclusion decisions, each rejected candidate with its reason. Every occurrence also gives the corresponding word of the Hungarian Károli translation, with the method and confidence of the alignment. Three of the nine motifs are fully checked, closed releases; six come from an earlier stage of the work and will be updated in later versions. This paper focuses on how the method excludes (negative criterion, broader concept, three-net completeness test) and on the Hungarian reader layer. A companion English data paper describes the dataset itself (`<ANGOL_KOZLEMENY_HIVATKOZAS>`).

**Kulcsszavak:** bibliai motívumok; intertextualitás; Károli-fordítás; Septuaginta; negatív lelet; nyílt adat

## 1. A kérdés

A motívumkutatás jellemző hibája nem az, hogy átsiklik egy hely fölött, hanem az, hogy túl sokat vesz fel. A hasonlóság felnagyítódik, és a motívum határa szétfolyik a tágabb téma felé. Samuel Sandmel ezt „parallelomániának” nevezte (Sandmel, 1962). Ez a közlemény azt mutatja be, hogyan lehet a kizárást ugyanolyan dokumentált adattá tenni, mint a felvételt.

Az adatkészlet egy hosszú távú, magyar nyelvű motívumlexikon nyílt adatrétege. Egy motívumot itt mindig az eredeti szöveg valamely ellenőrizhető eleme azonosít. Hat motívumnál ez egyetlen szó, például a seól és a hádész. Kettőnél állandó szókapcsolat, például „segítségül hívni az Úr nevét” (héberül *qārāʾ bĕšēm YHWH*). Egynél több szó visszatérő együttállása. Motívumnak tehát olyan visszatérő bibliai témát nevezünk, amelynek jelenléte egy versben a héber vagy a görög szövegen ellenőrizhető.

Az elutasított helyek ezért nem a munka hulladékai, hanem az adatkészlet részei. A motívum határát nem a meghatározás rajzolja meg, hanem a kizárások. A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva. Ez a közlemény csak az adatmaggal foglalkozik.

## 2. A felvétel és a kizárás eszközei

**Hét lépés.** Minden motívum ugyanabban a sorrendben készül:

1. a motívum legfontosabb helyein (törzshelyein) közösen előforduló szavak Strong-számai, vagyis a héber és görög szótári szavak szabványos sorszámai, a névelők, kötőszók és más nyelvtani szavak nélkül;
2. a szemantikai mező feltevése (ez az egyetlen generatív lépés, ezért naplózzuk);
3. a teljes ó- és újszövetségi szöveg átvizsgálása a STEPBible címkézett szövegén (TAHOT, TAGNT);
4. szópárok keresése egy versen belül;
5. az igealak ellenőrzése;
6. a Septuaginta-megfelelés;
7. a nevesített magyarázókkal való egyezés (ez már a lexikon értelmező szövegéhez tartozik, nem az adatmaghoz).

Az 1. és a 3–6. lépést program végzi, tehát mindig lefut, és ugyanarra a bemenetre ugyanazt adja.

**Nincs közvetlen út.** Keresési találat nem kerülhet egyenesen az adatkészletbe. Minden jelölt egy jelölttáblán megy át, ahol döntés és indoklás születik róla. Ha a keresés üres, az eredményt üresként rögzítjük, és nem töltjük ki asszociatív anyaggal.

**Négy kérdés.** Mielőtt egy motívum azonosítót kap, négy kérdésre kell felelni. Mi hordozza az azonosságát? Mi az a legkisebb jegy, amely nélkül egy hely nem tartozik ide? (Ez a negatív kritérium.) Ha egy hely két motívumhoz is tartozik, más-e a szerepe a kettőben? És nem részhalmaza-e egy másik motívumnak?

**A fölérendelt fogalom.** Minden motívum megnevezi azt a tágabb fogalmat, amely felé hígulna. A bűn következményeinek továbbgyűrűzéséről szóló motívumnál ez maga a „bűn”. Ha egy hely csak a bűn általános leírásán át kapcsolódik, kimarad. A negatív kritérium és a fölérendelt fogalom mind a kilenc motívumnál ki van töltve. A motívumokat a kutatási program választotta ki; nem reprezentatív mintái a Bibliának.

**A kizárási okok.** A kizárások 418 sorban állnak. 394 sor egy-egy verset ír le; 24 összesítő sor 3 115 olyan verset képvisel, amelyet ugyanabból az okból utasítottunk el. Ez összesen 3 509 döntés, 54 okkategóriában. Mivel egy összesítő sor sok verset képvisel, más rangsort ad, ha a verseket számoljuk, és mást, ha a sorokat. Versszám szerint három ok a leggyakoribb: a szópárból csak az egyik szó áll a versben (1 713 vers); a versben más lexéma áll (651); a Károli ugyanazzal a magyar szóval más héber vagy görög szót fordít (295). Az egyenként eldöntött sorok között „a formula nincs a versben” (58), „a tohu és bohu szópár nincs a versben” (40) és „átok-kimondás, a következmény továbbterjedése nélkül” (29) a leggyakoribb. Az utóbbi két példán jól látszik, hogyan dolgozik a negatív kritérium: a szó önmagában nem elég, ha a motívum szerkezete hiányzik.

**Teljesség-mérés három hálóval.** Négy motívum előfordulás-listáját három „hálóval” vetettük össze a teljes kánonon: három, egymástól független kereséssel, amelyeknek az a dolguk, hogy kifogják a lista hiányait. Az első a Strong-számok (TAHOT, TAGNT), a második a Károli-szó, a harmadik a Brown–Driver–Briggs- és a Thayer-szótár által a motívum szavainál idézett versek. A seól/hádész és a „segítségül hívás” motívumnál egyik háló sem hozott olyan verset, amelyben a motívum jegye áll, és az adatból mégis hiányzik. A pneuma/pszükhé megkülönböztetésnél a görög szópár minden verse benne van az adatban, előfordulásként vagy eldöntött jelöltként. A bűn továbbgyűrűzésénél más a helyzet. A Strong-háló 1 233 verset hozott az adaton kívül: ebből 651-et egy tömbben elutasítottunk (a szó kívül esik a negatív kritériumon), 582 kézi átnézésre vár. Ráadásul 12 előfordulás-verset egyik háló sem talál meg, mert tematikus a kapcsolat, vagy a szó a verstartomány egy másik versében áll. Ez a motívum tehát nem bizonyítottan teljes. A hálók általában is csak azt mérik, mennyit fog meg a lista a lexikai jegyek alapján; a teljességet nem bizonyítják.

## 3. A magyar olvasói réteg: a Károli-szó

Az előfordulás bizonyítéka mindig a héber vagy a görög szöveg. Mellette azonban a 255 előfordulásból 203-nál ott áll a Károli-fordítás megfelelő szava is. A párosítást 176 esetben a szerkesztő végezte a Károli-szöveg olvasásával, 25 esetben gépi szópárosítás, 2 esetben következtetés. A bizonyosság 192 esetben magas, 11 esetben közepes.

A Károli-szó nem bizonyíték: azt mutatja meg, mit lát a helyből a magyar olvasó. Nemzetközi exegetikai érvelésben ezért nincs szerepe, a magyar fordítástörténetnek viszont önálló adata. Három példa mutatja, mit lát és mit nem lát a magyar olvasó.

**A seól szava.** A Károli a seólt és a hádészt nem egy szóval fordítja. A 74 előfordulásban „sír” (29), „Seol” (19), „pokol” (17), „koporsó” (5), „mélység” (2) és „alvilág” (2) áll; egy helyen több alak is lehet. A magyar olvasó ezért a szóról nem ismeri fel a motívumot. A Károli-szóra épülő háló 298 olyan verset is hozott, amelyben ugyanezek a magyar szavak más héber vagy görög szót fordítanak, köztük a sírás igéjét.

**Lélek és szellem.** A Károli a πνεῦμα (pneuma) és a ψυχή (pszükhé) szót nem választja szét. A Lukács 1:46–47-ben mindkettő „az én lelkem”; az 1Thessz 5:23-ban a pneuma „valótok”, a Zsid 4:12-ben a pszükhé „szívnek”. „Szellem” csak az 1Kor 15:45-ben áll („megelevenítő szellemmé”). A megkülönböztetés, amely a motívum lényege, a magyar szövegben nem látszik, csak az eredetiben.

**A formula.** A „segítségül hívni az Úr nevét” a Károliban állandó fordulat („segítségűl hívá az Úrnak nevét”). Itt ezért a Károli-háló szűkebb, mint a Strong-háló: 96 verset hoz, a Strong-háló 204-et. A „hív” és a „kiált” ige önmagában viszont túl tág, mert a Károliban elnevezést és meghívást is fordít. A háló ezért csak azokat a verseket számolja, ahol a „név” is mellettük áll.

A kizárási döntések egy része éppen a Károli-szóból fakad. A seól-motívumnál 295, a „segítségül hívás” motívumnál 51 vers azért esik ki, mert a magyar szó mögött más héber vagy görög szó áll.

## 4. Az adatkészlet

A kilenc motívum nem egyforma érettségű. Három (seól/hádész, pneuma/pszükhé, „segítségül hívni az Úr nevét”) végigment a lexikon teljes kiadási eljárásán: lexikonlapja kiadott, az olvasói kapu nem talált rajta hibát, és a szerző átnézte. Ezek lezárt kiadások. A másik hat a projekt korábbi szakaszában, régebbi eljárással készült; adataik a mai sémában állnak és ugyanazon a kapun mentek át, de a teljes ellenőrzés még hátravan, és a későbbi változatokban frissülnek. Az állapotot a csomag minden motívumnál adatként rögzíti (`motivumok.tsv`, `feldolgozasi_allapot`).

| Motívum (rövid címke) | Az azonosság hordozója | Előfordulás | Feldolgozási állapot |
|---|---|---:|---|
| ALVIL-001 — Hádész/Seol | szó | 74 | lezárt kiadás |
| ANTROP-001 — Pneuma/pszükhé | szó | 11 | lezárt kiadás |
| ISTENTISZT-001 — Névbe vetett segítségülhívás | szókapcsolat | 22 | lezárt kiadás |
| HAMART-001 — Bűn gyűrűzése | szavak együttállása | 52 | régi feldolgozás, frissítés alatt |
| HODIT-001 — Refáim/óriás-népek | szó | 33 | régi feldolgozás, frissítés alatt |
| KIRALY-001 — Melkizedek-rend | szó | 9 | régi feldolgozás, frissítés alatt |
| MENNY-001 — Isten fiai/Nefilim | szó | 9 | régi feldolgozás, frissítés alatt |
| TEREMT-001 — Tehóm/Abüsszosz | szó | 42 | régi feldolgozás, frissítés alatt |
| TEREMT-002 — Tohu va-vohu | szókapcsolat | 3 | régi feldolgozás, frissítés alatt |

A 255 előfordulásból 107 a lezárt, 148 a régi feldolgozású motívumokhoz tartozik.

| | |
|---|---|
| Név és kiadás | PaRDeS nyílt mag, kiadás 2026-11-04-8f3a2c1a00769da7 |
| Hely | `<DOI>` (kanonikus közzétételi hely: `<KANONIKUS_FORRAS_URL>`) |
| Formátum | UTF-8 TSV (tabulátorral tagolt, idézőjelezés nélkül), Markdown, SHA-256 ellenőrzőösszeg; 20 fájl, 507 141 bájt |
| Táblák | motívumok (9), előfordulások (255), felvételi döntések (257), kizárások (418) és az összesítő sorok tagjai (3 115), igehely-kapcsolatok (32), motívumok közötti kapcsolatok (3), döntésnapló (8), források és licencek (54), kódkönyv (213 bejegyzés, magyarul és angolul) |
| Létrehozás | 2026-08-22 – 2026-11-04 |
| Nyelv | magyar oszlopnevek és értékek, héber és görög szavakkal; a kódkönyv kétnyelvű |
| Licenc | CC BY 4.0; a szemantikai domének külön rétege (UBS SDBH/SDGNT, 237 sor) CC BY-SA 4.0 |
| Készítő | `<SZERZO>` |

A sorok négy forrásra épülnek: a TAHOT és a TAGNT címkézett szövegére (CC BY 4.0; STEPBible, é. n.), az OpenBible.info kereszthivatkozásaira, amelyek a Treasury of Scripture Knowledge-ből származnak (CC BY; OpenBible.info, é. n.), és az 1908-as Károli-szövegre, amely kora miatt közkincs. 25 forrást kihagytunk: kilenc a projekt zárt, származtatott rétege, kilencnek tisztázatlan a licence, háromnál korlátozott a kereskedelmi felhasználás, négy CC BY-SA forrásra pedig a csomagnak nincs szüksége.

A PaRDeS-szint (Peshat, Remez, Drash, Sod) recepciós címke. Azt mondja meg, hogyan kapcsolódik egy hely a motívumhoz a középkori zsidó négyes olvasási séma nyelvén; azt nem, hogy mit szándékolt a bibliai szerző. Az adatkészlet a bibliai korpuszon belül marad. Ókori közel-keleti összevető réteg nincs benne, így egy ilyen párhuzam hiánya nem lelet.

## 5. Ellenőrzés és korlátok

**Az ellenőrzés lánca.** Három szinten ellenőriztünk. Először a csomag kapuja: ez a belső jelölést, a kódkönyv lefedését, a licencszűrést, a hivatkozások feloldását és a bájtazonos újragenerálást vizsgálja (ebben a kiadásban 0 hibával és 9 figyelmeztetéssel). Az olvasói kapu ezen felül minden kiadott lexikonlapon nulla olvasói hibát követel. Másodszor egy friss kontextusú MI-ellenőr minden változást saját lekérdezéssel újra megvizsgál, egy második modell pedig a motívum határát nézi át. Harmadszor a lezárt három motívum a hivatalos kiadási eljáráson is átment: ezekről nyolc rögzített vizuális átnézés és 29, a szerző által jóváhagyott javítás tanúskodik.

**Korlátok.** A legfontosabb korlát az, hogy a kilenc motívumból csak három lezárt kiadás. A másik hat régebbi eljárással készült: a kiadási eljárás átnézései és javításai rájuk még nem vonatkoznak, és adataik a későbbi változatokban módosulhatnak. Aki csak a lezárt anyaggal akar dolgozni, a `feldolgozasi_allapot` mező szerint szűrhet. A szerzőn kívül minden ellenőr program vagy nyelvi modell; független szakmai lektorálás és annotátorok közötti egyezésmérés nem volt. A 255 előfordulásból 251-et szerkesztői döntésként rögzítettünk, nem egyetlen lekérdezés kimeneteként. A Strong-hozzárendelésből 183-at igazoltunk a TAHOT héber szövegén. 36 újszövetségi helyen áll, ahol héber szöveg nincs, 36 pedig nincs igazolva. A Károli-kiadás kereszthivatkozás-táblájában más versek listájának másolatai állnak (5 078 gyanús forrásvers). Ebből a táblából az adatkészlet adatot nem vesz át, de 28 kizárás-sort ezen keresztül találtunk. Végül a minta kicsi: kilenc motívum.

## 6. Újrahasznosítás

Az előfordulás- és a kapcsolattáblák igehely-hálózatot adnak, amelyben a helyeket közös héber és görög szavak kötik össze, és a negatív lelet is ki van mondva. A Hays-féle kritériumokra épülő intertextualitás-vizsgálatok (Hays, 1989) mellé így dokumentált döntési nyom kerül. Az indokolt felvételek és kizárások próbakészletként szolgálhatnak visszakeresési vagy osztályozási feladatokhoz. Kérdés lehet például, hogy egy rendszer szétválasztja-e az Úr nevének segítségül hívását az elnevezéstől. A negatív kritérium, a fölérendelt fogalom és a háromhálós teljesség-mérés más korpuszra is átvihető.

**A Károli-fordítás mint vizsgálati tárgy.** A 3. szakasz a Károli-szót olvasói rétegként mutatta be, a fordítás azonban önmagában is kutatási tárgy. Károli Gáspár 1590-es fordítása, amelyet az adatkészlet 1908-as revíziójában használ, évszázadokon át a magyar protestánsok bibliája volt [HIVATKOZÁS: a Károli-fordítás és revízióinak története, recepciója]. Az adatkészletből soronként kiolvasható, hogyan adja vissza ez a népnyelvi fordítás a motívum héber vagy görög szavát: a Károli-szót tartalmazó 203 sor mindegyike megadja a vers magyar szóalakját, mellette a párosítás módját és bizonyosságát. Egyetlen szűréssel összegyűjthető tehát ugyanannak a szónak minden magyar megfelelője. A tehóm (H8415) 35 sorából 28-ban „mély” tövű szó áll (mélység, mély vizek, mély ár), hétben más, például hullám, víz-ár, tenger, örvény. A Refáim nevet (H7497) a Károli-szöveg 13 versben átírja, négyféle írásmóddal (Réfaim, Refaim, Refáim, Refeus), 11 versben lefordítja („óriás”); az átírt alakok közül nyolc a Refáim völgyének helynevében áll. Ilyen adatokon vizsgálható a fordítói következetesség, az átírás és a fordítás közötti választás, a szóhasználat egységesítése vagy annak hiánya, és az is, milyen képet kapott a magyar olvasó egy-egy bibliai fogalomról. A szerkesztő által párosított 176 szópár magyar szóillesztő programok próbaanyagául is szolgálhat. A Károli-szó itt tárgy, nem mérce: az adatkészlet leírja a fordítást, nem minősíti. Három korlátra érdemes figyelni. Csak a motívumszó van párosítva, a vers többi szava nem; a Strong-számokkal címkézett teljes Károli-szöveg a lexikon zárt rétege. 27 sorban a párosítás gépi vagy következtetésen alapul (ebből 25 modell-kimenet), ezt az `azonositas_modja` mező jelöli. A szerkezeti motívum (HAMART-001) 52 sorában pedig nincs Károli-szó, mert ott nem egyetlen szó hordozza az azonosságot.

## Nyilatkozat a mesterséges intelligencia használatáról

A lekérdezéseket determinisztikus programok végzik. A felvételi és kizárási döntések az Anthropic Claude nyelvi modelljeivel segített munkamenetekben születtek (a modellek nevét munkamenetenként a projekt naplói rögzítik), mindegyik indoklással. Az adatkészlet döntéseket és rövid indoklásokat tartalmaz, modell írta értelmező prózát nem. A Károli-szó párosításának egy része gépi, és így is van jelölve. A fent leírt MI-ellenőrzések modellfutások. A kézirat szövegét a claude-opus-5-5 modell fogalmazta a repó adataiból. MI-eszköz nem szerző; az adatokért és a szövegért `<SZERZO>` felel. `<SZERZOI_NYILATKOZAT>`

## Összeférhetetlenség

A szerző a nyílt adatra épülő lexikont kereskedelmi kiadásban is megjelenteti. `<OSSZEFERHETETLENSEG_MEGFOGALMAZAS>`

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
| 9 motívum; 6 szó, 2 szókapcsolat, 1 szavak együttállása (lexikai / formulaikus / strukturális); mindkét mező kitöltve | P1.motivum, P1.azonossag, P1.ures_negativ_kriterium, P1.ures_folerendelt | `nyilt_mag/motivumok.tsv` |
| 3 lezárt kiadás, 6 régi feldolgozás; motívumonként a táblázatban | P1.feldolgozasi_allapot | `nyilt_mag/motivumok.tsv`, `feldolgozasi_allapot` (forrása: `adat/kiadasok.tsv` és az `olvasoi_kapu.py` a kiadott lapon) |
| 107 és 148 előfordulás állapot szerint; motívumonként 74 / 11 / 22 / 52 / 33 / 9 / 9 / 42 / 3 | P2.allapot_szerint, P2.motivumonkent | `nyilt_mag/elofordulasok.tsv` × `nyilt_mag/motivumok.tsv` |
| 255 előfordulás; 251 kézi döntés; 183 / 36 / 36 | P2.elofordulas_sor, P2.kezi_dontes, P2.igazolas | `nyilt_mag/elofordulasok.tsv` |
| 203 kitöltött Károli-szó; 176 / 25 / 2; 192 / 11 | P2.karoli_szo_kitoltve, P2.azonositas_modja, P2.megbizhatosag | `nyilt_mag/elofordulasok.tsv`, `karoli_szo`, `azonositas_modja`, `megbizhatosag` |
| 74 seól-sor; sír 29, Seol 19, pokol 17, koporsó 5, mélység 2, alvilág 2 | P2.motivumonkent, P9.alvil_karoli | `nyilt_mag/elofordulasok.tsv`, ALVIL-001, `karoli_szo` (kisbetűs részszöveg-egyezés; egy sor több alakot is tartalmazhat) |
| a „lélek/szellem” Károli-alakjai | — | `nyilt_mag/elofordulasok.tsv`, ANTROP-001, `karoli_szo` (Luk 1:46, 1:47, 1Thessz 5:23, Zsid 4:12, 1Kor 15:45) |
| „segítségűl hívá az Úrnak nevét” | — | `nyilt_mag/elofordulasok.tsv`, ISTENTISZT-001, `karoli_szo` |
| 6. szakasz, Károli-bekezdés: 203 kitöltött sor, a HAMART-001 52 sorában nincs Károli-szó; 176 szerkesztői pár | P2.karoli_szo_kitoltve, P10.karoli_motivumonkent, P2.azonositas_modja | `nyilt_mag/elofordulasok.tsv`, `karoli_szo`, `azonositas_modja` = tartalom-alapú |
| tehóm (H8415): 35 sor, 28 „mély” tövű, 7 más | P10.alak_strongonkent, P10.H8415 | `nyilt_mag/elofordulasok.tsv`, `strong` = H8415, `karoli_szo` („mély” részszöveg) |
| Refáim (H7497): 13 átírás négy írásmóddal, ebből 8 a völgy nevében; 11 „óriás” | P10.H7497, P10.H7497_irasmod | `nyilt_mag/elofordulasok.tsv`, `strong` = H7497, `karoli_szo` (Réfaim / Refaim / Refáim / Refeus, illetve „óriás” részszöveg) |
| 27 gépi vagy kikövetkeztetett párosítás, ebből 25 modell-kimenet | P10.gepi_vagy_kovetkeztetett, P2.azonositas_modja | `nyilt_mag/elofordulasok.tsv`, `azonositas_modja` = szó-szintű-gépi (25) vagy kikövetkeztetett (2) |
| 298 „sír”-vers a Károli-hálóban | P8.ALVIL-001 | `naplok/F123_teljesseg_ALVIL-001.md`, 1. és 2. szakasz |
| 96 és 204 vers (formula) | P8.ISTENTISZT-001 | `naplok/F123_teljesseg_ISTENTISZT-001.md`, 1. Összegzés |
| 418 / 394 / 24 / 3 115 / 3 509; 54 okkategória; 1 713 / 651 / 295; 58 / 40 / 29 | P3.* | `nyilt_mag/kizarasok.tsv` |
| 295 (seól) és 51 („segítségül hívás”) vers: a Károli-szó más szót fordít | P3.ok | `nyilt_mag/kizarasok.tsv`, „más szó a Károli-fordításban” (ALVIL-001, 5 sor), „a Károli-szó más szót fordít” (ISTENTISZT-001, 1 sor) |
| 28 kizárás-sor a Károli-kereszthivatkozásból | P3.keresesi_mod | `nyilt_mag/kizarasok.tsv`, `keresesi_mod` |
| 3 115 tag, minden összesítő sor felsorolva | P3.csoport_tabla_sor = P3.csoport_vers; P3.osszesito_tag_nelkul = 0 | `nyilt_mag/kizarasok.tsv`, `nyilt_mag/kizaras_csoportok.tsv` |
| 257 / 32 / 3 / 8 / 213 / 237 sor | P4.* | a csomag azonos nevű fájljai |
| 54 forrás; 25 kizárt (9 / 9 / 3 / 4) | P5.forras_sor, P5.kizart_ok | `nyilt_mag/forrasok_es_licencek.tsv` |
| 20 fájl, 507 141 bájt; dátumtartomány; kiadás-azonosító | P6.fajl, P6.meret_bajt, P6.datum_tartomany, P0.kiadas | `nyilt_mag/` |
| 0 hiba, 9 figyelmeztetés | — | `python eszkozok/nyilt_mag_kapu.py`, 2026-11-04 |
| 3 kiadott motívum, 8 átnézés, 29 javítás | P7.* | `adat/kiadasok.tsv`, `adat/lap_atnezesek.tsv`, `adat/lap_javitasok.tsv` |
| teljesség-mérés (1 233 / 651 / 582 / 12 stb.) | P8.* | `naplok/F123_teljesseg_<ID>.md`, 1. Összegzés (az 582 a HAMART-001 napló „Eredmény” 1. pontjából) |
| 5 078 gyanús forrásvers | — | `nyilt_mag/ISMERT_HIBAK.md`, 1. szakasz |

## Jegyzet: kettős közlés

Ugyanaz a mű nem lehet egyszerre két folyóiratnál elbírálás alatt; a JDMDH és az RDJ beküldési feltétele ezt ki is mondja, és a Digitális Bölcsészet is korábban nem közölt művet vár (❓, a „Labor” rovatra nem ellenőrzött). A magyar és az angol kézirat ezért **két külön mű** csak akkor, ha a hangsúlyuk valóban eltér, és egymásra kölcsönösen hivatkoznak:

- **az angol** (`kezirat_en.md`) az adatkészletet írja le (data paper: szerkezet, formátum, újrahasznosítás);
- **a magyar** (ez a kézirat) a módszer kizárási eszközeire és a magyar olvasói rétegre (a Károli-szó) helyezi a hangsúlyt; az adatkészlet leírása itt csak két táblázat.

A számok és a mondatok egy része szükségszerűen közös (ugyanaz az adat). Ha a szerkesztőség ezt átfedésnek tekinti, a másodközlés csak a két folyóirat tudtával, a második közlésben az elsőre való hivatkozással lehetséges.

**Javasolt sorrend** (a döntés a felhasználóé): (1) a nyílt mag letétele (DOI); (2) az angol data paper beküldése a fő csatornára; (3) a magyar kézirat beküldése **az angol elfogadása után**, a kísérőlevélben a két közlés viszonyának kimondásával, és a magyar szövegben az angolra hivatkozva (`<ANGOL_KOZLEMENY_HIVATKOZAS>`). Párhuzamos beküldés csak akkor, ha mindkét szerkesztőség előzetesen hozzájárul.

## Jegyzet: a „Labor” rovat (Digitális Bölcsészet)

Forrás: `folyoirat_lehetosegek.md` (PR #632), ✅ = a folyóirat oldaláról lekérve, ❓ = nem ellenőrzött.

- A rovat kódot, adatkészletet és vizualizációt közöl, **rövid magyar és angol leírással és dokumentációval** ✅. A kézirat ezért magyar kivonattal, angol absztrakttal és dokumentáló szakaszokkal készült. A rovat szerkezeti és terjedelmi előírását nem találtuk ❓; a „Műhely” rovat határa 5 000 szó ✅, ez a kézirat ennél jóval rövidebb.
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
| `<OSSZEFERHETETLENSEG_MEGFOGALMAZAS>` | a lexikon kereskedelmi kiadásának viszonya a nyílt adathoz (a megfogalmazás a szerzőé) |
| `<TAMOGATO>` | finanszírozó, vagy „A kutatás külső támogatás nélkül készült.” |
| `[HIVATKOZÁS: a Károli-fordítás és revízióinak története, recepciója]` | 6. szakasz, Károli-bekezdés (F171): egy ellenőrzött irodalmi tétel arra, hogy a Károli-fordítás (1590, revízió 1908) évszázadokon át a magyar protestánsok bibliája volt; a választás a szerzőé, a szöveg jelölt nélkül készült |

## Nyitott kérdések

1. A kettős közlés sorrendje és a két folyóirat tájékoztatása (fent).
2. A „Labor” rovat szerkezete, terjedelme, anonimizálási szabálya és hivatkozási stílusa: a szerkesztőségtől kérdezendő.
3. A HAMART-001 582 nyitott verse, a Károli 1908 licence, a hivatkozások ellenőrzése: mint az angol kéziratnál.
4. A hat régi feldolgozású motívum frissítése: ha a letét előtt valamelyik lezárt kiadás lesz, a 4. szakasz táblázata, a kivonat „három / hat” mondata és a 107 / 148 frissül (`szamok.py` újrafuttatásával).
