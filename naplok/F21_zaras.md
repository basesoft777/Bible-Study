# F21 zárójelentés — Károli–Strong mérőpilot (P3 + P3b)

*Lezárva 2026.09.30 · ág `claude/f21-pilot` · PR #92 (draft) · modell: sonnet (szkriptek), opus (aranyminta, besorolás) · külső modellek: Gemini 3.1 Flash Lite (A), DeepSeek V4 Flash (B), Gemini 3.8 Flash (C)*

- **Eredmény:** az A+B és az A+B+C is mért, és egyik sem felel meg a rögzített döntési szabálynak; a „Javaslat” pont szerint: egyik sem. Az A, B és C egymodelles, a PD6 szerint nem minősíthető. Részletek: `naplok/F21P_jelentes.md`, `naplok/F21P_meres_p3b.md`.
- **Mi bukott el:** A+B: a `magas` pontosság (rétegenként 90,6–97,0%), a lefedettség (64,5%), a régi arany egyezés (56,2%, PD9-cel 60,0%), az `alacsony` arány (69,7%). A+B+C: mind az öt feltétel, köztük a vetített költség 85,75 USD [79,63–92,33] a 60 USD ellen.
- **C egymodelles:** pontosság 93,6% / 93,0%, lefedettség 97,1% / 97,5% (F3V2 / F3V2b, az arany v2-n); a két azonos promptú futás eltérése ±0,6 pp (90%: pontosság [−1,64; +0,53] pp, lefedettség [−0,62; +1,60] pp), ez az ingadozás becslése egy futáspárból.
- **Költség:** a teljes pilot 1,605 USD (P3 0,7346 + P3b); plafon 3 USD, a 2 USD-s küszöb nem aktiválódott. P5 a teljes Bibliára: A 22,83, B 5,12, C 42,03, A+B 27,95, A+B+C 85,75 USD, 90%-os intervallummal.
- **KJV (N29) a v2-adaton:** a `magas` pontosság +15,6 pp a közös halmazon (n=7 R1-vers), az A–B eltérés relatív csökkenése nem teljesíti a 20%-ot; nem végleges. A #19 függéséhez nem nyúltunk.
- **Egyeztetett eltérések:** a DT21 lezárása visszavonva (DT22), a pilot folytatódott (P3b); a bootstrap egysége a köteg (DT21 f, nyitott); a C gondolkodása kötelező `minimal`, az A/B kikapcsolva (DT21 j); a #22 fejléce `dontesre_var` a felhasználó kifejezett utasítására.
- **Nyitott (DT21, DT22):** a #22 sorsa (marad / módosított céllal indul / elhalasztva) és az a–j tételek; a döntések a felhasználóéi. A korrigált értékek csak „Opus-besorolás, nem mérés” jelöléssel szerepelnek.
- **Ellenőrzés:** `naplok/ELLENOR_F21P.md`, `ELLENOR_F21P_2.md` (P3-ra), `ELLENOR_F21P_3.md` (P3b-re); CI: a PR-cím „[ELLENŐRZŐ]” előtagú (E16).
- **Átvihető eszközök:** `eszkozok/karoli_strong/` (tokenek, kapu, futtat, meres, meres_p3b, c_diff, koltseg_vetit), `f21p/prompt_v1.md`, `prompt_v2.md`, `prompt_biro_v2.md`, `arany_opus_v2.jsonl` (befagyasztva, sha256).
- **Megtanult korlátok:** TAHOT-sorrend 57 versben, X/Q(K) változatsorok, `[nem TR]`, összetett Strong, az A/B JSON-hibái (B első próbára 70,5% kapuhiba v2-vel), a C gondolkodási tokenje nem mérhető.
- **Merge:** csak a felhasználótól.
