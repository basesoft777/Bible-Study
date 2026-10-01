---
feladat: 21
cim: Károli–Strong mérőpilot (minőség és költség)
kod: F21
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ad: mért adat arról, megéri-e a teljes Bibliát külső modellekkel Strong-számmal párosítani (minőség, költség, KJV-támpont haszna)
kovetkezo: regressziós mérés (P3c): a jegyzet v2, prompt_v3, F3V3 és a Sonnet; ⛔ a Sonnet szárazbecslésénél és az arany v3 diffjénél
olvas: [konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_Strong_kivonat.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/KJV_Strongs_Genesis.tsv]
ir: [eszkozok/karoli_strong/, f21p/, naplok/F21P_jelentes.md, DONTESEK.md, .github/workflows/f21p_pilot.yml]
ag: claude/f21-regresszio-meres
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
| PD11 | A DT21 lezárása visszavonva, a pilot folytatódik (P3b): minden összeállítás kimérve a `prompt_v2`-vel, a C második futásával az ingadozás mérésére; az F4v2 csak akkor fut, ha a döntőbírói prompt teljesíti a rögzített feltételeket (az A–B egyező linkek rögzítettek, a séma és a kapu ugyanaz, nincs modell által írt Strong-szám, K5); plafon 3 USD, 2 USD kumulatív költségnél megállás és jelentés | az A és a B nem volt mérve a `prompt_v2`-vel, az A+B+C (F4) egyszer sem futott, a két C-futás nélkül a futások közti ingadozás nem választható el a prompthatástól (a 97%-os és 98%-os mért érték nem hasonlítható) | a pilot lezárása a meglévő adattal (DT21) |
| PD12 | A DT21 döntései: a mért régi arany érték a kizárás nélküli (C 93,8%, 30/32), a kizárás csak tájékoztatás; az 1Móz 13:4 „hibás” jelölése visszavonva, csak az 1Móz 6:17 marad (a PD9 ennek megfelelően módosul); a P5 teljes-Biblia rétegbesorolása az F22 brief szerinti, műfaji (Préd, Sir → költészet, Dán → próféta, Ruth, Eszt → ÓSZ-próza); a köteg mint bootstrap-egység elfogadva; a költség-ellenőrzésnél a konzervatívabb (leave-one-out) számít; az `alacsony` arányt az A+B+C-nél a szó szerinti G4-olvasat adja (59,7%), az A+B definíciója elfogadva; a gondolkodási mód eltérése (A és B kikapcsolva, C `minimal`) a pilot idején elfogadva; az a–e tételek regressziós mérésre átvéve; a #22 döntése elhalasztva a regressziós futás utánra | a mért érték ne függjön utólagos kizárástól; a rétegbesorolás egységes az F22-vel | a kizárásos érték mint mért érték |
| PD13 | Regressziós mérés (P3c): (1) az a–e döntések (K7: a jegyzet az irányadó, a prompt kivétele szűkül; C: a névmás csak *'et* + ragnál megy az igére, máshol `betoldas`; „azt/azért … hogy”: a mutató névmás `betoldas`, ha nincs eredetije, a *hogy* a kötőszóra megy; 2Móz 26:13 *is* marad; D: a rag arra a magyar szóra megy, amelyik a megfelelő személyragot viseli) a jegyzet v2-be; ha valamelyik az arany v2 linkjeit érinti, versenkénti diff és megállás a jóváhagyásig, az arany v3 csak utána fagy be; (2) `prompt_v3` a tíz konvencióval és az a–e pontokkal, a példaversek nincsenek a 200 verses mintában; (3) F3V3 (C, 200 vers) és a Sonnet az OpenRouteren (`prompt_v3`, 200 vers, ugyanaz a kapu és mérés), a mérés az arany legfrissebb befagyott változatára, rétegenként, a v2-es két C-futással egymás mellett, a (c) hibák újrabesorolásával; (4) a Sonnet szárazbecslése a trigger előtt; a pilot kumulatív költsége (1,605 USD) ezzel 3 USD fölé nem mehet; (5) a P4 a Sonnetet egyedül és a Sonnet + C párt méri (A∩B = `magas`, a C döntőbírós változat nélkül; a párban a C a saját F3V3-futása a `prompt_v3`-mal; ha az egyik oldal kapuhibás, a vers minden linkje `alacsony` és beleszámít az `alacsony` arányba), rétegenként, az öt feltétellel; (6) a P5 a Sonnet egyedül és a Sonnet + C költségét vetíti a teljes Bibliára, 90%-os intervallummal; (7) az Opus nem fut, mert az arany is Opus, így a mérés nem lenne független; (8) megállás a mérés után, a #22 döntése a felhasználóé | a DT21 döntései (a–e regressziós mérésre átvéve) és a felhasználó kiegészítései | a prompt módosítása mérés nélkül; Opus a mérésben |
| PD14 | A regressziós mérés döntései (2026.10.01): (1) az arany v3 az **A változat** (3 link: Jób 33:13 *Azért*, Mt 21:4 *azért*, Ez 39:13 *ezt* → `betoldas`; 1048 link), a **B elutasítva**, mert ütközik a K4-gyel; befagyasztás előtt a jegyzet v2 és a `prompt_v3` C/D szövege ellenőrizve (a magyar tárgyi névmás csak akkor `betoldas`, ha nincs eredeti megfelelője; az igén álló névmási ragra a K4/D szerint kötődik), nem kellett javítani; az arany v3 és a `prompt_v3` befagyasztva (`f21p/arany_opus_v3.sha256`, `f21p/prompt_v3.sha256`); (2) a pilot kemény plafonja **4,00 USD**, a megállási küszöb (`plafon_usd`) **3,90** (a PD13 4. pontját és a korábbi 3 USD-s keretet felváltja); (3) sorrend: F3V3 (C, 200 vers) → kalibráló trigger (`SONNETV3`, `koteg_max=1`) → a teljes `SONNETV3`; (4) a kalibrálás után jelentés, de nincs megállás, kivéve ha a modell elutasítja a `reasoning: {enabled: false}` vagy a `temperature: 0` paramétert, vagy a mért köteg-költségből vetített kumulatív összeg 3,90 USD fölött van; (5) P4: a C (F3V3) egyedül, a Sonnet egyedül és a Sonnet + C pár, az öt feltétellel, rétegenként, az arany v3-ra; a v2-es C-futások tájékoztatásul; a (c) hibák újrabesorolása; (6) P5: mindhárom összeállítás a teljes Bibliára, 90%-os intervallummal; (7) a hosszarány definíciója és újraszámolása; (8) megállás a mérés után, a #22 döntése a felhasználóé | a felhasználó döntései (2026.10.01); a B változat a K4-gyel ütközik | az arany v3 B változata; 3 USD-s keret; megállás a kalibrálás után minden esetben |
| PD15 | A Sonnet beállítása (2026.10.01): a kalibráló triggeren (futás 36822937380) az `anthropic/claude-sonnet-5.5` OpenRouter-endpointja a `reasoning: {enabled: false}`-t elutasította (HTTP 400: „Reasoning is mandatory for this endpoint and cannot be disabled.”; `f21p/valaszok/SONNETV3.hibak.jsonl`); a felhasználó döntése: a Sonnet gondolkodása minimális szinten (`reasoning: {max_tokens: 1024}`, az Anthropic minimuma, ha az endpoint elfogadja; különben `effort: "low"`), a `temperature` elhagyva (gondolkodás mellett az Anthropic nem fogad el 0-t), a jelentés jelöli, hogy a Sonnet-futás nem determinisztikus; a dry-run a gondolkodási tokent (hívásonként legfeljebb 1024 token, kimeneti áron) beleszámolja; ha a kumulatív becslés 3,90 USD alatt van, jöhet az új kalibráló trigger, és ha az ellenőrző 0-t ad, a teljes `SONNETV3` megállás nélkül. **Beállítás-eltérés a futások között (a DT21 j) mintájára):** az A és a B gondolkodás nélkül, a C (`kotelezo_effort=minimal`) és a Sonnet (minimális gondolkodási kerettel) gondolkodással fut; a minőség- és költség-összevetésnél ezt jelölni kell | a gondolkodás nem kapcsolható ki az endpointon; a felhasználó jóváhagyta a minimális szintet | Sonnet gondolkodás nélkül (nem lehetséges); másik Sonnet-azonosító; a Sonnet elhagyása |
| PD16 | KJV-mérés a teljes F19-importtal (2026.10.01): (1) az **N29 tárgytalan, az F19 importálta** (`konkordancia/KJV_Strongs_teljes.tsv`); a pilot-brief korábbi, az N29-re hivatkozó mondatai (a Döntési szabály „KJV-import (N29)” bekezdése, a P4 KJV-hatás sora) történeti jelentésűek; a pilot KJV-kérdése innentől: **segít-e a KJV-támpont a párosításban**; (2) **F8V3**: a C (`prompt_v3`, a 200 verses minta) KJV-támponttal minden rétegben az F19-es KJV-táblából; mérés az F3V3-mal szemben rétegenként (pontosság, lefedettség, kapuhiba); az R1-en a különbség kontroll (ott az F3V3-ban is volt KJV, a régi Genesis/Exodus/Proverbs táblából); becslés kb. 0,26–0,30 USD, a 3,90-es küszöbön belül; (3) a szkriptes előpárosításban a KJV-szabály („nincs KJV-tag → `forditatlan`-jelölt”) külön mérve minden rétegben (hány döntést ad, milyen pontossággal); (4) megállás és jelentés | az F19 importálta a teljes KJV-t, így a kérdés nem az import, hanem a haszon | az N29 mint nyitott import-döntés |
| PD17 | A KJV-mérés utáni döntések (2026.10.01): (1) a Károli ↔ KJV versmegfeleltetés zsoltár-eltolódására (zsoltárfeliratok, 1039 ÓSZ-vers, F19-tábla) új tétel a `NYITOTT_FELADATOK.md`-ben (`N-F21`); **most nem javítjuk**, az F8V3 megismétlése a javítás után jön, külön döntéssel; (2) ÚSZ-megfeleltetés: most nem kell; a jelentésben az R4 **„KJV nélkül, nem mérhető”** jelölést kap; (3) **a KJV a promptban: a mérés szerint nincs kimutatható hatás (+0,2 pp, az ingadozáson belül); a pilot döntése: „nem igazolt, a javított táblával újramérhető”**; (4) a Sonnet folytatása a korábbi jóváhagyás szerint (`reasoning: {max_tokens: 1024}`, ha nem fogadja el, `effort: "low"`; `temperature` elhagyva; dry-run; kalibráló trigger; ha az ellenőrző 0-t ad, a teljes `SONNETV3`; 3,90-es küszöb); (5) utána a P4 (a C egyedül a (c) hibák újrabesorolásával, a Sonnet egyedül, a Sonnet + C pár) és a P5; megállás és jelentés | a mérés szerint a KJV-hatás az ingadozáson belül van, és a KJV-támpont a zsoltároknál valószínűleg rossz versről jön | a KJV „igazoltnak” vagy „megcáfoltnak” minősítése a hibás tábla alapján; az F8V3 azonnali újrafuttatása |

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.30 | első változat |
| v1.1 | 2026.09.30 | a P2 ⛔ döntései: a küszöbök rögzítve (PD5); egymodelles összeállítás csak mérésre, a teljes futásra csak A+B vagy A+B+C (PD6); a vegyes példa: R1 és R4 A+B-vel, R2–R3 A+B+C-vel; `[nem TR]` javítás és az „eltérő alak” tokenek kizárása a pontossági mérésből (PD7) |
| v1.2 | 2026.09.30 | a P3/P4 utáni döntések: az A és a B kiesik (a kapun átment versekben is 81%, illetve 65% pontosság), v2 nem lesz hozzájuk, az F4 nem fut (PD8); a régi arany egyezése halmazként mért, a 2 hibás hármas jelölve (PD9); arany v2 csak a jegyzet konvenciójával ütköző esetekre, jóváhagyásig nem fagy be (PD10); KJV (N29): a v1-adaton nem teljesül, n=8, nem végleges |
| v1.3 | 2026.09.30 | a DT21 lezárása visszavonva (DT22): a pilot folytatódik (P3b), minden összeállítás kimérve: F1v2 (A), F2v2 (B), F5v2/F6v2 (KJV nélkül, R1), F3V2b (a C második futása az ingadozáshoz), F4v2 (a C döntőbíróként); a `prompt_v2` és az arany v2 befagyasztva, az öt nyitott kérdés a jelentésbe kerül (PD11) |
| v1.4 | 2026.09.30 | a P3b kész: minden összeállítás kimérve a `prompt_v2`-vel (F1V2, F2V2, F5V2, F6V2, F3V2b, F4V2, 1,605 USD kumulatív); az A+B és az A+B+C sem felel meg; a C két futásának eltérése az ingadozás becslése; a #22 sorsa a felhasználó döntése |
| v1.5 | 2026.09.30 | a DT21 döntései (PD12): a mért régi arany érték a kizárás nélküli (C: 93,8%), a kizárás csak tájékoztatás, az 1Móz 13:4 „hibás” jelölése visszavonva (csak az 1Móz 6:17 marad); a P5 rétegbesorolása az F22 brief szerinti, műfaji (Préd, Sir → költészet, Dán → próféta, Ruth, Eszt → ÓSZ-próza); a köteg mint bootstrap-egység elfogadva; a konzervatívabb (leave-one-out) költség-ellenőrzés számít; az a–e tételek regressziós mérésre átvéve; a #22 döntése elhalasztva |
| v1.6 | 2026.09.30 | regressziós mérés (P3c, új ág a PR #92 merge után): az a–e tételek a jegyzet v2-be, `prompt_v3`, F3V3 (C) és a Sonnet az OpenRouteren (`prompt_v3`, 200 vers), P4/P5 a Sonnetre és a Sonnet + C párra; az arany v3 csak versenkénti diff és jóváhagyás után fagy be; az Opus nem fut (PD13) |
| v1.7 | 2026.10.01 | a regressziós mérés döntései (PD14): az arany v3 az A változat (3 link, 1048), a B elutasítva (K4-ütközés), az arany v3 és a `prompt_v3` befagyasztva (sha256); a pilot kemény plafonja 4,00 USD, a megállási küszöb (`plafon_usd`) 3,90; sorrend: F3V3 (C) → kalibráló `SONNETV3` (`koteg_max=1`) → a teljes `SONNETV3`; megállás a kalibrálás után csak ha a modell elutasítja a `reasoning: {enabled: false}` vagy a `temperature: 0` paramétert, vagy a mért köteg-költségből vetített kumulatív összeg 3,90 USD fölött van |
| v1.8 | 2026.10.01 | a Sonnet beállítása (PD15): az `anthropic/claude-sonnet-5.5` endpoint a gondolkodás kikapcsolását elutasította (HTTP 400), a Sonnet minimális gondolkodási kerettel fut (`reasoning: {max_tokens: 1024}`, ha elutasított: `effort: "low"`), a `temperature` elhagyva (a Sonnet-futás nem determinisztikus); a beállítás-eltérés (A és B gondolkodás nélkül, C és Sonnet minimális gondolkodással) rögzítve |
| v1.9 | 2026.10.01 | a KJV-mérés a teljes F19-importtal (PD16): az N29 (a KJV-import kérdése) tárgytalan, az F19 importálta; a pilot KJV-kérdése innentől: segít-e a KJV-támpont a párosításban (F8V3 az F3V3-mal szemben, rétegenként; a szkriptes előpárosításban a KJV-szabály külön mérve) |
| v1.10 | 2026.10.01 | a KJV-mérés utáni döntések (PD17): zsoltár-eltolódás új tétel (`N-F21`), nem javítva; ÚSZ-megfeleltetés most nem; az R4 „KJV nélkül, nem mérhető”; a KJV a promptban: „nem igazolt, a javított táblával újramérhető”; a Sonnet folytatása a jóváhagyott beállítással |
