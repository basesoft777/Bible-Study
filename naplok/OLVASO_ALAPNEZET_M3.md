# OLVASO_ALAPNEZET — M3: arculat (#134)

*FELADATOK #134 · ág: `claude/olvaso-alapnezet` · 2026-10-23 · modell: claude-opus-5-5 · a brief: `F134_OLVASO_ALAPNEZET_BRIEF.md`, 2.5, 2.6 és 3. szakasz (M3); a döntések: DT295, DT296, DT-F134i (a); a vizuális mérce: a mockup 9. változata (https://claude.ai/artifact/ExAeE1TKsNfuEMutErqsuA, ver. `1792660119-3840`, Artifact `read`; a mockup-kereteket nem írtam át)*

Az M3 a felhasználó indítására futott („Mehet” a „következő lépés az M3” javaslatra). Az M4-et nem indítottam.

## 1. Mi készült

| Elem | Hol | Mit csinál |
|---|---|---|
| **Világos alaptéma** (DT295, DT-F134i (a)) | `sablonok/alap.html`, új `statikus/tema.js`, `statikus/olvaso.js` | A szerver minden lapon `<html lang="hu" data-tema="light">`-ot ad. A `<head>`-ben a stíluslapok előtt egy külső, nem halasztott szkript (`/statikus/tema.js`, 14 sor) a localStorage `pardes_tema` értékét alkalmazza az első rajzolás előtt: `dark` → sötét, `rendszer` → attribútum nélkül (a token-blokk `prefers-color-scheme` szabálya), minden más → világos. A ⚙ menüben Rendszer / Világos / Sötét, a szerver a Világosat jelöli; az `olvaso.js` alapja ugyanígy a világos. Inline szkript nincs (CSP változatlan). |
| **Műfajszínek** (DT296) | `konfig/arculat.json` | Nyolc új színtoken a mockup 9. változatának világos és sötét értékével: `g-tor`, `g-tort`, `g-bolcs`, `g-prof`, `g-kis`, `g-ev`, `g-lev`, `g-apok` (→ `--g-*`). |
| **Árnyék-token** | `konfig/arculat.json` | `arnyek` (mindkét témában `#000000`, a mockup `rgb(0 0 0 / …)` árnyéka): a felugró panelek, a két alsó lap, a tájoló pirula árnyéka és a fátyol ebből (a kódban eddig az `fg`-ből volt, ami sötét témában világos „fényt” adott volna). |
| **A fejléc térközei** | `konfig/arculat.json` | `space-fejlec-fugg` 10 → 8 px, `space-fejlec-oszlop` 20 → 10 px, `space-fejlec-sor` 12 → 6 px (a mockup `sor1`: `padding-block: 8px`, `gap: 10px`). |
| **Kánon-sáv és könyvválasztó** | `statikus/olvaso.css` | A kánon-sáv téglalapja a `data-mufaj` horgon kapja a színt (`color: var(--g-*)`), a kitöltés ennek 35%-a (`color-mix(…, currentColor 35%, …)`), rámutatva és a mostani könyvnél a teljes szín (+ `fg` keret). A könyvgomb kerete és háttere a műfajszín 40 / 10%-a, rámutatva 28%, a mostani könyv teljes színnel, `panel` szöveggel; a műfaji csoport címe nagybetűs felirat a műfajszín 10 px-es négyzetével. A Pál- és az általános levelek közös színe a `--g-lev` (a mockup szerint). Műfaj nélkül (nem 66 könyves lista) az `accent`. Új adat és új horog nincs (a `data-mufaj` az M2-é). |
| **Egysoros fejléc 900 px-től** | `statikus/olvaso.css` | A fejléc `panel` hátterű; első sora: logó, morzsa, kereső (a sor maradékát kitölti, legalább 280 px-es alapból), ‹ ›, Aa, ⚙; alatta a kánon-sáv (a sor 55%-ától), mellette a jelölés-chip és a „Legutóbb” (900 px-től legfeljebb 3 hely). 920 px-en ma 3 sor helyett 2 (a vezérlők és a kánon-sáv sora). |
| **32 px-es ikongombok** | `statikus/olvaso.css`, `alap.html` | A `.lap-gomb` (‹ › Aa ⚙ és a lap ‹ ⤢ ✕-e) átlátszó hátterű, rámutatva `accent-soft`; nyitott `details`-nél és `aria-pressed="true"`-nál `accent-soft` háttér és `accent` keret (a mockup `.ib[aria-expanded]`-je). A kereső „Keresés” gombja ⌕ ikongomb lett (`aria-label="Keresés"`). A morzsa rámutatva és nyitva ugyanígy. |
| **Pirula-chip** | `alap.html`, `statikus/olvaso.css` | A „Kapcsolt szavak jelölése” kapcsoló `label.kapcs.chip`: pirula, pöttyel; a jelölőnégyzet a chipben rejtve marad (fókuszálható, a címke vált), bekapcsolva `accent` keret, `accent-soft` háttér, `accent` pötty (`:has(input:checked)`); fókusznál a chip kap körvonalat. A kapcsoló szövege és `id`-je változatlan. |
| **Árnyékos felugró elemek** | `statikus/olvaso.css` | A könyvválasztó, az Aa és a ⚙ panelje és a kereső javaslatlistája `0 8px 24px` 18%-os, a két alsó lap `0 -10px 30px` 20%-os, a pirula 15%-os árnyékot kap, a fátyol 30%-os — mind az `arnyek` tokenből. |
| **Fülsor** | `statikus/olvaso.css` | A fülek a mockup szerint aláhúzott fülsor: egy sorban, egyenlő szélességgel (`flex: 1 0 auto`), alattuk `rule` vonal, az aktív alatt 2 px `accent`, félkövér `fg` felirat, a többi `muted`; szűk helyen vízszintesen görgethető (375 px-en a négy fül elfér: 0 túlfolyás). |
| **Kereső** | `statikus/olvaso.css` | 32 px magas mező, `rule` keret, `radius-csempe`, `bg` háttér, `fs-sor`; a sor maradékát kitölti (920 px-en 458 px, 1280 px-en 818 px; a mockup omni-mezője `flex: 1 1 280px`). |
| **Regiszter** | `konfig/elemek.toml` | 19 új elem (új „Navigáció” csoport): `kereso`, `morzsa`, `felugro-panel`, `fejezetgomb`, `konyvgomb`, `mufaj-cim`, a nyolc műfajszín (`mufaj-tor` … `mufaj-apok`, a `--g-*` tokenekkel — így a tervező módban írhatók), `chip`, `navlap`, `reszletek-lap`, `hatter`, `tajolo`. A `[kizart]` táblából 15 osztály kikerült (mert most szelektorban állnak), a `kereso-gomb` (⌕) bekerült. A `fejlec` elem kapta a `panel` hátteret; a `lap-gomb` neve „Ikongomb, 32 px” lett, a tokenjei az új stílushoz igazodtak (a `bg` háttér helyett `accent-soft` / `accent`); a `ful` és a `ful-aktiv` tokenjei az aláhúzott fülsorhoz (`muted`, `fs-gomb`, `accent-soft` / `accent`, `fg`). Az elemszám 83 → 102. Az `fs-alcim` a #98 M1.7 szerint regiszteren kívüli token marad (csak előnézet): a morzsa és a pirula elemébe nem vettem fel. |
| **Tesztek** | `teszt_arculat.py`, `teszt_tervezo.py` | Új `TestMufajszinekEsTema` (4 teszt: a műfajszínek a mockup értékeivel; minden `MUFAJOK`-kód és szín-kód saját szabályt kap; az árnyék nem az `fg`-ből; a téma-szkript) és `test_a_lap_vilagos_alappal_es_a_temaszkripttel` (4 lapon: `data-tema="light"`, a szkript a `<head>`-ben a stíluslapok előtt, a Világos jelölve, inline szkript nincs, a `/statikus/tema.js` 200); `test_a_mufajszinek_irhatok`. A számok frissítve: 19 színtoken, 102 elem; a token-blokk szerkezeti tesztje a két témában azonos értékű tokent (`arnyek`) háromszor számolja. |
| **Egyéb** | `oldalak.py`, `README.md` | `SABLON_VERZIO = 'f134-m3'` (a gyorsítótár-kulcs az új sablonra vált); a README egy mondattal. |

### 1.1 Az Aa: CSSOM marad (az M2 4. szakaszának 1. pontja)

**Választás:** az Aa a betűméretet és a sorközt továbbra is CSSOM-mal (`style.setProperty`) állítja a szövegoszlopon; fokozatonkénti token nem lesz.

**Miért:** (1) az Aa a *néző* helyi beállítása (localStorage `pardes_aa`), a token-fájl pedig a *közös* arculat egyetlen forrása, amelyet a #98 Tervező mentési végpontja ír — a kettő keverése azt jelentené, hogy egy olvasói kényelmi beállítás az arculati forrásban él, vagy hogy a tervezőben hét értelmetlen `--fs-*` fokozat jelenik meg; (2) a token-szabály (`teszt_arculat.py`: betűméret, sorköz csak `var(--…)` vagy 0) a stíluslapra vonatkozik, és ott nincs literál: a CSSOM a már tokenből számolt alapértéket szorozza; (3) a CSP a CSSOM-ot engedi (a jelölésben `style=""` nincs), és a #98 Tervező előnézete is így dolgozik; (4) `calc(var(--fs-karoli-folyo) * 1.1)` jellegű osztályok a token-szabály `font-size` mintáján elbuknának. Tartalmi döntést nem igényel.

### 1.2 Eltérések a mockuptól (szándékosak)

- A fejléc 900 px-től nem ragadós (a mockupban `position: sticky`): a brief „egysoros fejlécet” ír elő, ragadósat nem, és a ragadós fejléc az oldalblokk ragadós tetejét is eltolná. Nyitott pontként jelölve (3. szakasz).
- A kereső ikonja (⌕) a mezőn kívül, gombként áll (a mockupban a mezőn belül díszítő ikon, gomb nélkül): a submit gomb a JS nélküli működéshez kell. A `/` billentyű-jelzés nem került be (a meglévő gyorsbillentyű Ctrl+K).
- A felugró alsó lapok lekerekítése a `radius-panel` (10 px), nem a mockup 14 px-e: új lekerekítés-tokent nem vettem fel.
- A „Legutóbb” 900 px-től a kánon-sáv mellett, legfeljebb 3 hellyel áll (a mockupban az alsó, rögzített sávban): a szerveren tartós alsó sáv nincs.

## 2. Saját próba böngészőben (nem független ellenőrzés)

*Módszer: ideiglenes fejlesztői szerver a WSL-ben (127.0.0.1:8799, `belso` kiadás, `kutato` szint a `/szint/kutato` hivatkozással, WSL-natív `~/pardes/pardes.db`, `--ujratolt`; a végén leállítva), a beépített böngészőpanel emulált szélességén (375×812, 768×1024, 920×900, 1280×900), világos és sötét témában (a ⚙ gombjaival), mérőszkripttel (`getBoundingClientRect`, `scrollWidth`, a látható `fixed`/`sticky` elemek, a fejléc gyermekeinek sor-tetői; kontraszt: a WCAG-relatív fénysűrűség a számított `color` és a legközelebbi átlátszatlan háttér között) és képernyőképpel. Oldal: Ez 37 (kijelölés nélkül; a fülsorhoz Ez 37:12). A böngészőpanel rejtett volt: a navigációs lap méréséhez az átmeneteket egy `adoptedStyleSheets`-lappal kikapcsoltam (az M2 módszere); a kód ettől nem változott. Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 @cbc2dbbc (+ a 9ca20b91 CSS-javítása, --ujratolt) | forras=bongeszo-meres | ts=2026-10-23`.*

| Mérés | 375 px | 768 px | 920 px | 1280 px |
|---|---|---|---|---|
| **E1** az első vers teteje (világos / sötét) | **100 / 100 px** (h1: 18 px) | 67 / 67 px | 211 px (M2: 249 px) | 211 px |
| a fejléc magassága, sorai | — (navigációs lap) | — (navigációs lap) | **80 px, 2 sor** (M2: 117 px, 3 sor) | 80 px, 2 sor |
| a kereső mezőjének szélessége | a lapon teljes sor | — | 458 px | 818 px |
| vízszintes túlfolyás | **0** (a navigációs lapon belül is 0) | 0 | 0 | 0 |
| tartós (`fixed`/`sticky`) látható elem lap nélkül | **nincs** | nincs | — | az oldalblokk és a fejsora (ragadós, szándékos) |
| ikongombok (‹ › Aa ⚙) | 32×32 | — | 32×32, 32×32, 33×32, 32×32 | — |
| navigációs lap (375 px, ⚙ nyitva) | teteje 377 px, 435 px magas; chip 23 px, kánon-sáv 22 px | — | — | — |
| részletek lapja (375 px, sötét, Ez 37:12) | teteje 422 px; a vers 80–233 px, a lap fölött; a négy fül 19–356 px között, a fülsor túlfolyása 0; árnyék `rgb(0 0 0 / .2)` | — | — | — |
| téma | betöltéskor tárolt érték nélkül, **sötét rendszer-beállítás mellett is világos**; Sötét → újratöltés után sötét (a fej-szkript alkalmazza); Rendszer → attribútum nélkül, sötét rendszeren sötét háttér; Világos → `light` | ugyanígy mérve 768 px-en | — | — |

**Kontraszt (a szöveg és a háttere, világos / sötét):** Károli-szöveg 15,56 / 14,48; versszám 7,17 / 8,99; kereső 15,56 / 14,48; chip (bekapcsolva) 14,61 / 10,45; a mostani könyv gombja (Ez, `g-prof` háttér, `panel` szöveg) 5,83 / 8,18; a mostani fejezet gombja 7,17 / 8,99; műfajcím 7,32 / 6,24; számláló-címke 6,74 / 6,49; a fül (aktív `fg`, a többi `muted`) 17,12 / 13,04 és `muted`. **Szembetűnő kontraszthiba nem volt;** a legkisebb mért érték 5,83 (WCAG AA ≥ 4,5). A böngészőben nem mért eset: a `g-kis` teljes színén a mostani könyv szövege a token-értékekből számolva 4,26 (4. szakasz, 5. pont).

A képernyőképeken (920 px világos; 920 px sötét, nyitott könyvválasztóval; 1280 px sötét, versmód; 375 px világos, navigációs lap; 375 px sötét, versmód) a fejléc egysoros, a kánon-sáv és a könyvválasztó műfajszínes (a mostani könyv a teljes színnel), a fülsor aláhúzott, a felugró panelek árnyékosak. Konzolhiba (CSP is) nem jelent meg.

**Javítás a próba nyomán (F134.10):** 1280 px-en a kánon-sáv (320 px-es alappal) felkúszott az első sorba, és a kereső 272 px-re szűkült; a sáv alapja most a sor 55%-a, így mindkét szélességen a vezérlők alá törik (a fenti 1280 px-es sor már a javítás utáni mérés).

## 3. Tesztek

*Futtatás: `python eszkozok/teszt_futtat.py --gyors` (WSL `pardes`, venv Python 3.12.3, WSL-natív `~/pardes/pardes.db`, 895 MB, `epites_ts` 2026-10-14T09:35:00Z — a DT300 szerinti régi adatbázis), a 9ca20b91 állapotán. Proveniencia: `scope=eszkozok/olvaso_szerver teszt_*.py (--gyors, teszt_szintek.py nélkül) | forras=teszt_futtat.py | ts=2026-10-23`.*

| Fájl | Az M2 után (574a6e50, az M2 jelentése szerint) | Az M3 után (9ca20b91, ez a futás) | Megjegyzés |
|---|---|---|---|
| `teszt_arculat.py` | 22 / zöld | 27 / zöld | új: `TestMufajszinekEsTema` (4), a lap világos alapja és a téma-szkript (1); a token-szabály (betűméret, sorköz, lekerekítés csak tokenből; nincs `:root`, `data-tema`, hex az `olvaso.css`-ben) az új CSS-en is áll |
| `teszt_bdb_vers_jelentes.py` | 26 / zöld | 26 / zöld | |
| `teszt_indito.py` | 39 / zöld | 39 / zöld | |
| `teszt_kereses.py` | 36 / zöld | 36 / zöld | |
| `teszt_olvaso_szerver.py` | 90 / 2 piros (1 kihagyva) | 90 / 2 piros (1 kihagyva) | |
| `teszt_pilot_aranymintaval.py` | 22 / 2 piros | 22 / 2 piros | a téma-választó tesztje (DT-F76i) zöld: a három `data-tema` gomb megvan, a JS `setAttribute('data-tema'`-t hív |
| `teszt_tervezo.py` | 48 / zöld | 49 / zöld | 102 elem, minden szelektor talál a valódi lapokon; a műfajszínek írhatók (új teszt); 19 színtoken a szinkron-kimenetben; a CSP- és a kiadás-őrök zöldek |
| **összesen** | **283, ebből 4 piros** | **289, ebből 4 piros** (mind a 4 ismert DT299-eset; **új piros: 0**; 1 kihagyott teszt) | |

**A 4 piros mind a régi adatbázis ismert esete (DT299), az M1 előtt is piros volt, és nem a #134 hibája:** `TestD2PilotEgyezes.test_1moz_1_25` (`vers:macula`), `TestD2PilotEgyezes.test_zsolt_22` (`vers:tsk_darab`), `test_heber_csempe_szavankent_a_pilot_szerint` (1Móz 1:9 LXX-alak), `test_szamlalok_egyeznek_a_pilottal` (könyvszám 57 / 61). Ugyanez az eredmény az F134.9 állapotán (cbc2dbbc) is, a CSS-javítás előtt.

A lassú `teszt_szintek.py` (DT129) nem futott (`--gyors`); a hozzáférési szintek kódja nem változott (a szintváltó hivatkozásai, a sablon szint-ágai és a `hozzaferes.py` érintetlenek). A teljes futás az M5-é. A regiszter-őr (`regiszter_or.py`): 0 hiba (192 osztály a felületen, 97 a regiszterben, 95 kizárva).

## 4. Nyitott pontok az M4-hez

1. **A nem fejezet-lapok fejléce kis képernyőn** (az M2 3. pontja): nem bővítettem. Az M3 stílusa (panel háttér, ikongomb, kereső) ezeken is érvényes, a navigációs lap viszont csak a fejezet-lapon van; az M4 mérése mutassa meg, kell-e.
2. **Ragadós fejléc 900 px-től?** A mockupban ragadós, a szerveren nem (1.2). Ha a valódi használatban hiányzik, az oldalblokk ragadós tetejét is hozzá kell igazítani.
3. **A ⚙ nyitásakor a navigációs lapon a ⚙ gomb új sorba kerül** (a nyitott `details` teljes sort kap; az M2 viselkedése). Látványbeli apróság, az M4 képernyőképein a 9. változathoz mérendő.
4. **Valódi mozgás** (az M2 4. pontja): a rejtett panelen az átmenet nem lép; a lapok mozgása és a pirula az M4 telefonos próbáján mérendő.
5. **Kontraszt a `g-kis` teljes színén (világos téma):** a mostani könyv gombján a `panel` szöveg a műfajszínen áll. A token-értékekből számolva (a fenti képlettel, `panel` `#fffdf8` a nyolc világos műfajszínen): `g-tor` 7,44 · `g-tort` 6,94 · `g-bolcs` 5,57 · `g-prof` 5,83 · **`g-kis` 4,26** · `g-ev` 7,89 · `g-lev` 5,41 · `g-apok` 7,47; sötétben (`panel` `#1d2321`) mind 7,02 fölött. A `g-kis` (a mockup `#a0702a`-ja) 13 px-es szövegnél kevéssel a WCAG AA 4,5 alatt van, és csak egy Kispróféta-fejezeten jelenik meg. Nem változtattam, mert a mockup értékétől való eltérés lenne; a token a tervező módban állítható. Az M4 vizuális mérésére bízom, vagy a felhasználó dönthet róla.
6. **Munkamódszer:** minden szkript (a kizárt-tábla frissítése, a mérőszkript) a Write eszközzel készült fájlból futott; heredoc és magyar szöveget tartalmazó inline kód nem volt. A böngészős mérőkódot a `javascript_tool` kapta (a böngészőben fut, nem a shellben).
