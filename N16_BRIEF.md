# N16_BRIEF.md — v1

ISTENTISZT-001: a hiányzó ÚSZ-i idézőhelyek betöltése (N16) + a pilot szótári anyagának pótlása a lexikon-oldalon

## 0. Kiindulás — mérve, `6ad18cf` (2026.09.21)

- Az `elofordulasok.tsv` 29 ISTENTISZT-001 sorából hiányzik az ApCsel 2:21 és a Róm 10:13. A `kapcsolatok.tsv` egyetlen sora (Jóel 2:32 → Róm 10:14, „Beteljesedés", „szó szerinti LXX-idézés-lánc (2:32⇒Róm 10:13⇒10:14)") vonja össze a lezárt study (`tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`) kapcsolat-táblájának három sorát (Jóel 2:32 → ApCsel 2:21; Jóel 2:32 → Róm 10:13; Róm 10:13 → Róm 10:14).
- A `lexikon/ISTENTISZT-001_TUDOMANYOS.md` 5 ⚠ ELTÉRÉS-jelölést tartalmaz, a `_OLVASHATO.md` 2-t.
- A LEX-brief G5-je tévesen feltételezte, hogy a pilot szótári részeit a generált 2. szakasz fedi. Valójában csak 4 jelentést fed (TBESG G1941 1–2, BDB H7121 2.c és 3). A pilot 2–4. szakasza (teljes BDB H7121 és H8034, teljes TBESG G1941/G2564/G0994 Thayerrel, MCGED/SECE/LSJ, TBESH+SECE) csak a `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` 173–340. sorában él. A SEMA 2.5 szerint a `lexikon_hivatkozasok.szoveg_en` „rövid kivonat, nem teljes szócikk", ezért a teljes szócikkek nem adat-útra, hanem kézi alszakaszba kerülnek.
- A `generalt_proba/` a `--cel mind`-dal 20 fájlban változna (köztük egy N14 óta elavult HAMART-001 hiánylista-blokk). Ez nem hatókör.

## 1. A feladat

(a) Az ApCsel 2:21 és a Róm 10:13 betöltése a `jeloltek.tsv` → munkalap → `betolt.py beepit` úton, és a kapcsolat szétbontása a study szerinti három sorra.
(b) A négy érintett generált kimenet frissítése.
(c) A lexikon-oldal ⚠ ELTÉRÉS-jelöléseinek rendezése.
(d) A pilot szótári anyagának (2–4. szakasz) szó szerinti átemelése egy új kézi alszakaszba.
(e) Az N16 lezárása.

## 2. G-döntések — jóváhagyva (2026.09.21)

- **G1:** a két sor tartalmát a brief rögzíti (4. pont), a végrehajtó nem fogalmaz. A proveniencia `scope=manual`, forrás a study, ts a study Jóel-idézőlánc-körének dátuma (2026-09-05). Az ISTENTISZT-001 már a `RETROAKTIV_IDK` listán van.
- **G2:** a kapcsolat szétbontása szó szerint a study kapcsolat-táblájának (107–109. sor) típusait és funkció-szövegeit követi. Bizonyosság: `magas`, PaRDeS: `Remez`, mint az eredeti sornál.
- **G3:** generálás csak a `naplo`, `index`, `nyitott` és `lexikon --id ISTENTISZT-001` célokra. `--cel mind` és a `generalt_proba/` tilos.
- **G4:** az ApCsel 2:21 / Róm 10:13 miatti ⚠ ELTÉRÉS-jelölések törlődnek (a szöveg visszaáll a pilot szó szerinti alakjára). A 21 igehelyes jelölések maradnak, a bennük álló „29" szám „31"-re frissül. A „15 emberi-invokációs eset" jelölés szövege a 4. pontban adott mondatra cserélődik (a korábbi „27" becslés volt, nem mérés).
- **G5 (a LEX-brief G5-jének helyesbítése):** a pilot 2–4. szakasza (173–340. sor) szó szerint egy új kézi alszakaszba kerül. Kivétel az a három bekezdés, amely a LEX.2-ben már a „Miért fontos ez a lelet" helyre került (G1941 „Miért fontos", G0994 „Miért fontos", „Kiemelt módszertani jelentőség"): ezek helyén egysoros utalás áll, hogy ne legyen kétszer. Megengedett változtatás csak a LEX-brief G4/1–2 szerinti: a címszintek eltolása és a belső szakaszhivatkozások igazítása. A nem feloldható hivatkozás változatlan marad, és a jelentésbe kerül.
- **G6:** az alszakasz végére a szótáranként kötelező forrás- és licencmegjelölés kerül, szó szerint a 4. pont szerint (MCGED: F6 D16/K26; LSJ: Perseus). A generált 9. szakasz ezeket nem látja, mert kézi szövegből idéznek.
- **G7:** a G2564 és a G0994 nem lesz motívum-token. A szócikkeik csak a 2/b-ben, pilot-idézetként szerepelnek.

## 3. Mi NEM a hatókör

- `generalt_proba/` (a HAMART-001 hiánylista-drift külön tétel lehet), `--cel study`/`naplok`/`mind`.
- `lexikon_hivatkozasok.tsv` bővítése, új motívum-tokenek.
- A study (`tematikus_lezart/…`) szövegének módosítása.
- A többi motívum lexikon-oldala, N11, N13, N15.

## 4. Tételek

### N16.0 — kiindulás *(nem commitol)*
HEAD a brief-commit, szülője `6ad18cf`. `git status` tiszta. A 0. pont számainak visszamérése, és az `ellenoriz.py` összesítő: `RENDBEN: 6 | SÉRTÉS: 0 | KÉZI: 3 | JELENTÉS: 1`.

### N16.1 — adat (jelöltek, munkalap, beépítés, kapcsolatok)
Minden TSV-írás `'\t'.join()`-nal (CLAUDE.md). Mezősorrend a fájl fejléce szerint.

**1. `adat/jeloltek.tsv` végére két sor** (`id | igehely | forras_kereses | dontes | indoklas | karoli_szo | azonositas_modja | megbizhatosag | datum`):

| mező | 1. sor | 2. sor |
|---|---|---|
| id | ISTENTISZT-001 | ISTENTISZT-001 |
| igehely | ApCsel 2:21 | Róm 10:13 |
| forras_kereses | N16: a study kapcsolat-táblájából (Jóel 2:32 → ApCsel 2:21), retroaktív | N16: a study kapcsolat-táblájából (Jóel 2:32 → Róm 10:13), retroaktív |
| dontes | beépítve | beépítve |
| indoklas | A study (Segitsegul_hivni_az_Urat_tematikus.md) kapcsolat-táblája szerint a Jóel 2:32 szó szerinti LXX-idézete (Beteljesedés); az F3.1 betöltés a Jóel 2:32 sorba vonta össze, önálló sorként nem töltötte be. | A study (Segitsegul_hivni_az_Urat_tematikus.md) kapcsolat-táblája szerint a Jóel 2:32 szó szerinti LXX-idézete (Beteljesedés), a Róm 10:14 közvetlen előzménye; az F3.1 betöltés a Jóel 2:32 sorba vonta össze, önálló sorként nem töltötte be. |
| karoli_szo | az Úrnak nevét segítségül hívja | segítségül hívja az Úr nevét |
| azonositas_modja | tartalom-alapú | tartalom-alapú |
| megbizhatosag | magas | magas |
| datum | 2026.09.21 | 2026.09.21 |

**2. Munkalap:** `naplok/N16_istentiszt_elofordulasok_munkalap.tsv`. Első sor: `# N16.1 munkalap -- betolt.py beepit formátumában. Sema: adat/SEMA.md 2.2`, második sor az `elofordulasok.tsv` fejléce, utána két sor:

| mező | 1. sor | 2. sor |
|---|---|---|
| id | ISTENTISZT-001 | ISTENTISZT-001 |
| igehely | ApCsel 2:21 | Róm 10:13 |
| kapcsolodas | Péter pünkösdi beszéde szó szerint idézi a LXX Jóel 2:32-t: "mindaz, a ki az Úrnak nevét segítségül hívja, megtartatik." | Pál szó szerint idézi a LXX Jóel 2:32-t: "minden, a ki segítségül hívja az Úr nevét, megtartatik." — erre épül a 10:14 kérdéssora. |
| pardes_szint | Remez | Remez |
| funkcio | 🎯 előkép/beteljesedés (idézet) — az ÚSZ szó szerint idézi a Jóel 2:32-t | 🎯 előkép/beteljesedés (idézet) — az ÚSZ szó szerint idézi a Jóel 2:32-t |
| gerinc_elem | G1941 | G1941 |
| strong | G1941 | G1941 |
| lexikon_szotar | TBESG | TBESG |
| lexikon_entry_id | G1941 | G1941 |
| jelentes_szam | 2 | 2 |
| jelentes_en | *(üres)* | *(üres)* |
| jelentes_hu | segítségül hívni, invokálni | segítségül hívni, invokálni |
| karoli_szo | az Úrnak nevét segítségül hívja | segítségül hívja az Úr nevét |
| azonositas_modja | tartalom-alapú | tartalom-alapú |
| megbizhatosag | magas | magas |
| proveniencia | scope=manual \| forras=Segitsegul_hivni_az_Urat_tematikus.md \| ts=2026-09-05 | *(ugyanaz)* |
| igazolas | nincs | nincs |
| fo_elofordulas | *(üres)* | *(üres)* |
| felmerult_tanulmany | *(üres)* | *(üres)* |

(A táblában a `\|` csak markdown-escape; a mezőben szóköz–függőleges vonal–szóköz áll.)

**3.** `python eszkozok/betolt.py beepit --munkalap naplok/N16_istentiszt_elofordulasok_munkalap.tsv` → „RENDBEN -- mind a 2 sor átmegy", majd ugyanez `--ir`-rel → „2 új elofordulasok.tsv sor íródott".

**4. `adat/kapcsolatok.tsv`:** a `Jóel 2:32 | Róm 10:14 | ISTENTISZT-001 | Beteljesedés | szó szerinti LXX-idézés-lánc (2:32⇒Róm 10:13⇒10:14) | magas | Remez` sor helyére, ugyanott, három sor:

| forras_igehely | cel_igehely | id | tipus | funkcio | bizonyossag | pardes_szint |
|---|---|---|---|---|---|---|
| Jóel 2:32 | ApCsel 2:21 | ISTENTISZT-001 | Beteljesedés | szó szerinti LXX-idézés, ÓSZ-prófécia → ÚSZ-beteljesedés | magas | Remez |
| Jóel 2:32 | Róm 10:13 | ISTENTISZT-001 | Beteljesedés | szó szerinti LXX-idézés, ÓSZ-prófécia → ÚSZ-beteljesedés | magas | Remez |
| Róm 10:13 | Róm 10:14 | ISTENTISZT-001 | Párhuzam | azonos szereposztás, közvetlen folytatás ugyanabban a szakaszban | magas | Remez |

**5.** `ellenoriz.py` és `gate.py` futtatása.

### N16.2 — generálás (csak G3 szerint)
`general.py --cel naplo --ir`, `--cel index --ir`, `--cel nyitott --ir`, `--cel lexikon --id ISTENTISZT-001 --ir`. Utána `git status` csak ezeket mutathatja: `motivumlog/PaRDeS_motivumok.md`, `Lezart_tematikus_tanulmanyok_index.md`, `NYITOTT_FELADATOK.md`, `lexikon/ISTENTISZT-001_TUDOMANYOS.md`.

### N16.3 — ⚠ ELTÉRÉS-jelölések rendezése
A `lexikon/ISTENTISZT-001_TUDOMANYOS.md`-ben:
- Az Alátámasztás-tábla két sorának végéről („1Móz 4:26 → Jóel 2:32 → ApCsel 2:21 / Róm 10:13" és „Róm 10:13 → Róm 10:14") a ⚠ ELTÉRÉS-szöveg törlődik. A sor a pilot szó szerinti alakjára áll vissza, a záró `|` megmarad.
- A két „21 igehelyre lefuttatva" jelölésben a „29" → „31".
- A „15 emberi-invokációs eset" jelölés teljes szövege erre cserélődik: `⚠ ELTÉRÉS: a táblázat „15 emberi-invokációs eset" száma a pilot 2026.09.06-i, a 2026.09.09-i 7-soros bővítés előtti állapotára vonatkozik; a jelenlegi „Előfordulások" tábla 31 igehelyet tartalmaz, az emberi-invokációs esetek száma rajta nem mért.`
- A 8. szakasz („Nyitott kérdések") 3. pontjában a `(l. a` … `"Miért fontos ez a lelet").` zárójeles rész helyére ez kerül: `(l. 2/b. szakasz).` (A LEX.2 betoldott félmondata ezzel megszűnik.)

A `lexikon/ISTENTISZT-001_OLVASHATO.md`-ben mindkét ⚠ ELTÉRÉS-szöveg törlődik (az idézet sorvégi megjegyzése, valamint a Mermaid-diagram utáni üres sor és megjegyzés-sor). A fájl így bájtra azonos lesz a `motivumlog/lexikon_pilot/ISTENTISZT-001_OLVASHATO.md`-vel.

### N16.4 — 2/b. alszakasz: a pilot szótári anyaga
A `lexikon/ISTENTISZT-001_TUDOMANYOS.md`-ben a 2. szakasz szócikk-blokkjának `GENERÁLT-VÉGE` sora után, a `### Miért fontos ez a lelet *(kézi)*` elé, egy üres sorral körülvéve:

1. Fejléc: `### 2/b. Teljes szótári anyag — a pilotból *(kézi)*`, alatta egy sor: `*A \`motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md\` 2–4. szakaszának szó szerinti átvétele (N16, 2026.09.21).*`
2. A pilot 173–340. sora szó szerint. A címszintek eltolása: pilot `## ` → `#### `, pilot `### ` → `##### `. A „2. / 3. / 4." sorszám a címekben megmarad.
3. Kivétel: a pilot 242. sorában kezdődő („**Miért fontos ez a lelet:** a Thayer **explicit**…"), a 287. sorában kezdődő („**Miért fontos ez a lelet:** a Thayer megerősíti…") és a 309. sorában kezdődő („**Kiemelt módszertani jelentőség:**…") bekezdés helyére rendre egy sor kerül: `*(L. lent: Miért fontos ez a lelet — G1941.)*`, `*(L. lent: Miért fontos ez a lelet — G0994.)*`, `*(L. lent: Miért fontos ez a lelet — Kiemelt módszertani jelentőség.)*`.
4. Belső hivatkozások a LEX-brief G4/1 szerint (a pilot „10. szakasz" hivatkozása → „9. szakasz — Források és licencek", ha tartalmilag oda mutat; ha nem dönthető el, változatlan, és a jelentésbe kerül).
5. Az alszakasz végén, egy üres sor után, szó szerint:

```
*Források és licencek ehhez az alszakaszhoz:* BDB (Brown–Driver–Briggs) — közkincs; TBESG, TBESH (STEPBible-Data, Abbott-Smith-alapú) — CC BY 4.0; Thayer's Greek-English Lexicon — közkincs; SECE — közkincs; LSJ forrás: Liddell-Scott-Jones, Perseus Digital Library (`lexica` repó), CC BY-SA 3.0.; Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, www.teknia.com/greek-dictionary
```

### N16.5 — az N16 lezárása
A `NYITOTT_FELADATOK.md` N16 blokkjának első sorában `- **N16 — Az ISTENTISZT-001 hiányzó ÚSZ-i idézőhelyei.**` → `- **N16 — Az ISTENTISZT-001 hiányzó ÚSZ-i idézőhelyei. LEZÁRVA (N16, 2026.09.21).**`. A blokk végére egy új bekezdés kerül: `  **Megoldás (N16_BRIEF.md):** a két sor a study kapcsolat-táblája alapján, \`scope=manual\` provenienciával, \`betolt.py beepit\` úton betöltve (29 → 31 sor); a Jóel 2:32 → Róm 10:14 kapcsolat a study szerinti három sorra bontva (23 → 25 kapcsolat). A lexikon-oldal ApCsel/Róm 10:13 ⚠ ELTÉRÉS-jelölései feloldva; a pilot szótári anyaga (2–4. szakasz) a 2/b. kézi alszakaszba átemelve. L. \`N16.0\`–\`N16.5\` commitok.` A `MUNKAMENET.md` nyitott felsorolásából az N16 kikerül.

## 5. Várt számok — jóváhagyva (2026.09.21)

A szimuláció a `6ad18cf` klónján futott.

| Mérés | Előtte | Utána |
|---|---|---|
| `betolt.py beepit` munkalap-ellenőrzés | — | 2 sor, 0 hiba |
| `elofordulasok.tsv` összes sor | 253 | 255 |
| ISTENTISZT-001 előfordulás / ebből lexikon-jelentéssel | 29 / 22 | 31 / 24 |
| ISTENTISZT-001 kapcsolat / csomópont | 23 / 29 | 25 / 31 |
| TSK/KH: igehely találattal / találat | 20 / 93 | 22 / 102 |
| LXX-híd (1 görög token) | változatlan | 22 ÓSZ igehely, 13 találat |
| `jeloltek.tsv` beépítve | 253 | 255 |
| `ellenoriz.py` | 6·0·3·1 | 6·0·3·1 |
| `naplo` 4 blokk / `index` / `nyitott` `--ellenoriz` az N16.2 után | — | mind ZÖLD |
| `lexikon --id ISTENTISZT-001 --ellenoriz` az N16.2 után | — | változatlan |
| ⚠ ELTÉRÉS: TUDOMANYOS / OLVASHATO | 5 / 2 | 3 / 0 |
| „Kézzel írandó" az ISTENTISZT-001-ben | 0 | 0 |

## 6. Elfogadási kritériumok

- **K1:** az N16.1 után a `git diff --stat` csak a `jeloltek.tsv`, `elofordulasok.tsv`, `kapcsolatok.tsv` fájlokat és az új munkalapot mutatja; `ellenoriz.py` 6·0·3·1; `gate.py` nem jelez új ütközést.
- **K2:** az N16.2 után csak a G3 négy kimenete változott; a számok az 5. pont szerintiek.
- **K3:** az N16.3 és N16.4 után `general.py --cel lexikon --id ISTENTISZT-001 --ir` „változatlan"-t ad, és utána a `git diff` üres (a kézi szöveg túléli az újragenerálást).
- **K4:** `diff motivumlog/lexikon_pilot/ISTENTISZT-001_OLVASHATO.md lexikon/ISTENTISZT-001_OLVASHATO.md` üres.
- **K5:** a 2/b. alszakasz a pilot 173–340. sorával a G5 kivételein, a címszint-eltoláson és a jelentett hivatkozás-igazításokon kívül soronként azonos. A három kiemelt bekezdés a fájlban pontosan egyszer szerepel (a „Miért fontos" helyen).
- **K6:** a GENERÁLT-blokkok tartalma az N16.3–N16.4 során nem változik.
- **K7:** a pilot-mappa és a `generalt_proba/` változatlan (`git diff --stat` üres rájuk).
- **K8:** a MOUNCE- és LSJ-megjelölés szó szerint szerepel a 2/b végén.
- **K9:** `general.py --cel nyitott --ellenoriz` ZÖLD az N16.5 után; a `MUNKAMENET.md` nyitott listája: N11, N13, N15.

## 7. Commitok

1. `N16_BRIEF.md v1`
2. `N16.1: ApCsel 2:21 és Róm 10:13 betöltése, Jóel 2:32 kapcsolat szétbontása (study szerint)`
3. `N16.2: naplo, index, nyitott, lexikon ISTENTISZT-001 újragenerálása`
4. `N16.3: ISTENTISZT-001 lexikon ⚠ ELTÉRÉS-jelöléseinek rendezése`
5. `N16.4: ISTENTISZT-001 lexikon 2/b — a pilot szótári anyaga`
6. `N16.5: N16 lezárása`

Push: ha a K1–K9 mind teljesül.

## Döntésnapló

| Verzió | Dátum | Döntés |
|---|---|---|
| v1 | 2026.09.21 | N16 és a pilot szótári anyagának pótlása egy menetben (Sonnet, emberi megállás nélkül, a sorok tartalma a briefben rögzítve); a kapcsolat a study szerinti három sorra bontva; a LEX-brief G5-je helyesbítve (a teljes szócikkek kézi 2/b-be, mert a SEMA 2.5 szerint a `lexikon_hivatkozasok` csak rövid kivonatot tart); G2564/G0994 nem lesz token; `generalt_proba/` és `--cel mind` kizárva; push a K1–K9 teljesülése esetén |
