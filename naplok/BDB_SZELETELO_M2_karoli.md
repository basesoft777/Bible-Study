# F99 M2 — a Károli-oszlop gépi összevetése (vak minta, seed 99)

*Generálta: `eszkozok/olvaso_szerver/m2_karoli_ellenoriz.py` (csak olvas). A felhasználó döntése (2026-10-15, 5. pont): a Károli-oszlopot nem a vak ellenőr bírálja, hanem gépi összevetés a repó Károli-adatával. Proveniencia: `scope=adat/bdb_vers_jelentes.tsv + vak minta seed 99 | forras=TAHOT_kivonat.tsv (Igehely = Károli-vers, F85.6), Karoli_1908.tsv, Karoli_versmegfeleltetes.tsv | ts=2026-10-15`.*

## 1. A próba

A TAHOT `Igehely` kulcsa a Károli-vers, amelynek a héber szövegét a sor hordozza. Ha a szócikk Strong-száma a táblában álló Károli-vers TAHOT-sorai között van, a Károli-kulcs a héber szöveg szerint helyes („igen”). Ha nincs, a ±3 versnyi környezet TAHOT-találatai jelzik, hová kerülne. **Korlát:** a BDB szócikk és a TAHOT Strong-címkéje eltérhet (héber–arámi pár, homonima, H5920/H5921), ezért a „nem” nem bizonyított hiba, hanem vizsgálandó jel.

## 2. A teljes tábla (szűretlen, Károli-verses sorok)

| feloldás | TAHOT-ban a Strong a Károli-versen | nincs | arány |
|---|---:|---:|---:|
| atkulcsolt | 5383 | 698 | 88.52% |
| atkulcsolt_f85 | 2619 | 373 | 87.53% |
| azonos | 136172 | 13391 | 91.05% |
| azonos_tahot | 551 | 0 | 100.00% |
| **összesen** | 144725 | 14462 | 90.92% |

Fejezetenként rendszeres eltolás (a TAHOT-találat nélküli sorok közül legalább 20, amelyeknél a szomszédos vers hordozza a szót, egyirányú eltolással; ez a kulcsolás rendszerhibájának jele, nem a Strong-címkézésé):

| feloldás | fejezet | eltolás (Károli-vers + d) | sor | a fejezet találat nélküli sorai |
|---|---|---:|---:|---:|
| atkulcsolt | 1Krón 12 | +1 | 78 | 98 |
| azonos | 5Móz 5 | +3 | 54 | 74 |

A `nincs_karoli` okkódú (Károli-megfelelő nélküli, DT-F99a (3) a) szűretlen sorok, a TAHOT szerint:

| eset | sor |
|---|---:|
| a ±3 versnyi környezetben a TAHOT-ban | 134 |
| a környezetben sincs | 54 |
| nincs azonos számú Károli-vers | 13 |

## 3. A vak minta (200 véletlen sor)

A mai tábla Károli-verse és a két kitöltés Károli-értéke („=” = az MT-vers) 189 sorban egyezik, 11 sorban tér el (a kulcs-üres sorokat is beleértve).

| azon | Strong | nyers | MT-vers | tábla Károli | feloldás | okkód | ellenőrök | TAHOT a táblai versen | TAHOT az ellenőri versen | TAHOT az MT-számon | versmegf. osztály |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M014 | H6524 | 92:13 | Zsolt 92:13 | Zsolt 92:13 | azonos |  | Zsolt 92:12 / — | igen | Zsolt 92:12: nem → Zsolt 92:13, Zsolt 92:14 | (= tábla) | MT |
| M027 | H2543 | Neh 7:68 | Neh 7:68 | Neh 7:68 | azonos | tobb_karoli_vers | ? / — | nem → Neh 7:69 | ?: nincs vers | (= tábla) | KJV |
| M029 | H8398 | Job 37:12 | Jób 37:12 | Jób 37:11 | atkulcsolt_f85 |  | Jób 37:12 / — | igen | Jób 37:12: nem → Jób 37:11 | nem → Jób 37:11 | — |
| M045 | H3885 | Job 17:2 | Jób 17:2 | Jób 17:1 | atkulcsolt_f85 |  | Jób 17:2 / — | igen | Jób 17:2: nem → Jób 17:1 | nem → Jób 17:1 | — |
| M098 | H3409 | Psa 45:4 | Zsolt 45:4 | Zsolt 45:4 | azonos |  | Zsolt 45:3 / — | igen | Zsolt 45:3: nem → Zsolt 45:4 | (= tábla) | MT |
| M102 | H3027 | Hosea 13:14 | Hós 13:14 | Hós 13:14 | azonos_tahot | karoli_tahot | Hós 13:14 / — | igen | — | (= tábla) | — |
| M106 | H8548 | 51:5 | Zsolt 51:5 | Zsolt 51:5 | azonos |  | Zsolt 51:3 / — | igen | Zsolt 51:3: nem → Zsolt 51:5 | (= tábla) | MT |
| M112 | H8641 | , 6 | 2Móz 36:6 | 2Móz 36:5 | atkulcsolt_f85 |  | 2Móz 36:6 / — | igen | 2Móz 36:6: nem → 2Móz 36:5 | nem → 2Móz 36:5 | — |
| M119 | H3516 | Lam 2:11 | JSir 2:11 | Sir 2:11 | azonos |  | JSir 2:11 / — | igen | JSir 2:11: a Károliban nincs ilyen vers | a Károliban nincs ilyen vers | KJV |
| M145 | H7481 | Job 37:4 | Jób 37:4 | Jób 37:3 | atkulcsolt_f85 |  | — / Jób 37:4 | igen | Jób 37:4: igen | igen | — |
| M228 | H7620 | Tob 11:19 |  | — |  | nem_bibliai | — / - | nincs vers | -: nincs vers | (= tábla) | — |
| M230 | H3615 | Lam 3:32 | JSir 3:32 | Sir 3:32 | azonos |  | — / JSir 3:32 | nem → Sir 3:22 (fejezet) | JSir 3:32: a Károliban nincs ilyen vers | a Károliban nincs ilyen vers | KJV |
