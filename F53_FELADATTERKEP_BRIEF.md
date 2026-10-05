---
feladat: 53
cim: Feladattérkép — a feladatok, döntések és a munkaterv generált vizuális áttekintése
kod: FELADATTERKEP
tipus: feladat
fazis: folyamat
modell: sonnet
munka: folyamat
allapot: megallt
ad: "a FELADATTERKEP.html (gyökér, mindig ugyanazon a néven felülírva) és a feladatterkep.json minden main-merge után a forrásokból generálódik; a claude.ai-artifact megnyitáskor a files képességgel ugyanezt a JSON-t olvassa, így újrafeltöltés nélkül friss"
kovetkezo: Te: a draft PR és a független ellenőrzés átnézése; döntés, hogy az FT.7 az FT.5-tel együtt halasztódik-e (az FT.5 halasztva, N-F53f: nincs chan_… azonosító); merge után az Action-próba (7.6)
olvas: ["F*_BRIEF.md", MUNKATERV.md, eszkozok/feladatok.py, .github/workflows/feladatok.yml, FELADATTERKEP.html]
ir: [eszkozok/feladatterkep.py, eszkozok/feladatterkep_kartyak.tsv, eszkozok/teszt_feladatterkep.py, FELADATTERKEP.html, feladatterkep.json, .github/workflows/feladatok.yml, eszkozok/main_frissit.py]
fugg: []
ag: claude/f53-feladatterkep
nem_fugg: [52]
helyi_gep: nem
---

# F53_FELADATTERKEP_BRIEF.md — Feladattérkép: generált vizuális áttekintés

*FELADATOK #53 · Modell: sonnet · v1.1 · 2026.10.05 (v1.1: FT.7, helyi `main`-frissítés)*

*Előzmény: a 2026-10-05-i chat-session kézzel épített egy áttekintő lapot
(`FELADATTERKEP.html`, a gyökérben) és egy claude.ai-artifactot
(https://claude.ai/artifact/Dwnq3JtHgmgPiwDPaUnJzx, 8. verzió). Mindkettő
pillanatkép: az adatok kézzel vannak a fájlba írva. Ez a brief a kettőt
generált kimenetté teszi. A kézi lap a kinézet mintája; az adat nem onnan,
hanem a forrásokból jön.*

## 1. Cél

Egy lap, amely egy pillantással megmutatja, **mi áll, mi fut, mi indítható,
mire vár, és mit kell eldöntened**:

- összkép-csempék (megállt / fut / indítható / függésre vár / felvehető / nyitott döntés);
- „Most induló sor”;
- a MUNKATERV hullámai, a ⛔ feltétellel;
- feladat-oszlopok állapot szerint, fázisszűrővel; minden kártyán: cím, szám vagy
  kódnév, fázis, **részletes leírás (2–3 mondat)**, „Most:” (következő lépés),
  „függ:”, és a végén **„Röviden:” egymondatos, közérthető összefoglaló**;
- függési térkép (Mermaid), a döntések hatszögként;
- döntések: nyitott · eldöntve, alkalmazásra vár · javasolt, még nincs felvéve.

A lap **generált kimenet** (CLAUDE.md rétegszabály): kézzel nem szerkeszthető, a
forrás javul, és újragenerálódik.

## 2. Hatókör

**Benne van**

1. `eszkozok/feladatterkep.py` — a generátor. Két kimenet, egy futásból:
   - `feladatterkep.json` (gyökér): a lap összes adata, kinézet nélkül;
   - `FELADATTERKEP.html` (gyökér): önálló lap, a JSON beágyazva.
   Mindkettő **mindig ugyanazon a néven íródik felül** (felhasználói kérés,
   2026-10-05); dátum vagy commit a fájlnévben nincs, csak a fájlon belül.
2. `eszkozok/feladatterkep_kartyak.tsv` — kézi tábla a kártyaszövegekhez
   (`kod`, `reszletes`, `roviden`, `forras`). Ez az egyetlen kézzel írt bemenet;
   a kezdő tartalma a mai kézi lap 31 kártyájának szövege.
3. `eszkozok/teszt_feladatterkep.py` — tesztek (l. 4. pont).
4. `.github/workflows/feladatok.yml` bővítése: a `general` után a generátor is
   fut, és a két kimenet ugyanabba a gépi commitba kerül.
5. Az artifact-változat (`--cel artifact`, a repón **kívüli** ideiglenes
   könyvtárba) és egyszeri feltöltése ugyanarra a linkre a `files` képességgel.

**Nincs benne**

- a FELADATOK.md generált blokkjainak módosítása; a `feladatok.py` logikájának
  átírása (csak a függvényeit hívja);
- tartalmi döntés: a „Most induló sor” sorrendje és a hullám-besorolás a
  MUNKATERV-ből jön, a generátor nem talál ki sorrendet;
- ütemezett artifact-újrafeltöltés (a `files`-olvasás teszi fölöslegessé; a
  helyi munkapéldány frissen tartása az FT.7 dolga);
- a `generalt_proba/` könyvtár (nem érinti).

## 3. Bemenetek és levezetés

| lap-elem | forrás | hogyan |
|---|---|---|
| feladat, állapot, következő lépés, „Mit ad” | brief-fejlécek | `feladatok.py`: `briefek_beolvas`, `main_allapotok`, `statusz` — ugyanaz, amiből a FELADATOK.md generálódik |
| függés | brief-fejlécek | `feladatok.py`: `fuggesek` (kézi + levezetett), a kész feladatok nélkül |
| tervezett feladatok (kódnévvel) | `MUNKATERV.md` 4. szakasz, „—” számú sorok | táblasor-olvasás `split('|')`-szel; ha a kód már a FELADATOK-ban van, a FELADATOK-sor nyer |
| hullámok, ⛔ | `MUNKATERV.md` 5. szakasz | táblasor-olvasás |
| javasolt DT-k | `MUNKATERV.md` 2. szakasz | csak azok, amelyek nincsenek a `DONTESEK.md`-ben |
| nyitott / alkalmazásra váró döntések | `DONTESEK.md` | állapot-oszlop: 🟡 vagy „nyitott” = nyitott; 🟢 = alkalmazásra vár; ✅ = kimarad. **A mezők szabad szövegében `|` is előfordul** (pl. DT19, DT-F46): a generátor az állapotot az ismert jelek alapján keresi, és ha egy sor oszlopszáma eltér a fejlécétől, a sort `ellenőrizendő` jelöléssel mutatja, nem találgat |
| kártyaszöveg | `eszkozok/feladatterkep_kartyak.tsv` | kódnév szerint; **ha nincs sor, a kártya megjelenik „nincs leírás” jelöléssel** — a hiányt nem tölti ki semmivel (CLAUDE.md 3. szabály) |
| állapot-bélyeg | git | a források utolsó változásának dátuma és commitja (`git log -1 -- <források>`), **nem a HEAD és nem a futás ideje** — így azonos bemenetre a kimenet bájtazonos, és nincs fölösleges gépi commit |

TSV-olvasás `split('\t')`, írás `'\t'.join()`; a `csv` modul tilos (CLAUDE.md).
A szkript a docstring és az importok után ráteszi magára az UTF-8 stdout-wrappert.

## 4. A kinézet — a mai kézi lap tanulságai (kötelező)

A 2026-10-05-i session ezeket próbálta ki; a generátor ezeket követi:

1. **Téma.** A lap saját jelölőt használ (`data-tema`), **nem** a `data-theme`-et:
   azt a claude.ai és a beépített előnézet felülírja. Kapcsoló jobb fent
   (☀ Világos / ☾ Sötét), **újratöltés nélkül** vált (helyi fájlnál a
   böngészőtárhely nem mindig elérhető). Repóbeli HTML: alapból sötét.
   Artifact: alapból a claude.ai témáját veszi át.
2. **Színek.** Telített állapotszínek (piros megállt, zöld fut, kék indítható,
   sárga vár, lila szaggatott tervezett, szürke halasztott, narancs hatszög
   döntés); a kártyák tónusos háttérrel, az oszlopfejek színes sávval.
3. **Mermaid, repóbeli HTML.** Külső Mermaid 11.16.1 (jsdelivr), kézi rajzolás,
   témaváltáskor újrarajzol; betűméret 10 px; a lap többi része 10%-kal nagyobb
   (`.wrap{zoom:1.1}`).
4. **Mermaid, artifact.** A claude.ai **saját** rajzolója (`<pre class="mermaid">`,
   külső könyvtár nélkül — a külső könyvtár a keretben nem fut le). **Az SVG
   méretét nem szabad felülírni** (a 2240×1600 px-es térképből különben csak egy
   csomópont látszik). Nagyítás: − / + / Illesztés gombok, amelyek a tárolót
   szélesítik (`.mermaid-diagram{width:calc(var(--nagyitas,1)*100%)}`), 100–300%.
   A témaváltó a `data-theme`-et is állítja, hogy a rajzoló újrarajzoljon.
5. **Szöveg.** Magyar, közérthető; a kártya végén „Röviden:”.

## 5. Az artifact: `files`-olvasás

Az artifact megnyitáskor a `files` képességgel a repó `feladatterkep.json`-ját
olvassa, és abból rajzol; a feltöltéskor beágyazott pillanatkép a tartalék
(ha a `files` `null`, vagy az olvasás hibát ad). A lap jelzi, melyiket mutatja:
„élő adat, <bélyeg>” vagy „pillanatkép, <bélyeg>”.

Tudnivalók, amelyeket a lap láblécében is ki kell írni:

- a `files` a **helyi munkapéldányt** olvassa, nem a GitHubot: ha a helyi `main`
  nincs frissítve, a régebbi állapot látszik (`git pull` után friss);
- csak a projekt tagjai látják az élő adatot; mindenki más a pillanatképet;
- az első megnyitáskor egyszer engedélyt kér.

A `files` deklarálásához a projekt azonosítója (`chan_…`) kell. Ha a session
nem tudja megállapítani, **⛔** (l. 6.).

Az artifact kinézete csak akkor töltendő fel újra, ha a generátor sablonja
változik; az adat frissítéséhez nem kell feltöltés.

## 6. Lépések (⛔ a kötelező megállások)

1. **FT.0** — a `feladatterkep_kartyak.tsv` létrehozása a mai kézi lap 31
   kártyájának szövegéből (`forras` oszlop: `kezi-2026-10-05`); a tábla
   fejlécének és oszlopainak leírása a brief 8. pontjába.
2. **FT.1** — a generátor, csak JSON-kimenettel; tesztek (l. 7.).
3. **FT.2** — HTML-kimenet a mai `FELADATTERKEP.html` kinézetével.
   **Kis minta:** a generált lap a repón kívüli ideiglenes könyvtárba; összevetés
   a mai kézi lappal: a csempék számai, az oszlopok kártyái, a döntéslisták és a
   térkép csomópontjai. Minden eltérés egy sor a naplóban: *a kézi lap tévedett*
   vagy *a generátor téved*. **⛔ a felhasználó átnézi.**
4. **FT.3** — a `FELADATTERKEP.html` és a `feladatterkep.json` felülírása a
   generált változattal; a kézi lap fejléc-megjegyzése helyére
   `<!-- GENERÁLT: eszkozok/feladatterkep.py — kézzel ne szerkeszd -->`.
5. **FT.4** — **⛔ a workflow módosítása előtt**: a `feladatok.yml` diffje a
   felhasználónak. Jóváhagyás után: a `general` lépés után
   `python eszkozok/feladatterkep.py`, és a gépi commit a két fájlt is
   hozzáadja (`git add FELADATOK.md FELADATTERKEP.html feladatterkep.json`).
   Az üzenet változatlan logikájú (`… frissítés (gép)`).
6. **FT.5** — artifact-változat (`--cel artifact`, ideiglenes könyvtár, a repón
   kívül), a projekt-azonosító megállapítása, feltöltés ugyanarra a linkre
   `capabilities: {files: {project: "chan_…"}}`-val. **⛔ ha az azonosító nem
   kapható meg, vagy a `files`-olvasás nem működik**: a naplóba, mi történt; az
   artifact a beágyazott pillanatképpel marad, frissítés kérésre.
7. **FT.6** — napló, draft PR, `fuggetlen-ellenor`; N-tétel a
   `NYITOTT_FELADATOK.md`-be a CI-védelemről (8.1).
8. **FT.7** — helyi `main`-frissítés, hogy az artifact `files`-olvasása friss
   JSON-t lásson (a `files` a helyi munkapéldányt olvassa, az Action viszont a
   GitHubon frissít).
   - `eszkozok/main_frissit.py`: `git fetch`, majd `git pull --ff-only` a
     `main`-en — **csak akkor**, ha (a) a kiválasztott ág a `main`, (b) a
     munkakönyvtár tiszta (`git status --porcelain` üres, a követetlen fájlokat
     nem számítva), (c) a fast-forward lehetséges. Bármelyik feltétel hiányában
     nem nyúl semmihez, és egy sort ír a kimenetre, miért hagyta ki. Nem
     commitol, nem pushol, nem vált ágat, nem stashel. UTF-8 wrapper az
     importok után (CLAUDE.md).
   - Teszt a `teszt_feladatterkep.py`-ban: másik ágon, piszkos munkakönyvtárral
     és nem fast-forward helyzetben a szkript nem változtat semmit.
   - Ütemezés **terve** a naplóba: **Claude-os helyi ütemezett feladat**, hogy
     a Claude alkalmazás **Routines** listájában látsszon (felhasználói kérés,
     2026-10-05), a #51 `konzisztencia-napi` feladata mellett. Javasolt név:
     `main-frissites-napi`; naponta egyszer, csak ha a gép be van kapcsolva (a
     kimaradt futás a következő bekapcsoláskor pótlódik); a repó gyökeréből a
     `python eszkozok/main_frissit.py`-t futtatja, és a kimenetét egy sorban
     jelenti. Modell: a legolcsóbb elérhető (haiku) — a feladat egyetlen
     parancs, értelmező munka nincs benne. Költség: futásonként egy rövid
     session; ezt a naplóban becsülni kell.
   - A Windows Feladatütemező **nem** használandó (a felhasználó a Claude
     Routines alatt akarja látni és kezelni).
   - **⛔ az ütemezett feladat létrehozása előtt:** a felhasználó jóváhagyja a
     tervet (időpont, mód), és a létrehozás külön lépésben történik (a #51 K5
     mintája). A brief végrehajtója magától nem hoz létre ütemezett feladatot.

Commitok tétel-szinten (`FT.0: …`, `FT.1: …`), az üzenet UTF-8 fájlból.

## 7. Elfogadási feltételek

1. **Idempotens:** két egymás utáni futás bájtazonos kimenetet ad; a kimenetben
   nincs futási időbélyeg.
2. **Teljes:** a FELADATOK.md minden nyitott sora megjelenik kártyaként, azonos
   állapottal; a `DONTESEK.md` minden nem ✅ tétele megjelenik a döntéseknél.
3. **Nem pótol:** kártyaszöveg nélküli feladat „nincs leírás” jelöléssel jelenik
   meg; egy oszlopszám-eltérő DONTESEK-sor `ellenőrizendő` jelöléssel.
4. **TSV-szabály:** a `csv` modul nincs importálva; a teszt ezt ellenőrzi.
5. **A kis minta eltéréslistája** átnézve és jóváhagyva (FT.2 ⛔).
6. **Action:** egy `main`-re futó próba után a gépi commit a három fájlt
   tartalmazza, és változatlan forrásnál nem keletkezik commit.
7. **Artifact:** a lap jelzi, élő adatot vagy pillanatképet mutat; a térkép
   alapállásban a dobozba illesztve látszik; a nagyítás és a témaváltó működik.
   (Vagy: FT.5 ⛔ dokumentálva.)
8. `python eszkozok/feladatok.py ellenoriz` 0.
9. **FT.7:** a `main_frissit.py` tesztje zöld (másik ág, piszkos munkakönyvtár,
   nem fast-forward → nincs változás); az ütemezés terve a naplóban, és a
   létrehozása a felhasználó jóváhagyásával dokumentálva (vagy ⛔-ban áll).

## 8. Eldöntött kérdések

1. **CI-védelem:** a `FELADATTERKEP.html` és a `feladatterkep.json` kap
   E18-hoz hasonló védelmet (PR ne szerkeszthesse, csak az Action), de **nem
   ebben a menetben**: külön ágon (D6), mert az `eszkozok/ellenorzes/szabalyok.py`-t
   a #30, #37, #40 és #51 is írja. A menet végén N-tételként felveendő.
2. **„Most induló sor”:** a `python eszkozok/feladatok.py jeloltek` kimenete —
   ugyanaz a lista, amelyből a `/kovetkezo` választ. A chatben született
   2026-10-05-i sorrend nem kerül át. A tervezett, még fel nem vett feladatok a
   hullámoknál és a „Tervezett” oszlopban látszanak.
3. **A kártyaszöveg-tábla helye:** `eszkozok/feladatterkep_kartyak.tsv`
   (folyamat-konfiguráció, nem kutatási adat; SEMA-bejegyzés nem kell).
4. **A `feladatterkep_kartyak.tsv` leírása (FT.0).** Tabulátorral tagolt, UTF-8,
   LF; az első sor a fejléc, utána soronként egy kártya; olvasása `split('	')`,
   írása `'	'.join()` (a mezők nem tartalmaznak tabot és sortörést).

   | oszlop | tartalom |
   |---|---|
   | `kod` | a kártya kulcsa: a brief `kod:` mezője; ha a briefnek nincs `kod`-ja, `#<szám>` (pl. `#7`); még fel nem vett (MUNKATERV-beli) feladatnál a MUNKATERV kódneve. A `SZOTAR S2` kulcsban szóköz van, mert a #9 `kod`-ja is ilyen |
   | `reszletes` | a részletes leírás, 2–3 mondat |
   | `roviden` | a „Röviden:” egymondatos, közérthető összefoglaló |
   | `forras` | honnan származik a szöveg: `kezi-2026-10-05` (a kézi lap 31 kártyája); később `kezi-<dátum>` vagy a szerző jelölése |

   A generátor a táblát csak olvassa. Sor nélküli kártya „nincs leírás”
   jelöléssel jelenik meg; kártya nélküli sor (pl. kész feladat) a JSON
   `kartya_tabla.felhasznalatlan` listájába kerül, de nem hiba. A kezdő
   tartalom a kézi lap 31 kártyájának szövege **változtatás nélkül**; azok a
   kódok, amelyeknél a kézi lap kódneve eltért a brief `kod`-jától (a #22
   `KAROLI_STRONG` helyett `F22`), a brief `kod`-ját kapták.

## 9. Döntésnapló

| dátum | döntés | forrás |
|---|---|---|
| 2026-10-05 | a repóbeli lap mindig ugyanazon a néven íródik felül (`FELADATTERKEP.html`, gyökér) | felhasználó, chat |
| 2026-10-05 | az artifact a `files` képességgel olvassa a repó JSON-ját; tartalék a beágyazott pillanatkép | felhasználó, chat |
| 2026-10-05 | a kártyákon részletes leírás + „Röviden:” egymondatos összefoglaló | felhasználó, chat |
| 2026-10-05 | CI-védelem igen, de külön ágon, későbbi N-tételként (8.1) | felhasználó, chat |
| 2026-10-05 | a „Most induló sor” forrása a `feladatok.py jeloltek` (8.2) | felhasználó, chat |
| 2026-10-05 | a kártyaszöveg-tábla az `eszkozok/`-ban (8.3) | felhasználó, chat |
| 2026-10-05 | v1.1: FT.7 — időzített helyi `main`-frissítés (ff-only, csak tiszta `main`-en), hogy az artifact friss JSON-t lásson; létrehozás ⛔ után | felhasználó, chat |
| 2026-10-05 | az FT.7 ütemezése Claude-os helyi ütemezett feladat (Routines alatt látható), nem Windows Feladatütemező; modell: haiku | felhasználó, chat |
| 2026-10-05 | FT.2 ⛔: a kis minta jóváhagyva; az öt kérdésre adott válasz és az N-F53a–d a `naplok/F53_kis_minta_eltereslista.md` végén; a lap három kisebb hibája (N-F53c) és a kártyaszöveg-piszkozat (N-F53d) nem az FT.3 része; a main az FT.3 előtt behúzva | felhasználó, chat |
| 2026-10-05 | FT.4: a `feladatok.yml`-diff jóváhagyva, változtatás nélkül; a #56-nál a `#57*` rendben (a MUNKATERV-hiány a #52 naplójában, PR #200); a CI-őr N-F53e | felhasználó, chat |
| 2026-10-05 | FT.5 halasztva (c): az artifact a kézi 8. verzión marad, amíg a `chan_…` azonosító nincs meg (N-F53f); az FT.7 nem indul, a halasztásáról a felhasználó dönt | felhasználó, chat |
