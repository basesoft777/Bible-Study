# F140 GLOSSZA_FORDITAS — zárójelentés (M2)

*Modell: `claude-sonnet-5-5` (a `modell` mezőben mindenhol ez áll) · 2026-10-25 · ág: `ccr-636782ad-lysuoh`*

Proveniencia: `scope=adat/glosszak_heber_hu.tsv + konkordancia/TBESH.txt | forras=helyi-futtatas (eszkozok/glossza_forditas.py --ellenoriz) | ts=2026-10-25`.

- **Darabszám:** 11 677 sor / 11 677, 8 718 Strong / 8 718 legalább egy sorral; `--ellenoriz`: 0 hiba, 15 teszt zöld; az `adat/forditasok.tsv` érintetlen.
- **Kapuhibák:** a 18.–82. kötegben 9 pár bukott az első rögzítésen (H3724C, H1166H, H4478A/B, H4479, H6163A, H4488, H2104, H4192: angolnak ismert szó vagy tiltott jel); mind az újrafordítás után átment. Elakadó: 0 (`naplok/GLOSSZA_FORDITAS_elakad.tsv` nem jött létre).
- **Bizonytalan** (`?` a `megjegyzes`-ben): 32 sor.
- **Átnézési lista:** `naplok/GLOSSZA_FORDITAS_atnezes.tsv` — a 300 leggyakoribb Strong (TAHOT-előfordulás szerint) minden sora, plusz a kiemelt sorok (96: ismert hiba, H90xx-csoport, 20 homonima-szúróminta, `?` sorok); összesen 846 sor. A javítást a felhasználó a `javitas_hu` oszlopba írja, majd `kezi` sorral kerül a táblába.
- **Egyeztetett eltérés (kontextus-hossz):** az `a Meaning of` árnyalat-soroknál 90 karakteres kontextus (a brief ~200-zal szemben); a 17. köteg előtt kész 20 homonima-sor tévedésből 90-et kapott (`naplok/GLOSSZA_FORDITAS_homonima_szuroproba.tsv`) — ezek az átnézésnél elsők.
- **Ismert hibás sorok** (a szkript védelme miatt a tábla nem módosítható, az átnézési lista `megjegyzes` oszlopa jelzi): H3104 „kos/kürt” (jubileum/kürt), H9045 „-nk” (mi, alany), H4578 „belső” (has), H8577M „kígyó: kígyó”; H6310G ajak/száj eldöntendő; H90xx egységesítendő.
- **K8 (nyitott, merge előtt kötelező):** az `ADAT_LICENC` bejegyzés (`glosszak_heber_hu`: TBESH, TAHOT, projekt_adat) az `eszkozok/sqlite_epit.py`-ban hiányzik; a tábla main-re kerülése előtt külön kisfeladatként el kell végezni (CC BY 4.0 forrásjelölés).
- **Átnézés (a felhasználó jóváhagyta):** 17 javítás és 3 „?” törlés alkalmazva a naplózott `--javit` móddal (`allapot=kezi`, napló: `naplok/GLOSSZA_FORDITAS_javit_naplo.tsv`); a 20 homonima 200 karakteres újrafordításából 2 sor tért el (H1197A, H7760A). Bizonytalan sor most: 20.
- **Hátra:** független ellenőr, majd zárás és PR.
