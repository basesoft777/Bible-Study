---
feladat: 240
cim: Kis adatjavítás — hamis görög LXX-megfelelés, nyelvtani szó az LXX-megfelelők közt, kettőzött könyvnév a fordított BDB-szövegben, hamis jelentés a BDB-utalás miatt
kod: LXXBDB
tipus: feladat
fazis: folyamat
modell: opus
sav: CONTENT
allapot: fut
alap: 50976c3a
ad: a szólapon és a BDB-kártyán nem áll hamis görög megfelelő (φωσφόρος a „reggel” szónál), nyelvtani szó (μου, σου) az LXX-megfelelők közt, sem kettőzött könyvnév („Zsolt Zsolt 97:7”) és belőle csonka fejléc, és a versenkénti jelentés nem ugrik egy „see N infra” utalásra (tehóm: „örvény · 5”); mind a négy a forrásban javítva, gépi kapuval
kovetkezo: Folytatás: L1–L6 a brief szerint, majd független ellenőr és push előtti kapu
munka: adat
olvas: [IRANY.md, adat/SEMA.md, adat/grammatikai_strongok.tsv, adat/kulso/lxx_bridge.tsv, adat/forditasok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_aranyminta.tsv, konkordancia/BDB_teljes_unabridged.tsv, "konkordancia/Macula_heber_*.tsv", konkordancia/LXX_OS/, konkordancia/Strong_szotar.tsv, eszkozok/grammatikai_strongok_general.py, eszkozok/sqlite_epit.py, eszkozok/bdb_adatblokk.py, eszkozok/bdb_psi_javit.py, eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, adat/bdb_szakaszok.tsv, naplok/F34_M0_felmeres.md]
ir: [F240_LXX_BDB_ADATJAVITAS_BRIEF.md, naplok/F240_dontesek.md, adat/grammatikai_strongok.tsv, adat/lxx_strong_javitas.tsv, adat/forditasok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_aranyminta.tsv, adat/SEMA.md, konkordancia/BDB_teljes_unabridged.tsv, eszkozok/grammatikai_strongok_general.py, eszkozok/lxx_strong_javitas.py, eszkozok/bdb_konyvketto_javit.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, adat/bdb_vers_jelentes.tsv, eszkozok/sqlite_epit.py, eszkozok/bdb_adatblokk.py, eszkozok/ellenoriz.py, "eszkozok/teszt_lxxbdb*.py", "naplok/LXXBDB_*", naplok/F240_jelentes.md, nyitott/uj/lxx-bdb-adatjavitas-213252.md, dontesek/uj/lxx-bdb-adatjavitas-213252.md]
fugg: []
nem_fugg: [7, 101, 106, 122, 133, 134, 135, 137, 138, 139, 147, 153, 154, 164, 231, 233, 235, 236]
helyi_gep: igen
---

# F240 — Kis adatjavítás: LXX-megfelelés és BDB-könyvnév (LXXBDB)

**Honnan:** `IRANY.md` „Következő szálak” első sora (a szerkesztő a #810-es olvasó-előnézeten látta, `/szo/H0430`, `/szo/H1242`). A tétel az IRANY-ban áll, ezért a jóváhagyás az integrátoré (DT-F0b). Az N-F231a (#231 ága, `nyitott/uj/olvaso-egyben-3464e1.md`) célfeladata ez a brief.

**Nehéz kör** (DT919): adatot és adatbázis-építést érint → független ellenőr, legfeljebb egy javítókör, teljes `python eszkozok/push_elott.py`. Lapgen-futás nem kell (a mérés szerint egyik `lexikon/*_TUDOMANYOS.md` sem mutatja az érintett párokat vagy kettőzést); ha mégis kell: előtte `python.exe`-lista, egyszerre egy futás.

## 0. Mérés (2026-11-23, `pardes.db` a main tükréből, csak olvasva; a mérőszkriptek a scratchpadben, a jelentés a `naplok/LXXBDB_meres.md`-be kerül)

**1. osztály — hamis görög Strong a Macula LXX-párjaiban.** A `konkordancia/Macula_heber_*.tsv` `gorog_strong` oszlopa a Macula forrás `greekstrong` attribútuma, változatlanul (`eszkozok/f17/macula_futtat.py`). A `πρωὶ` (tompa ékezetes) alak 88-szor (a H1242 „reggel” sorain; összesen 90) `G5459` (φωσφόρος) címkét kapott a `G4404` (πρωΐ) helyett; az LXX_OS-ben a G5459 egyszer sem fordul elő. Az `adat/kulso/lxx_bridge.tsv` (bcv-commons, a Macula összesítése) ugyanezt viszi tovább: `H1242 G5459 88` / `G4404 47` — pontosan a token-szám. **Nem egyedi:** a Macula-tokenek és az LXX_OS (ugyanaz a Károli-vers, ugyanaz az ékezet-normalizált alak) összeillesztése szerint további Macula-címkék mutatnak más lemmára, pl. `μόσχους` → G2353 θρέμμα (42), `βόες/βοος` → G1003 Βοόζ (26), `φόρου` → G5410 (4), `ἀποστάται` → G3848 (4), `μόνας` → G2651 (3), egy-egy ritkább. A pontos lista a mérésnaplóba kerül, soronként ítélettel.

**1b. (mellékelet, nem e brief hatóköre — a ⛔1 dönti el) — az LXX_OS homográf-hibái.** Az `eszkozok/lxx_os_import.py` a lemmát ékezet- és lehelet-mentesen, kisbetűsítve keresi a GreekWordList-ben (`strip_accents`), ezért az azonos betűsorú lemmák egy Strong-számra esnek: εἷς „egy” → G1519 εἰς „-ba” (≈460 + μία 263), τίς „ki?” → G5100 τις (≈1100), μήν „hónap” → G3375 (198), ποῦ/πῶς/πότε (≈210), καρπός → G2591 Κάρπος (97), στέφανος, σμύρνα, στάχυς, γάζα, φοῖνιξ, ἕκτος, ὦ. Az olvasó versnézetének LXX-sorában ezek rossz szólapra visznek. A javításhoz a két rögzített forrásfájl (lxx-morph `verse_pairs.jsonl`, `GreekWordList.js`, a szkriptben rögzített commitokból) **letöltése** és az LXX_OS újragenerálása kell.

**2. osztály — nyelvtani szó az LXX-megfelelők közt.** Az `adat/grammatikai_strongok.tsv` görög oldala (31 Strong) a lemma-szintű számokat ismeri (G1473 ἐγώ, G4771 σύ, G3778 οὗτος, G0846 αὐτός). A Macula LXX-címkéi viszont a Strong-szótár **alakszámait** használják: μου G3450 (3 578 token), σου G4675 (4 735), αὐτούς/αὐτήν G0848 (2 176), ὑμῶν G5216, σε G4571, σοι G4671, ἡμῶν G2257, μοι G3427, τοῦτο G5124, ταῦτα G5023, és még kb. 25 alak (névmás, mutató névmás, összevont tagadó). Ezek átcsúsznak a szűrőn: a BDB-kártya jelentésenkénti LXX-sora (`blokkok._szk_lxx`) és a „Görög megfelelő (Septuaginta)” blokk (`lxx_bridge`) is mutatja őket (H0430: „θεός 4 · μου 1”). A gyökérok a lista, nem a megjelenítés. *A hány szónál fordul elő pontos száma (szólap és jelentés szerint) a mérésnaplóba kerül.*

**3. osztály — kettőzött könyvnév a BDB-szövegben, és belőle csonka fejléc.** A forrás (`konkordancia/BDB_teljes_unabridged.tsv`) a BDB ψ-jelét „Psalm” szóként adja, utána a hivatkozás saját könyvrövidítése áll; az F34 (`bdb_psi_javit.py`) a rossz könyvet `Psa`-ra javította, a „Psalm Psa …” kettőzés kezelését „M1-es opcióként” nyitva hagyta (`naplok/F34_M0_felmeres.md`), és nem készült el. Angolul 35 kettőzés 33 szócikkben (`Psalm/Paslm Psa` 13, `Job Job` 14, `Ruth Ruth` 3, `Neh Neh` 2, `Dan Dan` 2, `Prov Prov` 1); ebből néhány valódi személynév + hivatkozás (`Dávid 2Sám 5:10, Jób Jób 1:3`; `Ámós Ámós 7:12`), ezek maradnak. A magyar fordításban (`adat/forditasok.tsv`, 43 előfordulás) „Zsolt Zsolt”, „Zsoltár Zsolt”, „Jób Jób”, „Neh Neh”, „Dán Dán”, „Jóel Jóel”, „Ruth Ruth”, „Péld Péld”, „1Móz 1Móz”, „Ez Ez” áll; a fordító az angol „Psalm 40:18”-at is „Zsoltár Zsolt”-ra tette (6 hely). A csonka fejléc („c. angyalok Zsolt”) ugyanennek a következménye: a fejléc a jelentés szövege az első hivatkozásig, és a kettőzés első tagja ottmaradt.

## Feladat

**L1 — Macula LXX-Strong javítása (1. osztály).**
1. `naplok/LXXBDB_meres.md` + `naplok/LXXBDB_lxx_jeloltek.tsv`: a Macula–LXX_OS összeillesztés teljes jelöltlistája (Macula-Strong ≠ az LXX_OS-beli Strong, a Macula-Strong az LXX_OS-ben nem fordul elő, a két lemma nem azonos szó), soronként ítélettel: `macula_hiba` / `konvencio` (alakszám, pl. μου G3450 ↔ ἐγώ G1473) / `lxx_os_hiba` (az 1b-be) / `nem_eldontheto`.
2. `adat/lxx_strong_javitas.tsv` (új, kézi, `manual` proveniencia, SEMA-sorral): `alak_norm`, `hibas_strong`, `helyes_strong` (üres, ha a helyes lemmának nincs Strong-száma), `indok`, `proveniencia`. Csak a `macula_hiba` sorok.
3. `eszkozok/lxx_strong_javitas.py`: egy közös segéd, amelyen át **minden fogyasztó** olvas: a Macula-token `gorog_strong`-ját javítja, és az `lxx_bridge`-et a javított tokenek különbségével (héber Strong szerint −1/+1) igazítja. Bekötve: `sqlite_epit.py` (`token_macula`, `lxx_bridge`), `bdb_adatblokk.py`, és minden további olvasó, amelyet a grep talál (a nyers `lxx_bridge.tsv` és `gorog_strong` közvetlen olvasása a segéden kívül kapuval tiltva). A nyers forrásfájlok változatlanok (licenc, SHA).
4. **Kapu:** az `ellenoriz.py`-ben új szabály: (a) a javított Macula-párok közt nincs olyan, amely az összeillesztés szerint `macula_hiba`-mintájú, és nincs ítélve a jelöltlistán (új forrásverzió esetén bukik); (b) a nyers fájlt csak a segéd olvassa.

**L2 — Nyelvtani lista az alakszámokkal (2. osztály).**
1. `grammatikai_strongok_general.py`: `GOROG_KEZI` mellé `GOROG_ALAK` lista — a már felvett lemmák Strong-alakszámai (μου G3450 → ἐγώ G1473 stb.), soronként „X alakszáma” indokkal; új kategória nincs, a kritérium nem változik (a lemma már nyelvtani). Nem kerül be: εἷς G1520, μία G3391 (számnév; csak az LXX_OS homográf-hibája miatt látszik nyelvtaninak). A tábla újragenerálása.
2. **Kapu:** a Macula LXX-Strong, amely az összeillesztés szerint ≥90%-ban egy nyelvtani lista-elem alakjával esik egybe, és legalább 3 tokenje van, vagy a listán áll, vagy a generátor kivétellistáján indokkal — különben bukik.
3. A mérésnaplóba: hány héber szónál és hány BDB-jelentésnél tűnik el nyelvtani szó az LXX-sorból (előtte / utána).

**L3 — Kettőzött könyvnév (3. osztály).**
1. `eszkozok/bdb_konyvketto_javit.py` (az F34 `bdb_psi_javit.py` mintájára: száraz futás, `--ir`, mezőkulcsos és pozícióhoz kötött csere, írás előtt sor-összevetés, `split('\t')`): az angol forrásban és az `adat/forditasok.tsv` BDB-soraiban a hivatkozás előtti kettőzött könyvszó törlése; a `forras_hash` frissítése a változott angol szöveghez (fizetős újrafordítás nélkül). Csere-napló: `naplok/LXXBDB_konyvketto_csere.tsv` (szócikk, pozíció, régi, új, döntés, ok); a személynév-esetek `marad` döntéssel, egy sor indokkal.
2. `adat/bdb_szakasz_hu.tsv` újragenerálása (`bdb_jelolt/hu_illeszt.py`); az `adat/bdb_aranyminta.tsv` érintett kézi sorainak igazítása a forráshoz.
3. **Kapu:** az `ellenoriz.py`-ben: a BDB angol forrásában és a magyar fordításban hivatkozás előtt nem áll kettőzött könyvszó, kivéve a csere-napló `marad` sorait.
4. A csonka fejléc ellenőrzése: a H0430 „c.” jelentés fejléce a javítás után „angyalok”; az összes fejléc közül, amely könyvszóra végződik, a mérésnaplóba (előtte / utána).

**L5 — Hamis versenkénti jelentés a BDB „see N infra” utalása miatt (4. osztály; az integrátor bővítése, 2026-11-23).** A tehóm (H8415, TEREMT-001 próbalap) 1. táblájának jelentés-oszlopa minden ószövetségi helyen „örvény · 5”-öt mutat. Mérve (`adat/bdb_vers_jelentes.tsv`, csak olvasva): a H8415 44 sorából 38 a `-/5` útvonalat kapja, a „Psa 71:20 (but see 5 infra)” utalástól (táblapozíció ≈ 322) kezdve, holott az 1–4. jelentés szakaszai (`adat/bdb_szakaszok.tsv`) utána állnak; a lábjegyzet ezért hamisan mondja, hogy a BDB az 5. szakaszban maga idézi a helyet (pl. 1Móz 49:25, 7:11). A BDB-ben 37 szócikkben 47 ilyen utalás áll („see/compare N infra/supra/below/above”); ezek közül a mérés szerint csak a H8415 sorai csúsznak el (a H1696, H2403, H5927, H7462 útvonal-sorrendje rendben). A gyártó: `eszkozok/olvaso_szerver/bdb_vers_jelentes.py` (`TablaPont`, a hivatkozás → jelentéspont leképezés).
1. A gyökérok pontos helyének igazolása a gyártóban (melyik lépés olvassa az utalást jelentéskezdetnek), és javítása **minden szóra**: a „see N infra/supra/below/above” típusú utalás nem jelentéskezdet.
2. A teljes `adat/bdb_vers_jelentes.tsv` újragenerálása; soronkénti diff a `naplok/LXXBDB_vers_jelentes_diff.tsv`-be, összesítve: hány szó, hány igehely változik.
3. **Kapu:** (a) az utalás-minta a jelentéskezdet-felismerésben bukás (egységteszt a H8415-re és egy szintetikus esetre); (b) általános konzisztencia: a sor nem kaphat olyan jelentéspontot, amelynek szakasza a sor táblapozíciója után kezdődik (a javítás előtti állapoton a H8415-ön bukik; a mérésnapló rögzíti, hány további szót jelez, és azok ítéletét).
4. A kiadott lapok ellenőrzése: a mérés szerint a H8415 a kiadott lapok közül csak az ALVIL-001 proveniencia-sorában áll, az 1. táblában nem; a végrehajtáskor a kiadott lapok (HAMART-001, ISTENTISZT-001, ALVIL-001 és a többi `lexikon/*_TUDOMANYOS.md`) 1. táblájának jelentés-oszlopát a diff alapján újra ellenőrizni, és ha bármelyik érintett, azonnal jelezni az integrátornak.

**L6 — Közszó tulajdonnév-címkével az LXX-párokban (az integrátor bővítése, 2026-11-23).** A TEREMT-001 próbalapjának 5. (LXX) szakaszában a 2Móz 15:5 πόντῳ-ja a G4195 „Pontosz · Pontusz” (földrajzi név) címkét kapja; a jelentés ott „tenger” (közszó). Mérve (`pardes.db`, csak olvasva): a címke az **LXX_OS**-ből jön (`lxx_token`: πόντῳ, lemma πόντος → G4195; az LXX_OS-ben 2 hely), a Macula-párokban a G4195 nem fordul elő (a 2Móz 15:5 H8415-tokenje mellett a Macula görög Strongja üres), a `lxx_bridge`-ben sincs. A gyökérok tehát azonos az N-F240a-éval: az `lxx_os_import.py` a lemmát kisbetűsítve, ékezet nélkül keresi, így a közszó a tulajdonnév Strong-számát kapja (mint a καρπός → Κάρπος, στέφανος → Στέφανος, σμύρνα → Σμύρνα).
1. A közszó ↔ tulajdonnév homográf-osztály teljes mérése mindkét forrásban (Macula, LXX_OS): a Strong-szótár szerint tulajdonnévi Strong, amelyet a szövegben kisbetűs alak visel; az eredmény a mérésnaplóba (`naplok/LXXBDB_meres.md`), forrásonként és szavanként.
2. A Macula-esetek az L1 javítótáblájába kerülnek (ugyanaz a segéd és kapu). Az LXX_OS-esetek (a πόντος is) az N-F240a hatókörébe tartoznak (DT-F240a, külön PR); a mért szám és a példák az N-F240a-ba kerülnek. ⛔3: ha az integrátor a πόντος javítását mégis ebben a PR-ban kéri, az az LXX_OS újragenerálását vonja be (a letöltési engedély megvan).
3. **Kapu:** kisbetűs szóalak tulajdonnévi Strong-számmal az LXX-párokban bukás; az LXX_OS-esetekre az N-F240a lezárásáig kivétel, csak csökkenő darabszám-plafonnal (mint az L1/L2-nél).

**L4 — Ellenőrzés.** Az olvasó-szerver tesztjei (`python eszkozok/teszt_futtat.py --gyors`), egy próba-adatbázis a repón kívül (a 8765-ös tükör adatbázisát és más session szerverét nem érinti), azon a `/szo/H0430`, `/szo/H1242` és két további érintett szó és a TEREMT-001 próbalapjának tehóm-sorai ágas előnézetben (szabad 8776–8779-es port), a független ellenőr (`fuggetlen-ellenor`) a base..head diffen, legfeljebb egy javítókör, teljes `push_elott.py`. A PR első sora: „Mérce · Állapot · Következő · Akadály”.

## Döntések (az integrátor, a felhasználó felhatalmazásával, 2026-11-23)

- **⛔1 → (b) (DT-F240a):** az 1b (az LXX_OS homográf-hibái, kb. 1 800 hely) külön N-tétel és külön PR: **N-F240a** (`nyitott/uj/lxx-bdb-adatjavitas-213252.md`). Indok: a két forrásfájl letöltése új forrás, ehhez a szerkesztő engedélye kell (letöltés, licenc: `Rendszerfejlesztesi_playbook.md` 2. pont); egy feladat = egy kis PR. Addig az L1 és az L2 kapuja az LXX_OS homográf-párjaira kivétellel él, **darabszám-plafonnal, amely csak csökkenhet**, az N-F240a-ra hivatkozva.
- **⛔2 → igen (DT-F240b):** ahol a hibás Strong mögötti lemmának nincs Strong-száma, a pár „megfelelő nélkül” lesz, **kifejezetten jelölve** (a javítótábla `helyes_strong` mezője üres, az `indok` kimondja; az olvasó a „megfelelő nélkül” számban mutatja), nem csendben üres. Indok: a hamis megfelelés rosszabb a hiányzónál (CLAUDE.md 3. szabály).

## Kész, ha

- a négy osztály minden mért példánya javítva vagy a naplóban `marad` / `nem_eldontheto` ítélettel, egy sor indokkal (hamis tartalom nem marad elvetve);
- a négy osztály kapui élnek, és a javítás előtti állapoton bukik (próbával igazolva);
- a független ellenőr jelentése a `naplok/F240_jelentes.md`-ben; a `push_elott.py` zöld; a PR nyitva.
