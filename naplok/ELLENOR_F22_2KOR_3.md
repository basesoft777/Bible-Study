# ELLENOR_F22_2KOR_3 — újraellenőrzés, 2. (utolsó) kör

F22_KAROLI_STRONG_BRIEF.md (22.9, D45), `79cde01..ad24b7d` (javítás: F22.27; ág: claude/f22-2kor)

*A független ellenőr (`fuggetlen-ellenor`) jelentése. A subagentnek nincs Write eszköze, ezért a végrehajtó session mentette a repóba; a jelentés tartalma rövidítve, az eredmények és a számok változatlanok.*

**Eredmény: TISZTA** (az 1. kör 3 tétele megszűnt; ELTÉRÉS nincs)

**Modell-ellenőrzés.** A tényleges modell `claude-opus-5-5`, a kért modell `opus`, egyezik. Az F22.27 adattáblát nem érintett (`git diff --stat 79cde01..ad24b7d`: 4 fájl: brief, `NYITOTT_FELADATOK.md`, `ELLENOR_F22_2KOR_2.md`, `F22_2Kor_jelentes.md`); a commit `Co-Authored-By: Claude Sonnet 5.5`, egyezik a brief `modell: sonnet` mezőjével.

**Tanulmány-ellenőrzés (F37 T4):** nem alkalmazható. **Eljárási közlés:** az ellenőr néhány olvasó parancs kimenetét csővel szűrte (fájlt nem írt); a `feladatok.py ellenoriz` nincs a megengedett körében, nem futtatta (a végrehajtó futtatása: 145 brief, 0 hiba).

| pont | eredmény | indok |
|---|---|---|
| 1. Róm 16:25–27 görög szövege | OK | `lekerdez.py scan G2316 --szakasz "Róm 16:25-27"` → Róm 16:26, 16:27 (`scope=range:Róm 16:25-27 \| forras=TAGNT_kivonat.tsv \| strong=G2316 \| n=2 \| ts=2026-10-19T16:12Z`); `scan G1410 --szakasz "Róm 16:25"` → Róm 16:25 |
| 1. Jel 12:18 görög szövege | OK | `scan G0285 --szakasz "Jel 12:18"` → Jel 12:18 (`n=1 \| ts=2026-10-19T16:12Z`); `scan G2281` → Jel 12:18 |
| 1. a brief C-sora (`:182`) | OK | „Róm 16:25–27, Jel 12:18 (az F90 óta megvan a görög szövegük)”; a három Károli-összevonás változatlanul benne van |
| 1. a „Hiányzó görög szöveg” pont (`:195`) | OK | a régi állítás eltűnt; szúrópróba: `scan G2316 --szakasz "2Kor 13:13"`, `scan G5547 --szakasz "Fil 1:16-17"` találat |
| 1. „a kivonatban nincs eredeti vers nélküli hely” | NEM ELLENŐRIZHETŐ az ellenőrnek | a négy megnevezett hely igazolva; a teljes ÚSZ-re szóló összevetés nem volt a megengedett körben (a végrehajtó: `f22/versmegfeleltetes.tsv` `nincs_eredeti` sorainak száma 0) |
| 1. az új tokenszintű előírás és a D45 | OK | az előírás a „csomagonként versbeosztás-jóváhagyást” szigorítja, nem cseréli le; a „×1,2-vel egészben, különben Róm+1Kor” feltételt nem érinti; nincs ellentmondás |
| 2. 7,995 ≤ 8,306, különbség 0,311 | OK | 0,005226×1638 = 8,560188; +1,36 = 9,920188; /1894 = 0,0052377; ×1272 = 6,6624; ×1,2 = 7,9949 ≈ 7,995; maradék 104,36 − 96,0540 = 8,306 |
| 2. „kb. 98.3 USD” a Róm után | OK | 96,054 + 431×0,0052377 = 98,31; Róm = 431 vers (Károli) |
| 2. C = 1272 vers | OK | `^(Róm\|1Kor\|Jel) \d+:\d+\t` a `Karoli_1908.tsv`-ben: 1272 |
| 3. az `ir` mező | OK (megjegyzéssel) | mindhárom fájl szerepel; a `naplok/ELLENOR_F22_2KOR.md` duplikátum (az `ir` listában már korábban is 12 duplikátum volt) |
| Regresszió: a javítás köre | OK | adat/, f22/, FELADATOK.md változatlan; a C nem indult; `f22/versosszevonas.tsv` nem változott |
| Regresszió: commit-üzenet | OK | `ad24b7d`: magyar, `F22.27` előtaggal |
| Regresszió: NYITOTT_FELADATOK.md 3. sora | OK | „Utolsó frissítés: 2026.10.19 (F22 …)” |
| A1, A2, A6 / CI | OK | `futtat.py` a 4 változott fájlra: exit 1; E12–E15, E2–E16, E19, E20, E26, E28–E31: 0; E25: 4 JELENTÉS (a diffen kívül); E27: 1 HIBA (`FELADATOK.md:56`, `1f420a7c`, az F52-brief generált blokkja, a diffen kívül; ugyanez volt az előző körben) |
| Lista 1–5 | OK | törölt sorok: 6 átírt szöveg a 4 .md fájlban, adatsor nem törlődött; a sorszám-Δ a main-hez az előző kör listájával azonos; a ⛔ pontok betartva, a C nem indult |

**ELTÉRÉS-ek:** nincs.

**Megjegyzések (nem eltérések):**
- `naplok/F22_2Kor_jelentes.md:70`: „`ELLENOR_F22_2KOR_2.md` (ha készül)” elavult, a 3. körre nincs hivatkozás.
- A brief `ir` mezőjében a `naplok/ELLENOR_F22_2KOR.md` kétszer szerepel.
- Nem ellenőrizhető az ellenőrnek: az ÚSZ-szintű „nincs eredeti vers nélküli hely” állítás és a `feladatok.py ellenoriz` futása.

## Rendezés (F22.28)

A két apróság rendezve: a 2Kor-jelentés 6. szakasza a 3. kört is megnevezi; az `ir` mezőből a duplikált `naplok/ELLENOR_F22_2KOR.md` kikerült, az `ELLENOR_F22_2KOR_3.md` bekerült. A „nincs eredeti vers nélküli hely” állítás a végrehajtó lekérdezésével igazolt: az `f22/versmegfeleltetes.tsv`-ben 0 `nincs_eredeti` sor.
