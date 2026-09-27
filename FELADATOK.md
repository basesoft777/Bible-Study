# FELADATOK.md — feladatkövető

*v1 · 2026.09.27 · `main` = `4b9ae49` · Ez az egyetlen fájl, amit a chat egy új beszélgetés elején elolvas. A részletek a briefekben és a `NYITOTT_FELADATOK.md`-ben vannak; ide csak az állapot, a függés és a következő lépés kerül.*

## Alapelv: előbb az adatréteg, utána a render

Amíg nem látjuk, mit adnak az új források, nem foglalkozunk rendereléssel (lexikonoldal, törzscikk, migráció), mert a késői adat miatt mindent újra kellene generálni. Emiatt két fázis van, és a 2. fázis egyik feladata sem indul, amíg az 1. fázis el nem készül.

**Kritikus út:** #1 és #2 → #4 → #5 → #7 → #9 → #10

## 1. fázis — adatréteg

| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Következő lépés | Hol |
|---|---|---|---|---|---|---|
| 3 | Fordítási próba eredményének beolvasztása | a fordító eszközök és a prompt v2 a main-ben | ✅ lefutott, **még nincs ellenőrizve** | — | Független ellenőrzés (a CI után a CI + az ellenőrző ügynök), majd merge | ág `claude/forditas-pilot-brief-3afbbf-37c8ky` (`5873918`) |
| 4 | Szkript-karbantartás (KARBANTARTAS 1a–1c) | egységes parancssor, CRLF-tűrés, 26 Strong-szám nullázása (N21) | ⬜ nem futott | #2 | A briefet a repóba kell tenni, majd futtatni | brief csak chatben |
| 5 | Szótári adatréteg, 1. menet (SZOTAR S1) | a szerepmátrix hiányzó sorai adatként: fordítási gyorsítótár, terminológia, kiejtés-táblák, UBS DBH, TBESH, Girdlestone, Mounce | ⬜ nem futott | #1, #2, #4 | **Előbb:** brief-frissítés v1.2-re (FJ-eredmény: Macula küszöb alatt → S13 versszintű marad; KK; CI). Menet közben ⛔ jóváhagyásra vár tőled a Girdlestone-szöveg és 24 héber kiejtés-jelölt | `SZOTAR_BRIEF.md` v1.1 |
| 6 | Új források 2. felmérése **helyi gépről** (FJ 2. menet) | döntés a Nave, a teljes KJV/ASV és a BSB importjáról; a Macula lefedettsége | ⬜ nincs brief | — (#5-tel párhuzamosan futhat) | Brief kell. Helyi gépen fusson, mert a cloud proxy blokkolt (N27, N29–N31) | `naplok/FORRAS_jelentes.md` (fejlécébe kell a „felülírva: N27–N29” megjegyzés) |
| 7 | Thayer teljes magyar fordítása (éles) | a görög mélységi szócikk magyarul, adatként | ⬜ nem futott | #3, #5 (terminológia, kiejtés) | **Te:** döntés a v3-ról („természetes hű” stílus a promptban) | `FORDITAS_ELES_THAYER_BRIEF.md` v2, csak chatben |
| 8 | LXX-fordítói döntések a 87 függő igehelyre | minden ÓSZ-helyhez LXX-megfelelő (`adat/lxx_dontesek.tsv`) | ⬜ nem futott | #1, #6 (Macula-lefedettség) | Kutatói adatmunka; 58 gépi jelölt tájékoztatásul: `naplok/FORRAS_FJ1_lxx_jeloltek.tsv` | eredetileg a LEXIKON_LEZARAS 4c pontja |

## 2. fázis — render (csak az 1. fázis után)

| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Megjegyzés | Hol |
|---|---|---|---|---|---|---|
| 9 | Szótári adatréteg, 2. menet (SZOTAR S2) | az 1. fázis adatai megjelennek a 8 lexikonoldalon és a 8 törzscikkben | ⬜ | #5, #6, #7 | Ez javítja a törzscikkek elavult Cremer-sorát is (a CI E11 szabálya jelzi) | `SZOTAR_BRIEF.md` 2. menet |
| 10 | 8 lexikonoldal lezárása (LEXIKON_LEZARAS) | mérhetően kész oldalak (L1–L7) | ⬜ | #8, #9 | **Te:** döntés az L6 és L7 feltételről. Ide tartozik N18, N19 | brief csak chatben |
| 11 | Migráció: egy forrásból renderelés (MIGRACIO) | minden motívum a forrásrétegből renderel | ⬜ | #9 | Az M0 felmérés csak olvas, de az eredménye itt kell | brief csak chatben |
| 12 | TEREMT-002 3. lépés (próza, lexikonoldal) | az első natív egyforrású motívum kész | ⬜ | #11 | — | `TEREMT002_KUTATAS_BRIEF.md` |
| 13 | 1Móz 17-től a tanulmányok és a 6 betöltetlen motívum | a Genezis-kiadás tartalma | ⬜ | #10 | döntés 2026.09.21: a lexikonoldalak lezárása után | — |

## Takarítás (bármikor, rövid)

- A `claude/forditas-pilot-brief-3afbbf` ág törlése (csak az FP0 van rajta, ős).
- A chatben készült briefek (#4, #7, #10, #11) commitolása a repó gyökerébe, hogy a chat onnan olvassa őket.
- 72 távoli ág van, ebből kb. 60 régi (2026.09.02–09.11). Egyszeri átnézés, majd törlés.

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

- Gépi ellenőrzés GitHubon (CI.0–CI.5 + D8–D18), merge (ez a commit) (09.27); E5 javítás: PR #59
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
