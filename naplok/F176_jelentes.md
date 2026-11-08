# F176 jelentés — a visszhang-réteg adatrétege

*FELADATOK #176 · végrehajtó modell: claude-sonnet-5-5 (a kért: sonnet; egyezik) · ág: `claude/f176-visszhang-adat-c1579f` · 2026-11-08*

A lexikonlap és a `lexikon_general.py` **nem változott**, újragenerálás (lap) nem történt. A `fuggetlen-ellenor` nem futott;
a fejléc `allapot` értékét a végrehajtó nem állítja `lezarva`-ra.

## 0. Összefoglaló

| | |
|---|---|
| Mérce | „kimenetbe tehető” (NC kizáró; közkincs, CC0, CC BY mehet). Az elsődleges helyeken minden licencet újraellenőriztem; **egyik sem NC vagy BY-SA, egyik sem tért el a várttól — ⛔ nem történt.** |
| Táblák | Targum_PD 15 142 sor · Vulgata_Clementina 31 434 sor · SBLGNT_apparatus 6 934 sor · TAGNT_valtozatok 11 777 sor · BDB_rokon_irasok 5 sor (HAMART-001 első futás; az egybetűs szír token kiszűrve, F176.8) |
| Eltérés / figyelmeztetés | (1) A Sefaria ÁSZF kereskedelmi-használati mondata miatt a két Sefaria-eredetű tábla előbb `kereskedelmi=feltetelesen` volt; a DT-F176b döntéssel (a felhasználó, 2026-11-08) `igen`; (2) a Sefaria lexikon-adatán nincs licencmező (BDB); (3) a versszámozás-feloldás nincs elvégezve (DT-F176a); (4) a `nyilt_mag/` csomagot újra kellett generálni (l. 5.) |
| Kapu | `nyilt_mag_kapu.py`: 0 BUKÁS; a mai nyílt magra az ARANY ellenőrzés egyetlen forrást jelez 1% felett: BDB 131 / 8 099 = 1,62% (FIGYELMEZTETÉS) |

## 1. Licencellenőrzés (F176.1)

Lekérések: 2026-11-08; azonosító User-Agent `PaRDeS-research/1.0`, felhasználói e-mail nélkül; ≥ 1 s a kérések között.
A nyers letöltés a repón kívül, forrásonként új, üres könyvtárban maradt; a konverziót `python -I` olvasta.

### 1.1 Sefaria — felhasználási feltételek (az F176.3 előfeltétele)

Elsődleges hely: https://www.sefaria.org/terms (a közzétett Google-dokumentum:
`docs.google.com/document/d/e/2PACX-1vQHQfHUVMNugNyPyJRucHa9cEU9VUdFD8DAcLFAsUmBORodDmIO2YG85-m01OtF3FUlIgmaSxW_YWSc/pub`),
„Sefaria, Inc. Terms of Use — Last Updated: April 15, 2026”. A releváns mondatok szó szerint:

- „You may download our data directly from the Sefaria Data GitHub Repository at https://github.com/Sefaria/Sefaria-Export or by learning about our API on our developers site.”
- „However, any exploitation of the Service or its Content for any commercial use is strictly prohibited without our express, prior written consent, unless expressly stated otherwise.”
- „Any use of data mining, screen-scraping, robots, or similar data gathering and extraction systems, techniques, or code bases whose primary purpose is simply to crawl the Service for its Content is strictly prohibited.”
- „Engaging in automated uses of the Service that are abusive or disruptive of the services;” (a tiltott magatartások listájából)
- „Reuse of Content that we host is welcome, though exceptions exist (1) for Content contributed under "fair use" or similar exemptions under copyright law and (2) per these Terms of Use. Any reuse must comply with the underlying license(s).”

Az API-doksi (https://developers.sefaria.org) külön felhasználási feltételt vagy rátakorlátot nem közöl. A Sefaria-Export README:
a szövegek ~26 GB-os nyilvános tárolóban vannak, „can be downloaded without authentication”.

**Értékelés (⛔ 4.):** az ÁSZF az **adatletöltést a Sefaria-Exportból és az API-t kifejezetten megengedi**; tiltja a Szolgáltatás
tartalmának tömeges bejárását (crawl) és a visszaélésszerű automatizált használatot. Amit tettünk: a Targum-szövegek a
Sefaria-Exportból (nem az API-ból) jöttek, 26 fájl + a `books.json`, ≥ 1 s közökkel; az API-t 27 `texts/versions` hívás (a
`license` mező ellenőrzésére), a BDB-gyorsítótár építő futása 10 `words` hívás, a hibakeresés további kb. 15 kézi `words` hívás érte, ≥ 1 s közökkel. Ez nem bejárás és nem terheli a szolgáltatást,
tehát az ÁSZF **nem tiltja** — ⛔ nem lépett életbe. A **kereskedelmi használatra** vonatkozó mondat („unless expressly stated
otherwise”) értelmezése nyitott: a verziónkénti `Public Domain` jelölés kifejezett nyilatkozatnak tekinthető, de jogi
véleményt nem adok. Ezért a végrehajtó a `Targum_PD`-t és a `BDB_rokon_irasok`-at először `kereskedelmi=feltetelesen` értékkel vette fel (DT-F176b).

**Döntés (DT-F176b, 2026-11-08, a felhasználó):** „szerintem ez az irányadó” (arra, hogy „a tartalom közkincs, és a szerzői jog szerint senki nem korlátozhatja”); a javaslatra: „mehet”. A két tábla `kereskedelmi=igen` (engedett), a nyílt mag szempontjából is engedett. Indok: a tartalom közkincs, a Sefaria nem szerzője, és nem licencelheti; a Targum-verziók „Public Domain” licencmezője az ÁSZF kereskedelmi tiltásának „unless expressly stated otherwise” kivételeként olvasandó; a BDB-nél, ahol nincs licencmező, a közkincs-állítás az 1906-os kiadáson alapul; a letöltés útja (Sefaria-Export / API) az ÁSZF szerint megengedett. A döntés a Sefaria kapcsolattáblára (tanúréteg, a Sefaria saját munkája) NEM vonatkozik. Átvezetve: F176.6 (licencek.tsv, README), F176.6b (`nyilt_mag/` újragenerálás).

### 1.2 Targum (Sefaria-Export) — `Targum_PD.tsv`

- **Elsődleges hely:** Sefaria-Export `LICENSE.md` (https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/LICENSE.md): „Each text is licensed separately, so there is no overall license for this repository.” / „You can find the license for each text in their JSON versions under the `license` field. This is generally either "Public Domain", "CC0", "CC-BY", "CC-BY-SA" or "CC-BY-NC".”
- **Verziónként** (a JSON-ok saját `license` mezője és az API `texts/versions` válasza egyezik): mind a 26 verzió `"license": "Public Domain"`. Onkelos: `versionTitle` „Onkelos <Könyv>”, `versionSource` http://toratemetfreeware.com/; Jonatán: `versionTitle` „Mikraot Gedolot”, `versionSource` https://www.sefaria.org (a Zechariah-fájlé: „Mikraot Gedolot”). A `merged` fájl nem használt.
- **Kimaradt (a kért szabály szerint):** az Onkelos Genesis jemeni (Taj) verziója — `CC-BY-SA`; a Metsudah — `CC-BY-NC`; az angol fordítások (köztük egy `unknown`). Az Onkelos Genesis-listán (API `versions`) a magyar-célú héber/arám verziók közül csak a `Public Domain` jelölésű lett letöltve.
- A 26 fájl: cím · versionTitle · licenc · fájl SHA-256 (a lista SHA-256-ja: `8e6bc36039345b256601c0d20d1960b2804051d6785270ca962fe790308ff115`; `books.json`: `e5784fcf2ece785e2137ad4411c101839ada49a6ed1930b1af7b3d4510d20361`, 21 824 152 bájt):

| cím | versionTitle | license | sha256 |
|---|---|---|---|
| Onkelos Deuteronomy | Onkelos Deuteronomy | Public Domain | `e45770c06acc59a5524efea298d213f81d531c5182d13b444d9995fa3dacf5e0` |
| Onkelos Exodus | Onkelos Exodus | Public Domain | `58965f70188de972cc13ebde03d6fbe5b299c249471610c7c717663de279a09f` |
| Onkelos Genesis | Onkelos Genesis | Public Domain | `d35c944077d33238bba5e6de40808ee68a7cffd1f64c0ca8d1f632d469ab7cf4` |
| Onkelos Leviticus | Onkelos Leviticus | Public Domain | `47b555fa6fabbbdda8f7c452287c7f1ac51f52c6e67befa78fb9bbd085865764` |
| Onkelos Numbers | Onkelos Numbers | Public Domain | `208ccd843fe8507d11e09ea1057db55875d052435bff0d1f09f73c95bc63185d` |
| Targum Jonathan on Amos | Mikraot Gedolot | Public Domain | `ec16df1bce7fef9e68ef995a9b0d440a1be63774f2c45d5e357dccf48ae11dda` |
| Targum Jonathan on Ezekiel | Mikraot Gedolot | Public Domain | `19888c9590967b6b6c22acf9605dc3149f435b810ad278ec7db045808a2d63da` |
| Targum Jonathan on Habakkuk | Mikraot Gedolot | Public Domain | `0af0ac4919aa6ddbe38a99abaafaccfaffdd7038994f3fd4c319864f1af2698a` |
| Targum Jonathan on Haggai | Mikraot Gedolot | Public Domain | `a5aee86c9af44ffc93366769d28c85b2a8f6fa0da50e9f736af4c1f2fe3ee4e0` |
| Targum Jonathan on Hosea | Mikraot Gedolot | Public Domain | `1ef94d34740cb3e681443a4ebe95b1f0d802fa8ae94d02a21bf188353683c71b` |
| Targum Jonathan on II Kings | Mikraot Gedolot | Public Domain | `a6b229569fb0fe1c57979db8086de474b7ef66e9dd52055f638ef0b54c8523c6` |
| Targum Jonathan on II Samuel | Mikraot Gedolot | Public Domain | `4c59b69429a88f1d3bc19f00d30b3d95f3f0361d66de508296a850cd9d07256b` |
| Targum Jonathan on I Kings | Mikraot Gedolot | Public Domain | `9cdfee3625701efbd0bccb20cd1160e14ca50b7b0a755c5f20bd8d7931f0fb7d` |
| Targum Jonathan on I Samuel | Mikraot Gedolot | Public Domain | `52959286d21f7b365cd192fa6ece650730ba3aed9cb084896627a96cb48279fa` |
| Targum Jonathan on Isaiah | Mikraot Gedolot | Public Domain | `b6bf6c4bbfea3526841779fc47595df11e63f14e1392fc2e51ce39035e10c2b6` |
| Targum Jonathan on Jeremiah | Mikraot Gedolot | Public Domain | `d6fa71be33e3138275695d2688340137a5e31b797de43d88994951f1a76f6364` |
| Targum Jonathan on Joel | Mikraot Gedolot | Public Domain | `059b54cdb732d9b6cd6e5c81fec8581fe69ce27f1e3c10ea6a969bdfd755429d` |
| Targum Jonathan on Jonah | Mikraot Gedolot | Public Domain | `b89d633f4feaf47572a248b7da002b146a8b2c5a79a420b1305e351992209dc3` |
| Targum Jonathan on Joshua | Mikraot Gedolot | Public Domain | `0b81b9f29c228816201b1d1296e1f25bdee368662dee4f98fc6cf85fc5fed2d6` |
| Targum Jonathan on Judges | Mikraot Gedolot | Public Domain | `41454a73658175ca6e01e3cfe5ac5cb781791fcc6602b137e50eb2223b357fe3` |
| Targum Jonathan on Malachi | Mikraot Gedolot | Public Domain | `9516b1268a5ab392d9241d1cbf0b2ce3af34f6ba6c1239e639b39a03d6eae3ce` |
| Targum Jonathan on Micah | Mikraot Gedolot | Public Domain | `87d415684c3a13d3243eb156e30ad7e227e58681831400effff038f7ac927a0f` |
| Targum Jonathan on Nahum | Mikraot Gedolot | Public Domain | `1c62743e98795ca4c0605c460db18f96d1b7ad465f2711eb58fdc2742c645311` |
| Targum Jonathan on Obadiah | Mikraot Gedolot | Public Domain | `ae75199ca584a37516db4f9bfa63ffd97de5e2669b08412bb3615af8f4ae5c21` |
| Targum Jonathan on Zechariah | Mikraot Gedolot | Public Domain | `723df1ef6cd96f7bf76a5b7e5d440e0495195a1869db81b3cc172fb82285ac70` |
| Targum Jonathan on Zephaniah | Mikraot Gedolot | Public Domain | `80deb8853efe81cc71d091af45e294c70926bc27d9d680b514e7b710b43ea978` |

### 1.3 Vulgata (eBible `latVUC`) — `Vulgata_Clementina.tsv`

- **Elsődleges hely:** https://ebible.org/latVUC/copr.htm és `copyright.htm`; a zip saját `copr.htm`-je azonos: „Bibbia Vulgata Clementina na 1598”; „Clementine Vulgate of 1598 with Glossa Ordinaria Migne edition 1880 in Latin”; „Public Domain”.
- **Kiadás-azonosítás:** a csomag az eBible megnevezése szerint „Clementine Vulgate of 1598”, a Glossa Ordinaria (Migne, 1880) lábjegyzeteivel; a lábjegyzetek (12 968) nem kerültek át. A kiadásról (1592/1598/1880) **nem döntöttem**, a tábla az eBible megjelölését hordozza (tartalmi kérdés, ha lap-szintű kiadás-hivatkozás kell: N-F176a).
- **Fájl:** `latVUC_usfm.zip`, SHA-256 `5d73ce3473e40b70cfcc976b967e0f259cbb031d6c0cd4f9798fbabf9f5b4e6c`, 3 554 568 bájt, bejegyzések 2026-10-29.

### 1.4 SBLGNT apparátus — `SBLGNT_apparatus.tsv`

- **Elsődleges hely:** github.com/LogosBible/SBLGNT @ `d7f35adca9ec410e1d1499c63b4dd989d76c8d4d`: `README.md` — „The SBLGNT is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).”; „Copyright 2010 by the [Society of Biblical Literature](https://sbl-site.org/) and [Logos Bible Software](https://www.logos.com/).”; verziótörténet: „v1.1 2022-12-19 Update public version and license on github”. `LICENSE` (SHA-256 `7e7170e3cebf88a9f60c7b8421418323c09304da1af4d5e90f4da1dc1c8a2661`, 18 650 bájt): „Attribution 4.0 International” (a CC BY 4.0 teljes szövege). https://sblgnt.com/license/ („SBL Greek New Testament - End User License Agreement”): „Creative Commons Attribution 4.0 International Public License”. A relicencelés commitjai: `1db394956decded8fd6d228dcdf37145e7297715` (2022-12-19), PR #1 merge `7200631022206cb7c7a76c6106ad687dcca0759c` (2023-01-09).
- **Az apparátus** a `data/sblgntapp/` könyvtárból jön, ugyanabban a CC BY 4.0 repóban (a repó README-je és LICENSE-fájlja a repó egészére vonatkozik; az apparátus-könyvtárban külön licenc-fájl nincs).
- **A korábbi EULA archiválása** (a relicencelés előtti állapot, commit `a785c74fa38fc5d36a16f7cbb36960dff5364cc4`, `LICENSE.md`, SHA-256 `0d8bcbbcbbaf16a6339155de623a74d8180cd9dbfc5fbd498214cbf84affbe07`, 2 101 bájt) — **már nem hatályos**, csak dokumentáció:

```
# End User License Agreement

SBL Greek New Testament

Copyright 2010 by the [Society of Biblical Literature](https://sbl-site.org/) and [Logos Bible Software](https://www.logos.com/).

You may freely distribute the SBL Greek New Testament (SBLGNT), but you are not permitted to sell it on its own, either in print or electronic format.

If the SBLGNT constitutes less than 25 percent of the content of a larger print or electronic work, you may sell it as part of that work.
If the SBLGNT will constitute more than 25 percent of the content of a larger print or electronic work that you wish to sell, you must secure written permission or secure a licensing agreement to do so prior to publication.
All permissions and licensing requests should be addressed to:

```
Rights and Permissions Office
Society of Biblical Literature
825 Houston Mill Road, Suite 350
Atlanta, GA 30329 USA
```

If you give away the SBLGNT for use with a commercial product or sell a print or electronic work containing more than 500 verses from the SBLGNT, you must annually report the number of units sold, distributed, and/or downloaded to the Society of Biblical Literature’s Rights and Permissions Office.

You must always attribute quotations from the SBLGNT.
If you quote fewer than 100 verses of the SBLGNT in a single print or electronic work, you can attribute it by simply adding "SBLGNT" after the quotation.
Use of 100 or more verses in a single work must be accompanied by the following statement:

> Scripture quotations marked SBLGNT are from the SBL Greek New Testament.
> Copyright © 2010 Society of Biblical Literature and Logos Bible Software.

With online or electronic quotations, link "SBLGNT" and "SBL Greek New Testament" to https://sblgnt.com, "Society of Biblical Literature" to https://www.sbl-site.org, and "Logos Bible Software" to https://www.logos.com.

The SBLGNT may not be used in a Greek-English diglot without a license, regardless of whether such work will be sold or given away.
Diglots containing the SBLGNT and a language other than English may be produced for free distribution.
```

### 1.5 TAGNT — `TAGNT_valtozatok.tsv`

- **Elsődleges hely:** a nyers fájlok fejléce (STEPBible-Data @ `5de0a47f35f0fc13dfe1430d104e5db8a4285f9c`, 2026-11-08): „Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)”; „Include any part of this data in software or publications and send it to AI servers  without requesting permission”; „Attribute the data to Tyndale House and STEPBible.org, and include a link to STEPBible.github.io/STEPBible-Data as the source of this data.”; „Please do not post copies of this data file elsewhere, so that this remains the single up-to-date source”. (A korábbi, `licencek.tsv`-beli TAGNT-sor idézete még a „Please do not redistribute it yourself.” mondatot tartalmazta; a mai fejléc ezt a fenti mondatra cserélte. A tábla kivonat, nem másolat; a THGNT szövege nem jött át.)
- SHA-256: `TAGNT Mat-Jhn` `d4c0c820fdf9f2b450c9f96ce6103d6875028affd2e44094d753f1329ca1fd85` (14 188 364 bájt), `TAGNT Act-Rev` `122040eeeaeba50d6abbf67b39cacaff687211bda69b080e5d53927c830d9968` (15 938 967 bájt).

### 1.6 BDB rokon írások (Sefaria „BDB Dictionary”, „BDB Aramaic Dictionary”)

- **Licencmező nincs:** a Sefaria lexikon-modelljében (`sefaria/model/lexicon.py`) nincs licenc-attribútum; az API `parent_lexicon_details`: `name, language, to_language, text_categories, source, attribution, index_title, version_title, version_lang`. `attribution`: „F. Brown, S. Driver & C. Briggs”; `version_title`: „A Hebrew and English lexicon of the Old Testament, by Francis Brown. With the co-operation of S. R. Driver and Charles A. Briggs. Oxford, 1906”. A brief „közkincs (licencmező)” várakozása tehát **nem igazolható licencmezőből**; a közkincs-státusz a mű korán (1906) alapul, ahogy a repó BDB-sora (DT-F33g). Ez nem NC és nem BY-SA, ezért nem állítottam meg (⛔ 3. a „NC / BY-SA / eltér” esetre szól; itt a hiányzó mező kérdése DT-F176b-be került).

### 1.7 Eredmény

Minden licenc egyezik a várttal (közkincs, közkincs, CC BY 4.0, CC BY 4.0, közkincs), kivéve a fenti két megjegyzést (1.1 kereskedelmi mondat; 1.6 hiányzó licencmező). NC/BY-SA tétel nem került be.

## 2. Adatkészletek (F176.2)

SHA-256 és sorszám: `konkordancia/VISSZHANG_README.md` 1. szakasza (gépi olvasású tábla; a `teszt_visszhang.py` a sorszámot ellenőrzi).

| Tábla | Sorok | SHA-256 | `forras_kulcs=nem` |
|---|---|---|---|
| Targum_PD.tsv | 15 142 | `ef320a5fc30d02a59ae0cdd5f00142eaec7d272501c95872278206afa7f396c8` | 96 |
| Vulgata_Clementina.tsv | 31 434 | `83ec4780d8a188375698773ea2206864033ba6b159c0c65c2c1b913552300915` | 1 269 |
| SBLGNT_apparatus.tsv | 6 934 | `63f3af16a91bdf3ef5a0911185459273045cada9aead13a33a16c509fdbf7daf` | 1 |
| TAGNT_valtozatok.tsv | 11 777 | `c7261e19591f6432f1b1c229a9ffaa726dec5316b970513a76ca3fd70d40ebd7` | 0 |
| BDB_rokon_irasok.tsv | 5 | l. 3. (gyorsítótár, nő) | — |

- **Targum:** 15 142 vers = Onkelos 5 846 vers (5 könyv) + Jonatán 9 296 vers (21 könyv); saját mérés a `targum` oszlopból (az ellenőr mérése ugyanezt adta); üres vers 0; HTML-jelölés 0.
- **Vulgata:** 66 kanonikus könyv, 31 434 vers; kimaradt: TOB, JDT, WIS, SIR, BAR, 1MA, 2MA.
- **SBLGNT:** 27 fájl, 6 934 jegyzet; a 27 könyvcím-blokk kimarad.
- **TAGNT:** 142 095 szóból 11 777 (11 773, ahol a kiadás-jelölő nem teljes + 4 NKO-tól eltérő típusú, de teljes halmazú); 4 csak-Tyn szó: a `gorog` mező üres.
- **Versszámozás (nincs némán javítva).** Az `igehely` a forrás fejezet:versét hordozza, a `forras_vers`/`forras_ref` változatlanul; a `forras_kulcs` csak a kulcs **létezését** jelzi a `Karoli_1908.tsv`-ben. Mért hézag: Targum `nem` 96 sor (pl. Jóel 4: 21, 4Móz 17: 15, 1Kir 5: 14, 2Móz 7: 4, Mal 3: 6, Hós 2: 3, Zak 2: 4); Vulgata `nem` 1 269 sor (Zsolt 786, Dán 174, JSir 154, Eszter 108, Jób 15, Préd 10, …); SBLGNT 1. **A „létezik” nem „azonos vers”:** pl. Jóel 3 a Targumban az MT 3 (= Károli Jóel 2:28–32), a Vulgata zsoltárai egyaránt a Vulgata-számozással szerepelnek. A feloldás tartalmi döntés (DT-F176a).

## 3. BDB rokon írások — HAMART-001 első futás (F176.3)

Parancs: `python -I eszkozok/visszhang/bdb_rokon.py --strong H0779 H0127 H6093 H2403 H2555 H7843 H6975 H1863`; 10 HTTP-kérés (a H6093 és H0779 második alakot is kért); a második futás **0** kérés (gyorsítótár).
A Sefaria `/api/words` a **szóalak-indexben** keres (nem fejszóban): az `ארר` fejszóra nincs találat, az `ארור` alakra van. Ezért a szkript a fejszó után a `TAHOT_kivonat.tsv` leggyakoribb alakjait is próbálja.

| Strong | próbált alakok | BDB-szócikk | rokon írás | megjegyzés |
|---|---|---|---|---|
| H0127 | אדמה | 1 | 2 (arab: أَدَمَة, دَمَّ) | |
| H0779 | ארר, ארור | 1 | 0 | a szócikkben nincs nem-latin, nem-héber írású token |
| H1863 | דרדר | **0** | 0 | **a Sefaria nem adott BDB-szócikket** (a repó BDB-szövegében „Arabic ,” áll: itt a szócikk megvan, de nem érhető el); a „nincs rokon írás” nem állítható |
| H2403 | חטאת | 2 | 0 | |
| H2555 | חמס | 1 | 0 | elvárt: nincs rokon szó — egyezik |
| H6093 | עצבון, עצבונ | **0** | 0 | elvárt: nincs rokon szó — az eredmény egyezik, de oka az, hogy a Sefaria **nem adott szócikket** (nem az, hogy a szócikk üres) |
| H6975 | קוץ | 2 | 0 | elvárt: nincs rokon szó — egyezik |
| H7843 | שחת | 1 | 3 (arab سَحَتَ; etióp ሰሐጠ; szír ܫܰܚܶܛ; az egybetűs „ܬ” kiszűrve, F176.8) | **elvárt: arab, etióp és szír — egyezik** |

Ellenpróba a briefhez képest: a H7843 mindhárom írással megvan; a H2555 és H6975 szócikke megvan, rokon írás nélkül; a H6093 és a H1863 esetében a Sefaria szóalak-keresése **nem talál szócikket**, ezért ott a „nincs” hiányt jelent, nem negatív leletet (CLAUDE.md 3. szabály: a hiányt nem töltöm ki). A `# lekérdezve:` fejlécsorok `bdb_szócikk=0` értéke ezt jelöli.

Megjegyzés a kontextusról: az `kontextus` oszlop a szócikk szövegéből vett ≤ 120 karakteres ablak (a token körül), nem a BDB-fej elejéről; a BDB-szövegben a rokon szavak a fej-részben állnak, de a Sefaria-szócikk szerkezete miatt az ablak a tokenhez igazodik.

## 4. Arány-kapu (F176.4)

- Megvalósítás: `eszkozok/nyilt_mag_kapu.py`, `ARANY` ellenőrzés. Forrásonként kiírja: `<forrás>: <nyílt mag tételei> / <forrás tételszáma> = <arány>%`. **1% felett FIGYELMEZTETÉS** (átnézés a következő kiadás előtt), **5% felett BUKÁS** (a kapu megáll; további átvétel a felhasználó döntésével vagy ügyvédi vélemény után). A határérték maga (1,0%, 5,0%) még nem lépi át a küszöböt.
- A **forrás tételszáma nincs kódba írva**: a `konkordancia/VISSZHANG_README.md` gépi olvasású tábláján vagy az `adat/datasetek.tsv` `fajl` oszlopán át a fájl adatsorainak száma.
- A nyílt mag tétele: az `elofordulasok.tsv` sora, amelynek `forras_dataset` (`;`-vel tagolt) vagy `szotar` oszlopa a forrást nevezi (sor, nem egyedi forrástétel: felső becslés).
- **A küszöbök indoka:** óvatos mérnöki értékek, **jogi alapjuk nincs** (a #86 terv 6. szakasz 13. pontja).
- Mai kimenet (jelzés-szint): BDB 131 / 8 099 = 1,62% (**FIGYELMEZTETÉS** — a meglévő nyílt mag BDB-hivatkozásai; nem az új források); TAGNT 3 / 142 096; TAHOT 4 / 469 300; Thayer 20 / 5 426 = 0,37%; TBESG 6 / ? (a tételszám nem állapítható meg: nincs a `datasetek.tsv`-ben; **FIGYELMEZTETÉS** az F176.9 óta); a visszhang-források (Targum_PD, Vulgata_Clementina, SBLGNT_apparatus, TAGNT_valtozatok, BDB_rokon_irasok) 0%.
- Teszt: `eszkozok/teszt_visszhang.py` (0,5% → rendben; 2% → FIGYELMEZTETÉS; 6% → BUKÁS; 1,0% és 5,0% nem lép át; a gyorsítótár második futása nem kér le újra).

## 5. A `nyilt_mag/` csomag újragenerálása (hatókör-megjegyzés)

A `licencek.tsv` új sorai a generált nyílt mag `forrasok_es_licencek.tsv`-jét változtatják (az export minden licenc-sort kiírja), ezért a `nyilt_mag_kapu.py` BAJTAZONOS-ellenőrzése a régi csomagon BUKÁST adott (10 db). A `nyilt_mag/` **nem szerepel a brief `ir` mezőjében**; a kész-kritériumhoz (`nyilt_mag_kapu.py` zöld) mégis újra kellett generálni (`python eszkozok/nyilt_mag_export.py`; változás: 5 új sor a `forrasok_es_licencek.tsv`-ben, az ELLENORZO_OSSZEG/KIADAS/RELEASE/OLVASSEL/README hash- és kizárt-lista sora). Külön commitban (`F176.4b`), így az orkesztrátor külön visszavonhatja; a mechanikus következmény a licenc-sor, nem tartalmi döntés. Mind az öt új forrás (`Targum_PD`, `BDB_rokon_irasok`, `Vulgata_Clementina`, `SBLGNT_apparatus`, `TAGNT_valtozatok`) „engedett, de a csomag nem használja” (a `Targum_PD` és a `BDB_rokon_irasok` a DT-F176b döntés után, `kereskedelmi=igen`), a `nyilt_mag/forrasok_es_licencek.tsv` szerint.

## 6. Ellenőrzések kimenete

A végső futás (a javítókör 2/2 minden adat- és kódjavítása után, a jelentés commitja előtt; friss kimenet, 2026-11-08):

```
$ python eszkozok/ellenoriz.py
RENDBEN: 25 | SÉRTÉS: 0 | KÉZI: 2 | JELENTÉS: 10          (kilépési kód 0; az alapállapot a main-en azonos)

$ python eszkozok/teszt_visszhang.py
Ran 20 tests in 5.374s
OK                                                         (kilépési kód 0)

$ python eszkozok/nyilt_mag_kapu.py                        (újragenerálás nélkül; bajtazonos ellenőrzés zöld)
ARANY  BDB: 131 / 8099 = 1.62%
ARANY  BDB_rokon_irasok: 0 / 5 = 0.00%
ARANY  SBLGNT_apparatus: 0 / 6934 = 0.00%
ARANY  TAGNT: 3 / 142096 = 0.00%
ARANY  TAGNT_valtozatok: 0 / 11777 = 0.00%
ARANY  TAHOT: 4 / 469300 = 0.00%
ARANY  TBESG: 6 / ? (a forrás tételszáma nem állapítható meg)
ARANY  Targum_PD: 0 / 15142 = 0.00%
ARANY  Thayer: 20 / 5426 = 0.37%
ARANY  Vulgata_Clementina: 0 / 31434 = 0.00%
nyílt mag kapu: 0 BUKÁS, 19 FIGYELMEZTETÉS                 (kilépési kód 0; 17 meglévő KJV/angol-funkciószó figyelmeztetés + BDB 1,62% > 1% + TBESG tételszám ismeretlen)

$ python eszkozok/feladatok.py ellenoriz
190 brief, 0 hiba, 0 figyelmeztetés                        (kilépési kód 0)

$ python eszkozok/teszt_nyilt_mag.py
Ran 59 tests in 172.518s
OK                                                         (kilépési kód 0)

$ python eszkozok/ellenorzes/futtat.py --valtozott <a main-hez képesti diff fájljai> --diff-alap origin/main --diff-fej HEAD
E32: 0 találat (a három DT-F176a hiba megszűnt)
E26: HIBA 1 -- naplok/ELLENOR_F176_2.md:21 (a független ellenőr jelentése említi a „DT630” számot; a jelentés változatlan marad, nem szerkeszthető)
E30: 5 FIGYELMEZTETÉS (köztük 301456c7 „vesz” = DT-F176f, és ennek a körnek két commit-üzenete: 097a932b, 6a2413e8; a kimenet csak hármat sorol fel)
E25: 3, E27: 42, E34: 45 (mind régi, a main-en is meglévő jelentés-szintű találat); a többi ellenőrzés 0
kilépési kód 1                                             (az E26 HIBA miatt)
```

Egyéb meglévő tesztek, amelyek a változtatott fájlokat érintik: `teszt_nyilt_mag.py` 59 teszt OK; `teszt_ellenoriz_30/31/32/33/35.py` OK.

## 7. Nyitott kérdések (helyőrzők: `dontesek/uj/f176-visszhang-adat-c1579f.md`, `nyitott/uj/f176-visszhang-adat-c1579f.md`)

- **DT-F176a — versszámozás-feloldás.** 🟢 Eldöntve (az orkesztrátor döntése a felhasználó felhatalmazásával („a 176 döntését hozd meg”, 2026-11-08)): (a) — a források saját számozása marad, a Károli-feloldás nézetoldali (versmegfeleltetés, lapszerkezeti generátor-kör); a `karoli_kulcs` oszlop `forras_kulcs` néven csak a szám létezését jelzi (F176.12). Hamis egyezések (ELLENOR_F176 2.): Vulgata Zsolt 22:1 = Károli Zsolt 23:1; Targum Jóel 3:1 = Károli Jóel 2:28; Vulgata Dán 3:24 Azariás-kiegészítés.
- **DT-F176c — a Sefaria-feltételeknél elmaradt megállás (ELLENOR_F176 1.).** 🟢 az orkesztrátor döntése a felhasználó felhatalmazásával („a 176 döntését hozd meg”, 2026-11-08): elfogadva, utólag a DT-F176b rendezte.
- **DT-F176d — a licenc-commit az adatcommit után (ELLENOR_F176 3.).** 🟢 az orkesztrátor döntése a felhasználó felhatalmazásával („a 176 döntését hozd meg”, 2026-11-08): elfogadva (egyik licenc sem lett NC/BY-SA, a kizárás a kódban volt), történet-átírás nincs.
- **DT-F176e — a `kontextus` a token körüli szövegrész (ELLENOR_F176 7.).** 🟢 az orkesztrátor döntése a felhasználó felhatalmazásával („a 176 döntését hozd meg”, 2026-11-08): a token körüli szövegrész marad, mert az mutatja a rokon szót; az indok a `SEMA.md`-ben és a `VISSZHANG_README.md`-ben.
- **DT-F176f — a `301456c7` commit üzenetében ékezet nélküli „vesz” (ELLENOR_F176_2 5.).** 🟢 az orkesztrátor döntése a felhasználó felhatalmazásával („176 mehet a döntésed szerint”, 2026-11-08): elfogadva, történet-átírás nincs.
- **DT-F176b — a Sefaria-eredetű források kereskedelmi használata.** 🟢 Eldöntve (a felhasználó, 2026-11-08): `kereskedelmi=igen`, l. 1.1.
- **N-F176a — a Vulgata-kiadás megjelölése a lapon** (Clementina 1598 az eBible megnevezése szerint; a Glossa Ordinaria — 12 968 lábjegyzet, nincs átvéve — külön recepciós forrás lehet).
- **N-F176b — a BDB-keresés hézagai.** A Sefaria szóalak-indexe a H1863 és a H6093 szócikkét nem adja; addig a „nincs rokon írás” ezekre nem állítható.
- **N-F176c — a `teszt_visszhang.py` nincs a CI teszt-listájában** (a workflow nem az `ir` mezőben van).
