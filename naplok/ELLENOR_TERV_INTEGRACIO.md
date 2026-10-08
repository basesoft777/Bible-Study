ELTÉRÉS: 7 tétel

# ELLENŐR — TERV_INTEGRACIO

*Az ellenőr szövege; fájlírási jog híján az orkesztrátor mentette. Bemenet: `naplok/TERV_INTEGRACIO_dontesi_lista.md`, `naplok/TERV_INTEGRACIO_leltar.md`, `naplok/TERV_INTEGRACIO_zaras.md` · tartomány: `6b62808c..dceee1e` (TI.1–TI.13, ág `claude/terv-integracio`).*

*A `feladatok.py fuggesek/jeloltek` futtatása nem fér bele a megengedett parancsok körébe (git diff/log, lekerdez.py, futtat.py), ezért nem futott; az 5. pontot az `eszkozok/feladatok.py` forrásának (603–611., 731–774., 539–546., 67–70. sor) és a fejléceknek az olvasásával vizsgálta.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 7 CI (E5) | ELTÉRÉS | `.claude/commands/konzisztencia.md:41` | `futtat.py --valtozott $(git diff --name-only $B..HEAD) --diff-alap $B --diff-fej HEAD` → **EXIT=1**, `## E5 (HIBA: 1)`: „torolt cimsor "TÖRLÉS-SZÁNDÉKOS:" jeloles nelkul: ## 1. Átvezetetlen döntés · … · 4. Régóta álló továbbvivő”. A sablon címsorát a TI.11 (`e28bb0a`) bővítette az „5. Tervelem feladat nélkül” résszel. A PR-módú CI ezen bukik; a zárójelentés és a TI.12 csak a `--teljes` exit 0-t állítja (az igaz: `--teljes` EXIT=0, E5 0). |
| 1 / 10. tétel (DT-M5) | ELTÉRÉS | `MUNKATERV.md:27` | A DT-M5 sora: „🟢 2026-10-08 (DT-F52e), a javaslat szerint — elvetés egyelőre, saját MCP után újra” — ez a döntési lista 10. tételének **b)** változata. Az „a)” és a `DONTESEK.md:108` DT-M5 sora: lezárás a DT32 szerint, chatbeli ellenőrzésre használható, bekötés nincs. A fájl 32. sora „a DT32 szerint lezárva”-t ír, tehát önmagának is ellentmond. |
| 1 / 12., 15. tétel (ADATVAGYON 19.) | ELTÉRÉS | `ADATVAGYON_TERV.md:865`, `:871` | A `[ ] eszkozok/sqlite_epit.py séma…` és a `[ ] BDB javító menet…` teendő `[x]`-re váltott, pedig a #79 és a #80 csak csonk (`brief_kell`). A 864. sor szerint a „brief megvan” állapot `[ ]` marad, így a két `[x]` hamis kész-állapot. |
| 1 / 5. tétel (DT2-sor) | ELTÉRÉS | `DONTESEK.md:12` | A lista 5. tételének „Érinti” mezője a DT2 sort is megnevezi; a sor változatlan: „L2 és L7 nincs; a #10 briefje az »L1–L7« helyett ezt a mércét írja” — ellentmond az új F10 fejlécnek (L1–L7) és a DT-F52c (5)-nek; nincs mutató a DT68 (2) / DT-F52c (5) felé. |
| 1 / 9. tétel (DT-M4 ↔ #78) | ELTÉRÉS | `F78_SZEREPMATRIX_VAZ_BRIEF.md:12`, `DONTESEK.md:147` | A DT-F52e (9) szerint a 13–14. szerep sora „a #9 vagy a #78 menetében” kerül a `szotar_szerepek.tsv`-be; az F78 `ir` mezője csak `[eszkozok/lexikon_general.py, generalt_proba/]`, a #9 `fugg: [..., 78]`. A tábla ma 22 sor (11 szerep × 2), 13–14. nincs. A 9a szerint a váz a 13–14. szerepet üres/részleges blokkként mutatná, de a fejlécek szerint ez nem állhat elő. |
| 5 (#80 fejléc) | ELTÉRÉS | `F80_BDB_KAROLI_POTLAS_BRIEF.md:1-15` | A fejlécből hiányzik az `ir`; a `feladatok.py` 603–611. sora szerint a nem kész feladat `ir` nélkül `REGI` sort kap. |
| 1 (listán kívüli változás) | ELTÉRÉS (alacsony) | `MUNKATERV.md:49` | Az „`ellenor` mindig Haiku vagy Sonnet” helyére „`fuggetlen-ellenor` (Opus, FELADATOK D10)” került — tartalmilag a D10 szerint helyes, de a 23 tétel egyike sem fedi. |
| 1 / 1., 2. tétel | OK | `F78…:1-15`, `F23…:15`, `F09…:12`, `F12…:9` | #78 `munka: adat`, `modell: sonnet`, `fazis: 1` (jóváhagyva); #23 `fugg: [32, 78]`, #9 `fugg` +78; a TEREMT-002 a második minta. |
| 1 / 3. tétel | OK | `F36…:11`, `F55…:11`, `F70…:11`, `F13…:9`, `FELADATOK.md:222-223` | #36, #55, #70 befagyasztva (#55 `Te:`), #13 a #11 után, #63/#65 nem érintett, D-F52b. |
| 1 / 5. tétel (sablon) | OK | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md:403-442` | L2 és L7 bent, blokkoló lista L1, L2, L3, L4, L6, L7 (DT68 (2)); F10 és F23 M1 mércéje L1–L7 + DT2. |
| 1 / 6. tétel | OK | `F61…:6`, `F62…:6` | `fazis: folyamat` → `1`. |
| 1 / 7. tétel | OK | `F76…:6,13-14`, `FELADATOK.md:7,222` | #76 `fazis: 1`, `fugg: [44, 79]`; D-F52a és az Alapelv kiegészítése. |
| 1 / 19. tétel | OK | `konzisztencia.md:17,26`, `F51…:84`, `F52…:93-104`, `kovetkezo.md:16`, `F82…` | (2) 5. kategória, (3) 3b, `/kovetkezo` őr-mondat („a #82 vezeti be”); (1) a #82-ben, külön ágon (D6). |
| 1 / 20. tétel | OK | `ATALAKITASI_TERV.md.md` | v10, 13. „Állapot és kiegészítések” szakasz; elavult-jelölések; F52 `olvas/ir` + ATALAKITASI. |
| 1 / 13., 14., 16., 17., 18., 21., 22., 23. tétel | OK | `MUNKATERV.md:63`, `F76…:13`, `F81…`, `ATALAKITASI…:153,162,171`, `F11…:10`, `F13…:9`, `VIBE_GUIDE.md:123,171` | SZPA_AUDIT feltételes; openbible és 17. tétel a #76-ban; #81 a #65 után; a 18. már a v4-ben kész volt. |
| 2 `Te:` várakozások | OK | `F22…:11`, `F23…:12`, `F38…:12`, `F55…:11` | A `Te:`/`Folytatás:` mindenhol megmaradt; az F22 „ready és merge” kikerülése jogos (`48caa80`); F38 PR #236 helyes. A #23 a #78-ra vár. |
| 3 E26 / helyőrzők | OK | `DONTESEK.md:91,107-109,145-149`; `FELADATOK.md:222-223` | E26 0; minden helyőrző egyszer; DT-M4/M5/M6 a helyükön, duplikálás nélkül. |
| 4 FELADATOK generált blokk | OK | `FELADATOK.md` | A diff hunkjai a GENERÁLT blokkokon kívül. |
| 5 #82 jelölt / fuggesek | NEM ELLENŐRIZHETŐ | `F82…:1-16` | A parancs a szerepen kívül; a fejléc alapján valószínűleg jelölt. |
| 6 / DT3 táblák Δ | OK | `adat/dontes_hatas.tsv` | Csak `dontes_hatas.tsv` +6; minden más tábla és a `lexikon/`, `tematikus_lezart/`, `motivumok/`, `generalt_proba/` változatlan. |
| 7 E27 | OK | `F81…:12` | 34 sor, egyik sem HIBA; egy új FIGYELMEZTETES (`adat/karoli_variancia.tsv` még nem létezik, a #65 állítja elő) — indokolt. |
| 8 commit-üzenetek | OK | — | 13 üzenet magyar, `TI.<n>:`; a TI.8 „16 brief” igaz; a TI.12 a PR-módú E5-hibát elhallgatja. |

**ELTÉRÉS-ek súlyossági sorrendben:** (1) E5 HIBA a PR-módú CI-ben; (2) DT-M5 a MUNKATERV-ben a b) változattal; (3) ADATVAGYON 19. két hamis `[x]`; (4) a DT2 sora mutató nélkül; (5) DT-M4 ↔ #78 `ir`; (6) #80 `ir` hiányzik; (7) listán kívüli MUNKATERV-mondat (alacsony).

---

## Orkesztrátor-kiegészítés (nem az ellenőr szövege)

A `feladatok.py jeloltek` a TI.13 után (a végrehajtó futtatásában): a #82 JELOLT. A javításokat a TI.14 viszi; utána 2. ellenőri kör.
