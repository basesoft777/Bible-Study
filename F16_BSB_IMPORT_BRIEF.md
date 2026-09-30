---
feladat: 16
cim: BSB-import, teljes Biblia (N30)
kod: F16
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: claude/bsb-import
ad: BSB minden könyvre, ahol a lefedettség ≥ 95%
kovetkezo: `/kovetkezo` csomag: #16–#19 és #7
olvas: [konkordancia/Karoli_versmegfeleltetes.tsv]
ir: [naplok/F16_bsb_lefedettseg.tsv, konkordancia/BSB_Strongs.tsv, NYITOTT_FELADATOK.md, DONTESEK.md]
fugg: [6]
---
# F16 — BSB-import, teljes Biblia

*FELADATOK #16 · N30 · v1 · 2026.09.29*
*Modell: `sonnet`*
*Ág: `claude/bsb-import` · Függ: #6 · Párhuzamosan fut: #17, #18, #19*

## Cél

A BSB importja minden olyan könyvre, amelyen a lefedettség eléri a küszöböt.

## Lépések

1. **Licenc:** vesd össze a BSB licencét a repóéval.
2. **Mérés:** mérd a lefedettséget mind a 66 könyvre, ugyanazzal a szkripttel és módszerrel, mint a PR #75 1Mózes-mérésénél (ott 98,83% volt). A mérés eredménye: `naplok/F16_bsb_lefedettseg.tsv`.
3. **Import:** a küszöb könyvenként 95%. Az ennél jobb könyveket importáld. A küszöb alattiakról egy összesített tétel kerüljön a `DONTESEK.md`-be, könyvenként a mért értékkel.
4. **Külső modell:** nem kell. A munka determinisztikus, a meglévő mérőszkripttel fut.

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
