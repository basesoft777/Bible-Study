ELTÉRÉS: 5 tétel

# Független ellenőrzés, 2. kör — F60_OLVASOI_PILOT_BRIEF.md (v3.4)

*Ellenőr: `fuggetlen-ellenor` (claude-opus-5-5), 2026-10-12. Az ellenőr nem tudott fájlt írni; a jelentést szó szerint (a táblázat rövidítésével, a lényeg megtartásával) az orkesztrátor mentette ide. Nem commitolt.*

Tartomány: teljes `86ad59263154b10dcda6fac19ffa40110aa99ef3..3631e504ef8e6f137fae39db9aa95e126db2b12d`; javítások `e0e32cec..3631e504` (F60.44–F60.50, 7 commit, 14 fájl).

*Eljárási megjegyzés (az ellenőré):* a megengedett parancsokon túl csak olvasó segédparancsokat használt (`cd`, `git -C`, `grep`/`head`/`tr`/`cut`/`sort`), a `futtat.py` kimenetét a repón kívülre irányította.

| pont | eredmény | indok |
|---|---|---|
| 0 Modell | OK | A 7 javító commit „Claude Sonnet 5.5”, egyezik a brief `modell: sonnet` mezőjével. |
| CI / 1. kör #1 | OK, megszűnt | `futtat.py` a teljes diffre: exit=0; E5: 0; E25: 3, E27: 33 a diffen kívül. |
| K1 lefedettség / 1. kör #2 | OK, megszűnt | A regresszió nem `skipUnless`; az 1Móz 1–25 teszt 693 verset ad (`1Móz 1:1` … `1Móz 25:34`); a végpontok `lekerdez.py karoli`-val igazolva. |
| **K1 engedélyezett-eltérés lista** | **ELTÉRÉS** | A teszt a prototípus `adat.py`-ját az `eszkozok/olvaso_pilot/` könyvtárba írja és onnan futtatja; a prototípus `from bdb_szelet import szeletel`-lel a **HEAD `bdb_szelet.py`-ját** importálja. Hibrid összevetés: a szeletelő hat változása (F60.17, .18, .21, .23, .25, .35) a regresszióban láthatatlan (az `ertekeles.md` 2. pontja szerint az 1:1–2:3-on a „nincs számozott jelentés” 25 → 26, a teszt mégis „a többi 90 lap appar-ja azonos”). A `bdb_szeletelo` (8 lap) indoka téves: az eltérés a `szeletel(…, lemma)` második argumentumából jön (F60.17, 8b642341), nem az F60.31–38-ból. A többi tétel indoka helytálló (`morf_hu` 746, `tbesg` 38, `thayer` 64, `prov.elofordulas` 1). |
| K1 teszt mellékhatása | ELTÉRÉS | Futás közben `eszkozok/olvaso_pilot/_proto_adat_teszt.py` jön létre a repóban; megszakadáskor ott marad. A prototípus `adat.py`-ját és `bdb_szelet.py`-ját együtt, repón kívüli ideiglenes könyvtárba kellene írni. |
| K2 / 1. kör #6 | OK, megszűnt | TBESG/Thayer vágás nélkül, `.bdb.hosszu` gördíthető blokkban. |
| M1 TBESH / 1. kör #5 | OK, megszűnt | `['TBESH', 'konkordancia/TBESH.txt']`; „licenc-kérdés”, „Online Bible”: 0 találat; teszt `tisztazott`-ra. |
| M1 ellenőrzőlista | OK, megszűnt | (c)2, (c)3 „Kikerült (F60.29)”; (c)6 a `licencek.tsv`-hez kötve. |
| M2 frissesség / 1. kör #3 | OK, megszűnt | A mérés (F60.47) a szeletelő- és adat-változások után; 537+28+510 = 1075, 124+1+34 = 159. |
| Nulla-diff / 1. kör #4 | OK, megszűnt | A „0 eltérés” a felsorolt blokkokra szűkítve; a négy eltérő csoport a zárásban és a 8.3-ban. |
| A1 / 1. kör #7 | OK, megszűnt | A 12 Strong-számból 4 csak a `BDB_strong_alias_elvetett.tsv`-ben (`nem_ebbol_a_szocikkbol`); az értékelés egyezik. |
| DT124 végrehajtás | OK, megszűnt | `--kiadas {belso,nyilvanos,kereskedelmi}`; `TestKiadas` 7 teszt. Megjegyzés: a súgó statikus listája és a JSON `licenc` szótára a nyilvános kiadásban is megnevezi a `KJV_Strongs_teljes`-t (metaadat, nem GPL-tartalom). |
| Brief döntésnapló, `kovetkezo`, `ir` | OK, megszűnt | v3.4 sor; `kovetkezo` frissítve; az `ir` a diff 22 fájlját tartalmazza. |
| README, adatfelmérés, értékelés belső ellentmondásai | OK, megszűnt | Hatókör, méretek, TAHOT, TBESH; tesztszám 99; D4 MB (886 415 360 bájt = 845,35 MiB). |
| **Tétel-azonosítók** | ELTÉRÉS | A teljes angol szöveget a 86f83768 (F60.45) hozta, a hivatkozások „F60.46”-ot írnak (`adat.py:492`, `db_meres.py:223`, `teszt:765-766`, `:869`, `ellenorzolista.md:43`, `ertekeles.md:38`, `:122`, `:129`); a `TestRegresszioProto` docstringje „F60.45”, holott F60.46; a `db_meres.py:313` nem létező „F60.52”-re hivatkozik. |
| **Proveniencia-ts** | ELTÉRÉS | `ertekeles.md:213` (8.3) `ts=2026-10-12T15:11Z` maradt az újramért D4 mellett; a 2. pont `ts=…17:40Z`, a hivatkozott `meres.md` `17:42Z`. |
| **„Négy eltérő blokk”** | ELTÉRÉS (kisebb) | `ertekeles.md:169`: három nevet sorol (BDB angol és magyar összevonva). |
| K3, adat-szúrópróba, A2, A6, törölt sorok, kulcstartomány, nulla-diff, E17/DT3 | OK | — |
| K5 D1–D5 értékek, tesztek, `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | Nem megengedett parancs / a nyers JSON a repón kívül. |
| A3–A5 | nem alkalmazható | — |
| ⛔ M3 | OK / NEM ELLENŐRIZHETŐ | `allapot: megallt`; a chatbeli jóváhagyás nem ellenőrizhető. |

## ELTÉRÉS-ek súlyossági sorrendben

1. K1 regresszió: hibrid összevetés (a prototípus a HEAD `bdb_szelet.py`-jával fut); a `bdb_szeletelo` tétel indoka téves. A felhasználó döntése előtt pontosítandó.
2. A K1-teszt futás közben ideiglenes kódfájlt ír a repóba.
3. Téves tétel-azonosítók („F60.46” az F60.45-ös változásra; nem létező „F60.52”).
4. Elavult vagy eltérő proveniencia-ts (8.3 `15:11Z`; 2. pont `17:40Z` vs. `17:42Z`).
5. A „négy eltérő blokk” felsorolása három nevet ad.

Az első kör mind a 14 eltérése megszűnt.
