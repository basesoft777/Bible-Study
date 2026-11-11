---
feladat: 196
cim: Harmadik tanú a BDB vers → jelentéspont hozzárendeléshez (Sefaria BDB)
kod: BDB_HARMADIK_TANU
tipus: feladat
fazis: folyamat
modell: claude-opus-5-5
allapot: fut
ad: a 2.29 jelentéspontjának harmadik, független tanúja (a Sefaria BDB-jelentésfája); egyezésnél `biztos`, eltérésnél `ketes`; kapcsolóval, alapból kikapcsolva
kovetkezo: "Folytatás: a független ellenőrzés és a draft PR; a merge a felhasználóé"
munka: adat
olvas: [CLAUDE.md, adat/SEMA.md, naplok/F185_jelentes.md, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/bdb_jelolt/belso_tanu.py, adat/licencek.tsv]
ir: [eszkozok/olvaso_szerver/bdb_sefaria_tanu.py, eszkozok/olvaso_szerver/teszt_bdb_sefaria_tanu.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, adat/bdb_vers_jelentes.tsv, adat/bdb_jp_sefaria.tsv, adat/SEMA.md, naplok/F196_jelentes.md, naplok/F196_seed103_reszlet.tsv, naplok/F196_proba40_reszlet.tsv, dontesek/uj/bdb-harmadik-tanu-618784.md, nyitott/uj/bdb-harmadik-tanu-618784.md]
fugg: [185]
nem_fugg: [182, 183, 193, 194, 195]
---

# F196_BDB_HARMADIK_TANU_BRIEF.md — Harmadik tanú a BDB jelentésponthoz

*FELADATOK #196 · Modell: claude-opus-5-5 · v1 · 2026.11.11*

*Az orkesztrátor indította, külön sessionben, ugyanezen az ágon; befogadás nélkül. A felhasználó jóváhagyása (2026-11-11), szó szerint.
A leírás: „A BDB harmadik tanú: … Egy kész, nyílt BDB-feldolgozás (BrownDriverBriggs.jl, Sefaria-alapú) harmadik tanúként jelezné, hol téved:
ahol egyezik, biztos; ahol eltér, kétes, és kézzel kell eldönteni. A felmérés szerint megéri, egy 40 soros próba után.” A válasz: „ezeket csináljuk”.*

## 1. Cél

A 2.29 (`adat/bdb_vers_jelentes.tsv`) jelentéspontja ma két forrásból jön: a szakasztábla dönt, a szeletelő tanú (`jp_tanu_elter`). A seed-103
vak mérés: 188/200 (biztos 180/181, ketes 8/19). Harmadik, független tanú: a Sefaria saját BDB-feldolgozásának jelentésfája.

## 2. Lépések

1. **Licenc és letöltés.** A nyers Sefaria-válaszok a repón kívül (`D:\pardes_tanu\bdb\`), a licenc idézetével (`LICENC.txt` ott). Ha nem szabad
   vagy kétes: megállás. *(A BrownDriverBriggs.jl csak burkoló a Sefaria API körül, GPL-3.0; nem használjuk, az API-t közvetlenül hívjuk.)*
2. **⛔ 40 soros téves-riasztási próba** (a felmérés szerint: a 19 `ketes` és 21 `biztos` seed-103 sor). Ha a tanú több zajt ad, mint hasznot:
   megállás, jelentés; a döntés a felhasználóé.
3. **Bekötés** (ha a próba jó): okkód `jp_tanu_sefaria`; egyezésnél `biztos`, eltérésnél `ketes`; **kapcsolóval, alapból KIKAPCSOLVA**
   (`SEFARIA_TANU = False`), hogy a HAMART-lap ne változzon a kiadás alatt. A bekapcsolás külön lépés.
4. **Újramérés** a seed-103 200 pontján: hány hibát fogott volna meg a 12-ből, hány új téves riasztást adott.

## 3. Határok

Nem nyúl: `lexikon/`, `eszkozok/lexikon_general.py`, `eszkozok/visszhang/`, `sablonok/`, a `DONTESEK.md` meglévő sorai. A lapot nem generálja újra.
A 2.29 sorai kikapcsolt tanúval bájtra azonosak maradnak (csak a fejléc kód-hash-e változik).

## 4. Gépi kapu (G)

- G1: `python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-11-10 --ellenoriz` → bájtra azonos (kikapcsolt tanúval).
- G2: a 2.29 adatsorai a base-hez képest változatlanok (csak a `# forras` fejlécsor tér el).
- G3: `python eszkozok/teszt_futtat.py --gyors` zöld, köztük a `teszt_bdb_sefaria_tanu.py` (a kapcsoló alapértéke `False`).
- G4: a repóba Sefaria-szöveg nem kerül (a 2.29.1 csak normalizált útvonalat tárol).

## 5. Döntések

DT-F196a (helyőrző): a dontesek/uj/bdb-harmadik-tanu-618784.md-ben.
