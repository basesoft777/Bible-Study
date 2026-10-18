# F117.5 — nem körkörös mérés (M1–M5), fogyasztói hatás, E6

*FELADATOK #117 · ág: `claude/f117-versmegf-javitas` · végrehajtó: claude-opus-5-5 · 2026-10-18*

## 1. M1–M5 (`eszkozok/tsk_versszam_felmeres.py`, új G. rész)

proveniencia: scope=A–D′ (346 Károli-vers) + teljes ÓSZ (M3) + elofordulasok.tsv (M5) | forras=TSK_kereszthivatkozasok.tsv + naplok/F117_itelet.tsv (referencia) + Karoli_versmegfeleltetes.tsv (új) + `git show 89b30c2e:konkordancia/Karoli_versmegfeleltetes.tsv` (régi, sha256 edd6b457…b562) és az F114-es NINCS_PAR_KIVETEL | eszkoz=`python eszkozok/tsk_versszam_felmeres.py --kimenet <repón kívül> --regi-tabla <régi tábla>` | ts=2026-10-18

**A referencia** a versenkénti kézi ítélet (`naplok/F117_itelet.tsv`; összevont versnél az első KJV-vers, DT206 (2)), nem a tábla. A javító bemenet ebből készült, ezért a (ii) = (iii) azt igazolja, hogy a lánc (bemenet → KK4 → `tsk_kulcs`) a referenciát szállítja. A referencia helyességét a kézi ítélet hordozza, a korláttal együtt (N-F117c).

| Mérés | Osztály | Vers | (i) régi | (ii) új | (iii) referencia | (ii) ≠ (iii) |
|---|---|---|---|---|---|---|
| M1 forrás (TSK-forrássor) | A | 261 | 0 | 3 730 | 3 730 | 0 |
| | C | 3 | 0 | 59 | 59 | 0 |
| | B | 8 | 0 | 110 | 110 | 0 |
| | D | 67 | 15 | 780 | 780 | 0 |
| | D′ | 7 | 81 | 95 | 95 | 0 |
| | **össz** | **346** | **96** | **4 774** | **4 774** | **0** |
| M2 cél (TSK-célelőfordulás) | A | 261 | 0 | 2 923 | 2 923 | 0 |
| | C | 3 | 0 | 82 | 82 | 0 |
| | B | 8 | 0 | 107 | 107 | 0 |
| | D | 67 | 9 | 922 | 922 | 0 |
| | D′ | 7 | 31 | 42 | 42 | 0 |
| | **össz** | **346** | **40** | **4 076** | **4 076** | **0** |

- **M3 (teljes ÓSZ):**
  - Károli→KJV irány: 345 kulcs változott, mind az A–D′ halmazban. Az 1Kir 22:43 párja azonos maradt (22:43), csak az osztálya és a forrása változott. A halmazon kívül **0** eltérés.
  - KJV→Károli irány: 350 kulcs változott. Olyan nincs köztük, amely egyetlen A–D′ verset sem érint (**0**).
- **M4:** a felmérő B- és E-része a javított táblán.
  - E: a fogyasztói úton olvasott 21 568 ÓSZ-kulcsból 0-nak hibás a KJV-forrása. Az előfordulás-versek között 0 rossz versről érkező és 0 elmaradó TSK-sor van (minden Votes-értéknél és Votes ≥ 15-nél is).
  - F (a régi, identitásos elérés): a „régen elért, most nem” veszteség 7 KJV-kulcsra és 128 forrássorra szűkült. Ez pontosan a visszairányú összevonás-veszteség: az N-F117b öt KJV-verse, valamint a régi Préd 2:26 és Zsolt 13:6. A #114-ben a veszteség 235 forráskulcs és 3 653 sor volt (tábla-lyuk).
- **M5 (`elofordulasok.tsv`, régi / új / referencia TSK-forrássor):**

  | Motívum | Vers | Régi | Új | Referencia |
  |---|---|---|---|---|
  | TEREMT-001 | Jón 2:6 | 0 | 4 | 4 |
  | ALVIL-001 | Jón 2:3 | 0 | 26 | 26 |
  | ALVIL-001 | Hós 13:14 | 0 | 29 | 29 |
  | ALVIL-001 | Jób 17:12 | 0 | 11 | 11 |
  | ALVIL-001 | Jób 17:15 | 0 | 14 | 14 |

## 2. Fogyasztói hatás (4.6)

A `Karoli_versmegfeleltetes.tsv`-t olvasó eszközök (`grep -rl Karoli_versmegfeleltetes eszkozok/ naplok/*.py`, a tesztek és az F117-fájlok nélkül), 45 fájl. Mind a teljes táblát olvassa, tehát A–D′ verset is.

**A `KEZI` + kitöltött `igehely_mt` (Károli ≠ KJV és ≠ MT) kezelése, a kért hat fogyasztón** (próba: `naplok/F117_fogyaszto_proba.py`, csak olvas):

| Fogyasztó | Mit csinál az `igehely_mt`-vel | Ítélet |
|---|---|---|
| `f17/macula_kk.py` | a kitöltött `igehely_mt` az MT-vers (`kk_mt`), a KEZI-ág csak üres mt-nél | helyes |
| `lexikon_general.py` (csak olvastam) | Károli→MT: a kitöltött `igehely_mt`, különben `KJV` osztálynál azonosság | helyes |
| `olvaso_szerver/bdb_vers_jelentes.py` | `vm_mt` (MT→Károli) csak keresztellenőrzés (`atkulcsolt_bizonytalan` jelölés) | helyes; a kimenete újragenerálva változna |
| `olvaso_pilot/bdb_szelet_m0.py` | `vm_mt` MT→Károli térkép | helyes (az MT-kulcs a valódi MT); a kimenete újragenerálva változna |
| **`fj2/bsb_import.py`** | `fejezet_eltolasok()`: az `igehely_mt` MT-fejezet-maximumát a TAHOT **Károli**-fejezet-maximumával veti össze, eltérésnél `SystemExit` | **HIBÁS: újrafuttatva 13 fejezeten megállna** (a régi táblán 0). A feltevése (kitöltött mt = Károli-szám) a régi konvenció volt. Fejezetek: 1Sám 20, 1Sám 21, 2Móz 36, Hós 2, Jób 17, Jób 37, Jób 40, Préd 10, Péld 12, Én 6, Én 7, Ézs 2, Ézs 3 |
| **`sqlite_epit.py`** (`_bsb_szamozas`) | MT-kulcs → Károli a kitöltött `igehely_mt`-ből (`mt_kk`), különben **azonosság** | **HIBÁS: 6 Károli-vers kapna két BSB MT-verset** (a régi táblán 0). Ezek: Hós 2:1 ← MT 2:1, 2:4; Hós 2:2 ← 2:2, 2:5; Hós 2:3 ← 2:3, 2:6; Jób 17:1 ← 17:1, 17:2; Jób 37:1 ← 37:1, 37:2; Péld 12:1 ← 12:1, 12:2. Ok: az előző fejezetek (Hós 1, Jób 16, Jób 36, Péld 11) MT-verseit az azonosság-tartalék a Károli-fejezet elejére teszi |

**A többi fogyasztó**: nem vizsgáltam részletesen; mind olvas A–D′ verset. Az újragenerálásuk (ha a kimenet `adat/`, `konkordancia/`, `pardes.db` vagy Macula-kimenet) az N-F117a tárgya:
- a TSK-út a `tsk_kulcs`-on át: `lekerdez.py`, `nem_vizsgalt.py`, `lexikon_general.py`, `sqlite_epit.py` (`tsk`), `olvaso_pilot/adat.py`;
- Macula: `f17/macula_futtat.py`, `macula_kozos.py` (a `Macula_heber_*.tsv` `karoli` oszlopa);
- LXX: `lxx_os_import.py`, `f91_lxx_os_replay.py`, `naplok/LXX_OS_LEFEDETTSEG_M0_general.py`;
- `karoli_strong/elopar_kjv.py`, `karoli_strong/tokenek.py`;
- `nave_import.py`, `nave_bontas.py`;
- `tahot_verskulcs_finomit.py`, `tahot_verskulcs_esetlista.py`;
- `f08/*`, `f92_db_igazolas.py`, `f93_tipnr_token_hiany.py`, `terkep_kjv_kulcs_felmeres.py`, `zsolt_felirat_*.py`, `bdb_konyv_javit.py`, `ellenorzes/tanulmany_ellenorzes.py`;
- `olvaso_pilot/*` (`bovites`, `db_meres`, `felmeres`, `meres`), `olvaso_szerver/m2_karoli_ellenoriz.py`, `fj2/bsb_verseltolas_diag.py`, `naplok/F09_S2_7_szerepek_frissit.py`.

**Nem futtattam újra egyik fogyasztót sem.**

## 3. E6 — a többi adat bájtra változatlan

`git ls-tree -r <ref> -- adat konkordancia`: a 305 egyéb `*.tsv` (a `Karoli_versmegfeleltetes.tsv` és a `_javitas.tsv` nélkül; az `LXX_OS/` is benne van) (blob, útvonal) listájának sha256-ja az alapcommiton (89b30c2e) és a HEAD-en egyaránt `eb706190034459ea3c31fd37c1e6c8f12987b862e7ce9f08f2e02806328d89ca`. A `git diff --name-only 89b30c2e -- adat/ konkordancia/` csak a `Karoli_versmegfeleltetes.tsv`-t, a `Karoli_versmegfeleltetes_javitas.tsv`-t és a `README.md`-t mutatja.

## 4. Az F117.5 őr (DT209 (a)) és a tesztek

- **Őr:** `eszkozok/sqlite_epit.py` `kezi_mt_or()`, a `_bsb_szamozas()` elején hívva. Ha a versmegfeleltető táblában `KEZI` osztályú sor kitöltött `igehely_mt`-t hordoz, `VersmegfKeziMt` hibával leáll: kiírja a sorok számát és az első öt példát, és hivatkozik az N-F117a-ra. A valós táblán 174 sor, első példák: 1Sám 20:43, 2Móz 35:36, 2Móz 36:1, 36:10, 36:11. Az `sqlite_epit.py` és a tesztfájl írása egyeztetett eltérés: a brief `ir` mezőjén kívül esik, a felhasználó kérése.
- **Teszt:** `eszkozok/teszt_sqlite_epit.py` `KeziMtOr`, fixtúrával, 2 teszt, mindkettő zöld (`cd eszkozok && python -m unittest -v teszt_sqlite_epit.KeziMtOr`):
  - a `KEZI` + mt sor leállít;
  - a `KEZI` üres mt-vel, az `MT` és a `KJV` sor nem állít le.
- **A teljes tesztfájl** (`python eszkozok/teszt_sqlite_epit.py`; ezek nem olvasó-szerver tesztek, a `teszt_futtat.py` nem futtatja őket): 38 teszt futott, 1 FAIL és 2 ERROR.
  - **ERROR: `Integracio.setUpClass`.** A valós repóadatból épít (`Epito(ROOT, …, 'minta')`), és az őr leállítja. Emiatt az összes integrációs teszt kimarad (korábban 70 teszt futott).
  - **ERROR: `FeliratHalmaz.test_a_felirat_versnek_nincs_terkep_erteke_a_db_ben`.** Ugyanez az ok.
  - **FAIL: `Pozitiv.test_mai_adat_zold`.** A main-en is fennálló „15. kapcsolatok.tsv” jelentéssor (`naplok/F117_javitas_jelentes.md` 4. pont), nem az őr okozza.
  - A két ERROR a felhasználó feltétele szerint ⛔: nem gyengítettem és nem kerültem meg. Feloldásuk az N-F117a (a `_bsb_szamozas` javítása), vagy a felhasználó döntése.
- **Kimondott kihagyás (Felhasználó, 2026-10-18; DT209 kiegészítés):** az `Integracio` osztály és a `FeliratHalmaz.test_a_felirat_versnek_nincs_terkep_erteke_a_db_ben` `unittest.skip`-et kapott, indoklással: „N-F117a: … az N-F117a javításakor visszaveendő”. Újrafuttatás (`python eszkozok/teszt_sqlite_epit.py -v`): 72 teszt, **0 ERROR**, 35 skip, 1 FAIL. A FAIL a main-en is meglévő `test_mai_adat_zold`.
- **F117.8 (6) — szűkítés:** a feltétel nélküli `@unittest.skip` helyett feltételes kihagyás. A `kezi_mt_or_kihagy()` a valós táblán meghívja az őrt; csak `VersmegfKeziMt` esetén `SkipTest` / `skipTest`, okkal. Az `Integracio` 34 tesztje mind a közös `setUpClass`-építésen áll (két `S.main(--mod minta)` a valós `ROOT`-ból), ezért leválasztani nem lehet. A unittest a setUpClass-skipet egy skipként számolja. A `KeziMtOr` már nem nyel el minden kivételt: az őr utáni `FileNotFoundError`-t várja, a `BSB_Strongs.tsv` fájlnévvel. Futás: `python eszkozok/teszt_sqlite_epit.py -v`: 38 teszt, 2 skip (Integracio setUpClass + FeliratHalmaz), 1 FAIL (`test_mai_adat_zold`, a main-en is), 0 ERROR.
