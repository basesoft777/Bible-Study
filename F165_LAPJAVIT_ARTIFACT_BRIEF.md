---
feladat: 165
cim: A /lap-javit artifact-módja: beépített beszélgetés a lapnézetben
kod: LAPJAVIT_ARTIFACT
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: nem_indult
ad: a lapnézet-artifactban bekezdésenként „Kérdezz / javasolj” gomb (`sample` capability); a jóváhagyott javaslat a lap `db`-jébe kerül (hely, régi, új, ok); a session `ArtifactData`-val kiolvassa, a `/lap-javit` szabályai szerint beírja a forrásba, és újrapublikálja a nézetet; a `lap_javitasok.tsv` naplózása marad
kovetkezo: "Te: indítás a /kovetkezo-val, a #123 /lap-javit részének (#618) merge-e után"
olvas: [.claude/commands/lap-javit.md, eszkozok/lektor_felulet/, adat/lap_javitasok.tsv, adat/SEMA.md]
ir: [.claude/commands/lap-javit.md, eszkozok/lektor_felulet/epit.py, eszkozok/lektor_felulet/sablon.html, eszkozok/teszt_lektor_felulet.py]
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

*(a menet tölti ki)*
