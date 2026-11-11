# F196 — Gyökérok-kapuk: jelentés

*FELADATOK #196 · ág: `claude/gyokerok-kapuk-a1d120` · modell: claude-opus-5-5 · 2026-11-11 · a mérés alapja: a main `7095bc63` (a HAMART-001 lap a PR #686 merge-e utáni állapotban).*

## 1. Mi készült

| Fájl | Mit csinál |
|---|---|
| `eszkozok/ellenorzes/allitas_adat.py` | állítás–adat kapu: a lap és a melléklet számai és „nincs …” mondatai a saját adatukhoz mérve; JELENTÉS (`--szigoru`: 1-es kilépési kód eltérésnél) |
| `eszkozok/ellenorzes/kovetelmeny_kapu.py` | követelménylista-kapu: a `KESZ_LAP_KOVETELMENY.md` K-sorainak gépi szabályai egy lapra, „N/M követelmény teljesül (gépi)”; JELENTÉS |
| `eszkozok/teszt_gyokerok_kapuk.py` | 27 teszt (áladat + a valódi HAMART-001 egy rontott másolaton) |
| `.github/workflows/ellenorzes.yml` | új, nem bukó lépés (a két kapu a Step Summary-ba), a tesztfájl a „Szabaly-tesztek” lépésben |

Az állítás–adat kapu katalógusa 46 mintát mér (előfordulás, Kivonat, Döntési út, kizárt helyek, LXX régi és új alak, kapcsolatok típusonként, kapcsolódó motívumok, 4.13, 4.14, 12 „nincs” mondat, melléklet összegei, okonkénti címsorai és felsorolt versei tagonként). Az adat a generátor saját függvényeiből jön; hat helyen a kapu a blokkfüggvény számolását ismétli (`SAJAT_SZAMOLAS`, N-F196a). Futásidő: 9 lap 23 mp.

A követelménylista-kapu 109 K-sorból 55-öt mér gépi szabállyal (ebből 5-öt csak részben: a cella lektori, „grep” vagy „nincs” része nem gépi); 47 sort ember ellenőriz (lektor, szerkesztő, „gépi: nincs”, „gépi: tervezett”), 7 sor gépi, de nem gyűjthető (az F24, F27 (b) kapuja, a lap 1.2 táblája, `megfelelo_kinyer.py`, `muhely_allapot.py`, „gépi + szerkesztő”, és az E28, amely a generátort futtatja: csak `--e28`-cal fut, a HAMART-on 15 perc alatt sem végzett, ezért leállítottam). Futásidő: 1–3 perc lapanként (az `ellenoriz.py` szabályai).

## 2. Próba: HAMART-001

**Állítás–adat kapu: 163 állítás, 163 egyezik, 0 eltér.** A lap mai állapotában minden mért szám és hiánymondat egyezik az adattal (47 hely, 54 vers, 1 796 megvizsgált vers, 56 kapcsolat 42 csomóponttal, LXX 46/6/28/12, az 5. tábla összesítője 6/28/0/11/1, 4.13: 23 szócsalád, 4.14: 1 rejtett, 2 312 hamis párhuzam; a melléklet 29 okcímsora és felsorolt versei tagonként). A gyökérok-példa („nincs rögzített kapcsolat” 56 sor mellett) a lapon már nem áll; a rontott másolaton a kapu jelzi (teszt).

**Követelménylista-kapu: HAMART-001: 44/55 követelmény teljesül (gépi) — a 11 nem teljesülőből 1 gátló szintű, 10 csak figyelmeztetés.**

| K | Szint | Mit talál | A lista szerint |
|---|---|---|---|
| K01 | gátló | `ellenoriz.py` 11. SÉRTÉS: `HAMART-001 / alatamasztas` — a `res_forras.tsv` sora még a rögzített „A motívumhoz nincs rögzített kapcsolat.” mondatot tartja, a generátor viszont (F182) a kapcsolat-táblából renderel; a tábla és a lap nem egyezik. A gyökérok-példa maradványa az adatrétegben. | teljesül |
| K07 | figyelmeztetés | `ellenoriz.py` 22.: 63 kiejtés nélküli héber/görög szó a lapon | teljesül |
| K11, K60 | figyelmeztetés | ANGOL_SOR: 7 | teljesül |
| K19 | figyelmeztetés | HIANYJEL: 1 | részben |
| K20, K26 | figyelmeztetés | KIVONAT_SZAM: 2 | teljesül |
| K58 | figyelmeztetés | `ellenoriz.py` 43.: 8 szótári hivatkozás nem létező Károli-versre | teljesül |
| K93, K94 | figyelmeztetés | `ellenoriz.py` 39.: a határ modelles része n=48 sorra készült, ma n=47 | teljesül |
| K97 | figyelmeztetés | `ellenoriz.py` 23.: próza-lefedettség (el 6, kap 14) | nem eldönthető |

A lista „HAMART-állapot” oszlopa 9 sorban „teljesül”-t mond, a gép nem. Két ok: (1) a lista a #182 egy korábbi commitján mért (`9e74455e`); (2) a lista a FIGYELMEZTETÉS-szintű találatot nem számolja nem teljesülésnek, a kapu igen, de a szintet külön jelöli. A K01 nem szint kérdése: a 11. szabály SÉRTÉS-e a mai main-en áll fenn.

## 3. Próba: ISTENTISZT-001

**Állítás–adat kapu: 43 állítás, 43 egyezik, 0 eltér.** A régi szerkezetű lap mondatait a kapu a régi mintákkal méri (LXX helyben, 4.13 szótári alakokkal, 4.14 régi alak); a Döntési út és a melléklet ezen a lapon még nincs, ezért azokat nem méri.

**Követelménylista-kapu: ISTENTISZT-001: 41/55 követelmény teljesül (gépi) — a 14 nem teljesülőből 0 gátló szintű, 14 csak figyelmeztetés.** A találatok: az `ellenoriz.py` 40. szabálya (a HAMART regressziós kapui: K02, K03, K33, K34, K68), MUNKASZO 24 (K04, K57), PONT 2 (K04, K45), ATIRAS_VALT 3 és 22. szabály (K07), HIANYJEL 11 (K19), 42. szabály (K52, K59), 27. szabály (K56), 23. szabály (K97). Ezek a régi lapszerkezet ismert hiányai: az ISTENTISZT új cikkének menete (F194) kezeli őket.

## 4. A többi lap (állítás–adat kapu, `--minden`)

| Lap | Állítás | Eltér | Mi |
|---|---|---|---|
| ALVIL-001, ANTROP-001, TEREMT-002 | 38, 27, 29 | 0 | — |
| HODIT-001 | 8 | 4 | a 3. blokk jelöltsor-száma 17 ↔ 18; az 5. LXX-összesítő: eltérő 0 ↔ 18, függőben 28 ↔ 15, számozás 5 ↔ 0 |
| KIRALY-001 | 9 | 3 | jelöltsor 0 ↔ 14; LXX eltérő 0 ↔ 4, függőben 6 ↔ 2 |
| MENNY-001 | 8 | 4 | jelöltsor 2 ↔ 3; LXX eltérő 0 ↔ 4, függőben 5 ↔ 2, számozás 1 ↔ 0 |
| TEREMT-001 | 8 | 5 | jelöltsor 0 ↔ 2; LXX egyező 27 ↔ 30, eltérő 0 ↔ 4, függőben 5 ↔ 1, számozás 2 ↔ 0 |

A négy régi lap a mai adatnál régebbi generálás: a lapon álló szám igaz volt a generáláskor, ma nem az. Ezt az eddigi kapuk nem látták (N-F196b). Javítás: újragenerálás a generátor-körben, kézi folt nincs.

## 5. Ami nyitva marad

- **DT-F196a:** a HIBA-szintre emelés a HAMART-001 kiadása után (E-szám, SEMA 3.11, `--szigoru`).
- **N-F196a:** a hat `SAJAT_SZAMOLAS` hely kiemelése a generátorba közös függvénnyé.
- **N-F196b:** a négy régi lap újragenerálása.
- **N-F196c:** további állítás-típusok (6. Kereszthivatkozások, 1.2 keresési számai, 4.6 szavankénti LXX, szabad próza).
- **N-F196d:** a követelménylista K19/K77 „Ellenőrzés” cellája nevezze meg az állítás–adat kaput (a kapu a hivatkozást már felismeri).
- A K01 (a `res_forras.tsv` HAMART `alatamasztas` sora) adatjavítás; ez a menet az `adat/`-hoz nem nyúlt. A HAMART #183 menetére tartozik, vagy külön tételre.

## 6. Független ellenőrzés és javítókör

`naplok/ELLENOR_F196.md`: 4 ELTÉRÉS (a lapra nem futó E19/E34 mérés nélküli teljesülése; az LXX-összesítő új címkéi; a K03 „olvasói kapu” és a vegyes cellák; csupa nem mérhető állítás). Mind javítva az F196.5-ben, teszttel; a fenti számok a javítás utániak. A helyi E2–E37 futás zöld volt (kilépési kód 0), az E32 JELENTÉS-ét (helyőrző string-literálban) is javítottam.
