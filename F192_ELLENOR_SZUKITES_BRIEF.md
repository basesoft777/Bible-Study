---
feladat: 192
cim: A független ellenőr hatókörének szűkítése — a generált kimenetet nem olvassa
kod: ELLENOR_SZUKITES
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: megallt
ag: claude/ellenor-szukites-2766eb
pr: 0
ad: a `fuggetlen-ellenor` csak a kód-, adat- és szabályváltozást olvassa; a generált lapot a CI kapui és a lektor fedik le
kovetkezo: "Te: a draft PR áttekintése és merge-e; a #183 menete már az új ellenőrrel fut"
munka: folyamat
olvas: [.claude/agents/fuggetlen-ellenor.md, MUNKAMENET.md, .claude/commands/kovetkezo.md, .claude/commands/elteres.md]
ir: [.claude/agents/fuggetlen-ellenor.md, .claude/commands/kovetkezo.md, .claude/commands/elteres.md, MUNKAMENET.md, dontesek/uj/ellenor-szukites-2766eb.md, F192_ELLENOR_SZUKITES_BRIEF.md]
fugg: []
---

# F192_ELLENOR_SZUKITES_BRIEF.md — A független ellenőr hatóköre

*FELADATOK #192 · Modell: sonnet · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó, 2026-11-11, szó szerint).** A javaslat: „a független ellenőr ezentúl csak a kód-, adat- és szabályváltozásokat nézi, a generált lapot nem. A lapot a kapuk és a lektor fedik le. Ez az ellenőrzést várhatóan a töredékére rövidíti, a technikai hibák kiszűrése pedig megmarad.” A válasz: „mehet”.

**Indok.** A HAMART #182 független ellenőrzése 30–40 percig tartott, mert a 550 KB-os generált lap diffjét is végigolvasta. A gépi egyezést a CI kapui ellenőrzik (E28, E29, olvasói kapuk), a lap olvasása a lektor dolga.

## Teendő

1. `.claude/agents/fuggetlen-ellenor.md`: új „Hatókör” szakasz; a generált kimenetek (`lexikon/*_TUDOMANYOS.md`, `*_TORZSCIKK.md`, `*_KIZARASOK.md`, `nyilt_mag/`, `generalt*/`, `# GENERÁLT` fejlécű fájl) tartalmilag kimaradnak; helyettük a generátor lefutása és a kapuk zöldje; kódváltozásnál a lap érintett blokkja célzottan. Az A1–A6 és a többi pont marad.
2. `MUNKAMENET.md` „Menet-ellenőrzés” 3a, `kovetkezo.md` 9. lépés, `elteres.md` 5. lépés: egy-egy mondat.
3. Döntés: `DT742` (`dontesek/uj/ellenor-szukites-2766eb.md`).

## Garanciák és döntési napló

- G1: a diff csak a fenti `ir` fájlokat érinti; lexikon, `adat/`, generátor, `CLAUDE.md` változatlan.
- G2: helyi E-ellenőrzés zöld.
- D1: független ellenőrzés ehhez a menethez nem készül: egy leírásfájl-csoport változik, és maga a változás csökkenti az ellenőrzést. Ez eltérés a szokásos menettől, orkesztrátori döntés.
- ⛔ A merge a felhasználóé.
