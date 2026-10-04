# ELLENOR_KONTEXTUS — F32_KONTEXTUS_BRIEF.md · origin/main..claude/f32-kontextus

*A `fuggetlen-ellenor` jelentése (összefoglalva; az ellenőr nem írhat, a fájlt az orkesztrátor mentette). Eredmény: **ELTÉRÉS: 6 tétel**. Hatókör OK: motívumfájl, `adat/`, `konkordancia/` nem változott; K1, K2.1, K3.0, K3.1 (kód), K4, K5 (DT-F32a 🟡) OK; E2–E19 0 találat; #49-cel szöveges ütközés nincs (az ág az F49 merge-e után indult).*

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | K2/K-D4: a motívumot író, `munka` nélküli brief „nem fut” helyett csak „nem csomagolható” (egyedül fut) | **Nyitott** — döntés a felhasználóé: az `ellenoriz`/választó is tiltsa-e (`KOTELEZO`). |
| 2 | K-D9: a szabály „az értelmező modell (`DONTESEK.md`)” tételre hivatkozik, de ilyen tétel nincs | **Nyitott** — vagy új tétel, vagy a hivatkozás kivétele. |
| 3 | K3.2 csak ID-s fájlnévre (`[ID]_tematikus.md`) fut; a témanevű tanulmányokat (pl. F09) nem fogja meg | **Nyitott** — dokumentált korlát (`naplok/KONTEXTUS_szabalyok.md`). |
| 4 | A `kovetkezo.md` csomag-utasítása kétszer szerepel | **Javítva.** |
| 5 | A `git diff --stat` kimenete hiányzik a naplóból | **Javítva.** |
| 6 | Téves naplóállítás (F33, F42 nem ír motívumfájlt) | **Javítva.** |

Nem ellenőrizhető az ellenőrnek: a K3 próbák és az `ellenoriz` futtatása (a végrehajtó jelentése: 0 hiba, 28 unittest zöld).
