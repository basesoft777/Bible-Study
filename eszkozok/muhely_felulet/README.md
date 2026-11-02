# eszkozok/muhely_felulet — a műhely Feed/Stash Dashboard forrása (F156)

Kézzel írt forrás (nem generált): a Dashboard-artifact oldala és kiegészítői. A generált adat a `generalt/muhely/*.json` (`eszkozok/muhely_allapot.py` kimenete); ez a mappa csak olvassa.

| fájl | szerep |
|---|---|
| `index.html` | az oldal (`files/index.html` a Dashboardban); az A. Olvasó tokenek saját osztályokon, mindig a világos készlet (DT-F156h) |
| `look.json` | a `dash/look` dokumentum (az A értékei tartalékként) |
| `adat_laposit.py` | `feed_*.json` → a Dashboard hat adatfájlja (nyilvános: motivumok, stash, tortenes; belső: belso_matrix, belso_hatra, belso_kapuk) |
| `olvaso_elonezet.py` | az olvasói Feed/Stash önálló előnézete: sima HTML-oldal (A. Olvasó, mindig világos), a `feed_nyilvanos.json` és `stash.json` adatából, csak előrehaladással (DT-F156j); publikálás: `Artifact`, `file_path` |
| `betu_css.py` | az öt betű-CSS (`files/*.css`, `data:` URL) az olvasó-szerver OFL betűfájljaiból |

## Hogyan kerül az artifactba

1. `python eszkozok/muhely_allapot.py` (a kimenet: `generalt/muhely/`).
2. `python eszkozok/muhely_felulet/adat_laposit.py <könyvtár>` → hat JSON.
3. A hat JSON feltöltése az artifact asset-tárába (`Artifact`, `asset: true`), majd a `datasets/<id>` dokumentumok `source.url`-jének cseréje (`ArtifactData`).
4. Az oldal vagy a betű-CSS változásakor a `files/index.html` és a `files/*.css` dokumentumok írása (`{"text": …}`); `betu_css.py <könyvtár>` állítja elő a CSS-eket. A `dash/look` a `look.json`.

A belső fül hibaszövegeket tartalmaz: az artifact hivatkozását nem szabad megosztani, amíg az a fül rajta van.
