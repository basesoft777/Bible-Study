# FELADATOK.md — feladatkövető

*v1.3 · 2026.09.30 · `main` = `29ada3c` (PR #76) + a csomagmód átvétele · Ez az egyetlen fájl, amit a chat egy új beszélgetés elején elolvas. A részletek a briefekben és a `NYITOTT_FELADATOK.md`-ben vannak; ide csak az állapot, a függés és a következő lépés kerül. Munkafolyamat: `/kovetkezo` orkesztrátor, döntések a `DONTESEK.md`-ben.*

## Alapelv: előbb az adatréteg, utána a render

Amíg nem látjuk, mit adnak az új források, nem foglalkozunk rendereléssel (lexikonoldal, törzscikk, migráció), mert a késői adat miatt mindent újra kellene generálni. Emiatt két fázis van, és a 2. fázis egyik feladata sem indul, amíg az 1. fázis el nem készül.

**Kritikus út:** #1 és #2 → #4 → #5 → #7 → #9 → #10; az LXX-ágon #6 → #17 → #8 → #10

## 1. fázis — adatréteg

<!-- GENERÁLT-KEZDET: feladatok.py --cel fazis1 -->
| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Következő lépés | Hol |
|---|---|---|---|---|---|---|
| 7 | Thayer teljes magyar fordítása (éles) | a görög mélységi szócikk magyarul, adatként | ⬜ brief kell | #3 (kész), #5 (kész), #14 (kész) | halasztva (D46): a teljes Thayer gépi fordítása akkor, ha lesz böngésző felhasználó; a lexikon szócikkeit a #28 fordítja | `F07_THAYER_ELES_BRIEF.md` |
| 22 | "Károli–Strong párosítás könyvenként, két modellel (Sonnet + Gemini); első könyv: 1Mózes" (F22) | "Az 1Mózes minden Károli-szavához az eredeti szó és a Strong-szám, bizonyossági jelöléssel (magas = a két modell egyezik)" | ⏸ döntésre vár | #21 (kész) | "Te: következő könyv előtt a jelzett fejezetek kézi jóváhagyása (első: 4Móz 30); Ézs 9:17–20 megfeleltetése hamis; a 3Móz csak Sonnettel készült (DT-F22c nyitva: a Gemini marad-e), a PR #114 merge-e és a zárt összevetés (zart_osszevet.py) a felhasználóé" | `F22_KAROLI_STRONG_BRIEF.md` |
| 23 | Egyforrású motívumdokumentum: forrássablon és mélységi szintek (terv) (MOTIVUM_FORRAS) | a B szerkezet terve mérésekkel: szakasz-leképezés, forrássablon-tervezet, szintjelölés a SEMA-ban, CI-szabályok leírása; renderelés és fájlmozgatás nélkül | ⬜ | #37* | /kovetkezo; ⛔ az M0 felmérés után | `F23_MOTIVUM_FORRAS_BRIEF.md` |
| 27 | Thayer-fordítás: Opus és Gemini összevetése, Max-keret méréssel (FP3) | mért adat a #7 modellválasztásához (A: Opus mindenre, B: vegyes hosszhatárral, vagy Gemini marad): minőség hosszkategóriánként, gépi kapuk, Max-keret fogyása és kivetítése a teljes Thayerre | ⬜ | — | halasztva (D46): a gépi alap modellválasztásához kell, a #7-tel együtt veszi elő a felhasználó | `F27_FP3_BRIEF.md` |
| 30 | Döntés- és N-számok kiosztása merge-kor (helyőrző az ágakon) (SZAMOZAS) | az ágak nem foglalnak végleges DT/N-számot; a párhuzamos merge-ek nem ütköznek sorszámon; a main-en a számokat egy Action osztja ki | ⬜ | #8 (kész), #16 (kész), #17 (kész), #32* | a helyőrző-Action és a CI-szabály megírása, a DT18 átszámozása, a nyitott ágak helyőrzőre állítása | `F30_SZAMOZAS_BRIEF.md` |
| 38 | A teljes BDB héber szótár magyar fordítása Opusszal, megállási pontokkal (BDB_FORDITAS) | a BDB_teljes_unabridged.tsv mind a 8 090 szócikkének teljes magyar fordítása az adat/forditasok.tsv-ben (allapot=opus), gyakorisági sorrendben, adagonként commitolva; ami a futás leállításáig nem készül el, angol marad | ⬜ | #34 (kész) | M0 felmérés + M1 mérő adag, utána megállási pont (⛔ M1) | `F38_BDB_FORDITAS_BRIEF.md` |
| 40 | Hivatkozás-ellenőrzés a feladatkövetőben (CI új szabálya) (HIVATKOZAS_ELLENORZES) | a CI minden PR-nál jelzi, ha a FELADATOK.md vagy egy brief nem létező fájlra, ágra vagy commitra mutat, illetve ha egy PR áthelyez vagy töröl egy hivatkozott fájlt anélkül, hogy a mutatót frissítené | ⬜ | #2 (kész), #30*, #37* | /kovetkezo | `F40_HIVATKOZAS_ELLENORZES_BRIEF.md` |
| 41 | BSB-import kiegészítése — a küszöb alatti 8 ószövetségi könyv újramérése versszám-megfeleltetéssel, és az üres angol szavak jelölése (BSB_UJRAMERES) | a versszámozás miatt küszöb alatt maradt ószövetségi könyvek a 95%-os küszöbbel újramérve és importálva, a többinél igazolt ok; a BSB_Strongs.tsv-ben megkülönböztethető a „szándékosan nem fordított” és a „hiányzó” angol szó | ⬜ | #16 (kész) | futtatás az orkesztrátorral; az 1. lépés végén ⛔ megállás | `F41_BSB_UJRAMERES_BRIEF.md` |
| 43 | LXX-döntések ellenőrzése a lxx_bridge héber–görög párlistával (LXX_BRIDGE) | a 86 LXX-döntés mindegyikéhez a lxx_bridge (MACULA-eredetű, LXX-en összesített héber→görög Strong-párok) egyezés/eltérés/nincs-adat ítélete, a bizonyosság-emelés jelöltjeivel; az lxx_dontesek.tsv nem változik | ⬜ | #8 (kész) | "Te: a lxx_bridge CSV és a LICENC.md commitja az adat/kulso/ alá; utána /kovetkezo" | `F43_LXX_BRIDGE_BRIEF.md` |
| 44 | Licenc-utókövetés — a Károli 1908 és a versifikációs táblák forrásának tisztázása (LICENC_UTOKOVETES) | az adat/licencek.tsv Karoli_1908, Karoli_KH és Versifikacios_tablak sora tisztázott vagy dokumentáltan tisztázatlan marad, szó szerinti licencidézettel és rögzített commit-tal; a k-mktr/karoli_bible_hu nyílt Károli-jelölt felmérve; a TVTMS fájl neve és commitja rögzítve; az openbible.info kereszthivatkozás-tábla forrásjelöltként felvéve licencidézettel; a bible-mcp connector használati szabálya döntési javaslatként | ⬜ | #33 (kész), #42 | "Te: a karoli_bible_hu dataset-kártya licenc-mezőjének és README-jének lemásolása az adat/kulso/karoli_bible_hu_LICENC.txt-be (0. lépés), és az openbible.info licencnyilatkozatának lemásolása az adat/kulso/openbible_crossrefs_LICENC.txt-be (3b); a /kovetkezo nem indítja az F44-et, amíg mindkét fájl nincs a repóban" | `F44_LICENC_UTOKOVETES_BRIEF.md` |
| 46 | A BDB rosszul feloldott könyvneveinek felmérése és javítása a forrásban és a fordításokban (BDB_KONYVFELOLDAS) | a konkordancia/BDB_teljes_unabridged.tsv és az adat/forditasok.tsv BDB-sorainak igehelyei a helyes bibliai könyvre mutatnak (független BDB-forrással és versszám-ellenőrzéssel igazolva); a kétes esetek kézi listán; az N-F34 maradéka és az N-F34c lezárva | ⬜ | #34 (kész) | végrehajtás a /befogad után, a BDB-fordítás (#38) két adagja közötti megállásnál | `F46_BDB_KONYVFELOLDAS_BRIEF.md` |
<!-- GENERÁLT-VÉGE: feladatok.py --cel fazis1 -->

## 2. fázis — render (csak az 1. fázis után)

<!-- GENERÁLT-KEZDET: feladatok.py --cel fazis2 -->
| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Megjegyzés | Hol |
|---|---|---|---|---|---|---|
| 9 | Szótári adatréteg, 2. menet (SZOTAR S2) | az 1. fázis adatai megjelennek a 8 lexikonoldalon és a 8 törzscikkben | ⬜ | #5 (kész), #6 (kész), #7*, #38*, #46* | Ez javítja a törzscikkek elavult Cremer-sorát is (a CI E11 szabálya jelzi) | `F05_SZOTAR_BRIEF.md#2. menet — kimenet-változtató` |
| 10 | 8 lexikonoldal lezárása (LEXIKON_LEZARAS) | mérhetően kész oldalak (L1–L7) | ⬜ brief kell | #8 (kész), #9 | **Te:** döntés az L6 és L7 feltételről. Ide tartozik N18, N19. Előfeltétel: a #8 négy nyitott sora (LD008, LD009, LD058, LD064) eldöntve | `F10_LEXIKON_LEZARAS_BRIEF.md` |
| 11 | Migráció: egy forrásból renderelés (MIGRACIO) | minden motívum a forrásrétegből renderel | ⬜ brief kell | #9 | Az M0 felmérés csak olvas, de az eredménye itt kell | `F11_MIGRACIO_BRIEF.md` |
| 12 | TEREMT-002 3. lépés (próza, lexikonoldal) | az első natív egyforrású motívum kész | ⬜ brief kell | #11 | A tohu/bohu szótári adata az S1-ben készül (SZOTAR-D29). | `TEREMT002_KUTATAS_BRIEF.md` |
| 13 | 1Móz 17-től a tanulmányok és a 6 betöltetlen motívum | a Genezis-kiadás tartalma | ⬜ brief kell | #10 | döntés 2026.09.21: a lexikonoldalak lezárása után | `F13_GENEZIS_KIADAS_BRIEF.md` |
| 25 | Olvasói felület: statikus HTML állítható mélységgel (OLVASOI_HTML) | a motívumforrásból generált statikus HTML-oldalak (Netlify), lenyitható apparátussal és mélységi szintekkel; később PWA | ⬜ brief kell | #11, #12, #23 | brief a #11 1. lépcsője (ISTENTISZT-001) után, a MOTIVUM_FORRAS szintjelölésére építve | `F25_OLVASOI_HTML_BRIEF.md` |
| 36 | Az éles lexikon/ újragenerálása az F28, a BDB_PSI és a SIR_SZENTSZELLEM után (LEXIKON_UJRAGEN) | a lexikon/[ID]_TUDOMANYOS.md és _TORZSCIKK.md fájlok a jelenlegi adatból újragenerálva; a nulla-diff / várt diff dokumentálva (az F28 fordításai, a javított ψ-igehelyek, a Szent Szellem-szöveg) | ⬜ | #7*, #9*, #28 (kész), #34 (kész), #35 (kész), #37*, #38*, #42*, #46* | M0 szárazfutás ideiglenes könyvtárba (a repón kívülre); ⛔ az éles fájlok felülírása előtt | `F36_LEXIKON_UJRAGEN_BRIEF.md` |
<!-- GENERÁLT-VÉGE: feladatok.py --cel fazis2 -->

## Folyamat és eszközök

<!-- GENERÁLT-KEZDET: feladatok.py --cel folyamat -->
| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Következő lépés | Hol |
|---|---|---|---|---|---|---|
| 32 | Kontextus-őrzés: az értelmező munka egy kézben marad, a csomagmód csak adatfeladatra (KONTEXTUS) | négy munkaszabály a MUNKAMENET-ben és a brief-sablonban, a feladatok.py fejléc- és csomag-ellenőrzése, a #23 briefjének kiegészítése és függése; döntési tétel a TEREMT-002 3. lépésének előrehozásáról | ⬜ | — | /kovetkezo; ⛔ a K5 DONTESEK-tétele után | `F32_KONTEXTUS_BRIEF.md` |
| 37 | Tanulmány-ellenőrzés: CI-szabályok és független ellenőr (TANULMANY_ELLENORZES) | a tanulmányokat CI (E20–E24, a T0 szerint) és a fuggetlen-ellenor ügynök ellenőrzi; a régi tanulmányokról két auditjelentés készül | ⬜ | #30, #32, #45* | /kovetkezo; ⛔ a T0 után (nincs Strong-jelölt eredeti szöveg, vagy az SzPA kötelező szakasz a Tanulmány sablonban) és a T2 után (az alap tanulmányok sorsa) | `F37_TANULMANY_ELLENORZES_BRIEF.md` |
| 42 | Forrásfájlok kivezetése és a licencállapot egyetlen forrása (FORRASKIVEZETES) | A TBESH-család a gitignore-olt _nyers/ alatt, letöltő szkripttel. Az LXX_kivonat kivezetve. A generátor licencjelölése az adat/licencek.tsv-ből olvas. | ⬜ | #33 (kész), #35 (kész) | a lexikonoldalak újrarenderelése a frissített licencjelöléssel; a BDB-fordítás (az előfeltétele a tisztázott licencforrás) | `F42_FORRASKIVEZETES_BRIEF.md` |
| 45 | Modell-ellenőrzés minden brief futtatásának elején (MODELL_ELLENORZES) | minden brief-futtatás (közvetlen és /kovetkezo útján, subagenttel vagy anélkül) az elején ellenőrzi, hogy a ténylegesen futó modell egyezik-e a brief fejlécének `modell` mezőjével, eltérésnél nem dolgozik; az adattáblák `modell` mezőjébe mindig a tényleges modellnév kerül | ⬜ | — | végrehajtás a /befogad után | `F45_MODELL_ELLENORZES_BRIEF.md` |
<!-- GENERÁLT-VÉGE: feladatok.py --cel folyamat -->

## Naplózás

<!-- GENERÁLT-KEZDET: feladatok.py --cel naplozas -->
- #26 Egyforrású lánc (B) döntéseinek rögzítése és az érintett briefek fejléce — ⬜ — /kovetkezo, a MOTIVUM_FORRAS, LICENC és OLVASOI_HTML befogadása után (`F26_EGYFORRAS_NAPLO_BRIEF.md`)
<!-- GENERÁLT-VÉGE: feladatok.py --cel naplozas -->

## Takarítás (bármikor, rövid)

- A `claude/forditas-pilot-brief-3afbbf` ág törlése (csak az FP0 van rajta, ős).
- A chatben készült briefek (#4, #7, #10, #11) commitolása a repó gyökerébe, hogy a chat onnan olvassa őket.
- 72 távoli ág van, ebből kb. 60 régi (2026.09.02–09.11). Egyszeri átnézés, majd törlés.
- E5: a `-` kezdetű törölt sorok (felsorolás) alulszámolása, 68eb348 óta (l. naplok/ELLENOR_CI_E5.md, 2. kör). Rövid CI-javítás külön ágon (D6), legkésőbb a 2. fázis előtt.
- E9: a F*_BRIEF.md fájlok kizárása (a fordítási szabályok angol szavakat idéznek; l. PR #88). Külön ágon (D6).
- A `claude/macula-import` távoli ág törlése (az F17 PR #87 óta mergelve; a javító menet új ágon, `claude/f17-macula-javitas` fut).

## Munkamenet (tokentakarékos)

1. **Indítás és egyeztetés:** új Code-session, `/kovetkezo`. Egy session egy feladatot vagy egy csomagot futtat; a csomag egymástól független feladatokból áll (D20). A parancs csak a `main`-ben lévő briefekből futtat, javaslatot tesz a következő végrehajtható feladatra vagy csomagra, és veled egyezteti (feladatválasztás, hatókör, modell). Addig semmit nem ír és nem indít; csak a kifejezett „mehet” után futtat. **Új brief befogadása külön sessionben, a `/befogad` paranccsal** (csatolt brief vagy a `beerkezo/` mappa; D22, D29): a befogadás saját ágon, draft PR-rel jár, és csak a PR merge-e után futtatható a feladat (D30).
2. **Egy feladat = egy brief = egy ág.** A brief a repóban van. Neve a feladat kétjegyű számával kezdődik: `F<nn>_<NEV>_BRIEF.md` (pl. `F05_SZOTAR_BRIEF.md`). A fejléce (l. `BRIEF_SABLON.md`) a feladat számát, állapotát, modelljét (`sonnet` | `opus` | `haiku` | `külső:<név>`), az `olvas`/`ir` listáit és a „Mit ad” / „Következő lépés” szöveget hordozza; ebből generálódik a tábla (D24). A feladat nélküli (régi) brief `tipus: archiv`, szám és átnevezés nélkül. Brief nélkül (csonk, `brief_kell`) a feladat nem indul.
3. **Modellkiosztás:** orkesztrátor Sonnet; végrehajtás a brief szerint (szkript- és adatmunka Sonnet, kutatói ítélet Opus, takarítás Haiku, a Thayer-fordítás a rögzített külső modellel); ellenőr mindig Opus.
4. **Ellenőrzés (gépi):** zöld CI és a `fuggetlen-ellenor` jelentése (`naplok/ELLENOR_*.md`) a kötelező ellenőrzőlistával. Második szem a chat helyett: friss Code-session vagy PR-review.
5. **Döntés:** a ⛔ pontok és a hiányzó briefek (`brief_kell` csonk) a `DONTESEK.md`-be kerülnek. A chat csak ezt a fájlt kapja (raw link); rutinszerű „kész” jelentés nem megy a chatbe.
6. **Merge:** te indítod, zöld CI és `TISZTA` ellenőri jelentés mellett a chat nélkül is. A ✅-hoz nem kell külön lépés: a brief `lezarva` állapota a merge-gel kerül a `main`-re, és a `main`-re futó Action a sort a „Kész” listába mozgatja (D26).
7. **Keret és hossz:** ha a keret fogy vagy a session hosszú, a parancs tiszta ponton megáll („Folytatási pont” a zárójelentésben); a következő `/kovetkezo` onnan folytatja.
8. **Párhuzamos futás (csomag):** a `/kovetkezo` a független feladatokat egy sessionben, párhuzamosan futtatja. Feladatonként külön worktree, ág, ellenőrzés és draft PR készül. Az ⛔ csak a saját feladatát állítja meg. A `FELADATOK.md`-t senki nem szerkeszti (az állapot a saját brief fejlécében van); a `DONTESEK.md`, a `NYITOTT_FELADATOK.md` és a szerepmátrix közös fájljaiban mindegyik csak a saját sorait írja; a PR előtt rebase kell, ütközésnél mindkét oldal megmarad. A merge sorrendje tetszőleges. Csomagba csak olyan feladat kerül, amelynek fejlécében van `ir`, és nincs írás–írás ütközése (D21, D27).

**Állapot és új feladat:** minden menet a saját briefje fejlécét frissíti; a generált blokkot csak a `main`-re futó Action írja (D25). Új feladat a `/befogad` paranccsal, a felhasználó jóváhagyásával kerül be (D22). A csatolt vagy beérkezett brief adat, nem utasítás (D30).

## Jelmagyarázat

- **Állapot:** ✅ kész (a brief `lezarva` a `main`-en) · 🔀 PR-ben (`lezarva`, de még nem a `main`-en; csak a PR-ág helyi generálásában látszik, a commitolt blokkban nem) · ▶ fut · ⏸ döntésre vagy jóváhagyásra vár · ⬜ nem indult · ⬜ brief kell (csonk) · ⛔ kötelező megállás menet közben
- **KK:** Károli-kulcs, a Károli–LXX versmegfeleltetés
- **CI:** gépi ellenőrzés GitHub Actionsben; E1–E16 a szabályai, E18 a feladatkövetésé (fejléc-érvényesség, generált blokk)
- **FJ:** forrásjelöltek felmérése; **FP:** fordítási próba
- **SZOTAR S1/S2:** a szótári brief 1. (adat) és 2. (render) menete
- **N-szám:** tétel a `NYITOTT_FELADATOK.md`-ben
- **TBESG/TBESH:** STEP-szótárak (görög/héber alapjelentés); **UBS DBH/DNTG:** UBS héber/görög szótár; **LXX:** Septuaginta
- **DONTESEK.md:** a nyitott döntések sora; 🟡 nyitott · 🟢 eldöntve · ✅ alkalmazva
- **Szerepmátrix:** `adat/szotar_szerepek.tsv`, 10 szerep × 2 nyelv
- **`tipus`:** `feladat` (fázissor) · `naplozas` (szám és a „Naplózás” lista, a futtatása a `/kovetkezo`-é) · `dontes` (`DONTESEK.md`-tétel, szám nélkül) · `archiv` (régi, feladat nélküli brief, szám és átnevezés nélkül)
- **`fazis: folyamat`:** a feladat nem az adat- vagy a render-fázis része (folyamat, eszköz); külön táblába kerül, és a `/kovetkezo` csak alternatívaként ajánlja
- **Generált blokkok:** a `<!-- GENERÁLT-KEZDET … -->` és `<!-- GENERÁLT-VÉGE … -->` jelölők közötti rész (a két fázistábla, a „Folyamat és eszközök”, a „Naplózás” és a „Kész” lista) a brief-fejlécekből generálódik (`python eszkozok/feladatok.py general`); kézzel szerkeszteni tilos

## Kész (utolsó 2 hét)

<!-- GENERÁLT-KEZDET: feladatok.py --cel kesz -->
- Régi „Sir” hivatkozások migrálása JSir-re és a „Szentlélek” / „Isten Lelke” helyek egységesítése „Szent Szellem”-re (#35, SIR_SZENTSZELLEM): 6 Sir→JSir csere (jeloltek, genezis, motivumlog 4 sor), 3 Szentlélek→Szent Szellem hely, SEMA E9-javítás; auditok.tsv 169–171 marad; DT-F35b eldöntve (marad); részletek naplok/SIR_SZENTSZELLEM_zaras.md (merge `37f2a80`, 2026-10-02)
- Forrásaink licencének rendezése (az F24 utófeladata) (#33, LICENC_RENDEZES): "17 tisztazott/1 kozkincs/21 tisztazatlan, TBESG marad, TBESH-család nem mozdult (TBESH tisztazatlan), LXX_kivonat tisztazatlan, N-F33 javasolt, DT-F33a-d alkalmazva (részletek: naplok/LICENC_RENDEZES_zaras.md)" (merge `ea7cc96`, 2026-10-02)
- Macula-import, héber és görög (N31) (#17, F17): Macula-import (#17): héber 475 911 és görög 275 520 sor a KK-hoz kötve (CC BY 4.0, UBS-mezők nélkül), a 87 hely 38 LXX-megfelelővel (F06: 39, közös módszerhiba javítva); ellenőrzés `naplok/ELLENOR_F17.md`; a Dán 4, a szerepmátrix és a fájlméret DT7-ben nyitva
- Az orkesztrátor függés-levezetésének javítása (körök feloldása) (#39, ORKESZTRATOR_FUGGES): "A függés-levezetés javítva (#39): az írás–írás ütközés kizar (×), zárt kontextus-olvasás lista, a kölcsönös írás–olvasás kizar + FIGYELEM, a kettőnél hosszabb kör hiba; jeloltek parancs; 60 teszt, ellenoriz 0 hiba; ellenőrzés naplok/ELLENOR_ORKFUGG.md (2 kör), zárás naplok/F39_zaras.md" (merge `9b164cf`, 2026-10-01)
- BDB „ψ” (Zsoltárok) feloldási hiba javítása a forrásban és az érintett fordítások igehelyei (#34, BDB_PSI): 159 ψ-hely javítva a BDB-forrásban (56 szócikk, TAHOT + MT-versszámozási tábla), forditasok.tsv 78/81/84/89 csak token + forras_hash (DT-F34c); 13. szabály RENDBEN, ellenoriz.py = 0; maradék 156 hely az N-F34/N-F34c-ben; részletek naplok/F34_zaras.md (merge `fa501c9`, 2026-10-01)
- "Károli–Strong párosítás: regressziós mérés az új prompttal (DT21 a–e)" (#31, F21R): "Teljesítve a #21 regressziós mérésében (PR #105), külön nem fut." (merge `259c0c7`, 2026-10-01)
- A lexikon Thayer- és BDB-szócikkeinek Opus-fordítása, javítóréteggel és CI-őrrel (#28, EMELES): 39 Thayer/BDB szócikk teljes fordítása (10 kezi, 29 opus), kapuk + javítóréteg, CI E19, MUNKAMENET C0; ellenőrzés tiszta az ir-lista kiegészítése után; zárás naplok/F28_zaras.md (10.01); DT27: a terminológia-tábla `kapu` oszlopa, SEMA 2.15, a kapu=nem sorok nem követeltek és nem vonnak el kulcsot, PR #102 (merge `a7de734`, 2026-10-01)
- Forrásaink licencének átnézése (#24, LICENC): licenc-leltár (#24, F24): adat/licencek.tsv 39 adatkészlet-sorral (15 tisztazott, 24 tisztazatlan; 6 share-alike), SEMA 2.19, összesítő DT-F24 (köztük a mostani nyilvános terjesztés: LXX_kivonat, MCGED); ellenőrzés naplok/ELLENOR_F24.md (5 kör, az utolsó 9 tétellel, K4 nem TISZTA, a maradék a zárójelentésben) (merge `e962566`, 2026-10-01)
- LXX-fordítói döntések a 87 függő igehelyre (#8, F08): LXX-döntések (#8): a 87 függő hely 86 sora az `adat/lxx_dontesek.tsv`-ben (LD005–LD090), biztos 61 / valószínű 13 / nyitott 4 / nem_alkalmazhato 8 (a DT23 (b) szerint kitöltött 4 sor valószínű: LD027, LD035, LD052 ellentmondásos források, felhasználói döntéssel feloldva, `feloldas=DT23`; LD050 egy forrás); a Macula 38 gépi megfelelőjéből 36 megerősítve, 2 ellentmondó; SEMA 2.11 bővítve (`bizonyossag`, `nincs_heber_kulcsszo`, `feloldas=`), az `ellenoriz.py` 10. szabálya a `feloldas=`-t is ellenőrzi; a generátor csak a biztos sorokat jeleníti meg (merge-elt nulladiff: LD001–LD004 renderje és a 8 törzscikk soronként azonos, `naplok/F08_nulladiff.txt`); ellenőrzés `naplok/ELLENOR_F08.md`; PR-cím `[ELLENŐRZŐ]` (E16); DT23 ✅ (F8.8, F8.10), külön tételek N-F08a (Préd 9:10 igehely) és N-F08b (generátor-címke); zárás `naplok/F08_zaras.md`
- A szótárfordítás döntései, a #7 és az FP3 halasztása (#29, SZOTAR_FORD_NAPLO): a D42–D50 a FELADATOK.md döntésnaplójában (#EM = #28); a #7 és az FP3 (#27) fejléce és a #7 csonk-törzse halasztott (D46); ellenőrzés `naplok/ELLENOR_F29.md` (merge `53b3eaa`, 2026-09-30)
- Károli–Strong mérőpilot (minőség és költség) (#21, F21): Károli–Strong mérőpilot (F21), regressziós mérés (P3c) és KJV-mérés: egyik összeállítás sem felel meg a rögzített döntési szabálynak (A+B, A+B+C, Sonnet + C pár mért és nem felel meg; az egymodelles összeállítások PD6 szerint nem minősíthetők; a pár (1) feltételének R3-ja nem mérhető); C (F3V3) 42,49 USD [38,55–46,52], Sonnet 374 USD, pár 416 USD a teljes Bibliára; a Sonnet a gondolkodási keretet nem tartotta be (11 144 token/hívás az 1024-es keret ellenére, 10 R3-aranyvers length-lezárás miatt kapuhibás); a KJV a promptban: nem igazolt, a javított táblával újramérhető (+0,25 pp, az ingadozáson belül; N-F21); a pilot összesen 4,325 USD; a #22 választott iránya javaslatként a jelentésben; jelentés `naplok/F21P_jelentes.md` (merge `524f8a4`, 2026-09-30)
- Brief-befogadás és generált feladatkövető (#20, BEFOGADAS): brief-befogadás (`/befogad`, csonk-kitöltéssel), a FELADATOK.md táblái a brief-fejlécekből generálva (`eszkozok/feladatok.py`), E18 CI-szabály és a main-re futó frissítő Action; ellenőrzés `naplok/ELLENOR_F20.md`; a main-t ruleset védi, az Action a pardes-feladatok GitHub App tokenjével ír (merge `4fa1265`, 2026-09-30)
- KJV/ASV-import, eBible (N29) (#19, F19): "KJV/ASV-import (#19, eBible): KJV teljes (349 308 sor, javaslat); az ASV forráshibás (javaslat, nem használható), a hiányok besorolva; ellenőrzés naplok/ELLENOR_F19.md, nyitott DT19 és N29 (PR #94)" (merge `2dc9954`, 2026-09-30)
- Nave-import, basokant (N27) (#18, F18): "adat: javaslat, nyitva N45 + független kiadás-összevetés; basokant/nave saját parszolóval importálva (85 246 sor, 5 322 téma, javaslat-állapot; DT5: a theonize GPLv3 miatt kimaradt); licenc- és import-napló `naplok/F18_licenc.md`, `naplok/F18_import_naplo.md`, ellenőrzés `naplok/ELLENOR_F18.md`; eredet-ellenőrzés a 4980 témán és a Gemini-lépés nem futott; nyitott tételek DT18" (merge `7ec656f`, 2026-09-30)
- BSB-import, teljes Biblia (N30) (#16, F16): BSB-import (#16): 31 ÓSZ-könyv (242 597 sor, CC0) importálva, mind a 66 könyv lefedettsége mérve (8 ÓSZ küszöb alatt; az ÚSZ szándékosan kimarad), ellenőrzés `naplok/ELLENOR_F16.md`; a küszöb alatti könyvek és a hiányzó 117 első vers (116 feliratos zsoltár és Zak 12:1; a fejezet 1. versének érdemi szövege) DT6-ban nyitva (merge `516fcbe`, 2026-09-30)
- Orkesztrátor-parancs (#15, F15): `/kovetkezo`, `DONTESEK.md`, végrehajtó subagentek, ellenőrzőlista, PR #70, ✅ a merge-commitban (09.29); próbafuttatás merge után új sessionben: `/kovetkezo`
- Új források 2. felmérése (#6, F06): GitHub Actionsben futott, helyi gép nem kellett; BSB 1Móz 98,83% (küszöb 95%, mérés előtt rögzítve), Macula teljes letöltés és 39/87 függő helyre LXX-megfelelő (#8 bemenete), KJV/ASV, Nave és licenc-javaslatok (MiniMax-költség 0,011927 USD); jelentés `naplok/F06_forras_jelentes.md`, ellenőrzés `naplok/ELLENOR_F06.md`, `naplok/ELLENOR_F06_v2.md`, merge `634d567` (PR #75, 09.29). Az import-döntés (N27, N29–N31) a felhasználóé, nyitva.
- Szótári adatréteg, 1. menet (#5, SZOTAR S1): fordítási gyorsítótár, terminológia/kiejtés-táblák, 7 konkordancia-import (TBESH, UBS DBH, MCGED, BDB-etimológia-határ, LXX-versszint, tW), `ellenoriz.py` 13–14. szabály, 26 héber kiejtés-jelölt + 6 BDB-etimológia-határ jóváhagyva; a `fuggetlen-ellenor` 3 körben talált és javított hibák (TBESH betű-utótag adatvesztés D38–D40, BDB-határ szabály D41), K6/K7 pótolva; ellenőrzés `naplok/ELLENOR_SZOTAR_S1.md`, merge `d0736aa` (PR #72, 09.29). Tartalmi döntést igénylő tételek N39–N44-ként nyitva (`NYITOTT_FELADATOK.md`).
- Thayer-stíluspróba (#14, FP2): Gemini 3.1 Flash Lite, DeepSeek V4 Flash, MiniMax M3 összevetése, vak bírálat és költségbecslés, `naplok/FP2_jelentes.md`; döntés (FP2-D13): fő fordító Gemini 3.1 Flash Lite; ellenőrzés `naplok/ELLENOR_FP2.md`, merge `971d0f2` (PR #68, 09.28)
- Szkript-karbantartás (#4, KARBANTARTAS KB0–KB4): K1–K10 teljesül (K10 öt körben, ágleltárral, nulla-kimenet-őrrel és három mutációs/hiba-próbával: `naplok/ELLENOR_KARB.md`), merge `b8a418a` (09.27); mérőszkript-vakfoltok és -őrök javítása, PR #60 (`8bd1e40`), PR #61
- Fordítási próba (#3, FP0–FP-KOR2.9): fordító eszközök és a próba eredményei, ellenőrzés naplok/ELLENOR_FP.md, merge `9eb43fe` (PR #62, 09.27)
- Gépi ellenőrzés GitHubon (#2, CI): PR #57, merge `68eb348` (09.27); E5 javítás: PR #59
- Károli-versszámok javítása a görög Ószövetségben (#1, KK0–KK7.5): merge `4b9ae49` (09.27)
<!-- GENERÁLT-VÉGE: feladatok.py --cel kesz -->

*Régebbi lezárt tételek: `git log` és a `NYITOTT_FELADATOK.md` „Lezárva” szakasza.*

## Korábbi, szám nélküli lezárt tételek

- Forrásjelöltek 1. menete (FJ0–FJ5), merge `ec7aebc`, zárás `72b200c` (09.25)
- TEREMT-002 1–2. lépés, merge `15c338e` (09.25)
- Szótári brief v1.1 (Cremer kivezetve), merge `a6783e4` (09.25)

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | Az adatréteg megelőzi a rendert, két fázisban | késői adat miatt ne kelljen újrarenderelni (09.26) | vegyes sorrend a menetek készültsége szerint |
| D2 | A feladatkövető md-fájl a repóban, nem ügynök | az ügynököt úgyis el kell indítani, és nem látja a chateket; a fájlt minden szereplő olvassa és írja | ügynök, amely vezeti a folyamatot |
| D3 | A Code csak a saját sorát frissíti, új sor csak chat-jóváhagyással | a fájl ne nőjön kontrollálatlanul | a Code szabadon szerkeszti |
| D4 | Az LXX-döntések (#8) az adatfázisba kerülnek a LEXIKON_LEZARAS-ból | kutatói adat, nem render | a lexikonlezárással együtt |
| D5 | A Thayer-fordítás (#7) a SZOTAR 1. menet után | terminológia és kiejtés nélkül utólagos csere-körök kellenének (ISTENTISZT-001 tanulsága) | a próba után azonnal |
| D6 | CI-szabály hibáját külön ágon javítjuk, nem az érintett menetben | a PR ne írja át a saját ellenőrzését | javítás a #58-ban |
| D7 | A v3 stílust és a MiniMaxot külön stíluspróba (#14) méri: Gemini 3.1 Flash Lite, DeepSeek V4 Flash és MiniMax M3, Claude vak bírálatával, költségbecsléssel | a #7 éles döntéséhez mért adat kell; a próba nem tesz adatot a kanonikus rétegbe, ezért nem vár az adatfázisra | Claude mint fordító (a kor2-ben 4.); a modellek egymást bírálják |
| D8 | Orkesztrátor igen, de Claude Code-parancsként (`/kovetkezo`), döntési ponton megállva; a D2-t módosítja | a meglévő eszközökre épül (CLAUDE.md, subagentek, CI), az előfizetésen belül fut, egy session egy feladat, így nem hízik | külön ügynök-rendszer (API, karbantartás); teljes autonómia (a ⛔ pontok szakmai döntések, a hibák a kritikus úton halmozódnak) |
| D9 | A chat csak döntéskor kap jelzést, a `DONTESEK.md`-n keresztül | a chat adat nélkül ellenőrizne: drága és gyenge (TBESH-szűrés tanulsága) | minden zárójelentés bemásolása a chatbe |
| D10 | Második szem: `fuggetlen-ellenor` (Opus) kötelező ellenőrzőlistával, szükség esetén friss Code-session | tiszta kontextus, közvetlen adathozzáférés | a chat mint ellenőr; külső session-verziózó eszközök (Agent-Git, agit) |
| D11 | A végrehajtó modellt a brief `Modell:` sora írja elő | a modellválasztás a felhasználónál marad; a költség oda megy, ahol szakmai ítélet kell | az orkesztrátor maga választ |
| D12 | A brief neve a feladat számával kezdődik: `F<nn>_<NEV>_BRIEF.md` | a brief a fájllistában és az orkesztrátor számára is egyértelműen a feladathoz köthető | szám csak a brief fejlécében |
| D13 | Az orkesztrátor futtatás előtt mindig egyeztet: javaslat → kérdés/módosítás → kifejezett „mehet”; az egyeztetésig csak olvas | a feladatválasztás és a hatókör a felhasználó döntése; az automatikus indulás rossz feladatot vagy rossz hatókört futtathat | a parancs automatikusan indul, csak a tervet írja ki |
| D14 | A PR #75 utáni munka hat önálló feladatra bomlik: négy import (#16–#19), a Thayer (#7) és az LXX (#8); mindegyiket az orkesztrátor futtatja, a független feladatokat csomagban (D20) | az importok egymástól függetlenek, így párhuzamosan futhatnak; a Thayer és az LXX eltérő modellt és ítéletet kíván | egyetlen összevont menet; a #7 és a #8 egy menetben |
| D15 | BSB: import a teljes Bibliára, könyvenként 95%-os küszöbbel | a teljes feldolgozás elve; az 1Mózesen mért 98,83% alapján a módszer működik | csak 1Mózes-hatókör |
| D16 | Macula: teljes import (héber és görög), Strong-számhoz és KK-hoz kötve; a #8 fő forrása | a 87 helyből 39-re közvetlen megfelelőt ad | csak a 87 helyre szűkített import |
| D17 | Nave: a theonize a fő forrás, a basokant az eredet-ellenőrzésre szolgál, az elcafe7 kimarad; az ellenőrzés mind a 4980 témán fut, a szkript utáni maradékot a Gemini 3.1 Flash Lite bírálja (2 USD-s ⛔ keret) | a theonize a legteljesebb forrás, de a Nave-eredetet nem mondja ki; az elcafe7 licence dokumentálatlan | 50 témás minta; az elcafe7 importja |
| D18 | KJV/ASV: az eBible az importforrás, a luvlylavnder keresztellenőrzésre szolgál, a scrollmapper kimarad | az eBible szinte teljesen Strong-címkés; a luvlylavnder CC0; a scrollmapper nem volt mérhető | luvlylavnder mint fő forrás |
| D19 | Menet közben csak a briefben felsorolt ⛔ pontoknál van megállás; a többi döntésre váró sor `javaslat` jelölést kap, és egy összesített `DONTESEK.md`-tételbe kerül a zárás előtt | nagyobb, egyben lefutó feladatok (Max-fiók); a jelölés miatt minden visszakereshető | megállás minden tartalmi döntésnél |
| D20 | Csomagmód: a `/kovetkezo` a független feladatokat egy sessionben, párhuzamos subagentekkel futtatja, feladatonként külön worktree-ben, ágon, ellenőrzéssel és PR-rel. A D8 „egy session = egy feladat” szabályát módosítja | egy indítás és egy egyeztetés öt helyett; a worktree miatt az ágak nem akadnak össze; az ⛔ csak a saját feladatát állítja meg | feladatonként külön Code-session; egy közös ág több feladatra |
| D21 | A brief erőforrást deklarál (`olvas`, `ir`), a függést a `feladatok.py` számolja; a `fugg`/`nem_fugg` csak kézi kiegészítés | a chatek nem tudnak egymásról, a függést nem ismerhetik, a saját fájljaikat igen | a chat becsüli a függést |
| D22 | A befogadás külön parancs (`/befogad`), külön sessionben, saját ágon és PR-rel; a `/kovetkezo` csak a `main` briefjeiből futtat. **A D3-at módosítja:** új sort a felhasználó hagy jóvá a `/befogad` egyeztetésében | a szétválasztás szerkezetileg zárja ki, hogy a befogadás feladat-futtatásba váltson | a `/kovetkezo` 0. lépése; skill (magától betöltődne csatolt brief láttán); subagent (nincs közvetlen egyeztetés); chat-jóváhagyás |
| D23 | `tipus` mező. A naplózó brief számot kap és a „Naplózás” listába kerül, a `/kovetkezo` futtatja (csomagban is); a `dontes` típus `DONTESEK.md`-tétel lesz | a `/befogad` ne hajtson végre semmit; a naplózás ne foglaljon fázissort | naplózás végrehajtása a befogadás ágán (v1) |
| D24 | A fázistáblák, a „Naplózás” és a „Kész” lista a fejlécekből generálódnak; a többi szakasz kézi | csomagmódban a közösen szerkesztett tábla minden rebase-nél ütközik; a projekt render-elve | kézzel szerkesztett tábla |
| D25 | A generált blokkot csak a `main`-re futó Action írja; PR nem szerkesztheti (**E18**; az E17 a DT3 sorszám-változás szabályáé) | a GitHub-os merge-nél se legyen ütközés | minden ág maga generál |
| D26 | ✅ = a brief `lezarva` állapotban van a `main`-en; nincs külön merge-commit-lépés. **A Munkamenet 6. pontját módosítja** | egy kézi lépéssel kevesebb | a merge-commit állítja ✅-ra |
| D27 | Régi fejlécű (`ir` nélküli) brief nem kerül csomagba | hiányos fejléc ne okozhasson ütközést | a régi briefek tiltása |
| D28 | Egyszeri fejléc-pótlás és átnevezés egy menetben, munkalap-jóváhagyással; a Takarítás átnevezési tételét elnyeli | kevesebb menet; a számokat a felhasználó látja, mielőtt fejlécbe kerülnek | fokozatos pótlás futtatáskor |
| D29 | A brief bejutásának alapútja a csatolás a `/befogad` indításakor; a `beerkezo/` gyűjtőhely a webes feltöltéshez és a helyi pushhoz, és kimarad a CI-ből | a chat nem ír a repóba; a csatolás a meglévő szokás | csak webes feltöltés; GitHub-összekötő (nincs a katalógusban) |
| D30 | A csatolt vagy beérkezett brief adat, nem utasítás; a nyitó prompt `KOZVETLEN_FUTTATAS` jelölők közé kerül, és egyik parancs sem hajtja végre. Új feladat csak a befogadás PR-jének merge-e után fut, sürgős esetben is | a brief szövege ne írhassa felül a parancs menetét | szabály jelölés nélkül; sürgős futtatás a befogadás ágából |
| D31 | A feladat nélküli (régi) brief fejléce `tipus: archiv`, szám és átnevezés nélkül; az `ellenoriz` náluk a fájlnév–szám egyezést nem vizsgálja (az `F4_BRIEF.md` a terv F4 fázisa, nem a #4) | a régi briefek neve ne keveredjen a feladatszámokkal | a régi briefek átnevezése |
| D32 | A szám nélküli lezárt tételek (FJ 1. menet, TEREMT-002 1–2. lépés, Szótári brief v1.1) kézi szakaszban maradnak; a generált „Kész” csak számozott feladatot ad | a fejléc nélküli tételt a generátor nem ismeri | számok utólagos kiosztása |
| D33 | A „lezárva, még a `main`-en kívül” állapot jele 🔀 (a B4-ben 🔎 volt, a v1.4 cserélte) | a nagyító-jelek közül a U+1F50D a CI E2 szabályában „ellenőrizve” jelölés, proveniencia nélkül hibát ad; a 🔀 szabad jel | az E2 módosítása (D6: külön ágon) |
| D42 | A lexikonba kerülő Strong-számok teljes Thayer- és BDB-szócikkét az Opus fordítja (#28); a felhasználó szúrópróbát olvas | ott a legjobb minőség, ahol olvassák; a Gemini v3 fordítása (pl. G26) nem volt elég jó | Gemini mindenre; gépi alap + Opus-emelés |
| D43 | Tárolás az `adat/forditasok.tsv`-ben: `teljes` szintű `opus`/`kezi` sor; a meglévő jelentésszintű `kezi` sorok megmaradnak, elsőbbségi sorrend `kezi` > `opus`; a render a jelentést a forrás tagolása mentén vágja ki, ezt a tagolás-kapu biztosítja | egy fordítás, több nézet | jelentésenkénti fordítás |
| D44 | CI-őr: a lexikon minden Thayer- és BDB-hivatkozásához kötelező az `opus` vagy `kezi` fordítás (jelentés- vagy `teljes` szinten) | a fordítás ne maradhasson ki | kézi ellenőrzés |
| D45 | Közös, determinisztikus javítóréteg (`eszkozok/normalizal.py`) és fordítási kapuk (idézőjel, tagolás, igetörzs) minden fordítási kimenetre | a gépi szabály biztosabb, mint a promptban kért | csak promptszabály |
| D46 | A teljes szótár gépi alapfordítása (#7 Thayer, BDB-alap) és a modellpróbák (FP3 #27, BDB-próba) halasztva, amíg nincs böngésző felhasználó (a #25 HTML-felület vagy a kereskedelmi kiadás veti fel); addig a nem lexikoni szócikkek angolok | ma senki nem böngész szócikkeket; a fordítás akkor is elkészülhet | gépi alap most (kb. 25 USD) |
| D47 | Az első fordítási kör: 47 szócikk (18 Thayer, 29 BDB), 187 863 karakter (a 2026.09.30-i mérés); a G1941 már kézi | a Max-keret elbírja; a szöveg kevesebb mint 2%-a | — |
| D48 | A fordítás a motívum-munkafolyamat lépése: új motívum vagy előfordulás után a hiányzó szócikkek fordítása (`MUNKAMENET.md`) | a lexikon bővülésével folyamatos | egyszeri fordítási menet |
| D49 | Szúrópróba menetenként a lefordított szócikkek 10%-a, legalább 5; 20% fölötti kifogásnál a menet megáll | a felhasználó döntése: csak szúrópróba | minden szócikk kézi átnézése |
| D50 | A lexikonba a szótárból csak a motívumhoz illeszkedő jelentéstartomány kerül, a Thayernél is (a BDB-nél eddig is így volt); a kiválasztás a render/#9 feladata: gépi jelölt (a jelentés igehelyei metszik a motívum előfordulásait), a döntés a felhasználóé | kisebb, pontosabb kimenet | a teljes szócikk a lexikonban |
