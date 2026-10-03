# F46 zárójelentés — BDB_KONYVFELOLDAS (#46)

*Ág: `claude/bdb-konyvfeloldas` · modell: opus · ⛔ 3.5 megállás után a DT-F46 döntéssel folytatva · ellenőr: `naplok/ELLENOR_F46.md` (ELTÉRÉS 6, nem blokkoló; 2–5. javítva F46.9)*

- **Független forrás:** OSHL BrownDriverBriggs.xml (commit `21c9add`, CC BY 4.0); kivonat `konkordancia/OSHL_BDB_igehelyek.tsv` (4053 sor). A forrás hiányos (a szócikkek ~negyedében van igehely), ezért `magas` csak 12 sor.
- **Felmérés:** csere-tábla 1032 sor (magas 12 / kozepes 309 / kezi 711); napló `naplok/BDB_KONYVFELOLDAS_naplo.md`.
- **Gépi csere (DT-F46 szerint):** forrás 269 token / 207 szócikk (266 igehely + 3 névhiba), fordítás 57 token / 42 sor (forras_hash frissítve); H8034 védett sora változatlan.
- **Kapuk:** Károli-létezés 266/266; 13. kapu a forráson 109→60 szócikk, a fordításon JELZES 64→47; 11. kapu 432/432; `ellenoriz.py` 0 SÉRTÉS. Döntésen túli F46.6 kapu (H5656), csak szigorít.
- **Lezárva:** N-F34 és N-F34c. **Új nyitott:** N-F46a (kézi lista, 763 sor).
- **Egyeztetett eltérés:** nincs. Döntésen túli: F46.6 kapu (a felhasználó jelezve).
- **Nyitott, a felhasználó dönt:** (1) 6 sor (H2204, H7871, H2938, H7138, H3940, H1932) MT-számozású Károli-alakja: MT vagy Károli számozás legyen-e a `javasolt_karoli_alak`-ban és a fordításban (nem került fordításba; a forrásban a csere megtörtént). (2) `BDB_teljes_unabridged_README.md` sha256-sora elavult (`ff5357fe…f427a0` az új). (3) `teszt_bdb_zaras` 2 FAIL + 1 ERROR már a változtatás előtt is fennállt.
- **Folytatási pont:** nincs; a feladat lezárva, a merge a felhasználóé.
