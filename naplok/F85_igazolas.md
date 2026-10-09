# F85_igazolas.md — az átkulcsolás és a kivezetés utólagos igazolása

*Generálta: `eszkozok/tahot_verskulcs_igazolas.py` (csak olvas). Alap: `8ce6e95c~1` (az átkulcsolás előtti állapot). Összesen 45 vizsgálat, 4 HIBA.*

| pont | tárgy | eredmény | részlet |
|---|---|---|---|
| a | sorszám (régi/új) | OK | 469302 / 469302 |
| a | eltérő sorok = a napló sorai (sorszám szerint) | OK | 6330 eltérő sor, 6330 naplósor |
| a | az eltérés csak az Igehely mezőben | OK |  |
| a | a napló régi/új kulcsa a két fájl kulcsaival egyezik minden sorban | OK |  |
| a | nem érintett sorok bájtazonosak | OK | 462972 sor |
| b | a mai pipeline betölt (KeyError nélkül) | OK | versmegfeleltetes sorok: 0, osszevonas sorok: 0 |
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
| c | parok/szavak sorai: 1Krón | OK | repó 15344/32018 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 1Móz | OK | repó 31613/61716 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 1Sám | OK | repó 20152/40376 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 2Krón | OK | repó 20341/41218 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 2Móz | OK | repó 24487/49396 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 2Sám | OK | repó 16499/33213 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 3Móz | OK | repó 18347/36655 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: 4Móz | HIBA | repó 24695/49211 sor; régi pipeline = repó: True; új pipeline = repó: False; eltérő versek (1): 4Móz 29:39 |
| c | parok/szavak sorai: 5Móz | OK | repó 23392/45447 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Bír | OK | repó 14939/29913 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Eszt | OK | repó 4500/9062 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Ez | OK | repó 28852/56397 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Ézs | HIBA | repó 25488/50069 sor; régi pipeline = repó: True; új pipeline = repó: False; eltérő versek (2): Ézs 64:1, Ézs 9:20 |
| c | parok/szavak sorai: Ezsd | OK | repó 5533/10989 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Jer | OK | repó 32797/64563 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Jób | HIBA | repó 13420/26225 sor; régi pipeline = repó: True; új pipeline = repó: False; eltérő versek (2): Jób 16:22, Jób 36:33 |
| c | parok/szavak sorai: Józs | OK | repó 15023/30405 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | parok/szavak sorai: Péld | HIBA | repó 10761/21781 sor; régi pipeline = repó: True; új pipeline = repó: False; eltérő versek (1): Péld 11:31 |
| c | parok/szavak sorai: Zsolt | OK | repó 32189/61064 sor; régi pipeline = repó: True; új pipeline = repó: True |
| c | adat/ (benne parok_*/szavak_*) a git szerint változatlan az átkulcsolás előtti állapothoz képest | OK | 38 adat/karoli_strong fájl |
