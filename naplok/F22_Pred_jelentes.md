# F22_Pred_jelentes.md — Károli–Strong párosítás: Prédikátor (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Préd`, `egyesit.py --konyv Préd` és `--ellenoriz`, `f22_elemzes.py --konyv Préd`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Pred-soraiból: `futas = api_termeles/high/Pred`, `cimke = pred`, a `f22/api_termeles/high/_munka/Pred_k*.json` hibaüzenetei). Ág: `claude/f22-pred` (külön worktree, a main `7953519e` commitjáról; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277, a Dán PR #279, a Ruth PR #280, a Jón PR #281 és a Náh PR #283 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a hiányzó kis könyvek egyike (221 vers); a választás a felhasználóé. Indítás: felhasználó, chat, 2026.10.11 („mehet a Prédikátor”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Préd 221/221 vers, 12 fejezet, a gépi listában (`versmegfeleltetes.tsv`) nincs sora; **egy jóváhagyott beolvasztás van**: Préd 2:26 1–8. szó = TAHOT 2:25 (`f22/versosszevonas.tsv`, a felhasználó jóváhagyása 2026.10.09, F85.10, DT92). A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Préd'`).
- **Minta:** `f22/minta_Pred.tsv`, 221 vers (= a `Karoli_1908.tsv` `Préd ` sorai), 23 köteg (10 vers/köteg, az utolsó 1).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01J425RvX1sKMLJSf5pdEJNE`, 23 kérés (2026-10-11T16:17Z); javító kör `msgbatch_01VP5r14mBwPc4cdsZr5kQVm`, 4 kérés (16:21Z).
- **Futásnapló** (Pred: 27 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 23 | 19 | 4 köteg (4 vers) | 1,2682 | 236 788 / 206 281 |
| 2. próba (javító) | 4 | 4 | 0 | 0,0781 | 46 953 / 6 234 |
| **összesen** | 27 | | | **1,3463** | |

A javító körbe került kötegek: 1, 2, 9, 15 (1-1 vers); formátumhibás egész köteg nincs.

A könyvplafonból (221 × 0,0074 × 1,5 = 2,45 USD) 1,35 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 79,1039 USD (Ézs–Náh 77,7576 + Préd 1,3463), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0061 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer:* a menet saját worktree-ben (`C:\Users\bases\Desktop\Bible-Study-pred`) készült, ahogy a D36 előírja.

## 1a. Szkriptkimenet

```
Sonnet: 23 köteg, 221 vers; kapuhiba első próbára 1.8% (4/221); végleg 0.0% (0/221)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Préd`: `parok_Pred.tsv` 4 440 link (mind `alacsony`, `S`), `szavak_Pred.tsv` 9 114 token. A szavak bontása: hu 4 659 (3 636 `parositva`, 1 015 `betoldas`, 8 `fuggoben`), er 4 455 (4 062 `parositva`, 384 `forditatlan`, 9 `fuggoben`); a 17 `fuggoben` token mind a Préd 2:26 jóváhagyott beolvasztásából való, `kezi` bizonyosságú (hu 1–8. szó és a TAHOT 2:25 tokenjei, link nélkül). Az er szám = a `TAHOT_kivonat.tsv` `Préd ` sorainak száma (4 455). Az átnézési sor (`naplok/F22_Pred_atnezes.tsv`): 1 vers (Préd 2:26). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Préd --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Préd` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/4440), alacsony 100.0% (4440/4440), kezi 0.0% (0/4440); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/9114), alacsony 99.8% (9097/9114), kezi 0.2% (17/9114).

Link-forrás megoszlás (parok): S 4440. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 221 (Préd 10:1, Préd 10:10, Préd 10:11, Préd 10:12, Préd 10:13, Préd 10:14, Préd 10:15, Préd 10:16, Préd 10:17, Préd 10:2).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 297 | 0.0% (0/297) | 100.0% (297/297) | 0.0% (0/297) | 597 | 0.0% (0/597) | 100.0% (597/597) | 0.0% (0/597) |
| 2 | 615 | 0.0% (0/615) | 100.0% (615/615) | 0.0% (0/615) | 1236 | 0.0% (0/1236) | 98.6% (1219/1236) | 1.4% (17/1236) |
| 3 | 420 | 0.0% (0/420) | 100.0% (420/420) | 0.0% (0/420) | 867 | 0.0% (0/867) | 100.0% (867/867) | 0.0% (0/867) |
| 4 | 310 | 0.0% (0/310) | 100.0% (310/310) | 0.0% (0/310) | 656 | 0.0% (0/656) | 100.0% (656/656) | 0.0% (0/656) |
| 5 | 447 | 0.0% (0/447) | 100.0% (447/447) | 0.0% (0/447) | 865 | 0.0% (0/865) | 100.0% (865/865) | 0.0% (0/865) |
| 6 | 245 | 0.0% (0/245) | 100.0% (245/245) | 0.0% (0/245) | 497 | 0.0% (0/497) | 100.0% (497/497) | 0.0% (0/497) |
| 7 | 466 | 0.0% (0/466) | 100.0% (466/466) | 0.0% (0/466) | 988 | 0.0% (0/988) | 100.0% (988/988) | 0.0% (0/988) |
| 8 | 334 | 0.0% (0/334) | 100.0% (334/334) | 0.0% (0/334) | 666 | 0.0% (0/666) | 100.0% (666/666) | 0.0% (0/666) |
| 9 | 570 | 0.0% (0/570) | 100.0% (570/570) | 0.0% (0/570) | 1182 | 0.0% (0/1182) | 100.0% (1182/1182) | 0.0% (0/1182) |
| 10 | 262 | 0.0% (0/262) | 100.0% (262/262) | 0.0% (0/262) | 551 | 0.0% (0/551) | 100.0% (551/551) | 0.0% (0/551) |
| 11 | 153 | 0.0% (0/153) | 100.0% (153/153) | 0.0% (0/153) | 320 | 0.0% (0/320) | 100.0% (320/320) | 0.0% (0/320) |
| 12 | 321 | 0.0% (0/321) | 100.0% (321/321) | 0.0% (0/321) | 689 | 0.0% (0/689) | 100.0% (689/689) | 0.0% (0/689) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 1; a Károli-szó/kifejezés nem található a vers tokenjei közt: 1.
- **Mért érték (kizárás nélkül, minden link):** 0.0% (0/1).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/1).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): n.é. (0/0).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **Préd 2:26** (`naplok/F22_Pred_atnezes.tsv`): a jóváhagyott 2:1 beolvasztás; a Károli 2:26 1–8. szava és a TAHOT 2:25 tokenjei `kezi` / `fuggoben` állapotúak, link nélkül (a felhasználóé).
- **Régi arany (2.2): 0/1, kulcseltérés a régi arany oldalán.** Az egyetlen hármas az `Ecc.9.10 H7585 „a Seolban”` (STEP-kulcs); a Károli-datasetben a „Seolban” szó a `Préd 9:12`-ben áll (a `Préd 9:10` szövege: „A te ruháid mindenkor legyenek fejérek…”), és a párosítás ezt helyesen köti a H7585-höz (`parok_Pred.tsv`: `Préd 9:12 Seolban → H7585`, a `TAHOT_kivonat.tsv` `Préd 9:12` H7585-tel egyezik). A 0/1 tehát a régi arany kulcsának (STEP/héber-számozás ≠ Károli-számozás) műterméke, nem a párosítás hibája. Javaslat: az `Ecc.9.10` felvétele az `f21p/regi_arany_hibas.tsv`-be, külön tétel (a `Job.17.13` esethez hasonlóan).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a Préd bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D38, v2.32.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- Kézi átnézés: Préd 2:26 (3. szakasz).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 12 kis könyv hiányzik (Én, Sir, Hós, Jóel, Ámós, Abd, Mik, Hab, Sof, Hag, Zak, Mal; együtt 1 224 vers); a Hós (1:11, 11:11) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ott kézi átnézési pont várható; a többi 11 beolvasztás nélküli.

