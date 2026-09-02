# Motívum-azonosító séma — v2, kétdimenziós (2026.09.02)

*Felváltja a `Motivum_azonosito_sema_javaslat_v1.md`-t (egydimenziós,
`IMAGO-001` próbával) — az ott felmerült kategorizálási problémák miatt
(3 motívum sehova nem illett, 2 motívum két területet is érintett)
áttérve egy kétdimenziós modellre. Nem commitolva, jóváhagyásra vár.*

---

## 1. Formátum

```
[BIBLIAI-TEOLÓGIAI TÉMA]-NNN
```

Az ID **a bibliai-teológiai témára** épül (nem a szisztematikus locusra),
mert ez a mező sosem üres — minden motívumnak van narratív-tematikus
kötődése, míg a szisztematikus dogmatikai besorolás 3 esetben (l. lent)
nem egyértelmű vagy nem is releváns.

A **szisztematikus locus** (ha releváns — a klasszikus loci-rendszerből:
Antropológia, Angelológia, Krisztológia, Hamartológia,
Szövetségteológia, Eszkatológia, Teremtéstan stb.) **külön, opcionális
mezőként** szerepel, akár több érték is megadható egyszerre.

## 2. Bibliai-teológiai téma-kódok (nyitott lista, projekt-belső, nem szakirodalmi szabvány)

| Kód | Téma |
|---|---|
| `TEREMT` | Teremtés, kozmosz, ős-rend/káosz |
| `ALVIL` | Halál, alvilág |
| `KULTUSZ` | Istentisztelet, áldozat, szentély, névsegítségül hívás |
| `HODIT` | Ígéret földje, hódítás, ott lakó népek |
| `ANTROP` | Ember mivolta, méltósága, alkotóeleme |
| `MENNY` | Mennyei/szellemvilág, angyalok |
| `KIRALY` | Királyság, papság |
| `HAMART` | Bűn és következményei |
| `SZOVETS` | Szövetség |

*Bővíthető — új téma-kód bármikor felvehető.*

## 3. A 13-as kör — teljes kiosztás (próba, mind a 13-ra)

| Motívum | Bibliai-teológiai ID | Szisztematikus locus (opcionális) |
|---|---|---|
| Tehóm-Abüsszosz-Hádész-Tartarosz komplexum | `TEREMT-001` | Teremtéstan |
| Hádész (seól) | `ALVIL-001` | Eszkatológia |
| Segítségül hívni az Úr nevét | `KULTUSZ-001` | *(nincs)* |
| Rafeusok/óriás-népek | `HODIT-001` | *(nincs)* |
| Pneuma/pszükhé megkülönböztetés | `ANTROP-001` | Antropológia / Pneumatológia |
| Isten fiai — angyali/Séthita vita | `MENNY-001` | Angelológia |
| Melkizedek — király-pap rendje | `KIRALY-001` | Krisztológia |
| Oltárépítés — Ábrám vándorlásának jelölői | `KULTUSZ-002` | *(nincs)* |
| Bűn következményeinek gyűrűzése | `HAMART-001` | Hamartológia |
| Uralom-megbízás / emberi méltóság | `ANTROP-002` | Antropológia |
| **Isten képmása (celem/eikón)** | **`ANTROP-003`** | **Antropológia + Krisztológia** (mindkettő megadva) |
| Brít | `SZOVETS-001` | Szövetségteológia |

*(12 sor, nem 13 — a Tehóm és a Tehóm-Abüsszosz-Hádész-Tartarosz kibővített
komplexum egyetlen folytonos motívum-ívnek számít, egy ID alatt, ahogy azt
korábban, a "13-as kör" pontosításakor is jeleztük.)*

**A tegnapi próba-ID (`IMAGO-001`) átnevezve `ANTROP-003`-ra** — ugyanaz
a tartalom (5 igehely, mind Magas Bizonyosság), csak az új formátum
szerint.

## 4. Rövid UI-címke (változatlan a v1-hez képest)

| Mező | Példa |
|---|---|
| ID | `ANTROP-003` |
| Teljes név | Isten képmása (celem/eikón) motívum |
| UI-címke | "Isten képmása" |
| Szisztematikus locus | Antropológia, Krisztológia |

## 5. Kapcsolódás a KAPCSOLATOK-réteghez — változatlan elv

Az ID idegen kulcsként szolgál, a Típus/Funkció/Bizonyosság/PaRDeS-szint
adatok külön, az ID-hez kapcsolva:

```
ANTROP-003 (Isten képmása)
  ↳ 1Móz 1:26 ↔ Kol 1:15    | Bizonyosság: Magas | Locus a kapcsolatnál: Krisztológia
  ↳ 1Móz 1:26 ↔ Kol 3:10    | Bizonyosság: Magas
  ↳ 1Móz 1:26 ↔ Ef 4:24     | Bizonyosság: Magas
  ↳ 1Móz 1:26 ↔ 2Kor 3:18   | Bizonyosság: Magas
  ↳ 1Móz 1:26 ↔ 1Kor 11:7   | Bizonyosság: Magas
```

## 6. Nyitott kérdések

1. A 9 téma-kód (2. pont) végleges-e, vagy bővítendő már most (pl. a
   jövőbeli 1Móz 17+ motívumok — körülmetélés, névváltoztatás — melyik
   témába esnének? Egyik jelenlegi kód sem illik rájuk pontosan.)
2. A motívumnaplóba (`PaRDeS_motivumok.md`) történő tényleges bevezetés
   még nem történt meg — ez a dokumentum egyelőre önmagában áll.
3. Ez a dokumentum is elveszhet, ha nem kerül azonnal átadásra Code-nak.
