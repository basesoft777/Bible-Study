---
feladat: 65
cim: Károli-idézetek ellenőrzése a Károli–Strong párokon, variancia-térkép és a Károli-triplet frissítése
kod: KAROLI_ELLENORZES
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: nem_indult
ad: a tematikus táblák és a jelölt-/előfordulás-sorok Károli-szó + Strong párjai a #22 párosítása (adat/karoli_strong/parok_<könyv>.tsv) ellen ellenőrizve, eltéréslistával; a variancia-térkép (Strong → Károli-szóalakok, szóalak → Strongok) adattáblaként; a SEMA 1.7 a DT-M2 szerint bővítve, és a megerősített sorok azonosítási módja szó-szintű-gépi
kovetkezo: /kovetkezo; ⛔ az M0 után (a „magas” lefedettség és a frissítés szabálya) és az M3 ANTROP-001 mintája után; a #11 előtti befagyasztás nem érinti (adatréteg, DT-F52c (3))
olvas: [adat/karoli_strong/, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/SEMA.md, tematikus_lezart/, konkordancia/Karoli_Strong_kivonat.tsv, konkordancia/Karoli_1908.tsv, F22_KAROLI_STRONG_BRIEF.md, naplok/F22_Jozs_jelentes.md]
ir: [adat/SEMA.md, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/karoli_variancia.tsv, eszkozok/karoli_ellenorzes.py, eszkozok/teszt_karoli_ellenorzes.py]
fugg: [62, 63]
nem_fugg: [22]
---

# F65_KAROLI_ELLENORZES_BRIEF.md — Károli-idézetek ellenőrzése és a Károli-triplet frissítése

*FELADATOK #65 · Modell: sonnet · v1 · 2026.10.05 · forrás: `MUNKATERV.md` 4. szakasz (KAROLI_ELLENORZES, 2. hullám; FELADATTERKEP sorrend 5. lépés), `ADATVAGYON_TERV.md` 1.1–1.2 · döntés: DT-M2*

## 1. Cél

A régi join-sorok (`jeloltek.tsv`, `elofordulasok.tsv`: `karoli_szo`, `azonositas_modja`, `megbizhatosag`) mind `tartalom-alapú` azonosításúak: a tanulmány írója a Károli-szöveget olvasva rendelte a szót a Strong-számhoz. A #22 azóta szó-szintű, gépi Károli–Strong párosítást ad könyvenként. A feladat a régi párokat ez ellen ellenőrzi, a különbségeket listázza, és a megerősített sorok azonosítási módját frissíti.

**DT-M2 (🟢, 2026-10-05):** a SEMA 1.7 `AZONOSITAS_MODJA` zárt listája új értékkel bővül: `szó-szintű-gépi` — a #22 gépi párosításából, **csak `magas` bizonyosságú párból** tölthető; a `szó-szintű-tagged` egy esetleges kiadói, kézzel taggelt szövegnek marad. Az 1.7 elavult mondata („nincs és nem is lesz szó-szintű Strong-taggelt Károli”) javítandó. A meglévő `tartalom-alapú` sorok frissítése ennek a feladatnak a dolga, a #22 kész könyveire. *(A munkaterv sora még `szó-szintű-tagged`-et ír; a DT-M2 felülírja.)*

**Állapot a befogadáskor (2026-10-05, mérés):** a #22 hat könyve kész, de a `bizonyossag` megoszlása könyvenként eltér:

| könyv | `magas` (S+C) | `alacsony` (csak S) |
|---|---|---|
| 1Móz | 29 579 | 2 034 |
| 2Móz | 23 265 | 1 222 |
| 3Móz, 4Móz, 5Móz, Józs | 0 | mind (DT-F22c: csak Sonnet) |

A DT-M2 „csak `magas`” szabálya szerint tehát **ma csak az 1Móz és a 2Móz** sorai frissíthetők `szó-szintű-gépi`-re; a 3Móz–Józs párok az ellenőrzésben és a varianciában részt vehetnek, de a triplethez nem. A ma `tartalom-alapú` sorok száma: `jeloltek.tsv` 221, `elofordulasok.tsv` 205, `Karoli_Strong_kivonat.tsv` 383.

## 2. Hatókör

**Benne van:**
- SEMA 1.7: a `szó-szintű-gépi` érték és a javított mondat (DT-M2); SEMA-alfejezet az új `adat/karoli_variancia.tsv`-hez;
- **1.1 ellenőrzés:** a `jeloltek.tsv` és az `elofordulasok.tsv` minden `karoli_szo` + `strong` sora (és a tematikus táblák Károli-idézet + Strong párjai, ha az M0 szerint gépileg kinyerhetők) a `parok_<könyv>.tsv` ellen, igehelyenként; eltéréslista `naplok/KAROLI_ELLENORZES_elteresek.tsv`;
- **1.2 variancia-térkép:** `adat/karoli_variancia.tsv` (Strong → Károli-szóalakok darabszámmal; szóalak → Strongok), könyvenként, a `bizonyossag` jelölésével, proveniencia-sorral;
- **triplet-frissítés:** az 1.1-ben megerősített sorokon (`magas` pár, ugyanaz a szó és Strong ugyanazon a versen) `azonositas_modja` → `szó-szintű-gépi`; a `karoli_szo` és a `megbizhatosag` frissítésének szabályát az M0 javasolja;
- `eszkozok/karoli_ellenorzes.py` + teszt.

**Nincs benne:**
- az eltérések tartalmi feloldása: ha a régi pár és a gépi pár eltér, a sor nem változik, hanem az eltéréslistába kerül (a feloldás értelmező döntés, külön tétel);
- tanulmány- vagy motívumfájl javítása (`tematikus_lezart/`, `motivumok/`) és generált kimenet írása (`lexikon/`; a DT28 szerint nem motívumfájl, de kézzel nem írható): csak jelentés;
- a `konkordancia/Karoli_Strong_kivonat.tsv` írása (az M0 jelzi, hogy generált nézet-e, és ki frissíti);
- a #22 párosításának javítása vagy újrafuttatása (a #22 dolga); `alacsony` párból triplet-frissítés.

## 3. Lépések

### M0 — Felmérés és ⛔

Jelentés: `naplok/KAROLI_ELLENORZES_M0.md`.
1. A `parok_<könyv>.tsv` szerkezete (oszlopok, `hu_szo` alak, `strong` alak, többszavas és `+` láncú párok), és a `bizonyossag` megoszlása könyvenként (a 1. szakasz táblájának újramérése).
2. A `jeloltek.tsv` / `elofordulasok.tsv` `tartalom-alapú` sorai könyvenként: hány esik a hat kész könyvre, ebből hány 1Móz/2Móz (a `magas` lefedettség).
3. Az illesztés szabálya: hogyan felel meg a `karoli_szo` (lehet szókapcsolat, ragozott alak) a `hu_szo`-nak; az igehely-formátum (a `parok` `1Móz 1:1` alakú, a `Karoli_Strong_kivonat` STEPBible-alakú: `Konyv_normalizalo_tabla.tsv`, CLAUDE.md).
4. A tematikus táblák Károli-idézetei gépileg kinyerhetők-e (melyik szakasz, milyen alak); ha nem, az 1.1 a táblákra csak a `jeloltek`/`elofordulasok` sorain át fut.
5. Javaslat a `karoli_szo` és a `megbizhatosag` kezelésére megerősített soron (marad / a gépi alakra vált / csak az `azonositas_modja` vált).

**⛔ Megállás:** a felhasználó elfogadja az illesztés szabályát, a frissítés szabályát (5.), és tudomásul veszi a „magas” lefedettséget (a 3Móz–Józs ma nem frissül).

### M1 — SEMA és variancia-térkép

- SEMA 1.7 a DT-M2 szerint; az új tábla SEMA-alfejezete.
- `adat/karoli_variancia.tsv` a hat könyvből, a `bizonyossag` oszloppal; TSV-írás `'\t'.join()`, a `csv` modul tilos (CLAUDE.md).
- Commit: `F65.<n>: …`.

### M2 — Ellenőrzés és eltéréslista

- Minden `tartalom-alapú` sor a hat könyvön: `egyezik` / `elter` / `nincs_par` (a gépi párosításban nincs megfelelő), indoklás nélküli ítélet nincs; a 0 találat is a jelentésbe kerül.

### M3 — ANTROP-001 minta és ⛔

- A munkaterv kis mintája: ANTROP-001 eltéréslistája és legalább 3 triplet-sor (frissítendő) átnézésre. Ha az ANTROP-001-nek nincs 1Móz/2Móz sora, az M0 másik motívumot javasol.

**⛔ Megállás:** a felhasználó átnézi a mintát; utána indul a teljes frissítés.

### M4 — Triplet-frissítés

- Csak az M2 `egyezik` + `magas` sorain; meglévő más mező nem változik. Írás előtt soronkénti összevetés az eredetivel, eltérésnél megáll (minta: `eszkozok/igazolas_migracio.py`).
- Commit motívumonként vagy könyvenként.

### M5 — Zárás

`naplok/KAROLI_ELLENORZES_zaras.md` (≤20 sor: egyezik / elter / nincs_par számok, frissített sorok), `fuggetlen-ellenor` (`naplok/ELLENOR_KAROLI_ELLENORZES.md`, szúrópróba 10 frissített és 10 eltérő soron), a brief fejléce `lezarva`, push, draft PR. Javaslat: a #22 következő könyvei után a feladat újrafuttatható (könyvenként).

## 4. Elfogadási feltételek

- **K1.** SEMA 1.7 a DT-M2 szerint; az új tábla dokumentált.
- **K2.** `szó-szintű-gépi` csak `magas` páron és `egyezik` ítéletű soron áll.
- **K3.** Eltérő sor nem változott; minden eltérés a listában, igehellyel és mindkét párral.
- **K4.** Tanulmány-, motívum- és lexikonfájl változatlan; az `ellenoriz.py` és a CI zöld.
- **K5.** A független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | Az új érték `szó-szintű-gépi` (nem `szó-szintű-tagged`), csak `magas` párból. | DT-M2 |
| v1 | 2026-10-05 | A befogadáskori mérés szerint `magas` pár csak az 1Móz és a 2Móz könyvben van; a 3Móz–Józs triplet-frissítése a kétmodelles párosításig vár. | befogadás, mérés 2026-10-05, DT-F22c |
