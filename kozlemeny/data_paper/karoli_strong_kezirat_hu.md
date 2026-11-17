<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, nem része a nyilt_karoli_strong/ csomagnak. -->
# A Károli-biblia 1908-as szövegének szavankénti párosítása a héber és görög eredetivel: nyílt adatkészlet mért pontossággal

*Data paper · kézirat-tervezet a Journal of Open Humanities Data számára · az adatkészlet DOI-ja: 10.5281/zenodo.24141883*

**Demeter Tamás**, független kutató · ORCID: https://orcid.org/0009-0005-9254-9731 · levelező szerző: [e-mail-cím]

## Kivonat

Az adatkészlet a Károli-biblia, a klasszikus magyar fordítás 1908-as szövegének 599 367 szavát kapcsolja a héber és
görög eredetihez (STEPBible TAHOT/TAGNT) 598 715 szópárral, mindegyik az eredeti szó Strong-számával. Egy nyelvi modell
csak szósorszámokat jelölt; a Strong-szám az eredeti szöveg adatából jön. A pontosság rétegzett véletlen mintán,
vak modell-ellenőrrel 95,06% (95%-os KI: 93,81–96,32%), két emberi ellenőr szerint [pontosság]; a fő
szavak egyezése egy független, zárt Strong-számos kiadással 98,72%. A CC BY 4.0 licencű táblák Strong-alapú keresést
és szóillesztési kutatást szolgálnak.

**Kulcsszavak:** Károli-biblia; Strong-számok; szóillesztés; magyar; bibliai héber; koiné görög

**Szerzői szerepek (CRediT):** Demeter Tamás: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Áttekintés

### A tárhely helye

https://doi.org/10.5281/zenodo.24141883 (concept DOI; jelenlegi változat: 1.0).

### Háttér

Az adatkészlet a Logosz-lexikon nevű, a szerző által vezetett független kutatási projektben készült. A Károli-fordítás négy
évszázada a magyar protestáns bibliaolvasás alapszövege. A Strong-számok (Strong, 1890) egy fordítás szavait a héber és
görög szókincshez kötik. Strong-számos Károli-kiadás létezik; ez a párosítás nyílt licencű, szavanként dokumentált, és
a pontossága mért.

Az adatkészlet versenként rögzíti, melyik magyar szó melyik eredeti szót adja vissza, mely magyar szó betoldás, és mely
eredeti szó marad fordítatlan. A kapcsolat lehet egy–több és több–egy: az *Azután* a *ʾaḥărê kēn* kettőst fedi
(Józs 8:34), a *meg van írva* egyetlen *kātûb* alakot ad vissza (1Kir 2:3).

## 2. Módszer

### Lépések

**Szövegek és szavakra bontás.** A magyar oldal a Károli 1908 közkincs szövege, az eredeti oldal a STEPBible TAHOT
(héber és arámi Ószövetség) és TAGNT (görög Újszövetség) adata (Tyndale House, Cambridge; CC BY 4.0). A TAHOT a héber
előtagokat és ragokat külön szóként számolja (H9001–H9049). A Károli versbeosztását determinisztikus
vershossz-igazítással feleltettük meg az eredetiének; minden vers-egybeolvadást kézzel hagytunk jóvá.

**Párosítás.** Egy nyelvi modell (Claude Sonnet) versenként két számozott szólistát kapott: a Károli szavait, és az
eredeti szavakat alakkal, Strong-számmal és a TAHOT/TAGNT rövid angol glosszájával; a Strong-szám csak tájékoztatásul
állt ott, a válaszban tilos volt. A rögzített utasítás egy kidolgozott példában egy választható, Strong-címkés
KJV-sort is mutatott; versbemenet ilyet nem tartalmazott. A modell csak sorszámpárokat adott vissza, a betoldásokkal és
a fordítatlan szavakkal. Az 1Móz 1:1-ben például a *teremté* (2) szót a 3. eredeti szóval (*bārāʾ*), a *Kezdetben* (1)
szót az 1–2. szóval (*bə-*, *rēʾšît*) párosította, a tárgyjelölő *ʾēt* (5) szót fordítatlannak jelölte; a H1254, H9003
és H7225 számot ezután program tette hozzá a sorszám alapján. A vitás eseteket tizenkét írott szabály döntötte el. A
funkciószavakra rögzített konvenció érvényes: a magyar névelő és az eredeti szó nélküli segédige betoldás, a héber és
görög névelő fordítatlan, mert a névelőhasználat a nyelvek között nem felel meg egy az egyben; a névmásként álló
névelő párosított. Minden választ program ellenőrzött (minden magyar szó pontosan egyszer, minden eredeti szó legalább
egyszer, csak létező sorszám); a bukott választ a modell újra elkészítette. A modell így nem tudott Strong-számot vagy
szótári tételt kitalálni; legfeljebb rossz szót párosíthatott, és minden pár egy eredeti szóra mutat, amelyet az
emberi validáció ellenőriz. A jelentés és a Strong-szám forrása a nyílt, szakmai forrásadat. A modellválaszok egyszer
készültek, és archiválva vannak; a párok építése, a Strong-szám hozzárendelése és az érvényességi kapu determinisztikus,
ezért a táblák az archivált válaszokból bájtra azonosan újraépíthetők, a modell újrafuttatása viszont kis eltéréseket
adhat.

### Mintavétel

A vak ellenőrzés mintája rétegzett véletlen minta: a párkészletet könyvcsoportonként hét rétegre osztottuk
(Mózes öt könyve; történeti, költői és prófétai könyvek; evangéliumok és ApCsel; levelek; Jelenések), rétegenként
200 párral (Mózes öt könyvéből 400 párral, két részmintában, pársúllyal összegezve). A zárt
kiadással való keresztellenőrzés klaszter-mintán futott: rétegenként egy, Mózes öt könyvében két teljes fejezet (nyolc fejezet, 2 663
fő szó párja).

### Minőség-ellenőrzés

**Vak modell-ellenőrzés és kalibráció.** Egy második modell (Claude Opus) a mintába került magyar szóhoz maga jelölte
ki az eredeti szavakat, ugyanazokkal a szabályokkal, a gépi pár ismerete nélkül. Egy korábbi, kézi mintán az ellenőr
96,79%-ban, a gépi párosítás 97,06%-ban egyezett; mivel az ellenőr nem pontosabb a párosításnál, az egyezés
csak akkor alsó becslés, ha a közös hiba elhanyagolható.

**Keresztellenőrzés zárt kiadással.** A közös hiba kiegészítő ellenőrzésére a fő szavak párjait helyben összevetettük
egy független, zárt licencű, Strong-számos Károli-kiadással; a forrás nem terjeszthető és az olvasó számára nem
ellenőrizhető, ezért csak az összesített egyezés nyilvános. A kiadás magyar szavanként egy fő Strong-számot jelöl, és
csak ez a pár kerül összevetésre. Az eltérés nem feltétlenül párosítási hiba, mert a felbontás eltérhet (*ʾaḥărê
kēn*); az eltéréseket háromutasan (gépi pár, zárt forrás, vak ellenőr) ítéltük meg.

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
| emberi validáció | [pontosság] | [KI] |
| a fő szavak egyezése a zárt kiadással | 98,72% | 98,22–99,08% |
| ugyanez háromutas ítélet után | 99,81% | 99,56–99,92% |

A rétegek egyezése 93,00% (próféták) és 98,00% (evangéliumok és Apostolok cselekedetei) között mozog.
Az 1 600 mintapárból 72 tért el az ellenőrtől, leggyakrabban szomszédos szóval (37): jellemzően
egy héber előtag, névelő vagy elöljáró szabályellenes hozzákötésével. A zárt kiadástól való 34 eltérésből
öt bizonyult párosítási hibának; minden megerősített hibát az adatkészlet felsorol.

## 3. Az adatkészlet leírása

- **Tárhely neve:** Zenodo
- **Objektum neve:** `karoli-1908-strongs-1.0.zip`
- **Formátumok és változatok:** TSV (UTF-8, tabulátorral tagolt, LF sorvég) az adathoz és a gépi kódkönyvhöz;
  Markdown a kétnyelvű dokumentációhoz; CFF hivatkozási fájl; SHA-256
  ellenőrző összeg
- **Létrehozás dátumai:** 2026-10-01 – 2026-11-01
- **Az adatkészlet készítője:** Demeter Tamás (független kutató; ORCID: 0009-0005-9254-9731): szabályok, feldolgozási lánc, mérés,
  gondozás. Az eredeti oldal szavai és Strong-számai: STEPBible (Tyndale House, Cambridge).
- **Nyelv:** magyar (szóalakok, oszlopnevek és kódok); magyar és angol (dokumentáció, kétnyelvű kódkönyv)
- **Licenc:** CC BY 4.0
- **Közzététel dátuma:** 2026-11-15

**Tartalom.** `data/parok/` (könyvenként, kapcsolatonként egy sor: sorszámok, magyar alak, Strong-szám,
kapcsolattípus, állapot, Textus Receptus-jelölés); `data/szavak/` (könyvenként minden szó egyszer, állapottal:
párosított, betoldás, fordítatlan, függőben); `data/versek.tsv` (a Károli 1908 szövege); `data/meres.tsv` (a mérés
minden száma). A kulcs az OSIS-versazonosító és a szó sorszáma. Az eredeti szóalak nincs a csomagban; a sorszám a
STEPBible szövegéhez illeszthető.

**Méret.** 66 könyv, 31 158 vers, 598 715 pár (466 785 héber, 131 930 görög; ebből 157 163 morféma),
109 914 betoldás, 63 017 fordítatlan eredeti szó, 794 függőben lévő magyar szó
(45 vers).

## 4. Újrahasznosítási lehetőségek

Bibliaprogramok Strong-alapú keresést kínálhatnak a magyar szövegen. A fordítástörténet vizsgálhatja a Károli következetességét, betoldásait és fordítatlan szavait.
Nyelvtechnológiai célra kis erőforrású nyelvpár (magyar–héber, magyar–görög) szóillesztési adata, rétegenként mért
hibával; a mintapárok szóillesztő programok értékeléséhez is használhatók. A párosításra a Logosz-lexikon,
egy motívum-indexelt, kereszthivatkozott bibliai lexikon épül.

Kísérő adatkészlet: ugyanezek a párok a Károli modernizált szövegén (Demeter, 2026b). A modernizálás, a szerző saját
munkája, csak a helyesírást és az igealakokat változtatja, szabályok szerint; a ritka igealakoknál nyelvi modellek
javasoltak változást, amely csak egyező független javaslatok és tőellenőrzés után lépett életbe. Minden szó a helyén
maradt, az összeolvadt szavak (*a kik* → *akik*) mindkét párja megmaradt, így a párkészlet azonos, és a fenti
pontossági számok rá is érvényesek; a modernizálást külön ellenőrzés és mérés vizsgálta.

Korlátok. A párosítás gépi javaslat, és a vak ellenőr maga is modell. A zárt kiadással való keresztellenőrzés kis
klaszter-minta, a 157 163 héber morféma-pár nélkül. A Károli a Textus Receptust fordította, a
párosítás alapja a TAGNT; a Textus Receptusban nem szereplő 369 párosított görög szó jelölve van. A 2. kiadás
javítja a megerősített hibákat, és előre rögzített minőségi célokhoz mérten újra mér.

## Adat-elérhetőség

Mindkét adatkészlet nyíltan elérhető a Zenodón, CC BY 4.0 licenccel: https://doi.org/10.5281/zenodo.24141883,
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

(1) Párosítás: a Claude Sonnet (Anthropic; a kötegelt futások naplója szerint
claude-sonnet-5-5) csak sorszámpárokat adott vissza (l. Módszer). Az 1Móz és a 2Móz párosításánál egy másik nyelvi
modell is futott keresztellenőrzésként; egyetlen közölt pár sem csak tőle származik. (2) Minőség-ellenőrzés: a Claude
Opus a mintán vak ellenőr volt; az emberi validáció MI nélkül készült. (3) Kísérő adatkészlet: nyelvi modellek csak a
ritka igealakokra tettek javaslatot (l. Újrahasznosítás). A kézirat
szövegének megfogalmazásában és szerkesztésében a claude-opus-5-5 modell segített, az adatkészlet adataiból; a számok
az adatokból generáltak. A kutatást a szerző tervezte, minden szerkesztői döntést ő hozott, minden állítást az adatokon
ellenőrzött, és a tartalomért teljes felelősséget vállal; MI-eszköz nem szerző.

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi rész a beküldött változatból kivehető. -->

---

## Beküldési jegyzet

Szószám (a beküldési szöveg angol változatában): az 1–4. szakasz, a cím, a szerzői sor, a kivonat, a táblázat és a
hivatkozások nélkül (a JOHD-sablon számítása) 1 173; a számozatlan nyilatkozatokkal 1 332; a
hivatkozásokkal is 1 406 (a beküldési oldal szerint a korlát a hivatkozásokat is tartalmazza; a kivonatról nem
szól); a kivonattal együtt 1 499. A JOHD data paper terjedelme 1000–1500 szó; a szerkesztőség megerősítheti, melyik
számítás érvényes.

Beküldés előtt kitöltendő: az emberi validáció mezői ([N], pontosság, KI, kappa, egyezés a modell-ellenőrrel), a
levelező szerző e-mail-címe, a két ellenőr neve. A szöveg a JOHD hivatalos Word- vagy LaTeX-sablonjába kerül; a
kísérőlevél: `kozlemeny/data_paper/johd_cover_letter_en.md`.
