# F06_forras_jelentes.md — Új források 2. felmérése (FJ 2. menet)

*F06_FORRASFELMERES_BRIEF.md v1 · ág `claude/f06-forrasfelmeres` · 2026.09.29. · a mérés GitHub Actionsben futott (futások: 36606454914, 36607700736), helyi gép nem kellett. Javítva az `ELLENOR_F06.md` „Eltérések” 1–7. pontja szerint; a mérést nem futtattam újra.*

**Számok forrása.** A jelentés F06-mérésre hivatkozó számai a `naplok/F06_*.tsv` kimenetekből vagy a `naplok/F06_5_osszesito.py` kimenetéből (`naplok/F06_5_osszesito.txt`) származnak; a szkript ugyanezeket a fájlokat olvassa. Ettől eltérő forrású számokat külön jelölök: az **FJ1/FJ4/FJ3-ból átvett** értékek (`naplok/FORRAS_jelentes.md`, `FORRAS_FJ1_mtlxx_macula.md`, `FORRAS_FJ4_nave.md`, `FORRAS_FJ3_kjv_bsb.md`) nem újramértek. A MiniMax kimenetéből szám nem került ide. A MiniMax ítéletei **javaslatok**; ahol szó szerinti idézet nincs (üres idézet, kézi jelölés, vagy a kapu elbukott), ott ezt kimondom, és a **saját olvasatot** a forráshellyel (fájl és sor a `naplok/F06_licenc_szovegek/` alatt) adom meg. A végső licencdöntés a felhasználóé.

**A licenc-ítéletek olvasása.** A `F06_licenc.tsv` 24 kapun átment sora közül 11 `nincs_adat` üres idézettel. Ez **nem** „a szövegben nincs licencinformáció”: az `eng-kjv_usfm.zip#copr.htm`, az `eng-asv_usfm.zip#copr.htm` és az `elcafe7_lex/docs/LICENSING.md` tartalmaz licencre vonatkozó állítást (lent, saját olvasat). A `macula_hebrew` két fájlja kétszer is elbukott az idézetkapun (`kezi_kapu`). Hat szöveg 12 000 karakter fölötti, ezek „kézi” jelölést kaptak (nincs darabolás): `theonize_bible_database/LICENSE`, `elcafe7_lex/docs/README.html`, `kjvstudy.org` `kjvstudy_org/data/README.md`, `KJV-Strongs-EBook` `LICENSE` és `README.md`, `scripture-intelligence-server/README.md`.

## 1. Forrásonként

### Nave (N27) — `naplok/F06_nave.tsv`

| Jelölt | Mérés | Licenc (idézettel) | Javaslat | Indok |
|---|---|---|---|---|
| `basokant/nave` | elérhető (commit `4f35c7d4…`); `data/parsed-nave.json`: lista, 5322 elem; `data/nave.txt` 4 565 849 bájt; téma↔vers reláció **nem mérve** (a JSON belső szerkezetét a szkript nem bontja) | nincs LICENSE-fájl a gyűjtött fájlok között. MiniMax: `nincs_adat`, **idézet nincs (üres), saját olvasat**: `basokant_nave__README.md.txt` 5. sor „Based off of Nave's Topical Bible.”; 9. sor „It also happens to be in the public domain.” (a Nave 1897-es művéről); 58. sor „A scraper for Nave's Topical Bible from www.naves-topical-bible.com, using Bun.” | **FELTÉTELLEL** | a README a közkincs-állítást a műre (Nave 1897) teszi, nem a repó adatfájljaira; az adat lekaparás eredménye, a weboldal feltételeit nem vizsgáltuk |
| `theonize/bible_database` | elérhető (`0df2f992…`); `Topics.csv` 32253 sor, 4980 egyedi Topic; `TopicIndex.csv` 92609 reláció; mind a 92609 reláció könyve leképezhető a `Konyv_normalizalo_tabla.tsv`-re (0 nem leképezhető; csak könyvszint) | `LICENSE` 35141 karakter → **kézi** (nincs MiniMax-ítélet). Saját olvasat: `theonize_bible_database__LICENSE.txt` 1–2. sor „GNU GENERAL PUBLIC LICENSE”, „Version 3, 29 June 2007”. `README.md` (86 karakter): MiniMax `nincs_adat`, idézet nincs (üres); a README forrást nem nevez | **FELTÉTELLEL** | a legjobb szerkezet és kész reláció, de GPLv3 (copyleft), és a Nave-eredet sehol nincs kimondva |
| `elcafe7/lex` | elérhető (`4e777320…`); `topics` tábla 5319 sor; „KOD fej:vers” horgonyok: 40089 (alsó becslés), ebből 40088 leképezhető, 1 nem (`1JHN`) | MiniMax, idézettel: „Lex code is MIT licensed. Bible data and Lexicon content are subject to their respective upstream licenses.” (`README.md`). `docs/LICENSING.md`: MiniMax `nincs_adat`, **idézet nincs (üres), saját olvasat**: a 29–36. sor az ismert adatforrásokat (ESV, TSK, Strong's, STEPBible, UBS, Geocoding, Easton, ISBE, hitvallás-adatok) nevezi, Nave-et nem | **NEM** | az adat eredete és licence dokumentálatlan, a kód MIT-je az adatra nem terjed ki |

**N27:** a felmérés szintjén lezárható. A `basokant/nave` létezik (az FJ4 „nem létezik” állítása téves volt), de a három közül egyik sem tisztán importálható licencszempontból. **Hiányzik:** a felhasználó döntése arról, hogy a `basokant/nave` README-beli közkincs-állítása és a lekaparás elég-e, vagy a `theonize` GPLv3-a vállalható-e; a `basokant` JSON-jában a téma↔vers relációk számának mérése. Eltérés az **FJ4-hez** (FJ4-ből átvett, nem újramért érték): az FJ4 32254 sort, 4951 főtémát és 92610 relációt jelzett a `theonize`-re, a mostani mérés 32253, 4980 és 92609; az okot nem tisztáztam.

### Teljes KJV/ASV (N29) — `naplok/F06_kjv_asv.tsv`

| Jelölt | Mérés | Licenc (idézettel) | Javaslat | Indok |
|---|---|---|---|---|
| **eBible.org USFM** (`eng-kjv_usfm.zip`, `eng-asv_usfm.zip`) | HTTP 200 mindkettő. KJV: 66 kanonikus könyv, 31102 vers, ebből 31099 `strong=` címkés; ASV: 66 kanonikus könyv, 31102 vers, ebből 30978 címkés (a KJV-zip az apokrifokkal együtt 81 könyvet tartalmaz) | MiniMax: `nincs_adat`, **idézet nincs (üres), saját olvasat**: `ebible_org__eng-kjv_usfm.zip__copr.htm.txt` 40. sor „You may copy the King James Version of the Holy Bible freely.”, 41. sor „Public Domain”; a 25. sor a királyi szabadalmat említi (nyomtatás az Egyesült Királyságban engedélyhez kötött). ASV (`…eng-asv…copr.htm.txt` 39. sor): „The American Standard Version of the Holy Bible is in the Public Domain. Copy freely.” | **IMPORT** | teljes, kanonikus, szó-szintű (`\w szó\|strong="…"`), közkincs-nyilatkozattal; az import-menet feladata a címke-formátum mintaellenőrzése (számformátum, többszámú címkék) |
| `luvlylavnder/bible-app-data` | KJV JSON: 66 könyv, 31102 vers, mind címkés; ASV JSON: 66 könyv, 31086 vers, mind címkés; Genezis 1:1 példa a kimenetben (`{H7225}` szó után) | MiniMax, idézettel: „All data is in the public domain and licensed under [CC0 1.0](LICENSE).” (`README.md`); gyökér `LICENSE`: CC0 1.0 („…the person associating CC0 with a Work (the "Affirmer")…”). A `Bible-Versions/KJV/LICENSE` és `…/NIV/LICENSE` MIT („Permission is hereby granted, free of charge, to any person obtaining a copy of this software…”); a `KJV-Strongs/` mappának nincs saját licencfájlja | **FELTÉTELLEL** | teljes és feldolgozásra kész, de harmadik fél csomagolása, a címkézés eredete nincs megnevezve; ellenőrző másodforrásnak alkalmas |
| studybible.info | HTTP 200 a `KJV_Strongs/Genesis%201` és `ASV_Strongs/Genesis%201` oldalra | licencfájl **nincs gyűjtve** | **NEM** | a meglévő táblák forrása, oldalankénti lekaparás; a licencét ez a menet nem vizsgálta, ezért nem minősíthető másképp |
| `RonTurrentine/KJV-Strongs-EBook` (`kjv.osis.xml`) | 355850 `lemma="strong:…"` címke; lefedettség nem mérve | `LICENSE`/`README.md` **kézi** (12 000 fölött), **MiniMax-ítélet nincs**; saját olvasat: `…KJV-Strongs-EBook__README.md.txt` 283–286. sor „This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License… either version 3” | **NEM** | GPL-3.0 (copyleft); az eBible mellett nincs rá szükség |
| `kennethreitz/kjvstudy.org` | a `szo_szintu_strong_bizonyitek` sor **`igen`** (`F06_kjv_asv.tsv`), mert a szkript a KJV/ASV nevű fájlok között egy Genezis 1:1 mintapéldát talált (`index.html`, `interlinear_landing.html`, `word_studies.json`: mind `nincs_mintaillesztes`); **ez nem tömeges, szó-szintű KJV/ASV-címkézés** (tömeges adatfájl nincs, lefedettség nem mérhető), tehát a szkript `igen` jelölése és a javaslat nem azonos állítás | MiniMax, idézettel: „Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted…” (`LICENSE`, ISC) | **NEM** | web-alkalmazás, nem adatforrás |
| `1John419/kjs` | a szkript a KJV/ASV nevű fájlokban nem talált címke-mintát (`nem`) | MiniMax, idézettel: „This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License…” (`LICENSE.md`, GPL-3.0) | **NEM** | nincs mérhető szó-szintű címke, copyleft |
| `Realbizdigital/scripture-intelligence-server` | nincs címke-minta (`nem`) | MiniMax, idézettel: „Permission is hereby granted, free of charge, to any person obtaining a copy of this software…” (`LICENSE`, MIT, kód); `README.md` kézi | **NEM** | nincs mérhető szó-szintű címke |
| `kaiserlik/kjv` | nincs címke-minta (`nem`) | nincs licencfájl; a `README.md` 224 karakter, MiniMax: `nincs_adat`, idézet nincs (üres); saját olvasat: a README „Includes Strong's Hebrew/Greek lexicon tags” állítást tesz, de a szkript nem talált címke-mintát | **NEM** | licenchiány, nincs mérhető címke |
| `scrollmapper/bible_databases` | **nem mérhető**: a klónozás időtúllépett (`F06_kjv_asv.tsv`: „idokorlat (420 mp) a klonozasnal”) | — | **NEM** (megjegyzés: nem mérhető, nincs minősítés; az eBible mellett a döntéshez nem szükséges) | nyitott hézag |

A GitHub-keresés négy lekérdezése 10, 0, 2 és 0 találatot adott (`kereses:` sorok).

**N29:** lezárható. Van elérhető, közkincs-nyilatkozattal ellátott, teljes, szó-szintű Strong-címkézésű forrás (eBible USFM). **Hiányzik:** a felhasználó döntése; az import előtti mintaellenőrzés (címke-formátum, TAHOT-hoz mért egyezés) az import-menet dolga.

### BSB (N30) — `naplok/F06_bsb_genezis.tsv`, `naplok/F06_bsb_elteresek.tsv`

- **Rögzített feltétel (mérés előtt, `eszkozok/fj2/kuszob.txt`):** küszöb 95%; egyezés = a vers TAHOT Strong-halmaza része a BSB-halmaznak, a 9000-es és afeletti prefixkódok nélkül; nevező = a TAHOT-tal rendelkező versek. **A nevezőt a felhasználó a javaslat részeként hagyta jóvá** (kifejezetten nem vitatta); a küszöböt és a definíciót jóváhagyta.
- **Mérés (BSB commit `a4a2c055…`):** 1533 vers; mind a 1533 TAHOT-lefedett (`nincs_tahot = 0`, így a két nevező azonos); 1515 egyezik, 18 eltér: **98,83%**; eredmény **ELÉRI** a 95%-ot. Átlagos Jaccard 99,83%.
- **Az eltérések** (18 sor, mind `tahot_nincs_a_bsb-ben`): közülük 7-ben a TAHOT `H2895`, a BSB `H2896` (טוֹב). Az **FJ3** (FJ3-ból átvett, nem újramért) ezt „feltehetően” a TAHOT saját tövesítési döntésének tartotta; ez **hipotézis**, a mostani mérés csak az eltérés tényét és a számát igazolja.
- **Licenc:** a `README.md` táblázata, MiniMax idézettel: „`base/display/` | CC0 (Public Domain) | No” és „`base/index-cc-by/` | CC-BY 4.0 | **Yes**”; a `LICENSE-CC0.md` és `LICENSE-CC-BY.md` kapun átment. Az import célja a `base/display/` (CC0).
- **Javaslat: IMPORT.** **N30:** lezárható, a feltétel (teljes Genezis-összevetés, előre rögzített küszöb) teljesült és eléri a küszöböt. Megjegyzés: a `CLAUDE.md` szerint a TAHOT-kivonatból hiányzik az 1Móz 32; a mérésben az 1Móz 32-nek van TAHOT-sora (`nincs_tahot = 0`), tehát a hiány legfeljebb tartalmi, nem versszintű; ezt nem vizsgáltam tovább (az 1Móz 32:28 az eltérések között szerepel).

### Macula Hebrew (N31) — `naplok/F06_macula_lefedettseg.tsv`, `naplok/F06_macula_87_hely.tsv`

- **Lefedettség (commit `47db250b…`):** 39 könyv, 929 `lowfat`-fájl, egyik könyvnél sem 0 a fájlok száma. Az 1Sám–2Krón mind a hat könyve megvan: 167 fájl, 4807 Macula-vers a TAHOT 4806 versével szemben, 4772 közös. Összesen 23213 Macula-vers, 23179 TAHOT-vers, 23045 közös; 14 könyvnél teljes az egyezés a verslistában. A többi könyvnél a `csak_macula` / `csak_tahot` oszlop eltér (pl. Jób: Macula 1070 vers, TAHOT 1036, `csak_macula` 42, `csak_tahot` 8; Jóel: `csak_macula` 21). **Az ok nincs vizsgálva**; a versszámozási különbség csak feltevés, ezért nem állítom.
- **Az FJ1 „hiánya”:** az 1Sám–2Krón fájljai megvannak a mostani letöltésben (a mért fájlkódok `1Sa`, `2Sa`, `1Ki`, `2Ki`, `1Ch`, `2Ch`). Az FJ1 szkriptjeinek fájlnév-mintája (`^\d+-([A-Za-z]+)-…`) számjegyre kezdődő fájlkódot nem illesztene; ez **hipotézis** az FJ1 hiányára, az FJ1 futását nem reprodukáltam, tehát azt nem állítom, hogy az FJ1-ben nem letöltési hiba volt.
- **Licenc:** MiniMax `kezi_kapu` (kétszer bukott az idézetkapun, **idézet nincs, saját olvasat**): `macula_hebrew__LICENSE.md.txt` 3. sor „is licensed under [CC BY 4.0 ]” (Biblica, Inc); 7. sor „Greek equivalents drawn from the Septuagint”; 9. sor „Strong's numbers for both Hebrew and Greek equivalents”. **Nem „rendben” egyszerűen:** a 21. sor szerint a Semantic Dictionary of Biblical Hebrew (a szemantikai domének forrása) „Used with permission” — ez nem CC BY; ha a felhasználás az SDBH-származékot (domének, jelentések) érinti, külön tisztázás kell. A 87 hely LXX-megfelelője (`greek`, `greekstrong`) ebből a szempontból külön nincs vizsgálva.
- **Javaslat: FELTÉTELLEL** (feltétel: az SDBH-engedély tisztázása, ha az SDBH-adatot használjuk; CC BY 4.0 forrásmegjelölés). Az FJ1 a szó-szintű MT–LXX-illesztésre 78,3%-ot mért (FJ1-ből átvett, nem újramért), ezért a G8 tagmondat-tagoláshoz és a 87 hely kiinduló javaslatához használható, importja a küszöb miatt nem javasolt.
- **N31:** lezárható. A letöltés teljes.

## 2. A #8-nak átadott rész — a 87 függő hely (`naplok/F06_macula_87_hely.tsv`)

A számok a `naplok/F06_5_osszesito.txt` kimenetéből valók (az új bontás a szkriptben szerepel).

| Állapot | Sor | Bontás |
|---|---|---|
| **LXX_MEGFELELO** (a talált héber szóhoz a Macula görög Strong-számot rendel) | **39** | 37 `strong`, 2 `szoalak` azonosítás |
| HEBER_SZO_GOROG_NELKUL (a héber szó megvan, **görög Strong nincs** rendelve) | 38 | **27** sorban van görög szóalak (csak a görög Strong hiányzik), **11** sorban valóban nincs görög sem; azonosítás: 26 `strong`, 12 `szoalak` |
| HEBER_SZO_NINCS_A_VERSBEN | 8 | mind a 8 sorban a `heber_kulcsszo` `—` és a munkalap Strong-mezője üres: **nem volt mit keresni**, nem keresési kudarc |
| NINCS_VERS | 2 | mindkettő 4Móz 13:34 (két motívum); csak erre a 2 sorra jöhet szóba a számozási magyarázat (N28), ez nincs vizsgálva |

**A Macula tehát 39 függő helyre (a 87-ből) ad görög Strong-számmal is ellátott LXX-megfelelőt.** Ezenfelül 27 helyen van görög szóalak Strong nélkül (a #8 kézi munkájához támpont, de nem azonosított görög lemma). Figyelmeztetések a #8-nak: (1) a munkalap igehelyei Károli-számozásúak, a Macula héber; számozás-átalakítás nem történt; (2) az `azonositas = szoalak` sorok (2 + 12) a munkalap hiányzó `heber_strong` mezője miatt ékezet nélküli szóalak-egyezésen alapulnak, gyengébb bizonyosságúak; (3) az FJ1 a Macula szó-szintű illesztését 78,3%-osnak mérte (FJ1-ből átvett), tehát a 39 sor **javaslat, kézi megerősítést igényel**, nem döntés.

## 3. MiniMax-költség (`naplok/F06_koltseg.tsv`)

29 hívás (`minimax/minimax-m3`, OpenRouter), a sorok összege **0,011927 USD** (a plafon 1 USD); a hívások 7 különböző providerhez mentek (CoreWeave, GMICloud, Minimax, ModelRun, SambaNova, StreamLake, Together). A fájl fejlécsora 0,011926-ot ír: a különbség a hívásonkénti hatjegyű értékek kerekítéséből adódik, a mérvadó a sorösszeg (`F06_5_osszesito.txt`). Az újrafuttatás a már kapun átment ítéleteket nem kérdezte újra. A 32 elemzett szövegből 24 ment át a kapun, 6 „kézi_hosszu” (nincs darabolás), 2 „kézi_kapu” (Macula).

## 4. Nyitott pontok, amelyek a felhasználó döntésére várnak

1. **Nave:** `basokant/nave` (közkincs-állítás + lekaparás) vagy `theonize` (GPLv3), vagy egyik sem.
2. **KJV/ASV:** eBible USFM (javasolt), esetleg a `luvlylavnder` másodforrásként.
3. **BSB:** import indítható (98,83%).
4. **Macula:** a #8 a 87 helyből 39-re kap görög Strong-számos gépi javaslatot; az SDBH-engedély tisztázandó, ha a domének is kellenek.
5. Hézagok: studybible.info licence, `scrollmapper/bible_databases` (nem mérhető), a `basokant` JSON relációszáma, a Macula–TAHOT verslista-eltérések oka.

## 5. Ellenőrzés és kimenetek

Kimenetek: `naplok/F06_nave.tsv`, `F06_kjv_asv.tsv`, `F06_bsb_genezis.tsv`, `F06_bsb_elteresek.tsv`, `F06_macula_lefedettseg.tsv`, `F06_macula_87_hely.tsv`, `F06_licenc.tsv`, `F06_koltseg.tsv`, `F06_licenc_szovegek/` (a licenc-/README-szövegek szó szerinti másolata, `INDEX.tsv`-vel), `F06_5_osszesito.py/.txt`. A független ellenőrzés: `naplok/ELLENOR_F06.md`. A zárás (`F06_zaras.md`, `FELADATOK.md`, PR) az orkesztrátor feladata.
