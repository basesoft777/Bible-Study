# F21 zárójelentés — Károli–Strong mérőpilot

*Lezárva 2026.09.30 · ág `claude/f21-pilot` · modell: sonnet (szkriptek), opus (aranyminta, besorolás) · külső modellek: Gemini 3.1 Flash Lite (A), DeepSeek V4 Flash (B), Gemini 3.8 Flash (C)*

- **Eredmény:** egyik mért összeállítás sem felel meg a rögzített döntési szabálynak; az A+B+C nem mért (PD8, az F4 nem futott). Részletek: `naplok/F21P_jelentes.md`.
- **Mi bukott el:** az A+B `magas` pontossága (R1 85,2%, R3 91,8%, R4 91,7% a 98% ellen) és a régi arany egyezése (60%, 3/5). Az A és a B végleges kapuhibája 41–41% (megfigyelés, nem feltétel). A C egymodelles, a PD6 szerint nem minősíthető (pontosság 91,7–95,6% rétegenként az arany v2-n).
- **Mért számok:** a C (F3 → F3V2) lefedettsége 94,2% → 97,1%, pontossága 93,3% → 93,6%; kapuhiba első próbára 15,0% → 9,5%. A "korrigált" értékek csak "Opus-besorolás, nem mérés" jelöléssel szerepelnek.
- **Költség:** a pilot 0,7346 USD (plafon 3 USD). P5 a C-re: F3 42 USD (90%: 38–47), F3V2 42 USD (90%: 38–46) a teljes Bibliára.
- **KJV (N29):** a v1-adaton nem teljesül, n=8, nem végleges. A #19 függéséhez nem nyúltunk.
- **Egyeztetett eltérések:** az A és a B kiesett, v2 nem lesz hozzájuk, az F4 nem fut (PD8); P5 csak a C-re; a bootstrap egysége a köteg (DT21 f, nyitott); a C gondolkodása kötelező `minimal`, az A/B kikapcsolva (DT21 j); a #22 fejléce `dontesre_var` a felhasználó kifejezett utasítására.
- **Nyitott (DT19–DT21):** a #22 sorsa (marad / módosított céllal indul / elhalasztva) és az a–j tételek a DT21-ben; a döntések a felhasználóéi.
- **Ellenőrzés:** `naplok/ELLENOR_F21P.md` (1. kör, NEM TISZTA, 7 figyelmeztetés, javítva) és `naplok/ELLENOR_F21P_2.md` (2. kör, hiba és figyelmeztetés nélkül, 2 megjegyzés); CI: az E16 miatt a PR-cím „[ELLENŐRZŐ]” előtagú.
- **Átvihető eszközök:** `eszkozok/karoli_strong/` (tokenek, kapu, futtat, meres, c_diff, koltseg_vetit), `f21p/prompt_v1.md`, `prompt_v2.md`, `arany_opus_v2.jsonl` (befagyasztva, sha256), `f21p/meres_kizaras.tsv`.
- **Megtanult korlátok:** TAHOT-sorrend 57 versben, X/Q(K) változatsorok, `[nem TR]`, összetett Strong, az A/B JSON-hibái, a C gondolkodási tokenje nem mérhető az F1–F6-ban.
- **Merge:** csak a felhasználótól.
