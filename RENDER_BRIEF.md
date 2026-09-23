# RENDER_BRIEF.md — render-átállás és szótári adatréteg

*v1 — 2026.09.23 · jóváhagyásra: a §2 G-döntései és a §0/§4 számai*

**Cél.** A lexikonoldal tiszta render legyen: a kézi szövegek a forrásrétegben élnek, a
generátor egy belső adatmodellből dolgozik, és ebből két kimenet készül egy futásban —
a tudományos lexikonoldal (`_TUDOMANYOS.md`, változatlan formában) és a kereszthivatkozási
törzscikk (`_TORZSCIKK.md`, a pilot szerint). Ugyanebben a briefben megy a szótári
adatréteg (fordítási gyorsítótár, terminológia, kiejtés, szerepkör-mátrix, TBESH, Mounce, SECE).

**Szerkezet.** R0 felmérés (csak olvas) ⛔ → 1. menet: nulla-diff ⛔ → 2. menet: kimenet-változtató.
A két ⛔ megállás a független ellenőrzésé; köztük brief-módosítás csak akkor kell, ha a
felmérés vagy az ellenőrzés eltérést talál.

**Modell:** Sonnet. **Push csak külön kérésre.**

**Nincs benne:** fordítási pipeline (`fordit.py`, külső modellek), BDB SQLite-csere, héber gépi
kiejtés, a C2 tartalmi munkája, a LEXV2_3 többi tétele (TSK-tábla, kapcsolat-indoklás,
bibliográfia).

---

## 0. Kiindulás *(az R0.1 újraméri; eltérésnél ÁLLJ)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` = `origin/main` | `2eea2c2` |
| 0.2 | `ellenoriz.py` összesítő | RENDBEN 8 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 1, kód 0 |
| 0.3 | `general.py --cel lexikon --ellenoriz` | 8/8 „változatlan lenne" |
| 0.4 | lexikonoldalak | 8 (`lexikon/*_TUDOMANYOS.md`), mind 10 generált blokkal |
| 0.5 | kézi szöveg a blokkokon kívül | ISTENTISZT-001: 37 222 karakter; a másik 7: 995–1 033 karakter, oldalanként 8 „Kézzel írandó" helyőrző |
| 0.6 | a 7 helyőrzős oldal eltérése a mai `VAZ_SABLON`-tól | mindegyiknél a 6. és 7. szakasz régebbi helyőrző-szerkezete (`### PaRDeS keretrendszer`, `### Módszertani napló`, `### Nyitott kérdések és séma-korlátok`) |
| 0.7 | `adat/lexikon_hivatkozasok.tsv` | 24 sor (Thayer 14, BDB 4, TBESG 4, TBESH 1, LSJ 1); `forditas_hu` kitöltve: 11 |
| 0.8 | `adat/forditas_ubs.tsv` | 20 sor; `definicio_hu` 20, `glosszak_hu` 20 |
| 0.9 | `motivumok/*.md` (napló-forrásréteg) | 8 fájl — a lexikonoldal kézi szövegét **nem** tartalmazzák |
| 0.10 | kiejtés-pár a kézi szövegben (blockquote nélkül) | görög 50, héber 49 — mind az ISTENTISZT-001-ben |
| 0.11 | tudományos átírás-gyanú a generált blokkokban (becslés) | 859 (8 oldal összesen) — az R0.4 pontosítja |
| 0.12 | nyers SQLite | `MCGED.lexicon` 10 666 sor; `TBESH.lexicon` 9 888 sor |
| 0.13 | törzscikk-pilot (ISTENTISZT-001) | 32 igehely (22 ÓSZ / 10 ÚSZ) · 25 kapcsolat · 22 LXX-sor · 106 kereszthivatkozás · 0 üzemeltetési elem |

---

## 1. Fogalmak

- **Rés:** a lexikonoldal egy kézi szakasza a saját fejlécsorával együtt. Hét rögzített rés van,
  a `VAZ_SABLON` sorrendjében: `kivonat`, `2b`, `miert_fontos`, `minosites`, `alatamasztas`,
  `ertelmezes`, `modszertan`. A rés a fejlécsorától a következő rés fejlécéig, generált markerig
  vagy váz-fejlécig tart; a résen belüli alfejlécek (akár `*(kézi…)*` jelölésűek is) a rés részei.
- **Váz-fejléc:** a `VAZ_SABLON` nem kézi fejlécei (`## Tartalomjegyzék`, `## 1. Előfordulások` … `## Kolofon`).
- **Nulla-diff:** az `--ir` futás után `git status --porcelain lexikon/` üres — bájtra, `ts=` értékekkel együtt.

---

## 2. G-döntések *(jóváhagyásra)*

| # | Kérdés | Javaslat | Alternatíva |
|---|---|---|---|
| G1 | Hol élnek a lexikonoldal rései? | **Új fájl motívumonként: `motivumok/lexikon/[ID].md`** — a napló-forrásréteg (`motivumok/[ID].md`) érintetlen | a meglévő `motivumok/[ID].md` új szakasza |
| G2 | Hogyan tárolódik egy rés? | **Szó szerint, fejlécsorral együtt, résjelölők közt:** `<!-- RÉS-KEZDET: kivonat -->` … `<!-- RÉS-VÉGE: kivonat -->`. A 7 helyőrzős oldal rései a mai helyőrző-szöveget hordozzák (0.6 is) | csak a törzs, a fejléc a vázból — ez a 7 oldalon és az ISTENTISZT 2/b fejlécén nem adna nulla-diffet |
| G3 | Nulla-diff mérce | **bájtazonosság `ts=` értékekkel együtt**: változatlan blokk fejléce nem íródik újra (a mai `_blokk_beilleszt_fejleccel` viselkedése) | `ts`-normalizált egyezés |
| G4 | A lexikonoldal szerkeszthetősége az 1. menet után | **Kézzel nem szerkeszthető**; a rés csak a forrásrétegben javítható. Az `ellenoriz.py` új 11. szakasza sértésnek jelzi, ha a lap rése eltér a forrásrétegtől. A `CLAUDE.md` és a `MUNKAMENET.md` ezt rögzíti. A fájl-eleji „GENERÁLT" jelölés a 2. menetben (R2.5) | — |
| G5 | Belső adatmodell | **`modell_epit(m, …)` → egy szótár** (a 10 blokk adatai + a 7 rés + a szótári szerepek); a `_TUDOMANYOS` és a `_TORZSCIKK` render ebből dolgozik, a blokk-építők logikája nem változik | — |
| G6 | Fordítási gyorsítótár | **`adat/forditasok.tsv`**, oszlopok: `szotar`, `strong`, `entry_id`, `jelentes_szam`, `mezo`, `forras_hash`, `forditas_hu`, `allapot`, `modell`, `datum`, `terminologia_verzio`. Kulcs: `szotar+strong+entry_id+jelentes_szam+mezo`. `forras_hash` = a forrásszöveg SHA-1-e (lexikonsornál a `szoveg_en`, UBS-nél a forrás definíció, illetve glossza). Migráció: 11 lexikon-fordítás (`mezo=forditas`) + 20 UBS-definíció + 20 UBS-glossza = **51 sor**, `allapot=kezi`. A `lexikon_hivatkozasok.forditas_hu` oszlop és a `forditas_ubs.tsv` megszűnik | a UBS marad külön táblában |
| G7 | Terminológia | **`adat/terminologia.tsv`** (`angol`, `magyar`, `megjegyzes`, `verzio`); induló sorok a mai jelmagyarázat konvenciójából: spirit = szellem, spiritual = szellemi, soul = lélek. Az ellenőrző csak jelent (JELENTÉS), nem sért | — |
| G8 | Kiejtés | **Görög: szabálytábla (`adat/kiejtes_szabalyok.tsv`) + `eszkozok/kiejtes.py`.** Héber: nincs gépi átírás; a lemma-kiejtés csak a kézi `adat/kiejtes_kivetelek.tsv`-ből jön (induló sorai kizárólag a tesztkészletben már jóváhagyott alakok). Az 1. menetben a `kiejtes.py` csak mér és jelent. Élesítés (R2.1) feltétele: a görög tesztkészlet 100%-a egyezik, a kivételekkel együtt | — |
| G9 | Szerepkör-mátrix | **`adat/szotar_szerepek.tsv`** (`nyelv`, `sorrend`, `szerep`, `forras`, `feltetel`) a pilot D6 sorrendjével; csak a törzscikk-render olvassa | — |
| G10 | Törzscikk | **`lexikon/[ID]_TORZSCIKK.md` mind a 8 motívumra**, új cél `general.py --cel torzscikk` (élesíthető), új sablon `sablonok/8_PaRDeS_torzscikk_sablon.md`. A pilot döntései (D1–D13, `ISTENTISZT-001_TORZSCIKK_dontesnaplo.md`) érvényesek. A helyőrző-rés és a `【NAPLO: …】` blokk kimarad. Az 1. menetben a 2/b rés egyben, „Kiegészítő szótári adatok" címmel jelenik meg; a „Miért fontos" rés `#### [Strong]` alszakaszai a szó „Jelentősége" pontjához kerülnek, a többi a „A szavak együtt" alá | csak az ISTENTISZT-001-re |
| G11 | Mounce és SECE | **Adatosítás a 2. menetben:** MCGED-import (`konkordancia/MCGED_teljes.tsv` a nyers SQLite-ból); a SECE a meglévő `SECE_G_teljes.tsv` / `SECE_H_teljes.tsv`-ből (L–N és megfelelő-lista kinyerése). Új generált sorok a 2. szakasz szócikkeiben, a Mounce szó szerinti megjelölésével a 8. szakaszban és a kolofonban. Az ISTENTISZT-001 2/b Mounce/SECE-táblái ezzel a forrásrétegből törlődnek | — |
| G12 | TBESH | **Átállás a konszolidált változatra** (`konkordancia/TBESH_konszolidalt.tsv` a `TBESH.lexicon`-ból), ha az R0.5 összevetése nem talál tartalomvesztést | marad a `TBESH.txt` |
| G13 | A 3 tartalmi NAPLO-blokk (ISTENTISZT-001: a Típus-mező névütközése; a study 15 → 22 frissítése; a Variáns-döntés) | **Maradnak NAPLO-blokkban** (a lexikonoldalon látszanak, a törzscikkből kimaradnak); a study-frissítés már nyitott tétel | nyitott kérdésként a 7. szakaszba (R2.4) |

---

## 3. Tételek

### R0 — felmérés *(csak olvas; egy commit: a jelentés és a munkalapok)*

- **R0.1** A §0 minden sorának újramérése. Ha bármi eltér: **ÁLLJ**, jelentés.
- **R0.2** Rés-leltár: 8 oldal × 7 rés — bájtméret, helyőrző-e, fejlécsor szövege; a réseken és a vázon kívül eső szöveg listája (várt: 0). `naplok/RENDER_R0_resek.tsv`.
- **R0.3** Kiejtés-tesztkészlet: minden „görög szó (kiejtés)" és „héber szó (kiejtés)" pár a lexikonoldalak kézi szövegéből (blockquote nélkül), a `lexikon_hivatkozasok.forditas_hu` és a `forditas_ubs` mezőiből. `naplok/RENDER_kiejtes_tesztkeszlet.tsv` (`nyelv`, `szo`, `kiejtes`, `hely`).
- **R0.4** A generált blokkok átírásainak leltára oldalanként és blokkonként: görög lemma, görög alak, héber lemma, héber alak (STEP). `naplok/RENDER_R0_atirasok.tsv`. Ez adja az R2.1 elvárt diffjét.
- **R0.5** Forrás-összevetés: a 8 motívum H-tokenjeire a `TBESH.txt` és a `TBESH.lexicon` szövege (egyezik / bővebb / szűkebb); a G-tokenekre az MCGED lefedettsége; a SECE L–N- és megfelelő-mezőinek kinyerhetősége.
- **R0.6** Volumen a későbbi fordítási pipeline-hoz: szócikk/sor és karakter a Thayer, BDB, TBESG, UBS, SDBH, SDGNT kivonatban.
- **R0.7** Jelentés: `naplok/RENDER_R0_jelentes.md` — a mérések és **egy csokorban** minden kérdés, ami a G-döntések végrehajtását befolyásolja. **ÁLLJ.**

### 1. menet — nulla-diff

- **R1.1** Forrásréteg: `motivumok/lexikon/[ID].md` × 8, fejléccel (forrásréteg, kézzel szerkeszthető) és a 7 réssel szó szerint (G1, G2). Kivágó szkript: `eszkozok/render_resek_kivag.py`.
- **R1.2** `lexikon_general.py`: a `_TUDOMANYOS` oldal a vázból + a blokkokból + a forrásréteg réseiből áll össze; változatlan blokk fejléce nem íródik újra (G3). Hiányzó forrásréteg-fájl vagy rés: hibakód, nem helyőrző. A `VAZ_SABLON` kézi helyőrzői csak új motívum forrásréteg-fájljának létrehozásakor íródnak.
- **R1.3** Belső adatmodell (G5): `modell_epit()`; a két render ebből dolgozik.
- **R1.4** Fordítási gyorsítótár (G6): `adat/forditasok.tsv`, migráció 51 sorral; a generátor innen olvas; SEMA új 2.x pont; a régi oszlop és tábla megszűnik.
- **R1.5** Új adattáblák: `terminologia.tsv` (G7), `kiejtes_szabalyok.tsv`, `kiejtes_kivetelek.tsv` (G8), `szotar_szerepek.tsv` (G9); SEMA-bejegyzésekkel.
- **R1.6** `eszkozok/kiejtes.py`: görög átírás függvénye; `--ellenoriz` mód a tesztkészleten (egyezési arány, eltérések listája). Nem ír.
- **R1.7** `ellenoriz.py` új szakaszai:
  - **11.** forrásréteg ≡ lexikonoldal rései (eltérés = SÉRTÉS);
  - **12.** fordítási gyorsítótár: kulcs egyedi, `forras_hash` egyezik a forrással (eltérés = SÉRTÉS, `allapot` → `elavult` javaslat), terminológia-verzió elmaradás (JELENTÉS);
  - **13.** kiejtés és terminológia (JELENTÉS): hiányzó vagy szabálytól eltérő görög kiejtés a kézi szövegben; terminológia-sértés a gyorsítótárban.
- **R1.8** Törzscikk (G10): sablon 8, `--cel torzscikk`, 8 fájl.
- **R1.9** Dokumentáció: `CLAUDE.md` (a lexikonoldal rései csak a forrásrétegben szerkeszthetők; a `_TORZSCIKK` generált), `MUNKAMENET.md` (a C2 a forrásrétegben dolgozik), `adat/SEMA.md`, `NYITOTT_FELADATOK.md`. **ÁLLJ.**

### 2. menet — kimenet-változtató, elvárt diffel

- **R2.1** Görög kiejtés a generált blokkokban a `kiejtes.py`-ból (lemma és alak); héber lemma a kivétel-táblából, ha van sora; héber alak (STEP) változatlan. Előfeltétel: az R1.6 görög egyezése 100%.
- **R2.2** TBESH: import és átállás (G12).
- **R2.3** Mounce és SECE adatosítása (G11), a Mounce angol glosszáinak fordítása a gyorsítótárból; a 2/b-ben már meglévő 3 magyar glossza `kezi` sorként átkerül. Hiányzó fordítás: „*Fordítás függőben.*"
- **R2.4** Forrásréteg-javítások (ISTENTISZT-001): a 2/b Mounce/SECE-táblái törlődnek; a 2/b jelentőség-bekezdései (BDB 2.c/3 kiemelés, „√ unknown", a három ige kereszt-elemzése) a „Miért fontos" rés `#### H7121`, `#### H8034`, `#### G0994` alszakaszaiba kerülnek; a G0994-megjegyzés javítása („rokon szóként szerepel; LXX-beli szerepe a 3. szakaszban"); G13 szerint.
- **R2.5** A lexikonoldal első sora elé gépi jelölés: `<!-- GENERÁLT: general.py --cel lexikon | rések: motivumok/lexikon/[ID].md -->`.
- **R2.6** Újragenerálás (`lexikon` és `torzscikk`), majd diff-osztályozó (`eszkozok/render_diff_osztalyoz.py`): minden változott sor egy kategóriába esik — `kiejtes`, `tbesh`, `mounce_sece`, `forrasreteg`, `fejlec`, `licenc`. Ismeretlen kategória: **ÁLLJ**.
- **R2.7** Lezárás: `NYITOTT_FELADATOK.md` (új tételek: fordítási pipeline, BDB SQLite-csere, héber gépi kiejtés, a 12 Thayer-szócikk fordítása a gyorsítótárba), `MUNKAMENET.md`.

---

## 4. Várt számok

| Menet | Mérés | Várt |
|---|---|---|
| R0 | rés-leltár | 8 × 7 rés; ISTENTISZT-001: 0 helyőrző; a többi 7: 8 helyőrző; réseken kívüli szöveg: 0 |
| R0 | kiejtés-tesztkészlet | ≥ 99 pár (50 görög + 49 héber a kézi szövegből) + a fordítás-mezők párjai |
| 1 | `--cel lexikon --ir` után `git status --porcelain lexikon/*_TUDOMANYOS.md` | üres |
| 1 | `motivumok/lexikon/` | 8 fájl × 7 rés |
| 1 | `adat/forditasok.tsv` | 51 sor, mind `kezi` |
| 1 | `ellenoriz.py` | RENDBEN 10 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2, kód 0 |
| 1 | `kiejtes.py --ellenoriz` | görög egyezési arány jelentve (cél 100%; alatta a kivételtábla bővítése jóváhagyásra) |
| 1 | `lexikon/*_TORZSCIKK.md` | 8 fájl; ISTENTISZT-001: 32 (22/10) · 25 · 22 · 106, üzemeltetési elem 0, helyőrző 0 |
| 2 | diff-osztályozó | ismeretlen kategória: 0; a `kiejtes` kategória darabszáma = az R0.4 leltár görög tételei + a kivételtábla héber lemmái |
| 2 | `ellenoriz.py` | SÉRTÉS 0, kód 0 |

---

## 5. Elfogadási kritériumok

### R0
| # | Kritérium |
|---|---|
| K1 | a §0 minden sora jelentve; eltérésnél megállás |
| K2 | a négy munkalap és a jelentés megvan; a kérdések egy listában |
| K3 | az éles `adat/`, `lexikon/`, `motivumok/` bájtra változatlan |

### 1. menet
| # | Kritérium |
|---|---|
| K4 | nulla-diff: `git status --porcelain lexikon/*_TUDOMANYOS.md` üres |
| K5 | a forrásréteg réseit visszaillesztve a lap bájtra azonos (az `ellenoriz.py` 11. szakasza RENDBEN) |
| K6 | `forditasok.tsv` 51 sor, kulcs egyedi, hash egyezik; a régi oszlop és tábla nincs; a generált szövegek nem változtak (K4 fedi) |
| K7 | a négy új adattábla SEMA-bejegyzéssel; a `kiejtes.py` nem ír |
| K8 | a 8 törzscikk megvan; az ISTENTISZT-001 számai a §4 szerint; `grep -c` a törzscikkekben: `GENERÁLT` 0, `【NAPLO` 0, `proveniencia:` 0, `Kézzel írandó` 0 |
| K9 | `ellenoriz.py` a §4 szerint, kód 0 |
| K10 | a TSV-kezelés `csv` modul nélkül; import, nem másolás (`general`, `lekerdez`) |
| K11 | commitok a §6 szerint; `git status --porcelain` üres |

### 2. menet
| # | Kritérium |
|---|---|
| K12 | R2.1 csak 100%-os görög egyezés után futott |
| K13 | diff-osztályozó: ismeretlen kategória 0; a kategóriák darabszáma jelentve |
| K14 | a 8. szakasz és a kolofon tartalmazza a Mounce szó szerinti megjelölését és a SECE-t, ahol használva van |
| K15 | az ISTENTISZT-001 2/b rése csak prózát tartalmaz; a jelentőség-bekezdések a „Miért fontos" alatt |
| K16 | `ellenoriz.py` SÉRTÉS 0, kód 0; a törzscikkek újragenerálva, K8 ismét teljesül |
| K17 | commitok a §6 szerint; `git status --porcelain` üres |

---

## 6. Commitok

**R0**
| Üzenet | Fájlok |
|---|---|
| `RENDER_BRIEF.md v1` | `RENDER_BRIEF.md` |
| `R0: felmérés — rés-leltár, kiejtés-tesztkészlet, átírások, forrás-összevetés` | `naplok/RENDER_R0_*.tsv`, `naplok/RENDER_kiejtes_tesztkeszlet.tsv`, `naplok/RENDER_R0_jelentes.md` |

**1. menet**
| Üzenet | Fájlok |
|---|---|
| `R1.1–R1.3: forrásréteg-rések és belső adatmodell (nulla-diff)` | `motivumok/lexikon/*.md`, `eszkozok/render_resek_kivag.py`, `eszkozok/lexikon_general.py`, `eszkozok/general.py` |
| `R1.4–R1.5: fordítási gyorsítótár és új adattáblák` | `adat/forditasok.tsv`, `adat/terminologia.tsv`, `adat/kiejtes_szabalyok.tsv`, `adat/kiejtes_kivetelek.tsv`, `adat/szotar_szerepek.tsv`, `adat/lexikon_hivatkozasok.tsv`, `adat/forditas_ubs.tsv` (törlés), `adat/SEMA.md`, `eszkozok/lexikon_general.py` |
| `R1.6–R1.7: kiejtes.py és az ellenőrző új szakaszai` | `eszkozok/kiejtes.py`, `eszkozok/ellenoriz.py` |
| `R1.8: kereszthivatkozási törzscikk (8. sablon, --cel torzscikk)` | `sablonok/8_PaRDeS_torzscikk_sablon.md`, `eszkozok/torzscikk_general.py`, `eszkozok/general.py`, `lexikon/*_TORZSCIKK.md` |
| `R1.9: dokumentáció` | `CLAUDE.md`, `MUNKAMENET.md`, `NYITOTT_FELADATOK.md` |

**2. menet**
| Üzenet | Fájlok |
|---|---|
| `R2.1: görög kiejtés a generált blokkokban` | `eszkozok/lexikon_general.py`, `eszkozok/kiejtes.py`, `adat/kiejtes_kivetelek.tsv`, `lexikon/*` |
| `R2.2–R2.3: TBESH konszolidált, Mounce és SECE adatosítva` | `konkordancia/TBESH_konszolidalt.tsv`, `konkordancia/MCGED_teljes.tsv`, importszkriptek, `adat/forditasok.tsv`, `eszkozok/lexikon_general.py`, `lexikon/*` |
| `R2.4–R2.5: forrásréteg-javítások és GENERÁLT-fejléc` | `motivumok/lexikon/ISTENTISZT-001.md`, `eszkozok/lexikon_general.py`, `lexikon/*` |
| `R2.6–R2.7: diff-osztályozó és lezárás` | `eszkozok/render_diff_osztalyoz.py`, `naplok/RENDER_R2_diff.tsv`, `NYITOTT_FELADATOK.md`, `MUNKAMENET.md` |

---

## 7. Nyitó promptok *(Sonnet)*

### R0
```
Olvasd el a CLAUDE.md-t, majd a RENDER_BRIEF.md-t teljes egészében.

0. Commitold a briefet: "RENDER_BRIEF.md v1".
1. R0.1: mérd újra a §0 tábláját. Ha bármi eltér, ÁLLJ MEG és jelents.
2. R0.2–R0.6 a §3 szerint. Az éles adat/, lexikon/, motivumok/ könyvtárba NE írj.
3. R0.7: jelentés, a kérdések egy listában. Commit a §6 R0-táblája szerint. K1–K3.
4. ÁLLJ.
```

### 1. menet
```
Olvasd el a CLAUDE.md-t, a RENDER_BRIEF.md-t (a jóváhagyott verziót) és a
naplok/RENDER_R0_jelentes.md-t.

0. main = origin/main = <az R0 utáni hash>. Ha nem, ÁLLJ MEG.
1. R1.1–R1.3. Utána: general.py --cel lexikon --ir, majd git status --porcelain
   lexikon/*_TUDOMANYOS.md — ha nem üres, ÁLLJ MEG, és ne commitolj.
2. R1.4–R1.9 a §3 szerint, minden tétel után újra a nulla-diff próba.
3. K4–K11. Commitok a §6 1. menet-táblája szerint.
4. ÁLLJ.
```

### 2. menet
```
Olvasd el a CLAUDE.md-t és a RENDER_BRIEF.md-t (a jóváhagyott verziót).

0. main = origin/main = <az 1. menet utáni hash>. Ha nem, ÁLLJ MEG.
1. R2.1 csak akkor, ha a kiejtes.py --ellenoriz görög egyezése 100%; ha nem, ÁLLJ MEG.
2. R2.2–R2.5, majd R2.6: ha a diff-osztályozó ismeretlen kategóriát talál, ÁLLJ MEG.
3. R2.7. K12–K17. Commitok a §6 2. menet-táblája szerint.
4. ÁLLJ.
```

---

## 8. Döntésnapló

| # | Döntés | Indoklás |
|---|---|---|
| D1 | Egy brief, három szakasz (R0 → 1. menet → 2. menet), két független ellenőrzési megállással | a felhasználó kérése: kevesebb brief, a kérdések egy csokorban |
| D2 | Az 1. menet nulla-diff: minden tétel, ami a lexikonoldal kimenetét nem változtatja, ide került (forrásréteg, adatmodell, gyorsítótár, új táblák, ellenőrzők, törzscikk) | a szerkezeti átállás tartalmi változás nélkül, bájtra ellenőrizhető |
| D3 | A kimenet-változtató tételek (kiejtés, TBESH, Mounce/SECE, forrásréteg-javítás, fejléc) a 2. menetben, diff-osztályozóval | minden változás kategóriába sorolva; ismeretlen változás = megállás |
| D4 | A rés szó szerint, fejlécsorral együtt tárolódik | a 7 oldal régi helyőrző-szerkezete (0.6) és az ISTENTISZT eltérő 2/b-fejléce így is nulla-diff marad |
| D5 | A 7 helyőrzős oldal rései a helyőrzőt hordozzák, a törzscikkből kimaradnak | a C2 ezeket tölti ki, már a forrásrétegben |
| D6 | Héber gépi kiejtés nincs; csak a kézi kivétel-tábla | a magyaros héber átírás nem vezethető le megbízhatóan (svá, dagesh, qamets qatan) |
| D7 | A törzscikk az 1. menetben a 2/b rést egyben mutatja; a pilot szerinti szétosztás a 2. menet forrásréteg-javításával (R2.4) valósul meg | a render nem értelmez szabad prózát; a hozzárendelés a forrásban történik |
| D8 | Kizárva: fordítási pipeline, BDB SQLite-csere, héber gépi kiejtés, C2, a LEXV2_3 többi tétele | külön kockázat és külön döntés; a 2. menet lezárása nyitott tételként rögzíti őket |
| D9 | A diff-osztályozó és a nulla-diff próba minden tétel után fut | a szkript csendes sorvesztésének tanulsága (ISTENTISZT ZARO-körök) |
