ELTÉRÉS: 1 tétel

# Független újraellenőrzés: F38_BDB_FORDITAS_BRIEF.md, 12. adag, javítókör 1/2, PR #551

*A `fuggetlen-ellenor` jelentése, az orkesztrátor által változtatás nélkül (összefoglaló formában) mentve; az ellenőrnek nem volt fájlíró eszköze.*

- **Tartomány:** `bf69bcf1..87deb621` (6 commit, F38.444–F38.449)
- **Előző jelentés:** `naplok/ELLENOR_F38_adag12.md` (ELTÉRÉS: 4 tétel)

| pont | eredmény | indok |
|---|---|---|
| 0 modell | OK | ellenőr `claude-opus-5-5` = kért `opus`; a menet sorai `claude-sonnet-5-5`. |
| ELTÉRÉS 1 (D10 (5)) | OK | `forditasok.tsv:20206, 23019, 23650, 21374`: `AV morning`, `AV gather blackness`, `AV RV ivory`, `AV RV Da tumult`, szó szerint a forrás szerint; más magyarra fordított glossza nincs. |
| ELTÉRÉS 2 (H7688) | OK | `abszolút használatban: participium` (`terminologia.tsv:67`); a megjegyzés változatlan. |
| ELTÉRÉS 3 (brief `ir`) | OK | az `ir` végére felkerült a `naplok/BDB_FORDITAS_adag12_bontas.md`. |
| ELTÉRÉS 4a (DT-F38k tartalom) | OK | `DONTESEK.md:504`, 8 oszlop, ✅, `a)`, forrás: orkesztrátor, a felhasználó megbízásából, 2026-11-01. |
| **ELTÉRÉS 4b (helyőrző ütközés)** | **ELTÉRÉS** | A `DT-F38k` helyőrzőt a számkiosztás már kétszer végleges számra cserélte (DT57: `7419c7dc`; DT323: `44debc74`). Merge után a `szamkiosztas.py` a definíciós sor helyőrzőjét a repó minden `.md`/`.tsv` fájljában átírná, így 5 régi ellenőri jelentés (`ELLENOR_F141_3.md:23` ×2, `ELLENOR_F38_adag7_2.md:37`, `ELLENOR_F38_nf107b.md:21`, `ELLENOR_F38_nf107b_2.md:20`, `ELLENOR_F67_2.md:27`) 6 hivatkozása csendben hamisulna. Javítás: nem kiosztott betű (pl. `DT-F38o`-hoz hasonló) a `DONTESEK.md:504`-be és a bontási napló 92. sorába, vagy az érintett jelentések `DT-F38k`-ja előbb `DT323`-ra. |
| ELTÉRÉS 4c (helyesbítés a bontási naplóban) | OK | a hat szó (`reszleges`, `gyakorisagi`, `felulbiralas`, `lasd`, `naplo`, `lezarva`) egyezik a `2c4b5fe3` üzenetével. |
| 5671. sor | OK | `5671 H8546 … 13`; az 5670-ig tartó adag 1690 Strong; a Károli-mérő az adagot a küszöböt átlépő sorral zárja. |
| Darabszámok / más adatváltozás | OK | 4996 sor, 1690 Strong; `forditasok.tsv` 5+/5−, más `adat/`/`konkordancia/` tábla nem változott. |
| `EMELES_munka.tsv` 11/11 | OK (megjegyzés) | 5 tartalmi változás, 6 sor tartalom nélkül mozdult el (az újrarögzítés mellékterméke). |
| CI ↔ saját futás | NEM ELLENŐRIZHETŐ | saját futtat.py: HIBA nincs, E2–E32 0 a diff fájljaira (E25: 4, E27: 40 JELENTÉS nem a diff fájljai). |
| Lista 1–5 | OK | törölt adatsor 0; kulcstartomány lefedett; nulla-diff hatóköre pontos; tábla-Δ 0; ⛔ pont nem érintett. |

**Az ELTÉRÉS:** a `DT-F38k` helyőrző ütközik a már kiosztott számokkal (4b).

Verdikt: ELTÉRÉS
