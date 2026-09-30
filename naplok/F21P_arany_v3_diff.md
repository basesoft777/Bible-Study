# F21P_arany_v3_diff.md — az Opus-arany v2 -> v3 JAVASLAT versenkénti diffje

<!-- GENERÁLT: eszkozok/karoli_strong/arany_v3_javaslat.py | scope=f21p/arany_opus_v2.jsonl -> f21p/arany_opus_v3_javaslat.jsonl (60 vers), hatás az F3V2 és F3V2B C-diffjére | forras=f21p/arany_opus_v2.jsonl (befagyasztva), f21p/arany_opus_v2.sha256, f21p/arany_opus_jegyzetek_v2.md (8. szakasz), eszkozok/karoli_strong/arany_v3_javaslat.py (JAVITASOK, UJ_OSZTALY), f21p/valaszok/F3V2.jsonl, f21p/valaszok/F3V2B.jsonl, f21p/meres_kizaras.tsv, f21p/c_diff_f3v2_osszevetes.tsv, f21p/c_diff_f3v2b_besorolas.tsv | ts=2026-09-30T17:16:07+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

> ⛔ **Megállás (PD13, DT23).** Ez JAVASLAT: az `f21p/arany_opus_v3_javaslat.jsonl` nem befagyasztott, sha256-fájlja nincs. A felhasználó jóváhagyásáig az arany v3 nem fagy be, és a mérés (F3V3, Sonnet) nem fut az arany v3-ra; a befagyasztás a jóváhagyás után az orkesztrátoré.

> **Két változat, a felhasználó választ (F21.44).** **A:** a jelenlegi javaslat, 3 link (`f21p/arany_opus_v3_javaslat.jsonl`, változatlan). **B:** A + a DT21 b) szó szerinti olvasatának további linkjei (`f21p/arany_opus_v3_javaslat_B.jsonl`, 5. szakasz; NEM alkalmazott, NEM befagyasztott). A jegyzet v2 és a prompt_v3 C szabálya az A olvasatot követi.

A javaslat az arany v2 másolata; csak a jegyzet v2 (`f21p/arany_opus_jegyzetek_v2.md` 8. szakasz, a DT21 a–e döntések) konvencióival ütköző linkek változnak, a többi sor bájtra azonos (a szkript ellenőrzi). A szabály- és konvenció-azonosítás és az indok **kézi ítélet (Opus), nem mérés**.

## 1. A változások (vers, magyar szó, régi link, új link)

| vers | magyar szó | régi link (v2) | új link (v3-javaslat) | szabály (DT21) | konvenció | indok |
|---|---|---|---|---|---|---|
| Jób 33:13 | 4 Azért | 4 Azért -> 5 כִּ֥י H3588 [that] | 4 Azért -> betoldas | c | K11 | Azért, hogy ← כִּי: az Azért korrelatív mutató névmásnak nincs külön eredetije, ezért betoldas; a hogy (5) marad a כִּי-n |
| Mt 21:4 | 3 azért | 3 azért -> 5 ἵνα G2443 [that] | 3 azért -> betoldas | c | K11 | azért lett, hogy ← ἵνα: az azért korrelatív mutató névmásnak nincs külön eredetije, ezért betoldas; a hogy (5) marad a ἵνα-n |
| Ez 39:13 | 18 ezt | 18 ezt -> 16 נְאֻ֖ם H5002 [[the] utterance of] | 18 ezt -> betoldas | b | K3 v2 | ezt mondja ← נְאֻם: az ezt tárgyi mutató névmás, nincs sem 'et + rag, sem más eredeti névmási elem, ezért betoldas; a mondja (19) marad a נְאֻם-on (a 6. táblázat sorának alternatívája, a sor maga nem változik) |

Összesen: 3 vers, 3 link változik (a link törlődik, a magyar szó `betoldas`-ba kerül; az eredeti szó a versben más párban marad, tehát `forditatlan` nem változik). Linkek: v2 1051, v3-javaslat 1048. Szabályonként: c (K11) 2, b (K3 v2) 1; a (K7 v2) 0, e (K4 v2) 0, d 0.

## 2. Hatás a v2-es C-diffre (F3V2, F3V2B)

Gépi, számított (nem becslés): melyik eltérés szűnik meg és melyik keletkezik (a c_diff_f3v2.elteresek és a meres.py linkhalmazai, a kizárt tokenek nélkül, a kapun átment aranyverseken). Osztály: a megszűnőé a meglévő kézi besorolás, az újé kézi ítélet (Opus, nem mérés).

| futás | vers | irány | magyar szó | eredeti szó | állapot | osztály | konvenció | indok |
|---|---|---|---|---|---|---|---|---|
| F3V2 | Ez 39:13 | tobblet | 18 ezt | 16 נְאֻ֖ם H5002 [[the] utterance of] | új | a | K3 v2 | az ezt a C-nél a נְאֻם-hoz kötve; a K3 v2 szerint betoldas |
| F3V2 | Jób 33:13 | tobblet | 4 Azért | 5 כִּ֥י H3588 [that] | új | a | K11 | az Azért a C-nél a כִּי-hoz kötve; a K11 szerint betoldas |
| F3V2 | Mt 21:4 | tobblet | 3 azért | 5 ἵνα G2443 [that] | új | a | K11 | az azért a C-nél a ἵνα-hoz kötve; a K11 szerint betoldas |
| F3V2B | Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | megszűnik (c → egyező) | c | — | a meglévő kézi besorolás szerint |
| F3V2B | Ez 39:13 | tobblet | 18 ezt | 16 נְאֻ֖ם H5002 [[the] utterance of] | új | a | K3 v2 | mint az F3V2-nél |
| F3V2B | Jób 33:13 | tobblet | 4 Azért | 5 כִּ֥י H3588 [that] | új | a | K11 | mint az F3V2-nél |

| futás | megszűnő (a / b / c) | új (a / b / c) | eltérés v2 → v3-javaslat | mért pontosság v2 → v3-javaslat | mért lefedettség v2 → v3-javaslat |
|---|---|---|---|---|---|
| F3V2 | 0 (0 / 0 / 0) | 3 (3 / 0 / 0) | 101 → 104 | 93.6% (1020/1090) → 93.3% (1017/1090) | 97.1% (1020/1051) → 97.0% (1017/1048) |
| F3V2B | 1 (0 / 0 / 1) | 2 (2 / 0 / 0) | 103 → 104 | 93.0% (1025/1102) → 92.8% (1023/1102) | 97.5% (1025/1051) → 97.6% (1023/1048) |

A mért pontosság és lefedettség itt csak a 60 aranyversre, a két arany összevetésére szól (tájékoztató; a küszöb szempontjából a P4-mérés számít, és az a jóváhagyás után az arany v3-ra fut). A javaslat a C-diffet nem javítja: a három link a mért C-futásokban az arany v2-vel egyezett, a v3 konvenciója szerint viszont a C (a) konvenciókülönbséget mutat; az arany nem igazodik a mért modellhez (PD10).

## 3. Nem érintett pontok (a–e)

- **a (K7 v2):** az arany v2-ben minden segédige `betoldas`, ahol nincs külön eredeti ige; a kivétel csak a Mt 4:4 *Meg van írva*. A *lészen* (Jak 3:1 ← λημψόμεθα) és a *van* (Mk 2:10, Mt 11:18 ← ἔχει) külön eredeti igét fordít, nem segédige-betoldás. Nincs változás.
- **b (K3 v2):** a többi magyar tárgyi névmás *'et* + ragra (K3), igei/elöljárós névmási ragra (K4) vagy önálló eredeti névmásra kötött, a megfelelő nélküliek (Péld 23:19 *engem*, Zsolt 22:32 *ezt*, Mt 5:34 *azt*, Mt 11:18 *azt*, Jak 3:1 *azt*, 1Ján 1:10 *azt*) már `betoldas`. A döntés szó szerinti (szűkebb) olvasatának hatása: a jegyzet v2 8.3 pont 1. kérdése és az 5. szakasz (B változat).
- **c (K11):** a Jak 3:1 és az 1Ján 1:10 *azt … hogy* már a K11 szerinti (*azt* `betoldas`, *hogy* a ὅτι-n); a 2Móz 21:26 *úgy … hogy* a 6. táblázat szerint szintén.
- **d:** 2Móz 26:13 *is*: marad (a 6. táblázat és az arany v2 szerint).
- **e (K4 v2):** minden birtokos/névmási rag a megfelelő személyragot viselő szón (2Móz 21:26 *szolgálójának* ← 13 -ô); birtokláncban (Zsolt 18:1 *ellenségének kezéből*, Jer 46:21 *romlásuk napja*, *megfenyíttetésök ideje*) a rag a megfelelő szón. Nyitott: 2Móz 25:40 *arra*, Ez 39:13 *megdicsőítem* (jegyzet v2 8.3).

## 4. Kapu

A javaslat ellenőrzése: `python eszkozok/karoli_strong/arany_ellenoriz.py --arany f21p/arany_opus_v3_javaslat.jsonl` (a befagyasztás-ellenőrzés csak az arany v2 útvonalára fut; a javaslatra a kapu öt pontja, a `[nem TR]` és a mérési kizárás ellenőrzése fut). Ez a szkript a javaslat minden versét a kapun is átengedi (kapu.vers_ellenoriz), különben hibával megáll: **60/60 vers átmegy a kapun**, 1048 link.

## 5. B) változat — a DT21 b) szó szerinti olvasata (NEM alkalmazott, döntésre)

A felhasználó értelmezése (F21.44): „a névmás a ragra kötődik” — *'et* + rag esetén a magyar névmás a ragra megy, az *'et* `forditatlan` (ez mindkét változatban így van). **Nincs eldöntve** az igén (főnévi igenéven, elöljárón) álló, *'et* nélküli névmási rag külön kitett magyar névmása: **(A)** a K4 szerint a raghoz kötve marad (a jelenlegi javaslat, `f21p/arany_opus_v3_javaslat.jsonl`); **(B)** szó szerint: a névmás `betoldas`, a rag `forditatlan` (`f21p/arany_opus_v3_javaslat_B.jsonl` = A + az alábbi linkek; NEM befagyasztott). A B a DT20 a) kérdését (tárgyrag az igén) is érinti: a rag itt `forditatlan`, nem az igéhez kötött. Az osztály és az indok kézi ítélet (Opus), nem mérés.

| vers | magyar szó | régi link (A) | új link (B) | konvenció | indok |
|---|---|---|---|---|---|
| 2Móz 20:25 | 19 azt | 19 azt -> 21 הָ H9034 [it] | 19 azt -> betoldas | K3 v2, B olvasat | megfertőztetted azt ← -hā az igén (nincs 'et): az azt betoldas, a rag forditatlan |
| 2Móz 21:6 | 3 őt | 3 őt -> 3 וֹ H9033 [him] | 3 őt -> betoldas | K3 v2, B olvasat | vigye őt ← -ô, szolgálja őt ← -ô az igén (nincs 'et): mindkét őt betoldas, a ragok forditatlan |
| 2Móz 21:6 | 29 őt | 29 őt -> 30 וֹ H9033 [him] | 29 őt -> betoldas | K3 v2, B olvasat | vigye őt ← -ô, szolgálja őt ← -ô az igén (nincs 'et): mindkét őt betoldas, a ragok forditatlan |
| 2Móz 21:26 | 16 azt | 16 azt -> 20 נּוּ H9033 [him] | 16 azt -> betoldas | K3 v2, B olvasat | bocsássa azt ← -ennû az igén (nincs 'et): az azt betoldas, a rag forditatlan |
| 2Móz 26:13 | 28 azt | 28 azt -> 31 וֹ H9033 [it] | 28 azt -> betoldas | K3 v2, B olvasat | befedje azt ← -ô a főnévi igenéven (nincs 'et): az azt betoldas, a rag forditatlan |
| Péld 28:17 | 14 őt | 14 őt -> 11 בֽ H9003 [<in>]; 12 וֹ H9033 [him] | 14 őt -> betoldas | K3 v2, B olvasat | támogassa őt ← bô (elöljáró + rag, nincs 'et): az őt betoldas, az elöljáró és a rag forditatlan (elöljárós eset: a B olvasat itt a legvitathatóbb) |
| Zsolt 6:5 | 9 engem | 9 engem -> 9 נִי H9030 [me] | 9 engem -> betoldas | K3 v2, B olvasat | segíts meg engem ← -ní az igén (nincs 'et): az engem betoldas, a rag forditatlan |
| Zsolt 16:11 | 3 engem | 3 engem -> 2 נִי֮ H9030 [me] | 3 engem -> betoldas | K3 v2, B olvasat | tanítasz engem ← -ní az igén (nincs 'et): az engem betoldas, a rag forditatlan |

A B változat az A-hoz képest: 7 vers, 8 magyar szó, 9 link (a rag `forditatlan`-ba kerül). Linkek: A 1048, B 1039. Kapu: **60/60 vers átmegy** (B).

**A B változat további hatása a C-diffre** (a B-nek az arany v2-höz mért eltérései közül azok, amelyek az A-ban nincsenek; számított, c_diff_f3v2.elteresek):

| futás | vers | irány | magyar szó | eredeti szó | állapot | osztály | konvenció |
|---|---|---|---|---|---|---|---|
| F3V2 | 2Móz 20:25 | tobblet | 19 azt | 21 הָ H9034 [it] | új | a | K3 v2, B olvasat |
| F3V2 | 2Móz 21:26 | tobblet | 16 azt | 20 נּוּ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2 | 2Móz 21:6 | tobblet | 3 őt | 3 וֹ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2 | 2Móz 21:6 | tobblet | 29 őt | 30 וֹ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2 | 2Móz 26:13 | tobblet | 28 azt | 31 וֹ H9033 [it] | új | a | K3 v2, B olvasat |
| F3V2 | Péld 28:17 | tobblet | 14 őt | 11 בֽ H9003 [<in>] | új | a | K3 v2, B olvasat |
| F3V2 | Péld 28:17 | tobblet | 14 őt | 12 וֹ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2 | Zsolt 16:11 | tobblet | 3 engem | 2 נִי֮ H9030 [me] | új | a | K3 v2, B olvasat |
| F3V2 | Zsolt 6:5 | tobblet | 9 engem | 9 נִי H9030 [me] | új | a | K3 v2, B olvasat |
| F3V2B | 2Móz 20:25 | tobblet | 19 azt | 21 הָ H9034 [it] | új | a | K3 v2, B olvasat |
| F3V2B | 2Móz 21:26 | tobblet | 16 azt | 20 נּוּ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2B | 2Móz 21:6 | tobblet | 3 őt | 3 וֹ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2B | 2Móz 21:6 | tobblet | 29 őt | 30 וֹ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2B | 2Móz 26:13 | tobblet | 28 azt | 31 וֹ H9033 [it] | új | a | K3 v2, B olvasat |
| F3V2B | Péld 28:17 | tobblet | 14 őt | 11 בֽ H9003 [<in>] | új | a | K3 v2, B olvasat |
| F3V2B | Péld 28:17 | tobblet | 14 őt | 12 וֹ H9033 [him] | új | a | K3 v2, B olvasat |
| F3V2B | Zsolt 16:11 | tobblet | 3 engem | 2 נִי֮ H9030 [me] | új | a | K3 v2, B olvasat |
| F3V2B | Zsolt 6:5 | tobblet | 9 engem | 9 נִי H9030 [me] | új | a | K3 v2, B olvasat |

**A két változat hatása a két C-futásra (az arany v2-höz képest):**

*A változat:*

| futás | megszűnő (a / b / c) | új (a / b / c) | eltérés v2 → A | mért pontosság v2 → A | mért lefedettség v2 → A |
|---|---|---|---|---|---|
| F3V2 | 0 (0 / 0 / 0) | 3 (3 / 0 / 0) | 101 → 104 | 93.6% (1020/1090) → 93.3% (1017/1090) | 97.1% (1020/1051) → 97.0% (1017/1048) |
| F3V2B | 1 (0 / 0 / 1) | 2 (2 / 0 / 0) | 103 → 104 | 93.0% (1025/1102) → 92.8% (1023/1102) | 97.5% (1025/1051) → 97.6% (1023/1048) |

*B változat:*

| futás | megszűnő (a / b / c) | új (a / b / c) | eltérés v2 → B | mért pontosság v2 → B | mért lefedettség v2 → B |
|---|---|---|---|---|---|
| F3V2 | 0 (0 / 0 / 0) | 12 (12 / 0 / 0) | 101 → 113 | 93.6% (1020/1090) → 92.5% (1008/1090) | 97.1% (1020/1051) → 97.0% (1008/1039) |
| F3V2B | 1 (0 / 0 / 1) | 11 (11 / 0 / 0) | 103 → 113 | 93.0% (1025/1102) → 92.0% (1014/1102) | 97.5% (1025/1051) → 97.6% (1014/1039) |

Mindkét C-futás mind a 9 érintett linknél az A olvasatot követte (a névmás a raghoz kötve), ezért a B minden további linkje új (a) eltérés. A változatválasztás a felhasználóé; az arany nem igazodik a mért modellhez (PD10).
