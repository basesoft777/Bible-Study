---
feladat: 17
cim: Macula-import, héber és görög (N31)
kod: F17
tipus: feladat
fazis: 1
modell: sonnet
allapot: lezarva
ad: Macula a Strong-számhoz és a KK-hoz kötve; a #8 fő forrása
kovetkezo: `/kovetkezo` csomag: #16–#19 és #7
olvas: [konkordancia/Karoli_versmegfeleltetes.tsv]
ir: [naplok/F17_illesztetlen.tsv, konkordancia/Macula_heber_*.tsv, konkordancia/Macula_gorog.tsv, NYITOTT_FELADATOK.md, DONTESEK.md, adat/datasetek.tsv, naplok/F17_import_naplo.md, naplok/F17_87_hely.tsv, naplok/F17_import_stat.json, naplok/F17_kezi_fejezetek.tsv, eszkozok/f17/*]
fugg: [6]
ag: claude/macula-import
pr: 87
lezarva_osszegzes: Macula-import (#17): héber 475 911 és görög 275 520 sor a KK-hoz kötve (CC BY 4.0, UBS-mezők nélkül), a 87 hely 38 LXX-megfelelővel (F06: 39, közös módszerhiba javítva); ellenőrzés `naplok/ELLENOR_F17.md`; a Dán 4, a szerepmátrix és a fájlméret DT6-ben nyitva
---
# F17 — Macula-import, héber és görög

*FELADATOK #17 · N31 · v1 · 2026.09.29*
*Modell: `sonnet`*
*Ág: `claude/macula-import` · Függ: #6 · Párhuzamosan fut: #16, #18, #19 · Erre épül: #8*

## Cél

A Macula teljes importja (a letöltés héber és görög része) az adatrétegbe.

## Lépések

1. **Licenc:** vesd össze a Macula licencét a repóéval.
2. **Import:** teljes import, a Strong-számhoz és a Károli-kulcshoz (KK) kötve.
   - Ahol a Strong-szám vagy a KK-vers nem illeszthető, a sor `javaslat` jelölést kap.
   - Az illeszthetetlen sorok listája: `naplok/F17_illesztetlen.tsv`.
3. **Ellenőrző szám a #8-hoz:** a 87 függő hely közül hányhoz ad LXX-megfelelőt az import. A PR #75 szerint ez 39. Az eltérést naplózd.
4. **Külső modell:** nem kell. Strukturált adat, az illesztés determinisztikus.

## Munkaszabályok (a négy importfeladatban azonosak: #16–#19)

1. **Teljes feldolgozás:** teljes Biblia, teljes állomány, ne minta.
2. **Párhuzamos futás:** ez a feladat a #16–#19 másik hárommal egy időben fut, az orkesztrátor csomagjában, saját worktree-ben és saját ágon.
   - Csak a saját fájljaidat hozd létre vagy módosítsd: a saját `adat/` fájlokat, a saját naplót és a `FELADATOK.md` saját sorát.
   - Közös fájl a `adat/szotar_szerepek.tsv` és a `NYITOTT_FELADATOK.md`. Ezekben csak a saját soraidat írd.
   - A PR előtt futtass `git rebase origin/main`-t. Ütközés esetén mindkét oldal sorait tartsd meg.
   - Az importdöntések döntésnapló-sorait (D14–D19) a chat már rögzítette. Új D-sort ne írj.
3. **⛔ azonnali megállás csak ebben a két esetben:**
   - licencütközés;
   - a meglévő `adat/` vagy `konkordancia/` sorainak nem szándékolt csökkenése vagy törlése.
4. **A többi döntés a menet végére gyűlik.** Menet közben ne állj meg. Az érintett adatsor `javaslat` jelölést kap. A zárás előtt nyiss egyetlen összesített tételt a `DONTESEK.md`-ben, gépi javaslattal.
5. **A számokat a PR #75 mérési fájljaiból olvasd**, ne ebből a briefből. Eltérés esetén a fájl az irányadó, az eltérést naplózd.
6. **Minden importnál naplózd:** forrás, licenc, verzió vagy commit, sorszám. A szerepmátrixba (`adat/szotar_szerepek.tsv`) is kerüljön bejegyzés.
7. **Zárás a `/kovetkezo` 9–10. lépése szerint:** `fuggetlen-ellenor`, zárójelentés, a saját sor frissítése, draft PR. A `NYITOTT_FELADATOK.md`-ben zárd le a saját N-tételedet.
