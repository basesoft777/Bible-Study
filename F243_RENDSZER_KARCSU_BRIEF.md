---
feladat: 243
cim: A rendszer karcsúsítása — rövid tanulságfájl a memória helyett, a lezárt tételek archiválása, rövidebb CLAUDE.md
kod: RENDSZER_KARCSU
tipus: feladat
fazis: folyamat
modell: opus
sav: SYSTEMS
allapot: nem_indult
alap: bd878146
ad: minden session kisebb, mindig betöltött szabálytesttel indul (a CLAUDE.md legfeljebb 12 000 bájt, a memória egy legfeljebb 4 000 bájtos tanulságfájl), a lezárt tételek és a régi memória archívumban, a méretet gépi kapu őrzi
kovetkezo: "Indul a kis adatjavítás (F240) lezárása után, az IRANY „Következő szálak” sorrendje szerint; utána jön a push előtti kapu kettévágása"
munka: folyamat
olvas: [CLAUDE.md, IRANY.md, MUNKAMENET.md, BRIEF_SABLON.md, CSAPDAK.md, NYITOTT_FELADATOK.md, sablonok/KESZ_LAP_KOVETELMENY.md, RENDER_BRIEF.md, .claude/commands/kovetkezo.md, .claude/agents/vegrehajto-sonnet.md, eszkozok/szamkiosztas.py, eszkozok/brief_lezaras.py]
ir: [CLAUDE.md, CSAPDAK.md, MUNKAMENET.md, BRIEF_SABLON.md, sablonok/KESZ_LAP_KOVETELMENY.md, .claude/commands/kovetkezo.md, archivum/NYITOTT_FELADATOK_lezart.md, eszkozok/indulo_teher.py, eszkozok/teszt_indulo_teher.py, eszkozok/szamkiosztas.py, .github/workflows/ellenorzes.yml]
fugg: []
---

# F243_RENDSZER_KARCSU_BRIEF.md — A rendszer karcsúsítása

*FELADATOK #243 · Modell: opus · v1 · 2026.11.24*

*Az integrátor indította (local_5140778b) a szerkesztő szavára (2026-11-24: „mehet a karcsúsítás briefje”). Az IRANY.md „Következő szálak” 2. pontja: „rövid tanulságfájl a teljes memória helyett; a lezárt tételek és memóriafájlok archiválása (nem törlés); a CLAUDE.md rövidítése a te jóváhagyásoddal (a tervre »mehet«, a diff merge előtt eléd); mérce: a CLAUDE.md sorszáma és az induló kontextus előtte és utána”. Előzmény és minta: F189 (a CLAUDE.md 18 KB-ról 14 KB-ra, a magyarázat a `CSAPDAK.md`-be); azóta a fájl 22,7 KB-ra nőtt vissza.*

## 1. Cél

Kevesebb induló kontextus és kevesebb szabály. Minden session minden fordulója újraolvassa a mindig betöltött fájlokat (a költség nagy része cache-olvasás, fordulónként a teljes kontextus), ezért az itt megtakarított bájt minden sessionben, minden fordulóban megtérül. Három lépésben:

1. a teljes memória-index helyett egy rövid tanulságfájl;
2. a lezárt tételek és a régi memóriafájlok archívumba kerülnek (végleges törlés nincs);
3. a `CLAUDE.md` a szabályokat tartja meg, a részlet a saját szabályhelyére költözik (CLAUDE.md „egy szabály, egy hely”, F184).

A visszanövés ellen gépi kapu, nem újabb bekezdés (DT952).

## 2. Mérce — a mai értékek (alap: bd878146, 2026-11-24)

| Mérés | Előtte (mért) | Cél utána |
|---|---|---|
| `CLAUDE.md` | 192 sor · 22 683 bájt (CRLF) · 20 715 karakter | ≤ 110 sor · ≤ 12 000 bájt |
| `MEMORY.md` (memória-index, minden sessionben betöltődik) | 73 sor · 10 940 bájt | tanulságfájl: ≤ 30 sor · ≤ 4 000 bájt |
| memóriamappa (`C:\Users\bases\.claude\projects\C--Users-bases-Desktop-Bible-Study\memory\`) | 74 fájl · 250 657 bájt | 1 fájl (a `MEMORY.md`) + `archivum/` |
| `IRANY.md` (a CLAUDE.md „bármi” sora szerint minden session olvassa) | 39 sor · 5 945 bájt | változatlan (a szerkesztő lapja) |
| `MUNKAMENET.md` | 290 sor · 54 767 bájt | nem töltődik be magától; a beköltöző szakaszokkal legfeljebb +4 000 bájt |
| **Mindig betöltött együtt** (CLAUDE.md + MEMORY.md + IRANY.md) | **39 568 bájt** ≈ 12 400 token | **≤ 22 000 bájt** ≈ 6 900 token |
| Induló kontextus (mért: egy integrátor által indított session első válasza, ennek a briefnek a sessionje) | **91 647 token** (cache-írás 36 022 + cache-olvasás 55 623 + 2) | ≈ 86 000 token (−5 500) |
| `NYITOTT_FELADATOK.md` (csak tételkereséskor) | 1 338 sor · 554 965 bájt; a „Lezárva” szakasz 58 876 bájt, mellette 82 sorközi `LEZÁRVA` tétel | a „Lezárva” szakasz nélkül (≈ 496 000 bájt; a menet méri) |

*A tokenbecslés bájt/3,2 (magyar, ékezetes szöveg; becslés, nem tokenizálóval mért). Az induló kontextus nagyobb része a rendszerprompt és az eszközleírások, ezekhez a repó nem nyúl: a mi részünk a 91,6 ezerből kb. 12,4 ezer; a cél ennek kb. a fele. A megtakarítás fordulónként kicsi (~6%), de minden fordulóban és minden sessionben jelentkezik.*

Mérés utána ugyanígy: az F243.1 mérőszkriptje (`eszkozok/indulo_teher.py`), és egy friss session első válaszának `usage` sora a saját átiratából (`~/.claude/projects/<projekt>/<session>.jsonl`, az első `"usage"`).

## 3. Hatókör

**Benne van:**
- **A) Tanulságfájl.** A memóriamappa `MEMORY.md`-je maga lesz a rövid tanulságfájl (ez töltődik be automatikusan; külön repófájl nem töltődne be). Minden sora önmagában érthető szabály, forrással zárójelben; részletért egy archív fájlra mutat. Fejléc-szabály a fájl elején: új sor csak akkor, ha a tanulságnak nincs szabályhelye és gépi kapuja; legfeljebb 30 sor.
- **B) Memória-archívum.** Mind a 74 fájl (a régi `MEMORY.md` is, `MEMORY_2026-11-24.md` néven) a memóriamappa `archivum/` almappájába kerül, első sorként ARCHÍV fejléccel (`<!-- ARCHÍV <dátum> (F243): <hová került a tanulsága> -->`), alatta bájtra változatlan törzzsel (a DT-F11a mintája). **A memória-archívum nem a repóban van, mert a repó nyilvános, a memóriában pedig magánadat áll** (életkörülmény, pénzügyi terv, külső kapcsolattartók nevei). Ezért a repó `archivum/` könyvtára csak a repó saját anyagát kapja (C pont).
- **C) A lezárt nyitott tételek archiválása.** A `NYITOTT_FELADATOK.md` „## Lezárva” szakasza (58 876 bájt) → `archivum/NYITOTT_FELADATOK_lezart.md` (ARCHÍV fejléc, változatlan szöveg). Előtte minden olvasó listája (`grep -l NYITOTT_FELADATOK`; ma 17 fájl, köztük `szamkiosztas.py`, `brief_lezaras.py`, `feladatok.py`, `dontes_nezet.py`, `ellenoriz.py`, `ellenorzes/szabalyok.py`, `sqlite_epit.py`, `olvasoi_kapu.py`, `push_elott.py`), és ahol egy olvasó N-számot keres vagy számot oszt, az archívumot is olvassa. **Kötelező teszt:** a következő N-szám az archívumbeli legnagyobb számot is figyelembe veszi (különben számütközés jön); a `feladatok.py ellenoriz` zöld marad. A 82 sorközi `LEZÁRVA` tétel most a helyén marad: az áthelyezésükhöz a `feladatok.py` `lezar:`-ellenőrzését is át kellene kötni, azt viszont a futó #241 és #123 is írja (függési kör); ezért a helyükön maradnak, és ezt a jelentés egy sorban kimondja.
- **D) A `CLAUDE.md` rövidítése** a 6. szakasz terve szerint, a szerkesztő jóváhagyásával. A kiköltöző szöveg a célhelyre kerül; ha a célhelyen a szabály már áll, csak a hivatkozás marad. Minden kódból, briefből, parancsból mutató hivatkozás (pl. „CLAUDE.md „Gyors sáv az olvasóra””, „„Új motívum-ID”, 4. kérdés”, „„Modell-ellenőrzés””, „„Git””, „„TSV-olvasás””) ugyanabban a commitban frissül vagy célt talál (E27, E36).
- **E) Gépi kapuk:** (1) `eszkozok/indulo_teher.py`: kiírja a mindig betöltött fájlok sorát, bájtját és becsült tokenjét, és ha a memóriamappa helyben elérhető, a `MEMORY.md` méretét is; plafon fölött figyelmeztet. (2) CI-kapu: `python eszkozok/indulo_teher.py --kapu` egy új lépésként a `.github/workflows/ellenorzes.yml`-ben (egy lépés hozzáadása; a szabálytáblához, az `eszkozok/ellenorzes/szabalyok.py`-hoz nem nyúl, mert azt a futó #241 és #123 is írja): a `CLAUDE.md` 12 600 bájt fölött (a cél + 5%) HIBA, és az üzenet megmondja a teendőt („a részlet a szabályhelyére, a CLAUDE.md-be csak hivatkozás”). A memória a repón kívül van, ezért azt a CI nem látja: azt a mérőszkript és az integrátor napi cseréje nézi.
- **F) Hivatkozások a memóriára.** A `sablonok/KESZ_LAP_KOVETELMENY.md` Forrás oszlopa ma 30 helyen hivatkozik memóriafájlra (`memória: <név>`; leggyakrabban `hamart-uj-arany` 6, `visszhang-reteg-terv` 4, `lap-jovahagyas-elott` 3, `lezaras-rogzitett-lepesszam` 3). Ahol a szabálynak van DT-je vagy repóbeli szabályhelye, arra cserélődik; ahol nincs, `memória-archívum: <név>` lesz. A lezárt briefek szövege nem változik (F194, F203, F218 is hivatkozik memóriára: ezek a nevek az archívumban továbbra is feloldhatók).
- A mechanikusan áthelyezhető csapdák a `CSAPDAK.md`-be: a zárfájl törlése (`~/.pardes/ellenorzes.zar`: a pid újraolvasása közvetlenül törlés előtt, élő pidnél tilos), a WSL-indítás (`PARDES_DB` a natív példányra, `wsl -e`, nem `--`), a nehéz lapgen-futás előtti `python.exe`-lista. A hiányzó M-MÉRCE mechanizmus (ma csak a memóriában él) a `naplok/HIBA_MECHANIZMUSOK.md`-be való, de azt a futó generátor-átállás (#241) írja: a session a szövegét az integrátornak küldi, aki a #241-nek adja, vagy annak lezárása után pótoltatja.

**Nincs benne:**
- A lezárt briefek (201 fájl, 2,3 MB a gyökérben) áthelyezése: nem töltődnek be, az áthelyezés viszont a `feladatok.py` számkiosztását, a függésszámítást és az E27-et érintené, haszon nélkül.
- A `FELADATOK.md`: a „Kész” lista már ma is csak az utolsó két hetet mutatja (generált blokk), archiválnivaló nincs.
- A `DONTESEK.md` (1,45 MB) és a két changelog: a döntés nem lezárt tétel; nem töltődnek be.
- Az `IRANY.md` írása: az a szerkesztő lapja; ahol a CLAUDE.md-terv az IRANY-ra hivatkozik, ott a szabály már ott áll.
- Új szabály. A menet csak áthelyez, rövidít és hivatkozást ír; a szabály tartalma nem változik és nem gyengül (a szabálylista-összevetés méri, F243.7).
- Más session folyamata, a lexikon, az `adat/` és a generátor.
- A futó ágak fájljai: a `naplok/HIBA_MECHANIZMUSOK.md` (#241), a `konkordancia/README.md` (#48), a `sablonok/6_…` és `sablonok/9_…` (#123). Ezeket a menet csak olvassa (az F243.2 grep-je), nem írja; a függésszámításba ezért nem kerültek be.

## 4. Lépések (⛔ a kötelező megállások)

0. **F243.0** — Modell-ellenőrzés; `python eszkozok/feladatok.py alap 243` (alap: bd878146), a brief `allapot: fut`, draft PR (első sor: Mérce · Állapot · Következő · Akadály). A 2. szakasz „előtte” értékeinek újramérése a mai main-en; ha eltérnek, a jelentésbe mindkettő.
1. **F243.1** — `eszkozok/indulo_teher.py` + `eszkozok/teszt_indulo_teher.py`; az „előtte” sor a jelentésbe.
2. **F243.2** — Memória-táblázat (`naplok/F243_memoria_tabla.md`): mind a 74 fájl egy sorban: fájlnév · besorolás (`tanulsag` / `szabalyhely` / `csapdak` / `archiv`) · a szabályhely grep-pel igazolva (fájl + kulcsszó) vagy „nincs”. **A táblázatba tartalom nem kerül, csak fájlnév, besorolás és szabályhely** (a repó nyilvános). Kiindulás az 5. szakasz besorolása; ahol a grep nem igazolja a szabályhelyet, a besorolás `tanulsag` vagy „a szabályhelyre kerül” (a célfájl megnevezésével), nem `archiv`.
   **⛔ Az integrátor jóváhagyja a memória-archiválás listáját és a tanulságfájl sorait** (a tanulságfájl tervezete a repón kívül, a közös jegyzetmappában: `F243_TANULSAG_TERVEZET.md`). Jóváhagyás nélkül a memóriához nem nyúlsz.
3. **F243.3** — Memória: az új `MEMORY.md` (tanulságfájl), a 74 fájl az `archivum/`-ba ARCHÍV fejléccel. A memória a repón kívül van, commit nincs; a jelentésbe: a fájllista, az áthelyezés előtti és utáni sha256 a fejléc nélküli törzsre (bájtra egyezés), és az új `MEMORY.md` mérete. A `CSAPDAK.md` három új szakasza, az M-MÉRCE szövege az integrátornak, a `KESZ_LAP_KOVETELMENY.md` 30 hivatkozása (F pont) — commit.
4. **F243.4** — `NYITOTT_FELADATOK.md` → `archivum/NYITOTT_FELADATOK_lezart.md` (C pont): olvasó-lista a jelentésbe, átkötés, a két kötelező teszt, bájt előtte és utána.
5. **⛔ A CLAUDE.md-terv (6. szakasz) a szerkesztő „mehet”-je nélkül nem indul.** Az integrátor viszi elé; a jóváhagyás szövege és dátuma a Döntésnaplóba (5. szakasz) kerül, a forrás „szerkesztői döntés”. Ha a szerkesztő a terv egy sorát módosítja, az a módosított sor szerint megy.
6. **F243.5** — A `CLAUDE.md` rövidítése a jóváhagyott terv szerint; a kiköltöző szöveg a célhelyre; a hivatkozások frissítése; `python eszkozok/feladatok.py ellenoriz` és a helyi E-ellenőrzés (E27, E36) zöld.
7. **F243.6** — CI-kapu a `CLAUDE.md` méretére (E pont 2.), teszttel; ha a #241 közben a `.github/workflows/ellenorzes.yml`-t is módosította, a main behozása után.
8. **F243.7** — „Utána” mérés (2. szakasz minden sora), a régi és az új `CLAUDE.md` szabálylistájának tételes összevetése a jelentésben (minden szabály: hol áll most). `python eszkozok/teszt_futtat.py --gyors` és a push előtti kapu. Egy független ellenőrzés (`fuggetlen-ellenor`; eszköz és szabályhely változik, nehéz kör), legfeljebb egy javítókör.
9. **⛔ A diff merge előtt a szerkesztő elé kerül** (a `CLAUDE.md` diffje és a szabálylista-összevetés, az integrátoron át). Merge csak utána; a nézett commit hash-e a PR leírásába.

*Átadás:* kb. 150–200 ezer token kontextusnál a lépéshatáron `/handoff`, a PR első sora és a jelentés frissítése után; a folytató session ugyanazon az ágon.

## 5. A memória besorolása (kiindulás az F243.2-höz)

A 74 fájl végigolvasva 2026-11-24-én. A tanulságfájlba csak az kerül, aminek nincs szabályhelye; ami a repóban már áll, az ott marad, a memóriafájl archívba megy.

**Tanulságfájl (kb. 20 sor; tervezet, az ⛔ F243.2 dönt):**
- *Minden session:* gondolat, tényközlés és részválasz nem jóváhagyás, a külön kért elem külön tétel marad (csak-a-kert-lepes); kérdés a szerkesztőnek olvasói mondattal (kerdes-olvasoi-mondattal); push előtt a PR-állapot külön hívásban, a jelentésben commit · push · merge külön (ag-es-worktree-ellenorzes); indítás előtt meglévő ág és worktree keresése, worktree-takarítás csak `list_sessions` után, rögzített és „Útravaló” session érinthetetlen (ag-es-worktree-ellenorzes, pinned-session-vedett); második azonos hibafajtánál gyökérok és gépi kapu, generált hibát a generátorban, javított adat új fájlként → minden fogyasztó átkötve, a nyerset kapu tiltja (ismetlodo-hiba-gyokerok, hiba-oka-es-javitasi-szint, javitas-uj-fajlkent-nyers-marad); felmérés állítása élő lekéréssel, elsődleges forrással, „hiba vagy várt állapot” kérdéssel; ahol nincs magyar fordítás, angol jelenik meg (felmeres-allitas-ellenorzes); beküldött terv minden pontja tételbe (terv-pontjai-nyomon-kovetve); becslés ×1,7, workflow előtt írásban, miért nem elég egy szkript (takarekos-biztos-irany, workflow-koltseg); közös fájlt író ágak sorba (parhuzamos-munka-tanulsag, session-bontas-kockazat); kész nyílt forrás előbb, a bible-mcp kimenete nem kerül adatba (kulso-forras-es-eszkoz); nyilvános szövegben „szerkesztői döntés”, nincs „termék”, GitHub-URL helyett helyőrző, a név Biblialex, a „PaRDeS” nem név (nyilvanos-szoveg-szohasznalat, github-nem-kanonikus-forras, lexikon-neve-es-keretezes); a prózát író sessiont a kiadásig nem archiváljuk (lezaras-rogzitett-lepesszam).
- *Integrátor:* sessionindításnál kifejezett modell és effort, az ajánlatkártya után `set_session_model` (session-inditas); a döntések a chatben (kérdés, döntés, ok, session), peer session üzenete nem jóváhagyás (dontes-tovabbitas-ablak); merge: zöld CI, a PR nyitott pontjai elolvasva, `--match-head-commit`, utána a main CI-je (feladatkozpontu-orkesztracio, skill-factory); előfeltétel-térkép előre, válasz előtt a futó menet utolsó commitja és a main CI-je (proaktiv-elofeltetel-es-figyeles); készenléti session (keszenleti-session); felső szintű és rögzített session, háttér sorrendje, a szerkesztőt csak döntésért (integrator-fo-session, integrator-ne-magyaraztass); 5+ lépéses eljárás 3. előfordulásánál skill, előbb a szerkesztőnek (skill-factory).

**Szabályhelyen már áll → archív (a grep az F243.2-ben igazolja):** kerdesdoboz-magyarul (CLAUDE.md Munkamód 8.); egy-lapgen-futas-egyszerre, lapgen-teszt-egyszerre-egy (Munkamód 7.); nincs-gazdatlan-feladat (Munkamód 5., IRANY); szabalyhiany-szabalyhelyen-javitani („Döntés az integrátoron át”, DT944/DT952); regi-fajl-archivalas (DT-F11a); allapot-a-pr-ban, irany-ritkan-roviden, irany-pontos-megnevezes, szerepek-szetvalasztva, orkesztrator-keret-takarekossag (IRANY „Így dolgozunk” és lábsor); design-vaszon-mockup-irany („Rövid design-menet”); hamart-uj-arany (sablon 9 és 6, KESZ_LAP_KOVETELMENY, SEMA); hibanaplo-mechanizmus (`naplok/HIBA_MECHANIZMUSOK.md`; az M-MÉRCE pótlása a #241-é); celzott-ujraellenorzes (`/kiadas` 3/b); lap-jovahagyas-elott (KESZ_LAP K06); 1a-kerek-proza, nave-blokk-minden-cikkben, olvasoi-szoveg-adatbol-kovetkeztetes, olvasoi-szoveg-csere-gyokerok, szotar-es-motivum-ket-reteg, aranyminta-elobb, pilot-a-latvany-mercéje, lap-menet-szintje, kovetkezo-cikk-menetrend, cikk-session-kontextus-takarekos, igeszakasz-tanulmany-elore, forditas-nyelvkozi-egyseg (sablon 6/9/10, MUNKAMENET C, KESZ_LAP; ahol a grep nem igazolja, a szabályhelyre kerül); kereszthivatkozas-ket-rendszer (DT-F181a).

**A `CSAPDAK.md`-be → archív:** zarfajl-torles-elott, wsl-inditas-es-tesztek.

**Projektállapot, háttér, magánadat → archív (nem töltődik be, kérdésre olvasható):** doktori-ut-kizarva, technologia-nem-nyilt, orcid, f86-dontesek-2026-10-28, nyilt-adat-kozles, kulso-lektor, fable-kreditbol, forditas-keret-es-menet, utemezes-2026-11-11, befogadasra-var, olvaso-felmeresek-nyitva, olvaso-ketnyelvu-jegyzek, olvaso-alapnezet-es-felvetesek, visszhang-reteg-terv, f125-kiejtes-es-lepesek, lexikon-ag-lezaras-2026-11-08, a régi MEMORY.md. *Ezekben csak itt él több azonosító (artifact-URL-ek, DOI-k, kapcsolattartók, vászon-azonosítók): az archívum ezért megmarad, és a tanulságfájl utolsó sora rá mutat.*

## 6. A `CLAUDE.md` terve — szakaszonként (⛔ a szerkesztő „mehet”-je)

Jelölés: **M** = megmarad · **R** = rövidül (a mag marad) · **H** = hivatkozássá rövidül, a szöveg a célhelyre költözik (ha ott már áll, csak a hivatkozás marad) · **K** = kiesik (a feltétele megszűnt). A kódból hivatkozott szakaszcímek megmaradnak.

| # | Szakasz (mai bájt) | Döntés | Célhely | Cél (bájt) |
|---|---|---|---|---|
| 1 | Cím és bevezető (423) | M | — | 420 |
| 2 | „Ezt olvasd, ezt ne”: az archív-figyelmeztetés és a feladattábla (1 718) | R: a 96 KB-os archívumra egy sor; a tábla marad, a „hol áll egy szabály” sor tömörebben | — | 1 100 |
| 3 | Rétegek táblázata (932) | M | — | 930 |
| 4 | „Átmenet (D34)” bekezdés | K vagy egy sor: a feltétele, a #11 lezárása teljesült (F11 `lezarva`); a szerkesztő dönt, kiesik-e | DONTESEK D34 | 0–150 |
| 5 | „Egyirányúság (DT28)” (~900) | R: három mondat (egy fájl egy réteg; forrás → adat → kimenet; forrásba adatot visszaírni tilos) | DONTESEK DT28 | 500 |
| 6 | A nyolc rés bekezdése (~800) | H: „A lexikonlap réseit csak a forrásban szerkeszted” + mutató | RENDER_BRIEF G1/G4, sablon 6 | 200 |
| 7 | Az értelmező próza egy kézben (K1) és a `generalt_proba/` (~400) | M, soronként egy mondat | — | 350 |
| 8 | Három szabály (788) | M, szó szerint | — | 788 |
| 9 | Modell-ellenőrzés (1 528) | R: a mag (első lépés a saját modellnév, összevetés, eltérésnél megállás, az adattáblába a tényleges név); a subagent-esetek és a `külső:<név>` részletei | `.claude/commands/kovetkezo.md` 6. lépés, `vegrehajto-sonnet.md` | 650 |
| 10 | Kutatási menet — a hét lépés (923) | H: egy sor („a gerincet mindig levezetni és dokumentálni, üres eredménynél is”) + mutató; a lépések a MUNKAMENET B2–B9 táblájában már állnak | MUNKAMENET B | 200 |
| 11 | Új motívum-ID, négy kérdés (841) | R: a négy kérdés és a fölérendelt fogalom tömörebben marad (a szerkesztő határ-szabálya, DT938; a sablon 9-et a futó #123 írja, oda most nem költözik) | — | 450 |
| 12 | Adat-tár (1 307) | R/H: marad a „nyers adat nem a fő szálba” és az igehely-formátum normalizálása (néma nem-találat); a TAHOT-, KJV- és SDBH-korlát egy „Adatkorlátok” szakaszba (a `konkordancia/README.md`-t a futó #48 írja) | `CSAPDAK.md` (a TAHOT már ott) | 500 |
| 13 | Shell (635) | M | — | 635 |
| 14 | TSV-olvasás (522) | M (kódból hivatkozott cím) | — | 522 |
| 15 | Git (2 204) | R: commit-szabály, hivatkozás-frissítés, granularitás, UTF-8 fájlból; a helyőrző és a PR-onkénti döntés-/nyitott-fájl szabálya két sorra, a teljes szöveg | `BRIEF_SABLON.md` (ma onnan mutat vissza ide) | 1 200 |
| 16 | Munkamód 1–10 (3 232) | R: a tíz pont marad, pontonként egy-két sor; a 4. pont felhatalmazás-része és a 10. pont integrátor-része az IRANY-ban már áll („Így dolgozunk”), ide hivatkozás | IRANY „Így dolgozunk” | 1 600 |
| 17 | Döntés az integrátoron át (2 245) | R: a mag (a kérdés az indító sessionnek megy; technikai kérdésben a session dönt, DT920) és a kivétellista (pénz, külső közlés, végleges törlés, motívumhatár DT938); a szabályhiány-mondat (DT944/DT952) egy sor | IRANY „Új szabály helyett gépi kapu” | 1 200 |
| 18 | Rövid design-menet (1 148) | H: két sor (csak CSS/arculat diff: DESIGN-APRO; ágas előnézet, nézett hash) | MUNKAMENET új „Rövid sávok” szakasz (DT886) | 200 |
| 19 | Gyors sáv az olvasóra (2 018) | H: két sor (csak `eszkozok/olvaso_szerver/` diff: OLVASO-GYORS); a „Felmérési szünet” pont K (a #231 lezárva) | MUNKAMENET „Rövid sávok” (DT919) | 250 |
| | **Összesen** | | | **≈ 11 750** |

## 7. Elfogadási feltételek

- A 2. szakasz minden sora előtte és utána a jelentésben; a `CLAUDE.md` ≤ 12 000 bájt és ≤ 110 sor; a `MEMORY.md` ≤ 4 000 bájt és ≤ 30 sor; a mindig betöltött három fájl együtt ≤ 22 000 bájt.
- Szabály nem vész el és nem gyengül: a régi és az új `CLAUDE.md` szabálylistája tételesen össze van vetve (minden szabály: hol áll most); a memória mind a 74 fájlja a táblázatban, besorolással és igazolt szabályhellyel.
- Végleges törlés nincs: a memória-archívumban mind a 74 fájl törzse bájtra egyezik az eredetivel (sha256); a `NYITOTT_FELADATOK.md` lezárt tételei az archívumban változatlanok.
- A következő N-szám az archívumot is látja (teszt); a `lezar:`-ellenőrzés változatlanul zöld.
- A CI-kapu a `CLAUDE.md` méretére él; a `feladatok.py ellenoriz`, az E27 és az E36 zöld; a gyors tesztek zöldek.
- Memóriatartalom nem kerül a repóba (a táblázatban csak fájlnév, besorolás, szabályhely).

## 8. Döntésnapló

- **Befogadás (2026-11-24), szerkesztői döntés (az integrátor, a felhasználó felhatalmazásával, DT936):** „a befogadás mehet így”. Elfogadva az is, hogy a memória-archívum a memóriamappában van, nem a repóban („helyes, elfogadva”). A CLAUDE.md-terv (6. szakasz) itt tervként áll; a ⛔ (4. szakasz, 5. lépés) a végrehajtásban marad: a szerkesztő válaszát az integrátor továbbítja, és ha a szerkesztő módosít, a brief a PR-on igazodik.
- Szám: a briefet 242-re írtam, de a `kovetkezo_szam --foglal` a helyi, még commitolatlan briefet is foglaltnak vette, és a 243-at foglalta le (`foglalas/F243`). A brief ezért 243 lett, így foglalóágat nem kellett törölni; a 242 szabad maradt.
- (A további ⛔ pontok jóváhagyása ide kerül, idézettel és dátummal. Új döntés helyőrzővel a `dontesek/uj/<ágnév>.md`-be.)
