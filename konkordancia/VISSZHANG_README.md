# A visszhang-réteg adatkészletei (F176, FELADATOK #176)

A lexikonlap „visszhang” rétegének **adatai**: ókori fordítások (Targum, Vulgata), az ÚSZ kritikai apparátusa és
szövegváltozat-jelölése, valamint a BDB rokon nyelvi írásainak gyorsítótára. Ez a dokumentum az öt tábla leírása,
licenc-igazolása és újragenerálása. **A lexikonlap ebben a körben nem változott** (a `lexikon_general.py`
érintetlen); a lapra írás külön feladat.

*Mérce: „kimenetbe tehető” (fizetős lexikonlap és a Zenodón közzétett nyílt mag). NC licenc kizáró ok; közkincs,
CC0, CC BY mehet (CC BY-nál a forrásmegnevezés kötelező); CC BY-SA és GPL ebbe a körbe nem került.*

## 1. Táblák és tételszámok (gépi olvasású tábla — a `nyilt_mag_kapu.py` ARANY ellenőrzése innen olvassa a tételszámot)

A `tetel` oszlop az adatsorok száma (a `#` sorok és az oszlopfejléc nélkül); `sor` = a tételszám futáskor a fájlból
számolódik (a gyorsítótár nő). A `sha256` a repóbeli fájl SHA-256-ja a rögzítéskor (a `teszt_visszhang.py` a
sorszámot ellenőrzi, a hash-t a generátor újrafuttatása igazolja).

| dataset | fajl | tetel | sha256 | licenc |
|---|---|---|---|---|
| Targum_PD | konkordancia/Targum_PD.tsv | 15142 | 745656cdd22424fc445e3bb12a7577f16f09c3cb10c5b1fb23013cd9e1dbc605 | közkincs (Sefaria `license`: Public Domain, verziónként) |
| Vulgata_Clementina | konkordancia/Vulgata_Clementina.tsv | 31434 | f19e90be193ad94201bbedc893246ca304d661597a770abc084d53b89d02986e | közkincs (eBible: Public Domain) |
| SBLGNT_apparatus | konkordancia/SBLGNT_apparatus.tsv | 6934 | caad1eff83341840838ebcfd8883762322a7f3da8149da0945c1d56ff86ea048 | CC BY 4.0 |
| TAGNT_valtozatok | konkordancia/TAGNT_valtozatok.tsv | 11777 | df1c7de3f03c92bba54e035d1f4ef82b99f0143a5f7488a4b65907ff7cb94848 | CC BY 4.0 |
| BDB_rokon_irasok | konkordancia/BDB_rokon_irasok.tsv | sor | gyorsítótár, nő | közkincs (BDB, 1906; DT-F33g) |

Közös szabály mind az öt táblára: **a versszámozás a forrás saját számozása**. Az `igehely` oszlop a magyar
könyvrövidítés (a `Konyv_normalizalo_tabla.tsv` szerint) és a forrás fejezet:verse; **Károli-átszámozás nincs**
(MT ↔ Károli, Vulgata ↔ Károli, NRSV ↔ Károli feloldása tartalmi döntés, DT-F176a). A `forras_vers` / `forras_ref`
oszlop a forrás hivatkozását változatlanul őrzi. **Az `igehely` a forrás saját számozása (magyar könyvnévvel), nem
Károli-vers.** A `forras_kulcs` (`igen` | `nem`) oszlop csak azt jelzi, hogy ugyanez a fejezet:vers szám **létezik-e** a
`Karoli_1908.tsv`-ben; versegyezést nem állít (hamis egyezés: Vulgata Zsolt 22:1 = Károli Zsolt 23:1; Targum Jóel 3:1 =
Károli Jóel 2:28; Vulgata Dán 3:24 = az Azariás-kiegészítés). **A Károli-feloldás nézetoldali** (DT-F176a): a
versmegfeleltetéssel (`Karoli_versmegfeleltetes.tsv` / TVTMS) a lapszerkezeti generátor-körben történik, nem ebben az
adatban. A `Konyv_normalizalo_tabla.tsv`-vel normalizált könyvkulcs nélkül néma nem-találat lenne (CLAUDE.md).

## 2. Targum — `Targum_PD.tsv`

- **Forrás:** a Sefaria-Export (`storage.googleapis.com/sefaria-export/json/Tanakh/Targum/…`), 26 verziófájl:
  Onkelos a Tórához (5 könyv; `versionTitle`: „Onkelos <Könyv>”, `versionSource`: http://toratemetfreeware.com/) és
  Jonatán a Prófétákhoz (21 könyv; `versionTitle`: „Mikraot Gedolot”). A forrásfájlonkénti hash és licenc a
  `naplok/F176_jelentes.md` 1. szakaszában; a 26 fájl hash-listájának SHA-256-ja: `8e6bc36039345b256601c0d20d1960b2804051d6785270ca962fe790308ff115`.
  A `books.json` SHA-256: `e5784fcf2ece785e2137ad4411c101839ada49a6ed1930b1af7b3d4510d20361`.
- **Licenc (elsődleges hely):** a Sefaria-Export `LICENSE.md`: „Each text is licensed separately, so there is no
  overall license for this repository.” és „You can find the license for each text in their JSON versions under the
  `license` field.” A 26 JSON mindegyikében: `"license": "Public Domain"`. A `merged` fájl nem használt; a jemeni
  (Taj) Onkelos-verzió CC BY-SA, a Metsudah NC — **kimaradtak**. **Kereskedelmi: engedett** (DT-F176b, a felhasználó döntése, 2026-11-08): a verziónkénti „Public Domain” licencmező a Sefaria ÁSZF kereskedelmi tiltásának „unless expressly stated otherwise” kivétele; a tartalom közkincs, a Sefaria nem licencelheti.
- **Oszlopok:** `igehely`, `forras_vers` (Sefaria-hivatkozás), `targum` (`Onkelos` | `Jonatan`), `forras_mu`,
  `verzio`, `forras_kulcs`, `szoveg` (arám, magánhangzó-jelekkel, a forrás szerint).
- **Nem benne:** az Írások Targumja, a Targum Jeruzsálemi / Pszeudo-Jonatán, a Targum Neofiti, az angol fordítások.
- **Újragenerálás:** `python -I eszkozok/visszhang/targum_import.py --be <letöltött json könyvtár> --books <books.json>`.

## 3. Vulgata — `Vulgata_Clementina.tsv`

- **Forrás:** https://ebible.org/Scriptures/latVUC_usfm.zip (SHA-256 `5d73ce3473e40b70cfcc976b967e0f259cbb031d6c0cd4f9798fbabf9f5b4e6c`,
  3 554 568 bájt; a zip bejegyzései 2026-10-29-esek).
- **Kiadás (az eBible saját megjelölése):** „Bibbia Vulgata Clementina na 1598” — „Clementine Vulgate of 1598 with
  Glossa Ordinaria Migne edition 1880 in Latin”. A kiadásról (1592/1598/1880) **nem döntöttünk**: a tábla az
  eBible által megnevezett kiadást hordozza; a szöveg a Clementina, a Glossa Ordinaria (Migne, 1880) lábjegyzetei
  nem kerültek át (12 968 lábjegyzet).
- **Licenc (elsődleges hely):** `ebible.org/latVUC/copr.htm` és `copyright.htm`: „Public Domain”.
- **Oszlopok:** `igehely`, `forras_vers` (USFM-könyvkód + forrás fejezet:verse), `forras_kulcs`, `szoveg`.
  66 kanonikus könyv; a deuterokanonikus könyvek (TOB, JDT, WIS, SIR, BAR, 1MA, 2MA) kimaradtak. A zsoltárok
  Vulgata-számozásúak; az Eszter- és Dániel-kiegészítések a forrás fejezetszámán állnak.
- **Újragenerálás:** `python -I eszkozok/visszhang/vulgata_import.py --zip <latVUC_usfm.zip>`.

## 4. SBLGNT apparátus — `SBLGNT_apparatus.tsv`

- **Forrás:** github.com/LogosBible/SBLGNT @ `d7f35adca9ec410e1d1499c63b4dd989d76c8d4d`, `data/sblgntapp/text/*.txt`
  (27 fájl; a 27 fájl hash-listájának SHA-256-ja: `190f883fc61f435c00ab08856d9885155b14467df8ea9107862a20dfa2c222a5`).
- **Licenc (elsődleges hely):** a repó `README.md`: „The SBLGNT is licensed under a Creative Commons Attribution 4.0
  International License.” és „Copyright 2010 by the Society of Biblical Literature and Logos Bible Software.”; a
  `LICENSE` fájl (SHA-256 `7e7170e3cebf88a9f60c7b8421418323c09304da1af4d5e90f4da1dc1c8a2661`) a CC BY 4.0 teljes
  szövege; a https://sblgnt.com/license/ oldal a CC BY 4.0-t adja. A 2022. decemberi áttérés előtti EULA
  („You may freely distribute the SBL Greek New Testament (SBLGNT), but you are not permitted to sell it on its own…”)
  már nem hatályos; szövege és hash-e a `naplok/F176_jelentes.md`-ben archiválva.
- **Kötelező megjelölés:** „SBL Greek New Testament, Copyright 2010 Society of Biblical Literature and Logos Bible
  Software, CC BY 4.0 (https://sblgnt.com)”.
- **Oszlopok:** `igehely`, `forras_vers`, `sorszam` (a jegyzet sorszáma a vers alatt), `forras_kulcs`, `jegyzet` (szó
  szerint). Az SBLGNT alapszövege nincs a táblában.
- **Újragenerálás:** `python -I eszkozok/visszhang/sblgnt_import.py --be <app könyvtár> --commit <sha> --license <LICENSE>`.

## 5. TAGNT változatjelölés — `TAGNT_valtozatok.tsv`

- **Forrás:** github.com/STEPBible/STEPBible-Data @ `5de0a47f35f0fc13dfe1430d104e5db8a4285f9c`, „TAGNT Mat-Jhn” és
  „TAGNT Act-Rev” (SHA-256: `d4c0c820fdf9f2b450c9f96ce6103d6875028affd2e44094d753f1329ca1fd85`, `122040eeeaeba50d6abbf67b39cacaff687211bda69b080e5d53927c830d9968`).
- **Licenc (elsődleges hely, a fájlfejléc):** „Data created by www.STEPBible.org based on work at Tyndale House
  Cambridge (CC BY 4.0)”; „Include any part of this data in software or publications and send it to AI servers
  without requesting permission”; „Attribute the data to Tyndale House and STEPBible.org, and include a link to
  STEPBible.github.io/STEPBible-Data as the source of this data.”
- **Tartalom:** minden olyan szó, amelynél a `editions` jelölő nem a teljes NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz
  halmaz, vagy a szó-típus nem `NKO` (11 777 az 142 095 szóból). **A THGNT (Tyndale House GNT, `Tyn`) szövege nem
  jött át**: csak az, hogy a szó mely kiadásban áll; a `Meaning variants` és `Spelling variants` oszlop (Tyn-alakot
  is hordoz) kimaradt, helyette `jelentesvaltozat` (igen/nem). A 4 csak-Tyn szónál a `gorog` mező üres.
- **Oszlopok:** `igehely`, `forras_ref` (pl. `Mat.15.6{15.5}`), `szamozas` (`nrsv` | `kjv` | `egyeb` | `na`: a forrás
  zárójel-jelölése), `szo_sorszam`, `tipus`, `strong`, `gorog`, `kiadasok`, `hianyzik_ebbol`, `mozgatas` (`»n`/`«n`),
  `jelentesvaltozat`, `forras_kulcs`. A zárójeles kettős hivatkozások Károli-feloldása (F90) itt **nincs** átvéve.
- **Újragenerálás:** `python -I eszkozok/visszhang/tagnt_valtozatok.py --be <tagnt könyvtár> --commit <sha>`.

## 6. BDB rokon írások — `BDB_rokon_irasok.tsv` (gyorsítótár)

- **Miért:** a `BDB_teljes_unabridged.tsv`-ben a nem-latin, nem-héber írású rokon szavak elvesztek (pl.
  „Arabic ,”); a Sefaria BDB-szócikke megőrizte őket. A `BDB_teljes_unabridged.tsv` **nem változik**.
- **Forrás:** a Sefaria `/api/words/<szó>` végpontja („BDB Dictionary”, „BDB Aramaic Dictionary”); a szócikk
  illesztése a `strong_numbers` mező szerint. A Sefaria a **szóalak-indexben** keres, nem a fejszóban: a szkript
  először a fejszót (a `BDB_teljes_unabridged.tsv` Strong-sorából), ha az nem ad illeszkedő BDB-szócikket, a
  `TAHOT_kivonat.tsv` leggyakoribb (legfeljebb 4) felszíni alakját kéri le.
- **Licenc:** a Sefaria lexikon-modelljében **nincs licencmező** (`sefaria/model/lexicon.py`; a `parent_lexicon_details`
  kulcsai: name, language, to_language, text_categories, source, attribution, index_title, version_title, version_lang).
  A BDB (Brown–Driver–Briggs, Oxford 1906) közkincs-státusza a mű korán alapul (a repó DT-F33g döntése, `licencek.tsv`
  BDB sor); a Sefaria megnevezése: „F. Brown, S. Driver & C. Briggs”. **Kereskedelmi: engedett** (DT-F176b, a felhasználó döntése, 2026-11-08): a tartalom közkincs, a közkincs-állítás az 1906-os kiadáson alapul.
- **Oszlopok:** `strong`, `sefaria_ref`, `nyelv` (`arab` | `etióp` | `szír`, Unicode-blokk szerint), `szoalak`,
  `kontextus` (≤ 120 karakter), `proveniencia`. A `kontextus` a token körüli szövegrész a BDB-szócikkből (nem a
  szócikk feje): az mutatja, melyik rokon szóhoz tartozik a token (DT-F176e). A görög és a latin írású, valamint az
  egybetűs token nem rokon szóalak, nem kerül be.
- **A „nincs rokon írás” nem sor:** a lekérdezés tényét és eredményét a fájl fejlécének `# lekérdezve: <Strong> | …`
  sora rögzíti (a próbált alakok, a talált BDB-szócikkek és a rokon-írás-sorok száma). Ezért a gyorsítótár második
  futása nem kér le újra.
- **Rátakorlát és azonosítás:** ≥ 1 s a kérések között; User-Agent: `PaRDeS-research/1.0` (felhasználói e-mail nélkül).
- **Futtatás:** `python -I eszkozok/visszhang/bdb_rokon.py --motivum HAMART-001` vagy `--strong H7843 H0779 …`.

## 7. Arány-kapu (F176.4)

A `eszkozok/nyilt_mag_kapu.py` `ARANY` ellenőrzése forrásonként kiírja: `<forrás>: <nyílt mag tételei> / <forrás
tételszáma> = <arány>%`. **1% felett FIGYELMEZTETÉS** (átnézés a következő kiadás előtt), **5% felett HIBA** (a kapu
megáll; további átvétel a felhasználó döntésével vagy ügyvédi vélemény után). A nyílt mag tétele az `elofordulasok.tsv`
sora, amelynek `forras_dataset` (`;`-vel tagolt) vagy `szotar` oszlopa a forrást nevezi. A forrás tételszáma e
dokumentum 1. szakaszának táblájából vagy az `adat/datasetek.tsv` `fajl` oszlopából jön. **A küszöbök óvatos mérnöki
értékek, jogi alapjuk nincs** (a #86 terv 6. szakasz 13. pontja). A mai nyílt magban visszhang-tétel még nincs, ezért
a visszhang-források aránya 0%.

## 8. Szándékosan kimaradt

- **Szír (Peshitta) ág:** szabad Peshitta-szöveg nincs (az ETCBC és a SEDRA NC), a szír ág ebben a körben kimarad;
  a `BDB_rokon_irasok.tsv` szír tokenjei a BDB szócikkéből jönnek, nem Peshitta-szövegből.
- **Kizárt források:** ETCBC és SEDRA Peshitta (NC), Nova Vulgata, THGNT-szöveg, Sahidica, AlHaTorah, a Sefaria NC- és
  „unknown” verziói, a Sefaria CC BY-SA verziói (jemeni Onkelos).
- **Tanúréteg** (sermonindex, Sefaria kapcsolattábla), a Vulgata Glossa Ordinaria, a lapra írás: következő fázis.
