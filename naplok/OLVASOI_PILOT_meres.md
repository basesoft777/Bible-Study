<!-- GENERÁLT: eszkozok/olvaso_pilot/meres.py — kézzel nem szerkesztendő. -->
# Olvasói pilot — mérés (F60.2, bővítve: F60.5)

*Gép által generált (`eszkozok/olvaso_pilot/meres.py`), kézzel nem szerkesztendő; a #60 M2 lépése. Mért adatállapot: repó-commit `7f18c4c` (az `ág: claude/olvasoi-pilot` feje a mérés előtt), a szakasz-adatok `ts` ideje: 1Móz 1:1–2:3 2026-10-07T14:29Z, Zsolt 22 2026-10-07T14:29Z.*

A pilot az aktuális adatállapotot méri (a #7, #9, #22, #38, #54, #56, #57 lezárása után újrafuttatható). A számok a pilot-oldalra kerülő adatot jellemzik, nem a repó egészét.

## 1. A Károli-szavak kötése héber szóhoz

- `scope=1Móz 1:1–2:3 | forras=adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása) | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása) | ts=2026-10-07T14:29Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| Károli-szó (írásjelekkel együtt, szótoken) | 662 | 407 |
| kötött tartalmas héber szóhoz (kattintható, szó-lappal) | 399 (60.3%) | 243 (59.7%) |
| — ebből „magas” bizonyosság | 396 (99.2% a kötöttekből) | 0 (0.0% a kötöttekből) |
| — ebből nem „magas” (alacsony) | 3 (0.8% a kötöttekből) | 243 (100.0% a kötöttekből) |
| csak nyelvtani elemhez kötött (nincs szó-lap) | 161 (24.3%) | 92 (22.6%) |
| párosítás nélkül | 102 (15.4%) | 72 (17.7%) |

## 2. Héber szó-lapok: BDB-szócikk

- `scope=1Móz 1:1–2:3 | forras=adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol) | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol) | ts=2026-10-07T14:29Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| héber szó-lap (nem nyelvtani Strong-szám) | 98 | 159 |
| van magyar BDB-szócikk | 61 (62.2%) | 112 (70.4%) |
| csak angol BDB-szócikk | 37 (37.8%) | 47 (29.6%) |
| egyik sincs (csak a Strong-szótár rövid jelentése) | 0 (0.0%) | 0 (0.0%) |

- Zsolt 22: a saját szócikk nélküli, de a BDB_strong_alias.tsv szerint másik Strong-szám alatt álló szó-lapok (az alias-szócikk a lapon jelezve; a fenti számokban a magyar/angol sorban szerepelnek): H0136, H7358

## 3. BDB-bontás (gépi szeletelés)

- `scope=1Móz 1:1–2:3 | forras=adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja | ts=2026-10-07T14:29Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| legalább 2 jelentésre bomlik | 68 (69.4%) | 125 (78.6%) |
| egyben marad (1 számozott jelentés) | 5 (5.1%) | 2 (1.3%) |
| nincs számozott jelentés a szeletelésben (0) | 25 (25.5%) | 32 (20.1%) |

- 1Móz 1:1–2:3, egyben maradó szócikkek (5): H2009 הִנֵּה, H3533 כָּבַשׁ, H6153 עֶ֫רֶב, H7287 רָדָה, H8415 תְּהוֹם
- 1Móz 1:1–2:3, számozott jelentés nélkül (25): H0226 אוֹת, H0402 אׇכְלָה, H0922 בֹּהוּ, H1419 גַּל, H1710 דָּגָה, H1876 דָּשָׁא, H1877 דֶּ֫שֶׁא, H2145 זָכָר, H3004 יַבָּשָׁה, H3220 יָם, H3418 יֶ֫רֶק, H3556 כּוֹכָב, H3974 מָאוֹר, H4327 מִין, H4723 מִקְוֶה, H6086 עֵץ, H6212 עֵ֫שֶׂב, H7363 רָחַף, H7549 רָקִיעַ, H7992 שְׁלִישִׁי, H8141 שָׁנָה, H8145 שֵׁנִי, H8318 שֶׁ֫רֶץ, H8345 שִׁשִּׁי, H8432 תָּ֫וֶךְ
- 1Móz 1:1–2:3, bomló szócikkek (68), jelentésszám szerint csökkenően: H6942 קָדַשׁ (17), H6213 עָשָׂה (12), H0216 אוֹר (11), H2896 טוֹב (10), H5315 נֶ֫פֶשׁ (10), H1254 בָּרָא (9), H7307 רוּחַ (9), H6440 פָּנֶה (8), H0127 אֲדָמָה (7), H4725 מָקוֹם (7), H7200 רָאָה (7), H7673 שָׁבַת (7), H4390 מָלֵא (6), H4399 מְלָאכָה (6), H5414 נָתַן (6), H7121 קָרָא (6), H0215 אוֹר (5), H0776 אֶ֫רֶץ (5), H1288 בָּרַךְ (5), H1961 הָיָה (5), H2233 זֶ֫רַע (5), H3318 יָצָא (5), H4150 מוֹעֵד (5), H6509 פָּרָה (5), H0120 אָדָם (4) …
- Zsolt 22, egyben maradó szócikkek (2): H1518 גִּיחַ, H3119 יוֹמָם
- Zsolt 22, számozott jelentés nélkül (32): H0251 אָח, H0355 אַיָּלָה, H0360 אֱיָלוּת, H0376 אִישׁ, H0408 אַל, H0595 אָֽנֹכִ֫י, H0657 אֶ֫פֶס, H0738 אַרְיֵה, H0859 אַתָּ֫ה, H1316 בָּשָׁן, H1556 גָּלַל, H1732 דָּוִד, H1747 דּוּמִיָּה, H1749 דּוֹנַג, H1879 דָּשֵׁן, H2963 טָרַף, H3373 יָרֵא, H3611 כֶּ֫לֶב, H3803 כָּתַר, H3830 לְבוּשׁ, H3932 לָעַג, H4210 מִזְמוֹר, H4410 מְלוּכָה, H4455 מַלְקוֹחַ, H5826 עָזַר, H6039 עֱנוּת, H6869 צָרָה, H7214 רְאֵם, H7227 רַב, H7768 שָׁוַע, H7837 שַׁ֫חַר, H8432 תָּ֫וֶךְ
- Zsolt 22, bomló szócikkek (125), jelentésszám szerint csökkenően: H7725 שׁוּב (20), H2142 זָכַר (15), H0398 אָכַל (12), H3513 כָּבֵד (12), H6213 עָשָׂה (12), H5437 סָבַב (11), H2505 חָלַק (10), H3820 לֵב (10), H3824 לֵבָב (10), H5315 נֶ֫פֶשׁ (10), H0001 אָב (9), H1697 דָּבָר (8), H3427 יָשַׁב (8), H4422 מָלַט (8), H6440 פָּנֶה (8), H8085 שָׁמַע (8), H0410 אֵל (7), H5307 נָפַל (7), H6666 צְדָקָה (7), H7200 רָאָה (7), H0136 אֲדֹנָי (6), H0369 אַ֫יִן (6), H0935 בּוֹא (6), H1984 הָלַל (6), H2199 זָעַק (6) …

## 4. Görög szó-lapok

- `scope=1Móz 1:1–2:3 | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire, és minden görög szó, amelyre egy héber szó-lap a lxx_bridge-ből hivatkozik | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire, és minden görög szó, amelyre egy héber szó-lap a lxx_bridge-ből hivatkozik | ts=2026-10-07T14:29Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| görög szó-lap | 202 | 304 |
| van magyar jelentés (adat/forditasok.tsv: Thayer / UBS_DNTG) | 4 (2.0%) | 3 (1.0%) |
| van újszövetségi előfordulás (TAGNT) | 191 (94.6%) | 286 (94.1%) |
| van héber háttér (lxx_bridge) | 187 (92.6%) | 286 (94.1%) |
| van TBESG szótári szöveg (angol) | 202 (100.0%) | 304 (100.0%) |

## 5. A görög szóalak forrása

- `scope=1Móz 1:1–2:3 | forras=konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás) | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás) | ts=2026-10-07T14:29Z`

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

- `scope=1Móz 1:1–2:3 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám) | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám) | ts=2026-10-07T14:29Z`

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

## 7. A bővítés (F60.5, v2): a meglévő adatok megjelenítésének mérése

A bővítés új adatot nem állít elő: minden érték egy meglévő tábla sora; a gépi feldolgozás (kulcs-illesztés, tartomány bontása, morf-kód feloldása) jelölt. A teljes adatkészlet-felmérés: `naplok/OLVASOI_PILOT_adatfelmeres.md`.

### 7.1 Szó-lapok (Strong-kulcs)

- `scope=1Móz 1:1–2:3 | forras=konkordancia/{SDBH_domenek,SDGNT_domenek,SECE_H_teljes,SECE_G_teljes,OSHL_lexikalis_index,LSJ_teljes,MCGED_teljes,UBS_DNTG_jelentesek,tW_szocikkek}.tsv + TBESH.txt; szó-lapok: adat.py → bovites.py | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=konkordancia/{SDBH_domenek,SDGNT_domenek,SECE_H_teljes,SECE_G_teljes,OSHL_lexikalis_index,LSJ_teljes,MCGED_teljes,UBS_DNTG_jelentesek,tW_szocikkek}.tsv + TBESH.txt; szó-lapok: adat.py → bovites.py | ts=2026-10-07T14:29Z`

| Mérőszám (a szakasz szó-lapjai közül) | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| héber: SDBH-domén | 91/98 (92.9%) | 154/159 (96.9%) |
| héber: SECE_H-szócikk | 98/98 (100.0%) | 159/159 (100.0%) |
| héber: OSHL (TWOT, BDB-azonosító) | 98/98 (100.0%) | 159/159 (100.0%) |
| héber: TBESH-szócikk | 98/98 (100.0%) | 159/159 (100.0%) |
| héber: tW-szócikk | 55/98 (56.1%) | 124/159 (78.0%) |
| görög: SDGNT-domén | 189/202 (93.6%) | 282/304 (92.8%) |
| görög: UBS_DNTG angol jelentések | 189/202 (93.6%) | 282/304 (92.8%) |
| görög: LSJ-szócikk | 202/202 (100.0%) | 304/304 (100.0%) |
| görög: MCGED (Mounce) | 195/202 (96.5%) | 294/304 (96.7%) |
| görög: SECE_G-szócikk | 202/202 (100.0%) | 304/304 (100.0%) |
| görög: tW-szócikk | 89/202 (44.1%) | 141/304 (46.4%) |
| görög: ÚSZ-hely UBS_DNTG-besorolása (a lapon listázott helyek) | 819/879 (93.2%) | 1214/1298 (93.5%) |

### 7.2 Vers-lapok (vers-kulcs)

- `scope=1Móz 1:1–2:3 | forras=konkordancia/{BSB_Strongs,KJV_Strongs_teljes,Nave_basokant,TIPNR_kivonat,LXX_versszintu_parok,LXX_tobblet_szakaszok,Verzifikacios_elteres_tabla}.tsv + adat/{elofordulasok,kapcsolatok,lxx_dontesek,motivumok}.tsv; vers-kulcs: eszkozok/olvaso_pilot/bovites.py (gépi illesztés) | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=konkordancia/{BSB_Strongs,KJV_Strongs_teljes,Nave_basokant,TIPNR_kivonat,LXX_versszintu_parok,LXX_tobblet_szakaszok,Verzifikacios_elteres_tabla}.tsv + adat/{elofordulasok,kapcsolatok,lxx_dontesek,motivumok}.tsv; vers-kulcs: eszkozok/olvaso_pilot/bovites.py (gépi illesztés) | ts=2026-10-07T14:29Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| vers, amelyhez van BSB-sor (MT-kulcs) | 34/34 (100.0%) | 30/32 (93.8%) |
| BSB-szó összesen (ebből „elhagyva” állapotú) | 461 (35) | 232 (4) |
| BSB „Számozás” oszlop értékei a pilot-versekre | mt | mt |
| vers, amelyhez van KJV-sor (KJV-kulcs) | 34/34 (100.0%) | 32/32 (100.0%) |
| KJV-szó összesen | 355 | 196 |
| a KJV-kulcs forrása | LXX_OS KJV-oszlop: 34 | LXX_OS KJV-oszlop: 31; a fejezet eltolása (nincs LXX-szó a versre): 1 |
| a versmegfeleltető tábla KJV-száma eltér a KJV-kulcstól (vers) | 0 | 31 |
| vers, amelyhez van Nave-sor (vers- és tartományhivatkozás) | 34/34 (100.0%) | 31/32 (96.9%) |
| Nave-sor a versekre összesen (ebből tartományból bontva); fejezet-szintű sor | 191 (93); 3 | 130 (64); 8 |
| TIPNR: vers névvel; a szakasz TIPNR-sorai közül illesztve | 1 vers; 1/1 (100.0%) | 7 vers; 9/9 (100.0%) |
| adat/elofordulasok.tsv: sor a szakasz verseire | 2 | 0 |
| adat/kapcsolatok.tsv: sor a szakasz verseire | 3 | 0 |
| adat/lxx_dontesek.tsv: sor a szakasz verseire | 0 | 0 |
| LXX versszintű együttelőfordulás: vers; pár | 29/34 (85.3%); 497 | 4/32 (12.5%); 31 |
| LXX_tobblet_szakaszok / Verzifikacios_elteres_tabla: sor | 0 / 0 | 0 / 0 |

### 7.3 Morfológia és méret

- `scope=1Móz 1:1–2:3 | forras=adat/morf_kulcs_heber.tsv + adat/morf_nyelv_aramai.tsv; Macula-kód: konkordancia/Macula_heber_*.tsv; feldolgozás: eszkozok/olvaso_pilot/bovites.py (gépi feldolgozás) | ts=2026-10-07T14:29Z`
- `scope=Zsolt 22 | forras=adat/morf_kulcs_heber.tsv + adat/morf_nyelv_aramai.tsv; Macula-kód: konkordancia/Macula_heber_*.tsv; feldolgozás: eszkozok/olvaso_pilot/bovites.py (gépi feldolgozás) | ts=2026-10-07T14:29Z`

| Mérőszám | 1Móz 1:1–2:3 | Zsolt 22 |
|---|---|---|
| Macula-szó morfológiai kóddal, ebből magyarul feloldva (a nyers kód mellett marad) | 746/746 (100.0%) | 388/388 (100.0%) |
| ismeretlen jelű kód (a jelkulcs nem oldja fel) | 0 | 0 |
| arámi szó a szakaszban (adat/morf_nyelv_aramai.tsv) | 0 | 0 |
| olvaso_pilot.json mérete (bájt) | 4 635 070 | 6 316 611 |
| karoli_konkordancia_proba.html mérete (bájt; egyetlen fájl, minden adat beágyazva) | 4 727 842 | 6 409 362 |

A legnagyobb HTML 6 409 362 bájt, vagyis 8 MB alatt van: lusta betöltésre vagy külön JSON-ra nem kellett áttérni (a határ átlépése esetén a nagy szövegek: SECE, LSJ, tW, TBESH, BDB teljes szöveg külön JSON-ba kerülnének).

