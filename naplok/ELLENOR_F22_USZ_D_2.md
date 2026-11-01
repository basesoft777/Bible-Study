# ELLENOR_F22_USZ_D_2 — F22_KAROLI_STRONG_BRIEF.md 22.9, D csomag (Mt, Mk) · `194151b1..eba304a6` · 2. kör

*Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`) csak olvasó szerepű, ezért a jelentést a végrehajtó mentette ide (a táblázat sorai rövidítve).*

**Verdikt: ELTÉRÉS, 4 tétel (az 1. kör 10 tételéből 6 teljesen rendben).**

| pont | eredmény |
|---|---|
| (1) `NYITOTT_FELADATOK.md` sorvége, CI | OK: a `main`-hez képest 1/1 sor; a `futtat.py` kilépési kód 0, HIBA nincs. |
| (2) formátumhiba | OK: Mt 9 + Mk 1 = 10 egész köteg, a `_munka/*.json`-ból igazolva; a szám szkriptből jön. |
| (3) P6 | OK: `datasetek.tsv` és `SEMA.md` a 27 ÚSZ-könyvet felsorolja. |
| (4) brief `ag`, `kovetkezo`, `allapot`, v2.47, 22.9 bekezdés | OK; `ir` mező **ELTÉRÉS** (enyhe): 21 írt fájl hiányzott; a 22.9 címe nem frissült. |
| (5) Mt 11:19 / G2041 | **ELTÉRÉS**: a Mt-jelentés csak a táblasort tartalmazta, a lexikai hibát nem mondta ki. |
| (6) DONTESEK formailag | OK: 8 oszlop, helyőrzők. |
| (7) Ján 1:51 | OK (adattal igazolva). A `kezi_versek_Jan.tsv` DT-hivatkozása (DT-F22j) **ELTÉRÉS** (enyhe): az A út a DT-F22k (2). |
| granularitás | **ELTÉRÉS** (enyhe): az F22.47/F22.48 két könyvet, az F22.50 az E-t, F-et és a D javítókört egy commitban hozza. |
| E17/DT3 sorszám-Δ, kulcstartomány | OK. |
| ⛔ versbeosztás | a felhasználó döntse el (DT-F22k). |

**Javítás a 2. kör után (F22.51):** az Mt-jelentés a lexikailag hamis linket kimondja; az `ir` mező és a 22.9 címe frissítve; a `kezi_versek_*` hivatkozások DT-F22k-ra javítva. A granularitás utólag nem pótolható.
