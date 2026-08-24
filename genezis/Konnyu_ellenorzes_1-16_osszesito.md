# Könnyű, célzott ellenőrzés — Genezis-sorozat (1Móz 1-16), 20 bővített tanulmány

*v1 — 2026.08.24 (első lefuttatás: 20 tanulmány ellenőrizve a 2. pont [Strong-adat] és a 3/b pont [kereszthivatkozás] területén, a jelenlegi STEPBible/Károli-infrastruktúrával [TAHOT_kivonat.tsv, Karoli_kereszthivatkozasok.tsv] összevetve — 185 szó megerősítve, 2 valódi eltérés, 104 új kereszthivatkozási jelölt, 27 sor kihagyva [nincs önálló Strong-szám])*

**FONTOS — ez a fájl kizárólag feltáró jellegű.** Egyetlen tanulmányfájl vagy motívumlog-bejegyzés sem lett módosítva ennek a futásnak a során. A cél egy tiszta helyzetkép, ami alapján utólag, külön döntünk arról, mely tanulmányoknál szükséges mélyebb emberi felülvizsgálat.

## Módszertan és korlátok

- **20 tanulmányfájl** lett ellenőrizve (a `genezis/` mappa mind az 1Móz 1-16 tartományba eső bővített tanulmánya — a feladatkiírás "16 tanulmányt" említett, de a tényleges fájlszám 20, mert néhány korai fejezet több, szűkebb szakaszra bontva készült; ez a teljes 1-16 tartomány lefedettségét nem érinti).
- **2. pont (Strong-adat) ellenőrzése:** a tanulmány táblázatában megadott Strong-számot összevetettük a `konkordancia/TAHOT_kivonat.tsv` tényleges adatával. Két táblaformátum fordul elő:
  - **"per-vers" (13 tanulmány):** a táblázat "Vers" oszlopa megadja, melyik igehelyhez tartozik az adott szó — ekkor pontosan arra a versre történt az ellenőrzés.
  - **"range-wide" (7 tanulmány):** a táblázatban nincs verset azonosító oszlop (`1v1`, `1v2-2v3`, `2v4-7`, `2v8-25`, `3v1-6`, `3v7-24`, `12v1-20`) — ekkor a teljes tanulmányozott igeszakaszon belül *bárhol* kerestük a Strong-számot. Ez egy gyengébb, de még mindig értelmes ellenőrzés: ha egy Strong-szám sehol sem fordul elő a teljes szakaszban, az önmagában is figyelemre méltó.
  - **Homográf-jelölés és vezető nullák (pl. `H430` vs `H0430`) normalizálva lettek** összehasonlítás előtt — ezek nem számítanak eltérésnek.
  - **27 sor ki lett hagyva** az összevetésből, mert a tanulmány explicit jelezte, hogy a szónak nincs önálló Strong-száma (funkciószó, pl. tárgyeset-jelölő *ét*).
- **3/b pont (kereszthivatkozás) ellenőrzése:** minden tanulmány "kulcsversére" (a 2. pontban szereplő, ill. range-wide táblázatnál a teljes szakasz összes versére) lekérdeztük a `konkordancia/Karoli_kereszthivatkozasok.tsv` teljes hivatkozás-listáját, és összevetettük azzal, amit a tanulmány 3/b pontja már ténylegesen idéz. A már idézett hivatkozásokat két formában kerestük: a szokásos **félkövér inline** formában (`**Zsid 11:3**`) és az idézet utáni **zárójeles** formában (`(Zsid 11:8)`) — mindkettő előfordul a korpuszban. **Korlát:** ha egy hivatkozás csak prózai, összefűzött felsorolásban szerepel (pl. "1Móz 15:6 ↔ Róm 4:1-25 ↔ Gal 3:6 ↔ Jak 2:23"), azt a szkript nem ismeri fel idézetként — ez néhány "ÚJ JELÖLT" tételnél hamis pozitívumot okozhat (lásd lent, 1Móz 15-nél jelezve).
- **Tartomány-hivatkozások (pl. `Heb.7.1-Heb.7.2`) külön jelöltként szerepelnek**, még akkor is, ha a tartomány egy már idézett egyedi verset (pl. `Heb.7.2`) tartalmaz — ez tudatos döntés: a tartomány tágabb kontextust ad, ezért érdemes külön jelölni, nem automatikusan duplikátumnak tekinteni.

---

## Összesítő táblázat

| Tanulmány | 2. pont: megerősített szavak | 2. pont: ELTÉRÉS | 3/b: ÚJ jelölt kapcsolódás |
|---|---|---|---|
| 1Móz 1:1 | 5/5 | — | 6 |
| 1Móz 1:2-2:3 | 18/18 | — | 24 |
| 1Móz 2:4-7 | 7/7 | — | 1 |
| 1Móz 2:8-25 | 14/14 | — | 10 |
| 1Móz 3:1-6 | 8/8 | — | 2 |
| 1Móz 3:7-24 | 18/19 | **1** | 11 |
| 1Móz 4:1-24 | 11/12 | **1** | 0 |
| 1Móz 4:25-5:32 | 7/7 | — | 2 |
| 1Móz 6:1-8 | 11/11 | — | 5 |
| 1Móz 6:9-22 | 10/10 | — | 2 |
| 1Móz 7:1-24 | 6/6 | — | 1 |
| 1Móz 8:1-22 | 7/7 | — | 3 |
| 1Móz 9:1-17 | 7/7 | — | 5 |
| 1Móz 9:18-29 | 6/6 | — | 2 |
| 1Móz 10:1-11:32 | 9/9 | — | 1 |
| 1Móz 12:1-20 | 9/9 | — | 8 |
| 1Móz 13:1-18 | 7/7 | — | 4 |
| 1Móz 14 | 7/7 | — | 4 |
| 1Móz 15 | 11/11 | — | 11 (⚠️ lásd megjegyzés lent — 1 valószínűleg hamis pozitívum) |
| 1Móz 16 | 7/7 | — | 2 |
| **Összesen** | **185/193** | **2** | **104** |

---

## Részletes szakasz — csak azok a tanulmányok, ahol ELTÉRÉS vagy ÚJ JELÖLT előkerült

### ⚠️ ELTÉRÉS TALÁLVA (2 eset — emberi döntést igényel)

**1Móz 3:7-24 — עֵרֻמִּם ("meztelen")**
- A tanulmány Strong-száma: **H6174**
- A `TAHOT_kivonat.tsv` tényleges adata Gen.3.7-nél (és ugyanígy Gen.3.10, 3.11-nél): **H5903** (עֵירֹם, "naked")
- **Megjegyzés:** a héber szövegben ismert szójáték áll fenn a קָרוּם/עָרוּם *arum* ("ravasz" — a kígyó jelzője, 3:1, Strong **H6175**) és az עֵירֹם *erom* ("meztelen" — Ádám és Éva állapota, 3:7/10/11, Strong **H5903**) között. A tanulmány H6174 száma egyik fenti Strong-számmal sem egyezik pontosan (közel van H6175-höz) — érdemes megvizsgálni, hogy elgépelés történt-e (H6174→H6175), vagy a tanulmány szándékosan egy másik, rokon alakra hivatkozott.

**1Móz 4:1-24 — הֶבֶל (Ábel neve)**
- A tanulmány Strong-száma: **H1892** (a köznévi "hiábavalóság/pára" jelentésű alak, pl. Prédikátor könyvében)
- A `TAHOT_kivonat.tsv` tényleges adata Gen.4.2-nél: **H1893** (ugyanaz a szótő, de a tulajdonnévi — "Ábel" — disambiguated alak)
- **Megjegyzés:** ez valószínűleg **nem hiba, hanem tudatos választás** — a tanulmány feltehetően a névetimológiai kapcsolatot (Ábel neve = "pára/mulandóság") akarta hangsúlyozni a köznévi Strong-számmal, hasonlóan a döntési fájl 4.11-es pontjában már dokumentált H2895/H2896 (טוֹב-gyök) kettős lehetőséghez. Emberi döntés kell hozzá, hogy a join-táblába melyik kerüljön (vö. a `Karoli_Strong_kivonat.tsv` "bizonytalan" megbízhatósági kategóriája, 4.13 pont).

### ÚJ JELÖLT kapcsolódások — tanulmányonként

*(Az "ÚJ JELÖLT" azt jelenti: a `Karoli_kereszthivatkozasok.tsv`-ben szerepel egy kapcsolódás a tanulmány valamelyik kulcsverséhez, de a tanulmány 3/b pontja jelenleg nem idézi. Tartalmi értékelés — lexikai vagy csak tematikus — nem történt, ez emberi/tanulmány-szintű döntés.)*

**1Móz 1:1** (6): Gen.2.4-Gen.2.5 (1Móz 2,4-5) · Psa.89.12 (Zsolt 89,12) · Psa.136.5 (Zsolt 136,5) · Act.14.15 (Csel 14,15) · Act.17.24 (Csel 17,24) · Job.33.4 (Jób 33,4)

**1Móz 1:2-2:3** (24): 2Co.4.6 (2Kor 4,6) · Isa.45.7 (Ésa 45,7) · Jer.10.12 (Jer 10,12) · Jer.51.15 (Jer 51,15) · Psa.148.4 (Zsolt 148,4) · Job.38.8 (Jób 38,8) · Psa.33.6-Psa.33.7 (Zsolt 33,6-7) · Psa.33.9 (Zsolt 33,9) · Psa.136.6 (Zsolt 136,6) · Psa.95.5 (Zsolt 95,5) · Psa.104.19 (Zsolt 104,19) · Jer.31.35 (Jer 31,35) · Psa.136.7-Psa.136.9 (Zsolt 136,7-9) · Gen.8.17 (1Móz 8,17) · Gen.5.1 (1Móz 5,1) · 1Co.11.7 (1Kor 11,7) · Col.3.10 (Kol 3,10) · Mat.19.4 (Máté 19,4) · Mrk.10.6 (Márk 10,6) · Gen.9.3 (1Móz 9,3) · Psa.115.16 (Zsolt 115,16) · Psa.104.14 (Zsolt 104,14) · Isa.40.26 (Ésa 40,26) · Exo.20.11 (2Móz 20,11)

**1Móz 2:4-7** (1): 1Co.15.45-1Co.15.47 (1Kor 15,45-47)

**1Móz 2:8-25** (10): Rev.2.7 (Jel 2,7) · Dan.10.4 (Dán 10,4) · Rom.5.12 (Róm 5,12) · Ecc.4.9 (Préd 4,9) · 1Co.11.8 (1Kor 11,8) · Mat.19.5 (Máté 19,5) · Mrk.10.7 (Márk 10,7) · 1Co.6.16 (1Kor 6,16) · Eph.5.31 (Eféz 5,31) · Gen.3.7 (1Móz 3,7)

**1Móz 3:1-6** (2): Jhn.8.44 (Ján 8,44) · 1Ti.2.14 (1Tim 2,14)

**1Móz 3:7-24** (11): Gen.2.25 (1Móz 2,25) · Rev.12.9 (Jel 12,9) · Isa.65.25 (Ésa 65,25) · Mic.7.17 (Mik 7,17) · 1Jn.3.8 (1Ján 3,8) · 1Co.14.34 (1Kor 14,34) · 1Ti.2.11-1Ti.2.12 (1Tim 2,11-12) · 1Pe.3.5 (1Pét 3,5) · Gen.4.12 (1Móz 4,12) · Psa.146.4 (Zsolt 146,4) · 2Th.3.10 (2Thess 3,10)

**1Móz 4:1-24** (0): —

**1Móz 4:25-5:32** (2): Gen.1.26 (1Móz 1,26) · Gen.9.6 (1Móz 9,6)

**1Móz 6:1-8** (5): Mat.24.38 (Máté 24,38) · Luk.17.27 (Luk 17,27) · Gen.8.21 (1Móz 8,21) · Jer.17.9 (Jer 17,9) · Mat.15.19 (Máté 15,19)

**1Móz 6:9-22** (2): 1Pe.3.20 (1Pét 3,20) · 2Pe.2.5 (2Pét 2,5)

**1Móz 7:1-24** (1): 2Pe.2.5 (2Pét 2,5)

**1Móz 8:1-22** (3): Gen.6.5 (1Móz 6,5) · Isa.54.9 (Ésa 54,9) · Mat.15.19 (Máté 15,19)

**1Móz 9:1-17** (5): Lev.17.14 (3Móz 17,14) · Deu.12.23 (5Móz 12,23) · Mat.26.52 (Máté 26,52) · Rev.13.10 (Jel 13,10) · Isa.54.9 (Ésa 54,9)

**1Móz 9:18-29** (2): Jos.17.13 (Józs 17,13) · Jdg.1.28 (Bír 1,28)

**1Móz 10:1-11:32** (1): 1Ch.1.10 (1Krón 1,10)

**1Móz 12:1-20** (8): Act.7.3 (Csel 7,3) · Heb.11.8-Heb.11.9 (Zsid 11,8-9) · Jos.24.3 (Józs 24,3) · Gen.18.18 (1Móz 18,18) · Isa.51.2 (Ésa 51,2) · Act.3.25 (Csel 3,25) · Gen.20.2 (1Móz 20,2) · Gen.26.7 (1Móz 26,7)

**1Móz 13:1-18** (4): Gen.12.8 (1Móz 12,8) · Ezk.16.49 (Ezék 16,49) · Rom.4.17 (Róm 4,17) · Heb.11.12 (Zsid 11,12)

**1Móz 14** (4): Heb.7.1-Heb.7.2 (Zsid 7,1-2) · Heb.7.3 (Zsid 7,3) · Heb.7.2-Heb.7.4 (Zsid 7,2-4) · Heb.7.6 (Zsid 7,6)

**1Móz 15** (11, ⚠️ 1 valószínűleg hamis pozitívum — lásd alább): Psa.18.3 (Zsolt 18,3) · Isa.41.10 (Ésa 41,10) · **Jas.2.23 (Jak 2,23) — a tanulmány prózában, összefűzött felsorolásban ("1Móz 15:6 ↔ Róm 4:1-25 ↔ Gal 3:6 ↔ Jak 2:23") már megemlíti, csak nem formális 3/b idézetblokként; emberi mérlegelés kell, számít-e "már kezeltnek"** · Act.7.6 (Csel 7,6) · Exo.12.40 (2Móz 12,40, kétszer is jelöltként, 15:13 és 15:16 versekhez) · Gen.12.7 (1Móz 12,7) · Gen.13.15 (1Móz 13,15) · Gen.26.4 (1Móz 26,4) · Deu.34.4 (5Móz 34,4) · 2Ch.9.26 (2Krón 9,26)

**1Móz 16** (2): Gen.24.62 (1Móz 24,62) · Gen.25.11 (1Móz 25,11)

---

## Összefoglalás

- **20 tanulmány** ellenőrizve (1Móz 1-16 teljes lefedettséggel).
- **185 kulcsszó "megerősítve"** — a tanulmány Strong-száma egyezik a TAHOT-adattal.
- **2 "ELTÉRÉS TALÁLVA"** — 1Móz 3:7-24 (עֵרֻמִּם, H6174 vs tényleges H5903) és 1Móz 4:1-24 (הֶבֶל, H1892 vs tényleges H1893) — mindkettő emberi döntést igényel, egyik sem lett automatikusan javítva.
- **104 "ÚJ JELÖLT TALÁLVA"** kereszthivatkozás — egyik sem lett tartalmilag értékelve, ez teljes egészében nyitva marad jövőbeli, tanulmány-szintű mérlegelésre.
- **27 sor kihagyva** (funkciószó, nincs önálló Strong-szám).
