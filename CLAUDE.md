# Bible-Study — belépési pont

PaRDeS-módszerű bibliai motívumkutatás. **A hosszú távú termék egy motívum-indexelt,
kereszthivatkozott motívumlexikon; a tanulmányok ennek előállítási folyamata.**
Ebből következik a rendszer egyetlen fő szabálya: *a kereszthivatkozás adat, a tanulmány
és a lexikon pedig ennek az adatnak a nézete.*

Nyelv: minden fájl, commit-üzenet és válasz **magyarul**.

## Ezt olvasd, ezt ne

**Ne olvasd be egyben** a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md`-t (96 KB) —
ez a szabály 2026.09.13-tól **nem érvényes**. A fájl archívum; szakaszonként nyisd meg,
a `Rendszerfejlesztesi_playbook.md` 1. pontjának táblázata szerint. Ugyanígy ne olvasd be
a két changelogot (`PaRDeS_dontesek_CHANGELOG.md`, `motivumlog/PaRDeS_motivumok_CHANGELOG.md`)
és a felfüggesztett SzPA-join dokumentációt, hacsak a feladat nem azokról szól.

| Feladat | Amit megnyitsz |
|---|---|
| bármi | ez a fájl + `NYITOTT_FELADATOK.md` |
| adattábla írása/olvasása | `adat/SEMA.md` |
| tanulmányírás | a megfelelő `sablonok/` fájl + `sablonok/PaRDeS_gyorsreferencia.md` |
| lexikai kutatás | `adat/datasetek.tsv` + `konkordancia/README.md` |
| új dataset, licenc | `Rendszerfejlesztesi_playbook.md` 2. pont |
| rendszer-átalakítás | `ATALAKITASI_TERV.md.md` (fázisok: 6. szakasz) |

## Rétegek — a réteghatár egyetlen kérdés: ki írja?

| Réteg | Hol | Szabály |
|---|---|---|
| **adat** — kanonikus igazságforrás | `adat/*.tsv` | séma szerint; ha itt és egy .md-ben ellentmondás van, **ez az irányadó** |
| **forrás** — kézzel írt | `tematikus_lezart/`, `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `motivumlog/[ID].md` | szabadon szerkeszthető |
| **kimenet** — generált | l. `ATALAKITASI_TERV.md.md` 1.C | **kézzel szerkeszteni tilos**; a forrás javul, és újragenerálódik |

Generált fájl fejlécében gépi jelölés áll (`# GENERÁLT: …`). Ha ilyet látsz, ne írd át.

## Három szabály, amit soha ne sérts

1. **Proveniencia.** Minden lekérdezésből származó állítás mellé a lekérdezés saját
   proveniencia-sora kerül (`scope=… | forras=… | ts=…`). Ha nem futott lekérdezés, az
   érték `manual` — **nem üres, és nem „ellenőrizve"**.
2. **Nincs közvetlen út.** Keresési találatból nem lehet közvetlenül study-táblázat sor.
   Minden jelölt a `adat/jeloltek.tsv`-n megy át, döntéssel és indoklással.
3. **Memória vs. lekérdezés.** Amit nem a repó adata mond, az értelmezés. Hiányt **soha
   ne tölts ki** gyenge vagy asszociatív anyaggal — az üres eredmény elfogadható kimenet,
   és explicit jelölendő.

*Mindhárom megsértésének dokumentált esete van; l. `adat/SEMA.md` 1.5 és 2.4.1.*

## Kutatási menet — a hét lépés

A sorrend maga a védelem a hígulás ellen: **a gerincet mindig le kell vezetni, és a
levezetést dokumentálni kell — akkor is, ha üres az eredmény.**

1. **gerinc-metszet** (közös Strong-halmaz, `adat/grammatikai_strongok.tsv` szűréssel)
2. **szemantikai mező-hipotézis** — az egyetlen *generatív* lépés; a mező-szavak a naplóba kerülnek
3. **teljes ÓSZ/ÚSZ scan** · 4. **kollokáció** (szópár egy versben) · 5. **igealak-ellenőrzés** · 6. **LXX-híd**
7. **nevesített tanító** (web) — önálló menet, saját fájl

Az 1., 3-6. lépés determinisztikus: CLI-ből fut, tehát mindig lefut. Minden
előfordulás-sornak meg kell tudnia nevezni, **melyik gerinc-elemen lóg** (`gerinc_elem`).
Ha nem tudja, a `jeloltek.tsv`-ben marad.

## Új motívum-ID kiosztása — négy kérdés, kötelezően

1. **Mi az azonosság hordozója?** `lexikai` / `formulaikus` / `referenciális` / `fogalmi` /
   `strukturális`
2. **Mi az a minimális jegy, amely nélkül egy igehely NEM tartozik ide?** (negatív kritérium)
3. **Ha egy igehely két motívumhoz is tartozik: különbözik-e a funkciója?** Ha a funkció is
   azonos → egy motívum két néven.
4. **Részhalmaz-e?** Ha B minden előfordulása benne van A-ban → B nem új ID, hanem ↳ alpont.

Plusz a **fölérendelt fogalom** megnevezése: az a tágabb kategória, amely felé a motívum
hígulni fog. Minden új sornál: *csak ezen keresztül tartozik ide?* Ha igen, kizárandó.
**A határt a kizárások rajzolják meg, nem a meghatározás.**

## Adat-tár

`konkordancia/` — 387 MB, 17 dataset; kötelezőségük study-típusonként: `adat/datasetek.tsv`.
Három korlát, amit tudnod kell:

- **`TAHOT_kivonat.tsv` nem teljes**, bár a README annak mondja (hiányzik legalább
  1Móz 32, Zsolt 88/89/140/142, Jóel 3) — minden „teljes körű scan" ennyivel gyengébb.
- **`KJV_/ASV_Strongs`** csak Genezis, Exodus, Példabeszédek.
- **SDBH / SDGNT** (szemantikai domének) **még nincs importálva**.

Nyers adat soha ne kerüljön a fő szál kontextusába — csak kivonat.

**Igehely-formátum:** `1Móz 3:16`, `Mt 24:38`. Három dataset viszont STEPBible-alakot
használ (`Gen.1.1`): `Karoli_kereszthivatkozasok.tsv`, `Karoli_Strong_kivonat.tsv`,
`TIPNR_kivonat.tsv`. Köztük a `konkordancia/Konyv_normalizalo_tabla.tsv` konvertál —
**normalizálás nélkül néma nem-találatot kapsz**, nem hibát.

**Git:** munkaág `main`; commit-üzenet magyarul, tétel-azonosítóval kezdve (`F1.4: …`);
push csak kérésre.
