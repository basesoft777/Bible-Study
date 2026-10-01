# ELLENOR_F24 — F24_LICENC_BRIEF.md · origin/main..72d5390

*A `fuggetlen-ellenor` 1. köri jelentése. Az ellenőrnek nincs fájlíró eszköze, ezért az orkesztrátor mentette; a tartalom az ellenőr tételei, tömörítve (a parancsok és a fájl:sor hivatkozások megmaradtak). Eredmény: **ELTÉRÉS, 14 tétel**. A javítás és a 2. kör alább.*

Alap: 5 commit (F24.0–F24.3), fájlok: `DONTESEK.md` +1, `F24_LICENC_BRIEF.md` 2/1, `adat/SEMA.md` +56, `adat/licencek.tsv` +43. A `lexikon/`, `generalt_proba/`, `eszkozok/`, `konkordancia/`, `FELADATOK.md`, `NYITOTT_FELADATOK.md` és a többi `adat/*.tsv` nulla-diff; `.py` nem változott (csv-tilalom nem sérülhetett).

## Igazolt (OK)

- 39 dataset, 39 egyedi kulcs, mind 9 mező; 23 `tisztazott`, 16 `tisztazatlan` (egyezik a DT-F24 (1) listájával).
- K1 a `datasetek.tsv` ellen: 21/21 dataset megvan a táblában. A szerepmátrix forrásai lefedve (a BDB-etimológia csak közvetve).
- K2: mind a 23 `tisztazott` sorban van `forras_hely`.
- Mind a 7 `share_alike=igen` sor megjegyzése rögzíti a share-alike következményt.
- K3: a SEMA 2.19 kész, a DT-F24 🟡 nyitott; a TSV-séma egyezik a SEMA 2.19-cel; D41 (adatkészlet-szint, leltár, nem jogi vélemény) rendben.
- F30 helyőrző-szabály: az azonosító `DT-F24`, új végleges DT/N-szám nincs. Az N9 nyitott marad.
- A `lexikon_general.py` LICENC-konstansából 14 kulcs szerepel a táblában; a 7 felsorolt eltérés egyezik a `tisztazatlan` állapotokkal.
- E2–E8, E10–E16: 0 találat; E9: 2 JELENTES (`adat/SEMA.md:236–237`), mindkettő a main-en is ott volt, a diff nem érinti.

## ELTÉRÉSEK (súlyossági sorrendben)

1. **Kitöltött hiány (munkaszabály 1, SEMA 2.19 indoklása).** Öt `tisztazatlan` sorban határozott `kereskedelmi=igen` áll (BDB, LSJ, TSK, Thayer, Konyv_nevtablak: `adat/licencek.tsv:5,10,20,21,22,39`), négyben `share_alike=nem` (BDB, TSK, Thayer, Konyv_nevtablak), a Nave-nél is `share_alike=nem`, licencfájl nélkül. A SECE_G/H ugyanilyen másodkézből származó „közkincs” állítás mellett `tisztazatlan/tisztazatlan`-t kapott: következetlen.
2. **DT-F24 hiányos (brief 3.5).** A 6 `tisztazott` + `javaslat` sort (Karoli_KH, TAGNT, TAHOT, Macula_heber, Macula_gorog, KJV_Strongs_teljes: `licencek.tsv:8,17,18,24,25,37`) a tétel nem sorolja fel.
3. **Származtatott sor állapota.** A Karoli_Strong_kivonat `tisztazott` (`:9`), de a saját licence „projekt-adat + …”, a `projekt_adat` sor (`:43`) pedig `tisztazatlan`.
4. **K1 a `konkordancia/` ellen sérül.** A `BDB_etimologia_kezi_hatarok.tsv` (szerepmátrix heber 8) és a `Strongs bővítés` fájl egyik sorban sincs megnevezve; a „K1 eltérés 0” csak a `datasetek.tsv`-re igaz. A számszerű igazolást adó zárójelentés még nincs.
5. **`kotelezo_megjeloles`.** Macula (`:24–25`): a forrás szó szerinti szövege teljes a `naplok/F06_licenc_szovegek/macula_hebrew__LICENSE.md.txt:40`-ben, a tábla csonkolt. TBESH/TBESG (`:26–27`): a repó saját attribúciója áll, a SEMA szerint üres kellene (a TAHOT/TAGNT üres: következetlen). LXX_OS (`:29`): hiányzik a GreekResources („credit the Open Scriptures Septuagint Project”).
6. **STEPBible „4.0” verzió** (`:17–19,26–27`) a repó állítása, a forrás szövege csak „CC BY”-t mond; a BDB ugyanezen az alapon `tisztazatlan`.
7. **Kisebb:** SDBH/SDGNT/UBS `forras_hely` sortartománya (`:12,13,32,33,34`; a szó szerinti ©-mondat a `SDBH_SDGNT_README.md` 30. és 32. sora); OSHL commit hiányzik (`:28`, a README 6. sora rögzíti: `21c9add…`); SECE_H (`:15`) megjegyzésében nincs `javaslat` (a `lexikon_general.py:72` `'SECE_H': 'közkincs'`), a 8., 24., 25. sor nem `javaslat:` kezdetű; `adat/SEMA.md:11` „A nyolc tábla” (a lista 9 soros); `adat/SEMA.md:850` literális tabulátor a `\t` helyett; a `licencek.tsv:12` „(N11)” kétértelmű (a `NYITOTT_FELADATOK.md` N11 más; ez a terv N11-e).

Nem ellenőrizhető: E17 (új tábla, a küszöb DT3-ban nyitott); a végrehajtó CI-jelentésével való egyezés.

---

## 2. kör — origin/main..17ae98f (a javítás: 72d5390..17ae98f)

*Az ellenőr 2. köri jelentése, az orkesztrátor mentette, tömörítve. Eredmény: **ELTÉRÉS, 13 tétel**. Az 1. kör 14 tételéből a (1) öt sora, a K1 `BDB_etimologia`/`Strongs bővítés`, a Macula_heber megjelölés, a SEMA:11/:850, az SDBH ©-sorok, az OSHL-commit és az N11 javítva (OK). Igazolt: 39 sor, 22 `tisztazott` / 17 `tisztazatlan`; a 9 `tisztazott`+`javaslat` sor egyezik a DT-F24 listájával; nulla-diff a `eszkozok/`, `konkordancia/`, `lexikon/`, `FELADATOK.md` útvonalakon; E2–E8, E10–E16 és E12–E15: 0 találat (E9: 2 régi JELENTES, `SEMA.md:236–237`).*

Súlyossági sorrendben:

1. **TBESH `kereskedelmi=igen` + `tisztazott` (`licencek.tsv:26`), pedig a forrás (`konkordancia/TBESH.txt:6`) kimondja: „Permission should be gained from Online Bible before these definitions are applied in any project.”** Kitöltött hiány (munkaszabály 1); a záradékot a repó egyetlen dokumentuma sem rögzíti; a brief 3.2 szerint a `lexikon_general.py:63` besorolástól való eltérés `javaslat`-ot kérne.
2. **A „TBESH/TBESG 4.0 verzió nem igazolt” állítás hamis** (`licencek.tsv:26–27`, DT-F24 zárójele): a `TBESH.txt:10` és a `TBESG.txt:12` kimondja „(CC BY 4.0)”. (Az 1. kör 6. pontja e két sorra téves volt.) `forras_hely`: TBESH.txt 10–20., TBESG.txt 12–22. sor; `licenc`: CC BY 4.0.
3. **STEPBible „Please do not redistribute it yourself”** (`TBESH.txt:17`, `TBESG.txt:19`; valószínűleg a TAHOT/TAGNT/TIPNR is) nincs a táblában; SEMA 2.19 szerint `feltetelesen` vagy legalább `javaslat:`.
4. **Karoli_Strong_kivonat** (`:9`): `allapot=tisztazatlan`, de `kereskedelmi=igen`, `share_alike=nem`; a `naplok/F24_zaras.md:7` állítása („minden tisztazatlan sorban tisztazatlan/tisztazatlan”) hamis (16, nem 17); a „ts a fájl fejlécében” sem igaz; a `kotelezo_megjeloles` nem szó szerinti.
5. **Macula_gorog `tisztazott`** (`:25`), de a sor maga írja, hogy a görög LICENSE-szöveg nincs a repóban; a hivatkozott hely (`F17_import_naplo.md:16`) összefoglaló, nem idézet → SEMA 2.19 2. szabálya szerint nem `tisztazott`.
6. DT-F24 (1) 2. opciója 17 tisztázatlanból ötöt nem sorol be (Karoli_Strong_kivonat, Girdlestone, Versifikacios_tablak, LSJ, projekt_adat).
7. DT-F24: „a (4) pont szerinti LICENSE-idézés” téves kereszthivatkozás (a (4) az N9; az (1) pont ajánlás-oszlopa a helyes).
8. LXX_OS és Strong_szotar `kotelezo_megjeloles` (`:16,29`): a GreekResources-mondat a `Strong_szotar_README.md:66–68`-ból való, a `forras_hely` nem erre mutat; a héber „Open Scriptures, CC BY 4.0” a repó megfogalmazása.
9. Kisebb: SECE_H a `lexikon_general.py` 73. sora (nem 72.); a DT-F24 az LSJ-t „CC BY-SA 4.0”-ként csoportosítja, a tábla 3.0-t ír; `:25` megjegyzése nem `javaslat:` kezdetű mondat.

K4: nem TISZTA; a commitolt `ELLENOR_F24.md` 1. sora nem „TISZTA / ELTÉRÉS: n tétel” alakú. Nem ellenőrizhető: a `konkordancia/` 153 bejegyzésének alkönyvtáras bontása az ellenőr eszközeivel; E17; a végrehajtó CI-jelentése.

---

## 3. kör — origin/main...f0034f5 (a javítás: 17ae98f..f0034f5)

*Az ellenőr 3. köri jelentése, az orkesztrátor mentette, tömörítve. Eredmény: **ELTÉRÉS, 8 tétel**. Módszertani megjegyzés: az ellenőrzés közben a közös munkafa HEAD-je egy párhuzamos session (`/befogad`) miatt másik ágra váltott; az ellenőr a táblát `git diff`-ből igazolta, a CI-futás ezért nem a head-állapoton ment. Az F24 azóta külön worktree-ben (`../wt-f24-licenc`) folytatódik.*

Igazolt (OK): TBESH `feltetelesen` és az Online Bible-záradék szó szerint (`TBESH.txt:6`); TBESH/TBESG CC BY 4.0 és `forras_hely` (10–20., 12–22.); a „do not redistribute” idézése TBESH/TBESG-nél; Karoli_Strong_kivonat `tisztazatlan/tisztazatlan`; a számok (39 sor, 21 `tisztazott`, 18 `tisztazatlan` mind `tisztazatlan/tisztazatlan`, 8 `tisztazott`+`javaslat`) egyeznek a táblával és a DT-F24-gyel; a DT-F24 kereszthivatkozásai; SECE_H a 73. sor; SEMA↔TSV séma; N9-javaslat↔kódkonstans; K2, K3; nulla-diff a `eszkozok/`, `konkordancia/`, `lexikon/`, `FELADATOK.md` útvonalakon; törölt adatsor nincs.

1. **TAGNT/TAHOT/TIPNR `kereskedelmi=feltetelesen` következtetésből kitöltve** (`licencek.tsv:17–19`): a nyers fájlok nincsenek a repóban (csak kivonatok), a sor maga is „nem ellenőrizhető”-t ír → helyesen `tisztazatlan`. A DT-F24 (`DONTESEK.md:23`) és a `F24_zaras.md:8` a terjesztési kérést jelöletlen tényként közli (munkaszabály 1, A1). (A fejléc 13. sora egyébként a felhasználást engedi; a „do not redistribute” terjesztési kérés, nem kereskedelmi feltétel.)
2. **TBESH/TBESG** (`:26–27`): a forrás ad megjelölés-mondatot (`TBESH.txt:10`, `TBESG.txt:12`: „Data created by www.STEPBible.org …”), utalási kérést (`:17`/`:19`) és változtatás-jelzést ír elő (`TBESH.txt:16`, `TBESG.txt:18`: „include a note of changes”); a tábla szerint a forrás „nem ad” megjelölést, a mező üres, a `:26` megjegyzése pedig a „README 175. sorából” kezdődik: belső ellentmondás.
3. **`F24_zaras.md:9` és `SEMA.md:871–872`**: az LSJ-t `share_alike=igen` sorként kezeli, a táblában `tisztazatlan/tisztazatlan` (`:10`); a `share_alike=igen` sorok száma 6, nem 7.
4. **Strong_szotar** (`:16`): a repónak tulajdonított „Open Scriptures, CC BY 4.0” idézet sehol nincs a repóban (Grep: 0 találat); a `kotelezo_megjeloles` nem szó szerinti, és hibás forrásfájlt (GreekWordList.js) nevez meg (az idézet a `Strong_szotar_README.md:66–68`-ból való).
5. **Karoli_Strong_kivonat** (`:9`): a „a fájlnak nincs fejlécsora” hamis (`konkordancia/Karoli_Strong_kivonat.tsv:1` oszlopfejléc); csak `#`-proveniencia-sor nincs.
6. **Macula_gorog** (`:25`): a `licenc` mezőből hiányzik a zárójeles „nem igazolt” jelölés; a `forras_hely` „3. pont” eltér a hivatkozott napló „3. sor”-ától (a „3. pont” az F17:25 szerint az UBS-kivétel).
7. **DT-F24**: a Konyv_nevtablak a „közkincs-eredetűek” között szerepel, holott CC BY 4.0 + projekt-adat (`licencek.tsv:39`).
8. Három nem `javaslat:` kezdetű javaslat-mondat maradt (`licencek.tsv:18,25,37`).

K4: nem TISZTA. Nem ellenőrizhető: a CI a head-állapoton; a 153 bejegyzés alkönyvtáras bontása; E17.

---

## 4. kör — origin/main...3d01801 (a javítás: f0034f5..3d01801)

*Az ellenőr 4. köri jelentése, az orkesztrátor mentette, tömörítve. Eredmény: **ELTÉRÉS, 11 tétel**. Igazolt (OK): TAGNT/TAHOT/TIPNR `kereskedelmi=tisztazatlan`; TBESH/TBESG `kotelezo_megjeloles` szó szerint; LSJ és a 6 `share_alike=igen` sor; Strong_szotar megjelölés; Karoli_Strong_kivonat; DT-F24 besorolás (18 tisztázatlan, 8 `tisztazott`+`javaslat`); a számok (39; 21/18; 6; 8; 4 `feltetelesen`) egyeznek a tábla, a DT-F24, a SEMA 2.19 és a `F24_zaras.md` között; K2, K3; séma; E2–E8, E10–E16 és E12–E15: 0 találat a merge-base alapon (E9: 2 régi JELENTES); törölt adatsor nincs; `eszkozok/`, `konkordancia/`, `lexikon/`, `FELADATOK.md` nulla-diff (háromponttal).*

1. **TAGNT/TAHOT/TIPNR `allapot=tisztazott` + `kereskedelmi=tisztazatlan`** (`licencek.tsv:17–19`): a sor maga írja, hogy a feltételek és a verzió nem ellenőrizhetők; a Macula_gorog ugyanezen az alapon `tisztazatlan`; az N9-javaslat szerint a `TISZTAZATLAN_SZOTARAK` az `allapot`-ból képződne → következetlen. Vagy `tisztazatlan` az állapot, vagy a SEMA 2.19 mondja ki a kombináció jelentését.
2. **Származtatott sorok** (`:30` LXX_versszintu_parok, `:31` Karoli_versmegfeleltetes): `tisztazott`/`kereskedelmi=igen`, pedig TAHOT- és projekt-adat komponensük van (`LXX_versszintu_parok.tsv:1–4`, `konkordancia/README.md:245–250`, `Karoli_versmegfeleltetes.tsv:2`); a Karoli_Strong_kivonat ugyanezzel az indokkal `tisztazatlan`. A `:30` `verzio_vagy_commit` a verse_pairs sha-ját adja, a generátor az `LXX_OS/*.tsv`-t olvassa.
3. **Nyilvános terjesztés** (`:11,35`; `naplok/F18_licenc.md:15`; `LXX_kivonat_README.md:51–52`): a repó nyilvános, az LXX_kivonat README-je szerint „kizárólag belső”, az MCGED „All Rights Reserved”, és az `MCGED_teljes.tsv`, a `lexikonok_nyers/MCGED.lexicon` a repóban van; a tábla és a DT-F24 csak a jövőbeli „nyilvános nézetből kimarad” kérdést teszi fel, a mostani terjesztést nem rögzíti.
4. **Az ág le van maradva az origin/main-től** (8e9540a, b98c4ae): a kétpontos diff az F32 brief hamis törlését mutatja, E5 HIBA: 10 (a merge-base alappal 0). Merge előtt rebase kell.
5. **LXX_OS** (`:29`, örökölten `:30–31`): a `forras_hely` a README összefoglalójára mutat („CC BY 4.0”), nem szó szerinti idézetre → SEMA 2.19 2. szabálya szerint nem `tisztazott`; a `kotelezo_megjeloles` szó szerintisége nem ellenőrizhető.
6. **K1:** a HEAD-en 152 bejegyzés van, nem 153 (a `konkordancia/_nyers/` nincs követve; a Cremer_nyers sora ezt nem mondja ki); a 133/20 bontás nem reprodukálható az ellenőr eszközeivel.
7. **Macula_gorog** (`:25`): a megjegyzésben maradt „3. pontját” (a 3. pont az UBS-kivétel; a licencsor a 3. sor); a `javaslat:` mondat közben áll.
8. **`javaslat:` előtag hiányzik** (`licencek.tsv:6,14,25,42`).
9. **DT-F24 (2):** az SA-források közül az `SDBH_SDGNT_segedtablak` (`:34`, `share_alike=igen`) kimaradt (5 van felsorolva, 6 kellene).
10. **SEMA 2.19 N9 eltérés-lista:** a `projekt-adat` kulcs (`projekt_adat`, `tisztazatlan`) kimaradt.
11. **LSJ megjegyzése** (`:10`) feltétel nélküli tényként állítja a SHARE-ALIKE-ot, miközben `share_alike=tisztazatlan` (A1, kis súly).

K4: nem TISZTA. Nem ellenőrizhető: a végrehajtó CI-jelentése; E17; a zárás (`allapot: fut`, a `F24_zaras.md` tervezet).
