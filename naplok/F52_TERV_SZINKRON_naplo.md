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
| 13 | #30 ✅ SZAMOZAS: számkiosztás merge-kor (`szamkiosztas.py` + Action, E26); DT18 → DT29, DT30; az új DT-kat ágon helyőrzővel kell írni | FELADATOK #30; CLAUDE.md; BRIEF_SABLON | igen | MUNKATERV 4a (#30 sor) | átvezetve; a tervdokumentumok új DT-t helyőrzővel kapnak (DT49…), végleges számot nem írok |
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

## 3. futás — 2026-10-09

kiindulasi_allapot: FELADATOK v1.3 (a generált blokkok 2026-10-09-i állapota), `main` `1f420a7c` (a `78844919` = a #264 merge-e + a DT87–DT89 számkiosztás), 2026-10-09.

- **Viszonyítási pont a delta-listához:** a 2. futás kiindulása, `7dd0183` (2026-10-06; a 2. futás napló-szakasza). A TERV-INTEGRÁCIÓ menet (TI.10 `6b85561e`, TI.14 `e906be14`, 2026-10-08) azóta átvezette a DT74–DT78-at az ATALAKITASI_TERV-re (v10), a MUNKATERV-re (v5) és az ADATVAGYON_TERV-re (v16); a delta-listában ezek „átvezetve (TI.10)” jelölést kapnak, nem vezettem át újra. A tényleges munka a 2026-10-08 utáni delta és a TI által „a következő #52-futásra” hagyott táblák (MUNKATERV 4a).
- **Kiváltó esemény (brief 2.):** (1) a `/konzisztencia` KONZISZTENCIA_20261009 jelentése, 1.16 (a 6. számozott pont): ATALAKITASI 13.4 (#78, #23 sor) és MUNKATERV 158. sor (#22) elavult — gépi jelzés a driftre; (2) új DT-tételek, amelyek tervdokumentumot érintenek: DT79–DT86, DT-F51a–c (= DT87–DT89, ez utóbbiak az ATALAKITASI 10.-be már átvezetve — csak ellenőrizve); (3) lezárt feladatok: #77, #78, #82, #83, #84, valamint a #22 előrehaladása; (4) a #23 M1 jelentése befogadva (a M0-é a TI.10-ben átvezetve); (5) felhasználói kérés. **Nem** kiváltó: MUNKATERV-hullám lezárása (az 1. hullám #62, #63 ⬜).
- **Ág:** `claude/f52-terv-szinkron-3` (indulás: `2108fc67`).
- **⛔ vizsgálat (brief 6.):** alapfeltevést megfordító, még el nem döntött változás nincs; két forrás közti ellentmondás nincs (a FELADATOK `#52 ⬜` sora a brief `allapot: fut` fejlécével szemben a generált blokk késése, nem ellentmondás). Két tartalmi kérdést nem döntöttem el, hanem DONTESEK-tételbe tettem (3.3): DT-F52h (D23, `OT-full`), DT-F52i (VIBE „feltételes” jelzés). Egyik sem alapfeltevés, ezért a 4. pont előtt nem álltam meg.

### 3.1 Delta-lista és érintettség (brief 4.2–4.3)

Forrás: `git diff 7dd0183..HEAD -- FELADATOK.md DONTESEK.md NYITOTT_FELADATOK.md adat/SEMA.md CLAUDE.md MUNKAMENET.md BRIEF_SABLON.md`, a `git log`, a brief-fejlécek (`F*_BRIEF.md`) és a `.claude/konzisztencia/KONZISZTENCIA_20261009.md`. „Érint” = a szakasz egy állítása a változás után hamis vagy hiányos lenne (brief 4.3).

| # | változás | forrás | érinti-e | szakasz | státusz |
| --- | --- | --- | --- | --- | --- |
| 1 | DT74 (A): aranyminta és szótári rész, befagyasztás a #11 1. lépcsőjéig, a #9 szűkítése, a #10 mércéje L1–L7 + DT2 + váz | DONTESEK DT74 | igen | ATALAKITASI 13; MUNKATERV 4a (#9, #10, #36, #55, #70 sor); ADATVAGYON v16 | átvezetve (TI.10); a MUNKATERV 4a #10 sora `095a6e97` (KONZISZTENCIA 1.14); a 4a többi sora e futásban |
| 2 | DT75 (B): fázis- és függés-szabály (#62 `folyamat`→`1`, #76 `fazis: 1`, D51/D52) | DONTESEK DT75 | igen | MUNKATERV 4a fázis-besorolás | átvezetve (TI.10 a szabályt; e futás a 4a-t) |
| 3 | DT76 (C): DT-M4, DT-M5, DT-M6 🟢 | DONTESEK DT76 | igen | MUNKATERV 2., 3.; ADATVAGYON 0.4, 18.5 | átvezetve (TI.10); e futás: MUNKATERV 2. dátumjelölés, 4. #76 sor |
| 4 | DT77 (D): SQLITE_EPIT = #79, SZPA_AUDIT feltételes, openbible-import a #76-ban, #80, #81 | DONTESEK DT77 | igen | MUNKATERV 1., 4., 4a, 5.; ADATVAGYON 16., 19., 21.; VIBE 1., 5. | átvezetve (TI.10 a 4. táblát és az ADATVAGYON v16 sort); e futás: a megmaradt kódnevek számra cserélve, SZPA_AUDIT az 1. hullámból ki |
| 5 | DT78 (E): #52 hatóköre, terv → feladat irány (19)–(20), D16 CCR elavult, kritikus út, arany-készlet | DONTESEK DT78 | igen | ATALAKITASI 13, 10. D16; FELADATOK kézi szakaszai | átvezetve (TI.9, TI.10); e futás: 3b (3.3) |
| 6 | #78 SZEREPMATRIX_VAZ ✅ (PR #254, #256); DT80 (üres blokk jelölése), DT81 (szűkített hatókör), DT82 (három tartalmi eltérés), DT83 (héber 1. szerep forrása) | FELADATOK #78, F78 brief, DONTESEK DT80–DT83 | igen | ATALAKITASI 13.3, 13.4; MUNKATERV 4a (#78 sor, #9, #23 függés); ADATVAGYON „Státuszok”, 18.5 | átvezetve |
| 7 | `ÜRES-BLOKK` / `ÜRES-NYELV` jelölő és az „adatosítva, nincs bekötve” harmadik állapot (DT80, DT82 (a), DT83) | DONTESEK DT80, DT82, DT83 | igen | ATALAKITASI 13.3 (állapot-leképezés); ADATVAGYON 18.5 (Igazítás, 2. pont) | átvezetve |
| 8 | `adat/szotar_szerepek.tsv`: 26 sor, a 13. és 14. szerep `javaslat` állapotban (F78.3); SEMA 2.13 | adat/szotar_szerepek.tsv, adat/SEMA.md | igen | ADATVAGYON 18.5 (bevezető „11 szerep”, a 13. szerep felvétele), v16 | átvezetve |
| 9 | #23 M0 ✅ (PR #243, DT66) és M1 kész (PR #258): forrássablon-tervezet, SEMA 3.10, CI-terv (E28, E29), pilot-terv; DT84 🟡 a felhasználóra vár | FELADATOK #23, F23 brief, DONTESEK DT66, DT84 | igen | ATALAKITASI 13.4; MUNKATERV 4a (#23); ADATVAGYON 16. | átvezetve (M0: TI.10; M1 és DT84: e futás). Az ADATVAGYON 22. a SEMA 3.10-et nem idézi, a „motívum-séma a #23 után” állítás (22.3, 16. 2. pont) nem hamis → nem érint |
| 10 | #64 ✅ (PR #247): a #12a lezárult; DT68 (a próza helye, mérce L1–L7), DT69 | FELADATOK #64, DONTESEK DT68, DT69 | igen | MUNKATERV 4a (#12, #11 sor, kész lista); ADATVAGYON 16. | átvezetve (DT68 (2) a TI.10-ben; e futás a 4a-t) |
| 11 | #82 TERV_FELADAT_OR ✅ (PR #250): gépi terv → feladat őr, `TERVELEM-MUTATO` jelölőpár; DT79 | FELADATOK #82, DONTESEK DT79 | igen (kicsi) | ATALAKITASI 13.4 (a leírás a TI.10-ben előre bent); MUNKATERV 4. jelölőpár | átvezetve (bent); az őr (`feladatok.py ellenoriz`) 0 hiba |
| 12 | #77 API_VAKPROBA ✅ (PR #249): a #22 hátralévő könyvei API-n (Batch), `high`; DT73; DT70 (nincs 22.6 szúrópróba), DT71 (10 verses prófétai köteg), DT72 (futásnapló-átcímkézés) | FELADATOK #77, DONTESEK DT70–DT73 | igen (kicsi) | MUNKATERV 4a (#22 sor, kész lista), 5.; ADATVAGYON 16. | átvezetve; a költségmérés a D16-ban már átvezetve (TI.10) |
| 13 | #22: kész Zsolt (PR #239), Ézs és Jer (PR #249), 1Krón (PR #253), 2Krón (PR #255), Ezsd és Ez (PR #259); hátra a Jób és a Péld; DT54, DT57, DT58–DT60 | FELADATOK #22, F22 brief, DONTESEK DT54, DT57–DT60 | igen | ATALAKITASI 4.7 jelölés; MUNKATERV 1., 4a, 5.; ADATVAGYON 0.3, 13. (Státuszok), 16., 18.1, 19. | átvezetve (KONZISZTENCIA 1.16, 3. pont) |
| 14 | #83 JOB_VERSBEOSZTAS ✅ (PR #260): Jób 38–42 megfeleltetés, kézi tábla 19 sor; DT85 | FELADATOK #83, DONTESEK DT85 | igen | MUNKATERV 4a (#22 sor: a Jób előfeltételei) | átvezetve |
| 15 | #84 TAHOT_JOB41 ✅ (PR #262): a Jób 41 332 sora pótolva; DT86; N55 és N-F34b lezárva; a `CLAUDE.md` TAHOT-mondata a mért állapotra | FELADATOK #84, DONTESEK DT86, NYITOTT_FELADATOK, CLAUDE.md | igen | ADATVAGYON 17.2 (Adat-tár), 18.4 (N-F34b), 22.5; ATALAKITASI 10. N13 | átvezetve; a D23 (`OT-full`) újratárgyalása DT-F52h |
| 16 | #38: 6 adag kész (DT52), a 7. adag a `claude/f38-adag7` ágon; DT55 (#67 kapuja), DT56 (≥85% Károli-lefedettség), N53 | FELADATOK #38, DONTESEK DT52, DT55, DT56 | igen (kicsi) | MUNKATERV 4a (#38 sor); ADATVAGYON „Státuszok” | átvezetve |
| 17 | #37 ✅ (PR #240), #40 ✅ (PR #242), #66 ✅ (PR #227), #68 ✅ (PR #244), #71 ✅, #72 ✅ (PR #236), #73 ✅ | FELADATOK „Kész”, brief-fejlécek | igen (kicsi) | MUNKATERV 4a (Kész bekezdés, #37 sor); ADATVAGYON „Státuszok” | átvezetve |
| 18 | új briefek: #67, #69, #70, #74, #75, #76, #79, #80, #81 | FELADATOK, F67–F81 brief | igen | MUNKATERV 4a (sorok, összesítés) | átvezetve (a 4. tábla sorait a TI.10 felvette; a 4a e futásban) |
| 19 | ATALAKITASI 10. N1, N2, N5 lezárva (DT-F51a–c = DT87–DT89) | DONTESEK DT87–DT89; F51 `10ffd310` | igen | ATALAKITASI 10. | átvezetve (F51); az 888., 889., 892. sor ellenőrizve |
| 20 | KONZISZTENCIA_20261009 1.16: ATALAKITASI 13.4 #78/#23 sor, MUNKATERV #22 mondat | `.claude/konzisztencia/KONZISZTENCIA_20261009.md` | igen | ATALAKITASI 13.4; MUNKATERV 5. (158. sor) | átvezetve |
| 21 | KONZISZTENCIA 1.14: a #10 mércéje a MUNKATERV 4a-n L1–L7; új `dontes_hatas.tsv`-sor (DT74, MUNKATERV.md) | F51 `095a6e97` | igen | MUNKATERV 4a (#10 sor) | átvezetve (F51); a 4a újraírása a sort megtartotta |
| 22 | `adat/dontes_hatas.tsv`: sorok a MUNKATERV-re (DT74, DT76) és az ATALAKITASI-ra (DT78) — a MUNKATERV 4a #51 sora „ma nincs sor” állítása hamis lett | adat/dontes_hatas.tsv | igen (kicsi) | MUNKATERV 4a (#51 sor) | átvezetve |
| 23 | a #25 csonk kettéválasztva: #25a = #76 (befogadva), #25 = #25b | FELADATOK #25, #76 | igen | MUNKATERV 4a (#25 sor), 1. (a TI.10 mondata); ADATVAGYON 16. (ábra) | átvezetve |
| 24 | DT-M8 (d): a #11 csonk `olvas:` sorában az ADATVAGYON_TERV és a MUNKATERV bent van | F11 brief fejléce | igen | MUNKATERV 1., 2. (DT-M8 sor), 3., 4. (TERV_BEFOGAD sor); ADATVAGYON 0.8, 19. | átvezetve |
| 25 | DT49 (VIBE MCP_BUROK sor), DT50 (K5 worktree), DT51 (#66 M1), DT53 (#73), DT58–DT60 (#22 Zsolt), DT61–DT65 (#37, #40), DT67 (#68), DT69 (#64 LXX-állítások), DT2, DT6, DT-F41a | DONTESEK | nem (a DT49 a 2. futásban átvezetve; a többi: a tervdokumentumok nem hivatkoznak rájuk) | — | a DT52, DT54, DT56–DT57, DT66, DT68, DT70–DT73 a fenti sorokban |
| 26 | `NYITOTT_FELADATOK.md`: N-F78a, N-F72a, N48–N54, N-F83a (→ N55), N-F38c lezárva, N53 | NYITOTT_FELADATOK | nem (kivéve N-F34b, N55, N53 — a 13., 15. sorban) | — | a tervdokumentumok nem hivatkoznak rájuk |
| 27 | `adat/SEMA.md`: 2.13 (26 sor), 3.10 szintjelölés, 2.22; a 4. szakasz ma is „Jób 40:1-5 és a teljes Jób 41. fejezet hiányzik”-ot ír (SEMA :1229) | adat/SEMA.md | igen (forrás-ellentmondás a `CLAUDE.md` TAHOT-mondatával; a 2.13 a 8. sor) | ADATVAGYON 22.5 (SEMA 4. sor) | ⛔ jelezve a felhasználónak (orkesztrátor); a SEMA 4 javítása a #52 hatókörén kívül esik (3.3/11.); a 3.10-et az ADATVAGYON 22. nem idézi |
| 28 | `CLAUDE.md`: TAHOT-mondat (F84), E27 hivatkozás-szabály | CLAUDE.md | igen (csak a TAHOT-mondat) | ADATVAGYON 17.2, 22.5 | átvezetve (15. sor); az E27-szabály nem terv-tétel |
| 29 | `MUNKAMENET.md`: „bővített” törölve, a 4. szabály mércéje L1–L7 + DT2 | MUNKAMENET.md | nem | — | a VIBE nem hivatkozza; a MUNKATERV mércéje már L1–L7 |
| 30 | `BRIEF_SABLON.md`: `munka`-kivételek (F09 → `adat`) | BRIEF_SABLON.md | nem | — | a VIBE nem hivatkozza |
| 31 | MUNKATERV-hullám lezárása | FELADATOK | nem | — | az 1. hullám #62, #63 ⬜ |
| 32 | a `#51` CI-szabály jelzése a három dokumentumra | `dontes_hatas.tsv`, KONZISZTENCIA_20261009 | igen (a 20–22. sor) | — | gépi jelzés nem volt; a `/konzisztencia` 1.14, 1.16 tételei a 20–21. sor |
| 33 | terv → feladat gépi őr (`feladatok.py ellenoriz`) és a `/konzisztencia` 5. kategóriája | `feladatok.py ellenoriz`; KONZISZTENCIA 5.1–5.3 | igen | ATALAKITASI 10. N1, N2, N5 (19. sor); 3b | az őr 0 hibát jelez; 5.1–5.3 átvezetve (19. sor) |

### 3.2 Átírt szakaszok (brief 4.7) — a `git diff 2108fc67..HEAD` tételei

**ATALAKITASI_TERV.md.md** (v10 → v11)

| szakasz | egy mondat |
| --- | --- |
| fejléc (3–4. sor), „Státusz” sor | v11 sor és verziószám; a státuszsor a 13. szakasz v11-ére mutat |
| 4.7 (jelölő sor) | a #22 kész könyvei a mai állapotra (DT57) |
| 10. D23, N13 | N13 lezárva (N55, F84, DT86); a D23 újratárgyalása DT-F52h |
| 13. (cím), 13.3 | v11 jelölés; az üres-blokk állapotok a DT80/DT82/DT83 szerint; a #78 ✅, a #23 M1 kész, DT84 🟡 |
| 13.4 (táblasorok) | #78 lezárva; #23 M0/M1 kész; #9 a #23 után (a #78 kész) |

**MUNKATERV.md** (v5 → v6)

| szakasz | egy mondat |
| --- | --- |
| 1. (7. és 15. bekezdés) | a számot kapott feladatok (#79, #76); a #22 állapota; a #11 csonk `olvas:` sora (DT-M8 (d)) |
| 2. (bevezető, DT-M8 sor) | a döntések állapota 2026-10-08; DT-M8 (d) bent |
| 3. (0. lépcső, `olvas:` pipa) | a #11 csonk `olvas:` sora |
| 4. (TERV_BEFOGAD, #65, MCP_BUROK, #76 sor; a lánc mondata) | #79-re cserélt függések, a #65 kész könyvei és a `magas` pár korlátja, DT-M4/DT-M6 🟢; a #78 → #23 → #9 → #11 → #10 lánc |
| 4a. (teljes szakasz) | a nyitott sorok és függések a 2026-10-09-i FELADATOK szerint (33 sor), új sorok (#67, #69, #70, #74–#81), lezárt feladatok a Kész bekezdésben, összesítés újraszámolva, az „elavult” jelölés megszűnt |
| 5. (1., 2., 4., „után” hullámsor; két bekezdés; ábra) | SZPA_AUDIT ki az 1. hullámból (DT77 (13)); #79 és #76 számok; a #22 állapota; a lánc sorrendje |
| 7. | v6 sor |

**ADATVAGYON_TERV.md** (v16 → v17)

| szakasz | egy mondat |
| --- | --- |
| kiindulási állapot sor (5.), „Státuszok” sor (13.), új sor (16.) | viszonyítási pont `1f420a7c`, 2026-10-09; a mai státuszok; a 2026-10-09-i változások (DT73, DT79–DT89) |
| 0. (3. pont, 8. pont) | a #22 kész könyvei; DT-M8 (d) bent |
| 16. (ábra, frissítés-jelzés, állapotfrissítés) | a függések a FELADATOK szerint; #23 M1; #78 kész; #25a = #76 |
| 17.2 (Adat-tár sor), 18.1 (ATALAKITASI 4.7 sor), 18.4 (N-F34b sor) | a TAHOT fejezet-szinten teljes (F84); N-F34b lezárva; a #22 kész könyvei |
| 18.5 (bevezető, Igazítás 2. pont, 13. szerep) | 13 szerep × 2 nyelv; `ÜRES-BLOKK`/„adatosítva, nincs bekötve”; a 13. szerep felvéve (F78.3) |
| 19. (Károli–Strong sor; terminologia, tárhely, KK-kulcs, DT-M8 (d) teendő-jelölések) | a #22 állapota; négy teendő jelölve (#38 `olvas`, hosting ⛔, #79, #11 `olvas`) |
| 21. (5., 6. lépcső) | a lánc sorrendje; a 6. lépcső feltételes jelölése (3b) |
| 22.5 (TAHOT-sor) | fejezet-szinten teljes; maradó korlát a Jób 40 kulcsa |
| 19. döntésnapló (v17 sor) | a futás tételei |

**VIBE_GUIDE.md** (v4 → v5)

| szakasz | egy mondat |
| --- | --- |
| 1. (7. sor) | SQLITE_EPIT = #79, OLVASOI_KONKORDANCIA = #76 (= #25a) |
| 5. (a feladatonkénti tábla két sorának neve) | #79 SQLITE_EPIT, #76 OLVASOI_KONKORDANCIA |
| 8. (v5 sor) | a változás; a „feltételes” jelzés DT-F52i-re vár |

**Egyéb fájlok**

- `DONTESEK.md`: DT-F52h, DT-F52i (helyőrzők, 🟡).
- `F52_TERV_SZINKRON_BRIEF.md`: fejléc (`allapot`, `ag`, `kovetkezo`).
- ez a napló.

### 3.3 Nem átvezetett, kérdéses tételek (brief 4.7, 6. pont) és a terv → feladat rések (3b)

Minden rés pontosan egy kimenettel (átvezetés, DONTESEK-tétel, befogadási csonk-javaslat vagy ⛔). Csonk-javaslat (`beerkezo/TERV_SZINKRON_*.md`) ebben a futásban nem született: nincs olyan terv-elem, amelynek új feladat kellene.

| # | tétel | kimenet |
| --- | --- | --- |
| 1 | ATALAKITASI D23 („`scope=OT-full` nem adható ki”) indoka (a Jób 40:1-5 / Jób 41 hiánya) a #84-gyel megszűnt; az N13 szerint a tiltás újratárgyalható; a Jób 40 MT-kulcsa marad | DONTESEK **DT-F52h** (🟡); az ATALAKITASI D23 és N13 sora mutat rá |
| 2 | a VIBE 5. szakasz MCP_BUROK és SZPA_AUDIT sora a „kilenc tervezett feladat” része, de mindkettő feltételes (DT-M7, DT77 (13)); a brief 6. pontja a VIBE 5. szakaszát csak sorszám/név cseréig engedi | DONTESEK **DT-F52i** (🟡) |
| 3 | ADATVAGYON 21. 6. lépcső: „hasznosítás” (fordítói eszköz, licencelt adatkészlet, AI-réteg, kereskedelmi döntés jogásszal) — se feladat, se DT, se jelölés | átvezetés: „feltételes” jelölés (a 4–5. lépcső után, a felhasználó döntésére) |
| 4 | ADATVAGYON 19. teendők: `terminologia.tsv` a #38 adagjainak; tárhely-döntés; KK-kulcs/`szamozas`; DT-M8 (d) | átvezetés: jelölve (a #38 `olvas:` listája; ⛔ hosting a #76 briefje előtt; #79; a #11 csonk `olvas:` sora) |
| 5 | a #65 „csak `magas` link számít egyezésnek” (MUNKATERV 4., 6.) — a 3Móztól csak Sonnet fut, a linkek `alacsony` (DT-F22c, DT70), `magas` pár csak az 1–2Mózon | a #65 M0 ⛔-ja viszi (F65 `kovetkezo`, v1 sor, 2026-10-05); a MUNKATERV #65 sora a korlátot jelzi — új tétel nincs |
| 6 | DT84 🟡 (a #23 M1 13 `javaslat` pontja) | a felhasználóé; a #23 `kovetkezo`-ja és az ATALAKITASI 13.4 „DT84 🟡” jelölése mutat rá — új tétel nincs |
| 7 | a 2. futás 2.3/7.: a MUNKATERV 4. szakasz „kimenet”/„bemenet” cellái a brief-ek `ir`/`olvas` listájával nincsenek egyeztetve | nem rés: a tartalom a briefeké (brief 1. „nem újraírás”); a MUNKATERV a brief összefoglalója — nincs kimenet |
| 8 | a 2. futás nyitott tételei: VIBE `lepes=MCP` (DT49 ✅), #25 kettéválasztás (#76), DT-M4–M6 (DT76), DT-M8 (d) (bent), SQLITE_EPIT/SZPA számtalan (#79 / feltételes) | lezárva — l. „Nyitott a következő futásra” |
| 9 | KONZISZTENCIA 1.15 / N-F83a (a `CLAUDE.md` TAHOT-mondata) | lezárva az F84-ben (N55, CLAUDE.md); a 15. delta-sor |
| 10 | ATALAKITASI 11.2 „LEZÁRVA címke cseréje (az F3-ban végzendő)” | nem terv → feladat rés: az F3 lefutott, a háromértékű `statusz` a SEMA-ban bent van (TI.1 leltár „nem rés”); nincs kimenet |
| 11 | `adat/SEMA.md` 4. szakasz (:1229) „Jób 40:1-5 és a teljes Jób 41. fejezet hiányzik” ↔ `CLAUDE.md` „Adat-tár” (fejezet-szinten teljes, a Jób 41 pótolva, F84, DT86) — két forrás ellentmond (brief 6.) | ⛔ jelezve a felhasználónak (orkesztrátor); a SEMA 4 javítása a #52 hatókörén kívül esik (a SEMA nincs az `ir`-ben); az ADATVAGYON 22.5 „SEMA 4.” sora az ellentmondást jelzi, nem állítja a hiányt |

### 3.4 Proveniencia

- delta-lista: `scope=FELADATOK.md, DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, CLAUDE.md, MUNKAMENET.md, BRIEF_SABLON.md | forras=git diff 7dd0183..HEAD (HEAD: `1f420a7c` + F52.16) | ts=2026-10-09`.
- brief-fejlécek (`fazis`, `allapot`, `pr`, `fugg`): `scope=F22, F23, F37, F40, F64, F66–F70, F74–F84_*_BRIEF.md | forras=grep a fejlécekre | ts=2026-10-09`.
- nyitott FELADATOK-sorok száma: `scope=FELADATOK.md 1. fázis, 2. fázis, Folyamat és eszközök tábla (sorok, amelyek `| <szám>`-mal kezdődnek) | forras=egyszeri számláló szkript a scratchpadban (nem repó-eszköz) | ts=2026-10-09`; eredmény: 16 + 9 + 8 = 33.
- DT státuszok és szövegek: `scope=DONTESEK.md | forras=olvasás (DT57, DT70–DT73, DT79–DT89) | ts=2026-10-09`.
- `adat/szotar_szerepek.tsv` sorai: `scope=adat/szotar_szerepek.tsv | forras=olvasás (`cut -f1-5`) | ts=2026-10-09` — 13 szerep (1–10, 12, 13, 14) × 2 nyelv = 26 adatsor.
- `adat/karoli_strong/parok_*.tsv` `bizonyossag` oszlop: `scope=adat/karoli_strong/parok_Ezs.tsv (első sor) | forras=head | ts=2026-10-09` — `alacsony`; a `magas` pár korlátját az F65 brief 2026-10-05-i mérése adja, nem újramértem.
- minden további „van / nincs” állítás: `forras=manual` (olvasás és grep a megnevezett fájlokon), nem lekérdezés.

### 3.5 Elfogadási pontok (brief 7.)

| # | pont | állapot |
| --- | --- | --- |
| 1 | minden delta-sor a naplóban, igen/nem érintettséggel és indokkal | 33 sor, 3.1 |
| 2 | az átírt szakaszok listája és a `git diff` egyezik | 3.2; a hunk-ok `git diff -U0 2108fc67..HEAD` szerint szakaszra bontva, az ellenőr lefuttatja |
| 3 | minden átírt állítás mellett a hivatkozott DT-/N-/#-tétel | DT57, DT73, DT74–DT89, DT-M1/M4–M8, DT-F52h/i, N-F34b, N55, FELADATOK-számok |
| 4 | nem maradt megfordított állítás | keresve: `M1 a #78 után`, `1–5Móz és Józs`, `a Bírák`, `Bírákig`, `11 szerep`, `nem teljes` (TAHOT), `▶ fut (2. futás`, `Azóta négy`, `2026-10-06-i`: a találatok csak történeti döntésnapló-sorok és a lezárt jelölések |
| 5 | döntésnapló-sor és kiindulási állapot sor bent | ATALAKITASI v11 sor; MUNKATERV v6; ADATVAGYON v17 + kiindulási állapot sor; VIBE v5 |
| 6 | a dokumentum többi része bájtazonos | cserék pontos illesztéssel (`ed.py`: pontosan egy előfordulás, különben leáll; a 4a tartományt sor-kezdetek jelölik), CRLF megőrizve |
| 7 | terv → feladat (3b): nincs rés kimenet nélkül; `feladatok.py ellenoriz` 0 hiba | 3.3 (11 sor: 2 DT-tétel, 2 átvezetés, 1 ⛔ jelezve a felhasználónak, 6 meglévő kimenet / lezárt / nem rés); `ellenoriz`: 0 hiba (104 brief) |

### 3.6 Ellenőr és javító kör (brief 4.8)

A `fuggetlen-ellenor` jelentése: `naplok/ELLENOR_TERV_SZINKRON_3.md` (F52.26, `24366c5e`): 5 eltérés, blokkoló nincs; a `feladatok.py ellenoriz` 0 hibáját az orkesztrátor futtatta. Az F52.25 (`6e2336d5`) a napló sorvégeit LF-re normalizálta (az F52.23 hibás sorvéggel írta); a javító kör LF-fel ír.

| # | eltérés (ellenőr) | javítás | commit |
| --- | --- | --- | --- |
| 1 | ATALAKITASI 9. kockázat-tábla, TAHOT-sor: a jelen idejű Jób 40:1-5 / Jób 41 rés-állítás hamis | „elavult” jelölés (F84, DT86, N55), maradó korlát a Jób 40 MT-kulcsa | F52.27 |
| 2 | ATALAKITASI 13.3 és ADATVAGYON 18.5: a DT80–DT83 összefoglalása hiányos (hivatkozás az `adatosítva` szerepnél, 5./6./7. szerep, H7121 → BDB 2.c) | a DONTESEK szövege szerint kiegészítve | F52.28 |
| 3 | ADATVAGYON „Státuszok”, v16 sor, állapotfrissítés: „a 7. adag a DT56 küszöbével” | a 7. adag (86%) indulhat, a 8. adagtól a küszöb dönt (DT56) | F52.29 |
| 4 | napló 3.2 és ADATVAGYON v17/új sor: az ATALAKITASI 4.7 sor a 18.1-ben, az N-F34b a 18.4-ben van, nem a 17.2-ben | szakaszbesorolás javítva (a napló delta 15. sora is) | F52.30 |
| 5 | SEMA 4 ↔ CLAUDE.md ellentmondás ⛔ nélkül (SEMA :1229) | ⛔ jelezve a felhasználónak; a SEMA nincs az `ir`-ben, nem javítva; delta 27. sor, 3.3/11., Nyitott tábla, ADATVAGYON 22.5 | F52.32 |

Az ellenőr megjegyzései (alap `1f420a7c`, #71 PR #226, #73 PR #231, a 6. lépcső DT nélküli eljárási állítása) szintén javítva: F52.31.

## Nyitott a következő futásra

A futások között felgyűlt tételek, amelyeket a következő szinkron a delta-listájába vesz (brief 4.2). Csak hivatkozással (brief 4.3b): a tétel kimenete a hivatkozott DT-tétel, csonk vagy ⛔. A 2. futás nyitott tételei lezárva: a VIBE `lepes=MCP` sor (DT49 ✅), a #25 kettéválasztása (#76 befogadva), DT-M4–M6 (DT76), a DT-M8 (d) (a #11 csonk `olvas:` sora), a SQLITE\_EPIT (#79) és a SZPA\_AUDIT (feltételes, DT77 (13)).

| tétel | forrás | kimenet |
| --- | --- | --- |
| a D23 (`OT-full` scope-címke) újratárgyalása a #84 után | a 3. futás 3.3/1. | DT-F52h (🟡); a döntés után az ATALAKITASI D23/N13 sora és az ADATVAGYON 22.4 `scope`-mondata |
| „feltételes” jelzés a VIBE 5. szakasz MCP\_BUROK és SZPA\_AUDIT sorában | a 3. futás 3.3/2. | DT-F52i (🟡) |
| a #23 M1 13 `javaslat` pontja | DONTESEK DT84 (🟡) | a felhasználó döntése; utána a #23 `kovetkezo`-ja, az ATALAKITASI 13.4 „DT84 🟡” jelölése és a MUNKATERV 4a #23 sora |
| a `adat/SEMA.md` 4. szakasz (:1229) „Jób 40:1-5 és a teljes Jób 41. fejezet hiányzik” ↔ `CLAUDE.md` TAHOT-mondat ellentmondása | a 3. futás 3.3/11. | ⛔ jelezve a felhasználónak (orkesztrátor); a SEMA 4 javítása a #52 hatókörén kívül esik; a javítás után az ADATVAGYON 22.5 „SEMA 4.” sora |
| a #22 Jób és Péld menete, a #38 7. adagja, a #62/#63 indítása | FELADATOK | a státuszok a következő futás delta-listájába (nem terv-tétel) |
