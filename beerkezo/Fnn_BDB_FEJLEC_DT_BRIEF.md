---
feladat:
cim: A bdb_szakaszok.tsv és a bdb_forras_javitas.tsv fejléc-literáljai a végleges DT-számokra; a két bukó teszt_bont Determinizmus-teszt javítása
kod: BDB_FEJLEC_DT
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: nem_indult
ad: a bont.py és a forras_javit.py fejléc-literálja a végleges DT225 / DT228 számot írja, a három érintett BDB-tábla újragenerálva (csak a fejlécsorok változnak), a teszt_bont.py Determinizmus.test_ellenoriz és test_javitas_ellenoriz zöld
kovetkezo: Te: /befogad — a #128 (F128) merge-e után
olvas: [eszkozok/bdb_jelolt/bont.py, eszkozok/bdb_jelolt/forras_javit.py, eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/bdb_jelolt/teszt_bont.py, eszkozok/szamkiosztas.py, adat/SEMA.md, naplok/ELLENOR_F128.md, F119_BDB_HEADER_DT_BRIEF.md]
ir: [eszkozok/bdb_jelolt/bont.py, eszkozok/bdb_jelolt/forras_javit.py, adat/bdb_szakaszok.tsv, adat/bdb_forras_javitas.tsv, adat/bdb_szakasz_hu.tsv]
fugg: [128]
---

# Fnn_BDB_FEJLEC_DT_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

Eredet: az F128 javítókörének 1. tétele (`naplok/ELLENOR_F128.md` 1.), az F128.20–21 futásakor talált, **hatókörön kívüli** lelet: a két
bukó teszt fájljai nincsenek az F128 `ir` mezőjében, és a hiba nem az F128-ból ered (a main-en is fennáll). Rokon, lezárt eset: #119
(`F119_BDB_HEADER_DT_BRIEF.md`, a `bdb_vers_jelentes.py` fejléc-literáljai). Az ismétlődés megelőzése (a `szamkiosztas` és a `.py`
kimeneti literálok) a `beerkezo/Fnn_LEXIKON_UJRAGEN_BRIEF.md` tervezet tárgya; ez a tervezet csak a két BDB-generátort javítja.

## Háttér — a pontos ok (mérve 2026-10-21, az F128 ágán, írás nélkül; a main-nel azonos fájlokon)

A `python eszkozok/bdb_jelolt/teszt_bont.py` két tesztje bukik:

| teszt | tábla | eltérő sor | a táblában | a generátor kimenetében |
|---|---|---|---|---|
| `Determinizmus.test_ellenoriz` (`bont.py --ellenoriz`) | `adat/bdb_szakaszok.tsv` (36 625 sor) | csak a 2. (`# forras`) | `… section/remarks; DT225) + kód@c13da6a31b2a` | `… section/remarks; DT-F107a) + kód@c13da6a31b2a` |
| `Determinizmus.test_javitas_ellenoriz` (`forras_javit.py --ellenoriz`) | `adat/bdb_forras_javitas.tsv` (7 206 sor) | az 1. (`# GENERÁLT`) és a 2. (`# forras`) | 1.: `(F107, DT228 (a); …`; 2.: `adat/bdb_szakaszok.tsv@495d1c81cfc0` | 1.: `(F107, DT-F107f (a); …`; 2.: `adat/bdb_szakaszok.tsv@66bd24b9abb6` |

Adatsor egyik táblában sem tér el.

1. **DT-szám:** a `szamkiosztas` Action (`3fbb927a`, 2026-10-19: `DT-F107a → DT225`, `DT-F107f → DT228`) a két generált tábla
   fejlécét átszámozta, a generátorok kimeneti string-literáljait nem: `eszkozok/bdb_jelolt/bont.py:618` (`DT-F107a`) és
   `eszkozok/bdb_jelolt/forras_javit.py:319` (`DT-F107f (a)`). A változatlan generátor a helyőrzőt írná vissza.
2. **Elavult bemenet-hash:** a `bdb_forras_javitas.tsv` 2. sora a `bdb_szakaszok.tsv` egy korábbi állapotára mutat (`495d1c81cfc0`;
   a szakasztábla azóta az F107.29-ben és a `3fbb927a`-ban változott, ma `66bd24b9abb6`). A javítótábla adatsorai a mai szakasztáblából
   generálva is azonosak.

## Lépések (terv)

1. **Felmérés újra** a befogadáskor, a main aktuális állapotán: a két `--ellenoriz` futtatása és soronkénti összevetés (írás nélkül:
   `general` + `fajl_szoveg`, `split('\n')`, csv modul nélkül). Ha a fejlécsorokon kívül bármi eltér, megállni, és a tartalmi okot
   döntésre vinni.
2. A két kimeneti literál a végleges számra: `bont.py:618` `DT-F107a` → `DT225`; `forras_javit.py:319` `DT-F107f (a)` → `DT228 (a)`.
   Megjegyzés és docstring nem kötelező (nem kerül kimenetbe); ha átírja, külön tételben.
3. **Újragenerálás láncban, ebben a sorrendben** (`--ts 2026-10-18`, a táblák meglévő értéke), mert a hash-ek egymásra épülnek:
   - `python eszkozok/bdb_jelolt/bont.py --ts 2026-10-18` → `adat/bdb_szakaszok.tsv`: várhatóan csak a 2. sor változik (`DT225` marad,
     a `kód@` a javított `bont.py`-é lesz) — ezzel a tábla saját hash-e is megváltozik;
   - `python eszkozok/bdb_jelolt/forras_javit.py --ts 2026-10-18` → `adat/bdb_forras_javitas.tsv`: csak az 1–2. sor (`DT228 (a)`,
     az új `bdb_szakaszok.tsv@`, az új `kód@`);
   - `python eszkozok/bdb_jelolt/hu_illeszt.py --ts 2026-10-18` → `adat/bdb_szakasz_hu.tsv`: csak a 2. sor (az új `bdb_szakaszok.tsv@`).
     Ez az F128-ban sorvég-független lett (F128.21), ezért a `#128` merge-e után fusson (`fugg: [128]`).
   Minden lépés után soronkénti összevetés a régi táblával (a régi tábla mentve a repón kívül); ha a megengedett fejlécsoron kívül
   bármi változik, megállni, a táblát visszaállítani (`git checkout -- <tábla>`), és jelenteni. Az `adat/forditasok.tsv` nem íródik
   (sha256 előtte/utána).
4. **Elfogadási feltétel:** `python eszkozok/bdb_jelolt/teszt_bont.py` teljesen zöld (a `Determinizmus` két tesztje és a
   `HuIlleszt.test_ellenoriz` is); a három `--ellenoriz` „azonos”; más teszt eredménye nem változik.
5. Más, a `bdb_szakaszok.tsv` hash-ére hivatkozó generált fájl a mérés idején nem volt (`git grep "bdb_szakaszok.tsv@"`: a fenti két
   tábla, a két generátor és az F128 naplója); a befogadáskor újra ellenőrizni.

Tiltás: a generált táblát kézzel szerkeszteni tilos (CLAUDE.md, kimenet-réteg); a fejlécsort a generátor írja.
