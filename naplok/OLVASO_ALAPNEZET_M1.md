# OLVASO_ALAPNEZET — M1: vázszerkezet (#134)

*FELADATOK #134 · ág: `claude/olvaso-alapnezet` · 2026-10-23 · modell: claude-opus-5-5 · a brief: `F134_OLVASO_ALAPNEZET_BRIEF.md`, 3. szakasz M1; a terv: `naplok/OLVASO_ALAPNEZET_M0.md` 5. szakasz, a 9. szakasz döntéseivel (DT-F134f–m)*

Az M1 a felhasználó indítására futott („Az M1 mehet.”, majd „folytasd”). Az M2-t és az M3-at nem indítottam.

## 1. Mi készült

| Elem | Hol | Mit csinál |
|---|---|---|
| **Rétegek a nézetek helyett** (DT294, DT-F134f (b), DT-F134g (c)) | `oldalak.py` (`RETEGEK = ('il',)`, `reteg_ervenyes`, `NEZET_ALNEVEK`), `alkalmazas.py`, `konfig/szerver.toml` | egyetlen réteg, az interlineáris sor (`il`); állapota: `?reteg=` > a régi `?nezet=` (álnév: `interlinearis` → `il`, `olvaso`/`munkaasztal` → réteg nélkül) > a `pardes_reteg` süti > réteg nélkül. A süti csak a `/reteg/il/be\|ki` és a `/nezet/<nev>` útvonalon jön létre (302 a `vissza` címre); a régi `pardes_nezet` sütit a szerver nem olvassa; ismeretlen név 404, süti nélkül. A gyorsítótár-kulcs a réteget tartalmazza. Nincs verslista-réteg. |
| **A nézetváltó kivétele** | `sablonok/alap.html`, `statikus/olvaso.css`, `konfig/elemek.toml` | a fejlécben a nézetváltó helyén a rétegkapcsoló („Interlineáris sor”, be/ki); a body horga `reteg-il` / `reteg-nincs` (+ `lap-nyitva`), a `nezet-*` osztályok megszűntek |
| **Egy elrendezés** | `sablonok/fejezet.html` | a folyó Károli-szöveg (vagy az `il` réteggel a versenkénti csempék, a DT148 (c) szerint) + a részletek lapja; a h1 a fejezet (a vers nem része: a lap mutatja) |
| **A részletek lapja — egy komponens, két mód** (DT293) | `oldalak.py` (`szo_resz`, `vers_resz`, `VERS_FULEK`, `FULBLOKK`), `sablonok/_vers_panel.html`, `sablonok/_szo_panel.html`, `sablonok/fejezet.html` | a meglévő `/r/szo` és `/r/vers` töredékekre épül. **Fejsor:** ‹ (előzmény), cím + alcím (versmódban igehely + a vers eleje; szómódban Strong + héber/görög alak + alapjelentés), ⤢ (csak 900 px alatt), ✕. **Versmód fülei** a mockup FULBLOKK-ja szerint: Vers (a többi vers-blokk) · Kereszthiv. (`vers.kh`, `vers.tsk`) · Témák (`vers.nave`, `vers.tipnr`) · Motívum (`vers.motivum`, `vers.kapcsolat`); a látható blokk nélküli fül kimarad (DT129). **Szómód:** „A vers: … →” hivatkozás a versmódra (vers-kontextusnál). A mód a szerverről érkezik (`?ful=szo` → szómód; vers a címben → versmód, a `?ful=vers\|kh\|temak\|motivum` a fül; `?ful=info` → üres állapot nyitott lapon), tehát JS nélkül is működik. |
| **Üres állapot** (DT-F134l) | `sablonok/fejezet.html` | rövid útmutató (versszám → vers, szó → szó, a jelleg-címkék, az arany számláló), alatta a szövegoszlop forrássora (`szoveg_jegy`) és a számlálók. Nincs fejezet-kalauz, nincs „Másolás forrással” (DT-F134m). 900 px alatt a lapozó sor „Forrás és számlálók” hivatkozása (`?ful=info`) nyitja meg. |
| **JS** | `statikus/olvaso.js` | töredék-betöltés a versszámra, a szóra, a csempe- és a töredékbeli szó-hivatkozásokra (ugyanazon a fejezeten a versekre); fülváltás a lapon; előzménylánc (verem, legfeljebb 20, azonos egymás utáni állapot nem ismétlődik; a fülváltás nem új állapot); ✕ (900 px alatt bezár, fölötte vissza az üres állapotba), ⤢, Esc; a címsor (`history.replaceState`) az állapotot követi; hibánál a teljes lap töltődik. A helyi beállítások (jelölés, téma) változatlanok. |
| **Két alak** (DT293) | `statikus/olvaso.css` | 900 px-től a lap állandó, ragadós oldalblokk (rács: `1fr` + 320–440 px); 900 px alatt (egyetlen töréspont: `max-width: 899.98px`) alulról felugró lap, 48vh betekintés, ⤢: `100dvh − 28px`; nyitott lapnál a szöveg alja 52vh párnát kap, a koppintott vers a lap fölé gördül. A színek tokenekből (árnyék: `color-mix` a `--fg`-ből), betű/sorköz/lekerekítés csak tokenből (`teszt_arculat.py`). |
| **Regiszter** | `konfig/elemek.toml`, `regiszter_or.py` | a nézetváltó két eleme helyén a rétegkapcsoló két eleme (azonos tokenekkel); a verslista helyén a lap gombja (`lap-gomb`); az elemszám marad 83. A `[kizart]` lista: ki a nézetek rács-, panel- és body-horgai, be a lap és a réteg szerkezeti és JS-horgai, indokkal. A `nezet-` dinamikus előtag megszűnt. A regiszter-őr: 0 hiba. |
| **Export** (DT-F134h (a)) | `export.py` | az új elrendezés, rétegek nélkül (`ALAP_RETEG`), ugyanabból a sablonból; teszt őrzi |
| **Szövegjegy** | `blokkok.py` | `szoveg_jegy_html(kozos, il=False)`: a nézet-paraméter helyett a réteg |

Ami az M1-be **nem** került (a brief szerint az M2/M3): a fejléc nélküli kis képernyő, a navigációs lap, a tájoló pirula, a húzás, a kereső javaslatlistája (DT-F134k), a világos alaptéma, a `--g-*` tokenek, a mockup komponensstílusai. A fejléc 900 px alatt ma is a lap tetején áll (ez az M2).

## 2. Ellenőrzés böngészőben (saját próba, nem független ellenőrzés)

*Módszer: ideiglenes fejlesztői szerver a WSL-ben (127.0.0.1:8799, `belso`, WSL-natív `pardes.db`), a beépített böngészőpanel, mérőszkript (`getBoundingClientRect`). Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 @00c512e3 | forras=bongeszo-meres | ts=2026-10-23`.*

- 931 px (oldalblokk): szóra koppintás → szómód (`H7121`, a ‹ megjelenik, a cím `/1Moz/1/5?szo=H7121&ful=szo`); „A vers: … →” → versmód (`1Móz 1:5`); Kereszthiv. fül → a `kh` tartalom látszik (`?ful=kh`); ‹ → vissza a szómódra; ‹ → vissza az 1Móz 1:3-ra, a ‹ eltűnik. Konzolhiba (CSP is) nincs.
- 375 px: kijelölés nélkül a lap rejtett (teteje 831 px, a képernyő alatt); versszámra (1Móz 1:20) a lap 422 px-nél nyílik (390 px magas), a vers teteje 8 px-en, a lap fölött; ⤢ után a lap teteje 28 px; ✕ után zárva, üres állapot, nincs kijelölés, a cím `/1Moz/1`. Vízszintes túlfolyás: 0 (`scrollWidth` 375).

A teljes mérés (375 / 768 / 920 / 1280 px, a brief 6. szakaszának táblázata, valódi telefon) az M4.

## 3. Tesztek

*Futtatás: `python eszkozok/teszt_futtat.py --gyors` (WSL `pardes`, venv Python 3.12.3, WSL-natív `~/pardes/pardes.db`, 895 MB, `epites_ts` 2026-10-14T09:35:00Z — a DT300 szerinti régi adatbázis). Proveniencia: `scope=eszkozok/olvaso_szerver teszt_*.py (--gyors, teszt_szintek.py nélkül) | forras=teszt_futtat.py | ts=2026-10-23`.*

| Fájl | Az M1 előtt (a767d074) | Az M1 után | Megjegyzés |
|---|---|---|---|
| `teszt_arculat.py` | 22 / zöld | 22 / zöld | |
| `teszt_bdb_vers_jelentes.py` | 26 / zöld | 26 / zöld | |
| `teszt_indito.py` | 39 / zöld | 39 / zöld | a sablon-kontextus `nezet`/`nezetek` kulcsa helyett `reteg`/`il` |
| `teszt_kereses.py` | 36 / zöld | 36 / zöld | „minden nézetből” → réteggel és nélküle |
| `teszt_olvaso_szerver.py` | 78 / 2 piros | 86 / 2 piros | a süti- és nézet-tesztek a rétegekre írva; új: álnevek, `/reteg/…`, a régi süti nem hat, `TestReszletekLapja` (6 teszt: üres állapot, fülek és blokk-kiosztás, szómód, töredékek fejsora, a JS, az export) |
| `teszt_pilot_aranymintaval.py` | 22 / 2 piros | 22 / 2 piros | a „mindhárom nézetben” tesztek a két rétegállapotra |
| `teszt_tervezo.py` | 48 / zöld | 48 / zöld | `LAPOK` a rétegekre és a lap módjaira; a regiszter elemszáma 83 marad |
| **összesen** | **271, ebből 4 piros** | **279, ebből 4 piros** (1 kihagyott teszt mindkét futásban) | |

**A 4 piros mind a régi adatbázis ismert esete (DT299), az M1 előtt is piros volt, és nem a #134 hibája:** `TestD2PilotEgyezes.test_1moz_1_25` (`vers:macula`), `TestD2PilotEgyezes.test_zsolt_22` (`vers:tsk_darab`), `test_heber_csempe_szavankent_a_pilot_szerint` (1Móz 1:9 LXX-alak: συναξθήτω / συναχθήτω), `test_szamlalok_egyeznek_a_pilottal` (könyvszám 57 / 61). **Új piros: 0.**

A lassú `teszt_szintek.py` (DT129, hozzáférési szintek) nem futott (`--gyors`); a fájl nincs az `ir`-ben, és nem változott: a `fejezet_lap` 4. paramétere a régi nézetnevet álnévként elfogadja, így a hívásai (`'olvaso'`, `'interlinearis'`) változatlanul érvényesek. A teljes futás az M5-é.

## 4. Nyitott kérdések, megjegyzések

1. **A régi `?nezet=` címek** a naplókban (pl. `naplok/TERVEZO_MOD_zaras.md`) álnévként működnek; a `teszt_tervezo.py` `LAPOK` listája már a rétegeket és a lap módjait (`?ful=info|kh|temak|motivum`) méri.
2. **A fülváltás nem kerül az előzményláncba** (a ‹ módot vagy tartalmat lép vissza, fület nem). Ha a mockup a fület is lépteti, az M4 vizuális összevetése mutatja meg; ez nem tartalmi döntés, az M2/M4-ben igazítható.
3. **A fejezetcím** (h1) a fejezetet mutatja, a verset nem (a JS-váltásnál nem frissülne); a vers a lap fejsorában áll.
4. Munkamódszer: egy csere-szkript (a `oldalak.py` két paraméternevének átírása) egyszer inline heredocban futott magyar szöveggel; a többi szkript fájlból futott. Kár nem keletkezett (a diff ellenőrizve), a szabály (CLAUDE.md, Shell) ettől még áll.
