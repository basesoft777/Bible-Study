# F121 — az ALVIL-001 lexikonlap 13 hiányzó szótári egysége (napló)

*Menet: 2026-10-29, `claude-sonnet-5-5` (a kért modell: `sonnet`; a modell-ellenőrzés egyezik). Ág: `claude/f121-alvil-13` (friss `origin/main`-ről). Megbízó: az orkesztrátor; a felhasználó szó szerint (az orkesztrátor chatjében, 2026-10-29): „Igen, így” — a jóváhagyott szöveg: „… A 13 fordítás az M1 után Sonnettel, a #121 eszközével.” Bemenet: a #123 átadó listája (`naplok/F123_forditas_atadas_ALVIL-001.tsv`, a `claude/f123-alvil-adat` ágon). Az ALVIL-001 lapot ez a menet **nem** generálja újra, a #123 fájljaihoz nem nyúl.*

**Állapot: rögzítve (F121.15).** A DT408, DT409, DT410 eldöntve (orkesztrátor, a felhasználó felhatalmazásával, 2026-10-29). Az ellenőri jelentés (ELLENOR_F121_3) javításai után a PR draft.

## 1. Az átadó lista két hibája (a #123-nak)

1. **A két glossza-sor hash-e hibás.** A lista a `UBS_DNTG 12.50 glosszak_hu` és az `UBS_DBH 007131001001000 glosszak_hu` sorához a *definíció* hash-ét (79, illetve 266 karakter) adja. A valódi forrás: „death” (5 karakter) és „world of the dead” (17 karakter). A `forditasok.tsv`-be a valódi forrás hash-e kerül.
2. **A tW-sorok kulcsa nem a lap Strongja.** A lista a `kt/hades`-t, a `kt/hell`-t a `G0086` alatt sorolja; a `forditasok.tsv` kulcsában a cikk első Strongja áll (`H7585`; `other/pit` → `H0875`; `other/tomb` → `H1430`), ahogy a generátor hívja (`forditas_ehhez('tW_szocikkek', r['strongok'][0], …)`). A rögzítés a hiánylista (`naplok/F123_adat_ALVIL-001_forditas_hiany.tsv`) `strong_kulcs` oszlopát követi.

## 2. Forrásszerződés (DT408, javaslat)

A hat nem-UBS forrásnak nincs `lexikon_hivatkozasok.tsv`-sora, ezért az `ellenoriz.py` 13. szabálya nem találna forrásszöveget. A feloldó: `glossza_lexikon_forditas.tovabbi_forras` (SEMA 2.14 új bekezdése, tesztek: `teszt_glossza_lexikon_forditas.py` `TovabbiForras`, `teszt_ellenoriz_13.py` `Szabaly13Tovabbi`). **Eltérés a #123 listájától:** a TBESH/TBESG-sor forrása a 7–8. oszlop tisztítva (a lista a teljes tabos sort hash-eli); ennek oka, hogy a fordítás a glosszát és a szócikket fedi, a fejléc-lemmát (ᾍδης, שְׁאוֹל) a lap külön adja, és az 1. kapu a nyers sorban a lemmát hiányolná. A TBESG/TBESH-sor hash-e ezért nem egyezik a lista előtagjával (a másik 11 egyezik, a 2 glossza az 1. pont szerint javítva).

## 3. A tervezet és a kapuk

`naplok/F121_ALVIL_forditas_tervezet.tsv` (forrás, fordítás, hash soronként). Kapuk: **9 sor átment**, **4 sor** a 11. (könyvnév-) kapun bukik, kizárólag azért, mert a kapu forrásoldalon nem ismeri a `Matthew` / `Revelation` / `Romans` alakot, sem a pontozott `Mat.` / `Rev.` / `Luk.` alakot (TBESG-ben): a fordításban a hivatkozások darabra egyeznek a forrással (Károli-rövidítések: Mt, Jel, Róm, Luk, Ján, ApCsel, 1Móz, Jón, Jób, Péld, Mk, Jak). Kézi egyeztetés: `naplok/F121_ALVIL_forditas_bukottak.tsv`. A gate-hiba a 11. kapu külön javítandó pontja (nem ennek a menetnek a tétele).

| Sor | Kapuk | Megjegyzés |
|---|---|---|
| TBESG G0086 `teljes` | 11. bukik (kézi) | „pokol: Hádész …”; `__1.`/`__2.` → 1./2. |
| tW `kt/hades` (H7585) | 11. bukik (kézi) | „Ábrahám kebele” (Károli Luk 16:22; forrás: *side*) |
| tW `kt/hell` (H7585) | 11. bukik (kézi) | |
| tW `other/pit` (H0875) | átment | |
| tW `other/tomb` (H1430) | 11. bukik (kézi) | |
| UBS_DNTG 12.50 glossza, definíció | átment | „halál”; „(idióma, szó szerint: a Hádész kapui) a halál mint személytelen természetfeletti hatalom” |
| MCGED G50087 glossza | átment | |
| LSJ G0086 `teljes` | átment | csere-alapú: a görög/idegen karakterek bájtra azonosak; Iliász/Odüsszeia kifejtve (LSJ G2564 mintája) |
| TBESH H7585 `teljes` | átment | „pokol: Seol Seol, alvilág, sír, pokol, verem 1a) …” |
| UBS_DBH 007131001001000 glossza, definíció | átment | „a holtak világa”; a 63 cella erre a glosszára vált |
| BDB H7585 `nyelvi_hatter` | átment | az F28 `teljes` sor (`kezi`, Opus) megfelelő szakasza változatlanul; a forrás elírásai (*palce*, *hallow*) a fordításban *helye*, *üreges* |

## 4. Terminológia (DT409, javaslat)

Kilenc új v4 sor (`adat/terminologia.tsv`, a megjegyzés „F121 ALVIL-001 menet (javaslat…)”-tal kezdődik): `Sheol` → Seol, `Hades` → Hádész, `underworld` → alvilág, `hell` → pokol, `tomb` → sírbolt (mind `kapu=igen`), `grave` → sír, `pit` → verem, `lake of fire` → tüzes tó (`kapu=nem`), és `Bibl. Hades` → `Bibl. Hades` (`igen`: Beer műcíme a BDB H7585 szócikkében; e nélkül a `Hades` kapu a címet is hádészre kényszerítené).

## 5. Mankók (a felhasználó nem engedte el)

Eszköz: `python eszkozok/glossza_lexikon_forditas.py manko | szojegyzek | visszamenoleges` — most `--jel F121.14 --ki …` kapcsolóval, így a korábbi menetek naplói nem íródnak felül. Újdonságok: (a) a hosszú (`forditas_hu`) sorokra **kulcsszó-ellenőrzés** (`kulcsszo_ellenorzes`): azok a szójegyzék-kulcsok, amelyek az angol forrásban szó szerint állnak, a magyar alakjuk Károli- és BDB-egyezése; (b) a visszamenőleges felmérés `--uj-term` kapcsolója: az új terminológia-sorok a régi sorokon.

- **`naplok/F121_ALVIL_forditas_manko.tsv`** (13 sor): 4 egyezik, 9 kézi ítéletre. A kézi ítéletek mind ugyanabból a két okból jönnek, és soronként megegyeznek a terminológia-döntéssel: (i) a Károli a G86-ra a #22 párosításban „pokol”-t ad (3+1; az ApCsel 2:27, 31 Károli-szövege „sírban”, ez a párosításban nem szerepel), tehát a *Hádész* és az *alvilág* nincs a Károli-alakok között; a H7585-re seol, sír, koporsó, pokol, mélység; (ii) a BDB-magyar szövegben a *Seol*, *Hádész*, *sírbolt* kisbetűs/más alakban áll. A rangsor (szójegyzék > Károli > BDB, DT239) szerint ez tájékoztató; a javaslat: marad.
- **`…_szojegyzek_javaslat.tsv`** (DT240): 437 versengő angol kulcs a gyorsítótárban; **új sort nem javasolok** (a legtöbb szótövezési/formai eltérés).
- **`…_visszamenoleges.tsv`** (DT242): 12 tétel, mind más sorokat érint, a tábla nem íródott. 2× Thayer G1941 `teljes` (archív `kezi` sor, a lapra nem kerül) és BDB H3068 (`deity`/istennév) a korábbi menetből; újak: a BDB H7585 `teljes` `Sheol`/`Hades` (a `Hades` találat álpozitív: a *Bibl. Hades* műcím), BDB H0559 `hell`, és hat BDB-sor `tomb` → *sírbolt* hiánya (H4908, H6912, H1004 `sz8`, H0068 `sz4`, H2710 `sz4`, H1430 `sz4`). Javaslat: egyik sem változik (a BDB-ben a *tomb* = sír/sírkamra, a régi sorok jóváhagyottak); a `tomb` → *sírbolt* sor ezért a tW-re és az új sorokra érvényes.

## 6. Mit nem csináltam

- Nem generáltam újra az ALVIL-001 lapot; nem nyúltam a #123 fájljaihoz.
- Nem javítottam a 11. kaput (a `Matthew`/`Revelation`/`Romans` alias hiánya) és a #123 átadó listáját: ezek külön tételek.
- A `pardes.db` nem épült újra; a szónézet és a lap az új sorokat csak újraépítés után mutatja.

## 7. Az MCGED-sor kivétele és a D1 (DT411, 2026-10-29)

- A 13-ból **12 sor** marad: az `MCGED G0086 G50087 glosszak_hu` („the invisible abode or mansion of the dead; …”) kikerült. Indok: a Mounce szövege „Copyright 1993 All Rights Reserved”, a DT235 / DT272 (c) („a Mounce kimarad”) nyitott; lefordított szöveget nem teszünk közzé a licencdöntésig. **Hiányként jelölve** (DT235); a lapon a Mounce csak forrásmegjelölés (DT-F131m).
- A BDB H7585 sor marad (DT410 (1)); a brief E5 pontja kiegészítve.
- **D1 rendben:** a `licencek.tsv`-ben megvan a TBESG (CC BY 4.0), az LSJ (CC BY-SA 4.0) és a tW_szocikkek (CC BY-SA 4.0) sora.
