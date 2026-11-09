# F181 jelentés — a Károli-KH jelölt szintjének mérése, a beemelési szabály és alkalmazása

*Végrehajtó: `claude-sonnet-5-5`. Ág: `claude/f181-karoli-kh-jeloltek`. 2026-11-09.*
*scope=konkordancia/Karoli_KH_javitott.tsv (szint=jelolt) + konkordancia/Karoli_KH_MEK.tsv + konkordancia/Karoli_kereszthivatkozasok.tsv + konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv + konkordancia/Karoli_1908.tsv + konkordancia/Karoli_KH_MEK_versszerkezet.tsv + konkordancia/TSK_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_mek.py jelolt-bontas | ts=2026-11-09*

*Az 1–6. szakasz a #177 utáni (J4 előtti) táblán készült: `git show d3252809:konkordancia/Karoli_KH_javitott.tsv` (az F181.1 commit), a mérés `python eszkozok/karoli_kh_mek.py jelolt-bontas --be <ez a fájl>`.*

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

## 2. A szabály (J2) kimenete, soronként

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

* **Elírás-gyanús beemelés:** 15 beemelt MEK-sor áll olyan HunKar-sorral párban, amelytől egyetlen összetevőben (könyv/fejezet/versszám) tér el, és a MEK-cél létezik. Ezekben a MEK-elírás is lehet (pl. 5Móz 21:23 → Gal 2:13 a Gal 3:13 helyett); a szabály a MEK-et fogadja el (a felhasználó előírása), a HunKar-párja `kiesik` lesz. Bontás: könyv-elírás 2, fejezet-elírás 8, versszám-elírás 5. Ez a szabály tudott ára; a J3 szúrópróba ezt méri.
* **Tartomány-végpontok:** 9 beemelt MEK-sor a HunKar-tartomány végpontja vagy annak szomszédja; a HunKar a tartományt egy sorban adja, a MEK két végponttal, ezért a beemelt végpontsor és a `kiesik` tartománysor együtt azonos tartalmat hordozhat (a lap/index oldalán összevonandó).
* **A fogyasztók nem látják a MEK-oldali megerősített sort.** A `karoli_kh_szuro.elfogad(forras, cel)` és a hívói (`lekerdez.py`, `sqlite_epit.py`, `olvaso_pilot/adat.py`, `nav_kinyer.py`) a `Karoli_kereszthivatkozasok.tsv` sorait szűrik; a csak a MEK-ben álló, most `megerositett` sorok nincsenek abban a táblában, ezért a lapra/indexbe csak a fogyasztók bővítésével jutnának (N-F177a körébe tartozik; ez a menet nem módosítja őket).

## 5. A jelölt szint súlya

* A tábla sorai: 35204; ebből `jelolt`: **2863** (8.1%).
* Forrásversek a táblában: 19849; legalább egy `megerositett` sora van: 13120; legalább egy `jelolt` sora van: **1530**.
* **Jelölt nélkül nem marad megerősített KH-ja: 51 vers** (a jelölt versek 3.3%-a); ezek közül 0 versnek van `kiesik` sora is, 51 versnek csak jelölt sora van.
* A szabály 1379 forrásversen emel be sort; ebből 13 versnek ezzel lesz először megerősített KH-ja (a `megerositett` szint 13120 forrásversét 0.1%-kal bővíti).

## 6. Példák (kategóriánként legfeljebb 8, egyenletes minta a tábla sorrendjéből)

Jelölés: `forrásvers → cél`; partner: a másik oldal párosított sora; TSK: a saját cél (mai szabály / tiszta; csak tájékoztatás); L: a cél létezik; gy: gyanús (H: HunKar-oldali, M: MEK-oldali).

### beemel (MEK-sor -> megerositett) (2594 sor)

* Gen.21.2 → Gen.18.10 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 2Sa.6.10 → 1Ch.13.13 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 2Ch.8.6 → 1Ki.7.12 | MEK | altípus: csak MEK | TSK nem/nem | L: igen
* Isa.1.16 → Jas.4.8 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Jol.2.32 → Oba.1.17 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Jhn.17.12 → Psa.41.10 | MEK | altípus: csak MEK | TSK nem/nem | L: igen
* 1Co.7.10 → Mat.5.32 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 1Jn.2.2 → Jhn.4.42 | MEK | altípus: csak MEK | TSK igen/igen | L: igen

### marad: gyanús ismétlődő (86 sor)

* Gen.48.4 → Gen.28.13 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ki.2.32 → 2Sa.20.10 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ch.17.9 → 2Ki.21.14 | MEK | altípus: csak MEK | TSK nem/nem | L: igen | gy: H
* Psa.18.31 → Psa.12.7 | MEK | altípus: csak MEK | TSK igen/nem | L: igen | gy: H
* Ecc.1.1 → Ecc.1.12 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: H
* Jer.25.31 → Jer.15.6 | MEK | altípus: csak MEK | TSK nem/nem | L: igen | gy: H
* Mrk.11.17 → Jer.7.11 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Co.6.7 → 1Th.5.15 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: H

### marad: nem létező célvers (139 sor)

* Exo.6.3 → Gen.16.17 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Jos.24.7 → Exo.15.19-Exo.15.29 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK nem/nem | L: nem
* 2Ch.35.27 → 2Ki.22.28 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Psa.80.15 → Isa.64.9-Isa.64.12 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK nem/nem | L: nem
* Isa.19.25 → Gen.12.23 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Ezk.23.32 → 2Ki.16.23 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Col.2.12 → Rom.4.17-Rom.4.26 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK igen/igen | L: nem
* Psa.24.5 → Isa.18.18 | MEK | altípus: csak MEK | TSK nem/nem | L: nem

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

## 7. A maradék szúrópróbája és a kontroll (J3)

*scope=konkordancia/Karoli_KH_javitott.tsv (a J4 utáni állapot) + konkordancia/Karoli_1908.tsv | forras=eszkozok/karoli_kh_mek.py szuroproba (mag=181) + a végrehajtó olvasata | ts=2026-11-09*

**Módszer.** A minta könyvenként arányos (legnagyobb maradék módszere), rögzített maggal ismételhető (`python eszkozok/karoli_kh_mek.py szuroproba`). Rétegek: (1) a gyanús ismétlődésként jelöltben maradt 86 MEK-oldali sorból 30; (2) a HunKar-oldali, jelöltben maradt 14 sor mind; (3) **kontroll**: a szabály által beemelt 2 594 sorból 40 (a szabály hibaarányának mérésére). A 139 nem létező célvers sort nem mintázom: tételesen az A. függelék. Az ítélet a két vers (Károli) szövegének olvasata: **rendben** = a cél a forrásvers idézete, párhuzama vagy szoros témai kapcsolata; **gyenge** = laza, de védhető kapcsolat; **hiba** = nincs felismerhető kapcsolat. **Korlát:** az ítélet a végrehajtó (nem független) olvasata, a `fuggetlen-ellenor` nem helyettesíti; olyan elírást, amely véletlenül értelmes helyre mutat, nem fog meg. A hibaarány ezért alsó becslés.

| réteg | n | rendben | gyenge | hiba | hibaarány | 95% Wilson-felső |
|---|---|---|---|---|---|---|
| maradék: gyanús ismétlődő | 30 | 25 | 5 | 0 | 0.0% | 11.4% |
| maradék: HunKar-sor jelölt marad (mind) | 14 | 9 | 4 | 1 | 7.1% | 31.5% |
| kontroll: beemelt MEK-sor | 40 | 35 | 5 | 0 | 0.0% | 8.8% |

**Mit mutat.** (1) A gyanús ismétlődésként jelöltben tartott MEK-sorok mintájában **egyetlen hiba sincs** (30-ból 25 rendben, 5 gyenge): a kizárás itt döntően jó sort tart vissza. Oka: a 86 sorból 80 a **HunKar-oldali** gyanús-jelölés miatt marad (a #177 gyanús halmaza a HunKar-lista másoltságát jelzi, a MEK-lista ilyenkor pont a javító tanú); csak 6 sor esik a MEK-oldali ismétlődés alá. **Javaslat a felhasználónak (döntés kell, DT-F181d értelmezése):** a gyanús ismétlődés kizárása legyen csak MEK-oldali (a 80 HunKar-oldali sor beemelődne). (2) A jelöltben maradt HunKar-oldali sorok 14-ből 9 rendben, 4 gyenge, 1 hiba: a HunKar-sor itt többnyire helyes, a MEK-párja nem létező vers (MEK-elírás), tehát a „jelölt marad” helyes választás. (3) A beemelés kontrollmintájában 40-ből 0 hiba (35 rendben, 5 gyenge), a Wilson-felső korlát 8,8%.

**Célzott réteg: az elírás-gyanús beemelések (15 sor).** Ahol a beemelt MEK-sor egyetlen összetevőben tér el a forrásvers HunKar-sorától (l. 4. szakasz), külön, tételesen olvastam mind a 15-öt (a 7. szakasz sorszámai az `elo.tsv` szerinti sorrend; a pár: forrásvers / MEK-cél / HunKar-pár):

| forrásvers | MEK-cél | HunKar-pár | olvasat |
|---|---|---|---|
| Jos.2.15 | Act.9.25 | Act.9.2 | a MEK helyes (kosárban a falon át), a HunKar-pár téves |
| Jos.2.15 | 2Co.11.25 | Act.11.25 | bizonytalan (mindkettő laza; a helyes 2Kor 11:33) |
| Psa.27.4 | Psa.23.2 | Psa.42.2-3 | a MEK hibás (a HunKar-pár a jobb) |
| Psa.27.4 | Psa.23.3 | Psa.42.2-3 | a MEK hibás |
| Psa.34.18 | Psa.9.10 | Psa.32.10 | a MEK elfogadható (a kővár a szükség idején) |
| Psa.35.12 | Psa.38.10 | Psa.41.10 | bizonytalan |
| Isa.5.30 | Amo.8.1 | Amo.8.10 | a MEK hibás |
| Isa.53.7 | Psa.38.10 | Psa.39.10 | a MEK hibás (a „megnémultam” a Zsolt 39:10) |
| Php.3.4 | 2Co.11.21 | Rom.11.21 | a MEK helyes (testi dicsekvés) |
| 1Th.3.9 | 1Th.2.19 | 1Th.2.19–2.3 (tartomány-szemét) | a MEK helyes, a HunKar-sor hibás tartomány |
| 1Pe.2.20 | Luk.12.47 | Luk.12.47–12.15 (tartomány-szemét) | a MEK elfogadható |
| 1Pe.2.20 | Luk.15.14 | Luk.3.14–17 | bizonytalan |
| 1Pe.2.20 | Luk.15.17 | Luk.3.14–17 | bizonytalan |
| 1Jn.2.27 | Jhn.14.26 | Jhn.14.26–14.16 (tartomány-szemét) | a MEK helyes |
| 1Jn.2.27 | Jhn.16.13 | Jhn.14.13 | a MEK helyes (a Lélek tanít) |

Összesítve: a MEK **helyes/elfogadható 7**, **hibás 4** (Zsolt 27:4 → Zsolt 23:2 és 23:3, Ézs 5:30 → Ám 8:1, Ézs 53:7 → Zsolt 38:10), **bizonytalan 4**. A 15 sor a beemelt sorok 0,6%-a; a 4 hibás sor a 2 594-nek 0,15%-a, és mind létező célverset hordoz (a versellenőrzés nem fogja meg). **Ajánlás:** a 15 elírás-gyanús sor (vagy legalább a 4 hibás) maradjon `jelolt`; ez szűkítés lenne a felhasználó szabályán, ezért a J4-ben **nem** alkalmaztam, hanem jelzem (a 15 sor azonosítható: `altipus` ∈ könyv-/fejezet-/versszám-elírás, MEK-oldali, beemelt).

## A. függelék — a nem létező célvers miatt jelöltben maradó sorok (tételesen, 139)

Forrásvers → cél; „egyező”: a HunKar és a MEK ugyanazt a nem létező célt hordozza (a hibás tartomány-végpont). Mérés: `Karoli_1908` ∪ MEK-versszerkezet.

* Exo.6.3 → Gen.16.17
* Lev.19.6 → Lev.7.15-Lev.7.48 (egyező)
* Lev.23.17 → Lev.2.17 — HunKar-pár: Lev.2.12
* Lev.26.14 → Deu.18.15-Deu.18.58 (egyező)
* Num.26.64 → Num.1.64
* Num.27.3 → Gen.32.35
* Deu.4.6 → Psa.111.25
* Deu.4.35 → Isa.18.22
* Deu.31.21 → Ezk.19.21
* Deu.32.39 → Isa.18.22
* Jos.6.25 → Jos.6.32
* Jos.8.34 → Deu.27.15-Deu.27.28 (egyező)
* Jos.8.34 → Deu.27.68
* Jos.22.3 → Jos.11.28 — HunKar-pár: Jos.11.18
* Jos.22.20 → Jos.20.21
* Jos.22.20 → Jos.20.24
* Jos.22.20 → Jos.20.26
* Jos.24.7 → Exo.15.19-Exo.15.29 (egyező)
* Jos.24.11 → Jos.20.21
* Jdg.6.22 → Jdg.13.22-Jdg.13.33 (egyező)
* 1Sa.31.11 → 2Sa.2.45
* 2Sa.7.8 → 
* 2Sa.23.3 → Deu.30.21
* 1Ki.2.26 → 1Sa.22.33
* 1Ki.5.12 → 1Ki.4.29-1Ki.4.39 (egyező)
* 2Ki.21.5 → 
* 1Ch.6.14 → 
* 1Ch.11.11 → 1Sa.23.8-1Sa.23.39 (egyező)
* 1Ch.15.19 → Psa.73.74
* 1Ch.15.19 → Psa.73.75
* 1Ch.28.8 → Num.28.1-Num.28.68 (egyező)
* 2Ch.32.32 → Isa.36.37
* 2Ch.32.32 → Isa.36.38
* 2Ch.35.27 → 2Ki.22.1-2Ki.22.23 (egyező)
* 2Ch.35.27 → 2Ki.22.28
* Ezr.9.12 → Ezr.1.19
* Neh.1.5 → Neh.4.32 — HunKar-pár: Neh.9.32
* Neh.8.9 → Neh.10.65
* Neh.8.9 → Neh.10.70
* Neh.12.28 → Ezr.1.22
* Neh.13.10 → Neh.5.12-Neh.5.47 (egyező)
* Est.1.19 → Dan.12.15
* Job.26.6 → Psa.138.8-Psa.138.12 (egyező)
* Psa.9.12 → Psa.133.13
* Psa.9.12 → Psa.133.14
* Psa.26.8 → Psa.42.23
* Psa.27.4 → Psa.23.42
* Psa.34.18 → Psa.9.32
* Psa.35.12 → Psa.38.41
* Psa.37.37 → Psa.20.44
* Psa.49.15 → Psa.58.13
* Psa.55.6 → 2Sa.21.11-2Sa.21.23 (egyező)
* Psa.80.15 → Isa.64.9-Isa.64.12 (egyező)
* Psa.93.1 → Psa.97.13
* Psa.104.26 → Job.25.13
* Psa.105.13 → Gen.20.26
* Psa.106.39 → Jdg.10.18-Jdg.10.19 (egyező)
* Psa.107.34 → Deu.24.38
* Psa.107.34 → Deu.24.42
* Psa.126.4 → 2Ch.16.35
* Psa.129.6 → Isa.36.37
* Psa.138.7 → Psa.16.17
* Psa.141.7 → Isa.27.19
* Psa.143.3 → 1Sa.23.78 — HunKar-pár: 1Sa.23.7-1Sa.23.8
* Psa.145.18 → Psa.50.51
* Pro.11.17 → Pro.11.25-Pro.11.37 (egyező)
* Ecc.7.15 → Psa.63.4-Psa.63.17 (egyező)
* Isa.1.1 → 2Ch.26.29
* Isa.1.24 → Deu.23.63
* Isa.19.25 → Gen.12.23
* Isa.42.7 → Luk.4.48
* Isa.45.1 → 2Ch.22.23
* Isa.47.6 → Isa.4.16
* Isa.53.7 → Psa.38.39
* Isa.55.12 → Isa.35.12
* Isa.65.15 → Num.5.51
* Jer.7.3 → 2Ch.19.21
* Jer.9.26 → Isa.15.18
* Jer.49.1 → Num.19.38
* Jer.50.2 → Isa.39.46
* Ezk.10.2 → Ezk.9.3-Ezk.9.16 (egyező)
* Ezk.11.19 → Jer.2.32-Jer.2.39 (egyező)
* Ezk.16.8 → Deu.26.27
* Ezk.20.36 → Num.27.64
* Ezk.20.36 → Num.27.65
* Ezk.21.12 → 2Ki.7.19-2Ki.7.21 (egyező)
* Ezk.23.32 → 2Ki.16.23
* Ezk.23.32 → 2Ki.16.24
* Ezk.36.22 → Isa.33.25
* Hos.2.17 → Mic.4.34
* Hos.4.10 → Hos.12.16
* Amo.7.8 → Amo.8.28
* Mal.2.15 → Gen.2.24-Gen.2.28 (egyező)
* Mat.23.12 → Isa.21.31
* Mrk.1.44 → Deu.14.2-Deu.14.32 (egyező)
* Luk.23.30 → Rev.6.19
* Jhn.8.12 → Jhn.9.46 — HunKar-pár: Jhn.12.46
* Act.14.22 → Act.11.43 — HunKar-pár: Act.13.43
* Act.21.8 → Act.12.26 — HunKar-pár: Act.8.26-Act.8.40
* Act.21.8 → Act.12.40 — HunKar-pár: Act.8.26-Act.8.40
* 1Co.1.20 → Job.17.20
* 2Co.8.16 → 1Co.16.57
* Eph.2.12 → Gen.12.23
* Eph.2.20 → Isa.18.16 — HunKar-pár: Isa.28.16
* Col.2.12 → Rom.4.17-Rom.4.26 (egyező)
* 1Th.1.5 → 1Co.2.20
* 2Pe.3.14 → Col.1.32
* Rev.16.5 → Rev.4.17
* Exo.6.20 → Exo.26.59
* Exo.30.1 → Exo.37.35
* Deu.7.15 → Gen.15.26
* 2Sa.19.40 → 2Sa.11.41
* 2Sa.19.40 → 2Sa.11.43
* 2Ch.34.14 → Deu.21.24
* 2Ch.34.14 → Deu.21.26
* Job.7.14 → Job.23.21
* Job.13.24 → Psa.8.15
* Job.34.29 → Rom.8.61
* Job.37.12 → Job.26.27
* Job.37.12 → Job.26.28
* Psa.9.16 → Psa.16.17
* Psa.24.5 → Isa.18.18
* Psa.106.40 → Psa.78.79
* Psa.142.3 → Psa.2.19
* Psa.143.6 → Psa.63.20
* Pro.5.3 → Pro.2.26
* Pro.15.18 → Pro.26.32
* Isa.13.1 → Isa.46.47
* Isa.42.8 → Isa.18.11
* Jer.37.5 → Jer.24.31
* Ezk.5.17 → Deu.26.22
* Ezk.28.24 → Num.35.55
* Ezk.28.24 → Num.35.56
* Dan.10.9 → Dan.8.28
* Amo.9.13 → Hos.2.23
* Mat.6.6 → 2Co.4.33
* Mat.12.1 → Deu.23.26
* Mat.12.40 → Jon.2.12
* Mrk.12.8 → Psa.13.12

## 8. A J4 Δ-naplója (a tábla frissítése)

*scope=konkordancia/Karoli_KH_javitott.tsv | forras=eszkozok/karoli_kh_mek.py beemel | ts=2026-11-09*

```
sorok: 35204 -> 35204
megerositett: 21314 -> 23908 (Δ +2594)
kiesik: 11027 -> 11057 (Δ +30)
jelolt: 2863 -> 239 (Δ -2624)
átment jelolt -> kiesik: 30
átment jelolt -> megerositett: 2594
```

A 239 jelölt maradék: 139 nem létező célvers (ebből 22 egyező), 86 gyanús ismétlődő, 14 HunKar-oldali. A `osszevet` (a beemeléssel) és a `beemel` kimenete bájtra azonos; a `beemel` a kész táblán idempotens (mérve). A szűrő (`karoli_kh_szuro.py`) és a fogyasztók változatlanok; lap nem generálódott.
