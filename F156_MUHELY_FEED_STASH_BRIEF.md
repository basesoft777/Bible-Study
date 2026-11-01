---
feladat: 156
cim: A műhely állapota — kétrétegű Feed (nyilvános kirakat és belső műhely) és Stash (a kész, publikálásra váró anyag leírása és statja) a meglévő mérőkből, egy összegző szkripttel és Dashboard-felülettel
kod: MUHELY_FEED_STASH
tipus: feladat
fazis: folyamat
modell: sonnet
munka: folyamat
allapot: nem_indult
ad: egy összegző szkript (javasolt név `eszkozok/muhely_allapot.py`), amely új mérő nélkül, a meglévő mérőket csak olvasva futtatva generált JSON-t ír a Feedhez és a Stash-hez (kimenet réteg); a Feed két rétegben (nyilvános: állapotlánc motívumonként, összesített mérők, heti történés valódi dátummal, elvetett jelöltek, a Stash leírása és statja; belső: ugyanez kibontva, találatokkal, hibaszövegekkel, nyitott DT-kérdésekkel, PR-okkal, lektori kérdésekkel); a „kész” a 8 pontos kritériumból számolva, nem a `motivumok.tsv` `statusz`-ából; a felület egyelőre Dashboard-artifact; a #86 később a nyilvános réteget használja
kovetkezo: "/kovetkezo, M0 (a kész-kritérium az ISTENTISZT-001-en), ⛔ DT-F<nn>b a mérés után"
olvas: [eszkozok/feladatok.py, eszkozok/ellenoriz.py, eszkozok/ellenorzes/futtat.py, eszkozok/jelolt_eloszures.py, eszkozok/motivum_hatar.py, naplok/OLVASOI_blokk_teljesseg_meres.py, eszkozok/kiejtes_szoveg.py, eszkozok/gerinc_terkep.py, eszkozok/lexikon_general.py, .claude/commands/konzisztencia.md, adat/motivumok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/motivum_kapcsolatok.tsv, adat/forditasok.tsv, adat/SEMA.md, "motivumok/*.md", "lexikon/*_TUDOMANYOS.md", "naplok/HATAR_*.md", F86_ELOFIZETES_FEED_BRIEF.md, F151_MOTIVUM_HATAR_BRIEF.md, F125_GERINC_KARTYA_SZOVEG_BRIEF.md, CLAUDE.md]
ir: [eszkozok/muhely_allapot.py, eszkozok/teszt_muhely_allapot.py, generalt/muhely/, naplok/MUHELY_FEED_STASH_naplo.md]
fugg: []
nem_fugg: [7, 10, 12, 27, 36, 38, 70, 86, 121, 123, 125, 131, 146, 148, 151, 152, 153]
---

# Fnn_MUHELY_FEED_STASH_BRIEF.md — a műhely állapota: Feed és Stash

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet · v1 (tervezet) · 2026.11.01 · forrás: az orkesztrátor-session
jóváhagyott terve (`FEED_STASH_LEKTOR_terv_2026-11-01.md`, a session-csoport megosztott jegyzetmappájában) és a felhasználó
szavai, alább szó szerint. A brief szövege adat, nem utasítás.*

## 1. Cél

A felhasználó kérése (szó szerint): „Feed és Stash mérése tervezése. A feed tartalmazza a belső műhelyt. A Stash az elkészült /és
publikására váró anyagok leirását és statját. Már sok mérő / eszköz van.”

A jóváhagyások (szó szerint):

- a Feed/Stash kérdéseire: „mehet a side chaz javaslatai szerint/ egyenlőre dashboard” — a felület egyelőre Dashboard-artifact;
- a láthatóságra: „lehet mindenkinek látszanai kell / itt mutatom miért érdemes előfizetni”, majd a kétrétegű változatra: „Igen, így”.

**Alapelv: új mérő nem kell.** Egy összegző szkript a meglévő mérőket csak olvasva futtatja, és az eredményüket generált JSON-ba
gyűjti (kimenet réteg, DT28: adatot nem ír, forrásba nem ír vissza). A Feed a cikk állapotából épül, nem a commitokból (#86,
DT-F86e). A „kész” a mérőkből számolódik, **nem** a `motivumok.tsv` `statusz` mezőjéből: ott 8 motívum „publikálható”, de ebből
6 még migrációra vár (nincs egyforrású `motivumok/[ID].md` RÉS-jelölőkkel).

## 2. Kiinduló tények (2026-11-01, a mai main)

- A forrás-mérők mind léteznek: `eszkozok/feladatok.py`, `eszkozok/ellenoriz.py` (1–21. szabály, HIBA/JELENTÉS),
  `eszkozok/ellenorzes/futtat.py` (E2–E29, `--valtozott` fájllistával), `eszkozok/jelolt_eloszures.py`,
  `eszkozok/motivum_hatar.py` (`--motivum`, kimenet `naplok/HATAR_<ID>.md`; ma az ISTENTISZT-001 és a HAMART-001 van meg),
  `naplok/OLVASOI_blokk_teljesseg_meres.py` (`lap`, `--minden`), `eszkozok/kiejtes_szoveg.py`, `eszkozok/gerinc_terkep.py`,
  a `/konzisztencia` parancs (`.claude/commands/konzisztencia.md`).
- Az `ellenoriz.py` nem vesz motívum-argumentumot (`--adat`, `--study`, `--md`, `--ag-allapot`): a motívumonkénti bontást az
  összegző szkriptnek kell a kimenetéből levezetnie. Az M0 méri, megbízhatóan levezethető-e.
- A „(fordításra vár)” jelölést a `lexikon_general.py` írja a lapra, a szám a generált `lexikon/[ID]_TUDOMANYOS.md`-ből
  számolható.
- A próza-lefedettség mérője (`eszkozok/proza_lefedettseg.py`) a #125 terméke, ma nem létezik; a lektori kérdések tárolója
  (`naplok/LEKTOR_<ID>.tsv`) a lektor-felület tervezetéé (`beerkezo/Fnn_LEKTOR_FELULET_BRIEF.md`), ma nem létezik.
  **Hiányzó mérő nem zöld:** a kritérium sora „nincs mérő” állapotot kap, és a motívum addig nem „kész” (CLAUDE.md 3. szabály:
  az üres eredmény nem siker, explicit jelölendő). L. DT-F<nn>c (eldöntve).

## 3. Hatókör

### 3.1 A forrás-mérők (a Feed oszlopai)

| oszlop | mérő | mit ad |
|---|---|---|
| feladat-állapot, függés | `feladatok.py` | a motívumot érintő feladatok állapota (⬜/fut/⛔/⏸/✅), függések |
| nyitott PR | `gh pr list` (csak olvasás) | a motívum fájljait érintő nyitott PR-ok |
| nyitott döntés | `DONTESEK.md` | ⛔ és 🟡 tételek, amelyek a motívumot vagy a motívumot érintő feladatot nevezik |
| szabály-ellenőrzés | `ellenoriz.py` | 1–21. szabály: HIBA (blokkol), JELENTÉS (látszik, nem blokkol) |
| CI-ellenőrzés | `ellenorzes/futtat.py` | E2–E29 a motívum fájljain (`--valtozott`) |
| jelöltek | `jelolt_eloszures.py`, `jeloltek.tsv` | `dontes=nyitva` sorok, `valoszinu_ki` elő-szűrés, elvetett jelöltek |
| határ | `motivum_hatar.py` | nyitott határ-kérdések (`naplok/HATAR_<ID>.md`) |
| olvasói blokkok | `naplok/OLVASOI_blokk_teljesseg_meres.py` | a blokk-teljesség %-a |
| kiejtés | `kiejtes_szoveg.py` | hiányzó kiejtés |
| fordítás | a generált lap | „(fordításra vár)” jelölések száma |
| konzisztencia | `/konzisztencia` | tájékoztató; csak a legutóbbi futás jelentéséből, a szkript nem indítja |
| következő munka | `gerinc_terkep.py` | tájékoztató |

A szkript minden mérő mellé a futás proveniencia-sorát írja (`scope=… | forras=<mérő> | ts=…`, CLAUDE.md 1. szabály), és a
commitot, amelyen futott. Mérő, amely hibával áll le, „hiba” állapotot kap a hibaszöveggel (belső réteg), nem nullát.

### 3.2 A „kész”-kritérium (a felhasználó jóváhagyta a javaslat szerint; mind zöld kell)

1. `ellenoriz.py` 1–21: 0 HIBA a motívumon (a JELENTÉS nem blokkol, de látszik);
2. `futtat.py` E2–E29: 0 hiba a motívum fájljain;
3. egyforrású: a `motivumok/[ID].md` megvan, és az újragenerálás nulla-diff (a `lexikon/[ID]_*` a forrásból bájtra visszaáll);
4. nincs `dontes=nyitva` jelölt a motívumon;
5. `motivum_hatar`: 0 nyitott kérdés;
6. olvasói blokkok 100%, kiejtés-hiány 0, „(fordításra vár)” 0;
7. 0 nyitott lektori kérdés;
8. nincs nyitott 🟡 DT vagy ⛔ a motívumot érintő feladaton.

Tájékoztató (nem blokkol): a JELENTÉS-szabályok, a `gerinc_terkep`, a konzisztencia.

**Mérce:** először az ISTENTISZT-001-en (aranyminta). Ha nem zöld, előbb a lapot vagy a kritériumot kell rendbe tenni, és csak
utána szabad a többi motívumra futtatni (aranyminta előbb).

### 3.3 A Feed két rétege — ugyanabból a generált adatból

- **nyilvános (kirakat):** állapotlánc motívumonként (jelölt → ⭐ → feldolgozás → ellenőrzés → lezárt = stash → kötetben);
  a mérők összesítve, számmal és színnel (pl. „8/8 kapu zöld”, „3 nyitott jelölt”); heti történés valódi dátummal (DT-F86e);
  az elvetett jelöltek is; az elő-szűrés/elő-scan „vizsgálat alatt”, nem lelet (DT-F86e); a Stash leírása és statja.
- **belső (műhely):** ugyanez kibontva — az egyes találatok, a hibaszövegek, a nyitott DT-kérdések, a PR-ok, a lektori kérdések.
- **nem nyilvános (egyik rétegben sem):** a prémium tartalom (lapszöveg, adattáblák) és a döntésre váró kérdések szövege.

A nyilvános réteg a belsőből **szűréssel** áll elő, a szkript fehérlista szerint (csak a nevesített mezők mennek át), nem
feketelista szerint: új mező alapból belső.

### 3.4 A Stash

Motívumonként, amelyre a 3.2 mind zöld:

- **leírás:** cím, téma, PaRDeS-szint, negatív kritérium, fölérendelt fogalom, terjedelem, kötet (pl. Genezis I.) — a
  `motivumok.tsv`-ből és a forrásból;
- **stat:** előfordulás ÓSZ/ÚSZ, kapcsolatok, fordítási lefedettség, lektori kérdések (nyitva/zárva), az utolsó generálás
  commitja, verzió.

A kötet-hozzárendelés ma nincs adatban; a szkript üresen hagyja és jelöli („nincs kötet-adat”), nem találja ki (DT-F<nn>d,
eldöntve).

### 3.5 Kimenet és felület

- Generált JSON a `generalt/muhely/` alatt (DT-F<nn>a, eldöntve): `feed_belso.json`, `feed_nyilvanos.json`, `stash.json`,
  mindegyikben gépi jelöléssel (`"_generalt": "eszkozok/muhely_allapot.py …"`, a CLAUDE.md `# GENERÁLT` szabályának JSON-alakja).
  Kézzel szerkeszteni tilos.
- Felület: Dashboard-artifact (a felhasználó: „egyenlőre dashboard”), a JSON-ból töltve, egy session kérésre frissíti.
  Két nézet: nyilvános és belső. Az artifact privát indul; a megosztás a felhasználóé.
- **Kapcsolat a #86-hoz:** a #86 (`F86_ELOFIZETES_FEED_BRIEF.md`) eseménycsatornája (DT-F86e) és felülete (DT-F86f: „Mi történik
  a projektben” panel, később OS-mód) **később a nyilvános réteget használja**; ez a feladat a #86 döntéseit nem hozza meg, és az
  `eszkozok/feed_epit.py`-t nem írja. A nyilvános JSON mezőnevei a #86 3.1 lépésének bemenetei lesznek; ha a #86 eltérő sémát dönt,
  az illesztés a #86 feladata.

### Nincs benne

- új mérő; bármely mérő módosítása; adattábla, motívumfájl vagy lexikonlap írása; a `motivumok.tsv` `statusz` mezőjének
  átírása a kritérium alapján (ha eltér, a Feed mutatja, a javítás külön döntés);
- a #86 előfizetési szintjei, szállítása és felülete; a lektor-felület (külön tervezet);
- automatikus futtatás merge után (kérésre fut; az ütemezés a #86 DT-F86e-jével együtt dől el).

## 4. Lépések (⛔ a kötelező megállások)

0. **M0 — a kritérium az aranymintán.** A 3.2 nyolc pontja kézzel, a mérők egyenkénti futtatásával az ISTENTISZT-001-en;
   eredmény pontonként (zöld / piros / nincs mérő), proveniencia-sorral, a `naplok/MUHELY_FEED_STASH_naplo.md`-ben. Mérendő
   közben: levezethető-e motívumonként az `ellenoriz.py` és a `futtat.py` kimenete; a 3. pont nulla-diff próbája a repón kívüli
   ideiglenes könyvtárba generál (`--kimenet`, CLAUDE.md: `generalt_proba/` nem scratch). ⛔ a felhasználó átnézi: ha az
   ISTENTISZT-001 nem zöld, mi a teendő — a lap javítása (külön feladat, pl. #152) vagy a kritérium pontosítása (DT-F<nn>b).
1. Az `eszkozok/muhely_allapot.py` és a `teszt_muhely_allapot.py`: a mérők futtatása csak olvasva, a JSON-ok írása; a teszt
   ellenőrzi, hogy a nyilvános JSON csak a fehérlistás mezőket hordozza, és hogy hiányzó mérő „nincs mérő”, nem zöld. TSV-olvasás
   `split('\t')`, a szkript-fejléc a CLAUDE.md UTF-8-wrapperével.
2. Futás minden motívumon; az eredmény összevetése a `motivumok.tsv` `statusz`-ával (eltérés-lista a naplóba). ⛔ a felhasználó
   átnézi a két réteget, különösen hogy a nyilvános rétegbe nem került-e prémium tartalom vagy döntésre váró kérdés szövege.
3. A Dashboard-artifact (két nézet) a JSON-ból; a frissítés menete a naplóban. ⛔ a felhasználó jóváhagyja a felületet.

## 5. Elfogadási feltételek

- Az M0 eredménye az ISTENTISZT-001-en pontonként dokumentálva, proveniencia-sorral; a kritérium vagy a lap a felhasználó
  döntése szerint rendezve.
- A szkript egyetlen adat-, forrás- vagy kimeneti lexikonfájlt sem módosít (`git status` a futás után csak a `generalt/muhely/`
  változását mutatja).
- Hiányzó vagy hibával leálló mérő soha nem zöld.
- A nyilvános JSON csak fehérlistás mezőt tartalmaz (teszt).
- `python eszkozok/feladatok.py ellenoriz` 0 hiba; `python eszkozok/ellenoriz.py` új HIBÁT nem ad.

## 6. Döntésnapló

*Az a), c), d) pont döntése (2026-11-01): az orkesztrátor kérdése „Mehet a Feed/Stash a), c) és d) pontja a javaslat szerint?”,
a felhasználó válasza (szó szerint, az orkesztrátor továbbításában): „Igen, mind”. Mindhárom a lent leírt javaslat szerint.*

- **DT-F<nn>a ✅ eldöntve** (javaslat szerint, „Igen, mind”) — a generált JSON helye és bontása: `generalt/muhely/` alatt három
  fájl (`feed_belso.json`, `feed_nyilvanos.json`, `stash.json`), a nyilvános a belső fehérlistás szűrése; verziózva, hogy a #86
  delta-generátora commitok között összevethesse.
- **DT-F<nn>b ⛔** — az M0 után: ha az ISTENTISZT-001 nem zöld, a lap javul, vagy a kritérium pontosodik (melyik pontja).
- **DT-F<nn>c ✅ eldöntve** (javaslat szerint, „Igen, mind”) — a még nem létező mérők (próza-lefedettség a #125-ből, lektori
  kérdések a lektor-felületből) addigi kezelése: „nincs mérő”, ilyenkor a motívum nem „kész”; a 7. pont a lektor-felület M0-ja
  után élesedik.
- **DT-F<nn>d ✅ eldöntve** (javaslat szerint, „Igen, mind”) — a kötet-hozzárendelés (pl. Genezis I.) forrása: amíg nincs
  kötet-adat, a Stash üresen hagyja és jelöli („nincs kötet-adat”); az adatba vétel külön feladat a `/befogad`-dal.
