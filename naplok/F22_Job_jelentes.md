# F22_Job_jelentes.md — Károli–Strong párosítás: Jób (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Jób`, `egyesit.py --konyv Jób` és `--ellenoriz`, `f22_elemzes.py --konyv Jób`, `versbeosztas.py`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Jób-sorainak összesítése (`futas = api_termeles/high/Job`, `cimke = job`), a `f22/api_termeles/high/_munka/Job_k*.json` hibaüzenetei). Ág: `claude/peaceful-meitner-1vzy4m`, a Péld- és a Bír-menet után; a main (`ce9f7be`, benne a #84) a `7ace9ad` merge-dzsel bevonva. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Indítás: a felhasználó a Jób újbóli átnézését kérte, majd jóváhagyta (chat, 2026.10.09: „Mehet a Jób, egy menetben. Jóváhagyom”). Előzmény: a #83 (Jób 38–42 megfeleltetés, DT85) és a #84 (a Jób 41 34 verse a `TAHOT_kivonat`-ba, N55 / DT86).*

## 1. Menet

### 1.1 Versbeosztás

- **A detektor újragenerálása** (`python eszkozok/karoli_strong/versbeosztas.py`, a #84 utáni `TAHOT_kivonat`-ból, a felhasználó feltétele szerint): a `f22/versmegfeleltetes.tsv`-ben csak a Jób sorai változtak. A Jób 40:1–5, 13, 16, 19 és a Jób 41 26 `nincs_eredeti` sora helyére a Károli 40:n → TAHOT 40:(n+5), n = 1–19 `eltolt` sorok kerültek (= a #83 kézi sorai, amelyek maradnak); a Jób 41-nek nincs sora. A `naplok/F22_versbeosztas.md` Jób-sora: Károli 1068, TAHOT 1070 vers, K-hiány 0 (korábban 34). A 17. és a 37. fejezet detektorsorai (17:10 `nincs_karoli`, 17:10–15 `eltolt`; 37:21 `nincs_karoli`, 37:21–23 `eltolt`) nem változtak. Commit: „F22.Job: versbeosztas.py újragenerálva …”.
- **Kézi javítás (jóváhagyva):** a detektor a 17. és a 37. fejezetben csak a fejezet végét jelzi, a fejezet elejét nem. A szövegösszevetés szerint mindkét helyen a Károli a következő fejezet első héber versét az előző fejezet utolsó versébe vonja (2:1):
  - **Jób 16:22** (21 szó): az 1–13. szó = TAHOT 16:22 („Mert a kiszabott esztendők letelnek … nem térek vissza”), a **14–21. szó** („Lelkem meghanyatlott, napjaim elfogynak, vár rám a sír”) = **TAHOT 17:1** (9 héber szó). Ezután Károli 17:n → TAHOT 17:(n+1), n = 1–15 (pl. a Károli 17:9 „Nosza hát, térjetek ide mindnyájan …” = TAHOT 17:10 „and but all of them you will return and come please …”; a 17:15 „Leszáll az majd a sír üregébe …” = TAHOT 17:16 „[the] poles of Sheol will they go down? …”).
  - **Jób 36:33** (21 szó): az 1–12. szó = TAHOT 36:33, a **13–21. szó** („Ezért remeg az én szívem, és csaknem kiszökik helyéből”) = **TAHOT 37:1** (11 héber szó). Ezután Károli 37:n → TAHOT 37:(n+1), n = 1–23 (pl. a 37:1 „Halljátok meg figyelmetesen az ő hangjának dörgését …” = TAHOT 37:2 „listen completely <to listen> to [the] raging of voice his …”; a 37:23 „Azért rettegjék őt az emberek …” = TAHOT 37:24).
  - `f22/versmegfeleltetes_kezi.tsv` +40 sor (17. fejezet: 1 `nincs_karoli` + 15 `eltolt`; 37. fejezet: 1 + 23), `f22/versosszevonas.tsv` +2 sor; a #83 19 sora (40. fejezet) változatlan.
  - **A detektor 17. és 37. fejezeti sorai ezzel rendeződnek:** a kézi sorok azonos Károli-kulccsal kiváltják a detektor `eltolt` sorait (17:10–15, 37:21–23), a `nincs_karoli` sorokat (TAHOT 17:10, 37:21) pedig az azonos eredetijű kézi `eltolt` sor (Károli 17:9 → TAHOT 17:10, 37:20 → 37:21). Igazolás: a szimuláció (alább) szerint pár nélküli Károli-vers és gazdátlan (+1000-es) eredeti vers nincs.
- **Teljes könyv ellenőrzése** a jóváhagyás előtt: fejezetenkénti vershossz-korreláció (azonos sorrend vs. ±1 eltolás) a javított megfeleltetéssel. Eltolás-jel (az eltolt korreláció érdemben jobb) egyetlen fejezetben sincs; a gyenge r(0) a költői fejezetekben az egyenletes vershossz miatt nem eltolódás-jel. Mintaversek a fejezethatárokon (25:1, 25:6, 15:35, 39:1, 39:34, 39:38, 40:19, 41:1, 41:25, 41:26, 41:34, 42:1) mind tartalmilag egyeznek. A 41:25 „összeolvadt vers” régi gyanúja nem igazolódott (a #84 is így döntött, DT86 (b)).
- **Szimuláció** (ezen az ágon, a detektor újragenerálása után): nyers 1070 TAHOT-vers / 12 482 token = leképezett 1068 vers / 12 462 token + 20 beolvasztott token (9 + 11); Károli-vers pár nélkül és gazdátlan vers nincs.
- Jóváhagyási sor: `naplok/F22_versbeosztas_jovahagyas.md`; a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Jób'`).

### 1.2 Futás

- **Minta:** `f22/minta_Job.tsv`, 1068 vers (= a `Karoli_1908.tsv` `Jób ` sorai), 107 köteg (10 vers/köteg, az utolsó 8).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01PMYrqEz62YnqUFG5xTqr7y`, 107 kérés (2026-10-09T06:46Z); javító kör `msgbatch_016KFNC94pEetXEZEpEz3nMS`, 26 kérés (06:51Z).
- **Futásnapló** (Jób: 133 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 107 | 81 | 26 köteg (103 vers) | 3,0193 | 890 660 / 425 731 |
| 2. próba (javító) | 26 | 26 | 0 | 0,5918 | 259 513 / 66 454 |
| **összesen** | 133 | | | **3,6111** | |

A javító körbe került kötegek: 1, 9, 11, 19, 21, 27, 32, 33, 37, 38, 39, 61, 66, 67, 72, 73, 79, 82, 86, 89, 96, 97, 98, 102, 106, 107. Ebből **hat köteg egészében bukott**, mert a válasz nem érvényes JSON (k021, k032, k037, k038, k067, k082, egyenként 10 vers, összesen 60), tehát a forma volt hibás, nem a párosítás. A többi 43 vers versszintű kapuhiba (34 hibás pár-forma, 6 gazdátlan eredeti sorszám, 3 hiányzó vagy többször szereplő magyar sorszám). Az első próbás kapuhiba (9,6%) magasabb a Péld (6,1%) és a Bír (2,1%) értékénél; a végleges kapuhiba 0.

A könyvplafonból (1068 × 0,0074 × 1,5 = 11,85 USD) 3,61 fogyott; a futásnapló futó összege 47,0709 USD (Ézs–Bír 43,4598 + Jób 3,6111), a globális 110 USD-ből. Versenként 0,0034 USD.

## 1a. Szkriptkimenet

```
Sonnet: 107 köteg, 1068 vers; kapuhiba első próbára 9.6% (103/1068); végleg 0.0% (0/1068)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Jób`: `parok_Job.tsv` 13 420 link (mind `alacsony`, `S`; a fájl 13 422 sora a proveniencia- és a fejlécsorral), `szavak_Job.tsv` 26 225 token (26 227 sor). A szavak bontása: hu 13 743 (10 928 `parositva`, 2 798 `betoldas`, 17 `fuggoben`), er 12 482 (11 999 `parositva`, 463 `forditatlan`, 20 `fuggoben`); az er szám = a `TAHOT_kivonat.tsv` `Jób ` sorainak száma (12 482, benne a #84 332 Jób 41-es sora). A 37 `fuggoben` (`kezi`) token a két beolvasztott rész: a Károli 16:22 14–21. és a 36:33 13–21. szava (8 + 9), valamint a TAHOT 17:1 és 37:1 szavai (9 + 11), link nélkül. Az átnézési sor (`naplok/F22_Job_atnezes.tsv`) ezt a két verset tartalmazza (Jób 16:22, 36:33).

`egyesit.py --ellenoriz --konyv Jób` (2026.10.09, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Jób` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/13420), alacsony 100.0% (13420/13420), kezi 0.0% (0/13420); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/26225), alacsony 99.9% (26188/26225), kezi 0.1% (37/26225).

Link-forrás megoszlás (parok): S 13420. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 1068 (Jób 10:1, Jób 10:10, Jób 10:11, Jób 10:12, Jób 10:13, Jób 10:14, Jób 10:15, Jób 10:16, Jób 10:17, Jób 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 557 | 0.0% (0/557) | 100.0% (557/557) | 0.0% (0/557) | 1081 | 0.0% (0/1081) | 100.0% (1081/1081) | 0.0% (0/1081) |
| 2 | 347 | 0.0% (0/347) | 100.0% (347/347) | 0.0% (0/347) | 666 | 0.0% (0/666) | 100.0% (666/666) | 0.0% (0/666) |
| 3 | 317 | 0.0% (0/317) | 100.0% (317/317) | 0.0% (0/317) | 631 | 0.0% (0/631) | 100.0% (631/631) | 0.0% (0/631) |
| 4 | 256 | 0.0% (0/256) | 100.0% (256/256) | 0.0% (0/256) | 474 | 0.0% (0/474) | 100.0% (474/474) | 0.0% (0/474) |
| 5 | 337 | 0.0% (0/337) | 100.0% (337/337) | 0.0% (0/337) | 656 | 0.0% (0/656) | 100.0% (656/656) | 0.0% (0/656) |
| 6 | 355 | 0.0% (0/355) | 100.0% (355/355) | 0.0% (0/355) | 687 | 0.0% (0/687) | 100.0% (687/687) | 0.0% (0/687) |
| 7 | 300 | 0.0% (0/300) | 100.0% (300/300) | 0.0% (0/300) | 571 | 0.0% (0/571) | 100.0% (571/571) | 0.0% (0/571) |
| 8 | 268 | 0.0% (0/268) | 100.0% (268/268) | 0.0% (0/268) | 502 | 0.0% (0/502) | 100.0% (502/502) | 0.0% (0/502) |
| 9 | 397 | 0.0% (0/397) | 100.0% (397/397) | 0.0% (0/397) | 777 | 0.0% (0/777) | 100.0% (777/777) | 0.0% (0/777) |
| 10 | 305 | 0.0% (0/305) | 100.0% (305/305) | 0.0% (0/305) | 586 | 0.0% (0/586) | 100.0% (586/586) | 0.0% (0/586) |
| 11 | 226 | 0.0% (0/226) | 100.0% (226/226) | 0.0% (0/226) | 476 | 0.0% (0/476) | 100.0% (476/476) | 0.0% (0/476) |
| 12 | 265 | 0.0% (0/265) | 100.0% (265/265) | 0.0% (0/265) | 583 | 0.0% (0/583) | 100.0% (583/583) | 0.0% (0/583) |
| 13 | 330 | 0.0% (0/330) | 100.0% (330/330) | 0.0% (0/330) | 623 | 0.0% (0/623) | 100.0% (623/623) | 0.0% (0/623) |
| 14 | 293 | 0.0% (0/293) | 100.0% (293/293) | 0.0% (0/293) | 562 | 0.0% (0/562) | 100.0% (562/562) | 0.0% (0/562) |
| 15 | 413 | 0.0% (0/413) | 100.0% (413/413) | 0.0% (0/413) | 829 | 0.0% (0/829) | 100.0% (829/829) | 0.0% (0/829) |
| 16 | 289 | 0.0% (0/289) | 100.0% (289/289) | 0.0% (0/289) | 566 | 0.0% (0/566) | 97.0% (549/566) | 3.0% (17/566) |
| 17 | 167 | 0.0% (0/167) | 100.0% (167/167) | 0.0% (0/167) | 335 | 0.0% (0/335) | 100.0% (335/335) | 0.0% (0/335) |
| 18 | 243 | 0.0% (0/243) | 100.0% (243/243) | 0.0% (0/243) | 458 | 0.0% (0/458) | 100.0% (458/458) | 0.0% (0/458) |
| 19 | 359 | 0.0% (0/359) | 100.0% (359/359) | 0.0% (0/359) | 678 | 0.0% (0/678) | 100.0% (678/678) | 0.0% (0/678) |
| 20 | 367 | 0.0% (0/367) | 100.0% (367/367) | 0.0% (0/367) | 714 | 0.0% (0/714) | 100.0% (714/714) | 0.0% (0/714) |
| 21 | 419 | 0.0% (0/419) | 100.0% (419/419) | 0.0% (0/419) | 774 | 0.0% (0/774) | 100.0% (774/774) | 0.0% (0/774) |
| 22 | 346 | 0.0% (0/346) | 100.0% (346/346) | 0.0% (0/346) | 686 | 0.0% (0/686) | 100.0% (686/686) | 0.0% (0/686) |
| 23 | 217 | 0.0% (0/217) | 100.0% (217/217) | 0.0% (0/217) | 403 | 0.0% (0/403) | 100.0% (403/403) | 0.0% (0/403) |
| 24 | 297 | 0.0% (0/297) | 100.0% (297/297) | 0.0% (0/297) | 622 | 0.0% (0/622) | 100.0% (622/622) | 0.0% (0/622) |
| 25 | 68 | 0.0% (0/68) | 100.0% (68/68) | 0.0% (0/68) | 140 | 0.0% (0/140) | 100.0% (140/140) | 0.0% (0/140) |
| 26 | 146 | 0.0% (0/146) | 100.0% (146/146) | 0.0% (0/146) | 290 | 0.0% (0/290) | 100.0% (290/290) | 0.0% (0/290) |
| 27 | 291 | 0.0% (0/291) | 100.0% (291/291) | 0.0% (0/291) | 558 | 0.0% (0/558) | 100.0% (558/558) | 0.0% (0/558) |
| 28 | 314 | 0.0% (0/314) | 100.0% (314/314) | 0.0% (0/314) | 629 | 0.0% (0/629) | 100.0% (629/629) | 0.0% (0/629) |
| 29 | 293 | 0.0% (0/293) | 100.0% (293/293) | 0.0% (0/293) | 566 | 0.0% (0/566) | 100.0% (566/566) | 0.0% (0/566) |
| 30 | 371 | 0.0% (0/371) | 100.0% (371/371) | 0.0% (0/371) | 709 | 0.0% (0/709) | 100.0% (709/709) | 0.0% (0/709) |
| 31 | 509 | 0.0% (0/509) | 100.0% (509/509) | 0.0% (0/509) | 977 | 0.0% (0/977) | 100.0% (977/977) | 0.0% (0/977) |
| 32 | 289 | 0.0% (0/289) | 100.0% (289/289) | 0.0% (0/289) | 583 | 0.0% (0/583) | 100.0% (583/583) | 0.0% (0/583) |
| 33 | 400 | 0.0% (0/400) | 100.0% (400/400) | 0.0% (0/400) | 761 | 0.0% (0/761) | 100.0% (761/761) | 0.0% (0/761) |
| 34 | 444 | 0.0% (0/444) | 100.0% (444/444) | 0.0% (0/444) | 889 | 0.0% (0/889) | 100.0% (889/889) | 0.0% (0/889) |
| 35 | 183 | 0.0% (0/183) | 100.0% (183/183) | 0.0% (0/183) | 371 | 0.0% (0/371) | 100.0% (371/371) | 0.0% (0/371) |
| 36 | 382 | 0.0% (0/382) | 100.0% (382/382) | 0.0% (0/382) | 749 | 0.0% (0/749) | 97.3% (729/749) | 2.7% (20/749) |
| 37 | 293 | 0.0% (0/293) | 100.0% (293/293) | 0.0% (0/293) | 572 | 0.0% (0/572) | 100.0% (572/572) | 0.0% (0/572) |
| 38 | 414 | 0.0% (0/414) | 100.0% (414/414) | 0.0% (0/414) | 834 | 0.0% (0/834) | 100.0% (834/834) | 0.0% (0/834) |
| 39 | 409 | 0.0% (0/409) | 100.0% (409/409) | 0.0% (0/409) | 815 | 0.0% (0/815) | 100.0% (815/815) | 0.0% (0/815) |
| 40 | 224 | 0.0% (0/224) | 100.0% (224/224) | 0.0% (0/224) | 428 | 0.0% (0/428) | 100.0% (428/428) | 0.0% (0/428) |
| 41 | 358 | 0.0% (0/358) | 100.0% (358/358) | 0.0% (0/358) | 699 | 0.0% (0/699) | 100.0% (699/699) | 0.0% (0/699) |
| 42 | 362 | 0.0% (0/362) | 100.0% (362/362) | 0.0% (0/362) | 715 | 0.0% (0/715) | 100.0% (715/715) | 0.0% (0/715) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 14; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 92.9% (13/14).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/14).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 92.9% (13/14).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

### 2.4 A régi arany eltérésének oka

**A régi arany 13/14 eltérése a régi arany kulcshibája, nem párosítási hiba.** A `Karoli_Strong_kivonat.tsv` `Job.17.13` hármasa („A sírnak”, H7585) a Károli 17:13 szavát a H7585-tel párosítja. A H7585 (שְׁאוֹל) azonban a TAHOT 17:13-ban áll, ami a fenti eltolás szerint a Károli 17:12 („… a sír már az én házam …”); a párosítás ott H7585-öt ad (`parok_Job.tsv`: Jób 17:12 hu 5 „sír” → H7585). A Károli 17:13 („A sírnak mondom: Te vagy az én atyám …”) = TAHOT 17:14, ahol a szó שַׁחַת (H7845, „pit”); a Sonnet ezt adta (Jób 17:13 hu 2 „sírnak” → H7845, H9005). A régi arany a Károli-szót és a héber Strongot két különböző versszámozásból vette. Ugyanebből a forrásból a `Job.17.16` („a sír üregébe”) hármas a mérésből kiesik, mert Károli 17:16 nincs (a szó a Károli 17:15-ben áll, ott H7585-tel párosítva). Javaslat: a `Job.17.13` sor kerüljön az `f21p/regi_arany_hibas.tsv`-be (külön tétel; az `f21p/` ebben a menetben nem módosul).

## 3. Kézi átnézésre jelölt pontok

- **Jób 16:22 és 36:33** (`naplok/F22_Job_atnezes.tsv`): a beolvasztott részek link nélkül, `kezi`; a kézi párosítás a felhasználóé.
- A régi arany `Job.17.13` hármasa (lásd fent): javasolt felvétel a hibás hármasok közé.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A main bevonása (`7ace9ad`, #84), ütközés a jóváhagyási naplóban (a main frissített Jób 38–42 sora maradt).
- A detektor újragenerálása (`f22/versmegfeleltetes.tsv`, `naplok/F22_versbeosztas.md`, csak Jób-sorok).
- K9: a Jób bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba (a 17., 37., 40. fejezeti megfeleltetés és a két beolvasztás is).
- A brief fejléce: `kovetkezo`, `ir`, D26, v2.20.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_Job.md`.
- Kézi átnézés: Jób 16:22, 36:33, Péld 11:31; korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1.
- PR és merge a felhasználóé (az ág a Péld-, a Bír- és a Jób-menetet hordozza).
- A következő könyv a felhasználó döntése; a mérés (2026.10.09) szerinti tiszta jelöltek: Eszt, 2Sám, 1Sám, 1Kir, Neh, 2Kir; a Dán (37 detektorsor) előtt versbeosztás-döntés kell.
