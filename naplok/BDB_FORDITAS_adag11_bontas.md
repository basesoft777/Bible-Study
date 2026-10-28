# BDB_FORDITAS — a 11. adag (sorrend 2822–3980): tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 11. adagának szakaszonkénti fordítása (prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 11. adag (2822–3980, 1159 szócikk, 499 918 forráskarakter). Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 2822 --adagok 1`: 1160 szócikk, 1160 Károli-pár; a mérés 1160-at számol, az adag a sorrend szerint 1159 — ugyanaz az egy szócikk eltérés, mint a 10. adagnál, nem vizsgáltam). Mérés ideje: 2026-10-28 18:45 (proveniencia: scope=BDB-sorrend 2822– , 1 adag | forras=naplok/BDB_FORDITAS_sorrend.tsv x adat/karoli_strong/parok_*.tsv x konkordancia/TAHOT_kivonat.tsv x adat/forditasok.tsv | ts=2026-10-28 18:45).*

*Az adag állapota: folyamatban (az adag szeletenként készül).*

## 1. Tábla-Δ

| tábla | alap (`cd8e3942`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor nélkül) | 14666 | 15244 | +578 | 578 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 14668 | 15246 | +578 | |
| `naplok/EMELES_munka.tsv` | — | — | +578 | 578 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | — | 0 | — |
| minden más `adat/` tábla | — | — | 0 | — |

**Megjegyzés-sorok (forráshiba-jelölés, DT362 (1)(a), DT363).** A H5628 minden szakaszsorának `megjegyzes` mezőjében „forráshiba: „overhungof” összetapadás (overhung of)” áll (a forrás „overhungof turbans” szavát a fordítás szétválasztva adja: „lelógott; turbánokról”). A megjegyzés Strong-szintű (DT363 kiegészítés).

**Szakasztáblán kívüli Strongok (régi `teljes` út).** A H7560 nincs az `adat/bdb_szakaszok.tsv`-ben; `emeles.py helyorzo`/`ellenoriz`/`rogzit`/`beir` úton, `jelentes_szam=teljes` sorral került be (1 sor, az F38.421-ben); régi `teljes` sora nem volt (`--regi-elavult` nem kellett).

Törölt vagy módosított meglévő `forditasok.tsv`-sor nincs (0 törlés). `kezi` sorhoz nem nyúltam.

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor | forrás-karakter (`BDB_FORDITAS_sorrend.tsv` karakter-oszlop) |
|---|---|---|---|---|---|
| F38.421 | 1. szelet, 1. rész (sorrend 2822–2990) | 169 | 578 | 578 / 0 / 0 | 75056 |
| **össz.** | | **169** | **578** | **578 / 0 / 0** | **75056** |

## 3. Strongok commitonként (sorrendben)

**F38.421** (2822–2990; 169 szócikk, 75056 karakter): H5559, H5590, H5628, H5649, H5689, H5692, H5801, H5825, H5849, H5907, H5947, H5959, H5986, H6057, H6089, H6124, H6131, H6274, H6287, H6288, H6316, H6329, H6367, H6389, H6395, H6432, H6452, H6472, H6484, H6569, H6621, H6651, H6701, H6781, H6814, H6834, H6835, H6953, H7032, H7049, H7092, H7117, H7140, H7147, H7156, H7253, H7267, H7271, H7279, H7290, H7389, H7410, H7415, H7469, H7560, H7565, H7581, H7645, H7696, H7776, H7826, H7895, H7898, H7909, H7982, H8048, H8140, H8185, H8256, H8262, H8289, H8314, H8322, H8333, H8471, H8590, H8602, H8620, H8621, H8639, H8658, H0032, H0033, H0046, H0080, H0125, H0137, H0172, H0217, H0283, H0295, H0317, H0328, H0329, H0345, H0362, H0363, H0458, H0460, H0469, H0483, H0501, H0533, H0562, H0634, H0724, H0732, H0737, H0757, H0774, H0812, H0826, H0827, H0851, H0881, H0893, H0902, H0907, H0913, H1000, H1026, H1031, H1043, H1067, H1142, H1165, H1171, H1173, H1189, H1262, H1309, H1377, H1405, H1498, H1500, H1505, H1518, H1521, H1551, H1555, H1586, H1641, H1651, H1668, H1673, H1674, H1736, H1763, H1785, H1807, H1828, H1844, H1905, H1916, H1918, H1933, H1979, H2062, H2067, H2083, H2122, H2158, H2197, H2209, H2227, H2255, H2276, H2300, H2331

## 4. 17_bdb_javitas (DT55, #67 kapu; DT367)

(folyamatban: az adag végén kerül kitöltésre; az eddigi szeleteken a fordítás egyetlen Strongja sem érintett `javitva` sorral.)

## 5. Kapu-felülbírálások (DT361)

| Strong | kapu | forrásidézet és indok |
|---|---|---|
| H1031 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "±Ain „ajla (or Qaƒr „ajla compare Rob & Di Gen 50:11)" (a „ (U+201E) OCR-maradvány, pár nélkül); hű fordítás: "±Ain „ajla (vagy Qaƒr „ajla vö. Rob és Di 1Móz 50:11)". Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nincs átfogalmazás vagy jelcsere. |
| H1171 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "or „âsbêyâ Bd^Pal 297 Di" (a „ (U+201E) OCR-maradvány, pár nélkül); hű fordítás: "vagy „âsbêyâ Bd^Pal 297 Di". Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nincs átfogalmazás vagy jelcsere. |

## 6. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (minden commit előtt).
- A tesztek (`teszt_forditas_kapuk.py`, `teszt_emeles.py`, `bdb_jelolt/teszt_szakasz_bemenet.py`) az adag végén futnak (l. a záró jelentést).

*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ cd8e3942 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat` | ts=2026-10-28)*
