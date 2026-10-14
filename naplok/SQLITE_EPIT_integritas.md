# SQLITE_EPIT -- integritás-ellenőrzés (F79)

*Proveniencia: `scope=manual | forras=adat/*.tsv | ts=2026-10-14T09:33:38Z`; az ellenőrzés a betöltés ELŐTT, a TSV-sorlistákon fut, az `eszkozok/ellenoriz.py` függvényeivel (DT109 (3), (7)); építési mód: teljes.*

**1. Hivatkozási épség**: RENDBEN

**2. Nincs közvetlen út**: RENDBEN

**3. Proveniencia-kényszer**: RENDBEN

**4. Horgony-kényszer**: RENDBEN

**5. Károli-triplet**: RENDBEN

**6. Gate-kényszer (4.6)**: RENDBEN

**7. Ütközés-/részhalmaz-jelentés (gate.py)**: JELENTÉS -- 5 osztozó igehely, 4 átfedő motívumpár, 0 részhalmaz-gyanús pár (l. `python eszkozok/gate.py` a részletekért)

**8. Dataset-lefedettség (gépi)**: RENDBEN

**9. 'teljes'/'részlet' jelentes_szam korlatok (SEMA 2.2.2)**: RENDBEN

**10. LEXV2_2 tablak (forditas_ubs -- RETIRED S1.1, lxx_dontesek)**: RENDBEN -- forditas_ubs.tsv rész RETIRED (a tábla megszűnt, SZOTAR S1.1, l. adat/SEMA.md 2.10) -- a kulcs-/hash-ellenőrzés a 13. szabályban fut

**11. Rés-forrás egyezés (tanulmány/adat ≡ tábla + tanulmány)**: RENDBEN

**13. Fordítási gyorsítótár (kulcs egyediség, forras_hash)**: RENDBEN

A 7. szabály (gate.py ütközés/részhalmaz) jelentés, nem kényszer (a CLI sem számolja sértésnek); a 8/b és 8/c KÉZI sorok az `ellenoriz.py` kimenetében állnak.
