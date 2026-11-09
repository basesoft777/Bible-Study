# F184 — Egy szabály, egy hely (DOKU_EGY_FORRAS): jelentés

*Menet- és zárójelentés egy fájlban (a brief D4 szerint). Első kör: D0, majd ⛔; második kör (a D0 jóváhagyása után): D1–D5 és a Zárás. A D6 (független ellenőr, draft PR) az orkesztrátoré.*

## D0 — leltár

**Modell-ellenőrzés.** A session tényleges modellje `claude-opus-5-5`; a brief `modell` mezője `opus` — egyezik.

**Proveniencia.**
- Gépi keresés 1 (azonosítók): `python naplok/F184_leltar_azonositok.py . <kimenet.tsv>` — 26 dokumentum (`CLAUDE.md`, `MUNKAMENET.md`, `BRIEF_SABLON.md`, `adat/SEMA.md`, `Rendszerfejlesztesi_playbook.md`, `sablonok/*.md`, `.claude/commands/*.md`; a `DONTESEK.md`-ből csak a hivatkozott DT-sorok definíciós sora), jelek: `V<n>`, `E<nn>`, `HIBA-*`, `C-vh`, `DT<n>`, `DT-F<nn><x>`, `SEMA <n.nn>`, kapunevek, `ellenoriz.py <n>.`; eredmény: 62 azonosító legalább két dokumentumban.
- Gépi keresés 2 (szabály-kifejezések azonosító nélkül): `python naplok/F184_leltar_kifejezesek.py .` — 34 kifejezés (pl. „első előfordulásnál”, „Pesat-gerinc”, „Feed 8”, „U2/U3”, „másik kéz”, `dontesek/uj`), a fenti dokumentumok + `.claude/agents/*.md`.
- Összevetés: a találati sorok szövegének kiolvasása (scratch sorkiíró, a repón kívül), a kiejtés-bekezdés hat példánya `md5sum`-mal.
- `scope=folyamat-dokumentumok (26 + agents) | forras=naplok/F184_leltar_azonositok.py, naplok/F184_leltar_kifejezesek.py @ cc7e1930 | ts=2026-11-09T17:14:51Z`
- A „másolat-e” és az „eltér-e” ítélet a kiolvasott sorokon alapuló értelmezés, nem gépi mérés (CLAUDE.md 3. szabály); ahol nem vetettem össze mondatról mondatra, a sor ezt kimondja.

**Jelölések.** ⛔ = a másolatok tartalmilag eltérnek, és a kanonikus kiválasztása tartalmi döntés. **D1-kérdés** = a szabály a D1 öt kategóriájának (lap → `6_`; forrás/cikk → `9_`/`10_`; adat → SEMA; munkamenet-lépés → MUNKAMENET; döntés → DONTESEK) egyikébe sem esik tisztán (folyamat-, git- vagy parancsszabály); a hely kijelölése az orkesztrátoré, nem tartalmi döntés.

| # | szabály (rövid név + azonosító) | előfordulások (fájl:szakasz/sor) | eltérnek-e a másolatok | javasolt kanonikus hely | D2 érinti a SEMA-t |
|---|---|---|---|---|---|
| 1 | Visszhang: a lánc levezetése a motívumadatból (DT648) | `MUNKAMENET.md` C-vh :75; `adat/SEMA.md` 2.53 „A lánc honnan jön” :2120–2131; `sablonok/6_…` „A 4.11 visszhang-blokk szabályai” 0. :532; `DONTESEK.md` :682 | **igen** — hiány: a C-vh rövidebb (nincs benne a szópár, a `tematikus:` és a görög elem kizárása, „az első Pesat-sor könyvében”, „Pesat-sor nélkül nincs lánc”); a SEMA és a `6_` egyezik *[helyesbítés, F184.13 (ELLENOR_F184 1.): nem egyezett; a SEMA-ban négy elem többlet volt, l. „Javítókör 1/2”]* | `6_` 4.11-szabályok 0. pont (lapszabály); a SEMA 2.53 a tábla szerepét mondja + hivatkozás; a C-vh csak lépés + hivatkozás | igen |
| 2 | Visszhang: kinyerés két kézzel, átnézés-bemenet (DT639, DT646, ELLENOR_F178 3–4.) | `MUNKAMENET.md` C-vh :75; `adat/SEMA.md` 2.53 „Két kéz” :2133–2148; `sablonok/9_…` :5; `sablonok/6_…` :519 (említés) | nem (a C-vh tömörített, egyező) | SEMA 2.53 „Két kéz” (adatírás szabálya) | nem |
| 3 | ⛔ Visszhang: mikor kiemelt a következtetés (DT645 + utólagos pontosítás) | `sablonok/6_…` „Visszhang-blokk (4.11)” összefoglaló :527; `sablonok/6_…` 4.11-szabályok 2.–3. :534–535; `eszkozok/olvasoi_kapu.py` V5-komment :975–976; `DONTESEK.md` DT645 :679 | **igen** — tartalom: a :527 és a V5-komment szerint két héber lánc-szó egy szóval *feltétel nélkül* kiemelt (a DT645 (a) eredeti szövege); a :535 és a DT645 „Pontosítás (orkesztrátori átnézés)” szerint csak alapvonallal (Targum/Vulgata: nem kiemelt). A DT-sor tartalma utólag, új tétel nélkül módosult (a brief #178-as esete) | javaslat: `6_` :535 (a pontosított alak); a :527 → hivatkozás; a V5-komment a D3-ban a kódból | nem |
| 4 | Visszhang-kapu V1–V7 (DT646, DT-F178d/e) | `eszkozok/olvasoi_kapu.py` docstring :37–40 (V1–V7); ugyanott kódkomment :970–977 (**V1–V6**); `sablonok/6_…` :529–540 (a szabályokba szórva); `MUNKAMENET.md` :75 („V1–V7”); `DONTESEK.md` DT646 :680 (V1–V7) | **igen** — a kód belső kommentje V1–V6 (V7 hiányzik); a dokumentumok egyeznek | a kód docstringje → D3 GENERÁLT blokk | nem |
| 5 | Gépi kapuk a generált lapon: `ellenoriz.py` 24. és 25., olvasói kapu 0 BUKÁS, teljesség-mérés (DT546, DT547) | `MUNKAMENET.md` C-g :76, „A lezárás menete” 1. :90; `sablonok/6_…` Minőségi kapu L8 :480–483; `sablonok/9_…` „Gépi kapuk a generált lapon” :283; `sablonok/10_…` :55–59; `.claude/commands/lap-javit.md` 5.2 :84 | nem | `6_` Minőségi kapu L8 | nem |
| 6 | A lezárás „kész” feltétele: Feed-kapuk száma (DT547: 9. kapu = olvasói kapu) | `MUNKAMENET.md` C5 :81 („mind a 9 kapuja”); `sablonok/6_…` Kolofon :304 („a Feed 8 kapuja zöld”); `sablonok/4_…` :387 („a Feed 8 kapuja zöld”); `DONTESEK.md` :588 | **igen** — elavult: a `6_` és a `4_` a DT547 előtti 8 kaput mondja (a döntés eldöntötte, nem tartalmi kérdés) | a „kész” definíció: `6_` (a lap kiadhatósága), a kapulista a `muhely_allapot.py`-ból (D3-jelölt); MUNKAMENET C5 hivatkozik | nem |
| 7 | Kiadás-sor és kolofon kiadásszám (SEMA 2.46, DT492, DT486) | `adat/SEMA.md` 2.46 :1827–; `sablonok/6_…` :304; `MUNKAMENET.md` C5 :81, C-k :82; `.claude/commands/kiadas.md` 5. :22; `.claude/commands/lap-javit.md` 5.4 :87 | nem (a `kiadas.md` a mezőket is felsorolja, egyezően) | SEMA 2.46 | nem |
| 8 | Lapjavítás és a kolofon „Emberi lektorálás” sora (SEMA 2.49, DT599) | `adat/SEMA.md` 2.49 :1907–1936; `sablonok/6_…` :304; `MUNKAMENET.md` C-j :83; `.claude/commands/lap-javit.md` :7, :97; `.claude/commands/kiadas.md` 4. :21 | nem | SEMA 2.49 (adat) + `lap-javit.md` (az eljárás) | nem |
| 9 | ⛔ Lap-átnézés érvényessége gépi javítás után (SEMA 2.48, DT554, DT569) | `adat/SEMA.md` 2.48 „Érvényesség” :1899–1901; `adat/SEMA.md` 2.49 :1933–1934; `MUNKAMENET.md` menetszabály 7. :101; `.claude/commands/lap-javit.md` 5.4 :88; `DONTESEK.md` DT569 :607 | **igen** — tartalom: a SEMA 2.48 szerint *bármely* lapváltozás érvényteleníti az átnézést (a Feed 9 így méri); a MUNKAMENET :101 („DT569 mintája”) és a `lap-javit.md` kivételt tesz a gépi forrásadat-javításra, eltérő hatókörrel („szótári/KH-rész” ↔ „szótári rész”); a DT569 egy esetre (ALVIL-001) szól | döntésre: általános szabály-e a DT569, és ha igen, a SEMA 2.48-ba kerül (a 9. kapu kódjával együtt); javaslat: SEMA 2.48 | igen (a döntéstől függően) |
| 10 | Kiejtés-szabály (a „Kiejtés.” bekezdés; `ellenoriz.py` 22.) | `sablonok/1_…` :68; `sablonok/2_…` :305; `sablonok/4_…` :437; `sablonok/5_…` :72; `sablonok/6_…` :382; `sablonok/PaRDeS_gyorsreferencia.md` :30 | nem (hat bájtazonos példány, md5 `7d6808da`) | **D1-kérdés** (tanulmány- és lapszabály egyszerre); javaslat: `sablonok/PaRDeS_gyorsreferencia.md` (a CLAUDE.md táblája minden tanulmányíráshoz nyitja), a többi öt hivatkozik | nem |
| 11 | Az 1/a kötelező formája: kerek `kapcsolodas` + „Funkció:” (25. szabály, DT546, DT-F1Ab) | `sablonok/9_…` 4. pont :108–112, hét szabály 5. :156; `sablonok/6_…` :138–142, v3.1 :5; `sablonok/10_…` :33; `MUNKAMENET.md` C-g :76 | nem | `9_` 4. pont | nem |
| 12 | Károli-idézet a `kapcsolodas`-ban (CI E34, SEMA 2.50, DT614; olvasói kapu IDEZET) | `adat/SEMA.md` 2.50 :1940–1951; `sablonok/9_…` :110, öt szabály 5. :148, hét szabály 5. :156; `sablonok/10_…` :33 | nem tartalmilag; a SEMA részletesebb (elfogadott jelölések: „saját fordítás”, „szó szerint:”, „ford.:”), a `9_` csak a „saját fordításban” alakot mondja | SEMA 2.50 (a mező tartalmi kötése) | nem |
| 13 | U2/U3 szétválasztás (F178.2) | `sablonok/9_…` hét szabály 1. :152; `MUNKAMENET.md` C-w :74; `sablonok/10_…` 1. :15 | nem | `9_` hét szabály 1. | nem |
| 14 | Határ-frissesség, SORÁLLAPOT-jel (`ellenoriz.py` 39., Feed 5) | `sablonok/9_…` hét szabály 2. :153; `MUNKAMENET.md` C-h :77; `sablonok/10_…` :15; `sablonok/6_…` :542 | nem | `9_` hét szabály 2. | nem |
| 15 | HAMART-001 regressziós kapui és a Nave-blokk (`ellenoriz.py` 37–40, DT595) | `sablonok/6_…` :542; `sablonok/9_…` hét szabály :150–160 (a :160 már hivatkozik a `6_`-ra); `sablonok/10_…` 4. :35 | nem | `6_` (a gépi rész) + `9_` (a cikkszabály), a mai felosztás szerint | nem |
| 16 | A lexikonlap rései (DT276, DT597, DT643) | `CLAUDE.md` rétegek :46–58; `adat/SEMA.md` 2.12 :742–768; `sablonok/6_…` :256, :457, :521; `MUNKAMENET.md` C1 :70, C2 :71 | **igen** — elavult: a MUNKAMENET C1/C2 „hét rést” sorol (`alkalmazas`, `tanitoi` nélkül), a DT276 óta kilenc (a `tanitoi` kivezetés alatt, DT643); a döntés eldöntötte | SEMA 2.12 | nem |
| 17 | A régi lektori kártyák lezárása („az újraírás okafogyottá tette”; DT566, DT585) | `MUNKAMENET.md` „A lezárás menete” :95 és menetszabály 5. :99 (belső ismétlés) | **igen** — kiegészítés: a :99 kiveszi a határkártyákat (`forras=hatar`: a felhasználó dönt), a :95 nem | `MUNKAMENET.md` :99 (munkamenet-szabály), a :95 hivatkozik | nem |
| 18 | ISTENTISZT-mérce: L1–L7 + a DT2 két rés-szabálya (DT68, DT74) | `sablonok/6_…` Minőségi kapu :502–506; `sablonok/9_…` 8. :270; `MUNKAMENET.md` :168 | nem | `6_` Minőségi kapu | nem |
| 19 | Elutasítási okok, nincs „egyéb” (`ellenoriz.py` 28., SEMA 2.43) | `adat/SEMA.md` 2.43 :1755; `sablonok/9_…` öt szabály 1. :144 | nem | SEMA 2.43 | nem |
| 20 | Értelmező próza egy kézben / a próza gazdája (K1, DT-F32b) | `CLAUDE.md` :48; `MUNKAMENET.md` „Kontextus-őrzés” 1. :146–154, C-w :74; `BRIEF_SABLON.md` :50; `sablonok/9_…` :27; `.claude/commands/lap-javit.md` :15, :99; `.claude/commands/kiadas.md` :21 | nem | **D1-kérdés** (folyamatszabály, nem lépés); javaslat: `MUNKAMENET.md` „Kontextus-őrzés” 1., a `CLAUDE.md` egy mondattal hivatkozik | nem |
| 21 | A `munka` mező szabályai (E18 `MUNKA_HIANY`, DT-F32c; a `lexikon/` nem motívumfájl, DT28) | `BRIEF_SABLON.md` :48–53; `MUNKAMENET.md` „Kontextus-őrzés” :144–162; `CLAUDE.md` :37; `.claude/commands/kovetkezo.md` :16 | nem | **D1-kérdés**; javaslat: `BRIEF_SABLON.md` (fejlécmező) | nem |
| 22 | Egyirányúság (DT28) | `CLAUDE.md` :37; `adat/SEMA.md` bevezető :8–11 és 3. szakasz 9. :2207–; `sablonok/9_…` 1. pont :42; `BRIEF_SABLON.md` :51 | nem (a SEMA-n belül is két helyen áll) | SEMA 3. szakasz 9. (adatfolyam); a `CLAUDE.md` egy bekezdéssel hivatkozik — **D1-kérdés**, mert a `CLAUDE.md` a belépési pont | igen (a SEMA :8–11 → hivatkozás) |
| 23 | Nincs közvetlen út (CLAUDE.md 2. szabály) | `CLAUDE.md` :69; `adat/SEMA.md` 2.2 :193–195, 3. szakasz 2. :2187; `.claude/agents/vegrehajto-*.md` :15 | nem | SEMA 3. szakasz 2.; a `CLAUDE.md` „Három szabály” egy mondattal marad — **D1-kérdés** | nem (a 2.2 már utal) |
| 24 | Szintjelölés és kinyerés a kézi forrásból (DT66, DT84, DT182, DT183, DT202, DT76, DT-F86a/c, E29) | `adat/SEMA.md` 3.10 :2216–2367 és 2.x (:218, :320, :357); `sablonok/9_…` passim (:15–19, :38, :56–101, :162–256); `sablonok/2_…` :258, :276; `sablonok/4_…` :402–416 | **nem mértem** — a `9_` a jelölőket a szerző felől, a SEMA 3.10 a kinyerés felől írja (MUNKAMENET „Kontextus-őrzés” 2. ezt a felosztást rögzíti); mondatról mondatra a D2-ben vetendő össze | SEMA 3.10 (kinyerés), `9_` (jelölők, szakaszrend) | mérendő a D2-ben |
| 25 | Helyőrző és PR-fájl az új döntéshez/nyitott tételhez (`dontesek/uj`, `nyitott/uj`; E26) | `CLAUDE.md` Git :198; `BRIEF_SABLON.md` :55, :73; `MUNKAMENET.md` :112; `.claude/commands/lap-javit.md` :36, :69, :98; `.claude/commands/elteres.md` :20, :27, :33 | nem | **D1-kérdés** (git-/koordinációs szabály); javaslat: `CLAUDE.md` Git-szakasz | nem |
| 26 | Commit-üzenet UTF-8 fájlból | `CLAUDE.md` :205–225; `.claude/commands/elteres.md` :30; `.claude/agents/vegrehajto-*.md` :18 | nem | **D1-kérdés**; javaslat: `CLAUDE.md` | nem |
| 27 | Modell-ellenőrzés | `CLAUDE.md` :77–79; `.claude/commands/lap-javit.md` 0. :13; `.claude/agents/*.md` (6 fájl) | nem | **D1-kérdés**; javaslat: `CLAUDE.md` | nem |
| 28 | TSV: `split('\t')`, a `csv` modul tilos | `CLAUDE.md` :160–190; `adat/SEMA.md` táblánként (30 hely, „l. CLAUDE.md”); `sablonok/9_…` :67; `.claude/commands/lap-javit.md` :9; `.claude/agents/hatar-ellenor.md`, `lektor.md` | nem (a SEMA már hivatkozik) | `CLAUDE.md` | nem |
| 29 | Próza-lefedettség, küszöbök (DT471) | `MUNKAMENET.md` C-z :73; `.claude/commands/kiadas.md` 1. :13 | nem (a C-z részletesebb: küszöbök) | **D1-kérdés** (eszközszabály); javaslat: a `proza_lefedettseg.py` docstringje, a C-z és a `kiadas.md` hivatkozik | nem |
| 30 | CI-javító kör a draft PR után (F50, DT252) | `.claude/commands/kovetkezo.md` :91; `.claude/commands/befogad.md` :29 | nem (a `befogad` a saját fájlokra szűkít, ez szerepkülönbség) | **D1-kérdés** (parancsszabály); javaslat: `kovetkezo.md`, a `befogad.md` a szűkítéssel hivatkozik | nem |
| 31 | SEMA-szakaszszám ütközése: két „2.50” (a #166 esete, N-F166a) | `adat/SEMA.md` :1940 (E34, F166) és :1953 (nyílt mag, F162); `NYITOTT_FELADATOK.md` :852 | nem másolat, hanem kétértelmű hivatkozási cél: a „SEMA 2.50” két szabályt jelöl | a számozás rendezése (N-F166a) és a D5 hivatkozás-kapu: a szakaszszám egyedi legyen | igen |

**Kiszűrt találatok (csak hivatkozás, nem a szabály másolata).** A gépi keresés további azonosítói a dokumentumokban csak rámutatnak a szabályra (forrás- vagy döntésjelölés, változásnapló): DT-F37 (`1_`/`2_` verziófej), DT-F51 és E25 (`konzisztencia.md` → SEMA 2.21), E19 (`MUNKAMENET.md` C0 → SEMA :837), DT78 (`konzisztencia.md`, `kovetkezo.md`), DT226 (playbook → SEMA), DT277, DT430, DT473, DT512, DT603 (SEMA ↔ `6_`/`2_`: egymondatos utalás a mezőre), DT497, DT585 (a `9_` :3 kimondja, hogy a menetszabályok a MUNKAMENET-ben állnak), DT2/DT68/DT74 (a 18. sorban). Ezeket mondatról mondatra nem vetettem össze; a D2-ben a kanonikus hely kijelölése után egy ismételt gépi futás megmutatja, maradt-e másolat.

**Összesítés.**
- Sorok: **31**; ebből ⛔ (tartalmi döntés): **2** (3., 9.); elavult vagy hiányos másolat, amelyet egy meglévő döntés eldönt: **5** (1., 4., 6., 16., 17.); D1-kérdés (hely, nem tartalom): **11** (10., 20., 21., 22., 23., 25., 26., 27., 28., 29., 30.); nem mért: **1** (24.).
- Érintett fájlok (17): `CLAUDE.md`, `MUNKAMENET.md`, `BRIEF_SABLON.md`, `adat/SEMA.md`, `sablonok/1_…`, `2_…`, `4_…`, `5_…`, `6_…`, `9_…`, `10_…`, `sablonok/PaRDeS_gyorsreferencia.md`, `.claude/commands/kovetkezo.md`, `befogad.md`, `kiadas.md`, `lap-javit.md`, `elteres.md`; a táblán kívül, csak hivatkozásként: `eszkozok/olvasoi_kapu.py`, `.claude/agents/*.md`.
- A D2 SEMA-t érintő cseréi: **3 biztos** (1., 22., 31.), **1 döntésfüggő** (9.), **1 a D2-ben mérendő** (24.). A D3 GENERÁLT blokkja ezen felül kerül a SEMA-ba, ha az alábbi javaslat áll.
- Mellékmegfigyelés (nem D2-tétel, a briefen kívüli fájl): a DT646 (a) maga írja elő, hogy a visszhang-szabályok a `6_`-ban, a `10_`-ben és a C-vh-ban álljanak. A D2 ezt nem sérti, ha a `10_` és a C-vh csak hivatkozik (a `10_` :37–38 már így tesz).

### D3 előkészítés — a kapuk forrásai a kódban

| kapu | hol definiált | gépi kinyerhetőség |
|---|---|---|
| olvasói kapu (23 osztály: BELSO … NAVE_ANGOL; a VISSZHANG alatt V1–V7) | `eszkozok/olvasoi_kapu.py` docstring, „Ellenőrzések (azonosító — súlyosság)” :10–45; a találatok `talalat('<AZON>', BUKAS/FIGY, …)` hívásokban; a V-azonosítók csak az üzenetszövegben (`'V5 …'`) és a docstring VISSZHANG-sorában | az azonosítók a `talalat(` első argumentumaiból (23 egyedi) megbízhatóan; a leírás és a súlyosság ma csak a docstringből, szövegelemzéssel. Stabil forrás: egy modulszintű tábla (`KAPUK = {azon: (súly, leírás)}`, a V-alszabályokkal), amelyből a docstring és a GENERÁLT blokk is készül |
| `ellenoriz.py` szabályai (1–41, plusz 2/b, 8/b, 8/c) | függvények `szabalyNN_<név>` (:139–2296, nem számsorrendben: a 35. a fájl végén); a cím a `Sor('<N>. <cím>', …)` első argumentumában (43 ilyen literál), egyes helyeken `cim = '…'` változóban | igen: AST-tel a `Sor(...)`/`cim` literálokból a sorszám és a cím; a hosszabb leírás a függvény előtti `# NN. szabaly …` kommentben áll, egységes docstring nincs |
| CI E-szabályok (E2–E35) | `eszkozok/ellenorzes/szabalyok.py`: `def eNN_<név>` (28 függvény), szint a `SZINT` szótárban (:54–58, később bővítve: `SZINT['E30']` :2455 stb.), a futtatandók a `SZABALYOK_FUGGVENYEI`-ben (:1541–), egyesek közvetlenül a `futtat.py`-ban (E26, E27, E30, E35); az E1 maga az `ellenoriz.py` (`.github/workflows/ellenorzes.yml` :100) | igen: a modul importja után a `SZINT` kulcsai + a függvények docstringjének első sora; a `futtat.py` közvetlen hívásai miatt a teljes lista a `SZINT`-ből vehető, nem a `SZABALYOK_FUGGVENYEI`-ből |

Ma a CI E-szabályok listája egyetlen folyamat-dokumentumban sem áll (csak régi briefekben: `F02_…`, `F37_…`, `F116_…`), az `ellenoriz.py` szabályaiból pedig a SEMA 3. szakasza csak az 1–9.-et sorolja.

**Javaslat a GENERÁLT blokk helyére (egy hely):** `adat/SEMA.md` 3. szakasz („Integritási szabályok”) végén egy új alszakasz, például „3.11 Gépi kapuk — szabálylista”, `<!-- GENERÁLT: … -->` jelölők között. Három blokk: olvasói kapu (V-alszabályokkal), `ellenoriz.py` 1–41, CI E1–E35; mindegyik sorban azonosító, rövid leírás, súlyosság, forrásfüggvény. A CI-őr a blokkot újragenerálja, és eltérésnél bukik.
- Ok: a SEMA 3. szakasza ma is az `ellenoriz.py` szabályait írja le (1–9.), tehát ez a meglévő helye, és a kapuk zöme adatszabály. A `6_` L8, a `9_` :283 és :160, valamint a MUNKAMENET C-g és C-o csak hivatkozik rá.
- Alternatíva: a `6_` Minőségi kapuja, ha a blokk csak a lapon futó kapukat (olvasói kapu, 24., 25., 37–40.) tartja. Ekkor a CI és az adatszabályok listája külön helyre kerülne, ami a D3 „egy hely” céljával ütközik.

## A D0 jóváhagyása és az orkesztrátor döntései (2026-11-09, szó szerint)

Az orkesztrátor (`local_c8cc3610`) üzenete, a döntések szó szerint:

- „A 31 soros leltár-tábla jóváhagyva.”
- „(1) DT645: a 6-os sablon 535. sora (kiemelés csak alapvonallal) a kanonikus. Az 527. sort és a V5-kommentet erre igazítsd. A DT645 utólagos pontosítását új helyőrzős tétel rögzítse: DT-F184a, 🟢, orkesztrátori döntés, hivatkozással a #178 javítókörére, ahol ez már így dőlt el.”
- „(2) DT569: általános szabály, a tágabb hatókörrel. A **gépi** szótári és Károli-KH forrásadat-javítás nem érvényteleníti a lap átnézését, ha (a) a próza, a minősítés és a határ nem változik, (b) a diff csak a generált szótári/KH blokkokat érinti (gépileg ellenőrizve), és (c) a változást a kolofon vagy a jelentés felsorolja. Minden más lapváltozás érvényteleníti. Kanonikus hely: a SEMA 2.48; a MUNKAMENET és a /lap-javit erre hivatkozik. Új helyőrzős tétel: DT-F184b.”
- „D1: a munkamenet-szintű szabály a CLAUDE.md-ben, a lapszintű a 6-os sablonban kanonikus. A CLAUDE.md „Ezt olvasd” táblájába egy sor kerül a kanonikus helyekről.”
- „D3: a GENERÁLT blokk az adat/SEMA.md új 3.11 „Gépi kapuk — szabálylista” szakaszába kerül, generátorral és CI-őrrel. Ha egy kapu (pl. a V-alszabályok) leírása ma csak docstringben áll, vezess be hozzá modulszintű táblát.”
- „A két leltár-szkript maradhat; vedd fel őket a brief `ir` mezőjébe.”
- „Futás közben nincs hatókör-bővítés.”
- Kiegészítés: „a SEMA-cserék most mehetnek, külön commitokban, a nem-SEMA munka után. A 2.50-es szétválasztásnál: a #166 (PR #660, mergelve) nyitott tételként már rögzítette a két 2.50 ütközését (N-F166a). A szétválasztás ezt zárja le.”

A két új döntés a `dontesek/uj/doku-egy-forras.md`-ben áll (DT-F184a, DT-F184b, 🟢).

**Az `ir` mező kiegészítése.** A leltár-szkriptek és a PR-fájlok mellett felvettem azokat a fájlokat, amelyeket a jóváhagyott D0 tábla D2-cseréi érintenek, de a befogadó `ir`-listájából hiányoztak: `sablonok/1_*`, `2_*`, `4_*`, `5_*`, `sablonok/PaRDeS_gyorsreferencia.md`, `.claude/commands/lap-javit.md`, `kiadas.md`, `befogad.md`, valamint a `NYITOTT_FELADATOK.md`-t (az N-F166a lezárása). Ez nem új hatókör: a D2 a jóváhagyott tábla szerint ezeket a fájlokat cseréli. Ha az orkesztrátor másként látja, a megfelelő cserék visszavonhatók.

## D1 — kanonikus helyek (F184.1, `62900b28`)

A `CLAUDE.md` „Ezt olvasd” táblájába egy sor került: lapszabály → 6-os sablon; forrás-/cikkszabály → 9-es sablon, a próza promptja a 10-es; adatszabály → `adat/SEMA.md` (a kapulista: 3.11); munkamenet-lépés → `MUNKAMENET.md` (csak a lépés és a hivatkozás); munkamenet-szintű szabály → `CLAUDE.md`; döntés → `DONTESEK.md`.

A D0 tábla javasolt helyeitől két ponton tértem el, a D1-döntés miatt. (1) A kiejtés-szabály (10. sor) kanonikus helye a 6-os sablon lett a gyorsreferencia helyett, mert a D1 a lapszintű szabályt a 6-osba teszi. (2) A „kész” feltétel (6. sor) a `MUNKAMENET.md` C5-ben és a `muhely_allapot.py`-ban maradt; a 6-os és a 4-es sablon elavult „Feed 8” mondatát javítottam és hivatkozássá tettem.

## D2 — a másolatok cseréje hivatkozásra

| tétel | commit | cserék | fájlok |
|---|---|---|---|
| nem-SEMA cserék | F184.2 `e3338a2b` | 29 | 13 |
| SEMA: lánc-levezetés (1.), egyirányúság (22.), a 2.49 érvényesség-hivatkozása (9.) | F184.5 `0dfe41a7` | 3 | 1 |
| SEMA 2.48: DT-F184b (9.) | F184.6 `e3114724` | 1 | 1 |
| SEMA: a két „2.50” szétválasztása (31.) + az N-F166a lezárása | F184.7 `d0cb8d6c` | 1 + 1 | 2 |

Leltár-soronként (a nem-SEMA rész): 1.: 1, 2.: 1, 3.: 1, 4.: 2, 5.: 2, 6.: 2, 7.: 3, 8.: 1, 9.: 2, 10.: 5, 13.: 1, 14.: 1, 16.: 2, 17.: 1, 25.: 1, 26.: 1, 27.: 1, 30.: 1. A számlálás a cseréket méri; a 6-os sablon kolofon-mondata egyetlen cserével a 6., 7. és 8. sort is érinti, ezért ott a sorösszeg nagyobb a cserék számánál.

Ahol nem cseréltem, és miért:
- **11., 12., 15., 18., 19., 28. sor:** a másolat már hivatkozás volt, vagy a kanonikus helyen áll; nincs teendő.
- **10-es U3-prompt (11., 13., 14. sor):** a `sablonok/10_…` :15, :33, :35 a modellnek szóló utasítás. A D1 a 10-est a próza promptjaként a 9-essel együtt kanonikusnak veszi, ezért nem cseréltem.
- **20., 21. sor („egy kézben”, `munka` mező):** a D1 szerint a `CLAUDE.md` a kanonikus hely. A részletes szabályok azonban a MUNKAMENET „Kontextus-őrzés” szakaszában és a BRIEF_SABLON-ban állnak; áthelyezésük tartalmi és terjedelmi kérdés, ezért nem döntöttem → N-F184c.
- **22., 23. sor:** a jóváhagyott tábla szerint a SEMA a kanonikus. A SEMA bevezetőjének egyirányúság-mondata hivatkozássá vált; a `CLAUDE.md` alapszabályai maradtak (belépési pont).
- **24. sor:** nem mértem → N-F184d.
- **29. sor (próza-lefedettség):** a `kiadas.md` :13 csak egy tagmondatot ismétel (DT471); csere nélkül hagytam.
- **31. sor:** a „2.50” szétválasztásakor az E34-szakasz kapott új számot (2.55, a 2.54 után), mert a nyílt mag 2.50-es szakaszára élő mutatók hivatkoznak (`adat/nyilt_angol.tsv` fejléce, `eszkozok/nyilt_mag_angol.py`). Az E34-szakaszra csak a lezárt F166 brief `lezarva_osszegzes`-e és a belőle generált `FELADATOK.md`-sor mutat; ezek történeti szövegek, nem javítottam őket. *[Helyesbítés, F184.14 (ELLENOR_F184 2.): az állítás nem volt igaz. Élő mutató a `DONTESEK.md` DT614-sorának hivatkozás-oszlopa is volt; a `DONTESEK.md` nem állt az `ir`-ben, ezért jelentenem kellett volna. A javítás és a teljes mutatólista: „Javítókör 1/2”, 2. tétel.]* Az N-F166a a `NYITOTT_FELADATOK.md` meglévő sorában lezárva.

**Tartalmi eltérés, amelyet a döntések nem fednek: nincs.** A két ⛔ sort (3., 9.) a DT-F184a és a DT-F184b fedi; az elavult másolatokat (1., 4., 6., 16., 17.) meglévő döntés dönti el.

## D3 — generált szabálylista (F184.4 `5c5575dd`, F184.8 `f26301dc`)

- **Modulszintű táblák:** `eszkozok/olvasoi_kapu.py` `KAPUK` (23 azonosító, súlyosság, leírás) és `VISSZHANG_ALSZABALYOK` (V1–V7; a V5 a DT-F184a szerint). A docstring ellenőrzés-listája és a V1–V6-os kommentblokk helyett hivatkozás áll. `eszkozok/ellenorzes/szabalyok.py`: `SZABALY_LEIRAS` (30 CI-szabály) és `KULSO_SZABALYOK` (E1, E18). Az `ellenoriz.py` szabálycímei a kódliterálokból jönnek (`Sor('<N>. …')`, `cim = '<N>. …'`; 43 sor, a 34. szabály nem létezik).
- **Generátor:** `python eszkozok/ellenorzes/szabalyok.py --kapulista [--ir]`. Az `adat/SEMA.md` új 3.11 szakaszába ír, a `<!-- GENERÁLT-KEZDET: szabalyok.py --kapulista -->` … `<!-- GENERÁLT-VÉGE: … -->` jelölők közé.
- **CI-őr: E37** (HIBA, fájlszintű). A blokk egyezik a generálttal, és a forrástáblák a kóddal: a kibocsátott `talalat(...)`-azonosítók, a V-üzenetek, a `SZINT` kulcsai és a workflow lépésneveinek E-azonosítói. Akkor fut, ha a PR a SEMA-t vagy a blokk valamely forrását módosítja.
- A V5-kód már a pontosított szabályt mérte (`VH_KIEMELT_JO_RX`); csak a komment volt elavult.

## D4 — egy jelentés feladatonként (F184.3, `223b44d4`)

A `/kovetkezo` 10. lépése a zárást a `naplok/F<nn>_jelentes.md` „Zárás” szakaszába teszi. Külön `_zaras.md` nem készül, az `ELLENOR_*` külön marad. Az 5d, a 8. lépés és a csomag-sorok a jelentésre mutatnak (5 csere). A BRIEF_SABLON új „Jelentés” bekezdést kapott. A régi `_zaras.md` fájlokhoz nem nyúltam. A `feladatok.py` ütközés-kivétele (`naplok/*_zaras.md`, a feladat saját `naplok/F<nn>_*` fájljai) változatlanul lefedi a jelentést, ezért a `feladatok.py`-t nem kellett módosítani.

## D5 — hivatkozás-kapu (F184.4, `5c5575dd`)

**E36** (`eszkozok/ellenorzes/szabalyok.py`). A folyamat-dokumentumok négyféle hivatkozása létező célra kell, hogy mutasson:
- `SEMA[.md] n.nn[.n]` (a 3. szakasz számozott tételei „SEMA 3.n”-ként is érvényesek);
- `MUNKAMENET[.md] <lépés>`;
- `ellenoriz.py N.`;
- `olvasói kapu <AZON>`.

Emellett a SEMA szakaszszámai egyediek. A szabály nem a másolatok egyezését nézi.

Hatókör: a PR változott folyamat-dokumentumai. `None` vagy `--teljes` módban mindegyik dokumentumot nézi. Sorhoz kötött (D8): a hozzáadott soron HIBA, máshol JELENTÉS.

Korlát: ha egy PR csak a célt változtatja meg (például átszámoz egy SEMA-szakaszt), a változatlan hivatkozó dokumentumot PR-módban nem nézi. A `--teljes` jelentés viszont mutatja.

A mai repón az E36 egyetlen találata a SEMA 2.34 kettőzése (N-F184b).

Tesztek: `E36Teszt` (7) és `E37Teszt` (7) a `eszkozok/ellenorzes/tesztek/test_szabalyok.py`-ban.

## Javítókör 1/2 (ELLENOR_F184, 5 ELTÉRÉS-tétel)

*A besorolás és a döntések az orkesztrátoré (`local_c8cc3610`): az 1–4. tétel mechanikus, az 5. tartalmi, az orkesztrátor döntésével. A modell-ellenőrzés: a session tényleges modellje `claude-opus-5-5`, a brief `modell` mezője `opus` — egyezik.*

### 1. A D2 cseréinek tartalomvesztés-ellenőrzése (F184.13; ELLENOR_F184 1.)

A szabály: a csere nem törölhet tartalmat, csak másolatot cserélhet hivatkozásra. Hatókör: a `b4c4dae5..d4bd1f44` diff minden törölt sora (109), a brief fejlécének sorai nélkül (azokat az orkesztrátor állítja). Minden törlést tartalmazó hely (hunk) egy sor; a törölt tartalmat tagmondatonként vetettem össze a kanonikus hellyel (kiolvasás, nem gépi mérés).

| # | csere | törölt tartalom | hol áll a kanonikus helyen | eredmény |
|---|---|---|---|---|
| 1 | `befogad.md:29` (30. sor) | a CI-javító kör teljes leírása (`gh run …`, log-idézet + proveniencia, javítható/nem javítható, két kör, üzenetalak, megállás) | `.claude/commands/kovetkezo.md` 10. lépés, „CI-javító kör” (minden elem; a „befogadott brief” is) + a két szűkítés a `befogad.md`-ben | OK |
| 2 | `elteres.md:30` (26. sor) | nincs törölt tartalom (csak hivatkozás került a sor végére) | – | OK; a hivatkozás célja hibás volt, l. a 4. tételt |
| 3 | `kiadas.md:22` (7. sor) | a `kiadasok.tsv` mezői és kitöltésük | `adat/SEMA.md` 2.46 (`kiadas` folytonos, `datum`, `valtozas` egy mondat, `proza_modell` a futó környezetből vagy `manual`, `forras`); a „nem briefből másolva”: `CLAUDE.md` „Modell-ellenőrzés” | OK |
| 4–8 | `kovetkezo.md:56, 81, 83, 87, 92` (D4) | „zárójelentés”, `naplok/<feladat>_zaras.md` | a D4 döntése szerint a jelentés „Zárás” szakasza; `BRIEF_SABLON.md` „Jelentés” | OK (szándékolt csere, D4) |
| 9 | `lap-javit.md:15` (27. sor) | a modell-eltérés jelzésének szövege | `CLAUDE.md` „Modell-ellenőrzés” (szó szerint) | OK |
| 10 | `lap-javit.md:87` (7. sor) | `kiadas` = előző + 1, `valtozas` egy mondat, `proza_modell` a tényleges modellnév | `adat/SEMA.md` 2.46 | OK |
| 11 | `lap-javit.md:88` (9. sor) | DT569; gépi forrásadat-javítás csak a szótári részen nem érvényteleníti; próza-/szerkezeti változásnál új átnézés | `adat/SEMA.md` 2.48 „Érvényesség” (DT-F184b, a DT569 általánosítása; „minden más lapváltozás érvényteleníti”) | OK |
| 12 | `BRIEF_SABLON.md:73` (25. sor) | PR-fájl, a fő fájl végére nem (ütközés, `dontes_nezet.py`), `szamkiosztas` Action, helyőrző, végleges szám nem | `CLAUDE.md` „Git” (minden elem) | OK |
| 13 | `MUNKAMENET.md` C1 (16. sor) | „a hét rés” felsorolása | `adat/SEMA.md` 2.12 (kilenc rés; a hét elavult, DT276) | OK (elavult másolat) |
| 14 | `MUNKAMENET.md` C2 (16. sor) | „hét rés, l. lent” | `adat/SEMA.md` 2.12 | OK (elavult másolat) |
| 15 | `MUNKAMENET.md` C-w (13. sor) | az U2/U3 szabály szövege | `sablonok/9_…` hét szabály 1. | OK |
| 16 | `MUNKAMENET.md` C-vh, lánc (1. sor) | a lánc-szó, a kulcsszavak, a láncvers, a gerinc meghatározása | `sablonok/6_…` 4.11-szabályok 0. pont | OK |
| 17 | `MUNKAMENET.md` C-vh, két kéz (2. sor) | soronkénti ítélet, lemma-megerősítés, `bdb`-kulcs, a sablonmondatot elutasító beolvasó, a kinyerő = ellenőr eset | `adat/SEMA.md` 2.53 „Két kéz” | OK |
| 18 | `MUNKAMENET.md` C-vh, kapu (4. sor) | „V1–V7” | `adat/SEMA.md` 3.11 (GENERÁLT, V1–V7) | OK |
| 19 | `MUNKAMENET.md` C-g (5. sor) | 24. és 25. szabály, a forma helye, a teljesség-mérés | `sablonok/6_…` Minőségi kapu L8 (a 3. tétel bővítésével) | OK |
| 20 | `MUNKAMENET.md` C-h (14. sor) | 52/60/11; a `SORÁLLAPOT`-jel és parancsa; az elavulás feltétele; Feed 5; `ellenoriz.py` 39.: **„jelentés minden érintett motívumra”** | `sablonok/9_…` hét szabály 2. és a bevezető (52/60/11) — a „jelentés minden érintett motívumra” tagmondat **hiányzott** | **visszaállítva** a 9_ hét szabály 2. pontjába |
| 21 | `MUNKAMENET.md:95` (17. sor) | a régi lektori kártyák lezárása („az újraírás okafogyottá tette”) | `MUNKAMENET.md` 5. menetszabály (bővebb: a határkártyák kivétele) | OK |
| 22 | `MUNKAMENET.md:101` (9. sor) | a DT569 kivétele | `adat/SEMA.md` 2.48 „Érvényesség” | OK |
| 23–27 | `sablonok/1_`, `2_`, `4_:437`, `5_`, gyorsreferencia: „Kiejtés.” (10. sor) | a kiejtés-szabály teljes bekezdése | `sablonok/6_…` :382, bájtazonos | OK |
| 28 | `sablonok/4_:387` (6. sor) | C-h (a felhasználó indítja) → C-l (`naplok/LEKTOR_<ID>.tsv`) → C5 (Feed-kapuk, 1. kiadás, verzió-emelés); `/kiadas` = 2. kiadás bemenete (C-k) | `MUNKAMENET.md` C-h, C-l, C5, C-k („Feed 8” → 9: DT547) | OK |
| 29 | `sablonok/6_:304`, kolofon (6., 7., 8. sor) | verzió-emelés, újragenerálás; `/kiadas` 5. lépése, a felhasználó indítja; DT486; `/lap-javit` útja, a négy `gond`, `lap_javitasok.tsv` | `MUNKAMENET.md` C5, C-k, C-j; `adat/SEMA.md` 2.46, 2.49 | OK |
| 30 | `sablonok/6_:481–482`, L8 | nincs törölt tartalom (a két törölt sor szövege a négy új sorban megvan) | – | OK; a bővítés: 3. tétel |
| 31 | `sablonok/6_:527` (3. sor) | cella kiejtéssel és `n/N`; „ugyanaz a szócsalád”; betoldás; alapvonal (≥ 80%, < 40%, Targum/Vulgata nem mérhető); kiemelés; csak valódi rokon nyelv, nyelvenként egy sor; kiejtés minden nem latin betűs szónál | `sablonok/6_…` 4.11-szabályok 1–6. (a kiemelés a DT-F184a szerinti pontosított alakban) | OK |
| 32 | `sablonok/6_:529` (4. sor) | „V1–V7” | `adat/SEMA.md` 3.11 | OK |
| 33 | `sablonok/9_:283` (5. sor) | 24., 25. szabály („arany szintű: kerek próza + Funkció”), olvasói kapu, teljesség-mérés | `sablonok/6_…` L8 | OK |
| 34 | `adat/SEMA.md:9–11` (22. sor) | egyirányúság: kinyerés a `jeloltek.tsv`-n át, generálás, nincs visszaírás | `adat/SEMA.md` 3. szakasz 9. | OK |
| 35 | `adat/SEMA.md` 2.53 „A lánc honnan jön” (1. sor) | a lánc levezetése, benne: **„A háttér-táblában csak a lánc-szavak és tövük állnak”**, **„(TAHOT)”**, **„HAMART-001: 6 kulcsszó”**, **„(a beépített sorok versei, a tartomány versenként)”** | `sablonok/6_…` 4.11-szabályok 0. pont — a négy elem **hiányzott** (a többi megvan; a „lánc-szó `bdb` sor nélkül” mondat a 8. pontban, a `lanc_szavak` a SEMA 2.53-ban maradt) | **visszaállítva**: a három lánc-elem a 0. pontba, a „lánc-szavak és tövük” a 6. pontba (BDB-háttér) |
| 36 | `adat/SEMA.md` 2.48 (9. sor) | nincs törölt tartalom (a két sor bővült) | – | OK |
| 37 | `adat/SEMA.md` 2.49 :1934 (9. sor) | „DT569” | `adat/SEMA.md` 2.48 („a DT569 általánosítása”) | OK |
| 38 | `adat/SEMA.md` 2.50 → 2.55 (31. sor) | a teljes E34-szakasz | `adat/SEMA.md` 2.55, szó szerint (a cím kiegészült) | OK; a mutatók: 2. tétel |
| 39 | `eszkozok/olvasoi_kapu.py` docstring (D3) | a 23 kapu leírása és súlyossága | `KAPUK` tábla (szó szerint; a helyőrzők helyén a végleges DT602/603/645/646) | OK |
| 40 | `eszkozok/olvasoi_kapu.py` V1–V6 komment (4. sor) | V1–V6 leírása | `VISSZHANG_ALSZABALYOK` (V1–V7; a V5 a DT-F184a szerint) | OK |
| 41 | `.github/workflows/ellenorzes.yml:73` | a lépés neve („E2-E30”) | ugyanott, „E2-E37” (a régi szöveg minden eleme megvan) | OK |
| 42 | `NYITOTT_FELADATOK.md:852` | nincs törölt tartalom (az N-F166a sora lezárva, a régi szöveg „Előzmény”-ként megmaradt) | – | OK |

**Összesítés:** 42 törlést tartalmazó hely; ebből **2 volt hiányos** (20., 35.); visszaállítva **5 elem** (a 9_ hét szabály 2. pontjába 1 tagmondat; a 6_ 4.11-szabályok 0. pontjába 3, a 6. pontjába 1). A többi 40 helyen a törölt tartalom szó szerint vagy egyenértékűen megvan a kanonikus helyen.

### 2. A régi „2.50”-mutatók (F184.14; ELLENOR_F184 2.)

Keresés: `git grep -n -I '2\.50'` a teljes repón, a találatok kézi szétválogatásával (a `12.50`-féle UBS-domén és versszám-találatok kiszűrve). `scope=teljes repó | forras=git grep '2\.50' @ 6a6c39ab | ts=2026-11-09`

- **Javítva (élő mutató az E34-szakaszra):** `DONTESEK.md:652`, a DT614-sor hivatkozás-oszlopa: `adat/SEMA.md` 2.50 → 2.55 (a meglévő sor szerkesztése, a „Közös koordinációs fájlok” kivétele szerint; a fájl végére nem írtam). Más élő mutató az E34-szakaszra nincs: a kódban, a `.tsv`-fejlécekben, a `.claude/`, a `dontesek/uj/` és a `nyitott/uj/` alatt 0 találat.
- **Helyes, nem változik (a nyílt mag 2.50-es szakaszára mutat):** `DONTESEK.md:649` (DT610), `adat/nyilt_kodkonyv.tsv` és `adat/nyilt_angol.tsv` fejléce, `eszkozok/nyilt_mag_angol.py:37`.
- **Meg nem változtatott történeti mutatók** (az orkesztrátor kivétele, illetve a futáskori állapotot rögzítő napló):
  - `F166_KAROLI_IDEZET_SZABALY_BRIEF.md:17` (`lezarva_osszegzes`) és `:53` (a lezárt brief naplósora);
  - `FELADATOK.md:142` (generált blokk, a lezárt F166 összegzéséből);
  - `F184_DOKU_EGY_FORRAS_BRIEF.md:27` (a brief problémaleírása a #166 esetéről);
  - `naplok/F166_zaras.md:12, 15`; `naplok/ELLENOR_F166.md`, `ELLENOR_F166_2.md`, `ELLENOR_F166_3.md` (az akkori SEMA-állapotról);
  - e jelentés D0-leltára (12. és 31. sor) és az orkesztrátor szó szerint idézett döntése;
  - `NYITOTT_FELADATOK.md:852` (az N-F166a lezárt sora, amely az átszámozást maga írja le).
- **A jelentés pontatlansága:** a D2 „31. sor” bekezdése (és az F184.7 `d0cb8d6c` commit-üzenete) szerint az E34-szakaszra csak történeti szöveg mutatott. Ez nem volt igaz; a bekezdés helyesbítve, a commit-üzenet nem írható át.

## Zárás

- **Elkészült:** D1 (1 sor a `CLAUDE.md`-ben; DT-F184a, DT-F184b), D2 (34 csere: 29 nem-SEMA csere 13 fájlban + 5 SEMA-csere, köztük a DT-F184b 2.48-szövege és a „2.50” szétválasztása; ezen felül az N-F166a lezárása a `NYITOTT_FELADATOK.md` meglévő sorában), D3 (modulszintű táblák, generátor, SEMA 3.11 GENERÁLT blokk, E37), D4 (`/kovetkezo` 10. lépés + 4 kapcsolódó csere, BRIEF_SABLON „Jelentés”), D5 (E36). A D6 (független ellenőr, draft PR) az orkesztrátoré.
- **SEMA-commitok** külön, a többi után: F184.5 `0dfe41a7`, F184.6 `e3114724`, F184.7 `d0cb8d6c`, F184.8 `f26301dc`, F184.10 `ebe7add9` (a blokk újragenerálása az F184.9 után).
- **A CI PR-módú futásának javítása (F184.9 `88d0293b`):** az első futás két, általam okozott HIBA-t talált. (1) E32: a `KAPUK` literáljaiban már kiosztott helyőrzők álltak (DT-F181b/c, DT-F178d/e); ezek helyére a végleges számok kerültek (DT602, DT603, DT645, DT646). (2) E10: az E10 saját leírása a generált blokkban kiváltotta a tiltott-fordítás mintát; a leírást átfogalmaztam.
- **Generált blokk:** `adat/SEMA.md` 3.11, naprakész (`python eszkozok/ellenorzes/szabalyok.py --kapulista --ir` → „naprakész”); E37: 0 találat.
- **Tesztek (2026-11-09):**
  - `python eszkozok/feladatok.py ellenoriz`: 201 brief, 0 hiba, 0 figyelmeztetés;
  - `python eszkozok/teszt_feladatok.py`: 119 teszt, OK;
  - `eszkozok/ellenorzes/tesztek`: `test_szabalyok` 251 (köztük E36Teszt 7, E37Teszt 7), `test_dontes_nezet` 9, `test_szamkiosztas` 14, `test_tanulmany` 32 — mind OK;
  - `python eszkozok/ellenoriz.py` (E1): 0 SÉRTÉS (RENDBEN 27, KÉZI 2, JELENTÉS 14).
  - A `test_szabalyok` 26 E27-tesztje ezen a gépen csak akkor fut le, ha az ideiglenes könyvtár a repóval azonos meghajtón van (`TMP=E:\…`; különben `relpath`-hiba: „path is on mount 'E:', start on mount 'C:'”). Ez környezeti adottság, nem a #184 hatása.
- **CI-futtató PR-módban** (`futtat.py`, base `a0547c03`..HEAD): a javítások után exit 0, HIBA nincs; JELENTÉS-szinten E9 5, E25 3, E27 43, E30 1, E34 41, E36 1 (a SEMA 2.34, N-F184b) — ezek nem a #184 hozzáadott sorain állnak. A futás `--pr-cim "[ELLENŐRZŐ] …"`-tel ment.
- **E16:** a PR az ellenőrzőt módosítja (`szabalyok.py`, `olvasoi_kapu.py`, `ellenorzes.yml`), ezért a PR címe `[ELLENŐRZŐ]` jelölést kíván.
- **Nyitott pontok** (`nyitott/uj/doku-egy-forras.md`):
  - N-F184a: a Feed 9. kapuja még nem ismeri a DT-F184b kivételét (a blokkszintű lapdiff gépi ellenőrzése hiányzik);
  - N-F184b: a SEMA 2.34 kettőzése (az E36 találta; a D0-n kívül esett);
  - N-F184c: a „Kontextus-őrzés” és a `munka` mező szabályainak helye a D1-hez képest (döntés kell);
  - N-F184d: a szintjelölés (SEMA 3.10 ↔ 9-es sablon) mérése.
  - Egyik sem blokkolja a #184 lezárását.
- **Proveniencia:** `scope=F184 D1–D5 | forras=git log 19290a7a..HEAD, a fenti parancsok kimenete | ts=2026-11-09`.
