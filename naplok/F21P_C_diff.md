# F21P_C_diff.md — a C (F3) eltérései az Opus-aranytól és a régi aranytól

<!-- GENERÁLT: eszkozok/karoli_strong/c_diff.py | scope=f21p F3, a kapun átment aranyversek (60) és a C régi-arany-hármasai | forras=f21p/valaszok/F3.jsonl, f21p/arany_opus.jsonl, f21p/meres_kizaras.tsv, f21p/c_diff_besorolas.tsv, f21p/c_regi_arany_besorolas.tsv, f21p/arany_opus_v2.jsonl, f21p/regi_arany_hibas.tsv, konkordancia/Karoli_Strong_kivonat.tsv | ts=2026-09-30T13:12:52+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

**A számok a szkript kimenetei** (a meres.py definícióival: link = (magyar sorszám, eredeti sorszám), a f21p/meres_kizaras.tsv tokenjei nélkül). **Az osztályba sorolás kézi ítélet (Opus, F21.11), nem mérés.** Osztályok: (a) konvenciókülönbség — a f21p/arany_opus_jegyzetek.md 2. szakaszának tíz konvenciója; (b) az arany vitatható döntése — a jegyzet 6. szakaszának táblázata; (c) a C valódi hibája az arany szerint; a régi aranynál (d) a régi arany hibás, (e) mérési műtermék (a megadott felosztáson túli osztály, l. 6. pont).

## 1. Eltérések rétegenként és osztályonként

| réteg | versek | C link | arany link | közös | hiányzó (a / b / c) | többlet (a / b / c) |
|---|---|---|---|---|---|---|
| R1 | 20 | 312 | 317 | 294 | 23 (15 / 6 / 2) | 18 (6 / 10 / 2) |
| R2 | 10 | 155 | 153 | 146 | 7 (7 / 0 / 0) | 9 (7 / 2 / 0) |
| R3 | 10 | 272 | 266 | 250 | 16 (8 / 0 / 8) | 22 (8 / 6 / 8) |
| R4 | 20 | 322 | 315 | 299 | 16 (8 / 1 / 7) | 23 (11 / 2 / 10) |
| Összes | 60 | 1061 | 1051 | 989 | 62 (38 / 7 / 17) | 72 (32 / 20 / 20) |

## 2. Pontosság és lefedettség: a P4 mérés és a korrigált érték

A **P4** sor a meres.py definíciója (a f21p/meres_eredmeny.tsv C-sorával azonos kell legyen). A **korrigált** sor NEM mérés: az (a) és (b) osztályú eltéréseket a **kézi besorolás (Opus, F21.11)** alapján nem-hibának veszi — a többlet (a)/(b) linkeket a pontosság, a hiányzó (a)/(b) linkeket a lefedettség számlálójához adja. A korrekció tehát ítéletfüggő.

| réteg | mérőszám | P4 (mérés) | korrigált (az Opus besorolása, nem mérés) |
|---|---|---|---|
| R1 | pontosság | 94.2% (294/312) | 99.4% (310/312) |
| R1 | lefedettség | 92.7% (294/317) | 99.4% (315/317) |
| R2 | pontosság | 94.2% (146/155) | 100.0% (155/155) |
| R2 | lefedettség | 95.4% (146/153) | 100.0% (153/153) |
| R3 | pontosság | 91.9% (250/272) | 97.1% (264/272) |
| R3 | lefedettség | 94.0% (250/266) | 97.0% (258/266) |
| R4 | pontosság | 92.9% (299/322) | 96.9% (312/322) |
| R4 | lefedettség | 94.9% (299/315) | 97.8% (308/315) |
| Összes | pontosság | 93.2% (989/1061) | 98.1% (1041/1061) |
| Összes | lefedettség | 94.1% (989/1051) | 98.4% (1034/1051) |

## 3. Az (a) és (b) eltérések konvenció, ill. jegyzetpont szerint (kézi besorolás)

| osztály | konvenció / jegyzetpont | eltérés (link) |
|---|---|---|
| a | K1 névelők (2. szakasz 1.) | 12 |
| a | K10 összeolvadt névelő + elöljáró (2. szakasz 10.) | 3 |
| a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.) | 12 |
| a | K3 tárgyjelölő névmási raggal (2. szakasz 3.) | 6 |
| a | K4 birtokos és névmási ragok (2. szakasz 4.) | 29 |
| a | K6 külön kitett alanyi névmás (2. szakasz 6.) | 2 |
| a | K7 segédige (2. szakasz 7.) | 2 |
| a | K9 le nem fordított ve-/kai (2. szakasz 9.) | 4 |
| b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | 1 |
| b | 6. szakasz táblázat: 1Pét 5:12 | 1 |
| b | 6. szakasz táblázat: 2Móz 20:25 | 1 |
| b | 6. szakasz táblázat: 2Móz 21:26 | 2 |
| b | 6. szakasz táblázat: 2Móz 25:40 | 4 |
| b | 6. szakasz táblázat: 2Móz 25:8 | 1 |
| b | 6. szakasz táblázat: 2Móz 30:3 | 2 |
| b | 6. szakasz táblázat: Ez 11:3 | 1 |
| b | 6. szakasz táblázat: Ez 16:57 | 1 |
| b | 6. szakasz táblázat: Ez 33:31 | 3 |
| b | 6. szakasz táblázat: Mt 5:34 | 2 |
| b | 6. szakasz táblázat: Péld 28:17 | 2 |
| b | 6. szakasz táblázat: Péld 30:17 | 2 |
| b | 6. szakasz táblázat: Péld 31:5 | 1 |
| b | 6. szakasz táblázat: Péld 31:8 | 1 |
| b | 6. szakasz táblázat: Zsolt 18:1 | 2 |

## 4. A (c) esetek — a C valódi hibái az arany szerint (mind, kézi besorolás)

Összesen 37 (c) eltérés; ebből 13-nél az indok jelzi, hogy az arany döntése is vitatható, de a jegyzet 6. szakaszának táblázatában nem szerepel (a (b) definíciója ezért nem alkalmazható rájuk).

| vers | irány | magyar szó | eredeti szó (sorszám, alak, Strong, tükör) | osztály | konvenció / jegyzetpont | indok (kézi) |
|---|---|---|---|---|---|---|
| Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | c | — | a -י (fiam) rag a fiam-hoz tartozik; a C a betoldott engem-hez köti, a fiam-hoz nem |
| Péld 23:19 | tobblet | 4 engem | 4 י H9020 [my] | c | — | az engem Károli betoldása (a héberben nincs tárgy); a C a fiam birtokos ragját köti hozzá |
| Péld 31:8 | hianyzo | 13 dolgában | 6 אֶל H0413 [to] | c | — | az אֶל (a ... ügyében) a dolgában -ban ragja; a C az és-hez köti |
| Péld 31:8 | tobblet | 11 és | 6 אֶל H0413 [to] | c | — | az és (betoldas) nem felel meg az אֶל-nek („felé, ügyében”); a jegyzet 6. táblázata az és betoldas-t felsorolja, de a C választása nyelvileg nem védhető |
| Jer 46:21 | hianyzo | 2 zsoldosai | 3 הָ H9024 [its] | c | — | a zsoldosai birtokos ragja (-hā); a C az is-hez köti, a zsoldosai-hoz nem |
| Jer 46:21 | hianyzo | 3 is | 1 גַּם H1571 [also] | c | — | Még ... is = גַּם (1); a C az első is-t a második גַם-hoz köti |
| Jer 46:21 | hianyzo | 4 olyanok | 7 כְּ H9004 [[are] like] | c | — | olyanok ... mint = כְּ; a C csak a mint-et köti [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Jer 46:21 | hianyzo | 13 is | 11 גַם H1571 [also] | c | — | ők is = גַם הֵמָּה: a második is a második גַם; a C ezt az első is-hez tette |
| Jer 46:21 | tobblet | 3 is | 3 הָ H9024 [its] | c | — | az is nem birtokos rag; a C a zsoldosai ragját köti hozzá |
| Jer 46:21 | tobblet | 3 is | 11 גַם H1571 [also] | c | — | az első is a C-nél a második גַם-on (l. fent) |
| Jer 51:3 | hianyzo | 8 arra | 8 אֶל H0408 [may not] | c | — | arra = a második אֶל (a jegyzet 3. szakasza szerint Károli „felé” értelemben olvassa); a C a ki-hez köti |
| Jer 51:3 | hianyzo | 11 pánczéljába | 10 בְּ H9003 [in] | c | — | a be- a pánczéljába -ba ragja; a C az arra-hoz köti |
| Jer 51:3 | tobblet | 8 arra | 10 בְּ H9003 [in] | c | — | az arra nem a be- elöljáró (l. fent) |
| Jer 51:3 | tobblet | 10 ki | 8 אֶל H0408 [may not] | c | — | a ki (vonatkozó) nem az אֶל; az arany: a ki betoldas |
| Ez 11:3 | tobblet | 9 város | 10 סִּ֔יר H5518 [pot] | c | — | a város nem a „fazék” (סִיר); a 6. táblázat a város döntését felsorolja (alternatíva: város -> 8, הִיא), de a C választása nyelvileg nem védhető |
| Ez 16:57 | hianyzo | 16 valóknak | 13 סְבִיבוֹתֶ֖י H5439 [around] | c | — | körülötted valóknak: az arany a valóknak-ot is a סְבִיבוֹת-hoz köti, a C betoldas-nak veszi [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Ez 22:25 | hianyzo | 7 olyanok | 7 כַּ H9004 [like] | c | — | olyanok ... mint = כַּ; a C csak a mint-et köti [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Ez 33:31 | tobblet | 32 pedig | 30 הֵ֣מָּה H1992 [they] | c | — | a pedig nem a הֵמָּה („ők”); a 6. táblázat a הֵמָּה forditatlan döntését felsorolja (alternatíva: azokat -> 30), de a C választása nyelvileg nem védhető |
| Ez 46:12 | tobblet | 25 ő | 27 וֹ֙ H9023 [his] | c | — | az ő a vigye alanya (K6: betoldas), nem az égőáldozatát birtokos ragja; a C a -וֹ ragot köti hozzá |
| Ez 46:12 | tobblet | 39 azután | 40 יָצָ֛א H3318 [he will go out] | c | — | az azután Károli betoldása; a C az יָצָא („kimegy”) igéhez köti, amely már a menjen ki-é |
| Mt 6:31 | hianyzo | 5 ne | 1 μὴ G3361 [Not] | c | — | és ne mondjátok: az arany a második ne-t is a μή-hez köti; a C betoldas-nak veszi [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Mt 11:18 | tobblet | 4 a | 4 μήτε G3383 [neither] | c | — | a ki (vonatkozó, a melléknévi igenevet fordítja) nem a μήτε; a μήτε a sem-é |
| Mt 11:18 | tobblet | 5 ki | 4 μήτε G3383 [neither] | c | — | mint fent |
| Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | c | — | azért ... hogy = ἵνα: az arany a korrelatív azért-et is a ἵνα-hoz köti; a C betoldas-nak veszi [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Mt 21:4 | hianyzo | 8 próféta | 9 διὰ G1223 [through] | c | — | a próféta mondása: az arany a διά-t a próféta-hoz köti; a C forditatlan-nak veszi [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Mt 23:31 | hianyzo | 2 hát | 1 ὥστε G5620 [Thus] | c | — | Így hát = ὥστε: az arany mindkét tokent köti; a C csak az így-et [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Jak 3:4 | tobblet | 12 mindazáltal | 12 μετάγεται G3329 [are turned about] | c | — | a mindazáltal Károli betoldása; a C a μετάγεται igéhez köti, amely a fordíttatnak-é |
| Jak 3:4 | tobblet | 16 oda | 17 ἂν G0302 [ever] | c | — | az ἄν a hová-hoz tartozik (ὅπου ἄν), nem a korrelatív oda-hoz |
| Jak 3:4 | tobblet | 23 akarja | 19 ὁρμὴ G3730 [impulse] | c | — | az akarja a (kizárt, TR-alakú) βούλεται-é; a C az ὁρμή-t („szándék”) is hozzáköti, amely a szándéka-é |
| 1Pét 4:11 | hianyzo | 14 erővel | 11 ἐξ G1537 [of] | c | — | azzal az erővel: az arany az ἐκ-et az erővel-hez köti (a -vel ragja), a C az azzal-hoz [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 7 szólja | 3 λαλεῖ G2980 [speaks] | c | — | a szólja Károli kiegészítése (a jegyzet 5. szakasza szerint betoldas); a C az első λαλεῖ-hez is köti [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 12 azzal | 11 ἐξ G1537 [of] | c | — | az ἐκ a C-nél az azzal-on (l. fent) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 15 szolgáljon | 9 διακονεῖ G1247 [serves] | c | — | a szolgáljon Károli kiegészítése (5. szakasz); a C a διακονεῖ-hez is köti [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 21 ὁ G3588 [<the>] | c | — | Károli a második ὁ θεός-t nem fordítja (5. szakasz); a C a névelőt a dícsőíttessék-hez köti |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 22 θεὸς G2316 [God] | c | — | a θεός nem a dícsőíttessék ige megfelelője; Károlinál nincs fordítva (5. szakasz) |
| 2Pét 1:7 | hianyzo | 6 való | 6 φιλαδελφίαν, G5360 [brotherly affection,] | c | — | atyafiakhoz való hajlandóságot: az arany a való-t is a φιλαδελφία-hoz köti, a C betoldas-nak veszi [az arany döntése is vitatható; a jegyzetben nem szerepel] (vö. Péld 30:17 iránt való: ott az arany betoldas) |
| 2Pét 1:7 | hianyzo | 10 való | 10 φιλαδελφίᾳ G5360 [brotherly affection] | c | — | mint fent [az arany döntése is vitatható; a jegyzetben nem szerepel] |

## 5. Jellemző példák (a) és (b) osztályból (kézi válogatás)

| vers | irány | magyar szó | eredeti szó (sorszám, alak, Strong, tükör) | osztály | konvenció / jegyzetpont | indok (kézi) |
|---|---|---|---|---|---|---|
| 2Móz 21:6 | hianyzo | 6 ura | 5 ו֙ H9023 [his] | a | K4 birtokos és névmási ragok (2. szakasz 4.) | az ő ura: a rag az arany szerint a névmáshoz és a birtokszóhoz is; a C csak az ő-höz |
| 2Móz 20:25 | tobblet | 9 azt | 10 אֶתְ H0853 [<obj.>] | a | K3 tárgyjelölő névmási raggal (2. szakasz 3.) | a C az 'et-et is a névmáshoz köti; az arany az 'et-et forditatlan-nak veszi |
| 2Móz 20:25 | tobblet | 14 mint | 13 כִּ֧י H3588 [for] | b | 6. szakasz táblázat: 2Móz 20:25 | az arany: a mint betoldas; a C a jegyzetben megnevezett alternatívát választotta (a mint -> כִּי), itt a mint tokennel |
| 2Móz 21:26 | tobblet | 1 Ha | 1 וְ H9002 [and] | b | 6. szakasz táblázat: 2Móz 21:26 | az arany: a kezdő ve- forditatlan; a C a jegyzet alternatíváját választotta (Ha -> 1, 2) |
| 2Móz 25:8 | tobblet | 7 ő | 10 ם H9028 [them] | b | 6. szakasz táblázat: 2Móz 25:8 | az arany: ő betoldas (1. sz. igéhez nem illő névmás); a C az ő-t a -ām raghoz köti: az ő közöttök archaikus birtokos névmás (vö. K4), tehát a C olvasata valószínűleg helyes, az aranyé hibás; a jegyzet nem nevezett alternatívát |
| 2Móz 26:13 | tobblet | 11 mi | 12 עֹדֵ֔ף H5736 [surplus] | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.) | a mi: az arany betoldas (a K2 listájában), a C a jegyzetben megnevezett opciót választotta (az igenévhez köti) |
| Péld 30:17 | tobblet | 10 iránt | 7 לִֽ H9005 [<to>] | b | 6. szakasz táblázat: Péld 30:17 | iránt -> li-: a jegyzet alternatívája |
| Zsolt 16:11 | tobblet | 1 Te | 1 תּֽוֹדִיעֵ H3045 [you will make known to] | a | K6 külön kitett alanyi névmás (2. szakasz 6.) | a külön kitett Te: az arany betoldas, a C az igéhez köti |
| Zsolt 18:1 | tobblet | 14 azon | 18 בְּ H9003 [on] | b | 6. szakasz táblázat: Zsolt 18:1 | az arany: azon betoldas; a C a jegyzet alternatíváját választotta (azon -> 18), és a יוֹם-ra is kiterjesztette |
| Zsolt 18:3 | tobblet | 22 szarva | 19 וְ H9002 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.) | a magyarban nincs és; a C a ve-t a szarva-hoz köti, az arany forditatlan |
| Jer 51:3 | tobblet | 2 kézívesre | 2 יִדְרֹ֤ךְ H1869 [he bend] | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | a Ketiv kettőzött igéje (a jegyzet 3. szakasza szerint) a kézívesre része; a C a meglévő יִדְרֹךְ-ot a kézívesre-hez is köti, ami a Ketiv-olvasatot tükrözi. Felhasználói döntés (F21.12): (b) a jegyzet 3. szakasza alapján; a 6. táblázatba nem kerül be, hanem a 3. szakaszra hivatkozik |
| Ez 11:3 | tobblet | 1 Mondván | 1 הָ H9009 [who] | b | 6. szakasz táblázat: Ez 11:3 | az arany: a vonatkozó הָ forditatlan; a C a jegyzet alternatíváját választotta (Mondván -> 1, 2) |
| Ez 39:13 | tobblet | 3 fog | 2 קָֽבְרוּ֙ H6912 [they will bury [them]] | a | K7 segédige (2. szakasz 7.) | a fog segédige: a C az igéhez köti |
| Mk 2:10 | tobblet | 10 e | 13 ἐπὶ G1909 [on] | a | K10 összeolvadt névelő + elöljáró (2. szakasz 10.) | mint fent |
| 1Pét 4:11 | tobblet | 29 dicsőség | 28 ἡ G3588 [the] | a | K1 névelők (2. szakasz 1.) | a névelőt (ἡ) a C a dicsőség-hez köti |

## 6. A régi arany (C, kapun átment versek)

**Definíció (F21.12, meres.regi_egyezik):** a régi Strong mezőt „+” mentén összetevőkre bontjuk; a hármas egyezik, ha a Károli-szó (kifejezés) valamelyik előfordulásához linkelt eredeti szavak Strongjai között MINDEN összetevő ott van. A korábbi (F21.10) definíció a Strong mezőt egész karakterláncként hasonlította, ezért összetett Strong sosem egyezhetett; az itt csak kontroll.

| mérőszám | érték |
|---|---|
| egyezés — korábbi, összetett Strong nélkül (kontroll) | 75.0% (24/32) |
| egyezés — halmaz-definíció, kizárás nélkül | 93.8% (30/32) |
| kizárva: a régi arany hibás (f21p/regi_arany_hibas.tsv) | 2 hármas |
| egyezés — halmaz-definíció, a hibás hármasok nélkül | 100.0% (30/30) |

A korábbi definíció szerint nem egyező 8 hármas (kontroll). Az osztály kézi ítélet; (d) = a régi arany (konkordancia/Karoli_Strong_kivonat.tsv) maga a hibás.

| vers | Károli-szó | régi Strong | a C linkje(i) ehhez a szóhoz | halmaz-definíció | hibás-jelölés | osztály | indok (kézi) |
|---|---|---|---|---|---|---|---|
| 1Móz 4:12 | bujdosó és vándorló | H5128+H5110 | 14 bujdosó -> 13 נָ֥ע H5128 [a wanderer]; 15 és -> 14 וָ H9002 [and]; 16 vándorló -> 15 נָ֖ד H5110 [a fugitive] | egyezik | — | e | mérési műtermék: a régi arany összetett Strongot ad (+), a meres.py korábban (F21.10) a teljes karakterláncot hasonlította, így ez sosem egyezhetett (F21.12-ben javítva); mindkét összetevő a C linkjei között van |
| 1Móz 6:17 | élő lélek | H5315+H2416 | 14 élő -> 21 חַיִּ֔ים H2416 [life]; 15 lélek -> 20 ר֣וּחַ H7307 [[the] breath of] | nem egyezik | kizárva (hibás) | d | a régi arany hibás: a versben nincs H5315 (a héber רוּחַ חַיִּים, H7307 + H2416); a C lélek -> H7307 linkje helyes. Összetett Strong is (l. e) |
| 1Móz 7:23 | és csak Noé marada meg | H7604+H0389 | 29 és -> 28 וַ H9001 [and]; 30 csak -> 30 אַךְ H0389 [only]; 31 Noé -> 31 נֹ֛חַ H5146 [Noah]; 32 marada -> 29 יִשָּׁ֧אֶר H7604 [he was left]; 33 meg -> 29 יִשָּׁ֧אֶר H7604 [he was left] | egyezik | — | e | mérési műtermék (összetett Strong); mindkét összetevő a C linkjei között van |
| 1Móz 12:8 | segítségűl hívá az Úr nevét | H7121+H8034 | 25 segítségűl -> 33 יִּקְרָ֖א H7121 [he called]; 26 hívá -> 33 יִּקְרָ֖א H7121 [he called]; 27 az -> —; 28 Úr -> 36 יְהוָֽה H3068 [Yahweh]; 29 nevét -> 34 בְּ H9003 [on], 35 שֵׁ֥ם H8034 [[the] name of] | egyezik | — | e | mérési műtermék (összetett Strong); mindkét összetevő a C linkjei között van |
| 1Móz 12:17 | nagy csapásokkal | H5061+H1419 | 11 nagy -> 7 גְּדֹלִ֖ים H1419 [great]; 12 csapásokkal -> 6 נְגָעִ֥ים H5061 [plagues] | egyezik | — | e | mérési műtermék (összetett Strong); mindkét összetevő a C linkjei között van |
| 1Móz 13:4 | segítségűl hívá | H7121+H3068 | 11 segítségűl -> 11 יִּקְרָ֥א H7121 [he called]; 12 hívá -> 11 יִּקְרָ֥א H7121 [he called] | nem egyezik | kizárva (hibás) | d | a régi arany vitatható: a segítségűl hívá kifejezésben nincs YHWH (az a versben az Úrnak szó, a C ott köti); a H7121 a C linkjei között van. Összetett Strong is (l. e) |
| 1Móz 13:14 | Emeld fel szemeidet | H5375+H5869 | 10 Emeld -> 12 שָׂ֣א H5375 [lift up]; 11 fel -> 12 שָׂ֣א H5375 [lift up]; 12 szemeidet -> 14 עֵינֶ֙י H5869 [eyes], 15 ךָ֙ H9021 [your] | egyezik | — | e | mérési műtermék (összetett Strong); mindkét összetevő a C linkjei között van |
| 1Móz 13:4 | segítségűl hívá ott Ábrám az Úrnak nevét | H7121+H8034 | 11 segítségűl -> 11 יִּקְרָ֥א H7121 [he called]; 12 hívá -> 11 יִּקְרָ֥א H7121 [he called]; 13 ott -> 12 שָׁ֛ם H8033 [there]; 14 Ábrám -> 13 אַבְרָ֖ם H0087 [Abram]; 15 az -> —; 16 Úrnak -> 16 יְהוָֽה H3068 [Yahweh]; 17 nevét -> 14 בְּ H9003 [on], 15 שֵׁ֥ם H8034 [[the] name of] | egyezik | — | e | mérési műtermék (összetett Strong); mindkét összetevő a C linkjei között van |

(e) = mérési műtermék (F21.12-ben elfogadva, a meres.py-ban javítva): a Karoli_Strong_kivonat.tsv összetett Strongja („H5128+H5110”) a korábbi egyezésvizsgálatban egész karakterláncként szerepelt. A halmaz-definícióval mind a 6 (e) hármas egyezik.

Osztályonként (kézi): (a) 0, (b) 0, (c) 0, (d) 2, (e) 6.

## 7. A C diffje az arany v2-höz (f21p/arany_opus_v2.jsonl; jóváhagyásig nem befagyasztott)

A v1-es P4 (naplok/F21P_meres_v1.md) és a fenti 1–6. pont változatlanul a v1-re vonatkozik. A **mért** érték a meres.py definíciója a megadott aranyhoz; a **korrigált** érték **az Opus besorolása, nem mérés** (az (a)/(b) eltérést nem-hibának veszi). A küszöb szempontjából csak a mért érték számít.

| réteg | mérőszám | v1 mért | v2 mért | v1 korrigált (Opus besorolása, nem mérés) | v2 korrigált (Opus besorolása, nem mérés) |
|---|---|---|---|---|---|
| R1 | pontosság | 94.2% (294/312) | 94.6% (295/312) | 99.4% (310/312) | 99.4% (310/312) |
| R1 | lefedettség | 92.7% (294/317) | 93.1% (295/317) | 99.4% (315/317) | 99.4% (315/317) |
| R2 | pontosság | 94.2% (146/155) | 94.2% (146/155) | 100.0% (155/155) | 100.0% (155/155) |
| R2 | lefedettség | 95.4% (146/153) | 95.4% (146/153) | 100.0% (153/153) | 100.0% (153/153) |
| R3 | pontosság | 91.9% (250/272) | 91.9% (250/272) | 97.1% (264/272) | 97.1% (264/272) |
| R3 | lefedettség | 94.0% (250/266) | 94.0% (250/266) | 97.0% (258/266) | 97.0% (258/266) |
| R4 | pontosság | 92.9% (299/322) | 92.9% (299/322) | 96.9% (312/322) | 96.9% (312/322) |
| R4 | lefedettség | 94.9% (299/315) | 94.9% (299/315) | 97.8% (308/315) | 97.8% (308/315) |
| Összes | pontosság | 93.2% (989/1061) | 93.3% (990/1061) | 98.1% (1041/1061) | 98.1% (1041/1061) |
| Összes | lefedettség | 94.1% (989/1051) | 94.2% (990/1051) | 98.4% (1034/1051) | 98.4% (1034/1051) |

Eltérések a v1-hez képest: 2 eltérés megszűnt, 0 új (összes v1: 134, v2: 132).

| vers | irány | magyar szó | eredeti szó | v1-osztály | v2 |
|---|---|---|---|---|---|
| 2Móz 25:8 | tobblet | 7 ő | 10 ם H9028 [them] | b | egyező |
| 2Móz 26:13 | hianyzo | 24 másfelől | 26 וּ H9002 [and] | a | egyező |

