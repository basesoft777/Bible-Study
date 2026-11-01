# F148 UJ_MOTIVUM_VEDOKORLAT — napló

*Brief: `F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md` · ág: `claude/f148-vedokorlat-4b117b` · alap: `origin/main` b23fe651*

## 0. Modell-ellenőrzés és mérés (2026-10-29)

**Modell.** Kért: `opus` (a brief `modell` mezője). Tényleges: `claude-opus-5-5`. Egyezik.

Mérőszkript: `naplok/F148_meres.py` (`split('\t')`, csak olvas; a (iii) ponthoz a lapokat repón kívüli ideiglenes könyvtárba rendereli, `--forditas`).

### 0.1 A #123 ALVIL-001 PR-ja a main-en

`f711291d Merge pull request #513 from basesoft777/claude/f123-alvil-adat` — teljesül. (Utána: #514, F121 TBESG G0086.)

### 0.2 Kitöltöttség az `adat/elofordulasok.tsv`-ben

| id | sor | `jelentes_szam` | `karoli_szo` | `lexikon_entry_id` | `lexikon_szotar` |
|---|---|---|---|---|---|
| ALVIL-001 | 72 | 13 | 72 | 13 | 13 |
| ANTROP-001 | 8 | 0 | 8 | 0 | 0 |
| HAMART-001 | 52 | 26 | 0 | 42 | 42 |
| HODIT-001 | 33 | 0 | 33 | 0 | 0 |
| ISTENTISZT-001 | 33 | 33 | 33 | 33 | 33 |
| KIRALY-001 | 9 | 4 | 9 | 5 | 5 |
| MENNY-001 | 9 | 0 | 9 | 0 | 0 |
| TEREMT-001 | 42 | 0 | 42 | 0 | 0 |
| TEREMT-002 | 3 | 0 | 3 | 0 | 0 |

`scope=adat/elofordulasok.tsv (9 id, 261 sor) | forras=naplok/F148_meres.py | ts=2026-10-29`

Eltérés a brief táblájától: az ALVIL-001 `jelentes_szam`-ja 0 → 13 (a #513 óta). A 13 kitöltött sor: 5 H7585 (Jób 17:12 `1`, Zsolt 49:15 `2.a`, Zsolt 88:4 `1`, Ez 31:16 `2.a`, Hós 13:14 `4`) és 8 G0086 (`2`). A többi **59 sor (mind H7585)** `lexikon_szotar`, `lexikon_entry_id` és `jelentes_szam` nélkül áll.

### 0.3 Gerincen álló motívumok

`SZOTARI_GERINC_MOTIVUMOK = {'ISTENTISZT-001', 'ALVIL-001'}` (`eszkozok/lexikon_general.py:1779`).

Várható kivétellista: ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 — és a mérés szerint a **TEREMT-002** is kérdés (l. ⛔ A/3).

### 0.4 A négy új szabály próbafutása (kivétellistával, a brief kiinduló mintáival)

| szabály | ISTENTISZT-001 (gerinc) | ALVIL-001 (gerinc) | kivétellistás motívumok (JELENTÉS) |
|---|---|---|---|
| 18. gerinc-Strong címkéje | 0 | **59 SÉRTÉS** (a 0.2 59 sora: nincs `jelentes_szam`, nincs mire leképezni) | — |
| 19. kötelező mezők | 0 | **59 SÉRTÉS** (`lexikon_szotar`/`lexikon_entry_id`/`jelentes_szam` üres) | ANTROP 8/8, HAMART 52/52, HODIT 33/33, KIRALY 5/9, MENNY 9/9, TEREMT-001 42/42, TEREMT-002 3/3 hiányos sor |
| 20. `jelentes_hu` (kiinduló minták) | **26 SÉRTÉS**, mind az `invokál` mintán: „invokálni, segítségül hívni” | 0 | 0 |
| 21. lap tisztasága | l. 0.5 | l. 0.5 | — |

A 20. szabály 26 találata **hamis pozitív**: az „invokálni” a BDB *invoke* glosszájának magyarja, a szó jelentése, nem funkció-címke. A brief „invokáció mint értelmező címke” mintája tehát főnévi alakra szűkítendő. A többi kiinduló minta (`(NEM`, „tagadó szerkezet”, „vádjaként”, „motívum”, „funkció”, `tiltott_fordulatok.tsv`) 0 találatot ad a teljes táblán. A kötelező negatív teszt esete (1Kir 18:25–26 „Baál nevével”) egyik mintán sem akad fenn. Figyelemre méltó, minta nem fogja: 1Kir 18:24 „annak konkrét kérésére, hogy Jahve mutassa meg hatalmát” (az N-F131a köréhez tartozhat; az ISTENTISZT-menet dolga, nem e feladaté).

### 0.5 A 21. szabály mintái a `lexikon/` lapjain

Létező tételek: 385 `| DT<n> |` sor a `DONTESEK.md`-ben, 49 `**N<n>` tétel a `NYITOTT_FELADATOK.md`-ben.

| lap | helyőrző (`DT-F`/`N-F`) | „Kézzel írandó” | „a(z)” | `(fordításra vár)` | DT-hiv. (nem létező) | N-hiv. (nem létező) |
|---|---|---|---|---|---|---|
| ALVIL-001_TUDOMANYOS | **3** (`DT-F123e`) | 0 | 0 | 0 | 14 (0) | 0 |
| ANTROP-001_TUDOMANYOS / _TORZSCIKK | 0 / 0 | 0 | 0 | 0 | 1 / 0 (0) | 0 |
| HAMART-001_TUDOMANYOS / _TORZSCIKK | 0 / 0 | 0 | 0 | 0 | 2 / 0 (0) | 0 |
| HODIT-001_TUDOMANYOS / _TORZSCIKK | 0 / 0 | 0 | 0 | 0 | 1 / 0 (0) | 0 |
| ISTENTISZT-001_TUDOMANYOS | 0 | 0 | 0 | 0 | 41 (0) | 2 (0) |
| KIRALY-001_TUDOMANYOS / _TORZSCIKK | 0 / 0 | 0 | 0 | 0 | 1 / 0 (0) | 0 |
| MENNY-001_TUDOMANYOS / _TORZSCIKK | 0 / 0 | 0 | 0 | 0 | 1 / 0 (0) | 0 |
| TEREMT-001_TUDOMANYOS / _TORZSCIKK | 0 / 0 | 0 | 0 | 0 | 1 / 0 (0) | 0 |

A lapszám: **8 TUDOMANYOS + 6 TORZSCIKK** (az ALVIL-001-nek és az ISTENTISZT-001-nek nincs törzscikke); a brief „7 törzscikk”-je 6.

**A `DT-F123e` a main-en.** A `DONTESEK.md`-ben a main-en ma is helyőrzővel áll a `DT-F123b`…`DT-F123m` és a `DT-F131r`, összesen 82 `| DT-F…|` sor. A `szamkiosztas` Action a #513, #514 és #515 merge-e után mind `cancelled` (`gh run list --workflow szamkiosztas.yml`). Ráadásul a korábbi kiosztó commit (`c14bde29`: `DT-F141a → DT407` …) számai nincsenek a táblában: a legmagasabb `DT406`, a `DT-F141a` ma is helyőrző. Ez a #141 (DT-F141a) tárgya; e feladaton kívül esik, de a 21. (i) main-szintű SÉRTÉS-ét közvetlenül érinti.

**(iii) fordítatlan egység — a lista_keszit és a lap jelölései:**

| id | `forditas_ehhez` hívás | hiányzó egység | `(fordításra vár)` a renderelt lapon |
|---|---|---|---|
| ALVIL-001 | 10 | **4** (BDB H7585 `1`/`2.a`/`4`, Thayer G86 `2`; `forditas_hu`) | **0** |
| ANTROP-001 | 113 | 99 | 100 |
| HAMART-001 | 169 | 152 | 155 |
| HODIT-001 | 17 | 17 | 17 |
| ISTENTISZT-001 | 26 | **6** (SECE_G/H, TBESH `forditas_hu`) | **0** |
| KIRALY-001 | 59 | 52 | 53 |
| MENNY-001 | 77 | 77 | 77 |
| TEREMT-001 | 12 | 8 | 8 |

A brief (iii) egyenlősége („hiányzó = jelölés”) egyik lapon sem pontos, és a két gerinces lapon 4/6 ≠ 0. A gerincmódban a generátor a hiányzó `forditas_hu`-t meghívja, de az eredményt nem írja ki angolul (a lap más forrásból ad magyart, vagy a cellát kihagyja). Ezért a hívásszám nem a lapon álló fordítatlan egységek száma. Ez az N-F148a korlát másik oldala: a mérőszám a hívást látja, nem a kiírást.

`scope=lexikon/*.md (14 lap) + render ideiglenes könyvtárba (8 id) | forras=naplok/F148_meres.py --forditas | ts=2026-10-29`

### 0. ⛔ — döntési pontok

**A — ALVIL-001: 59 gerinces sor kötelező mező nélkül (0.4, a brief szerint megállás).**
A gerincen álló ALVIL-001 59 H7585-során nincs `lexikon_szotar`/`lexikon_entry_id`/`jelentes_szam`: a 18. és a 19. szabály 59–59 SÉRTÉS-t adna. A brief szerint a szabály nem lazul, a sor nem kerül kivételre. Mért: mind az 59 sornak **pontosan egy** BDB-példa-útvonala van (`bdb_vers_jelentes.tsv`, `bdb_peldak`). A gerinc ma ebből címkéz, ezért a lap helyes; csak az adat nem explicit.
- (1) **a #123 kiegészítő adatjavítása:** a 59 sor `BDB`/`H7585`/`jelentes_szam` értéke a BDB saját példahelyéből, gépileg, proveniencia-sorral; a #148 szabály-commitjai addig az ágon maradnak, a PR ez után mergelhető. *Javaslat.* Az adat explicit lesz (CLAUDE.md 3. szabály), és a 3. lépés eszköze ugyanezt az utat ellenőrzi.
- (2) a 19. szabály elfogad üres `jelentes_szam`-ot, ha a BDB saját példája egyértelműen kijelöli a szakaszt — lazítás, a brief kizárja.
- (3) az ALVIL-001 visszakerül a kivétellistára — a brief kizárja, és a lapot visszaállítaná.

**A/3 — TEREMT-002 a kivétellistán?** A brief kivétellistája a TEREMT-002-t nem sorolja fel, a 0.2 szerint viszont 3/3 sora hiányos. Ha nincs a listán, a 19. szabály a main-en 3 SÉRTÉS-t ad. *Javaslat:* a TEREMT-002 a #12-ig a kivétellistán áll; a #12 első adatcommitja veszi le (ez a fordított irány pilotja, nem régi motívum). Másik lehetőség: a #148 merge-e a #12 adat-PR-ja után.

**B — DT-F148a (a kivétellista helye).** *Javaslat (változatlan): (1) kódbeli konstans* (`GERINC_KIVETEL_MOTIVUMOK` a `lexikon_general.py`-ban, az `ellenoriz.py` importálja).

**C — DT-F148b (tagolatlan szócikk).** *Javaslat (változatlan): (3), mellette (1).* A mérés nem talált gerinces sort tagolatlan entryvel; a H7585 tagolt (`-/1/-`…`-/4/-`).

**D — DT-F148c (gépi `cimke_hu`).** *Javaslat (változatlan): (1).*

**E — DT-F148d (21. szabály súlyossága), két mért pontosítással.**
- *Javaslat: (2)* — az ágon JELENTÉS, a main-en SÉRTÉS. A main ma **3 SÉRTÉS-t** adna (ALVIL `DT-F123e`), mert a `szamkiosztas` a #513 óta nem futott le (l. 0.5). A #148 merge-e előtt a számkiosztásnak le kell futnia, és az ALVIL-lapot újra kell generálni. Ez a #141/DT-F141a körébe tartozik, külön feladat.
- **(iii) újradefiniálása:** a „hiányzó egység = jelölés” egyenlőség helyett **a kiírt angol szöveg mérése**: a renderelés alatt a generátor `FORDITASRA_VAR`-kiírását és a `forditas_ehhez`→`None` utáni tényleges angol kiírást is naplózni; SÉRTÉS, ha egy kiírt angol egység jelöletlen. Ha ez a generátorban túl mély, a (iii) a #148-ban JELENTÉS, és az N-F148a nyitott tételként él tovább.

**F — a 20. szabály mintái.** Kódbeli lista az `ellenoriz.py`-ban (nem új `tiltott_fordulatok.tsv`-oszlop); az `invokál` igei alak kimarad, csak a főnévi `invokáció` címke tiltott, mellette a `tiltott_fordulatok.tsv` meglévő mintái. Így a main-en 0 találat; az 1Kir 18:25–26 negatív teszt teljesül.

### 0.6 Újramérés a mai main-en (2026-11-01, a felhasználó „Igen, folytassa” válasza után)

Alap: az `origin/main` beolvasztva (`a4122290`, #517–#531). Ugyanaz a szkript (`naplok/F148_meres.py --forditas`).

| pont | 2026-10-29 | 2026-11-01 | változás |
|---|---|---|---|
| 0.2 kitöltöttség | l. fent | **változatlan** (ALVIL-001 13/72 `jelentes_szam`) | — |
| 0.3 gerinc | kódbeli konstans | **adat**: `adat/funkcio_kapcsolok.tsv` `SZOTARI_GERINC` `aktiv` sorai (ISTENTISZT-001, ALVIL-001; SEMA 2.44, DT427) | a DT-F148a ezt veszi alapul |
| 0.4 / 18. | ALVIL-001 59 SÉRTÉS | **59 SÉRTÉS** (ugyanaz az 59 H7585-sor) | — |
| 0.4 / 19. | ALVIL-001 59 SÉRTÉS | **59 SÉRTÉS** | — |
| 0.4 / 20. | 26 (mind `invokál`) | **26** (mind `invokál`) | — |
| 0.5 (i) helyőrző | ALVIL 3 (`DT-F123e`) | **0** (a számkiosztás lefutott; 402 `DT` sor) | ⛔ E megszűnt |
| 0.5 (ii) „a(z)” | 0 | 0 | — |
| 0.5 (iv) nem létező DT/N | 0 | 0 | — |
| 0.5 (iii) hiányzó / jelölés | ALVIL 4/0, ISTENTISZT 6/0 | ALVIL **4/0**, ISTENTISZT **1/0**; ANTROP 120/122, HAMART 226/239, KIRALY 57/58, a többi egyenlő | a hívásszám továbbra sem a kiírás |

`scope=adat/elofordulasok.tsv, adat/funkcio_kapcsolok.tsv, lexikon/*.md (14 lap), render 8 id-re ideiglenes könyvtárba | forras=naplok/F148_meres.py --forditas | ts=2026-11-01`

**Döntések** (DT-F148a–d a `DONTESEK.md`-ben, helyőrzővel, a felhasználó idézetével): a (4) `funkcio_kapcsolok.tsv`, b (3)+(1), c (1), d (2). Az `invokál`-ra a 0. javaslat (csak a főnévi „invokáció” tiltott) az orkesztrátor közlése szerint elfogadva, és a mérés továbbra is igazolja.

**A kivétel formája (DT-F148a, a végrehajtó javaslata).** A `SZOTARI_GERINC` motívum-sor `allapot`-ja `aktiv` vagy új értékként `kivetel`; sor nélkül a gerinc be van kapcsolva. Kivétel-sor: ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 (a #123 hátralévő hat motívuma), valamint a **TEREMT-002** a #12 adatcommitjáig (A/3: 3/3 sora hiányos; a #12 állítja `aktiv`-ra). A `felfuggesztve` (a SzPA-join szünetelő funkciója) más jelentés, ezért nem azt használom.

**Nyitva marad (a végén ⛔-ként jelentve):**
- **A** — az ALVIL-001 59 sorának kitöltése (`lexikon_szotar`=BDB, `lexikon_entry_id`=H7585, `jelentes_szam` a BDB saját példahelyéből). Ez a kanonikus `adat/elofordulasok.tsv` 59 sorának írása, a brief viszont kizárja („Nincs benne: adatjavítás”; 4. elfogadási feltétel 7.: az `elofordulasok.tsv` nem változik). Ezért nem itt történik. Amíg nem kész, a 18. és a 19. szabály a main-en 59–59 SÉRTÉS-t ad, és a #148 nem mergelhető.
- **(iii)** — a „hiányzó = jelölés” egyenlőség a mért adaton nem tartható (ALVIL 4/0, ISTENTISZT 1/0), és a mérés laponként teljes renderelést kíván, ami az E1 lépésbe nem fér. A 0. javaslat második ága szerint: a (iii) nem SÉRTÉS-szabály. Nyitott tétel lesz (N-F148a), a mérőszkript (`naplok/F148_meres.py --forditas`) adja a JELENTÉS-t.

## 1. A gerinc-kapcsoló megfordítása (F148.1)

A `SZOTARI_GERINC` alapból be; a kivétel a `funkcio_kapcsolok.tsv` `kivetel` sora (7 motívum, l. 0.6). Elfogadás 1.: a 8 lexikonlap és a 6 törzscikk repón kívül renderelve a változás előtt és után bájtra azonos (14/14, `cmp`). Elfogadás 2.: `teszt_szotari_gerinc.py` `test_uj_motivum_kapcsolobejegyzes_nelkul`.

## 2. Ellenőrző-szabályok (F148.2)

A 18–21. szabály a repón (ág-állapot): 18. SÉRTÉS 59, 19. SÉRTÉS 59 (mind az ALVIL-001 H7585-sora, ⛔ A), 20. RENDBEN, 21. RENDBEN. A 19. kivétellistás JELENTÉS-e: ANTROP 8, HAMART 52, HODIT 33, KIRALY 5, MENNY 9, TEREMT-001 42, TEREMT-002 3. A négy szabály egy commitban (közös segédfüggvények és kivétellista-olvasás), a brief tételenkénti commitjától eltérve.

`scope=adat/elofordulasok.tsv, adat/funkcio_kapcsolok.tsv, lexikon/*.md | forras=eszkozok/ellenoriz.py | ts=2026-11-01`

## 3. A szakaszcímke gépi levezetése (F148.3)

`eszkozok/szakasz_cimke_levezet.py`. **Regresszió:** ISTENTISZT-001 33/33, ALVIL-001 13/13 levezetett szakasz azonos a kézi leképezéssel (`naplok/F148_levezetes_ISTENTISZT-001.tsv`, `naplok/F148_levezetes_ALVIL-001.tsv`).

Két mért lelet a megvalósítás közben, mindkettő adatból feloldva, választás nélkül:
- **A binyan.** A H7121 `2.c` a BDB-ben a Qal és a Niph'al alatt is áll; a `jelentes_szam` binyant nem hordoz. Az eszköz a vers héber morfológiájából (`konkordancia/Macula_heber_*.tsv` `morf`, `V`+törzsbetű) szűkít, csak egyértelmű esetben; különben J2. Az ISTENTISZT-001 21 `2.c` sora így Qal.
- **A Macula `karoli` oszlopa elavult.** Az F17-ben (2026-10-18) a #117/#146 előtti versmegfeleltetéssel készült: az Ézs 64:6 MT ott Károli 64:7, a mai `Karoli_versmegfeleltetes.tsv`-ben 64:6 (a TAHOT és az `elofordulasok.tsv` is 64:6). Az eszköz ezért a Macula MT-hivatkozását (`ref`) a mai versmegfeleltetésen át kulcsolja, a `karoli` oszlopot csak a könyv azonosítására használja. A Macula-táblák újragenerálása nem e feladaté; javasolt nyitott tétel (N-F148b).

Jelzések a többi motívumon (tájékoztató, a #123 bemenete): HAMART-001 — J4 binyan-alakú `jelentes_szam` (`Qal pass. ptc.`, `Pi'él`, `Hif'íl` …, 13 sor), J2 `Nif'ál / Hif'íl`, J1 négy helyen (a BDB-példa más pontra mutat), J7 kettő; KIRALY-001 — J7 („pl. Melkisédek”: az első glossza nem glossza). A `--ir` nem futott: a #148 nem ír adatot (elfogadás 7.). Az ALVIL-001 Jób 17:12 és Zsolt 88:4 során J1/J2 jelzés áll (a BDB példahelye -/2/b, ill. -/3/b): ezek a #123 ismert kutatói kérdései (`naplok/F123_cimke_javaslat_ALVIL-001.md`), a kézi döntés szakaszát (`-/1/-`) az eszköz visszaadja.

`scope=adat/elofordulasok.tsv (ISTENTISZT-001, ALVIL-001, HAMART-001, KIRALY-001) + adat/szotar_szakasz_cimke.tsv + adat/bdb_*.tsv + konkordancia/Macula_heber_*.tsv + konkordancia/Karoli_versmegfeleltetes.tsv | forras=eszkozok/szakasz_cimke_levezet.py | ts=2026-11-01`

## 4. SEMA (F148.4)

2.2.2: a `tagolatlan` érték (DT-F148b) és a 18./19. szabály kötelező mezői; 2.40: a gépi levezetés köre és a proveniencia-alak (DT-F148c); 2.44 (F148.1): a `kivetel` állapot.

## 5. Zárás (2026-11-01)

| ellenőrzés | eredmény |
|---|---|
| `python eszkozok/ellenoriz.py` | RENDBEN 17, **SÉRTÉS 2** (18. és 19.: ALVIL-001 59 sora, ⛔ A), KÉZI 2, JELENTÉS 3 |
| `teszt_ellenoriz_vedokorlat.py` | 26 OK |
| `teszt_szakasz_cimke_levezet.py` | 17 OK |
| `teszt_szotari_gerinc.py` | 61 OK |
| `teszt_szerepmatrix.py` | 47 OK (1 kihagyva) |
| `teszt_ellenoriz_11.py` / `_13.py` | 6 OK / 70 OK |
| `teszt_szerep_karoli.py` | 12 OK |
| `python eszkozok/feladatok.py ellenoriz` | 0 hiba |
| CI-emuláció (`eszkozok/ellenorzes/futtat.py --valtozott … --diff-alap origin/main`) | 0 HIBA (a PR-cím `[ELLENŐRZŐ]` előtaggal, E16) |
| 4. elfogadás 7.: `lexikon/`, `adat/elofordulasok.tsv`, `MUNKAMENET.md` | nem változott |

**A merge feltétele (⛔ A):** a 18. és a 19. szabály SÉRTÉS-e az E1 lépést pirosra állítja — a PR-en is, nem csak a main-en (ELLENOR_F148). Az ALVIL-001 59 sorának kitöltése (`BDB`, `H7585`, a `jelentes_szam` a BDB saját példahelyéből, proveniencia-sorral) a #148 merge-e előtt kell, külön adat-commitban vagy a #123 kiegészítő menetében. A `szakasz_cimke_levezet.py` a kitöltött sorokat ugyanezen az úton ellenőrzi.

**Mellékhatás:** a saját `naplok/F148_meres.py` az F148.8-ban átállítva (`LG.gerinc_aktiv`); a `naplok/F131_dbh_meres.py` (archív mérőszkript) a megszűnt `LG.SZOTARI_GERINC_MOTIVUMOK`-ot olvassa; újrafuttatáskor `LG.gerinc_aktiv`-ra állítandó. A brief nem írja, ezért nem nyúltam hozzá.

## 6. Javaslat a #125-nek (a `MUNKAMENET.md` szövege — ezt nem ez a feladat írja)

A brief 6. szakaszának két lépése a megvalósítás szerint pontosítva:

> **C-x. Szakaszcímke (⛔ csak jelzésnél).** Az előfordulás-sorok `jelentes_szam`-ából a szótári szakaszt és a címkét a `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id [ID]` vezeti le (a kimenet: `naplok/F148_levezetes_[ID].tsv`). Jelzés nélkül az `--ir` rögzíti. Jelzésnél (J1 a szótár példahelye más pontra mutat, J2 két pont, J3 üres mező, J4 nincs útvonal, J5 tagolatlan szócikk, J6 minősítő, J7 a címke gépileg nem képezhető, J8 eltérés a kézi leképezéstől) a menet megáll, és a kutató dönt; kitöltés nem gyenge vagy asszociatív anyaggal történik. Az új motívumon a gerinc kapcsoló nélkül fut; az `ellenoriz.py` 18–19. szabálya a hiányzó mezőt SÉRTÉS-ként jelzi.
>
> **C-y. Fordítás a lap előtt.** A lap generálása előtt a `python eszkozok/glossza_lexikon_forditas.py lista --id [ID]` listázza a lap fordítatlan szótári egységeit. A hiányzókat a #121 eszköze és kapui rögzítik az `adat/forditasok.tsv`-be. Ami a lapon fordítatlan marad, `(fordításra vár)` jelölést kap; a gépi mérése nyitott (N-F148a), addig `python naplok/F148_meres.py --forditas`.

## 7. Független ellenőrzés és javítás (F148.8)

`naplok/ELLENOR_F148_UJ_MOTIVUM_VEDOKORLAT.md`: 5 ELTÉRÉS (2 közepes, 3 alacsony). Az 1–4. javítva (mérőszkript, a Macula MT nélküli tartalékága, az `--ir` 17. szabály szerinti kulcsa, a lezárt N-tétel alakja), az 5. (commit-granularitás) dokumentált eltérés. `teszt_szakasz_cimke_levezet.py` 19 OK, `teszt_ellenoriz_vedokorlat.py` 26 OK; a regresszió változatlan.
