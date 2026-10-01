# F22_1Moz_jelentes.md — Károli–Strong párosítás: 1Mózes

*A számok kizárólag szkriptkimenetből jönnek (`eszkozok/karoli_strong/f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`). Állapot: a menet közben épül; a 2. szakasz a 22.5-ben készül.*

## 1. Próbaszakasz (22.2): az első 14 köteg

**Hatókör.** A brief „1Móz 1–5, 138 vers, 14 köteg” megnevezése és a 10 verses kötegelés nem esik egybe: az első 14 köteg 140 vers (az 1–5. fejezet 138 verse + 1Móz 6:1–2). Mindkét modell ugyanezt a 14 kötegét futtatta; a vetítés a ténylegesen futtatott 140 versre épül (×1 533/140).

**Beállítások.** Prompt: `f21p/prompt_v3.md` (hash a futás elején rendben). Bemenet KJV-támpont nélkül (a brief szerint a KJV a promptban nem igazolt; a pilot Sonnet- és C-futásai a KJV-sort ott adták, ahol volt). Sonnet: `vegrehajto-sonnet` subagentek, kötegenként egy, sorban. C: `google/gemini-3.8-flash`, GitHub Actions, kötelező minimális gondolkodási szint (`kotelezo_effort=minimal`).

**Szkriptkimenet (`f22_statisztika.py --konyv 1Móz --ig-koteg 14 --vetit 1533`):**

```
Sonnet: 14 köteg, 140 vers; kapuhiba első próbára 0.7% (1/140); végleg 0.0% (0/140)
C: 14 köteg, 140 vers; kapuhiba első próbára 6.4% (9/140); végleg 0.0% (0/140)
C költség: 0.183644 USD, 17 hívás, bemenet 146937, kimenet 21053 (ebből gondolkodás 0) token
C költség vetítve 1533 versre: 2.0109 USD
```

**A /usage állása** (`get_usage`, a heti keret „all models” ablaka; az érték egész százalék):

| időpont | heti keret | 5 órás ablak |
|---|---|---|
| a menet kezdetén (az 1. köteg előtt, az előkészítés — minta, szkriptek, workflow — után) | 36% | 22% |
| a 14 köteg után | 37% | 25% |

A mért heti fogyás a 14 kötegre 1 százalékpont (az egész százalékos kerekítés miatt 0–2 pont közötti valódi érték), az 5 órás ablakban 3 pont. Vetítés a teljes 1Mózesre (×1 533/140 ≈ 10,95): kb. 11 százalékpont (0–22 pont sáv) a heti keretből. A 30%-os küszöb a heti keret százalékpontjára vonatkozik; a mérés durvasága miatt a 22.3 alatt a `/usage`-t kötegcsoportonként újramérem.

**⛔ 1. megállás feltételei** (egyik sem teljesül):

| feltétel | mért/vetített | küszöb | teljesül? |
|---|---|---|---|
| vetített keretfogyás | kb. 11 pont (sáv: 0–22) | > 30% | nem |
| Sonnet végleges kapuhiba | 0,0% | > 5% | nem |
| C költségének vetítése | 2,01 USD | > 3,90 USD | nem |

A 22.3 megállás nélkül folytatódik.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Móz` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 93.6% (29579/31613), alacsony 6.4% (2034/31613), kezi 0.0% (0/31613); szavak (tokenek, Károli és eredeti együtt): magas 88.6% (54710/61716), alacsony 11.4% (7006/61716), kezi 0.0% (0/61716).

Link-forrás megoszlás (parok): S 2034, S+C 29579. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 4 (1Móz 28:11, 1Móz 43:32, 1Móz 48:19, 1Móz 7:22).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 621 | 95.7% (594/621) | 4.3% (27/621) | 0.0% (0/621) | 1304 | 90.6% (1181/1304) | 9.4% (123/1304) | 0.0% (0/1304) |
| 2 | 482 | 93.8% (452/482) | 6.2% (30/482) | 0.0% (0/482) | 1021 | 90.9% (928/1021) | 9.1% (93/1021) | 0.0% (0/1021) |
| 3 | 514 | 95.7% (492/514) | 4.3% (22/514) | 0.0% (0/514) | 1062 | 91.8% (975/1062) | 8.2% (87/1062) | 0.0% (0/1062) |
| 4 | 509 | 94.7% (482/509) | 5.3% (27/509) | 0.0% (0/509) | 982 | 91.5% (899/982) | 8.5% (83/982) | 0.0% (0/982) |
| 5 | 467 | 97.9% (457/467) | 2.1% (10/467) | 0.0% (0/467) | 892 | 92.9% (829/892) | 7.1% (63/892) | 0.0% (0/892) |
| 6 | 452 | 96.9% (438/452) | 3.1% (14/452) | 0.0% (0/452) | 906 | 92.5% (838/906) | 7.5% (68/906) | 0.0% (0/906) |
| 7 | 517 | 87.8% (454/517) | 12.2% (63/517) | 0.0% (0/517) | 991 | 83.1% (824/991) | 16.9% (167/991) | 0.0% (0/991) |
| 8 | 467 | 89.1% (416/467) | 10.9% (51/467) | 0.0% (0/467) | 934 | 85.9% (802/934) | 14.1% (132/934) | 0.0% (0/934) |
| 9 | 531 | 94.4% (501/531) | 5.6% (30/531) | 0.0% (0/531) | 1038 | 87.6% (909/1038) | 12.4% (129/1038) | 0.0% (0/1038) |
| 10 | 367 | 95.1% (349/367) | 4.9% (18/367) | 0.0% (0/367) | 795 | 91.2% (725/795) | 8.8% (70/795) | 0.0% (0/795) |
| 11 | 515 | 95.1% (490/515) | 4.9% (25/515) | 0.0% (0/515) | 1031 | 92.3% (952/1031) | 7.7% (79/1031) | 0.0% (0/1031) |
| 12 | 419 | 96.2% (403/419) | 3.8% (16/419) | 0.0% (0/419) | 836 | 90.7% (758/836) | 9.3% (78/836) | 0.0% (0/836) |
| 13 | 367 | 93.2% (342/367) | 6.8% (25/367) | 0.0% (0/367) | 724 | 89.1% (645/724) | 10.9% (79/724) | 0.0% (0/724) |
| 14 | 461 | 96.3% (444/461) | 3.7% (17/461) | 0.0% (0/461) | 948 | 92.6% (878/948) | 7.4% (70/948) | 0.0% (0/948) |
| 15 | 375 | 89.1% (334/375) | 10.9% (41/375) | 0.0% (0/375) | 756 | 85.8% (649/756) | 14.2% (107/756) | 0.0% (0/756) |
| 16 | 355 | 94.6% (336/355) | 5.4% (19/355) | 0.0% (0/355) | 682 | 90.0% (614/682) | 10.0% (68/682) | 0.0% (0/682) |
| 17 | 605 | 96.7% (585/605) | 3.3% (20/605) | 0.0% (0/605) | 1086 | 93.4% (1014/1086) | 6.6% (72/1086) | 0.0% (0/1086) |
| 18 | 675 | 95.6% (645/675) | 4.4% (30/675) | 0.0% (0/675) | 1316 | 90.3% (1188/1316) | 9.7% (128/1316) | 0.0% (0/1316) |
| 19 | 900 | 94.7% (852/900) | 5.3% (48/900) | 0.0% (0/900) | 1764 | 90.0% (1587/1764) | 10.0% (177/1764) | 0.0% (0/1764) |
| 20 | 432 | 94.4% (408/432) | 5.6% (24/432) | 0.0% (0/432) | 807 | 89.7% (724/807) | 10.3% (83/807) | 0.0% (0/807) |
| 21 | 638 | 94.7% (604/638) | 5.3% (34/638) | 0.0% (0/638) | 1245 | 88.2% (1098/1245) | 11.8% (147/1245) | 0.0% (0/1245) |
| 22 | 541 | 92.4% (500/541) | 7.6% (41/541) | 0.0% (0/541) | 1086 | 87.2% (947/1086) | 12.8% (139/1086) | 0.0% (0/1086) |
| 23 | 429 | 96.0% (412/429) | 4.0% (17/429) | 0.0% (0/429) | 821 | 90.0% (739/821) | 10.0% (82/821) | 0.0% (0/821) |
| 24 | 1540 | 93.1% (1433/1540) | 6.9% (107/1540) | 0.0% (0/1540) | 2978 | 87.4% (2603/2978) | 12.6% (375/2978) | 0.0% (0/2978) |
| 25 | 578 | 95.5% (552/578) | 4.5% (26/578) | 0.0% (0/578) | 1157 | 91.4% (1058/1157) | 8.6% (99/1157) | 0.0% (0/1157) |
| 26 | 727 | 95.0% (691/727) | 5.0% (36/727) | 0.0% (0/727) | 1422 | 90.0% (1280/1422) | 10.0% (142/1422) | 0.0% (0/1422) |
| 27 | 1088 | 94.9% (1032/1088) | 5.1% (56/1088) | 0.0% (0/1088) | 2062 | 87.6% (1807/2062) | 12.4% (255/2062) | 0.0% (0/2062) |
| 28 | 510 | 88.0% (449/510) | 12.0% (61/510) | 0.0% (0/510) | 983 | 83.6% (822/983) | 16.4% (161/983) | 0.0% (0/983) |
| 29 | 697 | 90.1% (628/697) | 9.9% (69/697) | 0.0% (0/697) | 1384 | 86.6% (1198/1384) | 13.4% (186/1384) | 0.0% (0/1384) |
| 30 | 872 | 91.3% (796/872) | 8.7% (76/872) | 0.0% (0/872) | 1704 | 87.1% (1484/1704) | 12.9% (220/1704) | 0.0% (0/1704) |
| 31 | 1225 | 92.7% (1136/1225) | 7.3% (89/1225) | 0.0% (0/1225) | 2342 | 86.5% (2026/2342) | 13.5% (316/2342) | 0.0% (0/2342) |
| 32 | 682 | 94.1% (642/682) | 5.9% (40/682) | 0.0% (0/682) | 1329 | 88.7% (1179/1329) | 11.3% (150/1329) | 0.0% (0/1329) |
| 33 | 422 | 95.5% (403/422) | 4.5% (19/422) | 0.0% (0/422) | 837 | 88.8% (743/837) | 11.2% (94/837) | 0.0% (0/837) |
| 34 | 654 | 90.7% (593/654) | 9.3% (61/654) | 0.0% (0/654) | 1280 | 83.1% (1064/1280) | 16.9% (216/1280) | 0.0% (0/1280) |
| 35 | 566 | 95.9% (543/566) | 4.1% (23/566) | 0.0% (0/566) | 1099 | 91.7% (1008/1099) | 8.3% (91/1099) | 0.0% (0/1099) |
| 36 | 607 | 97.0% (589/607) | 3.0% (18/607) | 0.0% (0/607) | 1262 | 94.5% (1193/1262) | 5.5% (69/1262) | 0.0% (0/1262) |
| 37 | 779 | 96.1% (749/779) | 3.9% (30/779) | 0.0% (0/779) | 1519 | 90.8% (1379/1519) | 9.2% (140/1519) | 0.0% (0/1519) |
| 38 | 679 | 91.5% (621/679) | 8.5% (58/679) | 0.0% (0/679) | 1276 | 85.9% (1096/1276) | 14.1% (180/1276) | 0.0% (0/1276) |
| 39 | 574 | 94.1% (540/574) | 5.9% (34/574) | 0.0% (0/574) | 1086 | 84.5% (918/1086) | 15.5% (168/1086) | 0.0% (0/1086) |
| 40 | 463 | 92.0% (426/463) | 8.0% (37/463) | 0.0% (0/463) | 909 | 87.3% (794/909) | 12.7% (115/909) | 0.0% (0/909) |
| 41 | 1090 | 94.7% (1032/1090) | 5.3% (58/1090) | 0.0% (0/1090) | 2256 | 90.9% (2051/2256) | 9.1% (205/2256) | 0.0% (0/2256) |
| 42 | 846 | 93.9% (794/846) | 6.1% (52/846) | 0.0% (0/846) | 1587 | 89.1% (1414/1587) | 10.9% (173/1587) | 0.0% (0/1587) |
| 43 | 817 | 89.5% (731/817) | 10.5% (86/817) | 0.0% (0/817) | 1578 | 85.0% (1342/1578) | 15.0% (236/1578) | 0.0% (0/1578) |
| 44 | 768 | 92.4% (710/768) | 7.6% (58/768) | 0.0% (0/768) | 1452 | 84.1% (1221/1452) | 15.9% (231/1452) | 0.0% (0/1452) |
| 45 | 646 | 91.3% (590/646) | 8.7% (56/646) | 0.0% (0/646) | 1217 | 87.2% (1061/1217) | 12.8% (156/1217) | 0.0% (0/1217) |
| 46 | 614 | 95.1% (584/614) | 4.9% (30/614) | 0.0% (0/614) | 1181 | 91.1% (1076/1181) | 8.9% (105/1181) | 0.0% (0/1181) |
| 47 | 832 | 91.8% (764/832) | 8.2% (68/832) | 0.0% (0/832) | 1579 | 87.9% (1388/1579) | 12.1% (191/1579) | 0.0% (0/1579) |
| 48 | 562 | 89.0% (500/562) | 11.0% (62/562) | 0.0% (0/562) | 1058 | 85.8% (908/1058) | 14.2% (150/1058) | 0.0% (0/1058) |
| 49 | 543 | 93.9% (510/543) | 6.1% (33/543) | 0.0% (0/543) | 1026 | 88.7% (910/1026) | 11.3% (116/1026) | 0.0% (0/1026) |
| 50 | 593 | 92.9% (551/593) | 7.1% (42/593) | 0.0% (0/593) | 1126 | 87.4% (984/1126) | 12.6% (142/1126) | 0.0% (0/1126) |

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 194; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 96.9% (188/194).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 96.4% (187/194).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): 97.0% (164/169).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 97.4% (188/193).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 3528; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 2649. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|
| 1 | a | betoldas | H0834 | 46 | 1Móz 1:11 |
| 2 | azért | H9001 | betoldas | 46 | 1Móz 6:12 |
| 3 | és | H9002 | H9002 | 28 | 1Móz 7:8 |
| 4 | monda | H0559 | H0559+H9001 | 17 | 1Móz 13:8 |
| 5 | tehát | H9001 | betoldas | 17 | 1Móz 1:12 |
| 6 | akkor | H9001 | betoldas | 15 | 1Móz 2:21 |
| 7 | és | betoldas | H9002 | 13 | 1Móz 14:1 |
| 8 | azért | betoldas | H9001 | 12 | 1Móz 6:13 |
| 9 | pedig | H9001 | betoldas | 11 | 1Móz 14:13 |
| 10 | ő | betoldas | H9033 | 11 | 1Móz 8:9 |
| 11 | az | betoldas | H1931 | 10 | 1Móz 2:19 |
| 12 | e | H2088+H9009 | H2088 | 10 | 1Móz 21:26 |
| 13 | földön | H0776+H5921+H9009 | H0776+H5921 | 10 | 1Móz 7:14 |
| 14 | és | H9001 | H9001 | 10 | 1Móz 4:14 |
| 15 | hogy | H9001 | betoldas | 9 | 1Móz 4:3 |
| 16 | a | H0834 | betoldas | 8 | 1Móz 7:2 |
| 17 | is | betoldas | H9002 | 8 | 1Móz 6:21 |
| 18 | vala | H2421 | betoldas | 8 | 1Móz 11:12 |
| 19 | vizek | H4325+H9009 | H4325 | 8 | 1Móz 7:17 |
| 20 | és | betoldas | H9005 | 8 | 1Móz 10:5 |

Megjegyzés a 2.3 táblához: a „típus” a magyar szó és a két modell Strong-jelöltje; ahol a két jelölt azonos (pl. `és` H9002 / H9002), a két modell ugyanazt a Strongot de **más eredeti tokenhez** kötötte (a partner-sorszám különbözik). Ilyen sor az eltérés-számba azért kerül, mert a bizonyosság token-szinten a partnerhalmaz azonosságán múlik.

## 3. A teljes futás összesítése (22.3)

**Szkriptkimenet (`f22_statisztika.py --konyv 1Móz`):**

```
Sonnet: 154 köteg, 1533 vers; kapuhiba első próbára 1.5% (23/1533); végleg 0.0% (0/1533)
C: 154 köteg, 1533 vers; kapuhiba első próbára 10.0% (153/1533); végleg 0.3% (4/1533)
C költség: 2.271972 USD, 216 hívás, bemenet 1932557, kimenet 259736 (ebből gondolkodás 0) token
```

- A C futásnapló (`f22/futasnaplo.tsv`): a gondolkodási mód minden hívásnál `kotelezo_effort=minimal`; két hívás `finish_reason=error` válasszal tért vissza (költség 0, a köteg újrapróbálva), a többi `stop`. A kumulatív költség a 3,90 USD küszöb és a 4,00 USD plafon alatt maradt (K5).
- A `prompt_v3` hash-e a C-futás elején és végén mindkét Actions-futásban egyezett (a futás naplója: „prompt_v3 hash: rendben”, „a futás végén: RENDBEN”); a Sonnet-oldalon a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte (hiba nélkül), a menet végén is rendben (K3).
- Az `OPENROUTER_API_KEY` repo-secret megvan (`gh secret list`, 2026-09-29-i létrehozás); a kulcs-grep mindkét futásban tisztát jelzett.
- A Sonnet-oldal 154 köteg = 154 `vegrehajto-sonnet` subagent, sorban, kötegenként egy; az újrakérést a subagent végezte a `sonnet_koteg.py mentes` hibaüzenete alapján (egy újrakérés kötegenként, a brief szerint). A subagentek csak a köteg promptját olvasták.
- Az újraépítés (`egyesit.py`) kétszeri futása bájtra azonos táblát adott (K7); `egyesit.py --ellenoriz` („rendben”): minden Károli- és eredeti token pontosan egyszer szerepel a `szavak_1Moz.tsv`-ben, és a `strong` oszlop minden értéke a TAHOT-ból levezethető (K1, K2). A `kezi` versek száma 0, tehát az átnézési sor (`naplok/F22_1Moz_atnezes.tsv`) üres (csak fejléc).
- Önteszt kimenetek (mind „önteszt: rendben”): `kapu.py`, `futtat.py`, `f22_c_futtat.py`, `sonnet_koteg.py`, `egyesit.py`, `zart_osszevet.py`.

**A /usage állása a menet végén** (heti keret „all models”): 41% (a menet elején 36%); 5 órás ablak 58% (a menet elején 22%). A teljes 1Mózesre a heti keretből mért fogyás tehát 5 százalékpont (egész százalékos kerekítéssel, tehát 4–6 pont), a 30%-os keretszabály alatt maradt; a menet közbeni 30%-os megállás nem jött el. A mért fogyásban benne van a menet teljes munkája (előkészítés, szkriptírás, a 154 subagent, az orkesztráló session), nem csak a subagenteké. A kötegcsoportonkénti mérés: 36% (kezdet) → 37% (14 köteg) → 37% (30) → 38% (50) → 39% (80) → 40% (100) → 40% (120) → 41% (154).

## 4. Független szúrópróba (22.6)

A `zart_osszevet.py` elkészült és mintaadaton tesztelve van (`--onteszt`: a szintetikus „zárt” fájl a **saját tábla** adataiból készül, a repón kívüli ideiglenes könyvtárban; zárt forrásból származó adat a menetben nem fordult meg). A szkript:

- a bemeneti fájl útvonalát parancssori paraméterként kapja (`--bemenet`), és megtagadja a futást, ha az a repón belül van;
- soronként egy verset vár, inline Strong-számokkal (`<7225>`, `{7225}`, `(7225)`, `[7225]`, `7225`, `H7225`), a sor elején igehellyel (`1Móz 1:1` vagy `Gen.1.1`), vagy igehely nélkül a `--sorrend` kapcsolóval;
- a vesszővel kapcsolt pár második tagját eldobja (`5647, 8799` → `5647`), és a `--max-strong` (alap 8674) fölötti számokat mindkét oldalon;
- csak összesített számot ír (egyezés %, n), külön a `magas` és az `alacsony` linkekre/tokenekre; versenkénti vagy szavankénti tartalmat nem ír, a hibaüzenetek sem idéznek a bemenetből.

**A felhasználó teendője (helyben):** a zárt forrásból kimásolt verseket a repón kívüli fájlba tenni, majd

```
python eszkozok/karoli_strong/zart_osszevet.py --konyv 1Móz --bemenet <a fájl útvonala>
```

futtatni, és az összesítést ide bemásolni. Ha a forrás jelölése eltér a fent felsoroltaktól, a `sor_elemzes` reguláris kifejezése bővíthető (a bemenet tartalmát a szkript nem naplózza).

**A zárt összevetés eredménye (a felhasználó tölti ki):** *(még nincs)*

## 5. Eltérések a briefhez és nyitott kérdések az orkesztrátornak

1. **Hatókör a próbaszakaszban.** A brief „1Móz 1–5, 138 vers, 14 köteg” megnevezése és a 10 verses kötegelés nem azonos: az első 14 köteg 140 vers (1Móz 6:1–2 is benne). A próbát az első 14 köteggel futtattam mindkét oldalon, a vetítést a ténylegesen futtatott 140 versre számoltam.
2. **KJV a bemenetben.** A brief „Mi nincs benne” szakasza szerint a KJV a promptban nem igazolt; ezért mindkét modell a `kjv=False` bemenetet kapta (a prompt befagyasztott példaversei a prompt_v3 szerint változatlanul tartalmazzák a KJV-támpont sort). A pilot 97,3% / 95,3% pontossága a mintán ott mért, ahol volt KJV-támpont (Gen/Exo/Pro); a KJV nélküli bemenet pontossága **nincs külön mérve**. Az 1Móz régi aranyon mért egyezés (2.2) és a zárt összevetés ad majd erre közvetett képet. Döntésre vár, ha a KJV-s bemenet visszakerülne.
3. **Új fájlok a brief `ir` listáján kívül.** A C-futtató (`eszkozok/karoli_strong/f22_c_futtat.py`, vékony burkoló a `futtat.py` fölött: a pilot `futtat.py` fix mintafájlra és `f21p/` kimenetre épül), a számokat előállító `f22_statisztika.py` és `f22_elemzes.py` nem szerepelt az `ir` listában; a brief szerint „a futtat.py újrahasználva”, számadat csak szkriptkimenetből jöhet a jelentésbe. A `futtat.py`-t nem módosítottam. Az `adat/datasetek.tsv` bejegyzése `ajanlott` / `korlatos` (nem `mindig`, hogy az `ellenoriz.py` 8. szabálya ne kezelje lekérdezés-kötelező datasetként); az `ellenoriz.py` ezután is 11 RENDBEN / 0 SÉRTÉS.
4. **Commit-üzenet.** A workflow commit-üzenet-sablonja `F22.3:` előtagot visel mindkét Actions-futásnál (a 22.2-es próbaszakasz kimenete is így van commitolva); a git-történetben ez a két gépi commit.
5. **Heti keret:** a mérés egész százalékos; a próbaszakasz 1 pontja 0–2 pontot jelentett volna, a végső 5 pont a pontosabb adat.
6. **Munkafájlok:** a Sonnet-subagentek munkafájljai (`f22/_munka/`) nincsenek verziózva (`.git/info/exclude`); a verziózott nyers válasz a `f22/valaszok/sonnet/1Moz.jsonl`.

**⛔ 2. megállás:** a jelentés elkészült; az ellenőri kör (22.7) után merge előtt a felhasználó dönt a 2Móz indításáról.
