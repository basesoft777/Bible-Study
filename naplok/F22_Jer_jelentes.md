# F22_Jer_jelentes.md — Károli–Strong párosítás: Jeremiás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Jer`, `egyesit.py --ellenoriz --konyv <könyv>`, `f22_elemzes.py --konyv Jer`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Jer-sorainak összesítése). Ág: `claude/wonderful-einstein-ezr2pw` (= `claude/loving-cerf-dvm71f`). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT-F77 (a), a második éles könyv), **a C (Gemini) kimarad** (DT-F22c). Sorrend: DT57 (Ézs, utána Jer).*

## 1. Menet

- **Előkészítés (F77.11, `e50a0bc`):** az Ézs-ellenőr két nyitott pontja (ELLENOR_F22_Ezs 3., 8.) a futás előtt javítva: könyvenkénti költségplafon (`api_koteg.konyv_plafon`: vers × 0,0074 USD × 1,5, legalább 1 USD; a Jeremiásra 1 364 × 0,0074 × 1,5 = 15,14 USD), és a futásnapló `futas` címkéje a `--gyoker` szerint (`api_termeles/high/<könyv>`; az Ézs 145 sora átcímkézve). A globális `PLAFON_USD` 110 USD maradt.
- **Versbeosztás-jóváhagyás (2026.10.08, chat: „mehet”)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Jer tiszta (1 364/1 364 vers, 52 fejezet, K-hiány 0, E-hiány 0, eltolt 0), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.
- **Minta:** `f22/minta_Jer.tsv`, 1 364 vers (= a `Karoli_1908.tsv` `Jer ` sorai), 137 köteg (10 vers/köteg, az utolsó 4).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_013DuXHMN7jhrqnFje7XTLGR`, 137 kérés (2026-10-08T10:42Z); javító kör `msgbatch_013D2oWwj7pt7ZzxkhGAzEQ9`, 16 kérés (11:06Z).
- **Futásnapló** (Jer: 153 sor, `futas=api_termeles/high/Jer`): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `prompt_sha256_12` minden soron `84f12ca7aafb` (mint az Ézsnél és a korábbi futásnaplóban). A hash-ellenőrzést az `api_koteg.prompt_szoveg` végzi minden prompt előtt (`sonnet_koteg.prompt_hash_hiba`, K3); az `f21p/` diffje üres.

| kör | kérés | kapun átment | kapun bukott (vers) | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 137 | 121 | 16 köteg (41 vers) | 8,5645 | 1 581 645 / 1 396 578 |
| 2. próba (javító) | 16 | 16 | 0 | 0,4906 | 231 117 / 51 903 |
| **összesen** | 153 | | | **9,0552** | |

A javító körbe került kötegek: 9, 14, 32, 60, 64, 68, 72, 76, 90, 92, 100, 101, 109, 111, 124, 127. A költség `batch_ar_szamolt`; versenként 0,0066 USD (a plafon alapja 0,0074). A könyvplafonból (15,14 USD) 9,06 fogyott; a futásnapló futó összege 16,1386 USD (Ézs 7,0834 + Jer 9,0552), a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 137 köteg, 1364 vers; kapuhiba első próbára 3.0% (41/1364); végleg 0.0% (0/1364)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Jer`: `parok_Jer.tsv` 32 797 link (mind `alacsony`, `S`; a fájl 32 799 sora a proveniencia- és a fejlécsorral), `szavak_Jer.tsv` 64 563 token (64 565 sor). A szavak bontása: hu 32 034 (26 388 `parositva`, 5 646 `betoldas`), er 32 529 (30 046 `parositva`, 2 483 `forditatlan`); `fuggoben` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Jer ` sorainak száma (32 529). Az átnézési sor (`naplok/F22_Jer_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz` (2026.10.08, ezen az ágon): 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer — mind „rendben”. A Jer-menet (`36135a3..5b0457a`) az `adat/` alatt csak a két Jer-táblát érinti; `konkordancia/` és `f21p/` változatlan. A proveniencia-sor: `scope=manual | forras=f22/valaszok/sonnet/Jer.jsonl, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv | ts=manual (… az API (Batch)-futásnak nincs lekérdezés-időbélyege) | …`.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Jer` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/32797), alacsony 100.0% (32797/32797), kezi 0.0% (0/32797); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/64563), alacsony 100.0% (64563/64563), kezi 0.0% (0/64563).

Link-forrás megoszlás (parok): S 32797. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 1364 (Jer 10:1, Jer 10:10, Jer 10:11, Jer 10:12, Jer 10:13, Jer 10:14, Jer 10:15, Jer 10:16, Jer 10:17, Jer 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 424 | 0.0% (0/424) | 100.0% (424/424) | 0.0% (0/424) | 779 | 0.0% (0/779) | 100.0% (779/779) | 0.0% (0/779) |
| 2 | 811 | 0.0% (0/811) | 100.0% (811/811) | 0.0% (0/811) | 1566 | 0.0% (0/1566) | 100.0% (1566/1566) | 0.0% (0/1566) |
| 3 | 626 | 0.0% (0/626) | 100.0% (626/626) | 0.0% (0/626) | 1212 | 0.0% (0/1212) | 100.0% (1212/1212) | 0.0% (0/1212) |
| 4 | 618 | 0.0% (0/618) | 100.0% (618/618) | 0.0% (0/618) | 1221 | 0.0% (0/1221) | 100.0% (1221/1221) | 0.0% (0/1221) |
| 5 | 667 | 0.0% (0/667) | 100.0% (667/667) | 0.0% (0/667) | 1301 | 0.0% (0/1301) | 100.0% (1301/1301) | 0.0% (0/1301) |
| 6 | 611 | 0.0% (0/611) | 100.0% (611/611) | 0.0% (0/611) | 1173 | 0.0% (0/1173) | 100.0% (1173/1173) | 0.0% (0/1173) |
| 7 | 828 | 0.0% (0/828) | 100.0% (828/828) | 0.0% (0/828) | 1596 | 0.0% (0/1596) | 100.0% (1596/1596) | 0.0% (0/1596) |
| 8 | 503 | 0.0% (0/503) | 100.0% (503/503) | 0.0% (0/503) | 999 | 0.0% (0/999) | 100.0% (999/999) | 0.0% (0/999) |
| 9 | 583 | 0.0% (0/583) | 100.0% (583/583) | 0.0% (0/583) | 1145 | 0.0% (0/1145) | 100.0% (1145/1145) | 0.0% (0/1145) |
| 10 | 496 | 0.0% (0/496) | 100.0% (496/496) | 0.0% (0/496) | 957 | 0.0% (0/957) | 100.0% (957/957) | 0.0% (0/957) |
| 11 | 603 | 0.0% (0/603) | 100.0% (603/603) | 0.0% (0/603) | 1143 | 0.0% (0/1143) | 100.0% (1143/1143) | 0.0% (0/1143) |
| 12 | 403 | 0.0% (0/403) | 100.0% (403/403) | 0.0% (0/403) | 778 | 0.0% (0/778) | 100.0% (778/778) | 0.0% (0/778) |
| 13 | 601 | 0.0% (0/601) | 100.0% (601/601) | 0.0% (0/601) | 1188 | 0.0% (0/1188) | 100.0% (1188/1188) | 0.0% (0/1188) |
| 14 | 537 | 0.0% (0/537) | 100.0% (537/537) | 0.0% (0/537) | 1049 | 0.0% (0/1049) | 100.0% (1049/1049) | 0.0% (0/1049) |
| 15 | 517 | 0.0% (0/517) | 100.0% (517/517) | 0.0% (0/517) | 978 | 0.0% (0/978) | 100.0% (978/978) | 0.0% (0/978) |
| 16 | 601 | 0.0% (0/601) | 100.0% (601/601) | 0.0% (0/601) | 1122 | 0.0% (0/1122) | 100.0% (1122/1122) | 0.0% (0/1122) |
| 17 | 630 | 0.0% (0/630) | 100.0% (630/630) | 0.0% (0/630) | 1231 | 0.0% (0/1231) | 100.0% (1231/1231) | 0.0% (0/1231) |
| 18 | 521 | 0.0% (0/521) | 100.0% (521/521) | 0.0% (0/521) | 975 | 0.0% (0/975) | 100.0% (975/975) | 0.0% (0/975) |
| 19 | 440 | 0.0% (0/440) | 100.0% (440/440) | 0.0% (0/440) | 840 | 0.0% (0/840) | 100.0% (840/840) | 0.0% (0/840) |
| 20 | 448 | 0.0% (0/448) | 100.0% (448/448) | 0.0% (0/448) | 891 | 0.0% (0/891) | 100.0% (891/891) | 0.0% (0/891) |
| 21 | 388 | 0.0% (0/388) | 100.0% (388/388) | 0.0% (0/388) | 767 | 0.0% (0/767) | 100.0% (767/767) | 0.0% (0/767) |
| 22 | 716 | 0.0% (0/716) | 100.0% (716/716) | 0.0% (0/716) | 1365 | 0.0% (0/1365) | 100.0% (1365/1365) | 0.0% (0/1365) |
| 23 | 933 | 0.0% (0/933) | 100.0% (933/933) | 0.0% (0/933) | 1877 | 0.0% (0/1877) | 100.0% (1877/1877) | 0.0% (0/1877) |
| 24 | 270 | 0.0% (0/270) | 100.0% (270/270) | 0.0% (0/270) | 549 | 0.0% (0/549) | 100.0% (549/549) | 0.0% (0/549) |
| 25 | 869 | 0.0% (0/869) | 100.0% (869/869) | 0.0% (0/869) | 1776 | 0.0% (0/1776) | 100.0% (1776/1776) | 0.0% (0/1776) |
| 26 | 640 | 0.0% (0/640) | 100.0% (640/640) | 0.0% (0/640) | 1279 | 0.0% (0/1279) | 100.0% (1279/1279) | 0.0% (0/1279) |
| 27 | 611 | 0.0% (0/611) | 100.0% (611/611) | 0.0% (0/611) | 1216 | 0.0% (0/1216) | 100.0% (1216/1216) | 0.0% (0/1216) |
| 28 | 390 | 0.0% (0/390) | 100.0% (390/390) | 0.0% (0/390) | 816 | 0.0% (0/816) | 100.0% (816/816) | 0.0% (0/816) |
| 29 | 785 | 0.0% (0/785) | 100.0% (785/785) | 0.0% (0/785) | 1564 | 0.0% (0/1564) | 100.0% (1564/1564) | 0.0% (0/1564) |
| 30 | 550 | 0.0% (0/550) | 100.0% (550/550) | 0.0% (0/550) | 1048 | 0.0% (0/1048) | 100.0% (1048/1048) | 0.0% (0/1048) |
| 31 | 943 | 0.0% (0/943) | 100.0% (943/943) | 0.0% (0/943) | 1861 | 0.0% (0/1861) | 100.0% (1861/1861) | 0.0% (0/1861) |
| 32 | 1154 | 0.0% (0/1154) | 100.0% (1154/1154) | 0.0% (0/1154) | 2296 | 0.0% (0/2296) | 100.0% (2296/2296) | 0.0% (0/2296) |
| 33 | 620 | 0.0% (0/620) | 100.0% (620/620) | 0.0% (0/620) | 1263 | 0.0% (0/1263) | 100.0% (1263/1263) | 0.0% (0/1263) |
| 34 | 660 | 0.0% (0/660) | 100.0% (660/660) | 0.0% (0/660) | 1293 | 0.0% (0/1293) | 100.0% (1293/1293) | 0.0% (0/1293) |
| 35 | 528 | 0.0% (0/528) | 100.0% (528/528) | 0.0% (0/528) | 1039 | 0.0% (0/1039) | 100.0% (1039/1039) | 0.0% (0/1039) |
| 36 | 861 | 0.0% (0/861) | 100.0% (861/861) | 0.0% (0/861) | 1792 | 0.0% (0/1792) | 100.0% (1792/1792) | 0.0% (0/1792) |
| 37 | 478 | 0.0% (0/478) | 100.0% (478/478) | 0.0% (0/478) | 975 | 0.0% (0/975) | 100.0% (975/975) | 0.0% (0/975) |
| 38 | 758 | 0.0% (0/758) | 100.0% (758/758) | 0.0% (0/758) | 1556 | 0.0% (0/1556) | 100.0% (1556/1556) | 0.0% (0/1556) |
| 39 | 427 | 0.0% (0/427) | 100.0% (427/427) | 0.0% (0/427) | 858 | 0.0% (0/858) | 100.0% (858/858) | 0.0% (0/858) |
| 40 | 557 | 0.0% (0/557) | 100.0% (557/557) | 0.0% (0/557) | 1081 | 0.0% (0/1081) | 100.0% (1081/1081) | 0.0% (0/1081) |
| 41 | 481 | 0.0% (0/481) | 100.0% (481/481) | 0.0% (0/481) | 1005 | 0.0% (0/1005) | 100.0% (1005/1005) | 0.0% (0/1005) |
| 42 | 641 | 0.0% (0/641) | 100.0% (641/641) | 0.0% (0/641) | 1177 | 0.0% (0/1177) | 100.0% (1177/1177) | 0.0% (0/1177) |
| 43 | 331 | 0.0% (0/331) | 100.0% (331/331) | 0.0% (0/331) | 670 | 0.0% (0/670) | 100.0% (670/670) | 0.0% (0/670) |
| 44 | 1030 | 0.0% (0/1030) | 100.0% (1030/1030) | 0.0% (0/1030) | 1949 | 0.0% (0/1949) | 100.0% (1949/1949) | 0.0% (0/1949) |
| 45 | 122 | 0.0% (0/122) | 100.0% (122/122) | 0.0% (0/122) | 234 | 0.0% (0/234) | 100.0% (234/234) | 0.0% (0/234) |
| 46 | 607 | 0.0% (0/607) | 100.0% (607/607) | 0.0% (0/607) | 1203 | 0.0% (0/1203) | 100.0% (1203/1203) | 0.0% (0/1203) |
| 47 | 152 | 0.0% (0/152) | 100.0% (152/152) | 0.0% (0/152) | 292 | 0.0% (0/292) | 100.0% (292/292) | 0.0% (0/292) |
| 48 | 837 | 0.0% (0/837) | 100.0% (837/837) | 0.0% (0/837) | 1644 | 0.0% (0/1644) | 100.0% (1644/1644) | 0.0% (0/1644) |
| 49 | 857 | 0.0% (0/857) | 100.0% (857/857) | 0.0% (0/857) | 1684 | 0.0% (0/1684) | 100.0% (1684/1684) | 0.0% (0/1684) |
| 50 | 1033 | 0.0% (0/1033) | 100.0% (1033/1033) | 0.0% (0/1033) | 2032 | 0.0% (0/2032) | 100.0% (2032/2032) | 0.0% (0/2032) |
| 51 | 1340 | 0.0% (0/1340) | 100.0% (1340/1340) | 0.0% (0/1340) | 2633 | 0.0% (0/2633) | 100.0% (2633/2633) | 0.0% (0/2633) |
| 52 | 760 | 0.0% (0/760) | 100.0% (760/760) | 0.0% (0/760) | 1625 | 0.0% (0/1625) | 100.0% (1625/1625) | 0.0% (0/1625) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 1; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (1/1).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/1).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (1/1).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: a Jeremiásban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–Ézs menetekben); a versbeosztás a detektor szerint tiszta.
- A régi arany egyetlen hármasa egyezik; mérésre alkalmatlanul kis minta.

## 4. Kiegészítések ebben a menetben

- K9: a Jer bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D17, v2.11.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT-F22e, a felhasználó döntése, 2026.10.08).
- Független ellenőr: `naplok/ELLENOR_F22_Jer.md`.
- A következő könyv indítása a felhasználó döntése (⛔ 2.). A DT57 (1) szerint a Jer után a BDB-haszon mérése szerinti sorrend jön (a DONTESEK.md DT57 sorának mérése: 1Krón 189, 2Krón 169, Ezsd 162, Jób 159, Ez 147, Péld 145 szócikk; a Bír később); a Jób előtt TAHOT-hiány (Jób 40:1–5, 41) és döntés az 1:2 / 2:1 támogatásról.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Jer.md`)

Az ellenőr 5 eltérést talált; adathibát nem. A számokat Grep-számlálással és `lekerdez.py`-jal igazolta, a szkripteket nem futtathatta (az `--ellenoriz` a 9 könyvre ebben a menetben lefutott, l. 1a).

| # | eltérés | kezelés |
|---|---|---|
| 1 | prófétai kötegméret: a brief 22.1.3 és a DT-F21g (3) szerint 5 vers, az Ézs és a Jer 10 verses kötegekkel futott | **nyitva, felhasználói döntés** (a 10 vers utólagos elfogadása, vagy 5 a következő prófétai könyvektől); kár nem látszik: minden sor `end_turn`, végleges kapuhiba 0 |
| 2 | az F77.11 a 145 Ézs-futásnapló-sor `futas` mezőjét átírta, döntés nélkül | **nyitva, felhasználói döntés** (utólagos elfogadás); az adat ép, csak ez a mező változott |
| 3 | elavult Ézs-jelentés (6. tábla 2., 3., 8. sor, 5. pont) | javítva |
| 4 | ág és F77-brief: az F77-brief fejléce nem rögzíti az F77.11-et | nyitva (a #77 saját fejléce, a merge előtt frissítendő); az Ézs-jelentés 6/2 állítása javítva |
| 5 | SEMA 2.20: a „nincs sora a listában” felsorolásból kimaradt a Zsolt és a Jer | javítva |
