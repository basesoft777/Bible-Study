# F187 — A Thayer-blokk kétrétegű olvasói kártyája; F29 (a)–(e); N-F186g (THAYER_KARTYA)

*FELADATOK #187 · végrehajtó: claude-opus-5-5 · ág: `claude/f187-thayer-kartya` · 2026-11-10*

## 0. Modell-ellenőrzés

A tényleges modell `claude-opus-5-5`, a brief `modell` mezője `opus`: egyezik.

## 1. Mi készült (röviden)

| tétel | hol | állapot |
|---|---|---|
| T5: a görög 4.2 Thayer-kártyája két rétegű | `eszkozok/lexikon_general.py` | kész; a kapcsoló ki |
| T4 (rész): a #186 mért pontossága a szó-lapon, CI-vel | `eszkozok/olvaso_szerver/konfig/thayer_pontossag.toml`, `blokkok.py` | kész |
| a szó-lap Thayer-része két rétegű | `blokkok._r_magyar_gorog`, `lekerdezesek.py` | kész |
| N-F186g: csak érvényes Thayer-sor | `lekerdezesek.magyar_gorog`, `olvaso_pilot/adat.py`, `teszt_thayer_api_koteg.py` | kész |
| F29 (a), (b), (c) olvasói réteg, (e) | `lexikon_general.py` | kész |
| F29 (c) apparátus, (d) | — | nem javítva, N-F187b, N-F187a |
| BDB_OLVASOI kapu: (b), (c), Thayer-kártya | `eszkozok/olvasoi_kapu.py`, SEMA 3.11 | kész |

A lapok nem generálódtak újra, a `lexikon/` nem változott. A kapcsoló (`KETRETEGU_BDB_KARTYA`) üres maradt: a #182 kapcsolja be.

## 2. T5 — a görög 4.2 kétrétegű kártyája

**A mechanizmus a #104-é.** Ugyanaz a kapcsoló (`KETRETEGU_BDB_KARTYA`; a kártya mindkét szótárra az `uj` ágon fut), ugyanaz a jelölő
(`APPARATUS-KEZDET/-VÉGE`, a `<details>` „Szótári apparátus” címmel), és ugyanaz a kapu (`BDB_OLVASOI`, a görög kártyára is).

- **Olvasói réteg:** „A jelentések rendje a Thayer szerint” (a jelentésfa, a motívum helyein álló pont félkövér, magyar glosszával:
  a jóváhagyott címke, ennek híján a magyar szöveg első tagmondata a görög szó előtt elvágva); „A motívum helyein: vers → jelentés”;
  a nem idézett hely kimondva. A Thayer feje gyakran maga is meghatározás: ha van magyar meghatározása, „a szócikk eleje — …” sorként
  áll (G2671: „kiátkozás, elátkozás, átok”); a tagolatlan szócikk „a szócikk egésze — …” (G1944, G5351).
- **Glossza nélküli szakasz:** a magyar meghatározás, ennek híján „a szótár csak párhuzamot közöl” (klasszikus szerzőnév a szövegben)
  vagy „a szótár csak alakot közöl”; magyar szöveg nélkül „(fordításra vár)”.
- **Kutatói réteg** (`<details>`): a teljes eddigi Thayer-blokk — a szócikk feje a görög alakjegyzékkel, a kibontott és a csukott
  szakaszok a klasszikus párhuzamokkal és az igehelyekkel, a kutatói megjegyzés, a szónézet-mutató. A csukott cím glosszás
  („2. – 2.a (2 szakasz): elpusztítani, tönkretenni · felemészteni, …”), a kibontott cím is („2.b — elpusztítani”); a hivatkozásszám a
  `thayer_vers_jelentes.tsv`-ből (`thayer_hivatkozas_szam`).
- **Kikapcsolt kapcsolóval** a HAMART-001 a `--kimenet` próbán a `ts=` sorokon kívül bájtra azonos a commitolt lappal (`diff`: 0).

## 3. F29 — a BDB-kártya öt hibája (egyenként)

### 3.1 (a) Pi'el glossza-felismerés (H0779) — javítva

Az ok: a Pi'el szakasz „3. hímnemű egyes szám suffixummal אֵרֲרָהּ (éraráh) átkozni, átok alá vetni 1Móz 5:29” személyszámmal nyílik, és az
alakjegyzék-felismerés (`_ALAKTANI_KEZDET`) a szám miatt nem ismerte fel. A számot levágva az alak utáni meghatározás áll:
„Pi'el — átkozni, átok alá vetni”. Teszt: `test_a_piel_glossza_szemelyszammal_kezdodo_alakjegyzekbol`.

### 3.2 (b) a szócikk feje nem jelentéspont; egy vers egyszer — javítva

`helyek_pontjai`: versenként a pontok; a fej-pont elmarad, ha a versnek más pontja is van; az ős-pont (pl. `Hiph'il`) elmarad, ha
ugyanannál a versnél a leszármazottja (`Hiph'il 2`) is áll; az azonos pontú versek egy csoportban, a több pontú vers egyszer, a pontok
„;”-vel. A csak a fejben idézett hely: „a szótár csak alakként idézi”. A félkövér a helyek sorát követi (a H7843 „Hiph'il” törzs már
nem félkövér). Eredmény a mintán: H2403 „1Móz 4:7 → 1.b Isten ellen.”, H6975 „1Móz 3:18, Hós 10:8 → 1. tövisbokor …”, H7843
„1Móz 6:12 → Niph'al — …; Hiph'il 2 — …”, H0127 „1Móz 3:23 → 1. …; 3. …”. Kapu: „a szócikk feje” az olvasói rétegben és a kétszer álló
vers BUKÁS. Tesztek: `test_b_fej_nem_jelentespont_es_vers_egyszer`, `test_b_helyek_pontjai`, `test_f187_szocikk_sorszam_fej_es_ismetles`.

### 3.3 (c) belső azonosító — az olvasói rétegben javítva; az apparátusban nyitott (N-F187b)

Az olvasói rétegben a szócikk neve „első/második/… szócikk” (számjegy és BDB-azonosító nélkül); ha csak egy szócikk látható (H2403:
a BDB9520 szövege a BDB2699 5. szakaszában áll), nincs szócikk-név. A héber címszó nem áll a névben: csak jóváhagyott kiejtéssel
állhatna (a kiejtés-szabály). Kapu: „1. szócikk”, „II. szócikk”, `BDB\d+` BUKÁS. Az apparátusban a BDB-azonosító a #104 óta kutatói
rétegként marad (szócikkfej, elnyelő mondat, kutatói megjegyzés); az F29 szövege szerint „nem maradhat a lapon” — ez kérdéses,
N-F187b.

### 3.4 (d) az 1.a számeltérése — nem javítva (N-F187a); lelet

*Proveniencia: scope=H2403 | forras=adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv (olvasva) | ts=2026-11-10.*

- **A magyar bontás nem csonka:** a `bdb_szakasz_hu.tsv` H2403 1.a sora (sorszám 4) mind az öt helyet tartalmazza („1Móz 31:36; 50:17
  (E), 4Móz 12:11 (J) 1Sám 20:1; … 4Móz 5:6 (P)”), és a `bdb_vers_jelentes.tsv`-ben is öt `-/1/a` sor áll (16–20.). A felirat száma
  (5) helyes.
- **A kártyán:** a csukott vázlatsor a szakasz első tagmondata (az első „;”-ig), ezért egy hely látszik. A teljes szöveget kipróbáltam:
  a HAMART-001 mintáján a kiejtés-szabály hiánya 21-ről 126-ra nőtt (a csukott szakaszok héber szavai jóváhagyott kiejtés nélkül), ezért
  visszavontam (F187.3).
- **A szakasztáblán (a #185-é):** a H2403 13–16. sora (a forrásban a „4. bűnért való áldozat” a/b/c pontjai, „1 above …” kezdettel)
  `-/1/-`, `-/1/a`, `-/1/b`, `-/1/c` útvonalat kapott; a kártya a szöveget útvonalanként fűzi, így az 1.b apparátusbekezdés végén
  „b. bikát mutattak be a papokért …” áll. A táblát nem írtam.

### 3.5 (e) a csak bizonytalan sorral idézett pont nem félkövér — javítva

A félkövér a végső helyek-lista erős (nem csak bizonytalan okkódú) pontjait követi. Teszt: `test_e_csak_gyenge_pont_nem_felkover`.

## 4. A szó-lap: két réteg, mért pontosság, N-F186g

### 4.1 A mért szám (a javítókörben javítva, ELLENOR_F187 T4 + A1)

*Proveniencia: scope=seed-204, a mérvadó vak mérés | forras=adat/thayer_aranyminta.tsv (`seed = 204`; a `gep_utvonal` =
`arany_utvonal` sorok: egyezik + kitolto_hiba) + naplok/F186_jelentes.md 10.3 | ts=2026-11-10.*

A mérést nem ismételtem. A szám: **196/200 (98,0%), Wilson 95%: 95,0–99,2%** — a #186 mérvadó, valóban vak mérése (a
`F186_jelentes.md` 10.3: „ez a mérvadó szám”; a kitöltő a nyers forrásbekezdéseket kapta). Egyetlen forrása a
`konfig/thayer_pontossag.toml` (proveniencia-sorral, a seed-204-re); a szó-lap ebből számolja, a teszt a Wilson-intervallumot
újraszámolja, és ellenőrzi, hogy a szám kézzel nem áll a kódban (`test_thayer_pontossag_egy_forrasbol`). Az első menetben ide a
seed-203 száma került (194/200), „vak ellenőrzéssel” felirattal; a seed-203 vaksága a tábla fejléce szerint korlátozott, tehát ez
hiba volt. A seed-204-en az A kitöltő nyers egyezése is 196 (10.3, tájékoztató sor), így a nyers és az ítélet utáni érték azonos
(a BDB-nél a lapon a nyers szám áll, DT658 (a)).

### 4.2 A szó-lap Thayer-része (`szo.magyar_gorog`)

Olvasói réteg: a jelentések rendje a Thayer szerint (a `thayer_szakaszok` útvonalából, glosszával); versből megnyitva „Ebben a versben:
… A Thayer itt idézi: …” a `thayer_vers_jelentes` szerint (pont tippelése nélkül; idézet nélkül „nem idézi”), a „próba” felirattal és a
mért pontossággal (proveniencia a súgóban). Kutatói réteg: a teljes magyar Thayer-szöveg szakaszonként csukott `<details>`-ben; a
`teljes` sor és az UBS DNTG-sorok változatlanul. A blokk jellege `modell` + `gepi` (a vers → pont gépi). Új CSS-osztály nincs (a
regiszter-őr). Tudnivaló: a WSL-natív `pardes.db` `thayer_szakaszok` táblája a #186 előtti (17 093 sor; a tábla ma 17 317); a szó-lap a
DB újraépítése után követi a #186 vágásait.

### 4.3 N-F186g

A SEMA (2.14, DT718) szerint a tagsor `sz<n>~<m>` alakú és mindig `elavult`; érvényes sor tehát: nem `elavult`, és nem tagsor (döntés
nem kellett). `lekerdezesek.magyar_gorog` (SQL-szűrés; az `allapot` oszlop nélküli régi táblán csak a tagsor-szűrés), a #60 pilot
(`olvaso_pilot/adat.py`: `r[7] != 'elavult'`, `'~' not in r[3]`) és a `teszt_thayer_api_koteg.py` `hu_sorok`-ja (csak `sz\d+`, nem
`elavult`). Teszt: `test_csak_ervenyes_sor`.

## 5. A BDB-kártya forrása és a #185 (DT-F185a)

- **Ma:** a 4.2 BDB-kártyájának vers → pont adata a `adat/bdb_vers_jelentes.tsv` (a szeletelő, `olvaso_szerver/bdb_szelet.py` +
  `bdb_vers_jelentes.py` kimenete); a jelentésfa és a szöveg a `adat/bdb_szakaszok.tsv` + `adat/bdb_szakasz_hu.tsv` (`bdb_jelolt/bont.py`).
  A kettőt az útvonal köti (`gerinc_blokk` `teljes_ut`, `bdb_hivatkozas_szam`). A szó-lap BDB-blokkja a megjelenített bontást a
  szeletelőből veszi (`blokkok._bdb_bontas`), a vers-jelölést a DB `bdb_vers_jelentes`-éből.
- **A #185 után:** ha a #185 a `bdb_vers_jelentes.tsv` `utvonal`-át a javított szakasztáblából írja újra, a kártya változtatás nélkül
  követi; ha új táblát vagy oszlopot vezet be, a `gerinc_adat` `bdb_vj`/`bdb_vj_feloldott` betöltése és a `bdb_hivatkozas_szam` arra
  állítandó, és a szó-lap `_bdb_bontas`-a is. N-F187c.

## 6. Minta és saját átnézés

**Minta (a repón kívül; a kapcsoló csak a futtató folyamatban bekapcsolva, `minta_bekapcsolva.py`):**
`C:\Users\bases\AppData\Local\Temp\claude\a526c0d9d93cb95b\6a03f1ea-23dc-4c53-8b22-b1c1212f0869\scratchpad\f187_minta\` —
`HAMART-001_4.2_gorog.md`, `HAMART-001_4.2_heber.md`, `HAMART-001_4.2_olvasoi_retegek.md` (csak az olvasói rétegek), a teljes lap:
`utana\lexikon\HAMART-001_TUDOMANYOS.md`; összevetésül a #104-es állapot bekapcsolva: `elotte\` és `elotte_42.md`.

**Kapu a mintán:** olvasói kapu 0 BUKÁS, 25 FIGY (azonos a #104-es bekapcsolt mintával és a mai lappal); kiejtés-szabály 21 hiány (azonos).
A #104-es bekapcsolt állapoton az új kapu 4 BUKÁS-t ad (görög alak a Thayer-blokkban, „a szócikk feje”, kétszer álló vers, ⓘ).

**Saját átnézés (az olvasói rétegek, mind a 15 kártya):**

- *Munkaszó, belső azonosító:* nincs (sorszám, `BDB…`, `sz<n>`, „1. szócikk”, „szócikk feje” nem áll).
- *Szám:* csak a „(5 hely)”, „(13 hely)” (a tábla száma, DT-F104d).
- *Ismétlés:* egyetlen vers sem áll kétszer; a H0127 1Móz 3:23 és a H7843 1Móz 6:12, illetve a G1311 Jel 11:18 két különböző,
  egymásba nem ágyazott pontnál áll, egy csoportban.
- *Félkövér:* a helyek sorának pontjai; a csak alakjegyzékes ős-törzs (Hiph'il) nem.
- *Maradék észrevételek:* három BDB-szakasz glossza nélkül áll („külön meghatározás nélkül”: H2403 1.f, H7451 6., 8.) — N-F187d;
  a G2671 „c — a szótár csak párhuzamot közöl” a Thayer saját, előzmény nélküli „c” jelét adja (a forrás tagolása); a glosszák
  igealakja vegyes (címke: „megront”, fordítás: „elpusztítani”) — a címke- és fordításrétegé, nem a kártyáé.

## 7. Tesztek

- `python -m unittest eszkozok.teszt_szotari_gerinc eszkozok.teszt_olvasoi_kapu`: 149 teszt; 7 bukik, **ugyanaz a 7 a main
  `lexikon_general.py`/`olvasoi_kapu.py`-jával is** (KaroliHelyette, Megjelenites.test_kapcsolo, Olvasoi1314 ×2, ThayerSzakaszsorok,
  ValodiAdat.test_33_sor, Arany.test_G7) — előzetes, a #187-től független. Az új `F187KartyaJavitasok` (8) és a `BdbOlvasoiReteg` új
  tesztjei (2) zöldek.
- `python eszkozok/teszt_futtat.py --diff origin/main` (WSL, `~/pardes/pardes.db`): zöld a `teszt_olvaso_szerver`, `teszt_pilot_aranymintaval`,
  `teszt_bdb_vers_jelentes`, `teszt_visszhang_kapu` és a többi; a `teszt_ubs_dbh` és a `teszt_tervezo` hibáját a #187 okozta
  (`allapot` oszlop nélküli teszttábla; dinamikus CSS-osztály) — javítva (F187.4), újrafuttatva WSL-ben: `teszt_tervezo`,
  `teszt_ubs_dbh`, `TestF187ThayerKartya`, `TestRegiszterEsAdatbazis` — 67 OK.
- `teszt_szintek.py` (lassú): 2 bukás — `test_heber_szavak_alacsony_es_magas_szinten` (N110, a main-en is) és
  `test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat` (a H6440 héber lapon a BDB-blokk „Ebben a versben”
  doboza; a #187 a héber szó-lapot nem érinti). A második a main-en **nem futtattam** (keret), tehát az előzetessége nem igazolt.
- `python -m unittest eszkozok.teszt_thayer_api_koteg`: 35-ből 2 bukik — `BUt.test_nagy_strong_javitasa_egyenkent_marad` a main-en is;
  `Kicsi.test_prompt_azonos_a_forditas_prompt_epittel` a falióra-időbélyegen bukik (két prompt-építés más másodpercben,
  `thayer_jelolt/adatblokk.py:284`), a #187 változtatása (`hu_sorok`) ezt a tesztet nem érinti.

## Egyeztetett eltérés

A hatókör az orkesztrátor döntésével bővült: az N-F186g-vel (az olvasó és a #60 pilot csak érvényes Thayer-sort mutat; a
`teszt_thayer_api_koteg.py` tagsor-biztos) és az F29 (a)–(e)-vel (a BDB-kártya hibái), a BDB_OLVASOI kapu bővítésével (a (b)–(c) és a
görög kártya). Az orkesztrátor menet közbeni iránya szerint a kérdéses pontok (F29 (d), (c) az apparátusban) nem javultak, csak
jelölve vannak (N-F187a, N-F187b). Az `ir` mező ennek megfelelően bővült (F187.0).
