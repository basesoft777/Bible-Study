# F22_Ez_jelentes.md — Károli–Strong párosítás: Ezékiel (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Ez`, `egyesit.py --ellenoriz --konyv Ez`, `f22_elemzes.py --konyv Ez`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Ez-sorainak összesítése, a `f22/api_termeles/high/_munka/Ez_k*.json` hibaüzenetei). Az összesítés **pontos egyezéssel** szűr (`futas = api_termeles/high/Ez`, `cimke = ez`, `Ez_k*.json`), mert az „Ez” előtag az Ézs- és az Ezsd-sorokra is illeszkedne. Ág: `claude/f22-ez`, az Ezsd-ág utolsó commitjáról (`5e88854`) indítva; az Ezsd-ág még nincs a main-ben. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek (a prófétáknál is, DT71 (a)).*

*Sorrend: a DT57 (1) mérése szerint az Ezsd után a Jób (159) jönne; a Jób versmegfeleltetése nyitott (TAHOT-hiány, Jób 40:1–5, 41; #83), ezért az Ez (147) a felhasználó utasítására előre került (chat, 2026.10.08: „menjen ezékiel”). A könyvnév (`Ez`) ASCII és magyar alakja azonos.*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.08, chat: „menjen ezékiel”)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az Ez tiszta (1273/1273 vers), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Ez'`).
- **Minta:** `f22/minta_Ez.tsv`, 1273 vers (= a `Karoli_1908.tsv` `Ez ` sorai), 128 köteg (10 vers/köteg, az utolsó 3).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01X2PBzAbkXg74SpKvLaZaNX`, 128 kérés (2026-10-08T17:18Z); javító kör `msgbatch_018rXDJYERgVKYWFenHzTJQm`, 18 kérés (17:25Z).
- **Futásnapló** (Ez: 146 sor, `futas=api_termeles/high/Ez`): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb` (mint az Ézs–Ezsd soraiban).

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 128 | 110 | 18 köteg (32 vers) | 7,3445 | 1 429 233 / 1 183 048 |
| 2. próba (javító) | 18 | 18 | 0 | 0,4567 | 247 154 / 41 901 |
| **összesen** | 146 | | | **7,8011** | |

A javító körbe került kötegek: 3, 16, 17, 18, 24, 28, 29, 45, 46, 52, 63, 72, 77, 83, 88, 94, 99, 116. Ebből **egy köteg egészében bukott**: a k088 (Ez 34:22–31, 10 vers), mert a válasz nem érvényes JSON („Extra data”), tehát a forma volt hibás, nem a párosítás. A többi 22 vers versszintű kapuhiba (főleg gazdátlan eredeti sorszám, ritkábban hiányzó magyar sorszám és üres partnerlista).

A könyvplafonból (1273 × 0,0074 × 1,5 = 14,13 USD) 7,80 fogyott; a futásnapló futó összege 36,4560 USD (Ézs 7,0834 + Jer 9,0552 + 1Krón 4,5552 + 2Krón 6,3183 + Ezsd 1,6428 + Ez 7,8011), a globális 110 USD-ből. Versenként 0,0061 USD (a plafon alapja 0,0074).

## 1a. Szkriptkimenet

```
Sonnet: 128 köteg, 1273 vers; kapuhiba első próbára 2.5% (32/1273); végleg 0.0% (0/1273)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Ez`: `parok_Ez.tsv` 28 852 link (mind `alacsony`, `S`; a fájl 28 854 sora a proveniencia- és a fejlécsorral), `szavak_Ez.tsv` 56 397 token (56 399 sor). A szavak bontása: hu 27 173 (22 722 `parositva`, 4 451 `betoldas`), er 29 224 (27 159 `parositva`, 2 065 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Ez ` sorainak száma (29 224). Az átnézési sor (`naplok/F22_Ez_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz --konyv Ez` (2026.10.08, ezen az ágon): „ellenőrzés: rendben”. A többi könyvre ebben a menetben nem futott újra; a táblájuk az Ezsd-ellenőr óta (`5e88854..HEAD`) nem változott (`git diff --stat -- adat/karoli_strong/` csak a két Ez-táblát mutatja; `konkordancia/`, `f21p/` üres, az `eszkozok/` alatt csak a `tokenek.py` jóváhagyási sora).

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Ez` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/28852), alacsony 100.0% (28852/28852), kezi 0.0% (0/28852); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/56397), alacsony 100.0% (56397/56397), kezi 0.0% (0/56397).

Link-forrás megoszlás (parok): S 28852. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 1273 (Ez 10:1, Ez 10:10, Ez 10:11, Ez 10:12, Ez 10:13, Ez 10:14, Ez 10:15, Ez 10:16, Ez 10:17, Ez 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 639 | 0.0% (0/639) | 100.0% (639/639) | 0.0% (0/639) | 1273 | 0.0% (0/1273) | 100.0% (1273/1273) | 0.0% (0/1273) |
| 2 | 228 | 0.0% (0/228) | 100.0% (228/228) | 0.0% (0/228) | 437 | 0.0% (0/437) | 100.0% (437/437) | 0.0% (0/437) |
| 3 | 662 | 0.0% (0/662) | 100.0% (662/662) | 0.0% (0/662) | 1251 | 0.0% (0/1251) | 100.0% (1251/1251) | 0.0% (0/1251) |
| 4 | 404 | 0.0% (0/404) | 100.0% (404/404) | 0.0% (0/404) | 765 | 0.0% (0/765) | 100.0% (765/765) | 0.0% (0/765) |
| 5 | 470 | 0.0% (0/470) | 100.0% (470/470) | 0.0% (0/470) | 885 | 0.0% (0/885) | 100.0% (885/885) | 0.0% (0/885) |
| 6 | 338 | 0.0% (0/338) | 100.0% (338/338) | 0.0% (0/338) | 640 | 0.0% (0/640) | 100.0% (640/640) | 0.0% (0/640) |
| 7 | 550 | 0.0% (0/550) | 100.0% (550/550) | 0.0% (0/550) | 1074 | 0.0% (0/1074) | 100.0% (1074/1074) | 0.0% (0/1074) |
| 8 | 475 | 0.0% (0/475) | 100.0% (475/475) | 0.0% (0/475) | 958 | 0.0% (0/958) | 100.0% (958/958) | 0.0% (0/958) |
| 9 | 307 | 0.0% (0/307) | 100.0% (307/307) | 0.0% (0/307) | 617 | 0.0% (0/617) | 100.0% (617/617) | 0.0% (0/617) |
| 10 | 466 | 0.0% (0/466) | 100.0% (466/466) | 0.0% (0/466) | 994 | 0.0% (0/994) | 100.0% (994/994) | 0.0% (0/994) |
| 11 | 533 | 0.0% (0/533) | 100.0% (533/533) | 0.0% (0/533) | 1029 | 0.0% (0/1029) | 100.0% (1029/1029) | 0.0% (0/1029) |
| 12 | 595 | 0.0% (0/595) | 100.0% (595/595) | 0.0% (0/595) | 1134 | 0.0% (0/1134) | 100.0% (1134/1134) | 0.0% (0/1134) |
| 13 | 522 | 0.0% (0/522) | 100.0% (522/522) | 0.0% (0/522) | 1055 | 0.0% (0/1055) | 100.0% (1055/1055) | 0.0% (0/1055) |
| 14 | 622 | 0.0% (0/622) | 100.0% (622/622) | 0.0% (0/622) | 1148 | 0.0% (0/1148) | 100.0% (1148/1148) | 0.0% (0/1148) |
| 15 | 148 | 0.0% (0/148) | 100.0% (148/148) | 0.0% (0/148) | 304 | 0.0% (0/304) | 100.0% (304/304) | 0.0% (0/304) |
| 16 | 1427 | 0.0% (0/1427) | 100.0% (1427/1427) | 0.0% (0/1427) | 2631 | 0.0% (0/2631) | 100.0% (2631/2631) | 0.0% (0/2631) |
| 17 | 584 | 0.0% (0/584) | 100.0% (584/584) | 0.0% (0/584) | 1124 | 0.0% (0/1124) | 100.0% (1124/1124) | 0.0% (0/1124) |
| 18 | 674 | 0.0% (0/674) | 100.0% (674/674) | 0.0% (0/674) | 1344 | 0.0% (0/1344) | 100.0% (1344/1344) | 0.0% (0/1344) |
| 19 | 259 | 0.0% (0/259) | 100.0% (259/259) | 0.0% (0/259) | 480 | 0.0% (0/480) | 100.0% (480/480) | 0.0% (0/480) |
| 20 | 1260 | 0.0% (0/1260) | 100.0% (1260/1260) | 0.0% (0/1260) | 2411 | 0.0% (0/2411) | 100.0% (2411/2411) | 0.0% (0/2411) |
| 21 | 651 | 0.0% (0/651) | 100.0% (651/651) | 0.0% (0/651) | 1250 | 0.0% (0/1250) | 100.0% (1250/1250) | 0.0% (0/1250) |
| 22 | 615 | 0.0% (0/615) | 100.0% (615/615) | 0.0% (0/615) | 1167 | 0.0% (0/1167) | 100.0% (1167/1167) | 0.0% (0/1167) |
| 23 | 1005 | 0.0% (0/1005) | 100.0% (1005/1005) | 0.0% (0/1005) | 1864 | 0.0% (0/1864) | 100.0% (1864/1864) | 0.0% (0/1864) |
| 24 | 585 | 0.0% (0/585) | 100.0% (585/585) | 0.0% (0/585) | 1112 | 0.0% (0/1112) | 100.0% (1112/1112) | 0.0% (0/1112) |
| 25 | 382 | 0.0% (0/382) | 100.0% (382/382) | 0.0% (0/382) | 734 | 0.0% (0/734) | 100.0% (734/734) | 0.0% (0/734) |
| 26 | 481 | 0.0% (0/481) | 100.0% (481/481) | 0.0% (0/481) | 936 | 0.0% (0/936) | 100.0% (936/936) | 0.0% (0/936) |
| 27 | 651 | 0.0% (0/651) | 100.0% (651/651) | 0.0% (0/651) | 1201 | 0.0% (0/1201) | 100.0% (1201/1201) | 0.0% (0/1201) |
| 28 | 566 | 0.0% (0/566) | 100.0% (566/566) | 0.0% (0/566) | 1045 | 0.0% (0/1045) | 100.0% (1045/1045) | 0.0% (0/1045) |
| 29 | 502 | 0.0% (0/502) | 100.0% (502/502) | 0.0% (0/502) | 968 | 0.0% (0/968) | 100.0% (968/968) | 0.0% (0/968) |
| 30 | 502 | 0.0% (0/502) | 100.0% (502/502) | 0.0% (0/502) | 1001 | 0.0% (0/1001) | 100.0% (1001/1001) | 0.0% (0/1001) |
| 31 | 472 | 0.0% (0/472) | 100.0% (472/472) | 0.0% (0/472) | 904 | 0.0% (0/904) | 100.0% (904/904) | 0.0% (0/904) |
| 32 | 723 | 0.0% (0/723) | 100.0% (723/723) | 0.0% (0/723) | 1392 | 0.0% (0/1392) | 100.0% (1392/1392) | 0.0% (0/1392) |
| 33 | 846 | 0.0% (0/846) | 100.0% (846/846) | 0.0% (0/846) | 1599 | 0.0% (0/1599) | 100.0% (1599/1599) | 0.0% (0/1599) |
| 34 | 692 | 0.0% (0/692) | 100.0% (692/692) | 0.0% (0/692) | 1385 | 0.0% (0/1385) | 100.0% (1385/1385) | 0.0% (0/1385) |
| 35 | 287 | 0.0% (0/287) | 100.0% (287/287) | 0.0% (0/287) | 545 | 0.0% (0/545) | 100.0% (545/545) | 0.0% (0/545) |
| 36 | 875 | 0.0% (0/875) | 100.0% (875/875) | 0.0% (0/875) | 1708 | 0.0% (0/1708) | 100.0% (1708/1708) | 0.0% (0/1708) |
| 37 | 727 | 0.0% (0/727) | 100.0% (727/727) | 0.0% (0/727) | 1370 | 0.0% (0/1370) | 100.0% (1370/1370) | 0.0% (0/1370) |
| 38 | 578 | 0.0% (0/578) | 100.0% (578/578) | 0.0% (0/578) | 1130 | 0.0% (0/1130) | 100.0% (1130/1130) | 0.0% (0/1130) |
| 39 | 651 | 0.0% (0/651) | 100.0% (651/651) | 0.0% (0/651) | 1282 | 0.0% (0/1282) | 100.0% (1282/1282) | 0.0% (0/1282) |
| 40 | 1097 | 0.0% (0/1097) | 100.0% (1097/1097) | 0.0% (0/1097) | 2275 | 0.0% (0/2275) | 100.0% (2275/2275) | 0.0% (0/2275) |
| 41 | 532 | 0.0% (0/532) | 100.0% (532/532) | 0.0% (0/532) | 1161 | 0.0% (0/1161) | 100.0% (1161/1161) | 0.0% (0/1161) |
| 42 | 393 | 0.0% (0/393) | 100.0% (393/393) | 0.0% (0/393) | 892 | 0.0% (0/892) | 100.0% (892/892) | 0.0% (0/892) |
| 43 | 626 | 0.0% (0/626) | 100.0% (626/626) | 0.0% (0/626) | 1312 | 0.0% (0/1312) | 100.0% (1312/1312) | 0.0% (0/1312) |
| 44 | 784 | 0.0% (0/784) | 100.0% (784/784) | 0.0% (0/784) | 1519 | 0.0% (0/1519) | 100.0% (1519/1519) | 0.0% (0/1519) |
| 45 | 583 | 0.0% (0/583) | 100.0% (583/583) | 0.0% (0/583) | 1231 | 0.0% (0/1231) | 100.0% (1231/1231) | 0.0% (0/1231) |
| 46 | 599 | 0.0% (0/599) | 100.0% (599/599) | 0.0% (0/599) | 1247 | 0.0% (0/1247) | 100.0% (1247/1247) | 0.0% (0/1247) |
| 47 | 545 | 0.0% (0/545) | 100.0% (545/545) | 0.0% (0/545) | 1136 | 0.0% (0/1136) | 100.0% (1136/1136) | 0.0% (0/1136) |
| 48 | 739 | 0.0% (0/739) | 100.0% (739/739) | 0.0% (0/739) | 1477 | 0.0% (0/1477) | 100.0% (1477/1477) | 0.0% (0/1477) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 8; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (8/8).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/8).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (8/8).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: az Ezékielben nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–Ezsd menetekben); a versbeosztás a detektor szerint tiszta.
- A régi arany (2.2) 8 hármasa mind egyezik (8/8); kis minta.

## 4. Kiegészítések ebben a menetben

- K9: az Ez bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag` (`claude/f22-ez`), `kovetkezo`, `ir`, D23, v2.17.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_Ez.md`.
- Az Ezsd-ág (`claude/f22-ezsd`) és az Ez-ág PR-ja még nincs; az Ez-ág az Ezsd-ágra épül.
- A korábbi kézi átnézések (1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1) továbbra is a felhasználóé.
- A következő könyv indítása a felhasználó döntése (⛔ 2.). A DT57 (1) mérése szerint a Jób (159) és a Péld (145) maradt a mért listából; a Jób előtt a versmegfeleltetés (#83, TAHOT-hiány Jób 40:1–5, 41) és döntés az 1:2 / 2:1 támogatásról.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Ez.md`)

Az ellenőr eltérést nem talált (TISZTA). A számokat pontos könyvegyezéssel (Grep `\tapi_termeles/high/Ez\t`, `cimke=ez`, `^Ez `, `Ez_k*.json`) és `lekerdez.py`-jal igazolta; a laza „Ez” előtag a futásnaplóban 324 sort adna (146 Ez + 145 Ézs + 33 Ezsd), a jelentés számai csak az Ez-sorokat tartalmazzák. A szkripteket (`egyesit.py`, `f22_statisztika.py`, `f22_elemzes.py`) nem futtathatta. A saját CI-futásában HIBA szintű találat nincs.

- **Régi arany:** a 8 `Ezk.` hármas (H8415, H7585) mind a várt Károli-szónál áll a `parok_Ez.tsv`-ben (8/8).
- **Strong a TAHOT-ból:** Ez 1:1, 34:22 (a javított k088-ból) és 48:35 mintavétele 57/57 er-tokenen egyezik.
- **Merge-sorrend:** az Ez-ág az Ezsd-commitokat is hordozza, ezért az Ezsd-PR előbb vagy együtt merge-elendő; szöveges ütközés a main-nel nem várható.
- **Tájékoztató:** a `szavak_Ez.tsv`-ben a `\tmagas\t` minta 15 hamis pozitívot ad (a magyar „magas” szó a `szo` oszlopban); bizonyosság szerinti számlálásnál oszlopra kell horgonyozni.
