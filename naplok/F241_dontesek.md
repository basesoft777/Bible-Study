# F241 — az integrátor döntései (a session a fájl aktuális állapotát hajtja végre)

*MUNKAMENET „Szereposztás”: egy sor = sorszám, dátum, kérdés – döntés – indok, a szerkesztő szava, ha van, és a visszavont sor („visszavonja: D<n>”). Lépéshatáron és commit előtt újraolvasandó.*

Forrás mindegyik sornál: szerkesztői döntés — az integrátor, a felhasználó felhatalmazásával; 2026-11-23.

- **D1** (2026-11-23) — Befogadás. Kérdés: befogadható-e a 218c briefje a tervezet szerint? Döntés: igen, változtatás nélkül. Indok: a 218c az IRANY „Következő szálak” első sora (DT936); a brief az N243 (1)–(7) minden pontját lefedi, három kis PR-ra bontva.
- **D2** (B1) (2026-11-23) — Kérdés: az N236 teljes egészében a 218c-be tartozik-e? Döntés: csak az átálló három lap (ISTENTISZT-001, HAMART-001, TEREMT-001) jelölésfajtái; a többi a befagyasztott motívumok nulláról írt cikkeivel (#123). Indok: a befagyasztott lapok nem generálódnak újra, ezért a többi jelölésfajtának most nincs fogyasztója.
- **D3** (B2) (2026-11-23) — Kérdés: a #70 és a #123 kézi függés legyen-e? Döntés: nem_fugg: [70, 123]. Indok: a 241 a motívumfájlokat csak olvassa, jóváhagyott állapotban; a #70 befagyasztva, a #123 maga is az új generátort várja, kézi függésként kör adódna. Ha közben a #70 vagy a #123 indulna, a motívumfájlon egyszerre egy feladat fut (D39).
- **D4** (B3) (2026-11-23) — Kérdés: az N242 D (ISTENTISZT-001, 1Móz 4:26 → 2Móz 33:19 kapcsolat-cella csupasz Strong-száma) a 2. kiadásba kerüljön-e? Döntés: igen, a 2. kiadásba (F241.7), egysoros célzott nézéssel, a szerkesztőhöz az integrátoron át. Indok: különben a 2. kiadás ismert csupasz Strong-számmal jelenne meg, és egy 3. kiadás kellene.
- **D5** (B4) (2026-11-23) — Kérdés: a kis adatjavítás (#821, LXX-párok) és az F241.11 (a B36 tábla újragenerálása) sorrendje? Döntés: a #821 előbb. Ha az F241.11-hez érve a #821 még nincs a main-en, a B szelet többi lépését (F241.12) végzed előbb, és jelzel; a B36 táblát a #821 merge-e előtt nem írod. Indok: a #821 hamis tartalmat javít; két ág nem ír egy fájlba. (A #821 szálhelye a TEREMT-001 szünetében várható, amikor a cikk a 218c-re vár.)
- **D6** (B5) (2026-11-23) — Kérdés: a #236 és a #237 a 241 egészét várja-e? Döntés: igen, a levezetett függés szerint. Indok: a lapgen/ és a lapgen_bemenetek.tsv közös; ez megfelel a DT933-nak.
- **D7** (2026-11-23) — Kérdés: az IRANY 218c-sorának „előtte az olvasóban a forrássor a névtáblából, és egy névtábla” feltétele a #810 része vagy a 218c külön előfeltétele? Döntés: egyik sem; az olvasó újraépítésébe tartozik (blokk-jegyzék, egy névtábla), amely a szerkesztő 2026-11-23-i iránya szerint a generátor után jön. A brief kovetkezo mezője nem változik. Indok: a szerkesztő: „a 218c a #810 után azonnal”, és az újraépítés kódja a generátor után; ez a mondat a korábbi, javítókörös olvasó-irányból maradt az IRANY-ban, ott javítom.

*Végrehajtás csak a #810 merge-e után, az integrátor jelére.*
