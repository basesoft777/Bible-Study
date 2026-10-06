# F52 TERV_SZINKRON — napló

A tervdokumentumok (`ADATVAGYON_TERV.md`, `MUNKATERV.md`, `VIBE_GUIDE.md`) szinkronjának futásnaplója. Minden futás egy szakasz; a legutóbbi szakasz `kiindulasi_allapot` sora a következő futás viszonyítási pontja (brief 4.1).

## 1. futás — 2026-10-04 (kis minta, majd teljes futás)

kiindulasi_allapot: FELADATOK v1.3, merge `8e8f771` (#171), 2026-10-04.

- **Viszonyítási pont a delta-listához:** `5b4fcf8` (2026-10-03, a tervdokumentumok utolsó döntésnapló-sorának napja; korábbi szinkron-napló nincs). A brief 5. pontja a `117bafc` merge-et nevezi; a futás a frissebb HEAD-merge-et vette, mert a #170/#171 (a tervdokumentumok befogadása, az F52 brief) azután került be — a `117bafc` óta a hat bemeneti fájl nem változott tartalmilag.
- **Kiváltó esemény:** DT-F33e–j (licenc), MUNKATERV DT-M6; felhasználói kérés.
- **Menet:** kis minta (felhasználói kérés: ADATVAGYON 0. szakasz 4. pont, 2. szakasz, 17.1 első sor; MUNKATERV 2. szakasz DT-M6) → jóváhagyva → a 16. delta-sorra felhasználói döntés (a MUNKATERV a FELADATOK számaihoz igazodik, DT-F52a) → teljes futás.
- **Ág:** `claude/f52-terv-szinkron` (az `origin/main`-ből, `8e8f771`).

### 1.1 Delta-lista és érintettség (brief 4.2–4.3)

Forrás: `git diff 5b4fcf8..8e8f771 -- FELADATOK.md DONTESEK.md NYITOTT_FELADATOK.md adat/SEMA.md CLAUDE.md MUNKAMENET.md`, kiegészítve a `naplok/ATNEZES_2026-10-04.md` átnézésével. „Érint" = a szakasz egy állítása a változás után hamis vagy hiányos lenne (brief 4.3).

| # | változás | forrás | érinti-e | szakasz | státusz |
| --- | --- | --- | --- | --- | --- |
| 1 | STEPBible-származék CC BY 4.0; a „do not redistribute" kérés, nem feltétel; az 1. út (böngészős SQLite) nem esik ki | DT-F33f | igen | ADATVAGYON 0.4; 17.1 1. sor | átvezetve (kis minta) |
| 2 | Károli 1908 közkincs, kiadói nyilatkozat nem kell; a #44 Károli-része tárgytalan | DT-F33e | igen | ADATVAGYON 0.4 | átvezetve (kis minta) |
| 3 | BDB, Thayer, Nave, SECE közkincs; SECE_G LN/GK nem a renderbe | DT-F33g, h, i | igen | ADATVAGYON 0.4 | átvezetve (kis minta) |
| 4 | két kimeneti mód (nem kereskedelmi / kereskedelmi), szűrés a `kereskedelmi` oszlop szerint | DT-F33j, N-F33b | igen | ADATVAGYON 0.4; 17.1 1. sor; MUNKATERV DT-M6 | átvezetve (kis minta) |
| 5 | a DT-M6 régi tartalma (STEPBible kizárása, `licenc_allapot` szűrő) hamis | DT-F33f, DT-F33j | igen | MUNKATERV 2. DT-M6 | átvezetve (kis minta) |
| 6 | a STEPBible-útra vonatkozó 2. szakasz | DT-F33f | nem | ADATVAGYON 2. | nem kellett: a repóbeli szöveg már a DT-F33f szerint áll |
| 7 | 17.1 2. sor: „21 tisztazatlan, 17 tisztazott, 1 kozkincs" | DT-F33c–j, `adat/licencek.tsv` | igen | ADATVAGYON 17.1 2. sor | átvezetve: 44 sor, 24/9/11; `kereskedelmi=nem` és `feltetelesen` felsorolva (proveniencia: 1.4) |
| 8 | „a bemeneti STEPBible-fájlok nem terjeszthetők (DT-F33a)" | DT-F33f, DT-F33j | igen | ADATVAGYON 0.2 alatti 2. pont; 0.2 Károli–Strong sor | átvezetve |
| 9 | „a STEPBible-származék nem terjeszthető… csak backend-út" | DT-F33f, DT-F33j | igen | MUNKATERV 1. szakasz 3. elv | átvezetve |
| 10 | a 2026-10-03 v5 és „nyitott" döntésnapló-sor a DT-F33a-ra hivatkozik | DT-F33f | igen | ADATVAGYON 19. döntésnapló | a v5 sor történeti, marad; a „nyitott" sor státusza lezárva (v14); új v14 sor |
| 11 | MUNKATERV 6. szakasz: „STEPBible-származék kerül a publikus nézetbe" kockázat, OLVASOI_KONKORDANCIA licencszűrő-mérőszám | DT-F33j, N-F33b | igen | MUNKATERV 6. | átvezetve: a kockázat és a mérőszám a két módra fogalmazva |
| 12 | #22 ▶ fut → ⛔ megállt (1–5Móz és Józs kész; a Józs PR merge-e és a következő könyv a felhasználóra vár) | FELADATOK #22 | igen | MUNKATERV 1., 4a, 5.; ADATVAGYON 16. állapotfrissítés | átvezetve |
| 13 | #43 ⬜ → ▶ fut; DT-F43: a bridge nem független forrás, csak tájékoztató | FELADATOK #43, DT-F43 | igen | MUNKATERV 1., 3., 4a, 5.; ADATVAGYON 15., 21. 0–1. lépcső | átvezetve |
| 14 | #44: a Károli-rész tárgytalan (DT-F33e); a 0. lépés fájljai bent | DT-F33e, `adat/kulso/` | igen | MUNKATERV 3., 4a; ADATVAGYON 15., 19., 21. | átvezetve |
| 15 | #46 ✅ (a merge `4e6f979` 2026-10-03-i, a viszonyítási pont előtti: nem tartomány-delta, a terv eleve elavult státusszal vette fel) | FELADATOK Kész lista | igen | MUNKATERV 1., 4a (#46, összesítés); ADATVAGYON 21. 1. lépcső | átvezetve; a #9/#36 függéséből kivéve (ellenőr 12.) |
| 16 | a javasolt #47–#55 sorszámok ütköznek a FELADATOK-kal (#47 ALLAPOT_ELLENTMONDASOK, #48 KJV_REGI_KIVEZETES, #49 FOLYTATAS, #50 CI_JAVITO_KOR, #51 KONZISZTENCIA, #52 TERV_SZINKRON) | FELADATOK | igen | MUNKATERV 1., 2., 3., 4., 4a, 5., 6.; VIBE 1., 5., 6., 7.; ADATVAGYON fejléc-tábla, javaslat 1./4. pont | ⛔ → **felhasználói döntés (DT-F52a):** a FELADATOK számaihoz igazodik; a tervezett feladatok kódnévvel, számot a `/befogad` ad; átvezetve |
| 17 | új FELADATOK-sorok: #48 KJV_REGI_KIVEZETES ⬜, #50 CI_JAVITO_KOR ⬜, #51 KONZISZTENCIA ⬜, #52 TERV_SZINKRON ▶; kész: #26, #32, #49 | FELADATOK | igen | MUNKATERV 4a (új sorok, kész lista, összesítés), 5. (folyamat-feladatok mondata) | átvezetve |
| 18 | D34–D41, DT-F26a (motívumcikk-név) | DONTESEK / FELADATOK | nem | — | az ADATVAGYON fejléc-táblája már rögzíti |
| 19 | az `ATNEZES_2026-10-04.md` „nincs brief fájl" sorai (F01, F05, F19, F22, F24, F38, F43, F44) tévesek; mind a nyolc brief megvan | `terv_atnezes.py` új futás | nem (a naplót érinti) | — | nem átvezetve; a `naplok/ATNEZES_*.md` cseréje külön döntés (1.3) |
| 20 | DT-F32a (#12 kettéválik: #12a próza-próba a #23 M0 és M1 között; #11 brief a #12a után), DT-F32b (értelmező modell Opus), DT-F32c | DONTESEK, MUNKAMENET | igen | ADATVAGYON 16. ábra (#23, #11); MUNKATERV 4a (#23, #11) | átvezetve; a fejléc-tábla #32-sora már rögzítette |
| 21 | FELADATOK függések: #9 +#23; #10 +#11; #11 → #9, #23; #23 → #32 ✅, #37*; #30 nélkül #32; #37 → #32 ✅; #36: #46 ✅ | FELADATOK | igen | ADATVAGYON 16. ábra; MUNKATERV 4a | átvezetve |
| 22 | a három kézi 0. lépés fájlja bent: `lxx_bridge.tsv` + `LICENC.md` (F43.0, `0a56427`), `karoli_bible_hu_LICENC.txt` (F44.0, `5d61f7a`), `openbible_crossrefs_LICENC.txt` (F44.1, `ba18cb7`); a tervdokumentumok a repóban (`ab73f7b`) | `adat/kulso/`, git log | igen | MUNKATERV 3. (0. lépcső pipák), 5. 1. hullám; ADATVAGYON 15., 19. teendők, 21. 0. lépcső | átvezetve; a fájlnév `.csv` → `.tsv` |
| 23 | SEMA 2.19: LSJ tisztázott (CC BY-SA 4.0); DT-F33e/f/g kivételek a 2. szabályban | adat/SEMA.md | igen | ADATVAGYON 17.1 2. sor (a 7. sorral együtt) | átvezetve |
| 24 | MUNKAMENET: Kontextus-őrzés szakasz (F32), ⛔-nál döntés-előkészítés a `DONTES_KERDES_SABLON.md` szerint | MUNKAMENET.md | nem | VIBE 6. „Határok" nem mond ellent; ADATVAGYON fejléc-táblája rögzíti | nem kellett |
| 25 | NYITOTT: N29 lezárva (ASV nem jön, D7); N-F33a, N-F33b új | NYITOTT_FELADATOK.md | igen | N-F33b: a 4. sorral átvezetve; N29: ADATVAGYON fejléc-tábla és a MUNKATERV új #48-sora | átvezetve |
| 26 | CLAUDE.md: D34 átmeneti sor, K1 csomagmód-sor | CLAUDE.md | nem | — | a fejléc-tábla (D34–D41, #32) rögzíti |
| 27 | TERV_BEFOGAD részben teljesült: a három dokumentum a repóban (`ab73f7b`); nyitott: a #23/#25 brief `olvas:` sora (csak az F52 brief hivatkozza az ADATVAGYON_TERV-et), ATALAKITASI_TERV 4.7 jelölése, CLAUDE.md KJV-sora | repó (grep, git) | igen | MUNKATERV 1., 3., 4., 4a, 5.; ADATVAGYON 19. teendők | átvezetve („részben kész") |
| 28 | DT-F26b (a #12 helye: a DT-F32a az irányadó, az F12 fejléce a main-állapotra, a #11 `fugg`-jából a 12 ki; D38 kiegészítve) | DONTESEK | igen | ADATVAGYON 16. ábra (#11 függ), MUNKATERV 4a #11 (a 20–21. sorral együtt átvezetve) | átvezetve |
| 29 | DT-F26c (az F10 `kovetkezo` mezőjébe vissza a #8 négy nyitott LXX-sorának előfeltétele) | DONTESEK | nem | a tervdokumentumok a #10 előfeltételét nem részletezik | nem kellett |

### 1.2 Átírt szakaszok (brief 4.7) — a `git diff` tételei

**ADATVAGYON_TERV.md**

| szakasz | egy mondat |
| --- | --- |
| kiindulási állapot sor (5. sor) | viszonyítási pont `8e8f771`, az F52 napló megnevezve; „a hamissá vált állítást a #52 cseréli (v14)" |
| fejléc-tábla, Sorszámok sor | a DT-F52a döntés: a MUNKATERV és a VIBE a FELADATOK számaihoz igazodik, a tervezett feladatok kódnévvel |
| fejléc-tábla, DT-F33f sor (9.) | (F52.5) a `pardes.db` terjeszthetőségét a források módja dönti el (DT-F33j) |
| fejléc-tábla, Státuszok sor (13.) | (F52.5) DT-F43 (a) eldöntve: a bridge tájékoztató réteg |
| „A sorrend a továbbiakban” mondat (25.) | (F52.5) a doc a repóba költözött (`ab73f7b`) |
| javaslat 1. és 4. pont | `#54` → OLVASOI_KONKORDANCIA |
| 0. szakasz 3. és 7. pont | (F52.5) #22: 1–5Móz és Józs kész, ⛔; a kézi 0. lépés kész |
| 0. szakasz 4. pont | (kis minta) DT-F33e–j: CC BY 4.0, két mód, `kereskedelmi` szűrő; (F52.5) MCGED a kereskedelmi kizárások közt |
| 0.2 Károli–Strong sor | a bemenet (TAHOT) is terjeszthető (DT-F33f) |
| 0.2 alatti 2. pont | a szétválasztás kereskedelmi/nem kereskedelmi (DT-F33j), nem STEPBible/saját |
| 15. bevezető, #43/#44 sorok, 1. pont | a 0. lépés fájljai bent; #43 fut; a Károli-rész tárgytalan (DT-F33e) |
| 16. ábra (5 sor), állapotfrissítés, dőlt frissítés-jelzés a törzsben | függések a FELADATOK szerint; #22 ⛔; (F52.5) a cím visszaállítva az eredetire, #46 ki a #9/#36 függéséből |
| 17.1 első sor | (kis minta) az 1. út nem esik ki, a hosting nyitott; (F52.5) a `pardes.db` terjeszthetősége a források módja szerint |
| 17.1 második sor | 44 sor: 24 tisztazott / 9 kozkincs / 11 tisztazatlan; `kereskedelmi` oszlop; (F52.5) proveniencia a cellában, (F52.6) `\|` escape |
| 17.2 ATALAKITASI\_TERV 4.7 sor; 18.4 hiányzó-adat tábla | (F52.5) #22: 1–5Móz és Józs kész, ⛔ |
| 19. teendők (3 sor + 1 új) | kézi 0. lépés pipálva; Károli licenc tárgytalan; export kész, az olvas-lista nyitott |
| 19. döntésnapló | a 2026-10-03 „nyitott" sor lezárva (v14); új v14 sor |
| 21. 0., 1., 3., 4. lépcső | 0. lépcső kész; #46 kész; `kereskedelmi` oszlop; hosting-út a mód szerint; (F52.5) a #44 a #42-re vár |

**MUNKATERV.md**

| szakasz | egy mondat |
| --- | --- |
| 1. (7., 13., 15. sor) | sorszám-szabály (DT-F52a); 3. elv a DT-F33f/j szerint; F22 ⛔, F43 fut, F46 kész, TERV_BEFOGAD nyitott része |
| 2. DT-M1–M5 | a feloldott feladat oszlopa és a DT-M1 függése kódnévvel (#48/#50/#51/#54 → kód) |
| 2. DT-M6 | (kis minta) a két mód és a `kereskedelmi` oszlop szerinti szűrés |
| 3. 0. lépcső | négy pipa (lxx_bridge, Károli, openbible, tervdokumentumok), az olvas-lista külön nyitott sor; tárhely-sor a DT-F33f/j szerint |
| 4. tábla | `#` oszlop `—`; TERV_BEFOGAD „részben kész"; SQLITE_EPIT `kereskedelmi` oszlop; OLVASOI_KONKORDANCIA hosting és elfogadás a mód szerint; záró mondat kódnevekkel; (F52.5) a kimeneti fájlnevek `naplok/F48_…`–`F55_…` → kódnév-alapú (`naplok/KAROLI_ELLENORZES_elteresek.tsv` stb.) |
| 4a | bevezető dátum; #22, #43, #44, #46, #23, #30, #9, #10, #11, #32, #37 sora; a #7, #13, #25, #36, #38, #40, #42 sor „kapcsolat" oszlopa (kódnév-csere); új #48, #50, #51, #52 sor; „Tervezett" cím és tábla kódnevekkel; kész lista (+#26, #32, #46, #49); összesítés újraszámolva |
| 5. | hullám-tábla kódnevekkel, 1. és 4. sor státusza; folyamat-feladatok mondata; #22 mondat; ábra újrarajzolva |
| 6. | licenc-kockázat és OLVASOI_KONKORDANCIA mérőszám a két módra; kódnevek |
| 7. | v3 sor |

**VIBE_GUIDE.md**

| szakasz | egy mondat |
| --- | --- |
| 1. (7. sor) | a kilenc tervezett feladat kódnévvel (DT-F52a) |
| 5. tábla | a név oszlop sorszám nélkül (9 sor) |
| 6., 7. (135., 159., 160. sor) | `#50`/`#54` → kódnév |
| 5. OLVASOI_KONKORDANCIA sor, 7. hibatábla licenc-sor (F52.7) | a STEPBible-kizárás helyett blokkonkénti forrásjelölés és `kereskedelmi` mód-szűrő (DT-F33f/j, N-F33b); felhasználói döntés |
| 8. (F52.7) | v3 sor |
| 8. | v2 sor |

**Egyéb fájlok (nem tervdokumentum)**

- `DONTESEK.md`: DT-F52a — a brief 6. pontja szerinti megállás tétele, a felhasználó chat-döntésének rögzítése (✅ alkalmazva).
- `F52_TERV_SZINKRON_BRIEF.md`: fejléc (`allapot: fut`, `ag`, `pr: 172`, `kovetkezo`, `ir` + DONTESEK.md és az ellenőr-napló), cím `F52`.
- ez a napló.

### 1.3 Nem átvezetett, kérdéses tételek (brief 4.7, 6. pont)

| tétel | miért nem | javaslat |
| --- | --- | --- |
| VIBE 5. szakasz OLVASOI_KONKORDANCIA sora és 7. hibatábla licenc-sora: „a licenc-szűrő STEPBible-származékot nem enged ki", „STEPBible-származék a kimenetben = 0" | a brief 6. pontja a VIBE 5. szakaszt a sorszám/név cseréig engedi; a DT-F33f/j után az állítás elavult | **eldöntve, átvezetve (F52.7):** a felhasználó 2026-10-04-én a chatben kérte az átírást; az új alak „blokk dataset-kulcs nélkül = 0; kereskedelmi módban `kereskedelmi=nem` forrásból jövő mező = 0" (DT-F33j, N-F33b), a MUNKATERV 6. szakaszával egyezően; VIBE döntésnapló v3 |
| TERV_BEFOGAD nyitott részei: a #23/#25 brief `olvas:` sora, ATALAKITASI_TERV 4.7 elavult-jelölés, CLAUDE.md KJV-sor („csak Genezis, Exodus, Példabeszédek") | nem a tervdokumentumok, hanem a TERV_BEFOGAD feladat tartalma (brief 8.) | a TERV_BEFOGAD befogadása vagy a #40/#51 jelzése |
| ADATVAGYON 21. 3. lépcső „`pardes.db` (nem commit)", MUNKATERV SQLITE_EPIT „`.gitignore`-ban" | generált fájl, méret és reprodukálhatóság kérdése, nem licenc; a DT-F33f nem fordítja meg | marad |
| `naplok/ATNEZES_2026-10-04.md` téves „nincs brief fájl" sorai (19. delta) | a napló nem tervdokumentum; a `terv_atnezes.py` új futása cserélné | külön döntés |
| a brief 5. pontjának `117bafc` hivatkozása | a kis minta a `8e8f771`-et vette (l. fent) | a brief 5. pontja történeti, marad |
| MUNKATERV 4. „az `ellenor` mindig Haiku vagy Sonnet" kontra FELADATOK D10 (`fuggetlen-ellenor` Opus) | nem delta (2026-10-03 előtti állapot), a brief 2. pontja szerint nem kiváltó | a következő szinkron vagy a MUNKATERV szerzője |

### 1.4 Proveniencia

- licenc-összesítés (17.1 2. sor): `scope=adat/licencek.tsv (44 adatsor, allapot × kereskedelmi) | forras=egyszeri számláló szkript a scratch-könyvtárban (nem repó-eszköz) | ts=2026-10-04`
- delta-lista: `scope=FELADATOK.md, DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, CLAUDE.md, MUNKAMENET.md | forras=git diff 5b4fcf8..8e8f771 | ts=2026-10-04`
- `adat/kulso/` fájlok és a tervdokumentumok bekerülése: `scope=adat/kulso/, ADATVAGYON_TERV.md | forras=git log (0a56427, 5d61f7a, ba18cb7, ab73f7b) | ts=2026-10-04`
- brief-fájlok létezése (19. delta): `scope=F*_BRIEF.md | forras=ls | ts=2026-10-04`

### 1.5 Elfogadási pontok (brief 7.)

| # | pont | állapot |
| --- | --- | --- |
| 1 | minden delta-sor a naplóban, igen/nem érintettséggel és indokkal | 29 sor, 1.1 (F52.5: DT-F26b/c felvéve, a 25. sor igen) |
| 2 | az átírt szakaszok listája és a `git diff` egyezik | 1.2; ellenőr 1. kör: ADATVAGYON, VIBE OK; MUNKATERV hiányai F52.5-ben pótolva |
| 3 | minden átírt állítás mellett a hivatkozott DT-/N-/#-tétel | DT-F33e–j, DT-F33a, DT-F43, DT-F32a, DT-F52a, N-F33b, N29/D7, FELADATOK-számok |
| 4 | nem maradt megfordított állítás (régi alak keresve) | „nem terjeszthet", „csak backend", „Józsué következik/jön", „merge-elve, kézi", „#47–#55" (döntésnaplón kívül): 0 találat; a VIBE két licenc-sora F52.7-ben átírva (1.3) |
| 5 | döntésnapló-sor és kiindulási állapot sor bent | ADATVAGYON v14 + kiindulási sor; MUNKATERV v3; VIBE v2 |
| 6 | a dokumentumok többi része bájtazonos | a cserék egyszeri, pontos illesztéssel; CRLF megőrizve; ellenőr 1. kör: OK (hunkon kívül bájtazonos, sorvég-váltás nincs) |

### 1.6 Ellenőr (brief 4.8) és javító kör

**1. kör** (`fuggetlen-ellenor`, 2026-10-04; jelentés: `naplok/ELLENOR_TERV_SZINKRON.md`, az ügynök fájlíró eszköz nélkül futott, a szöveget a hívó menet mentette): **JAVÍTANDÓ, 15 tétel.** Javítás F52.5-ben:

| # | ellenőr tétele | javítás |
| --- | --- | --- |
| 1 | CI E5: a 16. címsor átírása `TÖRLÉS-SZÁNDÉKOS` jelölés nélkül | a cím visszaállítva az eredetire; a frissítés jelzése egy dőlt sor a szakasz törzsében |
| 2 | hibás tömeges csere `BDB_ADATBLOKK TERV_SZINKRON` (MUNKATERV 4a bevezető) | `#52 TERV_SZINKRON` |
| 3 | DT-F43 (a) „nyitott" a fejléc-táblában | eldöntve: a bridge nem független forrás, tájékoztató réteg; a 26-os pont a DT23 szerint |
| 4 | #22 régi alak (0.3, 17.2 ATALAKITASI-sor, 18.4 tábla; MUNKATERV 4. tábla) | „1–5Móz és Józs kész", ⛔ |
| 5 | régi sorszám a kimeneti fájlnevekben (`naplok/F48_…`–`F55_…`) | kódnév-alapú nevek, a repó mintájára (`naplok/LXX_BRIDGE_naplo.md`) |
| 6 | „a `pardes.db` CC BY 4.0 alatt terjeszthető" — a DT-F33f nem mondja ki | a STEPBible-származék terjeszthető; az adatbázis terjeszthetőségét a benne lévő források módja dönti el (DT-F33j); a fejléc-tábla v13-sora ugyanígy |
| 7 | DT-F26b/c hiányzik a delta-listából; a #46 nem tartomány-delta; a 25. sor „részben" | 28–29. sor; a 15. sor átfogalmazva; 25. sor `igen` |
| 8 | az 1.2 lista hiányos (DT-M1–M5, 4a kapcsolat-oszlopok) | kiegészítve |
| 9 | MCGED hiányzik a 0.4 kizárásai közül | felvéve (`kereskedelmi=nem`), hivatkozás DT-F33i, j, N-F33b |
| 10 | #46 dátuma 2026-10-04 helyett 2026-10-03 | javítva (MUNKATERV 1., 4a, kész lista) |
| 11 | „#44 indítható", de a #42-től (⬜) függ | „a #44 a #42-re vár" (ADATVAGYON 21., MUNKATERV 5.) |
| 12 | „#46 ✅/kész" a #9 és #36 függései között, a FELADATOK-ban nincs | kivéve (ADATVAGYON 16. ábra, MUNKATERV 4a #9) |
| 13 | 0. szakasz elavult állításai (kézi 0. lépés; „a doc a repóba költözik") | „kész", „költözött (`ab73f7b`)" |
| 14 | `DONTESEK.md` hiányzik a brief `ir:` listájából | felvéve (+ az ellenőr-napló) |
| 15 | a 17.1 2. sor számai mellett nincs proveniencia-sor | proveniencia a cellában |

**2. kör** (`fuggetlen-ellenor`, 2026-10-04, csak a 15 tétel és a CI; a jelentés a `naplok/ELLENOR_TERV_SZINKRON.md` 2. kör szakaszában): **14 tétel ELFOGADVA, CI exit 0; két új, a javítás által behozott eltérés**, javítva F52.6-ban:

| # | ellenőr tétele | javítás |
| --- | --- | --- |
| Ú1 | a 17.1 második sorának provenienciájában escape-eletlen `\|` jelek: a 3 oszlopos sor 5 cellára esett | `\|` a cellán belül; a `forras=` a tényleges lekérdezést nevezi (az `allapot` és `kereskedelmi` oszlop számlálása); gépi ellenőrzés: a sor 3 cellás |
| Ú2 | a napló 1.2 ADATVAGYON-listája nem követte az F52.5-öt (16. cím mint tétel; a 13., 25., 33., 37., 776., 851. sor hunkja hiányzott) | a lista kiegészítve, a „16. cím” tétel javítva |
| — | a delta-lista 28–29. sora a 27. elé került | sorrend javítva |

Az ellenőr „NEM ELLENŐRIZHETŐ" jelzése (a kis minta chatbeli jóváhagyása) és a DT-F52a „Felhasználó, chat" idézete: a döntés a chatben született, a repóban a DONTESEK-tétel és ez a napló rögzíti; más nyoma nincs.

## 2. futás — 2026-10-06

kiindulasi_allapot: FELADATOK v1.3 (a generált blokkok 2026-10-06-i állapota), `main` `7dd0183` (a #218 merge-e `a25c7a0` után; az ág eredetileg a `69da794`-ről indult, a futás közben mergelt #56 miatt rebase-elve), 2026-10-06.

- **Viszonyítási pont a delta-listához:** az 1. futás merge-e, `de9c464` (PR #172, 2026-10-04 21:57 +0200; a napló 1. futás szakaszának kiindulása a `8e8f771` volt). `git log de9c464..origin/main` (a `--since=2026-10-04T19:57` helyi időként értelmezve néhány 1. futásbeli commitot is behozna): 215 commit a `69da794`-ig (köztük a gépi „FELADATOK.md frissítés” sorok); a tervdokumentumokat azóta csak a `2e439f6` (DT-M8, MUNKATERV függések) és a `9d9d685` (F52.8, a napló nyitott tétele) érintette.
- **Kiváltó esemény (brief 2.):** (1) új DT-tételek, amelyek a MUNKATERV/ADATVAGYON állításait módosítják (DT-M1, M2, M3, M7, M8; DT-F42d/g; DT31–34); (2) a MUNKATERV feladatainak állapotváltozása és a tervezett feladatok számot kapása; (3) a DT-M8 kifejezett utasítása („a következő futás — kiváltó esemény: a felhasználó kéri — elvégzi az (a), (b), (c) pontot”; előfeltétele, a #52 PR #172 merge-e, teljesült); (4) felhasználói kérés. **Nem** kiváltó: a `#23` M0 jelentése (a #23 `nem_indult`, nincs `naplok/F23_M0_*.md`); a `#51` CI-jelzése (az E25 `dontes_hatas.tsv`-ben a három tervdokumentumra nincs sor; a `naplok/konzisztencia/KONZISZTENCIA_20261005.md` a MUNKATERV-et csak a DT-M névtér miatt említi, ütközést nem talált); MUNKATERV-hullám lezárása (az 1. hullám #62, #63 ⬜).
- **Ág:** `claude/f52-terv-szinkron-2` (az `origin/main`-ből, `69da794`; külön worktree).
- **⛔ vizsgálat (brief 6.):** a MUNKATERV sorrendjét és hullámait módosító döntések (DT-M1, DT-M7) és a DT-M8 átvezetési utasításai a felhasználó kifejezett, a chatben hozott és a `main`-re mergelt döntései; a #52-nek címzett átvezetés (DT-M7, DT-M8 „Alkalmazás” sora). Alapfeltevést fordító, még el nem döntött változás nincs; ezért a 4. pont előtt nem álltam meg. Két forrás közti **ellentmondás** nincs; egy szabály-szintű feszültség van (2.3 / 1. tétel: a brief 6. pontja a VIBE 5. szakaszát csak a sorszámok és nevek cseréjéig engedi, a DT-M3 viszont a VIBE `lepes=MCP` állítását elavulttá teszi) — ezt nem döntöttem el, hanem jelzem.

### 2.1 Delta-lista és érintettség (brief 4.2–4.3)

Forrás: `git diff de9c464..origin/main -- FELADATOK.md DONTESEK.md NYITOTT_FELADATOK.md adat/SEMA.md CLAUDE.md MUNKAMENET.md BRIEF_SABLON.md`, a `git log` és a brief-fejlécek (`F*_BRIEF.md`) átnézésével. „Érint” = a szakasz egy állítása a változás után hamis vagy hiányos lenne (brief 4.3).

| # | változás | forrás | érinti-e | szakasz | státusz |
| --- | --- | --- | --- | --- | --- |
| 1 | DT-M1 🟢: az olvasói konkordancia a #25 előtt; a #25 kettéválik (#25a = OLVASOI_KONKORDANCIA, #25b motívumos nézet); a kettéválasztás külön `/befogad`, még nem történt meg | DONTESEK DT-M1 (PR #214) | igen | MUNKATERV 1., 2., 3. (0. lépcső), 4 (OLVASOI sor), 4a (#25, tervezett tábla), 5, 7; ADATVAGYON 0.2 (3., 4., 5.), 16. (ábra, 1. pont), 21. (4–5. lépcső, 1. szabály) | átvezetve |
| 2 | DT-M2 🟢: új `AZONOSITAS_MODJA` érték `szó-szintű-gépi` (a terv `szó-szintű-tagged` javaslata helyett) | DONTESEK DT-M2 | igen | MUNKATERV 2., 4 (KAROLI sor); ADATVAGYON 22.2 | átvezetve |
| 3 | DT-M3 🟢: `auditok.lepes` = a kutatási lépés kódja, lépésen kívül `adhoc`, a csatorna a proveniencia-sorba (a terv `MCP` javaslata helyett); alkalmazás: #61 | DONTESEK DT-M3 | igen | MUNKATERV 2., 4 (MCP sor); ADATVAGYON 22.4, 9. | átvezetve; a VIBE `lepes=MCP` sora → 2.3/1. |
| 4 | DT-M7 🟢: az MCP_BUROK feltételes, kikerül a 3. hullámból; előbb a #61; a 9. szakasz „további előnyei” újraértékelve | DONTESEK DT-M7 („a TERV_SZINKRON vezeti át”) | igen | MUNKATERV 2., 4, 4a, 5 (3. hullám, ábra); ADATVAGYON 0. (2., 7.), 9., 19., 21. (3. lépcső) | átvezetve |
| 5 | DT-M8 🟢: a TERV_BEFOGAD külön brief nélkül; (a) 3. szakasz pipa, (b) ATALAKITASI_TERV 4.7 jelölés, (c) CLAUDE.md KJV-sor, (d) a #11 briefjébe | DONTESEK DT-M8 | igen | MUNKATERV 1., 2., 3., 4, 4a, 5; ADATVAGYON 0. (8.), 17.2, 18.1, 19.; **ATALAKITASI_TERV.md.md 4.7; CLAUDE.md „Adat-tár”** (a #52 `ir` listája DT-M8 szerint bővül) | átvezetve; a (d) a #11 befogadására vár |
| 6 | DT-M4, DT-M5, DT-M6 továbbra is 🟡 nyitott | DONTESEK | igen (jelölés) | MUNKATERV 2. (🟡 jelölések, DT-M7/M8 sor), 3. | átvezetve (tartalmi változás nincs) |
| 7 | DT2 🟢: a #10 mércéje L1, L3–L6 + rés-feltétel; N18/N19 nem blokkol | DONTESEK DT2 (PR #213) | igen | MUNKATERV 4a (#10 sor); az ADATVAGYON nem említi az L-feltételeket | átvezetve |
| 8 | DT40 ✅ → új feladat #66 BDB_ARAM_POTLAS (külön tábla; a #38/#56/#60 nem függ tőle) | DONTESEK DT40; FELADATOK #66 (PR #212) | igen | MUNKATERV 4a, 5 (önálló feladatok); ADATVAGYON 2. futás sor (v15) | átvezetve |
| 9 | DT-F41a 🟢: a Zsolt 13 kézi BSB→MT megfeleltetése | DONTESEK DT-F41a (PR #215) | nem | — | a #41 következő menetére vár; a versszámozás-kockázat (N-F41a/d) állítása nem fordul meg |
| 10 | DT-F21j, DT-F38d ✅ (állapotjavítás); lezárt briefek merge-sora, F22 cím (PR #216) | DONTESEK, F-briefek | nem | — | a tervdokumentumok nem hivatkoznak rájuk |
| 11 | #53 FELADATTERKEP lezárása (PR #217, `6078a41`); `FELADATTERKEP.html`/`feladatterkep.json` generált | FELADATOK #53 | igen (kicsi) | MUNKATERV 4a (kész lista); ADATVAGYON „Státuszok” sor | átvezetve |
| 12 | DT28 ✅: egyirányúság (szétválasztás, nem visszaírás); CLAUDE.md „Egyirányúság”; SEMA 3/9; BRIEF_SABLON `lexikon/` nem motívumfájl; F23 v1.3 | DONTESEK DT28; CLAUDE.md; adat/SEMA.md; BRIEF_SABLON.md | nem | — | a tervdokumentumok „visszaírása” az `adat/` TSV-kbe írást jelenti (14. szakasz), nem forrás-md-be; a 22.2 triplet-frissítés adat→adat |
| 13 | #30 ✅ SZAMOZAS: számkiosztás merge-kor (`szamkiosztas.py` + Action, E26); DT18 → DT29, DT30; az új DT-kat ágon helyőrzővel kell írni | FELADATOK #30; CLAUDE.md; BRIEF_SABLON | igen | MUNKATERV 4a (#30 sor) | átvezetve; a tervdokumentumok új DT-t helyőrzővel kapnak (DT-F52b…), végleges számot nem írok |
| 14 | #42 ✅ FORRASKIVEZETES + DT-F42a–j: licenc-címke egyetlen forrása `licencek.tsv` `cimke`; `KJV_Strongs_teljes` Strong-címkéi `tisztazatlan` (DT-F42d); `LXX_kivonat` kivezetve; `licencek.tsv` 46 sor | FELADATOK #42; DONTESEK; adat/SEMA.md 2.19; `adat/licencek.tsv` | igen | MUNKATERV 4a (#42 sor); ADATVAGYON 17.1 (licenc-összesítés) | átvezetve (számok: 2.4) |
| 15 | #43 ✅ (PR #167, 2026-10-04) | FELADATOK #43 | igen | MUNKATERV 1., 4a; ADATVAGYON 15., 16., „Státuszok” sor, 19., 21. | átvezetve |
| 16 | #44 ✅ + DT31–34: `karoli_bible_hu` elvetve, openbible 4 sor `hianyzik` + JELÖLT, az import külön feladat | FELADATOK #44 (PR #205); DONTESEK DT31–34 | igen | MUNKATERV 1., 3., 4 (OLVASOI sor), 4a; ADATVAGYON 15., 19., 21. | átvezetve; a bible-mcp kérdés (DT-M5) nyitott |
| 17 | #51 ✅ KONZISZTENCIA (E25, `/konzisztencia`, napi ütemezés) | FELADATOK #51 (PR #192) | igen | MUNKATERV 4a (#51 sor); ADATVAGYON „Státuszok” | átvezetve |
| 18 | #57 ✅ BDB_STRONG_POTLAS (alias-tábla; DT37–DT45) — a BDB-lánc első lépése (#57 → #56 → #38); a napló nyitott tétele (1. futás) | FELADATOK #57 (PR #209); naplók „Nyitott” tétel | igen | MUNKATERV 1., 4a (kész lista, szöveg) | átvezetve; a nyitott tétel lezárva |
| 19 | #58 ✅ MORF_KULCS (DT35, DT36; SEMA 2.22) | FELADATOK #58 (PR #208) | igen (kicsi) | MUNKATERV 4a (kész lista, #59 függése) | átvezetve |
| 20 | #22: a Józs PR mergelve; a következő könyv a Bírák (előbb versbeosztás-detektor és kézi jóváhagyás) | FELADATOK #22 | igen | MUNKATERV 1., 4a, 5; ADATVAGYON „Státuszok”, 16. (állapotfrissítés) | átvezetve |
| 21 | #38 ▶ fut: DT-F38i 🟢, a 6. adag a #56 adatblokkjával; az M0 5. pont a menet elején | FELADATOK #38; DONTESEK DT-F38i | igen | MUNKATERV 3., 4a, 5; ADATVAGYON 0. (6.), 13., 15., 17.1, 19., 21. | átvezetve |
| 22 | a tervezett feladatok számot kaptak: #56 BDB_ADATBLOKK (közvetlen TSV-változat, `fugg: []`), #62 STRONG_NORMALIZAL, #63 JELOLTEK_RETRO, #65 KAROLI_ELLENORZES (DT-F52a: számot a `/befogad` ad) | FELADATOK #56, #62, #63, #65 | igen | MUNKATERV 1., 4, 4a, 5; VIBE 1., 5.; ADATVAGYON „Státuszok”, 18.4 (N37) | átvezetve; a #56 az 1. hullámba (nem függ SQLITE_EPIT-től) |
| 23 | új feladatok a terven kívülről: #54 LXX_OS_LEFEDETTSEG, #55 ZSOLTAR_UJRAELLENORZES, #59 SZOSZEDET, #60 OLVASOI_PILOT, #61 LEKERDEZ_NAPLO, #64 TEREMT002_PROZA_PROBA (#12a), #66 | FELADATOK | igen | MUNKATERV 4a, 5; ADATVAGYON „2026-10-04 óta eldöntve” sor, v15 | átvezetve |
| 24 | FELADATOK-függések: #9 + #56*; #36 + #56*, #42/#37…; #40 nem függ #30-tól; #37 függése #30 ✅ | FELADATOK | igen | MUNKATERV 4a; ADATVAGYON 16. (ábra) | átvezetve |
| 25 | `DONTESEK.md`: DT-F42a–j, DT37–DT45 (#57), DT35–36 (#58), DT30 (#30), új számkiosztás | DONTESEK | nem (kivéve a fenti sorokban hivatkozottak) | — | a tervdokumentumok nem hivatkoznak a #57/#58 döntéseire |
| 26 | `NYITOTT_FELADATOK.md`: N9 lezárva (F42), N47, N-F53a–f, a Macula χ/ξ csere, a HODIT-001/#36 tétel | NYITOTT_FELADATOK | nem | — | N9: az ADATVAGYON a SEMA 2.19-re hivatkozik, az pontos; a #36 tétel a 4a #36 sorában (a #42 ✅ után renderel újra) |
| 27 | `adat/SEMA.md`: 2.19 `cimke`, 2.21 `dontes_hatas.tsv`, 2.22 morf-kulcs, 3/9 egyirányúság, `LXX_OS` útvonal | adat/SEMA.md | nem (az `AZONOSITAS_MODJA`/`lepes` 1.7/2.9 szövegét a DT-M2/M3 alkalmazása, nem a SEMA e futás előtti változása érinti) | — | a 22. szakasz az 1.7 és 2.9 elavultságát már kimondja; a SEMA módosítása külön feladat (#61, #65) |
| 28 | `MUNKAMENET.md`: nem változott | git diff | nem | — | VIBE a MUNKAMENET szabályát nem érzi (brief 6.) |
| 29 | `BRIEF_SABLON.md`: `lexikon/` nem motívumfájl; DT-/N-helyőrző szabály | git diff | nem | — | a VIBE nem hivatkozik rá |
| 30 | `CLAUDE.md`: egyirányúság, helyőrző-szabály; KJV-sor (DT-M8 (c)) | CLAUDE.md | igen (csak a KJV-sor) | **CLAUDE.md „Adat-tár”** | átvezetve (5. sor) |
| 31 | a `#23` M0 jelentése; MUNKATERV-hullám lezárása | `naplok/F23_M0_*.md` (nincs); FELADATOK | nem | — | a #23 `nem_indult`; az 1. hullám #62/#63 ⬜ |
| 33 | #56 ✅ BDB_ADATBLOKK (PR #218, merge 2026-10-06; DT46–48 számkiosztás), a #38 függése `#56 (kész)`, a #9/#36 függéséből a `#56*` kikerült — az ellenőr szerint a futás közben történt, rebase után átvezetve | FELADATOK #56, #38, #9, #36 | igen | MUNKATERV 4a (#56, #38, #9, #36 sor, tervezett tábla), 5 (1. hullám sor); ADATVAGYON „Státuszok” sor, 16. (ábra) | átvezetve |
| 32 | `naplok/ATNEZES_2026-10-04.md` téves „nincs brief” sorai (1. futás 19. sor) | naplók | nem | — | változatlan, külön döntés |

### 2.2 Átírt szakaszok (brief 4.7) — a `git diff` tételei

**MUNKATERV.md**

| szakasz | egy mondat |
| --- | --- |
| 1. (3. bekezdés, 2. elv, „Viszony a meglévő briefekhez”) | a négy számot kapott feladat; az OLVASOI_KONKORDANCIA = #25a (DT-M1); TERV_BEFOGAD lezárva (DT-M8); F22/F42/F43/F44/F46 állapota; a BDB-lánc #57 → #56 → #38 |
| 2. (bevezető, DT-M1–M6 státuszjelölés, DT-M7, DT-M8 sor, záró mondat) | a döntések állapota (🟢/🟡), DT-M2 `szó-szintű-gépi`, DT-M3 `adhoc`, két új sor |
| 3. (0. lépcső három pipa) | a #23/#25 `olvas:` pipa kész (DT-M8 (a)); DT-M tételek állapota; a #38 6. adagja |
| 4. (feladatlista) | (DT-M5 megfogalmazása a 2. szakaszban: DT32) TERV_BEFOGAD lezárva; a számot kapott sorok `#` oszlopa (#65, #62, #56, #63, #25a); `szó-szintű-gépi`; MCP_BUROK feltételes és `adhoc`; BDB_ADATBLOKK függése; OLVASOI sor bemenete (`Karoli_1908`, nem `karoli_bible_hu`) és függése; záró mondat; DT-M5 megfogalmazás (DT32) |
| 4a. (teljes szakasz) | a nyitott sorok állapota, függése és a #25 kettéválása; új sorok: #54, #55, #56, #59, #60, #61, #62, #63, #64, #65, #66; #30, #42, #43, #44, #51 ✅; tervezett tábla; kész lista; összesítés újraszámolva |
| 5. (1–4. hullám sor, két bekezdés, ábra) | a #56 az 1. hullámba; az MCP_BUROK a 3. hullámban feltételes; #65, #25a; önálló feladatok; az ábra |
| 7. | v4 sor |

**ADATVAGYON_TERV.md**

| szakasz | egy mondat |
| --- | --- |
| kiindulási állapot sor (5. sor), „Státuszok” sor + új sor (13–14. sor) | a 2. futás viszonyítási pontja; a mai státuszok; a 2026-10-04 óta eldöntött tételek |
| 0. (2., 6., 7., 8. pont; 0.2 3., 4., 5. pont) | MCP feltételes; #56; az `olvas:` teendők kész; #25a |
| 9. (bevezető állapot-bekezdés, „További előnyök”) | DT-M7: az MCP feltételes; a tényleges többlet és a nem MCP-előnyök |
| 13. (záró bekezdés) | a #38 nem áll meg, a 6. adag a #56-tal |
| 15. (két sor a táblában, „Nyitott kérdés”, 1. pont) | #43/#44 ✅, `karoli_bible_hu` elvetve (DT31), a #38 M0 5. pont |
| 16. (ábra, frissítés-jelzés, 1. pont, állapotfrissítés) | #25a/#25b, #56* függés, DT-M1, a #22 és a #38 állapota |
| 17.1 (licenc-összesítés, DT-F38e/i sor), 17.2 (CLAUDE.md-elavultság) | 46 sor 26/8/12; DT-F38i 🟢; a CLAUDE.md KJV-sora javítva |
| 18.1 (ATALAKITASI 4.7 sor), 18.4 (N37 sor) | az ATALAKITASI_TERV 4.7 jelölve; N37 → #62 |
| 19. (nyolc teendő-sor, v15 döntésnapló-sor, a 2026-10-03-i „karoli_bible_hu” sor lezárása) | #65, #63, MCP feltételes, openbible, #43/#44 pipa, #38 M0 5. pont, `olvas:` és 4.7 pipa |
| 21. (0–5. lépcső sorai, 1. szabály) | #43/#44 kész; #56/#62/#65; MCP feltételes; #25a/#25b |
| 22.2, 22.4 | DT-M2 `szó-szintű-gépi`; DT-M3 `adhoc` |

**VIBE_GUIDE.md**

| szakasz | egy mondat |
| --- | --- |
| 1. (7. sor) | a számot kapott feladatok és az OLVASOI_KONKORDANCIA = #25a |
| 5. (a feladatonkénti tábla hét sorának neve) | #65, #62, #56, #63, TERV_BEFOGAD lezárva, MCP_BUROK feltételes, OLVASOI_KONKORDANCIA (= #25a) |
| 8. (v4 sor) | a változás és a nem átvezetett `lepes=MCP` jelzése |

**Egyéb fájlok (DT-M8 szerint a #52 hatóköre)**

- `ATALAKITASI_TERV.md.md`: a 4.7 pont elé egy „Elavult” jelölő sor (DT-M8 (b)).
- `CLAUDE.md`: az „Adat-tár” szakasz KJV-sora (DT-M8 (c)).
- `F52_TERV_SZINKRON_BRIEF.md`: fejléc (`ag`, `pr: 219`, `kovetkezo`, `ir` + `ATALAKITASI_TERV.md.md`, `CLAUDE.md`).
- ez a napló.

### 2.3 Nem átvezetett, kérdéses tételek (brief 4.7, 6. pont)

| # | tétel | miért nem | javaslat |
| --- | --- | --- | --- |
| 1 | VIBE 5. szakasz MCP_BUROK sora: „minden hívás auditok-sort ír `lepes=MCP`-vel” | a DT-M3 szerint elavult (a `lepes` a kutatási lépés kódja vagy `adhoc`); a brief 6. pontja a VIBE 5. szakaszát csak a sorszámok és nevek cseréjéig engedi, a DT-M7 a MUNKATERV-et és az ADATVAGYON-t nevezi meg átvezetendőnek | a felhasználó döntsön (mint az 1. futás 2 licenc-sora): a sor átírása („`lepes` a kutatási lépés kódja vagy `adhoc`, `csatorna=mcp`”) engedélyezett-e; vagy marad, mert az MCP_BUROK feltételes |
| 2 | a #25 csonk tényleges kettéválasztása és a #25a befogadása | a DT-M1 szerint külön `/befogad` menet; a #52 nem vesz fel feladatot | `/befogad`: #25a OLVASOI_KONKORDANCIA (függ SQLITE_EPIT), a #25 csonk szűkítése |
| 3 | DT-M4, DT-M5, DT-M6 nyitott | a felhasználóé; a DT-M6 és a hosting az OLVASOI_KONKORDANCIA briefje előtt | döntés a #25a befogadása előtt |
| 4 | a DT-M8 (d): a #11 briefjének `olvas:` sora | a #11 csonk, a valódi brief a #12a után; nem a tervdokumentum | a #11 csonk-kitöltésekor |
| 5 | a MUNKATERV 4. szakasz bevezetőjének „az `ellenor` mindig Haiku vagy Sonnet” mondata kontra FELADATOK D10 (`fuggetlen-ellenor` Opus) | nem delta (az 1. futás 1.3 szakasza már jelezte); nem érint változást e futásban | a MUNKATERV szerzője vagy külön döntés |
| 6 | a SQLITE_EPIT és az MCP_BUROK, SZPA_AUDIT még számtalan; nincs a FELADATOK-ban | a `/befogad` dolga | `/befogad` a megfelelő időben |
| 7 | a MUNKATERV 4. szakaszának „kimenet”/„bemenet” cellái a brief-ek tényleges `ir`/`olvas` listájával nincsenek egyeztetve (#56, #62, #63, #65) | a #52 hatóköre a státusz/függés/sorszám; a tartalom a briefeké (brief 1. „nem újraírás”) | a következő futás, ha egy brief tartalma eltér |

### 2.4 Proveniencia

- licenc-összesítés (ADATVAGYON 17.1): `scope=adat/licencek.tsv (46 adatsor; allapot × kereskedelmi) | forras=egyszeri számláló szkript (split('\t'), nem a csv modul; a szkript a scratchpad-könyvtárban, nem repó-eszköz) | ts=2026-10-06`; eredmény: `allapot` — 26 tisztazott, 8 kozkincs, 12 tisztazatlan; `kereskedelmi` — 33 igen, 2 nem (MCGED, Heber_ETCBC_modulok), 1 feltetelesen (tW_szocikkek), 10 tisztazatlan.
- delta-lista: `scope=FELADATOK.md, DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, CLAUDE.md, MUNKAMENET.md, BRIEF_SABLON.md | forras=git diff de9c464..origin/main (69da794) | ts=2026-10-06`.
- brief-fejlécek (`fugg`, `nem_fugg`, `allapot`, `pr`): `scope=F22–F66_*_BRIEF.md | forras=Read/grep a fejlécekre | ts=2026-10-06`.
- DT státuszok: `scope=DONTESEK.md | forras=grep a DT-M1–M8, DT2, DT28, DT31–34, DT40, DT-F38i, DT-F41a, DT-F42a–j sorokra | ts=2026-10-06`.

### 2.5 Elfogadási pontok (brief 7.)

| # | pont | állapot |
| --- | --- | --- |
| 1 | minden delta-sor a naplóban, igen/nem érintettséggel és indokkal | 33 sor, 2.1 |
| 2 | az átírt szakaszok listája és a `git diff` egyezik | 2.2; a diff hunk-jai szakaszra bontva ellenőrizve (`git diff -U0`), az ellenőr lefuttatja |
| 3 | minden átírt állítás mellett a hivatkozott DT-/N-/#-tétel | DT-M1–M3, M7, M8, DT-F38i, DT-F42d/g, DT31–34, DT32, FELADATOK-számok, #52 |
| 4 | nem maradt megfordított állítás | keresve: `#43 fut`, `#42-re vár`, `részben kész`, `nyitott része`, `lepes=MCP`, `Józs PR merge-e`, `vagy TSV)`: 0 találat a MUNKATERV-ben és az ADATVAGYON-ban; a VIBE-ben a `lepes=MCP` marad (2.3/1., döntésre vár) |
| 5 | döntésnapló-sor és kiindulási állapot sor bent | ADATVAGYON v15 + kiindulási állapot sor; MUNKATERV v4; VIBE v4 |
| 6 | a dokumentum többi része bájtazonos | cserék pontos illesztéssel (`ed.py`: pontosan egy előfordulás, különben leáll), CRLF megőrizve |

## Nyitott a következő futásra

A futások között felgyűlt tételek, amelyeket a következő szinkron a delta-listájába vesz (brief 4.2). A TERV\_BEFOGAD maradéka (DT-M8 🟢) a 2. futásban elvégezve (a (d) pont a #11 befogadására vár).

| tétel | forrás | javaslat |
| --- | --- | --- |
| *(lezárva, 2. futás)* a MUNKATERV a #57 BDB\_STRONG\_POTLAS-t nem tartalmazta | az 1. futás nyitott tétele | a #57 ✅ (PR #209), a 4a térkép kész listájába és a BDB-lánc mondatába (#57 → #56 → #38) átvezetve |
| a VIBE 5. szakasz MCP\_BUROK sorának `lepes=MCP` állítása elavult (DT-M3) | a 2. futás 2.3/1. | felhasználói döntés: átírható-e a brief 6. pontja ellenére |
| a #25 csonk kettéválasztása és a #25a befogadása; DT-M4, M5, M6; a DT-M8 (d) | a 2. futás 2.3/2–4. | `/befogad`, ill. felhasználói döntés; a következő szinkron a döntések után |
