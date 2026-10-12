# ELLENOR_BDB_KAROLI_POTLAS — brief: F80_BDB_KAROLI_POTLAS_BRIEF.md (v2)

*Tartomány: origin/main..5f13e0ce (6 commit). A `fuggetlen-ellenor` jelentése; a szerepköre miatt a fájlba mentést az orkesztrátor végezte, a tartalom a jelentés tömörített, a megállapításokat és a számokat megtartó változata.*

**Eredmény: ELTÉRÉS, 6 tétel.**

## Rendben

| pont | megállapítás |
|---|---|
| Diff-hatókör | 7 fájl: DONTESEK, brief, SEMA, `adat/bdb_karoli.tsv` (új), `bdb_adatblokk.py`, teszt, M0-napló; a main nem haladt tovább |
| K1 | 466 785 sor 39 ÓSZ-fájlban, a nem 4 jegyű H-alak 0 (egyezik az M0-val) |
| K2 | 674 kész szócikk = 674 `szocikk` sor = 674 teljes proveniencia-sor; `[NINCS KÁROLI-ALAK]` 0 (az ágat csak mockolt teszt fedi) |
| Visszakereshetőség | öt saját Strong (H0001, H0426, H3722, H3782, H4054) példái visszakereshetők a `parok_*.tsv`-ből; a `tahot_elofordulas` négy esetben egyezik a `lekerdez.py scan` eredményével (102, 62, 119, 95) |
| K3 | `adat/forditasok.tsv` blob `1060f59d` az `origin/main`-en és a HEAD-en is; a diff üres |
| M1, M2 | `split('\t')`/`'\t'.join`, `csv` nincs; a tabot/újsort `assert` védi |
| `test_nincs_karoli_alak` | a módosítás jogos (a H0426-nak ma 95 `parok`-sora van); a mock ugyanazt az ágat teszteli |
| Blokkgenerálás | `bdb_adatblokk.py`: 94 hozzáadott, 0 törölt sor |
| D, ⛔ | DT117 rögzítve, az M1 a döntés után készült; A1–A6 rendben |

## Eltérések (súlyossági sorrendben)

1. **A példaversek nem kanonikus sorrendűek.** A SEMA 2.25 (`adat/SEMA.md:1122`) szerint a `parok` kanonikus sorrendjében állnak, de a `parok_konyvek()` (`eszkozok/bdb_adatblokk.py:165-175`) az 1–5Móz és a Józs után ASCII fájlnév szerint rendez. Példa: H2617 `irgalmassága` → „1Krón 16:34;1Krón 16:41;1Sám 20:14”. A hiba a meglévő blokk példaválasztását is érinti.
2. **Mind a 61 852 `alak` sor proveniencia-mezője üres.** Ellentétes a SEMA 1.5-tel („a `manual` a helyes kitöltés, nem az üresen hagyás”) és a CLAUDE.md 1. szabályával. A szócikk-sorra mutató csoportszintű hivatkozás új konvenció, amelyet csak a 2.25 rögzít. Döntés kell: a proveniencia ismétlése a sorokon, vagy kivétel a SEMA 1.5-ben.
3. **A `par_db` leírása téves** (`adat/SEMA.md:1124`): link-darab, nem a `tahot_elofordulas` részhalmaza (H3722: 178 pár 102 előfordulásra; H4191: 1087 / 840).
4. **Hiányzik az E17/DT3 bontási napló** az új, 62 526 soros táblához (`szocikk` 674 + `alak` 61 852).
5. **A SEMA „ábécé-sorrendje” kódpont-sorrend** (`adat/SEMA.md:1127`; alacsony súly).
6. **A brief `kovetkezo` mezője elavult** (alacsony súly).

## Nem ellenőrizhető (az ellenőr szerepköre miatt)

- A tesztek és az `ellenoriz.py` futtatása; a végrehajtó jelentése szerint 42 teszt zöld, SÉRTÉS 0.
- `test_pelda_idezet_szo_szerinti`: az új teszt gyengébb (nincs rögzített vers); a régi rögzítés (1Móz 24:14) a táblában ma is szerepel.
- Az M0 432/214/28 csoportbontása (git-történeti rekonstrukció, `scope=manual`, a korlát kimondva).
- CI-jelentés nem volt; a `futtat.py`: E2–E20, E26 0 találat, HIBA 0.
