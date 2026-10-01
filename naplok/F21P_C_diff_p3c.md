# F21P_C_diff_p3c.md — a (c) hibák újrabesorolása: C (F3V3) eltérései az arany v3-höz, a v2-es C-futásokkal összevetve

<!-- GENERÁLT: eszkozok/karoli_strong/c_diff_p3c.py --csak-c | scope=F3V3 (prompt_v3) a kapun átment aranyversekre, arany v3 (60 vers, sha256 acdeb55f969c96fe); az F3V3 (c) esetei a v2-es C-futások (F3V2, F3V2B; arany v2) (c) eseteivel összevetve | forras=f21p/valaszok/{F3V3,F3V2,F3V2B}.jsonl, arany_opus_v3.jsonl (sha256 ellenőrizve), f21p/arany_opus_v2.jsonl, f21p/meres_kizaras.tsv, f21p/c_diff_f3v2_osszevetes.tsv, f21p/c_diff_f3v2b_besorolas.tsv, f21p/c_diff_p3c_besorolas.tsv (MANUAL) | ts=2026-10-01T07:58:58+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

Gépi diff: a kapun átment aranyverseken az arany linkjeiből hiányzó és a futás többlet linkjei; az állapot (eltérés / megszűnt / nem mérhető), az előzmény (a v2-es C-futások arany v2-höz mért eltérései és azok v2-es kézi osztálya) és az arany v2 → v3 változása gépi. **Az osztályok (a / b / c), a konvenció és a változást magyarázó konvenció kézi besorolás: Opus-besorolás, nem mérés.** A mért értékek (pontosság, lefedettség, küszöb-viszony) a naplok/F21P_meres_p3c_c.md-ben; a küszöb szempontjából csak azok számítanak.

A SONNETV3 még nem futott; a Sonnet eltéréseinek besorolása a Sonnet-adat megérkezése után (--sablon --hozzafuz, --csak-c nélkül).

## 1. Eltérések futásonként és rétegenként (gépi)

| futás | réteg | aranyversek (kapun átment) | hiányzó | többlet | eltérő versek |
|---|---|---|---|---|---|
| C (F3V3) | R1 | 20 | 21 | 11 | 13 |
| C (F3V3) | R2 | 10 | 0 | 6 | 5 |
| C (F3V3) | R3 | 10 | 10 | 15 | 7 |
| C (F3V3) | R4 | 20 | 8 | 18 | 12 |
| C (F3V3) | Összes | 60 | 39 | 50 | 37 |
| C (F3V2) × arany v2 | R1 | — | 18 | 19 | 14 |
| C (F3V2) × arany v2 | R2 | — | 0 | 7 | 4 |
| C (F3V2) × arany v2 | R3 | — | 7 | 16 | 8 |
| C (F3V2) × arany v2 | R4 | — | 6 | 28 | 13 |
| C (F3V2) × arany v2 | Összes | — | 31 | 70 | 39 |
| C (F3V2B) × arany v2 | R1 | — | 13 | 20 | 11 |
| C (F3V2B) × arany v2 | R2 | — | 1 | 7 | 3 |
| C (F3V2B) × arany v2 | R3 | — | 3 | 17 | 9 |
| C (F3V2B) × arany v2 | R4 | — | 9 | 33 | 14 |
| C (F3V2B) × arany v2 | Összes | — | 26 | 77 | 37 |

### Az F3V3 sorainak állapota rétegenként (gépi)

| réteg | eltérés | ebből: a v2-ben is eltérés | ebből: a v2-ben (c) | megszűnt v2 (c) | nem mérhető v2 (c) | az arany v2→v3-ban változott szó |
|---|---|---|---|---|---|---|
| R1 | 32 | 23 | 3 | 12 | 0 | 0 |
| R2 | 6 | 4 | 0 | 1 | 0 | 1 |
| R3 | 25 | 17 | 5 | 7 | 0 | 0 |
| R4 | 26 | 18 | 8 | 19 | 0 | 2 |
| Összes | 89 | 62 | 16 | 39 | 0 | 3 |

## 2. A kézi besorolás (a / b / c) rétegenként, a v2-es C-futásokkal egymás mellett (Opus-besorolás, nem mérés)

Az F3V3 az arany v3-hoz, az F3V2 és az F3V2B a saját aranyához (v2) mérve, a v2-es kézi besorolással (F21.16, F21.31).

| réteg | F3V2 a | F3V2 b | F3V2 c | F3V2B a | F3V2B b | F3V2B c | C (F3V3) a | C (F3V3) b | C (F3V3) c |
|---|---|---|---|---|---|---|---|---|---|
| R1 | 15 | 9 | 13 | 15 | 12 | 6 | 19 | 9 | 4 |
| R2 | 3 | 3 | 1 | 6 | 2 | 0 | 4 | 2 | 0 |
| R3 | 12 | 3 | 8 | 7 | 4 | 9 | 8 | 8 | 9 |
| R4 | 16 | 1 | 17 | 19 | 2 | 21 | 11 | 4 | 11 |
| Összes | 46 | 16 | 39 | 47 | 20 | 36 | 42 | 23 | 24 |

## 3. Az F3V3 (c) esetei a v2-es C-futások (c) eseteihez képest (Opus-besorolás, nem mérés)

v2 (c) = az F3V2 vagy az F3V2B (c) esete (kulcs: vers, irány, magyar szó, eredeti szó). **maradt** = az F3V3-nál is eltérés és (c); **megszűnt** = az F3V3-nál nem eltérés; **átsorolt** = az F3V3-nál is eltérés, de a jegyzet v2 / arany v3 szerint (a) vagy (b); **új** = az F3V3 (c) esete, amely a v2-ben nem volt (c). Az „arany v2→v3: változott” jelölésű sorokban a változást (részben) az arany változása okozza, nem a modell.

| réteg | v2 (c) összesen | F3V2 (c) | F3V2B (c) | F3V3 (c) | maradt | megszűnt | ebből mindkét v2-ben (c) | átsorolt (a/b) | nem mérhető | új (c) |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | 15 | 13 | 6 | 4 | 2 | 12 | 2 | 1 | 0 | 2 |
| R2 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| R3 | 12 | 8 | 9 | 9 | 5 | 7 | 2 | 0 | 0 | 4 |
| R4 | 27 | 17 | 21 | 11 | 8 | 19 | 5 | 0 | 0 | 3 |
| Összes | 55 | 39 | 36 | 24 | 15 | 39 | 9 | 1 | 0 | 9 |

A „megszűnt” eset, amely csak az egyik v2-futásban volt (c), a futásközi ingadozással is összefér (a két v2-futás azonos prompttal sem adta ugyanazt); a mindkét v2-futásban (c) eset megszűnése erősebb jel.

### Korrigált pontosság és lefedettség — Opus-besorolás, nem mérés

Az (a) és (b) eltérést nem-hibának véve. Az F3V3 az arany v3-hoz, az F3V2 és az F3V2B az arany v2-höz (a saját v2-es kézi besorolásukkal). A küszöb szempontjából csak a mért érték számít (PD10).

| réteg | mérőszám | F3V2 × v2 mért | F3V2 × v2 korrigált (Opus, nem mérés) | F3V2B × v2 mért | F3V2B × v2 korrigált (Opus, nem mérés) | F3V3 × v3 mért | F3V3 × v3 korrigált (Opus-besorolás, nem mérés) |
|---|---|---|---|---|---|---|---|
| R1 | pontosság | 94.0% (299/318) | 97.5% (310/318) | 93.8% (304/324) | 99.1% (321/324) | 96.4% (296/307) | 99.3% (305/307) |
| R1 | lefedettség | 94.3% (299/317) | 98.4% (312/317) | 95.9% (304/317) | 99.1% (314/317) | 93.4% (296/317) | 99.4% (315/317) |
| R2 | pontosság | 95.6% (153/160) | 99.4% (159/160) | 95.6% (152/159) | 100.0% (159/159) | 96.2% (152/158) | 100.0% (158/158) |
| R2 | lefedettség | 100.0% (153/153) | 100.0% (153/153) | 99.3% (152/153) | 100.0% (153/153) | 100.0% (152/152) | 100.0% (152/152) |
| R3 | pontosság | 94.2% (259/275) | 97.8% (269/275) | 93.9% (263/280) | 97.5% (273/280) | 94.4% (255/270) | 97.8% (264/270) |
| R3 | lefedettség | 97.4% (259/266) | 99.2% (264/266) | 98.9% (263/266) | 99.2% (264/266) | 96.2% (255/265) | 98.9% (262/265) |
| R4 | pontosság | 91.7% (309/337) | 96.1% (324/337) | 90.3% (306/339) | 95.6% (324/339) | 94.4% (306/324) | 97.8% (317/324) |
| R4 | lefedettség | 98.1% (309/315) | 98.7% (311/315) | 97.1% (306/315) | 98.1% (309/315) | 97.5% (306/314) | 98.7% (310/314) |
| Összes | pontosság | 93.6% (1020/1090) | 97.4% (1062/1090) | 93.0% (1025/1102) | 97.7% (1077/1102) | 95.3% (1009/1059) | 98.6% (1044/1059) |
| Összes | lefedettség | 97.1% (1020/1051) | 99.0% (1040/1051) | 97.5% (1025/1051) | 99.0% (1040/1051) | 96.3% (1009/1048) | 99.1% (1039/1048) |

## 4. A változás konvenciónként (kézi: a valtozas_konvencio oszlop)

segített = a v2 (c) eset megszűnt (vagy a jegyzet v2 szerint már nem hiba), és a megnevezett konvenció (prompt-szabály vagy az arany v3 változása) magyarázza; nem segített = a v2 (c) eset maradt (a változás-konvenció itt a rá vonatkozó szabály, ha van); ártott / új = új (c) eset. „nincs” = nem konvenció, modell-ingadozás. A DT21-oszlop: a jegyzet v2-ben a DT21 melyik a–e döntése módosította a konvenciót (a = K7 szűkítés, b = K3, c = K11, d = 2Móz 26:13 *is*, e = K4 pontosítás). Zárójelben: ebből az arany v2 → v3 változásához kötött sor.

| változás-konvenció | DT21 | segített (v2 (c) megszűnt) | segített (v2 (c) átsorolva a/b-be) | nem mérhető | nem segített (v2 (c) maradt) | ártott / új (c) |
|---|---|---|---|---|---|---|
| K3 | b | 4 | 0 | 0 | 0 | 0 |
| K4 | e | 2 | 1 | 0 | 0 | 0 |
| K7 | a | 2 | 0 | 0 | 0 | 0 |
| K11 | c | 4 (2) | 0 | 0 | 0 | 0 |
| nincs | — | 27 | 0 | 0 | 15 | 9 |

### Az a–e szabályok (DT21) hatása összesítve

| DT21 | konvenció | segített (megszűnt + átsorolt) | nem segített (maradt) | ártott (új c) |
|---|---|---|---|---|
| a | K7 | 2 | 0 | 0 |
| b | K3 | 4 | 0 | 0 |
| c | K11 | 4 | 0 | 0 |
| d | K9 (2Móz 26:13) | 0 | 0 | 0 |
| e | K4 | 3 | 0 | 0 |

## 5. Jellemző példák (kézi válogatás)

| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C (F3V3) | Péld 23:19 | tobblet | 4 engem | 4 י H9020 [my] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az engem (Károli betoldása) most betoldas: a C szabály v3-as szűkítése (DT21 b: a megfelelő nélküli tárgyi névmás betoldas, ne kösd más szóhoz); mindkét v2-futásban (c) volt |
| C (F3V3) | Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | megszunt | F3V2:c, F3V2B:c | — | — | — | K4 (DT21 e) | a -י most a fiam-on (a D szabály v3-as pontosítása, DT21 e: a megfelelő személyragú szó); mindkét v2-futásban (c) volt |
| C (F3V3) | 2Móz 21:26 | tobblet | 9 szemét | 13 וֹ H9023 [his] | megszunt | F3V2:c | — | — | — | K4 (DT21 e) | a -וֹ már nem a szemét-en: a D szabály v3-as pontosítása (DT21 e) pontosan ezt a birtokláncot írja le (nem a közelebbi, hanem a megfelelő személyragú szó); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | elteres | F3V2:c | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | K4 (DT21 e) | a v2-ben (c): a -וֹ a szemét-en (rossz szó). Az F3V3 a ragot már nem a szemét-hez köti (a D szabály v3-as pontosítása, DT21 e: birtokláncban a megfelelő személyragú szó, a prompt példája éppen ez a szerkezet), de a szolgálójának-hoz sem, hanem forditatlan-nak veszi: a hibás link megszűnt, a maradék a K4 alkalmazásának hiánya (a); részleges javulás |
| C (F3V3) | Mt 5:34 | tobblet | 3 azt | 3 λέγω G3004 [say] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az azt (azt mondom) most betoldas: a C szabály v3-as szűkítése (DT21 b: a megfelelő nélküli tárgyi névmás nem kötődik az igéhez); mindkét v2-futásban (c) volt |
| C (F3V3) | Mt 27:18 | tobblet | 2 jól | 1 ᾔδει G1492 [He knew] | megszunt | F3V2:c | — | — | — | K7 (DT21 a) | a jól (határozószó) már nem az ᾔδει-n: a G szabály v3-as szűkítése (DT21 a: a kivétel nem terjed ki a határozószóra); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mk 2:23 | tobblet | 3 hogy | 2 ἐγένετο G1096 [it came to pass] | megszunt | F3V2:c | — | — | — | K7 (DT21 a) | a hogy (lőn, hogy) már nem az ἐγένετο-n: a G szabály v3-as szűkítése (DT21 a: a kivétel nem terjed ki a kötőszóra); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jak 3:1 | tobblet | 7 azt | 8 ὅτι G3754 [that] | megszunt | F3V2:c | — | — | — | K11 (DT21 c) | tudván azt, hogy: az azt most betoldas, a hogy a ὅτι-n: az L szabály (DT21 c) pontosan ezt írja elő; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | megszunt | F3V2B:c | változott | — | — | K11 (DT21 c) | az arany v3-ban az azért betoldas (K11, az arany v2 -> v3 változása); az F3V3 is betoldas-nak veszi (az L szabály szerint): a v2-es „hiányzó” link az arany változásával tárgytalan; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jób 33:13 | tobblet | 4 Azért | 5 כִּ֥י H3588 [that] | elteres | — | változott | a | K11 korrelatív mutató névmás a hogy előtt (8.1; prompt L) | — | az arany v3-ban az Azért betoldas (K11); a C az Azért-et a כִּי-hez is köti (a hogy mellett): az L szabály itt nem érvényesült. Az eltérést az arany v2 -> v3 változása hozta létre (az arany v2 így párosított) |
| C (F3V3) | 2Móz 25:40 | hianyzo | 12 néked | 9 אַתָּ֥ה H0859 [you] | elteres | — | — | c | — | nincs | új: a néked az אַתָּה egyetlen magyar megfelelője (Károli részes esettel adja); a C betoldas-nak veszi, az אַתָּה-t a 3. személyű mutattatott-hoz köti: nem védhető. A C szabály (K3 v2) túláltalánosítása (névmás -> betoldas) nem zárható ki, de a szabály a tárgyi névmásról szól, a néked nem az: konvencióval nem magyarázható |
| C (F3V3) | Jer 51:3 | tobblet | 8 arra | 9 יִתְעַ֖ל H5927 [he lift] | elteres | — | — | c | — | nincs | új: az arra („felé”, a második אֶל) a C-nél az „emeli” (יִתְעַל) igéhez kötve, miután az אֶל-t forditatlan-nak vette: nem védhető; konvenció nem érinti |
| C (F3V3) | Ez 22:25 | hianyzo | 7 olyanok | 7 כַּ H9004 [like] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): olyanok ... mint = כַּ; a C az olyanok-at betoldas-nak veszi. Határeset: az arany döntése is vitatható, a jegyzetben nem szerepel; az L szabály (korrelatívum) túláltalánosítása nem zárható ki, de az L csak az azt/azért … hogy szerkezetről szól |
| C (F3V3) | 1Pét 4:11 | tobblet | 7 szólja | 3 λαλεῖ G2980 [speaks] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a szólja (a jegyzet 5. szakasza szerint Károli-kiegészítés, betoldas) továbbra is a λαλεῖ-hez kötve (maradt) |
| C (F3V3) | Jer 51:3 | hianyzo | 2 kézívesre | 1 אֶֽל H0408 [may not] | elteres | — | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | — | a C mindkét אֶל-t (1, 8) forditatlan-nak veszi (a TAHOT „ne” címkéje szerint); a jegyzet 3. szakasza maga is felkínálja (c) opcióként: az arany döntése vitatható |

## Minden új (c) eset

| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C (F3V3) | 2Móz 25:40 | hianyzo | 12 néked | 9 אַתָּ֥ה H0859 [you] | elteres | — | — | c | — | nincs | új: a néked az אַתָּה egyetlen magyar megfelelője (Károli részes esettel adja); a C betoldas-nak veszi, az אַתָּה-t a 3. személyű mutattatott-hoz köti: nem védhető. A C szabály (K3 v2) túláltalánosítása (névmás -> betoldas) nem zárható ki, de a szabály a tárgyi névmásról szól, a néked nem az: konvencióval nem magyarázható |
| C (F3V3) | 2Móz 25:40 | tobblet | 11 mutattatott | 9 אַתָּ֥ה H0859 [you] | elteres | — | — | c | — | nincs | új: az אַתָּה a mutattatott-hoz kötve; l. a néked sort |
| C (F3V3) | Jer 51:3 | hianyzo | 11 pánczéljába | 10 בְּ H9003 [in] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): a be- a pánczéljába -ba ragja; a C az arra-hoz köti; konvenció nem érinti (az elöljáró kezelése a v3-ban nem változott): modell-ingadozás |
| C (F3V3) | Jer 51:3 | tobblet | 8 arra | 9 יִתְעַ֖ל H5927 [he lift] | elteres | — | — | c | — | nincs | új: az arra („felé”, a második אֶל) a C-nél az „emeli” (יִתְעַל) igéhez kötve, miután az אֶל-t forditatlan-nak vette: nem védhető; konvenció nem érinti |
| C (F3V3) | Jer 51:3 | tobblet | 8 arra | 10 בְּ H9003 [in] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete): az arra nem a be- elöljáró |
| C (F3V3) | Ez 22:25 | hianyzo | 7 olyanok | 7 כַּ H9004 [like] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): olyanok ... mint = כַּ; a C az olyanok-at betoldas-nak veszi. Határeset: az arany döntése is vitatható, a jegyzetben nem szerepel; az L szabály (korrelatívum) túláltalánosítása nem zárható ki, de az L csak az azt/azért … hogy szerkezetről szól |
| C (F3V3) | Mt 21:4 | tobblet | 9 mondása | 9 διὰ G1223 [through] | elteres | — | — | c | — | nincs | új: a διά a mondása-n (az arany: a próféta-n); ugyanannak a v2-es (c) esetnek (a διά helye) új alakja [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | Mt 23:31 | hianyzo | 2 hát | 1 ὥστε G5620 [Thus] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): Így hát = ὥστε; a C a hát-ot betoldas-nak veszi. Határeset [az arany döntése is vitatható; a jegyzetben nem szerepel]; konvenció nem érinti |
| C (F3V3) | Jak 3:4 | tobblet | 12 mindazáltal | 12 μετάγεται G3329 [are turned about] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): a mindazáltal (Károli betoldása) a μετάγεται-hez kötve, amely a fordíttatnak-é |

## Minden megszűnt v2 (c) eset (az F3V3-nál nem eltérés)

| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C (F3V3) | 2Móz 20:25 | tobblet | 13 a | 18 הָ H9034 [it] | megszunt | F3V2:c | — | — | — | nincs | az a mint már nem a rávetetted tárgyragján (-hā); az F3V3 a mint-et a כִּי-hez köti (a 6. táblázat alternatívája, külön sor); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér, a B szabály a v3-ban nem változott: modell-ingadozás |
| C (F3V3) | 2Móz 20:25 | tobblet | 14 mint | 18 הָ H9034 [it] | megszunt | F3V2:c | — | — | — | nincs | mint fent (a mint token) |
| C (F3V3) | 2Móz 21:26 | tobblet | 9 szemét | 13 וֹ H9023 [his] | megszunt | F3V2:c | — | — | — | K4 (DT21 e) | a -וֹ már nem a szemét-en: a D szabály v3-as pontosítása (DT21 e) pontosan ezt a birtokláncot írja le (nem a közelebbi, hanem a megfelelő személyragú szó); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | 2Móz 26:13 | tobblet | 9 abból | 12 עֹדֵ֔ף H5736 [surplus] | megszunt | F3V2:c | — | — | — | nincs | az abból már csak a ba--hoz (11) kötve; a B szabály a v3-ban nem változott; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | megszunt | F3V2:c, F3V2B:c | — | — | — | K4 (DT21 e) | a -י most a fiam-on (a D szabály v3-as pontosítása, DT21 e: a megfelelő személyragú szó); mindkét v2-futásban (c) volt |
| C (F3V3) | Péld 23:19 | tobblet | 4 engem | 4 י H9020 [my] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az engem (Károli betoldása) most betoldas: a C szabály v3-as szűkítése (DT21 b: a megfelelő nélküli tárgyi névmás betoldas, ne kösd más szóhoz); mindkét v2-futásban (c) volt |
| C (F3V3) | Péld 25:24 | hianyzo | 4 tetőnek | 5 גָּ֑ג H1406 [a roof] | megszunt | F3V2:c | — | — | — | nincs | tetőnek ormán: most helyesen (a v2-ben felcserélve); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér, konvenció nem érinti: modell-ingadozás |
| C (F3V3) | Péld 25:24 | hianyzo | 5 ormán | 4 פִּנַּת H6438 [[the] corner of] | megszunt | F3V2:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 25:24 | tobblet | 4 tetőnek | 4 פִּנַּת H6438 [[the] corner of] | megszunt | F3V2:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 25:24 | tobblet | 5 ormán | 5 גָּ֑ג H1406 [a roof] | megszunt | F3V2:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 31:5 | hianyzo | 11 ne | 1 פֶּן H6435 [lest] | megszunt | F3V2B:c | — | — | — | nincs | a második ne most a פֶּן-é; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér, konvenció nem érinti |
| C (F3V3) | Péld 31:5 | tobblet | 11 ne | 6 וִֽ֝ H9002 [and] | megszunt | F3V2B:c | — | — | — | nincs | mint fent |
| C (F3V3) | Zsolt 22:32 | tobblet | 13 ezt | 10 עָשָֽׂה H6213 [he has acted] | megszunt | F3V2:c | — | — | — | K3 (DT21 b) | az ezt (Károli betoldása) most betoldas: a C szabály v3-as szűkítése (DT21 b) az ezt-et kifejezetten megnevezi; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jer 51:3 | hianyzo | 15 ifjainak | 16 אֶל H0413 [<to>] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | az אֶל most az ifjainak-on; mindkét v2-futásban (c) volt, de a v3 egyik változott szabálya sem szól az elöljáróról: modell-ingadozás (vagy a prompt egészének hatása) |
| C (F3V3) | Jer 51:3 | tobblet | 9 a | 8 אֶל H0408 [may not] | megszunt | F3V2B:c | — | — | — | nincs | az a (a ki) már nem az אֶל-en (a C az אֶל-t forditatlan-nak veszi, az a betoldas); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jer 51:3 | tobblet | 10 ki | 8 אֶל H0408 [may not] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | a ki már nem az אֶל-en; helyette az igéhez került (külön sor, (a) K2): a hibás link áthelyeződött, konvenció nem magyarázza; mindkét v2-futásban (c) volt |
| C (F3V3) | Ez 16:57 | tobblet | 6 miképen | 7 עֵ֚ת H6256 [[the] time of] | megszunt | F3V2B:c | — | — | — | nincs | a miképen már nem az עֵת-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Ez 16:57 | tobblet | 7 te | 7 עֵ֚ת H6256 [[the] time of] | megszunt | F3V2:c | — | — | — | nincs | a te már nem az עֵת-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Ez 33:31 | tobblet | 15 mint | 14 י H9020 [my] | megszunt | F3V2:c | — | — | — | nincs | a mint már nem az én népem ragján; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér; a D szabály pontosítása is magyarázhatná, de a -י a népem-hez sem került: konvencióval nem igazolható |
| C (F3V3) | Ez 33:31 | tobblet | 32 pedig | 30 הֵ֣מָּה H1992 [they] | megszunt | F3V2:c | — | — | — | nincs | a pedig már nem a הֵמָּה-n (helyette a 20. ve--n, külön (c) sor): a hibás link áthelyeződött; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 5:34 | tobblet | 3 azt | 3 λέγω G3004 [say] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az azt (azt mondom) most betoldas: a C szabály v3-as szűkítése (DT21 b: a megfelelő nélküli tárgyi névmás nem kötődik az igéhez); mindkét v2-futásban (c) volt |
| C (F3V3) | Mt 6:31 | tobblet | 4 és | 4 λέγοντες· G3004 [saying;] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | az és már nem a λέγοντες-en (betoldas); mindkét v2-futásban (c) volt, de a v3 egyik változott szabálya sem szól erről: modell-ingadozás (vagy a prompt egészének hatása) |
| C (F3V3) | Mt 6:31 | tobblet | 5 ne | 4 λέγοντες· G3004 [saying;] | megszunt | F3V2B:c | — | — | — | nincs | a ne már nem a λέγοντες-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 11:18 | tobblet | 4 a | 4 μήτε G3383 [neither] | megszunt | F3V2B:c | — | — | — | nincs | a ki vonatkozó (a) most betoldas, nem a μήτε-n; a B szabály a v3-ban nem változott; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 11:18 | tobblet | 5 ki | 4 μήτε G3383 [neither] | megszunt | F3V2B:c | — | — | — | nincs | mint fent (ki) |
| C (F3V3) | Mt 11:18 | tobblet | 11 azt | 9 λέγουσιν· G3004 [they say;] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az azt (azt mondják) most betoldas: a C szabály v3-as szűkítése (DT21 b); mindkét v2-futásban (c) volt |
| C (F3V3) | Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | megszunt | F3V2B:c | változott | — | — | K11 (DT21 c) | az arany v3-ban az azért betoldas (K11, az arany v2 -> v3 változása); az F3V3 is betoldas-nak veszi (az L szabály szerint): a v2-es „hiányzó” link az arany változásával tárgytalan; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 21:4 | tobblet | 3 azért | 4 γέγονεν G1096 [has come to pass] | megszunt | F3V2B:c | változott | — | — | K11 (DT21 c) | az azért már nem a γέγονεν-en, hanem betoldas: az L szabály (DT21 c) szerint; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 21:4 | tobblet | 13 szólott | 9 διὰ G1223 [through] | megszunt | F3V2B:c | — | — | — | nincs | a szólott már nem a διά-n; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 27:18 | tobblet | 2 jól | 1 ᾔδει G1492 [He knew] | megszunt | F3V2:c | — | — | — | K7 (DT21 a) | a jól (határozószó) már nem az ᾔδει-n: a G szabály v3-as szűkítése (DT21 a: a kivétel nem terjed ki a határozószóra); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mk 2:23 | tobblet | 3 hogy | 2 ἐγένετο G1096 [it came to pass] | megszunt | F3V2:c | — | — | — | K7 (DT21 a) | a hogy (lőn, hogy) már nem az ἐγένετο-n: a G szabály v3-as szűkítése (DT21 a: a kivétel nem terjed ki a kötőszóra); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jak 1:18 | hianyzo | 2 ő | 1 βουληθεὶς G1014 [Having willed [it]] | megszunt | F3V2B:c | — | — | — | nincs | az ő akarata most a βουληθείς-hez (a 6. táblázat szerint); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér; konvenció nem igazolja |
| C (F3V3) | Jak 1:18 | tobblet | 2 ő | 13 αὐτοῦ G0846 [of His] | megszunt | F3V2B:c | — | — | — | nincs | mint fent |
| C (F3V3) | Jak 3:1 | tobblet | 7 azt | 8 ὅτι G3754 [that] | megszunt | F3V2:c | — | — | — | K11 (DT21 c) | tudván azt, hogy: az azt most betoldas, a hogy a ὅτι-n: az L szabály (DT21 c) pontosan ezt írja elő; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jak 3:4 | hianyzo | 15 kormánytól | 13 ὑπὸ G5259 [by] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | az ὑπό most a kormánytól-on; mindkét v2-futásban (c) volt, de a v3 egyik változott szabálya sem szól erről: modell-ingadozás (vagy a prompt egészének hatása) |
| C (F3V3) | Jak 3:4 | hianyzo | 19 hová | 17 ἂν G0302 [ever] | megszunt | F3V2:c | — | — | — | nincs | az ἄν most a hová-n is; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jak 3:4 | tobblet | 12 mindazáltal | 13 ὑπὸ G5259 [by] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | a mindazáltal már nem az ὑπό-n (helyette a μετάγεται-n, külön (c) sor): a hibás link áthelyeződött; mindkét v2-futásban (c) volt |
| C (F3V3) | 1Pét 4:11 | tobblet | 22 dícsőíttessék | 27 ἐστιν G1510 [be] | megszunt | F3V2B:c | — | — | — | nincs | az ἐστιν már nem a dícsőíttessék-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | 1Ján 1:10 | tobblet | 2 azt | 3 ὅτι G3754 [that] | megszunt | F3V2:c | — | — | — | K11 (DT21 c) | azt mondjuk, hogy: az azt most betoldas, a hogy a ὅτι-n: az L szabály (DT21 c); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |

## Minden átsorolt v2 (c) eset (az F3V3-nál is eltérés, de a/b)

| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C (F3V3) | 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | elteres | F3V2:c | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | K4 (DT21 e) | a v2-ben (c): a -וֹ a szemét-en (rossz szó). Az F3V3 a ragot már nem a szemét-hez köti (a D szabály v3-as pontosítása, DT21 e: birtokláncban a megfelelő személyragú szó, a prompt példája éppen ez a szerkezet), de a szolgálójának-hoz sem, hanem forditatlan-nak veszi: a hibás link megszűnt, a maradék a K4 alkalmazásának hiánya (a); részleges javulás |

## Minden maradt (c) eset

| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C (F3V3) | Péld 31:8 | hianyzo | 13 dolgában | 6 אֶל H0413 [to] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az אֶל a dolgában ragja; a C továbbra is az és-hez köti; konvenció nem érinti (maradt) |
| C (F3V3) | Péld 31:8 | tobblet | 11 és | 6 אֶל H0413 [to] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az és (6. táblázat: betoldas) nem az אֶל („ügyében”); maradt |
| C (F3V3) | Jer 46:21 | hianyzo | 3 is | 1 גַּם H1571 [also] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | Még ... is = גַּם (1); a C az első is-t továbbra is a második גַם-hoz köti (maradt) |
| C (F3V3) | Jer 46:21 | tobblet | 3 is | 11 גַם H1571 [also] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az első is a második גַם-on (maradt) |
| C (F3V3) | Ez 11:3 | tobblet | 9 város | 10 סִּ֔יר H5518 [pot] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a város továbbra is a „fazék”-hoz (סִיר) kötve (maradt; a 6. táblázat a város döntését felsorolja, de ez nem az alternatívája) |
| C (F3V3) | Ez 33:31 | tobblet | 32 pedig | 20 וְ H9002 [and] | elteres | F3V2B:c | — | c | — | nincs | a pedig nem a 20. ve- (az a de-é); maradt az F3V2B-ből |
| C (F3V3) | Ez 46:12 | tobblet | 39 azután | 40 יָצָ֛א H3318 [he will go out] | elteres | F3V2B:c | — | c | — | nincs | az azután Károli betoldása; a „kimegy” igéhez kötve (maradt az F3V2B-ből; az F3V2-ben a ve--hez került) |
| C (F3V3) | Mt 6:31 | hianyzo | 5 ne | 1 μὴ G3361 [Not] | elteres | F3V2B:c | — | c | — | nincs | a második ne a μή-é (az arany szerint); a C betoldas-nak veszi; maradt az F3V2B-ből [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | Mt 21:4 | hianyzo | 8 próféta | 9 διὰ G1223 [through] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a διά továbbra sincs a próféta-n (maradt) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | Jak 3:4 | tobblet | 16 oda | 17 ἂν G0302 [ever] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az ἄν továbbra is az oda-n (a hová-é); maradt |
| C (F3V3) | 1Pét 4:11 | hianyzo | 14 erővel | 11 ἐξ G1537 [of] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az ἐκ továbbra is az azzal-on, nem az erővel-en (maradt) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | 1Pét 4:11 | tobblet | 7 szólja | 3 λαλεῖ G2980 [speaks] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a szólja (a jegyzet 5. szakasza szerint Károli-kiegészítés, betoldas) továbbra is a λαλεῖ-hez kötve (maradt) |
| C (F3V3) | 1Pét 4:11 | tobblet | 12 azzal | 11 ἐξ G1537 [of] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | mint az erővel sor (az ἐκ az azzal-on); maradt |
| C (F3V3) | 1Pét 4:11 | tobblet | 15 szolgáljon | 9 διακονεῖ G1247 [serves] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a szolgáljon (5. szakasz: betoldas) továbbra is a διακονεῖ-hez kötve (maradt) |
| C (F3V3) | 1Pét 4:11 | tobblet | 22 dícsőíttessék | 22 θεὸς G2316 [God] | elteres | F3V2:c | — | c | — | nincs | a θεός (Károlinál nem fordított, 5. szakasz) továbbra is a dícsőíttessék-hez kötve (maradt) |

## 6. Minden sor (gépi állapot, kézi besorolás)

| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C (F3V3) | 2Móz 20:23 | hianyzo | 4 mellém | 5 י H9030 [me] | elteres | F3V2:a, F3V2B:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | a -י rag csak az én-hez kötve, a mellém-hez nem (a K4 szerint a külön névmás és a ragot viselő szó is kapja); mint az F3V2/F3V2B |
| C (F3V3) | 2Móz 20:25 | tobblet | 13 a | 18 הָ H9034 [it] | megszunt | F3V2:c | — | — | — | nincs | az a mint már nem a rávetetted tárgyragján (-hā); az F3V3 a mint-et a כִּי-hez köti (a 6. táblázat alternatívája, külön sor); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér, a B szabály a v3-ban nem változott: modell-ingadozás |
| C (F3V3) | 2Móz 20:25 | tobblet | 14 mint | 13 כִּ֧י H3588 [for] | elteres | F3V2B:b | — | b | 6. szakasz táblázat: 2Móz 20:25 | — | a mint -> כִּי: a jegyzet alternatívája (mint az F3V2B-nél) |
| C (F3V3) | 2Móz 20:25 | tobblet | 14 mint | 18 הָ H9034 [it] | megszunt | F3V2:c | — | — | — | nincs | mint fent (a mint token) |
| C (F3V3) | 2Móz 20:25 | tobblet | 18 megfertőztetted | 19 וַ H9001 [and] | elteres | F3V2:a, F3V2B:a | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a le nem fordított vav-konszekutívum az igéhez kötve (az I szabály szerint forditatlan); mint a v2-ben |
| C (F3V3) | 2Móz 21:6 | hianyzo | 6 ura | 5 ו֙ H9023 [his] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő ura: a rag csak az ő-höz, a birtokszóhoz nem; mint a v2-ben |
| C (F3V3) | 2Móz 21:6 | hianyzo | 20 ura | 22 ו H9023 [his] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő ura: mint fent |
| C (F3V3) | 2Móz 21:6 | hianyzo | 25 fülét | 25 וֹ֙ H9023 [his] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő fülét: mint fent |
| C (F3V3) | 2Móz 21:26 | hianyzo | 5 szolgájának | 8 וֹ H9023 [his] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő szolgájának: a rag csak az ő-höz; mint a v2-ben |
| C (F3V3) | 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | elteres | F3V2:c | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | K4 (DT21 e) | a v2-ben (c): a -וֹ a szemét-en (rossz szó). Az F3V3 a ragot már nem a szemét-hez köti (a D szabály v3-as pontosítása, DT21 e: birtokláncban a megfelelő személyragú szó, a prompt példája éppen ez a szerkezet), de a szolgálójának-hoz sem, hanem forditatlan-nak veszi: a hibás link megszűnt, a maradék a K4 alkalmazásának hiánya (a); részleges javulás |
| C (F3V3) | 2Móz 21:26 | hianyzo | 14 elpusztul | 16 הּ H9034 [it] | elteres | — | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D); tárgyrag az igén: DT20 a), nyitott (8.3/4) | — | a tárgyi rag (-hā „azt”) az elpusztul igén; a C forditatlan-nak veszi (vö. Péld 30:17, v2: a) |
| C (F3V3) | 2Móz 21:26 | hianyzo | 20 szeméért | 23 וֹ H9023 [his] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő szeméért: a rag csak az ő-höz; mint a v2-ben |
| C (F3V3) | 2Móz 21:26 | tobblet | 9 szemét | 13 וֹ H9023 [his] | megszunt | F3V2:c | — | — | — | K4 (DT21 e) | a -וֹ már nem a szemét-en: a D szabály v3-as pontosítása (DT21 e) pontosan ezt a birtokláncot írja le (nem a közelebbi, hanem a megfelelő személyragú szó); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | 2Móz 25:8 | hianyzo | 8 közöttök | 10 ם H9028 [them] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | a -ām rag csak az ő-höz, a közöttök-höz nem; mint a v2-ben |
| C (F3V3) | 2Móz 25:40 | hianyzo | 2 hogy | 3 וַ H9002 [and] | elteres | — | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a hogy a második ve- (3) helyén áll; a C az első ve--hez (1) köti, a 3-at az igéhez: melyik ve- a „fordított” — a Strong azonos (H9002) |
| C (F3V3) | 2Móz 25:40 | hianyzo | 3 arra | 7 ם H9028 [their] | elteres | F3V2B:b | — | b | 6. szakasz táblázat: 2Móz 25:40; jegyzet v2 8.3/3 | — | a -ām a formára-n (mint a v2-ben); a 8.3/3 szerint a K4 v2-vel egyik magyar szó sem visel megfelelő személyragot |
| C (F3V3) | 2Móz 25:40 | hianyzo | 5 formára | 5 בְּ H9003 [in] | elteres | F3V2:b, F3V2B:b | — | b | 6. szakasz táblázat: 2Móz 25:40 | — | a be- az arra-n (a -ra rag mindkét szón); mint a v2-ben |
| C (F3V3) | 2Móz 25:40 | hianyzo | 12 néked | 9 אַתָּ֥ה H0859 [you] | elteres | — | — | c | — | nincs | új: a néked az אַתָּה egyetlen magyar megfelelője (Károli részes esettel adja); a C betoldas-nak veszi, az אַתָּה-t a 3. személyű mutattatott-hoz köti: nem védhető. A C szabály (K3 v2) túláltalánosítása (névmás -> betoldas) nem zárható ki, de a szabály a tárgyi névmásról szól, a néked nem az: konvencióval nem magyarázható |
| C (F3V3) | 2Móz 25:40 | tobblet | 2 hogy | 1 וּ H9002 [and] | elteres | — | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a hogy az első ve--hez (1) kötve; l. a hianyzo sort |
| C (F3V3) | 2Móz 25:40 | tobblet | 3 arra | 5 בְּ H9003 [in] | elteres | F3V2:b, F3V2B:b | — | b | 6. szakasz táblázat: 2Móz 25:40 | — | a be- az arra-n (l. fent) |
| C (F3V3) | 2Móz 25:40 | tobblet | 5 formára | 7 ם H9028 [their] | elteres | F3V2B:b | — | b | 6. szakasz táblázat: 2Móz 25:40; jegyzet v2 8.3/3 | — | a -ām a formára-n (l. fent) |
| C (F3V3) | 2Móz 25:40 | tobblet | 6 csináld | 3 וַ H9002 [and] | elteres | — | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a második ve- (3) az igén (csináld); az I szabály szerint a hogy-é |
| C (F3V3) | 2Móz 25:40 | tobblet | 11 mutattatott | 9 אַתָּ֥ה H0859 [you] | elteres | — | — | c | — | nincs | új: az אַתָּה a mutattatott-hoz kötve; l. a néked sort |
| C (F3V3) | 2Móz 26:13 | tobblet | 9 abból | 12 עֹדֵ֔ף H5736 [surplus] | megszunt | F3V2:c | — | — | — | nincs | az abból már csak a ba--hoz (11) kötve; a B szabály a v3-ban nem változott; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | 2Móz 26:13 | tobblet | 11 mi | 12 עֹדֵ֔ף H5736 [surplus] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a mi az igenévhez kötve (a K2 listájában megnevezett opció); mint a v2-ben |
| C (F3V3) | 2Móz 29:4 | hianyzo | 6 fiait | 7 ו֙ H9023 [his] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő fiait: a rag csak az ő-höz; mint a v2-ben |
| C (F3V3) | 2Móz 30:3 | hianyzo | 17 is | 19 וְ H9001 [and] | elteres | — | — | b | 6. szakasz táblázat: 2Móz 30:3 | — | az arany: is -> ve- (19); a C az is-t betoldas-nak, a ve--t az igéhez köti; nem pontosan a jegyzet alternatívája (is betoldas, 19 forditatlan); az F3 (v1) besorolásával azonos |
| C (F3V3) | 2Móz 30:3 | tobblet | 18 csinálj | 19 וְ H9001 [and] | elteres | — | — | b | 6. szakasz táblázat: 2Móz 30:3 | — | a ve- a csinálj-on (l. fent) |
| C (F3V3) | Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | megszunt | F3V2:c, F3V2B:c | — | — | — | K4 (DT21 e) | a -י most a fiam-on (a D szabály v3-as pontosítása, DT21 e: a megfelelő személyragú szó); mindkét v2-futásban (c) volt |
| C (F3V3) | Péld 23:19 | hianyzo | 5 hogy | 5 וַ H9002 [and] | elteres | F3V2:a, F3V2B:a | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a וַ az arany szerint a hogy-hoz; a C forditatlan-nak, a hogy-ot betoldas-nak veszi; mint a v2-ben |
| C (F3V3) | Péld 23:19 | hianyzo | 11 úton | 9 בַּ H9003 [in the] | elteres | F3V2:a, F3V2B:a | — | a | K10 összeolvadt névelő + elöljáró (2. szakasz 10.; prompt J) | — | ez úton: a בַּ csak az ez-hez; mint a v2-ben |
| C (F3V3) | Péld 23:19 | tobblet | 4 engem | 4 י H9020 [my] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az engem (Károli betoldása) most betoldas: a C szabály v3-as szűkítése (DT21 b: a megfelelő nélküli tárgyi névmás betoldas, ne kösd más szóhoz); mindkét v2-futásban (c) volt |
| C (F3V3) | Péld 25:24 | hianyzo | 4 tetőnek | 5 גָּ֑ג H1406 [a roof] | megszunt | F3V2:c | — | — | — | nincs | tetőnek ormán: most helyesen (a v2-ben felcserélve); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér, konvenció nem érinti: modell-ingadozás |
| C (F3V3) | Péld 25:24 | hianyzo | 5 ormán | 4 פִּנַּת H6438 [[the] corner of] | megszunt | F3V2:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 25:24 | tobblet | 4 tetőnek | 4 פִּנַּת H6438 [[the] corner of] | megszunt | F3V2:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 25:24 | tobblet | 5 ormán | 5 גָּ֑ג H1406 [a roof] | megszunt | F3V2:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 28:17 | hianyzo | 11 senki | 10 יִתְמְכוּ H8551 [people support] | elteres | — | — | b | 6. szakasz táblázat: Péld 28:17 | — | az arany: senki -> 9, 10 (6. táblázat); a C csak a tagadóhoz (9) köti; az F3 (v1) besorolásával azonos |
| C (F3V3) | Péld 28:17 | tobblet | 6 vér | 3 בְּ H9003 [by] | elteres | F3V2B:b | — | b | 6. szakasz táblázat: Péld 28:17 | — | vér -> 3, 4: a jegyzet alternatívája |
| C (F3V3) | Péld 30:17 | hianyzo | 13 kivágják | 11 הָ H9034 [it] | elteres | F3V2B:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D); tárgyrag az igén: DT20 a), nyitott (8.3/4) | — | a tárgyi rag az igén nincs kötve (forditatlan); mint a v2-ben |
| C (F3V3) | Péld 30:17 | hianyzo | 18 megeszik | 16 הָ H9034 [it] | elteres | F3V2B:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D); tárgyrag az igén: DT20 a), nyitott (8.3/4) | — | mint a 13. szónál |
| C (F3V3) | Péld 31:5 | hianyzo | 11 ne | 1 פֶּן H6435 [lest] | megszunt | F3V2B:c | — | — | — | nincs | a második ne most a פֶּן-é; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér, konvenció nem érinti |
| C (F3V3) | Péld 31:5 | tobblet | 11 ne | 6 וִֽ֝ H9002 [and] | megszunt | F3V2B:c | — | — | — | nincs | mint fent |
| C (F3V3) | Péld 31:8 | hianyzo | 13 dolgában | 6 אֶל H0413 [to] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az אֶל a dolgában ragja; a C továbbra is az és-hez köti; konvenció nem érinti (maradt) |
| C (F3V3) | Péld 31:8 | tobblet | 11 és | 6 אֶל H0413 [to] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az és (6. táblázat: betoldas) nem az אֶל („ügyében”); maradt |
| C (F3V3) | Jób 33:13 | tobblet | 4 Azért | 5 כִּ֥י H3588 [that] | elteres | — | változott | a | K11 korrelatív mutató névmás a hogy előtt (8.1; prompt L) | — | az arany v3-ban az Azért betoldas (K11); a C az Azért-et a כִּי-hez is köti (a hogy mellett): az L szabály itt nem érvényesült. Az eltérést az arany v2 -> v3 változása hozta létre (az arany v2 így párosított) |
| C (F3V3) | Zsolt 16:11 | tobblet | 1 Te | 1 תּֽוֹדִיעֵ H3045 [you will make known to] | elteres | F3V2:a | — | a | K6 külön kitett alanyi névmás (2. szakasz 6.; prompt F) | — | a külön kitett Te az igéhez kötve; mint a v2-ben |
| C (F3V3) | Zsolt 18:1 | tobblet | 14 azon | 18 בְּ H9003 [on] | elteres | F3V2:b, F3V2B:b | — | b | 6. szakasz táblázat: Zsolt 18:1 | — | azon -> 18: a jegyzet alternatívája; mint a v2-ben |
| C (F3V3) | Zsolt 18:1 | tobblet | 19 melyen | 18 בְּ H9003 [on] | elteres | — | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a melyen (a K2 listájában betoldas) a C-nél a בְּ-hez is kötve (a -en rag miatt); a vonatkozó szó kezelése |
| C (F3V3) | Zsolt 18:3 | tobblet | 7 és | 4 וּ H9002 [and] | elteres | F3V2:a | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a magyarban egy és van; a C mindkét וּ-t (4, 7) hozzáköti; mint az F3V2 |
| C (F3V3) | Zsolt 22:32 | tobblet | 8 ő | 8 נ֝וֹלָ֗ד H3205 [about to be born] | elteres | F3V2:b | — | b | 6. szakasz táblázat: Zsolt 22:32 | — | az arany: ő (8) betoldas; a C a נוֹלָד-hoz köti; mint az F3V2 |
| C (F3V3) | Zsolt 22:32 | tobblet | 13 ezt | 10 עָשָֽׂה H6213 [he has acted] | megszunt | F3V2:c | — | — | — | K3 (DT21 b) | az ezt (Károli betoldása) most betoldas: a C szabály v3-as szűkítése (DT21 b) az ezt-et kifejezetten megnevezi; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jer 46:21 | hianyzo | 3 is | 1 גַּם H1571 [also] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | Még ... is = גַּם (1); a C az első is-t továbbra is a második גַם-hoz köti (maradt) |
| C (F3V3) | Jer 46:21 | hianyzo | 6 közöttök | 6 הּ֙ H9024 [its] | elteres | F3V2:a, F3V2B:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | ő közöttök: a rag csak az ő-höz; mint a v2-ben |
| C (F3V3) | Jer 46:21 | hianyzo | 27 megfenyíttetésök | 27 ם H9028 [their] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő megfenyíttetésök: a rag csak az ő-höz; mint a v2-ben |
| C (F3V3) | Jer 46:21 | tobblet | 3 is | 11 גַם H1571 [also] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az első is a második גַם-on (maradt) |
| C (F3V3) | Jer 51:3 | hianyzo | 2 kézívesre | 1 אֶֽל H0408 [may not] | elteres | — | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | — | a C mindkét אֶל-t (1, 8) forditatlan-nak veszi (a TAHOT „ne” címkéje szerint); a jegyzet 3. szakasza maga is felkínálja (c) opcióként: az arany döntése vitatható |
| C (F3V3) | Jer 51:3 | hianyzo | 8 arra | 8 אֶל H0408 [may not] | elteres | — | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | — | mint fent (az arra és a második אֶל) |
| C (F3V3) | Jer 51:3 | hianyzo | 11 pánczéljába | 10 בְּ H9003 [in] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): a be- a pánczéljába -ba ragja; a C az arra-hoz köti; konvenció nem érinti (az elöljáró kezelése a v3-ban nem változott): modell-ingadozás |
| C (F3V3) | Jer 51:3 | hianyzo | 15 ifjainak | 16 אֶל H0413 [<to>] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | az אֶל most az ifjainak-on; mindkét v2-futásban (c) volt, de a v3 egyik változott szabálya sem szól az elöljáróról: modell-ingadozás (vagy a prompt egészének hatása) |
| C (F3V3) | Jer 51:3 | tobblet | 2 kézívesre | 2 יִדְרֹ֤ךְ H1869 [he bend] | elteres | F3V2B:b | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | — | a kézívesre a Ketiv kettőzött igéjével (F21.12: b) |
| C (F3V3) | Jer 51:3 | tobblet | 2 kézívesre | 3 הַ H9009 [the] | elteres | F3V2B:a | — | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelő (הַ) a kézívesre-n |
| C (F3V3) | Jer 51:3 | tobblet | 2 kézívesre | 4 דֹּרֵךְ֙ H1869 [[one] bending] | elteres | F3V2:b, F3V2B:b | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | — | a kézívesre a „hajlító” (דֹּרֵךְ) részeként (a Ketiv-olvasat; F21.12: b) |
| C (F3V3) | Jer 51:3 | tobblet | 3 kézíves | 2 יִדְרֹ֤ךְ H1869 [he bend] | elteres | — | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | — | a kettőzött יִדְרֹךְ a kézíves-hez is kötve (a Ketiv-olvasat egyik lehetséges felosztása) |
| C (F3V3) | Jer 51:3 | tobblet | 8 arra | 9 יִתְעַ֖ל H5927 [he lift] | elteres | — | — | c | — | nincs | új: az arra („felé”, a második אֶל) a C-nél az „emeli” (יִתְעַל) igéhez kötve, miután az אֶל-t forditatlan-nak vette: nem védhető; konvenció nem érinti |
| C (F3V3) | Jer 51:3 | tobblet | 8 arra | 10 בְּ H9003 [in] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete): az arra nem a be- elöljáró |
| C (F3V3) | Jer 51:3 | tobblet | 9 a | 8 אֶל H0408 [may not] | megszunt | F3V2B:c | — | — | — | nincs | az a (a ki) már nem az אֶל-en (a C az אֶל-t forditatlan-nak veszi, az a betoldas); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jer 51:3 | tobblet | 10 ki | 8 אֶל H0408 [may not] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | a ki már nem az אֶל-en; helyette az igéhez került (külön sor, (a) K2): a hibás link áthelyeződött, konvenció nem magyarázza; mindkét v2-futásban (c) volt |
| C (F3V3) | Jer 51:3 | tobblet | 10 ki | 9 יִתְעַ֖ל H5927 [he lift] | elteres | — | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a vonatkozó ki a mellékmondat igéjéhez (יִתְעַל) kötve; a K2 szerint betoldas (az igenév-opció itt nem áll, az ige finit): a vonatkozó szó kezelése |
| C (F3V3) | Ez 11:3 | tobblet | 9 város | 10 סִּ֔יר H5518 [pot] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a város továbbra is a „fazék”-hoz (סִיר) kötve (maradt; a 6. táblázat a város döntését felsorolja, de ez nem az alternatívája) |
| C (F3V3) | Ez 16:57 | tobblet | 6 miképen | 7 עֵ֚ת H6256 [[the] time of] | megszunt | F3V2B:c | — | — | — | nincs | a miképen már nem az עֵת-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Ez 16:57 | tobblet | 7 te | 7 עֵ֚ת H6256 [[the] time of] | megszunt | F3V2:c | — | — | — | nincs | a te már nem az עֵת-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Ez 22:25 | hianyzo | 4 prófétái | 3 הָ֙ H9024 [its] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő prófétái: a rag csak az ő-höz; mint a v2-ben |
| C (F3V3) | Ez 22:25 | hianyzo | 6 közepette | 6 הּ H9024 [it] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | ő közepette: mint fent |
| C (F3V3) | Ez 22:25 | hianyzo | 7 olyanok | 7 כַּ H9004 [like] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): olyanok ... mint = כַּ; a C az olyanok-at betoldas-nak veszi. Határeset: az arany döntése is vitatható, a jegyzetben nem szerepel; az L szabály (korrelatívum) túláltalánosítása nem zárható ki, de az L csak az azt/azért … hogy szerkezetről szól |
| C (F3V3) | Ez 33:31 | hianyzo | 18 népem | 14 י H9020 [my] | elteres | F3V2:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az én népem: a rag csak az én-hez; mint a v2-ben |
| C (F3V3) | Ez 33:31 | tobblet | 9 szokott | 6 מְבוֹא H3996 [[the] coming of] | elteres | F3V2:b, F3V2B:b | — | b | 6. szakasz táblázat: Ez 33:31 | — | szokott -> מְבוֹא; mint a v2-ben |
| C (F3V3) | Ez 33:31 | tobblet | 15 mint | 5 כִּ H9004 [like] | elteres | F3V2B:b | — | b | 6. szakasz táblázat: Ez 33:31 | — | a mint -> כְּ (mint az F3V2B-nél); védhető |
| C (F3V3) | Ez 33:31 | tobblet | 15 mint | 14 י H9020 [my] | megszunt | F3V2:c | — | — | — | nincs | a mint már nem az én népem ragján; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér; a D szabály pontosítása is magyarázhatná, de a -י a népem-hez sem került: konvencióval nem igazolható |
| C (F3V3) | Ez 33:31 | tobblet | 32 pedig | 20 וְ H9002 [and] | elteres | F3V2B:c | — | c | — | nincs | a pedig nem a 20. ve- (az a de-é); maradt az F3V2B-ből |
| C (F3V3) | Ez 33:31 | tobblet | 32 pedig | 30 הֵ֣מָּה H1992 [they] | megszunt | F3V2:c | — | — | — | nincs | a pedig már nem a הֵמָּה-n (helyette a 20. ve--n, külön (c) sor): a hibás link áthelyeződött; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Ez 33:31 | tobblet | 33 nyereség | 34 ם H9028 [their] | elteres | F3V2:b | — | b | 6. szakasz táblázat: Ez 33:31 | — | a nyereség ragja kötve (az arany: forditatlan); mint az F3V2 |
| C (F3V3) | Ez 39:13 | tobblet | 15 melyen | 13 י֚וֹם H3117 [[the] day of] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a melyen vonatkozó a יוֹם-hoz kötve (az arany: betoldas); mint a v2-ben |
| C (F3V3) | Ez 46:12 | tobblet | 39 azután | 40 יָצָ֛א H3318 [he will go out] | elteres | F3V2B:c | — | c | — | nincs | az azután Károli betoldása; a „kimegy” igéhez kötve (maradt az F3V2B-ből; az F3V2-ben a ve--hez került) |
| C (F3V3) | Mt 4:4 | tobblet | 16 a | 17 ἐκπορευομένῳ G1607 [coming out] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a mely: a C mindkét tokent (a, mely) az igenévhez köti (a K2 opciója); mint a v2-ben |
| C (F3V3) | Mt 4:4 | tobblet | 17 mely | 17 ἐκπορευομένῳ G1607 [coming out] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | mint fent |
| C (F3V3) | Mt 5:34 | hianyzo | 13 az | 14 ἐστὶν G1510 [it is] | elteres | — | — | b | 6. szakasz táblázat: Mt 5:34 | — | az arany: az (13) -> ἐστὶν; a C a jegyzet alternatíváját választja (az betoldas) |
| C (F3V3) | Mt 5:34 | tobblet | 3 azt | 3 λέγω G3004 [say] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az azt (azt mondom) most betoldas: a C szabály v3-as szűkítése (DT21 b: a megfelelő nélküli tárgyi névmás nem kötődik az igéhez); mindkét v2-futásban (c) volt |
| C (F3V3) | Mt 5:34 | tobblet | 17 széke | 14 ἐστὶν G1510 [it is] | elteres | — | — | b | 6. szakasz táblázat: Mt 5:34 | — | a ki nem mondott létige (ἐστίν) a C-nél a széke (az állítmányi névszó) szóhoz kötve; a 6. táblázat ennek a versnek az ἐστίν-kezelését bizonytalan döntésként sorolja |
| C (F3V3) | Mt 6:31 | hianyzo | 5 ne | 1 μὴ G3361 [Not] | elteres | F3V2B:c | — | c | — | nincs | a második ne a μή-é (az arany szerint); a C betoldas-nak veszi; maradt az F3V2B-ből [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | Mt 6:31 | tobblet | 4 és | 4 λέγοντες· G3004 [saying;] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | az és már nem a λέγοντες-en (betoldas); mindkét v2-futásban (c) volt, de a v3 egyik változott szabálya sem szól erről: modell-ingadozás (vagy a prompt egészének hatása) |
| C (F3V3) | Mt 6:31 | tobblet | 5 ne | 4 λέγοντες· G3004 [saying;] | megszunt | F3V2B:c | — | — | — | nincs | a ne már nem a λέγοντες-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 11:18 | tobblet | 4 a | 4 μήτε G3383 [neither] | megszunt | F3V2B:c | — | — | — | nincs | a ki vonatkozó (a) most betoldas, nem a μήτε-n; a B szabály a v3-ban nem változott; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 11:18 | tobblet | 5 ki | 4 μήτε G3383 [neither] | megszunt | F3V2B:c | — | — | — | nincs | mint fent (ki) |
| C (F3V3) | Mt 11:18 | tobblet | 11 azt | 9 λέγουσιν· G3004 [they say;] | megszunt | F3V2:c, F3V2B:c | — | — | — | K3 (DT21 b) | az azt (azt mondják) most betoldas: a C szabály v3-as szűkítése (DT21 b); mindkét v2-futásban (c) volt |
| C (F3V3) | Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | megszunt | F3V2B:c | változott | — | — | K11 (DT21 c) | az arany v3-ban az azért betoldas (K11, az arany v2 -> v3 változása); az F3V3 is betoldas-nak veszi (az L szabály szerint): a v2-es „hiányzó” link az arany változásával tárgytalan; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 21:4 | hianyzo | 8 próféta | 9 διὰ G1223 [through] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a διά továbbra sincs a próféta-n (maradt) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | Mt 21:4 | tobblet | 3 azért | 4 γέγονεν G1096 [has come to pass] | megszunt | F3V2B:c | változott | — | — | K11 (DT21 c) | az azért már nem a γέγονεν-en, hanem betoldas: az L szabály (DT21 c) szerint; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 21:4 | tobblet | 9 mondása | 9 διὰ G1223 [through] | elteres | — | — | c | — | nincs | új: a διά a mondása-n (az arany: a próféta-n); ugyanannak a v2-es (c) esetnek (a διά helye) új alakja [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | Mt 21:4 | tobblet | 10 a | 12 λέγοντος· G3004 [saying;] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a ki: az igenévhez (λέγοντος) kötve — a K2 listájában megnevezett opció; mint a v2-ben |
| C (F3V3) | Mt 21:4 | tobblet | 11 ki | 12 λέγοντος· G3004 [saying;] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | mint fent |
| C (F3V3) | Mt 21:4 | tobblet | 13 szólott | 9 διὰ G1223 [through] | megszunt | F3V2B:c | — | — | — | nincs | a szólott már nem a διά-n; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mt 23:31 | hianyzo | 2 hát | 1 ὥστε G5620 [Thus] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): Így hát = ὥστε; a C a hát-ot betoldas-nak veszi. Határeset [az arany döntése is vitatható; a jegyzetben nem szerepel]; konvenció nem érinti |
| C (F3V3) | Mt 27:18 | tobblet | 2 jól | 1 ᾔδει G1492 [He knew] | megszunt | F3V2:c | — | — | — | K7 (DT21 a) | a jól (határozószó) már nem az ᾔδει-n: a G szabály v3-as szűkítése (DT21 a: a kivétel nem terjed ki a határozószóra); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mk 2:23 | hianyzo | 14 tanítványai | 14 αὐτοῦ G0846 [of Him] | elteres | — | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő tanítványai: az αὐτοῦ csak az ő-höz (az F3 v1-gyel azonos) |
| C (F3V3) | Mk 2:23 | tobblet | 3 hogy | 2 ἐγένετο G1096 [it came to pass] | megszunt | F3V2:c | — | — | — | K7 (DT21 a) | a hogy (lőn, hogy) már nem az ἐγένετο-n: a G szabály v3-as szűkítése (DT21 a: a kivétel nem terjed ki a kötőszóra); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Mk 2:23 | tobblet | 6 vetések | 8 διὰ G1223 [through] | elteres | — | — | a | K10 összeolvadt névelő + elöljáró (2. szakasz 10.; prompt J) | — | vetések közt: a διά a közt mellett a vetések-hez is kötve (a J szabály második fele: az elöljáró a főnévhez is kötődhet) |
| C (F3V3) | Jak 1:18 | hianyzo | 2 ő | 1 βουληθεὶς G1014 [Having willed [it]] | megszunt | F3V2B:c | — | — | — | nincs | az ő akarata most a βουληθείς-hez (a 6. táblázat szerint); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér; konvenció nem igazolja |
| C (F3V3) | Jak 1:18 | hianyzo | 13 teremtményeinek | 13 αὐτοῦ G0846 [of His] | elteres | F3V2:a, F3V2B:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő teremtményeinek: az αὐτοῦ csak az ő-höz; mint a v2-ben |
| C (F3V3) | Jak 1:18 | tobblet | 2 ő | 13 αὐτοῦ G0846 [of His] | megszunt | F3V2B:c | — | — | — | nincs | mint fent |
| C (F3V3) | Jak 1:18 | tobblet | 10 hogy | 8 εἶναι G1511 [to be] | elteres | — | — | b | 6. szakasz táblázat: 1Pét 5:12 (azonos szerkezet) | — | εἰς τὸ εἶναι: a hogy a C-nél az εἶναι-hoz is kötve; az arany az 1Pét 5:12-ben éppen így párosít (hogy -> εἶναι, 6. táblázat), itt nem: az arany két verse között a döntés nem egységes |
| C (F3V3) | Jak 3:1 | tobblet | 7 azt | 8 ὅτι G3754 [that] | megszunt | F3V2:c | — | — | — | K11 (DT21 c) | tudván azt, hogy: az azt most betoldas, a hogy a ὅτι-n: az L szabály (DT21 c) pontosan ezt írja elő; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jak 3:4 | hianyzo | 15 kormánytól | 13 ὑπὸ G5259 [by] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | az ὑπό most a kormánytól-on; mindkét v2-futásban (c) volt, de a v3 egyik változott szabálya sem szól erről: modell-ingadozás (vagy a prompt egészének hatása) |
| C (F3V3) | Jak 3:4 | hianyzo | 19 hová | 17 ἂν G0302 [ever] | megszunt | F3V2:c | — | — | — | nincs | az ἄν most a hová-n is; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | Jak 3:4 | tobblet | 12 mindazáltal | 12 μετάγεται G3329 [are turned about] | elteres | — | — | c | — | nincs | új a v2-höz képest (az F3 v1 (c) esete, a v2-ben megszűnt): a mindazáltal (Károli betoldása) a μετάγεται-hez kötve, amely a fordíttatnak-é |
| C (F3V3) | Jak 3:4 | tobblet | 12 mindazáltal | 13 ὑπὸ G5259 [by] | megszunt | F3V2:c, F3V2B:c | — | — | — | nincs | a mindazáltal már nem az ὑπό-n (helyette a μετάγεται-n, külön (c) sor): a hibás link áthelyeződött; mindkét v2-futásban (c) volt |
| C (F3V3) | Jak 3:4 | tobblet | 16 oda | 17 ἂν G0302 [ever] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az ἄν továbbra is az oda-n (a hová-é); maradt |
| C (F3V3) | 1Pét 4:2 | tobblet | 1 Hogy | 2 τὸ G3588 [<the>] | elteres | F3V2B:a | — | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelős főnévi igenév névelője (τό) a Hogy-on; mint az F3V2B |
| C (F3V3) | 1Pét 4:11 | hianyzo | 14 erővel | 11 ἐξ G1537 [of] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | az ἐκ továbbra is az azzal-on, nem az erővel-en (maradt) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| C (F3V3) | 1Pét 4:11 | tobblet | 7 szólja | 3 λαλεῖ G2980 [speaks] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a szólja (a jegyzet 5. szakasza szerint Károli-kiegészítés, betoldas) továbbra is a λαλεῖ-hez kötve (maradt) |
| C (F3V3) | 1Pét 4:11 | tobblet | 12 azzal | 11 ἐξ G1537 [of] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | mint az erővel sor (az ἐκ az azzal-on); maradt |
| C (F3V3) | 1Pét 4:11 | tobblet | 15 szolgáljon | 9 διακονεῖ G1247 [serves] | elteres | F3V2:c, F3V2B:c | — | c | — | nincs | a szolgáljon (5. szakasz: betoldas) továbbra is a διακονεῖ-hez kötve (maradt) |
| C (F3V3) | 1Pét 4:11 | tobblet | 22 dícsőíttessék | 22 θεὸς G2316 [God] | elteres | F3V2:c | — | c | — | nincs | a θεός (Károlinál nem fordított, 5. szakasz) továbbra is a dícsőíttessék-hez kötve (maradt) |
| C (F3V3) | 1Pét 4:11 | tobblet | 22 dícsőíttessék | 27 ἐστιν G1510 [be] | megszunt | F3V2B:c | — | — | — | nincs | az ἐστιν már nem a dícsőíttessék-en; csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |
| C (F3V3) | 1Pét 4:11 | tobblet | 33 örökké | 36 τῶν G3588 [of the] | elteres | F3V2:a, F3V2B:a | — | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelő (τῶν) az örökké-hez kötve; mint a v2-ben |
| C (F3V3) | 1Pét 5:12 | tobblet | 9 atyátokfia | 3 ὑμῖν G4771 [to you] | elteres | F3V2B:b | — | b | 6. szakasz táblázat: 1Pét 5:12 | — | ὑμῖν az atyátokfia -tok ragjához; mint az F3V2B |
| C (F3V3) | 1Pét 5:12 | tobblet | 22 a | 21 εἰς G1519 [in] | elteres | F3V2:a, F3V2B:a | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a melyben: az εἰς mindkét tokenhez (a, melyben); mint a v2-ben |
| C (F3V3) | 1Ján 1:10 | hianyzo | 13 ígéje | 12 αὐτοῦ G0846 [of Him] | elteres | F3V2:a, F3V2B:a | — | a | K4 v2 birtokos és névmási ragok (2. szakasz 4., 8.1; prompt D) | — | az ő ígéje: az αὐτοῦ csak az ő-höz; mint a v2-ben |
| C (F3V3) | 1Ján 1:10 | tobblet | 2 azt | 3 ὅτι G3754 [that] | megszunt | F3V2:c | — | — | — | K11 (DT21 c) | azt mondjuk, hogy: az azt most betoldas, a hogy a ὅτι-n: az L szabály (DT21 c); csak az egyik v2-futásban volt (c): a megszűnés az ingadozással is összefér |

