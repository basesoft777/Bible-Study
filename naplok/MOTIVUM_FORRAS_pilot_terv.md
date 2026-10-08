# MOTIVUM_FORRAS — pilot-terv: a #12 és a #11 1. lépcsőjének bemenetei

*FELADATOK #23 · `F23_MOTIVUM_FORRAS_BRIEF.md` M1/4 · 2026.10.08 · ág: `claude/f23-m1-forrassablon` · döntések: D34, D38, DT28, DT66, DT74 (1)–(3), DT78 (22)*

Ez a fájl a #11 (MIGRACIO) briefjének közvetlen bemenete, és a #12 (TEREMT-002) pilotjáé.
Nem dönt: ahol értelmezés kell, `javaslat` jelölést visel, és a `DONTESEK.md` DT-F23a tétele
dönt róla. Minden szám futtatott parancsból jön; a proveniencia-sor a mérés mellett áll.
A szabályok helye: `sablonok/9_PaRDeS_motivum_forras_sablon.md` (v0, tervezet), `adat/SEMA.md`
3.10, `naplok/MOTIVUM_FORRAS_ci_terv.md` (E28, E29).

## 1. A két pilot és a sorrend

| | #12 — TEREMT-002 | #11 1. lépcső — ISTENTISZT-001 |
|---|---|---|
| fajta | **natív**: nincs régi tanulmány, a forrás eleve `motivumok/TEREMT-002.md` (DT68 (1)) | **örökölt**: a motívumadat ma a prózában (is) áll, a migráció szétválasztás (DT28) |
| mit mér | a forrásból renderelés útját (ma nincs: #64 mérés 1. szakasz, „Renderút nincs”) és a sablon jelölőit | a szétválasztást, a nulla-/elfogadott-diffet az aranymintához, a visszaírás-számlálót |
| aranyminta / referencia | a #64 próza-próbája + a #78 második mintája (`generalt_proba/TEREMT-002_szotari_proba/`) | a #78 váza (`generalt_proba/F78_szerepmatrix_proba/`); kontroll: HAMART-001 (4. szakasz) |
| kimenete | a forrássablon véglegesítése (a `v0` → `v1`) | a migrált ISTENTISZT-001; a befagyasztás oldása (DT74 (3)) |

**Sorrend-eltérés, amelyet a #11 briefje elé kell tenni.** A sablon fejléce szerint „a #12 pilotja
véglegesíti”, a `F12_TEREMT002_PROZA_BRIEF.md` fejléce viszont `fugg: [11]`, tehát a #11 1.
lépcsője a `v0` tervezeten futna. *[javaslat: DT-F23a (13) — (a) a #11 1. lépcsője a `v0`-n fut,
és a #12 a két pilot tapasztalatával véglegesít; vagy (b) a #12 sablon-véglegesítő része (a
renderút és a jelölők) a #11 elé kerül, a `fugg` megfordul. Javaslat: (a), mert a #12 natív
motívuma a szétválasztást nem méri, a sablon pedig mindkét esetre szól.]*

## 2. Közös bemenetek (mindkét pilot)

1. **Forrássablon v0** és a 9. pontjának javaslatai (DT-F23a (1)–(8)).
2. **SEMA 3.10**: a szintek, a jelölőpár, a kinyerés jelölőnként.
3. **A generátor két új képessége** (egyik sincs még meg; a #64 mérés 1. szakasza szerint a
   `general.py` a `motivumok/[ID].md`-ből ma semmit nem olvas):
   - a forrás olvasása szintszűréssel (`olvasoi` / `apparatus` / `belso`), a sablon 4. pontjának
     szakaszlistája mint engedélyezőlista (SEMA 3.10.4);
   - a kinyerés: `JELÖLT` → `jeloltek.tsv`, proveniencia-lábjegyzet → `auditok.tsv`, `ADAT-HIV` /
     `ADAT-ÉRTÉK` ellenőrzés, kinyerési jelentés (SEMA 3.10.5).
   Ezek a #11 (vagy a #12, DT-F23a (13) szerint) implementációs lépései; az E28/E29 implementációja
   külön ágon, előttük (D6).
4. **A mérce** (DT68 (2), DT74 (5)): L1–L7 + a DT2 két rés-szabálya, a szótári részen a #78 váza;
   a forrásra a sablon 8. pontja szerint, a renderre a lexikonoldal-sablon kapuja szerint.
5. **Az arany-készlet eszköze:** `eszkozok/nulladiff.sh` (A/B: két commit generált kimenete, külön
   worktree-ben, azonos `PARDES_DATUM`-mal; `--csere 'régi=>új'` a bájtpontos, előre jóváhagyott
   cseréhez; hatástalan csere végzetes hiba). Az elfogadott-diff kategóriák (5. szakasz) ennek a
   `--csere`-listáját adják.

## 3. A #12-nek: TEREMT-002 (natív)

**Kiinduló állapot** (`scope=motivumok/TEREMT-002.md + adat/{motivumok,elofordulasok,jeloltek,kapcsolatok,auditok,res_forras}.tsv | forras=manual (szkript, split('\t')) | ts=2026-10-08`):

| Elem | Érték |
|---|---|
| `motivumok/TEREMT-002.md` | 239 sor, 38 169 bájt, 10 `##` szakasz, 13 `【NAPLO`, 39 lábjegyzet-definíció |
| ideiglenes jelölők (#64 mérés, sor eleji) | `SZINT` 6, `INAKTÍV` 5, `ADAT-NÉZET` 4 |
| adat | `elofordulasok` 3, `jeloltek` 66, `kapcsolatok` 5, `auditok` 222 sor; `res_forras` **0** sor |
| statusz, ⭐ | `feldolgozás alatt`; `COUNT(DISTINCT fo_elofordulas)` = 3 (a tematikus szakaszok aktívak) |
| szótári rész | a #78 második mintája: `generalt_proba/TEREMT-002_szotari_proba/TEREMT-002_2_SZOTARI_HATTER.md`; a héber 1–2. szerep `adatosítva, nincs bekötve` (a #9 köti be), `lexikon_hivatkozasok` 0 sor |

**Mit kell tudnia a #12-nek:**
1. **Jelölő-átírás a v0 alakra:** a 6 `<!-- SZINT: x -->` → `SZINT-KEZDET`/`SZINT-VÉGE` pár, a
   szakasz alapszintjénél jelölő nélkül (sablon 2. pont); az `INAKTÍV` és az `ADAT-NÉZET` alakja
   változatlan. A számlálás a #64 módszerével (sor eleji jelölő) ismételhető.
2. **`res_forras.tsv`:** 7 sor kell (`id=TEREMT-002`, a hét rés), `forras=tanulmany` helyett a
   forrásra mutató úttal (`tanulmany` = `motivumok/TEREMT-002.md`) vagy `adat` értékkel a
   `minosites` / `alatamasztas` / `2b` résnél (lekepezes: `adat`). Ez adatsor, döntéssel írandó,
   nem kinyerés. A `RÉS` jelölők ma hiányoznak a forrásból (0 db); a #12 teszi be őket.
3. **A renderút:** a lexikonoldal a forrásból, szintszűréssel (`apparatus`); a motívumcikk
   (`apparatus`); az olvasói nézet (`olvasoi`). Mindhárom a `generalt_proba/` alá (DT74 (3)).
4. **Mérés a renderen** (nem csak a forráson, ellentétben a #64-gyel): L1–L7 + DT2; E29 kézi
   futtatása (0 `【NAPLO`, 0 `belso` jelölő az `apparatus` és az `olvasoi` nézetben); E28 kézi
   futtatása (kétszeri generálás azonos `PARDES_DATUM`-mal bájtazonos).
5. **Ismert hiányok (a #64 mérés 4. szakasza):** három „függő” LXX-hely `lxx_dontesek.tsv`-sor
   nélkül; a három előfordulás-sor BDB-mezői üresek; a 7. lépés (nevesített tanító) nem futott.
   Ezek a renderben **explicit hiányként** látszanak (CLAUDE.md 3. szabály), nem pótolandók.
6. **Visszaírás-számláló** (7.4) natív motívumon is: a `motivumok/TEREMT-002.md` diffjében nem
   lehet adatból vagy generált nézetből származó sor. Szétválasztás nincs (nincs régi tanulmány).
7. **A sablon véglegesítése:** a DT-F23a pontjainak tapasztalata a #12 zárójelentésébe, a
   sablon `v1` fejléccel.

## 4. A #11 1. lépcsőjének: ISTENTISZT-001 (örökölt)

### 4.1 A régi források

`scope=a hat fájl | forras=manual (szkript; blokk = üres sorral határolt egység a kódkerítésen kívül, a ## címsor nélkül) | ts=2026-10-08`

| Fájl | Sor | Blokk | `【NAPLO` | `RÉS` |
|---|---|---|---|---|
| `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md` | 602 | 140 | 23 | 6 (kivonat, alatamasztas, miert_fontos, 2b, ertelmezes, modszertan) |
| `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` | 100 | 18 | 0 | 1 (minosites) |
| `motivumok/ISTENTISZT-001.md` | 36 | 8 | 1 | 0 |
| **összesen (a szétválasztás egységei)** | | **166** | **24** | **7** |

A tematikus tanulmány szakaszonként (blokk / `【NAPLO`): Kivonat 7/1 · 0. Forrás-összegyűjtés 3/0 ·
1. Előfordulások 15/7 · 1/b. Kapcsolatok 7/1 · 2. Eredeti nyelvi összevetés (+2/b, Miért fontos)
38/4 · 3. PaRDeS 32/5 · 4. Kutatási sablon 2/0 · 5. Alkalmazás 7/0 · 6. Napló-frissítés (+Módszertan,
Nyitott kérdések, Minőségi kapu) 28/5 · fejléc 1/0.

**Az adatréteg ma** (`split('\t')`, `id=ISTENTISZT-001`): `elofordulasok` 32, `jeloltek` 32,
`kapcsolatok` 25, `res_forras` 7, `auditok` 0 sor; `statusz` `publikálható`, ⭐ csoport 5.
Az `auditok` 0 sora azt jelenti, hogy a módszertani réteg-tábla (Módszertan, „8 ellenőrzési
réteg”) ma csak prózában él: ha `adat`-ba megy, sor- és séma-kérdés (SEMA 3.10.7 3.).

### 4.2 Az aranyminta

A #78 váza szerint rekonstruált lap (DT74 (1)); a #11 1. lépcsőjéig befagyasztott (DT74 (3)):

| Fájl | Sor | Bájt | `GENERÁLT-KEZDET` | `ÜRES-BLOKK` | `【NAPLO` |
|---|---|---|---|---|---|
| `generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md` | 1436 | 119 738 | 10 | 12 | 14 |
| összevetésül: `lexikon/ISTENTISZT-001_TUDOMANYOS.md` (éles, a #78 előtti 2. szakasszal) | 1335 | 115 601 | 10 | 0 | 14 |

*(`scope=a két fájl | forras=manual (szkript) | ts=2026-10-08`.)* A próba-törzscikk
(`…/ISTENTISZT-001_TORZSCIKK.md`) **nem** referencia: az éles `lexikon/`-ból készült (N-F78a), és a
törzscikk a #11-ben megszűnik.

**A pilot célállapota:** a migráció után a `motivumok/ISTENTISZT-001.md`-ből generált lexikonoldal
és az aranyminta között **csak** az 5. szakasz elfogadott kategóriái szerinti eltérés lehet.

### 4.3 A szétválasztás előbecslése (szakaszonként)

A `naplok/MOTIVUM_FORRAS_lekepezes.tsv` besorolásából, a 7. szakasz négy kategóriájával. Ez
előbecslés: a végleges besorolás blokkonként, a #11 leképezési táblájában (7.2) születik.

| Régi szakasz (blokk) | Várható kategória | Cél |
|---|---|---|
| Kivonat (7) | `forras` | sablon K, `RÉS: kivonat`; a `【NAPLO` `forras`/`belso` |
| fejléc verzió-sora (1) | `adat` + `archivum` | `motivumok.tsv` `statusz_verzio`; a verziótörténet archívum |
| 0. Forrás-összegyűjtés (3) | `archivum` (folyamat-nyom) | ha van benne `auditok`-sorrá tehető lekérdezés-nyom: `adat` |
| 1. Előfordulások (15) | `generalt` (a tábla: 32 sor már az adatban) + `forras`/`belso` (P1–P7, `【NAPLO`) | `ADAT-NÉZET` `--cel study` |
| 1/b. Kapcsolatok (7) | `generalt` (a tábla: 25 sor már a `kapcsolatok.tsv`-ben); az Alátámasztás `adat` vagy `forras` | séma-kérdés: SEMA 3.10.7 1. |
| 2. Eredeti nyelvi összevetés (38) | `forras` (értelmezés, Miért fontos) + `adat` (2/b szótári kivonat → `lexikon_hivatkozasok.tsv`) | sablon 2, 2.M; a 2/b blokk megszűnik |
| 3. PaRDeS (32) | `forras` | sablon 3, `RÉS: ertelmezes` |
| 4. Kutatási sablon (2) | `forras` vagy `INAKTÍV` | sablon 4 |
| 5. Alkalmazás (7) | `forras`; a tanítói eredmény a 7. lépés saját fájljába (DT66 (a) 2.) | ha a saját fájl nem létezik: a #11 dönt (a beemelést a DT66 (a) 2. kizárja) |
| 6. Napló-frissítés + Módszertan + Nyitott kérdések + Minőségi kapu (28) | `adat` (státusz), `adat`/`archivum` (réteg-tábla, kapu-eredmény: SEMA 3.10.7 3.), `forras` (tartalmi nyitott kérdés), `archivum` (dátumozott kapu-blokk, önellenőrzés) | 4.4 |
| kereszthivatkozás-napló (18) | `generalt` (a minősítés a `jeloltek.tsv` 32 sorából), `adat` (ha van a táblában nem álló döntés), `archivum` (nyers találatok, módszertan-próza) | séma-kérdés: SEMA 3.10.7 2. |
| `motivumok/ISTENTISZT-001.md` (8) | `archivum` (a négy archív napló-blokk), `generalt` (fejléc), `forras` (a ⭐-bekezdés és a „Kulcsszavak részletesen” értelmező mondatai) | lekepezes, `szetvalasztando` |

### 4.4 A „7. Nyitott kérdések” öt tétele (DT66 (a) 4.)

A sablon 4. pontjának tételenkénti szabálya alkalmazva (*[javaslat: DT-F23a (5)]*):

| # | Tétel (rövidítve) | Jelleg | Kategória |
|---|---|---|---|
| 1 | a 2Móz 33:19/34:5 funkcionális besorolása | séma-korlát (a funkció-készlet nem fedi) | N-tétel; a forrásban `【NAPLO】` mutató |
| 2 | egy versen belüli kontraszt (1Kir 18:24) | séma-korlát (kétpontos modell) | N-tétel; a forrásban `【NAPLO】` mutató |
| 3 | a görög oldal erősítése (a Thayer-pont lezárva) | adatállapot | `archivum` (a lezárt rész), N-tétel, ha maradt nyitott pont |
| 4 | LXX-híd két adatminőségi hibája (áthúzva, lezárva) | lezárt | `archivum` |
| 5 | UBS-besorolás: az ApCsel 9:14 alakja a 11.28-hoz tartozik | tartalmi (exegetikai) | `forras`, 7.N, `apparatus` |

### 4.5 A bővített tanulmányokba visszaírt leletek (DT66 (a) 5.)

Az M0 átfedés-mérése (`naplok/MOTIVUM_FORRAS_atfedes.tsv`, 8 szavas n-gram) a Segítségül-tanulmányra
3 `reszleges`, 15 `rovid_egyezes` és 22 `sablonformula` párt ad; a három `reszleges` pár a
tanulmány 1. sorára (a címsorra) esik, a `genezis/1Moz_12v1-20_bovitett.md` (1 pár) és a
`genezis/1Moz_13v1-18_bovitett.md` (2 pár) felé. A `genezis/` a #11-ben sem
íródik ezen a pilot-terven belül; a #11 dönti el soronként: a visszamutató link `generalt`
(`elofordulasok.tsv` `felmerult_tanulmany`), a visszaírt lelet szövege `archivum`, vagy törlés, ha
a forrásban megvan (DT66 (a) 5.).

## 5. A diff-kategóriák

A migráció kimenetét két összevetés méri, mindkettő `eszkozok/nulladiff.sh`-val (A/B, azonos
`PARDES_DATUM`):

- **ISTENTISZT-001:** az aranyminta (4.2) ↔ a migrált forrásból generált lexikonoldal;
- **HAMART-001** (kontroll, 6. szakasz): a #11 ágának alapja ↔ a feje, a még nem migrált motívumon.

| Kód | Kategória | ISTENTISZT-001 | HAMART-001 | Hogyan engedi át a kapu |
|---|---|---|---|---|
| **N0** | **nulla-diff** | a generált blokkok (1., 1/a, 1/b, 2. szerepmátrix, 3., 4. tábla, 5. tábla, 8., Kolofon) bájtra azonosak, kivéve a D2-t | **a teljes generált kimenet** (lexikonoldal, `naplo`, `index`, `nyitott`, `study`) bájtra azonos | nincs `--csere` |
| D1 | dátum (`ts=`, `Generálva:`) | — | — | nem diff: a `PARDES_DATUM` megszünteti |
| D2 | forrás-útvonal | a lap fejléce (`rések: tematikus_lezart/…` → `motivumok/ISTENTISZT-001.md`), a `res_forras.tsv` `tanulmany`-útja, a Kolofon „Forrás-study” cellája | nem lehet | `--csere`, előre felsorolt literálokkal; a darabszám a jelentésben |
| D3 | `belso`-kihagyás | a lapon ma álló 14 `【NAPLO` kimarad, ha a lexikonoldal `apparatus` nézet (*[javaslat: DT-F23a (10)]*); mindegyiknek a forrásban `belso` blokként kell állnia | nem lehet | blokkonként igazolva: a kimaradt szöveg a `motivumok/ISTENTISZT-001.md`-ben megvan |
| D4 | adatból generált rés | a `minosites`, `2b` (és ha a séma engedi, `alatamasztas`, `modszertan`-tábla) próza helyett adatból renderel | nem lehet | soronként: a régi rés minden igehely + döntés + indoklás eleme megvan a táblában, vagy a leképezési tábla `archivum`-nak jelöli |
| D5 | archivált egység | a leképezési táblában `archivum`-ként jelölt egység eltűnik a nézetből | nem lehet | a leképezési tábla sora a forrás |
| D6 | megszűnt kimenet | a `lexikon/ISTENTISZT-001_TORZSCIKK.md` (D34, N-F78a) | — | a fájl törlése a #11 dolga |
| — | **minden más eltérés** | **ÁLLJ** | **ÁLLJ** | — |

Nem elfogadott (ÁLLJ) például: szakaszsorrend- vagy címváltozás a lexikonoldalon (a `VAZ_SABLON`
kötött), szövegváltozás egy `forras` egység rés-törzsében (a próza bájtra átkerül, csak a
helye változik), új `ÜRES-BLOKK` vagy eltűnt szerep a 2. szakaszban.

## 6. HAMART-001 — a nulla-diff referencia (DT78 (22), ATALAKITASI 11.4)

**Szerepe az 1. lépcsőben:** kontroll. A HAMART-001 az 1. lépcsőben nem migrál; a #11 generátor-
változásai (forrásolvasás, szintszűrés, kinyerés) a még nem migrált motívum kimenetét nem
érinthetik. *[javaslat: DT-F23a (9) — a „nulla-diff referencia” így értve: A/B a generátor két
állapota között, nem a commitolt éles fájlhoz; az éles `lexikon/HAMART-001_TUDOMANYOS.md` a #78
előtti 2. szakaszt viseli, a mai generátor attól eltér, és befagyasztott (DT74 (3)).]*

**Bemenetek** (`scope=a fájlok + adat/*.tsv, id=HAMART-001 | forras=manual (szkript, split('\t')) | ts=2026-10-08`):

| Elem | Érték |
|---|---|
| `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` | 331 sor, 106 blokk, 16 `【NAPLO`, 7 `RÉS` |
| `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` | 276 sor, 46 blokk, 1 `【NAPLO`, 2 `RÉS` |
| `motivumok/HAMART-001.md` | 23 sor, 7 blokk, 1 `【NAPLO` |
| `lexikon/HAMART-001_TUDOMANYOS.md` (éles) | 1275 sor, 116 621 bájt, 10 `GENERÁLT-KEZDET`, 3 `【NAPLO`, 52 lábjegyzet-definíció |
| adat | `elofordulasok` 52, `jeloltek` 52, `kapcsolatok` 0, `res_forras` 7 (`alatamasztas`: `adat`), `auditok` 0; ⭐ csoport 4 |
| átfedés a bővítettel (M0) | 3 `bekezdes_masolat` (a 6:11–13 idézet-bekezdések, `genezis/1Moz_6v9-22_bovitett.md`), 11 `rovid_egyezes` |

**A próba:** `eszkozok/nulladiff.sh <a #11 ágának alapja>` a #11 minden generátort érintő
commitja után; a HAMART-001 összes `general.py` célja (`lexikon`, `naplo`, `index`, `nyitott`,
`study`, `naplok`) — a `torzscikk` nélkül (N-F78a). **Elvárt: üres diff** (N0), `--csere` nélkül.
Amikor a HAMART-001 később migrál, a saját migrációja az ISTENTISZT-001 kategóriáival mérődik
(a 7 `RÉS`-ből a `alatamasztas` már ma `adat`).

## 7. A szétválasztás (DT28)

### 7.1 A négy kategória

A régi tanulmány minden egysége **pontosan egy** célrétegbe kerül:

| Kategória | Mit jelent | Hova | Ellenőrzés |
|---|---|---|---|
| `adat` | a prózában álló motívumadat, amely ma nincs a táblában | a `jeloltek.tsv`-n át, döntéssel (SEMA 3/2, 3.10.5); nem igehely-kulcsú adatnál a döntéssel írt adatút (SEMA 3.10.7 4.) | a sor `manual` provenienciával létezik; a próza nem tartalmazza tovább |
| `forras` | értelmező próza (és a `【NAPLO`, `belso` szinten) | `motivumok/ISTENTISZT-001.md`, a sablon 4. pontja szerinti szakaszba | a szöveg bájtra átkerül (a helye változhat, a szövege nem) |
| `generalt` | ma a forrásban áll, de adatból újraállítható | nem kézi a migráció után; a nézetben a generátor írja | a nézetben a generált változat megvan (N0 vagy D4) |
| `archivum` | sem adat, sem forrás: megőrzött, de nem forrás | archív hely (*[javaslat: DT-F23a (12) — pl. a régi fájl változatlanul, `ARCHÍV` fejléccel egy archív könyvtárban, vagy git-történet + címke]*) | a leképezési táblában jelölve; a nézetből eltűnik (D5) |

**Az egység.** Alapesetben a blokk (üres sorral határolt egység; 4.1: 166 db). A **vegyes blokk**
(adat és értelmezés egy bekezdésben: a lekepezes 19 `szetvalasztando` sora ilyen szakaszokat
jelöl) előbb részegységekre bomlik (mondat, táblasor vagy táblacella), és minden részegység kap
egy kategóriát. *[javaslat: DT-F23a (11)]*

### 7.2 A leképezési tábla (a #11 kimenete)

Javasolt hely: `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv` (a #11 briefje nevezi meg), `split('\t')`
olvasással, oszlopok:

`fajl` · `szakasz` · `blokk` (sorszám a fájlon belül) · `resz` (üres, vagy a részegység sorszáma) ·
`sor_tol` · `sor_ig` · `kategoria` (`adat` / `forras` / `generalt` / `archivum`) · `cel` (adat:
`tábla` + kulcs; forras: sablon-szakasz + szint; generalt: `general.py --cel …`; archivum: hely) ·
`indoklas` · `forras_parancs`.

### 7.3 Sikerfeltételek

1. **Teljesség:** a 166 blokk (és minden részegység) pontosan egy sort kap; sorok száma = egységek
   száma; hiányzó vagy duplikált (`fajl`, `blokk`, `resz`) nincs.
2. **Nincs egység két rétegben:** (a) `forras` egység szövege nem jelenik meg új adatsor
   cellájaként; (b) `adat` egység szövege nem marad a `motivumok/ISTENTISZT-001.md`-ben; (c)
   `generalt` egység szövege nem marad kézi szövegként a forrásban. Mérés: az M0 8 szavas n-gram
   módszere (`naplok/MOTIVUM_FORRAS_M0.py`, átfedés), a sablonformulák kiszűrésével. Elvárt: 0.
3. **A diff** az aranymintához csak N0 és D2–D6 (5. szakasz); a HAMART-001 kontroll üres.
4. **A visszaírás-számláló nulla** (7.4).
5. E28 és E29 zöld a migrált motívumon (ha az implementációjuk addig elkészül; különben kézi
   futtatás, a jelentésben jelölve).

### 7.4 A visszaírás-számláló

**Definíció:** visszaírás minden sor, amely az adatrétegből vagy egy generált nézetből került a
(b) rétegbe (SEMA 3/9: (a)→(b) út nincs). A pilot akkor sikeres, ha a számláló **0**.

**Számolás** a #11 ágán, `git diff <alap>..<fej> -- motivumok/ISTENTISZT-001.md` hozzáadott sorain
(script fájlba írva, `split('\t')`):

1. **Megengedett** a hozzáadott sor, ha (a) az alap-commit régi forrásaiban (4.1 három fájlja)
   szó szerint megvan (áthelyezés); vagy (b) forrás-csak jelölő-sor (`SZINT-*`, `INAKTÍV`,
   `ADAT-NÉZET`, `JELÖLT`, `ADAT-HIV`, `ADAT-ÉRTÉK`, `RÉS-*`, `FORRÁSRÉTEG`); vagy (c) üres sor
   vagy sablon-címsor; vagy (d) új kötőszöveg, amely a leképezési táblában `forras` sorként,
   indoklással szerepel.
2. **Visszaírás (+1)** minden más hozzáadott sor, amelynek szövege (8 szavas n-gram, vagy rövid
   sornál teljes egyezés) az alap-commit `adat/*.tsv` celláiban vagy generált nézeteiben
   (`lexikon/`, a `motivumlog/` generált blokkjai, `generalt_proba/F78_szerepmatrix_proba/`)
   megtalálható.
3. **Visszaírás (+1)** minden generált jelölő a forrásban (`GENERÁLT-KEZDET`, `GENERÁLT-VÉGE`,
   `GENERÁLT:`, `ÜRES-BLOKK`, `ÜRES-NYELV`).
4. A **nem besorolt** hozzáadott sor (sem 1., sem 2.–3.) nem visszaírás, de a jelentésben
   tételesen áll, és a leképezési táblába kell kerülnie, mielőtt a pilot zárul.

A jelentés: a három szám (megengedett, visszaírás, nem besorolt) és a visszaírás-sorok listája.

## 8. A DT-F23a-ba gyűjtött pontok ebből a fájlból

(9) HAMART-001 nulla-diff mint A/B kontroll (6.) · (10) a lexikonoldal `apparatus` nyilvános nézet,
a `【NAPLO` kimarad (5., D3) · (11) vegyes blokk részegységekre bontása (7.1) · (12) az archívum helye
(7.1) · (13) a #11/#12 sorrend és a `v0` sablon (1.) · és a sablonból: (5) a Nyitott kérdések
tételenkénti szabálya, itt az öt tételre alkalmazva (4.4).
