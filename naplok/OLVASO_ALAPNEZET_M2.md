# OLVASO_ALAPNEZET — M2: kis képernyő (#134)

*FELADATOK #134 · ág: `claude/olvaso-alapnezet` · 2026-10-23 · modell: claude-opus-5-5 · a brief: `F134_OLVASO_ALAPNEZET_BRIEF.md`, 2.1, 2.3 és 3. szakasz (M2); a terv: `naplok/OLVASO_ALAPNEZET_M0.md` (9. szakasz: DT-F134f–m); a vizuális mérce: a mockup 9. változata (https://claude.ai/artifact/ExAeE1TKsNfuEMutErqsuA, ver. `1792660119-3840`, Artifact `read`)*

Az M2 a felhasználó indítására futott („Az M2 mehet.”). Az M3-at nem indítottam.

## 1. Mi készült

| Elem | Hol | Mit csinál |
|---|---|---|
| **Fejléc nélküli olvasó** (DT292) | `statikus/olvaso.css` (`@media (max-width: 899.98px)`) | 900 px alatt a fejezet-lapon nincs tartós fejléc és alsó sáv: a lap teteje a fejezetcím, alatta a „Forrás és számlálók” hivatkozás, aztán a szöveg. A lapozó sor előző/következő hivatkozásai a navigációs lapra költöznek (‹ ›). |
| **Navigációs lap** | `sablonok/alap.html` (`header.fejlec.navlap#navigacio`), `oldalak.py` (`navigacio()`, `MUFAJOK`), `statikus/olvaso.js` | A fejezet-lap fejléce 900 px alatt alulról felugró lap (86vh, fátyollal), a fejezetcímre (`h1 > a.navlap-nyito`, „ ▾”) vagy a tájoló pirulára koppintva nyílik; ✕, a fátyol és az Esc zárja. JS nélkül a `#navigacio` cél (`:target`) nyitja. Tartalma a mockup sorrendjében: Navigáció + ✕; a kereső; a könyvválasztó (morzsa: „Ez 37 ▾”); ‹ ›; Aa; ⚙ (a lapon kinyitva: rétegek — az interlineáris sor —, a szint és a Tervező kapcsoló csak a belső kiadásban, a téma); a kánon-sáv; a jelölés kapcsolója; „Legutóbb”. **Fejezet-kalauz gomb nincs** (DT-F134l). A nyitása elrejti a részletek lapját, az állapotát megtartja (a mockup `lapZar(true)`-ja). |
| **Kereső javaslata** (DT-F134k (b)) | `statikus/olvaso.js` | A könyvválasztó gombjaiból (`.konyvgomb[data-kk]`: kód, név, slug, fejezetszám) — a lapban már meglévő könyvlista, **új végpont és új adat nélkül**. Könyvkód, slug vagy név eleje + opcionális fejezet és vers (`ez 3`, `1moz 3:16`); ékezet- és kisbetű-független; a pontos kód-egyezés elöl; a fejezetszám a könyv fejezetszámát nem haladhatja meg. ↑↓ Enter Esc. Strong-szám és szó: nincs javaslat, a megszokott keresés megy. |
| **Könyvválasztó és kánon-sáv** | `sablonok/alap.html`, `oldalak.py` | Szerveroldali, JS nélkül is működik: a könyv fejezetrácsa, alatta a 66 könyv a mockup műfaji csoportjaiban (a könyv lapjára mutat). JS-sel a könyvre vagy a kánon-sáv téglalapjára koppintva helyben rajzolja a fejezetrácsot (folytonos számozásnál). A kánon-sáv SVG: a könyvek szélessége a fejezetszámmal arányos (legalább 3 egység), az Ó- és Újszövetség határán köz; `style=""` nélkül (CSP). A műfajszín `data-mufaj`-ban áll; a színek (`--g-*`) az M3-é, addig az `accent` tokenből. 66-tól eltérő könyvlistánál két csoport (Ó/Új). |
| **Aa** | `sablonok/alap.html`, `statikus/olvaso.js` | Betűméret (7 fok, 85–150%), sorköz (szűk / közepes / tág), versenként új sor; localStorage (`pardes_aa`). A méretet és a sorközt CSSOM-mal (`style.setProperty`) állítja a szövegoszlopon: a CSP ezt engedi, a jelölésben `style=""` nincs, és a token-fájlt nem írja (a #98 Tervező is CSSOM-mal dolgozik). |
| **⚙ menü** | `sablonok/alap.html` | Minden lapon `details` (JS nélkül is nyitható); 900 px-től lenyíló panel. A sorrend (réteg, szint, Tervező, téma) a #98 őrét (`teszt_tervezo.py`: szintváltó < Tervező < téma) megtartja; a Tervező mód és a DT129 szintek működése nem változott. A nem fejezet-lapok (kezdőlap, könyv, kereső, szó-lap) fejléce egyébként a régi (navigációs lap nélkül). |
| **Tájoló pirula** | `sablonok/fejezet.html` (`a.tajolo#tajolo`), CSS, JS | 900 px alatt felfelé görgetésre (300 px mélység fölött, 6 px-es küszöb) a lap tetején megjelenik („Ez 37 ▾”, kijelölt versnél „Ez 37:5 ▾”), lefelé görgetésre vagy 2,5 mp után eltűnik; nyitott lapnál nem látszik; koppintásra a navigációs lapot nyitja. |
| **A részletek lapjának húzása** | `statikus/olvaso.js`, CSS | A fejsoron (`.lap-fej`, `touch-action: none`, a gombok kivételével): fel (−40 px) → teljes nézet; le (+40 px) → teljesből betekintés, betekintésből zárás; rövid koppintás a fejsoron: váltás. A teljes nézet mögött fátyol (koppintásra vissza betekintésre). A koppintott vers a lap fölött marad: a mockup szabálya szerint csak akkor görget, ha a vers a képernyő felénél lejjebb (vagy fölötte) van. |
| **Versműveletek a fejsorban** | `sablonok/fejezet.html` (`.lap-muv`), JS | A fejsor műveletsora: szómódban az „A vers: … →” (a töredékből a JS költözteti ide; JS nélkül a töredékben marad). Versmódban üres és rejtett, mert a „Másolás forrással” nem kerül be (DT-F134m). |
| **Legutóbb** | `alap.html` (`#legutobb`), JS | Az utoljára megnyitott 6 vers (localStorage `pardes_legutobb`), a navigációs lap (900 px-től a fejléc) kiegészítő sorában; üresen rejtett. A mockup előzménysora szerint versek, nem fejezetek. |
| **Regiszter** | `konfig/elemek.toml` | Az új osztályok (47) a `[kizart]` listán, indokkal; az elemszám 83 marad (a komponensstílusok regisztrálása az M3-é). A regiszter-őr: 0 hiba (190 osztály a felületen, 109 kizárva). |
| **Tesztek** | `teszt_olvaso_szerver.py` | Új: `TestNavigacio` (4 teszt): a navigációs lap elemei, a 66 könyv és a műfaji csoportok, a fejezetrács, a kánon-sáv `style` nélkül, a ⚙ sorrendje, a lépegető szélei, a többi lap fejléce változatlan, az `il` rétegben nincs jelölés, a JS és a CSS horgai (a `:target` tartalék, a fülváltás az előzményláncban). |
| **Egyéb** | `oldalak.py` (`SABLON_VERZIO = 'f134-m2'`), `README.md` | a gyorsítótár-kulcs az új sablonra vált; a README egy bekezdéssel |

### 1.1 A fülváltás és az előzménylánc (az M1 nyitott pontja)

**Mit találtam a mockupban** (9. változat, a `panel()` és a `v9Utan` kódja): az állapot `{v: vers, s: Strong, f: fül}`; a fülre kattintás `ful = k; panel()`-t hív, a `panel()` a `v9Utan(true)`-n át minden új, az előzőtől eltérő állapotot a verembe tesz (az `azonos` mindhárom mezőt veti össze). **A fülváltás tehát a mockupban új előzmény-állapot**: a ‹ az előző fülre is visszalép. A ‹ csak akkor látszik, ha van hová visszalépni, és a lap bezárása törli a láncot.

**Mit változtattam:** az M1-ben a fülváltás nem került a láncba; most igen. A `azonos()` versmódban a fület is összeveti; fülváltáskor az előző állapot a verembe kerül (legfeljebb 20, azonos egymás után nem ismétlődik). A ‹ ugyanazon vers másik fülére töredék-letöltés nélkül vált vissza. Saját próbán: Ez 37:12 → Kereszthiv. fül (‹ megjelenik, `?ful=kh`) → ‹ → Vers fül, a ‹ eltűnik.

### 1.2 Eltérések a mockuptól (szándékosak)

- 900 px-től a fejezetcímre kattintva a könyvválasztó nyílik (a mockupban ott a cím nem kattintható); a cím így mindkét szélességen ugyanazt jelenti: „hol vagyok, hová mennék”.
- A navigációs lapon a lenyíló elemek (`details`) helyben nyílnak ki, a kereső javaslatlistája lebeg (a mockupban statikus); a ⚙ a lap nyitásakor kinyílik, mint a mockupban.
- A jelölő chipek helyén a meglévő egyetlen kapcsoló (kapcsolt szavak jelölése): a többi chip (kereszthivatkozás, motívum, témák) a szerveren nem létező szövegjelölés, új adat kellene hozzá (hatókörön kívül).

## 2. Saját próba böngészőben (nem független ellenőrzés)

*Módszer: ideiglenes fejlesztői szerver a WSL-ben (127.0.0.1:8799, `belso` kiadás, `kutato` alapszint, WSL-natív `~/pardes/pardes.db`, `--ujratolt`), a beépített böngészőpanel emulált szélességén, mérőszkripttel (`getBoundingClientRect`, `scrollWidth`, a látható `fixed`/`sticky` elemek listája) és képernyőképpel. Oldal: Ez 37. A böngészőpanel a mérés alatt rejtett volt; ilyenkor a böngésző a CSS-átmenetet, a sima görgetést és a `scroll` eseményt nem lépteti, ezért a mérőszkript a mérés idejére egy `adoptedStyleSheets`-lappal kikapcsolta az átmeneteket, a `scrollBy`-t azonnalira állította, és a pirula-mérésnél a `scroll` eseményt kézzel küldte. A kód ettől nem változott; a valódi mozgást az M4 telefonos próbája méri. Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 @574a6e50 | forras=bongeszo-meres | ts=2026-10-23`.*

| Mérés | 375 px | 768 px | 920 px |
|---|---|---|---|
| **E1** az első vers teteje a lap tetejétől | **100 px** (h1: 18 px) | 67 px | 249 px (fejléc 117 px; nem E1-feltétel) |
| tartós (`fixed`/`sticky`) látható elem lap nélkül | **nincs** | nincs | — (a fejléc nem ragadós) |
| vízszintes túlfolyás (`scrollWidth` − szélesség) | **0** (375) | 0 (753 = a görgetősáv nélküli szélesség) | 0 (905) |
| **E2** versszám (Ez 37:12, 900 px-re görgetve): a lap teteje / a vers | **422 px** (390 px magas) / 80–233 px, a lap fölött | **532 px** (492 px magas) / 18–120 px, fölötte | oldalblokk, 449 px-től jobbra |
| E2 további versek (375 px): 37:3, 37:25, 37:1 | a lap 422 px; a vers 293–415, 80–266, 100–221 px: mind a lap fölött | — | — |
| **E2** szó (Ez 37:20, H6086) | a lap 422 px; a vers 80–137 px, fölötte | a lap 532 px; a vers 84–149 px, fölötte | — |
| húzás a fejsoron (375 px) | fel: a lap teteje 28 px (teljes); le: 422 px (betekintés); le: zárva, üres állapot | — | — |
| navigációs lap | nyitva: a teteje 348 px (464 px magas, a ⚙ kinyitva); ✕ és Esc zár; JS nélkül (`:target`): nyílik | — | 900 px-től fejléc; a cím a könyvválasztót nyitja, kívülre kattintva zár, egyszerre egy lenyíló nyitva |
| tájoló pirula (375 px) | felfelé görgetésre a teteje 8 px, szövege „Ez 37 ▾”; lefelé eltűnik; 2,5 mp után eltűnik; koppintásra a navigációs lap nyílik | — | — |
| kereső javaslat | `ez 3` → Ez 3, Ézs 3, Ezsd 3 (a javítás után a pontos kód elöl); `1moz 3:16` → `/1Moz/3/16#v16`; `H0216` → nincs javaslat | — | — |
| kánon-sáv | 66 téglalap; a Zsolt téglalapra koppintva a Zsoltárok 150 fejezetes rácsa nyílik helyben | — | látszik a fejléc alatt |
| Aa | — | — | A+ → 22 px (110%), Alapértékek → 20 px |

A képernyőképeken (375 px, szómód: H7307, Ez 37:5) a vers a lap fölött, a fejsorban a cím, ⤢ ✕ és alatta „A vers: Ez 37:5 →”. Konzolhiba (CSP is) nem jelent meg.

## 3. Tesztek

*Futtatás: `python eszkozok/teszt_futtat.py --gyors` (WSL `pardes`, venv Python 3.12.3, WSL-natív `~/pardes/pardes.db`, `epites_ts` 2026-10-14T09:35:00Z — a DT300 szerinti régi adatbázis). Proveniencia: `scope=eszkozok/olvaso_szerver teszt_*.py (--gyors, teszt_szintek.py nélkül) | forras=teszt_futtat.py | ts=2026-10-23`.*

| Fájl | Az M1 után (fc7a9282, az M1 jelentése szerint) | Az M2 után (574a6e50, ez a futás) | Megjegyzés |
|---|---|---|---|
| `teszt_arculat.py` | 22 / zöld | 22 / zöld | a token-szabály (betűméret, sorköz, lekerekítés csak tokenből; nincs `:root`, hex) az új CSS-en is áll |
| `teszt_bdb_vers_jelentes.py` | 26 / zöld | 26 / zöld | |
| `teszt_indito.py` | 39 / zöld | 39 / zöld | |
| `teszt_kereses.py` | 36 / zöld | 36 / zöld | |
| `teszt_olvaso_szerver.py` | 86 / 2 piros | 90 / 2 piros (1 kihagyva) | új: `TestNavigacio` (4 teszt), zöld |
| `teszt_pilot_aranymintaval.py` | 22 / 2 piros | 22 / 2 piros | a jelölés-kapcsoló a fejlécbe költözött, a jelölése változatlan |
| `teszt_tervezo.py` | 48 / zöld | 48 / zöld | a regiszter 83 elemének minden szelektora talál; a Tervező kapcsoló a ⚙ menüben, a sorrend-őr zöld |
| **összesen** | **279, ebből 4 piros** | **283, ebből 4 piros** (mind a 4 ismert DT299-eset; új piros: 0; 1 kihagyott teszt) | |

**A 4 piros mind a régi adatbázis ismert esete (DT299), az M1 előtt is piros volt, és nem a #134 hibája:** `TestD2PilotEgyezes.test_1moz_1_25` (`vers:macula`), `TestD2PilotEgyezes.test_zsolt_22` (`vers:tsk_darab`), `test_heber_csempe_szavankent_a_pilot_szerint` (1Móz 1:9 LXX-alak), `test_szamlalok_egyeznek_a_pilottal` (könyvszám 57 / 61). **Új piros: 0.** A regiszter-őr (`regiszter_or.py`): 0 hiba.

A lassú `teszt_szintek.py` (DT129) nem futott (`--gyors`); a hozzáférési szintek kódja nem változott (a szintváltó a ⚙ menübe került, ugyanazokkal a hivatkozásokkal). A teljes futás az M5-é.

## 4. Nyitott pontok

1. **Az Aa CSSOM-mal állítja a betűméretet** (a token-szabály — betűméret csak tokenből — a stíluslapra vonatkozik, és ott nincs literál). Ha az M3 tokenekből akarja (pl. fokozatonkénti `--fs-*` tokenekkel), ott dönthető el; tartalmi döntést nem igényel.
2. **Arculat (M3):** a kánon-sáv és a könyvválasztó műfajszínei (`data-mufaj` → `--g-*`), az egysoros fejléc nagy képernyőn (920 px-en ma három sor: elemek, kánon-sáv, jelölés + Legutóbb; az első vers 249 px-nél), a kereső mezőjének szélessége, a pirula-chipek, a világos alaptéma.
3. **A nem fejezet-lapok** (kezdőlap, könyv, kereső, szó-lap) fejléce 900 px alatt a régi (tördelt, nem navigációs lap); a brief a fejezet-lapot (olvasót) írja elő. Ha ezeken is navigációs lap kell, az M3/M4-ben eldönthető.
4. **Valódi mozgás:** a rejtett böngészőpanelen az átmenet, a sima görgetés és a `scroll` esemény nem fut, ezért a húzás, a pirula és a lap mozgása az M4 telefonos próbáján mérendő.
5. **Munkamódszer:** egy csere-szkriptet (a `fejezet.html` öt cseréje, magyar szöveggel) idézett heredockal írtam fájlba, majd a fájlt futtattam; a szabály a heredocot is kizárja. Kár nem keletkezett (a diffet soronként ellenőriztem); utána minden szkript a Write eszközzel készült.
