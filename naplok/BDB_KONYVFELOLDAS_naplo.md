# BDB_KONYVFELOLDAS — napló (F46, FELADATOK #46)

*Brief: `F46_BDB_KONYVFELOLDAS_BRIEF.md` · ág: `claude/bdb-konyvfeloldas` · végrehajtó: Opus
(claude-opus-5-5) · 2026-10-03 · állapot: ⛔ a 3.5 megállásnál (DT-F46), a gépi csere (3.6) nem futott*

proveniencia (a mérések): `scope=BDB_teljes_unabridged.tsv minden könyvjelölt igehely-tokene (105 723) | forras=konkordancia/BDB_teljes_unabridged.tsv + konkordancia/OSHL_BDB_igehelyek.tsv + TAHOT_kivonat.tsv (+-1 vers) + Macula_heber_*.tsv (MT) | ts=2026-10-03`
(újrafuttatás: `python eszkozok/bdb_konyv_javit.py`; vetítés: `--vetit --szintek …`).

## 3.0–3.2 Előfeltételek és a független forrás

- **3.0 modell:** a végrehajtó Opus (`claude-opus-5-5`), a fejléc `modell: opus` mezőjével egyezik.
- **3.1:** a #38 `megallt` (⛔ DT-F38i), az utolsó adag ága (`claude/f38-adag5`) a `main`-ben
  (PR #137, `98b9006`). Az ág a `main`-ből (`510a6b1`), első commit `abe841c` (F46.0).
- **3.2 licenc — nincs megállás.** A `BrownDriverBriggs.xml` az `openscriptures/HebrewLexicon`
  `21c9add13bc727d3a951361778e97e3ff7afd1ce` commitjában van (ugyanaz, mint az OSHL-import
  `LexicalIndex.xml`-je; a letöltött `LexicalIndex.xml` sha256-ja azonos a
  `OSHL_lexikalis_index_README.md`-ben rögzítettel). A licenc a repó `readme.md`-jében áll
  (külön LICENSE-fájl nincs, a `LICENSE` útvonal 404): „These files are released under the
  Creative Commons Attribution 4.0 International license” — a readme 1. pontja a
  `BrownDriverBriggs.xml`-t a „These files” közé sorolja. Új sorok: `adat/licencek.tsv`
  `OSHL_BDB` (tisztazott, szó szerinti idézettel), `adat/datasetek.tsv` `OSHL_BDB_igehelyek`
  (ajanlott / korlatos). A nyers XML a gitignore-olt `konkordancia/_nyers/oshl/` alatt
  (sha256 `2b52658a…c38f8`); a repóba csak a kivonat kerül:
  `konkordancia/OSHL_BDB_igehelyek.tsv` (4053 sor: 3952 `<ref>`, Strong a `LexicalIndex.xml`-ből;
  19 `r=` attribútum nem értelmezhető, pl. `Ezra.814`, `Job.37:23` — kimaradt, a szkript kiírja).

**A független forrás lefedettsége kicsi — ez a felmérés legfontosabb korlátja.** A forrás saját
szavával „work in progress”: 11 845 szócikkéből csak 2855-ben van `<ref>`, a többi igehely nélküli
„base” vázlat. A BDB-forrás 105 723 könyvjelölt tokenjéből a csere-táblán **mindössze 18 sornál
mond valamit a független forrás**. A brief `magas` szintje (független forrás + vers + Strong-próba)
ezért csak 12 sorra teljesülhet; a csere-jelöltek túlnyomó része a versszám-ellenőrzésen és a
Strong-próbán áll (`kozepes`).

## Módszer (3.3–3.4) és az értelmezési döntések

Egység: a **könyvjelölt token** (`Hab 41:47`, `1 Samuel 3:22`), a 11. kapu forrásoldali
leképezésével (`normalizal.py`, a `Forrás-alakok` oszloppal). A könyv nélküli, láncolt
igehelyek (`; 42:3`) a token könyvét öröklik, tehát a token cseréje a láncot is javítja.
Kulcs: `(strong, pozicio = karakter-offset a Teljes_szocikk-ben, forras_alak)`.

1. **Rendben**, ha a hely a forrásbeli könyvben létezik, és a Strong-szám ott ±1 versen áll
   (TAHOT vagy Macula), vagy a független forrás ugyanezt a könyvet mondja: 97 704 token.
2. **Hibajel**: a fejezet vagy a vers nem létezik (`fejezet_tullepes`, `vers_tullepes`), 176-nál
   nagyobb vers vagy szám-farok (`osszeolvadt_alak`), nem leképezett alak (`Kings`, `Ki`, `Sam`,
   `Samuel`, `Chron`, `Chronicles`, `Ze`, `Jes`, `Esc`, `De`, `En`, `Ear`), a független forrás más
   könyvet mond. Létező, de igazolatlan helynél (`mas_konyv_ervenyes_fejezettel`) csak akkor
   jelölt, ha egy másik könyvben nem véletlen-szerű találat van; különben **igazolatlan, nem
   jelölt: 7087 token** (ezeknél a hely létezik, de a Strong-próba nem igazolja — eltérő
   Strong-címke, emendáció, versszámozás; hiba-bizonyíték nincs, ezért nem kerültek a táblára).
3. **Jelöltek**: minden ÓSZ-könyv, ahol a c:v létezik; versszám-túllépésnél ugyanabban a könyvben
   az egyjegyű eltérés, a jegy-kiesés és a felcserélt szomszédos jegyek a versben és a fejezetben
   (`21:83 → 21:33`, `18:82 → 18:28`); összeolvadt alaknál a szám kettévágása (`33:816 → 33:8 16`).
4. **Bizonyosság (a brief 3.4):** három feltétel: (a) a független forrás egyezik, (b) a vers
   létezik, (c) Strong-próba (TAHOT ±1). 3 → `magas`, 2 → `kozepes`, a többi `kezi`.

Értelmezések, amelyek a brief szövegén túlmennek (a DT-F46 (4) pontja kéri a jóváhagyásukat):

- **Versszám-tábla: a Macula (MT) és a TAHOT uniója.** A brief „MT-számozás, TAHOT”-ot ír; a
  TAHOT-kivonat Károli-szerű számozású (Mal 4, Jóel 1–3) és ismert résekkel bír, a BDB MT-t
  követ. A Strong-próba a TAHOT-ot nézi a BDB-helyen és a Macula MT→Károli megfeleltetése
  szerinti helyen is (±1); ahol a TAHOT a fejezetet nem fedi le (ismert rés), ott a Macula.
- **A Strong-próba szelektivitása.** A gyakori szó (`H0834`, `H6213`, `H0413`, `H9005` …) szinte
  minden versben áll, a próbája semmit nem bizonyít. A veletlen találat várható száma
  E = (jelölt helyek) × p^(1+lánc-találatok), p a szó esélye egy véletlen 3 verses ablakban
  (Macula/TAHOT). A próba „sikeres”, ha E ≤ 0,25 (lehetetlen helynél); létező helynél
  (a forrásbeli hely is lehet jó) E ≤ 0,05 és lánc/csoport-támasz is kell, különben `kezi`.
- **Csoport:** a konvertáló a nyomtatott lánc tagjait gyakran külön tokenekre bontotta
  (`1 Samuel 3:22; 1 Samuel 5:26; 1Sam 15:22; 1 Samuel 29:19` = „Jb 3:22; 5:26; 15:22; 29:19”);
  az egymást követő, azonos könyvre feloldott tokenek (közöttük csak írásjel, szám, `compare`,
  `and`, `also`, `see`, `so`) egymás támaszai. Ugyanabban a könyvben (számjegy-javítás) a lánc
  nem támasz.
- **Kizárások:** arámi szakaszok (Dán 2:4–7:28, Ezsd 4:8–6:18, 7:12–26, Jer 10:11, 1Móz 31:47)
  létező helyein a héber Strong-próba hiánya nem hibajel; bibliográfiai hivatkozás (`De^Job 2:598`,
  `Che^Comm. Isaiah 2:148`) nem igehely; a 0,5 alatti megbízhatóságú szócikkben (a hivatkozott
  helyeken a Strong-szám a címkézésben általában nem áll) a létező hely nem jelölt; könyvnév,
  amely törzs- vagy személynév is (`Dan`, `Samuel` …), angol elöljáró után `kezi`
  (`assigned to Dan 19:41`: a csere a nevet törölné).
- **A brief hibatípusain túl két típus:** `lanc_lehetetlen` (könyv nélküli láncolt hely, amely az
  örökölt könyvben nem létezik: 100, ebből 4-et a token javaslata megold, 96 kézi listán, javaslat
  nélkül — a gépi csere csak tokent cserél) és a jelentésszámhoz tapadt számozott könyv
  (`22Chr 35:9` = 2. jelentés + 2Chr; 12, `osszeolvadt_alak`, kézi, a javítás szóköz-beszúrás
  lenne: könyvnéven túli OCR, a brief „Nincs benne” pontja).

## 3.5 Mérés

### Hibatípus × bizonyosság (csere-tábla: `naplok/BDB_KONYVFELOLDAS_csere.tsv`, 1032 sor)

| hibatípus | magas | kozepes | kezi | össz |
|---|---|---|---|---|
| ψ-maradék (`psi_maradek`) | 0 | 0 | 37 | 37 |
| más könyv érvényes fejezettel | 10 | 34 | 191 | 235 |
| fejezet-túllépés | 1 | 98 | 38 | 137 |
| vers-túllépés | 1 | 174 | 322 | 497 |
| összeolvadt alak | 0 | 0 | 13 | 13 |
| nem leképezett alak | 0 | 3 | 10 | 13 |
| névhiba | 0 | 0 | 4 | 4 |
| láncolt hely, lehetetlen (`lanc_lehetetlen`) | 0 | 0 | 96 | 96 |
| **össz** | **12** | **309** | **711** | **1032** |

A kézi lista (`naplok/BDB_KONYVFELOLDAS_kezi.tsv`, 711 sor, szövegkörnyezettel): 299 sornak van
javaslata, 412-nek nincs. Okok: több egyenrangú jelölt 198; létező hely lánc-támasz nélkül 177;
nincs igazolt jelölt 106; nem szelektív Strong-próba (gyakori szó) 103; láncolt lehetetlen hely 96;
jelentésszám tapadt 12; TAHOT nem igazolja, csak a Macula 8; törzs-/személynév 5; névhiba 4;
szigla (`De`, `En`) 2.

### Érintett szócikkek

| szint | szócikk a forrásban | ebből lefordított (`adat/forditasok.tsv`) | érintett token a fordításban |
|---|---|---|---|
| magas | 12 | 0 | 0 |
| kozepes | 219 | 55 | 89 (mind illeszthető) |
| kezi | 466 | 194 | 373 |
| össz (különböző) | 634 | 217 | — |

A fordításban a token a forrásbeli (hibás) könyv Károli-alakjával áll (`1Sám 3:22`); az
illesztés a szócikken belüli azonos alakú tokenek sorrendjével történik (eltérő darabszámnál nem
cserél, kézi). A nem leképezett alakot (`Chron 7:8`, `Ze 8:17`) a fordító betűhíven vitte át.

### A 13. kapu (fejezetszám) jelzései

- **Előtte, a forráson:** 109 szócikk (a `naplok/BDB_FORDITAS_M0.py --nem-ir` is 109-et mér,
  egyezik a #38 M0-jával). **A fordított sorokon:** 64 / 436 BDB-sor JELZES.
- **Vetítés a forráson** (`--vetit`, semmit nem ír):

  | változat | forrás-csere | fordítás-csere (sor) | 13. kapu utána |
  |---|---|---|---|
  | csak `magas` | 12 | 0 (0) | 108 |
  | `magas` + lehetetlen típusú `kozepes` (a javaslat) | 287 | 76 (48) | 57 |
  | `magas` + minden `kozepes` | 321 | 89 (55) | 57 |
  | + a kézi lista összes javaslata (névhiba nélkül) | 616 | 245 (149) | 34 |

### Az N-F34 maradéka és az N-F34c

- **N-F34** (`naplok/F34_M2_maradek.tsv`, 153 sor): 141 a csere-táblán (37 `psi_maradek`, mind
  `kezi`; a többi valódi típusa szerint, pl. `2Sam 25:18 → 1Sám 25:18`, `Lev 29:5 → 2Móz 29:5` —
  az F34 B/R listája nem csak ψ-hibát tartalmazott); 12 sor **helyesnek bizonyult** (a vers
  létezik, a Strong-próba sikeres: pl. `Ezra 4:21`, `Neh 6:13`, `Hab 3:9`, `Isa 63:13`).
- **N-F34c** (`Dan c:v`): 11 token; `Dan 22:14`, `Dan 22:19` (H8034) → 5Móz (`kozepes`, a
  csoport támasza dönt az 1Móz 22:14-gyel szemben); `Dan 21:15`, `Dan 24:2` (H8478) → 1Móz
  (`kozepes`); `Dan 4:14` (H2742) → Jóel 4:14 (`magas`); 6 kézi (H3117, H4490, H6881, H7489,
  H8478 `Dan 18:4`, H9004). `Lev 28:17` (H0398): kézi, két egyenrangú jelölt (4Móz / Ez 28:17).
  A H8034 fordítássora a #34-ben védett volt (DT-F34c); a csere most ezt is érintené (DT-F46 (5)).

### Tíz jellemző példa

| # | szócikk | forrás | javaslat | típus / szint | indok |
|---|---|---|---|---|---|
| 1 | H3167 | `Ezek 10:15` | Ezsd 10:15 | más könyv / magas | független forrás + Strong; a nyomtatott „Ezr” Ezékielre oldódott (10 ilyen `magas`) |
| 2 | H5838 | `Ezra 12:33` | Neh 12:33 | fejezet / magas | Ezsdrásnak 10 fejezete van; független forrás |
| 3 | H0413 | `1 Samuel 3:22; … 29:19` (4 token) | Jób | vers / kozepes | „only in Job”: a csoport 4 helye mind Jóbban igazolt |
| 4 | H8034 | `Dan 22:19` | 5Móz 22:19 | fejezet / kozepes | az N-F34c példája; a csoport (22:14) dönt |
| 5 | H7389 | `Mal 24:34` (és 6 társa) | Péld 24:34 | fejezet / kozepes | a „Pr” Malakiásra oldódott |
| 6 | H1320 | `1Kin 4:34; 5:10; 5:14; 6:30` | 2Kir 4:34 | más könyv / kozepes | Elizeus és Naamán: a lánc 4/4 a 2Kir-ben |
| 7 | H3867 | `Proverbs 22:77` | Péld 22:7 | vers / kozepes | az audit gyanúja; a 22. fejezetnek 29 verse van |
| 8 | H0413 | `Deut 37:36` | 1Móz 37:36 | fejezet / **kezi** | a felhasználó példája: helyes javaslat, de a אֶל szinte minden versben áll (p = 54%), a próba nem szelektív |
| 9 | H9005 | `Hab 41:47` | 1Móz 41:47 | fejezet / **kezi** | ugyanígy: a ל elöljáró (p ≈ 100%) |
| 10 | H9005 | `cried to Phoenician לַלָּחֶם` | Pharaoh | névhiba / kezi | 1Móz 41:55; a független forrás nem igazolja (a szó a BDB-XML-ben nem áll) — még H5973 `with Phoenician Exod 8:8`, H7588 `name of Phoenician a crash`; a H3117 (`to Phoenician ימם`) nyelvi használat, téves jelölt |

### Saját szúrópróba (értelmezés, nem mérés: `forras=manual`)

A javaslatokat szövegkörnyezetben néztem át (ez nyelvi ítélet, nem lekérdezés):
`magas` 12/12 helyes; `kozepes` lehetetlen típusú (fejezet/vers/nem leképezett, 275 sor) kb.
30 soros mintában kb. 90% helyes; `kozepes` „más könyv érvényes fejezettel” (34 sor, mind
átnézve) kb. 24 helyes, 9 téves, 1 bizonytalan — a tévesek jellemzően eltérő Strong-címkéjű
helyek (H6965 = מָקוֹם-alszócikk, H2063 זֹאת vs. זֶה, H3091 Józsué vs. Jésua, H6270 Atália), ahol
a forrás helye jó, és egy másik könyvben véletlen a találat.

## Korlátok

- A független forrás a szócikkek kb. negyedét fedi, igehelyeik is hiányosak: üres eredménye nem
  negatív lelet (CLAUDE.md 3. szabály).
- A 7087 „igazolatlan” token nem bizonyítottan hibás, de nem is igazolt; nem kerültek a táblára.
- A Strong-próba a TAHOT/Macula címkézésére épül; a BDB szócikk és a Strong-szám nem mindig
  fedi egymást (alszócikkek, arámi alakok, tulajdonnevek).
- A gépi csere tokenszintű: a láncolt (könyv nélküli) hely számhibája (96) és a jelentésszám
  tapadása (12) kézi.

## ⛔ Megállás — DT-F46

A csere-tábla jóváhagyása a `DONTESEK.md` DT-F46 tételében. A 3.6 (gépi csere, 11. és 13. kapu,
`ellenoriz.py`) és a 3.7 (lezárás, N-F34/N-F34c, ellenőr, PR) csak a döntés után fut.
