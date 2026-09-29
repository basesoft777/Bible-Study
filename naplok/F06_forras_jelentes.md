# F06_forras_jelentes.md — Új források 2. felmérése (FJ 2. menet)

*F06_FORRASFELMERES_BRIEF.md v1 · ág `claude/f06-forrasfelmeres` · 2026.09.29. · a mérés GitHub Actionsben futott (futások: 36606454914, 36607700736), helyi gép nem kellett.*

**Számok forrása.** Minden szám egy `naplok/F06_*.tsv` kimenetből származik, vagy a `naplok/F06_5_osszesito.py` kimenetéből (`naplok/F06_5_osszesito.txt`), amely ugyanezeket a fájlokat olvassa. A MiniMax kimenetéből szám nem került ide. A MiniMax ítéletei **javaslatok**, mindig a szó szerinti idézetük mellett szerepelnek; a végső licencdöntés a felhasználóé.

**Módszertani figyelmeztetés a licenc-ítéletekhez.** A `F06_licenc.tsv` 24 kapun átment sora közül 11 `nincs_adat` üres idézettel. Ezt nem szabad „a szövegben nincs licencinformáció”-ként olvasni: az `eng-kjv_usfm.zip#copr.htm`, az `eng-asv_usfm.zip#copr.htm` és az `elcafe7_lex/docs/LICENSING.md` szövege tartalmaz licencre vonatkozó állítást (lásd lent, saját szó szerinti olvasatom, **nem MiniMax-ítélet**). A `macula_hebrew` két fájlja (`LICENSE.md`, `README.md`) kétszer is elbukott az idézetkapun (`kezi_kapu`), ezért ott is saját olvasatot adok. Hat szöveg 12 000 karakter fölötti, ezek „kézi” jelölést kaptak (nincs darabolás): a `theonize_bible_database/LICENSE`, az `elcafe7_lex/docs/README.html`, a `kjvstudy.org` `kjvstudy_org/data/README.md`, a `KJV-Strongs-EBook` `LICENSE` és `README.md`, a `scripture-intelligence-server/README.md`.

## 1. Forrásonként

### Nave (N27) — `naplok/F06_nave.tsv`

| Jelölt | Mérés | Licenc | Javaslat | Indok |
|---|---|---|---|---|
| `basokant/nave` | elérhető (commit `4f35c7d4…`); `data/parsed-nave.json`: lista, 5322 elem; `data/nave.txt` 4 565 849 bájt; téma↔vers reláció **nem mérve** (a JSON belső szerkezetét a szkript nem bontja) | nincs LICENSE-fájl a gyűjtött fájlok között (csak `README.md`). Saját olvasat, szó szerint: „Based off of Nave's Topical Bible.” és „It also happens to be in the public domain.” (a README a Nave 1897-es művéről szól). MiniMax: `nincs_adat`, üres idézet | **FELTÉTELLEL** | a README a közkincs-állítást a műre (Nave 1897) teszi, nem a repó adatfájljaira; a README szerint az adat a naves-topical-bible.com oldal lekaparása („A scraper for Nave's Topical Bible from www.naves-topical-bible.com”), ennek az oldalnak a feltételeit nem vizsgáltuk |
| `theonize/bible_database` | elérhető (`0df2f992…`); `Topics.csv` 32253 sor, 4980 egyedi Topic; `TopicIndex.csv` 92609 reláció; mind a 92609 reláció könyve leképezhető a `Konyv_normalizalo_tabla.tsv`-re, 0 nem leképezhető (csak könyvszint, vers-szint nem ellenőrzött) | `LICENSE` 35141 karakter → **kézi** (12 000 fölött). Saját olvasat: a fájl első sora „GNU GENERAL PUBLIC LICENSE”, „Version 3, 29 June 2007”. A `README.md` 86 karakter, forrást nem nevez (MiniMax: `nincs_adat`) | **FELTÉTELLEL** | a legjobb szerkezet és kész reláció, de GPLv3 (copyleft), és a Nave-eredet sehol nincs kimondva |
| `elcafe7/lex` | elérhető (`4e777320…`); `topics` tábla 5319 sor; „KOD fej:vers” horgonyok: 40089 (alsó becslés), ebből 40088 leképezhető, 1 nem (`1JHN`) | MiniMax, idézettel: „Lex code is MIT licensed. Bible data and Lexicon content are subject to their respective upstream licenses.” (`README.md`). A `docs/LICENSING.md` az ismert adatforrások felsorolásában (saját olvasat) ESV-t, TSK-t, Strong's-t, STEPBible-t, UBS-t, Geocoding-ot, Easton-t, ISBE-t és a hitvallás-adatokat nevezi, Nave-et nem | **NEM** | az adat eredete és licence dokumentálatlan, a kód MIT-je az adatra nem terjed ki |

**N27:** a felmérés szintjén lezárható. A `basokant/nave` létezik (az FJ4 állítása téves volt), de a három közül nincs, amelyik licencszempontból tisztán importálható. **Hiányzik:** a felhasználó döntése arról, hogy a `basokant/nave` README-beli közkincs-állítása és a lekaparás elég-e, vagy a `theonize` GPLv3-a vállalható-e; a `basokant` JSON-jában a téma↔vers relációk számának mérése. Eltérés az FJ4-hez képest: az FJ4 32254 sort, 4951 főtémát és 92610 relációt jelzett a `theonize`-re, a mostani mérés 32253, 4980 és 92609; az okot nem tisztáztam.

### Teljes KJV/ASV (N29) — `naplok/F06_kjv_asv.tsv`

| Jelölt | Mérés | Licenc | Javaslat | Indok |
|---|---|---|---|---|
| **eBible.org USFM** (`eng-kjv_usfm.zip`, `eng-asv_usfm.zip`) | HTTP 200 mindkettő. KJV: 66 kanonikus könyv, 31102 vers, ebből 31099 `strong=` címkés; ASV: 66 kanonikus könyv, 31102 vers, ebből 30978 címkés (a KJV-zip az apokrifokkal együtt 81 könyvet tartalmaz) | saját olvasat a `copr.htm`-ból: KJV „Public Domain”, valamint „You may copy the King James Version of the Holy Bible freely.”; a szöveg egy UK-beli nyomtatási kizárólagosságot is említ (királyi szabadalom, csak az Egyesült Királyságban); ASV: „The American Standard Version of the Holy Bible is in the Public Domain. Copy freely.” MiniMax: `nincs_adat` | **IMPORT** | teljes, kanonikus, szó-szintű (`\w szó\|strong="…"`), közkincs-nyilatkozattal; az import-menet feladata a címke-formátum mintaellenőrzése (számformátum, többszámú címkék) |
| `luvlylavnder/bible-app-data` | KJV JSON: 66 könyv, 31102 vers, mind címkés; ASV JSON: 66 könyv, 31086 vers, mind címkés; Genezis 1:1 példa a kimenetben (`{H7225}` szó után) | MiniMax, idézettel: „All data is in the public domain and licensed under [CC0 1.0](LICENSE).” A repó gyökér `LICENSE`-e CC0 1.0. Ugyanakkor a `Bible-Versions/KJV/LICENSE` és `…/NIV/LICENSE` MIT (MiniMax, idézettel), a `KJV-Strongs/` mappának nincs saját licencfájlja | **FELTÉTELLEL** | teljes és feldolgozásra kész, de harmadik fél csomagolása, a címkézés eredete nincs megnevezve; ellenőrző másodforrásnak alkalmas |
| studybible.info | HTTP 200 a `KJV_Strongs/Genesis%201` és `ASV_Strongs/Genesis%201` oldalra | **nem gyűjtöttük** | **NEM (hézag)** | a meglévő táblák forrása, de a licencét ez a menet nem vizsgálta; oldalankénti lekaparás |
| `RonTurrentine/KJV-Strongs-EBook` (`kjv.osis.xml`) | 355850 `lemma="strong:…"` címke; lefedettség nem mérve | GPL-3.0 (README: „License” szakasz, a `LICENSE` kézi) | **NEM** | copyleft, nincs szükség rá az eBible mellett |
| `kennethreitz/kjvstudy.org` | nincs tömeges, KJV/ASV nevű, címkézett adatfájl (a kimenet csak sablon- és tanulmány-JSON-t mutat) | ISC (MiniMax, idézettel) | **NEM** | web-alkalmazás, nem adatforrás |
| `1John419/kjs`, `kaiserlik/kjv`, `Realbizdigital/scripture-intelligence-server` | a szkript a KJV/ASV nevű fájlokban nem talált címke-mintát (`szo_szintu_strong_bizonyitek = nem`) | `1John419/kjs`: GPL-3.0; `kaiserlik/kjv`: nincs licencfájl; `scripture-intelligence-server`: MIT (kód) | **NEM** | nincs mérhető szó-szintű címke, ill. licenchiány |
| `scrollmapper/bible_databases` | **nem mérhető**: a klón ismételten időtúllépett (az első futásban 900 mp, utána 420 mp) | — | nem minősítve | nyitott hézag; az eBible megléte mellett nem szükséges a döntéshez |

A GitHub-keresés négy lekérdezése 10, 0, 2 és 0 találatot adott (`kereses:` sorok).

**N29:** lezárható. Van elérhető, licenccel (közkincs-nyilatkozattal) ellátott, teljes, szó-szintű Strong-címkézésű forrás (eBible USFM). **Hiányzik:** a felhasználó döntése; az import előtti mintaellenőrzés (címke-formátum, TAHOT-hoz mért egyezés) az import-menet dolga.

### BSB (N30) — `naplok/F06_bsb_genezis.tsv`, `naplok/F06_bsb_elteresek.tsv`

- **Rögzített feltétel (mérés előtt, `eszkozok/fj2/kuszob.txt`):** küszöb 95%; egyezés = a vers TAHOT Strong-halmaza része a BSB-halmaznak, a 9000-es és afeletti prefixkódok nélkül; nevező = a TAHOT-tal rendelkező versek. **A nevezőt a felhasználó a javaslat részeként hagyta jóvá** (kifejezetten nem vitatta); a küszöböt és a definíciót jóváhagyta.
- **Mérés (BSB commit `a4a2c055…`):** 1533 vers; mind a 1533 TAHOT-lefedett (`nincs_tahot = 0`, így a két nevező azonos); 1515 egyezik, 18 eltér: **98,83%** (a fájl fejléc-sorából); eredmény **ELÉRI** a 95%-ot. Átlagos Jaccard 99,83%.
- **Az eltérések** (18 sor, mind `tahot_nincs_a_bsb-ben`): közülük 7 a TAHOT 2895 (BSB 2896, טוֹב), ez az FJ3-ban már látott TAHOT-tövesítési eltérés.
- **Licenc:** a `README.md` táblázata, MiniMax idézettel: „`base/display/` | CC0 (Public Domain) | No” és „`base/index-cc-by/` | CC-BY 4.0 | **Yes**”; a `LICENSE-CC0.md` és `LICENSE-CC-BY.md` kapun átment. Az import célja a `base/display/` (CC0).
- **Javaslat: IMPORT.** **N30:** lezárható, a feltétel (teljes Genezis-összevetés, előre rögzített küszöb) teljesült és eléri a küszöböt. Megjegyzés: a `CLAUDE.md` szerint a TAHOT-kivonatból hiányzik az 1Móz 32; a mérésben az 1Móz 32-nek van TAHOT-sora (a `nincs_tahot = 0`), tehát a hiány legfeljebb tartalmi, nem versszintű; ezt nem vizsgáltam tovább (az 1Móz 32:28 az eltérések között szerepel).

### Macula Hebrew (N31) — `naplok/F06_macula_lefedettseg.tsv`, `naplok/F06_macula_87_hely.tsv`

- **Lefedettség (commit `47db250b…`):** 39 könyv, 929 `lowfat`-fájl, egyik könyvnél sem 0 a fájlok száma. Az 1Sám–2Krón mind a hat könyve megvan: 167 fájl, 4807 Macula-vers a TAHOT 4806 versével szemben, 4772 közös. Összesen 23213 Macula-vers, 23179 TAHOT-vers, 23045 közös; 14 könyvnél teljes az egyezés a verslistában (a többi eltérés versszámozási: pl. Jób 42 csak Maculában, Jóel 21 csak Maculában).
- **Az FJ1 „hiánya”:** az 1Sám–2Krón megvan, tehát nem letöltési hiba. A magyarázat valószínűleg az FJ1 szkriptek fájlnév-mintája (`^\d+-([A-Za-z]+)-…`), amely számjegyre kezdődő fájlkódot (`1Sam`) nem illeszt; ez a mintából következő hipotézis, az FJ1 futását nem reprodukáltam.
- **Licenc:** saját olvasat, szó szerint a `LICENSE.md`-ből: „is licensed under [CC BY 4.0 ]”, „Greek equivalents drawn from the Septuagint” és „Strong's numbers for both Hebrew and Greek equivalents”. MiniMax: `kezi_kapu` (kétszer bukott az idézetkapun).
- **Javaslat: FELTÉTELLEL.** A licenc rendben (CC BY 4.0, forrásmegjelölés kell), és az FJ1 a szó-szintű MT–LXX-illesztésre 78%-ot mért; a G8 tagmondat-tagoláshoz és a 87 hely kiinduló javaslatához használható, importja nem javasolt a küszöb miatt.
- **N31:** lezárható. A letöltés teljes.

## 2. A #8-nak átadott rész — a 87 függő hely (`naplok/F06_macula_87_hely.tsv`)

| Állapot | Sor | ebből azonosítás |
|---|---|---|
| **LXX_MEGFELELO** (a Macula a talált héber szóhoz görög Strong-számot rendel) | **39** | 37 `strong`, 2 `szoalak` |
| HEBER_SZO_GOROG_NELKUL (a héber szó megvan, görög társ nincs rendelve) | 38 | 26 `strong`, 12 `szoalak` |
| HEBER_SZO_NINCS_A_VERSBEN | 8 | |
| NINCS_VERS | 2 | |

**A Macula tehát 39 függő helyre (a 87-ből) ad LXX-megfelelőt.** Figyelmeztetések a #8-nak: (1) a munkalap igehelyei Károli-számozásúak, a Macula héber; számozás-átalakítás nem történt, a 8 + 2 nem talált sor részben ebből adódhat (N28); (2) az `azonositas = szoalak` sorok (2 + 12) a munkalap hiányzó `heber_strong` mezője miatt ékezet nélküli szóalak-egyezésen alapulnak, gyengébb bizonyosságúak; (3) az FJ1 a Macula szó-szintű illesztését 78%-osnak mérte, tehát a 39 sor **javaslat, kézi megerősítést igényel**, nem döntés.

## 3. MiniMax-költség (`naplok/F06_koltseg.tsv`)

29 hívás (`minimax/minimax-m3`, OpenRouter), összesen **0,011927 USD** (a plafon 1 USD); a hívások 7 különböző providerhez mentek (CoreWeave, GMICloud, Minimax, ModelRun, SambaNova, StreamLake, Together). Az újrafuttatás a már kapun átment ítéleteket nem kérdezte újra. A 32 elemzett szövegből 24 ment át a kapun, 6 „kézi_hosszu” (nincs darabolás), 2 „kézi_kapu” (Macula).

## 4. Nyitott pontok, amelyek a felhasználó döntésére várnak

1. **Nave:** `basokant/nave` (közkincs-állítás + lekaparás) vagy `theonize` (GPLv3), vagy egyik sem.
2. **KJV/ASV:** eBible USFM (javasolt), esetleg a `luvlylavnder` másodforrásként.
3. **BSB:** import indítható (98,83%).
4. **Macula:** a #8 a 87 helyből 39-re kap gépi javaslatot.
5. Hézagok: studybible.info licence, `scrollmapper/bible_databases` (időtúllépés), a `basokant` JSON relációszáma.

## 5. Ellenőrzés és kimenetek

Kimenetek: `naplok/F06_nave.tsv`, `F06_kjv_asv.tsv`, `F06_bsb_genezis.tsv`, `F06_bsb_elteresek.tsv`, `F06_macula_lefedettseg.tsv`, `F06_macula_87_hely.tsv`, `F06_licenc.tsv`, `F06_koltseg.tsv`, `F06_licenc_szovegek/` (a licenc-/README-szövegek szó szerinti másolata, `INDEX.tsv`-vel), `F06_5_osszesito.py/.txt`. A fuggetlen-ellenor (`naplok/ELLENOR_F06.md`) és a zárás (`F06_zaras.md`, `FELADATOK.md`, PR) az orkesztrátor feladata.
