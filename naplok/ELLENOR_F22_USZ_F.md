# ELLENOR_F22_USZ_F — F22_KAROLI_STRONG_BRIEF.md 22.9, F csomag (ApCsel) és a keret-összesítő · `194151b1..eba304a6` · 1. kör

*Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`) csak olvasó szerepű, ezért a jelentést a végrehajtó mentette ide (a táblázat sorai rövidítve). Ami nem futtatható volt, NEM ELLENŐRIZHETŐ.*

**Verdikt: ELTÉRÉS, 4 tétel.**

| pont | eredmény |
|---|---|
| modell, P3 | OK: 118 ApCsel-sor, mind `claude-sonnet-5-5`, `adaptive,effort=high`, `84f12ca7aafb`. |
| P1 | OK (18800 + 18986 token; a TAGNT 18986 sora egyezik); a „pontosan egyszer” NEM ELLENŐRIZHETŐ. |
| P2, P6 | OK (szúrópróba; `datasetek.tsv`, `SEMA.md`, `VERSBEOSZTAS_JOVAHAGYOTT`). |
| P4 | számok OK (634 / 37); **ELTÉRÉS**: az ApCsel 24:2 er 15 (διορθωμάτων, G1357) `fuggoben`, nem listázva. |
| költség | OK: ApCsel 6,014115; futó összeg 124,067843 → 130,081958; maradék 11,448042. |
| keret | **ELTÉRÉS**: a pontos érték 26,551119, azaz 26,5511 (a jelentés 26,5512-t írt: két kerekített futó összeg különbsége, kézzel beírt szám). |
| verszám 4785, végleges kapuhiba | OK (2/4785: Ján 2:8, 4:30; ApCsel 0/1006). |
| 1. próba kapuhiba 27/1006, javító kör 17 köteg, formátumhiba 1 (k025) | OK. |
| ApCsel 13:32–33, 24:2–3 | OK (szövegen igazolva); további ApCsel-eltolódás szúrópróbán nincs. |
| adatminőség: ApCsel 2:27, 2:31 | **ELTÉRÉS**: az ᾅδην (G0086) mindkét versben `forditatlan`, a „sírban” csak az εἰς-hez kötött, a 2:31 „nem hagyatott” `betoldas`; a régi arany két hibás hármasa (3/5); a jelentés nem nevezte meg. |
| „a meglévő 8 vers” | **ELTÉRÉS**: a meglévő `kezi` vers 10 (a 2Kor 8:13–14 kimaradt), az N-F22e köre 30 vers. |
| ⛔ versbeosztás-jóváhagyás | a felhasználó döntse el (DT436). |
| A1–A6, CI | OK (a CI saját futása HIBA nélkül). |

**Súlyossági sorrend:** (1) ApCsel 2:27, 2:31 (Hádész) hiányos Strong-index, nem nevesítve; (2) „meglévő 8 vers” helyesen 10; (3) P4: a 24:2 `fuggoben` token nincs listázva; (4) 26,5512 helyesen 26,5511.
