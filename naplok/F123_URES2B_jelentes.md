# F123.URES2B — az adat nélküli 2/b blokk lekerül a lexikonlapról (jelentés)

*Modell: `claude-opus-5-5`. Dátum: 2026-11-04. Döntés: DT-F174a (az F123 helyőrző-betűi elfogytak, ezért friss szám) (`dontesek/uj/dreamy-varahamihira-09a975.md`).*

## 1. Mi volt a hiba

A lexikonlap „2/b. Kiegészítő szótári adatok” rése 9 lapból 8-on csak hiánymondatot hordozott:

| Lap | `res_forras.tsv` `forras` | Ami a lapon állt |
|---|---|---|
| ISTENTISZT-001, ALVIL-001, ANTROP-001, TEREMT-002 | `adat` | olvasói bevezető + „*Nincs a szerepmátrixon (2. szakasz) túli kiegészítő szótári sor…*” + egy olvasónak látható „Proveniencia:” sor |
| KIRALY-001, MENNY-001, HODIT-001, HAMART-001 | `tanulmany` | olvasói bevezető + a RENDER G15 helyőrzője: „Nincs kiegészítő szótári adat.” |
| TEREMT-001 | `tanulmany` | valódi kézi 2/b (a tehóm 28 további igehelye) — **marad** |

Az `adatres_2b` csak a `KIEGESZITO_SZOTARAK` sorait mutatná, de a SECE az arany lap (2026-10-29) óta a 2. szakasz
7. szerepében és a „Rokon szavak” táblázatában áll, itt ki van zárva; MCGED-sor pedig egy sincs a
`lexikon_hivatkozasok.tsv`-ben. A blokk tehát szerkezetileg mindig üres volt: nem kutatási hiány (CLAUDE.md
3. szabály), hanem adat nélküli szerkezeti blokk. A G15 helyőrző a tanulmány jelölőpárjának mechanikus kitöltése
(RENDER_BRIEF.md G15), szintén nem lelet.

## 2. Javítás a generátorban (`eszkozok/lexikon_general.py`)

- `OPCIONALIS_RESEK = ('2b',)`, `SZERKEZETI_HELYORZOK`, `res_ures_e()`: az opcionális rés üres, ha a törzse — a
  GENERÁLT-RÉS jelölő és a proveniencia-sor nélkül — üres vagy csak a hiánymondata.
- `adatres_2b` adat nélkül üres szöveget ad; a `res_torzs` az üres opcionális résre (adat- és tanulmány-ágon is)
  üres törzset ad, keret és proveniencia-sor nélkül.
- `res_blokkok_alkalmaz`: az üres opcionális rés fejléce csak a többi rés határkereséséig marad, utána a teljes span
  (fejléc, olvasói bevezető, törzs, proveniencia-sor) kikerül (`opcionalis_resek_torol`). A következő futáskor az
  `opcionalis_res_visszaallit` a fejlécet a határkereséshez visszateszi — a generálás fixpont.
- `res_torzs_lapbol`: a lapon nem álló opcionális rés törzse üres; a többi rés határa változatlanul olvasható.
- A tartalomjegyzékben a 2/b nem szerepelt (a `SZAKASZOK` csak a `##` szakaszokat sorolja), ott nincs teendő.
- Az olvasói bevezető „Ha nincs ilyen adat, ezt egy sor jelzi.” mondata törölve (adat nélkül a rés nem jelenik meg).
- A rés a sémában és a `res_forras.tsv`-ben marad: ha egyszer lesz MCGED-sor vagy kézi 2/b, magától megjelenik.

Dokumentáció: `adat/SEMA.md` 2.12 (`tanulmany` mező), `RENDER_BRIEF.md` G15, `CLAUDE.md` (a kilenc rés mondata).

## 3. CI-szabály

`eszkozok/ellenoriz.py` **31. szabály — „Adat nélküli szerkezeti blokk az olvasói lapon (DT-F174a)”**
(`szabaly31_ures_szerkezeti_blokk`): SÉRTÉS, ha egy `lexikon/*_TUDOMANYOS.md` lapon opcionális rés adat nélkül áll.
A szabály szövege kimondja: a kutatási üres eredmény (pl. „üres blokk: javaslat” a szerepmátrixban, a Minősítés
„nincs” mondatai, az üres `domen`-eredmény) nem ilyen blokk, a lapon marad. Teszt: `eszkozok/teszt_ellenoriz_31.py`
(9 eset: a mai lap rendben; a repón a migrált lap gátol, a régi sablonú jelentés; a régi üres 2/b és a G15 helyőrző SÉRTÉS; adattal rendben; kutatási üres eredmény nem
érintett; a generátor törlése, visszaállítása és fixpontja). A teszt a CI „Szabaly-tesztek” lépésében fut
(`.github/workflows/ellenorzes.yml`).

## 4. Újragenerálás és eredmény

`PARDES_DATUM=2026-11-03 python eszkozok/general.py --cel lexikon --id <ID> --ir` a migrált lapokra (E28-lista). A
dátum a lapok saját generálási napja: az E28 a commitolt lap első GENERÁLT-jelölőjének `ts`-ével generál újra, így a
változatlan blokkok időbélyege sem mozdul.

**A 2/b blokk 4 lapról került le** (a teljes span: fejléc, olvasói bevezető, GENERÁLT-RÉS jelölő, hiánymondat,
proveniencia-sor; laponként −10 sor): ISTENTISZT-001, ALVIL-001, TEREMT-002, ANTROP-001.

Mérés a hatás elkülönítésére: a régi és az új generátorral ugyanabból az állapotból generált lapok különbsége
(scratchpad, `diff`) mind a 9 lapon **csak a 2/b span** — 8 lapon kiesik, a TEREMT-001 valódi kézi 2/b-je érintetlen.

**A hatókör eltérése a feladatleírástól („minden lap”):** a DT507 (a) kimondja, hogy a 6 nem migrált lapot nem
generáljuk újra a régi forrásrétegből, mert a #123 migrációja úgyis felváltja; az N86 (1) ugyanezt nyitott
kérdésként tartja. A mért különbség ezeken: a 2/b-n túl a teljes F78 szerep-sorrendű váz (KIRALY-001 +1 174,
MENNY-001 +1 608, HODIT-001 +775, TEREMT-001 +951, HAMART-001 +3 204 diff-sor; a törzscikkeken is 193–968). Ezért az 5
régi sablonú lap (KIRALY-001, MENNY-001, HODIT-001, HAMART-001, TEREMT-001) és a törzscikkek nem változnak. Négyükön
(a TEREMT-001 kivételével) a 2/b a G15 helyőrzőjét hordozza; a generátor ezt üresnek veszi, tehát a lap első
újragenerálásakor (a #123 migrációja, a HAMART-001-nél a #609) magától lekerül. Addig a 31. szabály ott JELENTÉS.

Fixpont: `general.py --cel lexikon --id <ID> --ellenoriz` a 4 lapon „változatlan”.

## 5. A kiadott lapok átnézése (DT569)

A kiadott lapokon (ISTENTISZT-001, ALVIL-001, ANTROP-001) a lapdiff a main-hez képest (`git diff -U0`) kizárólag:

**kizárólag a 2/b generált rés kiesése** (laponként 10 törölt sor, a fenti span; `git diff --stat`: 4 fájl, 40
törlés, 0 beszúrás). Próza (kézi rés: Kivonat, Miért fontos, Értelmezés, 6/b, Módszertan), adat és szerkezet egyéb része nem változott.
A DT569 (a) mércéje — gépi, a prózát és a szerkezetet nem érintő változás után nem kell újra kérdezni — teljesül:
a felhasználó átnézése érvényes marad. Az olvasói kapu a 3 kiadott lapon változatlan (ALVIL-001 0 BUKÁS / 13 FIGY,
ANTROP-001 0 / 15, ISTENTISZT-001 24 / 7, mind a main-beli értékkel azonos).

Tudnivaló: az `adat/lap_atnezesek.tsv` az átnézést a lap utolsó commitjához köti (SEMA 2.48), ezért merge után a
Feed 9. kapuja a 3 lapra új, a DT569-re hivatkozó sort kér. (A main mai állapotában sincs a táblában sor az
ISTENTISZT-001 és az ALVIL-001 utolsó commitjára, `ef04ec94`, sem az ANTROP-001-ére, `7c6ec946`.) A sort a felhasználó
idézetével az orkesztrátor írja; ez az ág nem ír a táblába.

A 11. szabály (rés-forrás egyezés) a régi sablonú lapon álló G15 helyőrzőt — ahol az elvárt rés már üres — nem
jelzi kétszer: az a 31. szabály esete.

## 6. Kapuk

| Kapu | Eredmény |
|---|---|
| `python eszkozok/ellenoriz.py` | kilépés 0 — RENDBEN 20, SÉRTÉS 0, KÉZI 2, JELENTÉS 9; a 11. (rés-forrás egyezés) RENDBEN; a 31. JELENTÉS (4: HAMART-001, HODIT-001, KIRALY-001, MENNY-001 — régi sablonú lapok, l. 4.) |
| `python eszkozok/olvasoi_kapu.py --osszes` | a 4 újragenerált lapon a main-nel azonos (a végleges lapokon újramérve) (ALVIL 0/13, ANTROP 0/15, ISTENTISZT 24/7, TEREMT-002 17/28); nincs új BUKÁS |
| `python eszkozok/ellenorzes/futtat.py` (E2–E30) | kilépés 0 — E2–E33: 0 HIBA (JELENTÉS: E12 916, E13 205, E25 3, E27 42, mind a változástól független); PR-cím `[ELLENŐRZŐ]` előtaggal (E16), a törölt fejléc `TÖRLÉS-SZÁNDÉKOS:` jelöléssel (E5), az E28 a lapok saját dátumával egyezik |
| `teszt_ellenoriz_31.py`, `teszt_ellenoriz_11.py`, `teszt_lexikon_adatres.py` | OK (9, 6, 27 teszt) |
| `teszt_ellenoriz_vedokorlat`, `teszt_szerepmatrix`, `teszt_szotari_gerinc` | 1 + 3 + 5 bukás — **a main-en is megvan** (az eredeti generátorral ugyanez a 9 bukás; adatszám-eltérések, pl. 22 ≠ 33 igehely), nem e változás okozza |

## 7. A main behozása után (#617, #620; 2026-11-04)

- Ütközés csak az `eszkozok/ellenoriz.py`-ban volt (a szabályok definíciója és a `main()` hívássora): kézzel feloldva, **mindkét szabály megmaradt** — a #617 28. („Nincs „egyéb” az 1/b. blokkban”) és ez a 31.; a hívássorban a 28. a 31. előtt.
- A generált lapok automatikusan beolvadtak; a 4 migrált lap a saját dátumával (`PARDES_DATUM=2026-11-03`) újragenerálva: mind a négy **változatlan** (fixpont), az E28 egyezik.
- **A 2/b blokk a merge után is lekerült mind a 4 migrált lapról** (ISTENTISZT-001, ALVIL-001, ANTROP-001, TEREMT-002; a main-hez képest 4 × 10 törölt sor, más változás nincs). A „### 2/b” fejléc az 5 régi sablonú lapon áll (KIRALY-001, MENNY-001, HODIT-001, HAMART-001: G15 helyőrző, a 31. szabály ott JELENTÉS; TEREMT-001: valódi kézi 2/b) — DT507 (a), l. 4.
- Kapuk a merge után: `ellenoriz.py` kilépés 0 (RENDBEN 21, SÉRTÉS 0, KÉZI 2, JELENTÉS 9; 11. RENDBEN, 28. RENDBEN, 31. JELENTÉS 4); `futtat.py` E2–E33 0 HIBA; olvasói kapu ISTENTISZT 24/7, ALVIL 0/13, ANTROP 0/9 (a #617 javította a FIGY-et), TEREMT-002 17/28; tesztek (31, 11, adatres, szerep_kizart) OK.
