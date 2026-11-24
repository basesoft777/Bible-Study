# LSJ: a biblematedata-modul és a hivatalos Perseus lexica összevetése (2026-11-24)

**Igazolt-e, hogy a mi LSJ-adatunk a Perseus lexica-anyaga? Tartalmilag igen, szó szerinti másolatként nem.** A modul (`konkordancia/lexikonok_nyers/LSJ.lexicon`) 5 523 szócikkéből 894 a modul készítőjének saját pótszövege (nem LSJ); a maradék 4 629 LSJ-szöveges szócikk közül 4 588 (99,1%) megtalálható a Perseus-anyagban; 3 811 (82,3%) betűről betűre azonos görög szöveggel és azonos angol tartalmi szavakkal, további 388 (8,4%) legalább 99%-os lefedettséggel. Szó szerint azonos szócikk viszont 0 van: a modul átdolgozott változat (HTML, sorszámcímkék, átírt szentírási hivatkozások, hozzáadott bibliai linkek, 157 csonkolt szócikk). A szöveg tehát a Perseus LSJ-je; a „lexica repó → Eliran Wong modulja” lánc dokumentuma továbbra sincs, csak a szöveg egyezése bizonyítja a forrást.

```
proveniencia: scope=konkordancia/lexikonok_nyers/LSJ.lexicon (5523 szócikk, sha256 6fb20986a6840de0d8d92b8c38abd87c07ec57f4930ccee1b83f22285a14072f) × PerseusDL/lexica CTS_XML_TEI/perseus/pdllex/grc/lsj/ (27 XML, 116 497 entryFree) | forras=github.com/PerseusDL/lexica @ 1c34cdf756c63cf37db61bd366d733431dbd7aa0 (master, 2026-10-26T18:46:46Z) | ts=2026-11-24
```

A mérés és a jelentés kész; az esetleges átállás külön döntés (a javaslat a 6. pontban, ⛔ az integrátornak).

## 1. A Perseus-oldal: hely, méret, rögzített commit

| | |
|---|---|
| repó, ág, fej | `PerseusDL/lexica`, `master`, `1c34cdf756c63cf37db61bd366d733431dbd7aa0` (2026-10-26) |
| az LSJ helye | `CTS_XML_TEI/perseus/pdllex/grc/lsj/` (a `lsj` mappa fa-azonosítója ezen a commiton `eae306a548b675d18281f8160764a1871ada7c2c`) |
| tartalom | `README.md` (446 bájt) + 27 db `grc.lsj.perseus-eng1..27.xml` |
| méret | 283 629 390 bájt (≈ 270 MiB), a 300 MB-os határ alatt |
| szócikk | 116 497 `entryFree` (111 895 `main`, 4 602 `gloss`); a kulcs (`key`) Beta-kódú, a görög szöveg is |
| licenc | a fájlok fejlécében: CC BY-SA, a 4.0-s licenc hivatkozásával; a megjelölés: Perseus Digital Library |

A nyers fájlok a repón **kívül** (scratchpad) vannak, a repóba nem kerültek. SHA-256 minden fájlra (a letöltés mérete a git-fa szerinti méretekkel egyezett, mind a 28 fájlra):

```
d58b026368925f2fb11dce70a51022efe224a09fb4902e44c740496a4db67a91  README.md
96c89b299bd3a81ee8707bd7092e42878d172b3f301da0adfa41d8d09dfbfde9  grc.lsj.perseus-eng1.xml
51e496289761bab5fb0c4346eded476f12266ce203a30ed2d0fb7500193a9a81  grc.lsj.perseus-eng10.xml
aefc985475f565798afc59ead25d6afa7175dfbc2ab858ef26cc0f3742b84809  grc.lsj.perseus-eng11.xml
6f58010f38711cdcd2812ec9baaedc6d51f2cc39adb24ae9941371c0f2cc2543  grc.lsj.perseus-eng12.xml
983c54dbb094763cb2b92a130656fdd73454b9e85bcfbd121c578c7f4795d58c  grc.lsj.perseus-eng13.xml
8190b1823958783f4820fa7dbeef590cb7f46a50f366473d3008778dfd260c3c  grc.lsj.perseus-eng14.xml
a5f8cc41fe8a05ad3dc45e105e647f20cadebd46ca5250256fe79913746eedb0  grc.lsj.perseus-eng15.xml
492ce0d174267544388f4938324a4137f21a8d7ae86e5d28dec5beaf1a496b7e  grc.lsj.perseus-eng16.xml
4c02d9b465e684d4d83286c80049492e7c5e81250e3ed8e6b1ca1d3fb21a6dc5  grc.lsj.perseus-eng17.xml
72f346e95bf9cb334d119103ff1cab89e39b0bb2fae1364de51428ac8655f727  grc.lsj.perseus-eng18.xml
867386bbb250dc127d73ba105a92fd3a2115a94702ec3c1ffdea575c77bdca57  grc.lsj.perseus-eng19.xml
e711d36e733f6c199afb84819e86ea0f607b92cbaea4ee8a915e77ebc4662ced  grc.lsj.perseus-eng2.xml
b39478b6c607db3750ab71e5c4dc4ff40b688cac3d966f4afe62d5ec281e142b  grc.lsj.perseus-eng20.xml
21e5b7e46964192e520c90a177b2dc5c7893e524afce356ccbf9054d43d03189  grc.lsj.perseus-eng21.xml
953b6c398e460cd633be2fefc144e17399a3a9f111d3388d032023227380149b  grc.lsj.perseus-eng22.xml
36ad46cab32dc131619a902d959893a407f1fcfc743c7e129ea9aee6fbde6597  grc.lsj.perseus-eng23.xml
6d3d8c83110b0a3b94c97cf2f9ddf8ced87a6d740a312de2b8a21a3b224677c7  grc.lsj.perseus-eng24.xml
5ba38f1e6f5886af6ee236028d6aee8e910aec89cb66954ae719a05a6866111d  grc.lsj.perseus-eng25.xml
174f544c0afed660fb0aebf7457da4d78a26889b8d40922533473bdf0a6b5c9e  grc.lsj.perseus-eng26.xml
23bea40e1fe0484c39df438112c9cf728df29f3c97d9c465f1b1aaa194840ab6  grc.lsj.perseus-eng27.xml
2853d7882df86225df5824e63b579f1ac84f72a89f2ae75961a77a443b4958fa  grc.lsj.perseus-eng3.xml
dbe9a65694887bac4e99c41155e48926ab4b840157ce955479642925bdfc029b  grc.lsj.perseus-eng4.xml
ea63fc316565059bc05c338f369f72b1366dc464e3b3d761e1f9ad447416eb3f  grc.lsj.perseus-eng5.xml
ce0111eb40d9b9d720e59e0d6caaa97b3386ff72f46b195d7a238756d1348479  grc.lsj.perseus-eng6.xml
5340dd231acf6bc79d134e57def4c459c71ed9afbcd0ef3ad4457ebcab164c17  grc.lsj.perseus-eng7.xml
94ea07a228bb7a25f1d2cf93fe0f3fa4b72e6b17553fca069ad06ae5bb78f518  grc.lsj.perseus-eng8.xml
7f274c8dce5f6837c55f3f3db5c8e86c84c70c42631bb07b761b196d5c0d4f86  grc.lsj.perseus-eng9.xml
```

**A repóban rögzített régebbi commit** (`adat/licencek.tsv`: `56061ca…`, 2026-09-02) és a mostani fej között a 27 XML-fájl mindegyikének mérete ~490 bájttal nőtt: a 2026-10-22-i és 10-26-i commit (`LSJ: availability statement work`, `updating license statement`) a fejlécbe új `<availability>` blokkot tett. Négy fájlon (eng6, eng7, eng18, eng19) ellenőriztem: az `<availability>` nélkül a két commit tartalma szóközig azonos. A mappa érintő commitjai: 2026-10-26, 2026-10-22, majd 2025-09-24 (egy hivatkozás-javítás); vagyis az LSJ-szöveg a repóba beemelés (2026-09-07) és a mostani fej között érdemben nem változott. Nem mértem: a 2025-09-24-i javítás előtti változatot, és a modul készítőjének letöltési időpontja ismeretlen.

## 2. Mit mértem, és hogyan

1. **Perseus-oldal:** a 27 XML-ből regexszel kinyertem az `entryFree` elemeket; a görög elemek (`lang="greek"`) Beta-kódját saját átalakítóval Unicode-ra váltottam, a jelölést eltávolítottam, a szóközt normalizáltam. 116 497 szócikk.
2. **Modul-oldal:** az SQLite `Lexicon` tábla 5 523 sora (`Topic` = Strong-szám, `Definition` = HTML); a jelölést eltávolítottam, az entitásokat feloldottam. A modul sorai a `konkordancia/LSJ_teljes.tsv` sorával egy az egyben megfelelnek (5 523).
3. **Párosítás:** a modul nem a Perseus-kulcs, hanem a Strong-szám szerint kulcsolt, és a Strong-lemma gyakran sérült (a kombináló jelek külön tokenként állnak). Ezért a szöveg elejéről 1–4 tokenes lemmajelölteket képeztem (ékezet nélkül, kisbetűsen), ezekkel kerestem a Perseus-szócikkeket; a modul egy sora több Perseus-homográfot is tartalmazhat, ezért a Perseus-szócikkek halmazát vettem (a modulban legalább 60%-ban megtalálható szócikkek, plusz a legjobb egyetlen jelölt). Az 51 párosítatlan sort még egy részlet-keresés követte (3 minta × 22 görög betű az egész Perseus-szövegben).
4. **Összehasonlítás:** *görög váz* (a görög betűk ékezet és szóköz nélkül, ς=σ) és *angol tartalmi szavak* (4 betűnél hosszabb latin betűs szavak, a szentírási könyvnév-rövidítések és a római számok kivételével) szerint, kétirányú 5-gram-lefedettséggel. Külön számoltam az idézethelyek számtokenjeit is (pl. `277b19`, `2.143`; a kettőspont pontra normalizálva).
5. **Pótszöveg-felismerés:** a modul olyan sorai, amelyek nem LSJ-t tartalmaznak, hanem a készítő saját sablonmondatát (l. 3. pont).

**Mit nem fog meg a mérés (merce_vakfolt):** az 1–3 betűs latin rövidítések (szerző- és műnév-rövidítések: „Il.”, „Ep.Cor.” vs „2Co”) és a számok közül csak a legalább 3 jegyű vagy ponttal tagolt idézethelyek számítanak; a jelentésszavak közül a rövid (≤3 betűs) angol szavak nem. A sorszámcímkék (I, II, 1., 2.) nem számítanak. A „T2b” osztály egy része a saját átalakítóm műterméke (Beta-kód-szóköz a görög elemek határán, szóvégi szigma). A szócikkpárosítás heurisztika: a határesetekben (rövid, 1–2 szavas szócikkek) a lefedettségi mutató ingadozó.

## 3. Az eredmény

**A modul 5 523 szócikke:**

| | db | % |
|---|---|---|
| modul-szerzői pótszöveg, nem LSJ (nevek: „is not Defined by LSJ”; Strong-utalás „Adverb from G…”; „no Definition found”) | 894 | 16,2 |
| ezekhez jön 41 rövid (≤ 40 görög betűs) párosítatlan sor, szintén Strong-eredetű nyelvtani megjegyzés („Accusative plural masculine of G3778”) | 41 | 0,7 |
| **LSJ-szöveges, Perseus-párral** | 4 588 | 83,1 |

**A 4 629 LSJ-szöveges sor** (894 pótszöveg nélkül) osztályai:

| osztály | db | % | jelentés |
|---|---|---|---|
| szó szerint azonos | 0 | 0 | a modul átdolgozott: minden szócikkben van formázási eltérés |
| **T2 azonos tartalom, csak formázás** | 3 539 | 76,4 | görög váz és angol tartalmi szavak egyeznek; eltérés: sorszámcímkék, szóköz/írásjel, hivatkozás-átírás |
| **T2b azonos betűanyag** | 272 | 5,9 | a görög betűk azonosak; csak ékezet/hosszúságjel/szóköz-részlet más (részben mérési műtermék) |
| **T3 csekély eltérés** | 388 | 8,4 | kölcsönös lefedettség ≥ 99%: pár szó/hivatkozás tér el |
| T5a modul rövidebb | 132 | 2,9 | a modul szövege a Perseus-szócikk része (a Perseus-szövegnek 50–97%-a) |
| T5b modul sokkal rövidebb | 25 | 0,5 | a modul a Perseus-szócikknek kevesebb mint felét tartalmazza (csonkolt) |
| T6 modul hosszabb | 61 | 1,3 | a Perseus-szócikk benne van, de a modul több szöveget tartalmaz |
| T7 kétirányú eltérés | 161 | 3,5 | mindkét oldalon van többlet (összevont homográfok, szomszédos szócikkek) |
| párosítatlan | 51 | 1,1 | 10 részlet-kereséssel megfeleltetve; 41 rövid, Strong-eredetű mondat (l. fent) |

T2+T2b = 3 811 (82,3%); T2+T2b+T3 = 4 199 (90,7%). A T2+T2b szócikkek közül 3 154-nél (82,8%) az idézethelyek számtokenjei is azonosak; 657-nél eltérnek (a modul a szentírási hivatkozásokat átírta, lásd lent).

**Eltérés-típusok (formázás, nem tartalom):**

- sorszámcímkék beszúrva (`I`, `II`, `1.`, `2.`): a Perseus a sorszámot attribútumban tartja, a szövegben nincs;
- a szentírási hely-hivatkozások átírva: `Ev.Luc.` → `Luk`, `2 Ep.Cor.` → `2Co`, `Ep.Hebr.` → `Heb`, `Apoc.` → `Rev`, `Ge.` → `Gen`; a fejezet.vers-elválasztó pontból kettőspont (`11.9` → `11:9`); a LXX Királyok-könyveket átszámozta (`1 Ki` → `1Sa`);
- 3 125 szócikkbe (a 5 523-ból) a modul bibliai linkeket (`bcv(...)`) tett be;
- a Perseus `<xr>` hivatkozásaiból a modulban a „cross” szó lett;
- Beta-kódból Unicode; a modul HTML-lé alakította, színes tagekkel;
- szóköz az írásjelek előtt (`Od . 24.486`).

**Perseus-oldal:** 116 497 szócikkből a modul kb. 5 000-et (4,3%) használ; a többi (kb. 111 400) nincs a modulban. Ez nem hiba: a modul a Strong-számokhoz rendelt lexémákat tartalmazza (NT + LXX), a Perseus pedig a teljes LSJ-t.

## 4. Az eltérések háttere

- **Csonkolás (157 szócikk, T5a+T5b):** a modul a hosszú szócikkeket valahol félbevágja (pl. G5259 ὑπό: a modul 12 240 karakter a Perseus 21 149 karakteréből; a szöveg a 3 896. görög betűnél ér véget a 6 749-ből). A legnagyobb modul-sorok 53–62 KB-os HTML-ek.
- **Összevonás és szomszéd szócikk (T6+T7, ~220):** a modul egy Strong-számhoz több Perseus-szócikket (homográfok, rokon szavak) fűz. Példák: G1650 ἔλεγχος alatt a szócikk végén az ἐν szócikke áll; G1390 δόμα alatt a δῶμα szócikke. Hogy a Strong → szócikk hozzárendelés hány helyen téves, ezt **nem mértem**; a minták szerint van ilyen.
- **Pótszöveg (894 + 41):** a modul készítője a Strong-számokhoz olyan sorokat is tett, amelyeknek nincs LSJ-szócikkük (nevek, ragozott alakok); ez nem Perseus-anyag. Ezek a Strong's-lexikonból származó mondatok („Adverb from G2152”, „Middle voice from G4253 and G2192”); az eredetük a repóban nincs külön rögzítve.

## 5. 20 eltérő minta

Minden minta: Strong, lemma, a Perseus-kulcs és -azonosító, osztály, a kétirányú lefedettség (modul → Perseus / Perseus → modul), az eltérés rövid kivonata. (A Perseus-oldal már átalakított szöveg; a szövegrészletek legfeljebb 170 karakteresek, CC BY-SA, forrás: Perseus.)

1. **G4847 συμπολῑτ-ης** · `sumpoli/ths` (n98766) · T2b · 1,00/1,00 — görög betűk azonosak; „συμπολῑτ” (modul, macron) / „συμπολί τ” (Perseus, ékezet és szóköz; a szóköz az átalakítóm műterméke).
2. **G5021 τάσσω** · `ta/ssw` (n102515) · T2b · 1,00/1,00 — „φυλάσσουσ” (modul) / „φυλάσσους” (Perseus): szóvégi szigma-alak.
3. **G2149 εὐρῠχωρ-ος** · `eu)ru/xwros` (n45066) · T2b · 1,00/1,00 — „εὐρῠχωρ” (modul) / „εὐρύ χωρ” (Perseus): hosszúságjel vs. ékezet+szóköz.
4. **G3555 νοσσια** · `neossia/` (n70379) · T3 · 1,00/1,00 — modul: „νοσσια νεοσσ-ιά, Ion”; Perseus: „νεοσς-ιά, Ion”: a modul a Strong-lemmát (νοσσια) a szócikk elé teszi; a „σς” az átalakítóm szóvégi szigma-műterméke.
5. **G5500 χειροτον-έω** · `xeirotone/w` (n113692) · T3 · 1,00/1,00 — modul: „Act 14:23; Acts cf. 2 Cor”; Perseus: „Ap. 14.23, cf. 2 Ep”: könyvnév- és elválasztó-átírás.
6. **G2932 κτάομαι** · `kta/omai`+`kte/omai` (n60308+n60330) · T3 · 1,00/0,994 — a Perseus-halmaz az apró κτέομαι-szócikket („Ion. for κτάομαι”) is tartalmazza, a modul szövegében ez nem szerepel.
7. **G3321 μεσουρᾰν-ημα** · `mesoura/nhma` (n66517) · T3 · 1,00/1,00 — modul: „1. ulmination, Str. 3.5”; Perseus: „culmination, Str. 3.5”: a modulban betűhiány (c) és sorszámcímke.
8. **G4183 πολύς** · `polu/s` (n85306) · T5a · 0,999/0,852 — a modul a Perseus-szöveg ~85%-át tartalmazza; az idézethelyek számtokenjeiből 50 hiányzik a modulból, 3 többlet van.
9. **G4538 σαλπ-ιστής** · `salpigkth/s`+`salpisth/s` (n93164+n93170) · T5a · 1,00/0,957 — a modul az „σαλπ-ιστής, v. σαλπιγκτής” utalást a szócikk elejére teszi; a Perseus a végén.
10. **G1848 ἐξουθεν-έω** · `e)coudeno/w`+`e)couqene/w` (n37631+n37636) · T5a · 1,00/0,939 — a modulban nincs meg az ἐξουδενόω-szócikk („set at naught, LXX Jd. 9.38”), amely a Perseus-halmazban benne van.
11. **G5100 τις** · `tis` (n104051) · T5b · 1,00/0,418 — a modul a nagy szócikknek 42%-át tartalmazza; a hiányzó rész ~343 számtokent (idézethelyet) hordoz.
12. **G1432 δωρεάν** · `dwrea/` (n29787) · T5b · 1,00/0,0095 — a modul csak egy rövid Strong-eredetű sort („δωρεάν Accusative …”) tartalmaz (a pótszöveg-felismerőm kihagyta); a Perseus a δωρεά szócikkét adja.
13. **G2402 ἱδρώς** · `i)=dos1` (n49922) · T6 · 0,56/1,00 — a modulban „A strengthened form of a primary word ἰδος idos (sweat)” (Strong-szótár) áll az LSJ-szócikk előtt.
14. **G1390 δόμα** · `do/ma1`+`do/ma2` (n27967+n27968) · T6 · 0,16/1,00 — a modul végén a δῶμα szócikke is megjelenik („δῶμα, ατος, τό, (δέμω) I 1. house”).
15. **G1650 ἔλεγχος** · `e)/legxos1`+`e)/legxos2` (n33537+n33538) · T6 · 0,19/0,994 — a modul a szócikk után az ἐν („in”) szócikkét is tartalmazza (224 számtoken többlet).
16. **G234 ἀλίσγεμα** · `a)lisge/w` (n4271) · T6 · 0,33/1,00 — a modul a Strong-sablonmondatot („ἀλίσγεμα from ἀλισγέω, pollute”) a szócikk elé teszi.
17. **G1709 ἐμπνέω** · `e)mpnei/w`+`e)mpne/w`+`pnei/w` (n34423+n34431+n84033) · T7 · 1,00/0,978 — a Perseus-halmaz az apró ἐμπνείω-szócikket („poet. for ἐμπνέω”) is tartalmazza, a modulban nincs.
18. **G4430 πτῶμα** · `ptw=ma` (n91272) · T7 · 0,985/1,00 — a modul a lemmát kétszer adja („πτω ͂ μα πτῶμα”: Strong-lemma + LSJ-lemma).
19. **G2338 θῆλυς** · `qh/lea`+`qh=lus` (n48635+n48670) · T7 · 1,00/0,983 — a Perseus-halmaz a két apró szomszéd szócikket (θήλεα, θηλεογονία) is tartalmazza, a modulban nincsenek.
20. **G390 ἀναστρέφω** · `a)nastre/fw` (n7561) · T7 · 0,993/0,972 — a modul szövegében egy görög szó Beta-kódban maradt (`a)nakukliko/s`: a modul saját átalakítási hibája); a Perseus-oldalon „ϝ. ἀνακυκλικός”: a `v.` digammává alakulása az **én** átalakítóm hibája, nem adateltérés.

## 6. Javaslat

**(a) A származás igazolt, a lap mondata igaz — két kiegészítéssel.** Az `adat/licencek.tsv` LSJ-sorába és a lap „LSJ forrás: … Perseus Digital Library (lexica repó)” mondatába a mérés alapján ez írható: *a szöveg tartalmilag azonos a Perseus lexica LSJ-jével* (a görög és angol szöveg 82–91%-ban betűről betűre; a mérés: ez a jelentés), *de a mi adatunk a biblematedata-modul átdolgozott változata*, amelyben a Strong-számhoz rendelés, a HTML-formázás, a bibliai hivatkozások átírása és a pótszövegek a modul készítőjének hozzáadása. A CC BY-SA 4.0 „módosítva” jelzést igényel; a lapmondat így pontosabb: „LSJ: Perseus Digital Library (lexica repó), Eliran Wong biblematedata-moduljának átdolgozásában, Strong-számokhoz rendelve”. A jelenlegi `licencek.tsv`-sor megjegyzése („a Wong-modul marvel.bible oldala CC BY-SA 3.0-t jelöl”) és a Perseus 4.0-s nyilatkozata közti eltérés (3.0 / 4.0) a mérés tárgyán kívül esik, a 4.0 a hivatalos forrás szerint érvényes.

**(b) Átállás a hivatalos változatra: nem szükséges a származás igazolásához, és nem helyettesítő csere.** Ha az integrátor mégis kéri (például a 157 csonkolt szócikk, a hozzárendelési hibák és a pótszöveg miatt), az átállás nem fájlcsere: a Perseus lemma-kulcsú, **nincs benne Strong-szám**, ezért a Strong → szócikk hozzárendelést magunknak kell előállítani (a modul hozzárendelése adja a kiindulást, a hibás helyeket külön mérni kell). Ami érintené: `konkordancia/LSJ_teljes.tsv` (5 523 sor, a modulból levezetve), `konkordancia/lexikonok_nyers/LSJ.lexicon` és `LXX.lexicon` (az `adat/licencek.tsv` szerint LSJ-alapú), `adat/forditasok.tsv` (2 LSJ-sor: `G2564`, `G0086`), `adat/szotar_szerepek.tsv` (gorog: „LSJ, ha releváns”), és a lexikonlapok, amelyek az LSJ-t nevezik meg: `ALVIL-001`, `ANTROP-001`, `HAMART-001`, `ISTENTISZT-001` (`_TUDOMANYOS.md`), `HODIT-001`, `KIRALY-001`, `MENNY-001`, `TEREMT-001` (`_TORZSCIKK.md`). **Ez ⛔ az integrátornak: ezt a jelentés nem hajtja végre.**

**Külön észrevétel (nem a kérdés része, nem javítottam):** a Strong → LSJ hozzárendelésben a mintákban van téves (a szócikk végén más lemma szócikke áll: G1390 δόμα / δῶμα, G1650 ἔλεγχος / ἐν). Az 5 523 sor teljes átvizsgálása nem történt meg; ha az LSJ-szövegből valamelyik lap idézne, azt a hely szerint kell ellenőrizni.

## 7. Korlátok és ami nincs bizonyítva

- A lánc **Perseus → Eliran Wong modulja** csak a szöveg egyezéséből bizonyított, nem a modul készítőjének nyilatkozatából. Az LSJ szövegének ugyanezen az átdolgozáson kívüli, más (nem-Perseus) forrásból származó példánya nem zárható ki, de a Perseus-féle jelölés (pl. a `g[uglide]el` jellegű átírások, az azonos görög szöveg a hosszúságjelekkel együtt) a Perseus-szöveget jelzi.
- A 2025-09-24-i, a mappát érintő commit előtti Perseus-változatot nem néztem; a modul készülte (a beemelés 2026-09-07) ezután van.
- A mérés a Beta-kód → Unicode átalakítón és a párosítási heurisztikán múlik; az osztályhatárok (99%, 97%, 50%) saját választásúak. A számok nagyságrendileg megbízhatóak (a T2+T2b ±1–2 százalékpont), egy-egy szócikk besorolása nem.
- A modul-oldali pótszöveg eredete (Strong's-lexikon-mondat) csak a minták alapján állítható, a teljes forrásuk nem azonosítva.
- Az összevető szkriptek a scratchpadben maradtak, a repóba nem kerültek; az ismétléshez a jelentés 2. pontja leírja a lépéseket. A szkriptek másolata a munkamenetek közös jegyzet-mappájában van.
