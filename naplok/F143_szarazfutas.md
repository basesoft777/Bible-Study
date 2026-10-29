# F143 M0 — szárazfutás napló (KIRALY-001 lexikonoldalai)

*Modell: claude-sonnet-5-5 (kért: sonnet) · egyetlen író: a végrehajtó session.*

**Proveniencia.** `scope=general.py --cel lexikon / --cel torzscikk --id KIRALY-001 (és a 7 kontroll-ID), --kimenet a repón kívüli scratchpad-könyvtárba, --ir nélkül; adat/elofordulasok.tsv @ origin/main f3764787 | forras=helyi-futtatas (eszkozok/general.py; diff: GNU diff --strip-trailing-cr, difflib) | ts=2026-10-28`

A repó a futások alatt és után tiszta maradt (`git status --short` üres); éles lexikonfájlt nem írtam.

## 1. Mért diff (éles ↔ szárazfutás)

| Fájl | éles sorok | új sorok | törölt / hozzáadott sor | hunk (`diff`) |
|---|---|---|---|---|
| `KIRALY-001_TUDOMANYOS.md` | 632 | 1323 | −74 / +759 | 70 |
| `KIRALY-001_TORZSCIKK.md` | 427 | 459 | −31 / +63 | 20 |

A törzscikk a lexikonoldalból renderel; a próba-törzscikk a `--kimenet` alatti próba-lexikonoldalt olvassa (N-F78a), ezért a mért törzscikk-diff az **újragenerált** lexikonoldalra épül (közös `--kimenet` könyvtár). Külön könyvtárral az éles, elavult oldalra épülne, és a régi G0813-at hozná vissza; az első futás ilyen volt, eldobtam.

## 2. Osztályozás: (i) a G0813 → G0540 javításból eredő, (ii) egyéb drift

Módszer: ellenpélda-futás. Az `adat/elofordulasok.tsv` KIRALY-001 / Zsid 7:1-28 sorát átmenetileg a régi `G5010+G0813+G0282` mezőre állítottam, szárazfutás a scratchpadre (alap), majd `git checkout` visszaállította a fájlt (a repó tiszta). Így: **(ii) = éles → alap**, **(i) = alap → új**.

| | (i) javításból | (ii) egyéb drift |
|---|---|---|
| TUDOMANYOS | −16 / +10 sor, 10 hunk | −73 / +764 sor |
| TORZSCIKK | −5 / +5 sor, 3 hunk | −29 / +61 sor |

(Az összegek nem additívak az éles ↔ új számmal, mert a hunkok összeérnek.)

**(i) tartalma (TUDOMANYOS).** A Zsid 7:1-28 előfordulás-sor `strong` mezője és UBS-értéke (78. sor); a [^9] proveniencia-lábjegyzet; a „### Görög szavak: G0282, G0540, G5010” fejléc; a G0813 Thayer-szakasza (7 sor) helyett egy sor; a tW/domén/UBS/megfelelők/kiejtés G0540-es sorai. (TORZSCIKK): a cím „Fő szavak” sora, a Zsid 7:1-28 kulcsszó-/Strong-/UBS-sorai, a „Lefedettség szavanként” táblasor.

**(ii) tartalma.** Az éles oldal a mai generátorhoz és adatokhoz képest elavult (2026-10-20-i generálás): a „2. Szótári háttér” újrastrukturálva (szavanként 10 pontos szócikk-szerkezet), új TBESH/BDB-nyelvi-háttér blokkok, „Nyelvfüggetlen szerepek”, az „1/b” kizárt-jelöltek bővülése (+14 sor), a rés-blokkok generált szövege, `ts=`/licenc-fejlécek (pl. `projekt-adat` → `minden jog fenntartva`), megbízhatóság-jelölés (`tartalom-alapú` → `szó-szintű-gépi`), a 2Móz 19:6 fordítás („papok birodalma”), irodalom és kolofon bővülése. A fejlécek száma 43 → 70. A törzscikkben az igehely-szakaszok táblái és a szótári lefedettség-blokk változik. Ugyanezt rögzítette az F141 zárónaplója (`naplok/F141_zaras.md`): a 7 lap a generátorhoz képest elavult, tartalmi újragenerálásuk a #36 és a #143 dolga.

Az (ii) nem a generátor hibája: a kontroll (3. pont) igazolja.

## 3. Kontroll — a többi lexikonlap

A brief „7 másik lap nulladiffjét” nem definiálja részletesen; kontrollnak a `lexikon/` összes többi motívumát vettem (pontosan 7: ALVIL, ANTROP, HAMART, HODIT, ISTENTISZT, MENNY, TEREMT -001). Egyik sem hordoz G0813/G0540 sort (az ALVIL-001 egy „Zsid 7” szóegyezést tartalmaz, de G0813/G0540 nincs benne). Ugyanaz a szárazfutás, repón kívülre.

| Motívum | TUDOMANYOS (−/+) | TORZSCIKK (−/+) |
|---|---|---|
| ISTENTISZT-001 (E28: migrált) | −16 / +16; ebből `ts=` nélkül **2 sor** (csak a „Generálva” dátuma) | nincs kimenet (migrált, a törzscikk megszűnt, D6) |
| ALVIL-001 | −140 / +627 | −163 / +184 |
| ANTROP-001 | −59 / +903 | −22 / +44 |
| HAMART-001 | −160 / +2120 | −119 / +309 |
| HODIT-001 | −65 / +279 | −59 / +77 |
| MENNY-001 | −46 / +1287 | −24 / +42 |
| TEREMT-001 | −115 / +384 | −93 / +129 |

**Eredmény.** Nulladiff (a `ts=` és a „Generálva” dátumon kívül) csak az ISTENTISZT-001-re áll: ez az egyetlen, amelyet a CI (E28) figyel és a #11 migrált. A másik 6 lap ugyanúgy elavult, mint a KIRALY-001, tehát az (ii) drift **rendszerszintű** (a #36 hatóköre), nem KIRALY-specifikus. A generátor az ISTENTISZT-001-en determinisztikus.

## 4. G0540 és G0813 az új kimenetben

- `TUDOMANYOS`: a G0813 egyetlen előfordulása a [^9] proveniencia-lábjegyzet (88. sor), amely a javítást dokumentálja (`strong G0813→G0540: DT337 (a)`, forrása a `Melkizedek_tematikus.md`); a „G0813 — ἄτακτος” alszakasz és a Thayer G813 szakasz megszűnt. **A brief Mz-pontja („Grep G0813 → 0”) ezért szó szerint nem teljesülne a lábjegyzet miatt**; a feltétel finomítása döntés tárgya (DT369).
- `TORZSCIKK`: G0813 0 előfordulás; G0540 5.
- G0540 az új TUDOMANYOS-ban megjelenik a szócikk-blokkokban (tW: „a forrás nem tárgyalja”; domén: 010002 Kinship Relations Involving Successive Generations; UBS DNTG: 1 jelentés, 1 hely; kiejtés: ἀπάτωρ (apatór)).
- **Hiány (nem kitöltve, CLAUDE.md 3. szabály):** a G0540-hez nincs Thayer-sor („*G0540: nincs Thayer-sor ehhez a szerephez.*”), nincs önálló Thayer G540 alszakasz; a SECE megfelelő-lista is hiány. Ez a #132 Thayer-szakaszának hatóköre, nem a #143-é.

## 5. Következtetés az M0 ⛔-ra

A diff nem csak (i)-ből áll: a változott sorok túlnyomó része (ii), vagyis az éles írás a DT74 (3) („befagyasztva a #11 1. lépcsőjéig”) hatálya alá esik. A döntés a felhasználóé (`DONTESEK.md`, DT369); az éles írást (`--ir`) nem futtattam.
