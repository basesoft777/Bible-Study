---
feladat: 8
cim: LXX-fordítói döntések a 87 függő igehelyre
kod: F08
tipus: feladat
fazis: 1
modell: opus
allapot: lezarva
pr: 96
ag: claude/lxx-dontesek
ad: minden ÓSZ-helyhez LXX-megfelelő (`adat/lxx_dontesek.tsv`); a 87 függő helyből 38 kap gépi LXX-megfelelőt (Macula, #17), 49 marad kutatói döntésre
kovetkezo: "merge-re kész (ellenőrizve)"
olvas: [adat/lxx_dontesek.tsv, naplok/FORRAS_FJ1_lxx_jeloltek.tsv, konkordancia/Karoli_versmegfeleltetes.tsv]
ir: [adat/lxx_dontesek.tsv, DONTESEK.md]
fugg: [1, 17]
lezarva_osszegzes: LXX-döntések (#8): a 87 függő hely 86 sora az `adat/lxx_dontesek.tsv`-ben (LD005–LD090), biztos 61 / valószínű 13 / nyitott 4 / nem_alkalmazhato 8 (a DT23 (b) szerint kitöltött 4 sor valószínű: LD027, LD035, LD052 ellentmondásos források, felhasználói döntéssel feloldva, `feloldas=DT23`; LD050 egy forrás); a Macula 38 gépi megfelelőjéből 36 megerősítve, 2 ellentmondó; SEMA 2.11 bővítve (`bizonyossag`, `nincs_heber_kulcsszo`, `feloldas=`), az `ellenoriz.py` 10. szabálya a `feloldas=`-t is ellenőrzi; a generátor csak a biztos sorokat jeleníti meg (merge-elt nulladiff: LD001–LD004 renderje és a 8 törzscikk soronként azonos, `naplok/F08_nulladiff.txt`); ellenőrzés `naplok/ELLENOR_F08.md`; PR-cím `[ELLENŐRZŐ]` (E16); DT23 ✅ (F8.8, F8.10), külön tételek N-F08a (Préd 9:10 igehely) és N-F08b (generátor-címke); zárás `naplok/F08_zaras.md`
---
# F08 — LXX-döntések mind a 87 függő igehelyre

*FELADATOK #8 · v1 · 2026.09.29*
*Modell: `opus` (kutatói ítélet)*
*Ág: `claude/lxx-dontesek` · Függ: #1, #17 (Macula-import)*

## Cél

Mind a 87 ÓSZ-helyhez LXX-sor az `adat/lxx_dontesek.tsv`-ben, bizonysági szinttel és indoklással.

## Munkaszabályok

1. **Teljes feldolgozás:** mind a 87 hely.
2. **⛔ csak egy esetben:** a meglévő `adat/` sorainak nem szándékolt csökkenése vagy törlése.
3. **A döntések a menet végére gyűlnek.** Menet közben nem állsz meg. A zárás előtt egyetlen összesített tétel kerül a `DONTESEK.md`-be (lásd 3. lépés).
4. **A számokat a fájlokból olvasd:** a PR #75 és a #17 fájljaiból, ne ebből a briefből.

## Lépések

1. **Bemenet soronként:**
   - a Macula-megfelelő (a #17 importjából; a PR #75 szerint 39 helyre van);
   - az FJ1 gépi jelöltje (`naplok/FORRAS_FJ1_lxx_jeloltek.tsv`);
   - a KK-versmegfeleltetés;
   - a görög szóalak (38 sorból 26-nál van, 12-nél nincs).
2. **Kimenet:** `adat/lxx_dontesek.tsv`. Oszlopok: hely, héber szó, LXX-megfelelő, forrás(ok), bizonyosság, egysoros indoklás.
3. **Bizonyosság:**
   - *biztos*: két független forrás egyezik;
   - *valószínű*: egy forrás, ellentmondás nélkül;
   - *nyitott*: nincs forrás, vagy a források ellentmondanak.

   A *valószínű* és a *nyitott* sorok **egyetlen** összesített `DONTESEK.md`-tételbe kerülnek, nem helyenként külön tételbe.
4. **Külső modell:** nem kell. 87 hely, szakmai ítélet; ez Opus-munka.
5. **Zárás:** a `/kovetkezo` 9–10. lépése szerint.

## Döntésnapló (v1)

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| F08-1 | Önálló feladat, az orkesztrátor futtatja, a Macula-import (#17) után | a Macula a legerősebb forrás; a felhasználó kérése | közös menet a #7-tel |
| F08-2 | Az egyes helyek nem állítják meg a menetet, a döntés egy összesített tételben jön | 87 hely, a helyenkénti megállás szétaprózná a munkát | megállás helyenként |
