# F22_Zsolt_elofutas.md — Zsoltárok: a 12 kötegű előfutás (DT-F22g, 1. opció)

*Számok szkriptkimenetből (`f22_statisztika.py`, `sonnet_koteg.py allapot`, `get_usage`). Csak Sonnet (DT-F22c), `prompt_v3` változatlanul (a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte a hash-t, hiba nélkül). Jóváhagyás: felhasználó, 2026-10-07, chat (DT-F22f igen mindkét részre, DT-F22g 1. opció).*

## 1. Minta

12 köteg (120 vers), rögzített lista (`f22/_munka/zsolt_elofutas_valaszt.py`, nem verziózott): 2 (Zsolt 2:5–3:2, felirat 3:1), 5, 79 (51:1–10, felirat), 91 (59:11–60:2, felirat 60:1), 174 (105:1–10, jelzett fejezet), 193 (111:3–112:2, akrosztichon, 112 jelzett), 195 (113:3–114:3, jelzett), 200 (116:18–118:6, rövid 117), 212 (119:88–97, akrosztichon), 221 (120:2–121:4, 121 jelzett), 230 (132:15–134:3, rövid 134), 245 (144:9–145:3, akrosztichon 145).

## 2. Szkriptkimenet

```
Sonnet: 12 köteg, 120 vers; kapuhiba első próbára 0.0% (0/120); végleg 0.0% (0/120)
köteg összesen: 253, kész: 12, hátralevő: 241
```

Rendszerszintű hiba (kapu, hash, sorszám-lefedettség) nem jelent meg. A jelzett fejezetekből a mintában a 105, 114, 121 szerepel (a 6 nem; a rögzített lista 12 különböző kötegre esett).

## 3. Keret

Heti „all models”: 61% az előfutás előtt, 61% utána (a kerekítés alatti fogyás); 5 órás ablak 32% → 35%. A teljes futás becslése (253 köteg) a mérés alapján: az előfutás 12 kötegére ≤ 1 pp / 120 vers, így nem haladja meg a korábbi 9–15 pp becslést.

## 4. Megjegyzések

- A subagentek `f22\_munka`/`f22_munka` útvonal-összekeveréssel egy ideiglenes `f22_munka/` könyvtárat hoztak létre; a válaszfájlokat áthelyeztem az `f22/_munka/` alá, a mappát töröltem; a mentés mind a 12 kötegre az `f22/_munka/…_v1.json` fájlból futott.
- A subagentek gépi ellenőrzést nem futtattak, a kaput a `mentes` futtatta.
- Vitás döntések a subagentek jelentéséből (kézi átnézésre): 119:94 „vagyok” betoldás/„ani” fordítatlan; 144:15 „a melynek”; 145:1 „dicsérő éneke”.
- **Teendő (felhasználó, helyben):** `eszkozok/karoli_strong/zart_osszevet.py` futtatása a zárt forrásból kimásolt, **a 12 köteg 120 versére** (repón kívüli fájl, parancssori útvonal), az összesítő szám (egyezés %, n) bemásolása ide; csak ezután indulhat a teljes futás (241 köteg).
