---
feladat: 37
cim: Tanulmány-ellenőrzés: CI-szabályok és független ellenőr
kod: TANULMANY_ELLENORZES
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/tanulmany-ellenorzes
ad: a tanulmányokat CI (E20–E24, a T0 szerint) és a fuggetlen-ellenor ügynök ellenőrzi; a régi tanulmányokról két auditjelentés készül
kovetkezo: Egyeztetett eltérés: a #45 levezetett függést a felhasználó felülbírálta (2026.10.07); ⛔ a T0 után (nincs Strong-jelölt eredeti szöveg, vagy az SzPA kötelező szakasz a Tanulmány sablonban, vagy a T0 mégis alap tanulmányt talál)
olvas: [sablonok/, genezis/, ujszovetseg/, tematikus_lezart/, konkordancia/, adat/, .claude/agents/fuggetlen-ellenor.md, eszkozok/ellenorzes/, CLAUDE.md]
ir: [sablonok/1_PaRDeS_alap_sablon.md, sablonok/2_PaRDeS_bovitett_sablon.md, MUNKAMENET.md, adat/SEMA.md, ATALAKITASI_TERV.md.md, Join_tabla_folyamat_magyarazat.md, .claude/agents/fuggetlen-ellenor.md, eszkozok/ellenorzes/, .github/workflows/ellenorzes.yml, naplok/T0_felmeres.md, naplok/TANULMANY_AUDIT.md, naplok/TANULMANY_AUDIT_ugynok.md]
fugg: [30, 32]
---
# TANULMANY_ELLENORZES_BRIEF.md

*v1.1 · 2026.10.07 · a T2 elhagyva (nincs alap tanulmány, DT-F37-9); a Károli–Strong párosítás állapota frissítve · v1 · 2026.10.01 · FELADATOK #37 (új sor, chat-jóváhagyással) · függ: #2 (CI) merge-e · ág: `claude/tanulmany-ellenorzes`*

## Cél

Egy tanulmány egy menetben készül. Minden új tanulmányt két szereplő ellenőriz: a gép (CI) és a `fuggetlen-ellenor` ügynök. A felhasználó csak a két jelentést olvassa, és a ⛔ pontokon dönt. A meglévő tanulmányokat egyszer auditáljuk. A javításuk külön feladat lesz.

## Háttér (rögzített döntések)

- Alap tanulmány nincs többé. A bővített tanulmány neve mostantól „tanulmány”, a sablon neve „Tanulmány sablon”.
- Tanulmányokat nem kötegelünk: egy tanulmány egy menet.
- Az SzPA a projektből kivezetve (2026.10.01).
- A Károli–Strong párosítás (#22) részben kész: 2026.10.07-én 1–5Móz és Józsué (`adat/karoli_strong/parok_*.tsv`); a többi könyv folyamatban. A zárt licencű forrás adata nem kerülhet a repóba.
- Alap tanulmány a repóban nem létezik: a `genezis/` és az `ujszovetseg/` alatt csak bővített tanulmány van, a git-történetben sincs törölt alap tanulmány; a repón kívül sincs bevonandó (felhasználó, 2026.10.07; DT-F37-9).

## Nem tartozik ide

- A régi tanulmányok javítása (erről utófeladat-javaslat készül, lásd T6).
- Új tanulmány írása (#13).
- Annak ellenőrzése, hogy a magyar szóhoz jó Strong-szám tartozik-e (a #22-től függ).

## Lépések

### T0 — felmérés (csak olvas)

Mérd fel, és írd a `naplok/T0_felmeres.md` fájlba:
- a sablonfájlok helyét (bővített/tanulmány és alap);
- a tanulmányfájlok helyét és listáját (a 2026.10.07-i állapot szerint mind bővített; ha a T0 mégis alap tanulmányt talál, jelentsd, és állj meg ⛔);
- a CI-szabályok helyét és az utolsó E-számot;
- a `fuggetlen-ellenor` ügynök definíciójának helyét;
- a „Bővített” szó élő előfordulásait (grep, a lezárt naplók nélkül);
- a Strong-számmal jelölt eredeti szöveget a repóban (héber, illetve görög/LXX), fájlnévvel és lefedettséggel;
- a szótári réteget (TBESH, TBESG), fájlnévvel;
- van-e még SzPA-szakasz vagy SzPA-hivatkozás a Tanulmány sablonban, a `CLAUDE.md`-ben vagy a `MUNKAMENET.md`-ben (az SzPA kivezetésre került); ha van, jelentsd, de ne javítsd.
- az `ATALAKITASI_TERV.md.md` dupla kiterjesztését jelentsd, javítás nélkül, utófeladat-javaslatként.

⛔ Ha nincs Strong-jelölt eredeti szöveg: állj meg, és jelentsd. Ugyanígy állj meg, ha az SzPA kötelező szakaszként szerepel a Tanulmány sablonban, mert az E20 szakaszellenőrző szabály a szakaszlistát ebből olvassa. Más SzPA-előfordulás miatt nem kell megállni, azt csak jelentsd.

### T1 — átnevezés

A „Bővített sablon” nevet írd át „Tanulmány sablon”-ra minden élő hivatkozásban: sablonfájl, briefek, ügynökdefiníció. A lezárt naplókat és a git-történetet ne írd át. Az alap sablont ne töröld, csak jelöld elavultnak (a sorsáról a T6 utófeladat-javaslata szól; alap tanulmány nincs, DT-F37-9).

A T1 a futáskori `main`-en fut. A vele ütköző nyitott ágak (#9 `MUNKAMENET.md`, #23 `adat/SEMA.md`) a saját merge-ükkor igazodnak az átnevezéshez.

### T2 — elhagyva (DT-F37-9)

Az eredeti T2 az alap tanulmányokat vetette volna össze a bővített párjukkal. Alap tanulmány nincs (sem a repóban, sem rajta kívül), ezért a lépés és a ⛔ pontja elmarad; a `naplok/T2_alap_osszevetes.md` nem készül. A lépésszámozás a hivatkozások miatt marad (T3–T6).

### T3 — CI-szabályok (az utolsó E-szám után folytatva; itt E20-tól jelölve, a végleges számozás a T0 szerint)

A T0 minden tervezett szabályt vessen össze a meglévő E1–E19 szabályokkal. Átfedés esetén a meglévő szabály hatókörét bővítse, ne vegyen fel újat.

| Szabály | Mit ellenőriz |
|---|---|
| E20 | Megvan-e minden kötelező szakasz. A szakaszlistát a Tanulmány sablonból olvassa, nem kódba égetve. |
| E21 | Van-e kiejtés minden görög és héber szó mellett. |
| E22 | Egységes-e a versformátum (`1Móz 17:1`). |
| E23 | Nincs-e angolul hagyott „sense”. |
| E24 | A naplójellegű szöveg `【NAPLO】` blokkban van-e. A felismerés módját a T0 alapján javasold; ha bizonytalan, ez a szabály csak figyelmeztessen. |

Futási mód:
- **Kötelező (piros):** csak az új vagy módosított tanulmányfájlokra, a base ághoz képest.
- **Jelentés mód (nem bukik):** minden tanulmányfájlra. Kimenet: `naplok/TANULMANY_AUDIT.md`.

Minden szabályhoz kell egy pozitív és egy negatív teszt (fixture).

### T4 — az ügynök tanulmány-ellenőrzőlistája

Új szakasz a `fuggetlen-ellenor` definíciójában, kimenet: `naplok/ELLENOR_<tanulmány>.md`.

1. Előfordul-e a hivatkozott Strong-szám az adott versben a Strong-jelölt eredeti szövegben.
2. A tanulmány szótári alakja és kiejtése egyezik-e a szótári réteg (TBESH/TBESG) sorával.
3. Léteznek-e a kereszthivatkozott igehelyek.
4. A Sod levezethető-e a Peshat, Remez és Drash szintekből.
5. Minden ⚠️ mellett van-e megnevezett képviselő.
6. Frissült-e a motívumnapló mind a 7 szakasza, és összhangban van-e a tanulmánnyal.
7. *Függő (#22):* a magyar szóhoz jó Strong-szám tartozik-e. Amíg a #22 nincs kész, a jelentésben „kihagyva: #22” szerepel.

A jelentés ⛔-t ad, ha egy motívum átlépi a ⭐-küszöböt, vagy ha valódi ⚠️-vita merül fel.

### T5 — egyszeri ügynöki audit a régi tanulmányokra

Az 1–6. pontot futtasd végig a meglévő tanulmányokon. Kimenet: `naplok/TANULMANY_AUDIT_ugynok.md`. Javítást ne végezz.

### T6 — zárás

- Frissítsd a `FELADATOK.md` saját sorát.
- Javasolj utófeladatot a régi tanulmányok javítására a két auditjelentés alapján. Ez csak javaslat: új sor a chat jóváhagyásával kerülhet a fájlba.

## Elfogadási feltételek

- A CI zöld, és minden új szabálynak van pozitív és negatív tesztje.
- Mindkét auditjelentés elkészült (`TANULMANY_AUDIT.md`, `TANULMANY_AUDIT_ugynok.md`).
- A „Bővített sablon” név élő hivatkozásban nem fordul elő.
- A T0 felmérése megerősíti, hogy nincs alap tanulmány (vagy a ⛔ megállás megtörtént, ha mégis van).

## Nyitó prompt (Code)

<!-- KOZVETLEN_FUTTATAS -->
> Olvasd el a `TANULMANY_ELLENORZES_BRIEF.md`-t és a `CLAUDE.md`-t. Hajtsd végre a T0–T6 lépéseket sorrendben, a `claude/tanulmany-ellenorzes` ágon. A ⛔ pontokon állj meg, és jelentsd, mire vársz. A döntésszámoknál helyőrzőt használj (`DT-F37`). Az utolsó commit frissítse a `FELADATOK.md` saját sorát.
<!-- /KOZVETLEN_FUTTATAS -->

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| DT-F37-1 | Nincs alap tanulmány; a bővített neve „tanulmány” | felhasználói döntés (10.01) | két szint fenntartása |
| DT-F37-2 | Tanulmány nem kötegelhető, egy tanulmány egy menet | felhasználói döntés (10.01); a kontextus egyben marad | soros vagy párhuzamos köteg |
| DT-F37-3 | A CI csak az új vagy módosított tanulmányra kötelező, a régiekre jelentés mód | különben a régi fájlok miatt minden PR piros lenne | minden tanulmányra kötelező |
| DT-F37-4 | A magyar szó és a Strong-szám ellenőrzése függő a #22-ig | nincs párosítás *(2026.10.07: a párosítás részben kész, 1–5Móz, Józs; a szabály változatlan, a T4 7. pontjának részleges bekapcsolása külön döntés)*; a zárt forrás adata nem kerülhet a repóba | ellenőrzés a zárt forrásból (licenc miatt elvetve) |
| DT-F37-5 | A régi tanulmányok javítása külön feladat | a brief ne duzzadjon; a felhasználó dönt a javítás köréről | javítás az auditban |
| DT-F37-6 | Az E20 a szakaszlistát a sablonból olvassa | sablonváltozáskor ne kelljen kódot módosítani | beégetett lista |
| DT-F37-7 | ~~Az alap tanulmányok sorsa a T2 ⛔-pontjában dől el~~ — tárgytalan, l. DT-F37-9 | előbb látni kell, van-e bennük átvezetendő tartalom | előzetes archiválás vagy törlés |
| DT-F37-8 | Nincs duplikált CI-szabály; átfedésnél a meglévő szabály hatóköre bővül, ezért a számozás E20-tól indul, a T0 szerint | az E17–E19 már foglalt a `szabalyok.py`-ban | E17–E22 új szabályokkal |
| DT-F37-9 | A T2 elmarad: alap tanulmány nincs, sem a repóban, sem rajta kívül | felhasználói döntés (2026.10.07, chat); a repóban csak `_bovitett.md` tanulmány van (`genezis/` 20, `ujszovetseg/` 3), törölt alap tanulmány a git-történetben sincs | a T2 lefuttatása üres eredménnyel |
