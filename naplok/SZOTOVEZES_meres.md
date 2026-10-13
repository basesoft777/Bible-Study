# SZOTOVEZES — mérési napló (FELADATOK #94)

*A #94 (F94_SZOTOVEZES_BRIEF.md) mérési naplója. Az 1–4. szakasz a 2026-10-12/13-i, repón kívüli előmérés átvétele (F94.0/4): a fájlok tartalma szó szerint, mindegyik a saját proveniencia-sorával (a forrásfájl neve + sha256 + az átvétel ideje). Az 5. szakasz a régi 1–2. minta eltérés-listája a DT130 végleges pontjaitól (F94.0/3, ⛔ felhasználói döntésre vár). Az emMorph (CC BY-NC-SA) számai csak mérceként szerepelnek; az emMorph kódja és kimenete a repóba nem kerül (DT130 (12)). Az előmérés mintái a mérés idején a régi oszlopnevekkel (`to_regies`, `to_mai`) álltak; az átvett, egységes sémájú alakjuk: `adat/szoto/szoto_minta_{1,2,3}_*.tsv` (SEMA 2.27).*

*Állapotjelölés: az 1. és a 2. minta szótári alakjai modell-javaslatok (`modell_ellenorizetlen`; a 2. mintában 6 sor `felhasznalo`); a 3. minta mind a 113 sora `felhasznalo`. A mérőszám csak az utóbbin független ellenőrzésű.*

## 1. Mérési terv (az előmérésé)

*proveniencia: scope=manual (a mérési terv, modell-javaslat, a felhasználó jóváhagyta 2026-10-13) | forras=meresi_terv.md (sha256:fc2f69c77b5ebe513170bc20fa0de54624b8aa975802a2192c8e498d6b8afc38; a repón kívüli előmérés, 2026-10-12/13, szó szerinti átvétel) | ts=2026-10-13T12:09Z*

*2026-10-13. Repón kívüli előmérés; a döntési tétel alapja. A felhasználó jóváhagyta: hibrid prototípus, független minta (a mérés előtt átnézésre), mérés; a keresési találati arány is mérendő.*

#### 1. A hibrid (licenctiszta)

1. **Károli-helyesírási réteg:** *-űl → -ül*, *szűl → szül*, *körűl → körül*, *sűly → süly*, *nyny → nny* stb. (szabálylista).
2. **Régies igealak-réteg:** *-á/-é* (múlt, tárgyas, E/3), *-ának/-ének* (múlt, T/3), *-a/-e* (múlt, alanyi, E/3) levágása; a jelölt tövet a simplemma szótára igazolja (ismert ige-e). Ha nem igazolható, a jelölt elvetődik.
3. **Kivételtábla:** rendhagyó tövek (*vala, lőn, vevé, menének, evének, tevé* …), névmások a 3. döntés szerint (*néki, vele, nékik → ő*), tőváltó névszók (*fi- → fiú*, *ur- → úr*, *szav- → szó*). Általános Károli-ismeret alapján, nem a mérés hibáiból válogatva.
4. **simplemma** a maradékra. Az emMorph csak összehasonlító mérce (CC BY-NC-SA).

#### 2. Független minta

Kb. 200 Károli-szóalak **más könyvekből**: Zsoltárok (1–41), Ézsaiás (40–55) és a párosított ÚSZ-levelek (Gal, Ef, Zsid). Ugyanaz a rétegzés, mint az első mintánál. Az első minta alakjai kizárva. A tövek modell-javaslatok; **a mérés előtt a felhasználó átnézi**.

#### 3. Mérőszámok

- **M1 — tövezési pontosság:** alakonként és előfordulással súlyozva, rétegenként; a hibrid, a simplemma egyedül és az emMorph (mérce).
- **M2 — keresési találati arány** (a teljes párosított Bibliában, automatikusan): 25 gyakori és 10 ritka lemmára. A célhalmaz a lemma fő Strong-számához párosított Károli-tokenek köre. Mérve, hogy mennyit talál meg ebből:
  - (a) a tő-keresés;
  - (b) a tő vagy a pontos alak;
  - (c) a tő vagy a Strong-szám.

  Mellette a tő-keresés fölösleges találatai: más Strong-hoz kötött token aránya.
- Proveniencia-sor minden számhoz; az aranyminta-állapot (ellenőrizetlen / ellenőrzött) jelölve.

#### 4. Döntési küszöb (javaslat)

A hibrid akkor mehet a `pardes.db`-be (a #92 bővítése vagy külön feladat), ha a független mintán előfordulással súlyozva ≥ 90%, és az M2 (c) találati arány ≥ 98% a vizsgált lemmákon. Ha nem éri el, a kivételtábla bővítése gyakoriság szerint, újramérés.

*Megjegyzés (F94.0): a 2. pont „Gal, Ef, Zsid” része üres maradt (a `token_karoli` csak az ÓSZ-t tartalmazta); a független minta valójában Zsolt 1–41 + Ézs 40–55. Az M2 a terv szerinti definícióval nem informatív, a felhasználó jóváhagyásával újradefiniálva (pooled célhalmaz, l. 2.3). A #94 a küszöböt a negyedik mintán méri (K3).*

## 2. Mérések

### 2.1 Első minta (1Móz 1–25, 213 alak, fejlesztési halmaz)

*proveniencia: scope=1. minta, 213 alak, modell_ellenorizetlen | forras=ATADAS.md 3. szakasz (sha256:2e637161b073ee2081adf1516828b93df14cd1b7a3621a0cf47c109dcf690150; a repón kívüli átadó jegyzet; a `meres.py` kimenete nem mentődött külön fájlba, a soronkénti részlet `meres_reszlet.tsv` emMorph-kimenetet tartalmaz, ezért nem kerül át) | ts=2026-10-13T12:09Z*

- Alakonként / súlyozva: simplemma 69% / 84,5%, emMorph (mérce) 67% / 86,6%, a kettő együtt 85% / 90,5%; a régies igéken (teremté, látá, elmenének) a nagy elemzők 2%-on.
- Hibrid v2 a két fejlesztési halmazon (1. és 2. minta): 99,2% / 97,6% (súlyozva), a hangolás után — **fejlesztési szám, nem független**. A teljes Károlin a v1→v2 váltás 11 449 alakot változtatott; ismert új hibák: hozzá→hoz, alá→al, elé→el, éljen→élj, köteleid→kötelei, -ván/-vén csonka tő.

### 2.2 M1 a 2. (független) mintán, a hibrid v1-gyel (a v2 előtt)

*proveniencia: scope=2. minta, 180 alak (6 felhasznalo, 174 modell_ellenorizetlen); a táblában szereplő „hibrid” a v1 | forras=meres_fuggetlen_eredmeny.md (sha256:b78cb877c3a044066380e2f2e3d670d25cc298a909857d2bbd0f28ad5f5216e0; a repón kívüli előmérés, 2026-10-12/13, szó szerinti átvétel) | ts=2026-10-13T12:09Z*

#### M1 — tövezési pontosság (alakonként / előfordulással súlyozva)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid | 73% / 84.4% (132/180) | 85% / 87.4% (34/40) | 73% / 81.4% (47/64) | 75% / 76.7% (24/32) | 23% / 35.9% (3/13) | 76% / 75.6% (16/21) | 80% / 84.2% (8/10) |
| simplemma | 69% / 78.4% (124/180) | 80% / 80.3% (32/40) | 72% / 80.9% (46/64) | 69% / 69.8% (22/32) | 0% / 0.0% (0/13) | 76% / 75.6% (16/21) | 80% / 84.2% (8/10) |
| emMorph (mérce) | 74% / 88.0% (134/180) | 95% / 92.6% (38/40) | 97% / 95.8% (62/64) | 16% / 14.0% (5/32) | 15% / 33.3% (2/13) | 90% / 89.7% (19/21) | 80% / 75.3% (8/10) |
| hibrid VAGY emMorph | 88% / 95.3% (159/180) | 98% / 97.4% (39/40) | 97% / 95.8% (62/64) | 78% / 79.1% (25/32) | 31% / 43.6% (4/13) | 90% / 89.7% (19/21) | 100% / 100.0% (10/10) |

scope=független minta, 180 alak (Zsolt 1–41, Ézs 40–55, Gal, Ef, Zsid), sha256:cbdf2843c34c | forras=szoto_fuggetlen_minta.tsv (6 sor felhasználói döntéssel, a többi ellenőrizetlen) + hibrid.py + simplemma 2.0.0 + emMorph/hfst (mérce, CC BY-NC-SA) | ts=2026-10-13T07:02Z

##### A hibrid hibái (alak → hibrid tő | elvárt; súly)
Ímé→Ímé | ím/íme (31); Urat→ura | Úr/Úr (29); Istenem→istenem | Isten/Isten (28); nincs→van | nincs/nincs (27); lelkemet→lelkem | lélek/lélek (20); reám→reá | én/én (13); Izráelnek→Izráelnek | Izráel/Izráel (12); Istene→istene | Isten/Isten (11); orczádat→orczádat | orca/arc (7); méhétől→méhétől | méh/méh (7); igazat→igaza | igaz/igaz (6); előre→előre | elő/elő (5); eleitől→eleitől | elő/eleje (4); elvesznek→elveszik | elvész/elvész (4); leborulnak→leborul. | leborul/leborul (4); jőnek→jő | jön/jön (4); törnek→törik | tör/tör (4); közülök→közülök | közül/közül (3); gyűlölőim→gyűlöl | gyűlölő/gyűlölő (3); házában→háza | ház/ház (3); gyalázatot→gyaláz | gyalázat/gyalázat (3); bosszankodjál→bosszankodjál | bosszankodik/bosszankodik (3); megváltá→megváltá | megvált/megvált (2); megvígasztalá→megvígasztalá | megvígasztal/megvígasztal (2); előttök→előttök | előtt/előtt (2); belőlök→belőlök | ő/ő (2); bennök→bennök | ő/ő (2); Mostantól→mostantól | mostan/most (2); kivánságának→kivánsága | kívánság/kívánság (2); szövetségévé→szövetsége | szövetség/szövetség (2); mértéklé→mértéklé | mértékel/mértékel (1); kifeszíté→kifeszíté | kifeszít/kifeszít (1); nyomorgatá→nyomor | nyomorgat/nyomorgat (1); vettetének→vet | vettetik/vettetik (1); elhamvadának→elhamvada | elhamvad/elhamvad (1); meglennének→megleszik | meglesz/meglesz (1); erejök→erejök | erő/erő (1); ragadománynyá→ragad | ragadomány/ragadomány (1); barátjának→barátja | barát/barát (1); derekának→dereka | derék/derék (1); alkotójának→alkot | alkotó/alkotó (1); magvának→magvának | mag/mag (1); lelkének→lelke | lélek/lélek (1); felebarátjának→felebarátja | felebarát/felebarát (1); sátrának→sátra | sátor/sátor (1); szolgájának→szolgája | szolga/szolga (1); pozdorjává→pozdorjává | pozdorja/pozdorja (1); tavává→tava | tó/tó (1)

Az ugyanitt futott, a terv szerinti M2 (a fő Strong-hoz párosított tokenek) nem informatív (a (c) definíció szerint 100%, az (a)-t a fordítási szinonímia uralja); összesítője:

> Összesen: cél 51108; (a) hibrid 37.7%, simplemma 32.6%; (b) hibrid 38.1%; (c) 100.0% (definíció szerint); gyakori (a) hibrid 42.1%, ritka (a) hibrid 9.5%
> scope=teljes Károli (token_karoli, oldal=hu, 456879 token, 54600 alak); 35 lemma a független mintából | forras=pardes.db + hibrid.py + simplemma 2.0.0 | ts=2026-10-13T07:02Z

### 2.3 M2 újradefiniálva (pooled célhalmaz), a 2. minta 35 lemmáján

*proveniencia: scope=teljes Károli ÓSZ (token_karoli), 35 lemma a 2. mintából; a pooled célhalmaz az emMorph-ot is tartalmazta — a #94 meres.py-ja emMorph nélkül számol (F94_SZOTOVEZES_BRIEF.md .1/4) | forras=meres_m2_eredmeny.md (sha256:e420928487aadf42b4c89548be93fbc56e65e33571fa5c4ea10246d224f8a3d7; a repón kívüli előmérés, 2026-10-12/13, szó szerinti átvétel) | ts=2026-10-13T12:09Z*

#### M2 (újradefiniálva) — keresési találati arány

| csoport | lemma | fő Strong | A(L) alak | cél | ebből Strong nélküli | (a) hibrid | (a) simplemma | (a) emMorph | (b) hibrid | (c) hibrid | tő-találat más Strong-on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gyakori | én | H0589 | 47 | 1179 | 423 | 99% | 96% | 100% | 99% | 99% | 5017/6182 |
| gyakori | az | H1931 | 61 | 25353 | 24845 | 100% | 100% | 100% | 100% | 100% | 4662/29892 |
| gyakori | mert | H3588 | 3 | 2471 | 49 | 100% | 100% | 100% | 100% | 100% | 362/2833 |
| gyakori | ő | H0413 | 47 | 1606 | 961 | 95% | 53% | 80% | 95% | 96% | 10392/11912 |
| gyakori | szól | H1696 | 69 | 727 | 17 | 99% | 99% | 65% | 99% | 100% | 624/1342 |
| gyakori | van | H1961 | 59 | 7570 | 6198 | 85% | 41% | 56% | 85% | 93% | 1156/7594 |
| gyakori | fel | H5927 | 10 | 235 | 39 | 100% | 87% | 87% | 100% | 100% | 1003/1238 |
| gyakori | ez | H0428 | 57 | 1427 | 941 | 99% | 99% | 100% | 99% | 99% | 1943/3355 |
| gyakori | te | H0859 | 44 | 1015 | 366 | 97% | 94% | 100% | 97% | 98% | 5245/6227 |
| gyakori | de | H0389 | 2 | 132 | 103 | 100% | 100% | 100% | 100% | 100% | 1254/1386 |
| gyakori | íme | H2009 | 5 | 437 | 17 | 100% | 8% | 8% | 100% | 100% | 97/534 |
| gyakori | úr | H3068 | 79 | 6534 | 42 | 95% | 95% | 100% | 95% | 100% | 771/6996 |
| gyakori | isten | H0430 | 134 | 2574 | 51 | 46% | 46% | 98% | 46% | 100% | 605/1796 |
| gyakori | nincs | H0369 | 6 | 314 | 5 | 4% | 100% | 100% | 61% | 98% | 33/45 |
| gyakori | így | H3541 | 2 | 416 | 198 | 100% | 100% | 100% | 100% | 100% | 218/634 |
| gyakori | mi | H0834 | 61 | 1236 | 638 | 93% | 93% | 99% | 93% | 97% | 2817/3968 |
| gyakori | mond | H0559 | 83 | 3598 | 26 | 100% | 42% | 33% | 100% | 100% | 602/4195 |
| gyakori | lesz | H1961 | 37 | 2605 | 719 | 94% | 66% | 73% | 94% | 99% | 534/2978 |
| gyakori | zsoltár | H4210 | 4 | 56 | 0 | 100% | 16% | 98% | 100% | 100% | 1/57 |
| gyakori | ha | H0518 | 2 | 815 | 209 | 100% | 100% | 100% | 100% | 100% | 547/1362 |
| gyakori | lélek | H5315 | 56 | 431 | 2 | 40% | 40% | 100% | 40% | 100% | 169/343 |
| gyakori | nagy | H1419 | 32 | 510 | 63 | 98% | 98% | 96% | 98% | 99% | 347/849 |
| gyakori | gonosz | H7451 | 26 | 299 | 7 | 100% | 100% | 97% | 100% | 100% | 213/512 |
| gyakori | éneklőmester | H5329 | 1 | 56 | 0 | 100% | 100% | 100% | 100% | 100% | 0/56 |
| gyakori | igaz | H6662 | 34 | 212 | 10 | 70% | 70% | 99% | 70% | 99% | 171/319 |
| ritka | foglal | H3423 | 24 | 8 | 0 | 62% | 62% | 100% | 62% | 100% | 33/38 |
| ritka | támaszt | H6965 | 13 | 15 | 1 | 87% | 87% | 87% | 100% | 100% | 13/26 |
| ritka | hall | H8085 | 62 | 395 | 2 | 71% | 71% | 92% | 71% | 100% | 14/294 |
| ritka | kifeszít | H5186 | 5 | 3 | 0 | 0% | 0% | 100% | 0% | 100% | 0/0 |
| ritka | megerősít | H3559 | 30 | 27 | 1 | 100% | 100% | 78% | 100% | 100% | 84/111 |
| ritka | emészt | H0398 | 23 | 62 | 0 | 100% | 100% | 73% | 100% | 100% | 19/81 |
| ritka | hirdet | H5046 | 38 | 33 | 1 | 91% | 91% | 91% | 91% | 100% | 70/100 |
| ritka | művel | H6213 | 23 | 28 | 1 | 86% | 82% | 32% | 93% | 100% | 13/37 |
| ritka | parancsol | H6680 | 32 | 326 | 3 | 100% | 100% | 86% | 100% | 100% | 31/357 |
| ritka | terjeszt | H6566 | 18 | 4 | 0 | 100% | 100% | 25% | 100% | 100% | 15/19 |

**gyakori** (cél 61808 token, ebből Strong nélküli 35929): (a) hibrid 93.6%, simplemma 82.1%, emMorph 87.8%; (b) hibrid 93.8%; (c) hibrid 98.7% — lemmánkénti átlag: (a) hibrid 88.5%, (c) hibrid 99.1%

**ritka** (cél 901 token, ebből Strong nélküli 9): (a) hibrid 85.6%, simplemma 85.5%, emMorph 85.9%; (b) hibrid 86.0%; (c) hibrid 100.0% — lemmánkénti átlag: (a) hibrid 79.7%, (c) hibrid 100.0%

**összes** (cél 62709 token, ebből Strong nélküli 35938): (a) hibrid 93.4%, simplemma 82.1%, emMorph 87.7%; (b) hibrid 93.7%; (c) hibrid 98.7% — lemmánkénti átlag: (a) hibrid 86.0%, (c) hibrid 99.3%

scope=teljes Károli (token_karoli, oldal=hu, 456879 token, 54600 alak; emMorph-elemzés nélkül 1 alak); 35 lemma a független mintából; pooled célhalmaz (hibrid ∪ simplemma ∪ emMorph) | forras=pardes.db + hibrid.py + simplemma 2.0.0 + emMorph/hfst (mérce) | ts=2026-10-13T07:07Z

### 2.4 M1 a 3. (felhasználó által ellenőrzött) mintán — a K2 viszonyítási száma

*proveniencia: scope=3. minta, 113 alak, mind felhasznalo | forras=meres_harmadik_eredmeny.md (sha256:8c858721fac1d07f53eb255a7a3486adeb1ff6537e75d1aadf9a23edeb0124a7; a repón kívüli előmérés, 2026-10-12/13, szó szerinti átvétel) | ts=2026-10-13T12:09Z*

#### M1 a harmadik mintán (alakonként / előfordulással súlyozva)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid v2 | 80% / 99.1% (90/113) | 100% / 100.0% (25/25) | 80% / 84.4% (28/35) | 50% / 58.3% (10/20) | 67% / 71.4% (8/12) | 92% / 96.6% (12/13) | 88% / 81.8% (7/8) |
| hibrid v1 | 69% / 94.2% (78/113) | 92% / 95.6% (23/25) | 74% / 59.4% (26/35) | 45% / 55.6% (9/20) | 58% / 64.3% (7/12) | 77% / 89.7% (10/13) | 38% / 27.3% (3/8) |
| simplemma | 67% / 88.6% (76/113) | 84% / 89.7% (21/25) | 74% / 59.4% (26/35) | 45% / 55.6% (9/20) | 58% / 64.3% (7/12) | 77% / 89.7% (10/13) | 38% / 27.3% (3/8) |
| emMorph (mérce) | 70% / 96.6% (79/113) | 96% / 97.9% (24/25) | 77% / 81.2% (27/35) | 45% / 44.4% (9/20) | 50% / 50.0% (6/12) | 85% / 86.2% (11/13) | 25% / 18.2% (2/8) |
| hibrid v2 VAGY emMorph | 88% / 99.6% (100/113) | 100% / 100.0% (25/25) | 94% / 96.9% (33/35) | 65% / 77.8% (13/20) | 75% / 78.6% (9/12) | 100% / 100.0% (13/13) | 88% / 81.8% (7/8) |

##### A hibrid v2 hibái (alak → hibrid | helyes; gyakoriság)
magának → mag | maga (4); atyámnak → atyám | atya (4); kevéssé → kevés | kevéssé (2); láttad-é → láttad-é | lát (2); Melkié → melkié | melki (2); eljőtök → eljőtök | eljön (1); hitszegők → hitszegők | hitszegő (1); gyermekszűlőt → gyermekszűlőt | gyermekszülő/gyermekszűlő (1); legelőjök → legel | legelő (1); véghetetlen-é → véghetetlen-é | véghetetlen/végtelen (1); értheti-é → értheti-é | ért/érthet (1); megütközzék → megütközzék | megütközik (1); hívhatja-é → hívhatja-é | hív/hívhat (1); elérheted-é → elérheted-é | elérhet/ér (1); megkiván → megki | megkíván (1); határozod-é → határozod-é | határoz (1); igéjéért → igéje | ige (1); házadhoz → háza | ház (1); meggyarapodnak → meggyarapodnak | meggyarapodik (1); barátaiért → barátai | barát (1); kerekségének → kereksége | kerekség (1); elhivésére → elhisz | elhivés (1); feloldja → feloldja | felold (1)

scope=harmadik minta, 113 alak (Jer, Jób, Luk, Jak), mind felhasználó által ellenőrzött, sha256:c805d55133f4 | forras=szoto_harmadik_minta.tsv + hibrid.py (sha256:7ee1b6050740) + hibrid_v1.py + karoli_lexikon.tsv (sha256:75ad61617a88) + simplemma 2.0.0 + emMorph/hfst (mérce) | ts=2026-10-13T08:16Z

## 3. A szabályellenőrzés összefoglalója

*proveniencia: scope=hibrid.py (v2) HELYESIRAS (9) + TOVALTO (42) szabályai, teljes Károli ÓSZ (token_karoli, 456 879 token) | forras=szabaly_ellenorzes.md (sha256:cb6e2f5088f3680d3238bfeda2b999d558bc3eb48ae91459aa9dd1f4c946c482; a repón kívüli előmérés, 2026-10-12/13, szó szerinti átvétel) | ts=2026-10-13T12:09Z*

Módszer: a szabály régi alakjának tokenjei hordozzák-e az új alak fő Strong-ját (Strong-támasz), és a régi/új alak könyv-eloszlása. 51 szabály: **alátámasztva 34, gyenge 12, ellentmond 3, nincs adat 2** (a teljes tábla a #94 .1-ben a repó saját eszközéből áll elő: `adat/szoto/szabaly_ellenorzes.tsv`).

- **gyenge (12):** űl$ → ül; ur- → úr; level- → levél; bokr- → bokor; erej- → erő; köv- → kő; füv- → fű; tehen- → tehén; kebl- → kebel; terh- → teher; dolg- → dolog; értelm- → értelem.
- **ellentmond (3):** ^kiván → kíván (20%); falv- → falu (29%); félelm- → félelem (25%).
- **nincs adat (2):** sűly → süly; fark- → farok.
- Az előmérés értelmezése (manual): a gyenge/ellentmondó esetek a fordítási szinonímiából fakadnak (több héber szó egy magyarra); egyik sem mutat hibás szabályt.
- **cz → c:** a táblában „alátámasztva” (97%, 30/31), de a 759 cz-alakból csak 5-nek van c-s párja a Károliban, így a korpusz a szabályt érdemben nem tudja igazolni (a brief .2 pontja ezt külön kiemeli; a `szabaly_forras` jelölése a .2-ben dől el).

## 4. Az előmérés eszközei és a K2 viszonyítási alapja

*proveniencia: scope=hibrid.py (v2) + karoli_lexikon.tsv | forras=hibrid.py (sha256:7ee1b6050740522c60c12ecf9d0f54035cb57af41b08c78c5c01677bf2371ae5), karoli_lexikon.tsv (sha256:75ad61617a88a1315960264df686d8f6c3e834738ac12237973f604580efeaec; a pardes.db `vers.karoli_szoveg`-éből) | ts=2026-10-13T12:09Z*

A 2.4 mérése ugyanezzel a két fájllal futott (a sha256-ok első 12 jegye a 2.4 proveniencia-sorában egyezik). A #94 .1 a lexikont a `konkordancia/Karoli_1908.tsv`-ből építi újra (DT28); a K2 próbája, hogy az átvett v2 a három mintán ugyanazt az M1-számot adja.

## 5. Eltérés-lista: az 1. és 2. minta a DT130 végleges pontjaihoz mérve (F94.0/3) ⛔

*Gépi összevetés (`eszkozok/szoto/elteres_dt130.py`), **javítás nélkül**. A „javaslat” oszlop modell-állítás (manual). A felhasználó dönt soronként vagy csoportosan; a javítás csak utána, `ellenorzes=felhasznalo` jelöléssel (F94_SZOTOVEZES_BRIEF.md .0/3).*

| csoport | eltérő sor | ebből `felhasznalo` |
|---|---|---|
| E-1. DT130 (6)–(7): a van rendhagyó alakjai / a lesz külön szótári alak | 0 | 0 |
| E-2. DT130 (8): Seregek / sereg | 1 | 0 |
| E-3. DT130 (9): kevéssé | 0 | 0 |
| E-4. DT130 (10): C) képzett igealak (szenvedő, -hat/-het) alapigével | 2 | 0 |
| E-5. Kérdéses (nem DT130-pont): műveltető igealak alapige nélkül | 1 | 0 |
| E-6. DT130 (11): kétértelmű alak, kettős elfogadás | 2 | 1 |
| E-7. DT130 (4): igekötős ige alapige nélkül | 16 | 1 |
| E-8. Konvenció: az 1. minta alapige-oszlopa nem igén és igekötő nélküli igén is ki van töltve | 190 | 0 |

#### E-1. DT130 (6)–(7): a van rendhagyó alakjai / a lesz külön szótári alak

Nincs eltérő sor (az 1. és 2. mintában ilyen alak nem fordul elő, vagy a pont szerint áll).

#### E-2. DT130 (8): Seregek / sereg

| minta | alak | gyak. | szotari_alak / mai | alapige | tovabbi | ellenorzes | javaslat (modell, manual) |
|---|---|---|---|---|---|---|---|
| 2 | seregeknek | 5 | sereg / sereg | — | — | modell_ellenorizetlen | a pont betűje szerint rendben; de a példavers (Ézs 44:6) kisbetűs Istenre vonatkozó cím („a seregeknek Ura”), l. alább: a felhasználó dönt (sereg, vagy Seregek / tovabbi_elfogadhato) |

Környezet a `Karoli_1908.tsv`-ben (a teljes Károli): nagybetűs *Seregek…* 223 token (ebből a pontos *Seregek* alak 119, ez a DT130 (8) „119”-e; a többi *Seregeknek*), ebből Ur-/Isten- előtt 223; kisbetűs *seregek…* 85 token, ebből Ur-/Isten- előtt 64. A DT130 (8) a kisbetűs alakot a *sereg* alá veszi; ha a kisbetűs alak Ur-/Isten- előtt áll (Istenre vonatkozó cím kisbetűvel), az a pont hatókörén kívüli kérdés, a felhasználó dönt.

#### E-3. DT130 (9): kevéssé

Nincs eltérő sor (az 1. és 2. mintában ilyen alak nem fordul elő, vagy a pont szerint áll).

#### E-4. DT130 (10): C) képzett igealak (szenvedő, -hat/-het) alapigével

| minta | alak | gyak. | szotari_alak / mai | alapige | tovabbi | ellenorzes | javaslat (modell, manual) |
|---|---|---|---|---|---|---|---|
| 1 | születének | 3 | születik / születik | születik | — | modell_ellenorizetlen | gépi jelölt (-etik/-atik): ha szenvedő képzés, alapige kitöltendő; ha önálló -ik-es ige (pl. születik), változatlan — a felhasználó dönt |
| 2 | vettetének | 1 | vettetik / vettetik | — | — | modell_ellenorizetlen | alapige kitöltendő (az igekötő és a képző nélküli ige) |

#### E-5. Kérdéses (nem DT130-pont): műveltető igealak alapige nélkül

| minta | alak | gyak. | szotari_alak / mai | alapige | tovabbi | ellenorzes | javaslat (modell, manual) |
|---|---|---|---|---|---|---|---|
| 1 | helyezteté | 5 | helyeztet / helyeztet | helyeztet | — | modell_ellenorizetlen | műveltető (-tat/-tet): a DT130 (10) nem nevezi meg; a felhasználó dönt, kap-e alapigét |

#### E-6. DT130 (11): kétértelmű alak, kettős elfogadás

| minta | alak | gyak. | szotari_alak / mai | alapige | tovabbi | ellenorzes | javaslat (modell, manual) |
|---|---|---|---|---|---|---|---|
| 1 | az | 661 | az / az | az | — | modell_ellenorizetlen | a két olvasat (névelő / mutató névmás) szótári alakja azonos: változatlan |
| 1 | ki | 45 | ki / ki | ki | — | modell_ellenorizetlen | tovabbi_elfogadhato: aki (a vonatkozó névmás mai alakja; az igekötői olvasat: ki) |
| 2 | elvesznek | 4 | elvész / elvész | — | — | felhasznalo | elvesz / elvész: a forma szövegkörnyezet nélkül kétértelmű; a felhasználó a sort elvész-ként zárta |

#### E-7. DT130 (4): igekötős ige alapige nélkül

| minta | alak | gyak. | szotari_alak / mai | alapige | tovabbi | ellenorzes | javaslat (modell, manual) |
|---|---|---|---|---|---|---|---|
| 2 | kiterjeszté | 2 | kiterjeszt / kiterjeszt | — | — | modell_ellenorizetlen | alapige: terjeszt |
| 2 | megváltá | 2 | megvált / megvált | — | — | modell_ellenorizetlen | alapige: vált |
| 2 | megvígasztalá | 2 | megvígasztal / megvígasztal | — | — | modell_ellenorizetlen | alapige: vígasztal |
| 2 | kifeszíté | 1 | kifeszít / kifeszít | — | — | modell_ellenorizetlen | alapige: feszít |
| 2 | megerősíté | 1 | megerősít / megerősít | — | — | modell_ellenorizetlen | alapige: erősít |
| 2 | megalapítá | 1 | megalapít / megalapít | — | — | modell_ellenorizetlen | alapige: alapít |
| 2 | elszéleszté | 1 | elszéleszt / elszéleszt | — | — | modell_ellenorizetlen | alapige: széleszt |
| 2 | megrémülének | 1 | megrémül / megrémül | — | — | modell_ellenorizetlen | alapige: rémül |
| 2 | elhamvadának | 1 | elhamvad / elhamvad | — | — | modell_ellenorizetlen | alapige: hamvad |
| 2 | bekövetkezének | 1 | bekövetkezik / bekövetkezik | — | — | modell_ellenorizetlen | alapige: következik |
| 2 | meglennének | 1 | meglesz / meglesz | — | — | modell_ellenorizetlen | alapige: lesz |
| 2 | elhagynának | 1 | elhagy / elhagy | — | — | modell_ellenorizetlen | alapige: hagy |
| 2 | megszégyenülnek | 5 | megszégyenül / megszégyenül | — | — | modell_ellenorizetlen | alapige: szégyenül |
| 2 | elvesznek | 4 | elvész / elvész | — | — | felhasznalo | alapige: vész |
| 2 | leborulnak | 4 | leborul / leborul | — | — | modell_ellenorizetlen | alapige: borul |
| 2 | megértsék | 1 | megért / megért | — | — | modell_ellenorizetlen | alapige: ért |

#### E-8. Konvenció: az 1. minta alapige-oszlopa

Az 1. minta a forrásban minden sorban kitölti az `alapige`-t: nem igei sorban a mai szótári alakkal (160 sor, pl. a, és, az, ő, pedig), igekötő nélküli igénél a szótári alakkal (30 sor, pl. nemzé, nevezé, valának, látá, mondának). A 3. minta (felhasználó által ellenőrzött) az `alapige`-t csak ott tölti, ahol eltér a szótári alaktól (igekötős vagy képzett ige); a 2. mintának nincs `alapige` oszlopa (mind a 180 sor üres). Javaslat (modell): a 3. minta konvenciója, vagyis az 1. minta azonos értékű `alapige`-mezőinek ürítése. A mérést nem érinti (az M1 a szótári alakot, a mai alakot és a tovabbi_elfogadhato-t veti össze).

scope=adat/szoto/szoto_minta_1_fejlesztes.tsv (sha256:294771857de4) + szoto_minta_2_fejlesztes.tsv (sha256:489a3043ae01), DT130 (4), (6)–(11) | forras=eszkozok/szoto/elteres_dt130.py + konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) | ts=2026-10-13T12:08Z

### 5.1 Döntés és javítás (DT-F94a, DT-F94b; F94.0f)

*proveniencia: scope=adat/szoto/szoto_minta_1_fejlesztes.tsv + szoto_minta_2_fejlesztes.tsv | forras=manual (a felhasználó döntése, chat, 2026-10-13; alkalmazás: eszkozok/szoto/minta_javit_f94a.py, idempotens, a nem érintett mezők változatlanok) | ts=2026-10-13*

- **E-4:** *vettetének* — alapige *vet*. *születének* — változatlan (önálló ige).
- **E-5 (alakonként, általános szabály nélkül):** *helyezteté* — szótári alak *helyeztet*, mai alak *helyez*, alapige *helyez* (nem műveltető, H5414 Qal). *tudatá* — *tudat* / *tudat*, alapige *tud* (valódi műveltető, H8085 Hif’íl).
- **E-6:** *ki* — tovabbi_elfogadhato *aki*; az indoklásban a három olvasat (igekötő: 1Móz 2:5 „hajtott ki”; kérdő névmás: Ézs 41:26 „Ki jelenté meg”; vonatkozó névmás: 1Móz 2:5 „ki a földet művelje”). *elvesznek* — tovabbi_elfogadhato *elvesz*, a sor *elvész* marad (Ézs 41:11, H0006).
- **E-7:** a 16 igekötős ige alapigéje a fenti javaslat-oszlop szerint; az `ellenorzes` nem változott (a felhasználó egyenként nem nézte át).
- **E-8:** az 1. minta azonos értékű alapigéi kiürültek (189 mező; a 190. a *helyezteté*, amely az E-5 szerint *helyez* lett); formai igazítás, az `ellenorzes` nem változott.
- **E-2 / DT-F94b:** *seregeknek* — szótári alak *sereg*, tovabbi_elfogadhato *Seregek*.
- **`ellenorzes=felhasznalo` lett:** *vettetének, születének, helyezteté, tudatá, ki, elvesznek* (már az volt), *seregeknek*. Az 1. mintában most 3, a 2. mintában 9 `felhasznalo` sor.
- **Megfigyelések (manual, nem adat):** a felhasználó a Bible Discovery moduljaiból hozott összevetést; a szövegük és Strong-rétegük nem kerül adatba (DT124). Ézs 44:6 „a seregeknek … Ura”: a *seregek* köznév, az Istenre vonatkozó cím a szókapcsolat. Zsolt 13:2 *orcádat*: a *cz → c* helyesírás egy modern megfelelője (nem korpusz-támasz).

## 6. A minták Strong-oszlopa (F94.1)

### 6.1 Eltérés-lista az újraszámítás előtt

*A régi `strong` érték a `pardes.db` `token_karoli`-jából jött (a 2026-10-12-i állapot); az új a repó Károli–Strong párosításából (SEMA 2.20, modell-kimenet, javaslat, nem ellenőrizve). Példa a régi hibára: az 1. minta *ki* sora (1Móz 2:5) H0834-et adott, de a `TAHOT_kivonat.tsv` szerint a versben nincs H0834 (a vers vonatkozó *ki*-je a párosításban betoldás).*

Az 1–2. minta 393 sorából **83** sor `strong` mezője tér el a repó párosításától (ebből 4 a párosításban betoldás vagy nincs ilyen token: üres lesz); a példaversben nem található alak: 0.

| minta | alak | példa | régi (token_karoli) | új (karoli_strong) | a vers azonos alakú tokenjei (sorszám, állapot, Strong, bizonyosság) |
|---|---|---|---|---|---|
| 1 | vala | 1Móz 1:2 | — | H1961 | #7 parositva H1961 (magas); #10 betoldas — (magas); #19 betoldas — (magas) |
| 1 | én | 1Móz 4:9 | H9020 | H0595 | #21 parositva H0595 (magas); #23 parositva H9020 (magas) |
| 1 | hogy | 1Móz 1:4 | H9005 | H3588 | #4 parositva H3588 (magas) |
| 1 | is | 1Móz 1:22 | H1571 | H9002 | #17 parositva H9002 (magas) |
| 1 | meg | 1Móz 1:9 | H8085 | H7200 | #15 parositva H7200 (magas) |
| 1 | néki | 1Móz 1:11 | H9005+H9033 | H9033 | #23 parositva H9033 (alacsony) |
| 1 | azt | 1Móz 2:3 | — | H9033 | #9 parositva H9033 (magas) |
| 1 | ki | 1Móz 2:5 | H0834 | H6779 | #16 parositva H6779 (magas); #32 betoldas — (alacsony) |
| 1 | mely | 1Móz 1:6 | H0834 | — | #10 betoldas — (alacsony) |
| 1 | el | 1Móz 3:13 | H1980 | H5377 | #17 parositva H5377 (magas) |
| 1 | egy | 1Móz 1:9 | — | H0259 | #11 parositva H0259 (magas) |
| 1 | s | 1Móz 2:5 | H9001 | H9002 | #9 parositva H9002 (magas) |
| 1 | annak | 1Móz 2:12 | H9023 | H1931 | #2 parositva H1931 (magas) |
| 1 | között | 1Móz 1:6 | H0996 | H9003+H8432 | #8 parositva H9003+H8432 (magas) |
| 1 | való | 1Móz 1:7 | — | H0834 | #11 parositva H0834 (alacsony); #16 parositva H0834 (alacsony) |
| 1 | esztendős | 1Móz 5:32 | H8141 | H1121+H8141 | #5 parositva H1121+H8141 (magas) |
| 1 | vele | 1Móz 3:6 | H0854+H9033 | H5973+H9034 | #31 parositva H5973+H9034 (magas) |
| 1 | földnek | 1Móz 1:10 | H0776 | H9005+H0776 | #6 parositva H9005+H0776 (alacsony) |
| 1 | sem | 1Móz 2:5 | H3808 | H2962 | #5 parositva H2962 (alacsony); #14 parositva H2962 (alacsony); #30 parositva H0369 (magas) |
| 1 | be | 1Móz 1:22 | H0935 | H4390 | #11 parositva H4390 (magas) |
| 1 | előtt | 1Móz 4:7 | H9005 | H9005+H6607 | #17 parositva H9005+H6607 (magas) |
| 1 | legyen | 1Móz 1:11 | H1961 | — | #22 betoldas — (magas) |
| 1 | valának | 1Móz 4:8 | — | H1961+H9048 | #16 parositva H1961+H9048 (magas) |
| 1 | szűlé | 1Móz 4:2 | H3205 | H9005+H3205 | #3 parositva H9005+H3205 (magas) |
| 1 | elmenének | 1Móz 8:3 | H1980 | H7725 | #2 parositva H7725 (magas) |
| 1 | vevének | 1Móz 6:2 | H1396 | H3947 | #13 parositva H3947 (magas) |
| 1 | Monda | 1Móz 4:10 | H9001+H0559 | H0559 | #1 parositva H0559 (magas) |
| 1 | őnéki | 1Móz 7:16 | H9005+H9033 | H0853+H9033 | #17 parositva H0853+H9033 (alacsony) |
| 1 | földön | 1Móz 1:11 | H9003+H0776 | H5921+H0776 | #26 parositva H5921+H0776 (magas) |
| 1 | földről | 1Móz 2:6 | H9006+H5921+H0776 | H4480+H0776 | #7 parositva H4480+H0776 (magas) |
| 1 | fiainak | 1Móz 7:7 | H1121 | H1121+H9023 | #12 parositva H1121+H9023 (magas) |
| 1 | életének | 1Móz 5:5 | H3117 | H0834+H2421 | #5 parositva H0834+H2421 (magas) |
| 1 | feleségének | 1Móz 3:21 | H0802 | H9005+H0802+H9023 | #10 parositva H9005+H0802+H9023 (alacsony) |
| 1 | állatokat | 1Móz 1:21 | H7431 | H8577 | #7 parositva H8577 (magas); #13 parositva H5315+H2416 (magas) |
| 1 | embernek | 1Móz 2:16 | H9005+H0121 | H5921+H0120 | #7 parositva H5921+H0120 (magas) |
| 1 | helyre | 1Móz 1:9 | H9009+H4725 | H0413+H4725 | #12 parositva H0413+H4725 (magas) |
| 1 | égből | 1Móz 8:2 | H4480+H8064 | H4480+H9009+H8064 | #15 parositva H4480+H9009+H8064 (alacsony) |
| 1 | égnek | 1Móz 1:8 | H8064 | H9005+H8064 | #6 parositva H9005+H8064 (alacsony) |
| 1 | képére | 1Móz 1:27 | H9003+H6754 | H9003+H6754+H9023 | #9 parositva H9003+H6754+H9023 (magas); #11 parositva H9003+H6754 (magas) |
| 1 | nevet | 1Móz 2:19 | H8034 | H7121 | #28 parositva H7121 (alacsony) |
| 1 | keletre | 1Móz 4:16 | H9006+H6924 | H6926 | #13 parositva H6926 (magas) |
| 1 | népet | 1Móz 14:16 | H1471 | H5971 | #19 parositva H5971 (magas) |
| 1 | atyjafiának | 1Móz 4:21 | H0251 | H0251+H9023 | #3 parositva H0251+H9023 (magas) |
| 1 | melyben | 1Móz 1:11 | H0834+H9003+H9033 | H0834+H9003 | #21 parositva H0834+H9003 (alacsony) |
| 1 | melynek | 1Móz 1:12 | — | H0834 | #17 parositva H0834 (alacsony) |
| 1 | kinek | 1Móz 9:5 | H9002 | — | #20 betoldas — (alacsony); #21 parositva H0376 (magas) |
| 1 | nincsen | 1Móz 13:9 | H0369 | H3808 | #2 parositva H3808 (magas) |
| 1 | Úrnak | 1Móz 4:3 | H3068 | H9005+H3068 | #10 parositva H9005+H3068 (magas) |
| 1 | Ábrahámnak | 1Móz 17:9 | H9005+H0085 | H0413+H0085 | #4 parositva H0413+H0085 (magas) |
| 1 | Ábrámnak | 1Móz 11:31 | H0413+H0087 | H0087 | #20 parositva H0087 (magas) |
| 1 | Izsáknak | 1Móz 17:19 | H9005+H3327 | H3327 | #17 parositva H3327 (magas) |
| 1 | Ádám | 1Móz 3:20 | H0121 | H0120 | #4 parositva H0120 (magas) |
| 2 | vagyok | Ézs 41:4 | — | H1931 | #23 parositva H1931 (alacsony) |
| 2 | fel | Ézs 40:9 | H5375 | H5927 | #4 parositva H5927 (alacsony) |
| 2 | téged | Ézs 41:12 | H9031 | H9021 | #14 parositva H9021 (alacsony) |
| 2 | nékem | Ézs 41:28 | H9005+H9030 | — | #17 betoldas — (alacsony) |
| 2 | Ímé | Ézs 40:10 | H2005 | H2009 | #1 parositva H2009 (alacsony); #10 parositva H2009 (alacsony) |
| 2 | Istenem | Ézs 40:27 | H0430+H9020 | H9006+H0430+H9020 | #18 parositva H9006+H0430+H9020 (alacsony) |
| 2 | föl | Ézs 40:9 | H5782 | H7311 | #8 parositva H7311 (alacsony); #14 parositva H7311 (alacsony) |
| 2 | lesz | Ézs 43:10 | — | H1961 | #33 parositva H1961 (alacsony) |
| 2 | zsoltára | Zsolt 3:1 | H4210 | H4210+H9005 | #2 parositva H4210+H9005 (alacsony) |
| 2 | lelkemet | Ézs 42:1 | H5315+H9020 | H7307+H9020 | #15 parositva H7307+H9020 (alacsony) |
| 2 | nagy | Ézs 40:26 | H7227 | H7230 | #22 parositva H7230 (alacsony) |
| 2 | Úrban | Ézs 40:31 | H9003+H3068 | H3068 | #5 parositva H3068 (alacsony) |
| 2 | igaz | Ézs 44:2 | H6662 | H3484 | #21 parositva H3484 (alacsony) |
| 2 | tőlem | Ézs 43:27 | H4480+H9030 | H9003+H9030 | #8 parositva H9003+H9030 (alacsony) |
| 2 | vannak | Ézs 41:27 | — | H9048 | #7 parositva H9048 (alacsony) |
| 2 | szívében | Ézs 47:8 | H9003+H3820+H9023 | H9003+H3824+H9024 | #15 parositva H9003+H3824+H9024 (alacsony) |
| 2 | ezeket | Ézs 42:16 | H0428 | H0428+H1697 | #28 parositva H0428+H1697 (alacsony) |
| 2 | népeknek | Ézs 42:1 | H3816 | H9005+H1471 | #22 parositva H9005+H1471 (alacsony) |
| 2 | kiket | Ézs 46:3 | — | H9009 | #11 parositva H9009 (alacsony) |
| 2 | időben | Ézs 51:9 | H9003+H6256 | H3117 | #17 parositva H3117 (alacsony) |
| 2 | gyülekezetben | Zsolt 22:23 | H9003+H6951 | H9003+H8432+H6951 | #9 parositva H9003+H8432+H6951 (alacsony) |
| 2 | igazságban | Ézs 41:2 | H9003+H6664 | H6664 | #8 parositva H6664 (alacsony) |
| 2 | titeket | Ézs 41:24 | H9036 | H9003+H9036 | #15 parositva H9003+H9036 (alacsony) |
| 2 | igaznak | Ézs 43:26 | H6662 | H6663 | #9 parositva H6663 (alacsony) |
| 2 | sötétséget | Ézs 42:16 | H2822 | H4285 | #20 parositva H4285 (alacsony) |
| 2 | házában | Ézs 44:13 | H9003+H1004 | H1004 | #23 parositva H1004 (alacsony) |
| 2 | bíznak | Ézs 40:31 | H2620 | H6960 | #6 parositva H6960 (alacsony) |
| 2 | szólnak | Ézs 45:24 | H1696 | H0559 | #6 parositva H0559 (alacsony) |
| 2 | örüljenek | Zsolt 13:5 | H8055 | H1523 | #9 parositva H1523 (alacsony) |
| 2 | szeret | Ézs 41:24 | H0157 | H0977 | #16 parositva H0977 (alacsony) |
| 2 | Dávid | Ézs 55:3 | H9005+H1732 | H1732 | #16 parositva H1732 (alacsony) |

scope=adat/szoto/szoto_minta_1_fejlesztes.tsv + szoto_minta_2_fejlesztes.tsv, a pelda_igehely verse | forras=eszkozok/szoto/minta_strong.py + szavak_1Moz.tsv sha256:e62bba953842, szavak_Zsolt.tsv sha256:3eb9085ae600, szavak_Ezs.tsv sha256:d77853e2f34d (modell-kimenet, javaslat) | ts=2026-10-13T12:26Z

### 6.2 Átírva

A `minta_strong.py --ir` a 83 eltérő `strong` mezőt átírta (más mező nem változott; a fájlok fejlécében `# strong:` proveniencia-sor). Utána a lista 0 eltérést ad.


## 7. Megfigyelések (F94.1; manual, javítás nélkül)

### 7.1 A hátravetett igekötő (N-F94d)

A tövezés alakonként megy: a *vettettek el*, *ragadja el*, *jelenté … meg*, *hajtott ki*, *felejtkezel el*, *rejted el* igéje igekötő nélküli alakként kap szótári alakot, ezért az igekötős szótári alakra (*elvet*, *elragad*, *megjelent*, *kihajt*) keresve ezek nem jönnek elő, az alapigére igen. Gyakoriság a teljes Károliban (`eszkozok/szoto/hatravetett_igekoto.py`, heurisztika):

| igekötő | alsó becslés (utána írásjel / versvég) | felső becslés (minden külön álló token) | példa |
|---|---|---|---|
| meg | 1022 | 4869 | 1Móz 3:4 „haltok meg” |
| el | 573 | 2317 | 1Móz 12:19 „menj el” |
| fel | 221 | 937 | 1Móz 13:17 „Kelj fel” |
| ki | 193 | 4033 | 1Móz 2:5 „hajtott ki” |
| hozzá | 131 | 355 | 1Móz 15:4 „ő hozzá” |
| be | 113 | 600 | 1Móz 7:2 „vígy be” |
| alá | 103 | 218 | 1Móz 1:28 „birodalmatok alá” |
| reá | 90 | 237 | 1Móz 15:12 „ő reá” |
| vissza | 74 | 259 | 1Móz 8:12 „hozzá vissza” |
| le | 71 | 336 | 1Móz 44:26 „mehetünk le” |
| át | 51 | 224 | 1Móz 48:17 „tegye át” |
| oda | 47 | 320 | 1Móz 19:20 „kérlek oda” |
| elő | 44 | 123 | 1Móz 43:9 „kérd elő” |
| föl | 36 | 91 | Bír 5:2 „kele föl” |
| utána | 35 | 112 | 1Móz 22:1 „ezeknek utána” |
| rá | 22 | 66 | 5Móz 25:3 „üttessen rá” |
| össze | 20 | 100 | 1Móz 3:7 „azért össze” |
| szét | 8 | 23 | 4Móz 1:51 „azt szét” |
| széjjel | 1 | 1 | 4Móz 16:37 „hintsd széjjel” |
| végig | 1 | 16 | 5Móz 31:30 „mind végig” |
| **összesen** | **2856** | **15237** | |

scope=OT+NT-full (31158 Károli-vers) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + eszkozok/szoto/hatravetett_igekoto.py (heurisztika, manual megfigyelés) | ts=2026-10-13T12:28Z

Olvasat (manual): az „alsó becslés” a *meg, el, fel, föl, ki, be, le, át, elő, vissza, rá* igekötőknél valóban hátravetett igekötő (összesen 2 420 token); a *hozzá, alá, reá, oda, utána, össze, szét, végig* sorában névutó- és határozószói használat is van („ő hozzá”, „birodalmatok alá”, „ezeknek utána”), ezért ott nem alsó becslés. A felső becslés a *ki* névmást és a *meg* kötőszót is tartalmazza. Nyitott tétel: N-F94d (`NYITOTT_FELADATOK.md`); a brief N-F94a-ja (különálló igekötő) ennek az előre vetett párja.

### 7.2 Ézs 41:11 — a Strong-párosítás

*proveniencia: scope=range:Ézs 41:11 | forras=konkordancia/TAHOT_kivonat.tsv + adat/karoli_strong/szavak_Ezs.tsv | ts=2026-10-13*

A `TAHOT_kivonat.tsv` sorai szerint a vers 2. héber tokenje H0954 (*jēbōšū*, „szégyenben maradnak”), a 15. H0006 (*jōbdū*, „elvesznek”). A repó párosítása: *megszégyenülnek* → H0954, *elvesznek* → H0006 (mindkettő `alacsony` bizonyosságú javaslat); a 2. minta két sora ugyanezt hordozza. A felhasználó által behozott Bible Discovery-összevetésben a párosítás eltolt; a mi H0954-ünk a TAHOT-sorral egyezik. Csak megfigyelés: a Discovery szövege és Strong-rétege adatba nem kerül (DT124).

### 7.3 A *cz → c* szabály forrásjelölése (a .2-ben alkalmazandó)

A felhasználó utasítása (2026-10-13): a *cz → c* szabály `szabaly_forras` értéke `manual` (általános helyesírás-történeti tudás), mellette a korpusz-támasz száma: a 759 cz-alakból 5-nek van c-s párja a Károliban. A Zsolt 13:2 *orczádat* / mai *orcádat* manual megfigyelés, nem korpusz-támasz. A K4 „34 `korpusz_strong`”-ja így 33 `korpusz_strong` + 1 `manual` lesz; ez a .2-ben a szabálytáblában jelenik meg.

## 8. A simplemma adatlicence (F94.1/6) ⛔

*proveniencia: scope=simplemma 2.0.0 | forras=a telepített csomag `simplemma-2.0.0.dist-info/METADATA` („Credits and licenses”) és `licenses/LICENSE`; https://github.com/adbar/simplemma/tree/main/licenses (a mappa fájlnevei); https://github.com/michmech/lemmatization-lists README | ts=2026-10-13*

Szó szerinti idézetek:

- METADATA: „The software is licensed under the MIT license. For information on the licenses of the linguistic information databases, see the `licenses` folder.”
- METADATA: „The surface lookups (non-greedy mode) rely on lemmatization lists derived from the following sources, listed in order of relative importance:” — „Lemmatization lists by Michal Měchura (Open Database License)”; „Wiktionary entries packaged by the Kaikki project”; „FreeLing project”; „spaCy lookups data”; „Unimorph Project”; „Wikinflection corpus by Eleni Metheniti (CC BY 4.0 License)”.
- A forrásrepó `licenses` mappája: `CC_BY_License.txt`, `Open_Database_License.txt`, `Other.txt`, `PL_License.txt`, `TR_Source.txt`; az `Other.txt` szövege: „See 2b.- DATA COMPONENTS in https://github.com/TALP-UPC/FreeLing/blob/master/COPYING”.
- A lemmatization-lists README: a lista tartalmazza a `lemmatization-hu.txt`-t („Hungarian (hu) (39,898 pairs)”); licence: „Available under the Open Database License”.

Következtetés (manual, nem jogi vélemény): a simplemma **kódja** MIT, a **magyar adata** (legalább részben) az ODbL alatti lemmatization-lists-ből származik, a többi forrás licence nyelvenként nem azonosított (CC BY, FreeLing-adat, Wiktionary/Kaikki). Az ODbL share-alike adatbázis-licenc: a belőle származtatott adatbázis (pl. a `karoli_szotari_alak.tsv` simplemma-módszerű sorai) ODbL alá kerülhet, és forrásmegjelölést kíván. Ez **nem MIT-kompatibilis** a nyilvános kiadással a brief értelmében → megállás, a felhasználó dönt (DT-F94c). A `licencek.tsv` sora a döntés után kerül be.


## 9. A simplemma szerepének mérése: A / B / C (F94.1, DT-F94c részleges döntés)

*A felhasználó döntése (2026-10-13): a WSL-es Python 3.11 a helyben telepített simplemma 2.0.0 csomagkönyvtárat PYTHONPATH-on kapja (csak a `simplemma` csomag egy ideiglenes könyvtárban, a repón kívül; új letöltés nincs); M1 mindhárom mintán, három változattal; a mérés után megállás. A DT-F94c 🟡 marad.*

**Futtatókörnyezet:** WSL (Ubuntu), Python 3.11.17 (a repón kívüli uv-venv), simplemma 2.0.0 (a magyar adatfájl `hu.plzma` sha256-ja a proveniencia-sorokban). A repó eszközei (`eszkozok/szoto/hibrid.py`, `lexikon_epit.py`, `meres.py`) így Python 3.11 alatt is futnak.

**Változatok** (`hibrid.valtozat()`; a pontos szöveg a `hibrid.py` docstringjében):
- **A** — az előmérés v2-je: a simplemma tartalék-lemmatizáló és igető-igazoló is.
- **B** — simplemma nélkül: a lemmatizáló az alakot adja vissza, a `simplemma.is_known` mindig hamis, és a régies igevégződés-réteg jelöltjét semmi nem igazolja (a réteg nem vág).
- **C** — simplemma nélkül, tartalék-lemmatizáló nélkül, de az igető-igazolást a Károli-lexikon (`adat/szoto/karoli_lexikon.tsv`, a közkincs Károli 1908-ból, DT-F33e) végzi. **Az elfogadás feltétele (rögzítve):** a régies végződés levágása után kapott c jelölt tő elfogadott, ha (1) c önálló kisbetűs alakként előfordul a Károliban (E/3 jelen: *teremt*, *lát*); vagy (2) c+*ik* előfordul, és c nem -tat/-tet/-ít/-szt végű (*születik*); vagy (3) c valamely igei ragos alakja előfordul (az A-val azonos lista: -ni, -ani, -eni, -ott, -ett, -ött, -tt, -ván, -vén, -nak, -nek, -tek, -tok, -tök). Az igekötő-leválasztás ugyanaz, mint az A-ban. A névszói ágban a C-ben sincs simplemma-próba (a `is_known` hamis), mert a lexikonbeli előfordulás nem jelenti, hogy az alak szótári alak (a *földön* is előfordul).

### 9.1 Az átvétel próbája (K2)

- **Korpusz-lexikon:** a `lexikon_epit.py` a `konkordancia/Karoli_1908.tsv`-ből épít; az adatrésze (a `#`-sor és a fejléc nélkül) **bájtra azonos** az előmérés `karoli_lexikon.tsv`-jével (66 824 alak; `cmp`).
- **Viselkedés:** az előmérés `hibrid.py`-ja és a repó `hibrid.py`-jának A változata a lexikon mind a 61 673 alakján (a kisbetűs és a mondat belsejében nagybetűs alakok) azonos kimenetet ad: `Python 3.11.17; alak: 61673; eltérő kimenet: 0 []`. *(Átvételi hiba, javítva a mérés előtt: az új betöltő először az `alak\t` előtagú sorokat fejlécként hagyta ki, és ezzel a Károli valódi „alak” szavát is; most csak a pontos fejlécsort.)*
- **M1, A változat** (az 1–2. mintán a DT-F94a/b előtti állapot, a `c9332ca8` commitból; a 3. minta változatlan):

| minta | előmérés | most (A) |
|---|---|---|
| 1. (súlyozva) | 99,2% | 95% / 99.2% (203/213) |
| 2. (súlyozva) | 97,6% | 92% / 97.6% (166/180) |
| 3. (alakonként / súlyozva) | 80% / 99,1% (90/113) | 80% / 99.1% (90/113) |

A K2 teljesül: mindhárom szám bitre az előmérésé.

*scope=elotte_szoto_minta_1_fejlesztes.tsv (sha256:294771857de4) | forras=eszkozok/szoto/meres.py + hibrid.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:04Z*

### 9.2 M1 a mostani mintákon (a DT-F94a/b után), A / B / C és a simplemma önmagában

##### szoto_minta_1_fejlesztes.tsv (213 alak)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 95% / 99.2% (203/213) | 98% / 99.6% (54/55) | 95% / 96.6% (62/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 71% / 78.9% (5/7) | 100% / 100.0% (27/27) |
| hibrid B | 70% / 90.8% (149/213) | 84% / 93.3% (46/55) | 66% / 71.2% (43/65) | 44% / 56.9% (20/45) | 79% / 88.2% (11/14) | 29% / 42.1% (2/7) | 100% / 100.0% (27/27) |
| hibrid C | 79% / 92.6% (169/213) | 85% / 93.8% (47/55) | 71% / 73.6% (46/65) | 80% / 88.6% (36/45) | 79% / 88.2% (11/14) | 29% / 42.1% (2/7) | 100% / 100.0% (27/27) |
| simplemma | 70% / 84.6% (149/213) | 80% / 87.2% (44/55) | 60% / 64.0% (39/65) | 60% / 58.9% (27/45) | 79% / 75.0% (11/14) | 86% / 89.5% (6/7) | 81% / 90.3% (22/27) |

*A hibrid A hibái (alak → kimenet | helyes; gyakoriság):* minekutánna → minekutána | minekutánna/miután (20); Éle → éle | él (9); magodnak → magod | mag (6); földére → földér | föld (5); fájáról → fája | fa (4); elsűlyeszté → elsülyeszt | elsüllyeszt (2); letelepedének → leteleped | letelepedik (2); megnyilatkozának → megnyilatkoz | megnyilatkozik (2); mossátok → moss | mos (2); tekints → tekints | tekint (2)

*A hibrid C hibái (alak → kimenet | helyes; gyakoriság):* minden → mind | minden (80); azt → azt | az (47); mert → mer | mert (43); föld → föl | föld (37); annak → annak | az (29); mint → min | mint (28); mind → min | mind (23); kik → kik | aki/ki (22); esztendeig → esztendeig | esztendő (16); azokat → azok | az (12); feleséget → felesége | feleség (10); Éle → éle | él (9); kinek → kin | aki/ki (8); abban → abba | az (6); azoknak → azok | az (6); magodnak → magod | mag (6); méhében → méhe | méh (6); állatokat → áll | állat (6); felemelé → felemelik | felemel (5); égből → égből | ég (5); atyjának → atyja | atya (4); barmokat → barmok | barom (4); fájáról → fája | fa (4); gyümölcséből → gyümölcse | gyümölcs (4); hetet → hetet | hét (4); házából → háza | ház (4); képére → képe | kép (4); színéről → színe | szín (4); égnek → égnek | ég (4); körűlmetélé → körülmetélé | körülmetél (3); segítségűl → segítségül | segítség (3); szövetségűl → szövetségül | szövetség (3); töltsétek → tölts | tölt (3); elbeszélé → elbeszélik | elbeszél (2); elsűlyeszté → elsülyeszt | elsüllyeszt (2); elvégezé → elvégezik | elvégez (2); esének → esének | esik (2); letelepedének → leteleped | letelepedik (2); látsz → látsz | lát (2); megnyilatkozának → megnyilatkoz | megnyilatkozik (2); megtölté → megtöltik | megtölt (2); mossátok → moss | mos (2); tekints → tekints | tekint (2); világítsanak → világítsanak | világít (2)

scope=szoto_minta_1_fejlesztes.tsv (sha256:a7f8d65d42de) | forras=eszkozok/szoto/meres.py + hibrid.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:04Z

##### szoto_minta_2_fejlesztes.tsv (180 alak)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 92% / 97.6% (166/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 86% / 85.9% (18/21) | 100% / 100.0% (10/10) |
| hibrid B | 68% / 84.1% (123/180) | 90% / 87.6% (36/40) | 73% / 75.3% (47/64) | 25% / 25.6% (8/32) | 77% / 69.2% (10/13) | 57% / 64.1% (12/21) | 100% / 100.0% (10/10) |
| hibrid C | 80% / 85.8% (144/180) | 90% / 87.6% (36/40) | 78% / 76.7% (50/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 57% / 64.1% (12/21) | 100% / 100.0% (10/10) |
| simplemma | 69% / 78.4% (124/180) | 80% / 80.3% (32/40) | 72% / 80.9% (46/64) | 69% / 69.8% (22/32) | 0% / 0.0% (0/13) | 76% / 75.6% (16/21) | 80% / 84.2% (8/10) |

*A hibrid A hibái (alak → kimenet | helyes; gyakoriság):* orczádat → orcádat | arc/orca (7); előre → előre | elő (5); eleitől → elei | eleje/elő (4); elvesznek → elveszik | elvesz/elvész (4); törnek → törik | tör (4); bosszankodjál → bosszankodjál | bosszankodik (3); gyalázatot → gyaláz | gyalázat (3); gyűlölőim → gyűlöl | gyűlölő (3); Mostantól → mostantól | most/mostan (2); alkotójának → alkot | alkotó (1); felebarátjának → felebarátja | felebarát (1); mértéklé → mértéklé | mértékel (1); szigetekké → szigetek | sziget (1); vettetének → vettet | vettetik (1)

*A hibrid C hibái (alak → kimenet | helyes; gyakoriság):* Mert → mer | mert (70); ezt → ezt | ez (41); éneklőmesternek → éneklőmesternek | éneklőmester (19); olyan → oly | olyan (15); bíznak → bíznak | bízik (8); szívében → szíve | szív (8); ezeket → ezek | ez (7); méhétől → méhe | méh (7); orczádat → orcádat | arc/orca (7); kiket → kik | aki/ki (5); eleitől → eleitől | eleje/elő (4); szeret → szer | szeret (4); bosszankodjál → bosszankodjál | bosszankodik (3); cselekedjél → cselekedj | cselekedik/cselekszik (3); emlékezzél → emlékezz | emlékezik/emlékszik (3); fejedelmeket → fejedelmek | fejedelem (3); folyóvizeket → folyóvizek | folyóvíz (3); gyűlölőim → gyűlölői | gyűlölő (3); halmokat → halmok | halom (3); hegyeket → hegyek | hegy (3); házában → háza | ház (3); mennek → mennek | megy (3); jelentsék → jelentsék | jelent (2); mondaná → mondaná | mond (2); alkotójának → alkotója | alkotó (1); barátjának → barátja | barát (1); elhagynának → elhagynának | elhagy (1); elszéleszté → elszéleszté | elszéleszt (1); felebarátjának → felebarátja | felebarát (1); megalapítá → megalapítá | megalapít (1); megértsék → megértsék | megért (1); mértéklé → mértéklé | mértékel (1); szigetekké → szigetek | sziget (1); vegyék → vegyék | vesz (1); vettetének → vettet | vettetik (1); volnék → volnék | van (1)

scope=szoto_minta_2_fejlesztes.tsv (sha256:587e47bded57) | forras=eszkozok/szoto/meres.py + hibrid.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:04Z

##### szoto_minta_3_ellenorzott.tsv (113 alak)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 80% / 99.1% (90/113) | 100% / 100.0% (25/25) | 80% / 84.4% (28/35) | 50% / 58.3% (10/20) | 67% / 71.4% (8/12) | 92% / 96.6% (12/13) | 88% / 81.8% (7/8) |
| hibrid B | 53% / 90.2% (60/113) | 88% / 92.0% (22/25) | 49% / 57.8% (17/35) | 30% / 33.3% (6/20) | 17% / 21.4% (2/12) | 54% / 48.3% (7/13) | 75% / 72.7% (6/8) |
| hibrid C | 56% / 90.3% (63/113) | 88% / 92.0% (22/25) | 51% / 62.5% (18/35) | 40% / 30.6% (8/20) | 17% / 21.4% (2/12) | 54% / 48.3% (7/13) | 75% / 72.7% (6/8) |
| simplemma | 67% / 88.6% (76/113) | 84% / 89.7% (21/25) | 74% / 59.4% (26/35) | 45% / 55.6% (9/20) | 58% / 64.3% (7/12) | 77% / 89.7% (10/13) | 38% / 27.3% (3/8) |

*A hibrid A hibái (alak → kimenet | helyes; gyakoriság):* atyámnak → atyám | atya (4); magának → mag | maga (4); Melkié → melkié | melki (2); kevéssé → kevés | kevéssé (2); láttad-é → láttad-é | lát (2); barátaiért → barátai | barát (1); elhivésére → elhisz | elhivés (1); eljőtök → eljőtök | eljön (1); elérheted-é → elérheted-é | elérhet/ér (1); feloldja → feloldja | felold (1); gyermekszűlőt → gyermekszűlőt | gyermekszülő/gyermekszűlő (1); határozod-é → határozod-é | határoz (1); hitszegők → hitszegők | hitszegő (1); házadhoz → háza | ház (1); hívhatja-é → hívhatja-é | hív/hívhat (1); igéjéért → igéje | ige (1); kerekségének → kereksége | kerekség (1); legelőjök → legel | legelő (1); meggyarapodnak → meggyarapodnak | meggyarapodik (1); megkiván → megki | megkíván (1); megütközzék → megütközzék | megütközik (1); véghetetlen-é → véghetetlen-é | véghetetlen/végtelen (1); értheti-é → értheti-é | ért/érthet (1)

*A hibrid C hibái (alak → kimenet | helyes; gyakoriság):* mit → mit | mi (111); Ezt → ezt | ez (95); azok → azok | az (80); cselekedék → cselekedék | cselekedik/cselekszik (9); hallgattatok → hallgattatok | hallgat (9); atyámnak → atyám | atya (4); magának → mag | maga (4); tanítványoknak → tanítványok | tanítvány (3); Melkié → melkié | melki (2); adának → adá | ad (2); elenyésznek → elenyésznek | elenyészik (2); kevéssé → kevés | kevéssé (2); könnyeivel → könnyeivel | könny (2); láttad-é → láttad-é | lát (2); tudománynyal → tudománnyal | tudomány (2); Mutassa → mutassa | mutat (1); barátaiért → barátai | barát (1); barázdához → barázdához | barázda (1); boldoguljanak → boldoguljanak | boldogul (1); czédrust → cédrust | czédrus/cédrus (1); elhivésére → elhivésére | elhivés (1); eljőtök → eljőtök | eljön (1); elérheted-é → elérheted-é | elérhet/ér (1); feloldja → feloldja | felold (1); felügyelők → felügyelők | felügyelő (1); fillért → fillért | fillér (1); gyermekszűlőt → gyermekszűlőt | gyermekszülő/gyermekszűlő (1); gyűlöletesek → gyűlöletesek | gyűlöletes (1); határozod-é → határozod-é | határoz (1); hitszegők → hitszegők | hitszegő (1); házadhoz → háza | ház (1); hívhatja-é → hívhatja-é | hív/hívhat (1); igéjéért → igéje | ige (1); kerekségének → kereksége | kerekség (1); kiküldök → kiküldök | kiküld (1); követelnek → követelnek | követel (1); lakókat → lakók | lakó (1); megbocsátani → megbocsátani | megbocsát (1); meggyarapodnak → meggyarapodnak | meggyarapodik (1); megkiván → megki | megkíván (1); megütközzék → megütközzék | megütközik (1); mostani → mostan | mostani (1); paréjtól → paréjtól | paréj (1); tömlöczre → tömlöcre | tömlöc/tömlöcz (1); vendégséget → vendégséget | vendégség (1); verettek → verettek | ver/veretik (1); vonszolják → vonszolják | vonszol (1); véghetetlen-é → véghetetlen-é | véghetetlen/végtelen (1); vízieké → vízieké | vízi (1); értheti-é → értheti-é | ért/érthet (1)

scope=szoto_minta_3_ellenorzott.tsv (sha256:bafc1e67a061) | forras=eszkozok/szoto/meres.py + hibrid.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:04Z

### 9.3 Olvasat (manual, nem döntés)

- **A B és a C messze az A alatt van.** A 3. (felhasználó által ellenőrzött) mintán súlyozva A 99,1%, B 90,2%, C 90,3%; alakonként A 80%, B 53%, C 56%. Az 1–2. (fejlesztési) mintán súlyozva A 99,2 / 97,6%, C 92,6 / 85,8%.
- **A C az igető-igazolást nagyrészt pótolja** (régies ige az 1–2. mintán: A 91–94%, B 25–44%, C 78–80% alakonként); a 3. mintán a régies igék rétege kicsi és vegyes (20 alak).
- **A veszteség zöme a névszói ágból jön**, ahol a simplemma szótári-alak próbája védte a már szótári alakot a további vágástól: *mert → mer, minden → mind, föld → föl, mint → min, szeret → szer*, és ahol a tartalék-lemmatizáló a névmást vitte szótári alakra: *azt, ezt, mit, azok, annak* (a 3. mintán a *mit* 111, az *Ezt* 95, az *azok* 80 előfordulás). Ezeket a C a megadott feltétel szerint nem pótolja; pótlásuk (pl. a Károli-lexikon gyakoriságával vagy a kivételtábla bővítésével) új szabály lenne, amelyet nem hangoltam a mérés után.
- A felhasználó által megfogalmazott döntési szabály szerint („ha C/B közel az A-hoz → 2. opció”) a C/B **nincs közel** az A-hoz. A döntés a felhasználóé (DT-F94c).


## 10. A szabályellenőrzés a repó párosításából (F94.1)

A `szabaly_ellenorzes.py` a repóban a `adat/karoli_strong/szavak_*.tsv`-ből számol (57 párosított könyv, ÓSZ + a párosított ÚSZ-levelek, 484 820 Károli-token), az előmérés a `pardes.db` régi `token_karoli`-jából (csak ÓSZ, 456 879 token). A módszer és a küszöbök változatlanok; a kimenet: `adat/szoto/szabaly_ellenorzes.tsv` (generált).

**Eltérés az előméréstől:** 31 alátámasztva / 14 gyenge / 4 ellentmond / 2 nincs adat (az előmérés: 34 / 12 / 3 / 2). Átsorolódott: *körűl → körül*, *nyny → nny*, *^setét → sötét* (alátámasztva → gyenge), *értelm- → értelem* (gyenge → ellentmond). Ok: a párosítás más (a régi `token_karoli` Strong-párjai helyett a #22 párosítása, pl. az 1. minta *ki*-jének téves H0834-e, 6.1), és a hatókör bővebb (ÚSZ-levelek).

**Következmény a `szabaly_forras`-ra (a .2-ben):** a `korpusz_strong` jelölést a repó saját ellenőrzése adja (alátámasztva), kivéve a *cz → c*-t, amely a felhasználó utasítása szerint `manual` (7.3); így a .2-ben az 51 szabály: **30 `korpusz_strong` + 1 `manual` (*cz → c*) + 20 `modell_ellenorizetlen`**. A brief K4-e (34 `korpusz_strong`) az előmérés számát rögzítette; az eltérést a felhasználó a következő megállásnál látja.


Helyesírásinál a „pár” oszlop: hány régi alaknak van cserélt párja a Károliban; tőváltónál: az új család alakszáma.

| típus | szabály | régi alak / token | pár (alak / token) | Strong-támasz | könyvek | minősítés | példák |
|---|---|---|---|---|---|---|---|
| helyesírás | űl$ → ül | 26 / 160 | 21 / 155 | 64% (71/111) | csak régi 0, csak új 41, mindkettő 9 | gyenge | közűl(60)~közül(695); feleségűl(18)~feleségül(56); körűl(13)~körül(124); köröskörűl(12)~köröskörül(134) |
| helyesírás | űle → üle | 15 / 60 | 8 / 45 | 93% (41/44) | csak régi 1, csak új 26, mindkettő 4 | alátámasztva | szűle(31)~szüle(7); leűle(5)~leüle(11); közűletek(3)~közületek(35); űle(2)~üle(14) |
| helyesírás | ^szűl → szül | 33 / 124 | 16 / 103 | 89% (93/104) | csak régi 5, csak új 18, mindkettő 8 | alátámasztva | szűle(31)~szüle(7); szűlt(19)~szült(19); szűlé(18)~szülé(17); szűl(8)~szül(10) |
| helyesírás | körűl → körül | 19 / 47 | 9 / 35 | 67% (22/33) | csak régi 1, csak új 27, mindkettő 2 | gyenge | körűl(13)~körül(124); köröskörűl(12)~köröskörül(134); körűlmetélé(3)~körülmetélé(2); körűlmetéletlen(2)~körülmetéletlen(13) |
| helyesírás | sűly → süly | 1 / 2 | 0 / 0 | — | csak régi 0, csak új 0, mindkettő 0 | nincs adat |  |
| helyesírás | nyny → nny | 35 / 139 | 8 / 82 | 65% (53/82) | csak régi 5, csak új 13, mindkettő 18 | gyenge | aranynyal(51)~arannyal(5); bizonynyal(16)~bizonnyal(4); tudománynyal(8)~tudománnyal(1); menynyivel(2)~mennyivel(19) |
| helyesírás | ^setét → sötét | 14 / 50 | 8 / 42 | 67% (29/43) | csak régi 9, csak új 13, mindkettő 5 | gyenge | setétség(15)~sötétség(28); setétségben(9)~sötétségben(13); setétben(6)~sötétben(8); setétségnek(4)~sötétségnek(6) |
| helyesírás | cz → c | 783 / 2088 | 5 / 14 | 97% (30/31) | csak régi 6, csak új 2, mindkettő 3 | alátámasztva | harminczhárom(5)~harminchárom(1); harminczezer(4)~harmincezer(1); tizennyolczezer(3)~tizennyolcezer(2); nyolczvanhat(1)~nyolcvanhat(1) |
| helyesírás | ^kiván → kíván | 51 / 122 | 21 / 81 | 16% (13/80) | csak régi 5, csak új 13, mindkettő 17 | ellentmond | kiván(11)~kíván(7); kivánsága(9)~kívánsága(11); kivánatos(8)~kívánatos(7); kivánják(6)~kívánják(3) |
| tőváltó | lelk- → lélek | 53 / 641 | 6 / 171 | 89% (594/670) | csak régi 13, csak új 3, mindkettő 34 | alátámasztva | lelkem(111); lelke(110); lelkét(73); lelkemet(63) | fő Strong régi: H5315,H7307, új: G4151,H5315,H7307 |
| tőváltó | ur- → úr | 47 / 1468 | 14 / 6142 | 57% (893/1559) | csak régi 2, csak új 6, mindkettő 47 | gyenge | uram(552); urat(342); ura(257); urának(63) | fő Strong régi: H0113,H3068, új: H3068 |
| tőváltó | tav- → tó | 7 / 9 | 7 / 15 | 75% (9/12) | csak régi 4, csak új 5, mindkettő 2 | alátámasztva | tavakat(2); tavává(2); tavaira(1); tavat(1) | fő Strong régi: H0098,H1295,H5921, új: H0098,H1295,H8583 |
| tőváltó | magv- → mag | 15 / 81 | 81 / 1630 | 79% (68/86) | csak régi 0, csak új 31, mindkettő 25 | alátámasztva | magva(22); magvát(14); magvából(12); magvának(11) | fő Strong régi: H2233, új: H2233 |
| tőváltó | sátr- → sátor | 11 / 20 | 40 / 342 | 89% (16/18) | csak régi 3, csak új 16, mindkettő 10 | alátámasztva | sátrai(4); sátrakat(3); sátrait(3); sátraiból(2) | fő Strong régi: H0168, új: H0168 |
| tőváltó | derek- → derék | 25 / 46 | 4 / 14 | 79% (45/57) | csak régi 12, csak új 3, mindkettő 6 | alátámasztva | derekának(8); derekadat(6); derekán(4); derekukat(2) | fő Strong régi: H4975,H5921, új: H2428,H4803,H4975,H5921 |
| tőváltó | kez- → kéz | 88 / 1262 | 8 / 40 | 85% (1107/1309) | csak régi 27, csak új 0, mindkettő 17 | alátámasztva | kezébe(185); keze(120); kezéből(114); kezét(105) | fő Strong régi: H3027, új: H3027 |
| tőváltó | nev- → név | 38 / 781 | 5 / 18 | 91% (755/834) | csak régi 38, csak új 0, mindkettő 9 | alátámasztva | neve(190); nevét(154); nevében(56); nevedet(42) | fő Strong régi: H8034, új: G3686,H8034 |
| tőváltó | viz- → víz | 38 / 347 | 12 / 164 | 90% (320/356) | csak régi 11, csak új 5, mindkettő 22 | alátámasztva | vizet(113); vizek(87); vize(16); vizét(15) | fő Strong régi: H4325, új: H4325 |
| tőváltó | tüz- → tűz | 9 / 84 | 13 / 232 | 82% (69/84) | csak régi 3, csak új 17, mindkettő 18 | alátámasztva | tüzet(54); tüze(14); tüzét(8); tüzében(3) | fő Strong régi: H0784,H2740, új: H0784 |
| tőváltó | kenyer- → kenyér | 21 / 196 | 6 / 54 | 81% (162/200) | csak régi 12, csak új 0, mindkettő 19 | alátámasztva | kenyeret(113); kenyerét(15); kenyerek(13); kenyeredet(10) | fő Strong régi: H3899,H4682, új: H3899 |
| tőváltó | level- → levél | 11 / 57 | 5 / 27 | 56% (34/61) | csak régi 5, csak új 3, mindkettő 11 | gyenge | levelet(34); leveleket(8); levele(4); levelei(2) | fő Strong régi: H0107,H5612, új: G1992,H5612 |
| tőváltó | madar- → madár | 19 / 76 | 5 / 30 | 77% (61/79) | csak régi 8, csak új 3, mindkettő 9 | alátámasztva | madarak(18); madarat(15); madarainak(7); madaraknak(7) | fő Strong régi: H5775,H6833, új: H5775,H6833 |
| tőváltó | falv- → falu | 4 / 7 | 8 / 48 | 29% (2/7) | csak régi 3, csak új 5, mindkettő 2 | ellentmond | falvakban(3); falvait(2); falvainak(1); falvak(1) | fő Strong régi: H2333,H2334,H2691,H3723,H5892, új: H1323,H2691 |
| tőváltó | ökr- → ökör | 17 / 88 | 6 / 51 | 89% (82/92) | csak régi 9, csak új 3, mindkettő 11 | alátámasztva | ökröt(28); ökrök(12); ökrét(8); ökröket(8) | fő Strong régi: H1241,H7794, új: H1241,H7794 |
| tőváltó | bokr- → bokor | 1 / 3 | 1 / 2 | 33% (1/3) | csak régi 1, csak új 1, mindkettő 1 | gyenge | bokrok(3) | fő Strong régi: H2336,H5521,H7880, új: H7880 |
| tőváltó | szav- → szó | 40 / 399 | 17 / 159 | 82% (338/413) | csak régi 4, csak új 4, mindkettő 31 | alátámasztva | szavát(110); szava(84); szavára(75); szavakat(13) | fő Strong régi: H1697,H6963, új: H1697,H6963 |
| tőváltó | erej- → erő | 12 / 109 | 16 / 127 | 46% (53/116) | csak régi 6, csak új 9, mindkettő 24 | gyenge | ereje(34); erejét(26); erejével(19); erejének(10) | fő Strong régi: H3581,H5797, új: H3581,H5797 |
| tőváltó | lov- → ló | 22 / 109 | 7 / 49 | 86% (102/118) | csak régi 13, csak új 4, mindkettő 12 | alátámasztva | lovak(22); lovakat(20); lovat(16); lovakon(13) | fő Strong régi: H5483, új: H3876,H5483 |
| tőváltó | köv- → kő | 25 / 241 | 8 / 70 | 55% (134/244) | csak régi 5, csak új 2, mindkettő 24 | gyenge | követ(68); követeket(51); köveket(40); kövek(17) | fő Strong régi: H0068,H4397, új: H0068 |
| tőváltó | füv- → fű | 7 / 28 | 5 / 32 | 47% (14/30) | csak régi 8, csak új 5, mindkettő 6 | gyenge | füvet(14); füve(4); füvön(3); füveknek(3) | fő Strong régi: H1314,H2682,H6211,H6212, új: G5528,H1877,H2682,H6212 |
| tőváltó | nyar- → nyár | 1 / 1 | 4 / 12 | 100% (1/1) | csak régi 0, csak új 6, mindkettő 1 | alátámasztva | nyarat(1) | fő Strong régi: H7019, új: H7019 |
| tőváltó | pohar- → pohár | 11 / 28 | 4 / 17 | 86% (25/29) | csak régi 6, csak új 4, mindkettő 5 | alátámasztva | poharat(6); poharát(6); pohara(4); poharakból(2) | fő Strong régi: H1375,H3563,H3713, új: H1375,H3563,H3713 |
| tőváltó | gyöker- → gyökér | 12 / 32 | 1 / 2 | 79% (26/33) | csak régi 13, csak új 1, mindkettő 1 | alátámasztva | gyökere(7); gyökeret(6); gyökereit(4); gyökerök(3) | fő Strong régi: H8328, új: H8328 |
| tőváltó | tehen- → tehén | 8 / 23 | 2 / 12 | 61% (14/23) | csak régi 5, csak új 2, mindkettő 2 | gyenge | tehenet(8); tehenek(5); teheneidnek(3); teheneket(2) | fő Strong régi: H0504,H6510,H7794, új: H6510 |
| tőváltó | szeker- → szekér | 28 / 124 | 8 / 40 | 95% (124/131) | csak régi 11, csak új 1, mindkettő 12 | alátámasztva | szekeret(21); szekerek(20); szekereket(15); szekerei(11) | fő Strong régi: H4818,H5699,H7393, új: H0413,H4818,H5699,H7393 |
| tőváltó | kebl- → kebel | 13 / 16 | 13 / 19 | 60% (12/20) | csak régi 6, csak új 5, mindkettő 5 | gyenge | kebleden(2); keblébe(2); keblében(2); keblem(1) | fő Strong régi: H0413,H1717,H2436,H7130, új: H0413,H2436 |
| tőváltó | terh- → teher | 11 / 55 | 5 / 23 | 53% (28/53) | csak régi 14, csak új 4, mindkettő 7 | gyenge | terhét(23); terhe(12); terhet(8); terhére(4) | fő Strong régi: H4853,H5375, új: H2029,H4853 |
| tőváltó | ajk- → ajak | 31 / 64 | 8 / 11 | 80% (57/71) | csak régi 16, csak új 2, mindkettő 5 | alátámasztva | ajkai(7); ajkait(7); ajkaim(4); ajkaival(4) | fő Strong régi: H8193, új: H8193 |
| tőváltó | fark- → farok | 4 / 10 | 0 / 0 | 0% (0/10) | csak régi 5, csak új 0, mindkettő 0 | nincs adat | farkát(6); farkat(2); farka(1); farkait(1) | fő Strong régi: H0451,H2180, új: — |
| tőváltó | dolg- → dolog | 45 / 439 | 9 / 159 | 38% (144/377) | csak régi 12, csak új 3, mindkettő 30 | gyenge | dolgot(127); dolgai(52); dolgokat(47); dolga(24) | fő Strong régi: H1697, új: H1697 |
| tőváltó | torny- → torony | 16 / 37 | 3 / 13 | 78% (31/40) | csak régi 9, csak új 1, mindkettő 4 | alátámasztva | tornyot(8); tornyok(5); tornyokat(3); tornya(3) | fő Strong régi: H1785,H4026, új: H4026,H5704 |
| tőváltó | esztendej- → esztendő | 7 / 162 | 11 / 229 | 87% (148/170) | csak régi 1, csak új 12, mindkettő 16 | alátámasztva | esztendejében(108); esztendeje(24); esztendejéig(15); esztendejétől(5) | fő Strong régi: H8141, új: H8141 |
| tőváltó | idej- → idő | 10 / 280 | 16 / 252 | 83% (229/275) | csak régi 6, csak új 5, mindkettő 35 | alátámasztva | idejében(92); ideje(86); idején(74); idejét(8) | fő Strong régi: H3117,H6256, új: H3117,H6256 |
| tőváltó | mezej- → mező | 9 / 44 | 17 / 207 | 70% (33/47) | csak régi 1, csak új 13, mindkettő 16 | alátámasztva | mezején(22); mezejére(5); mezejének(5); mezejéről(5) | fő Strong régi: H7704, új: H7704 |
| tőváltó | tetej- → tető | 8 / 82 | 7 / 9 | 82% (98/120) | csak régi 20, csak új 1, mindkettő 4 | alátámasztva | tetején(34); tetejére(26); tetejéről(6); tetejét(6) | fő Strong régi: H5921,H7218, új: H1354,H1406,H5921,H7218 |
| tőváltó | fi- → fiú | 72 / 4535 | 9 / 72 | 93% (4405/4745) | csak régi 25, csak új 0, mindkettő 27 | alátámasztva | fiai(1397); fia(1207); fiainak(506); fiának(298) | fő Strong régi: H1121, új: G5207,H1121,H5288 |
| tőváltó | kegyelm- → kegyelem | 22 / 161 | 6 / 44 | 76% (131/172) | csak régi 13, csak új 5, mindkettő 15 | alátámasztva | kegyelme(61); kegyelmet(25); kegyelmed(20); kegyelmedet(8) | fő Strong régi: G5485,H2617, új: G5485,H2617 |
| tőváltó | félelm- → félelem | 19 / 65 | 6 / 36 | 24% (16/67) | csak régi 9, csak új 6, mindkettő 8 | ellentmond | félelme(24); félelmére(9); félelmében(6); félelmét(5) | fő Strong régi: H2851,H3374,H6343, új: G5401,H6343 |
| tőváltó | értelm- → értelem | 11 / 64 | 5 / 37 | 26% (18/69) | csak régi 10, csak új 1, mindkettő 8 | ellentmond | értelmet(21); értelmét(18); értelme(11); értelmetek(3) | fő Strong régi: H0998,H6591,H8394, új: G5426,H0998,H8394 |
| tőváltó | szerelm- → szerelem | 13 / 29 | 3 / 7 | 78% (25/32) | csak régi 9, csak új 0, mindkettő 2 | alátámasztva | szerelme(5); szerelmemben(4); szerelmében(4); szerelmet(3) | fő Strong régi: H0160,H1730,H7068, új: H0160,H1730,H7065,H7068 |
| tőváltó | eg- → ég | 17 / 150 | 14 / 283 | 82% (126/153) | csak régi 7, csak új 12, mindkettő 22 | alátámasztva | egek(57); eget(30); egeket(24); egeknek(8) | fő Strong régi: H8064, új: H8064 |

Összesen: alátámasztva: 31, gyenge: 14, ellentmond: 4, nincs adat: 2

scope=hibrid.py (sha256:864d6876437a) HELYESIRAS (9) + TOVALTO (42) szabályai; a párosított Károli-könyvek (57 szavak-fájl, oldal=hu, 484820 token) | forras=adat/karoli_strong/szavak_*.tsv (együttes sha256:c3266499df09; modell-kimenet, javaslat) | ts=2026-10-13T13:10Z


## 11. Hibrid v3 (F94.2)

### 11.1 A K tábla (C+K változat, DT-F94c)

*proveniencia: scope=a Károli 1908 leggyakoribb 400 alakja | forras=adat/szoto/karoli_lexikon.tsv (a kiválasztás, gépi) + manual (a szótári alak modell-javaslat a DT130 szerint, modell: claude-opus-5-5) | ts=2026-10-13*

- **N = 400.** A gyakorisági lista (kisbetűs + mondatkezdő előfordulás, kisbetűsítve) lefedettsége: 100 alak 49,7%, 200 alak 55,0%, 300 alak 58,1%, **400 alak 60,4%**, 500 alak 62,1%, 1000 alak 67,7% (553 804 token). A 400. alak 107-szer fordul elő. 300 felett a lefedettség lassan nő (kb. 2 százalékpont / 100 alak), és a K-sorokat a felhasználó soronként nézi át (F94.3 ⛔); a 400 a kettő közti egyensúly. A sorok kiválasztása gépi (`eszkozok/szoto/k_tabla_epit.py`), nem a mérés hibáiból és nem a minták alakjaiból (meresi_terv 1.3).
- **A szótári alak forrása:** modell-javaslat a DT130 szerint; 222 sor nem önmagára leképezett (ragos névmás → személyes névmás, a van/lesz rendhagyó alakjai, régies igealakok, birtokos/ragos névszók, régi/mai írásmód), 178 önálló szótári alak. **A simplemma kimenetéből nem jön** (DT-F94c): a kitöltéskor a simplemmát és a hibridet a K alakjain nem futtattam, és összevetés utáni átvétel sem történt. Őszinte korlát: a 9. szakasz hibalistái (néhány gyakori alak A- és C-kimenete a mintákon, pl. *mert → mer, azt*) a kitöltés előtt a modell előtt voltak; ezek a DT130 szerinti szótári alakot nem befolyásolják, de a felhasználó átnézésekor érdemes tudni.
- `ellenorzes=modell_ellenorizetlen` mind a 400 sorban; `felhasznalo` csak a felhasználó átnézése után (F94.3 ⛔, a 4. mintával együtt). A K a v3 része: a v3 befagyasztása a K tábla mostani tartalmával történik; a felhasználói javítás a C+K változatot a 4. minta mérése előtt módosíthatja — ez esetben a K tábla új sha256-ja a mérés proveniencia-sorában áll.

### 11.2 A v3 változásai (osztály- és szabályszinten)

A teljes lista a `eszkozok/szoto/hibrid.py` leírásában. Röviden: -é kérdőszócska kötőjellel; birtokos + rag (csupasz-tő bővítése, -ság/-ség/-ás/-és + birtokos -a/-e); igekötő + ismeretlen ige; képzett igealak (DT130 (10): -hat/-het, szenvedő -tatik/-tetik, alapigével); mai igei ragozás igei attesztációval (C/CK; az A-ban csak ha a simplemma-ág nem változtatott); kivételtábla (maga, névutók és határozószók -á/-é alakja, hozzá/reá, v-tövű igék -vén alakja, jő-alakok, lesz/visz/hisz/tesz/vesz alapalakja, egyétek); tőváltó *kötel-*, *atyj-*; *^kiván* igekötő után is; -ök → -ük lexikon-attesztációval; a simplemma tulajdonnévi lemmája kisbetűs alakra elvetve; -ás/-és/-ság/-ség képzős főnév a simplemma alapszava helyett.

**Szigorított régies ige-felismerés (v1.1):** a jelölt tő csak igei alakkal igazolható (-ni, -ott/-ett/-ött/-tt, -ván/-vén, -jon/-jen/-jön; önmaga nem; legfeljebb hárombetűs tőnél két különböző alak); a -nak/-nek/-tok/-tek/-tök csak akkor, ha a tő a Károliban egyértelmű névszói raggal nem fordul elő; az igekötő önmagában nem igető; -ik-es ige csak mássalhangzós, önállóan elő nem forduló, igeileg attesztált tőből; a -ál/-él/-ék végű névszó és az egyértelmű névszói esetraggal is előforduló tő (*fej-re*, *szív-ben*) nem régies ige; a -ték/-tték múlt T/3; -felé/-felől határozószó kizárva. Az A-ban a simplemma igei tudása (ismert főnévi igenév / múlt idejű alak ugyanarra a tőre) is igazol; a névszói „ismert szó” próba nem.

**Régies igei jegy (`regies_jegy`):** értékkészlet: `mult.alanyi.E3` (-a/-e), `mult.targyas.E3` (-á/-é), `mult.E1` (-ék), `mult.E2` (-ál/-él), `mult.T1` (-ánk/-énk), `mult.T2` (-átok/-étek), `mult.T3` (-ának/-ének), `felszolito.E2` (-jál/-jél, -zzál …), `hatarozoi_igenev` (-ván/-vén); a kivételtábla régies igealakjai (vala, vevé, menének …) saját jegyet kapnak; a mai felszólító (-jen, -janak) és a nem igei alak jegye üres. A K-sor jegye a szabályág (C) elemzéséből jön, ha az ugyanarra a szótári alakra jut.

**Szabályforrás (`szabaly_forras`):** a helyesírási (9) és tőváltó (44, ebből 2 új: *kötel-*, *atyj-*) szabályokból **30 `korpusz_strong`** (a 10. szakasz szabályellenőrzésének alátámasztott szabályai, a *cz → c* nélkül), **1 `manual`** (*cz → c*, 7.3), **22 `modell_ellenorizetlen`** (a nem alátámasztott 20 + a 2 új, ellenőrizetlen tőváltó); a régies végződés-, képző- és ragozási szabályok `modell_ellenorizetlen`.

### 11.3 Regresszió: v3 a v2-höz képest a három fejlesztési mintán

*A v2 = `eszkozok/szoto/hibrid_v2.py` (az átvett előmérési v2, A/B/C kapcsolóval). Alakonként / súlyozva, rétegenként.*

##### szoto_minta_1_fejlesztes.tsv (213 alak)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 97% / 99.4% (206/213) | 98% / 99.6% (54/55) | 98% / 99.1% (64/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 86% / 89.5% (6/7) | 100% / 100.0% (27/27) |
| hibrid C | 85% / 94.3% (182/213) | 89% / 95.0% (49/55) | 82% / 82.2% (53/65) | 87% / 93.9% (39/45) | 79% / 88.2% (11/14) | 43% / 52.6% (3/7) | 100% / 100.0% (27/27) |
| hibrid CK | 91% / 99.0% (193/213) | 100% / 100.0% (55/55) | 89% / 93.0% (58/65) | 87% / 93.9% (39/45) | 79% / 88.2% (11/14) | 43% / 52.6% (3/7) | 100% / 100.0% (27/27) |
| v2 A | 95% / 99.2% (203/213) | 98% / 99.6% (54/55) | 95% / 96.6% (62/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 71% / 78.9% (5/7) | 100% / 100.0% (27/27) |
| v2 C | 79% / 92.6% (169/213) | 85% / 93.8% (47/55) | 71% / 73.6% (46/65) | 80% / 88.6% (36/45) | 79% / 88.2% (11/14) | 29% / 42.1% (2/7) | 100% / 100.0% (27/27) |

scope=szoto_minta_1_fejlesztes.tsv (sha256:a7f8d65d42de) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:7c7160343b55) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:46Z

##### szoto_minta_2_fejlesztes.tsv (180 alak)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 93% / 97.9% (167/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 90% / 91.0% (19/21) | 100% / 100.0% (10/10) |
| hibrid C | 84% / 87.8% (151/180) | 90% / 87.6% (36/40) | 84% / 86.5% (54/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 71% / 82.1% (15/21) | 100% / 100.0% (10/10) |
| hibrid CK | 87% / 96.0% (156/180) | 98% / 98.4% (39/40) | 88% / 92.1% (56/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 71% / 82.1% (15/21) | 100% / 100.0% (10/10) |
| v2 A | 92% / 97.6% (166/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 86% / 85.9% (18/21) | 100% / 100.0% (10/10) |
| v2 C | 80% / 85.8% (144/180) | 90% / 87.6% (36/40) | 78% / 76.7% (50/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 57% / 64.1% (12/21) | 100% / 100.0% (10/10) |

scope=szoto_minta_2_fejlesztes.tsv (sha256:587e47bded57) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:7c7160343b55) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:46Z

##### szoto_minta_3_ellenorzott.tsv (113 alak)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 94% / 99.7% (106/113) | 100% / 100.0% (25/25) | 91% / 90.6% (32/35) | 100% / 100.0% (20/20) | 75% / 78.6% (9/12) | 100% / 100.0% (13/13) | 88% / 81.8% (7/8) |
| hibrid C | 76% / 91.3% (86/113) | 88% / 92.0% (22/25) | 71% / 78.1% (25/35) | 95% / 97.2% (19/20) | 25% / 28.6% (3/12) | 77% / 58.6% (10/13) | 88% / 81.8% (7/8) |
| hibrid CK | 79% / 99.0% (89/113) | 100% / 100.0% (25/25) | 71% / 78.1% (25/35) | 95% / 97.2% (19/20) | 25% / 28.6% (3/12) | 77% / 58.6% (10/13) | 88% / 81.8% (7/8) |
| v2 A | 80% / 99.1% (90/113) | 100% / 100.0% (25/25) | 80% / 84.4% (28/35) | 50% / 58.3% (10/20) | 67% / 71.4% (8/12) | 92% / 96.6% (12/13) | 88% / 81.8% (7/8) |
| v2 C | 56% / 90.3% (63/113) | 88% / 92.0% (22/25) | 51% / 62.5% (18/35) | 40% / 30.6% (8/20) | 17% / 21.4% (2/12) | 54% / 48.3% (7/13) | 75% / 72.7% (6/8) |

scope=szoto_minta_3_ellenorzott.tsv (sha256:bafc1e67a061) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:7c7160343b55) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T13:46Z

**Eredmény:** a v3 A **mindhárom mintán és minden rétegben legalább a v2 A szintjén** áll (a 3. mintán 80% / 99,1% → 94% / 99,7%); a v3 C minden rétegben legalább a v2 C szintjén. Egyedi alakon (a v2-ben helyes, a v3-ban hibás):

```
szoto_minta_1_fejlesztes.tsv A ROMLÁS: —
szoto_minta_1_fejlesztes.tsv C ROMLÁS: —
szoto_minta_1_fejlesztes.tsv CK ROMLÁS: —
szoto_minta_2_fejlesztes.tsv A ROMLÁS: —
szoto_minta_2_fejlesztes.tsv C ROMLÁS: leheletének(ragos_nevszo,1): v2=lehelet v3=leheletének
szoto_minta_2_fejlesztes.tsv CK ROMLÁS: leheletének(ragos_nevszo,1): v2=lehelet v3=leheletének
szoto_minta_3_ellenorzott.tsv A ROMLÁS: —
szoto_minta_3_ellenorzott.tsv C ROMLÁS: —
szoto_minta_3_ellenorzott.tsv CK ROMLÁS: —
```

A *leheletének* (C, CK) a v1.1 szigorítás közvetlen ára: a v2 a *leheletnek* alakkal „igazolta” a *lehelet*-et régies igének, és így véletlenül jó tövet adott; a v3 ezt már nem fogadja el, a névszói ág pedig a ritka *lehelet*-et nem attesztálja. A C+K a 3. (ellenőrzött) mintán súlyozva 99,0%, az A 99,7%; alakonként 79% és 94%.

### 11.4 K6 — a teljes Károli 200 leggyakoribb felismert régies igealakja, kézi besorolással

*proveniencia a lista alatt; a besorolás manual (modell: claude-opus-5-5). A gyakoriság kisbetűsítve; a mondat belsejében nagybetűs (név) alakok kihagyva, mert a hibrid névágon tövezi őket.*

**Előtte (v2 A):** 74 / 200 **nem ige** (névszó, névutó, határozószó, névmás): felé, többé, házának, királyának, mellé, közé, nemzetsége, magának, földére, halál, angyala, népének, sátorának, sokasága, továbbá, háznépe, leányának, szélessége, zsoltára, fölé, nemzetségének, feleségének, életének, gyülekezete, magassága, emberének, nyilván, igazsága, földének, belé, maradéka, szövetségének, városának, dicsőségének, gyümölcse, seregének, hosszúsága, testvérének, testének, uralkodásának, erőssége, fiaié, gonoszsága, királyságának, országának, reménysége, gazdagsága, parancsolata, rendelése, fejének, szájának, szívének, ítélete, gyülekezetének, temploma, teljessége, világossága, angyalának, bölcsesége, férjének, mögé, nyílása, elsőszülötte, felének, hegyének, oltára, tisztának, hajlékának, háznépének, irgalmassága, kevélysége, robota, törvényének, zúgása. A többi 126 ige (köztük téves tövű igék is: *tudjátok → tudj, egyétek → egyik, bocsátok → bocs*).

(hibrid_v2, A): a 200 leggyakoribb felismert régies igealak

mondván (1237) → mond; felé (304) → fel; többé (297) → több; házának (260) → ház; királyának (182) → király; nemzé (175) → nemz; mellé (165) → mell; közé (142) → köz; felelvén (123) → felel; nemzetsége (115) → nemzetség; magának (109) → mag; látá (92) → lát; földére (90) → földér; látván (87) → lát; tudjátok (87) → tudj; nevezé (83) → nevez; halál (81) → hal; angyala (69) → angyal; cselekedjél (68) → cselekedik; elmenvén (68) → elmen; elindulának (67) → elindul; népének (63) → nép; sátorának (62) → sátor; felelének (60) → felel; sokasága (60) → sokaság; elküldé (59) → elküld; továbbá (59) → tovább; cselekedének (58) → cselekedik; háznépe (58) → háznép; emlékezzél (56) → emlékezik; bemenvén (54) → bemen; felkelvén (54) → felkel; leányának (53) → leány; megtudjátok (52) → megtudj; szélessége (52) → szélesség; menvén (51) → men; megölé (50) → megöl; zsoltára (48) → zsoltár; kimenvén (47) → kimen; meghallá (47) → meghall; megveré (47) → megver; hallván (46) → hall; fölé (45) → föl; nemzetségének (45) → nemzetség; szólának (45) → szól; tudván (45) → tud; megáldá (44) → megáld; feleségének (42) → feleség; megparancsolá (41) → megparancsol; felemelé (39) → felemel; elbocsátá (38) → elbocsát; életének (38) → élet; egyétek (37) → egyik; veté (36) → vet; kiáltának (35) → kiált; akará (34) → akar; bocsátok (33) → bocs; csinálának (33) → csinál; gyülekezete (33) → gyülekezet; állának (33) → áll; elbeszélé (32) → elbeszél; magassága (32) → magasság; emberének (31) → ember; kezdé (31) → kezd; tartsátok (31) → tarts; nyilván (30) → nyil; felkelének (29) → felkel; igazsága (29) → igazság; követé (29) → követ; megkérdé (29) → megkérd; parancsolá (29) → parancsol; cselekedvén (28) → cselekedik; hozának (28) → hoz; szólván (27) → szól; földének (26) → föld; megépíté (26) → megépít; belé (25) → bel; eljutának (25) → eljut; maradéka (25) → maradék; meghajtá (25) → meghajt; meglátá (25) → meglát; szövetségének (25) → szövetség; városának (25) → város; dicsőségének (24) → dicsőség; gyümölcse (24) → gyümölcs; seregének (24) → sereg; szólítá (24) → szólít; visszatérének (24) → visszatér; építé (24) → épít; összegyűjté (24) → összegyűjt; elvégezé (23) → elvégez; felgerjede (22) → felgerjed; hagyá (22) → hagy; hosszúsága (22) → hosszúság; teremté (22) → teremt; testvérének (22) → testvér; elfutának (21) → elfut; jutának (21) → jut; kéré (21) → kér; szeressétek (21) → szeress; testének (21) → test; uralkodásának (21) → uralkodás; akarván (20) → akar; beborítá (20) → beborít; erőssége (20) → erősség; fiaié (20) → fiai; gonoszsága (20) → gonoszság; királyságának (20) → királyság; országának (20) → ország; reménysége (20) → reménység; gazdagsága (19) → gazdagság; helyhezteté (19) → helyheztet; illeté (19) → illet; küldének (19) → küld; megfogván (19) → megfog; megnyitá (19) → megnyit; megszaggatá (19) → megszaggat; szülé (19) → szül; áldozának (19) → áldoz; elfuta (18) → elfut; hallá (18) → hall; leborula (18) → leborul; parancsolata (18) → parancsolat; rendelése (18) → rendelés; szűlé (18) → szül; találá (18) → talál; vessétek (18) → vess; vetének (18) → vet; bízzál (17) → bízik; fejének (17) → fej; hívatá (17) → hívat; megemészté (17) → megemészt; megfélemlének (17) → megféleml; megtartsátok (17) → megtarts; szájának (17) → száj; szívének (17) → szív; ítélete (17) → ítélet; összegyűlének (17) → összegyűl; bocsátá (16) → bocsát; gyülekezetének (16) → gyülekezet; temploma (16) → templom; izenvén (15) → izen; járván (15) → jár; kinyújtá (15) → kinyújt; lakozának (15) → lakozik; leborulának (15) → leborul; megcsókolá (15) → megcsókol; meghalának (15) → meghal; megméré (15) → megmér; megállának (15) → megáll; teljessége (15) → teljesség; világossága (15) → világosság; angyalának (14) → angyal; bölcsesége (14) → bölcseség; felindítá (14) → felindít; férjének (14) → férj; hivatá (14) → hivat; hívá (14) → hív; megkérdezé (14) → megkérdez; méré (14) → mér; mögé (14) → mög; nyílása (14) → nyílás; öljétek (14) → ölj; elsőszülötte (13) → elsőszülött; felének (13) → fel; hegyének (13) → hegy; ismeré (13) → ismer; kezdének (13) → kezd; követvén (13) → követ; küldé (13) → küld; maradának (13) → marad; megdorgálá (13) → megdorgál; meggyógyítá (13) → meggyógyít; meghallgatá (13) → meghallgat; megszabadítá (13) → megszabadít; oltára (13) → oltár; tisztának (13) → tiszt; vetvén (13) → vet; akarjátok (12) → akarj; ejté (12) → ejt; elküldvén (12) → elküld; elrejté (12) → elrejt; felállítá (12) → felállít; fölkele (12) → fölkel; hajlékának (12) → hajlék; háznépének (12) → háznép; irgalmassága (12) → irgalmasság; járának (12) → jár; kevélysége (12) → kevélység; kitölté (12) → kitölt; kiűzé (12) → kiűz; kérvén (12) → kér; megcsinálá (12) → megcsinál; meghagyá (12) → meghagy; meglátván (12) → meglát; robota (12) → robot; találának (12) → talál; tanítván (12) → tanít; törvényének (12) → törvény; zúgása (12) → zúgás

**Utána (v3 A): 0 / 200 nem ige** — a besorolt listán nincs névszó régies igeként (K6). A tövek közül nem mind helyes (pl. *látszék → látsz*, *egybegyűle → egybegyül*, *egybegyűjté → egybegyűjtik*, *megjelenék → megjelen*), de mind ige.

#### Utána (hibrid v3, A): a 200 leggyakoribb felismert régies igealak (végződés, jegy)

mondván (1237) → mond [hatarozoi_igenev]; nemzé (175) → nemz [mult.targyas.E3]; adá (141) → ad [mult.targyas.E3]; cselekedék (124) → cselekszik [mult.E1]; felelvén (123) → felel [hatarozoi_igenev]; uralkodék (109) → uralkodik [mult.E1]; látá (92) → lát [mult.targyas.E3]; látván (87) → lát [hatarozoi_igenev]; nevezé (83) → nevez [mult.targyas.E3]; cselekedjél (68) → cselekszik [felszolito.E2]; elindulának (67) → elindul [mult.T3]; ütének (64) → üt [mult.T3]; esék (62) → esik [mult.E1]; felelének (60) → felel [mult.T3]; elküldé (59) → elküld [mult.targyas.E3]; cselekedének (58) → cselekszik [mult.T3]; emlékezzél (56) → emlékszik [felszolito.E2]; felkelvén (54) → felkel [hatarozoi_igenev]; megölé (50) → megöl [mult.targyas.E3]; meghallá (47) → meghall [mult.targyas.E3]; megveré (47) → megver [mult.targyas.E3]; hallván (46) → hall [hatarozoi_igenev]; adának (45) → ad [mult.T3]; szólának (45) → szól [mult.T3]; tudván (45) → tud [hatarozoi_igenev]; megáldá (44) → megáld [mult.targyas.E3]; megparancsolá (41) → megparancsol [mult.targyas.E3]; felemelé (39) → felemel [mult.targyas.E3]; elbocsátá (38) → elbocsát [mult.targyas.E3]; láték (37) → lát [mult.E1]; eltemeték (36) → eltemet [mult.E1]; veté (36) → vet [mult.targyas.E3]; kiáltának (35) → kiált [mult.T3]; tetszék (35) → tetszik [mult.E1]; akará (34) → akar [mult.targyas.E3]; csinálának (33) → csinál [mult.T3]; állának (33) → áll [mult.T3]; elbeszélé (32) → elbeszél [mult.targyas.E3]; kezdé (31) → kezd [mult.targyas.E3]; megjelenék (31) → megjelen [mult.E1]; adván (29) → ad [hatarozoi_igenev]; eltemetteték (29) → eltemettet [mult.E1]; felkelének (29) → felkel [mult.T3]; követé (29) → követ [mult.targyas.E3]; lakozék (29) → lakozik [mult.E1]; megkérdé (29) → megkérd [mult.targyas.E3]; parancsolá (29) → parancsol [mult.targyas.E3]; cselekedvén (28) → cselekszik [hatarozoi_igenev]; hozának (28) → hoz [mult.T3]; megölék (28) → megöl [mult.E1]; szólván (27) → szól [hatarozoi_igenev]; eltávozék (26) → eltávozik [mult.E1]; megépíté (26) → megépít [mult.targyas.E3]; áldozék (26) → áldoz [mult.E1]; eljutának (25) → eljut [mult.T3]; meghajtá (25) → meghajt [mult.targyas.E3]; meglátá (25) → meglát [mult.targyas.E3]; adaték (24) → adatik [mult.E1]; szólítá (24) → szólít [mult.targyas.E3]; visszatérének (24) → visszatér [mult.T3]; építé (24) → épít [mult.targyas.E3]; összegyűjté (24) → összegyűjt [mult.targyas.E3]; elvégezé (23) → elvégez [mult.targyas.E3]; imádkozék (23) → imádkozik [mult.E1]; felgerjede (22) → felgerjed [mult.alanyi.E3]; hagyá (22) → hagy [mult.targyas.E3]; teremté (22) → teremt [mult.targyas.E3]; elfutának (21) → elfut [mult.T3]; jutának (21) → jut [mult.T3]; kéré (21) → kér [mult.targyas.E3]; akarván (20) → akar [hatarozoi_igenev]; beborítá (20) → beborít [mult.targyas.E3]; hallék (20) → hall [mult.E1]; helyhezteté (19) → helyheztet [mult.targyas.E3]; illeté (19) → illet [mult.targyas.E3]; küldének (19) → küld [mult.T3]; megfogván (19) → megfog [hatarozoi_igenev]; megnyitá (19) → megnyit [mult.targyas.E3]; megszaggatá (19) → megszaggat [mult.targyas.E3]; szülé (19) → szül [mult.targyas.E3]; áldozának (19) → áldoz [mult.T3]; elfuta (18) → elfut [mult.alanyi.E3]; hallá (18) → hall [mult.targyas.E3]; kérék (18) → kér [mult.E1]; leborula (18) → leborul [mult.alanyi.E3]; szűlé (18) → szül [mult.targyas.E3]; találá (18) → talál [mult.targyas.E3]; vetének (18) → vet [mult.T3]; érkezék (18) → érkezik [mult.E1]; bízzál (17) → bízik [felszolito.E2]; hívatá (17) → hívat [mult.targyas.E3]; követék (17) → követ [mult.E1]; megemészté (17) → megemészt [mult.targyas.E3]; megfélemlének (17) → megféleml [mult.T3]; nevezék (17) → nevez [mult.E1]; összegyűlének (17) → összegyűl [mult.T3]; bocsátá (16) → bocsát [mult.targyas.E3]; izenvén (15) → izen [hatarozoi_igenev]; járván (15) → jár [hatarozoi_igenev]; kinyújtá (15) → kinyújt [mult.targyas.E3]; lakozának (15) → lakozik [mult.T3]; leborulának (15) → leborul [mult.T3]; megcsókolá (15) → megcsókol [mult.targyas.E3]; meghalának (15) → meghal [mult.T3]; megméré (15) → megmér [mult.targyas.E3]; megállának (15) → megáll [mult.T3]; felindítá (14) → felindít [mult.targyas.E3]; hivatá (14) → hivat [mult.targyas.E3]; hívá (14) → hív [mult.targyas.E3]; kezdék (14) → kezd [mult.E1]; megkérdezé (14) → megkérdez [mult.targyas.E3]; megkérdezék (14) → megkérdez [mult.E1]; méré (14) → mér [mult.targyas.E3]; tartózkodék (14) → tartózkodik [mult.E1]; elbeszélék (13) → elbeszél [mult.E1]; ismeré (13) → ismer [mult.targyas.E3]; kezdének (13) → kezd [mult.T3]; követvén (13) → követ [hatarozoi_igenev]; küldé (13) → küld [mult.targyas.E3]; maradának (13) → marad [mult.T3]; megdorgálá (13) → megdorgál [mult.targyas.E3]; meggyógyítá (13) → meggyógyít [mult.targyas.E3]; meghallgatá (13) → meghallgat [mult.targyas.E3]; megkérdék (13) → megkérd [mult.E1]; megszabadítá (13) → megszabadít [mult.targyas.E3]; megtelék (13) → megtel [mult.E1]; vetvén (13) → vet [hatarozoi_igenev]; élvén (13) → él [hatarozoi_igenev]; ejté (12) → ejt [mult.targyas.E3]; elküldvén (12) → elküld [hatarozoi_igenev]; elküldék (12) → elküld [mult.E1]; elrejté (12) → elrejt [mult.targyas.E3]; felelék (12) → felel [mult.E1]; felállítá (12) → felállít [mult.targyas.E3]; fölkele (12) → fölkel [mult.alanyi.E3]; járának (12) → jár [mult.T3]; kitölté (12) → kitölt [mult.targyas.E3]; kiűzé (12) → kiűz [mult.targyas.E3]; kérvén (12) → kér [hatarozoi_igenev]; megcsinálá (12) → megcsinál [mult.targyas.E3]; meghagyá (12) → meghagy [mult.targyas.E3]; meglátván (12) → meglát [hatarozoi_igenev]; megverék (12) → megver [mult.E1]; találának (12) → talál [mult.T3]; tanítván (12) → tanít [hatarozoi_igenev]; állítá (12) → állít [mult.targyas.E3]; egybegyűle (11) → egybegyül [mult.alanyi.E3]; elfoglalá (11) → elfoglal [mult.targyas.E3]; fogadá (11) → fogad [mult.targyas.E3]; hallgatának (11) → hallgat [mult.T3]; javítgata (11) → javítgat [mult.alanyi.E3]; kiáltván (11) → kiált [hatarozoi_igenev]; levágá (11) → levág [mult.targyas.E3]; leülvén (11) → leül [hatarozoi_igenev]; megerősíté (11) → megerősít [mult.targyas.E3]; megfogá (11) → megfog [mult.targyas.E3]; megmutatá (11) → megmutat [mult.targyas.E3]; megszámlálá (11) → megszámlál [mult.targyas.E3]; megölvén (11) → megöl [hatarozoi_igenev]; szállának (11) → száll [mult.T3]; tartván (11) → tart [hatarozoi_igenev]; építének (11) → épít [mult.T3]; adál (10) → ad [mult.E2]; csinálá (10) → csinál [mult.targyas.E3]; egybegyűlének (10) → egybegyűl [mult.T3]; elhozá (10) → elhoz [mult.targyas.E3]; elkezdé (10) → elkezd [mult.targyas.E3]; elálmélkodának (10) → elálmélkodik [mult.T3]; fogá (10) → fog [mult.targyas.E3]; fordulván (10) → fordul [hatarozoi_igenev]; gondolá (10) → gondol [mult.targyas.E3]; hozá (10) → hoz [mult.targyas.E3]; kinyujtá (10) → kinyujt [mult.targyas.E3]; lakék (10) → lakik [mult.E1]; látszék (10) → látsz [mult.E1]; megemlékezék (10) → megemlékezik [mult.E1]; megfordulván (10) → megfordul [hatarozoi_igenev]; megjelenté (10) → megjelent [mult.targyas.E3]; megrémülének (10) → megrémül [mult.T3]; megtérének (10) → megtér [mult.T3]; megállván (10) → megáll [hatarozoi_igenev]; növekedék (10) → növekedik [mult.E1]; találtatának (10) → találtat [mult.T3]; távozék (10) → távoz [mult.E1]; tölté (10) → tölt [mult.targyas.E3]; állván (10) → áll [hatarozoi_igenev]; betölté (9) → betölt [mult.targyas.E3]; csináltata (9) → csináltat [mult.alanyi.E3]; egybegyűjté (9) → egybegyűjtik [mult.targyas.E3]; elfüstölögteté (9) → elfüstölögtet [mult.targyas.E3]; elhagyván (9) → elhagy [hatarozoi_igenev]; elveté (9) → elvet [mult.targyas.E3]; előszólítván (9) → előszólít [hatarozoi_igenev]; engedé (9) → enged [mult.targyas.E3]; esének (9) → esik [mult.T3]; fordulának (9) → fordul [mult.T3]; gondolván (9) → gondol [hatarozoi_igenev]; hadakozék (9) → hadakozik [mult.E1]; helyezteté (9) → helyeztet [mult.targyas.E3]; helyezék (9) → helyez [mult.E1]

scope=a teljes Károli korpusz-lexikona (62869 kisbetűsített alak) | forras=eszkozok/szoto/regies_felismeres.py + hibrid_v2.py (sha256:864d6876437a) + hibrid.py (sha256:682e83127d2b) + karoli_lexikon.tsv (sha256:215f687f5d68) | ts=2026-10-13T13:45Z

### 11.5 A teljes Károli: v2 → v3 változás és 30 véletlen változás kézi listája

A teljes Károli 61673 alakjából **4605** alak kimenete változott (v2 A → v3 A), 13740 előfordulás.

| # | alak | előfordulás | v2 | v3 | kézi ítélet (manual) |
|---|---|---|---|---|---|
| 1 | babiloniai | 1 | Babilon | babiloniai | jobb (-i képzős melléknév) |
| 2 | bíráskodék | 2 | bír | bíráskodik | jobb |
| 3 | cselekedtetek-é | 2 | cselekedtetek-É | cselekedik | jobb |
| 4 | elfelejtkezzék | 1 | elfelejtkezzék | elfelejtkezik | jobb |
| 5 | eltávozhatnám | 1 | eltávozhatnám | eltávozik | részben jobb (DT130 (10): eltávozhat lenne; az alapige helyes) |
| 6 | elátkozom | 2 | elátkozom | elátkoz | jobb |
| 7 | felindíttatván | 1 | felindíttat | felindíttatván | rosszabb (a ritka műveltető -ván alakja igazolatlan) |
| 8 | feltátom | 1 | feltátom | feltát | jobb |
| 9 | fonál | 1 | fon | fonál | jobb |
| 10 | hamisságukat | 2 | hamis | hamisság | jobb |
| 11 | háborgatása | 2 | háborgat | háborgatás | jobb |
| 12 | hívatni | 2 | hívatni | hívatik | semleges (mindkettő hibás: hívat) |
| 13 | járjatok | 31 | járj | jár | jobb |
| 14 | jövendölgetnek | 1 | jövendölgetnek | jövendölget | jobb |
| 15 | kezdjétek | 1 | kéz | kezd | jobb |
| 16 | kisarjadt | 1 | kisarjadt | kisarjad | jobb |
| 17 | megholtaké | 1 | megholtak | meghal | semleges (megholt lenne) |
| 18 | megidősödtél | 1 | megidősödtél | megidősöd | részben jobb (megidősödik) |
| 19 | meglehet | 4 | megvan | meglehet | jobb |
| 20 | napjaimban | 2 | napjai | nap | jobb |
| 21 | paráználkodott | 8 | paráználkodott | paráználkodik | jobb |
| 22 | pikkelye | 5 | pikkely | pikkelye | rosszabb (pikkely; a v2 a hamis régies-ige úton jutott rá) |
| 23 | szidalmazhatja | 1 | szidalmazhatja | szidalmazhat | jobb |
| 24 | szorongatásnak | 3 | szorongat | szorongatás | jobb |
| 25 | takarhatja | 1 | takar | takarhat | jobb |
| 26 | tapodja | 6 | tapodja | tapod | jobb |
| 27 | tartod-é | 3 | tartod-É | tart | jobb |
| 28 | táplálására | 1 | táplál | táplálás | jobb |
| 29 | övezkedjenek | 1 | övezkedjen | övezked | részben jobb (övezkedik) |
| 30 | üssétek | 1 | üss | üt | jobb |

scope=a korpusz-lexikon kisbetűs és mondat belsejében nagybetűs alakjai | forras=eszkozok/szoto/valtozas_v2_v3.py (mag 20261013) + hibrid_v2.py (sha256:864d6876437a) + hibrid.py (sha256:682e83127d2b) + karoli_lexikon.tsv (sha256:215f687f5d68) | ts=2026-10-13T13:46Z

Összesítés (manual): 24 jobb, 2 részben jobb, 2 semleges (mindkét változat hibás), 2 rosszabb.

### 11.6 Ismert korlátok (nem javítva, a 4. mintás mérés előtt)

- a szigorítás ára a ritka igéken (más igei alak nélkül): *mélyede, felindíttatván, sírának* (homográf névszóval); a C-ben *leheletének*;
- a simplemma-ág hibái az A-ban: *bűn → bű*, *hasának → hasa*;
- *látszék → látsz* (a *látsz* a *lát* E/2-je is), *egybegyűle → egybegyül* (az *űle → üle* szabály a *gyűl* hosszú ű-jét is rövidíti), passzív/műveltető kétértelműség (*hívatni → hívatik*);
- a `szotari_alak` Károli-írásmódja a helyesírási szabályok visszafordításával közelített (`_VISSZA`), nem minden esetben pontos;
- a különálló igekötő (N-F94a, N-F94d) nem kezelt.

### 11.7 A v3 befagyasztása (a .3 mintavétele előtt)

*proveniencia: scope=hibrid v3 | forras=a repó fájljai (sha256, LF sorvégekkel, ahogy a git tárolja) | ts=2026-10-13*

| fájl | sha256 |
|---|---|
| `eszkozok/szoto/hibrid.py` (v3) | `682e83127d2bc2e7dd81ed68308b016f157bf6e878f855caf2f5a27142ab003c` (git blob `458b5ea5b5976aba6e4b2d6e9c735459e660b686`) |
| `adat/szoto/gyakori_alakok.tsv` (K tábla, a felhasználó átnézése előtt) | `7c7160343b55c07df1c21171215bc2ae9c6ca17dfff61d9f9d18a2d89eacebc6` |
| `adat/szoto/karoli_lexikon.tsv` | `215f687f5d68eff664da51bd4884a25ef927c1f67131e60ce5114faaee239215` |
| `eszkozok/szoto/hibrid_v2.py` (összevetéshez) | `864d6876437a468ccda04a243c5ee2926c0e2cd6460b35652b1c31389835d204` |

A 4. minta mintavétele és a modell-javaslatok ezután készülnek, a hibrid futtatása előtt (F94.3).


## 12. A negyedik (független) minta (F94.3/1–2) ⛔

*proveniencia: scope=5Móz, 1Sám, Péld, Ez, Mk, Ján, Róm, Jel Károli-szóalakjai, az 1–3. minta alakjai nélkül, rétegzett, mag 20261013 | forras=konkordancia/Karoli_1908.tsv + eszkozok/szoto/minta4_jeloltek.py (mintavétel) + manual (a szótári alak modell-javaslat, eszkozok/szoto/minta4_ir.py) | ts=2026-10-13*

- **Sorrend:** a v3 befagyasztása (11.7) után a mintavétel, utána a modell-javaslatok a példavers alapján; **a hibridet és a simplemmát a 4. minta alakjain nem futtattam.**
- **Mintavétel:** a 3. minta mintavevőjével azonos rétegszabályok és rétegen belüli gyakoriság-rétegzés; 113 alak (gyakori 25, ragos névszó 35, régies ige 20, régies helyesírás 12, mai igealak 13, tulajdonnév 8). A nyolc könyvben 20 838 alak, 60 945 token.
- **A tábla:** `adat/szoto/szoto_minta_4_fuggetlen.tsv` (SEMA 2.27). `ellenorzes=modell_ellenorizetlen` minden sorban; **a felhasználó soronként ellenőrzi, és ő írja `felhasznalo`-ra; a mérés csak a `felhasznalo` sorokon fut** (`meres.py --csak-felhasznalo`). 7 sor `[bizonytalan: …]` jelölésű (Filiszteusok, Girzeusokat: a népnév szótári alaka; elfeledték: elfeled/elfelejt; összegyűlekezének: mai írásmód; mikre: mi/ami; felingereltessenek: szenvedő/műveltető; bízott: bíz/bízik). A `strong` a repó párosításából (5Móz, 1Sám, Péld, Ez; 82 sor); az Mk, Ján, Róm, Jel nincs párosítva.
- **Átfedés a K táblával (fontos a C+K méréséhez):** a 4. minta 20 alakja (mind a gyakori rétegben: *hanem, közül, által, azon, Akkor, sok, többé, oda, se, jó, két, valaki, maga, hét, hol, most, hozzám, sing, volna, senki*) a K tábla sora is, és a két javaslat szótári alakja azonos (ugyanaz a modell írta mindkettőt). Ez a minta súlyának **73%-a** (2 221 / 3 053 előfordulás). A C+K súlyozott M1-e a 4. mintán ezért nagyrészt a K-sorok és a mintasorok egyezésén múlik; független ellenőrzést a felhasználó átnézése ad (a K táblát és a 4. mintát együtt nézi). Javaslat: a mérés a C+K-t a K-sorok nélkül is kiírja (alakonként és súlyozva).
- **A v3 fejlesztése közben már látott alakok:** *többé* (K6-lista, 30-as változásminta, K tábla), *tartózkodék* (K6-lista), valamint két, a végleges listákban már nem szereplő, de egy korábbi 30-as változásmintában látott alak: *szombatimat* (a „-i csak magánhangzó után” szabály visszavonásakor), *tévelyedjék*. A mérésben ezek külön jelölhetők.
- **Megfigyelés (nem javítva, a v3 befagyasztva):** az -ik-es igék régies múlt **E/3**-a is *-ék* (*tartózkodék, uralkodék, lakozék, esék*: „Saul … tartózkodék”), a v3 viszont minden *-ék*-et `mult.E1` jeggyel lát el (*láték* = láttam, helyes). A jegy -ik-es igénél hibás; javítás a 4. mintás mérés után (N-F94e).
- **A K4 számeltérése:** a v3-ban 30 `korpusz_strong` + 1 `manual` + 22 `modell_ellenorizetlen` (a 10. szakasz repó-alapú szabályellenőrzése és a *cz → c* utasítás szerint), a brief K4-e 34-et írt (az előmérés száma). Döntés: DT-F94d.


## 13. A felhasználó döntései (2026-10-13) a 4. mintán, a DT-F94d és a mérési iránymutatás

### 13.1 A 4. minta hét bizonytalan sora

*proveniencia: scope=adat/szoto/szoto_minta_4_fuggetlen.tsv, 7 sor | forras=manual (a felhasználó döntése, chat, 2026-10-13; alkalmazás: eszkozok/szoto/minta4_javit.py, idempotens) | ts=2026-10-13*

`ellenorzes=felhasznalo` lett, a `[bizonytalan: …]` helyén `[döntés: …]`: *Filiszteusok* (Filiszteus, további: Filiszteusok), *Girzeusokat* (Girzeus, további: Girzeusok), *összegyűlekezének* (összegyűlekezik / összegyülekezik, alapige gyülekezik), *elfeledték* (elfeled / elfelejt, alapige feled), *mikre* (mi / ami; a `tovabbi_elfogadhato` ürítve, mert azonos a szótári alakkal), *felingereltessenek* (felingereltetik, alapige ingerel; kategória `ragos_nevszo` → `regies_ige`), *bízott* (bíz, további: bízik). A többi 106 sor `modell_ellenorizetlen` maradt; az átnézésük a felhasználónál van. A `minta4_ir.py` ezentúl nem írja felül a meglévő mintát (`--felulir` nélkül hibával áll meg), és a *mikre* javaslata is ürített `tovabbi`-val szerepel benne.

**A rétegzés:** a mintavételt nem érinti (a rétegenkénti húzás a jelölt-listán már megtörtént: 35 ragos névszó, 20 régies ige), de a rétegenkénti kiírás 34 / 21 lesz. A SEMA 2.27 szerint a `kategoria` a **mintavételi réteg**, nem a helyes elemzés; a 4. mintában további 17 sor rétege tér el az elemzéstől: a `regies_ige` rétegben névszó *ötvenedesekké, házánál, veszszejévé, fügefának, hosszútűrésénél, kárbunkulusoknál*; a `ragos_nevszo` rétegben ige *összehívá, hunyorgat, hívogatnak, megtére, törekesznek, vehet, kivánnak, keresztülszúrjanak, múlnak, űzzenek*; az `ige_mai_alak` rétegben névszó *dolgotok, jóakaratja, szegénységök*; a `tulajdonnev` rétegben ige *Üldözzem-é* (ugyanez a jelenség a 3. mintában is: *adának, készítének* a ragos névszó rétegben). Javaslat (modell): a mérés rétegenkénti számai a mintavételi rétegre vonatkozzanak (a 3. mintával összevethetően), és a *felingereltessenek* visszakerüljön a `ragos_nevszo` rétegbe; vagy egységesen mind a 18 sor átsorolódjon elemzés szerinti rétegbe. A felhasználó dönt; addig a döntése szerinti egy átsorolás áll.

### 13.2 DT-F94d: a K4 szabályszáma

**a) Az összeg.** 30 + 1 + 22 = **53** szabály = 9 helyesírási + **44** tőváltó. Az előmérés 51 szabálya 9 + 42 volt; a v3 két új tőváltót vett fel (*kötel- → kötél*, *atyj- → atya*; 11.2, a v2 ismert hibáiból: *köteleid → kötelei*, *atyámnak → atyám*). A két új szabályt a szabályellenőrzés (10. szakasz) még nem mérte (az a v2 szabálylistáján futott), ezért `modell_ellenorizetlen`. Az 51 eredeti szabály: 30 `korpusz_strong` + 1 `manual` + 20 `modell_ellenorizetlen`.

**b) A 34 → 30 eltérés szabályonként.** Az előmérés 34 alátámasztott szabályából négy nem `korpusz_strong` a v3-ban:

| szabály | Strong-támasz az előmérésben (`token_karoli`, ÓSZ) | a repó párosításában (`adat/karoli_strong`, 57 könyv) | minősítés most | a v3 jelölése | ok |
|---|---|---|---|---|---|
| körűl → körül | 71% (22/31) | 67% (22/33) | gyenge | `modell_ellenorizetlen` | a 70%-os küszöb alá esett: a régi alakoknak 2-vel több Strong-párja van, egyik sem az új alak fő Strongja |
| nyny → nny | 71% (52/73) | 65% (53/82) | gyenge | `modell_ellenorizetlen` | a bővebb (ÚSZ-levelekkel bővült) és más párosítás 9 új párt adott, ebből 1 támasztja alá |
| ^setét → sötét | 72% (31/43) | 67% (29/43) | gyenge | `modell_ellenorizetlen` | azonos párszám, 2 pár más Stronghoz került a #22 párosításában |
| cz → c | 97% (30/31) | 97% (30/31) | alátámasztva | `manual` | a felhasználó utasítása (7.3): a 759 cz-alakból csak 5-nek van c-s párja, a korpusz érdemben nem igazolja; általános helyesírás-történeti tudás |

Mindhárom átsorolt szabály a 70%-os küszöb közelében (65–72%) volt; az ok a párosítás cseréje (a régi `token_karoli` helyett a repó #22-párosítása, pl. a 6.1-ben javított téves párok) és a hatókör bővülése, nem a szabály változása. (A *értelm- → értelem* a gyenge sávból az ellentmondóba került, a jelölése mindkét esetben `modell_ellenorizetlen`.) A DT-F94d a felhasználó döntésével 🟢 (adatréteg-elsőbbség).

### 13.3 Mérési iránymutatás (a mérés még nem indult)

*A felhasználó döntése (2026-10-13):* a DT-F94c döntő száma a 4. mintán **a K tábla alakjai nélküli** M1 (alakonként és súlyozva), nem kiegészítő szám; a fejlesztés közben látott négy alak (*többé, tartózkodék, szombatimat, tévelyedjék*) nélküli szám is a naplóba kerül. A `meres.py --fuggetlen` mindhárom halmazt kiírja: (1) a K tábla alakjai nélkül — **döntő**; (2) a K tábla alakjai és a látott alakok nélkül; (3) minden sor (tájékoztató). A mérés a `--csak-felhasznalo` kapcsolóval, a felhasználó átnézése után fut.

**Figyelem (manual, a kód próbája a 3. mintán):** a K tábla alakjai nélküli halmazon a C+K **szükségszerűen azonos a C-vel**, mert a K tábla csak a saját alakjaira hat (a 3. mintán: K nélkül C = C+K = 73% / 92,3%, 90 alak). A döntő szám tehát az A (simplemmával) és a C (simplemma és K nélkül) összevetése a nem-K sorokon; a K tábla hozzájárulása csak a K-sorokon mérhető, azokat pedig a mintával együtt ugyanaz a modell írta, ezért ott a független ellenőrzés a felhasználó soronkénti átnézése.


## 14. A felhasználói átnézés alkalmazása, megfigyelések (F94.3, 2026-10-13)

*proveniencia: scope=a 4. minta 113 sora és a K tábla 400 sora | forras=felhasználói átnézés, áttekintő oldal (https://claude.ai/artifact/PvJ8YFw3y561Nku1xwBdkr), 2026-10-13 | ts=2026-10-13T15:10Z*

- **4. minta:** mind a 113 sor `ellenorzes=felhasznalo` (`minta4_javit.py`, idempotens); a 106 sor változatlan, a 7 korábban eldöntött sor marad. A *felingereltessenek* kategóriája visszakerült a mintavételi rétegre (`ragos_nevszo`): a rétegek 25 / 35 / 20 / 12 / 13 / 8, a mintavétel szerint. A 13.1-ben listázott 18 sor elemzés szerinti rétege csak ott, a naplóban szerepel (külön oszlop nincs).
- **K tábla:** mind a 400 sor `ellenorzes=felhasznalo` (`k_tabla_epit.py --felhasznalo-atnezte …`, a proveniencia-sor a fájlban); két sor változott a `JAVASLAT`-ban: *mit* (rang 55) és *miket* (rang 366) `tovabbi_elfogadhato = ami` (a Károli „a mit” szerkezetében vonatkozó névmás). A felhasználó külön megvizsgálta és a javaslat mellett hagyta: *vala/valának → van*, *monda → mond*, *ki* (további: aki), *vagy* (további: van).
- **A *vagy* a repó párosításában** (`adat/karoli_strong/parok_*.tsv`, a parok-fájlok együttes sha256-ja `bb482963c328`; modell-kimenet, javaslat): 603 párosított *vagy*-token. Kötőszói Strong: kb. 483 (H0176 263, H9002 118, H0518 43, G2228 35, H0518+H9002 9, H9001 6, H3588+H9002 3, H2006 3, G2532 2, H5704+H9002 1); kérdő partikula (H9008): 5; **létige-olvasat** kb. 77 — főként a névszói mondat névmási alanyán (H0859 50, H0859+H8033 1, H1931 11, H1932 3, H9031 2, H9021 1), igei Stronggal (H1961 4, G1510 5); egyéb 12 (H9042 4, H9005 2, H3302 2, H1819 2, H0413 1, H9041 1); a maradék 26 token ritka kombináció. A felhasználó becslése (kb. 480 / 64) nagyságrendben egyezik; a létige-olvasat a pontosabb számlálással 77.
- **N-F94f (új nyitott tétel, megfigyelés, javítás nélkül): a különírt vonatkozó névmás.** A Károli a vonatkozó névmást többnyire két szóban írja („a ki”, „a mely”, „a mit”); a tövezés alakonként megy, ezért a különírt *a* névelőként kap szótári alakot, holott a vonatkozó névmás (aki, amely, ami) része, és az *amely*-re keresve az *a* token nem jelenik meg. Gyakoriság (`eszkozok/szoto/kulonirt_vonatkozo.py`, heurisztika, manual):

| család | különírt („a” + névmás), felső | alsó (a „mi” birtokos nélkül) | egybeírt (aki-, amely-, ami-) | példa |
|---|---|---|---|---|
| ki- | 5282 | 5282 | 17 | 1Móz 2:8 „a kit” |
| mely- | 1565 | 1565 | 11 | 1Móz 1:6 „a mely” |
| mi- | 1987 | 1425 | 8 | 1Móz 1:26 „a mi” |
| **összesen** | **8834** | **8272** | **36** | |

scope=OT+NT-full | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + eszkozok/szoto/kulonirt_vonatkozo.py (heurisztika, manual megfigyelés) | ts=2026-10-13T15:15Z

  A „ki” családban a felső becslés kevés igekötői *ki*-t is tartalmazhat („a ki…” igekötő + ige ritka). Rokona: N-F94d (hátravetett igekötő), N-F94a (különálló igekötő).


## 15. Mérés a 4. (független, felhasználó által ellenőrzött) mintán: M1, M2, K3 (F94.3/4)

*Futtatókörnyezet: WSL (Ubuntu), Python 3.11.17, simplemma 2.0.0 a helyi csomagkönyvtárból PYTHONPATH-on (új letöltés nincs; a `hu.plzma` sha256-ja a proveniencia-sorokban). A hibrid a befagyasztott v3 (`hibrid.py` sha256 `682e83127d2b…`, 11.7). A K tábla sha256-ja a befagyasztáskori `7c7160343b55`-ről `a5d9ad94273e`-re változott, mert a felhasználó a *mit* és a *miket* `tovabbi_elfogadhato`-ját javította, és minden sor `ellenorzes`-e `felhasznalo` lett; a hibrid a K táblából csak a `szotari_alak`-ot használja, az nem változott, így a C+K kimenete a befagyasztotthoz képest azonos. A mérés mind a 113 soron (`--csak-felhasznalo`; mind `felhasznalo`).*

### 15.1 M1 — szótárialak-pontosság (`meres.py --fuggetlen --csak-felhasznalo`)

A DT-F94c döntő száma a K tábla alakjai nélküli halmaz (13.3); ezen a C+K szükségszerűen azonos a C-vel. A táblák oszlopai a mintavételi rétegek (13.1).

##### szoto_minta_4_fuggetlen.tsv — a K tábla alakjai NÉLKÜL — a DT-F94c DÖNTŐ száma (93 alak, 832 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 78% / 96.6% (73/93) | 100% / 100.0% (5/5) | 83% / 81.2% (29/35) | 70% / 81.2% (14/20) | 58% / 50.0% (7/12) | 92% / 96.7% (12/13) | 75% / 80.0% (6/8) |
| hibrid C | 60% / 94.6% (56/93) | 100% / 100.0% (5/5) | 66% / 68.8% (23/35) | 55% / 71.9% (11/20) | 33% / 33.3% (4/12) | 62% / 83.3% (8/13) | 62% / 73.3% (5/8) |
| hibrid CK | 60% / 94.6% (56/93) | 100% / 100.0% (5/5) | 66% / 68.8% (23/35) | 55% / 71.9% (11/20) | 33% / 33.3% (4/12) | 62% / 83.3% (8/13) | 62% / 73.3% (5/8) |
| simplemma | 55% / 74.8% (51/93) | 80% / 77.9% (4/5) | 60% / 54.2% (21/35) | 45% / 62.5% (9/20) | 17% / 11.1% (2/12) | 85% / 93.3% (11/13) | 50% / 60.0% (4/8) |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:17Z

##### szoto_minta_4_fuggetlen.tsv — a K tábla alakjai és a fejlesztés közben látott alakok (szombatimat, tartózkodék, tévelyedjék, többé) NÉLKÜL (90 alak, 819 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 79% / 96.7% (71/90) | 100% / 100.0% (5/5) | 82% / 80.0% (28/34) | 72% / 77.3% (13/18) | 58% / 50.0% (7/12) | 92% / 96.7% (12/13) | 75% / 80.0% (6/8) |
| hibrid C | 61% / 95.0% (55/90) | 100% / 100.0% (5/5) | 68% / 73.3% (23/34) | 56% / 63.6% (10/18) | 33% / 33.3% (4/12) | 62% / 83.3% (8/13) | 62% / 73.3% (5/8) |
| hibrid CK | 61% / 95.0% (55/90) | 100% / 100.0% (5/5) | 68% / 73.3% (23/34) | 56% / 63.6% (10/18) | 33% / 33.3% (4/12) | 62% / 83.3% (8/13) | 62% / 73.3% (5/8) |
| simplemma | 56% / 74.8% (50/90) | 80% / 77.9% (4/5) | 62% / 57.8% (21/34) | 44% / 50.0% (8/18) | 17% / 11.1% (2/12) | 85% / 93.3% (11/13) | 50% / 60.0% (4/8) |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:17Z

##### szoto_minta_4_fuggetlen.tsv — minden sor (a K tábla alakjaival; tájékoztató) (113 alak, 3053 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 81% / 95.7% (92/113) | 96% / 96.5% (24/25) | 83% / 81.2% (29/35) | 70% / 81.2% (14/20) | 58% / 50.0% (7/12) | 92% / 96.7% (12/13) | 75% / 80.0% (6/8) |
| hibrid C | 65% / 91.5% (74/113) | 92% / 92.7% (23/25) | 66% / 68.8% (23/35) | 55% / 71.9% (11/20) | 33% / 33.3% (4/12) | 62% / 83.3% (8/13) | 62% / 73.3% (5/8) |
| hibrid CK | 67% / 98.5% (76/113) | 100% / 100.0% (25/25) | 66% / 68.8% (23/35) | 55% / 71.9% (11/20) | 33% / 33.3% (4/12) | 62% / 83.3% (8/13) | 62% / 73.3% (5/8) |
| simplemma | 61% / 86.3% (69/113) | 88% / 87.6% (22/25) | 60% / 54.2% (21/35) | 45% / 62.5% (9/20) | 17% / 11.1% (2/12) | 85% / 93.3% (11/13) | 50% / 60.0% (4/8) |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:17Z

##### szoto_minta_4_fuggetlen.tsv — CSAK a K tábla alakjai (a C+K hozzájárulása; a K táblát a felhasználó ellenőrizte) (20 alak, 2221 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 95% / 95.4% (19/20) | 95% / 95.4% (19/20) | — | — | — | — | — |
| hibrid C | 90% / 90.4% (18/20) | 90% / 90.4% (18/20) | — | — | — | — | — |
| hibrid CK | 100% / 100.0% (20/20) | 100% / 100.0% (20/20) | — | — | — | — | — |
| simplemma | 90% / 90.6% (18/20) | 90% / 90.6% (18/20) | — | — | — | — | — |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:17Z

### 15.2 M2 — keresési találati arány (`meres_m2.py`, pooled célhalmaz, emMorph nélkül)

Definíció: a kód leírása (az előmérés újradefiniált M2-je, 2.3): a célhalmaz azok a párosított Károli-tokenek, amelyek alakját bármelyik elemző (hibrid A, C, CK, simplemma) a lemmára vezeti, és amelyek a lemma fő Strong-jához párosítottak vagy Strong nélküliek; (a) az elemző a lemmára vezeti, (b) … vagy az alak maga a lemma, (c) … vagy a token a fő Stronghoz párosított. Hatókör: a repó párosított könyvei (57 könyv; az Mk, Ján, Róm, Jel nincs párosítva). **Megjegyzés:** az M2-ben a K tábla a K-nélküli lemmák tokenjeire is hat (a K-ban szereplő ragozott alakok más lemmák célhalmazában is ott vannak), ezért a K nélküli lemmákon a C+K nem azonos a C-vel.

##### M2 — a minta minden lemmája: 99 lemma, célhalmaz 58027 token (célhalmaz nélküli lemma: 7: kárbunkulus, tévelyedik, jóna, béth-aven, girzeus, felingereltetik, nyiratkozik)

| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |
|---|---|---|---|---|---|
| hibrid A | 97.57% | 98.03% | 98.65% (57244/58027) | 91.6% | 99.0% |
| hibrid C | 91.01% | 91.01% | 94.70% (54953/58027) | 74.4% | 98.1% |
| hibrid CK | 95.87% | 95.87% | 98.40% (57097/58027) | 75.0% | 98.3% |

*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* se 0% / 100% (146, H3808); bíz 87% / 0% (38, H0982); űz 100% / 0% (29, H3423); kényszerít 100% / 0% (8, H7650); unoka 100% / 0% (8, H1121); láncz 83% / 0% (6, H8333); összegyűlekezik 33% / 0% (3, H6950); elhajt 100% / 0% (3, H3947); hosszútűrés 100% / 0% (2, G3326); hunyorgat 0% / 100% (2, H7169); hívogat 100% / 0% (2, H7121); keresztülszúr 100% / 0% (2, H1856)

##### M2 — a K tábla alakjai nélküli lemmák (a DT-F94c döntő halmaza): 79 lemma, célhalmaz 19645 token (célhalmaz nélküli lemma: 7: kárbunkulus, tévelyedik, jóna, béth-aven, girzeus, felingereltetik, nyiratkozik)

| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |
|---|---|---|---|---|---|
| hibrid A | 95.59% | 96.21% | 98.20% (19292/19645) | 90.7% | 99.1% |
| hibrid C | 89.65% | 89.65% | 97.60% (19173/19645) | 68.9% | 97.9% |
| hibrid CK | 91.77% | 91.77% | 98.02% (19257/19645) | 69.4% | 97.9% |

*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* bíz 87% / 0% (38, H0982); űz 100% / 0% (29, H3423); kényszerít 100% / 0% (8, H7650); unoka 100% / 0% (8, H1121); láncz 83% / 0% (6, H8333); összegyűlekezik 33% / 0% (3, H6950); elhajt 100% / 0% (3, H3947); hosszútűrés 100% / 0% (2, G3326); hunyorgat 0% / 100% (2, H7169); hívogat 100% / 0% (2, H7121); keresztülszúr 100% / 0% (2, H1856); ötvenedes 0% / 100% (1, H2572)

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) lemmái; a párosított Károli-könyvek (484820 hu token, 58041 alak) | forras=eszkozok/szoto/meres_m2.py + adat/karoli_strong/szavak_*.tsv (együttes sha256:c3266499df09; modell-kimenet, javaslat) + hibrid.py (v3, sha256:682e83127d2b) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:18Z

### 15.3 K3

Küszöb (brief K3, meresi_terv 4.): a 4. mintán súlyozva ≥ 90% (M1), és M2 (c) ≥ 98% a minta lemmáin.

| v3 változat | M1 súlyozva, K nélkül (döntő) | M1 súlyozva, minden sor | M2 (c), K nélküli lemmák | M2 (c), minden lemma | K3 |
|---|---|---|---|---|---|
| **A** (simplemmával) | 96,6% | 95,7% | 98,20% | 98,65% | **teljesül** |
| **C+K** (simplemma nélkül, K táblával) | 94,6% (= C) | 98,5% | 98,02% | 98,40% | **teljesül** (az M2 (c) a K nélküli lemmákon a küszöbön: 19 257 / 19 645) |
| **C** (simplemma és K nélkül) | 94,6% | 91,5% | 97,60% | 94,70% | **nem teljesül** (M2 (c)) |

A K3 a v3 A-ra és a v3 C+K-ra teljesül, a v3 C-re (K nélkül) nem. A döntő halmazon az A és a C különbsége súlyozva 2,0 százalékpont (96,6% / 94,6%), **alakonként 18 százalékpont** (78% / 60%). A különbség a ritka alakokon van: ragos névszó 83% / 66%, régies ige 70% / 55%, régies helyesírás 58% / 33%, mai igealak 92% / 62% (alakonként). M2 (a), K nélküli lemmák: A 95,6%, C+K 91,8%, C 89,7%. A simplemma önmagában a döntő halmazon 55% / 74,8%.

### 15.4 Olvasat (manual, nem döntés)

- A C+K-val (a simplemma nélkül) a K3 teljesül, tehát a 2. lehetőség (a simplemma csak fejlesztési mérce) a küszöb szerint járható. Az M2 (c) azonban a döntő halmazon épp a határon van (98,02%), és a ritka alakokon a C/C+K alakonként jóval gyengébb az A-nál.
- A C-ben a gyenge rétegek (régies helyesírás 33%, ritka ragos névszó, mai igealak) saját szabályokkal javíthatók lennének, de **ugyanerre a mintára nem hangolok** (brief K3); egy javítás új, független mérést kívánna.
- Az N-F94e (-ik-es igék *-ék* alakjának jegye) a döntéssel együtt javítandó (a v3 újbóli befagyasztásával).


## 16. DT-F94e: a kiadott hibrid a C+K; N-F94e; a v3 újbóli befagyasztása; a szótárialak-tábla; K1–K6 (F94.3)

### 16.1 A döntés (a felhasználó, 2026-10-13)

DT-F94e = 2.: **a kiadott hibrid a C+K, a simplemma csak fejlesztési mérce**; a DT-F94c ezzel végleges (mindkettő 🟢). A `licencek.tsv`: a `simplemma_nyelvi_adat` csak fejlesztési mérce, kiadásba nem kerül (ODbL 1.0, `tisztazott`; új címke a SEMA 2.19-ben); a `szoto_tablak` a repó saját adatlicence + a Károli 1908 (közkincs). Új nyitott tétel: N-F94g (a C+K ritka alakjai; javítás Hunspell-lel, külön licencdöntéssel, új ötödik mintán — nem a #94 része). `requirements.txt`: a simplemma csak fejlesztési függőség.

**Keresési mód (Kiegészítés B):** a C+K pontossága a (c) módra (szótári alak VAGY Strong) érvényes — M2 (c) a 4. mintán 98,4% (K nélküli lemmákon 98,0%); a tisztán szótári alakos keresésre (a) nem: a K nélküli lemmákon 91,8%. A `karoli_szotari_alak.tsv` fejléce és a zárójelentés ezt kimondja.

### 16.2 N-F94e és a determinizálás — a v3 újbóli befagyasztása

- **N-F94e (általános szabály):** a szabályág (R) *-ék* jegye -ik-es szótári alaknál `mult.E3` (*tartózkodék, uralkodék, esék, cselekedék*), egyébként `mult.E1` (*láték*); a kivételtábla saját jegyét nem írja felül. Csak a jegyet érinti, a szótári alakot nem. Megfigyelés (manual, nem javítva): magas hangrendű, nem -ik-es igénél az *-ék* a T/3 tárgyassal is egyezik (*kérék* = kértem / kérték; *kényszeríték őt*), ott a jegy szövegkörnyezet nélkül nem dönthető el. A 3. minta *cselekedék* indoklása E/1-et írt, a Jer 36:8 alanya Báruk (E/3) — az indoklás nem mért mező.
- **Determinizálás:** a `_nevszo_to` egy halmazt járt be (`{t, _hosszitas_vissza(t)}`), amelynek sorrendje a Python string-hash véletlenítése miatt futásonként változott, és egyenlő jelöltek között döntött (a teljes Károlin 4 alak: *emelém, tudnád, tudnám, Összehajtám*). Rendezett bejárásra javítva; a tábla két hash-maggal és Python 3.14 / 3.11 alatt bájtra azonos. A `hibrid_v2.py` (befagyasztott összevetési másolat) és az előmérés v2-je ugyanezt a hibát hordozza; a K2 bitre egyezett, a v2 nem kerül kiadásra.
- **Újbóli befagyasztás:** `eszkozok/szoto/hibrid.py` sha256 `74d0ebe5062240857355ae49480375d3648cc7747eeff49811702c775d8c89ed` (git blob `e1d9d91c59b8b1509c8a273c98253f19156e544e`); K tábla `a5d9ad94273e0db5a29b7acbba0532758db0e68eb743334000ac3f7d17494f65`; lexikon `215f687f5d68…` (változatlan).

### 16.3 Regresszió és a 4. minta mérésének frissítése

**A 4. minta a mérés és a fenti javítások után fejlesztési halmaz; az erre a v3-ra kapott eredmény már nem független** (brief .3/4). A javítások a szótári alakot a három fejlesztési mintán nem változtatták:

##### szoto_minta_1_fejlesztes.tsv (213 alak, 6375 előfordulás)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 97% / 99.4% (206/213) | 98% / 99.6% (54/55) | 98% / 99.1% (64/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 86% / 89.5% (6/7) | 100% / 100.0% (27/27) |
| hibrid C | 85% / 94.3% (182/213) | 89% / 95.0% (49/55) | 82% / 82.2% (53/65) | 87% / 93.9% (39/45) | 79% / 88.2% (11/14) | 43% / 52.6% (3/7) | 100% / 100.0% (27/27) |
| hibrid CK | 91% / 99.0% (193/213) | 100% / 100.0% (55/55) | 89% / 93.0% (58/65) | 87% / 93.9% (39/45) | 79% / 88.2% (11/14) | 43% / 52.6% (3/7) | 100% / 100.0% (27/27) |
| v2 A | 95% / 99.2% (203/213) | 98% / 99.6% (54/55) | 95% / 96.6% (62/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 71% / 78.9% (5/7) | 100% / 100.0% (27/27) |
| v2 C | 79% / 92.6% (169/213) | 85% / 93.8% (47/55) | 71% / 73.6% (46/65) | 80% / 88.6% (36/45) | 79% / 88.2% (11/14) | 29% / 42.1% (2/7) | 100% / 100.0% (27/27) |

scope=szoto_minta_1_fejlesztes.tsv (sha256:a7f8d65d42de) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:74d0ebe50622) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:38Z

##### szoto_minta_2_fejlesztes.tsv (180 alak, 1695 előfordulás)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 93% / 97.9% (167/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 90% / 91.0% (19/21) | 100% / 100.0% (10/10) |
| hibrid C | 84% / 87.8% (151/180) | 90% / 87.6% (36/40) | 84% / 86.5% (54/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 71% / 82.1% (15/21) | 100% / 100.0% (10/10) |
| hibrid CK | 87% / 96.0% (156/180) | 98% / 98.4% (39/40) | 88% / 92.1% (56/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 71% / 82.1% (15/21) | 100% / 100.0% (10/10) |
| v2 A | 92% / 97.6% (166/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 86% / 85.9% (18/21) | 100% / 100.0% (10/10) |
| v2 C | 80% / 85.8% (144/180) | 90% / 87.6% (36/40) | 78% / 76.7% (50/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 57% / 64.1% (12/21) | 100% / 100.0% (10/10) |

scope=szoto_minta_2_fejlesztes.tsv (sha256:587e47bded57) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:74d0ebe50622) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:38Z

##### szoto_minta_3_ellenorzott.tsv (113 alak, 3745 előfordulás)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 94% / 99.7% (106/113) | 100% / 100.0% (25/25) | 91% / 90.6% (32/35) | 100% / 100.0% (20/20) | 75% / 78.6% (9/12) | 100% / 100.0% (13/13) | 88% / 81.8% (7/8) |
| hibrid C | 76% / 91.3% (86/113) | 88% / 92.0% (22/25) | 71% / 78.1% (25/35) | 95% / 97.2% (19/20) | 25% / 28.6% (3/12) | 77% / 58.6% (10/13) | 88% / 81.8% (7/8) |
| hibrid CK | 79% / 99.0% (89/113) | 100% / 100.0% (25/25) | 71% / 78.1% (25/35) | 95% / 97.2% (19/20) | 25% / 28.6% (3/12) | 77% / 58.6% (10/13) | 88% / 81.8% (7/8) |
| v2 A | 80% / 99.1% (90/113) | 100% / 100.0% (25/25) | 80% / 84.4% (28/35) | 50% / 58.3% (10/20) | 67% / 71.4% (8/12) | 92% / 96.6% (12/13) | 88% / 81.8% (7/8) |
| v2 C | 56% / 90.3% (63/113) | 88% / 92.0% (22/25) | 51% / 62.5% (18/35) | 40% / 30.6% (8/20) | 17% / 21.4% (2/12) | 54% / 48.3% (7/13) | 75% / 72.7% (6/8) |

scope=szoto_minta_3_ellenorzott.tsv (sha256:bafc1e67a061) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:74d0ebe50622) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:38Z

Egyedi romlás a v2-höz képest (a regressziós szkript most a 4. mintát is látja):

```
szoto_minta_1_fejlesztes.tsv A ROMLÁS: —
szoto_minta_1_fejlesztes.tsv C ROMLÁS: —
szoto_minta_1_fejlesztes.tsv CK ROMLÁS: —
szoto_minta_2_fejlesztes.tsv A ROMLÁS: —
szoto_minta_2_fejlesztes.tsv C ROMLÁS: leheletének(ragos_nevszo,1): v2=lehelet v3=leheletének
szoto_minta_2_fejlesztes.tsv CK ROMLÁS: leheletének(ragos_nevszo,1): v2=lehelet v3=leheletének
szoto_minta_3_ellenorzott.tsv A ROMLÁS: —
szoto_minta_3_ellenorzott.tsv C ROMLÁS: —
szoto_minta_3_ellenorzott.tsv CK ROMLÁS: —
szoto_minta_4_fuggetlen.tsv A ROMLÁS: atyafiaival(ragos_nevszo,1): v2=atyafi v3=atyafiai
szoto_minta_4_fuggetlen.tsv C ROMLÁS: atyafiaival(ragos_nevszo,1): v2=atyafi v3=atyafiaival
szoto_minta_4_fuggetlen.tsv CK ROMLÁS: atyafiaival(ragos_nevszo,1): v2=atyafi v3=atyafiaival
```

Az *atyafiaival* (4. minta) a v3-ban az első befagyasztáskor is hibás volt (a 15. szakasz számai ezt már tartalmazzák); a *leheletének* a szigorítás ára (11.3).

A 4. minta M1-e változatlan (15.1); az M2 a determinizálás miatt a második tizedesben mozdult (C 89,65 → 89,66%, C+K 91,77 → 91,78% (a), lemmánkénti átlag A 90,7 → 90,8%), a (c) változatlan:

##### M2 — a minta minden lemmája: 99 lemma, célhalmaz 58027 token (célhalmaz nélküli lemma: 7: kárbunkulus, tévelyedik, jóna, béth-aven, girzeus, felingereltetik, nyiratkozik)

| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |
|---|---|---|---|---|---|
| hibrid A | 97.57% | 98.03% | 98.65% (57244/58027) | 91.6% | 99.0% |
| hibrid C | 91.01% | 91.01% | 94.70% (54953/58027) | 74.4% | 98.1% |
| hibrid CK | 95.87% | 95.87% | 98.40% (57097/58027) | 75.0% | 98.3% |

*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* se 0% / 100% (146, H3808); bíz 87% / 0% (38, H0982); űz 100% / 0% (29, H3423); kényszerít 100% / 0% (8, H7650); unoka 100% / 0% (8, H1121); láncz 83% / 0% (6, H8333); összegyűlekezik 33% / 0% (3, H0622); elhajt 100% / 0% (3, H3947); hosszútűrés 100% / 0% (2, G3326); hunyorgat 0% / 100% (2, H7169); hívogat 100% / 0% (2, H7121); keresztülszúr 100% / 0% (2, H1856)

##### M2 — a K tábla alakjai nélküli lemmák (a DT-F94c döntő halmaza): 79 lemma, célhalmaz 19645 token (célhalmaz nélküli lemma: 7: kárbunkulus, tévelyedik, jóna, béth-aven, girzeus, felingereltetik, nyiratkozik)

| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |
|---|---|---|---|---|---|
| hibrid A | 95.59% | 96.21% | 98.20% (19292/19645) | 90.8% | 99.1% |
| hibrid C | 89.66% | 89.66% | 97.60% (19173/19645) | 68.9% | 97.9% |
| hibrid CK | 91.78% | 91.78% | 98.02% (19257/19645) | 69.4% | 97.9% |

*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* bíz 87% / 0% (38, H0982); űz 100% / 0% (29, H3423); kényszerít 100% / 0% (8, H7650); unoka 100% / 0% (8, H1121); láncz 83% / 0% (6, H8333); összegyűlekezik 33% / 0% (3, H0622); elhajt 100% / 0% (3, H3947); hosszútűrés 100% / 0% (2, G3326); hunyorgat 0% / 100% (2, H7169); hívogat 100% / 0% (2, H7121); keresztülszúr 100% / 0% (2, H1856); ötvenedes 0% / 100% (1, H2572)

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) lemmái; a párosított Károli-könyvek (484820 hu token, 58041 alak) | forras=eszkozok/szoto/meres_m2.py + adat/karoli_strong/szavak_*.tsv (együttes sha256:c3266499df09; modell-kimenet, javaslat) + hibrid.py (v3, sha256:74d0ebe50622) + gyakori_alakok.tsv (sha256:a5d9ad94273e) + karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T15:39Z

### 16.4 A teljes Károli szótárialak-táblája

`adat/szoto/karoli_szotari_alak.tsv` (generált, `eszkozok/szoto/szotari_alak_epit.py`; sha256 `d757ba74a5b523cf98174d50af0876ae86e9342b915027a474533673450f989f`): 66 824 sor (a korpusz-lexikon minden írásmódja), a C+K változattal, **simplemma nélkül** — az előállító a simplemma importját letiltja, és hibával áll meg, ha egy sor `modszer=simplemma` lenne. Módszer: lexikon 43 672, szabály 14 931, név 6 772, K tábla 770, kivétel 679. `szabaly_forras`: üres 51 877, `modell_ellenorizetlen` 13 498, `manual` 733, `korpusz_strong` 716. `regies_jegy`: 3 297 sor (`mult.targyas.E3` 738, `hatarozoi_igenev` 690, `mult.T3` 551, `mult.alanyi.E3` 508, `mult.E1` 394, `mult.E3` 160, `felszolito.E2` 92, `mult.E2` 76, `mult.T1` 53, `mult.T2` 35), mind szabály-, kivétel- vagy K-sorban. **Ismert korlát (új, manual):** a régies E/1 tárgyas *-ám/-ém* (*emelém, összehajtám*) nincs a felismert végződések között.

### 16.5 K1–K6

| feltétel | állapot |
|---|---|
| K1 — a három régi minta a repóban, egységes sémával, soronként `ellenorzes`; az eltérés-lista naplózva és lezárva | **teljesül** (5., 5.1, 6. szakasz; DT-F94a/b 🟢; üres `ellenorzes` nincs) |
| K2 — az átvett v2 a három mintán bitre az előmérés M1-e | **teljesül** (9.1: 99,2 / 97,6 / 80% / 99,1%; 61 673 alakon azonos kimenet) |
| K3 — a 4. mintán súlyozva ≥ 90%, M2 (c) ≥ 98% | **teljesül a kiadott C+K-ra** (M1 súlyozva 98,5%, a döntő K nélküli halmazon 94,6%; M2 (c) 98,4%, K nélküli lemmákon 98,02% — a határon) és az A-ra; a C-re (K nélkül) nem (15.3) |
| K4 — minden szabály `szabaly_forras`; a simplemma adatlicence szó szerint idézve | **teljesül** a DT-F94d szerinti számmal (30 `korpusz_strong` + 1 `manual` + 22 `modell_ellenorizetlen`; a brief 34-e helyett, 13.2); idézet: `licencek.tsv` |
| K5 — emMorph-kód/-kimenet nincs; abszolút útvonal nincs; `csv` modul nincs; Python 3.11; CI zöld; független ellenőr eltérés nélkül zár | **teljesül** az ellenőrzött részekben (gépi keresés: nincs emMorph-fájl/-hivatkozás a kódban, nincs abszolút útvonal, nincs `csv`; Python 3.11.17 alatt a tábla bájtra azonos; a helyi CI-ellenőrző zöld); **a független ellenőrzés még hátra van** |
| K6 — 200 alakos kézi besorolás előtte/utána; utána nincs névszó régies igeként; a `regies_jegy` csak igei alakon | **teljesül a 200 leggyakoribb jegyes alakon** (pontosítva: 18.1, brief v1.2; a ritka alakokon ismert korlát, N-F94h) (11.4: előtte 74 / 200 nem ige, utána 0; a v2 74 nem-igéjéből a táblában egy sem kap jegyet; jegy csak szabály-, kivétel- és K-sorban) |


## 17. Az ELLENOR_F94 utáni javítás (F94.5; a felhasználó döntése, 2026-10-13: az (a) út)

*Ellenőri jelentés: `naplok/ELLENOR_F94.md` (7 eltérés). A javítások általános szabályok, nem alakokra szabva; kézi kivétel nincs.*

### 17.1 Licenc és proveniencia (2., 3., 5. eltérés)

- `simplemma_nyelvi_adat`: `kereskedelmi=igen` (az ODbL engedi), `allapot=tisztazatlan` (nem azonosított, melyik további adatforrás érinti a magyart), a sor kimondja: csak fejlesztési mérce, nem kerül kiadásra (DT-F94e). A SEMA 2.19 címkelistájába korábban felvett `ODbL 1.0` visszavonva (nem használt; a sor címkéje `tisztázatlan`).
- `szoto_tablak`: + TAHOT/TAGNT (CC BY 4.0, kötelező forrásmegjelöléssel; a minták `strong` oszlopa és a szabályellenőrzés az `adat/karoli_strong/`-ból); a simplemma csak mérésre szolgált, nem összetevő; ODbL-összetevő nincs.
- `k_tabla_epit.py` és a K tábla fejléce: a modell a kitöltés előtt látta a 9. szakasz A- (simplemmás) és C-hibalistáit (11.1); a szótári alakok nem a simplemma vagy a hibrid kimenetéből lettek átvéve (a hibalisták hibás kimeneteket mutattak, a K azoktól eltérő, DT130 szerinti alakot ad); mind a 400 sort a felhasználó ellenőrizte. A K sorai nem változtak.

### 17.2 K6: a 26 névszói alak (1. eltérés) és a javító szabályok

Ok (az ellenőr szerint): a C/C+K-ban a simplemmás -a/-e névszószűrő kiesett, és ritka névszónál a névszóval közös *-nak/-nek* attesztáció átengedte a tövet. Javítás (`hibrid.py`): **R1** — névszóképzős tő (-ság/-ség, -mány/-mény, -vány/-vény, -alom/-elem; -ás/-és, ha előtte igető áll vagy a tő legalább 6 betű) nem régies igető; **R2** — a birtokos névszó (a megnyújtott tő névszói raggal is áll, *felekezeté-ben*) nem -a/-e, -ának/-ének igealak; a C/C+K-ban az **-at/-et/-ot/-öt végű tőnél** a *-nak/-nek* attesztáció nem elég (kivéve a -hat/-het, -tat/-tet igeképzőt); a csupasz-tő lépés igevizsgálata csak szigorú igei alakot néz; simplemma nélkül az **-ás/-és/-ság/-ség képzős főnév** ragos alakja attesztáció nélkül is szótári alakot kap. (Egy közbülső változat — a *-nak/-nek* attesztáció teljes elhagyása a C/C+K-ban — a 2. minta régies ige rétegét a v2 alá vitte (*elhamvadának*), és a teljes Károlin 30 változásból 12 igét rontott; elvetve.)

A 26 sor a javítás előtt (a 6f6f5c32 táblája) és után (C+K):

| alak | előtte | utána |
|---|---|---|
| dicsekvésének | régi: dicsekvés, alapige —, szabaly, jegy mult.T3 | új: dicsekvés, alapige —, lexikon, jegy — |
| elnézése | régi: elnézés, alapige nézés, szabaly, jegy mult.alanyi.E3 | új: elnézés, alapige —, lexikon, jegy — |
| elnézésének | régi: elnézés, alapige nézés, szabaly, jegy mult.T3 | új: elnézés, alapige —, lexikon, jegy — |
| felekezete | régi: felekezet, alapige —, szabaly, jegy mult.alanyi.E3 | új: felekezet, alapige —, lexikon, jegy — |
| felekezetének | régi: felekezet, alapige —, szabaly, jegy mult.T3 | új: felekezet, alapige —, lexikon, jegy — |
| gyűlölése | régi: gyűlölés, alapige —, szabaly, jegy mult.alanyi.E3 | új: gyűlölés, alapige —, lexikon, jegy — |
| istensége | régi: istenség, alapige —, szabaly, jegy mult.alanyi.E3 | új: istenség, alapige —, lexikon, jegy — |
| jövendölése | régi: jövendölés, alapige —, szabaly, jegy mult.alanyi.E3 | új: jövendölés, alapige —, lexikon, jegy — |
| keresése | régi: keresés, alapige —, szabaly, jegy mult.alanyi.E3 | új: keresés, alapige —, lexikon, jegy — |
| körülmetéletlensége | régi: körülmetéletlenség, alapige —, szabaly, jegy mult.alanyi.E3 | új: körülmetéletlenség, alapige —, lexikon, jegy — |
| lakossága | régi: lakosság, alapige —, szabaly, jegy mult.alanyi.E3 | új: lakosság, alapige —, lexikon, jegy — |
| megfizetése | régi: megfizetés, alapige —, szabaly, jegy mult.alanyi.E3 | új: megfizetés, alapige —, lexikon, jegy — |
| megtisztulása | régi: megtisztulás, alapige tisztulás, szabaly, jegy mult.alanyi.E3 | új: megtisztulás, alapige —, lexikon, jegy — |
| megtisztulásának | régi: megtisztulás, alapige tisztulás, szabaly, jegy mult.T3 | új: megtisztulás, alapige —, lexikon, jegy — |
| megölése | régi: megölés, alapige —, szabaly, jegy mult.alanyi.E3 | új: megölés, alapige —, lexikon, jegy — |
| okossága | régi: okosság, alapige —, szabaly, jegy mult.alanyi.E3 | új: okosság, alapige —, lexikon, jegy — |
| restsége | régi: restség, alapige —, szabaly, jegy mult.alanyi.E3 | új: restség, alapige —, lexikon, jegy — |
| rettentése | régi: rettentés, alapige —, szabaly, jegy mult.alanyi.E3 | új: rettentés, alapige —, lexikon, jegy — |
| születése | régi: születés, alapige —, szabaly, jegy mult.alanyi.E3 | új: születés, alapige —, lexikon, jegy — |
| születésének | régi: születés, alapige —, szabaly, jegy mult.T3 | új: születés, alapige —, lexikon, jegy — |
| teremtésének | régi: teremtés, alapige —, szabaly, jegy mult.T3 | új: teremtés, alapige —, lexikon, jegy — |
| tisztulása | régi: tisztulás, alapige —, szabaly, jegy mult.alanyi.E3 | új: tisztulás, alapige —, lexikon, jegy — |
| tisztulásának | régi: tisztulás, alapige —, szabaly, jegy mult.T3 | új: tisztulás, alapige —, lexikon, jegy — |
| tudásának | régi: tudás, alapige —, szabaly, jegy mult.T3 | új: tudás, alapige —, lexikon, jegy — |
| ültetése | régi: ültetés, alapige —, szabaly, jegy mult.alanyi.E3 | új: ültetés, alapige —, lexikon, jegy — |
| ültetésének | régi: ültetés, alapige —, szabaly, jegy mult.T3 | új: ültetés, alapige —, lexikon, jegy — |

Mind a 26 jegy nélküli; az *elnézés → nézés* alapige is eltűnt. A szótári alak 26-ból 26 helyes (a *születése*, *dicsekvésének*, *elnézésének* a közbülső változatban rosszabb volt, a végleges szabályokkal helyes).

### 17.3 K6 a kiadott C+K-n: 200 leggyakoribb felismert régies igealak

*Előtte: a v2 C (simplemma nélkül, a szigorítás előtt); utána: a javított v3 C+K. A K tábla sorai (`modszer=k_tabla`) nem a szabályág felismerései, ezért nem szerepelnek (a K-t a felhasználó ellenőrizte). Besorolás: manual, modell: claude-opus-5-5.*

**Előtte (v2 C): 93 / 200 nem ige** (névszó, névutó, határozószó, névmás): maga, királya, hozzá, felé, többé, házának, háza, előtte, tiszta, királyának, népe, beszéde, mellé, ellene, közé, leánya, nemzetsége, szíve, utána, magának, felette, felesége, száma, dicsősége, halál, feje, fejére, angyala, helyette, népének, serege, sátorának, országa, sokasága, szája, továbbá, háznépe, vége, embere, része, leányának, szélessége, törvénye, felőle, közepette, mellette, zsoltára, vére, fölé, nemzetségének, szeme, feleségének, férje, határa, élete, általa, városa, életének, öröksége, helye, sátora, tele, gyülekezete, magassága, teste, emberének, földe, bűne, füle, nyilván, igazsága, fele, testvére, áldozata, földének, vezére, halála, maradéka, szövetségének, városának, dicsőségének, gyümölcse, seregének, éneke, este, hegye, nyelve, tanácsa, hosszúsága, kinél, lakosa, testvérének, testének. A többi ige (sok téves tővel: *mondjátok → mondj, adja → adj, felemelé → felemelik*).

mondván (1237) → mond; maga (400) → mag; szóla (382) → szól; királya (363) → király; hozzá (359) → hozz; felele (318) → felel; felé (304) → fel; többé (297) → több; házának (260) → ház; háza (235) → ház; előtte (188) → előtt; tiszta (183) → tiszt; királyának (182) → király; nemzé (175) → nemz; népe (171) → nép; beszéde (170) → beszéd; mellé (165) → mell; ellene (163) → ellen; közé (142) → köz; mondjátok (141) → mondj; leánya (140) → leány; adja (136) → adj; felelvén (123) → felel; meghala (118) → meghal; nemzetsége (115) → nemzetség; szíve (115) → szív; utána (115) → után; magának (109) → mag; felette (106) → felett; felesége (102) → feleség; halljátok (102) → hallj; parancsolta (93) → parancsolt; száma (93) → szám; látá (92) → lát; felkele (87) → felkel; látván (87) → lát; nevezé (83) → nevez; dicsősége (82) → dicsőség; halál (81) → hal; külde (80) → küld; feje (78) → fej; fejére (73) → fejér; angyala (69) → angyal; helyette (69) → helyett; cselekedjél (68) → cselekedj; elmenvén (68) → elmen; hallja (68) → hallj; elindulának (67) → elindul; megparancsolta (64) → megparancsolt; népének (63) → nép; kiálta (62) → kiált; serege (62) → sereg; sátorának (62) → sátor; felelének (60) → felel; országa (60) → ország; sokasága (60) → sokaság; szája (60) → száj; elküldé (59) → elküld; továbbá (59) → tovább; cselekedének (58) → cselekedik; háznépe (58) → háznép; vége (57) → vég; embere (56) → ember; emlékezzél (56) → emlékezz; része (55) → rész; bemenvén (54) → bemen; felkelvén (54) → felkel; adjátok (53) → adj; elkülde (53) → elküld; leányának (53) → leány; szélessége (52) → szélesség; menvén (51) → men; megölé (50) → megöl; törvénye (50) → törvény; felőle (49) → felől; közepette (49) → közepett; meghallotta (49) → meghallott; mellette (48) → mellett; szerze (48) → szerz; zsoltára (48) → zsoltár; kezde (47) → kezd; kimenvén (47) → kimen; meghallá (47) → meghall; megveré (47) → megver; vére (47) → vér; hallván (46) → hall; mossa (46) → moss; fogja (45) → fogj; fölé (45) → föl; hallotta (45) → hallott; nemzetségének (45) → nemzetség; szeme (45) → szem; szólának (45) → szól; tudván (45) → tud; megáldá (44) → megáld; visszatére (44) → visszatér; feleségének (42) → feleség; férje (42) → férj; határa (42) → határ; megálla (42) → megáll; építe (42) → épít; megparancsolá (41) → megparancsol; álla (41) → áll; élete (41) → élet; általa (40) → által; felemelé (39) → felemelik; marada (39) → marad; voltál (39) → volt; elbocsátá (38) → elbocsát; városa (38) → város; életének (38) → élet; öröksége (38) → örökség; egyétek (37) → egy; helye (37) → hely; támada (37) → támad; sátora (36) → sátor; tele (36) → telik; veté (36) → vet; kiáltának (35) → kiált; akará (34) → akar; szálla (34) → száll; csinálának (33) → csinál; gyülekezete (33) → gyülekezet; parancsola (33) → parancsol; szűle (33) → szül; állának (33) → áll; cselekedjétek (32) → cselekedj; elbeszélé (32) → elbeszélik; lássátok (32) → láss; magassága (32) → magasság; teste (32) → test; emberének (31) → ember; földe (31) → föld; kezdé (31) → kezd; tartsátok (31) → tarts; bűne (30) → bűn; füle (30) → fül; nyilván (30) → nyil; vigyétek (30) → vigy; csinála (29) → csinál; felkelének (29) → felkel; igazsága (29) → igazság; követé (29) → követ; megkérdé (29) → megkérd; parancsolá (29) → parancsol; teremtette (29) → teremtett; cselekedvén (28) → cselekedik; fele (28) → fel; hozának (28) → hoz; testvére (28) → testvér; szólván (27) → szól; áldozata (27) → áldozat; földének (26) → föld; láta (26) → lát; megverte (26) → megvert; megépíté (26) → megépít; vezére (26) → vezér; eljutának (25) → eljut; halála (25) → halál; juta (25) → jut; jöttél (25) → jött; maradéka (25) → maradék; meghajtá (25) → meghajt; meglátá (25) → meglát; szövetségének (25) → szövetség; városának (25) → város; dicsőségének (24) → dicsőség; gyümölcse (24) → gyümölcs; megölte (24) → megölt; nemze (24) → nemz; seregének (24) → sereg; szólítá (24) → szólít; visszatérének (24) → visszatér; áldjátok (24) → áldj; éneke (24) → ének; építé (24) → épít; összegyűjté (24) → összegyűjt; elvégezé (23) → elvégezik; este (23) → est; hagyja (23) → hagyj; hegye (23) → hegy; nyelve (23) → nyelv; tanácsa (23) → tanács; ölje (23) → ölj; felgerjede (22) → felgerjed; hagyá (22) → hagy; hosszúsága (22) → hosszúság; kinél (22) → kin; lakosa (22) → lakos; teremté (22) → teremt; testvérének (22) → testvér; elfutának (21) → elfut; hagyjátok (21) → hagyj; hozza (21) → hozz; jutának (21) → jut; kéré (21) → kér; meglássátok (21) → megláss; megtére (21) → megtér; szeressétek (21) → szeress; testének (21) → test

**Utána (v3 C+K): 0 / 200 nem ige** — *pontosítás (18.1, DT-F94f): ez a 200 leggyakoribb jegyes alakra érvényes, a teljes táblára nem; a ritka alakokon ismert korlát, becsült hibaaránnyal (18.3, N-F94h).* Határeset: *érte → ért* (az *ért* ige múltja; a „érte” névmási olvasat a Károliban többnyire *érette*) — igének sorolva. Téves, de igei tövek: *hívatá → hívatik*, *felemelé → felemelik*, *eltemeték → eltemetik*, *elvégezé → elvégezik*, *könyörge → könyörg*, *megfélemlének → megféleml*.

ada (93) → ad [mult.alanyi.E3]; látá (92) → lát [mult.targyas.E3]; felkele (87) → felkel [mult.alanyi.E3]; látván (87) → lát [hatarozoi_igenev]; nevezé (83) → nevez [mult.targyas.E3]; külde (80) → küld [mult.alanyi.E3]; cselekedjél (68) → cselekszik [felszolito.E2]; elindulának (67) → elindul [mult.T3]; ütének (64) → üt [mult.T3]; esék (62) → esik [mult.E3]; kiálta (62) → kiált [mult.alanyi.E3]; felelének (60) → felel [mult.T3]; elküldé (59) → elküld [mult.targyas.E3]; cselekedének (58) → cselekszik [mult.T3]; emlékezzél (56) → emlékszik [felszolito.E2]; felkelvén (54) → felkel [hatarozoi_igenev]; elkülde (53) → elküld [mult.alanyi.E3]; megölé (50) → megöl [mult.targyas.E3]; szerze (48) → szerz [mult.alanyi.E3]; kezde (47) → kezd [mult.alanyi.E3]; meghallá (47) → meghall [mult.targyas.E3]; megveré (47) → megver [mult.targyas.E3]; hallván (46) → hall [hatarozoi_igenev]; adának (45) → ad [mult.T3]; szólának (45) → szól [mult.T3]; tudván (45) → tud [hatarozoi_igenev]; megáldá (44) → megáld [mult.targyas.E3]; visszatére (44) → visszatér [mult.alanyi.E3]; megálla (42) → megáll [mult.alanyi.E3]; építe (42) → épít [mult.alanyi.E3]; megparancsolá (41) → megparancsol [mult.targyas.E3]; felemelé (39) → felemelik [mult.targyas.E3]; marada (39) → marad [mult.alanyi.E3]; elbocsátá (38) → elbocsát [mult.targyas.E3]; láték (37) → lát [mult.E1]; támada (37) → támad [mult.alanyi.E3]; eltemeték (36) → eltemetik [mult.E3]; veté (36) → vet [mult.targyas.E3]; kiáltának (35) → kiált [mult.T3]; tetszék (35) → tetszik [mult.E3]; akará (34) → akar [mult.targyas.E3]; szálla (34) → száll [mult.alanyi.E3]; csinálának (33) → csinál [mult.T3]; parancsola (33) → parancsol [mult.alanyi.E3]; szűle (33) → szül [mult.alanyi.E3]; elbeszélé (32) → elbeszél [mult.targyas.E3]; kezdé (31) → kezd [mult.targyas.E3]; megjelenék (31) → megjelen [mult.E1]; üle (30) → ül [mult.alanyi.E3]; adván (29) → ad [hatarozoi_igenev]; csinála (29) → csinál [mult.alanyi.E3]; eltemetteték (29) → eltemettet [mult.E1]; felkelének (29) → felkel [mult.T3]; követé (29) → követ [mult.targyas.E3]; lakozék (29) → lakozik [mult.E3]; megkérdé (29) → megkérd [mult.targyas.E3]; parancsolá (29) → parancsol [mult.targyas.E3]; cselekedvén (28) → cselekszik [hatarozoi_igenev]; hozának (28) → hoz [mult.T3]; megölék (28) → megöl [mult.E1]; szólván (27) → szól [hatarozoi_igenev]; eltávozék (26) → eltávozik [mult.E3]; láta (26) → lát [mult.alanyi.E3]; megépíté (26) → megépít [mult.targyas.E3]; áldozék (26) → áldoz [mult.E1]; eljutának (25) → eljut [mult.T3]; juta (25) → jut [mult.alanyi.E3]; meghajtá (25) → meghajt [mult.targyas.E3]; meglátá (25) → meglát [mult.targyas.E3]; adaték (24) → adatik [mult.E3]; nemze (24) → nemz [mult.alanyi.E3]; szólítá (24) → szólít [mult.targyas.E3]; visszatérének (24) → visszatér [mult.T3]; építé (24) → épít [mult.targyas.E3]; összegyűjté (24) → összegyűjt [mult.targyas.E3]; elvégezé (23) → elvégezik [mult.targyas.E3]; imádkozék (23) → imádkozik [mult.E3]; felgerjede (22) → felgerjed [mult.alanyi.E3]; hagyá (22) → hagy [mult.targyas.E3]; teremté (22) → teremt [mult.targyas.E3]; elfutának (21) → elfut [mult.T3]; jutának (21) → jut [mult.T3]; kéré (21) → kér [mult.targyas.E3]; megtére (21) → megtér [mult.alanyi.E3]; akarván (20) → akar [hatarozoi_igenev]; beborítá (20) → beborít [mult.targyas.E3]; hallék (20) → hall [mult.E1]; leüle (20) → leül [mult.alanyi.E3]; helyhezteté (19) → helyheztet [mult.targyas.E3]; illeté (19) → illet [mult.targyas.E3]; küldének (19) → küld [mult.T3]; megfogván (19) → megfog [hatarozoi_igenev]; megnyitá (19) → megnyit [mult.targyas.E3]; megszaggatá (19) → megszaggat [mult.targyas.E3]; szülé (19) → szül [mult.targyas.E3]; áldozának (19) → áldoz [mult.T3]; elfuta (18) → elfut [mult.alanyi.E3]; hallá (18) → hall [mult.targyas.E3]; kérék (18) → kér [mult.E1]; leborula (18) → leborul [mult.alanyi.E3]; leszálla (18) → leszáll [mult.alanyi.E3]; rendele (18) → rendel [mult.alanyi.E3]; szűlé (18) → szül [mult.targyas.E3]; találá (18) → talál [mult.targyas.E3]; vetének (18) → vet [mult.T3]; érkezék (18) → érkezik [mult.E3]; akara (17) → akar [mult.alanyi.E3]; borula (17) → borul [mult.alanyi.E3]; bízzál (17) → bízik [felszolito.E2]; hallgata (17) → hallgat [mult.alanyi.E3]; hívatá (17) → hívatik [mult.targyas.E3]; követék (17) → követ [mult.E1]; megemészté (17) → megemészt [mult.targyas.E3]; megfélemlének (17) → megféleml [mult.T3]; nevezék (17) → nevez [mult.E1]; érte (17) → ért [mult.alanyi.E3]; összegyűlének (17) → összegyűl [mult.T3]; bocsátá (16) → bocsát [mult.targyas.E3]; hoza (16) → hoz [mult.alanyi.E3]; könyörge (16) → könyörg [mult.alanyi.E3]; bocsáta (15) → bocsát [mult.alanyi.E3]; fogada (15) → fogad [mult.alanyi.E3]; izenvén (15) → izen [hatarozoi_igenev]; járván (15) → jár [hatarozoi_igenev]; kinyújtá (15) → kinyújt [mult.targyas.E3]; lakozának (15) → lakozik [mult.T3]; leborulának (15) → leborul [mult.T3]; megcsókolá (15) → megcsókol [mult.targyas.E3]; meghalának (15) → meghal [mult.T3]; megméré (15) → megmér [mult.targyas.E3]; megállának (15) → megáll [mult.T3]; talála (15) → talál [mult.alanyi.E3]; beszéle (14) → beszél [mult.alanyi.E3]; felindítá (14) → felindít [mult.targyas.E3]; felkiálta (14) → felkiált [mult.alanyi.E3]; hivatá (14) → hivat [mult.targyas.E3]; hívá (14) → hív [mult.targyas.E3]; kezdék (14) → kezd [mult.E1]; megkérdezé (14) → megkérdez [mult.targyas.E3]; megkérdezék (14) → megkérdez [mult.E1]; méré (14) → mér [mult.targyas.E3]; tartózkodék (14) → tartózkodik [mult.E3]; vete (14) → vet [mult.alanyi.E3]; elbeszélék (13) → elbeszél [mult.E1]; ismeré (13) → ismer [mult.targyas.E3]; jára (13) → jár [mult.alanyi.E3]; kezdének (13) → kezd [mult.T3]; követvén (13) → követ [hatarozoi_igenev]; küldé (13) → küld [mult.targyas.E3]; maradának (13) → marad [mult.T3]; megdorgálá (13) → megdorgál [mult.targyas.E3]; meggyógyítá (13) → meggyógyít [mult.targyas.E3]; meghallgatá (13) → meghallgat [mult.targyas.E3]; megkérdék (13) → megkérd [mult.E1]; megszabadítá (13) → megszabadít [mult.targyas.E3]; megtelék (13) → megtelik [mult.E3]; vetvén (13) → vet [hatarozoi_igenev]; élvén (13) → él [hatarozoi_igenev]; ejté (12) → ejt [mult.targyas.E3]; elindula (12) → elindul [mult.alanyi.E3]; elküldvén (12) → elküld [hatarozoi_igenev]; elküldék (12) → elküld [mult.E1]; elrejté (12) → elrejt [mult.targyas.E3]; felelék (12) → felel [mult.E1]; felállítá (12) → felállít [mult.targyas.E3]; fölkele (12) → fölkel [mult.alanyi.E3]; járának (12) → jár [mult.T3]; kitölté (12) → kitölt [mult.targyas.E3]; kiűzé (12) → kiűz [mult.targyas.E3]; kérvén (12) → kér [hatarozoi_igenev]; készíte (12) → készít [mult.alanyi.E3]; megcsinálá (12) → megcsinál [mult.targyas.E3]; meghagyá (12) → meghagy [mult.targyas.E3]; meglátván (12) → meglát [hatarozoi_igenev]; megverék (12) → megver [mult.E1]; találának (12) → talál [mult.T3]; tanítván (12) → tanít [hatarozoi_igenev]; állítá (12) → állít [mult.targyas.E3]; egybegyűle (11) → egybegyül [mult.alanyi.E3]; elfoglalá (11) → elfoglal [mult.targyas.E3]; fogadá (11) → fogad [mult.targyas.E3]; hallgatának (11) → hallgat [mult.T3]; javítgata (11) → javítgat [mult.alanyi.E3]; kiáltván (11) → kiált [hatarozoi_igenev]; levágá (11) → levág [mult.targyas.E3]; leülvén (11) → leül [hatarozoi_igenev]; megerősíté (11) → megerősít [mult.targyas.E3]; megfogá (11) → megfog [mult.targyas.E3]; megmutatá (11) → megmutat [mult.targyas.E3]; megszámlálá (11) → megszámlál [mult.targyas.E3]; megölvén (11) → megöl [hatarozoi_igenev]; szállának (11) → száll [mult.T3]; tartván (11) → tart [hatarozoi_igenev]; választa (11) → választ [mult.alanyi.E3]; építének (11) → épít [mult.T3]; adál (10) → ad [mult.E2]; csinálá (10) → csinál [mult.targyas.E3]; egybegyűlének (10) → egybegyűl [mult.T3]; elhozá (10) → elhoz [mult.targyas.E3]; elkezdé (10) → elkezd [mult.targyas.E3]

scope=a teljes Károli korpusz-lexikona (62869 kisbetűsített alak) | forras=eszkozok/szoto/regies_felismeres.py + hibrid_v2.py (sha256:864d6876437a) + hibrid.py (sha256:7dc76b42c876) + karoli_lexikon.tsv (sha256:215f687f5d68) | ts=2026-10-13T16:08Z

A táblában: a v2 A 74 nem-igéjéből (11.4) egy sem kap jegyet; jegyes sor: szabály 2 965, kivétel 228, K tábla 39.

### 17.4 Regresszió a fejlesztési mintákon

##### szoto_minta_1_fejlesztes.tsv (213 alak, 6375 előfordulás)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 97% / 99.4% (206/213) | 98% / 99.6% (54/55) | 98% / 99.1% (64/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 86% / 89.5% (6/7) | 100% / 100.0% (27/27) |
| hibrid C | 85% / 94.2% (181/213) | 89% / 95.0% (49/55) | 82% / 82.2% (53/65) | 84% / 90.2% (38/45) | 79% / 88.2% (11/14) | 43% / 52.6% (3/7) | 100% / 100.0% (27/27) |
| hibrid CK | 90% / 98.9% (192/213) | 100% / 100.0% (55/55) | 89% / 93.0% (58/65) | 84% / 90.2% (38/45) | 79% / 88.2% (11/14) | 43% / 52.6% (3/7) | 100% / 100.0% (27/27) |
| v2 A | 95% / 99.2% (203/213) | 98% / 99.6% (54/55) | 95% / 96.6% (62/65) | 91% / 93.9% (41/45) | 100% / 100.0% (14/14) | 71% / 78.9% (5/7) | 100% / 100.0% (27/27) |
| v2 C | 79% / 92.6% (169/213) | 85% / 93.8% (47/55) | 71% / 73.6% (46/65) | 80% / 88.6% (36/45) | 79% / 88.2% (11/14) | 29% / 42.1% (2/7) | 100% / 100.0% (27/27) |

scope=szoto_minta_1_fejlesztes.tsv (sha256:a7f8d65d42de) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

##### szoto_minta_2_fejlesztes.tsv (180 alak, 1695 előfordulás)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 93% / 97.9% (167/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 90% / 91.0% (19/21) | 100% / 100.0% (10/10) |
| hibrid C | 84% / 87.8% (151/180) | 90% / 87.6% (36/40) | 84% / 86.5% (54/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 71% / 82.1% (15/21) | 100% / 100.0% (10/10) |
| hibrid CK | 87% / 96.0% (156/180) | 98% / 98.4% (39/40) | 88% / 92.1% (56/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 71% / 82.1% (15/21) | 100% / 100.0% (10/10) |
| v2 A | 92% / 97.6% (166/180) | 100% / 100.0% (40/40) | 91% / 93.0% (58/64) | 94% / 95.3% (30/32) | 77% / 69.2% (10/13) | 86% / 85.9% (18/21) | 100% / 100.0% (10/10) |
| v2 C | 80% / 85.8% (144/180) | 90% / 87.6% (36/40) | 78% / 76.7% (50/64) | 78% / 81.4% (25/32) | 85% / 74.4% (11/13) | 57% / 64.1% (12/21) | 100% / 100.0% (10/10) |

scope=szoto_minta_2_fejlesztes.tsv (sha256:587e47bded57) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

##### szoto_minta_3_ellenorzott.tsv (113 alak, 3745 előfordulás)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 94% / 99.7% (106/113) | 100% / 100.0% (25/25) | 91% / 90.6% (32/35) | 100% / 100.0% (20/20) | 75% / 78.6% (9/12) | 100% / 100.0% (13/13) | 88% / 81.8% (7/8) |
| hibrid C | 78% / 91.4% (88/113) | 88% / 92.0% (22/25) | 77% / 81.2% (27/35) | 95% / 97.2% (19/20) | 25% / 28.6% (3/12) | 77% / 58.6% (10/13) | 88% / 81.8% (7/8) |
| hibrid CK | 81% / 99.0% (91/113) | 100% / 100.0% (25/25) | 77% / 81.2% (27/35) | 95% / 97.2% (19/20) | 25% / 28.6% (3/12) | 77% / 58.6% (10/13) | 88% / 81.8% (7/8) |
| v2 A | 80% / 99.1% (90/113) | 100% / 100.0% (25/25) | 80% / 84.4% (28/35) | 50% / 58.3% (10/20) | 67% / 71.4% (8/12) | 92% / 96.6% (12/13) | 88% / 81.8% (7/8) |
| v2 C | 56% / 90.3% (63/113) | 88% / 92.0% (22/25) | 51% / 62.5% (18/35) | 40% / 30.6% (8/20) | 17% / 21.4% (2/12) | 54% / 48.3% (7/13) | 75% / 72.7% (6/8) |

scope=szoto_minta_3_ellenorzott.tsv (sha256:bafc1e67a061) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + hibrid_v2.py (sha256:864d6876437a) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

Egyedi romlás a v2-höz képest:

```
szoto_minta_1_fejlesztes.tsv A ROMLÁS: —
szoto_minta_1_fejlesztes.tsv C ROMLÁS: —
szoto_minta_1_fejlesztes.tsv CK ROMLÁS: —
szoto_minta_2_fejlesztes.tsv A ROMLÁS: —
szoto_minta_2_fejlesztes.tsv C ROMLÁS: leheletének(ragos_nevszo,1): v2=lehelet v3=leheletének
szoto_minta_2_fejlesztes.tsv CK ROMLÁS: leheletének(ragos_nevszo,1): v2=lehelet v3=leheletének
szoto_minta_3_ellenorzott.tsv A ROMLÁS: —
szoto_minta_3_ellenorzott.tsv C ROMLÁS: —
szoto_minta_3_ellenorzott.tsv CK ROMLÁS: —
szoto_minta_4_fuggetlen.tsv A ROMLÁS: atyafiaival(ragos_nevszo,1): v2=atyafi v3=atyafiai
szoto_minta_4_fuggetlen.tsv C ROMLÁS: atyafiaival(ragos_nevszo,1): v2=atyafi v3=atyafiaival
szoto_minta_4_fuggetlen.tsv CK ROMLÁS: atyafiaival(ragos_nevszo,1): v2=atyafi v3=atyafiaival
```

A v3 A és C/C+K **minden fejlesztési mintán és rétegben legalább a v2 szintjén** (a 2. minta régies ige rétege C/C+K-ban 78% = v2). A *leheletének* és az *atyafiaival* a korábbi v3-ban is hibás volt.

### 17.5 A 4. minta mérése a javított v3-mal (M1, M2, K3)

**A 4. minta után módosított v3; a minta erre a változatra nem teljesen független** (a minta a 15. szakasz mérése óta fejlesztési halmaz). A régi számok a 15. szakaszban változatlanul maradnak.

##### szoto_minta_4_fuggetlen.tsv — a K tábla alakjai NÉLKÜL — a DT-F94c DÖNTŐ száma (93 alak, 832 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 78% / 96.6% (73/93) | 100% / 100.0% (5/5) | 83% / 81.2% (29/35) | 70% / 81.2% (14/20) | 58% / 50.0% (7/12) | 92% / 96.7% (12/13) | 75% / 80.0% (6/8) |
| hibrid C | 63% / 95.0% (59/93) | 100% / 100.0% (5/5) | 69% / 70.8% (24/35) | 60% / 75.0% (12/20) | 33% / 33.3% (4/12) | 69% / 86.7% (9/13) | 62% / 73.3% (5/8) |
| hibrid CK | 63% / 95.0% (59/93) | 100% / 100.0% (5/5) | 69% / 70.8% (24/35) | 60% / 75.0% (12/20) | 33% / 33.3% (4/12) | 69% / 86.7% (9/13) | 62% / 73.3% (5/8) |
| simplemma | 55% / 74.8% (51/93) | 80% / 77.9% (4/5) | 60% / 54.2% (21/35) | 45% / 62.5% (9/20) | 17% / 11.1% (2/12) | 85% / 93.3% (11/13) | 50% / 60.0% (4/8) |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

##### szoto_minta_4_fuggetlen.tsv — a K tábla alakjai és a fejlesztés közben látott alakok (szombatimat, tartózkodék, tévelyedjék, többé) NÉLKÜL (90 alak, 819 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 79% / 96.7% (71/90) | 100% / 100.0% (5/5) | 82% / 80.0% (28/34) | 72% / 77.3% (13/18) | 58% / 50.0% (7/12) | 92% / 96.7% (12/13) | 75% / 80.0% (6/8) |
| hibrid C | 64% / 95.4% (58/90) | 100% / 100.0% (5/5) | 71% / 75.6% (24/34) | 61% / 68.2% (11/18) | 33% / 33.3% (4/12) | 69% / 86.7% (9/13) | 62% / 73.3% (5/8) |
| hibrid CK | 64% / 95.4% (58/90) | 100% / 100.0% (5/5) | 71% / 75.6% (24/34) | 61% / 68.2% (11/18) | 33% / 33.3% (4/12) | 69% / 86.7% (9/13) | 62% / 73.3% (5/8) |
| simplemma | 56% / 74.8% (50/90) | 80% / 77.9% (4/5) | 62% / 57.8% (21/34) | 44% / 50.0% (8/18) | 17% / 11.1% (2/12) | 85% / 93.3% (11/13) | 50% / 60.0% (4/8) |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

##### szoto_minta_4_fuggetlen.tsv — minden sor (a K tábla alakjaival; tájékoztató) (113 alak, 3053 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 81% / 95.7% (92/113) | 96% / 96.5% (24/25) | 83% / 81.2% (29/35) | 70% / 81.2% (14/20) | 58% / 50.0% (7/12) | 92% / 96.7% (12/13) | 75% / 80.0% (6/8) |
| hibrid C | 68% / 91.6% (77/113) | 92% / 92.7% (23/25) | 69% / 70.8% (24/35) | 60% / 75.0% (12/20) | 33% / 33.3% (4/12) | 69% / 86.7% (9/13) | 62% / 73.3% (5/8) |
| hibrid CK | 70% / 98.6% (79/113) | 100% / 100.0% (25/25) | 69% / 70.8% (24/35) | 60% / 75.0% (12/20) | 33% / 33.3% (4/12) | 69% / 86.7% (9/13) | 62% / 73.3% (5/8) |
| simplemma | 61% / 86.3% (69/113) | 88% / 87.6% (22/25) | 60% / 54.2% (21/35) | 45% / 62.5% (9/20) | 17% / 11.1% (2/12) | 85% / 93.3% (11/13) | 50% / 60.0% (4/8) |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

##### szoto_minta_4_fuggetlen.tsv — CSAK a K tábla alakjai (a C+K hozzájárulása; a K táblát a felhasználó ellenőrizte) (20 alak, 2221 előfordulás, csak felhasznalo)

| elemző | ossz | gyakori | ragos_nevszo | regies_ige | regies_helyesiras | ige_mai_alak | tulajdonnev |
|---|---|---|---|---|---|---|---|
| hibrid A | 95% / 95.4% (19/20) | 95% / 95.4% (19/20) | — | — | — | — | — |
| hibrid C | 90% / 90.4% (18/20) | 90% / 90.4% (18/20) | — | — | — | — | — |
| hibrid CK | 100% / 100.0% (20/20) | 100% / 100.0% (20/20) | — | — | — | — | — |
| simplemma | 90% / 90.6% (18/20) | 90% / 90.6% (18/20) | — | — | — | — | — |

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + adat/szoto/karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

##### M2 — a minta minden lemmája: 99 lemma, célhalmaz 58034 token (célhalmaz nélküli lemma: 7: kárbunkulus, tévelyedik, jóna, béth-aven, girzeus, felingereltetik, nyiratkozik)

| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |
|---|---|---|---|---|---|
| hibrid A | 97.56% | 98.02% | 98.65% (57251/58034) | 90.9% | 99.0% |
| hibrid C | 91.02% | 91.02% | 94.70% (54960/58034) | 75.7% | 98.4% |
| hibrid CK | 95.87% | 95.87% | 98.40% (57104/58034) | 76.4% | 98.6% |

*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* se 0% / 100% (146, H3808); bíz 87% / 0% (38, H0982); űz 100% / 0% (29, H3423); kényszerít 100% / 0% (8, H7650); unoka 100% / 0% (8, H1121); láncz 83% / 0% (6, H8333); összegyűlekezik 33% / 0% (3, H0622); elhajt 100% / 0% (3, H3947); hunyorgat 0% / 100% (2, H7169); hívogat 100% / 0% (2, H7121); keresztülszúr 100% / 0% (2, H1856); ötvenedes 0% / 100% (1, H2572)

##### M2 — a K tábla alakjai nélküli lemmák (a DT-F94c döntő halmaza): 79 lemma, célhalmaz 19652 token (célhalmaz nélküli lemma: 7: kárbunkulus, tévelyedik, jóna, béth-aven, girzeus, felingereltetik, nyiratkozik)

| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |
|---|---|---|---|---|---|
| hibrid A | 95.55% | 96.17% | 98.20% (19299/19652) | 89.9% | 99.1% |
| hibrid C | 89.68% | 89.68% | 97.60% (19180/19652) | 70.6% | 98.2% |
| hibrid CK | 91.80% | 91.80% | 98.03% (19264/19652) | 71.0% | 98.3% |

*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* bíz 87% / 0% (38, H0982); űz 100% / 0% (29, H3423); kényszerít 100% / 0% (8, H7650); unoka 100% / 0% (8, H1121); láncz 83% / 0% (6, H8333); összegyűlekezik 33% / 0% (3, H0622); elhajt 100% / 0% (3, H3947); hunyorgat 0% / 100% (2, H7169); hívogat 100% / 0% (2, H7121); keresztülszúr 100% / 0% (2, H1856); ötvenedes 0% / 100% (1, H2572); harczol 100% / 6% (47, H3898)

scope=szoto_minta_4_fuggetlen.tsv (sha256:4f754045d207) lemmái; a párosított Károli-könyvek (484820 hu token, 58041 alak) | forras=eszkozok/szoto/meres_m2.py + adat/karoli_strong/szavak_*.tsv (együttes sha256:c3266499df09; modell-kimenet, javaslat) + hibrid.py (v3, sha256:7dc76b42c876) + gyakori_alakok.tsv (sha256:ffe73f0e0add) + karoli_lexikon.tsv (sha256:215f687f5d68) + simplemma 2.0.0 (hu.plzma sha256:0ebc6a84a326) | futtatókörnyezet: Python 3.11.17 (Linux) | ts=2026-10-13T16:08Z

| | M1 súlyozva, K nélkül (döntő) | M1 alakonként, K nélkül | M1 súlyozva, minden sor | M2 (c), K nélküli lemmák | M2 (c), minden lemma | K3 |
|---|---|---|---|---|---|---|
| C+K, javított v3 (nem teljesen független) | 95,0% | 63% | 98,6% | 98,03% | 98,40% | **teljesül** |
| C+K, a 15. szakaszban (független mérés) | 94,6% | 60% | 98,5% | 98,02% | 98,40% | teljesül |
| A, javított v3 | 96,6% | 78% | 95,7% | 98,20% | 98,65% | teljesül |

Az M2 a determinizálás miatt is változhatott: a `meres_m2.py` a fő Strongot egyenlő darabszámnál korábban a halmaz bejárási sorrendje szerint választotta (az ellenőr megfigyelése: az *összegyűlekezik* fő Strongja a 15.2-ben H6950, a 16.3-ban H0622); most egyenlőségnél a kisebb Strong-szám (H0622), két futás bájtra azonos.

### 17.6 A teljes Károli táblája

A teljes Károli 66 824 alakjából **1053** alak szótári alakja változott (a javítás előtti v3 C+K → a javított v3 C+K); jegy elveszett 65, új jegy 0.

| # | alak | előtte | utána |
|---|---|---|---|
| 1 | apostolságára | apostolságára | apostolság |
| 2 | bujdosásod | bujdosásod | bujdosás |
| 3 | bántásától | bántásától | bántás |
| 4 | egybegyűjtésének | egybegyűjtésének | egybegyűjtés |
| 5 | elsőszülöttségem | elsőszülöttségem | elsőszülöttség |
| 6 | elvettetésök | elvettetésök | elvettetés |
| 7 | felgerjedésedben | felgerjedésedben | felgerjedés |
| 8 | felállítását | felállítását | felállítás |
| 9 | fáradozásából | fáradozásából | fáradozás |
| 10 | hallgatására | hallgatására | hallgatás |
| 11 | ház-fölverésen | ház-fölverésen | ház-fölverés |
| 12 | imádkozásokban | imádkozásokban | imádkozás |
| 13 | kifosztogattál | kifosztogat | kifosztogattál |
| 14 | kijavítására | kijavítására | kijavítás |
| 15 | kérésem | kérésem | kérés |
| 16 | közléseivel | közléseivel | közlés |
| 17 | mentségére | mentségére | mentség |
| 18 | metszéseket | metszéseket | metszés |
| 19 | nevekedését | nevekedését | nevekedés |
| 20 | sujtását | sujtását | sujtás |
| 21 | szóratta | szórat | szóratta |
| 22 | szülésem | szülésem | szülés |
| 23 | tapodását | tapodását | tapodás |
| 24 | társaságok | társaságok | társaság |
| 25 | törvényszegésünk | törvényszegésünk | törvényszegés |
| 26 | vendégséget | vendégséget | vendégség |
| 27 | vetekedésöket | vetekedésöket | vetekedés |
| 28 | vigasztalásai | vigasztalásai | vigasztalás |
| 29 | vigasztalásom | vigasztalásom | vigasztalás |
| 30 | zavarását | zavarását | zavarás |

Kézi ítélet (manual): 28 jobb (-ás/-és/-ság/-ség főnevek), 2 rosszabb (*kifosztogattál*, *szóratta*: gyengén attesztált -at végű ige).

`adat/szoto/karoli_szotari_alak.tsv` újragenerálva (simplemma nélkül, C+K; Python 3.14, 3.11 és két hash-mag alatt bájtra azonos): sha256 `b1c6f5131d0182286f248c959099173cfdfcf8e41dc5ab9ae5079a2b19715a39`. **A v3 újbóli befagyasztása:** `eszkozok/szoto/hibrid.py` sha256 `7dc76b42c876f00191fac64e9b10dcba8881caab0b32c0ae02e4ac58f6cb4f2b` (git blob `1706b2f47c603bd7de83e948d1104d8aaf37086c`); K tábla `ffe73f0e0add26d796429bd5e6aaee32564a46821210292dea8254c5b6c62913` (csak a fejlécsor változott).

### 17.7 Ismert hibák a kiadott C+K-ban (6. eltérés; kézi kivétellel nem javítva, mert az a 3. mintára hangolás volna)

*Melkié → Melkié* (helyesen *Melki*: név + -é birtokjel), *atyámnak → atyám* (helyesen *atya*), *meggyarapodnak → meggyarapod* (helyesen *meggyarapodik*). Az A-ban mindhárom helyes; a C+K-ban az általános szabályok nem fedik le (név + -é; a ritka *atya* + hosszú birtokos; ritka -ik-es ige -nak alakja).

### 17.8 Formai pontok (4. és 7. eltérés)

N-F94e lezárva a `NYITOTT_FELADATOK.md`-ben; az N-F94a–c önálló tételként felvéve (az N-F94c: *jó*, 1Móz 1:4, H2895 a TAHOT-ban); SEMA 2.27 `alapige` és `strong` sora javítva.


## 18. Az újraellenőrzés után (ELLENOR_F94_2; DT-F94f, a felhasználó döntése: 2. opció — ismert korlát)

### 18.1 A K6 szűkítése (brief v1.2)

A brief K6-a: „a `regies_jegy` a 200 leggyakoribb jegyes alakon csak igei alakon kitöltött; a ritka alakokon ismert korlát, becsült hibaaránnyal (N-F94h)”. A 17.3 szakasz „0 / 200 nem ige” eredménye erre a 200 alakra érvényes; a teljes táblára nem (az ELLENOR_F94_2 legalább 13 ritka nem igei alakot talált igei jeggyel: *alája, körüle, bérese, zsellére, vendége, látnoka, részese, királynéasszonya, felirata, követe, feljáratának, királyasszonyának, királynéasszonyának*). Új javító kör nem indul: a birtokos -a/-e és a régies alanyi múlt -a/-e alakilag egyezik, a szótári alak ezekben jórészt helyes, és minden újabb kör tovább rontaná a 4. minta függetlenségét.

### 18.2 N-F94e lezárása: *evék, ivék* (kivételtábla)

`hibrid.py`: az *evék* és az *ivék* (az -ik-es *eszik / iszik* régies múlt E/3-a; 1Móz 3:6, 9:21) kivételtábla-jegye `mult.E1` helyett `mult.E3`. **Oszloponkénti igazolás** (a tábla a javítás előtt és után, `split('\t')`, soronként és oszloponként összevetve):

```
alak: 0 eltérés 
szotari_alak: 0 eltérés 
szotari_alak_mai: 0 eltérés 
alapige: 0 eltérés 
tovabbi_elfogadhato: 0 eltérés 
modszer: 0 eltérés 
szabaly_forras: 0 eltérés 
regies_jegy: 4 eltérés [('Evék', 'mult.E1', 'mult.E3'), ('evék', 'mult.E1', 'mult.E3'), ('ivék', 'mult.E1', 'mult.E3'), ('megevék', 'mult.E1', 'mult.E3')]
sorrend azonos: True | sorok: 66824
```

Csak a `regies_jegy` változott, 4 soron (*Evék, evék, ivék, megevék*) — *pontosítás (18.6, ELLENOR_F94_3, DT-F94f): a *megevék* `mult.E3`-a tévedés volt (mind a 4 helyén T/3 tárgyas); a jegye most üres, a befagyasztás a 18.6 szerint* —; minden más oszlop bájtra azonos, a sorrend és a sorszám is. A fejlécben csak a hibrid sha256-ja változott. Újramérés nem kellett (a szótári alak nem változott; az M1/M2/K3 érvényben, 17.5). **A v3 befagyasztása:** `eszkozok/szoto/hibrid.py` sha256 `719ee6fff776993f0793cb3b1a82ba8111a93245e4c34551f289917fe6e4624e`; `adat/szoto/karoli_szotari_alak.tsv` sha256 `565e1f573ef85f531e819f749af2e34c946d9c8d4f7ab1bd663d72a363ef91bb`.

### 18.3 A korlát számszerűsítése: 100-as minta a jegyes sorokból

*proveniencia: scope=a karoli_szotari_alak.tsv jegyes sorai (a 18.2 javítása után) | forras=eszkozok/szoto/jegy_minta.py, mag 20261013, + konkordancia/Karoli_1908.tsv (példaversek) + manual (besorolás, modell: claude-opus-5-5) | ts=2026-10-13*

```
jegyes sor: 3232; minta: 100 (mag 20261013)
hibás jegy: 6 (6%; Wilson 95%: 2.8–12.5%); kétes: 0; hibás + kétes: 6 (2.8–12.5%)
nem igei alak jeggyel: 0 (0%; Wilson 95%: 0.0–3.7%)
becsült hibás jegyes sor a táblában: 194 (90–403)
```

A minta: `adat/szoto/regies_jegy_minta.tsv` (SEMA 2.27). Mind a 100 alak ige; a 6 hibás jegy mind *-ék* alak: *elutazék, virágozék* (-ik-es ige E/3-a, de a lemmából hiányzik az -ik, ezért az N-F94e-szabály nem fogta), *kiűzék, metélék* (T/3 tárgyas; a magas hangrendű -ék kétértelműsége), *megsegítteték, megtaláltaték* (szenvedő E/3). Mellékes lemmahibák a mintában (a jegy helyes): *intének → intik, eloszlának → eloszl, megölelé → megölelik, menénk → men, irigykedének → irigyked, elrejtőzének → elrejtőz, meggyökerezvén → meggyökerez*. A becslés a jegyes sorok egészére szól; a nem igei alakra tévesen tett jegy a mintában 0 (Wilson 95% felső határ 3,7%), vagyis az ellenőr által talált ritka névszói esetek a jegyes sorok kis töredékét adják.

### 18.4 A -ta/-te osztály (lemmahiba, N-F94h; javítás nélkül)

A mai -ta/-te tárgyas múltat a hibrid régies -a/-e múltként vágja: *mosta → most, áldotta → áldott, gyűlölte → gyűlölt, bánta → bánt, megáldotta → megáldott* (határeset: *érte → ért*). Ez nem csak jegy-, hanem lemmahiba, a „mai igealak” réteg ismert gyengesége (a 4. mintán a C alakonként 62%), és a keresőt is érinti. Gyanús sorok a teljes Károliban (heurisztika, manual megfigyelés; felső becslés, köztük valódi régies alakok is: *hajta, nevete, hinte, csináltata*):

```
a -ta/-te osztály gyanús sorai (mult.alanyi.E3, a tő = az alak -a/-e nélkül):
 -tt végű tő (áldotta → áldott): 3 Megáldotta, megáldotta, áldotta
 -t végű tő, a t nélküli tő önállóan áll (mosta → most): 21 Csináltata, Hajta, Megszámláltata, Nevete, bánta, csináltata, elveszte, feltekintete, gyűlölte, hajta, helyeztete, hinte
 összesen (felső becslés): 24
```

### 18.5 A DT128 modernizálás felé

A modernizálási brief a `regies_jegy`-et **jelöltként** kezelje, ne tényként, és a saját aranymintáján mérje (a 100-as jegy-minta ebbe beépíthető).

### 18.6 A *megevék* jegye (ELLENOR_F94_3; a felhasználó döntése, 2026-10-13)

Az ELLENOR_F94_3 szerint a *megevék* `mult.E3` jegye a Károli mind a 4 előfordulásában hibás: T/3 tárgyas, többes alannyal (2Krón 30:18, Ezsd 6:21, Mk 4:4, Luk 8:5). Az E/3 az előző kör tévedése volt (a 18.2 javítása a *megevék*-et az *evék* jegyével együtt E/3-ra tette). **A döntés** (felhasználó, chat, 2026-10-13): (d) `mult.E1` saját `JEGY['megevék']` bejegyzéssel, *ha a SEMA 2.27 szövege alátámasztja*; ha nem, (b) üres jegy. Az (a) (`mult.T3` jelentésének bővítése) és a (c) (`mult.E3` marad) nem jön.

**A SEMA 2.27 `mult.E1` meghatározása szó szerint:** „`mult.E1` (-ék nem -ik-es igén: *láték*; magas hangrendű igénél a T/3 tárgyassal azonos alakú, l. napló 16.)”. A hivatkozott napló 16.2 (N-F94e): „magas hangrendű, nem -ik-es igénél az *-ék* a T/3 tárgyassal is egyezik”.

**Értékelés: a szöveg a (d)-t nem támasztja alá, ezért (b).** A `mult.E1` meghatározása az *-ék* alakot **nem -ik-es** igére korlátozza, a T/3 tárgyassal való alaki azonosságot is csak ezen belül mondja ki; az -ik-es igék *-ék* alakjának címkéje a `mult.E3` („-ék -ik-es igén”, N-F94e). Az *eszik* -ik-es ige, tehát a *megevék*-re a `mult.E1` a SEMA szövege szerint nem illik. Ugyanezt mutatja a 18.3 mintája: a T/3 tárgyas *-ék* alakon álló `mult.E1`-et (*kiűzék*) hibás jegynek számolta. A T/3 tárgyas múltra a jegykészletben nincs címke, újat bevezetni nem szabad; a SEMA 2.27 szerint az üres jegy a „kivételtábla jegy nélküli sora” is lehet. A *megevék* jegye ezért **üres**.

**A kód** (`hibrid.py`): `JEGY['megevék'] = ''`, és a kivételtábla igekötős ágában az igekötős alak saját jegye elsőbb az igekötő nélküli alakénál: `JEGY.get(w, JEGY.get(w[len(ik):], ''))`. A többi igekötős alak viselkedése nem változik (a `JEGY`-ben nincs más igekötős kulcs; a táblában igazolva, lent). Az *evék* jegye `mult.E3` marad (az *evék* 2 helyen T/3 tárgyas: 2Móz 16:35, Ján 6:58 — kétértelmű alak, N-F94h); az *Evék, evék, ivék* sor nem változott (az *ivék* mind a 9 helyén E/3).

**Oszloponkénti igazolás** (a tábla a 18.6 előtt és után, `split('\t')`, soronként és oszloponként; az előállítás `--ts` nélkül, a valódi idővel):

```
alak: 0 eltérés 
szotari_alak: 0 eltérés 
szotari_alak_mai: 0 eltérés 
alapige: 0 eltérés 
tovabbi_elfogadhato: 0 eltérés 
modszer: 0 eltérés 
szabaly_forras: 0 eltérés 
regies_jegy: 1 eltérés [('megevék', 'mult.E3', '')]
sorrend azonos: True | sorok: 66824
```

Csak a *megevék* `regies_jegy`-e változott (`mult.E3` → üres), 1 adatsor; minden más oszlop bájtra azonos, a sorrend és a sorszám is. A fejlécben a `# GENERÁLT` sor hibrid-sha256-ja és ts-e változott (`ts=2026-10-13T17:14Z`, az újragenerálás tényleges ideje). Újramérés nem kellett (a szótári alak nem változott). A 18.3 mintájában a *megevék* nem szerepel, a becslés változatlan. **A v3 befagyasztása (érvényes):** `eszkozok/szoto/hibrid.py` sha256 `60e1c21510037dd09c589be81acf127c8a975694b03eaef8a6f3fbc9c7cd2efb`; `adat/szoto/karoli_szotari_alak.tsv` sha256 `c3fc23c93a7350c5950e6b760db67fec6a2dc45ad2892e1b2dcd2726c5358612`. A 18.2 sha-i ezzel elavultak.
