# F7 — Üzemmenet: a munkamenet rögzítése

*Készítette: chat-menet (Opus 5), 2026-09-20, **v1**.*
*Kiindulási állapot: `main` = `origin/main` = `e8a7259` (az F6 lezárva és pusholva).*

---

## 0. Miért tér el ez a brief a terv F7-szakaszától

A terv F7-je három mondat (464–467. sor): az F0–F6 után „a 7. ponti munkafolyamat lép életbe". A tényleges tartalom tehát a **7. pont** (470–522. sor), amely 23 lépést ír le három szakaszban (A1–A7 az A3b-vel és A6b-vel, B1–B10, C1–C4).

A 7. pont öt dolgot feltételez meglévőként, amely a `e8a7259`-en **nem létezik**: `jelolt.py` (A3b), a B1 küszöbfigyelő önálló eszköze, `_tanitoi_kereses.md` minta (B9), a `lexikai-scan`/tanítói/audit subagentek (B1, B9, B10, C1), és a „sorozat-tábla" (A7), amely a tervben sehol nincs definiálva.

Emellett a terv három lexikon-állítása az F6 óta nem igaz (l. §1 L2).

**Ezért az F7 hatóköre: a munkamenet rögzítése dokumentumként, a terv átvezetése, és a hiányok megjelölése.** A hiányzó eszközök megépítése az F8 dolga. Egy nem létező eszközre hivatkozó runbook rosszabb, mint a hiány bevallása — és eszközt nem lehet nem létező specifikáció ellen írni.

---

## 1. Kiindulási állapot — mérve, `e8a7259`

A §1 számai a 2026.09.20-i mérésből valók, változtatás nélkül.

| Mit | Mért érték |
|---|---|
| `CLAUDE.md` | 179 sor, 9 főcím; a „Kutatási menet — a hét lépés" az 50–62. soron |
| `eszkozok/` | 41 `.py` szkript |
| `general.py --cel` | `naplo`, `index`, `naplok`, `study`, `nyitott`, `lexikon`, `mind` |
| `ELESITHETO` | `{naplo, index, nyitott, lexikon}` — a `naplok` és a `study` **nem** élesíthető |
| ⭐-küszöb számítása | `general.py`: `fo_elofordulas_csoportok()` + `render_naplo_kuszob()` |
| `gate.py` | `collision_report`, `pair_overlap_report`, `subset_report` — küszöböt nem számol |
| `lekerdez.py` | `cmd_gerinc`, `cmd_scan`, `cmd_kollokacio`, `cmd_igealak`, `cmd_lxx_hid`, `cmd_tsk`, `cmd_karoli`, `cmd_domen` |
| `adat/` adatsorok | `motivumok` 7, `elofordulasok` 201, `kapcsolatok` 32, `jeloltek` 221, `lexikon_hivatkozasok` 5, `datasetek` 68, `grammatikai_strongok` 85 |
| `sablonok/` | 10 fájl; a lexikon-sablon **v2** |
| `lexikon/` | 7 `_TUDOMANYOS.md`; éles `_OLVASHATO.md` egy sincs |
| `.claude/` | csak `worktrees/gifted-almeida-e4ba62` (F1 előtti repó-másolat); nincs `agents/`, nincs `settings.json` |
| `Alap_bejegyzes_kigyujtes_v1_PISZKOZAT.tsv` | 124 sor; **egyetlen szkript sem hivatkozik rá**, csak a terv |
| `NYITOTT_FELADATOK.md` | N1–N6 a 25–30. soron, N7/N8/N9 a 32./43./49. soron |

**Négy lelet:**

- **L1 — a B1 nagyrészt megvan.** A ⭐-számítás nem hiányzik, csak nem külön eszköz: a `general.py` naplóblokkjában él. Az F8 B1-tétele ezért jelentés- és kilépési kód-burok a meglévő logika köré, nem új számítás.
- **L2 — három tervbeli lexikon-állítás megdőlt az F6-ban.** (a) A `[ID]_TUDOMANYOS.md` nem 0–8-ig generált: a ténylegesen generált szakaszok 0, 1, 2, 3, 4, 5 és **9**. (b) A 9. szakasz nem „Nyitott kérdések", hanem „Források és licencek", és teljes egészében generált; a „Nyitott kérdések és séma-korlátok" a **8.**, kézi. (c) A C2 két kézi szakaszt nevez meg, miközben a v2 sablon szerint hét kézi rész van (1/b, „Miért fontos ez a lelet", „Minősítés", „Alátámasztás", 6, 7, 8).
- **L3 — az N4 és az N5 elavult.** Mindkettő a Thayert, az LSJ-t és a SECE-t tisztázatlan licencűként kezeli; az F6.5b óta a Thayer és a SECE `közkincs`, az LSJ `CC BY-SA 3.0`, `tisztazatlan` pedig csak az LXX-kivonat (és az MCGED védett mű, saját megjelöléssel).
- **L4 — az A3 kiváltása már megtörtént, csak nincs kimondva.** A visszabányászó piszkozat-TSV-re egyetlen szkript sem hivatkozik; élő csak a tervbeli említése. Az F7-ben tehát dokumentum-aktus, nem eszközcsere.

---

## 2. Rögzített döntések

| # | Döntés | Indok |
|---|---|---|
| D1 | Az F7 dokumentum-fázis; a hiányzó eszközök az F8-ba kerülnek | A hiányzó darabok egy része (sorozat-tábla, tanítói minta) ma nem specifikáció, csak névhivatkozás |
| D2 | A runbook külön `MUNKAMENET.md`, a `CLAUDE.md` egy hivatkozó sort kap | A `CLAUDE.md` belépési pont, és az értéke a rövidség; egy 23 lépéses ív megfojtaná |
| D3 | A három subagent-szerep nem egyforma: az audit (B1, B10) **szkript**, a `lexikai-scan` **szkript + vékony burok**, a tanítói (B9) **valódi subagent** | Az audit determinisztikus számolás, ott a modell csak hibaforrás; a scan-nél a szerep kontextus-védelem; a tanítói lépés tartalmi ítélet |
| D4 | A „sorozat-tábla" nem törlődik, hanem megjelölést kap + N10 lesz | A vak törlés elveszítené a mögötte lévő szándékot, a rekonstrukció pedig találgatás volna |
| D5 | Az N4 szűkül, az N5 lezárul | Az F6.5b lépte túl őket; a runbook rájuk hivatkozik, tehát előbb igazzá kell tenni őket |
| D6 | A runbook nem nevez meg futtathatóként nem létező eszközt; minden hiány `F8` jelölést kap | Az F6.5a tanulsága: a széttartó forrásokat a végrehajtás betű szerint követi |
| D7 | A `CLAUDE.md` hét lépése és a 4.6-gate négy kérdése nem másolódik át, csak hivatkozás | Egy igazság-forrás; a duplikátum előbb-utóbb szétcsúszik (v. ö. N9) |

---

## 3. Mi NEM az F7 hatóköre

- Bármely hiányzó eszköz megírása (`jelolt.py`, B1-burok, tanítói minta, subagent-definíciók) — F8.
- Az A4/B5 megállás **kikényszerítése** kóddal — F8; az F7 csak leírja a szabályt.
- A lexikon OLVASHATÓ változatának megírása — kézi, motívumonként, külön menet.
- Az N1–N3, N6–N9 tételek érdemi megoldása.
- A `.claude/worktrees/gifted-almeida-e4ba62` sorsa — külön kérdés, nem F7.

---

## 4. Tételek

### F7.0 — kiindulás *(nem commitol)*
`main` = `origin/main` = `e8a7259`, munkafa tiszta. Ha nem, megállás.

### F7.1 — N4 szűkítése, N5 lezárása
A `NYITOTT_FELADATOK.md` kézi részében a 28. sor (N4) szövegéből a Thayer, az LSJ és a SECE kikerül: a tétel az **LXX-kivonatra és az MCGED-re** szűkül. A 29. sor (N5) **lezárt** jelölést kap, a lezárás dátumával és az F6.5b commit-hashével (`3099114`), megtartva a §1.6 fenntartását: a besorolás a szerző forrásoldaláról való, nem a letöltött fájlokhoz csatolt licencszövegből. A GENERÁLT blokk nem módosul.

### F7.2 — `MUNKAMENET.md`
Új fájl a repó gyökerében. Kötelező tartalma:

1. **Fejléc:** mire való, mire nem, és hogy a hét lépés és a 4.6-gate a `CLAUDE.md`-ben áll (D7).
2. **Mind a 23 lépés saját sorral**, a terv 7. pontjának sorrendjében és azonosítóival (A1, A2, A3, A3b, A4, A5, A6, A6b, A7, B1–B10, C1–C4), lépésenként négy adattal: **ki** végzi (kutató / ember / végrehajtó / audit), **kimenet**, **ma mivel fut**, **megjegyzés**.
3. A „ma mivel fut" oszlopban csak három érték állhat: konkrét, ma létező parancs (pl. `eszkozok/general.py --cel naplo`); `kézi`; vagy `F8 — nincs eszköz`. Nem létező eszköz futtathatóként nem szerepelhet (D6).
4. **A4 és B5 kiemelve** mint kötelező emberi megállási pont: a menet itt megáll és kérdez, akkor is, ha a válasz nyilvánvalónak látszik. Indoklásként a 2026.09.11-i modell-összehasonlítás tanulsága (mindkét ág némán átlépett egy besorolási döntésen).
5. A drága modellt igénylő kilenc lépés (A1, A2, A4, A5, A6, B3, B8, C2, C3) megjelölése.
6. **Szereposztás a D3 szerint**, a mai valósággal: a `.claude/` alatt ma nincs agent-definíció.
7. A generátor-tények a §1 szerint, külön kiemelve, hogy a `naplok` és a `study` cél **nem élesíthető**.
8. A lexikon-lépések (C1, C2) az L2 szerinti helyes szakasz-listával.
9. Záró szakasz: **mi hiányzik az üzemmenetből ma** — az öt hiány felsorolása, mindegyiknél `F8`.

### F7.3 — `CLAUDE.md` hivatkozó sor
Egyetlen sor a „Kutatási menet — a hét lépés" szakasz elején vagy végén: a hét lépés a B2–B6 és B9 belső protokollja, a teljes A/B/C ív a `MUNKAMENET.md`-ben áll. A fájl máshol nem módosul.

### F7.4 — a terv átvezetése
Az `ATALAKITASI_TERV.md.md`-ben:
- a 462. sor és a 7. pont C1/C2 sorai az L2 szerint javulnak (generált: 0–5 és 9; a 8. a Nyitott kérdések, kézi; a C2 hét kézi részt nevez meg);
- az A7 „sorozat-tábla" említése megjelölést kap: *(nem definiált, nem implementált — l. `NYITOTT_FELADATOK.md` N10)*;
- az F7-szakasz (464–467. sor) egy sorral kiegészül: az üzemmenet leírása a `MUNKAMENET.md`-ben él.

Más tervbeli szöveg nem módosul.

### F7.5 — a piszkozat-TSV archív jelölése
A `motivumlog/Alap_bejegyzes_kigyujtes_v1_PISZKOZAT.tsv` mellett a `_README.md` megkapja, hogy a fájl **archív**: a visszabányászó módszert az A3 váltotta ki, gépi hivatkozás nincs rá (mérve: 0 szkript). A TSV tartalma nem módosul.

### F7.6 — N10
Új tétel a `NYITOTT_FELADATOK.md` kézi részébe: a „sorozat-tábla" (terv A7) nincs definiálva és nincs implementálva; eldöntendő, hogy definiálandó artefaktum-e vagy törlendő fogalom. A GENERÁLT blokk nem módosul.

---

## 5. Elfogadási kritériumok

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | N4 szűkítve, N5 lezárva | a 28. sorban nincs `Thayer`, `LSJ`, `SECE`; a 29. sor `lezárt` jelölést és a `3099114` hashet viseli; `git diff` a GENERÁLT blokkon 0 sor |
| K2 | Mind a 23 lépés megvan | `grep -c` az azonosítókra: A1, A2, A3, A3b, A4, A5, A6, A6b, A7, B1–B10, C1–C4 — mind ≥ 1, egyik sem hiányzik |
| K3 | Nincs kitalált eszköz | a „ma mivel fut" oszlop minden értéke a három megengedett alak egyike; minden megnevezett szkript létezik (`test -f`); a `jelolt.py`, a `_tanitoi_kereses.md` és a subagentek kizárólag `F8` jelöléssel szerepelnek |
| K4 | A4/B5 kiemelve | mindkettő megállási pontként jelölve, az indoklással együtt |
| K5 | Nincs duplikáció | a hét lépés szövege és a 4.6-gate négy kérdése nem szerepel a `MUNKAMENET.md`-ben, csak hivatkozásként |
| K6 | Generátor-tények egyeznek | `ELESITHETO` négy célja, a `naplok`/`study` nem élesíthetősége és a ⭐ helye a §1 szerint szerepel |
| K7 | `CLAUDE.md` érintetlen a hivatkozó soron kívül | `git diff CLAUDE.md` legfeljebb egy hozzáadott sor |
| K8 | Terv átvezetve | a 462. sor és a C1/C2 javítva; a sorozat-tábla megjelölve; `git diff` csak ezeket a helyeket érinti |
| K9 | N10 felvéve | `grep -c "N10"` ≥ 1; a GENERÁLT blokk 0 sor |
| K10 | Piszkozat archív jelölés | a `_README.md`-ben szerepel az archív státusz; a TSV bájtra változatlan |
| K11 | Commitok | a §6 táblája szerint, **hiányzó és plusz fájl is jelentve**; `git status --porcelain` üres |

---

## 6. Commit és push

| Commit-üzenet | Fájlok |
|---|---|
| `F7.1: NYITOTT_FELADATOK.md — N4 szűkítése, N5 lezárása` | `NYITOTT_FELADATOK.md` |
| `F7.2-F7.3: MUNKAMENET.md — az A/B/C ív rögzítése + CLAUDE.md hivatkozás` | `MUNKAMENET.md`, `CLAUDE.md` |
| `F7.4: ATALAKITASI_TERV.md.md — lexikon-állítások és sorozat-tábla átvezetése` | `ATALAKITASI_TERV.md.md` |
| `F7.5: a visszabányászó piszkozat archív jelölése` | `motivumlog/Alap_bejegyzes_kigyujtes_v1_PISZKOZAT_README.md` |
| `F7.6: NYITOTT_FELADATOK.md — N10 sorozat-tábla` | `NYITOTT_FELADATOK.md` |

Az F7.0 nem commitol. A brief saját commitot kap tétel-azonosító nélkül (`F7_BRIEF.md v1: …`). **Push csak külön kérésre.**

---

## 7. Nyitó prompt *(Sonnet)*

```
Olvasd el a CLAUDE.md-t, majd az F7_BRIEF.md-t teljes egészében.

0. main = origin/main = e8a7259, munkafa tiszta (az F7_BRIEF.md
   commitolatlanul állhat). Ha nem, állj meg.
1. F7.1 a §4 szerint. K1.
2. F7.2 és F7.3 a §4 szerint. K2-K7.
3. F7.4, F7.5, F7.6. K8, K9, K10.
4. Commitok a §6 táblája szerint. K11. Külön commit: F7_BRIEF.md v1.

A MUNKAMENET.md tartalmát te írod, de KIZÁRÓLAG a §1 mért tényeiből és a
terv 7. pontjából. Ha egy lépésről nem tudod megmondani, ma mivel fut,
az "F8 — nincs eszköz" — ne találgass és ne vezess le eszközt.
Ha a §1 bármelyik mért értéke ma másnak bizonyul, ÁLLJ MEG és jelentsd.

Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Push nincs. Zárójelentés: hash-ek, K1-K11 kritériumonként (mindegyik külön
sorban, kihagyás nélkül), és minden eltérés — külön kiemelve a hiányzó és
a plusz fájlokat a §6 táblájához képest.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1–D7 | l. §2 | — |
| D8 | A `MUNKAMENET.md` tartalmát a végrehajtó menet írja, nem a brief | A brief a szerkezetet és a kötelező elemeket rögzíti; a 23 soros tábla kitöltése mért adatból mechanikus, és a K2–K6 ellenőrzi |
| D9 | Az F7.2 és az F7.3 egy commitban | A hivatkozó sor önmagában értelmetlen a hivatkozott fájl nélkül |
