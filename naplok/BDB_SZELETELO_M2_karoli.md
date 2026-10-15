# F99 M2 — a Károli-oszlop gépi összevetése (vak minta, seed 99)

*Generálta: `eszkozok/olvaso_szerver/m2_karoli_ellenoriz.py` (csak olvas). A felhasználó döntése (2026-10-15, 5. pont): a Károli-oszlopot nem a vak ellenőr bírálja, hanem gépi összevetés a repó Károli-adatával. Proveniencia: `scope=adat/bdb_vers_jelentes.tsv + vak minta seed 99 | forras=TAHOT_kivonat.tsv (Igehely = Károli-vers, F85.6), Karoli_1908.tsv, Karoli_versmegfeleltetes.tsv | ts=2026-10-15`.*

## 1. A próba

A TAHOT `Igehely` kulcsa a Károli-vers, amelynek a héber szövegét a sor hordozza. Ha a szócikk Strong-száma a táblában álló Károli-vers TAHOT-sorai között van, a Károli-kulcs a héber szöveg szerint helyes („igen”). Ha nincs, a ±3 versnyi környezet TAHOT-találatai jelzik, hová kerülne. **Korlát:** a BDB szócikk és a TAHOT Strong-címkéje eltérhet (héber–arámi pár, homonima, H5920/H5921), ezért a „nem” nem bizonyított hiba, hanem vizsgálandó jel.

## 2. A teljes tábla (szűretlen, Károli-verses sorok)

| feloldás | TAHOT-ban a Strong a Károli-versen | nincs | arány |
|---|---:|---:|---:|
| atkulcsolt | 6211 | 1029 | 85.79% |
| azonos | 136467 | 13998 | 90.70% |
| azonos_f85 | 7 | 202 | 3.35% |
| **összesen** | 142685 | 15229 | 90.36% |

Fejezetenként rendszeres eltolás (a TAHOT-találat nélküli sorok közül legalább 20, amelyeknél a szomszédos vers hordozza a szót, egyirányú eltolással; ez a kulcsolás rendszerhibájának jele, nem a Strong-címkézésé):

| feloldás | fejezet | eltolás (Károli-vers + d) | sor | a fejezet találat nélküli sorai |
|---|---|---:|---:|---:|
| azonos_f85 | Ézs 3 | +1 | 181 | 202 |
| atkulcsolt | Hós 2 | -1 | 166 | 187 |
| azonos | Ézs 9 | +1 | 159 | 175 |
| atkulcsolt | 1Krón 12 | +1 | 78 | 98 |
| azonos | 2Móz 36 | -1 | 77 | 85 |
| atkulcsolt | Ézs 64 | -1 | 65 | 72 |
| azonos | 5Móz 5 | +3 | 54 | 74 |
| azonos | Én 6 | -3 | 52 | 75 |

A `nincs_karoli` okkódú (Károli-megfelelő nélküli, DT-F99a (3) a) szűretlen sorok, a TAHOT szerint:

| eset | sor |
|---|---:|
| azonos számú Károli-versen a TAHOT-ban | 719 |
| a ±3 versnyi környezetben a TAHOT-ban | 443 |
| a környezetben sincs | 117 |
| nincs azonos számú Károli-vers | 92 |

## 3. A vak minta (200 véletlen sor)

A mai tábla Károli-verse és a két kitöltés Károli-értéke („=” = az MT-vers) 188 sorban egyezik, 12 sorban tér el (a kulcs-üres sorokat is beleértve).

| azon | Strong | nyers | MT-vers | tábla Károli | feloldás | okkód | ellenőrök | TAHOT a táblai versen | TAHOT az ellenőri versen | TAHOT az MT-számon | versmegf. osztály |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M014 | H6524 | 92:13 | Zsolt 92:13 | Zsolt 92:13 | azonos |  | Zsolt 92:12 / — | igen | Zsolt 92:12: nem → Zsolt 92:13, Zsolt 92:14 | (= tábla) | MT |
| M027 | H2543 | Neh 7:68 | Neh 7:68 | Neh 7:68 | azonos | tobb_karoli_vers | ? / — | nem → Neh 7:69 | ?: nincs vers | (= tábla) | KJV |
| M029 | H8398 | Job 37:12 | Jób 37:12 | Jób 37:11 | atkulcsolt |  | Jób 37:12 / — | igen | Jób 37:12: nem → Jób 37:11 | nem → Jób 37:11 | — |
| M045 | H3885 | Job 17:2 | Jób 17:2 | — | nincs_karoli | nincs_karoli | Jób 17:2 / — | nincs vers | Jób 17:2: nem → Jób 17:1 | nem → Jób 17:1 | — |
| M098 | H3409 | Psa 45:4 | Zsolt 45:4 | Zsolt 45:4 | azonos |  | Zsolt 45:3 / — | igen | Zsolt 45:3: nem → Zsolt 45:4 | (= tábla) | MT |
| M102 | H3027 | Hosea 13:14 | Hós 13:14 | — | nincs_karoli | nincs_karoli | Hós 13:14 / — | nincs vers | Hós 13:14: igen | igen | — |
| M106 | H8548 | 51:5 | Zsolt 51:5 | Zsolt 51:5 | azonos |  | Zsolt 51:3 / — | igen | Zsolt 51:3: nem → Zsolt 51:5 | (= tábla) | MT |
| M112 | H8641 | , 6 | 2Móz 36:6 | — | nincs_karoli | nincs_karoli | 2Móz 36:6 / — | nincs vers | 2Móz 36:6: nem → 2Móz 36:5 | nem → 2Móz 36:5 | — |
| M119 | H3516 | Lam 2:11 | JSir 2:11 | Sir 2:11 | azonos |  | JSir 2:11 / — | igen | JSir 2:11: a Károliban nincs ilyen vers | a Károliban nincs ilyen vers | KJV |
| M145 | H7481 | Job 37:4 | Jób 37:4 | Jób 37:3 | atkulcsolt |  | — / Jób 37:4 | igen | Jób 37:4: igen | igen | — |
| M228 | H7620 | Tob 11:19 |  | — |  | nem_bibliai | — / - | nincs vers | -: nincs vers | (= tábla) | — |
| M230 | H3615 | Lam 3:32 | JSir 3:32 | Sir 3:32 | azonos |  | — / JSir 3:32 | nem → Sir 3:22 (fejezet) | JSir 3:32: a Károliban nincs ilyen vers | a Károliban nincs ilyen vers | KJV |
