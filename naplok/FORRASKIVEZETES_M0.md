# FORRASKIVEZETES M0 — felmérés (csak olvasás és mérés)

*Brief: `F42_FORRASKIVEZETES_BRIEF.md` · ág: `claude/forraskivezetes` · 2026-10-05 · fájlt nem mozgattam, nem töröltem, kódot nem írtam át. A mérőszkriptek a repón kívül futottak.*
*Proveniencia: scope=git ls-files + git grep a teljes repón; konkordancia/LXX_OS/*.tsv; konkordancia/LXX_kivonat_*.tsv | forras=git grep, gh api (STEPBible-Data fa), WebFetch (ebible.org, crosswire.org), saját mérőszkriptek | ts=2026-10-05. Ahol a mérés nem lekérdezés, `manual`-nak jelölt.*

## 0. Fő meglepetés: a brief kiinduló feltevése részben elavult

A brief 2026-10-02-i. Azóta (2026-10-04) a DT-F33f a **TBESH-t `tisztazott`-ra** emelte (a `Meaning` oszlopot is beleértve, SEMA 2.19 második kivétele), és az `adat/licencek.tsv` TBESH sora már `tisztazott`. A brief „Kiinduló döntések” szakasza viszont a DT-F33d (2) „TBESH `tisztazatlan`” állapotából indul, és erre épül a K6 és az M0 (a) kérdés. Ráadásul a DT-F33f szövege kétértelmű az áthelyezésről („A nyers fájlok a repóban maradnak (DT-F33a)”, miközben a DT-F33a alkalmazott döntése a három TBESH-fájl `_nyers/` alá mozgatása). Ez az (e) kérdés. A `licencek.tsv` TBESH-sorának megjegyzése ezen felül önmagának ellentmond: a régi „Az állapot ettől `tisztazatlan` marad” mondat bent maradt az új állapot mellett (SEMA 2.19 2. szabály: a `tisztazott` sor megjegyzése nem mondhat ellent az állapotnak).

## 1. Az olvasók teljes listája

### 1.A TBESH-család

| Fájl | Hely | Olvasás / említés | Mit olvas |
|---|---|---|---|
| `TBESH.txt` | `eszkozok/lexikon_general.py:52,225` (`tbesg_tbesh_index`) | **olvasás** | csak a 4–5. oszlop (héber lemma, átírás), a `Meaning`-et nem |
| | `lexikon_general.py:750,1124` | útvonal-címke a renderben | a kimenet „forrás:” fejlécei és a kolofon táblája tartalmazza a `konkordancia/TBESH.txt` útvonalat |
| | `eszkozok/kockazat_szures_18_tanulmany.py:84` | **olvasás** | a `Meaning` mezőt (első G-végű bejegyzés) is; kimenete `sablonok/Kockazat_szures_riport_2026-09-03.md` |
| | `eszkozok/cremer_ocr_javit.py:551` | **olvasás** (`os.path.exists` őrrel: hiány esetén csendben kihagyja) | az egész fájl szövegét az alak-igazoláshoz |
| | `eszkozok/tbesh_konszolidalt_import.py:44` | **olvasás** | teljes |
| | `eszkozok/istentiszt_2b_d1_toltes.py:153` | **ír** `forrasfajl` mezőt (a rendelt oldalszövegből, nem a fájlból olvas) | |
| | `motivumlog/lexikon_pilot/torzscikk_pilot.py:258`, `istentiszt_2b_d3_szerkeszt.py:50` | említés (markdown-blokk) | |
| `TBESH.lexicon` | `tbesh_konszolidalt_import.py:45` | **olvasás** (egyetlen kódolvasó) | |
| `TBESH_konszolidalt.tsv` | `tbesh_konszolidalt_import.py:46` | **ír** (generált) | **kód nem olvassa** (git grep az egész repón: nincs olvasó; a NYITOTT_FELADATOK 454. sora is azt írja, hogy a generátor nem olvassa) |
| mindhárom | `adat/lexikon_hivatkozasok.tsv:25` (`forrasfajl` mező), `adat/licencek.tsv`, `konkordancia/README.md:274`, `TBESH_TBESG_README.md` (11 említés), `lexikonok_nyers/README.md`, `Uj_lexikon_fajlok_2026-09-07.md`, `Javasolt_gorog_oldal_erositese.md`, `adat/SEMA.md`, `ADATVAGYON_TERV.md`, brieffájlok és naplók (F05, F6, LEXV2_2, ELLENOR_*, S1_*, …) | említés | |
| rendert oldalak | `lexikon/*_TUDOMANYOS.md` mind a 8 (65 előfordulás a `lexikon/`, `generalt_proba/`, `motivumlog/`, `tematikus_lezart/` alatt, összesen 16 fájlban) | a `konkordancia/TBESH.txt` útvonal a generált fejlécben és kolofonban | az áthelyezés ezeket a 16 fájlt a rendernél érinti |

Hiányzik a briefnek az `ir` listájáról és érinti: `eszkozok/tbesh_konszolidalt_import.py` benne van; **nincs benne**: `konkordancia/TBESH_TBESG_README.md`, `konkordancia/lexikonok_nyers/README.md`, `konkordancia/Uj_lexikon_fajlok_2026-09-07.md`, `adat/forditasok.tsv`, `sablonok/Kockazat_szures_riport_2026-09-03.md`.

### 1.B Az `LXX_kivonat` (39 adatfájl + `LXX_kivonat_README.md`; a `*_README.md` fájlok könyvenként nincsenek, egyetlen README van)

| Hely | Olvasás / említés |
|---|---|
| `eszkozok/lekerdez.py:444–470` (`_lxx_filename`, `cmd_lxx_hid`) | **olvasás**; a CLAUDE.md 6. lépése (LXX-híd) |
| `eszkozok/t1_teremt002_munkalap.py:214,250` | közvetett olvasás: `lxx-hid` hívás a `lekerdez.py`-n át |
| `eszkozok/teszt_lekerdez_sir.py:61` | közvetett: `lxx-hid Sir 2:8`, n=24 rögzítve (`adat/auditok.tsv` 169) |
| `eszkozok/lxx_osszevetes.py:30,93` | **olvasás** (a régi↔új összevetés eszköze; kimenete `naplok/LEXV2_lxx_osszevetes.tsv`) |
| `eszkozok/kockazat_szures_18_tanulmany.py:135–137` | **olvasás**, csak `LXX_kivonat_Genezis.tsv` |
| `eszkozok/lxx_bridge_egyezes.py:25,119,197` | **olvasás** (glob `LXX_kivonat_*.tsv`) — a futó #43 írja; **a #42 nem módosítja**, csak rögzítem. A kivezetés után ez a szkript hibázik, amíg a #43 át nem állítja: sorrendi függés a #43-tól |
| `eszkozok/lxx_kivonat_fetch.py`, `lxx_kivonat_fetch_v2.py` | **írók** (generátorok) |
| **`eszkozok/lxx_os_import.py:30`** | **kódfüggés, nincs a briefben:** `from lxx_kivonat_fetch_v2 import KEZI_ELTOLASOK` — az `LXX_OS` importerje a fetch_v2 szkriptből importál. A szkript törlése (az `ir` listában szerepel) az LXX_OS újragenerálását törné; előbb a konstanst át kell vinni. |
| `eszkozok/f4_0c_korut_ellenoriz.py:52` | említés (a `Betu_utotag_kizarva.tsv`-t a fetch_v2 írja) |
| `eszkozok/f08/f08_dontesek.py:103,109`, `f08_dt_sor.py:37`, `eszkozok/f17/macula_import.py:203` | említés (szöveg / megjegyzés) |
| `adat/datasetek.tsv` 11., 29., 47., 65. sor (`fajl` = `konkordancia/LXX_kivonat_*.tsv`, négy study-típus, ebből a `melyelemzes` sor `mindig`) | **adat, nincs a briefben** (`ir`-ben nincs `adat/datasetek.tsv`). Az `ellenoriz.py` 8. szabálya (dataset-lefedettség) ezeket a sorokat használja. |
| `adat/auditok.tsv` (58 sor), `naplok/F4_0_csv_karmeres.tsv`, `F4_0c_korut_ellenoriz.tsv` (39–39 sor), `naplok/T1_TEREMT002_auditok_munkalap.tsv` (58) | történeti proveniencia-sorok (`forras=LXX_kivonat_*.tsv`): nem módosítandók |
| `adat/SEMA.md:44,360`, `adat/lxx_dontesek.tsv` (2 sor), `adat/licencek.tsv` (2 sor) | említés |
| további említések (md): DONTESEK, FELADATOK, NYITOTT_FELADATOK (8), F4/F6/F24/F33/F43/F47 brief, LEX/LEXV2_1/LEXV2_2 brief, `konkordancia/README.md`, `LXX_OS/README.md`, `LXX_hid_lezaras_2026-09-05.md`, `Nem_parszolhato_ertekek_kategorizalas.md`, `sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, `sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md`, `lexikon/HAMART-001_*.md`, több tematikus napló, `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` (6) | említés |

## 2. CI és tesztek függése

- A CI (`.github/workflows/*.yml`) **egyik lépése sem olvassa** a TBESH-fájlokat vagy az `LXX_kivonat`-ot: az `ellenorzes.yml` az `eszkozok/ellenorzes/futtat.py`-t, az `ellenoriz.py`-t (adat-táblák) és a `feladatok.py` teszteket futtatja; a többi workflow önteszt (`fj2`, `karoli_strong`). A generátorok (`general.py`, `lexikon_general.py`) és a `lekerdez.py` a CI-ben **nem futnak**. A `datasetek.tsv`-ből csak az `allapot` oszlopot olvassa a `lekerdez.py` (619–625. sor), a `fajl` meglétét nem ellenőrzi.
- Egyetlen teszt érinti: `eszkozok/teszt_lekerdez_sir.py` (kézi, CI-ben nincs). Hiányzó `LXX_kivonat`-nál a `cmd_lxx_hid` `Hiányzó LXX-fájl:` hibával és kilépési kóddal áll (nem csendes). A `cremer_ocr_javit.py` viszont a hiányzó `TBESH.txt`-t **csendben kihagyja** (`os.path.exists`), ami a brief M2 „csendes kihagyás nem lehet” szabályába ütközik: ezt az olvasót át kell írni.
- Nincs `tests/` könyvtár; a tesztek `eszkozok/teszt_*.py` és `eszkozok/*/tesztek/`.

## 3. A `TBESH.lexicon` eredete

- `TBESH.txt`: **rögzíthető forrás van.** STEPBible-Data `b99716b0cddb648ddb95cc786a197180f2f97d48`, út: `Lexicons/TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt`. Mérés (`gh api` a fa metaadatáról, a fájlt nem töltöttem le): a git blob sha `a64990a674d13245ae1e9ed426bc69197c2fbad5`, méret 3 288 045 bájt — a helyi fájl `git hash-object` értéke és mérete pontosan ugyanez. Helyi sha256: `464dccadd95fd8620dd05fa0d7a4caba58ec3c4d5db3ebf38e43d046ca25b591` (ezt a `licencek.tsv` eddig csak az első 30 sorra igazolta, most az egész fájlra egyezik az upstreammel). A TBESG blobja is egyezik (`efe271a1…`). Tehát az M1 a `TBESH.txt`-t sha256-tal pontosan visszaállíthatja.
- `TBESH.lexicon`: **nem rögzíthető commitra.** Eredete: Eliran Wong `biblematedata` csomagja, egy Google Drive fájl (`1xlvJ6GURwYCxPnYwo2xuyREutWTeWMcH`, a `main.py`-ból azonosítva; `lexikonok_nyers/README.md`, a pilot átadási dokumentum 113–118. sora). A GitHub-repónak nincs licence (`gh api`: `license: null`), a Drive-fájl módosítható, commit/verzió nincs. Helyi sha256: `5a8e306ef974a14a7a691f0cf1b6302337034387ff85ea5edf576d75e327ce32` (2 387 968 bájt). Letöltési próbát nem végeztem (a letöltés felhasználói engedélyhez kötött; nem is volt a mérés tárgya). Következtetés: az M1 a `.lexicon`-ra **nem ad reprodukálható letöltőt**; csak helyben élhet, az olvasója egyetlen szkript.
- A `TBESH_konszolidalt.tsv` a két fájl uniója (`tbesh_konszolidalt_import.py`); a `.lexicon` hiányában nem generálható újra. **Kódolvasója nincs** (l. 1.A).

## 4. A származtatott Online Bible-tartalom (a legfontosabb rész)

**Módszer (`manual`, saját mérés):** a `TBESH.txt` összes `Meaning` mezőjéből 6 szavas szó-n-gramokat (150 584 db) képeztem, és megkerestem minden verziózott szöveges fájlban (md/tsv/txt/py/json), kizárva magukat a TBESH-fájlokat. A találatok javát kiszűrtem (azonos tartalom közkincsű/CC forrásokban: BDB, TBESG, Strong, SECE, Nave, Thayer, UBS …: a rövidített BDB maga is BDB-idézeteket ad, ezek nem jelölik az Online Bible-átvételt; 1Móz 2:4–7 bővített, 79. sor: BDB-azonos mondat; számsorok az `adat/forditasok.tsv` 296. sorában: zaj). Az egyetlen valódi, bekezdésnyi átvétel a **H7121 (קָרָא) TBESH-„részlet”**.

| # | Hely | Szöveg (≤15 szó) | Átvétel / fordítás | Helyettesítő más forrásból |
|---|---|---|---|---|
| 1 | `adat/lexikon_hivatkozasok.tsv:25` (H7121, `szotar=TBESH`, `jelentes_szam=részlet`) | „to call, call out, recite, read, cry out, proclaim” | szó szerinti angol átvétel (a konszolidált `.lexicon` szövege) | van: ugyanezen Strongra a BDB 2.c és 3. jelentés sora (`lexikon_hivatkozasok.tsv:3–4`) |
| 2 | `adat/forditasok.tsv:12` (TBESH H7121 `részlet`, `forditas_hu`) | — (magyar) | saját (gépi) magyar fordítás az 1. sorból: származtatott mű | a BDB-sorok fordításai ugyanott (`forditasok.tsv:3–4`) |
| 3 | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:399–405` (generált `szocikkek` blokk, a #1 sorból) és `:528–530` („A héber oldal kiegészítő adatai”: angol idézet + „Magyarul (TBESH)” bekezdés) | uaz | átvétel + fordítás | BDB-blokk ugyanazon az oldalon |
| 4 | `generalt_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md:512–514` | uaz | átvétel + fordítás (verziózott próba-kimenet, törölni tilos) | — |
| 5 | **forrásréteg:** `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md:220–222` | uaz | átvétel + fordítás (kézi forrás, ebből jön a 3. pont rése) | BDB/TBESG szövegek ugyanott |
| 6 | `motivumlog/Olvasoi_szint_pilot_ISTENTISZT-001.md:451`; `motivumlog/lexikon_pilot/ISTENTISZT-001_TORZSCIKK.md:833`; `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md:325` | uaz | átvétel (pilot-példányok) | — |
| 7 | `naplok/EMELES_elso_adag.md:171` | „call, cry, utter a loud sound” | részletidézet egy naplóban | — |
| 8 | `konkordancia/TBESH_konszolidalt.tsv` (egész fájl, 3,3 MB) | — | a teljes `Meaning` mező, szó szerint (`teljes_szoveg` oszlop) | — |
| 9 | `konkordancia/TBESH.txt` (egész fájl, 3,3 MB) | — | nyers forrás | — |

A 8. és 9. pont az áthelyezés (M2) tárgya; az 1–7. a tartalmi kérdés (a). A `lexikon_general.py` TBESH-ből csak a héber lemmát és az átírást olvassa (4–5. oszlop), tehát a renderelt oldalak többi része nem hordoz `Meaning`-et: **a render-felületen egyetlen Strong (H7121) van érintve, egy oldalon (ISTENTISZT-001)**, plusz a pilot- és próba-példányok. A `lexikon/*_TORZSCIKK.md` oldalak csak a szerepmátrix „TBESH” szót tartalmazzák (szótárnév), szöveget nem.
*Megjegyzés:* a brief a `forditas_hu` mezőt az `adat/lexikon_hivatkozasok.tsv`-ben említi; a tábla jelenlegi sémájában (`strong, szotar, entry_id, jelentes_szam, szoveg_en, forrasfajl`) ilyen oszlop nincs, a fordítások az `adat/forditasok.tsv`-ben vannak (SEMA 2.14). Az `istentiszt_2b_d1_toltes.py` ma már a régi 7 oszlopos fejlécet írná.

## 5. N9: a licenc-konstans és a `licencek.tsv`

A `lexikon_general.py` 60–76. sor: `LICENC` (16 kulcs → rövid címke), 81. sor: `TISZTAZATLAN_SZOTARAK = set()` (**üres**, a megjegyzés szerint „ma egyik sem tisztázatlan”). A halmazt a 689. sor használja (`tisztazatlan_erintve`).

- **Kulcs sor nélkül (2):** `UBS` (a táblában `UBS_DBH` és `UBS_DNTG` van, a kettő külön sor) és `projekt-adat` (a táblában `projekt_adat`, kötőjel/alsóvonás eltérés).
- **Sor kulcs nélkül (30 a 44-ből):** `KJV_ASV_Strongs, Karoli_1908, Karoli_Strong_kivonat, LXX_kivonat, Strong_szotar, TAGNT, TAHOT, TIPNR, Nave_basokant, BSB_Strongs, Macula_heber, Macula_gorog, lxx_bridge, LXX_versszintu_parok, Karoli_versmegfeleltetes, UBS_DBH, UBS_DNTG, SDBH_SDGNT_segedtablak, tW_szocikkek, KJV_Strongs_teljes, Versifikacios_tablak, Konyv_nevtablak, lexikonok_nyers, MGLNT_lexicon, LXX_lexicon, Heber_ETCBC_modulok, Cremer_nyers, Girdlestone, projekt_adat, OSHL_BDB`. A generátor ezeket ma nem címkézi; ezek közül a renderben ténylegesen megjelennek még, ha bekerülnek a `szotar` mezőbe.
- **A 14 egyező kulcs állapota a táblában:** `kozkincs`: BDB, Karoli_KH, Thayer, SECE_G, SECE_H; `tisztazott`: TBESH, TBESG, TSK, OSHL, SDBH, SDGNT, LXX_OS, LSJ, MCGED. **Egyik sem `tisztazatlan`.**
- **Címke-eltérések:** `LSJ` a konstansban `CC BY-SA 3.0`, a táblában CC BY-SA 4.0 (Perseus nyilatkozata, 2026.10.04); a tábla `licenc` oszlopa hosszú, vegyes prózai szöveg, **nem használható közvetlenül rövid címkének**; rövid-címke oszlop nincs.
- **A brief M7 várt diffjei elavultak:** „a BDB most tisztázatlan-jelölést kap a 8 oldalon” már nem igaz (BDB `kozkincs`, DT-F33g), a TBESH `tisztazott`. A mai táblával az egyetlen `tisztazatlan` kulcs a `projekt_adat`. A tényleges render-diff a címke-eltérésekből (LSJ 3.0→4.0, a TBESH `Meaning`-megjelölés, KJV-sor átsorolás) és a `projekt_adat` jelölésből áll majd.

## 6. A KJV Strong-címkék eredete és licence

- **Mit tartalmaz az eBible fájl:** a repó `KJV_Strongs_teljes.tsv` 4. fejlécsora a `eng-kjv_usfm.zip` sha256-ját rögzíti (`1bab5d4d…`). A zipet nem töltöttem le (letöltés engedélyhez kötött), a belső USFM-fejléc szövege ezért nem idézhető.
- **eBible-oldalak** (WebFetch, 2026-10-05): a `details.php?id=eng-kjv` oldal és a `copr.htm` **nem említi a Strong-címkézést, annak eredetét vagy licencét**. A `copr.htm` (oldaldátum 2026-09-26) szerint a szöveg „courtesy of the Crosswire Bible Society and eBible.org”, jelölése Public Domain. A címkézés eredetére tehát **az eBible nem nyilatkozik**.
- **CrossWire (az eBible szerinti szövegforrás) KJV-modulja** (`crosswire.org/sword/modules/ModInfo.jsp?modName=KJV`, WebFetch-kivonat, **nem szó szerinti, kézzel ellenőrzendő az eredeti `kjv.conf`-ból**): `DistributionLicense` „GPL”; „CrossWire Bible Society © 2003-2023”, amely „grants a general public license to use this text for any purpose”; a címkézés: ÓSZ Bible Foundation (bf.org), ÚSZ KJV2003 projekt, görög szövegbázis Dr. Maurice Robinson; **a címkézésre külön licencnyilatkozat nincs**, csak a modul egészére az említett GPL.
- Következtetés: az eBible-címkék **CrossWire-eredete valószínű, de nem bizonyított** (az eBible nem mondja ki, a két forrás egyezése nem igazolt). Ha az eredet CrossWire, a modul nyilatkozata (GPL) **eltér** a `licencek.tsv` „Public Domain”-jétől a címkeréteg esetén. A `licencek.tsv` KJV_Strongs_teljes sora maga is rögzíti: „Nyitott: a Strong-címkék (CrossWire) külön licence nincs idézve.”
- Összefügg az F48-cal (a régi studybible.info KJV/ASV fájlok kivezetése, a `KJV_Strongs_teljes` lesz az egyetlen KJV-forrás).

## 7. M5 előfelmérés: kiváltható-e az `lxx-hid` az `LXX_OS`-sel?

**Mit kellene tudnia:** Károli-igehely → szóalak, Strong, (morfológia). **Az LXX_OS tudja** (`igehely_karoli`, `szoalak`, `strong`, `morf`), de nem drop-in:

1. **Strong-formátum:** nullák nélküli (`746`), a régi `G0746`; morfológia **angol szöveg** (`noun fem dat sg`), a régi Robinson-kód (`N-DSF`). A kimenet 3. oszlopa tehát megváltozna.
2. **Szóalak:** a régi ékezet nélküli kisbetűs (θεος), az új Rahlfs ékezettel (θεός); végső-szigma/ékezet eltérés az összehasonlításban csak normalizálással tűnik el.
3. **Strong-hozzárendelés konvenciója eltér** a ragozott igéknél, ezért az ÚSZ-híd (TAGNT Strong szerinti keresés) eredménye változhat.
4. **Lefedettség:** `igehely_karoli` az `1-esdras`, `2-esdras` (= Ezsd, Neh) és `esther-greek` fájlban **mind üres**: Ezsdr 280 + Neh 392 + Eszt 163 = **835 vers**, amelyre az `lxx-hid` ma ad eredményt, az LXX_OS nem. Józs: `joshua.tsv` 95, `joshua-vaticanus-b.tsv` 616 Károli-kulcsos vers; Dán: `daniel.tsv` 308 / `daniel-theodotion.tsv` 327; Bír: két szövegváltozat — **szövegváltozat-választás kell** (egy vers kétszer szerepelne). Zsolt 66 vers (régi) nincs meg az újban; Dán 49–50 vers.
5. **Zsoltárok:** a régi kivonat **egy verssel eltolt**: a „Zsolt 22:2” a régi fájlban a Károli 22:3 tartalmát (LXX 21:3: „ο θεος μου κεκραξομαι ημερας…”) adja, az LXX_OS a helyeset (LXX 21:2, „Én Istenem, én Istenem…”, a Károli-szöveggel egyezik: `Karoli_1908.tsv` „Zsolt 22:2”). A régi fájl tehát a felirat-versszámozásban hibás; az átállás itt javítás, de a régi adatra épült állítások érintettek.

**Mintavételes eltérés** (a régi `lekerdez.py lxx-hid` kimenete vs. `LXX_OS`, azonos igehelyre; a szóalak-eltérések mind ékezet/végső-szigma-artefaktok, kivéve ahol jelezve):

| Igehely | régi n | LXX_OS n | Valódi eltérés |
|---|---|---|---|
| 1Móz 1:1 | 10 | 10 | nincs (a Strong-halmaz azonos) |
| 2Móz 33:19 | 28 | 28 | εἶπεν: régi G2036, új G3004; οἰκτιρήσω: régi G3627, új üres (az utolsó igealaknak az új nem ad Strongot; a másik οἰκτίρω-nak igen) |
| Zsolt 22:2 | 15 | 21 | **teljesen más vers** (régi: LXX 21:3; új: LXX 21:2); az új `karoli_ok=mt_szamozas_kovetes` |
| Ézs 53:5 | 23 | 23 | μεμαλάκισται: régi G3119, új üres |
| Jer 31:31 | 16 | 16 | διαθήσομαι: régi G1303, új üres; Ισραηλ: régi G2474, új üres (az új `strong_ok=nincs_uszbeli_megfelelo` jelzi) |

Proveniencia (a régi parancs saját sorai): `scope=range:1Móz 1:1 | forras=LXX_kivonat_Genezis.tsv+TAGNT_kivonat.tsv | n=10 | ts=2026-10-05T07:02Z`; `…2Móz 33:19 | forras=LXX_kivonat_Exodus.tsv+… | n=28`; `…Zsolt 22:2 | forras=LXX_kivonat_Zsoltarok.tsv+… | n=15`; `…Ézs 53:5 … n=23`; `…Jer 31:31 … n=16`. Az új oldal: `scope=range:<igehely> | forras=LXX_OS/*.tsv (lxx-morph@c91f6b1e + GreekWordList@dd5a2fd5) | n=10/28/21/23/16 | ts=2026-10-05T07:02Z` (manuális mérés, `manual`, nem `lekerdez.py`-kimenet).

**Teljes körű, tájékoztató összevetés** (`manual`; versenként a nem üres Strong-multihalmazok Jaccard-hasonlósága, a szövegváltozat-fájlok közül a Károli-kulccsal ellátott/elsődleges kiválasztva; csak az irányt jelzi): 22 627 régi vers → azonos 4 048, kis eltérés (J≥0,8) 11 673, nagy eltérés (J<0,8) 5 030, az újban nem található 1 876. A „csak régi” zöme az Ezsd/Neh/Eszt (835) és a Józs-szövegváltozat. Az eltérés tehát nem elhanyagolható: a felsorolás-igényt (brief M5) a teljes táblázat jelenti, amit az M5 fog elkészíteni.

## 8. ⛔ Kérdéscsokor (mindegyik DONTESEK-tétel, `DT-F42a`…)

**(a) Mi legyen az Online Bible-eredetű szövegekkel (4. pont: 1 sor a `lexikon_hivatkozasok.tsv`-ben, 1 a `forditasok.tsv`-ben, 1 oldal-blokk a lexikonoldalon, 1 kézi forrásszakasz, pilot- és próba-példányok)?** A DT-F33f szerint a `Meaning` oszlop `tisztazott`, tehát a kérdés szűkebb, mint a brief feltételezi. *Javaslat:* kiváltás a BDB-sorokkal, amelyek ugyanerre a Strongra már megvannak: a TBESH `részlet` sor törlése a két táblából, a `Segitsegul_hivni…tematikus.md` 220–222. sorának és a lexikonoldal „héber oldal kiegészítő” bekezdésének átírása BDB-alapra, a pilot- és próba-példányok (törölni tilos) változatlanul maradnak, regenerálás nélkül. *Alternatívák:* (2) marad, a DT-F33f jóváhagyására hivatkozva, a „© Larry Pierce / OnlineBible.net” jelöléssel kiegészítve a kolofonban; (3) saját átfogalmazás; (4) törlés csere nélkül.

**(b) A `TBESH.lexicon` nem tölthető le rögzített forrásból** (Google Drive, nincs commit, nincs licenc; 3. pont). Elég-e, hogy csak helyben él, és az olvasó hiányra jelez? *Javaslat:* igen, a `_nyers/` alatt, a hiány a `tbesh_konszolidalt_import.py`-ban hibával jelez, a letöltő szkript nem ígér letöltést; és mivel a `TBESH_konszolidalt.tsv`-nek **nincs kódolvasója**, a konszolidált fájl is csak helyben él. *Alternatívák:* (2) a `.lexicon` és a konszolidált tábla végleges elhagyása (nincs olvasójuk; az `S4` unió története a `TBESH_TBESG_README.md`-ben megmarad); (3) a Drive-letöltés scriptelése sha256-tal (törékeny, a Drive-fájl nem verziózott).

**(c) Teszt/CI a hiányzó fájlnál.** A CI semmit sem olvas (2. pont), a kézi `teszt_lekerdez_sir.py` az `LXX_kivonat` törlése után az `LXX_OS`-t olvasná. *Javaslat:* kihagyással fusson (egyértelmű `forras_letolt.py`-ra mutató üzenet), a CI ne futtassa a letöltőt (az `LXX_OS` ráadásul a repóban marad, a TBESH-nek nincs CI-olvasója). A `teszt_lekerdez_sir.py` rögzített n-eit (24/15/1/38/10) az M5 után újra kell rögzíteni. *Alternatíva:* a CI futtassa a letöltőt a `TBESH.txt`-re.

**(d) KJV Strong-címkék licence (6. pont):** az eBible nem nyilatkozik a címkékről; a CrossWire-modul GPL-t jelez és a címkékre külön nyilatkozata nincs; az eredet valószínű, de nem bizonyított. Átkerüljön-e a sor `tisztazatlan`-ra? *Javaslat:* igen, a `KJV_Strongs_teljes` sor `tisztazatlan`, amíg a CrossWire-modul eredeti `kjv.conf`-ja szó szerint nincs idézve és az eBible-tag eredete igazolva (a szöveg, mint közkincs, külön sorként/megjegyzésként marad). *Alternatíva:* marad `kozkincs` a DT-F33d (3) szerint, a megjegyzés pontosításával.

**(e) Még érvényes-e a TBESH-fájlok `_nyers/` alá mozgatása a DT-F33f után?** A DT-F33a alkalmazott döntése mozgat; a DT-F33f „TBESH tisztazott” és „a nyers fájlok a repóban maradnak (DT-F33a)” mondata ezzel nem egyértelműen egyeztethető; a README tükrözést megenged. *Javaslat:* a mozgatás **marad** mindhárom fájlra (a `.lexicon` és a konszolidált tábla licence/eredete tisztázatlan, a `TBESH.txt` pedig letölthető és sha256-tal ellenőrizhető, tehát a repóból kivétele veszteség nélküli). *Alternatívák:* (2) a `TBESH.txt` marad a repóban (CC BY, mirror-megengedés), csak a `.lexicon` és a konszolidált tábla mozog; (3) mind marad, a brief megszűnik (K1 teljesíthetetlen).

**(f) Az `LXX_kivonat` kivezetése nem drop-in (7. pont).** Három döntés kell: **(f1)** a 835 vers (Ezsd/Neh/Eszt), amelyre az LXX_OS-ben nincs Károli-kulcs: *javaslat:* az `lxx-hid` ezekre explicit „nincs LXX_OS-megfeleltetés” üres eredményt ad (CLAUDE.md 3. szabály, nincs kitöltés), a kulcsok pótlása külön feladat; *alternatíva:* a kivezetés várjon a mapping elkészültéig. **(f2)** szövegváltozat (Józs: B/A; Bír: B/A; Dán: OG/Theodotion): *javaslat:* az a változat, amelyik a legtöbb Károli-verset kulcsolja (Józs: `joshua-vaticanus-b`, Dán: `daniel-theodotion` 327 vers, Bír: `judges` 618 vers), és ezt a README rögzíti. **(f3)** Strong-konvenció és a régi zsoltár-eltolás: az eltérés-listát az M5 jelentésbe teszem; *javaslat:* az átállás a javítást (a zsoltár-eltolás) elfogadja, az eltérő Strong-hozzárendelést jelöli. Plusz **kódfüggés:** `lxx_os_import.py` importálja a `lxx_kivonat_fetch_v2.KEZI_ELTOLASOK`-t, ezért a fetch_v2 szkript nem törölhető, amíg a konstans át nincs vive (*javaslat:* áthelyezés az `lxx_os_import.py`-ba, a fetch szkriptek archiválása); a `lxx_bridge_egyezes.py` (#43) a kivezetés után hibázik: *javaslat:* a #42 M5 csak a #43 lezárása után fusson, vagy a #43 állítsa át a saját olvasóját előbb.

**(g) N9: a rövid licenc-címke forrása.** A `licencek.tsv`-ben nincs rövid-címke oszlop (a `licenc` hosszú próza), `UBS`-nek nincs sora (két külön sor van), `projekt-adat`/`projekt_adat` név-eltérés, az LSJ-címke 3.0 vs 4.0, és a brief M7 várt diffje elavult (BDB már `kozkincs`, TBESH `tisztazott`). *Javaslat:* új, zárt `cimke` oszlop a `licencek.tsv`-ben (SEMA 2.19 bővítés; ez nem új *állapotérték*), a generátor ebből és az `allapot`-ból dolgozik; `UBS` kulcs → a generátor a két UBS-sor `cimke`-jét egyezőként követeli meg; a hiányzó sor hibát ad (K7). *Alternatíva:* a címke a `licenc` oszlop első tagja (kódba írt elválasztóval; törékeny), vagy a `LICENC` konstans marad csak a címkékre (K7-et sérti).

**(h) Hatókör-bővítés (az `ir` lista hiányai).** Hozzá kell venni: `adat/datasetek.tsv` (4 `LXX_kivonat` sor; `melyelemzes`: `mindig` — az `ellenoriz.py` 8. szabálya ezen áll, nem csak törlés, hanem helyettesítés kell az `LXX_OS` soraira), `adat/forditasok.tsv` (a TBESH H7121 sor, ha (a)=kiváltás), `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, `lexikon/ISTENTISZT-001_TUDOMANYOS.md` (generált: csak forrásból), `konkordancia/TBESH_TBESG_README.md`, `lexikonok_nyers/README.md`, `Uj_lexikon_fajlok_2026-09-07.md`, `eszkozok/lxx_os_import.py`, `sablonok/Kockazat_szures_riport_2026-09-03.md` + kimenet. *Javaslat:* hozzávétel, a brief `ir` mezője bővüljön. *Alternatíva:* külön befogadott feladat.

**(i) A `licencek.tsv` TBESH-sorának önellentmondása** (régi „tisztazatlan marad” mondat a `tisztazott` állapot mellett; SEMA 2.19 2. szabály): *javaslat:* az M6-ban javítom (a megjegyzés rendezése, tartalmi állítás nélkül). *Alternatíva:* külön javítás. A `generalt_proba/` és a `KJV_ASV_Strongs` sor hasonló vizsgálata nem tartozik ide.

## 9. Megjegyzések a következő lépésekhez

- A git-történetben a TBESH-fájlok és az `LXX_kivonat` a korábbi commitokban megmaradnak (a történetet nem írjuk át): ez az M7 DONTESEK-tétele.
- A fenti `ir`-hiányok közül a `adat/auditok.tsv` és a naplók proveniencia-sorai (`forras=LXX_kivonat_*.tsv`) történeti rekordok: nem módosítandók.
- A mérőszkriptek (`shingle.py`, `lxxcmp*.py`, `lxxglob.py`) a munkamenet scratchpad-könyvtárában vannak, a repón kívül.
