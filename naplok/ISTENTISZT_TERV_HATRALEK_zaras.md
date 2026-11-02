# ISTENTISZT_TERV_HATRALEK — zárójelentés (#152, F152)

*2026.11.02 · modell: claude-opus-5-5 · ág: claude/f152-lezaras · ⛔ a brief `lezarva` állapota és a `motivumok.tsv` két kérdésre vár (5.)*

## 1. Mi készült el

- **PR #549 (F152.0–F152.8), mergelve:** az A-pont két hibás indoklása javítva lett. A negatív kritérium bekerült a Kivonatba. A generátorban összevonódtak a közös forrásmegjelölések (181 → 6) és a tartományok. A „gerinc” szó az olvasói helyekről kikerült (18 → 0). Kiejtés került a kézi prózába. A Minősítés jelölt-táblája csukva áll (DT449).
- **PR #559 (F152.9–F152.20), mergelve:** megtörtént a K1–K5 (DT476), a DT478 („Csak ahol JHVH áll”) és a DT479 átvezetése. Az ISTENTISZT-001 33 helyéből 22 maradt (16 ÓSZ, 6 ÚSZ), a kapcsolatokból 25 → 18. A `negativ_kriterium` bővült. A próza egészében átolvasva frissült, a Kivonat 2. és 3. mondata a felhasználó jóváhagyott szövegével áll.
- **PR #563 (F152.21–22), mergelve:** az Ézs 41:25 elutasítva (DT478). Az N-F146b lezárva, mert a fordítás megvan.
- **Ez az ág (F152.23):** bekerült a DT-F152d (a lap lezárható, 1. kiadás; a felhasználó: „ettől független lezárható / a lektori átnézés eredménye egy új kiadás”). Az N-F152a–g tételek mellé került, hova tartoznak, és ez a jelentés.

## 2. A kolofon kiadás-sora (DT-F152d 3. pont)

A kiadásszám és a változásjegyzék a generátorban ma nem renderelődik, és adatforrása sincs kijelölve (N-F125a). Az 1. kiadás sora ezért nem került sem adatba, sem forrásba. A lexikonlapot kézzel nem szerkesztettem. Ha az N-F125a elkészül, az 1. kiadás sora (2026.11.02, „az arany lap első kiadása: a #152 és a #151 K1–K5 átvezetése”) a kijelölt adatforrásba írható.

## 3. A próza-lefedettség a lezárás előtt (MUNKAMENET C-z)

`python eszkozok/proza_lefedettseg.py ISTENTISZT-001` (2026-11-02, a main a5eb0827-en; scope=motivumok/ISTENTISZT-001.md + adat/elofordulasok.tsv, kapcsolatok.tsv, motivum_kapcsolatok.tsv, jeloltek.tsv | forras=eszkozok/proza_lefedettseg.py | ts=2026-11-02 | csatorna=cli):

| rovat | adat | megnevezve | nem |
|---|---|---|---|
| előfordulás | 22 | 22 | 0 |
| kapcsolat | 18 | 17 | 1: 1Móz 4:26 → Sof 3:9 (Párhuzam) |
| motívumközi kapcsolat | 3 | 3 | 0 |
| nyitott jelölt | 3 | 3 | 0 |

Egyenetlenség-jel: Kivonat (68 karakter/elem, „kevés”) és 7. Módszertan (1520 karakter/elem). A Kivonat összefoglaló, a 7. szakasz módszertani próza; mindkettő jellegéből adódik. A meg nem nevezett kapcsolat két verse a prózában külön-külön áll (Kitekintés, Remez), a párt viszont semmi nem mondja ki. Ez a C-z szerint indoklást vagy prózát kíván (5. kérdés).

## 4. Az N-F152a–g sorsa

| tétel | sors |
|---|---|
| N-F152a | nyitva; rendszerszintű olvasó-tétel (#149) |
| N-F152b | nyitva; szerkezeti döntés minden lexikonra |
| **N-F152c** | **az ISTENTISZT-001 2. kiadására tartozik**, a lektori kérdésekkel együtt |
| N-F152d | nyitva, részben megvalósult (#125: mérő és C-z lépés; az `eszkozok/ellenorzes/` szabály hiányzik) |
| N-F152e | nyitva, részben megvalósult (#125: C-w lépés; a motívumonkénti értelmező feladat nincs rögzítve) |
| N-F152f | nyitva; generátor-tétel minden lexikonra |
| N-F152g | nyitva; kilenclépéses prózasablon nincs a `sablonok/`-ban (#125 köre) |

Csendben egyik sem zárult le: mindegyik sorhoz jegyzet került a `NYITOTT_FELADATOK.md`-ben.

## 5. ⛔ Nyitott a lezárás előtt

1. **MUNKAMENET C-w** (a #125 óta): ha a motívum adata érdemben változik, a lezárás előtt kötelező egy értelmező prózafeladat, és „az adatot író feladat nem zárhat le prózafeladat nélkül”. A K1–K5 adatváltozás ilyen. A prózát az F152.17 egészében átolvasta és átírta (értelmező modell, a teljes szöveg). Ezt viszont az adatot író feladat végezte, a C-z mérése pedig akkor még nem futott. Kérdés: elég-e az F152.17 a C-w-hez, és indokolható-e az egy meg nem nevezett kapcsolat (1Móz 4:26 → Sof 3:9)? Vagy előbb egy rövid prózafeladat kell (a pár kimondása)?
2. **`motivumok.tsv` állapota** (SEMA 2.1.1): ma `publikálható`, `v3`, `2026.09.22`. A `véglegesített` állapotot csak új lexikai bizonyíték nyithatja újra, szerkesztői szándék nem. A felhasználó viszont a lektori átnézésből új kiadást vár, ez szerkesztői szándék. Ezért a `véglegesített` nem illik. A végrehajtó javaslata: `publikálható` marad, a verzió `v4`, a dátum `2026.11.02`, mert a K1–K5 a motívum határát érdemben változtatta. A SEMA ezt nem írja elő egyértelműen.
