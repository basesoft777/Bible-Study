<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, nem része a nyilt_karoli_strong/ csomagnak. -->
# A Károli-biblia 1908-as szövegének szavankénti párosítása a héber és görög eredetivel: nyílt adatkészlet mért pontossággal

*Data paper · kézirat-tervezet a Journal of Open Humanities Data számára · az adatkészlet DOI-ja: 10.5281/zenodo.24141883*

**Demeter Tamás**, független kutató · ORCID: https://orcid.org/0009-0005-9254-9731 · levelező szerző: [e-mail-cím]

## Kivonat

Az adatkészlet a Károli-biblia, a klasszikus magyar fordítás 1908-as szövegének 599 367 szavát kapcsolja a héber és
görög eredetihez (STEPBible TAHOT/TAGNT) 598 715 szópárral, minden párt az eredeti szó Strong-számával. Írott szabályok
szerint egy nyelvi modell csak szósorszámokat jelölt; a Strong-szám az eredeti szöveg adatából jön. A pontosságot
rétegzett véletlen mintán egy vak modell-ellenőr (95,06%, 95%-os KI: 93,81–96,32%), egy független,
Strong-számos Károli-kiadás a fő szavakon (98,72%) és két emberi ellenőr ([pontosság]) mérte. A TSV-táblák (CC BY 4.0)
Strong-alapú keresést, fordítástörténeti és szóillesztési kutatást szolgálnak.

**Kulcsszavak:** Károli-biblia; Strong-számok; szóillesztés; magyar; bibliai héber; koiné görög

**Szerzői szerepek (CRediT):** Demeter Tamás: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Áttekintés

### A tárhely helye

https://doi.org/10.5281/zenodo.24141883 (concept DOI: mindig a legfrissebb változatra mutat; jelenleg 1.0).

### Háttér

Az adatkészlet a Logosz-lexikon nevű, a szerző által vezetett független kutatási projektben készült. A Károli-fordítás négy évszázada a magyar
protestáns bibliaolvasás alapszövege. A Strong-számok (Strong, 1890) egy fordítás szavait a héber és görög szókincshez
kötik. Strong-számos Károli-kiadás létezik; az itt közölt párosítás nyílt licencű, szavanként dokumentált, és a
pontossága mért.

Az adatkészlet versenként rögzíti, melyik magyar szó melyik eredeti szót adja vissza, mely magyar szó betoldás, és mely
eredeti szó marad fordítatlan. A kapcsolat lehet egy–több és több–egy: az *Azután* a *ʾaḥărê kēn* kettőst fedi
(Józs 8:34), a *meg van írva* egyetlen *kātûb* alakot ad vissza (1Kir 2:3).

## 2. Módszer

### Lépések

**Szövegek és szavakra bontás.** A magyar oldal a Károli 1908 közkincs szövege, az eredeti oldal a STEPBible TAHOT
(héber és arámi Ószövetség) és TAGNT (görög Újszövetség) adata (Tyndale House, Cambridge; CC BY 4.0, forrásmegjelöléssel
használva). A TAHOT a héber előtagokat és ragokat külön szóként kezeli (H9001–H9049), ezért egy magyar szóhoz gyakran
több eredeti „szó” tartozik. A Károli versbeosztását determinisztikus vershossz-igazítással feleltettük meg az
eredetiének; két vers minden egybeolvadását kézzel hagytuk jóvá.

**Párosítás.** Egy nyelvi modell (Claude Sonnet) versenként két számozott szólistát kapott: a Károli szavait, és az
eredeti szavakat alakkal, Strong-számmal és a TAHOT/TAGNT rövid angol glosszájával; a Strong-szám csak tájékoztatásul
állt ott, a válaszban tilos volt. A rögzített utasítás egy kidolgozott példában egy választható, Strong-címkés
KJV-sort is mutatott; versbemenet ilyet nem tartalmazott. A modell csak sorszámpárokat adott vissza, a betoldásokkal és a fordítatlan szavakkal.
Az 1Móz 1:1-ben például a *teremté* (2) szót a 3. eredeti szóval (*bārāʾ*), a *Kezdetben* (1) szót az 1–2. szóval
(*bə-*, *rēʾšît*) párosította, a tárgyjelölő *ʾēt* (5) szót fordítatlannak jelölte; a H1254, H9003 és H7225 számot
ezután program tette hozzá a sorszám alapján. A vitás eseteket tizenkét írott szabály döntötte el. A funkciószavakra
rögzített konvenció érvényes: a magyar névelő és az eredeti szó nélküli segédige betoldás, a héber és görög névelő
fordítatlan, mert a névelőhasználat a nyelvek között nem felel meg egy az egyben; a névmásként álló névelő párosított.
Minden választ program ellenőrzött (minden magyar szó pontosan egyszer, minden eredeti szó legalább
egyszer, csak létező sorszám); a bukott választ a modell újra elkészítette. A modell így nem tudott Strong-számot vagy
szótári tételt kitalálni: legfeljebb rossz szót párosíthatott. Minden pár egy konkrét eredeti szóra mutat, ezért
ellenőrizhető, és az emberi validáció ezt nézi; a jelentés és a Strong-szám forrása a nyílt, szakmai forrásadat, nem a
modell. A táblák a mentett modellválaszokból determinisztikus programokkal (Python) bájtra azonosan újraépíthetők.

### Mintavétel

A vak ellenőrzés mintája rétegzett véletlen minta: a párkészletet könyvcsoportonként hét rétegre osztottuk
(Mózes öt könyve; történeti, költői és prófétai könyvek; evangéliumok és ApCsel; levelek; Jelenések), rétegenként
200 párral (Mózes öt könyvéből 400 párral, két részmintában, pársúllyal összegezve). A független
összevetés klaszter-minta: rétegenként egy, Mózes öt könyvében két teljes fejezet (nyolc fejezet, 2 663
fő szó párja).

### Minőség-ellenőrzés

**Vak modell-ellenőrzés és kalibráció.** Egy második modell (Claude Opus) a cél magyar szóhoz maga jelölte ki az eredeti
szavakat, ugyanazokkal a szabályokkal, a gépi pár ismerete nélkül. Egy korábbi, kézzel összeállított mintán az ellenőr
96,79%-ban, a gépi párosítás 97,06%-ban egyezett a mintával: az ellenőr nem pontosabb a párosításnál, ezért az
egyezés csak akkor alsó becslés, ha a közös hiba elhanyagolható.

**Független összevetés.** A közös hibát egy Strong-számokkal jelölt Károli-kiadás méri; a forrás magyar szavanként
egy fő Strong-számot jelöl, ezért csak az a pár számít, ugyanannak a szónak a további párjai (morféma, többszavas
kapcsolat) nem hiba. Az eltéréseket háromutasan (gépi pár, forrás, vak ellenőr) ítéltük meg. Csak az
összesített arány nyilvános, a külső forrás adata nem.

**Emberi validáció.** Két független emberi ellenőr, végzett teológus, bibliai héber és görög ismerettel, egymástól
függetlenül ítélt meg egy rétegzett véletlen mintát ([N] pár, valamint párosítatlan szavak); a párosítatlan szavak
mintájából a szabály által meghatározott funkciószavak kimaradtak. Az ítéletük szerinti pontosság [pontosság] (95%-os KI:
[KI]); a két ellenőr egyezése Cohen-féle kappa = [kappa]; az egyezésük a vak modell-ellenőrrel [egyezés a
modell-ellenőrrel].

| mérés | becslés | 95%-os KI |
|---|---|---|
| teljes párkészlet, vak ellenőr, súlyozott | 95,06% | 93,81–96,32% |
| ebből Ószövetség / Újszövetség | 94,50% / 97,07% | 92,95–96,05% / 95,55–98,59% |
| tartalmi szó / héber morféma | 96,44% / 90,74% | 95,20–97,69% / 87,18–94,29% |
| fő szavak, a független forrás szerint | 98,72% | 98,22–99,08% |
| fő szavak, háromutas ítélet után | 99,81% | 99,56–99,92% |
| emberi validáció | [pontosság] | [KI] |

A rétegek egyezése 93,00% (próféták) és 98,00% (evangéliumok és Apostolok cselekedetei) között mozog (rétegenként: `data/meres.tsv`).
Az 1 600 mintapárból 72 tért el az ellenőrtől; a leggyakoribb típus a szomszédos szó (37),
jellemzően egy héber előtag, névelő vagy elöljáró hozzákötése a szóhoz a szabályok ellenére. A független összevetés
34 eltéréséből öt maradt a párosítás hibája; minden megerősített hibát az adatkészlet
felsorol.

## 3. Az adatkészlet leírása

- **Tárhely neve:** Zenodo
- **Objektum neve:** `karoli-1908-strongs-1.0.zip` (Logosz Lexikon – Károli Bible (1908): Word Alignment with Hebrew and Greek Strong's
  Numbers, változat: 1.0)
- **Formátumok és változatok:** TSV (UTF-8, tabulátorral tagolt, LF sorvég) az adathoz és a gépi kódkönyvhöz; Markdown a kétnyelvű
  dokumentációhoz (kódkönyv, módszertani leírás, ismert hibák); CFF hivatkozási fájl; SHA-256 ellenőrző összeg
- **Létrehozás dátumai:** 2026-10-01 – 2026-11-01
- **Az adatkészlet készítője:** Demeter Tamás (független kutató; ORCID: 0009-0005-9254-9731): szabályok, feldolgozási lánc, mérés,
  gondozás. Az eredeti oldal szavai és Strong-számai a STEPBible adatából valók (Tyndale House, Cambridge).
- **Nyelv:** magyar (szóalakok, oszlopnevek és kódok); magyar és angol (dokumentáció, kétnyelvű kódkönyv)
- **Licenc:** CC BY 4.0
- **Közzététel dátuma:** 2026-11-15

**Tartalom.** `data/parok/` (könyvenként, kapcsolatonként egy sor: sorszámok, magyar alak, Strong-szám,
kapcsolattípus, állapot, Textus Receptus-jelölés); `data/szavak/` (könyvenként minden szó egyszer, állapottal:
párosított, betoldás, fordítatlan, függőben); `data/versek.tsv` (a Károli 1908
szövege); `data/meres.tsv` (a mérés minden száma). A kulcs az OSIS-versazonosító és a szó sorszáma. A héber és görög
szóalak nincs a csomagban: a sorszám a STEPBible TAHOT/TAGNT szövegéhez illeszthető.

**Méret.** 66 könyv, 31 158 vers, 598 715 pár (466 785 héber, 131 930 görög; ebből 157 163 morféma),
109 914 betoldás, 63 017 fordítatlan eredeti szó, 794 függőben lévő magyar szó
(45 vers).

## 4. Újrahasznosítási lehetőségek

Bibliaprogramok Strong-alapú keresést kínálhatnak a magyar szövegen: egy eredeti szó minden Károli-megfelelője egy
szűréssel előáll. Fordítástörténeti kutatásban vizsgálható a Károli
fordítói következetessége, a betoldások és a fordítatlan szavak eloszlása. Nyelvtechnológiai célra kis erőforrású
nyelvpár (magyar–héber, magyar–görög) szóillesztési adata, rétegenként mért hibával; a mintapárok és a hibatípusok
szóillesztő programok értékeléséhez is használhatók. A párosításra a Logosz-lexikon, egy motívum-indexelt, kereszthivatkozott
bibliai lexikon épül.

Kísérő adatkészlet: ugyanezek a párok a Károli modernizált szövegén (Demeter, 2026b). A modernizálás a szerző saját
munkája: csak a helyesírást és az igealakokat változtatja, szabályok szerint; a ritka igealakoknál nyelvi modellek
javasoltak, és egy alak csak akkor változott, ha független javaslatok egyeztek, és a tőellenőrzés átengedte; az
eredményt független ellenőrzés vizsgálta. Minden szó a helyén maradt, így a két adatkészlet a vers és a szósorszám
kulcsán szóról szóra összekapcsolható.

Korlátok. A párosítás gépi javaslat. A vak ellenőr maga is modell; a független összevetés csak a fő szavakat méri, kis
klaszter-mintán; a héber morfémák párjainak (157 163 pár) pontosságát a külső forrás nem méri. A Károli a Textus
Receptust fordította, a párosítás alapja a TAGNT: 369 párosított görög szó nem szerepel a Textus Receptusban,
és jelölve van. A 2. kiadás javítja a megerősített hibákat, majd ugyanazzal a protokollal újra mér, a módszertani
leírásban előre rögzített minőségi célokhoz mérten.

## Adat-elérhetőség

Az adatkészlet és a kísérő adatkészlet nyíltan elérhető a Zenodón, CC BY 4.0 licenccel: https://doi.org/10.5281/zenodo.24141883,
https://doi.org/10.5281/zenodo.24141949.

## Köszönetnyilvánítás

A szerző köszöni [1. emberi ellenőr neve] és [2. emberi ellenőr neve] munkáját az emberi validációban.

## Finanszírozás

A munka külső finanszírozás nélkül készült.

## Érdekütközés

A szerzőnek nincs bejelentendő érdekütközése.

## Hivatkozások

Demeter, T. (2026a). *Logosz Lexikon – Károli Bible (1908): Word alignment with Hebrew and Greek Strong's numbers*
(változat: 1.0) [adatkészlet]. Zenodo. https://doi.org/10.5281/zenodo.24141883

Demeter, T. (2026b). *Logosz Lexikon – Modernized Károli Bible: Word alignment with Hebrew and Greek Strong's numbers*
(változat: 1.0) [adatkészlet]. Zenodo. https://doi.org/10.5281/zenodo.24141949

STEPBible. (é. n.). *Translators Amalgamated Hebrew OT (TAHOT) és Translators Amalgamated Greek NT (TAGNT)*
[adatkészlet]. Tyndale House, Cambridge. https://www.STEPBible.org

Strong, J. (1890). *The exhaustive concordance of the Bible*. Hunt & Eaton.

## Nyilatkozat a mesterséges intelligencia használatáról

Generatív MI három helyen dolgozott. (1) Párosítás: egy nyelvi modell (Claude Sonnet, Anthropic; a kötegelt futások
naplója szerint claude-sonnet-5-5) csak sorszámpárokat adott vissza (l. Módszer); Strong-számot nem írhatott, azt a
sorszám alapján a TAHOT/TAGNT adja, és minden pár egy eredeti szóra mutat. Az 1Móz és a 2Móz párosításánál egy másik
nyelvi modell is futott keresztellenőrzésként; egyetlen közölt pár sem csak tőle származik. (2) Minőség-ellenőrzés: a Claude Opus a mintán vak ellenőr volt; az emberi validáció ítéleteit emberek hozták, MI nélkül. (3) Kísérő adatkészlet: nyelvi modellek csak a
ritka igealakokra tettek javaslatot (l. Újrahasznosítás). Minden más feldolgozás determinisztikus. A
kézirat szövegének megfogalmazásában és szerkesztésében a claude-opus-5-5 modell segített, az adatkészlet adataiból; a
számok az adatokból generáltak. A kutatást a szerző tervezte, minden szerkesztői döntést ő hozott, minden állítást az
adatokon ellenőrzött, és a tartalomért teljes felelősséget vállal; MI-eszköz nem szerző.

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi rész a beküldött változatból kivehető. -->

---

## Beküldési jegyzet

Szószám (a beküldési szöveg angol változatában): az 1–4. szakasz, a cím, a szerzői sor, a kivonat, a táblázat és a
hivatkozások nélkül (a JOHD-sablon számítása) 1 227; a számozatlan nyilatkozatokkal 1 423; a
hivatkozásokkal is 1 497 (a beküldési oldal szerint a korlát a hivatkozásokat is tartalmazza; a kivonatról nem
szól); a kivonattal együtt 1 602. A JOHD data paper terjedelme 1000–1500 szó; a szerkesztőség megerősítheti, melyik
számítás érvényes.

Beküldés előtt kitöltendő: az emberi validáció mezői ([N], pontosság, KI, kappa, egyezés a modell-ellenőrrel), a
levelező szerző e-mail-címe, a két ellenőr neve. A szöveg a JOHD hivatalos Word- vagy LaTeX-sablonjába kerül; a
kísérőlevél: `kozlemeny/data_paper/johd_cover_letter_en.md`.
