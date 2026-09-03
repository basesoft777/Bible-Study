# 2. Bővített PaRDeS sablon — teljes, részletes verzió

*v15 — 2026.09.03 (Új, feltételes „7. Lexikai audit — módszertani napló"
pont felvéve, a determinisztikus BDB/TBESH-protokoll [`Javasolt_sablon_
kiegeszites_BDB_arnyalat.md`] 2/a-2/e technikasorának dokumentálására;
a 4. pont „Kereséskor" bekezdése kiegészítve a technikasorra mutató
kereszthivatkozással; a záró önellenőrzés frissítve a 2/e LXX-híd
tanulsággal — üres Strong-szám-metszet önmagában nem elég a „tematikus,
nem lexikai" minősítéshez, gyök-szintű kapcsolatot is ellenőrizni kell)*
*v14 — 2026.08.31 (Új, opcionális „További igazolt kapcsolódások" kompakt lista
a 4. pont végén — a szintenkénti 1-2-es limiten túli ✅ jelöltek tömör
megjelenítésére, a kereszthivatkozás-napló mellett, nem helyette)*
*v13 — 2026.08.27 (Napló-frissítési utasítás javítva: a korábbi felsorolás csak
5 szekciót nevezett meg a hivatalos 7-ből, kimaradt a Részletes kulcsszó-
magyarázatok és a Feldolgozott igeszakaszok tábla — most mind a 7 név szerint
szerepel, számozva.)*
*v12 — 2026.08.27 (a 4. pont „Kereséskor:" bekezdése kiegészítve a kötelező
kereszthivatkozás-keresési napló előírásával — minden vizsgált jelöltet, nem
csak a kiválasztottakat, rögzíteni kell egy önálló `[könyv-mappa]/naplok/`
fájlban)*
*v11 — 2026.08.27 (3/b és 3/c önálló, főszintű ponttá alakítva (4. és 5.), a
Kiegészítő szempontok 6-ra tolódott)*
*v10 — 2026.08.26 (a 3/b pont „Kereséskor:" mondata lecserélve: a korábbi „célzott,
konkordancia-jellegű előfordulás-ellenőrzés" helyett explicit hivatkozás a
`PaRDeS_gyorsreferencia.md` új „Motívum-felismerés módszertana" szakaszára —
négyforrásos jelölt-gyűjtés és forrás-cimke megőrzése [Claude-tudás] eredetnél)*
*v9 — 2026.08.24 (a 2. pont 6. kiválasztási kritériuma finomítva: az objektív ritkaság szempontja mostantól explicit utal a `Strong_szotar.tsv` szófaj-mezőjére, mint kiegészítő, nem kötelező mérlegelési szempontra — az ige/melléknév-különbségtétel indoklásával; a kritériumlista 1-5. pontja és a lezáró mondat változatlan)*
*v8 — 2026.08.24 (STEPBible-integráció beépítve: a 2. pontba felvéve a kulcsszó-kiválasztás 6 szempontos explicit kritériumlistája; a 3/b pont végére felvéve a STEPBible TAGNT/TAHOT-alapú kötelező ellenőrzés a közös görög/héber szó feltételezésénél — mindkettő a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` 7.1 pontjában és a sablon-módosítási tervben korábban rögzített, de a sablonfájlba eddig be nem épített döntés végrehajtása)*
*v7 — 2026.08.15 (kiegészítve: nevesített tanítói egyezés-keresés öt lépéses módszere az Alkalmazás pontnál)*

**Kimenet nyelve:** magyar

---

## 0. Sorozat-kontextus *(feltételes pont)*

**Aktiválási feltétel:** nézd meg a `PaRDeS_motivumok.md` projektfájl „Feldolgozott igeszakaszok" táblázatát — ha ugyanabból a bibliai könyvből már volt korábbi tanulmány, automatikusan illeszd be ezt a pontot; egyébként hagyd ki (jelezve, hogy miért marad el).

Ha aktiválódik: rövid, 3-4 mondatos „eddig történt" összegzés, ami összeköti ezt a szakaszt az előző fejezetek/tanulmányok fő szálaival.

---

## 1. Alapkérdések

*(megegyezik az alap sablon Alapkérdések pontjával — teljes egészében, nem rövidítve)*

👤 **Ki írja ezt?**
Szerző háttere, szerepe (próféta, apostol, pap, király stb.), történelmi és lelki helyzete az írás pillanatában.

👂 **Kinek szól?**
Izraelnek, a korai egyháznak, egy konkrét személynek vagy gyülekezetnek íródott? Milyen helyzetben voltak a címzettek (üldözés, száműzetés, lelki eltévelyedés, öröm, konfliktus stb.)?

🌍 **Történelmi és kulturális háttér** *(rövid, tájékozódó jelleggel — 2-3 mondat)*
Mikor íródott? Melyik birodalom/kormányzat volt hatalmon? Feltámadás előtti vagy utáni esemény/irat? Ó- vagy újszövetségi könyv?

📖 **Irodalmi kontextus**
Milyen műfaj? Hol helyezkedik el ez a szakasz a könyv egészének ívében?

---

## 1/b. Idővonal / térkép *(feltételes pont)*

**Aktiválási feltétel:** illeszd be, ha a szakaszban legalább két különálló helyszín vagy időpont szerepel, vagy ha a történések sorrendje kulcsfontosságú a megértéshez (pl. útinapló-jellegű szakaszok); egyébként hagyd ki, és jelezd explicit módon, hogy nem releváns.

Ha aktiválódik: az események kronológiai sorrendje és/vagy földrajzi helyszínei röviden felsorolva.

---

## 2. Eredeti nyelvi szöveg *(a Peshat előtt)*

- A kulcsversek kulcsszavai táblázatban — **max. 6-8 szó versenként**, csak azok, amelyek ténylegesen befolyásolják az értelmezést: görög/héber szó, **kiejtés**, **Strong-szám** (G=görög/Újszövetség, H=héber/Ószövetség), szó szerinti jelentés.
- A teljes vers eredeti nyelven, mellette egy **szó szerinti tükörfordítás** (szórendhelyes, nyelvtanilag hű a göröghöz/héberhez), és a **Károli-fordítás** egymás mellett, összehasonlításképp.
- **Megjegyzés a πνεῦμα (*pneuma*, „szellem") és ψυχή (*pszükhé*, „lélek") megkülönböztetéséről**, valahányszor a szakaszban bármelyik szó előfordul — mivel a szokásos magyar fordítások (Károli, RÚF stb.) mindkettőt gyakran „lélek"-nek fordítják, elmosva a köztük lévő különbséget.

**A kiválasztás szempontjai** (legalább egynek teljesülnie kell ahhoz, hogy egy szó bekerüljön a táblázatba):
1. **Teológiai súly** — a szó jelentése önmagában állítást hordoz, ami a Peshat-értelmezést érdemben alakítja (pl. egy ige, ami kizárólag isteni alannyal fordul elő)
2. **Elmosódás a Károli/SzPA fordításban** — két vagy több eredeti szó egyetlen magyar szóvá olvad össze, elrejtve egy különbségtételt (pl. pneuma/pszükhé mindkettő „lélek")
3. **Motívum-kapcsolódás** — a szó egy, a `PaRDeS_motivumok.md`-ban már nyomon követett motívumhoz köthető
4. **Kereszthivatkozási potenciál** — a szó ritka, és emiatt a 4. pontban erős, lexikailag pontos kapcsolódást tehet lehetővé más igehelyekkel
5. **Exegetikai vita forrása** — a szó jelentése önmagában ad okot egy ⚠️ vitatott pontra
6. **Objektív ritkaság (STEPBible-adat alapján), szófajjal súlyozva.** Ha a szó előfordulás-száma alacsony (tájékoztató küszöb: kevesebb mint 15-20 előfordulás a teljes ÓSZ/ÚSZ-ben), ez önmagában felveti a kiválasztás lehetőségét. A Strong_szotar.tsv szófaj-mezője (most már elérhető) finomíthatja ezt a mérlegelést: egy ritka IGE gyakran nagyobb teológiai súlyt hordoz, mint egy hasonlóan ritka, de leíró jellegű melléknév vagy határozószó — ez nem szigorú szabály, csak további szempont a tartalmi mérlegeléshez, nem helyettesíti azt.

A 6. szempont nem helyettesíti, csak kiegészíti az 1-5. tartalmi mérlegelést.

---

## 3. PaRDeS keretrendszer

**Peshat (Szó szerinti)** *(részletesen kifejtve)* — A szöveg egyszerű jelentése, szerző, címzettek, kontextus, nyelvtani-kontextuális elemzés.

**Remez (Utalás)** — *„Milyen máshonnan ismert bibliai mintázatra/motívumra utal ez a szöveg?"* Asszociatív, intertextuális felismerés, következtetés nélkül.

**Drash (Keresés)** *(részletesen kifejtve)* — *„Milyen erkölcsi/teológiai tanítás vagy alkalmazás vezethető le belőle?"* Normatív, tanító réteg.

**Sod (Titok)** *(tömör, fegyelmezett)* — csak a Peshat/Remez/Drash rétegekből ténylegesen levezethető mélyebb igazság, önkényes allegorizálás vagy gematria nélkül. Releváns dokumentált misztikus forrás esetén → az 5. ponton keresztül, hivatkozva vonandó be, nem saját spekulációként.

⚠️ **Vitatott pontok** — csak ha ténylegesen van érdemi tudományos/teológiai vita, nevesített képviselőkkel bemutatva, nem homályos "egyesek szerint" megfogalmazással.

---

## 4. Kapcsolódó igehelyek — hol találkozunk még ezekkel a gondolatokkal a Bibliában

*Az alábbi kereszthivatkozások megmutatják, mely más igehelyek erősítik meg vagy világítják meg az egyes PaRDeS-rétegek meglátásait — irányjelöléssel: ← előkép, ↔ párhuzam, ⇒ beteljesedés.*

**Kereséskor:** A ritkább/egyedibb kulcsszavakra a „Motívum-felismerés módszertana"
(`PaRDeS_gyorsreferencia.md`) szerint járj el: mind a négy forrásból gyűjts jelöltet,
minősítsd tartalmilag, és csak ezután válaszd ki a legerősebb 1-2 kapcsolódást a 4.
blokkba. A forrás-cimkét (🔤/📖/📚/🧠) tartsd meg a végleges szövegben is, ha a
kiválasztott kapcsolat [Claude-tudás] eredetű. (Egy ritka szó néhány előfordulása
pontosabb és erősebb kapcsolódást adhat, mint egy tartalmilag hasonló, de lexikailag
független párhuzam.)

**A 2/a-2/e technikasor kapcsolódása:** ha egy kiválasztott kulcsszó a "13-as kör"
tagja (l. `Javasolt_sablon_kiegeszites_BDB_arnyalat.md` 8. pont), a fenti
négyforrásos FELFEDEZŐ keresésen túl kötelezően lefut a determinisztikus
BDB/TBESH-protokoll 2/a-2/e technikasora is (2/a BDB-ellenőrzés, 2/b Origin-lánc,
2/c teljes-előfordulás feltárás, 2/d motívum-azonosság, 2/e LXX-híd) — ez a
MINŐSÍTŐ funkció, nem újabb felfedezés. Az eredménye a 7. pontban (Lexikai audit)
dokumentálandó.

**Kötelező napló:** a fenti keresési/minősítési folyamat eredményét — MINDEN
vizsgált jelöltet, nem csak a kiválasztottakat — rögzítsd egy önálló fájlban:
`[könyv-mappa]/naplok/[study-fájlnév-kiterjesztés-nélkül]_kereszthivatkozas_naplo.md`.
A napló szerkezete: vizsgált kulcsszavak → nyers találatok forrásonként →
tartalmi minősítés minden jelöltre → végső döntés és indoklás → összegzés. Ez
teszi auditálhatóvá, hogy egy jelölt tényleg megvizsgálva lett és elutasítva,
nem egyszerűen kimaradt a keresésből.

- A kapcsolódó igehelyeket **közvetlenül az adott PaRDeS-szint alatt**, kontextusban add meg — ne külön táblázatban hátrébb.
- Szintenként **max. 1-2 legerősebb** igehely.
- A közös motívum-szót/fogalmat **emeld ki félkövérrel** mind a fő szövegben, mind a kapcsolódó igehely magyarázatában.
- A kapcsolódó igehelyet **vizuálisan elkülönített, behúzott blokkban** add meg (idézet-formázással, 🔗 jelöléssel), és **idézd a tényleges bibliai szöveget** (Károli-fordításban, mivel közkincs) — ne csak parafrazeáld.
- Az idézett szöveg mellett **zárójelben** tüntesd fel a kapcsolódó kulcsszót magyarul és az eredeti görög/héber szót kiejtéssel is, pl. *(kulcsszó: lehelet — héberül nesamá)*.
- Rövid, önmagában érthető „miért kapcsolódik" magyarázat.
- Ha egy kapcsolat kivételesen gazdag vagy vitatott: jelezd — *„Ez a kapcsolat érdemes lenne egy önálló összevetésre — szólj, ha szeretnéd."*
- A rész végén **összegző mondat** köti vissza a kereszthivatkozásokat a tanulmány gondolatmenetéhez.
- Ha a `PaRDeS_motivumok.md` fájlban már szerepel az adott motívum egy korábbi tanulmányból: *„Ismétlődő motívum korábbi tanulmányodból: ..."* — csak tényleges kapcsolódás esetén.
- **A tanulmány után frissítsd** a `PaRDeS_motivumok.md` fájlt az új előfordulással — a bővített naplószerkezet mind a HÉT érintett részét (1. tematikus áttekintés, 2. kulcsszó-index Téma/ÓSZ-ÚSZ/Előfordulás-szám oszlopai, 3. részletes kulcsszó-magyarázatok — beleértve a „Lásd még" kereszthivatkozásokat is, 4. könyv szerinti index, 5. ⭐ Emlékeztető küszöb, 6. „Még nem feldolgozott, de valószínű motívumok", 7. „Feldolgozott igeszakaszok" tábla), nem csak a kulcsszó-listát. Mielőtt a frissítést véglegesítenéd, `grep`-pel ellenőrizd, mely szekciók ténylegesen érintettek — ne feltételezd.
- **Rokon motívum-csoport küszöbszámítás:** ha egy azonosított motívum **tematikusan rokon, de lexikailag önálló** egy másik, már naplózott motívummal (pl. eltérő szó, de rokon fogalom vagy ismétlődő mintázat), az egyéni előfordulás-számláló mellett **jelöld külön a rokon-csoport összesített előfordulását is**, figyelmeztetésként (pl. „a szűkebb motívum önmagában még N-nél tart, de a tágabb rokon-csoporttal együtt már túl van a küszöbön"). A csoportosítás mindig indoklással történjen — ne legyen automatikus vagy erőltetett.

**További igazolt kapcsolódások (opcionális, kompakt lista):**
Ha a keresés a szintenkénti 1-2 legerősebbön túl is talál ✅ minősítésű
jelöltet, ezeket NE teljes 🔗 idézet-blokkban, hanem egy rövid, bullet-point-os
listában add meg az „Összegzés" bekezdés után:

> **További igazolt kapcsolódások:** Ámós 4:13 (Isten mint teremtő, doxológia);
> Ézs 40:28 (Isten mint a föld határainak teremtője); 2Kir 19:15 / Ézs 37:16
> (szinoptikus pár, „te teremtetted az eget és a földet")

Formátum: igehely + zárójeles, 3-6 szavas indoklás, vesszővel elválasztva,
NEM külön 🔗 blokkban. Ez nem helyettesíti a kereszthivatkozás-naplót (ahol a
TELJES minősített lista, indoklással szerepel) — ez a tanulmány saját olvasói
számára ad tömör, de nem elveszejtett hozzáférést a további igazolt
kapcsolódásokhoz, anélkül hogy a fő szöveget túlterhelné.

**Ha explicit kéred egy igehely-pár/motívum mélyebb összevetését**, az önálló, célzott elemzésként készül (nem a fő tanulmány része), az alábbi szerkezettel:
1. Szövegkörnyezet mindkét igehelyre.
2. Nyelvi/filológiai összevetés, ha közös görög/héber szó van.
3. Az irodalmi kapcsolat jellege (tudatos utalás vs. független fogalmi rokonság).
4. Tudományos vélemények nevesített szerzőkkel, ha vitatott.
5. Záró mondat, hogy érdemes-e frissíteni ennek fényében a fő tanulmány 4. pontját vagy a `PaRDeS_motivumok.md` naplót.

**STEPBible-ellenőrzés:** ha közös görög/héber szó feltételezhető két igehely között, ellenőrizd a STEPBible TAGNT/TAHOT adatbázisban (`konkordancia/TAGNT_kivonat.tsv`, `konkordancia/TAHOT_kivonat.tsv`) mindkét igehely releváns szavának Strong-számát és szótövét, és a nyers eredményt (Strong-szám, szótő, morfológiai alak) építsd be az összevetésbe — ne csak háttér-ellenőrzésként használd. Ha a Strong-szám azonos, de a szótő eltér, vagy fordítva, ezt a tényt explicit rögzítsd a kapcsolódás leírásában.

---

## 5. Rabbinikus és patrisztikus hangok

A Remez/Sod rétegekhez: korai zsidó (Midrás, Talmud) és korai egyházatyai értelmezések bemutatása a modern kommentárok mellett. Ha van releváns rabbinikus **és** patrisztikus anyag is, mindkettő szerepeljen; ha csak az egyik hagyományban van releváns forrás, jelezd ezt explicit módon (pl. „rabbinikus párhuzam nem azonosítható, mivel..."), hogy tudatos döntésnek tűnjön, ne hiányosságnak.

---

## 6. Kiegészítő szempontok

**Hermeneutika** — mint az alap sablonban: szerzői szándék, műfaj, irodalmi mintázatok, értelmezési elvek.

**Bibliai nyelvek** — mint az alap sablonban, kiejtéssel kiegészítve.

**Történelmi és kulturális kontextus** *(konkrét, célzott)* — mint az alap sablonban: csak a vers/kifejezés jelentését ténylegesen alakító részletek.

**Vitatott pontok jelzése** — ⚠️, nevesített képviselőkkel, csak érdemi vita esetén.

**Alkalmazás és tanítványság** *(itt konkretizálva — ez csak a bővített sablon sajátja)*
Zárja a tanulmányt 2-3 konkrét kérdés megválaszolásával:
1. *Mit jelent ez a mai hívő mindennapi életében?*
2. *Milyen konkrét lépést, döntést vagy szokásváltozást von maga után?*
3. *Milyen érzelmi/lelki ellenállás vagy nehézség merülhet fel ezzel kapcsolatban, és hogyan szólítja meg ezt a szöveg?*

**Forrás:** alapértelmezésben a válaszok a tanulmány saját Peshat/Remez/Drash/Sod megállapításaiból vezetendők le. Ha a felhasználó explicit kér egy adott nevesített tanító/szerző szemszögéből megfogalmazott alkalmazást (pl. Derek Prince, Charles Capps), a 3 kérdés struktúráját megtartva, de kizárólag az adott szerző fellelhető, ellenőrizhető tanításaira támaszkodva készül — forrásmegjelöléssel (mű/prédikáció címe, elérhetőség). Ha nincs elég megbízható forrás az adott szerzőtől erre a versre nézve, ezt explicit jelezni kell, nem szabad gyengébb anyaggal pótolni.

**Nevesített tanítói egyezés-keresés módszere** *(mindig ez az öt lépés, ebben a sorrendben, ha a felhasználó nevesített tanítói forrást kér)*:
1. **Motívum-kiemelés** — a tanulmány Peshat/Remez/Drash/Sod megállapításaiból a konkrét, teológiailag súlyos csomópontok kiszűrése.
2. **Névsor a jóváhagyott listából** — csak az elmentett, jóváhagyott tanítói körből dolgozz, ne tetszőleges nevekből.
3. **Célzott keresés motívumonként** — minden motívumhoz külön keresés: tanító neve + a konkrét vers/téma; nem elég az általános tematikus egyezés.
4. **Forrás-ellenőrzés** — csak akkor vehető fel, ha elsődleges vagy megbízható másodlagos forrás (könyv/kiadói leírás, prédikáció-átirat, elemző cikk idézettel) ténylegesen az adott igehelyre hivatkozik; puszta asszociatív/tematikus rokonság nem elég.
5. **Hiány explicit jelzése** — ha egy motívumhoz nem található így megbízható, nevesíthető anyag, ezt nyíltan jelezni kell, nem szabad gyengébb vagy csak áttételes kapcsolattal pótolni.

---

## 7. Lexikai audit — módszertani napló *(feltételes pont)*

**Aktiválási feltétel:** illeszd be, ha a tanulmány bármely kulcsszavára
lefutott a determinisztikus BDB/TBESH-protokoll (`Javasolt_sablon_
kiegeszites_BDB_arnyalat.md`) 2/a-2/e technikasora — tipikusan azért,
mert a szó a "13-as kör" tagja. Ha egyetlen kulcsszóra sem futott le a
technikasor, hagyd ki ezt a pontot, és jelezd explicit, miért marad el
(pl. "egyik kulcsszó sem tagja a 13-as körnek ebben a tanulmányban").

Dokumentálja, tömören, mely kulcsszavakon futott le a technikasor:

| Kulcsszó (Strong) | 2/a BDB | 2/b Origin-lánc | 2/c Teljes-előfordulás | 2/d Kereszthiv./motívum-azonosság | 2/e LXX-híd | Eredmény |
|---|---|---|---|---|---|---|
| *(pl. H7604)* | *(rövid összegzés)* | *(talált-e láncot, hova vezetett)* | *(hány előfordulás, van-e kiaknázatlan)* | *(erősít/gyengít egy meglévő kapcsolatot)* | *(ha releváns, gyök-szintű eredmény)* | *(beépítve / elutasítva, hol a tanulmányban)* |

**Elutasított leletek külön, indoklással:** minden olyan találat, amit a
fenti lépések feltártak, de NEM került be a study szövegébe, itt
rögzítendő, megnevezett indokkal (pl. "BDB szerint a gyök ismeretlen, a
Strong-szótár spekulatív hivatkozását nem építettük be — l.
forrás-hivatkozási fegyelem"). Ez nem redundáns a kereszthivatkozás-
naplóval (ami a 4. pont felfedező keresésének teljes nyers anyagát
tartalmazza) — ez a 2/a-2/e lexikai audit saját, tömör összegzése.

**Forrás-hivatkozási fegyelem (kötelező minden sorban):** minden fenti
cellánál explicit jelölve, honnan jött az adat — közvetlenül a saját
repó fájljából (`BDB_teljes_unabridged.tsv`, `Strong_szotar.tsv`,
`TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv`, `LXX_kivonat_Genezis.tsv`) vagy
külső, csak tartalmilag ellenőrzött forrásból (l. `Javasolt_sablon_
kiegeszites_BDB_arnyalat.md` 2. pont).

---

## Terminológiai és formai szabályok (minden sablonra érvényes)

- „Szentlélek" helyett mindig **„Szent Szellem"**
- A Sod rétegnél „misztikus" helyett mindig **„spirituális"**
- Minden görög/héber szótári szó mellett feltüntetve a **kiejtés**
- Igehely-rövidítések egységesen, szóköz nélkül (pl. „1Thessz 5:23")
- A Szent Pál Akadémia-fordításból csak rövid idézetek; teljes versekhez a Károli-fordítás
- **Fájlnév-konvenció:** `[Könyv]_[fejezet]v[vers]_[típus].md` (pl. `1Moz_1v1_bovitett.md`); tartománynál `[Könyv]_[fejezet]v[vers]-[fejezet]v[vers]_[típus].md` (pl. `1Moz_1v2-2v3_bovitett.md`); teljes fejezetnél vers-komponens nélkül (pl. `1Moz_14_bovitett.md`). A `v` betű egyértelműen elválasztja a fejezetet a verstől, a kötőjel kizárólag a tartomány határait jelöli.

## Konfliktuskezelés
Ha két elmentett szabály ütközni látszik, explicit rákérdezés következik, nem önkényes döntés.

---

*A tanulmány véglegesítése előtt belső önellenőrzés fut le minden fenti szabályra. Ennek része: valahányszor a szöveg azt állítja/sugallja, hogy két igehely közös szótő/szócsalád (lexikai) kapcsolatban áll, ellenőrizni kell, hogy ténylegesen ugyanaz-e a görög/héber szó (nem csak rokon jelentésű). Ha nincs azonos Strong-szám, EZ ÖNMAGÁBAN MÉG NEM ELÉG a "tematikus, nem lexikai" minősítéshez (l. a protokoll 2/e pontja, LXX-híd) — külön ellenőrizni kell a gyök-szintű kapcsolatot is (közös triliterális héber gyök, vagy közös görög szótő eltérő igekötővel/alakban). Csak ha SEM az azonos szó, SEM a közös gyök nem áll fenn, minősíthető a kapcsolat "tematikus, nem lexikai párhuzamnak". Ha gyök-szintű kapcsolat van, de nem azonos a szóalak, ezt "gyök-szintű lexikai rokonság"-ként kell rögzíteni — sem "tematikus"-ként, sem azonos-szóként nem szabad feltüntetni.*
