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
