# JELOLT_ELOSZURES_naplo.md — F150 (#150) M0 mérés

*Modell: claude-sonnet-5-5 · 2026-11-01 · ág: `claude/f150-jelolt-eloszures-8db30b` · lépés: 4. szakasz 0. (M0 mérés), utána ⛔ DT-F150a.*

*(proveniencia: scope=adat/jeloltek.tsv (`jelolt_tipus=elofordulas`, `dontes` = beépítve vagy elutasítva, n=604: 261 beépítve + 343 elutasítva) + adat/elofordulasok.tsv (gerinc-kombinációk) + adat/motivumok.tsv (`azonossag_tipusa`) + adat/elutasitasi_okok.tsv (mintaszótár) | forras=naplok/JELOLT_ELOSZURES_meres.py (szerep_karoli.vers_strongok: TAHOT+TAGNT, Károli-kulcs; lexikon_general.igehely_lista) | ts=2026-11-01)*

Újrafuttatás: `python naplok/JELOLT_ELOSZURES_meres.py [--reszletes]` (a szkript csak olvas; az `adat/*.tsv`-hez nem nyúl).

## 1. Módszer

- **Kör:** a `jeloltek.tsv` `elofordulas` típusú, eldöntött sorai. A 34 `nyitva` sor nincs benne (nincs döntés, amihez mérni lehetne); a 7 `motivumkozi` sor sincs (nem előfordulás-jelölt).
- **Gerinc-kombináció:** motívumonként az `elofordulasok.tsv` `strong` mezőjének különböző értékei (pl. `H7121+H8034`, `G1941`), a nyelvtani Strongok (a `grammatikai_strongok.tsv` és a H9xxx; `szerep_karoli.nyelvtani`) kiszűrve. A sorok `strong` nélküli részét (HAMART-001 5 sor, MENNY-001 3 sor) a kombináció-halmaz nem tartalmazza.
- **Próba:** a jelölt versében (tartománynál `lexikon_general.igehely_lista` szerint minden versben) a vers Strong-halmaza (`szerep_karoli.vers_strongok`: TAHOT+TAGNT, kulcsa a Károli-vers, F85) tartalmazza-e egy gerinc-kombináció **minden** tagját **egy versben**. Ha egyiket sem: `valoszinu_ki`. A STEPBible-alakú datasetek nem kellettek, ezért a `Konyv_normalizalo_tabla.tsv` itt nem szerepel.
- **Hordozó-szűrés:** `valoszinu_ki` csak a `motivumok.tsv` `azonossag_tipusa` = `lexikai` vagy `formulaikus` motívumon; máshol `vizsgalando` („a hordozó nem lexikai: a gépi szabály nem dönt”). Hordozók: lexikai = ALVIL-001, ANTROP-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001; formulaikus = ISTENTISZT-001, TEREMT-002; **strukturális = HAMART-001**.
- **Szöveg nélküli jelölt:** külön számolva (nincs Strong-halmaz a versre): 1 elutasított sor (TEREMT-002), mindkét összesítésben kívül marad a nevezőből.
- **Négy változat** is kiszámolva (teljes kombináció / bármely tag; egy versben / a tartomány összes versében). A tartomány-változat a mintán nem ad eltérést (a két „union” sor azonos a „vers” sorral), a „bármely tag” enyhébb szabály. **Fő változat:** teljes kombináció, egy versben (a brief „szópár egy versben” elve; ez adja vissza az eredeti próba számait).
- **Ok-egyezés (c):** az elutasítás `indoklas`-át az `adat/elutasitasi_okok.tsv` mintaszótárával (regex, kis-nagybetű nélkül, a `sorrend` szerinti első egyező) címkéztem. A mintaszótár egyetlen címkéje fedi a „szókapcsolat-hiányt”: **„a formula nincs a versben”** (10. sor); a **„név nélküli forma”** (20.) a formula részének megléte, nevének hiánya: ezt is ide számoltam. A többi címke (névadás, passzív, jogi fellebbezés, eskü, erkölcsi intelem, stb.) más ok. Mivel a mintaszótár az ISTENTISZT-001 indoklásaiból készült, a TEREMT-002 („nincs H8414+H0922 pár — önálló tohu”) és a többi motívum indoklásai nagyrészt „egyéb”-be esnek; ezért **második, bővített mérték** is: a mintaszótár két címkéje VAGY az indoklásban a hiány kifejezése (`nincs … pár / a versben / szókapcsolat / Hxxxx / Gxxxx`, `nem tartalmaz`, `hiányzik`, `nem szerepel`, `nincs meg`, `nem találhat`). A bővített mérték heurisztika (a mérés kedvéért, nem a mintaszótár része), a pontos regex a szkriptben (`HIANY_JELLEGU`).

## 2. Összesítő: az eredeti próbával összevetve

| | elutasítva (szöveggel) | `valoszinu_ki` | beépítve (szöveggel) | hamis kizárás |
|---|---|---|---|---|
| eredeti próba (a brief 2. szakasza) | 342 | 217 (63%) | 261 | 12 (4,6%) |
| **M0, hordozó-szűrés NÉLKÜL** | 342 (+1 szöveg nélkül) | **217 (63,5%)** | 261 | **12 (4,6%)** |
| **M0, hordozó-szűréssel** | 342 (+1 szöveg nélkül) | **134 (39,2%)**; `vizsgalando` 208 | 261 | **7 (2,7%)** |

**Az eredeti számok pontosan reprodukálódtak (217/342, 12 hamis kizárás).** A hordozó-szűrés a 83 HAMART-001-es felismerést és a 12-ből 5 hamis kizárást veszi ki (mind HAMART-001), de **7 hamis kizárás megmarad, és a küszöb (0 a lexikai motívumokon) nem teljesül**.

Ok-egyezés a 134 felismert elutasításon: mintaszótár szerint **64/134** (48%), bővített mérték szerint **106/134** (79%). A hiányzó 28 a bővítés után is nem „hiány-jellegű” indoklás (pl. névadás, erkölcsi intelem: ISTENTISZT-001 12 sor; „más igehely/téma”: KIRALY-001; „tematikus párhuzam, más görög szavak”; szövegkritika: ALVIL-001; Minősítési mérce: ALVIL-001). Ezeknél a gép a helyes irányba rendez (a gerinc-szókapcsolat tényleg hiányzik), de a döntés oka más, mint a hiány.

Az enyhébb („bármely tag egy versben”) szabály hordozó-szűréssel: 108 felismert (31,6%), **4 hamis kizárás** (MENNY-001 3, ANTROP-001 1: 1Kor 2:15). Tehát a 7 hamis kizárásból 3 az enyhe szabállyal is megmarad ott, ahol a versben a gerincből egyetlen Strong sincs.

## 3. Motívumonként (fő változat, hordozó-szűréssel)

| motívum | hordozó | beépítve | elutasítva | hamis kizárás | felismert elutasítás (arány) | ok-egyezés (mintaszótár / bővített) |
|---|---|---|---|---|---|---|
| ALVIL-001 | lexikai | 72 | 5 | 0 | 4/5 (80%) | 1/4 · 3/4 |
| ANTROP-001 | lexikai | 8 | 0 | **4** | – | – |
| HAMART-001 | **strukturális** | 52 | 163 | 0 (a szűrés nélkül 5) | 0/163 (szűrés nélkül 83/163, 51%) — mind `vizsgalando` | – |
| HODIT-001 | lexikai | 33 | 4 | 0 | 3/4 (75%) | 0/3 · 0/3 |
| ISTENTISZT-001 | formulaikus | 33 | 92 | 0 | 58/92 (63%) | 46/58 · 46/58 |
| KIRALY-001 | lexikai | 9 | 13 | 0 | 4/13 (31%) | 0/4 · 0/4 |
| MENNY-001 | lexikai | 9 | 1 | **3** | 1/1 | 0/1 · 0/1 |
| TEREMT-001 | lexikai | 42 | 2 | 0 | 2/2 | 0/2 · 0/2 |
| TEREMT-002 | formulaikus | 3 | 63 (1 szöveg nélkül) | 0 | 62/62 (100%) | 17/62 · 57/62 |
| **összesen** | | 261 | 343 | **7** (szűrés nélkül 12) | 134/342 (39%) (szűrés nélkül 217/342, 63%) | 64/134 · 106/134 |

A két formulaikus motívumon (ISTENTISZT-001 + TEREMT-002) a szabály **0 hamis kizárás** mellett 120 elutasítást ismer fel a 154 szöveggel rendelkezőből (78%), a 36 beépítettből egyet sem zár ki. A lexikai motívumokon az elutasítások száma kicsi (ALVIL 5, HODIT 4, KIRALY 13, MENNY 1, TEREMT-001 2, ANTROP 0), tehát az arányok statisztikai értéke gyenge; a hamis kizárás viszont ott jelentkezik, ahol számít (MENNY-001, ANTROP-001).

### 3.1 A hamis kizárások soronként (hordozó-szűrés nélkül mind a 12; a hordozó-szűréssel megmaradó 7 ★)

| motívum | igehely | hordozó | ok (a versben a gerincből mi van) | megmarad szűréssel |
|---|---|---|---|---|
| MENNY-001 | Júd 1:6 | lexikai | H0430+H1121 / H5303 hiányzik; semmi | ★ |
| MENNY-001 | Júd 1:14-15 | lexikai | ugyanaz; semmi | ★ |
| MENNY-001 | 2Pét 2:4-5 | lexikai | ugyanaz; semmi | ★ |
| ANTROP-001 | Luk 1:46 | lexikai | G4151+G5590 / H2416+H5315 hiányzik; a versben G5590 (a pár a 47. versben folytatódik) | ★ |
| ANTROP-001 | Luk 1:47 | lexikai | ugyanaz; a versben G4151 | ★ |
| ANTROP-001 | 1Kor 2:14 | lexikai | ugyanaz; a versben G4151 (a „ψυχικός ἄνθρωπος” melléknévi alak más Strong) | ★ |
| ANTROP-001 | 1Kor 2:15 | lexikai | ugyanaz; semmi (πνευματικός) | ★ |
| HAMART-001 | Ézs 24:5-6 | strukturális | a 14 Strong-elem egyike sem a versben | kikerül (`vizsgalando`) |
| HAMART-001 | Hós 4:1-3 | strukturális | ugyanaz | kikerül |
| HAMART-001 | Mt 15:19 | strukturális | ugyanaz | kikerül |
| HAMART-001 | Mk 7:21-23 | strukturális | ugyanaz | kikerül |
| HAMART-001 | 2Pét 3:6-7 | strukturális | ugyanaz | kikerül |

**A 12 ismert eset sorsa:** a brief a 12-t tartományokkal nevezi meg (Luk 1:46–47, 1Kor 2:14–15); a `jeloltek.tsv`-ben ezek versenként külön sorok (4 ANTROP-001 sor), így a 12 = 3 MENNY-001 + 4 ANTROP-001 + 5 HAMART-001. **A hordozó-szűréssel csak az 5 HAMART-001-es kerül ki.** A brief 2. szakaszának állítása, hogy „mind nem lexikai hordozójú motívum”, **a `motivumok.tsv` szerint nem igaz**: a MENNY-001 és az ANTROP-001 `azonossag_tipusa` mezője `lexikai`; csak a HAMART-001 `strukturális`.

**A HAMART-001 megjegyzés (a „FIGYELEM”-re):** a HAMART-001 hordozója `strukturális`, nem lexikai, ezért a szűrés a hamis kizárást ott megszünteti, és nem marad lexikai hamis kizárás a HAMART-001-en. A megmaradó hamis kizárás oka a MENNY-001 és az ANTROP-001 (mindkettő `lexikai` a `motivumok.tsv`-ben) meghatározása, nem a hordozó-szűrés hibája: a motívum meghatározása („tematikus/szerkezeti” NT-helyek a MENNY-001-ben; melléknévi alakok és versen átnyúló párok az ANTROP-001-ben) nagyobb, mint amit a `strong` oszlop kombinációi lefednek.

## 4. A mérés torzítása és korlátai

1. **Szó szerinti torzítás.** A jelöltek jó része eleve Strong-kereséssel jött (3. lépés, teljes ÓSZ/ÚSZ scan), tehát a jelölt nagy valószínűséggel tartalmazza a keresett Strongot. A gép és az aranystandard (a felhasználó döntése) ugyanazt a szó szerinti jegyet nézi, ezért a mérés a szó szerinti esetnek kedvez; a tematikus/szerkezeti eseteket (a MENNY-001 NT-helyei, a HAMART-001) a keresés eleve nem hozza, és a beépítettek közül azok jelennek meg, amelyeket a felhasználó külön, kézzel vett fel. A hamis kizárás tehát **alsó becslés** olyan jelöltekre, amelyek a jövőbeli scanből jönnek, és a felismerési arány **felső becslés**.
2. **Kis minta a lexikai motívumokon.** ALVIL-001 5, HODIT-001 4, MENNY-001 1, TEREMT-001 2, ANTROP-001 0 elutasítás; a felismerési arány ezeken nem általánosítható.
3. **Az aranystandard a `jeloltek.tsv` döntése, az indoklás utólagos.** Az ok-egyezés a mintaszótár érvényességi köre (ISTENTISZT-001 indoklásai) szerint a TEREMT-002-n és a lexikai motívumokon alulmér (17/62 → 57/62 a bővített mértékkel); a bővített mérték heurisztika.
4. **Versszint, nem szinttartomány.** A szabály egy versben keresi a szópárt; a versen átnyúló párok (Luk 1:46–47 ψυχή ↔ πνεῦμα) a mai bemenettel hamis kizárást adnak. A tartomány-változat nem javít (a jelöltsorok már tartományok vagy külön versek).
5. **A kombinációk a már beépített sorokból jönnek.** Új alakot (pl. melléknévi ψυχικός/πνευματικός) a halmaz nem ismer, amíg valaki fel nem veszi; ez a MENNY-001/ANTROP-001 hibaforrása.

## 5. DT-F150a — kérdés a felhasználónak

**Kérdés:** bevezessük-e a gépi előszűrőt (a gerinc-szókapcsolat hiánya → `valoszinu_ki`, csak átnézési sorrend, a `jeloltek.tsv` nem változik), és ha igen, milyen hatókörrel? A brief küszöbe: **0 hamis kizárás a lexikai motívumokon**. A mérés szerint ez a küszöb a lexikai hordozón **nem teljesül** (7 hamis kizárás: MENNY-001 3, ANTROP-001 4), a formulaikus hordozón **teljesül** (0/36).

**Opciók:**
- **(a)** Bevezetés **csak formulaikus hordozóra** (ISTENTISZT-001, TEREMT-002; a gép kimondja: lexikai és más hordozón minden sor `vizsgalando`). Mért: 0 hamis kizárás, 120/154 felismert elutasítás. A lexikai motívumokat a javítás után külön M0-val vesszük fel.
- **(b)** Bevezetés lexikai + formulaikus hordozóra, **motívum-kivétellistával** (MENNY-001 és ANTROP-001 kimarad). A mintán 0 hamis kizárás, de a kivétellista a mintán illesztett (túlillesztés), és a többi lexikai motívum (kis minta) nincs igazolva.
- **(c)** Bevezetés lexikai + formulaikus hordozóra változatlanul, **a küszöb módosításával** (pl. ≤ 3%). Mért: 7/261 (2,7%) hamis kizárás.
- **(d)** A szabály javítása (versen átnyúló párok; a jóváhagyott kombinációk bővítése melléknévi/rokon alakokkal; a MENNY-001 NT-helyeinek tematikus hordozóként való átsorolása), utána új M0; addig nincs bevezetés.
- **(e)** Nincs gépi előszűrő; a brief 3.4 modelles lépése (M3) a teljes sorrendezésre.

**Javaslat: (a).** Okok: ott teljesül a 0-küszöb, a formulaikus motívumokon van az elutasítások zöme (155 a 343-ból; a két motívum a jövőbeli scanek fő forrása), a hordozó-szűrés a brief elvét (a gépi szabály csak lexikai/formulaikus jegyen dönt) szó szerint követi, és a lexikai motívumok hibái azonosíthatók (nem „zaj”, hanem meghatározás-hiány), tehát a (d) külön tételben javítható anélkül, hogy a bevezetés várna rá. A (c)-t nem javaslom: a küszöböt a felhasználó 0-ra rögzítette, és a hamis kizárás itt az elnémult tartalmi vers (MENNY-001 Júd 1:6, 1Kor 2:14), amit a sorrend a lista végére tenne.

*Megjegyzés a gyakorlati értékhez:* a mai 34 `nyitva` sorból formulaikus motívumra csak 1 `elofordulas` sor esik (ISTENTISZT-001; a 5 motívumközi nem ide tartozik), tehát az azonnali haszon kicsi; a haszon a következő scanekben jelentkezik (a TEREMT-002 és az ISTENTISZT-001 típusú, sok jelöltet adó, szóegyezés-alapú motívumokon).

## 6. Eltérések a brieftől

- A 12 ismert hamis kizárás a `jeloltek.tsv`-ben versenként külön sorok (a brief tartományokat írt a Luk 1:46–47, 1Kor 2:14–15 helyén).
- A brief 2. szakasza szerint mind a 12 nem lexikai hordozójú; a `motivumok.tsv` szerint csak az 5 HAMART-001-es az; a MENNY-001 (3) és az ANTROP-001 (4) lexikai, a hordozó-szűrés ezeket nem szűri ki.
- A szkript a négy változatot és a szűrés nélküli/szűréssel összesítőt is kiadja (a brief a fő próbát kérte); a fő változat a brief szerinti.
- A `jeloltek.tsv`-hez és a `lexikon_general.py`-hoz nem nyúltam; az utóbbit csak importáltam (`igehely_lista`).
