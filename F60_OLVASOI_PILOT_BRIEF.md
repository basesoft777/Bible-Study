---
feladat: 60
cim: Olvasói pilot — a konkordancia-nézet mérhető próbája két szakaszon, csak adatból, jelölt jelleggel
kod: OLVASOI_PILOT
tipus: feladat
fazis: folyamat
modell: sonnet
munka: adat
allapot: fut
ag: claude/olvasoi-pilot
ad: a repóban futó olvasói pilot (eszkozok/olvaso_pilot/) két szakaszon (1Móz 1:1–2:3 és Zsolt 22), minden blokk jellegjelöléssel (forrásadat / gépi feldolgozás / modell-kimenet), és egy értékelő jelentés számokkal, amely a DT-M1 döntés (olvasói konkordancia előre) alapja
kovetkezo: /kovetkezo; ⛔ az M3 felhasználói átnézésnél
olvas: [eszkozok/olvaso_pilot/README.md, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, "konkordancia/Macula_heber_*.tsv", "konkordancia/LXX_OS/*.tsv", konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/Karoli_kereszthivatkozasok.tsv, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/Strong_szotar.tsv, konkordancia/TBESG.txt, konkordancia/Thayer_teljes.tsv, konkordancia/UBS_DBH_referenciak.tsv, konkordancia/UBS_DBH_jelentesek.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, "adat/karoli_strong/*.tsv", adat/forditasok.tsv, adat/kulso/lxx_bridge.tsv, adat/licencek.tsv, MUNKATERV.md, ADATVAGYON_TERV.md]
ir: [eszkozok/olvaso_pilot/adat.py, eszkozok/olvaso_pilot/bdb_szelet.py, eszkozok/olvaso_pilot/epit.py, eszkozok/olvaso_pilot/sablon.html, eszkozok/olvaso_pilot/README.md, eszkozok/olvaso_pilot/teszt_olvaso_pilot.py]
fugg: []
nem_fugg: [7, 9, 22, 38, 52, 54, 56, 57]
---

# F60_OLVASOI_PILOT_BRIEF.md — Olvasói pilot

*FELADATOK #60 · Modell: sonnet · v1 · 2026.10.05 · kiinduló állapot: `eszkozok/olvaso_pilot/` (a 2026-10-05-i prototípus, README-vel) · döntés-előkészítés: DT-M1*

## 1. Cél

A munkaterv DT-M1 döntése azt kérdezi, kiadható-e az olvasói konkordancia (vers- és szó-lap, motívum nélkül) a migráció (#11, #23) előtt. A döntéshez mérés kell arról, mit tud a repó adata egy valós olvasási helyzetben. A 2026-10-05-i prototípus (1Móz 1:1–2:3) ezt megmutatta egy szakaszon. A feladat ezt **reprodukálható, mérhető pilottá** teszi.

**Alapszabály (felhasználói döntés, 2026-10-05):** a pilot csak adatból dolgozik. Ami nem változatlan forrásadat, az jelölve van: **gépi feldolgozás** (determinisztikus szabály) vagy **modell-kimenet** (nyelvi modell fordítása vagy párosítása). Magyarázó szöveg nem kerülhet a lapra; az a #59 jóváhagyott szószedetén át jöhet később.

## 2. Hatókör

**Benne van:**
- a prototípus paraméterezése szakaszra (`--szakasz`), és egy második szakasz, a **Zsoltárok 22** (költői szöveg, feliratos zsoltár versszámozással, a Károli–Strong párosításon kívüli könyv);
- a jellegjelölés teljessége és ellenőrzése (M1);
- mérőszámok és értékelő jelentés (M2, M4);
- tesztek.

**Nincs benne:**
- nyilvános közzététel, tárhely, kereskedelmi licenc (DT-M6, a 4. hullám);
- motívumréteg (#25b);
- új adat előállítása: a hiányokat a pilot méri és jelzi, nem pótolja (a pótlás a #54, #57, #58, #59 dolga).

## 3. Lépések

### M0 — Átvétel és paraméterezés

- Az `adat.py` kapjon `--szakasz` paramétert (pl. `"1Móz 1:1-2:3"`, `"Zsolt 22"`). A versek listája a `Karoli_1908.tsv`-ből jön, a könyvfájlok (Macula, LXX_OS) a `Konyv_normalizalo_tabla.tsv` és a meglévő névkonvenciók szerint.
- Az 1Móz 1:1–2:3 kimenete legyen azonos a prototípuséval (bájtra azonos JSON, a `ts` mező kivételével). Ez a regressziós alap.

### M1 — Jellegjelölés és „csak adat” ellenőrzés

- Minden blokk jelleg-címkéje a README táblázata szerint. A Károli–Strong párosításon alapuló aláhúzás modell-kimenet.
- **Ellenőrző lista** a jelentésben: a sablon minden szövege vagy (a) felületi utasítás (mire lehet kattintani), vagy (b) adatból jön. Ami egyik sem, az kikerül. A független ellenőr ezt külön ellenőrzi.
- `teszt_olvaso_pilot.py`: legalább a fő szó választása (1Móz 1:4 „világosságot” → H0216, „setétségtől” → H2822), a görög szóalak párosítása (1Móz 1:1 → ἀρχῇ), a BDB-bontás (H7225: 1. a., 1. b., 2.; H0216: 11 jelentés).

### M2 — Mérés

Mindkét szakaszra, proveniencia-sorral (`scope=… | forras=… | ts=…`):
- a Károli-szavak hány százaléka kötött héber szóhoz (magas / alacsony bizonyosság);
- a héber szó-lapok hány százalékának van magyar BDB-szócikke, angol szócikke, vagy egyik sem;
- a BDB-bontás: hány szócikk bomlik legalább 2 jelentésre, hány marad egyben (lista);
- a görög szó-lapok: magyar jelentés, újszövetségi előfordulás, héber háttér aránya;
- a görög szóalak forrása (LXX_OS / Macula) és a χ/ξ-eltérések száma;
- a UBS-jelentés lefedettsége, a versszámozási eltérések (Zsolt 22 felirat).

### M3 — ⛔ Felhasználói átnézés

A felhasználó megnézi mindkét szakasz oldalát. A közzétételt privát artifactként az orkesztrátor végzi; a végrehajtó a HTML-t a `--kimenet` könyvtárba írja, és a jelentésben megadja az útvonalát. A felhasználó jelzi, mi hiányzik, mi felesleges, és melyik mérőszám a döntő. Az észrevételek a jelentésbe kerülnek.

### M4 — Értékelő jelentés és zárás

- `naplok/OLVASOI_PILOT_ertekeles.md`: a mérőszámok, az M3 észrevételei, és a DT-M1 opcióinak (1 / 1b küszöbbel / 2) **adatalapú** összevetése. Javaslat lehet, döntés nem: a döntés a felhasználóé.
- `naplok/OLVASOI_PILOT_zaras.md` (≤20 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_OLVASOI_PILOT.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Az 1Móz 1:1–2:3 adata azonos a prototípuséval; a Zsolt 22 is lefut, hiba nélkül.
- **K2.** Minden blokk jelleg-címkét és adatforrás-jelzést kap; a lapon nincs adatforrás nélküli tartalmi szöveg.
- **K3.** A mérőszámok mindkét szakaszra proveniencia-sorral állnak a jelentésben.
- **K4.** A tesztek zöldek; a kimenet nem kerül a repóba (CLAUDE.md: `--kimenet` a repón kívül); a CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A pilot csak adatból dolgozik; ami értelmezés (gépi feldolgozás, modell-kimenet), az jelölve van. | felhasználó |
| v1 | 2026-10-05 | Kiinduló állapot a prototípus (`eszkozok/olvaso_pilot/`); második szakasz a Zsolt 22 (költői szöveg, feliratos zsoltár, párosításon kívüli könyv). | befogadás |
| v1 | 2026-10-05 | `fazis: folyamat`: döntés-előkészítő eszköz, nem az adat- vagy a render-fázis része; a #57, #58 lezárása után újrafuttatható. | befogadás |
| v1 | 2026-10-05 | `nem_fugg: [52]`: a tervdokumentum olvasása kontextus. | kontextus-olvasás |
| v1 | 2026-10-05 | `nem_fugg: [7, 9, 22, 38, 54, 56, 57]`: a pilot az aktuális adatállapotot méri, nem vár a táblákat író feladatokra; ezek lezárása után újrafuttatható (a jelentés rögzíti, melyik állapoton mért). | befogadás |
