# LXX_OS_LEFEDETTSEG — M1 végrehajtás és M2 ellenőrzés

*F54 · 2026.10.11 · modell: sonnet · a mérések `manual` proveniencia (gépi összevetés; a mintavétel sorai a `lekerdez.py lxx-hid` saját proveniencia-sorával). A tartalmi egyezést a végrehajtó állapította meg (nyelvi olvasat, `manual`); független ellenőr még nem látta.*

`scope=konkordancia/LXX_OS/*.tsv, konkordancia/Karoli_1908.tsv | forras=manual (naplok/LXX_OS_LEFEDETTSEG_M2_ellenoriz.py) | ts=2026-10-11`

## 1. Mi történt (M1)

- `eszkozok/lxx_os_import.py`: `lefedettseg_javit_konyv()` (a teljes import `process_book` utáni lépése is) és `--ujrabesorol-lefedettseg` (offline). Csak az `igehely_karoli` és a `karoli_ok` oszlop változhat — a függvény `assert`-tel veti össze a sorokat az eredetivel (K5).
- **F54.2 (A1 + A3):** 310 új kulcs. Az M0 A1+A3 (308) közül 304 jött létre; **4 kimaradt** (2Móz 37:4, 37:13, 38:1, 1Kir 4:27), mert az általános szabályok (tábla-jelölt + sorrend-beágyazás / szószám-korreláció / kölcsönös egyértelműség) nem támasztják alá, csak a régi, kivezetett szöveg egyezése — ezek üresek maradnak. **6 extra** (az 503-on kívül, ugyanazokkal a szabályokkal): Zsolt 13:6, Zsolt 54:2 (DT-F54a (b)), Én 5:17–19, Ézs 64:1.
- **A2 (130 vers):** a `karoli_vers_felulbiralas.tsv` új sorai (`naplok/LXX_OS_LEFEDETTSEG_A2_general.py`), `indok` oszlopban a párosítás módja, r és a mintavétel versei; a függvény csak üres kulcsra és csak nem foglalt Károli-versre alkalmazza. A felülbírálat feltétele (DT-F54a (a)) az 1. szakasz mintavétele fejezetenként.
- A `teszt_lekerdez_sir.py` zöld (11 teszt), a rögzített számok nem változtak.

## 2. Ellenőrzések (K4, K5, lefedettség)

| Ellenőrzés | Előtte | Utána |
|---|---|---|
| idegen Károli-kulcs | 0 | **0** |
| kettős Károli-kulcs | 9 | **9** (l. 3. szakasz) |
| K5: más oszlop változott-e | — | nem (a javító `assert`-je futáskor ellenőriz) |

Kulcsolt Károli-versek az elsődleges fájlban (kulcsolt / összes), csak a változó könyvek:

| Könyv | előtte | utána | | Könyv | előtte | utána |
|---|---|---|---|---|---|---|
| Zsolt | 2458 | 2525 / 2527 | | Jób | 991 | 1052 / 1068 |
| Jer | 1239 | 1294 / 1364 | | Hós | 137 | 194 / 195 |
| Péld | 841 | 863 / 914 | | 2Móz | 1103 | 1134 / 1213 |
| 1Sám | 738 | 772 / 811 | | Dán | 327 | 357 / 357 |
| Én | 88 | 117 / 117 | | Józs | 616 | 643 / 658 |
| Ézs | 1264 | 1288 / 1290 | | Jón | 46 | 48 / 48 |
| 4Móz | 1285 | 1286 / 1287 | | 1Kir | 753 | 753 / 817 |

## 3. A 9 meglévő kettős kulcs (DT-F54a (d))

Nyolc **jogos összevonás**: egy Károli-verset az LXX két versre bont (a két LXX-vers együtt adja a Károli-verset), tehát a kettős kulcs helyes, és a K4 „kivéve, ahol a megfeleltető tábla összevonást ír” kivételébe esik: 1Krón 12:4 (LXX 12:4 + 12:5), 1Kir 7:1 (7:38 + 7:50), Préd 2:26 (2:25 + 2:26), 2Móz 38:30 (39:7 + 39:9), 2Móz 39:1 (36:8 + 39:12), 2Móz 39:40 (39:19 + 39:21), Jer 25:13 (25:13 + 32:13), Jer 49:34 (25:14 + 25:20). Ezek nem változnak.

Egy **hibás**: Zsolt 13:1 (LXX 12:1 és 12:2 is erre mutat), és mögötte a Zsolt 13 kulcsai egy verssel eltoltak (LXX 12:2 → 13:1, 12:3 → 13:2, 12:4 → 13:3, 12:5 → 13:4; a helyes: LXX 12:n → Zsolt 13:n, n = 1..6). A javítás **nem történt meg**: a változó kulcsokra hivatkozó adat érintett, ezért ⛔ (l. a DONTESEK.md DT-F54b sorát).

## 4. Mintavétel — az A2 fejezetek (a felülbírálat feltétele)

| Fejezet | Párosítás | Ellenőrzött versek (Károli ↔ LXX) | Eredmény |
|---|---|---|---|
| 2Móz 35 | L+0, r=0,81 | 35:1 ↔ Ex 35:1 (Mózes egybegyűjti a gyülekezetet); 35:10 ↔ 35:10 (a bölcs szívűek jöjjenek); 35:30 ↔ 35:30 (Bezalel, Húr fia, Júda törzséből) | átment |
| Dán 3 | K+0, r=0,89 | 3:1 ↔ Theod. 3:1 (aranykép, 60 sing); 3:12 ↔ 3:12 (Sidrák, Misák, Abednégó); 3:25 ↔ 3:92 (négy férfi a tűzben, „istenek fia”) | átment (a 3:24–30 az LXX 3:91–97, a Theodotion betoldása miatt) |
| Hós 2 | L+3, r=0,88 | 2:1 ↔ Hos 2:4 (pereljetek anyátokkal); 2:8 ↔ 2:11 (visszaveszem a búzát, mustot, gyapjút, lenet); 2:20 ↔ 2:23 (az egek meghallgatják a földet) | átment (a régi kivonat +2-t használt, ez +3: a régi szöveg itt is eltolt volt) |
| Hós 13 | L+0, r=0,73 | 13:1 ↔ 13:1 (Efraim … Baál, meghalt); 13:7 ↔ 13:7 (párduc az úton) | átment |
| Hós 14 | K−1+L+0, r=0,95 | 14:1 ↔ 14:1 (Samaria pusztul); 14:6 ↔ 14:6 (harmat, liliom, Libánon) | átment |
| Jób 37 | L+1, r=0,70 | 37:1 ↔ Job 37:2 (halljátok a dörgést / szájából kijön); 37:5 ↔ 37:6 (a hónak: essél le); 37:14 ↔ 37:15 (laza: „Isten tette a műveit”, a Károli-szöveg villámot említ); 37:23 ↔ 37:24 (az emberek félik, a bölcsek is) | **átment** 4-ből 3 szoros egyezéssel; a 37:14 az LXX szabad fogalmazása — a Jób 37 felülbírálati sorai ezzel együtt beírva; a döntés feltétele („tartalmi egyezés nélkül marad bizonytalan”) nem állt elő |

## 5. Mintavétel — `lekerdez.py lxx-hid`, 17 A osztályú vers

A sorok az `lxx-hid` kimenetéből (LXX-vers és `karoli_ok` a kimenet saját sora, a proveniencia-sor: `scope=range:<vers> | forras=LXX_OS/<fájl>.tsv+TAGNT_kivonat.tsv | n=… | ts=2026-10-11…`). A görög szövegre a tartalmi egyezés a Károli-verssel:

| Károli | LXX-vers (`karoli_ok`) | Tartalmi egyezés |
|---|---|---|
| Jób 38:1 | Job 38:1 (versmegfeleltetes_tabla) | az Úr felel Jóbnak a forgószélből — egyezik |
| Jób 38:20 | Job 38:20 (versmegfeleltetes_tabla) | a lakóhely útjai — egyezik (laza) |
| Jób 37:5 | Job 37:6 (kezi_eltolas_tabla) | a hónak parancsol: essél a földre — egyezik |
| Hós 11:1 | Hos 11:1 (versmegfeleltetes_tabla) | gyermek Izráel, Egyiptomból hívtam — egyezik |
| Hós 2:8 | Hos 2:11 (kezi_eltolas_tabla) | búza, must, gyapjú, len — egyezik |
| Zsolt 3:1 | Ps 3:1 (zsolt_felirat_eltolas) | Dávid zsoltára, Absolon elől — egyezik |
| Zsolt 51:2 | Ps 50:2 (zsolt_felirat_eltolas) | Nátán, Bethsabé — egyezik |
| Zsolt 54:2 | Ps 53:2 (zsolt_felirat_eltolas) | a Zifeusok Saulnak — egyezik (az 503-on kívüli extra) |
| Zsolt 13:6 | Ps 12:6 (versmegfeleltetes_tabla) | kegyelmedben bíztam, énekelek — egyezik (extra) |
| Jer 33:1 | Jer 40:1 (versmegfeleltetes_tabla) | másodszor szólt Jeremiásnak a tömlöc pitvarában — egyezik |
| Én 5:17 | Ének 6:1 (sorrend_beagyazas) | hová ment a szerelmesed — egyezik (extra) |
| Ézs 64:1 | Isa 64:1 (sorrend_beagyazas) | olvadás, tűz, a név ismertté tétele — egyezik (extra) |
| Ézs 63:19 | Isa 63:19 (sorrend_beagyazas) | a „kik felett nem neveztetett neved” — egyezik; az LXX-vers vége már a Károli 64:1 eleje |
| Péld 18:1 | Prov 18:1 (versmegfeleltetes_tabla) | ürügyet keres, aki elválni akar a barátoktól — egyezik |
| Józs 8:1 | Josh(B) 8:1 (versmegfeleltetes_tabla) | ne félj, Ai királya kezedbe adva — egyezik |
| 1Sám 17:1 | 1Sam 17:1 (versmegfeleltetes_tabla) | a Filiszteusok Sokónál — egyezik |
| Jón 2:1 | Jon 2:1 (sorrend_beagyazas) | nagy hal, három nap — egyezik |

Legalább 3 Jób-, 2 Hóseás- és 2 zsoltárvers: teljesül (3 / 2 / 4). Hiba nem merült fel; az egyetlen laza egyezések: Jób 38:20, Jób 37:14 (az LXX-Jób szabad fogalmazása).

## 6. Nyitott megállapítások

- **⛔ DT-F54b:** a Zsolt 13 hibás kulcsai (3. szakasz); a változó kulcsokra hivatkozik a `konkordancia/LXX_versszintu_parok.tsv` 15 sora (Zsolt 13:3 → Psalms (LXX) 12:4 8 sor; Zsolt 13:4 → 12:5 7 sor).
- **Elavult generált tábla:** a `konkordancia/LXX_versszintu_parok.tsv` (generált, `eszkozok/lxx_versszintu_import.py`) az M1 előtti kulcsokból készült; a 438 új kulcs miatt újragenerálandó — a hatókörön kívül, a Zsolt 13 döntése után egyszerre.
- **N-F54a:** Péld 12, Jób 17, 2Móz 36 (NYITOTT_FELADATOK.md).
- **Megmaradt üres:** 3 B, 5 C, a bizonytalan (Péld 12 27, Jób 17 15, 2Móz 36 11, Jer 48:40–41 2, 2Móz 39:38, Zsolt 13:5 — ez utóbbi most a Zsolt 13:6 extra-kulcs mellett: a Károli 13:5 a hibás kulcsú LXX 12:5-nek felel meg) és a 4 kimaradt A1 (2Móz 37:4, 37:13, 38:1, 1Kir 4:27).

## 7. Utólagos javítások és tételes melléklet (F54.4)

- **Javított hiba (F54.3 → F54.4):** az A2 felülbírálati sorok az F54.3-ban versenként csak az első szósort kulcsolták (az `lxx-hid` ezért pl. a Hós 2:8-ra n = 1-et adott). Az F54.4 mind a 130 versre minden szósort kulcsol; ellenőrzés: nincs olyan LXX-vers, amelynek szósorai között kulcsos és kulcs nélküli is van (0 vegyes vers az `LXX_OS`-ben). A 4. és 5. szakasz tartalmi megállapításai ezen nem változnak (a vers azonosítása ugyanaz).
- **Zsolt 13 (DT-F54b):** a 6 felülbírálati sor (LXX Ps 12:n → Zsolt 13:n) beírva; kettős kulcs 9 → **8** (mind jogos összevonás), idegen 0. A Zsolt 13:6 extra kulcs újraellenőrizve: az `lxx-hid Zsolt 13:6` a Psalms (LXX) 12:6-ot adja (28 szó, „kegyelmedben bíztam, énekelek”), a lánc 12:1–12:6 → 13:1–13:6 egységes. Zsolt kulcsolt: 2526 / 2527.
- **A 6 extra kulcs (az 503-on kívül, ugyanazokkal a szabályokkal):** Zsolt 13:6 → Ps 12:6 (tábla, kjv „13:5;13:6”); Zsolt 54:2 → Ps 53:2 (feliratvers, sorrendi párosítás; DT-F54a (b)); Én 5:17, 5:18, 5:19 → Ének 6:1, 6:2, 6:3 (sorrend-beágyazás); Ézs 64:1 → Isa 64:1 (sorrend-beágyazás; az LXX 63:19 vége már a Károli 64:1 eleje).
- **A 4 kimaradt vers** (üresek; csak a régi, kivezetett szöveg egyezése támasztaná alá, az általános szabályok nem): 2Móz 37:4 (jelölt Exodus 38:4, 8 szó, r = −0,01); 2Móz 37:13 (Exodus 38:10, 25 ↔ 15 szó, r = 0,40); 2Móz 38:1 (Exodus 38:22, 21 ↔ 21 szó, r = −0,20) — az LXX-2Móz 36–39 átrendezett; 1Kir 4:27 (1 Kings 5:1, 48 ↔ 23 szó, r = 0,43).
