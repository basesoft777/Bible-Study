# ELLENOR_F22_4Moz.md

*A `fuggetlen-ellenor` ügynök jelentése (tartomány: `claude/f22-2moz...77ba110`, worktree `Bible-Study-f22`), tömörítve; az ügynök szerepköre csak olvasó volt (az `egyesit.py` futtatását nem végezhette), a fájlt az orkesztrátor mentette. A „Kezelés” szakasz az orkesztrátoré.*

**Minősítés: ELTÉRÉS: 3 tétel (közepes 1, alacsony 2); minden többi pont OK.**

## Rendben (OK)
- K1/K2: 1 287 vers, 129 köteg mind kész; szavak: hu 24 330 (19 885 parositva, 4 431 betoldas, 14 fuggoben), er 24 881 = a TAHOT 4Móz tokenjei (a beolvasztott TAHOT 30:1 13 tokenje is), összesen 49 211; a TAHOT 30:1 Strongjai sorrendben egyeznek.
- A négy kért ellenőrzés: a 30. fejezet 16 verse a TAHOT 30:(n+1) tokenjeivel (kézi szúrópróba 30:1, 30:2, 30:13, 30:16; `er` 392 = 405 − 13), `kezi` a 30. fejezetben 0; a 29:39 hu 25–38 mind `fuggoben`/`kezi`, `betoldas` 0, a `parok` táblában 0 sor; `30:1001` táblában, jsonl-ben, mintában nincs; a jóváhagyási napló a kért tartalommal megvan; a TAHOT 29:40 nem létezik, a Károli 30. fejezet 16 verses.
- Csak-Sonnet: parok 24 695 / szavak 49 184 `alacsony`/`S` (+27 `kezi`), nincs C-jsonl, `ts=manual`; kapuhiba 12/1287, végleg 0; régi arany 3/3.
- 1–3Móz táblák/jsonl/minta, `f21p/` változatlanok; a jóváhagyott lista `2Móz, 3Móz, 4Móz`, a 4Mózesre csak a 30. fejezet sorai; kulcs-grep, zárt licencű adat, datasetek, brief D10/v2.4/ir/kovetkezo rendben; a CI-futtató E2–E16, E19: 0 találat.
- Nem ellenőrizhető az ügynöknek: `egyesit.py --ellenoriz`, K7, /usage (65%→74%), köteg előtti hash-ellenőrzés.

## Eltérések és Kezelés
| # | Eltérés | Kezelés |
|---|---|---|
| 1 | (közepes) a 4Móz-táblák proveniencia-sorából hiányzik az `f22/versosszevonas.tsv` | **Javítva:** `egyesit.proveniencia_sor` a kézi beolvasztás fájlját is megnevezi (csak ahol a könyvnek van sora; az 1–3Móz sora változatlan); a 4Móz táblái újraépítve, `--ellenoriz` rendben. |
| 2 | (alacsony) SEMA: a `4Móz 30:1001` példa már nem létezik | **Javítva** (a SEMA kimondja, hogy a jelenlegi listában +1000-es azonosító nincs). |
| 3 | (alacsony) brief `ag: claude/f22-2moz` | **Javítva:** `ag: claude/f22-4moz`. |
| — | Megjegyzés: a `szur` a kiszűrt hu-tokenek linkjeit némán eldobja; ha egy eredeti token csak ilyenhez kötődött, `forditatlan` lesz, nem `kezi` (a 29:39-ben nem fordult elő); a `versosszevonasok()` a jóváhagyott listától független | **Nyitva, dokumentálva** (N-F22); a 4Mózesre nem aktív. |

**Második független kör az 1. kör után nem készült.**
