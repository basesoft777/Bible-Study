# BDB_FORDITAS — a 10. adag (sorrend 1975–2821): tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 10. adagának szakaszonkénti fordítása (prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 10. adag (1975–2821, 847 szócikk, 499 390 forráskarakter). Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 1975 --adagok 1`: 848 szócikk, 848 Károli-pár). **Állapot: a sorrend 2466-ig kész (492 szócikk); hátra: 2467–2821 (355 szócikk).***

## 1. Tábla-Δ

| tábla | alap (`f3764787`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor nélkül) | 11049 | 13245 | +2196 | 2196 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 11051 | 13247 | +2196 | |
| `naplok/EMELES_munka.tsv` | — | — | +2196 | 2196 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | — | a javítóréteg 5_kisnagybetu cseréi (ha vannak) | `git diff --numstat` |
| minden más `adat/` tábla | — | — | 0 | — |

Törölt vagy módosított meglévő `forditasok.tsv`-sor nincs (0 törlés). `kezi` sorhoz nem nyúltam. Régi `teljes` sor egyik Strongnál sem volt (`--regi-elavult` nem kellett).

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor | forrás-karakter (`BDB_FORDITAS_sorrend.tsv` karakter-oszlop) |
|---|---|---|---|---|---|
| F38.411 | 1. szelet, 1. rész (sorrend 1975–2038) | 64 | 283 | 283 / 0 / 0 | 39125 |
| F38.412 | 1. szelet, 2. rész (a szelet lezárva) (sorrend 2039–2196) | 158 | 725 | 725 / 0 / 0 | 110906 |
| F38.413 | 2. szelet, 1. rész (sorrend 2197–2358) | 162 | 728 | 728 / 0 / 0 | 96846 |
| F38.414 | 2. szelet, 2. rész (sorrend 2359–2466) | 108 | 460 | 460 / 0 / 0 | 61243 |
| **össz.** | | **492** | **2196** | **2196 / 0 / 0** | **308120** |

Szeletek tervezett tartománya: 1. 1975–2196 (222 szócikk, 150 031 karakter); 2. 2197–2453 (150 495); 3. 2454–2734 (150 531); 4. 2735–2821 (48 333).

## 3. Strongok commitonként (sorrendben)

**F38.411** (1975–2038): H5273, H5409, H5576, H5700, H5732, H5992, H6382, H6441, H6496, H6711, H6854, H6901, H6922, H7031, H7064, H7280, H7349, H7394, H7425, H7456, H7481, H7613, H7690, H7722, H7751, H7822, H7910, H8203, H8316, H8372, H8481, H8593, H0030, H0041, H0062, H0130, H0155, H0471, H0771, H0831, H0934, H0936, H0947, H0994, H1156, H1187, H1271, H1420, H1522, H1538, H1593, H1677, H1889, H1904, H1908, H1928, H1988, H1994, H2023, H2078, H2147, H2183, H2194, H2270

**F38.412** (2039–2196): H2376, H2487, H2605, H2645, H2655, H2714, H2771, H2874, H2902, H2916, H3173, H3391, H3713, H3792, H3843, H3906, H3940, H4005, H4023, H4103, H4133, H4172, H4249, H4550, H4701, H4723, H4740, H4753, H4759, H4878, H4889, H4938, H4966, H4999, H5392, H5399, H5457, H5532, H5549, H5582, H5663, H5872, H5997, H6003, H6034, H6135, H6211, H6252, H6355, H6363, H6678, H6735, H6759, H6780, H6938, H6943, H7017, H7101, H7131, H7203, H7219, H7251, H7273, H7327, H7385, H7411, H7553, H7836, H8245, H8319, H8407, H8454, H8553, H0048, H0061, H0182, H0354, H0355, H0453, H0585, H0615, H0632, H0761, H0781, H0910, H0927, H0937, H1090, H1283, H1296, H1351, H1496, H1534, H1569, H1625, H1719, H1769, H1856, H1878, H1920, H2087, H2090, H2134, H2166, H2180, H2268, H2292, H2336, H2545, H2557, H2586, H2607, H2610, H2748, H2766, H2782, H2834, H2836, H2873, H2893, H2938, H3048, H3049, H3076, H3098, H3120, H3202, H3315, H3364, H3365, H3508, H3664, H3851, H3929, H4033, H4055, H4083, H4147, H4288, H4363, H4435, H4569, H4679, H4809, H5042, H5055, H5172, H5181, H5200, H5287, H5301, H5312, H5327, H5333, H5550, H5601, H5737, H5791

**F38.413** (2197–2358): H5810, H5813, H5998, H6049, H6116, H6141, H6175, H6194, H6290, H6307, H6492, H6603, H6616, H6631, H6693, H6765, H6936, H6939, H7073, H7081, H7123, H7144, H7247, H7306, H7308, H7467, H7526, H7554, H7623, H7677, H7718, H7752, H7757, H7775, H8068, H8154, H8263, H8484, H8487, H8532, H8585, H0107, H0119, H0213, H0231, H0357, H0375, H0447, H0564, H0653, H0672, H0744, H0861, H0919, H0961, H1062, H1091, H1160, H1177, H1328, H1331, H1358, H1367, H1443, H1463, H1558, H1602, H1642, H1663, H1683, H1867, H1885, H2048, H2060, H2102, H2128, H2139, H2213, H2318, H2504, H2527, H2529, H2720, H2787, H2883, H3002, H3062, H3078, H3334, H3395, H3504, H3524, H3543, H3608, H3774, H3857, H4066, H4465, H4471, H4479, H4565, H4635, H4673, H4688, H4743, H4745, H4830, H4916, H5000, H5064, H5095, H5144, H5176, H5177, H5374, H5402, H5571, H5606, H5710, H5714, H5744, H5903, H5943, H5989, H6026, H6147, H6158, H6210, H6340, H6347, H6354, H6388, H6399, H6418, H6501, H6561, H6634, H6770, H6790, H6846, H6872, H6881, H6914, H6931, H7025, H7054, H7075, H7158, H7165, H7239, H7340, H7600, H7649, H7652, H7935, H7990, H8018, H8082, H8307, H8362, H8396, H8544

**F38.414** (2359–2466): H0002, H0073, H0098, H0122, H0164, H0324, H0411, H0436, H0454, H0467, H0481, H0551, H0605, H0652, H0663, H0699, H0728, H0775, H0811, H0838, H0863, H0883, H1119, H1196, H1212, H1238, H1343, H1404, H1448, H1524, H1541, H1603, H1607, H1617, H1650, H1681, H1809, H1814, H1846, H1909, H2069, H2184, H2230, H2384, H2404, H2635, H2648, H2660, H2731, H2767, H2795, H2966, H3039, H3096, H3103, H3148, H3218, H3257, H3266, H3286, H3324, H3336, H3344, H3463, H3500, H3503, H3528, H3564, H3734, H3767, H3800, H3948, H4102, H4181, H4340, H4385, H4468, H4585, H4627, H4719, H4749, H4865, H4902, H4959, H5086, H5154, H5174, H5201, H5253, H5348, H5371, H5408, H5429, H5445, H5480, H5709, H5718, H5736, H5777, H5835, H5977, H6001, H6006, H6009, H6061, H6064, H6079, H6157

## 4. 17_bdb_javitas (DT55, #67 kapu)

A felsorolt Strongok közül egynek sincs olyan sora az `adat/bdb_igehely_javitas.tsv`-ben, amelyet a fordítás `Y [BDB: X]` jelöléssel érintene; a 17. kapu mindegyiknél RENDBEN („nincs javítótábla-sor”).

## 5. Kapu-felülbírálások (DT361)

| Strong | kapu | forrásidézet és indok |
|---|---|---|
| H7394 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "descended from „mmath, ⟦7⟧" (a „ OCR-maradvány, pár nélkül) ; hű fordítás: „mmathtól származnak. Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |
| H2938 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 5_terminologia | forrás: "Psa 34:9 taste ye and see that ⟦21⟧" (a see itt ige: lásd/nézd, nem utalás) ; hű: "ízleljétek és lássátok". Felülbírálás: `--kapu-felulir 5_terminologia --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |
| H5042 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 5_terminologia | forrás: "belch forth, emphatic expression: ⟦13⟧ Prov 15:28" (az emphatic itt köznyelvi: nyomatékos, nem nyelvtani) ; hű: "nyomatékos kifejezés". Felülbírálás: `--kapu-felulir 5_terminologia --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |
| H0231 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 9_tagolas | forrás: "Exod 12:22 (J) ⟦8⟧ a bunch of h. for sprinkling blood" (a h. a hyssop rövidítése, nem tagolójel) ; hű: "egy csokor izsóp". Felülbírálás: `--kapu-felulir 9_tagolas --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |
| H4719 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 11_konyvek | forrás: "captured by Joshua 10:28" (a Joshua itt személy, Józsué, nem könyvnév) ; hű: "Józsué elfoglalta 10:28". Felülbírálás: `--kapu-felulir 11_konyvek --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |

A kapuk egyéb elakadásai (5_terminologia: `p.` → `o.`, `suffix` → `suffixummal`, `proper name, of a people/location`; 11_konyvek: elmaradt vagy teljes alakban kiírt könyvnév, pl. `Ezekiel`, `Psalm`, `Joshua`, `2Mózes`) mind **valódi** megoldással, tartalmi változtatás nélkül, az egyszeri újrapróbálkozásban zárultak. Több kapu egyszerre egyik szócikknél sem bukott.

**Megjegyzés (forráshiba, nem javítótábla-sor):** a H5532 forrásában `Eccl 22:22t.` áll (nem létező fejezet; `adat/bdb_igehely_javitas.tsv`: javítás nincs, nincs jelölt); a fordítás hűen átveszi (`Préd 22:22t.`), `Y [BDB: X]` jelölés nélkül.

**Megjegyzés (forráshiba, nem javítótábla-sor):** a H5710 forrásában `Prov 38:19` áll (nem létező fejezet; `adat/bdb_igehely_javitas.tsv`: javítás nincs, nincs jelölt); a fordítás hűen átveszi (`Péld 38:19`), `Y [BDB: X]` jelölés nélkül; a 13. kapu JELZÉS-t ad.

**Megjegyzés (forráshiba, nem javítótábla-sor):** a H6881 forrásában `Dan 19:41` áll (nem létező fejezet; javítás nincs, nincs jelölt); a fordítás hűen átveszi (`Dán 19:41`), `Y [BDB: X]` jelölés nélkül.


## 6. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (minden commit előtt).
- a három teszt a 10. adag végén fut.


*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ f3764787 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat` | ts=2026-10-28)*
