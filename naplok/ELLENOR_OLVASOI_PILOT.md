ELTÉRÉS: 14 tétel

# Független ellenőrzés — F60_OLVASOI_PILOT_BRIEF.md (v3.3)

*Ellenőr: `fuggetlen-ellenor` (claude-opus-5-5), 2026-10-12. Az ellenőr ebben a futásban nem tudott fájlt írni; a jelentést szó szerint az orkesztrátor mentette ide. Az ellenőr a `teszt_olvaso_pilot.py`-t és a `feladatok.py ellenoriz`-t nem futtathatta (a szerepe szerint nem megengedett parancs).*

Tartomány: `86ad59263154b10dcda6fac19ffa40110aa99ef3..e0e32cecc64ac49d86146d35b0ca104252a02356` (46 commit, 21 fájl). Munkafa: `C:\Users\bases\Desktop\wt-olvasoi`.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | Tényleges modell `claude-opus-5-5`, kért `opus`: egyezik. A menet saját modell-mezői: `ertekeles.md:3` „Végrehajtó: claude-sonnet-5-5”. A `B..H` commitjainak Co-Authored-By trailerei: 41 Sonnet 5.5, 5 Opus 5.5 (F60.0d, F60.33, F60.34, F60.39, F60.40). Ez az 5 csak döntésrögzítés (brief, DONTESEK.md, beerkezo-brief, ertekeles 7. pont). Adattábla `modell`-mezője nem változott. |
| CI (3.) | ELTÉRÉS | `eszkozok/olvaso_pilot/README.md:0` | `futtat.py --valtozott … --diff-alap B --diff-fej H --esemeny pull_request` → exit=1. **E5 HIBA**: törölt címsor „TÖRLÉS-SZÁNDÉKOS:” jelölés nélkül (`## Ismert korlátok (2026-10-05)`). E2–E4, E6–E16, E19, E20, E26: 0 találat. E25: 3, E27: 33 JELENTES/FIGYELMEZTETES, a diffen kívüli fájlokra. A K4 „a CI zöld” feltétele nem teljesül. |
| K1 | ELTÉRÉS | `teszt_olvaso_pilot.py:33`, `:757`; `ertekeles.md:122` | A tesztek `SZAKASZOK = {'gen': '1Móz 1:1-2:3', 'zsolt': 'Zsolt 22'}` szakaszokon futnak, az **1Móz 1–25 nincs a tesztben**. A regresszió (`Regresszio.test_prototipussal_azonos`) `skipUnless(OLVASO_PROTOTIP_JSON)`; részhalmaz-összevetés az F60.4-állapottal (98b5098), maszkolt `morf_hu` mezővel, nem bájtra azonos. A bájtra azonos `TestRegresszioProto`-t a menet szándékosan nem vette át (ertekeles 5.3). Az M0/K1 „bájtra azonos, a ts kivételével” feltételét semmi nem igazolja. |
| K2 / v3.1 angol-pótlás | ELTÉRÉS | `adat.py:489-490`; `sablon.html:985`, `:1013` | A BDB angol szócikk teljes (`adat.py:231-247`). A görög lapon a TBESG `[:900]`, a Thayer `[:700]` + „…” vágással kerül a lapra; a blokk jellege csak `['forras']`, a kivágás nincs „gépi feldolgozás”-ként jelölve. Az ertekeles 4. pontja a vágást nem említi. Az állapotjelzés megvan (`sablon.html:946`, `:1116`, `:1173`). |
| M1 „csak adat” (sablon) | ELTÉRÉS | `sablon.html:1020` | A TBESH forrás-sora rögzített szöveg: „a jelentés-lista az Online Bible-eredetű: a licenc-kérdés nyitott”. Nem adatból jön, és ellentmond a `adat/licencek.tsv:29` TBESH sorának (`tisztazott`, DT-F33f) és a DT-F60a szövegének. A többi statikus szöveg (346, 717, 721, 979, 980, 1118) felületi utasítás vagy adatállapot-jelzés; az 1118-ast a felhasználó M3-döntése tartja meg. |
| M1 ellenőrzőlista | ELTÉRÉS | `naplok/OLVASOI_PILOT_ellenorzolista.md:60-61,64` | Utoljára az F60.9 módosította. A (c)2 és (c)3 pont a TAHOT-„nem teljes” és a Macula „kb. 78%” lábléc-szövegeket írja le, de ezeket az F60.29 kivette; a sablonban 0 találat. A lista elavult. |
| K3 | OK | `ertekeles.md:15-17,50-51,154,172,179,186,193,200` | Mindkét szakaszra van `scope=… \| forras=… \| ts=…` sor; a 8. pont külön tárgyalja a #25a feltételeit. |
| M2 mérőszámok frissessége | ELTÉRÉS | `ertekeles.md:28-29`; `zaras.md:10` | A `naplok/OLVASOI_PILOT_meres.md`-t utoljára az a1282275 (F60.31) módosította; a `bdb_szelet.py` utána változott (d5f14636, F60.35; 147 szócikk). A BDB-bontás számai (531 / 510 = 47,4%; 123 / 34) nem a HEAD állapotát mérik, a zárás mégis aktuálisként adja. |
| Nulla-diff hatóköre (3.) | ELTÉRÉS | `zaras.md:6`; `ertekeles.md:202,206` | A zárás: „D2: 0 eltérés”. A D2 tábla (`ertekeles.md:66-71`) négy eltérés-csoportot mutat: BDB angol 9/1, BDB magyar 6/1, ÚSZ-előfordulás 117/52, LXX-versszám 356/28. A 0 csak a felsorolt blokkokra igaz; a 8.3 „a kettő ugyanazt adja” általánosítása túlmegy ezen. |
| K5 | OK | `ertekeles.md:50`; `teszt_olvaso_pilot.py:800-834` | A `forras=` mező tartalmazza a `meta.epites_ts=2026-10-12T08:27:32Z`, a `meta.mod` értékét és 39 tábla hash-ét. A D2-tesztben van vers-lap és szó-lap (H7225, H0430), „nem mérhető” ág és negatív ellenpróba. A D1–D5 számértékei NEM ELLENŐRIZHETŐK (a nyers JSON a repón kívül van). |
| db_meres.py csak olvas | OK | `db_meres.py:77`, `:575-580` | Egyetlen kapcsolat, `file:…?mode=ro`, uri=True, írási SQL nincs. A JSON a repón kívüli `--kimenet` könyvtárba kerül. |
| Tesztek | NEM ELLENŐRIZHETŐ | `teszt_olvaso_pilot.py` | A futtatás nem megengedett parancs. 85 `def test_` metódus, egyezik a zárás számával. Az M1-ben előírt esetek a forrásban megvannak: `:80-81` H0216/H2822, `:88` ἀρχῇ, `:99` H7225, `:102` H0216 = 11. |
| feladatok.py ellenoriz | NEM ELLENŐRIZHETŐ | — | Nem megengedett parancs. |
| Adat-szúrópróba | OK | `teszt:80-88`; `ertekeles.md:10` | `lekerdez.py scan H0216 --szakasz "1Móz 1:4"` → n=1; `scan H2822 --szakasz "1Móz 1:4"` → n=1; `lxx-hid "1Móz 1:1"` → `G0746 ἀρχῇ`; `lxx-hid "Zsolt 22:1"` → 11 görög szó, `karoli_ok=zsolt_felirat_eltolas`. |
| Kulcstartomány (2.) | OK / NEM ELLENŐRIZHETŐ | `zaras.md:5` | `karoli "Zsolt 22:32"` van, `"Zsolt 22:33"` nincs; `"1Móz 25:34"` van, `"1Móz 25:35"` nincs. A 693 vers darabszáma nem számolható a megengedett parancsokkal. |
| A1 memória vs. lekérdezés | ELTÉRÉS | `ertekeles.md:187` | Állítás: a 12 BDB nélküli szó-lap szócikke „a `BDB_strong_alias.tsv`-ben … más Strong-szám alatt áll”. Grep `\b(H0553\|H1746\|H3231\|H5503\|H7742\|H8646)\b` a `konkordancia/BDB_strong_*.tsv` fájlokon: az alias- és a pótlás-táblában 0 találat, a H3231 csak az `_elvetett` táblában van. Forrás nélküli és önellentmondó állítás. |
| A2 nyitott tételek | OK | `zaras.md:11-15`; `DONTESEK.md` DT-F60c | A DT-F60c 🟡, Döntés „—”. A `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md` létezik. A tW U+FFFD állítás NEM ELLENŐRIZHETŐ. |
| A3–A5 | nem alkalmazható | — | A diffben nincs tanulmány, PaRDeS-réteg vagy nevesített tanító. |
| A6 (E12–E15) | OK | — | E12–E15: 0 találat. |
| DT-F60a/b/c ↔ értékelés | OK | `DONTESEK.md` (+3 sor); `ertekeles.md:143-144,173-174` | A 8 oszlop egyezik a fejléccel; a döntések szövege egyezik az értékelés 7. és 8.2 pontjával és a zárással. A KJV-állítást a `licencek.tsv:40` igazolja. Ideiglenes azonosítók (DT-F60x). |
| DT-F60a végrehajtás | ELTÉRÉS | `DONTESEK.md` DT-F60a | A döntés „1. + a 2. előkészítése” (kapcsoló az `adat.py`-ban); kapcsoló a kódban nincs, csak az ertekeles 8.4/1 javaslata viszi tovább, nyitott tétel nem követi. |
| DT-F60a/b/c ↔ brief döntésnapló | ELTÉRÉS | `F60_OLVASOI_PILOT_BRIEF.md:12`, `:97-112` | A brief döntésnaplójában nincs sor a DT-F60a/b/c-ről és az M3-döntésről („Gépi szeletelés (próba)” marad). A `kovetkezo` mező elavult (még az M3-at írja). |
| D (brief döntésnapló sorai) | OK, kivétel a fenti sorokban | brief `:101-112` | v1, v2, v1.1/v3.1 `nem_fugg`, v2 hatókör, v3 M2b, v3.2 egyesítés, v3.3: teljesülnek. |
| Brief `ir` mező | ELTÉRÉS | brief `:14` | Írt, de az `ir`-ben nem szereplő fájlok: `szakasz.py`, `naplok/OLVASOI_PILOT_meres.md`, `_ellenorzolista.md`, `_szeletelo_atnezes.md`, `_zaras.md`, `DONTESEK.md`, `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md`. |
| README | ELTÉRÉS | `README.md:3,24,69,73` | Elavult: „két szakaszon fut: 1Mózes 1:1–2:3 és Zsoltárok 22”; „ma 3,7 és 4,8 MB, a 8 MB-os határ alatt, ezért nincs lusta betöltés” (vö. `:79`: 10 MB, 16 MB-os határ, gzip); „a TAHOT-kivonat nem teljes” (CLAUDE.md F85: fejezetszinten teljes); „TBESH … külön engedély kell” (licencek.tsv: `tisztazott`). Ide tartozik a CI E5-ös címsor-törlése. |
| Adatfelmérés | ELTÉRÉS | `felmeres.py:325`; `OLVASOI_PILOT_adatfelmeres.md:20` | A TAHOT sorában „nem teljes (CLAUDE.md)” áll; a sablonból ugyanezt elavultként kivették. |
| Értékelés belső ellentmondásai | ELTÉRÉS | `ertekeles.md:3,121` | A fejléc „M4 1–2. pont kész”, a 8. pont teljes. Az 5.2 pont „tesztek összesen 79”, a zárás és a forrás szerint 85. A D4 „843,8 MB”, a `naplok/SQLITE_EPIT_meres.md:5,81` szerint 845,4 / 845,6 MB, a fájlméret 886,4 MB (valószínűleg MiB és MB keveredik; NEM ELLENŐRIZHETŐ). |
| Zárás ≤ 20 sor | OK | `naplok/OLVASOI_PILOT_zaras.md` | 16 sor, proveniencia-sorral. |
| K4 kimenet a repón kívül | OK | — | Nincs `.html` vagy `.json` kimenet a diffben. |
| 1. Törölt sorok | OK (felsorolva) | — | 198 törölt sor (sablon.html 92, adat.py 34, bdb_szelet.py 30, README 16, epit.py 14, brief 12); adatsor nem törlődött. |
| 4. E17/DT3 sorszám-Δ | OK | — | `adat/` és `konkordancia/` alatt Δ = 0, bontási napló nem kell. |
| 5. ⛔ pontok (M3) | NEM ELLENŐRIZHETŐ | brief `:80-82`; `ertekeles.md:134-146` | Az F60.32 megállt; a felhasználói döntések utána jöttek; a chat nem ellenőrizhető. Az értékelés 7. pontja továbbra is „Nyitva”. |

## ELTÉRÉS-ek súlyossági sorrendben

1. A CI piros (E5 HIBA a README-ben, exit=1), a K4 nem teljesül.
2. A K1 nincs igazolva: az 1Móz 1–25 nincs a tesztekben, a bájtra azonos regresszió hiányzik, a részhalmaz-regresszió kihagyva.
3. Az M2 BDB-bontás mérőszámai az F60.35-ös szeletelő-változás előttiek, a zárás mégis aktuálisként közli őket.
4. A zárás „D2: 0 eltérés” állítása túl széles: négy eltérés-csoport van.
5. A sablon rögzített TBESH-licencmondata adat nélküli, és ellentmond a licencek.tsv-nek.
6. A Thayer- és TBESG-szöveg 700/900 karakterre vágva, „forrásadat” jelleggel áll a lapon.
7. Az ertekeles 8.2 a 12 szó-lapról forrás nélkül állítja, hogy a szócikk alias alatt áll.
8. Kisebb tételek: elavult dokumentáció (README, adatfelmérés, ellenőrzőlista, az értékelés fejléce és 5.2 pontja); a brief `kovetkezo` mezője, döntésnaplója és `ir` mezője nincs frissítve; a DT-F60a „2. előkészítése” követés nélkül maradt.
