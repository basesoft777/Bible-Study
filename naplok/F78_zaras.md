# F78 SZEREPMATRIX_VAZ — zárójelentés

*FELADATOK #78 · 2026.10.08 · ág: `claude/f78-szerepmatrix-vaz` · modell: sonnet · ellenőrzés: `naplok/ELLENOR_F78.md` (2 kör)*

## Mi készült
- `lexikon_general.py`: a `_TUDOMANYOS` 2. szakasza szerepenként, a `szotar_szerepek.tsv` sorrendjében; az üres blokk B változatú (`<!-- ÜRES-BLOKK: szerep | állapot -->` + látható sor); `ÜRES-NYELV` jelölő token nélküli nyelvre; a TWOT, a domén és a kiejtés a saját szerepe alá költözött.
- `szotar_szerepek.tsv` 22 → 26 sor (13., 14. szerep, `javaslat`), SEMA 2.13 frissítve; `teszt_szerepmatrix.py` (16 teszt OK).
- Próbarender `generalt_proba/` alá: ISTENTISZT-001 (aranyminta), TEREMT-002 szótári rész (második minta). Mérés: `naplok/F78_meres.md`. Az éles `lexikon/` érintetlen.

## Egyeztetett eltérés
- A DT-F78c (a) a két héber TBESH-sor bekötését írta elő. Ez a DT-F42a (licenc) miatt nem történt meg; a felhasználó a negyedik utat választotta: az ISTENTISZT-001 héber 1. szerepe a meglévő BDB-sorokra hivatkozik. Új adatsor és `jeloltek.tsv`-sor nincs.

## Nyitott
- **DT-F78d** 🟡: a tábla héber 1. sorának forrás-oszlopa (TBESH) a DT-F42a után (javaslat: forrás → BDB, állapot marad `adatosítva`). Nem blokkolja a #23 M1-et és a #9-et.
- **N-F78a**: a próba-törzscikk az éles lexikonból készül (nulla-diff nem áll) — #36, #11.
- A TEREMT-002 héber 1–2. szerepe `adatosítva, nincs bekötve`: a #9-nek a BDB-t kell bekötnie.

## Ellenőrzés (`manual`, az orkesztrátor futtatása)
`feladatok.py ellenoriz`: 102 brief, 0 hiba · `teszt_szerepmatrix.py`: OK. A 2. ellenőri kör után a harmadik nem futott (csak dokumentáció változott). Az E5 CI-hiba a main előnyéből jön, nem az ágból.
