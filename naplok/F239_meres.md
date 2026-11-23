# F239 — lépésenkénti mérés (a TEREMT-001 cikke)

*A brief 3. pontja szerint: lépésenként `get_usage` előtte és utána, modell, effort, idő, a futások és az ellenőrzések száma. A keret %-a az egész fiókra vonatkozik (más sessionök is fogyasztanak közben), ezért felső becslés.*

| Lépés | Modell | Idő | 5 órás keret (előtte → utána) | Heti keret, minden modell | Token | Futások / ellenőrzések | Megjegyzés |
|---|---|---|---|---|---|---|---|
| S0 · brief + `/befogad` | `claude-opus-5-5` (session) | kb. 45 perc | – → 10% | – → 46% | a session kontextusa a befogadás végén kb. 222 ezer | `feladatok.py fuggesek --extra` 5×, `ellenoriz` 4×; 2 üzenet az integrátornak | a kontextus a plafon fölött: az U2 új sessionben |
| U1 · gépi adat-előkészítés | `claude-sonnet-5-5` (`vegrehajto-sonnet` subagent) | 21,5 perc | 10% → 15% | 46% → 47% | 255 ezer (a subagent összesen) | 112 eszközhívás; `lekerdez.py` 64×; ellenőrzés: a hívó a diffet nézte (a `jeloltek.tsv` +28, -0) | a `teszt_futtat.py --diff` a helyi zár miatt nem futott le (más worktree tartotta) |
| U2 · határ és érvvázlat | `claude-opus-5-5` (session) + `hatar-ellenor` és `biralo` (`claude-sonnet-5-5`) | kb. 2 óra 15 perc, egy leállással (a session újraindult, a határ-ellenőr újra futott) | – → 34% (a 13:04-es mérés 28%) | – → 49% (13:04: 48%) | a session kontextusa a végén kb. 430 ezer (a plafon fölött; az U3 új sessionben); a subagentek: 73 ezer (határ-ellenőr), 103 ezer (bíráló) | `lekerdez.py` 7× (kollokáció) + a bíráló 30 lekérdezése; `ellenoriz.py` 4× (az utolsó: SÉRTÉS 0); 8 egyszeri szkript; 6 üzenet az integrátornak; 2 subagent (+1 megszakadt) | a „get_usage előtte” elmaradt (a session az U1 átadójából indult); a határ a szerkesztő döntésére egyszer visszavéve (F239.6), majd elfogadva (F239.7) |
