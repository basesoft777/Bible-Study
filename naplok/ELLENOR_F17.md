# ELLENŐR — F17 (Macula-import), 3 kör, tömörítve

*Megjegyzés: a jelentésekben szereplő `DT6` azóta **DT7** (a #86 merge-e után a #85 kapta a DT6-ot).*

Ág: `claude/macula-import`, base `origin/main` (4525a63). Ellenőr: `fuggetlen-ellenor`; a jelentés az orkesztrátor által mentett tömörítés (az ellenőrnek nincs írási eszköze).

**1. kör — ELTÉRÉS 7:** (1) a KK `igehely_kjv` mezőjét a kód nem használta (KEZI sorok), ~2570 héber sor rossz Károli-verssel `rendben` állapotban (4Móz 13, Jób 39–40, Préd); (2) a 87 hely napló-indoklása („azonos számozás”) hamis, az F06-egyezés közös módszerhiba; (3) 169 081 Strong-illeszthetetlen sor `allapot=rendben`; (4) Strong-csapda 3 sorban (H1886 = Dothan) és `tobbes` sorokban; (5) a szerepmátrix 11. sora sérti a SEMA 2.13-at; (6) `ir:` hiányos; (7) DT6 forma.
**Javítás (F17.4):** KEZI `igehely_kjv`; a 87 hely 39 → 38 LXX-megfelelő (3 sor tér el az F06-tól, naplózva); `allapot=javaslat` Strong-illeszthetetlenségnél; Strong-szabály számcsaládra; szerepmátrix-sorok visszavonva; `ir:`; DT6 (a)–(h).

**2. kör — ELTÉRÉS 5:** Dán 4 rossz `kk_kjv` kötés (KJV≠MT, 947 sor); Jób 39:1–3 és 4Móz 13:1 rossz terkep-kötés; Préd 2:26 többes raw; `datasetek.tsv` +8 sor és szerepmátrix-bejegyzés (SEMA-ütközés, dokumentált, DT6 (f)).
**Javítás (F17.5):** fejezetenkénti KJV=MT igazolás (`naplok/F17_kezi_fejezetek.tsv`), Dán 4 `javaslat`; tekintély-szabály; interpoláció (40 Károli-vers, `javaslat`); több-raw kezelés.

**3. kör — ELTÉRÉS 6:** Préd 5 / 4Móz 30 identitás-kötése egy verssel elcsúszott (hamis `javaslat`-érték); a DT6 (c) és a napló okmegosztása pontatlan; a tekintély-szabály 0-szor futott le; a napló KK-számai nem partíciók (23 065 vs. 23 053); `kezi_fejezetek` oszlop-szemantika; M6 (dokumentált).
**Javítás (F17.6):** eltolódás-gyanús identitás üres értékre (44 Károli-vers, `javaslat:terkep_egyik_sem_eltolodas_gyanu`), partíció = 23 053, okmegosztás (242 Károli nélküli MT-vers: 154 EGYIK_SEM, 34 Dán 4, 54 KJV-osztály), oszlopok átnevezve. Az orkesztrátor összevetette: a partíció összege 23 053, a `Macula_heber.tsv` 475 911 adatsor, `feladatok.py ellenoriz` 0 hiba, E2–E16 0 találat; `lekerdez.py karoli` mintákkal (Dán 4:1) egyezik. A 4. kör nem futott (a javítás dokumentációs/számolási, az előző kör minden tartalmi kötést igazolt).

**Nyitva (felhasználói döntés, DT6):** a Dán 4 kezelése (a Károli Dán 3–4 szövege MT-számozású: identitás), az interpoláció `rendben`-né emelése, `datasetek.tsv` +8 sor és a Macula-szerep felvétele (SEMA 2.13/2.6), a héber fájl mérete (65 051 446 bájt, ~62 MiB; az F17.9-ben 39 könyvfájlra bontva), UBS-mezők (F24).
**Nem ellenőrizhető:** a külső Macula `LICENSE.md` sorai; az interpolált láncolt sorok (Jób 37–38, Préd 2:1, 9:1–2, 9:21–23, 12:1–2) sor-szintű igazolása, a 4. kör hiánya.
