# SZOTAR S2 (#9) — `elavult_adat` szúrópróba (DT-F09g, 3. javító menet)

*Ág: `claude/f09-szotar-s2` · modell: `claude-sonnet-5-5` · mintavétel: `naplok/F09_J_elavult_szuropr.py` (seed 20261017) · proveniencia: scope=`generalt_proba/F09_szotar_s2_proba/lexikon/*_TUDOMANYOS.md` vs `lexikon/` | forras=`eszkozok/render_diff_osztalyoz.py` (`proba_osztalyoz`, kizárólagos párosítás) + `naplok/F09_J_elavult_szuropr.py` | ts=2026-10-17*

Alap: a `_TUDOMANYOS` fájlok `elavult_adat` sorai: 41 törölt (az F87.3-lábnyom nélkül), 320 hozzáadott, 27 az `ATKULCSOLT_SOROK` törölt sora (a törzscikk-oldal `elavult_adat` sorai a minta alapjában nincsenek). Rétegzett minta: 10 törölt + 5 hozzáadott + 5 lábnyom-sor. A **horgony pontos szövegegyezés vagy a kizárólagos (teljes kulcsú) pár**; az igehely-egyezés nem horgony. A „pontos egyezés” oszlop: a normalizált sor teljes egyezése a másik oldalon; minden mintánál „nincs”, mert a sorok megváltoztak (különben nem volnának a diffben), ezért a döntő a kizárólagos pár.

| # | Réteg | Fájl | Sor (rövidítve) | Horgony | Ítélet |
|---|---|---|---|---|---|
| 1 | törölt | ISTENTISZT-001 | `\| [1Móz 4:26] … H7121+H8034 … tartalom-alapú[^1] \|` | pár: ugyanaz a sor, kulcs = (sor, elofordulasok, 1Móz 4:26, {H7121,H8034}); a módszer-jelző `tartalom-alapú` → `szó-szintű-gépi` | tovább él (jelző-frissítés, `adat/elofordulasok.tsv` mai értéke) |
| 2 | törölt | ALVIL-001 | `\| [1Móz 42:38] \| a koporsóba … \|` | pár: azonos sor, kulcs (…, 1Móz 42:38, {H7585}), jelző frissítve | tovább él |
| 3 | törölt | KIRALY-001 | `*Ez a blokk … motívum 0 elutasított/nyitva maradt jelöltjét fedi …*` | pár: ugyanez a leíró mondat 14-gyel (kulcs: leíró, kizart); a `jeloltek.tsv` KIRALY-001 sorai adják a számot | elavult (a szám frissült) |
| 4 | törölt | ANTROP-001 | ugyanaz a leíró mondat, 1 | pár: 3-mal; `adat/jeloltek.tsv` ANTROP-001: 3 elutasított/nyitva sor | elavult (a szám frissült) |
| 5 | törölt | ALVIL-001 | ugyanaz a leíró mondat, 0 | pár: 2-vel | elavult (a szám frissült) |
| 6 | törölt | MENNY-001 | `\| [1Móz 6:4] \| Az óriások … H5303 … \|` | pár: azonos sor, jelző frissítve | tovább él |
| 7 | törölt | TEREMT-001 | `\| [1Móz 1:2] \| mélység … H8415 … \|` | pár: azonos sor, jelző frissítve | tovább él |
| 8 | törölt | TEREMT-001 | `\| [1Móz 7:11] \| a nagy mélység … \|` | pár: azonos sor, jelző frissítve | tovább él |
| 9 | törölt | ISTENTISZT-001 | `\| [1Móz 26:25] … \|` | pár: azonos sor, jelző frissítve | tovább él |
| 10 | törölt | TEREMT-001 | `\| [2Móz 15:5] \| a mélységbe … \|` | pár: ugyanaz a sor `a hullámok` glosszával és új jelzővel; F87.3 (98f22fc6): `karoli_szo` `a mélységbe` → `a hullámok` | elavult (adatjavítás), a sor tovább él |
| 11 | hozzáadott | ISTENTISZT-001 | `- **1Sám 13:13** (elutasítva, …)` | nincs régi pár; `adat/jeloltek.tsv`: ISTENTISZT-001, 1Sám 13:13, elutasítva | új adatsor (az éles oldal régebbi) |
| 12 | hozzáadott | ISTENTISZT-001 | `- **Róm 2:8** (elutasítva, …)` | `adat/jeloltek.tsv`: Róm 2:8, elutasítva | új adatsor |
| 13 | hozzáadott | ISTENTISZT-001 | `\| [1Móz 21:33] … ➕ bővülés … szó-szintű-gépi \|` | pár a régi sorral (kulcs: 1Móz 21:33, {H7121,H8034}) | tovább él / jelző-frissítés |
| 14 | hozzáadott | ISTENTISZT-001 | `- **ApCsel 25:21** (nyitva, …)` | `adat/jeloltek.tsv`: ApCsel 25:21, nyitva | új adatsor |
| 15 | hozzáadott | ISTENTISZT-001 | `- **Zsid 11:16** (nyitva, …)` | `adat/jeloltek.tsv`: Zsid 11:16, nyitva | új adatsor |
| 16 | lábnyom | ALVIL-001 (törzs.) | `\| [Préd 9:10](#v-préd-9-10) \| — \| Remez \| közepes … \|` | nincs pár (a régi kulcs megszűnt); a próbában `### Préd 9:12` áll (666. sor) | elavult: F87.3 átkulcsolás (`Préd 9:10` → `9:12`) |
| 17 | lábnyom | ALVIL-001 (törzs.) | `- **Kulcsszó:** A sírnak — שְׁא֣וֹל (she.'ol)` | nincs pár; a próbában a `Jób 17:12` blokk (293. sor) a javított kulcsot hordozza | elavult: F87.3 (`Jób 17:13` → `17:12`) |
| 18 | lábnyom | ALVIL-001 (tud.) | `**Préd 9:10**` | nincs pár; `Préd 9:12` az új kulcs | elavult: F87.3 |
| 19 | lábnyom | ALVIL-001 (törzs.) | `> *(Jób 17:16: nincs Károli-szöveg)*` | nincs pár; a próbában a `Jób 17:15` blokk (305. sor) Károli-szöveggel áll | elavult: F87.3 (`Jób 17:16` → `17:15`) |
| 20 | lábnyom | ALVIL-001 (törzs.) | `> *A te ruháid mindenkor legyenek fejérek …*` | nincs pár; a Károli 1908 szerint ez a Préd 9:8, nem a Seol-vers; az új kulcs `Préd 9:12` | elavult: F87.3 (a régi idézet téves versé volt) |

**Összegzés:** a 20 mintából 0 olyan sor van, amelynek a tartalma sehol nem él tovább és nem igazoltan elavult. 15 sor kizárólagos teljes kulcsú párral, vagy adatrétegbeli (`adat/jeloltek.tsv`) sorral igazolt; az 5 lábnyom-sor nincs párban, a próba átkulcsolt blokkja és az F87.3-commit (98f22fc6) igazolja. A tartalom-megőrzés tehát nem a mechanikus pontos egyezésen, hanem a pár/adatsor-horgonyon áll; ahol nincs pár és nincs lábnyom, a sor `ismeretlen` (l. `naplok/SZOTAR_S2_ismeretlen.tsv`).
