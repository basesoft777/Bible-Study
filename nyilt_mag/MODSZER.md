# Módszer — a motívum-adatmag

*Logosz-lexikon — nyílt adatmag · adatállapot: 2026-11-10 · DOI: 10.5281/zenodo.24141612*

## 1. Mi ez az adatkészlet

Bibliai motívumok nyílt adatkészlete. Motívumnak olyan visszatérő bibliai témát nevezünk, amelynek jelenléte egy
versben a héber vagy a görög szövegen ellenőrizhető: egy szón, egy állandó szókapcsolaton vagy szavak
együttállásán. A csomag 9 motívumot tartalmaz, 250 előfordulással. Mellettük ugyanolyan részletesen áll a
másik oldal is: 540 kizárás-sor rögzíti indoklással azokat a helyeket, amelyeket megvizsgáltunk, de a
motívumhoz nem soroltunk.

A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva. Az adatmagban döntések és rövid indoklások állnak, értelmező próza nem.

## 2. A motívum meghatározása

Egy motívum akkor kap azonosítót, ha négy kérdésre megvan a válasz: mi hordozza az azonosságát; mi az a legkisebb
jegy, amely nélkül egy hely nem tartozik ide (a kizáró jegy); ha egy hely két motívumhoz is tartozik, más-e a
szerepe a kettőben; és nem részhalmaza-e egy másik motívumnak. Minden motívum megnevezi azt a tágabb fogalmat is,
amely felé a határa szétfolyna (fölérendelt fogalom). Ha egy hely csak ezen keresztül kapcsolódik, kimarad.

A `motivumok.tsv` ezt három oszlopban adja: az azonosság hordozója (`azonossag_tipusa`; ebben a kiadásban
lexikai: 6; formulaikus: 2; strukturális: 1), a kizáró jegy (`negativ_kriterium`) és a fölérendelt fogalom (`folerendelt_fogalom`). Az olvasói
meghatározás (`meghatarozas`) egy-két mondatban mondja meg, mi a motívum; ebben a kiadásban 1 motívumnál áll,
a többinél üres. A motívum határát azonban nem a meghatározás rajzolja meg, hanem a kizárások.

## 3. A jelöltek gyűjtése

A lehetséges előfordulásokat (jelölteket) rögzített sorrendű keresések hozzák elő:

1. a motívum törzshelyein közösen előforduló szavak Strong-számai, a névelők, kötőszók és más nyelvtani szavak
   nélkül;
2. a szemantikai mező feltevése: ez az egyetlen nem gépi lépés, ezért a mező szavait rögzítjük;
3. a teljes ó- és újszövetségi szöveg átvizsgálása Strong-szám szerint, a STEPBible címkézett szövegén (TAHOT,
   TAGNT);
4. két szó együttes előfordulása egy versben;
5. az igealak ellenőrzése;
6. a Septuaginta-megfelelés.

Az 1. és a 3–6. lépést program végzi, ugyanarra a bemenetre ugyanazt az eredményt adja. Jelöltet hoztak még a
kereszthivatkozások (Treasury of Scripture Knowledge; a Károli-kiadás kereszthivatkozásai, l. `ISMERT_HIBAK.md`),
szótári szócikkek és a szerkesztői teljességi felmérés. Hogy egy döntött jelölt honnan jött, a `kizarasok.tsv` és
a `beepitesi_dontesek.tsv` `keresesi_mod` oszlopa mondja meg (ebben a kiadásban 11 keresési mód).

## 4. Döntés minden jelöltről

Keresési találatból nem lesz közvetlenül előfordulás. Minden jelöltről döntés születik, indoklással. A felvett
jelölt az `elofordulasok.tsv`-be kerül, a döntés indoklása a `beepitesi_dontesek.tsv`-be (252 sor); az
elutasított a `kizarasok.tsv`-be, egy kizárási okkal (61 ok) és indoklással.

A kizárás-sorok közül 443 egy-egy helyről szól. 97 sor összesítő: egy csoportot képvisel,
amelynek minden versét ugyanabból az okból utasítottuk el; a csoportok 3 984 versét a
`kizaras_csoportok.tsv` sorolja fel, és az összesítő sor indoklása a csoport minden versére érvényes.

Ha egy keresés üres, az eredmény üres marad: a hiányt nem töltjük ki gyenge vagy asszociatív anyaggal. A még el
nem döntött jelöltek (20) nincsenek a csomagban. Ahol egy sor szerkesztői döntésre hivatkozik, a döntés
nyilvános azonosítója (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel (15 döntés).

## 5. Az előfordulás sora

Minden előfordulás egy igehely, és megnevezi, mire épül a besorolása (`horgony_tipus`, `horgony`): szóbázis: 197; közös szóbázis: 33; kollokáció (szópár egy versben): 13; tematikus kapcsolat: 4; formula-kapcsolat: 1; hivatkozás-kapcsolat: 1; idézet-kapcsolat: 1.
A `strong` oszlop a horgonyszó Strong-száma, a `jelentes_en` a szótári jelentés kivonata, a `strong_glossza_en` a
STEPBible rövid angol glosszája.

**A Károli-szó.** Minden előfordulásnál ott áll a Károli-fordítás megfelelő szava is. A Károli-szó nem bizonyíték:
azt mutatja meg, mit lát a helyből a magyar olvasó. A párosítást (`azonositas_modja`) 223 esetben a
szerkesztő végezte a Károli-szöveg olvasásával, 25 esetben gépi szópárosítás adta (csak magas
bizonyosságú pár igazolhat sort), 2 esetben következtetés. A bizonyosság (`megbizhatosag`)
234 esetben magas, 16 esetben közepes. A vers többi szavának párosítása nem része ennek az
adatkészletnek; az a kapcsolódó Károli – Strong adatkészletekben áll.

**Eredetjelölés.** Minden sor megnevezi, honnan származik: ha lekérdezésből, akkor a lekérdezés típusát, a forrást,
annak licencét és a dátumot; ha nem, azt, hogy kézi döntés, lekérdezés nélkül. Az előfordulások közül 246
kézi döntés, 4 egy lekérdezés közvetlen eredménye. A „kézi döntés” nem azt jelenti, hogy a sor ellenőrzött,
hanem azt, hogy nem egyetlen lekérdezés adta. A Strong-hozzárendelést 181 sorban a TAHOT héber szövegén
tételesen visszakerestük (`igazolas`).

## 6. Feldolgozási állapot

4 motívum lezárt kiadás (ALVIL-001, ANTROP-001, HAMART-001 és ISTENTISZT-001): a lexikonlapjuk kiadott, és hiba nélkül átment az olvasói kapun. A
többi 5 a projekt korábbi szakaszában, régebbi eljárással készült. Adataik a mai sémában állnak, és ugyanazon
a kapun mennek át, de a kiadási eljárás átnézései rájuk még nem vonatkoznak, és a későbbi változatokban
módosulhatnak. Az állapot a `motivumok.tsv` `feldolgozasi_allapot` oszlopában áll; aki csak a lezárt anyaggal
dolgozna, ezen szűrhet.

## 7. A visszhang-réteg

Négy tábla a motívumok ókori fordításbeli és értelmezői visszhangját adja, forrásonként a licenccel:

- `visszhang_megfelelok.tsv` (101 sor): a horgonyszavak megfelelője a Targumban (32), a
  Vulgatában (38) és a Septuagintában (31);
- `visszhang_tanuk.tsv` (6 sor): egyházatyai, rabbinikus és Glossa Ordinaria-tanúk: ki, melyik műben, mit
  lát a helyen, saját szavas egy mondatban, idézet nélkül;
- `vitatott_forrasok.tsv` (3 sor): a vitatott pontok lektorált szakirodalma, csak bibliográfiai adat; az üres
  szerző azt jelenti, hogy a vizsgált adatbázisokban a pontról lektorált forrás nem került elő;
- `sblgnt_apparatus.tsv` (61 sor): az újszövetségi helyek kritikai apparátusa.

Csak ellenőrzött sor kerül be. A Septuaginta-megfelelők közül azokat, amelyeknél a versben egyetlen lemma jön
szóba, gép ellenőrizte; minden más sort egy második kéz nézett át. Nincs a csomagban: a Chain Lineage Browser
tanúi (a böngésző licencet nem közöl), a BDB rokon nyelvi sorai (külön döntésre várnak), és a források szövege.

## 8. Az angol réteg

Az oszlopnevek és az értékek magyarok; mellettük angol párhuzamos oszlopok állnak.

- **Igehely:** minden igehely-oszlop mellett `…_osis`, szabványos OSIS-kulccsal. A könyvkód szabványos, a fejezet- és
  versszám a Károli-fordítás számozása; ahol ez eltér a STEPBible-számozástól, a kulcs a Károli-verset jelöli.
- **Zárt értékek:** minden zárt értékkészletű oszlop mellett `…_en`, a kódkönyv szerkesztett angol címkéjével.
- **Szabad szöveg** (indoklás, funkció, a motívum meghatározása, a döntésnapló): `…_en` párhuzamos mező, **gépi
  fordítás** (főként `claude-sonnet-5-5`; kis részben `claude-opus-5-5`). A sor `forditas_modja` oszlopa megnevezi a modellt, és kimondja a hiányt
  (38 sorban hiányzik a fordítás teljesen vagy részben).

## 9. Licencszűrés

A csomag csak közkincs, CC0 vagy CC BY 4.0 licencű forrásból vesz át értéket, a projekt licencleltára szerint.
23 forrást kizártunk: nem kereskedelmi vagy GPL licencűt, tisztázatlan licencűt, és a projekt zárt,
származtatott rétegeit. A kizárt források listája és oka az `ATTRIBUCIO.md`-ben és a `forrasok_es_licencek.tsv`-ben
áll. A CC BY-SA 4.0 licencű szemantikai domének (UBS SDBH/SDGNT) külön könyvtárban vannak (`cc_by_sa_reteg/`),
mert a ShareAlike feltétel a belőlük származó munkára is kiterjed; a csomag többi része ettől független. A leltár
nem jogi vélemény.

## 10. A mesterséges intelligencia használata

A keresések determinisztikus programok. Hogy egy jelölt a motívumhoz tartozik-e, arról mesterséges intelligenciával
segített munkamenet dönt, a szerkesztő irányításával, és minden döntés indoklással rögzül. Gép végezte még a
Károli-szó gépi párosítását (5. pont), a szabad szöveges mezők angol fordítását (8. pont) és a Septuaginta-megfelelők
egyértelmű eseteinek ellenőrzését (7. pont). Az adattáblákat program állítja elő az adatból, nyelvi modell nem írja
őket; ugyanabból az adatból mindig ugyanaz a csomag készül. A leíró szövegeket (ez a módszerleírás, az olvass-el és
a közlemény) nyelvi modell fogalmazta, a számokat az export adja, a szöveget a szerkesztő hagyta jóvá. A modell nem
szerző; a tartalomért a szerző felel.

## 11. Ellenőrzés

A csomag saját gépi kapuja minden kiadás előtt fut. Méri a belső munkajelölést, a kódkönyv lefedettségét (minden
oszlop és zárt érték, mindkét nyelven), a licencszűrést, a döntés- és motívum-hivatkozások feloldását, az összesítő
sorok tagszámát, az OSIS-kulcsokat, a fordítás frissességét és a bájtazonos újragenerálást. Az
`ELLENORZO_OSSZEG.sha256` minden kiadott fájl SHA-256 összegét tartalmazza; a `KIADAS.txt` tartalmi hash-e ennek a
listának az összege.

A kiadott lexikonlapon az olvasói kapu nulla hibát követel. A munka minden lépésének változásait egy friss
kontextusú modell saját lekérdezéssel újra ellenőrzi; a motívum határát egy második modell nézi át. Ez nem
független szakmai lektorálás: a szerzőn kívül minden ellenőr program vagy nyelvi modell.

## 12. Korlátok

- Lezárt kiadás csak 4 motívum; 5 régi feldolgozás (6. pont).
- A teljesség nem bizonyított. A keresések azt mérik, mennyit fog meg a lista a lexikai jegyek alapján; a
  tematikus kapcsolatot nem.
- Független szakmai lektorálás és annotátorok közötti egyezésmérés nem volt.
- A motívumokat a kutatási program választotta ki; nem reprezentatív mintái a Bibliának.
- A forrásadatok ismert hibáit és kezelésüket az `ISMERT_HIBAK.md` írja le.
