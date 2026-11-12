# A Károli-biblia 1908-as szövegének szavankénti párosítása a héber és görög eredetivel: nyílt adatkészlet mért pontossággal

*Kézirat-tervezet (data paper) · Károli 1908 – Strong szóillesztés · Logosz-lexikon · DOI: 10.5281/zenodo.24141884*

## Kivonat

Az adatkészlet a Károli-biblia 1908-as szövegének 599 367 szavát és a héber és görög eredeti szöveg 611 396 szavát
kapcsolja össze 598 715 szópárral, minden párt az eredeti szó Strong-számával. A párosítást nyelvi modellek végezték egy
írott szabálykészlet szerint; a modell csak sorszámot jelölt, a Strong-szám a STEPBible nyílt TAHOT és TAGNT adataiból
jön. A pontosságot kétféleképpen mértük: nyolc rétegből húzott véletlen mintán egy vak modell-ellenőrrel (a teljes
párkészleten 95,06%, 95%: 93,81–96,32%), és egy független, Strong-számos Károli-kiadással a fő szavak
párjain (98,72%, 95%: 98,22–99,08%). Az adatkészlet a mért állapotot adja közre, a megerősített hibák listájával
és a következő kiadás előre rögzített minőségi céljával. Licenc: CC BY 4.0.

## 1. Áttekintés

**Háttér.** A Károli-fordítás négy évszázada a magyar protestáns bibliaolvasás alapszövege, de a mögötte álló héber és
görög szavak szavankénti, szabadon használható hozzárendelése eddig hiányzott. Az angol nyelvterületen a Strong-számos
King James-szöveg régóta az olvasók és a kutatók alapeszköze; magyarul hasonló nyílt adat nem volt hozzáférhető. Ez az
adatkészlet ezt a hiányt pótolja, a Logosz-lexikon egyik nyílt adatmagjaként.

**A kérdés, amelyre válaszol.** Melyik magyar szó melyik eredeti szót fordítja; mely magyar szó a fordító betoldása;
mely eredeti szót nem ad vissza külön magyar szó. A harmadik kérdés ugyanolyan fontos, mint az első: a `szavak` tábla
minden szót egyszer sorol fel, így a fordítás „hiányai” is kiolvashatók.

## 2. Módszer

**Szövegek és szavakra bontás.** A magyar oldal a Károli 1908 közkincs szövege, az eredeti oldal a STEPBible TAHOT
(héber és arámi Ószövetség) és TAGNT (görög Újszövetség) adatkészlete. A TAHOT a héber előtagokat és ragokat külön
szóként kezeli (H9001–H9049); ezért egy magyar szóhoz gyakran több eredeti „szó” tartozik. A Károli versbeosztását a
párosítás előtt determinisztikus vershossz-igazítással feleltettük meg az eredetiének; két vers egybeolvadását kézzel
hagytuk jóvá.

**Párosítás.** A modell versenként sorszámozott magyar és eredeti szavakat kapott (az eredetinél alakkal,
Strong-számmal és angol tükörfordítással), és sorszámpárokat adott vissza, a betoldásokkal és a fordítatlan szavakkal
együtt. A vitás eseteket tizenkét írott szabály döntötte el: a névelőkről, a kettéírt kötőszóról és vonatkozó
névmásról, a tárgyjelölőről, a birtokos ragról, a különírt igekötőről, a kitett alanyi névmásról és a segédigéről, a
héber *ve-* kötőszóról, valamint a Textus Receptusban nem szereplő görög szóról. Minden választ program ellenőrzött
(minden magyar szó pontosan egyszer, minden eredeti szó legalább egyszer, csak létező sorszám); a bukott választ a modell
újra elkészítette. Mózes első két könyvét két független modell (Claude Sonnet és Gemini Flash) párosította: ahol
egyeztek, a pár `magas` bizonyosságú (52 844 pár). A többi könyvet a költségkeret miatt egy modell (Claude Sonnet)
párosította (`alacsony`, 545 871 pár). A táblák a mentett modellválaszokból bájtra azonosan újraépíthetők.

**Pontosságmérés.** (1) *Vak ellenőrzés.* A párkészletet nyolc rétegre osztottuk (Mózes két modellel és egy modellel;
történeti, költői és prófétai könyvek; evangéliumok és ApCsel; levelek; Jelenések), rétegenként 200 véletlen
párral. Egy harmadik modell (Claude Opus) a cél magyar szóhoz maga jelölte ki az eredeti szavakat, ugyanazokkal a
szabályokkal, a gépi pár ismerete nélkül. (2) *Kalibráció.* Egy korábbi, kézzel összeállított mintán az ellenőr
96,79%-ban, a gépi párosítás 97,06%-ban egyezett a mintával: az ellenőr nem pontosabb a párosításnál, ezért az
egyezés csak akkor alsó becslés, ha a közös hiba elhanyagolható. (3) *Független összevetés.* Ezt a közös hibát egy
Strong-számokkal jelölt Károli-kiadás méri, rétegenként egy teljes fejezeten (8 fejezet, 2 663 fő szó
párja); a forrás csak a fő szót jelöli, a mellékszót és a morfémát nem. Az eltéréseket háromutasan (gépi pár, forrás,
vak ellenőr) ítéltük meg. A külső forrás adata nem része az adatkészletnek, csak az összesített arány.

## 3. Eredmények

| mérés | becslés | 95% |
|---|---|---|
| teljes párkészlet, vak ellenőr, súlyozott | 95,06% | 93,81–96,32% |
| ebből Ószövetség / Újszövetség | 94,50% / 97,07% | 92,95–96,05% / 95,55–98,59% |
| tartalmi szó / héber morféma | 96,44% / 90,74% | 95,20–97,69% / 87,18–94,29% |
| fő szavak, a független forrás szerint | 98,72% | 98,22–99,08% |
| fő szavak, háromutas ítélet után | 99,81% | 99,56–99,92% |

A rétegek egyezése 92,00% (Mózes, egy modell) és 99,00% (Mózes, két modell egyezése)
között mozog; a rétegenkénti táblát az adatkészlet `meres.tsv` fájlja és módszertani leírása közli. A 1 600 mintapárból
72 tért el az ellenőrtől; a leggyakoribb típus a szomszédos szó (37), jellemzően egy héber
előtag, névelő vagy elöljáró hozzákötése a szóhoz a szabályok ellenére. A független összevetés 34 eltéréséből
5 maradt a párosítás hibája; ezeket és a többi megerősített hibát az adatkészlet név szerint felsorolja.

## 4. Az adatkészlet

**Hely és azonosító.** Zenodo, DOI: 10.5281/zenodo.24141884; licenc: CC BY 4.0; nyelv: magyar (adat), magyar és angol (dokumentáció);
adatállapot: 2026-11-01.

**Fájlok.** `parok/` (könyvenként, kapcsolatonként egy sor: vers, a magyar szó sorszáma és alakja, az eredeti szó
sorszáma, Strong-szám, kapcsolattípus, bizonyosság, állapot, Textus Receptus-jelölés); `szavak/` (könyvenként minden
magyar és eredeti szó egyszer, állapottal: párosított, betoldás, fordítatlan, függőben); `versek.tsv` (a Károli 1908
szövege); `meres.tsv` (a mérés minden száma); kétnyelvű kódkönyv, módszertani leírás, ismert hibák, ellenőrző összeg. A
kulcs az OSIS-versazonosító és a szó sorszáma. A héber és görög szóalak nincs a csomagban: a sorszám a STEPBible
TAHOT/TAGNT szövegéhez illeszthető.

**Méret.** 66 könyv, 31 158 vers, 598 715 pár (466 785 héber, 131 930 görög; ebből 157 163 morféma),
109 914 betoldás, 63 017 fordítatlan eredeti szó, 794 függőben lévő magyar szó
(45 vers).

## 5. Újrahasznosítás

Az adatkészlet bibliaolvasó és -tanulmányozó alkalmazásoknak Strong-alapú keresést ad a magyar szövegen: egy héber vagy
görög szó minden Károli-megfelelője egy szűréssel összegyűjthető. Fordítástörténeti kutatásban vizsgálható a Károli
fordítói következetessége, a betoldások és a fordítatlan szavak eloszlása. Nyelvtechnológiai célra kis erőforrású
nyelvpár (magyar–héber, magyar–görög) szóillesztési adata, rétegenként mért hibával; a mintapárok és a hibatípusok
szóillesztő programok értékeléséhez is használhatók. Ugyanezek a párok a Károli modernizált szövegén is megjelennek
(https://doi.org/10.5281/zenodo.24141950); a két adatkészlet a vers és a szósorszám kulcsán szóról szóra összekapcsolható.

## 6. Korlátok és a következő kiadás

A párosítás gépi javaslat. A vak ellenőr maga is modell; a független összevetés csak a fő szavakat méri, és kis
klaszter-mintán; a héber morfémák párjainak (157 163 pár) pontossága (90,74%) csak a vak ellenőrrel mért. Mózes két
könyvén kívül minden pár egy modell javaslata. A Károli a Textus Receptust fordította, a párosítás alapja a TAGNT:
369 párosított görög szó nem szerepel a Textus Receptusban, és jelölve van.

A közlés szerkesztői döntés: a párosítás azért jelenik meg nyílt adatként, mert a pontossága mérve és dokumentálva
van — rétegenként és kapcsolattípusonként, konfidencia-intervallummal, hibatípusokkal. Nem egy előre kitűzött küszöb
teljesülésén alapul. A 2. kiadás javítja a megerősített hibákat és a szomszédos szó szabályellenes eseteit, majd
ugyanazzal a protokollal újra mér. Minőségi célját előre rögzítettük: a független fő-szó egyezés alsó széle legalább 98%,
a vak ellenőrrel mért súlyozott egyezés alsó széle legalább 93%, és egyetlen réteg sem 90% alatti.

## Nyilatkozat a mesterséges intelligencia használatáról

A párosítást nyelvi modellek (Claude Sonnet, Gemini Flash), a vak ellenőrzést egy harmadik modell (Claude Opus) végezte,
a fent leírt módon; a modellek Strong-számot nem írtak. A szavakra bontás, a gépi kapu, a táblák összeállítása és a
statisztika determinisztikus program. A kézirat szövegét a claude-opus-5-5 modell fogalmazta az adatkészlet adataiból;
a számok az adatokból generáltak. MI-eszköz nem szerző; az adatokért és a szövegért a szerző felel.

## Hivatkozások

Demeter, T. (2026). *Modernizált Károli – Strong* [adatkészlet]. Zenodo. https://doi.org/10.5281/zenodo.24141950

STEPBible. (é. n.). *Translators Amalgamated Hebrew OT (TAHOT) és Translators Amalgamated Greek NT (TAGNT)*
[adatkészlet]. Tyndale House, Cambridge. https://www.STEPBible.org

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi rész a beküldött változatból kivehető. -->

---

## Csatornajavaslat

A kézirat data paper-alakban készült (áttekintés, módszer, adatkészlet, újrahasznosítás). Két csatornatípus illik hozzá.
Az egyik egy bölcsészeti adatközlő folyóirat (például a Journal of Open Humanities Data), amelynek kimondott data
paper-típusa és MI-nyilatkozati helye van, de a terjedelme 1000–1500 szó, ezért a 2. és a 3. szakasz rövidítendő. A
másik egy nyelvi erőforrásokat közlő hely, ahol a szóillesztés kis erőforrású nyelvpárként és mért hibájú adatként kap
közönséget. Díjmentes alternatíva a nyílt adatkészletekről rövid cikket fogadó adatbányászati és digitális bölcsészeti
folyóirat. A Zenodo-letét mindhárom út előfeltétele; ugyanaz a kézirat egyszerre csak egy helyre küldhető.
