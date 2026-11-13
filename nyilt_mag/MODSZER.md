# Módszer — a motívum-adatmag

*Logosz-lexikon — nyílt adatmag · adatállapot: 2026-11-12 · DOI: 10.5281/zenodo.24141612*

## 1. Mi ez az adatkészlet

Ez a csomag bibliai motívumok nyílt adatkészlete. Motívumnak olyan visszatérő bibliai témát nevezünk, amelynek
jelenléte egy versben a héber vagy a görög szövegen ellenőrizhető: egy szón, egy állandó szókapcsolaton vagy szavak
együttállásán. A csomag 9 motívumot tartalmaz, 250 előfordulással. Ugyanilyen részletesen szerepel a másik
oldal is: 554 kizárás-sor rögzíti indoklással azokat a helyeket, amelyeket megvizsgáltunk, de a motívumhoz nem
soroltunk.

A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva. Az adatmagban döntések és rövid indoklások állnak, értelmező próza nem.

## 2. A motívum meghatározása

Egy motívum akkor kap azonosítót, ha négy kérdésre megvan a válasz. Mi hordozza az azonosságát? Mi az a legkisebb
jegy, amely nélkül egy hely nem tartozik ide (a kizáró jegy)? Ha egy hely két motívumhoz is tartozik, más-e a
szerepe a kettőben? És nem részhalmaza-e a motívum egy másiknak? Minden motívum megnevezi azt a tágabb fogalmat is,
amely felé a határa szétfolyna (fölérendelt fogalom). Az a hely, amely csak ezen a tágabb fogalmon keresztül
kapcsolódik a motívumhoz, kimarad.

A `motivumok.tsv` ezt három oszlopban adja meg: az azonosság hordozója (`azonossag_tipusa`; ebben a kiadásban
lexikai: 6; formulaikus: 2; strukturális: 1), a kizáró jegy (`negativ_kriterium`) és a fölérendelt fogalom (`folerendelt_fogalom`). Az olvasói
meghatározás (`meghatarozas`) egy-két mondatban mondja meg, mi a motívum; ebben a kiadásban 2 motívumnál áll,
a többinél üres. A motívum határát azonban nem a meghatározás rajzolja meg, hanem a kizárások.

## 3. A jelöltek gyűjtése

A lehetséges előfordulásokat, vagyis a jelölteket rögzített sorrendű keresések hozzák elő:

1. a motívum törzshelyein közösen előforduló szavak Strong-számai, a névelők, kötőszók és más nyelvtani szavak
   nélkül;
2. a szemantikai mező feltevése: ez az egyetlen nem gépi lépés, ezért a mező szavait rögzítjük;
3. a teljes ó- és újszövetségi szöveg átvizsgálása Strong-szám szerint, a STEPBible címkézett szövegén (TAHOT,
   TAGNT);
4. két szó együttes előfordulása egy versben;
5. az igealak ellenőrzése;
6. a Septuaginta-megfelelés.

Az 1. és a 3–6. lépést program végzi, amely ugyanarra a bemenetre mindig ugyanazt az eredményt adja. Jelöltet hoztak
még a kereszthivatkozások (a Treasury of Scripture Knowledge és a Károli-kiadás kereszthivatkozásai), a szótári
szócikkek és a szerkesztői teljességi felmérés. Hogy egy eldöntött jelölt honnan jött, azt a `kizarasok.tsv` és a
`beepitesi_dontesek.tsv` `keresesi_mod` oszlopa mondja meg (ebben a kiadásban 11 keresési mód).

A Károli-kiadás kereszthivatkozás-táblájában másolat-típusú hibát találtunk. Ezt egy független második tanúval, a
Károli-fordítás MEK 00161 kiadásának kereszthivatkozásaival javítottuk, és a jelöltkeresés már a javított táblát
használja. A nyílt adatmag maga nem tartalmaz kereszthivatkozás-adatot; a hiba és a javítás részletei az
`ISMERT_HIBAK.md` 1. pontjában állnak.

## 4. Döntés minden jelöltről

Keresési találatból nem lesz közvetlenül előfordulás: minden jelöltről döntés születik, indoklással. A felvett
jelölt az `elofordulasok.tsv`-be kerül, a döntés indoklása a `beepitesi_dontesek.tsv`-be (252 sor). Az
elutasított jelölt a `kizarasok.tsv`-be kerül, egy kizárási okkal (62 ok) és indoklással.

A kizárás-sorok közül 454 egy-egy helyről szól. 100 sor összesítő: egy csoportot képvisel,
amelynek minden versét ugyanabból az okból utasítottuk el. A csoportok 4 034 versét a
`kizaras_csoportok.tsv` sorolja fel, és az összesítő sor indoklása a csoport minden versére érvényes.

Ha egy keresés üres, az eredmény üres marad: a hiányt nem töltjük ki gyenge vagy asszociatív anyaggal. A még el
nem döntött jelöltek (20) nincsenek a csomagban. Ahol egy sor szerkesztői döntésre hivatkozik, a döntés
nyilvános azonosítója (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel (17 döntés).

## 5. Az előfordulás sora

Minden előfordulás egy igehely, és megnevezi, mire épül a besorolása (`horgony_tipus`, `horgony`): szóbázis: 195; közös szóbázis: 33; kollokáció (szópár egy versben): 13; tematikus kapcsolat: 6; formula-kapcsolat: 1; hivatkozás-kapcsolat: 1; idézet-kapcsolat: 1.
A `strong` oszlop a horgonyszó Strong-száma, a `jelentes_en` a szótári jelentés kivonata, a `strong_glossza_en` a
STEPBible rövid angol glosszája.

**A Károli-szó.** Minden előfordulásnál ott áll a Károli-fordítás megfelelő szava is. A Károli-szó nem bizonyíték: azt
mutatja meg, mit lát a helyből a magyar olvasó. A párosítást (`azonositas_modja`) 223 esetben a
szerkesztő végezte a Károli-szöveg olvasásával, 25 esetben gépi szópárosítás adta (sort csak magas
bizonyosságú pár igazolhat), 2 esetben következtetés. A bizonyosság (`megbizhatosag`)
232 esetben magas, 18 esetben közepes. A vers többi szavának párosítása nem része ennek az
adatkészletnek; az a kapcsolódó Károli – Strong adatkészletekben áll.

**Eredetjelölés.** Minden sor megnevezi, honnan származik. Ha lekérdezésből, akkor megadja a lekérdezés típusát, a
forrást, annak licencét és a dátumot; ha nem, akkor azt mondja ki, hogy kézi döntés, lekérdezés nélkül. Az
előfordulások közül 246 kézi döntés, 4 egy lekérdezés közvetlen eredménye. A „kézi döntés” nem azt
jelenti, hogy a sor ellenőrzött, hanem azt, hogy nem egyetlen lekérdezés adta. A Strong-hozzárendelést
201 sorban a TAHOT héber szövegén tételesen visszakerestük (`igazolas`).

## 6. Feldolgozási állapot

Lezárt kiadás az a motívum, amelynek lexikonlapja a kész lap mai mércéje szerint jelent meg (ez a mérce 2026-11-11
óta érvényes), és hiba nélkül átment az olvasói kapun. Ilyen motívum ebben a kiadásban 1 van: HAMART-001.

A többi motívum, szám szerint 8, korábbi feldolgozás, újraírás alatt. Ezek a munka korábbi szakaszában,
régebbi eljárással készültek, és a lexikonlapjukat a mai mérce szerint újraírjuk. Az adatuk a csomagban marad, a mai
sémában áll, és a csomag gépi kapuján ugyanúgy átmegy, mint a lezárt motívumoké; a kiadási eljárás átnézései azonban
rájuk még nem vonatkoznak, ezért az adatuk az újraírás során változhat.

Az állapot a `motivumok.tsv` `feldolgozasi_allapot` oszlopában áll; aki csak a lezárt anyaggal dolgozna, ezen az
oszlopon szűrhet.

## 7. A visszhang-réteg

Négy tábla a motívumok ókori fordításbeli és értelmezői visszhangját adja, forrásonként a licenccel:

- `visszhang_megfelelok.tsv` (144 sor): a horgonyszavak megfelelője a Targumban (42), a
  Vulgatában (55) és a Septuagintában (47);
- `visszhang_tanuk.tsv` (8 sor): egyházatyai, rabbinikus és Glossa Ordinaria-tanúk: ki, melyik műben, mit
  lát a helyen, egyetlen saját szavas mondatban, idézet nélkül;
- `vitatott_forrasok.tsv` (3 sor): a vitatott pontok lektorált szakirodalma, csak bibliográfiai adat; az üres
  szerző azt jelenti, hogy a vizsgált adatbázisokban a pontról lektorált forrás nem került elő;
- `sblgnt_apparatus.tsv` (60 sor): az újszövetségi helyek kritikai apparátusa.

Ezekbe a táblákba csak ellenőrzött sor kerül be. A Septuaginta-megfelelők közül azokat, amelyeknél a versben egyetlen
lemma jön szóba, gép ellenőrizte; minden más sort egy második kéz nézett át. Három dolog nincs a csomagban: a Chain
Lineage Browser tanúi (a böngésző licencet nem közöl), a BDB rokon nyelvi sorai (külön döntésre várnak) és a források
szövege.

## 8. Az angol réteg

Az oszlopnevek és az értékek magyarok; mellettük angol párhuzamos oszlopok állnak.

- **Igehely:** minden igehely-oszlop mellett `…_osis` oszlop áll, szabványos OSIS-kulccsal. A könyvkód szabványos, a
  fejezet- és versszám a Károli-fordítás számozását követi; ahol ez eltér a STEPBible-számozástól, a kulcs a
  Károli-verset jelöli.
- **Zárt értékek:** minden zárt értékkészletű oszlop mellett `…_en` oszlop áll, a kódkönyv szerkesztett angol
  címkéjével.
- **Szabad szöveg** (indoklás, funkció, a motívum meghatározása, a döntésnapló): `…_en` párhuzamos mező, **gépi
  fordítás** (főként `claude-sonnet-5-5`; kis részben `claude-opus-5-5`). A sor `forditas_modja` oszlopa megnevezi a modellt, és kimondja a hiányt
  (222 sorban hiányzik a fordítás teljesen vagy részben).

## 9. Licencszűrés

A csomag csak közkincs, CC0 vagy CC BY 4.0 licencű forrásból vesz át értéket, a projekt licencleltára szerint.
23 forrást kizártunk: a nem kereskedelmi és a GPL licencűeket, a tisztázatlan licencűeket, valamint a
projekt zárt, származtatott rétegeit. A kizárt források listája és a kizárás oka az `ATTRIBUCIO.md`-ben és a
`forrasok_es_licencek.tsv`-ben áll. A CC BY-SA 4.0 licencű szemantikai domének (UBS SDBH/SDGNT) külön könyvtárban
vannak (`cc_by_sa_reteg/`), mert a ShareAlike feltétel a belőlük származó munkára is kiterjed; a csomag többi része
ettől független. A leltár nem jogi vélemény.

## 10. A mesterséges intelligencia használata

A keresések determinisztikus programok. Arról, hogy egy jelölt a motívumhoz tartozik-e, mesterséges intelligenciával
segített munkamenet dönt a szerkesztő irányításával, és minden döntés indoklással rögzül. Gép végezte még a
Károli-szó gépi párosítását (5. pont), a szabad szöveges mezők angol fordítását (8. pont) és a Septuaginta-megfelelők
egyértelmű eseteinek ellenőrzését (7. pont). Az adattáblákat program állítja elő az adatból, nyelvi modell nem írja
őket; ugyanabból az adatból mindig ugyanaz a csomag készül. A leíró szövegeket (ezt a módszerleírást, az olvass-el
fájlt és a közleményt) nyelvi modell fogalmazta, a számokat az export adja, a szöveget a szerkesztő hagyta jóvá. A
modell nem szerző; a tartalomért a szerző felel.

## 11. Ellenőrzés

A csomag saját gépi kapuja minden kiadás előtt lefut. Azt vizsgálja, hogy nem maradt-e a csomagban belső
munkajelölés, hogy a kódkönyv minden oszlopot és zárt értéket lefed-e mindkét nyelven, hogy érvényesül-e a
licencszűrés, hogy feloldható-e minden döntés- és motívum-hivatkozás, hogy egyezik-e az összesítő sorok tagszáma,
hogy helyesek-e az OSIS-kulcsok, hogy friss-e a fordítás, és hogy az újragenerálás bájtra azonos csomagot ad-e. Az
`ELLENORZO_OSSZEG.sha256` minden kiadott fájl SHA-256 összegét tartalmazza; a `KIADAS.txt` tartalmi lenyomata (hash)
ennek a listának az összege.

A kiadott lexikonlapon az olvasói kapu nulla hibát követel. A munka minden lépésének változásait egy előzmények
nélkül induló nyelvi modell saját lekérdezéssel újra ellenőrzi; a motívum határát egy második modell nézi át. Ez nem
független szakmai lektorálás: a szerzőn kívül minden ellenőr program vagy nyelvi modell.

## 12. Korlátok

- Lezárt kiadás csak 1 motívum. A többi, szám szerint 8, korábbi feldolgozás, újraírás alatt, és az
  adata az újraírás során változhat (6. pont).
- A teljesség nem bizonyított. A keresések azt mérik, mennyit fog meg a lista a lexikai jegyek alapján; a
  tematikus kapcsolatot nem mérik.
- Független szakmai lektorálás nem volt, és annotátorok közötti egyezést sem mértünk.
- A motívumokat a kutatási program választotta ki; nem reprezentatív mintái a Bibliának.
- A forrásadatok ismert hibáit és kezelésüket az `ISMERT_HIBAK.md` írja le; a Károli-kiadás kereszthivatkozásainak
  javítása az 1. pontjában áll.
