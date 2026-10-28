# BDB_FORDITAS — a 10. adag (sorrend 1975–2821): részleges bontás, tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 10. adagának szakaszonkénti fordítása (prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 10. adag (1975–2821, 847 szócikk, 499 390 forráskarakter). **Az adag nem készült el: ez a napló az 1975–2038. sorszámú részt (64 szócikk) rögzíti; a 2039–2821. sorszám (783 szócikk) fordítatlan marad, és új fordító sessionben folytatandó.** Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 1975 --adagok 1`: 848 szócikk, 848 Károli-pár).*

## 1. Tábla-Δ

| tábla | alap (`f3764787`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor nélkül) | 11 049 | 11 332 | +283 | 283 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 11 051 | 11 334 | +283 | |
| `naplok/EMELES_munka.tsv` | — | — | +283 | 283 / 0 |
| minden más `adat/` tábla | — | — | 0 | — |

Törölt vagy módosított meglévő `forditasok.tsv`-sor nincs (0 törlés). `kezi` sorhoz nem nyúltam. Régi `teljes` sor egyik Strongnál sem volt (`--regi-elavult` nem kellett).

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor | forrás-karakter (`BDB_FORDITAS_sorrend.tsv` karakter-oszlop) |
|---|---|---|---|---|---|
| F38.411 | 1. szelet, részleges (sorrend 1975–2038) | 64 | 283 | 283 / 0 / 0 | 39 125 |

Az 1. szelet tervezett tartománya 1975–2196 (222 szócikk, 150 031 karakter); ebből 1975–2038 készült el. A szelet nem zárult le, a többi szelet (2. 2197–2453; 3. 2454–2734; 4. 2735–2821) nem indult.

## 3. Strongok (1. szelet, részleges)

H5273, H5409, H5576, H5700, H5732, H5992, H6382, H6441, H6496, H6711, H6854, H6901, H6922, H7031, H7064, H7280, H7349, H7394, H7425, H7456, H7481, H7613, H7690, H7722, H7751, H7822, H7910, H8203, H8316, H8372, H8481, H8593, H0030, H0041, H0062, H0130, H0155, H0471, H0771, H0831, H0934, H0936, H0947, H0994, H1156, H1187, H1271, H1420, H1522, H1538, H1593, H1677, H1889, H1904, H1908, H1928, H1988, H1994, H2023, H2078, H2147, H2183, H2194, H2270 (sorrendben, 1975–2038).

## 4. 17_bdb_javitas (DT55, #67 kapu)

Az 1975–2038. sorszámú Strongok közül egynek sincs sora az `adat/bdb_igehely_javitas.tsv`-ben (és az adatblokk 6. szakasza egyiknél sem jelzett javított hivatkozást), ezért `Y [BDB: X]` jelölés nem keletkezett; a 17. kapu mindegyiknél RENDBEN („nincs javítótábla-sor”). A fennmaradó 783 szócikkre a vizsgálat még hátravan.

## 5. Kapu-felülbírálások (DT361)

| Strong / szakasz | kapu | forrásidézet | indok |
|---|---|---|---|
| H7394 — mind a 9 `forditas_hu` sor (sz1–sz9; a rögzítő eszköz kapuelnyomása Strong-szintű) | 8_idezojel | `are said to be descended from „mmath, ⟦7⟧` (sz4) | A forrásban a `„` (U+201E) pár nélküli OCR-maradvány (egy ʿ/ʿayin helyén); a kapu a forrás oldalán 0 párt, a fordítás oldalán 1 párt számol. A hű fordítás a jelet megtartja (`„mmathtól származnak`); nem cseréltem és nem töröltem a kapu kedvéért. Felülbírálás: `--kapu-felulir 8_idezojel --dontes DT361`. |

A kapuk egyéb elakadásai (5_terminologia: `p.` → `o.`, `suffix` → `suffixummal`, `proper name, of a location` → `tulajdonnév, helynév`; 11_konyvek: elmaradt vagy hibásan kiírt könyvnevek, pl. `Ezekiel 21:35`, `Psalm 60:14`, `Joshua 8:36`, `Hab 2:9` kimaradása) mind **valódi** megoldással, tartalmi változtatás nélkül, az egyszeri újrapróbálkozásban zárultak. Több kapu egyszerre egyik szócikknél sem bukott.

## 6. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS.
- `python eszkozok/teszt_forditas_kapuk.py`: OK (exit 0).
- `python eszkozok/teszt_emeles.py`: OK (exit 0).
- `python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py`: OK (exit 0).

*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ f3764787 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat` | ts=2026-10-28)*
