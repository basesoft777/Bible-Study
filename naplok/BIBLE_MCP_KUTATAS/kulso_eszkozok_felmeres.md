# Külső eszközök felmérése — igehely-felismerés és versszámozás

Dátum: 2026-10-17. Proveniencia: `manual` (forráskód- és dokumentáció-olvasás). Egy mérés futott,
a lekérdezés saját sorával: `scope=BPRP hu könyvnév-regexek × konkordancia/Konyv_normalizalo_tabla.tsv (66 könyv × rövidítés+teljes név) | forras=openbibleinfo/Bible-Passage-Reference-Parser@master esm/lang/hu.js (4.0.0, push 2026-10-16) | ts=2026-10-17`.
Szkript: `naplok/BIBLE_MCP_KUTATAS/bprp_hu_konyvnev_teszt.mjs`. A szkript csak a modul
regex-literáljait olvassa ki és fordítja le, a letöltött kódot nem futtatja.

## Lezáró ítélet (2026-10-17, felhasználói döntés)

**Egyik eszközt sem emeljük be; a téma lezárva.** Ok: a szerver már szerveroldalon linkeli a
kanonikus igehelyeket a saját könyvtáblánkból (`ig_link`, `eszkozok/olvaso_szerver/blokkok.py`), így
az igehely-előnézet egyszerű hover a meglévő `a.igehely` linkeken, saját végponttal, külső felismerő
és CSP-változás nélkül. A szabad próza esetleges felismerése is a `Konyv_normalizalo_tabla.tsv`-re
épülő, szerveroldali Python feladat. A BPRP egyetlen haszna, a független ellenőrzés, nem éri meg
a beemelést. A BibleEngine és a VerseTagger nem ad újat. Az alábbi felmérés indoklásként marad.

---

A felmérés egy előzetes ítélet-táblázat (a beillesztett „4. Külső eszközök” szakasz) állításait
ellenőrzi. Az eredmény: **mindhárom ítélet megáll, de az első eszköz hiánylistája téves és rövidebb
a valósnál, a javasolt sorrend 4. pontja pedig rossz előfeltételre épül.**

## 1. Bible-Passage-Reference-Parser (BPRP)

| Állítás | Ellenőrizve | Eredmény |
|---|---|---|
| MIT | `package.json`, `LICENSE.md` | ✅ MIT, 4.0.0; futásidejű függőség nincs |
| van magyar modulja | `esm/lang/hu.js` (43 KB) + `esm/bcv_parser.js` (196 KB), 116 könyvminta | ✅ |
| hiányzik: JSir, Sof, Agg, 1Ján | mérés (fent) | ⚠️ **részben téves** — l. lent |
| a vesszős íráshoz külön beállítás kell | README, `punctuation_strategy` | ✅ `eu`: a vessző fejezet–vers elválasztó, a pont a sorozat-elválasztó („Mt 1, 2. 4” → Matt.1.2, Matt.1.4) |
| kliensoldali, CSP-vel összefér | `alkalmazas.py:36` (`script-src 'self'`) | ✅ ha a fájlok a `statikus/` alól, helyben szolgálódnak ki; CDN-ről nem |

**A mért hiány.** A repó saját 66 rövidítéséből 7-et nem ismer fel a modul. Mindegyik **néma
nem-találat**, tehát nem dob hibát:

| Repó-alak | Mit ismer helyette a modul |
|---|---|
| `JSir` | Siralm, Siralmak, Jeremiás sir(almai) |
| `Sof` | Szof, Sofoniás, Zofóniás (a „Sofóniás” ó-val **nem**) |
| `Luk` | Lk, Lukács |
| `Ján` | Jn, János |
| `1Ján`, `2Ján`, `3Ján` | 1Jn, 1 János, I. János … |

- Az **`Agg` nem a repó alakja** (a táblában `Hag` áll, és azt a modul felismeri). Az „Agg” a modulban
  valóban nincs meg, csak az Ag, Aggeus, Hag, Haggeus, Haggai. Kézzel írt prózában előfordulhat, ezért pótolni érdemes,
  de nem a mi kulcsunk.
- **A `Luk` és a `Ján` a legsúlyosabb hiány.** Ez a két leggyakoribb evangélium-rövidítés a repó
  igehely-formátumában, és az eredeti lista nem említi.
- A teljes könyvnevek közül 25 nem talál, többnyire a „Mózes első könyve”, „Királyok második
  könyve”, „Rómabeliekhez írt levél” típusú alakok. A modul „1 Mózes”, „Róma” stb. formákat ismer.
  Az olvasói igehely-előnézetnél ez kisebb gond, mert a forrásszövegeink rövidítést használnak.
- A modul **futás közben bővíthető** (`add_books()`), tehát a hiány a forrás módosítása nélkül pótolható:
  a 7 rövidítés és az `Agg` a `Konyv_normalizalo_tabla.tsv`-ből generálható, és nem kézzel tartandó.

**Versszámozás — ez az eredeti javaslat gyenge pontja.** A BPRP versszámozási rendszerei
(`default`, `kjv`, `nrsv`, `vulgate` …) mind angol fordításhagyományok: **MT- és Károli-rendszer
nincs**. A modul *érvényesít* (létezik-e a fejezet/vers), *megfeleltetést nem végez*. A Károli-számozást
nem normalizálással kell elé tenni, hanem **egyedi rendszerként betölteni** (`add_translations()` +
`systems.<név>.chapters`: könyvenként a fejezetek verszáma). Ez a `Karoli_1908.tsv`-ből gépileg
előállítható. Különben várhatóan a modul a Károliban létező, de az angol rendszerben nem létező
verset érvénytelennek veszi (a README szerint az érvénytelen részt alapból figyelmen kívül hagyja,
`invalid_passage_strategy: "ignore"`). Ezt nem mértem, a dokumentációból következik. Az MT↔Károli megfeleltetés marad a
repó dolga (`Karoli_versmegfeleltetes.tsv`, F85); a BPRP-nek ehhez nincs köze.

**Ítélet: hasznos, beemelhető** — három feltétellel: (1) a fájlok helyben, `statikus/` alól,
rögzített verzióval (`@4.0.0` + hash) kerülnek be, és a licenc a `adat/licencek.tsv`-be; (2) az `add_books()`-bővítés
és a Károli-versrendszer a repó adatából generálódik; (3) a modul kimenete OSIS (`John.3.16`),
ezért a `Konyv_normalizalo_tabla.tsv` mellé egy STEP↔OSIS oszlop kell (a mérés szkriptje
már tartalmazza a 66 párost). Független ellenőrnek is jó: ugyanazt a szöveget két
felismerő olvassa, és az eltérés naplózható.

## 2. STEPBible/BibleEngine

| Állítás | Ellenőrizve | Eredmény |
|---|---|---|
| MIT | `package.json` | ⚠️ MIT, de **LICENSE-fájl nincs** a repóban; mintának elég, kódátvételhez kevés |
| TypeScript, második adatbázis | repófa: TypeORM-entitások (`core/src/entities/*.entity.ts`) | ✅ |
| versszámozási szabályok | `importers/src/stepdata/v11n-rules/data/v11n-rules.tsv` (+ `.orig.tsv`, `.diff`, `false-positives.txt`) | ✅ a STEPBible TVTMS egy **saját javításokkal ellátott pillanatképe** |
| szerkezeti modell | `BibleSection`, `BibleParagraph`, `BibleNote`, `BiblePhrase` entitások | ✅ |
| karbantartás | utolsó commit 2025-10-31 | lassú |

**Ítélet: csak mintának** — megáll. Új adat nincs benne: a repó versszámozási kulcsa már
TVTMS-alapú (`Karoli_versmegfeleltetes.tsv` fejléce: `lxx-morph@c91f6b1e…`, „TVTMS-alapú MT-KJV kulcs”).
Egyetlen dolgot érdemes megnézni: a `v11n-rules.diff` és a `false-positives.txt`. Ez a BibleEngine
saját javításlistája a TVTMS-hez, és összevethető a mi `KEZI_ELTOLASOK`-unkkal. Ha ez megtörténik, az csak tanúként szolgál, a `jeloltek.tsv`-n át.

## 3. VerseTagger (bibleengine.org)

**Névütközés:** a bibleengine.org **nem** azonos a STEPBible/BibleEngine-nel. Az előbbi egy önálló, CC0
licencű projekt; a táblázat két sora két különböző szerzőre vonatkozik.

| Állítás | Ellenőrizve | Eredmény |
|---|---|---|
| nem ismeri a magyar könyvneveket | `versetagger.js` (18 KB) + `js/BibleEngine.js` (24 KB) | ✅ angol könyvnevek; ékezetes karakter 0 db |
| KJV-t mutat | a projekt lapja | ✅ KJV, opcióként AKJV |
| külső API, CSP-ütközés | a kód `https://bibleengine.org/api/`-ra kér | ✅ a `default-src 'self'` és `script-src 'self'` mellett nem tölthető be és nem kérhet |

**Ítélet: csak az ötlet** — megáll. A CC0 miatt a hover-viselkedés kódja szabadon átvehető lenne, de
a felismerője angol, és a mi esetünkben a BPRP mindenben jobb alap.

## 4. A javasolt sorrend — egy pontosítás

Az 1–3. pont rendben van. **A 4. pont előfeltétele téves:** az igehely-előnézet nem a
„versszámozási normalizálás után” jön, hanem két, ettől független dolog után:

1. a BPRP-be töltött **Károli-versrendszer** (fejezetenkénti verszámok, a `Karoli_1908.tsv`-ből), és
2. a 7 (+`Agg`) hiányzó rövidítés `add_books()`-pótlása a normalizáló táblából.

Mindkettő generált, kis munka. A versszámozási felmérés (1. pont) a *megfeleltetéshez*
kell (MT/KJV-tanú ↔ Károli). Az előnézet viszont Károli-szöveget mutat Károli-kulccsal, tehát nem
függ tőle. A 4. pont ezért akár a 2. pont mellett is futhat. Az előnézet szövegét saját,
azonos eredetű végpont adja (nem külső API), így a CSP-n nem kell változtatni.

## Nyitott kérdések (nem mért)

- A BPRP nyelvtanát (tartományok, „k.”/„kk.” jelölés, „vö.”) **nem futtattam**, csak a könyvnév-regexeket;
  a magyar prózai szokások (pl. „1Móz 3,16–19; 4,1”) tényleges kezelése egy próbafuttatást igényel.
- Az `Agg` és a teljesnév-hiányok súlya a mi szövegeinkben (hány előfordulás) nincs megszámolva.
