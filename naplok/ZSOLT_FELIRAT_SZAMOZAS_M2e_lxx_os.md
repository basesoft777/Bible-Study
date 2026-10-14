# ZSOLT_FELIRAT_SZAMOZAS_M2e_lxx_os.md — az LXX_OS újragenerálása az új A-táblával (F91 E1, CSAK MÉRÉS)

*Végrehajtó: claude-sonnet-5-5. Mért adat. Az `eszkozok/lxx_os_import.py` és a `konkordancia/LXX_OS/` fájljai nem módosultak (`git status`: tiszta); a mérés memóriában fut: `python eszkozok/f91_lxx_os_replay.py` (a táblázat a 3. szakaszban és a szkript kimenetében azonos).*

Proveniencia: `scope=LEFEDETTSEG_KONYVEK (14 könyv, elsődleges LXX_OS-fájlok), gap-fill lépés | forras=konkordancia/LXX_OS/*.tsv + eszkozok/lxx_os_import.py lefedettseg_javit_konyv() | ts=2026-10-14` · `scope=A-tábla, régi = 25e39a1a (az ág merge-base-e), új = HEAD | forras=konkordancia/Karoli_versmegfeleltetes.tsv | ts=2026-10-14` · `scope=Zsolt, felirat-halmaz | forras=eszkozok/zsolt_felirat_halmaz.py | ts=2026-10-14`

## 1. Hatókör és módszer — és ami NEM készült el

**A teljes újragenerálás (`lxx_os_import.py --letolt`) nem futott le.** A szkript forrásai (az `lxx-morph`, a `GreekWordList` és a `verse_pairs.jsonl`) nincsenek a gépen (a `konkordancia/_nyers/` nem tartalmazza; a `D:` meghajtón és a Bible-Study-másolatokban sem találhatók), a `--letolt` pedig a rögzített GitHub-commitokról töltene le; ehhez a felhasználó külön, kifejezett engedélye kell, ezért nem indítottam el.

Ehelyett a szkript egyetlen A-tábla-függő lépését futtattam újra, offline, a szkript saját függvényével:

- Az A-tábla a szkriptben **két** helyen olvasódik: a `_tabla_kjv()` (`lxx_os_import.py:464–477`), amelyet a `lefedettseg_javit_konyv()` használ (`:573` `tk = tabla.get(ig)`; a felirat-szabály `:584–593`), és a `load_kjv_karoli_index()` (`:340–358`), amely csak Ezsd/Neh/Eszt sorokat indexel. Az F91 az A-táblán csak `Zsolt` sorokat és egy jegyzetsort módosított (az ellenőr szerint a nem `Zsolt` sorok bájtra azonosak), tehát az Ezsd/Neh/Eszt-függés nem érintett. Az alap-lépés (`process_book` / `resolve_karoli`) nem olvassa az A-táblát, és a térképet sem (a `LXX_versificacios_terkep.tsv`-re csak megjegyzések hivatkoznak), tehát a térkép F91.12-es oszlop-átnevezése az importert nem törte.
- A mérés: a commitolt `psalms-lxx.tsv`-ben (és a másik 13 elsődleges fájlban) a gap-fill-eredetű sorokat (`karoli_ok` ∈ `zsolt_felirat_eltolas`, `versmegfeleltetes_tabla`, `sorrend_beagyazas`) kulcs nélkülire állítottam (a gap-fill előtti állapot), majd lefuttattam a `lefedettseg_javit_konyv()`-et (a) a **régi** A-táblával (`25e39a1a`), (b) az **új** A-táblával (HEAD). A szkript saját K5-invariánsa szerint csak az `igehely_karoli` és a `karoli_ok` oszlop változhat.
- Korlát: ha a base-lépés (a letöltött forrásokból) valamely felirat-versre maga adna `zsolt_felirat_eltolas` jelölést (`:1071`), a mérés ezt nem látná. A commitolt fájlban a 66 jelölt vers pontosan a felirat-halmaz Zsolt 13:1 nélküli része, tehát a base-lépés a zsoltárokon ilyet nem adott; ez következtetés a commitolt adatból, nem futtatás.

## 2. Reprodukálja-e a régi A-tábla a commitolt LXX_OS-t?

**Igen.** A régi A-táblával a 14 könyv mindegyikén **0** eltérő vers, **0** eltérő token. (Gap-fill-eredetű token-sorok a 14 könyvben: Zsolt 699, Józs 649, 1Sám 893, Jób 431, Péld 245, Én 529, Ézs 524, Jer 1 029, Hós 219, Jón 31, 4Móz 21, 2Móz/1Kir/Dán 0.) A mérés tehát a commitolt állapotot a régi táblával pontosan visszaadja; az eltérés kizárólag az új A-tábla hatása.

## 3. Az új A-tábla hatása (E1 mért számai)

A 14 könyvből **csak a `psalms-lxx.tsv`** (34 951 token-sor) változik; a másik 13 fájlban 0 sor.

| mérés | érték |
|---|---|
| eltérő vers | **66** (62 zsoltár: 58 × 1 + Zsolt 51, 52, 54, 60 × 2) |
| eltérő token-sor | **671** |
| eltérő mező | `karoli_ok`: 671 token-sor; `igehely_karoli`: 29 token-sor; a többi mező (az `igehely_kjv` is) 0 |
| a `zsolt_felirat_eltolas` jelölés | **elveszik: 66 vers, 671 token → 0** (a commitoltban 66 vers / 671 token viseli) |
| 64 vers (642 token) | `zsolt_felirat_eltolas` → `sorrend_beagyazas`; a Károli-kulcs változatlan |
| 2 vers (29 token) | a Károli-kulcs is elvész, `karoli_ok` üres: `Psalms (LXX) 29:1` (→ Zsolt 30:1, 11 token), `Psalms (LXX) 64:1` (→ Zsolt 65:1, 18 token) |
| Zsolt 13:1 | változatlan (`Psalms (LXX) 12:1`, `igehely_kjv=13:1`, `karoli_ok` üres): a jelölés sosem tartalmazta |

**Az etalon (`igehely_kjv`) maga nem változik.** A Károli→KJV párosítás (az `igehely_karoli` ↔ `igehely_kjv` etalon-térkép) pontosan két Károli-versen változik: Zsolt 30:1 és Zsolt 65:1 (mindkettő felirat-vers, a javító számára v ≤ d, tehát irreleváns). Fixpont-próba: az `f91_versmegf_javit.py` az így regenerált etalonnal futtatva a **mostani A-táblát bájtra azonosan** adja (nincs oszcilláció).

Következmény a `pardes.db`-re (kódolvasásból, nem építve): a 64 vers `megjegyzes` oszlopa (`lxx_versszam`) `zsolt_felirat_eltolas` → `sorrend_beagyazas` lenne; a Zsolt 30:1 és 65:1 LXX_OS-sora `forras=nincs`-re változna. A builder és az f92 felirat-szűrése az F91.14 óta a közös halmazból dolgozik, tehát ettől függetlenül helyes marad.

## 4. A körkörös függés

`Karoli_versmegfeleltetes.tsv` (generált: KK4 + `f91_versmegf_javit.py`) ← az LXX_OS Károli-kulcsú etalonja; az LXX_OS (generált: `lxx_os_import.py`) ← az A-tábla (`_tabla_kjv`, gap-fill). Az F91 óta a felirat-versek KJV-értéke az A-táblában üres, ezért a gap-fill felirat-szabálya (a `cand` az A-tábla KJV-értékéből épül) nem talál jelöltet. A kör a mostani adaton fixpontban van (3. szakasz), de a felirat-jelölés az újragenerálásnál elvész.

## 5. Ellenpróba az (a) opcióra

Az (a) opció prototípusa (memóriában): a gap-fill-ben a felirat-halmaz versei (`zsolt_felirat_halmaz.felirat_versek()`) az A-tábla helyett a halmazból kapják a KJV-kulcsot (`Zsolt c:v` → `c:v`, ahogy a régi A-tábla identitása is volt), minden más vers marad `tabla.get(ig)`. Eredmény: a commitolt `psalms-lxx.tsv`-hez képest **0 eltérő token-sor, 0 vers** — a felirat-jelölés (66 vers / 671 token) és a két Károli-kulcs (Zsolt 30:1, 65:1) megmarad. A változtatás az `lxx_os_import.py`-ben a `tk` képzése (egy sor) és az import a közös modulból; ezt a döntésig nem hajtottam végre.

## 6. Megvalósítás és igazolás (F91.16; DT-F91d (a), a felhasználó döntése, 2026-10-14)

**Változás.** Az `eszkozok/lxx_os_import.py` `_tabla_kjv()` függvénye az A-tábla beolvasása után a közös felirat-halmaz (`zsolt_felirat_halmaz.felirat_versek()`, 67 vers) minden versére felülírja a KJV-kulcsot a Károli-kulcsból (`Zsolt c:v` -> `c:v`). A `lefedettseg_javit_konyv()` `tk = tabla.get(ig)` sora változatlan, ezért a `zsolt_felirat_eltolas` jelölés és a két Károli-kulcs (LXX 29:1 -> Zsolt 30:1, LXX 64:1 -> Zsolt 65:1) logikája érintetlen. A `konkordancia/LXX_OS/` fájljait nem írtam, a `--letolt` futást nem indítottam.

**Igazolás.** Az `eszkozok/f91_lxx_os_replay.py` most a módosított importer-függvényt hívja (nincs másolt logika, a prototípus-ág kikerült). Eredmény mind a 14 könyvre (2Móz, 4Móz, Józs, 1Sám, 1Kir, Jób, Zsolt, Péld, Én, Ézs, Jer, Dán, Hós, Jón): **régi A-tábla (25e39a1a): 0 eltérő vers / 0 token; új A-tábla: 0 eltérő vers / 0 token, 0 kulcsot vesztett vers**; `ELTERES-OSSZEG: 0`. Negatív kontroll: a módosítás nélküli importerrel az új A-tábla a Zsoltokon 66 vers / 671 token eltérést (2 kulcsot vesztett vers) ad, tehát a replay érzékeny a változásra. A `psalms-lxx.tsv` felirat-jelölése (66 vers / 671 token) és a két Károli-kulcs megmarad.

**Regressziós ellenőrzés (iii).** Futtatás: `python eszkozok/f91_lxx_os_replay.py [regi_revizio]` (alapértelmezett régi revízió: `25e39a1a`). Elvárt: minden könyvsor `0/0` mindkét A-táblával, az utolsó sor `ELTERES-OSSZEG: 0`, kilépési kód 0; bármely eltérésnél 1. Offline, nem ír a repóba.

**Határ (ii).** A kör csak a felirat-versekre szűnik meg. A NEM felirat verseken az LXX_OS az A-táblából (`_tabla_kjv`), az A-tábla az LXX_OS etalonjából dolgozik; a mostani adaton ez fixpont (3. szakasz), de az A-tábla és az LXX_OS közötti függés ott megmarad.

**NAVE-0130 (N-F91b).** A `_nave_vers` a `karoli_ok` jelölést használja; a felirat-halmazra átírva a `nave_vers` 156 214 sorából 1 sor tűnne el (NAVE-0130, `Zsolt 13:1-4`, `Zsolt 13:1`). Ezt az N-F91b-ben kell eldönteni; az F91 nem nyúl hozzá (a megjegyzés az `NYITOTT_FELADATOK.md` N-F91b tételében).
