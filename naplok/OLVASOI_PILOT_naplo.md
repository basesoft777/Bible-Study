# OLVASOI_PILOT (#60) — munkanapló és állapotjelentés

*2026-10-07 · ág: `claude/olvasoi-pilot` · utolsó commit: `F60.23` (`4c06b91`) · a #60 állapota: `megallt` (felfüggesztve a felhasználó kérésére, F60.16)*

## 1. Állapot egy mondatban

Az olvasói pilot (1Móz 1:1–2:3 és Zsolt 22) a repó minden használható adatával bővítve, jelölve (forrásadat / gépi feldolgozás / modell-kimenet), minden blokk alatt látható forrássorral; az M3 (felhasználói átnézés) tart, az M4 (értékelő jelentés, zárás, független ellenőr, draft PR) **nem indult el**. A BDB-szeletelő javítása közben a munka **megszakadt**: a H7121 törzs-hibák javítása a munkafában van, nem commitolva (l. 4.).

## 2. Kronológia (commitok)

| Tétel | Mi |
|---|---|
| F60.0–F60.3 | M0–M2: `--szakasz` paraméter, jellegjelölés és ellenőrzőlista, 22 teszt, mérés; megállás az M3-nál |
| F60.4 | fülváltás-hiba (a `section.lap{display:grid}` felülírta a `hidden`-t) |
| F60.5–F60.9 | v2 bővítés: SDBH/SDGNT, SECE, OSHL, TBESH, tW, LSJ, MCGED, UBS DNTG, BSB/KJV angol szavak, Nave, TIPNR, igealak-feloldás, adatréteg-sorok; adatfelmérés (81 sor, 201 fájl); DT-F60a/b |
| F60.10–F60.12 | tipográfia; tanulmányozó rész, látható forrássor; szélesebb panel (5:7), világos színséma és váltó |
| F60.13–F60.15 | minden blokk nyitva (a „Forrás” és „?” kivételével); LXX-kiemelés és átkattintható LXX; minden híd-beli görög szónak lap (110→202, 153→304) |
| F60.16 | a #60 felfüggesztve (`allapot: megallt`, folytatási pont a brief `kovetkezo` mezőjében) |
| F60.17–F60.18 | BDB-szeletelő: zárójeles előszócikk, homonima-szakaszok (I./IV., arámi Pe`al); TBESH-sorrend a Strong-lemma és jelentés szerint |
| F60.19–F60.21 | alapjelentés a szó-lap fejlécében; a tisztítás a szeletelőbe (`alap_jelentes`) |
| F60.22 | a pilot újragenerálva |
| F60.23 | BDB-fejléc: átírás-változatok után az első héber szó a címszó (588 sor javul), szófajos szakasz = alapjelentés, zárójelben álló szám nem jelentés-sorszám (H4100) |

Nem a repóba kerül (a CLAUDE.md szerint a kimenet a repón kívülre megy): a két HTML (`<temp>\olvaso_pilot\…`) és a Zsolt 22:3 mockup (`<temp>\olvaso_pilot\mockup\`).

## 3. Mérőszámok (a `naplok/OLVASOI_PILOT_meres.md` és `_adatfelmeres.md` részletezi)

- Károli-szó kötött tartalmas héber szóhoz: 60,3% (1Móz) / 59,7% (Zsolt 22); a Zsolt 22 párosítása mind „alacsony” bizonyosságú.
- Magyar BDB-szócikk: 61/98 és 112/159 héber lapon (a #38 gyakorisági sorrendben, 674 teljes szócikk kész a 8090-ből).
- Magyar alapjelentés a fejlécben (a tisztítás után): 58 és 106 lapon; a többi angol (nincs magyar BDB, vagy nem kinyerhető).
- Görög lapok: 202 és 304; ebből magyar jelentés 4 és 3.
- Teszt: 73 zöld (F60.23-kor), 1 kihagyva.

## 4. Megtalált hibák és javításuk

| Hiba | Állapot |
|---|---|
| Szó/Vers részletei fülváltás nem váltott | javítva (F60.4), teszt |
| Mockup: a szó-lap fülsora 1 px-re zsugorodott (a mérésem csak a gombok számát nézte, nem a láthatóságot) | javítva, **a mockup a repón kívül** |
| H6030: alapjelentés „lakni” (a zárójeles [עוּן] előszócikk) | javítva (F60.17–18); a sor 4 szakaszra bomlik |
| H6030: a Dán-helyek a Hiph'il alá kerültek (arámi Pe`al rész) | javítva (F60.18) |
| TBESH: H6030a „dwell” állt elöl | javítva (F60.18), 12 lapon változott az első sor, mind a Strong-jelentéssel egyezik |
| 588 BDB-sorban nem héber szó a címszó („or”, „vagy”) | javítva (F60.23) |
| H4100: a zárójelben álló „2” jelentés-sorszámnak számított | javítva (F60.23) |
| **H7121: a Qal-alakok személyszámai („1. egyes szám”, „3. nőnemű”) jelentés-sorszámnak számítanak; a Niph`al és Pu`al törzs a Qal 7.9 pontjába olvad (szám nélküli törzsfejléc); a zárójeles törzsfejléc (`Pu`al (Ezékiel…) perfectum`) sem ismert** | **folyamatban, nem commitolva** (l. 5.) |
| TBESH: a „H7121H/I/J = a Meaning of” sorok „másik homonimaként” jelöltek, a jelentés-listájuk azonos és ismétlődik | **nyitva** |

Közben az én hibáim: a mockupban az „üres” fül láthatósága nem volt mérve; a hiányzó magyar BDB okát és a DT-M1 állapotát (már eldöntve 2026-10-06, 1. opció) is csak a felhasználó kérdésére tisztáztam; az F60.18 előtti válaszomban a Dán-helyeket tévesen a BDB szerkezetének tulajdonítottam.

## 5. Folyamatban lévő munka (a munkafában, NEM commitolt)

Helye: `C:\Users\bases\Desktop\wt-olvasoi` (a `claude/olvasoi-pilot` ág `git worktree`-je), módosított fájl: `eszkozok/olvaso_pilot/bdb_szelet.py`. Tartalma:
1. `TORZS_FEJ`: szám nélküli törzsfejléc is törzs, ha alakcsoport-szó követi (opcionális zárójeles közbevetéssel).
2. `_jelentesek`: az „alakok; — 1 jelentés” szerkezetben a számozás a gondolatjel utáni „1”-nél indul (csak ha az előtte álló rész alakcsoportot tartalmaz — `FORMA_RE`), az alak-lista előtag marad.
3. Törzsfelismerés: a „Name_N / Name <alakcsoport>” és a tartalék (gondolatjel/mondatvég utáni törzsnév) felismerés egyesítve.

Mért (az egész BDB-táblán, régi vs. új szeletelő): 8099 sor, hiba 0; **elvesztett törzsnév 0**; 237 szócikk több törzset kap, 131 szócikknél egy névtelen elem helyett egy névvel jelölt törzs áll; a jelentés-szerkezet 6 sornál változik azonos törzsek mellett — **ezt a 6 sort még nem néztem át**. H7121: Qal 6 jelentéspont (1–6, alpontokkal) + alak-előtag, Niph`al 2 + előtag, Pu`al.
**Nem történt meg:** a teszt futtatása, új tesztek, a pilot újragenerálása, commit.

## 6. Döntésre és teendőre váró

- **DT-F60a** (licenc közzététel előtt: TBESH, MCGED, KJV+Strong, LXX-páros, share-alike források) és **DT-F60b** (feliratos zsoltárok számozása; a Károli–KJV azonosság hibás a Zsolt 22-re) — `DONTESEK.md`, helyőrzővel.
- **M3 határesetek:** a „Gépi szeletelés (próba)” szöveg a lapon; „TAHOT nem teljes” lábjegyzet; a „Macula-illesztés kb. 78%” átvett szám.
- **A brief frissítése:** a DT-M1 már eldőlt (2026-10-06: igen, a #25 kettéválik #25a/#25b); a brief v1 még a három opciót írja. Az M4 értékelő jelentés ennek megfelelően a #25a feltételeit (DT-M4, DT-M6, hosting) értékelje.
- **Felületi irány:** a mockup (réteges szó-lap, igazítási sáv, Ctrl+K, mobil lap) kipróbálva; a #25a briefjébe vihető. Nyitott kérdés: minden Károli-szó legyen kattintható (a szavak ~40%-a ma nem az: nyelvtani elemhez kötött vagy nincs héber párosítás).
- **Kisebb:** az „Alakok” blokk H4100-nál az első alak nélkül kezdődik; a gépi alapjelentés-tisztítás eredményéhez nincs automata (böngészőn kívüli) teszt a valós adatra.

## 7. Munkamenet-kockázatok

- A főmappa (`C:\Users\bases\Desktop\Bible-Study`) ágát **más munkamenet váltogatja** (láttam `claude/hivatkozas-ellenorzes`-t). Ezért a pilotot külön `git worktree`-ben szerkesztem; egyszer véletlenül a főmappa más ágán módosítottam három fájlt, ezeket visszaállítottam (nem commitolva).
- A `wt-olvasoi` munkafa **nyitva maradt** a nem commitolt szeletelő-módosítással; folytatás előtt ezt kell dönteni (befejezés, vagy `git worktree remove` a módosítás elvetésével).
- A heredoc-os Python-szkriptek a `\\n` / `\\b` escape-eket elrontják (egyszer vezérlő karakter került a regexbe, F60.17); a javítások fájlból futtatva (Write → futtatás) biztonságosak.

## 8. Következő lépések (javasolt sorrend)

1. A H7121-javítás befejezése: a 6 jelentés-szerkezet-változás átnézése, tesztek (H7121-minta, zárójeles törzsfejléc, szám nélküli törzs), a pilot újragenerálása, commit `F60.24`.
2. A TBESH-sorok címkéje („jelentés-ág” a „másik homonima” helyett) és az azonos jelentés-lista egyszeri megjelenítése.
3. Az M3 lezárása: a határesetek és a DT-F60a/b eldöntése.
4. A brief frissítése (DT-M1 alkalmazása), majd az M4: `naplok/OLVASOI_PILOT_ertekeles.md`, `…_zaras.md`, `fuggetlen-ellenor`, draft PR.
