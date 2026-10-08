# F22_Ezs_jelentes.md — Károli–Strong párosítás: Ézsaiás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Ézs`, `egyesit.py --ellenoriz --konyv <könyv>`, `f22_elemzes.py --konyv Ézs`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` összesítése). A futás ága: `claude/wonderful-einstein-ezr2pw` (a #77 ága, l. 4. pont), a jelentés ága: `claude/loving-cerf-dvm71f` (annak csúcsáról, `4d2f292`). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT-F77 (a), az első éles minta), **a C (Gemini) kimarad** (DT-F22c). A következő könyv sorrendje: DT57 (Ézs, utána Jer).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.08)**, a jóváhagyási naplóban (`naplok/F22_versbeosztas_jovahagyas.md`): a detektor az Ézs 9 és 64 fejezetben hibás volt, kézi javítás `f22/versmegfeleltetes_kezi.tsv`-ben, két 2:1 beolvasztás (`f22/versosszevonas.tsv`): a TAHOT Ézs 9:20 a Károli 9:20 15–34. szava, a TAHOT 64:2 a Károli 64:1 12–31. szava. Ellenőrzés a jóváhagyáskor: nyers 1 292 vers / 25 222 token = leképezett 1 290 vers / 25 180 token + 42 beolvasztott token.
- **Minta:** `f22/minta_Ezs.tsv`, 1 290 vers, 129 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01HEKmVhAaRF9zmDkMkSeFrH`, 129 kérés (2026-10-08T09:13Z); javító kör `msgbatch_01GF4UqJE45mzqsWhHcqk4pN`, 16 kérés (09:32Z).
- **Futásnapló** (`f22/api_termeles/futasnaplo.tsv`, 145 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `prompt_sha256_12` minden soron ugyanaz (`84f12ca7aafb`, ugyanaz az érték, mint a korábbi futásnaplóban, `f22/futasnaplo.tsv`). Az `api_koteg.prompt_szoveg` minden prompt előtt ellenőrzi a `prompt_v3.sha256`-ot (`sonnet_koteg.prompt_hash_hiba`, K3); az `f21p/` diffje üres.

| kör | kérés | kapun átment | kapun bukott (vers) | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 129 | 113 | 16 köteg (29 vers) | 6,7543 | 1 351 156 / 1 080 631 |
| 2. próba (javító) | 16 | 16 | 0 | 0,3291 | 193 661 / 27 094 |
| **összesen** | 145 | | | **7,0834** | |

A javító körbe került kötegek: 14, 21, 27, 33, 42, 45, 47, 54, 60, 62, 68, 73, 74, 81, 93, 94. A költség `batch_ar_szamolt` (a válasz tokenszámaiból, batch-árral); a 110 USD-s plafonból (F77.8) 7,08 fogyott. Előfizetési keret (`/usage`) nem fogyott; a K4 `/usage`-sora ezért itt az API-költség.

## 1a. Szkriptkimenet

```
Sonnet: 129 köteg, 1290 vers; kapuhiba első próbára 2.2% (29/1290); végleg 0.0% (0/1290)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Ézs`: `parok_Ezs.tsv` 25 488 link (mind `alacsony`, `S`), `szavak_Ezs.tsv` 50 069 sor. A szavak bontása: hu 24 847 (20 581 `parositva`, 4 226 `betoldas`, 40 `fuggoben`), er 25 222 (23 961 `parositva`, 1 219 `forditatlan`, 42 `fuggoben`); az er szám = a `TAHOT_kivonat.tsv` `Ézs ` sorainak száma (25 222). A `fuggoben` tokenek a két beolvasztott rész (20 + 20 Károli-szó, 42 héber szó); az átnézési sor (`naplok/F22_Ezs_atnezes.tsv`) ezt a két verset tartalmazza (Ézs 9:20, 64:1), link nélkül.

`egyesit.py --ellenoriz` (2026.10.08, ezen az ágon): 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs — mind „rendben” (minden Károli- és eredeti token pontosan egyszer szerepel, a `strong` a TAHOT-ból levezethető, az újraépítés bájtra azonos a commitolt táblával). Az `egyesit.py` proveniencia-fejlécének bővítése (API-futás, kézi versmegfeleltetés) a korábbi könyvek tábláit nem változtatta. `git diff f21p/` üres.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Ézs` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/25488), alacsony 100.0% (25488/25488), kezi 0.0% (0/25488); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/50069), alacsony 99.8% (49987/50069), kezi 0.2% (82/50069).

Link-forrás megoszlás (parok): S 25488. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 1290 (Ézs 10:1, Ézs 10:10, Ézs 10:11, Ézs 10:12, Ézs 10:13, Ézs 10:14, Ézs 10:15, Ézs 10:16, Ézs 10:17, Ézs 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 528 | 0.0% (0/528) | 100.0% (528/528) | 0.0% (0/528) | 1022 | 0.0% (0/1022) | 100.0% (1022/1022) | 0.0% (0/1022) |
| 2 | 379 | 0.0% (0/379) | 100.0% (379/379) | 0.0% (0/379) | 755 | 0.0% (0/755) | 100.0% (755/755) | 0.0% (0/755) |
| 3 | 381 | 0.0% (0/381) | 100.0% (381/381) | 0.0% (0/381) | 823 | 0.0% (0/823) | 100.0% (823/823) | 0.0% (0/823) |
| 4 | 141 | 0.0% (0/141) | 100.0% (141/141) | 0.0% (0/141) | 271 | 0.0% (0/271) | 100.0% (271/271) | 0.0% (0/271) |
| 5 | 608 | 0.0% (0/608) | 100.0% (608/608) | 0.0% (0/608) | 1189 | 0.0% (0/1189) | 100.0% (1189/1189) | 0.0% (0/1189) |
| 6 | 281 | 0.0% (0/281) | 100.0% (281/281) | 0.0% (0/281) | 566 | 0.0% (0/566) | 100.0% (566/566) | 0.0% (0/566) |
| 7 | 509 | 0.0% (0/509) | 100.0% (509/509) | 0.0% (0/509) | 969 | 0.0% (0/969) | 100.0% (969/969) | 0.0% (0/969) |
| 8 | 415 | 0.0% (0/415) | 100.0% (415/415) | 0.0% (0/415) | 818 | 0.0% (0/818) | 100.0% (818/818) | 0.0% (0/818) |
| 9 | 390 | 0.0% (0/390) | 100.0% (390/390) | 0.0% (0/390) | 825 | 0.0% (0/825) | 94.8% (782/825) | 5.2% (43/825) |
| 10 | 621 | 0.0% (0/621) | 100.0% (621/621) | 0.0% (0/621) | 1249 | 0.0% (0/1249) | 100.0% (1249/1249) | 0.0% (0/1249) |
| 11 | 335 | 0.0% (0/335) | 100.0% (335/335) | 0.0% (0/335) | 662 | 0.0% (0/662) | 100.0% (662/662) | 0.0% (0/662) |
| 12 | 102 | 0.0% (0/102) | 100.0% (102/102) | 0.0% (0/102) | 193 | 0.0% (0/193) | 100.0% (193/193) | 0.0% (0/193) |
| 13 | 359 | 0.0% (0/359) | 100.0% (359/359) | 0.0% (0/359) | 711 | 0.0% (0/711) | 100.0% (711/711) | 0.0% (0/711) |
| 14 | 565 | 0.0% (0/565) | 100.0% (565/565) | 0.0% (0/565) | 1096 | 0.0% (0/1096) | 100.0% (1096/1096) | 0.0% (0/1096) |
| 15 | 160 | 0.0% (0/160) | 100.0% (160/160) | 0.0% (0/160) | 311 | 0.0% (0/311) | 100.0% (311/311) | 0.0% (0/311) |
| 16 | 258 | 0.0% (0/258) | 100.0% (258/258) | 0.0% (0/258) | 520 | 0.0% (0/520) | 100.0% (520/520) | 0.0% (0/520) |
| 17 | 267 | 0.0% (0/267) | 100.0% (267/267) | 0.0% (0/267) | 536 | 0.0% (0/536) | 100.0% (536/536) | 0.0% (0/536) |
| 18 | 170 | 0.0% (0/170) | 100.0% (170/170) | 0.0% (0/170) | 343 | 0.0% (0/343) | 100.0% (343/343) | 0.0% (0/343) |
| 19 | 475 | 0.0% (0/475) | 100.0% (475/475) | 0.0% (0/475) | 936 | 0.0% (0/936) | 100.0% (936/936) | 0.0% (0/936) |
| 20 | 154 | 0.0% (0/154) | 100.0% (154/154) | 0.0% (0/154) | 273 | 0.0% (0/273) | 100.0% (273/273) | 0.0% (0/273) |
| 21 | 276 | 0.0% (0/276) | 100.0% (276/276) | 0.0% (0/276) | 541 | 0.0% (0/541) | 100.0% (541/541) | 0.0% (0/541) |
| 22 | 465 | 0.0% (0/465) | 100.0% (465/465) | 0.0% (0/465) | 912 | 0.0% (0/912) | 100.0% (912/912) | 0.0% (0/912) |
| 23 | 314 | 0.0% (0/314) | 100.0% (314/314) | 0.0% (0/314) | 624 | 0.0% (0/624) | 100.0% (624/624) | 0.0% (0/624) |
| 24 | 354 | 0.0% (0/354) | 100.0% (354/354) | 0.0% (0/354) | 750 | 0.0% (0/750) | 100.0% (750/750) | 0.0% (0/750) |
| 25 | 235 | 0.0% (0/235) | 100.0% (235/235) | 0.0% (0/235) | 463 | 0.0% (0/463) | 100.0% (463/463) | 0.0% (0/463) |
| 26 | 334 | 0.0% (0/334) | 100.0% (334/334) | 0.0% (0/334) | 667 | 0.0% (0/667) | 100.0% (667/667) | 0.0% (0/667) |
| 27 | 266 | 0.0% (0/266) | 100.0% (266/266) | 0.0% (0/266) | 517 | 0.0% (0/517) | 100.0% (517/517) | 0.0% (0/517) |
| 28 | 558 | 0.0% (0/558) | 100.0% (558/558) | 0.0% (0/558) | 1110 | 0.0% (0/1110) | 100.0% (1110/1110) | 0.0% (0/1110) |
| 29 | 493 | 0.0% (0/493) | 100.0% (493/493) | 0.0% (0/493) | 981 | 0.0% (0/981) | 100.0% (981/981) | 0.0% (0/981) |
| 30 | 719 | 0.0% (0/719) | 100.0% (719/719) | 0.0% (0/719) | 1418 | 0.0% (0/1418) | 100.0% (1418/1418) | 0.0% (0/1418) |
| 31 | 229 | 0.0% (0/229) | 100.0% (229/229) | 0.0% (0/229) | 440 | 0.0% (0/440) | 100.0% (440/440) | 0.0% (0/440) |
| 32 | 270 | 0.0% (0/270) | 100.0% (270/270) | 0.0% (0/270) | 580 | 0.0% (0/580) | 100.0% (580/580) | 0.0% (0/580) |
| 33 | 378 | 0.0% (0/378) | 100.0% (378/378) | 0.0% (0/378) | 754 | 0.0% (0/754) | 100.0% (754/754) | 0.0% (0/754) |
| 34 | 352 | 0.0% (0/352) | 100.0% (352/352) | 0.0% (0/352) | 654 | 0.0% (0/654) | 100.0% (654/654) | 0.0% (0/654) |
| 35 | 180 | 0.0% (0/180) | 100.0% (180/180) | 0.0% (0/180) | 373 | 0.0% (0/373) | 100.0% (373/373) | 0.0% (0/373) |
| 36 | 534 | 0.0% (0/534) | 100.0% (534/534) | 0.0% (0/534) | 1060 | 0.0% (0/1060) | 100.0% (1060/1060) | 0.0% (0/1060) |
| 37 | 811 | 0.0% (0/811) | 100.0% (811/811) | 0.0% (0/811) | 1576 | 0.0% (0/1576) | 100.0% (1576/1576) | 0.0% (0/1576) |
| 38 | 407 | 0.0% (0/407) | 100.0% (407/407) | 0.0% (0/407) | 791 | 0.0% (0/791) | 100.0% (791/791) | 0.0% (0/791) |
| 39 | 207 | 0.0% (0/207) | 100.0% (207/207) | 0.0% (0/207) | 411 | 0.0% (0/411) | 100.0% (411/411) | 0.0% (0/411) |
| 40 | 531 | 0.0% (0/531) | 100.0% (531/531) | 0.0% (0/531) | 1069 | 0.0% (0/1069) | 100.0% (1069/1069) | 0.0% (0/1069) |
| 41 | 538 | 0.0% (0/538) | 100.0% (538/538) | 0.0% (0/538) | 1066 | 0.0% (0/1066) | 100.0% (1066/1066) | 0.0% (0/1066) |
| 42 | 460 | 0.0% (0/460) | 100.0% (460/460) | 0.0% (0/460) | 908 | 0.0% (0/908) | 100.0% (908/908) | 0.0% (0/908) |
| 43 | 514 | 0.0% (0/514) | 100.0% (514/514) | 0.0% (0/514) | 971 | 0.0% (0/971) | 100.0% (971/971) | 0.0% (0/971) |
| 44 | 610 | 0.0% (0/610) | 100.0% (610/610) | 0.0% (0/610) | 1177 | 0.0% (0/1177) | 100.0% (1177/1177) | 0.0% (0/1177) |
| 45 | 530 | 0.0% (0/530) | 100.0% (530/530) | 0.0% (0/530) | 1046 | 0.0% (0/1046) | 100.0% (1046/1046) | 0.0% (0/1046) |
| 46 | 239 | 0.0% (0/239) | 100.0% (239/239) | 0.0% (0/239) | 441 | 0.0% (0/441) | 100.0% (441/441) | 0.0% (0/441) |
| 47 | 353 | 0.0% (0/353) | 100.0% (353/353) | 0.0% (0/353) | 647 | 0.0% (0/647) | 100.0% (647/647) | 0.0% (0/647) |
| 48 | 433 | 0.0% (0/433) | 100.0% (433/433) | 0.0% (0/433) | 818 | 0.0% (0/818) | 100.0% (818/818) | 0.0% (0/818) |
| 49 | 576 | 0.0% (0/576) | 100.0% (576/576) | 0.0% (0/576) | 1106 | 0.0% (0/1106) | 100.0% (1106/1106) | 0.0% (0/1106) |
| 50 | 267 | 0.0% (0/267) | 100.0% (267/267) | 0.0% (0/267) | 513 | 0.0% (0/513) | 100.0% (513/513) | 0.0% (0/513) |
| 51 | 530 | 0.0% (0/530) | 100.0% (530/530) | 0.0% (0/530) | 1053 | 0.0% (0/1053) | 100.0% (1053/1053) | 0.0% (0/1053) |
| 52 | 290 | 0.0% (0/290) | 100.0% (290/290) | 0.0% (0/290) | 553 | 0.0% (0/553) | 100.0% (553/553) | 0.0% (0/553) |
| 53 | 274 | 0.0% (0/274) | 100.0% (274/274) | 0.0% (0/274) | 528 | 0.0% (0/528) | 100.0% (528/528) | 0.0% (0/528) |
| 54 | 338 | 0.0% (0/338) | 100.0% (338/338) | 0.0% (0/338) | 651 | 0.0% (0/651) | 100.0% (651/651) | 0.0% (0/651) |
| 55 | 301 | 0.0% (0/301) | 100.0% (301/301) | 0.0% (0/301) | 577 | 0.0% (0/577) | 100.0% (577/577) | 0.0% (0/577) |
| 56 | 291 | 0.0% (0/291) | 100.0% (291/291) | 0.0% (0/291) | 558 | 0.0% (0/558) | 100.0% (558/558) | 0.0% (0/558) |
| 57 | 392 | 0.0% (0/392) | 100.0% (392/392) | 0.0% (0/392) | 776 | 0.0% (0/776) | 100.0% (776/776) | 0.0% (0/776) |
| 58 | 351 | 0.0% (0/351) | 100.0% (351/351) | 0.0% (0/351) | 708 | 0.0% (0/708) | 100.0% (708/708) | 0.0% (0/708) |
| 59 | 459 | 0.0% (0/459) | 100.0% (459/459) | 0.0% (0/459) | 881 | 0.0% (0/881) | 100.0% (881/881) | 0.0% (0/881) |
| 60 | 464 | 0.0% (0/464) | 100.0% (464/464) | 0.0% (0/464) | 888 | 0.0% (0/888) | 100.0% (888/888) | 0.0% (0/888) |
| 61 | 251 | 0.0% (0/251) | 100.0% (251/251) | 0.0% (0/251) | 498 | 0.0% (0/498) | 100.0% (498/498) | 0.0% (0/498) |
| 62 | 264 | 0.0% (0/264) | 100.0% (264/264) | 0.0% (0/264) | 500 | 0.0% (0/500) | 100.0% (500/500) | 0.0% (0/500) |
| 63 | 417 | 0.0% (0/417) | 100.0% (417/417) | 0.0% (0/417) | 755 | 0.0% (0/755) | 100.0% (755/755) | 0.0% (0/755) |
| 64 | 202 | 0.0% (0/202) | 100.0% (202/202) | 0.0% (0/202) | 436 | 0.0% (0/436) | 91.1% (397/436) | 8.9% (39/436) |
| 65 | 542 | 0.0% (0/542) | 100.0% (542/542) | 0.0% (0/542) | 1083 | 0.0% (0/1083) | 100.0% (1083/1083) | 0.0% (0/1083) |
| 66 | 591 | 0.0% (0/591) | 100.0% (591/591) | 0.0% (0/591) | 1172 | 0.0% (0/1172) | 100.0% (1172/1172) | 0.0% (0/1172) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 17; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (17/17).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/17).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (17/17).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **Ézs 9:20 és 64:1** (`naplok/F22_Ezs_atnezes.tsv`): a kézi 2:1 beolvasztás része (a TAHOT 9:20, illetve 64:2 tokenjei) `fuggoben`, link nélkül. A vers többi része párosítva van.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–Zsolt menetekben); az eltolódást a detektor és a kézi javítás kezeli.
- A régi arany 17 hármasa mind egyezik; kis minta, pontosságot nem minősít.

## 4. Eljárási megjegyzés: az ág

A futás commitjai (`d288e08` … `4d2f292`) a #77 ágán (`claude/wonderful-einstein-ezr2pw`) vannak, az F77.1–F77.10 commitokkal együtt, nem egy saját `claude/f22-ezs` ágon (mint az `f22-1moz` … `f22-zsolt`). Ez a „session = egy feladat” szabálytól eltér. A merge előtt eldöntendő (a felhasználóé): a #77 és az Ézs egy PR-ban megy-e be, vagy az F22.Ézs commitok külön ágra kerülnek (cherry-pick az F77.10 után).

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT-F22e, a felhasználó döntése, 2026.10.08).
- Független ellenőr: `naplok/ELLENOR_F22_Ezs.md`.
- A Jeremiás (DT57) indítása a felhasználó döntése (⛔ 2.); lefutott, l. `naplok/F22_Jer_jelentes.md`.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Ezs.md`)

Az ellenőr 8 eltérést talált. Mindegyik dokumentációs, eljárási vagy formai; adathibát nem talált. A számokat Grep-számlálással és `lekerdez.py`-jal igazolta, az `--ellenoriz`-t nem futtathatta (a 8 könyvre ez a menetben lefutott, l. 1a).

| # | eltérés | kezelés |
|---|---|---|
| 1 | K9: az Ézs nincs az `adat/datasetek.tsv`-ben és a SEMA 2.20-ban | javítva: datasetek (8 sor), SEMA 2.20 (jóváhagyott lista, kézi megfeleltetés, 2:1 beolvasztás, csak-Sonnet könyvek) |
| 2 | az ág (F77 + F22.Ézs egy ágon) | a felhasználó döntése (2026.10.08): a #77 és az Ézs egy ágon marad (`claude/wonderful-einstein-ezr2pw` = `claude/loving-cerf-dvm71f`), külön commitokban; egy commit a main-en „Squash and merge”-dzsel lesz (az egy commitba vont változat kényszerített pusht kívánt volna) |
| 3 | a DT-F77 (a) könyvméretű plafonja nem valósult meg (110 USD maradt) | lezárva az F77.11-ben (`e50a0bc`): könyvenkénti plafon (vers × 0,0074 × 1,5) |
| 4 | proveniencia-sor: „a API (Batch)-futásnak” | javítva az `egyesit.py`-ban; az Ézs táblái újraépítve, csak az 1. sor változott; a régi könyvek bájtra azonosak |
| 5 | K3 leírása a jelentésben | javítva (1. pont) |
| 6 | a briefből hiányzik a v2.10 sor | javítva |
| 7 | a brief `ir` mezőjéből hiányzik az `f22/api_termeles/*` | javítva |
| 8 | a futásnapló `futas` mezője éles futáson is `vakproba/high/Ezs` | lezárva az F77.11-ben (`e50a0bc`): a címke a `--gyoker` szerint; az Ézs 145 sorának `futas` mezője átcímkézve (csak ez a mező, l. ELLENOR_F22_Jer) |

A dupla „## 2.” címsor javítva (1a). Az üres `f22/api_termeles/javitando.txt` az eszköz állapotfájlja, marad.
