# F22_Zsolt_elofutas.md — Zsoltárok: a 12 kötegű előfutás (DT59, 1. opció)

*Számok szkriptkimenetből (`f22_statisztika.py`, `sonnet_koteg.py allapot`, `get_usage`). Csak Sonnet (DT-F22c), `prompt_v3` változatlanul (a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte a hash-t, hiba nélkül). Jóváhagyás: felhasználó, 2026-10-07, chat (DT58 igen mindkét részre, DT59 1. opció).*

## 1. Minta

12 köteg (120 vers), rögzített lista (`f22/_munka/zsolt_elofutas_valaszt.py`, nem verziózott): 2 (Zsolt 2:5–3:2, felirat 3:1), 5, 79 (51:1–10, felirat), 91 (59:11–60:2, felirat 60:1), 174 (105:1–10, jelzett fejezet), 193 (111:3–112:2, akrosztichon, 112 jelzett), 195 (113:3–114:3, jelzett), 200 (116:18–118:6, rövid 117), 212 (119:88–97, akrosztichon), 221 (120:2–121:4, 121 jelzett), 230 (132:15–134:3, rövid 134), 245 (144:9–145:3, akrosztichon 145).

## 2. Szkriptkimenet

```
Sonnet: 12 köteg, 120 vers; kapuhiba első próbára 0.0% (0/120); végleg 0.0% (0/120)
köteg összesen: 253, kész: 12, hátralevő: 241
```

Rendszerszintű hiba (kapu, hash, sorszám-lefedettség) nem jelent meg. A jelzett fejezetekből a mintában a 6 (a 5. köteg: 5:5–6:1), 105, 114, 121 szerepel.

## 3. Keret

Heti „all models”: 61% az előfutás előtt, 61% utána (a kerekítés alatti fogyás); 5 órás ablak 32% → 35%. A teljes futás becslése (253 köteg) a mérés alapján: az előfutás 12 kötegére ≤ 1 pp / 120 vers, így nem haladja meg a korábbi 9–15 pp becslést.

## 4. Megjegyzések

- A subagentek `f22\_munka`/`f22_munka` útvonal-összekeveréssel egy ideiglenes `f22_munka/` könyvtárat hoztak létre; a válaszfájlokat áthelyeztem az `f22/_munka/` alá, a mappát töröltem; a mentés mind a 12 kötegre az `f22/_munka/…_v1.json` fájlból futott.
- A subagentek gépi ellenőrzést nem futtattak, a kaput a `mentes` futtatta.
- Vitás döntések a subagentek jelentéséből (kézi átnézésre): 119:94 „vagyok” betoldás/„ani” fordítatlan; 144:15 „a melynek”; 145:1 „dicsérő éneke”.
- **Teendő (felhasználó, helyben):** `eszkozok/karoli_strong/zart_osszevet.py` futtatása a zárt forrásból kimásolt, **a 12 köteg 120 versére** (repón kívüli fájl, parancssori útvonal), az összesítő szám (egyezés %, n) bemásolása ide; csak ezután indulhat a teljes futás (241 köteg).

## 5. Szúrópróba eredménye (a felhasználó által továbbított; nem ellenőrzött)

*A felhasználó 2026-10-07-i chat-döntése: a szúrópróba a **Zsolt 51:1–10-re szűkül** (n = 10 vers, a 79. köteg), a DT59 lezárva. Az összesítőt a `zart_osszevet.py` helyi futásából egy másik session továbbította; a zárt szöveg nem a repóban van, a számokat ebben a session nem tudta újramérni. A `parok_Zsolt.tsv` még nem létezik, az összevetés ideiglenes (repón kívüli) táblán futott.*

- szószint, `alacsony` token (n = 55): a partner-Strongok tartalmazzák a zárt szó összes Strongját: 100,0% (55/55); azonos halmaz 96,4% (53/55); eltérő 0. `magas` token: n = 0 (csak Sonnet, DT-F22c).
- versszint: azonos halmazú vers 50,0% (5/10); elemszintű átfedés 85,7% (54/63); a saját táblának 9 többlet-Strongja van, a zárt forrásban nincs olyan Strong, amely nálunk hiányzik (a többlet jellege nem ellenőrzött).
- Értelmezés: rendszerszintű hiba nincs; n = 10 futás előtti ellenőrzésnek elég, pontossági becslésnek nem.

## 6. Döntés és következő lépés

DT59 lezárva; a teljes futás (241 köteg, csak Sonnet, DT-F22c) a felhasználó jóváhagyásával indul, a heti keret 85%-ánál a köteg végén megáll. A futás végén kézi átnézés: 119:94, 144:15, 145:1.
