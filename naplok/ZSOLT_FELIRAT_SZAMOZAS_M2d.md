# ZSOLT_FELIRAT_SZAMOZAS_M2d.md — az egyetlen felirat-halmaz (F91 E2)

*Végrehajtó: claude-sonnet-5-5. Mért adat. A repó `pardes.db`-je nem íródott felül: az előtte/utána méréshez két ideiglenes teljes építés készült (`sqlite_epit.py --mod teljes --kimenet <temp>`; elő = F91.13 builder, új = a mostani).*

Proveniencia: `scope=Zsolt 1–150 | forras=konkordancia/Karoli_1908.tsv + konkordancia/KJV_Strongs_teljes.tsv | ts=2026-10-14` · `scope=Zsolt, felirat-sorok | forras=konkordancia/Karoli_versmegfeleltetes.tsv | ts=2026-10-14` · `scope=Zsolt, karoli_ok | forras=konkordancia/LXX_OS/psalms-lxx.tsv | ts=2026-10-14` · `scope=pardes.db összes tábla, elo vs uj | forras=eszkozok/sqlite_epit.py (F91.13 vs F91.14) | ts=2026-10-14`

## 1. A definíció (felhasználói döntés, 2026-10-14)

Egyetlen halmaz, egy helyen: `eszkozok/zsolt_felirat_halmaz.py` (`felirat_versek()`, `felirat_d()`, önellenőrzés `onellenorzes()`). Kizárólag a `Karoli_1908.tsv` és a `KJV_Strongs_teljes.tsv` verszámaiból: zsoltáronként d = Károli-max − KJV-max; ahol d > 0, a felirat-versek `Zsolt c:1 … c:d`. Az egyetlen rögzített kivétel a Zsolt 13 (d = 1; a két maximum egyenlő, a KJV a 13:5-öt két versre bontja, az etalon szerint a 13:1 felirat-vers). **Nem** az A-táblából és **nem** az LXX_OS jelöléséből számol.

Önellenőrzés (`python eszkozok/zsolt_felirat_halmaz.py`): **67 vers, 63 zsoltár** (62 feliratos + Zsolt 13); d = 2: Zsolt 51, 52, 54, 60; d = 1: 59 (58 + Zsolt 13). Egyezik az M0.md mérésével.

## 2. Összevetés a két másik megjelöléssel

| | elemszám | a halmazhoz képest |
|---|---|---|
| halmaz (Károli+KJV) | 67 | — |
| A-tábla `felirat` megjegyzésű `Zsolt` sorai | 67 | **azonos** (0 különbség mindkét irányban) |
| LXX_OS `karoli_ok = zsolt_felirat_eltolas` (verskulcs, `igehely_karoli`) | 66 verskulcs (671 token) | a halmaz része; a halmazból **hiányzik** az LXX_OS jelöléséből: `Zsolt 13:1` (1 vers) |

Tehát a korábbi builder-szűrés pontosan a Zsolt 13:1-et nem zárta ki (ellenőr E2).

## 3. Hol használja a halmaz

| Fájl | Változás |
|---|---|
| `eszkozok/sqlite_epit.py` `_lxx_versszam` | a KJV-kulcs → Károli-átváltás kizárása `ig in ZFH.felirat_versek()` (előtte: `ok == 'zsolt_felirat_eltolas'`); a `lxx_versszam` sorai (az LXX_OS adatai, `megjegyzes`, `kjv_vers`) változatlanok |
| `eszkozok/f92_db_igazolas.py` | a 6. szakasz átváltási térképe a halmazzal szűr (SQL-ben nincs `megjegyzes`-szűrés); új ellenőrzés: a halmaz egyetlen versének sincs `terkep_ertek`-e (0); a várt számok újraszámolva: Károli-vers a térkép-értékkel 5 002 → **5 001**, ebből ÓSZ 5 002 → **5 001**, ebből LXX_OS-sal 4 907 → **4 906**, nem üres `terkep_ertek` 5 002 → **5 001** |
| `eszkozok/f91_versmegf_javit.py` | a d-értékeket (`dd`) és a kivételt a halmaz adja (a saját Károli/KJV-olvasó és az `etalon_d` kikerült); az LXX_OS-etalon csak az ÉRTÉKET adja. **A tábla bájtjai nem változnak** (l. 4.) |
| `eszkozok/teszt_sqlite_epit.py` | új `FeliratHalmaz` osztály, 3 teszt: a halmaz 67/63 és a d = 2 zsoltárok; az A-tábla `felirat` sorai = a halmaz; a minta-DB-ben a halmaz egyetlen versének sincs `terkep_ertek`-e |

Nem módosítva (jelzés): a `_nave_vers` (`sqlite_epit.py`, `lxx_kjv` szűrés `karoli_ok != 'zsolt_felirat_eltolas'`) továbbra is a jelölést használja. Mérés (ideiglenes építés a halmazra átírt `_nave_vers`-sel, a változat nem maradt a kódban): a `nave_vers` 156 214 sorából **1 sor** térne el (`forras_sor` 1966, NAVE-0130 „PRAYER IN”, `Zsolt 13:1-4` → a `Zsolt 13:1` vers-sor eltűnne). Ez viselkedésváltozás, ezért külön döntést/tételt kér (N-F91b területe: a Nave-újragenerálás).

## 4. Mérések

- **Javító és generátor:** a `f91_versmegf_javit.py` a halmazra átírva ugyanazt a `dd`-t adja (63 zsoltár, kivétel [13], d-értékek azonosak a régi számítással); a mostani táblán 0 módosuló sor, 0 etalon-eltérés. A KK4-generátor `KK4_KIMENET=<temp>`-mel futtatva **bájtra azonos** a repó `Karoli_versmegfeleltetes.tsv`-jével (`cmp`; sha256 `edd6b4578e7f30bd2025a09e486250be1568b60ccff6479a0c344306a52bb562`).
- **Ideiglenes DB-k elő vs új (a builder 73 táblát ír; mind összevetve):** két tábla tér el: `lxx_versszam` (**1 sor**) és `meta` (5 sor: időbélyeg, hash, + `terkep_karoli_kulcs` 5 002 → 5 001, `terkep_ot_vers`, `mindket_forras_verse` 4 907 → 4 906). Minden más tábla (köztük `nave_vers`, `normalizalas_jelentes`) bájtra azonos.
- **A kizárás utáni `terkep_ertek`-változás:** egyetlen vers, **Zsolt 13:1**: `Psa.12:1-2` → üres (a többi sor azonos; a `kjv_vers` `13:1` az LXX_OS adata, marad). A Zsolt 13:2 (KJV 13:1) `terkep_ertek`-e változatlan.
- **Tesztek:** `python eszkozok/teszt_sqlite_epit.py`: **64 teszt, OK** (61 + 3 új). `python eszkozok/ellenoriz.py`: RENDBEN 11 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 3 (változatlan). `python eszkozok/f92_db_igazolas.py --db <új.db>`: 0 `ELTÉRÉS` (az új sor: felirat-halmaz verse `terkep_ertek`-tel = 0, egyezik).
