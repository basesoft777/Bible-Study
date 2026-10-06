---
feladat: 56
cim: BDB-adatblokk — szócikkenként előre számolt Károli-, példavers- és LXX-adat a fordító promptba (közvetlen TSV-változat)
kod: BDB_ADATBLOKK
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: megallt
ag: claude/bdb-adatblokk
ad: a #38 minden adagjában a BDB-szócikk elé egy gépileg előállított adatblokk kerül (Károli-szóalakok gyakorisággal, legfeljebb 3 Károli-példavers szóalakonként, LXX-megfelelő, rokon szavak, meglévő magyar szócikk, a forrás fejezetszám-hibáinak javítása), minden sor proveniencia-jelöléssel; a fejezetszám-javítótábla elkészül, és visszamenőleg az 1–5. adag fordításain is átvezetve
kovetkezo: Te: az M3 mintablokk (naplok/BDB_ADATBLOKK_minta.md, 20 blokk) és a javítótábla első eredménye (adat/bdb_igehely_javitas.tsv: 21 javitva, 72 jelolt_marad; 12 javitva soron FIGYELEM-jelzés) jóváhagyása; utána /kovetkezo az M4–M6-ra
olvas: [konkordancia/BDB_teljes_unabridged.tsv, "adat/karoli_strong/*.tsv", konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, adat/kulso/lxx_bridge.tsv, konkordancia/Strong_szotar.tsv, adat/lexikon_hivatkozasok.tsv, adat/terminologia.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, naplok/BDB_FORDITAS_sorrend.tsv, naplok/BDB_FORDITAS_naplo.md, F38_BDB_FORDITAS_BRIEF.md, eszkozok/forditas_kapuk.py, ADATVAGYON_TERV.md]
ir: [eszkozok/bdb_adatblokk.py, eszkozok/teszt_bdb_adatblokk.py, eszkozok/emeles.py, eszkozok/teszt_emeles.py, forditas/prompt_v4.md, adat/bdb_igehely_javitas.tsv, adat/forditasok.tsv, adat/SEMA.md]
fugg: []
nem_fugg: [22, 38, 52]
---

# F56_BDB_ADATBLOKK_BRIEF.md — BDB-adatblokk (közvetlen TSV-változat)

*FELADATOK #56 · Modell: sonnet · v1 · 2026.10.05 · döntés: DT-F38i 🟢 (a) 2b és (c) · terv: `ADATVAGYON_TERV.md` 12.1, `MUNKATERV.md` BDB_ADATBLOKK (itt SQLite nélkül)*

## 1. Cél

A #38 (BDB_FORDITAS) fordító modellje ma csak a BDB angol szócikkét kapja, és a magyar megfelelőt a szótári jelentésből választja. Ez a feladat minden szócikk elé egy **előre, gépileg számolt adatblokkot** tesz a projekt saját adataiból. Így a szóválasztás Károli tényleges gyakorlatához igazodik, az adagok között egységes marad, és a forrás fejezetszám-hibái javítva kerülnek a fordításba.

A blokk **nem értelmez és nem egészít ki emlékezetből** (CLAUDE.md 3. szabály). Ha egy forrás nem ad adatot, a blokk ezt kifejezetten jelzi („—”, illetve `[NINCS KÁROLI-ALAK]`).

A DT-F38i (a) 2b szerint a feladat **adatbázis nélkül**, közvetlenül a TSV-kből dolgozik. A munkaterv SQLite-alapú változata (SQLITE_EPIT) később ugyanezt a kimenetet adhatja; ez a feladat nem vár rá.

## 2. Hatókör

**Benne van:**
- `eszkozok/bdb_adatblokk.py`: a blokk előállítása egy Strong-számra (M1);
- a fejezetszám-javítótábla, `adat/bdb_igehely_javitas.tsv`, és annak SEMA-leírása (M2, DT-F38i (c));
- a prompt bővítése (`forditas/prompt_v4.md` → v4.2, `{{ADATBLOKK}}` helyőrző) és a bekötés az `emeles.py` `prompt_epit` függvényébe (M4);
- a javítótábla visszamenőleges átvezetése az 1–5. adag fordításain (M5);
- tesztek.

**Nincs benne:**
- a 6. adag fordítása: az a #38 dolga, a #56 lezárása után;
- SQLite, MCP;
- a Károli–Strong párosítás bővítése (#22): a blokk azt használja, ami kész, és a lefedettséget jelzi;
- a BDB-gyökcsoportok (a #38 M0 5. pontja): ezek a #38 menetében mérődnek, nem kerülnek a blokkba;
- a BDB forrásfájl (`BDB_teljes_unabridged.tsv`) módosítása: a javítás csak a javítótáblában és a fordításban jelenik meg.

## 3. Lépések

### M0 — Felmérés (csak olvas)

Jelentés: `naplok/BDB_ADATBLOKK_M0.md`.
1. **Források és oszlopaik:** a `parok_<könyv>.tsv` (`vers`, `hu_szo`, `strong`, `bizonyossag`), a `Karoli_1908.tsv`, a `lxx_bridge.tsv`, a `Strong_szotar.tsv` (TWOT-csoport), a `lexikon_hivatkozasok.tsv`, a `TAHOT_kivonat.tsv`. A Strong-alakok normalizálása (`H2617` / `H02617` / `2617`) mindenhol egyezzen; normalizálás nélkül néma nem-találat lesz (CLAUDE.md).
2. **Lefedettség:** a Károli–Strong párok mely könyvekre készek (ma 1–5Móz, Józs), és a 6. adag első 50 szócikkéből (`BDB_FORDITAS_sorrend.tsv`, 407–456) hánynál ad a blokk legalább egy Károli-alakot.
3. **Fejezetszám-hibák:** a 13. kapu (`forditas_kapuk.ellenoriz_fejezetszam`) által az 1–5. adagban jelzett összes hely listája, a naplóból és újrafuttatásból.

### M1 — Az adatblokk előállítása

`python eszkozok/bdb_adatblokk.py H2617` → Markdown blokk, ebben a sorrendben:
1. **Károli-szóalakok:** magyar szóalak + előfordulás-szám, csökkenő sorrendben; külön a `magas` és az alacsonyabb bizonyosságú párok; mellette a **lefedettség** (mely könyvekből). Ha nincs pár: `[NINCS KÁROLI-ALAK]`.
2. **Példaversek:** szóalakonként legfeljebb 3 vers, igehely + Károli-szöveg, a szó kiemelve. A kiválasztás determinisztikus (pl. kanonikus sorrend, első három), és a szabály a blokkban áll.
3. **LXX-megfelelő:** a `lxx_bridge` görög Strong-számai előfordulásszámmal (legfeljebb 3), a görög lemmával a `Strong_szotar`-ból; ha nincs: „—”.
4. **Rokon szavak:** azonos TWOT-csoportba tartozó Strong-számok (legfeljebb 5), lemmával; ha nincs: „—”.
5. **Meglévő magyar szócikk:** ha a Strong-számhoz van sor a `lexikon_hivatkozasok.tsv`-ben, a magyar jelentés-összefoglaló; ha nincs: „—”.
6. **Javított forrás-hivatkozások:** a javítótábla (M2) e szócikkre vonatkozó sorai: „a forrásban `X` → helyesen `Y`”.

Minden szakasz végén proveniencia-sor (`scope=… | forras=… | ts=…`). A blokk egészének mérete korlátos (pl. legfeljebb 2 500 karakter); a levágás szabálya a blokkban jelölve.

A TSV-olvasás `split('\t')`, a `csv` modul tilos (CLAUDE.md).

### M2 — Fejezetszám-javítótábla (DT-F38i (c))

`adat/bdb_igehely_javitas.tsv`, új tábla, a SEMA-ba új szakasszal. Javasolt oszlopok: `strong`, `forras_hivatkozas`, `javitott_hivatkozas`, `allapot` (`javitva` / `jelolt_marad`), `indok`, `proveniencia`.

Az algoritmus minden olyan BDB-hivatkozásra, amelynek fejezetszáma az adott könyvben nem létezik:
1. a szócikk Strong-számának előfordulásai az adott könyvben (`TAHOT_kivonat.tsv`, kiegészítve a `parok_<könyv>.tsv`-vel; a TAHOT ismert hiányai miatt mindkettő);
2. azok a jelöltek, amelyek a hibás számból **egy számjegy elhagyásával, betoldásával vagy cseréjével** állnak elő (pl. `17:10` → `7:10`);
3. **pontosan egy jelölt** → `javitva`; nulla vagy több → `jelolt_marad`, a jelöltek felsorolásával. Találgatás nincs.

Az algoritmus és a küszöb a naplóba kerül. Az ismert példa (H7223, `Eccl 17:10` → `Eccl 7:10`) teszteset.

### M3 — Mintablokk és ⛔ elfogadási próba

Minta: 10 szócikk a H2617 körül (a `BDB_FORDITAS_sorrend.tsv` szerint) és a 6. adag első 10 szócikke (sorrend 407–416). Jelentés: `naplok/BDB_ADATBLOKK_minta.md`, a 20 blokkal.

Ellenőrzés: a blokk minden száma és idézete visszakereshető egy forrássorra (szúrópróba szócikkenként legalább 2 adaton, a parancs kimenetével).

**⛔ Megállás.** A felhasználó jóváhagyja:
- a blokk tartalmát és formáját;
- a javítótábla első eredményét (hány `javitva`, hány `jelolt_marad`).

### M4 — Bekötés a fordító promptba

- `forditas/prompt_v4.md` → v4.2: új `{{ADATBLOKK}}` helyőrző, és egy szabály a fordítónak:
  - a Károli-alakok **ajánlások**, nem kötelező kulcsok; a kötelező alakokat továbbra is a terminológia (`{{KOTELEZO_ALAKOK}}`) adja;
  - `[NINCS KÁROLI-ALAK]` esetén a szótári jelentésből választ;
  - a javított hivatkozást így írja: `Y [BDB: X]`.
- Az `emeles.py` `prompt_epit` függvénye kitölti a helyőrzőt. A meglévő adagok újrafuttatása nem cél; a `teszt_emeles.py` zöld marad.
- A prompt verziónaplója frissül.

### M5 — Visszamenőleges átvezetés az 1–5. adagon

- A `javitva` sorok átvezetése a már kész `adat/forditasok.tsv`-sorok fordításában, `Y [BDB: X]` formában. Más mező nem változik.
- Táblaírás előtt és után a sorok összevetése (CLAUDE.md, TSV): csak az érintett sorok érintett szövegrésze változhat; eltérésnél állj meg.
- A darabszám a végső mezőtartalomból számolva kerül a naplóba.

### M6 — Zárás

- `naplok/BDB_ADATBLOKK_zaras.md` (≤20 sor), a `fuggetlen-ellenor` jelentése (`naplok/ELLENOR_BDB_ADATBLOKK.md`), a brief fejléce `lezarva`, push, draft PR.
- A #38 a #56 lezárása után a 6. adaggal folytatódik (a #38 fejlécében `fugg: [34, 56]`).

## 4. Elfogadási feltételek

- **K1.** A blokk minden adata visszakereshető forrássorra, és minden szakasznak van proveniencia-sora; üres forrásnál kifejezett jelzés áll, nem kitöltés.
- **K2.** A Strong-normalizálás egységes; a mintában nincs néma nem-találat (ellenőrizve legalább 3 ismert Strong-számon, amelynek van Károli-párja).
- **K3.** A javítótáblában minden `javitva` sor egyetlen jelöltre épül, `indok`-kal és proveniencia-sorral; a H7223 tesztesete teljesül.
- **K4.** A prompt v4.2 és az `emeles.py` bekötése mellett a `teszt_emeles.py` és a `teszt_bdb_adatblokk.py` zöld.
- **K5.** Az M5 átvezetésben csak a `javitva` hivatkozások szövegrésze változott a `forditasok.tsv`-ben.
- **K6.** A felhasználó jóváhagyta az M3 mintát; a CI zöld; a független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A 6. adag a #56 után indul; a #56 SQLite nélkül, közvetlenül a TSV-kből dolgozik. | DT-F38i (a) 2b |
| v1 | 2026-10-05 | A fejezetszám-hibák javítótáblája ebbe a feladatba kerül, visszamenőleg az 1–5. adagra is; csak egyértelmű jelöltnél javít. | DT-F38i (c) |
| v1 | 2026-10-05 | A Károli-alakok a fordítónak ajánlások; kötelező alakot továbbra is csak a terminológia ad. | ADATVAGYON_TERV 12.1, prompt v4.1 |
| v1 | 2026-10-05 | A tervdokumentum olvasása nem ad függést a TERV_SZINKRON-tól (`nem_fugg: [52]`). | kontextus-olvasás |
| v1 | 2026-10-05 | `nem_fugg: [22, 38]`: a #56 szándékosan a részleges Károli–Strong adattal dolgozik (a lefedettséget jelzi), és a #38 előtt fut (a #38 vár a #56-ra, DT-F38i); a levezetett #38 ↔ #56 kör így feloldva. | DT-F38i, felhasználó |
