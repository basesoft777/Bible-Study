# ELLENOR_F22_USZ_C_2 — újraellenőrzés, 1. kör (F22 C csomag)

**Brief:** `F22_KAROLI_STRONG_BRIEF.md` (22.9 C csomag, D45, DT262). **Tartomány:** `20670a6..55e3fc1` (1 commit, F22.41); az előző jelentés: `naplok/ELLENOR_F22_USZ_C.md` (ELTÉRÉS: 5 tétel). *A független ellenőr (`fuggetlen-ellenor`) jelentése; fájlírási eszköze nincs, a végrehajtó mentette, a hosszú parancscellák rövidítve, az eredmények változatlanok.*

**Eredmény: ELTÉRÉS: 1 tétel** (az előző kör 5 tételéből 4 megszűnt, 1 új, alacsony súlyú)

**Modell-ellenőrzés:** az ellenőr modellje `claude-opus-5-5`, a kért `opus`, egyezik; az F22.41 egyetlen `modell` mezőt sem ír (`adat/`, `f22/api_termeles` diffje üres). **Eljárás:** egy hívásban a `git diff --word-diff` kimenetét csővel szűrte (csak olvasás); a `feladatok.py ellenoriz` nincs a megengedett körében.

| pont | eredmény | indok (rövidítve) |
|---|---|---|
| 1. DT262 | OK | `DONTESEK.md:324`: csak ez a sor változott; Állapot ✅; a Döntés idézi a „b: részletekben, most” választ (2026-10-20), alkalmazás F22.35–F22.38; a Kérdés/Opciók/Javaslat/Napló cella bájtra azonos; új DT-szám nincs. A chatbeli jóváhagyás maga nem ellenőrizhető |
| 2a. 2Kor 2:13 tokenhatár | OK | TAGNT: 1. token οὐκ … 14. token μου, a 15. ἀλλ᾽; `lekerdez.py scan G3165 --szakasz "2Kor 2:13"` → n=1; a Károli 2:12 „…nem találtam Titust, az én atyámfiát;”-tal zárul |
| 2b. Zsid 1:2 tokenhatár | OK | TAGNT: 1. ἐπ᾽ … 9. υἱῷ, a 10. ὃν; `scan G5207 --szakasz "Zsid 1:2"` → n=1; a Károli 1:1 „…ez utolsó időkben szólott nékünk Fia által,”-val zárul |
| 2c. 2Kor 8:14 „1–11” | OK | ἐν(1) … ὑστέρημα(11), a 12. ἵνα; `scan G5303 --szakasz "2Kor 8:14"` → találat |
| 2d. Javított szöveg mindenütt | OK | a hét érintett fájlban minden találat 1–14 / 1–9; a maradék „1–7.”, „1–11.” a 2Kor 8:13–14-re vonatkozik, ott helyes |
| 2e. Az adattáblák nem változtak | OK | `git diff --stat 20670a6..55e3fc1 -- adat f22/valaszok f22/api_termeles FELADATOK.md` üres |
| 3. N-F22e (NYITOTT_FELADATOK.md:117) | OK | „(a mergelt könyvekben; most `kezi` kényszerben)”, összhangban az „ÁTMENETI KEZELÉS” mondattal; a `F22_C_elokeszites.md:38,41` „mergelve, javítatlan” az F22.31 pillanatképe, nem ellentmondás |
| **3/új. N-F22e commit-hivatkozása** | **ELTÉRÉS (alacsony)** | az „ÁTMENETI KEZELÉS (F22.32, 2026.10.19)” az öt `kezi` kényszert az F22.32-nek tulajdonítja; `git log` szerint a 2Kor 8:13–14 az F22.24-ben (3f8b959), a többi az F22.33-ban (ad00eae) lett kezi; az F22.32 (e6dd7cf) a C versbeosztásának jóváhagyása. A hibás hivatkozást az F22.34 (daf5812) írta be; az előző kör nem jelezte |
| 4. Költség 7,4769 | OK | a brief, a DONTESEK és az összesítő mindenütt 7,4769; a 7,4768 csak az `ELLENOR_F22_USZ_C.md` idézetében; a pontos érték a futásnaplóból 103.530839 − 96.053973 = 7.476866 |
| 5. Brief `ir` mező | OK | benne a C táblái, válaszai, átnézési listái, `tokenszint_vershatar.py`; megjegyzés: az `ELLENOR_F22_USZ_C_2.md` mentéskor felveendő |
| CI | NEM ELLENŐRIZHETŐ / saját futás | E2–E20, E26, E28–E31: 0; E25: 4 JELENTÉS (régi); E27 HIBA 1 (`FELADATOK.md:58`, `1f420a7c`, a fájl változatlan, a hiba korábbi) |
| Regresszió (érintett fájlok, modellhívás, commit-üzenet, Lista 1–5) | OK | 12 fájl, +68/−18 sor, mind dokumentum; `FELADATOK.md` változatlan; nem futott új modellhívás (145 C-sor); a commit-üzenet magyar, `F22.41` előtaggal; az adattáblák Δ = 0 |

**ELTÉRÉS:** 1. (alacsony, az F22.34-ből) `NYITOTT_FELADATOK.md:117`: az „ÁTMENETI KEZELÉS (F22.32, …)” hivatkozás hibás.

## Javítás (F22.42, 2026.10.20)

A hivatkozás javítva: „(a 2Kor 8:13–14: F22.24; a 2Kor 2:12–13, 5:14–15, Zsid 1:1–2, Fil 3:13–14: F22.33; 2026.10.19)”; a brief `ir` mezője felvette ezt a jelentést. Következő lépés: 2. (utolsó) újraellenőrzés (`naplok/ELLENOR_F22_USZ_C_3.md`).
