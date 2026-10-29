---
feladat: 124
cim: Előremutató gerinc-scan — gerinc-kártya a tanulmány A3b lépéséhez és prioritási térkép a következő igeszakasz kiválasztásához
kod: GERINC_KARTYA
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: fut
ad: determinisztikus, provenienciás gerinc-kártya egy igeszakaszra (a meglévő motívumok gerinc-elemei, kollokáció, állapotjelölés, a #110 szűrője a tág Strongokon) a vak olvasás után, kártya ↔ kulcsszó-táblázat összevetéssel; és egy ütemezett, gépi prioritási térkép a teljes Bibliára (hol sűrűsödnek a feldolgozatlan gerinc-találatok), GitHub Actionből, modell és költség nélkül; adatot nem ír, minden jelölt a jeloltek.tsv-n át, döntéssel
kovetkezo: a független ellenőr javítókörének lezárása, majd a draft PR; a 2.3 szöveg jóváhagyása után a #125
olvas: [adat/motivumok.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/kulcsszavak.tsv, adat/grammatikai_strongok.tsv, adat/SEMA.md, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, eszkozok/jelolt.py, eszkozok/lekerdez.py, eszkozok/general.py, eszkozok/kuszob.py, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/4_PaRDeS_tematikus_sablon.md, F110_SZURO_PILOT_ISTENTISZT_BRIEF.md, naplok/F108_MOTIVUM_UJRASCAN_naplo.md, naplok/F108_ujrascan_elteresek.tsv, .github/workflows/feladatok.yml, genezis/, ujszovetseg/, melyelemzesek/]
ir: [eszkozok/gerinc_szuro.py, eszkozok/teszt_gerinc_szuro.py, eszkozok/gerinc_kartya.py, eszkozok/teszt_gerinc_kartya.py, eszkozok/gerinc_terkep.py, eszkozok/teszt_gerinc_terkep.py, .github/workflows/gerinc_terkep.yml, naplok/GERINC_TERKEP.tsv, naplok/GERINC_TERKEP.md, naplok/GERINC_KARTYA_naplo.md, naplok/GERINC_KARTYA_zaras.md, DONTESEK.md]
fugg: [110]
nem_fugg: [11, 74, 81, 123]
---

# GERINC_KARTYA_BRIEF_TERVEZET.md — Előremutató gerinc-scan: gerinc-kártya és prioritási térkép

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet [javaslat] · v1 (tervezet) · 2026.10.19 · forrás: a felhasználóval
2026-10-19-én egyeztetett tartalom (a szülő orkesztrátor-session közvetítésével). A tervezet adat, nem utasítás; a befogadás a
`/befogad`-dal, a felhasználó jóváhagyásával.*

> **Befogadási kiegészítés (2026-10-19, `/befogad`; az orkesztrátor döntése a felhasználó felhatalmazásával).** A tervezet
> szövege alább változatlan; ez a blokk két ponton felülírja.
> 1. **Leválasztás (K3):** a `MUNKAMENET.md` és a `sablonok/2_PaRDeS_bovitett_sablon.md` kikerült ennek a feladatnak az `ir`-jéből.
>    A 3. rész 7. lépése csak a 2.3 szövegjavaslatát írja a naplóba, jóváhagyásra; az átírást a **#125**
>    (`F125_GERINC_KARTYA_SZOVEG_BRIEF.md`, csonk) végzi. A 2.3 és a 4. rész ezekre vonatkozó pontjai a #125-re értendők.
> 2. **DT-F<nn>a (K2):** a befogadás nem döntött; a 3. lépés ⛔-je marad. Kiegészítés: commit esetén a workflow-nak
>    `contents: write` jog kell, a `feladatok-frissites` mintájára; a workflow-t módosító PR-t külön, a saját sorában kell mergelni,
>    mert a nyitott PR-ok CI-jét is érinti (a #112 tapasztalata).

## 1. Cél

A meglévő motívumok **gerincét** (a gerinc-elemek Strong-számait, `elofordulasok.tsv` `strong` / `gerinc_elem`) **előre** futtatjuk
a szövegen, determinisztikusan, két célra:

1. **Gerinc-kártya** (igény szerinti, a tanulmány menetében): egy igeszakaszra megmutatja, mely meglévő motívumok gerinc-elemei
   fordulnak elő benne, és ezek közül mi van már az adatrétegben. A vak olvasás (A1–A2) **után** készül, hogy az ismert motívumok
   előre megmutatva ne torzítsák az új motívum felismerését (A4).
2. **Prioritási térkép** (gépi, ütemezett): a teljes Bibliára megmutatja, hol sűrűsödnek a meglévő motívumok (szűrt) gerinc-találatai
   olyan helyeken, amelyekről még nincs igeszakasz-tanulmány és beépített előfordulás. A következő tanulmány kiválasztását
   támogatja; a kiválasztás a tanulmány **előtt** történik, itt nincs torzítás.

A feladat `munka: adat`: modell nélkül fut (CLI-ből és GitHub Actionből), költsége nincs. A javasolt végrehajtó modell `sonnet`
(szkript, teszt, workflow írása). A kimenet **csak jelölt**: semmi nem kerül közvetlenül tanulmány-sorba vagy az
`elofordulasok.tsv`-be (CLAUDE.md 2. szabály); a minősítés a B5 emberi döntése marad.

## 2. Hatókör

### 2.1 Gerinc-kártya — `eszkozok/gerinc_kartya.py`

**Helye a menetben: a vak olvasás után, az A3b helyén.** Az A1 (a szakasz PaRDeS-feldolgozása) és az A2 (kulcsszó-táblázat)
kártya nélkül készül; az A3 (`betolt.py kulcsszo`) után fut a kártya, és a mai `jelolt.py --szakasz` jelöltlistáját bővíti.

*Technikai döntés (a végrehajtó ezt követi):* a kártya **új modul**, amely a `jelolt.py` függvényeire épít (`szakasz_strongok`,
`elofordulas_strong_index`, `jelolt_sorok_szamit`), a `jelolt.py` maga **változatlan**. Ok: a #110 a `jelolt.py`-t olvassa, a
`jelolt.py` írása ezért levezetett függést adna a #110-nek erre a feladatra, miközben ez a feladat a #110-től függ (kör). A
`jelolt.py --szakasz` a régi kimenettel tovább fut; a MUNKAMENET A3b-sora a kártyára mutat (2.3).

**Tartalom (soronként egy motívum-ID + igehely + Strong):**

1. **Gerinc-találat:** a szakasz minden Strongja (TAHOT + TAGNT, a `grammatikai_strongok.tsv` szerint szűrve), amely egy meglévő
   motívum gerinc-elemén áll; a `+`-os összetett gerinc-elemek tagonként (mint a `jelolt.py`-ban), és a sor megnevezi, **melyik
   gerinc-elemen lóg** (`gerinc_elem`; CLAUDE.md, „Kutatási menet”).
2. **Kollokáció:** az összetett gerinc-elemnél (pl. `H7121+H8034`) külön jelzés, ha a gerinc-elem **minden tagja egy versben** áll
   (a `lekerdez.py kollokacio` logikája szerint). A csak egy taggal álló sor `egy_tag` jelzést kap.
3. **Állapot:** `már előfordulás` (id + igehely az `elofordulasok.tsv`-ben) · `már jelölt` (a `jeloltek.tsv`-ben; a `dontes` értékével:
   `nyitva` / `elutasítva` / `beépítve`) · `új`.
4. **Szűrő a tág gerinc-Strongokon:** a #108 által tágnak mért gerinc-Strongokon (H3548, H7451, H2403, H0127, H1121+H0430,
   H7121+H8034, H7843, H7043, H5315+H2416, H2555; `naplok/F108_MOTIVUM_UJRASCAN_naplo.md`) a **#110 szűrője** fut, ahol a #110
   géppel alkalmazható szabályt adott (DT283). Ahol nincs (a #110 csak az ISTENTISZT-001-re ad szabályt; a többi motívum tág
   Strongjainak szűrése külön tétel), a sor `szuretlen_tag` jelzést kap, és a kártya összesítője külön számolja. A szűrő kizárta sor
   nem tűnik el: `kiszurve: <ok>` jelzéssel a kártya mellékletébe kerül.
5. **Formulaikus motívum:** a `jelolt.py` szerinti `pozicionális ellenőrzés kell` jelzés megmarad.
6. **Proveniencia:** minden lekérdezés (a szakasz Strong-halmaza, minden kollokáció, a szűrő futása) saját proveniencia-sort ad,
   a `lekerdez.py` alakjában (`scope=range:<szakasz> | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | strong=… | n=… | ts=…`),
   **0 találatnál is** (CLAUDE.md 1. szabály). *(A mai `jelolt.py` nem ír proveniencia-sort; ezt a kártya pótolja.)*

**Összevetés: kártya ↔ kulcsszó-táblázat (új lépés, `--osszevet <tanulmány-útvonal>`).** A kártya (igehely, Strong) párjait a
`kulcsszavak.tsv` ugyanazon tanulmányhoz tartozó soraival veti össze (az A3 írja, SEMA 2.8):

- **„Kártya talált, olvasás nem”** = elmulasztott ismert motívum-előfordulás. Javítandó: a kutató megnézi, és ha a hely a motívumhoz
  tartozik, a jelölt a `jeloltek.tsv`-n át, döntéssel kerül be; a motívum ⭐ számlálásában így, a B5 döntés után számít.
- **„Olvasás talált, kártya nem”** = a kulcsszó egyetlen meglévő gerinc-elemen sem áll: **új motívum gyanúja** → A4 ⛔ (emberi döntés,
  a CLAUDE.md négy kérdése szerint). A lista nem dönt; csak az A4 bemenete.
- **Mindkét lista a tanulmány kereszthivatkozás-naplójába kerül, üres eredménynél is** (explicit „üres” jelöléssel; CLAUDE.md 3.
  szabály). A naplóba írás kézi (a napló forrásréteg); a kártya a két listát beilleszthető Markdown-blokként adja.

**Kimenet:** stdout, és `--md <fájl>` esetén `# GENERÁLT: gerinc_kartya.py …` fejlécű Markdown. Javasolt helye a tanulmány
mellett: `[könyv-mappa]/naplok/[tanulmány-név]_gerinc_kartya.md` — ez generált fájl a forrás-könyvtárban, ezért N-F<nn>a nyitott
(a helye vagy `naplok/kartyak/`).

**Írás:** a kártya alapértelmezésben **nem ír táblát**. `--ir` esetén, mint a `jelolt.py --ir`: csak az `új` sorok a `jeloltek.tsv`
végére `dontes=nyitva`-val, a `forras_kereses` mezőben a lekérdezés proveniencia-sorával; `beépítve`/`elutasítva` értéket soha nem
ír; írás előtt sorösszevetés az eredetivel, eltérésnél megállás (minta: `eszkozok/igazolas_migracio.py`); a `szuretlen_tag` és a
`kiszurve` sorok **nem** íródnak be (DT184: a szűretlen tág bevétel elvetve).

### 2.2 Prioritási térkép — `eszkozok/gerinc_terkep.py` + `.github/workflows/gerinc_terkep.yml`

**Számítás (determinisztikus, a teljes TAHOT + TAGNT-en):**

1. Minden motívum minden gerinc-elemére teljes scan (a `lekerdez.py scan`/`kollokacio` logikájával), grammatikai szűrés, a tág
   Strongokon a #110 szűrője (2.1/4.; szűrő nélkül `szuretlen_tag`, külön oszlopban, a sűrűségbe nem számít).
2. Kizárva: az (id, igehely), amely `elofordulasok.tsv`-sor, vagy `jeloltek.tsv`-sor `elutasítva`/`beépítve` döntéssel; a `nyitva`
   jelölt külön oszlopban számít (már látott, el nem bírált hely).
3. Kizárva: a már feldolgozott igeszakasz (van róla igeszakasz-tanulmány). A lefedettség forrása a tanulmányfájlok neve
   (`genezis/1Moz_12v1-20_bovitett.md` → `1Móz 12:1-20`; `ujszovetseg/`, `melyelemzesek/`); a 0. lépés méri, hogy a nevek
   géppel értelmezhetők-e, és a nem értelmezhetőket listázza. Ha a mérés szerint nem elég, ⛔ (DT-F<nn>d: kézi lefedettségi
   lista az adatrétegben, vagy a névből levezetés).
4. Egység: **fejezet** (könyv + fejezet). Rangsor lexikografikusan, súlyok nélkül: (különböző motívumok száma, kollokációs
   találatok, összes szűrt találat), egyezésnél kanonikus sorrend. Súlyozott pontszám nincs: az önkényes súly nem determinisztikus
   állítás.

**Kimenet (csak az Action írja; helyben `--kimenet <ideiglenes könyvtár>`, a repón kívül — CLAUDE.md, `generalt_proba/`-szabály):**

- `naplok/GERINC_TERKEP.tsv` — fejezetenként: `konyv`, `fejezet`, `motivum_db`, `motivumok`, `kollokacio_db`, `talalat_db`,
  `nyitva_db`, `szuretlen_tag_db`, `proveniencia`; első sora `# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes |
  forras=… | bemenet=<a bemeneti fájlok git blob-hash-e> | ts=<a legutóbbi bemeneti commit ideje>`.
- `naplok/GERINC_TERKEP.md` — rövid összesítő: a legjobb 20 fejezet, motívumonkénti számok, a `szuretlen_tag` arány
  motívumonként (jelzi, hol kell még szűrő), a lefedettség-mérés hibái.
- **Idempotencia:** a `ts` és a proveniencia a bemenetből származik (blob-hash, a bemeneti commit ideje), nem a futás idejéből;
  változatlan bemenetre a kimenet bájtra azonos, tehát az Action nem commitol (a `feladatok-frissites` mintája: nincs diff → nincs
  commit).

**Futás (GitHub Action, `gerinc_terkep.yml`):**

- `on: push` a `main`-re, `paths:` `adat/motivumok.tsv`, `adat/elofordulasok.tsv`, `adat/jeloltek.tsv`,
  `adat/grammatikai_strongok.tsv`, a szűrő fájlja (N-F<nn>b: a #110 után nevezendő meg), `eszkozok/gerinc_terkep.py`;
  tartalékként heti `schedule` (cron); és `workflow_dispatch`.
- A `feladatok.yml` mintája: `[bot]` actor kimarad, `concurrency` csoport, a `pardes-feladatok` App tokenje (a `main` ruleset
  egyetlen bypassa), `git pull --rebase` a push előtt, commit-üzenet UTF-8 fájlból.
- **DT-F<nn>a (⛔ nyitott):** a kimenet (a) **commit a `main`-re** a fenti mintával, vagy (b) **csak Action-artifact** (letölthető,
  a repóba nem kerül). Az (a) a `naplok/`-ba ad verziózott, olvasható térképet, de a `main`-re író második gép-Action (az App
  jogosultságát erre is ki kell terjeszteni, és a két Action push-a egymásra rebase-el); a (b) egyszerűbb és nem érinti a
  `main`-t, de a térkép nincs a repóban, és a `/kovetkezo` nem olvashatja. **Javaslat: (a)**, mert a térkép a következő tanulmány
  kiválasztásának bemenete, és a repó-adatból a repóba kell kerülnie; ha az (a) mellett a CI E28 (generált nézet egyezés) a
  térképet is ellenőrizné, a végrehajtó a `eszkozok/ellenorzes/e28_migralt_nezetek.tsv`-be nem veszi fel (külön tétel).

### 2.3 A sablon és a MUNKAMENET módosítása (javaslat — a végrehajtó a ⛔ jóváhagyás után írja át)

- **`MUNKAMENET.md`, A3b-sor:** „jelölt-generálás meglévő motívumokhoz → **gerinc-kártya** (a vak olvasás után)”; ma mivel fut:
  `eszkozok/gerinc_kartya.py --szakasz "…" --osszevet <tanulmány>`; megjegyzés: az A1–A2 kártya nélkül készül (A4 torzítás); a
  kártya csak jelölt, `--ir` csak `új` sort ír `nyitva`-val; a `jelolt.py` régi kimenete megmarad.
- **`MUNKAMENET.md`, új A3c-sor:** „kártya ↔ kulcsszó-táblázat összevetés” — végrehajtó (`gerinc_kartya.py --osszevet`) + kutató;
  kimenet: két lista a kereszthivatkozás-naplóba, üresen is; a „olvasás talált, kártya nem” lista az A4 ⛔ bemenete.
- **`MUNKAMENET.md`, B-szakasz előtt / „Mi hiányzik” után:** egy mondat a prioritási térképről (a következő igeszakasz kiválasztása,
  `naplok/GERINC_TERKEP.md`, gépi, ütemezett).
- **`sablonok/2_PaRDeS_bovitett_sablon.md` (v21 → v22):** a 2. pont után egy rövid bekezdés: „A kulcsszó-táblázat a gerinc-kártya
  **előtt** készül (vak olvasás). A kártya és az összevetés két listája a 4. pont kötelező naplójába kerül, üres eredménynél is; a
  „kártya talált, olvasás nem” hely jelöltként a `jeloltek.tsv`-n át, a „olvasás talált, kártya nem” kulcsszó az A4 elé.” A 2. pont
  3. kiválasztási szempontja („Motívum-kapcsolódás”) **nem** hivatkozik a kártyára (a vak olvasás alatt nincs kártya); erre a
  bekezdés egy mondatban utal. A changelog-sor a fájl elején.
- A `4_PaRDeS_tematikus_sablon.md` P1–P7 nem változik: a kártya az igeszakasz-tanulmány eszköze, a tematikus study a B2–B4-et futtatja.

### 2.4 Opcionális előminősítés — **nem a feladat része**, csak nyitott opció

Egy modell (pl. Sonnet, Message Batches API, `high` erőfeszítés, a #22 mintájára, költségplafonnal) a szűrőn átjutott
jelöltekhez rövid javaslatot írhatna. A kimenete csak javaslat; a B5 emberi döntés marad; a keret a felhasználó döntése.
**DT-F<nn>b (nyitott), alapértelmezés: kimarad.** Ez a feladat ehhez semmit nem épít, és nem készít elő.

### Nincs benne

- a `jeloltek.tsv` tömeges írása (a térkép nem ír táblát; a kártya `--ir` csak kérésre, egy szakaszra);
- a többi motívum tág Strongjainak szűrő-szabálya (a #110 utáni külön tétel(ek)); itt csak `szuretlen_tag` jelölés;
- az `elofordulasok.tsv` írása, a tanulmányok és a lexikon;
- a `lekerdez.py` `--lepes` értékkészletének bővítése (A3b-kód) és az `auditok.tsv` írása: a kártya proveniencia-sorai a kártyában
  és a naplóban állnak (az `auditok.tsv` motívumszintű, DT103);
- a #81 Károli-ujjlenyomata (magyar szóalak-út); a térkép a Strong-utat számolja, a kettő később összeköthető (N-F<nn>c);
- a 2.4 előminősítés.

## 3. Lépések (⛔ a kötelező megállások)

1. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév kiírása, összevetés a fejléc `modell` mezőjével; eltérésnél megállás.
2. **0. mérés** (a `naplok/GERINC_KARTYA_naplo.md`-be): (a) a motívumok gerinc-elemeinek listája az `elofordulasok.tsv`-ből
   (`gerinc_elem`, `strong`), motívumonként; (b) a #110 kimenete: van-e géppel alkalmazható szűrő-szabály, és hol áll; (c) a
   tanulmányfájl-nevek értelmezhetősége (2.2/3.); (d) próbakártya három szakaszra (egy feldolgozott genezis-szakasz, amelynek
   ismert előfordulásai vannak; egy feldolgozatlan; egy ÚSZ-szakasz), a `jelolt.py` kimenetével összevetve (a kártya `jelolt.py`-sorai
   azonosak).
3. ⛔ **DT-F<nn>a** (commit vagy artifact) és — ha a 2/c mérés szerint kell — **DT-F<nn>d** (lefedettségi forrás) a `DONTESEK.md`-be,
   kérdés, opciók, javaslat; megállás. A DT-F<nn>b (előminősítés) a tételben nyitva marad, alapértelmezés: kimarad.
4. `eszkozok/gerinc_kartya.py` + `eszkozok/teszt_gerinc_kartya.py` (pozitív és negatív esetek: 0 találat, összetett gerinc egy taggal,
   tág Strong szűrővel és szűrő nélkül, `--osszevet` mindkét listája üresen is, `--ir` sorösszevetése). A CLAUDE.md shell-, kódlap- és
   TSV-szabályai szerint (`split('\t')`, a wrapper az importok után).
5. `eszkozok/gerinc_terkep.py` + `eszkozok/teszt_gerinc_terkep.py` (idempotencia: két futás bájtra azonos; kizárási szabályok;
   rangsor-stabilitás). Próbafutás `--kimenet`-tel, ideiglenes könyvtárba a repón kívül; a legjobb 20 fejezet a naplóba.
6. `.github/workflows/gerinc_terkep.yml` a DT-F<nn>a döntése szerint; a `feladatok.yml` mintája (2.2). A workflow ágon nem fut le
   írással; a próbája `workflow_dispatch` a merge után (a felhasználó lépése).
7. ⛔ **A 2.3 szövegmódosítások** (MUNKAMENET A3b/A3c, 2_ sablon v22) szövege a naplóba, jóváhagyásra; megállás. Jóváhagyás után az
   átírás, külön tételcommitban.
8. Zárás: `naplok/GERINC_KARTYA_zaras.md`, a brief fejlécének frissítése, `fuggetlen-ellenor`.

## 4. Elfogadási feltételek

- A kártya minden sora megnevezi a motívum-ID-t, az igehelyet, a Strongot és a `gerinc_elem`-et, és állapotot kap (`már előfordulás`
  / `már jelölt: <dontes>` / `új`); minden lekérdezés proveniencia-sort ad, 0 találatnál is.
- A kártya a három próbaszakaszon a `jelolt.py` minden sorát tartalmazza (eltérés csak a bővítésben: kollokáció, szűrő, proveniencia).
- Az összevetés mindkét listája kiíródik, üres eredménynél explicit „üres” jelöléssel.
- A tág gerinc-Strongok szűretlen sora sem a `jeloltek.tsv`-be, sem a térkép sűrűségébe nem kerül; külön számolva látszik.
- Alapfutásban egyik szkript sem ír adattáblát; a `--ir` csak `új` sort ír `nyitva`-val, sorösszevetés után; az `elofordulasok.tsv`
  változatlan (CLAUDE.md 2. szabály).
- A térkép változatlan bemenetre bájtra azonos; az Action nem commitol, ha nincs diff; a generált fájlok fejléce `# GENERÁLT`.
- A `MUNKAMENET.md` és a 2_ sablon csak a jóváhagyott szöveggel változik.
- A `python eszkozok/feladatok.py ellenoriz` 0 hibát ad; a tesztek zöldek.

## 5. Döntésnapló

- (helyőrző) **DT-F<nn>a** — a térkép kimenete: commit a `main`-re (javaslat) vagy csak Action-artifact.
- (helyőrző) **DT-F<nn>b** — opcionális modell-előminősítés (Batches API, költségplafon); alapértelmezés: kimarad; a keret a
  felhasználóé.
- (helyőrző, feltételes) **DT-F<nn>d** — a tanulmány-lefedettség forrása, ha a fájlnevekből nem vezethető le.
- (helyőrző) **N-F<nn>a** — a gerinc-kártya fájl helye (a tanulmány `naplok/` mappája vagy `naplok/kartyak/`).
- (helyőrző) **N-F<nn>b** — a #110 szűrőjének géppel olvasható helye (a #110 `ir`-je ma csak a `jeloltek.tsv`; a szűrő-szabály a
  naplóban és a DT-F110a-ban áll); az Action `paths:` listája ettől függ.
- (helyőrző) **N-F<nn>c** — a térkép és a #81 Károli-ujjlenyomat összekötése (Strong-út + magyar szóalak-út).

### Függés-indoklás (a `/befogad` számára)

- `fugg: [110]` — a szűrő nélkül a tág gerinc-Strongokon a kártya és a térkép zajos (DT184 (d)); az F108 ~2 400 tág új helye
  szűretlenül elnyomná a valódi jelölteket.
- `nem_fugg: [123]` — a kártya a meglévő adatréteggel dolgozik; a térkép a migráció adatváltozásaival az Actionből frissül.
- `nem_fugg: [11]` — a #11 (`megallt`) a `jeloltek.tsv`-t, a `motivumok.tsv`-t és a 2_ sablont írja; a kártya és a térkép a mindenkori
  adatot olvassa, a 2_ sablon módosítása a 7. lépés ⛔-je után, a main friss állapotára készül.
- `nem_fugg: [74]` — a #74 a 2_ sablont írja (gépi javítás); a két módosítás más szakaszt érint, sorrend nem kell; ütközésnél a
  később futó feladat a main-ből indul.
- `nem_fugg: [81]` — a #81 csak saját szkriptet és jelentést ír; rokon cél (motívum → új jelölt könyvenként), de független út (N-F<nn>c).
- **Mellékhatás (a `/befogad` döntse el):** a 2_ sablon az `ir`-ben van, ezért a #74 és a #75 (mindkettő olvassa a 2_ sablont)
  levezetett függést kap erre a feladatra, és a 7. lépés jóváhagyásáig várna (próbafutás `feladatok.py fuggesek`-kel, 2026-10-19).
  Ha ez nem kívánatos: a 2.3 szövegmódosítás (MUNKAMENET + 2_ sablon) leválasztható egy kis `munka: folyamat` utótételbe, és
  ebből az `ir`-ből a két fájl kikerül.
- A #108 és a #109 lezárt: függést nem adnak; a #108 eltérés-táblája csak a tág Strongok listájának forrása.
