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
