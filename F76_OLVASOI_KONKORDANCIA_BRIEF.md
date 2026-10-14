---
feladat: 76
cim: Olvasói konkordancia motívum nélkül (#25a) — kutatói felület a pardes.db-ből, előbb helyben (WSL), három váltható nézettel
kod: OLVASOI_KONKORDANCIA
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: megallt
ag: claude/olvasoi-konkordancia-m2b
ad: kutatói olvasói felület helyben (WSL): bibliaszöveg-kezdőlap könyv–fejezet–vers választóval, három váltható nézet (Olvasópult, Interlineáris, Munkaasztal), a #60 pilot teljes blokk-készlete a pardes.db-ből szerveroldali lapelőállítással, keresés (Strong, magyar szó és frázis, héber frázis), hozzáférési szintek konfigurációból, kiadási kapcsoló, telepítő szkript; mérés a VPS-t utánzó korlátokkal
kovetkezo: "/kovetkezo; M2b: kész, felhasználói vizuális összevetés (pilot és szerver egymás mellett), utána merge; M3; ⛔ M5–M7"
olvas: [ADATVAGYON_TERV.md, MUNKATERV.md, adat/szotar_szerepek.tsv, adat/SEMA.md, adat/licencek.tsv, "eszkozok/olvaso_pilot/*", eszkozok/sqlite_epit.py, naplok/OLVASOI_PILOT_ertekeles.md, naplok/SQLITE_EPIT_meres.md, DONTESEK.md]
ir: [eszkozok/olvaso_szerver/, naplok/OLVASOI_KONKORDANCIA_M0.md, naplok/OLVASOI_KONKORDANCIA_meres.md, naplok/OLVASOI_KONKORDANCIA_zaras.md, naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md, naplok/ELLENOR_F76_M2b.md]
fugg: [44, 79, 92, 95, 97]
nem_fugg: [52, 93]
---

# Olvasói konkordancia motívum nélkül — kutatói felület a `pardes.db`-ből, előbb helyben (WSL), három váltható nézettel (OLVASOI_KONKORDANCIA)

*Befogadásra váró brief-tervezet: a #76 csonkjának kitöltése (`F76_OLVASOI_KONKORDANCIA_BRIEF.md`, ugyanazon a számon és néven). Források: a DT129 (a felhasználó öt alapdöntése és a (4) pontosítása, 2026-10-13), a DT127 (saját hosting, a `pardes.db` mérete nem köt), a DT128 (modernizált Károli-réteg, nyitott), a DT124 (kiadási kapcsoló), a #60 olvasói pilot értékelő jelentése (`naplok/OLVASOI_PILOT_ertekeles.md`, 8. pont), és a látványterv (https://claude.ai/artifact/SivJAN3Q9iSFm9j8EziAiE). A csonk „Bemenet a hosting ⛔-hez és a CI-hez” szakasza (N-F76a–c) a kitöltésnél megmarad.*

**Javasolt fejléc-adatok:** `tipus: feladat` · `fazis: 1` · `modell: sonnet` · `munka: adat` · `fugg: [44, 79, 92]` · `nem_fugg: [52]` · `kovetkezo: "/kovetkezo; ⛔ M0 (terv), ⛔ M1 (helyi környezet: a disztribúció létrehozása a felhasználóé), ⛔ M5 (helyi próbaüzem), ⛔ M6 (VPS), ⛔ M7 (nyilvános közzététel)"`.

## 1. Cél

Az olvasói felület első, motívum nélküli kiadása **kutatóknak**: a kezdőlap a Károli-bibliaszöveg könyv-, fejezet- és versválasztóval; minden szóhoz és vershez a #60 pilot **teljes blokk-készlete** (39 blokk); kereséssel (ADATVAGYON_TERV 4. szakasz, 1–6., 13–15., 18–19. pont). Három, az olvasó által váltható nézet:

| Nézet | Elrendezés |
|---|---|
| **Olvasópult** | bal oldalon a folyamatos Károli-szöveg, jobb oldalon a „Szó” és a „Vers részletei” fül (a #60 pilot elrendezése) |
| **Interlineáris** | versenként minden magyar szó alatt a párosított eredeti szó és a Strong-szám, mellette a szó-lap |
| **Munkaasztal** | verslista, szöveg, és egyszerre nyitva a szó-lap és a vers részletei; Ctrl+K gyorsugrás |

Az első kiadás **helyben, WSL-ben** fut; a VPS-re telepítés és a nyilvános közzététel külön megállók.

## 2. Architektúra (DT129, DT127)

- **Adatforrás:** a `pardes.db` (a #92 után: a hat hiány pótolva, a magyar szavak indexe, újraépítve). A TSV az igazságforrás; az adatbázis belőle generált, kézzel nem szerkesztett index; a lapok és a keresés ennek nézetei.
- **Lapelőállítás a szerveren**, kérésre, állandó címekkel (pl. `/1Moz/1/4`, `/szo/H0216`) és gyorsítótárral. Az adatbázis nem kerül ki a böngészőbe; a böngésző csak a kért lap HTML-jét kapja. Előre legyártott statikus HTML az első kiadásban nincs; a kód úgy épüljön, hogy statikus export később egy paranccsal előállítható legyen.
- **A blokkok** a #60 pilot `eszkozok/olvaso_pilot/` blokklogikájából, az adatbázisra átírva (jellegjelölés: forrásadat / gépi feldolgozás / modell-kimenet; forrás- és licencsor minden blokk alatt, N-F33b).
- **Interlineáris illesztés pozíció szerint** a `token_par` táblából (a pilot sorrendi, Strong-szám szerinti illesztése nem elég: ismétlődő szónál téveszthet).
- **Hozzáférési szintek már most** (DT129 (3)): a lapelőállítás blokkonként jogosultságot néz; a szintek és a blokk–szint hozzárendelés **konfigurációban**, nem a kódban. Az első kiadásban minden blokk mindenkinek elérhető; a tartalmi szétválasztás és a DT-M6 viszonya külön döntés. Belépés és fizetés nem része.
- **Kiadási kapcsoló** (DT124): a KJV-Strong blokk minden nyilvános kiadásból kimarad (GPL), az MCGED kereskedelmi kiadásból; a pilot `--kiadas {belso,nyilvanos,kereskedelmi}` szabálya a szerveren is.
- **Magyar szótövezés** (DT129 (5)): a keresés a tőre is talál, ha a szótövezési döntés (a repón kívüli előmérés alapján, `D:\pardes_szoto\szoto\`) a hibrid megoldást jóváhagyja, és a szótő-oszlop a `pardes.db`-ben van. Addig a keresés a pontos szóalakra és a Strong-számra megy, és ezt a felület jelzi.
- **Technika:** Python 3.12 (eredetileg 3.11; egyeztetett eltérés, DT146 és M0 1. szakasz E1), kis webes keretrendszer (FastAPI vagy Flask, az M0-ban eldöntve), SQLite csak olvasásra, fordított proxy (Caddy vagy nginx). A nézetek közti váltás és a választott nézet megjegyzése az első kiadás része.

## 3. Hatókör

**Benne van**
- A webalkalmazás a fenti architektúrával; a három nézet; navigáció (könyv, fejezet, vers); keresés (Strong-szám, magyar szó, kétszavas magyar frázis, héber frázis a `frazis_pozicio`-ból).
- A helyi szerverkörnyezet leírása és telepítő szkriptje (WSL, külön disztribúció az E:-n), amely később a VPS-en is fut.
- Tesztek: lapok és keresés; a #60 D2-egyezése mindkét pilot-szakaszon (1Móz 1–25, Zsolt 22); Python 3.12 (eredetileg 3.11, DT146/E1); link- és keresési próba (N-F76b); SQL-injekció és XSS (N-F76c); hozzáférési szintek; kiadási kapcsoló.
- Mérés a VPS-t utánzó korlátokkal (1 vCPU, 2 GB RAM): vers-lap, szó-lap, keresés ideje.

**Nincs benne**
- Motívumréteg (#25b); új adat (#38, #27/#7, a #22 hiányzó ÚSZ-könyvei); a feliratos zsoltárok táblajavítása (#91); modernizált Károli-réteg (DT128).
- A szótő-oszlop előállítása (külön döntés és feladat); belépés, fizetés, a hozzáférési szintek tartalmi szétválasztása.

## 4. Lépések

- **M0 — terv (csak olvas).** Útvonalak, a három nézet, a blokkok listája a pilotból, a lekérdezések SQL-terve, a keretrendszer választása, a hozzáférésiszint-konfiguráció formája. ⛔ Jóváhagyás.
- **M1 — ⛔ helyi környezet.** Külön WSL-disztribúció az E:-n (eredetileg D:; egyeztetett eltérés, M0 1. szakasz E2), hogy a felhasználó meglévő Ubuntuja (futó projekt) érintetlen maradjon: `wsl --install -d Ubuntu-24.04 --name pardes --location E:\WSL\pardes`. **A disztribúció létrehozása és a jelszó megadása a felhasználóé**; utána a telepítő szkript (Python 3.12, csomagok, a `pardes.db` a disztribúció saját lemezén, fordított proxy).
- **M2 — alkalmazás.** Lapok és nézetek, navigáció, hozzáférési szintek, kiadási kapcsoló; tesztek.
- **M3 — keresés.** Strong-szám, magyar szó és frázis (a #92 indexén), héber frázis; a szótő-keresés, ha a szótő-oszlop addig elkészül.
- **M4 — mérés.** A VPS-t utánzó korlátokkal; D2-egyezés a pilottal; jelentés proveniencia-sorral.
- **M5 — ⛔ helyi próbaüzem.** A felhasználó átnézi; észrevételek a jelentésbe.
- **M6 — ⛔ VPS.** A KVM S VPS megrendelése a felhasználóé; telepítés a szkriptből SSH-n át, HTTPS; mért lapidő az éles szerveren. Ha a felhasználó így dönt, külön feladat.
- **M7 — ⛔ nyilvános közzététel.** Csak ha teljesül: #89 (LICENSE, a saját adat licence), DT126 (a GPL-es KJV-fájl sorsa), DT78 (17) (idézési szabály és a saját réteg licence), és a DT-M6 szerinti kiadási mód.

## 5. Elfogadás

- **K1.** Minden lap és keresés a `pardes.db`-ből jön; a #60 két szakaszán a D2-egyezés 0 eltérés, egyetlen dokumentált kivétellel: a görög szó-lapok `usz_elofordulas` blokkja, ahol a `token_strong` a TAGNT „+” Strong-láncainak elemeit is számolja, a pilot TSV-útja nem (DT-F76d: elfogadva; a lapon az érték bontása látszik).
- **K2.** A három nézet váltható, a választás megmarad; a kezdőlap a bibliaszöveg könyv-, fejezet- és versválasztóval.
- **K3.** Minden blokk jellegjelöléssel, forrás- és licencsorral; a hozzáférési szintek konfigurációból zárnak; a kiadási kapcsoló szerint a KJV-Strong és (kereskedelmi módban) az MCGED kimarad.
- **K4.** Az adatbázis a böngészőbe nem kerül ki; a frissességi teszt (a `meta` hashek egyeznek a TSV-kkel) a telepítés feltétele.
- **K5.** A VPS-t utánzó korlátokkal mért vers-lap idő a jelentésben (a pilot: 93 ms medián, szó-lap 3–5 ms); a magyar szóra keresés 100 ms alatt (#92 K5).
- **K6.** Tesztek zöldek (Python 3.12 alatt; eredetileg 3.11, DT146/E1), CI zöld, a független ellenőr eltérés nélkül zár.

## 6. Kapcsolódás

#60 (OLVASOI_PILOT), #79 (SQLITE_EPIT), #88, #89, #91, #92 (PARDES_DB_OLVASOI), #78 (szerepmátrix), #25b; DT-M4, DT-M6, DT76, DT78 (17), DT124, DT126, DT127, DT128, DT129; ADATVAGYON_TERV 3–4. és 8. szakasz; N-F76a–c (a csonkból).

## Bemenet a hosting ⛔-hez és a CI-hez

*Forrás: a Notion „Claude Code - 2.” oldal (MCP- és agent-ajánlások) átnézése, 2026-10-08. Helyőrzők; a végleges számot a `szamkiosztas` adja.*

- **N-F76a — Supabase mint 4. tárhely-opció.** Az ADATVAGYON_TERV 3. és 8. szakaszának opciói (Netlify Function, Cloudflare Workers + D1, Netlify Blobs, cPanel) mellé, a mért `pardes.db`-méret után mérlegelendő. Mellette: az ingyenes keret (500 MB) bőven fedi a becsült 30–60 MB-ot; a Postgres teljes szöveges keresése magyar szótövezést ad; beépített belépés a későbbi fizetős réteghez. Ellene: élő, külön adatbázis, amely elcsúszhat a TSV-ktől. **Feltétel (DT28):** csak generált, deploykor felülírt kimenet lehet, sosem forrás. A Supabase MCP legfeljebb csak olvasásra kapcsolható be, mert írási joggal megkerülné az adatréteget és a proveniencia-láncot.
- **N-F76b — Playwright link- és keresési próba a CI-ben.** Az ATALAKITASI_TERV 11.5 elvének („hibás kapcsolat = rossz link, azonnal látszik”) gépi végrehajtása: minden buildnél a generált oldalak bejárása — törött motívum- és igehely-link, üres keresési találat ismert kérdésre, hiányzó forrás- és licencsor egy blokk alatt (ez a #76 elfogadási pontja is). CI-tesztként, nem MCP-ként; kézi nézéshez a beépített böngésző elég.
- **N-F76c — Semgrep CI-lépés.** Amint van nyilvános keresőfüggvény: SQL-injekció a keresési paramétereken (`strong=`, `szo=`, `frazis=`) és XSS a markdownból renderelt HTML-ben. Előzmény: a feladattérkép escape-hibája (N-F53c). A Python-eszközökön ma nincs mit vizsgálnia; a lépés a #76 kódjával együtt kerül be.
