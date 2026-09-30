---
feladat: 21
cim: Károli–Strong mérőpilot (minőség és költség)
kod: F21
tipus: feladat
fazis: 1
modell: sonnet
allapot: lezarva
ad: mért adat arról, megéri-e a teljes Bibliát külső modellekkel Strong-számmal párosítani (minőség, költség, KJV-támpont haszna)
kovetkezo: lezárva, nem felel meg; a #22 sorsa a felhasználó döntése (l. DT21)
olvas: [konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_Strong_kivonat.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/KJV_Strongs_Genesis.tsv]
ir: [eszkozok/karoli_strong/, f21p/, naplok/F21P_jelentes.md, DONTESEK.md, .github/workflows/f21p_pilot.yml]
ag: claude/f21-pilot
lezarva_osszegzes: Károli–Strong mérőpilot (F21): egyik összeállítás sem felel meg a rögzített döntési szabálynak (az A+B `magas` pontossága és az A/B kapuhibája bukott, a C egymodelles szabály szerint nem minősíthető, rétegenként 91,7–95,6% pontosság a 98% ellen); C-vetítés 42 USD (90%: 38–47), a pilot 0,7346 USD; KJV (N29): a v1-adaton nem teljesül, n=8, nem végleges; jelentés `naplok/F21P_jelentes.md`
fugg: [6]
---
# F21_KAROLI_STRONG_PILOT_BRIEF.md — Károli–Strong párosítás: mérőpilot (minőség és költség)

*FELADATOK #21 · pilot · v1 · 2026.09.30 · Modell: sonnet (szkript, mérés) · aranyminta: opus (`vegrehajto-opus`) · Külső modellek (OpenRouter): `google/gemini-3.1-flash-lite` (A), `deepseek/deepseek-v4-flash` (B), `google/gemini-3.8-flash` (C) · Ág: `claude/f21-pilot` · Egy menet, egy ⛔ megállással*

## Mit ad, ha kész

Mért adatot arról, hogy megéri-e a teljes Bibliát külső modellekkel párosítani, és ha igen, melyik összeállításban. A pilot három kérdésre felel:

1. **Minőség:** milyen pontosan párosítanak a modellek egyenként, párban és döntőbíróval, bibliai műfajonként külön mérve.
2. **Költség:** mennyibe kerülne a teljes futás. A becslés a pilot mért token-felhasználásából és a teljes Biblia valódi vershosszaiból készül, nem naiv szorzással. (A Thayer-becslés tanulsága: a ~30 USD nem volt levezethető, `naplok/ELLENOR_FP.md`.)
3. **A KJV-támpont haszna:** érdemes-e a teljes KJV-t importálni (N29), vagy a modellek nélküle is elég jók.

A pilot **mérés, nem adatgyártás**. Nem kerül adat az `adat/` és a `konkordancia/` könyvtárba. A prompt, a kapu és az aranyminta viszont újrahasználható a teljes futáshoz (`F22_KAROLI_STRONG_BRIEF.md`), ezért annak 22.1–22.4 lépése a pilot után lerövidül.

## Munkamegosztás

| Lépés | Ki végzi |
|---|---|
| Minta, tokenizálás, prompt, kapu, mérőszkriptek | Code (sonnet) |
| Aranyminta 60 versre | `vegrehajto-opus`, a modellek válaszainak ismerete nélkül |
| Az aranyminta szúrópróbája és a küszöbök megerősítése | te, a ⛔ pontnál |
| Modellfuttatás | GitHub Actions, OpenRouter |
| Jelentés és javaslat | Code, kizárólag a szkriptkimenetekből |
| Ellenőrzés | CI és `fuggetlen-ellenor` |

## Keretek

- **A modell nem ír Strong-számot**, csak sorszámpárokat. A Strong-számot a mérőszkript veszi a TAHOT/TAGNT-ből (l. a fő brief 22.1 pontját).
- **Számadat** csak szkriptkimenetből kerülhet a jelentésbe.
- **Kulcs:** `OPENROUTER_API_KEY` repo-secret, csak az Actions job `env`-jében; commit előtt kulcs-grep.
- **HTTP-kliens:** az `eszkozok/fordit.py` `_valodi_http_kuldo` függvénye, újrahasználva. A költséget a válasz `usage` mezőjéből naplózd hívásonként (bemeneti, kimeneti és gondolkodási token, és a `cost`, ha a válasz tartalmazza).
- **Gondolkodási mód:** mindhárom modellnél ugyanaz a beállítás, rögzítve a futásnaplóban (javaslat: kikapcsolva vagy a legalacsonyabb szinten). A gondolkodási token a költségbe beleszámít.
- **Költségplafon: 3 USD** a teljes pilotra. Minden köteg előtt ellenőrizd.
- Minden lépés után commit és push.

## Lépések

### P0. Előkészítés

1. **Tokenizálás:** `eszkozok/karoli_strong/tokenek.py` (Károli: Unicode betű- és számjegysorozat). Az eredeti szavak versen belüli sorszámát a TAHOT/TAGNT sorrendje adja; ellenőrizd a nyers fájl `#01, #02…` sorszámával (`konkordancia/TAHOT_TAGNT_README.md`).
2. **Minta (rögzített véletlenmaggal):** `f21p/minta.tsv`, 200 vers, négy rétegben:

   | Réteg | Könyvek | Vers | KJV-támpont |
   |---|---|---|---|
   | R1 ÓSZ, próza + bölcsesség | 1Móz 40, 2Móz 30, Péld 30 | 100 | van (meglévő `KJV_Strongs_*.tsv`) |
   | R2 ÓSZ, költészet | Zsolt, Jób | 25 | nincs |
   | R3 ÓSZ, próféták | Ézs, Jer, Ez | 25 | nincs |
   | R4 ÚSZ | evangéliumok 25, levelek 25 | 50 | nincs |

   Az R1 1Mózes-verseinek legalább fele olyan vers legyen, amelyhez van sor a `Karoli_Strong_kivonat.tsv`-ben (régi arany). A 61 + 30 versmegfeleltetési maradék verse nem kerülhet a mintába.
3. **Prompt és kapu:** a fő brief 22.1 pontja szerint (bemenet, JSON-kimenet, H9xxx-szabály, `betoldas`, `forditatlan`, ötpontos kapu, egy újrakérés). A prompt: `f21p/prompt_v1.md`. Kötegméret: 10 vers / hívás.
4. **A régi arany:** a `Karoli_Strong_kivonat.tsv` mintába eső sorai `(igehely, Károli-szó, Strong)` hármasként, Károli-natív igehellyel és nullázott Strong-számmal, csak memóriában.

### P1. Aranyminta

A `vegrehajto-opus` 60 versre teljes, szó-szintű párosítást készít a modellek JSON-formájában: R1-ből 20, R2 és R3 együtt 20, R4-ből 20 verset. A modellek válaszait nem láthatja; ezek ekkor még nem is léteznek. Kimenet: `f21p/arany_opus.jsonl`.

### P2. ⛔ Megállás a futtatás előtt

Nyiss tételt a `DONTESEK.md`-ben, és kérd:

1. **Szúrópróba:** az Opus-aranyból 10 vers (rétegenként 2–3, a szkript választja), olvasható formában (`naplok/F21P_arany_szuroproba.md`: magyar szó → eredeti szó, Strong, angol glossza). A felhasználó jelzi a hibás linkeket. Ha a hibás linkek aránya 3% fölött van, az Opus javítja az aranyat, és a szúrópróba megismétlődik.
2. **A döntési küszöbök megerősítése** (lent, „Döntési szabály”). **A küszöbök a futtatás előtt rögzülnek, utána nem változnak.**
3. **Secret:** az `OPENROUTER_API_KEY` repo-secret beállítva.

### P3. Futtatás (Actions)

Workflow: `.github/workflows/f21p_pilot.yml`, indítás push-ra, ha az `f21p/futtatas.txt` változik.

| Futás | Modell | Versek | Cél |
|---|---|---|---|
| F1 | A | 200 | egyéni minőség, költség |
| F2 | B | 200 | egyéni minőség, költség, A–B egyezés |
| F3 | C | 200 | az erősebb modell egyedül; olcsóbb-e, mint A + B + döntőbíró |
| F4 | C döntőbíróként | az F1–F2 eltérő versei | a döntőbírós összeállítás minősége és költsége |
| F5 | A, KJV nélkül | R1, 100 | a KJV-támpont haszna |
| F6 | B, KJV nélkül | R1, 100 | a KJV-támpont haszna |

A nyers válaszok: `f21p/valaszok/<futás>.jsonl`. Futásnapló hívásonként: `f21p/futasnaplo.tsv`.

### P4. Mérés

`eszkozok/karoli_strong/meres.py` minden összeállításra (**A**, **B**, **C**, **A+B** egyezéses, **A+B+C** döntőbírós) és rétegenként külön számolja:

| Mérőszám | Definíció |
|---|---|
| Pontosság | a kimenet linkjeiből hány van az Opus-aranyban; a bizonyossági szintekre külön is (`magas`, `kozepes`, `alacsony`, a fő brief G4 szabálya szerint) |
| Lefedettség | az arany linkjeiből hány van a kimenetben |
| Régi arany egyezés | a régi hármasokból hány egyezik (azonos vers és Károli-szó, a Strong-szám a linkelt eredeti szavak között) |
| A–B egyezés | az azonos linkek aránya a két modell linkjeinek uniójához |
| Kapuhiba-arány | első és második próbálkozás után |
| `alacsony` arány | a linkek hány százaléka kapna `alacsony` jelölést |
| KJV-hatás | F1–F5 és F2–F6 különbsége az R1-en: pontosság, lefedettség, A–B egyezés |

### P5. Költségvetítés

A becslés levezetése, lépésenként a jelentésbe írva:

1. Hívásonként a mért token-felhasználás (bemenet, kimenet, gondolkodás) és a vers-tulajdonságok: eredeti szavak száma, Károli-szavak száma, van-e KJV-támpont.
2. Modellenként és tokenfajtánként lineáris illesztés: `token = a + b · (eredeti szavak + Károli-szavak)`, a köteg utasításrészét hívásonként egyszer számolva.
3. Az illesztés alkalmazása a teljes Biblia **valódi** vershosszaira (31 158 vers, a `Karoli_1908.tsv`, a `TAHOT_kivonat.tsv` és a `TAGNT_kivonat.tsv` alapján), rétegenkénti besorolással (a 66 könyv négy rétegbe sorolva, a besorolás táblája a jelentésben).
4. Ár: a válasz `cost` mezője, ha van; ha nincs, a `fp2/koltsegbecsles.py` modelláraiból.
5. Összeállításonként: **A+B+C** = A + B + (eltérési arány × C döntőbíró), ahol az eltérési arányt és a döntőbírói hívás tokenigényét rétegenként a pilot adja.
6. Bizonytalanság: bootstrap a pilot versein (1 000 újramintavétel), 90%-os intervallum.
7. Ellenőrzés: a pilot saját tényleges költsége és a módszerrel a 200 versre vetített költség eltérése a jelentésbe kerül. Ha az eltérés 10% fölött van, a módszert javítani kell, mielőtt a vetítés bekerül.

Kézimunka-vetítés: a teljes Bibliára várható `alacsony` linkek száma és a fő brief 22.7/3 szerinti átnézési sor mérete.

### P6. Jelentés és zárás

- `naplok/F21P_jelentes.md`: a mérőszámok összeállításonként és rétegenként, a költségvetítés levezetéssel és intervallummal, a KJV-hatás, a javaslat a döntési szabály szerint.
- Döntési tétel a `DONTESEK.md`-ben (a javaslattal).
- `fuggetlen-ellenor` (`naplok/ELLENOR_F21P.md`), push, draft PR, a `FELADATOK.md` #21 sorának frissítése.

## Döntési szabály (a P2 ⛔ pontnál rögzül)

Egy összeállítás **megfelel**, ha:

- a `magas` linkek pontossága ≥ 98% minden rétegben;
- az összes link lefedettsége ≥ 95%;
- a régi arany egyezése ≥ 95%;
- a vetített teljes költség 90%-os intervallumának felső széle ≤ 60 USD;
- a vetített `alacsony` arány ≤ 10%.

**Javaslat:**

- ha van megfelelő összeállítás, a legolcsóbb megfelelő;
- ha csak egyes rétegekben felel meg, vegyes összeállítás rétegenként (pl. R1 és R4 A+B-vel, R2–R3 A+B+C-vel);
- ha egyik sem felel meg, a teljes futás nem indul, és a jelentés megnevezi, mi bukott el (pontosság, költség vagy kézimunka).

**Egymodelles összeállítás (A, B, C külön; rögzítve 2026.09.30, PD6):** a P4 ezeket is méri (összpontosság, lefedettség, régi arany egyezés, költség), és a C egyedül versenyez az A+B+C-vel (PD2), de csak a jelentés kedvéért. Egymodelles összeállításhoz a G4 szerinti `magas` / `alacsony` szint nem értelmezhető (az A és a B egyezésén alapul), ezért az ilyen összeállítás nem kaphat megfelelt minősítést, és a teljes futásra, rétegenként sem, mehet. **A teljes futásra, rétegenként is, csak az A+B vagy az A+B+C mehet.** A G4 nem változik.

**KJV-import (N29):** érdemes, ha a KJV-támpont az R1-en legalább 1 százalékponttal növeli a `magas` pontosságot, vagy legalább 20%-kal (relatívan) csökkenti az A–B eltérést.

## Kész, ha

- **P-K1** A minta és a régi arany rögzítve, a sorrend-ellenőrzés lefutott.
- **P-K2** Az Opus-arany elkészült, a szúrópróba lezárult (≤ 3% hibás link).
- **P-K3** Az F1–F6 futások lefutottak, a kapuhibák naplózva.
- **P-K4** Minden mérőszám összeállításonként és rétegenként a jelentésben.
- **P-K5** A költségvetítés levezetve, intervallummal, és a 200 versre visszaellenőrizve (≤ 10% eltérés).
- **P-K6** A pilot összköltsége ≤ 3 USD, a futásnapló alapján.
- **P-K7** Javaslat a döntési szabály szerint; a döntési tétel a `DONTESEK.md`-ben.
- **P-K8** Kulcs-grep tiszta, `ELLENOR_F21P.md` TISZTA, CI zöld.

<!-- KOZVETLEN_FUTTATAS -->
## Nyitó prompt (a Code-sessionhöz, `/kovetkezo` után)

> A feladat: FELADATOK #21 mérőpilotja. A brief: `F21_KAROLI_STRONG_PILOT_BRIEF.md` a repó gyökerében; a prompt és a kapu leírása a fő briefben van (`F22_KAROLI_STRONG_BRIEF.md` 22.1). Futtasd a P0–P1 lépéseket, a P2 ⛔ pontján állj meg, és a tételt a `DONTESEK.md`-be írd. A „mehet” után P3–P6. Ág: `claude/f21-pilot`. Minden lépés után commit és push. A végén `fuggetlen-ellenor`, push, draft PR, a `FELADATOK.md` #21 sorának frissítése.
<!-- /KOZVETLEN_FUTTATAS -->

## A FELADATOK.md #21 sorának „Következő lépés” mezője

> Mérőpilot (`F21_KAROLI_STRONG_PILOT_BRIEF.md`): minőség és költségvetítés 200 versen, ⛔ a futtatás előtt. A teljes futás csak a pilot megfelelő eredménye után.

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| PD1 | Önálló mérőpilot a teljes futás előtt | a teljes futás költsége és minősége nem ismert; a pilot legfeljebb 3 USD | a fő brief 1. menete (több előkészítés, pl. KJV-import, még a mérés előtt) |
| PD2 | A C modell a teljes mintán is fut, nem csak döntőbíróként | kiderül, hogy egyetlen erősebb modell olcsóbb-e, mint két gyenge és egy döntőbíró | csak döntőbírói mód |
| PD3 | KJV-támpont az R1-en, kikapcsolt változattal is | az N29 importdöntéséhez mért adat kell; az R1 könyveihez már van KJV-tábla, import nélkül | a KJV importja a mérés előtt |
| PD4 | Költségvetítés illesztéssel a valódi vershosszakra, bootstrap-intervallummal és visszaellenőrzéssel | a naiv szorzás a Thayer-becslésnél nem volt levezethető | átlagköltség × versszám |
| PD5 | A küszöbök a futtatás előtt rögzülnek | a mérés utáni küszöbállítás torzít (az F06 BSB-mérés gyakorlata) | küszöb az eredmények láttán |
| PD6 | Egymodelles összeállítás (A, B, C külön) csak mérésre; a teljes futásra rétegenként is csak A+B vagy A+B+C mehet | a G4 bizonyossági szintje két modell egyezésén alapul, egy modellnél nem értelmezhető | megengedő változat: minden link `magas`, az `alacsony` a kapuhibás versek aránya |
| PD7 | `[nem TR]`: a „TR»N” és „TR«N” TR-nek számít (tokenek.py javítás), a „más helyen” versekre az alternatív arany; az „eltérő alak” három tokenje (Jak 3:4 #22, Jak 3:8 #8, 1Pét 5:12 #23) kimarad a pontossági mérésből | a modell-bemenet és az arany a TR-rel összhangban legyen; az eltérő alaknak nincs sora a kivonatban | jelölés a jelentésben; kizárás a mintából |
| PD8 | Az A és a B kiesik, v2 nem lesz hozzájuk; az F4 nem fut | a kapun átment versekben is az A pontossága 81,2%, a B-é 65,1%; a 197/200 döntőbírós vers mellett az F4 nem ad új információt az F3-hoz képest | v2 az A-hoz és a B-hez; F4 a jelenlegi adattal |
| PD9 | A régi arany egyezése halmazként mért (összetett Strong a `+` mentén bontva); a két hibás hármas (1Móz 6:17, 13:4) jelölve (`f21p/regi_arany_hibas.tsv`), nem javítva | a `meres.py` az összetett Strongot egész karakterláncként hasonlította: mérési műtermék | a régi arany javítása |
| PD10 | Arany v2: csak a jegyzet konvenciójával ütköző esetek, a sértett konvenció számával; a 6. táblázat a futás előtt lezárult, nem bővül; a korrigált pontosság csak „az Opus besorolása, nem mérés” megjelöléssel szerepelhet, a küszöb szempontjából csak a mért érték számít | az arany ne igazodjon a mért modellhez | az arany szabad javítása a C-diff alapján |

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.30 | első változat |
| v1.1 | 2026.09.30 | a P2 ⛔ döntései: a küszöbök rögzítve (PD5); egymodelles összeállítás csak mérésre, a teljes futásra csak A+B vagy A+B+C (PD6); a vegyes példa: R1 és R4 A+B-vel, R2–R3 A+B+C-vel; `[nem TR]` javítás és az „eltérő alak” tokenek kizárása a pontossági mérésből (PD7) |
| v1.2 | 2026.09.30 | a P3/P4 utáni döntések: az A és a B kiesik (a kapun átment versekben is 81%, illetve 65% pontosság), v2 nem lesz hozzájuk, az F4 nem fut (PD8); a régi arany egyezése halmazként mért, a 2 hibás hármas jelölve (PD9); arany v2 csak a jegyzet konvenciójával ütköző esetekre, jóváhagyásig nem fagy be (PD10); KJV (N29): a v1-adaton nem teljesül, n=8, nem végleges |
