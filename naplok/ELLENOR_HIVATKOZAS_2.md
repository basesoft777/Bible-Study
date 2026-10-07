# ELLENŐR (2. kör): F40 HIVATKOZAS_ELLENORZES — origin/main..995aa63

*A `fuggetlen-ellenor` jelentésének tömörített mentése (az ellenőrnek nincs fájlíró eszköze; az orkesztrátor mentette). Döntések: DT63/b/c (✅). Az 1. kör: `naplok/ELLENOR_HIVATKOZAS.md`.*

## Az 1. kör hat pontja
Az 1–5. pontot a DT63/b/c szerinti javítás kódban és tesztben megoldotta (generált blokk nyitott sora: fájl/commit HIBA, ághiány FIGYELMEZTETÉS, forrás-brief az üzenetben; Kész szakasz FIGYELMEZTETÉS; D-ág csak `olvas`; lezárt brief és nem lezárt `ir`-fedés FIGYELMEZTETÉS; kivételek dokumentálva és tesztelve; a tesztek a `futtat.py` valódi kilépési kódját mérik; F23 `ir`-bővítés csak az `ir`-t és a verziót érinti, F46/F64 fejléce, FELADATOK.md, NYITOTT_FELADATOK.md érintetlen). A 6. pont (tesztszám) a zárónaplóban újra elavult volt.

## Saját futtatás (ellenőr)
`futtat.py --valtozott … --pr-cim "[ELLENŐRZŐ] F40: …"`: E2–E26 0 HIBA; **E27: 0 HIBA, 3 FIGYELMEZTETES (FELADATOK.md:20, F46:14, F64:12), 30 JELENTES**, KILEPES=0.

## ELTÉRÉS: 4 tétel (az orkesztrátor javította az F40.11-ben)
1. Az F40 brief fejléce elavult (`dontesre_var`, „Te: DT65”) — zárásnál `lezarva`.
2. `naplok/F40_zaras.md`: a régi „Eredmény” (2 HIBA, 1 bukó teszt, 33 metódus/107 teszt) ellentmond az újnak; tényleges szám: E27Teszt 37, összesen 111, mind OK.
3. `szabalyok.py` fejkomment és `_e27_brief_terkep` docstringje a felváltott „`fugg`-beli” szabályt írta.
4. Az F40 `ir`-ből hiányzott az `F23_MOTIVUM_FORRAS_BRIEF.md`, a `naplok/F40_zaras.md`, a `DONTESEK.md`.

## NEM ELLENŐRIZHETŐ
- A tesztfuttatás az ellenőr szerepkörében (az orkesztrátor lefuttatta: `test_szabalyok.py` 111 teszt OK).
- CI-jelentés; az Actions-tokenes `ls-remote` (B-ellenőrzés): csak az első CI-futás igazolja; ha elbukik, egyetlen FIGYELMEZTETÉS jön.
