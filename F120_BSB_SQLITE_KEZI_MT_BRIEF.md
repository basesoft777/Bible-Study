---
feladat: 120
cim: A bsb_import és a sqlite_epit javítása a KEZI + kitöltött igehely_mt sorokra (N-F117a, 1. rész)
kod: BSB_SQLITE_KEZI_MT
tipus: feladat
fazis: folyamat
munka: adat
modell: opus
allapot: nem_indult
helyi_gep: igen
ad: a BSB-import és az SQLite-építő helyesen kezeli a javított Károli-versmegfeleltető tábla 174 KEZI + kitöltött igehely_mt sorát; a DT-F117f őre és a két feltételes tesztkihagyás megszűnik, az olvasó adatbázisa újra építhető, a BSB Strong-tábla a döntés szerint újragenerálva
kovetkezo: indítás a /kovetkezo-val (opus, helyi gép: BSB-klón kell); első ⛔ a 3.2 kulcsszemantika-döntés (DT-F120a)
olvas: [konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_versmegfeleltetes_javitas.tsv, konkordancia/README.md, konkordancia/TAHOT_kivonat.tsv, konkordancia/BSB_Strongs.tsv, eszkozok/fj2/bsb_verseltolas_diag.py, eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py, eszkozok/fj2/bsb_parameter_erzekenyseg.py, eszkozok/fj2/wlc_versek.py, naplok/F117_meres.md, naplok/F117_fogyaszto_proba.py, naplok/F117_mt_levezetes.tsv, naplok/F117_osztaly_utkozes.tsv, naplok/VERSMEGF_JAVITAS_zaras.md, naplok/ELLENOR_VERSMEGF_JAVITAS.md, naplok/F41_wlc_versszam_ellenorzes.tsv, naplok/F16_bsb_zsolt_megfeleltetes.tsv, naplok/F85_jelentes.md, adat/SEMA.md, F117_VERSMEGF_JAVITAS_BRIEF.md]
ir: [eszkozok/fj2/bsb_import.py, eszkozok/fj2/teszt_bsb_import.py, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, konkordancia/BSB_Strongs.tsv, naplok/F41_wlc_versszam_ellenorzes.tsv]
fugg: [117]
nem_fugg: [48]
---

# F120_BSB_SQLITE_KEZI_MT_BRIEF.md — A bsb_import és a sqlite_epit javítása a KEZI + kitöltött igehely_mt sorokra

*FELADATOK #120 (várható szám; a végleges a befogadáskor) · Modell: opus (két fogyasztó számozási szemantikája, ⛔ döntési pontokkal; a #117 is opus volt) · v0 tervezet · 2026.10.18 · előzmény: N-F117a (NYITOTT_FELADATOK.md), DT-F117e (c), DT-F117f (a), `naplok/F117_meres.md` 2. és 4. pont, `naplok/VERSMEGF_JAVITAS_zaras.md` 10–11. pont*

*Befogadási megjegyzés.* A tervezet a #117 ágáról (`claude/f117-versmegf-javitas`, PR #409, draft) olvasott állapotra épül; a hivatkozott N-F117a, DT-F117e/f és F117-naplók a `main`-en csak a PR #409 merge-e után lesznek ott. Ezért `fugg: [117]`. A `teszt_bsb_import.py` új fájl (ma nincs tesztje a `bsb_import`-nak). Az N-F117a második fele (a többi fogyasztó újragenerálása) **nem** ennek a briefnek a része: külön tétel (6. szakasz).

## 1. Cél

A DT-F117e (c) óta a `konkordancia/Karoli_versmegfeleltetes.tsv`-ben 174 `KEZI` osztályú sor kitöltött `igehely_mt`-t hordoz, ahol az érték a valódi MT-vers, és eltér a Károli-számtól. Két fogyasztó a régi konvenciót feltételezi, amely szerint a kitöltött `igehely_mt` azonos a Károli-számmal (csak `MT` osztályú sorban állt):

1. **`eszkozok/fj2/bsb_import.py`.** Az `igehely_mt`-ből MT-fejezet-maximumot számol (`kk_max_tabla`, `_kk_mt_max`), és a TAHOT fejezet-maximumával veti össze. A TAHOT az F85.6 óta Károli-kulcsú (`CLAUDE.md`, „Adat-tár”), a kettő tehát nem összevethető.
2. **`eszkozok/sqlite_epit.py` `_bsb_szamozas()`.** MT-kulcs → Károli-vers leképezés a kitöltött `igehely_mt`-ből (`mt_kk`), különben azonosság. Az azonosság-tartalék a szomszéd fejezet MT-verseit a Károli-fejezet elejére teszi, így a mérés szerint 6 Károli-vers két BSB MT-verset kapna: Hós 2:1–3, Jób 17:1, Jób 37:1, Péld 12:1.

A cél a két fogyasztó javítása úgy, hogy a kanonikus tábla (adat-réteg) változatlan marad (DT-F117f (a)), a DT-F117f őre (`kezi_mt_or`, `VersmegfKeziMt`) kivezethető, a `teszt_sqlite_epit.py` két feltételes kihagyása (`kezi_mt_or_kihagy()`) magától megszűnik, és a `pardes.db` újra építhető.

## 2. Hatókör

**Benne van:**
- a `bsb_import.py` MT-maximum-ellenőrzésének (R4 a `konyv_megfeleltetes()`-ben, valamint a `fejezet_eltolasok()`) átírása a Károli↔MT párokra;
- a `sqlite_epit.py` `_bsb_szamozas()` javítása: az azonosság-tartalék csak ott, ahol a vers tényleg nem kap táblapárt, és ahol az azonosság nem ütközik;
- a `kezi_mt_or` őr, a `VersmegfKeziMt` és a `teszt_sqlite_epit.kezi_mt_or_kihagy()` kivezetése; a `KeziMtOr` tesztosztály átírása pozitív tesztté (a `KEZI` + mt sor helyes leképezése);
- új `eszkozok/fj2/teszt_bsb_import.py` fixtúrás tesztekkel (R4 a három osztályra: `KJV`, `MT`, `KEZI` + mt);
- a `BSB_Strongs.tsv` újragenerálása, **ha** a 3.2 ⛔ így dönt (helyi gép: a BSB-klón kell, `--munka` a repón kívül);
- a `pardes.db` építési próbája a repón kívüli kimenetbe (a valós építés a felhasználó gépén, #101).

**Nincs benne:**
- a `Karoli_versmegfeleltetes.tsv` és a `_javitas.tsv` módosítása (DT-F117f (a): a tábla marad; ha a javítás táblaváltozást igényelne, ⛔);
- a többi fogyasztó újrafuttatása (Macula `karoli` oszlop, `LXX_OS`, `karoli_strong`, `bdb_vers_jelentes`, `bdb_szelet_m0`, TSK-lexikonoldalak, `nave_*`, `tahot_verskulcs_*`, `f08/*` stb.; lista: `naplok/F117_meres.md` 2. pont): 6. szakasz, külön tétel;
- az N-F117b (öt összevont vers visszairányú TSK-vesztesége), az N-F117c, az N-F117d;
- a `Pozitiv.test_mai_adat_zold` FAIL-ja (a `main`-en is fennálló „15. kapcsolatok.tsv” jelentéssor, nem e tétel tárgya).

## 3. Lépések (⛔ a kötelező megállások)

### 3.0 Modell-ellenőrzés és ág
Kiírod a tényleges modellnevedet, és összeveted a fejléc `modell: opus` mezőjével; eltérésnél megállsz (CLAUDE.md). Ág: `claude/f120-bsb-sqlite-kezi-mt`, a PR #409 merge-e utáni `main`-ről. Először keresd meg, van-e már ága/worktree-je a feladatnak.

### 3.1 Újramérés: a tényleges hibamód (csak olvas)
Az N-F117a és a `naplok/F117_meres.md` a `bsb_import` hibáját `SystemExit`-ként írja le (13 fejezet). **A tervezet kódolvasása szerint ez pontosítandó** (scope=manual, a #117 ágának `bsb_import.py`-ja):
- a `fejezet_eltolasok()` (a `SystemExit` forrása) a `bsb_import.py` fő útján **nem hívódik**; csak a `fj2/bsb_verseltolas_diag.py:250` hívja;
- a fő út (`fut()` → `ot_konyv()` → `konyv_megfeleltetes(…, kk_max)`) az R4 szabályt alkalmazza: eltérésnél `allapot[f].append('kk_max_eltérés: …')`, a fejezet **csendben `illesztetlen`** lesz, és kimarad az importból. Ez adatvesztés, nem leállás, és a veszélyesebb hibafajta („minden hibátlanul lefut”).

Feladat: az F117 próbáját (`naplok/F117_fogyaszto_proba.py`) kiterjesztve mérd meg, a régi és az új táblán:
1. az R4 hány BSB-fejezetet tenne `illesztetlen`-né, melyeket, és hány BSB-verssel/-sorral (a BSB-klón nélkül: a `kk_max_tabla` × TAHOT-max összevetés fejezetlistája; a klónnal: a tényleges `allapot`);
2. a `bsb_verseltolas_diag.py` `fejezet_eltolasok()`-hívása hol állna le;
3. a `sqlite_epit._bsb_szamozas()` ütközései a mai `BSB_Strongs.tsv`-n (az F117 szerint 6), és az `azonos_feltetelezett` sorok száma fejezetenként.

Kimenet: `naplok/F120_meres.md`, proveniencia-sorral (`scope=… | forras=… | eszkoz=… | ts=…`). Commit: `F120.1:`.

### 3.2 ⛔ A `BSB_Strongs.tsv` `Igehely`-kulcsának szemantikája
A `bsb_import` a BSB-verset a TAHOT verseihez illeszti (`mt_versek(forras, fmag)`, Strong-illeszkedés). A `BSB_Strongs.tsv` utolsó generálása 2026-10-02/06 (F41, F71), **az F85.6 versszintű átkulcsolása előtt**, amikor a TAHOT-kulcs még nem volt Károli-vers. Ma a TAHOT `Igehely`-kulcsa a Károli-vers. A mai fájlban a `Számozás` oszlop vegyes (`mt` / `kjv` / `ellenorizetlen`); a Hós 1:10–2:1 sorai például `ellenorizetlen`, KJV-szerű számozással.

Ebből adódik a kérdés: **újrafuttatva a `bsb_import` milyen számozást ad az `Igehely`-be?** Ha a TAHOT Károli-kulcsú, a „MT-vers” valójában Károli-vers lesz. Ekkor a `sqlite_epit` MT→Károli leképezése (`mt_kk`) kétszeres leképezés volna, és a `kk_max` R4-ellenőrzésnek sincs értelme. A 3.1 mérése után vázold a lehetőségeket, előny–hátrány–javaslat formában, `DT-F120a` helyőrzővel. Legalább ezeket:
- **(a)** a `BSB_Strongs.tsv` `Igehely` = MT-vers marad; a `bsb_import` az MT-kulcsot a TAHOT Károli-kulcsából a versmegfeleltető táblán át (Károli → `igehely_mt`, üres mt-nél `MT`/`KJV`-osztály szerint) állítja elő; a `sqlite_epit` MT→Károli leképezése értelmes marad;
- **(b)** a `BSB_Strongs.tsv` `Igehely` = Károli-vers (a TAHOT-tal azonos kulcs); a `sqlite_epit` `_bsb_szamozas()` azonosságot vesz, az `mt_kk` kikerül; a SEMA/`datasetek.tsv` leírása és a fejléc módosul;
- **(c)** a `BSB_Strongs.tsv` nem generálódik újra; csak a `sqlite_epit` javul a mai (F85.6 előtti, MT/KJV-vegyes) fájlra, és az újragenerálás külön tétel.

Itt **megállsz**, a felhasználó dönt. Döntési tétel a `DONTESEK.md`-be (helyőrzővel).

### 3.3 A `bsb_import` javítása (a DT-F120a szerint)
- Az R4 és a `fejezet_eltolasok()` a Károli↔MT párokra: az MT-fejezet maximumát az MT-oldali adattal vesd össze, ne a Károli-kulcsú TAHOT-maximummal. A `KJV` osztályú sorok kizárása (`kk_max_tabla` docstringje) marad. A `KEZI` + mt sor az MT-oldalra számít, a Károli-oldalra nem.
- A Zsoltár-ág (F16, `k` = 0..2) és a Jób 41 / `KEZI_KIVETEL` (F71) viselkedése nem változhat: bájtra azonos import a Zsoltárokon (`naplok/F16_bsb_zsolt_megfeleltetes.tsv`), és a Zsolt 13 kézi kivétele is.
- `teszt_bsb_import.py`: fixtúra (pici versmegfeleltető + TAHOT-max), R4 mindhárom osztályra; egy `KEZI` + mt fejezet **nem** lesz `illesztetlen`; egy valódi eltérés továbbra is az lesz (negatív próba: a régi viselkedés szándékos visszaállítására a teszt piros).
- A `bsb_verseltolas_diag.py` hívója nem az `ir`-ben áll: ha a `fejezet_eltolasok()` szignatúrája változik, ⛔ (egyeztetett eltérés kell).

Commit: `F120.3:`.

### 3.4 A `sqlite_epit` javítása
- `_bsb_szamozas()`: az azonosság-tartalék (`azonos_feltetelezett`) csak akkor, ha (i) a BSB-kulcs nem szerepel `mt_kk`-ban, **és** (ii) a kapott Károli-vers nem célja egy `mt_kk`-párnak (ugyanaz a Károli-vers nem kaphat két MT-forrást). Ütközésnél a tartalék sor **nem** kerül be csendben: `jelent_norm('bsb', …, 'azonosság ütközik táblapárral')`, és számlálva a jelentésbe. A DT-F120a (b) esetén a függvény egyszerűsödik, az ütközés-őr marad.
- A `kezi_mt_or`, a `VersmegfKeziMt` és a hívása törlendő; a `teszt_sqlite_epit.kezi_mt_or_kihagy()` és a két hívása szintén (N-F117a: „a segédfüggvény ekkor törölhető”). A `KeziMtOr` osztály átírandó: fixtúrával a `KEZI` + mt sor a helyes Károli-versre képez, a 6 ismert ütközés-mintából egy sem keletkezik.
- `python eszkozok/teszt_sqlite_epit.py -v`: az `Integracio` (34 teszt) és a `FeliratHalmaz.test_a_felirat_versnek_nincs_terkep_erteke_a_db_ben` újra fut és zöld; a skip-szám 0 (vagy csak a nem e tételhez tartozó, megnevezett skip). A `test_mai_adat_zold` FAIL-ja marad (nem e tétel tárgya), és jelentve van.

Commit: `F120.4:`.

### 3.5 ⛔ Újragenerálás (a DT-F120a szerint) és mérés
- Ha a döntés (a) vagy (b): `python eszkozok/fj2/bsb_import.py --munka <repón kívüli mappa>` a BSB-klónnal (helyi gép). Ha a klón nem elérhető, ⛔: a felhasználó adja meg a helyét, vagy a lépés a gépén fut.
- Mérés, a régi és az új `BSB_Strongs.tsv` között: sorszám, fejezetenkénti `illesztetlen`, `Számozás`-eloszlás, a 13 érintett fejezet sorai, és a Zsoltárok bájtazonossága. Minden eltérést a táblához kell kötni (a 346 A–D′ vers vagy a 3.2 kulcsváltása); ami nem köthető, ⛔.
- `pardes.db` építési próba a repón kívüli kimenetbe (`PARDES_DB` vagy `--kimenet`), WSL-natív úton (`eszkozok/teszt_futtat.py` mintájára, `/mnt/c` nélkül). Az építés nem állhat le, és a `bsb` táblában nincs Károli-vers két különböző MT-forrással (SQL-lel igazolva, a lekérdezés a naplóban).

Itt **megállsz**: a felhasználó jóváhagyja-e a `BSB_Strongs.tsv` cseréjét a repóban (adat-réteg, kanonikus). Commit (jóváhagyás után): `F120.5:`.

### 3.6 Zárás
- `naplok/F120_zaras.md` (eredmény, mérés, egyeztetett eltérések, nyitott tételek), a brief fejléce (`allapot`, `ad`, `kovetkezo`, `lezarva_osszegzes`).
- `NYITOTT_FELADATOK.md` N-F117a: az 1. rész (bsb_import + sqlite_epit) lezárva, a fogyasztói újragenerálás nyitva (→ 6. szakasz).
- Független ellenőrzés (`fuggetlen-ellenor`): `naplok/ELLENOR_F120.md`.
- Push és PR csak a felhasználó kérésére.

## 4. Elfogadási feltételek

- **E1.** A `bsb_import` a javított táblán egyetlen fejezetet sem tesz `illesztetlen`-né `kk_max_eltérés` miatt, ha az eltérés oka csak a `KEZI` + mt sor (a 13 fejezet: 1Sám 20, 21; 2Móz 36; Hós 2; Jób 17, 37, 40; Préd 10; Péld 12; Én 6, 7; Ézs 2, 3). Valódi eltérésre az R4 továbbra is jelez: ezt negatív teszt igazolja.
- **E2.** A `sqlite_epit` `bsb` táblájában 0 Károli-vers kap két különböző MT-forrást, és 0 sor kerül be azonossággal táblapárral ütközve. Az F117 6 esete (Hós 2:1–3, Jób 17:1, Jób 37:1, Péld 12:1) név szerint ellenőrizve van.
- **E3.** A `kezi_mt_or`, a `VersmegfKeziMt` és a `kezi_mt_or_kihagy` nincs a kódban (`grep` 0 találat); az `Integracio` és a `FeliratHalmaz` teszt fut és zöld.
- **E4.** A `Karoli_versmegfeleltetes.tsv`, a `_javitas.tsv` és minden más `adat/`, `konkordancia/` TSV bájtra változatlan; kivétel csak a `BSB_Strongs.tsv` (és a `naplok/F41_wlc_versszam_ellenorzes.tsv`, ha a 3.5 újragenerálja), és csak felhasználói jóváhagyással (E6-módszer: `git ls-tree` sha256, mint a `naplok/F117_meres.md` 3. pontjában).
- **E5.** A Zsoltárok BSB-importja (F16) és a Zsolt 13 kézi kivétele (F71) bájtra azonos.
- **E6.** A `pardes.db` a repón kívül felépül hiba nélkül; az építés naplója és a 3.5 SQL-ellenőrzése a `naplok/F120_meres.md`-ben, proveniencia-sorral.
- **E7.** Minden számállítás mellett proveniencia-sor; ahol kódolvasás az alap, ott `scope=manual`.

## 5. Döntésnapló

- **DT-F120a** (3.2 ⛔): a `BSB_Strongs.tsv` `Igehely`-kulcsának szemantikája az F85.6 Károli-kulcsú TAHOT-ja után: (a) MT marad, (b) Károli, (c) nincs újragenerálás. *Nyitott.*
- A 3.3-ban, ha a `fejezet_eltolasok()` szignatúrája változik: egyeztetett eltérés a `bsb_verseltolas_diag.py`-ra (nincs az `ir`-ben). *Feltételes.*

## 6. A fogyasztói újragenerálás (N-F117a, 2. rész) — külön tétel, javaslat

E brief lezárása után külön brief (várható `F<nn>_VERSMEGF_FOGYASZTOK_BRIEF.md`, `fugg: [117, 120]`, `munka: adat`, modell: sonnet a futtatáshoz, opus az eltérések ítéletéhez) újrafuttatja a javított táblát olvasó, adatot író fogyasztókat. Mindegyik eltérése a 346 A–D′ vershez kötendő, és a kimenet csak jóváhagyással cserélődik:
- Macula `karoli` oszlop (`f17/macula_futtat.py`, `macula_kozos.py`);
- `LXX_OS` (`lxx_os_import.py`; az N-F54a nyitott LXX-oldala: a Péld 12, Jób 17, 2Móz 36 `szamozas_elteres`);
- `karoli_strong` (`elopar_kjv.py`, `tokenek.py`);
- `olvaso_szerver/bdb_vers_jelentes.py`, `olvaso_pilot/bdb_szelet_m0.py`;
- a TSK-ra épülő lexikonoldalak (#36/#10, generált réteg);
- a többi (`nave_*`, `tahot_verskulcs_*`, `f08/*` stb.): előbb mérés, hogy ír-e kanonikus kimenetet.

A sorrend a függésből adódik: a `pardes.db` (#101) a `BSB_Strongs.tsv` és a Macula után épül újra.
