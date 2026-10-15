# F93 zárójelentés — a TIPNR token nélküli alapszámai (#93)

- Modell: `claude-sonnet-5-5` (végrehajtó), ellenőr `claude-opus-5-5`; ág: `claude/f93-tipnr-token-hiany`; merge nincs, PR-t az orkesztrátor nyit.
- Kész: a 62 token nélküli alapszám (88 TIPNR-sor; 16 görög, 46 héber) osztályozva és jelölve: `naplok/F93_alapszamok.tsv` (szkript: `eszkozok/f93_tipnr_token_hiany.py`), összesítő: `naplok/F93_jelentes.md`. Jelölés, nem javítás: a források és a `pardes.db` nem változtak.
- Eloszlás (alapszám / sor): szövegváltozat 5/6 (görög), alak-/névhasítás 15/29, fordítási névalak 19/25 (héber), nincs Károli-vers 6/10, nem eldönthető 17/18 (ebből 12 LK/LQ/Mss ketiv/qere-jelölés nélkül); a ketiv/qere, az adathiány és a számozási eltérés osztály üres.
- Egyeztetett eltérés: a brief „62 görög alapszám” hatóköre helyett mind a 62 alapszám (görög TAGNT-ből, héber TAHOT-ból), bővített osztálylistával; az `ir` mezőből kikerült a `sqlite_epit.py`, a `teszt_sqlite_epit.py` és az `adat/SEMA.md` (részletek: a jelentés 2. szakasza).
- Ellenőrzés, négy kör: `ELLENOR_F93.md` 6 eltérés, javítva; `ELLENOR_F93_2.md` 3, javítva; `ELLENOR_F93_3.md` 1, javítva (`ef55c97a`); `ELLENOR_F93_4.md` 2 nem tartalmi eltérés, a zárásban rendezve.
- Döntések: DT-F93a (jelölés a naplóban, hatókör mind a 62), DT-F93b (a héber szövegváltozat megszűnik), DT-F93c (jelölés nélküli görög szövegváltozat csak egyező glosszával), DT-F93d (a `ts` az adatállapot ideje). Nyitott: N-F93a (ketiv/qere LK/LQ jelentése), N-F93b (a `lekerdez.py` néma nem-találata), N-F93c (a TAGNT kiadás-mező „»N” jelölése). Végleges szám a `main`-en lesz.
- G4: két futás bájtazonos, a lista sha256-ja `0c7946c1b40de82e54e684f4292fb369263784f93aaad936770f68819a5ed5a0`; `python eszkozok/feladatok.py ellenoriz`: 0 hiba.
- Megjegyzés: az `F93.21` előtag két commiton áll (`cc7f41db`, `ef55c97a`); a history nem íródott át.
