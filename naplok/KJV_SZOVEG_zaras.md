# KJV_SZOVEG — zárójelentés (#118, F118)

**Egyeztetett eltérés:** az új eBible-zip (sha256 `00532b6d…d447`, 2026-10-17) a brief `1bab5d4d…` hash-e helyett; a Strong-réteg ezzel bájtra azonos a #19-es táblával (M0). Táblaforma: `Elotte`/`Utoirat` oszlop, `[…]` és `‹…›` jelölés (DT213). Döntések: DT210 1. (`kozkincs`), DT211 (a) (saját importáló), DT214 (b) (külön feladat, `beerkezo/`-tervezet), DT212 (d) (a zip a repón kívül), DT213 (a minta).

**Fő számok.** `konkordancia/KJV_teljes_szoveg.tsv`: 31 218 sor (31 102 vers + 116 zsoltárfelirat); 22 `Elotte`, 14 `Utoirat`. M-a: S ⊆ T, T ∖ S = a 3 címke nélküli vers (= `F19_hianyok.tsv`). M-b: 362 399 szóelem, megmagyarázatlan eltérés 0 (76 összetett szó, 8 szótöredék). M-c: üres szöveg 0, vershíd 0, a veszteség-sor 9/9 tételben egyezik a nyers forrással. 29 teszt OK, az újragenerálás adatsorai bájtra azonosak, és az importáló írás előtt összevet (`--felulir`). Független ellenőrzés: `naplok/ELLENOR_KJV_SZOVEG.md` (2 alacsony súlyú ELTÉRÉS, javítva: F118.22 és a fejléc).

**E6, `git diff --stat origin/main..HEAD`** a védett fájlokra (`KJV_Strongs_teljes.tsv`, `F19_hianyok.tsv`, `f19_ebible_import.py`, `Karoli_versmegfeleltetes*`, `tsk_kulcs.py`, `eszkozok/bdb_jelolt/`, `eszkozok/olvaso_szerver/`, `sqlite_epit.py`): **üres**. Az `adat/`-ban csak hozzáfűzés történt: `SEMA.md` +7, `datasetek.tsv` +4, `licencek.tsv` +1 sor.

**Nyitott pontok.**
- A zip második példányának helye: megadandó (a felhasználó adja meg; `adat/SEMA.md` 2.6).
- A DT126 (a `KJV_Strongs_teljes.tsv` GPL-kérdése) nyitott.
- Nyitott a CrossWire szövegszintű hozzájárulásának kérdése is (`licencek.tsv`, kitöltés nélkül).
- A megjelenítési tervezet (`beerkezo/KJV_SZOVEG_MEGJELENITES_BRIEF_TERVEZET.md`) befogadása `/befogad`-dal, a #118 merge-e után, külön lépésben. A tervezet előfeltétele a #117 és az N-F117a; M0-kérdése a kereskedelmi kiadás.

**Merge-sorrend.** A #107 is írja a `licencek.tsv`-t, a `datasetek.tsv`-t és a `SEMA.md`-t. A #118 csak hozzáfűzött, rebase-nél mindkét oldal sorai maradnak (a `SEMA.md`-ben a 2.6 `KJV_Strongs_teljes`-mondata után áll a #118 bekezdése).
