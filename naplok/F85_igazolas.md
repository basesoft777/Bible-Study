# F85_igazolas.md — az átkulcsolás és a kivezetés utólagos igazolása

*Generálta: `eszkozok/tahot_verskulcs_igazolas.py` (csak olvas). Alap: `8ce6e95c~1` (az átkulcsolás előtti állapot). Összesen 81 vizsgálat, 0 HIBA.*

*proveniencia: scope=manual (csak-olvasó összevetés: git show 8ce6e95c~1 vs. a mostani fa; egyesit.epit/ellenoriz memóriában) | forras=konkordancia/TAHOT_kivonat.tsv, naplok/F85_kulcsvaltas.tsv, f22/*.tsv, adat/karoli_strong/*.tsv, f22/valaszok/ | ts=2026-10-09T11:47:08Z*

| pont | tárgy | eredmény | részlet |
|---|---|---|---|
| a | sorszám (régi/új, fejléccel) | OK | 469301 / 469301 sor |
| a | eltérő sorok = a napló sorai (sorszám szerint) | OK | 6330 eltérő sor, 6330 naplósor |
| a | az eltérés csak az Igehely mezőben | OK |  |
| a | a napló régi/új kulcsa a két fájl kulcsaival egyezik minden sorban | OK |  |
| a | nem érintett sorok bájtazonosak | OK | 462972 sor |
| b | a mai pipeline betölt (KeyError nélkül) | OK | versmegfeleltetes sorok: 0, osszevonas sorok: 9 |
| b | jóváhagyott könyvek vers -> héber szavak (régi vs. új pipeline) | OK | 17747 vers, 0 eltérő |
| b | könyv 1Krón | OK | 942 vers, 0 eltérő |
| b | könyv 1Sám | OK | 811 vers, 0 eltérő |
| b | könyv 2Krón | OK | 822 vers, 0 eltérő |
| b | könyv 2Móz | OK | 1213 vers, 0 eltérő |
| b | könyv 2Sám | OK | 695 vers, 0 eltérő |
| b | könyv 3Móz | OK | 859 vers, 0 eltérő |
| b | könyv 4Móz | OK | 1287 vers, 0 eltérő |
| b | könyv 5Móz | OK | 959 vers, 0 eltérő |
| b | könyv Bír | OK | 618 vers, 0 eltérő |
| b | könyv Eszt | OK | 167 vers, 0 eltérő |
| b | könyv Ez | OK | 1273 vers, 0 eltérő |
| b | könyv Ezsd | OK | 280 vers, 0 eltérő |
| b | könyv Jer | OK | 1364 vers, 0 eltérő |
| b | könyv Jób | OK | 1068 vers, 0 eltérő |
| b | könyv Józs | OK | 658 vers, 0 eltérő |
| b | könyv Péld | OK | 914 vers, 0 eltérő |
| b | könyv Zsolt | OK | 2527 vers, 0 eltérő |
| b | könyv Ézs | OK | 1290 vers, 0 eltérő |
| c | parok/szavak sorai: 1Krón | OK | repó 15344/32018 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: 1Móz | OK | repó 31613/61716 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: 1Sám | OK | repó 20152/40376 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: 2Krón | OK | repó 20341/41218 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: 2Móz | RÉSZBEN | repó 24487/49396 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/False, szavak True/False, atnezes True/True; a sorok és az átnézési napló bájtazonosak, CSAK a proveniencia-sor (forras=) tér el (az f22/versmegfeleltetes*.tsv már nem forrás) |
| c | parok/szavak sorai: 2Sám | OK | repó 16499/33213 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: 3Móz | OK | repó 18347/36655 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: 4Móz | RÉSZBEN | repó 24695/49211 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/False, szavak True/False, atnezes True/True; a sorok és az átnézési napló bájtazonosak, CSAK a proveniencia-sor (forras=) tér el (az f22/versmegfeleltetes*.tsv már nem forrás) |
| c | parok/szavak sorai: 5Móz | OK | repó 23392/45447 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Bír | OK | repó 14939/29913 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Eszt | OK | repó 4500/9062 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Ez | OK | repó 28852/56397 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Ézs | RÉSZBEN | repó 25488/50069 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/False, szavak True/False, atnezes True/True; a sorok és az átnézési napló bájtazonosak, CSAK a proveniencia-sor (forras=) tér el (az f22/versmegfeleltetes*.tsv már nem forrás) |
| c | parok/szavak sorai: Ezsd | OK | repó 5533/10989 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Jer | OK | repó 32797/64563 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Jób | RÉSZBEN | repó 13420/26225 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/False, szavak True/False, atnezes True/True; a sorok és az átnézési napló bájtazonosak, CSAK a proveniencia-sor (forras=) tér el (az f22/versmegfeleltetes*.tsv már nem forrás) |
| c | parok/szavak sorai: Józs | OK | repó 15023/30405 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| c | parok/szavak sorai: Péld | RÉSZBEN | repó 10761/21781 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/False, szavak True/False, atnezes True/True; a sorok és az átnézési napló bájtazonosak, CSAK a proveniencia-sor (forras=) tér el (az f22/versmegfeleltetes*.tsv már nem forrás) |
| c | parok/szavak sorai: Zsolt | OK | repó 32189/61064 sor; régi pipeline = repó: True; új pipeline = repó: True; teljes fájl bájtra (régi/új): parok True/True, szavak True/True, atnezes True/True |
| e | összevonás szétválasztása: 4Móz 29:39 (fő: 4Móz 29:39, extra: 4Móz 30:1) | OK | fő 30 token, extra 13 token |
| e | összevonás szétválasztása: Jób 16:22 (fő: Jób 16:22, extra: Jób 17:1) | OK | fő 9 token, extra 9 token |
| e | összevonás szétválasztása: Jób 36:33 (fő: Jób 36:33, extra: Jób 37:1) | OK | fő 9 token, extra 11 token |
| e | összevonás szétválasztása: Péld 11:31 (fő: Péld 11:31, extra: Péld 12:1) | OK | fő 10 token, extra 8 token |
| e | összevonás szétválasztása: Ézs 9:20 (fő: Ézs 9:19, extra: Ézs 9:20) | OK | fő 18 token, extra 23 token |
| e | összevonás szétválasztása: Ézs 64:1 (fő: Ézs 64:1, extra: Ézs 64:2) | OK | fő 9 token, extra 19 token |
| e | összevonás szétválasztása: Hós 1:11 (fő: Hós 1:11, extra: Hós 2:1) | OK | fő 23 token, extra 11 token |
| e | összevonás szétválasztása: Hós 11:11 (fő: Hós 11:11, extra: Hós 12:1) | OK | fő 19 token, extra 20 token |
| e | összevonás szétválasztása: Préd 2:26 (fő: Préd 2:26, extra: Préd 2:25) | OK | fő 38 token, extra 9 token |
| n | negatív próba: Péld 11:31 er_tol–er_ig 11–18 -> 10–17 (határon belüli, de rossz tartomány) | OK | BUKOTT, ahogy kell: Péld 11:31: fő vers egyezik: False, extra egyezik: False (fő 10, extra 8 token) |
| n | negatív próba: Hós 11:11 er_tol–er_ig 20–39 -> 1–19 (a fő vers és az extra felcserélve) | OK | BUKOTT, ahogy kell: Hós 11:11: fő vers egyezik: False, extra egyezik: False (fő 20, extra 19 token) |
| n | negatív próba: Ézs 64:1 er_ig 28 -> 99 (a tokenlistán kívüli tartomány) | OK | BUKOTT, ahogy kell: SystemExit: versosszevonas.tsv: Ézs 64:1 er_tol–er_ig (10–99) nem fér a kulcs 28 tokenjébe |
| n | ugyanaz az ellenőrzés a valós (nem rontott) bemeneten | OK |  |
| d | a kivezetett 3 kézi sor (Ézs 9:20 nincs_karoli, Ézs 64:1 torol x2) visszaállítva: a betöltés változatlan | OK | 0 eltérő kulcs |
| g | Hós/Préd betolt_eredeti() eltérése a nyers listától = a 3 várt összevonás | OK | Hós 11:11: nyers 39 -> fő 19 + extra 20 token; Hós 1:11: nyers 34 -> fő 23 + extra 11 token; Préd 2:26: nyers 47 -> fő 38 + extra 9 token |
| g | a többi könyvben csak a 6 futott összevonás kulcsa tér el a nyerstől | OK | 4Móz 29:39, Jób 16:22, Jób 36:33, Péld 11:31, Ézs 64:1, Ézs 9:20 |
| f | egyesit.ellenoriz: 1Krón | OK | rendben |
| f | egyesit.ellenoriz: 1Móz | OK | rendben |
| f | egyesit.ellenoriz: 1Sám | OK | rendben |
| f | egyesit.ellenoriz: 2Krón | OK | rendben |
| f | egyesit.ellenoriz: 2Móz | OK | rendben |
| f | egyesit.ellenoriz: 2Sám | OK | rendben |
| f | egyesit.ellenoriz: 3Móz | OK | rendben |
| f | egyesit.ellenoriz: 4Móz | OK | rendben |
| f | egyesit.ellenoriz: 5Móz | OK | rendben |
| f | egyesit.ellenoriz: Bír | OK | rendben |
| f | egyesit.ellenoriz: Eszt | OK | rendben |
| f | egyesit.ellenoriz: Ez | OK | rendben |
| f | egyesit.ellenoriz: Ézs | OK | rendben |
| f | egyesit.ellenoriz: Ezsd | OK | rendben |
| f | egyesit.ellenoriz: Jer | OK | rendben |
| f | egyesit.ellenoriz: Jób | OK | rendben |
| f | egyesit.ellenoriz: Józs | OK | rendben |
| f | egyesit.ellenoriz: Péld | OK | rendben |
| f | egyesit.ellenoriz: Zsolt | OK | rendben |
| f | egyesit.ellenoriz összesen | OK | 19 könyv |
| c | adat/ (benne parok_*/szavak_*) a git szerint változatlan az átkulcsolás előtti állapothoz képest | OK | 38 adat/karoli_strong fájl |
