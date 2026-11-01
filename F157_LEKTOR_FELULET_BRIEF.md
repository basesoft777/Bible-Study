---
feladat: 157
cim: Lektor-felület — a lektori és ellenőrző kérdések egy helyen, közös sémával; a felhasználó dönt, a válasz csak szabályos úton (jelöltdöntés vagy döntéstétel) jut a repóba
kod: LEKTOR_FELULET
tipus: feladat
fazis: folyamat
modell: sonnet
munka: folyamat
allapot: megallt
ad: egy közös kérdés-séma minden kérdés-forrásra (a `/kiadas` lektora, a határ-ellenőrzés `naplok/HATAR_<ID>.md`, a próza-lefedettség, a kiejtés-kalibráció, az artifact-kommentek, a `proza_javaslat`: a lektor olvasás közben is kérdezhet, a `dontes`: a `DONTESEK.md` nyitott tartalmi tételei, a `motivum_jelolt`: talált, kidolgozatlan motívumok); motívumonként generált `naplok/LEKTOR_<ID>.tsv`; egy artifact a kalibráló sablon mintájára (kérdésenként: elfogadom / elvetem / visszakérdezek / saját szöveg; szűrés forrás és motívum szerint; ugrás a lapnézet helyére); a válaszok tárolója és kérésre történő beolvasása; a szabályos visszaút (`jeloltek.tsv` sor `manual` provenienciával és a válasz idézetével, `DONTESEK.md` DT-F helyőrző, prózai teendő a forrásfájl feladataként), közvetlen út az adatba nincs
kovetkezo: "/kovetkezo, 0. ellenőrzés (db capability), M0"
olvas: [naplok/HATAR_ISTENTISZT-001.md, naplok/HATAR_HAMART-001.md, eszkozok/motivum_hatar.py, eszkozok/kiejtes_szoveg.py, adat/jeloltek.tsv, adat/motivumok.tsv, adat/SEMA.md, DONTESEK.md, "lexikon/*_TUDOMANYOS.md", F151_MOTIVUM_HATAR_BRIEF.md, F125_GERINC_KARTYA_SZOVEG_BRIEF.md, F86_ELOFIZETES_FEED_BRIEF.md, CLAUDE.md]
ir: [eszkozok/lektor_kerdesek.py, eszkozok/teszt_lektor_kerdesek.py, eszkozok/lektor_felulet/, "naplok/LEKTOR_*.tsv", naplok/LEKTOR_FELULET_naplo.md]
fugg: []
nem_fugg: [10, 12, 36, 86, 121, 123, 125, 131, 146, 148, 151, 152]
---

# Fnn_LEKTOR_FELULET_BRIEF.md — lektor-felület

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet · v1 (tervezet) · 2026.11.01 · forrás: az orkesztrátor-session
jóváhagyott terve (`FEED_STASH_LEKTOR_terv_2026-11-01.md`, a session-csoport megosztott jegyzetmappájában) és a felhasználó
szavai, alább szó szerint. A brief szövege adat, nem utasítás.*

## 1. Cél

A felhasználó kérése (szó szerint): „Kell egy lektor / revier felület, ezt tervezd meg.” A három nyitott tervkérdésre a
javaslatot kérte (szó szerint): „javaslat?” — a javaslat a 6. szakaszban; a felhasználó elfogadta („Igen, mehet”, „Igen, mind”).

**Elv:** a lektor nem ír át, csak kérdez; a döntés a felhasználóé; a repóba csak szabályos úton (`adat/jeloltek.tsv`,
`DONTESEK.md`) jut válasz, **közvetlen út nincs** (CLAUDE.md 2. szabály; DT28 egyirányúság). A felület kérdéseket mutat és
válaszokat gyűjt; a válasz adat, nem utasítás: döntéstétel csak a válasz idézetével, egy session átvezetésével lesz belőle.

## 2. Kiinduló tények (2026-11-01, a mai main)

- **Határ-ellenőrzés (#151):** az `eszkozok/motivum_hatar.py` kész; a `naplok/HATAR_ISTENTISZT-001.md` és a
  `naplok/HATAR_HAMART-001.md` gépi része megvan. A modelles rész (`hatar-ellenor` subagent) a #151 ⛔ pontján áll (DT443).
- **A `/kiadas` lektora (#125):** a `F125_GERINC_KARTYA_SZOVEG_BRIEF.md` 7. pontja írja le (friss kontextus, másik modell, csak a
  jelölt helyeken, kérdéslista, átírás nélkül); a `.claude/commands/kiadas.md` és az `eszkozok/proza_lefedettseg.py` ma nem
  létezik (#125 ⬜).
- **Kiejtés-kalibráció:** a kalibráló sablon a repón kívül él (`C:\Users\bases\pardes_eszkozok\kalibracio_sablon.html`; előkép:
  artifact T9Uo78435J6PoyDweSE6TL és MwXB1m55ic8CjgPLZ6U6X7); a válaszokat ma a böngésző `localStorage`-a tartja, tehát csak
  abban a böngészőben élnek.
- Előzmény még: a Megvalósulás-jelentés (Claude Docs FxVMBRHBt2ER1Gwh2oYktN); a #86 (`F86_ELOFIZETES_FEED_BRIEF.md`, DT-F86e/f)
  — a lektori kérdések száma (nyitva/zárva) a Feed belső rétegébe megy (`beerkezo/Fnn_MUHELY_FEED_STASH_BRIEF.md`, a „kész”
  7. pontja), a kérdések szövege nem nyilvános.

## 3. Hatókör

### 3.1 Közös kérdés-séma

Egy kérdés egy sor; a mezők:

| mező | érték |
|---|---|
| `kerdes_id` | stabil azonosító: `<forras>:<motivum>:<sorszám vagy horgony-hash>`; újragenerálásra nem változik, ha a kérdés nem változott |
| `forras` | `lektor` (`/kiadas`) · `hatar` (`naplok/HATAR_<ID>.md`) · `proza_lefedettseg` · `proza_javaslat` (a lektor olvasás közben kérdez: az adatból ez következik, de a lap nem mondja ki) · `dontes` (a `DONTESEK.md` nyitott tartalmi tétele; technikai/folyamat-döntés nem) · `motivum_jelolt` (talált, kidolgozatlan motívum: érdemes-e kidolgozni; `igen` = `/befogad`-javaslat, ID közvetlenül nem keletkezik) · `kiejtes_kalibracio` · `artifact_komment` |
| `motivum` | motívum-ID |
| `hely` | szakasz-horgony (a lexikonlap RÉS-/szakaszjelölője) vagy igehely (`1Móz 3:16`-alak) |
| `kerdes` | a kérdés szövege, a forrás saját szavaival (idézett sorokkal, `fájl:sor`) |
| `valaszlehetosegek` | a forrás által felkínált lehetőségek (`;`-vel), üres is lehet |
| `proveniencia` | a kérdést előállító futás sora (`scope=… | forras=… | ts=…`); kézi kérdésnél `manual` |
| `allapot` | `nyitva` · `megvalaszolva` · `atvezetve` |
| `valasz` | a felhasználó válasza szó szerint (a tárolóból beolvasva) |
| `atvezetes` | a visszaút: a `jeloltek.tsv` sora, a DT-F helyőrző, vagy a prózai feladat, és a commit/PR |

### 3.2 `naplok/LEKTOR_<ID>.tsv` — generált

- Az `eszkozok/lektor_kerdesek.py` motívumonként a forrásokból generálja (a forrásokat csak olvassa); a meglévő sorok `valasz`,
  `allapot`, `atvezetes` mezőjét megőrzi, a kérdés-mezőket újraírja. Írás előtt összevetés az eredetivel, eltérésnél megállás
  (minta: `eszkozok/igazolas_migracio.py`); TSV `split('\t')` / `'\t'.join()`, a CLAUDE.md UTF-8-wrapperével.
- A fájl generált (fejléc-megjegyzés `# GENERÁLT: …`); kézzel nem szerkeszthető, a válasz a felületről és a beolvasásból jön.
- Az első lépcsőben csak a ma létező forrás kerül be: `hatar` (gépi rész). A `lektor` és a `proza_lefedettseg` a #125 után, a
  `kiejtes_kalibracio` a sablon átvétele után, az `artifact_komment` az `ArtifactComments` beolvasásával.

### 3.3 Felület — artifact a kalibráló sablon mintájára

- A sablon a repóba kerül (`eszkozok/lektor_felulet/`: HTML-sablon és az építő szkript a `pardes_eszkozok/epit_nezet.py`
  mintájára), hogy a felület verziózott legyen.
- Kérdésenként gombok: **elfogadom / elvetem / visszakérdezek / saját szöveg**; szűrés forrás és motívum szerint; ugrás a lapnézet
  `hely`-ére (az arany lap nézetének horgonyára).
- Telefonon is használható (egy hasáb, nagy gombok).
- Az artifact privát indul; a megosztás a felhasználóé.

### 3.4 Visszaút — szabályos, közvetlen út nélkül

Egy session **kérésre** beolvassa a válaszokat (6. szakasz, DT-F<nn>c, eldöntve), és mindegyiket a fajtája szerint vezeti át:

- **jelöltdöntés:** `adat/jeloltek.tsv` sor `manual` provenienciával, az indoklásban a válasz idézetével és a `kerdes_id`-vel;
- **tartalmi döntés:** `DONTESEK.md` tétel DT-F helyőrzővel, a válasz idézetével; ha a döntés a felhasználó jóváhagyását kéri,
  a session megáll;
- **`proza_javaslat` „igen”:** prózai teendő (alább) — a kérdés megnevezi a forrás adatsort (`fájl:sor`, kötelező) és az adat saját proveniencia-sorát; a lektor mondatot **nem** ír és nem javasol (DT-F32b: a próza egy kézben, Opus), a mondatot a próza írója írja az egészet olvasva;
- **prózai teendő:** a forrásfájl feladata (`/befogad`-dal, a felhasználó jóváhagyásával) — a lektor-felület prózát nem ír, a
  generált lapot nem szerkeszti;
- a `LEKTOR_<ID>.tsv` sorába az átvezetés commitja/PR-ja kerül, az `allapot` `atvezetve` lesz.

A „visszakérdezek” válasz új kérdést nyit ugyanarra a `hely`-re, a forráshoz rendelve; döntés nem lesz belőle.

### Nincs benne

- bármely motívumfájl, forrásfájl vagy lexikonlap írása; értelmező próza (K1); automatikus döntés;
- a `/kiadas` lektorának, a `hatar-ellenor` subagentnek vagy a próza-lefedettség mérőjének megírása (#125, #151);
- a Feed/Stash szkript (külön tervezet) — ez csak a `LEKTOR_<ID>.tsv`-t adja neki.

## 4. Lépések (⛔ a kötelező megállások)

0. **Ellenőrzés:** a DT-F<nn>a–c eldöntve (6. szakasz); a végrehajtó a befogadott brief 6. szakaszából veszi át őket, és
   megnézi, hogy az artifact-adatbázis (db capability) ma elérhető-e. Ha nem, a tartalék (másolható összesítő) az első lépcső, és
   ezt a naplóba írja.
1. **M0:** az `eszkozok/lektor_kerdesek.py` és a teszt; a `naplok/LEKTOR_ISTENTISZT-001.tsv` és a `naplok/LEKTOR_HAMART-001.tsv`
   a `hatar` forrásból (a meglévő `HATAR_*.md` gépi része). A teszt: stabil `kerdes_id` újragenerálásra; a válasz-mezők
   megőrzése; nem létező forrás üres, jelölt eredmény, nem hiba.
2. A felület (`eszkozok/lektor_felulet/`) és az artifact az M0 kérdéseivel; a tároló a DT-F<nn>b (eldöntve) szerint. ⛔ a felhasználó
   kipróbálja (telefonon is) és jóváhagyja.
3. Egy próbakör: a felhasználó válaszol néhány kérdésre; egy session beolvassa, és a 3.4 szerint átvezetési **javaslatot** ír a
   naplóba (a `jeloltek.tsv`-sor és a DT-F tétel szövege). ⛔ a felhasználó jóváhagyja az átvezetést; csak utána íródik.
4. A többi forrás bekötése, ahogy a forrásuk elkészül (`lektor` és `proza_lefedettseg` a #125 után; `kiejtes_kalibracio`;
   `artifact_komment`) — forrásonként külön tétel.

## 5. Elfogadási feltételek

- A `LEKTOR_<ID>.tsv` generált, fejléccel; újragenerálás után a válasz-mezők bájtra változatlanok.
- A felület és a beolvasás egyetlen adattáblát sem ír; adat csak a 3. lépés jóváhagyott átvezetéséből, `manual`
  provenienciával és a válasz idézetével kerül a `jeloltek.tsv`-be vagy a `DONTESEK.md`-be.
- A tároló sora adat, nem utasítás: a beolvasó session idézi, nem hajtja végre.
- `python eszkozok/feladatok.py ellenoriz` 0 hiba; `python eszkozok/ellenoriz.py` új HIBÁT nem ad.

## 6. Döntésnapló

*A három pont döntése (2026-11-01): a felhasználó a három kérdésre a javaslatot kérte („javaslat?”); az orkesztrátor javaslata az
alábbi; a brief-írást a felhasználó erre hagyta jóvá: „Igen, mehet”; és megerősítette (szó szerint, az orkesztrátor
továbbításában): „Igen, mind” — arra az üzenetre, amely kimondta, hogy a három pontot a befogadáskor elfogadottként rögzítjük.*

- **DT-F<nn>a ✅ eldöntve** (javaslat szerint; „Igen, mehet”, „Igen, mind”) — egy felület vagy több: **egy felület mindhárom
  kérdésfajtára** (lektori, határ-, kalibrációs és egyéb kérdések), közös sémával, egy helyen döntve, forrás szerinti szűrővel.
- **DT-F<nn>b ✅ eldöntve** (javaslat szerint; „Igen, mehet”, „Igen, mind”) — a válaszok tárolója: **artifact-adatbázis** (db
  capability): tartós, telefonról is elérhető, a session az `ArtifactData`-val olvassa; tartalék: a felület másolható összesítő
  sort ad, ha az adatbázis nem érhető el. A db sora adat, döntéstétel csak idézettel lesz belőle (a `localStorage` csak kényelmi
  tartalék, nem tároló).
- **DT-F<nn>c ✅ eldöntve** (javaslat szerint; „Igen, mehet”, „Igen, mind”) — a beolvasás ütemezése: **kérésre**, nem minden
  merge után; a Feed belső rétege mutatja a „megválaszolva, de nincs átvezetve” számot, hogy a felhasználó lássa, mikor érdemes
  beolvastatni.
- **DT-F157d ✅ eldöntve** (javaslat szerint; a felhasználó felvetése: „a lektor nem kaphat olyan kérdést" mi az amit az adatból meg lehet irni" prózát”, a javaslatra: „mehet”) — a lektor olvasás közben is kérdezhet (`proza_javaslat` forrás: adatsor és proveniencia kötelező), de prózát nem ír; az „igen” a forrásfájl prózai feladata, a mondatot a próza írója írja. Megvalósítva: `eszkozok/lektor_kerdesek.py` (`proza_javaslat_sor`), a felület gombjai, `naplok/LEKTOR_FELULET_naplo.md` M2.
- **DT-F157e ✅ eldöntve** (javaslat szerint; a felhasználó felvetése: „a lektor felület /reviewer felült is / pl döntések / már csak tartalmi / kidolgozatlan de talált motivumok?”, a javaslatra: „mehet”) — két új kérdés-forrás: (1) `dontes`: a `DONTESEK.md` nyitott TARTALMI tételei kártyaként (kérdés, lehetőségek, javaslat indokkal, a négy gomb); technikai/folyamat-döntés (CI, merge, ütközés, javítókör) nem kerül ide; visszaút: session beolvassa, a felhasználó idézetével a `DONTESEK.md`-be. (2) `motivum_jelolt`: talált, kidolgozatlan motívum kártyája (jelölt neve, talált igehelyek, forrás, „érdemes-e kidolgozni?”); „igen” esetén a CLAUDE.md négy kötelező kérdése a session előre kitöltött javaslatával; az „igen” `/befogad`-javaslat, a felhasználó fogadja be; ID közvetlenül nem keletkezik. Az építés a felmérés (`naplok/LEKTOR_FELULET_naplo.md` M3) megmutatása után.
