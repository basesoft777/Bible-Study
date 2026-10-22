---
feladat: 135
cim: Az olvasói felület VPS-re telepítése és nyilvános közzététele — a #76 M6 és M7 lépése önálló feladatként
kod: OLVASO_VPS
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: nem_indult
helyi_gep: igen
ad: az olvasói felület a KVM S VPS-en fut a telepítő szkriptből, HTTPS-sel, friss pardes.db-vel és zöld tesztekkel; a mérvadó lapidő-mérés (K5) az éles szerveren; a nyilvános közzététel a licencfeltételek teljesülése után, külön ⛔-pel
kovetkezo: "/kovetkezo; ⛔ M0 (terv: a #120 utáni építés, a #134 viszonya, tárhely-opciók), ⛔ M2 (VPS megrendelése a felhasználóé), ⛔ M4 (éles próbaüzem), ⛔ M5 (nyilvános közzététel)"
olvas: [F76_OLVASOI_KONKORDANCIA_BRIEF.md, naplok/OLVASOI_KONKORDANCIA_zaras.md, naplok/OLVASOI_KONKORDANCIA_meres.md, naplok/OLVASOI_KONKORDANCIA_M0.md, ADATVAGYON_TERV.md, adat/licencek.tsv, eszkozok/sqlite_epit.py]
ir: [eszkozok/olvaso_szerver/telepit.sh, eszkozok/olvaso_szerver/indit.sh, eszkozok/olvaso_szerver/blokkok.py, naplok/OLVASO_VPS_M0.md, naplok/OLVASO_VPS_meres.md, naplok/OLVASO_VPS_zaras.md]
fugg: [76, 120]
---

# F135_OLVASO_VPS_BRIEF.md — Az olvasói felület VPS-re telepítése és nyilvános közzététele

*FELADATOK #135 · Modell: opus [javaslat] · v1 · 2026.10.22 · Forrás: a #76 M6 és M7 lépése, amelyet a felhasználó döntése (DT-F76p, 2026-10-22) vett ki a #76-ból, és a #76 zárásakor átadott feltételek és nyitott tételek (DT-F76r; `naplok/OLVASOI_KONKORDANCIA_zaras.md`; N-F76a, N-F76d, N-F76l, N-F76m, N-F76n).*

## 1. Cél

A #76-ban helyben (WSL) elkészült és a felhasználó által átnézett (M5, DT270) olvasói felület kerüljön a célszerverre (DT129 (1) a: KVM S VPS, 1 vCPU, 2 GB RAM, 20 GB NVMe), a telepítő szkriptből, HTTPS-sel, friss és a TSV-kkel egyező `pardes.db`-vel. A #76 K4–K6 VPS-oldali része itt teljesül; a nyilvános közzététel külön, feltételes megálló.

## 2. Hatókör

**Benne van**
- **Átvett feltételek a #76-ból:**
  - **K6 (DT-F76r):** a `pardes.db` friss építése a main TSV-iből és a teljes tesztfutás (`python eszkozok/teszt_futtat.py`), miután a #120 a `sqlite_epit.py` `kezi_mt_or` őrének okát (N-F117a) megszüntette. A #76 zárásakor a futás 8 fájlból 6 zöld volt, a régi (2026-10-14-i) építés miatt.
  - **K4 (D5):** a frissességi teszt (a `meta` hashek egyeznek a TSV-kkel) a telepítés feltétele; az N-F76m TSK-eltérése itt rendeződik.
  - **K5 (DT221):** a mérvadó lapidő-mérés az éles szerveren; a bemelegítés (N-F76n).
- **Telepítés:** a `telepit.sh` futtatása SSH-n át, fordított proxy (Caddy vagy nginx, N-F76d), HTTPS, szolgáltatásként indítás.
- **Javítás a saját hatókörben:** N-F76l (a Károli-KH tartomány vége, a TIPNR ismétlődő sor; `blokkok.py`), a vers-panel két mechanikus eltérése a pilothoz képest.
- **Mérlegelés:** a Supabase mint 4. tárhely-opció (N-F76a). A mért `pardes.db` 938–970 MB, ez nagyobb a csonk 30–60 MB-os becslésénél, ezért az ingyenes keretre épülő érvet újra kell mérlegelni.

**Nincs benne**
- A felület átépítése (#134, OLVASO_ALAPNEZET). [javaslat: az M0 döntse el, hogy a telepítés a #134 előtti vagy utáni felületet viszi-e ki.]
- Az N-F76b (Playwright-próba) és az N-F76c (Semgrep CI-lépés): elhalasztva (a felhasználó 2026-10-18-i döntése). [javaslat: a nyilvános közzététel (M5) előtt újra mérlegelendő.]
- A hozzáférési szintek valódi szétválasztása, belépés és fizetés (#86).

## 3. Lépések

- **M0 — ⛔ terv.** Rögzíteni kell: a #120 utáni építés menetét; a #134 viszonyát; a proxy választását (Caddy vagy nginx); a tárhely-opciókat (N-F76a); a DB-szinkron módját a VPS-en (a helyi `indit.sh` a fő checkout `pardes.db`-jét szinkronizálja `epites_ts` szerint).
- **M1 — építés és tesztek helyben.** A friss `pardes.db` a #120 után; a frissességi teszt (K4); a teljes tesztfutás (K6); az N-F76l javítása.
- **M2 — ⛔ VPS.** A KVM S VPS megrendelése a felhasználóé; a telepítés a szkriptből SSH-n át, HTTPS.
- **M3 — mérés az éles szerveren.** A vers-lap, a szó-lap és a keresés ideje; a bemelegítés (N-F76n); jelentés proveniencia-sorral.
- **M4 — ⛔ éles próbaüzem.** A felhasználó átnézi; az észrevételek a jelentésbe kerülnek.
- **M5 — ⛔ nyilvános közzététel.** Csak akkor, ha teljesül: #89 (LICENSE, a saját adat licence), DT126 (a GPL-es KJV-fájl sorsa), DT78 (17) (idézési szabály és a saját réteg licence), valamint a DT-M6 szerinti kiadási mód; a kiadási kapcsoló (DT124) `nyilvanos` módja.

## 4. Elfogadási feltételek

- **K1.** A szerveren a frissességi teszt zöld: a `meta` hashek egyeznek a TSV-kkel, a TSK-eltérés (N-F76m) megszűnt.
- **K2.** A teljes tesztkészlet zöld a friss építésen (a #76 K6-ja, DT-F76r).
- **K3.** Az adatbázis a böngészőbe nem kerül ki (`/pardes.db` → 404 a szerveren is); HTTPS.
- **K4.** A mérvadó K5-mérés az éles szerveren: a vers-lap ideje, és a magyar szóra keresés 100 ms alatt (#92 K5), vagy dokumentált eltérés döntéssel (DT221).
- **K5.** A nyilvános közzététel csak az M5 feltételeinek teljesülése után; addig a szerver a `belso` kiadást szolgálja ki, hozzáférés-korláttal. [javaslat]
- **K6.** CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

- DT-F76p (a #76 hatókör-szűkítése), DT-F76r (a K6 átadása), DT129, DT127, DT221, DT124, DT126, DT78 (17), DT270.
- Nyitott tételek: N-F76a, N-F76d, N-F76l, N-F76m, N-F76n; N-F76b/c (elhalasztva).
