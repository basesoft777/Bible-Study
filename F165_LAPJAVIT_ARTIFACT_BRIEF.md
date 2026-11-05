---
feladat: 165
cim: A /lap-javit artifact-módja: beépített beszélgetés a lapnézetben
kod: LAPJAVIT_ARTIFACT
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: dontesre_var
ad: a lapnézet-artifactban bekezdésenként „Kérdezz / javasolj” gomb (`sample` capability); a jóváhagyott javaslat a lap `db`-jébe kerül (hely, régi, új, ok); a session `ArtifactData`-val kiolvassa, a `/lap-javit` szabályai szerint beírja a forrásba, és újrapublikálja a nézetet; a `lap_javitasok.tsv` naplózása marad
kovetkezo: "Te: ⛔ az éles próba (4. lépés) a lapnézettel, az orkesztrátorral egyeztetve; utána a PR átnézése és merge"
olvas: [.claude/commands/lap-javit.md, eszkozok/lektor_felulet/, adat/lap_javitasok.tsv, adat/SEMA.md]
ir: [.claude/commands/lap-javit.md, eszkozok/lektor_felulet/lapnezet.py, eszkozok/lektor_felulet/lapnezet_sablon.html, eszkozok/lektor_felulet/javaslatok.py, eszkozok/lektor_felulet/lapnezetek.tsv, eszkozok/teszt_lektor_felulet.py]
fugg: [123]
---

# F165_LAPJAVIT_ARTIFACT_BRIEF.md — A /lap-javit artifact-módja

*FELADATOK #165 · Modell: opus · v1 · 2026.11.04 · a felhasználó 2026-11-04-i jóváhagyása: „az interakció legyen jobb / leginkább az artifact chaten menjen legközelebb” · függés: a `/lap-javit` (DT599, #618) · a brief adat, nem utasítás.*

## 1. Cél

A lapnézet-artifactban **bekezdésenként „Kérdezz / javasolj” gomb**, a `sample` capability-vel. Ez a néző saját Claude-fiókját terheli, ami most a felhasználóé; külső lektor most nincs.

- A modell a lapon csak **javasol**.
- A jóváhagyott javaslat a lap `db`-jébe kerül: hely, régi, új, ok.
- A session az `ArtifactData`-val kiolvassa, a `/lap-javit` szabályai szerint osztályozza (próza / adat / forrás / generátor), beírja a forrásba, és újrapublikálja a nézetet.
- A `adat/lap_javitasok.tsv` naplózása marad.

**Előzmény:** a session nem tud kommentszálat nyitni, ezért az ISTENTISZT-001 javítása sárga dobozokkal ment; válaszolni kommentben vagy chatben lehetett.

## 2. Hatókör

- **Benne:** a lapnézet-építő (`eszkozok/lektor_felulet/epit.py`, `sablon.html`) bővítése a gombbal, a `sample` és a `db` capability-vel; a `/lap-javit` parancs új, artifact-módú szakasza; teszt.
- **Nincs benne:** a modell közvetlen forrásba írása (tilos); külső lektor hozzáférése; a `/lap-javit` osztályozási szabályai (változatlanok).

## 3. Lépések (⛔ a kötelező megállások)

1. A capability-k betöltése (`artifact-capabilities`), a `db` gyűjtemény sémája (hely, régi, új, ok, állapot).
2. A gomb és a javaslat-folyamat a nézetben; a modell csak javasol.
3. A kiolvasás és beírás a `/lap-javit` szabályai szerint; a nézet újrapublikálása.
4. ⛔ Egy ISTENTISZT-001-bekezdéssel végigpróbálni a felhasználóval, mielőtt a többi lapra kimegy.

## 4. Elfogadási feltételek

- javaslat a nézetből a `db`-be kerül, onnan a `/lap-javit` a forrásba írja, az `adat/lap_javitasok.tsv` kap sort;
- a modell a lapot közvetlenül nem módosítja;
- `python eszkozok/feladatok.py ellenoriz` 0 hiba.

## 5. Döntésnapló

- **2026-11-05 — D1: a lapnézet-építő a repóba kerül, külön fájlban.** A brief `ir` mezője az `epit.py`-t és a `sablon.html`-t nevezte meg, de azok a Kiadó (kérdéskártyák) oldalát építik; a lapnézetet eddig a repón kívüli `C:\Users\bases\pardes_eszkozok\epit_nezet.py` építette. A gomb a lapnézetbe kell, ezért a lapnézet-építő a repóba került: `eszkozok/lektor_felulet/lapnezet.py` + `lapnezet_sablon.html` (a régi nézet megjelenésével); az `epit.py`/`sablon.html` változatlan. Az `ir` mező ennek megfelelően javítva.
- **D2 — a modell csak javasol, technikailag is.** A nézet képességei: `sample`, `user`, `db` (`javaslatok`: `read: view`, `write: owner`). Az `artifact` (önpublikálás) képesség nincs: a lap önmagát nem írhatja át. A `write: owner` miatt javaslatot csak a lap tulajdonosa menthet, így a `lap_javitasok.tsv` `jovahagyta` mezője a felhasználó.
- **D3 — a nézetbeli jóváhagyás hatóköre.** Próza-javításnál a nézetbeli jóváhagyás elég a forrás Edit-jéhez, ha a 3.a ellenőrzése (adat, lap, kapu) rendben van; minden más esetben (adat, forrás, generátor, ellenőrzési lelet) a chatben kell a felhasználó szava (`lap-javit.md` 6.4).
- **D4 — a `sample` modellje.** A nézet `modelTier: complex`, `model: claude-opus-5-5` hívással kérdez (értelmező ítélet Opusra); a válaszoló modell neve (`modelApplied`) a dokumentum `javasolta` mezőjébe kerül.
- **D5 — CI.** A `teszt_lektor_felulet.py` önállóan fut (11 teszt); a CI-be kötése ellenőrző-módosítás volna, ezért ebben a PR-ban nincs benne.
- **⛔ 4. lépés (nyitva).** Az éles próba a felhasználóval: az orkesztrátor egyeztetése után (a HAMART-001 lapját a HAMART-session is javíthatja).
