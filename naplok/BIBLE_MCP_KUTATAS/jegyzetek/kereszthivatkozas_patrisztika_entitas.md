# A bible-mcp kereszthivatkozás-, patrisztikus idézet- és entitásrétege — eredet, minőség, illeszkedés a PaRDeS-munkamenethez

*Kutatási jegyzet, 2026-10-16. Kutató modell: claude-opus-5-5. Csak olvasás a repón; a mérő szkript a session scratchpadjában (`kh_osszevet.py`, `python -I`, `split('\t')`).*

**Jelölés.** **[MÉRT]**: saját MCP-hívás vagy repó-lekérdezés, a hívás pontos alakjával. **[FORRÁS]**: webes vagy repóbeli dokumentum. **Következtetés**: értelmezés, külön szakaszban.

**Az MCP-hívások (2026-10-16, a hostolt szerver, `mcp__c545d7fb-…`):**
`corpus_info()`; `get_cross_references(reference=…, limit=50)` a következőkre: „Genesis 14:18”, „Psalm 110:4”, „Hebrews 7:1”, „Genesis 1:2”; `get_citations(reference=…, limit=50)` a következőkre: „Psalm 110:4”, „Psalm 110:1”, „Isaiah 53:5”, „Isaiah 53:7”, „Isaiah 53” és „Genesis 14:18”; `search(query="Melchizedek OR Melchisedek OR Melchisedec", version="JUSTIN-DIAL", limit=30)`; `search(query='"as a sheep to the slaughter"', version="JUSTIN-1AP")`; `entities_in_passage("Genesis 14:18")`; `get_entity("Melchizedek")`; `get_entity("Salem", entity_type="place")`.

---

## 1. Kereszthivatkozások: forrás, súlyozás, irány, típus; összevetés a repó Károli_KH és TSK tábláival

### Takeaway
A 344 799 link az **OpenBible.info** kereszthivatkozás-táblája (ez túlnyomórészt a TSK-ból származik), **közösségi szavazatokkal súlyozva**. A linkek **irányítottak** (A→B ≠ B→A), és **nincs típusuk**. Ugyanez az adat **már bent van a repóban**: a `konkordancia/TSK_kereszthivatkozasok.tsv` név alatt, egy régebbi szavazat-pillanatképpel. A négy tesztversen az MCP linkjeinek **100%-a megvan ebben a fájlban**. Az MCP-réteg tehát **nem új adat**, csak frissebb szavazatszám és angol céltextus. A Károli saját kereszthivatkozásai (Karoli_KH) ennél nagyságrenddel szűkebbek.

### Cited Findings
- **[FORRÁS]** Az MCP-eszköz leírása: „Cross-references for a verse (OpenBible.info, ranked by community votes), with the target text included.” — `get_cross_references` tool-séma. A `corpus_info()` 344 799 linket közöl. — [bible-mcp README](https://github.com/nirajagarwal/bible-mcp)
- **[FORRÁS]** Az OpenBible.info a saját adatáról: „draws primarily from public-domain sources, especially the Treasury of Scripture Knowledge, which provides most of the data”. Kb. 340 000 hivatkozás. A kezdeti szavazatokat a saját Topical Bible és Twitter Bible Search adataiból vetették be („seed the initial votes”). Letöltés: `https://a.openbible.info/data/cross-references.zip` (2 MB). Licenc: Creative Commons Attribution (link: CC BY 4.0). Dátumot és verziót az oldal nem ad, a szavazás menetét nem írja le. — [OpenBible.info Cross References](https://www.openbible.info/labs/cross-references/)
- **[FORRÁS]** A bible-mcp README szerint a réteg „OpenBible.info, ~345,000 ranked links, CC BY”. A szavazat-pillanatkép dátuma nincs megadva, és a release-jegyzetek (v0.9–v0.14.1) sem közlik. — [bible-mcp README](https://github.com/nirajagarwal/bible-mcp), [bible-mcp releases](https://github.com/nirajagarwal/bible-mcp/releases)
- **[FORRÁS, repó]** A repó `TSK` sora a `adat/licencek.tsv` 22. sorában: forrás „scrollmapper/bible_databases GitHub-tükör, cross_references_0..6.sql, letöltve 2026-08-26 (master); commit nincs”. Licenc: „CC BY (az OpenBible.info licenc-oldala szerint …)”. Szó szerinti idézetként rögzíti az OpenBible „draws primarily from … Treasury of Scripture Knowledge” mondatát. → **A repó „TSK” nevű táblája valójában az OpenBible-tábla**, a fejlécében `Votes` oszloppal.
- **[FORRÁS, repó]** Az `adat/datasetek.tsv` 106–109. sora az `openbible_crossrefs` datasetet külön, „JELÖLT, NEM IMPORTÁLT” (`hianyzik`, F44 3b, DT33/DT34) tételként vezeti, és megjegyzi: „főleg a TSK-ból ered”. Ugyanakkor a 20/38/56/74. sor a `TSK`-t `elerheto`-ként, „mindig” kötelezőként tartja nyilván. **A két sor ugyanarra az adatra vonatkozik** (l. a következtetéseket).
- **[MÉRT]** `TSK_kereszthivatkozasok.tsv`: 432 949 adatsor (fejléc nélkül). Oszlopok: `Igehely | Kapcsolódó igehely | Kapcsolódó igehely magyar megjelenítése | Votes`, magyar igehely-alakban (`1Móz 1:1`). Egy tartomány (pl. `Mt 26:26-29`) két sorra bomlik, kezdő- és zárósorra. Ez magyarázza, miért több a sor (432 949), mint az MCP-link (344 799).
- **[MÉRT]** Összevetés kezdővers szerint (`kh_osszevet.py`):

| Vers | MCP-linkek | ebből a repó TSK-fájlban | Karoli_KH sorai | MCP ∩ Karoli_KH |
|---|---|---|---|---|
| 1Móz 14:18 | 16 | 16 (100%) | 2 (`Heb.7.1-Heb.7.2`, `Heb.7.3`) | 0 kezdővers szerint; tartalmilag mindkettő benne van az MCP `Heb.6.20-Heb.7.3` tartományában |
| Zsolt 110:4 | 13 | 13 (100%) | 3 (`Heb.5.6`, `Heb.6.20`, `Heb.7.17`) | 3 (a Károli mind benne) |
| Zsid 7:1 | 14 | 14 (100%) | 1 (`Gen.14.18-Gen.14.20`) | 1 |
| 1Móz 1:2 | 8 | 8 (100%) | **0** | — |

  A „csak a TSK-fájlban” maradó 1–3 sor versenként mind tartomány-zárósor (pl. `Mt 26:29`, `Zsid 7:22`, `Zsid 7:3`, `Ézs 40:14`), tehát valódi többlet nincs.
- **[MÉRT]** **A szavazatszámok eltérnek; az MCP a frissebb pillanatkép.** 1Móz 1:2 → Jer 4:23: MCP 101, repó 84. → Zsolt 104:30: 75 vs 61. → Ézs 45:18: 67 vs 55. → Náh 2:10: **−26** vs −14. 1Móz 14:18 → Zsolt 110:4: 19 vs 14. Zsolt 110:4 → Zsid 7:17: 27 vs 25. A sorrend nagyjából stabil, az abszolút érték nem.
- **[MÉRT]** **Irányítottság.** A pár a két irányban más súllyal és más alakban szerepel. 1Móz 14:18 → Zsolt 110:4: 19 szavazat. Zsolt 110:4 → 1Móz 14:18: 17. 1Móz 14:18 → `Heb.6.20-Heb.7.3`, de Zsid 7:1 → `Gen.14.18-Gen.14.20`.
- **[MÉRT]** **Típus nincs.** A kimenet csak `[cél] (votes: n) szöveg`. Nem jelzi, hogy idézet, allúzió, tematikus vagy lexikai kapcsolatról van-e szó. A gyenge, asszociatív linkek ugyanúgy jönnek, mint az idézetek. Példák: 1Móz 14:18 → Gal 6:10 (2), → 2Sám 2:5 (1), → Ruth 3:10 (3), csak a „blessed” szón át; Zsid 7:1 → 1Móz 16:14-16 (5).
- **[MÉRT]** **Negatív szavazatú link is visszajön, szűrés nélkül:** 1Móz 1:2 → Náh 2:10 (votes: −26).
- **[MÉRT]** **A céltextus fordítása vegyes.** Ugyanazon a listán BSB-mondat („The LORD has sworn…”) és WEB-mondat („…by Yahweh, my daughter”, „Yahweh Most High”) is áll. A visszaadott szöveg forrásverziója a sorból nem derül ki.
- **[MÉRT]** A `limit=50` mellett a válasz 8–16 találat volt. Ez a négy versnél egyezik a repó-fájl teljes kezdővers-halmazával, tehát a szerver itt nem vágott le semmit.

### Inferences
- Az MCP kereszthivatkozás-rétege a projektnek **nem új dataset**, hanem a meglévő `TSK_kereszthivatkozasok.tsv` (valójában OpenBible) **frissebb szavazatú, élő nézete**. A determinisztikus munkamenethez a repó-fájl a jobb: verziózott, helyben greppelhető, magyar igehely-alakú, és nem függ hálózattól. Az MCP egyetlen többlete a frissebb szavazatszám. Ez tényleges előny csak akkor, ha a rangsor (votes) bekerül a döntésbe.
- **Névadási és katalógus-ellentmondás a repóban** (javaslat, nem döntés). A `TSK` sor (`elerheto`, forrás: scrollmapper OpenBible-SQL) és az `openbible_crossrefs` sor (`hianyzik`, „nem letöltve”) ugyanannak az adatnak két katalógus-sora. Az `openbible_crossrefs` „import: külön feladat (DT34)” tétele gyakorlatilag már teljesült, csak más néven és scrollmapper-tükörből. A közvetlen `cross-references.zip` letöltése (dátummal és sha256-tal) javítaná a provenienciát: a mostani sor „commit nincs”. Ez tartalmi döntés, a `DONTESEK.md`-be tartozik.
- A Károli_KH és az OpenBible **kategóriában más**. A Károli_KH egy kiadás szerkesztői apparátusa: kevés, főleg idézet- és párhuzamhely-link, az 1Móz 1:2-nél üres. Az OpenBible tömeges, rangsorolt jelöltlista. A Károli_KH így „magas pontosság, kis lefedettség”, az OpenBible „nagy lefedettség, sok asszociatív zaj”. A projekt 3. szabálya („hiányt soha ne tölts ki gyenge vagy asszociatív anyaggal”) miatt az OpenBible-sor **csak jelölt lehet**, egyedi minősítéssel. A `datasetek.tsv` TSK-sora ezt már előírja („minden jelölt egyedi minősítést kíván (sablon Q2)”).
- A votes **nem minőségi bizonyíték**, hanem népszerűségi rangsor. A −26-os Náh 2:10 mutatja, hogy a közösség hibás linket is jelöl, és ezt a szerver nem szűri. Küszöböt (pl. votes ≥ 5) csak rangsorolásra érdemes használni, kizárásra nem; és ha a küszöb szerepet kap, a provenienciába kell írni.
- A vegyes BSB/WEB céltextus miatt az MCP-ből vett angol szövegrészlet nem idézhető forrásként verziójelölés nélkül. A projekt amúgy is Károlira kulcsol, így ez legfeljebb kényelmi szöveg.
- **Javasolt provenienciasor**, ha mégis az MCP-ből jön lekérdezés (a SEMA 1.5 kötelező kulcsai mellé verzió és pillanatkép):
  `scope=range:Zsolt 110:4 | forras=bible-mcp:get_cross_references (OpenBible.info, CC BY 4.0) | szerver=bible-mcp v0.14.x @ bible-mcp-server.fly.dev | limit=50 | n=13 | votes_pillanatkep=ismeretlen | ts=2026-10-16T…Z`
  A `votes_pillanatkep=ismeretlen` kötelezően kiírandó, mert a szerver nem közli. A repó-fájlból jövő sor: `scope=range:… | forras=TSK_kereszthivatkozasok.tsv (OpenBible via scrollmapper, 2026-08-26) | n=… | ts=…`.
- A `jeloltek.tsv` `forras_kereses` mezőjébe ilyen érték kerül: `OpenBible Zsolt 110:4 (votes 27)` vagy `TSK 1Móz 14:18`. A sémában a `TSK 1Móz 6:4` minta már szerepel. Ha a votes számít, külön mező kellene; ez sémadöntés.

### Gaps
- Az OpenBible zip **verziója és dátuma** nem derült ki, sem az OpenBible oldalán, sem a bible-mcp release-jegyzeteiben. Hogy a két pillanatkép pontosan mikori, nem mérhető.
- A szavazási mechanizmust (ki szavaz, mikor frissül a zip) az OpenBible oldal nem írja le.
- A teljes korpuszon nem mértem, hány TSK-sor esik egybe a Károli_KH-val. Ehhez a 432 949 soros fájl teljes összevetése kellene; a négy vers csak minta.
- Nem ellenőriztem, hogy az MCP-réteg a 344 799 linkből szűr-e valamit (pl. negatív votes küszöb alatt). A Náh 2:10 (−26) visszajött, tehát legalább ezt nem.

---

## 2. Patrisztikus idézetek: kinyerés, megbízhatóság, művek; illeszkedés a 7. lépéshez és a Drash-szinthez

### Takeaway
A 2 479 idézet a fordítók (ANF I, Roberts–Donaldson–Crombie) lábjegyzeteiből gépileg kinyert igehely-hivatkozás („tier 1”). A **pontosság jónak tűnik, a lefedettség gyenge**: a Zsolt 110:4 Jusztin-féle szó szerinti idézeteinek többsége és az Ézs 53:5/7 1. Apológia-beli teljes idézete nincs az indexben. A réteg **nem illik a 7. lépéshez**, mert a jóváhagyott tanítói lista csak modern pünkösdi és karizmatikus tanítókat tartalmaz, egyházatyát egyet sem. Recepciótörténeti (Drash) támaszként használható, jelöltként, de üres eredménye **nem negatív lelet**.

### Cited Findings
- **[FORRÁS]** A tool-leírás: „extracted from the translators' own footnotes (tier 1)… COVERAGE NOTE: footnote extraction has known recall gaps — an empty result is normal and does NOT mean the verse is uncited; full-text `search` within the patristic works is the thorough probe”. — `get_citations` tool-séma
- **[FORRÁS]** A bible-mcp README szerint a tier 1 a fordítói lábjegyzetekből jön (Irenaeus 1 598, Justin ~408), a tier 2 („shingling”, szövegegyezéses idézetkeresés) **még nem készült el**, a roadmap következő tétele. A README egyik sora az Irenaeust bent lévőként, a roadmap-sor „source acquisition” alatt említi; a két állítás nem teljesen egybevágó. — [bible-mcp README](https://github.com/nirajagarwal/bible-mcp)
- **[FORRÁS]** A `corpus_info()` szerint a művek a következők. Apostoli atyák (1–2 Kelemen, Barnabás, Polükarposz és vértanúsága, Ignác rövidebb recenzió, Ignác vértanúsága, Diognétosz, Hermász, Papiasz): „Project Gutenberg #77576”. Irenaeus (Adversus haereses I–V, töredékek) és Jusztin (1–2. Apológia, Dialógus Trüphónnal, vértanúság): „Wikisource transcription of ANF I”. Mind „Public Domain”. Ágoston *Vallomásai*, *Krisztus követése*, Bunyan, Lőrinc testvér, Norwichi Julianna és Chesterton szintén bent van, de ezekhez **nincs idézet-index**: csak az apostoli atyáknál, Irenaeusnál és Jusztinnál áll a „Tier-1 citations” megjegyzés.
- **[FORRÁS]** PG #77576: *The writings of the Apostolic Fathers*, fordítók Frederick Crombie, James Donaldson és Alexander Roberts (Ante-Nicene Christian Library vol. 1, T. & T. Clark 1870). Kiadva 2025-12-30, „Public domain in the USA”. — [Project Gutenberg #77576](https://www.gutenberg.org/ebooks/77576)
- **[FORRÁS]** A bible-mcp levezetett adata (versemap, „citation graph”, embeddingek) **CC BY-NC 4.0**, a kód **PolyForm Noncommercial 1.0.0**. A forrásszövegek a saját licencüket tartják meg. — [bible-mcp README](https://github.com/nirajagarwal/bible-mcp)
- **[MÉRT] Zsolt 110:4.** A `get_citations` 2 találatot adott: `JUSTIN-DIAL.63.2` (szó szerinti idézet, helyes) és `JUSTIN-DIAL.118.1` (utalás: „the Lord swore, ‘after the order of Melchizedek’”, helyes). A `search(... version="JUSTIN-DIAL")` további **szó szerinti** Zsolt 110:4-idézeteket talált, **amelyek nincsenek az indexben**: `JUSTIN-DIAL.32.2` (a teljes Zsolt 110 idézve), `JUSTIN-DIAL.33.1` (kétszer szó szerint, a Hiszkija-értelmezés cáfolatával) és `JUSTIN-DIAL.83.1` (Zsolt 110:1–4 idézve). Utalásként ugyancsak hiányzik a `JUSTIN-DIAL.19.3` („after whose order God declared, by the mouth of David…”) és a `JUSTIN-DIAL.113.1` („king of Salem after the order of Melchizedek”). → Csak a Dialóguson belül: **5 szó szerinti vagy formulás előfordulásból 2 indexelt** (két szó szerinti hiányzik), az utalások közül 1 indexelt és 2 hiányzik.
- **[MÉRT] Zsolt 110:1.** 10 találat (1Kel 36.1, Barn 12.1, Irenaeus 5 helyen, 1Apol 45.1, Dial 56.15 és 127.1). Ugyanakkor a fent megtalált `JUSTIN-DIAL.32.2` és `JUSTIN-DIAL.83.1`, amelyek a Zsolt 110:1-et szó szerint idézik, **nincsenek köztük**.
- **[MÉRT] Ézs 53.** Fejezetszintű hívás („Isaiah 53”) → „Please give a specific verse”: csak versszintű lekérdezés lehetséges. Ézs 53:7: 6 találat (Irenaeus AH 3.12.8, 4.23.2, 4.33.1, 4.33.12; Jusztin Dial 111.1, 114.1). Ézs 53:5: 1 találat (Barn 5.1). A `JUSTIN-1AP.50.1` szó szerint idézi az Ézs 52:13–53:8-at, benne az 53:5-öt („by His stripes we are healed”) és az 53:7-et („He was brought as a sheep to the slaughter”). A `search('"as a sheep to the slaughter"', version="JUSTIN-1AP")` megtalálja, de **egyik versnél sincs az indexben**.
- **[MÉRT]** 1Móz 14:18 → „No patristic citations found”, pedig a `JUSTIN-DIAL.19.3` és `33.1` Melkisédek papságát a 1Móz 14 alapján tárgyalja („as Melchizedek was described by Moses as the priest of the Most High… blessed the circumcised Abraham who brought him tithes”).
- **[MÉRT]** Az index-találat egy 200 karakteres részletet ad az elejéről. Hogy a passzus melyik pontján áll az idézet, és idézet vagy utalás-e, azt nem jelzi; az ellenőrzéshez a `read_work`/`search` kell.
- **[FORRÁS, repó]** A 7. lépés („nevesített tanító (web) — önálló menet, saját fájl”, CLAUDE.md) a `tanito-kereso` subagenttel fut. A subagent kizárólag a `sablonok/PaRDeS_tanitok_lista.md` jóváhagyott listájából választhat, és „más forrást nem vonsz be”. A lista (v1, 2026.08.01) Mumford, Basham, Baxter, Simpson, Prince, Hagin, Copeland, Oral Roberts, Osborn, Capps, Wigglesworth, Lake, Bosworth, Kuhlman, Lindsay, Wommack, Savelle és Price nevét tartalmazza. **Egyházatya nincs rajta.** A lista kimondja, hogy az akadémiai kör „más kategória, más forrás-szabályokkal”.

### Inferences
- **Pontosság és lefedettség.** A mintában minden index-találat valódi idézet vagy egyértelmű utalás volt: hamis pozitívot nem láttam. A lefedettség viszont versenként erősen hiányos: Zsolt 110:4-nél a Dialóguson belül a szó szerinti idézetek kb. 2/4-e hiányzik, Ézs 53:5-nél a legismertebb jusztini idézet. Ez egyezik a szerver saját figyelmeztetésével. A lábjegyzet-alapú kinyerés oka valószínűleg az, hogy az ANF fordítók egy hosszú idézetblokknál csak egyszer lábjegyzetelnek, és a lábjegyzet gyakran csak a kezdőverset (pl. „Ps. cx. 1”) adja meg. Ez következtetés, nem mért adat.
- **A projekt 3. szabályából** az következik, hogy a `get_citations` üres vagy rövid eredménye **soha nem írható „nincs patrisztikus recepció”-ként**. A korrekt menet kétlépcsős. (a) `get_citations` a versre. (b) Kötelező full-text `search` minden patrisztikus `version`-re, a vers kulcsszavaival vagy angol (ANF-) szövegével. Mindkettőt külön provenienciasorral kell naplózni. A (b) ugyanakkor szómező-keresés, tehát a 2. lépéshez hasonlóan generatív elem, a kulcsszavakat naplózni kell.
- **A 7. lépéshez nem illik** a lista mostani állapotában. Ha a felhasználó egyházatyákat akarna nevesített tanítóként, az a lista bővítését vagy egy új, „patrisztikus recepció” kategóriát jelentene. Ez **tartalmi döntés** (`DONTESEK.md`, majd megállás), nem kutatói hatáskör.
- **Drash-szint.** A tipológiai és krisztológiai olvasat (Jusztin: Melkisédek mint a körülmetéletlenek papja; Zsolt 110 a Hiszkija-olvasattal szemben) korai, datálható recepciótörténeti adat. Értelmező bekezdést alátámaszthat, **forrásmegjelöléssel (mű.fejezet.szakasz)**. Motívum-előfordulást a `elofordulasok.tsv`-be viszont nem termelhet, mert patrisztikus szöveg nem bibliai igehely. Ha ilyen adat táblába kerül, inkább a `lexikon_hivatkozasok.tsv`-hez vagy egy külön recepciós táblához hasonló helyre illik; ez sémadöntés.
- **Licenc.** A forrásszövegek PD-k (PG és Wikisource ANF I). A **kinyert idézetgráf** viszont a bible-mcp levezetett adata, **CC BY-NC 4.0**. Ha a projekt bulkban átveszi, NC-kötöttséget örököl. A szövegből saját kinyerés ezt elkerülné.
- **Javasolt provenienciasor:**
  `scope=range:Zsolt 110:4 | forras=bible-mcp:get_citations (tier-1, ANF I lábjegyzet; PG #77576 + Wikisource ANF I; származtatott adat CC BY-NC 4.0) | n=2 | lefedettseg=hianyos (szerver-figyelmeztetés) | ts=…`
  A kiegészítő full-text keresés sora: `scope=range:Zsolt 110:4 | forras=bible-mcp:search version=JUSTIN-DIAL q="Melchizedek OR Melchisedek OR Melchisedec" | n=7 | ts=…`.

### Gaps
- Tier 2 (shingling) nincs. Hogy a teljes 2 479-es indexben mekkora a lefedettség, nem mérhető, csak versenként, mintán.
- Hogy az ANF lábjegyzetek bibliahivatkozásai milyen versszámozást követnek (KJV vagy LXX Zsoltár-számozás; a lábjegyzetek római fejezetszámai, pl. „Ps. cx.”), és ezt a szerver hogyan normalizálja, nem derült ki.
- Irenaeusnál nem végeztem full-text recall-próbát; a hiány-arány csak Jusztinra mért.
- Ágoston *Vallomásai* és a többi PG-klasszikus idézet-indexe hiányzik: csak full-text kereshetők.

---

## 3. Entitások: forrás, mezők, összevetés a TIPNR_kivonat.tsv-vel

### Takeaway
Az entitásréteg a **Theographic Bible Metadata** (CC BY-SA 4.0). A Theographic maga **részben a STEPBible TIPNR-ből** készült, ezért a repó `TIPNR_kivonat.tsv`-jével **nem független**: a Melkisédek-próbán a versek halmaza azonos. Többlete Easton-leírás, nem és koordináta. A TIPNR-hez képest viszont **hiányzik** belőle a Strong-szám, ami a projekt gerince. A projekt számára a TIPNR az elsődleges, a Theographic legfeljebb geo- és kronológiai kiegészítő.

### Cited Findings
- **[FORRÁS]** A `get_entity` tool leírása: „(Theographic knowledge graph)”. A `corpus_info()` 4 814 entitást és 53 133 entitás–vers említést ad. A README: „Theographic, ~4,800 people/places/events/groups and 53,000 verse links | CC BY-SA 4.0”. — [bible-mcp README](https://github.com/nirajagarwal/bible-mcp)
- **[FORRÁS]** Theographic: licenc **CC BY-SA 4.0**. Formátumok: JSON (preferált, táblánként egy fájl), CSV, GeoJSON (Linked Places), Neo4j és GraphQL API. Darabszámok: 3 067 személy, 1 298 hely, 450 esemény, 23 népcsoport, 6 519 Easton-szócikk. Mezők: személyeknél név, családi kapcsolatok, születési és halálozási hely és év; helyeknél koordináta, típus, más nevek; eseményeknél dátum, résztvevők, helyszín. A szöveg a KJV 1769: „Every verse of the King James Version (1769) is linked to the people, places, events, and dictionary entries it mentions.” Kronológia: Floyd Nolen Jones. — [Theographic GitHub](https://github.com/robertrouse/theographic-bible-metadata)
- **[FORRÁS]** A Theographic forrásjegyzéke szerint a személyeket, kapcsolatokat és versjelöléseket a **STEPBible TIPNR**, a Marshall Genealogy és a Complete Bible Genealogy alapján azonosították. A helykoordináták az **OpenBible.info Bible Geocoding** adatai (`openBibleLat`/`openBibleLong`). Az Easton a CCEL XML kiadásából van parszolva. A `verses.yearNum` a TSK dátumaiból jön. Hogy a versjelölés gépi vagy kézi volt, a forrásjegyzék nem mondja meg. — [Theographic data-source-bibliography](https://github.com/robertrouse/theographic-bible-metadata/blob/master/docs/data-source-bibliography.md)
- **[FORRÁS]** Az Easton a bible-mcp-ben 2 491 szócikk, „via Theographic's structured JSON re-derivation”. A Theographic 6 519 tételt közöl; az eltérés oka (töredék-összevonás: „itemNum fragments concatenated”) a `corpus_info()`-ból következik, nem mért.
- **[MÉRT]** A `get_entity("Melchizedek")` a nevet nem pontosan, hanem előtag szerint egyezteti: Melchi (×2), Melchiah és Melchisedec (KJV-alak, `id=recV4oVk0yumm0aol`, Airtable-rekord). Mezők: `gender=Male`, Easton-kivonat, „Mentions (11 total)”: Gen.14.18, Ps.110.4, Heb.5.6, 5.10, 6.20, 7.1, 7.10, 7.11, 7.15, 7.17, 7.21.
- **[MÉRT]** A `TIPNR_kivonat.tsv` Melchizedek-sorai: H4442 (Gen.14.18, Psa.110.4) és G3198 (Heb.5.6, 5.10, 6.20, 7.1, 7.10, 7.11, 7.15, 7.17, 7.21) — **ugyanaz a 11 vers**, de nyelvenkénti Strong-számmal és fordításonkénti névváltozattal („=ESV,NIV; Melchisedec =KJV”). A fájl 35 523 sort és 2 737 egyedi normalizált nevet tartalmaz; mezői: `Név (normalizált) | Névváltozat | Strong-szám | Nyelv | Igehely`.
- **[MÉRT]** **Azonosítási különbség (Salem).** A Theographic a `Salem`-et önálló helyként vezeti (`featureType=City`, koordináta: 31.777444, 35.234935, ez Jeruzsálem), 4 említéssel: Gen.14.18, Heb.7.1, Heb.7.2, Ps.76.2. A TIPNR ugyanezt a 4 verset `Jerusalem` normalizált név alatt, `Salem` névváltozatként adja (H8004 és G4532). Mindkettő **értelmező azonosítás**: Szálem = Jeruzsálem. A Theographic a koordinátában, a TIPNR a normalizált névben rögzíti.
- **[MÉRT]** Az `entities_in_passage("Genesis 14:18")` eredménye: személyek: Melchisedec, God; helyek: Salem. „God” is entitásként szerepel.

### Inferences
- Mivel a Theographic versjelölése a TIPNR-ből (is) ered, a két forrás egyezése **nem független megerősítés**. A projekt `megbizhatosag` és `igazolas` mezőiben nem számíthat két forrásnak.
- A projekt gerince Strong-alapú (gerinc-metszet, `gerinc_elem`). A Theographic Strong-szám nélkül, KJV-szövegre kulcsolva **gyengébb illeszkedésű**, mint a meglévő, CC BY 4.0 licencű TIPNR. Valódi többlete: (1) koordináta és geo-gazetteer; (2) eseménytábla és kronológia (Jones-féle, egyetlen, vitatható kronológiai iskola: értelmezés, nem adat); (3) családi kapcsolatok gráfja.
- A **CC BY-SA 4.0 share-alike**. A `datasetek.tsv` már tart CC BY-SA forrást (SDBH/SDGNT), de a Theographic-ből levezetett tábla továbbadása SA-kötelezettséget hordoz. Ez a `Rendszerfejlesztesi_playbook.md` 2. pontja szerinti licencdöntés.
- A **névegyeztetés előtag-alapú** (Melchizedek → Melchi, Melchiah). A KJV-alak (Melchisedec) a kanonikus név. Gépi kinyerésnél a Theographic `id`-re kell kulcsolni, nem névre.
- **Javasolt provenienciasor:**
  `scope=range:1Móz 14:18 | forras=bible-mcp:entities_in_passage (Theographic Bible Metadata, CC BY-SA 4.0; versjelölés TIPNR-alapú) | entitas_id=recV4oVk0yumm0aol | n=3 | ts=…`

### Gaps
- A Theographic commitja vagy verziója, amelyet a bible-mcp betöltött, nem derült ki.
- A teljes TIPNR ↔ Theographic halmaz-összevetést nem végeztem el: bulk letöltés nélkül nem mérhető, és a feladat csak olvasást engedett.
- A Theographic forrásjegyzéke az OpenBible geocoding és az Easton licencét nem adja meg. Az OpenBible geo licencét külön nem ellenőriztem (valószínűleg az oldal általános CC BY-a, de ez nem igazolt).

---

## 4. Közös kérdés: illeszkedés a három szabályhoz, bulk elérhetőség, licencek

### Takeaway
Mindhárom réteg csak **jelöltforrásként** illeszthető, a `jeloltek.tsv`-n át, döntéssel. Élő MCP-hívásként a reprodukálhatóság gyenge: a pillanatkép dátuma ismeretlen, a szavazatok változnak, a céltextus fordítása vegyes. Mindhárom alapadat **bulkban letölthető**: az OpenBible zip (CC BY), a Theographic JSON/CSV (CC BY-SA 4.0), az ANF I szöveg (PD), és maga a teljes `bible.db` (~400 MB, de a levezetett rész CC BY-NC 4.0). A projekt szabályaihoz a **verziózott dataset-import** illik, nem az élő lekérdezés.

### Cited Findings
- **[FORRÁS]** A bible-mcp teljes korpusza egy SQLite-fájl (`db/bible.db`, kb. 400 MB, FTS5), a GitHub Release-ből letölthető, vagy újraépíthető a `data/sources/`-ból. Hostolt végpont: `https://bible-mcp-server.fly.dev/mcp`. — [bible-mcp README](https://github.com/nirajagarwal/bible-mcp)
- **[FORRÁS]** Release-ek: v0.14.1 (latest, szept. 28; „Concept-graph confidence floor changed to weight<7”), v0.13.0 (szept. 28), v0.12.0 (szept. 2), v0.11.0 (aug. 6), v0.10.0 (aug. 4), v0.9.0 (aug. 3, ~230 MB). A jegyzetek az OpenBible-letöltés dátumát és a Theographic-commitot nem adják meg. — [bible-mcp releases](https://github.com/nirajagarwal/bible-mcp/releases)
- **[FORRÁS]** Az OpenBible zip közvetlenül letölthető (`a.openbible.info/data/cross-references.zip`, 2 MB, CC BY 4.0). — [OpenBible.info](https://www.openbible.info/labs/cross-references/)
- **[FORRÁS]** A Theographic JSON/CSV/GeoJSON a GitHubon érhető el, CC BY-SA 4.0. — [Theographic GitHub](https://github.com/robertrouse/theographic-bible-metadata)
- **[FORRÁS, repó]** SEMA 1.5: a proveniencia kötelező kulcsai `scope`, `forras`, `ts`. A `scope` zárt értékkészlete: `OT-full | NT-full | OT+NT-full | LXX-39 | range:<…> | manual`. SEMA 2.4: a `jeloltek.tsv` kötelező mezői `id, igehely, forras_kereses, dontes (beépítve|elutasítva|nyitva), indoklas, datum`.

### Inferences
- **1. szabály (proveniencia).** Az élő MCP-hívás provenienciasorához a SEMA kötelező kulcsain túl kell még: a szerver verziója (`corpus_info` nem adja meg; a README v0.14), az alréteg forrása és licence, a `limit`, és ahol releváns, a szavazat-pillanatkép (ismeretlen). A `scope` zárt értékkészletébe az MCP-hívás `range:<igehely>`-ként fér be. A teljes korpuszra futó „OT+NT-full” állítás MCP-ből nem tehető, mert a hívás versszintű.
- **2. szabály (nincs közvetlen út).** Mindhárom réteg kimenete jelölt. A kereszthivatkozás és a patrisztikus találat `forras_kereses` értéke legyen pl. `OpenBible Zsolt 110:4 v27` vagy `bible-mcp get_citations Ézs 53:7`, `dontes=nyitva`, majd tételes minősítés. Az entitás-találat csak a `TIPNR`-rel együtt, Strong-számon át kapcsolódhat `gerinc_elem`-hez.
- **3. szabály (nincs asszociatív kitöltés).** Ez a legnagyobb kockázat az OpenBible-nél: alacsony votes, egyszavas egyezések (Gal 6:10, Ruth 3:10), negatív votes. A patrisztikus rétegnél fordított a kockázat: ott a hamis negatív a veszély („nincs recepció”).
- **Ajánlás (javaslat, a döntés a felhasználóé).**
  (a) **Kereszthivatkozás:** nincs új adat. A meglévő `TSK_kereszthivatkozasok.tsv`-t érdemes a hivatalos zipből, dátummal és hash-sel újra-importálni, és a `TSK` / `openbible_crossrefs` kettős katalógus-sort feloldani. Az MCP-t legfeljebb a friss votes ellenőrzésére érdemes használni.
  (b) **Patrisztika:** a forrásszöveg (PD) importja és saját, determinisztikus idézetkeresés jobb, mint a CC BY-NC levezetett index átvétele. Addig az MCP `get_citations` és `search` kétlépcsős, naplózott jelöltmenet a Drash-recepcióhoz, nem a 7. lépéshez.
  (c) **Entitás:** a TIPNR marad elsődleges. A Theographic-ből csak geo, esemény és rokonsági kiegészítés jöhet szóba, CC BY-SA licencdöntés után.
- Az élő hívás reprodukálhatósága gyenge (a votes változik, a szerver verziója a hívásból nem olvasható ki). Ez a projekt „a kereszthivatkozás adat” elvével ütközik. A verziózott, repóban tartott dataset a konzisztens megoldás.

### Gaps
- A `bible.db` release-asset tényleges tartalmát és méretét nem töltöttem le és nem ellenőriztem (csak olvasás és letöltési engedély-szabály).
- Nem derült ki, hogy a hostolt szerver (`fly.dev`) pontosan melyik release-t futtatja. A `corpus_info` 139 675 mechanikus concept-élt közöl, ez a v0.14.1 „weight<7” küszöb-változásával összefér, de nem igazolt.
- A mcpservers.org listázó oldala 403-at adott; a v0.10–v0.12 közötti leírás-eltéréseket csak keresési kivonatból láttam.
