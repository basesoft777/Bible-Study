---
feladat: 117
cim: A Károli↔KJV versmegfeleltetés táblahibáinak javítása (VERSMEGF_JAVITAS)
kod: VERSMEGF_JAVITAS
tipus: feladat
fazis: folyamat
munka: adat
modell: opus
allapot: megallt
ag: claude/f117-versmegf-javitas
ad: a `Karoli_versmegfeleltetes.tsv` a #114 által mért táblahibák nélkül generálódik (13 fejezet pótolva, a KEZI-, Dán 3- és eltolt párok szöveg-összevetéssel javítva); a `tsk_kulcs.NINCS_PAR_KIVETEL` üres, a Jón 2:3 (ALVIL-001) és Jón 2:6 (TEREMT-001) TSK-sorai visszatérnek
kovetkezo: Te: jóváhagyás az F117.3-hoz (javító bemenet + modul + KK4)
olvas: [konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_1908.tsv, konkordancia/KJV_Strongs_teljes.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TSK_kereszthivatkozasok.tsv, naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv, naplok/KAROLI_KK1b_kulcstabla_general.py, eszkozok/f91_versmegf_javit.py, eszkozok/lxx_os_import.py, eszkozok/tsk_versszam_felmeres.py, naplok/TSK_VERSSZAM_zaras.md, naplok/TSK_VERSSZAM_jelentes.md, naplok/F114_elveszett_sorok.tsv, naplok/ELLENOR_TSK_VERSSZAM.md, naplok/LXX_OS_LEFEDETTSEG_M0.md, adat/elofordulasok.tsv, adat/SEMA.md, adat/datasetek.tsv, Rendszerfejlesztesi_playbook.md]
ir: [naplok/KAROLI_KK4_tabla_veglegesit.py, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_versmegfeleltetes_javitas.tsv, eszkozok/versmegf_javitas.py, eszkozok/teszt_versmegf_javitas.py, eszkozok/versmegf_szoveg_osszevet.py, eszkozok/tsk_kulcs.py, eszkozok/teszt_tsk_kulcs.py, eszkozok/tsk_versszam_felmeres.py]
fugg: []
nem_fugg: [107, 109]
---
# F117_VERSMEGF_JAVITAS_BRIEF.md — A Károli↔KJV versmegfeleltetés táblahibáinak javítása

*FELADATOK #117 · Modell: opus (a versenkénti magyar–angol szöveg-összevetés ítéletet igényel; felhasználói döntés, 2026-10-18) · v1.1 · 2026.10.18 · előzmény: N-F54a (F54, bővítve a #114-ben), DT200 (a #114 TSK_VERSSZAM, PR #398), `naplok/TSK_VERSSZAM_zaras.md`*

## 1. Cél

A `konkordancia/Karoli_versmegfeleltetes.tsv` a projekt Károli↔KJV(↔MT) verskulcs-táblája. Generált fájl (`# GENERÁLT: naplok/KAROLI_KK4_tabla_veglegesit.py`), ezért **kézzel szerkeszteni tilos**: a javítás a generátorban vagy annak kézi bemenetében történik, a TSV újragenerálódik.

A #114 (TSK_VERSSZAM) a TSK-t erre a táblára kulcsolta (`eszkozok/tsk_kulcs.py`), és négy ellenőrzési kör után kimutatta, hogy a hibák gyökere maga a tábla. A felhasználó döntése (DT200 (b), 2026-10-18): az átváltó a hibás helyeken „nincs pár”-t ad, kivétellistával; a tábla pótlása az N-F54a bővítéseként külön tétel. **Ez az a tétel.**

A #114 mérése szerint javítandó (`NYITOTT_FELADATOK.md` N-F54a, „BŐVÍTÉS” és „BŐVÍTÉS 2”; tételesen `naplok/F114_elveszett_sorok.tsv`):

| Osztály | Helyek | Kár a TSK-n (#114 mérése) |
|---|---|---|
| **A — hiányzó fejezet** (`nincs_sor`, a táblában a Károli-fejezetnek nincs sora) | 13 fejezet: 2Móz 35, 2Móz 36, Dán 3, Hós 2, Hós 13, Hós 14, Jób 17, Jób 37, Péld 12, Én 5, Én 6, Ézs 4, Ézs 64 | 235 forráskulcs / 3 653 forrássor; 243 célvers / 2 360 előfordulás |
| **B — üres KJV-pár, holott létezik** (`KEZI|kezi_identitas_javitas`, 8 sor) | Károli Préd 9:21–23 = KJV 10:1–3; Károli Jób 39:34–38 = KJV 40:1–5 | a `tablahiba_kjv_par_letezik` osztály része (25 tétel) |
| **C — Dán 3:31–33** (a Károli-sorok hiányoznak) | Károli Dán 3:31–33 = KJV Dán 4:1–3 | uo. |
| **D — eltolt azonosság** (MT-tartalék vagy `tvtms` adna eltolt párt; ma `NINCS_PAR_KIVETEL`) | 1Kir 22:46–49 (= KJV 22:45–48) és 22:54; Ézs 3:1–27 (Károli 3:1 = KJV 2:22); Jón 2:1–11 (Károli 2:1 = KJV 1:17, 2:9 = KJV 2:8; N-F41a); 1Sám 24:1–23 (Károli 24:2 = KJV 24:1); 1Sám 20:43 | `kivetel_nincs_par_*` 119 tétel |
| **D′ — `tvtms` szomszédok** (azonosság eltolt tartalomra) | 1Kir 22:43–45 és 22:50–53 (az 1Kir 22:45 Károli-szövege = KJV 22:44) | a #114 nem mérte külön |

A Károli-oldali fejezetméret a pótlásnál nem tételezhető fel azonosnak a KJV-vel: Károli Hós 13 = 15, Hós 14 = 10, Én 6 = 10 vers; KJV 16, 9, illetve 13 vers (DT200 indoklása). A számegyezés ezért **nem** pótlási szabály.

A cél:

1. **versenkénti szöveg-összevetés** a `Karoli_1908.tsv` és a `KJV_Strongs_teljes.tsv` között az érintett fejezetekben, a táblától függetlenül;
2. a generátor (vagy kézi bemenete) javítása úgy, hogy a táblában az A–D′ osztály minden Károli-verse a szövegileg igazolt KJV-párt (vagy indokolt „nincs pár”-t) kapja;
3. a `tsk_kulcs.NINCS_PAR_KIVETEL` kiürítése (a kivétel oka megszűnik);
4. az ALVIL-001 `Jón 2:3` és a TEREMT-001 `Jón 2:6` (`adat/elofordulasok.tsv`) TSK-sorainak visszatérése, a TEREMT-001 `Zsolt 42:8 → Jón 2:4` céllal együtt;
5. **nem körkörös** mérés: hány TSK-forrássort ér el egy Károli-kulcs a javítás előtt és után.

## 2. A tábla előállítási lánca (a #114 után, main `49dd711e`)

| Lépés | Fájl | Megjegyzés |
|---|---|---|
| 1 | `naplok/KAROLI_KK1b_kulcstabla_general.py` → `naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv` | a bemenete a repón kívüli `lxx-morph` `verse_pairs.jsonl` (`/tmp/lxxmorph_test/…`, sha256 a KK4 fejlécében) és a `lxx_os_import.KEZI_ELTOLASOK`; **ma nem futtatható újra a repóból** |
| 2 | `naplok/KAROLI_KK4_tabla_veglegesit.py` | a tervezetből (a repóban verziózott) választja ki soronként a végleges sort |
| 3 | `eszkozok/f91_versmegf_javit.py` (a KK4 importálja) | a zsoltárfeliratok `igehely_kjv`-javítása, egy helyen élő szabály (DT-F91a/c) |

A javítás tehát a 2–3. lépés mintáját követi: **verziózott kézi bemenet + egy helyen élő alkalmazó modul, a KK4 importálja**. A pontos helyét a ⛔ 4.1 dönti el.

## 3. Hatókör

**Benne van:**
- `eszkozok/versmegf_szoveg_osszevet.py`: versenkénti összevetés Károli 1908 ↔ KJV az érintett fejezetekben (A–D′), a `Karoli_versmegfeleltetes.tsv` olvasása nélkül. Jelek legalább: tulajdonnevek és számnevek egyezése; versenkénti hosszarány; a vers első és utolsó tartalmi eleme. Kiegészítő jelként a `TAHOT_kivonat.tsv` (Károli-kulcs, F85) Strong-halmaza és a `KJV_Strongs_teljes.tsv` Strong-halmaza közti Jaccard. **Figyelem:** a TAHOT F85-ös átkulcsolása a táblát egyik tanúként használta (`eszkozok/tahot_verskulcs_finomit.py`), ezért a TAHOT-jel önmagában nem független; elfogadott párhoz kell a szöveg-összevetés jele is. A kimenet: `naplok/F117_szoveg_osszevetes.tsv` (Károli-vers, javasolt KJV-vers(ek), jelek, döntési ok, proveniencia);
- a javító bemenet (javaslat: `konkordancia/Karoli_versmegfeleltetes_javitas.tsv`, soronként `igehely_karoli`, `igehely_kjv`, `igehely_mt`, `osztaly`, `forras`, `megjegyzes`, `proveniencia`) és alkalmazó modulja (javaslat: `eszkozok/versmegf_javitas.py`, egységteszttel), a KK4-be importálva, az F91-javítás mintájára; a ⛔ 4.1 szerint;
- a `Karoli_versmegfeleltetes.tsv` újragenerálása a KK4-gyel; a fejléc proveniencia-sora a javítást is megnevezi;
- `eszkozok/tsk_kulcs.py`: a `NINCS_PAR_KIVETEL` kiürítése, a docstring „ISMERT KORLÁTOK” részének frissítése; `eszkozok/teszt_tsk_kulcs.py`: a kivétel-tesztek (`test_1kir_22_kivetel_nincs_par`, `test_kivetel_fejezetek_nincs_par`) átírása pozitív párokra (pl. Jón 2:3 → KJV 2:2, 1Sám 24:2 → KJV 24:1, Préd 9:21 → KJV 10:1, Hós 14:2 → a szövegileg igazolt KJV-vers);
- a felmérőszkript (`eszkozok/tsk_versszam_felmeres.py`) kiegészítése a nem körkörös méréssel (5.).

**Nincs benne:**
- a `Karoli_versmegfeleltetes.tsv` kézi szerkesztése (generált fájl);
- a KK1b-lépés újrafuttatása vagy a `verse_pairs.jsonl` újraletöltése (repón kívüli forrás); ha a javítás mégis ezt kívánná: ⛔ megállás;
- a Károli-összevonás szabálya (Préd 2:26 = KJV 2:25–26, Zsolt 13:6 = KJV 13:5–6; „csak az első KJV-vers a pár”, F91): változatlan, a jelentés tételesen említi;
- az ÚSZ-versmegfeleltetés (N-F114a) és a tartomány-igehelyek TSK-keresése (N-F114b);
- a táblát olvasó **további fogyasztók** kimenetének újragenerálása (pl. `lxx_os_import`, `sqlite_epit` → `pardes.db` (#101), F17-Macula, BSB, `karoli_strong`); a hatásukat a 4.6 méri és listázza, az újragenerálás külön tétel;
- az N-F54a LXX-oldala (`lxx-hid`, `karoli_ok = szamozas_elteres` a Péld 12, Jób 17, 2Móz 36-on): a tábla pótlása ennek előfeltétele, de az `LXX_OS` újraimportja nem része ennek a feladatnak;
- az éles `lexikon/` újragenerálása (a #36/#10 dolga); a próbagenerálás a repón kívülre megy (`--kimenet`).

## 4. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév kiírása és összevetése a fejléc `modell` mezőjével; eltérésnél megállás. Előtte a meglévő ág/worktree keresése a feladathoz. Az #11 M2 párhuzamosan futhat: a `general.py`-hoz, a `motivumok/`-hoz és a `sablonok/9_*`-hoz ez a feladat nem nyúl.
1. ⛔ **A javítás helye.** Lehetőségek: **(a)** új, verziózott kézi bemenet (`konkordancia/Karoli_versmegfeleltetes_javitas.tsv`) + alkalmazó modul (`eszkozok/versmegf_javitas.py`), a KK4 az F91 után importálja; a javítás sorai felülírják vagy pótolják a tervezet sorait, `forras=szoveg_osszevetes_f117` értékkel; **(b)** a javító sorok közvetlenül a `naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv`-be (ez generált tervezet, ezért nem javasolt); **(c)** más. Szempont: egy szabály egy helyen éljen (F91-minta), és a tábla minden sora visszavezethető legyen a forrására. Tétel a `DONTESEK.md`-be (`DT-F117a`), megállás.
2. **F117.1 — szöveg-összevetés, kis minta** (`Rendszerfejlesztesi_playbook.md` 3. pont): az összevető szkript a 13 hiányzó fejezetből háromra (javaslat: Hós 14, Én 6, Dán 3) és a D-osztály egy fejezetére (Jón 2). ⛔ **A minta bemutatása** (versenként: Károli-szöveg eleje, javasolt KJV-vers, jelek), megállás a felhasználó jóváhagyásáig. A jelek küszöbe és a „nincs pár” szabálya itt dől el (`DT-F117b`).
3. **F117.2 — teljes összevetés** az A–D′ osztály minden versére. Bizonytalan párnál (a jelek ellentmondanak, vagy két KJV-vers egyformán illik) **nem** dönt automatikusan: `bizonytalan` jelölés, tételes lista (playbook 4. pont). Ha bizonytalan sor van: ⛔ megállás, tételes listával.
4. **F117.3 — a javító bemenet és a modul** a DT-F117a szerint, egységteszttel (legalább: egy pótolt fejezet, egy KEZI-pár, a Dán 3:31, egy D-osztályú eltolás, egy D′-szomszéd, egy változatlan sor). A KK4 újrafuttatása → `Karoli_versmegfeleltetes.tsv`. Írás előtti sor-összevetés az eredetivel (`eszkozok/igazolas_migracio.py` minta): a változott, hozzáadott és törölt sorok száma osztályonként a jelentésbe; az A–D′ halmazon kívül **egyetlen sor sem változhat** — ha mégis, megállás.
5. **F117.4 — `tsk_kulcs` kivezetés**: a `NINCS_PAR_KIVETEL` kiürítése, a tesztek átírása, a docstring frissítése; a `teszt_tsk_kulcs.py` zöld.
6. **F117.5 — mérés** (5. szakasz) és a fogyasztói hatás: a táblát olvasó eszközök listája (`grep Karoli_versmegfeleltetes eszkozok/`), és mindegyikre: olvas-e A–D′ osztályú verset. Ahol az újrafuttatás egy `adat/*.tsv`-t vagy `konkordancia/*.tsv`-t változtatna, azt **nem** futtatja, csak N-tételbe (`N-F117a`, …) írja.
7. **F117.6 — próbagenerálás** a repón kívülre (`--kimenet`): ALVIL-001 és TEREMT-001; összevetés a #114 utáni állapottal (`naplok/TSK_VERSSZAM_jelentes.md`).
8. Független ellenőrzés (`fuggetlen-ellenor`), zárójelentés: `naplok/VERSMEGF_JAVITAS_zaras.md`. Lezáráskor az N-F54a TSK-oldali része (BŐVÍTÉS, BŐVÍTÉS 2, KORLÁT) lezártnak jelölve, és az N-F41a, ha a Jón 2:1 rendeződött; az N-F54a LXX-oldali része nyitva marad, hivatkozással. Push és PR csak a felhasználó kérésére.

## 5. Kötelező mérés — nem körkörösen

A #114 mérése a kivétel-verseken körkörös volt: az átváltó és a „helyes” halmaz ugyanabból a táblából jött (`naplok/TSK_VERSSZAM_zaras.md` 2. pont). Ezért itt a **referencia a szöveg-összevetés** (`naplok/F117_szoveg_osszevetes.tsv`), nem a tábla.

- **M1 — Károli-kulcsonként elért TSK-forrássor, előtte és utána.** Az A–D′ osztály minden Károli-versére: (i) a main tábláján és `tsk_kulcs`-án (#114 utáni állapot) elért TSK-forrássorok száma; (ii) a javított táblán és üres kivétellistán elért szám; (iii) a referenciából várt szám (a szöveg-összevetés KJV-versének TSK-sorai, a táblától függetlenül számolva). Elvárás: (ii) = (iii) minden versen; az eltérés tételesen. Összesítés osztályonként és mindösszesen.
- **M2 — célkulcs-oldal:** ugyanez a TSK `Kapcsolódó igehely` oldalán (hány TSK-célelőfordulás kerül a referencia szerinti Károli-versre).
- **M3 — mellékhatás a teljes ÓSZ-en:** a javítás előtti és utáni `tsk_kulcs` összevetése minden ÓSZ Károli-kulcson; az A–D′ halmazon kívül 0 eltérés.
- **M4 — a #114 felmérője:** a `tsk_versszam_felmeres.py` B-része a javított táblán; a kivétel-versek most nem körkörösek, mert nincs kivétel, és a referencia a szöveg-összevetés.
- **M5 — `elofordulasok.tsv`:** az érintett sorok (legalább ALVIL-001 `Jón 2:3`, TEREMT-001 `Jón 2:6`, és minden A–D′ osztályú `igehely`) TSK-sorainak száma előtte/utána.

Minden mérés proveniencia-sorral (`scope=… | forras=… | n=… | ts=…`); kézi szövegolvasásnál `scope=manual`.

## 6. Elfogadási feltételek

| # | Feltétel |
|---|---|
| E1 | A `Karoli_versmegfeleltetes.tsv` a KK4-ből generálódik, `# GENERÁLT` fejléccel; kézi szerkesztés nincs (a git-diff csak a generátor és bemenete változását tükrözi; a KK4 kétszeri futtatása bájtra azonos). |
| E2 | A 13 fejezet minden Károli-versének van sora a táblában; a B-osztály 8 sora és a Dán 3:31–33 a szövegileg igazolt KJV-párt kapja. |
| E3 | A D–D′ osztály sorai a szöveg-összevetés szerinti párt adják; a `tsk_kulcs.NINCS_PAR_KIVETEL` üres; a `teszt_tsk_kulcs.py` és a `teszt_versmegf_javitas.py` zöld. |
| E4 | M1: a (ii) = (iii) minden A–D′ versen, vagy az eltérés tételes és indokolt; M3: az A–D′ halmazon kívül 0 eltérés. |
| E5 | Az ALVIL-001 `Jón 2:3` és a TEREMT-001 `Jón 2:6` a próbalexikonban TSK-sorokat kap (a KJV 2:2, ill. 2:5 sorait), és a TEREMT-001 `Zsolt 42:8` TSK-célja `Jón 2:4`-en áll. |
| E6 | A táblát olvasó fogyasztók hatása listázva; `adat/*.tsv` és a többi `konkordancia/*.tsv` bájtra változatlan (hash a jelentésben). |
| E7 | A licenc és forrás a jelentésben: Károli 1908 és KJV (eBible) Public Domain; a `verse_pairs.jsonl` (lxx-morph, CC BY 4.0) változatlan forrásként marad megnevezve (`Rendszerfejlesztesi_playbook.md` 2. pont, `adat/datasetek.tsv`). |

## 7. Döntésnapló

- **DT-F117a:** a javítás helye (4.1 ⛔).
- **DT-F117b:** a szöveg-összevetés küszöbe és a „nincs pár” szabálya a minta alapján (4.2 ⛔).
- **N-F117a, …:** a táblát olvasó fogyasztók szükséges újragenerálása (4.6), ha van.
- Kapcsolódó: **N-F54a** (TSK-oldali része ezzel zárul), **N-F41a** (Jón 2:1), **DT200** (a kivétellista ezzel kivezetődik), **N-F114a**, **N-F114b** (nem érinti).
