# ELLENOR_F29 — F29_SZOTAR_FORD_NAPLO_BRIEF.md · origin/main..HEAD

*A `fuggetlen-ellenor` jelentése; az ellenőr fájlt nem írhatott, az orkesztrátor rögzítette. Alap: `origin/main` (ad69675).*

| pont | eredmény |
|---|---|
| Előfeltétel: EMELES a main-en, `#EM` = #28 | OK |
| N1: D42–D50 szó szerint a brief táblájával (`#EM`→`#28`) | OK |
| N1: D-számozás (D34–D41 a #26 foglalása) | OK, megjegyzéssel |
| Generált blokk érintetlen (D24, D25) | OK |
| N3: F27 törzs nulla diff | OK |
| Csak az előírt fájlok változtak; `fp3/` nincs a commitokban; `adat/` érintetlen | OK |
| A6 / E2–E16 (`futtat.py --valtozott …`) | 0 találat |
| N2: F07 csonk „Következő lépés” sor | ELTÉRÉS → javítva |
| `kovetkezo` értékek idézőjelesek → idézőjellel kerülnének a generált táblába | ELTÉRÉS → javítva (idézőjel nélkül, `general` ellenőrizve) |
| `ir` nem tartalmazta a `FELADATOK.md`-t (D21) | ELTÉRÉS → javítva |
| `ellenoriz`, `fuggesek`, `general` | az ellenőr nem futtathatta; az orkesztrátor futtatta: 49 brief, 0 hiba; nincs körkörös függés |
| A1 (D47 számai proveniencia nélkül) | nem végrehajtói hiba: a brief szó szerinti átvételt ír elő |
