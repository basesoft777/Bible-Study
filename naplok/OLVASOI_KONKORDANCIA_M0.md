# OLVASOI_KONKORDANCIA — M0 terv (#76)

*Csak olvas: a terv semmit nem telepít, nem tölt le, nem épít újra. A „javaslat” jelölésű tételek javaslatok; a döntés a felhasználóé (DT146). Modell: `claude-sonnet-5-5`. Állapot: **M0 jóváhagyva (felhasználó, chat, 2026-10-14); DT146 eldöntve.** A szöveg a döntések szerint átvezetve.*

Mért adatok forrása, ahol nincs más jelölés: `scope=pardes.db (a fő munkamásolat, 938 287 104 bájt), csak olvasás (mode=ro) | forras=meta.epites_ts=2026-10-13T18:10:45Z, 73 hash-sor; EXPLAIN QUERY PLAN és egyszeri időmérés, Windows, Python 3.14 | ts=2026-10-14`. Az időértékek tájékoztatók (nem a VPS-korlátokkal mért); a mérés az M4-é.

## 0. Összefoglaló

- Szerveroldali Flask-alkalmazás (Jinja2, automatikus escape), amely a `pardes.db`-t csak olvasásra nyitja; a böngésző csak a kért lap HTML-jét kapja.
- Három nézet (Olvasópult, Interlineáris, Munkaasztal) ugyanabból a blokk-regiszterből; a nézet sütiben és `?nezet=` paraméterben él; JavaScript nélkül is működik (a szó-lap és a vers részletei külön, állandó című lap).
- 39 blokk a #60 pilot `BLOKKOK` listájából; mindegyik regiszter-bejegyzés: jelleg, tábla(k), `tabla_licenc` kulcs, minimális hozzáférési szint, kiadási kizárás. A jelleg- és licencsor a regiszterből generálódik, így nem maradhat ki.
- Hozzáférés és kiadás konfigurációból (TOML). Az SQLite-kapcsolat `set_authorizer`-rel megtiltja a kiadásból kizárt táblák olvasását, tehát a kizárás nem csak a megjelenítésen múlik.
- Döntések (DT146, eldöntve 2026-10-14, 6. szakasz): Flask; szótő-keresés alapja alak ∪ szótári alak ((c) mód kapcsolóval); frázis-keresés a `token_karoli`-ból; süti csak nézetváltáskor; korlát a disztribúción belül `systemd-run`-nal; helyben a teljes `pardes.db`, a nyilvános célgépen szűrt példány.
- Öt eltérés/változás a briefhez képest (1. szakasz): kettő a felhasználóval egyeztetett (E1, E2), három a repó mai állapotából vagy a mért adatból következik (E3–E5).

## 1. Egyeztetett eltérések a brieftől, és a brief óta változott tények

| # | Brief | M0 | Ok |
|---|---|---|---|
| E1 | Python 3.11 (2. szakasz „Technika”, K6, tesztek) | **Python 3.12**, uv-vel rögzítve; a VPS-en ugyanez | A felhasználóval egyeztetve (l. 2. szakasz (b)). |
| E2 | külön disztribúció helye `D:\WSL\pardes` (4. szakasz M1, 3. szakasz) | **`E:\WSL\pardes`** | A felhasználóval egyeztetve. Mért: C: szabad 1,9 GB, D: 1806 GB, E: 640,2 GB (`Get-PSDrive`, 2026-10-14); `E:\WSL` még nem létezik. |
| E3 | „A keresés a pontos szóalakra és a Strong-számra megy, szótő-keresés, ha a szótő-oszlop addig elkészül” (2. szakasz, M3) | **A szótő-oszlop elkészült (#95 lezárva, PR #337):** `szotari_alak` 66 824 sor, `szotari_kereso` 72 720 sor, `szotari_token_kotojeles` 4 750 sor; az M3 tehát szótő-keresést is épít (3.6) | A `F95_SZOTOVEZES_DB_BRIEF.md` fejléc (`allapot: lezarva`, `lezarva_osszegzes`) és a `pardes.db` táblalistája. A #95 K-adata: a (c) mód gyakori lemmákon 173–874 ms; a lapozást a #76 kezeli (a #95 briefje szerint). |
| E4 | „héber frázis a `frazis_pozicio`-ból” (3. szakasz) | **frázis-keresés a `token_karoli`-ból** (`oldal='hu'`/`'er'`, `szo_kis`, egymást követő `sorszam`); a `frazis_pozicio` a Strong-sorozatos kereséshez marad | Mért (3.6): a `frazis_pozicio` nem rendelkezik szó-indexszel (`SCAN a`, 247 ms a „a föld” párra); a héber oldalán a `szo` pontozott alak (pl. `אָ֗רֶץ`), a `sorszam` hézagos (1:2-ben a 2. hiányzik); a `token_karoli.szo_kis` mássalhangzós alak, indexelt (`ix_token_karoli_2`), a „a föld” pár 27 ms. |
| E5 | `ir`: csak `eszkozok/olvaso_szerver/` és `naplok/` | változatlan; a `pardes.db` építőjét (`sqlite_epit.py`) a #76 nem módosítja | l. 3.6 és a 6. szakasz 3. pontja. |

## 2. Egyeztetett környezeti döntések (a felhasználóval, ide rögzítve)

**(a) Helyi környezet.** Külön WSL-disztribúció: neve `pardes`, kiadása `Ubuntu-24.04`, helye `E:\WSL\pardes`. A telepítés az **M1**-é, a felhasználó jóváhagyásával; az M0-ban semmit nem telepítettem és nem töltöttem le. A felhasználó meglévő `Ubuntu` disztribúciója (WSL2, jelenleg fut; `wsl -l -v`, 2026-10-14) érintetlen marad. Következmény az M1/M4-re: **a `.wslconfig` globális** (minden disztribúcióra érvényes), ezért az erőforrás-korlát (1 vCPU, 2 GB) nem a `.wslconfig`-ban, hanem a disztribúción belül, a processz szintjén állítandó be (6. szakasz, D-F76c/5). A megbízott disztribúció a **saját ext4 lemezén** tartja a `pardes.db`-t (nem a `/mnt/c`, `/mnt/e` DrvFs-en: ott lassú az SQLite és a fájlzárolás).

**(b) Python 3.12, uv-val rögzítve.** Az Ubuntu 24.04 alap Pythonja 3.12. A projekt gyökerében `.python-version` (3.12) és zárolt függőségek (`pyproject.toml` + `uv.lock`); a VPS-en ugyanez a telepítő szkriptből. A szótövező aranyminta-teszt (hibrid v2, 99,1% súlyozva; `D:\pardes_szoto\ATADAS.md` 3. szakasz) az M1-ben fut a 3.12-n; **eltérés esetén visszalépés 3.11-re** (a hfst Python-kötés kompatibilitása 3.12-vel nem ellenőrzött). A szótövezés kimenete (a `szotari_alak` tábla) kész adat a `pardes.db`-ben; a szerver a hfst-et **nem** használja futásidőben (csak olvassa a táblát), így a 3.11-re visszalépés a szerver kódját nem érinti. Az `.python-version` ezért az M1 aranyminta-teszt után véglegesedik. Az F79/F92/F95 építők és tesztjeik (`sqlite_epit.py`, `teszt_sqlite_epit.py`) Windowson 3.14-en futnak; **a 3.12-n való futásukat az M1 nem igazolta** (a ritka klónban nincs `konkordancia/`, a tesztek a TSV-kből építenek; a 389 MB letöltése nem volt jóváhagyva). Az építő nem szerveroldali eszköz: a szerver a kész `pardes.db`-t csak olvassa, a 3.12-re vonatkozó igazolás a szerver kódjára és a szótövező kimenetre (4.3/8. lépés) szól. Nyitott: az építő-tesztek 3.12-es futtatása (csak ha a `pardes.db`-t a disztribúcióban építenénk újra).

**(c) Keretrendszer: Flask** (DT146/1, a felhasználó döntése, 2026-10-14; indoklás: 5. szakasz).

## 3. Architektúra

### 3.1 Szerkezet (`eszkozok/olvaso_szerver/`)

```
eszkozok/olvaso_szerver/
  alkalmazas.py     Flask app-factory: útvonalak, süti, fejlécek; nem tartalmaz SQL-t
  adatbazis.py      csak-olvasó kapcsolat (mode=ro, query_only), authorizer, meta-frissesség
  blokkok.py        a 39 blokk regisztere: id, oldal, cím, jelleg, táblák, licenckulcs, szint, kiadási kizárás
  lekerdezesek.py   az összes SQL (paraméteres), blokkonként egy függvény
  oldalak.py        vers-lap, szó-lap, fejezet-lap, kereső-lap előállítása (HTML-szöveget ad; nem függ a Flasktól)
  kereses.py        keresési mód-szétválasztás, normalizálás (magyar, héber), lapozás
  frissesseg.py     a telepítés utáni épségi teszt (meta ↔ táblák ↔ manifest); `--manifest-keszit` az építés gépén (M1-ben kész)
  manifest_pardes_db.tsv  a pardes.db meta hash-sorainak másolata (a másolat-épséghez)
  pyproject.toml, uv.lock, .python-version   Python 3.12, zárolt függőségek (M1-ben kész)
  hozzaferes.py     szintek és blokk–szint hozzárendelés a konfigurációból
  gyorsitotar.py    LRU a kész lapokra + ETag
  konfig/szerver.toml, konfig/hozzaferes.toml
  sablonok/         Jinja2 (alap, olvasopult, interlinearis, munkaasztal, blokkok/*.html)
  statikus/         CSS, a kis JS (nézetváltó, Ctrl+K, szó-kattintás fragment)
  export.py         a statikus export egy paranccsal (oldalak.py-t hívja; az első kiadásban nincs kész, csak a váz)
  telepit.sh        a telepítő szkript (M1; WSL és VPS)
  teszt_*.py        unittest (a pilot is azt használja)
```

Az `oldalak.py` nem importálja a Flaskot: a lapelőállítás egy függvény (`vers_lap(igehely, nezet, szint, kiadas)` → HTML), ezért a statikus export később egy parancs (`export.py` bejárja a `vers` táblát és kiírja a fájlokat), és a tesztek szerver nélkül is futnak.

### 3.2 Útvonalak

Az igehely-azonosító az URL-ben ASCII-sített könyvkód (a `konyv` tábla `normalizalo_kod` oszlopából, pl. `1Móz` → `1Moz`; az egyediséget teszt őrzi, 66 könyv), fejezet, vers. Mindkét alak (`1Moz`, `1Móz`) elfogadott; a kanonikus cím az ASCII.

| Útvonal | Tartalom |
|---|---|
| `/` | kezdőlap: a Károli-szöveg, könyv–fejezet–vers választó, nézetváltó, keresődoboz |
| `/<konyv>` | a könyv fejezetlistája |
| `/<konyv>/<fej>` | a fejezet szövege (a választott nézetben), vers-kiemelés nélkül |
| `/<konyv>/<fej>/<vers>` | ugyanaz a fejezet, a vers kijelölve, a vers részletei nyitva |
| `/szo/<strong>` | szó-lap (`H0216`, `G1504`; a bemenet `^[HG][0-9]{1,4}[A-Za-z]?$`, normalizálva négy számjegyre; ismeretlen → 404) |
| `/kereses?strong=…` · `?szo=…` · `?frazis=…` · `?heber=…` | keresés; az eredmény lapozott verslista (3.6) |
| `/nezet/<nev>?vissza=<út>` | a nézet beállítása (süti), átirányítás; a `vissza` csak `/`-rel kezdődő, `//`-t és `:`-ot nem tartalmazó belső út lehet |
| `/r/szo/<strong>` · `/r/vers/<konyv>/<fej>/<vers>` | csak a blokkok HTML-töredéke (a fejléc/lábléc nélkül), a szó-kattintás és a verslista-kattintás tölti be `fetch`-csel; JS nélkül a hivatkozás a teljes lapra visz |
| `/statusz` | `meta.epites_ts`, kiadás, hash-egyezés (K4), szerver-verzió; nincs adat-tartalom |
| `/robots.txt` | első kiadásban: `Disallow: /` (próbaüzem, M7 előtt) |

A kéréskezelő egyetlen helyen fordít igehely-kulcsot (a `vers.igehely` formátuma `1Móz 1:4`); egyéb bemenetet nem fűz SQL-be.

### 3.3 A három nézet

Ugyanaz a blokk-regiszter és ugyanaz az adat, három elrendezés (Jinja2 sablon); a nézet nem módosít tartalmat.

| Nézet | Elrendezés | Mi kerül hova |
|---|---|---|
| **Olvasópult** (alap) | bal: a fejezet folyamatos Károli-szövege, kattintható szavak; jobb: „Szó” és „Vers részletei” fül | a szó-kattintás a `/r/szo/…` töredéket tölti a jobb oldali „Szó” fülbe; a vers-szám kattintása a „Vers részletei” fülbe |
| **Interlineáris** | versenként minden magyar szó alatt a párosított eredeti szó és Strong-szám; mellette a szó-lap | az illesztés a `token_par.hu_sorszam` / `er_sorszam` pozíció szerint, **nem** Strong-szám szerint (a pilot sorrendi illesztése ismétlődő szónál téveszthet, brief 2. szakasz); a párosítatlan eredeti szavak (a `token_eredeti` szavai, amelyek `er_sorszam`-a nem szerepel a `token_par`-ban) a vers alatt külön sorban |
| **Munkaasztal** | verslista, szöveg, és egyszerre nyitva a szó-lap és a vers részletei; Ctrl+K gyorsugrás | a Ctrl+K a `/` kereső dobozára fókuszál / könyv–fejezet–vers beírás (pl. `1Moz 1:4`) az 3.2 útvonalra ugrik; nincs külön szerveroldali logika |

**Megjegyzés és váltás.** A választás a `pardes_nezet` sütiben él (`olvaso` | `interlinearis` | `munkaasztal`; `SameSite=Lax`, `HttpOnly`, 1 év; személyes adatot nem hordoz), a `?nezet=` paraméter felülírja. Az ismeretlen érték az alapra esik vissza. A gyorsítótár kulcsa tartalmazza a nézetet (3.8). A nézetváltó sima hivatkozás (`/nezet/…`), JS nélkül is működik. **Döntés (DT146/4): a süti csak nézetváltáskor jön létre**; első látogatáskor és böngészéskor nem állítunk be sütit (süti nélkül az alap, az Olvasópult érvényes).

**Kattinthatóság.** Az első kiadásban a pilot szabálya érvényes: kattintható a fő héber szóhoz kötött Károli-szó (a pilot: 58,8% az 1Móz 1–25-ben; `naplok/OLVASOI_PILOT_ertekeles.md` 8.1). A nyelvtani elemhez kötött 24,8% szó-lapjának kérdése felületi döntés (pilot 8.4/5); nem része az M0-nak, nyitott megjegyzés (6. szakasz, 8).

### 3.4 A 39 blokk (a pilot `db_meres.py` `BLOKKOK` listájából)

A blokk regiszter-sora: id · oldal · jelleg · `pardes.db` táblák. A **jelleg** a pilot README-jének szabálya szerint van kitöltve (forrásadat / gépi feldolgozás / modell-kimenet); az M2-ben a pilot `adat.py`/`sablon.html` tényleges jellegcímkéivel veti össze egy teszt, és eltérésnél a pilot a mérvadó. *Javasolt kitöltés, a pilot-kód nem olvasva soronként.*

| # | Blokk | Oldal | Jelleg | Táblák |
|---|---|---|---|---|
| 1 | Károli-szöveg | vers | forrásadat | `vers` |
| 2 | Károli–Strong párosítás (aláhúzás) | vers | modell-kimenet | `token_par` |
| 3 | héber szavak (TAHOT) | vers | forrásadat | `token_eredeti` |
| 4 | igealak-kód, szófaj (Macula) | vers | forrásadat | `token_macula` |
| 5 | héber–görög párosítás szavanként (Macula) | vers | forrásadat | `token_macula` |
| 6 | görög szóalak és LXX-vers szavai (LXX_OS) | vers | forrásadat | `lxx_token` |
| 7 | LXX-versszám | vers | gépi feldolgozás | `lxx_versszam` |
| 8 | versszámozás (MT / KJV) | vers | gépi feldolgozás | `vers_szamozas` |
| 9 | angol szavak szavanként (BSB; KJV+Strong) | vers | forrásadat | `bsb`; `kjv` (**GPL, kiadási kizárás**) |
| 10 | Nave-témák (versekre bontva) | vers | gépi feldolgozás | `nave_vers` |
| 11 | TIPNR (személy- és helynevek) | vers | gépi feldolgozás | `tipnr` |
| 12 | igealak magyar feloldása | vers | gépi feldolgozás | `morf_kulcs_heber` (+ `token_macula`) |
| 13 | LXX-döntés, kapcsolat, motívum (adatréteg-sorok) | vers | forrásadat (soronként saját proveniencia-mező) | `lxx_dontesek`, `kapcsolatok`, `motivumok` |
| 14 | TSK-kereszthivatkozás | vers | forrásadat | `tsk` |
| 15 | Károli-kereszthivatkozás | vers | forrásadat | `kh` |
| 16 | UBS-jelentés az előfordulásra | vers | forrásadat | `ubs_dbh_referenciak`, `ubs_dbh_jelentesek` |
| 17 | Strong-szótár (szótő, kiejtés, szófaj, rövid jelentés) | szó (héber) | forrásadat | `strong_szotar` |
| 18 | előfordulás, könyvek száma | szó (héber) | gépi feldolgozás | `token_strong` |
| 19 | Károli-alakok és bizonyosság | szó (héber) | modell-kimenet | `token_par` |
| 20 | BDB angol szócikk (és alias) | szó (héber) | forrásadat (az alias: gépi feldolgozás) | `bdb`, `bdb_alias` |
| 21 | BDB magyar fordítás | szó (héber) | modell-kimenet | `forditasok` |
| 22 | görög megfelelő (lxx_bridge) | szó (héber) | forrásadat | `lxx_bridge` |
| 23 | szemantikai domén (SDBH) | szó (héber) | forrásadat (CC BY-SA) | `sdbh_domenek` |
| 24 | SECE-szócikk (héber) | szó (héber) | forrásadat | `sece_h` |
| 25 | OSHL (lexikális index, BDB-helyek) | szó (héber) | forrásadat | `oshl_lexikalis_index`, `oshl_bdb_igehelyek` |
| 26 | TBESH | szó (héber) | forrásadat | `tbesh` |
| 27 | tW-szócikk | szó (héber) | forrásadat (CC BY-SA) | `tw_szocikkek` |
| 28 | nyelvtani Strong-számok szűrése (nincs lap) | szó (héber) | gépi feldolgozás | `grammatikai_strongok` |
| 29 | TBESG | szó (görög) | forrásadat | `tbesg` |
| 30 | Thayer (angol) | szó (görög) | forrásadat | `thayer` |
| 31 | magyar jelentés (Thayer, UBS DNTG) | szó (görög) | modell-kimenet | `forditasok` |
| 32 | ÚSZ-előfordulás és versek | szó (görög) | gépi feldolgozás | `token_strong`, `vers` |
| 33 | héber háttér | szó (görög) | forrásadat | `lxx_bridge` |
| 34 | szemantikai domén (SDGNT) | szó (görög) | forrásadat (CC BY-SA) | `sdgnt_domenek` |
| 35 | SECE-szócikk (görög) | szó (görög) | forrásadat | `sece_g` |
| 36 | LSJ | szó (görög) | forrásadat (CC BY-SA) | `lsj` |
| 37 | MCGED | szó (görög) | forrásadat (**nem kereskedelmi**) | `mcged` |
| 38 | UBS DNTG jelentés | szó (görög) | forrásadat (CC BY-SA) | `ubs_dntg_jelentesek`, `ubs_dntg_referenciak` |
| 39 | tW-szócikk (görög) | szó (görög) | forrásadat (CC BY-SA) | `tw_szocikkek` |

A `pardes.db` ma mind a 39 blokk táblájával rendelkezik (a Macula, LXX_OS, nave_vers, bdb_alias táblák az #92 óta). **Forrás- és licencsor minden blokk alatt (N-F33b, K3):** a regiszter `licenckulcs` mezője a `tabla_licenc` (74 sor: `tabla`, `licenc_allapot`, `kereskedelmi`, `licenc_dataset`, `cimke`) és a `licencek` (51 sor) táblára mutat; a sablon a blokk alá a `licenc_dataset`, a `cimke` és a `licenc_allapot` értékét írja, továbbá a „share-alike”/„nem kereskedelmi”/„tisztázatlan” jelzést a tábla jelzései alapján. **Teszt:** minden renderelt blokk tartalmaz jelleg-címkét és forrás+licencsort; hiány hibát dob (N-F76b elvi része).

### 3.5 Kiadási kapcsoló és hozzáférési szintek

**Kiadás** (`konfig/szerver.toml`: `kiadas = "belso" | "nyilvanos" | "kereskedelmi"`, környezeti változó `PARDES_KIADAS` felülírhatja; alap: `belso`). A pilot `--kiadas` szabálya a szerveren: `nyilvanos` — a KJV-Strong blokk (9. blokk KJV fele, `kjv` tábla; GPL, DT124/DT126) kimarad; `kereskedelmi` — a KJV-Strong és az MCGED (37. blokk, `mcged`) is kimarad.
- A regiszterben a blokk `kiadas_kizar = ["nyilvanos","kereskedelmi"]` (KJV) illetve `["kereskedelmi"]` (MCGED) mezőt kap.
- **Kemény zár:** az `adatbazis.py` a kapcsolatra `sqlite3.set_authorizer`-t állít: ha a kiadás kizárja a táblát, `SQLITE_DENY`-t ad a `SQLITE_READ`-re. Ha a keresés vagy egy új blokk véletlenül lekérdezné (pl. „Strong → KJV-szavak”), a lekérdezés hibával áll meg, nem szivárog. Teszt: mindhárom kiadásra végigfuttat egy lapkészletet, és igazolja, hogy a kizárt táblákra nem történt olvasási kísérlet (az authorizer-napló üres), és a blokkok a HTML-ben nincsenek.
- A kiadás a lap lábjában és a `/statusz`-ban látszik. A licenc-állapot a „?” súgóban marad (ahogy a pilotban).

**Hozzáférési szintek** (`konfig/hozzaferes.toml`; a kódban csak a mechanizmus van):

```toml
# szintek: növekvő sorrend; a szint neve szabad
szintek = ["nyilvanos", "regisztralt", "kutato"]
alapertelmezett_szint = "kutato"      # az első kiadásban mindenki mindent lát (DT129 (3))

[blokk]                                # blokk-id → legkisebb szint, amely látja
"vers.karoli" = "nyilvanos"
# "szo.bdb_magyar" = "regisztralt"     # példa a későbbi szétválasztásra; ma nincs kitöltve
default = "nyilvanos"                  # ami a listában nincs: ez a szint
```

- Az `hozzaferes.py` egyetlen belépési pontja `szint(kerés) -> int`; az első kiadásban az `alapertelmezett_szint`-et adja (belépés nincs). Később ezt cseréli le a bejelentkezés, a blokk-szűrő változatlan marad.
- **Biztonsági irány:** ha a blokk-id nem szerepel a regiszterben vagy a konfigurációban hibás/hiányzik, a blokk **a legmagasabb szintre** esik (nem a legalacsonyabbra); az indulás hibaüzenettel áll meg ismeretlen szintnévnél.
- A szűrés a **lapelőállításnál** történik (a blokk nem kerül a HTML-be), nem CSS-sel; a blokkot nem látó szint a blokk lekérdezését sem futtatja (a blokk függvénye nem hívódik). A szint része a gyorsítótár-kulcsnak (3.8).
- A tartalmi szétválasztás és a DT-M6 viszonya külön döntés (nincs az M0-ban).

### 3.6 Lekérdezések SQL-terve

Minden lekérdezés paraméteres (`?`); az egyetlen dinamikus elem a `LIMIT`/`OFFSET` (egész, ellenőrzött) és a rendezés (fix lista). Az SQL kizárólag a `lekerdezesek.py`-ban áll. A kapcsolat: `file:…?mode=ro` URI, `PRAGMA query_only=ON`, `PRAGMA mmap_size` a RAM-keretnek megfelelően (6. szakasz, 5), kérésenként új kurzor, szálanként egy kapcsolat.

**Vers-lap** (`:ig` = pl. `1Móz 1:4`):

| Blokk | SQL (váz) | Index (mért terv) |
|---|---|---|
| Károli-szöveg | `SELECT karoli_szoveg, konyv, fejezet, vers, sorrend FROM vers WHERE igehely=?` | `SEARCH vers USING INDEX ix_vers_0`; 0,2 ms |
| Szavak + párosítás | `SELECT tk.sorszam, tk.szo, tp.er_sorszam, tp.er_szo, tp.strong, tp.bizonyossag FROM token_karoli tk LEFT JOIN token_par tp ON tp.igehely=tk.igehely AND tp.hu_sorszam=tk.sorszam WHERE tk.igehely=? AND tk.oldal='hu' ORDER BY tk.sorszam` | `ix_token_karoli_0`, `ix_token_par_2`; 0,9 ms (1Móz 1:4, 17 sor) |
| Héber szavak (TAHOT) | `SELECT … FROM token_eredeti WHERE igehely=? ORDER BY sorszam` | `ix_token_eredeti_*` |
| TSK, kh, nave_vers, tipnr, bsb, kjv, ubs_*_referenciak, lxx_*, vers_szamozas, kapcsolatok, lxx_dontesek | `… WHERE igehely=?` (illetve `forras_igehely`, `karoli_igehely`) | a pilot `db_meres.py` D1 listája szerint mind indexelt igehely-kulccsal (D3: vers-lap 93 ms medián, p95 161 ms a pilotban) |
| Strong-szintű vers-adatok | a vers `token_strong`/`token_par` Strongjaira egy `IN (…)` (a darabszám ≤ 100, paraméter-lánc) | `ix_token_strong_1` |

**Szó-lap** (`:s` = pl. `H0216`): egy-egy `WHERE strong=:s` a 17–27, 29–39. blokk táblájára (`strong_szotar`, `bdb`/`bdb_alias`, `forditasok`, `lxx_bridge`, `sdbh_domenek`, `sece_h`, `oshl_*`, `tbesh`, `tw_szocikkek`, ill. görögre a megfelelők); előfordulás: `SELECT COUNT(*), COUNT(DISTINCT konyv) FROM token_strong JOIN vers …`; Károli-alakok: `SELECT hu_szo_kis, COUNT(*) FROM token_par WHERE strong=? GROUP BY hu_szo_kis ORDER BY 2 DESC` (`ix_token_par_0`). A pilot D3: szó-lap 3,4–5,4 ms.

**Fejezet-lap:** `SELECT igehely, vers, karoli_szoveg FROM vers WHERE konyv=? AND fejezet=? ORDER BY vers`; a kattintható szavak a fejezet szavaira egy lekérdezés (`token_karoli LEFT JOIN token_par … WHERE igehely IN (a fejezet versei)`, a fő héber szó választása a pilot szabálya szerint: `magas` bizonyosság, azon belül tartalmas szófaj; a `strong_szotar.szofaj` és a `grammatikai_strongok` alapján).

**Keresés** (a lapozás **kulcsos**: `ORDER BY konyv.sorrend, vers.fejezet, vers.vers`, a következő oldal a legutolsó `(sorrend)` fölött; oldalanként 50 vers):

| Mód | Lekérdezés | Mért terv / idő (tájékoztató) |
|---|---|---|
| `strong=H0216` | `SELECT DISTINCT igehely FROM token_strong WHERE strong=?` → `vers` JOIN rendezés; mellette a Károli-alakok (`token_par`, 3.6 fent) | `ix_token_strong_0`; 110 sor 13 ms (a `DISTINCT` ideiglenes B-fát használ; az M2-ben `vers.sorrend`-re rendezve, `LIMIT 50`) |
| `szo=világosság` (pontos alak) | `SELECT igehely, sorszam FROM token_karoli WHERE szo_kis=? AND oldal='hu'` (kis/nagybetű-független: a bemenetet NFC + kisbetűsre hozza a `kereses.py`, ahogy az építő `szo_kis`-t számol) | `ix_token_karoli_2` vagy a részleges `ix_token_karoli_szo_hu`; 32 sor 0,5 ms (#92 K5: 9 ms) |
| `szo=…` mellé a Strong-lista | `SELECT strong, COUNT(*) FROM token_par WHERE hu_szo_kis=? GROUP BY strong ORDER BY 2 DESC` (ADATVAGYON_TERV 4. szakasz 2. pont) | `ix_token_par_3` |
| szótő (a): alak ∪ szótári alak | `SELECT a.alak FROM szotari_kereso k JOIN szotari_alak a ON a.alak=k.alak WHERE k.keresoalak=?` → az `alak`-ok tokenjei a `token_karoli`-ban (`szo` = `alak`, pontos alak, kis/nagybetű érzékeny; kötőjeles alakot a `szotari_token_kotojeles` fedi) | `szotari_kereso` / `ux_szotari_alak_alak`: covering, 22 sor 0,2 ms |
| szótő (c): + a lemma Strong-ága | az (a) tokenjeinek fő Strongjai (`token_par`), majd ezek összes tokenje | #95 mérés: gyakori lemmákon 173–874 ms; **lapozva és `LIMIT`-tel**; a Strong-ág csak kérésre (6. szakasz, 2) |
| `frazis=a föld pusztává` (2–4 magyar szó) | önillesztés a `token_karoli`-n: `a.szo_kis=? AND b.szo_kis=? AND b.oldal='hu' AND b.sorszam=a.sorszam+1 [AND c…]` | `ix_token_karoli_2` covering; „a föld”: 404 sor 27 ms; ritka pár („kietlen és”): 3 sor 1,7 ms |
| `heber=בראשית ברא` (héber frázis) | ugyanaz `oldal='er'`-re, a bemenetet a `kereses.py` mássalhangzós alakra hozza (a niqqud- és ékezet-jelek U+0591–U+05C7 törlése, végbetűk egységesítése — a `szo_kis` az építőben ugyanígy készül; a pontos szabályt az M3 az építő kódjából veszi át, hogy a két oldal egyezzen) | `ix_token_karoli_2`; a TAHOT a prefixumokat külön tokenként tartja (`ב` + `ראשית`, mért: `token_karoli` 1Móz 1:1): egy „בראשית” beírt szó nem egyezik egyetlen tokennel. **M3-hoz:** előtag-toleráns illesztés (a H9001–H9009 stb. előtag-tokenek átugrása) vagy Strong-sorozatos illesztés (`token_strong`/`frazis_pozicio` `strong` indexe) |
| `strong=H1254+H0430` (két Strong egy versben, ADATVAGYON 4. pont) | `SELECT igehely FROM token_strong a JOIN token_strong b ON b.igehely=a.igehely WHERE a.strong=? AND b.strong=?` | `ix_token_strong_0` |

A mért szám a pardes.db-n, hideg Windows-gyorsítótárral nem mérendő pontosan; az M4 a VPS-t utánzó korlátokkal méri a K5-öt (vers-lap, szó-lap, magyar szó < 100 ms).

**A #76 nyitott bemenete a `NYITOTT_FELADATOK.md`-ből (nem döntések, az M2/M3 figyelembe veszi):** **N-F94f** (a különírt vonatkozó névmás: „a melyet”; az *amely*-re keresve az „a” token nem jelenik meg) és **N-F94d** (a hátravetett igekötő: *vettettek el*; az igekötős szótári alakra keresve nem jön elő, csak az alapigére; rokon: N-F94a): a szótő-keresés ((a) és (c) mód) eredményét ez korlátozza, a felület ne ígérjen teljes körű találatot, és a súgó jelezze; **N-F92a** (a Nave-bontás két példánya): a #76 kiolvasója az `eszkozok/nave_bontas.py` közös modult használja, a pilot-példány (`olvaso_pilot/bovites.py`) a #76-ban megszűnik; addig a `teszt_olvaso_pilot.py` D2-egyezési tesztje őrzi az azonosságot.

**M3-ellenőrzés (DT146/3):** az önillesztés `igehely`-egyezést követel, tehát a frázis nem lóg át versen; az M3 igazolja a vershatárt, külön a Károli-versösszevonásos helyeken (9 hely, `f22/versosszevonas.tsv`), ahol két TAHOT-vers áll egy Károli-versen. 

**A `frazis_pozicio` indexe (E4/E5, DT146/3).** A `frazis_pozicio`-nak a `strong` és az (`igehely`,`oldal`,`sorszam`) indexén kívül nincs szó-indexe (`EXPLAIN`: `SCAN a`). A fenti `token_karoli`-alapú frázis-keresés ezt megkerüli, tehát **a tervhez új index nem kell**; a `frazis_pozicio` a Strong-sorozatos keresésben marad. Nincs `sqlite_epit.py`-módosítás.

### 3.7 Biztonság (N-F76c elő)

- **SQL-injekció:** a bemenet sosem kerül a SQL szövegébe; a `lekerdezesek.py` kizárólag paraméterezett utasításokat tartalmaz; a rendezés/limit fix listából. A Semgrep-szabály (N-F76c) a `lekerdezesek.py` kivételével tilt minden `.execute(` hívást és minden f-stringes/`%`-os SQL-összefűzést.
- **XSS:** Jinja2 autoescape bekapcsolva minden sablonra; `|safe` csak a regiszterből jövő, előre elkészített (tesztelt) töredékekre; a forrásokból jövő szöveg (BDB, tW, SECE, LSJ stb.) mind escape-elt. Ha egy forrás jelölést tartalmaz (pl. a BDB-szeletelő gépi bontása), azt a szerveroldali kód állítja elő escape-elt elemekből, nem az adat HTML-je. Teszt: ismert hibás/`<script>`-os adatsor (a `tW_szocikkek.tsv` ismert U+FFFD cikke és egy szintetikus `<script>` érték) escape-elve jelenik meg.
- **Adatbázis nem megy ki:** nincs statikus fájl-kiszolgálás a db könyvtárából; a fordított proxy (Caddy) csak az alkalmazás portját és a `statikus/` könyvtárat tükrözi; nincs `.db`/`.tsv` kiszolgálás (teszt: `GET /pardes.db` → 404).
- **Átirányítás:** a `vissza` paraméter whitelist (3.2). **Fejlécek:** `Content-Security-Policy` (saját forrás, inline script nincs), `X-Content-Type-Options`, `Referrer-Policy`.
- **Naplózás:** a keresési kifejezés nem személyes adat, de az első kiadásban a napló nem rögzíti a lekérdezés szövegét (csak az útvonal-típust és az időt).

### 3.8 Gyorsítótár és frissesség

- **Lap-gyorsítótár:** korlátos LRU (alap: 512 lap vagy 64 MB, amelyik előbb betelik) a kész HTML-re; kulcs: `(útvonal, normalizált paraméterek, nézet, szint, kiadás, adatbázis-kulcs, sablon-verzió)`. Az `adatbazis-kulcs` a `meta.epites_ts` + a `meta` hash-sorok hash-e. Egy folyamat egy gyorsítótárat tart (a szerver 1–2 worker; a kimenet a worker-ek között nem megosztott, ez az 1 vCPU-nál nem baj).
- **HTTP:** `ETag` = a gyorsítótár-kulcs hash-e, `Cache-Control: no-cache` a próbaüzemben (belső), `public, max-age=300` a nyilvános módban; a Caddy `encode zstd gzip`.
- **Frissesség (K4), két külön igazolás:** (1) **másolat-épség** a célgépen: a `telepit.sh` lefuttatja a `frissesseg.py`-t: a `meta` `hash:<tábla>` sorait (73) összeveti az adatbázis tényleges tábláinak újraszámolt hash-ével és a telepítéshez adott `manifest_pardes_db.tsv`-vel. A manifest ugyanabból a `meta`-ból készül, tehát **ez nem frissességi bizonyíték**, csak azt mutatja, hogy a célgépre ugyanaz a példány került, és ép. (2) **TSV-frissesség** az építés gépén: a `eszkozok/olvaso_pilot/db_meres.py` D5-je (git-alapú: a forrás-TSV-k utolsó commitja az építés időpontja után van-e; a `meta` hash a tábla mai tartalmával). Ez a K4 tényleges feltétele; a telepítés (és az M5/M6) előtt le kell futtatni, és eltérésnél a `pardes.db`-t újra kell építeni. A `/statusz` az épségi eredményt és az `epites_ts`-t mutatja futás közben. A manifest a célgépre kerülő táblákat fedi (nyilvános célgépen a szűrt példány táblakészletét, 6. szakasz 6.).

## 4. Telepítő szkript és M1 (terv; nem fut le most)

**Az M1 jóváhagyva (felhasználó, chat, 2026-10-14) és lefutott; a mért eredmény a 4.3-ban áll.** A telepítő szkript az M2 elején készül el; a disztribúciót a felhasználó hozta létre. Az alábbi 4.1/4.2 az M1 előtti terv (a méretek becslések).

### 4.1 Mit tölt le a `wsl --install -d Ubuntu-24.04 --name pardes --location E:\WSL\pardes`

*Az alábbi méretek **becslések** (a mért értékek: 4.3); az M1 előtt nem voltak mérve (nem futott letöltés, a repó nem tartalmaz ilyen adatot). A parancs előfeltétele a `--name` és `--location` kapcsolókat ismerő WSL: `wsl --version` ellenőrzendő (a kapcsolók újabb, 2.4.x körüli WSL-kiadásban jelentek meg; ez emlékezetből való állítás, nem repó-tény).*

| Mit | Forrás | Becsült méret | Hova kerül |
|---|---|---|---|
| Ubuntu 24.04 WSL-lemezkép (rootfs) | a Microsoft által kiszolgált WSL disztribúciós lista (Canonical hivatalos Ubuntu 24.04 WSL-képe); a pontos URL a `wsl --list --online` / a parancs kimenete | letöltés ≈ 300–450 MB (becslés) | letöltési gyorsítótár, majd kibontva |
| A telepített disztribúció (`ext4.vhdx`) | kibontás a fenti képből | kezdetben ≈ 1,5–2,5 GB (becslés); a vhdx nő a használattal | `E:\WSL\pardes` (E: szabad 640,2 GB; `E:\WSL` még nem létezik, a parancs létrehozza) |
| WSL-frissítés, ha a telepített WSL a kapcsolókhoz régi | Microsoft | néhány tíz MB (becslés) | rendszer |

A meglévő `Ubuntu` disztribúciót a parancs nem érinti (külön név és hely). A C: szabad helye 1,9 GB: **semmi nem kerülhet C:-re** (a parancs `--location` miatt E:-re ír; az M1 ezt a parancs előtt újra ellenőrzi).

### 4.2 A telepítés utáni lépések (a disztribúcióban, a felhasználó jelszava után)

1. `wsl -d pardes` — első indítás, felhasználónév és jelszó megadása (a felhasználóé).
2. `/etc/wsl.conf`: `[boot] systemd=true`, majd a disztribúció újraindítása (`wsl --terminate pardes`) — **disztribúciónként** érvényes, a globális `.wslconfig`-hoz és a meglévő `Ubuntu`-hoz nem nyúlunk.
3. Ellenőrzés: `systemctl is-system-running`, a `cpuset` és `memory` cgroup-vezérlők elérhetősége (`cat /sys/fs/cgroup/cgroup.controllers`) — az erőforrás-korlát előfeltétele (6. szakasz 5.).
4. `sudo apt update && sudo apt install -y git curl sqlite3 ca-certificates` + a fordított proxy (Caddy vagy nginx; az M2 dönti el a konfigurációval) — becsült letöltés ≈ 100–250 MB (becslés).
5. `uv` telepítése (a hivatalos telepítő vagy a csomagkezelő; ≈ 20–40 MB, becslés); `python3 --version` = 3.12 (Ubuntu 24.04 alap).
6. A projekt-tároló klónozása a disztribúció saját lemezére (`~/pardes/`), **nem** `/mnt`-re; `uv sync` (zárolt függőségek: Flask, Jinja2, Werkzeug, gunicorn és tranzitívjaik; becslés < 50 MB PyPI-ról).
7. `pardes.db` + manifest másolása a disztribúció ext4 lemezére (≈ 0,94 GB, helyi példány: a teljes fájl, 6. szakasz 6.); másolat-épségi teszt (3.8; a TSV-frissesség külön: D5).
8. Az aranyminta-teszt (szótövezés) a 3.12-n; eltérésnél 3.11, az `.python-version` az eredménnyel rögzítődik (2. szakasz (b)).
9. Az erőforrás-korlátozott indítás kipróbálása: `systemd-run … -p MemoryMax=2G -p AllowedCPUs=0` (6. szakasz 5.), a gunicorn indítása, `GET /statusz`.
10. Az M1 zárása: napló a tényleges letöltött és lemezen foglalt méretekkel (proveniencia-sorral), a becslések cseréje mért értékre.

### 4.3 M1 zárónapló (2026-10-14; a becslések helyett mért értékek)

`scope=pardes WSL-disztribúció (Ubuntu 24.04.5 LTS, WSL2), E:\WSL\pardes; a 4.2 lépései | forras=a disztribúcióban futtatott parancsok kimenete (wsl -d pardes), D:\pardes_szoto\szoto\meres_harmadik*, a repó a608882b…fd4175b2 állapota | ts=2026-10-14`

| Lépés (4.2) | Eredmény |
|---|---|
| 1. első indítás | a felhasználó létrehozta a Linux-felhasználót (`basesoft`, uid 1000); a jelszót nem ismerem, rootként és `basesoft`-ként dolgoztam |
| 2. systemd | `/etc/wsl.conf` már tartalmazta a `[boot] systemd=true` sort (az új disztribúció alapja); **nem módosítottam**, `.wslconfig`-hoz és a meglévő `Ubuntu`-hoz nem nyúltam; `systemctl is-system-running` = `running` (systemd 255) |
| 3. cgroup | `cgroup2fs`; `cgroup.controllers` = cpuset cpu io memory hugetlb pids rdma. Az `systemd-run -p MemoryMax=2G -p AllowedCPUs=0` próba: `Cpus_allowed_list: 0`, `memory.max` = 2147483648, `cpuset.cpus` = 0, `nproc` = 1 (a disztribúció 8 CPU-t és 7 905 MB RAM-ot lát) |
| 4. apt | `git` és `ca-certificates` már megvolt; telepítve: `sqlite3` 3.45.1, `caddy` 2.6.2 (+ libnss3, libnspr4; 4 csomag frissült); **letöltés 14,5 MB, lemezfoglalás +46,1 MB**; a `caddy` szolgáltatás **letiltva és leállítva**; a Caddy előtelepítése a 4.2/4. lépés szerinti előkészítés, **nem döntés**: Caddy vagy nginx között az M2 dönt (nginx esetén a `caddy` csomag eltávolítandó) |
| 5. uv, Python | `uv` 0.13.1 a hivatalos telepítővel (a telepítő szkript 71 300 bájt; a bináris a `~/.local/bin` alatt 37 MB, `du -sb ~/.local` = 38,2 MB); Python **3.12.3** a rendszer csomagjából (`UV_PYTHON_DOWNLOADS=never`, interpreter-letöltés nem történt) |
| 6. klón, uv sync | `git clone --depth 1 --filter=blob:none --sparse --branch claude/olvasoi-konkordancia`, `sparse-checkout set eszkozok adat/szoto naplok`: munkamásolat 63 MB, `.git` 18 MB (a 389 MB-os `konkordancia/` **nem** töltődött le); `uv lock` + `uv sync --all-groups`: flask 3.1.3, gunicorn 26.2.0, simplemma 2.0.0 (dev, 18,1 MiB letöltés); `.venv` 25 MB; a `uv.lock` a repóban (F76.5) |
| 7. pardes.db | a fő munkamásolat `pardes.db`-je (938 287 104 bájt) a disztribúció ext4 lemezére (`~/pardes/pardes.db`), a másolás 15,1 s; **sha256 egyezik** (589e0422ef0731f4…) a forrással; **másolat-épségi teszt** (`eszkozok/olvaso_szerver/frissesseg.py`, manifest: `manifest_pardes_db.tsv`, 73 tábla): 73 tábla újraszámolt hash-e = `meta`, `meta` = manifest, **ÉP**, 33 s (`epites_ts=2026-10-13T18:10:45Z`). Ez másolat-épség, **nem a TSV-frissesség**: l. a K4-bekezdést alább |
| 8. szótövező aranyminta-teszt | Python **3.12.3** alatt a hibrid v2 a harmadik mintán (113 alak): **ossz 80% / 99,1% súlyozva (90/113)**, minden réteg és minden sor **azonos** a Windowson (3.14, simplemma 2.0.0) rögzített eredménnyel; a `meres_harmadik_reszlet.tsv` bájtra azonos (`cmp`); a bemenetek sha256-ja egyezik (hibrid.py `7ee1b6050740`, minta `c805d55133f4`, `karoli_lexikon.tsv` `75ad61617a88`). A kiadott út (C+K, simplemma nélkül): `szotari_alak_epit.py` 3.12-n újragenerálva: 66 824 sor, a törzs sha256-ja (a `#` fejlécsorok nélkül) **azonos** a repó `adat/szoto/karoli_szotari_alak.tsv`-jével (2313dcf488811696…). **Nincs eltérés a szótövező mintán, nincs visszalépés 3.11-re. A 3.12 az F79/F92/F95 építők és tesztek futtatása nélkül, csak erre az aranymintára (és a kiadott szótári alak-generátor bájtazonosságára) építve véglegesedett; az építők 3.12-es futása nem igazolt (2. szakasz (b)).** |
| 9. korlátozott indítás | `systemd-run --unit=pardes-proba -p User=basesoft -p MemoryMax=2G -p AllowedCPUs=0` + gunicorn (`gthread`, 1 worker, 4 szál) egy próba-Flask-alkalmazással (nem része a repónak): `GET /statusz` → HTTP 200, 6,1 ms, `cpus: 1`, `epites_ts` és a `meta` 73 hash-sora olvasható; a szolgáltatást leállítottam |
| 10. zárónapló | ez a szakasz |

**Mért méretek** (a 4.1 táblázat becsléseinek cseréje):

| Mit | Becslés | Mért |
|---|---|---|
| a rootfs letöltése | ≈ 300–450 MB | **nem mérhető utólag** (a letöltést a felhasználó indította; a WSL nem naplózza). A kicsomagolt, telepítés utáni `ext4.vhdx`: **1 455 423 488 bájt (1,36 GiB)** |
| `ext4.vhdx` most | 1,5–2,5 GB kezdetben | **2 931 818 496 bájt (2,73 GiB)** az M1 végén (+1,48 GB: pardes.db 0,94 GB, klón 0,08 GB, `uv`, `.venv`, csomagok, apt-gyorsítótár 131 MB) |
| apt | ≈ 100–250 MB | **14,5 MB letöltés**, +46,1 MB lemez |
| uv | ≈ 20–40 MB | **37 MB** a telepített bináris |
| Python-csomagok | < 50 MB | `.venv` **25 MB** (ebből a simplemma 18,1 MiB letöltés) |
| klón | — | 63 MB munkamásolat + 18 MB `.git` (ritka, blob-szűrt) |
| a disztribúció szabad helye | — | `/` 1,0 TB látszólagos, 954 GB szabad a gazda E: lemezén (E: szabad: 637,5 GB a végén); C: szabad 16,5 GB a végén (az M0 mérésekor 1,9 GB; C:-re a disztribúció nem ír) |

**K4 — TSV-frissesség (D5, Windows-oldalon futtatva, 2026-10-14):** a `db_meres.py` `frissesseg(con, True)` függvénye (hash-újraszámítással, 41 s). `scope=pardes.db (fő munkamásolat, epites_ts=2026-10-13T18:10:45Z, 73 hash-sor) | forras=eszkozok/olvaso_pilot/db_meres.py D5, a repó git-története | ts=2026-10-14`. **Eltérő táblák: `vers_szamozas`, `lxx_versszam`, `nave_vers`.** Ok: a forrás-TSV-k az építés után módosultak: `konkordancia/Karoli_versmegfeleltetes.tsv` (utolsó commit 2026-10-14T07:47+02:00, F91.10; a `nave_vers` és a `vers_szamozas` forrása), `konkordancia/LXX_versificacios_terkep.tsv` (2026-10-14T08:12+02:00, F91.12; az `lxx_versszam` forrása). A `pardes.db` tehát a #91 (feliratos zsoltárok számozása) javításai előtti állapot. **A K4 feltétele ma nem teljesül ezekre a táblákra; a `pardes.db` újraépítése szükséges az M5 előtt** (a #79 építője, `eszkozok/sqlite_epit.py`; ez nem a #76 `ir` mezője, ezért nem végeztem el, és a disztribúció példánya is a régi). Addig a Zsolt-lapok és a Nave/LXX-versszám blokkok a régi számozást mutatnák; az M2 D2-egyezési tesztje a Zsolt 22-re ezt jelezné. Döntés kell: ki, mikor és melyik ágon építteti újra az adatbázist.

**Ismert tudnivalók / nyitott pontok:**
- A `systemd=true` az új disztribúció alapja volt; ha a `wsl.conf` a jövőben változik, az érinti az erőforrás-korlát módszerét (DT146/5).
- A rootfs letöltési méretét nem tudtam utólag megállapítani; ha a felhasználó adata kell, a Windows `wsl --install` kimenetéből olvasható.
- A klón ritka (sparse): a `konkordancia/` és `adat/` többi része nincs a disztribúcióban; az M2 szerver a `pardes.db`-t használja, a TSV-k frissességét a Windows oldali `db_meres.py` D5 igazolja (3.8).
- A `~/probe/app.py` (próba) és a `~/szoto_arany/` (aranyminta-másolatok) a disztribúcióban maradt, a repón kívül; törölhetők.
- A Windows-oldali `pardes.db` és a distroban lévő példány azonos (sha256); a szerver M2-től a distro példányát használja.

## 5. Keretrendszer: Flask vagy FastAPI (indoklással)

| Szempont | Flask | FastAPI |
|---|---|---|
| Munka természete | szinkron SQLite-olvasás, szerveroldali HTML | az `async` előnye nem érvényesül: az `sqlite3` blokkol, szálkészlet kell hozzá |
| Függőségek | flask, jinja2, werkzeug, markupsafe, itsdangerous, click, blinker; kiszolgáló: gunicorn | fastapi, starlette, pydantic, uvicorn (+ jinja2); nagyobb futásidejű készlet |
| Sablonok / escape | Jinja2 beépített, autoescape alapból HTML-sablonokra | Jinja2 külön csatolva |
| Memória 2 GB-on | egy gunicorn worker (gthread) ~ 40–60 MB RSS (**becslés, nem mért**; az M4 méri); az SQLite oldalcache közös | hasonló; az uvicorn+pydantic többletet ad |
| Tesztelés | `app.test_client()` szerver nélkül | `TestClient` (httpx függőség) |
| Eddigi gyakorlat a repóban | — (nincs webes kód) | — |
| API-séma, validáció | nem kell (nincs JSON API, a paramétereket a `kereses.py` fix szabályai ellenőrzik) | automatikus dokumentáció, típus-ellenőrzés: itt feleslegesek |

**Javaslat: Flask** (a szinkron, egyszerű kérés–válasz modellre; kevesebb függőség, kisebb támadási felület; a lapelőállítás a Flasktól független `oldalak.py`-ban él, így a döntés bármikor visszafordítható). Kiszolgáló: gunicorn `--worker-class gthread --workers 1 --threads 4` az 1 vCPU-ra (az M4 méri, hogy 2 worker ad-e többet).

## 6. Döntésre váró pontok (DT146) és nyitott kérdések

**DT146 eldöntve (felhasználó, chat, 2026-10-14).** A döntések:

1. **Keretrendszer: Flask.**
2. **Szótő-keresés:** az alap az alak ∪ szótári alak ((a) mód); a Strong-ággal bővített (c) mód kapcsolóval. A felület mindkét módnál megmutatja, mit talált és milyen módon (a „tő” szótári alak, DT130).
3. **Frázis-keresés a `token_karoli`-ból.** Az M3 ellenőrzi a vershatárt (3.6).
4. **Nézet sütije: funkcionális `pardes_nezet`** (`SameSite=Lax`, `HttpOnly`, 1 év); **a süti csak nézetváltáskor jön létre** (3.3).
5. **Erőforrás-korlát a disztribúción belül, `systemd-run` módszerrel:** `-p MemoryMax=2G -p AllowedCPUs=0` (1 vCPU, 2 GB), `prlimit` nélkül; globális `.wslconfig` nincs. Előfeltétel: `systemd=true` a disztribúció `wsl.conf`-jában és elérhető `cpuset`/`memory` cgroup-vezérlő (4.2/3. lépés; az M1 ellenőrzi). Az M4 jelentése rögzíti a tényleges módszert; a Windows-WSL2 mérés tájékoztató, a mérvadó az M6.
6. **Adatbázis:** helyben (WSL) a **teljes `pardes.db`**, a kiadás szerinti olvasási tiltással (authorizer). A **nyilvános célgépre (M6/M7) szűrt példány kerül, a telepítés előtt** előállítva (a kiadás által kizárt táblák nélkül: `nyilvanos` — `kjv`; `kereskedelmi` — `kjv`, `mcged`), a manifest ezt a táblakészletet fedi (3.8). A szűrő-lépés (`szur_peldany` jellegű parancs) az M6 előtti tétel; az authorizer a szűrt példányon is fennmarad (kettős védelem).

7. **Szótövezés és a `pardes.db` frissessége:** az `Ubuntu-24.04` disztribúción a hfst-et a szerver nem használja; a szótő-tábla kész. Nincs döntés, megjegyzés.
8. **Nyitott megjegyzés (nem akadály):** a nyelvtani elemhez kötött Károli-szavak (24,8%) szó-lapja; a pilot 8.4/5 kérdése. Az M0 az alapszabályt (pilot-szabály) viszi át.

**Nyitott kérdés, amelyet a terv nem old meg:** a Zsolt 22-ben a Károli–Strong párosítás 100%-ban „alacsony” bizonyosságú (pilot 8.1); az olvasói felület ezt jelöli (a „bizonyosság” megjelenik a 2. blokkban), a javítás nem a #76 dolga.

## 7. Tesztterv (M2–M4)

- **Lap- és útvonal-tesztek** (`app.test_client()`, szerver nélkül): `/`, fejezet, vers, szó (héber, görög), ismeretlen Strong → 404, ismeretlen könyv → 404, érvénytelen vers → 404.
- **Linkpróba (N-F76b):** a kezdőlapról bejárt minta (minden könyv első fejezete + a pilot két szakasza + a szó-lapok) — nincs törött belső link, nincs 5xx; ismert kérdésre (pl. `szo=világosság`) a találat nem üres; hiányzó forrás-/licencsor egy blokk alatt hiba.
- **D2-egyezés a #60 pilottal:** az 1Móz 1–25 (693 vers) és a Zsolt 22 (32 vers) vers- és szó-lapjainak blokk-adata a pilot `adat.py` JSON-jával (a `db_meres.py` D2 módszerével) — a #92 óta ismert eltérések (ÚSZ-láncelemek, elfogadva) listázva; K1: a többi blokkban 0 eltérés.
- **Hozzáférési szintek:** egy blokk szintje 2-re állítva, a kérés szintje 1 → a blokk a HTML-ben nincs, a lekérdezése nem fut (hívásszámláló); a szint a gyorsítótár-kulcsban van (a szint-1 lap nem szolgálható szint-2-nek és fordítva).
- **Kiadási kapcsoló:** `belso`/`nyilvanos`/`kereskedelmi` kiadásra a KJV-Strong és az MCGED blokk jelenléte/hiánya; az authorizer-napló üres a kizárt táblákra.
- **Nézetek:** a három nézet ugyanazokat a blokk-id-ket tartalmazza; a süti és a `?nezet=` kezelése; a `vissza` whitelist.
- **SQL-injekció és XSS (N-F76c):** `strong='; DROP…`, `szo=%`, `<script>` a keresésben és az adatban; a Semgrep CI-lépés a `lekerdezesek.py` kivételével tilt minden összefűzött SQL-t.
- **Frissesség (K4):** a `meta` hash-ek egyeznek a manifesttel; szándékosan megváltoztatott sor esetén a teszt elbukik.
- **Futtatás:** Python 3.12 alatt (uv); ha az aranyminta-teszt miatt 3.11-re lépünk vissza, mindkettőn.
- **CI:** a `teszt_*.py` fájlok a szokásos módon; a CI a repó adatbázisa nélkül a `pardes.db`-t igénylő teszteket kihagyja (jelezve), ahogy a pilot tesztjei teszik.

## 8. Mérés (M4) és az elfogadás megfeleltetése

| Elfogadás | M0-beli megvalósítás |
|---|---|
| K1 | lapok és keresés csak a `pardes.db`-ből; D2-egyezés a pilot két szakaszán (7. szakasz) |
| K2 | három nézet, süti, kezdőlap a bibliaszöveg választóval (3.2–3.3) |
| K3 | blokkregiszter jelleggel és licencsorral, hozzáférési konfig, kiadási kapcsoló + authorizer (3.4–3.5) |
| K4 | nincs db-kiszolgálás, `mode=ro`, `query_only`; a másolat-épségi teszt és az építés gépén a D5 (TSV-frissesség) a telepítés feltétele (3.7–3.8); a D5 ma 3 táblára eltér, a K4 nyitott (4.3) |
| K5 | M4: vers-lap, szó-lap, keresés idő a korlátozott környezetben; magyar szóra keresés < 100 ms (a tájékoztató mérés 0,5 ms) |
| K6 | tesztek 3.12 (szükség esetén 3.11) alatt, CI, független ellenőr |

Mérési módszer (M4): 20+ vers-lap (a két pilot-szakasz véletlen mintája), 20+ szó-lap, az 3.6 keresési módok (a gyakori szavakkal is), hideg és meleg, medián és p95; a pilot referenciaértéke 93 ms (vers-lap), 3–5 ms (szó-lap). Az eredmény `naplok/OLVASOI_KONKORDANCIA_meres.md`, proveniencia-sorral. A mérés Windows-WSL2 környezetben csak tájékoztató; a VPS-en (M6) ismétlődik.

## 9. Mi nincs az M0-ban (a brief szerint)

A szótő-keresés ismert korlátai (N-F94a/d/f) és a Nave-bontás közös modulja (N-F92a) a 3.6 szerint nyitott bemenetek, nem az M0 hatóköre.

Motívumréteg (#25b), új adat, modernizált Károli (DT128), belépés/fizetés, a hozzáférési szintek tartalmi szétválasztása, a szótő-oszlop előállítása. A frázis-keresés előtag-toleranciája az M3 része (3.6), nem külön feladat.

## 10. Állapot

**M0 jóváhagyva (felhasználó, chat, 2026-10-14); DT146 eldöntve. M1 lefutott a `pardes` disztribúcióban (4.3 zárónapló): a környezet kész, az aranyminta-teszt eltérés nélkül lefutott a 3.12-n, a másolat-épségi teszt zöld (a TSV-frissesség a K4 szerint nem igazolt).** Következő: M2 (az alkalmazás), a brief szerint.

**M1: megállás a K4-nél (E1 NYITOTT, nem javított).** A frissesség **nem igazolt**: a D5 lefutott, de három táblára eltérést talált. A `frissesseg.py` csak másolat-épséget igazol. **Nyitott:** a K4 TSV-frissesség (D5) három táblára eltér (4.3), a `pardes.db` újraépítése az M5 előtt szükséges; az építő-tesztek 3.12-es futtatása nem igazolt (2. szakasz (b)).
