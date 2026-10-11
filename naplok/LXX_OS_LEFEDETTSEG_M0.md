# LXX_OS_LEFEDETTSEG — M0 felmérés (csak olvas)

*F54 · M0 · 2026.10.11 · modell: sonnet · a mérés `manual` proveniencia: gépi összevetés, nem `lekerdez.py`-kimenet.*

Versenkénti tábla: `naplok/LXX_OS_LEFEDETTSEG_osztalyozas.tsv` (503 sor). Generátor: `naplok/LXX_OS_LEFEDETTSEG_M0_general.py` (csak olvas; a régi `LXX_kivonat` a törlés előtti git-állapotból, `0c2d1b44^`, kizárólag összehasonlítási bizonyítékként).

`scope=naplok/FORRASKIVEZETES_M5_eltereslista.tsv (kategoria=csak_regi_vers, 503 vers); konkordancia/LXX_OS/*.tsv; konkordancia/Karoli_versmegfeleltetes.tsv; konkordancia/Karoli_1908.tsv | forras=manual (naplok/LXX_OS_LEFEDETTSEG_M0_general.py) | ts=2026-10-11`

## 1. Eredmény

| Könyv | A | B | C | bizonytalan | össz |
|---|---|---|---|---|---|
| Jób | 61 | 0 | 2 | 15 | 78 |
| Zsolt | 65 | 0 | 0 | 1 | 66 |
| Jer | 55 | 2 | 0 | 2 | 59 |
| Hós | 57 | 0 | 0 | 0 | 57 |
| Péld | 22 | 0 | 1 | 27 | 50 |
| 2Móz | 34 | 0 | 0 | 12 | 46 |
| 1Sám | 34 | 0 | 0 | 0 | 34 |
| Dán | 30 | 0 | 0 | 0 | 30 |
| Én | 26 | 0 | 2 | 0 | 28 |
| Józs | 27 | 0 | 0 | 0 | 27 |
| Ézs | 23 | 1 | 0 | 0 | 24 |
| Jón | 2 | 0 | 0 | 0 | 2 |
| 4Móz | 1 | 0 | 0 | 0 | 1 |
| 1Kir | 1 | 0 | 0 | 0 | 1 |
| **össz** | **438** | **3** | **5** | **57** | **503** |

**Az előfelmérés hipotézise igazolódott:** a rés túlnyomó része (438 / 503 = 87%) nem görög hiány, hanem kulcsolási rés — a görög vers megvan az `LXX_OS`-ben, de nincs Károli-kulcsa.

### A osztály, alosztályonként (a kulcs forrása szerint)

| Alosztály | db | Kulcsforrás | Hol |
|---|---|---|---|
| **A1_tabla** | 204 | `Karoli_versmegfeleltetes.tsv` sora → `igehely_kjv` → az egyetlen nem kulcsolt LXX-vers ezzel a kjv-vel; alátámasztás: a régi szöveg szóalak-Jaccardja, a sorrend-beágyazás vagy a fejezet-szószámkorreláció | 1Sám 17 (32), Józs 8 (27), Jer 33/48 (55), Jób 38 (38), Péld 18 (22), Ézs 9/56 (12), Hós 11 (11), 2Móz 37–38, … |
| **A1_zsolt_cim** | 65 | ugyanaz a tábla; a rés az 1. (cím)vers, amelyet a dup-KJV-cél szabály zár ki az importból (két LXX-vers mutat ugyanarra a kjv-célra, csak a magasabb kapja a kulcsot); a 3 kétcímű zsoltárnál (51, 52, 60) a 2. cím sorrendi párosítással | 62 zsoltár `N:1` + 51:2, 52:2, 60:2 |
| **A3_sorrend_beagyazas** | 39 | nincs egyértelmű tábla-jelölt, de a nem kulcsolt Károli-szakasz és a nem kulcsolt LXX-szakasz a kulcsolt szomszédok között azonos hosszú (adatból levezethető, tábla nélkül) | Én 5/6 (26), Ézs 64 (10), Ézs 63:19, Jón 2:1, 1Sám 24:1 |
| **A2_tabla_nelkul** | 130 | **nincs tábla-sor** (a `Karoli_versmegfeleltetes.tsv`-ből a fejezet hiányzik); a párosítás független fejezet-szószámkorrelációból (r ≥ 0,70, az ellentmondó párosítástól ≥ 0,15 különbség), LXX-fejezeten belüli sorszám-eltolásból vagy az `LXX_OS` `igehely_kjv` (TVTMS) hivatkozásából | 2Móz 35 (31, L+0, r=0,81), Dán 3 (30, K+0, r=0,89), Hós 2 (22, L+3, r=0,88), Hós 13 (15, r=0,73), Hós 14 (9, r=0,95), Jób 37 (23, L+1, r=0,70) |

Az A1/A3 versek kulcsa megfeleltető táblán (vagy a kulcsolt szomszédokon) lóg és visszakereshető; az **A2 versekhez ma nincs tábla-sor**, tehát az M1-ben csak új felülbírálati sorral kerülhetnek be — ezért az (a) kérdés.

### B osztály (3 vers — valódi görög hiány)

| Károli | Bizonyíték | Régi szöveg |
|---|---|---|
| Ézs 3:1 | a kulcsolt szomszédok (Ézs 2:21 = Isaiah 2:21, Ézs 3:2 = Isaiah 3:1) között az LXX-szakasz üres, a Károli-szakasz 1 vers; a `Verzifikacios_elteres_tabla.tsv` szerint Isa 2:22 = Károli Ézs 3:1 (IGAZOLVA) | a régi „Ézs 3:1” az Isaiah 3:1 (= Károli 3:2) szövege volt (eltolt) |
| Jer 7:27 | Jer 7:26 = LXX 7:26 és Jer 7:28 = LXX 7:27 között üres az LXX-szakasz; egyetlen LXX-vers `igehely_kjv`-je sem 7:27 | a régi „Jer 7:27” az LXX 7:27 (= Károli 7:28) szövege volt |
| Jer 27:17 | Jer 27:16 = LXX 34:16 és Jer 27:18 = LXX 34:18 között üres az LXX-szakasz; egyetlen LXX-vers kjv-je sem 27:17 | a régi szöveg más vers (LXX 34:14, Károli 27:14) szövege |

### C osztály (5 vers — idegen Károli-kulcs, nem létező Károli-vers)

Jób 17:16, Jób 37:24, Péld 12:28, Én 6:11, Én 6:12: a Károli-fejezetnek nincs ilyen verse (`Karoli_1908.tsv`), a régi kivonat az LXX-számozást vitte át Károli-kulcsként. Kulcs itt nem keletkezhet (K4: idegen kulcs nincs); az LXX-vers marad kulcs nélkül, a `karoli_ok = szamozas_elteres` jelöléssel.

### bizonytalan (57 vers) — maradék üres, nem A

| Hely | db | Ok |
|---|---|---|
| Péld 12 | 27 | nincs tábla-sor; legjobb fejezet-párosítás r=0,45 (L+1) |
| Jób 17 | 15 | nincs tábla-sor; legjobb r=0,41 (L−3); az LXX-Jób ezen a helyen szabadon fogalmaz |
| 2Móz 36 | 11 | nincs tábla-sor; legjobb r=0,67 (K−1) < 0,70; az LXX-2Móz 36–39 a MT-hez képest átrendezett |
| Jer 48:40, 48:41 | 2 | tábla-jelölt egyedi, de a szószám-arány 0,27 (a jelölt lényegesen rövidebb) |
| 2Móz 39:38 | 1 | a tábla-jelölt (Exodus 39:15) ellentmond a régi szövegnek, amely az Exodus 39:16-ra mutat, és az már a 2Móz 39:37 kulcsa |
| Zsolt 13:5 | 1 | az egyetlen jelölt (Psalms (LXX) 12:6, kjv „13:5;13:6”) szószám-aránya 2,55; a Károli 13:5–13:6 egy LXX-versnek felel meg |

## 2. Megfigyelések, amelyek az M1-et érintik

1. **A régi kivonat gyakran nem a Károli-vershez tartozó szöveget adott** (A osztályon belül `regi_helyes = nem`: 129 / 438). Zsoltárok: a 65-ből 51 helyen a régi „Zsolt N:1” a következő (nem-cím) vers szövege volt — az N17-ben leírt egy verssel eltolt zsoltár-kivonat (a 14 egyező eset a kivonatban is cím volt). Hós 2: a régi eltolás +2, a független párosítás +3. Ez azt jelenti, hogy a régi szövegre épülő állítások nem csak „hiányosak”, hanem tartalmilag is eltoltak lehettek (#55 hatóköre).
2. **Meglévő kettős Károli-kulcs az `LXX_OS`-ben: 9 db** (a K4-et ma sérti): 1Krón 12:4, 1Kir 7:1, Préd 2:26, 2Móz 39:1 / 38:30 / 39:40, Jer 25:13 / 49:34, Zsolt 13:1 (LXX 12:1 és 12:2 is `Zsolt 13:1`). A Zsolt 13-ban a meglévő kulcsok egy verssel eltoltak (a Károli 13:n szövege az LXX 12:n; a tábla a Zsolt 13-at KJV-osztályba sorolja, de a Károli a címet számozott versnek veszi). Ez a 503 versen kívül esik, de a K4 (nincs kettős kulcs) teljesüléséhez az M1-nek vagy javítania kell, vagy kivételként dokumentálnia.
3. **Zsolt 54:2** (második feliratvers): a 503-ban nincs (nem `csak_regi_vers`), de a Zsolt 54:1 kulcsolásakor az LXX 53:2 és a Károli 54:2 kulcs nélkül marad — ugyanaz a kétcímű mintázat, mint a 51, 52, 60.
4. **A régi szöveg nem kulcsforrás.** Az osztályozás a régi szöveget csak alátámasztásként használja (szóalak-Jaccard a törölt `LXX_kivonat` git-állapotából); kulcs csak táblán, a sorrend-beágyazáson vagy új, bizonyítékoszlopos felülbírálati soron lóghat (CLAUDE.md 2–3. szabály).
5. **A fejezet-szószámkorreláció gyenge ott, ahol az LXX szabadon fogalmaz** (Jób: Jób 38 r=0,28; az A1-et itt a tábla + a régi szöveg egyezése tartja, az r csak tájékoztató). Ezeket az M2 mintavétele (3 Jób-vers) külön ellenőrzi.

## 3. Módszer és korlátai

- **Táblakeresés:** a Károli-vers sora a `Karoli_versmegfeleltetes.tsv`-ben → `igehely_kjv` → az `LXX_OS` elsődleges fájljának nem kulcsolt versei, amelyeknek `igehely_kjv`-je ezt tartalmazza (pontosvesszős listákkal, pl. „13:5;13:6”).
- **Sorrend-beágyazás:** a Károli-vers legközelebbi kulcsolt Károli-szomszédai → az őket hordozó LXX-versek az `LXX_OS` fájlsorrendjében → az LXX-szakasz és a Károli-szakasz hossza; egyező hossz esetén sorrendi párosítás, üres LXX-szakasz esetén B-bizonyíték.
- **Fejezet-szószámkorreláció (A2):** Pearson r a Károli- és LXX-szószámok között, L-módban (az LXX-fejezeten belüli sorszám-eltolás) és K-módban (az `igehely_kjv` hivatkozás eltolása). Küszöb r ≥ 0,70 és ≥ 0,15 különbség az ellentmondó párosítástól; a jelölt nem lehet már kulcsolt.
- **Korlát:** a szószám-korreláció ténye (Károli vs. LXX szószám) nem tartalmi egyezés. Az A2 és A3 sorok a javaslat, nem az igazolt kulcs; a tartalmi egyezést az M2 ≥ 10 verses mintavétele ellenőrzi (legalább 3 Jób-, 2 Hóseás-, 2 zsoltárvers). A besorolás nem „ellenőrzött” — független ellenőr az M3-ban.
- Az osztályokat gép állapítja meg; a tartalmi (nyelvi) olvasatom nem szerepel a tábla indoklásában.

## 4. ⛔ Megállás — döntések (DT-F54a)

**(a) Az A osztály javításának módja.** A 438 A-vers négy alosztályra oszlik; az egy lépéssel nem fedhető le:
- *Opció 1 (javaslat):* **kétszintű javítás.** (i) az `lxx_os_import.py` besorolása kap két általános szabályt — a *dup-KJV-cél címvers-szabály* (Zsolt N:1, és a kétcímű zsoltárok sorrendi párosítása; A1_zsolt_cim, 65) és a *sorrend-beágyazás* (A3, 39) —, valamint a tábla `igehely_kjv`-kereséséhez a pontosvesszős listák kezelése (A1_tabla, 204); (ii) az A2 (130 vers: 2Móz 35, Dán 3, Hós 2/13/14, Jób 37) fejezetenként a `karoli_vers_felulbiralas.tsv`-be kerül, **bizonyítékoszloppal** (r, a párosítás módja), mert tábla-sor nincs. Előny: az A2 kulcsa nyomon követhető, és a későbbi tábla-bővítés (KK2b) felülírhatja.
- *Opció 2:* az A2 fejezetek sorai a `Karoli_versmegfeleltetes.tsv`-be mennek (a tábla bővítése) — de ez a KK-feladatsor tábláját módosítja, és az `ir` mezőnk nem tartalmazza; külön brief kell.
- *Opció 3:* az A2-t egyelőre nem kulcsoljuk (csak A1+A3, 308 vers), az A2 a `bizonytalan`-nal együtt marad üres.

**(b) A zsoltár-feliratok kulcsolása.** A rés oka igazolódott (65/66 zsoltárvers cím). *Javaslat:* a Károli számozása az irányadó (a cím az 1. vers; ahol két cím van, az első cím az 1., a második a 2. vers); az LXX-cím a megfelelő `Zsolt N:1`-et kapja. *Alternatíva:* a címeket nem kulcsoljuk (`Zsolt N:1` üres marad), mert a feliratok szövegét a motívumkutatás ritkán használja. Ha a javaslat: a Zsolt 54:2 (megfigyelés 3) is bekerül az M1-be, az 503-on kívül.

**(c) A `bizonytalan` (57) és a B (3), C (5) sorok sorsa.** *Javaslat:* maradjanak üresek, explicit `karoli_ok = szamozas_elteres`-sel, listájuk a zárásban (K3: az `lxx-hid` explicit üres eredményt ad). *Alternatíva:* kézi döntés a Péld 12 (27), Jób 17 (15) és 2Móz 36 (11) fejezetekre — ehhez nyelvi/tartalmi egyeztetés kell, amit a CLAUDE.md 3. szabálya miatt nem végeznék memóriából.

**(d) A meglévő 9 kettős kulcs (megfigyelés 2).** *Javaslat:* a K4 teljesüléséhez az M1 a 9 kulcsot is javítja (főleg a Zsolt 13-at, ahol a tábla és a Károli számozása ellentmond), a változtatás külön commitban, a K5 (csak `igehely_karoli`/`karoli_ok` változhat) megőrzésével. *Alternatíva:* kivétel-listaként dokumentáljuk, és külön feladat kapja.
