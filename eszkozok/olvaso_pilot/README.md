# Olvasói pilot (nem éles)

Az olvasói nézet első, belső próbája (2026-10-05): a teremtéstörténet (1Mózes 1:1–2:3) folyamatos Károli-szövege, kattintható szavakkal, jobb oldalon a héber és görög szó-lapokkal és a versrészletekkel. A továbbfejlesztés és az értékelés a **#60 OLVASOI_PILOT** feladat (`F60_OLVASOI_PILOT_BRIEF.md`).

## Futtatás

```bash
python eszkozok/olvaso_pilot/adat.py --szakasz "1Móz 1:1-2:3"
python eszkozok/olvaso_pilot/epit.py --szakasz "1Móz 1:1-2:3"
python eszkozok/olvaso_pilot/adat.py --szakasz "Zsolt 22"
python eszkozok/olvaso_pilot/epit.py --szakasz "Zsolt 22"
python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py
```

A `--szakasz` vers-tartomány (`"1Móz 1:1-2:3"`) vagy egész fejezet (`"Zsolt 22"`); a versek a `Karoli_1908.tsv`-ből jönnek, a könyvfájlok a `szakasz.py` `KONYVFAJLOK` táblájából (ma: 1Móz, Zsolt; más könyvre a pilot hibával áll meg). Mindkét program a `--kimenet KÖNYVTÁR` könyvtárba ír, alapból a repón kívüli `<temp>/olvaso_pilot/<szakasz-azonosító>/` könyvtárba. A kimenet (`olvaso_pilot.json`, `karoli_konkordancia_proba.html`) nem kerül a repóba. A `ts=` mező a futás UTC ideje.

| Fájl | Szerep |
|---|---|
| `szakasz.py` | a `--szakasz` feloldása (versek, könyvfájlok, szakaszcím) |
| `teszt_olvaso_pilot.py` | tesztek: szakasz, fő szó, görög szóalak, BDB-bontás, proveniencia, „csak adat” ellenőrzés |
| `adat.py` | adatkinyerés a repó tábláiból (csak olvas), JSON-kimenet |
| `bdb_szelet.py` | a BDB-szócikk gépi bontása apparátusokra (címszó, alapjelentés, nyelvi háttér, alakok, törzsek, jelentésszerkezet, jelek) |
| `epit.py` | a JSON beágyazása a sablonba |
| `sablon.html` | az oldal (HTML, CSS, JS); a tartalmat a beágyazott JSON-ból rajzolja |

## Alapszabály: csak adat, és a jellege jelölve

A lapon minden tartalom a repó egy táblájából jön; magyarázó szöveg nincs rajta (felhasználói döntés, 2026-10-05). Minden blokk címe mellett a jellege áll:

| Jelleg | Jelentése | Példa |
|---|---|---|
| **forrásadat** | változtatás nélkül egy adatkészletből | Károli-szöveg, TAHOT, LXX_OS, TSK, BDB angolul, UBS DBH, lxx_bridge |
| **gépi feldolgozás** | determinisztikus szabály rendezi vagy párosítja a forrásadatot | BDB-bontás, a fő héber szó választása, a görög szóalak párosítása, rövid jelentés kivágása |
| **modell-kimenet** | nyelvi modell állította elő; javaslat-értékű | Károli–Strong párosítás (#22), BDB magyarul (#38), Thayer/UBS magyarul (#28) |

A „?” jel a blokk adatkészletét, fájlját és licencét mutatja (`adat/licencek.tsv`). A teszt ellenőrzi, hogy a sablon minden blokk-címe kap jelleg-címkét és adatforrást, és hogy a lapon nincs feladatszám.

## A gépi szabályok röviden

- **Fő héber szó**, ha egy Károli-szó több héber szót ad vissza: előbb a `magas` bizonyosságú pár, azon belül a tartalmas szófajú (a `Strong_szotar.tsv` szófaja szerint nem elöljárószó, kötőszó, partikula, névmás, indulatszó). A többi pár a szó-lapon látható.
- **Görög szóalak**: a héber–görög párosítás a Maculából jön, a szóalak az `LXX_OS`-ből (azonos Strong-szám, és a szóalak ékezet nélkül azonos vagy legfeljebb 1 betűben tér el). Ok: a Macula `gorog_lxx` oszlopában a χ és a ξ fel van cserélve (`NYITOTT_FELADATOK.md`).
- **BDB-bontás**: a szócikk saját jelölői (gondolatjel, sorrendhelyes „1, 2 …” és „a, b …”, törzsnevek). Hibás határ előfordulhat; a szöveg nem változik.
- **Igealak**: a Macula nyers kódja és szófaja, feloldás nélkül (jelkulcs: #58).

## Ismert korlátok (2026-10-05)

- A 98 héber szóból 54-nek van magyar BDB-szócikke (a #38 gyakorisági sorrendben halad).
- A H4725 (*mákóm*) és további 395 Strong-szám BDB-szócikke hiányzik a táblából (#57).
- A Károli–Strong párosítás csak 1–5Móz és Józsué könyvére kész; az Újszövetségre nincs.
- A görög szó-lapokon magyar jelentés csak a #28 lexikon-szócikkeiből van (110-ből 3).
