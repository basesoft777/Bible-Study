---
feladat: 30
cim: Döntés- és N-számok kiosztása merge-kor (helyőrző az ágakon)
kod: SZAMOZAS
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: claude/szamozas
ad: az ágak nem foglalnak végleges DT/N-számot; a párhuzamos merge-ek nem ütköznek sorszámon; a main-en a számokat egy Action osztja ki
kovetkezo: a helyőrző-Action és a CI-szabály megírása, a DT18 átszámozása, a nyitott ágak helyőrzőre állítása
fugg: [8, 16, 17]
olvas: [DONTESEK.md, NYITOTT_FELADATOK.md, FELADATOK.md, CLAUDE.md, .github/workflows/, eszkozok/feladatok.py]
ir: [.github/workflows/szamkiosztas.yml, eszkozok/szamkiosztas.py, eszkozok/ellenorzes/szabalyok.py, DONTESEK.md, NYITOTT_FELADATOK.md, CLAUDE.md, BRIEF_SABLON.md]
nem_fugg: [22]
---

# Döntés- és N-számok kiosztása merge-kor

*v1 · 2026.09.30 · a feladatszámot a `/befogad` adja*

## Miért

A #85–#87–#89 körben ugyanaz a hiba jött elő négyszer: több ág párhuzamosan foglalta le ugyanazt a következő `DT<n>` és `N<n>` számot (DT5 három ágon, N45 két ágon). Minden közbeékelődő merge újabb rebase-t, átszámozást és a `DONTESEK.md` duplikátum-takarítását okozta (F16.14: 4 + 3 + 12 duplikált sor). A számot ezért ne az ág, hanem a merge adja.

## A szabály

1. **Az ágon csak helyőrző áll.** Új döntés: `DT-F<nn>` (az `nn` a feladat száma). Ha egy feladat több döntést hoz: `DT-F<nn>a`, `DT-F<nn>b`, … Új nyitott tétel: `N-F<nn>`, illetve `N-F<nn>a`, … Minden hivatkozás (napló, zárójelentés, brief, TSV-megjegyzés) a helyőrzőre mutat.
2. **Végleges számot csak a main-re futó Action ad.** Merge után az Action megkeresi a helyőrzőket, a fájlbeli sorrendjükben kiosztja a következő szabad `DT<n>`, illetve `N<n>` számot, a repó összes `.md` és `.tsv` fájljában kicseréli a hivatkozásokat, majd egy commitot tesz a main-re: `szamkiosztas: DT-F17 → DT7, …`.
3. **A CI tiltja a végleges számot az ágon.** Új E-szabály (a következő szabad E-szám): PR-en a diffben új `DT<n>` vagy `N<n>` azonosító nem jelenhet meg, csak helyőrző; a helyőrzők a PR-en belül egyediek. Kivétel: maga a `szamkiosztas` commit a main-en.
4. **Ha a FELADATOK.md döntésnaplója (D-sorozat) is kézzel nő az ágakon**, ugyanez vonatkozik rá (`D-F<nn>`). Ha az generált blokk, és csak a main-Action írja, akkor nem kell vele foglalkozni. Ezt a menet elején állapítsd meg, és írd a naplóba.

## Tételek

**SZ.0 Felmérés (nem ír).** Listázd:
- a main `DONTESEK.md` összes DT-azonosítóját sorrendben (várhatóan DT1–DT7 és DT18);
- a main `NYITOTT_FELADATOK.md` legnagyobb N-számát;
- az összes nyitott távoli ágon azokat a `DT<n>`/`N<n>` azonosítókat, amelyek a main-en nincsenek (pl. `claude/f21-pilot`: DT5, DT6);
- a D-sorozat kezelését (4. pont).

**SZ.1 Eszköz.** `eszkozok/szamkiosztas.py`: helyőrzők keresése, kiosztás, csere, `--proba` (csak kiírja, mit cserélne) és `--ir` mód. Idempotens: helyőrző nélkül nem változtat semmit. Szabványos könyvtárakkal (csv-modul nélkül, a projekt szabálya szerint).

**SZ.2 Action.** `.github/workflows/szamkiosztas.yml`: main-pushra fut, ha van helyőrző. Futtatja az `--ir` módot, és commitol. Ugyanazzal a jogosultsággal és mintával készüljön, mint a FELADATOK.md generált blokkját író meglévő Action. Ne indítson végtelen ciklust (a saját commitjára ne fusson újra).

**SZ.3 CI-szabály.** Az új E-szabály a 3. pont szerint, a meglévő ellenőrző szkriptben. Hibaüzenet köznyelven: „Az ágon helyőrző kell (DT-F<nn>), a végleges számot a merge adja.”

**SZ.4 Meglévő eltérések rendbetétele.**
- **DT18 a main-en:** a #86 (Nave) valószínűleg a feladatszámot (F18) vette DT-számnak. Számozd át a következő szabad számra (a DT7 után), minden hivatkozással. Ha az SZ.0-ban kiderül, hogy a DT18 szándékos, ⛔ állj meg, és jelezd.
- **Nyitott ágak:** a main-en nem létező `DT<n>`/`N<n>` azonosítókat állítsd vissza helyőrzőre az adott ágon (egy commit ágonként, pl. `claude/f21-pilot`: DT5, DT6 → `DT-F21a`, `DT-F21b`). Ha az ágon draft PR van, a CI-nek zöldnek kell maradnia.

**SZ.5 Dokumentáció.**
- `CLAUDE.md`, új sor (szó szerint):
  > „Új döntés vagy nyitott tétel az ágon csak helyőrzővel kerül be (`DT-F<nn>`, `N-F<nn>`, több esetén `a`, `b` betűvel). Végleges számot a main-en a `szamkiosztas` Action ad merge után. Végleges `DT<n>`/`N<n>` számot ágon ne írj, a CI elutasítja.”
- `BRIEF_SABLON.md`: egy mondat a helyőrzőkről a döntés/N-tétel szakasznál.
- A `DONTESEK.md` fejlécében egy sor, amely a szabályra hivatkozik.

**SZ.6 Próba.** Egy eldobható ágon: két helyőrzős döntés, PR-en a CI zöld. Egy szándékosan végleges számmal a CI piros. A `--proba` kimenete a naplóba. A próbaágat töröld, a PR-t zárd be merge nélkül. Az Action élesben az első valódi merge-kor fut. Az első futás eredményét a következő menetzáró összefoglaló jelzi.

## Zárás

A `CLAUDE.md` menetzárása szerint: `fuggetlen-ellenor` → `naplok/ELLENOR_<feladat>.md` → push → draft PR → az összefoglaló első sora a PR linkje és a CI állapota. Legfeljebb 20 sor: SZ.0 számai, a DT18 új száma, az átállított ágak listája, és a D-sorozat kezelése.

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| 1 | A végleges számot merge után a main-Action adja | a párhuzamos ágak ne ütközzenek; a FELADATOK.md generált blokkja már így működik (D25) | az ág foglal számot, ütközésnél rebase és átszámozás (a mostani gyakorlat) |
| 2 | A helyőrző a feladatszámból képződik (`DT-F<nn>a`) | ágon belül egyedi, és a számból látszik, melyik feladat hozta | véletlen vagy dátumalapú azonosító |
| 3 | A CI tiltja a végleges számot az ágon | a szabály gépi, nem múlik azon, hogy a session emlékszik-e rá | csak `CLAUDE.md`-sor, ellenőrzés nélkül |
| 4 | A `DONTESEK.md` fájl egyben marad, nem bomlik feladatonkénti töredékekre | a sorszám-ütközés a fő baj; a sorhozzáfűzéses ütközés rebase-nél egyszerű | döntésenkénti töredékfájlok, amelyeket az Action fűz össze |
| 5 | A DT18 átszámozása ebben a menetben történik, nem a Nave-ágon | a Nave már mergelve; a javítás egy helyen, a szabállyal együtt | külön javító PR most |
