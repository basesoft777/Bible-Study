# F39 M0 — a függés-levezetés felmérése (csak olvasás)

*2026.10.01 · ág: `claude/upbeat-wright-81rpah` · forrás: `python eszkozok/feladatok.py fuggesek` (59 brief, `ellenoriz`: 0 hiba)*

## 1. A levezetést számoló függvények (`eszkozok/feladatok.py`)

| Függvény | Szerepe |
|---|---|
| `fuggesek(briefek, main_all)` | a levezetett (`levezetett`) és kézi (`kezi`) függések; ütközések (`utkozesek`); régi fejlécek; `sorrend` |
| `_elso_egyezes`, `utvonal_egyezik` | útvonal-illesztés: azonos / könyvtár-prefix / glob |
| `_szurt`, `_kozos`, `KOZOS_FAJLOK` | a közös koordinációs fájlok és a feladat saját `naplok/<F nn>_`, `<KOD>_` fájljai kimaradnak |
| `fuggesek_szoveg` | a kimenet: `FUGGES` (`*` = levezetett), `UTKOZES`, `SORREND`, `REGI` |
| `_fugg_cella`, `blokkok` | a `FELADATOK.md` „Függ ettől” oszlopa (`#N*`) |

**Fontos eltérés a brief 1. pontjától.** A kódban a `*`-gal jelölt levezetett függés ma már **írás–olvasás** (A `olvas` ∩ B `ir`), nem írás–írás. Az írás–írás ütközés külön `UTKOZES`/`SORREND` sor. A körök forrása az, hogy az `olvas` listák tág könyvtárakat (`naplok/`, `eszkozok/`, `adat/`, `lexikon/`, `CLAUDE.md`) tartalmaznak, és ezeket más feladatok `ir` listája (`naplok/`, `eszkozok/`, `CLAUDE.md`) fedi.

## 2. Mai levezetett függések (írás–olvasás, 51 él) — ok szerint

| Ok | Élek (A → B: A olvas valamit, amit B ír) |
|---|---|
| **`naplok/` (B `ir` listája helyettesítő könyvtár: #37 `naplok/`)** | #22→#37, #27→#37, #33→#37, #35→#37, #38→#37 (az olvasott fájl mind egy lezárt feladaté: `F21P_jelentes.md`, `FP2_jelentes.md`, `F24_zaras.md`, `EMELES_szentlelek_lista.tsv`, `EMELES_naplo.md`) |
| **halasztott / brief nélküli B (#7)** | #38→#7, #9→#7, #36→#7, #37→#7 (`adat/forditasok.tsv`) |
| **2. fázisú B (#9, #36) az 1. fázisú A-nak** | #23→#9, #23→#36, #33→#9, #38→#9 |
| **`CLAUDE.md` / `BRIEF_SABLON.md` (A olvassa, B írja)** | #23→#26/#30/#32; #26↔#30↔#32 (mind olvassa és írja); #37→#26/#32; #30→#26… |
| **`eszkozok/`, `eszkozok/feladatok.py` (tág olvasás)** | #33→#22/#30/#32/#35/#37/#39; #30→#39; #32→#39 |
| egyéb valódi fájl-kapcsolat | #37→#35 (`genezis/`, `tematikus_lezart/`), #37→#38/#22 (`adat/…`), #23→#35 (`tematikus_lezart/`), #23→#37 (`sablonok/…`), #32→#35, #30→#37, #36→#33/#37, #9→#33/#36, #32→#9 (`MUNKAMENET.md`) |

(A teljes nyers kimenet: `python eszkozok/feladatok.py fuggesek`.)

## 3. Mely párok származnak csak …-ból

- **csak a `naplok/` helyettesítőből:** #22→#37, #27→#37, #35→#37, #38→#37; a #33→#37 mellett `eszkozok/ellenorzes/` is köti.
- **halasztott / brief nélküli (#7):** #38→#7, #9→#7, #36→#7, #37→#7.
- **2. fázisú (#9, #36) → 1. fázisú A:** #23→#9, #23→#36, #33→#9, #38→#9.
- **#37 (folyamat) → #7, #9:** a brief 4. szabálya csak az *1. fázisú* fogadót védi; a #37 folyamat-típusú, ezekre várni fog.

## 4. Körök (a mai állapotban a levezetett élekből)

Egyetlen erősen összefüggő komponens: **{9, 22, 23, 26, 30, 32, 33, 35, 36, 37, 38}**. Elemi körök, amelyeket a brief említ:
- #35→#37 (`naplok/`) és #37→#35 (`genezis/`, `tematikus_lezart/`) — a #35→#37 fele a `naplok/` helyettesítőből jön.
- #30→#37 (`.github/workflows/`) és #37→#30 (`eszkozok/ellenorzes/`) és #30→#39→… a feladatok.py miatt.
- #26↔#30↔#32 (`CLAUDE.md`, `BRIEF_SABLON.md`), #9↔#36 (`lexikon/`), #32↔#37 (`MUNKAMENET.md`/`CLAUDE.md`), #23↔#37 (`sablonok/`).
- Csak explicit (`fugg`) körök: nincs.

## 5. A javítás szabályainak hatása (prototípus, még nincs a kódban)

A brief 3. és 4. szabályával (a `naplok/` helyettesítő és az `ELLENOR_*`/`*_zaras.md` kizárása; a halasztott, brief nélküli és 2. fázisú B nem köt 1. fázisú A-t) számolva:

- eltűnik: #22/#27/#33/#35/#38→#37 (`naplok/`); #38→#7, #38→#9, #23→#9, #23→#36, #33→#9.
- **marad (2. szabály, valódi írás–olvasás):** a `CLAUDE.md`, `BRIEF_SABLON.md`, `MUNKAMENET.md`, `eszkozok/`, `lexikon/`, `sablonok/` miatti élek. Ezekből a komponens **{9, 23, 26, 30, 32, 33, 36, 37}** továbbra is kört alkot, vagyis a 2. szabály szerint hiba lenne, a K1 pedig nem teljesülne.
- jelölt a 3. lépés szerint: **#35 és #38 szabad**; **#23 blokkolt** (#26, #30, #32: `CLAUDE.md`; #35: `tematikus_lezart/`; #37: `sablonok/`); #22 `dontesre_var`, #27 halasztott; #30 és #33 blokkolt.

## 6. Megállás (⛔)

A fenti valódi írás–olvasás élek közül a javítás megszüntet: #23→#9, #23→#36, #33→#9, #38→#9, #38→#7 (D1 szerint szándékos), és a maradék élek (különösen a `CLAUDE.md` körei) a 2. szabállyal ütköznek a K1-gyel. Döntés kell: `DONTESEK.md`, DT-F39g.
