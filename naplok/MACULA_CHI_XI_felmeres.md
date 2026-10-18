# MACULA_CHI_XI_felmeres.md — a Macula `gorog_lxx` χ↔ξ cseréjének felmérése

*2026.10.18 · felmérő menet (csak olvas; adat és generált fájl nem változott) · modell: claude-opus-5-5 · a javító brief: `F115_MACULA_CHI_XI_BRIEF.md` · előzmény: `NYITOTT_FELADATOK.md` „2026.10.05, olvasói prototípus” tétel*

## 0. Összefoglaló

- **A hiba forrásoldali.** A pinelt upstream XML (Clear-Bible/macula-hebrew@47db250b, `WLC/lowfat/01-Gen-001-lowfat.xml`) `greek` attribútumában `ἀρξ` 4 / `ἀρχ` 0, `ψυξ` 4 / `ψυχ` 0, `χύλ` 3 / `ξύλ` 0. Az `eszkozok/f17/macula_futtat.py:101` a `greek` attribútumot változtatás nélkül írja a `gorog_lxx` oszlopba; a `macula_kozos.tisztit()` (`eszkozok/f17/macula_kozos.py:62`) csak tabot és sortörést cserél.
- **A csere teljes, nem „szinte teljes”.** 19 876 sor tartalmaz χ-t vagy ξ-t. **Egyetlen sorban sem igazolja a Rahlfs az eredeti alakot, és kétértelmű sor sincs** (A és B változatban is 0). A 2026-10-05-i mérés „5 helyes `ψυχ`” sora is hibás. Ezek a ψύχω / ἀνάψυξις alakjai: `ἔψυχα` → `ἔψυξα`, `ἀνέψυχαν` → `ἀνέψυξαν`, `ἀνάψυχις` → `ἀνάψυξις`. Mind az öt `igazolt_csere`.
- **Betűre (NFC) igazolt csere: 17 497 / 19 876 = 88,0%** (A: alak a Károli-versben). Ha ugyanazon a tokenen a Strong is egyezni köteles (B): 16 468 = 82,9%. A különbség 1 029 sor, ahol az alak betűre egyezik, de a Strong-kódolás tér el (pl. `χρυσᾶ`: Macula G5552, LXX_OS más). Ez nem alakhiba.
- **A nem igazolt maradék oka szinte mindig a Macula és a Rahlfs általános eltérése, nem a csere.**
  - Csak kis- és nagybetűben tér el 2 004 sor (10,1%). Ezek a Macula kisbetűs tulajdonnevei (`ισσαξαρ` → Rahlfs `Ισσαχαρ`).
  - Csak ékezetben tér el 30 sor, főleg a Préd.
  - Nincs egyezés a versben 147 sorban; Dán 3 és Ézs: eltérő LXX-szövegforma vagy versszám.
  - Nincs Károli-kulcs 158 sorban, nincs LXX_OS-vers 40 sorban.
  - Minden laza illeszkedés a **csere** oldalán van, az eredetién soha (`(csere)` utótag a táblában).
  - A nem igazolt sorok csere-alakja 311 / 345 esetben a teljes LXX_OS-ben betűre előfordul, az eredeti alak egyszer sem (lásd 3. szakasz).
- **Kontroll.** A χ/ξ-mentes, nem üres sorok közül azokban, amelyeknek van LXX-verse, 91,1% egyezik betűre a Rahlfs-szal. A χ/ξ-s sorok 88,0%-os igazolt aránya tehát ugyanennek a felső korlátnak a közelében van. A maradék nem csere-specifikus.

## 1. Upstream-újraigazolás

- Letöltve a repón kívülre (session scratchpad): `https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/47db250bd55d0d8577f2a94fba114ef16c35b23c/WLC/lowfat/01-Gen-001-lowfat.xml`, 640 186 bájt, sha256 `523856a1f2953408d847e8d3fcc231f2bd681e540aa91c349cd9c4e128f30f60`.
- Számolás: `python eszkozok/macula_chi_xi_felmeres.py --upstream-xml <fájl> --tovek "ἀρξ,ἀρχ,ψυξ,ψυχ,χύλ,ξύλ"`. Az eredmény a 2. szakasz „(1) Upstream XML” része.
- *(proveniencia: scope=macula-hebrew@47db250b WLC/lowfat/01-Gen-001-lowfat.xml (`greek` attribútum) | forras=eszkozok/macula_chi_xi_felmeres.py --upstream-xml | ts=2026-10-18)*
- A mérés egyezik a 2026-10-17-i orkesztrátori méréssel (`ἀρξ`/`ἀρχ` 4/0).

## 2. A mérés kimenete (változtatás nélkül)

**Módszer.** A Macula-sor `karoli` versei (`;`-vel tagolva) megadják az LXX_OS ugyanazon `igehely_karoli` kulcsú tokenjeit, minden szövegformában (Józs/Bír/Dán párhuzamos változatai is). A Maculában nincs LXX-tokenazonosító, mert a `greek` attribútum mellett nincs pozíció-mutató. A „hely” ezért a Károli-vers; a szó egyezése betűre (NFC) értendő.
- **A változat:** van-e a versben ilyen alakú token.
- **B változat:** az alak és a Strong ugyanazon a tokenen egyezik.
- Ha az eredeti és a csere-alak is megvan a versben, a sor `ketertelmu` (nem találgatunk). Ez 0 sor.

### (1) Upstream XML

`01-Gen-001-lowfat.xml`: `greek` attributummal bíró `<w>` elem: 601
- `ἀρξ`: 4
- `ἀρχ`: 0
- `ψυξ`: 4
- `ψυχ`: 0
- `χύλ`: 3
- `ξύλ`: 0

### (2) Macula `gorog_lxx` vs. Rahlfs (LXX_OS)

- összes sor: 475911; nem üres `gorog_lxx`: 373897
- χ-t vagy ξ-t tartalmazó (érintett) sor: 19876 (χ-s: 7681, ξ-s: 12275)
- kontroll (χ/ξ nélküli nem üres sor): LXX-verssel 347705, ebből betűre egyező 316807 (91.1%); LXX-vers nélkül 6316
- tövek (szóelőfordulás): `ξηρ` 16, `χηρ` 99, `χύλ` 261, `ψυξ` 688, `ψυχ` 5, `ἀρξ` 250, `ἀρχ` 3

| osztály | A (alak) | A % | B (alak + Strong) | B % |
|---|---:|---:|---:|---:|
| `igazolt_csere` | 17497 | 88.0% | 16468 | 82.9% |
| `nem_igazolt:nincs_karoli` | 158 | 0.8% | 158 | 0.8% |
| `nem_igazolt:nincs_lxx_vers` | 40 | 0.2% | 40 | 0.2% |
| `nem_igazolt:strong_elteres(csere)` | 0 | 0.0% | 1029 | 5.2% |
| `nem_igazolt:csak_kisbetu(csere)` | 2004 | 10.1% | 2004 | 10.1% |
| `nem_igazolt:csak_ekezet(csere)` | 30 | 0.2% | 30 | 0.2% |
| `nem_igazolt:nincs_egyezes` | 147 | 0.7% | 147 | 0.7% |

Igazoló szövegforma (B, szavanként): psalms-lxx 1606, ezekiel 1109, jeremiah-lxx 1061, isaiah 953, exodus 936, numbers 879, genesis 795, leviticus 776, 2-chronicles 749, deuteronomy 728, 1-samuel 608, 1-kings 586, 2-kings 563, job-lxx 557, 1-chronicles 513, 2-samuel 503, 2-esdras 490, proverbs 450, judges,judges-vaticanus-b 374, joshua-vaticanus-b 313, judges-vaticanus-b 227, zechariah 207, daniel 155, amos 132, lamentations 131, esther-greek 119, hosea 115, micah 100, ecclesiastes 100, joel 89, daniel,daniel-theodotion 78, habakkuk 74, ruth 65, malachi 60, song-of-solomon 59, jonah 44, nahum 42, zephaniah 42, haggai 34, obadiah 20, joshua,joshua-vaticanus-b 14, daniel-theodotion 12

### Könyvenként

| könyv | érintett | A igazolt_csere | A % | B % | A igazolt_eredeti | A kétértelmű | A csak kis/nagybetű | A csak ékezet | A nincs egyezés | nincs Károli/LXX-vers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Abdias | 22 | 21 | 95.5% | 90.9% | 0 | 0 | 1 | 0 | 0 | 0 |
| Aggeus | 35 | 35 | 100.0% | 97.1% | 0 | 0 | 0 | 0 | 0 | 0 |
| Amos | 144 | 143 | 99.3% | 91.7% | 0 | 0 | 1 | 0 | 0 | 0 |
| Birak | 760 | 634 | 83.4% | 79.1% | 0 | 0 | 126 | 0 | 0 | 0 |
| Daniel | 336 | 260 | 77.4% | 72.9% | 0 | 0 | 58 | 0 | 18 | 0 |
| Deuteronomium | 815 | 782 | 96.0% | 89.3% | 0 | 0 | 29 | 0 | 4 | 0 |
| Enekek_Eneke | 93 | 61 | 65.6% | 63.4% | 0 | 0 | 0 | 0 | 3 | 29 |
| Eszter | 190 | 129 | 67.9% | 62.6% | 0 | 0 | 56 | 0 | 2 | 3 |
| Exodus | 1104 | 1028 | 93.1% | 84.8% | 0 | 0 | 27 | 1 | 3 | 45 |
| Ezekiel | 1207 | 1171 | 97.0% | 91.9% | 0 | 0 | 32 | 0 | 4 | 0 |
| Ezsaias | 1080 | 990 | 91.7% | 88.2% | 0 | 0 | 31 | 3 | 45 | 11 |
| Ezsdras | 234 | 199 | 85.0% | 79.1% | 0 | 0 | 35 | 0 | 0 | 0 |
| Genezis | 1141 | 848 | 74.3% | 69.7% | 0 | 0 | 290 | 0 | 2 | 1 |
| Habakuk | 76 | 75 | 98.7% | 97.4% | 0 | 0 | 1 | 0 | 0 | 0 |
| Hoseas | 150 | 119 | 79.3% | 76.7% | 0 | 0 | 3 | 0 | 13 | 15 |
| Jeremias | 1219 | 1101 | 90.3% | 87.0% | 0 | 0 | 114 | 0 | 3 | 1 |
| Job | 596 | 584 | 98.0% | 93.5% | 0 | 0 | 7 | 0 | 0 | 5 |
| Joel | 91 | 91 | 100.0% | 97.8% | 0 | 0 | 0 | 0 | 0 | 0 |
| Jonas | 46 | 45 | 97.8% | 95.7% | 0 | 0 | 0 | 0 | 1 | 0 |
| Jozsue | 496 | 357 | 72.0% | 65.9% | 0 | 0 | 134 | 0 | 4 | 1 |
| Kiralyok_1 | 784 | 641 | 81.8% | 74.7% | 0 | 0 | 115 | 0 | 8 | 20 |
| Kiralyok_2 | 758 | 614 | 81.0% | 74.3% | 0 | 0 | 144 | 0 | 0 | 0 |
| Kronikak_1 | 817 | 552 | 67.6% | 62.8% | 0 | 0 | 262 | 0 | 3 | 0 |
| Kronikak_2 | 961 | 841 | 87.5% | 77.9% | 0 | 0 | 118 | 0 | 2 | 0 |
| Leviticus | 802 | 799 | 99.6% | 96.8% | 0 | 0 | 3 | 0 | 0 | 0 |
| Malakias | 63 | 62 | 98.4% | 95.2% | 0 | 0 | 1 | 0 | 0 | 0 |
| Mikeas | 113 | 109 | 96.5% | 88.5% | 0 | 0 | 3 | 0 | 1 | 0 |
| Nahum | 47 | 47 | 100.0% | 89.4% | 0 | 0 | 0 | 0 | 0 | 0 |
| Nehemias | 370 | 309 | 83.5% | 82.4% | 0 | 0 | 61 | 0 | 0 | 0 |
| Numeri | 1078 | 929 | 86.2% | 81.5% | 0 | 0 | 120 | 0 | 3 | 26 |
| Peldabeszedek | 480 | 461 | 96.0% | 93.8% | 0 | 0 | 1 | 1 | 2 | 15 |
| Predikator | 156 | 109 | 69.9% | 64.1% | 0 | 0 | 0 | 25 | 1 | 21 |
| Ruth | 76 | 66 | 86.8% | 85.5% | 0 | 0 | 9 | 0 | 1 | 0 |
| Samuel_1 | 718 | 648 | 90.3% | 84.7% | 0 | 0 | 69 | 0 | 1 | 0 |
| Samuel_2 | 661 | 534 | 80.8% | 76.1% | 0 | 0 | 127 | 0 | 0 | 0 |
| Siralmak | 147 | 133 | 90.5% | 89.1% | 0 | 0 | 0 | 0 | 14 | 0 |
| Sofonias | 48 | 44 | 91.7% | 87.5% | 0 | 0 | 3 | 0 | 1 | 0 |
| Zakarias | 238 | 224 | 94.1% | 87.0% | 0 | 0 | 12 | 0 | 0 | 2 |
| Zsoltarok | 1724 | 1702 | 98.7% | 93.2% | 0 | 0 | 11 | 0 | 8 | 3 |

### A `ψυχ`-tövű sorok (a 2026-10-05-i mérés „5 helyes” sora)

| ref | Károli | gorog_lxx | csere | A osztály |
|---|---|---|---|---|
| EXO 8:11!5 | 2Móz 8:15 | ἀνάψυχις | ἀνάψυξις | `igazolt_csere` |
| 2KI 19:24!2 | 2Kir 19:24 | ἔψυχα | ἔψυξα | `igazolt_csere` |
| NUM 11:32!18 | 4Móz 11:32 | ἔψυχαν | ἔψυξαν | `igazolt_csere` |
| 2SA 16:14!8 | 2Sám 16:14 | ἀνέψυχαν | ἀνέψυξαν | `igazolt_csere` |
| 2SA 17:19!9 | 2Sám 17:19 | ἔψυχεν | ἔψυξεν | `igazolt_csere` |

*(proveniencia: scope=konkordancia/Macula_heber_*.tsv (gorog_lxx) × konkordancia/LXX_OS/*.tsv (igehely_karoli, minden szövegforma) | forras=eszkozok/macula_chi_xi_felmeres.py | ts=2026-10-18)*

## 3. A nem igazolt sorok a teljes LXX_OS-szókincsen (diagnosztika, nem igazolás)

A B változat 345 `nincs_*` során (nincs egyezés a versben, nincs Károli-kulcs, nincs LXX-vers) megnéztük, előfordul-e a csere-alak, illetve az eredeti alak bárhol az LXX_OS `szoalak` oszlopában. Ez szkript-mérés (`globalis.py` a session scratchpadban), a repóba nem került.

| osztály | csere betűre | csere csak kisbetűvel | egyik sem | az eredeti bárhol |
|---|---:|---:|---:|---:|
| `nincs_egyezes` (147) | 128 | 6 | 13 | 0 |
| `nincs_karoli` (158) | 147 | 1 | 10 | 0 |
| `nincs_lxx_vers` (40) | 36 | 2 | 2 | 0 |

*(proveniencia: scope=a 345 B-osztályú `nincs_*` sor × konkordancia/LXX_OS/*.tsv `szoalak` (összes fájl) | forras=manual (scratchpad-szkript, 2026-10-18) | ts=2026-10-18)*

A szótári előfordulás **nem helyigazolás**. A javító brief szerint ezek a sorok jelölten üresek maradnak. A tábla csak azt mutatja, hogy a „nem igazolt” itt a helyhiány jele, nem az alaké.

## 4. Fogyasztók — ki olvassa a `gorog_lxx` / `lxx_szo` mezőt

| fájl:sor | szóalakként használja? | megjelenik-e ma, hol |
|---|---|---|
| `eszkozok/f17/macula_futtat.py:101` | előállítja (a `greek` nyersen) | `konkordancia/Macula_heber_*.tsv` |
| `eszkozok/f17/macula_futtat.py:103,289` | igen | `naplok/F17_87_hely.tsv` (a 87 függő hely, nyers Macula-alak) |
| `eszkozok/sqlite_epit.py:991,1004` | betölti: `gorog_lxx` → `token_macula.lxx_szo` | közvetlenül nem |
| `eszkozok/olvaso_szerver/lekerdezesek.py:234-239` `macula()` | igen, `lxx` kulcs | a lenti blokkokon át |
| `eszkozok/olvaso_szerver/blokkok.py:227-229` `_r_macula_gorog` | **igen, nyersen** | **IGEN, mindig:** vers-lap, „Héber–görög párosítás szavanként (Macula)”, „Görög (Macula)” oszlop (`vers.macula_gorog`, `blokkok.py:1156`) |
| `eszkozok/olvaso_szerver/blokkok.py:425-442` `_heber_csempek`, `_r_heber_csempe` (464-477) | párosít, és az alakot az LXX_OS-ből cseréli | **esetenként:** a héber csempék alatti görög alak. A Macula-alak marad, ha nincs `lxx_strong`, vagy nincs azonos Strongú LXX-token legfeljebb 1 betűnyi ékezetlen eltéréssel. Két χ/ξ-vel a távolság 2, ilyenkor sincs csere. |
| `eszkozok/olvaso_szerver/blokkok.py:518-543` `_r_ebben` | ugyanaz | esetenként: szó-lap, „Görögül ebben a versben (LXX)” |
| `eszkozok/olvaso_szerver/blokkok.py:486` `_r_lxx_csempe` | nem, csak LXX_OS | nem érintett (Septuaginta-csempék) |
| `eszkozok/olvaso_pilot/adat.py:340,389-407` | igen (`r[13]` a TSV-ből) | pilot HTML; `lxx_forras='Macula'` visszaesésnél, `lxx_macula` = nyers alak |
| `eszkozok/olvaso_pilot/meres.py:104-116,265`, `db_meres.py:119,265` | igen (számlál, összevet) | mérési napló, csak darabszámok |
| `eszkozok/olvaso_mockup/konk_kinyer.py:23`, `nav_kinyer.py:23`, `minta.py:9` | igen | mockup HTML (a generált mockup nincs a repóban) |
| `eszkozok/f08/f08_bemenet.py:60,64` | igen | `naplok/F08_bemenet.txt`: 3 hibás alak, a 10., 76. és 208. sorban (`ψυξὴν`, `ψυξῆς`, `ἀρξόντων`); történeti napló |
| `eszkozok/lexikon_general.py:1803` `blokk_lxx` | **nem**: LXX_OS + `adat/lxx_dontesek.tsv` | a lexikon nem érintett |

**Tesztek.** Az `eszkozok/olvaso_pilot/teszt_olvaso_pilot.py:88,90` elvárt értéke `lxx_macula = 'ἀρξῇ'`, vagyis a hibás alakot rögzíti. Az `eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py:233` a „Görögül ebben a versben” szöveget veti össze. Az `eszkozok/olvaso_szerver/teszt_olvaso_szerver.py:187` csak a blokk helyét nézi. Az `lxx_szo` értékét egyetlen teszt sem ellenőrzi.

**Generált kimenet.** A `lexikon/` és a `generalt_proba/` alatt nincs hibás alak (grep `ψυξ`, `ἀρξ`). Egyedül a `naplok/F08_bemenet.txt` hordozza.

*(proveniencia: scope=eszkozok/, lexikon/, generalt_proba/, naplok/ (grep: gorog_lxx, lxx_szo, Macula_heber, token_macula, ψυξ, ἀρξ) | forras=manual (Explore-ügynök + kézi ellenőrzés) | ts=2026-10-18)*

## 5. Megjegyzések a javításhoz

> **Utólagos döntés (2026-10-18, a felhasználó):** teljes χ↔ξ csere minden érintett sorban; a Rahlfs-igazolás soronkénti minőségjelölés (a B változat osztályai), nem feltétel; jelölten üres mező nem keletkezik. Az alábbi három pont (a feltételes szabály v1-es érvelése) ezzel történeti; az érvényes szabály: `F115_MACULA_CHI_XI_BRIEF.md` v2, `DT-F115a`.

- A javítás illesztési kulcsa a Károli-vers, mert pozíció-mutató nincs. 0 kétértelmű sor mellett ez elegendő. A brief mégis előírja a kétértelműség-őrt.
- A B változat (Strong-egyezés) 1 029 sort vesztene el úgy, hogy közben egyetlen hibát sem szűrne ki. A javasolt szabály ezért az A változat.
- A kis- és nagybetű-tolerancia 2 004 sort (10,1%) hozna be. Ezek a Macula kisbetűs tulajdonnevei. Az elfogadásuk felhasználói döntés (brief ⛔1). A felhasználó irányelve „betűre” szól.
- Mellékleletek, nem e tétel hatóköre:
  - 29 Én és 21 Préd sornak nincs Károli-kulcsa vagy LXX_OS-verse (kulcsrés).
  - A Dán 3 és az Ézs 9 Macula-görögje más szövegformát követ.
