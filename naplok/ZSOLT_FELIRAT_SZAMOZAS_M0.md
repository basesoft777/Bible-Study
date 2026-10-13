# ZSOLT_FELIRAT_SZAMOZAS_M0.md — a feliratos zsoltárok számozásának felmérése (F91 M0)

*Gép által generált (`eszkozok/zsolt_felirat_felmeres.py`), csak olvas; kézzel nem szerkesztendő. Mért adat, nem becslés.*

## 1. Módszer

- **Felirat-hossz** `d` = Károli-maximumvers − KJV-maximumvers zsoltáronként. Okfejtés: a Károli az MT szerint számoz (a felirat számozott vers); a KJV a feliratot nem számozza. Ahol a két maximum azonos, a Károli és a KJV számozása egyezik.
- **Etalon:** az `LXX_OS/psalms-lxx.tsv` Károli-kulcsa (`igehely_karoli` ↔ `igehely_kjv`, F54, `karoli_ok = zsolt_felirat_eltolas` a feliratversekre, `mt_szamozas_kovetes` a többire). Az etalon KJV-oszlopa a KJV-szöveggel egyező (verse_pairs.jsonl TVTMS-alapú MT–KJV kulcs); a felirat-versek KJV-célja duplikált (a felirat a következő KJV-verssel közös célra mutat), ezért a felirat-verseket a `d` alapján, nem az etalon KJV-oszlopa alapján azonosítom.
- **Független KJV-hossz:** `KJV_Strongs_teljes.tsv` (eBible) különböző versszáma fejezetenként.
- **A tábla** = `Karoli_versmegfeleltetes.tsv` (Károli → `igehely_kjv`). Várt: `v ≤ d` felirat → nincs KJV-vers; `v > d` → KJV `v − d`. Hibás: felirat-versre van KJV-érték (`A_fel`); vagy `v > d` és az érték ≠ `v − d` (`A_hibas`).
- **B tábla** = `LXX_versificacios_terkep.tsv` (Károli → `Heber_vers`). Mivel a Károli az MT-számozást követi, a várt Héber-halmaz egyetlen elem: a vers maga. Hibás (`B_hibas`): a Károli-vers sorainak Héber-halmaz-uniója ≠ {v}.

Proveniencia: `scope=Zsolt 1–150 | forras=konkordancia/Karoli_1908.tsv | ts=2026-10-13T18:39Z` · `scope=Zsolt 1–150 | forras=konkordancia/TAHOT_kivonat.tsv | ts=2026-10-13T18:39Z` · `scope=Zsolt 1–150 | forras=konkordancia/KJV_Strongs_teljes.tsv | ts=2026-10-13T18:39Z` · `scope=Zsolt 1–150 | forras=konkordancia/LXX_OS/psalms-lxx.tsv | ts=2026-10-13T18:39Z` · `scope=Zsolt 1–150 | forras=konkordancia/Karoli_versmegfeleltetes.tsv | ts=2026-10-13T18:39Z` · `scope=Zsolt 1–150 | forras=konkordancia/LXX_versificacios_terkep.tsv | ts=2026-10-13T18:39Z` · `scope=Zsolt 1–150 | forras=konkordancia/Nave_basokant.tsv | ts=2026-10-13T18:39Z`

## 2. Fő számok

- Zsoltárfejezet összesen: 150.
- Feliratos (`d > 0`): **62**; ebből `d = 1`: 58, `d = 2`: 4, más: 0.
- Nem feliratos (`d = 0`, Károli = KJV): 88; `d < 0` (Károli rövidebb): 0.
- A tábla hibás vers (Károli v > d, érték ≠ v − d): 917; feliratversre adott KJV-érték: 66; A-ban hiányzó Károli-vers: 0.
- B tábla hibás Károli-vers (Héber-halmaz ≠ {v}): 995; B-ben hiányzó Károli-vers: 107.
- A tábla közvetlen ellentmondása az etalon KJV-oszlopával (egyértelmű etalon-soron): 925 vers.
- Károli-max ≠ TAHOT-max (a TAHOT-kulcs F85.6 óta Károli-kulcsú): 0 zsoltár.
- Az etalon alapján kivétel-jelölt (d = 0 a maximumok szerint, mégis eltolt): Zsolt 13.
- Összes érintett zsoltár (feliratos + kivétel): 63.
- **Zsolt 22:** d = 1, Károli 32 vers, KJV 31 vers; A_hibas = 30, A_fel = 1, A vs etalon = 30, B_hibas = 31.

## 3. Zsoltáronkénti táblázat (csak a feliratos zsoltárok, `d > 0`)

| Zsolt | Károli max | KJV max | TAHOT max | d | etalon d | A_hibas | A_fel | A_hiany | A vs etalon | B_hibas | B_hiany | v1 kezdete |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 9 | 8 | 9 | 1 | 1 | 7 | 1 | 0 | 7 | 8 | 1 | Dávid zsoltára; fia, Absolon elől való f |
| 4 | 9 | 8 | 9 | 1 | 1 | 7 | 1 | 0 | 7 | 8 | 1 | Az éneklőmesternek a neginóthra, Dávid z |
| 5 | 13 | 12 | 13 | 1 | 1 | 11 | 1 | 0 | 11 | 12 | 1 | Az éneklőmesternek a nehilótra, Dávid zs |
| 6 | 11 | 10 | 11 | 1 | 1 | 9 | 1 | 0 | 9 | 10 | 1 | Az éneklőmesternek a neginóthra, a semin |
| 7 | 18 | 17 | 18 | 1 | 1 | 16 | 1 | 0 | 16 | 17 | 1 | Dávid siggajonja, a melyet az Úrhoz ének |
| 8 | 10 | 9 | 10 | 1 | 1 | 8 | 1 | 0 | 8 | 9 | 1 | Az éneklőmesternek a gittithre; Dávid zs |
| 9 | 21 | 20 | 21 | 1 | 1 | 19 | 1 | 0 | 19 | 20 | 1 | Az éneklőmesternek a múthlabbén szerint; |
| 12 | 9 | 8 | 9 | 1 | 1 | 7 | 1 | 0 | 7 | 8 | 1 | Az éneklőmesternek a seminithre; Dávid z |
| 18 | 51 | 50 | 51 | 1 | 1 | 49 | 1 | 0 | 49 | 50 | 1 | Az éneklőmesternek, az Úr szolgájától, D |
| 19 | 15 | 14 | 15 | 1 | 1 | 13 | 1 | 0 | 13 | 14 | 1 | Az éneklőmesternek; Dávid zsoltára. |
| 20 | 10 | 9 | 10 | 1 | 1 | 8 | 1 | 0 | 8 | 9 | 1 | Az éneklőmesternek; Dávid zsoltára. |
| 21 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek; Dávid zsoltára. |
| 22 | 32 | 31 | 32 | 1 | 1 | 30 | 1 | 0 | 30 | 31 | 1 | Az éneklőmesternek az ajjelethassakhar s |
| 30 | 13 | 12 | 13 | 1 | 1 | 11 | 1 | 0 | 11 | 12 | 1 | Dávid zsoltára. Templomszentelési ének. |
| 31 | 25 | 24 | 25 | 1 | 1 | 23 | 1 | 0 | 23 | 24 | 1 | Az éneklőmesternek, Dávid zsoltára. |
| 34 | 23 | 22 | 23 | 1 | 1 | 21 | 1 | 0 | 21 | 22 | 1 | Dávidé, mikor elváltoztatta értelmét Abi |
| 36 | 13 | 12 | 13 | 1 | 1 | 11 | 1 | 0 | 11 | 12 | 1 | Az éneklőmesternek; az Úr szolgájáé, Dáv |
| 38 | 23 | 22 | 23 | 1 | 1 | 21 | 1 | 0 | 21 | 22 | 1 | Dávid zsoltára emlékeztetőül. |
| 39 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek Jeduthunnak, Dávid zs |
| 40 | 18 | 17 | 18 | 1 | 1 | 16 | 1 | 0 | 16 | 17 | 1 | Az éneklőmesternek; Dávid zsoltára. |
| 41 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek; Dávid zsoltára. |
| 42 | 12 | 11 | 12 | 1 | 1 | 10 | 1 | 0 | 10 | 11 | 1 | Az éneklőmesternek; Kóráh fiainak tanítá |
| 44 | 27 | 26 | 27 | 1 | 1 | 25 | 1 | 0 | 25 | 26 | 1 | Az éneklőmesternek; a Kóráh fiainak taní |
| 45 | 18 | 17 | 18 | 1 | 1 | 16 | 1 | 0 | 16 | 17 | 1 | Az éneklőmesternek a sosannimra, Kóráh f |
| 46 | 12 | 11 | 12 | 1 | 1 | 10 | 1 | 0 | 10 | 11 | 1 | Az éneklőmesternek, a Kóráh fiainak ének |
| 47 | 10 | 9 | 10 | 1 | 1 | 8 | 1 | 0 | 8 | 9 | 1 | Az éneklőmesternek, a Kóráh fiainak zsol |
| 48 | 15 | 14 | 15 | 1 | 1 | 13 | 1 | 0 | 13 | 14 | 1 | A Kóráh fiainak zsoltáréneke. |
| 49 | 21 | 20 | 21 | 1 | 1 | 19 | 1 | 0 | 19 | 20 | 1 | Az éneklőmesternek, a Kóráh fiainak zsol |
| 51 | 21 | 19 | 21 | 2 | 2 | 17 | 2 | 0 | 18 | 19 | 2 | Az éneklőmesternek; Dávid zsoltára; |
| 52 | 11 | 9 | 11 | 2 | 2 | 7 | 2 | 0 | 8 | 9 | 2 | Az éneklőmesternek; Dávid tanítása; |
| 53 | 7 | 6 | 7 | 1 | 1 | 5 | 1 | 0 | 5 | 6 | 1 | Az éneklőmesternek a mahalathra, Dávid t |
| 54 | 9 | 7 | 9 | 2 | 2 | 5 | 2 | 0 | 6 | 7 | 2 | Az éneklőmesternek, hangszerekkel; Dávid |
| 55 | 24 | 23 | 24 | 1 | 1 | 22 | 1 | 0 | 22 | 23 | 1 | Az éneklőmesternek, hangszerekkel; Dávid |
| 56 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek a Jónathelem rehokimr |
| 57 | 12 | 11 | 12 | 1 | 1 | 10 | 1 | 0 | 10 | 11 | 1 | Az éneklőmesternek az altashétre; Dávid  |
| 58 | 12 | 11 | 12 | 1 | 1 | 10 | 1 | 0 | 10 | 11 | 1 | Az éneklőmesternek az altashétre; Dávid  |
| 59 | 18 | 17 | 18 | 1 | 1 | 16 | 1 | 0 | 16 | 17 | 1 | Az éneklőmesternek az altashétre. Dávid  |
| 60 | 14 | 12 | 14 | 2 | 2 | 10 | 2 | 0 | 11 | 12 | 2 | Az éneklőmesternek a susanheduthra, Dávi |
| 61 | 9 | 8 | 9 | 1 | 1 | 7 | 1 | 0 | 7 | 8 | 1 | Az éneklőmesternek hangszerre: Dávidé. |
| 62 | 13 | 12 | 13 | 1 | 1 | 11 | 1 | 0 | 11 | 12 | 1 | Az éneklőmesternek, Jedutun szerint; Dáv |
| 63 | 12 | 11 | 12 | 1 | 1 | 10 | 1 | 0 | 10 | 11 | 1 | Dávid zsoltára, mikor a Júda pusztájában |
| 64 | 11 | 10 | 11 | 1 | 1 | 9 | 1 | 0 | 9 | 10 | 1 | Az éneklőmesternek; Dávid zsoltára. |
| 65 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek; zsoltár; Dávid éneke |
| 67 | 8 | 7 | 8 | 1 | 1 | 6 | 1 | 0 | 6 | 7 | 1 | Az éneklőmesternek, hangszerekkel; zsolt |
| 68 | 36 | 35 | 36 | 1 | 1 | 34 | 1 | 0 | 34 | 35 | 1 | Az éneklőmesternek; Dávid zsoltára, ének |
| 69 | 37 | 36 | 37 | 1 | 1 | 35 | 1 | 0 | 35 | 36 | 1 | Az éneklőmesternek a sósannimra; Dávidé. |
| 70 | 6 | 5 | 6 | 1 | 1 | 4 | 1 | 0 | 4 | 5 | 1 | Az éneklőmesternek, Dávidtól, emlékeztet |
| 75 | 11 | 10 | 11 | 1 | 1 | 9 | 1 | 0 | 9 | 10 | 1 | Az éneklőmesternek, az altashétre, Aszáf |
| 76 | 13 | 12 | 13 | 1 | 1 | 11 | 1 | 0 | 11 | 12 | 1 | Az éneklőmesternek hangszerekkel; Aszáf  |
| 77 | 21 | 20 | 21 | 1 | 1 | 19 | 1 | 0 | 19 | 20 | 1 | Az éneklőmesternek, Jedutunnak; Aszáfé,  |
| 80 | 20 | 19 | 20 | 1 | 1 | 18 | 1 | 0 | 18 | 19 | 1 | Az éneklőmesternek a sosannim-éduthra; A |
| 81 | 17 | 16 | 17 | 1 | 1 | 15 | 1 | 0 | 15 | 16 | 1 | Az éneklőmesternek, a gittithre. Aszáfé. |
| 83 | 19 | 18 | 19 | 1 | 1 | 17 | 1 | 0 | 17 | 18 | 1 | Ének; Aszáf zsoltára. |
| 84 | 13 | 12 | 13 | 1 | 1 | 11 | 1 | 0 | 11 | 12 | 1 | Az éneklőmesternek, a gittitre; Kóráh fi |
| 85 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek, Kóráh fiainak zsoltá |
| 88 | 19 | 18 | 19 | 1 | 1 | 17 | 1 | 0 | 17 | 18 | 1 | Ének. A Kóráh fiainak zsoltára. Az énekl |
| 89 | 53 | 52 | 53 | 1 | 1 | 51 | 1 | 0 | 51 | 52 | 1 | Az Ezrahita Ethán tanítása. |
| 92 | 16 | 15 | 16 | 1 | 1 | 14 | 1 | 0 | 14 | 15 | 1 | Zsoltár, ének szombat napra. |
| 102 | 29 | 28 | 29 | 1 | 1 | 27 | 1 | 0 | 27 | 28 | 1 | A nyomorultnak imádsága, a mikor eleped  |
| 108 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Ének. Dávid zsoltára. |
| 140 | 14 | 13 | 14 | 1 | 1 | 12 | 1 | 0 | 12 | 13 | 1 | Az éneklőmesternek, Dávid zsoltára. |
| 142 | 8 | 7 | 8 | 1 | 1 | 6 | 1 | 0 | 6 | 7 | 1 | Dávid tanítása; imádság a barlangban lét |

## 4. Nem feliratos zsoltárok, amelyeknél a mérés mégis eltérést jelez (`d = 0`, de hibás sor van, vagy az etalon más `d`-t ad)

- Zsolt 1: Károli 6, KJV 6, TAHOT 6, etalon d = 0, A_hibas 0, A_hiany 0, B_hibas 6, B_hiany 0, A vs etalon 0
- Zsolt 2: Károli 12, KJV 12, TAHOT 12, etalon d = 0, A_hibas 0, A_hiany 0, B_hibas 0, B_hiany 11, A vs etalon 0
- Zsolt 13: Károli 6, KJV 6, TAHOT 6, etalon d = 1, A_hibas 0, A_hiany 0, B_hibas 5, B_hiany 0, A vs etalon 4
- Zsolt 37: Károli 40, KJV 40, TAHOT 40, etalon d = 0, A_hibas 0, A_hiany 0, B_hibas 1, B_hiany 1, A vs etalon 0
- Zsolt 148: Károli 14, KJV 14, TAHOT 14, etalon d = 0, A_hibas 0, A_hiany 0, B_hibas 0, B_hiany 14, A vs etalon 0
- Zsolt 149: Károli 9, KJV 9, TAHOT 9, etalon d = 0, A_hibas 0, A_hiany 0, B_hibas 0, B_hiany 9, A vs etalon 0
- Zsolt 150: Károli 6, KJV 6, TAHOT 6, etalon d = 0, A_hibas 0, A_hiany 0, B_hibas 0, B_hiany 6, A vs etalon 0

## 5. Etalon és a független `d` összevetése

Az etalon legnagyobb eltolása (`etalon d`) és a Károli−KJV maximum-különbség (`d`) eltér 1 zsoltárban: Zsolt 13 (d=0, etalon=1)

Az etalon KJV-oszlopa eltér a `d`-szabálytól (Károli v → KJV v−d), vagyis kivétel-jelölt (v → KJV-vers; több KJV-vers = a KJV két verse egy Károli-versben):

- Zsolt 13 (d = 0, etalon d = 1): 2->1, 3->2, 4->3, 5->4

## 6. Nave `karoli_allapot` (csak a Zsoltárok vers-szintű sorai)

| feliratos fejezet | karoli_allapot | igehely_karoli |  sor |
|---|---|---|---|
| False | azonos | karoli_ures | 3088 |
| True | azonos | karoli_ures | 2036 |
| nem_vers:fejezet | fejezet |  | 425 |
| nem_vers:tartomany | tartomany |  | 639 |

Minta feliratos fejezet sorokból (igehely, karoli_allapot, igehely_karoli): ('Zsolt 77:20', 'azonos', ''); ('Zsolt 51:2', 'azonos', ''); ('Zsolt 51:7', 'azonos', '')

