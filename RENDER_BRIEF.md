# RENDER_BRIEF.md — render-átállás: a lexikonoldal és a törzscikk a tematikus tanulmányból

*v5 — 2026.09.23 · jóváhagyva: a §2 G-döntései és a §0/§4 számai · v2 → v3: a rések forrása a tematikus tanulmány (D12); a szótári adatréteg külön briefbe került (`SZOTAR_BRIEF.md`, D13); új szerepmátrix (D14), benne az LXX-híd (D19) és a kiejtés (D20) · v3 → v4: az R0.8 jóváhagyott döntései (G14–G16, D21–D27) · v4 → v5: az R2.6 diff-osztályozó kategórialistája kiegészül (D28)*

**Cél.** A render-elv végrehajtása a 8 kész motívumon: minden a tematikus tanulmányban
készül, a lexikonoldal (`_TUDOMANYOS.md`) és a kereszthivatkozási törzscikk
(`_TORZSCIKK.md`) abból renderel. A 8 lexikonoldalas motívum mind a 8 tematikus
tanulmánya kész (`adat/motivumok.tsv` `forras_study`, 1:1), ezért a 7 helyőrzős oldal
réseit a tanulmányból töltjük, nem külön kutatói munkával. A brief végén mind a 8
lexikonoldal helyőrző nélküli, és a 8 törzscikk elkészült.

**Szerkezet.** R0 (kész) → R0.8 kiegészítő felmérés ⛔ → 1. menet: nulla-diff ⛔ →
2. menet: kimenet-változtató, egy belső ⛔-vel (kivonatok jóváhagyása).

**Modell:** Sonnet. **Push csak külön kérésre.**

**Nincs benne** (→ `SZOTAR_BRIEF.md`, a RENDER lezárása után): fordítási gyorsítótár,
terminológia, kiejtés és átírás, TBESH, UBS DBH-import, Mounce/SECE, Cremer, Girdlestone,
BDB-etimológia, az ISTENTISZT-001 2/b Mounce/SECE-tábláinak kiváltása. Továbbra sincs
benne: fordítási pipeline, BDB SQLite-csere, héber gépi kiejtés, a LEXV2_3 többi tétele.

---

## 0. Kiindulás *(az R0.8.1 újraméri; eltérésnél ÁLLJ)*

Az R0 (R0.1–R0.7) lefutott, élő adatba nem írt (K3). A 0.7, 0.8, 0.10–0.12 sor a
`SZOTAR_BRIEF.md` §0-jába került.

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `origin/main` a `main` őse, divergencia nélkül (D25) | `origin/main` = `f840330` (az R0.8 után) |
| 0.2 | `ellenoriz.py` összesítő | RENDBEN 8 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 1, kód 0 |
| 0.3 | `general.py --cel lexikon --ellenoriz` | 8/8 „változatlan lenne" |
| 0.4 | lexikonoldalak | 8 (`lexikon/*_TUDOMANYOS.md`), mind 10 generált blokkal |
| 0.5 | kézi szöveg a blokkokon kívül | ISTENTISZT-001: 37 222 karakter; a másik 7: 995–1 033 karakter, oldalanként 8 „Kézzel írandó" helyőrző |
| 0.6 | a 7 helyőrzős oldal eltérése a mai `VAZ_SABLON`-tól | a 6. és 7. szakasz régebbi helyőrző-szerkezete; a 2/b fejléce `### 2/b *(kézi, ha van)*` (az ISTENTISZT-001-é `### 2/b. Kiegészítő szótári adatok *(kézi)*`) |
| 0.9 | `motivumok/*.md` (napló-forrásréteg) | 8 fájl — a lexikonoldal kézi szövegét nem tartalmazzák |
| 0.13 | törzscikk-pilot (`motivumlog/lexikon_pilot/ISTENTISZT-001_TORZSCIKK.md`) | 32 igehely (22 ÓSZ / 10 ÚSZ) · 25 kapcsolat · 22 LXX-sor · 106 kereszthivatkozás · 0 üzemeltetési elem; a `torzscikk_pilot.py` a mai lexikonoldalból reprodukálja. **Kiindulási alap, nem célállapot:** az 5. szakasza és a lábléce a G6/G7 szerint változik |
| 0.14 | tematikus tanulmányok | 8 (`tematikus_lezart/*_tematikus.md`), motívumonként 1, a `forras_study` szerint; a 4. sablon szerkezete (0–6. pont), kivonat egyikben sincs |
| 0.15 | ISTENTISZT-001: tanulmány vs. lexikonoldal | a lexikonoldal jár előrébb (17/15 → 22/18; a D-minta görög folytatása csak a lexikonoldalon) |
| 0.16 | R0 munkalapok | `naplok/RENDER_R0_resek.tsv` (56 sor, fejlécsorokkal), `RENDER_R0_jelentes.md` és a többi (a SZOTAR használja) |

---

## 1. Fogalmak

- **Rés:** a lexikonoldal egy kézi szakasza. Hét rögzített rés van, a `VAZ_SABLON`
  sorrendjében: `kivonat`, `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`,
  `modszertan`. Határai az R0.2 szerint (fejlécsortól a következő rés-fejlécig, generált
  markerig vagy váz-fejlécig).
- **Tanulmány-rés:** a tematikus tanulmányban `<!-- RÉS-KEZDET: [rés] -->` … `<!-- RÉS-VÉGE: [rés] -->`
  jelölők közé zárt szöveg. Ez a rés **törzse**; a fejlécsor nem része.
- **Megfeleltetési tábla:** `adat/res_forras.tsv` — motívumonként és résenként megmondja a rés
  fejlécsorát és a forrását (`tanulmany` vagy átmenetileg `lap`).
- **Nulla-diff:** az `--ir` futás után `git status --porcelain lexikon/` üres — bájtra, `ts=` értékekkel együtt.

---

## 2. G-döntések *(jóváhagyva)*

| # | Kérdés | Döntés |
|---|---|---|
| G1 | Hol élnek a rések? | **A motívum tematikus tanulmányában** (`forras_study` első eleme), tanulmány-résként. Új kézi réteg nem készül (a v2 `motivumok/lexikon/` javaslata elvetve, D12). |
| G2 | Hogyan áll össze egy rés? | **Fejlécsor a megfeleltetési táblából + törzs a tanulmányból.** A `fejlec` induló értéke az R0.2 fejlécsora, így a 7 oldal régi fejlécei és az ISTENTISZT-001 eltérő 2/b-fejléce is nulla-diff. Egy rés több tanulmány-szakaszból is állhat: azonos nevű jelölőpárok, dokumentum-sorrendben, egy üres sorral összefűzve. |
| G3 | Nulla-diff mérce | Bájtazonosság `ts=` értékekkel együtt; változatlan blokk fejléce nem íródik újra. |
| G4 | Szerkeszthetőség | **A lexikonoldal kézzel nem szerkeszthető**; a rés csak a tanulmányban javítható. Az `ellenoriz.py` 11. szakasza sértésnek jelzi, ha a lap rése eltér a táblából + tanulmányból összeállítottól. A `CLAUDE.md` és a `MUNKAMENET.md` ezt rögzíti. |
| G5 | Belső adatmodell | `modell_epit(m, …)` → egy szótár (a 10 blokk adatai + a 7 rés + a szerepmátrix); a `_TUDOMANYOS` és a `_TORZSCIKK` render ebből dolgozik, a blokk-építők logikája nem változik. |
| G6 | Szerepmátrix | **`adat/szotar_szerepek.tsv`** (`nyelv`, `sorrend`, `szerep`, `forras`, `allapot`), 10 szerep × 2 nyelv = **20 sor**, az alábbi táblával; `allapot` = `adatosítva` / `nincs adatosítva`. A pilot D6-ját váltja fel (D14). |
| G7 | Törzscikk | `lexikon/[ID]_TORZSCIKK.md` mind a 8 motívumra; `general.py --cel torzscikk` (élesíthető); sablon `sablonok/8_PaRDeS_torzscikk_sablon.md`. A pilot döntései közül **D1–D5, D7–D11, D13 érvényes; a D6-ot a G6 váltja fel; a D12 (lábléc) a ténylegesen használt forrásokra szűkül, az új források megjelölése a SZOTAR-ban.** Az 5. szakasz két mátrixa: szerepek (G6) és lefedettség szavanként (a modellből); a cella értéke: forrás-hivatkozás, `kézi (2/b)` vagy `nincs adatosítva`. A helyőrző és a `【NAPLO: …】` blokk kimarad. A 2/b rés egyben jelenik meg „Kiegészítő szótári adatok" címmel (v2 D7). |
| G8 | ISTENTISZT-001 visszaírás | **A lexikonoldal rései felváltják a tanulmány megfeleltetett szakaszait** (ez a G13-as study-frissítés); a régi szöveg a git-történetben marad. A felváltandó szakaszokat az R0.8.5 tételesen listázza, jóváhagyásra. A kivonat új `## Kivonat` szakaszként kerül a tanulmány elejére. |
| G9 | A 7 tanulmány | **A jelölők a meglévő szöveg köré kerülnek, a szöveg nem változik**, kivéve: (a) az R0.8.4-ben jóváhagyott elavult számok javítása; (b) az új kivonat (G10); (c) hiányzó rés jóváhagyott kezelése — pótlás a tanulmányban, vagy a jelölők közt egyetlen sor: *„A tematikus tanulmány ezt a részt nem tárgyalja."* |
| G10 | Kivonat | 3–5 mondat (a mai helyőrző előírása szerint). A 7 tanulmányba a 2. menet írja tervezetként; **⛔ jóváhagyás a commit előtt.** |
| G11 | 2/b fejléc | A 2. menetben a 8 motívum `fejlec` értéke egységesen `### 2/b. Kiegészítő szótári adatok *(kézi)*` (R0 7. szakasz, 3. kérdés). |
| G12 | Átmeneti forrás | Az 1. menetben csak az ISTENTISZT-001 rései `tanulmany` forrásúak, a 7 oldal rései `lap` (a lap mai rése, változatlanul). A 2. menet végén `lap` sor nincs. Az `ellenoriz.py` 12. szakasza a `lap` sorok számát jelenti. |
| G13 | A 3 tartalmi NAPLO-blokk (ISTENTISZT-001) | Az 1. menetben maradnak. A study-frissítésről szóló blokk (a lexikonoldal ~1041. sora, *„a tematikus study 3. pontja még 17 ószövetségi igehelyről…"*, az `ertelmezes` résben; D24) a 2. menetben lezárul, mert a G8 teljesíti; a másik kettő marad (a lexikonoldalon látszik, a törzscikkből kimarad). |
| G14 | `minosites` forrása | **A motívum kereszthivatkozás-naplója** (`tematikus_lezart/naplok/*_kereszthivatkozas_naplo.md`), a „Tartalmi minősítés minden jelöltre" és a „Végső döntés és indoklás" szakasz (D21). A `res_forras.tsv` `tanulmany` oszlopa ilyenkor a napló útvonalát tartja. Lefedettség 7/8; az ANTROP-001-nek nincs naplója — a rés a tanulmányban, jelölők közt egy sort kap: *„A kereszthivatkozás-minősítés ennél a motívumnál nem készült el."*, és új NYITOTT-tétel. ISTENTISZT-001: a lexikonrés a napló minősítő szakaszát váltja fel; ha nincs ilyen, új szakasz a napló végén. |
| G15 | `2b` | **ISTENTISZT-001:** az 1. menetben egyben, új szakaszként a tanulmány „2. Eredeti nyelvi összevetés" szakasza után (D22); a SZOTAR S12 később szétbontja. **A többi 7:** TEREMT-001 (2/b + 2/c) és ALVIL-001 (2/b) a meglévő szakaszt kapja; a másik 5 tanulmányban a jelölők közt egy sor: *„Nincs kiegészítő szótári adat."* |
| G16 | `alatamasztas` | Forrás `adat` (új `forras` érték): ahol a motívumnak 0 kapcsolata van (`adat/kapcsolatok.tsv`; 6 motívum), a generátor adatból írja: *„A motívumhoz nincs rögzített kapcsolat."* (D26). ISTENTISZT-001 (25 kapcsolat): a lexikonrés felváltja a tanulmány „1/b. Kapcsolatok" szakaszát. KIRALY-001 (9 kapcsolat): a forrást a 2. menet javasolja (várhatóan a napló „Végső döntés és indoklás" szakasza), jóváhagyás az R2.2 ⛔-nél. |

**G6 — a szerepmátrix tartalma:**

| Szerep | Görög | Héber |
|---|---|---|
| Alapjelentés | TBESG | TBESH |
| Mélységi szócikk | Thayer | BDB |
| Teológiai szócikk | Cremer (1895) | Girdlestone (1897) + Cremer héber mutatója; TWOT-szám hivatkozásként |
| Jelentésszerkezet, szemantikai mező | UBS DNTG (Louw–Nida) | UBS DBH (SDBH) |
| Tömör jelentés, előfordulás | UBS DNTG glossza + referencia-szám; Mounce kiegészítő | UBS DBH glossza + referencia-szám |
| LXX-híd (korpusz, a motívum igehelyein) | az ÚSZ-szó LXX-háttere: mely héber szavakat ad vissza, mely versekben (`lekerdez.py lxx-hid`, `LXX_OS`) | LXX-fordítói döntés versenként: mely görög szó adja vissza (`LXX_OS` + `adat/lxx_dontesek.tsv`; a lexikonoldal 3. szakasza) |
| Megfelelők a másik nyelven (szótári lista) | SECE (héber) | SECE (görög) |
| Nyelvi háttér | LSJ, ha releváns | BDB etimológia |
| Versenkénti jelentés | UBS DNTG (szópozícióig) | UBS DBH |
| Kiejtés (magyaros) | `kiejtes.py` szabálytábla | lemma: `kiejtes_kivetelek.tsv` (kézi, OSHL-alapú jelöltekből); alak: STEP-átírás, változatlanul |

A RENDER végén `adatosítva`: TBESG, TBESH, Thayer, BDB, UBS DNTG (a meglévő import), SDBH
domének, LSJ, LXX-híd (mindkét irány). A többi `nincs adatosítva`; ezeket a SZOTAR tölti.

---

## 3. Tételek

### R0 — felmérés *(kész: R0.1–R0.7, `d0a5aa1`)*

### R0.8 — kiegészítő felmérés *(csak olvas; egy commit)* ⛔

- **R0.8.1** `main` = `origin/main` = e brief commitja; a §0 0.2–0.4 sora újramérve. Eltérésnél **ÁLLJ**.
- **R0.8.2** A 8 tanulmány szakasz-leltára: minden `#`–`###` fejléc, bájtméret. `naplok/RENDER_R08_szakaszok.tsv`.
- **R0.8.3** Megfeleltetési javaslat, 8 × 7 = 56 sor: `id`, `res`, `fejlec` (R0.2), `tanulmany_szakaszok` (fejlécek, sorrendben), `hiany` (igen/nem), `megjegyzes`. Kiinduló hipotézis, amelyet a leltár igazol vagy cáfol:

  | Rés | Tanulmány-szakasz (hipotézis) |
  |---|---|
  | `kivonat` | nincs — új szakasz (G10) |
  | `2b` | 2/b, 2/c, ahol van |
  | `miert_fontos` | 2. Eredeti nyelvi összevetés |
  | `minosites` | a kereszthivatkozások minősítése (ahol a tanulmány tárgyalja) |
  | `alatamasztas` | 1/b Kapcsolatok |
  | `ertelmezes` | 3. PaRDeS + ⚠️ Vitatott pontok |
  | `modszertan` | 0. Forrás-összegyűjtés + 6. Napló-frissítés + Minőségi kapu |

  `naplok/RENDER_R08_megfeleltetes.tsv`.
- **R0.8.4** Elavult számok a tanulmányok prózájában: minden igehely-, előfordulás- és kapcsolatszám, összevetve az `adat/*.tsv` mai értékével (`tanulmany`, `sor`, `szoveg`, `tanulmany_ertek`, `adat_ertek`). `naplok/RENDER_R08_szamok.tsv`.
- **R0.8.5** ISTENTISZT-001 visszaírási terv: résenként melyik tanulmány-szakasz törzsét váltja fel. `naplok/RENDER_R08_visszairas.tsv`.
- **R0.8.6** Jelentés: `naplok/RENDER_R08_jelentes.md` — a mérések, a hiányzó rések listája, és **egy csokorban** minden kérdés. **ÁLLJ.** A megfeleltetés, a számjavítások és a visszaírási terv jóváhagyás után válik érvényessé.

### 1. menet — nulla-diff

- **R1.1** `adat/res_forras.tsv` (`id`, `res`, `fejlec`, `forras`, `tanulmany`), 56 sor: ISTENTISZT-001 7 sora `tanulmany`, a többi 49 `lap`. SEMA-bejegyzés.
- **R1.2** ISTENTISZT-001 tanulmány és kereszthivatkozás-napló: visszaírás a jóváhagyott R0.8.5 szerint, a G14–G16 és a D23 módosításaival (`minosites` → a napló; `2b` → új szakasz a 2. után; `modszertan` → csak a „6. Napló-frissítés" helyére, a 0. szakasz és a Minőségi kapu jelölő nélkül, változatlanul), jelölőkkel; új `## Kivonat` szakasz a lexikonoldal kivonatával (G8).
- **R1.3** `lexikon_general.py`: a rések a tábla szerint (`tanulmany`: fejléc + jelölt törzs; `lap`: a lap mai rése). Hiányzó jelölő vagy tábla-sor: hibakód, nem helyőrző.
- **R1.4** Belső adatmodell (G5): `modell_epit()`.
- **R1.5** `adat/szotar_szerepek.tsv` (G6), 20 sor; SEMA-bejegyzés.
- **R1.6** `ellenoriz.py`: **11.** lap rése ≡ tábla + tanulmány (eltérés = SÉRTÉS); **12.** `lap` forrású sorok száma (JELENTÉS).
- **R1.7** Törzscikk (G7): sablon 8, `--cel torzscikk`, 8 fájl. Az ISTENTISZT-001 törzscikke a pilottól csak az 5. szakaszban és a láblécben tér el; a diff ezt igazolja (`naplok/RENDER_R1_pilot_diff.tsv`).
- **R1.8** Dokumentáció: `CLAUDE.md` (a rések csak a tanulmányban szerkeszthetők; a lexikonoldal és a `_TORZSCIKK` generált), `MUNKAMENET.md` (C2: a tanulmányban; C1 és a törzscikk: render), `adat/SEMA.md`, `NYITOTT_FELADATOK.md`. **ÁLLJ.**

### 2. menet — kimenet-változtató, elvárt diffel

- **R2.1** A 7 tanulmány és 6 kereszthivatkozás-napló: jelölők a jóváhagyott megfeleltetés és a G14–G16 szerint; elavult szám-javítás nincs (R0.8.4: 0 tétel, D27); a hiányzó rések jóváhagyott kezelése (G9).
- **R2.2** Kivonat-tervezetek a 7 tanulmány elejére (G10) és a KIRALY-001 `alatamasztas` forrásjavaslata (G16). **ÁLLJ — jóváhagyás**, utána commit.
- **R2.3** `res_forras.tsv`: a 49 `lap` sor → `tanulmany`; a 2/b `fejlec` egységesítése (G11).
- **R2.4** Az ISTENTISZT-001 study-frissítési NAPLO-blokkjának lezárása (G13).
- **R2.5** A lexikonoldal első sora elé gépi jelölés: `<!-- GENERÁLT: general.py --cel lexikon | rések: [forras_study] -->`.
- **R2.6** Újragenerálás (`lexikon` és `torzscikk`), majd diff-osztályozó (`eszkozok/render_diff_osztalyoz.py`): minden változott sor egy kategóriába esik — `tanulmany`, `kivonat`, `fejlec`, `naplo`, `jeloles`, `torzscikk_res`, `adat_res` (D28). Ismeretlen kategória: **ÁLLJ**; `adat_res` esetén pontosan 7 sor várt (motívumonként egy, mind `alatamasztas`), eltérésnél **ÁLLJ**.
- **R2.7** Lezárás: `NYITOTT_FELADATOK.md` (következő: `SZOTAR_BRIEF.md`), `MUNKAMENET.md`.

---

## 4. Várt számok

| Menet | Mérés | Várt |
|---|---|---|
| R0.8 | szakasz-leltár | 8 tanulmány |
| R0.8 | megfeleltetési javaslat | 56 sor (8 × 7); a `kivonat` 8 sora `hiany=igen` |
| 1 | `--cel lexikon --ir` után `git status --porcelain lexikon/*_TUDOMANYOS.md` | üres |
| 1 | `adat/res_forras.tsv` | 56 sor: `tanulmany` 7, `lap` 49 |
| 1 | `adat/szotar_szerepek.tsv` | 20 sor |
| 1 | `ellenoriz.py` | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 (a 12. szakasz 49 `lap` sort jelent), kód 0 |
| 1 | `lexikon/*_TORZSCIKK.md` | 8 fájl; ISTENTISZT-001: 32 (22/10) · 25 · 22 · 106, üzemeltetési elem 0, helyőrző 0; pilot-diff csak az 5. szakaszban és a láblécben |
| 2 | `res_forras.tsv` | `lap` 0; `adat` 6 (`alatamasztas`, 0 kapcsolat); `tanulmany` 50, ebből `minosites` 7 a kereszthivatkozás-naplóból |
| 2 | `Kézzel írandó` a 8 lexikonoldalon | 0 |
| 2 | `## Kivonat` a 8 tanulmányban | 8 |
| 2 | diff-osztályozó | ismeretlen kategória: 0 |
| 2 | `ellenoriz.py` | SÉRTÉS 0, kód 0; a 12. szakasz: 0 `lap` sor |

---

## 5. Elfogadási kritériumok

### R0 *(teljesült: K1–K3)*

### R0.8
| # | Kritérium |
|---|---|
| K4 | a négy munkalap és a jelentés megvan; a kérdések egy listában |
| K5 | az éles `adat/`, `lexikon/`, `motivumok/`, `tematikus_lezart/` bájtra változatlan |

### 1. menet
| # | Kritérium |
|---|---|
| K6 | nulla-diff: `git status --porcelain lexikon/*_TUDOMANYOS.md` üres |
| K7 | az `ellenoriz.py` 11. szakasza RENDBEN; a 12. a §4 szerint |
| K8 | az ISTENTISZT-001 tanulmányában mind a 7 rés jelölve (a `kivonat` az új `## Kivonat` szakaszban); a felváltott szakaszok az R0.8.5 szerint |
| K9 | a 8 törzscikk megvan; az ISTENTISZT-001 számai a §4 szerint; `grep -c` a törzscikkekben: `GENERÁLT` 0, `【NAPLO` 0, `proveniencia:` 0, `Kézzel írandó` 0; a pilot-diff csak az 5. szakaszt és a láblécet érinti |
| K10 | TSV-kezelés `csv` modul nélkül; import, nem másolás (`general`, `lekerdez`) |
| K11 | commitok a §6 szerint; `git status --porcelain` üres |

### 2. menet
| # | Kritérium |
|---|---|
| K12 | a kivonatok csak jóváhagyás után kerültek commitba |
| K13 | diff-osztályozó: ismeretlen kategória 0; a kategóriák darabszáma jelentve |
| K14 | a 7 tanulmányban és a kereszthivatkozás-naplókban a jelölőkön, a kivonaton, a G14–G15 egysoros bejegyzésein és a jóváhagyott pótlásokon kívül nincs változás (`git diff` a tanulmányokon, kategóriánként) |
| K15 | `ellenoriz.py` a §4 szerint; a törzscikkek újragenerálva, K9 ismét teljesül |
| K16 | commitok a §6 szerint; `git status --porcelain` üres |

---

## 6. Commitok

**R0.8**
| Üzenet | Fájlok |
|---|---|
| `RENDER_BRIEF.md v3` | `RENDER_BRIEF.md` |
| `SZOTAR_BRIEF.md v1` | `SZOTAR_BRIEF.md` |
| `R0.8: tanulmány-leltár, megfeleltetés, elavult számok, visszaírási terv` | `naplok/RENDER_R08_*.tsv`, `naplok/RENDER_R08_jelentes.md` |

**1. menet**
| Üzenet | Fájlok |
|---|---|
| `RENDER_BRIEF.md v4` | `RENDER_BRIEF.md` |
| `R1.1–R1.2: megfeleltetési tábla, ISTENTISZT-001 visszaírás a tanulmányba` | `adat/res_forras.tsv`, `adat/SEMA.md`, `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` |
| `R1.3–R1.5: generátor a tanulmányból, belső adatmodell, szerepmátrix (nulla-diff)` | `eszkozok/lexikon_general.py`, `eszkozok/general.py`, `adat/szotar_szerepek.tsv`, `adat/SEMA.md` |
| `R1.6: ellenőrző 11–12. szakasz` | `eszkozok/ellenoriz.py` |
| `R1.7: kereszthivatkozási törzscikk (8. sablon, --cel torzscikk)` | `sablonok/8_PaRDeS_torzscikk_sablon.md`, `eszkozok/torzscikk_general.py`, `eszkozok/general.py`, `lexikon/*_TORZSCIKK.md`, `naplok/RENDER_R1_pilot_diff.tsv` |
| `R1.8: dokumentáció` | `CLAUDE.md`, `MUNKAMENET.md`, `NYITOTT_FELADATOK.md` |

**2. menet**
| Üzenet | Fájlok |
|---|---|
| `R2.1: a 7 tanulmány és a naplók résjelölése` | `tematikus_lezart/*_tematikus.md` (7), `tematikus_lezart/naplok/*_kereszthivatkozas_naplo.md` (6) |
| `R2.2: kivonatok a 7 tanulmányban (jóváhagyva)` | `tematikus_lezart/*_tematikus.md` (7) |
| `R2.3–R2.5: forrás = tanulmány mind a 8-nál, 2/b fejléc, NAPLO-lezárás, GENERÁLT-fejléc` | `adat/res_forras.tsv`, `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, `eszkozok/lexikon_general.py`, `lexikon/*` |
| `R2.6–R2.7: diff-osztályozó és lezárás` | `eszkozok/render_diff_osztalyoz.py`, `naplok/RENDER_R2_diff.tsv`, `NYITOTT_FELADATOK.md`, `MUNKAMENET.md` |

---

## 7. Nyitó promptok *(Sonnet)*

### R0.8
```
Olvasd el a CLAUDE.md-t, a RENDER_BRIEF.md-t (v3) teljes egészében és a
naplok/RENDER_R0_jelentes.md-t.

0. Commitold: "RENDER_BRIEF.md v3" és "SZOTAR_BRIEF.md v1" (a §6 R0.8-táblája szerint).
1. R0.8.1: main = origin/main = az imént készült commit; a §0 0.2–0.4 sorát mérd újra.
   Ha bármi eltér, ÁLLJ MEG és jelents.
2. R0.8.2–R0.8.5 a §3 szerint. Az éles adat/, lexikon/, motivumok/, tematikus_lezart/
   könyvtárba NE írj.
3. R0.8.6: jelentés, a hiányzó rések és a kérdések egy listában. Commit a §6 szerint. K4–K5.
4. ÁLLJ.
```

### 1. menet
```
Olvasd el a CLAUDE.md-t, a RENDER_BRIEF.md-t (v4) és a naplok/RENDER_R08_jelentes.md-t,
valamint az R0.8 munkalapokat. Ahol a munkalap és a v4 G14–G16 / D21–D27 eltér,
a v4 érvényes.

0. main = origin/main = f840330. Ha nem, ÁLLJ MEG. Commitold: "RENDER_BRIEF.md v4".
1. R1.1–R1.3. Utána: general.py --cel lexikon --ir, majd git status --porcelain
   lexikon/*_TUDOMANYOS.md — ha nem üres, ÁLLJ MEG, és ne commitolj.
2. R1.4–R1.8 a §3 szerint, minden tétel után újra a nulla-diff próba.
3. K6–K11. Commitok a §6 1. menet-táblája szerint.
4. ÁLLJ.
```

### 2. menet
```
Olvasd el a CLAUDE.md-t és a RENDER_BRIEF.md-t (v4).

0. main = origin/main = <az 1. menet utáni hash>. Ha nem, ÁLLJ MEG.
1. R2.1, commit.
2. R2.2: a 7 kivonat-tervezetet írd meg, mutasd be egyben, és ÁLLJ MEG jóváhagyásra.
   Jóváhagyás után commit.
3. R2.3–R2.5, majd R2.6: ha a diff-osztályozó ismeretlen kategóriát talál, ÁLLJ MEG.
4. R2.7. K12–K16. Commitok a §6 2. menet-táblája szerint.
5. ÁLLJ.
```

---

## 8. Döntésnapló

| # | Döntés | Indoklás |
|---|---|---|
| D1 | Egy brief, szakaszokra bontva, független ellenőrzési megállásokkal | kevesebb brief, a kérdések egy csokorban |
| D2 | Az 1. menet nulla-diff — *v3: a szótári tételek (gyorsítótár, új táblák, kiejtés) a SZOTAR-ba kerültek (D13)* | a szerkezeti átállás tartalmi változás nélkül, bájtra ellenőrizhető |
| D3 | A kimenet-változtató tételek a 2. menetben, diff-osztályozóval | ismeretlen változás = megállás |
| D4 | A rés fejlécsora szó szerint megőrződik — *v3: a megfeleltetési tábla `fejlec` mezőjében (G2)* | a 7 oldal régi fejlécei és az ISTENTISZT eltérő 2/b-fejléce nulla-diff marad |
| D5 | ~~A 7 helyőrzős oldal rései a helyőrzőt hordozzák, a C2 a forrásrétegben tölti ki~~ — *v3: felváltja a D12* | — |
| D6 | Héber gépi kiejtés nincs — *v3: a SZOTAR-ban* | svá, dagesh, qamets qatan |
| D7 | A törzscikk a 2/b rést egyben mutatja; a szétosztás a forrásban történik — *v3: a SZOTAR S12-je végzi, a tanulmányban* | a render nem értelmez szabad prózát |
| D8 | Kizárva: fordítási pipeline, BDB SQLite-csere, héber gépi kiejtés, a LEXV2_3 többi tétele — *v3: a C2 már nincs kizárva, a 7 oldal C2-je a tanulmányból jön* | külön kockázat |
| D9 | A diff-osztályozó és a nulla-diff próba minden tétel után fut | a csendes sorvesztés tanulsága |
| D10 | A törzscikk-pilot a v2-vel verzióba került (`motivumlog/lexikon_pilot/`) | chatben készült artifact csak commit után hivatkozható |
| D11 | A rés-mérés blokkhatár-pontos, nem soronkénti | a soronkénti mérés a 0.5-nél 9 karakterrel tévedett |
| D12 | **v3: a rések forrása a tematikus tanulmány**, jelölők közt; a v2 `motivumok/lexikon/` rétege elvetve | a render-elv (minden a tanulmányban készül); a 8 motívum tanulmánya kész, 1:1; harmadik kézi réteg ellentmondana az elvnek |
| D13 | **v3: kettéválás** — a szótári adatréteg a `SZOTAR_BRIEF.md`-be került (v2 G6–G8, G11, G12, R1.4–R1.6, az ellenőrző 12–13. szakasza, R2.1–R2.4) | a 8 oldal gyors lezárása; a TBESH-átállás feltétele nem teljesült (R0 jelentés, 7.1), ez nem tarthatja fel a lezárást |
| D14 | **v3: új, kétoldalú szerepmátrix** (G6); a pilot D6-ja felváltva | minden szerepnek görög és héber forrása van: TBESG/TBESH, Thayer/BDB, Cremer/Girdlestone, UBS DNTG/UBS DBH, LSJ/BDB-etimológia; a TAHOT és az OSHL kiesett |
| D15 | **v3: az ISTENTISZT-001 lexikonrései felváltják a tanulmány megfeleltetett szakaszait** | a lexikonoldal az újabb (22/18); ez teljesíti a G13-as study-frissítést |
| D16 | **v3: a kivonatokat a 2. menet írja, jóváhagyással** | egyik tanulmányban sincs kivonat; a tartalom a tanulmányból adott, a kivonat szerkesztői munka |
| D17 | **v3: az R0 jelentés kérdései** — 3. (2/b fejléc) → G11; 1., 2., 4. (TBESH, átírás-mérce, kiejtés-tesztkészlet) → SZOTAR | a kettéválás szerint |
| D18 | **v3: a törzscikk-pilot kiindulási alap, nem célállapot**; az R1.7 a pilottól csak az 5. szakaszban és a láblécben térhet el | a szerepmátrix változott (D14); a 0.13 számai nem az 5. szakaszból jönnek |
| D19 | **v3: az LXX-híd önálló szerep a mátrixban**, mindkét irányban; a SECE sora „szótári lista" lett | a projekt módszerének gerince; a SECE a teljes megfelelő-listát adja gyakoriság és igehely nélkül, az LXX-híd a motívum tényleges verseiben mutatja a fordítói döntést; már adatosítva (`LXX_OS`, CC BY 4.0, és `adat/lxx_dontesek.tsv`) |
| D20 | **v3: a kiejtés (magyaros) önálló szerep a mátrixban**; 10 szerep × 2 nyelv = 20 sor | a szó megjelenítésének szerepe; görögül szabálytábla, héberül kézi kivételtábla OSHL-alapú jelöltekből (SZOTAR S3); a render héber kiejtést továbbra sem generál (v2 D6) |
| D21 | **v4: a `minosites` forrása a kereszthivatkozás-napló** (G14) | az R0.8 csak a tanulmányfájlt vizsgálta; a `tematikus_lezart/naplok/` 7 naplója pontosan a jelöltenkénti minősítést és indoklást hordozza. Az ANTROP-001 hiánya valós C2-hiány, jelölve és NYITOTT-tételként |
| D22 | **v4: az ISTENTISZT-001 2/b rése az 1. menetben egyben kerül a tanulmányba, a 2. szakasz után** (G15) | a nulla-diff csak a RENDER 1. menetére vonatkozik; a SZOTAR S12 saját elvárt diffel, `tanulmany` kategóriában bontja szét. A 2/b a vázban „ha van" — az 5 üres tanulmányban egy sor jelzi |
| D23 | **v4: az ISTENTISZT-001 `modszertan` rése csak a „6. Napló-frissítés" szakaszt váltja fel**; a 0. szakasz és a Minőségi kapu jelölő nélkül marad | egy tömb nem bontható gépileg három szakaszra; a 7 másik motívumnál marad a háromszegmenses összeállítás, fejléc szerinti illesztéssel (R0.8 4. kérdés) |
| D24 | **v4: a G13 study-frissítési NAPLO-blokkja azonosítva** (a lexikonoldal ~1041. sora, `ertelmezes`) | a visszaírás után a tanulmány 3. pontja friss, a blokk elavul, a 2. menet törli |
| D25 | **v4: a §0 0.1 mércéje: `origin/main` a `main` őse, divergencia nélkül** | a push csak kérésre történik, ezért a brief-commit után a szó szerinti egyezés mindig eltérést mutatna (R0 és R0.8 5. kérdés); a menetek nyitó promptja az egyezést a push után ellenőrzi |
| D26 | **v4: 0 kapcsolatnál az `alatamasztas` rés adatból generált sor** (G16) | a `kapcsolatok.tsv` 34 sora két motívumé (ISTENTISZT 25, KIRALY 9); ahol nincs kapcsolat, nincs mit alátámasztani — ez adat, nem tanulmány-szöveg |
| D27 | **v4: elavult szám-javítás nincs** | az R0.8.4 17 sora más hatókörű vagy dátumozott történeti szám; valódi elavult összeg nem került elő |
| D28 | **v5: az R2.6 kategórialistája kiegészül az `adat_res` kategóriával** | a `forras=adat` (G16/D26, KIRALY-001-re a R2.2-ben kiterjesztve, l. `NYITOTT_FELADATOK.md` N19) később született, mint a hatkategóriás lista; várt tételszám 7 (motívumonként egy, mind `alatamasztas`) |
