# Ellenőri jelentés — F19 (KJV/ASV-import, eBible)

*fuggetlen-ellenor, 2 kör; a jelentést az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze).*

## 1. kör — ELTÉRÉS: 8 tétel (HEAD 4d8833d)
1. Az `ASV_Strongs_teljes.tsv` héber címkéi hibásak (H430, H776, H1 = 0; H3068 = 51 517; 1Móz 1:1 „God” → H8064).
2. Az ASV 108 „adathiány” sora nagyrészt versszámozási eltolás (MT/KJV); a szomszédos versek Strongjai is elcsúsznak.
3. A DT19 (b) magyarázata (függvényszó-konvenció) bizonyítatlan volt.
4. Az N29 lezárása idő előtti.
5. A szerepmátrix `sorrend=13` sora a SEMA 2.13-at sérti.
6. A DT19 (d) „nem frázis” a KJV-re nem igaz (9328 többszavas sor).
7. Hiányzott a proveniencia-sor a számok mellől.
8. A brief fejléce lezáratlan (M7; a zárásnál az orkesztrátor végzi).

Javítás: F19.3 (`0595c30`). Igazolt tény: a nyers eBible ASV-USFM-ben is 0 db H430/H776/H1/G746 — a forrás hibás, a parszoló hű; az ASV-tábla `javaslat`, tartalmi keresésre nem használható.

## 2. kör — ELTÉRÉS: 6 tétel (HEAD 0595c30); az 1. kör mind a 8 leletét megoldottnak találta
1. `adat/datasetek.tsv` glob beveszi a forráshibás ASV_teljest → F19.4-ben javítva (a 6 Genezis/Exodus/Péld fájl felsorolva).
2. 2Kor 13:14 (ASV) versszámozási eset, nem adathiány → ÚSZ-szabály (Károli-összevetés), táblázat és DT19 (a) javítva.
3. A KJV állapota háromféle → egységesen `importált, javaslat`.
4. A generátor konstansokat ír a fejlécbe; a hiánytáblán nincs `# GENERÁLT` → `manual` jelölés és `# GENERÁLT`.
5. Szerepmátrix: két meglévő sor módosítva (M2) → **marad**, a DT19 (f) dokumentálja.
6. DT19 (c): ASV-felirat 0. vers pontosítás → javítva (a Hab 3:0 az egyetlen 0. versű ASV-sor).

Javítás: F19.4 (`041398d`). Az ellenőr által „NEM ELLENŐRIZHETŐ”-nek jelölt: a fejezetszintű eltolás-szabály soronkénti helyessége (heurisztika, a DT19-ben jelölve), a KJV/luvlylavnder licenc-fájl hiánya a repóban.
Gépi ellenőrzés: `eszkozok/ellenoriz.py` 11 RENDBEN / 0 SÉRTÉS; CI E2–E10, E12–E16: 0 találat (E11: örökölt Cremer-sor, nem F19).

**Összegzés: a 2. kör után a maradék (5. pont) dokumentált; nincs blokkoló lelet. Kézi döntés kell: DT19.**
