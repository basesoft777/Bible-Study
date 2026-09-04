# Motívum-azonosító séma — v3, VÉGLEGESÍTVE (2026.09.04)

*Felváltja a `Motivum_azonosito_sema_javaslat_v1.md`-t (egydimenziós,
`IMAGO-001` próbával) — az ott felmerült kategorizálási problémák miatt
(3 motívum sehova nem illett, 2 motívum két területet is érintett)
áttérve egy kétdimenziós modellre. A v2 (2026.09.02) 3 nyitott kérdését
a felhasználó 2026.09.04-én lezárta (l. 6. pont) — a séma ezzel
véglegesítve, ténylegesen bevezetve a `PaRDeS_motivumok.md`-be.*

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
| Por/formáltatás (jacar-afar) — emberi esendőség | `ANTROP-004` | Antropológia |

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

## 6. Nyitott kérdések — LEZÁRVA (felhasználói döntés, 2026.09.04)

1. **A 9 téma-kód bővítése:** a lista **nyitott marad**, nem bővül
   előre. Új téma-kód csak akkor kerül bevezetésre, amikor egy tényleges
   motívum ténylegesen nem illik egyik meglévő kódba sem (pl. a
   jövőbeli 1Móz 17+ körülmetélés/névváltoztatás-motívumoknál, ha
   felmerül). A mai תהו/בהו-lelet a meglévő `TEREMT` kódba illeszkedett
   — ez megerősítette, hogy a tág, nyitott kódok jól működnek
   spekulatív előregyártás nélkül is.
2. **ID-kiosztás hatóköre:** **nem** kap minden meglévő motívum
   visszamenőleg ID-t. Az ID-kiosztás a ⭐-küszöböt elért vagy ✅
   lezárt motívumokra korlátozódik (l. 3. pont — ténylegesen 13 tétel,
   a por/afar pótlásával). Ezentúl minden újonnan ⭐-küszöböt érő vagy
   lezáruló motívum a felvétel pillanatában kap ID-t.
3. **Mely motívumok kapjanak ID-t egyáltalán:** **csak** a ⭐-küszöböt
   elért/lezárt motívumok — az egyszeri, még alakuló bejegyzések nem.
   Indoklás: az ID stabil kereszthivatkozási kulcs, aminek csak azoknál
   a motívumoknál van értéke, amelyek ténylegesen visszatérnek/több
   study-ban hivatkozásra kerülnek; korai fázisú, még névváltozás
   előtt álló tételeknél az ID-adás korai elköteleződés lenne.
4. A motívumnaplóba (`PaRDeS_motivumok.md`) történő tényleges bevezetés
   **megtörtént** — l. a párhuzamos Code-prompt-részt.
