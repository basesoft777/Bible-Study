# F85_jelentes.md — TAHOT_VERSKULCS: az esetlista (1. tétel)

*Feladat: FELADATOK #85 (`F85_TAHOT_VERSKULCS_BRIEF.md`), ág: `claude/tahot-verskulcs`. Állapot: az 1. tétel kész, a ⛔ 1 jóváhagyásra vár (`DONTESEK.md`, DT-F85a). Táblát ez a menet nem írt: a `TAHOT_kivonat.tsv`, az `f22/` és a `parok_*` / `szavak_*` táblák bájtazonosak (git: csak új fájlok).*

*Kimenetek: `naplok/F85_esetlista.tsv` (345 sor), `naplok/F85_macula_elvetve.tsv` (1 fejezet), a generáló `eszkozok/tahot_verskulcs_esetlista.py` (csak olvas; újrafuttatható: `python eszkozok/tahot_verskulcs_esetlista.py`). A szkript és a `F85_macula_elvetve.tsv` nincs a brief `ir` mezőjében — az `ir` kiegészítését a `/befogad`-ra / az orkesztrátorra bízom.*

## 0. Összefoglalás

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
