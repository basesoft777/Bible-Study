# TEREMT002_KUTATAS_BRIEF.md — a TEREMT-002 (תֹהוּ וָבֹהוּ) kutatása: gate, hétlépéses scan, jelöltek, minősítés

*v1 — 2026.09.25 · jóváhagyásra: a §2 G-döntései és a §0 számai · a 2026.09.25-i munkaterv tartalmi szála (T1–T2)*

**Cél.** A TEREMT-002 („teremtés-visszavonás mint ítélet-nyelvezet”) motívum kutatási és
adatrésze a `MUNKAMENET.md` B-íve szerint: gate, hétlépéses protokoll (1–6. lépés), jelöltlista,
minősítés, betöltés. **Ez az első natív egyforrású motívum:** tematikus tanulmány nem készül,
a próza a T3-ban közvetlenül a forrásrétegbe kerül (munkaterv M7, 5f).

**Előfeltétel:** nincs. A `FORRASJELOLTEK_BRIEF.md`-vel párhuzamosan futhat (más fájlokat ír).

**Futás: helyi** (a havi keretből). **Modell:** Opus a fő szálon (B3, gate, minősítés); a
B2/B4 lekérdezések a `lexikai-scan` subagenttel is futhatnak. **Push:** csak külön kérésre.

**Szerkezet.**
- **1. menet (T1):** T1.0 kiindulás → T1.1 lekérdezések munkalapba → T1.2 gate-javaslat ⛔ →
  T1.3 betöltés (motívum-sor, auditok, jelöltek `nyitva`) → ÁLLJ.
- **2. menet (T2):** T2.1 minősítési javaslat ⛔ → T2.2 átvezetés → T2.3 forrásréteg és
  generált napló/index → T2.4 ellenőrzés → ÁLLJ.

**Nincs benne:** PaRDeS-értelmezés és bármilyen próza; tematikus tanulmány; lexikonoldal,
törzscikk, `res_forras.tsv`-sor; `lxx_dontesek.tsv`; a 7. lépés (nevesített tanító). Ezek a
T3-ban jönnek, az 5b (forrásréteg rés-séma) után.

---

## 0. Kiindulás *(a T1.0 újraméri; eltérésnél ÁLLJ)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` | `a6783e4` |
| 0.2 | TEREMT-002 sorai az `adat/`-ban (`motivumok`, `elofordulasok`, `jeloltek`, `kapcsolatok`, `auditok`) | 0 |
| 0.3 | TEREMT-002 említései a `motivumlog/PaRDeS_motivumok.md`-ben | 3 (a ⭐-bekezdés, a táblasor, egy „Lásd még” hivatkozás) |
| 0.4 | A napló állítása (**hipotézis, nem ellenőrzött tény** — a T1.1 kollokációja méri) | a H8414 + H0922 pár a teljes ÓSZ-ben 3 igehelyen: 1Móz 1:2, Jer 4:23, Ézs 34:11 |
| 0.5 | `adat/motivumok.tsv` | 8 sor |
| 0.6 | `eszkozok/ellenoriz.py` | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 |
| 0.7 | `eszkozok/kuszob.py` | 8 ID, 0 átlépés |

---

## 1. Szabályok és mércék

- **Szám csak lekérdezésből** (CLAUDE.md 3. szabály). A 0.4 napló-állítás addig hipotézis, amíg a
  `kollokacio` meg nem erősíti; eltérésnél a lekérdezés az irányadó, és az eltérés jelentendő.
- **Proveniencia minden futásra, 0 találatnál is** (`scope= | forras= | ts=`). A nem alkalmazható
  lépés (pl. `igealak` főnévre) is sort kap, „nem alkalmazható” indokkal.
- **Nincs közvetlen út:** minden találat a `jeloltek.tsv`-n megy át (CLAUDE.md 2. szabály).
- **Rokon jelöltek:** a H8414 (*tohu*) és a H0922 (*bohu*) önálló előfordulásai is jelöltek;
  egyik sem kerül be automatikusan.
- **Határ a TEREMT-001-gyel (tehóm):** az 1Móz 1:2 mindkét motívumé lehet. A gate 3. kérdése
  (funkció-különbség) itt kötelezően kifejtendő.
- **Shell:** héber szöveget tartalmazó kód csak fájlba írt szkriptből fut (CLAUDE.md, Shell).
- **Közös fájlt a menet nem ír** (`NYITOTT_FELADATOK.md`, changelogok, más briefek).

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | A TEREMT-002 natív egyforrású motívum: tanulmányfájl nem készül, prózát a T1–T2 nem ír. |
| G2 | A motívum-sor csak a gate ⛔ után kerül a `motivumok.tsv`-be: `statusz` = `feldolgozás alatt`, `statusz_verzio` = `v1`, `forras_study` üres. Emiatt a T2 után a `kuszob.py` várhatóan 1 átlépést jelez (≥ 3 és üres `forras_study`) — ez várt JELENTÉS, nem hiba; a natív motívumok küszöbszabálya az 5f tárgya. |
| G3 | A lekérdezések eredménye előbb munkalapba kerül (`naplok/T1_TEREMT002_*`); az `auditok.tsv`-be és a `jeloltek.tsv`-be csak a motívum-sor felvétele után (az `ellenoriz.py` 1. szabálya: hivatkozási épség). |
| G4 | A T1-ben minden jelölt `nyitva`; `beépítve`/`elutasítva` csak a T2-ben, a felhasználó döntésével. |
| G5 | `gerinc_elem`: a szópárnál a SEMA 2.2 pár-alakja (`tohu+bohu`), önálló előfordulásnál `tohu` vagy `bohu` — javaslat, a T2.1-ben dől el. |
| G6 | A napló kézi TEREMT-002-szövegei a T2.3-ban a forrásrétegbe költöznek (`motivumok/TEREMT-002.md`), karakterre azonosan (N14 mintája); a napló és az index generált blokkja újragenerálódik. |
| G7 | Az `lxx-hid` a T1.1-ben fut, eredménye munkalapba kerül; az `lxx_dontesek.tsv` a T3 tárgya (ha az FJ1 szószintű illesztést ad, azzal). |

---

## 3. Tételek

### 1. menet (T1)

- **T1.0 — Kiindulás.** `pwd`, ág, HEAD; a §0 újramérése. Eltérésnél ÁLLJ.

- **T1.1 — Lekérdezések munkalapba (a hét lépésből az 1–6.).**
  1. `eszkozok/lekerdez.py gerinc "1Móz 1:2" "Jer 4:23" "Ézs 34:11"` — gerinc-metszet.
  2. **B3 mező-hipotézis (Opus, az egyetlen generatív lépés):** mező-szavak Strong-számmal és
     egy-egy mondatos indokkal. A `lekerdez.py domen H8414 H0922` támasz, nem helyettesítő.
  3. `scan H8414`, `scan H0922` — teljes ÓSZ/ÚSZ-scan.
  4. `kollokacio H8414 H0922` — a 0.4 hipotézis mérése.
  5. `igealak` — csak ha van igei Strong a mezőben; különben „nem alkalmazható” sor.
  6. `lxx-hid` minden ÓSZ-jelöltre; `tsk` és `karoli` a három magigehelyre és minden jelöltre
     (a `karoli_szo` a `karoli` kimenetéből).

  Kimenet: `naplok/T1_TEREMT002_scan.md` (összefoglaló: a gerinc, a mező, lépésenkénti találatszám),
  `naplok/T1_TEREMT002_jeloltek_munkalap.tsv` (a `jeloltek.tsv` oszlopaival, `dontes` = `nyitva`),
  `naplok/T1_TEREMT002_auditok_munkalap.tsv` (az `auditok.tsv` oszlopaival, minden futás egy sor).
  Commit: `T1.1: TEREMT-002 lekérdezések munkalapba`.

- **T1.2 — Gate-javaslat ⛔.** A négy kérdés és a fölérendelt fogalom kifejtése
  (CLAUDE.md, „Új motívum-ID kiosztása”): `azonossag_tipusa`, `negativ_kriterium`, funkció-különbség
  a TEREMT-001-gyel az 1Móz 1:2-n, részhalmaz-kérdés, `folerendelt_fogalom`. A jelölthalmaz és a
  TEREMT-001 `elofordulasok`-sorainak átfedése szkripttel számolva. Javasolt `cim`, `ui_cimke`
  (≤ 24 karakter), `tema`, `pardes_szint`. `naplok/T1_TEREMT002_gate.md`.
  **ÁLLJ: a felhasználó dönt a gate-ről és a motívum-sor mezőiről.**

- **T1.3 — Betöltés (a jóváhagyás után).** A motívum-sor a `motivumok.tsv`-be (G2); a munkalap
  sorai az `auditok.tsv`-be és a `jeloltek.tsv`-be (`nyitva`). `ellenoriz.py`: SÉRTÉS 0.
  Commit: `T1.3: TEREMT-002 motívum-sor, auditok, jelöltek`. **ÁLLJ, jelentés.**

### 2. menet (T2)

- **T2.1 — Minősítési javaslat ⛔.** Jelöltenként: `beépítve`/`elutasítva` javaslat érdemi
  indoklással (elutasításnál kötelező), `karoli_szo`, `azonositas_modja`, `megbizhatosag`,
  `gerinc_elem` (G5), `fo_elofordulas`, `pardes_szint`. Kapcsolat-javaslatok a `kapcsolatok.tsv`
  PaRDeS-tengelyén (Előkép / Párhuzam / Beteljesedés / Kontraszt / Variáns), a TEREMT-001-gyel
  való kapcsolattal együtt. `naplok/T2_TEREMT002_minosites.tsv`.
  **ÁLLJ: a felhasználó dönt jelöltenként.**

- **T2.2 — Átvezetés.** A döntések a `jeloltek.tsv`-be; a `beépítve` sorok
  `eszkozok/betolt.py beepit --munkalap … --ir` útján az `elofordulasok.tsv`-be; a jóváhagyott
  kapcsolatok kézzel a `kapcsolatok.tsv`-be (G10). Commit: `T2.2: TEREMT-002 előfordulások és kapcsolatok`.

- **T2.3 — Forrásréteg és generált fájlok.** `motivumok/TEREMT-002.md` létrehozása a napló kézi
  szövegeivel (G6); `general.py --cel naplo --ir` és `--cel index --ir`; fixpont-ellenőrzés
  (`--ellenoriz`). Commit: `T2.3: TEREMT-002 forrásréteg, napló és index`.

- **T2.4 — Ellenőrzés és jelentés.** `ellenoriz.py` (SÉRTÉS 0), `kuszob.py` (G2 szerinti várt
  JELENTÉS), `gate.py` (TEREMT-001 ütközés-jelentés). **ÁLLJ, jelentés.**

---

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | `ellenoriz.py`: SÉRTÉS 0 a T1.3 és a T2.4 után |
| K2 | minden lefutott lekérdezés egy sor az `auditok.tsv`-ben, a 0 találatos és a nem alkalmazható is |
| K3 | minden `elofordulasok`-sornak van `beépítve` `jeloltek`-sora (nincs közvetlen út) |
| K4 | minden `elofordulasok`-sorban kitöltött `gerinc_elem` |
| K5 | nincs új tanulmányfájl; a `lexikon/` és a `tematikus_lezart/` változatlan |
| K6 | a napló és az index `--ellenoriz` fixponton ZÖLD a T2.3 után |
| K7 | nincs `csv` modul; nullázott Strong-számok (SEMA 1.2) |
| K8 | a 0.4 hipotézis eredménye (megerősítve / eltér) a T1.1 összefoglalójában szerepel |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.25 | Első változat a munkaterv tartalmi szálából (T1–T2; M7): natív egyforrású motívum, tanulmány nélkül (G1); gate ⛔ előtt nincs adat-írás (G2, G3); jelöltek `nyitva` a T1-ben (G4); a napló kézi szövegei a forrásrétegbe (G6); próza, lexikon és LXX-döntések a T3-ban. |

---

## 6. Nyitó promptok (helyi session; a briefet csatold)

**1. menet:**
```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t és a MUNKAMENET.md-t.
1. Hozz létre egy teremt002-t1 ágat a main-ről. A csatolt TEREMT002_KUTATAS_BRIEF.md-t mentsd
   a repó gyökerébe, változtatás nélkül. Commit: "T1: TEREMT002_KUTATAS_BRIEF.md v1".
2. Hajtsd végre a T1.0–T1.2 tételeket a brief §3 szerint, a §1 szabályaival és a §2 döntéseivel.
ÁLLJ a T1.2 után: a gate-javaslat a chatbe, döntésre.
```

**A gate-döntés után (ugyanabban a sessionben):**
```
A gate-döntés: [ide a döntés]. Hajtsd végre a T1.3-at. ÁLLJ: jelentés (commitok, K1, K2, K8).
```

**2. menet:**
```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t és a TEREMT002_KUTATAS_BRIEF.md-t.
Hajtsd végre a T2.1-et. ÁLLJ: a minősítési javaslat a chatbe, döntésre.
A döntések után: T2.2–T2.4, majd ÁLLJ: jelentés (commitok, K1–K8).
```
