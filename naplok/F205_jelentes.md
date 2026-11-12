# F205 — jelentés (IGESZAKASZ_ELOKESZITES)

*Végrehajtó: claude-opus-5-5 · ág: `claude/f205-igeszakasz-elokeszites` · 2026-11-12*

## 1. Felmérés (M0): a hat pont meglévő célhelye

Mérés: `origin/main` @ `d30c7787`, a táblák adatsorai a fejléc és a `#`-sorok nélkül
(`split('\t')`). A számok a mai állapotot írják le, nem becslések.

| Pont | Meglévő célhely az adatrétegben | Kulcs | Mai állapot | Mi hiányzik a tanulmány felől |
|---|---|---|---|---|
| 1. funkció | `elofordulasok.tsv` `funkcio` (SEMA 2.2) | `id` + `igehely` | 250 sorból 166-ban kitöltött | A tanulmány felől nincs út. A sor csak a `jeloltek.tsv` `elofordulas` jelöltjéből, döntéssel jön létre (3/2). |
| 2. negatív próba | `jeloltek.tsv` `indoklas` (SEMA 2.4: „csak a fölérendelt fogalmon keresztül tartozna ide”); a fölérendelt fogalom: `motivumok.tsv` | `id` + `igehely` + `jelolt_tipus` + `cel_id` | 812 jelölt-sor: 805 `elofordulas`, 7 `motivumkozi` | Nincs külön mező: a próba az `indoklas` prózájában áll. Ez elég, ha a blokk a próbát olvasói mondatban adja. |
| 3. jelentéspont | `bdb_vers_jelentes.tsv` (2.29, 162 053 sor), `thayer_vers_jelentes.tsv` (2.35, 64 431 sor), `bdb_jp_sefaria.tsv` (2.29.1), `JELENTESPONT_KEZI` | `strong` + vers | a szótár olvasata, gépi | **A mi olvasatunknak nincs helye.** A `JELENTESPONT_KEZI` csak a BDB félreolvasását javítja (brief K5). |
| 4. vita | `vitatott_forrasok.tsv` (2.58) + a motívumforrás „Vitatott pontok” prózája | `motivum` + `pont` | 3 sor | Motívumhoz és ponthoz kötött, nem igehelyhez. Versre vonatkozó vita-jelöltnek nincs helye. |
| 5. visszhang | `visszhang_tanuk.tsv` (2.57) és `visszhang_megfelelok.tsv` (2.53) | tanú: `motivum` + `igehely` + `hagyomany` + `tanu` + `forras`; megfelelő: `motivum` + `strong` + `igehely` + `forras` | 10 tanú-sor, 133 megfelelő-sor | Motívumhoz kötött. A tanulmányban talált tanúnak nincs jelölt-alakja; ma a kinyerő (`tanu_kinyer.py`) keresésből ír. |
| 6. versszámozás | `konkordancia/Karoli_versmegfeleltetes.tsv` (+ `_javitas`), a `pardes.db` `lxx_versszam` táblája (2.26), `f22/versosszevonas.tsv`, a TAHOT Károli-kulcsa | Károli-igehely | l. lent | Gépi. Kézi rögzítés csak az ÚSZ-ben kell. |

### 1.1 Versszámozás: mennyi derül ki gépileg

- **Károli ↔ KJV ↔ MT:** a `Karoli_versmegfeleltetes.tsv` 23 195 sora az ÓSZ-t és a Sirákot fedi.
  - 1 420 sorban a KJV-vers eltér a Károli-verstől.
  - 200 sorban az MT-vers ki van töltve, és eltér a Károli-verstől.
  - Osztályonként: `KJV` 21 005, `MT` 1 707, `KEZI` 483.
  - A javítótábla 373 sora felülírja a fő tábla sorait (F117).
- **Károli ↔ LXX:** a `pardes.db` `lxx_versszam` táblájában minden ÓSZ Károli-versnek van sora. Ahol nincs `LXX_OS`-sor, ott `forras=nincs` áll, kitöltés nélkül (2.26). A térkép nem forrás (DT-F92b).
- **Összevont versek:** az `f22/versosszevonas.tsv` 12 sora; a TAHOT mindkét versét a közös Károli-kulcson tartja (F85).
- **ÚSZ:** a Károli ↔ NA/TAGNT versbeosztásnak **nincs megfeleltető táblája**. Ott a blokk pontja kézi (`scope=manual`), vagy `üres`.

**Következmény:** az ÓSZ-ben a 6. pont gépileg kiolvasható, ezért a kinyerő az `ADAT-HIV` mintájára csak ellenőrzi (SEMA 3.10.7 4.). A tanulmányíró a blokkba a lekérdezés proveniencia-sorát másolja. Ha a blokk állítása eltér a lekérdezéstől, az a jelentésben ELTÉR-sor, nem jelölt. Jelölt-sor csak ott keletkezik, ahol a gép nem tud (ÚSZ), vagy ahol a tanulmány a táblát vitatja.

### 1.2 Amit a séma-javaslat nem kerülhet meg

1. **A `jeloltek.tsv` `id` mezője kötelező motívum-ID.** A jelentéspont, a vita és a versszámozás motívumtól független (K2), és a blokk fejlécében `motivum: új` is állhat. Az ilyen sorhoz nincs ID.
2. **A kulcs nem bírja a többszörös pontot.** A mai kulcs `id` + `igehely` + `jelolt_tipus` + `cel_id`.
   - Egy versben több Strong-nak lehet jelentéspontja.
   - Egy versnek több visszhang-tanúja lehet.
   - Egy versre több vita vonatkozhat.

   Ezeket a mai kulcs nem különbözteti meg. Tárgymező kell, vagy más kulcs.
3. **A `jeloltek.tsv`-t 70 eszköz olvassa** (`grep -l jeloltek.tsv eszkozok/**/*.py`). A beolvasás szótár-alapú (`sor.get(...)`), de az új oszlop hatását eszközönként meg kell nézni. A meglévő 812 sor bájtra változatlansága (brief M5) csak úgy tartható, ha a régi sorok a záró üres mezőt sem kapják meg.

### 1.3 Indítás és ütközések

- A felhasználó 2026-11-12-én előrehozta az indítást. A HAMART-001 kiadása (PR #696) ekkor még nyitott.
- A brief v2-je a #702-vel került a main-re. A #706 lezárta az F200 és az F206 fejlécét, és ideiglenesen kivette a `proza_allitas.py`-t az F205 `ir`-jéből.
- Az M0 1. lépése (az `ir` visszabővítése az öt fájllal és a két `proza_allitas` fájllal) a `feladatok.py ellenoriz`-ben függési kört ad: #74 ↔ #121 ↔ #123 ↔ #125 ↔ #156 ↔ #157 ↔ #178 ↔ #179 ↔ #190 ↔ #193 ↔ #205. A kört a #205 élei zárják:
  - #125 ↔ #205 a 2. sablonon (kétirányú, a mag);
  - #205 → #178 a 9. sablonon;
  - #156 → #205 az `ellenoriz.py`-n.

  Jelezve az orkesztrátornak (⛔).
- A #699 az `adat/SEMA.md`-t, az `eszkozok/ellenoriz.py`-t és az `adat/jeloltek.tsv`-t írja. Az orkesztrátor döntése: az M3–M5 a #699 merge-e után, behozott main-nel készül.

## 2. M1–M2 (2026-11-12)

- **M1** (F205.1): a `sablonok/2_PaRDeS_bovitett_sablon.md` 4/b. pontja (v23). A blokk-alak: `<!-- IGEHELY-BLOKK: [igehely] | motivum: [ID | új | —] | gerinc: [gerinc_elem | —] -->` … `<!-- IGEHELY-BLOKK-VÉGE -->`; a hat pont `- **[pont]:**` sorokban, mezőelválasztó ` · `, proveniencia szögletes zárójelben; `üres — [ok]`. A minta a HAMART-001 1Móz 8:21-es sorából, a repó adatával: `bdb_vers_jelentes.tsv` (H7043, `s.br.aa`, pont nélkül), `visszhang_tanuk.tsv` (Szent Ambrus), `Karoli_versmegfeleltetes.tsv` + `LXX_OS/genesis.tsv` (8:21 mindhárom számozásban). A vita pontja `üres`, mert a HAMART-001 „Az 1Móz 8:21 hatóköre” pontjának nincs nevesített képviselője (a `vitatott_forrasok.tsv` hiány-sora) — a minta így az `üres` szabályt is mutatja.
- **M2** (F205.2): a `MUNKAMENET.md` A-szakasza: A2b, A2c, A4b, A4c, A4d. A még nem létező eszköz `F8 — nincs eszköz` (a fájl szabálya); az A2c az M4-gyel létező parancsot kapott.

## 3. M4 — szakasz-fordítás (2026-11-12)

`eszkozok/szakasz_forditas.py` (+ `teszt_szakasz_forditas.py`, 15 teszt). Új fordítómotor nincs, a meglévő állapot-szabályokat importálja:
- BDB: `bdb_jelolt/szakasz_bemenet` (szakaszok, `strong_magyar_sorok`) és a `thayer_jelolt/szolista.allapot` lefedés-szabálya; a nem `elavult` `teljes` sor érvényes (a 13. szabály a lefedést csak a szakaszsorral bíró Strongon méri); a másodlagos Strong a `BDB_strong_alias.tsv` szerinti szócikk-Strongon.
- Thayer: `thayer_jelolt/szolista.allapot` (az M3 szólistájáé).
- TBESG rövid glossza: `glossza_lexikon_forditas.tovabbi_forras` (a 13. szabályé), `forras_hash`-összevetéssel.

**Ellenőrzés a mért alapvonalon.** Az F182.17 szerint a HAMART-001 Strongjai mind érvényes fordítással állnak. Az eszköz ugyanezt adja: az 1Móz 8:20-22 szakaszon 0 fordítandó (37 BDB-Strong kész, 1 a BDB-n kívül: H5668; 13 nyelvtani kihagyva); a G1944, G2671, G5356 a Thayer- és a TBESG-láncban kész.

**Próba egy meglévő szakaszon (G6): Gal 3:10-14** (5 vers, 49 Strong, 15 nyelvtani kihagyva). Fordítandó: Thayer 18 Strong (8 `hianyos`, 10 `hianyzik`; 111 hiányzó szakasz, 51 141 forráskarakter), TBESG 28 rövid glossza (225 karakter), BDB 0. A láncok saját száraz futása a kiadott bemeneten, repón kívüli munkamappával, hálózat nélkül:
- `thayer_api_koteg.py szaraz --adag 9205 --strongok …`: 18 Strong, 25 kérés, forrás 140 546 karakter (a lánc a Strong **összes** szakaszát küldi, nem csak a hiányzókat), becslés 3,77 USD Batch-áron (első kör 2,28 + javító kör 1,48; `manual`);
- `glossza_api_koteg.py szaraz --lista …`: 28 egység, 2 kérés, 0,056 USD (`manual`, mérés nélkül).

Fordítás és API-hívás nem futott; a repóban fájl nem keletkezett (teszt: `test_repo_erintetlen`).

**Rés, nyitott tétel:** a `bdb_api_koteg.py`-nak nincs Strong-listás bemenete (az adagot a sorrend-fájl adja), ezért a BDB-listát kézzel kell az adagba venni. A TBESH héber glossza (`glosszak_heber_hu.tsv`) nem része a három láncnak, és a brief sem kérte.
