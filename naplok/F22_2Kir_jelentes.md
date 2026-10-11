# F22_2Kir_jelentes.md — Károli–Strong párosítás: 2Királyok (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Kir`, `egyesit.py --konyv 2Kir` és `--ellenoriz`, `f22_elemzes.py --konyv 2Kir`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Kir-sorainak összesítése (`futas = api_termeles/high/2Kir`, `cimke = 2kir`), a `f22/api_termeles/high/_munka/2Kir_k*.json` hibaüzenetei). Ág: `claude/f22-2kir` (a main `6c1acf69` commitjáról; az 1Kir PR #274 és a Neh PR #275 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026.10.09) szerint a Neh után a tiszta versbeosztású könyvek közül a 2Kir (413 előfordulás, 87 NINCS-szócikk) a következő. Indítás: felhasználó, chat, 2026.10.11 („mehet a 2Királyok”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a 2Kir tiszta (719/719 vers, 25 fejezet), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Kir'`).
- **Minta:** `f22/minta_2Kir.tsv`, 719 vers (= a `Karoli_1908.tsv` `2Kir ` sorai), 72 köteg (10 vers/köteg, az utolsó 9).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_017TF87vEB2ZVZNxoXErcq1Q`, 72 kérés (2026-10-11T12:16Z); javító kör `msgbatch_014Qio2csrro9dKS8GK33HxP`, 12 kérés (12:20Z).
- **Futásnapló** (2Kir: 84 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 72 | 60 | 12 köteg (21 vers) | 5,2950 | 869 286 / 885 139 |
| 2. próba (javító) | 12 | 12 | 0 | 0,3363 | 175 020 / 32 263 |
| **összesen** | 84 | | | **5,6313** | |

A javító körbe került kötegek: 4, 5, 6, 7, 18, 21, 27, 28, 29, 38, 44, 47.

A könyvplafonból (719 × 0,0074 × 1,5 = 7,98 USD) 5,63 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 73,9602 USD (Ézs–Neh 68,3289 + 2Kir 5,6313), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0078 USD (a plafon alapja 0,0074 fölött).

## 1a. Szkriptkimenet

```
Sonnet: 72 köteg, 719 vers; kapuhiba első próbára 2.9% (21/719); végleg 0.0% (0/719)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Kir`: `parok_2Kir.tsv` 18 184 link (mind `alacsony`, `S`), `szavak_2Kir.tsv` 36 736 token. A szavak bontása: hu 18 102 (14 668 `parositva`, 3 434 `betoldas`), er 18 634 (16 625 `parositva`, 2 009 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `2Kir ` sorainak száma (18 634). Az átnézési sor (`naplok/F22_2Kir_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv 2Kir --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Kir` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/18184), alacsony 100.0% (18184/18184), kezi 0.0% (0/18184); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/36736), alacsony 100.0% (36736/36736), kezi 0.0% (0/36736).

Link-forrás megoszlás (parok): S 18184. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 719 (2Kir 10:1, 2Kir 10:10, 2Kir 10:11, 2Kir 10:12, 2Kir 10:13, 2Kir 10:14, 2Kir 10:15, 2Kir 10:16, 2Kir 10:17, 2Kir 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 576 | 0.0% (0/576) | 100.0% (576/576) | 0.0% (0/576) | 1080 | 0.0% (0/1080) | 100.0% (1080/1080) | 0.0% (0/1080) |
| 2 | 650 | 0.0% (0/650) | 100.0% (650/650) | 0.0% (0/650) | 1299 | 0.0% (0/1299) | 100.0% (1299/1299) | 0.0% (0/1299) |
| 3 | 637 | 0.0% (0/637) | 100.0% (637/637) | 0.0% (0/637) | 1294 | 0.0% (0/1294) | 100.0% (1294/1294) | 0.0% (0/1294) |
| 4 | 1070 | 0.0% (0/1070) | 100.0% (1070/1070) | 0.0% (0/1070) | 2160 | 0.0% (0/2160) | 100.0% (2160/2160) | 0.0% (0/2160) |
| 5 | 783 | 0.0% (0/783) | 100.0% (783/783) | 0.0% (0/783) | 1554 | 0.0% (0/1554) | 100.0% (1554/1554) | 0.0% (0/1554) |
| 6 | 820 | 0.0% (0/820) | 100.0% (820/820) | 0.0% (0/820) | 1667 | 0.0% (0/1667) | 100.0% (1667/1667) | 0.0% (0/1667) |
| 7 | 598 | 0.0% (0/598) | 100.0% (598/598) | 0.0% (0/598) | 1244 | 0.0% (0/1244) | 100.0% (1244/1244) | 0.0% (0/1244) |
| 8 | 783 | 0.0% (0/783) | 100.0% (783/783) | 0.0% (0/783) | 1516 | 0.0% (0/1516) | 100.0% (1516/1516) | 0.0% (0/1516) |
| 9 | 917 | 0.0% (0/917) | 100.0% (917/917) | 0.0% (0/917) | 1917 | 0.0% (0/1917) | 100.0% (1917/1917) | 0.0% (0/1917) |
| 10 | 940 | 0.0% (0/940) | 100.0% (940/940) | 0.0% (0/940) | 1885 | 0.0% (0/1885) | 100.0% (1885/1885) | 0.0% (0/1885) |
| 11 | 504 | 0.0% (0/504) | 100.0% (504/504) | 0.0% (0/504) | 1153 | 0.0% (0/1153) | 100.0% (1153/1153) | 0.0% (0/1153) |
| 12 | 515 | 0.0% (0/515) | 100.0% (515/515) | 0.0% (0/515) | 1080 | 0.0% (0/1080) | 100.0% (1080/1080) | 0.0% (0/1080) |
| 13 | 599 | 0.0% (0/599) | 100.0% (599/599) | 0.0% (0/599) | 1191 | 0.0% (0/1191) | 100.0% (1191/1191) | 0.0% (0/1191) |
| 14 | 690 | 0.0% (0/690) | 100.0% (690/690) | 0.0% (0/690) | 1357 | 0.0% (0/1357) | 100.0% (1357/1357) | 0.0% (0/1357) |
| 15 | 847 | 0.0% (0/847) | 100.0% (847/847) | 0.0% (0/847) | 1607 | 0.0% (0/1607) | 100.0% (1607/1607) | 0.0% (0/1607) |
| 16 | 512 | 0.0% (0/512) | 100.0% (512/512) | 0.0% (0/512) | 1067 | 0.0% (0/1067) | 100.0% (1067/1067) | 0.0% (0/1067) |
| 17 | 1032 | 0.0% (0/1032) | 100.0% (1032/1032) | 0.0% (0/1032) | 2067 | 0.0% (0/2067) | 100.0% (2067/2067) | 0.0% (0/2067) |
| 18 | 948 | 0.0% (0/948) | 100.0% (948/948) | 0.0% (0/948) | 1887 | 0.0% (0/1887) | 100.0% (1887/1887) | 0.0% (0/1887) |
| 19 | 843 | 0.0% (0/843) | 100.0% (843/843) | 0.0% (0/843) | 1673 | 0.0% (0/1673) | 100.0% (1673/1673) | 0.0% (0/1673) |
| 20 | 515 | 0.0% (0/515) | 100.0% (515/515) | 0.0% (0/515) | 1048 | 0.0% (0/1048) | 100.0% (1048/1048) | 0.0% (0/1048) |
| 21 | 614 | 0.0% (0/614) | 100.0% (614/614) | 0.0% (0/614) | 1197 | 0.0% (0/1197) | 100.0% (1197/1197) | 0.0% (0/1197) |
| 22 | 532 | 0.0% (0/532) | 100.0% (532/532) | 0.0% (0/532) | 1096 | 0.0% (0/1096) | 100.0% (1096/1096) | 0.0% (0/1096) |
| 23 | 1102 | 0.0% (0/1102) | 100.0% (1102/1102) | 0.0% (0/1102) | 2298 | 0.0% (0/2298) | 100.0% (2298/2298) | 0.0% (0/2298) |
| 24 | 448 | 0.0% (0/448) | 100.0% (448/448) | 0.0% (0/448) | 905 | 0.0% (0/905) | 100.0% (905/905) | 0.0% (0/905) |
| 25 | 709 | 0.0% (0/709) | 100.0% (709/709) | 0.0% (0/709) | 1494 | 0.0% (0/1494) | 100.0% (1494/1494) | 0.0% (0/1494) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25.

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

- Nincs: a 2Királyokban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2) egyetlen hármasa egyezik (1/1); kis minta.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a 2Kir bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D32, v2.26.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv a felhasználó döntése; a Dán (1644 / 312) előtt versbeosztás-döntés kell (37 detektorsor); további tiszta jelölt a mérés szerint nincs a listán.

