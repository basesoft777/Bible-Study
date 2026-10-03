# F46 zárójelentés — BDB_KONYVFELOLDAS (#46)

*Ág: `claude/bdb-konyvfeloldas` · modell: opus · ⛔ 3.5 megállás után a DT-F46 döntéssel folytatva · ellenőr: `naplok/ELLENOR_F46.md` (ELTÉRÉS 6, nem blokkoló; 2–5. javítva F46.9)*

- **Független forrás:** OSHL BrownDriverBriggs.xml (commit `21c9add`, CC BY 4.0); kivonat `konkordancia/OSHL_BDB_igehelyek.tsv` (4053 sor). A forrás hiányos (a szócikkek ~negyedében van igehely), ezért `magas` csak 12 sor.
- **Felmérés:** csere-tábla 1032 sor (magas 12 / kozepes 309 / kezi 711); napló `naplok/BDB_KONYVFELOLDAS_naplo.md`.
- **Gépi csere (DT-F46 szerint):** forrás 253 token / 197 szócikk (250 igehely + 3 névhiba), fordítás 54 token / 39 sor (forras_hash frissítve); H8034 védett sora változatlan. A DT-F46 kiegészítés 2 szerint a Károli-vers Strong-kapun (±1 tűrés nélkül) nem igazolt 16 csere visszaállítva (F46.14; az F46.6-ban 269 / 57 volt).
- **Kapuk:** Károli-létezés és Károli-vers Strong-kapu (ablak 0) 250/250; 13. kapu a forráson 109→63 szócikk, a fordításon JELZES 64→49; 11. kapu 432/432; `ellenoriz.py` 0 SÉRTÉS. Az F46.6 kapu (H5656) utólag jóváhagyva (DT-F46 kiegészítés).
- **Lezárva:** N-F34 és N-F34c. **Új nyitott:** N-F46a (kézi lista, 779 sor), N-F46b (teszt_bdb_zaras korábbi hibái).
- **Egyeztetett eltérés:** nincs. Döntésen túli: F46.6 kapu (a felhasználó jelezve).
- **Eldöntve (DT-F46 kiegészítés és kiegészítés 2):** a 6 sor `javasolt_karoli_alak`-ja Károli-számozású (a forrás MT marad); a README sha256-sora `dfb5b2aaa722291736d567c4e56c10d2890f2c860eadf416629e5d02f0e59acc` (előzmény: F46.6, F34, K7); a 16 nem igazolt csere visszaállítva; a `teszt_bdb_zaras` korábbi hibái N-F46b.
- **Folytatási pont:** nincs; a feladat lezárva, a merge a felhasználóé.
