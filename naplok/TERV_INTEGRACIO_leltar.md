# TERV-INTEGRÁCIÓ — leltár (TI.1)

*Feladatszám nélküli folyamatjavítás (a felhasználó kérése, 2026-10-08: „ne aprózzuk el, véglegesen csináljuk meg”; a zárójelentés „Egyeztetett eltérés” címen rögzíti) · ág `claude/terv-integracio` · kiindulás `origin/main` `ef8f7e5` · 2026-10-08 · ez az 1. lépés (leltár); a döntési lista: `naplok/TERV_INTEGRACIO_dontesi_lista.md`. Az átvezetés (3.) és a zár (4.) a felhasználó döntései után jön; ez a fájl semmit nem ír át.*

**Tárgy.** A három tervdokumentum (`ATALAKITASI_TERV.md.md` = alap; `MUNKATERV.md` és `ADATVAGYON_TERV.md` = kiegészítés, nem fork) feladat-, lépcső- és döntés-elemei, összevetve a `FELADATOK.md`-vel (generált sorok és kézi szakaszok), a briefek fejlécével és szövegével, a `DONTESEK.md` nyitott tételeivel és a #52 TERV_SZINKRON naplójának nem átvezetett tételeivel. A #64 (PR #247, nem mergelt) tartalmát az ágról olvastam (`git show origin/claude/f64-teremt002-proza-proba:…`), átmásolás nélkül.

**A rés oka** (a #52 naplója, 1.3, 2.3, „Nyitott a következő futásra”): a szinkron csak repó → terv irányban vezet át. A terv → feladat irány tételei („a /befogad dolga”, „felhasználói döntés”, „a #11 csonk-kitöltésekor”) a naplóban maradnak, és senki nem hajtja be őket. Ezért a feladatlánc a kiegészítés nélküli alapterv szerint halad.

## 0. Proveniencia

- brief-fejlécek (fázis, állapot, `fugg`, `olvas`, `ir`, `kod`), DONTESEK-állapotok: `scope=F*_BRIEF.md (74 feladat-brief), DONTESEK.md | forras=egyszeri olvasó szkript a scratchpadban (leltar_szamok.py; nem repó-eszköz) | ts=2026-10-08T12:47Z`
- függések, kizárások, régi fejlécek, 1. fázisú jelöltek: `scope=F*_BRIEF.md | forras=python eszkozok/feladatok.py fuggesek; python eszkozok/feladatok.py jeloltek | ts=2026-10-08`
- `kovetkezo`-mezők, „Te:” jelölés, hivatkozott PR-ek merge-állapota: `scope=nyitott F*_BRIEF.md + git log origin/main | forras=egyszeri szkript a scratchpadban (te_mezok.py) | ts=2026-10-08`
- DONTESEK nem ✅ tételei: `scope=DONTESEK.md | forras=egyszeri szkript a scratchpadban (dt_nyitott.py) | ts=2026-10-08`
- a szerepmátrix használata a generátorokban: `scope=eszkozok/lexikon_general.py, eszkozok/torzscikk_general.py, adat/szotar_szerepek.tsv | forras=grep + olvasás | ts=2026-10-08`
- a #64 mérése és a DT-F64a/b: `scope=origin/claude/f64-teremt002-proza-proba (a399e14) naplok/TEREMT002_PROZA_PROBA_meres.md 2., 3., 7. szakasz; DONTESEK.md DT-F64a/b | forras=git show | ts=2026-10-08`
- a nyitott PR-ek: `scope=GitHub | forras=gh pr list --state open | ts=2026-10-08` (egyetlen: #247)
- minden további „van / nincs” állítás: `forras=manual` (olvasás és grep a megnevezett fájlokon), nem lekérdezés.

## 1. Fő számok

| mérőszám | érték | proveniencia |
| --- | --- | --- |
| feladat-brief / ebből nyitott | 74 / 32 (1. fázis 12, 2. fázis 10, folyamat 10) | leltar_szamok.py, ts=2026-10-08T12:47Z |
| csonk (`brief_kell`) a nyitottak közt | 11: #7, #10, #11, #12, #13, #25, #67, #69, #74, #75, #76 | ugyanaz |
| régi fejléc (`ir`/`olvas` hiányzik) | 6: #10, #11, #12, #13, #25, #76 | feladatok.py fuggesek |
| a MUNKATERV 4. szakaszának 8 kódos tervezett feladatából FELADATOK-sor nélkül | 3: SQLITE_EPIT, SZPA_AUDIT, MCP_BUROK (ez utóbbi a DT-M7 szerint szándékosan feltételes) | leltar_szamok.py |
| a kulcs-briefek közül a szerepmátrixot említi | 1 / 12 (#9; nem: #10, #11, #12, #13, #23, #25, #36, #63, #65, #70, #76) | leltar_szamok.py |
| DONTESEK állapot | 🟡 4 (DT-M4, DT-M5, DT-M6, DT57) · 🟢 41 · ✅ 87 | leltar_szamok.py, dt_nyitott.py |
| nyitott brief, amelynek `kovetkezo`-ja elavult (merge-elt PR, kész előfeltétel vagy lefutott lépés) | 4: #22, #23 (a #247 merge-e után), #38, #64 (a main-en) | te_mezok.py |
| **rés összesen** | **44**: döntést igényel **23** (2. szakasz) · gépies **10** (3. szakasz) · „elavult a tervben” **11** (4. szakasz) | ez a leltár (`manual`) |

## 2. Döntést igénylő rések

Mindegyik tétel szerepel a döntési listán (az utolsó oszlop a lista sorszáma).

| # | tétel | forrás (terv, szakasz) | hol hiányzik | javasolt átvezetés | döntés (lista) |
| --- | --- | --- | --- | --- | --- |
| R1 | **ISTENTISZT-001 rekonstrukciója a szerepmátrix szerint** (a)) — az aranyminta maga sem a mátrix szerint épül | ADATVAGYON 18.5 („a szó-lap a mátrix renderelése; a blokkok sorrendje és töltöttsége innen jön”; `allapot` → üres, jelölt blokk); #64 mérés 7. szakasz | FELADATOK-sor nincs; a `lexikon_general.py` 10 generált blokkja a mátrixtól független (a mátrix csak a `modell_epit`-ben és a `torzscikk_general.py` 5. szakaszában él); a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` 2. szakasza Strong → forrás sorrendű, a 9., 12. és (javasolt) 13. szerep hiányzik; a #23 M1, a #10 és a #11 mércéje erre épülne | új feladat: „szerepmátrix-váz” — a generátor a `_TUDOMANYOS` 2. szakaszát szerepenként, mátrix-sorrendben rendereli, a nem adatosított szerep explicit üres blokk; az adatosítás a #9 (és a 13. szerepnél a #22) dolga; a #23 M1 előtt fut. Kör-veszély: #23 M1 → aranyminta → #9-adat → #9 `fugg` #23; a váz (szerkezet adat nélkül) ezt megtöri | 1 |
| R2 | **TEREMT-002 szótári részének újramérése** a rekonstruált aranymintához (f)) | #64 mérés 7. („a szerepmátrix szerinti szótári rész nincs mérve”) | sehol nincs feladat vagy lépés; a TEREMT-002-nek lexikonoldala nincs (`res_forras.tsv`-sor és `lexikon_hivatkozasok`-sor 0, #64 mérés 4.) | a váz-feladat második mintája (próbarender a `generalt_proba/` alá), vagy a #12b, vagy a #23 M1 része | 2 |
| R3 | **Befagyasztás**: régi motívumhoz a #11 előtt ne kerüljön tartalom a régi szerkezet szerint (b)) | ATALAKITASI 0., 1.B; D34, DT28 (egyirányúság); ADATVAGYON 0.2/5 („a motívum-réteg ráépítve”) | nincs szabály; érintett nyitott feladatok: #70 (`tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md` 2/b, Strong-szerinti alszakaszokkal — a mátrix-vázzal ütközik), #55 (forrásbeli állítások javítása a `tematikus_lezart/`-ban), #36 (az éles `lexikon/` újragenerálása a régi blokkszerkezettel), #13 (6 betöltetlen motívum), #63 és #65 (`jeloltek`/`elofordulasok` írása a 8 régi motívumra) | a forrásréteg és az éles lexikon fagy a #11 1. lépcsőjéig; az adatréteg (#63, #65) mehet, mert a DT28 szerint a migráción változatlanul átmegy | 3 |
| R4 | **A #9 szűkítése** a motívumokban szereplő szócikkekre (c)) | ADATVAGYON 16 (#9 függ #7\*, #23, #38\*); D42, D50 | a #9 lágy függése a #38-ra (`adat/forditasok.tsv`\*) és a #7-re; a #9 hatóköre nincs kimondva; a #38 a teljes BDB-t fordítja (8 090 szócikk, a 7. adag következik) | a #9 hatóköre: a 8 motívum Strongjai (ezeket a #28 Opus-fordítással lefedte, D42), `nem_fugg: [7, 38]`; `olvas` + `ADATVAGYON_TERV.md`, `adat/szotar_szerepek.tsv` | 4 |
| R5 | **Fázisszabály 1: a #62 `folyamat`**, de 1. fázisú feladatok várnak rá (d)) | MUNKATERV 4a (#62 „az SQLITE_EPIT előfeltétele”, „eszközök”); FELADATOK D1, Jelmagyarázat („a /kovetkezo csak alternatívaként ajánlja”) | a `feladatok.py jeloltek` szerint a #54, #63 a #62-re vár, a #65 a #62-re és a #63-ra, a #55 ezeken át; a #62 maga nem 1. fázisú jelölt. A #68 (ugyanez a gond) 2026-10-08-án lezárult (merge `31ad9b1`), tárgytalan | a #62 (és a ráépülő #61) `fazis: 1`, vagy a /kovetkezo szabálya: az 1. fázist blokkoló folyamat-feladat 1. fázisú jelölt | 5 |
| R6 | **Fázisszabály 2: a #76 (#25a) a teljes 1. fázisra vár** | ADATVAGYON 21 (a 2. lépcső „könyvenként, nem kell a teljes”; a 4. lépcső a 3.-ra ül); DT-M1 (a #25a nem vár a motívum-rétegre); ADATVAGYON 0.2/5 („1. fázis végig”) | a #76 `fazis: 2`; a D1 szerint a 2. fázis egyik feladata sem indul, amíg az 1. el nem készül — az 1. fázisban áll a #22 (teljes Biblia), a #38 (8 090 szócikk), a halasztott #7 és #27 is. A két terv-mondat egymásnak is ellentmond | a D1 kiegészítése: a #76 az SQLITE_EPIT után indulhat, az 1. fázis lezárása nélkül (a 0.2/5 „végig”-je a kész könyvekre értendő) | 6 |
| R7 | **L2/L7 a lexikonoldal-sablon kapujába és a #10 mércéjébe** (e)) | DT-F64a (2) (PR #247, 🟢: „Alkalmazásra vár: a sablon Minőségi kapujának átszámozása és a #10 mércéje (külön tétel, nem a #64 dolga)”) | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` kapuja ma L1, L3–L6; a #10 csonk `ad`/`kovetkezo`-ja „L2 és L7 nincs”; a #23 M1 előfeltétele „L1–L5, #10”; a DT-F64a még nincs a main-en | a #247 merge-e után: a kapu L1–L7 (L2 napló-jelölés, L7 PaRDeS-rétegfegyelem), a #10 mércéje L1–L7 + a DT2 két rés-szabálya + a szerepmátrix-váz; a #23 M1 előfeltétele ugyanerre | 7 |
| R8 | **Elavult `kovetkezo` („Te:”) mezők és más briefek fejléce** (g)) | — (folyamat); a CLAUDE.md szerint „minden menet a saját briefje fejlécét frissíti” | #22: „Zsoltárok kész (PR #239) … ready és merge (a felhasználóé)” — a PR #239 mergelve (`48caa80`); #38: „a #72 lezárása után” — a #72 kész; #64 (a main-en): „indítás a #23 M0 jóváhagyása után” — lefutott, PR #247; #23: „M1 várja: #12a (#64)” — a #247 merge-ével elavul | a TI 3. lépése egyszeri kivételként frissíti ezeket és a 3. szakasz többi brief-fejlécét (a felhasználó jóváhagyásával), vagy a feladatok saját menete | 8 |
| R9 | **DT-M4**: 13. szerep (Károli-megfelelők + SZPA) és 14. szerep (rejtett/hamis párhuzam) | ADATVAGYON 18.5 javaslat; MUNKATERV 2. | 🟡 nyitott; a 13. szerep a #64 mérés 7. szakasza szerint az aranymintából is hiányzik | 1. felvétel `javaslat` állapottal; a váz üres blokként mutatja | 9 |
| R10 | **DT-M5**: külső `bible-mcp` | MUNKATERV 2.; ADATVAGYON 11., 15./4 | 🟡 nyitott; a DT32 (🟢, 2026-10-05) a chatbeli használatot már szabályozza (a kimenet adatfájlba, briefbe, tanulmányba nem kerül) | lezárás a DT32-re hivatkozva (egyelőre nincs bekötés) | 10 |
| R11 | **DT-M6**: a saját kimenet licence és a kiadás módja | MUNKATERV 2.; ADATVAGYON „Javaslat (licenc és saját réteg)” 3–4. | 🟡 nyitott; a #76 publikálásának feltétele | 1. az első kiadás nem kereskedelmi, blokkonként dataset-kulccsal; a saját réteg licence külön tétel | 11 |
| R12 | **SQLITE_EPIT befogadása** | MUNKATERV 4., 5. (2. hullám); ADATVAGYON 21 (3. lépcső), 22.4 (a SEMA 3. integritási szabályai mint teszt), 19. (KK-alapú vers-kulcs, `szamozas`) | FELADATOK-sor és brief nincs; a #76 `kovetkezo`-ja: „előbb az SQLITE_EPIT feladatként felveendő”; a #76 `fugg`-ja ezért csak `[44]` | `/befogad` (folyamat, Sonnet, `munka: adat`, függ #62); utána a #76 `fugg`-ja kiegészül | 12 |
| R13 | **SZPA_AUDIT befogadása — és a bemenete hiányzik a repóból** | MUNKATERV 4. (1. hullám); ADATVAGYON 10., 21 (6. lépcső) | FELADATOK-sor nincs; a `SZPA_FORDITOI_PROFIL_prompt.md` nincs a repóban (`git ls-files` 0 találat), tehát a brief nem írható meg | a profilfájl a repóba (kézi 0. lépés, mint a #43/#44-é), a feladat a 6. lépcsőben | 13 |
| R14 | **openbible.info-import** (DT34 🟢: „külön feladat”) | ADATVAGYON 19. (teendő), 22.1 (`jeloltek.forras_kereses` új értéke, nem a `kapcsolatok`) | FELADATOK-sor nincs; a DT34 eldöntötte, csak a befogadás és az időzítés hiányzik | befogadás a #76 brief-írásával együtt (a szó-/vers-lap „kapcsolódó igehelyek” blokkja) | 14 |
| R15 | **BDB javító menet a teljes Károli–Strong után** | ADATVAGYON 19. (teendő: „Károli-oszlop minden szócikkhez”), 21 (1. lépcső); MUNKATERV 6. (kockázat) | FELADATOK-sor nincs; a DT54 (✅) szerint „a 7. adag nem vár, a hiányt a javító menet pótolja”, a DT56 (🟢) viszont az utólagos visszaellenőrzést elvetette („a Károli-támasz nélkül fordított szócikket később senki nem fordítja újra”) — a két döntés ellentmond | a felhasználó mondja ki: van-e javító menet (és csak adatblokk-pótlás vagy újrafordítás), vagy a DT54 szövege javítandó | 15 |
| R16 | **Károli-ujjlenyomat (motívum-index előre)** | ADATVAGYON 1.4 | sehol nincs (a #65 az 1.1–1.2-t viszi, a #76 az 1.3-at) | befogadás a #65 után (a variancia-térképre ül), jelentés-kimenettel, adatírás nélkül | 16 |
| R17 | **Idézési szabály a saját prózára** (közkincs/CC BY szó szerint; NC/SA csak hivatkozás) | ADATVAGYON „Javaslat (licenc és saját réteg)” 2. („DT-tétel”) | DT-tétel nincs | DT-tétel a DT-M6-tal együtt, a #76 publikálása előtt | 17 |
| R18 | **VIBE `lepes=MCP` sor** | #52 2. futás 2.3/1., „Nyitott a következő futásra” | a VIBE_GUIDE 5. szakaszában áll; a DT-M3 szerint elavult | átírás: „`lepes` a kutatási lépés kódja vagy `adhoc`, `csatorna=mcp`” | 18 |
| R19 | **A terv → feladat irány gazdája** (a rés gyökéroka) | #52 napló 1.3, 2.3; `F52_TERV_SZINKRON_BRIEF.md` (csak repó → terv) | senki nem hajtja be a terv → feladat tételeket; a #51 `dontes_hatas.tsv`-jében a tervdokumentumokra nincs sor (MUNKATERV 4a, #51 sor) | a #52 minden futása terv → feladat résjelentést is ad (DONTESEK-tétellel), és a #51 gépi őre a tervdokumentumokra is kiterjed | 19 |
| R20 | **Az ATALAKITASI_TERV állapota és hatóköre** | ATALAKITASI fejléc (v9, 2026.09.14, „Státusz: javaslat, jóváhagyásra vár”) | nincs benne a D34/B út, a DT28, a kiegészítő tervek mutatója, az F0–F7 lezárása; nem tartozik a #52 hatókörébe (a #52 csak az ADATVAGYON-t, a MUNKATERV-et és a VIBE-ot vezeti) | új „Állapot és kiegészítések” szakasz + a #52 hatókörébe vétel | 20 |
| R21 | **Célvonal: meddig tart a korpusz, minden motívum végigmegy-e a három szakaszon** | ATALAKITASI 11.1, 10. N8/N9 | DT-tétel nincs; a #13 (1Móz 17-től) éppen a korpusz bővítése | DT-tétel a #13 befogadásakor | 21 |
| R22 | **Arany-készlet a regresszióhoz** (ISTENTISZT-001, HAMART-001 referencia) | ATALAKITASI 11.4 | feladat nincs; az N33 (a CI nem futtatja a `general.py`-t) nyitott; a #23 M1/4 a migráció nulla-diff kategóriáit írja le | a #11 része (a rekonstruált ISTENTISZT-001 a referencia), a CI-rész külön ágon (D6) | 22 |
| R23 | **CCR mérőműszer** (ATALAKITASI D16: „bevezetendő”) | ATALAKITASI 11.6, 10. D16 | nem valósult meg, és nincs feladat; a költségmérés azóta az API-naplókból jön (#21, #77) | elavultnak jelölés a tervben | 23 |

## 3. Gépies rések (döntés nélkül átvezethetők — a 3. lépésben; a brief-fejlécekhez a 8. döntés kell)

| # | tétel | forrás | hol hiányzik | javasolt átvezetés |
| --- | --- | --- | --- | --- |
| G1 | a #11 `olvas:` sora: `ADATVAGYON_TERV.md` | DT-M8 (d) 🟢; MUNKATERV 1., 4a | a #11 csonk fejlécében nincs `olvas` | a #11 csonk fejlécébe most, vagy a `kovetkezo`-ba emlékeztetőként (a csonk-kitöltésig) |
| G2 | a #9 `olvas:` sora: `ADATVAGYON_TERV.md`, `MUNKATERV.md`, `adat/szotar_szerepek.tsv` | ADATVAGYON 18.5, 16.3 („a lexikonoldal = szó-lap elv, a leképezést a #9/#10 végzi”) | a #9 a mátrixot csak írja (`ir`), a terveket nem olvassa | fejléc-kiegészítés |
| G3 | a #10 csonk `olvas:` sora: a három terv, `adat/szotar_szerepek.tsv`, a sablon | ADATVAGYON 16.3, 18.5 | a #10 régi fejlécű (`ir`, `olvas` nincs) | fejléc-kiegészítés (a mérce-szöveg az R7 döntésétől függ) |
| G4 | a #76 `olvas:` sora: `adat/szotar_szerepek.tsv`, `adat/SEMA.md`, `adat/licencek.tsv` | MUNKATERV 4. (OLVASOI_KONKORDANCIA: „szó-lap a szerepmátrix (18.5) szerint”, `kereskedelmi` szűrő) | a #76 csak a két tervet olvassa | fejléc-kiegészítés |
| G5 | a #23 `olvas:` sora: `adat/szotar_szerepek.tsv` | ADATVAGYON 18.5 | a #23 M1 forrássablonja a szótári szakaszt mátrix nélkül tervezné | fejléc-kiegészítés (az M1-szöveg az R1/R7 döntésétől függ) |
| G6 | FELADATOK „Kritikus út” sora | FELADATOK Alapelv (kézi szakasz) | „#1 és #2 → #4 → #5 → #7 → #9 → #10; az LXX-ágon #6 → #17 → #8 → #10”: a #7 halasztott (D46), a #9 `nem_fugg: [7]`, az LXX-ág kész | a mai út: #62 → (SQLITE_EPIT → #76) és #23 (M1) → szerepmátrix-váz → #9 → #11 → #10 (az R1, R5, R6 döntése szerint) |
| G7 | FELADATOK Jelmagyarázat „Szerepmátrix: 10 szerep × 2 nyelv” | `adat/szotar_szerepek.tsv` (22 sor: 1–10 + 12. Nave, mindkét nyelven) | elavult szám | „11 szerep × 2 nyelv” (+ a DT-M4 után 13–14.) |
| G8 | a #52 „Nyitott a következő futásra” tábla 2. sora: a #25 kettéválasztása és a #25a befogadása | #52 napló | a kettéválasztás megtörtént: #25 = #25b (OLVASOI_HTML), #76 = #25a | a következő #52-futás lezárja (a napló a #52-é) |
| G9 | a #12 (TEREMT-002 3. lépés) `ad`-ja és a #12b mérési bemenete | #64 mérés 4. („A #12b-nek”: LXX „függő” helyek, BDB-mezők, `lexikon_hivatkozasok` 0 sor, `res_forras.tsv`-sor hiányzik) | a #12 csonk ezt nem tartalmazza | a #247 merge-e után a #12 csonk `kovetkezo`-jába hivatkozás a mérés 4. szakaszára |
| G10 | a 4. szakasz 11 „elavult a tervben” tétele | — | — | terv-javítás a 3. lépésben (vagy a #52 3. futásában, a 20. döntés szerint) |

## 4. Elavult a tervben (nem feladat; a terv szövegét kell jelölni vagy javítani)

| # | terv, szakasz | elavult állítás | mai állapot (forrás) |
| --- | --- | --- | --- |
| E1 | ATALAKITASI 4.3 dataset-mátrix | „KJV/ASV Strongs: korlátos: csak Genezis, Exodus, Példabeszédek” | a KJV teljes (`KJV_Strongs_teljes.tsv`, #19), az ASV kiesik (D7); a CLAUDE.md sora már javítva (DT-M8 (c)) |
| E2 | ATALAKITASI 2. „Hookok (`.claude/settings.json`)” | commit előtti / írás előtti / írás utáni hookok | nincs hook (`.claude/settings.json` nincs a repóban); a MUNKAMENET B10: „hook nincs (F8 §3)”; a védelem a CI E-szabályaiban; N26 nyitott |
| E3 | ATALAKITASI 10. nyitott kérdések | N3 (tudatos duplikáció), N4 (olvasói pilot), N10 (MCP), N11 (CC BY-SA hatása) | N3 → D34 (a forrás hivatkozik, nem másol); N4 → az OLVASHATÓ 2026.09.21-én megszűnt; N10 → DT-M7; N11 → DT7, DT-F33j, N-F33b |
| E4 | ATALAKITASI fejléc | „Státusz: javaslat, jóváhagyásra vár” | az F0–F7 lefutott (az `F4_BRIEF.md` … `F8_BRIEF.md` `tipus: archiv`, `allapot: lezarva`); az R20 dönt a szakaszról |
| E5 | MUNKATERV 1. és 4a (#25 sor), ADATVAGYON 16., 21. | „a csonk tényleges kettéválasztása és a #25a befogadása külön `/befogad` menet, még nem történt meg”; OLVASOI_KONKORDANCIA számtalan | a #76 = #25a (befogadva), a #25 = #25b |
| E6 | MUNKATERV 4a, 5.; ADATVAGYON 0., 13., 16., 21. (1. lépcső) | „#38: 5 adag kész, a 6. adag a #56 adatblokkjával indul”; „#22: a következő könyv a Bírák” | a 6. adag kész (DT52), a 7. következik (DT56 küszöbbel); a #22-ben a Zsoltárok kész (PR #239), utána DT54 (Bír) / DT57 (🟡) |
| E7 | MUNKATERV 4a státuszok | #37, #40 ⬜; #64 „indítás a #23 M0 után”; #23 „M0 után” | #37 ✅ (`4068a20`), #40 ✅ (`35eee3b`), #68 ✅ (`31ad9b1`), #72 ✅, #73 ✅; #23 M0 kész (DT66, PR #243); #64 lefutott (PR #247 nyitott); új sorok: #67, #69, #70, #74, #75, #76, #77 |
| E8 | MUNKATERV 4. bevezető | „az `ellenor` mindig Haiku vagy Sonnet” | FELADATOK D10: a `fuggetlen-ellenor` Opus (a #52 1.3 és 2.3/5 már jelezte) |
| E9 | MUNKATERV 3. (0. lépcső), ADATVAGYON 15., 19. | „a #38 6. adagja: az M0 5. pont (BDB-gyökcsoport-felmérés) … ellenőrizendő” | lefutott: `naplok/BDB_FORDITAS_gyokcsoportok.tsv`, DT52 (c), N53 |
| E10 | ADATVAGYON 0.4 / MUNKATERV 2. DT-M5 sor | „a bible-mcp: elvetés egyelőre” mint nyitott kérdés | a DT32 (🟢) a chatbeli használatot szabályozza (az R10 dönt a DT-M5 lezárásáról) |
| E11 | ADATVAGYON 18.5 táblája | „11 szerep × 2 nyelv”, 13/14. szerep „javaslat” | a táblázat egyezik a repóval; a 13/14. a DT-M4-től függ — csak a döntés után frissítendő |

## 5. Ellenőrizve, nem rés (átvezetve)

- ADATVAGYON 1.1–1.2 → #65 (eltéréslista, variancia-térkép, a DT-M2 triplet-frissítése); 1.3 (magyar frázis-keresés) → #76 `ad`.
- ADATVAGYON 22.1 (napló gépi alakja, „még nem vizsgált”) → #63; N37 → #62; 12.1/13. (build-blokk) → #56 ✅; DT-M3 → #61; DT-M1 → #76/#25.
- MUNKATERV 0. lépcső: a három kézi fájl bent (#43, #44 ✅); TERV_BEFOGAD lezárva (DT-M8 (a)–(c)); ATALAKITASI 4.7 jelölve.
- MCP_BUROK és az ADATVAGYON 14. író eszközei: szándékosan feltételes (DT-M7), FELADATOK-sor nélkül — nem rés.
- ATALAKITASI F0–F7: lefutott (archív briefek); 4.6 gate-mezők a `motivumok.tsv`-ben (`azonossag_tipusa`, `negativ_kriterium`, `folerendelt_fogalom`); 1.C generátorok (`general.py` célok: `naplo`, `index`, `naplok`, `study`, `nyitott`, `lexikon`, `torzscikk`); az élesítés korlátja a MUNKAMENET B7-ben dokumentált, a teljes egy-forrásos renderelés a #11 (D34).
- DT-M1, M2, M3, M7, M8 🟢 — átvezetve a tervekbe (#52 2. futás) és a feladatokba (#61, #65, #76).

## 6. Kívül eső megfigyelések (nem terv-tétel; a döntési listán nincsenek)

- **DT57** 🟡 (#22 könyvsorrend a BDB-haszon szerint): a #22 saját menetének kérdése, nem terv-elem.
- **41 🟢 tétel** vár alkalmazásra a DONTESEK-ben (köztük DT2 → #10, DT-F26a → #11, DT-F32a/b/c, DT-F42a–i); a terv-integrációt csak a DT2 és a DT-F26a érinti, mindkettő a #10/#11 brief-írásakor alkalmazandó (az R7, ill. a G1 viszi).
- A #64 PR #247 nincs mergelve: az R2, R7, R8 és a G9 a DT-F64a/b-re és a mérési jelentésre hivatkozik, ezek a main-en csak a merge után lesznek meg. A 3. lépés sorrendje ezért: a #247 merge-e előbb.
