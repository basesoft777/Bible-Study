# F21 zárójelentés — Károli–Strong mérőpilot (P3 + P3b + regressziós mérés P3c)

*Lezárva 2026.10.01 · ág `claude/f21-regresszio-meres` (a P3/P3b: `claude/f21-pilot`, PR #92) · modell: sonnet (szkriptek), opus (arany, besorolás) · külső modellek: Gemini 3.1 Flash Lite (A), DeepSeek V4 Flash (B), Gemini 3.8 Flash (C), Claude Sonnet 5.5 (Sonnet) · részletek: `naplok/F21P_jelentes.md`, `naplok/F21P_meres_p3c.md`*

- **Eredmény (Döntési szabály):** egyik összeállítás sem felel meg. A+B (P3b): bukott 1, 2, 3, 5; A+B+C (P3b): bukott 1–5; Sonnet + C pár (P3c, döntőbíró nélkül, arany v3): bukott 3, 4, 5, az (1) R3-ja nem mérhető (PD19). Az A, B, C, Sonnet egymodelles: PD6 szerint nem minősíthető.
- **A pár mért számai:** `magas` pontosság R1 98,3%, R2 99,3%, R4 98,7% (R3: 0/0); lefedettség 98,6%; régi arany 93,8% (tájékoztató, 1Móz 6:17 nélkül 96,8%); `alacsony` arány 19,1% (200 vers), vetítve 21,4%, R3 55,9%.
- **Egymodelles (mért):** C (F3V3) pontosság 95,3%, lefedettség 96,3%; Sonnet (50/60 aranyvers kapun át) 97,3% / 96,8%. A prompt_v2 → v3 hatás a C-n: pontosság +2,21 pp, lefedettség −1,05 pp (mindkettő az ingadozáson kívül, egy futáspárral becsülve).
- **P5 (teljes Biblia, F22-rétegek, 90%):** Sonnet 373,94 USD [337,97–418,65], Sonnet + C 416,43 [379,88–460,97], C (F3V3) 42,49 [38,55–46,52]; A+B 27,96, A+B+C 85,91 (P3b).
- **A pilot költsége:** 4,325231 USD (P3 0,734594, P3b 0,870473, P3c 2,720164; ebből a Sonnet 2,197554, a baleseti F8V3-kötegek 0,023232). Plafon 3 → 4 → 5 USD (küszöb 2 → 3,90 → 4,90); a futó összeg a küszöb alatt maradt.
- **Sonnet-keret:** a modell a `reasoning.max_tokens = 1024` keretet nem tartotta be: 142 077 gondolkodási token a 173 414 kimeneti tokenből, hívásonként max. 11 144; 2 length-lezárás a 15. kötegben, a 10 R3-aranyvers (Jer 46:21, 51:3; Ez 11:3, 16:57, 22:25, 30:5, 33:31, 39:13, 41:2, 46:12) végleg kapuhibás; a futás nem determinisztikus.
- **KJV:** a mérés szerint nincs kimutatható hatás (+0,25 pp, az ingadozáson belül); a pilot döntése: „nem igazolt, a javított táblával újramérhető”; az R4 „KJV nélkül, nem mérhető”.
- **(c)-besorolás (Opus, nem mérés):** C (F3V3) a/b/c = 41/22/26, Sonnet 22/17/7, közös (c) 1; a DT-F21j a–e segített (a 2, b 4, c 4, e 3 eset), ártott egyik sem.
- **#22:** a felhasználó választott iránya javaslatként rögzítve (Sonnet a Code-ban + C az Actionsben, könyvenként, a Genezissel kezdve; `magas` = egyezés, eltérésnél a Sonnet-változat `alacsony`; próféták 5 verses kötegben; az 1Móz 1–5 után `/usage`, megállás 50% fölött); a #22 `dontesre_var`, brief-diff nincs, teljes futás nem indul.
- **Nyitott:** N-F21 (Károli ↔ KJV zsoltár-eltolódás); az (1) R3 nem mérhető (a Sonnet R3-pótlása a próféták előtt); hét „arany-felülvizsgálatra jelölt” C-eset (a Sonnetnél egy); az F31-brief átfedése. A DT-F21j a–e lezárva.
- **Merge:** csak a felhasználótól.
