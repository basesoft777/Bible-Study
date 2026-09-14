# `naplok/` — menetek kézzel készült nyomai

Ez a könyvtár a **forrás** rétegbe tartozik (l. `CLAUDE.md` rétegtáblázata): kézzel
készült, szabadon szerkeszthető fájlok, amelyek egy-egy menet tartalmi ítéleteit
őrzik. Nem kanonikus tábla (az az `adat/`), és nem generált kimenet (az például a
`motivumlog/gate_jelentesek/`).

| Fájl | Mi ez |
|---|---|
| `f3_4_dontesek.tsv` | Az F3.4 menet 191 soronkénti, tartalom-alapú Károli-Strong ítélete. Ebből dolgozik az `eszkozok/f3_4_join_potlas.py`, és ezt ellenőrzi az `eszkozok/f3_4_ellenoriz.py`. |
| `f3_4_extra_join.tsv` | Ugyanannak a menetnek a kiegészítése: egy igehelyhez tartozó több Strong, illetve tartományok további versei. |

A terv 4.4 pontja ugyanide szánja a nevesített tanítói keresések fájljait is
(`naplok/[motívum]_tanitoi_kereses.md`).

**Miért nem az `eszkozok/` alatt:** az `eszkozok/` szkripteket tart, nem adatot. A
döntési fájl nem szkript-melléklet, hanem az F3.4 legértékesebb terméke — az az egyetlen
hely, ahol a 191 ítélet visszakereshető.
