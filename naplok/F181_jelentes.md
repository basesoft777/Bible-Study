# F181 jelentés — a Károli-KH jelölt szintjének mérése, a beemelési szabály és alkalmazása

*Végrehajtó: `claude-sonnet-5-5`. Ág: `claude/f181-karoli-kh-jeloltek`. 2026-11-09.*
*scope=konkordancia/Karoli_KH_javitott.tsv (szint=jelolt) + konkordancia/Karoli_KH_MEK.tsv + konkordancia/Karoli_kereszthivatkozasok.tsv + konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv + konkordancia/Karoli_1908.tsv + konkordancia/Karoli_KH_MEK_versszerkezet.tsv + konkordancia/TSK_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_mek.py jelolt-bontas | ts=2026-11-09*

*Az 1–6. szakasz a #177 utáni (J4 előtti) táblán készült: `git show d3252809:konkordancia/Karoli_KH_javitott.tsv` (az F181.1 commit; azonos az `osszevet --nyers` kimenetével), a mérés `python eszkozok/karoli_kh_mek.py jelolt-bontas --be <ez a fájl>`; a soronkénti döntés a végleges szabályé (DT-F181d–i). **A javítókör 1 (ELLENOR_F181, 10. szakasz) után az 1–3., 6–8. szakasz és az A. függelék újraszámolva; a 4. szakasz kiegészítve (E3: tartomány-végpontok, E2: hibaminta).** Az első kör számai: `git show 290260f3:naplok/F181_jelentes.md`.*

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

A szabály (a szövege egy helyen: `konkordancia/Karoli_KH_MEK_README.md` 7.): a MEK-oldali jelölt sor `megerositett`, **kivéve** (1) a hivatkozott vers vagy a forrásvers nem létezik, (2) a forrásvers MEK-listája gyanús ismétlődő (a HunKar-oldali gyanús-jelölés nem zár ki), (3) a MEK-cél az E2-hibaminta létező töredéke (DT-F181h), (4) a MEK-cél egyetlen összetevőben tér el a HunKar-céltól (elírás-gyanús). A HunKar-oldali jelölt sor `megerositett`, ha a MEK-párja nem ellentmond neki (E1: a pár célja nem létezik, DT-F181g; E2: az E2-minta megfelelője; E3: a MEK a tartomány egyik végpontját adja, DT-F181i); különben `kiesik`, ha a forrásverse MEK-listájából legalább egy sor beemelődik (kivéve az elírás-gyanús sor párját); egyébként jelölt marad. A TSK nem szerepel a szabályban.

| döntés | sor |
|---|---|
| beemel (MEK-sor -> megerositett) | 2647 |
| marad: MEK-oldali gyanús ismétlődő | 6 |
| marad: nem létező célvers | 136 |
| marad: elírás-gyanús (egyetlen összetevőben tér el a HunKar-céltól) | 10 |
| marad: MEK fejezet-hibaminta (a létező töredék) | 9 |
| HunKar-sor -> kiesik (a MEK-lista elfogadva a versen) | 3 |
| HunKar-sor marad jelölt (a MEK-sor nem emelődik be) | 21 |
| HunKar-sor -> megerositett (a MEK-pár célja nem létezik) | 5 |
| HunKar-sor -> megerositett (a MEK fejezet-hibamintájának megfelelője) | 7 |
| HunKar-tartomány -> megerositett (a MEK az egyik végpontot adja) | 8 |
| MEK-végpontsor -> kiesik (a megerősített HunKar-tartományba olvad) | 11 |
| **összesen** | **2863** |

**A számok (MEK-oldali jelölt sorok: 2797):** bekerül **2647**; gyanús ismétlődésként marad **6**; a nem létező célvers miatt marad **114** (+ 22 egyező-de-nem-létező sor, összesen 136 nem létező célvers); elírás-gyanús osztályként marad **10**; az E2-hibaminta létező töredékeként marad **9**; a megerősített HunKar-tartományba olvad (kiesik) **11**.

A gyanús ismétlődés kizárása csak a **MEK-oldali** ismétlődésre vonatkozik (a MEK-lista szó szerint azonos egy másik vers MEK-listájával, ≥2 elem, 496 forrásvers): 6 sor marad jelölt. A **HunKar-oldali** gyanús-jelölés (a #177 gyanús halmaza, 5078 forrásvers) a HunKar-lista másoltságát jelzi, nem a MEK-listáét; az ilyen forrásversen álló, ismétlődés nélküli MEK-sor (80 sor) a felhasználó döntése szerint beemelődik. A szúrópróba (7. szakasz) szerint ezek mintája hibátlan volt.
A **nem létező célvers** és a gyanús ismétlődés átfedése: 0 MEK-oldali sor mindkettő; a nem létező célvers az elsőbbségű.

**A HunKar-oldali jelölt sor sorsa.** A #177 `eltero_lista` sora: a HunKar-sor, amelyet a MEK a versen nem listáz, de más hivatkozást igen. A javítókör (ELLENOR_F181 E1–E3) után a sorrend: (1) az E2-hibaminta megfelelője → `megerositett` (7); (2) a MEK a tartomány egyik végpontját adja → a tartomány `megerositett`, `forras=HunKar+MEK` (8), a MEK-végpontsor és az értelmezhetetlen társa `kiesik` (11 sor); (3) a MEK-pár nem létező célra mutat → `megerositett` (5); (4) a sor egy elírás-gyanús MEK-sor párja → jelölt marad; (5) egyébként `kiesik`, ha a verse MEK-listájából legalább egy sor beemelődik (3), különben jelölt marad. A `kiesik` itt **nem** állítja, hogy a HunKar-sor hibás: a MEK-lista elfogadásának következménye. HunKar-oldali jelölt sor: 44; ebből `megerositett`: 20, `kiesik`: 3, jelölt marad: 21.

## 3. Keresztábla és könyvenkénti eloszlás

**Altípus × döntés:**

| altípus | beemel (MEK-sor -> megerositett) | marad: MEK-oldali gyanús ismétlődő | marad: nem létező célvers | marad: elírás-gyanús (egyetlen összetevőben tér el a HunKar-céltól) | marad: MEK fejezet-hibaminta (a létező töredék) | HunKar-sor -> kiesik (a MEK-lista elfogadva a versen) | HunKar-sor marad jelölt (a MEK-sor nem emelődik be) | HunKar-sor -> megerositett (a MEK-pár célja nem létezik) | HunKar-sor -> megerositett (a MEK fejezet-hibamintájának megfelelője) | HunKar-tartomány -> megerositett (a MEK az egyik végpontot adja) | MEK-végpontsor -> kiesik (a megerősített HunKar-tartományba olvad) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| tartomány/vershatár | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 8 | 8 |
| könyv-elírás | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| fejezet-elírás | 0 | 0 | 6 | 3 | 5 | 0 | 2 | 2 | 7 | 0 | 0 |
| versszám-elírás | 0 | 0 | 3 | 5 | 0 | 0 | 9 | 3 | 0 | 0 | 0 |
| eltér (nem sorolható) | 15 | 0 | 5 | 0 | 3 | 2 | 9 | 0 | 0 | 0 | 3 |
| csak MEK | 2631 | 6 | 100 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| egyéb (egyező, de nem létező hivatkozás) | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

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

| könyv | jelölt | beemel | gyanús | nem létező | elírás-gyanús | E2-töredék | HunKar→megerősített | HunKar→kiesik | HunKar marad | MEK-végpont→kiesik |
|---|---|---|---|---|---|---|---|---|---|---|
| Gen | 16 | 15 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Exo | 23 | 20 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| Lev | 17 | 13 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |
| Num | 35 | 33 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Deu | 103 | 97 | 0 | 5 | 0 | 0 | 0 | 0 | 1 | 0 |
| Jos | 127 | 111 | 0 | 9 | 2 | 0 | 1 | 0 | 4 | 0 |
| Jdg | 7 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Rut | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1Sa | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2Sa | 111 | 105 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 2 |
| 1Ki | 93 | 88 | 2 | 2 | 0 | 1 | 0 | 0 | 0 | 0 |
| 2Ki | 62 | 59 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 |
| 1Ch | 84 | 76 | 1 | 4 | 0 | 0 | 1 | 0 | 0 | 2 |
| 2Ch | 90 | 84 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ezr | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Neh | 29 | 22 | 0 | 5 | 0 | 1 | 1 | 0 | 0 | 0 |
| Est | 14 | 13 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Job | 23 | 17 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| Psa | 198 | 163 | 0 | 27 | 0 | 4 | 4 | 0 | 0 | 0 |
| Pro | 56 | 53 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ecc | 6 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Isa | 69 | 54 | 0 | 11 | 1 | 1 | 1 | 0 | 1 | 0 |
| Jer | 121 | 115 | 0 | 5 | 0 | 0 | 0 | 0 | 1 | 0 |
| Ezk | 102 | 90 | 0 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |
| Dan | 42 | 41 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hos | 45 | 43 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Jol | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Amo | 23 | 21 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Mic | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Nam | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hag | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Zec | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Mal | 5 | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Mat | 82 | 77 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| Mrk | 29 | 26 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Luk | 106 | 105 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Jhn | 89 | 85 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| Act | 226 | 217 | 0 | 3 | 0 | 1 | 2 | 1 | 2 | 0 |
| Rom | 43 | 43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1Co | 158 | 157 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2Co | 98 | 95 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| Gal | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Eph | 11 | 7 | 0 | 2 | 0 | 0 | 1 | 1 | 0 | 0 |
| Php | 6 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 |
| Col | 14 | 2 | 0 | 1 | 0 | 0 | 4 | 1 | 2 | 4 |
| 1Th | 4 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 2 | 0 |
| 1Ti | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2Ti | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Tit | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Heb | 42 | 42 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Jas | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1Pe | 6 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 2 | 0 |
| 2Pe | 30 | 29 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1Jn | 41 | 37 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |
| 2Jn | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3Jn | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Jud | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Rev | 277 | 276 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

## 4. Mire kell figyelni a szabály alkalmazásakor

* **Elírás-gyanús osztály (orkesztrátori döntés):** 10 MEK-oldali sor áll olyan HunKar-sorral párban, amelytől egyetlen összetevőben (könyv/fejezet/versszám) tér el, és a MEK-cél létezik. A végrehajtói olvasat szerint ezek közül 4 valószínűen MEK-elírás (7. szakasz), ezért az egész osztály `jelolt` marad. Bontás: könyv-elírás 2, fejezet-elírás 3, versszám-elírás 5.
* **Tartomány-végpontok (E3, DT-F181i):** a HunKar a tartományt egy sorban adja, a MEK két végponttal. Ahol a MEK a tartomány egyik végpontját adja (a másik hiányzik vagy értelmezhetetlen), a HunKar-tartomány `megerositett` (8 sor, ebből 3 értelmezhetetlen, de a tartomány végének versszámával egyező MEK-véggel), a MEK-végpontsor és az értelmezhetetlen társa `kiesik` (11 sor): a lap/index a tartományt egyszer kapja, a tartomány vége nem vész el. A beemelt MEK-sorok közül még 1 a HunKar-tartomány szomszédja (nem végpontja), ezek nem olvadnak be.
* **Az E2-hibaminta (DT-F181h):** a MEK a HunKar `X a:b` célját két töredékre bontva adja (`X c:a`, `X c:b`); a létező töredék nem emelődik be (9 sor `jelolt`), a HunKar-megfelelő `megerositett` (7 sor); a teljes mérés: `python eszkozok/karoli_kh_mek.py e2-meres` (10. szakasz).
* **A fogyasztók** (`karoli_kh_szuro.mek_sorok()` a `lekerdez.py`, `sqlite_epit.py`, `olvaso_pilot/adat.py`, `nav_kinyer.py` oldalán) a csak a MEK-ben álló, megerősített sorokat is olvassák (N-F181e, lezárva: 9. szakasz).
## 5. A jelölt szint súlya

* A tábla sorai: 35204; ebből `jelolt`: **2863** (8.1%).
* Forrásversek a táblában: 19849; legalább egy `megerositett` sora van: 13120; legalább egy `jelolt` sora van: **1530**.
* **Jelölt nélkül nem marad megerősített KH-ja: 51 vers** (a jelölt versek 3.3%-a); ezek közül 0 versnek van `kiesik` sora is, 51 versnek csak jelölt sora van.
* A szabály 1405 forrásversen emel be sort; ebből 7 versnek ezzel lesz először megerősített KH-ja (a `megerositett` szint 13120 forrásversét 0.1%-kal bővíti).

## 6. Példák (kategóriánként legfeljebb 8, egyenletes minta a tábla sorrendjéből)

Jelölés: `forrásvers → cél`; partner: a másik oldal párosított sora; TSK: a saját cél (mai szabály / tiszta; csak tájékoztatás); L: a cél létezik; gy: gyanús (H: HunKar-oldali, M: MEK-oldali).

### beemel (MEK-sor -> megerositett) (2647 sor)

* Gen.21.2 → Gen.18.10 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 2Sa.6.12 → 2Sa.6.14 | MEK | altípus: csak MEK | TSK nem/nem | L: igen
* 2Ch.7.11 → 1Ch.28.20 | MEK | altípus: csak MEK | TSK igen/nem | L: igen
* Ecc.1.17 → Ecc.2.1 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Hos.10.8 → Hos.9.6 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Jhn.12.35 → 1Jn.2.10 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 1Co.4.12 → 1Th.2.9 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* 2Pe.3.17 → 2Pe.3.9 | MEK | altípus: csak MEK | TSK nem/nem | L: igen

### marad: MEK-oldali gyanús ismétlődő (6 sor)

* Gen.48.4 → Gen.28.13 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ki.2.5 → 2Sa.20.10 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ki.2.32 → 2Sa.20.10 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* 1Ch.6.8 → 1Ch.27.17 | MEK | altípus: csak MEK | TSK nem/nem | L: igen | gy: M
* Mat.21.13 → Jer.7.11 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M
* Mrk.11.17 → Jer.7.11 | MEK | altípus: csak MEK | TSK igen/igen | L: igen | gy: M

### marad: nem létező célvers (136 sor)

* Exo.6.3 → Gen.16.17 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Jos.24.7 → Exo.15.19-Exo.15.29 | egyező | altípus: egyéb (egyező, de nem létező hivatkozás) | TSK nem/nem | L: nem
* Neh.8.9 → Neh.10.65 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Psa.104.26 → Job.25.13 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Isa.45.1 → 2Ch.22.23 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Ezk.36.22 → Isa.33.25 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* 1Th.1.5 → 1Co.2.20 | MEK | altípus: csak MEK | TSK nem/nem | L: nem
* Psa.106.40 → Psa.78.79 | MEK | altípus: csak MEK | TSK nem/nem | L: nem

### marad: elírás-gyanús (egyetlen összetevőben tér el a HunKar-céltól) (10 sor)

* Jos.2.15 → Act.9.25 | partner: Act.9.2 | MEK | altípus: versszám-elírás | TSK igen/igen | L: igen
* Jos.2.15 → 2Co.11.25 | partner: Act.11.25 | MEK | altípus: könyv-elírás | TSK nem/nem | L: igen
* Isa.5.30 → Amo.8.1 | partner: Amo.8.10 | MEK | altípus: versszám-elírás | TSK nem/nem | L: igen
* Php.3.4 → 2Co.11.21 | partner: Rom.11.21 | MEK | altípus: könyv-elírás | TSK igen/igen | L: igen
* 1Pe.2.20 → Luk.12.47 | partner: Luk.12.47-Luk.12.15 | MEK | altípus: versszám-elírás | TSK nem/nem | L: igen
* 1Pe.2.20 → Luk.15.14 | partner: Luk.3.14-Luk.3.17 | MEK | altípus: fejezet-elírás | TSK nem/nem | L: igen
* 1Pe.2.20 → Luk.15.17 | partner: Luk.3.14-Luk.3.17 | MEK | altípus: fejezet-elírás | TSK nem/nem | L: igen
* 1Jn.2.27 → Jhn.14.26 | partner: Jhn.14.26-Jhn.14.16 | MEK | altípus: versszám-elírás | TSK igen/igen | L: igen

### marad: MEK fejezet-hibaminta (a létező töredék) (9 sor)

* 1Ki.2.26 → 1Sa.22.20 | MEK | altípus: csak MEK | TSK igen/igen | L: igen
* Neh.1.5 → Neh.4.9 | MEK | altípus: eltér (nem sorolható) | TSK igen/nem | L: igen
* Psa.27.4 → Psa.23.2 | partner: Psa.42.2-Psa.42.3 | MEK | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Psa.27.4 → Psa.23.3 | partner: Psa.42.2-Psa.42.3 | MEK | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Psa.34.18 → Psa.9.10 | partner: Psa.32.10 | MEK | altípus: fejezet-elírás | TSK nem/nem | L: igen
* Psa.35.12 → Psa.38.10 | partner: Psa.41.10 | MEK | altípus: fejezet-elírás | TSK nem/nem | L: igen
* Isa.53.7 → Psa.38.10 | partner: Psa.39.10 | MEK | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Jhn.8.12 → Jhn.9.12 | MEK | altípus: eltér (nem sorolható) | TSK nem/nem | L: igen

### HunKar-sor -> kiesik (a MEK-lista elfogadva a versen) (3 sor)

* Act.5.40 → Mrk.13.2 | HunKar | altípus: eltér (nem sorolható) | TSK nem/nem | L: igen
* Eph.3.1 → Gal.6.2 | HunKar | altípus: eltér (nem sorolható) | TSK nem/nem | L: igen
* Col.4.17 → Phm.1.1 | partner: Phm.1.2 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen

### HunKar-sor marad jelölt (a MEK-sor nem emelődik be) (21 sor)

* Deu.28.38 → Hag.1.6 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Jos.2.15 → Act.9.5-Act.9.2 | partner: Act.9.25 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen
* Isa.5.30 → Amo.8.10 | partner: Amo.8.1 | HunKar | altípus: versszám-elírás | TSK igen/igen | L: igen
* Jhn.5.8 → Mrk.2.11 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Php.1.3 → Phm.1.4 | HunKar | altípus: eltér (nem sorolható) | TSK igen/igen | L: igen
* Col.1.9 → Col.2.18-Col.2.23 | HunKar | altípus: eltér (nem sorolható) | TSK nem/nem | L: igen
* 1Th.3.9 → 1Th.2.19-1Th.2.3 | partner: 1Th.2.19 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen
* 1Pe.2.20 → Luk.3.14-Luk.3.17 | partner: Luk.15.14 | HunKar | altípus: fejezet-elírás | TSK nem/nem | L: igen

### HunKar-sor -> megerositett (a MEK-pár célja nem létezik) (5 sor)

* Lev.23.17 → Lev.2.12 | partner: Lev.2.17 | HunKar | altípus: versszám-elírás | TSK igen/igen | L: igen
* Jos.22.3 → Jos.11.18 | partner: Jos.11.28 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen
* Psa.143.3 → 1Sa.23.7-1Sa.23.8 | partner: 1Sa.23.78 | HunKar | altípus: versszám-elírás | TSK nem/nem | L: igen
* Act.21.8 → Act.8.26-Act.8.40 | partner: Act.12.26 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Eph.2.20 → Isa.28.16 | partner: Isa.18.16 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen

### HunKar-sor -> megerositett (a MEK fejezet-hibamintájának megfelelője) (7 sor)

* Neh.1.5 → Neh.9.32 | partner: Neh.4.32 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Psa.27.4 → Psa.42.2-Psa.42.3 | partner: Psa.23.2 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Psa.34.18 → Psa.32.10 | partner: Psa.9.10 | HunKar | altípus: fejezet-elírás | TSK nem/nem | L: igen
* Psa.35.12 → Psa.41.10 | partner: Psa.38.10 | HunKar | altípus: fejezet-elírás | TSK nem/nem | L: igen
* Isa.53.7 → Psa.39.10 | partner: Psa.38.10 | HunKar | altípus: fejezet-elírás | TSK nem/nem | L: igen
* Jhn.8.12 → Jhn.12.46 | partner: Jhn.9.46 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen
* Act.14.22 → Act.13.43 | partner: Act.11.43 | HunKar | altípus: fejezet-elírás | TSK igen/igen | L: igen

### HunKar-tartomány -> megerositett (a MEK az egyik végpontot adja) (8 sor)

* 2Sa.7.8 → 1Sa.16.11-1Sa.16.12 | partner: 1Sa.16.11 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 2Ki.21.5 → 2Ki.23.11-2Ki.23.12 | partner: 2Ki.23.11 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 1Ch.6.14 → 2Ki.25.18-2Ki.25.21 | partner: 2Ki.25.18 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 2Co.7.4 → Phm.1.1-Phm.1.8 | partner: Phm.1.8 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* Col.1.7 → Phm.1.1-Phm.1.23 | partner: Phm.1.23 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* Col.4.9 → Phm.1.1-Phm.1.10 | partner: Phm.1.10 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* Col.4.14 → Phm.1.1-Phm.1.24 | partner: Phm.1.24 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* Col.4.15 → Phm.1.1-Phm.1.2 | partner: Phm.1.2 | HunKar | altípus: tartomány/vershatár | TSK igen/igen | L: igen

### MEK-végpontsor -> kiesik (a megerősített HunKar-tartományba olvad) (11 sor)

* 2Sa.7.8 → 1Sa.16.11 | partner: 1Sa.16.11-1Sa.16.12 | MEK | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 2Sa.7.8 →  | MEK | altípus: eltér (nem sorolható) | TSK igen/nem | L: nem
* 2Ki.21.5 → 2Ki.23.11 | partner: 2Ki.23.11-2Ki.23.12 | MEK | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 1Ch.6.14 → 2Ki.25.18 | partner: 2Ki.25.18-2Ki.25.21 | MEK | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* 1Ch.6.14 →  | MEK | altípus: eltér (nem sorolható) | TSK igen/nem | L: nem
* 2Co.7.4 → Phm.1.8 | partner: Phm.1.1-Phm.1.8 | MEK | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* Col.4.9 → Phm.1.10 | partner: Phm.1.1-Phm.1.10 | MEK | altípus: tartomány/vershatár | TSK igen/igen | L: igen
* Col.4.14 → Phm.1.24 | partner: Phm.1.1-Phm.1.24 | MEK | altípus: tartomány/vershatár | TSK igen/igen | L: igen

## 7. A maradék szúrópróbája és a kontroll (J3) — az első kör, történeti

> **Javítókör 1 (ELLENOR_F181 E5, DT-F181j):** ez a szakasz az első kör mintája és a végrehajtó olvasata (az E1/E2/E3 előtti szabályra; a számai — 190 jelölt, 15 elírás-gyanús, 30 HunKar-oldali sor — nem frissültek, mert a mintát újra kell venni). Az ellenőr szerint a tételek nincsenek dokumentálva, és az értelmező ítéletet Opus hozza. Az E1/E2/E3 utáni új minta tételei, üres ítélet-oszloppal: `naplok/F181_szuroproba.md` (136 tétel, mag=181). Az alábbi hibaarányok **nem** az új mintára vonatkoznak.

*scope=konkordancia/Karoli_KH_javitott.tsv (a J4 utáni állapot) + konkordancia/Karoli_1908.tsv | forras=eszkozok/karoli_kh_mek.py szuroproba (mag=181) + a végrehajtó olvasata | ts=2026-11-09*

**Módszer.** A minta könyvenként arányos (legnagyobb maradék módszere), rögzített maggal ismételhető (az F181.5 commit állapotán: `git checkout c29b0f65`, majd `python eszkozok/karoli_kh_mek.py szuroproba`; a végleges szabálynál a rétegek mérete más). Rétegek: (1) az első szabályváltozat szerint gyanús ismétlődésként jelöltben maradt 86 MEK-oldali sorból 30 (ebből 80 HunKar-oldali jelölésű, ezek a végleges szabály szerint beemelődnek: a minta róluk szól); (2) a HunKar-oldali, jelöltben maradt 14 sor mind (a végleges szabály szerint 30: a többi az elírás-gyanús sorok HunKar-oldali párja, ezeket a célzott rétegben olvastam); (3) **kontroll**: a szabály első változata által beemelt 2 594 sorból 40 (a szabály hibaarányának mérésére); ebből 1 sor (a 58.) az elírás-gyanús osztályba esik, amely a végleges szabály szerint nem emelődik be, ezért a kontrollban 39 sor érvényes. A 139 nem létező célvers sort nem mintázom: tételesen az A. függelék. Az ítélet a két vers (Károli) szövegének olvasata: **rendben** = a cél a forrásvers idézete, párhuzama vagy szoros témai kapcsolata; **gyenge** = laza, de védhető kapcsolat; **hiba** = nincs felismerhető kapcsolat. **Korlát:** az ítélet a végrehajtó (nem független) olvasata, a `fuggetlen-ellenor` nem helyettesíti; olyan elírást, amely véletlenül értelmes helyre mutat, nem fog meg. A hibaarány ezért alsó becslés.

| réteg | n | rendben | gyenge | hiba | hibaarány | 95% Wilson-felső |
|---|---|---|---|---|---|---|
| maradék: gyanús ismétlődő | 30 | 25 | 5 | 0 | 0.0% | 11.4% |
| maradék: HunKar-sor jelölt marad (mind) | 14 | 9 | 4 | 1 | 7.1% | 31.5% |
| kontroll: beemelt MEK-sor | 39 | 35 | 4 | 0 | 0.0% | 9.0% |

**Mit mutat.** (1) A gyanús ismétlődésként elsőre kizárt 86 MEK-oldali sor 30-as mintájában **egyetlen hiba sincs** (25 rendben, 5 gyenge). A 86 sorból 80 a **HunKar-oldali** gyanús-jelölés miatt esett volna ki (a #177 gyanús halmaza a HunKar-lista másoltságát jelzi, a MEK-lista ilyenkor a javító tanú), 6 a MEK-oldali ismétlődés miatt. A felhasználó döntése (DT-F181f, „beemeljük”): a 80 HunKar-oldali gyanús-jelölésű, a MEK-ben ismétlődés nélkül álló sor `megerositett` lesz; a 6 MEK-oldali ismétlődés miatti sor `jelolt` marad. A mintában 3 sor MEK-oldali ismétlődés is volt (Gen.48.4, 1Ki.2.32, Mrk.11.17): ezek is rendben voltak, de a döntés szerint jelöltben maradnak. (2) A jelöltben maradt HunKar-oldali sorok első változatból vett 14-es mintájában 9 rendben, 4 gyenge, 1 hiba: a HunKar-sor itt többnyire helyes, a MEK-párja nem létező vers (MEK-elírás), tehát a „jelölt marad” helyes választás. (3) A beemelés kontrollmintájában 39-ből 0 hiba (35 rendben, 4 gyenge), a Wilson-felső korlát 9,0%.

**Célzott réteg: az elírás-gyanús osztály (15 sor, DT-F181e).** Ahol a MEK-sor egyetlen összetevőben tér el a forrásvers HunKar-sorától (l. 4. szakasz), külön, tételesen olvastam mind a 15-öt (a 7. szakasz sorszámai az `elo.tsv` szerinti sorrend; a pár: forrásvers / MEK-cél / HunKar-pár):

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

Összesítve: a MEK **helyes/elfogadható 7**, **hibás 4** (Zsolt 27:4 → Zsolt 23:2 és 23:3, Ézs 5:30 → Ám 8:1, Ézs 53:7 → Zsolt 38:10), **bizonytalan 4**. A 4 hibás sor mind létező célverset hordoz (a versellenőrzés nem fogja meg). **Döntés (DT-F181e, orkesztrátori, nem felhasználói):** a 4 valószínű MEK-elírás miatt az egész osztály (MEK-oldali sor, amely egyetlen összetevőben tér el a forrásvers egy jelölt HunKar-sorának céljától, és létezik) `jelolt` marad, nem emelődik be. A szabály a `karoli_kh_mek.py`-ban (`D_ELIRAS`) és a README 7. szakaszában áll.

## A. függelék — a nem létező célvers miatt jelöltben maradó sorok (tételesen, 136)

Forrásvers → cél; „egyező”: a HunKar és a MEK ugyanazt a nem létező célt hordozza (a hibás tartomány-végpont). Mérés: `Karoli_1908` ∪ MEK-versszerkezet. A javítókör 1 (E3) után az értelmezhetetlen MEK-végű három sor (2Sám 7:8, 2Kir 21:5, 1Krón 6:14) a megerősített HunKar-tartományba olvad (`kiesik`), ezért nem szerepel itt (139 → 136).

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
* 2Sa.23.3 → Deu.30.21
* 1Ki.2.26 → 1Sa.22.33
* 1Ki.5.12 → 1Ki.4.29-1Ki.4.39 (egyező)
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

## 8. A J4 Δ-naplója (a tábla frissítése, a végleges szabállyal)

*scope=konkordancia/Karoli_KH_javitott.tsv | forras=eszkozok/karoli_kh_mek.py beemel (az F181.1 nyers táblán: `osszevet --nyers`) | ts=2026-11-09*

```
sorok: 35204 -> 35204
megerositett: 21314 -> 23981 (Δ +2667)
kiesik: 11027 -> 11041 (Δ +14)
jelolt: 2863 -> 182 (Δ -2681)
átment jelolt -> kiesik: 14
átment jelolt -> megerositett: 2667
```

A `beemel` a nyers táblán és az `osszevet` (a beemeléssel) ugyanazt a végleges táblát adja (bájtra azonos); a `beemel` a kész táblán idempotens (a sorok és a bájtok változatlanok). Az első kör Δ-ja: megerositett +2 659, kiesik +14, jelolt −2 673 (190 maradék).

**Menet közbeni döntések és hatásuk.** Az első szabályváltozat (DT-F181d, a felhasználó szava) 2 594 sort emelt be (jelölt 239). Ezt módosította: **DT-F181e** (orkesztrátori döntés, nem felhasználói: az elírás-gyanús osztály `jelolt` marad), **DT-F181f** (a felhasználó: „beemeljük”: a 80 HunKar-oldali gyanús-jelölésű, ismétlődés nélküli MEK-sor `megerositett`; a MEK-oldali ismétlődés miatti 6 sor `jelolt`), majd a javítókör 1 döntései (**DT-F181g**: a nem létező célú MEK-pár nem ítéli el a HunKar-sort; **DT-F181h**: az E2-hibaminta; **DT-F181i**: a tartomány vége nem vész el).

A végleges maradék **182** `jelolt` sor, mindegyik a saját indokában hordozza az okát (`marad=<kód>`): 136 nem létező célvers (114 MEK-oldali + 22 egyező), 6 MEK-oldali gyanús ismétlődő, 10 elírás-gyanús MEK-sor, 9 E2-hibaminta-töredék, 21 HunKar-oldali sor (10 elírás-gyanús vagy E2-sor párja, 11 olyan, amelynek a verse MEK-listájából egyik sor sem emelődik be). Az 1–6. szakasz soronkénti döntései a végleges szabályé.

## 9. Egyeztetett eltérés a briefhez képest (N-F181e: a fogyasztók)

A brief `ir` listáján a szűrő és a fogyasztói nem szerepeltek; a koordinátor és a felhasználó („javítani”, 2026-11-09) a hatókört bővítette, hogy a `Karoli_KH_javitott.tsv` csak a MEK-ben álló, `megerositett` sorait a fogyasztók is lássák. Módosított fájlok (kód; a bővített `ir` mező a brief fejlécében):
* `eszkozok/karoli_kh_szuro.py`: új `mek_sorok(forras=None)` (a csak-MEK `megerositett` sorok a HunKar-tábla kulcsaival és magyar megjelenítéssel); az `elfogad` a javított tábla minden `megerositett` sorát elfogadja (ez eddig is így volt kulcsra, most van olyan sor, amelyet a fogyasztók a HunKar-táblából nem kaptak volna meg).
* `eszkozok/lekerdez.py` (`karoli`), `eszkozok/sqlite_epit.py` (`kh` tábla építése), `eszkozok/olvaso_pilot/adat.py`, `eszkozok/olvaso_mockup/nav_kinyer.py`: a HunKar-sorok mellé a `mek_sorok()`-t is olvassák, ugyanazzal az `elfogad` szűrővel.
* `eszkozok/teszt_karoli_kh_mek.py`: `test_szuro_csak_mek_megerositett_sor` (a szűrő elfogadja a csak-MEK sort; a `kiesik` és a `jelolt` nem jut át).
Nem történt: lexikonlap-újragenerálás; a `pardes.db` (a `sqlite_epit.py` csak kódja módosult, az adatbázis nem épült újra). A `lexikon_general.py` `kh_index` és az `olvasoi_kapu.py` `KH_MASOLT` szabálya (N-F177a) változatlan. **N-F181e lezárva** ebben a PR-ban (kód + teszt); a lapok újragenerálása a motívumonkénti teljes folyamatban (N-F177a).

## 10. Javítókör 1 (ELLENOR_F181: 8 ELTÉRÉS-tétel)

*Végrehajtó: `claude-sonnet-5-5`. Az orkesztrátor döntései: DT-F181g–k (`dontesek/uj/f181-karoli-kh-jeloltek.md`). Commitok: F181.11–F181.20. Az ágon nem történt push, merge és lapgenerálás.*

**Állapot a javítókör után.** `megerositett` 23 981 (volt 23 973), `kiesik` 11 041 (11 041), `jelolt` 182 (190); összesen 35 204. Az F181.10 tábla ↔ a végleges: **213 sor változott, a többi 34 991 bájtra azonos**. Ebből 35 sor szintje/forrása változott a szabályváltozás miatt (9 `jelolt` → `megerositett` HunKar-sor; 3 `kiesik` → `megerositett` HunKar-sor; 8 `kiesik` → `megerositett` HunKar+MEK tartománysor; 4 `megerositett` → `jelolt` MEK-töredék; 8 `megerositett` és 3 `jelolt` → `kiesik` MEK-végpontsor), 178 soré változatlan szinttel és forrással csak az indok-/proveniencia-oszlopot bővítette a `marad=` tag (E8; az `igehely`, `kapcsolodo`, `szint`, `forras` oszlop azonos). Az átmeneti táblák az előző állapothoz képest: E1 8 sor (F181.12), E2 11 sor (F181.13), E3 19 sor (F181.14), E8 182 sor (F181.17); minden más sor bájtra azonos.

**E1 — a nem létező célú MEK-pár nem ítéli el a helyes HunKar-sort (DT-F181g; F181.12).** A szabály: ha a HunKar-sor célverse létezik, és a MEK-oldali párja (egyetlen összetevőben eltérő MEK-sor) kizárólag nem létező célra mutat, a HunKar-sor `megerositett` (`forras=HunKar`, `mek_par_nem_letezik=…`), a versen beemelődő más sortól függetlenül. A három megnevezett eset (Neh 1:5 → 9:32, Ján 8:12 → 12:46, ApCsel 14:22 → 13:43) az E1-gyel önmagában is `megerositett` lett (F181.12), a végleges szabály szerint az E2-megfelelő (az E2 az első a sorrendben). A **Lev 23:17 → Lev 2:12 ugyanilyen helyzet** (a MEK-párja `2,17`, nem létező), ezért ugyanúgy `megerositett`; a szabály még 4 HunKar-sort érint, amelyek eddig `jelolt` voltak: Józs 22:3 → 11:18 (MEK `11,28`), Zsolt 143:3 → 1Sám 23:7–8 (MEK `23,78`), ApCsel 21:8 → 8:26–40 (MEK `12,26`, `12,40`), Ef 2:20 → Ézs 28:16 (MEK `18,16`). **Összesen 5 sor kapja az E1 megjegyzést** (a Lev 23:17-tel), ez a 3 megnevezett eseten túli kiterjesztés; a döntés a Lev 23:17-re adott „ugyanúgy kezeld” általánosítása. Tesztek: `test_e1_*`, `test_e1_esetek_a_tablan`.

**E2 — a MEK fejezet-hibamintája (DT-F181h; F181.13).** Gépi felismerés: `karoli_kh_mek.e2_mintak`; teljes mérés: `python eszkozok/karoli_kh_mek.py e2-meres` (a nyers táblán):

```
E2-hibaminta (DT-F181h), teljes mérés a nyers táblán
minta (két-három egymás utáni MEK-sor): 26; forrásvers: 24
HunKar-megfelelővel bíró minta: 7 (forrásvers: 7); HunKar-megfelelő nélküli: 19
létező MEK-töredék a mintákban: 21
  ebből a táblában csak_mek sor (a szűrő érinti): 9; HunKar-sorral egyezik (a szűrő nem érinti): 12
  a csak_mek töredékek közül a minta nélkül beemelődött volna: 4; elírás-gyanús osztályban lett volna: 5; gyanús ismétlődőként jelolt lett volna: 0
  a csak_mek töredékek közül HunKar-megfelelő nélküli mintában áll: 1
a minta nélkül beemelődött töredékek: 1Ki.2.26 → 1Sa.22.20; Act.14.22 → Act.11.13; Jhn.8.12 → Jhn.9.12; Neh.1.5 → Neh.4.9
a HunKar-megfelelő nélküli mintában álló csak_mek töredékek: 1Ki.2.26 → 1Sa.22.20
```

Tehát **26 minta (24 forrásvers)**, ebből **7-nek van HunKar-megfelelője** (Neh 1:5, Zsolt 27:4, 34:18, 35:12, Ézs 53:7, Ján 8:12, ApCsel 14:22); a minták **21 létező töredéket** tartalmaznak, ebből **9 áll a táblában `csak_mek` sorként** (ezeket érinti a szűrő), 12 egy HunKar-sorral egyezik (nem érinti). A 9 töredékből 4 `megerositett` lett volna (Neh 4:9, Ján 9:12, ApCsel 11:13, 1Sám 22:20), 5 az elírás-gyanús osztályban volt (Zsolt 23:2, 23:3, 9:10, 38:10 ×2). **A DT-F181e két esetét is elkapja a szűrő:** Zsolt 35:12 (HunKar 41:10, MEK 38,41 + 38,10) és Ézs 53:7 (HunKar 39:10, MEK 38,39 + 38,10) — és a Zsolt 27:4-et (23,42 + 23,2 + 23,3 → 42:2–3) és a Zsolt 34:18-at (9,32 + 9,10 → 32:10) is. Az Ézs 5:30 → Ám 8:1 (versszám-eltérés) nem E2-minta, az elírás-gyanús osztályban marad. Hatás: 4 MEK-sor `megerositett` → `jelolt`; 7 HunKar-sor `megerositett` (3 volt `kiesik`: Neh 1:5, Ján 8:12, ApCsel 14:22; 4 volt `jelolt`); az elírás-gyanús osztály 15 → 10. **Nyitott kérdés (N-F181f, az orkesztrátor döntésére vár):** a HunKar-megfelelő nélküli mintákból a szűrő a 9 töredékből **1-et** érint: 1Kir 2:26 → 1Sám 22:20 (MEK `22,20` + nem létező `22,33`); a Károli-szöveg szerint („Akhitób fiának, Akhiméleknek egy fia azonban, a kit Abjáthárnak hívtak, elmenekült, és Dávid után futott”) a töredék tartalmilag helyesnek látszik, a DT-F181h szövege szerint mégis `jelolt`. Opció: (a) marad `jelolt` (mai állapot); (b) a szűrő csak a HunKar-megfelelővel bíró mintára vonatkozik (+1 `megerositett`, jelolt 181). Tesztek: `test_e2_*`.

**E3 — a tartomány vége nem vész el (DT-F181i; F181.14).** A HunKar-tartomány egyik végpontját adó MEK-sor mellett a tartomány `megerositett` (`forras=HunKar+MEK`); a MEK-végpontsor és az értelmezhetetlen társa `kiesik` (`tartomany_vegpont=`), így nincs duplikáció, és a tábla többi tartománykezelésével összhangban a tartományt a lap egyszer kapja. **Esetek (mért): 8 HunKar-tartomány**: a három megnevezett (2Sám 7:8 → 1Sám 16:11–12; 2Kir 21:5 → 2Kir 23:11–12; 1Krón 6:14 → 2Kir 25:18–21; a MEK második végpontja `12,.`, `12,.`, `21,.`, és a megmaradt szám mindhárom esetben a tartomány végének versszáma: `mek_vege_elirt`), valamint **5 további Filemon-tartomány**, ahol a MEK csak a tartomány végpontját adja (Kol 1:7 → Filem 1:1–23; Kol 4:9 → 1:1–10; Kol 4:14 → 1:1–24; Kol 4:15 → 1:1–2; 2Kor 7:4 → 1:1–8). Összesen **11 MEK-sor** olvad a tartományba (8 végpontsor + 3 értelmezhetetlen). **Nem érint:** 3 fordított HunKar-tartomány (1Thessz 2:19–3, Luk 12:47–15, Ján 14:26–16, a vég kisebb a kezdetnél), ezek az elírás-gyanús osztályban maradnak (DT-F181e); a Zsolt 143:3 (`1 Sám. 23,78`: a „7–8” összeolvadt alakja) az E1 alá esik; a Kol 4:17 (HunKar Filem 1:1, MEK Filem 1:2) nem tartomány-végpont, `kiesik` marad. Tesztek: `test_e3_*`.

**E4 — N-F177b (F181.18).** Lezárva a tényleges, újraszámolt állapottal (`NYITOTT_FELADATOK.md` 851. sor): megerositett +2 667, kiesik +14, jelolt 182; a 182 sor mindegyike szabály szerinti okkal jelölt marad, az ok a sorban. Ami ténylegesen nyitva marad, az külön tétel: N-F181f (az E2-minta egy esete) és a szúrópróba Opus-ítélete (DT-F181j).

**E5 — a szúrópróba (DT-F181j; F181.19).** `naplok/F181_szuroproba.md`: 136 tétel táblázatban (forrásvers, cél, MEK-alak, réteg, a két vers Károli-szövege, **üres** ítélet és indok oszlop). Rétegek: kontroll (beemelt MEK-sor, 2 647-ből 40), HunKar-gyanús forrásversen beemelt MEK-sor (80-ból 30), MEK-oldali gyanús ismétlődő (6, mind), elírás-gyanús (10, mind), HunKar-oldali jelölt marad (21, mind), E2-szűrt töredék (9, mind), az E1/E2/E3 által megerősített HunKar-sor (20, mind). Reprodukálható: `python eszkozok/karoli_kh_mek.py szuroproba --be konkordancia/Karoli_KH_javitott.tsv --md naplok/F181_szuroproba.md --mag 181 --kontroll 40 --hunkar-gyanus 30 --hossz 150 --ts 2026-11-09` (a tábla állapota: `6af8b0cf`). **Ítéletet nem adtam**; az értelmező ítéletet Opus hozza, külön lépésben.

**E6 — vegyes könyvnevek (F181.15).** `karoli_kh_szuro.hu_megjelenites`: a HunKar-tábla szentiras.hu-alakú könyvnevét a repó egységes alakjára (`ApCsel`) cseréli; a `lekerdez.py karoli`, az `olvaso_pilot/adat.py` és az `olvaso_mockup/nav_kinyer.py` ezt használja. Mért keveredés: a 32 407 HunKar-sorból **8 680** megjelenítése változik, **17 eltérő alak, 15 könyv**: `Csel`→`ApCsel` (1 116), `Ésa`→`Ézs` (2 110), `Mát`/`Máté`→`Mt` (1 835 + 294), `Márk`→`Mk` (924), `Ezék`→`Ez` (902), `Eféz`→`Ef` (475), `1Thess`→`1Thessz` (217), `2Thess`→`2Thessz` (89), `Ezsdr`→`Ezsd` (163), `Bir`→`Bír` (159), `Siral`/`Sir`→`JSir` (124 + 30), `Nehem`→`Neh` (101), `Malak`→`Mal` (84), `Agge`→`Hag` (31), `Énekek`→`Én` (26). Többkönyves tartomány-megjelenítés nincs. Az elavult docstring javítva. A `lexikon_general.py` (lapgenerálás, N-F177a) érintetlen.

**E7 — proveniencia és licenc (F181.16).** `olvaso_pilot/adat.py`: a `kh` proveniencia `forras=` mezője megnevezi a HunKar-táblát, a `Karoli_KH_MEK.tsv`-t (MEK 00161, közkincs) és a szűrőként használt `Karoli_KH_javitott.tsv`-t. `sqlite_epit.py`: `'kh': ['Karoli_KH', 'Karoli_KH_MEK']`. Az `adat/datasetek.tsv`-ben létezik a MEK-dataset azonosítója (`Karoli_KH_MEK`, és a szűrőé: `Karoli_KH_javitott`), az `adat/licencek.tsv`-ben mindkettőnek sora van; új azonosítót nem találtam ki. A `Karoli_KH_javitott` (a szűrő, a saját rész `minden jog fenntartva`) szándékosan **nem** került a licenc-térképbe: a `kh` tábla csak a megerősített sorok STEP-hivatkozásait hordozza, a szintet és az indokot nem; ha a térképbe kellene, a származtatott licenc `minden jog fenntartva` lenne (DT-F79a (2c): a legszigorúbb érték) — ez licencdöntés, nem hoztam meg. **`teszt_sqlite_epit.py`:** a teljes futás (79 teszt) 1 hibát ad, `test_baseline_a_masolaton_zold`: a 13. szabály (fordítási gyorsítótár, `UBS_DBH`, 443 tétel; ismert, nem e feladathoz tartozik; local_7dc8df8f-3d34-452d-845b-fec09f2b2761 dolgozik rajta) és — a feladatleírás ezt nem említette — a **4. szabály (horgony-kényszer) 1 sérülése: `KIRALY-001 / 1Móz 14:18-20`**. Az utóbbi a lexikon-horgonyokról szól, a `kh` táblához nincs köze; hogy az alapállapotban is megvolt-e, nem mértem (nem futtattam a tesztet az F181.10 állapoton). Az én változtatásom (a licenc-térkép és a proveniencia-szöveg) új bukást nem okozott: minden `kh`-teszt zöld.

**E8 — a jelölt sor oka a sorban (DT-F181k; F181.17).** `…;marad=<kód>`, új oszlop nélkül, a README 7. szakasz 5. pontja felsorolja: `nem_letezo_cel` 136, `gyanus_ismetlodo` 6, `eliras_gyanus` 10, `mek_fejezet_minta` 9, `eliras_gyanus_par` 10 (HunKar-sor), `mek_lista_nincs_elfogadva` 11 (HunKar-sor); összesen 182. Teszt: minden `jelolt` sor pontosan egy kódot hordoz, a kód a sor tartalmával egyezik, és a README felsorolja.

**Tesztek.** `python eszkozok/teszt_karoli_kh_mek.py`: **58 teszt, mind OK** (a javítókör előtt 39). `python eszkozok/teszt_sqlite_epit.py`: 79 teszt, 1 bukás (l. E7: UBS_DBH 13. szabály + a horgony-kényszer 1 sérülése, nem a `kh`-hoz tartozó).

**Nyitott.** N-F181f (az E2-minta egy HunKar-megfelelő nélküli esete: 1Kir 2:26 → 1Sám 22:20); a szúrópróba Opus-ítélete (DT-F181j); az E1 kiterjesztése a 3 megnevezett eseten túli 4 sorra (Józs 22:3, Zsolt 143:3, ApCsel 21:8, Ef 2:20) az orkesztrátor jóváhagyására vár.
