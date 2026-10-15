# TERVEZO_MOD — zárónapló (#98)

*A napló szakaszonként bővül: M1 (előkészítés), M2 (tervező mód és mentés), M3 (felhasználói próba), zárás. Az M0 terve: `naplok/TERVEZO_MOD_M0.md`; a döntések: DT-F98a–f, `DONTESEK.md`.*

## M1 — előkészítés

*Modell: `claude-opus-5-5`. Ág: `claude/tervezo-mod`, alap `77022490` (F98.3). Állapot: **kész**; a megjelenés-azonosság mérése **0 eltérést** ad. A következő lépés az M2, amelyet a felhasználó „mehet”-je indít.*

A felhasználó 2026-10-14-én a chatben jóváhagyta az M0-t (a regiszter magyar nevei és tulajdonság-köre), és a DT-F98a–e mind (a) szerint dőlt el. Az M1 ezek szerint készült.

### M1.1 A token-fájl (`eszkozok/olvaso_szerver/konfig/arculat.json`)

- **Tartalom:** 10 szín (világos és sötét érték), 5 betűcsalád, **52 betűméret** (DT-F98a, szerep szerint), **18 sorköz** (DT-F98c), **35 térköz** (DT-F98b, csak a regiszterben kitettek), **6 lekerekítés**. Az értékek a mai `olvaso.css` ténylegesen érvényes deklarációi, az M0 3. szakaszának névjegyzéke szerint. A fájl 4 158 bájt, `sha256` 16 jegye `13b0c486cc801556` (ez a lapokon a `/arculat.css?v=` értéke).
- **Forma:** JSON, rendezett kulcsok, 2 szóközös behúzás, záró újsor; csak értékek, szabad szöveg nélkül (a magyar nevek az M2 regiszterébe kerülnek).
- **Ellenőrzés betöltéskor** (`arculat.py`): ismeretlen csoport, rossz token-név (csak kisbetű, szám, kötőjel), rossz alakú érték (szín: `#rgb`, `#rrggbb`, `rgb()`, `hsl()`; betűméret és térköz: `px`/`rem`/`em`; lekerekítés: `px`; sorköz: mértékegység nélküli szám; betűcsalád: betű, szám, szóköz, idézőjel, vessző, kötőjel) → indulási hiba, a hibás kulcs megnevezésével. A **tartományokat** a betöltés nem ellenőrzi: azok az M2 mentési végpontjához tartoznak (l. DT-F98f).

### M1.2 A token-blokk a szerveren (DT-F98e)

- `arculat.css_blokk()` állítja elő a régi `olvaso.css` 3–15. sorának megfelelő blokkot: `:root` minden tokennel (a színek világos értékével), `@media (prefers-color-scheme: dark) { :root:not([data-tema="light"]) { … } }` és `:root[data-tema="dark"] { … }` (a színek sötét értékével, `color-scheme: dark`). Fejléce `/* GENERÁLT: … */`.
- **Útvonal:** `GET /arculat.css` (`alkalmazas.py`): `text/css; charset=utf-8`, `ETag: "arculat-<hash>"`, 304 az egyező `If-None-Match`-re; a jelenlegi hash-sel kért változat `public, max-age=31536000, immutable`, minden más kérés `no-cache`. Minden kiadásban létezik (az arculat része, nem a tervező módé).
- **Link:** `sablonok/alap.html` a `fonts.css` után, az `olvaso.css` előtt: `<link rel="stylesheet" href="/arculat.css?v={{ arculat_hash }}">`. A CSP nem változott (nincs inline stílus).
- **Gyorsítótár és ETag:** az `arculat.hash` külön tag a lap gyorsítótár-kulcsában (így az ETag-ben is); a `kod_verzio` a `.json`-t is hasheli. Az M2 mentése után így nincs 304 a régi ETag-re, és nincs régi lap a gyorsítótárból (teszt: `teszt_arculat.py`, `test_a_hash_a_lap_kulcsaban_es_etagjeben`).
- A token-fájl a konfiguráció könyvtárából jön, ha ott van (`PARDES_KONFIG_DIR`), különben a szerver `konfig/arculat.json`-jából (`Arculat.konfigbol`).
- **Statikus export:** az `export.py` a kimenet gyökerébe írja az `arculat.css`-t, ugyanabból a függvényből (`css_blokk`); a lapok a váz szerver-abszolút hivatkozásaival linkelik.

### M1.3 A stíluslap (`statikus/olvaso.css`)

- A `:root` és a két sötét téma-blokk kikerült. A betűméret, a sorköz és a lekerekítés minden előfordulása, valamint a 35 kitett térköz `var(--…)`-hivatkozás. A stíluslapban nincs CSS-változó definíció és nincs színérték; minden `var()` létező token, és minden token használt (teszt).
- **DT-F98d — a felülírt deklarációk törlése: 42 deklaráció.** Az M0 felmérése (`holt.py`) 46-ot számolt. Az M1 elemzője (`css_elemzo.py`, a session scratch-könyvtárában) szigorúbb: egy deklaráció csak akkor holt, ha ugyanazon szelektor (a szelektorlistát egyenként nézve), ugyanabban a média-környezetben egy későbbi deklarációja **minden longhandjét** felülírja (a `font`, `padding`, `margin`, `border-radius`, `gap`, `border`, `text-decoration`, `background` rövidítéseket longhandekre bontva). A különbség a **részben** felülírt rövidítésekből adódik: például a `.jelleg { font: 500 12.5px var(--font-ui) }` betűméretét a későbbi `font-size` felülírja, de a vastagságát és a családját nem, ezért nem holt. A törölt 42:

| Sor (régi) | Szelektor | Deklaráció |
|---|---|---|
| 17 | `body` | `font: 16px/1.5 var(--font-ui)` |
| 20 | `.logo` | `font-weight: 700` |
| 31 | `h1` | `font-size: 24px` |
| 46 | `.szoveg-oszlop` | `font: 18px/1.7 var(--font-text)` (a szabály megszűnt) |
| 47 | `.jobb-oszlop` | `background: var(--panel)`, `border-radius: 8px`, `padding: 10px 12px`, `font-size: 14.5px` |
| 50 | `.versszam` | `font: 600 12px var(--font-ui)` |
| 51 | `.szo` | `text-decoration: underline dotted`, `text-underline-offset: 3px` |
| 58 | `.il-szavak` | `display: flex`, `flex-wrap: wrap`, `gap: 6px 12px` (a szabály megszűnt) |
| 59 | `.il-szo` | `display: flex` |
| 60 | `.il-szo .hu` | `font-weight: 600` (a szabály megszűnt) |
| 62 | `.il-parositatlan` | `margin-top: 4px` |
| 69 | `.blokk` | `padding-bottom: 8px` |
| 75 | `.forras` | `font-size: 12.5px` |
| 80 | `.szoveg` | `font: 14px/1.5 var(--font-ui)` |
| 83 | `.karoli-szoveg` | `font: 18px/1.6 var(--font-text)` |
| 84 | `.szocim .heb, .szocim .gor` | `font-size: 1.3em` (a szabály megszűnt) |
| 89 | `.cimkek .cimke` | `background: var(--panel)` |
| 93 | `.utmutato ol` | `font-size: 14px` |
| 95 | `.he-szo` | `min-width: 64px`, `padding: 6px 8px` |
| 99 | `.he-szo .he` | `font-size: 1.5rem` |
| 100 | `.he-szo .at` | `font-size: 13px` |
| 101 | `.he-szo .gl` | `font-size: 13px` (a szabály megszűnt) |
| 107 | `.lxx-sor` | `gap: 4px 10px`, `font-size: 1.2rem` |
| 134 | `.il-szo` | `padding: 4px 6px` |
| 135 | `.il-szo .hu` | `font: 16px var(--font-text)` (a szabály megszűnt) |
| 140 | `.il-szo .heb` | `font-size: 1.25rem` |
| 146 | `.alapjel` | `font-size: 15px` |
| 147 | `.alapjel .fcim, .forrasnev .fcim` | `letter-spacing: .04em`, `color: var(--muted)`, `margin-right: 6px` |
| 150 | `.forrasnev` | `font-size: 12.5px` |
| 153 | `.helyek` | `font-size: 12px` |
| 154 | `.jsz` | `font-size: 14px` |
| 155 | `.torzs h5` | `font-size: 14px` |

- **Két részben felülírt rövidítés** egyik tagja a nyerő érték tokenjét kapta, hogy a stíluslapban ne maradjon félrevezető, soha nem érvényesülő méret: `.blokk { margin: 0 0 16px }` → `margin: 0 0 var(--space-blokkkoz)` (18px; a későbbi `margin-bottom: 18px` eddig is felülírta), és `.alapjel .fcim, .forrasnev .fcim { font: 600 11.5px … }` → `font: 600 var(--fs-forrascim) …` (12px; a későbbi `font-size: 12px` eddig is felülírta). A számított stílus egyik esetben sem változik (M1.4).

### M1.4 A megjelenés-azonosság mérése

**Módszer.** Két szerver futott egyszerre a `pardes` WSL-disztribúcióban (Python 3.12.3, Flask 3.1.3, a `.venv` a `~/pardes/eszkozok/olvaso_szerver/`-ből, csak olvasva), ugyanazon az adatbázison (`/mnt/c/…/Bible-Study/pardes.db`, belső kiadás): a **csere előtti** a `77022490` kódjával (`git archive` a session scratch-könyvtárába, 8801-es port), a **csere utáni** a munkafából (8802-es port). A mérés a Claude desktop app beépített böngészőjében futott, emulált 1280×900-as viewporton, és három lapon 375×812-esen is (mobil, a ≤640px-es média-lekérdezés is). A mérőszkript (`meres.js`, `sha256` 16 jegye a szkript szövegére `a27d0b54a9c3b578`, mindkét szerveren azonos) a `document.fonts.ready` után a `<html>`, a `<body>` és **minden** `body`-beli elem 57 számított tulajdonságát (betűcsalád, -méret, -vastagság, -stílus, sorköz, betűköz, számalak, OpenType-jellemzők, szín, háttérszín, átlátszóság, megjelenítés és flex/grid-igazítás, sor- és oszlopköz, a négy párna, a négy margó, a négy keret vastagsága, stílusa, színe, a négy sarok lekerekítése, aláhúzás vonala, stílusa, színe, vastagsága és eltolása, függőleges igazítás, legkisebb és legnagyobb szélesség, legnagyobb magasság, szóköz-kezelés, nagybetűsítés, színséma, körvonal) **és befoglaló téglalapját** (x, y, szélesség, magasság, két tizedesre) rögzítette, három témában (`data-tema="light"`, `data-tema="dark"`, attribútum nélkül = rendszer; a panel rendszer-beállítása sötét volt), és lapállapotonként SHA-256 kivonatot adott.

**Lapok** (26 lapállapot × 3 téma; 35 813 elem): a két pilot-szakasz (1Móz 1:1–2:3: `/1Moz/1`, `/1Moz/2`; Zsolt 22: `/Zsolt/22`) és egy ÚSZ-fejezet (`/Jan/1`), mindhárom nézetben (Olvasópult, Interlineáris, Munkaasztal); a jobb oldali panel szó- és vers-füllel (`/1Moz/1/1?szo=H0430&ful=szo`, `/1Moz/1/2?ful=vers`, `/Jan/1/1?szo=G3056&ful=szo`, `/Zsolt/22/2?szo=H0410&ful=szo` Interlineárisban); szó-lapok (`/szo/H0430`, `/szo/G3056`, `/szo/H7307`, `/szo/H6440` — BDB-apparátus, görög szó); kezdőlap, könyvlap, hibalap; mobilon `/1Moz/1`, `/Jan/1/1?szo=G3056&ful=szo` (Interlineáris), `/szo/H0430`.

**Eredmény: 0 eltérés.** Mind a 26 lapállapot mindhárom témában bitre azonos kivonatot adott a csere előtt és után.

| Lap | Szélesség | Elem | light | dark | rendszer | Előtte = utána |
|---|---|---|---|---|---|---|
| `/1Moz/1?nezet=olvaso` | 1280 | 753 | `f8442e418704de30` | `0e9ac3a270075c41` | `0e9ac3a270075c41` | igen |
| `/` | 1280 | 1622 | `63da6b51052a0069` | `d873ef7cd1809cd7` | `d873ef7cd1809cd7` | igen |
| `/1Moz` | 1280 | 78 | `95ef34d9cda9eacb` | `04a2cba25289fb82` | `04a2cba25289fb82` | igen |
| `/1Moz/1?nezet=interlinearis` | 1280 | 5568 | `697fd9178142444a` | `74a0879307067a83` | `74a0879307067a83` | igen |
| `/1Moz/1?nezet=munkaasztal` | 1280 | 812 | `edfc74a4a2e7ef4c` | `b2145f3f07096f70` | `b2145f3f07096f70` | igen |
| `/1Moz/2?nezet=olvaso` | 1280 | 627 | `8c5b8d3e451a75a2` | `782f2b560e24d3ba` | `782f2b560e24d3ba` | igen |
| `/1Moz/2?nezet=interlinearis` | 1280 | 4415 | `017c14a718b328d5` | `1aa41bbfbdd35bdd` | `1aa41bbfbdd35bdd` | igen |
| `/1Moz/2?nezet=munkaasztal` | 1280 | 674 | `90ae2d08a68a1c29` | `fa5741c616dab72f` | `fa5741c616dab72f` | igen |
| `/Zsolt/22?nezet=olvaso` | 1280 | 549 | `a09564aa8e0642ea` | `2fa3259a27c8c24e` | `2fa3259a27c8c24e` | igen |
| `/Zsolt/22?nezet=interlinearis` | 1280 | 3617 | `7451dcccfaabda9d` | `2f7810d7e6f3a58d` | `2f7810d7e6f3a58d` | igen |
| `/Zsolt/22?nezet=munkaasztal` | 1280 | 610 | `d7eb7c07b97d2b02` | `38ffc406199a0293` | `38ffc406199a0293` | igen |
| `/Jan/1?nezet=olvaso` | 1280 | 179 | `0d7999934886e93c` | `5875cc7557b8bb3d` | `5875cc7557b8bb3d` | igen |
| `/Jan/1?nezet=interlinearis` | 1280 | 275 | `afdc9d43a6d27f4a` | `faaa275ed9681ac4` | `faaa275ed9681ac4` | igen |
| `/Jan/1?nezet=munkaasztal` | 1280 | 278 | `f9c532fff5cb2824` | `5e2e5a97334ff250` | `5e2e5a97334ff250` | igen |
| `/1Moz/1/1?szo=H0430&ful=szo&nezet=munkaasztal` | 1280 | 2349 | `4682b0547e1a1dda` | `37c03fe6dba65b6b` | `37c03fe6dba65b6b` | igen |
| `/1Moz/1/2?ful=vers&nezet=munkaasztal` | 1280 | 2634 | `c8002724c5dd6cd2` | `372f392ed7131508` | `372f392ed7131508` | igen |
| `/Jan/1/1?szo=G3056&ful=szo&nezet=olvaso` | 1280 | 1072 | `e62638c0a805bb58` | `bfe966e11af4b169` | `bfe966e11af4b169` | igen |
| `/Zsolt/22/2?szo=H0410&ful=szo&nezet=interlinearis` | 1280 | 5547 | `5b56852ab4f4656f` | `493e281806901bcf` | `493e281806901bcf` | igen |
| `/szo/H0430` | 1280 | 439 | `020e23726ea029c3` | `79682e215fd40360` | `79682e215fd40360` | igen |
| `/szo/G3056` | 1280 | 405 | `1f0270feb3eb08b6` | `5750e768fe53cdd7` | `5750e768fe53cdd7` | igen |
| `/szo/H7307` | 1280 | 495 | `49f7ebbf1629bffe` | `7406fce1ef4b5392` | `7406fce1ef4b5392` | igen |
| `/szo/H6440` | 1280 | 425 | `02a230a931b43d54` | `8032f3874fb9a046` | `8032f3874fb9a046` | igen |
| `/nincs-ilyen-konyv` | 1280 | 28 | `b3c0f830c16da6f6` | `4f240fe353dce026` | `4f240fe353dce026` | igen |
| `/1Moz/1?nezet=olvaso` | 375 | 753 | `861fb5fce379282e` | `2eca12b121d7191f` | `2eca12b121d7191f` | igen |
| `/Jan/1/1?szo=G3056&ful=szo&nezet=interlinearis` | 375 | 1170 | `fec6b0fe5d31cf31` | `20107f4a0a366e49` | `20107f4a0a366e49` | igen |
| `/szo/H0430` | 493 | 439 | `637d95a31d30a993` | `5deb46939a9cb76c` | `5deb46939a9cb76c` | igen |

Összesítés (gépi): 26 lapállapot, 35813 elem, eltérés: **0**.

**Determinizmus és érzékenység.** Az `/1Moz/1` kétszeri mérése azonos kivonatot adott. Negatív kontroll a csere utáni szerveren: a `--fs-versszam` 0.61em-re állítva (csak a böngészőben, CSSOM-mal) a kivonat eltér (`af72e9fc5a3e955c`), 0.6em-re visszaállítva az eredeti (`f8442e418704de30`); a `--space-oldal` 17px-re állítva szintén eltér (`dd19e191226f71b8`). A mérés tehát egy 0.01em-es betűméret- és egy 1px-es térköz-változást is észlel. Ez egyúttal az M2 előnézetének alapfeltevését is igazolja: a `:root`-on CSSOM-mal állított token az egész lapon azonnal hat, a CSP lazítása nélkül.

**Amit a böngészős mérés nem fed le, és ami fedi.** A `:hover`, a `:focus-visible` és a `::selection` állapot nem idézhető elő a mérőszkriptből. Ezeket a **statikus ekvivalencia-ellenőrzés** (`css_ekvivalencia.py`, a session scratch-könyvtárában) fedi: a régi stíluslap a 42 felülírt deklaráció és a `:root`-blokkok nélkül, illetve az új stíluslap a tokenek visszahelyettesítésével **szabályról szabályra egyezik** (179 szabály); az egyetlen két eltérés az M1.3 két részben felülírt rövidítése. A generált token-blokk változói és értékei a régi `:root`-éval és a két sötét blokkéval egyeznek (15, 11, 11 változó, értékeltérés nincs), 111 új méret-tokennel kiegészülve (52 + 18 + 35 + 6).

*Proveniencia:* `scope=eszkozok/olvaso_szerver/ (olvaso.css előtte 16 156 B sha256 dd8f415d23cd295e @77022490, utána 16 952 B sha256 2f88b7c53315ac89 @d2019dc5; konfig/arculat.json 4 158 B sha256 13b0c486cc801556), pardes.db a munkafa gyökerében, belső kiadás, 26 lapállapot × 3 téma, 35 813 elem | forras=meres.js (sha256 a27d0b54a9c3b578, 57 számított tulajdonság + befoglaló téglalap, SHA-256 lapállapotonként) a Claude desktop beépített böngészőjében, két egyidejű szerver (8801: git archive 77022490, 8802: munkafa) a pardes WSL-ben (Python 3.12.3, Flask 3.1.3); css_ekvivalencia.py, css_elemzo.py | ts=2026-10-14`

### M1.5 A literálként maradt térközök és méretek (DT-F98b)

A DT-F98b szerint csak a regiszterben kitett 35 térköz token; a stíluslap többi hosszértéke literál marad. Az alábbi lista gépi (`literalok_md.py`, a session scratch-könyvtárában), a mai `olvaso.css` minden olyan deklarációja, amelynek az értékében `var()`-on kívül hosszérték áll; a sorszám az új stíluslapé.

| Kód | Indok | Deklaráció |
|---|---|---|
| V | vonalvastagság (1–3px); a vonal színe token (`rule`, `accent`), a vastagság nem arculati méret | 25 |
| M | címsor-, bekezdés- és blokk-margó, lista-behúzás; a regiszter nem teszi ki (DT-F98b) | 41 |
| G | belső sor- és oszlopköz egy regiszterben ki nem tett tárolóban (1–12px) | 13 |
| P | belső térköz olyan elemen, amelynek a regiszter nem ad térköz-tulajdonságot (szintváltó, fül, témaváltó, jel-címke, állapot, helyszám, gyorsugró mező, táblázat-cella) | 16 |
| E | elrendezési méret (szélesség, legkisebb szélesség, magasság, oszlop, ragadós eltolás, `ch`/`vw`/`vh`); elrendezés-szerkesztés nincs a hatókörben | 14 |
| T | tipográfiai finomhangolás (betűköz em-ben, aláhúzás-eltolás és -vastagság, fókuszkeret-eltolás) | 11 |

| Sor | Szelektor | Tulajdonság | Érték | Indok |
|---|---|---|---|---|
| 8 | `.fejlec` | `border-bottom` | `1px solid var(--rule)` | V |
| 10 | `.ugras input` | `width` | `240px` | E |
| 10 | `.ugras input` | `max-width` | `60vw` | E |
| 10 | `.ugras input` | `padding` | `5px 8px` | P |
| 12 | `.nezetvalto a` | `border` | `1px solid var(--rule)` | V |
| 15 | `.szintvalto a` | `padding` | `3px 8px` | P |
| 15 | `.szintvalto a` | `border` | `1px solid var(--rule)` | V |
| 19 | `.labjegyzet` | `border-top` | `1px solid var(--rule)` | V |
| 20 | `h1` | `margin` | `6px 0 10px` | M |
| 22 | `h3` | `margin` | `0 0 6px` | M |
| 23 | `h4` | `margin` | `10px 0 4px` | M |
| 24 | `.fejezetek a, .konyvek summary` | `margin-right` | `4px` | M |
| 25 | `.fejezetek a` | `min-width` | `2em` | E |
| 26 | `.valaszto` | `margin` | `8px 0 16px` | M |
| 28 | `.konyvek` | `columns` | `3 280px` | E |
| 29 | `.konyv` | `margin` | `2px 0` | M |
| 33 | `.munkaasztal` | `grid-template-columns` | `180px minmax(0, 1fr) minmax(0, 1.2fr)` | E |
| 35 | `.jobb-oszlop` | `top` | `8px` | E |
| 35 | `.jobb-oszlop` | `max-height` | `calc(100vh - 16px)` | E |
| 35 | `.jobb-oszlop` | `border` | `1px solid var(--rule)` | V |
| 36 | `.vers` | `margin` | `0 0 6px` | M |
| 38 | `.versszam` | `margin-right` | `3px` | M |
| 42 | `.verslista` | `max-height` | `calc(100vh - 80px)` | E |
| 43 | `.verslista a` | `padding` | `2px 4px` | P |
| 43 | `.verslista a` | `border-bottom` | `1px solid var(--rule)` | V |
| 45 | `.il-vers` | `margin` | `0 0 14px` | M |
| 45 | `.il-vers` | `padding` | `4px` | P |
| 51 | `.fulek` | `margin-bottom` | `8px` | M |
| 52 | `.ful` | `padding` | `3px 10px` | P |
| 52 | `.ful` | `border` | `1px solid var(--rule)` | V |
| 55 | `.blokk` | `border-bottom` | `1px solid var(--rule)` | V |
| 56 | `.blokk h3` | `gap` | `6px` | G |
| 57 | `.jelleg` | `border` | `1px solid` | V |
| 61 | `.forras` | `margin` | `6px 0 0` | M |
| 64 | `table.adat th, table.adat td` | `padding` | `2px 8px 2px 0` | P |
| 64 | `table.adat th, table.adat td` | `border-bottom` | `1px solid var(--rule)` | V |
| 67 | `.gordul` | `max-height` | `340px` | E |
| 68 | `.lista` | `margin` | `4px 0` | M |
| 68 | `.lista` | `padding-left` | `18px` | M |
| 70 | `.szoveg-jegy` | `margin` | `0 0 12px` | M |
| 70 | `.szoveg-jegy` | `padding` | `6px 8px` | P |
| 70 | `.szoveg-jegy` | `border` | `1px solid var(--rule)` | V |
| 71 | `.szoveg-jegy p` | `margin` | `0 0 4px` | M |
| 73 | `.cimkek` | `margin` | `0 0 8px` | M |
| 74 | `.cimkek .cimke` | `border` | `1px solid var(--rule)` | V |
| 76 | `.utmutato` | `border` | `1px solid var(--rule)` | V |
| 76 | `.utmutato` | `margin` | `0 0 12px` | M |
| 78 | `.utmutato ol` | `margin` | `8px 0 2px` | M |
| 78 | `.utmutato ol` | `padding-left` | `1.2rem` | M |
| 78 | `.utmutato ol` | `gap` | `6px` | G |
| 78 | `.utmutato ol` | `max-width` | `80ch` | E |
| 79 | `.heber-sor` | `margin` | `6px 0` | M |
| 80 | `.he-szo` | `gap` | `1px` | G |
| 80 | `.he-szo` | `border` | `1px solid var(--rule)` | V |
| 82 | `.he-fo` | `gap` | `1px` | G |
| 87 | `.he-szo .mf` | `max-width` | `11rem` | E |
| 88 | `.he-szo .lx` | `border-top` | `1px dotted var(--rule)` | V |
| 88 | `.he-szo .lx` | `padding-top` | `2px` | P |
| 88 | `.he-szo .lx` | `margin-top` | `2px` | M |
| 89 | `.he-szo .lx.kat` | `text-underline-offset` | `3px` | T |
| 91 | `.lxx-sor` | `margin` | `6px 0` | M |
| 92 | `.lxx-sor > a, .lxx-sor > span` | `border` | `1px solid transparent` | V |
| 94 | `.lxx-sor .gk .gr` | `text-underline-offset` | `4px` | T |
| 97 | `.angol-sor` | `gap` | `4px 8px` | G |
| 97 | `.angol-sor` | `margin` | `6px 0` | M |
| 98 | `.ang-csempe` | `border` | `1px solid var(--rule)` | V |
| 101 | `.sorok` | `gap` | `2px` | G |
| 102 | `.sor` | `gap` | `4px 12px` | G |
| 104 | `.fejezet-nave` | `margin-top` | `8px` | M |
| 105 | `.ubs` | `margin` | `4px 0` | M |
| 105 | `.ubs` | `gap` | `2px` | G |
| 110 | `.kapcs` | `gap` | `6px` | G |
| 110 | `.kapcs` | `margin` | `0 0 8px` | M |
| 112 | `.tema` | `gap` | `2px` | G |
| 113 | `.tema button` | `padding` | `3px 8px` | P |
| 113 | `.tema button` | `border` | `1px solid var(--rule)` | V |
| 118 | `.il-szo` | `gap` | `3px` | G |
| 118 | `.il-szo` | `border` | `1px solid var(--rule)` | V |
| 118 | `.il-szo` | `min-width` | `56px` | E |
| 119 | `.il-szo .er` | `border-top` | `1px dotted var(--rule)` | V |
| 119 | `.il-szo .er` | `padding-top` | `2px` | P |
| 121 | `.il-szo .er-fo` | `gap` | `1px` | G |
| 128 | `.il-parositatlan` | `margin-top` | `6px` | M |
| 129 | `.alapjel` | `margin` | `0 0 8px` | M |
| 131 | `.app` | `margin` | `0 0 10px` | M |
| 132 | `.app h4` | `margin` | `8px 0 2px` | M |
| 133 | `.forrasnev` | `margin` | `0 0 4px` | M |
| 134 | `.cimszo` | `gap` | `4px 12px` | G |
| 136 | `.helyek` | `margin-left` | `6px` | M |
| 137 | `.jsz` | `margin` | `2px 0` | M |
| 138 | `.torzs h5` | `margin` | `8px 0 2px` | M |
| 139 | `ol.jel` | `margin` | `4px 0` | M |
| 139 | `ol.jel` | `padding-left` | `1.3rem` | M |
| 140 | `ol.al` | `margin` | `4px 0` | M |
| 140 | `ol.al` | `padding-left` | `1.2rem` | M |
| 141 | `.jel-cimke` | `padding` | `1px 6px` | P |
| 141 | `.jel-cimke` | `margin` | `1px` | M |
| 141 | `.jel-cimke` | `border` | `1px solid var(--rule)` | V |
| 143 | `.allapot` | `padding` | `1px 8px` | P |
| 143 | `.allapot` | `margin` | `0 0 4px` | M |
| 144 | `.allapot.folyamat` | `border` | `1px solid var(--rule)` | V |
| 148 | `a:focus-visible, button:focus-visible, input:focus-visible` | `outline` | `2px solid var(--accent)` | V |
| 148 | `a:focus-visible, button:focus-visible, input:focus-visible` | `outline-offset` | `2px` | T |
| 151 | `.szoveg-oszlop` | `max-width` | `60ch` | E |
| 153 | `.versszam` | `letter-spacing` | `.02em` | T |
| 153 | `.versszam` | `padding` | `0 3px 0 4px` | P |
| 154 | `.szo` | `text-decoration-thickness` | `1px` | T |
| 154 | `.szo` | `text-underline-offset` | `6px` | T |
| 157 | `.jobb-oszlop` | `padding` | `var(--space-panel-fugg) clamp(18px, 2vw, 30px)` | P |
| 160 | `.blokk h3` | `letter-spacing` | `-.005em` | T |
| 162 | `.forrasnev .fcim, .alapjel .fcim` | `letter-spacing` | `.08em` | T |
| 162 | `.forrasnev .fcim, .alapjel .fcim` | `margin-right` | `8px` | M |
| 168 | `.app h4` | `letter-spacing` | `.09em` | T |
| 170 | `.jsz, .szoveg` | `max-width` | `76ch` | E |
| 171 | `.helyek` | `border` | `1px solid var(--rule)` | V |
| 171 | `.helyek` | `padding` | `1px 7px` | P |
| 176 | `.lxx-sor .gk .gr` | `text-decoration-thickness` | `1.5px` | T |
| 180 | `.ubs` | `border-left` | `3px solid var(--accent)` | V |
| 180 | `.ubs` | `padding` | `4px 0 4px 10px` | P |
| 182 | `.cimkek .cimke` | `letter-spacing` | `.02em` | T |

Összesen: 120 deklaráció.

### M1.6 Tesztek

A szerver tesztjei a `pardes` WSL-disztribúcióban futottak (Python 3.12.3, Flask 3.1.3), az **M1 állapotának tiszta pillanatképén** (`git archive 223efd45 eszkozok adat` a session scratch-könyvtárába, a `konkordancia/` symlinkkel), hogy a pilot- és a D2-tesztek is lefussanak, és a munkafa közbeni változásai (F98.9) ne keveredjenek bele.

| Tesztfájl | Eredmény | Kihagyva | Adatbázis |
|---|---|---|---|
| `teszt_arculat.py` (új, #98 M1) | 22 OK | 0 | `/mnt/c/…/Bible-Study/pardes.db` |
| `teszt_pilot_aranymintaval.py` | 22 OK | 0 | `/mnt/c/…/Bible-Study/pardes.db` |
| `teszt_szintek.py` | 13 OK | 0 | `/mnt/c/…/Bible-Study/pardes.db` |
| `teszt_olvaso_szerver.py` (a D2-vel együtt) | 68 OK | 0 | `~/pardes/pardes.db` (ext4) |

A `teszt_olvaso_szerver.py` első futása a `/mnt/c`-n lévő adatbázissal a D2-tesztben (`test_1moz_1_25`) több mint 30 percig nem jutott tovább: a 9P-fájlrendszeren a véletlen elérésű olvasás lassú, és egy másik, nem az M1-hez tartozó tesztfolyamat is ugyanazt a fájlt olvasta. Ezért a WSL ext4-en lévő másolattal futott újra; a két fájl ugyanaz az építés (a `meta` tábla 107 sora azonos, a kivonata `2cbcbe43106a06d1`, `epites_ts` 2026-10-14T09:35:00Z). Így 140 s alatt lefutott.

**Az ág végállapotán** (84f211ed, az F98.9-cel; a munkafában csak a napló, a brief fejléce, a `DONTESEK.md` és a stage-elt fejkomment): `teszt_arculat.py` 22 OK (az F98.9 54/19-es tokenszámaival), `teszt_pilot_aranymintaval.py` 22 OK, 0 kihagyás.

Az `eszkozok/feladatok.py ellenoriz`: 118 brief, 0 hiba, 0 figyelmeztetés.

*Proveniencia:* `scope=eszkozok/olvaso_szerver/teszt_*.py @223efd45 (M1) és @84f211ed (végállapot: teszt_arculat, teszt_pilot_aranymintaval) | forras=unittest, pardes WSL .venv (Python 3.12.3, Flask 3.1.3) | ts=2026-10-14`

### M1.7 Megfigyelések és nyitott tételek az M2-höz

1. **DT-F98f (🟡, `DONTESEK.md`): a térköz tartománya.** Az M0 2.2 a mentés térköz-tartományát javaslatként 0–64px-re tette, a `terkoz.he-csempe-min` mai értéke viszont 72px. A mentési végpont (M2) értékszűréséhez döntés kell; javaslat: (a) 0–128px (rem/em 0–8). A többi mai érték az M0 2.2 tartományán belül van.
2. **A regiszter és a tokenek.** Az M0 regiszter-tervezetének (1.1) mind a 104 méret- és 10 színhivatkozása létező token. Hét méret-token nincs egyetlen regiszter-elemen sem: `fs-alcim` (`h3`), `fs-kiscim` (`h4`), `fs-csempe-megj` (`.he-szo .mf`, `.he-szo .lx.ures`), `fs-il-eredeti-sor` (`.il-szo .er`, `.il-parositatlan`), `lh-jelleg`, `lh-lxx-csempe`, `space-oszlopkoz` (`.oszlopok`). Ezek az M2-ben a tartalékon (regisztrálatlan elem) át állíthatók; ha a felhasználó magyar nevet akar melléjük, a regiszter bővíthető (a jóváhagyott regiszter M1-ben nem változott).
3. **A naplóhely.** A brief `ir` mezője a `naplok/TERVEZO_MOD_M0.md`-t és ezt a zárónaplót engedi írni, ezért az M1 naplója ennek az M1 szakasza (a DT-F98b „az M1 naplójában” megfogalmazása ezt jelenti). Az F98.7 commit üzenete még `naplok/TERVEZO_MOD_M1.md`-t nevez meg; a stíluslap fejkommentje már ide mutat (F98.10).
4. **A zárónapló szakaszai.** A tervező mód elkészülte után, az M2-ben a regiszter (`elemek.toml`) és a regiszter-őr, a mentési végpont tesztjei és a szinkron-szkript kerülnek ide; az M3-ban a felhasználó észrevételei.

### M1 utáni változás (F98.9, a felhasználó commitja, 84f211ed)

Az M1 után az ágra került a 84f211ed (F98.9: BDB-jelentésszerkezet, a pilot `ol.jel`/`ol.al` szabályai az `olvaso.css`-ben). A fenti M1-számok az M1 állapotára (223efd45) igazak; az F98.9 óta:

- **Új tokenek (3):** `betumeret.jelentes-jel` (13px), `betumeret.jelentes-osszegzo` (15.5px), `sorkoz.jelentes-osszegzo` (1.5). A token-fájlban így **54 betűméret** és **19 sorköz** van (a térköz és a lekerekítés változatlan: 35, 6); az `arculat.json` hash-e `b677aeb7f42ecb27` (a lapokon `/arculat.css?v=b677aeb7f42ecb27`). A `teszt_arculat.py` tokenszámait az F98.9 frissítette (54/19).
- **Literálok:** az M1.5 listájának `ol.jel` és `ol.al` sorai (139–140: `margin: 4px 0`, `padding-left: 1.3rem` / `1.2rem`) a régi szabályokat írják le; az F98.9 ezeket a pilot jelentéslista-szabályaira cserélte (`list-style: none`, `content: attr(data-jel)`, `gap: 12px` / `6px`, `padding-left: 2.3rem` / `1.8rem` stb.). Ezek új literál-térközök, ugyanabban a kategóriában (M, G, P), mint az M1.5 többi lista-behúzása és belső sorköze; a betűméretük már token.
- **Szándékos megjelenés-változás:** a `/szo/H6440` szó-lap jelentéslistája az F98.9 óta másképp jelenik meg (a bontott BDB-szócikk alpontjai a., b. … jelölőt kapnak, a kinyitott jelentés összegzése rejtve). Mérve az M1 mérőszkriptjével (1280×900, a 8802-es szerver újraindítva az F98.9 állapotán): `/szo/H6440` light `a035c8efa529ead6`, dark/rendszer `2de0eafa069659de` (az M1-ben `02a230a931b43d54` / `8032f3874fb9a046`), ugyanannyi elemmel (425); az `/1Moz/1` (Olvasópult) és a `/szo/G3056` kivonata változatlan (`f8442e418704de30`, `1f0270feb3eb08b6`). Ez a változás nem az M1 megjelenés-azonosságának sérülése, hanem az F98.9 javítása.

### M1 utáni változás (F98.11–F98.13, 1af2422b, 788326bd, ec98a5b2)

Az F98.9 után három további commit került az ágra a BDB-jelentésszerkezetről (F98.11: vázlat, állandó jelentéscím, „hivatkozás” felirat, jelmagyarázat; F98.12: a vezető héber a magyar mögé, héber futamok `lang="he"`-vel; F98.13: a kölcsönzött cím jelölése). Az arculatot érintő részük:

- **Token-átnevezés (F98.11):** `betumeret.jelentes-osszegzo` → `betumeret.jelentes-cim` (15.5px) és `sorkoz.jelentes-osszegzo` → `sorkoz.jelentes-cim` (1.5); a CSS-ben `--fs-jelentes-osszegzo` / `--lh-jelentes-osszegzo` → `--fs-jelentes-cim` / `--lh-jelentes-cim`. A tokenszám nem változott (**54 betűméret, 19 sorköz**, 35 térköz, 6 lekerekítés). A `jelentes-osszegzo` név a repóban már csak a fenti F98.9-szakaszban és a `teszt_arculat.py` két megjegyzésében (62–63. sor: „összegzése”, „jelentés-összegzés”) áll; a tesztek számai helyesek.
- **Az `arculat.json` hash-e:** `ed1326eb32081fbf` (a lapokon `/arculat.css?v=ed1326eb32081fbf`); a fájl 4 243 bájt. Számítva a szerver saját függvényével (`arculat.tartalom_hash`: a CRLF→LF után sha256, első 16 jegy); ugyanez a 84f211ed állapotára a fent rögzített `b677aeb7f42ecb27`-et adja, tehát a módszer azonos.
- **Új osztályok a stíluslapban (`olvaso.css` 149–170) és a `blokkok.py`-ban:** `jel-vazlat` (a vázlat `nav`-ja), `vz-torzs`, `vz-fo`, `vz-jel`, `vz-al` (a vázlat sorai), `jcim` (a részletes lista állandó jelentéscíme, a megszűnt `.jt` helyett; a `ol.jel details[open] > summary .jt { display: none }` szabály törölve), `kolcsonzott` (F98.13), `jelmagyarazat` (`dl`, a `konfig/bdb_jelek.tsv`-ből), a `.jsz abbr[title]` szabály (a BDB-rövidítések), a `.jcim .he, .jel-vazlat .he` szabály (F98.12) és a `.helyek { white-space: nowrap }` (F98.12). Minden új szabály méret- és színértéke létező token (`fs-jelentes-jel`, `fs-jelentes-cim`, `lh-jelentes-cim`, `fs-sor`, `lh-forrassor`, `fs-apparatus-alcim`, `space-utmutato-*`, `radius-panel`, `radius-kiemeles`; `panel`, `rule`, `accent`, `accent-soft`, `muted`); a literálok (`margin: 4px 0 14px`, `gap: 6px`, `gap: 2px 12px`, `min-width: 1.6rem`, `padding-left: 1.6rem`, `margin: 6px 0 2px`, `scroll-margin-top: 8px`, `text-underline-offset: 3px`) az M1.5 M, G, P kategóriájába tartoznak (lista-behúzás, belső sorköz, elem-közi margó).
- **A regiszter:** az új elemek magyar névvel és állítható tulajdonsággal az M0 1.1 „M. BDB-jelentésszerkezet” részében (74–83. sor, F98.14), a felhasználó jóváhagyására várva; a `.jcim .he` / `.jel-vazlat .he` az 1.2 kizárt listájába került (állítható tulajdonsága nincs).
- **Megjelenés:** a szó-lapok BDB-blokkja szándékosan változott (vázlat, jelentéscím, jelmagyarázat); az M1 megjelenés-azonossági mérését ezek a commitok nem érintik, mert az a 223efd45 állapotára vonatkozik. Új mérés ezekről a lapokról nem készült.

*Proveniencia:* `scope=git diff 84f211ed..ec98a5b2 -- eszkozok/olvaso_szerver/{konfig/arculat.json,statikus/olvaso.css,blokkok.py}; arculat.tartalom_hash(konfig/arculat.json @ec98a5b2 és @84f211ed) | forras=git, eszkozok/olvaso_szerver/arculat.py | ts=2026-10-15`

## M2 — tervező mód és mentés

*Modell: `claude-opus-5-5`. Ág: `claude/tervezo-mod`, alap `fa344619` (F98.14); commitok: `019e1c30` (F98.15) … `03acfcb0` (F98.20). Állapot: **kész, ⛔ M3 (a felhasználó kipróbálja)**.*

A felhasználó 2026-10-15-én a chatben jóváhagyta a regiszter 74–83. sorának magyar neveit (a 83. `jelentes-jelolo` sorral együtt); a `.jcim .he` / `.jel-vazlat .he` nem kap sort. A DT-F98a–f mind eldőlt (DT-F98f: (a)). Kérése volt még, hogy a `jt` (az F98.11 óta nem létező osztály) a végleges kizárt listára ne kerüljön, és az M0 1.2-ből is kikerüljön.

### M2.1 Az elem-regiszter (`konfig/elemek.toml`, F98.15)

- **83 `[[elem]]`** a jóváhagyott M0 1.1 szerint (A–L: 1–73, M: 74–83), elemenként `id`, `nev` (magyar név), `csoport`, `szelektor`, `tulajdonsag` (magyar név → token). A magyar nevek a jóváhagyott táblázat szövege. Ahol a táblázat egy tulajdonsághoz két tokent adott (pl. „Belső térköz → `space-gomb-fugg`, `space-gomb-vizsz`”), a regiszterben két tulajdonság áll zárójeles megkülönböztetéssel („Belső térköz (függőleges)”, „(vízszintes)”; a 16. sornál „(sorok)”, „(oszlopok)”, az 57. sornál „Sorköz (héber)”, „(görög)”, a 83. sornál „„összecsuk” felirat betűmérete” és „… színe”). Ez a forma a panelen egy csúszkát ad tokenenként; a név és a tulajdonságkör nem változott.
- **Ellenőrzés induláskor** (`tervezo.Regiszter`, minden kiadásban): ismeretlen kulcs, ismétlődő `id`, üres név vagy szelektor, a token-fájlban nem létező token, betűcsalád-token (`font-*`, szabad szöveg) → indulási hiba, a hely megnevezésével.
- **Írható tokenek:** a regiszterben valamely elemhez rendelt tokenek (a mentés csak ezeket fogadja, M0 2.2). A M1.7 hét regiszteren kívüli tokenje (`fs-alcim`, `fs-kiscim`, `fs-csempe-megj`, `fs-il-eredeti-sor`, `lh-jelleg`, `lh-lxx-csempe`, `space-oszlopkoz`) a tartalékon át előnézetben állítható, de nem menthető; a panel és a változáslista ezt jelöli („csak előnézet”). Ha a felhasználó menteni akarja őket, magyar névvel a regiszterbe kell venni őket (a panel másolható `elemek.toml`-részletet ad).
- **A kizárt lista (`[kizart]`, 46 osztály)** a regiszter-őr kimenetéből készült, az M0 1.2 indokaival, osztályonként egy indokkal. Csak az az osztály áll rajta, amely a felületen előfordul **és** egyetlen regiszter-szelektorban sem szerepel; az M0 1.2 állapot- és szövegrész-osztályai közül a szelektorokban szereplők (`aktiv`, `kijelolt`, `arany`, `krit`, `folyamat`, `he`, `gk`, `st`, `st-link`, `at`, `gl`, `lx`, `hu`, `heb`, `gor`, `nincs-st`, `cimszo`, `torzs`, `app`, `al`, `jel`, `cimkek`, `vers`, `il-vers`) regisztráltnak számítanak, ezért nincsenek rajta (a `.jcim .he` / `.jel-vazlat .he` horga, a `he` is így). A **`jt`** nincs a felületen, így a listán sem (az őr az elavult kizárt osztályt hibának jelzi). Az M0 felmérésén túl két osztály került elő: `szo-nincs` (a felmérésből kimaradt; a párosítás nélküli Károli-szó) és `tervezo-kapcsolo` (az M2 saját vezérlője).

### M2.2 A regiszter-őr (`regiszter_or.py`, F98.15)

- **Módszer** (az M0 1.3 javaslata szerint): a sablonok `class="…"` attribútumai (a `{% … %}` közti szöveg osztály, a `{{ … }}` szöveg-literáljai osztályok; a dinamikus előtag `nezet-` → `oldalak.NEZETEK`, `par-` → `lekerdezesek.bizonyossag_ertekek`, az adatbázisból); a `blokkok.py` és az `oldalak.py` az `ast` modullal (a `class="…"`-t tartalmazó literálok; a `%s` operandusa: literál, feltételes kifejezés, függvényparaméter — alapérték és a hívási helyek literáljai, pl. `ctx_strong_link(…, 'st-link')` —, vagy modulszintű szótár-literál eleme, `JELLEG[j][1]`). A ki nem bontható kifejezés hiba.
- **Hibák:** `ismeretlen CSS-osztály: <osztály> (<fájl>:<sor>) — vedd fel az elemek.toml [[elem]] vagy [kizart] részébe`; az elavult (a felületen nem szereplő) és a fölösleges (szelektorban is álló) kizárt osztály.
- **Mai eredmény:** 127 osztály (221 előfordulás, 22 dinamikus kibontással), 81 a regiszter szelektoraiban, 46 kizárva, **0 hiba**. A `par-` értékkészlet az adatbázisból: `alacsony`, `magas`.

### M2.3 A mentési végpont (`tervezo.py`, F98.16)

| Követelmény (brief 3. pont) | Megvalósítás | Teszt (`teszt_tervezo.py`) |
|---|---|---|
| csak `belso` kiadás | a `/tervezo/*` útvonalakat az `alkalmazas.letrehoz` csak `belso` kiadásban jegyzi be; a lap `tervezo` jelzője is csak ott igaz; a kliens a `tervezo_statikus/` könyvtárból a `/tervezo/…` címen jön (nem a `/statikus/`-ból), így más kiadásban a fájl sem érhető el | `TestKiadasok.test_nyilvanos_es_kereskedelmi` (minden `/tervezo/*` GET és POST 404, a HTML-ben sem `tervezo`, sem `tervező`), `test_a_statikus_export_lapjan_nincs_tervezo` |
| csak helyi kérés | `remote_addr` ∈ {127.0.0.1, ::1, ::ffff:127.0.0.1}, és nincs `X-Forwarded-For`/`Forwarded`/`X-Real-IP`/`X-Forwarded-Host`, és a `Host` `localhost`/`127.0.0.1`/`[::1]` (port megengedett), és az `Origin` (ha van) ugyanaz a helyi cím, és a `Sec-Fetch-Site` (ha van) `same-origin` vagy `none` | `TestMentesBiztonsag.test_kod_csak_helyi_kerésre` (10 tiltott és 3 engedett eset), `test_tavoli_keres_ervenyes_koddal_is_403` |
| csak `POST` | `@app.post`; GET/PUT → 405 | `test_csak_post` |
| egyszeri kód | `GET /tervezo/kod` (no-store, csak helyi kérés) ad egy 32 bájtos kódot (legfeljebb 16 érvényes, 30 percig); a `POST` `X-Tervezo-Kod` fejléce `hmac.compare_digest`-tel; minden elfogadott kód elhasználódik (a 400-as kérésé is); hiányzó vagy rossz kód: 403 | `test_kod_nelkul_rossz_koddal_403`, `test_a_kod_egyszeri`, `test_a_rossz_kerest_is_elhasznalja_a_kodot` |
| csak regiszteres token, érvényes érték | törzs: `{"tokenek": {token: érték}}`, színnél `{"light"|"dark": …}`; a regiszteren kívüli, a betűcsalád- és az ismeretlen token, a rossz alak és a tartományon kívüli érték 400, a fájl változatlan; nem JSON tartalomtípus 415; legfeljebb 64 KB, 400 token | `TestErtekszures` (5 csoport határértékei), `test_a_rossz_ertek_400_es_a_fajl_valtozatlan` |
| szabad szöveg nincs | a fájl a meglévő szótárból, csak érték-cserével, `json.dumps(sort_keys, indent=2)`; a betűcsalád nem írható; az érték csak szám+mértékegység vagy szín-alak | `test_a_fajl_determinisztikus_es_a_diff_kicsi` (a diff pontosan egy sor; a csoportok halmaza változatlan) |
| atomi írás, előző állapot | ideiglenes fájl ugyanabban a könyvtárban (`fsync`), `os.replace`; előtte a régi tartalom `arculat.json.elozo`-ba (szintén atomi; `konfig/.gitignore`); `POST /tervezo/visszaallit` cserél (a visszaállítás is visszavonható); a sorvég (CRLF) megmarad | `test_atomi_iras_hiba_eseten_a_fajl_valtozatlan` (meghiúsuló `os.replace`: a fájl és a betöltött arculat változatlan, ideiglenes fájl nem marad), `test_elozo_allapot_es_visszaallitas`, `test_a_crlf_sorveg_megmarad` |
| újratöltés, ETag | a mentés után az új `Arculat` a gyárban, a lap-gyorsítótár ürül (`Gyorsitotar.urit`); az `arculat.hash` (a tartalom sha256-ja) a lap gyorsítótár-kulcsában, az ETag-ben, a `/arculat.css?v=` címben és a térkép ETag-jében | `TestMentes.test_mentes_es_megjelenes_a_kovetkezo_lapkeresnel` (régi ETag-re 200 és MISS, új stíluslap-cím, süti nélküli kliensen is; a sötét érték mindkét sötét blokkban, a világos változatlan), `test_terkep` |
| CSP nem lazul | a `CSP` állandó változatlan (`script-src 'self'; style-src 'self'`); a lapon nincs inline `<script>`, `<style>`, `style=` vagy `on…=`; a kliens nem használ `innerHTML`-t, `eval`-t, `style` attribútumot, `cssText`-et; az előnézet `style.setProperty('--…')` (CSSOM) | `test_csp_nem_lazul_es_nincs_inline`, `test_a_kliens_szkript_csp_kompatibilis` |

A `/tervezo/terkep.json` (csak `belso`): a regiszter (szelektor-részek és közelítő specifitás), a tokenek (érték, csoport, típus, írható-e), a mentés tartományai, és a stíluslap szabálytérképe (`css_szabalyok`: szelektor → tokenes deklarációk; a dinamikus állapot — `:hover`, `:focus-visible`, `:target`, `::before` … — levágva és megjelölve, a média-lekérdezés megőrizve; a csak ál-elemből álló szelektor, pl. `::selection`, kimarad).

**Korlát:** Fordított proxy mögött a feltétel csak akkor tartja távol a távoli kérést, ha a proxy továbbító fejlécet ad (`X-Forwarded-For`/`Forwarded`/`X-Real-IP`) vagy a külső `Host`-ot továbbítja: így a Caddy alapbeállítása. Az nginx alapbeállítása (`proxy_pass http://127.0.0.1:8000`, `proxy_set_header` nélkül) egyiket sem teszi: a kérés loopbackről, továbbító fejléc nélkül és `Host: 127.0.0.1:8000`-rel érkezik, így egy távoli, `Origin`/`Sec-Fetch-Site` nélküli kérés (pl. `curl`) átmegy a feltételen (a `GET /tervezo/kod` kódot ad, a `POST /tervezo/mentes` ír). A `belso` kiadást ezért proxy mögé csak továbbító fejlécet adó konfigurációval szabad tenni; a kérdés nyitott (DT-F98g, a proxy-választás: N-F76d; az ellenőri napló: `naplok/ELLENOR_TERVEZO_MOD.md`). *(Pontosítva a zárásnál, F98.25: a korábbi „fordított proxy mögött a mentés nem működik” állítás csak a továbbító fejlécet adó vagy a külső Host-ot megtartó proxyra igaz.)* Továbbá: több workerrel a mentés csak az egyik worker arculatát töltené újra. A tervező mód az egy workeres helyi futtatáshoz való (README).

### M2.4 A kliens (`tervezo_statikus/tervezo.js`, `tervezo.css`, F98.17)

Az M0 4. szakaszának vázlata szerint: kapcsoló a fejlécben a szintváltó után (rejtett, amíg a szkript be nem tölt); kiemelés `data-tz-kiemelt` attribútummal és a `tervezo.css` körvonalával, címke a magyar névvel (regisztrálatlan elemnél szaggatott keret, „nem regisztrált elem: `span.mf`”); a kattintás kiválaszt (a legmagasabb specifitású illeszkedő regiszter-sor; az ugyanazon elemen illeszkedő többi sor gombként), nem navigál (a `click`, `auxclick` és `submit` a tervező módban elnyelve); „Szülő elem ↑”; panel csak a regiszterbeli tulajdonságokkal; csúszka és számmező a mentés tartományával (px 0.5, rem/em 0.025, sorköz 0.01 lépés), színválasztó + értékmező + 10 színes paletta a látott témában, mindkét téma értékével; „ez a token N szabályban, M elemen hat ezen a lapon”; változáslista egyenkénti (↶) és teljes visszavonással, `sessionStorage`-ban; „Küldés a szerverre” (megerősítés, kód, POST, újratöltés; a regiszteren kívüli token kimarad és a listában marad) és „Előző mentés vissza”. A tervező saját felülete rögzített színekkel dolgozik (nem az arculat tokenjeivel), hogy egy rossz előnézeti érték ne tegye használhatatlanná.

**Böngészős ellenőrzés** (a Claude desktop beépített böngészője, 1280×900, a próbaszerver a `pardes` WSL-ben, 8799-es port, `belso` kiadás, a konfiguráció ideiglenes másolatával: `PARDES_KONFIG_DIR=/tmp/tz_konfig`; a képernyőkép időnként nem készült el, ezért az állapotot JavaScripttel olvastam, az egér-eseményeket szintetikusan küldtem — a valódi egeres próba az M3):

| Lépés | Eredmény |
|---|---|
| kapcsoló | `aria-pressed="true"`, `data-tervezo` a `<html>`-en, a panel látszik („Tervező mód”) |
| rámutatás a `.he-szo .gl`-re | címke: „Héber szócsempe: átírás és glossza”; a `.gl` kiemelve |
| kattintás | a panel: „Héber szócsempe: átírás és glossza” · „Vers részletei: héber szócsempék · .he-szo .at, .he-szo .gl”; tulajdonságok: Betűméret (`--fs-csempe-glossza`, 1 szabály, 22 elem), Átírás színe (`--muted`, 26 szabály, 546 elem, világos `#58554d`, sötét `#9ba49f`); az URL nem változott |
| csúszka 16px | a `.gl` számított mérete 13.5px → 16px; a változáslista: `--fs-csempe-glossza 13.5px → 16px` |
| Szülő elem ↑ | „Héber szócsempe” |
| tartalék: `.he-szo .mf` | „Nem regisztrált elem” · `span.mf`; betűméret (`--fs-csempe-megj`, „csak előnézet…”), szín (`--muted`), sorköz (`--lh-csempe`); a csúszkával 13px → 15px; másolható `elemek.toml`-részlet (`szelektor = ".he-szo .mf"`) |
| szín (`.he-szo` → Háttér) `#fbf7ee`, rendszer-téma: sötét | a `body` háttere `rgb(251, 247, 238)`; `data-tema="light"` → `rgb(245, 242, 234)` (a világos érték változatlan); `dark` → ismét az új érték |
| egyenkénti visszavonás | a glossza-méret vissza 13.5px-re; a kapcsoló felirata „Tervező (2)” |
| Küldés a szerverre (+ versszám 0.7em) | újratöltés; `/arculat.css?v=cc491d795fceef22`, `--fs-versszam: 0.7em`, `--bg` sötét `#fbf7ee` mindkét sötét blokkban; a próbakonfig diffje pontosan két sor (`versszam`, `bg.dark`), az `.elozo` = az eredeti; a nem menthető `fs-csempe-megj` a listában maradt; **a repó `konfig/arculat.json`-ja érintetlen** |
| Előző mentés vissza | újratöltés; `/arculat.css?v=ed1326eb32081fbf` (az eredeti hash), `--fs-versszam: 0.6em` |
| konzol | nincs üzenet (CSP-sértés sem) |

A Windows-os böngészőből a WSL-ben futó szerverhez érkező kérés a szerver felől loopback (a mentés működött), tehát a helyi kérés feltétele ebben a felállásban teljesül.

### M2.5 A szinkron-szkript (`arculat_szinkron.py`, F98.18)

`python arculat_szinkron.py --kimenet <tokens.json> [--alap <a design system mostani tokens.json-ja>] [--datum …]`: a design system szerkezete (`color.themes/tokens`, `type.fonts/families/groups`, `spacing.tokens`, `radius.tokens`, `name`, `meta`). Az értékek mindig a token-fájlból; a leírás `--alap`-pal a design systemé, különben a regiszterből („Használja: <elemek>”); a vastagság a szerver stíluslapjából (az `oldalcim` 600, M0 5. szakasz 2.); az em-es betűméret relatív értékként jelölve (M0 5. szakasz 3.); a `spacing` a szerver 35 térköz-tokenje. Próbafutás a design system mostani `tokens.json`-jával (`--alap`, a session scratch-könyvtárában, a kimenet is ott): 10 szín, 54 betűstílus (a design system 4 csoportja 7 + 5 + 5 + 1 stílussal, plusz „Szerver: további stílusok” 36-tal), 35 térköz, 6 lekerekítés, `meta.ref = claude/tervezo-mod@fa344619`. Feltöltés nem történt (az a felhasználó kérésére).

### M2.6 Megjelenés-azonosság

Az M2 a stíluslaphoz (`olvaso.css`) és a token-fájlhoz (`arculat.json`) nem nyúlt, tehát a meglévő elemek számított stílusa nem változhatott. A lapok HTML-jét a HEAD (`fa344619`, `git archive` pillanatkép) és a munkafa szerverén vetettem össze (16 lap: kezdőlap, könyvlap, hibalap, `/1Moz/1` mindhárom nézetben, panelek, `/Zsolt/22`, `/Jan/1`, öt szó-lap, két töredék): **nyilvános és kereskedelmi kiadásban 16/16 lap bájtra azonos**; a belső kiadásban a két töredék azonos, a 14 teljes lapon csak a három tervező-sor új (`<button class="tervezo-kapcsolo" … hidden>`, a `tervezo.css` és a `tervezo.js` linkje). A belső kiadás fejlécében így egy új gomb jelenik meg (a szkript betöltése után), ez szándékos változás.

### M2.7 Tesztek

| Tesztfájl | Eredmény | Kihagyva |
|---|---|---|
| `teszt_tervezo.py` (új) | 45 OK | 0 |
| `teszt_arculat.py` | 22 OK | 0 |
| `teszt_szintek.py` | 13 OK (az F98.20 után) | 0 |
| `teszt_pilot_aranymintaval.py` | 22 OK | 0 |
| `teszt_olvaso_szerver.py` | 71 OK | 0 |

A `teszt_szintek.py` `test_bdb_szocikk_minden_resze_alapbol_nyitva` tesztje a HEAD-en (`fa344619`) is bukott: a „Jelentésszerkezet” címtől 600 karakteren belül várta a `<details open>`-t, de az F98.11 óta előtte a vázlat (`nav.jel-vazlat`) áll. A teszt szándéka (a szakasz első lenyitható része nyitva) változatlan; az F98.20 ezt az ellenőrzést írja (a pillanatképen a hiba igazolva).

A brief tesztlistájából a **tartalék** kliensoldali része („a panel a tokenből jövő tulajdonságait kínálja, és az előnézet működik”) böngészőben, kézzel ellenőrzött (M2.4), nem automatikus teszt: a `pardes` venv-ben nincs fej nélküli böngésző. A szerveroldali fele (a térkép a `.he-szo .mf`-re a `fs-csempe-megj`-et adja, nem írhatóként) a `TestMentes.test_terkep`-ben automatikus.

Az `eszkozok/feladatok.py ellenoriz`: 118 brief, 0 hiba, 0 figyelmeztetés.

*Proveniencia:* `scope=eszkozok/olvaso_szerver/ @03acfcb0 (konfig/elemek.toml 34 541 B sha256 206de9651ad4e0a1; tervezo.py 27 546 B; tervezo_statikus/tervezo.js 27 582 B sha256 670c3863db5e9816; konfig/arculat.json változatlan, hash ed1326eb32081fbf), ~/pardes/pardes.db (ext4 másolat, a meta-kivonat az M1.6 szerint azonos), belso/nyilvanos/kereskedelmi kiadás | forras=unittest a pardes WSL .venv-jével (Python 3.12.3, Flask 3.1.3); regiszter_or.py; html_osszevet.py és head_szintek.sh (git archive fa344619) a session scratch-könyvtárában; a Claude desktop beépített böngészője (JavaScript-ellenőrzés, próbaszerver 8799, PARDES_KONFIG_DIR=/tmp/tz_konfig); arculat_szinkron.py a design system tokens.json-jával (verzió 1791995892-d37b, sha256 899439f5…) | ts=2026-10-15`

### M2.8 Nyitott tételek az M3-hoz

1. **⛔ M3 — a felhasználó kipróbálja** a futó szerveren: kiválaszt, állít, előnézetben lát, visszavon, ment, visszaállít. Az észrevételei ide kerülnek, a javítás ugyanebben a menetben.
2. A hét regiszteren kívüli token (M2.1) csak előnézetben állítható; ha mentést is akar rájuk, magyar névvel a regiszterbe kell venni őket.
3. A belső kiadás fejlécében új gomb jelenik meg (M2.6); ha zavaró, a helye és a megjelenése a `tervezo.css`-ben állítható.
