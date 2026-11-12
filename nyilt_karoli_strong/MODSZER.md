# Módszer — a Károli 1908 és az eredeti szöveg szavankénti párosítása

*Károli 1908 – Strong szóillesztés · Logosz-lexikon · 1. kiadás · adatállapot: 2026-11-01 · DOI: 10.5281/zenodo.24141884*

## 1. Mi ez az adatkészlet

Károli Gáspár fordításának 1908-as szövege, szavanként összekapcsolva a héber és görög eredeti szöveg szavaival. A
kapcsolat hordozója a Strong-szám: egy magyar szó Strong-számait az a héber vagy görög szó adja, amelyet fordít. A
csomag 66 könyvet, 31 158 verset, 599 367 magyar és 611 396 eredeti szót, valamint 598 715 szópárt tartalmaz.

A párosítás nyelvi modellek javaslata, mért pontossággal. Nem kézzel ellenőrzött adat: minden pár „javaslat” állapotú,
és a csomag megadja, mennyire bízhat benne az, aki használja — rétegenként, kapcsolattípusonként, konfidencia-intervallummal
(5.).

## 2. A két szöveg

A magyar oldal a Károli 1908 közkincs szövege. Az eredeti oldal a STEPBible két adatkészlete: a TAHOT (héber és arámi
Ószövetség) és a TAGNT (görög Újszövetség), mindkettő szavanként Strong-számmal és angol tükörfordítással. A TAHOT a
héber szót előtagjaira és ragjaira bontja: a kötőszó (*ve-*), a névelő, az elöljáró és a személyrag külön szóként, külön
számmal áll (H9001–H9049). Ezért egy magyar szóhoz gyakran több eredeti „szó” tartozik: a *Kezdetben* az elöljáróhoz és
a főnévhez is.

A szavakra bontás mindkét oldalon determinisztikus; az írásjel nem szó. Egy szót a vers és a versen belüli sorszáma
azonosít, oldalanként külön.

## 3. A versek megfeleltetése

A Károli versbeosztása helyenként eltér a héber és a görög szövegétől (főként a fejezethatárokon). A párosítás
előtt minden Károli-vershez megkerestük a neki megfelelő eredeti verset: a versek hosszának determinisztikus
igazításával, és ahol két vers egybe olvadt, kézi jóváhagyással. Az eredeti szavak ezért a Károli-vers kulcsán állnak;
az `eredeti_token` a megfeleltetett eredeti vers szavainak sorszáma.

## 4. A párosítás menete

**A feladat.** A modell versenként megkapta a magyar szavakat sorszámozva és az eredeti szavakat sorszámozva, alakkal,
Strong-számmal és angol tükörfordítással. Azt kellett megadnia, melyik magyar szó melyik eredeti szó(ka)t fordítja;
mely magyar szavaknak nincs eredetije (betoldás); és mely eredeti szavaknak nincs magyar megfelelője (fordítatlan). A
modell **Strong-számot nem ír**, csak sorszámokat: a Strong-szám a sorszámból, a forrásból jön. Így a modell nem találhat
ki számot.

**A szabályok.** A vitás esetekre írott szabálykészlet döntött, egy korábbi párosítási minta konvencióiból. A
fontosabbak: a magyar önálló névelő betoldás, a héber és görög névelő fordítatlan, kivéve, ha névmásként áll; a
kettéírt kötőszó és vonatkozó névmás (*a mely, a ki*) mindkét szava a közös eredetihez tartozik; a héber tárgyjelölő
fordítatlan, a tárgyi névmás a ragjához kötődik; a birtokos rag ahhoz a magyar szóhoz tartozik, amelyik a megfelelő
személyragot viseli; a különírt igekötő az ige eredetijéhez tartozik; a kitett alanyi névmás és a segédigei *vala* betoldás,
ha az eredetiben nincs külön szó; a héber *ve-* csak akkor kötődik, ha a magyarban a helyén kötőszó áll; a Textus
Receptusban nem szereplő görög szó fordítatlan.

**A gépi kapu.** Minden választ program ellenőrzött: minden magyar szó pontosan egyszer szerepel (párban vagy
betoldásként), minden eredeti szó legalább egyszer (párban vagy fordítatlanként), csak létező sorszám áll benne, és a
vers teljes. A kapun bukott választ a modell újra elkészítette. Ahol a versek megfeleltetése szavanként nem állt össze, vagy a
válasz végleg nem ment át a kapun, a vers kézi átnézésre vár: minden szava `fuggoben`, pár nélkül (45
vers).

**A modellek.** Mózes első két könyvét két független modell párosította ugyanazzal a feladatleírással: a Claude Sonnet
és a Gemini Flash. A két válaszból program állította össze a táblát: ahol a két modell ugyanazt a párt adta, a pár
`magas` bizonyosságú (52 844 pár); ahol eltértek, az első modell párja került be, `alacsony` bizonyossággal. A többi
könyvet a költségkeret miatt egy modell, a Claude Sonnet párosította; ezek párjai mind `alacsony`
(545 871 pár). A feladatleírás a futás alatt változatlan volt; a táblák a modellek mentett válaszaiból, újabb
modellhívás nélkül, bájtra azonosan újraépíthetők.

**Az eredmény.** 488 659 magyar szónak van párja, 109 914 betoldás; 547 585 eredeti szó párosított,
63 017 fordítatlan. A 598 715 párból 466 785 héber és 131 930 görög; 157 163 egy héber előtag- vagy
ragmorféma párja.

## 5. A pontosság mérése

A pontosságot két, egymást kiegészítő úton mértük.

**Vak ellenőrzés, rétegzett mintán.** A 598 715 párt nyolc rétegre osztottuk (Mózes két modellel és egy modellel; a
történeti, a költői és a prófétai könyvek; az evangéliumok és az Apostolok cselekedetei; a levelek; a Jelenések), és
rétegenként 200 párt húztunk véletlenszerűen. Egy harmadik nyelvi modell (Claude Opus) a minta minden céljára a
vers szövegéből és az eredeti szavakból maga jelölte ki a megfelelő eredeti szavakat, ugyanazokkal a szabályokkal, a gépi
pár ismerete nélkül. A pár helyes, ha az eredeti szava az ellenőr jelölései között van.

| réteg | n | helyes | arány | 95% |
|---|---|---|---|---|
| Mózes, két modell egyezése | 200 | 198 | 99,00% | 96,43–99,73% |
| Mózes, egy modell | 200 | 184 | 92,00% | 87,40–95,02% |
| történeti könyvek | 200 | 190 | 95,00% | 91,04–97,26% |
| költői könyvek | 200 | 190 | 95,00% | 91,04–97,26% |
| próféták | 200 | 186 | 93,00% | 88,59–95,78% |
| evangéliumok, Apostolok cselekedetei | 200 | 196 | 98,00% | 94,97–99,22% |
| levelek | 200 | 191 | 95,50% | 91,67–97,61% |
| Jelenések | 200 | 193 | 96,50% | 92,95–98,29% |
| **Ószövetség, súlyozott** | 1 000 | | 94,50% | 92,95–96,05% |
| **Újszövetség, súlyozott** | 600 | | 97,07% | 95,55–98,59% |
| **összes, súlyozott** | 1 600 | | **95,06%** | 93,81–96,32% |

A súlyozott becslés a rétegek pársúlyával számol. Kapcsolattípus szerint: a tartalmi szavak párjai 96,44%
(95%: 95,20–97,69%), a héber morfémák párjai 90,74% (95%: 87,18–94,29%). A két modell
egyezésének rétege 99,00%-os, de ebből nem következik, hogy a második modell okozza a különbséget: a két Mózes-réteg
könyvei nagyrészt eltérnek.

**Kalibráció.** Az ellenőr nem tévedhetetlen. Egy korábbi, kézzel összeállított mintán (374 mérhető eset) az
ellenőr 96,79%-ban (95%: 94,48–98,16%), a gépi párosítás 97,06%-ban (95%: 94,81–98,35%)
egyezett vele: az ellenőr nem pontosabb a párosításnál. Az eltérések egy része tehát az ellenőr hibája, és az egyezés
csak akkor alsó becslés, ha a közös (gépi és ellenőri) hiba elhanyagolható.

**Független összevetés.** Ezt a közös hibát egy független forrás méri: egy Strong-számokkal jelölt Károli-kiadás,
amelyet a csomag nem tartalmaz, és amelyből csak az összesített egyezés szerepel itt. Rétegenként egy teljes fejezetet
vetettünk össze (8 fejezet, 2 663 fő szó párja). A forrás szavanként egy fő Strong-számot jelöl, a ragban,
elöljáróban és névelőben álló mellékszót és a morfémát nem; ez a mérés tehát csak a fő szavak párjaira érvényes.

- A forrás ítéletét elfogadva a fő szavak párjainak 98,72%-a egyezik (95%: 98,22–99,08%; Ószövetség 98,93%,
  Újszövetség 98,50%).
- A 34 eltérést háromutasan ítéltük meg (gépi pár, forrás, vak ellenőr); ezek után 5 maradt a párosítás
  hibája, a fő szavak pontossága így 99,81% (95%: 99,56–99,92%).
- A fejezetek klaszterek, nem véletlen mintaelemek; a valódi bizonytalanság nagyobb, mint az intervallum.

**Hibatípusok.** A 1 600 mintapárból 72 tért el az ellenőrtől: szomszédos szó 37 (tartalmi
20, morféma 17), rossz szó a versben 17, fölös pár
16, azonos lexéma más előfordulása 2. A mérés minden száma a `meres.tsv`-ben
áll.

## 6. Miért nyílt adat

A párosítás nem hibátlan, és nem is így kerül közlésre. Szerkesztői döntés alapján nyílt adatként jelenik meg, mert a
pontossága **mérve és dokumentálva van**: rétegenként és kapcsolattípusonként, konfidencia-intervallummal, a hibák
típusával és a megerősített hibák listájával (`ISMERT_HIBAK.md`). A „javaslat” állapot és a bizonyosság-jelölés minden
páron megmarad. A közlés nem egy előre kitűzött küszöb teljesülésén alapul: a mérés előtt nem volt rögzített
kritérium, és utólag felállított küszöb utólagos kritérium volna.

## 7. A következő kiadás

Ez az 1. kiadás: a mért állapot, változatlanul. A 2. kiadás javítja a megerősített hibákat és a szomszédos szó
szabályellenes eseteit (szabályalapú utófeldolgozással, nem páronkénti folttal), majd ugyanazzal a protokollal újra
mér: rétegzett minta, vak ellenőr, független külső forrás. A 2. kiadás minőségi célját az 1. kiadás eredményeinek
ismeretében, előre rögzítettük: a független összevetés fő-szó egyezésének alsó széle legalább 98% (most 98,22%); a
vak ellenőrrel mért súlyozott egyezés alsó széle legalább 93% (most 93,81%), és egyetlen réteg pontbecslése sem
90% alatti (most a legkisebb 92,00%). A cél az 1. kiadásra nem vonatkozik.

## 8. Kapcsolódó adatkészlet

Ugyanezek a párok a Károli modernizált szövegén is megjelennek (https://doi.org/10.5281/zenodo.24141950). A modernizálás minden
szót a helyén hagyott, ezért a két csomag a vers és a szósorszám kulcsán szóról szóra összekapcsolható.
