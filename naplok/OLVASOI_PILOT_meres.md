<!-- GENERÁLT: eszkozok/olvaso_pilot/meres.py — kézzel nem szerkesztendő. -->
# Olvasói pilot — mérés (F60.2)

*Gép által generált (`eszkozok/olvaso_pilot/meres.py`), kézzel nem szerkesztendő; a #60 M2 lépése. Mért adatállapot: repó-commit `83f725d` (az `ág: claude/olvasoi-pilot` feje a mérés előtt), a szakasz-adatok `ts` ideje: 1Móz 1:1–2:3 2026-10-07T10:51Z, Zsolt 22 2026-10-07T10:51Z.*

A pilot az aktuális adatállapotot méri (a #7, #9, #22, #38, #54, #56, #57 lezárása után újrafuttatható). A számok a pilot-oldalra kerülő adatot jellemzik, nem a repó egészét.

## 1. A Károli-szavak kötése héber szóhoz

- `scope=1Móz 1:1–2:3 | forras=adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása) | ts=2026-10-07T10:52Z`
- `scope=Zsolt 22 | forras=adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása) | ts=2026-10-07T10:52Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| Károli-szó (írásjelekkel együtt, szótoken) | 662 | 407 |
| kötött tartalmas héber szóhoz (kattintható, szó-lappal) | 399 (60.3%) | 243 (59.7%) |
| — ebből „magas” bizonyosság | 396 (99.2% a kötöttekből) | 0 (0.0% a kötöttekből) |
| — ebből nem „magas” (alacsony) | 3 (0.8% a kötöttekből) | 243 (100.0% a kötöttekből) |
| csak nyelvtani elemhez kötött (nincs szó-lap) | 161 (24.3%) | 92 (22.6%) |
| párosítás nélkül | 102 (15.4%) | 72 (17.7%) |

## 2. Héber szó-lapok: BDB-szócikk

- `scope=1Móz 1:1–2:3 | forras=adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol) | ts=2026-10-07T10:52Z`
- `scope=Zsolt 22 | forras=adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol) | ts=2026-10-07T10:52Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| héber szó-lap (nem nyelvtani Strong-szám) | 98 | 159 |
| van magyar BDB-szócikk | 61 (62.2%) | 111 (69.8%) |
| csak angol BDB-szócikk | 37 (37.8%) | 46 (28.9%) |
| egyik sincs (csak a Strong-szótár rövid jelentése) | 0 (0.0%) | 2 (1.3%) |

- Zsolt 22: BDB-szócikk nélküli szó-lapok: H0136, H7358

## 3. BDB-bontás (gépi szeletelés)

- `scope=1Móz 1:1–2:3 | forras=adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja | ts=2026-10-07T10:52Z`
- `scope=Zsolt 22 | forras=adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja | ts=2026-10-07T10:52Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| legalább 2 jelentésre bomlik | 68 (69.4%) | 123 (77.4%) |
| egyben marad (1 számozott jelentés) | 5 (5.1%) | 2 (1.3%) |
| nincs számozott jelentés a szeletelésben (0) | 25 (25.5%) | 34 (21.4%) |

- 1Móz 1:1–2:3, egyben maradó szócikkek (5): H2009 הִנֵּה, H3533 כָּבַשׁ, H6153 עֶ֫רֶב, H7287 רָדָה, H8415 תְּהוֹם
- 1Móz 1:1–2:3, számozott jelentés nélkül (25): H0226 אוֹת, H0402 אׇכְלָה, H0922 בֹּהוּ, H1419 גַּל, H1710 דָּגָה, H1876 דָּשָׁא, H1877 דֶּ֫שֶׁא, H2145 זָכָר, H3004 יַבָּשָׁה, H3220 יָם, H3418 יֶ֫רֶק, H3556 כּוֹכָב, H3974 מָאוֹר, H4327 מִין, H4723 מִקְוֶה, H6086 עֵץ, H6212 עֵ֫שֶׂב, H7363 רָחַף, H7549 רָקִיעַ, H7992 שְׁלִישִׁי, H8141 שָׁנָה, H8145 שֵׁנִי, H8318 שֶׁ֫רֶץ, H8345 שִׁשִּׁי, H8432 תָּ֫וֶךְ
- 1Móz 1:1–2:3, bomló szócikkek (68), jelentésszám szerint csökkenően: H6942 קָדַשׁ (17), H6213 עָשָׂה (12), H0216 אוֹר (11), H2896 טוֹב (10), H5315 נֶ֫פֶשׁ (10), H1254 בָּרָא (9), H7307 רוּחַ (9), H6440 פָּנֶה (8), H0127 אֲדָמָה (7), H4725 מָקוֹם (7), H7200 רָאָה (7), H7673 שָׁבַת (7), H4390 מָלֵא (6), H4399 מְלָאכָה (6), H5414 נָתַן (6), H7121 קָרָא (6), H0215 אוֹר (5), H0776 אֶ֫רֶץ (5), H1288 בָּרַךְ (5), H1961 הָיָה (5), H2233 זֶ֫רַע (5), H3318 יָצָא (5), H4150 מוֹעֵד (5), H6509 פָּרָה (5), H0120 אָדָם (4) …
- Zsolt 22, egyben maradó szócikkek (2): H1518 גִּיחַ, H3119 יוֹמָם
- Zsolt 22, számozott jelentés nélkül (34): H0136 אֲדֹנָי, H0251 אָח, H0355 אַיָּלָה, H0360 אֱיָלוּת, H0376 אִישׁ, H0408 אַל, H0595 אָֽנֹכִ֫י, H0657 אֶ֫פֶס, H0738 אַרְיֵה, H0859 אַתָּ֫ה, H1316 בָּשָׁן, H1556 גָּלַל, H1732 דָּוִד, H1747 דּוּמִיָּה, H1749 דּוֹנַג, H1879 דָּשֵׁן, H2963 טָרַף, H3373 יָרֵא, H3611 כֶּ֫לֶב, H3803 כָּתַר, H3830 לְבוּשׁ, H3932 לָעַג, H4210 מִזְמוֹר, H4410 מְלוּכָה, H4455 מַלְקוֹחַ, H5826 עָזַר, H6039 עֱנוּת, H6869 צָרָה, H7214 רְאֵם, H7227 רַב, H7358 רֶ֫חֶם, H7768 שָׁוַע, H7837 שַׁ֫חַר, H8432 תָּ֫וֶךְ
- Zsolt 22, bomló szócikkek (123), jelentésszám szerint csökkenően: H7725 שׁוּב (20), H2142 זָכַר (15), H0398 אָכַל (12), H3513 כָּבֵד (12), H6213 עָשָׂה (12), H5437 סָבַב (11), H2505 חָלַק (10), H3820 לֵב (10), H3824 לֵבָב (10), H5315 נֶ֫פֶשׁ (10), H0001 אָב (9), H1697 דָּבָר (8), H3427 יָשַׁב (8), H4422 מָלַט (8), H6440 פָּנֶה (8), H8085 שָׁמַע (8), H0410 אֵל (7), H5307 נָפַל (7), H6666 צְדָקָה (7), H7200 רָאָה (7), H0369 אַ֫יִן (6), H0935 בּוֹא (6), H1984 הָלַל (6), H2199 זָעַק (6), H3956 לָשׁוֹן (6) …

## 4. Görög szó-lapok

- `scope=1Móz 1:1–2:3 | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire | ts=2026-10-07T10:52Z`
- `scope=Zsolt 22 | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire | ts=2026-10-07T10:52Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| görög szó-lap | 110 | 153 |
| van magyar jelentés (adat/forditasok.tsv: Thayer / UBS_DNTG) | 3 (2.7%) | 1 (0.7%) |
| van újszövetségi előfordulás (TAGNT) | 102 (92.7%) | 144 (94.1%) |
| van héber háttér (lxx_bridge) | 95 (86.4%) | 135 (88.2%) |
| van TBESG szótári szöveg (angol) | 110 (100.0%) | 153 (100.0%) |

## 5. A görög szóalak forrása

- `scope=1Móz 1:1–2:3 | forras=konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás) | ts=2026-10-07T10:52Z`
- `scope=Zsolt 22 | forras=konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás) | ts=2026-10-07T10:52Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| héber szó (TAHOT-sor, a nyelvtani elemekkel együtt) | 748 | 389 |
| nincs Macula-párja (a görög megfelelő nem is képezhető) | 2 (0.3%) | 1 (0.3%) |
| Macula-párral rendelkező szó | 746 | 388 |
| — van görög megfelelője | 642 (86.1%) | 324 (83.5%) |
| — a szóalak az LXX_OS-ből (egyezés Strong-szám + alak szerint) | 569 (88.6% a görögből) | 218 (67.3% a görögből) |
| — a szóalak a Maculából marad (nincs LXX_OS-egyezés) | 36 (5.6% a görögből) | 64 (19.8% a görögből) |
| — ebből χ vagy ξ van a Macula-alakban (a Macula-oszlop χ/ξ-hibás) | 1 | 2 |
| — nincs görög megfelelő (a Macula `gorog_lxx` üres) | 104 | 64 |
| Macula-alak ≠ LXX_OS-alak (ékezet és hehezet nélkül) | 33 | 14 |
| — ebből a χ/ξ felcserélése magyarázza | 30 | 11 |

## 6. UBS-jelentés lefedettsége, versszámozás

- `scope=1Móz 1:1–2:3 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám) | ts=2026-10-07T10:52Z`
- `scope=Zsolt 22 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám) | ts=2026-10-07T10:52Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| nem nyelvtani héber szó-előfordulás | 401 | 218 |
| — van UBS-jelentés-besorolás (előfordulásonként) | 345 (86.0%) | 200 (91.7%) |
| különböző héber szó-lap | 98 | 159 |
| — legalább egy előfordulásához van UBS-jelentés | 91 (92.9%) | 153 (96.2%) |
| vers a szakaszban | 34 | 32 |
| — a versmegfeleltető tábla szerint nincs KJV-megfelelő | 0 | 1 |
| — nincs LXX-szó a versre (LXX_OS) | 0 | 1 |
| — a tábla KJV- vagy MT-száma eltér a Károli-számtól | 0 | 0 |
| — a versmegfeleltető tábla és az LXX_OS saját KJV-oszlopa ellentmond | 0 | 31 |

- Zsolt 22, nincs KJV-megfelelő: Zsolt 22:32
- Zsolt 22, nincs LXX-szó: Zsolt 22:1
- Zsolt 22, a két tábla KJV-száma ellentmond: Zsolt 22:2, Zsolt 22:3, Zsolt 22:4, Zsolt 22:5, Zsolt 22:6, Zsolt 22:7, Zsolt 22:8, Zsolt 22:9, Zsolt 22:10, Zsolt 22:11, Zsolt 22:12, Zsolt 22:13, Zsolt 22:14, Zsolt 22:15, Zsolt 22:16, Zsolt 22:17, Zsolt 22:18, Zsolt 22:19, Zsolt 22:20, Zsolt 22:21, Zsolt 22:22, Zsolt 22:23, Zsolt 22:24, Zsolt 22:25, Zsolt 22:26, Zsolt 22:27, Zsolt 22:28, Zsolt 22:29, Zsolt 22:30, Zsolt 22:31, Zsolt 22:32

