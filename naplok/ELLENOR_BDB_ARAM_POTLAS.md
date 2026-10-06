# Független ellenőrzés: #66 BDB_ARAM_POTLAS

- Brief: `F66_BDB_ARAM_POTLAS_BRIEF.md`
- Tartomány: `origin/main..HEAD` = `bdae91d..30e0730`, ág: `claude/bdb-aram-potlas`, 8 commit (F66.0–F66.7)
- Az ellenőr (`fuggetlen-ellenor`) nem írhatott és nem commitolhatott; a jelentést az orkesztrátor mentette fájlba, tartalmilag változatlanul (tömörítve: az OK sorok összevonva).
- Eredmény: **ELTÉRÉS, 8 tétel** (alább; a javításuk állapota a „Kezelés” oszlopban).

## Eltérések súlyossági sorrendben

| # | Eltérés | Hely | Kezelés |
|---|---|---|---|
| 1 | A pótolt arámi szövegek többsége (6 mintából 5: H0007, H0069, H3606, H8450, BDB9285) már szerepel a fő táblában, a héber testvérsor végén; az N-F66b-féle hozzáfűzés duplikálna. Sehol nem dokumentált. A README „ütközés nincs” csak az alias-táblákra igaz. | `BDB_teljes_unabridged.tsv:6,56,237,3367,1688,7281`; `README:21,30`; `NYITOTT_FELADATOK.md:611` | dokumentálandó; az N-F66b-t a felhasználó dönti |
| 2 | A brief fejlécének 14. sora sérült (`kovetkezo:` idézőjele után sortörés nélkül az `olvas: [...]`); az `olvas` kétszer szerepel; az F66.7 nem javította. | `F66_BDB_ARAM_POTLAS_BRIEF.md:14-15` | javítandó |
| 3 | ⛔ M1 (a): a szúrópróba-kivonatban nincs ott a H0004, H0007, H3606 (a brief kötelezően előírja). A H0007 és H3606 sort a felhasználó a chatben külön megnézte; a H0004 a `cimke_reszleges` indokában szerepel. | `bdb_aram_potlas.py:338-339`; `BDB_ARAM_POTLAS_szurop.md` | a kivonatba felvenni a három sort |
| 4 | 3 sor `Teljes_szocikk` fejében benne maradt a betűfej (H3969, H8406, H5013): `H3969. mea מ מְאָה…`. A fő táblában ilyen nincs. | `tsv:90,168,102`; `bdb_aram_potlas.py:90` | javítandó (a teszt fej-regexe nem fogta meg) |
| 5 | README:30 a beemelésre N-F66a-ként hivatkozik (N51 kell); „csak egyertelmu” sorokat említ, miközben 170 elfogadott sor van. | `README:30` | javítandó |
| 6 | DT51: az opciók közt nincs a `kezi_elfogadott`; a felhasználói döntés nincs a szokásos lezárási alakban. | `DONTESEK.md:126` | javítandó |
| 7 | A `naplok/BDB_ARAM_POTLAS_szurop.md` új fájl, nincs az `ir:` listában. | `BRIEF:16` | felvenni |
| 8 | Docstring elavult: hiányzik a `kezi_elfogadott`, a `cimke_reszleges` példája H2298. | `bdb_aram_potlas.py:16-24` | javítandó |

## Rendben (saját lekérdezéssel igazolva)

- A `BDB_teljes_unabridged.tsv`, a `BDB_strong_alias.tsv`, a `BDB_strong_alias_elvetett.tsv` nulla-diff (`git diff --stat origin/main..HEAD`: üres); `BDB_strong_potlas.tsv`, `lexikonok_nyers/`, `adat/licencek.tsv` nem változott. SHA-256-ot az ellenőr nem számolt.
- 173 sor = az elvetett tábla `aram` sorai, azonos kulcsok és sorrend; 8 mező/sor; állapotok: `egyertelmu` 169, `kezi_elfogadott` 1 (H2298 → BDB9285), `csonk` 2 (H3769, H5013), `cimke_reszleges` 1 (H0004), `tobb_jelolt` 0, `nincs_szoveg` 0.
- Proveniencia: 173/173 sorban van; H2298 `manual`.
- TSV-olvasás: nincs `csv` modul a három szkriptben.
- A5/A6, A3–A4: nincs érintett találat (E12–E15: 0). `futtat.py` E2–E16, E19, E26: 0; E25 három találata a diffen kívül.
- Táblák Δ: `adat/*.tsv` Δ=0; `konkordancia/BDB_aram_potlas.tsv` új, +173.

## Nem ellenőrizhető az ellenőr szerepében

- Tesztfuttatás (K4), CI (a `pr: 227` zöld CI-t az orkesztrátor külön látta), a BDB.lexicon (SQLite) tartalmi egyezése (K2), a felhasználó chatbeli jóváhagyása.
