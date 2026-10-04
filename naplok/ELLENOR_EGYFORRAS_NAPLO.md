# ELLENOR — #26 EGYFORRAS_NAPLO

Brief: `F26_EGYFORRAS_NAPLO_BRIEF.md` · tartomány: `eccaf3e..c20b4a4` · ág: `claude/f26-egyforras-naplo`
Commitok: 608a89b F26.1, 2cd7604 F26.2, b4517e7 F26.3, 69d981c F26.4, ae45e9e F26.5, c20b4a4 F26.6

**Ítélet: JAVÍTANDÓ — 3 eltérés** (1 magas, 1 közepes, 1 alacsony). A merge a felhasználó döntése.

*A jelentést a `fuggetlen-ellenor` állította össze; a szerepe csak olvasás, ezért a fájlt az orkesztrátor írta ki és commitolta, tartalmi változtatás nélkül. A `feladatok.py` futtatását az ellenőr szerepszabálya nem engedte; az orkesztrátor futtatta (l. lent).*

## Eltérések

1. **(magas) Az N2 és a D38 ütközik a DT-F32a-val.** A diff után F12 `fugg: [9, 23]` (a 11 kikerült), F11 `fugg: [9, 12, 23]`. A DT-F32a (🟢, 2026.10.04, a brief v1-nél frissebb): „#12b élesítés: az eredeti helyén marad (#5, #8, #11 után) … a #12 briefje/sora változatlan”. Forrás: `F12_TEREMT002_PROZA_BRIEF.md:10`, `F11_MIGRACIO_BRIEF.md:11`, `DONTESEK.md` DT-F32a. A hiba oka a brief elavultsága, nem a végrehajtás. → **DT-F26b**
2. **(közepes) Az F10 `kovetkezo` mezőjéből kiesett az előfeltétel:** „Előfeltétel: a #8 négy nyitott sora (LD008, LD009, LD058, LD064) eldöntve”. A feltétel él (`adat/lxx_dontesek.tsv`: LD009, LD064 `nyitott`); a #8 `lezarva`, tehát a `fugg: [8]` nem hordozza; a DT2 nem idézi; csak a `naplok/F08_zaras.md:11` őrzi. A brief betűje írta elő. → **DT-F26c**
3. **(alacsony) A DT-F26a ✅-ot kapott**, de a #11-re háruló átnevezés (fájlok, sablonok, `tematikus_lezart/`) az F11-ben nincs rögzítve. → az orkesztrátor a DT-F26a-t 🟢-re állította vissza „Részben alkalmazva” jegyzettel.

## Rendben

| pont | eredmény | hivatkozás |
|---|---|---|
| GENERÁLT blokkok | OK — egyetlen hunk (`@@ -174,0 +175,8 @@`), a kézi „Döntésnapló” szakaszban | `FELADATOK.md:175-182` |
| N1 / D34 | OK — az új nevekkel (motívumcikk, tanulmány = igeszakasz-tanulmány); az „Elvetett alternatíva” oszlopban a régi név maradt, a „(a volt …)” megfeleltetés miatt nem eltérés | `FELADATOK.md:175` |
| N1 / D35–D41 | OK — #MF=23, #LIC=24, #HTML=25 (`^kod:` alapján); D36–D39 betűre a brief szerint | `FELADATOK.md:176-182` |
| D34–D41 számok | OK — a döntésnaplóban szabadok voltak (D33 → D42); `F29_SZOTAR_FORD_NAPLO_BRIEF.md:40` is így számol; F23/F24/F25, `adat/licencek.tsv:1`, `adat/SEMA.md:852` már ezekre hivatkozik. Az F05-lokális D34–D41 külön névtér, az F51 ismert ütközésként kezeli; előzmény, nem ez a diff hozta | `F05_SZOTAR_BRIEF.md:356-364`, `F51_KONZISZTENCIA_BRIEF.md` |
| N2 F09/F10/F11/F12 | OK a brief betűje szerint — csak a megadott mezők és a csonk-sor, egyeznek (numstat 3/3, 3/3, 5/5, 3/3) | — |
| N3 `CLAUDE.md` | OK — a brief szövege + a DT-F26a névmondata, a Rétegek-tábla alatt | `CLAUDE.md:35` |
| N4 `BRIEF_SABLON.md` | OK — betűre | `BRIEF_SABLON.md:56` |
| DONTESEK.md | OK — csak a DT-F26a sor változott (numstat 1/1) | — |
| Táblák (E17) | OK — `adat/*.tsv`, `konkordancia/*.tsv` Δ = 0 | — |
| CI-szabályok | OK — `eszkozok/ellenorzes/futtat.py --diff-alap eccaf3e --diff-fej HEAD`: E2–E16, E19 0 találat | — |
| A1–A6 | OK / nem releváns (nincs adatállítás, nincs próza) | — |

## Orkesztrátori futtatás (4.1–4.2)

- `python eszkozok/feladatok.py ellenoriz` → `71 brief, 0 hiba, 3 figyelmeztetés` (előzmény: F09, F36 E18; F37 helyettesítő minta)
- `python eszkozok/feladatok.py fuggesek` → `KOR` sor: 0. Sorrend a fejlécekből: #23 → #9 → #12 → #11 → #10 (`FUGGES 9 23`, `12 9`, `12 23`, `11 9`, `11 12`, `11 23`, `10 8`, `10 9`, `10 11`, mind `kezi`). Az 1. eltérés éppen ezt a #12 → #11 sorrendet kérdőjelezi meg.


---

## 2. kör — a DT-F26b és a DT-F26c alkalmazása

Az eredmény: 2 eltérés. Tartomány: `ec88b59..752b01a`, ág: `claude/f26-egyforras-naplo`, commitok: ace9cab, 1b293e5, 64eec1e, d496c26, b2d6fef, 752b01a. Az ellenőr csak olvasott; ezt a szakaszt az orkesztrátor fűzte a naplóhoz az ellenőr szövegéből, a saját futtatásával kiegészítve.

| pont | eredmény | indok |
|---|---|---|
| (1) Az F12 fejléce és csonk-sora egyezik a main-nal | OK | `git diff origin/main HEAD -- F12_TEREMT002_PROZA_BRIEF.md` üres |
| (2a) Az F11 `fugg`-jából kikerült a 12 | OK | `[9, 12, 23]` → `[9, 23]` (64eec1e) |
| (2b) Az F11 többi mezője | **ELTÉRÉS (közepes)** | Az F11 `kovetkezo` mezője és csonk-sora (10. és 19. sor): „brief a #12 után”. Ez ellentmond az F12 `fugg: [11]` értékének és a DT-F26b „#12b a #11 után” szövegének. A mondat az N2-ből maradt; a DT-F26b betűje csak a `fugg`-ot írta elő. |
| (3) A D38 sor | OK | A változás csak a kézi Döntésnaplóban van (FELADATOK.md:179), a GENERÁLT blokkokhoz nem nyúlt. |
| (4) Az F10 előfeltétele | OK | A main-beli mondat szó szerint került vissza; LD009 és LD064 ma is `nyitott`. |
| (5) DONTESEK | OK | A DT-F26b és a DT-F26c ✅, a hash-ek valósak, a DT-F26a 🟢 maradt. |
| (6) `feladatok.py` | OK (orkesztrátor) | `ellenoriz`: 71 brief, 0 hiba, 3 figyelmeztetés (F09, F36, F37 — korábbiak); `fuggesek`: 0 KOR. |
| (7) Hatókörön kívüli változás | OK | 6 fájl, 11/11 sor, nincs `.tsv`, nincs kódolási csere. `futtat.py` E2–E16 és E19: 0 találat. |
| Commit-üzenet | **ELTÉRÉS (alacsony)** | A 64eec1e üzenete a D38 kiegészítését is állítja, de az a d496c26-ban történt. A DONTESEK.md jól hivatkozik. |

Megjegyzés: az ág az `origin/main` mögött van (F43 merge: eddfc83, cb1cf76), ezért a DONTESEK.md-ben, a FELADATOK.md-ben és a NYITOTT_FELADATOK.md-ben ütközés lehetséges; a PR előtt rebase szükséges.
