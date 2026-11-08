---
feladat: 165
cim: A /lap-javit lapnézete: a generált lap blokkjelekkel, a javítás a sessionben
kod: LAPJAVIT_ARTIFACT
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: fut
ad: a lapnézet-artifact csak a generált lapot mutatja, minden blokk mellett látható jellel (pl. `1/a·12`); a felhasználó a chatben a jelre vagy idézetre mutat rá; a javítás a sessionben, a `/lap-javit` szerint folyik, a jóváhagyás után a session vezeti át, naplózza (`lap_javitasok.tsv`) és újrapublikálja a nézetet (DT637)
kovetkezo: "Te: a próba kész (2026-11-08, „működik”); a draft PR #641 átnézése és merge"
olvas: [.claude/commands/lap-javit.md, eszkozok/lektor_felulet/, adat/lap_javitasok.tsv, adat/SEMA.md]
ir: [.claude/commands/lap-javit.md, eszkozok/lektor_felulet/lapnezet.py, eszkozok/lektor_felulet/lapnezet_sablon.html, eszkozok/lektor_felulet/lap_javitas_naplo.py, eszkozok/lektor_felulet/lapnezetek.tsv, eszkozok/teszt_lektor_felulet.py, dontesek/uj/upbeat-pare-476379.md]
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
- **2026-11-05 — D6: a próba és a megkötések (orkesztrátor, a felhasználó felhatalmazásával).** Próba előbb az ISTENTISZT-001-en, új privát URL-en (`https://claude.ai/artifact/3NpqLc7P4FqHjU88zGpD8x`); a kiadott lapra a lelet a következő kiadás nyitott tétele, a próza-javítás a próza gazdájának megy (`lap-javit.md` 6.4–6.5).
- **2026-11-08 — DT637: a nézetben nincs beszélgetés (a felhasználó kérése).** A felhasználó szavai (a befogadó sessionen át): „az artifactba ne kerüljenek blokkok; az artifact csak generálja le a lexikon-lapot; a blokkra a felhasználó tud rámutatni; a javítás kontextusa a sessionben legyen; a jóváhagyás után a session vezesse át a javításokat”; a #641-en való átdolgozást a felhasználó jóváhagyta („Igen, a #641-en”). Ezzel **a D2–D4 és a `sample`/`db`-alapú artifact-mód elvetve**: a nézetből a gomb, a panel, a Claude-hívás és a `javaslatok` tár kikerült; a blokkokra bontás a `lapnezet.py`-ban van (a nézet és a `--jel` lekérdezés ugyanabból a bontásból dolgozik); a `javaslatok.py` helyett a `lap_javitas_naplo.py` csak a napló biztonságos bővítését végzi. A brief 1. és 3. pontja (gomb, `sample`, `db`) ezzel elavult; a hatókör a 6. pont szerinti.
- **2026-11-08 — ⛔ 4. lépés: kész.** A próbanézetben (fenti URL, képességek nélkül újrapublikálva) a felhasználó a Kivonat·2 blokkra megjegyzéssel mutatott rá; a megjegyzés a blokk horgonyával (`#b-kivonat-2`) érkezett a sessionbe, a válasz a szálban ment. A felhasználó: „működik”. A megjegyzés mint rámutatási út a `lap-javit.md` 6.2-be került. A próbában forrásba nem írtunk (kiadott lap).
