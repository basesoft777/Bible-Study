# F123.BDBILL — a szakaszos BDB-fordítás 1:1-es illesztése: mérés (DT-F123y)

proveniencia: scope=bdb_szakasz_hu.tsv (T0 HEAD 8578a109, T1 régi logika, T2 új logika) | forras=naplok/F123_BDBILL_meres.py + eszkozok/bdb_jelolt/hu_illeszt.py@418b92f8d0ae | ts=2026-11-03

Modell: `claude-opus-5-5`. Futtatás: `python naplok/F123_BDBILL_meres.py` (fájlt nem ír).

## 1. Az ok

A `hu_illeszt.forditasok()` a szakaszonként fordított Strong `sz<n>` sorait a közös összefűzővel
(`szakasz_bemenet.strong_magyar_sorok`) **egy szöveggé fűzte**, és a `strong_illeszt` ezt a jelölőkkel és horgonyokkal
**újraszabdalta**. A sorhatár, amely a fordításban már megvolt, így elveszett. Ahol a magyar jelölősorozat nem egyezett
a forráséval (például a H2416 BDB2718: `1 / a / b / c / 2 / 3 / 4`, miközben a szócikkben előbb a BDB2716 is `1 / 2 / 3`-at hoz),
a kurzor más szakasz jelölőjére ugrott: idegen szöveg, `elakad`, töredék („17:14;”).

Másodlagos lelet: a commitolt tábla (T0) **elavult**. 2026-10-18-án, a szakaszos fordítás előtt készült, és utána
csak részlegesen frissült, ezért a 8 090 szakaszolt Strongból csak 674-et fed le.

## 2. A javítás

Ha a Strong szakaszonként fordított, a `szakasz_egyezes` ellenőrzi a megfeleltetést:

- a felhasznált `sz<n>` sorszámok halmaza pontosan a Strong szakaszainak sorszáma (ismétlés nélkül);
- minden `sz<n>` `forras_hash`-e megegyezik a szakasz javított szövegének SHA-1-ével (`szakasz_bemenet.szakaszok`), és
  ez a hash a `jel`-et is fedi, tehát ugyanazt a jelölőt és szöveget.

Igazolt esetben a sor szövege a saját `sz<n>` sora, `kategoria` = `szakasz`, `horgony` = `sz<n>`, a proveniencia pedig
`(fejléc; sz<n> 1:1)`. Ha nem igazolt, a horgonyos illesztés marad, és a proveniencia megnevezi az okot
(`1:1 nem igazolt: …`). A `teljes` úton fordított Strong (585) változatlan.

## 3. Számok

| | Strong | sor | `szakasz` | `illeszkedik` | `horgonnyal` | `elakad` | `jelolo_nelkul` |
|---|---|---|---|---|---|---|---|
| T0 (HEAD) | 674 | 9 664 | — | 6 395 | 202 | 606 | 2 461 |
| T1 (mai bemenet, régi logika) | 8 090 | 36 621 | — | 14 291 | 583 | 659 | 21 088 |
| T2 (mai bemenet, új logika) | 8 090 | 36 621 | 29 311 | 5 211 | 111 | **0** | 1 988 |

- Szakaszos Strong: **7 514, mind igazolt 1:1** (29 311 sor); nem igazolt **0**.
- A 8 099 lefordított Strongból 9 nincs a szakasztáblában (H0747, H1753, H3367, H3848, H4123, H4725, H6433, H7560, H8065; korábban is így volt).
- **A logika hatása (T1→T2):** 21 625 sor szövege változik, 7 514 Strongban. Ebből 18 270 a cím/fej: a cím saját `sz1`-et kap,
  és a fej már nem hordozza a címet. A többi **3 355 sor 1 066 Strongban**.
- **A teljes hatás (T0→T2):** 26 957 új sor (7 416 Strong), és 2 265 meglévő sor szövege változik (98 Strong).

A szakaszos Strongok sorai a saját `sz<n>` szövegükhöz mérve (T2 = a saját szöveg):

| | azonos | részleges¹ | **idegen**² | üres, bár volt saját fordítás |
|---|---|---|---|---|
| T1 (régi logika) | 7 686 | 8 843 | **537 sor, 266 Strong** | 12 245 (ebből 659 `elakad`) |
| T0 (HEAD-tábla) | 89 | 1 142 | **142 sor, 59 Strong** | 981 (ebből 606 `elakad`) |

¹ A szöveg a saját szakasszal kezdődik, de hosszabb vagy rövidebb. A régi logikában ez jellemzően a `jelolo_nelkul` szomszéd szövegét is hordozó sor, vagy (T0-ban) a `teljes` fordítás más megfogalmazása.
² A szöveg eleje egy másik szakasz `sz<n>`-éé, a sajátban nincs meg. A legtöbb T1-ben: H1980 16, H0995 11, H2416 10, H3772 10, H7971 10, H4672 8, H3068 7, H5080 7, H5307 7, H0539 6.

Kategória-átmenet T1 → T2 (a szakaszos Strongok sorai): `jelolo_nelkul` 19 100, `illeszkedik` 9 080, `horgonnyal` 472, `elakad` 659 → mind `szakasz`.

## 4. Szúrópróba (T1 → T2, cím/fej nélkül; véletlen mag 123 + H2416)

| Strong | sor | előtte → utána | lelet |
|---|---|---|---|
| H2416 | 13 | `illeszkedik` „1 élet: testi 1Móz 27:46 …” (BDB2720) → „1 állat, mint élő, tevékeny lény:” | idegen → saját |
| H2416 | 14 | `elakad` (üres) → „a. általában, 1Móz 8:17 …” | üres → saját |
| H2416 | 15 | `horgonnyal` „17:14;” → „b. vadállatok, életerejük és tevékenységük miatt …” | töredék → saját |
| H2416 | 16–18 | idegen (BDB2720 2., 3.) → „c. élőlények …”, „2 élet, csak késői költészetben …”, „3 étvágy …” | idegen → saját |
| H2416 | 19 | `elakad` (üres) → „4 újjáéledés, megújulás …” | üres → saját |
| H1419 | 3–4 | „1. 1; הַגָּדוֺל הַכֹּהֵן a főpap …” (a 2. pont szövege) / `elakad` → „1 méretben és kiterjedésben …” / „2 számban …” | idegen és üres → saját |
| H1092 | 3–4 | a 3. sor a 4. szövegét is hordozta → a 4. saját szöveget kap („בְּלוֺא l. lent בלה.”) | szomszéd leválik |
| H6536 | 7 | a következő alszócikk feje („[מְּרַס] ige …”) is a sorban → csak a saját szöveg | szomszéd leválik |
| H6991 | 5 | a Pe`îl-szakasz is a Pe`al-sorban → csak a saját szöveg | szomszéd leválik |
| H2048, H2339, H4869, H4899 | — | a jelölős sor azonos, a `jelolo_nelkul` sor saját szöveget kap | szomszéd leválik |

A vizsgált sorok mindegyikében az új szöveg a sor saját angol szakaszának fordítása; ezt a hash-egyezés is igazolja. A H4899 7.
sora („3; így Ew l. Leng Schü Co Behrm], vagy Józsua főpapra [mint”) a forrásban is töredék (`jelolo_nelkul`), és az 1:1 ezt hűen viszi.

## 5. Lapok (`lexikon/`, mind a 9)

`python eszkozok/general.py --cel lexikon --id <ID> --ir` a 9 lapra, kétszer: a régi táblával (alapvonal) és az újjal.

| Lap | a tábla hatása (alapvonal → új) | BDB-blokk a lapon | megjegyzés |
|---|---|---|---|
| ALVIL-001 *(kiadott)* | 0 sor | H7585 | `teljes` (kézi) úton, változatlan |
| ISTENTISZT-001 *(kiadott)* | 0 sor | H7121, H8034 | `teljes` (kézi) úton, változatlan |
| TEREMT-002 | 0 sor | H0922, H8414 | `teljes` úton, változatlan |
| ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 | 0 sor | nincs bekötött BDB-blokk a main-en | — |

**A main-en a javítás egyik lapon sem változtat**, kiadott lapon sem. A HEAD-lapok és az alapvonal közti eltérés
(ANTROP 1 255, HAMART 3 196, KIRALY 1 172, MENNY 1 608, TEREMT-001 947, HODIT 767, TEREMT-002 2 sor) a lapok korábbi
elavultságából jön, és nem e tételé. Ezért a lapokat ez az ág nem írja: az ANTROP-001-et a #608, a HAMART-001-et a #609 hozza.

**Hatás a #608 után (ANTROP-001):** a #608 bekötése a lapon a H2416 és a H5315 BDB-blokkját mutatja. A #608 táblájához képest:

- H2416: a 13–19. sort a #608 már a saját szövegével hozza (egyezik a T2-vel). Javul a 9., 10., 24., 25. és 28. sor (idegen szöveg →
  saját; például a 9. sorban „2 élet, csak késői költészetben” → „2 (kétséges) élénk, tevékeny”, a 24.-ben „1 Istenről: status
  absolutus …” → „1 élet: testi …”), a 26. és a 28. sor üresből saját szöveget kap, és az alszócikkek feje (11., 12., 20.–23., 27., 30.)
  is saját szöveget kap.
- H5315: 42 / 43 sor más szöveget kap. A #608 táblájában a `teljes` fordításból illesztett szöveg áll, ezt most a szakaszos (`sz<n>`)
  fordítás váltja; a 3. és a 22. sor `elakad`-ból saját szöveget kap.

A #608 merge-e után az ágat a main-re kell hozni, a táblát újra kell generálni, és az ANTROP-001-et is újra kell generálni.

## 6. Kapuk

- `ellenoriz.py`: RENDBEN 18 · **SÉRTÉS 0** · KÉZI 2 · JELENTÉS 8.
- `feladatok.py ellenoriz`: 181 brief, 0 hiba.
- `olvasoi_kapu.py --osszes`: a lapok bájtra azonosak a main-nel, ezért az eredmény is azonos (a meglévő BUKÁS-ok nem e tételéi).
- `hu_illeszt.py --ellenoriz`: azonos.
- Tesztek: `teszt_hu_illeszt.py` 15 OK; `teszt_forditas_kapuk.py` 126 OK (a `SzakaszKeszMagyar` 8 090 Strongon RENDBEN);
  `teszt_bont.py` HuIlleszt 13 OK. Két hiba a HEAD-en is fennáll, nem e tételéi: a `teszt_bont.py`
  `Determinizmus.test_ellenoriz` (`bont.py --ellenoriz`: a `bdb_szakaszok.tsv` ELTÉR), és a `teszt_szakasz_bemenet.py`
  `test_kezi_regi_sor_dt_f128f`. Mindkettő ellenőrizve egy tiszta HEAD-worktree-ben.

## 7. A párhuzamos részmérés ellenőrzése (orkesztrátori bemenet, 2026-11-03)

proveniencia: scope=bdb_szakasz_hu.tsv T0 (HEAD 8578a109) ↔ T2 | forras=saját szkript (eseti, a scratchpadben) + `naplok/F123_BDBILL_lap_hatas.py` | ts=2026-11-03

| állítás (a leállított session részmérése) | saját mérés |
|---|---|
| a T0-ban 674 Strong; ebből 98 szakaszos forrású, mind elavult | 674; szakaszos 98, kategóriában vagy szövegben eltér 98 ✔ |
| 7 `teljes` forrású csak kategóriában tér el (H1115, H2403, H3427, H3581, H3782, H3956, H9009) | ✔, mind egy-egy sor `illeszkedik` → `horgonnyal` (a horgony-kód 10-18 utáni változása); szövegben eltérő `teljes` Strong 0 |
| 7 416 további szakaszos Strongnak van fordítása, de sora nincs; a `--strong` ezt nem pótolja | ✔ 7 416, mind szakaszos; a `reszleges_szoveg` valóban csak meglévő sorkulcsot cserél, ezért teljes generálás kellett (F123.BDBILL.2) |
| H1875 6. sor: „2 kikeresik 1Krón 26:31.” az sz6 „2 keres, megkérdez, tanácsot kér:” helyett | ✔; T2: `szakasz`, „2 keres, megkérdez, tanácsot kér:” |
| H8415 5. sor: „2. 5.” | ✔ (T0: a 2. sor „2. 5.”); T2: a 2. sor „2 (mély) tenger …”, az 5. „2. 5. örvény (si vera lectio) …” (a forrássor jele maga „2. 5.”) |
| felső becslés: az ISTENTISZT-001 (H3068, H3605, H3947, H4672, H6213, H7122), ALVIL-001 és TEREMT-001 (H8415), MENNY-001 (H3947) érintett | **mért: a lapok bájtra azonosak** (5. pont). Ezek a Strongok a main-en nem állnak BDB-gerincblokkban: a lapon BDB-blokkot csak a H7585, H7121, H8034, H0922 és H8414 kap, mind `teljes` úton, változatlanul. A kiadott lapok miatti megállás ezért nem következett be. |

## 8. Mit mutat most (main, régi tábla) egy táblából hiányzó vagy elavult Strong

- **Lap** (`lexikon_general.bdb_gerinc_szakaszok`, `naplok/F123_BDBILL_lap_hatas.py`): a hiányzó Strong minden szakasza magyar szöveg nélkül marad, és a lapon az angol szöveg + „*(fordításra vár)*” jelenik meg. Az elavult Strong szakaszai idegen szöveget vagy töredéket mutatnak.
  - H0509 (hiányzó): 2 útvonalból magyar szöveg nélkül régi 2 → új 0.
  - H1875 (elavult): 18 útvonalból régi 11 → új 0. Ezen felül a `Qal/1/-`, `Qal/2/-`, `Qal/3/-` és a `Niph'al/…` a szomszéd szakasz szövegét hordozta (például a `Qal/2/-` alatt „2 kikeresik 1Krón 26:31.”, ami a Niph'al 2.).
  - H8415 (elavult): 6-ból régi 1 → új 0; a `-/2/-` alatt „2. 5.”, a `-/3/-` és a `-/5/-` alatt töredék.
- **Szónézet** (olvasó szerver, `lekerdezesek.bdb_magyar`): **nem érintett.** A `forditasok.tsv`-ből a közös összefűzővel a teljes magyar szócikket adja, a `bdb_szakasz_hu.tsv`-t nem olvassa. A `pardes.db` manifestje (`manifest_pardes_db.tsv`: `bdb_szakasz_hu 9664`) a következő adatbázis-építéskor frissül (36 621).

## 9. Kapu (DT-F123z)

`ellenoriz.py` 26. szabály (`hu_illeszt.kapu_elteresek`): a commitolt tábla törzse egyezik-e a mai generálással; a fejléc és a `proveniencia` `ts=` része nem számít. Fokozat: **SÉRTÉS (gátló)**; a DT-F123z 🟢, az orkesztrátor döntése a felhasználó felhatalmazásával (2026-11-03), az indok ott áll.

- A javított táblán: RENDBEN (~4 mp).
- A régi (HEAD) táblán: SÉRTÉS 7 521 = 7 416 hiányzó + 105 eltérő (98 szakaszos + 7 kategória). Pontosan a fenti osztályok.
- Tesztek (`teszt_hu_illeszt.py` `Kapu`, ideiglenes adatmásolaton): a naprakész és a más `ts`-ű tábla egyezik; a törölt Strong hiányként, a megváltozott `sz13` elavult sorként bukik; egy Thayer-sor hozzáadása nem bukik.

## 10. Ami nem e PR-é

- **A `lexikon_general.py` BDB-gerince csak útvonal szerint azonosít** (a #608-ban N-F123m). A javítás nem kicsi: az útvonal a kulcs a `szotar_szakasz_cimke.tsv`-ben (`szotar` + `strong` + `szakasz`), a `lexikon_hivatkozasok` → útvonal leképezésben (`gerinc_utvonal_vag`), a kiemelésben (`celok`, `hordozo`), és a 17./18. szabályban is. A `bdb_id` + útvonal kulcs ezért séma- és kapuváltozás, így külön tétel marad; a táblajavítás megy előre. A H2416 lapblokkja ettől még összevonhat azonos útvonalú szakaszokat (például a `-/1/-` a BDB2716-ból, a BDB2718-ból és a BDB2720-ból).
- A H7585 „®” átírás-hibája és a TEREMT-002 üres-sor eltérése (orkesztrátor: külön tétel).
