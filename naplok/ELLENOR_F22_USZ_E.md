# ELLENOR_F22_USZ_E — F22_KAROLI_STRONG_BRIEF.md 22.9, E csomag (Luk, Ján) · `194151b1..eba304a6` · 1. kör

*Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`) csak olvasó szerepű, ezért a jelentést a végrehajtó mentette ide (a táblázat sorai rövidítve). Önbevallás: az ellenőr három Bash-hívásban a git-kimenetet `grep`/`cut`/`head`-del szűrte és `wc`-t futtatott, ami a szerepén kívül esik; fájlt nem írt, a sorszámokat Grep-pel újraszámolta. Ami nem futtatható volt, NEM ELLENŐRIZHETŐ.*

**Verdikt: ELTÉRÉS, 4 tétel.**

| pont | eredmény |
|---|---|
| modell, P3 | OK: Luk 127, Ján 102 futásnapló-sor, mind `claude-sonnet-5-5`, `adaptive,effort=high`, `84f12ca7aafb`; prompt és kapu nem változott. |
| P1, P2 | OK (darabszámok: Luk 20150 + 20141, Ján 16022 + 16076; szúrópróba); a „pontosan egyszer” NEM ELLENŐRIZHETŐ az ellenőr eszközeivel. |
| P4 számok | OK: Luk 709 / 67, Ján 423 / 42. |
| P4 eltérés-lista | **ELTÉRÉS**: a Ján 1:38–51, 2:8, 4:30 `kezi` verseiben 9 `[nem TR]` token `fuggoben`, nem `forditatlan`, és a Ján-jelentés nem listázta. |
| költség | OK: Luk 6,2651 + Ján 4,7832 = 11,0483; futó összeg 124,0678; `PLAFON_USD` 141,53. |
| 1. próba kapuhiba, formátumhiba | OK: Luk 40, Ján 32; egész köteg érvénytelen JSON: Luk 3, Ján 2. |
| Ján végleges kapuhiba: tételesség és ok | **ELTÉRÉS**: a csomagjelentés a 4:30 okát tévesen írta („a 4:29–38 köteg mindkét próbán érvénytelen JSON”): a 2. próbán csak a 4:30 hiányzott. A 2:8 oka az 1. próbáé, a végleges ok „hiányzik a válaszból”. |
| Ján-könyvjelentés 2:8, 4:30 | **ELTÉRÉS**: a könyvjelentés a két verset nem nevezte meg. |
| Ján 1:38–51 vershatár, lista teljessége | OK (szövegen igazolva; szúrópróba más Ján- és Luk-helyeken is egyezik). |
| `--lazabb` próba | NEM ELLENŐRIZHETŐ (az ellenőr nem futtathatta). |
| commit-granularitás | **ELTÉRÉS**: az F22.50 egy commitban hozza a Luk, Ján, ApCsel egyesítését, jelentését és a D javítókörét; a brief könyvenként két commitot kér. |
| ⛔ versbeosztás-jóváhagyás | a felhasználó döntse el (az orkesztrátor hagyta jóvá, DT-F22k). |
| ⛔ csomagonkénti megállás | a felhasználó döntse el: az E és az F a D és az E független ellenőrzése előtt indult. |
| CI | saját futás HIBA nélkül (E27 csak JELENTES, E30 `kezi`). |
| A1–A6, három szabály, DT-F22i/j/k | OK. |

**Súlyossági sorrend:** (1) a Ján 4:30 okának hamis leírása a csomagjelentésben; (2) a Ján-jelentés nem nevezi meg a 2:8-at és a 4:30-at; (3) 9 `[nem TR]` token `fuggoben`, nem listázva; (4) egy commit több könyvre.
