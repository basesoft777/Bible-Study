# F53 — FELADATTERKEP munkanapló

*Brief: `F53_FELADATTERKEP_BRIEF.md` · ág: `claude/f53-feladatterkep`. A kis minta
eltéréslistája és a felhasználó FT.2-válasza: `naplok/F53_kis_minta_eltereslista.md`.
A teljes napló (FT.6) ezt a fájlt bővíti.*

## Lépések

| tétel | commit | állapot |
|---|---|---|
| FT.0–FT.2 | `7508e84`, `3b95c3d`, `47a36c4` | kész; FT.2 ⛔ jóváhagyva 2026-10-05 (`3bcf666`) |
| main behúzása | `5c7abe2` | a PR #199 (DT-M8) és a PR #200 (F52.8) az FT.3 előtt |
| FT.3 | `5b7c305` | kész: a gyökérbeli lap és JSON generált; két futás bájtazonos; 19 teszt zöld; `feladatok.py ellenoriz` 0 hiba |
| FT.4 | `5e8e6b7`, `64813ad` | kész: a diff jóváhagyva, változtatás nélkül alkalmazva; N-F53e (CI-őr) felvéve |
| FT.5 | — | **⛔ áll** (l. lent) |

## FT.5 ⛔ — a projekt-azonosító nem állapítható meg (2026-10-05)

A brief 5. és 6. pontja szerint a `files` képesség deklarálásához a Claude Code
projekt azonosítója (`chan_…`) kell. A session ezt nem tudta megállapítani:

- a session saját metaadata (`get_session self`) csak a helyi session-azonosítót
  (`local_…`), a munkakönyvtárat és az ágat adja, projekt-azonosítót nem;
- a meglévő artifact (https://claude.ai/artifact/Dwnq3JtHgmgPiwDPaUnJzx) egyoldalas,
  külön publikált fájl nélkül; korábbi `files`-deklarációból azonosító nem olvasható ki;
- a repóban és a memóriában `chan_` azonosító nem szerepel (a brief két helyén csak
  a `chan_…` minta).

A brief szerint: **az artifact a beágyazott pillanatképpel marad** (a kézi 8. verzió,
változatlan), frissítés kérésre. A generátor `--cel artifact` kimenetét nem írtam meg,
és feltöltés nem történt: a feltöltés felülírná a meglévő linket, ezért a
felhasználó dönt.

**Kérdés a felhasználónak.** (a) Megadod a projekt-azonosítót (`chan_…`), és az FT.5
a `files`-olvasással fut le; (b) az FT.5 `files` nélkül fut: `--cel artifact` a
beágyazott pillanatképpel, feltöltés ugyanarra a linkre, a lap „pillanatkép, <bélyeg>”
jelzéssel, frissítés kérésre; (c) az artifact a kézi 8. verzión marad, az FT.5 később.
