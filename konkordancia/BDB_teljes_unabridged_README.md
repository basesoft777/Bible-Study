# BDB teljes (unabridged) — `BDB_teljes_unabridged.tsv`

## Forrás

- **Repó:** [eliranwong/unabridged-BDB-Hebrew-lexicon](https://github.com/eliranwong/unabridged-BDB-Hebrew-lexicon) (GitHub, publikus)
- **Felhasznált fájl:** `DictBDB.json`
- **Letöltés URL:** `https://raw.githubusercontent.com/eliranwong/unabridged-BDB-Hebrew-lexicon/master/DictBDB.json`
- **Letöltés dátuma:** 2026-09-02
- **Eredeti szöveg szerzősége:** Brown, F., Driver, S. R., & Briggs, C. A. — *A Hebrew and
  English Lexicon of the Old Testament* (BDB)
- **Digitalizálás:** Tim Morton (Bible Analyzer) eredeti transzkripciója, BibleHub
  adataival kereszt-ellenőrizve; Eliran Wong JSON-formázása
- **Licenc:** közkincs (public domain) — az eredeti BDB szövege és annak digitalizált
  átirata is közkincs; **a státusz a repóban „tisztázatlan”** (`adat/licencek.tsv`: a `BDB` sor 7. és a `lexikonok_nyers` sor 43. sora; a forrásrepó README-jének állítása nem független igazolás). Ugyanez áll a `konkordancia/lexikonok_nyers/BDB.lexicon`-ra, amelyből az F57 pótlása készült.
- **SHA-256** (`konkordancia/BDB_teljes_unabridged.tsv`, K7, F05b):
  `40d96e57b491457a712a0fc45ed84022a1d3929f480495472a11f66a445f3cf6` (aktuális: F57 utáni állapot, +3 pótolt sor, l. „Pótlás”; előzmény, az F57 előtti F46-os állapot:
  `dfb5b2aaa722291736d567c4e56c10d2890f2c860eadf416629e5d02f0e59acc`; F46 javított verzió, a DT-F46 kiegészítés 2 utáni állapot: 16 csere visszaállítva, F46.14; előzmények: F46.6 `ff5357fe69c19262aa2464fbae03e02a177f4a8e044b8f47290751fee4f427a0`; F34 javított verzió `5c176037617813e330eb57e883ab7fd728c19a244c42196668ea712d0f502f14`; az eredeti, K7: `1d28a84004817b8ee09eff92d762038ae2eac7351f24abd0a8b1cc5df380dfa5`)

## Konverzió

Python szkripttel (`_convert_bdb.py`, a `konkordancia/` mappában, egyszeri
segédszkript) HTML-jelölés eltávolítva, egyszerű szöveggé alakítva. A Strong-szám
oszlop a repó zero-padded konvencióját követi (4 számjegyre kitöltve, pl. `H8415`,
`H1` → `H0001`), homográf-toldalékkal együtt (pl. `H90a` → `H0090a`) — konzisztens a
`Strong_szotar.tsv` és a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` konvenciójával.

## Kimenet

**`BDB_teljes_unabridged.tsv`** (8090 sor + fejléc az eredeti konverzióban; F57 óta 8093, l. „Pótlás”; 3 oszlop):
```
Strong_padded | Strong_eredeti | Teljes_szocikk
```

- **Strong_padded:** zero-padded Strong-szám, pl. `H8415`, `H0001`
- **Strong_eredeti:** a forrásfájl eredeti, nem kitöltött azonosítója (pl. `H8415`, `H1`, `H90a`)
- **Teljes_szocikk:** a teljes BDB-szócikk, tiszta szövegként (HTML-jelölés eltávolítva)

## Minőségi mutató

- **8090/8090 sor sikeresen konvertálva, üres bejegyzés nélkül** (minden sor tartalmaz
  legalább egy rövid szöveget — 10 bejegyzés 20 karakternél rövidebb, ezek legitim
  kereszthivatkozások más szócikkre, pl. `H0381` „ish-chayil" → lásd a fő szócikket).
- Ez lényegesen teljesebb, mint az openscriptures `BrownDriverBriggs.xml`, ahol a
  gyök-bejegyzések **17,5%-a (453/2595) feldolgozatlan** („new" státuszú, üres).
- Ellenőrzött minta: `H8415` (תְּהוֹם) — teljes, tartalmas szócikk (kb. 2400 karakter).

## Szerep a determinisztikus BDB-ellenőrzési protokollban

**Ez a fájl az ELSŐDLEGES teljes-BDB forrás** a determinisztikus BDB-ellenőrzési
protokoll 2. lépésében. Az openscriptures `BrownDriverBriggs.xml` +
`LexicalIndex.xml` (lásd `TBESH_TBESG_README.md`) másodlagos/tartalék szerepbe kerül
a hiányossága miatt.

**Helyesbítés (2026-09-02, pontosítva 2026-09-03):** a הום-gyök „morajló
mélység" etimológiai adat (תְּהוֹם/1Móz 1:2 kapcsán) **valós és forrással
alátámasztott** — de a forrás-hozzárendelés pontosítást igényelt. A H8415
(תְּהוֹם) BDB-szócikke saját szövegében **NEM tartalmaz gyök-eredeztető
megjegyzést** (sem "Origin:" jelölést, sem H1949-hivatkozást) — ez
ellenőrizve mind az eredeti eliranwong-forrású `DictBDB.json`-ban, mind a
belőle készült ezen `BDB_teljes_unabridged.tsv`-ben. Az "Origin: from
H1949" hivatkozás ténylegesen a **`Strong_szotar.tsv`** (openscriptures
Strong-szótár, CC BY 4.0) "Gyök/Származtatás" oszlopából származik, ahol a
H8415 sora szó szerint "from H1949"-et rögzíti — ez egy **másik lexikon**
(Strong's Concise Dictionary) tartalma, nem a BDB-é. A gyök (H1949,
"morajlani, zúgni, megzavarodni") jelentése önmagában valós BDB-tartalom
is (l. e fájl H1949 sora), csak a תְּהוֹם↔הום kapcsolatot nem a BDB, hanem a
Strong-szótár mondja ki explicit módon.

**Módszertani tanulság (pontosítva):** a determinisztikus BDB-ellenőrzési
protokollnak a fejszó eredeztetési láncát a **`Strong_szotar.tsv`
"Gyök/Származtatás" mezőjéből** kell követnie (nem a BDB szabadszöveges
szócikkéből, ami nem tartalmaz strukturált gyök-hivatkozást). A
`Strong_szotar.tsv`-ben 4245+ sor tartalmaz "from H####" vagy hasonló
(„corresponding to H####", „variation of H####", „feminine of H####")
keresztre mutató mintázatot — ez az elsődleges, program által is
kinyerhető forrás az Origin-lánc-ellenőrzéshez, nem a BDB-fájl.

## Kereszthivatkozás

Ez a fájl önálló, a `Strong_padded` mezőn keresztül join-olható a meglévő
`Strong_szotar.tsv`, `Karoli_Strong_kivonat.tsv` stb. táblákkal (l.
`Join_tabla_folyamat_magyarazat.md` mintája szerint). A meglévő fájlok
változatlanok maradtak, semmi nem lett törölve vagy felülírva.

## `BDB_etimologia_kezi_hatarok.tsv` — nyelvi háttér, D28 hatókörű 26 token (F05_SZOTAR_BRIEF.md S9)

**Részben generált, részben kézi javaslat**
(`eszkozok/bdb_etim_hatarok_import.py`). A `nyelvi_hatter` mező a szócikk
fejének (címszó, szófaj, etimológia/rokon-nyelvi anyag) az ELSŐ,
zárójelen kívüli (nulla mélységű) em-dash-ig tartó része (D41) — a héber
lexikai nyelvi háttér szerepéhez (S9). Fejléc: `strong allapot
nyelvi_hatter szocikk_hossz hatar_pozicio`.

`allapot` négy érték egyike:
- **`gepi`** (14 token) — a `nyelvi_hatter` az ELSŐ, ZÁRÓJELEN KÍVÜLI
  (nulla mélységű) em-dash (—) előtt ér véget (D41, F05b, 2026.09.29;
  `eszkozok/bdb_etim_hatarok_import.py` `zero_melysegu_emdash()`), és a
  határ a szócikk hosszának legfeljebb 40%-ánál van. A korábbi `—\s*1\s`
  minta (csak a számozott „1.” értelem kezdetét kereste) hibás volt: nem
  vette figyelembe az igealak-paradigmákat és a zárójelen belüli
  véletlen „1”-eket — l. `naplok/ELLENOR_SZOTAR_S1.md`.
- **`javaslat`** — nincs korai (a 40%-os küszöbön belüli), nulla mélységű
  em-dash; a `nyelvi_hatter` **kézzel kijelölt** szöveg, a szkript
  `KEZI_JAVASLATOK` konstansában — jóváhagyásra vár.
- **`jovahagyott`** (6 token: `H0430`, `H0922`, `H2403`, `H3678`, `H8004`,
  `H8034`) — mint a `javaslat`, de a kézi határt a felhasználó
  chat-döntéssel már jóváhagyta (2026.09.29, `naplok/
  SZOTAR_S1_7_jelentes.md`). **`H2403` NEM a „nincs korai em-dash” eset**
  — a szócikknek VAN nulla mélységű em-dash-a (a szócikk 5,8%-ánál, a
  40%-os küszöbön messze belül), de addig a pontig egy hosszú, em-dash
  nélküli, vesszővel csatolt inflektált-alak/citációs lista áll
  (construct/suffix/plural alakok versekkel), ami NEM etimológia — ez a
  D41-szabály egy ismert gyengesége: csak az em-dash-sel határolt
  használati/alak-blokkokat ismeri fel, az em-dash nélkülit nem. A kézi
  határ ezért éppen ott vágja el a szöveget, ahol az érdemi etimológia
  ténylegesen véget ér („…sin, sin-offering” után). A szkript
  `JOVAHAGYOTT` halmaza dönti el, hogy `javaslat` vagy `jovahagyott`
  legyen a kimeneti címke.
- **`nem_targyalja`** (6 token: `H0779`, `H2555`, `H5303`, `H6093`,
  `H7496`, `H7497`) — rövid szócikk, nincs külön etimológiai bekezdés;
  `nyelvi_hatter` üres. Ez **végleges állapot, nem pótlandó hiány** (D11).

A 26 token a D28 hatókör-szabálya szerinti motívum-Strong-készlet (l.
`F05_SZOTAR_BRIEF.md` §0 0.4). Az S0-beli mérés (`naplok/SZOTAR_S0_bdb_etim.tsv`,
a régi 24-tokenes hatókörön) csak a `gepi`/nem-`gepi` elkülönítést mérte
(talál-e határt a regex, igen/nem), a tényleges `nyelvi_hatter` szöveget
és a `H8414`/`H0922` besorolását ez a tétel (S1.4) adja először.

## Javítás (F34, 2026.10.01): „ψ” (Zsoltárok) hibás feloldása

A forrás a „ψ” jelet több száz helyen az előző könyvnévre oldotta fel (pl. `Isa 106:9`, `Job 97:7`). Javított dataset-verzió: 159 helyhivatkozás (56 szócikk) `Psa`-ra cserélve (TAHOT-igazolással; az A-maradék 15 helye TAHOT nélkül, a Macula MT-versszámozási táblával igazolva), mezőkulcsos táblával; csak helyhivatkozás változott. Nyers JSON nincs a repóban, ezért a TSV közvetlen javítása történt. Proveniencia és a maradék (156 hely, 94 szócikk, kézi nézet; N-F34, N-F34c): `naplok/F34_M2_naplo.md`, `naplok/F34_M2_csere.tsv`, `naplok/F34_M2_maradek.tsv`; eszköz: `eszkozok/bdb_psi_javit.py`.

## Pótlás (F57, 2026.10.05): Strong-címke nélküli szócikkek

**Mi történt.** A `DictBDB.json`-ból készült tábla minden szócikkhez egyetlen Strong-kulcsot ad. A BDB-azonosító szerint kulcsolt `konkordancia/lexikonok_nyers/BDB.lexicon` (ugyanaz a BDB-kiadás; a licencstátusz „tisztázatlan”, l. fent; új licencsor nem kellett) két osztályban mutatott eltérést (felmérés: `naplok/BDB_STRONG_POTLAS_M0.md`).

**1. Címke nélküli szócikkek (a tábla +3 sora).** A BDB.lexicon 846 szócikkének fejlécében nincs Strong-címke. A párosítás szabálya (`naplok/BDB_STRONG_POTLAS_M1.md` 1. szakasz; `eszkozok/bdb_strong_potlas.py`): az OSHL-lemma és a BDB-címszó normalizált alakja egyezik (holem-waw egységesítve, kantilláció és meteg nélkül, magánhangzók megmaradnak); homonímiánál a glossza dönt, különben jelölt; ha a szócikknek van címkéje, vagy a Strongnak van sora a táblában, nem párosítható. Eredmény: 3 `egyertelmu`, 0 `tobb_jelolt`, 843 `nincs_par` (`konkordancia/BDB_strong_potlas.tsv`, minden sorban `indok` és proveniencia). A felhasználó a 3 párt jóváhagyta (DT-F57a, 2026-10-05): **H4725, H4123, H0747**. Ezek a sorok a tábla **végére** kerültek; a meglévő 8090 sor (és a fejléc) bájtra azonos (az `--m2` az írás előtt és után ellenőrzi). A sor fejében az átírás a meglévő sorok egyszerűsített, nem diakritikus átírását követi (K3 stílusegyezés): az OSHL `atiras` mezőjéből szabállyal származtatva (`egyszerusitett_atiras`): š → sh, az aleph/ajin jele (ʾ, ʿ) és minden kombináló diakritika (hosszúságjel, circumflex, breve, pont) elhagyva; **köznévnél kisbetű** (māqôm → `maqom`, mahătallôt → `mahatallot`), **tulajdonnévnél nagy kezdőbetű** (a meglévő tulajdonnév-fejek is nagybetűsek: Aryowk, Moab; ʾărîsay → `Arisay`; tulajdonnév: a BDB-szócikk szófaja „proper name”). A szöveg a BDB.lexicon HTML-jéből a `_convert_bdb.py` tisztításával készült, és a meglévő sorok stílusához igazítva (DT-F57c, ellenőri 2. tétel): a könyvnevek a meglévő alakok (1Kgs → 1Kin, 2Kgs → 2Kin, Ps → Psa, Hos → Hosea, Mic → Micah, Nah → Nahum, Esth → Est), nincs szóköz írásjel előtt, „(” és „^” után.

**2. Másodlagos címke (nem kerül a táblába; DT-F57a (c), DT-F57c, DT-F57f, DT-F57g, DT-F57h, DT-F57i).** A BDB.lexicon 529 Strong-kulcsa (pl. H0136, H0341) címkével áll egy szócikk fejlécében, a táblában azonban nincs sora. Szövegduplikáció helyett a megfeleltetés külön, generált táblában van (`python eszkozok/bdb_strong_potlas.py --alias`). **Az alias azt mondja meg, hol áll a BDB-szövege, nem azt, hogy a két szó azonos** (pl. az Abel-összetett helynevek H0059, H0063–H0067 a H0058 ʾābēl sorára oldódnak fel, mert a BDB alpontként tárgyalja őket; a H3071, H3073, H3074 és a H3070 Jahve-nevek (JHVH-összetételek) a második tag szócikkére).
- **`konkordancia/BDB_strong_alias.tsv`** (296 sor: héber 282, arámi 14; oszlopok: `masodlagos_strong`, `tabla_strong`, `bdb_id`, `nyelv`, `cimszo`, `szoveg_hasonlosag`, `proveniencia`). Alias-feltétel (nyelvi szűrés nélkül): (1) a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér `H<n>` kulcsának `bdb_id`-je egyezik a másodlagos címke `bdb_id`-jével); (2) **mérőszám** (`elejegyezes`): a szócikk ujjlenyomatának (CSAK latin betűk; a héber szöveg és a bibliai hivatkozások kimaradnak; legfeljebb 1500 karakter) az a hányada, amely a testvérsor elején megvan (a testvérsor `H<n>.` előtag nélküli ujjlenyomatának első `hossz + 60` karaktere az ablak; érték = a `difflib.SequenceMatcher` egyező blokkjainak karakterszáma / a szócikk ujjlenyomatának hossza), küszöb ≥ 0,9; (3) ha több azonos szócikkbeli testvér van, pontosan egy felel meg a (2)-nek, és az az alias célja (2+ megfelelő esetén elvetve; ilyen sor jelenleg nincs); (4) kézi kivétel: H2088. A héber szöveg azért marad ki, mert a DictBDB a többszavas héber kifejezések szórendjét megfordítja; a hivatkozások azért, mert a két forrás eltérően rövidíti őket. **Korlát: csonk szócikkeknél (pl. BDB515, BDB3121) a mérőszám triviálisan magas, ott gyenge bizonyíték** (az aliasban a mintában ebből hamis alias nem lett).
- **`konkordancia/BDB_strong_alias_elvetett.tsv`** (233 sor: héber 60, arámi 173; oszlopok: `masodlagos_strong`, `bdb_id`, `nyelv`, `cimszo`, `testver_strong`, `indok_kod`, `indok`, `proveniencia`; az `indok_kod` gépi kód, szűrhető, az `indok` a magyar magyarázat): ezek **nem** feloldhatók a táblában meglévő sorra, jelöltek maradnak. A `testver_strong` az azonos szócikkbeli testvéreket sorolja fel (a `nem_ebbol_a_szocikkbol` sorokban a más szócikkből származókat). Kódok (darab): `nem_ebbol_a_szocikkbol` 220 (ebből arámi 172: a testvérsor a héber szócikk sora, pl. H0399 → H0398); `a_testversor_mas_szocikk` 9 (a testvérsor valóban más szócikk, pl. H3606 → H6903; ebből arámi 1); `kuszob_alatt` 3 (H0706 0,832; H6737 0,858; H8112 0,873: a testvérsor ugyanazzal a címszóval kezdődik, de a mérőszám a küszöb alatt van; a #57-ben nincs egyenkénti beemelés, a kód szűrhető, egy későbbi feladat beemelheti őket); `kifejezes_tarscimke` 1 (H2088 → H6258: a BDB6199 fejlécében a „zeh” egy attá-kifejezés miatt kapott társcímkét; a saját szócikke máshol van, ezért valódi téves alias volna). Több testvér-Strong esetén nincs elvetés (nincs 2+ megfelelő sor); az alias célja pontosan egy megfelelő testvér: a „megfelelő testvérek száma = 1” feltétel minden aliasban teljesül (ellenőrzött); több azonos szócikkbeli testvér esetén a többi testvér sora más szócikk vagy csonk (pl. H6990, H8550, H1170). **Korlát:** a `kuszob_alatt` / `a_testversor_mas_szocikk` megkülönböztetés címszó-heurisztika, amely csak a legjobb mérőszámú testvért nézi és homonímára vak (pl. H5875, H5883, H5886 → H5871: „más szócikk” kódot kaptak, noha a címszó azonos), ezért a kód támpont, nem bizonyíték. A „stub-sor/rövid törzs” korábbi magyarázat téves volt: a valós ok az, hogy a testvérsor további szócikkeket is tartalmaz, vagy más szócikk.
- **Nyitott:** az elvetett arámi szócikkek tényleges pótlása (a BDB.lexicon szövegéből új táblasorok) külön feladat a `/befogad` útján (DT-F57d).

**Darabszám.** A tábla 8093 sor + fejléc (az eredeti konverzió: 8090). SHA-256: l. fent (aktuális érték).

**Reprodukálás.** Az `--m1` a pótlás *előtti* táblaállapotra írja a párosítást (a pótolt Strongok a táblában már szerepelnek, ezért újrafuttatva `nincs_par`-ra esnének); az `--m2` idempotens; az `--alias` a táblából és a BDB.lexicon-ból bármikor újragenerálja a két alias-táblát.
