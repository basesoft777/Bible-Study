---
feladat: 29
cim: A szótárfordítás döntései, a #7 és az FP3 halasztása
kod: SZOTAR_FORD_NAPLO
tipus: naplozas
modell: sonnet
allapot: lezarva
ag: claude/f29-szotar-ford-naplo
ad: a D42–D50 a FELADATOK.md döntésnaplójában; a #7 és az FP3 (#27) fejléce halasztott állapotra igazítva
kovetkezo: /kovetkezo, az EMELES befogadása után
olvas: [FELADATOK.md, "F*_BRIEF.md"]
ir: [F07_THAYER_ELES_BRIEF.md, F27_FP3_BRIEF.md, FELADATOK.md]
fugg: []
pr: "#90"
lezarva_osszegzes: a D42–D50 a FELADATOK.md döntésnaplójában (#EM = #28); a #7 és az FP3 (#27) fejléce és a #7 csonk-törzse halasztott (D46); ellenőrzés `naplok/ELLENOR_F29.md`
---

# F<nn>_SZOTAR_FORD_NAPLO_BRIEF.md — A szótárfordítás döntései

*FELADATOK #<nn> · Modell: sonnet · v3 · 2026.09.30 · naplózás, tartalmi munka nélkül*

## 1. Cél

A chat 2026.09.30-án eldöntötte:

- a lexikonba kerülő Strong-számok **teljes** Thayer- és BDB-szócikkét az Opus fordítja (az EMELES feladat);
- a render ebből csak a motívumhoz illeszkedő jelentéstartományt veszi át;
- a teljes szótár gépi alapfordítása halasztva van, amíg nincs böngésző felhasználó; addig a többi szócikk angol.

Ez a brief rögzíti a döntéseket, és a #7 és az FP3 (#27) fejlécét halasztottra állítja, hogy ne induljanak el.

## 2. Előfeltétel

Az EMELES befogadása a `main`-en van; a számát a `kod` mező alapján vedd (`#EM`). Ha hiányzik, állj meg.

## 3. Lépések

### N1 — Döntésnapló

A sorokat a következő szabad D-számtól vedd fel, sorrendben. A chat D42-től számolt (a #26 naplózó D34–D41-e után). Ha közben foglalt lett, csússzon, és ezt a zárójelentésben jelezd; más briefet ne írj át. A `#EM` helyére a valódi számot írd.

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D42 | A lexikonba kerülő Strong-számok teljes Thayer- és BDB-szócikkét az Opus fordítja (#EM); a felhasználó szúrópróbát olvas | ott a legjobb minőség, ahol olvassák; a Gemini v3 fordítása (pl. G26) nem volt elég jó | Gemini mindenre; gépi alap + Opus-emelés |
| D43 | Tárolás az `adat/forditasok.tsv`-ben: `teljes` szintű `opus`/`kezi` sor; a meglévő jelentésszintű `kezi` sorok megmaradnak, elsőbbségi sorrend `kezi` > `opus`; a render a jelentést a forrás tagolása mentén vágja ki, ezt a tagolás-kapu biztosítja | egy fordítás, több nézet | jelentésenkénti fordítás |
| D44 | CI-őr: a lexikon minden Thayer- és BDB-hivatkozásához kötelező az `opus` vagy `kezi` fordítás (jelentés- vagy `teljes` szinten) | a fordítás ne maradhasson ki | kézi ellenőrzés |
| D45 | Közös, determinisztikus javítóréteg (`eszkozok/normalizal.py`) és fordítási kapuk (idézőjel, tagolás, igetörzs) minden fordítási kimenetre | a gépi szabály biztosabb, mint a promptban kért | csak promptszabály |
| D46 | A teljes szótár gépi alapfordítása (#7 Thayer, BDB-alap) és a modellpróbák (FP3 #27, BDB-próba) halasztva, amíg nincs böngésző felhasználó (a #25 HTML-felület vagy a kereskedelmi kiadás veti fel); addig a nem lexikoni szócikkek angolok | ma senki nem böngész szócikkeket; a fordítás akkor is elkészülhet | gépi alap most (kb. 25 USD) |
| D47 | Az első fordítási kör: 47 szócikk (18 Thayer, 29 BDB), 187 863 karakter (a 2026.09.30-i mérés); a G1941 már kézi | a Max-keret elbírja; a szöveg kevesebb mint 2%-a | — |
| D48 | A fordítás a motívum-munkafolyamat lépése: új motívum vagy előfordulás után a hiányzó szócikkek fordítása (`MUNKAMENET.md`) | a lexikon bővülésével folyamatos | egyszeri fordítási menet |
| D49 | Szúrópróba menetenként a lefordított szócikkek 10%-a, legalább 5; 20% fölötti kifogásnál a menet megáll | a felhasználó döntése: csak szúrópróba | minden szócikk kézi átnézése |
| D50 | A lexikonba a szótárból csak a motívumhoz illeszkedő jelentéstartomány kerül, a Thayernél is (a BDB-nél eddig is így volt); a kiválasztás a render/#9 feladata: gépi jelölt (a jelentés igehelyei metszik a motívum előfordulásait), a döntés a felhasználóé | kisebb, pontosabb kimenet | a teljes szócikk a lexikonban |

A generált blokkokhoz ne nyúlj (D24, D25).

### N2 — A #7 fejléce (`F07_THAYER_ELES_BRIEF.md`)

Csak ez a mező változik, a csonk „Következő lépés” sorával együtt:

| Mező | Új érték |
|---|---|
| `kovetkezo` | halasztva (D46): a teljes Thayer gépi fordítása akkor, ha lesz böngésző felhasználó; a lexikon szócikkeit a #EM fordítja |

### N3 — Az FP3 fejléce (`F27_FP3_BRIEF.md`)

| Mező | Új érték |
|---|---|
| `kovetkezo` | halasztva (D46): a gépi alap modellválasztásához kell, a #7-tel együtt veszi elő a felhasználó |

A brief szövegéhez ne nyúlj.

## 4. Ellenőrzés és zárás

1. `python eszkozok/feladatok.py ellenoriz` = 0.
2. `python eszkozok/feladatok.py fuggesek`: nincs körkörös függés; a #9 a #EM után jön (az `adat/forditasok.tsv` miatt). A kimenetet idézd.
3. Zárás a `/kovetkezo` szerint: `fuggetlen-ellenor`, draft PR, a saját fejléc `lezarva`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | B modell (gépi alap + Opus-emelés) | — |
| v2 | 2026.09.30 | jelentésszintű emelés (D50) | — |
| v3 | 2026.09.30 | teljes szócikk Opus-fordítása csak a lexikon Strong-számaira; a gépi alap, a #7, az FP3 és a BDB-próba halasztva; új kód (`SZOTAR_FORD_NAPLO`), hogy ne keveredjen a visszavont változattal | a felhasználó döntése: ma nincs böngésző felhasználó |
