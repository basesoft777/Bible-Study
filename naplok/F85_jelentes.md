# F85_jelentes.md — TAHOT_VERSKULCS: az esetlista (1. tétel)

*Feladat: FELADATOK #85 (`F85_TAHOT_VERSKULCS_BRIEF.md`), ág: `claude/tahot-verskulcs`. Állapot: az 1. tétel kész, a ⛔ 1 jóváhagyásra vár (`DONTESEK.md`, DT-F85a). Táblát ez a menet nem írt: a `TAHOT_kivonat.tsv`, az `f22/` és a `parok_*` / `szavak_*` táblák bájtazonosak (git: csak új fájlok).*

*Kimenetek: `naplok/F85_esetlista.tsv` (345 sor), `naplok/F85_macula_elvetve.tsv` (1 fejezet), a generáló `eszkozok/tahot_verskulcs_esetlista.py` (csak olvas; újrafuttatható: `python eszkozok/tahot_verskulcs_esetlista.py`). A szkript és a `F85_macula_elvetve.tsv` nincs a brief `ir` mezőjében — az `ir` kiegészítését a `/befogad`-ra / az orkesztrátorra bízom.*

## 0. Összefoglalás

**Frissítés (F85.3):** az alábbi számok az F85.1 állapotot mutatják; a 3 `valodi_hiany_tahot` sor és a Hós 12:2 a 6. szakasz szerint módosult (új összeg: 328 `eltolas`, 17 `osszevonas_2_1`, 0 `valodi_hiany_tahot`, 4 `bizonytalan`; a B szintű sorok ellenőrzése: 6.3).

`scope=TAHOT_kivonat.tsv teljes ÓSZ (23 213 vers, 39 könyv); Károli_1908 ÓSZ-versei | forras=konkordancia/TAHOT_kivonat.tsv, Macula_heber_*.tsv, KJV_Strongs_teljes.tsv, Karoli_1908.tsv, f22/versmegfeleltetes.tsv, f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv | ts=2026-10-09`

| | darab |
|---|---|
| TAHOT-vers összesen | 23 213 |
| azonos kulcs, igazolt (nincs a listában) | 22 868 (22 827 WLC-vel; 15 alacsony WLC-illeszkedés, de a KJV-tanú azonos kulcson J ≥ 0,6; 26 az Ézs 3-ban, ahol a Macula más Károli-verset ad, de a Károli-oldali hosszkorreláció az azonos kulcsot támogatja: r 0,94 vs. 0,25) |
| azonos kulcs, de alacsony illeszkedés (a listában, `bizonytalan`) | 3 |
| **a listában (TAHOT-oldali sor)** | **345** = 326 `eltolas` + 11 `osszevonas_2_1` + 3 `valodi_hiany_tahot` + 5 `bizonytalan` |
| `osszevonas_1_2` (egy TAHOT-vers több Károli-versben) | 0 |
| `valodi_hiany_karoli` (Károli-vers TAHOT-tartalom nélkül) | 0 |

**A brief háttér-számai újramérve — egyeznek.** Kulcs-szinten 27 TAHOT-kulcs áll Károli-vers nélkül és 18 Károli-vers TAHOT-kulcs nélkül (a brief 27/16 fejezet és 18/6 fejezet számával megegyezően, ugyanazokon a helyeken). Mind a 27 + 18 szerepel az esetlistában (az ellenőrzés a szkript kimenetében: „nincs a listában: []”).

**Átkulcsolásra javasolt: 337 TAHOT-vers** (326 eltolás + 11 összevonás-sor), 9 könyvben:

| könyv | fejezetek | eltolás | összevonás (2:1) |
|---|---|---|---|
| 2Móz | 36 | 38 | — |
| 4Móz | 29–30 | 16 | 2 |
| Jób | 16, 17, 36, 37, 40 | 57 | 4 |
| Péld | 11–12 | 27 | 2 |
| Préd | 1, 2, 8, 9, 10 | 65 | — |
| Én | 6 | 13 | — |
| Ézs | 8, 9, 64 | 29 | 3 |
| Dán | 4 | 37 | — |
| Hós | 2, 12, 13, 14 | 44 | — |
| **össz.** | | **326** | **11** |

Nem átkulcsolásra javasolt (döntés kell): 3 `valodi_hiany_tahot` (Préd 2:25, Hós 2:1, Hós 12:3) és 5 `bizonytalan` (1Sám 14:41, Zsolt 77:11, Ézs 63:19 — alacsony WLC-illeszkedésű azonos kulcs; Ézs 64:1; Hós 12:2).

## 1. Módszer és annak korlátja (proveniencia)

1. **A tartalom MT-párja (Strong-halmaz-illeszkedés).** Könyvenként a TAHOT versfolyamot (kulcs szerint rendezve, a vers = a sorok `H<9000` Strong-halmaza, az elöljáró-kódok `H9xxx` nélkül) monoton igazítottam a Macula (MT/WLC) versfolyamához (Needleman–Wunsch, pontszám = Jaccard − 0,30, sáv ±80 vers; a versszám csak +0,01 döntetlen-feloldó). Az eredmény vers-páronként WLC-Jaccard; a 22 827 azonos kulcsú vers WLC-vel igazolt (J ≥ 0,5; a medián a legtöbb versnél 1,00).
2. **A Károli-oldal.** A Károli-szövegnek nincs teljes Strong-kivonata (`Karoli_Strong_kivonat.tsv`: 383 sor), és a `parok_*` / `szavak_*` táblák Strongja a #22 megfeleltetésen át keletkezett (körkörös), ezért **független Strong-igazolás a Károli-oldalra nincs.** A „melyik Károli-vers” kérdést három forrás adja, külön jelölve a `szint` mezőben:
   - a #22 tényleges K→T táblája (`f22/versmegfeleltetes.tsv` a `versmegfeleltetes_kezi.tsv` javításával, és a `versosszevonas.tsv`): a detektor vershossz-alapú, a kézi sorok emberi jóváhagyásúak (`naplok/F22_versbeosztas_jovahagyas.md`);
   - a Macula `karoli` oszlopa (KK/TVTMS-alapú) — **megbízhatatlannak bizonyult** eltolt régiókban (Ézs 3: 26 versnél tévesen −1; Ézs 9, Én 6, Hós 2 és 12: KJV-számozás, ami nem Károli-számozás), ezért csak támasz, nem döntő;
   - fejezeti log-hossz Pearson-korreláció (Károli szószám vs. TAHOT nem-előtag sorszám), ha a Macula és a #22 eltér (fejezethatáron át nem számolható).
3. **`szint` jelentése** az `igazolas` oszlopban: `A` = a #22 és a Macula egyezik; `B` = a Macula nem ad Károli-verset, csak a #22 hossz-detektor áll mögötte; `H` = a Macula eltér, de a fejezeti hosszkorreláció a #22 mellett dönt (r(#22) ≥ r(Macula) + 0,05); `+kezi` = a pár kézzel jóváhagyott a #22-ben (F22); `ellentmond` = a Macula eltér, és a hossz sem dönt. A TAHOT-oldali Strong-igazolás minden soron ott van (`WLC=… J=…`, `KJV-legjobb=… J=…`).

**Következmény:** a Strong-illeszkedés azt igazolja, hogy a TAHOT-vers tartalma melyik MT/KJV-verssel azonos; hogy ez melyik **Károli**-vers, azt a #22 hossz-detektora és kézi táblája mondja, a Macula `karoli` oszlopa és a hosszkorreláció megerősíti vagy ellentmond. A `B` szintű sorok (41 `eltolas`) csak a #22 detektorán / kézi jóváhagyásán állnak; a `B+kezi` (46) emberi jóváhagyású.

## 2. Szintenkénti bontás (az átkulcsolásra javasolt 337 sor)

| szint | sor | könyvek |
|---|---|---|
| A (#22 = Macula) | 161 | Dán 37, Préd 65, Jób 44, Hós 12, 4Móz 1, Péld 1, Ézs 1 |
| H (hossz a #22 mellett, a Macula ellenében) | 85 | 2Móz 29, Ézs 25, Hós 21, Én 10 |
| B (csak #22-detektor) | 41 | 4Móz 16, Hós 11, 2Móz 9, Én 3, Ézs 2 |
| B+kezi / H+kezi (kézzel jóváhagyott a #22-ben) | 50 | Péld 28, Jób 17, 4Móz 1, Ézs 4 |

## 3. Amit a mérés a #22 tábláiról elárult (hatókörön kívül, jelzés)

- **Hós 12:1–3 (a #22 detektor listája szerint hiányos).** A tábla K 12:1 → T 12:1 és K 12:2 → T 12:2 azonosságot ad, T 12:3-at pedig `nincs_karoli`-nak jelöli, és csak K 12:3-tól (→ T 12:4) tolja el. A Macula és a fejezeti hosszkorreláció (r(azonos) = −0,09, r(Macula) = 0,89) is azt mutatja, hogy K 12:n = T 12:(n+1) a fejezet elejétől (a Károli 11. fejezete 12 versű). A Hós a #22-ben még nem futott; a tábla javítása (kézi sor) külön döntés (lásd DT-F85a (3)).
- **Hós 2:1 és Préd 2:25:** a TAHOT-versnek a #22 szerint nincs Károli-megfelelője (`nincs_karoli`); a tartalom WLC-vel igazolt (Hós 2:1 = MT 2:3, Préd 2:25 = MT 2:25). Nem derül ki gépileg, hogy a Károli egy szomszédos versbe vonta-e (2:1) vagy a szöveg a Károliban nincs meg — ezt nem töltöm ki (3. szabály).
- A Macula `karoli` oszlop hibái (Ézs 3; Ézs 9; Én 6; Hós 2, 12) a `F85_macula_elvetve.tsv`-ben és az `igazolas` mezőkben dokumentáltak; javasolt nyitott tétel: N-F85a (a Macula `karoli` oszlop eltolt régióinak javítása vagy jelölése, külön feladat — nem része a #85-nek).

## 4. Fejezethatáron át ható ütközés-kockázat

Az átkulcsolás után két különböző tartalmú TAHOT-vers kerülhet ugyanarra a kulcsra, ha egy TAHOT-vers Károli-megfelelő nélkül marad (3 eset: Préd 2:25, Hós 2:1, Hós 12:3) és a kulcsa egy átkulcsolt vers új kulcsával egyezik (pl. Hós 12:3: a T 12:4 → K 12:3 ugyanezt a kulcsot kapja). Ezért a „marad a régi kulcson” opció nem biztonságos; ld. DT-F85a (2).

## 5. A következő lépés

A ⛔ 1 megállás: a felhasználó jóváhagyása (DT-F85a), utána 3. tétel (átkulcsolás-szkript). A futtatás sorrendje a #22 Péld-menetéhez képest a felhasználó döntése (a brief `kovetkezo` mezője szerint); a Péld 11:31/12:1 és 12:1–28 sorai is az átkulcsolt halmazban vannak.

## 6. F85.3 — a 3 `valodi_hiany_tahot` sor fejezeten átnyúló újramérése, a Hós 12 és a B szintű sorok ellenőrzése

*Szkript: `eszkozok/tahot_verskulcs_finomit.py` (az esetlista-szkript kimenetét finomítja; mindkettő csak olvas, idempotens; sorrend: előbb `tahot_verskulcs_esetlista.py`, utána `tahot_verskulcs_finomit.py`). A `F85_esetlista.tsv` három új oszlopot kapott (`b_ellenorzes`, `szoveg_olvasas`, `megjegyzes`), a B sorok jelei a `naplok/F85_b_ellenorzes.tsv`-ben vannak. A `TAHOT_kivonat.tsv`, az `f22/` és a `parok_*` táblák nem változtak. Kulcsba `-MT`-féle utótagot nem javaslok (a `parse_igehely` nem fogadja); jelölés kell-e: külön oszlop.*

`scope=Préd 1–3, Hós 1–3 és 11–13: Károli- és TAHOT-versszámok, Károli-szószám (tokenek.tokenizal) és TAHOT nem-előtag sorszám, a Károli-szöveg és a TAHOT-glossza összevetése; B sorok: KJV-tanú, TVTMS-sor, hossz | forras=konkordancia/Karoli_1908.tsv, TAHOT_kivonat.tsv, Macula_heber_*.tsv, KJV_Strongs_teljes.tsv, Karoli_versmegfeleltetes.tsv | ts=2026-10-09`

### 6.1 A három „hiány” nem hiány: mind 2:1 összevonás (a Károli egy versbe vonta)

| TAHOT-vers | Károli | típus | indok |
|---|---|---|---|
| Préd 2:25 (+ partner Préd 2:26) | Préd 2:26 | `osszevonas_2_1` | A Préd 2 mindkét oldalon 26 verses, de a Préd 1:18 → Károli 2:1 miatt K 2:n = T 2:(n−1) a 2:25-ig. A K 2:26 (51 szó) 1–8. szava („Mert kicsoda ehetnék és élhetne gyönyörűségére rajtam kivül”) = T 2:25 („for who will he eat who will enjoy outside from”), a 9–51. szó = T 2:26. Szóarány 51 / (7 + 22) = 1,76 (a könyv mediánja 1,58). |
| Hós 2:1 (+ partner Hós 1:11) | Hós 1:11 | `osszevonas_2_1` | A K 1:11 (30 szó) 23–30. szava („Mondjátok atyátokfiainak: Ammi! és a ti húgaitoknak: Rukhámáh”) = T 2:1 („say brothers people sisters shown compassion”). Szóarány 30 / (16 + 5) = 1,43. Utána K 2:n = T 2:(n+1) (a #22 táblában ez már így van). |
| Hós 12:1 (+ partner Hós 11:11) | Hós 11:11 | `osszevonas_2_1` | A K 11:11 (40 szó) 22–40. szava („Körülvett engem Efraim hazugsággal, az Izráel háza pedig csalárdsággal, de Júda uralkodik még az Istennel és a hűséges Szenttel”) = T 12:1 („surrounded lying Ephraim deceit house of Israel Judah still roamed with God … holy faithful”). Szóarány 40 / (11 + 14) = 1,60. K 11:12 nincs (a Károli Hós 11 11 verses). |
| Hós 12:3 | Hós 12:2 | `eltolas` | K 12:2 „Pere van az Úrnak a Júdával is…” = T 12:3 „a case at law Yahweh with Judah…”. |
| Hós 12:2 | Hós 12:1 | `eltolas` | K 12:1 „Széllel táplálkozik Efraim…” = T 12:2 „Ephraim feeding wind…”. |

**Igazolás szintje:** a TAHOT-oldali Strong-illeszkedés WLC-vel megvan (J = 0,92–1,00); a Károli-oldalon Strong-igazolás nincs. A döntő jel a **szövegtartalom** (a Károli-szakasz és a TAHOT-glossza kézi, soronkénti összevetése — ezért `szint=S`, megerősítést kér) és a szóarány. Az esetlista frissült: a 3 `valodi_hiany_tahot` és a Hós 12:2 `bizonytalan` sor megszűnt; helyettük 6 új `osszevonas_2_1` sor (3 extra + 3 partner) és 2 `eltolas` (Hós 12:2, 12:3). **Új összeg: 328 `eltolas`, 17 `osszevonas_2_1`, 0 `valodi_hiany_tahot`, 4 `bizonytalan` (1Sám 14:41, Zsolt 77:11, Ézs 63:19, Ézs 64:1), 0 `valodi_hiany_karoli`.**

### 6.2 A Hós 12:1–3 helyes megfeleltetése és a kézi tábla javítási javaslata (a fájlokat nem írtam)

Helyes: Károli 11:11 = T 11:11 + T 12:1; K 12:n = T 12:(n+1) (n = 1…14). A mai tábla K 12:1 → T 12:1 és K 12:2 → T 12:2 azonosságot ad (téves), T 12:3-at `nincs_karoli`-nak jelöli, és csak K 12:3-tól (→ T 12:4) tolja el. Javasolt sorok (a detektor `Hós 12:3 nincs_karoli` sorát az azonos `eredeti`jű `eltolt` sor kiváltja, a K 12:3→T 12:4 stb. sorok már jók):

```
f22/versmegfeleltetes_kezi.tsv (javaslat):
Hós 12:1	Hós 12:2	eltolt
Hós 12:2	Hós 12:3	eltolt
	Hós 12:1	nincs_karoli

f22/versosszevonas.tsv (javaslat; a hu_tol/hu_ig a tokenek.tokenizal sorszáma):
Hós 11:11	22	40	Hós 12:1	a Károli 11:11 „Körülvett engem Efraim … a hűséges Szenttel” része (22–40. szó) = a TAHOT 12:1 (2:1)
```

Ugyanígy a másik két összevonásra (a megfelelő #22 könyv-menetben): `Hós 1:11 23 30 Hós 2:1` és `Préd 2:26 1 8 Préd 2:25` (mindkettő `nincs_karoli` sora a detektor listájában megvan). A Hós és a Préd a #22-ben még nem futott (a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` nem tartalmazza), ezért e sorok futott könyvet nem érintenek.

### 6.3 A 41 B szintű sor (csak #22-detektor) független ellenőrzése

Jelek soronként (`naplok/F85_b_ellenorzes.tsv`): **kjv** (a Károli-vers `igehely_kjv` megfelelőjének Strong-Jaccardja a TAHOT-verssel, ≥ 0,5: +1), **tvtms** (az `osztaly=MT` sor MT-száma egyezik-e a WLC-vel igazolt MT-verssel), **hossz** (a Károli/TAHOT szóarány eltérése a könyv mediánjától a javasolt párosításnál vs. az azonos kulcsú Károli-versnél; a −1 rövid versekben zajos, nem blokkol), és külön, a gépi osztályozást nem módosító **szövegolvasás** (a Károli-vers és a TAHOT-glossza kézi egyezése; 33 sort olvastam végig, 8 4Móz-sort nem). Gépi osztály: igazolt = legalább 2 jel +1; ellentmond = kjv vagy tvtms −1; egyébként nem igazolt.

| könyv | sor | gépi: igazolt | gépi: nem igazolt | gépi: ellentmond | szövegolvasás: egyezik / nem olvasott |
|---|---|---|---|---|---|
| 2Móz 36 | 9 | 0 | 9 | 0 | 9 / 0 |
| 4Móz 30 | 16 | 12 | 4 | 0 | 8 / 8 |
| Hós (2:23, 13:16, 14:1–9) | 11 | 0 | 11 | 0 | 11 / 0 |
| Én 6 | 3 | 0 | 3 | 0 | 3 / 0 |
| Ézs (8:23, 64:12) | 2 | 0 | 1 | 1 | 2 / 0 |
| **össz.** | **41** | **12** | **28** | **1** | **33 / 8** |

- **Igazolt (12):** mind a 4Móz 30-ban (KJV-tanú J = 0,55–0,90 + hossz).
- **Nem igazolt (28):** nincs gépi jel, de nincs is ellenjel: a 2Móz 36 (9), Hós (11) és Én 6 (3) sorokra a `Karoli_versmegfeleltetes` nem ad KJV/TVTMS-megfelelőt (KEZI-osztály vagy hiányzik), a 4Móz 30 négy sorában (30:5, 10, 13, 15) a KJV-tanú +1 vagy 0, a hossz 0. **Mind a 28 sornál a szövegolvasás egyezik** (az eltolást támogatja); gépi igazolásnak ez nem számít.
- **Ellentmond (1):** Ézs 8:23 → K 9:1. A `Karoli_versmegfeleltetes` Ézs 9:1 sora MT 9:1-et ad (tvtms = −1), a KJV-tanú viszont +1 (J = 0,84) és a szövegolvasás is egyezik (K 9:1 „…Zebulon és Nafthali földjét…” = T 8:23 „…Zebulun … Naphtali…”). A TVTMS-tábla sora ezen a ponton hibásnak látszik (a KJV 9:1 = MT 8:23); a sort az eltolás javára értékelem, a döntés a felhasználóé.
- **Egyetlen sor sem mutat a javasolt eltolás ellen** (kjv −1: 0 sor; tvtms −1: 1 sor, a fenti TVTMS-hiba; szövegolvasás: 33 / 33 egyezik).

**Korlát:** a Károli-oldalon továbbra sincs független Strong-jel. A KJV-tanú a Károli-versnek a TVTMS-táblán át kapott KJV-megfelelőjére támaszkodik (az is származtatott tábla); a szövegolvasás kézi értelmezés, nem lekérdezés — ezért marad „nem igazolt” a gépi besorolás, ahol csak az olvasás áll mögötte.
