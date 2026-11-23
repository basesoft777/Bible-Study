# F239 — lépésenkénti mérés (a TEREMT-001 cikke)

*A brief 3. pontja szerint: lépésenként `get_usage` előtte és utána, modell, effort, idő, a futások és az ellenőrzések száma. A keret %-a az egész fiókra vonatkozik (más sessionök is fogyasztanak közben), ezért felső becslés.*

| Lépés | Modell | Idő | 5 órás keret (előtte → utána) | Heti keret, minden modell | Token | Futások / ellenőrzések | Megjegyzés |
|---|---|---|---|---|---|---|---|
| S0 · brief + `/befogad` | `claude-opus-5-5` (session) | kb. 45 perc | – → 10% | – → 46% | a session kontextusa a befogadás végén kb. 222 ezer | `feladatok.py fuggesek --extra` 5×, `ellenoriz` 4×; 2 üzenet az integrátornak | a kontextus a plafon fölött: az U2 új sessionben |
| U1 · gépi adat-előkészítés | `claude-sonnet-5-5` (`vegrehajto-sonnet` subagent) | 21,5 perc | 10% → 15% | 46% → 47% | 255 ezer (a subagent összesen) | 112 eszközhívás; `lekerdez.py` 64×; ellenőrzés: a hívó a diffet nézte (a `jeloltek.tsv` +28, -0) | a `teszt_futtat.py --diff` a helyi zár miatt nem futott le (más worktree tartotta) |
