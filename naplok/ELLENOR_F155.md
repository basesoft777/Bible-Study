ELTÉRÉS: 3 tétel

# ELLENOR_F155 — független ellenőrzés (THAYER_ELAVULT_HIVATKOZAS, #155)

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`). A jelentést az ellenőr nem tudta fájlba írni (nincs fájlíró eszköze); az orkesztrátor rögzítette a visszaadott szöveg alapján, tartalmi változtatás nélkül, az 1. tételt saját grep-pel igazolva (`DONTESEK.md:532` `DT-F157d` ↔ `:534` `DT480`). Az eredeti első sor `ELTÉRÉS` volt.*

**Brief:** `F155_THAYER_ELAVULT_HIVATKOZAS_BRIEF.md` · **Tartomány:** `44f0a63f..c969a551` (base = `git merge-base origin/main HEAD`).

**Egyeztetett eltérés:** a `teszt_lanc.py` G1941-állítása 10 → 6 (DT476 / F152.14), a felhasználó kérésére (chat, 2026-11-02: „#155 és a teszt”). **Döntés:** DT488 — „(a) Csere DT329-re”.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | ellenőr `claude-opus-5-5` (kért: `opus`); végrehajtó `claude-sonnet-5-5`, a brief `modell: sonnet` — egyezik; a `forditasok.tsv` `modell` mezője nem változott |
| **DONTESEK ütközésfeloldás** | **ELTÉRÉS (súlyos)** | `DONTESEK.md:532` | `git diff 44f0a63f HEAD -- DONTESEK.md` két sort ad hozzá: `DT-F157d` és `DT488`. A `DT-F157d` a main-en már `DT480` (`89d4fa9e szamkiosztas`), ugyanazzal a tartalommal a `:534`-en. Az F155.3 merge visszahozta a kiosztott helyőrzőt; merge után a `szamkiosztas` duplikált döntést számozna. Javítás: a `:532` sor törlése. A CI (E1–E32) nem jelezte. |
| Brief 1. lépés (forditas.py) | OK | `eszkozok/thayer_jelolt/forditas.py:219` | egy sor: `DT-F132c` → `DT329` |
| Brief 1. lépés (teszt) | OK (statikusan) | `teszt_lanc.py:447-449` | `assertIn('…(2026.10.25; DT329)')`, `assertNotIn('DT-F132c')`; az ellenőr nem futtatta |
| Egyeztetett eltérés G1941 10→6 | OK | `teszt_lanc.py:73-74` | `adat/elofordulasok.tsv`: 6 különböző igehely; a 4 kivett helyet a `4dd8bba6 F152.14` vette ki (`git log -G`) |
| Brief 2. lépés ⛔ | OK | — | a `forditasok.tsv`-t csak az F155.4 érinti, a döntés után; a DT488 sorában a felhasználó szavai (`DONTESEK.md:533`) |
| Brief 3. lépés / tiltások | OK | `adat/forditasok.tsv:66,67,69-71,73,79` | 7 csere, mind `Thayer … teljes … elavult` (G1311, G2671, G5010, G5356, G0012, G5351, G0086); szöveg, állapot, `kezi` sor változatlan |
| Elfogadás: `grep -c DT-F132c` = 0 | OK | `adat/forditasok.tsv` | 0; az `elavult` Thayer-sorok száma 7 |
| Elfogadás: `ellenoriz.py`, `teszt_lanc.py` | NEM ELLENŐRIZHETŐ | `naplok/THAYER_ELAVULT_HIVATKOZAS_naplo.md:51` | a szerep nem engedi; a napló: 18/0/2/6, 40 teszt, 1 ismert N66 |
| Brief §5 Döntésnapló | ELTÉRÉS (enyhe) | `F155_…_BRIEF.md:58` | üres maradt; a DT488 és a G1941-eltérés csak a naplóban áll |
| `ir` hatókör | ELTÉRÉS (enyhe) | `naplok/THAYER_ELAVULT_HIVATKOZAS_csere.py` | a brief `ir` listáján kívüli új szkript; tartalmilag rendben (split/join, soronkénti összevetés, 7 soros őr) |
| Maradék helyőrzők (nem hatókör) | OK, megjegyzéssel | `forditas.py:2,19,20,211,216`; `szolista.py:13,95`; `teszt_lanc.py:437,457` | a brief csak a 219. sort írja elő; a CI E32 a 211/216-ot JELENTÉS-ként jelzi |
| A1 | OK | napló:7,22,49 | proveniencia-sorok megvannak |
| A2 | OK | — | `NYITOTT_FELADATOK.md` nincs a diffben |
| A3–A5 | OK (nem érintett) | — | nincs tanulmány, párhuzam, tanító |
| A6 | OK | — | `futtat.py`: E12–E15 0 |
| CI | NEM ELLENŐRIZHETŐ | — | saját `futtat.py --valtozott …`: E2–E20 0; E25 4, E27 40, E32 2 JELENTÉS; SÉRTÉS nincs |
| Lista 1–5 | OK | — | `forditasok.tsv` 7 módosított, 0 törölt/új; lefedettség 7/7; nulla-diff csak a `forditasok.tsv`-re; E17 Δ 0; ⛔ betartva |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. `DONTESEK.md:532`: a merge visszahozta a már `DT480`-ként kiosztott `DT-F157d` duplikátumot — merge előtt törlendő.
2. A brief §5 Döntésnaplója üres; a DT488 és a G1941-eltérés nincs benne.
3. A `naplok/THAYER_ELAVULT_HIVATKOZAS_csere.py` a brief `ir` listáján kívül esik.
