# FORRASKIVEZETES — zárójelentés (#42)

Ág: `claude/forraskivezetes` · M0 jelentés: `naplok/FORRASKIVEZETES_M0.md` · M5/M7 jelentés és render-diff: `naplok/FORRASKIVEZETES_M5_M7.md` · döntések: DT-F42a–i (mind ✅).

1. **M1–M3:** `eszkozok/forras_letolt.py` (a `TBESH.txt` sha256-os helyreállítása a STEPBible-Data `b99716b`-ről, idempotens, CRLF-munkafánál is), `eszkozok/utvonalak.py`; a `TBESH.lexicon` és a `TBESH_konszolidalt.tsv` a gitignore-olt `konkordancia/_nyers/tbesh/` alatt él, hiányukra minden olvasó egyértelmű hibát ad (a `cremer_ocr_javit.py` csendes kihagyása megszűnt). 24 → 23 `forrasfajl`, 0 nem létező útvonal.
2. **M4:** az Online Bible-eredetű H7121-részlet kikerült a két tábla soraiból, a kézi forrásszakaszból és az ISTENTISZT-001 lexikonoldalról (BDB-alapú szakasz); a pilot-/próba-példányok és a `generalt_proba/` változatlanok.
3. **M5:** az `LXX_kivonat` kivezetve (39 fájl + README + a két fetch szkript törölve); az `lxx-hid`, a bridge-ellenőrzés, a generátor és a kockázat-szkript az `LXX_OS`-re állt; 2 Esdras → Ezsd/Neh és a görög Eszter → Eszt besorolva (Ezsd 280/280, Neh 392/406, Eszt 163/167 Károli-vers kulcsolva); elsődleges szövegváltozatok rögzítve; teljes eltéréslista: `naplok/FORRASKIVEZETES_M5_eltereslista.tsv` (a régi zsoltár-kivonat egy verssel eltolt volt: az átállás javítja, N17 lezárva).
4. **M6 (N9 lezárva):** a licenc-állapot és a rövid címke egyetlen forrása az `adat/licencek.tsv` (új `cimke` oszlop, SEMA 2.19); a `lexikon_general.py`-ban nincs licenc-konstans, hiányzó sor hiba. `KJV_Strongs_teljes` → `tisztazatlan` (a CrossWire `kjv.conf` szó szerint idézve: `DistributionLicense=GPL`); a TBESH-sor megjegyzése ellentmondás nélkül.
5. **M7:** törzscikkek 0 eltérés; ISTENTISZT-001 63 osztályozott sor, nem várt 0; a `futtat.py` (CI-ekvivalens) exit 0, E11 JELENTÉS (nem HIBA).

## Egyeztetett eltérés
- **`ir`-bővítés (DT-F42h):** `adat/datasetek.tsv`, `adat/forditasok.tsv`, README-k, `lxx_os_import.py`, `lxx_bridge_egyezes.py`, `naplok/KAROLI_KK*.py` (import) és más fájlok; `munka: ertelmezo` a fejlécben (motívumhoz tartozó forrásszöveget érint).
- **DT-F42e:** a `TBESH.txt` a repóban marad; a K1 ennek megfelelően szűkített.
- **M4 felzárkózás:** az ISTENTISZT-001 újrarenderelése a #42-től független adatváltozásokat is behozott (ts-ek, `forditasok.tsv` forrásnév, három fordítássor); a felhasználó jóváhagyta (2026-10-05).

## Nyitott tételek
- **HODIT-001** élő oldala nem renderelve (a #42 hatása: 5 Józs-sor; a #36 LEXIKON_UJRAGEN dolga); a többi 6 oldal a #42-től bájtazonos.
- A régi zsoltár-kivonatra épülő állítások (TEREMT-002 B4 auditsorok, két kereszthivatkozás-napló, pilot) újraellenőrzése: tartalmi döntés (lista: `naplok/FORRASKIVEZETES_M5_M7.md`).
- A forrásszövegek kézi licencsora (`Segitsegul_hivni_az_Urat_tematikus.md` stb.) LSJ-re még „CC BY-SA 3.0”-t ír, a generált rész már 4.0-t.
- A TBESH.lexicon forrása nem rögzíthető (Google Drive); a git-történetből állítható vissza.
- Git-történet: a TBESH.lexicon, a TBESH_konszolidalt.tsv és az LXX_kivonat a korábbi commitokban megmarad, a történet nem íródik át (DT-F42, rögzítve).
