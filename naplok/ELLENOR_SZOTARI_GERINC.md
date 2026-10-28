<!-- A jelentést a fuggetlen-ellenor subagent válaszként adta vissza (fájlíró eszköze nem volt). A végrehajtó 2026-10-28-án tartalmi változtatás nélkül mentette. -->

ELTÉRÉS: 6 tétel

# Független ellenőrzés: #131 SZOTARI_GERINC (pilot: ISTENTISZT-001)

**Brief:** `F131_SZOTARI_GERINC_BRIEF.md` · **Tartomány:** `3c6cb87e..8c042f53` (36 commit, ebből 3 main-beolvasztás) · **Ág:** `ccr-6dc5ac47-lksrko`

Eltérések a szerepszabálytól:
- Nemcsak a `git diff`/`git log`/`lekerdez.py`/`futtat.py` futott: a `git diff` kimenetét csak olvasó szűrők (grep, cut, sort, comm, join, awk, wc) is feldolgozták.
- Hat ideiglenes fájl készült a scratchpadban. Repófájlt az ellenőr nem írt.

A brief nem számozza G/D-ként a pontjait. Az ellenőrzés alapja ezért a brief 5. lépésének pontjai, a 7. szakasz elfogadási feltételei és a DT-F131a–l döntés.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | – | A tényleges modell `claude-opus-5-5`, a kért `opus`. A diff új/módosított tábláiban nincs `modell` oszlop (`szotar_szakasz_cimke`, `bdb_forras_javitas`, `bdb_vers_jelentes`). A `forditasok.tsv` nem változott (`git diff --numstat`). A napló 5.5 `claude-opus-5-5`-öt ír. |
| 5.1 Séma ↔ tábla ↔ generátor | OK | `adat/SEMA.md` 2.29, 2.31, 2.40 | `git diff -- adat/SEMA.md adat/szotar_szakasz_cimke.tsv`: a 2.40 oszlopai egyeznek a tábla fejlécével. A 2.29-ben a `forras_javitas` és a tartomány utáni folytatás, a 2.31-ben a `hivatkozas_kezi` dokumentálva. |
| 5.2 A 7 lap nulla-diff | git-szinten OK; újragenerálva NEM ELLENŐRIZHETŐ | `lexikon/` | `git diff --numstat 3c6cb87e..8c042f53`: a `lexikon/` alatt csak az `ISTENTISZT-001_TUDOMANYOS.md` változott (+243/−652). A `nulladiff.sh` nem megengedett parancs. |
| 5.3 Minden címke mögött létező útvonal | OK | `adat/szotar_szakasz_cimke.tsv:2-9` | Grep a `bdb_szakaszok.tsv`-ben: H7121 `Qal/2/c` (8, 9. sor), `Qal/3/-` (11.), `Qal/3/b` (13.); H8034 `-/3/-` (7.), `-/4/-` (10.). A Thayer `-/1/-` és `-/5/-` megvan (`thayer_vers_jelentes` 15, 37–43). |
| 5.4 Nincs `forditasok.tsv`-írás | OK | – | `git diff --numstat`: a fájl nincs a változottak között. |
| 5.5 Tiltott keretezés 0 | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:64-329, 438-786` | Grep `(?i)eltér\|máshová sorol\|NEM invokáció\|szemben a BDB\|a BDB szerint nem`: a két blokkban 0 találat. A többi találat a kizárt, a „Miért fontos”, az LXX és az értelmezés részben van. |
| 5.6 Minden kiemelés mögött tábla-sor | OK | `:556, 578, 638, 642, 456, 469` | Grep a `bdb_vers_jelentes.tsv`-ben: H7121 92–97, 99, 100, 129, 130; H8034 116–120, 208, 209 (17 BDB); Thayer 15, 37, 39–43 (7). Egyezik a napló 17/18, 7/7 számával. |
| 5.7 Proveniencia-sorok | OK | napló 4.–7.; táblák | Minden mérésnél áll `scope=…\|forras=…\|ts=…`. Az új 2.31-sor `manual` (SEMA 2.31 szerint). A cimke-sorok `scope=manual\|forras=F131…\|ts=…` alakúak. |
| 7.1 Döntések | OK | `DONTESEK.md:424-433, 440-441` | Az a–l rögzítve. Az f és a g az orkesztrátor döntése, a felhasználó ugyanabban a sessionben megerősítette (szó szerint idézve). |
| 7.1a Döntés-állapot | **ELTÉRÉS** | `DONTESEK.md:424-429` | A DT-F131a–e és h sora „🟢 eldöntve, alkalmazásra vár”, holott az F131.1–F131.4 alkalmazta őket. A brief fejléce `allapot: dontesre_var`, a `kovetkezo` már az 5. lépést nevezi meg. Elavult állapotjelölés. |
| 7.2 Gerinc | OK | `:442-475, 535-653` | A BDB és a Thayer tagolása megvan. A hordozó szakaszok kibontva és magyarul, a többi `<details>`-ben. A G1941 UBS-doménsora 4 kódból áll, az 56.15 `(fordításra vár)` a DT-F131f (3) szerint. |
| 7.2a A `horgonnyal` határ jelölése | **ELTÉRÉS** | `:644-649`; `eszkozok/lexikon_general.py:2192` | Grep `horgony` a lapon: 0. A jelölés csak a kibontott (hordozó) szakaszra kerül; a H8034 `-/5/-` összecsukva áll. Az 5. szakasz a hordozó `-/4/-` határán van, a határ hibája a kibontott szöveget is érintheti. A teszt (`teszt_szotari_gerinc.py:171`) szintetikus, hordozóvá tett `-/5/-` szakasszal fut. A 7. szakasz 2. feltétele az éles lapon nem teljesül. |
| 7.3 tW, TBESH, UBS, Mounce helyén mutató | OK | `:501, 509, 657-685, 713` | Szónézet-mutató és forrásfájl áll. A TBESH egysoros jelentése a DT-F131a (iv) szerint. |
| 7.3a tW-forrásmegjelölés | **ELTÉRÉS** | `:501, 669, 673` ↔ `:1660-1792` | A lap tW-azonosítókat mutat (`kt/call-speakloudly` stb.), és forrásként a `tW_szocikkek.tsv`-t nevezi meg. A tW (CC BY-SA 4.0) sora viszont kikerült az Irodalomból és a kolofon licenctáblájából (`git diff -U0 … lexikon/…`, `@@ -2102`). |
| 7.4 32 sor, két oszlop, ⓘ | OK | `:68-134` | Mind a 32 soron van címke vagy kimondott „*(nincs hozzárendelés)*”, és mindegyiken van ⓘ. |
| 7.4a 1Kir 18:24, H8034-címke | **ELTÉRÉS** | `:77`, `:110`; `lexikon_general.py:1950` | A cella „H8034: név: hamis istenekről · 4” (BDB-példa, 208. sor). A sor tokenje Illés szava: `שֵׁם (shem-)`, „az Úrnak nevét”. A `lekerdez.py igealak H8034` az 1Kir 18:24-re két tokent ad: `Shem` („a ti istenteknek nevét”) és `shem-` (az Úr neve); vö. Károli: „…a ti istenteknek nevét, és én is segítségül hívom az Úrnak nevét”. A BDB-példa versszintű, a generátor nem különbözteti meg a tokent, ezért a hamis istenek jelentése Jahve nevén áll. |
| 7.5 Kiemelés, meg nem találtak | OK | `:651` | A meg nem talált hely listázva (H8034 3. sor, 1Móz 12:8, `fej`). |
| 7.5a „A Thayer a helyet nem idézi” | **ELTÉRÉS** | `:127-128` ([^25], [^26]), `:471` | A Thayer 5. szakasza idézi: „Act 9:14,21; 22:16” (Grep, `thayer_szakaszok.tsv:6252`), a magyar szöveg ugyanígy (`:469`: „**ApCsel 9:14**,21; 22:16”). A `thayer_vers_jelentes.tsv` G1941-sorai (21355–21397) között viszont nincs 9:21 és 22:16. A lap a tábla hiányát a szótár hiányaként mondja ki: hamis negatív. Ugyanaz a hibaosztály, amelyet a DT-F131l a BDB-n javított. |
| 7.5b A gerinc ⓘ-je ellentmond a sor ⓘ-jének | **ELTÉRÉS** | `:616, 651` ↔ `:111` | A gerinc ⓘ-je: „a szótár nem idézi: … 1Kir 18:25” (H7121 és H8034). A [^9] és a DT-F131f szövegpontosítása szerint viszont a BDB a helyet az „1Kin 18:24-25” tartomány belsejében idézi. Ez a lapon is látható (`:556`, `:642`: „**1Kir 18:24**-25”). |
| 7.6 Tiltott keretezés | OK | – | Lásd 5.5. |
| 7.7 CI | OK | – | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 3c6cb87e..8c042f53) --diff-alap 3c6cb87e --diff-fej 8c042f53 --pr-cim "[ELLENŐRZŐ] F131: SZOTARI_GERINC" --esemeny pull_request` → kilépési kód 0. JELENTÉS: E12 (349), E13 (121), E25 (4), E27 (41), E30 (11), E32 (1). E28: 0 („1 migrált nézet”). Előtag nélkül: E16 HIBA, kilépési kód 1. |
| 7.7a `ellenoriz.py` 0 SÉRTÉS, `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | – | Nem megengedett parancs. |
| 7.8 TSV `csv` nélkül; próbarender a repón kívül | OK | – | Grep `import csv\|csv\.` a diff minden `.py`-fájljában: 0. A `generalt_proba/` nincs a változottak között. |
| V1 A 2.29 változása | OK | `adat/bdb_vers_jelentes.tsv` | A `git diff -U0` szűrve: régi 160 616, új 162 054 adatsor; `folytatas` 10 742 → 12 180 (+1 438). A `sorszam` és proveniencia nélküli kulcson 1 sor csak a régiben (H8034 26:35), 1 439 csak az újban (1 438 `folytatas` + 1 `forras_javitas`), 603 Strong. A (strong, poz, nyers) kulcson 35 012 sor kapott más `sorszam`-ot; minden sor `ts`-e új. Egyezik a napló 5.5-tel. |
| V1a `--ellenoriz` bájtazonosság (2.29, 2.31) | NEM ELLENŐRIZHETŐ | – | Nem megengedett parancs. |
| V1b DT-F131k forrás-tényei | OK | `adat/bdb_forras_javitas.tsv:7206` | `lekerdez.py scan H8034 --szakasz "1Móz 26"`: a 26:25 van, a 26:35 nincs. `karoli "1Móz 26:35"`: „…lelke keserűsége”; `karoli "1Móz 26:25"`: „segítségűl hívá az Úrnak nevét”. A forrás „26:35”-öt ír (`bdb_szakaszok.tsv:33920`). |
| V1c DT-F131l, 1Kir 18:26 | OK | `bdb_vers_jelentes.tsv:132951, 150059` | H7121: 100. sor, `, 26` (`Qal/2/c`); H8034: 209. sor (`-/4`). A `kollokacio H7121 H8034` szerint az 1Kir 18:24–26 mindhárom versében együtt állnak. |
| V2 A `hivatkozas_kezi` nem jut a szöveg-nézetbe | kódolvasással OK; a 13. szabály futása NEM ELLENŐRIZHETŐ | `nezet_general.py:111`, `szakasz_bemenet.py:102`, `szabalyok.py:1035` | Mindhárom csak az `allapot=='javitva' and hiba=='hivatkozas'` sorokat alkalmazza; az új sor `kezi`/`hivatkozas_kezi`. |
| V3 Az élő lap = a generátor kimenete | OK | `e28_migralt_nezetek.tsv:2` | Az E28 a lapot újragenerálja és bájtra összeveti: 0 találat. |
| V4 Tesztek (a kiinduló hibák forrása) | NEM ELLENŐRIZHETŐ | – | Futtatni nem megengedett. Diff-alapú érv: a `teszt_bont` 3 hibája a 2.30, a `bdb_szakasz_hu` és a `forditasok` tárgyú tesztekben van, ezeket a diff nem érinti. A `test_eles_sema` értékét az ág 29-ről 30-ra növeli (SEMA 2.40); a main-állapotot az ellenőr nem mérte. |
| A1 Memória vs. lekérdezés | OK | `motivumok/ISTENTISZT-001.md:232-235` | A Thayer 4. ágának új leírása szó szerint a `forditasok.tsv:8010` (sz6) szövege. A „sajtóhiba” lekérdezéssel alátámasztva (V1b). |
| A2 Nyitott tételek | OK | – | A diff nem írja a `NYITOTT_FELADATOK.md`-t. Az N-F131a–g a 6. lépésre vár, a brief szerint még nem esedékes. |
| A3 Tematikus vs. lexikai párhuzam | OK | – | A diff nem hoz új párhuzam-állítást. A Funkció-cellák tartalma változatlan (`@@ -70,67`, csak oszlopok). |
| A4 Remez/Sod | OK | `motivumok/ISTENTISZT-001.md:231-242` | Csak a tagolás tényleírása változott, következtetés nem került be. A Sod-réteget a diff nem érinti. |
| A5 Nevesített tanító | OK | – | Nem került be új tanító. A szótárszöveg Geseniusa és Winere a forrás része. |
| A6 E12–E15 | tartalmilag OK; a változás mértéke NEM ELLENŐRIZHETŐ | – | Az E12 és az E13 találatai a generált lapon vannak. Az E13 a szótári idézetek átírás nélküli héber/görög szövege, ami idézetben elfogadható. Az E14 és az E15: 0. A main-hez mért változás nem mérhető, mert a `futtat.py` a munkafát olvassa. |
| CI-jelentés egyezése | OK | napló 7. | A végrehajtó leírása (kilépési kód 0; JELENTÉS: E12, E13, E25, E27, E30, E32) egyezik az ellenőr futtatásával. Az E32 találata (`bdb_vers_jelentes.py:345`, DT-F99i) nem ebből az ágból jön: `git diff -U0 … eszkozok/ \| grep DT-F99i` üres. |
| L1 Kiszűrt és törölt sorok | OK | – | 2.29: 1 kulcs törölve (javított vers), +1 439 sor, 35 012 `sorszam`-eltolódás, minden sor `ts`-e új. 2.31: +1 sor, a 2 fejlécsor hash-e frissült. `szotar_szakasz_cimke`: új tábla, 8 sor. A lexikonlap: −652/+243 sor. |
| L2 Kulcstartomány-lefedettség | OK | – | A 2.29-ből nem tűnt el Strong. Csak 1 régi kulcs hiányzik (H8034), az javított alakban megvan. |
| L3 A nulla-diff hatóköre | – | – | Igazolt: a 7 lap git-szinten változatlan, az ISTENTISZT-001 = generátor (E28). Nem igazolt: a 7 lap újragenerálva, és a `bdb_szelet.py` hatása az olvasó-szerverre (szónézet, `pardes.db`); a napló szerint a szerver-tesztek régi adatbázison futnak. |
| L4 Sorszám-Δ (E17, DT3) | OK | napló 5.5 | `adat/bdb_vers_jelentes.tsv` +1 438 (≥ 10; kategória-napló: 5.5, darabszámokkal). `adat/bdb_forras_javitas.tsv` +1. `adat/szotar_szakasz_cimke.tsv` +8 (új tábla). `konkordancia/` 0. Az E17 nem szerepel a `futtat.py` kimenetében. |
| L5 A brief ⛔ pontjai | OK | `8a940472`, `6cba98d0`, `5f0bfacd` | `git log`: megállás a 0.3-nál, a 3.1-nél (két kör) és a 4-nél. Merge nincs. Az `adat/tiltott_fordulatok.tsv` írása (F131.3.5) az `ir`-en kívül volt, de a main (F142.38) ugyanezt tartalmazza, a nettó diff 0. |

**Eltérések súlyossági sorrendben:**
1. **7.4a:** az 1Kir 18:24-en a H8034 „név: hamis istenekről · 4” címkéje Illés Jahve-nevére vonatkozó tokenjén áll. A BDB-példa versszintű, nem a sor tokenjére vonatkozik.
2. **7.5a:** a lap azt állítja, hogy a Thayer nem idézi az ApCsel 9:21-et és 22:16-ot, pedig a Thayer 5. szakasza mindkettőt idézi. A hely csak a `thayer_vers_jelentes.tsv`-ből hiányzik.
3. **7.5b:** a gerinc ⓘ-je („nem idézi: 1Kir 18:25”) ellentmond a sor ⓘ-jének, amely szerint a hely a tartomány belsejében idézett.
4. **7.2a:** a `horgonnyal` határ (H8034 `-/5/-`) az éles lapon nincs jelölve, csak szintetikus teszt fedi.
5. **7.3a:** a tW-azonosítók és a forrásfájl a lapon maradtak, de a tW kikerült az Irodalomból és a licenclistából.
6. **7.1a:** elavult állapotjelölés a DT-F131a–e, h sorokban és a brief `allapot` mezőjében.
