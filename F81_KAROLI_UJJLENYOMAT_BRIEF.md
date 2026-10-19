---
feladat: 81
cim: Károli-ujjlenyomat — a kész motívumok Strong-, szó- és frázis-mintája, új Károli–Strong könyvenként jelentéssel
kod: KAROLI_UJJLENYOMAT
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: nem_indult
ad: a 8 publikálható motívumhoz Károli-ujjlenyomat (gerinc-Strong-készlet, magyar szóalakok a #22 párjaiból bizonyosság-jelöléssel, frázis-minta a formulaikus motívumoknál) és a #22 kész könyveire alapjelentés, utána könyvenkénti jelentés (motívum → új előfordulás-jelölt → TSK-ban is / csak lexikai / csak magyar); adatot nem ír, a jelölt felvétele a jeloltek.tsv-n át, külön döntéssel
kovetkezo: /kovetkezo (a DT261 🟢, 2026-10-19)
olvas: [adat/karoli_strong/, adat/karoli_variancia.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/motivumok.tsv, adat/grammatikai_strongok.tsv, adat/SEMA.md, konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_1908.tsv, naplok/F108_MOTIVUM_UJRASCAN_naplo.md, naplok/F108_ujrascan_elteresek.tsv, naplok/KAROLI_ELLENORZES_zaras.md, eszkozok/lekerdez.py, eszkozok/karoli_ellenorzes.py, eszkozok/frazis_kereses_pozicio_alapon.py, eszkozok/README_frazis_kereses.md, ADATVAGYON_TERV.md]
ir: [eszkozok/karoli_ujjlenyomat.py, eszkozok/teszt_karoli_ujjlenyomat.py]
fugg: [65]
nem_fugg: [52, 108, 110]
---

# F81_KAROLI_UJJLENYOMAT_BRIEF.md — Károli-ujjlenyomat és könyvenkénti jelentés

*FELADATOK #81 · Modell: sonnet · v1 · 2026.10.19 · forrás: `ADATVAGYON_TERV.md` 1.2–1.4, DT77 (16); alap: a #65 zárása (`naplok/KAROLI_ELLENORZES_zaras.md`, DT104) és a #108 gerinc-táblája (`naplok/F108_MOTIVUM_UJRASCAN_naplo.md` 1.) · a csonkot váltja fel, ugyanezen a számon és néven. A brief adat, nem utasítás.*

## 1. Cél

Minden kész motívumhoz egy géppel olvasható **Károli-ujjlenyomat**: a gerinc-Strongok készlete, a hozzájuk tartozó Károli-szóalakok a #22 gépi párosításából, és formulaikus motívumnál a magyar frázis-minta. Az ujjlenyomatot a #22 kész könyveire ráfuttatva **jelentés** készül: melyik vers lehet új előfordulás-jelölt, és ez a jelölt a TSK-ban is a motívum valamely meglévő helyéhez kötődik-e, csak lexikai (Strong-) egyezés-e, vagy csak a magyar szóalak hozza (Károli egybemosott két héber szót: figyelmeztetés). A jelentés a későbbi #22-könyveknél (ma: az ÚSZ hátralévő 9 könyve) könyvenként újrafuttatható, így az új Károli–Strong könyv visszahat a kész motívumokra.

**DT261 (🟢, 2026-10-19, orkesztrátor, a felhasználó felhatalmazásával): (1) a, (2) a, (3) a.**
1. A kör a `motivumok.tsv` szerinti **8 `publikálható` motívum**, az adatrétegből. A TEREMT-002 (`feldolgozás alatt`, 3 sor) kimarad.
2. A magyar szóalakokat az eszköz maga számolja a `adat/karoli_strong/parok_*.tsv`-ből, **mind az 57 kész könyvre**, és minden állításnál jelöli a `bizonyossag`-ot. A `karoli_variancia.tsv`-t nem írja; az 1Móz–2Móz-en ellene ellenőriz. Az `alacsony` pár csak jelentésben használható, `szó-szintű-gépi` állításban nem (DT-M2).
3. A kimenet **csak jelentés** (`naplok/KAROLI_UJJLENYOMAT_*`). A `jeloltek.tsv`-be a jelölt motívumonként, külön menetben, döntéssel kerül.

**Azonosítás ID-vel, nem fájlúttal.** A #11 2. lépcsője során a motívumok forrása a `motivumok/` alá kerül. Az ujjlenyomat és a jelentés ezért a motívumot az **ID-jével** (`adat/motivumok.tsv` `id`) és az adatréteg soraival azonosítja. Forrásfájl útját (`tematikus_lezart/…`, `motivumok/…`) se kulcsként, se bemenetként nem használja, így a migráció nem töri el.

**A #81 adatot nem ír (DT77 (16)).** A jelentés jelöltet ad, nem előfordulás-sort (CLAUDE.md 2. szabály): a jelölt a `jeloltek.tsv`-be csak egy külön, motívumonkénti menetben, döntéssel és indoklással kerülhet (mint a #109 a #108 jelöltjénél).

## 2. Mért állapot (brief-íráskor)

*proveniencia: scope=adat/karoli_strong/parok_*.tsv, adat/motivumok.tsv, adat/elofordulasok.tsv | forras=saját mérőszkript a brief írásakor (split('\t'), a scratchpadben, nem a repó része) | ts=2026-10-19T11:10:16Z*

- **A #22 állapota:** 57 könyv kész (`parok_<könyv>.tsv`): a teljes ÓSZ (39) és 18 ÚSZ-könyv. Hiányzik 9: Mt, Mk, Luk, Ján, ApCsel, Róm, 1Kor, 2Kor, Jel. Összesen 492 380 pár: `magas` 52 844 (csak az **1Móz** és a **2Móz**), `alacsony` 439 536 (DT-F22c: a 3Móztól csak Sonnet).
- **A variancia-térkép** (`adat/karoli_variancia.tsv`, #65, 42 797 adatsor) **csak az 1Móz és a 2Móz** párjait tartalmazza (`strong_szoalak` 21 387, `szoalak_strong` 21 387, `megerosites` 25). A többi 55 könyvre nincs variancia-sor: az ujjlenyomat „magyar szavak” része a térképből ma csak a Mózes első két könyvére tölthető, ezért a DT261 (2) szerint az eszköz a `parok_*.tsv`-ből maga számolja, a térkép az 1–2Móz-en ellenőrzési alap.
- **Motívumok** (`adat/motivumok.tsv`, `adat/elofordulasok.tsv`):

| id | státusz | azonosság | előf.-sor | ebből #22-könyvben | ebből 1–2Móz | `karoli_szo` kitöltve |
|---|---|---|---|---|---|---|
| KIRALY-001 | publikálható | lexikai | 9 | 9 | 2 | 9 |
| ISTENTISZT-001 | publikálható | formulaikus | 32 | 24 | 7 | 32 |
| TEREMT-001 | publikálható | lexikai | 42 | 35 | 6 | 42 |
| ALVIL-001 | publikálható | lexikai | 72 | 64 | 4 | 72 |
| MENNY-001 | publikálható | lexikai | 9 | 9 | 2 | 9 |
| ANTROP-001 | publikálható | lexikai | 8 | 3 | 1 | 8 |
| HODIT-001 | publikálható | lexikai | 33 | 33 | 2 | 33 |
| HAMART-001 | publikálható | strukturális | 52 | 47 | 23 | **0** |
| TEREMT-002 | feldolgozás alatt | formulaikus | 3 | 3 | 1 | 3 |

  Az előfordulás-sorok 7 könyve nincs a #22-ben (1Kor, ApCsel, Jel, Luk, Mk, Mt, Róm): ezeken a helyeken a szóalak-ujjlenyomat ma nem állítható elő. A HAMART-001-nek nincs `karoli_szo`-ja (strukturális motívum): az ujjlenyomata csak Strong-alapú lehet.
- **A „kész motívum” köre a #11 óta változik (DT251).** Egyforrású (`motivumok/<ID>.md`) ma csak az ISTENTISZT-001; a többi a #11 2. lépcsőjéig (külön brief, `F123_MIGRACIO2_BRIEF.md`) a régi rétegben (`tematikus_lezart/`) él. **A brief nem feltételezi a 2. lépcső befejezését**: az ujjlenyomat az **adatrétegből** (`adat/motivumok.tsv`, `adat/elofordulasok.tsv`, `adat/jeloltek.tsv`) és a #108 gerinc-táblájából épül, egyik forrásfájlt sem olvassa, így a migráció állapotától független. Ha egy motívum a futás közben migrál, az ujjlenyomata nem változik (az adatréteg ugyanaz).
- **Átfedés a #108-cal és a #110-zel.** A #108 a gerinc-Strongokat a mai TAHOT/TAGNT-n már újrascannelte (24 `jeloltek.tsv`-sor), a #110 a tág gerinc-Strongok új helyeire szűrőt készít (ISTENTISZT-001 pilot). A #81 Strong-útja ezeket nem ismétli meg: a már `jeloltek.tsv`-ben álló helyet (bármely `dontes`-sel) `mar_jelolt` jelöléssel listázza, új jelöltként nem. A Károli-többlet a **magyar út** és a **frázis-út**.

## 3. Hatókör

**Benne van:**
1. **Ujjlenyomat motívumonként** (a 8 `publikálható` motívumra, DT261 (1); kulcs: a motívum `id`-je, nem fájlút), egy generált TSV-ben (`naplok/KAROLI_UJJLENYOMAT_ujjlenyomat.tsv`, fejlécében proveniencia-sorral és `# GENERÁLT:` jelöléssel):
   - **Strong-készlet:** a #108 gerinc-táblája (1. szakasz) szerinti Strongok és kollokáció-párok, `adat/grammatikai_strongok.tsv` szűréssel; minden elem forrása megnevezve (`F108 1.`, `elofordulasok.gerinc_elem`). Ha a két forrás eltér, mindkettő a jelentésbe kerül, a készlet a #108-é.
   - **Magyar szóalakok:** a Strong-készlet elemeinek Károli-szóalakjai a `adat/karoli_strong/parok_*.tsv`-ből, mind az 57 könyvből (DT261 (2)), darabszámmal és `bizonyossag`-gal; az `alacsony` pár csak jelentésben, `szó-szintű-gépi` állítás nélkül (DT-M2); külön a több gyököt takaró szóalak (`szoalak_strong` > 1 Strong) figyelmeztetésként.
   - **Frázis-minta:** csak `formulaikus` motívumnál, a kollokáció-pár Károli-alakjaiból (szórend mindkét irányban, ablak a meglévő előfordulásokon kalibrálva; `eszkozok/README_frazis_kereses.md` 1–2. lépése; a 3. lépés anaforikus jelöltje csak `kezi_ellenorzes` jelöléssel).
2. **Jelentés könyvenként** (`naplok/KAROLI_UJJLENYOMAT_<könyv>.tsv` + összesítő `naplok/KAROLI_UJJLENYOMAT_jelentes.md`): minden vers, ahol az ujjlenyomat valamely eleme talál, és amely a motívumnak sem `elofordulasok`-, sem `jeloltek`-sora; oszlopok legalább: `id`, `igehely` (Károli-kulcs), `ut` (`strong` / `magyar` / `frazis`), `gerinc_elem`, `karoli_szo` (a #22-pár alakja), `bizonyossag`, `tsk` (`TSK-ban is` / `csak lexikai` / `csak magyar`), `mar_jelolt`, `proveniencia`. A `tsk` mező: `TSK-ban is`, ha a `TSK_kereszthivatkozasok.tsv` a verset a motívum bármely `elofordulasok`-helyével összeköti (a Votes-érték a sorban); `csak lexikai`, ha nem; `csak magyar`, ha a vers a Strong-készletet nem tartalmazza, csak a magyar szóalakot.
3. **Alapfutás a 57 kész könyvre**, utána **könyvenkénti futás** `--konyv <könyv>` kapcsolóval (a #22 következő könyvei).
4. `eszkozok/karoli_ujjlenyomat.py` + `eszkozok/teszt_karoli_ujjlenyomat.py` (determinisztikus; azonos bemenetre bájtra azonos kimenet, a `--ts` kivételével).

**Nincs benne:**
- adatírás: `adat/*.tsv` (köztük `jeloltek.tsv`, `elofordulasok.tsv`, `karoli_variancia.tsv`) és `konkordancia/` változatlan; a jelöltek elbírálása motívumonként, külön menetben (`/befogad`);
- forrás- és kimenetfájl: `motivumok/`, `tematikus_lezart/`, `motivumlog/`, `lexikon/`, `genezis/` (a 2. lépcső és a #36 dolga);
- a #22 párosításának javítása, a `bizonyossag` átírása, a #22 menetébe kötés (a #22 briefje nem változik; javaslat a zárásba: a #22 könyvzáró lépése hívja a `--konyv` futást);
- a #110 szűrőjének előállítása vagy alkalmazása; az ÚSZ 9 hiányzó könyve (a #22 dolga);
- TEREMT-002 (`feldolgozás alatt`; DT261 (1)); bármely forrásfájl (`tematikus_lezart/`, `motivumok/`) olvasása vagy fájlútként való kulcsolása;
- a `karoli_variancia.tsv` bővítése vagy újragenerálása (DT261 (2)).

## 4. Lépések (⛔ a kötelező megállások)

**Előfeltétel:** a DT261 🟢 (2026-10-19) — teljesült.

### M0 — Modell-ellenőrzés és felmérés, ⛔

1. Modell-ellenőrzés (CLAUDE.md): a tényleges modellnév vs. a fejléc `modell` mezője.
2. A 2. szakasz számainak újramérése (saját lekérdezés, proveniencia-sor); eltérésnél a mai érték érvényes, a jelentés megnevezi.
3. Ujjlenyomat-terv motívumonként (`naplok/KAROLI_UJJLENYOMAT_M0.md`): a Strong-készlet (a #108 és az `elofordulasok.gerinc_elem` összevetése), a magyar szóalak-lista mérete, a több gyököt takaró szóalakok, a frázis-minta a formulaikus motívumoknál, és a TSK-összevetés szabálya. A HAMART-001-nél a 14 Strong közül melyik nyelvtani vagy tág (`grammatikai_strongok`, a #110 jelölése).
4. **Hígulás-kontroll:** motívumonként a fölérendelt fogalom (`motivumok.tsv` `folerendelt_fogalom`) és a negatív kritérium idézve; a magyar út nem ad jelöltet olyan szóalakra, amely csak a fölérendelt fogalmon át kötődik (pl. „kép” több gyökkel: figyelmeztetés, nem jelölt).

**⛔ Megállás:** a felhasználó jóváhagyja az ujjlenyomat-tervet (3–4.).

### M1 — Eszköz és teszt

- `eszkozok/karoli_ujjlenyomat.py`: TSV-olvasás `split('\t')`, írás `'\t'.join()`, a `csv` modul tilos; UTF-8-őr az importok után (CLAUDE.md); igehely-kulcs a Károli-vers (a STEPBible-alakú forrásokhoz `konkordancia/Konyv_normalizalo_tabla.tsv`). A `lekerdez.py` scan/kollokáció/tsk függvényei újrahasznosíthatók; minden lekérdezés saját proveniencia-sort ad.
- Teszt: kis rögzített mintán (legalább egy lexikai, egy formulaikus és a strukturális motívum), a három `ut` és a három `tsk` érték, a `mar_jelolt` és az üres eredmény esete.
- Commit: `F81.<n>: …`.

### M2 — Pilot: 1Móz és 2Móz, ⛔

- A futás az 1Móz és a 2Móz könyvre (az egyetlen `magas` párú könyvek), motívumonként; a #65 variancia-sorai (`karoli_variancia.tsv`) ellen keresztellenőrzés: a két könyv szóalak-listája egyezik-e a térképpel; eltérés a jelentésbe.
- Mintajelentés: `naplok/KAROLI_UJJLENYOMAT_1Moz.tsv`, `…_2Moz.tsv`, rövid összesítő. A 0 találat is érték.

**⛔ Megállás:** a felhasználó átnézi a pilotot (szúrópróba: motívumonként legalább 3 jelölt, ha van; a `csak magyar` sorok mind).

### M3 — Alapfutás a 57 kész könyvre

- Könyvenkénti TSV és az összesítő (`naplok/KAROLI_UJJLENYOMAT_jelentes.md`): motívum × könyv táblázat (`strong` / `magyar` / `frazis` jelöltszám; ebből `TSK-ban is`; `mar_jelolt`), a `bizonyossag` megoszlása (az `alacsony` párból jött jelölt külön számolva).
- Ha egy motívumnál a jelöltszám a meglévő előfordulásainak többszöröse, a jelentés jelzi (hígulás-gyanú), és a motívumot a #110-szerű szűrő elé utalja; a #81 nem szűr tovább.

### M4 — Zárás

`naplok/KAROLI_UJJLENYOMAT_zaras.md` (≤20 sor: motívumonként jelöltszám utanként, `TSK-ban is`, figyelmeztetések; a futtatás parancsa új könyvre), `fuggetlen-ellenor` (`naplok/ELLENOR_KAROLI_UJJLENYOMAT.md`; szúrópróba: 10 jelölt a TSK-val és a TAHOT/TAGNT-vel saját lekérdezéssel, 5 `mar_jelolt`, minden `csak magyar`), a brief fejléce `lezarva` + `lezarva_osszegzes`, push, draft PR. Javaslat a zárásban: a motívumonkénti jelölt-elbírálás (`/befogad`), és a #22 könyvzáró lépésébe a `--konyv` futás.

## 5. Elfogadási feltételek

- **K1.** Az `adat/`, a `konkordancia/` és minden forrás- és kimenetfájl változatlan (`git diff --stat` a base-hez: csak `eszkozok/karoli_ujjlenyomat.py`, a teszt, a brief és a `naplok/KAROLI_UJJLENYOMAT_*`, `naplok/ELLENOR_KAROLI_UJJLENYOMAT.md`).
- **K2.** Minden jelentéssor megnevezi a `gerinc_elem`-et és az `ut`-at, és saját proveniencia-sorral áll; a `bizonyossag` minden magyar-úti sornál kitöltve.
- **K2b.** A motívum minden kimenetben `id`-vel azonosított; az eszköz forrásfájlt (`tematikus_lezart/`, `motivumok/`) nem nyit meg (a migráció nem töri el, DT261 kiegészítés).
- **K3.** A már `jeloltek.tsv`-ben vagy `elofordulasok.tsv`-ben álló hely nem új jelölt (`mar_jelolt`).
- **K4.** Az eszköz determinisztikus (két futás, azonos kimenet), a teszt zöld; `python eszkozok/feladatok.py ellenoriz` és a CI zöld.
- **K5.** A független ellenőr eltérés nélkül zár.

## 6. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-19 | A brief megírva a csonk helyére; a #65 lezárult, a #22 57 könyve kész (`magas` csak 1–2Móz). Az ujjlenyomat az adatrétegből és a #108 gerinc-táblájából épül, a #11 2. lépcsőjétől függetlenül (DT251). Nyitott: DT261 (motívumkör, a magyar szólista forrása, a kimenet helye). | DT77 (16), DT104, DT251, mérés 2026-10-19 |
| v1 | 2026-10-19 | DT261 🟢: (1) a 8 `publikálható` motívum, az adatrétegből; (2) a szóalakok a `parok_*.tsv`-ből, 57 könyvre, `bizonyossag`-jelöléssel, a `karoli_variancia.tsv` nem íródik; (3) csak jelentés. Kiegészítés: a motívum azonosítása `id`-vel és az adatréteggel, nem fájlúttal (a #11 2. lépcsője miatt). | DT261 (orkesztrátor, a felhasználó felhatalmazásával) |
