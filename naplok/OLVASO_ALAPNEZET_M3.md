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

## 5. Javítókör (a felhasználó visszajelzése, 2026-10-23)

*Ág: `claude/olvaso-alapnezet`, a b50093a7 (F134.11) után · modell: claude-opus-5-5 · a felhasználó a futó szerveren nézte (`http://192.168.1.172:9765/1Moz`), a visszajelzést a koordinátor továbbította. Az M4-et nem indítottam.*

**A visszajelzés szó szerint:** „Volt a mockupban több válaszható betűtípus, ezek eltűntek. A navigációnak felül kell maradnia . A beállitássak és a könyv választóval. Alapértelmezés, minden vers új sorban . Vers és szó blokk kicsi marad akkor is ha van több hely. A károli blokk sem tölti ki a rendelkezésre álló helyet.” — és a 900 px alatti esetre (a koordinátor továbbításával): „Telefonon is felül”.

### 5.1 Tételenként

| Tétel | Mit csináltam | Hol |
|---|---|---|
| **a) Betűtípus-választó** | A mockup betűválasztója a 4. változat („Szövegbeállítások”) Aa paneljében van, a 9. változat ezt vette át: **Betűcsalád: Source Serif / Noto Serif / IBM Plex Sans** (a mockup `BETU` táblája), mellette **Sorszélesség: keskeny 48ch / közepes 60ch / széles 80ch**. Mindhárom betű fájlja már a `statikus/fonts/` alatt van (Source Serif 4, Noto Serif, IBM Plex Sans, OFL), letöltés nem kellett, kihagyott betű nincs. Az Aa két új szegmens-választót kapott (`aa-betu`, `aa-szel`, a sorköz `.tema` gombjainak stílusával); a választás osztály a szövegoszlopon (`betu-noto` → `var(--font-gr)`, amelynek első tagja a Noto Serif; `betu-sans` → `var(--font-ui)`; `szel-keskeny` / `szel-szeles` → 48 / 80ch), és a localStorage `pardes_aa` őrzi, mint az Aa többi beállítását. A sorszélességet a mockup ugyanebben a panelben adja, és az e) tételhez tartozik, ezért vettem át. | `sablonok/alap.html`, `statikus/olvaso.js`, `statikus/olvaso.css`, `konfig/elemek.toml` |
| **b) A navigáció felül marad** | **900 px-től:** a fejléc ragadós (`position: sticky; top: 0`, minden lapon, a mockup `header.top`-ja); a könyvválasztó, az Aa és a ⚙ belőle nyílik. Az oldalblokk ragadós teteje a fejléc alá került (tartalék 96 px; a JS a mért fejléc-magasságból állítja: `top` = magasság + 8 px, `max-height` = `100vh` − magasság − 16 px, CSSOM), a horgonyokhoz `scroll-padding-top`. **900 px alatt (DT-F134n):** a fejezet-lap fejléce egysoros ragadós sáv: könyvválasztó (a morzsa, „Ez 37 ▾”), ‹ ›, Aa, ⚙ és egy új ⌕ gomb (`navlap-gomb`). A könyvválasztó, az Aa és a ⚙ a sávból lenyíló panel (8 px-es szegéllyel teljes szélességű, a képernyőn belül görgethető). A ⌕ (és a fejezetcím, a Ctrl+K) a sáv alatt nyitja a keresőt, a kánon-sávot, a jelölést és a „Legutóbb”-ot (fátyollal; a ⌕ újra, a fátyol vagy az Esc zárja; JS nélkül a `#navigacio` cél, ott ✕-szel). Egy lenyíló nyitása a navigációs részt bezárja. **A tájoló pirula kikerült** (sablon, JS, CSS, a regiszter `tajolo` eleme és három kizárt horga): a sáv mindig mutatja a helyet és a navigációt, a pirula fölösleges. A részletek alsó lapja a sáv alatt marad (z-sorrend; a teljes nézet magassága `100dvh − 56px`), a koppintott vers a sáv alá és a lap fölé görgetődik (a görgetés a sáv alját veszi alapul). A többi lap fejléce 900 px alatt változatlan (nem ragadós). | `sablonok/alap.html`, `sablonok/fejezet.html`, `statikus/olvaso.js`, `statikus/olvaso.css`, `konfig/elemek.toml`, `DONTESEK.md` (DT-F134n), a brief 2.1 és E1 |
| **c) Versenként új sor az alap** | A szövegoszlop a szerverről `versenkent` osztállyal jön (JS nélkül is versenként új sor), az Aa kapcsolója alapból bekapcsolt (`checked`). Aki kikapcsolja, annál a localStorage őrzi. A tárolt érték új `v: 2` jelet kap: a korábbi (jel nélküli) tárolásból a betűméret és a sorköz megmarad, a versenkénti kapcsoló viszont nem öröklődik (a régi alap a kikapcsolt volt, így a korábbi tárolás nem jelent kifejezett választást). Az „Alapértékek” a versenkéntire állít vissza. Az interlineáris réteg változatlan (ott a csempe a vers egysége). | `sablonok/fejezet.html`, `sablonok/alap.html`, `statikus/olvaso.js` |
| **d) A részletek-blokk nő a hellyel** | A fix `minmax(320px, 440px)` helyett a mockup 9. változatának `.fo` rácsa: a szöveg `minmax(0, 1fr)`, az oldalblokk 900–1100 px között `minmax(400px, .8fr)`, 1100 px fölött `minmax(460px, .9fr)`; az egész legfeljebb 1448 px (a mockup 1480 px-e a két oldali 16 px nélkül), középre igazítva. A köz a meglévő `space-oszlopkoz` token (16 px; a mockupban 20 / 28 px), új token nem kellett. | `statikus/olvaso.css` |
| **e) A Károli-szöveg oszlopa** | A szövegoszlop sávja most a fejléc szélessége és az oldalblokk közti teljes 1fr. **A mockup sorhossz-korlátot alkalmaz:** a szöveg `max-width` alapja 60ch (a 4. változat „közepes” sorszélessége), választhatóan 48 / 80ch. Ezt követtem: az alap 60ch maradt, és a „széles” (80ch) kitölti a sávot 1600 px-en is. 920 és 1280 px-en a 60ch-s szöveg már gyakorlatilag kitölti a sávot (lent). | `statikus/olvaso.css`, `statikus/olvaso.js` |

Egyéb: `SABLON_VERZIO = 'f134-m3j'` (a gyorsítótár-kulcs az új sablonra vált); a README bekezdése a ragadós sávval és az Aa új választóival.

**Munkamódszer-hiba (jelzem):** a tájoló két sablonsorát egy heredocban futtatott, magyar megjegyzést tartalmazó Python-részlettel töröltem; ez a CLAUDE.md shell-szabályát sérti. Lefutott, az eredmény helyes (pontosan a két sor törlődött, ellenőrizve), utána minden módosítás az Edit eszközzel készült.

### 5.2 Saját próba böngészőben (nem független ellenőrzés)

*Módszer: saját fejlesztői szerver a WSL `pardes` disztribúcióban (127.0.0.1:8799, `belso` kiadás, `kutato` szint, WSL-natív `~/pardes/pardes.db`, `--ujratolt`; a végén leállítva; a felhasználó 8765-ös szerverét nem érintettem), a beépített böngészőpanel emulált szélességén, mérőszkripttel (`getBoundingClientRect`, `scrollWidth − clientWidth`, a látható `fixed`/`sticky` elemek), tárolt Aa-érték nélkül (Source Serif, 20 px; a 920 és 1600 px-es sor újramérve alapméreten, miután egy korábbi próba 110%-os betűmérete bent maradt). Oldal: Ez 37. A részletek lapjánál a panelen a `smooth` görgetés nem lép (az M2/M3 is leírta): a vers helyét a `scrollBy` azonnali változatával mértem, a kód ettől nem változott; az átmeneteket egy `adoptedStyleSheets`-lap kapcsolta ki. Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 (munkafa a b50093a7 után, a javítókör változásaival) | forras=bongeszo-meres | ts=2026-10-23`.*

| Mérés | 375 px | 920 px | 1280 px | 1600 px |
|---|---|---|---|---|
| a fejléc / sáv magassága | **49 px, egy sor** (morzsa 72×30, öt 32×32-es gomb) | 80 px üres „Legutóbb”-bal; **102 px** (3 sor) két „Legutóbb”-bejegyzéssel | 80 px | 80 px |
| a fejléc teteje görgetés után | **0** (`sticky`) | 0 | 0 | 0 |
| az oldalblokk teteje görgetés után | — | 88 px (80 px-es fejléc); 110 px (102 px-es fejléc, lásd lent) | 89 px | 88 px |
| **E1** az első vers teteje | **146 px** (≤ 200; a sáv nélkül az M3-ban 100 px; a h1 67 px-nél) | 229 px (a 102 px-es fejléccel) | 207 px | 207 px |
| a szöveg sávja / a szöveg szélessége | 343 px / 343 px | 457 / 457 px | 641 / **600 px** (60ch) | 754 / **600 px** (60ch); „széles”: 754 px |
| az oldalblokk szélessége | — (alsó lap) | 400 px (M3: 440) | **576 px** (M3: 440) | **678 px** (M3: 440) |
| a rács | — | — | 1233 px | 1448 px, 69 px-nél kezdődik (középre) |
| vízszintes túlfolyás | **0** (a nyitott navigációs résszel is 0) | 0 | 0 | 0 |
| látható `fixed`/`sticky` elem lap nélkül | csak a sáv | a fejléc, az oldalblokk | ugyanígy | ugyanígy |

**375 px, a sáv működése:** a ⌕ után a body `navlap-nyitva`, `aria-expanded="true"`, a fókusz a keresőben; a kereső 46 px-nél, a kánon-sáv 84 px-nél, a jelölés és a „Legutóbb” 112 px-nél, a nyitott rész 146 px magas, a fátyol látszik; újra a ⌕-re zár, a sáv visszaáll 49 px-re. 1200 px-es görgetés után a könyvválasztó, az Aa és a ⚙ panelje a sávból nyílik: mindhárom 52 px-nél kezdődik, 8 px-től 359 px szélesen; a könyvválasztó 740 px magas (a `100dvh − 72px` korlát), a képernyőn belül.

**E2 (375 px, a részletek lapja):** a 20. versszámra koppintva versmód; a lap teteje 422 px (390 px magas betekintés), a 20. vers 80–144 px között: a 49 px-es sáv alatt és a lap fölött. Teljes nézet (⤢): a lap 56 px-nél kezdődik (756 px), a sáv látható marad.

**Aa (1280 px):** IBM Plex Sans + széles + versenként kikapcsolva → a szövegoszlop `betu-sans szel-szeles`, a betű `"IBM Plex Sans"`, `max-width` 960 px (80ch), a vers `inline`; tárolva `{"v":2,…,"betu":"sans","szel":"szeles","versenkent":false}`; újratöltés után ugyanez. „Alapértékek”: `versenkent`, a kapcsoló bejelölve. Régi, `v` nélküli tárolt érték (`meret: 3, versenkent: false`) mellett: a betű 22 px (megmaradt), a vers versenként (az új alap). Az Aa panel 300 px széles; a két új választó gombjai elférnek (túlfolyás 0).

**A fejléc magasságának követése:** 920 px-en a „Legutóbb” két bejegyzésével a fejléc 3 sorra (102 px) nő. Az 1600 → 920 px-es átméretezés után az oldalblokk még a régi (89 px-es) tetőn állt: a rejtett panelen a `ResizeObserver` és a `resize` esemény nem futott le (a böngészőpanel a mérés alatt rejtett volt). Kézzel kiváltott `resize` eseményre a kód helyesen számolt: `top` 110 px, `max-height` `calc(100vh − 118px)`, `scroll-padding-top` 110 px. Valódi (látható) böngészőben az M4 mérje.

**A többi lap** (`/kereses`): 375 px-en a fejléc `relative` (változatlan), 1280 px-en `sticky`, 800 px-es görgetés után is 0-n.

### 5.3 Tesztek

*Futtatás: `python eszkozok/teszt_futtat.py --gyors` (WSL `pardes`, WSL-natív `~/pardes/pardes.db`, 895 MB, `epites_ts` 2026-10-14T09:35:00Z — a DT300 szerinti régi adatbázis), a javítókör munkafáján, a commit előtt. Proveniencia: `scope=eszkozok/olvaso_szerver teszt_*.py (--gyors, teszt_szintek.py nélkül) | forras=teszt_futtat.py | ts=2026-10-23`.*

| Fájl | Az M3 után (9ca20b91) | A javítókör után | Megjegyzés |
|---|---|---|---|
| `teszt_arculat.py` | 27 / zöld | 27 / zöld | az árnyék-tesztben a `--arnyek` előfordulásainak alsó határa 6 → 5 (a tájoló pirula árnyéka kikerült) |
| `teszt_bdb_vers_jelentes.py` | 26 / zöld | 26 / zöld | |
| `teszt_indito.py` | 39 / zöld | 39 / zöld | |
| `teszt_kereses.py` | 36 / zöld | 36 / zöld | |
| `teszt_olvaso_szerver.py` | 90 / 2 piros (1 kihagyva) | 90 / 2 piros (1 kihagyva) | a navigációs tesztek az új állapotra: a ⌕ gomb, nincs tájoló, az Aa betűcsalád- és sorszélesség-gombjai, a bejelölt versenkénti kapcsoló, a szerver `versenkent` osztálya; a JS-ben a betű- és szélesség-osztályok, a `versenkent: true` alap, a `scroll-padding-top`; a CSS-ben a két ragadós fejléc, a régi alsó navigációs lap hiánya, a `minmax(460px, .9fr)` rács |
| `teszt_pilot_aranymintaval.py` | 22 / 2 piros | 22 / 2 piros | |
| `teszt_tervezo.py` | 49 / zöld | 49 / zöld | 101 elem (a `tajolo` kikerült; a teszt neve `test_101_elem_egyedi_id`), a térkép is 101; minden szelektor talál, a CSP- és a kiadás-őrök zöldek |
| **összesen** | **289, ebből 4 piros** | **289, ebből 4 piros** (mind a 4 ismert DT299-eset; **új piros: 0**; 1 kihagyott) | |

A 4 piros ugyanaz, mint az M3 után: `TestD2PilotEgyezes.test_1moz_1_25`, `TestD2PilotEgyezes.test_zsolt_22`, `test_heber_csempe_szavankent_a_pilot_szerint`, `test_szamlalok_egyeznek_a_pilottal` (régi adatbázis, DT299). Az első futás (a tesztek frissítése előtt) két újabb pirosat adott, mindkettő a tájoló kivételének számbeli következménye (`--arnyek` 5 < 6; a tervező térképe 101 ≠ 102); a számok frissítése után zöldek. A regiszter-őr (`regiszter_or.py`): 0 hiba (195 osztály a felületen, 96 a regiszterben, 99 kizárva). A `teszt_szintek.py` (DT129) nem futott; a szintek kódja nem változott.

### 5.4 Nyitott pontok

1. **Sorhossz 1600 px-en:** a mockup 60ch-s alapja mellett a szöveg 600 px, a sáv 754 px (154 px üres a szöveg és az oldalblokk között). A „széles” (80ch) kitölti. Ha a felhasználó nagy képernyőn a teljes kitöltést várja alapnak, az a mockuptól eltérő alapérték lenne (a széles alap vagy a sávhoz igazodó korlát): az ő döntése.
2. **920 px-en az oldalblokk 400 px** (az M3-ban 440): a mockup 900–1100 px közti rácsa ezt adja (`minmax(400px, .8fr)`), a szöveg így 457 px. 1100 px fölött az oldalblokk 460 px-ről nő.
3. **A rács köze 16 px** (a `space-oszlopkoz` token), a mockupban 20 / 28 px: a token a tervező módban állítható.
4. **Valódi telefon** (az M4-é): a ragadós sáv és a `100dvh` viselkedése a böngésző címsorának be- és kicsúszásakor, és a sávból lenyíló könyvválasztó görgetése érintéssel.
5. A 4. szakasz 2. pontja (ragadós fejléc 900 px-től) ezzel megoldott; a 3. pont (a ⚙ új sorba kerül a navigációs lapon) megszűnt, mert a ⚙ a sávban van.

## 6. Javítókör 2. kör (a kitöltetlen hely; a „Strong számok” kapcsoló), 2026-10-23

*Ág: `claude/olvaso-alapnezet`, a c67a4058 (F134.12) után · modell: claude-opus-5-5 · a felhasználó a futó szerveren nézte (`http://192.168.1.172:9765/1Moz`), a visszajelzést a koordinátor továbbította. Az M4-et nem indítottam.*

**A visszajelzés szó szerint:** „Még mindig túl sok a kitöltetlen hely a Károli blokk és a vers blokk között. Ha csak a Károli blokk jelenik meg ott is sok a Margó, a kitöltetlen hely”. Ugyanehhez a körhöz, egymás után: „A Strong ki be kapcsolása is a fő navigációban legyen”; majd pontosítva: „a „kapcsolt szavak jelölése” kapcsolót … erre gondoltam”; „Legyen Strong számok”; „Ne kapcsolt szavak”. Döntés: `DT-F134o` 🟢 (a `DONTESEK.md`-ben; a DT296 „komponensstílusok a mockupból” része ennyiben módosul, az 5.4 szakasz 1. nyitott pontja ezzel eldőlt).

**Az értelmezés javítása:** az első üzenet után a koordinátor értelmezése szerint az interlineáris réteg (`il`) kapcsolóját vittem ki a fő navigációba („Strong” chip). A pontosítás szerint a felhasználó a kapcsolt szavak jelölésének kapcsolójára gondolt: az `il`-es áthelyezést visszavontam (a kapcsoló a ⚙ menüben van, mint az F134.12-ben; stílusa és regiszter-bejegyzése változatlan), ez a köztes állapot nem került commitba.

### 6.1 Mit változtattam

| Tétel | Mit | Hol |
|---|---|---|
| **a) A szöveg kitölti a sávot** | A `.szoveg-oszlop` 60ch-s `max-width`-je megszűnt: a szöveg alapból a teljes sávot kitölti. Az Aa „Sorszélesség” választója négy gomb: keskeny (48ch) / közepes (60ch, új `szel-kozepes` osztály) / széles (80ch) / **teljes = az alap** (`data-aa-szel=""`, `aria-pressed="true"`). A korábban tárolt `szel: ''` (a régi 60ch-s alap, kifejezett választás nélkül) így az új alapra vált; aki a széleset vagy a keskenyet választotta, annál megmarad. | `statikus/olvaso.css`, `statikus/olvaso.js`, `sablonok/alap.html`, `konfig/elemek.toml` (`szel-kozepes` a `[kizart]` alatt, mint a többi `szel-*`) |
| **b) A rács nincs korlátozva és középre igazítva** | A `.olvaso-elrendezes { max-width: 1448px; margin-inline: auto; }` kikerült. Kívül csak a `.tartalom` `space-oldal` térköze (16 px), a szöveg és az oldalblokk között a meglévő `space-oszlopkoz` (16 px); új token nem kellett. Az oszlop-arány (a szöveg `1fr`, az oldalblokk 1100 px-ig `minmax(400px, .8fr)`, fölötte `minmax(460px, .9fr)`) maradt. | `statikus/olvaso.css` |
| **c) Csak a Károli-szöveg (900 px alatt)** | Ugyanaz az a) pont: a szövegnek nincs sorhossz-korlátja, a sáv a két 16 px-es `space-oldal` között teljes. 800 px-en a szöveg 753 px (korábban 600 px, 153 px üres maradt). | — |
| **d) A „Strong számok” kapcsoló a fő navigációs sorban** | A jelölés-chip (`div.jelolo` > `label.kapcs.chip` > `input#jeloles`) kikerült a `nav-extra` részből (900 px-től a kánon-sáv melletti 2. sor, 900 px alatt a ⌕ mögött), és a fejléc vezérlősorában az Aa és a ⚙ között áll: 900 px-től a ragadós fejléc első sorában, 900 px alatt az egysoros sávban. Felirata „Strong számok” (a „Kapcsolt szavak” szöveg kikerült), `title`: „A Strong-számmal párosított szavak jelölése (pontozott aláhúzás)”. **A működése változatlan:** a JS az `id="jeloles"`-t figyeli, a `.szoveg-oszlop`-ra a `nincs-jeloles` osztályt teszi, a `pardes_jeloles` localStorage-kulcs őrzi; az `il`-rétegben a chip továbbra sem jelenik meg. **A felirat nem félrevezető:** a kapcsoló a `.szo` osztályú szavak pontozott aláhúzását kapcsolja, és `.szo` csak az a szó, amelynek a Károli–Strong párosításból Strong-száma van (`sablonok/fejezet.html`, `w.fo` = a Strong-szám, `data-strong`); a Strong-szám nélküli szó `szo-nincs`. A kapcsoló tehát a Strong-számmal rendelkező szavakat jelöli; magukat a számokat nem írja ki (azokat a szóra koppintva a részletek lapja, ill. az interlineáris réteg mutatja). | `sablonok/alap.html`, `konfig/elemek.toml` (a `kapcs`, `chip`, `jelolo`, `navlap-gomb` leírása) |
| **e) A fejléc első sora 900 px-től** | A chip a vezérlősorba került, ezért a kereső alapja `max(280px, calc(100% - 1200px))` lett: 920 px-en a vezérlők (a chippel együtt) egy sorban maradnak, széles képernyőn pedig a kánon-sáv nem kúszik fel a vezérlők sorába. **Mellékesen talált hiba:** az F134.12 állapotában 1920 px-en a kánon-sáv a vezérlők sorába kúszott (a kereső 325 px-re szűkült), az F134.10 „mindig saját sorban” szándékával szemben; ezzel megszűnt. | `statikus/olvaso.css` |
| Egyéb | `SABLON_VERZIO = 'f134-m3k'`; a README bekezdése; a sablon és a CSS megjegyzései (a ⌕ már nem nyitja a jelölést). | `oldalak.py`, `README.md` |

### 6.2 Saját próba böngészőben (nem független ellenőrzés)

*Módszer: saját fejlesztői szerver a WSL `pardes` disztribúcióban (127.0.0.1:8799, `belso` kiadás, WSL-natív `~/pardes/pardes.db`, `--ujratolt`; a végén leállítva; a felhasználó 8765-ös szerverét nem érintettem), a beépített böngészőpanel emulált szélességén, mérőszkripttel (`getBoundingClientRect`, `scrollWidth − clientWidth`), tárolt Aa-érték nélkül. Oldal: Ez 37, az `il`-réteg kikapcsolva, a jelölés bekapcsolva. 900 px-től az emulált ablakban 15 px-es függőleges görgetősáv van: a jobb margó a lap látható szélétől (`clientWidth`) mért érték. A „Legutóbb” sorban a böngésző korábbi bejegyzései állnak (a 2. sor magasságát nem befolyásolják). Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 (munkafa a c67a4058 után, a 2. kör végső változásaival) | forras=bongeszo-meres | ts=2026-10-23`.*

| Szélesség (`clientWidth`) | margó bal | szöveg (sáv = szöveg) | köz | oldalblokk | margó jobb | túlfolyás | fejléc / sáv | E1 |
|---|---|---|---|---|---|---|---|---|
| 375 (375) | 16 | 343 | — (alsó lap) | — | 16 | 0 | **87 px, két sor** (⛔, lent) | 184 px (≤ 200; F134.12: 146) |
| 800 (785) | 16 | 753 | — (alsó lap) | — | 16 | 0 | 49 px, egy sor | 112 px |
| 920 (905) | 16 | 457 | 16 | 400 | 16 | 0 | 74 px (a vezérlők egy sorban) | 202 px |
| 1000 (985) | 16 | 521 | 16 | 416 | 16 | 0 | 74 px | 202 px |
| 1280 (1265) | 16 | 641 (F134.12: 600) | 16 | 576 | 16 | 0 | 74 px | 202 px |
| 1600 (1585) | 16 | 809 (F134.12: 600 a 754-es sávban) | 16 | 728 (F134.12: 678) | 16 | 0 | 74 px | 202 px |
| 1920 (1905) | 16 | 977 | 16 | 880 | 16 | 0 | 74 px (a kánon-sáv saját sorban) | 202 px |

**A szöveg és az oldalblokk között** minden szélességen pontosan a 16 px-es köz van, üres sáv nincs; a rács a 16 px-es bal margónál kezdődik (F134.12-ben 1600 px-en 69 px-nél, középre igazítva). A szöveg mindenhol kitölti a sávját (a szöveg szélessége = a sáv szélessége).

**A „Strong számok” chip 900 px-től:** 122×25 px, a fejléc első sorában az Aa és a ⚙ között (920 px-en x = 725, a ⚙ 857 px-nél, egy sorban; 1920 px-en x = 1725). Kattintásra (1000 px): a szövegoszlop `nincs-jeloles`, a `.szo` aláhúzása `none`, tárolva `pardes_jeloles: ki`; újra: aláhúzás, `be`.

**375 px — a sáv nem fér egy sorba (⛔):** a „Strong számok” chip 122 px; a sáv elemei: könyvválasztó 72, ‹ › 68, Aa 33, chip 122, ⚙ 32, ⌕ 32 = 359 px + öt 10 px-es köz = 409 px, a hely 343 px. Mérve: a ⚙ és a ⌕ a 2. sorba tör (46 px-nél), a sáv 87 px, túlfolyás 0, E1 184 px. 4 px-es sávközzel is két sor (87 px). **Mért alternatíva** (csak a böngészőben, a kódban nincs): „Strong” felirattal (74 px) és 4 px-es sávközzel egy sor (49 px), a ⌕ jobb széle 359 px; az F134.12-es próbán a pont nélküli 60 px-es „Strong” chippel a leghosszabb morzsánál (ApCsel 28, 106 px) is egy sor volt. A felirat cseréje a felhasználó döntése; magamtól nem cseréltem.

**Aa (1920 px):** a négy gomb (keskeny / közepes / széles / teljes) a 300 px-es panelben elfér (274 px, túlfolyás nélkül), alapból a „teljes” lenyomva; „közepes” → `szel-kozepes`, 600 px; „széles” → 800 px; „teljes” → 977 px, tárolva `"szel":""`.

### 6.3 Tesztek

*Futtatás: `python eszkozok/teszt_futtat.py --gyors` (WSL `pardes`, WSL-natív `~/pardes/pardes.db`, 895 MB, `epites_ts` 2026-10-14T09:35:00Z — a DT300 szerinti régi adatbázis), a 2. kör végső munkafáján, a commit előtt. Proveniencia: `scope=eszkozok/olvaso_szerver teszt_*.py (--gyors, teszt_szintek.py nélkül) | forras=teszt_futtat.py | ts=2026-10-23`.*

| Fájl | F134.12 után | A 2. kör után | Megjegyzés |
|---|---|---|---|
| `teszt_arculat.py` | 27 / zöld | 27 / zöld | |
| `teszt_bdb_vers_jelentes.py` | 26 / zöld | 26 / zöld | |
| `teszt_indito.py` | 39 / zöld | 39 / zöld | |
| `teszt_kereses.py` | 36 / zöld | 36 / zöld | |
| `teszt_olvaso_szerver.py` | 90 / 2 piros (1 kihagyva) | 90 / 2 piros (1 kihagyva) | a navigációs teszt az új állapotra: az Aa négy sorszélesség-gombja, a „teljes” az alap; a „Strong számok” chip a ⚙ előtt, nem a `nav-extra`-ban, „Kapcsolt szavak” felirat nincs; az interlineáris kapcsoló a ⚙ menüben; a CSS-ben nincs `.szoveg-oszlop` `max-width` és `max-width: 1448px`, van `szel-kozepes` (60ch); a JS-ben a `szel-kozepes` |
| `teszt_pilot_aranymintaval.py` | 22 / 2 piros | 22 / 2 piros | a DT-F76i-teszt a „Strong számok” feliratot várja |
| `teszt_tervezo.py` | 49 / zöld | 49 / zöld | |
| **összesen** | **289, ebből 4 piros** | **289, ebből 4 piros** (mind a 4 ismert DT299-eset; **új piros: 0**; 1 kihagyott) | |

A 4 piros ugyanaz, mint korábban: `TestD2PilotEgyezes.test_1moz_1_25`, `TestD2PilotEgyezes.test_zsolt_22`, `test_heber_csempe_szavankent_a_pilot_szerint`, `test_szamlalok_egyeznek_a_pilottal` (régi adatbázis, DT299). Egy köztes futás (az `il`-es változattal) egy új pirosat adott (`teszt_arculat.py`: a `--space-gomb-fugg` token használatlan lett az átírt rétegkapcsoló-stílus miatt); az `il`-es változat visszavonásával a stílus az eredeti, a teszt zöld. A regiszter-őr (`regiszter_or.py`): 0 hiba (196 osztály a felületen, 96 a regiszterben, 100 kizárva; az új a `szel-kozepes`). A `teszt_szintek.py` (DT129) nem futott; a szintek kódja nem változott.

### 6.4 Nyitott pontok

1. ~~**⛔ 375 px-en a sáv két sorra törik** a „Strong számok” chippel (87 px, mérve).~~ Eldőlt: a felhasználó „A” → (a); megvalósítva az F134.14-ben (6.5).
2. **Nagyon széles képernyőn a sorhossz:** 1920 px-en a szöveg 977 px — a döntés szerint ez az alap; a 48 / 60 / 80ch az Aa-ban választható.
3. A mérés emulált szélességen, a panel görgetősávjával; valódi böngésző és telefon az M4-é.

### 6.5 A 375 px-es sáv: a felhasználó döntése (F134.14)

A felhasználó, 2026-10-23 (chat, a koordinátor továbbította): „A” → a 6.4 (a) lehetősége. Megvalósítás: a chip mindkét feliratot tartalmazza (`<span class="jelolo-hosszu">Strong számok</span><span class="jelolo-rovid">Strong</span>`), a CSS a meglévő 900 px-es határon választ (alapból a rövid rejtett, 900 px alatt a sávban a hosszú). A `title` és az `input` `aria-label`-je mindkét szélességen a hosszú leírás („Strong számok: a Strong-számmal párosított szavak jelölése (pontozott aláhúzás)”). 900 px alatt a sáv oszlopköze a `space-gombsor` token (4 px), a chip pont nélküli, vízszintes belső térköze a `space-gomb-fugg` token (4 px): a 4 px-es köz és a pont elhagyása még nem volt elég a leghosszabb morzsához (ApCsel 27, mindkét nyíllal: 87 px, két sor, a ⌕ a 2. sorban), a szűkebb belső térközzel igen. Új token nem kellett; a két új osztály a regiszter `[kizart]` listáján. `SABLON_VERZIO = 'f134-m3l'`.

**Mérés (saját próba, 127.0.0.1:8799, emulált 375 px; nem független ellenőrzés).** Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 (munkafa a 90d71fc4 után) | forras=bongeszo-meres | ts=2026-10-23`.

| Oldal (375 px) | morzsa | chip | a sáv | ⌕ jobb széle | E1 | túlfolyás |
|---|---|---|---|---|---|---|
| Ez 37 | 72 px | 48 px, „Strong” | **49 px, egy sor** | 359 px | 146 px | 0 |
| ApCsel 28 (csak ‹) | 106 px | 48 px | **49 px, egy sor** | 359 px | 146 px | 0 |
| ApCsel 27 (‹ ›; a legszélesebb morzsa, vászon-méréssel a 66 könyv közül) | 106 px | 48 px | **49 px, egy sor**; a tartalék 3 px | 359 px | 146 px | 0 |
| 1Thessz 4 (‹ ›) | — | 48 px | 49 px, egy sor | — | 178 px | 0 |

920 px-en a chip felirata „Strong számok” (122 px), a fejléc első sorában (x = 725, a ⚙-val egy sorban), a fejléc 73 px, túlfolyás 0. Kattintásra (375 px, ApCsel 27) a szövegoszlop `nincs-jeloles`, újra kattintva visszaáll.

**Tesztek** (`teszt_futtat.py --gyors`, a végső munkafán): 289, ebből 4 piros, mind a 4 ismert DT299-eset; **új piros: 0**; 1 kihagyott. A felirat-tesztek igazítva (`teszt_olvaso_szerver.py`: a két felirat a jelölésben, az `aria-label`, a CSS négy szabálya; `teszt_pilot_aranymintaval.py`: a hosszú felirat). Regiszter-őr: 0 hiba (198 osztály a felületen, 96 a regiszterben, 102 kizárva).

**Nyitott:** a legrosszabb esetben (ApCsel 27) 3 px a tartalék; nagyobb rendszerbetűméretnél vagy más betűrenderelésnél (valódi telefon, M4) a sáv két sorra törhet.
