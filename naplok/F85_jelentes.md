# F85_jelentes.md — TAHOT_VERSKULCS: az esetlista (1. tétel)

*Feladat: FELADATOK #85 (`F85_TAHOT_VERSKULCS_BRIEF.md`), ág: `claude/tahot-verskulcs`. Állapot: az 1. tétel kész, a ⛔ 1 jóváhagyásra és az átkulcsolás (3. tétel) kifejezett engedélyére vár (`DONTESEK.md`, DT-F85a, 🟡). Az átkulcsolás nem indult: a `konkordancia/TAHOT_kivonat.tsv` és a `parok_*` / `szavak_*` táblák bájtazonosak; az `f22/versmegfeleltetes_kezi.tsv` és az `f22/versosszevonas.tsv` az F85.4-ben a Hós 12 javításával bővült (7. szakasz).*

*Kimenetek: `naplok/F85_esetlista.tsv` (349 sor), `naplok/F85_b_ellenorzes.tsv`, `naplok/F85_macula_elvetve.tsv`, a generáló `eszkozok/tahot_verskulcs_esetlista.py` és a finomító `eszkozok/tahot_verskulcs_finomit.py` (mindkettő csak olvas, idempotens; sorrend: előbb az esetlista-szkript, utána a finomító). Mindegyik szerepel a brief `ir` mezőjében (F85.2, F85.3). A független ellenőr jelentése: `naplok/ELLENOR_F85.md`.*

## 0. Összefoglalás

*(Az F85.1 számait az F85.3 és az F85.5 felülírta; az alábbi az aktuális, a `ELLENOR_F85.md` (6) pontjával egyező állapot.)*

`scope=TAHOT_kivonat.tsv teljes ÓSZ (23 213 vers, 39 könyv); Károli_1908 ÓSZ-versei | forras=konkordancia/TAHOT_kivonat.tsv, Macula_heber_*.tsv, KJV_Strongs_teljes.tsv, Karoli_1908.tsv, f22/versmegfeleltetes.tsv, f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv | ts=2026-10-09`

| | darab |
|---|---|
| TAHOT-vers összesen | 23 213 |
| azonos kulcs, igazolt, nincs a listában | 22 864 |
| **az esetlistában (TAHOT-oldali sor)** | **349** = 328 `eltolas` + 17 `osszevonas_2_1` + 4 `bizonytalan` |
| `valodi_hiany_tahot` / `valodi_hiany_karoli` / `osszevonas_1_2` | 0 / 0 / 0 |

**A brief háttér-számai újramérve — egyeznek.** Kulcs-szinten 27 TAHOT-kulcs áll Károli-vers nélkül és 18 Károli-vers TAHOT-kulcs nélkül (a brief 27/16 fejezet és 18/6 fejezet számával megegyezően, ugyanazokon a helyeken). Mind a 27 + 18 szerepel az esetlistában.

**Átkulcsolásra javasolt: 337 TAHOT-vers** (328 eltolás + 9 összevonás-sor, amely kulcsot vált), 9 könyvben. A 349 sorból 12 nem vált kulcsot: 8 összevonás-partner (a közös Károli-kulcsot már viseli) és 4 `bizonytalan`.

| könyv | fejezetek | eltolás | kulcsot váltó összevonás-sor | átkulcsolandó vers |
|---|---|---|---|---|
| 2Móz | 36 | 38 | — | 38 |
| 4Móz | 29–30 | 16 | 1 | 17 |
| Jób | 16, 17, 36, 37, 40 | 57 | 2 | 59 |
| Péld | 11–12 | 27 | 1 | 28 |
| Préd | 1, 2, 8, 9, 10 | 65 | 1 | 66 |
| Én | 6 | 13 | — | 13 |
| Ézs | 8, 9, 64 | 29 | 2 | 31 |
| Dán | 4 | 37 | — | 37 |
| Hós | 2, 12, 13, 14 | 46 | 2 | 48 |
| **össz.** | | **328** | **9** | **337** |

**A „gépi Strong-igazolás” pontos köre.** A gépi Strong-illeszkedés a **TAHOT-oldalra** szól: azt igazolja, hogy a TAHOT-vers tartalma melyik WLC/MT-verssel (és KJV-verssel) azonos. A brief által kért, a **Károli-oldalra** vonatkozó gépi Strong-igazolás nem teljesült: a Károli-szövegnek nincs Strong-kivonata (`Karoli_Strong_kivonat.tsv`: 383 sor), és a `parok_*` táblák Strongja a #22 megfeleltetésén át keletkezett (körkörös). Az „ez a TAHOT-vers ez a Károli-vers” állítás ezért a #22 hossz-detektorán / kézi jóváhagyásán, a Macula `karoli` oszlopán, a hosszkorreláción és (a 41 B sornál, valamint a 8 `szint=S` soron) kézi szövegolvasáson áll — ezek a sorok gépileg nem igazoltak. Az F85.1 commit címében szereplő „gépi Strong-igazolással” kifejezés a TAHOT-oldalra érvényes, a Károli-oldalra túlzás volt (a commit címe nem módosul).

Nem átkulcsolásra javasolt (döntés kell): a 4 `bizonytalan` sor — 1Sám 14:41, Zsolt 77:11, Ézs 63:19 (azonos kulcs, alacsony WLC-illeszkedés), Ézs 64:1 (kézi 2:1 összevonás, nincs WLC-párja).

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

*Az F85.1 állapot; a Hós 12:1–3, Hós 2:1 és Préd 2:25 sorokat a 6. szakasz felülírta (2:1 összevonás / eltolás), a Hós 12 javítása az F85.4-ben megtörtént (7. szakasz).*

- **Hós 12:1–3 (a #22 detektor listája szerint hiányos).** A tábla K 12:1 → T 12:1 és K 12:2 → T 12:2 azonosságot ad, T 12:3-at pedig `nincs_karoli`-nak jelöli, és csak K 12:3-tól (→ T 12:4) tolja el. A Macula és a fejezeti hosszkorreláció (r(azonos) = −0,09, r(Macula) = 0,89) is azt mutatja, hogy K 12:n = T 12:(n+1) a fejezet elejétől (a Károli 11. fejezete 12 versű). A Hós a #22-ben még nem futott; a tábla javítása (kézi sor) külön döntés (lásd DT-F85a (3)).
- **Hós 2:1 és Préd 2:25:** a TAHOT-versnek a #22 szerint nincs Károli-megfelelője (`nincs_karoli`); a tartalom WLC-vel igazolt (Hós 2:1 = MT 2:3, Préd 2:25 = MT 2:25). Nem derül ki gépileg, hogy a Károli egy szomszédos versbe vonta-e (2:1) vagy a szöveg a Károliban nincs meg — ezt nem töltöm ki (3. szabály).
- A Macula `karoli` oszlop hibái (Ézs 3; Ézs 9; Én 6; Hós 2, 12) a `F85_macula_elvetve.tsv`-ben és az `igazolas` mezőkben dokumentáltak; javasolt nyitott tétel (nincs felvéve, helyőrző: N-F85b): a Macula `karoli` oszlop eltolt régióinak javítása vagy jelölése, külön feladat — nem része a #85-nek.

## 4. Fejezethatáron át ható ütközés-kockázat

*Tárgytalan az F85.3 óta: nincs Károli-megfelelő nélküli TAHOT-vers, így megkülönböztetett kulcs nem kell (DT-F85a (2)). A kockázat általános alakja (két tartalom ugyanazon a kulcson) az átkulcsolás-szkript írás előtti összevetésében marad ellenőrzési pont.*

Az átkulcsolás után két különböző tartalmú TAHOT-vers kerülhet ugyanarra a kulcsra, ha egy TAHOT-vers Károli-megfelelő nélkül marad (3 eset: Préd 2:25, Hós 2:1, Hós 12:3) és a kulcsa egy átkulcsolt vers új kulcsával egyezik (pl. Hós 12:3: a T 12:4 → K 12:3 ugyanezt a kulcsot kapja). Ezért a „marad a régi kulcson” opció nem biztonságos; ld. DT-F85a (2).

## 5. A következő lépés

A ⛔ 1 megállás: a felhasználó áttekinti a frissített DT-F85a-t, és kifejezetten engedélyezi a 3. tételt (átkulcsolás-szkript). A futtatás sorrendje a #22 Péld-menetéhez képest a felhasználó döntése (a brief `kovetkezo` mezője szerint); a Péld 11:31/12:1 és 12:1–28 sorai is az átkulcsolt halmazban vannak.

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
- **Ellentmond (1):** Ézs 8:23 → K 9:1. A `Karoli_versmegfeleltetes` Ézs 9:1 sora MT 9:1-et ad (tvtms = −1), a KJV-tanú viszont +1 (J = 0,84) és a szövegolvasás is egyezik (K 9:1 „…Zebulon és Nafthali földjét…” = T 8:23 „…Zebulun … Naphtali…”). A `Karoli_versmegfeleltetes.tsv` (származtatott tábla) MT-oszlopa az Ézs 9 egészében eggyel eltolt, nem csak ebben a sorban — a tábla valószínű hibája (a KJV 9:1 = MT 8:23), nyitott tétel: N-F85a (a #85-ben nem javítom). A sor az esetlistában eltolásként (`eltolas`) szerepel.
- **Egyetlen sor sem mutat a javasolt eltolás ellen** (kjv −1: 0 sor; tvtms −1: 1 sor, a fenti TVTMS-hiba; szövegolvasás: 33 / 33 egyezik).

**Korlát:** a Károli-oldalon továbbra sincs független Strong-jel. A KJV-tanú a Károli-versnek a TVTMS-táblán át kapott KJV-megfelelőjére támaszkodik (az is származtatott tábla); a szövegolvasás kézi értelmezés, nem lekérdezés — ezért marad „nem igazolt” a gépi besorolás, ahol csak az olvasás áll mögötte.

## 7. F85.4–F85.5 — a Hós 12 javítása és a független ellenőr eltéréseinek rendezése

**F85.4 (a felhasználó jóváhagyásával, chat 2026.10.09):** 3 sor került az `f22/versmegfeleltetes_kezi.tsv` végére (`Hós 12:1 → Hós 12:2 eltolt`, `Hós 12:2 → Hós 12:3 eltolt`, `Hós 12:1 nincs_karoli`) és 1 sor az `f22/versosszevonas.tsv` végére (`Hós 11:11 22 40 Hós 12:1`). A detektor `Hós 12:3 nincs_karoli` sorát az azonos `eredeti`jű `eltolt` sor váltja ki (`tokenek._kezi_javitas`). A `Hós 1:11 … Hós 2:1` és `Préd 2:26 … Préd 2:25` összevonás-sor nem került be (saját #22-menetük).

Ellenőrzések (`tokenek` függvényekkel, írás előtt/után; a detektor újragenerálására nem volt szükség, a bemenete nem változott):
- mindkét fájl régi tartalma bájtonként változatlan előtag, a többi sor azonos (kezi 97 → 100 sor, versosszevonas 10 → 11);
- a hatékony K→T tábla (detektor + kézi, minden könyvre) egyetlen különbsége a Hós 12: eltávolított `Hós 12:3 nincs_karoli`, hozzáadott `Hós 12:1 nincs_karoli`, `Hós 12:1→12:2`, `Hós 12:2→12:3`;
- a jóváhagyott (már futtatható) könyvek táblája változatlan; a Hós nincs a `VERSBEOSZTAS_JOVAHAGYOTT`-ban, ezért a `tokenek.betolt_eredeti()` kimenete kulcsról kulcsra azonos (0 változott kulcs);
- az `adat/karoli_strong/parok_*.tsv` és `szavak_*.tsv` (38 fájl) SHA-256-ja változatlan.

**F85.5 (ELLENOR_F85.md eltérései):** E1 — a könyvenkénti hatókör a jelentésben és a DT-F85a (1)-ben az ellenőr (6) pontja szerinti (337 = 328 eltolás + 9 kulcsot váltó összevonás-sor; 2Móz 38, 4Móz 17, Jób 59, Péld 28, Préd 66, Én 13, Ézs 31, Dán 37, Hós 48); E2 — a DT-F85a javaslat-oszlopa és a brief `kovetkezo` mezője: nincs `-MT` utótag, nincs K 11:12, a (2) pont tárgytalan, a Hós 12 külön kezelve; E3 — a `F85_esetlista.tsv` és a `F85_b_ellenorzes.tsv` fejléce a `szoveg_olvasas` oszlopot nevesíti (a `finomit.py` javítva, a TSV-k újragenerálva; az esetlista minden sora 9 mezős); E4 — az `ir`-re vonatkozó állítás a fejlécben pontosítva; E5 — a „gépi Strong-igazolás” köre a 0. szakaszban pontosítva (TAHOT-oldal igen, Károli-oldal nem). Az Ézs 8:23 → Károli 9:1 sor eltolásként szerepel; a `Karoli_versmegfeleltetes.tsv` Ézs 9-es MT-oszlop-eltolása N-F85a helyőrzővel a `NYITOTT_FELADATOK.md`-ben nyitott tétel.

## 8. F85.6 — az átkulcsolás (3. tétel)

*A felhasználó jóváhagyta a DT-F85a döntéseit és az átkulcsolást (chat, 2026.10.09): (1) a, (2) tárgytalan, (3) a 4 `bizonytalan` sor azonos kulcson marad, (4) a (közös Károli-kulcs), (5) engedély. Szkript: `eszkozok/tahot_verskulcs_atkulcsolas.py`; napló: `naplok/F85_kulcsvaltas.tsv` (6 330 sor: fájlbeli sorszám, régi → új kulcs, típus, a sor TAHOT-verse, az összevonás partnere).*

`scope=konkordancia/TAHOT_kivonat.tsv, 337 vers (6 330 sor) a naplok/F85_esetlista.tsv szerint | forras=eszkozok/tahot_verskulcs_atkulcsolas.py, naplok/F85_kulcsvaltas.tsv | ts=2026-10-09`

| könyv | átkulcsolt vers | ebből eltolás | ebből összevonás (kulcsot váltó sor) | átírt sor |
|---|---|---|---|---|
| 2Móz | 38 | 38 | 0 | 781 |
| 4Móz | 17 | 16 | 1 | 405 |
| Jób | 59 | 57 | 2 | 641 |
| Péld | 28 | 27 | 1 | 270 |
| Préd | 66 | 65 | 1 | 1 420 |
| Én | 13 | 13 | 0 | 212 |
| Ézs | 31 | 29 | 2 | 603 |
| Dán | 37 | 37 | 0 | 1 055 |
| Hós | 48 | 46 | 2 | 943 |
| **össz.** | **337** | **328** | **9** | **6 330** |

**Írás előtti ellenőrzés (a szkript leállt volna és nem ír):** a sorok száma azonos (469 301 sor, sorvég: LF, BOM nincs, mind a régi, mind az új fájlban); minden sor az Igehely mezőn kívül bájtra egyezik; a nem érintett sorok teljesen bájtazonosak; a régi → új kulcs leképezés egyértelmű (337 régi kulcs, mindegyik egyetlen új); minden új kulcs létező Károli-vers; csak a 9 összevonó kulcson (4Móz 29:39, Jób 16:22, 36:33, Péld 11:31, Préd 2:26, Ézs 9:20, 64:1, Hós 1:11, 11:11) osztozik két TAHOT-vers; idempotencia-őr (a régi kulcsok jelenléte).

**Utólagos igazolás:**
- a szkriptes bájt-összevetés (HEAD vs. új fájl): 6 330 eltérő sor, pontosan a naplóé (sorszám, régi, új kulcs), csak az első mező; a többi 462 971 sor bájtazonos. (A `git diff --stat` 5 885 sort mutat, mert a Myers-diff a szomszédos, azonosra kulcsolt sorokat összepárosítja; a mérvadó a szkriptes összevetés.)
- `tahot_lefedettseg_ellenoriz.py`: „Fejezet-szinten nincs hiány”, hiányzó fejezet 0.
- `adat/karoli_strong/parok_*.tsv` és `szavak_*.tsv` (38 fájl): a git szerint változatlanok (diff üres), az `adat/`, `f22/` és más `konkordancia/` fájlok sem módosultak.
- **A futtató bemenete a jóváhagyott könyvekre (vers → héber szavak):** a régi hatékony bemenet (régi kulcsok + a #22 detektor/kézi tábla + az összevonás-sorok) és az új nyers kulcsok (`betolt_eredeti(versmegf=False)`) a 17 747 versre mind azonos (Strong, alak, tükörfordítás szerint, 0 eltérés). Vagyis a Károli-kulcs szerinti bemenet változatlan.
- **Ismert következmény (a 4. tétel előtt):** a mai `f22/versmegfeleltetes*.tsv` tábla már az új, Károli-kulcsú TAHOT-ra vonatkozna, ezért a `tokenek.betolt_eredeti()` (versmegf=True) `KeyError: '2Móz 36:38'`-cal leáll, amíg a 4. tétel (a kézi tábla és a detektor-lista kivezetése/újragenerálása) meg nem történik. Ez az ágon várt köztes állapot; a #22 futtatót addig ne indítsd az ágon.
- **Fájlsorrend:** nem változott. A TAHOT-fájl eleve tartalmaz áthelyezett blokkokat (23 törés a Károli-sorrendben, régi = új). Az összevonó kulcsok közül 7-nél a két TAHOT-vers sorai a fájlban folyamatosan következnek; a 4Móz 29:39 / 30:1 és a Hós 11:11 / 12:1 pároknál a második vers a fájl áthelyezett blokkjában áll (a 4Móz 30 és a Hós 12 az áthelyezett részben), így nem szomszédos. A közös kulcson belüli sorrend minden párnál helyes (a Károli-szövegben előbb álló vers sorai a fájlban is előbb állnak, a szkript ezt ellenőrzi), a kulcs szerinti olvasás (`betolt_eredeti`) ezért a helyes sorrendet adja. A fájlsorrendet a megbízás szerint nem módosítottam.
- A 12 nem kulcsot váltó sor (8 összevonás-partner, 4 `bizonytalan`) változatlan; a 4 `bizonytalan` sor azonos kulcson marad, jelzéssel (az esetlistában).

## 9. F85.8 — a 4. tétel (kézi táblák kivezetése) és az utólagos igazolások

*A felhasználó kifejezetten engedélyezte a 4. tételt három feltétellel (az ellenőrző kód a repóba; a párosítás-bemenet igazolása a kézi tábla nélkül; a `tokenek.py` addig nem fut, amíg a 4. tétel módosításai nincsenek commitolva). Szkriptek: `eszkozok/tahot_verskulcs_kivezetes.py` (a kivezetés), `eszkozok/tahot_verskulcs_igazolas.py` (az igazolás; csak olvas); kimenetek: `naplok/F85_kivezetett_sorok.tsv`, `naplok/F85_igazolas.tsv`, `naplok/F85_igazolas.md`. Commit: F85.8 (4. tétel: `0483fd9f`), az igazolás és a dokumentáció a következő commitban.*

### 9.1 A kivezetett sorok

`scope=f22/versmegfeleltetes_kezi.tsv (97 adatsor), f22/versosszevonas.tsv (7 adatsor); a naplok/F85_kulcsvaltas.tsv hivatkozásával | forras=a HEAD~ állapot sorai, naplok/F85_kulcsvaltas.tsv | ts=2026-10-09`

- **Kivezetve 97 kézi adatsor nettó** (az F85.8 pillanatában 104: kézi tábla 97 adatsor + összevonás-fájl 7 adatsor, de az összevonás-sorok az F85.10-ben visszakerültek, +2 új: a `versosszevonas.tsv` 7 → 9 adatsor; a kézi tábla 97 = 87 `eltolt` + 2 Hós 12 `eltolt` (F85.4) + 5 + 1 `nincs_karoli` + 2 `torol`, minden `eltolt`/`nincs_karoli` sor hivatkozott TAHOT-verse átkulcsolt; összevonás-fájl 7 = a 6 régi + a F85.4-ben felvett Hós 11:11). A fejléc- és megjegyzés-sorok maradnak, egy új megjegyzés-sor jelzi a kivezetést. A teljes lista az átkulcsolt eset hivatkozásával: `naplok/F85_kivezetett_sorok.tsv` (soronként: forrásfájl, sor a régi fájlban, Károli-vers, TAHOT-vers, típus, hu_tol/hu_ig, a TAHOT-vers új kulcsa, a `F85_kulcsvaltas.tsv` sora, egyezés, hivatkozás).
- **Ellenőrzés (írás előtt):** a kompenzáló sorok Károli-kulcsa 100 sorban egyezik az átkulcsolt vers új kulcsával, 0 sor nem egyezik, 4 sor olyan TAHOT-versre hivatkozik, amely nem váltott kulcsot (a `torol` párok és az Ézs 64:1). A megmaradó sorok bájtra az eredeti megjegyzés/fejléc sorok.
- **Detektor-lista:** `f22/versmegfeleltetes.tsv` és `naplok/F22_versbeosztas.md` a `versbeosztas.py` újrafuttatásával keletkezett (nem kézzel). Az ÓSZ-ben mind a 39 könyvre `eltolt = 0`, `K-hiány = 0`, `E-hiány = 0` (a Károli- és az eredeti versszám minden ÓSZ-könyvre egyezik); a lista 290 → 12 sor, a 12 az ÚSZ `nincs_eredeti` / `nincs_karoli` sora (változatlanok az előzőhöz képest). (A `versbeosztas.py` a `tokenek` nyers betöltőit használta — `versmegf=False` —, f22-táblát nem töltött be.)
- **Versösszevonás-fájl:** a 7 sor `eredeti` kulcsa az átkulcsolás után eltolt tartalomra mutatott volna (ELLENOR_F85_6 (5b)), és a beolvasztott vers sorai már a közös Károli-kulcson vannak (a beolvasztás kétszer adná a szavakat), ezért a sorok kivezetettek. A vershatár a fájlban az `F85_kulcsvaltas.tsv` `tahot_vers` oszlopából és a fájlsorrendből visszaállítható.

### 9.2 Az igazolások eredménye (`naplok/F85_igazolas.md`)

- **(a) bájt-összevetés** a `8ce6e95c~1` (a4a09ba9, átkulcsolás előtt) és a mostani `TAHOT_kivonat.tsv` között: 469 301 / 469 301 sor (fejléccel); **pontosan 6 330 sor különbözik, mind a `F85_kulcsvaltas.tsv` sorszáma szerint**; csak az Igehely mezőben; a napló régi/új kulcsa minden sorban egyezik a két fájl kulcsával; a többi 462 971 sor bájtazonos.
- **(b) vers → héber szavak** a jóváhagyott könyvekre (a régi pipeline: átkulcsolás előtti TAHOT + f22 táblák; az új: mai TAHOT + kivezetett táblák): **17 747 vers, 0 eltérés** (sorszám, strong, alak, tükörfordítás, TR-jelző), könyvenként 0, közte a 2Móz (1 213 vers) és a Péld (914 vers). A mai pipeline KeyError nélkül betölt; a `versmegfeleltetes()` 0, a `versosszevonasok()` 0 sort ad.
- **(c) `parok_*` / `szavak_*` sorok** (`egyesit.epit()`, memóriában, a táblák nem íródtak): a *régi* pipeline mind a 19 táblapárt a repó adatsoraival **azonosan** reprodukálja (a módszer érvényes); az *új* pipeline **15 könyvre azonos** (1Krón, 1Móz, 1Sám, 2Krón, 2Móz, 2Sám, 3Móz, 5Móz, Bír, Eszt, Ez, Ezsd, Jer, Józs, Zsolt), **4 könyvre (4Móz, Ézs, Jób, Péld) a 2:1 összevonású versekben tér el**: 4Móz 29:39; Ézs 9:20, 64:1; Jób 16:22, 36:33; Péld 11:31 (összesen 6 vers). Az `egyesit.py --ellenoriz` a 2Móz, 4Móz, Ézs, Jób és Péld táblákra az új pipeline-nal „rendben”.
- `adat/` (benne a 38 `karoli_strong` fájl): a git szerint változatlan az átkulcsolás előtti állapothoz képest.

### 9.3 Ami NEM bizonyítható a kézi tábla nélkül (és miért) — döntést/engedélyt kér

A 6 összevont versben a táblák `kezi` állapotú sorai (a Károli-vers `hu_tol`–`hu_ig` szavai és a beolvasztott vers `er` sorai nem párosítottak) az `f22/versosszevonas.tsv` + `tokenek.osszevont_extra()` + `egyesit.epit(kezi_hu=…, extra_er=…)` mechanizmusából jönnek. Az új kulcsokkal a beolvasztott vers tokenjei már a közös kulcson vannak, a mechanizmus pedig a régi (külön) kulcsra épül, ezért az új pipeline ezeket a hu-szavakat nem jelöli `kezi`-nek. A **bemenet** (vers → héber szavak, sorszámmal) azonos (b), a **táblák** 6 versre nem reprodukálhatók az `eszkozok/karoli_strong/tokenek.py` / `egyesit.py` módosítása nélkül — ezek nincsenek a brief `ir` mezőjében, ezért nem nyúltam hozzájuk. A repóbeli táblák változatlanok és (az `--ellenoriz` szerint) konzisztensek az új bemenettel. Javasolt külön lépés (a felhasználó döntése): a `tokenek.osszevont_extra()` / `egyesit` kiegészítése úgy, hogy a közös kulcson a beolvasztott vers tokenjeit a `versosszevonas.tsv` (`karoli`, `hu_tol`, `hu_ig`, a beolvasztott TAHOT-vers száma) alapján jelölje; addig a Hós, Préd, Dán és Én még-nem-futott könyvek 2:1 versei (Hós 1:11 + 2:1, Hós 11:11 + 12:1, Préd 2:25 + 2:26) a közös kulcson egyszerű versként kerülnek párosításra.

### 9.4 Fizikai szomszédosság (az F85.6 jegyzetének megerősítése)

A 9 összevonás-pár közül 7-nél a két TAHOT-vers sorai a fájlban szomszédos blokkok. Két kivétel: **4Móz 29:39 + 30:1** és **Hós 11:11 + 12:1**. Ok: a TAHOT-fájl eleve tartalmaz áthelyezett blokkokat (a Károli-sorrendben 23 törés, régi = új; pl. a 4Móz 30 és a Hós 12 az áthelyezett részben áll), a fájlsorrendet pedig a megbízás szerint nem módosítottam. A kulcs szerinti olvasás (`betolt_eredeti`) a helyes sorrendet adja: a közös kulcson belül a Károli-szövegben előbb álló vers sorai a fájlban is előbb állnak (az átkulcsoló szkript ellenőrzi).

### 9.5 Egyéb

- A `tokenek` modul a 4. tétel módosításainak commitja (`0483fd9f`) után futott (az igazoláshoz); a `versbeosztas.py` (a detektor újragenerálása) a commit előtt futott, f22-táblát nem töltött be. A #22 futtatót nem indítottam.
- **N-F85c** (a `NYITOTT_FELADATOK.md`-ben): az ALVIL-001 három régi kulcsú sora nem javítandó most.
- **DT-F85a (5)** tárgytalan (a `parok_Peld` már létezik); a DONTESEK.md-ben jelölve, az állapot 🟢 marad.

## 10. F85.10 — a 4 „nem átkulcsolt” kézi sor sorsa; a `tokenek.py` kiegészítése a közös kulcson álló összevonásokra

*A felhasználó kifejezetten jóváhagyta (chat, 2026.10.09). Érintett fájlok (a brief `ir` mezőjében): `eszkozok/karoli_strong/tokenek.py`, `f22/versosszevonas.tsv`, `eszkozok/tahot_verskulcs_igazolas.py`, `naplok/F85_igazolas.tsv/.md`. Az `eszkozok/karoli_strong/egyesit.py`-hoz nem kellett nyúlni.*

### 10.1 A 4 kivezetett sor, amely nem átkulcsolt versre hivatkozott — nem állítottam vissza

A 4 sor: `\tÉzs 9:20\tnincs_karoli` (kézi tábla), `Ézs 64:1\t\ttorol` és `\tÉzs 64:1\ttorol` (kézi tábla), valamint a `Ézs 9:20  15  34  Ézs 9:20` összevonás-sor (a versosszevonas.tsv-ből). Mind az átkulcsolás előtti eltolt állapotot kompenzálta:
- a `nincs_karoli Ézs 9:20` azt mondta, hogy a TAHOT 9:20-nak nincs saját Károli-verse (a régi kulcson a K 9:20 a T 9:19-et kapta, a T 9:20 a beolvasztással került a K 9:20-ba); az átkulcsolás után a T 9:19 maga K 9:20, a T 9:20 kulcsa változatlanul 9:20: a közös kulcs maga a beolvasztás;
- a két `torol` sor a *régi detektor-lista* Ézs 64:1-re vonatkozó sorait törölte; a detektor-lista újragenerálása után nincs mit törölniük (a `f22/versmegfeleltetes.tsv`-ben ÓSZ-sor nincs);
- az összevonás-sor `eredeti` címkéje (Ézs 9:20) *régi* címke: **a sor nem tűnt el, hanem F85.10-ben új alakban visszakerült** (10.2), a hozzá tartozó `hu_tol`–`hu_ig` és `megj` változatlan.

A `nincs_karoli` és a két `torol` sort **nem állítottam vissza**, indokok: (1) azt kompenzálták, ami már nincs; (2) a visszaállításuk a mai tokenek-kódban *kárt okoz*: az `igazolas.py` d) kontrollja szerint a `nincs_karoli Ézs 9:20` sor a `_versmegfeleltet`-ben az `Ézs 9:20` kulcsot kizárja a leképezésből (az `erintett_e` halmaz), és a sort a `beolvasztott` halmaz miatt ki is hagyja, így a K 9:20 kulcs tokenjei elvesznek (`SystemExit: … nem fér a kulcs 0 tokenjébe`). Bizonytalanság nincs.

### 10.2 A változtatások

- **`f22/versosszevonas.tsv`:** új 6. és 7. oszlop, `er_tol` / `er_ig`: a beolvasztott TAHOT-vers tokenjeinek 1-alapú helye a közös Károli-kulcs nyers tokenlistájában (a fájlfejléc-megjegyzés leírja). A 6 futott összevonás (4Móz 29:39 [31–43], Ézs 9:20 [19–41], Ézs 64:1 [10–28], Péld 11:31 [11–18], Jób 16:22 [10–18], Jób 36:33 [10–20]) az eredeti sorokkal (hu_tol, hu_ig, `eredeti`, `megj` verbatim a F85.4 előtti állapotból); a 3 még nem futott összevonás: Hós 11:11 [20–39] (F85.4), **Hós 1:11 + 2:1** (hu 23–30, er 24–34) és **Préd 2:26 + 2:25** (hu 1–8, er 1–9; az extra a vers *elején* áll, ezért az `er_tol` 1). Az `eredeti` a beolvasztott TAHOT-vers átkulcsolás előtti címkéje.
- **`eszkozok/karoli_strong/tokenek.py`:** `versosszevonasok()` az opcionális `er_tol`/`er_ig` oszlopokat is beolvassa; új `_eredeti_osztva()`: a nyers (`_nyers_eredeti()`) lista leképezése után a közös kulcs tokenlistájából kiemeli a beolvasztott vers tokenjeit (extra), a fő vers tokenjei 1-től újraszámozva maradnak; `betolt_eredeti(versmegf=True)` a fő verset adja (mint a régi pipeline), `osszevont_extra()` az extrát (sorszám = a fő vers tokenszáma + i, mint régen). `betolt_eredeti(versmegf=False)` (a detektor bemenete) a nyers listát adja, változatlanul. A régi alakú sorok (nincs `er_tol`) továbbra is a nyers kulcsról kapják az extrát (visszafelé kompatibilitás). Az `egyesit.py` változatlan: ugyanazt a `betolt_eredeti()` / `osszevont_extra()` / `versosszevonasok()` interfészt használja.

### 10.3 Az igazolás (`naplok/F85_igazolas.md`, `eszkozok/tahot_verskulcs_igazolas.py`)

- **(a)** 6 330 eltérő sor = a napló, csak az Igehely mező; a többi 462 971 sor bájtazonos (változatlan eredmény; a korábbi 462 972 a záró üres elemet is számolta).
- **(b)** a jóváhagyott könyvek vers → héber szavak bemenete a régi és az új pipeline között: **17 747 vers, 0 eltérés** (a futott 6 összevonás extrájával együtt: a `osszevont_extra()` is azonos).
- **(c) 19 táblapár** (`egyesit.epit()` memóriában, a `parok_*`/`szavak_*` fájlok nem íródtak): a régi pipeline (átkulcsolás előtti TAHOT + régi f22 táblák, az új kóddal futtatva) mind a 19-et bájtra reprodukálja (regresszió-teszt); az **új pipeline mind a 19 táblapár adatsorait és mind a 19 átnézési naplót bájtra reprodukálja, a 6 összevont verset a `kezi` jelölésekkel együtt** (0 eltérő vers). A teljes fájl-bájtokra a 19-ből 14 azonos; **5 könyvnél (2Móz, 4Móz, Ézs, Jób, Péld) csak az első, `#` kezdetű proveniencia-sor tér el**: a `forras=` mező az `f22/versmegfeleltetes.tsv` és az `f22/versmegfeleltetes_kezi.tsv` nevét sorolta fel (azok ÓSZ-sorai a kivezetéssel megszűntek), az `egyesit.proveniencia_sor()` újraíráskor ezeket már nem nevezi. A táblákat nem írtam felül; ez az egyetlen, amely a feltételtől („BÁJTRA”) eltér, és kódmódosítás nélkül nem is hozható egyezésre (a régi állapot forrásait nem szabad megnevezni, ha már nem használjuk). A döntés a felhasználóé: elfogadja-e, vagy az újraíráskor kézzel kell-e a proveniencia-sorba az F85-ig használt forrásokat megőrizni.
- **(d)** kontroll: a 4 kivezetett sor visszaállítása megszakítja a betöltést (10.1).
- **(e)** a 9 összevonás szétválasztása (a futott 6 + a nem futott Hós 1:11/2:1, Hós 11:11/12:1, Préd 2:26/2:25): a fő vers és az extra tokenjei (strong, alak, tükörfordítás, sorszám) megegyeznek az átkulcsolás előtti nyers TAHOT megfelelő verseivel.
- `egyesit.py --ellenoriz` mind a 19 könyvre „rendben”.
- **Megjegyzés:** a `versbeosztas.py --onteszt` 6. pontja (a 2Móz 35:36–36:37 eltolódását keresi a *nyers* TAHOT-ban) az F85.6 átkulcsolás óta hibát jelez (a 2Móz már Károli-kulcsú); ez az F85.6 átkulcsolás következménye (a régi teszt a nyers TAHOT eltolódását kereste; a kiinduló állapot kimenete a 11. szakaszban: „ÖNTESZT HIBA: a 2Móz 35:36–36:37 eltolódását nem találta meg”), a `versbeosztas.py` az F85.12-ig nem volt az `ir`-ben — külön tétel (frissítse az öntesztet az átkulcsolt állapotra).

## 11. F85.12 — a proveniencia-eltérés elfogadása; a `versbeosztas.py` önteszt 6. pontja

*A felhasználó kifejezetten jóváhagyta (chat, 2026.10.09, az `ELLENOR_F85_8.md` után).*

- **Proveniencia-sor (10.3 (c) 5 könyve: 2Móz, 4Móz, Ézs, Jób, Péld):** a felhasználó elfogadta, hogy a megszűnt `f22/versmegfeleltetes.tsv` / `f22/versmegfeleltetes_kezi.tsv` forrást a táblák proveniencia-sorában nem nevezzük meg. A meglévő `parok_*` / `szavak_*` táblákat **nem írjuk újra**; az új proveniencia-sor a következő valódi újrafuttatáskor kerül be. A táblák nem változtak (git: `adat/` diff üres, a `parok_*`/`szavak_*` blobok azonosak).
- **`eszkozok/karoli_strong/versbeosztas.py --onteszt` 6. pontja:** az F85.6 óta a 2Móz 35:36–36:37 eltolódása az átkulcsolt TAHOT-ban már nincs meg, ezért a régi teszt („az eltolódást nem találta meg”) hibát jelzett. A teszt most azt ellenőrzi, hogy a 2Móz-ra a detektor nem jelez eltolódást, a régi `2Móz 36:38` kulcsnak 0 sora van, és a `2Móz 35:36` / `2Móz 36:37` Károli-kulcsnak vannak sorai. Az 1Móz-teszt és minden más pont, valamint a detektor viselkedése változatlan. Az `--onteszt` kimenete: *előtte* `ÖNTESZT HIBA: a 2Móz 35:36–36:37 eltolódását nem találta meg`; *utána* `önteszt: rendben`. A generált `f22/versmegfeleltetes.tsv` és `naplok/F22_versbeosztas.md` nem íródott újra (SHA-256 azonos a futtatás előtt és után).
- **`eszkozok/karoli_strong/tokenek.py` 54. sor körüli megjegyzés:** pontosítva (a „2Móz 35:36–36:37 igazolt” az F22-beli állapotra vonatkozott; az F85.6 óta a kulcsok Károli-kulcsok, a lista az ÓSZ-ben üres). Kódváltozás nincs (a `beolvasztott` halmaz és a többi rész érintetlen).
- A brief `ir` mezője az F85.12-ben NEM bővült: az F85.12 az `eszkozok/karoli_strong/versbeosztas.py`-t (amely az `olvas` mezőben szerepelt, az `ir`-ben nem) az `ir` bővítése nélkül módosította. Az `ir` bővítését az F85.16 pótolta (és a `feladatok.py ellenoriz` 0 hibával lefutott).

## 12. F85.13 — dokumentációs javítások az ELLENOR_F85_8 eltérésére (1, 2, 5, 6, 7)

*A felhasználó kifejezetten jóváhagyta (chat, 2026.10.09). Kódfájl közül csak az `eszkozok/tahot_verskulcs_igazolas.py` változott (új f pont: `egyesit.ellenoriz` a 19 könyvre, proveniencia-sor a naplókban); az `adat/`, `parok_*`/`szavak_*`, `f22/` és `konkordancia/` fájlok érintetlenek.*

- **(1) DT-F85a:** a DONTESEK-sor rögzíti, hogy a Hós 1:11 + 2:1 és Préd 2:26 + 2:25 összevonás-sor felvételét, az `er_tol`/`er_ig` oszlopokat és a `tokenek.py` módosítását (F85.10) a felhasználó hagyta jóvá (chat, 2026-10-09); a cella belső ellentmondása feloldva: a 4. tétel (F85.8) és az F85.10–F85.12 kész, az 5–7. tétel vár (az állapot 🟢).
- **(2) `naplok/F85_kivezetett_sorok.tsv`:** új `allapot_F85_10_utan` oszlop: a 97 kézi sor `kivezetve`, a 7 `versosszevonas` sor `visszakerult_F85.10_er_tol_er_ig_oszloppal`, +2 új sor (`uj_felvett_F85.10`: Hós 1:11 + 2:1, Préd 2:26 + 2:25). Nettó kivezetve **97 kézi sor**; a `versosszevonas.tsv` 7 → 9 adatsor (a 10.1 és 9.1 „104 kivezetett” az F85.8 pillanatnyi állapota volt, javítva).
- **(5) A „csak a proveniencia-sor tér el” pontosítása (10.3 (c)):** a `forras=` mezőben az 5 könyv (2Móz, 4Móz, Ézs, Jób, Péld) közül a 4Móz csak az `f22/versmegfeleltetes.tsv`-t, a többi mindkét f22 táblát (`versmegfeleltetes.tsv` és `versmegfeleltetes_kezi.tsv`) nevezte meg.
- **(6) Az önteszt-regresszió** a jelentésben szerepel (11. szakasz; javítva az F85.12-ben), N-tételt nem veszek fel (lezárt). A „stash-sel ellenőrizve” állítást kivettem (a 10.3 pont); a kiinduló hibakimenet a 11. szakaszban áll.
- **(7) Számok:** a detektor-lista **290 → 12** sor (278 ÓSZ-sor ment ki: 269 `eltolt` + 9 `nincs_karoli`); a „469 302” → **469 301** sor (fejléccel).
- **`egyesit.py --ellenoriz` (A1):** a futtatás kimenete és proveniencia-sora az `igazolas.py` új `f` pontjában (`naplok/F85_igazolas.tsv/.md`).

## 13. F85.14 — a `beolvasztott` halmaz az átkulcsolt kulcsokra; az igazolás negatív próbával (ELLENOR_F85_8 (3), (4))

*A felhasználó kifejezetten jóváhagyta (chat, 2026.10.09). Érintett fájlok (mind az `ir` mezőben): `eszkozok/karoli_strong/tokenek.py`, `f22/versosszevonas.tsv` (csak a fejléc-megjegyzés), `eszkozok/tahot_verskulcs_igazolas.py`, `naplok/F85_igazolas.tsv/.md`. A parok_*/szavak_* fájlok és az `adat/` érintetlen; a generált `f22/versmegfeleltetes.tsv` nem íródott újra; a #22 futtatót nem indítottam.*

### 13.1 `tokenek.py`: a `beolvasztott` halmaz

- **Előtte:** `beolvasztott = {o['eredeti'] for o in versosszevonasok()}` — az `eredeti` oszlop átkulcsolás előtti (MT-számozású) címkéi (4Móz 30:1, Péld 12:1, Jób 17:1, 37:1, Hós 12:1, Hós 2:1, Ézs 64:2, …), amelyek a mai TAHOT-ban más verseket jelölnek; egy jövőbeli `nincs_karoli` sor ilyen kulcsra csendben eldobódott volna.
- **Utána:** `beolvasztott_regi` = a régi alakú sorok (nincs `er_tol`) `eredeti` kulcsai (a régi viselkedés, változatlanul); `beolvasztott_uj` = az új alakú sorok (`er_tol` van) **Károli-kulcsai** (a közös, átkulcsolt kulcs); `beolvasztott` = a kettő uniója. Az `erintett_e` halmazból az új kulcsok kimaradnak, így egy `nincs_karoli` sor a közös kulcsot sem a leképezésből nem dobhatja ki, sem át nem teheti a +1000-es azonosítóra. Ennek következménye: az F85.8-ban kivezetett `nincs_karoli Ézs 9:20` sor visszaállítva ma már ártalmatlan (az F85.10-ben még `SystemExit`-et okozott).
- **Docstring:** a `versosszevonasok()` és `_eredeti_osztva()` leírása pontosítva: a közös kulcs listája a *leképezett* (a detektor-/kézi tábla szerinti leképezés utáni, az összevonás kiemelése előtti) lista; az ÓSZ-ben a leképezés üres, így az a nyers lista. A `f22/versosszevonas.tsv` fejléc-megjegyzése is ugyanígy.
- **Reprodukálhatóság:** a mai állapotban a kézi tábla és a detektor-lista ÓSZ-sora üres, ezért a változás hatástalan; a 19 táblapár reprodukálása változatlan (13.3).

### 13.2 A Hós és Préd `betolt_eredeti()` kimenetének változása (a #22-menet szempontjából)

A `versosszevonas.tsv` nincs a jóváhagyott könyvekre szűrve (a szűrő csak az `f22/versmegfeleltetes*.tsv`-re vonatkozik), ezért a Hós és a Préd — amelyek még nem szerepelnek a `VERSBEOSZTAS_JOVAHAGYOTT`-ban — `betolt_eredeti()` kimenete már most eltér a nyers listától, **pontosan a 3 összevonás kulcsán** (`igazolas.py` g pont):

| kulcs | nyers (az F85.8 utáni) token | most: fő vers a kulcson + extra (`osszevont_extra()`) |
|---|---|---|
| Hós 1:11 | 34 | 23 + 11 (Hós 2:1) |
| Hós 11:11 | 39 | 19 + 20 (Hós 12:1) |
| Préd 2:26 | 47 | 38 + 9 (Préd 2:25) |

Minden más Hós/Préd kulcs változatlan; a többi könyvben csak a 6 futott összevonás kulcsa tér el a nyerstől (4Móz 29:39, Jób 16:22, 36:33, Péld 11:31, Ézs 9:20, 64:1).

**Várt-e ez a #22 Hós/Préd-menetében? Igen.** A futott könyveknél a #22 ugyanezt a mechanizmust használta (`betolt_eredeti()` = a Károli-vers fő TAHOT-verse, `osszevont_extra()` = a beolvasztott TAHOT-vers tokenjei `kezi` állapotban, `versosszevonas` `hu_tol`–`hu_ig` a Károli-vers `kezi` szavai). A Hós/Préd-menetben ezért a Hós 1:11, Hós 11:11 és Préd 2:26 vers a modellnek a fő verssel (a 23 / 19 / 38 tokennel) jelenik meg, a beolvasztott vers 11 / 20 / 9 tokenje és a Károli-szavak `hu` 23–30 / 22–40 / 1–8 tartománya `kezi` marad — az F22 Jób/Péld/Ézs/4Móz-menetekkel azonos kezeléssel. A Préd 2:26-nál az extra a közös lista *elején* áll (`er_tol` = 1): a fő vers tokenjei 1-től újraszámozva maradnak, az extra sorszáma a fő vers tokenszáma utáni folytatás, ahogy a többi összevonásnál.

### 13.3 Az igazolás negatív próbával (`naplok/F85_igazolas.md`)

- **n) Negatív próba (új):** szándékosan rontott, a repón kívül ideiglenes könyvtárban lévő `versosszevonas.tsv`-másolaton a 9 összevonás ellenőrzésének **bukni kell**, és bukott: (1) Péld 11:31 `er_tol–er_ig` 11–18 → 10–17 (határon belüli, rossz tartomány): „fő vers egyezik: False, extra egyezik: False”; (2) Hós 11:11 20–39 → 1–19 (fő és extra felcserélve): bukik; (3) Ézs 64:1 `er_ig` 28 → 99 (tartományon kívüli): `SystemExit` („nem fér a kulcs 28 tokenjébe”). A valós (nem rontott) bemeneten ugyanez az ellenőrzés nem bukik. A repóbeli `versosszevonas.tsv` nem módosult.
- **d) Kontroll átírva:** a 3 kézi sor (`nincs_karoli Ézs 9:20`, `torol Ézs 64:1` ×2; a negyedik kivezetett sor a versosszevonas Ézs 9:20 sora, amely új alakban visszakerült) visszaállítva a mai kóddal: a betöltés **azonos** (0 eltérő kulcs); az eredmény csak „azonos betöltés” esetén OK, megszakadásnál HIBA (a korábbi kettős-OK önigazoló volt). A docstring: 3 (nem 4) visszaállított sor.
- **a)** „469 301 / 469 301 sor (fejléccel)” (a záró üres elem nélkül).
- **19 táblapár újrafuttatása a valós bemeneten** (a módosított `tokenek.py`-val): a *régi* pipeline mind a 19-et bájtra reprodukálja; az *új* pipeline mind a 19 táblapár adatsorait és átnézési naplóját bájtra reprodukálja, a 6 összevont verset a `kezi` jelölésekkel együtt; a teljes fájl-bájtokra 14 azonos, **5 (2Móz, 4Móz, Ézs, Jób, Péld) csak a proveniencia-sorban (`forras=`) tér el** — a felhasználó ezt elfogadta (11. szakasz), a táblák nem íródnak újra. `egyesit.ellenoriz`: mind a 19 könyvre rendben. Összesen 0 HIBA.

## 14. F85.16 — az ELLENOR_F85_12 eltéréseinek kezelése (1, 2, 3, 4, 6, 7)

*A felhasználó kifejezetten jóváhagyta (chat, 2026.10.09). Az `adat/`, a `parok_*`/`szavak_*` és a `f22/` fájlok, valamint a generált `f22/versmegfeleltetes.tsv` érintetlenek; a #22 futtatót nem indítottam.*

- **(1) `ir`:** a brief `ir` mezőjét ténylegesen bővítettem az `eszkozok/karoli_strong/versbeosztas.py`-val (a `feladatok.py ellenoriz` 0 hibával lefutott). A 11. szakasz hamis állítása („az `ir` bővült”) javítva: az F85.12 az `ir` bővítése nélkül módosította a fájlt, az F85.16 pótolta.
- **(2) `naplok/F85_kivezetett_sorok.tsv`:** az `eszkozok/tahot_verskulcs_kivezetes.py` új `--archivum` módot kapott (a kivezetés előtti állapotot a `git show 0483fd9f~1` adja, az `allapot_F85_10_utan` oszlopot a mai `f22/versosszevonas.tsv` és a `naplok/F85_kulcsvaltas.tsv` alapján), a fájlt a generátor újragenerálta (`--archivum --ir`); a fejléc `# GENERÁLT: eszkozok/tahot_verskulcs_kivezetes.py --archivum | …` generátor-proveniencia. Egyezés a F85.13-as (kézzel bővített) fájllal: az oszlopfejléc és mind a **106 adatsor azonos** (97 `kivezetve`, 7 `visszakerult_F85.10_…`, 2 `uj_felvett_F85.10`); egyetlen sor változott, a `#` fejléc-megjegyzés (a `forras=` pontosítva). A régi, f22-táblákat író mód (az F85.8 egyszeri kivezetése) megtagadja a futást az F85.10 utáni f22-alakon.
- **(3) DT-F85a:** a proveniencia-sorról szóló mondat most a `parok_*` és a `szavak_*` táblát is nevezi (mindkét táblában).
- **(4) Számok:** „nem érintett sorok” 462 972 → **462 971** (a jelentésben, a `naplok/F85_igazolas.md/.tsv`-ben; az `igazolas.py` a) pontja a záró újsor utáni üres elemet kihagyja); az igazolás-naplók újrafuttatással frissültek (0 HIBA).
- **(6) 12. szakasz:** a „Nincs kódváltozás” a valóságra javítva (az `igazolas.py` változott az F85.13-ban); a „9.5 pont” → 10.3.
- **(7) 13. szakasz előtti szöveg (183. sor):** a kiesett szó pótolva („kézi tábla 97 adatsor + összevonás-fájl 7 adatsor”).

## 15. F85.17 — az `erintett_e` védelem szűkítése és önteszt-eset (ELLENOR_F85_12 (5))

*A felhasználó üzenete a „…önteszt-esetet, amely egy eltolt” mondatnál megszakadt; a teljes alak utólag megérkezett: az önteszt-eset „egy eltolt sornál a megkettőzés hiányát ellenőrzi”. Az én értelmezésem (eltolt sorral nem duplikálható vers) ezzel egyezik.*

- **Kód (`eszkozok/karoli_strong/tokenek.py`):** az `erintett_e` védelem (F85.14) csak a `nincs_karoli` sorokra szól: `erintett_e = {e … if e and not (t == 'nincs_karoli' and e in beolvasztott_uj)}`. Egy `eltolt` sor, amelynek `eredeti`-je beolvasztott (közös) Károli-kulcs, továbbra is elmozdítja onnan a verset. Korábban (F85.14) az ilyen sor a verset a saját kulcsán is meghagyta, és az `eltolt` kulcsra is bemásolta (megkettőzés).
- **Önteszt-eset (`eszkozok/karoli_strong/versbeosztas.py`, `eltolt_osszevonas_hibak()`, az `--onteszt` 5c pontja):** ideiglenes `versosszevonas.tsv`-ben az `X 1:2` kulcs új alakú (`er_tol`) beolvasztás; a lista egyetlen sora `('X 5:1', 'X 1:2', 'eltolt')`. Elvárás: mindhárom eredeti vers (`a`, `b+c`, `z`) pontosan egyszer szerepel az eredményben, és az `X 1:2` kulcs nem marad meg. A függvény a tokenek modult paraméterként kapja, hogy a régi kódon is futtatható legyen.
- **Bukás a régi kódon:** az F85.14 `tokenek.py`-ján (`9fb8dafd`) és a `HEAD`-en (F85.16) az eset **BUKIK** („a(z) b+c eredeti vers 2 példányban szerepel (1 kell)”, „a beolvasztott kulcs az eltolt sor után is megmaradt (megkettőzés)”); az új kódon rendben. A `versbeosztas.py --onteszt`: `önteszt: rendben`.
- **Feltétel:** a mai kód ugyanúgy viselkedik (a kézi tábla és a detektor-lista ÓSZ-sora üres, a módosított ág nem fut). Az igazolás újrafuttatva (`naplok/F85_igazolas.*`): 0 HIBA; a 19 táblapár sorai és átnézési naplója bájtazonos (5 könyvnél csak a proveniencia-sor tér el, elfogadva), `egyesit.ellenoriz` 19/19; a Hós/Préd összevetés (13.2) számai változatlanok (Hós 1:11 34 → 23+11, Hós 11:11 39 → 19+20, Préd 2:26 47 → 38+9).
- Az `eszkozok/karoli_strong/versbeosztas.py` az `ir` mezőben van (F85.16).
