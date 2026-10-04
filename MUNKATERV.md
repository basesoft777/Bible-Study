# PaRDeS munkaterv — adatvagyon, eszközök, olvasói nézet

Oct 3, 2026 · @basesoft

## 1. Alapelvek és forrás

Ez a munkaterv az `ADATVAGYON_TERV.md` 21. (hat lépcső) és 22. (SEMA-illesztés) szakaszát bontja feladatokra a repó szabályai szerint: egy session = egy feladat, `F<nn>_<NEV>_BRIEF.md`, kis minta a teljes futás előtt, `fuggetlen-ellenor`, draft PR, `/befogad`. A sorszámok (#47–#55) **javaslatok** — a `FELADATOK.md`-ben a felhasználó véglegesíti; a dátumokat nem a terv adja, hanem a felhasználó az ütemezéskor (ways-of-working).

Három elv, amitől a terv nem tér el:

1. **Egyik feladat sem ír az `adat/`-ba a briefen kívül**; a `pardes.db` és minden nézet generált. Író eszköz csak a `jeloltek.tsv`-be (SEMA 3. szabály 2.).
2. **Az olvasói konkordancia (motívum nélkül) nem vár a motívum-rétegre** — ez a D46 feloldó feltétele, és eltér a FELADATOK mai sorrendjétől (DT-tétel, l. 2. szakasz).
3. **A publikálás licenc-kérdés**: a STEPBible-származék nem terjeszthető (DT-F33a), ezért csak backend-út; a saját rétegek (párosítás, fordítás, döntés) a projekté, jogászi megerősítéssel.

**Viszony a meglévő briefekhez.** A munkaterv nem vált fel egyetlen meglévő briefet sem. F22, F43, F44, F46, F07 változatlanul futnak (a 0. lépcső és a 2. hullám bemenetei); F38 marad, a #52 adatblokkal és javító menettel egészíti ki; F23 és F11 változatlan, az `olvas:` listájukba az `ADATVAGYON_TERV.md` kerül (#47); SZOTAR, RENDER, LEXV2 érintetlen. Egyetlen módosul: **F25**, amely a DT-M1 szerint kettéválik — #25a olvasói konkordancia motívum nélkül (= #54) és #25b motívumos nézet (függ #11, #23). A #47–#55 ott kap briefet, ahol ma nincs.

## 2. Döntési előfeltételek (DT-tételek)

Hat döntés, amit a feladatok előtt vagy mellett a felhasználónak kell meghoznia. Mindegyik egy sor a `DONTESEK.md`-ben; a terv a javasolt irányt adja, nem a döntést.

| # | döntés | javasolt irány | melyik feladatot oldja fel |
| --- | --- | --- | --- |
| DT-M1 | Az olvasói konkordancia (motívum nélkül) a #25 előtt, a #11/#23-tól függetlenül kiadható | igen — a D46 feloldó feltétele; a FELADATOK #25 függése kettéválik: #25a konkordancia (függ #50, #44), #25b motívumos nézet (függ #11, #23) | #54 |
| DT-M2 | SEMA 1.7 `AZONOSITAS_MODJA` szövege és a DONTESEK 8. szakasza elavult: a #22 szó-szintű Strong-taggelt Károlit ad | módosítás: a `szó-szintű-tagged` érték a `parok_<könyv>` `magas` linkjéből tölthető; a `tartalom-alapú` sorok frissíthetők | #48 |
| DT-M3 | SEMA 2.9 `auditok.lepes` új értéke ad hoc kutatói lekérdezésre | `MCP` (vagy `adhoc`), a proveniencia változatlan szabályokkal; a 8. szabály dataset-lefedettsége ezeket a sorokat is számolja | #51 |
| DT-M4 | SEMA 2.13 szerepmátrix bővítése: 13. szerep Károli-megfelelők (+ SZPA alternatíva), 14. szerep rejtett/hamis párhuzam | felvétel `javaslat` állapottal, amíg a #22 nem teljes | #54 szó-lap |
| DT-M5 | F44 5.(d): külső `bible-mcp` connector | elvetés egyelőre, saját MCP után újra | #51 |
| DT-M6 | DT-F33a terjesztési kérdés az olvasói felületre: a saját kimenet (párosítás, fordítás, döntés) státusza, a STEPBible-származék kizárása a publikus nézetből | jogász a kereskedelmi döntéskor; addig a #54 csak tisztázott/közkincs/saját rétegből tölt, `licenc_allapot` szűrővel | #54 publikálás |

A DT-M1 a legsúlyosabb: átrendezi a FELADATOK sorrendjét. A többi öt a séma és a forráspolitika pontosítása, egy-egy sor.

## 3. 0. lépcső — a felhasználó kézi lépései

Ezek nélkül a `/kovetkezo` nem indítja a függő feladatokat, mert a források a cloud proxyról nem elérhetők, vagy a döntés csak a felhasználóé.

- [ ] `lxx_bridge` CSV letöltése + licencsor → `adat/kulso/lxx_bridge.csv`, `adat/kulso/LICENC.md` (#43 0. lépés)
- [ ] a `k-mktr/karoli_bible_hu` kártya licenc-mezője és README-je szó szerint → `adat/kulso/karoli_bible_hu_LICENC.txt` (#44)
- [ ] az openbible.info licencnyilatkozata szó szerint → `adat/kulso/openbible_crossrefs_LICENC.txt` (#44)
- [ ] `ADATVAGYON_TERV.md` és `MUNKATERV.md` a repó gyökerébe, commit; a #23/#25 brief `olvas:` listájába felvéve
- [ ] a 2. szakasz hat DT-tétele eldöntve (legalább DT-M1, DT-M2, DT-M3 a 2. hullám előtt)
- [ ] a #38 naplójában ellenőrizve: az M0 5. pont (BDB-gyökcsoport-felmérés) lefutott-e; a DT-F38i (6. adag indul-e) feloldva
- [ ] tárhely-döntés előkészítése: van-e cPanel-tárhely (PHP vagy Python a lekérdező), vagy Netlify marad — a #54 előtt ⛔

## 4. Feladatlista (javasolt FELADATOK-sorok)

Minden sor egy brief. A „kis minta" oszlop az elfogadási próba, amit a teljes futás előtt a felhasználó jóváhagy (playbook 3.). Modell: Sonnet, ahol nincs más jelölve; az `ellenor` mindig Haiku vagy Sonnet, a brieftől független menetben.

| # | név | cél | bemenet | kimenet | kis minta → elfogadás | függ | menet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #47 | TERV\_BEFOGAD | az `ADATVAGYON_TERV.md` és a `MUNKATERV.md` repóba vétele; a #23, #25 brief `olvas:` sora; ATALAKITASI\_TERV 4.7 elavultként jelölve; CLAUDE.md KJV-sora javítva | a két Markdown | commit, három fájl módosítása | — (szerkesztés) | 0. lépcső | ½ |
| #48 | KAROLI\_ELLENORZES | 1.1 ellenőrzés: a Genezis-igehelyes tematikus táblák Károli-idézet + Strong párjai a `parok_<könyv>` ellen, csak `magas` linkre; 1.2 variancia-térkép; a Károli-triplet frissítése (`tartalom-alapú` → `szó-szintű-tagged`) a `jeloltek`/`elofordulasok` sorain | `tematikus_lezart/*.md`, `adat/karoli_strong/parok_*.tsv`, `jeloltek.tsv` | `naplok/F48_elteresek.tsv`; `adat/karoli_variancia.tsv` (Strong → szóalakok db; szóalak → Strongok); triplet-frissítő PR | ANTROP-001 egy motívumon: eltéréslista + 3 triplet-sor átnézve | #22 könyvenként (1–5Móz kész), DT-M2 | 1 |
| #49 | STRONG\_NORMALIZAL | N37: egyetlen `strong_normalizal()` függvény (`H922` → `H0922`, `G746`, `+` láncok), `lekerdez.py`-ba és `betolt.py`-ba kötve; N21 nullázatlan értékek javítása | `eszkozok/*.py`, `adat/*.tsv` | függvény + teszt; javított TSV-sorok | 20 ismert eltérő alak | — | ½ |
| #50 | SQLITE\_EPIT | `eszkozok/sqlite_epit.py`: SEMA-típusok, `IGEHELY` normalizálás a `Konyv_normalizalo_tabla`-n át, KK-alapú vers-kulcs, `szamozas` (BSB-értékkészlet + N46), `licenc_allapot` minden táblán, `strong_parok` és frázis-pozíció előszámolva, FTS a `motivumok/` fölött; a SEMA 3. szakasz nyolc integritási szabálya tesztként, sértésnél megáll; `pardes.db` `.gitignore`-ban | `adat/*.tsv`, `konkordancia/*.tsv`, `licencek.tsv` | `pardes.db` (helyben), `naplok/F50_integritas.md` | 8 lexikonoldalas motívum + 1Mózes; a 26 pontból a 1–6, 13–15 lekérdezése visszaadja a tanulmányok ismert tényeit | #49 | 1–2 |
| #51 | MCP\_BUROK | FastMCP burok a `lekerdez.py`-ra, ≤ 8 eszköz: `lekerdez(parancs, …)`, `vers_lap`, `szo_lap`, `lelet_lap`, `ellenoriz`, `karoli_szoalakok`; minden hívás proveniencia-sorral és `auditok.tsv`-sorral (`lepes=MCP`); csak olvasó; `.mcp.json` | #50, `lekerdez.py` | `eszkozok/mcp_szerver.py`, `.mcp.json`, `naplok/F51_eszkozteszt.md` | a `lexikai-scan` subagent egy ANTROP-001 futása eszközökön át ugyanazt adja, mint CLI-n | #50, DT-M3, DT-M5 | 1 |
| #52 | BDB\_ADATBLOKK | a 12.1 szócikk-adatlekérés build-lépésként: Python előre számolja a Károli-szóalakok, példaversek, LXX-híd, rokonok, meglévő szócikk blokkját, és az adagfájlban a BDB-szócikk elé fűzi; `terminologia.tsv` olvasása minden adagban; a fordító prompt egy sora (`[NINCS KÁROLI-ALAK]`) | #50 (vagy közvetlen TSV), `BDB_FORDITAS_BRIEF.md` | adagfájl-generátor; a #38 javító menetének briefje | 10 szócikk H2617 körül: a blokk minden száma és idézete eszköz-kimenetből | #50, #38 ⛔ DT-F38i feloldva | 1 |
| #53 | JELOLTEK\_RETRO | a 8 retroaktív (F3/N14) motívum `jeloltek.tsv`-sorainak feltöltése a naplókból; a származtatott „még nem vizsgált" lista (`auditok` scan − `jeloltek`) generátora; a 12-es lelet-lap adatának első teljes futása | `tematikus_lezart/naplok/*.md`, `auditok.tsv`, `jeloltek.tsv` | `jeloltek.tsv` bővítés (PR), `eszkozok/nem_vizsgalt.py`, `naplok/F53_lelet_ANTROP.md` | ANTROP-001: minden ★ sor mellett `dontes` + `indoklas`, 0 „még nem vizsgált" | — (adat megvan) | 1–2 |
| #54 | OLVASOI\_KONKORDANCIA | első publikus kiadás motívum nélkül: `general.py --cel verslap / szolap`; szó-lap a szerepmátrix (18.5) szerint, `allapot` vezérli a blokkokat; vers-lap KK-kulccsal, Károli 1908 nyílt szöveg; backend-lekérdező (cPanel PHP vagy Netlify Function) `licenc_allapot` szűrővel; tipográfia/színséma kapcsoló | #50, #44, `karoli_bible_hu`, 1–6, 13–16, 18–20. pont | `kimenet/olvasoi/` generált oldalak, `api/kereses.*`, `naplok/F54_publikalas.md` | 20 vers + 20 Strong lapja; minden adat a `pardes.db`-ből; a 17.1 licenc-szűrő STEPBible-származékot nem enged ki | #50, #44, DT-M1, DT-M4, DT-M6; hosting ⛔ | 2–3 |
| #55 | SZPA\_AUDIT | a profil C üzemmódja: 1.2 tiltólista és 1.1 kötött párok gépi ellenőrzése a tanulmányok prózáján és a BDB-fordításon; kimenet a C-táblázat | `SZPA_FORDITOI_PROFIL_prompt.md`, tanulmányok, `forditasok.tsv` | `naplok/F55_szpa_audit.tsv` | 2 tanulmány + 50 szócikk | — | ½ |

A #54 után a meglévő lánc fut tovább: #23 (motívum-séma, mélységi szintek) → #9/#10 (lexikonoldal) → #11 (egy forrásból renderelés) → #25b (motívum-lap, lelet-lap ★, a 7–12. és 21–26. pont). A #51 és #53 kimenete ezekbe épül, nem külön rendszer.

## 4a. A teljes projekt feladattérképe

Minden nyitott FELADATOK-sor (2026-10-03, v1.3) és a kilenc új, fázisonként. A „terv" oszlop a viszony a munkatervhez: **marad** (nem érinti), **módosul** (a terv egy ponton átírja), **bemenet** (a terv valamelyik feladata rá épül), **új**. A „?" olyan állítás, amit a repó ellen a #47 első sessionje hitelesít — a kész feladatok briefjeit, a naplókat és az eszközök kódját ez a terv nem látta.

**1. fázis — adatréteg**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #22 | Károli–Strong párosítás könyvenként | ▶ fut (1–5Móz kész, Józsué jön) | #21 ✅ | **bemenet** | #48 könyvenként újrafut rá; #50, #54 forrása; 13. szerep (DT-M4) |
| #38 | BDB teljes magyar fordítása | ⛔ DT-F38i (5 adag kész) | #34 ✅ | **módosul** | a 6. adagtól a #52 adatblokkjával; javító menet a teljes #22 után |
| #43 | LXX-döntések ellenőrzése lxx\_bridge-dzsel | ⬜ merge-elve, kézi 0. lépésre vár | #8 ✅ | **bemenet** | 0. lépcső; a 26-os pont, a szó-lap LXX-blokkja |
| #44 | Licenc-utókövetés: Károli 1908, openbible.info | ⬜ draft PR, kézi 0. lépésre vár | #33 ✅, #42 | **bemenet** | 0. lépcső; a #54 publikálási előfeltétele |
| #46 | BDB rosszul feloldott könyvnevei | ⬜ | #34 ✅ | marad | a #52 példaversei innen javítva |
| #7 | Thayer teljes magyar fordítása | ⬜ brief kell | #3, #5, #14 ✅ | marad | D46: a #54 oldja fel; a #52 mintájára adatblokkal |
| #23 | Egyforrású motívumdokumentum, mélységi szintek | ⬜ M0 után | #37\* | marad | a motívum-séma itt születik; a 7–12, 21–26. pont erre vár; #25b feltétele |
| #27 | Thayer: Opus/Gemini összevetés | ⬜ | — | marad | nem érinti |
| #30 | Döntés- és N-számok kiosztása merge-kor | ⬜ | #8, #16, #17 ✅, #32\* | marad | a DT-M1–M6 számozása ezen át |
| #40 | Hivatkozás-ellenőrzés CI-szabály | ⬜ | #2 ✅, #30\*, #37\* | marad | a #47 által módosított briefek hivatkozásai |

**2. fázis — render**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #9 | Szótári adatréteg S2 | ⬜ | #5, #6 ✅, #7\*, #38\*, #46\* | marad | lexikonoldal = szó-lap elv; a 13–14. szerep (DT-M4) ide |
| #10 | 8 lexikonoldal lezárása | ⬜ brief kell | #8 ✅, #9 | marad | — |
| #11 | Migráció: egy forrásból renderelés | ⬜ brief kell | #9 | **módosul** (kicsi) | `olvas:` listába az ADATVAGYON\_TERV (#47); vers-lap/szó-lap mint `general.py --cel` ide ? |
| #12 | TEREMT-002 3. lépés | ⬜ brief kell | #11 | marad | — |
| #13 | 1Móz 17-től tanulmányok, 6 betöltetlen motívum | ⬜ brief kell | #10 | marad | a #53 után tisztábban futhat ? |
| #25 | Olvasói felület: statikus HTML mélységgel | ⬜ brief kell | #11, #12, #23 | **módosul** | DT-M1: kettéválik — **#25a** = #54 (konkordancia motívum nélkül, függ #50, #44); **#25b** motívumos nézet (függ #11, #12, #23) |
| #36 | Éles lexikon/ újragenerálása | ⬜ | #7\*, #9\*, #28, #34, #35 ✅ … | marad | a #54 generátora ugyanabban a CI-futásban (N33) |

**Folyamat és eszközök**

| # | feladat | státusz | függ | terv | kapcsolat |
| --- | --- | --- | --- | --- | --- |
| #32 | Kontextus-őrzés | ⬜ | — | marad | a guide 6. szakasza alkalmazza |
| #37 | Tanulmány-ellenőrzés: CI + független ellenőr | ⬜ | #30, #32, #45\* | **bemenet** | a #48 eltéréslistája és az MCP `ellenoriz` eszköz; a session 5. lépése |
| #42 | Forrásfájlok kivezetése, licencállapot egy forrása | ⬜ | #33, #35 ✅ | **bemenet** | a `licenc_allapot` szűrő forrása; #50, #54 feltétele |
| #45 | Modell-ellenőrzés brief elején | ⬜ | — | marad | minden új brief fejlécébe |

**Új (#47–#55)** — részletek a 4. szakaszban; itt a fázis-besorolás:

| # | fázis | mire ül |
| --- | --- | --- |
| #47 TERV\_BEFOGAD | folyamat | dokumentum |
| #48 KAROLI\_ELLENORZES | 1. adatréteg | #22, DT-M2 |
| #49 STRONG\_NORMALIZAL | eszközök | N37, N21 |
| #50 SQLITE\_EPIT | eszközök | #49, SEMA 3. |
| #51 MCP\_BUROK | eszközök | #50, ATALAKITASI\_TERV 11.7, DT-M3 |
| #52 BDB\_ADATBLOKK | 1. adatréteg | #50, #38 |
| #53 JELOLTEK\_RETRO | 1. adatréteg | SEMA 2.4, F3/N14 |
| #54 OLVASOI\_KONKORDANCIA (= #25a) | 2. render | #50, #44, DT-M1, DT-M6 |
| #55 SZPA\_AUDIT | folyamat | SZPA-profil |

**Kész feladatok, amelyekre a terv épít, de a briefjüket nem látta:** #21 (pilot), #8 (LXX-döntések), #5/#6 (szótár S1), #14, #28, #33, #34, #35, #16/#17, #19 (KJV teljes), #24 (licenc-leltár), #41 (versszámozás) ? — állapotuk a FELADATOK „Kész" szakaszából, a #47 veszi át.

**Összesítve:** 21 nyitott régi feladat — 3 módosul (#38, #25, #11 kicsit), 5 bemenet (#22, #43, #44, #37, #42), 13 marad érintetlenül; 9 új. Egyetlen régi feladat sem szűnik meg.

## 5. Hullámok és megállási pontok

A feladatok négy hullámban futnak; egy hullámon belül párhuzamosíthatók (külön session, külön ág). A ⛔ a felhasználói megállás, ahol a következő hullám nem indul.

| hullám | feladatok | miért együtt | ⛔ a végén |
| --- | --- | --- | --- |
| 1 | 0. lépcső; #47; #49; #53; #55 | egyik sem függ a másiktól, és egyik sem igényel új adatot; a #53 az első teljes lelet-lap-adat, a #55 azonnal mérhető hozam | DT-M1–M3 eldöntve; a #43/#44 kézi fájlok bent; `/kovetkezo` elindítja a #43-at és #44-et |
| 2 | #48; #50 | a #48 a #22 kész könyveire fut, a #50 a #49-re épül; a két brief független | a #50 integritási tesztje 0 sértés; a #48 eltéréslistája átnézve, a triplet-frissítés PR-je befogadva |
| 3 | #51; #52 | mindkettő a `pardes.db`-n ül; a #52 a #38 javító menetét készíti elő, a #51 a kutatást | a #51 eszközteszt egyezik a CLI-vel; a #38 6. adagja a #52 adatblokkjával indul (DT-F38i) |
| 4 | #54 | az első publikus kiadás; csak a hosting-döntés és a DT-M6 után | hosting ⛔; licenc-szűrő átnézve; első 40 lap jóváhagyva → publikálás |
| után | #23 → #9/#10 → #11 → #25b | a motívum-réteg a kész konkordanciára ül | a FELADATOK meglévő megállásai (A4/B5) |

Közben folyamatosan: **#22** könyvenként (Józsué következik) és **#38** adagonként — a 2. hullámtól a #48 minden új Károli–Strong könyvre újrafuttatható, a 3. hullámtól a #38 adagjai a #52 blokkjával mennek.

```
1. hullám  ─▶  2. hullám  ─▶  3. hullám  ─▶  4. hullám  ─▶  #23 → #9/#10 → #11 → #25b
0. lépcső      #48            #51            #54
#47 #49        #50            #52
#53 #55
     ⛔ DT-M1–3     ⛔ 0 sértés     ⛔ DT-F38i     ⛔ hosting, DT-M6
```

## 6. Kockázatok és mérőszámok

| kockázat | hol üt | kezelés |
| --- | --- | --- |
| versszámozás (N17, N46, N-F41a/d): a vers-lap rossz verset köt össze | #50, #54 | KK-alapú kulcs, `szamozas` jelző, interpoláció nélkül; a kis minta 20 verse közül 5 ismert eltolódásos (zsoltárfelirat, Jób 40–41) |
| a Károli–Strong `alacsony` linkjei az ellenőrzésben zajt adnak | #48 | csak `magas` link számít egyezésnek; az `alacsony` eltérés külön listán |
| a `jeloltek` retro-feltöltése a naplók szabad szövegéből kézi ítéletet kíván | #53 | motívumonként ⛔; a `nyitva` státusz megengedett, a `beépítve` csak napló-szöveggel |
| STEPBible-származék kikerül a publikus nézetbe | #54 | `licenc_allapot` minden táblán, a lekérdező szűr; teszt: egy TAHOT-oszlop sem jelenik meg a kimenetben |
| az MCP eszközdefiníciói kontextust fogyasztanak | #51 | ≤ 8 eszköz (ATALAKITASI\_TERV 11.7); mérés az eszközteszt-naplóban |
| a #38 adagjai a #52 nélkül folytatódnak, és a Károli-oszlop utólag hiányzik | #52 | a 6. adag csak a #52 blokkjával indul (DT-F38i); a kész 5 adag a javító menetben kapja meg |
| a CC BY-SA (SDBH/Louw–Nida) blokkok ShareAlike-feltétele | #54 | a szó-lap 4/5/9. szerepe csak azonos licencű kiadásban; a licenc-szűrő külön értéke |

**Mérőszámok** (a naplókban rögzítve, nem a chatben):

- \#48: eltérések száma / vizsgált sor; triplet-frissített sorok száma
- \#50: integritási sértések (cél: 0); `pardes.db` mérete (a hosting-döntés bemenete)
- \#51: eszközhívás vs. CLI egyezés (cél: 100% a mintán); auditsorok száma
- \#53: `jeloltek`-sorok száma motívumonként; „még nem vizsgált" (cél: 0 a 8 lexikonoldalas motívumon)
- \#54: a 26-ból futó pontok száma; a kimenetben STEPBible-származék (cél: 0)
- \#55: tiltólistás szó / 1000 szó a tanulmányokban és a BDB-fordításban

## 7. Döntésnapló

| dátum | döntés / változás | státusz |
| --- | --- | --- |
| 2026-10-03 | v1: munkaterv az ADATVAGYON\_TERV 21–22. szakaszából — hat DT-előfeltétel, 0. lépcső, kilenc javasolt feladat (#47–#55), négy hullám, kockázatok és mérőszámok | tervezet |
| 2026-10-03 | A sorszámok (#47–#55) javaslatok; véglegesítés a FELADATOK.md-ben a felhasználó döntésével; dátumokat a felhasználó ad | megjegyzés |
| 2026-10-03 | DT-M1 (olvasói konkordancia a #25 előtt, #25 kettéválasztása #25a/#25b-re) a terv legnagyobb sorrend-módosítása | nyitott — felhasználói döntés |
| 2026-10-03 | v2: 4a. szakasz — a teljes projekt feladattérképe a FELADATOK.md v1.3 nyitott sorai alapján (21 régi: 3 módosul, 5 bemenet, 13 marad; 9 új); a „?” tételeket a #47 hitelesíti a repó ellen; az 1. szakaszban a meglévő briefek viszonya | kiegészítés |
