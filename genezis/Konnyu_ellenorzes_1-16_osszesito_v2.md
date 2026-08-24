# Könnyű, célzott ellenőrzés — Genezis-sorozat (1Móz 1-16), 20 bővített tanulmány — v2 (teljes per-vers)

*v2 — 2026.08.24 (a 7 korábban "range-wide" formátumú tanulmány 2. pontja átalakítva pontos, versre bontott formátumra [ld. `genezis/Konnyu_ellenorzes_1-16_osszesito.md` v1-es feltárása alapján], majd a teljes 20 tanulmányra újra lefuttatva a könnyű ellenőrzés — most már MINDEN tanulmány per-vers alapon ellenőrzött, nincs benne "range-wide" gyengébb ellenőrzés)*

**FONTOS — ez a fájl is kizárólag feltáró jellegű.** A `Karoli_Strong_kivonat.tsv` join-tábla feltöltése ennek a futásnak NEM része — az egy külön, következő lépés.

## Mi változott a v1-hez képest

A v1-es feltárás (`Konnyu_ellenorzes_1-16_osszesito.md`) 7 tanulmányt "range-wide" formátumban talált (nincs "Vers" oszlop a 2. pont táblázatában, csak a teljes tanulmányozott szakaszra vonatkozott az ellenőrzés). Ezt a 7 tanulmányt (1Móz 1:1, 1:2-2:3, 2:4-7, 2:8-25, 3:1-6, 3:7-24, 12:1-20) átalakítottuk: minden szóhoz pontos, egyértelmű igehelyet rendeltünk, a tanulmány saját szövege (versre tagolt idézetek, alcímek) és a `konkordancia/TAHOT_kivonat.tsv` alapján.

**7 esetben a szó a vizsgált szakaszon belül több versben is előfordult, és a tanulmány szövege nem specifikálta egyértelműen, melyikre gondolt elsődlegesen — ezeket "TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ" jelöléssel dokumentáltuk a tanulmányokban, NEM találgattunk:**

| Tanulmány | Szó | Érintett versek |
|---|---|---|
| 1Móz 1:2-2:3 | צֶלֶם (celem, "képmás") | 1:26 / 1:27 |
| 1Móz 2:8-25 | גַּן (gan, "kert") | 2:8 / 2:9 |
| 1Móz 2:8-25 | עֵזֶר כְּנֶגְדּוֹ ("hozzá illő segítő") | 2:18 / 2:20 |
| 1Móz 2:8-25 | צֵלָע (cela, "oldalborda") | 2:21 / 2:22 |
| 1Móz 2:8-25 | אִשָּׁה (issá, "asszony") | 2:22 / 2:23 |
| 1Móz 3:1-6 | נָחָשׁ (nachás, "kígyó") | 3:1 / 3:2 / 3:4 |
| 1Móz 12:1-20 | מִזְבֵּחַ (mizbéach, "oltár") | 12:7 / 12:8 |

Emellett az 1Móz 3:7-24 tanulmánynál a korábban talált ELTÉRÉS (עֵרֻמִּם, H6174 vs. tényleges H5903) **tisztázódott, de nem lett automatikusan javítva** — lásd a "Kiemelt figyelem" szakaszt lent.

Minden más módszertani szabály (Strong-szám normalizálása, kereszthivatkozás-ellenőrzés bold/zárójeles idézet-felismeréssel) változatlan a v1-hez képest.

---

## Összesítő táblázat

| Tanulmány | 2. pont: megerősített szavak | 2. pont: ELTÉRÉS | 3/b: ÚJ jelölt kapcsolódás |
|---|---|---|---|
| 1Móz 1:1 | 5/5 | — | 6 |
| 1Móz 1:2-2:3 | 18/18 | — | 7 |
| 1Móz 2:4-7 | 7/7 | — | 1 |
| 1Móz 2:8-25 | 14/14 | — | 8 |
| 1Móz 3:1-6 | 8/8 | — | 2 |
| 1Móz 3:7-24 | 18/19 | **1** | 9 |
| 1Móz 4:1-24 | 11/12 | **1** | 0 |
| 1Móz 4:25-5:32 | 7/7 | — | 2 |
| 1Móz 6:1-8 | 11/11 | — | 5 |
| 1Móz 6:9-22 | 10/10 | — | 2 |
| 1Móz 7:1-24 | 6/6 | — | 1 |
| 1Móz 8:1-22 | 7/7 | — | 3 |
| 1Móz 9:1-17 | 7/7 | — | 5 |
| 1Móz 9:18-29 | 6/6 | — | 2 |
| 1Móz 10:1-11:32 | 9/9 | — | 1 |
| 1Móz 12:1-20 | 9/9 | — | 6 |
| 1Móz 13:1-18 | 7/7 | — | 4 |
| 1Móz 14 | 7/7 | — | 4 |
| 1Móz 15 | 11/11 | — | 11 (⚠️ lásd megjegyzés — 1 valószínűleg hamis pozitívum) |
| 1Móz 16 | 7/7 | — | 2 |
| **Összesen** | **185/193** | **2** | **81** |

*(A v1-hez képest a "megerősített" és "eltérés" számok változatlanok — a per-vers átalakítás nem módosította a Strong-adatot. Az "ÚJ JELÖLT" összesített száma 104-ről 81-re csökkent: a range-wide ellenőrzés korábban a teljes szakasz MINDEN versére lekérdezte a kereszthivatkozásokat, míg a per-vers ellenőrzés csak a ténylegesen táblázatba vett kulcsversekre — ez pontosabb, szűkebb, célzottabb listát ad.)*

---

## Kiemelt figyelem — 1Móz 3:7-24, az ELTÉRÉS tisztázása

A v.7-es עֵרֻמִּם ("meztelenek") szónál a tanulmány H6174-et ad meg, a `TAHOT_kivonat.tsv` szerint Gen.3.7 tényleges Strong-száma H5903. A pontosítás során kiderült: **H6174 valójában Gen.2.25 helyes Strong-száma** (ugyanaz a fogalom, de egy másik, disambiguated maszoréta alak) — nem elgépelésről (H6174↔H6175 összekeverés), hanem egy másik vers Strong-számának átvételéről van szó. A teljes indoklás és az emberi döntést igénylő kérdés a tanulmányfájl végén, külön szakaszban dokumentálva (`genezis/1Moz_3v7-24_bovitett.md`).

A másik korábbi ELTÉRÉS (1Móz 4:1-24, הֶבֶל/Ábel neve, H1892 vs. H1893) változatlan — ez a tanulmány nem volt a "range-wide" hét között, per-vers formátumú volt már a v1-es futásnál is.

---

## Részletes szakasz — ÚJ JELÖLT kapcsolódások tanulmányonként

*(Ugyanaz a módszertan, mint a v1-ben: a `Karoli_kereszthivatkozasok.tsv`-ben szereplő, de a tanulmány 3/b pontja által jelenleg nem idézett kapcsolódások. Tartalmi értékelés nem történt.)*

**1Móz 1:1** (6): Gen.2.4-Gen.2.5 (1Móz 2,4-5) · Psa.89.12 (Zsolt 89,12) · Psa.136.5 (Zsolt 136,5) · Act.14.15 (Csel 14,15) · Act.17.24 (Csel 17,24) · Job.33.4 (Jób 33,4)

**1Móz 1:2-2:3** (7): 2Co.4.6 (2Kor 4,6) · Gen.5.1-Gen.5.1 (1Móz 5,1) · 1Co.11.7 (1Kor 11,7) · Col.3.10 (Kol 3,10) · Mat.19.4 (Máté 19,4) · Mrk.10.6 (Márk 10,6) · Exo.20.11 (2Móz 20,11)

**1Móz 2:4-7** (1): 1Co.15.45-1Co.15.47 (1Kor 15,45-47)

**1Móz 2:8-25** (8): Rev.2.7 (Jel 2,7) · Ecc.4.9 (Préd 4,9) · 1Co.11.8 (1Kor 11,8) · Mat.19.5 (Máté 19,5) · Mrk.10.7 (Márk 10,7) · 1Co.6.16 (1Kor 6,16) · Eph.5.31 (Eféz 5,31) · Gen.3.7 (1Móz 3,7)

**1Móz 3:1-6** (2): Jhn.8.44 (Ján 8,44) · 1Ti.2.14 (1Tim 2,14)

**1Móz 3:7-24** (9): Gen.2.25 (1Móz 2,25) · Isa.65.25 (Ésa 65,25) · Mic.7.17 (Mik 7,17) · 1Jn.3.8 (1Ján 3,8) · 1Co.14.34 (1Kor 14,34) · 1Ti.2.11-1Ti.2.12 (1Tim 2,11-12) · 1Pe.3.5 (1Pét 3,5) · Psa.146.4 (Zsolt 146,4) · 2Th.3.10 (2Thess 3,10)

**1Móz 4:1-24** (0): —

**1Móz 4:25-5:32** (2): Gen.1.26 (1Móz 1,26) · Gen.9.6 (1Móz 9,6)

**1Móz 6:1-8** (5): Mat.24.38 (Máté 24,38) · Luk.17.27 (Luk 17,27) · Gen.8.21 (1Móz 8,21) · Jer.17.9 (Jer 17,9) · Mat.15.19 (Máté 15,19)

**1Móz 6:9-22** (2): 1Pe.3.20 (1Pét 3,20) · 2Pe.2.5 (2Pét 2,5)

**1Móz 7:1-24** (1): 2Pe.2.5 (2Pét 2,5)

**1Móz 8:1-22** (3): Gen.6.5 (1Móz 6,5) · Isa.54.9 (Ésa 54,9) · Mat.15.19 (Máté 15,19)

**1Móz 9:1-17** (5): Lev.17.14 (3Móz 17,14) · Deu.12.23 (5Móz 12,23) · Mat.26.52 (Máté 26,52) · Rev.13.10 (Jel 13,10) · Isa.54.9 (Ésa 54,9)

**1Móz 9:18-29** (2): Jos.17.13 (Józs 17,13) · Jdg.1.28 (Bír 1,28)

**1Móz 10:1-11:32** (1): 1Ch.1.10 (1Krón 1,10)

**1Móz 12:1-20** (6): Act.7.3 (Csel 7,3) · Heb.11.8-Heb.11.9 (Zsid 11,8-9) · Jos.24.3 (Józs 24,3) · Gen.18.18 (1Móz 18,18) · Isa.51.2 (Ésa 51,2) · Act.3.25 (Csel 3,25)

**1Móz 13:1-18** (4): Gen.12.8 (1Móz 12,8) · Ezk.16.49 (Ezék 16,49) · Rom.4.17 (Róm 4,17) · Heb.11.12 (Zsid 11,12)

**1Móz 14** (4): Heb.7.1-Heb.7.2 (Zsid 7,1-2) · Heb.7.3 (Zsid 7,3) · Heb.7.2-Heb.7.4 (Zsid 7,2-4) · Heb.7.6 (Zsid 7,6)

**1Móz 15** (11, ⚠️ 1 valószínűleg hamis pozitívum — lásd v1-es megjegyzés): Psa.18.3 (Zsolt 18,3) · Isa.41.10 (Ésa 41,10) · Jas.2.23 (Jak 2,23) · Act.7.6 (Csel 7,6) · Exo.12.40 (2Móz 12,40, kétszer) · Gen.12.7 (1Móz 12,7) · Gen.13.15 (1Móz 13,15) · Gen.26.4 (1Móz 26,4) · Deu.34.4 (5Móz 34,4) · 2Ch.9.26 (2Krón 9,26)

**1Móz 16** (2): Gen.24.62 (1Móz 24,62) · Gen.25.11 (1Móz 25,11)

---

## Összefoglalás

- **20 tanulmány** ellenőrizve, **mind a 20 most már per-vers formátumban** (0 range-wide).
- **7 tanulmány 2. pontja átalakítva** pontos vers-hozzárendeléssel (1Móz 1:1, 1:2-2:3, 2:4-7, 2:8-25, 3:1-6, 3:7-24, 12:1-20).
- **7 szónál "TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ"** eset — a táblázatban felsorolva, emberi döntésre várva.
- **185 kulcsszó "megerősítve"** — változatlan a v1-hez képest.
- **2 "ELTÉRÉS TALÁLVA"** — az 1Móz 3:7-24-es eset most tisztázva (nem elgépelés, hanem másik vers Strong-számának átvétele), de emberi döntésre vár mindkettő.
- **81 "ÚJ JELÖLT TALÁLVA"** kereszthivatkozás (a v1-es 104-ről csökkent, mert a per-vers ellenőrzés célzottabb, csak a ténylegesen táblázatba vett verseket nézi).
- A `Karoli_Strong_kivonat.tsv` join-tábla feltöltése **nem történt meg** — ez egy külön, következő lépés.
