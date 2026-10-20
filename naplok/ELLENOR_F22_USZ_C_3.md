# ELLENOR_F22_USZ_C_3 — újraellenőrzés, 2. (utolsó) kör (F22 C csomag)

**Brief:** `F22_KAROLI_STRONG_BRIEF.md` (22.9, D45). **Tartomány:** `55e3fc1..ca2cd02` (1 commit, F22.42). **Ág:** `claude/f22-2kor`, HEAD `ca2cd02`. *A független ellenőr (`fuggetlen-ellenor`) jelentése; fájlírási eszköze nincs, a végrehajtó mentette, a hosszú parancscellák rövidítve, az eredmények változatlanok.*

**Eredmény: TISZTA** (ELTÉRÉS nincs; az 1. kör egyetlen tétele megszűnt)

**Modell-ellenőrzés:** az ellenőr modellje `claude-opus-5-5`, a kért `opus`, egyezik. Az F22.42 egyetlen `modell` mezőt sem ír (az `adat/` és az `f22/` diffje üres).

| pont | eredmény | indok (rövidítve) |
|---|---|---|
| 1a. N-F22e, 2Kor 8:13–14 → F22.24 | OK | `git log --oneline -- f22/kezi_versek_2Kor.tsv`: a fájl legkorábbi commitja `3f8b959` (F22.24); a `2Kor 8:13`, `2Kor 8:14` sor ebben jön létre |
| 1b. 2Kor 2:12–13, 5:14–15, Zsid 1:1–2, Fil 3:13–14 → F22.33 | OK | a nyolc sor az `ad00eae` (F22.33) commitban kerül be; a `c0d1070` (F22.20) csak N-F22c-sorokat töröl (Fil 2:7–8, Zsid 3:9–10, 7:20–21, 12:22–23); az F22.41 csak az ok-szöveget módosítja |
| 1c. A sor többi része sértetlen | OK | `NYITOTT_FELADATOK.md:117`: egyetlen szócsere (`(F22.32,` → `(a 2Kor 8:13–14: F22.24; … F22.33;`), 1/1 sor, a dátum megmaradt |
| 2a. A brief `ir` mezője | OK | a lista elejére `naplok/ELLENOR_F22_USZ_C_2.md` és `_3.md` került, más változás nincs |
| 2b. `ELLENOR_F22_USZ_C_2.md` tartalma | OK | a tartomány, az „ELTÉRÉS: 1 tétel”, a DT262, a tokenhatárok, a 7,4769, a CI-eredmény és a regresszió az 1. körös jelentéssel egyezik; a fájl végén a végrehajtó „Javítás (F22.42)” szakasza jelölt, nem eltérés |
| Regresszió | OK | `git diff --stat 55e3fc1..ca2cd02`: brief 1/1, `NYITOTT_FELADATOK.md` 1/1, `ELLENOR_F22_USZ_C_2.md` +28; `adat/`, `f22/`, `FELADATOK.md`, `konkordancia/` diffje üres; nem futott modellhívás; a commit-üzenet magyar, `F22.42` előtaggal |
| Lista 1–5 | OK | adatsor nem törlődött; az adat- és konkordancia-táblákon Δ = 0; nem került be végleges DT/N-szám; nincs generált blokk-változás |
| CI (saját futtatás) | OK (korábbi hiba) | E2–E16, E19, E20, E26, E28–E31: 0; E25: 4 JELENTÉS (régi D34 jelzések); E27: HIBA 1 (`FELADATOK.md:58`, `1f420a7c`, az F52-brief generált blokkja, a fájl nem változott, a hiba korábbi) |

Az ellenőr megjegyzése: ez nem merge-ítélet, a merge-ről a felhasználó dönt.
