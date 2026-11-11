# F185 — A BDB vers → jelentéspont hozzárendelés javítása (BDB_JELENTESPONT_97)

*FELADATOK #185 · végrehajtó: claude-opus-5-5 · ág: `claude/f185-bdb-jelentespont-97` · 2026-11-10*

**Állapot (2026-11-10, a javítókör után):** P1, P2, P4 kész; P3 elmaradt (DT-F185e); P5: a seed-103 vak mérés 188 / 200 (94,0%),
a `BDB_MERT_PONTOSSAG` erre áll (10.); független ellenőrzés: `naplok/ELLENOR_F185.md`, javítókör: 11.
*(Történeti, a 2. szakasz idején: „a P1 részben kész, a P2 nem indult … A P3–P6 nem indult. A seed-103 mintát nem húztam ki.”)*

## 1. P0 — a seed-101/102 beolvasása

Kulcsok: `naplok/BDB_SZELETELO_M2_minta_seed10{1,2}_kulcs.tsv`; kitöltések: `_kitoltott_A.tsv`, `_B.tsv` (a két fájl a 250 sor két
fele, soronként egy kitöltő); ítéletek: `naplok/BDB_SZELETELO_M2_seed10{1,2}_iteletek.md`. Az arany érték a kitöltés, az ítéletek
javításaival: seed-101 M029 → `II -/4/e` (kulcs-ellentmondás, DT657: homonima-szakasz); seed-102 M052 → `I -/5`, rész III
(kitöltő-hiba), M143 bármelyik (kulcs-hiba), M018 kizárva (n = 199). A mérést a repón kívüli eseti szkript végezte (`meres.py`, a
`m2_minta_osszevet.py` `bont`/`fo` függvényeivel és a `--szakasztabla` útvonal-leképezésével), ezért a szám tájékoztató, nem vak.

*Proveniencia: scope=seed-101 véletlen 200, seed-102 véletlen 199 | forras=adat/bdb_vers_jelentes.tsv (mai) + adat/bdb_szakaszok.tsv
(a mai és az F185.1 utáni) + a kitöltések és az ítéletek | ts=2026-11-10.*

| | szeletelő (2.29, mai) | szakasztábla, előtte | szakasztábla, F185.1 után |
|---|---:|---:|---:|
| seed-101 (n = 200) | 188 | 189 | **193** |
| seed-102 (n = 199) | 184 | 186 | **193** (97,0%) |

A szám mindkét mintán a hangolás alapja volt (a szabályok ezek eseteiből készültek), tehát felfelé torzít.

## 2. P1 — szabályjavítás (csak a `bont.py`, sorvágás nélkül)

A JSON-bekezdés = a tábla sora; a sor `sorszam`-ára kulcsolódik 29 311 BDB-fordítás (`forditasok.tsv` `sz<n>`, 7 514 Strong) és a
2.31 kézi horgonyai. Ezért ebben a körben csak olyan szabály került be, amely sort nem vág: a sorok száma (36 621) és határai
változatlanok, csak az `utvonal`, a `jel`, a `jelolo`, az `alszocikk` és a `szoveg` változik (a `jel` + `szoveg` összefűzve azonos
marad). Változott 197 Strong 524 sora; a 2.29 sorai közül 3 294-nek (164 Strong) változik a 2.30-útvonala.

- **N103 (2) — hamis bekezdés-eleji fej (a Thayer K2-jének megfelelője).** A JSON a zárójeles megjegyzés vagy a kereszthivatkozás
  közepén tör bekezdést. Négy jel: (a) lezáratlan „(” az előző bekezdésben + nyitás nélküli „)” a fej után 120 karakteren belül
  (korpusz: 203 bekezdés); (b) „above/below” követi a fejet (61); (c) „see/compare/cf./read(s)” után álló egyetlen törzsnév; (d)
  mondat közepi sorrendsértés (betűvel végződő előző bekezdés, „a”-nál későbbi, a már elért alpontnál nem későbbi betű).
  Az első változatban a (c) minden fejre és a (d) az „a.”-ra is élt: a korpusz-átnézés 16 valódi fejet vesztett el (H1518, H3205,
  H4601, H2850 …), ezért szűkítve.
- **N103, hivatkozással tapadt betűfej:** „see <b>3b. b.</b> qualitatively” (H9004) — a valódi fej az utolsó, sorrendben várt betű.
- **N106 — törzsnév:** a félkövér törzsfejek közül tíz név hiányzott (Hithpa\`lel, Hithpo\`lel, Hithpolel, Po\`lel, Po\`lal, Pol\`el,
  Hothpa\`al, Pi\`lel, Pu\`lal, Pa\`lel); a rövidítés („Hithpa.”, „Po\`l.”) nem fej. Csak a `bont.py`-ban; a szeletelő listája nem
  változott.
- **Nagybetűs csoport a szám alatt** (H5676 „1 … A. … B. … 2”): a csoport a számot nem törli, a következő szám a csoportot zárja.
- **Jelöletlen alcímszó `sub1` nélkül** (héber címszó + félkövér szófaj): a tagolás-állapot nullázódik.

Osztályonként a seed-101/102 esetek (a szakasztábla-útvonalon):

| osztály | javult | nem javult |
|---|---|---|
| N103 (2) hamis fej | M002, M221, M198, M201 (102); M004, M184, M154 (101) | — |
| N103 tapadt betűfej | M184 (101, a fenti mellett) | M057 (101: a fej a bekezdés közepén, sorvágás kellene) |
| N103 (1) bekezdésen belüli, félkövér nélküli fej | — | M056, M194 („) b. without”), M042 (dőlt „1”) (102); M102, M117 (101) |
| N106 törzsfej | M223, M233 (102) | M036, M162 (a „Qal” név hiányzik a forrásban: a 2.31 `jelolo_hianyzik` kézi sora javítja, a mérő útvonal nem olvassa) |
| nagybetűs csoport | M226 (102) | — |
| alcímszó / szakasz | — | M242, M058 (102; a `szakasz` a 2.29-ből jön); M238 (101: mérési leképezés, a „, 22” rossz helyen találva; a tábla sora helyes) |
| rész (`resz`) | — | M203 (101: a tábla `resz` II, a mérő útvonal a 2.29 üres `resz`-ét veszi) |
| könyvnév nélküli hely, közbeékelt fejezet | nem kezdtem el | (M060, M039, M127, M196: a szűrés-/bizonytalan réteg, nem a jelentéspont-mérce) |

A H2403 (N99, HAMART) „see 1 above” hibája a táblában megszűnt (`-/4/a`–`-/4/c`). Ellenőrzés: `teszt_bont.py` (új `F185Fejek`
osztály, 16 teszt; a többi osztály: a `Javitas.test_heber_sorrend_sorok` a változtatás előtt is bukik, a `teszt_szakasz_bemenet.py`
három `EmelesSzakaszag` hibája környezeti — „path is on mount 'C:', start on mount 'E:'”), `teszt_hu_illeszt.py` OK; a
`forras_javit.py` újragenerálva (csak a fejléc-hash változott); az `ellenoriz.py` 17. szabálya és az E19: 0 hiba.

**Egyeztetett eltérés (`ir`):** a `adat/bdb_szakasz_hu.tsv` (a `hu_illeszt.py` generált nézete) a tábla `jel`-változása miatt
192 Strong 600 során változik; a `HuIlleszt.test_osszefuzo_a_mai_adaton_valtozatlan` enélkül bukik, ezért újragenerálva
(`--ts 2026-11-10`). A `bdb_szakaszok.tsv` és a `bdb_szakasz_hu.tsv` minden sorának `ts`-e ezért új (a teljes fájl diffje); a
tartalmi változás a fenti 524, ill. 600 sor. Az `ir`-be került még a `dontesek/uj/` és a `nyitott/uj/` ágfájl. A lapokat nem
generáltam újra; a `KETRETEGU_BDB_KARTYA` és a `BDB_MERT_PONTOSSAG` nem változott.

## 3. Szivárgás a seed-101/102 vak lapjain

A vak lap oszlopai (`azon strong poz nyers kornyezet` + üres kitöltendők) gépi útvonalat, szakaszt vagy törzset nem adnak. Két
gépi elem van benne: (1) a ⟦…⟧ jelölő a szeletelő hivatkozás-kinyeréséből (a könyv/vers mérést érinti, a jelentéspontot nem);
(2) a `kornyezet` a szeletelő `lapit()` alakja („1.a” → „1. a.”), ez a jelölőt szóközzel választja el, tagolást nem árul el. A
jelentéspont-tagolás nem szivárgott; a mérvadóságot az érinti inkább, hogy mindkét minta a javítás hangolási alapja lett.

## 4. Seed-103: eljárás és kapu (rögzítve a mintavétel és a kitöltés ELŐTT)

*Az orkesztrátor döntése szerint (2026-11-10) a seed-103 az egyetlen vak mérés, megismétlés nélkül; ha 97% alatt marad, a mért
szám kerül a lapra „mért” jelöléssel, és a P3 elmarad (erről az orkesztrátor dönt). A #186 seed-204 eljárásának mintájára.*

### 4.1 Mit mérünk

Az `adat/bdb_vers_jelentes.tsv` (2.29; a mintavételkori állapot, a jelentéspont forrása a szakasztábla, DT-F185a) egy sora: egy
BDB-szócikk egy igehely-hivatkozása. Két mutató, külön számmal:
- **könyv/vers:** az `mt_vers` (Károli-könyvrövidítés + MT fejezet:vers); szűrt (nem bibliai) sornál üres, ott a kitöltő
  „alhivatkozás” ítélete egyezik;
- **jelentéspont:** `szakasz` (római homonima-szám; a `h:` alcímszó-címke üresnek számít) + `resz` + `utvonal`. Az összevetés
  az `m2_minta_osszevet.py` szabálya: a törzsnévben „`” = „'”; „fej” = „tagolatlan” = „<törzs>” (= „<törzs>/-”); a fő mutató a
  zárójeles szintet („(2)”, „(c)”), a nagybetűs csoportot (`A`–`H`) és a görög betűs szintet elhagyja (DT657 (a)); a római
  szakasz és a rész pontosan egyezzen.

### 4.2 A minta

`naplok/F185_minta103.py`: 200 egyszerű véletlen sor a 2.29 összes sorából (`random.Random(103)`, (strong, sorszam) szerint
rendezve), a seed-99/100/101/102 kulcsainak sorai kizárva; azonosító `N001`–`s103-N200`. Rétegzés nincs (a seed-101/102 eljárása).

### 4.3 A kitöltés (vak, két független kéz)

- **Két független kitöltő, mindkettő Opus** (A és B), **mindkettő mind a 200 sort** kitölti (kitöltőnként legfeljebb két köteg,
  a köteg Strongonként zárt); egymás eredményét nem látják.
- **Amit kapnak:** a vak munkalap (`naplok/BDB_SZELETELO_M2_minta_seed103_vak.tsv`: `azon`, `strong`, a hivatkozás nyers alakja,
  `jelolve`, a TSV-szöveg ±100 karakteres környezete) és a szócikkek **nyers forrásbekezdései**
  (`naplok/BDB_SZELETELO_M2_minta_seed103_szocikkek.txt`: a `DictBDB.json` `<p>` bekezdései sima szövegként, gépi vágás és gépi
  döntés nélkül; a mért hely előtt `⟦azon⟧`; a szöveg az utolsó jelölt bekezdés utáni bekezdésnél véget ér). Ha a sorhoz nincs
  jelölő (`jelolve` = `nem`), a helyet a környezet szerint keresik meg.
- **Amit nem láthatnak:** a kulcsot, a 2.29-et, a 2.30-at, a 2.31-et, a `bdb_szelet.py`-t, a `bont.py`-t, és a repó más táblázatát
  sem olvashatják.
- **Amit kitöltenek** (a seed-102 vak lapjának szabályai szerint): `konyv_mt` (Károli-rövidítés és MT fejezet:vers; nem bibliai
  helynél „alhivatkozás: <ok>”); `jelentespont`: a BDB tagolása szerinti hely — római homonima-szám, ha a forrás a címszó előtt
  kiírja (a fő címszónál is: „I fej”, „II Hiph`il”), törzs, számozott jelentés, alpont (pl. „II Qal/2/a”, „-/1/b”), vagy „fej”
  (címsor, nyelvi háttér, alaktan), vagy „tagolatlan”; a római számos fő tagolás a `resz` oszlopba („I. of man … II. of God …”);
  a szócikk belsejében héber címszóval álló római fej címszó-szakasz (a jelentéspont elején); a jelöletlen második címszó
  szakasza római szám nélkül; a kereszthivatkozásban álló jelölő („see 1 above”, „compare Pi`el”) nem fej; `megjegyzes`:
  bizonytalanság, forráshiba gyanúja.

### 4.4 Az arany érték és az eltérések

- Ahol **A = B**, az az arany érték (a kapu számát ítélet nem változtatja; ha a végrehajtó a forrás alapján kitöltő-hibát lát,
  az külön, tájékoztató számként áll).
- Ahol **A ≠ B**, soronkénti ítélet a forrásszöveg alapján, idézettel (a végrehajtó; aki dönt, nem ellenőriz — a független
  ellenőrzés a `fuggetlen-ellenor`-é). Kategóriák: hozzárendelés-hiba, kitöltő-hiba, forrás-hiba (a forrás maga hibás: a gépi
  kimenet hibásnak számít).

### 4.5 A mutatók és a kapu

- **Mutatók:** a gépi kimenet egyezése az arany értékkel, **nyers számmal (x / 200)** és **Wilson-féle 95%-os
  konfidencia-intervallummal**, külön a könyv/versre és a jelentéspontra; tájékoztatóul A-ra és B-re külön, és a
  `bizonyossag` szerint (`biztos` / `ketes`) külön.
- **A kapu (előre rögzítve):** jelentéspont **≥ 194 / 200** (97%), és könyv/vers ≥ 198 / 200 (99%, DT658). A kapu a
  pontbecslésre vonatkozik; a CI a jelentésben áll.
- **Következmény:** ha teljesül, a „próba” jelölés lekerül, a szó-lapon (`blokkok.py` `BDB_MERT_PONTOSSAG`) az új mért szám CI-vel;
  ha nem, a mért szám kerül a lapra „mért” jelöléssel, ismételt mérés nincs (orkesztrátori döntés, 2026-11-10).

## 5. P1 vége, forrásváltás, P2 (F185.3–F185.4)

*Döntések: DT-F185a (A) a szakasztábla a forrás; DT-F185b (a) sorbelső fej-oszlop (orkesztrátori döntések, 2026-11-10, a
felhasználó delegálásával). Takarékos menet (a felhasználó szava, 2026-11-10): ami kétes, `ketes` jelölést kap, nem hangolok
tovább, a seed-101/102-n egyetlen záró tájékoztató szám.*

### 5.1 A 2.30 szabályai (a 2. szakaszon túl)

- **Sorbelső fejek (N103 (1), K1)** — `belso_fejek` oszlop (SEMA 2.30): a bekezdés közepi, félkövér nélküli, sorrendben várt
  betű-, szám- és törzsfej, a kereszthivatkozással tapadt betűfej („3b, c. c.”), és a 2.31 `jelolo_hianyzik` kézi sorai.
  A korpuszon 56 fej 43 Strongban (H3452 „) b. without article”, H5066 „, 1 human subject”, H0539 „Niph`al … 1.carried”,
  H4994 „3b, c. c.”, H0559 „Qal … 263.1Say”); a 2.31 sor eleji kézi javítása a H3318 „Qal”-ját is adja.
- **Homonima-szám:** a félkövér nélküli római szám a héber címszó előtt („I. מֶ֫לֶךְ noun”) a `szakasz`; a glossza előtti „I.”
  fő tagolás (`resz`), nem homonima (H3824 „I. seldom of things”).
- **A lefokozott fej szövege változatlan:** a `jel` + `szoveg` összefűzve ugyanaz, mint előtte (a fordítások hash-e erre számol).
  **Kötelező teszt** (`teszt_bont.py` `test_forditasok_kulcsai_valtozatlanok`): a `forditasok.tsv` 29 311 BDB `sz<n>` sorának
  kulcsa megvan, és a szakasz-nézet hash-e a sor `forras_hash`-ével egyezik — előtte és utána is 29 311 / 29 311.
- **Nem javítva (`ketes` vagy nyitott):** a könyvnév nélküli hely és a közbeékelt, nem létező fejezet (a seed-102 M060, M039,
  M127, M196) a mai óvatos szabály szerint `orokles_hibas` okkódot kap, amely a kártyán és az olvasóban gyenge jelölés; új
  szabály nem készült (a könyv/vers mérce a seed-101/102-n 99,5% fölött). N-F185c.

### 5.2 A forrásváltás (DT-F185a (A); egy szabály, egy hely)

A vers → jelentéspont döntés egyetlen helye a 2.29 generátora; minden fogyasztó (lapgenerátor, olvasó, #104 kártya) a 2.29-et
olvassa, a szeletelő jelentéspontját sehol máshol nem használja (`grep`: a `bdb_szelet.jelentespont`/`csomopont_savok` hívója
csak a `bdb_vers_jelentes.py` és a régi `eszkozok/olvaso_mockup/bdb_kinyer.py` mockup).

| fájl | függvény | változás |
|---|---|---|
| `eszkozok/olvaso_szerver/bdb_vers_jelentes.py` | `general`, új `tabla_betolt`, `TablaPont`, `_ut3`, `tanu_elter` | a `szakasz`/`resz`/`utvonal` a 2.30-ból (a hivatkozás a táblaszövegre illesztve); a szeletelő csak hivatkozás-kinyerés, csoport és tanú; új `bizonyossag` oszlop; a fejléc a 2.30 hash-ét is hordozza |
| `eszkozok/bdb_vj_szabaly.py` (**kártya-fájl**, a #104 kártyája és az olvasó közös szabálya) | `vj_bizonytalan`, új `BIZONYTALAN_PONT` | a `ketes` jelentéspont gyenge jelölést kap („vonatkozhat”) |
| `eszkozok/bdb_jelolt/bont.py` | `strong_sorok`, új `belso_fejek`, `kezi_jelolok`, `hamis_fej_kornyezet`, `hivatkozas_fej`, `alcimszo_nyito` | a 2.30 szabályai |

A `lexikon_general.py` és az `olvaso_szerver/blokkok.py` kódja nem változott (a 2.29-et olvassák). Az olvasó BDB-blokkja a
szeletelő bontását **megjeleníti**, és a 2.29 sorait (szakasz, útvonal) ennek csomópontjaihoz köti: ahol a tábla pontja a
szeletelő csomópontjai között nincs, a sor a blokk elején, szövegesen áll (a meglévő „nem azonosítható” út). Ez megjelenítési
kérdés, nem jelentéspont-döntés.

### 5.3 P2 — bizonyosság

A szabály a SEMA 2.29 `bizonyossag` sorában áll: `ketes`, ha (a) a hivatkozás nem illeszthető a táblaszövegre (`jp_illesztes`),
(b) a szeletelő mint független tanú más pontot ad (`jp_tanu_elter`), (c) a hely szakaszhatáron áll (`jp_hatar`); különben
`biztos`. A teljes 2.29-en (162 053 sor): `biztos` 146 679, `ketes` 15 374 (`jp_tanu_elter` 12 917, `jp_illesztes` 2 062,
`jp_hatar` 395).

### 5.4 Záró tájékoztató szám (nem vak; a seed-101/102 a hangolás alapja)

*Proveniencia: scope=seed-101 véletlen 200, seed-102 véletlen 199 | forras=adat/bdb_vers_jelentes.tsv (F185.4) + a kitöltések és
az ítéletek; eseti meres2.py | ts=2026-11-10.*

| | jelentéspont | `biztos` sor helyes | `ketes` sor helyes |
|---|---:|---:|---:|
| seed-101 | **190 / 200** | 183 / 184 | 7 / 16 |
| seed-102 | **192 / 199** | 183 / 183 | 9 / 16 |

## 6. Seed-103: a minta és a vakság-próba (a kitöltés előtt)

*Proveniencia: scope=adat/bdb_vers_jelentes.tsv (F185.4) | forras=naplok/F185_minta103.py, naplok/F185_vaksag_proba.py +
konkordancia/lexikonok_nyers/DictBDB.json | ts=2026-11-10.*

- **Minta:** sokaság 161 065 sor (a korábbi minták 988 sora kizárva); 200 sor, 183 szócikk; a mintavételkori bizonyosság:
  `biztos` 181, `ketes` 19 (a kulcsban; a kitöltőnek nem adandó). Jelölő nélkül (a nyers szövegben a hivatkozás nem található,
  a kitöltő a környezet szerint keres): 3 (s103-N056, s103-N071, s103-N135).
- **Vakság-próba:** a 183 szócikkből **183-ban** a kiírt bekezdések (a jelölők nélkül) sorrendben azonosak a nyers
  forrásbekezdésekkel, 0 eltér; ebből 9 szócikkben a gépi szerkezet vágna vagy sorbelső fejet tenne (ott szivárgott volna a
  gépi tagolásra épülő munkalap). A vak lapon gépi oszlop (útvonal, szakasz, okkód, bizonyosság, vers) nincs.
- **Szöveg:** 556 147 karakter. **Tokenbecslés két független Opus-kitöltőre együtt** (a #186 tényleges token/karakter
  arányaiból: 0,77; 1,32 átlag; 1,74 a seed-204-en): **≈ 0,73 M token** (sáv 0,43–0,97 M); a seed-204 aránya szerint a felső
  szél ≈ 0,97 M.

## 7. P4 — forráshibák tanúval (DT-F185c, DT-F185d)

*Proveniencia: scope=adat/bdb_forras_javitas.tsv `pe_mem` `jelolt_marad` (556) + `res_dalet` jelöltek (252) | forras=
eszkozok/bdb_jelolt/belso_tanu.py (TAHOT_kivonat.tsv teljes szavak és tő-tokenek, OSHL_lexikalis_index.tsv, Strong_szotar.tsv)
+ Sefaria `/api/words` (a repón kívüli gyorsítótárból) | ts=2026-11-10.*

A szabály a `belso_tanu.py` docstringjében és a SEMA 2.31 `tanu` sorában áll (belső tanú L1, majd L2; ahol kétes, Sefaria;
ellentmondásnál `ketes`; a rés/dálet belső döntése csak L1). A javítás tételes sor a 2.31-ben (`javitva`, a `tanu`
megnevezésével), laponkénti kézi javítás nincs.

| | belső tanú dönt | Sefaria dönt | `ketes` marad | ebből `javitva` |
|---|---:|---:|---:|---:|
| `pe_mem` `jelolt_marad` (556) | 295 (javít 175, marad 120) | 103 (javít 48, marad 55) | 158 | 223 |
| `res_dalet` jelölt (252) | 98 (javít 98) | 48 (javít 20, marad 28) | 106 | 118 |

- **Ellentmondás: 0** — a Sefaria csak a belső tanú kétes soraira fut, így a két tanú egy soron nem dönt egyszerre; a szabály az
  ellentmondást `ketes`-nek jelölné.
- **Sefaria-kérések:** 415 + 122 = 537 (a P0b 360 korábbi válaszát újrahasznosítva), 0 hiba; futásidő 657 + 213 s;
  ≥ 1,2 s szünet, User-Agent `bdb-ocr-check/1.0`; a gyorsítótár a repón kívül (`scratchpad\sefaria_cache\`), a hívó szkript is.
  *(Történeti; a 11. szakasz óta érvénytelen:)* ~~A 2.31 a gyorsítótár nélkül újragenerálva a Sefaria-ítéleteket nem kapja meg.~~
  A javítókör óta gyorsítótár nélkül a rögzített Sefaria-ítéletek maradnak (SEMA 2.31 `tanu`).
- A rés/dálet jelölt-szabálya a felhasználó HAMART-esetére (H0127 „׳עָפָד”) a 3 mássalhangzós, rövidítő geresses szóra is
  kiterjesztve (a P0b 4-es küszöbe ezt kihagyta).

### 7.1 A javítás megjelenítése mindkét nyelven (az orkesztrátor kiegészítése)

**(a) Előtte: nem.** A megjelenítés egyetlen héber javító lépése a `eszkozok/bdb_rovidites.py` `heber_sorrend_javit`-ja (a
lexikon-generátor `lexikon_general.bdb_rovidites_jelol`-ja és az olvasó `olvaso_szerver/blokkok.py` 747. sora hívja, az angol
és a magyar szövegre egyaránt), de csak a `heber_sorrend` sorokat (`sorrend_javitasok` → `_javitasok('heber_sorrend')`) és a
maqqéf-feloldást alkalmazta; a `pe_mem` javítást csak a `nezet_general.py --pe-mem` nézet (angol) ismerte.
**(b) Most:** a `heber_sorrend_javit` a végén a `betu_javit`-ot is hívja (új, ugyanabban a modulban): a 2.31 `pe_mem` és
`res_dalet` `javitva` sorai Strongonként, pontos héber tokenre (betű és pontozás, NFD; a rövidítő geres nem a token része), ha a
Strongban az alak minden előfordulása javított. A `forditasok.tsv` nem változott. Teszt: `teszt_szotari_gerinc.py`
`F185BetuJavitas` (a `gerinc_blokk` kimenetén a H0127 magyar 4.2-blokkja: „(מִן־הָא ׳עָפָר)” és „vö. még פְּנֵי הָא׳”, a régi
alak nélkül) — OK.

## 8. P5 — a seed-103 vak mérés (egyetlen mérés, megismétlés nélkül)

*Proveniencia: scope=seed-103 (200 sor, 183 szócikk) | forras=naplok/BDB_SZELETELO_M2_minta_seed103_kulcs.tsv (a 2.29 F185.4
utáni állapota) + négy vak kitöltés (A-K1, A-K2, B-K1, B-K2; mind `claude-opus-5-5`, külön subagent; összefűzve:
`naplok/BDB_SZELETELO_M2_seed103_kitoltott_A.tsv`, `_B.tsv`) + naplok/F185_seed103_osszevet.py + kézi ítélet (claude-opus-5-5) |
ts=2026-11-10.*

**A kitöltés körülményei.** A kitöltőket az orkesztrátor indította, a repón kívüli másolaton (a vak lap és a szócikkszöveg
két Strong-zárt kötegre bontva, változtatás nélkül; a jelölők száma ellenőrizve: K1 91/91, K2 106/106). A kitöltői utasítást
(`naplok/F185_seed103_kitoltoi_utasitas.md`, változatlan másolat) **az orkesztrátor írta a kitöltés előtt, és az a kitöltés
előtt nem került commitba**; a kitöltés szabályai (4.3) és a kapu (4.5) igen (F185.5, `39f359e4`). Mind a négy kitöltő
jelentette, hogy csak a saját bemenetét nyitotta meg.

| mutató | gépi = arany | arány | Wilson 95% |
|---|---:|---:|---|
| könyv/vers | **200 / 200** | 100,0% | 98,1–100,0 |
| jelentéspont (fő mutató) | **188 / 200** | **94,0%** | **89,8–96,5** |
| tájékoztató: A / B a gépivel (jelentéspont) | 187 / 188 | | |
| tájékoztató: `biztos` / `ketes` sor helyes | 180 / 181 · 8 / 19 | | |

- **A kapu (≥ 194 / 200): NEM teljesül** (188 / 200); a könyv/vers teljesül. A `BDB_MERT_PONTOSSAG` (`konfig/bdb_pontossag.toml`:
  183 / 200, 2026-11-09) *(történeti, a mérés napján:)* változatlan; P3 nem indul — az orkesztrátor dönt (4.5). **Utóbb (10.,
  DT-F185e): a `BDB_MERT_PONTOSSAG` 188 / 200-ra állt.**
- **A ≠ B: 1 sor** (s103-N182 H3318, A `-/1/c`, B `Qal/1/c`): ítélet B — „— 1 go or come out or forth: … c.”; a „Qal” név a
  digitális forrásban hiányzik (2.31 kézi `jelolo_hianyzik`), a szócikk később Hiph`il-t és Hoph`al-t nyit, tehát az 1. pont a
  Qal-é; a gépi helyes. Kitöltő-hiba más sorban nem vizsgálva (A = B soron ítélet nem mozdítja a számot, 4.4).
- **A „fej” = „<törzs>” egyenértékűség** a mérőben él (`m2_minta_osszevet.normal`: a „fej”, a „Qal” és a „Qal/-” egyaránt
  `NINCS_PONT`); a törzs alaktanában álló helyek ezért nem eltérések.
- **A 12 gépi hiba osztályai** (A = B): homonima-szám vagy rész (római) 6 — s103-N028, s103-N122 H7451 és s103-N076 H7651 (hiányzó „I”),
  s103-N094 H3899 (fölös „I”), s103-N061 H7663 (II mint rész ↔ szakasz, és a törzs), s103-N124 H5920 (I ↔ II); számozás/tagolás 4 — s103-N013
  H2469 (`fej` ↔ `-/1`), s103-N040, s103-N105 H3881 (a „II. … 3.” szint hiányzik), s103-N058 H3915 (`-/8` ↔ `-/1/b`); törzs 2 — s103-N004 H8248
  (Qal ↔ Hiph`il), s103-N071 H5186 (`jp_illesztes`, a pont az előző hivatkozásé). A 12-ből 11 `ketes` volt (a P2 jelölése a hibák
  92%-át előre jelezte); a `biztos` sorok 99,4%-a helyes.
- **Tokenfogyasztás:** A-K1 300 771, A-K2 308 404, B-K1 295 939, B-K2 304 617, összesen **1 209 731** — **a becslés (0,73 M;
  sáv 0,43–0,97 M) és az 1 M-es küszöb fölött**, mint a #186 seed-204-én; a karakterarány 2,18 token/karakter (a #186 legnagyobb
  arányánál, 1,74-nél is magasabb).

## 9. Zárás (P1–P5)

- **P1:** a szakasztábla fejfelismerése (hamis bekezdés-eleji fej, tapadt betűfej, törzsnévlista, csoport, alcímszó,
  homonima-szám) és a sorbelső fejek oszlopa (DT-F185b), sorvágás nélkül; a fordítások 29 311 kulcsa változatlan.
- **Forrás:** a 2.29 jelentéspontja a szakasztáblából (DT-F185a); a szeletelő hivatkozás-kinyerés, csoport és tanú.
- **P2:** `bizonyossag` (`biztos` / `ketes:<ok>`); a seed-103-on a `biztos` 180 / 181, a `ketes` 8 / 19 helyes.
- **P4:** pe/mem és rés/dálet tanúval (belső tanú, Sefaria), 341 tételes javítás; a javítás a megjelenítésben mindkét nyelven.
- **P5:** könyv/vers 200 / 200; jelentéspont **188 / 200 (94,0%, Wilson 89,8–96,5)** — a 97%-os kapu nem teljesül; a
  `BDB_MERT_PONTOSSAG` *(történeti: változatlan)* — utóbb 188 / 200 (10.); a lapot nem generáltam újra. A seed-102-höz (183 / 200, más minta) képest +5.
- **Nyitott:** N-F185b (leképezés), N-F185c (könyvnév nélküli hely); a 12 hiba osztályai (római szám, mélyebb számozás, törzs)
  a következő kör jelöltjei, a P3-ról az orkesztrátor dönt.

## 10. Döntések a P5 után (DT-F185e, orkesztrátori döntés, 2026-11-10)

- **A mért szám:** a `BDB_MERT_PONTOSSAG` (`eszkozok/olvaso_szerver/konfig/bdb_pontossag.toml`) új értéke **188 / 200
  (94,0%, Wilson 89,8–96,5), seed-103, valóban vak, 2026-11-10**, a szakasztábla hozzárendelésére. A régi 183 / 200 (seed-102,
  86,7–95,0, Clopper–Pearson) a szeletelőé volt: történeti adat. A CI-módszer a seed-103 eljárása szerint Wilson (a teszt is).
- **P3 elmarad;** a `ketes` sorok gyenge jelölést kapnak (`bdb_vj_szabaly.BIZONYTALAN_PONT`); a `biztos`/`ketes` bontás lapra
  vitele a #182 2. fázisa.
- **A „próba” kivezetése:** a brief feltételét („97% fölött kerül le”) az orkesztrátor kiváltotta. Az előfordulások:
  javítva — `eszkozok/olvaso_szerver/blokkok.py` (a BDB-blokk megjegyzése: „Gépi szeletelés (próba): …” → „Gépi szeletelés: … A
  vers → jelentéspont hozzárendelés kétes pontjai „vonatkozhat” jelölést kapnak.” + a mért szám; két kódmegjegyzés),
  `konfig/bdb_pontossag.toml` (fejléc), `konfig/elemek.toml` (két leírás), `teszt_olvaso_szerver.py` (három teszt). A
  lapgenerátorban (`eszkozok/lexikon_general.py`) és a `sablonok/`-ban BDB-vonatkozású „próba” nincs (a #182-nek nincs teendője
  ebből; a lexikon-oldalak meglévő szövegét nem néztem, lapot nem generáltam).
- **N-F185d:** a 12 hiba osztályai (római szám vagy rész 6, számozás 4, törzs 2) nyitott tételként.
- **Becslési tanulság:** a héber BDB-szöveg vak kitöltése kb. **2,2 token / karakter** (seed-103: 1 209 731 / 556 147), a #186
  görög Thayer-szövegének 1,74-es arányánál több; a következő BDB-becslés ezzel számoljon.
- **Tesztek:** `teszt_olvaso_szerver.py` a munkafa kódjával, a WSL-venv-vel és a WSL-natív `pardes.db`-vel (2026-11-02-i építés):
  104 teszt, OK (2 kihagyva); ebből a `TestF104Egysegek` (a pontosság egy forrásból, Wilson-CI) adatbázis nélkül is OK. (A
  `teszt_futtat.py` a WSL-ben a `~/pardes` klónt futtatja, nem ezt a munkafát, ezért a munkafát közvetlenül futtattam.)

## 11. Javítókör (`naplok/ELLENOR_F185.md`; egyetlen kör, 2026-11-10)

**Mechanikus tételek:**
1. **E32:** a `bdb_vers_jelentes.py` fejléc-literáljában és a `bdb_pontossag.toml` proveniencia-sorában semleges leírás („a
   szakasztábla, F185”) áll a helyőrző helyett; a 2.29 újragenerálva — csak a fejlécsor változott.
2. **E26:** a seed-103 mintaazonosítói a `.md` fájlokban `s103-N…` alakban (`naplok/F185_jelentes.md`, `nyitott/uj/…`, és a
   `naplok/ELLENOR_F185.md`-ben is, csak az azonosító alakja változott).
3. **A 2.31 reprodukálhatósága:** a GENERÁLT fejlécben a `--ts-tanu` és a `--sefaria-cache`; gyorsítótár nélkül (vagy ha a szó
   nincs benne) a mai tábla rögzített Sefaria-ítélete marad (`forras_javit._rogzitett`, `belso_tanu.rogzitett_itelet`; SEMA
   2.31). A `test_javitas_ellenoriz` gyorsítótár nélkül, az összes `--ts` kapcsolóval fut: OK.
4. **SEMA 2.31 állapot** (saját számlálás): `pe_mem` `javitva` 4 046, `valodi_mem` 2 402, `jelolt_marad` 333; `res_dalet` 252
   (`javitva` 118, `jelolt_marad` 134); 43 824 sor.
5. **Rés/dálet szabály** a SEMA-ban a kód szerint: ≥ 3 mássalhangzó, a szó szélén álló geres megengedett.
6. **N-F185a** lezárt blokkba (DT-F185b, `belso_fejek`).
7. A jelentés „Állapot” sora és a 8–9. szakasz „változatlan” mondata frissítve (a régi szöveg történetiként jelölve).
8. **Tanú-formátum:** a `ketes` is szinttel (`tahot/oshb:L2:ketes`, Sefariánál `L0`: nincs illeszthető szócikk); a pe_mem és a
   res_dalet proveniencia-mezője azonos alakú (`… (fejléc) + belso_tanu.py | ts=…`). A 2.31 újragenerálva; a sorok száma
   (43 824), a `sorszam`, az `allapot` és a `javitott_alak` 0 sorban változott, csak az `indok`, a `proveniencia` és a `tanu`.
9. **CK3 — a forrásváltás hatása a 2.29-re** (a base `ae37c175`-höz képest; tájékoztatás): **23 814 sor** (1 486 Strong) `szakasz`,
   `resz` vagy `utvonal` értéke változott (mezőnként: `utvonal` 17 606, `szakasz` 5 963, `resz` 2 440); ebből `ketes` 14 447,
   `biztos` 9 367. A 162 053 sorból a `ketes` összesen 15 374. *(Proveniencia: scope=adat/bdb_vers_jelentes.tsv, a base és a mai |
   forras=eseti összevetés kulcs (strong, sorszam) szerint | ts=2026-11-10.)*

**Tartalmi döntések (orkesztrátor, 2026-11-10):**
- **DT-F185f — a `betu_javit` kapcsolója:** `eszkozok/lexikon_general.py` `BDB_BETU_JAVIT = False` (egyetlen hely, a
  `KETRETEGU_BDB_KARTYA` mintájára); a generátor kikapcsolva a base kimenetét adja (a HAMART-001 és az ANTROP-001 E28-a zöld,
  lapújragenerálás nélkül); az olvasó (`blokkok.py`) a javítást alkalmazza. Tesztek: `F185BetuJavitas` (a bekapcsolt ág a
  függvény szintjén és a generátorban, a kapcsolót a teszt kapcsolja be; és a kikapcsolt kapcsoló hatástalansága) — OK.
- **DT-F185g — ALVIL-001, H7585 Zsolt 16:10:** a DictBDB H7585: „… Ezek 31:15-16, 17; 32:21, 27 b. righteous shall not be
  aban-doned, ׳לשׁ Psa 16:10 (|| שַׁחַת q. v. …)” — a hely a **2.b**-ben áll; **a tábla tévedett** (`-/2/a`, `ketes:jp_illesztes`):
  a sor közepi „b.” „27” után áll, a sorbelső fej szabálya írásjelet vár előtte. Lépés: tételes felülírás a 2.29 előállításánál
  (`bdb_vers_jelentes.JELENTESPONT_KEZI`, kulcs Strong + `poz`, indok idézettel, okkód `jp_kezi`, SEMA 2.29); a sor `-/2/b`, a
  többi 2.29-sor nem változott. Az osztály az N-F185d-ben.

**A #182 teendői:** a `betu_javit` kapcsoló (`lexikon_general.BDB_BETU_JAVIT`) bekapcsolása a lapokon a teljes folyamatban (az
F35 mellé), motívumonként; a `biztos`/`ketes` bontás lapra vitele (2. fázis).

## 12. A mért pontosság az olvasóban (DT-F185h; a felhasználó döntése, 2026-11-10: „semmi helye ott”)

A szólap BDB-blokkjának megjegyzéséből (`blokkok.py`) a mért pontosság kikerült; a megjegyzés: „Gépi szeletelés: … A vers →
jelentéspont hozzárendelés kétes pontjai „vonatkozhat” jelölést kapnak.” A `BDB_MERT_PONTOSSAG` adat (`konfig/bdb_pontossag.toml`:
188 / 200, Wilson 89,8–96,5) a kódban és a dokumentációban marad, az olvasó nem jeleníti meg. Egyeztetett eltérés a DT-F185e-től
(ott a „próba” helyén a mért szám állt). Teszt (`teszt_olvaso_szerver.py`, a munkafa kódjával, WSL): `TestLapok.test_bdb_proba_es_mert_pontossag`,
`TestF104BdbJeloles`, `TestF104Egysegek` — 14 teszt, OK; a doboz nem tartalmaz pontossági számot.

**Maradt (a javítókör utáni helyi CI szerint, döntésre):** E28 HAMART-001:1687 — a 2.30 H2403 „see 1 above” javítása (N99) a
lapon a bűnáldozat szövegét a 4.a–c alá tenné (a commitolt lap a régi, hibás helyen hordozza); a lap újragenerálása ebben a
feladatban tilos. Ez az N99 javításának lapra kerülése, nem új hiba.

## 13. Zárás a javítókör után

- **HAMART-001 újragenerálva (DT-F185i, N99; kikapcsolt `BDB_BETU_JAVIT`):** a lapdiff 4 hunk, mind a H2403 4.2-blokkjában — az
  „1 — bűn” sorából kikerül a bűnáldozat szövege és a „kutatói jelölés: … ellenőrzendő” sor, a „b. bikát …” töredék is; a
  szakaszszám 8 → 11; új 4.a, 4.b, 4.c sor. Más nem változott (új DT/N-hivatkozás és munkaszó nincs).
- **Teljes helyi CI** (`eszkozok/ellenorzes/futtat.py`, base `ae37c175` … `0cbbbe3a`): kilépési kód 0; HIBA egyik szabályban sincs
  (E26 0, E28 0, E32 csak a nem az ágból eredő `blokkok.py:1677` `DT-F76d` JELENTES). JELENTES/FIGYELMEZTETÉS: E12 423 és E13 79
  (az újragenerált HAMART-001 lap meglévő jelölései), E30 5 (ékezet nélküli szó a korábbi commit-üzenetekben: `ketes`,
  `javitva`), nem az ágból: E25 3 (`CLAUDE.md`, `MUNKAMENET.md`), E27 43, E34 41 (`adat/elofordulasok.tsv`), E36 1 (`SEMA.md:1617`).

**Maradék:**
- N-F185b — a mérő útvonal leképezése (rövid folytatás-hivatkozás) és a `szakasz`/`resz` forrása a mérésben;
- N-F185c — a könyvnév nélküli hely és a közbeékelt fejezet feloldása;
- N-F185d — a seed-103 12 hibájának osztályai (római szám vagy rész 6, számozás 4, törzs 2) + a H7585 sorbelső fej számjegy után;
- az olvasó BDB-blokkja a szeletelő bontását jeleníti meg (a 2.29 táblapontja, ahol a csomópontok között nincs, szövegesen áll);
- a #182 teendői: a `BDB_BETU_JAVIT` bekapcsolása a lapokon a teljes folyamatban (az F35 mellé), a `biztos`/`ketes` bontás lapra
  vitele (2. fázis).
