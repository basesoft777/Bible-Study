# F185 — A BDB vers → jelentéspont hozzárendelés javítása (BDB_JELENTESPONT_97)

*FELADATOK #185 · végrehajtó: claude-opus-5-5 · ág: `claude/f185-bdb-jelentespont-97` · 2026-11-10*

**Állapot:** a P1 részben kész, a P2 nem indult. Az orkesztrátor hatókör-módosítása (2026-11-10: egy külső BDB-digitalizáció
lehet a hozzárendelés forrása, döntés még nincs) szerint a menet tiszta ponton megáll. A P3–P6 nem indult. A seed-103 mintát nem
húztam ki.

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
rendezve), a seed-99/100/101/102 kulcsainak sorai kizárva; azonosító `N001`–`N200`. Rétegzés nincs (a seed-101/102 eljárása).

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
