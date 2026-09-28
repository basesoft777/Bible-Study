# FELADATOK.md — feladatkövető

*v1 · 2026.09.28 · `main` = `47fca73` (a `claude/general-teremt002-datum` PR mergelése után frissítendő) · Ez az egyetlen fájl, amit a chat egy új beszélgetés elején elolvas. A részletek a briefekben és a `NYITOTT_FELADATOK.md`-ben vannak; ide csak az állapot, a függés és a következő lépés kerül.*

## Alapelv: előbb az adatréteg, utána a render

Amíg nem látjuk, mit adnak az új források, nem foglalkozunk rendereléssel (lexikonoldal, törzscikk, migráció), mert a késői adat miatt mindent újra kellene generálni. Emiatt két fázis van, és a 2. fázis egyik feladata sem indul, amíg az 1. fázis el nem készül.

**Kritikus út:** #1 és #2 → #4 → #5 → #7 → #9 → #10

## 1. fázis — adatréteg

| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Következő lépés | Hol |
|---|---|---|---|---|---|---|
| 5 | Szótári adatréteg, 1. menet (SZOTAR S1) | a szerepmátrix hiányzó sorai adatként: fordítási gyorsítótár, terminológia, kiejtés-táblák, UBS DBH, TBESH, Mounce, Translation Words | ⬜ S0b kész, 1. menet S1.1-nél blokkolva volt, a blokk feloldva (D30) | #1, #2, #4 | Blokk feloldva: az 1. menet nulla-diff próbája (K4) `git status --porcelain lexikon/`-ról `eszkozok/nulladiff.sh`-ra vált (D30) — a `general.py --cel lexikon --ir` a TEREMT-002 hiányzó `res_forras.tsv` sora miatt szállt el (`main`-en is), és a `TS` mező a mai nap miatt sosem adott volna üres diffet. A `claude/general-teremt002-datum` PR mergelése után az S1.1 (`claude/szotar-s1-menet`) a SZOTAR_BRIEF.md v1.4 1. menet promptjának 1. lépésétől folytatódik, a `nulladiff.sh`-val. | `SZOTAR_BRIEF.md` v1.4, `naplok/SZOTAR_S0b_jelentes.md` |
| 6 | Új források 2. felmérése **helyi gépről** (FJ 2. menet) | döntés a Nave, a teljes KJV/ASV és a BSB importjáról; a Macula lefedettsége | ⬜ nincs brief | — (#5-tel párhuzamosan futhat) | Brief kell. Helyi gépen fusson, mert a cloud proxy blokkolt (N27, N29–N31) | `naplok/FORRAS_jelentes.md` (fejlécébe kell a „felülírva: N27–N29” megjegyzés) |
| 7 | Thayer teljes magyar fordítása (éles) | a görög mélységi szócikk magyarul, adatként | ⬜ nem futott | #3, #5 (terminológia, kiejtés), #14 | **Te:** döntés a v3-ról („természetes hű” stílus a promptban) + költség újraszámítása a teljes Thayer_teljes.tsv hosszeloszlásából (a P6 ~30 USD-ja nem vezethető le, naiv skálázással ~62 USD; ELLENOR_FP.md 1. eltérés) · a v3- és modelldöntés alapja a #14 jelentése | `FORDITAS_ELES_THAYER_BRIEF.md` v2, csak chatben |
| 8 | LXX-fordítói döntések a 87 függő igehelyre | minden ÓSZ-helyhez LXX-megfelelő (`adat/lxx_dontesek.tsv`) | ⬜ nem futott | #1, #6 (Macula-lefedettség) | Kutatói adatmunka; 58 gépi jelölt tájékoztatásul: `naplok/FORRAS_FJ1_lxx_jeloltek.tsv` | eredetileg a LEXIKON_LEZARAS 4c pontja |
| 14 | Thayer-stíluspróba modern magyarra: Gemini Flash Lite, DeepSeek, MiniMax (FP2) | döntési alap a #7-hez: v3 stílus, fő fordító és tartalék, költség | ⏸ jelentés kész, felhasználói döntésre vár | — (a #3 a main-ben) | **Te:** döntés a fő fordítóról a `naplok/FP2_jelentes.md` 6. pontja alapján (javaslat: Gemini 3.1 Flash Lite, prompt-cache + 1× önújrapróba); a PR nyitása és a `#7` briefjének v3-ra frissítése | ág `claude/thayer-stilusproba-fp2`, `FORDITAS_STILUSPROBA_FP2_BRIEF.md`, `naplok/FP2_jelentes.md` |

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

## Munkamenet (tokentakarékos)

1. **Új chat-beszélgetés:** csak ezt a fájlt olvasom be (raw URL, néhány KB). Nem töltöm le a teljes repót, és nem kell összefoglalnod, mi történt.
2. **Egy feladat = egy brief = egy ág.** A brief a repóban van, a nyitó prompt benne. A brief fejléce hivatkozik a feladat számára (pl. „FELADATOK #5”).
3. **Code-session:** a Code a menet utolsó commitjában frissíti ennek a fájlnak a saját sorát (állapot, ág, következő lépés). Más sort nem módosít.
4. **Ellenőrzés:** a CI zöld, és a `fuggetlen-ellenor` ügynök jelentése (`naplok/ELLENOR_*.md`) elkészült. A chat csak ezt a kettőt olvassa. Teljes letöltés csak piros CI vagy ügynök által jelzett eltérés esetén.
5. **Visszajelzés a chatnek:** elég annyi, hogy „#5 kész”, vagy a Code záró összefoglalója legfeljebb 20 sorban. Minden más a repóban van.
6. **Merge:** te indítod. A merge-commit ennek a fájlnak a sorát ✅-ra állítja, és a sort a „Kész” listába mozgatja.
7. **Hosszú chat helyett új chat:** ha egy beszélgetés hosszú, nyiss újat. A folytatáshoz ez a fájl elég.

**A `CLAUDE.md`-be kerülő sor:** „Minden menet utolsó commitja frissíti a `FELADATOK.md` saját sorát. Új feladat csak a chat jóváhagyásával kerül bele.”

## Jelmagyarázat

- **Állapot:** ✅ kész · ⏸ döntésre vagy jóváhagyásra vár · ⬜ nem indult · ⛔ kötelező megállás menet közben
- **KK:** Károli-kulcs, a Károli–LXX versmegfeleltetés
- **CI:** gépi ellenőrzés GitHub Actionsben; E1–E16 a szabályai
- **FJ:** forrásjelöltek felmérése; **FP:** fordítási próba
- **SZOTAR S1/S2:** a szótári brief 1. (adat) és 2. (render) menete
- **N-szám:** tétel a `NYITOTT_FELADATOK.md`-ben
- **TBESG/TBESH:** STEP-szótárak (görög/héber alapjelentés); **UBS DBH/DNTG:** UBS héber/görög szótár; **LXX:** Septuaginta
- **Szerepmátrix:** `adat/szotar_szerepek.tsv`, 10 szerep × 2 nyelv

## Kész (utolsó 2 hét)

- Fordítási próba (FP0–FP-KOR2.9): fordító eszközök és a próba eredményei, ellenőrzés naplok/ELLENOR_FP.md, merge `9eb43fe` (PR #62, 09.27)
- Szkript-karbantartás (KARBANTARTAS KB0–KB4), K1–K10 teljesül (K10 öt körben, ágleltárral, nulla-kimenet-őrrel és három mutációs/hiba-próbával: `naplok/ELLENOR_KARB.md`), merge `b8a418a` (09.27); mérőszkript-vakfoltok és -őrök javítása, PR #60 (`8bd1e40`), PR #61
- Gépi ellenőrzés GitHubon (CI, #2), PR #57, merge `68eb348` (09.27); E5 javítás: PR #59
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
| D7 | A v3 stílust és a MiniMaxot külön stíluspróba (#14) méri: Gemini 3.1 Flash Lite, DeepSeek V4 Flash és MiniMax M3, Claude vak bírálatával, költségbecsléssel | a #7 éles döntéséhez mért adat kell; a próba nem tesz adatot a kanonikus rétegbe, ezért nem vár az adatfázisra | Claude mint fordító (a kor2-ben 4.); a modellek egymást bírálják |
