# F22_Neh_jelentes.md — Károli–Strong párosítás: Nehémiás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Neh`, `egyesit.py --konyv Neh` és `--ellenoriz`, `f22_elemzes.py --konyv Neh`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Neh-sorainak összesítése (`futas = api_termeles/high/Neh`, `cimke = neh`), a `f22/api_termeles/high/_munka/Neh_k*.json` hibaüzenetei). Ág: `claude/f22-neh` (a main `ae6ee24d` commitjáig beolvasztva, az 1Kir PR #274 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026.10.09) szerint az 1Kir után a tiszta versbeosztású könyvek közül a Neh (479 előfordulás, 96 NINCS-szócikk) a következő. Indítás: felhasználó, chat, 2026.10.11 („mehet a Nehémiás”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Neh tiszta (406/406 vers, 13 fejezet), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Neh'`).
- **Minta:** `f22/minta_Neh.tsv`, 406 vers (= a `Karoli_1908.tsv` `Neh ` sorai), 41 köteg (10 vers/köteg, az utolsó 6).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01Jiyd74KHuNJC8v3jowKste`, 41 kérés (2026-10-11T11:34Z); javító kör `msgbatch_0192dYe83iCeh1vNkf2nrQWE`, 10 kérés (11:39Z).
- **Futásnapló** (Neh: 51 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 41 | 31 | 10 köteg (36 vers) | 2,1674 | 435 544 / 346 369 |
| 2. próba (javító) | 10 | 10 | 0 | 0,2803 | 127 205 / 30 623 |
| **összesen** | 51 | | | **2,4477** | |

A javító körbe került kötegek: 2, 4, 6, 10, 11, 12, 31, 32, 34, 35.

A könyvplafonból (406 × 0,0074 × 1,5 = 4,51 USD) 2,45 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 68,3289 USD (Ézs–1Sám 59,6292 + 1Kir 6,2520 + Neh 2,4477), a globális 110 USD-ből. A Neh-sor `futo_osszeg_usd` oszlopa (62,0769) az 1Kir nélküli ág szerint számolt, ezért a main-nel való beolvasztás után elavult; a beolvasztott sorok értékéhez nem nyúltam. Versenként 0,0060 USD (a plafon alapja 0,0074 alatt).

## 1a. Szkriptkimenet

```
Sonnet: 41 köteg, 406 vers; kapuhiba első próbára 8.9% (36/406); végleg 0.0% (0/406)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Neh`: `parok_Neh.tsv` 8 027 link (mind `alacsony`, `S`), `szavak_Neh.tsv` 16 169 token. A szavak bontása: hu 7 725 (6 326 `parositva`, 1 399 `betoldas`), er 8 444 (7 491 `parositva`, 953 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Neh ` sorainak száma (8 444). Az átnézési sor (`naplok/F22_Neh_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Neh --ellenoriz` (2026.10.11, a main beolvasztása után is): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Neh` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/8027), alacsony 100.0% (8027/8027), kezi 0.0% (0/8027); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/16169), alacsony 100.0% (16169/16169), kezi 0.0% (0/16169).

Link-forrás megoszlás (parok): S 8027. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 406 (Neh 10:1, Neh 10:10, Neh 10:11, Neh 10:12, Neh 10:13, Neh 10:14, Neh 10:15, Neh 10:16, Neh 10:17, Neh 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 321 | 0.0% (0/321) | 100.0% (321/321) | 0.0% (0/321) | 643 | 0.0% (0/643) | 100.0% (643/643) | 0.0% (0/643) |
| 2 | 569 | 0.0% (0/569) | 100.0% (569/569) | 0.0% (0/569) | 1130 | 0.0% (0/1130) | 100.0% (1130/1130) | 0.0% (0/1130) |
| 3 | 659 | 0.0% (0/659) | 100.0% (659/659) | 0.0% (0/659) | 1358 | 0.0% (0/1358) | 100.0% (1358/1358) | 0.0% (0/1358) |
| 4 | 545 | 0.0% (0/545) | 100.0% (545/545) | 0.0% (0/545) | 1083 | 0.0% (0/1083) | 100.0% (1083/1083) | 0.0% (0/1083) |
| 5 | 544 | 0.0% (0/544) | 100.0% (544/544) | 0.0% (0/544) | 1051 | 0.0% (0/1051) | 100.0% (1051/1051) | 0.0% (0/1051) |
| 6 | 482 | 0.0% (0/482) | 100.0% (482/482) | 0.0% (0/482) | 955 | 0.0% (0/955) | 100.0% (955/955) | 0.0% (0/955) |
| 7 | 798 | 0.0% (0/798) | 100.0% (798/798) | 0.0% (0/798) | 1501 | 0.0% (0/1501) | 100.0% (1501/1501) | 0.0% (0/1501) |
| 8 | 522 | 0.0% (0/522) | 100.0% (522/522) | 0.0% (0/522) | 1129 | 0.0% (0/1129) | 100.0% (1129/1129) | 0.0% (0/1129) |
| 9 | 1129 | 0.0% (0/1129) | 100.0% (1129/1129) | 0.0% (0/1129) | 2159 | 0.0% (0/2159) | 100.0% (2159/2159) | 0.0% (0/2159) |
| 10 | 482 | 0.0% (0/482) | 100.0% (482/482) | 0.0% (0/482) | 1022 | 0.0% (0/1022) | 100.0% (1022/1022) | 0.0% (0/1022) |
| 11 | 530 | 0.0% (0/530) | 100.0% (530/530) | 0.0% (0/530) | 1145 | 0.0% (0/1145) | 100.0% (1145/1145) | 0.0% (0/1145) |
| 12 | 694 | 0.0% (0/694) | 100.0% (694/694) | 0.0% (0/694) | 1458 | 0.0% (0/1458) | 100.0% (1458/1458) | 0.0% (0/1458) |
| 13 | 752 | 0.0% (0/752) | 100.0% (752/752) | 0.0% (0/752) | 1535 | 0.0% (0/1535) | 100.0% (1535/1535) | 0.0% (0/1535) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 0; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** n.é. (0/0).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): n.é. (0/0).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): n.é. (0/0).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: a Nehémiásban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2): a könyvben nincs hármas, ezért nincs mért érték.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a Neh bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D31, v2.25.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv a felhasználó döntése; a mérés (2026.10.09) szerinti tiszta jelölt: 2Kir (413 / 87); a Dán (1644 / 312) előtt versbeosztás-döntés kell (37 detektorsor).

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Neh.md`)

Az ellenőr a számszerű állításokat (406/406, 8 027 / 16 169, 36/406 → 0, 2,4477 USD, 68,3289 USD) saját lekérdezéssel igazolta; 3 eltérés:

- **`futo_osszeg_usd` (a naplóban):** a Neh-sorok értéke az 1Kir nélkül számolt (utolsó sor 62,0769, valós 68,3289); a kanonikus napló átírása a felhasználó döntése (DT72), **nyitott**.
- **K9 (`adat/datasetek.tsv`):** a parok-sorok jelentéslistájából hiányzott e jelentés; pótolva.
- **Brief `kovetkezo`:** az ellenőri jelentésre hivatkozott, mielőtt az létezett; a jelentés most megvan.

