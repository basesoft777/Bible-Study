# BDB_FORDITAS — a 11. adag (sorrend 2822–3980): tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 11. adagának szakaszonkénti fordítása (prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 11. adag (2822–3980, 1159 szócikk, 499 918 forráskarakter). Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 2822 --adagok 1`: 1160 szócikk, 1160 Károli-pár; a mérés 1160-at számol, az adag a sorrend szerint 1159 — ugyanaz az egy szócikk eltérés, mint a 10. adagnál, nem vizsgáltam). Mérés ideje: 2026-10-28 18:45 (proveniencia: scope=BDB-sorrend 2822– , 1 adag | forras=naplok/BDB_FORDITAS_sorrend.tsv x adat/karoli_strong/parok_*.tsv x konkordancia/TAHOT_kivonat.tsv x adat/forditasok.tsv | ts=2026-10-28 18:45).*

*Az adag állapota: folyamatban (az adag szeletenként készül).*

## 1. Tábla-Δ

| tábla | alap (`cd8e3942`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor nélkül) | 14666 | 17056 | +2390 | 2390 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 14668 | 17058 | +2390 | |
| `naplok/EMELES_munka.tsv` | — | — | +2390 | 2390 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | — | 0 | — |
| minden más `adat/` tábla | — | — | 0 | — |

**Megjegyzés-sorok (forráshiba-jelölés, DT362 (1)(a), DT363).** A H5628 minden szakaszsorának `megjegyzes` mezőjében „forráshiba: „overhungof” összetapadás (overhung of)” áll (a forrás „overhungof turbans” szavát a fordítás szétválasztva adja: „lelógott; turbánokról”). A megjegyzés Strong-szintű (DT363 kiegészítés).

**Szakasztáblán kívüli Strongok (régi `teljes` út).** A H7560 (F38.421) és a H6433 (F38.422) nincs az `adat/bdb_szakaszok.tsv`-ben; `emeles.py helyorzo`/`ellenoriz`/`rogzit`/`beir` úton, `jelentes_szam=teljes` sorral kerültek be (1–1 sor); régi `teljes` soruk nem volt (`--regi-elavult` nem kellett). A régi `rogzit` út az `EMELES_munka.tsv` megjegyzés-fejlécsorát (1. sor) `… irja: python eszkozok/emeles.py rogzit`-re írja át; ezt minden szelet commitja előtt az alapszövegre (`… rogzit / szakasz_rogzit`) állítottam vissza, így a munkatábla numstatja tiszta `N / 0`.

Törölt vagy módosított meglévő `forditasok.tsv`-sor nincs (0 törlés). `kezi` sorhoz nem nyúltam.

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor | forrás-karakter (`BDB_FORDITAS_sorrend.tsv` karakter-oszlop) |
|---|---|---|---|---|---|
| F38.421 | 1. szelet, 1. rész (sorrend 2822–2990) | 169 | 578 | 578 / 0 / 0 | 75056 |
| F38.422 | 1. szelet, 2. rész (sorrend 2991–3133) | 143 | 538 | 538 / 0 / 0 | 65466 |
| F38.423 | 2. szelet (sorrend 3134–3492) | 359 | 1274 | 1274 / 0 / 0 | 145871 |
| **össz.** | | **671** | **2390** | **2390 / 0 / 0** | **286393** |

## 3. Strongok commitonként (sorrendben)

**F38.421** (2822–2990; 169 szócikk, 75056 karakter): H5559, H5590, H5628, H5649, H5689, H5692, H5801, H5825, H5849, H5907, H5947, H5959, H5986, H6057, H6089, H6124, H6131, H6274, H6287, H6288, H6316, H6329, H6367, H6389, H6395, H6432, H6452, H6472, H6484, H6569, H6621, H6651, H6701, H6781, H6814, H6834, H6835, H6953, H7032, H7049, H7092, H7117, H7140, H7147, H7156, H7253, H7267, H7271, H7279, H7290, H7389, H7410, H7415, H7469, H7560, H7565, H7581, H7645, H7696, H7776, H7826, H7895, H7898, H7909, H7982, H8048, H8140, H8185, H8256, H8262, H8289, H8314, H8322, H8333, H8471, H8590, H8602, H8620, H8621, H8639, H8658, H0032, H0033, H0046, H0080, H0125, H0137, H0172, H0217, H0283, H0295, H0317, H0328, H0329, H0345, H0362, H0363, H0458, H0460, H0469, H0483, H0501, H0533, H0562, H0634, H0724, H0732, H0737, H0757, H0774, H0812, H0826, H0827, H0851, H0881, H0893, H0902, H0907, H0913, H1000, H1026, H1031, H1043, H1067, H1142, H1165, H1171, H1173, H1189, H1262, H1309, H1377, H1405, H1498, H1500, H1505, H1518, H1521, H1551, H1555, H1586, H1641, H1651, H1668, H1673, H1674, H1736, H1763, H1785, H1807, H1828, H1844, H1905, H1916, H1918, H1933, H1979, H2062, H2067, H2083, H2122, H2158, H2197, H2209, H2227, H2255, H2276, H2300, H2331

**F38.422** (2991–3133; 143 szócikk, 65466 karakter): H2418, H2485, H2531, H2535, H2558, H2560, H2624, H2625, H2651, H2690, H2698, H2704, H2730, H2750, H2752, H2892, H2976, H3043, H3066, H3127, H3166, H3179, H3226, H3278, H3355, H3418, H3420, H3511, H3553, H3585, H3700, H3784, H3785, H3803, H3868, H3892, H3897, H3928, H4093, H4114, H4132, H4174, H4234, H4245, H4302, H4315, H4345, H4371, H4375, H4387, H4407, H4457, H4494, H4514, H4689, H4708, H4800, H4807, H4822, H4903, H4906, H4933, H4968, H4985, H4991, H4997, H5011, H5031, H5050, H5067, H5102, H5121, H5123, H5138, H5246, H5257, H5365, H5382, H5450, H5512, H5543, H5572, H5585, H5596, H5603, H5617, H5651, H5670, H5696, H5832, H5840, H5873, H5874, H5896, H5909, H5912, H5955, H5988, H6137, H6144, H6152, H6181, H6191, H6202, H6225, H6236, H6319, H6424, H6433, H6443, H6458, H6530, H6531, H6540, H6551, H6600, H6620, H6728, H6842, H6875, H6906, H6927, H6945, H6962, H6976, H6979, H7018, H7028, H7034, H7039, H7067, H7236, H7241, H7244, H7249, H7312, H7336, H7376, H7400, H7426, H7461, H7468, H7476

**F38.423** (3134–3492; 359 szócikk, 145871 karakter): H7482, H7552, H7582, H7619, H7643, H7655, H7659, H7675, H7709, H7711, H7793, H7838, H7847, H7849, H7852, H7853, H7858, H7888, H8060, H8076, H8155, H8229, H8246, H8264, H8266, H8271, H8366, H8380, H8439, H8458, H8480, H8526, H8545, H8555, H8556, H8598, H8599, H8636, H8649, H8664, H0011, H0027, H0049, H0050, H0091, H0126, H0170, H0171, H0207, H0218, H0235, H0266, H0286, H0299, H0321, H0333, H0342, H0380, H0431, H0451, H0459, H0468, H0485, H0500, H0552, H0570, H0611, H0616, H0636, H0656, H0661, H0673, H0680, H0686, H0687, H0709, H0718, H0762, H0796, H0809, H0855, H0862, H0886, H0980, H1071, H1085, H1087, H1158, H1198, H1217, H1221, H1231, H1240, H1252, H1297, H1379, H1441, H1470, H1552, H1583, H1584, H1587, H1626, H1634, H1660, H1690, H1700, H1734, H1739, H1780, H1789, H1794, H1801, H1802, H1839, H1843, H1891, H1927, H1949, H2027, H2028, H2043, H2073, H2156, H2182, H2191, H2196, H2228, H2240, H2247, H2251, H2259, H2284, H2294, H2380, H2392, H2394, H2407, H2457, H2465, H2496, H2497, H2503, H2590, H2596, H2621, H2633, H2652, H2773, H2786, H2815, H2825, H2828, H2843, H2948, H2970, H2994, H3025, H3136, H3182, H3209, H3215, H3232, H3309, H3330, H3419, H3469, H3481, H3488, H3505, H3540, H3599, H3660, H3668, H3717, H3721, H3755, H3795, H3823, H3845, H3849, H3865, H3882, H3888, H3908, H3913, H3993, H3994, H4076, H4099, H4134, H4162, H4212, H4227, H4244, H4301, H4311, H4348, H4370, H4414, H4446, H4448, H4449, H4483, H4488, H4506, H4524, H4532, H4537, H4554, H4612, H4615, H4662, H4693, H4705, H4768, H4772, H4785, H4867, H4937, H4971, H4976, H4996, H5007, H5032, H5098, H5168, H5184, H5233, H5250, H5279, H5317, H5356, H5367, H5433, H5449, H5456, H5460, H5490, H5491, H5498, H5566, H5579, H5599, H5609, H5632, H5672, H5682, H5756, H5763, H5767, H5786, H5829, H5856, H5862, H5871, H5891, H5911, H5915, H5918, H5968, H5996, H6022, H6069, H6071, H6082, H6094, H6117, H6140, H6155, H6166, H6195, H6264, H6295, H6396, H6398, H6400, H6410, H6446, H6465, H6470, H6553, H6567, H6617, H6623, H6624, H6636, H6647, H6675, H6686, H6698, H6706, H6714, H6767, H6775, H6788, H6797, H6808, H6826, H6848, H6876, H6893, H6982, H6998, H7021, H7024, H7077, H7096, H7116, H7134, H7135, H7139, H7169, H7176, H7183, H7210, H7238, H7314, H7343, H7345, H7347, H7397, H7408, H7413, H7466, H7484, H7486, H7491, H7508, H7509, H7538, H7541, H7599, H7603, H7624, H7662, H7698, H7707, H7745, H7747, H7851, H7868, H7918, H7951, H8017, H8029, H8041, H8051, H8059, H8080, H8087, H8092, H8105, H8106, H8110, H8160, H8222, H8239, H8257

## 4. 17_bdb_javitas (DT55, #67 kapu; DT367)

(folyamatban: az adag végén kerül kitöltésre; az eddigi szeleteken a fordítás egyetlen Strongja sem érintett `javitva` sorral.)

## 5. Kapu-felülbírálások (DT361)

| Strong | kapu | forrásidézet és indok |
|---|---|---|
| H1031 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "±Ain „ajla (or Qaƒr „ajla compare Rob & Di Gen 50:11)" (a „ (U+201E) OCR-maradvány, pár nélkül); hű fordítás: "±Ain „ajla (vagy Qaƒr „ajla vö. Rob és Di 1Móz 50:11)". Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nincs átfogalmazás vagy jelcsere. |
| H1171 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "or „âsbêyâ Bd^Pal 297 Di" (a „ (U+201E) OCR-maradvány, pár nélkül); hű fordítás: "vagy „âsbêyâ Bd^Pal 297 Di". Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nincs átfogalmazás vagy jelcsere. |
| H8556 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 11_konyvek | forrás: "= ⟦2⟧1Makk 9:50 +?Tibneh" (a forrásban már Károli-alakú „1Makk 9:50” áll, a Makkabeusok 1. könyve; a kapu a forrásoldalon nem ismeri fel, a fordításban igen: „a forditasban tobb: 1Makk×1”); hű fordítás: "= ⟦2⟧1Makk 9:50 +?Tibneh". Felülbírálás: `--kapu-felulir 11_konyvek --dontes DT361`; a hivatkozás betűre azonos a forrással, átfogalmazás nincs. |

## 6. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (minden commit előtt).
- A tesztek (`teszt_forditas_kapuk.py`, `teszt_emeles.py`, `bdb_jelolt/teszt_szakasz_bemenet.py`) az adag végén futnak (l. a záró jelentést).

*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ cd8e3942 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat` | ts=2026-10-28)*
