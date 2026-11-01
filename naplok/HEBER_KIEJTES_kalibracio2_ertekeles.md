# Gépi héber kiejtés — a 2. kalibráló minta értékelése (N-F131w, DT430 után)

*Értékelés, nem döntés: szabály nem módosult, adat (`adat/`), `eszkozok/` és lexikonlap nem változott. A bekötésről a felhasználó dönt (⛔).*

- **Modell:** `claude-opus-5-5`
- **Bemenet:** a 2. minta (`naplok/HEBER_KIEJTES_kalibracio2.json`, 50 alak, seed 20261107, az 1. mintával átfedés nélkül) jelölései szó szerint: `naplok/HEBER_KIEJTES_kalibracio2_valasztas.txt`.
- **Gépi kiértékelés:** `naplok/HEBER_KIEJTES_kalibracio2_eredmeny.md`. Újrafuttatás:
  ```bash
  python naplok/HEBER_KIEJTES_kalibracio_kiertekel.py --menet 2 --chat "$(cat naplok/HEBER_KIEJTES_kalibracio2_valasztas.txt)"
  ```
- **Proveniencia:** `scope=naplok/HEBER_KIEJTES_kalibracio2.json + _kulcs.json + naplok/HEBER_KIEJTES_kalibracio2_valasztas.txt | forras=naplok/HEBER_KIEJTES_kalibracio_kiertekel.py --menet 2 | ts=2026-10-30`. A 4. és az 5. szakasz besorolása `manual`.

> **Javítás (2026-10-30, a DT430 kiegészítése):** az orkesztrátor a 41. sor jelölését hibásnak ismerte el (a
> קָרָאוּ pauzális alak, sevá nélkül; a gépi „káráú” a helyes). **A jelölő hibázott; a javított eredmény 50/50**
> (átlagos 13/13, nehéz 37/37). A 16. sorhoz szükséges R5b bekerült, a gépi alak most „úbókéa”. Az alábbi
> szakaszok a javítás előtti szigorú számot is megőrzik.

## 0. A jelölő nem független

A felhasználó szó szerint ezt írta: „döntsd el”. A jelöléseket ezért az orkesztrátor-session végezte, a kulcsfájl megnézése nélkül. Mércéje:
- a héber nyelvtan (tibériási olvasat);
- az első körben a felhasználó által választott konvenciók (DT430 R1–R8).

A jelölő tehát ugyanazokat a szabályokat alkalmazta, amelyeket a gép. **A mérés így a szabályok megvalósításának hibáit és a szabályok hiányait mutatja, nem a konvenciók helyességét.** A konvenciókat egyedül az első kör méri, ahol a felhasználó maga jelölt.

## 1. Röviden

| | gépi változat elfogadható | ebből preferált | (b) konvenció-eltérés | (a) valódi hiba |
|---|---|---|---|---|
| **átlagos (vegyes, 13)** | **12/13** (javítva: 13/13) | 12 | 0 | 1 (41., a jelölő hibája) |
| **nehéz (37)** | **37/37** | 35 | 1 (16.) | 0 |
| **összesen (50)** | **49/50** (javítva: 50/50) | 47 | 1 | 1 |

Ehhez két megjegyzés tartozik:
- **A 41. sor (קָרָאוּ) jelölése téves premisszán áll.** A pontozott szövegben a reson **kámec** áll, nem sevá (qārāʾû, pauzális alak atnachchal; a STEP is `ka.Ra.'u`). A jelölő a „káreú” saját alakot azzal indokolta, hogy „a sevá a torokhang előtt az R3 szerint kiejtett”, de ebben a szóban nincs sevá. A gépi „káráú” a pontozás szerinti olvasat. Ha a 41. sort a pontozás szerint értékeljük, az átlagos esetek is **13/13**, összesen **50/50**. A jelölést nem bíráltam felül: a szigorú szám 49/50, a döntés a felhasználóé.
- **A 16. sor (וּבֹקֵעַ) egy szabály hiányát mutatja** (4. szakasz).

## 2. Kategóriánként

| kategória | n | gépi: egyezik / elf. / (b) / (a) | gépi pontossága (a) szerint |
|---|---|---|---|
| kámec kátán (gyanú) | 6 | 5 / 1 / 0 / 0 | 6/6 |
| nem szókezdő sevá | 6 | 6 / 0 / 0 / 0 | 6/6 |
| furtív patah | 5 | 4 / 0 / 1 / 0 | 5/5 |
| dáges forte | 5 | 5 / 0 / 0 / 0 | 5/5 |
| ketiv/qere | 0 | — | nem mérhető (az 1. minta minden ilyen alakot felhasznált; l. a kivétel-próbát) |
| makkef | 5 | 5 / 0 / 0 / 0 | 5/5 |
| szókezdő begadkefat dáges nélkül | 5 | 5 / 0 / 0 / 0 | 5/5 |
| ס és שׂ | 5 | 5 / 0 / 0 / 0 | 5/5 |
| vegyes (átlagos) | 13 | 12 / 0 / 0 / 1 | 12/13 (a 41. sor, l. fent) |

A javasolt változatom szintén 49/50 sorban elfogadható. Egyedül a 2. sorban tért el a gépitől („rechullátechá”), és ott mindkettőt elfogadta a jelölő.

## 3. Kivétel-próba a teljes TAHOT-on (R2 kivétellista, R7)

A két minta a kivétellista szavait nem tartalmazta, ezért a teljes TAHOT-on külön próbáltam (`naplok/HEBER_KIEJTES_kivetel_proba.md`, szkript: `naplok/HEBER_KIEJTES_kivetel_proba.py`):

| tő | előfordulás | eredmény |
|---|---|---|
| H3605 כֹּל | 5 415 | a כָּל/כָל mindig „kol”; a holamos כֹּל/כֹל „kól” (a pontozás szerint hosszú) — a döntés szerint helyes |
| H2451 חָכְמָה | 153 | „chochmá”, „chochmat”, „chochmát…” — helyes |
| H3389 Jeruzsálem | 643 | a 638 szokásos alak „jerúsálajim”; **két szélső eset hibás**: a sinnel írt változat (ירוּשָׂלִָם, 2×) „…szálajim”-ot, az irányjelölős alak (יְרוּשָׁלְַמָה, 3×) „jerúsálamá”-t ad |

A TAHOT-tőalakok egy részében a jod pont nélkül áll („jrúsálajim”), mert az előtag (pl. בִּ) a TAHOT-ban külön sorban van. A teljes szóvá összerakott alakban („bírúsálajim”) ez nem fordul elő; a DT430 (5) a teljes szóra szól.

## 4. Maradt-e hiba, amelyhez szabály vagy kivétel kell?

| # | eset | kell-e szabály/kivétel | javaslat (⛔ a felhasználó dönt) |
|---|---|---|---|
| **1** | 16. sor וּבֹקֵעַ: a ב a **tő** kezdőbetűje, de előtag (וּ) után áll; a gép a pontozás szerint lágyat ad („úvókéa”), a jelölő kemény „úbókéa”-t preferált | **igen, szabálypontosítás (R5b)** | az R5 „a tő kezdőbetűje kemény” része vonatkozzon az előtag utáni tő-kezdőbetűre is. Az 1. körben a felhasználó a hasonló 36. sorban (וּפֶן) mindkettőt elfogadta („úpen”, „úfen”), tehát nem ellenkezik vele. |
| **2** | Jeruzsálem szélső alakjai (3. szakasz) | **igen, kivétel** | az R7 ne magánhangzó-szabály legyen (a pátah + hirek → „aji”), hanem lexikai kivétel a H3389 tőre: „jerúsálajim”, irányjelölővel „jerúsálajmá”, előtaggal a szokott előtag-kiejtés + a tő |
| **3** | 41. sor (קָרָאוּ) | nem | a gépi alak a pontozás szerinti; a jelölés premisszája téves (1. szakasz) |
| **4** | az 1. kör nyitott esetei (17. „mizebéach”, 19. „réjach”, 24. „missól”, 37. „kisól”, 41. „vesalém”) | a 2. kör nem mérte | ezek a felhasználó saját ítéletén múltak; a 2. kör jelölője a szabályokat követte, így nem ismétlődtek. Továbbra is nyitottak; szabályt nem javaslok rájuk |
| **5** | ketiv/qere a mintán kívül (pl. a tetragramma előtaggal: לַיהוָה) | figyelni | a megvalósítás „előtag + -Jahve” alakot ad (pl. „la-Jahve”); egyik mintában sem szerepelt, a felhasználó nem látta. Bekötés előtt érdemes egy pillantást vetni rá |

## 5. Állapot a bekötés előtt

- **Mért:** a DT430 szabályaival az 1. mintán 41/50 (a felhasználó jelölése; a 9 eltérésből 4 a döntések következménye), a 2. mintán 49/50 (szabálykövető jelölő; átlagos 12/13, nehéz 37/37).
- **A bekötés előtti teendők a döntés után:**
  - R5b és a lexikai R7, ha a felhasználó elfogadja;
  - a kivételtábla javítása (a ס-sorok sz-re, a H2555 ch-ra: „chámász”, Jeruzsálem, kol, chochmá);
  - az átíró `eszkozok/` alá tétele, „(gépi)” jelöléssel a lapokon;
  - tesztek, a lapok újragenerálása.

  Ezek egyike sem történt meg.
