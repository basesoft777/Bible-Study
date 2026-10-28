# BDB_FORDITAS — a 10. adag (sorrend 1975–2821): tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 10. adagának szakaszonkénti fordítása (prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 10. adag (1975–2821, 847 szócikk, 499 390 forráskarakter). Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 1975 --adagok 1`: 848 szócikk, 848 Károli-pár). **Állapot: a sorrend 2196-ig kész (222 szócikk); hátra: 2197–2821 (625 szócikk).***

## 1. Tábla-Δ

| tábla | alap (`f3764787`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor nélkül) | 11049 | 12057 | +1008 | 1008 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 11051 | 12059 | +1008 | |
| `naplok/EMELES_munka.tsv` | — | — | +1008 | 1008 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | — | a javítóréteg 5_kisnagybetu cseréi (ha vannak) | `git diff --numstat` |
| minden más `adat/` tábla | — | — | 0 | — |

Törölt vagy módosított meglévő `forditasok.tsv`-sor nincs (0 törlés). `kezi` sorhoz nem nyúltam. Régi `teljes` sor egyik Strongnál sem volt (`--regi-elavult` nem kellett).

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor | forrás-karakter (`BDB_FORDITAS_sorrend.tsv` karakter-oszlop) |
|---|---|---|---|---|---|
| F38.411 | 1. szelet, 1. rész (sorrend 1975–2038) | 64 | 283 | 283 / 0 / 0 | 39125 |
| F38.412 | 1. szelet, 2. rész (a szelet lezárva) (sorrend 2039–2196) | 158 | 725 | 725 / 0 / 0 | 110906 |
| **össz.** | | **222** | **1008** | **1008 / 0 / 0** | **150031** |

Szeletek tervezett tartománya: 1. 1975–2196 (222 szócikk, 150 031 karakter); 2. 2197–2453 (150 495); 3. 2454–2734 (150 531); 4. 2735–2821 (48 333).

## 3. Strongok commitonként (sorrendben)

**F38.411** (1975–2038): H5273, H5409, H5576, H5700, H5732, H5992, H6382, H6441, H6496, H6711, H6854, H6901, H6922, H7031, H7064, H7280, H7349, H7394, H7425, H7456, H7481, H7613, H7690, H7722, H7751, H7822, H7910, H8203, H8316, H8372, H8481, H8593, H0030, H0041, H0062, H0130, H0155, H0471, H0771, H0831, H0934, H0936, H0947, H0994, H1156, H1187, H1271, H1420, H1522, H1538, H1593, H1677, H1889, H1904, H1908, H1928, H1988, H1994, H2023, H2078, H2147, H2183, H2194, H2270

**F38.412** (2039–2196): H2376, H2487, H2605, H2645, H2655, H2714, H2771, H2874, H2902, H2916, H3173, H3391, H3713, H3792, H3843, H3906, H3940, H4005, H4023, H4103, H4133, H4172, H4249, H4550, H4701, H4723, H4740, H4753, H4759, H4878, H4889, H4938, H4966, H4999, H5392, H5399, H5457, H5532, H5549, H5582, H5663, H5872, H5997, H6003, H6034, H6135, H6211, H6252, H6355, H6363, H6678, H6735, H6759, H6780, H6938, H6943, H7017, H7101, H7131, H7203, H7219, H7251, H7273, H7327, H7385, H7411, H7553, H7836, H8245, H8319, H8407, H8454, H8553, H0048, H0061, H0182, H0354, H0355, H0453, H0585, H0615, H0632, H0761, H0781, H0910, H0927, H0937, H1090, H1283, H1296, H1351, H1496, H1534, H1569, H1625, H1719, H1769, H1856, H1878, H1920, H2087, H2090, H2134, H2166, H2180, H2268, H2292, H2336, H2545, H2557, H2586, H2607, H2610, H2748, H2766, H2782, H2834, H2836, H2873, H2893, H2938, H3048, H3049, H3076, H3098, H3120, H3202, H3315, H3364, H3365, H3508, H3664, H3851, H3929, H4033, H4055, H4083, H4147, H4288, H4363, H4435, H4569, H4679, H4809, H5042, H5055, H5172, H5181, H5200, H5287, H5301, H5312, H5327, H5333, H5550, H5601, H5737, H5791

## 4. 17_bdb_javitas (DT55, #67 kapu)

A felsorolt Strongok közül egynek sincs olyan sora az `adat/bdb_igehely_javitas.tsv`-ben, amelyet a fordítás `Y [BDB: X]` jelöléssel érintene; a 17. kapu mindegyiknél RENDBEN („nincs javítótábla-sor”).

## 5. Kapu-felülbírálások (DT361)

| Strong | kapu | forrásidézet és indok |
|---|---|---|
| H7394 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 8_idezojel | forrás: "descended from „mmath, ⟦7⟧" (a „ OCR-maradvány, pár nélkül) ; hű fordítás: „mmathtól származnak. Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |
| H2938 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 5_terminologia | forrás: "Psa 34:9 taste ye and see that ⟦21⟧" (a see itt ige: lásd/nézd, nem utalás) ; hű: "ízleljétek és lássátok". Felülbírálás: `--kapu-felulir 5_terminologia --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |
| H5042 (mind a szakaszsor; a rögzítő eszköz felülbírálása Strong-szintű) | 5_terminologia | forrás: "belch forth, emphatic expression: ⟦13⟧ Prov 15:28" (az emphatic itt köznyelvi: nyomatékos, nem nyelvtani) ; hű: "nyomatékos kifejezés". Felülbírálás: `--kapu-felulir 5_terminologia --dontes DT361`; hű fordítás, nem cseréltem, nem töröltem. |

A kapuk egyéb elakadásai (5_terminologia: `p.` → `o.`, `suffix` → `suffixummal`, `proper name, of a people/location`; 11_konyvek: elmaradt vagy teljes alakban kiírt könyvnév, pl. `Ezekiel`, `Psalm`, `Joshua`, `2Mózes`) mind **valódi** megoldással, tartalmi változtatás nélkül, az egyszeri újrapróbálkozásban zárultak. Több kapu egyszerre egyik szócikknél sem bukott.

**Megjegyzés (forráshiba, nem javítótábla-sor):** a H5532 forrásában `Eccl 22:22t.` áll (nem létező fejezet; `adat/bdb_igehely_javitas.tsv`: javítás nincs, nincs jelölt); a fordítás hűen átveszi (`Préd 22:22t.`), `Y [BDB: X]` jelölés nélkül.


## 6. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (minden commit előtt).
- a három teszt a 10. adag végén fut.


*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ f3764787 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat` | ts=2026-10-28)*
