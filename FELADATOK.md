# FELADATOK.md — feladatkövető

*v1.1 · 2026.09.28 · `main` = `47fca73` (a `claude/general-teremt002-datum` PR mergelése után frissítendő) · Ez az egyetlen fájl, amit a chat egy új beszélgetés elején elolvas. A részletek a briefekben és a `NYITOTT_FELADATOK.md`-ben vannak; ide csak az állapot, a függés és a következő lépés kerül. Munkafolyamat: `/kovetkezo` orkesztrátor, döntések a `DONTESEK.md`-ben.*

## Alapelv: előbb az adatréteg, utána a render

Amíg nem látjuk, mit adnak az új források, nem foglalkozunk rendereléssel (lexikonoldal, törzscikk, migráció), mert a késői adat miatt mindent újra kellene generálni. Emiatt két fázis van, és a 2. fázis egyik feladata sem indul, amíg az 1. fázis el nem készül.

**Kritikus út:** #1 és #2 → #4 → #5 → #7 → #9 → #10

## 1. fázis — adatréteg

| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Következő lépés | Hol |
|---|---|---|---|---|---|---|
| 5 | Szótári adatréteg, 1. menet (SZOTAR S1) | a szerepmátrix hiányzó sorai adatként: fordítási gyorsítótár, terminológia, kiejtés-táblák, UBS DBH, TBESH, Mounce, Translation Words | ⬜ S0b kész, 1. menet S1.1-nél blokkolva volt, a blokk feloldva (D30) | #1, #2, #4 | Blokk feloldva: az 1. menet nulla-diff próbája (K4) `git status --porcelain lexikon/`-ról `eszkozok/nulladiff.sh`-ra vált (D30) — a `general.py --cel lexikon --ir` a TEREMT-002 hiányzó `res_forras.tsv` sora miatt szállt el (`main`-en is), és a `TS` mező a mai nap miatt sosem adott volna üres diffet. A `claude/general-teremt002-datum` PR mergelése után az S1.1 (`claude/szotar-s1-menet`) a SZOTAR_BRIEF.md v1.4 1. menet promptjának 1. lépésétől folytatódik, a `nulladiff.sh`-val. | `SZOTAR_BRIEF.md` v1.4, `naplok/SZOTAR_S0b_jelentes.md` |
| 6 | Új források 2. felmérése **helyi gépről** (FJ 2. menet) | döntés a Nave, a teljes KJV/ASV és a BSB importjáról; a Macula lefedettsége | ⬜ nincs brief | — (#5-tel párhuzamosan futhat) | Brief kell. Helyi gépen fusson, mert a cloud proxy blokkolt (N27, N29–N31) | `naplok/FORRAS_jelentes.md` (fejlécébe kell a „felülírva: N27–N29” megjegyzés) |
| 7 | Thayer teljes magyar fordítása (éles) | a görög mélységi szócikk magyarul, adatként | ⬜ nem futott | #3, #5 (terminológia, kiejtés) | **Te:** döntés a v3-ról („természetes hű” stílus a promptban) + költség újraszámítása a teljes Thayer_teljes.tsv hosszeloszlásából (a P6 ~30 USD-ja nem vezethető le, naiv skálázással ~62 USD; ELLENOR_FP.md 1. eltérés) | `FORDITAS_ELES_THAYER_BRIEF.md` v2, csak chatben |
| 8 | LXX-fordítói döntések a 87 függő igehelyre | minden ÓSZ-helyhez LXX-megfelelő (`adat/lxx_dontesek.tsv`) | ⬜ nem futott | #1, #6 (Macula-lefedettség) | Kutatói adatmunka; 58 gépi jelölt tájékoztatásul: `naplok/FORRAS_FJ1_lxx_jeloltek.tsv` | eredetileg a LEXIKON_LEZARAS 4c pontja |
| 14 | Orkesztrátor-parancs (munkafolyamat) | a következő feladatot gép választja és futtatja; a chat csak döntéskor kap jelzést | ⏸ kész, draft PR merge-re vár (`claude/orkesztrator-14`) | — | Merge után próbafuttatás: új session, `/kovetkezo` (elvárt: terv egy konkrét feladatra, vagy a blokkoló `DONTESEK.md`-tétel megnevezése) | `F14_ORKESZTRATOR_BRIEF.md` |

## 2. fázis — render (csak az 1. fázis után)

| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Megjegyzés | Hol |
|---|---|---|---|---|---|---|
| 9 | Szótári adatréteg, 2. menet (SZOTAR S2) | az 1. fázis adatai megjelennek a 8 lexikonoldalon és a 8 törzscikkben | ⬜ | #5, #6, #7 | Ez javítja a törzscikkek elavult Cremer-sorát is (a CI E11 szabálya jelzi) | `SZOTAR_BRIEF.md` 2. menet |
| 10 | 8 lexikonoldal lezárása (LEXIKON_LEZARAS) | mérhetően kész oldalak (L1–L7) | ⬜ | #8, #9 | **Te:** döntés az L6 és L7 feltételről. Ide tartozik N18, N19 | brief csak chatben |
| 11 | Migráció: egy forrásból renderelés (MIGRACIO) | minden motívum a forrásrétegből renderel | ⬜ | #9 | Az M0 felmérés csak olvas, de az eredménye itt kell | brief csak chatben |
| 12 | TEREMT-002 3. lépés (próza, lexikonoldal) | az első natív egyforrású motívum kész | ⬜ | #11 | A tohu/bohu szótári adata az S1-ben készül (D29). | `TEREMT002_KUTATAS_BRIEF.md` |
| 13 | 1Móz 17-től a tanulmányok és a 6 betöltetlen motívum | a Genezis-kiadás tartalma | ⬜ | #10 | döntés 2026.09.21: a lexikonoldalak lezárása után | — |

## Takarítás (bármikor, rövid)

- A `claude/forditas-pilot-brief-3afbbf` ág törlése (csak az FP0 van rajta, ős).
- A chatben készült briefek (#4, #7, #10, #11) commitolása a repó gyökerébe, hogy a chat onnan olvassa őket.
- 72 távoli ág van, ebből kb. 60 régi (2026.09.02–09.11). Egyszeri átnézés, majd törlés.
- E5: a `-` kezdetű törölt sorok (felsorolás) alulszámolása, 68eb348 óta (l. naplok/ELLENOR_CI_E5.md, 2. kör). Rövid CI-javítás külön ágon (D6), legkésőbb a 2. fázis előtt.
- A meglévő briefek átnevezése `F<nn>_…_BRIEF.md` formára `git mv`-vel (a történet megmarad), a hivatkozások frissítésével (`FELADATOK.md` „Hol” oszlop, `CLAUDE.md`, más briefek, CI-konfiguráció, szkriptek: `grep -rn "_BRIEF.md"`). Feladathoz nem köthető brief nem kap számot. Modell: haiku.

## Munkamenet (tokentakarékos)

1. **Indítás és egyeztetés:** új Code-session, `/kovetkezo`. Egy session = egy feladat. A parancs javaslatot tesz a következő végrehajtható feladatra, és veled egyezteti (feladatválasztás, hatókör, modell). Addig semmit nem ír és nem indít; csak a kifejezett „mehet” után futtat.
2. **Egy feladat = egy brief = egy ág.** A brief a repóban van. Neve a feladat kétjegyű számával kezdődik: `F<nn>_<NEV>_BRIEF.md` (pl. `F05_SZOTAR_BRIEF.md`). A fejlécében a feladat száma és a `Modell:` sor (`sonnet` | `opus` | `haiku` | `külső:<név>`). Brief nélkül a feladat nem indul.
3. **Modellkiosztás:** orkesztrátor Sonnet; végrehajtás a brief szerint (szkript- és adatmunka Sonnet, kutatói ítélet Opus, takarítás Haiku, a Thayer-fordítás a rögzített külső modellel); ellenőr mindig Opus.
4. **Ellenőrzés (gépi):** zöld CI és a `fuggetlen-ellenor` jelentése (`naplok/ELLENOR_*.md`) a kötelező ellenőrzőlistával. Második szem a chat helyett: friss Code-session vagy PR-review.
5. **Döntés:** a ⛔ pontok és a hiányzó briefek a `DONTESEK.md`-be kerülnek. A chat csak ezt a fájlt kapja (raw link); rutinszerű „kész” jelentés nem megy a chatbe.
6. **Merge:** te indítod, zöld CI és `TISZTA` ellenőri jelentés mellett a chat nélkül is. A merge-commit a sort ✅-ra állítja, és a „Kész” listába mozgatja.
7. **Keret és hossz:** ha a keret fogy vagy a session hosszú, a parancs tiszta ponton megáll („Folytatási pont” a zárójelentésben); a következő `/kovetkezo` onnan folytatja.

**A `CLAUDE.md`-be kerülő sor:** „Minden menet utolsó commitja frissíti a `FELADATOK.md` saját sorát. Új feladat csak a chat jóváhagyásával kerül bele.”

## Jelmagyarázat

- **Állapot:** ✅ kész · ⏸ döntésre vagy jóváhagyásra vár · ⬜ nem indult · ⛔ kötelező megállás menet közben
- **KK:** Károli-kulcs, a Károli–LXX versmegfeleltetés
- **CI:** gépi ellenőrzés GitHub Actionsben; E1–E16 a szabályai
- **FJ:** forrásjelöltek felmérése; **FP:** fordítási próba
- **SZOTAR S1/S2:** a szótári brief 1. (adat) és 2. (render) menete
- **N-szám:** tétel a `NYITOTT_FELADATOK.md`-ben
- **TBESG/TBESH:** STEP-szótárak (görög/héber alapjelentés); **UBS DBH/DNTG:** UBS héber/görög szótár; **LXX:** Septuaginta
- **DONTESEK.md:** a nyitott döntések sora; 🟡 nyitott · 🟢 eldöntve · ✅ alkalmazva
- **Szerepmátrix:** `adat/szotar_szerepek.tsv`, 10 szerep × 2 nyelv

## Kész (utolsó 2 hét)

- Fordítási próba (FP0–FP-KOR2.9): fordító eszközök és a próba eredményei, ellenőrzés naplok/ELLENOR_FP.md, merge `9eb43fe` (PR #62, 09.27)
- Szkript-karbantartás (KARBANTARTAS KB0–KB4), K1–K10 teljesül (K10 öt körben, ágleltárral, nulla-kimenet-őrrel és három mutációs/hiba-próbával: `naplok/ELLENOR_KARB.md`), merge `b8a418a` (09.27); mérőszkript-vakfoltok és -őrök javítása, PR #60 (`8bd1e40`), PR #61
- Gépi ellenőrzés GitHubon (CI, #2), PR #57, merge `68eb348` (09.27); E5 javítás: PR #59; + E17 (sorszám-változás küszöb, lásd `DONTESEK.md`)
- Károli-versszámok javítása a görög Ószövetségben (KK0–KK7.5), merge `4b9ae49` (09.27)
- Forrásjelöltek 1. menete (FJ0–FJ5), merge `ec7aebc`, zárás `72b200c` (09.25)
- TEREMT-002 1–2. lépés, merge `15c338e` (09.25)
- Szótári brief v1.1 (Cremer kivezetve), merge `a6783e4` (09.25)

*Régebbi lezárt tételek: `git log` és a `NYITOTT_FELADATOK.md` „Lezárva” szakasza.*

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | Az adatréteg megelőzi a rendert, két fázisban | késői adat miatt ne kelljen újrarenderelni (09.26) | vegyes sorrend a menetek készültsége szerint |
| D2 | A feladatkövető md-fájl a repóban, nem ügynök | az ügynököt úgyis el kell indítani, és nem látja a chateket; a fájlt minden szereplő olvassa és írja | ügynök, amely vezeti a folyamatot |
| D3 | A Code csak a saját sorát frissíti, új sor csak chat-jóváhagyással | a fájl ne nőjön kontrollálatlanul | a Code szabadon szerkeszti |
| D4 | Az LXX-döntések (#8) az adatfázisba kerülnek a LEXIKON_LEZARAS-ból | kutatói adat, nem render | a lexikonlezárással együtt |
| D5 | A Thayer-fordítás (#7) a SZOTAR 1. menet után | terminológia és kiejtés nélkül utólagos csere-körök kellenének (ISTENTISZT-001 tanulsága) | a próba után azonnal |
| D6 | CI-szabály hibáját külön ágon javítjuk, nem az érintett menetben | a PR ne írja át a saját ellenőrzését | javítás a #58-ban |
| D7 | Orkesztrátor igen, de Claude Code-parancsként (`/kovetkezo`), döntési ponton megállva; a D2-t módosítja | a meglévő eszközökre épül (CLAUDE.md, subagentek, CI), az előfizetésen belül fut, egy session egy feladat, így nem hízik | külön ügynök-rendszer (API, karbantartás); teljes autonómia (a ⛔ pontok szakmai döntések, a hibák a kritikus úton halmozódnak) |
| D8 | A chat csak döntéskor kap jelzést, a `DONTESEK.md`-n keresztül | a chat adat nélkül ellenőrizne: drága és gyenge (TBESH-szűrés tanulsága) | minden zárójelentés bemásolása a chatbe |
| D9 | Második szem: `fuggetlen-ellenor` (Opus) kötelező ellenőrzőlistával, szükség esetén friss Code-session | tiszta kontextus, közvetlen adathozzáférés | a chat mint ellenőr; külső session-verziózó eszközök (Agent-Git, agit) |
| D10 | A végrehajtó modellt a brief `Modell:` sora írja elő | a modellválasztás a felhasználónál marad; a költség oda megy, ahol szakmai ítélet kell | az orkesztrátor maga választ |
| D11 | A brief neve a feladat számával kezdődik: `F<nn>_<NEV>_BRIEF.md` | a brief a fájllistában és az orkesztrátor számára is egyértelműen a feladathoz köthető | szám csak a brief fejlécében |
| D12 | Az orkesztrátor futtatás előtt mindig egyeztet: javaslat → kérdés/módosítás → kifejezett „mehet”; az egyeztetésig csak olvas | a feladatválasztás és a hatókör a felhasználó döntése; az automatikus indulás rossz feladatot vagy rossz hatókört futtathat | a parancs automatikusan indul, csak a tervet írja ki |
