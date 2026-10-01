# F34 (BDB_PSI) — zárójelentés

*Ág: `claude/bdb-psi` · 2026.10.01 · részletes napló: `naplok/F34_M2_naplo.md`, felmérés: `naplok/F34_M0_felmeres.md`*

- **Eredmény:** a BDB-forrásban 159 „ψ”-hely javítva (56 szócikk; A 100, B 57, R 2), mezőkulcsos csere-táblával (`naplok/F34_M2_csere.tsv`), diff-kapuval: csak helyhivatkozás változott. Új SHA-256: `5c176037…0f502f14`.
- **Igazolás:** TAHOT-próba (Zsolt c:v ±1); az A-maradék 15 helye TAHOT nélkül, a Macula MT-versszámozási táblával (a vers létezik). Köztük `Ezek 16:10` → `Psa 16:10` (rejtett eset, elfogadva).
- **adat/forditasok.tsv:** a 78. (H8415, `kezi`) és 89. (H0430) sor tokenjei és `forras_hash`-e javítva; a 81. (H7585, `kezi`) sorban 2 token (Ez 16:10, 49:16) javult az F34.3-ban. A 81. és 84. sor forrása a DT-F34b után tovább változott, a sorokat a döntés szerint nem írtam át, így a `forras_hash` elavult.
- **Kapu:** a 13. kapu (fejezetszám) a 78. és 89. soron 0; a 81. (Ez 73), 84. (Péld 57–59, `2Kir 36:10`) és 85. (Dán 22) soron a maradék miatt még jelez. `ellenoriz.py`: 13. szabály **SÉRTÉS (2)** — a 81. és 84. sor elavult `forras_hash`-e (kilépési kód 1); a 78., 85., 89. sor RENDBEN. `teszt_forditas_kapuk.py` 20 teszt OK (köztük negatív), `teszt_bdb_psi_javit.py` 6 teszt OK.
- **Maradék: 163 hely, 99 szócikk** (A 4, B 144, R 15; `naplok/F34_M2_maradek.tsv`) — nem javítva; N-F34 (helyőrző). A `Dan 22:14` forráshiba, nem hatókör.
- **Újrafuttathatóság:** `eszkozok/bdb_psi_javit.py --forditas` a csere-táblát a lefordított BDB-szövegen is alkalmazza (a 81/84/85. sort kihagyva), ezért a maradék nem blokkolja a BDB-fordítást; a főfutás idempotens.
- **Nyitott (helyőrző):** N-F34 (B/R maradék kézi nézet; a hash-elavulás rendezése), N-F34b (a „TAHOT-kivonat nem teljes” állítás elavult: Zsolt 150/150 fejezet, 2527/2527 vers; egyetlen fejezet-rés: Jób 41).

## Egyeztetett eltérés

- A brief fejléce `modell: opus`; a felhasználó kérésére Sonnet végrehajtó futott.
- A H6093, H7121, H1121 nincs a mostani forrásban (valószínűleg régi brief-sorok).
- Parser-javítás helyett TSV-csere: nincs `DictBDB.json` a repóban.
- A hatókör a brief 5 szócikkéről 56 szócikkre nőtt (DT-F34 jóváhagyta).
- A `fuggetlen-ellenor` futtatása és a merge a felhasználóé / az orkesztrátoré.
