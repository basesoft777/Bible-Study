---
feladat: 220
cim: A heti áttekintő oldal generátora — sávonként a brief-fejlécekből és a PR-állapotokból
kod: HETI_ATTEKINTO
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SYSTEMS
allapot: fut
ad: egy szkript (`eszkozok/heti_attekinto.py`), amely a brief-fejlécekből és a GitHub PR-okból önálló, olvasói nyelvű HTML-oldalt készít a felhasználónak: fent „A te teendőid”, utána négy sáv (fejlécben `sav`: SYSTEMS / CONTENT / SERVER / USER; a hiányzó vagy ismeretlen érték „besorolatlan”), mindegyikben folyamatban / vár / kész a héten; a kimenet a repón kívülre kerül, a repóba csak a szkript és a tesztje
kovetkezo: "Te: a draft PR áttekintése; a merge a felhasználóé; a `sav` mező bevezetése (másik session) után a próba-oldal újragenerálása"
munka: folyamat
olvas: [CLAUDE.md, eszkozok/feladatok.py]
ir: [eszkozok/heti_attekinto.py, eszkozok/tesztek/test_heti_attekinto.py, eszkozok/teszt_feladatok.py, F220_HETI_ATTEKINTO_BRIEF.md]
fugg: []
nem_fugg: [123, 188, 201]
---

# F220_HETI_ATTEKINTO_BRIEF.md — A heti áttekintő oldal generátora

*FELADATOK #220 · Modell: sonnet · 2026.11.15 · forrás: az orkesztrátor megbízása (2026-11-15); egy orkesztrátor, négy sáv (SYSTEMS, CONTENT, SERVER, USER) — a felhasználó döntése, 2026-11-14.*

**Mit csinál.** Az `eszkozok/heti_attekinto.py` az `eszkozok/feladatok.py` meglévő beolvasó függvényeivel (csak olvasva) beolvassa a brief-fejléceket, a `gh pr list`-ből a nyitott és az elmúlt 7 napban egyesített PR-okat, és egyetlen HTML-oldalt ír a `--kimenet` helyére (a repón kívülre; a repón belüli útvonalat elutasítja).

**Az oldal.** Fent „A te teendőid” (a `Te:` kezdetű következő lépés, a `dontesre_var` állapot, és a megkezdett munka ⛔ pontja; a még el nem indult feladat későbbi ⛔ pontja és a „Halasztva” tétel nem teendő). Utána sávonként három blokk: folyamatban (`fut`, `megallt`, `dontesre_var`, a main-en még nem lezárt), vár (`nem_indult`, `brief_kell`, a függésekkel), kész a héten (az elmúlt 7 napban lezárult, és az egyesített PR-ok). A végén az összeállítás ideje és a bemenet forrássora. Az állapotok magyar címkéi egy táblában (`ALLAPOT_CIMKE`) vannak.

**A `sav` mező.** A bevezetése másik session feladata (`feladatok.py` KULCSOK, brief-sablon, fejlécek); ez a brief azokhoz nem nyúl. Amíg a kulcs nincs a listában, az elemző `ismeretlen kulcs: sav` hibát jelez; a szkript ilyenkor a fejlécsort közvetlenül olvassa ki, ezért a bevezetés előtt és után is működik. Sáv nélküli brief a „besorolatlan” csoportba kerül.

**Teszt.** `eszkozok/tesztek/test_heti_attekinto.py` (a csoportosítás, a hiányzó `sav`, a teendők, a hét napos ablak, a PR-hozzárendelés, az oldal szerkezete); a CI-ben a `teszt_feladatok.py` láncán fut.

**A `nem_fugg` indoka.** A #123, #188 és #201 a `feladatok.py`-t írja; ez a brief csak importálja és olvassa (a `feladatok.py` változatlan marad), ezért nem függ tőlük. A `teszt_feladatok.py`-ban egyetlen import-sor kerül hozzá (a #123 és a #188 is írja): a sorok külön helyen állnak, a konfliktus rebase-nél triviális.

**Nem része.** Az oldal közzététele (az orkesztrátor teszi), a `feladatok.py`, a brief-sablon és a fejlécek módosítása, a CI-lépés felvétele a `.github/workflows/` alá.
