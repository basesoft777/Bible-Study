# F12 utómunka — a TEREMT-002 lapjának definíció nélküli lábjegyzetei

*2026-11-02 · ág `claude/f12-labjegyzet-def` (a friss `origin/main`-ről, `ec12f054`) · modell: `claude-opus-5-5` · megbízás: az orkesztrátor (a felhasználó hibajelzése: „hülye jelek”, a TEREMT-002 Kivonatában `[^koll]`, `[^scan-bohu]`, `[^d-elof]`)*

## 1. Mérés (a main-en)

`scope=lexikon/*_TUDOMANYOS.md | forras=a lap [^kulcs] hivatkozásai és [^kulcs]: definíciói (split, regex) | ts=2026-11-02`

| Lap | Hivatkozás | Definíció | Hiányzó |
|---|---|---|---|
| TEREMT-002 | 93 | 65 | **28** (bdb-tohu, bdb-vers, d-elof, d-jel, d-kapcs, d-mot, ford-tohu, gate, k-ezs, k-ezs2410, k-ezs3410, k-ezs4518, k-gen, k-gen3, k-jer, k-jer24–27, k-zsolt10740, koll, lxx-ezs, lxx-gen, lxx-jer, p2, scan-bohu, scan-tohu, tahot3) |
| a többi nyolc lap | — | — | 0 |

## 2. Az ok

A lexikonoldal kézi rése a forrás `<!-- RÉS-KEZDET -->` és `<!-- RÉS-VÉGE -->` jelölője közötti szöveg (`lexikon_general.res_tanulmany_torzs`). A benne álló nevesített `[^kulcs]` hivatkozások így a lapra kerültek, a definícióik viszont a forrás „Proveniencia-sorok” szakaszában, a réseken kívül állnak, és nem kerültek át. Ráadásul a `_tanulmany_szoveg` mélység szerint szűr, a `belso` „Proveniencia-sorok” abból kimarad. Az ISTENTISZT-001-en és az ALVIL-001-en azért nem jelentkezett, mert a forrásuk nevesített lábjegyzetet nem használ (0 db; a proveniencia ott inline áll). A TEREMT-002 az első natív forrás, amely a résekben nevesített lábjegyzetet használ (82 hivatkozás, 43 definíció).

## 3. Javítás

`eszkozok/lexikon_general.py`, `res_labjegyzetek_alkalmaz`: a rések beillesztése után a lap definíció nélküli nevesített hivatkozásainak definíciója a motívum kézi forrásaiból (a `res_forras.tsv` `tanulmany` fájljai, nyersen olvasva) egy generált blokkba kerül a kolofon elé (`lexikon#<ID>#res_labjegyzet`). Ha nincs hiány, nincs blokk. Változatlan tartalomnál a blokk fejléce az időbélyeggel együtt marad (fixpont).

## 4. Ellenőrző szabály

`eszkozok/ellenoriz.py` 24. szabály: a generált lapon (`*_TUDOMANYOS.md`, `*_TORZSCIKK.md`) definíció nélküli lábjegyzet-hivatkozás SÉRTÉS. Teszt: `eszkozok/teszt_ellenoriz_vedokorlat.py` `Szabaly24` (5 eset, köztük a valódi TEREMT-002 lap). A szabály a main-beli, javítás előtti lapon a 28 hiányt jelzi, a javítotton RENDBEN.

## 5. Újragenerálás és nulla-diff

- TEREMT-002: 93 hivatkozás, 93 definíció; a második generálás „változatlan”.
- A/B (`PARDES_DATUM=2026-11-02`, a régi és az új `lexikon_general.py`, mind a kilenc lap a repón kívül): nyolc lap bájtra azonos, csak a TEREMT-002 változik.
- Az ISTENTISZT-001 és az ALVIL-001 a saját `PARDES_DATUM`-ával (2026-10-29) újragenerálva: 0 eltérő sor a commitolt lappal.
- `ellenoriz.py`: SÉRTÉS 0, a 24. szabály RENDBEN. `teszt_general_forras.py`, `teszt_lexikon_adatres.py`: OK.
