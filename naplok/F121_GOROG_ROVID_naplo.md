# F121.21 — a görög rövid jelentés magyarul (7. szerep, SECE-táblák)

*2026-10-29, `claude-sonnet-5-5`. Kulcs: `TBESG | <Strong> | <Strong> | rovid | glosszak_hu` (DT-F121o). Forrás: a `TBESG.txt` sor 7. oszlopa (Strongonként az első sor, ahogy a generátor `tbesg_rovid_glossza`). 56 sor: az ISTENTISZT-001 lap 54 egyedi görög Strongja (53 a SECE-táblában + a G1941) és az ALVIL-001 két további (G0086, G2288).*

- **Tervezet:** `naplok/F121_GOROG_ROVID_tervezet.tsv`; jóváhagyva két módosítással (G2745 „dicsekedés”, G3870 „kérni/vigasztalni”) — orkesztrátor, a felhasználó felhatalmazásával. Kapuk: mind az 56 átment. 13. szabály RENDBEN.
- **Mankók:** `…_manko.tsv`: szójegyzék nincs ütközés (30 egyezik, 26 nincs adat); Károli 26 soron „nem található” (jórészt toldalék-eltérés; a szójegyzék dönt, DT239). `…_szojegyzek_javaslat.tsv` (DT240): 437 kulcs, új sort nem javaslok. `…_visszamenoleges.tsv` (DT242): a korábbi 3 tétel, új nincs.
- **G2564:** a TBESG forrás-glosszája hibás („to call: call”, a „call” megismétlődik); a fordítás „hívni”.
- **Egységesség:** G1521/G1533 mindkettő „behozni” (a forrás mindkettőnél „to bring in”); G2896 „kiáltozni” (a gyorsítótár: „to cry” → kiáltozni×5) a G0310/G0994 „kiáltani”-val szemben; G2362 „trón” (szójegyzék > Károli).
- **Generátor:** `lexikon_general.rovid_jelentes` görög ága a `forditas_ehhez('TBESG', strong, strong, 'rovid', 'glosszak_hu')`-t keresi, fallback az angol + `fordításra vár` (teszt: `eszkozok/teszt_gorog_rovid_jelentes.py`). Feloldó: `glossza_lexikon_forditas.tovabbi_forras` (SEMA 2.14).
- **Lapok:** az ISTENTISZT-001 és az ALVIL-001 újragenerálva; csak a SECE-sorok változtak (a `fordításra vár` jelölésű cella 0).
