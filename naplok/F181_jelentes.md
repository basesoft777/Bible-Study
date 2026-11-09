# F181 jelentés — a Károli-KH jelölt szintjének mérése, a beemelési szabály és alkalmazása

*Végrehajtó: `claude-sonnet-5-5`. Ág: `claude/f181-karoli-kh-jeloltek`. 2026-11-09.*
*scope=konkordancia/Karoli_KH_javitott.tsv (szint=jelolt) + konkordancia/Karoli_KH_MEK.tsv + konkordancia/Karoli_kereszthivatkozasok.tsv + konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv + konkordancia/Karoli_1908.tsv + konkordancia/Karoli_KH_MEK_versszerkezet.tsv + konkordancia/TSK_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_mek.py jelolt-bontas | ts=2026-11-09*

## 1. A jelölt sorok és az altípusok (J1; mért: 2863 sor)

| altípus | sor | MEK-oldali | HunKar-oldali | egyező |
|---|---|---|---|---|
| tartomány/vershatár | 18 | 9 | 9 | 0 |
| könyv-elírás | 3 | 2 | 1 | 0 |
| fejezet-elírás | 25 | 14 | 11 | 0 |
| versszám-elírás | 20 | 8 | 12 | 0 |
| eltér (nem sorolható) | 37 | 26 | 11 | 0 |
| csak MEK | 2738 | 2738 | 0 | 0 |
| egyéb (egyező, de nem létező hivatkozás) | 22 | 0 | 0 | 22 |
| **összesen** | **2863** | 2797 | 44 | 22 |

Indok-kódok: `csak_mek` 2797, `egyezik` 22, `eltero_lista` 44.
Az altípus a másik oldal **jelölt** soraihoz viszonyít (azonos forrásvers): a MEK-cél és a HunKar-cél egyetlen összetevőben tér el (könyv-/fejezet-/versszám-elírás), vagy a MEK-cél a HunKar-tartományban / egy versnyire áll (tartomány/vershatár). `csak MEK`: a forrásversen nincs jelölt HunKar-sor. `eltér (nem sorolható)`: van másik oldali jelölt sor, de a pár nem áll közel.

Nem létező cél vagy forrásvers (`Karoli_1908` ∪ MEK-versszerkezet szerint): **139** sor.

## 2. A szabály (J2) kimenete, soronként (DT-F181a)

A szabály: a MEK-oldali jelölt sor `megerositett`, **kivéve** (1) a hivatkozott vers vagy a forrásvers nem létezik, (2) a forrásvers gyanús ismétlődő. A HunKar-oldali jelölt sor `kiesik`, ha a forrásverse MEK-listájából legalább egy sor beemelődik; különben jelölt marad. A TSK nem szerepel a szabályban.

| döntés | sor |
|---|---|
| beemel (MEK-sor -> megerositett) | 2594 |
| marad: gyanús ismétlődő | 86 |
| marad: nem létező célvers | 139 |
| HunKar-sor -> kiesik (a MEK-lista elfogadva a versen) | 30 |
| HunKar-sor marad jelölt (a MEK-sor nem emelődik be) | 14 |
| **összesen** | **2863** |

**A három szám (MEK-oldali jelölt sorok: 2797):** bekerül **2594**; gyanús ismétlődésként marad **86**; a nem létező célvers miatt marad **117** (+ 22 egyező-de-nem-létező sor, összesen 139 nem létező célvers).

A gyanús ismétlődés két forrása (a MEK-oldali jelölt sorokon): HunKar-oldali jelölés (a #177 gyanús halmaza, 5078 forrásvers) 80 sor; MEK-oldali ismétlődés (a MEK-lista szó szerint azonos egy másik vers MEK-listájával, ≥2 elem, 496 forrásvers) 6 sor; mindkettő 0 sor. **Figyelem:** a HunKar-oldali jelölés a *HunKar-lista* másoltságát jelzi, nem a MEK-listáét; a szabály (a koordinátori előírás szerint) mégis jelöltben tartja ezeket.
A **nem létező célvers** és a gyanús ismétlődés átfedése: 1 MEK-oldali sor mindkettő; a táblázatban a nem létező célvers az elsőbbségű.

**A HunKar-oldali jelölt sor sorsa (mit választottam és miért).** A #177 `eltero_lista` sora: a HunKar-sor, amelyet a MEK a versen nem listáz, de más hivatkozást igen. Ha a MEK-lista a versen irányadó (a MEK-sor beemelődik), akkor a HunKar-sor a MEK-lista szerint nincs ott: ugyanaz a helyzet, mint a `kiesik` szinten (a MEK a versen nem listázza), ezért `kiesik` lesz (indok: `eltero_lista;tsk=…;szabaly=F181`). Ha a verse egyik MEK-sora sem emelődik be (nem létező cél, gyanús), a HunKar-sor jelölt marad: a verse MEK-listája nincs elfogadva, tehát a HunKar-sor sorsáról sincs mi alapján dönteni (hiányt nem töltünk ki, CLAUDE.md 3. szabály). A `kiesik` itt **nem** jelent hibás HunKar-sort: a sor a MEK-lista elfogadásának következménye (l. 4. az elírás-gyanús párokat). HunKar-oldali jelölt sor: 44; ebből `kiesik`: 30, jelölt marad: 14.

## 3. Keresztábla és könyvenkénti eloszlás

**Altípus × döntés:**

| altípus | beemel (MEK-sor -> megerositett) | marad: gyanús ismétlődő | marad: nem létező célvers | HunKar-sor -> kiesik (a MEK-lista elfogadva a versen) | HunKar-sor marad jelölt (a MEK-sor nem emelődik be) |
|---|---|---|---|---|---|
| tartomány/vershatár | 9 | 0 | 0 | 9 | 0 |
| könyv-elírás | 2 | 0 | 0 | 1 | 0 |
| fejezet-elírás | 8 | 0 | 6 | 9 | 2 |
| versszám-elírás | 5 | 0 | 3 | 9 | 3 |
| eltér (nem sorolható) | 18 | 0 | 8 | 2 | 9 |
| csak MEK | 2552 | 86 | 100 | 0 | 0 |
| egyéb (egyező, de nem létező hivatkozás) | 0 | 0 | 22 | 0 | 0 |

**TSK-támogatás (csak tájékoztatás, nem szabály-feltétel)** — a mai `tsk=` szabály szerint (TSK ±3 vagy visszautalás); „tiszta TSK”: csak a TSK ±3. Kategória: melyik oldal célját támogatja (a sor és a párosított másik oldali sor célja; párosítás nélkül a hiányzó oldal „nem támogatott”).

| altípus | TSK-kategória | cél létezik | cél nem létezik |
|---|---|---|---|
| tartomány/vershatár | mindkettő | 18 | 0 |
| könyv-elírás | csak a MEK-cél | 2 | 0 |
| könyv-elírás | egyik sem | 1 | 0 |
| fejezet-elírás | mindkettő | 3 | 0 |
| fejezet-elírás | csak a MEK-cél | 4 | 0 |
| fejezet-elírás | csak a HunKar-cél | 5 | 6 |
| fejezet-elírás | egyik sem | 7 | 0 |
| versszám-elírás | mindkettő | 2 | 1 |
| versszám-elírás | csak a MEK-cél | 9 | 0 |
| versszám-elírás | csak a HunKar-cél | 2 | 0 |
| versszám-elírás | egyik sem | 4 | 2 |
| eltér (nem sorolható) | csak a MEK-cél | 15 | 3 |
| eltér (nem sorolható) | csak a HunKar-cél | 6 | 0 |
| eltér (nem sorolható) | egyik sem | 8 | 5 |
| csak MEK | csak a MEK-cél | 1981 | 4 |
| csak MEK | egyik sem | 657 | 96 |
| egyéb (egyező, de nem létező hivatkozás) | mindkettő | 0 | 8 |
| egyéb (egyező, de nem létező hivatkozás) | egyik sem | 0 | 14 |

A sor saját céljára mutató TSK-támogatás: mai szabály szerint 2053 sor, ebből tiszta TSK ±3-mal 1986, csak visszautalással 67.

**Könyvenként (a forrásvers könyve szerint):**

| könyv | jelölt | beemel | gyanús | nem létező | HunKar→kiesik | HunKar marad |
|---|---|---|---|---|---|---|
| Gen | 16 | 15 | 1 | 0 | 0 | 0 |
| Exo | 23 | 19 | 1 | 3 | 0 | 0 |
| Lev | 17 | 13 | 0 | 3 | 0 | 1 |
| Num | 35 | 31 | 2 | 2 | 0 | 0 |
| Deu | 103 | 97 | 0 | 5 | 0 | 1 |
| Jos | 127 | 113 | 0 | 9 | 4 | 1 |
| Jdg | 7 | 6 | 0 | 1 | 0 | 0 |
| Rut | 2 | 2 | 0 | 0 | 0 | 0 |
| 1Sa | 11 | 10 | 0 | 1 | 0 | 0 |
| 2Sa | 111 | 101 | 5 | 4 | 1 | 0 |
| 1Ki | 93 | 84 | 7 | 2 | 0 | 0 |
| 2Ki | 62 | 59 | 1 | 1 | 1 | 0 |
| 1Ch | 84 | 69 | 9 | 5 | 1 | 0 |
| 2Ch | 90 | 81 | 3 | 6 | 0 | 0 |
| Ezr | 9 | 8 | 0 | 1 | 0 | 0 |
| Neh | 29 | 23 | 0 | 5 | 1 | 0 |
| Est | 14 | 13 | 0 | 1 | 0 | 0 |
| Job | 23 | 17 | 0 | 6 | 0 | 0 |
| Psa | 198 | 157 | 10 | 27 | 3 | 1 |
| Pro | 56 | 49 | 4 | 3 | 0 | 0 |
| Ecc | 6 | 3 | 2 | 1 | 0 | 0 |
| Isa | 69 | 56 | 0 | 11 | 2 | 0 |
| Jer | 121 | 101 | 14 | 5 | 0 | 1 |
| Ezk | 102 | 89 | 1 | 12 | 0 | 0 |
| Dan | 42 | 40 | 1 | 1 | 0 | 0 |
| Hos | 45 | 43 | 0 | 2 | 0 | 0 |
| Jol | 7 | 7 | 0 | 0 | 0 | 0 |
| Amo | 23 | 21 | 0 | 2 | 0 | 0 |
| Mic | 7 | 7 | 0 | 0 | 0 | 0 |
| Nam | 2 | 2 | 0 | 0 | 0 | 0 |
| Hag | 1 | 1 | 0 | 0 | 0 | 0 |
| Zec | 4 | 4 | 0 | 0 | 0 | 0 |
| Mal | 5 | 4 | 0 | 1 | 0 | 0 |
| Mat | 82 | 76 | 2 | 4 | 0 | 0 |
| Mrk | 29 | 25 | 2 | 2 | 0 | 0 |
| Luk | 106 | 105 | 0 | 1 | 0 | 0 |
| Jhn | 89 | 86 | 0 | 1 | 1 | 1 |
| Act | 226 | 218 | 0 | 3 | 2 | 3 |
| Rom | 43 | 42 | 1 | 0 | 0 | 0 |
| 1Co | 158 | 145 | 12 | 1 | 0 | 0 |
| 2Co | 98 | 94 | 2 | 1 | 1 | 0 |
| Gal | 11 | 11 | 0 | 0 | 0 | 0 |
| Eph | 11 | 7 | 0 | 2 | 1 | 1 |
| Php | 6 | 3 | 0 | 0 | 1 | 2 |
| Col | 14 | 6 | 0 | 1 | 5 | 2 |
| 1Th | 4 | 1 | 0 | 1 | 2 | 0 |
| 1Ti | 7 | 7 | 0 | 0 | 0 | 0 |
| 2Ti | 6 | 6 | 0 | 0 | 0 | 0 |
| Tit | 6 | 5 | 1 | 0 | 0 | 0 |
| Heb | 42 | 40 | 2 | 0 | 0 | 0 |
| Jas | 17 | 17 | 0 | 0 | 0 | 0 |
| 1Pe | 6 | 4 | 0 | 0 | 2 | 0 |
| 2Pe | 30 | 26 | 3 | 1 | 0 | 0 |
| 1Jn | 41 | 39 | 0 | 0 | 2 | 0 |
| 2Jn | 2 | 2 | 0 | 0 | 0 | 0 |
| 3Jn | 2 | 2 | 0 | 0 | 0 | 0 |
| Jud | 6 | 6 | 0 | 0 | 0 | 0 |
| Rev | 277 | 276 | 0 | 1 | 0 | 0 |

## 4. Mire kell figyelni a szabály alkalmazásakor

* **Elírás-gyanús beemelés:** 15 beemelt MEK-sor áll olyan HunKar-sorral párban, amelytől egyetlen összetevőben (könyv/fejezet/versszám) tér el, és a MEK-cél létezik. Ezekben a MEK-elírás is lehet (pl. 5Móz 21:23 → Gal 2:13 a Gal 3:13 helyett); a szabály a MEK-et fogadja el (DT-F181a), a HunKar-párja `kiesik` lesz. Bontás: könyv-elírás 2, fejezet-elírás 8, versszám-elírás 5. Ez a szabály tudott ára; a J3 szúrópróba ezt méri.
* **Tartomány-végpontok:** 9 beemelt MEK-sor a HunKar-tartomány végpontja vagy annak szomszédja; a HunKar a tartományt egy sorban adja, a MEK két végponttal, ezért a beemelt végpontsor és a `kiesik` tartománysor együtt azonos tartalmat hordozhat (a lap/index oldalán összevonandó).
* **A fogyasztók nem látják a MEK-oldali megerősített sort.** A `karoli_kh_szuro.elfogad(forras, cel)` és a hívói (`lekerdez.py`, `sqlite_epit.py`, `olvaso_pilot/adat.py`, `nav_kinyer.py`) a `Karoli_kereszthivatkozasok.tsv` sorait szűrik; a csak a MEK-ben álló, most `megerositett` sorok nincsenek abban a táblában, ezért a lapra/indexbe csak a fogyasztók bővítésével jutnának (N-F177a körébe tartozik; ez a menet nem módosítja őket).

## 5. A jelölt szint súlya

* A tábla sorai: 35204; ebből `jelolt`: **2863** (8.1%).
* Forrásversek a táblában: 19849; legalább egy `megerositett` sora van: 13120; legalább egy `jelolt` sora van: **1530**.
* **Jelölt nélkül nem marad megerősített KH-ja: 51 vers** (a jelölt versek 3.3%-a); ezek közül 0 versnek van `kiesik` sora is, 51 versnek csak jelölt sora van.
* A szabály 1379 forrásversen emel be sort; ebből 13 versnek ezzel lesz először megerősített KH-ja (a `megerositett` szint 13120 forrásversét 0.1%-kal bővíti).

## 6. Példák (kategóriánként legfeljebb 8, egyenletes minta a tábla sorrendjéből)

Jelölés: `forrásvers → cél` [MEK-alak]; partner: a másik oldal párosított sora; TSK: a saját cél (mai szabály / tiszta; csak tájékoztatás); L: a cél létezik; gy: gyanús (H: HunKar-oldali, M: MEK-oldali).

### beemel (MEK-sor -> megerositett) (2594 sor)

* Gen.21.2 → Gen.18.10 [1 Móz. 18,10.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 2Sa.6.10 → 1Ch.13.13 [1 Krón. 13,13.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 2Ch.8.6 → 1Ki.7.12 [1 Kir. 7,12.] | MEK | altípus: csak MEK | TSK nem/nem | L: igen
* Isa.1.16 → Jas.4.8 [Jak. 4,8.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Jol.2.32 → Oba.1.17 [Abd. 1,17.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Jhn.17.12 → Psa.41.10 [Zsolt. 41,10.] | MEK | altípus: csak MEK | TSK nem/nem | L: igen
* 1Co.7.10 → Mat.5.32 [Mát. 5,32.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 1Jn.2.2 → Jhn.4.42 [Ján. 4,42.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen

### marad: gyanús ismétlődő (86 sor)

* Gen.48.4 → Gen.28.13 [1 Móz. 28,13.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ki.2.32 → 2Sa.20.10 [2 Sám. 20,10.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ch.17.9 → 2Ki.21.14 [2 Kir. 21,14.] | MEK | altípus: csak MEK | TSK nem/nem | L: igen | gy: H
* Psa.18.31 → Psa.12.7 [Zsolt. 12,7.] | MEK | altípus: csak MEK | TSK igen/nem | L: igen | gy: H
* Ecc.1.1 → Ecc.1.12 [Préd. 1,12.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: H
* Jer.25.31 → Jer.15.6 [Jer. 15,6.] | MEK | altípus: csak MEK | TSK nem/nem | L: igen | gy: H
* Mrk.11.17 → Jer.7.11 [Jer. 7,11.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Co.6.7 → 1Th.5.15 [1 Thess. 5,15.] | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: H

### marad: nem létező célvers (139 sor)

* Exo.6.3 → Gen.16.17 [1 Móz. 16,17.] | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Jos.24.7 → Exo.15.19-Exo.15.29 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK nem/nem | L: nem
* 2Ch.35.27 → 2Ki.22.28 [2 Kir. 22,28.] | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Psa.80.15 → Isa.64.9-Isa.64.12 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK nem/nem | L: nem
* Isa.19.25 → Gen.12.23 [1 Móz. 12,23.] | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Ezk.23.32 → 2Ki.16.23 [2 Kir. 16,23.] | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Col.2.12 → Rom.4.17-Rom.4.26 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK igen/igen | L: nem
* Psa.24.5 → Isa.18.18 [Ésa. 18,18.] | MEK | altípus: csak MEK | TSK nem/nem | L: nem

### HunKar-sor -> kiesik (a MEK-lista elfogadva a versen) (30 sor)

* Jos.2.15 → Act.9.2 | partner: Act.9.25 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen
* Jos.2.15 → Act.11.25 | partner: Act.9.25 | HunKar | altípus: fejezet-elírás | TSK nem/nem | L: igen
* Neh.1.5 → Neh.9.32 | partner: Neh.4.32 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Isa.5.30 → Amo.8.10 | partner: Amo.8.1 | HunKar | altípus: versszám-elírás | TSK igen/igen | L: igen
* Act.14.22 → Act.13.43 | partner: Act.11.43 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Php.3.4 → Rom.11.21 | partner: 2Co.11.21 | HunKar | altípus: könyv-elírás | TSK nem/nem | L: igen
* Col.4.15 → Phm.1.1-Phm.1.2 | partner: Phm.1.2 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 1Pe.2.20 → Luk.12.47-Luk.12.15 | partner: Luk.12.47 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen

### HunKar-sor marad jelölt (a MEK-sor nem emelődik be) (14 sor)

* Lev.23.17 → Lev.2.12 | partner: Lev.2.17 | HunKar | altípus: versszám-elírás | TSK igen/igen | L: igen
* Deu.28.38 → Hag.1.6 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Psa.143.3 → 1Sa.23.7-1Sa.23.8 | partner: 1Sa.23.78 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen
* Jhn.5.8 → Mrk.2.11 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Act.21.8 → Act.8.12 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Act.21.8 → Act.8.26-Act.8.40 | partner: Act.12.26 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Php.1.3 → Phm.1.4 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Col.1.9 → Col.2.18-Col.2.23 | HunKar | altípus: eltér (nem sorolható) | TSK nem/nem | L: igen

