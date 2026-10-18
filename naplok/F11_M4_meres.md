# F11 M4 — mérési jelentés (ISTENTISZT-001, 1. lépcső)

*FELADATOK #11 · `F11_MIGRACIO_BRIEF.md` M4 (a)–(f) · ág: `claude/f11-m3b` @ `da06f880` · alap: `89b30c2e` (a main a migráció előtt) · végrehajtó: claude-opus-5-5 (kért: opus) · 2026-10-18.*

*A felhasználó jóváhagyása (2026-10-18, a szülő session közvetítésével): „indulhat az M4 (mérés) a brief szerint, (a)–(f); minden D2-n kívüli eltérésnél ÁLLJ; az M4 végén megállás, az M5 nem indul”.*

**Eredmény: ÁLLJ.** Az (a) mérés a D2-n kívül is talált eltéréseket; a tételes lista a 7. szakaszban. A (b) zöld, a (c)–(f) megjegyzésekkel. A mérés semmit nem javított, fájlt nem írt át (a lexikon, az adat és a forrás változatlan).

Részletes osztályozás: `naplok/F11_M4_osztalyozas.tsv` (az (a) mérés minden eltérő sora: szelet, kategória, irány, sor). A mérő szkriptek a session scratchpadjában futottak (`m4_meres.py`, `m4_visszairas.py`, `m4_ketreteg.py`, `m4_e28.py`, `m3_lefedes.py`); a módszerük alább.

## 1. (a) Aranyminta ↔ migrált render

**Módszer.** Aranyminta: `generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md` (generált blokkjainak dátuma `ts=2026-10-08`). Migrált render: `PARDES_DATUM=2026-10-08 python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --kimenet <repón kívül>` a `da06f880`-on. A D2 literálok cseréje az aranyminta oldalán (pontosan a pilot-terv 5. D2 sora, `--csere`-egyenértékű, literális):

| D2 literál | találat |
|---|---|
| `rések: tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md;` → `rések: motivumok/ISTENTISZT-001.md;` (a lap fejléce) | 1 |
| `| Forrás-study | \`tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md\`<br>` → `… \`motivumok/ISTENTISZT-001.md\`<br>` (Kolofon) | 1 |

A `res_forras.tsv` `tanulmany`-útja a lapon nem jelenik meg; az aranyminta 1287. sorában álló régi út a rés prózájában van (bájtra átvitt `forras` egység), nem D2.

A különbséget a mérés **szeletenként** osztályozza: a tíz generált blokk (a `GENERÁLT-KEZDET` kulcsa szerint, a `ts=` nélkül), a hét rés (a fejléctől a következő határig) és a maradék. Rés-soroknál: `【NAPLO】` → D3; a három adatrés (2b, minosites, alatamasztas) → D4; az archív példányban álló szöveg → D5; a T14/2 és a T47 apparátus-újraírása → D3 (a leképezési tábla külön sora); a lap másik pontján meglévő sor → „áthelyezve”; minden más → ÁLLJ.

**Eredmény szeletenként** (sorok száma, `−` és `+` együtt):

| szelet | aranyminta ↔ migrált | alap-render (89b30c2e) ↔ migrált |
|---|---|---|
| blokk `tartalom` | 2 | N0 |
| blokk `jelmagyarazat` | 2 | N0 |
| blokk `elofordulasok` | 36 | N0 |
| blokk `kizart` | 96 | **12** |
| blokk `szocikkek` | 531 | N0 |
| blokk `lxx` | 44 | N0 |
| blokk `kereszthivatkozasok` | 8 | N0 |
| blokk `kapcsolatok` | 2 | N0 |
| blokk `idezes` | 24 | N0 |
| blokk `kolofon` | 37 | **2** |
| rés `kivonat` | N0 | N0 |
| rés `2b` | D3 6, D4 58 | |
| rés `miert_fontos` | **áthelyezve 16** | |
| rés `minosites` | D4 122 | |
| rés `alatamasztas` | D3 4, D4 27 | |
| rés `ertelmezes` | D3 5, D5 6, **ÁLLJ 3** | |
| rés `modszertan` | D3 6 (ebből 2 apparátus-újraírás), D5 41 | |
| egyéb | N0 | N0 |

**A blokkok kettős mérése.** Mind a tíz generált blokk eltér az aranymintától, de az aranyminta ugyanígy eltér a **migráció előtti alap** renderétől is (`89b30c2e`, azonos `PARDES_DATUM`). Ez az aranyminta elavulása a 2026-10-08-i befagyasztás óta (adat- és generátorváltozások a main-en), nem a #11 hatása. A #11 saját hatása a blokkokon az alap ↔ migrált összevetés: csak a `kizart` és a `kolofon` blokk mozdul.

## 2. (b) HAMART-001 N0

`PARDES_DATUM=2026-10-18`, mind a hat cél (`lexikon`, `naplo`, `index`, `nyitott`, `study`, `naplok`) az alapon (`89b30c2e`, külön worktree) és a fejen (`da06f880`), `diff -rq`: **egyetlen HAMART-001 kimenet sem tér el.** Minden eltérés az ISTENTISZT-001-é: a lexikonoldal, az index és a NYITOTT ISTENTISZT-001-sora (`forras_study`, az elutasítva-szám 308 → 318), a study-kimenet új helye (`motivumok/ISTENTISZT-001_1_pont_GENERALT.md` a próba-kimenetben), a generált napló új neve (`ISTENTISZT-001_kereszthivatkozas_naplo_GENERALT.md`). `eszkozok/nulladiff.sh origin/main 2026-10-18` minden M3-commit után ugyanezt adta (csak a két ISTENTISZT-001 lexikonfájl tér el). **Zöld.**

## 3. (c) Visszaírás-számláló (pilot-terv 7.4)

`git diff 89b30c2e..HEAD -- motivumok/ISTENTISZT-001.md`, 430 hozzáadott sor:

| kategória | sor |
|---|---|
| megengedett — áthelyezés (szó szerint a régi három forrásfájlban) | 264 |
| megengedett — üres sor / címsor | 131 |
| megengedett — csak-forrásbeli jelölő | 25 |
| megengedett — új kötőszöveg a leképezési tábla szerint (fejléc-【NAPLO】, T14/2, T47, T135/1–2, a két horgony) | 7 |
| **visszaírás (formális)** | **2** |
| **nem besorolt** | **1** |
| generált jelölő a forrásban | 0 |

A három sor mind **részegység-vágott forras sor**: T20/1 (a C-minta elutasításának tagmondata nélkül), T22/1 (a D-minta héber példái és a Zsid 11:16 kizárása nélkül), T14/1 (a 【NAPLO】 a záró mondata nélkül). A vágás miatt nem bájtra egyeznek a régi sorral; a T20/1 és a T22/1 8 szavas n-gramja a régi, generált lexikonlapon megvan, mert az a régi tematikus tanulmányból generálódott. Tartalmi visszaírás (adatból vagy nézetből a forrásba) **0**. A 7.4 definíciója a részegység-vágást nem nevezi meg; a számláló **formálisan 2, nem besorolt 1** (7. szakasz, Á5).

## 4. (d) Nincs egység két rétegben (pilot-terv 7.3 2.)

- (b) és (c) ág — leképezési tábla, 211 sor (`m3_lefedes.py`): 97 `forras` egység bájtra a forrásban, a 114 nem-`forras` egység egyetlen ≥ 25 karakteres sora sem maradt benne. **0 hiba.**
- (a) ág — a forrás 8 szavas n-gramjai az M3-ban keletkezett vagy változott 68 hosszú adatcellában: **7 közös**, mind a hét a D-minta jelölt-sorainak saját indoklása, a közös n-gram egyetlen szakkifejezés (`נִקְרָא...עַל (nikrá … al)`), amelyet az indoklás idéz. Prózai egyezés 0. Sablonformula/terminus-szűrés után **0**.

## 5. (e) L1–L7 + DT2 (sablon 9 8. pont)

| pont | eredmény | mérés |
|---|---|---|
| L1 szerkezeti teljesség | OK | `##` szakaszok: Kivonat, 1., 2., 3., 4., 5., 7., Proveniencia-sorok; 9 `ADAT-NÉZET` (0, 1.T, 2.S, 2/b, 6, 7.K, 7.A, 7.M, 7.Q), 1 `INAKTÍV` (1.L, indokkal), 4 kézi RÉS (kivonat, miert_fontos, ertelmezes, modszertan) |
| L2 napló-jelölés | **eltérés (öröklött)** | az `apparatus` nézetben 0 【NAPLO】; 6 forrássor visel dátumot 【NAPLO】-n kívül (az `apparatus` nézet — `general.py --cel forras --melyseg apparatus` — 146., 173., 208., 308., 332. és 359. sora: „Lexikai kiegészítés (2026.09.22)”, „Róm 10:12 (2026.09.22-én felvéve)”, „Új felismerés … *(kézi, 2026.09.22)*”, „⚠ ELTÉRÉS … 2026.09.06 … 2026.09.09”, „2026.09.08-i”, „UBS-besorolás (2026.09.22)”). Mind bájtra átvitt `forras` egység, az aranymintában is így áll. |
| L3–L4, L6–L7 | nem mérve újra | a próza bájtra átkerült, tartalma nem változott; a régi lap értékelése öröklődik |
| L5 nevesített tanítói szakasz | **nem teljesül (várt)** | a tanítói eredmény ma beemelve áll (`motivumok:308–326`); hivatkozássá alakítása az M7 feladata |
| DT2/1 rések kitöltve | OK | mind a hét rés kitöltött vagy kimondott hiányú; „Kézzel írandó” helyőrző a lapon 0 |
| DT2/2 adatból generált rész jelölve | OK | a három adatrés `<!-- GENERÁLT-RÉS: … -->`, proveniencia-sor, `*(generált)*` fejléc |

## 6. (f) E28 / E29 kézi futtatása

Ideiglenes, memóriabeli engedélyezőlista-sorral (`id=ISTENTISZT-001`, `fajl=lexikon/ISTENTISZT-001_TUDOMANYOS.md`, `cel=lexikon`, `melyseg=apparatus`); az `eszkozok/ellenorzes/e28_migralt_nezetek.tsv` nem változott.

- **E28: HIBA (1).** „a commitolt nézet eltér az újragenerálttól (PARDES_DATUM=2026-10-18). commitolt: '' | generált: '# 📖 ISTENTISZT-001 — …'” — a lap 3. sora. Ok: a commitolt lap fejléce után két üres sor áll (a main-en is így; a helyben frissítés megőrzi), az új fájlként generált lap egyet ír. Ez az egyetlen eltérés (ELLENOR_F11_M 8. szakasz).
- **E29: 0 találat** (`apparatus` mélység).

## 7. ÁLLJ — tételes lista és a döntési kérdések

| # | tétel | hol | ok | javaslat (döntés a felhasználóé) |
|---|---|---|---|---|
| Á1 | az aranyminta mind a 10 generált blokkban eltér (2–531 sor) | (a), 1. szakasz | az aranyminta 2026-10-08 óta elavult: a migráció előtti alap ugyanígy eltér tőle; nem a #11 hatása | a blokkok N0-mérése A/B a migráció előtti alap és a fej renderje között (a HAMART-001 mintájára, DT84 (9)); az aranyminta a rések mércéje marad; vagy az aranyminta blokkjainak újraalapozása az alap renderére |
| Á2 | `kizart` blokk: +10 jelölt-sor, a fejléc 81 → 91 | (a), alap ↔ migrált | az M3.1 adat-egységei (T20/2, T22/3) a `jeloltek.tsv`-ben; a D2–D6 nem nevez ilyen kategóriát | új, elfogadott kategória: „adat-egység az adatrétegben” (a leképezési tábla `adat` sora a forrás) |
| Á3 | `kolofon` blokk: a napló-cella | (a), alap ↔ migrált | az ELLENOR_F11_M 7/3 javítása (F11.M3.8) | a D2 (forrás-útvonal) bővítése ezzel a literállal |
| Á4 | rés `ertelmezes`: 3 új sor | (a) | a régi forrásréteg forras egységei a 3. szakaszban: M5/6 (⚠️ Vitatott pont, 3.V), M7/6 és M7/8 (DT-F11g (2) horgonnyal) — a leképezési tábla szerint „a lapot módosítja” | a leképezési tábla sora mint forrás elfogadva (D5 mintájára „D3/D5-szerű, táblával indokolt”), vagy archívum |
| Á5 | rés `miert_fontos`: 16 áthelyezett sor | (a) | a régi 2/b kísérő mondatai (T46, T49, T61, T62, T68) a sablon 9 5. pontja szerint a Miért fontos résbe kerültek; a szöveg bájtra azonos, a helye változott | áthelyezés mint elfogadott eltérés (a pilot-terv 5. „a próza bájtra átkerül, csak a helye változik”) |
| Á6 | visszaírás-számláló: formálisan 2, nem besorolt 1 | (c) | részegység-vágott forras sorok (T20/1, T22/1, T14/1); a 7.4 definíciója a vágást nem nevezi | a 7.4 kiegészítése: „(e) a régi forrás egy sorából a leképezési tábla részegysége szerinti kivágással álló sor” — megengedett |
| Á7 | E28 HIBA a lap 3. során | (f) | a fejléc utáni két üres sor (helyben frissítés ↔ új fájl) | az E28-listára vétel (M5) előtt a lap új fájlként generálva, vagy a `_generalt_fejlec_alkalmaz` egységesítése (generátor-tétel) |
| Á8 | L2: 6 dátumos forrássor a kiadható nézetben | (e) | bájtra átvitt forras egységek | 【NAPLO】-ba vagy archívumba tétel (tartalmi döntés), vagy elfogadás öröklöttként |
| Á9 | L5 nem teljesül | (e) | a tanítói eredmény beemelve | az M7 feladata (várt) |

A D3 („többsoros 【NAPLO】 folytatása”, 5 sor), a D4 (2b, minosites, alatamasztas) és a D5 (ertelmezes 6, modszertan 41) eltérései a pilot-terv 5. szakasza szerint elfogadott kategóriák; a soronkénti lista a `naplok/F11_M4_osztalyozas.tsv`-ben.

**Az M4 itt megáll.** Az M5 nem indult; push és PR nem történt; merge csak zöld M4 után (DT-F11f).

## 8. Újramérés a DT-F11h után (2026-10-18)

*A felhasználó döntése (DT-F11h): „Á1 A/B-mérés (alap↔migrált); Á2 új kategória; Á3 D2-bővítés; Á4–Á5 elfogadva; Á6 a 7.4 (e) pontja; Á7 a generátor javítása; Á8 a 6 dátumsor belso szintre; Á9 az M7-é. Utána újramérés, megállás.” Átvezetve: F11.M4.1 (DT-F11h), F11.M4.2 (pilot-terv 5. szakasz: A/B a blokkokra, D2 a Kolofon napló-cellájával, D7 „adat-egység az adatrétegben”, D8 „táblával indokolt áthelyezés”, L5 → M7; 7.4 (e) részegység-kivágás), F11.M4.3 (Á7: `_generalt_fejlec_alkalmaz`, CRLF-es munkapéldányon a fejléc utáni `\r` is levágva, 2 teszt, az éles lap újragenerálva). Fej: `5dfb7f6d`; alap: `89b30c2e`.*

**Mérési környezet.** A `nulladiff.sh` és az alap-render **LF-es checkouttal** fut (`GIT_CONFIG_*`: `core.autocrlf=false`), mint a CI-ben. Az Á7 javítása előtt a Windows-os, CRLF-es ideiglenes worktree-ben a javítatlan alap minden lap fejléce után egy plusz üres sort hagyott; ezt a CRLF-módú nulladiff az Á7 után minden lapon eltérésként mutatta (HAMART-001-en is), LF-módban az eltérés nincs. Az M3 alatti N0-futások CRLF-módban, az Á7 előtt futottak, ezért ott a hatás nem jelentkezett.

| pont | eredmény | mérés |
|---|---|---|
| (a) blokkok, A/B (alap-render ↔ migrált render, `PARDES_DATUM=2026-10-08`) | **zöld** | 9 blokk N0; `kizart`: 12 sor, mind D7 (a T20/2 és T22/3 10 jelölt-sora + a blokk sorszáma 81 → 91); `kolofon` N0 a bővített D2-vel. D2 csere: 3 literál, 1-1 találat mindkét oldalon. |
| (a) rések (aranyminta ↔ migrált render) | **zöld** | `kivonat` N0; `2b` D3 4, D4 60; `minosites` D4 122; `alatamasztas` D3 1, D4 30; `ertelmezes` D3 5, D5 6, D8 3 (M5/6, M7/6, M7/8); `miert_fontos` D8 16 (T46, T49, T61, T62, T68); `modszertan` D3 6 (ebből 2 apparátus-újraírás), D5 41. **ÁLLJ-sor: 0.** Soronként: `naplok/F11_M4_osztalyozas_ujra.tsv`. |
| (b) HAMART-001 N0 | **zöld** | LF-módú `nulladiff.sh origin/main 2026-10-18`: eltér csak a két ISTENTISZT-001 lexikonfájl. Mind a hat cél (`lexikon`, `naplo`, `index`, `nyitott`, `study`, `naplok`) alap ↔ fej, LF-es worktree-kben: HAMART-001-et érintő eltérés 0. |
| (c) visszaírás-számláló (7.4, (e)-vel) | **zöld** | 430 hozzáadott sor: áthelyezés 264, üres/címsor 131, jelölő 25, új kötőszöveg 7, (e) részegység-kivágás 3; **visszaírás 0, nem besorolt 0**. |
| (d) nincs egység két rétegben | **zöld** | lefedettség: 0 hiba (97 forras bent, 114 nem-forras kint); n-gram: 7 közös a 68 új adatcellával, mind a D-minta szakkifejezése (`נִקְרָא...עַל (nikrá … al)`), prózai egyezés 0. |
| (e) L1, DT2 | zöld | változatlanul (5. szakasz). |
| (e) L2 | **nyitott — Á8 pontosítást kér** | 6 dátumos forrássor a kiadható nézetben; l. lent. |
| (e) L5 | M7 (DT-F11h Á9) | várt nem-teljesülés. |
| (f) E28 / E29 | **zöld** | ideiglenes listasorral: E28 0 találat (az Á7 után), E29 0. |

**Az Á8 végrehajtása pontosítást kér.** A `SZINT-KEZDET`/`SZINT-VÉGE` pár blokkszintű (DT84 (1)), a hat dátumos sor pedig hat blokkban áll (a forrás 188–190., 215–220., 259., 367., 395–404. és 431. sora; együtt kb. 260 szó). A blokkok `belso`-ba tétele ezeket egészében levenné a kiadható lapról, köztük:
- a 367. sor megbízhatósági figyelmeztetését („⚠ ELTÉRÉS: a táblázat „15 emberi-invokációs eset” száma …”), amely a DT84 (10) (ii) szerint apparátus-szöveg;
- a 7.N 5. tartalmi nyitott kérdését (431., UBS-besorolás);
- két értelmező bekezdést (Lexikai kiegészítés, Remez-szint; Róm 10:12) és a D-minta scan-bekezdését;
- a 3.U alcímét (259.).

Két végrehajtási mód:
- **(a) csak a dátum kerül `belso` szintre:** a dátum-részletek (pl. „(2026.09.22)”, „2026.09.06-i … 2026.09.09-i”, „2026.09.08-i”) inline `【NAPLO: …】` jelölőbe kerülnek (karakterszinten vágódik ki, SEMA 3.10.3), a mondatok a lapon maradnak; a forras egységek bájtjai csak a dátum helyén változnak, a leképezési táblában rögzítve. **Javasolt.**
- **(b) a hat blokk egészében `belso`:** `SZINT-KEZDET: belso` pár a hat blokk körül; a fenti tartalom eltűnik a lapról (D3 jellegű, de a 367. sor a DT84 (10) (ii)-vel ütközik).

**Eredmény: az M4 (a)–(d), (f) zöld, az (e) L2 az Á8 pontosításáig nyitott, az L5 az M7-é.** Az M5 nem indult; push és PR nem történt; merge csak zöld M4 után (DT-F11f).
