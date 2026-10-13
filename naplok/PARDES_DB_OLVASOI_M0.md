# PARDES_DB_OLVASOI (#92) — M0 felmérés

*Proveniencia: `scope=a #92 M0 (csak olvas; a repóba csak ez a napló kerül) | forras=konkordancia/Macula_heber_*.tsv, konkordancia/LXX_OS/*.tsv, konkordancia/BDB_strong_alias.tsv, konkordancia/Nave_basokant.tsv, konkordancia/LXX_versificacios_terkep.tsv, eszkozok/sqlite_epit.py, eszkozok/olvaso_pilot/bovites.py, a fő munkamásolat pardes.db-je (mode=ro, F79-es, F89 előtti állapot; csak sorszám- és időmérés) | ts=2026-10-13`*

A méretek **mért** értékek (ideiglenes SQLite-fájlok a session scratchpadjében, `VACUUM` után, a tervezett oszlopokkal és indexekkel), kivéve ahol „becslés” áll. A repó adatához nem nyúltam.

## 1. Táblaterv

Mindegyik tábla: `meta`-sor (sorszám, hash) és `tabla_licenc`-sor (DT113); az építő `SZARMAZTATOTT_LICENC` szótárába kerül. A kulcs, ahol van, a **Károli-igehely** (`1Móz 1:1`).

| tábla | oszlopok (javaslat) | indexek | forrás | sor | mért méret | licenc-kulcs |
|---|---|---|---|---:|---:|---|
| `token_macula` | `xml_id`, `igehely`, `sorszam` (a `ref` `!n` része), `szo`, `lemma`, `strong`, `morf`, `szofaj`, `gloss`, `lxx_szo`, `lxx_strong` | `(igehely, sorszam)`, `strong` | `Macula_heber_*.tsv` (39 fájl) | 475 911 (23 031 vers) | 60,4 MB | `Macula_heber` |
| `lxx_token` | `lxx_igehely`, `karoli_igehely`, `pozicio`, `szoalak`, `lemma`, `morf`, `strong` | `(lxx_igehely, pozicio)`, `karoli_igehely`, `strong` | `LXX_OS/*.tsv` (59 könyvfájl, 2 nem-könyv fájl kimarad) | 616 873 (30 336 LXX-vers) | 86,3 MB | `LXX_OS` |
| `bdb_alias` | `masodlagos_strong`, `tabla_strong`, `bdb_id`, `nyelv`, `cimszo`, `szoveg_hasonlosag` | `masodlagos_strong` | `BDB_strong_alias.tsv` | 460 | < 0,1 MB | lásd 4.4 |
| `nave_vers` | `tema_id`, `tema`, `cimke`, `kapcsolat`, `nave_hely` (az eredeti KJV-hivatkozás), `igehely` (Károli), `tartomanyos` (0/1) | `igehely`, `tema_id` | `Nave_basokant.tsv` + `vers_szamozas` | kb. 150–160 ezer (becslés, 4.2) | kb. 19 MB (becslés) | `Nave_basokant`, `Karoli_versmegfeleltetes` |
| `lxx_versszam` | `karoli_igehely`, `lxx_igehely`, `kjv_vers`, `forras` | `karoli_igehely`, `lxx_igehely` | `LXX_OS` verskulcsa (+ lásd 4.1) | 30 336 + a 4.1 szerinti pótlás | 2,4 MB | `LXX_OS`, `Karoli_versmegfeleltetes` |

**A v1.1 index a magyar szavakra (K5):**
- `token_karoli`: új oszlop `szo_kis` (kisbetűs, nem-szóalkotó karakterek nélkül) + index. Ma a `szo` oszlopon nincs index; a kisbetűs keresés 200–400 ms (mért a fő munkamásolat F79-es adatbázisán: `lower(szo)='kép'` 402 ms; a „segítségül hív” kétszavas önillesztéses frázis 361 ms). Mért méret az oszloppal és indexszel: **25,9 MB**.
- `token_par`: új oszlop `hu_szo_kis` + index. A `hu_szo`-n **már van** pontos-alak index (`ix_token_par_1`; `hu_szo='kép'` 2,7 ms), de kis/nagybetű-független keresésre nem használható (`lower(hu_szo)='kép'` 210 ms; a „Kép” alakra 0 találat). Mért méret: **14,5 MB**.
- A #76 kiinduló mérése 1–3 s volt; a mostani gépen az itt mért értékek 0,2–0,4 s. A K5 (100 ms) ellenőrzését az M2-ben ugyanazon a gépen, előtte–utána méréssel végzem.

## 2. Várható méret

| tétel | MB |
|---|---:|
| `token_macula` | 60,4 |
| `lxx_token` | 86,3 |
| `lxx_versszam` | 2,4 |
| `bdb_alias` | < 0,1 |
| `nave_vers` (becslés) | 19,4 |
| `szo_kis` + `hu_szo_kis` oszlopok és indexeik | 40,4 |
| **új összesen** | **kb. 209** |

Az F89 utáni adatbázis 619,0 MB (`naplok/SQLITE_EPIT_meres.md`), tehát az újraépített **kb. 830 MB**. Mérethatár nincs (DT127). Építési idő: a mostani 49 s-hoz kb. +15–25 s (becslés). A teljes újraépítés és az eredő méret mérése az M1-ben történik.

## 3. A Nave-bontás szabályának helye

Ma a szabály az `eszkozok/olvaso_pilot/bovites.py` 357–392. sorában él: reguláris kifejezés a `Könyv f:v[-f:v]` alakra; a fejezet-sor külön kezelve; a tartomány a pilot `kjv_cv` kulcsa szerint bomlik versekre, a `kjv_cv` pedig a LXX_OS KJV-oszlopából, ennek hiányában a fejezet eltolásából, végső esetben a versmegfeleltető táblából jön.

Javaslat: új közös modul `eszkozok/nave_bontas.py` (tiszta függvények: hely-elemzés, tartomány-bontás egy KJV-verslista fölött); az építő importálja, így a szabály egy helyen él. A pilot `bovites.py` átállása a közös modulra az `ir` listában nem szerepel; jóváhagyás nélkül az építő csak a közös modult használja, a pilot a saját példányát, és a D2-teszt ellenőrzi az egyezést.

## 4. Döntést igénylő megállapítások

1. **Az `lxx_versszam` „minden vers” nem teljesíthető a LXX_OS-ből.** A 23 204 ÓSZ Károli-versből 22 821-nek van LXX_OS-kulcsa, **383-nak nincs** (pl. `1Kir 11:23`, `11:24`, `12:2`, `13:27`, `14:1`, `14:10`–`14:16`). Ezek közül 137 szerepel a `LXX_versificacios_terkep.tsv`-ben (5 205 Károli-vers). Ezenfelül 6 487 LXX-versnek üres a `karoli_igehely`-je. Javaslat: a tábla minden ÓSZ Károli-versre kapjon sort; ahol a LXX_OS-ben nincs, a `forras` oszlop jelöli (`versificacios_terkep`, vagy `nincs` üres `lxx_igehely`-vel) — a hiány explicit, nem kitöltve (CLAUDE.md 3. szabály). A térképből pótolt 137 sor milyensége (és hogy elfogadható-e második forrásként) a te döntésed; a maradék 246 `nincs`.
2. **A Nave-sorok szerkezete.** 85 246 sor: 64 236 `vers`, 11 663 `tartomany`, 2 212 `fejezet`, 7 122 üres hely (`lasd`/`szoveg` kapcsolat: utalás témára vagy szövegre), 13 `ismeretlen_konyv`. A Károli-rácson bontva (felső becslés, az ÚSZ-sorokkal) kb. 156 ezer vers-sor. Javaslat: a `fejezet`-sorok **nem** bomlanak versekre és nem kerülnek `nave_vers`-be (a fejezet-szintű nézet az eredeti `nave_basokant` táblából jön); az igehely nélküli sorok sem. A KJV→Károli megfeleltetés a `vers_szamozas.kjv_igehely` oszlopból, a pilot szabályával egyezően; a 99 nulla-vers sor (rácson kívüli hivatkozás) a normalizálási jelentésbe kerül. Kérdés: fejezet-szintű sor kell-e a `nave_vers`-be?
3. **A Macula–TAHOT összekapcsolás.** A `token_macula` saját kulcsa az `xml_id`; a `token_eredeti` (TAHOT) `(igehely, sorszam)` kulcsához a Macula szósorszáma nem biztosan egyezik (más tokenizálás). Szó-szintű illesztést nem építek (új adat, nem része a feladatnak); a lapok vers+Strong alapon illesztenek, mint a pilot a TSV-úton. Ha a D2-ben ez eltérést ad, jelzem.
4. **Licenc a `bdb_alias`-hoz.** A `licencek.tsv`-ben a `BDB_strong_alias` kulcsra **nincs sor**. Javaslat: `SZARMAZTATOTT_LICENC['bdb_alias'] = ['BDB', 'projekt_adat']` (legszigorúbb érték érvényes), új licencsor nélkül. Új sor az `adat/licencek.tsv` módosítása lenne, ami az `ir` listában nincs.
5. **A `token_macula` licence.** A `Macula_heber` sora CC BY 4.0 (Biblica, Inc), szó szerinti idézet-kötelezettséggel (`LICENSE.md` 3. sor); a `tabla_licenc.cimke` hordozza.
6. **A `db_meres.py` módosíthatósága.** A D1–D5 újrafuttatásához a mérő (`eszkozok/olvaso_pilot/db_meres.py`) az új táblákból olvasna; ez a fájl és a `teszt_olvaso_pilot.py` az `ir` listában **nincs**. Kérés: engedélyezd a minimális módosításukat, vagy a mérés ideiglenes, nem commitolt kiterjesztéssel fusson, és a jelentés ezt jelzi.

## 5. Mit kérek jóváhagyásra

(a) az 1. szakasz táblaterve (oszlopok, indexek); (b) a kb. 209 MB növekedés (kb. 830 MB összesen); (c) a 4.1 (explicit hiány / térkép-pótlás), 4.2 (fejezet-sorok), 4.4 (licenc), 4.6 (`db_meres.py`) pontok javasolt megoldása; (d) a Nave-bontás közös modulja (3. szakasz).

## 6. M2 — a K5 mérés nyers kimenete (előtte–utána)

*Proveniencia: `scope=K5, magyar szóra és kétszavas frázisra keresés, 7 ismétlés, új kapcsolat minden ismétlésnél, median | forras=a fő munkamásolat F79-es pardes.db-je (előtte) és a #92 újraépített pardes.db (utána), lekérdezések: token_par/token_karoli, előtte lower(), utána hu_szo_kis/szo_kis | ts=2026-10-13`*

```
gép: Windows-11-10.0.26300-SP0, 8 CPU, python 3.14.7
== ELŐTTE (a fő munkamásolat F79-es pardes.db: nincs szo_kis; lower() keresés) | C:/Users/bases/Desktop/Bible-Study/pardes.db | 886.4 MB
  token_par szó        kép              találat      4  median    165.5 ms  max    209.4 ms
  token_karoli szó     kép              találat      4  median    327.7 ms  max    401.5 ms
  token_par szó        Isten            találat   1306  median    161.1 ms  max    164.0 ms
  token_karoli szó     Isten            találat   1293  median    325.8 ms  max    328.7 ms
  token_par szó        szeretet         találat      7  median    162.5 ms  max    164.2 ms
  token_karoli szó     szeretet         találat      6  median    326.1 ms  max    329.7 ms
  token_par szó        ország           találat     72  median    159.1 ms  max    163.8 ms
  token_karoli szó     ország           találat     63  median    324.7 ms  max    327.4 ms
  token_par szó        segítségül       találat     51  median    161.0 ms  max    162.8 ms
  token_karoli szó     segítségül       találat     47  median    325.7 ms  max    329.3 ms
  token_karoli frázis  segítségül hív   találat      1  median    326.5 ms  max    347.2 ms
  token_karoli frázis  Isten fia        találat      0  median    334.4 ms  max    451.5 ms
  token_karoli frázis  örök élet        találat      0  median    328.3 ms  max    338.7 ms
  legnagyobb median: 334.4 ms
== UTÁNA (F92: szo_kis / hu_szo_kis index) | C:/Users/bases/Desktop/wt-f92-pardes-db-olvasoi/pardes.db | 899.3 MB
  token_par szó        kép              találat      4  median      0.8 ms  max      0.9 ms
  token_karoli szó     kép              találat      4  median      0.7 ms  max      0.7 ms
  token_par szó        Isten            találat   1515  median      9.1 ms  max      9.3 ms
  token_karoli szó     Isten            találat   1508  median      1.8 ms  max      2.0 ms
  token_par szó        szeretet         találat     27  median      0.9 ms  max      1.2 ms
  token_karoli szó     szeretet         találat     25  median      0.7 ms  max      0.8 ms
  token_par szó        ország           találat     72  median      1.3 ms  max      1.4 ms
  token_karoli szó     ország           találat     63  median      0.7 ms  max      0.9 ms
  token_par szó        segítségül       találat     55  median      1.1 ms  max      1.2 ms
  token_karoli szó     segítségül       találat     50  median      0.7 ms  max      0.8 ms
  token_karoli frázis  segítségül hív   találat      1  median      0.8 ms  max      0.8 ms
  token_karoli frázis  Isten fia        találat      3  median      1.7 ms  max      1.7 ms
  token_karoli frázis  örök élet        találat      4  median      0.8 ms  max      0.8 ms
  legnagyobb median: 9.1 ms
```

A találatszám különbsége: az előtte-adatbázis régebbi építés, és a `szo_kis` az írásjelet levágja.
