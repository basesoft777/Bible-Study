# GENERALT_NEZET_CI — mérési napló (FELADATOK #116)

*Brief: `F116_GENERALT_NEZET_CI_BRIEF.md` · Ág: `claude/f116-generalt-nezet-ci` · Modell: claude-sonnet-5-5*

## 1. M0 — kiinduló mérés (2026-10-18)

`scope=general.py --ellenoriz (naplo, index, nyitott), blokk-diff scratch-szkripttel, git log/show, WSL-újrafuttatás git archive-ból | forras=manual (CLI-futtatás) | ts=2026-10-18 | alap=origin/main be85d5de (+ F116.0 commit 2fc22d66)`

### 1.1 Az E28/E29 számok

Az `E28` és az `E29` szabad: a `szabalyok.py`-ban és a workflow-ban (`.github/workflows/`) nincs
előfordulásuk, és a távoli ágak `*.py`/`*.yml` fájljaiban sincs (`git grep` minden `origin/*` ágon).
Az md-fájlokban a #23 CI-terve (DT84), a SEMA 3.10.4 hivatkozása és a #112 briefje (E30) említi
őket. A `szabalyok.py` legmagasabb száma az E27. **A brief feltevése egyezik.**

### 1.2 Blokkonkénti állapot (`general.py --cel <c> --ellenoriz`)

| Blokk | Állapot | Diff-sor |
|---|---|---|
| `naplo#attekintes` | zöld | 0 |
| `naplo#kuszob` | zöld | 0 |
| `naplo#kulcsszo_index` | zöld | 0 |
| `naplo#konyv_index` | **eltér** | 4 (2 törölt + 2 hozzáadott: a Jób-sor és a Préd-sor cseréje) |
| `index` | zöld | 0 |
| `nyitott` | **eltér** | 79 |

A mérés egyezik a brief mért állapotával (4 és 79 diff-sor).

### 1.3 Az eltérések oka

**`naplo#konyv_index` (4 diff-sor): adatváltozás újragenerálás nélkül.** A Jób 17:13/17:16 → 17:12/17:15
és a Préd 9:10 → 9:12 ALVIL-001-sor az `adat/elofordulasok.tsv` három sora; mind a `98f22fc6`
(F87.3: „M1 — az öt sor javítása az elofordulasok.tsv-ben és a jeloltek.tsv-ben”, 2026-10-12)
commitban változott (`git log -S'Jób 17:12'`, `-S'Préd 9:12'`). A `motivumlog/PaRDeS_motivumok.md`-t az óta nem érintette commit
(utolsó: `be2ae5b5`, 2026-10-02, F35.4 szövegcsere), tehát a blokk nem generálódott újra. Kézi szerkesztés
és generátor-változás a blokk törzsében nincs.

**`nyitott` (79 diff-sor): adatváltozás újragenerálás nélkül.** A blokk `ts=2026-09-15`
(`f4253313`) állapotán 17 nyitva sor állt a `jeloltek.tsv`-ben; azóta a nyitva-halmaz sorszintű
követése (`git show <rev>:adat/jeloltek.tsv` minden érintő commiton) szerint:

| Commit | Dátum | Hatás a nyitva-halmazra |
|---|---|---|
| `8313214d` T1.3 / `ed79575a` T2.2 | 2026-09-25 | TEREMT-002: +66, majd −66 (átmeneti, a végállapotban nincs) |
| `a0c3cd95` F63.5 (+244 sor) | 2026-10-11 | +8: HAMART-001 ×7 (2Pét 3:10, 3:12; 5Móz 4:25; Bír 2:19; Jób 16:18, 31:38; Sof 3:7), KIRALY-001 ×1 (1Pét 2:9); `elutasítva` 66→302 |
| `4f85d54c` F63.15 | 2026-10-11 | `elutasítva` 302→308 (nyitva nem változik) |
| `b5e60b5c` F108.1 | 2026-10-17 | +25: ANTROP-001 ×2 (Mt 12:18, 1Pét 1:22), HAMART-001 ×1 (2Tim 3:8), ISTENTISZT-001 ×21, TEREMT-001 ×1 (Jób 41:32) |

Összesen 17 + 8 + 25 = 50 nyitva sor 7 motívum-ID-ről (megszűnt nyitva sor: 0); `elutasítva` 308;
`beépítve` 259 (változatlan). A 79 diff-sor teljes lebontása: 1 fejsor (összegzés), 17 törölt +
50 hozzáadott táblasor (a 17 régi sor újraszámozva, +33 új), 5+5 sor a tanulmány-táblában
(nyitott-oszlop: ANTROP 1→3, HAMART 0→8, ISTENTISZT 0→21, KIRALY 0→1, TEREMT-001 0→1);
1+17+5 = 23 törölt, 1+50+5 = 56 hozzáadott. Kézi szerkesztés és generátor-változás nincs.

**A brief feltevése mindkét blokkra egyezik** (az ok újragenerálás nélküli adatváltozás).

### 1.4 A generátor futása friss checkouton, `konkordancia/_nyers/` nélkül

A worktree és a `git archive HEAD` kibontása is friss checkout; a `konkordancia/_nyers/` egyikben
sincs. A három cél (`naplo`, `index`, `nyitott`) mindkettőn hiba nélkül lefut (`rc=0`, üres stderr),
és az `--ellenoriz` ugyanazt az állapotot adja (lásd 1.2). **A generátor CI-ben futtatható.**

Futási idő célonként (egyszeri mérés, a Python-indítással együtt):

| Cél | Windows (worktree) | Linux/WSL2 (ext4, `git archive`) |
|---|---|---|
| naplo | ~0,19 s | ~0,10 s |
| index | ~0,19 s | ~0,07 s |
| nyitott | ~0,19 s | ~0,07 s |

### 1.5 Sorvég

- A három cél commitolt blobja tisztán LF (`git show HEAD:<út> | grep -c $'\r'` = 0; `git ls-files --eol`:
  `i/lf`); a Windowsos munkafában a `core.autocrlf=true` miatt `w/crlf`. A `.gitattributes` csak a
  `*.tsv`, a `.claude/agents/*.md` és a `*.sh` fájlokra ír elő `eol=lf`-et; a `*.md`-re nem.
- A `--kimenet` alá írt generátor-kimenet mindhárom célra tisztán LF (0 CR bájt), és **bájtra azonos**
  Windowson és Linuxon (`cmp`: naplo, index, nyitott, nyers és CR-mentesített összevetés is 0).
- A `--ir` (élő fájlba írás) a munkafa fájljának sorvégét őrzi (`eles_fajl_beolvas`/`eles_fajl_ir`);
  Windowson ez CRLF, amelyet a git commitkor LF-re normalizál. **Az E28 összevetési alapja ezért a
  commitolt blob (`git show <fej>:<út>`) legyen, nem a munkafa-fájl**, a CI-terv 1. szakasz 3. pontja szerint.
- Következmény: nem találtam platformfüggő eltérést a generátor-kimenetben; a brief feltevése egyezik.

### 1.6 Az M0 összegzése

Az M0 egyetlen pontja sem tér el a brief feltevésétől (számok szabadok; generátor CI-ben fut; sorvég
nem platformfüggő a kimenetben; mindkét eltérés oka újragenerálás nélküli adatváltozás). A 2. lépés ⛔
nem aktiválódik. A 3. lépés (újragenerálás) a felhasználói kikötés szerint commit nélkül áll meg
a diff bemutatásánál (lásd 2. szakasz).

## 2. A 3. lépés: a két blokk újragenerálása (`F116.3`)

`scope=general.py --cel naplo --ir; --cel nyitott --ir; git diff --numstat | forras=manual (CLI-futtatás, scratch-szkripttel igazolva) | ts=2026-10-18`

A felhasználó jóváhagyása a commit előtt megvolt („a #116-nak az F116.3 commit jóváhagyva”, az orkesztrátoron át).
A diff: `NYITOTT_FELADATOK.md` +56/−23 (79 diff-sor), `motivumlog/PaRDeS_motivumok.md` +2/−2 (4 diff-sor);
minden diff-sor visszavezetve commitolt adatváltozásra (1.3 szakasz: `98f22fc6`; `a0c3cd95`, `4f85d54c`, `b5e60b5c`).
Igazolás a commitolt blobbal szemben: a GENERÁLT-KEZDET/VÉGE közötti törzseken kívül minden bájtra azonos
(kézi szakaszok), a VÉGE-markerek azonosak, a kezdő markersorok `ts=` értéke is azonos maradt:
a generátor a meglévő marker-pár `ts=` értékét nem írja át (`2026-09-15` maradt), tehát a brief 3. lépésének
„`ts=` változik” várakozása nem teljesült, de a G5 feltételét ez nem sérti (csak törzs változott).
Utána a három cél `--ellenoriz`-e zöld (naplo 4/4, index, nyitott).

## 3. Mérés a kész kóddal (8. lépés)

`scope=futtat.py --teljes; futtat.py --valtozott (HIBA-szint); ideiglenes lista ISTENTISZT-001-gyel; test_szabalyok.py; feladatok.py ellenoriz; grep | forras=manual (CLI-futtatás a munkaágon, F116.8 = 49491587) | ts=2026-10-18`

**3.1 `python eszkozok/ellenorzes/futtat.py --teljes`** (üres lista; ~10 s): `## E28 (0 talalat)` + a
jelentés-megjegyzés „E28: 0 migrált nézet”; `## E29 (0 talalat)`; kilépési kód 0. A három marker-cél
`general.py --ellenoriz`-e zöld (naplo 4/4, index, nyitott). A `--teljes` mód a futtat.py meglévő szabálya
szerint minden találatot JELENTES-re minősít (kilépés mindig 0), ezért a HIBA-szintet a 3.2 külön méri.

**3.2 Próba ideiglenes listával, commit nélkül** (a lista egyetlen sora: `ISTENTISZT-001`,
`lexikon/ISTENTISZT-001_TUDOMANYOS.md`, `lexikon`, `apparatus`; a próba után `git checkout` az üres
listára, a munkafa tiszta):
- **E29: 14 `【NAPLO` sor** (474., 481., 485. … sor; minden találat a `【NAPLO` minta). Egyezik a CI-terv 2.
  szakaszának mért kiindulásával (14).
- **E28: 1 eltérés**, a generátor élesen fut a migrált úton (alfolyamat, `PARDES_DATUM=2026-10-05` = a
  commitolt fájl első GENERÁLT jelölőjének `ts=` dátuma, ideiglenes kimeneti könyvtár). Az újragenerált és a
  commitolt blob közt 931 diff-sor van (a CR-mentesített, LF-normalizált összevetésben); az első eltérés a 3.
  sorban (egy üres sor a generált fejléc után), többek közt a #78 óta eltérő 2. szakasz sorai is.
  Ez egyezik a brief várakozásával (a lap a #78 óta eltér az újragenerálttól).
- `--valtozott … --diff-alap HEAD --diff-fej HEAD` móddal a két szabály szintje **HIBA** (E28: 1, E29: 14),
  kilépési kód 1: a fájlszintű szint nem esik a D8 diff-leminősítés alá. A lista ezért üres addig, amíg a #11 a
  migrált lappal együtt fel nem veszi a sort.

**3.3 Tesztek és ellenőrzők:** `test_szabalyok.py` 137 teszt OK (köztük `E28Teszt` 13, `E29Teszt` 10),
`test_tanulmany.py` 32 teszt OK; `python eszkozok/feladatok.py ellenoriz`: 136 brief, 0 hiba, 0 figyelmeztetés.

**3.4 G4 (grep):** az E29-szakasz (`szabalyok.py` 2032–2077. sor, a `# E29 --` fejlécsortól a regisztrációs
sorig) a `import `, `general`, `motivumok/`, `lexikon_general`, `subprocess` mintákra **0 találat**: az
E29 nem importál generátort és nem olvas `motivumok/` forrást. A G6 grep (`import csv`, `csv.`) a
`szabalyok.py`-ban 0 találat; a TSV-t `kozos.dict_sorok_sorszammal` olvassa (`split('\t')`). A G7: a
`szabalyok.py` és a `test_szabalyok.py` a meglévő stdout/stderr-wrappert viseli.

## 4. Döntésnapló és eltérések a CI-tervtől

- **E1.** (javítva az F116.11-ben, a független ellenőr 1. eltérése nyomán) Az összevetés alapja a commitolt blob
  nyers bájtjai (`git show HEAD:<út>`, UTF-8 dekódolás, **sorvég-konverzió és normalizálás nélkül**): a sorvégnek is
  egyeznie kell, ahogy a CI-terv 1. szakasz 3. pontja és a brief 5. lépése kéri; a generált oldal is nyers. A korábbi
  változat (F116.5) mindkét oldalt LF-re normalizálta, ez eltért a CI-tervtől. Tartalék (a `git` hiánya vagy a
  HEAD-ben nem szereplő fájl, helyi futás): a munkafa-fájl LF-re normalizálva, és a jelentés megjegyzése jelzi, hogy
  ez nem blob-összevetés. A generált blokk a `general.py` saját függvényeiből jön (`blokk_lista_eles`,
  `marker_par_keres`, `blokk_torzs`), a generátor logikája nem duplikálódik.
- **E2.** A migrált ágon a generátor alfolyamatként fut (`--cel <cel> --id <id> --kimenet <tmp>`), a repón kívüli
  ideiglenes könyvtárba. A tesztben a generátor-hívás, a blob és a marker-blokkok forrása helyettesíthető
  (`_e28_general_futtat`, `_e28_commitolt`, `_e28_generalt_blokkok`); az éles generátor útját a 3.2 próba igazolja.
- **E3.** A jelentés az E28 alatt egy-soros megjegyzést ír („E28: 0 migrált nézet”, „E28: nem futott …”); ehhez
  a `futtat.py` `jelentes_szoveg`-e egy `E28_JEGYZETEK` listát olvas (az E16 push-megjegyzés mintájára).
- **E4.** Az E29 mintakészlete a CI-terv 2. szakaszán felül tartalmazza a `【NAPLÓ` (ékezetes) alakot is (az E2
  mindkét alakot ismeri), és a `SZINT: belso` ideiglenes alakot; a `SZINT-KEZDET`/`SZINT-VÉGE` bármely értékkel
  tiltott (a `belso` jelölőinek részhalmaza). Ismeretlen `melyseg` HIBA az E29 alatt.
- **E5.** Mind az E28, mind az E29 a `HATOKOR_SZABALYOK` közé került (a `--teljes` módban a `['__TELJES__']`
  jelzőt kapják, ahogy az E3/E19/E25), és a `FAJLSZINTU_SZABALYOK` közé (D6). Az E28 PR-en csak a brief szerinti
  érintett fájloknál indul (`_e28_indul`); az E29 minden futásban fut.
- **E6.** Ellentmondás a CI-tervvel: az F116.5 sorvég-normalizálása volt az (lásd E1, javítva); más nincs.
  Generátor-módosításra nem volt szükség, a nyers összevetés a mai main-en nem fordít pirosra semmit.
- **E7.** Tudnivaló a #11-nek (D7 szerint a felhasználó vezeti át): a lista sorának felvételekor a PR `[ELLENŐRZŐ]`
  előtagot kap (D3, E16); a workflow Python 3.11-et használ, az itteni mérés 3.14-gyel futott (a kód nem használ
  3.12+ nyelvi elemet, de a CI-futás ezt csak a PR-en igazolja).

## 5. Javítókör (F116.11, F116.12; a független ellenőr, `naplok/ELLENOR_F116.md`, `db57480d`)

`scope=test_szabalyok.py, test_tanulmany.py, futtat.py --teljes, general.py --ellenoriz ×3, feladatok.py ellenoriz | forras=manual (CLI-futtatás a munkaágon, F116.12 = 1570bf60) | ts=2026-10-18`

- **F116.11 (sorvég, közepes):** az E28 a commitolt blob nyers bájtjait veti össze a generált kimenettel; a `_lf()`
  normalizálás az E28 összevetéséből kikerült (az E29 sorokra bontásához marad). Új tesztek: CRLF-es commitolt nézet
  LF-es generált kimenettel piros; CRLF-es marker-blokk piros; a munkafa-tartalék LF-et ad és jelzi, hogy nem
  blob-összevetés. **Megjegyzés (a második javítókör, F116.14):** ez a három teszt a `_e28_commitolt`-ot mockolja
  (CRLF-es fixture-t ad vissza), ezért a `_e28_commitolt` blob-ága (a `git show` nyers visszaadása) nem volt tesztelve. A tesztfixture-ök sorvég-hűen íródnak (`_ir_nyers`), így Windowson sem lesz CRLF az LF-ből.
  A nyers összevetés a mai main-en nem fordít pirosra semmit (E28 üres listával 0 találat; a három marker-blob tisztán LF).
- **F116.12 (robusztusság, alacsony):** a záró marker nélküli nyitó marker `general.marker_par_keres`-féle
  `ValueError`-ját az E28 elfogja: HIBA-találat (fájl, cél-kulcs, a hiba szövege, javító parancs), a futtató és a
  többi szabály fut tovább. Teszt: `test_negativ_nyito_marker_zaro_nelkul_hibatalalat_nem_kivetel`.
- **Mérés:** `test_szabalyok.py` 141 OK, `test_tanulmany.py` OK; `futtat.py --teljes`: E28 0 találat („E28: 0 migrált
  nézet”), E29 0 találat, kilépés 0; a három `general.py --cel … --ellenoriz` zöld (naplo 4/4, index, nyitott);
  `python eszkozok/feladatok.py ellenoriz`: 136 brief, 0 hiba, 0 figyelmeztetés.

## 6. Második javítókör (F116.14)

`scope=test_szabalyok.py; a db57480d-s szabalyok.py ideiglenes visszaállítása commit nélkül | forras=manual (CLI-futtatás) | ts=2026-10-18`

- **Tesztlefedettség:** új teszt, `E28Teszt.test_valodi_blob_ag_nyers_bajtokat_ad_nem_mockolt_commitolt`: a
  `_e28_commitolt` **nincs mockolva**; a `subprocess.run` (a `git show`) CRLF-es bájtokat ad vissza (commitolt
  CRLF-blob). A teszt ellenőrzi, hogy a visszaadott szöveg megőrzi a CR-t (`_e28_commitolt` == a nyers dekódolt
  bájtok), és hogy az E28 piros (1 találat, a CR látszik a jelentésben); a generátor-hívás és a marker-cél helyettesített.
- **Igazolás, hogy a teszt a régi kódon bukik:** a `db57480d`-s `szabalyok.py` ideiglenes visszaállításával (commit
  nélkül, utána visszacserélve) a `test_szabalyok.py` 142 tesztjéből 3 bukik: az új
  `test_valodi_blob_ag_nyers_bajtokat_ad_nem_mockolt_commitolt` (FAIL: a régi `_lf()` eltávolítja a CR-t),
  a `test_munkafa_tartalek_lf_es_jelzi_hogy_nem_blob` (FAIL) és a
  `test_negativ_nyito_marker_zaro_nelkul_hibatalalat_nem_kivetel` (ERROR: kezeletlen `ValueError`). A javított
  kódon mind a 142 zöld.
- **Docstring:** az `e28_generalt_nezet_egyezes` docstringje („LF-normalizálva”) a nyers bájt-összevetésre igazítva.
