# F8 — Hiányzó eszközök: az üzemmenet kiegészítése

*Készítette: chat-menet (Opus 5), 2026-09-21, **v2** — a §2 G-döntései jóváhagyva (2026-09-21), alternatíva nélkül.*
*Kiindulási állapot: `main` = `origin/main` = `8511e35` (az F7 lezárva és pusholva).*

---

## 0. Miért tér el ez a brief a `MUNKAMENET.md` öt tételétől

A `MUNKAMENET.md` két helyen sorolja fel az F8 bemenetét, eltérő szűrővel. A lépéstábla lépésszinten jelöl (`F8 — nincs eszköz`: A3, A3b, B6, B9, B10). A „Mi hiányzik" szakasz üzemmenet-szinten jelöl (öt tétel, köztük a B1 és az A7, amelyek nem lépéshiányok). A kettő együtt **hét** tételt ad:

| # | Tétel | Lépés | Jelleg |
|---|---|---|---|
| 1 | `jelolt.py` | A3b | eszköz |
| 2 | küszöbfigyelő önálló eszköze, kilépési kóddal | B1 | kiemelés a `general.py` logikájára építve |
| 3 | `ellenoriz.py` — konzisztencia + Q-kapu gépi része | B10 | eszköz |
| 4 | `betolt.py` — study↔adat átjáró | A3, B6 | döntés + eszköz |
| 5 | tanítói keresés sablonja | B9 | sablon |
| 6 | subagentek | B4, B9 | agent-definíció |
| 7 | sorozat-tábla | A7 | fogalmi döntés (`NYITOTT_FELADATOK.md` N10) |

A 3. tétel csak a lépéstáblában szerepel: a B10 hiánya az `ellenoriz.py`, nem az agent. A 4. tétel neve a tervben `betolt.py` (terv 2. pont). Az F7 §3 az A4/B5 kódos kikényszerítését is ide sorolta; ez a 3. és a 4. tételben valósul meg (l. G2, G4).

---

## 1. Kiindulási állapot — mérve, `8511e35`

A §1 számai a 2026.09.21-i, `codeload`-tarballból vett mérésből valók. Az F8.0 újraméri őket; eltérésnél megállás.

| Mit | Mért érték |
|---|---|
| `eszkozok/` | 41 `.py` szkript; nincs `jelolt.py`, `betolt.py`, `ellenoriz.py`, `kuszob.py` |
| `.claude/` | nincs verziózva (a tarballban nincs); lokálisan csak `worktrees/` (F7 §1) |
| `adat/` adatsorok | `motivumok` 7, `elofordulasok` 201 (ebből 198 `strong`-gal, 18 különböző Strong), `jeloltek` 221 (201 `beépítve`, 3 `elutasítva`, 17 `nyitva`) |
| ⭐-állás (`COUNT(DISTINCT fo_elofordulas)`) | 24 csoport; ≥ 3: ALVIL-001 6, ANTROP-001 5, ISTENTISZT-001 5, TEREMT-001 5; 1: HODIT-001, KIRALY-001, MENNY-001; mind a 7 `publikálható` |
| `render_naplo_kuszob()` | kiírja a fő előfordulások számát, de **nem hasonlít 3-hoz és nem jelez átlépést** |
| `adat/SEMA.md` §3 | 8 integritási szabály, „ezeket az `ellenoriz.py` kényszeríti ki" |
| tematikus sablon, Minőségi kapu | Q1–Q7 (290–365. sor) |
| napló, „Feldolgozott igeszakaszok listája" | `motivumlog/PaRDeS_motivumok.md` 617. sor, 24 adatsor, kézi, generált blokk nélkül |
| kereszthivatkozás-naplók helye | `[study-mappa]/naplok/` (pl. `tematikus_lezart/naplok/`, 7 fájl); a gyökér `naplok/` futási naplók (8 fájl) |
| `_tanitoi_kereses` fájl | egy sincs a repóban |
| bővített tanulmányok | 23 `*_bovitett.md` |

**Leletek:**

- **L1 — a B1 csak félig van meg.** A számolás megvan, a küszöb-összevetés nincs. Az F7 L1-je („jelentés-burok a meglévő logika köré") ezért pontosítandó: kell egy küszöbdefiníció is (G5).
- **L2 — három `publikálható` motívumnak egy fő előfordulása van** (HODIT-001, KIRALY-001, MENNY-001). Nem F8-tárgy; a küszöbfigyelőnek viszont nem szabad ezeket hibának jelölnie.
- **L3 — az `ellenoriz.py` specifikációja kész.** A SEMA §3 nyolc szabálya. A Q-kapuból gépileg a Q1 (szerkezet) és a Q7 (dataset-lefedettség, egyezik a §3/8-cal) ellenőrizhető; a Q2–Q6 ítélet.
- **L4 — az A3 és a séma ütközik.** A terv szerint az A3 `jeloltek.tsv`-sorokat ír, de ott az `id` kötelező, A3-kor pedig még nincs motívum-ID (az A4-ben születik).
- **L5 — a „sorozat-tábla" azonosítható.** A bővített sablon 0. pontja (Sorozat-kontextus) a napló „Feldolgozott igeszakaszok" táblájából dolgozik, a terv 8.1–8.2 pontja „sorozat-kontextus" / „sorozat-kivonat" néven számol vele. Az A7 három tárgyából a napló és az index generált; ez az egyetlen, amelyik nem.
- **L6 — a jelölt-generálás formulaikus motívumoknál túltermel.** Egy formula (pl. ISTENTISZT-001) egyetlen gyakori Strongja sok hamis jelöltet ad; a projekt szabálya szerint formula-motívumhoz pozicionális keresés kell.

---

## 2. G-döntések — jóváhagyva (2026-09-21)

| # | Döntés | Elvetett alternatíva | Indok |
|---|---|---|---|
| G1 | A **sorozat-tábla = a napló „Feldolgozott igeszakaszok listája"**. Az F8 a definíciót rögzíti (N10 lezárul), a tábla **kézi marad**. A generálás új tétel: `NYITOTT_FELADATOK.md` N11 | `naplo#sorozat` generált blokk egy új `adat/tanulmanyok.tsv`-ből, a 24 sor migrálásával | A „Fő kulcsszavak" oszlopot generálás esetén is a kutató írja; a generálás nyeresége egyelőre csak a 0. pont aktiválási feltételének gépi ellenőrizhetősége. Az F8 hét tétele nélküle is sok |
| G2 | A **`betolt.py` két iránya**. (a) **A3:** a bővített 2. pont kulcsszó-táblázata egy új, `id` nélküli átmeneti táblába kerül: `adat/kulcsszavak.tsv` (`tanulmany`, `igehely`, `szo`, `strong`, `datum`), SEMA 2.8. (b) **B6:** csak `dontes=beépítve` `jeloltek`-sor léptethető elő `elofordulasok`-sorrá, egy kutató által kitöltött munkalapból (`kapcsolodas`, `gerinc_elem`, `funkcio` stb.). A betöltő **soha nem ír `dontes`-t**. Egyetlen hiányzó kötelező mező esetén az egész futás megáll, és lemezre semmi nem kerül. Alapértelmezésben próba; élesít az `--ir` | (a)-hoz: az A3 megszűnik önálló lépésként, az A4 írja közvetlenül a `jeloltek`-sort | Az (a) megszünteti az L4 ütközést séma-lazítás nélkül. A (b) a SEMA §3/2 („nincs közvetlen út") gépi kikényszerítése, vagyis a B5-megállás kódos alakja (F7 §3) |
| G3 | Az **N8 nem előfeltétel** | — | Sem a G1, sem a G2 nem hoz új `general.py`-célt |
| G4 | Az **`ellenoriz.py` hatóköre:** a SEMA §3 1–6. és 8. szabálya kikényszerítve; a 7. a `gate.py` meghívása, jelentésként, bukás nélkül; `--study <fájl>` esetén Q1 és Q7. A Q2–Q6 a jelentésben `kézi` jelölést kap, **soha nem „megfelelt"-et**. Kilépési kód: 0 = rendben, 1 = szabálysértés, 2 = hiba | a Q6 regex-alapú részleges gépesítése | Ítéletet igénylő pontra gépi „megfelelt" hamis ellenőrzöttség-állítás volna — ugyanaz a hibaosztály, mint a 2026.09.10-i 🔍-eset |
| G5 | A **küszöbfigyelő** új fájl: `eszkozok/kuszob.py`, amely a `general.fo_elofordulas_csoportok()`-ot **importálja**, nem másolja. **Átlépés = fő előfordulás ≥ 3 ÉS üres `forras_study`.** Kilépési kód: 0 = nincs átlépés, 1 = van, 2 = hiba. A `general.py` naplóblokkja nem változik | átlépés = ≥ 3 ÉS `statusz = feldolgozás alatt` | A `forras_study` azt méri, amit a B1 kérdez (van-e már tematikus study). A mai adaton 0 átlépést ad, és az L2 három motívumát nem jelöli hibának |
| G6 | **`jelolt.py`:** bemenet egy igeszakasz (`--szakasz "1Móz 16:1-16"`). Ebből a TAHOT/TAGNT a szakasz minden Strongját adja, a grammatikai Strongok kiszűrve; ezt metszi az `elofordulasok.strong`-gal. Kimenet: jelentés. `--ir` esetén `nyitva` sorok a `jeloltek.tsv`-be, kulcs-duplikáció nélkül, `forras_kereses = jelolt.py <szakasz>`. **Soha nem ír `beépítve`-t.** A `formulaikus` azonosságú motívumok jelöltjei „pozicionális ellenőrzés kell" jelölést kapnak (L6). A `lekerdez.py` beolvasó- és tartomány-függvényeit importálja | bemenet a study-szöveg Strong-számai | A terv A3b-je a *szakaszban* szereplő Strongokat írja, nem a study-ban említetteket. Így a lépés független a study megfogalmazásától |
| G7 | **Két subagent** (F7 D3): `.claude/agents/tanito-kereso.md` (sonnet; WebSearch, WebFetch, Read, Write) és `.claude/agents/lexikai-scan.md` (haiku; Bash, Read — kizárólag `lekerdez.py` és `jelolt.py`). Az audit (B1, B10) és a C1 szkript marad. `.gitignore`: `.claude/*` mellett `!.claude/agents/` | a terv öt subagentje (5.1) | F7 D3: az audit determinisztikus, ott a modell csak hibaforrás |
| G8 | **Tanítói sablon:** `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md`. A kimenet helye `[study-mappa]/naplok/[motívum]_tanitoi_kereses.md`, a kereszthivatkozás-naplók mintájára. Az öt lépést **nem másolja**, a tematikus sablon „Nevesített tanítói egyezés-keresés módszere" szakaszára hivatkozik. Az üres eredmény elfogadott kimenet; idézet helyett összefoglalás, pontos mű- és helyazonosítással | kimenet a gyökér `naplok/`-ba, a terv 4.4 betűje szerint | A gyökér `naplok/` futási naplóké (§1). Egy igazság-forrás (F7 D7) |

---

## 3. Mi NEM az F8 hatóköre

- Hookok (`.claude/settings.json`: commit előtti `ellenoriz.py --all`, proveniencia-hook) — új N-tétel, ha kell.
- A `szerkeszto` és az `ellenor` subagent (terv 5.1).
- A Q2–Q6 gépesítése; a sablon-megfelelőség teljes ellenőrzése.
- A B7 élesíthetősége (`study`, `naplok` cél); N4, N7, N8, N9.
- A sorozat-tábla generálása (N11).
- A mai adaton talált szabálysértések **javítása**: az `ellenoriz.py` jelenti őket, a javítás külön tétel.
- HAMART-001 betöltése; az L2 három motívumának felülvizsgálata.

---

## 4. Tételek

### 1. menet — dokumentum és döntések *(Sonnet)*

#### F8.0 — kiindulás *(nem commitol)*
`main` = `origin/main` = `8511e35`, munkafa tiszta (az `F8_BRIEF.md` commitolatlanul állhat). A §1 táblájának újramérése; bármely eltérésnél megállás és jelentés.

#### F8.1 — a `MUNKAMENET.md` „Mi hiányzik" szakasza
Csere, szó szerint. **Régi:**

```
Öt tétel, mindegyik `F8`:

1. **`jelolt.py`** (A3b) — jelölt-generálás meglévő motívumokhoz.
2. **A B1 küszöbfigyelő önálló eszköze** — ma a `general.py` naplóblokkjában
   él, nem külön jelentés/kilépési kód.
3. **`_tanitoi_kereses.md` minta** (B9).
4. **A `lexikai-scan`/tanítói/audit subagentek** (B1, B9, B10, C1) — a
   `.claude/` alatt ma nincs egyetlen agent-definíció sem.
5. **A „sorozat-tábla"** (A7) — a tervben sehol nincs definiálva, l.
   `NYITOTT_FELADATOK.md` N10.
```

**Új:**

```
Hét tétel, mindegyik `F8` (l. `F8_BRIEF.md` §0):

1. **`jelolt.py`** (A3b) — jelölt-generálás meglévő motívumokhoz.
2. **A B1 küszöbfigyelő önálló eszköze** (`kuszob.py`) — ma a `general.py`
   csak számol, küszöböt nem hasonlít, kilépési kódot nem ad.
3. **`ellenoriz.py`** (B10) — az `adat/SEMA.md` §3 szabályai és a Q-kapu gépi
   része (Q1, Q7).
4. **`betolt.py`** (A3, B6) — study→adat átjáró; csak `beépítve` sort léptet elő.
5. **A tanítói keresés sablonja** (B9).
6. **Két subagent** (B4, B9) — `lexikai-scan` és `tanito-kereso`; az audit (B1,
   B10) és a C1 szkript marad (F7 D3).
7. **A „sorozat-tábla"** (A7) — definiálva az F8.2-ben, l. `NYITOTT_FELADATOK.md` N10.
```

A lépéstábla sorai ebben a menetben **nem** változnak.

#### F8.2 — sorozat-tábla (G1)
- `NYITOTT_FELADATOK.md` N10: **lezárt** jelölés, dátummal és a definícióval (a napló „Feldolgozott igeszakaszok listája", kézi).
- Új tétel a kézi részbe, **N11**: a sorozat-tábla generálása, a G1 elvetett alternatívájával mint lehetséges megoldással.
- `ATALAKITASI_TERV.md.md` 486. sor: a *(nem definiált, nem implementált — …)* megjelölés helyébe *(= a napló „Feldolgozott igeszakaszok listája", kézi — l. `NYITOTT_FELADATOK.md` N10, N11)* kerül.
- `MUNKAMENET.md` A7 sor, Megjegyzés oszlop: ugyanez a definíció.
- A GENERÁLT blokkok nem módosulnak.

#### F8.3 — `kulcsszavak.tsv` séma (G2a)
- `adat/SEMA.md`: új **2.8** alszakasz a G2(a) mezőivel, kulcs: `tanulmany` + `igehely` + `strong`. Kimondja, hogy a tábla átmeneti: az `id` az A4-ben születik a `jeloltek`-ben.
- `adat/kulcsszavak.tsv`: csak komment-sor és fejléc, adatsor nélkül.

### 2. menet — eszközök *(Sonnet; a v3 nyitó promptjával)*

- **F8.4 — `eszkozok/kuszob.py`** a G5 szerint.
- **F8.5 — `eszkozok/ellenoriz.py`** a G4 szerint.
- **F8.6 — `eszkozok/jelolt.py`** a G6 szerint.
- **F8.7 — tanítói sablon** a G8 szerint.

Mindegyik tétel a saját `MUNKAMENET.md` sorát is frissíti. A „Ma mivel fut" oszlopba a tényleges parancs kerül (B1, A3b, B10). A B9 sor Megjegyzése a sablon helyét kapja; az oszlopa a 3. menetig `F8 — nincs eszköz` marad.

### 3. menet — átjáró és agentek *(Sonnet; a v4 nyitó promptjával)*

- **F8.8 — `eszkozok/betolt.py`** a G2 szerint, két alparanccsal (`kulcsszo`, `beepit`). Az A3 és a B6 sor frissül.
- **F8.9 — subagentek** a G7 szerint, `.gitignore`-ral. A B9 sor frissül; a `MUNKAMENET.md` „Szereposztás — a mai valóság" szakasza átíródik.
- **F8.10 — lezárás.** A „Mi hiányzik" szakasz: „Az F8 óta nincs `F8`-jelölt hiány; nyitva: N11 és a §3 tételei."

---

## 5. Elfogadási kritériumok

### 1. menet

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | Kiindulás mérve | a §1 minden sora jelentve, egyezik vagy eltérés-jelentés + megállás |
| K2 | „Mi hiányzik" hét tétel | a régi blokk nincs meg; az új blokk szó szerint megvan; `grep -c 'F8 — nincs eszköz' MUNKAMENET.md` = 5 (változatlan) |
| K3 | N10 lezárva, N11 felvéve | mindkettő megvan; a GENERÁLT blokkon a `git diff` 0 sor |
| K4 | Terv és runbook A7 átvezetve | a terv 486. sora és a `MUNKAMENET.md` A7 sora a definíciót hordozza; a tervben más sor nem változik |
| K5 | SEMA 2.8 + üres tábla | a 2.8 megvan; `adat/kulcsszavak.tsv` adatsora 0; a többi `adat/*.tsv` bájtra változatlan |
| K6 | Commitok | a §6 szerint, a hiányzó és a plusz fájlok is jelentve; `git status --porcelain` üres |

### 2. és 3. menet — a v3/v4 részletezi; a kötelező minimum

| # | Kritérium |
|---|---|
| K7 | `kuszob.py` a mai adaton 0 átlépés, kód 0; egy ideiglenes próba-TSV-n (nem az `adat/`-ban) egy átlépés, kód 1 |
| K8 | `ellenoriz.py` a mai adaton lefut; a talált sértéseket jelenti, **nem javítja**; a Q2–Q6 soha nem „megfelelt" |
| K9 | `jelolt.py --szakasz "1Móz 7:1-24"` jelentésében a TEREMT-001 / H8415 / 1Móz 7:11 pár szerepel, „már előfordulás" jelöléssel; `--ir` nélkül az `adat/` változatlan |
| K10 | `betolt.py beepit` elutasít minden nem `beépítve` sort, és hiányzó kötelező mezőnél semmit nem ír |
| K11 | F8 végén `grep -c 'F8 — nincs eszköz' MUNKAMENET.md` = 0; minden megnevezett eszköz létezik (`test -f`) |
| K12 | Az új eszközök a meglévő függvényeket importálják (`general`, `lekerdez`); a küszöb- és tartomány-logika nincs lemásolva |

---

## 6. Commit és push — 1. menet

| Commit-üzenet | Fájlok |
|---|---|
| `F8.1: MUNKAMENET.md — a hiánylista hét tételre igazítva` | `MUNKAMENET.md` |
| `F8.2: sorozat-tábla definiálva — N10 lezárva, N11 felvéve` | `NYITOTT_FELADATOK.md`, `ATALAKITASI_TERV.md.md`, `MUNKAMENET.md` |
| `F8.3: SEMA 2.8 — kulcsszavak.tsv átmeneti tábla` | `adat/SEMA.md`, `adat/kulcsszavak.tsv` |
| `F8_BRIEF.md v2: az F8 brief, a G1–G8 döntésekkel` | `F8_BRIEF.md` |

Az F8.0 nem commitol. **Push csak külön kérésre.** A 2. menet commit-táblája a v3-ban, a 3. menetté a v4-ben.

---

## 7. Nyitó prompt — 1. menet *(Sonnet)*

```
Olvasd el a CLAUDE.md-t, majd az F8_BRIEF.md-t teljes egészében.

0. F8.0: main = origin/main = 8511e35, munkafa tiszta (az F8_BRIEF.md
   commitolatlanul állhat). Mérd újra a §1 tábláját. Ha bármi eltér, ÁLLJ MEG.
1. F8.1 — a csere SZÓ SZERINT a §4 régi/új blokkja szerint. K2.
2. F8.2 a G1 szerint. K3, K4.
3. F8.3 a G2(a) szerint. K5.
4. Commitok a §6 táblája szerint, a brief-committal együtt. K6.

A 2. és 3. menet tételeihez (F8.4–F8.10) NE nyúlj.
Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Push nincs. Zárójelentés: hash-ek, K1-K6 kritériumonként, külön sorban,
kihagyás nélkül, és minden eltérés — külön kiemelve a hiányzó és a plusz
fájlokat a §6 táblájához képest.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Hét tétel, a lépéstábla és a „Mi hiányzik" uniója | A két lista eltérő szűrővel jelöl; külön-külön egyik sem teljes (§0) |
| D2 | Négy lépés: F8.0 + három menet (dokumentum/döntés → eszközök → átjáró/agentek) | Az agent az eszközt hívja; a `betolt.py` a legnagyobb, és adatmodell-döntésen áll |
| D3 | Az F7 D3 érvényben marad: két subagent | l. G7 |
| D4 | A G1–G8 jóváhagyva (2026-09-21), mind a javasolt változatban; ez a v2, az 1. menet ebből fut | A G0-minta az F4 és az F6 óta |
| D5 | A mai adaton talált szabálysértést az F8 nem javítja | Eszköz-fázis, nem adatjavító fázis; a javítás külön, látható tétel legyen |
| D6 | Az új eszközök importálnak, nem másolnak | Egy igazság-forrás (F7 D7, N9 tanulsága) |
| D7 | Próba alapértelmezés, élesítés `--ir`-rel; kilépési kód 0/1/2 | A `general.py` meglévő konvenciója |
| D8 | A `MUNKAMENET.md` sorai tételenként frissülnek, nem a fázis végén | A runbook soha ne hivatkozzon nem létező eszközre, és ne hallgasson el meglévőt (F7 D6) |
| D9 | A 2. menet részletei a v3-ba, a 3. menetéi a v4-be kerülnek | Az 1. menet eredménye alakítja őket; a v2 a jóváhagyási verzió |
