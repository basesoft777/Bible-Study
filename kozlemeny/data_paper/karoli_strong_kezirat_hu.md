<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, nem része a nyilt_karoli_strong/ csomagnak. -->
# A Károli-biblia 1908-as szövegének szavankénti párosítása a héber és görög eredetivel: nyílt adatkészlet mért párprecizitással

*Data paper · kézirat-tervezet a Journal of Open Humanities Data számára · az adatkészlet DOI-ja: 10.5281/zenodo.24141883*

**Demeter Tamás**, független kutató · ORCID: https://orcid.org/0009-0005-9254-9731 · levelező szerző: [e-mail-cím]

## Kivonat

Az adatkészlet a Károli-biblia, a klasszikus magyar fordítás 1908-as szövegének 599 367 szavát kapcsolja a héber és
görög eredetihez (STEPBible TAHOT/TAGNT) 598 715 párral, mindegyik az eredeti szó Strong-számával; egy nyelvi modell csak
szósorszámokat jelölt. A párprecizitás (egyezés egy vak modell-ellenőrrel) rétegzett mintán 95,06% (95%-os KI:
93,81–96,32%); az emberi validáció szerint [precizitás]. A CC BY 4.0 licencű táblák Strong-alapú keresést szolgálnak.

**Kulcsszavak:** Károli-biblia; Strong-számok; szóillesztés; magyar; bibliai héber; koiné görög

**Szerzői szerepek (CRediT):** Demeter Tamás: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Áttekintés

### A tárhely helye

https://doi.org/10.5281/zenodo.24141883 (concept DOI; jelenlegi változat: 1.0).

### Háttér

Az adatkészlet a szerző független kutatási projektjéből, a Logosz-lexikonból származik. A Strong-számok (Strong, 1890) egy
fordítás szavait a héber és görög szókincshez kötik. A Károli-szövegnek, amely négy évszázada a magyar protestáns
bibliaolvasás alapszövege, léteznek Strong-számos kiadásai; ez a párosítás nyílt licencű, szavanként dokumentált, és a
precizitása mért. Versenként rögzíti, melyik magyar szó melyik eredeti szót adja vissza (egy–több és több–egy
kapcsolattal is), a betoldásokat és a fordítatlan eredeti szavakat.

## 2. Módszer

### Lépések

**Szövegek.** A magyar oldal a Károli 1908 közkincs szövege (HunKar), az eredeti oldal a STEPBible TAHOT (héber és
arámi Ószövetség) és TAGNT (görög Újszövetség) adata (Tyndale House, Cambridge; CC BY 4.0; commit efe428a, letöltve 2026-08-24). A
TAHOT a héber előtagokat és ragokat külön szóként számolja (H9001–H9049). A versbeosztásokat determinisztikus
vershossz-igazítás feleltette meg egymásnak; minden vers-egybeolvadást kézzel hagytunk jóvá.

**Párosítás.** Egy nyelvi modell versenként két számozott szólistát kapott: a Károli szavait, és az eredeti szavakat
alakkal, Strong-számmal és rövid angol glosszával; a Strong-szám csak tájékoztatásul állt ott, a válaszban tilos volt. A
rögzített utasítás egy kidolgozott példában egy választható, Strong-címkés KJV-sort is mutatott; versbemenet ilyet nem
tartalmazott. A modell sorszámpárokat, betoldásokat és fordítatlan szavakat adott vissza. A Strong-számot ezután program tette
hozzá a sorszám alapján. A vitás eseteket tizenkét írott szabály döntötte el. A
funkciószavakra rögzített konvenció érvényes: a magyar névelő és az eredeti szó nélküli segédige betoldás, a héber és
görög névelő fordítatlan (a névelőhasználat a nyelvek között eltér); a névmásként álló névelő párosított.

**Futtatás és megismételhetőség.** Minden könyvet a claude-sonnet-5-5 párosított (a futtatás részletei a
letétben). Minden
választ program ellenőrzött (minden magyar szó pontosan egyszer, minden eredeti szó legalább egyszer, csak létező
sorszám); a bukott választ a modell újra elkészítette. A modell így nem tudott Strong-számot vagy szótári tételt
kitalálni; legfeljebb rossz szót párosíthatott, és minden pár egy ellenőrizhető eredeti szóra mutat. A modellválaszok
egyszer készültek, és archiválva vannak; a párok építése, a Strong-szám hozzárendelése és a kapu determinisztikus, ezért
a táblák a válaszokból bájtra azonosan újraépíthetők, a modell újrafuttatása kis eltérést adhat.

### Mintavétel

A vak ellenőrzéshez a párkészletet könyvcsoportonként hét rétegre osztottuk (Mózes öt könyve; történeti,
költői és prófétai könyvek; evangéliumok és ApCsel; levelek; Jelenések), rétegenként 200 véletlen párral; Mózes
öt könyvében 400 pár két részmintából, pársúllyal összegezve. Az emberi validáció mintája [N] pár és [M] pár
nélküli szó ugyanezekből a rétegekből, és súlyozott túlmintaként az a [87] pár, amelyet bármelyik gépi
ellenőr hibásnak jelölt. A zárt kiadással való keresztellenőrzés nyolc célzottan kiválasztott fejezeten
futott (rétegenként az, amelyben a legtöbb ellenőr-eltérés volt).

### Minőség-ellenőrzés

**Vak modell-ellenőrzés.** Egy második modell (Claude Opus) a mintába került magyar szóhoz maga jelölte ki az eredeti
szavakat, ugyanazokkal a szabályokkal, a gépi pár ismerete nélkül; a pár helyes, ha az eredeti szava az ellenőr
jelölései között van. A párprecizitás tehát egy modellel való egyezés, nem abszolút mérce.

**Emberi validáció.** Egy külső ellenőr, végzett teológus, bibliai héber és görög ismerettel, minden tételt megítélt;
a második ellenőr, szintén végzett teológus, a szerző családtagja; egyikük sem dolgozott az adatkészlet
előállításán. Az ítélet nem vak: az ellenőrök látják a gépi párt. A pár nélküli szavak mintájából a szabály által
meghatározott funkciószavak kimaradtak. A fő szám a külső ellenőré: precizitás [precizitás] (95%-os KI: [KI]), a
bizonytalan tételeket hibának számítva [konzervatív]. A második ellenőr száma ([precizitás 2]) és a kettejük egyezése
(kappa = [kappa]) kiegészítő adat; döntnök nincs. Az egyezés a vak modell-ellenőrrel [egyezés a modell-ellenőrrel].

**Keresztellenőrzés zárt kiadással.** Kiegészítő ellenőrzésként a fő szavak párjait helyben összevetettük a
Bible-Discovery Strong-számos Károlijával (HUN modul), egy zárt licencű kiadással, amelyet az olvasó nem ellenőrizhet;
csak az összesített egyezés nyilvános. A kiadás magyar szavanként egy fő Strong-számot jelöl, a mi felbontásunk
részletesebb, ezért az eltérés nem feltétlenül hiba; a nevezők és az eltérések a letétben állnak.

| mérés | becslés | 95%-os KI |
|---|---|---|
| párprecizitás, vak modell-ellenőr, súlyozott | 95,06% | 93,81–96,32% |
| tartalmi szó / héber morféma | 96,44% / 90,74% | 95,20–97,69% / 87,18–94,29% |
| emberi validáció (külső); a bizonytalan hibaként | [precizitás]; [konzervatív] | [KI] |
| a fő szavak egyezése, zárt kiadás | 98,72% | – |

A rétegek precizitása 93,00% (próféták) és 98,00% (evangéliumok és Apostolok cselekedetei) között mozog.
Az 1 600 mintapárból 72 tért el az ellenőrtől, leggyakrabban szomszédos szóval (37).

## 3. Az adatkészlet leírása

- **Tárhely neve:** Zenodo
- **Objektum neve:** `karoli-1908-strongs-1.0.zip`
- **Formátumok és változatok:** TSV (UTF-8) az adathoz és a kódkönyvhöz;
  Markdown a kétnyelvű dokumentációhoz; CFF hivatkozási fájl; SHA-256 ellenőrző összeg
- **Létrehozás dátumai:** 2026-10-01 – 2026-11-01
- **Az adatkészlet készítője:** Demeter Tamás (független kutató; ORCID: 0009-0005-9254-9731): szabályok, feldolgozási lánc, mérés,
  gondozás.
- **Nyelv:** magyar (adat); magyar és angol (dokumentáció)
- **Licenc:** CC BY 4.0
- **Közzététel dátuma:** 2026-11-15

**Tartalom.** `data/parok/` (kapcsolatonként egy sor: sorszámok, Strong-szám, kapcsolattípus, állapot, Textus
Receptus-jelölés), `data/szavak/` (minden szó egyszer, állapottal: párosított, betoldás, fordítatlan vagy függőben,
azaz még nem párosított), `data/versek.tsv`, `data/meres.tsv` (a mérés minden száma); kulcs: OSIS-vers és szósorszám.

**Méret.** 66 könyv, 31 158 vers, 598 715 pár (466 785 héber, 131 930 görög; ebből 157 163 morféma),
109 914 betoldás, 63 017 fordítatlan eredeti szó, 794 függőben lévő magyar szó
(45 vers).

## 4. Újrahasznosítási lehetőségek

Bibliaprogramok Strong-alapú keresést kínálhatnak a magyar szövegen. A fordítástörténet vizsgálhatja a Károli
következetességét és betoldásait. Nyelvtechnológiai célra kis erőforrású nyelvpár szóillesztési adata, rétegenként
mért hibával. A párosításra a Logosz-lexikon, egy motívum-indexelt, kereszthivatkozott bibliai lexikon épül. Egy kísérő
adatkészlet (Demeter, 2026b) ugyanezeket a párokat, szóról szóra, a szerző által modernizált szövegen adja.

### Korlátok

A vak ellenőr maga is modell, és az emberi validáció nem vak. A párprecizitás a fordítatlan eredeti szavakat nem méri.
Az egyik külső ellenőr ugyanabból a modellcsaládból való, mint az 1–2Mózes keresztellenőrző modellje, ezért ott
nem teljesen független. Az 1–2Mózesben
3 256 pár (1 486 vers), amelyre a második modell (l. MI-nyilatkozat) más párt javasolt, gyengébb: a mintából
12 közül három helyes, így nagyjából 1 500–3 000 lehet hibás; az ismert-hibák lista javítás
nélkül felsorolja őket; az 1.2-es változat újrapárosítja és újra méri őket.
A Textus Receptusban, amelyet Károli fordított, nem szereplő 369 párosított görög szó jelölve van.

## Adat-elérhetőség

Mindkét adatkészlet nyíltan elérhető a Zenodón, CC BY 4.0 licenccel (l. Hivatkozások). Az 1.1-es változat,
amely a beküldés előtt jelenik meg, hozzáadja a promptot (naplózott hash: 84f12ca7aafb), mind a 66 könyv nyers
modellválaszát, a versmegfeleltetést és a vers-összevonásokat, az 1 600 mintapárt az ellenőr ítéletével, az
ismert-hibák listát és az emberi ítéleteket, a STEPBible-commit és a modellazonosító rögzítésével; kódot nem.

## Köszönetnyilvánítás

A szerző köszöni [a külső ellenőr neve] és [a második ellenőr neve] munkáját az emberi validációban.

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

(1) Párosítás: a Claude Sonnet (Anthropic) csak sorszámpárokat adott vissza (l. Módszer). Az 1Móz és a 2Móz
párosításánál egy másik nyelvi modell (Google Gemini) is futott keresztellenőrzésként; egyetlen közölt pár sem csak
tőle származik. (2) Minőség-ellenőrzés: a Claude Opus és két más gyártótól származó ellenőrmodell (Google Gemini,
OpenAI GPT; azonosító, router és dátum a letétben) a mintán vak ellenőr volt; az emberi validáció MI nélkül készült.
(3) Kísérő adatkészlet: nyelvi modellek a ritka igealakokra tettek javaslatot, amely csak egyező független javaslatok
esetén lépett életbe. A kézirat szövegének megfogalmazásában és
szerkesztésében a claude-opus-5-5 modell segített, az adatkészlet adataiból; a számok az adatokból generáltak. A
kutatást a szerző tervezte, minden szerkesztői döntést ő hozott, minden állítást az adatokon ellenőrzött, és a
tartalomért teljes felelősséget vállal; MI-eszköz nem szerző.

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi rész a beküldött változatból kivehető. -->

---

## Beküldési jegyzet

Szószám (a beküldési szöveg angol változatában): az 1–4. szakasz, a cím, a szerzői sor, a kivonat, a táblázat és a
hivatkozások nélkül (a JOHD-sablon számítása) 966; a számozatlan nyilatkozatokkal 1 174; a
hivatkozásokkal is 1 248 (a beküldési oldal szerint a korlát a hivatkozásokat is tartalmazza; a kivonatról nem
szól); a kivonattal együtt 1 314. A JOHD data paper terjedelme 1000–1500 szó; a szerkesztőség megerősítheti, melyik
számítás érvényes. A kivonattól az MI-nyilatkozatig minden szó, a címsorokkal, a kulcsszavakkal, a szerzői
szerepekkel és a táblázattal: 1 408.

Beküldés előtt kitöltendő: az emberi validáció mezői ([N], pontosság, KI, kappa, egyezés a modell-ellenőrrel), a
levelező szerző e-mail-címe, a két ellenőr neve. A szöveg a JOHD hivatalos Word- vagy LaTeX-sablonjába kerül; a
kísérőlevél: `kozlemeny/data_paper/johd_cover_letter_en.md`.
