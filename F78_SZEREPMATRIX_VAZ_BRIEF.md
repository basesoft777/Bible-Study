---
feladat: 78
cim: Szerepmátrix-váz — a lexikonoldal szótári szakasza szerepenként (ISTENTISZT-001 aranyminta, TEREMT-002 második minta)
kod: SZEREPMATRIX_VAZ
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: brief_kell
ad: a lexikonoldal-generátor a `_TUDOMANYOS` 2. szakaszát szerepenként, az adat/szotar_szerepek.tsv sorrendjében rendereli, a nem adatosított szerep explicit üres blokk (adatosítás nélkül); próbarender az ISTENTISZT-001-re és a TEREMT-002-re a generalt_proba/ alá, mérési jelentéssel — ez a #23 M1, a #10 és a #11 aranymintája
kovetkezo: brief írása a DT-F52c (1)–(2) és a #64 mérésének 7. szakasza szerint; a #23 M1 előtt
olvas: [adat/szotar_szerepek.tsv, adat/SEMA.md, adat/lexikon_hivatkozasok.tsv, adat/forditasok.tsv, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/torzscikk_general.py, lexikon/ISTENTISZT-001_TUDOMANYOS.md, motivumok/TEREMT-002.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, RENDER_BRIEF.md, ADATVAGYON_TERV.md, ATALAKITASI_TERV.md.md, naplok/TEREMT002_PROZA_PROBA_meres.md]
ir: [eszkozok/lexikon_general.py, generalt_proba/]
fugg: []
nem_fugg: [38, 52]
---

# F78_SZEREPMATRIX_VAZ_BRIEF — csonk

*FELADATOK #78 · csonk-brief: nem végrehajtható, csak a feladat fejlécét és a briefbe tartozó bemeneteket hordozza · döntés: DT-F52c (1)–(2), DT-F52e (9) · forrás: `naplok/TERV_INTEGRACIO_dontesi_lista.md` 1–2. tétel, leltár R1–R2*

- **Mit ad, ha kész:** az aranyminta a szerepmátrix szerint (ADATVAGYON_TERV 18.5: „a szó-lap a mátrix renderelése; a blokkok sorrendje és töltöttsége innen jön”); a nem adatosított szerep helye explicit üres, jelölt blokk (a „memória vs. lekérdezés” szabály a renderben). Adatot nem tölt: az adatosítás a #9 dolga, a 13. szerepé (Károli-megfelelők) a #22-re épül (DT-M4: `javaslat`).
- **Miért:** a #64 mérésének 7. szakasza („A mérce korlátja”) szerint a mai `lexikon/ISTENTISZT-001_TUDOMANYOS.md` 2. szakasza Strong → forrás sorrendű, a 9., 12. és 13. szerep hiányzik; a `lexikon_general.py` 10 blokkja a mátrixtól független (a mátrix csak a `modell_epit`-ben és a törzscikk 5. szakaszában él).
- **Második minta:** a TEREMT-002 szótári része ugyanezzel a vázzal (próbarender; lexikonoldala nincs, `res_forras.tsv`- és `lexikon_hivatkozasok`-sora 0 — #64 mérés 4.), a #64 szótári mérésének pótlása.
- **Korlát:** az éles `lexikon/` nem íródik (befagyasztás a #11 1. lépcsőjéig, DT-F52c (3)); csak `generalt_proba/`.
- **Kör-feloldás:** a #23 M1 → aranyminta → #9-adat → #9 függ a #23-tól kör a vázzal megtörik: a váz szerkezet, adat nélkül; a #23 és a #9 erre függ.

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
