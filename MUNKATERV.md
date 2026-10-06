# PaRDeS munkaterv — adatvagyon, eszközök, olvasói nézet

Oct 3, 2026 · @basesoft

## 1. Alapelvek és forrás

Ez a munkaterv az `ADATVAGYON_TERV.md` 21. (hat lépcső) és 22. (SEMA-illesztés) szakaszát bontja feladatokra a repó szabályai szerint: egy session = egy feladat, `F<nn>_<NEV>_BRIEF.md`, kis minta a teljes futás előtt, `fuggetlen-ellenor`, draft PR, `/befogad`. A kilenc tervezett feladat **számot a `/befogad`-tól kap**; amelyik még nem kapott, a kódjával szerepel (SQLITE\_EPIT, MCP\_BUROK, SZPA\_AUDIT), mert az eredetileg javasolt #47–#55 számokat a `FELADATOK.md` időközben más feladatoknak osztotta ki (#47 ALLAPOT\_ELLENTMONDASOK, #48 KJV\_REGI\_KIVEZETES, #49 FOLYTATAS, #50 CI\_JAVITO\_KOR, #51 KONZISZTENCIA, #52 TERV\_SZINKRON; DT-F52a, 2026-10-04). Azóta négy kapott számot: BDB\_ADATBLOKK = #56, STRONG\_NORMALIZAL = #62, JELOLTEK\_RETRO = #63, KAROLI\_ELLENORZES = #65; az OLVASOI\_KONKORDANCIA a #25a lesz (DT-M1); a TERV\_BEFOGAD külön brief nélkül lezárult (DT-M8, #52 2. futás). A `#nn` alak ebben a dokumentumban mindig FELADATOK-szám; a dátumokat nem a terv adja, hanem a felhasználó az ütemezéskor (ways-of-working).

Három elv, amitől a terv nem tér el:

1. **Egyik feladat sem ír az `adat/`-ba a briefen kívül**; a `pardes.db` és minden nézet generált. Író eszköz csak a `jeloltek.tsv`-be (SEMA 3. szabály 2.).
2. **Az olvasói konkordancia (motívum nélkül) nem vár a motívum-rétegre** — ez a D46 feloldó feltétele, és eltért a FELADATOK addigi sorrendjétől; a DT-M1 2026-10-06-án eldöntötte: a #25 kettéválik (l. 2. szakasz).
3. **A publikálás licenc-kérdés, de nem akadály**: a STEPBible-származék CC BY 4.0 alatt, attribúcióval terjeszthető (DT-F33f), a hosting-út nyitott; a kiadás két módban megy, a `licencek.tsv` `kereskedelmi` oszlopa szerint szűrve (DT-F33j, N-F33b); a saját rétegek (párosítás, fordítás, döntés) a projekté, licencük külön DT-tétel, jogászi megerősítéssel.

**Viszony a meglévő briefekhez.** A munkaterv nem vált fel egyetlen meglévő briefet sem. F22 (⛔ megállt, 1–5Móz és Józs kész, a Józs PR mergelve) változatlanul fut; F43 (✅, PR #167), F44 (✅, PR #205), F42 (✅, PR #176) és F46 (✅) kész — a 0. lépcső és a 2. hullám bemenetei; F07 halasztott (D46); F38 marad, a #56 BDB\_ADATBLOKK adatblokkjával és javító menettel egészíti ki (a BDB-lánc első lépése a #57 BDB\_STRONG\_POTLAS ✅: #57 → #56 → #38 6. adag); F23 és F25 `olvas:` listájában az `ADATVAGYON_TERV.md` már bent van (DT-M8 (a)), a #11 briefjébe a befogadáskor kerül (DT-M8 (d)); SZOTAR, RENDER, LEXV2 érintetlen. Egyetlen módosul: **F25**, amely a DT-M1 (🟢 2026-10-06) szerint kettéválik — #25a olvasói konkordancia motívum nélkül (= OLVASOI\_KONKORDANCIA; függ SQLITE\_EPIT) és #25b motívumos nézet (függ #11, #12, #23); a csonk tényleges kettéválasztása és a #25a befogadása külön `/befogad` menet, még nem történt meg. A kilenc tervezett feladat ott kap briefet (és számot), ahol ma nincs.

## 2. Döntési előfeltételek (DT-tételek)

Hat döntés (DT-M1–M6), amit a feladatok előtt vagy mellett a felhasználónak kell meghoznia, és két későbbi (DT-M7, DT-M8). Mindegyik egy sor a `DONTESEK.md`-ben; a „javasolt irány” oszlop a terv javaslata; ahol a felhasználó döntött, az oszlop a döntést írja (2026-10-06-i állapot).

| # | döntés | javasolt irány | melyik feladatot oldja fel |
| --- | --- | --- | --- |
| DT-M1 | Az olvasói konkordancia (motívum nélkül) a #25 előtt, a #11/#23-tól függetlenül kiadható | 🟢 2026-10-06: igen — a D46 feloldó feltétele; a #25 kettéválik: #25a konkordancia (függ SQLITE\_EPIT; a #44 ✅), #25b motívumos nézet (függ #11, #12, #23); a #25a további feltételei (DT-M4, DT-M6, hosting ⛔, nem kereskedelmi mód, N-F33b) a briefjébe tartoznak | OLVASOI\_KONKORDANCIA |
| DT-M2 | SEMA 1.7 `AZONOSITAS_MODJA` szövege és a DONTESEK 8. szakasza elavult: a #22 szó-szintű, gépi Károli–Strong párosítást ad | 🟢 2026-10-05, a javaslattól eltérve: új érték `szó-szintű-gépi` (a modell-kimenet legyen jelölve); a `parok_<könyv>` `magas` linkjéből tölthető, a `tartalom-alapú` sorok frissíthetők; a `szó-szintű-tagged` esetleges kiadói taggelésnek marad | KAROLI\_ELLENORZES (#65) |
| DT-M3 | SEMA 2.9 `auditok.lepes` új értéke ad hoc kutatói lekérdezésre | 🟢 2026-10-05, a javaslattól eltérve: a `lepes` a kutatási lépés kódját kapja (bármely csatornán), a lépésen kívüli lekérdezés új értéke `adhoc`; a csatorna (`csatorna=cli`, később esetleg `mcp`) a proveniencia-sorba kerül; a 8. szabály dataset-lefedettsége ezeket a sorokat is számolja | #61 LEKERDEZ\_NAPLO (MCP nélkül is); MCP\_BUROK |
| DT-M4 | SEMA 2.13 szerepmátrix bővítése: 13. szerep Károli-megfelelők (+ SZPA alternatíva), 14. szerep rejtett/hamis párhuzam | 🟡 nyitott: felvétel `javaslat` állapottal, amíg a #22 nem teljes | OLVASOI\_KONKORDANCIA szó-lap |
| DT-M5 | F44 5.(d): külső `bible-mcp` connector | 🟡 nyitott: elvetés egyelőre, saját MCP után újra (DT32: ha használjuk, a kimenete adatfájlba, briefbe, tanulmányba nem kerül; a bekötés ennek a DT-nek a kérdése) | MCP\_BUROK |
| DT-M6 | A saját kimenet (párosítás, fordítás, döntés) licence és a két kimeneti mód: a STEPBible-származék DT-F33f szerint CC BY 4.0 alatt, attribúcióval terjeszthető (nem kizárandó); a szűrést a `licencek.tsv` `kereskedelmi` oszlopa adja (DT-F33j, N-F33b) | 🟡 nyitott: az első kiadás nem kereskedelmi, minden blokk dataset-kulccsal, forrás- és licenc-jelöléssel; az OLVASOI\_KONKORDANCIA a `kereskedelmi` oszlop szerint szűr; a saját réteg licence (javaslat: CC BY 4.0 az adatra) külön DT-tétel; jogász a kereskedelmi döntéskor | OLVASOI\_KONKORDANCIA publikálás |
| DT-M7 | Maradjon-e az MCP\_BUROK a 3. hullámban (a chatbeli újravizsgálat szerint a tényleges többlet az automatikus naplózás — MCP nélkül is a `lekerdez.py`-ban —, a strukturált hívás és a claude.ai-ból való hozzáférés, utóbbi csak hostolva) | 🟢 2026-10-05: kikerül a 3. hullámból, **feltételes**: akkor jön, ha a chatből való adathozzáférés ténylegesen hiányzik, vagy repó nélkül dolgozó munkatárs lesz; előbb a `lekerdez.py` automatikus naplózása (#61) | MCP\_BUROK |
| DT-M8 | A TERV\_BEFOGAD maradéka külön brief nélkül | 🟢 2026-10-05: nincs külön brief; (a) a 3. szakasz pipája, (b) az `ATALAKITASI_TERV.md.md` 4.7 jelölése és (c) a `CLAUDE.md` KJV-sora a #52 2. futásában (elvégezve, 2026-10-06); a (d) a #11 briefjének `olvas:` sorába kerül a befogadáskor; a #48 a `CLAUDE.md` KJV-sorát a régi fájlok kivezetésekor a végleges állapotra igazítja | TERV\_BEFOGAD |

A DT-M1 volt a legsúlyosabb: átrendezi a FELADATOK sorrendjét (eldöntve, 2026-10-06). Eldöntve (🟢): DT-M1, M2, M3, M7, M8; nyitott: DT-M4, M5, M6.

## 3. 0. lépcső — a felhasználó kézi lépései

Ezek nélkül a `/kovetkezo` nem indítja a függő feladatokat, mert a források a cloud proxyról nem elérhetők, vagy a döntés csak a felhasználóé.

- [x] `lxx_bridge` tábla + licencsor → `adat/kulso/lxx_bridge.tsv`, `adat/kulso/LICENC.md` (#43 0. lépés; bent, F43.0)
- [x] a `k-mktr/karoli_bible_hu` kártya licenc-mezője és README-je szó szerint → `adat/kulso/karoli_bible_hu_LICENC.txt` (#44; bent, F44.0 — a Károli-rész a DT-F33e-vel tárgytalan)
- [x] az openbible.info licencnyilatkozata szó szerint → `adat/kulso/openbible_crossrefs_LICENC.txt` (#44; bent, F44.1)
- [x] `ADATVAGYON_TERV.md` és `MUNKATERV.md` a repó gyökerébe, commit (`ab73f7b`, 2026-10-04)
- [x] a #23/#25 brief `olvas:` listájába felvéve (DT-M8 (a): mindkét fejlécben bent; a #11 briefjébe a befogadáskor, DT-M8 (d))
- [ ] a 2. szakasz DT-tételei eldöntve: DT-M1, M2, M3, M7, M8 🟢 (2026-10-05/06); **nyitott: DT-M4, M5, M6**
- [ ] a #38 6. adagja: a DT-F38i 🟢 feloldva; az M0 5. pont (BDB-gyökcsoport-felmérés) a 6. adag menetének elején fut (FELADATOK #38 következő lépés), ellenőrizendő
- [ ] tárhely-döntés előkészítése: böngészős SQLite, cPanel (PHP vagy Python a lekérdező) vagy Netlify — a licenc nem kényszerít (DT-F33f), a mód és az offline-igény dönt (DT-F33j); az OLVASOI\_KONKORDANCIA előtt ⛔

## 4. Feladatlista (javasolt FELADATOK-sorok)

Minden sor egy brief. A „kis minta" oszlop az elfogadási próba, amit a teljes futás előtt a felhasználó jóváhagy (playbook 3.). Modell: Sonnet, ahol nincs más jelölve; az `ellenor` mindig Haiku vagy Sonnet, a brieftől független menetben.

| # | név | cél | bemenet | kimenet | kis minta → elfogadás | függ | menet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | TERV\_BEFOGAD (**lezárva**, külön brief nélkül, DT-M8: a három dokumentum a repóban `ab73f7b`; a #23/#25 `olvas:` bent; az ATALAKITASI\_TERV 4.7 jelölve és a `CLAUDE.md` KJV-sora javítva a #52 2. futásában; a (d) a #11 briefjébe kerül) | az `ADATVAGYON_TERV.md` és a `MUNKATERV.md` repóba vétele; a #23, #25 brief `olvas:` sora; ATALAKITASI\_TERV 4.7 elavultként jelölve; CLAUDE.md KJV-sora javítva | a két Markdown | commit, három fájl módosítása | — (szerkesztés) | 0. lépcső | ½ |
| #65 | KAROLI\_ELLENORZES | 1.1 ellenőrzés: a Genezis-igehelyes tematikus táblák Károli-idézet + Strong párjai a `parok_<könyv>` ellen, csak `magas` linkre; 1.2 variancia-térkép; a Károli-triplet frissítése (`tartalom-alapú` → `szó-szintű-gépi`, DT-M2) a `jeloltek`/`elofordulasok` sorain | `tematikus_lezart/*.md`, `adat/karoli_strong/parok_*.tsv`, `jeloltek.tsv` | `naplok/KAROLI_ELLENORZES_elteresek.tsv`; `adat/karoli_variancia.tsv` (Strong → szóalakok db; szóalak → Strongok); triplet-frissítő PR | ANTROP-001 egy motívumon: eltéréslista + 3 triplet-sor átnézve | #62, #63 (brief); a #22 bemenet, nem előfeltétel: a kész könyveken fut (1–5Móz és Józs; `nem_fugg: [22]`), DT-M2 🟢 | 1 |
| #62 | STRONG\_NORMALIZAL | N37: egyetlen `strong_normalizal()` függvény (`H922` → `H0922`, `G746`, `+` láncok), `lekerdez.py`-ba és `betolt.py`-ba kötve; N21 nullázatlan értékek javítása | `eszkozok/*.py`, `adat/*.tsv` | függvény + teszt; javított TSV-sorok | 20 ismert eltérő alak | — | ½ |
| — | SQLITE\_EPIT | `eszkozok/sqlite_epit.py`: SEMA-típusok, `IGEHELY` normalizálás a `Konyv_normalizalo_tabla`-n át, KK-alapú vers-kulcs, `szamozas` (BSB-értékkészlet + N46), `licenc_allapot` és `kereskedelmi` minden táblán, `strong_parok` és frázis-pozíció előszámolva, FTS a `motivumok/` fölött; a SEMA 3. szakasz nyolc integritási szabálya tesztként, sértésnél megáll; `pardes.db` `.gitignore`-ban | `adat/*.tsv`, `konkordancia/*.tsv`, `licencek.tsv` | `pardes.db` (helyben), `naplok/SQLITE_EPIT_integritas.md` | 8 lexikonoldalas motívum + 1Mózes; a 26 pontból a 1–6, 13–15 lekérdezése visszaadja a tanulmányok ismert tényeit | STRONG\_NORMALIZAL (#62) | 1–2 |
| — | MCP\_BUROK (**feltételes**, DT-M7: csak ha a chatből való adathozzáférés hiányzik, vagy repó nélkül dolgozó munkatárs lesz; előbb a #61) | FastMCP burok a `lekerdez.py`-ra, ≤ 8 eszköz: `lekerdez(parancs, …)`, `vers_lap`, `szo_lap`, `lelet_lap`, `ellenoriz`, `karoli_szoalakok`; minden hívás proveniencia-sorral (`csatorna=mcp`) és `auditok.tsv`-sorral (`lepes` a kutatási lépés kódja vagy `adhoc`, DT-M3); csak olvasó; `.mcp.json` | SQLITE\_EPIT, `lekerdez.py` | `eszkozok/mcp_szerver.py`, `.mcp.json`, `naplok/MCP_BUROK_eszkozteszt.md` | a `lexikai-scan` subagent egy ANTROP-001 futása eszközökön át ugyanazt adja, mint CLI-n | SQLITE\_EPIT, #61, DT-M5 | 1 |
| #56 | BDB\_ADATBLOKK | a 12.1 szócikk-adatlekérés build-lépésként: Python előre számolja a Károli-szóalakok, példaversek, LXX-híd, rokonok, meglévő szócikk blokkját, és az adagfájlban a BDB-szócikk elé fűzi; `terminologia.tsv` olvasása minden adagban; a fordító prompt egy sora (`[NINCS KÁROLI-ALAK]`) | közvetlen TSV (a #56 briefje szerint nem függ az SQLITE\_EPIT-től), `BDB_FORDITAS_BRIEF.md` | adagfájl-generátor; a #38 javító menetének briefje | 10 szócikk H2617 körül: a blokk minden száma és idézete eszköz-kimenetből | — (F56 `fugg: []`); a #38 nem előfeltétel, hanem ráépül: a 6. adag a #56 után fut (F38 `fugg: [34, 56]`, F56 `nem_fugg: [38]`, DT-F38i 🟢) | 1 |
| #63 | JELOLTEK\_RETRO | a 8 retroaktív (F3/N14) motívum `jeloltek.tsv`-sorainak feltöltése a naplókból; a származtatott „még nem vizsgált" lista (`auditok` scan − `jeloltek`) generátora; a 12-es lelet-lap adatának első teljes futása | `tematikus_lezart/naplok/*.md`, `auditok.tsv`, `jeloltek.tsv` | `jeloltek.tsv` bővítés (PR), `eszkozok/nem_vizsgalt.py`, `naplok/JELOLTEK_RETRO_lelet_ANTROP.md` | ANTROP-001: minden ★ sor mellett `dontes` + `indoklas`, 0 „még nem vizsgált" | #62\* (szoftfüggés; az adat megvan) | 1–2 |
| — | OLVASOI\_KONKORDANCIA (a #25 kettéválasztása után #25a, DT-M1 🟢) | első publikus kiadás motívum nélkül: `general.py --cel verslap / szolap`; szó-lap a szerepmátrix (18.5) szerint, `allapot` vezérli a blokkokat; vers-lap KK-kulccsal, Károli 1908 nyílt szöveg; lekérdező a hosting-döntés szerint (böngészős SQLite, cPanel PHP vagy Netlify Function) a `kereskedelmi` oszlop szerinti mód-szűrővel (DT-F33j); tipográfia/színséma kapcsoló | SQLITE\_EPIT, `Karoli_1908` (közkincs, DT-F33e), 1–6, 13–16, 18–20. pont | `kimenet/olvasoi/` generált oldalak, `api/kereses.*`, `naplok/OLVASOI_KONKORDANCIA_publikalas.md` | 20 vers + 20 Strong lapja; minden adat a `pardes.db`-ből; minden blokk alatt forrás és licenc, nincs blokk dataset-kulcs nélkül (nem kereskedelmi mód, N-F33b) | SQLITE\_EPIT (a #44 ✅, DT-M1 🟢), DT-M4, DT-M6; hosting ⛔ | 2–3 |
| — | SZPA\_AUDIT | a profil C üzemmódja: 1.2 tiltólista és 1.1 kötött párok gépi ellenőrzése a tanulmányok prózáján és a BDB-fordításon; kimenet a C-táblázat | `SZPA_FORDITOI_PROFIL_prompt.md`, tanulmányok, `forditasok.tsv` | `naplok/SZPA_AUDIT_szpa_audit.tsv` | 2 tanulmány + 50 szócikk | — | ½ |

Az OLVASOI\_KONKORDANCIA után a meglévő lánc fut tovább: #23 (motívum-séma, mélységi szintek) → #9/#10 (lexikonoldal) → #11 (egy forrásból renderelés) → #25b (motívum-lap, lelet-lap ★, a 7–12. és 21–26. pont). Az MCP\_BUROK (feltételes, DT-M7) és a JELOLTEK\_RETRO kimenete ezekbe épül, nem külön rendszer.

## 4a. A teljes projekt feladattérképe

Minden nyitott FELADATOK-sor (státuszok és függések frissítve 2026-10-06, #52 TERV\_SZINKRON 2. futás; a FELADATOK fejléce változatlanul v1.3) és a kilenc tervezett, fázisonként. A „terv" oszlop a viszony a munkatervhez: **marad** (nem érinti), **módosul** (a terv egy ponton átírja), **bemenet** (a terv valamelyik feladata rá épül), **új**, **tervezett** (a kilenc egyike, számot kapott). A „?" olyan állítás, amit a repó ellen még nem hitelesítettünk — a kész feladatok briefjeit, a naplókat és az eszközök kódját ez a terv nem látta (a TERV\_BEFOGAD külön brief nélkül zárult, DT-M8).

**1. fázis — adatréteg**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #22 | Károli–Strong párosítás könyvenként | ⛔ megállt (1–5Móz és Józs kész, a Józs PR #165 mergelve; a következő könyv a Bírák: előbb versbeosztás-detektor és kézi jóváhagyás) | #21 ✅ | **bemenet** | KAROLI\_ELLENORZES (#65) könyvenként újrafut rá; SQLITE\_EPIT, OLVASOI\_KONKORDANCIA forrása; 13. szerep (DT-M4) |
| #38 | BDB teljes magyar fordítása | ▶ fut (5 adag kész; a 6. adag a #56 adatblokkjával, DT-F38i 🟢) | #34 ✅, #56 ✅ | **módosul** | a 6. adagtól a #56 BDB\_ADATBLOKK adatblokkjával; javító menet a teljes #22 után |
| #43 | LXX-döntések ellenőrzése lxx\_bridge-dzsel | ✅ kész (2026-10-04, PR #167; DT-F43: a bridge nem független forrás, csak tájékoztató) | #8 ✅ | **bemenet** | a 26-os pont, a szó-lap LXX-blokkja |
| #44 | Licenc-utókövetés: Károli 1908, openbible.info | ✅ kész (2026-10-05, PR #205; a Károli-rész tárgytalan, DT-F33e; a `karoli_bible_hu` elvetve, DT31; nyitott: az openbible-import külön feladat, DT34, és a DT-M5) | #33 ✅, #42 ✅ | **bemenet** | az OLVASOI\_KONKORDANCIA publikálási előfeltétele teljesült |
| #46 | BDB rosszul feloldott könyvnevei | ✅ kész (2026-10-03) | #34 ✅ | marad | a #56 példaversei innen javítva |
| #7 | Thayer teljes magyar fordítása | ⬜ brief kell (halasztva, D46) | #3, #5, #14 ✅ | marad | D46: az OLVASOI\_KONKORDANCIA (#25a) oldja fel; a #56 mintájára adatblokkal |
| #23 | Egyforrású motívumdokumentum, mélységi szintek | ⬜ M0 után; M1 a #12a (#64) próza-próba után (DT-F32a) | #32 ✅, #37\* | marad | a motívum-séma itt születik; a 7–12, 21–26. pont erre vár; #25b feltétele |
| #27 | Thayer: Opus/Gemini összevetés | ⬜ (halasztva, D46) | — | marad | nem érinti |
| #30 | Döntés- és N-számok kiosztása merge-kor | ✅ kész (2026-10-05, PR #206; `szamkiosztas.py` + Action, CI E26) | #8, #16, #17 ✅ | marad | az ágon helyőrző (`DT-F<nn>`), a végleges számot a main-en az Action adja |
| #40 | Hivatkozás-ellenőrzés CI-szabály | ⬜ | #2 ✅, #37\* | marad | a MUNKATERV által módosított briefek hivatkozásai |
| #48 | KJV\_REGI\_KIVEZETES: a régi studybible.info KJV/ASV fájlok kivezetése, minden az eBible KJV-forrásra | ⬜ | #19 ✅, #21 ✅, #22 | **bemenet** | az SQLITE\_EPIT KJV-forrása a `KJV_Strongs_teljes`; az ASV kiesik (N29 lezárva, D7); a `CLAUDE.md` KJV-sorát a végleges állapotra igazítja (DT-M8) |
| #54 | LXX\_OS\_LEFEDETTSEG: az 503 lefedetlen Károli-vers (valódi görög hiány vagy versszámozási rés) | ⬜ (⛔ az M0 után) | #42 ✅, #62\* | marad | a 26-os pont (LXX-híd) hiánykezelése: a lefedetlen vers explicit üres eredmény; a tervet nem érinti |
| #55 | ZSOLTAR\_UJRAELLENORZES: az eltolt zsoltár-kivonatra épülő állítások újraellenőrzése | ⬜ (⛔ az M0 után) | #42 ✅, #54\*, #63\*, #65\* | marad | szoftfüggés a #54, #63, #65 fájljaira; a tervet nem érinti |
| #56 | BDB\_ADATBLOKK (közvetlen TSV-változat) | ✅ kész (PR #218, 2026-10-06; DT48 alkalmazva) | — | **tervezett** | a #38 6. adagja ráépül; a javítótábla az 1–5. adagra is visszamenőleg |
| #63 | JELOLTEK\_RETRO | ⬜ (⛔ az M0 után) | #62\* | **tervezett** | az első teljes lelet-lap-adat; a #65 és a #55 szoftfüggése |
| #64 | TEREMT002\_PROZA\_PROBA (#12a) | ⬜ (indítás a #23 M0 jóváhagyása után) | — | marad | a #23 M1 bemenete (DT-F32a); a #12 első fele |
| #65 | KAROLI\_ELLENORZES | ⬜ (⛔ az M0 után) | #62, #63\* | **tervezett** | a #22 kész könyveire fut (`nem_fugg: [22]`); DT-M2 🟢 |
| #66 | BDB\_ARAM\_POTLAS: az elvetett arámi szócikkek külön táblába (DT40) | ⬜ (⛔ az M1 jelölttábla után) | #57 ✅ | marad | a #38, #56, #60 nem függ tőle |

**2. fázis — render**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #9 | Szótári adatréteg S2 | ⬜ | #5, #6 ✅, #7\*, #23, #38\* | marad | lexikonoldal = szó-lap elv; a 13–14. szerep (DT-M4) ide |
| #10 | 8 lexikonoldal lezárása | ⬜ brief kell | #8 ✅, #9, #11 | marad | a mérce: a sablon Minőségi kapuja (L1, L3–L6) + minden rés kitöltött vagy explicit hiány-/`adat`-jelölésű (DT2 🟢, 2026-10-06); N18, N19 nem blokkol; a #8 négy nyitott sora előfeltétel |
| #11 | Migráció: egy forrásból renderelés | ⬜ brief kell (a #12a után) | #9, #23 | **módosul** (kicsi) | `olvas:` listába az ADATVAGYON\_TERV (DT-M8 (d), a befogadáskor); vers-lap/szó-lap mint `general.py --cel` ide ? |
| #12 | TEREMT-002 3. lépés | ⬜ brief kell | #11 | marad | — |
| #13 | 1Móz 17-től tanulmányok, 6 betöltetlen motívum | ⬜ brief kell | #10 | marad | a #63 után tisztábban futhat ? |
| #25 | Olvasói felület: statikus HTML mélységgel | ⬜ brief kell (a kettéválasztás külön `/befogad`) | #11, #12, #23 | **módosul** | DT-M1 🟢 (2026-10-06): kettéválik — **#25a** = OLVASOI\_KONKORDANCIA (konkordancia motívum nélkül, függ SQLITE\_EPIT; a #44 ✅), **#25b** motívumos nézet (függ #11, #12, #23) |
| #36 | Éles lexikon/ újragenerálása | ⬜ | #7\*, #9\*, #28 ✅, #34 ✅, #35 ✅, #37\*, #38\* | marad | az OLVASOI\_KONKORDANCIA (#25a) generátora ugyanabban a CI-futásban (N33); a #42 ✅ után renderel újra (elavult törzscikkek) |
| #59 | SZOSZEDET: jóváhagyott, szerkesztői magyarázó tábla az olvasói nézethez | ⬜ (⛔ a tervezet után, tételenkénti jóváhagyás) | #58 ✅ | **bemenet** | az OLVASOI\_KONKORDANCIA (#25a) szó-lapjának szakszavai; minden sor „szerkesztői szöveg" jelölésű |

**Folyamat és eszközök**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #32 | Kontextus-őrzés | ✅ kész (2026-10-04; négy szabály a MUNKAMENET-ben, `munka` mező a fejlécben, DT-F32a/b/c) | — | marad | a guide 6. szakasza alkalmazza |
| #37 | Tanulmány-ellenőrzés: CI + független ellenőr | ⬜ | #30 ✅, #32 ✅, #45\* | **bemenet** | a #65 eltéréslistája és az MCP `ellenoriz` eszköz (ha az MCP\_BUROK elindul, DT-M7); a session 5. lépése |
| #42 | Forrásfájlok kivezetése, licencállapot egy forrása | ✅ kész (2026-10-05, PR #176; a licenc-címke egyetlen forrása az `adat/licencek.tsv` `cimke` oszlopa, DT-F42g) | #33, #35 ✅ | **bemenet** | a `licenc_allapot` szűrő forrása; SQLITE\_EPIT, OLVASOI\_KONKORDANCIA feltétele teljesült |
| #45 | Modell-ellenőrzés brief elején | ⬜ | — | marad | minden új brief fejlécébe |
| #50 | CI\_JAVITO\_KOR: push után a CI olvasása, a saját PR hibáinak javítása | ⬜ | — | marad | minden brief záró lépése |
| #51 | KONZISZTENCIA: döntések átvezetésének gépi és ügynöki ellenőrzése | ✅ kész (2026-10-05, PR #192; E25 CI-szabály, `/konzisztencia`, napi helyi ütemezés) | #37\* | **bemenet** | a TERV\_SZINKRON (#52) kiváltó jelzése; a `dontes_hatas.tsv`-ben a három tervdokumentumra ma nincs sor |
| #52 | TERV\_SZINKRON: a tervdokumentumok átvezetése a repó állapotára | ▶ fut (2. futás 2026-10-06) | — | **új** | ez a dokumentum, az ADATVAGYON\_TERV és a VIBE\_GUIDE karbantartója; ismétlődő |
| #60 | OLVASOI\_PILOT: a konkordancia-nézet mérhető próbája két szakaszon (1Móz 1:1–2:3, Zsolt 22) | ⬜ (⛔ az M3 felhasználói átnézésnél) | — | **bemenet** | a DT-M1 alapja volt; `eszkozok/olvaso_pilot/`; minden blokk jellegjelöléssel |
| #61 | LEKERDEZ\_NAPLO: a `lekerdez.py` maga naplóz, `lepes=adhoc` | ⬜ (⛔ az M0 után) | #54\*, #62\* | **bemenet** | a DT-M3 alkalmazása; MCP nélkül is automatikus naplózás (DT-M7) |
| #62 | STRONG\_NORMALIZAL: egyetlen `strong_normalizal()` | ⬜ (⛔ az M0 után) | — | **tervezett** | N37, N21; az SQLITE\_EPIT előfeltétele |

**Tervezett (a kilenc új; szám a befogadásnál)** — részletek a 4. szakaszban; itt a fázis-besorolás:

| # | fázis | mire ül |
| --- | --- | --- |
| TERV\_BEFOGAD (lezárva, DT-M8) | folyamat | dokumentum |
| #65 KAROLI\_ELLENORZES | 1. adatréteg | #62, #63; a #22 bemenet (kész könyvek), DT-M2 🟢 |
| #62 STRONG\_NORMALIZAL | eszközök | N37, N21 |
| SQLITE\_EPIT | eszközök | #62, SEMA 3. |
| MCP\_BUROK (feltételes, DT-M7) | eszközök | SQLITE\_EPIT, ATALAKITASI\_TERV 11.7, #61 |
| #56 BDB\_ADATBLOKK | 1. adatréteg | közvetlen TSV; a #38 ráépül (a 6. adag a #56 adatblokkjával, DT-F38i; a #56 kész) |
| #63 JELOLTEK\_RETRO | 1. adatréteg | SEMA 2.4, F3/N14, #62\* |
| OLVASOI\_KONKORDANCIA (= #25a) | 2. render | SQLITE\_EPIT, DT-M1 🟢, DT-M4, DT-M6 |
| SZPA\_AUDIT | folyamat | SZPA-profil |

**Kész feladatok, amelyekre a terv épít, de a briefjüket nem látta:** #21 (pilot), #8 (LXX-döntések), #5/#6 (szótár S1), #14, #28, #33, #34, #35, #16/#17, #19 (KJV teljes), #24 (licenc-leltár), #41 (versszámozás) ? — állapotuk a FELADATOK „Kész" szakaszából. A terv írása után kész: #26 (D34–D41), #32 (KONTEXTUS), #49 (FOLYTATAS) (2026-10-04); #43 (PR #167, 10-04); #42 (PR #176), #44 (PR #205), #30 (PR #206), #51 (PR #192), #53 FELADATTERKEP (PR #201, lezárás #217), #57 BDB\_STRONG\_POTLAS (PR #209), #58 MORF\_KULCS (PR #208) (2026-10-05/06); a #46 már 2026-10-03-án kész volt, a terv elavult státusszal vette fel. A BDB-lánc első lépése a #57 ✅ (`BDB_strong_alias.tsv`), utána #56 → #38 6. adag; a #66 külön táblába pótolja az elvetett arámi szócikkeket.

**Összesítve (2026-10-06):** 15 nyitott régi feladat (a #30, #32, #42, #43, #44, #46 kész) — 3 módosul (#38, #25, #11 kicsit), 2 bemenet (#22, #37), 10 marad érintetlenül; a terven kívülről 10 nyitott FELADATOK-sor (#48, #59, #60, #61 bemenet; #50, #54, #55, #64, #66 marad; #52 új); a kilenc tervezett közül 4 kapott számot (#56, #62, #63, #65), 1 lezárult (TERV\_BEFOGAD), 4 számtalan (SQLITE\_EPIT, OLVASOI\_KONKORDANCIA = #25a, MCP\_BUROK feltételes, SZPA\_AUDIT). Egyetlen régi feladat sem szűnik meg.

## 5. Hullámok és megállási pontok

A feladatok négy hullámban futnak; egy hullámon belül párhuzamosíthatók (külön session, külön ág). A ⛔ a felhasználói megállás, ahol a következő hullám nem indul.

| hullám | feladatok | miért együtt | ⛔ a végén |
| --- | --- | --- | --- |
| 1 | 0. lépcső (kész); TERV\_BEFOGAD (lezárva); #62 STRONG\_NORMALIZAL; #63 JELOLTEK\_RETRO; #56 BDB\_ADATBLOKK (kész); SZPA\_AUDIT | egyik sem igényel új adatot; a #63 az első teljes lelet-lap-adat, az SZPA\_AUDIT azonnal mérhető hozam; a #56 közvetlen TSV-változat volt (nem függött az SQLITE\_EPIT-től), PR #218-cal kész | DT-M1–M3 eldöntve (🟢); a #43 és a #44 kész; a #38 6. adagja a #56 adatblokkjával indul (DT-F38i 🟢) |
| 2 | #65 KAROLI\_ELLENORZES; SQLITE\_EPIT | a #65 a #22 kész könyveire fut, és a #62-től, #63-tól függ; az SQLITE\_EPIT a #62-re épül; a két brief független | az SQLITE\_EPIT integritási tesztje 0 sértés; a KAROLI\_ELLENORZES eltéréslistája átnézve, a triplet-frissítés PR-je befogadva |
| 3 | — (az MCP\_BUROK a DT-M7 szerint kikerült a hullámból; feltételes) | a `pardes.db`-n ül; csak akkor jön, ha a chatből való adathozzáférés hiányzik, vagy repó nélkül dolgozó munkatárs lesz; előbb a #61 LEKERDEZ\_NAPLO adja az automatikus naplózást | az MCP\_BUROK eszközteszt egyezik a CLI-vel (ha a hullám elindul) |
| 4 | OLVASOI\_KONKORDANCIA (a #25a) | az első publikus kiadás; csak a hosting-döntés és a DT-M6 után | hosting ⛔; a mód-szűrő és a blokkonkénti forrásjelölés átnézve (DT-F33j, N-F33b); első 40 lap jóváhagyva → publikálás |
| után | #23 → #9/#10 → #11 → #25b | a motívum-réteg a kész konkordanciára ül | a FELADATOK meglévő megállásai (A4/B5) |

A hullámoktól függetlenül, folyamat-feladatként fut: #50 CI\_JAVITO\_KOR és #52 TERV\_SZINKRON (ismétlődő, a briefje 2. pontja szerinti eseményeknél); a #51 KONZISZTENCIA kész (napi helyi ütemezés). A tervet nem érintő önálló feladatok: #54, #55, #64 (a #23 M1 bemenete, DT-F32a), #66; a tervhez bemenetként kapcsolódik a #59 SZOSZEDET, a #60 OLVASOI\_PILOT és a #61 LEKERDEZ\_NAPLO (DT-M3).

Közben folyamatosan: **#22** könyvenként (1–5Móz és Józs kész; ⛔ a felhasználónál a következő könyvig, a Bírákig) és **#38** adagonként — a 2. hullámtól a #65 minden új Károli–Strong könyvre újrafuttatható, a #38 adagjai az 1. hullámtól (a #56 után) a #56 blokkjával mennek.

```
1. hullám  ─▶  2. hullám  ─▶  3. hullám  ─▶  4. hullám  ─▶  #23 → #9/#10 → #11 → #25b
0. lépcső ✓         #65 KAROLI_ELLENORZES   —               OLVASOI_KONKORDANCIA (a #25a)
TERV_BEFOGAD ✓      SQLITE_EPIT             (MCP_BUROK: feltételes, DT-M7)
#62 STRONG_NORMALIZAL
#63 JELOLTEK_RETRO
#56 BDB_ADATBLOKK
SZPA_AUDIT
                         ⛔ 0 sértés                         ⛔ hosting, DT-M6
```

## 6. Kockázatok és mérőszámok

| kockázat | hol üt | kezelés |
| --- | --- | --- |
| versszámozás (N17, N46, N-F41a/d): a vers-lap rossz verset köt össze | SQLITE\_EPIT, OLVASOI\_KONKORDANCIA | KK-alapú kulcs, `szamozas` jelző, interpoláció nélkül; a kis minta 20 verse közül 5 ismert eltolódásos (zsoltárfelirat, Jób 40–41) |
| a Károli–Strong `alacsony` linkjei az ellenőrzésben zajt adnak | KAROLI\_ELLENORZES | csak `magas` link számít egyezésnek; az `alacsony` eltérés külön listán |
| a `jeloltek` retro-feltöltése a naplók szabad szövegéből kézi ítéletet kíván | JELOLTEK\_RETRO | motívumonként ⛔; a `nyitva` státusz megengedett, a `beépítve` csak napló-szöveggel |
| kereskedelmi módban `kereskedelmi=nem` vagy `tisztazatlan` forrás kerül a kimenetbe; nem kereskedelmi módban jelöletlen blokk | OLVASOI\_KONKORDANCIA | `licenc_allapot` és `kereskedelmi` minden táblán, a lekérdező a mód szerint szűr (DT-F33j, N-F33b); teszt: kereskedelmi módban egy ETCBC/MCGED-eredetű mező sem jelenik meg, nem kereskedelmi módban nincs blokk dataset-kulcs nélkül |
| az MCP eszközdefiníciói kontextust fogyasztanak | MCP\_BUROK | ≤ 8 eszköz (ATALAKITASI\_TERV 11.7); mérés az eszközteszt-naplóban |
| a #38 adagjai a BDB\_ADATBLOKK nélkül folytatódnak, és a Károli-oszlop utólag hiányzik | BDB\_ADATBLOKK | a 6. adag csak a BDB\_ADATBLOKK blokkjával indul (DT-F38i); a kész 5 adag a javító menetben kapja meg |
| a CC BY-SA (SDBH/Louw–Nida) blokkok ShareAlike-feltétele | OLVASOI\_KONKORDANCIA | a szó-lap 4/5/9. szerepe csak azonos licencű kiadásban; a licenc-szűrő külön értéke |

**Mérőszámok** (a naplókban rögzítve, nem a chatben):

- KAROLI\_ELLENORZES: eltérések száma / vizsgált sor; triplet-frissített sorok száma
- SQLITE\_EPIT: integritási sértések (cél: 0); `pardes.db` mérete (a hosting-döntés bemenete)
- MCP\_BUROK: eszközhívás vs. CLI egyezés (cél: 100% a mintán); auditsorok száma
- JELOLTEK\_RETRO: `jeloltek`-sorok száma motívumonként; „még nem vizsgált" (cél: 0 a 8 lexikonoldalas motívumon)
- OLVASOI\_KONKORDANCIA: a 26-ból futó pontok száma; blokk dataset-kulcs nélkül (cél: 0); kereskedelmi módban `kereskedelmi=nem` forrásból jövő mező (cél: 0)
- SZPA\_AUDIT: tiltólistás szó / 1000 szó a tanulmányokban és a BDB-fordításban

## 7. Döntésnapló

| dátum | döntés / változás | státusz |
| --- | --- | --- |
| 2026-10-03 | v1: munkaterv az ADATVAGYON\_TERV 21–22. szakaszából — hat DT-előfeltétel, 0. lépcső, kilenc javasolt feladat (#47–#55), négy hullám, kockázatok és mérőszámok | tervezet |
| 2026-10-03 | A sorszámok (#47–#55) javaslatok; véglegesítés a FELADATOK.md-ben a felhasználó döntésével; dátumokat a felhasználó ad | megjegyzés |
| 2026-10-03 | DT-M1 (olvasói konkordancia a #25 előtt, #25 kettéválasztása #25a/#25b-re) a terv legnagyobb sorrend-módosítása | nyitott — felhasználói döntés |
| 2026-10-03 | v2: 4a. szakasz — a teljes projekt feladattérképe a FELADATOK.md v1.3 nyitott sorai alapján (21 régi: 3 módosul, 5 bemenet, 13 marad; 9 új); a „?” tételeket a #47 hitelesíti a repó ellen; az 1. szakaszban a meglévő briefek viszonya | kiegészítés |
| 2026-10-04 | v3 (#52 TERV\_SZINKRON, 1. futás; kiindulás: merge `8e8f771`): DT-M6 és az 1. szakasz 3. elve a DT-F33e–j szerint; a tervezett feladatok sorszám helyett kóddal (DT-F52a: a #47–#55 a FELADATOK-ban már más feladat); a 4a térképbe #48, #50, #51, #52; státuszok #22 ⛔, #43 ▶, #44 Károli-rész tárgytalan, #46 ✅, #32 ✅; függések a FELADATOK szerint (#9, #10, #11, #23, #30, #37); 0. lépcső kész; a 6. szakasz licenc-kockázata és mérőszáma a két módra. Ellenőr 1. kör (JAVÍTANDÓ) javítva F52.5-ben: kimeneti fájlnevek kódnévvel, #46 dátum, #44 függés, #9 függés, egy hibás csere | szinkron |
| 2026-10-06 | v4 (#52 TERV\_SZINKRON, 2. futás; kiindulás: FELADATOK v1.3, `main` `69da794`, viszonyítási pont az 1. futás merge-e `de9c464`): DT-M1 🟢 (a #25 kettéválik, #25a = OLVASOI\_KONKORDANCIA, a csonk kettéválasztása külön `/befogad`), DT-M2 🟢 (`szó-szintű-gépi`), DT-M3 🟢 (`adhoc`, csatorna a proveniencia-sorban), DT-M7 🟢 (MCP\_BUROK feltételes, kikerül a 3. hullámból; előbb a #61), DT-M8 🟢 (TERV\_BEFOGAD lezárva: pipa, ATALAKITASI\_TERV 4.7 jelölés, CLAUDE.md KJV-sor); DT2 🟢 (a #10 mércéje); DT40 → #66; a 2. szakaszba DT-M7, DT-M8 sor; sorszámok: #56 BDB\_ADATBLOKK, #62 STRONG\_NORMALIZAL, #63 JELOLTEK\_RETRO, #65 KAROLI\_ELLENORZES (a BDB\_ADATBLOKK az 1. hullámba: közvetlen TSV-változat); státuszok: #22 (Józs PR mergelve, következő a Bírák), #42, #43, #44, #30, #51, #53, #57, #58 ✅, #38 ▶ (6. adag a #56 után); új sorok: #54, #55, #59, #60, #61, #64, #66; a DT-M4–M6 továbbra is nyitott. Napló: `naplok/F52_TERV_SZINKRON_naplo.md` | szinkron |
