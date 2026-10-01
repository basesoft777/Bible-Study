# F21P_arany_v3_dontes.md — az arany v3 jóváhagyása és befagyasztása

*Kézi rögzítés (a `F21P_arany_v3_diff.md` generált fájl, ezért a döntés külön fájlban áll). Proveniencia: manual (felhasználói döntés, 2026.10.01).*

- **Döntés:** az arany v3 = az **A változat** (3 link: Jób 33:13 *Azért*, Mt 21:4 *azért*, Ez 39:13 *ezt* → `betoldas`; 1048 link). A **B változat elutasítva**, mert ütközik a K4-gyel (az igén álló névmási rag névmása a K4/D szerint a ragra megy, nem lesz `betoldas`).
- **Befagyasztás előtti szövegellenőrzés (felhasználói kérés):** a jegyzet v2 (K3 v2, K4 v2) és a `prompt_v3` C/D szövege egyezik a kritériummal: a magyar tárgyi névmás csak akkor `betoldas`, ha nincs eredeti megfelelője (nincs *'et* + rag, sem más eredeti névmás vagy névmási rag); az igén vagy elöljárón álló névmási ragra a K4/D szerint kötődik. A szövegen nem kellett javítani.
- **Fájlok:** `f21p/arany_opus_v3.jsonl` (az `arany_opus_v3_javaslat.jsonl` bájtazonos másolata), `f21p/arany_opus_v3.sha256` (acdeb55f…d458), `f21p/prompt_v3.sha256` (5937e6ab…1b4e); mindkét hash az LF-re normalizált tartalom sha256-ja (`tokenek.sha256_lf`). A `arany_opus_v3_javaslat_B.jsonl` (elutasítva) dokumentációként megmarad, nem használt.
- **Következmény:** a regressziós mérés az arany v3-ra fut (`tokenek.legfrissebb_arany` = v3); az arany v2 érintetlen marad (a két C v2-futás tájékoztatásul).
