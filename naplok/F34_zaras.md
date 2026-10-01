# F34 (BDB_PSI) — zárójelentés

*Ág: `claude/bdb-psi` · 2026.10.01 · napló: `naplok/F34_M2_naplo.md`, felmérés: `naplok/F34_M0_felmeres.md`, ellenőrzés: `naplok/ELLENOR_F34.md`*

- **Eredmény:** a BDB-forrásban 159 „ψ”-hely javítva (56 szócikk; A 100, B 57, R 2), mezőkulcsos csere-táblával (`naplok/F34_M2_csere.tsv`); diff-kapu: csak helyhivatkozás változott (318 szó = 159 `-<könyv>` + 159 `+Psa`). Új SHA-256: `5c176037…0f502f14`.
- **Igazolás:** TAHOT-próba (Zsolt c:v ±1); az A-maradék 15 helye TAHOT nélkül, a Macula MT-versszámozási táblával (a vers létezik). Köztük `Ezek 16:10` → `Psa 16:10`. A `Dan` helyek nem ψ-hibák, nem módosultak.
- **adat/forditasok.tsv:** a 78., 81. (`kezi`), 84. és 89. sor: csak helyhivatkozás-token és `forras_hash` változott (szódiffel igazolva); a 85. (H8034) sor változatlan.
- **Kapu:** `ellenoriz.py` kilépési kód 0 (13. szabály RENDBEN); a 13. kapu (fejezetszám) a javított helyekre 0, a maradékra (Péld 57–59, `2Kir 36:10`, Dán 22) jelez. `teszt_forditas_kapuk.py` 20 teszt OK, `teszt_bdb_psi_javit.py` 8 teszt OK (negatív tesztekkel).
- **Maradék: 156 hely, 94 szócikk** (A 4, B 137, R 15; `naplok/F34_M2_maradek.tsv`): N-F34 (helyőrző). Nem ψ feloldási hibák és a Dán 22:14 felülvizsgálata: N-F34c. A „TAHOT nem teljes” állítás elavult (Zsolt 150/150 fejezet, 2527/2527 vers; csak Jób 41 hiányzik): N-F34b (a `CLAUDE.md`-t nem módosítottam).
- **Újrafuttathatóság:** `eszkozok/bdb_psi_javit.py --forditas` a lefordított szövegen is; `--hash-frissit`, `--meres-tahot`; a főfutás idempotens.
- **Döntések:** DT-F34, DT-F34b, DT-F34c (a felhasználó chat-beli döntése, 2026.10.01) ✅ alkalmazva.

## Egyeztetett eltérés

- A brief fejléce `modell: opus`; a felhasználó kérésére Sonnet végrehajtó futott.
- A H6093, H7121, H1121 nincs a mostani forrásban (valószínűleg régi brief-sorok).
- Parser-javítás helyett TSV-csere: nincs `DictBDB.json` a repóban.
- A hatókör a brief 5 szócikkéről 56 szócikkre nőtt (DT-F34); DT-F34c: a 81/84 sor frissítése jóváhagyva.
- A PR megnyitása és a merge a felhasználóé; a brief `pr` mezője üres.
