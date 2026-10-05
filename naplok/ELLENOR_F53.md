# ELLENOR_F53 — F53_FELADATTERKEP_BRIEF.md · cd62733..a596346

*A `fuggetlen-ellenor` jelentése (2026-10-05). Az ügynöknek nem volt fájlíró
eszköze, ezért a jelentést a végrehajtó másolta ide; a végrehajtó pótlása a
végén külön szakaszban áll.*

Base: `cd62733` (az `origin/main` csúcsa, a `git log --boundary origin/main..a596346`
határa). A tartomány 12 commit (`08f5825`…`a596346`).

## Eredmény: ELTÉRÉS, 4 tétel

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 7.1 idempotencia | NEM ELLENŐRIZHETŐ (az ügynöknél) | `eszkozok/feladatterkep.py` | a generátor és a teszt futtatása kívül esett a megengedett parancsokon; időbélyeg-minta (`\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}`, `\d{2}:\d{2}:\d{2}`) a két kimenetben: 0 találat; a teszt létezik (`teszt_feladatterkep.py:192`, `test_ketszer_azonos_bajtok`) |
| 7.1 bélyeg: a commitolt kimenet = friss generálás a HEAD-en | ELTÉRÉS | `feladatterkep.json:11`, `FELADATTERKEP.html:325` | a `belyeg()` (`feladatterkep.py:335`) `git log -1 -- <BELYEG_FORRASOK>`-t futtat; a HEAD-en ez `a596346`, a commitolt kimenetben `7d55ed7` áll. Rendszerszintű: ha egy commit forrást és kimenetet együtt ír, a bélyeg egy commitot késik (a saját hash generáláskor még nem ismert) |
| 7.1 a bemenet teljessége | ELTÉRÉS (alacsony) | `feladatterkep.py:349`; `feladatok.py:410-418` | az `F.main_allapotok()` az `origin/main` fejléceit olvassa; az `origin/main` nincs a `BELYEG_FORRASOK`-ban, így azonos bélyeg mellett a kimenet a helyi fetch idejétől függhet |
| 7.2 a DONTESEK minden nem ✅ tétele megjelenik | OK | `feladatterkep.json:848-1133` | 6 🟡 + 23 🟢 a DONTESEK-ben; a JSON-ban 6 nyitott + 23 alkalmazásra vár + 4 ellenőrizendő = 33 |
| 7.2 / 7.5 a kis minta számadata | ELTÉRÉS (alacsony) | `naplok/F53_kis_minta_eltereslista.md:72` | a minta „22 tétel” alkalmazásra vár, a HEAD-beli JSON-ban 23; valószínűleg a main behúzása (`5c7abe2`) után jött be |
| 7.3 nem pótol | OK | `feladatterkep.json:1141-1182`; `eszkozok/feladatterkep_kartyak.tsv` | DT1, DT3, DT4, DT19 `ellenőrizendő`; a TSV 31 sora `kezi-2026-10-05`; a 10 „nincs leírás” kártya egyezik |
| 7.4 a `csv` nincs importálva | OK | `feladatterkep.py:29-41` | `^\s*(import\|from)\s+csv`: 0 találat; `split('\t')` (`:87`, `:92`); UTF-8 wrapper az importok után |
| 7.5 kis minta jóváhagyva | OK (dokumentálva) | eltéréslista `:133-141`; brief 9. | sorrend: `47a36c4` → `3bcf666` → `5b7c305`; a jóváhagyás chatben |
| 7.6 Action | NEM ELLENŐRIZHETŐ | — | csak merge után |
| 7.7 artifact / FT.5 ⛔ | OK | napló; brief 9.; N-F53f | (c) döntés dokumentálva; feltöltés nem történt |
| 7.8 `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ (az ügynöknél) | — | l. a pótlást |
| 7.9 / FT.7 nem indul | OK | brief 9.; napló | `eszkozok/main_frissit.py` nem létezik; ütemezett feladat nem jött létre |
| FT.3 GENERÁLT-fejléc, kinézet | OK | `FELADATTERKEP.html:7`, `:122`, `:387` | `GENERÁLT`-jelölés, `data-tema`, `zoom:1.1`, `mermaid@11.16.1` |
| FT.4 a workflow-diff | OK | `.github/workflows/feladatok.yml:54-65` | +6/−3, csak a jóváhagyott változás |
| FT.4 nincs hurok | OK | `feladatterkep.py:49`; `feladatok.yml:27` | a `BELYEG_FORRASOK`-ban nincs FELADATOK.md és kimenet; a `[bot]`-feltétel is véd |
| FT.4 ⛔ jóváhagyás a módosítás előtt | NEM ELLENŐRIZHETŐ | brief 9. | chatben; a döntésnapló-sort csak az `a596346` vette fel |
| D (brief 9.) | OK | brief 9. | a fejléc, a napló és a NYITOTT konzisztens |
| brief verziósor | ELTÉRÉS (alacsony) | `F53_FELADATTERKEP_BRIEF.md:22` | a tartalom változott, a verziósor „v1.1” maradt |
| A1–A5 | OK / nem alkalmazható | — | folyamatfeladat, értelmező próza nincs |
| A6 E12–E15 | OK | — | `futtat.py`: 0 találat |
| CI | kockázat | `.github/workflows/feladatok.yml` | saját futtatás PR-cím nélkül: E16 HIBA (a PR érinti a `.github/`-ot, a cím nem „[ELLENŐRZŐ]” előtagú); a címmel exit 0 |
| adat/ és konkordancia/ | OK | — | `git diff --numstat -- adat/ konkordancia/`: üres; E17 nem kell |
| ⛔ pontok | OK | — | FT.2, FT.5, FT.7 betartva |

## A végrehajtó pótlása (2026-10-05)

- **7.1, 7.8 lefuttatva** a HEAD-en (`a596346`): `teszt_feladatterkep.py` OK (19 teszt);
  `feladatok.py ellenoriz` 85 brief, 0 hiba; két egymás utáni friss generálás bájtazonos
  (sha1 egyezik). A commitolttól a friss generálás **csak a bélyeg `commit` mezőjében**
  tér el (`7d55ed7` → `a596346`, a JSON-ban és a HTML-ben egy-egy sor) — ez az 1. ELTÉRÉS.
- **E16 (CI piros):** a PR #201 `ellenorzes` checkje a fenti okból bukott. Javítva: a PR
  címe „[ELLENŐRZŐ]” előtagot kapott (formai hiba a saját PR-ból).
- **Az 1. ELTÉRÉS (bélyeg-csúszás)** a branch-en nem javítható commit-hash alapú bélyeggel;
  a main-en az Action a merge után újragenerál, tehát a merge után egy gépi commit
  biztosan keletkezik. Javítási lehetőség (pl. tartalom-alapú bélyeg): a felhasználó
  dönt, külön tételben.
- A 2–4. ELTÉRÉS nem javítva; a felhasználó dönt.
