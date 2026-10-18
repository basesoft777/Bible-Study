---
feladat: 115
cim: A Macula héber LXX-szóalak χ↔ξ cseréjének javítása, Rahlfs-minőségjelöléssel
kod: MACULA CHI XI
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/f115-macula-chi-xi
ad: a `Macula_heber_*.tsv` `gorog_lxx` és a `token_macula.lxx_szo` χ↔ξ-hibája az importban javítva (teljes csere az érintett sorokban), soronkénti Rahlfs-minőségjelöléssel és a forrásalak megőrzésével; a vers-lap Macula-táblázata a javított alakot mutatja
kovetkezo: Te: a PR átnézése és a merge
munka: adat
helyi_gep: igen
olvas: [konkordancia/Macula_heber_*.tsv, konkordancia/LXX_OS/, naplok/MACULA_CHI_XI_felmeres.md, naplok/F17_import_naplo.md, eszkozok/f17/, eszkozok/macula_chi_xi_felmeres.py, eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/, eszkozok/olvaso_pilot/, adat/SEMA.md]
pr: (PR után kitöltendő)
lezarva_osszegzes: χ↔ξ teljes csere az importban (19 876 sor), forrásalak és Rahlfs-jelölés új oszlopban, osztályszámok pontosan a felmérés szerint; token_macula két új oszlop, olvasó-jelölő; ellenőrzés: naplok/ELLENOR_F115.md; zárójelentés: naplok/MACULA_CHI_XI_zaras.md
ir: ["konkordancia/Macula_heber_*.tsv", naplok/F17_87_hely.tsv, naplok/F17_illesztetlen.tsv, eszkozok/f17/macula_import.py, eszkozok/f17/macula_futtat.py, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_pilot/teszt_olvaso_pilot.py, eszkozok/macula_chi_xi_felmeres.py, adat/SEMA.md, adat/bdb_vers_jelentes.tsv]
fugg: []
nem_fugg: [11, 101, 114]
---

# F115_MACULA_CHI_XI_BRIEF.md — a Macula héber LXX-szóalak χ↔ξ cseréjének javítása

*FELADATOK #115 · Modell: sonnet · v2 · 2026.10.18*

*Előzmény: `NYITOTT_FELADATOK.md` „2026.10.05, olvasói prototípus — χ/ξ” tétel és 2026.10.18-i lelete; mérés: `naplok/MACULA_CHI_XI_felmeres.md`. **A felhasználó döntése (2026-10-18):** a javítás az importban történik, nem kézzel; **teljes χ↔ξ csere minden érintett sorban**, mert a felmérés szerint 19 876 érintett sorból 0-ban igazolja a Rahlfs az eredeti alakot, és kétértelmű sor sincs; a Rahlfs-igazolás **soronkénti minőségjelölés, nem feltétel**; az eredeti forrásalak külön oszlopban megmarad; jelölten üres mező nem keletkezik. (A v1 feltételes cseréjét és lefedettségi küszöbét ez a döntés váltotta fel.)*

## 1. Cél

A Clear-Bible/macula-hebrew@47db250b `greek` attribútumában a χ és a ξ fel van cserélve (forrásoldali hiba; az import csak átveszi). Az import ezentúl minden χ-t vagy ξ-t tartalmazó `gorog_lxx` értékben felcseréli a két betűt (`χ↔ξ`, `Χ↔Ξ`), az eredeti értéket külön oszlopban megőrzi, és minden érintett sorhoz rögzíti, igazolja-e a Rahlfs-LXX (LXX_OS) ugyanazon Károli-versének szava a javított alakot, és ha nem, miért nem.

## 2. Hatókör

**Benne van:** `eszkozok/f17/macula_import.py` (a javító és osztályozó függvény, LXX_OS-index), `eszkozok/f17/macula_futtat.py` (hívás, új oszlopok, fejléc), a 39 `konkordancia/Macula_heber_*.tsv` újragenerálása, a `naplok/F17_87_hely.tsv` / `naplok/F17_illesztetlen.tsv` (ha a futtató írja és változnak), `eszkozok/sqlite_epit.py` (`token_macula` két új oszlop), `eszkozok/olvaso_szerver/lekerdezesek.py` `macula()` és `blokkok.py` `_r_macula_gorog` (javított alak + jelölő), `adat/SEMA.md`, a tesztek (3.6), a `pardes.db` újraépítése és az olvasó-tesztek.

**Nincs benne:**
- **Upstream jelzés a Clear-Bible-nek** (GitHub issue) — nyilvános megszólalás, csak a felhasználó dönthet róla; javaslatként a zárónaplóba kerül (N-F115a).
- A `Macula_gorog.tsv` (ÚSZ) — nem érintett; a futtató újraírja, a diffje 0 legyen.
- A χ/ξ-t nem tartalmazó, mégis Rahlfs-eltérő sorok (a kontrollban a χ/ξ-mentes sorok 8,9%-a: kis-/nagybetű, szövegforma, versszám) — nem e hiba, nem kapnak jelölést.
- A `naplok/F08_bemenet.txt` 3 hibás alakja (történeti napló); az `adat/lxx_dontesek.tsv` (Strongon/lemmán dolgozik); a lexikon (a `blokk_lxx` LXX_OS-ből olvas); a `blokkok.py:425-442` csempe-heurisztikájának átírása.

## 3. Lépések

### 3.0 Modell-ellenőrzés, ág
Írd ki a tényleges modellnevedet, és vesd össze a fejléc `modell` mezőjével (CLAUDE.md). Saját ág a main-ről (`claude/f115-macula-chi-xi`, a befogadott számmal); commitonként tétel-azonosító (`F115.0:`, `F115.1:` …, a végleges számmal).

### 3.1 Pinelt klónok, reprodukálhatóság
- Sekély, sparse fetch a repón **kívülre** (a `naplok/F17_import_naplo.md` 241. sora szerint): `Clear-Bible/macula-hebrew@47db250bd55d0d8577f2a94fba114ef16c35b23c` (`WLC/lowfat`), `Clear-Bible/macula-greek@8423afe47b9e8f24b7772e808af45c7159a6fe7e` (`Nestle1904/tsv`, `SBLGNT/tsv`).
- A **változatlan** import futtatása ideiglenes kimeneti könyvtárba (a repón kívül; ha a futtató nem tud `--kimenet`-et, előbb ezt add hozzá, külön tétel, alapértelmezett viselkedés változatlan), és bájtra összevetés a 39 `Macula_heber_*.tsv`-vel és a `Macula_gorog.tsv`-vel (a fejléc `ts=` sora kivétel).
- ⛔ **0. megállás:** ha a diff nem 0, az import nem reprodukálható — jelentés, megállás (a javítás a változásoktól nem választható el).

### 3.2 A javító és osztályozó függvény (az importban)
- **LXX_OS-index** a `macula_import.py`-ban: `igehely_karoli → [(szoalak NFC, strong)]`, minden szövegformából (`konkordancia/LXX_OS/*.tsv`, csak a `igehely_karoli`, `szoalak`, `strong` oszlopot tartalmazó fájlok), `split('\t')`-tel (nem `csv`).
- **`lxx_chi_xi_javit(greek, gorog_strong, karoli_kulcsok, ix)` → `(gorog_lxx, gorog_lxx_rahlfs)`**:
  - nincs χ/Χ/ξ/Ξ: `(greek, '')` — érintetlen, jelölés nélkül;
  - van: `gorog_lxx = greek.translate({χ↔ξ, Χ↔Ξ})` — **mindig**, feltétel nélkül;
  - a minőségjelölés a `karoli_kulcsok` (`;`-vel tagolt) összes LXX_OS-tokenjén, a χ/ξ-s szavakra külön, a felmérő szkript (`eszkozok/macula_chi_xi_felmeres.py`) B-osztályai szerint:
    - `rahlfs_igazolt` — a javított szó betűre (NFC) megvan a versben, és ugyanazon a tokenen a Strong is egyezik (vagy a Macula `gorog_strong` üres);
    - `nem_igazolt:strong_elteres` — a javított szó betűre megvan, de a Strong eltér (alak igazolt, Strong-kódolási eltérés);
    - `nem_igazolt:csak_kisbetu` — csak kis-/nagybetűben tér el (jellemzően a Macula kisbetűs tulajdonnevei);
    - `nem_igazolt:csak_ekezet` — csak ékezetben tér el;
    - `nem_igazolt:nincs_egyezes` — van LXX-vers, de nincs megfelelő szó;
    - `nem_igazolt:nincs_karoli` — a sornak nincs Károli-kulcsa;
    - `nem_igazolt:nincs_lxx_vers` — a Károli-versnek nincs LXX_OS-tokenje.
  - Több χ/ξ-s szó egy sorban: ha mind `rahlfs_igazolt`, a sor `rahlfs_igazolt`; különben az első nem igazolt szó osztálya.
  - **Ellenőrző osztályok** (nem kimeneti értékek, hanem a ⛔1 kiváltói): `eredeti_igazolt` (az EREDETI, csere előtti szó betűre megvan a versben, a javított nincs), `ketertelmu` (mindkettő megvan). Ezeket a függvény számolja és naplózza; a mezőbe ilyenkor is a javított alak kerül, a jelölés `nem_igazolt:eredeti_igazolt` / `nem_igazolt:ketertelmu` — de a futás a ⛔1-nél megáll.
- **Új oszlopok a `Macula_heber_*.tsv` végén** (a meglévő indexek nem tolódnak; az `eszkozok/olvaso_pilot/adat.py:340` `r[13]`/`r[14]`-et olvas):
  - `gorog_lxx_forras` — az upstream `greek` attribútum változatlanul, **minden** sorban;
  - `gorog_lxx_rahlfs` — üres (χ/ξ-mentes, érintetlen sor) vagy a fenti minőségjelölés.
- **`gorog_lxx`** = a javított érték (χ/ξ-mentes sorban az upstream érték). Jelölten üres mező nem keletkezik: ahol a `gorog_lxx_forras` nem üres, ott a `gorog_lxx` sem.
- A fejlécbe egy sor a szabályról (`DT-F115a`, `naplok/MACULA_CHI_XI_felmeres.md`); a `naplok/F17_import_naplo.md`-be egy szakasz a javítás számaival. A `F17_87_hely.tsv` (a `macula_futtat.py:103,289` a nyers `greek`-et írja) ugyanazzal a függvénnyel a javított értéket kapja.

### 3.3 Mérés és ⛔1 (ellenőrzés)
- Futtatás az ideiglenes kimenetre; osztályonként és könyvenként számold a `gorog_lxx_rahlfs` értékeit.
- **Várt értékek** (a felmérés B változata, `naplok/MACULA_CHI_XI_felmeres.md` 2. szakasz; összesen 19 876 érintett sor):

  | `gorog_lxx_rahlfs` | várt |
  |---|---:|
  | `rahlfs_igazolt` | 16 468 |
  | `nem_igazolt:strong_elteres` | 1 029 |
  | `nem_igazolt:csak_kisbetu` | 2 004 |
  | `nem_igazolt:csak_ekezet` | 30 |
  | `nem_igazolt:nincs_egyezes` | 147 |
  | `nem_igazolt:nincs_karoli` | 158 |
  | `nem_igazolt:nincs_lxx_vers` | 40 |
  | `eredeti_igazolt` (ellenőrző) | 0 |
  | `ketertelmu` (ellenőrző) | 0 |

- ⛔ **1. megállás (ellenőrzés, nem döntés — a javítási szabályról a felhasználó már döntött):** megállás és jelentés, ha
  - (a) **bármely** sorban a Rahlfs az EREDETI alakot igazolja (`eredeti_igazolt` > 0), vagy
  - (b) kétértelmű sor jelenik meg (`ketertelmu` > 0), vagy
  - (c) az érintett sorok száma vagy bármelyik osztály száma **±1%-nál** jobban eltér a fenti várt értéktől.
  Ha egyik sem áll fenn, a menet megállás nélkül folytatódik; a számok a zárónaplóba kerülnek.

### 3.4 Élesítés
- Az import futtatása a repóba. **Diff-őr** (szkript, `split('\t')`): a 39 TSV-ben csak a `gorog_lxx` oszlop változhat, és csak χ/ξ-s sorban, pontosan a χ↔ξ csere szerint; a két új oszlop hozzáadódik; minden más oszlop 0 diff; a `Macula_gorog.tsv` 0 diff (`ts=` kivétel). Eltérésnél megállás.
- A felmérő szkript újrafuttatása a javított táblán: várt `igazolt_eredeti` = 17 497 (A változat), `igazolt_csere` = 0 (ha a szkript az új oszlopokat nem kezeli, egy `--forras-oszlop` kapcsolóval bővítendő).

### 3.5 `pardes.db` és olvasó
- `eszkozok/sqlite_epit.py`: a `token_macula` két új oszlopa `lxx_szo_forras`, `lxx_szo_rahlfs`; az `lxx_szo` a javított `gorog_lxx`; `meta` sorok: `token_macula:lxx_szo_rahlfs:<érték>` = darab.
- `adat/SEMA.md` `token_macula` sora (≈1147. sor) és megjegyzései: az `lxx_szo_forras` az upstream alak, az `lxx_szo_rahlfs` a minőségjelölés.
- `lekerdezesek.py` `macula()`: `lxx_rahlfs` kulcs. `blokkok.py` `_r_macula_gorog`: a „Görög (Macula)” oszlop a **javított** alakot mutatja; ahol a jelölés nem `rahlfs_igazolt` (és nem üres), a cellában jelölő áll (pl. apró „nem igazolt” jel, `title` attribútumban az osztály és a forrásalak). A `rahlfs_igazolt` és az érintetlen sor jelölés nélkül jelenik meg.
- DB-újraépítés WSL-natív útvonalra (`PARDES_DB`, `~/pardes/pardes.db`).

### 3.6 Tesztek
- `eszkozok/teszt_sqlite_epit.py` új teszt: (1) az 1Móz 1:1 `בְּרֵאשִׁית` sora: `lxx_szo` = `ἀρχῇ`, `lxx_szo_forras` = `ἀρξῇ`, `lxx_szo_rahlfs` a DB-ben mért érték (várhatóan `rahlfs_igazolt`; a pontos értékeket a DB-ből, nem a briefből); (2) nincs sor, ahol az `lxx_szo_forras` nem üres, az `lxx_szo` pedig üres; (3) χ/ξ-mentes sorban `lxx_szo_rahlfs` üres és `lxx_szo` = `lxx_szo_forras`; (4) χ/ξ-s sorban `lxx_szo` = `lxx_szo_forras` χ↔ξ cseréje.
- `eszkozok/olvaso_pilot/teszt_olvaso_pilot.py:88,90`: ma a hibás `lxx_macula = 'ἀρξῇ'`-t várja; a pilot az `r[13]`-at olvassa, ami a javítás után `ἀρχῇ` — az elvárt érték a javítottra áll, a változás naplózva (a pilot vizuális mércéje nem romlik: a pilot a Rahlfs-alakot mutatja).
- Futtatás: `python eszkozok/teszt_futtat.py` (teljes); a kimenet első sora (melyik adatbázist nyitotta meg) a naplóba.
- Böngészős ellenőrzés a vers-lapon (1Móz 1:1, 1Móz 2:7, 4Móz 1:8): a táblázatban a javított alak, a 4Móz 1:8 tulajdonnév-sorában (`ισσαχαρ`, `nem_igazolt:csak_kisbetu`) a jelölővel.

### 3.7 Zárás
- `naplok/MACULA_CHI_XI_zaras.md`: a számok osztályonként és könyvenként, a ⛔1-ellenőrzés eredménye, a diff-őr és a tesztkimenet.
- `NYITOTT_FELADATOK.md`: a „2026.10.05 χ/ξ” tétel LEZÁRVA; marad két javaslat: N-F115a (upstream jelzés), N-F115b (LXX_OS kulcsrés Én/Préd).
- `DONTESEK.md`: `DT-F115a` (a javítási szabály, l. 5.).
- Független ellenőr (`fuggetlen-ellenor`) a base..head diffen, saját lekérdezéssel: legalább 20 véletlen `rahlfs_igazolt` és 10 `nem_igazolt:*` sor összevetése az LXX_OS-szel és a forrásalakkal.
- Merge csak a felhasználótól.

## 4. Elfogadási feltételek

- **G1.** A 3.1 reprodukálhatósági diffje 0 (vagy a felhasználó döntött a ⛔0-nál).
- **G2.** Minden sorban `gorog_lxx_forras` = upstream `greek` (betűre); a χ/ξ-mentes sorokban `gorog_lxx` = `gorog_lxx_forras` és `gorog_lxx_rahlfs` üres.
- **G3.** Minden χ/ξ-s sorban `gorog_lxx` = `gorog_lxx_forras` χ↔ξ (Χ↔Ξ) cseréje, betűre; más karakter nem változik.
- **G4.** Jelölten üres mező nincs: ahol `gorog_lxx_forras` nem üres, ott `gorog_lxx` sem; minden χ/ξ-s sornak van `gorog_lxx_rahlfs` értéke.
- **G5.** Az `eredeti_igazolt` és a `ketertelmu` száma 0; az érintett sorok és a `gorog_lxx_rahlfs` osztályai a 3.3 várt értékeitől ±1%-on belül vannak (különben a ⛔1-nél megállás történt, és a felhasználó döntött).
- **G6.** A diff-őr szerint csak a megengedett oszlopok változtak.
- **G7.** A `pardes.db` újraépült; a `python eszkozok/teszt_futtat.py` zöld; a tesztkimenet és a megnyitott adatbázis naplózva.
- **G8.** A „Héber–görög párosítás (Macula)” táblázatban nincs χ↔ξ-hibás alak; a nem `rahlfs_igazolt` soroknál a jelölő megjelenik (3 vers, kézzel és teszttel).

## 5. Döntésnapló

| Azonosító | Tárgy | Állapot |
|---|---|---|
| DT-F115a | A javítási szabály: teljes χ↔ξ (Χ↔Ξ) csere minden χ/ξ-s `gorog_lxx` sorban, az import-lépésben; a forrásalak a `gorog_lxx_forras` oszlopban; a Rahlfs-igazolás soronkénti minőségjelölés (`gorog_lxx_rahlfs`: `rahlfs_igazolt` / `nem_igazolt:<ok>`), nem feltétel; jelölten üres mező nem keletkezik; megállás, ha a Rahlfs bárhol az eredeti alakot igazolja, kétértelmű sor jelenik meg, vagy az osztályszámok ±1%-nál jobban eltérnek a felméréstől. Indok: 19 876 érintett sorból 0-ban igazolja a Rahlfs az eredeti alakot, 0 kétértelmű (`naplok/MACULA_CHI_XI_felmeres.md`). | a felhasználó döntötte el (2026-10-18); a menet rögzíti a `DONTESEK.md`-ben |
| N-F115a | Upstream jelzés a Clear-Bible/macula-hebrew-nak a `greek` attribútum χ↔ξ cseréjéről | javaslat; a felhasználó dönt (nyilvános megszólalás) |
| N-F115b | LXX_OS Károli-kulcsrés: 29 Én- és 21 Préd-sornak nincs Károli-kulcsa vagy LXX_OS-verse (napló 5. szakasz) | külön tétel, ha a felhasználó kéri |
