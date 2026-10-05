# PaRDeS munkaterv — adatvagyon, eszközök, olvasói nézet

Oct 3, 2026 · @basesoft

## 1. Alapelvek és forrás

Ez a munkaterv az `ADATVAGYON_TERV.md` 21. (hat lépcső) és 22. (SEMA-illesztés) szakaszát bontja feladatokra a repó szabályai szerint: egy session = egy feladat, `F<nn>_<NEV>_BRIEF.md`, kis minta a teljes futás előtt, `fuggetlen-ellenor`, draft PR, `/befogad`. A kilenc tervezett feladat **számot a `/befogad`-tól kap**; addig a kódjával szerepel (TERV\_BEFOGAD … SZPA\_AUDIT), mert az eredetileg javasolt #47–#55 számokat a `FELADATOK.md` időközben más feladatoknak osztotta ki (#47 ALLAPOT\_ELLENTMONDASOK, #48 KJV\_REGI\_KIVEZETES, #49 FOLYTATAS, #50 CI\_JAVITO\_KOR, #51 KONZISZTENCIA, #52 TERV\_SZINKRON; DT-F52a, 2026-10-04). A `#nn` alak ebben a dokumentumban mindig FELADATOK-szám; a dátumokat nem a terv adja, hanem a felhasználó az ütemezéskor (ways-of-working).

Három elv, amitől a terv nem tér el:

1. **Egyik feladat sem ír az `adat/`-ba a briefen kívül**; a `pardes.db` és minden nézet generált. Író eszköz csak a `jeloltek.tsv`-be (SEMA 3. szabály 2.).
2. **Az olvasói konkordancia (motívum nélkül) nem vár a motívum-rétegre** — ez a D46 feloldó feltétele, és eltér a FELADATOK mai sorrendjétől (DT-tétel, l. 2. szakasz).
3. **A publikálás licenc-kérdés, de nem akadály**: a STEPBible-származék CC BY 4.0 alatt, attribúcióval terjeszthető (DT-F33f), a hosting-út nyitott; a kiadás két módban megy, a `licencek.tsv` `kereskedelmi` oszlopa szerint szűrve (DT-F33j, N-F33b); a saját rétegek (párosítás, fordítás, döntés) a projekté, licencük külön DT-tétel, jogászi megerősítéssel.

**Viszony a meglévő briefekhez.** A munkaterv nem vált fel egyetlen meglévő briefet sem. F22 (⛔ megállt, Józs kész), F43 (fut), F44, F07 változatlanul futnak (a 0. lépcső és a 2. hullám bemenetei); F46 kész (2026-10-03); F38 marad, a BDB\_ADATBLOKK adatblokkal és javító menettel egészíti ki; F23 és F11 változatlan, az `olvas:` listájukba az `ADATVAGYON_TERV.md` kerül (TERV\_BEFOGAD, még nyitott); SZOTAR, RENDER, LEXV2 érintetlen. Egyetlen módosul: **F25**, amely a DT-M1 szerint kettéválik — #25a olvasói konkordancia motívum nélkül (= OLVASOI\_KONKORDANCIA) és #25b motívumos nézet (függ #11, #12, #23). A kilenc tervezett feladat ott kap briefet (és számot), ahol ma nincs.

## 2. Döntési előfeltételek (DT-tételek)

Hat döntés, amit a feladatok előtt vagy mellett a felhasználónak kell meghoznia. Mindegyik egy sor a `DONTESEK.md`-ben; a terv a javasolt irányt adja, nem a döntést.

| # | döntés | javasolt irány | melyik feladatot oldja fel |
| --- | --- | --- | --- |
| DT-M1 | Az olvasói konkordancia (motívum nélkül) a #25 előtt, a #11/#23-tól függetlenül kiadható | igen — a D46 feloldó feltétele; a FELADATOK #25 függése kettéválik: #25a konkordancia (függ SQLITE\_EPIT, #44), #25b motívumos nézet (függ #11, #23) | OLVASOI\_KONKORDANCIA |
| DT-M2 | SEMA 1.7 `AZONOSITAS_MODJA` szövege és a DONTESEK 8. szakasza elavult: a #22 szó-szintű Strong-taggelt Károlit ad | módosítás: a `szó-szintű-tagged` érték a `parok_<könyv>` `magas` linkjéből tölthető; a `tartalom-alapú` sorok frissíthetők | KAROLI\_ELLENORZES |
| DT-M3 | SEMA 2.9 `auditok.lepes` új értéke ad hoc kutatói lekérdezésre | `MCP` (vagy `adhoc`), a proveniencia változatlan szabályokkal; a 8. szabály dataset-lefedettsége ezeket a sorokat is számolja | MCP\_BUROK |
| DT-M4 | SEMA 2.13 szerepmátrix bővítése: 13. szerep Károli-megfelelők (+ SZPA alternatíva), 14. szerep rejtett/hamis párhuzam | felvétel `javaslat` állapottal, amíg a #22 nem teljes | OLVASOI\_KONKORDANCIA szó-lap |
| DT-M5 | F44 5.(d): külső `bible-mcp` connector | elvetés egyelőre, saját MCP után újra | MCP\_BUROK |
| DT-M6 | A saját kimenet (párosítás, fordítás, döntés) licence és a két kimeneti mód: a STEPBible-származék DT-F33f szerint CC BY 4.0 alatt, attribúcióval terjeszthető (nem kizárandó); a szűrést a `licencek.tsv` `kereskedelmi` oszlopa adja (DT-F33j, N-F33b) | az első kiadás nem kereskedelmi, minden blokk dataset-kulccsal, forrás- és licenc-jelöléssel; az OLVASOI\_KONKORDANCIA a `kereskedelmi` oszlop szerint szűr; a saját réteg licence (javaslat: CC BY 4.0 az adatra) külön DT-tétel; jogász a kereskedelmi döntéskor | OLVASOI\_KONKORDANCIA publikálás |

A DT-M1 a legsúlyosabb: átrendezi a FELADATOK sorrendjét. A többi öt a séma és a forráspolitika pontosítása, egy-egy sor.

## 3. 0. lépcső — a felhasználó kézi lépései

Ezek nélkül a `/kovetkezo` nem indítja a függő feladatokat, mert a források a cloud proxyról nem elérhetők, vagy a döntés csak a felhasználóé.

- [x] `lxx_bridge` tábla + licencsor → `adat/kulso/lxx_bridge.tsv`, `adat/kulso/LICENC.md` (#43 0. lépés; bent, F43.0)
- [x] a `k-mktr/karoli_bible_hu` kártya licenc-mezője és README-je szó szerint → `adat/kulso/karoli_bible_hu_LICENC.txt` (#44; bent, F44.0 — a Károli-rész a DT-F33e-vel tárgytalan)
- [x] az openbible.info licencnyilatkozata szó szerint → `adat/kulso/openbible_crossrefs_LICENC.txt` (#44; bent, F44.1)
- [x] `ADATVAGYON_TERV.md` és `MUNKATERV.md` a repó gyökerébe, commit (`ab73f7b`, 2026-10-04)
- [ ] a #23/#25 brief `olvas:` listájába felvéve (TERV\_BEFOGAD nyitott része)
- [ ] a 2. szakasz hat DT-tétele eldöntve (legalább DT-M1, DT-M2, DT-M3 a 2. hullám előtt)
- [ ] a #38 naplójában ellenőrizve: az M0 5. pont (BDB-gyökcsoport-felmérés) lefutott-e; a DT-F38i (6. adag indul-e) feloldva
- [ ] tárhely-döntés előkészítése: böngészős SQLite, cPanel (PHP vagy Python a lekérdező) vagy Netlify — a licenc nem kényszerít (DT-F33f), a mód és az offline-igény dönt (DT-F33j); az OLVASOI\_KONKORDANCIA előtt ⛔

## 4. Feladatlista (javasolt FELADATOK-sorok)

Minden sor egy brief. A „kis minta" oszlop az elfogadási próba, amit a teljes futás előtt a felhasználó jóváhagy (playbook 3.). Modell: Sonnet, ahol nincs más jelölve; az `ellenor` mindig Haiku vagy Sonnet, a brieftől független menetben.

| # | név | cél | bemenet | kimenet | kis minta → elfogadás | függ | menet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | TERV\_BEFOGAD (részben kész: a három dokumentum a repóban, `ab73f7b`; nyitott: a #23/#25 brief `olvas:` sora, ATALAKITASI\_TERV 4.7, CLAUDE.md KJV-sor) | az `ADATVAGYON_TERV.md` és a `MUNKATERV.md` repóba vétele; a #23, #25 brief `olvas:` sora; ATALAKITASI\_TERV 4.7 elavultként jelölve; CLAUDE.md KJV-sora javítva | a két Markdown | commit, három fájl módosítása | — (szerkesztés) | 0. lépcső | ½ |
| — | KAROLI\_ELLENORZES | 1.1 ellenőrzés: a Genezis-igehelyes tematikus táblák Károli-idézet + Strong párjai a `parok_<könyv>` ellen, csak `magas` linkre; 1.2 variancia-térkép; a Károli-triplet frissítése (`tartalom-alapú` → `szó-szintű-tagged`) a `jeloltek`/`elofordulasok` sorain | `tematikus_lezart/*.md`, `adat/karoli_strong/parok_*.tsv`, `jeloltek.tsv` | `naplok/KAROLI_ELLENORZES_elteresek.tsv`; `adat/karoli_variancia.tsv` (Strong → szóalakok db; szóalak → Strongok); triplet-frissítő PR | ANTROP-001 egy motívumon: eltéréslista + 3 triplet-sor átnézve | #62, #63 (brief); a #22 bemenet, nem előfeltétel: a kész könyveken fut (1–5Móz és Józs; `nem_fugg: [22]`), DT-M2 🟢 | 1 |
| — | STRONG\_NORMALIZAL | N37: egyetlen `strong_normalizal()` függvény (`H922` → `H0922`, `G746`, `+` láncok), `lekerdez.py`-ba és `betolt.py`-ba kötve; N21 nullázatlan értékek javítása | `eszkozok/*.py`, `adat/*.tsv` | függvény + teszt; javított TSV-sorok | 20 ismert eltérő alak | — | ½ |
| — | SQLITE\_EPIT | `eszkozok/sqlite_epit.py`: SEMA-típusok, `IGEHELY` normalizálás a `Konyv_normalizalo_tabla`-n át, KK-alapú vers-kulcs, `szamozas` (BSB-értékkészlet + N46), `licenc_allapot` és `kereskedelmi` minden táblán, `strong_parok` és frázis-pozíció előszámolva, FTS a `motivumok/` fölött; a SEMA 3. szakasz nyolc integritási szabálya tesztként, sértésnél megáll; `pardes.db` `.gitignore`-ban | `adat/*.tsv`, `konkordancia/*.tsv`, `licencek.tsv` | `pardes.db` (helyben), `naplok/SQLITE_EPIT_integritas.md` | 8 lexikonoldalas motívum + 1Mózes; a 26 pontból a 1–6, 13–15 lekérdezése visszaadja a tanulmányok ismert tényeit | STRONG\_NORMALIZAL | 1–2 |
| — | MCP\_BUROK | FastMCP burok a `lekerdez.py`-ra, ≤ 8 eszköz: `lekerdez(parancs, …)`, `vers_lap`, `szo_lap`, `lelet_lap`, `ellenoriz`, `karoli_szoalakok`; minden hívás proveniencia-sorral és `auditok.tsv`-sorral (`lepes=MCP`); csak olvasó; `.mcp.json` | SQLITE\_EPIT, `lekerdez.py` | `eszkozok/mcp_szerver.py`, `.mcp.json`, `naplok/MCP_BUROK_eszkozteszt.md` | a `lexikai-scan` subagent egy ANTROP-001 futása eszközökön át ugyanazt adja, mint CLI-n | SQLITE\_EPIT, DT-M3, DT-M5 | 1 |
| — | BDB\_ADATBLOKK | a 12.1 szócikk-adatlekérés build-lépésként: Python előre számolja a Károli-szóalakok, példaversek, LXX-híd, rokonok, meglévő szócikk blokkját, és az adagfájlban a BDB-szócikk elé fűzi; `terminologia.tsv` olvasása minden adagban; a fordító prompt egy sora (`[NINCS KÁROLI-ALAK]`) | SQLITE\_EPIT (vagy közvetlen TSV), `BDB_FORDITAS_BRIEF.md` | adagfájl-generátor; a #38 javító menetének briefje | 10 szócikk H2617 körül: a blokk minden száma és idézete eszköz-kimenetből | SQLITE\_EPIT (vagy TSV); a #38 nem előfeltétel, hanem ráépül: a 6. adag a #56 után fut (F38 `fugg: [34, 56]`, F56 `nem_fugg: [38]`, DT-F38i 🟢) | 1 |
| — | JELOLTEK\_RETRO | a 8 retroaktív (F3/N14) motívum `jeloltek.tsv`-sorainak feltöltése a naplókból; a származtatott „még nem vizsgált" lista (`auditok` scan − `jeloltek`) generátora; a 12-es lelet-lap adatának első teljes futása | `tematikus_lezart/naplok/*.md`, `auditok.tsv`, `jeloltek.tsv` | `jeloltek.tsv` bővítés (PR), `eszkozok/nem_vizsgalt.py`, `naplok/JELOLTEK_RETRO_lelet_ANTROP.md` | ANTROP-001: minden ★ sor mellett `dontes` + `indoklas`, 0 „még nem vizsgált" | — (adat megvan) | 1–2 |
| — | OLVASOI\_KONKORDANCIA | első publikus kiadás motívum nélkül: `general.py --cel verslap / szolap`; szó-lap a szerepmátrix (18.5) szerint, `allapot` vezérli a blokkokat; vers-lap KK-kulccsal, Károli 1908 nyílt szöveg; lekérdező a hosting-döntés szerint (böngészős SQLite, cPanel PHP vagy Netlify Function) a `kereskedelmi` oszlop szerinti mód-szűrővel (DT-F33j); tipográfia/színséma kapcsoló | SQLITE\_EPIT, #44, `karoli_bible_hu`, 1–6, 13–16, 18–20. pont | `kimenet/olvasoi/` generált oldalak, `api/kereses.*`, `naplok/OLVASOI_KONKORDANCIA_publikalas.md` | 20 vers + 20 Strong lapja; minden adat a `pardes.db`-ből; minden blokk alatt forrás és licenc, nincs blokk dataset-kulcs nélkül (nem kereskedelmi mód, N-F33b) | SQLITE\_EPIT, #44, DT-M1, DT-M4, DT-M6; hosting ⛔ | 2–3 |
| — | SZPA\_AUDIT | a profil C üzemmódja: 1.2 tiltólista és 1.1 kötött párok gépi ellenőrzése a tanulmányok prózáján és a BDB-fordításon; kimenet a C-táblázat | `SZPA_FORDITOI_PROFIL_prompt.md`, tanulmányok, `forditasok.tsv` | `naplok/SZPA_AUDIT_szpa_audit.tsv` | 2 tanulmány + 50 szócikk | — | ½ |

Az OLVASOI\_KONKORDANCIA után a meglévő lánc fut tovább: #23 (motívum-séma, mélységi szintek) → #9/#10 (lexikonoldal) → #11 (egy forrásból renderelés) → #25b (motívum-lap, lelet-lap ★, a 7–12. és 21–26. pont). Az MCP\_BUROK és JELOLTEK\_RETRO kimenete ezekbe épül, nem külön rendszer.

## 4a. A teljes projekt feladattérképe

Minden nyitott FELADATOK-sor (v1.3; státuszok és függések frissítve 2026-10-04, #52 TERV\_SZINKRON) és a kilenc tervezett, fázisonként. A „terv" oszlop a viszony a munkatervhez: **marad** (nem érinti), **módosul** (a terv egy ponton átírja), **bemenet** (a terv valamelyik feladata rá épül), **új**. A „?" olyan állítás, amit a repó ellen a TERV\_BEFOGAD első sessionje hitelesít — a kész feladatok briefjeit, a naplókat és az eszközök kódját ez a terv nem látta.

**1. fázis — adatréteg**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #22 | Károli–Strong párosítás könyvenként | ⛔ megállt (1–5Móz és Józs kész; a Józs PR merge-e és a következő könyv döntése a felhasználóra vár) | #21 ✅ | **bemenet** | KAROLI\_ELLENORZES könyvenként újrafut rá; SQLITE\_EPIT, OLVASOI\_KONKORDANCIA forrása; 13. szerep (DT-M4) |
| #38 | BDB teljes magyar fordítása | ⛔ DT-F38i (5 adag kész) | #34 ✅ | **módosul** | a 6. adagtól a BDB\_ADATBLOKK adatblokkjával; javító menet a teljes #22 után |
| #43 | LXX-döntések ellenőrzése lxx\_bridge-dzsel | ▶ fut (DT-F43 ✅: a bridge nem független forrás, csak tájékoztató; a draft PR merge-e a felhasználóra vár) | #8 ✅ | **bemenet** | 0. lépcső; a 26-os pont, a szó-lap LXX-blokkja |
| #44 | Licenc-utókövetés: Károli 1908, openbible.info | ⬜ (a 0. lépés fájljai bent; a Károli-rész a DT-F33e-vel tárgytalan, az openbible/TVTMS-rész marad) | #33 ✅, #42 | **bemenet** | 0. lépcső; az OLVASOI\_KONKORDANCIA publikálási előfeltétele |
| #46 | BDB rosszul feloldott könyvnevei | ✅ kész (2026-10-03) | #34 ✅ | marad | a BDB\_ADATBLOKK példaversei innen javítva |
| #7 | Thayer teljes magyar fordítása | ⬜ brief kell | #3, #5, #14 ✅ | marad | D46: az OLVASOI\_KONKORDANCIA oldja fel; a BDB\_ADATBLOKK mintájára adatblokkal |
| #23 | Egyforrású motívumdokumentum, mélységi szintek | ⬜ M0 után; M1 a #12a próza-próba után (DT-F32a) | #32 ✅, #37\* | marad | a motívum-séma itt születik; a 7–12, 21–26. pont erre vár; #25b feltétele |
| #27 | Thayer: Opus/Gemini összevetés | ⬜ | — | marad | nem érinti |
| #30 | Döntés- és N-számok kiosztása merge-kor | ⬜ | #8, #16, #17 ✅ | marad | a DT-M1–M6 számozása ezen át |
| #40 | Hivatkozás-ellenőrzés CI-szabály | ⬜ | #2 ✅, #30\*, #37\* | marad | a TERV\_BEFOGAD által módosított briefek hivatkozásai |
| #48 | KJV\_REGI\_KIVEZETES: a régi studybible.info KJV/ASV fájlok kivezetése, minden az eBible KJV-forrásra | ⬜ | #19, #21 ✅, #22 | **bemenet** | az SQLITE\_EPIT KJV-forrása a `KJV_Strongs_teljes`; az ASV kiesik (N29 lezárva, D7) |

**2. fázis — render**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #9 | Szótári adatréteg S2 | ⬜ | #5, #6 ✅, #7\*, #23, #38\* | marad | lexikonoldal = szó-lap elv; a 13–14. szerep (DT-M4) ide |
| #10 | 8 lexikonoldal lezárása | ⬜ brief kell | #8 ✅, #9, #11 | marad | — |
| #11 | Migráció: egy forrásból renderelés | ⬜ brief kell (a #12a után) | #9, #23 | **módosul** (kicsi) | `olvas:` listába az ADATVAGYON\_TERV (TERV\_BEFOGAD); vers-lap/szó-lap mint `general.py --cel` ide ? |
| #12 | TEREMT-002 3. lépés | ⬜ brief kell | #11 | marad | — |
| #13 | 1Móz 17-től tanulmányok, 6 betöltetlen motívum | ⬜ brief kell | #10 | marad | a JELOLTEK\_RETRO után tisztábban futhat ? |
| #25 | Olvasói felület: statikus HTML mélységgel | ⬜ brief kell | #11, #12, #23 | **módosul** | DT-M1: kettéválik — **#25a** = OLVASOI\_KONKORDANCIA (konkordancia motívum nélkül, függ SQLITE\_EPIT, #44); **#25b** motívumos nézet (függ #11, #12, #23) |
| #36 | Éles lexikon/ újragenerálása | ⬜ | #7\*, #9\*, #28, #34, #35 ✅ … | marad | az OLVASOI\_KONKORDANCIA generátora ugyanabban a CI-futásban (N33) |

**Folyamat és eszközök**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #32 | Kontextus-őrzés | ✅ kész (2026-10-04; négy szabály a MUNKAMENET-ben, `munka` mező a fejlécben, DT-F32a/b/c) | — | marad | a guide 6. szakasza alkalmazza |
| #37 | Tanulmány-ellenőrzés: CI + független ellenőr | ⬜ | #30, #32 ✅, #45\* | **bemenet** | a KAROLI\_ELLENORZES eltéréslistája és az MCP `ellenoriz` eszköz; a session 5. lépése |
| #42 | Forrásfájlok kivezetése, licencállapot egy forrása | ⬜ | #33, #35 ✅ | **bemenet** | a `licenc_allapot` szűrő forrása; SQLITE\_EPIT, OLVASOI\_KONKORDANCIA feltétele |
| #45 | Modell-ellenőrzés brief elején | ⬜ | — | marad | minden új brief fejlécébe |
| #50 | CI\_JAVITO\_KOR: push után a CI olvasása, a saját PR hibáinak javítása | ⬜ | — | marad | minden brief záró lépése |
| #51 | KONZISZTENCIA: döntések átvezetésének gépi és ügynöki ellenőrzése | ⬜ | #37\* | **bemenet** | a TERV\_SZINKRON (#52) kiváltó jelzése |
| #52 | TERV\_SZINKRON: a tervdokumentumok átvezetése a repó állapotára | ▶ fut (1. futás 2026-10-04) | — | **új** | ez a dokumentum, az ADATVAGYON\_TERV és a VIBE\_GUIDE karbantartója; ismétlődő |

**Tervezett (a kilenc új; szám a befogadásnál)** — részletek a 4. szakaszban; itt a fázis-besorolás:

| # | fázis | mire ül |
| --- | --- | --- |
| TERV\_BEFOGAD (részben kész) | folyamat | dokumentum |
| KAROLI\_ELLENORZES | 1. adatréteg | #62, #63; a #22 bemenet (kész könyvek), DT-M2 🟢 |
| STRONG\_NORMALIZAL | eszközök | N37, N21 |
| SQLITE\_EPIT | eszközök | STRONG\_NORMALIZAL, SEMA 3. |
| MCP\_BUROK | eszközök | SQLITE\_EPIT, ATALAKITASI\_TERV 11.7, DT-M3 |
| BDB\_ADATBLOKK | 1. adatréteg | SQLITE\_EPIT; a #38 ráépül (a 6. adag a #56 után, DT-F38i) |
| JELOLTEK\_RETRO | 1. adatréteg | SEMA 2.4, F3/N14 |
| OLVASOI\_KONKORDANCIA (= #25a) | 2. render | SQLITE\_EPIT, #44, DT-M1, DT-M6 |
| SZPA\_AUDIT | folyamat | SZPA-profil |

**Kész feladatok, amelyekre a terv épít, de a briefjüket nem látta:** #21 (pilot), #8 (LXX-döntések), #5/#6 (szótár S1), #14, #28, #33, #34, #35, #16/#17, #19 (KJV teljes), #24 (licenc-leltár), #41 (versszámozás) ? — állapotuk a FELADATOK „Kész" szakaszából, a TERV\_BEFOGAD veszi át. A terv írása után kész (2026-10-04): #26 (D34–D41), #32 (KONTEXTUS), #49 (FOLYTATAS); a #46 már 2026-10-03-án kész volt, a terv elavult státusszal vette fel.

**Összesítve (2026-10-04):** 19 nyitott régi feladat (a #32 és a #46 kész) — 3 módosul (#38, #25, #11 kicsit), 5 bemenet (#22, #43, #44, #37, #42), 11 marad érintetlenül; 4 új FELADATOK-sor a terven kívülről (#48 és #51 bemenet, #50 marad, #52 új); 9 tervezett (1 részben kész). Egyetlen régi feladat sem szűnik meg.

## 5. Hullámok és megállási pontok

A feladatok négy hullámban futnak; egy hullámon belül párhuzamosíthatók (külön session, külön ág). A ⛔ a felhasználói megállás, ahol a következő hullám nem indul.

| hullám | feladatok | miért együtt | ⛔ a végén |
| --- | --- | --- | --- |
| 1 | 0. lépcső (kész); TERV\_BEFOGAD (részben kész); STRONG\_NORMALIZAL; JELOLTEK\_RETRO; SZPA\_AUDIT | egyik sem függ a másiktól, és egyik sem igényel új adatot; a JELOLTEK\_RETRO az első teljes lelet-lap-adat, az SZPA\_AUDIT azonnal mérhető hozam | DT-M1–M3 eldöntve; a #43/#44 kézi fájlok bent (kész); a #43 fut; a #44 a #42-re vár |
| 2 | KAROLI\_ELLENORZES; SQLITE\_EPIT | a KAROLI\_ELLENORZES a #22 kész könyveire fut, az SQLITE\_EPIT a STRONG\_NORMALIZAL-re épül; a két brief független | az SQLITE\_EPIT integritási tesztje 0 sértés; a KAROLI\_ELLENORZES eltéréslistája átnézve, a triplet-frissítés PR-je befogadva |
| 3 | MCP\_BUROK; BDB\_ADATBLOKK | mindkettő a `pardes.db`-n ül; a BDB\_ADATBLOKK a #38 javító menetét készíti elő, az MCP\_BUROK a kutatást | az MCP\_BUROK eszközteszt egyezik a CLI-vel; a #38 6. adagja a BDB\_ADATBLOKK adatblokkjával indul (DT-F38i) |
| 4 | OLVASOI\_KONKORDANCIA | az első publikus kiadás; csak a hosting-döntés és a DT-M6 után | hosting ⛔; a mód-szűrő és a blokkonkénti forrásjelölés átnézve (DT-F33j, N-F33b); első 40 lap jóváhagyva → publikálás |
| után | #23 → #9/#10 → #11 → #25b | a motívum-réteg a kész konkordanciára ül | a FELADATOK meglévő megállásai (A4/B5) |

A hullámoktól függetlenül, folyamat-feladatként fut: #50 CI\_JAVITO\_KOR, #51 KONZISZTENCIA, #52 TERV\_SZINKRON (ismétlődő, a briefje 2. pontja szerinti eseményeknél).

Közben folyamatosan: **#22** könyvenként (Józs kész; ⛔ a felhasználónál a következő könyvig) és **#38** adagonként — a 2. hullámtól a KAROLI\_ELLENORZES minden új Károli–Strong könyvre újrafuttatható, a 3. hullámtól a #38 adagjai a BDB\_ADATBLOKK blokkjával mennek.

```
1. hullám  ─▶  2. hullám  ─▶  3. hullám  ─▶  4. hullám  ─▶  #23 → #9/#10 → #11 → #25b
0. lépcső ✓         KAROLI_ELLENORZES   MCP_BUROK       OLVASOI_KONKORDANCIA
TERV_BEFOGAD (rész) SQLITE_EPIT         BDB_ADATBLOKK
STRONG_NORMALIZAL
JELOLTEK_RETRO
SZPA_AUDIT
     ⛔ DT-M1–3          ⛔ 0 sértés          ⛔ DT-F38i      ⛔ hosting, DT-M6
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
