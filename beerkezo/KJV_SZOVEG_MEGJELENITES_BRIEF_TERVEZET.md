---
feladat:
cim: A teljes KJV-szöveg párhuzamos megjelenítése a Károli mellett az olvasóban (KJV_MEGJELENITES)
kod: KJV_MEGJELENITES
tipus: feladat
fazis: folyamat
munka: adat
modell: opus
allapot: nem_indult
helyi_gep: igen
ad: a pardes.db új kjv_szoveg táblája (Károli-kulcs, KJV-vers, Szöveg, Szöveg_jelolt, Elotte, Utoirat, leképezési mód) és a vers-lap új vers.kjv_szoveg blokkja, amely az Olvasópultban a Károli mellett párhuzamos hasábként mutatja a teljes KJV-szöveget; mérve a WSL-natív pardes.db-n és vizuálisan a #60 pilothoz
kovetkezo: indítás csak a #117 és a #118 merge-e és az N-F117a (a pardes.db építőjének őre) javítása után; ⛔ M0 (terv, a kiadási kapcsoló), ⛔ M2 (a felhasználó kipróbálja)
olvas: [konkordancia/KJV_teljes_szoveg.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, f22/versosszevonas.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, adat/licencek.tsv, adat/SEMA.md, eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/olvaso_szerver/]
fugg: [117, 118]
---
# KJV_MEGJELENITES_BRIEF.md — a teljes KJV-szöveg párhuzamos megjelenítése a Károli mellett

*FELADATOK #(a `/befogad` adja, a #118 merge-e után) · Modell: opus · v0 (tervezet) · 2026.10.18 · előzmény: #118 (KJV_SZOVEG, DT-F118c (b)), #117 (VERSMEGF_JAVITAS, N-F117a), #76 (olvasói konkordancia), #60 (pilot), DT124, DT126, DT-F118a*

*Tervezet a `beerkezo/`-ben (DT-F118c (b), felhasználó, 2026-10-18: „külön feladat, a beerkezo/ tervezetből /befogad-dal; fugg: 117, 118, és az N-F117a (a pardes.db építőjének őre miatt)”). A tartalom az `F118_KJV_SZOVEG_BRIEF.md` M4 pontjának minimális listája. A feladatszámot a `/befogad` adja.*

## 1. Cél

A `konkordancia/KJV_teljes_szoveg.tsv` (#118; 31 218 sor, közkincs, DT-F118a) megjelenítése az olvasó vers-lapján (#76, `eszkozok/olvaso_szerver/`, `pardes.db`), a Károli-szöveg mellett, párhuzamos hasábként. A meglévő `vers.kjv` szavankénti blokk (Strong-címkés, GPL-jelölésű, DT124) változatlan marad.

## 2. Előfeltételek és függés — ⛔ ezek nélkül nem indul

- **#117 merge-e** (`fugg: 117`): a Károli-vers ↔ KJV-vers párosítás forrása a `konkordancia/Karoli_versmegfeleltetes.tsv`, amelyet a #117 javít.
- **#118 merge-e** (`fugg: 118`): a `KJV_teljes_szoveg.tsv`, a `licencek.tsv` sora és a `SEMA.md` 2.6 leírása.
- **N-F117a javítása** (a #117 ágán felvett nyitott tétel, `NYITOTT_FELADATOK.md`; a `fugg` mező csak feladatszámot vesz fel, ezért itt áll). A #117 az `eszkozok/sqlite_epit.py`-ba őrt tett (`kezi_mt_or()`, a `VersmegfKeziMt` kivétel, a `_bsb_szamozas()` elején; `claude/f117-versmegf-javitas` ág, `7522cf6e`, F117.5, DT-F117f (a)). Az őr leállítja az építést, ha a versmegfeleltető táblában `KEZI` osztályú sor kitöltött `igehely_mt`-vel áll. A javított tábla 174 ilyen sort tartalmaz, ezért **a `pardes.db` az N-F117a javításáig nem építhető**. Az N-F117a tartalma (a #117 ágán): a `fj2/bsb_import.py` és az `eszkozok/sqlite_epit.py` javítása a `KEZI` + kitöltött `igehely_mt` sorokra; a két kihagyott teszt (`teszt_sqlite_epit.Integracio`, `FeliratHalmaz.test_a_felirat_versnek_nincs_terkep_erteke_a_db_ben`) visszavétele; utána a fogyasztók újragenerálása. Ha az N-F117a a befogadásig feladatszámot kap, az a `fugg` mezőbe kerül.
- **Ütközés:** az `ir` lista (`eszkozok/sqlite_epit.py`, `eszkozok/olvaso_szerver/`) a #76 és a #11 M3 `ir` listájával fedi egymást, ezért a feladat velük egyszerre nem fut; a sorrendet a `python eszkozok/feladatok.py fuggesek` adja.

## 3. Hatókör

**Benne van:**
- **`pardes.db`:** új `kjv_szoveg` tábla (javaslat: `igehely` Károli-kulcs, `kjv_igehely`, `szoveg`, `szoveg_jelolt`, `elotte`, `utoirat`, `mod`) a `sqlite_epit.py` meglévő `_kjv` betöltőjének mintájára (`Karoli_versmegfeleltetes.tsv` `igehely_kjv` → Károli-vers); a `SZARMAZTATOTT_LICENC` új sora (`KJV_teljes_szoveg` és a párosító tábla licenckulcsai); az `azonos_feltetelezett` tartalék csak ott, ahol a javított tábla nem ad párt, és jelölve (`mod`);
- **egy Károli-vers – több KJV-vers, és fordítva** (versösszevonás, `f22/versosszevonas.tsv`, eltolt fejezetek): minden párosított KJV-vers a saját KJV-versszámával jelenik meg. A Károli-vers nélküli KJV-vers (pl. a #117 N-F117b öt verse: KJV Hós 2:1, Jób 17:1, Péld 12:1, Jób 37:1, Ézs 64:2) nem vész el némán, hanem a jelentésben számolva áll;
- **blokk:** új vers-blokk (`vers.kjv_szoveg`, jelleg `forras`, licencsor a `licencek.tsv`-ből); az Olvasópult nézetben a Károli-szöveg mellett párhuzamos hasáb. A `Szöveg_jelolt` jelölése (`[…]` dőlt betoldás, `‹…›` Jézus szavai, `¶`) a megjelenítésben dőlt, illetve megkülönböztetett írásra fordítandó; az `Elotte` (Zsolt 119 akrosztichon) a vers fölött, az `Utoirat` (páli utóirat) a vers alatt; az 1Jn 2:23 forrásbeli „[but]”-ja a forrás szerint (DT-F118e (3));
- **kiadási kapcsoló:** a DT-F118a szerint a szövegréteg közkincs, tehát a nyilvános kiadásban is megmarad; a `vers.kjv` szavankénti blokk a DT124 szerint továbbra is kimarad (`adatbazis.TABLA_KIZARAS['kjv']`). A kereskedelmi kiadásban a `licencek.tsv` sora `kereskedelmi=feltetelesen` (UK letters patent): ⛔ M0 döntés (javaslat: marad, a licenc-súgó jelzi a feltételt);
- **mérés:** a `pardes.db` újraépítése a WSL-natív `~/pardes/pardes.db`-n; a tesztek a `python eszkozok/teszt_futtat.py` hívással; a `kjv_szoveg` sorainak száma és a párosítási módok megoszlása; a vers-lap vizuális összevetése a #60 pilottal (a látvány mércéje), nem csak számokkal.

**Nincs benne:** a `KJV_teljes_szoveg.tsv` és a `KJV_Strongs_teljes.tsv` módosítása; a `Karoli_versmegfeleltetes*` (#117) és az N-F117a javítása; a DT126 eldöntése.

## 4. Lépések (⛔ a kötelező megállások)

- **M0 — ⛔ terv:** az előfeltételek igazolása (a #117 és a #118 a main-en, az N-F117a javítva, a `sqlite_epit.py` őre nem áll le); a táblaséma, a párosítási szabály, a kereskedelmi kapcsoló.
- **M1 — építő és teszt:** `_kjv_szoveg` a `sqlite_epit.py`-ban, egységteszt (`eszkozok/teszt_sqlite_epit.py`): egy-egy, egy-több, több-egy, nincs pár, 0. vers (zsoltárfelirat), `Elotte`/`Utoirat`.
- **M2 — ⛔ blokk és kipróbálás:** `vers.kjv_szoveg` az `eszkozok/olvaso_szerver/`-ben, kiadásonkénti teszt; a felhasználó kipróbálja (minta: 1Móz 1:1–3, Zsolt 3 a felirattal, Zsolt 119:1/9, Mt 1:1, Mk 9:43, Róm 16:27, egy versösszevonás).
- **M3 — mérés és zárás:** napló, független ellenőrzés.

## 5. Elfogadási feltételek

- **E1.** A `pardes.db` `kjv_szoveg` táblája minden KJV-verset tartalmaz, vagy a hiány a jelentésben számolva áll; az `azonos_feltetelezett` sorok jelölve.
- **E2.** A `vers.kjv_szoveg` blokk a belső és a nyilvános kiadásban megjelenik, a `vers.kjv` a nyilvánosban nem; a kereskedelmi kiadás az M0 döntése szerint.
- **E3.** A tesztek a `python eszkozok/teszt_futtat.py` hívással zöldek; a két N-F117a-skip vissza van véve (az N-F117a feltétele).
- **E4.** Vizuális összevetés a #60 pilottal; független ellenőrzés a zárás előtt.
