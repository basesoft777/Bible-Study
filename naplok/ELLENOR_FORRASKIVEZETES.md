# ELLENŐR — F42_FORRASKIVEZETES_BRIEF.md · `origin/main...HEAD` (3dda1ea..71ea153, F42.0–F42.15)

*A `fuggetlen-ellenor` ügynök jelentése (a szövege: az ügynök hand-back üzenete; a Write eszköz hiánya miatt a végrehajtó mentette fájlba, tartalmi változtatás nélkül, majd a „Javítás” szakaszt fűzte hozzá). Eredmény: **ELTÉRÉS: 6 tétel**.*

**Módszer és korlátok.** Csak `git diff`/`git log`, `lekerdez.py`, `futtat.py`, Read/Grep/Glob; a `git ls-files` helyett üres fával összevetett diff. **Nem futott:** `curl`, `general.py`, `torzscikk_general.py`, `teszt_lekerdez_sir.py`, `lxx_bridge_egyezes.py`, `forras_letolt.py`; ezért K2, K9 és a K8 bájtszintű része NEM ELLENŐRIZHETŐ.

| pont | eredmény | indok |
|---|---|---|
| K1 (DT-F42e szerint szűkítve) | OK | nincs `TBESH.lexicon`, `TBESH_konszolidalt.tsv`, `LXX_kivonat`; a `TBESH.txt` marad; `.gitignore:16` lefedi a `_nyers/`-t |
| K2 | NEM ELLENŐRIZHETŐ | friss klón/letöltő futtatása a szerepkörön kívül; a sha256 egyezik a `licencek.tsv`-sel |
| K3 | ELTÉRÉS (alacsony) | (1) a `.lexicon` hibaüzenete a sha256 helyéül rossz fájlt jelölt; (2) a hiányzó BDB-re a `cremer_ocr_javit` a letöltőre mutatott, pedig az a BDB-t nem állítja vissza |
| K4 | NEM ELLENŐRIZHETŐ | a CI dolga |
| K5 | OK | 23 `forrasfajl`, 4 útvonal, mind követett |
| K6 | ELTÉRÉS (alacsony) | `konkordancia/TBESH_TBESG_README.md:50` Online Bible-eredetű H7121-részletet idézett |
| K7 | OK | nincs licenc-konstans; hiányzó sor/üres `cimke` `SystemExit`; mind a 44 sorban van `cimke` |
| K8 | ELTÉRÉS (közepes) | `lexikon/ISTENTISZT-001_TORZSCIKK.md:1091` „CC BY-SA 3.0”, a lexikonoldal 4.0; az M5_M7 „törzscikkek 0 eltérés” állítása ezt nem fedi le; az ISTENTISZT-001 lexikonoldal diffje 63 sor, a 20/11/32 bontással egyezik |
| K9 | NEM ELLENŐRIZHETŐ | a `curl` nem futtatható; a sor `tisztazatlan`, a conf sha256-tal és dátummal idézett |
| K10 | OK (feltételesen) | `futtat.py` pull_request módban és a commit-üzenetekkel: HIBA 0 (a `TÖRLÉS-SZÁNDÉKOS:` jelölés a F42.13 üzenetben); a „független ellenőr eltérés nélkül zár” feltétel nem teljesült |
| 3. pont (CI-jelentés) | NEM ELLENŐRIZHETŐ | saját futtatás: E2–E8, E10, E14–E16, E19: 0; E9 JELENTÉS 2; E11 JELENTÉS 1 (a felhasználó tudomásul vette); E12 JELENTÉS 173; E13 JELENTÉS 52 |
| D1–D8, DT-F42a, c, d, g, j | OK | részletek: D3/DT-F42j: a `08d88dc` és `55c407a` a main őse, a blobok azonosak; D7: az M5 a #43 merge-e után futott |
| DT-F42h (`ir` bővítése) | ELTÉRÉS (alacsony) | a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` nem szerepel az `ir`-ben; a `kovetkezo` elavult |
| M5 f1/f2/f3, bridge | OK | `lxx-hid`: Ezsd 1:1 n=35, Neh 4:1 n=23, Neh 9:38 n=18, Eszt 2:5 n=22; explicit üres: Neh 3:7, 11:16, 12:5, Eszt 1:1, 4:6, 9:30; Józs 1:1 (Vaticanus) n=16; eltéréslista-összegek egyeznek; a bridge 86 sorában csak a `lefedettseg` változott |
| Táblaírások | OK | licencek: 44 sor + `cimke`, tartalmi változás 4 sorban (LXX_kivonat, TBESH, KJV_Strongs_teljes, lexikonok_nyers); datasetek/forditasok/lexikon_hivatkozasok csak a szándékolt sorok |
| A1 | OK, egy pontja NEM ELLENŐRIZHETŐ | hogy a Rahlfs-szöveg maga nem tartalmaz egy-egy Eszt/Neh verset, lekérdezéssel nem dönthető el (az LXX_OS-ben nincs sor) |
| A2 | OK | N9, N17 lezárva, az auditsorok helye igazolva |
| A3–A5 | OK (nem érintett) | |
| A6 | OK, megjegyzéssel | a generált oldalon E12 173 / E13 52; 3 új E13: az adatfelzárkózás átírás nélküli héber/görög fordítássorokat hozott |
| CLAUDE 1. szabály | ELTÉRÉS (alacsony) | „ellenőrizve” proveniencia-sor nélkül (`TBESH_TBESG_README.md:103`); N17-nél és az LXX_OS README darabszámainál hiányzik a proveniencia-sor |
| CLAUDE 2–3. szabály | OK | |
| Ellenőrzőlista 3 (nulla-diff hatóköre) | ELTÉRÉS | lásd K8 |
| Ellenőrzőlista 4 / DT3 | ELTÉRÉS (közepes) | a ≥10 soros táblaváltozásokhoz (−469 932 és −9 838 adatsor) nem volt táblánkénti, darabszámos bontás |

**Az ELTÉRÉS-ek súlyossági sorrendben:** (1) K8 törzscikk-elavulás; (2) DT3 bontási napló hiánya; (3) K6 a README 50. sorában; (4) proveniencia („ellenőrizve”); (5) K3 hibaüzenetek; (6) a brief fejléce (`ir`, `kovetkezo`).

**Ismert, szándékos eltérések:** HODIT-001 élő oldala nem renderelt; E11 JELENTÉS; az ISTENTISZT-001 adatfelzárkózása jóváhagyott; az LSJ „CC BY-SA 3.0” a kézi forrásban.

**Megfigyelések:** `f4_0c_korut_ellenoriz.py:52` a törölt fetch szkriptre hivatkozik (a `Betu_utotag_kizarva.tsv`-nek nincs író szkriptje); a `datasetek.tsv` `LXX_OS/*.tsv` globja a 2 segédtáblát is lefedi; a `tbesh_konszolidalt_import.py:23` docstringje a régi útvonalat írta; az `istentiszt_2b_d1_toltes.py:146-154` még tartalmazza a TBESH H7121 kinyerését (hangos hibával állna meg); az `lxx_os_import.py --ujrabesorol` írás előtt nem veti össze a sorokat (csak a 3. és 4. oszlopot írja).

## Javítás (végrehajtó, F42.16)
- **K8:** a törzscikkek renderelése a mai adathoz képest minden oldalon 65–326 sorban elavult, nem csak az ISTENTISZT-001-é: felzárkóztatásuk a #36 dolga, a #42-ben nem végezhető el nem várt tömeges diff nélkül. Az M5_M7 jelentés pontosítva (a „0 eltérés” a main- és az ág-állapot összevetése; az elavulás külön rögzítve), a záró jelentés nyitott tétele.
- **DT3:** a táblák sorszám-változása adatsorokra bontva az M5_M7 jelentésben.
- **K6:** a `TBESH_TBESG_README.md:50` idézete kikerült. **Proveniencia:** a README „ellenőrizve” sora `manual` jelöléssel pontosítva.
- **K3:** az `utvonalak.py` üzenete a `TBESH_TBESG_README.md`-re mutat; a hiányzó BDB-re a `cremer_ocr_javit` a `git checkout`-ot ajánlja. A `tbesh_konszolidalt_import.py` docstringje frissítve.
- **A brief `ir`-je:** a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` felvételét a `feladatok.py` E18 szabálya (motívum-ID-s `ir` → `olvas`-ban kötelező `tematikus_lezart/ISTENTISZT-001_tematikus.md`, ami nem létezik) hibának minősíti; ezért nem szerepel az `ir`-ben (egyeztetett, dokumentált eltérés). A `kovetkezo` a zárással frissül.
- **Nem javítva:** a `istentiszt_2b_d1_toltes.py` (egyszer futtatott, történeti töltő); az `f4_0c` megjegyzés; az A6 új E13-jelentések (jóváhagyott felzárkózás következménye); N17-hez és az LXX_OS README darabszámaihoz külön proveniencia-sor nem készült (a mérés `manual`, az `eszkozok/lxx_osszevetes.py` kimenetének fejlécében rögzítve).
