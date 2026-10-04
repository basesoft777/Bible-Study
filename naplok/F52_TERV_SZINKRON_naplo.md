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
| 8. | v2 sor |

**Egyéb fájlok (nem tervdokumentum)**

- `DONTESEK.md`: DT-F52a — a brief 6. pontja szerinti megállás tétele, a felhasználó chat-döntésének rögzítése (✅ alkalmazva).
- `F52_TERV_SZINKRON_BRIEF.md`: fejléc (`allapot: fut`, `ag`, `pr: 172`, `kovetkezo`, `ir` + DONTESEK.md és az ellenőr-napló), cím `F52`.
- ez a napló.

### 1.3 Nem átvezetett, kérdéses tételek (brief 4.7, 6. pont)

| tétel | miért nem | javaslat |
| --- | --- | --- |
| VIBE 5. szakasz OLVASOI_KONKORDANCIA sora és 7. hibatábla licenc-sora: „a licenc-szűrő STEPBible-származékot nem enged ki", „STEPBible-származék a kimenetben = 0" | a brief 6. pontja a VIBE 5. szakaszt a sorszám/név cseréig engedi; a DT-F33f/j után az állítás elavult | felhasználói döntés: „blokk dataset-kulcs nélkül = 0; kereskedelmi módban `kereskedelmi=nem` forrás = 0" (a MUNKATERV 6. szakaszával egyezően) |
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
| 4 | nem maradt megfordított állítás (régi alak keresve) | „nem terjeszthet", „csak backend", „Józsué következik/jön", „merge-elve, kézi", „#47–#55" (döntésnaplón kívül): 0 találat; a VIBE két licenc-sora szándékosan maradt (1.3) |
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
