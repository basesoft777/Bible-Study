---
feladat: 80
cim: A Károli-támasz nélkül fordított BDB-szócikkek adatblokkjának pótlása a teljes Károli–Strong után (újrafordítás nélkül)
kod: BDB_KAROLI_POTLAS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: megallt
ag: claude/f80-karoli-potlas
ad: a kész (teljes) BDB-fordítású szócikkek Károli-alakjai és példaversei a teljes ÓSZ Károli–Strong párosításból pótolva adatként; a fordítás szövege nem változik
kovetkezo: "Te: a tárolás helyének döntése (DT-F80a: (a) mező vagy (b) külön tábla; példák hivatkozásként vagy szövegesen; A+C vagy mind a 674 szócikk); utána M1"
olvas: [adat/karoli_strong/, adat/forditasok.tsv, adat/SEMA.md, eszkozok/bdb_adatblokk.py, naplok/BDB_FORDITAS_sorrend.tsv, naplok/BDB_FORDITAS_naplo.md, F38_BDB_FORDITAS_BRIEF.md, F56_BDB_ADATBLOKK_BRIEF.md]
ir: [adat/forditasok.tsv, adat/SEMA.md, eszkozok/bdb_adatblokk.py, eszkozok/teszt_bdb_adatblokk.py]
fugg: []
---

# F80_BDB_KAROLI_POTLAS_BRIEF.md — a BDB-szócikkek Károli-adatának pótlása

*FELADATOK #80 · Modell: sonnet · v1 · 2026.10.12 · a csonk-briefet váltja fel · döntés: DT77 (15), DT54, DT56 · forrás: `ADATVAGYON_TERV.md` 19. és 21. (1. lépcső), `F56_BDB_ADATBLOKK_BRIEF.md`, `F38_BDB_FORDITAS_BRIEF.md`*

## 1. Cél

A #38 BDB-fordításának adagjai a Károli–Strong párosítás hiányos állapotában készültek: a
fordítót tápláló adatblokk Károli-szakasza csak a #22 akkor kész könyveiből élt (1–5Móz, Józs),
a többi szócikknél `[NINCS KÁROLI-ALAK]` állt (DT54: a hátralévő sor 59,5%-ánál, a 7. adagban
13,7%-ánál). A DT56 az utólagos újrafordítást elvetette, a DT77 (15) pedig ezt a feladatot
vette fel: **az adat pótlódik, a fordítás szövege nem változik.**

Az ószövetségi párosítás ma teljes: az `adat/karoli_strong/` alatt mind a 39 ÓSZ-könyv
`parok_*.tsv` fájlja megvan. A feladat **nem vár a #22 hátralévő részére** (az ÚSZ-csomagokra,
köztük a 22.9-re): a BDB héber–arám szótár, ezért a szócikkek Károli-alakjai és példaversei
kizárólag ószövetségi helyekről jönnek. Ezt az M0 lefedettség-ellenőrzéssel igazolja
(39/39 könyv); ha az ellenőrzés mást mutat, ⛔.

A feladat eredménye: minden kész szócikkhez adatként elérhető a mostani adatblokk Károli-szakasza
(Károli-szóalakok előfordulás-számmal és bizonyossággal, példaversek), proveniencia-sorral.

## 2. Hatókör

**Benne van:**
- az `adat/forditasok.tsv` `BDB` szótárának kész (`teljes`) szócikkei;
- a mostani blokk és a fordításkori állapot eltérésének mérése (melyik szócikk kap új adatot);
- a pótolt adat tárolása a jóváhagyott helyen; ha külön tábla kell, SEMA-bővítéssel;
- tesztek.

**Nincs benne:**
- újrafordítás, a `forditas_hu` mező módosítása, a fordító prompt vagy a terminológia változtatása;
- a #38 adagjainak írása (a #38 és a #80 `adat/forditasok.tsv`-n kizárja egymást, a #38 megy előre);
- ÚSZ-adat (a BDB-hez nem tartozik).

## 3. Lépések (⛔ a kötelező megállások)

### M0 — Felmérés (csak olvas)

Jelentés: `naplok/BDB_KAROLI_POTLAS_M0.md`.
1. **Lefedettség:** a 39 ÓSZ-könyv `parok_*.tsv` fájljának megléte és sorszáma; a Strong-normalizálás (`H2617` / `H02617` / `2617`) egységes, normalizálás nélkül néma nem-találat lesz (CLAUDE.md).
2. **Érintett szócikkek:** a `forditasok.tsv` kész BDB-szócikkeiből hánynak ad a mostani `bdb_adatblokk.py` Károli-alakot, és hánynál volt a fordításkor `[NINCS KÁROLI-ALAK]` (a #38 naplója és a git-történet alapján). Ha a fordításkori állapot nem rekonstruálható, ezt a jelentés kimondja, és a teljes kész halmazt tekinti érintettnek.
3. **Tárolási lehetőségek:** (a) új mező az `adat/forditasok.tsv`-ben, (b) külön tábla az `adat/`-ban. Mindegyikhez a SEMA-hatás, a méret és az `emeles.py` / #38 írásával való ütközés.
4. **⛔ A tárolás helye** a felhasználó döntése.

### M1 — A pótlás

- A kész szócikkekre a `bdb_adatblokk.py` Károli-szakasza adatként a jóváhagyott helyre, szócikkenként proveniencia-sorral. Üres forrásnál kifejezett jelzés áll, nem kitöltés (CLAUDE.md 3. szabály).
- Táblaírás előtt és után a sorok összevetése (CLAUDE.md, TSV-olvasás: `split('\t')`, `'\t'.join()`, a `csv` modul tilos); a `forditas_hu` és minden más meglévő mező bájtra változatlan. Eltérésnél állj meg.
- SEMA-bővítés, ha új mező vagy tábla jön.

### M2 — Ellenőrzés

- Legalább 3 ismert Strong-számon (amelynek van Károli-párja) a kimenet visszakereshető forrássorra.
- Tesztek: `teszt_bdb_adatblokk.py` zöld, új teszt a változatlansági állításra.

### M3 — Zárás

- `naplok/BDB_KAROLI_POTLAS_zaras.md` (≤20 sor), a `fuggetlen-ellenor` jelentése (`naplok/ELLENOR_BDB_KAROLI_POTLAS.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** A 39 ÓSZ-könyv párosítása az M0-ban igazolt; a Strong-normalizálás egységes.
- **K2.** Minden kész szócikknek megvan a Károli-szakasza vagy a kifejezett üres jelzés, proveniencia-sorral.
- **K3.** Az `adat/forditasok.tsv` `forditas_hu` mezője és minden meglévő sor változatlan (bájtra egyező), kivéve az újonnan hozzáadott mezőt.
- **K4.** A SEMA a tárolás helyét leírja; a tesztek zöldek; a CI zöld.
- **K5.** A független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-12 | Csonk kitöltése; `fugg` üres: a BDB ószövetségi szótár, az ÓSZ-párosítás teljes, a #22 ÚSZ-csomagjai nem érintik. | a felhasználó jóváhagyása a chatben (2026-10-12) |
