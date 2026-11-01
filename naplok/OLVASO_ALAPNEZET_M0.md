# OLVASO_ALAPNEZET — M0: előkészítés és terv (#134)

*FELADATOK #134 · ág: `claude/olvaso-alapnezet` · 2026-10-22 · modell: claude-opus-5-5 · a brief: `F134_OLVASO_ALAPNEZET_BRIEF.md`, 3. szakasz M0 ⛔*

Ez a napló az M0 terve. Kód nem készült. A terv a felhasználó jóváhagyására vár; a döntést kérő pontok a `DONTESEK.md`-ben `DT-F134f`–`DT-F134k` helyőrzővel állnak (6. szakasz).

## 1. A #76 zárása a main-en (a `fugg: [76]` feltétele)

- `origin/main` = `e81fe6d0`; a worktree ebből ágazik, és az `origin/main` ennél nem jár előrébb (`git log e81fe6d0..origin/main` üres, 2026-10-22).
- A `F76_OLVASOI_KONKORDANCIA_BRIEF.md` fejléce az `origin/main`-en: `allapot: lezarva`, `pr: 461`; a merge-commit `bed87ada` („Merge pull request #461 from basesoft777/claude/f76-zaras”) az `origin/main` őse.
- A DT298 (🟢) szerint a #76 az M5-tel zárul, az M6/M7 új briefbe kerül; ez oldja fel a #134-et.
- Megjegyzés: a helyi `main` ág elavult (azon a F76 brief még `megallt`); a mérvadó az `origin/main`.

*Proveniencia:* `scope=git origin/main @e81fe6d0 (F76 brief fejléce, git log) | forras=git | ts=2026-10-22`

**Eredmény: a függés teljesül, a #134 indítható.**

## 2. A mockupok olvasása (Artifact `read`)

Mindkét mockup olvasható volt (a saját fiókban, privát).

| Mockup | Változat | Méret | Mit vettem ki |
|---|---|---|---|
| https://claude.ai/artifact/ExAeE1TKsNfuEMutErqsuA | 9. „Csak szöveg + felugró lap”, ver. `1792660119-3840` | 4,88 MB, 985 sor (a 351. sor a tömörített adat, 4,8 MB, nem olvastam) | a 9. változat CSS-e és JS-e (a lap, a navigációs lap, a pirula, a húzás, az előzménylánc, a fejezet-kalauz), az alap stíluslapja és jelölése |
| https://claude.ai/artifact/Scybm5aoGkc7N4Q3EYgm3r | Alap mockup, ver. `1792091902-30d0` | 4,85 MB, 722 sor | az alap stíluslap és jelölés (fejléc, kánon-sáv, könyvválasztó, ⚙ menü, panel, alsó sáv); a 9. változat erre épül |

*Proveniencia:* `scope=claude.ai artifact ExAeE1TKsNfuEMutErqsuA@1792660119-3840, Scybm5aoGkc7N4Q3EYgm3r@1792091902-30d0 | forras=Artifact read | ts=2026-10-22`

### 2.1 A 9. változat szerkezete (amit a szerverre át kell vinni)

- **Töréspont:** egyetlen, `max-width: 900px` (`matchMedia`), ahogy a DT293 rögzíti.
- **900 px alatt:**
  - a `header.top` alulról felugró **navigációs lap** lesz (`position: fixed; bottom: 0`, `transform: translateY(105%)`, nyitva `body.v9-nav`); benne a kereső, a morzsa és könyvválasztó, a ‹ ›, a ⚙ menü (statikusan kinyitva), a kánon-sáv (22 px), és ide költöznek a jelölő chipek, a „Legutóbb” és a „▤ Fejezet-kalauz” gomb (`.v9extra`). Az alsó sáv (`footer.also`) eltűnik, a szókártya (`.kartya`) is.
  - a fejezetcím (`.fejcim h1`, „ ▾” utótaggal) nyitja a navigációs lapot.
  - **a részletek lapja** az `aside.panel`: `position: fixed; bottom: 0; height: 48vh`, nyitva `body.v9-lap`, teljes nézetben `height: calc(100dvh - 28px)` (`body.v9-teljes`); háttér-fátyol (`#v9hatter`) csak teljes nézetben és a navigációs lapnál. A `.jegyzek` alja `52vh` párnát kap, hogy a koppintott vers a lap fölött maradjon (görgetés `scrollIntoView`).
  - **a lap fejsora** (`.v9fogo`, ragadós): fogantyú-pirula, ‹ (előzmény), a cím (igehely + a vers eleje, vagy Strong + héber alak + alapjelentés), ⤢ (teljes), ✕; alatta a műveletsor (`.v9fmuv`: „Másolás forrással”, szómódban „A vers: … →”). A versműveleti sor kis képernyőn a szövegből kimarad, a fejsorba kerül.
  - **húzás** a fejsoron (`pointerdown`/`pointerup`, `setPointerCapture`, `touch-action: none`): fel (−40 px) = teljes, le (+40 px) = betekintés, majd zárás; az Esc a nyitott lapot zárja.
  - **tájoló pirula** (`#v9pirula`): felfelé görgetésre (300 px mélység fölött, 6 px-es küszöb) megjelenik („Ez 37 :5 ▾”), lefelé vagy 2,5 mp után eltűnik; koppintásra a navigációs lapot nyitja.
- **900 px-től:** a panel állandó oldalblokk (ragadós, `top: 110px`), a fejléc egysoros és ragadós, az alsó sáv („Legutóbb”, billentyűk) marad. A ✕ itt „Vissza a fejezet-kalauzhoz”.
- **Módok:** a panel osztályai `v9-ures` (fejezet-kalauz, fülek nélkül), `v9-szo` (szómód, fülsor nélkül), egyébként versmód a fülekkel: **Vers · Kereszthiv. · Témák · Motívum** (+ a Szó fül). A fülek blokk-kiosztása a mockupban (`FULBLOKK`): Kereszthiv. = `vers.kh` + `vers.tsk`; Témák = `vers.nave` + `vers.tipnr`; Motívum = `vers.motivum` + `vers.kapcsolat`; Vers = az összes többi vers-blokk.
- **Előzménylánc:** `{vers, strong, fül}` állapotok verme (legfeljebb 20), az azonos egymás utáni állapot nem ismétlődik; a ‹ visszalép, nem zár.
- **Fejezet-kalauz** (az 5. változatból, a panel üres állapota): öt kártya, mindegyik soronként sávdiagrammal és forrássorral: *Kulcsszavak* (a szöveg pontozott szavainak Strong-gyakorisága, nyelvtani H9xxx nélkül, top 10; forrás: Károli–Strong párosítás, modell-kimenet; alapjelentés: magyar BDB), *Személyek és helyek* (`vers.tipnr`, versek száma), *Témák* (`vers.nave`, top 10), *Motívumok* (`vers.motivum`; üresen: „Ebben a fejezetben nincs lezárt motívum-előfordulás. Üres eredmény, nem negatív lelet.”), *Hová mutatnak a kereszthivatkozások?* (`vers.kh` + `vers.tsk`, célkönyvenként, top 10). A sorra kattintva a megfelelő vers/szó nyílik a megfelelő fülön.
- **Téma:** ha nincs `data-theme`, a mockup `light`-ot állít; a ⚙ menü „Téma” sora Rendszer/Világos/Sötét marad. A „Nézet” sor kikerül.
- **Arculat:** `--g-tor`, `--g-tort`, `--g-bolcs`, `--g-prof`, `--g-kis`, `--g-ev`, `--g-lev`, `--g-apok` világos és sötét értékkel; 32 px-es ikongombok (`.ib`), pirula-chipek (`.chip`, `radius 999px`), árnyékos felugró elemek (`box-shadow: 0 8px 24px rgb(0 0 0 / .18)`, a lapoknál `0 -10px 30px …/.2`), fülsor (`.fulek`, aktív: 2 px-es accent alsó szegély).

## 3. A meglévő kód felmérése (`eszkozok/olvaso_szerver/`)

| Elem | Hol | Mai viselkedés | Érinti-e a #134 |
|---|---|---|---|
| nézetlista | `oldalak.py` 24–26 | `NEZETEK = ('olvaso','interlinearis','munkaasztal')`, `ALAP_NEZET = 'olvaso'`, `nezet_ervenyes()` | igen: rétegekre cserélődik |
| nézet kiválasztása | `alkalmazas.py` 76–78 | `?nezet=` > `pardes_nezet` süti > alap; a gyorsítótár-kulcs része a nézet (96. sor) | igen |
| `/nezet/<nev>` | `alkalmazas.py` 194–202 | 302 a `vissza` címre, ITT jön létre a süti (DT146/4), `Cache-Control: no-store`; ismeretlen név: 404 | igen: kompatibilitási átirányítás (DT-F134f) |
| süti-konfig | `konfig/szerver.toml` [suti] | `nev = "pardes_nezet"`, `szint_nev`, `max_kor_mp`, `secure` | igen (a megjegyzés és esetleg a név) |
| DT148 elrendezések | `sablonok/fejezet.html` 77–109 | Olvasópult: folyó szöveg (`vers_folyo`) + panel fülekkel; Interlineáris: versenként `il-vers` csempékkel + panel `ketto`; Munkaasztal: verslista + versenként `vers_szoveg` + két panel egymás alatt | igen: egy elrendezés + rétegek |
| fejezet-lap | `oldalak.py` 237–293 | az interlineáris adat (`fejezet_eredeti`, `fejezet_parositatlan`) csak `nezet == 'interlinearis'`-nél fut; `szo_html`/`vers_html` szerveroldalon a lapba | igen: réteg szerint |
| szövegjegy | `blokkok.py` 1290 `szoveg_jegy_html(kozos, nezet)` | a forrássor szövege nézetfüggő | igen (`ir`-en kívül, DT-F134j) |
| `/r/szo`, `/r/vers` | `alkalmazas.py` 182–192, `oldalak.py` 212–222 | töredékek (`_szo_panel.html`, `_vers_panel.html`); a JS a szó-kattintást a Szó fülbe tölti; versszámra NINCS JS (teljes lap) | igen: a lap mindkét módja ezekre épül; a versszám is töredékkel nyílik |
| JS | `statikus/olvaso.js` (77 sor) | Ctrl+K, fülváltás, szó-töredék, jelölés-kapcsoló és téma **localStorage**-ban (`pardes_jeloles`, `pardes_tema`), attribútum: `data-tema` | igen: bővül (lap, húzás, előzmény, pirula, nav-lap) |
| téma | `arculat.py` 94–96 | a sötét tokenek `:root:not([data-tema="light"])` (prefers-color-scheme) és `:root[data-tema="dark"]` alatt | igen: alap = világos (DT295) |
| CSP | `alkalmazas.py` 37 | `script-src 'self'; style-src 'self'` — inline szkript és `style=""` attribútum tiltott (`teszt_arculat.py` 222 őrzi) | korlát (4. szakasz) |
| Tervező mód | `alap.html` 12–14, 35–37; `tervezo_statikus/tervezo.js` | csak `belso` kiadásban; a kapcsoló `#tervezo-kapcsolo` a fejlécben; a `tervezo.js` id alapján keresi | a kapcsoló a ⚙ menübe kerül, az id marad |
| regiszter-őr | `regiszter_or.py`, `konfig/elemek.toml` (83 `[[elem]]`) | minden sablon-/JS-osztály regisztrált vagy kizárt; a `nezet-{{ nezet }}` előtagot az `oldalak.NEZETEK`-ből bontja ki; `teszt_tervezo.py` `LAPOK` listája `?nezet=` címekkel méri, hogy minden szelektor talál | igen: új osztályok regisztrálása; a `nezet-` előtag kiváltása (`ir`-en kívül: `regiszter_or.py`, `teszt_tervezo.py`) |
| statikus export | `export.py` 40 | `fejezet_lap(..., oldalak.ALAP_NEZET, ...)` egy könyvre + `arculat.css`; szerver-abszolút hivatkozások (váz) | DT-F134h ⛔ |
| hozzáférési szint | `alkalmazas.py` 204–213, `alap.html` 28–33 | `/szint/<nev>` süti, csak `belso`; a fejlécben | a ⚙ menübe kerül, működése változatlan (E6, DT129) |
| lábléc (#100) | `alap.html` 46–55 | kiadás, ág, commit, építési idő, `role="alert"` figyelmeztetések | marad a lap alján (nem rögzített, tehát nem „tartós sáv”); `teszt_indito.py` őrzi |
| `?nezet=`-től függő tesztek | `teszt_olvaso_szerver.py` (29 hely), `teszt_tervezo.py` (8), `teszt_pilot_aranymintaval.py` (15), `teszt_kereses.py` (3), `teszt_indito.py` (1), `m4_meres.py` (5) | a három nézetet, a sütit és a nézetváltó hivatkozásait mérik | át kell írni (DT-F134j) |

*Proveniencia:* `scope=eszkozok/olvaso_szerver/ @e81fe6d0 (alkalmazas.py, oldalak.py, export.py, blokkok.py, regiszter_or.py, sablonok/alap.html, sablonok/fejezet.html, statikus/olvaso.js, arculat.py, konfig/szerver.toml, konfig/elemek.toml, teszt_*.py) | forras=grep, olvasás | ts=2026-10-22`

## 4. A DT294 alkalmazási terve (mi marad, mi megy, átirányítás)

A DT294 (a) szerint a nézetváltó kikerül, a nézetek helyett rétegek vannak. A terv (a nyitott részletek a DT-F134f és g döntésben):

**Ami megy**
- a `.nezetvalto` navigáció a fejlécből (és a `nezetvalto`, `nezetvalto-aktiv` elem a regiszterből);
- a három elrendezés-ág a `fejezet.html`-ben; helyette **egy** elrendezés: a folyó Károli-szöveg (a DT148 (c) Olvasópult-ága) + a részletek lapja/oldalblokkja;
- a `ketto` (két panel egymás alatt) mód: a DT293 szerint egyetlen komponens van, szó- és versmóddal;
- a `body.nezet-*` horgok (az `elemek.toml` 1014–1016 sorai);
- az útmutató („Hogyan olvasd ezt az oldalt?”) alapból nyitott állapota: az E1 (≤ 200 px az első versig 375 px-en) miatt a fejezetcím melletti „forrás, számlálók és útmutató” kapcsolóba kerül, csukva; ugyanide a számláló-címkék. A szövegjegy (jelleg- és forrássor) ott is elérhető marad (proveniencia-szabály).

**Ami marad**
- a `?szo=`, `?ful=` paraméterek és a `/<könyv>/<fej>/<vers>` címek (szerveroldali lap, JS nélkül is működik): a lap a szerverről nyitott állapotban érkezik;
- a `/r/szo`, `/r/vers` töredékek; a versszámra koppintás is töredékkel tölt (ma teljes lapot kér);
- a funkcionális süti szabálya (DT146/4: csak kapcsoláskor jön létre) — ha a rétegek sütit kapnak (DT-F134f (b));
- a DT148 versenkénti elrendezése az interlineáris rétegben (a csempe a vers egysége), a folyó szöveg az alap.

**Rétegek**
- `il` — interlineáris sor: a mai Interlineáris nézet csempéi; bekapcsolva a szöveg versenként tördelődik (DT148 (c) ennyiben marad).
- `lista` — a munkaasztal verslistája (DT-F134g a helye).
- a „panel” nem réteg többé: 900 px-től állandó, alatta felugró (DT293).

**Régi linkek és a régi süti (javaslat, DT-F134f)**
- `?nezet=olvaso` → réteg nélkül; `?nezet=interlinearis` → `il`; `?nezet=munkaasztal` → `lista`. Álnévként kezelve (ugyanaz a lap, átirányítás nélkül), hogy a könyvjelzők és a naplókban álló mérési címek (pl. `naplok/TERVEZO_MOD_zaras.md` 78–102) működjenek.
- `/nezet/<nev>` → 302 a `vissza` címre a megfelelő réteg-beállítással; ismeretlen név továbbra is 404.
- a régi `pardes_nezet` süti: nem olvassuk tovább (csak a helyi WSL-példányon élt, nyilvános telepítés nem volt, DT298).

## 5. Az M1–M5 bontása fájlokra

| Lépés | Tartalom | Fájlok (`ir` = a brief `ir` mezőjében; **+** = azon kívül, DT-F134j) |
|---|---|---|
| **M1 — váz** | rétegek a `NEZETEK` helyett (`RETEGEK`, érvényesítés, álnevek, gyorsítótár-kulcs); `/nezet/<nev>` kompatibilitás; a részletek-lap komponense (fejsor, fülek a `FULBLOKK` szerint, szó-/versmód, üres állapot) szerveroldalon, a `/r/szo`, `/r/vers` töredékekre építve; a fejezet-kalauz összesítése szerveroldalon (a meglévő lekérdezésekből, a hozzáférési szint láthatóságát követve, kártyánként forrássorral); a két alak CSS-e és az előzménylánc JS-e | `oldalak.py`, `alkalmazas.py`, `sablonok/fejezet.html`, `sablonok/alap.html`, `sablonok/_vers_panel.html`, `sablonok/_szo_panel.html`, új `sablonok/_kalauz.html`, `statikus/olvaso.js`, `statikus/olvaso.css`, `konfig/elemek.toml`; **+** `blokkok.py` (`szoveg_jegy_html` nézet-paramétere), **+** `lekerdezesek.py` (a kalauz összesítő lekérdezései, ha a meglévők fejezetszinten nem elegendők), **+** `regiszter_or.py` (a `nezet-` előtag kiváltása), **+** `konfig/szerver.toml` |
| **M2 — kis képernyő** | fejléc nélküli olvasó; a fejléc navigációs lappá alakul; tájoló pirula; húzás; a versműveletek (Másolás forrással) a lap fejsorában; a ⚙ menü: téma, szint (belső), Tervező kapcsoló (belső), Aa | `sablonok/alap.html`, `sablonok/fejezet.html`, `statikus/olvaso.js`, `statikus/olvaso.css`, `konfig/elemek.toml` |
| **M3 — arculat** | világos alaptéma (DT295, DT-F134i); `--g-*` tokenek (világos + sötét) az `arculat.json`-ba, az `arculat.py` ellenőrzésével; komponensstílusok tokeneken át; kánon-sáv és könyvválasztó műfajszínekkel | `konfig/arculat.json`, `arculat.py`, `statikus/olvaso.css`, `teszt_arculat.py`, `konfig/elemek.toml` (a regiszter magyar nevei az új tokenekhez); **+** esetleg `arculat_szinkron.py` (ha a szinkron a csoportlistát rögzíti) |
| **M4 — mérés ⛔** | a brief 6. szakaszának táblázata szkripttel (375 / 768 / 920 / 1280 px), képernyőképek, vizuális összevetés a 9. változattal; valódi telefon a belső hálón (portproxy, tűzfal: a felhasználó) | új mérőszkript a session scratch-könyvtárában vagy **+** `naplok/OLVASO_ALAPNEZET_meres.md` (a jelentés) |
| **M5 — tesztek, zárás** | `python eszkozok/teszt_futtat.py` (WSL-natív `pardes.db`); a `?nezet=`-es tesztek átírása rétegekre és álnevekre; új tesztek: álnevek, `/nezet/<nev>` átirányítás, süti-szabály, a kalauz üres eredménye, CSP (nincs inline stílus/szkript), regiszter-őr; független ellenőr; zárójelentés | `teszt_olvaso_szerver.py`, `teszt_arculat.py`; **+** `teszt_tervezo.py` (`LAPOK`), **+** `teszt_pilot_aranymintaval.py` („mindhárom nézetben” tesztek), **+** `teszt_kereses.py` (`test_minden_nezetbol_elerheto`), **+** `teszt_indito.py` (a sablon-kontextus `nezet`/`nezetek` kulcsa), **+** `m4_meres.py` (`nezetes()`), **+** `export.py` (DT-F134h), **+** `README.md`, **+** `naplok/OLVASO_ALAPNEZET_zaras.md` |

## 6. Döntést kérő pontok (⛔, a `DONTESEK.md`-ben)

| Helyőrző | Kérdés | Opciók | Javaslat |
|---|---|---|---|
| **DT-F134f** | Hogyan tárolódjon a rétegek állapota, és mi legyen a régi `?nezet=` / `/nezet/<nev>` linkekkel? | (a) csak URL-paraméter (`?reteg=il,lista`), a fejezet- és lapozó hivatkozások viszik tovább; süti nincs · (b) funkcionális süti `pardes_reteg`, csak kapcsoláskor (`/reteg/<nev>/be|ki`), a `?reteg=` felülírja (a DT146/4 rendje, a mai nézetsüti mintájára); a régi `?nezet=` álnév, a `/nezet/<nev>` 302-vel a megfelelő rétegre · (c) kliensoldali réteg (localStorage), az interlineáris sor új töredékből (`/r/il/<könyv>/<fej>`) | **(b)**: a JS nélküli működés és a gyorsítótár-kulcs megmarad, a süti-tesztek átvihetők, a régi linkek nem törnek; új adat vagy új töredék nem kell |
| **DT-F134g** | Hová kerüljön a `lista` réteg (a munkaasztal verslistája), ha a 9. változatban nincs helye? | (a) 1100 px-től bal oszlop (a mockup 1100 px-es lépcsőjénél), alatta a navigációs lapon · (b) csak a navigációs lapon · (c) elmarad; a fejezet-kalauz és a j/k léptetés pótolja | **(a)**: 900–1100 px között a harmadik oszlop a szöveget 300 px-re szorítaná (a 6. szakasz 920 px-es lelete) |
| **DT-F134h** | Statikus export (a brief ⛔): az új elrendezéssel vagy a régivel? | (a) az új elrendezés, rétegek nélkül, ugyanabból a sablonból; a lap JS nélkül olvasható, a szó/vers töredékek a statikus kimenetben nem élnek (a mai váz is szerver-abszolút hivatkozásokkal ír, l. `export.py` docstring) · (b) a régi elrendezés külön sablonban marad · (c) az export ebben a feladatban nem változik, a teljes statikus változat a M6/M7 briefé (DT298) | **(a)**: nincs két sablon karbantartása; a mai viselkedés (fejezet-lapok + `arculat.css` kiírása) megmarad, és ezt teszt őrzi |
| **DT-F134i** | A téma: hol tárolódik, és marad-e a „Rendszer” lehetőség? A brief E5 sütit ír (DT146/DT152), a kód ma localStorage-ot használ (`pardes_tema`, `data-tema`). | (a) localStorage marad; a `<html data-tema="light">` szerveroldali alap; a tárolt választást egy kis, nem halasztott **külső** szkript a `<head>`-ben alkalmazza (a CSP inline szkriptet nem enged), így nincs villanás; Rendszer / Világos / Sötét, alap: Világos · (b) funkcionális süti `pardes_tema` csak váltáskor, a szerver rendereli az attribútumot (a gyorsítótár-kulcs bővül) · (c) mint (a), de a „Rendszer” lehetőség kikerül | **(a)**; az E5 „megmarad” feltétele a localStorage-dzsal teljesül, a brief E5 szövegének „süti” szava így pontosítandó |
| **DT-F134j** | A brief `ir` mezője a 3. és 5. szakaszban **+**-szal jelölt fájlokat nem tartalmazza, pedig a nézetváltó kivétele ezeket érinti (a `nezet`-függő tesztek, a regiszter-őr, a szövegjegy, az export). | (a) az `ir` bővül: `blokkok.py`, `lekerdezesek.py`, `regiszter_or.py`, `export.py`, `konfig/szerver.toml`, `teszt_tervezo.py`, `teszt_pilot_aranymintaval.py`, `teszt_kereses.py`, `teszt_indito.py`, `m4_meres.py`, `README.md`, `sablonok/` (már benne), `naplok/OLVASO_ALAPNEZET_*.md` · (b) az `ir` marad; a belső `nezet` paraméter álnévként él tovább, és a `ir`-en kívüli tesztek változatlanok — de a nézetváltó hivatkozásait és a `nezet-*` osztályt mérő tesztek így pirosak lennének (E6-ütközés) | **(a)** |
| **DT-F134k** | A kereső: a mockup omni-mezője javaslatlistát ad (igehely, Strong, szó, motívum). A szerveren nincs javaslat-végpont, és a hatókör új adatot nem enged. | (a) a meglévő űrlap (`/kereses`, `/ugras`) a mockup stílusában, javaslatlista nélkül · (b) mint (a), plusz kliensoldali javaslat a könyvnevekre és az igehely-mintára (a lapban már meglévő könyvlistából; új végpont nélkül) · (c) új `/r/javaslat` végpont | **(b)** |

Ami **nem** döntés (a jóváhagyott mockupból vagy a briefből jön): a 900 px-es töréspont, a fülek blokk-kiosztása (2.1, `FULBLOKK`), a kalauz öt kártyája és üres felirata, a Tervező és a szintváltó a ⚙ menüben (csak `belso`), a lábléc a lap alján.

## 7. Kockázatok

1. **CSP** (`style-src 'self'`): a kalauz sávjainak `style="width:…%"` attribútuma tiltott. Megoldás: a szélesség JS-ből CSSOM-mal (`el.style.width`, ezt a CSP nem tiltja) vagy `<meter>` elem, vagy lépcsőzetes osztályok; inline `<style>`/`<script>` nem lehet (a `teszt_arculat.py` 222 őrzi). A témát alkalmazó szkript külső fájl.
2. **A regiszter-őr**: minden új osztály (lap, fejsor, pirula, kalauz, chip, kánon-sáv, könyvrács) regisztrálandó vagy kizárandó; a `teszt_tervezo.py` „minden szelektor talál” tesztje a `LAPOK` listán méri, ezért a rejtett (csak JS-sel nyíló) elemeknek a szerverről érkező jelölésben is ott kell lenniük.
3. **A kalauz költsége**: fejezetenként a `vers.tipnr`, `vers.nave`, `vers.motivum`, `vers.kh`, `vers.tsk` összesítése; a Zsolt 119 (176 vers) a legnehezebb. A K5 korlátja (DT221) ismert; az M1 méri, és ha a lap ideje érdemben nő, a kalauz külön töredékbe kerül (lusta betöltés). A kalauznak a hozzáférési szint szerint zárt blokkot nem szabad összesítenie (DT129).
4. **A kulcsszó-kártya proveniencia-jelölése**: a Strong-gyakoriság a Károli–Strong párosításból jön, ami modell-kimenet; a kártya forrássora ezt jelleg-címkével mondja ki (a mockup v5f-sora szerint).
5. **„Másolás forrással”** a telefonon: a `navigator.clipboard` csak biztonságos környezetben (HTTPS vagy `localhost`) él; a belső hálós `http://192.168…` próbán tartalék kell (`document.execCommand('copy')` vagy kijelölés + értesítés).
6. **iOS/Android húzás**: a `touch-action: none` csak a fejsoron; a lap tartalma görgethető maradjon (`overscroll-behavior: contain`). A valódi telefonos próba az M4 része.
7. **JS nélkül**: a szerver a `?szo=`/`?ful=`/vers címekre nyitott állapotú lapot ad (kis képernyőn a lap a szöveg alatt jelenik meg, mint ma); ez az alsó lap tartalék-viselkedése, nem hiba.
8. **Mérési alap**: a K6 a DT300 szerint régi `pardes.db`-n áll; az M5 tesztfutása ugyanezen az adatbázison fut, a D2/macula/tsk és az LXX-alak ismert piros esetei (DT299) nem a #134 hibái, a jelentés külön jelöli őket.

## 8. Megállás

A terv a felhasználó jóváhagyására vár: „Te: az M0-terv jóváhagyása (naplok/OLVASO_ALAPNEZET_M0.md)”, a DT-F134f–k döntésekkel együtt. Az M1 a jóváhagyás után indul.

## 9. A felhasználó döntései (2026-10-22, chat)

Az M0-terv jóváhagyva, a következő módosításokkal (a teljes szöveg a `DONTESEK.md`-ben):

| Tétel | Döntés | Hatás a tervre |
|---|---|---|
| DT-F134f | (b) | egyetlen réteg (`il`); a `?nezet=munkaasztal` is réteg nélkül |
| DT-F134g | (c) | nincs `lista` réteg; a 4. szakasz `lista` eleme ezzel érvénytelen |
| DT-F134h | (a) | az export az új sablonból |
| DT-F134i | (a) | localStorage; az E5 pontosítva |
| DT-F134j | (a) | az `ir` bővült, a `lekerdezesek.py` nélkül |
| DT-F134k | (b) | kliensoldali javaslat könyvnévre és igehelyre |
| DT-F134l | (a) | **nincs fejezet-kalauz**: üres állapotban rövid útmutató + forrás + számlálók; a 7. szakasz 1. (CSP, sávok) és 3. (a kalauz költsége) kockázata megszűnik; a témaszkript CSP-kérdése marad |
| DT-F134m | (c) | **nincs „Másolás forrással”**; a 7. szakasz 5. kockázata megszűnik |

Az M1 a felhasználó külön indítására indul.
