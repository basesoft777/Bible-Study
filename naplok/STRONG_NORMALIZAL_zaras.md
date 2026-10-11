# STRONG_NORMALIZAL — zárás (F62, M3)

*2026.10.11 · ág: `claude/strong-normalizal` · részletek: `naplok/STRONG_NORMALIZAL_M0.md` (7. pont), ellenőri jelentés: `naplok/ELLENOR_STRONG_NORMALIZAL.md`*

- **Kész:** `eszkozok/strong_util.py` (`strong_normalizal`, `strong_ervenyes`), `eszkozok/teszt_strong_util.py`, `eszkozok/strong_meres.py` (reprodukálható mérés); a `lekerdez.py` és a `betolt.py` bekötve.
- **Szabály:** 1–4 jegy négyre nullázva; vezető nullás ötjegyű a nullát elhagyja (`G00120` -> `G0120`); **G-kiegészítő kód** (`G` + öt számjegy, nem nullával kezdődik: `G20447` x2, `G20833` x1 a TAGNT-ben) érvényes és változatlan (DT-F62b, SEMA 1.2 egysoros bővítés); H-nál ötjegyű, `A####`, utótag (`utotag=tilt`), előtag nélküli szám (`nyelv=` nélkül) ValueError.
- **Leltár:** ≥28 Strong-függvény/regex, ebből 14 négyjegyűre nulláz; utótag-, hiba- és H/G-kezelésük eltér.
- **Mérés (`python eszkozok/strong_meres.py`):** a STRONG-típusú oszlopok (11 oszlop az `adat/` nem-`karoli_strong` tábláiban + 38 `karoli_strong/` fájl + a `Karoli_Strong_kivonat.tsv` oszlopa) 0 SEMA-eltérés; **ezen kívül 113 forrásalakú érték** áll nem STRONG-típusú oszlopban (`forditasok.tsv`/`lexikon_hivatkozasok.tsv` `entry_id`, 108 + 5), ezek nem normalizálandók. Adattábla nem változott.
- **`lekerdez.py`:** `scan`/`igealak`/`kollokacio` és a `domen` egyszerű `H####`/`G####` argumentuma szigorú (hiba a helyes alakkal, DT-F62a); `scan G20447` 2, `scan G20833` 1 igehely, mint a régi kódnál. **Kivétel:** a `domen` saját kódtere (`A####`, betűutótagos `H0032a`) nem SEMA 1.2, a kódban kimondva változatlan.
- **`betolt.py`:** a `kulcsszo` stdout-ja, `--md` és a `--ir` utáni `kulcsszavak.tsv` bájtra azonos; nem SEMA-alakú study-értékre csak stderr-figyelmeztetés (K2, DT-F62a).
- **Talált eset:** `genezis/1Moz_16_bovitett.md` kulcsszavai közt `H410`, `H883` nullázatlan (`--ir` így írná); a study javítása külön tétel.
- **Csere-javaslat (külön `/befogad`):** (1) pad-4 normalizálók (`emeles`, `ellenoriz`, `ellenorzes/szabalyok`, `ellenorzes/tanulmany_ellenorzes`, `karoli_strong/tokenek`, `karoli_strong/elopar_kjv`, `lxx_osszevetes`, `lexikon_general`) cseréje, kimenet-azonosság igazolásával; (2) `merge_karoli_szofaj`, `tbesh_konszolidalt_import`, `bdb_adatblokk`: csak újragenerálással; (3) `tw_import.py` csonkolása: N-F62a; (4) CI-szabály külön tétel.
- **N21 lezárási javaslat:** a `Karoli_Strong_kivonat.tsv` `H922` javítva (KB3, `4ecb612`), a mérés 0 eltérést ad; az N21 a „Lezárva” szakaszba vihető, a felhasználó jóváhagyásával.
- **Nyitva:** N-F62a; a `betolt.py --ir` a study nullázatlan értékét változatlanul írná; az új független ellenőrzés a fő sessionből indul (a brief `allapot: fut` marad).
