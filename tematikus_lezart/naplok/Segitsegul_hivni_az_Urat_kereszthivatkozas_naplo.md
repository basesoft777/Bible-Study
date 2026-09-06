# Kereszthivatkozás-napló — "Segítségül hívni az Úr nevét"

*Létrehozva: 2026.09.05, retroaktívan, a v12 sablon 1. pontjának
"Kötelező napló" előírása szerint. A 2026.08 havi eredeti kutatás
jelölt-listája nem maradt fenn dokumentált formában — ez a napló a
2026.09.05-i retroaktív audit teljes körét rögzíti.*

## Vizsgált kulcsszavak
H7121 (קָרָא, "hívni"), H8034 (שֵׁם, "név"), G1941 (ἐπικαλέομαι)

## Módszertan
Pozíció-alapú frázis-keresés (`eszkozok/frazis_kereses_pozicio_
alapon.py`), kalibrálva a már ismert találatokon, kiegészítve BDB
szótári idézet-ellenőrzéssel, TSK kereszthivatkozással és
szisztematikus LXX-egyeztetéssel. Részletek: l. a chat-munkamenet
2026.09.05-i naplója.

## Nyers találatok forrásonként
- Puszta H7121+H8034 közelség-grep: 153 nyers találat (túl zajos)
- Kalibrált szűk ablak (explicit isteni név): a 9 korábban ismert +
  2Móz 33:19/34:5
- Anaforikus bővítés (névmásos "az ő neve" forma, ha isteni név
  korábban szerepel a versben): 7 jelölt
- BDB szótári idézet (H7121 2.c sense saját forráslistája): Jer 10:25
  = Zsolt 79:6
- TSK kereszthivatkozás (2Móz 33:19/34:5-ről kiindulva): Ézs 12:4

## Tartalmi minősítés minden jelöltre

| Igehely | Döntés | Indoklás |
|---|---|---|
| Zsolt 105:1 / 1Krón 16:8 | ✅ BEÉPÍTVE | Azonos szerkezet, explicit isteni név, PÁRHUZAM-funkció |
| Ézs 12:4 | ✅ BEÉPÍTVE | Azonos szerkezet, névmásos, korábban יהוה a versben, PÁRHUZAM-funkció |
| Jer 10:25 / Zsolt 79:6 | ✅ BEÉPÍTVE | Fordított szórend (főnév-ige), tagadó/vádló forma — "nem hívták segítségül a Te nevedet" |
| 2Móz 33:19 / 2Móz 34:5 | ✅ BEÉPÍTVE, külön kategóriában | Fordított irányú (Isten mondja ki saját nevét) — BDB sense 3 ("proclaim"), NEM sense 2.c ("invocation") — nem sorolható a meglévő kapcsolat-funkciók egyikébe sem, l. study 1. pontja |
| Ézs 43:1 | ❌ ELUTASÍTVA | "Néven szólítalak" (Istent hívja valakit néven) — homonim szerkezet, MÁS jelentés (nem "Isten nevét hívni segítségül") |
| Ézs 44:5 | ❌ ELUTASÍTVA | "Jákób nevével nevezi magát" — identitás-felvétel, nem invokáció |
| Ézs 45:3 | ❌ ELUTASÍTVA | "Én, [az Úr], aki téged neveden hívlak" (Círuszról) — ugyanaz a homonim szerkezet, mint 43:1 |
| Ruth 4:11 | ❌ ELUTASÍTVA | "hogy híres neve legyen Betlehemben" — hírnév-áldás, más jelentésű "név" |
| Ruth 4:14 | ❌ ELUTASÍTVA | "hogy neveztessék az ő neve Izráelben" — ugyanaz, mint 4:11 |
| Zsolt 116:4, 13, 17 | ✅ MÁR KORÁBBAN BEÉPÍTVE | A study saját prózája már idézte; ezúttal formálisan táblázatba emelve |

## Összegzés
17 igehely a végleges táblázatban (5 genezisi + 1Kir 18:24-26 + 2Kir
5:11 + Sof 3:9 + Jóel 2:32 + Zsolt 116:4,13,17 + Zsolt 105:1/1Krón 16:8
+ Ézs 12:4 + Jer 10:25/Zsolt 79:6 + 2Móz 33:19/34:5), 5 jelölt
elutasítva megnevezett indokkal.

## LXX-ellenőrzés kiegészítő eredménye
15/17 igehely ἐπικαλέομαι-t használ a LXX-ben (néhánynál
"ELTERO_SZOVEGALAP" jelzéssel, Strong-szám nélkül, de a görög szóalak
azonosítható ἐπικαλέομαι-ként). 2 kivétel: 2Móz 33:19/34:5 (καλέω),
Ézs 12:4 (βοάω). Emellett két, ehhez a study-hoz nem tartozó, de itt
felfedezett LXX-híd adatminőségi észrevétel:
- **Zsolt 116:4**: a ἐπεκαλεσάμην szóalak tévesen G4506-tal (ῥύομαι)
  van címkézve a `LXX_kivonat_Zsoltarok.tsv`-ben — javítást igényel,
  külön Code-prompt tárgya, nem ennek a study-nak a hatásköre.
- **Zsolt 116:17**: a görög kivonat csak a vers első felét
  tartalmazza (a "segítségül hívom nevét" tagmondat hiányzik) — az
  LXX-híd dokumentált, ~94-96%-os átlagos lefedettségének egy konkrét
  esete, nem egyedi hiba.
