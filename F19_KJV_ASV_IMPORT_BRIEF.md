---
feladat: 19
cim: KJV/ASV-import, eBible (N29)
kod: F19
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ad: Strong-címkés KJV és ASV, a hiányok besorolásával
kovetkezo: végrehajtás fut (vegrehajto-sonnet)
ag: claude/kjv-asv-import
olvas: [konkordancia/KJV_Strongs_Genesis.tsv, konkordancia/ASV_Strongs_Genesis.tsv]
ir: [naplok/F19_hianyok.tsv, konkordancia/KJV_Strongs_teljes.tsv, konkordancia/ASV_Strongs_teljes.tsv, NYITOTT_FELADATOK.md, DONTESEK.md]
fugg: [6]
---
# F19 — KJV/ASV-import (eBible)

*FELADATOK #19 · N29 · v1 · 2026.09.29*
*Modell: `sonnet`*
*Ág: `claude/kjv-asv-import` · Függ: #6 · Párhuzamosan fut: #16, #17, #18*

## Cél

A Strong-címkés KJV és ASV teljes importja az eBible-ből.

## Lépések

1. **Licenc:** vesd össze az eBible és a luvlylavnder licencét a repóéval.
2. **Import:** az eBible KJV és ASV teljes importja.
3. **Hiányok besorolása:** a 3 címkézetlen KJV-verset és az ASV hiányzó verseit sorold be (versszámozási eltérés vagy adathiány), keresztben a luvlylavnder ellen. Eredmény: `naplok/F19_hianyok.tsv`. Az adathiány-sorok egy összesített `DONTESEK.md`-tételbe kerülnek.
4. **A scrollmapper kimarad.**
5. **Külső modell:** nem kell. A versszámozási eltérések szabályalapon besorolhatók.

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
