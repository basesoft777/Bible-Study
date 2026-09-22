# LEXV2_2_BRIEF.md — v1

Lexikon-oldal v2, 2. menet: generátor és sablon. Az új oldalszerkezet, az `LXX_OS` bekötése, a Thayer- és az UBS-szótár kirakása. Két végrehajtási kör, ⛔ emberi megállással: **1. kör** (V2.0–V2.6) csak a `generalt_proba/lexikon/` alá termel; **2. kör** (V2.7–V2.9) élesít.

## 0. Kiindulás — mérve, `9c0f2f0` (2026.09.22)

- 8 lexikon-oldal (`lexikon/*_TUDOMANYOS.md`). Valódi kézi tartalom **csak az ISTENTISZT-001-en** van (1/b, 2/b „Teljes szótári anyag — a pilotból", Miért fontos, Minősítés, Alátámasztás, 6. Módszertani napló); a többi 7 oldal kézi szakaszai helyőrzők („*Kézzel írandó.*").
- Az `elofordulasok.tsv` 256 sor; 13 különböző G-token: G0012, G0086, G0282, G0813, G1311, G1941, G1944, G2671, G4151, G5010, G5351, G5356, G5590.
- A `lexikon_hivatkozasok.tsv` 5 sor (3 BDB, 2 TBESG); Thayer-sor nincs, bár a `konkordancia/Thayer_teljes.tsv` (5 426 szócikk, közkincs) a repóban van, és a generátor `LICENC['Thayer']` kulcsa ismeri.
- Az `LXX_OS` (LEXV2_1, V1.3a) kész; a generátor még a régi `LXX_kivonat_*.tsv`-t olvassa (`tisztazatlan`).
- Az `LXX_OS` `karoli_ok` oszlopa üres a `KEZI_ELTOLASOK`-ból jövő soroknál (V1.3-ban még `kezi_eltolas_tabla` volt).
- Héber→görög megfelelő-lista gépi formában nincs: a `openscriptures/HebrewLexicon` @ `21c9add` `HebrewStrong.xml`-ben 0/8674 szócikk tartalmaz görög Strong-számot; a TBESG csak folyó szövegben említ LXX-megfelelőt. Ezért a nem egyező LXX-helyek görög megfelelője kutatói adat (G5).
- A `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` v2 licenc-szakasza elavult (a Thayert tisztázatlannak írja).

## 1. A feladat

(a) az `LXX_OS` `karoli_ok` pótlása; (b) sablon v3 = lexikon-oldal v2 szerkezet; (c) új adattáblák: UBS-fordítás, LXX-fordítói döntések; (d) Thayer-sorok a 13 görög tokenhez; (e) generátor: új váz és blokkok; (f) próba a `generalt_proba/lexikon/` alá; ⛔; (g) élesítés, az ISTENTISZT-001 kézi szövegeinek áthelyezése; (h) N15/N17 állapot.

## 2. G-döntések

- **G1 (szakaszrend).** Az oldal szerkezete, sorrendben:
  1. `# 📖 ID — cím`, alatta **Kivonat** *(kézi)*
  2. **Tartalomjegyzék** *(generált)* — horgonyokkal
  3. **Jelmagyarázat és rövidítések** *(generált, közös szöveg)*
  4. `## 1. Előfordulások` *(generált)*, benne `### 1/a. Az igehelyek szövege` *(generált)*
  5. `## 1/b. Kizárt és vizsgált helyek` *(generált)*
  6. `## 2. Szótári háttér` *(generált)*, alatta `### 2/b` *(kézi, ha van)* és `### Miért fontos ez a lelet` *(kézi)*
  7. `## 3. LXX-fordítói döntések` *(generált)*
  8. `## 4. Kereszthivatkozások` *(generált)*, alatta `### Minősítés` *(kézi)*
  9. `## 5. Kapcsolatok` *(generált)*, alatta `### Alátámasztás` *(kézi)*
  10. `## 6. Értelmezés` *(kézi)* — ide kerül a régi 1/b PaRDeS keretrendszer és a régi 7. ÚJ FELISMERÉS
  11. `## 7. Módszertan és nyitott kérdések` *(kézi)* — ide kerül a régi 6. Módszertani napló és a régi 8. Nyitott kérdések
  12. `## 8. Irodalom és idézés` *(generált)*
  13. `## Kolofon` *(generált)* — a régi 0. Metaadatok és a régi 9. Források és licencek
- **G2 (Előfordulások).** Tábla: Igehely | Kulcsszó (Károli-szó + eredeti szóalak **kiejtéssel** a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` `Kiejtés` oszlopából) | Funkció | PaRDeS-szint | Strong | Szótári jelentés | UBS-jelentés (csak ÚSZ-sornál) | Megbízhatóság · azonosítás módja. Az igehely horgony-link az 1/a-ra. A `proveniencia` és `igazolas` a tábla alatti számozott lábjegyzetbe kerül. Az **1/a** igehelyenként: horgony (`<a id="...">`), a Károli-vers szövege a `Karoli_1908.tsv`-ből (tartománynál minden vers), alatta a `kapcsolodas` szövege.
- **G3 (UBS).** Az UBS-jelentés renderidőben számolódik (LEXV2_1 G2), az `eszkozok/ubs_hozzarendeles.py` logikáját importálva, nem másolva. Megjelenés: `L–N kód — magyar definíció`, a magyar szöveg az új `adat/forditas_ubs.tsv`-ből; ha nincs fordítás, az angol eredeti áll `fordítás függőben` jelöléssel. `egyertelmu=nem` esetén minden jelölt jelentés felsorolva.
- **G4 (Thayer).** A 13 görög tokenhez egy-egy új `lexikon_hivatkozasok.tsv`-sor: `szotar=Thayer`, `szoveg_en` = a `Thayer_teljes.tsv` `Teljes_szocikk` mezője szó szerint, `forditas_hu` üres. A `jelentes_szam` a `SEMA.md` 2.2.2 szerint a teljes szócikkre megengedett érték; ha a 2.2.2 ilyet nem enged, ⛔ állj meg és jelentsd. Üres `forditas_hu` esetén a generátor `fordítás függőben` jelölést ír; gépi vagy saját fordítás nem kerül be. A fordításokat a felhasználó jóváhagyásával később, külön commitban kapja a `forditas_hu`.
- **G5 (LXX).** A 3. szakasz az `LXX_OS`-ből épül, a régi `LXX_kivonat_*.tsv` kikerül a generált rétegből. Minden ÓSZ-előfordulás-sorra (tartománynál minden versre) egy sor: Igehely (Károli) | LXX-igehely | Héber kulcsszó (kiejtéssel) | Görög megfelelő (ékezetes szóalak, lemma, átírás, G-szám) | Egyezés | Forrás. **Egyezés** = a motívum saját G-tokenje előfordul az LXX-versben (`egyező`). Ha nem: az `adat/lxx_dontesek.tsv` sora adja a görög megfelelőt (`eltérő`); ha ott sincs sor: `kutatói azonosítás függőben`. Automatikus héber→görög tippelés nincs. Ha a vers Károli-igehelye az `LXX_OS`-ben üres (`szamozas_elteres`), a sor ezt kiírja, üres görög mezővel. Licenc: CC BY 4.0 (lxx-morph, GreekWordList).
- **G6 (átírás).** Minden görög/héber szó mellett kiejtés áll. Héber és ÚSZ-görög szónál a TAHOT/TAGNT `Kiejtés` oszlopa, G-számos LXX-lemmánál a `Strong_szotar.tsv` `Kiejtés` oszlopa; ahol egyik sincs (csak LXX-ben előforduló lemma), determinisztikus gépi átírás SBL-séma szerint, `(gépi átírás)` jelöléssel.
- **G7 (Kizárt helyek).** Az 1/b a `jeloltek.tsv` `elutasítva` és `nyitva` sorait mutatja indoklással, és kiírja a `motivumok.tsv` `negativ_kriterium` mezőjét. `beépítve` sor nem jelenik meg.
- **G8 (Kereszthivatkozások, Kapcsolatok).** A 4. szakasz minden igehelyet Károli-formátumban ír (`Zsolt 50:15`, nem `Zsolt 50,15`). Az 5. szakaszban a tábla áll elöl, a Mermaid-ábra alatta, `<details>` blokkban.
- **G9 (Irodalom és idézés, 2. menetben szűk).** A 8. szakasz: „Hogyan hivatkozz" (ID, cím, `statusz_verzio`, `statusz_datum`, generálás dátuma, a fájl GitHub-URL-je) és a felhasznált szótárak listája a forrás-README-k szerinti teljes megnevezéssel. A teljes szakirodalmi bibliográfia-tábla a LEXV2_3 tárgya.
- **G10 (Jelmagyarázat).** A funkció-jelek jelentése a `SEMA.md` funkció-értékkészletéből, a PaRDeS-szintek a `PaRDeS_gyorsreferencia.md`-ből idézve, nem újrafogalmazva. A rövidítés-lista a használt forrásokat adja teljes névvel (BDB, TBESH, TBESG, Thayer, UBS, L–N = Louw–Nida, SDBH, SDGNT, OSHL, TWOT, TSK, KH = Károli-kereszthivatkozás, LXX, MT, KJV). Kötelező mondat: „A szótári fordításokban a πνεῦμα (pneuma) mindig *szellem*, a ψυχή (pszükhé) *lélek*; a Károli-idézetek szövege változatlan (pl. »Lélek«)."
- **G11 (kézi szöveg).** A kézi szakaszok szövege bájtra azonosan kerül át az új helyére; a generátor és a migráció kézi szöveget nem ír át, nem töröl, nem egészít ki.

## 3. Mi NEM hatókör

Szótári fordítás (Thayer, BDB); a Kivonat, Értelmezés és a többi kézi szöveg megírása; a TSK-minősítés és a kapcsolat-alátámasztás adatoszloppá alakítása és a bibliográfia-tábla (LEXV2_3); az `elofordulasok.tsv`, `kapcsolatok.tsv`, `jeloltek.tsv` tartalmi módosítása.

## 4. Tételek

### V2.0 — `karoli_ok` pótlás
Az `eszkozok/lxx_os_import.py` a `KEZI_ELTOLASOK`-ból jövő soroknál `karoli_ok=kezi_eltolas_tabla`-t írjon; futtasd újra. `git diff` csak a `karoli_ok` oszlopot érintheti az `LXX_OS/*.tsv`-ben (és a README számait). Jelentsd a pótolt sorok számát (vers-szinten várható ≈181).

### V2.1 — sablon v3
A `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` A) szakasza a G1 szerinti rendre írva, minden szakasznál (generált)/(kézi) jelöléssel és a G2–G10 tartalmi leírásával; a licenc-szakasz frissítése (Thayer: közkincs; LXX: `LXX_OS`, CC BY 4.0; a régi `LXX_kivonat` nem része a generált rétegnek); a Minőségi kapu L1 pontja az új szakaszlistára. Fejléc: `v3 — 2026.09.22 (LEXV2_2)`. A B) OLVASHATÓ archív szakasz és a közös szabályok változatlanok.

### V2.2 — új adattáblák
- `adat/forditas_ubs.tsv`: `strong | entry_kod | lexid | definicio_hu | glosszak_hu | megjegyzes | proveniencia`. A `lexid` a `konkordancia/UBS_DNTG_jelentesek.tsv`-ből a `strong` + `entry_kod` párral; ha nem egyértelmű, ⛔. Tartalom: az 5. pont 20 sora, szó szerint.
- `adat/lxx_dontesek.tsv`: `id | igehely | lxx_igehely | heber_strong | gorog_lemma | gorog_strong | lxx_pozicio | megjegyzes | proveniencia`. Ebben a körben üres (csak fejléc).
- Mindkettő bekerül a `SEMA.md`-be (új alpont) és az `ellenoriz.py` sémaellenőrzésébe; `ellenoriz.py` kód 0.
- A 3 soron, ahol az UBS-forrás `{N:001}` lábjegyzetet tartalmaz (G1311 88.266, G5351 88.266, G5590 9.20): nézd meg, van-e a lábjegyzet szövege az UBS-JSON-ban, és jelentsd (szó szerint, fordítás nélkül). A `forditas_ubs.tsv` `megjegyzes` mezője ezeknél: `forrásban {N:001} lábjegyzet`.

### V2.3 — Thayer-sorok
A G4 szerinti 13 új sor a `lexikon_hivatkozasok.tsv`-ben. Jelentsd a tokenenkénti karakterszámot.

### V2.4 — generátor
`eszkozok/lexikon_general.py`: új `VAZ_SABLON` és `BLOKK_NEVEK` a G1 szerint (új blokkok: `tartalom`, `jelmagyarazat`, `szovegek`, `kizart`, `idezes`, `kolofon`; az `lxx` blokk a G5 szerint újraírva; a `metaadat` és `forrasok` tartalma a `kolofon` blokkba). A G2–G10 megvalósítása. A régi `L._lxx_filename`/`LXX_kivonat` olvasás kikerül a lexikon-generálásból.

### V2.5 — migrációs szkript (még nem fut élesen)
`eszkozok/lexikon_v2_migracio.py`: meglévő oldalból kiolvassa a kézi szakaszokat (a régi címek alapján), felépíti az új vázat, és a G1 szerinti helyre illeszti őket. Önellenőrzés: szakaszonként a kézi szöveg bájtra azonos a migráció előtt és után; eltérésnél kilép hibakóddal. `--proba` kapcsolóval a `generalt_proba/lexikon/` alá ír.

### V2.6 — próba
`python eszkozok/lexikon_v2_migracio.py --proba` mind a 8 oldalra. Jelentés: oldalanként sorszám, szakaszlista, a G11-ellenőrzés eredménye; az 1. szakasz UBS-oszlopának kitöltöttsége; a 3. szakaszban `egyező` / `eltérő` / `függőben` / `szamozas_elteres` darabszám oldalanként; a Thayer-blokkok száma.

⛔ **Állj meg.** A felhasználó a `generalt_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md` alapján jóváhagyja vagy javíttatja a szerkezetet. A 2. kör csak ezután, a brief v2-vel indul.

### V2.7 — élesítés *(2. kör)*
A migráció élesben, a `lexikon/` alá; G11-ellenőrzés; `general.py --cel lexikon --ellenoriz` utána nem jelez változót.

### V2.8 — ISTENTISZT-001 LXX-döntések *(2. kör)*
Az ISTENTISZT-001 2/b és 6. Módszertani napló szövegében megnevezett nem-ἐπικαλέω (epikaleó) fordítások (pl. βοάω – boaó, καλέω – kaleó) átvétele az `lxx_dontesek.tsv`-be — **csak ott**, ahol a megnevezett lemma az `LXX_OS` adott versében ténylegesen szerepel; `proveniencia=ISTENTISZT-001 pilot szöveg + LXX_OS`. Ahol nem egyezik, sor nem kerül be; lista a jelentésbe.

### V2.9 — N15/N17 állapot *(2. kör)*
A `NYITOTT_FELADATOK.md`-ben: N15 lezárva (a régi kivonat kikerült a generált rétegből); N17 szűkítve: a régi `LXX_kivonat_*.tsv` már csak archív, a generált oldalakat nem érinti.

## 5. Az `adat/forditas_ubs.tsv` tartalma (V2.2)

A mezőket tabulátor választja el; `lexid` a V2.2 szerint töltendő, `proveniencia` = `forras=UBS_DNTG_jelentesek.tsv | forditas=chat-jovahagyas 2026.09.22`.

| strong | entry_kod | definicio_hu | glosszak_hu |
|---|---|---|---|
| G0012 | 1.20 | (az ἄβυσσος 'verem' jelentés átvitt kiterjesztése, amely az Újszövetségben nem fordul elő) a halottak helye, és az a hely, ahol az Ördögöt fogva tartják (Jel 20:3); a fenevadnak mint antikrisztusnak a lakóhelye (Jel 11:7), valamint Abaddoné, az alvilág angyaláé (Jel 9:11) | mélység; a gonosz lelkek lakóhelye; igen mély hely |
| G0086 | 1.19 | a halottak helye vagy lakóhelye, az igazakat és a hamisakat egyaránt beleértve (a legtöbb szövegösszefüggésben a ᾅδης[a] a héber seol megfelelője) | a halottak világa; Hádész |
| G0086 | 23.108 | (a ᾅδης[a] 'Hádész' [Louw–Nida 1.19] jelentés átvitt kiterjesztése: a Hádésznak mint a halottak helyének hatalmát személyesíti meg) | halál; a halál hatalma |
| G0282 | 10.17 | olyan személy, akinek anyjáról nincs feljegyzés, vagy akinek sohasem volt anyja, vagy akinek anyja meghalt | anya nélküli |
| G1311 | 20.40 | valakinek vagy valaminek a teljes pusztulását okozni | teljesen elpusztítani |
| G1311 | 88.266 | valakit romlottá vagy züllötté tenni, az erkölcsi pusztulás egy fajtájaként | megrontani; elferdíteni; tönkretenni; valakinek erkölcsi romlását okozni |
| G1941 | 33.131 | valakiről szólva megjelölést (címet, jelzőt) alkalmazni | hívni; nevezni |
| G1941 | 11.28 | (idióma, szó szerint: valakinek a nevét valakire hívják) elismertnek lenni úgy, mint aki ahhoz tartozik, akinek a nevét rá hívták | (Isten) népéhez tartozni; valakinek a népe lenni |
| G1941 | 33.176 | valakit arra hívni, hogy tegyen valamit; rendszerint segítségkérést is magában foglal | segítségül hívni; folyamodni valakihez; segítséget kérni |
| G1944 | 33.475 | átkozott állapotra vonatkozó | átkozott; elátkozott |
| G2671 | 33.474 | az, amit megátkoztak | átkozott; elátkozott |
| G4151 | 12.33 | természetfeletti, nem anyagi lény | szellem |
| G4151 | 12.18 | a Szentháromság harmadik személyének címe, szó szerint: szellem | Szellem; Isten Szelleme; Szent Szellem |
| G4151 | 26.9 | a nem anyagi, pszichológiai képesség, amely képes Isten iránt fogékony lenni és Istennek válaszolni (a πνεῦμα[e] ellentétben áll a σάρξ[f]-fel [Louw–Nida 26.7]: az isteni kifejeződése a pusztán emberivel szemben) | szellem; szellemi; szellemi természet; belső lény |
| G5010 | 58.21 | valamely dolog fajtája vagy típusa, más hasonló dolgokkal való szembeállítást és összehasonlítást feltételezve | fajta; típus |
| G5351 | 88.266 | valakit romlottá vagy züllötté tenni, az erkölcsi pusztulás egy fajtájaként | megrontani; elferdíteni; tönkretenni; valakinek erkölcsi romlását okozni |
| G5356 | 23.205 | rothadni vagy bomlani, szerves anyagra vonatkoztatva | rothadni; bomlani; bomlás |
| G5590 | 23.88 | az ember vagy más élőlény létezése, amelyet a belélegezhető levegő és az ennivaló jelenléte tart fenn | élet |
| G5590 | 26.4 | az élet lényege a gondolkodás, az akarás és az érzés tekintetében | belső én; elme; gondolatok; érzések; szív; lény |
| G5590 | 9.20 | (a ψυχή[a] 'belső én, elme' [Louw–Nida 26.4] jelentés átvitt kiterjesztése) személy mint élő lény | személy; emberek |

## 6. Várt számok

| Mérés | Várt |
|---|---|
| `forditas_ubs.tsv` sor | 20 |
| `lexikon_hivatkozasok.tsv` sor | 5 → 18 |
| Thayer-blokk az oldalakon | 13 token, minden olyan oldalon, ahol a token előfordul |
| `LXX_OS` pótolt `karoli_ok` | ≈181 vers |
| Próbaoldalak | 8 |
| 1. szakasz UBS-oszlop kitöltve | ≥ 33 ÚSZ-sor (a LEXV2_1 próba szerint) |
| 3. szakasz sorai | az ÓSZ-előfordulások versei (összesen 229), oldalanként mérve |
| G11 kézi szöveg-egyezés | 8/8 oldal |

## 7. Elfogadási kritériumok

- **K1:** `ellenoriz.py` kód 0 minden tétel után; az összesítő változását jelentsd.
- **K2:** az 1. körben a `lexikon/` alatt nincs változás (`git diff --stat lexikon/` üres).
- **K3:** minden görög/héber szó mellett kiejtés vagy `(gépi átírás)` áll a próbaoldalakon (szkriptes ellenőrzés, a kivételeket listázd).
- **K4:** a próbaoldalakon nincs `LXX_kivonat_` hivatkozás és `tisztazatlan` licenc az LXX-blokkban.
- **K5:** a TSK-blokkban nincs `,`-es igehely-alak (`\d+,\d+` minta a hivatkozásokban).
- **K6:** a G11-ellenőrzés mind a 8 oldalon egyezést ad.
- **K7:** üres `forditas_hu` / hiányzó UBS-fordítás mindenhol `fordítás függőben` jelölést kap, soha nem üres cellát.
- **K8:** a zárójelentés tartalmazza a 6. pont összes mért értékét és a V2.2 lábjegyzet-ellenőrzés eredményét.

## 8. Commitok

1. `LEXV2_2_BRIEF.md v1`
2. `V2.0: LXX_OS karoli_ok pótlás (kezi_eltolas_tabla)`
3. `V2.1: lexikon-oldal sablon v3`
4. `V2.2: forditas_ubs és lxx_dontesek tábla`
5. `V2.3: Thayer-sorok a 13 görög tokenhez`
6. `V2.4: generátor — lexikon-oldal v2`
7. `V2.5–V2.6: migrációs szkript és próba`

Push a K1–K8 teljesülése után, ⛔ előtt.

## Döntésnapló

| Verzió | Dátum | Döntés |
|---|---|---|
| v1 | 2026.09.22 | A felhasználó jóváhagyta a lexikon-oldal v2 szerkezetét és a G1–G7 javaslatot (chat). A πνεῦμα (pneuma) szótári fordítása mindig *szellem*, a spiritual *szellemi*; a ψυχή (pszükhé) *lélek* marad. A G5 a mérés miatt módosult: héber→görög megfelelő-lista gépi formában nincs (HebrewStrong.xml 0/8674, TBESG csak prózában), ezért automatikus tippelés helyett `adat/lxx_dontesek.tsv` kutatói adat. A bibliográfia-tábla, a minősítés és az alátámasztás adatosítása a LEXV2_3-ba került. Két kör ⛔ megállással. |
| v2 | 2026.09.22 | **V2.2 közbeni ⛔:** a G1944/33.475 pár a `UBS_DNTG_jelentesek.tsv`-ben `strong`+`entry_kod` szerint nem egyértelmű (2 sor: `strong_kod=G1944` ἐπικατάρατος és `strong_kod=G1944a` ἐπάρατος, azonos `entry_kod`/`domen_kod`/`megjegyzes`). Felhasználói döntés: a `lexid` a pontos `strong_kod`-egyezéssel dől el (`strong_kod` == `strong`, betűutótag nélkül) → G1944 → `lexid=001960001001000` (ἐπικατάρατος); megerősítve az `adat/elofordulasok.tsv` 248–249. sorával (HAMART-001, Gal 3:10/3:13), amely kifejezetten ezt a lemmát idézi. **Általános szabály (V2.2 és a generátor G3-lekérdezése egyaránt):** a kulcs `strong`+`entry_kod`; ha ez több sort ad, a pontos `strong_kod`==`strong` egyezés dönt; ha így is több vagy nulla sor marad, ⛔. A `forditas_ubs.tsv` G1944/33.475 sorának `megjegyzes` mezője rögzíti a kizárt alternatívát. |
| v3 | 2026.09.22 | **V2.3 közbeni ⛔:** a `Thayer_teljes.tsv` nem bont számozott jelentésekre (egy sor = teljes szócikk Strong-számonként), a `SEMA.md` 2.2.2 `jelentes_szam` union-je pedig nem definiált erre az esetre, holott a mező kötelező a 2.5-ben. Felhasználói döntés: a union ötödik értékkel bővül — `teljes` = a teljes szócikk, jelentés-bontás nélkül. Három korlát: (1) csak olyan szótárnál használható, amelynek forrásfájlja ténylegesen nem bont számozott jelentésekre (jelenleg: Thayer); (2) csak a `lexikon_hivatkozasok.tsv`-ben szerepelhet, az `elofordulasok.tsv` `jelentes_szam` mezője sosem `teljes`; (3) egy `szotar`+`strong`+`entry_id` hármashoz legfeljebb egy `teljes` sor. Az `entry_id` a Thayer-soroknál a `Thayer_teljes.tsv` `Strong_eredeti` mezője (nullázatlan, pl. `G12`), eltérve a BDB/LSJ/SECE `Strong_padded`-konvenciójától — a `SEMA.md` 2.5 táblája frissült. Mindkét korlát (2-3) bekerült az `eszkozok/ellenoriz.py`-ba (9. szabály). **A V2.2 hiánya is pótolva:** a `forditas_ubs.tsv` és a `lxx_dontesek.tsv` bekerült az `ellenoriz.py`-ba (10. szabály) — fejléc-oszlopok, `forditas_ubs.tsv` 20 sor/egyedi kulcs/létező `lexid`/nem üres `definicio_hu`, `lxx_dontesek.tsv` fejléc + soronkénti `igehely`+`gorog_strong` kitöltöttség. Új összesítő: RENDBEN 6→8, SÉRTÉS 0, KÉZI 3, JELENTÉS 1 (exit 0). |
| v4 | 2026.09.22 | **V2.6a — a felhasználó jóváhagyta a próbaoldalt, hat javítással a 2. kör előtt** (chat): (1) a migrált kézi címek egy szinttel lejjebb kerülnek, számozás nélkül (`### PaRDeS keretrendszer`, `### Új felismerés`, `### Módszertani napló`, `### Nyitott kérdések és séma-korlátok`), belső `###` címeik `####`-ra demótálva; a `### 2/b` helyőrző csak akkor generikus, ha nincs valódi kézi 2/b — a `G11` csak a szakasztörzsre vonatkozik, a címre nem. (2) A 2. szakasz tokencíme lemmát + kiejtést hordoz (`### G1941 — ἐπικαλέω (epikaleō)`), forrása a `TBESG.txt`/`TBESH.txt` 4–5. oszlopa (nem a `Strong_szotar.tsv`), betűutótag nélküli alapalakra visszaeső fallback-kal (a TBESH sense-onként bont: `H2416a` stb.); a 3. szakasz lemma-kiejtése ugyanonnan, G-szám nélküli LXX-lemmánál gépi átírással. A TAHOT/TAGNT ragozott-alak-kiejtés kizárólag az 1. szakasz Kulcsszó oszlopában marad. (3) Az 1/a Károli-vers dőlt bekezdés, nem blockquote, az igehely nem ismétlődik a sor végén. (4) A 3. szakasz LXX-igehelye magyar rövidítéssel, `(LXX)` jelöléssel csak számozás-eltérésnél (`Zsolt(LXX) 114:4`), egyezéskor jelölés nélkül (`1Móz 4:26`) — az `LXX_OS` saját fejezet:vers száma és a `lxx_os_import.BOOK_KEY_TO_KAROLI` szerint. (5) A 8. szakasz „Felhasznált szótárak" teljes névvel (a G10 rövidítés-listájával egyezően), fájllal zárójelben; az `adat/*.tsv` és a Károli-fájlok külön „Adatforrások" alcím alá kerülnek. (6) A `lxx_dontesek.tsv` új `tipus` oszlopa (`eltero_forditas` \| `lxx_minusz`); `lxx_minusz`-nál a 3. szakasz „nincs megfelelő a görögben (LXX-minusz)" szöveget ír a Görög megfelelő cellába. `SEMA.md` 2.11 és `ellenoriz.py` 10. szabálya frissült (a `gorog_strong`-kötelezőség megszűnt `lxx_minusz`-nál). **A négy ISTENTISZT-001-es függő hely (Zsolt 116:17, Ézs 12:4, 2Móz 33:19, 34:5) vizsgálata és az `lxx_dontesek.tsv` tartalmi feltöltése a V2.8 tárgya marad, ebben a körben nem történt meg** — a felhasználó a 2. kört külön jóváhagyás után indítja. |
| v5 | 2026.09.22 | **V2.6a jóváhagyva, V2.7–V2.9 lefutott** (chat). **V2.7-előtti javítás:** a 8. szakasz „Felhasznált szótárak" listája mostantól a `lexikon_hivatkozasok.tsv`-ben ténylegesen idézett szótárak saját forrásfájlját is felsorolja (nem csak magát a `lexikon_hivatkozasok.tsv`-t) — BDB (`konkordancia/BDB_teljes_unabridged.tsv`) és Thayer (`konkordancia/Thayer_teljes.tsv`) teljes névvel, a `blokk_szocikkek` minden idézett sor `forrasfajl` mezőjét regisztrálja; egy szótár egy sorban jelenik meg (fájljai zárójelben), a `lexikon_hivatkozasok.tsv` maga az „Adatforrások" alatt marad. Szkriptes ellenőrzés (a 2. szakasz `#### <szótár> <ID> —` alcímei mind szerepelnek a 8. szakaszban): 8/8. **V2.7:** a migráció élesben lefutott (`lexikon_v2_migracio.py`, `--proba` nélkül); a `general.py --cel lexikon --ellenoriz` mind a 8 oldalra „változatlan"-t ad (fixpont). **V2.8:** az ISTENTISZT-001 pilot szövege (2/b és a 8. pont Módszertani napló/Nyitott kérdések N15/N17-jegyzete) alapján 4 sor került az `lxx_dontesek.tsv`-be — mindegyiket az `LXX_OS` nyers szavai igazolják: 2Móz 33:19 és 34:5 → καλέω (G2564, `eltero_forditas`, pilot: „a fordító pont ezt az igét választotta Isten önmegnevező aktusára, nem az ἐπικαλέομαι-t"); Ézs 12:4 → βοάω (G0994, `eltero_forditas`, pilot: „az Ézs 12:4-nél használt fordítói döntés (βοάω)"); Zsolt 116:17 (LXX Zsolt 115:8) → `lxx_minusz` (pilot: „a görög LXX autentikusan nem fordítja le a vers második felét"). Az ISTENTISZT-001 oldal újragenerálva (`--ir`); a többi 7 oldal változatlan maradt (a `lxx_dontesek.tsv` csak ezekre a versekre vonatkozik). **Hiba menet közben:** a G994 Strong-szám nullázatlanul került be (`G994` a `STRONG`-típus `G0994` helyett) — a TBESG-lemma-kiejtés-lookup emiatt eleinte gépi átírásra esett vissza; javítva. **V2.9:** N15 lezárva (a lexikon-generátor kizárólag az `LXX_OS`-t olvassa a 3. szakaszhoz, a régi `LXX_kivonat_*.tsv`-re nincs hivatkozás egyetlen oldalon sem); N17 szűkítve (a régi kivonat csak archív, generált oldalt nem érint, a Zsoltár-számozási gyanú vizsgálata csak akkor válik ismét éles kérdéssé, ha valaki újra bemenetként használná). |
| v6 | 2026.09.22 | **V2.9 utáni javítás** (chat): a `lxx_igehely_magyar` segédfüggvény (V2.6a pont 4) mostantól az `lxx_dontesek.tsv`-ből jövő `eltérő`/`lxx_minusz` sorok LXX-igehelyét is magyar rövidítésre alakítja (pl. `2Móz 33:19`, `Ézs 12:4`, `Zsolt(LXX) 115:8`) — a függvény jelt cserélt: a `LXX_OS`-sor helyett közvetlenül a nyers igehely-string paramétert veszi, hogy mindkét forrásra (LXX_OS és lxx_dontesek) használható legyen. Az `adat/lxx_dontesek.tsv` `lxx_igehely` mezője változatlanul angol (`LXX_OS`-kulcs) marad — csak a generált oldal megjelenítése magyar. Az Egyezés-oszlop `tipus=lxx_minusz`-nál `LXX-minusz` (nem `eltérő`); az összesítő sor ötrészes: `egyező | eltérő | LXX-minusz | kutatói azonosítás függőben | szamozas_elteres`. ISTENTISZT-001 eredmény: 18/3/1/0/0 (a várt szám). Ellenőrzés: a 3. szakaszban egyetlen oldalon sincs angol könyvnév (`Genesis\|Exodus\|Isaiah\|Psalms\|Kings\|Chronicles\|Jeremiah\|Joel\|Zechariah\|Zephaniah` minta) — 0 találat mind a 8 oldalon. `general.py --cel lexikon --ir` mind a 8 oldalt frissítette (a formátumváltás miatt, tartalmilag csak ISTENTISZT-001 4 sora tér el); `--ellenoriz` utána fixpont. |
