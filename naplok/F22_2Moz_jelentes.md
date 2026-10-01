# F22_2Moz_jelentes.md — Károli–Strong párosítás: 2Mózes

*A számok kizárólag szkriptkimenetből jönnek (`f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`, `f22_elemzes.py`, `f22_arany_kereszt.py`, `eredeti_nelkuli_lista.py`). Ág: `claude/f22-2moz`. Módszer: ugyanaz, mint az 1Mózesnél (`F22_1Moz_jelentes.md`): `prompt_v3` változatlanul (hash a futás elején és végén rendben), Sonnet (`vegrehajto-sonnet` subagentek, kötegenként egy, sorban) + Gemini „C” (`google/gemini-3.8-flash`, GitHub Actions, OpenRouter, kötelező minimális gondolkodás). A DT-F22c (marad-e a Gemini) nyitva marad; ehhez a 5.4 szakasz adja a kereszttáblát az aranyhoz.*

## 1. Menet, hatókör, keret

- **Hatókör.** 2Móz: 1 213 Károli-vers; ebből 1 212 ment a modellekhez (122 köteg, 10 vers/köteg), 1 vers (2Móz 35:36) nincs a TAHOT-ban, ezért `kezi` (l. 5.1). A brief 1Mózesre szóló számait (1 533 vers, 154 köteg) a 2Mózesre a könyv versszáma váltotta.
- **Új push-útvonal (`persist-credentials: false`).** Élesben működött: négy Actions-futás, mindegyik a `claude/f22-2moz` ágra pusholta vissza a kimenetét, `f22/` alatti változással; a kulcs-grep mindig tiszta. A workflow ehhez minden `claude/f22-*` ágra kiterjesztve (`startsWith`; a push `$GITHUB_REF`-re).
- **Az elvetett első próbák naplózása aktív:** `f22/elvetett/2Moz_<köteg>.txt`, a futásnapló `ok` oszlopa (kapu / parse / api). A C-oldalon a 2Móz alatt 48 köteghez van elvetett nyers válasz (`f22/elvetett/2Moz_*.txt`); a futásnapló `ok` oszlopa szerint 50 hívás kapuhiba, 3 hívás parse-hiba (a könyv 171 C-hívásából).
- **Keret a /usage szerint (`get_usage`, heti „all models”):**

| időpont | heti keret | 5 órás ablak |
|---|---|---|
| a menet elején | 43% | 13% |
| a 14 köteg (próbaszakasz) után | 44% | 19% |
| a menet végén (122 köteg) | 49% | 60% |

  A mért heti fogyás a teljes 2Mózesre **6 százalékpont** (egész százalékos kerekítés: 5–7 pont), a 30%-os keretszabály alatt. A próbaszakasz vetítése (kb. 9 pont) nagyjából egyezett.

## 2. Próbaszakasz (22.2): az első 14 köteg

**Szkriptkimenet (`f22_statisztika.py --konyv 2Móz --ig-koteg 14 --vetit 1213`):**

```
Sonnet: 14 köteg, 140 vers; kapuhiba első próbára 1.4% (2/140); végleg 0.0% (0/140)
C: 14 köteg, 140 vers; kapuhiba első próbára 16.4% (23/140); végleg 0.0% (0/140)
C költség: 0.221374 USD, 20 hívás, bemenet 187745, kimenet 25155 (ebből gondolkodás 0) token
C költség vetítve 1213 versre: 1.9180 USD
```

**⛔ 1. megállás feltételei** (egyik sem teljesült): vetített heti fogyás kb. 9 pont (küszöb 30), Sonnet végleges kapuhiba 0,0% (küszöb 5%), C költségvetítés 1,92 USD (küszöb 3,90). A 22.3 megállás nélkül folytatódott; a próbaszakasz után a C a teljes könyvre indult.

## 3. A teljes futás (22.3)

**Szkriptkimenet (`f22_statisztika.py --konyv 2Móz`):**

```
Sonnet: 122 köteg, 1212 vers; kapuhiba első próbára 0.8% (10/1212); végleg 0.0% (0/1212)
C: 122 köteg, 1212 vers; kapuhiba első próbára 11.9% (144/1212); végleg 0.7% (9/1212)
C költség: 1.851702 USD, 171 hívás, bemenet 1553010, kimenet 207416 (ebből gondolkodás 0) token
```

- **Költség (C):** a futásnapló szerint a 2Móz C-költsége a `c/2Moz` sorokra összegezve 1,8517 USD, a könyv plafonja 2,69 USD (DT-F22d, l. 5.2); a teljes napló összege (1Móz + 2Móz) 4,1237 USD.
- **Hash (K3):** a `prompt_v3` hash-e a C-futás elején és végén mindegyik Actions-futásban rendben („a futás végén: RENDBEN”); a Sonnet-oldalon a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte, és a menet végén is `None` (nincs eltérés) a hash-ellenőrzés kimenete.
- **Futások és megszakadások.** (a) A C-futás a 104. kötegnél `KeyError`-ral leállt (2Móz 35:36, 5.1), ezt javítottam; (b) a 106. kötegnél a költségplafon megállította (a plafon az egész napló összegét számolta, 3,8982 USD az 1Móz 2,27 USD-jével együtt, 5.2); a felhasználó döntése után (A változat) a futás a 106. kötegtől folytatódott (a 105. kész volt), a kész kötegeket kihagyva. Sonnet-oldalon megszakadás nem volt; az újrapróbák kötegenként egy újrakéréssel (a brief szerint), végleges kapuhiba 0.
- **Egyesítés (`egyesit.py --konyv 2Móz`):** `parok_2Moz.tsv` 24 487 sor (magas 23 265, alacsony 1 222), `szavak_2Moz.tsv` 49 396 sor (magas 44 591, alacsony 4 805, kezi 0), átnézési sor 0 vers (`naplok/F22_2Moz_atnezes.tsv` csak fejléc); a fő menet (122 köteg) + a javító menet (38 vers, l. 5.1) együtt; `egyesit.py --ellenoriz`: „rendben” (minden Károli- és eredeti token pontosan egyszer szerepel, a `strong` a TAHOT-ból levezethető; K1, K2); az újraépítés API nélkül bájtra azonos táblákat adott (K7); az 1Móz táblák változatlanok, `--ellenoriz` rendben.
- **Önteszt-kimenetek** (mind „rendben”): `kapu.py`, `futtat.py`, `f22_c_futtat.py`, `sonnet_koteg.py`, `egyesit.py`, `zart_osszevet.py`. A kulcs-grep az `f22/`, `adat/karoli_strong/`, `naplok/` és `eszkozok/karoli_strong/` alatt tiszta.

## 4. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Móz` kimenetéből.*

### 4.1 Arányok

Összesen: linkek (parok): magas 95.0% (23265/24487), alacsony 5.0% (1222/24487), kezi 0.0% (0/24487); szavak (tokenek, Károli és eredeti együtt): magas 90.3% (44591/49396), alacsony 9.7% (4805/49396), kezi 0.0% (0/49396).

Link-forrás megoszlás (parok): S 1222, S+C 23265. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 2 (2Móz 29:5, 2Móz 39:19).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 348 | 96.6% (336/348) | 3.4% (12/348) | 0.0% (0/348) | 718 | 89.8% (645/718) | 10.2% (73/718) | 0.0% (0/718) |
| 2 | 507 | 96.6% (490/507) | 3.4% (17/507) | 0.0% (0/507) | 1083 | 91.5% (991/1083) | 8.5% (92/1083) | 0.0% (0/1083) |
| 3 | 571 | 96.5% (551/571) | 3.5% (20/571) | 0.0% (0/571) | 1148 | 92.9% (1067/1148) | 7.1% (81/1148) | 0.0% (0/1148) |
| 4 | 709 | 95.8% (679/709) | 4.2% (30/709) | 0.0% (0/709) | 1391 | 91.7% (1275/1391) | 8.3% (116/1391) | 0.0% (0/1391) |
| 5 | 496 | 94.2% (467/496) | 5.8% (29/496) | 0.0% (0/496) | 955 | 89.1% (851/955) | 10.9% (104/955) | 0.0% (0/955) |
| 6 | 563 | 98.4% (554/563) | 1.6% (9/563) | 0.0% (0/563) | 1122 | 93.3% (1047/1122) | 6.7% (75/1122) | 0.0% (0/1122) |
| 7 | 574 | 96.0% (551/574) | 4.0% (23/574) | 0.0% (0/574) | 1113 | 93.6% (1042/1113) | 6.4% (71/1113) | 0.0% (0/1113) |
| 8 | 787 | 95.4% (751/787) | 4.6% (36/787) | 0.0% (0/787) | 1510 | 93.2% (1408/1510) | 6.8% (102/1510) | 0.0% (0/1510) |
| 9 | 765 | 95.4% (730/765) | 4.6% (35/765) | 0.0% (0/765) | 1544 | 92.0% (1420/1544) | 8.0% (124/1544) | 0.0% (0/1544) |
| 10 | 742 | 97.2% (721/742) | 2.8% (21/742) | 0.0% (0/742) | 1454 | 92.0% (1338/1454) | 8.0% (116/1454) | 0.0% (0/1454) |
| 11 | 256 | 98.4% (252/256) | 1.6% (4/256) | 0.0% (0/256) | 497 | 89.5% (445/497) | 10.5% (52/497) | 0.0% (0/497) |
| 12 | 1117 | 94.5% (1056/1117) | 5.5% (61/1117) | 0.0% (0/1117) | 2171 | 89.5% (1944/2171) | 10.5% (227/2171) | 0.0% (0/2171) |
| 13 | 518 | 92.9% (481/518) | 7.1% (37/518) | 0.0% (0/518) | 1007 | 88.8% (894/1007) | 11.2% (113/1007) | 0.0% (0/1007) |
| 14 | 721 | 95.7% (690/721) | 4.3% (31/721) | 0.0% (0/721) | 1450 | 93.6% (1357/1450) | 6.4% (93/1450) | 0.0% (0/1450) |
| 15 | 475 | 97.7% (464/475) | 2.3% (11/475) | 0.0% (0/475) | 938 | 93.7% (879/938) | 6.3% (59/938) | 0.0% (0/938) |
| 16 | 788 | 94.4% (744/788) | 5.6% (44/788) | 0.0% (0/788) | 1594 | 89.3% (1424/1594) | 10.7% (170/1594) | 0.0% (0/1594) |
| 17 | 372 | 97.3% (362/372) | 2.7% (10/372) | 0.0% (0/372) | 735 | 93.1% (684/735) | 6.9% (51/735) | 0.0% (0/735) |
| 18 | 599 | 93.8% (562/599) | 6.2% (37/599) | 0.0% (0/599) | 1219 | 87.9% (1072/1219) | 12.1% (147/1219) | 0.0% (0/1219) |
| 19 | 536 | 95.9% (514/536) | 4.1% (22/536) | 0.0% (0/536) | 1097 | 92.0% (1009/1097) | 8.0% (88/1097) | 0.0% (0/1097) |
| 20 | 469 | 96.2% (451/469) | 3.8% (18/469) | 0.0% (0/469) | 931 | 93.6% (871/931) | 6.4% (60/931) | 0.0% (0/931) |
| 21 | 668 | 94.8% (633/668) | 5.2% (35/668) | 0.0% (0/668) | 1280 | 89.2% (1142/1280) | 10.8% (138/1280) | 0.0% (0/1280) |
| 22 | 558 | 96.6% (539/558) | 3.4% (19/558) | 0.0% (0/558) | 1054 | 90.5% (954/1054) | 9.5% (100/1054) | 0.0% (0/1054) |
| 23 | 650 | 98.0% (637/650) | 2.0% (13/650) | 0.0% (0/650) | 1230 | 92.1% (1133/1230) | 7.9% (97/1230) | 0.0% (0/1230) |
| 24 | 361 | 95.3% (344/361) | 4.7% (17/361) | 0.0% (0/361) | 756 | 92.5% (699/756) | 7.5% (57/756) | 0.0% (0/756) |
| 25 | 663 | 92.5% (613/663) | 7.5% (50/663) | 0.0% (0/663) | 1299 | 88.5% (1150/1299) | 11.5% (149/1299) | 0.0% (0/1299) |
| 26 | 646 | 94.9% (613/646) | 5.1% (33/646) | 0.0% (0/646) | 1391 | 92.2% (1282/1391) | 7.8% (109/1391) | 0.0% (0/1391) |
| 27 | 387 | 96.6% (374/387) | 3.4% (13/387) | 0.0% (0/387) | 786 | 93.0% (731/786) | 7.0% (55/786) | 0.0% (0/786) |
| 28 | 837 | 95.1% (796/837) | 4.9% (41/837) | 0.0% (0/837) | 1736 | 88.9% (1543/1736) | 11.1% (193/1736) | 0.0% (0/1736) |
| 29 | 986 | 94.2% (929/986) | 5.8% (57/986) | 0.0% (0/986) | 2019 | 90.2% (1821/2019) | 9.8% (198/2019) | 0.0% (0/2019) |
| 30 | 701 | 94.6% (663/701) | 5.4% (38/701) | 0.0% (0/701) | 1380 | 87.1% (1202/1380) | 12.9% (178/1380) | 0.0% (0/1380) |
| 31 | 301 | 94.4% (284/301) | 5.6% (17/301) | 0.0% (0/301) | 658 | 84.8% (558/658) | 15.2% (100/658) | 0.0% (0/658) |
| 32 | 833 | 91.6% (763/833) | 8.4% (70/833) | 0.0% (0/833) | 1593 | 85.5% (1362/1593) | 14.5% (231/1593) | 0.0% (0/1593) |
| 33 | 532 | 95.3% (507/532) | 4.7% (25/532) | 0.0% (0/532) | 1068 | 90.3% (964/1068) | 9.7% (104/1068) | 0.0% (0/1068) |
| 34 | 769 | 97.3% (748/769) | 2.7% (21/769) | 0.0% (0/769) | 1543 | 91.0% (1404/1543) | 9.0% (139/1543) | 0.0% (0/1543) |
| 35 | 618 | 93.2% (576/618) | 6.8% (42/618) | 0.0% (0/618) | 1346 | 85.3% (1148/1346) | 14.7% (198/1346) | 0.0% (0/1346) |
| 36 | 657 | 91.8% (603/657) | 8.2% (54/657) | 0.0% (0/657) | 1387 | 86.6% (1201/1387) | 13.4% (186/1387) | 0.0% (0/1387) |
| 37 | 527 | 93.7% (494/527) | 6.3% (33/527) | 0.0% (0/527) | 1067 | 90.2% (962/1067) | 9.8% (105/1067) | 0.0% (0/1067) |
| 38 | 556 | 93.2% (518/556) | 6.8% (38/556) | 0.0% (0/556) | 1205 | 87.7% (1057/1205) | 12.3% (148/1205) | 0.0% (0/1205) |
| 39 | 730 | 90.8% (663/730) | 9.2% (67/730) | 0.0% (0/730) | 1608 | 88.6% (1424/1608) | 11.4% (184/1608) | 0.0% (0/1608) |
| 40 | 594 | 94.6% (562/594) | 5.4% (32/594) | 0.0% (0/594) | 1313 | 90.7% (1191/1313) | 9.3% (122/1313) | 0.0% (0/1313) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): nincs.

### 4.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 6; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 83.3% (5/6).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 83.3% (5/6).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): 83.3% (5/6).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 83.3% (5/6).

### 4.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 2441; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 1862. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|
| 1 | a | betoldas | H0834 | 38 | 2Móz 1:15 |
| 2 | azért | H9001 | betoldas | 25 | 2Móz 1:11 |
| 3 | és | H9002 | H9002 | 24 | 2Móz 1:14 |
| 4 | is | betoldas | H9001 | 16 | 2Móz 8:7 |
| 5 | is | betoldas | H9002 | 16 | 2Móz 9:25 |
| 6 | is | H9002 | betoldas | 15 | 2Móz 25:11 |
| 7 | mint | H0834+H9004 | H0834 | 15 | 2Móz 7:10 |
| 8 | akkor | H9001 | betoldas | 12 | 2Móz 3:18 |
| 9 | hogy | H9001 | betoldas | 12 | 2Móz 1:7 |
| 10 | is | H9001 | betoldas | 12 | 2Móz 25:13 |
| 11 | a | H0834+H9004 | H9004 | 11 | 2Móz 7:13 |
| 12 | a | H0834 | betoldas | 10 | 2Móz 12:16 |
| 13 | a | betoldas | H9003 | 8 | 2Móz 5:13 |
| 14 | a | betoldas | H9009 | 8 | 2Móz 1:22 |
| 15 | azután | H9001 | betoldas | 8 | 2Móz 32:6 |
| 16 | és | betoldas | H9002 | 8 | 2Móz 5:2 |
| 17 | a | betoldas | H9004 | 7 | 2Móz 7:10 |
| 18 | az | betoldas | H1931 | 7 | 2Móz 1:6 |
| 19 | e | H2088+H9009 | H2088 | 7 | 2Móz 3:21 |
| 20 | is | H9002 | H9002 | 6 | 2Móz 25:29 |

## 5. Tételek és döntési helyőrzők

### 5.1 Versszám-eltolódás: a Károli 35:36 – 36:37 a TAHOT 36:1 – 36:38 (javítva: javító menet)

**Tény (az ellenőri kör találata, az adatból igazolva; a detektor, 5.5, ugyanezt találja meg):** a Károli 2Móz 35:36 szövege a TAHOT 36:1-nek felel meg, és a Károli 36:n a TAHOT 36:(n+1)-nek (n = 1–37); a Károli 37:1-től a két beosztás ismét egyezik. (Az első menetben ezt tévesen úgy írtam le, hogy a Károli kettébontja a héber 35:35-öt; az ellenőr cáfolta.)

**Javítás (a felhasználó utasítására, PR #114 merge előtt):** a 38 vers (Károli 35:36, 36:1–37) a **helyes megfeleltetéssel**, ugyanazzal a prompttal (`prompt_v3`) és modellpárral újrafutott (**javító menet**, könyv-kulcs `2Móz_javito`: `f22/minta_2Moz_javito.tsv`, `f22/valaszok/{sonnet,c}/2Moz_javito.jsonl`, 4 köteg). A megfeleltetést a futtató a detektor listájából (`f22/versmegfeleltetes.tsv`) kapja (`tokenek.betolt_eredeti`: a Károli-vers a megfeleltetett eredeti verset kapja; ahol nincs megfeleltetés, ott a vers a modellmintán kívül marad, és az egyesítő `kezi`-be teszi). Az egyesítő a javító menet válaszát versenként felülírja a fő menetét. A hamis linkek (a fő menet eltolt bemenetre adott válaszai erre a 38 versre) így **nincsenek a táblákban** (a táblák újraépítve); a nyers válaszok a fő menet jsonl-jében az audit miatt megmaradnak, de az egyesítő nem használja őket.

**Szkriptkimenet (`f22_statisztika.py --konyv 2Móz_javito`):**

```
Sonnet: 4 köteg, 38 vers; kapuhiba első próbára 2.6% (1/38); végleg 0.0% (0/38)
C: 4 köteg, 38 vers; kapuhiba első próbára 0.0% (0/38); végleg 0.0% (0/38)
C költség: 0.044636 USD, 4 hívás, bemenet 32721, kimenet 5359 (ebből gondolkodás 0) token
```

**Hatás:** a 36. fejezetben a linkek `magas` aránya 42,7%-ról (eltolt bemenet) 91,8%-ra (657 link, 603 `magas`) javult; a 35. fejezet 93,2%; a „gyanús fejezet” sor a 2Mózesre: nincs. A `kezi` szavak száma 1 456-ról 0-ra, az átnézési sor 39 versről 0-ra csökkent. (A korábbi, ideiglenes `kezi`-felülírás — `f22/kezi_versek_2Moz.tsv` — törölve; az `egyesit.kezi_felulir()` általános kód marad, a fájl hiánya üres halmaz.)

### 5.2 DT-F22d (helyőrző) — a C-költségplafon könyvenként

A korábbi plafon (3,90 USD küszöb, 4,00 USD kemény) az egész napló összegét korlátozta, így a 2Móz a 106. kötegnél megállt. A felhasználó döntése (A változat, kiegészítve): **a plafon könyvenkénti: a könyv versszáma × (2,27 / 1533) × 1,5 USD, de legalább 1,00 USD**; a futtató csak az adott könyv (`c/<könyv>`) naplósorait összegzi (`futtat.naplo_osszeg(…, futas)`); **külön összesített felső korlát: 60 USD a teljes naplóra**, elérésekor a futás megáll (kilépési kód 3). A 2Mózesre a képlet 2,69 USD; a mért költség 1,8517 USD. A vezérlőfájl `plafon_usd=auto` a képletet adja, egy szám szigorúbb értéket (0 < x ≤ 60). Az önteszt (`f22_c_futtat.py --onteszt`) lefedi a képletet, az `auto` értelmezését, a más könyv sorait kizáró összegzést és az összesített korlátot; a régi (F21) ág a `plafon_futas` nélkül változatlan. A szabály a brief döntésnaplójában D8 (DT-F22d helyőrző); a végleges számot a `DONTESEK.md`-ben a main-Action adja a merge után.

### 5.3 A páratlan versek listája a teljes Bibliára (Károli-kulcs)

`naplok/F22_nincs_parja_versek.tsv` (generálja: `eszkozok/karoli_strong/eredeti_nelkuli_lista.py`, API nélkül): azok a Károli-versek, amelyeknek nincs TAHOT/TAGNT-versük, és fordítva. A futtató az ilyen verseket eleve kihagyja a modellmintából (`sonnet_koteg.minta_epit` / `eredeti_nelkuli_versek`), az egyesítő pedig `kezi` állapotba teszi (`karoli_nelkuli_eredeti_versek`). Darabszámok (a fájl összesítő sorai):

```
ÖSSZESÍTŐ könyvenként (irany, konyv: vers_db, token_db)
karoli_eredeti_nelkul	2Kor	1 vers	16 token
karoli_eredeti_nelkul	2Móz	1 vers	36 token
karoli_eredeti_nelkul	3Ján	1 vers	12 token
karoli_eredeti_nelkul	Dán	3 vers	55 token
karoli_eredeti_nelkul	Fil	2 vers	25 token
karoli_eredeti_nelkul	Hós	1 vers	28 token
karoli_eredeti_nelkul	Jel	1 vers	5 token
karoli_eredeti_nelkul	Ján	1 vers	4 token
karoli_eredeti_nelkul	Jób	39 vers	432 token
karoli_eredeti_nelkul	Préd	5 vers	71 token
karoli_eredeti_nelkul	Róm	3 vers	58 token
karoli_eredeti_nelkul	Én	3 vers	53 token
eredeti_karoli_nelkul	1Kor	1 vers	6 token
eredeti_karoli_nelkul	2Móz	1 vers	22 token
eredeti_karoli_nelkul	4Móz	1 vers	24 token
eredeti_karoli_nelkul	Dán	3 vers	106 token
eredeti_karoli_nelkul	Hós	3 vers	60 token
eredeti_karoli_nelkul	Jób	7 vers	69 token
eredeti_karoli_nelkul	Préd	6 vers	146 token
eredeti_karoli_nelkul	Péld	1 vers	9 token
eredeti_karoli_nelkul	Róm	2 vers	34 token
eredeti_karoli_nelkul	Én	3 vers	47 token
eredeti_karoli_nelkul	Ézs	2 vers	44 token
ÖSSZESEN	karoli_eredeti_nelkul	61 vers	795 token
ÖSSZESEN	eredeti_karoli_nelkul	30 vers	567 token
```

Az 1Móz nem érintett (táblái az új kóddal bájtra azonosak maradtak). **Hatókör:** a lista csak azokat a verseket találja meg, amelyeknek a Károli-kulcson nincs párjuk; a fejezeten belüli eltolódást nem — ezt a versbeosztás-detektor (5.5) pótolja, amelynek gépi listáját a futtató használja (ezért a lista maga már csak tájékoztató).

### 5.4 Kereszttábla az aranyhoz (DT-F22c: marad-e a Gemini)

A régi arany (`Karoli_Strong_kivonat.tsv`) hármasain, modellenként külön (`f22_arany_kereszt.py --konyv 1Móz --konyv 2Móz`; halmaz-szabály, kizárás nélkül; ahol a vers valamelyik modell oldalán kapuhibás, a hármas külön sorba kerül):

```
1Móz: n=193 | mindkettő egyezik 187 | csak a Sonnet 0 | csak a C 0 | egyik sem 6 | (nincs választ: 1, a kifejezés nincs a versben: 0)
2Móz: n=6 | mindkettő egyezik 5 | csak a Sonnet 0 | csak a C 0 | egyik sem 1 | (nincs választ: 0, a kifejezés nincs a versben: 0)
ÖSSZESEN: n=199 | mindkettő egyezik 192 | csak a Sonnet 0 | csak a C 0 | egyik sem 7
Sonnet egyezés: 96.5% (192/199); C egyezés: 96.5% (192/199)
```

Az arany ezen a két könyvön **nem választja szét** a két modellt: nincs olyan hármas, ahol az egyik egyezik, a másik nem; a 7 „egyik sem” hármas mindkét modellnél ugyanaz (az 1Móz 6:17 aranyhiba és társai, l. `F22_DT-F22b_javaslat.md`). A 2Mózesre az arany csak 6 hármast ad, így a kereszttábla itt csak tájékoztató. A modellek közti különbséget az `alacsony` tokenek mutatják (2.3/4.3: a C gyakrabban `betoldas`-t vagy más eredetit köt); hogy az eltéréseknél melyik oldal a pontosabb, az a zárt összevetésből (6. szakasz) mérhető, amely a `magas`/`alacsony` kereszttáblát adja.

### 5.5 Versbeosztás-detektor (`eszkozok/karoli_strong/versbeosztas.py`)

A teljes Bibliára, könyvenként és fejezetenként, csak számokkal: **`naplok/F22_versbeosztas.md`** (generált; gépi lista: `f22/versmegfeleltetes.tsv`, 308 sor). Módszer: a két versfolyamot (Károli; eredeti, **fejezet és vers szerint rendezve**, mert a TAHOT-kivonat fájlsorrendje nem megbízható, pl. az 1Móz 32 a fájlban máshol áll, mint a sorrendben) a vershossz (szószám) logaritmusa szerint párosítja dinamikus programozással; a versszám csak döntetlen-feloldó, ezért az **azonos versszámú, de eltolt tartalom** is kiderül; ezt kiegészíti a fejezet szintű hosszkorreláció (`KORR_ELT`, `GYENGE`). Önteszt: azonos folyam → nincs jelzés; azonos versszámú, eggyel eltolt tartalom → jelzi; a valódi adaton az 1Móz tiszta, a 2Móz 35:36–36:37 megvan.

**Összesen (szkriptkimenet):** 1 189 fejezet, 95 jelzett fejezet; 250 eltolt pár, 43 Károli-vers eredeti nélkül, 12 eredeti vers Károli nélkül.

**1Mózes (külön jelezve):** 50 fejezet, **0 jelzett fejezet**, 0 eltolt pár, 0 hiány — az 1Móz Károli- és eredeti versbeosztása egyezik (a táblái ezért változatlanok).
**2Mózes (külön jelezve):** 40 fejezet, **2 jelzett fejezet (35, 36)**, 38 eltolt pár (Károli 35:36 → 36:1, 36:n → 36:(n+1), n = 1–37), 0 hiány; ez a 38 vers a javító menet tárgya (5.1).

Más könyvek (összesen, a `naplok/F22_versbeosztas.md` 1. szakasza szerint): 4Móz: 16 eltolt pár, 1 eredeti vers Károli nélkül (30. fejezet); Jób: 9 eltolt, 34 Károli-hiány, 2 eredeti-hiány, 15 jelzett fejezet; Zsolt: 27 jelzett fejezet (0 eltolt pár: a hossz-jelzés gyenge illeszkedést mutat); Péld: 18 jelzett fejezet; Préd: 65 eltolt pár; Én 13; Ézs 28; Dán 37; Hós 44 eltolt pár; Sir: 4 jelzett fejezet; a többi könyvben csak kisszámú Károli-/eredeti-hiány (Ján, Róm, 1Kor, 2Kor, Fil, 3Ján, Jel) vagy semmi. **A 3Móz tiszta (0 jelzés).** A listát a futtató minden könyvre alkalmazza (`tokenek.betolt_eredeti`), tehát a későbbi könyvek futása már a megfeleltetett verset kapja; az 1Móz és a 3Móz listája üres.

## 6. Független szúrópróba (22.6)

A `zart_osszevet.py` a 2Mózesre is fut (`--konyv 2Móz --bemenet <repón kívüli fájl>`; fejezet-mód: nyers, bemásolt fejezetszöveg, `== 2Móz 5 ==` fejléc). A zárt forrás adata nem került a repóba. **A felhasználó tölti ki:** *(még nincs)*

## 7. Eltérések a briefhez és nyitott kérdések

1. **Minta: 1 212 modellvers + 38 javító-menet vers** (5.1): a fő minta 35:36-ot nem tartalmazza (a futás idején nem volt eredeti verse), a 36:1–37 fő-menet válaszait a javító menet felülírja, a brief „`--var 1213`” ellenőrzése a modellmintát + a kimaradt versek számát veti össze.
2. **Új/módosított fájlok a brief `ir` listáján kívül:** `eredeti_nelkuli_lista.py`, `f22_arany_kereszt.py`, `naplok/F22_nincs_parja_versek.tsv`, a `futtat.py` és `egyesit.py` módosítása (plafon, páratlan versek); a brief `ir` listája bővítve. Az 1Móz kimenetei bájtra változatlanok.
3. **A Sonnet-subagentek segédszkriptje.** A 105. és 106. köteg subagentje a kézzel eldöntött párokat egy ideiglenes szkripttel írta JSON-ba (`f22/_munka/`, nem verziózott); a szkript nem párosít, csak a modell döntését szerializálja.
4. **A DT-F22c nyitva:** a Gemini-döntéshez a 5.4 szám és a felhasználó zárt összevetése kell.
5. **A bemenet KJV nélküli** (mint az 1Mózesnél, DT-F22a).
6. **E16 (CI).** A PR a `.github/workflows/f22_parositas.yml`-t érinti, ezért a címnek `[ELLENŐRZŐ]` előtaggal kell kezdődnie (az ellenőr E16-futtatása szerint); a draft PR címe ezt tartalmazza.
7. **Az ellenőri kör.** Az ellenőr nem futtathatott szkriptet (szerepköre csak olvasó); az `egyesit.py --ellenoriz`, a bájtazonos újraépítés, az öntesztek és a statisztika-szkriptek futtatását én végeztem, kimenetük a 3–4. szakaszban van. Egy második, független kör az ellenőri javítások után nem készült (a főbb javítások: 5.1 kezelése, önteszt, docstring, workflow, brief). A PR-hoz fűzött utasítás szerinti **második, független kör** a javító menet és a detektor után készült: `naplok/ELLENOR_F22_2Moz_2.md`.
8. **A versmegfeleltetés globális hatása.** A `tokenek.betolt_eredeti()` alapértelmezetten a `f22/versmegfeleltetes.tsv` szerint képez (a detektor `versmegf=False`-szal a nyers folyamot olvassa); a lista az 1Mózest és a 3Mózest nem érinti. A régi F21-mérőeszközök újrafuttatása a más könyvekben érintett versekre eltérő bemenetet adna (a lezárt F21 kimenetek nem változnak).
9. **Pszeudo-könyvkulcs.** A javító menet a `2Móz_javito` kulccsal fut (fájlnevek, `futas`: `c/2Moz_javito`); a költségplafon rá 1,00 USD (a képlet minimuma), a mért költség 0,0446 USD.
