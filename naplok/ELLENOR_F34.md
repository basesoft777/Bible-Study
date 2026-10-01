# ELLENOR_F34 — F34_BDB_PSI_BRIEF.md · `origin/main...HEAD`

Forrás: a `fuggetlen-ellenor` jelentése (szerep-korlát miatt fájlba nem írhatott; az orkesztrátor mentette,
tömörítve). A saját futtatás eredménye az orkesztrátoré: `ellenoriz.py` rc=1 (13. szabály SÉRTÉS (2)),
`teszt_forditas_kapuk.py` 20 teszt OK, `teszt_bdb_psi_javit.py` 6 teszt OK.

ELTÉRÉS: 7 tétel (súlyossági sorrendben)

1. **13. szabály (`forras_hash`) SÉRTÉS a `forditasok.tsv` 81. (H7585) és 84. (H7843) során.** A forrásuk
   a DT-F34b javításától tovább változott, a sorokat a döntés szerint nem írtuk át → elavult hash →
   `ellenoriz.py` kilépési kód 1 → az E1 miatt a CI piros. A brief 4. lépése és az `ad` mező („a 13. kapu
   jelzése megszűnik”) nem teljesül. Feloldás új döntést kér: (a) jóváhagyott token- és hash-frissítés a
   81. és 84. sorban (DT-F34 „kezi: csak token” mintájára; módosítja a DT-F34b „81/84/85 változatlan” kitételét),
   (b) újrafordítás; (c) kódlazítás nem ajánlott.
2. **DT-F34 és DT-F34b ✅ csak az alkalmazás után került a repóba** (F34.5), a B/R-javítás (59 hely) a DT-F34
   saját javaslatával ellentétes volt; a felhasználói döntés a chatben született, a repóban utólag rögzített.
3. **A DT-F34b premisszája (TAHOT-hiány Zsolt 88/89/140/142) hamis:** a lekérdezés szerint a fejezetek benne
   vannak; a napló 26. és 42. sora felülírt állítást tartalmaz „elavult” jelölés nélkül. Az A-maradék javítását
   nem érinti (mind a 15 fejezet > 66).
4. **A maradék-tábla H8034 `Dan 22:19` → `Psa 22:19` javaslata téves** (5Móz 22:19; Dt→Dan hiba, nem ψ).
   A többi `Dan` B-tétel (H8478, H3117, H6881, H9004) valószínűleg ugyanilyen; az N-F34 kézi nézetét félrevezeti.
5. A „150/150 fejezet, 2527/2527 vers, Jób 41” mérési állítás mellett nincs proveniencia-sor (`scope=… | forras=… | ts=…`).
6. A brief `ir` listája nincs frissítve (`bdb_psi_javit.py`, `teszt_bdb_psi_javit.py`, README).
7. Tesztminőség: `VEDETT_SOROK = {81, 84, 85}` fájlsorszámhoz kötött (nem kulcshoz); az egyik teszt tautológia.

OK: a BDB-diffben 318 változott szó = 159 `-<könyv>` + 159 `+Psa`; sorszám (8091), sorvégek, mezőszám változatlan;
a 159 JAVIT sor = a csere-tábla; A-/B/R-szabály mintavétellel igazolva (H8415, H0430, H0040, H2778, H6403, H9009);
`forditasok.tsv` 78./89.: csak token + hash, a 81. csak token + hash, 84./85. szövege változatlan; csv modul 0;
E2–E16 és E19: 0 találat; Dán 22:14 és `lexikon/` érintetlen.
NEM ELLENŐRIZHETŐ (az ellenőr szerep-korlátja): a tesztek futtatása (az orkesztrátor pótolta, l. fent), a CI,
a main-nel való ütközés (`DONTESEK.md`, `NYITOTT_FELADATOK.md` a main-en változott), az SHA-256.
