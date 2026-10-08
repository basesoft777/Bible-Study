---
feladat: 76
cim: Olvasói konkordancia motívum nélkül (#25a)
kod: OLVASOI_KONKORDANCIA
tipus: feladat
fazis: 1
modell: sonnet
allapot: brief_kell
olvas: [ADATVAGYON_TERV.md, MUNKATERV.md, adat/szotar_szerepek.tsv, adat/SEMA.md, adat/licencek.tsv]
nem_fugg: [52]
ad: vers- és szó-lap, variancia-térkép, magyar frázis-keresés és konkordancia motívum nélkül, kereséssel (ADATVAGYON_TERV 4. szakasz, 1–6, 13–16, 18–20. pont)
kovetkezo: brief a hosting ⛔ előtt, a #79 (SQLITE_EPIT) után; a briefbe: DT-M4/DT-M6 🟢 (DT76), az openbible-import befogadása (DT34, DT77 (14)), szó-lap a szerepmátrix szerint (#78), az idézési szabály és a saját réteg licencének DT-tétele a publikálás előtt (DT78 (17))
fugg: [44, 79]
---

# F76_OLVASOI_KONKORDANCIA_BRIEF — csonk

*FELADATOK #76 (= a DT-M1 #25a-ja) · csonk-brief: nem végrehajtható, csak a feladat fejlécét és a briefbe tartozó bemeneteket hordozza · döntés: DT-M1*

- **Mit ad, ha kész:** az olvasói felület első, motívum nélküli kiadása: vers- és szó-lap, variancia-térkép, magyar frázis-keresés, konkordancia, kereséssel. A motívumos nézet a #25 (#25b) dolga.
- **Következő lépés:** brief a hosting ⛔ előtt, a #79 (SQLITE_EPIT) után.
- **Függés:** #44 (kész), #79 (SQLITE_EPIT, DT77 (12)). **Fázis:** `1` — a D1 kiegészítése (DT75 (7), FELADATOK D51): a #76 a kész Károli–Strong könyvekkel indulhat, az 1. fázis lezárása nélkül.
- **A DT-M1 szerint a briefbe tartozó feltételek:** DT-M4 és DT-M6 (🟢, DT76), hosting ⛔, nem kereskedelmi mód, N-F33b (mezőszintű forrás- és licencjelölés); az openbible-import befogadása (DT77 (14)); az idézési szabály és a saját réteg licencének DT-tétele a publikálás előtt (DT78 (17)).

## Bemenet a hosting ⛔-hez és a CI-hez

*Forrás: a Notion „Claude Code - 2.” oldal (MCP- és agent-ajánlások) átnézése, 2026-10-08. Helyőrzők; a végleges számot a `szamkiosztas` adja.*

- **N-F76a — Supabase mint 4. tárhely-opció.** Az ADATVAGYON_TERV 3. és 8. szakaszának opciói (Netlify Function, Cloudflare Workers + D1, Netlify Blobs, cPanel) mellé, a mért `pardes.db`-méret után mérlegelendő. Mellette: az ingyenes keret (500 MB) bőven fedi a becsült 30–60 MB-ot; a Postgres teljes szöveges keresése magyar szótövezést ad; beépített belépés a későbbi fizetős réteghez. Ellene: élő, külön adatbázis, amely elcsúszhat a TSV-ktől. **Feltétel (DT28):** csak generált, deploykor felülírt kimenet lehet, sosem forrás. A Supabase MCP legfeljebb csak olvasásra kapcsolható be, mert írási joggal megkerülné az adatréteget és a proveniencia-láncot.
- **N-F76b — Playwright link- és keresési próba a CI-ben.** Az ATALAKITASI_TERV 11.5 elvének („hibás kapcsolat = rossz link, azonnal látszik”) gépi végrehajtása: minden buildnél a generált oldalak bejárása — törött motívum- és igehely-link, üres keresési találat ismert kérdésre, hiányzó forrás- és licencsor egy blokk alatt (ez a #76 elfogadási pontja is). CI-tesztként, nem MCP-ként; kézi nézéshez a beépített böngésző elég.
- **N-F76c — Semgrep CI-lépés.** Amint van nyilvános keresőfüggvény: SQL-injekció a keresési paramétereken (`strong=`, `szo=`, `frazis=`) és XSS a markdownból renderelt HTML-ben. Előzmény: a feladattérkép escape-hibája (N-F53c). A Python-eszközökön ma nincs mit vizsgálnia; a lépés a #76 kódjával együtt kerül be.

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
