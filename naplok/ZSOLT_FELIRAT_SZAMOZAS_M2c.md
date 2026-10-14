# ZSOLT_FELIRAT_SZAMOZAS_M2c.md — a B-oldali M2: a térkép `KJV_igehely` oszlopa, a builder KJV-kulcson illeszt (F91, DT-F91b)

*Végrehajtó: claude-sonnet-5-5. Mért adat. A `pardes.db` (938 MB, nem verziózott) nem lett felülírva: az előtte/utána méréshez két ideiglenes teljes építés készült (`sqlite_epit.py --mod teljes --kimenet <temp>`), ugyanazon A-tábla (A1 utáni) mellett, csak a builder + a térkép oszlopneve különbözik.*

Proveniencia: `scope=teljes ÓSZ, lxx_versszam | forras=konkordancia/LXX_versificacios_terkep.tsv + konkordancia/LXX_OS/*.tsv + konkordancia/Karoli_versmegfeleltetes.tsv | ts=2026-10-14` · `scope=pardes.db összes tábla, elo.db vs uj.db | forras=eszkozok/sqlite_epit.py (HEAD vs F91.12) | ts=2026-10-14`

## 1. Változtatások

| Fájl | Változás |
|---|---|
| `konkordancia/LXX_versificacios_terkep.tsv` | fejléc: `Karoli_igehely` → `KJV_igehely`; az értékek, a sorok száma (5 426) és minden más sor bájtra azonos (a fájl 3 bájttal rövidebb: csak a fejléc) |
| `eszkozok/sqlite_epit.py` `_lxx_versszam` | a térkép `r['KJV_igehely']`-t olvassa; a KJV-kulcs → Károli-vers(ek) átváltás: (1) az LXX_OS `igehely_kjv`-je (`os_par`; a `zsolt_felirat_eltolas` sorok kihagyva: a felirat-versnek nincs KJV-megfelelője, mint az A-táblában és a `_nave_vers`-ben), (2) a javított A-tábla `igehely_kjv`-je; a `terkep_ertek` Károli-kulcsos marad; a nem átváltható KJV-kulcs a `normalizalas_jelentes`-ben (`a térkép KJV-kulcsához nincs Károli-vers`) |
| meta-kulcsok | új: `lxx_versszam:terkep_kjv_kulcs` (5 204), `terkep_kjv_kulcs_karoli_nelkul` (203); megszűnt: `terkep_nem_karoli_kulcs`; megmaradt (új jelentéssel: Károli-vers, amelyhez térkép-érték kerül): `terkep_karoli_kulcs`, `terkep_ot_vers`, `terkep_nem_ot_vers` |
| `eszkozok/teszt_sqlite_epit.py` (570–586) | `KJV_igehely` oszlopnév; az összegző egyenlet az új meta-kulcsokra; a régi oszlopnév nem szerepelhet a fejlécben |
| `eszkozok/f92_db_igazolas.py` | a 6. szakasz (`terkep`) KJV-kulcsra átírva, a várt számok újraszámolva (l. 3.); a 3. szakasz két várt száma: `forras=nincs, de a terkep_ertek nem üres` 137 → 95, `terkep_ertek nélkül` 246 → 288 |
| `eszkozok/terkep_kjv_kulcs_felmeres.py`, `zsolt_felirat_felmeres.py` | a fejléc-felismerés mindkét oszlopnevet elfogadja (a felmérés-szkriptek újrafuttathatók maradnak) |
| `adat/SEMA.md` (1149, 1154, 1156), `eszkozok/olvaso_pilot/README.md` (79), `olvaso_pilot/felmeres.py` (406) | oszlopnevek és számok frissítve |

A `macula_kk.py` pozíció szerint olvas: nem módosult (M2b: 0 hatás). A `naplok/KAROLI_KK1b_*_general.py` archív szkriptek pozíció szerint olvasnak, nem futtatandók. DT3: a térkép és az A-tábla sorszáma nem változik (Δ = 0), bontási napló nem kell.

## 2. Hatásmérés: `lxx_versszam` (elo = HEAD builder + régi oszlopnév; uj = a mostani builder)

- A teljes `pardes.db` 79 táblájából **három** tér el: `lxx_versszam`, `meta` (9/10 sor: építési időbélyeg, hash, új meta-kulcsok), `normalizalas_jelentes` (179 → 204 sor). A `nave_vers` (156 214 sor), a `token_*`, `lxx_token` és minden más tábla **bájtra azonos**.
- `lxx_versszam`: 24 232 sor mindkét oldalon; **1 344 sor tér el, 1 315 Károli-versen, kizárólag a `terkep_ertek` oszlopban** (a `karoli_igehely`, `lxx_igehely`, `kjv_vers`, `forras`, `megjegyzes`, `szovegforma` változatlan). Könyvenként: Zsolt 1 054 vers (63 fejezet: pontosan a feliratos zsoltárok), Jób 57, Dán 37, 4Móz 35, 2Móz 34, Hós 31, 1Sám 24, Én 13, Ézs 12, Jón 11, 1Kir 4, Péld 2, Józs 1. A `terkep_ertek` változása: üres → van 85 vers, van → üres 109 vers (főleg a felirat-versek: a téves KJV-hozzárendelés megszűnt), van → másik érték 1 121 vers.
- A `lxx_versszam:*` összegzők (meta): `terkep_karoli_kulcs` 5 026 → 5 002; `mindket_forras_verse` 4 889 → 4 907; **`forras_elteres_verse` (LXX_OS ≠ térkép) 1 888 → 799**; `nincs_de_van_terkep_ertek_verse` 137 → 95.
- Átváltás nélküli KJV-kulcs (`karoli_nelkul`): **203** a 5 204-ből (előtte: 178 „nem Károli-vers” kulcs). Könyvenként: Eszt 105, Dán 47, 2Móz 35, 1Kir 5, Hós 3, 4Móz 2, Péld 2, Ézs 2, Józs 1, Zsolt 1. Ezek az A-tábla és az LXX_OS megfeleltetésén kívül eső KJV-versek (Eszt/Dán görög-többlet és a Károli-vers nélküli számozás; pl. Hós 11:12); az A-tábla hiányainak javítása nem az F91 hatóköre (N-F91a).

## 3. M3: a Zsolt 22 vers-lap és a #60 kerülőút kivezethetősége

| mérés (Zsolt 22, LXX_OS-sor a `lxx_versszam`-ban) | előtte (régi `pardes.db` = elo.db) | utána (uj.db) |
|---|---|---|
| LXX_OS-sor / ebből nem üres `terkep_ertek` | 32 / 31 | **32 / 31** (a 22:1 felirat-versnek nincs KJV-kulcsa, üres) |
| a `terkep_ertek` első verse = az LXX_OS `lxx_igehely` verse | **1** / 31 | **31 / 31** |
| minden Zsolt: egyező / összes (LXX_OS-sor, nem üres `terkep_ertek`) | 1 442 / 2 419 | **2 412 / 2 419** |

Példa: Zsolt 22:2 (= KJV 22:1, LXX 21:2): `terkep_ertek` előtte `Psa.21:3` (a KJV 22:2 értéke tévesen), utána `Psa.21:1-2 | Psa.21:2`; Zsolt 22:32: előtte üres, utána `Psa.21:32`; a 22:1 (felirat): előtte a KJV 22:1 (`Psa.21:1-2`) értéke tévesen, utána üres. A Zsolt 22 vers-lapon tehát a `lxx_versszam.terkep_ertek` a 31 nem felirat versen mind a 31-en egyezik az LXX_OS-szel (előtte 1 / 31), a felirat-vers üres; a 31 ellentmondás (#60 pilot lelet) megszűnt. **A #60 kerülőút (az LXX_OS KJV-oszlopa a térkép helyett) kivezethető a Zsolt 22-re**; a pilot kódját (`olvaso_pilot/`) ez a tétel nem módosítja. A Zsolt 13:6 (`13:5;13:6`) mindkét KJV-vers térkép-értékét viszi (`Psa.12:6a | Psa.12:6 | Psa.12:6b`). A minden-Zsolt 7 megmaradó eltérés: Zsolt 1:1–6 (6 vers: a térkép saját sorai `Psa.Psa.151:…` értékkel, a Zsolt 1 nem feliratos; meglévő térkép-adathiba, nem F91-es, külön tétel) és Zsolt 13:2 (a térkép `Psa.12:1-2` tartománya, az LXX_OS 12:2: tartomány-kezdet különbség). A Nave `karoli_allapot` (N-F91b) érintetlen; a `nave_vers` tábla nem változik (a `NB.KjvRacs` az LXX_OS `igehely_kjv`-jét használja az A-tábla előtt).

## 4. Tesztek

- Menet közbeni javítás: az első építésnél a felirat-vers (LXX_OS `zsolt_felirat_eltolas`) is megkapta az első KJV-vers térkép-értékét (Zsolt 3:1 ← KJV 3:1); ez kiszűrve (`sqlite_epit.py`), a számok már a javított builderé.
- `python eszkozok/teszt_sqlite_epit.py`: **61 teszt, OK** (a „INTEGRITÁS-SÉRTÉS” sorok a negatív tesztek szándékos kimenetei). A `test_f92_terkep_nem_meghatarozhato_nem_esik_ki_nemanan` az új meta-kulcsokkal és a `KJV_igehely` oszlopnévvel fut.
- `python eszkozok/f92_db_igazolas.py --db <uj.db>`: minden sor `egyezik`, 0 `ELTÉRÉS` (a 6. szakasz: NEM_MEGHATAROZHATO 39, KJV-kulcs 5 204, átváltható 5 001, karoli_nelkul 203, Károli-vers a térkép-értékkel 5 002, ebből LXX_OS-sal 4 907, csak térkép 95, nem üres `terkep_ertek` 5 002, Zsolt 22: 32 / 31). A repó `naplok/PARDES_DB_OLVASOI_db_igazolas.md`-je a régi `pardes.db` kimenete, nem lett újragenerálva (a `pardes.db` újraépítése külön döntés: 938 MB, nem verziózott).
- `python eszkozok/ellenoriz.py`: RENDBEN 11 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 3 (az F91 előtti állapottól független, a Károli-/térkép-tábla nem szerepel benne).

## 5. Ami nyitva marad

- A `pardes.db` újraépítése (a repó `pardes.db`-je a régi builderrel készült; a mért különbség 1 344 `terkep_ertek` sor).
- Nave `karoli_allapot` újragenerálása: N-F91b.
- Az A-tábla hiányai a Hós/Jób/4Móz/Dán helyeken (203 átváltás nélküli KJV-kulcs egy része): N-F91a.
