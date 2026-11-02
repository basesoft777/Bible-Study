# ELLENOR_F159 — független ellenőrzés (`fuggetlen-ellenor`, tartomány `0c597b1e..3ff5ba6b`)

*Az ellenőr nem tudott fájlt írni, ezért a jelentését a futtató session rögzíti. Az ellenőr eredménye: ELTÉRÉS, 7 tétel; a javítás után a státusz az alábbi.*

| # | Eltérés | Státusz |
|---|---|---|
| 1 | a `bekuld` és a `bbekuld` nincs összehangolva (kettős költség vagy kimaradó nagy Strong) | **javítva**: a `bekuld` kihagyja a már beküldött vagy megválaszolt kéréseket, a csomagfájl sorszáma folytatólagos; teszt: `test_bekuld_a_b_utan_nem_kuldi_ujra_a_b_strongokat` |
| 2 | a nagy Strongok javító körét a kivetítés alulbecsli | **javítva** a naplóban: 0,43-as javító/1. kör arány (F27 M1) → 87,8 (high) / 72,3 (medium) USD |
| 3 | hibás a becslő túlbecslésének magyarázata | **javítva** a naplóban: a túlbecslés a kimenetből jön, a bemenet pontos |
| 4 | a 10 pontos és a 130 USD-s küszöb forrás nélkül | **javítva** a naplóban: az orkesztrátor megbízása és üzenete a forrás |
| 5 | a `begyujtve_*.txt` felülíródik 0-ra | **javítva**: nem íródik felül; a két B-batch jelölője 64-re állítva; teszt: `test_begyujtve_jelolo_nem_irodik_felul` |
| 6 | a `mero_strongok.txt` kívül esik az `ir` mezőn | **javítva**: a brief `ir` mezője bővítve |
| 7 | pontatlanságok a napló 16. és 51. során | **javítva** |

Nem ellenőrizhető (az ellenőr korlátai): a teszt futtatása (a futtató session: 29 teszt zöld), a `bszaraz` számai, a kapunkénti első körös bontás (a futtató session újraszámolta a `strong_allapot`-tal az 1. próbás rekordokból, l. a napló 4. pontját), a beállított max_tokens.

Megjegyzés az ellenőrtől: a szűkítés `kapu=nem` sorokat is megtart (a napló jelzi); a `test_szukites_pontos_sorhalmaz` „mást nem” része azonos predikátummal ellenőriz. Elfogadott: a szabály a briefnél tágabb, szándékosan (a `kapu=nem` sorok a fordító számára is szabályok, pl. `grave` = sír).
