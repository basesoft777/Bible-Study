# `/lap-javit` próbafuttatás — HODIT-001 (F123.LAPJAVIT, DT-F123f)

*scope=HODIT-001 | forras=eszkozok/lap_javit_proba.py + eszkozok/ellenoriz.py `lap_javitas_hibak` + eszkozok/lexikon_general.py `kolofon_lektoralas`, repón kívüli ideiglenes könyvtárban | ts=2026-11-04*

Éles írás nem történt: a forrás (`tematikus_lezart/Rafaim_tematikus.md`), a lap és az `adat/lap_javitasok.tsv` változatlan. A felhasználói rámutatás és jóváhagyás **szimulált**; ezért a próba-sor `jovahagyta` mezője „PRÓBA (nincs jóváhagyás)”, és a sor nem került a táblába.

## 0. Modell-ellenőrzés

Kért: `opus`; tényleges: `claude-opus-5-5` — egyezik.

## 1. Beolvasás

- A próza forrása (`adat/res_forras.tsv`): a HODIT-001 nem migrált; a kézi rések a `tematikus_lezart/Rafaim_tematikus.md` (`kivonat`, `miert_fontos`, `2b`, `ertelmezes`, `modszertan` ×4) és a `tematikus_lezart/naplok/Rafaim_kereszthivatkozas_naplo.md` (`minosites` ×2) jelölői között. Mind egészben olvasva (K1).
- Lektor-kérdéslista: nincs (`naplok/KIADAS_HODIT-001_lektor.md` nem létezik).
- Kiadási állapot: nincs `kiadasok.tsv`-sor (nem kiadott lap), nincs átnézés, nincs korábbi javítás.

## 2. Rámutatás (szimulált) és osztályozás

Idézet a lap Kivonatából: „A motívum lexikai azonosságú: a רְפָאִים (*refáim*) szótő és rokon népnevei …”

- Hely: `kivonat`, 1. mondat; a szöveg a `Rafaim_tematikus.md` `kivonat` résében áll → **`próza`**.
- Gond: a „lexikai azonosságú” a `motivumok.tsv` `azonossag_tipusa` mezőjének belső értéke, az olvasónak nem mond semmit → **`szakszó`**.

## 3.a Javaslat, ellenőrzés, előnézet

1. Első javaslat: „A motívumot egyetlen szócsalád tartja össze: …” — **az ellenőrzés elvetette**: a Zuzim, az Émim és a Zamzummim nem a רְפָאִים szótő alakja, csak rokon népnév (a mondat folytatása is így nevezi őket); az „egyetlen szócsalád” valótlant állítana.
2. Végleges javaslat:
   - régi: `A motívum lexikai azonosságú: a רְפָאִים (*refáim*) szótő és rokon népnevei`
   - új: `A motívumot a szóhasználat köti össze: a רְפָאִים (*refáim*) szótő és rokon népnevei`
3. Ellenőrzés az adat ellen: a mondat számszerű állítása („33 igehelyen”) változatlan, és egyezik az `adat/elofordulasok.tsv` HODIT-001 sorainak számával (33; Strong szerint H7497 24, H7496 8, H5303 1). A javítás új állítást nem tesz.
4. Előnézet (`python eszkozok/lap_javit_proba.py --id HODIT-001 --csere <tmp>/csere.tsv --kimenet <tmp>/futas2`): 1 csere, 2 megváltozott lapsor (csak a Kivonat mondata); olvasói kapu alap 63 BUKÁS / 25 FIGYELMEZTETÉS → új 63 / 25 (nem romlik; a BUKÁS-ok a nem migrált lap meglévő hibái, nem a javításé). A forrás `regi` szövege pontosan egyszer áll a fájlban és a lapra kerülő nézetben.

## 4. Naplózás (ideiglenes táblán)

A tábla ideiglenes másolatához fűzött sor (a meglévő sorok változatlanságát a próba ellenőrizte):

| id | hely | tipus | gond | javasolta | jovahagyta | datum |
|---|---|---|---|---|---|---|
| HODIT-001 | kivonat (1. mondat) | próza | szakszó | claude-opus-5-5 | PRÓBA (nincs jóváhagyás) | 2026.11.04 |

- `ellenoriz.py` 28. szabály (`lap_javitas_hibak`): 0 hiba.
- Ugyanez a sor `jovahagyta=claude-opus-5-5`-tel: SÉRTÉS („modellnév — jóváhagyni csak ember tud”).
- Kolofon (`kolofon_lektoralas`): `| Emberi lektorálás | 1 hely (2026.11.04); lektorálók: PRÓBA (nincs jóváhagyás) |`

## 5. Zárás

Éles menetben itt jönne: a forrás szerkesztése a jóváhagyás után, `python eszkozok/general.py --cel lexikon --id HODIT-001 --ir`, `python eszkozok/olvasoi_kapu.py HODIT-001`, `python eszkozok/ellenoriz.py`, és a régi/új lista. Kiadási sor és átnézés nem kell (nem kiadott lap).
