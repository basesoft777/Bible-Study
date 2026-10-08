---
feladat: 61
cim: A lekérdező maga naplózzon — automatikus auditok-sor a lekerdez.py-ból, és az adhoc lépésérték
kod: LEKERDEZ_NAPLO
tipus: feladat
fazis: 1
modell: sonnet
munka: folyamat
allapot: nem_indult
ad: a lekerdez.py minden alparancsa egy kapcsolóval (--naplo ID --lepes KÓD) maga fűzi a saját proveniencia-sorát az adat/auditok.tsv-hez, hozzáfűzéssel, duplikáció nélkül; a SEMA 2.9 lepes-értékkészlete bővül az adhoc értékkel, a proveniencia-sor a futtatás csatornáját is rögzíti (DT-M3)
kovetkezo: /kovetkezo; ⛔ az M0 után (a motívumon kívüli lekérdezések naplózásának helye)
olvas: [eszkozok/lekerdez.py, adat/auditok.tsv, adat/SEMA.md, eszkozok/ellenoriz.py, MUNKAMENET.md, eszkozok/teszt_lekerdez_sir.py]
ir: [eszkozok/lekerdez.py, eszkozok/teszt_lekerdez_naplo.py, adat/SEMA.md, eszkozok/ellenoriz.py]
fugg: []
nem_fugg: [55]
---

# F61_LEKERDEZ_NAPLO_BRIEF.md — A lekérdező maga naplózzon

*FELADATOK #61 · Modell: sonnet · v1 · 2026.10.05 · döntések: DT-M3 (`adhoc` + csatorna a proveniencia-sorban), DT-M7 (az MCP_BUROK feltételes; előbb ez a kisebb lépés)*

## 1. Cél

A CLAUDE.md 1. szabálya szerint minden lekérdezésből származó állítás mellé a lekérdezés saját proveniencia-sora kerül, és a SEMA 2.9 szerint minden kutatási lekérdezés sort kap az `adat/auditok.tsv`-ben, **0 találatnál is**. Ma a `lekerdez.py` kiírja a proveniencia-sort, de az `auditok.tsv`-be kézzel kell átvinni („a rögzítés a fő szál feladata”, SEMA 2.9). Ez a szabály gyenge pontja: a kézi lépés elmaradhat.

A feladat ezt gépesíti, MCP nélkül. A munkaterv MCP_BUROK feladata ezzel feltételessé vált (DT-M7).

## 2. Hatókör

**Benne van:**
- `--naplo ID` és `--lepes KÓD` kapcsoló a `lekerdez.py` minden alparancsához (`gerinc`, `scan`, `kollokacio`, `igealak`, `lxx-hid`, `tsk`, `karoli`, és ami még van);
- a SEMA 2.9 bővítése: `lepes` értékkészlet + `adhoc`; a proveniencia-sorban a `csatorna=cli` kulcs (DT-M3);
- az `ellenoriz.py` igazítása, ha az értékkészletet ellenőrzi;
- tesztek.

**Nincs benne:**
- MCP-szerver (DT-M7: feltételes);
- a meglévő `auditok.tsv`-sorok átírása: a tábla csak bővül;
- a `jelolt.py` és más eszközök naplózása (ha az M0 szerint kell, külön tétel).

## 3. Lépések

### M0 — Felmérés és ⛔

Jelentés: `naplok/LEKERDEZ_NAPLO_M0.md`.
1. A `lekerdez.py` alparancsai és a proveniencia-sor pontos alakja alparancsonként.
2. Az `auditok.tsv` érvényességi szabályai: az `ellenoriz.py` 1. szabálya (az `id` a `motivumok.tsv`-ben létező motívum) és a 8. szabály (dataset-lefedettség a `forras` kulcsból). A CI lépésfüggő szabályait (`eszkozok/ellenorzes/szabalyok.py`, pl. `TELJES_SCAN_LEPESEK`) a feladat nem írja; ha az `adhoc` érték miatt módosítás kellene, ⛔ és külön tétel.
3. **A nyitott kérdés:** az `auditok.tsv`-ben csak motívumhoz kötött sor állhat. Hová kerüljön a motívumon kívüli `adhoc` lekérdezés (felmérés, pilot)?

**⛔ Megállás, javaslattal:**
- **(a)** *javaslat:* motívumon kívüli lekérdezés nem kerül az `auditok.tsv`-be; a `--naplo` ilyenkor a feladat saját naplófájljába ír (`naplok/<KÓD>_lekerdezesek.tsv`, azonos oszlopokkal), így a motívumszintű 8. szabály tiszta marad;
- **(b)** *alternatíva:* az `auditok.tsv` `id` mezője feladatkódot is elfogadhat (SEMA- és `ellenoriz.py`-módosítással).

### M1 — Megvalósítás

- `--naplo ID`: az alparancs a kimenete végén, a proveniencia-sor kiírása után hozzáfűz egy sort: `id`, `lepes`, `proveniencia` (szó szerint, `csatorna=cli` kulccsal), `datum`.
- `--lepes KÓD`: kötelező, ha `--naplo` van; zárt értékkészlet (`A5`, `B2`, `B3`, `B4`, `adhoc`); érvénytelen értéknél hiba, nem ír.
- **Biztonság:** csak hozzáfűzés; a TSV-írás `'\t'.join()`, a `csv` modul tilos (CLAUDE.md); ugyanazt a sort (azonos `id` + `lepes` + `proveniencia`) nem veszi fel kétszer; írás előtt a fájl utolsó sora ellenőrizve (sorvég, oszlopszám).
- Kapcsoló nélkül a viselkedés **bájtra azonos** a maival (a `teszt_lekerdez_sir.py` rögzített számai változatlanok).
- SEMA 2.9: az `adhoc` érték és a `csatorna` kulcs leírása; az M0 (a)/(b) döntése szerinti szabály.

### M2 — Zárás

`eszkozok/teszt_lekerdez_naplo.py` (ideiglenes `auditok.tsv`-másolaton: hozzáfűzés, duplikáció-szűrés, érvénytelen `--lepes`, kapcsoló nélküli azonos kimenet), `naplok/LEKERDEZ_NAPLO_zaras.md` (≤20 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_LEKERDEZ_NAPLO.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Minden alparancs naplóz `--naplo` mellett; kapcsoló nélkül a kimenet bájtra azonos a maival.
- **K2.** A naplósor proveniencia-mezője a kiírt proveniencia-sorral szó szerint egyezik, `csatorna=cli` kulccsal.
- **K3.** Nincs duplikált sor, nincs `csv`-modul, meglévő sor nem változik.
- **K4.** Az `ellenoriz.py` és a CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A lépés mező a kutatási lépést jelöli; a lépésen kívüli lekérdezés `adhoc`; a csatorna a proveniencia-sorba kerül. | DT-M3 |
| v1 | 2026-10-05 | Az automatikus naplózás MCP nélkül, a `lekerdez.py`-ban; az MCP_BUROK feltételes. | DT-M7 |
| v1 | 2026-10-05 | `nem_fugg: [55]`: a #55 új auditok-sorai nem befolyásolják a naplózó kapcsolót; a kör (#54 ↔ #55 ↔ #61) feloldva. A CI-szabályfájlt a feladat csak olvasná, ezért nincs az `olvas`-ban (nem ad sorrendet a #30, #37, #40, #51 felé). | befogadás |
