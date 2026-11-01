---
feladat: 114
cim: A TSK-kereszthivatkozások Károli-versszámra váltása (TSK_VERSSZAM)
kod: TSK_VERSSZAM
tipus: feladat
fazis: folyamat
munka: adat
modell: sonnet
allapot: lezarva
ag: claude/tsk-versszam
ad: a TSK forrás- és célkulcsa mind az öt fogyasztóban egy közös átváltón át Károli-versszámon áll (a dataset érintetlen); a felmérőszkript az ÓSZ-en 0 rossz és 0 elmaradó sort mér, az N-F09g lezárható
kovetkezo: lezárva; Te: a PR #398 merge-e
pr: https://github.com/basesoft777/Bible-Study/pull/398
lezarva_osszegzes: tsk_kulcs átváltó, öt fogyasztó Károli-kulcson; ÓSZ 0 rossz / 0 elmaradó (a kivétel-verseken körkörös); DT199–e; négy ellenőrzés, a maradék kimondott korlát (N-F54a, N-F114a, N-F114b); zárójelentés: naplok/TSK_VERSSZAM_zaras.md
olvas: [konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/TSK_kereszthivatkozasok_README.md, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_1908.tsv, eszkozok/lexikon_general.py, eszkozok/lekerdez.py, eszkozok/nem_vizsgalt.py, eszkozok/sqlite_epit.py, eszkozok/olvaso_pilot/adat.py, eszkozok/tsk_versszam_felmeres.py, eszkozok/render_diff_osztalyoz.py, eszkozok/teszt_render_diff_osztalyoz.py, naplok/TSK_VERSSZAM_felmeres.md, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/SEMA.md, lexikon/ALVIL-001_TUDOMANYOS.md, archivum/ALVIL-001/ALVIL-001_torzscikk_regi.md, lexikon/TEREMT-001_TUDOMANYOS.md]
ir: [eszkozok/tsk_kulcs.py, eszkozok/teszt_tsk_kulcs.py, eszkozok/lexikon_general.py, eszkozok/lekerdez.py, eszkozok/nem_vizsgalt.py, eszkozok/sqlite_epit.py, eszkozok/olvaso_pilot/adat.py, eszkozok/tsk_versszam_felmeres.py, eszkozok/render_diff_osztalyoz.py, eszkozok/teszt_render_diff_osztalyoz.py, konkordancia/TSK_kereszthivatkozasok_README.md, adat/jeloltek.tsv]
fugg: []
nem_fugg: [11, 36, 101]
---
# F114_TSK_VERSSZAM_BRIEF.md — A TSK-kereszthivatkozások Károli-versszámra váltása

*FELADATOK #114 · Modell: sonnet · v1 · 2026.10.18 · előzmény: `naplok/TSK_VERSSZAM_felmeres.md` (2026-10-17), N-F09g (#9, PR #381)*

## 1. Cél

A `konkordancia/TSK_kereszthivatkozasok.tsv` **mindkét kulcsa** (`Igehely` és `Kapcsolódó igehely`) KJV-számozású, a könyvnév viszont magyar. Öt fogyasztó átváltás nélkül, Károli-kulcsként olvassa:

| Fogyasztó | Hely (main, 2026-10-17) | Mire használja |
|---|---|---|
| `eszkozok/lexikon_general.py` | `tsk_index()`, `blokk_kereszthivatkozasok()` | a lexikon kereszthivatkozás-blokkja |
| `eszkozok/lekerdez.py` | `cmd_tsk()` | a `lekerdez.py tsk` CLI |
| `eszkozok/nem_vizsgalt.py` | `tsk_kor()` | a lelet-lap TSK-köre |
| `eszkozok/sqlite_epit.py` | `_kereszthivatkozasok()` | a `pardes.db` `tsk` táblája (olvasó-szerver) |
| `eszkozok/olvaso_pilot/adat.py` | 168–171. sor | a pilot-olvasó TSK-oszlopa |

A felmérés mért kára (`naplok/TSK_VERSSZAM_felmeres.md`; `proveniencia: scope=TSK-teljes | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=432949 | ts=2026-10-17`):

- a teljes TSK-ban **1 502 ÓSZ-forráskulcs, 23 150 sor** esik rossz (vagy nem létező) Károli-versre; céloldalon 23 540 sor mutat eltérő számozású versre;
- az `adat/elofordulasok.tsv`-ben **18 vers érintett, 6 motívumban** (ALVIL-001, TEREMT-001, HODIT-001, MENNY-001, HAMART-001, KIRALY-001); a ≥ 15-ös lexikonblokkban 10 sor rossz versről jön, 18 elmarad (pl. ALVIL-001 `Préd 9:12` = KJV 9:10: 12 sor elmarad; `Zsolt 18:6`: 6 sor rossz versről);
- a **17 tartomány-igehely** (pl. `1Móz 14:18-20`) egyáltalán nem kap TSK-t (a `tsk_index()` pontos kulcsra keres; ez nem versszám-hiba, de ugyanazt a függvényt érinti);
- a `jeloltek.tsv`-ben `beépítve` sor nem érintett; **7 elutasított HAMART-001-jelölt** KJV-kulcson áll;
- **az ÚSZ-oldal nincs mérve**: a `konkordancia/Karoli_versmegfeleltetes.tsv` csak az ÓSZ-t fedi (39 könyv), a felmérés ott azonosságot feltételezett (alsó becslés: 0).

A cél: **egyetlen közös átváltó modul**, amelyet mind az öt fogyasztó használ, mindkét kulcsra. **A dataset nem módosul**: a forrásfájl KJV-kulcsú marad, ahogy a README leírja; az átváltás olvasáskor történik.

## 2. Hatókör

**Benne van:**
- `eszkozok/tsk_kulcs.py`: KJV→Károli és Károli→KJV versátváltás a `Karoli_versmegfeleltetes.tsv`-ből. Egy KJV-vers több Károli-versre is mehet (és fordítva); a „nincs pár” eset explicit visszatérési érték, nem csendes azonosság. Az ÚSZ kezelése a ⛔ 3.1 döntése szerint. A TSV-olvasás `split('\t')` (CLAUDE.md, TSV-szakasz). Egységteszt: `eszkozok/teszt_tsk_kulcs.py`;
- az öt fogyasztó átállítása: a forrásoldalon a Károli-vers KJV-kulcsával keres, a céloldalt megjelenítés előtt Károli-kulcsra váltja; a nyers `Igehely`/`Kapcsolódó igehely` mezőt egyik sem olvassa a modul megkerülésével;
- a `konkordancia/TSK_kereszthivatkozasok_README.md` kiegészítése a kulcsolás tényével és az átváltó nevével (a TSV nem változik);
- a felmérőszkript (`eszkozok/tsk_versszam_felmeres.py`) kiegészítése úgy, hogy a javított átváltón át is mérjen (elfogadási mérés, 4.);
- **kapcsolódás a #9 N-F09g-hez:** az ALVIL-001 próbagenerálása után a `#### Préd 9:12` alatt visszatér a 12 TSK-sor és a törzscikk összevont TSK-sora; ezután az `eszkozok/render_diff_osztalyoz.py` `ISMERT_HIBA_TSK_VERSSZAM` listája (13 sor) és az `ismert_hiba_tsk_versszam` kategória kivezetendő, a `teszt_render_diff_osztalyoz.py` két érintett tesztjével (`test_ismert_hiba_tsk`, `test_tabla_merete` 13-as állítása) együtt;
- a 7 HAMART-001-jelölt kezelése a ⛔ 3.6 döntése szerint.

**Nincs benne:**
- a TSK-dataset bármilyen módosítása vagy átkulcsolt másolata;
- az ÚSZ-versmegfeleltetés elkészítése, ha a ⛔ 3.1 a korlátot választja (akkor N-F114a);
- a tartomány-igehelyek TSK-keresése: külön tétel, **N-F114b** (l. 5.); a `tsk_index()` átírása ne zárja ki a későbbi tartomány-kibontást, de ne is valósítsa meg;
- az éles `lexikon/` újragenerálása (a #36 vagy a #10 dolga, DT186) és a `pardes.db` újraépítése (#101); a próbagenerálás a repón kívülre megy (`--kimenet`, CLAUDE.md);
- a `jeloltek.tsv` bármely más sora.

## 3. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév kiírása és összevetése a fejléc `modell` mezőjével; eltérésnél megállás. Előtte a meglévő ág/worktree keresése a feladathoz.
1. ⛔ **ÚSZ-oldal.** A `Karoli_versmegfeleltetes.tsv` csak az ÓSZ-t fedi; ismert ÚSZ-eltérések lehetnek (pl. 2Kor 13:12–14, 3Ján 14–15, Róm 16 vége, Jel 12:18/13:1). Két út: **(a) mérés előbb** — a TSK ÚSZ-forrású sorainak összevetése a Károli 1908 ÚSZ-versszerkezetével (verszám-létezés és fejezetvégek), mérőszkripttel, és ha eltérés van, ÚSZ-megfeleltetés a dataset-szabályok szerint (`Rendszerfejlesztesi_playbook.md` 2. pont); **(b) kimondott korlát** — az átváltó az ÚSZ-en azonosságot ad, ezt a modul docstringje, a README és a jelentés kimondja, és N-F114a nyitott tétel marad. Tétel a `DONTESEK.md`-be (**DT197**), megállás.
2. **F114.1:** `eszkozok/tsk_kulcs.py` + `eszkozok/teszt_tsk_kulcs.py`. Esetek legalább: Préd 9:12 ↔ KJV 9:10; Zsolt 18:6 ↔ KJV 18:5; zsoltárfelirat (Károli-vers KJV-pár nélkül → explicit „nincs pár”); 4Móz 13:34 ↔ KJV 13:33; egy-a-többhöz eset (ha a tábla tartalmaz ilyet; ha nem, a teszt ezt rögzíti); ÚSZ a 3.1 szerint.
3. **F114.2:** a `lexikon_general.py` és a `lekerdez.py` átállítása. Igazolás: `lekerdez.py tsk "Préd 9:12"` a Kol 3:23-at (Votes 71) adja; `lekerdez.py tsk "Zsolt 18:6"` nem adja a Zsolt 50:15-öt; a céloldalon Károli-kulcs áll (pl. `Zsolt 16:10` → `Zsolt 49:16`, nem 49:15). A parancsok proveniencia-sorai a jelentésbe.
4. **F114.3:** a `nem_vizsgalt.py`, a `sqlite_epit.py` és az `olvaso_pilot/adat.py` átállítása. Az olvasó-szerver tesztjei csak `python eszkozok/teszt_futtat.py --gyors` hívással (CLAUDE.md).
5. **F114.4 — elfogadási mérés:** a `tsk_versszam_felmeres.py` újrafuttatása a javított átváltón át. Elvárás az ÓSZ-en: a B-rész „rossz versről” = 0 és „elmarad” = 0 (minden Votes-értéken és ≥ 15-ön is); az A-részben a fogyasztói úton olvasott kulcsok 0 rossz versre esnek (a „nincs pár” kulcsok külön számolva, tételesen). Ha nem 0: megállás, tételes lista. Az ALVIL-001 és a TEREMT-001 próbagenerálása a repón kívülre (`--kimenet`), összevetés a felmérés B-táblájával: `#### Préd 9:12` alatt a 12 TSK-sor (Kol 3:23 … Ézs 38:19, `NYITOTT_FELADATOK.md` N-F09g listája) és a törzscikk összevont sora; `#### Zsolt 18:6` alatt nincs Zsolt 50:15; `Zsolt 36:7` alatt nincs Ruth 2:12. Jelentés: `naplok/TSK_VERSSZAM_jelentes.md`, proveniencia-sorokkal.
6. **F114.5 — N-F09g kivezetése:** a `render_diff_osztalyoz.py` futtatása a próbán; az `ISMERT_HIBA_TSK_VERSSZAM` 13 sorának egyike sem lehet törölt sor. Ezután a lista, az `ismert_hiba_tsk_versszam` kategória és a hozzá tartozó ágak (`proba_osztalyoz` és társai) törlése, a tesztek frissítése; a teljes tesztkészlet zöld. Ha a próbán a 13 sorból bármelyik még törölt: megállás.
7. ⛔ **A 7 elutasított HAMART-001-jelölt kulcsa** (`jeloltek.tsv`; forrás: `Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` §4/b, 2026-10-11). Mai `igehely` (KJV-kulcs) → a tartalom szerinti Károli-vers: `Préd 9:3` → 9:5, `Préd 2:11` → 2:12, `Préd 2:17` → 2:18, `Préd 2:22` → 2:23, `Préd 2:23` → 2:24, `Zsolt 140:11` → 140:12, `Zsolt 55:9` → 55:10 (a felmérés C-része, Károli 1908-összevetés, `scope=manual`). Lehetőségek: **(a)** átkulcsolás Károli-versre, az `indoklas` végén hivatkozással (DT108-minta), írás előtti sor-összevetéssel (`eszkozok/igazolas_migracio.py` minta); a Préd 2:22 → 2:23 és 2:23 → 2:24 csak csökkenő sorrendben ütközésmentes (kulcs: id + igehely); **(b)** a sorok maradnak, csak napló-megjegyzés a jelentésben; **(c)** más. Tétel a `DONTESEK.md`-be (**DT199**), megállás; a `jeloltek.tsv` a döntés előtt nem változik.
8. Független ellenőrzés (`fuggetlen-ellenor`), PR. Lezáráskor az N-F09g a `NYITOTT_FELADATOK.md`-ben lezártnak jelölve, hivatkozással erre a feladatra.

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| E1 | A TSK `Igehely`/`Kapcsolódó igehely` mezőjét egyik fogyasztó sem olvassa a `tsk_kulcs` megkerülésével (grep-igazolás a jelentésben, az öt fájlra). |
| E2 | A `konkordancia/TSK_kereszthivatkozasok.tsv` bájtra változatlan (hash a jelentésben). |
| E3 | A felmérőszkript a javított átváltón át az ÓSZ-en 0 rossz és 0 elmaradó sort ad (B-rész, minden Votes-érték és ≥ 15); a „nincs pár” kulcsok tételesen. |
| E4 | Az ALVIL-001 próbalexikonában a `#### Préd 9:12` alatt a 12 TSK-sor áll (Kol 3:23, Votes 71 az első), a törzscikkben az összevont TSK-sor; a `#### Zsolt 18:6` alatt nincs Zsolt 50:15. |
| E5 | Az `ISMERT_HIBA_TSK_VERSSZAM` és az `ismert_hiba_tsk_versszam` kategória kivezetve; a `teszt_render_diff_osztalyoz.py` és a `teszt_tsk_kulcs.py` zöld; az olvasó-szerver tesztjei (`teszt_futtat.py --gyors`) zöldek. |
| E6 | Az ÚSZ kezelése a DT197 szerint: vagy mért eredmény, vagy kimondott korlát a modulban, a README-ben és a jelentésben. |
| E7 | Adattábla (`adat/*.tsv`) csak a DT199 döntése szerint változik; a `jeloltek.tsv` minden más sora bájtra azonos. |

## 5. Döntésnapló

- **DT199:** a 7 elutasított HAMART-001-jelölt kulcsa (3.7 ⛔).
- **DT197:** az ÚSZ-oldal — mérés előbb, vagy kimondott korlát (3.1 ⛔).
- **N-F114a** (csak ha a DT197 a korlát): ÚSZ Károli↔KJV versmegfeleltetés hiánya; a TSK ÚSZ-oldala nem ellenőrzött.
- **N-F114b:** a `lexikon_general.tsk_index()` tartomány-igehelyre nem keres: a 17 tartomány-sor nem kap TSK-t, ebből 7 versére volna ≥ 15 találat (felmérés B2). Javaslat: a tartomány versenkénti kibontása, a találatok uniója a legmagasabb Votes-értékkel; külön feladat vagy a #36 előtti kis tétel.
- Kapcsolódó: **N-F09g** (#9) ennek a feladatnak a lezárásával zárul.
