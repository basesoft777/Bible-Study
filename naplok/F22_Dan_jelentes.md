# F22_Dan_jelentes.md — Károli–Strong párosítás: Dániel (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Dán`, `egyesit.py --konyv Dán` és `--ellenoriz`, `f22_elemzes.py --konyv Dán`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Dan-soraiból: `futas = api_termeles/high/Dan`, `cimke = dan`, a `f22/api_termeles/high/_munka/Dan_k*.json` hibaüzenetei). Ág: `claude/f22-dan` (a main `fb31802e` commitjáról; az 1Kir PR #274, a Neh PR #275 és a 2Kir PR #277 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026.10.09) szerint a Dán (1644 előfordulás, 312 NINCS-szócikk) a leghasznosabb hiányzó könyv; a 2Kir után a BDB-mérés szerinti, beolvasztás nélküli tiszta jelöltek elfogytak. A korábban említett 37 detektorsor az F85.6/F85.8 óta nincs meg (`f22/versmegfeleltetes.tsv`: 0 Dán-sor); a detektort 2026.10.11-én újrafuttattam ideiglenes könyvtárba, a gépi lista a repóbelivel egyezik. Indítás: felhasználó, chat, 2026.10.11 („mehet a Dániel”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Dán tiszta (357/357 vers, 12 fejezet, eltolt 0), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Dán'`).
- **Minta:** `f22/minta_Dan.tsv`, 357 vers (= a `Karoli_1908.tsv` `Dán ` sorai), 36 köteg (10 vers/köteg, az utolsó 7).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01721UxC8tywyst3ZjmU7aSo`, 36 kérés (2026-10-11T14:06Z); javító kör `msgbatch_01BtMfCjHS63oJ8Wehzu8taS`, 4 kérés (14:10Z).
- **Futásnapló** (Dan: 40 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 36 | 32 | 4 köteg (7 vers) | 2,5710 | 431 629 / 427 873 |
| 2. próba (javító) | 4 | 4 | 0 | 0,1096 | 60 414 / 9 835 |
| **összesen** | 40 | | | **2,6806** | |

A javító körbe került kötegek: 8 (1 vers), 12 (4 vers), 13 (1 vers), 21 (1 vers); formátumhibás egész köteg nincs.

A könyvplafonból (357 × 0,0074 × 1,5 = 3,96 USD) 2,68 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 76,6408 USD (Ézs–2Kir 73,9602 + Dán 2,6806), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0075 USD (a plafon alapja 0,0074 fölött).

## 1a. Szkriptkimenet

```
Sonnet: 36 köteg, 357 vers; kapuhiba első próbára 2.0% (7/357); végleg 0.0% (0/357)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Dán`: `parok_Dan.tsv` 9 499 link (mind `alacsony`, `S`), `szavak_Dan.tsv` 18 377 token. A szavak bontása: hu 8 848 (7 357 `parositva`, 1 491 `betoldas`), er 9 529 (8 766 `parositva`, 763 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Dán ` sorainak száma (9 529). Az átnézési sor (`naplok/F22_Dan_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Dán --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Dán` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/9499), alacsony 100.0% (9499/9499), kezi 0.0% (0/9499); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/18377), alacsony 100.0% (18377/18377), kezi 0.0% (0/18377).

Link-forrás megoszlás (parok): S 9499. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 357 (Dán 10:1, Dán 10:10, Dán 10:11, Dán 10:12, Dán 10:13, Dán 10:14, Dán 10:15, Dán 10:16, Dán 10:17, Dán 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 478 | 0.0% (0/478) | 100.0% (478/478) | 0.0% (0/478) | 977 | 0.0% (0/977) | 100.0% (977/977) | 0.0% (0/977) |
| 2 | 1315 | 0.0% (0/1315) | 100.0% (1315/1315) | 0.0% (0/1315) | 2484 | 0.0% (0/2484) | 100.0% (2484/2484) | 0.0% (0/2484) |
| 3 | 937 | 0.0% (0/937) | 100.0% (937/937) | 0.0% (0/937) | 1805 | 0.0% (0/1805) | 100.0% (1805/1805) | 0.0% (0/1805) |
| 4 | 1012 | 0.0% (0/1012) | 100.0% (1012/1012) | 0.0% (0/1012) | 1915 | 0.0% (0/1915) | 100.0% (1915/1915) | 0.0% (0/1915) |
| 5 | 852 | 0.0% (0/852) | 100.0% (852/852) | 0.0% (0/852) | 1687 | 0.0% (0/1687) | 100.0% (1687/1687) | 0.0% (0/1687) |
| 6 | 822 | 0.0% (0/822) | 100.0% (822/822) | 0.0% (0/822) | 1577 | 0.0% (0/1577) | 100.0% (1577/1577) | 0.0% (0/1577) |
| 7 | 759 | 0.0% (0/759) | 100.0% (759/759) | 0.0% (0/759) | 1435 | 0.0% (0/1435) | 100.0% (1435/1435) | 0.0% (0/1435) |
| 8 | 632 | 0.0% (0/632) | 100.0% (632/632) | 0.0% (0/632) | 1254 | 0.0% (0/1254) | 100.0% (1254/1254) | 0.0% (0/1254) |
| 9 | 814 | 0.0% (0/814) | 100.0% (814/814) | 0.0% (0/814) | 1543 | 0.0% (0/1543) | 100.0% (1543/1543) | 0.0% (0/1543) |
| 10 | 541 | 0.0% (0/541) | 100.0% (541/541) | 0.0% (0/541) | 1034 | 0.0% (0/1034) | 100.0% (1034/1034) | 0.0% (0/1034) |
| 11 | 1058 | 0.0% (0/1058) | 100.0% (1058/1058) | 0.0% (0/1058) | 2095 | 0.0% (0/2095) | 100.0% (2095/2095) | 0.0% (0/2095) |
| 12 | 279 | 0.0% (0/279) | 100.0% (279/279) | 0.0% (0/279) | 571 | 0.0% (0/571) | 100.0% (571/571) | 0.0% (0/571) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12.

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

- Nincs: a Dánielben nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2): a könyvben nincs hármas, ezért nincs mért érték.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.
- A könyv arámi része (Dán 2:4b–7:28) is ugyanazzal a TAHOT-alapú tokenezéssel és a `prompt_v3`-mal futott; külön nyelvi ellenőrzés nem készült, a szúrópróba (22.6) elmarad (DT70).

## 4. Kiegészítések ebben a menetben

- K9: a Dán bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D33, v2.27.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv a felhasználó döntése: az ÓSZ-ből még 16 könyv hiányzik (Ruth, Préd, Én, Sir, Hós, Jóel, Ámós, Abd, Jón, Mik, Náh, Hab, Sof, Hag, Zak, Mal; együtt 1 625 vers); a detektor szerint a Hós (1:11, 11:11) és a Préd (2:26) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ezeknél kézi átnézési pont várható; a többi 14 kis könyv tiszta.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Dan.md`)

Az ellenőr a számszerű állításokat (357/357, 9 499 / 18 377, 7/357 → 0, 2,6806 USD, 76,6408 USD, a futó összeg folytonossága) saját lekérdezéssel igazolta; 1 eltérés:

- **A 16 kis könyv „mind tiszta” állítása pontatlan volt:** az `f22/versosszevonas.tsv` három jóváhagyott 2:1 beolvasztást rögzít a Hóseásban (1:11, 11:11) és a Prédikátorban (2:26); ezek a korábbi könyvekben kézi átnézési pontot adtak. A brief `kovetkezo` mezőjében és az 5. szakaszban javítva.
- Megfigyelés (nem eltérés): a Dán 3:1 „arany” (hu 5) szava a H1768 (er 6) tokenhez is kapcsolódik, nem csak a H1722-höz; modell-kimenet, `alacsony`, kézi átnézésre nem jelölt.

