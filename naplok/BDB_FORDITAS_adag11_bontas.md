# BDB_FORDITAS — a 11. adag (sorrend 2822–3980): tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 11. adagának szakaszonkénti fordítása (prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 11. adag (2822–3980, 1159 szócikk, 499 918 forráskarakter). Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 2822 --adagok 1`: 1160 szócikk, 1160 Károli-pár; a mérés 1160-at számol, az adag a sorrend szerint 1159 — ugyanaz az egy szócikk eltérés, mint a 10. adagnál, nem vizsgáltam). Mérés ideje: 2026-10-28 18:45 (proveniencia: scope=BDB-sorrend 2822– , 1 adag | forras=naplok/BDB_FORDITAS_sorrend.tsv x adat/karoli_strong/parok_*.tsv x konkordancia/TAHOT_kivonat.tsv x adat/forditasok.tsv | ts=2026-10-28 18:45).*

*Az adag állapota: lezárva: a fordítás kész a 3980. sorrendi helyig (az adag mind az 1159 szócikke), független ellenőrzésre vár.*

## 1. Tábla-Δ

| tábla | alap (`cd8e3942`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor nélkül) | 14666 | 18732 | +4066 | 4066 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 14668 | 18734 | +4066 | |
| `naplok/EMELES_munka.tsv` | — | — | +4066 | 4066 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | — | +2 sor | 2 / 0 |
| minden más `adat/` tábla | — | — | 0 | — |

**Megjegyzés-sorok (forráshiba-jelölés, DT362 (1)(a), DT363).** A H5628 minden szakaszsorának `megjegyzes` mezőjében „forráshiba: „overhungof” összetapadás (overhung of)” áll (a forrás „overhungof turbans” szavát a fordítás, a javítókör 1/2 után, egyben adja: „turbánokkal lelógó”). A megjegyzés Strong-szintű (DT363 kiegészítés).

**Szakasztáblán kívüli Strongok (régi `teljes` út).** A H7560 (F38.421) és a H6433 (F38.422) nincs az `adat/bdb_szakaszok.tsv`-ben; `emeles.py helyorzo`/`ellenoriz`/`rogzit`/`beir` úton, `jelentes_szam=teljes` sorral kerültek be (1–1 sor); régi `teljes` soruk nem volt (`--regi-elavult` nem kellett). A régi `rogzit` út az `EMELES_munka.tsv` megjegyzés-fejlécsorát (1. sor) `… irja: python eszkozok/emeles.py rogzit`-re írja át; ezt minden szelet commitja előtt az alapszövegre (`… rogzit / szakasz_rogzit`) állítottam vissza, így a munkatábla numstatja tiszta `N / 0`.

**További megjegyzés-sorok (forráshiba-jelölés, DT362 (1)(a)).** A H5460 minden szakaszsorának `megjegyzes` mezőjében „forráshiba: „perfect” = prefect (helytartó)” áll (a forrás „perfect”-nek írja a *prefektus* szót; a fordítás „prefektus”). A H5194 minden szakaszsorának `megjegyzes` mezőjében „forráshiba: „Judab” = Judah” áll (a fordítás: „Júdáról”). Mindkettő Strong-szintű megjegyzés (DT363 kiegészítés).

Törölt vagy módosított meglévő `forditasok.tsv`-sor nincs (0 törlés). `kezi` sorhoz nem nyúltam.

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor | forrás-karakter (`BDB_FORDITAS_sorrend.tsv` karakter-oszlop) |
|---|---|---|---|---|---|
| F38.421 | 1. szelet, 1. rész (sorrend 2822–2990) | 169 | 578 | 578 / 0 / 0 | 75056 |
| F38.422 | 1. szelet, 2. rész (sorrend 2991–3133) | 143 | 538 | 538 / 0 / 0 | 65466 |
| F38.423 | 2. szelet (sorrend 3134–3492) | 359 | 1274 | 1274 / 0 / 0 | 145871 |
| F38.424 | 3. szelet (sorrend 3493–3791) | 299 | 1052 | 1052 / 0 / 0 | 147256 |
| F38.425 | 4. szelet (sorrend 3792–3980) | 189 | 624 | 624 / 0 / 0 | 66269 |
| **össz.** | | **1159** | **4066** | **4066 / 0 / 0** | **499918** |

## 3. Strongok commitonként (sorrendben)

**F38.421** (2822–2990; 169 szócikk, 75056 karakter): H5559, H5590, H5628, H5649, H5689, H5692, H5801, H5825, H5849, H5907, H5947, H5959, H5986, H6057, H6089, H6124, H6131, H6274, H6287, H6288, H6316, H6329, H6367, H6389, H6395, H6432, H6452, H6472, H6484, H6569, H6621, H6651, H6701, H6781, H6814, H6834, H6835, H6953, H7032, H7049, H7092, H7117, H7140, H7147, H7156, H7253, H7267, H7271, H7279, H7290, H7389, H7410, H7415, H7469, H7560, H7565, H7581, H7645, H7696, H7776, H7826, H7895, H7898, H7909, H7982, H8048, H8140, H8185, H8256, H8262, H8289, H8314, H8322, H8333, H8471, H8590, H8602, H8620, H8621, H8639, H8658, H0032, H0033, H0046, H0080, H0125, H0137, H0172, H0217, H0283, H0295, H0317, H0328, H0329, H0345, H0362, H0363, H0458, H0460, H0469, H0483, H0501, H0533, H0562, H0634, H0724, H0732, H0737, H0757, H0774, H0812, H0826, H0827, H0851, H0881, H0893, H0902, H0907, H0913, H1000, H1026, H1031, H1043, H1067, H1142, H1165, H1171, H1173, H1189, H1262, H1309, H1377, H1405, H1498, H1500, H1505, H1518, H1521, H1551, H1555, H1586, H1641, H1651, H1668, H1673, H1674, H1736, H1763, H1785, H1807, H1828, H1844, H1905, H1916, H1918, H1933, H1979, H2062, H2067, H2083, H2122, H2158, H2197, H2209, H2227, H2255, H2276, H2300, H2331

**F38.422** (2991–3133; 143 szócikk, 65466 karakter): H2418, H2485, H2531, H2535, H2558, H2560, H2624, H2625, H2651, H2690, H2698, H2704, H2730, H2750, H2752, H2892, H2976, H3043, H3066, H3127, H3166, H3179, H3226, H3278, H3355, H3418, H3420, H3511, H3553, H3585, H3700, H3784, H3785, H3803, H3868, H3892, H3897, H3928, H4093, H4114, H4132, H4174, H4234, H4245, H4302, H4315, H4345, H4371, H4375, H4387, H4407, H4457, H4494, H4514, H4689, H4708, H4800, H4807, H4822, H4903, H4906, H4933, H4968, H4985, H4991, H4997, H5011, H5031, H5050, H5067, H5102, H5121, H5123, H5138, H5246, H5257, H5365, H5382, H5450, H5512, H5543, H5572, H5585, H5596, H5603, H5617, H5651, H5670, H5696, H5832, H5840, H5873, H5874, H5896, H5909, H5912, H5955, H5988, H6137, H6144, H6152, H6181, H6191, H6202, H6225, H6236, H6319, H6424, H6433, H6443, H6458, H6530, H6531, H6540, H6551, H6600, H6620, H6728, H6842, H6875, H6906, H6927, H6945, H6962, H6976, H6979, H7018, H7028, H7034, H7039, H7067, H7236, H7241, H7244, H7249, H7312, H7336, H7376, H7400, H7426, H7461, H7468, H7476

**F38.423** (3134–3492; 359 szócikk, 145871 karakter): H7482, H7552, H7582, H7619, H7643, H7655, H7659, H7675, H7709, H7711, H7793, H7838, H7847, H7849, H7852, H7853, H7858, H7888, H8060, H8076, H8155, H8229, H8246, H8264, H8266, H8271, H8366, H8380, H8439, H8458, H8480, H8526, H8545, H8555, H8556, H8598, H8599, H8636, H8649, H8664, H0011, H0027, H0049, H0050, H0091, H0126, H0170, H0171, H0207, H0218, H0235, H0266, H0286, H0299, H0321, H0333, H0342, H0380, H0431, H0451, H0459, H0468, H0485, H0500, H0552, H0570, H0611, H0616, H0636, H0656, H0661, H0673, H0680, H0686, H0687, H0709, H0718, H0762, H0796, H0809, H0855, H0862, H0886, H0980, H1071, H1085, H1087, H1158, H1198, H1217, H1221, H1231, H1240, H1252, H1297, H1379, H1441, H1470, H1552, H1583, H1584, H1587, H1626, H1634, H1660, H1690, H1700, H1734, H1739, H1780, H1789, H1794, H1801, H1802, H1839, H1843, H1891, H1927, H1949, H2027, H2028, H2043, H2073, H2156, H2182, H2191, H2196, H2228, H2240, H2247, H2251, H2259, H2284, H2294, H2380, H2392, H2394, H2407, H2457, H2465, H2496, H2497, H2503, H2590, H2596, H2621, H2633, H2652, H2773, H2786, H2815, H2825, H2828, H2843, H2948, H2970, H2994, H3025, H3136, H3182, H3209, H3215, H3232, H3309, H3330, H3419, H3469, H3481, H3488, H3505, H3540, H3599, H3660, H3668, H3717, H3721, H3755, H3795, H3823, H3845, H3849, H3865, H3882, H3888, H3908, H3913, H3993, H3994, H4076, H4099, H4134, H4162, H4212, H4227, H4244, H4301, H4311, H4348, H4370, H4414, H4446, H4448, H4449, H4483, H4488, H4506, H4524, H4532, H4537, H4554, H4612, H4615, H4662, H4693, H4705, H4768, H4772, H4785, H4867, H4937, H4971, H4976, H4996, H5007, H5032, H5098, H5168, H5184, H5233, H5250, H5279, H5317, H5356, H5367, H5433, H5449, H5456, H5460, H5490, H5491, H5498, H5566, H5579, H5599, H5609, H5632, H5672, H5682, H5756, H5763, H5767, H5786, H5829, H5856, H5862, H5871, H5891, H5911, H5915, H5918, H5968, H5996, H6022, H6069, H6071, H6082, H6094, H6117, H6140, H6155, H6166, H6195, H6264, H6295, H6396, H6398, H6400, H6410, H6446, H6465, H6470, H6553, H6567, H6617, H6623, H6624, H6636, H6647, H6675, H6686, H6698, H6706, H6714, H6767, H6775, H6788, H6797, H6808, H6826, H6848, H6876, H6893, H6982, H6998, H7021, H7024, H7077, H7096, H7116, H7134, H7135, H7139, H7169, H7176, H7183, H7210, H7238, H7314, H7343, H7345, H7347, H7397, H7408, H7413, H7466, H7484, H7486, H7491, H7508, H7509, H7538, H7541, H7599, H7603, H7624, H7662, H7698, H7707, H7745, H7747, H7851, H7868, H7918, H7951, H8017, H8029, H8041, H8051, H8059, H8080, H8087, H8092, H8105, H8106, H8110, H8160, H8222, H8239, H8257

**F38.424** (3493–3791; 299 szócikk, 147256 karakter): H8282, H8286, H8324, H8348, H8355, H8431, H8460, H8463, H8485, H8503, H8510, H8513, H8525, H8538, H8570, H8572, H8575, H8583, H8588, H8624, H8660, H0009, H0042, H0084, H0088, H0092, H0139, H0174, H0192, H0198, H0204, H0208, H0219, H0222, H0225, H0289, H0323, H0392, H0409, H0445, H0450, H0491, H0502, H0579, H0581, H0586, H0594, H0602, H0603, H0617, H0667, H0733, H0780, H0864, H0877, H0928, H0955, H0981, H1012, H1016, H1021, H1024, H1030, H1039, H1044, H1046, H1050, H1057, H1063, H1069, H1082, H1092, H1120, H1155, H1172, H1179, H1261, H1281, H1356, H1372, H1415, H1430, H1432, H1435, H1474, H1476, H1488, H1547, H1550, H1565, H1573, H1608, H1610, H1621, H1630, H1631, H1654, H1662, H1675, H1682, H1713, H1717, H1740, H1747, H1749, H1765, H1790, H1824, H1845, H1871, H1896, H1902, H1907, H1913, H1938, H1946, H1947, H2047, H2138, H2141, H2165, H2172, H2208, H2218, H2238, H2258, H2267, H2279, H2295, H2299, H2330, H2345, H2366, H2367, H2393, H2479, H2509, H2519, H2524, H2570, H2571, H2582, H2597, H2601, H2606, H2657, H2678, H2688, H2707, H2735, H2799, H2837, H2846, H2897, H2935, H2947, H2973, H2982, H3065, H3075, H3169, H3229, H3258, H3281, H3287, H3305, H3317, H3325, H3331, H3362, H3370, H3440, H3446, H3453, H3456, H3484, H3492, H3512, H3514, H3536, H3546, H3610, H3626, H3648, H3655, H3685, H3706, H3716, H3729, H3739, H3748, H3819, H3850, H3864, H3926, H3979, H3986, H3992, H4021, H4029, H4030, H4031, H4050, H4061, H4070, H4106, H4115, H4137, H4158, H4165, H4211, H4213, H4223, H4236, H4237, H4248, H4265, H4314, H4316, H4326, H4374, H4419, H4442, H4445, H4486, H4500, H4518, H4520, H4529, H4531, H4542, H4548, H4586, H4656, H4732, H4734, H4770, H4794, H4834, H4846, H4848, H4863, H4884, H4909, H4920, H4927, H4928, H4953, H4956, H4964, H4974, H5009, H5014, H5029, H5069, H5107, H5133, H5142, H5190, H5194, H5218, H5228, H5230, H5243, H5248, H5255, H5270, H5284, H5290, H5292, H5298, H5306, H5322, H5342, H5353, H5434, H5442, H5443, H5444, H5466, H5481, H5520, H5541, H5548, H5554, H5570, H5667, H5720, H5730, H5742, H5748, H5755, H5799, H5803, H5806, H5842, H5852, H5885, H5920

**F38.425** (3792–3980; 189 szócikk, 66269 karakter): H5934, H5939, H5963, H5964, H5995, H6005, H6012, H6056, H6081, H6090, H6151, H6170, H6182, H6185, H6209, H6217, H6228, H6251, H6262, H6277, H6292, H6302, H6304, H6312, H6313, H6320, H6322, H6335, H6357, H6365, H6380, H6385, H6427, H6428, H6454, H6460, H6473, H6572, H6594, H6611, H6682, H6689, H6691, H6695, H6699, H6703, H6716, H6734, H6750, H6760, H6761, H6777, H6778, H6850, H6877, H6892, H6926, H6932, H6949, H6989, H6994, H7008, H7020, H7030, H7033, H7046, H7062, H7074, H7087, H7146, H7152, H7154, H7160, H7168, H7182, H7184, H7211, H7216, H7248, H7256, H7258, H7292, H7298, H7300, H7320, H7344, H7353, H7404, H7409, H7428, H7445, H7504, H7532, H7574, H7683, H7685, H7713, H7726, H7727, H7779, H7784, H7791, H7803, H7833, H7875, H7880, H7883, H7903, H7958, H7989, H8001, H8069, H8070, H8072, H8089, H8099, H8113, H8114, H8124, H8148, H8149, H8178, H8186, H8247, H8272, H8275, H8278, H8361, H8367, H8423, H8424, H8425, H8443, H8447, H8495, H8496, H8521, H8528, H8536, H8562, H8609, H8622, H8648, H8663, H8674, H0018, H0022, H0083, H0100, H0101, H0103, H0104, H0124, H0132, H0140, H0142, H0152, H0163, H0165, H0167, H0180, H0181, H0187, H0201, H0228, H0233, H0250, H0253, H0254, H0260, H0294, H0311, H0338, H0344, H0350, H0358, H0366, H0368, H0384, H0393, H0407, H0416, H0417, H0418, H0444, H0473, H0484, H0492, H0508

## 4. 17_bdb_javitas (DT55, #67 kapu; DT367)

A 17. kapu (`17_bdb_javitas`, DT367) az adag 1159 Strongja közül két Strongot érintett (a forrásszöveg `adat/bdb_igehely_javitas.tsv`-beli hivatkozást tartalmaz):

| Strong | hivatkozás a forrásban | javítás-sor állapota | a fordításban |
|---|---|---|---|
| H2597 (`chanukkah`) | `Ezra 16:17` | `javitva` → `Ezra 6:17` | `Ezsd 6:17 [BDB: Ezsd 16:17]` (a javított olvasat áll elöl, a BDB eredeti hivatkozása szögletes zárójelben; a kapu átengedte) |
| H7216 (`Ramoth`) | `1Ki 145:31` | `jelolt_marad` (nincs javított olvasat) | `1Kir 145:31` — hűen, betű szerint marad, a hely nem javított (a forrás: „[Jerome Ib.^145. 1Ki 145:31 says E!]”; a fordítás: „[Jerome Ib.^145. 1Kir 145:31 szerint E!]”) |

A többi Strong forrásában nem szerepelt `javitva` vagy `jelolt_marad` sorral érintett hivatkozás.

**Megjegyzés (forráshiba; `jelolt_marad` sor a javítótáblában, javított hivatkozás nélkül):** a H7216 forrásában `1Ki 145:31` áll (nem létező fejezet; `adat/bdb_igehely_javitas.tsv`: `jelolt_marad` sor, javított hivatkozás nélkül); a fordítás hűen átveszi (`1Kir 145:31`), `Y [BDB: X]` jelölés nélkül.

## 5. Kapu-felülbírálások (DT361)

| Strong | kapu | forrásidézet és indok |
|---|---|---|
| H1031 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "±Ain „ajla (or Qaƒr „ajla compare Rob & Di Gen 50:11)" (a „ (U+201E) OCR-maradvány, pár nélkül); hű fordítás: "±Ain „ajla (vagy Qaƒr „ajla vö. Rob és Di 1Móz 50:11)". Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nincs átfogalmazás vagy jelcsere. |
| H1171 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "or „âsbêyâ Bd^Pal 297 Di" (a „ (U+201E) OCR-maradvány, pár nélkül); hű fordítás: "vagy „âsbêyâ Bd^Pal 297 Di". Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nincs átfogalmazás vagy jelcsere. |
| H8556 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 11_konyvek | forrás (`adat/bdb_szakaszok.tsv`): "= Θαμναθα1Makk 9:50 +?Tibneh" (a forrásban már Károli-alakú „1Makk 9:50” áll; a kapu a forrásoldalon nem ismeri fel, a fordításban igen); fordítás: "= Θαμναθα1Makk 9:50 +?Tibneh". Felülbírálás: `--kapu-felulir 11_konyvek --dontes DT361`; a hivatkozás betűre azonos a forrással, átfogalmazás nincs. |
| H5032 (mind a szakaszsor; Strong-szintű) | 5_terminologia | forrás (`adat/bdb_szakaszok.tsv`): "Eut^Nab p.78 GASm^Geogr. 547-629 pass." (a `pass.` a *passim* rövidítése egy irodalmi hivatkozásban, nem szenvedő alak); a rögzített (javítókör 1/2 utáni) fordítás: "Eut^Nab o.78 GASm^Geogr. 547-629 passim." Felülbírálás: `--kapu-felulir 5_terminologia --dontes DT361`; átfogalmazás nincs. |
| H8485 (mind a szakaszsor; Strong-szintű) | 5_terminologia | forrás (`adat/bdb_szakaszok.tsv`): "Modern Teyma, northwest Arabia, Doughty^Arab.Des.i, pass., especially 284-299" (a `pass.` a *passim* rövidítése, nem szenvedő alak); fordítás (javítókör 1/2 után): "Doughty^Arab.Des.i, passim, különösen 284-299". Felülbírálás: `--kapu-felulir 5_terminologia --dontes DT361`; átfogalmazás nincs. |
| H2688 (mind a szakaszsor; Strong-szintű) | 8_idezojel | forrás (`adat/bdb_szakaszok.tsv`): "Wady „uƒ¹ƒ¹ (= חצצן ?) lies northwest from Engedi GASm^l.c." (a „ (U+201E) OCR-maradvány, pár nélkül); fordítás: "Wady „uƒ¹ƒ¹ (= חצצן ?) Engedi-től északnyugatra fekszik GASm^l.c." Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; átfogalmazás nincs. |

## 6. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (minden commit előtt; a záró futás: RENDBEN 14 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 3).
- `python eszkozok/teszt_forditas_kapuk.py`: Ran 110 tests, OK.
- `python eszkozok/teszt_emeles.py`: Ran 31 tests, OK.
- `python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py`: Ran 25 tests, OK.

- Javítókör 1/2 után (HEAD `F38.428`): `python eszkozok/ellenoriz.py`: RENDBEN 14 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 3; a három teszt újrafutása: `teszt_forditas_kapuk` 110, `teszt_emeles` 31, `teszt_szakasz_bemenet` 25 teszt, mind OK.
- `python eszkozok/ellenorzes/futtat.py --valtozott F38_BDB_FORDITAS_BRIEF.md adat/forditasok.tsv naplok/BDB_FORDITAS_adag11_bontas.md naplok/EMELES_munka.tsv naplok/FORDITAS_kisnagybetu_csere.tsv naplok/ELLENOR_F38_adag11.md --diff-alap cd8e3942 --diff-fej HEAD`: E2–E16, E19, E20, E26, E28 (1 migrált nézet), E29, E31, E32: 0 találat; E25: JELENTÉS 4 és E27: JELENTÉS 40 (`CLAUDE.md`, `MUNKAMENET.md`, `FELADATOK.md`; nem ennek a diffnek a fájljai); E30: 1 FIGYELMEZTETÉS — az F38.425 (`b4a74cdd`) commitüzenetében a táblaérték ékezet nélkül és backtick nélkül áll (`javitva`); az üzenetet nem írtam át (l. Helyesbítés). HIBA szintű találat nincs.

*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ cd8e3942 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat` | ts=2026-10-28)*

## 7. Javítókör 1/2 (`naplok/ELLENOR_F38_adag11.md`, ELTÉRÉS: 4 tétel)

**Javított sorok (F38.428; `adat/forditasok.tsv` `git diff --numstat` 10 / 10, `naplok/EMELES_munka.tsv` 114 / 114 — a munkatábla sorait a `szakasz_rogzit` helyben cseréli, az 1. megjegyzés-sor változatlan).** Az eszközláncon át (`szakasz_ellenoriz` → `szakasz_rogzit` → `szakasz_beir`), a kapuk lefutásával; DT361-felülbírálás csak a korábban is felülbírált Strongoknál (H1171, H2688, H8556, H5032, H8485), azonos kapuval. 10 sor, mind `sonnet` / `claude-sonnet-5-5`:

| Strong, szakasz | javítás |
|---|---|
| H5920 sz5 | „építeni a templom ellen” → „építeni a templom mellé” (térbeli értelem) |
| H5628 sz5 | „lelógott; turbánokról” → „turbánokkal lelógó” (az „overhung of turbans” szerkezet egyben; a `forráshiba` `megjegyzes` marad) |
| H5142 sz4 | „aktív participium f. status constructus” → „… nőnemű status constructus” |
| H1069 sz7 | „Hiph`il participium f.” → „… nőnemű” (ugyanaz a hibatípus, szúrópróba-bővítés) |
| H1171 sz2 | „a szerencse istenként” → „isteneként” |
| H2688 sz2 | „GASm azt is felveti” → „GASm annak lehetőségét is felveti” |
| H8556 sz2 | „17 mérföldre nyugatra északtól Jeruzsálemtől” → „17 mérföldre északnyugatra Jeruzsálemtől” |
| H7216 sz5 | „xviii f.-ben” → „xviii k.-ben” (a „következő” rövidítése) |
| H5032 sz2 | „szétszórtan” → „passim” |
| H8485 sz2 | „pass.” → „passim” |

**Rövidítés-elv (2/f).** `grep` a korábbi adagokon (`adat/forditasok.tsv`, az adag előtti 14 668 adatsor): a „következő(k)” rövidítése `k.` (186 sor) / `kk.` (503 előfordulás), „f.” a szövegben nincs (a „feminine” rövidítésére 0 sor, a „nőnemű” 1512); a `pass.`/`passim` a korábbi adagokban nem fordult elő. Elv az adagon belül: (1) oldalszám/hely után a „következő(k)” `k.`/`kk.` (az eszköz az összeragadt „301f.” alakot már így adja); (2) a „feminine” rövidítése („f.”) mindig „nőnemű”; (3) a `pass.` (a latin *passim* rövidítése) **„passim”**, azaz latin szóként marad (mint a `si vera lectio`, `q. v.`), nem „szétszórtan” és nem „pass.”; a 5_terminologia kapu `pass.` → „szenvedő alakban” szabálya az irodalmi hivatkozásokban téves, ezért a két Strongnál (H5032, H8485) a DT361-felülbírálás marad. A betűjelű szakaszmarkerek („d. f. g.”) nem tartoznak ide.

**Szúrópróba-bővítés (grep, `adat/forditasok.tsv` ≥ 14 669. sor).** Fordítatlan „f.” rövidítés az adagban 3 helyen volt (H5142, H1069, H7216), mind javítva; „ff.” fordítatlanul nincs. A térbeli „against” → „ellen” hibatípus: az adag összes 18 „ellen” előfordulását átnéztem, más térbeli használat nincs (H5920 sz5 az egyetlen); további javított sor: 0 a térbeli „ellen” típusban. Összes javított sor: 10.

**Helyesbítés (a commitüzenetekhez; a korábbi üzeneteket nem írtam át).** A H1031 és a H1171 felülbírálása valójában az F38.421-ben (`12dd21b9`) van (az F38.423 üzenete tévesen említi); a H5460 `forráshiba` megjegyzése az F38.423-ban (`12779a2d`) van (az F38.424 üzenete tévesen említi); a H5920 forráskarakterszáma 37 656 (az F38.424 üzenete „34 660 karakteres”-t ír; a 34 660 a forrás-szócikk karakterszáma a szakasz-előkészítő kimenetében, a sorrendtábla karakter-oszlopa 37 656); az F38.425 üzenetében a `javitva` táblaérték backtick nélkül áll (az E30 figyelmeztetés a „javitva” ékezet nélküli írására vonatkozik; a táblaérték ékezet nélküli, az üzenetben backtickben kellett volna állnia).
