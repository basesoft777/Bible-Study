# F22_Hos_jelentes.md — Károli–Strong párosítás: Hóseás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Hós`, `egyesit.py --konyv Hós` és `--ellenoriz`, `f22_elemzes.py --konyv Hós`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Hos-soraiból: `futas = api_termeles/high/Hos`, `cimke = hos`, a `f22/api_termeles/high/_munka/Hos_k*.json` hibaüzenetei). Ág: `claude/f22-hos` (külön worktree, a main `5ce1fd8e` commitjáról; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277, a Dán PR #279, a Ruth PR #280, a Jón PR #281, a Náh PR #283, a régi-arany PR #284, a Préd PR #285, az Abd PR #286 és a Zak PR #289 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a hiányzó kis könyvek egyike (195 vers); a választás a felhasználóé. A könyv előzetes elemzése (kulcsok, tokenmérleg, a két beolvasztás szóhatára) a sessionben készült, és egy független másik session is igazolta. Indítás: a felhasználó chat-üzenete („nézzük meg mi a gond a hoseással”, majd a Hóseás elemzése után a továbbított „mehet a Hóseás” és a felhasználó „mindent fogadj el amit a session küld” utasítása, 2026.10.11).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Hós 195/195 vers, 14 fejezet, eltolt 0, a gépi listákban (`versmegfeleltetes.tsv`, `versmegfeleltetes_kezi.tsv`) nincs sora; **két jóváhagyott beolvasztás van** (`f22/versosszevonas.tsv`, a felhasználó jóváhagyása 2026.10.09, F85.4 és F85.10, DT92): a Hós 1:11 23–30. szava = TAHOT 2:1 (saját er 23 + beolvasztott 11), a Hós 11:11 22–40. szava = TAHOT 12:1 (saját er 19 + beolvasztott 20). Szimuláció: nyers 3 581 token = fő 3 550 + extra 31; a leképezett kulcshalmaz = a Károli-kulcshalmaz. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Hós'`).
- **Minta:** `f22/minta_Hos.tsv`, 195 vers (= a `Karoli_1908.tsv` `Hós ` sorai), 20 köteg (10 vers/köteg, az utolsó 5).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01F7Yu1QhP7GLm6FfnJmeDFs`, 20 kérés (2026-10-11T17:54Z); javító kör `msgbatch_019byn3Bw1nrtGyPi7h6U3za`, 2 kérés (17:57Z).
- **Futásnapló** (Hos: 22 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 20 | 18 | 2 köteg (2 vers) | 0,8932 | 200 245 / 138 586 |
| 2. próba (javító) | 2 | 2 | 0 | 0,0378 | 22 865 / 2 991 |
| **összesen** | 22 | | | **0,9310** | |

A javító körbe került kötegek: 8 és 19 (1-1 vers); formátumhibás egész köteg nincs.

A könyvplafonból (195 × 0,0074 × 1,5 = 2,16 USD) 0,93 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 81,4946 USD (Ézs–Zak 80,5636 + Hós 0,9310), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0048 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer:* a menet saját worktree-ben (`C:\Users\bases\Desktop\Bible-Study-hos`) készült, ahogy a D36 előírja.

## 1a. Szkriptkimenet

```
Sonnet: 20 köteg, 195 vers; kapuhiba első próbára 1.0% (2/195); végleg 0.0% (0/195)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Hós`: `parok_Hos.tsv` 3 711 link (mind `alacsony`, `S`), `szavak_Hos.tsv` 7 291 token. A szavak bontása: hu 3 710 (3 015 `parositva`, 668 `betoldas`, 27 `fuggoben`), er 3 581 (3 383 `parositva`, 167 `forditatlan`, 31 `fuggoben`); az 58 `fuggoben` token (27 hu + 31 er) `kezi` bizonyosságú, mind a két jóváhagyott beolvasztásból való (Hós 1:11: hu 23–30 és a TAHOT 2:1 tokenjei; Hós 11:11: hu 22–40 és a TAHOT 12:1 tokenjei), link nélkül. Az er szám = a `TAHOT_kivonat.tsv` `Hós ` sorainak száma (3 581). Az átnézési sor (`naplok/F22_Hos_atnezes.tsv`): 2 vers (Hós 1:11, Hós 11:11). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Hós --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Hós` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/3711), alacsony 100.0% (3711/3711), kezi 0.0% (0/3711); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/7291), alacsony 99.2% (7233/7291), kezi 0.8% (58/7291).

Link-forrás megoszlás (parok): S 3711. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 195 (Hós 10:1, Hós 10:10, Hós 10:11, Hós 10:12, Hós 10:13, Hós 10:14, Hós 10:15, Hós 10:2, Hós 10:3, Hós 10:4).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 249 | 0.0% (0/249) | 100.0% (249/249) | 0.0% (0/249) | 523 | 0.0% (0/523) | 96.4% (504/523) | 3.6% (19/523) |
| 2 | 503 | 0.0% (0/503) | 100.0% (503/503) | 0.0% (0/503) | 988 | 0.0% (0/988) | 100.0% (988/988) | 0.0% (0/988) |
| 3 | 113 | 0.0% (0/113) | 100.0% (113/113) | 0.0% (0/113) | 233 | 0.0% (0/233) | 100.0% (233/233) | 0.0% (0/233) |
| 4 | 334 | 0.0% (0/334) | 100.0% (334/334) | 0.0% (0/334) | 673 | 0.0% (0/673) | 100.0% (673/673) | 0.0% (0/673) |
| 5 | 265 | 0.0% (0/265) | 100.0% (265/265) | 0.0% (0/265) | 524 | 0.0% (0/524) | 100.0% (524/524) | 0.0% (0/524) |
| 6 | 172 | 0.0% (0/172) | 100.0% (172/172) | 0.0% (0/172) | 334 | 0.0% (0/334) | 100.0% (334/334) | 0.0% (0/334) |
| 7 | 296 | 0.0% (0/296) | 100.0% (296/296) | 0.0% (0/296) | 572 | 0.0% (0/572) | 100.0% (572/572) | 0.0% (0/572) |
| 8 | 227 | 0.0% (0/227) | 100.0% (227/227) | 0.0% (0/227) | 436 | 0.0% (0/436) | 100.0% (436/436) | 0.0% (0/436) |
| 9 | 325 | 0.0% (0/325) | 100.0% (325/325) | 0.0% (0/325) | 632 | 0.0% (0/632) | 100.0% (632/632) | 0.0% (0/632) |
| 10 | 301 | 0.0% (0/301) | 100.0% (301/301) | 0.0% (0/301) | 569 | 0.0% (0/569) | 100.0% (569/569) | 0.0% (0/569) |
| 11 | 221 | 0.0% (0/221) | 100.0% (221/221) | 0.0% (0/221) | 446 | 0.0% (0/446) | 91.3% (407/446) | 8.7% (39/446) |
| 12 | 234 | 0.0% (0/234) | 100.0% (234/234) | 0.0% (0/234) | 458 | 0.0% (0/458) | 100.0% (458/458) | 0.0% (0/458) |
| 13 | 272 | 0.0% (0/272) | 100.0% (272/272) | 0.0% (0/272) | 527 | 0.0% (0/527) | 100.0% (527/527) | 0.0% (0/527) |
| 14 | 199 | 0.0% (0/199) | 100.0% (199/199) | 0.0% (0/199) | 376 | 0.0% (0/376) | 100.0% (376/376) | 0.0% (0/376) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

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

- **Hós 1:11 és Hós 11:11** (`naplok/F22_Hos_atnezes.tsv`): a két jóváhagyott 2:1 beolvasztás; a Károli-vers beolvasztott szakasza (1:11: 23–30. szó, 8 szó; 11:11: 22–40. szó, 19 szó) és a TAHOT-vers tokenjei (11, illetve 20) `kezi` / `fuggoben` állapotúak, link nélkül (a felhasználóé).
- **Régi arany (2.2): 1/1, a `Hos.13.14 H7585` hármas.** A „Seol” a Károli-szövegben és a TAHOT 13:14-ben is kétszer szerepel; a párosítás az elsőt a 3. eredeti tokenre köti (`Hós 13:14`: hu 4 „Seol” → er 3 שְׁאוֹל H7585), a másodikat (hu 22 „oh”, 23 „Seol”) a 17. tokenre (H7585), tehát a hármas a várt (3.) tokenre párosult.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.
- Jelölési pontatlanság (adatot nem érint): a `versosszevonas.tsv` fejléce az `eredeti` címkét „MT-számozásúnak” mondja, de a „Hós 2:1” címke alatti szöveg az MT 2:3-a (KJV-számozás).

## 4. Kiegészítések ebben a menetben

- K9: a Hós bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D42, v2.36.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- Kézi átnézés: Hós 1:11 és Hós 11:11 (3. szakasz).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 9 kis könyv hiányzik (Én, Sir, Jóel, Ámós, Mik, Hab, Sof, Hag, Mal; együtt 797 vers), a detektor szerint mind beolvasztás nélküli; az egylépéses (egy ág, egy PR) futtatásról a felhasználó dönt (D15, DT60).

