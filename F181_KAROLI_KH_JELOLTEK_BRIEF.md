---
feladat: 181
cim: A Károli-kereszthivatkozások jelölt szintjének feldolgozása (a #177 folytatása)
kod: KAROLI_KH_JELOLTEK
tipus: feladat
fazis: folyamat
modell: sonnet
ag: claude/f181-karoli-kh-jeloltek
allapot: megallt
ad: a 2 863 jelölt sor mért bontása; jóváhagyott, tesztelt gépi beemelési szabály; rétegzett szúrópróba hibaaránnyal; frissített Karoli_KH_javitott.tsv; N-F177b lezárása
kovetkezo: "Te: draft PR #675 (a 2/2-es javítókör-korlát betelt, a maradék két tétel az orkesztrátor döntésével rendezve: F181.48, F181.49); a merge a felhasználóé"
munka: folyamat
olvas: [konkordancia/Karoli_KH_javitott.tsv, konkordancia/Karoli_KH_MEK.tsv, konkordancia/Karoli_KH_MEK_README.md, konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/Karoli_1908.tsv, F177_KAROLI_KH_MEK_BRIEF.md, naplok/F177_jelentes.md, adat/SEMA.md]
ir: [konkordancia/Karoli_KH_javitott.tsv, eszkozok/karoli_kh_mek.py, eszkozok/teszt_karoli_kh_mek.py, konkordancia/Karoli_KH_MEK_README.md, naplok/F181_jelentes.md, eszkozok/karoli_kh_szuro.py, eszkozok/lekerdez.py, eszkozok/sqlite_epit.py, eszkozok/olvaso_pilot/adat.py, eszkozok/olvaso_mockup/nav_kinyer.py, dontesek/uj/f181-karoli-kh-jeloltek.md, nyitott/uj/f181-karoli-kh-jeloltek.md, nyilt_mag/*]
fugg: [177]
---

# Brief-tervezet — a Károli-KH jelölt szintjének feldolgozása (a #177 folytatása)

*Orkesztrátori tervezet, 2026-11-09, a felhasználó kérésére („igen”, a jelöltek külön feladatként). Befogadás: `/befogad`, külön sessionben. Előfeltétel: a #177 (PR #656) a main-ben.*

**Javasolt fejléc [javaslat]:** `tipus: feladat`, `fazis: folyamat`, `modell: sonnet` (gépi szabály + szúrópróba; ha a szúrópróba értelmező ítéletet kíván: az ítélet-lépés `opus`), `fugg: [177]`, `munka: folyamat`.
`olvas`: `konkordancia/Karoli_KH_javitott.tsv`, `konkordancia/Karoli_KH_MEK.tsv`, `konkordancia/Karoli_KH_MEK_README.md`, `konkordancia/TSK_kereszthivatkozasok.tsv`, `konkordancia/Karoli_1908.tsv`, `F177_KAROLI_KH_MEK_BRIEF.md`, `naplok/F177_jelentes.md`, `adat/SEMA.md`.
`ir`: `konkordancia/Karoli_KH_javitott.tsv`, `eszkozok/karoli_kh_mek.py` [javaslat], `eszkozok/teszt_karoli_kh_mek.py`, `konkordancia/Karoli_KH_MEK_README.md`, `naplok/F<nn>_jelentes.md`, `nyilt_mag/*` (ha a nyílt mag a KH-indexet hordozza).

## Előzmény
A #177 a Károli-kereszthivatkozásokat a MEK 00161 kiadással (DT-F177b: közkincs) mint második tanúval háromszintűre bontotta: **megerősített 21 314** (lapra kerül), **kiesik 11 027** (végleg ki), **jelölt 2 863** (eltér a két forrás, vagy csak a MEK-ben áll; döntés nélkül maradt, versellenőrzéssel és TSK-támogatással jelölve). A MEK-nek saját elírásai vannak (pl. 2Móz 6:20 → „2Móz 26,59” = 4Móz 26:59; 5Móz 21:23 → „Gal 2,13” = Gal 3:13).

## Tételek
**J0** — modell-ellenőrzés; a #177 a main-ben.
**J1 — a jelölt szint mérése és bontása** (mérd, ne ebből a tervezetből vedd): altípusok (eltér: tartomány-/vershatár-eltérés, könyv-elírás, fejezet-elírás, versszám-elírás; csak MEK), soronként a versellenőrzés (`Karoli_1908`) és a TSK-támogatás eredménye; bontási napló.
**J2 — gépi beemelési szabály** (a szabály ⛔ előtte a felhasználó/orkesztrátor jóváhagyása): pl. ha a MEK-sor (vagy a HunKar-sor) célverse létezik, és a TSK is ugyanarra a célversre mutat → `megerositett` (két független tanú: MEK/HunKar + TSK); ha a MEK-elírás egyértelműen javítható (a HunKar és a TSK ugyanarra a helyes célra mutat) → a javított cél `megerositett`, a MEK-elírás a naplóba. A szabály egy helyen (README), tesztelve.
**J3 — a maradék szúrópróbája:** a gépi szabállyal nem dönthető sorokból rétegzett minta (könyvenként), a mért hibaaránnyal; a döntés nélküli maradék `jelolt` marad, és ezt a README kimondja (hiányt nem töltünk ki).
**J4 — a tábla frissítése** (`Karoli_KH_javitott.tsv`, sorszám-napló Δ), a szűrő és a fogyasztók változatlanok; a lapok NEM generálódnak újra (a motívumonkénti teljes folyamatban kapják meg, N-F177a).
**J5 — jelentés, független ellenőr, draft PR.**

## Nem része
Lapok újragenerálása; a `kiesik` szint újranyitása; új dataset.
