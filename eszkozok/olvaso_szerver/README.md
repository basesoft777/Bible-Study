# Olvasói szerver (#76 OLVASOI_KONKORDANCIA, M2–M3)

Szerveroldali Flask-alkalmazás, amely a `pardes.db`-ből (csak olvasásra) állítja elő a Károli-bibliaszöveg lapjait, három váltható nézettel. Terv: `naplok/OLVASOI_KONKORDANCIA_M0.md`; zárónapló: ugyanott 4.4, és `naplok/OLVASOI_KONKORDANCIA_zaras.md`.

## Szerkezet

| Fájl | Szerep |
|---|---|
| `alkalmazas.py` | Flask-gyár: útvonalak, süti, fejlécek, gyorsítótár/ETag; SQL nincs benne |
| `oldalak.py` | a lapelőállítás (HTML-szöveg), **nem függ a Flasktól**; a statikus export erre épül |
| `blokkok.py` | a blokk-regiszter (46 azonosító: az M2 40-e a pilot 39 mért adatblokkjára + az M2b 6 új blokkja a pilot kirajzolt készletéhez), jelleg-címke, forrás- és licencsor |
| `lekerdezesek.py` | az összes SQL, paraméterezve (N-F76c) |
| `kereses.py` | a keresés (M3): a bemenet értelmezése és normalizálása, a négy ág (Strong, magyar szó három móddal, magyar frázis, héber frázis), a héber előtag-toleráns illesztés, a kulcsos lapozás, a kiemelés; Flask és SQL nélkül |
| `adatbazis.py` | csak olvasó kapcsolat, `set_authorizer` a kiadás szerint kizárt táblákra |
| `hozzaferes.py` | hozzáférési szintek a `konfig/hozzaferes.toml`-ból |
| `gyorsitotar.py` | korlátos LRU a kész lapokra |
| `konfig/` | `szerver.toml` (kiadás, süti, gyorsítótár), `hozzaferes.toml`, `arculat.json` (az arculati token-fájl, #98), `elemek.toml` (az elem-regiszter és a kizárt osztályok, #98 M2) |
| `arculat.py` | a token-fájl betöltése és ellenőrzése, a token-blokk (`:root`, sötét téma) előállítása; a szerver a `/arculat.css?v=<hash>` címen adja (#98 M1, DT157) |
| `tervezo.py`, `tervezo_statikus/` | a tervező mód (#98 M2): a regiszter betöltése, a stíluslap szabálytérképe, a mentés értékszűrése, a mentési végpont; a kliens (`tervezo.js`, `tervezo.css`) a `/tervezo/…` címen, **csak a `belso` kiadásban** |
| `regiszter_or.py` | a regiszter-őr: a sablonok és a blokkok `class="…"` osztályai és a kliens (`olvaso.js`, `tervezo.js`) `classList.add/toggle/remove` literál-osztályai a regiszterben vagy a kizárt listán (`python regiszter_or.py`) |
| `arculat_szinkron.py` | a design system `tokens.json`-ja a token-fájlból (`--kimenet`, `--alap`; feltöltés nélkül) |
| `sablonok/`, `statikus/` | Jinja2 (autoescape), CSS, kis JS (nincs inline script/stílus: CSP); az `olvaso.css` token-értéket nem ismétel, csak `var(--…)`-hivatkozást |
| `gunicorn_conf.py`, `telepit.sh` | indítás (gthread, 1 worker, 4 szál), környezet, frissességi teszt |
| `frissesseg.py`, `manifest_pardes_db.tsv` | az épségi teszt (K4), M1 |
| `export.py` | statikus export váza |
| `indit.sh` | a közös indító (#100): régi példány leállítása, adatbázis-szinkron, szerver újratöltővel; a három asztali parancsikon ezt hívja |
| `allapot.py` | az indító és a lábléc állapota (#100): szinkron-döntés (`meta.epites_ts`), ág és commit (fájlolvasással, `git` nélkül), lábléc-figyelmeztetések; stdlib |
| `teszt_indito.py` | az indító tesztjei (#100): szinkron-döntés, git-olvasás, lábléc, `indit.sh` ideiglenes adatbázisokkal |
| `teszt_olvaso_szerver.py` | tesztek (unittest) |
| `teszt_kereses.py` | a keresés tesztjei (M3): értelmezés, független lekérdezéssel összevetett találatok, vershatár, üres eredmény, lapozás, SQL-injekció, XSS, a fejléc mezője minden nézetben, kiadás (authorizer-napló), hozzáférési szint |
| `teszt_arculat.py` | a token-fájl, a token-blokk és az `/arculat.css` tesztjei (#98 M1) |
| `teszt_tervezo.py` | a tervező mód tesztjei (#98 M2): regiszter, regiszter-őr, szabálytérkép, értékszűrés, a végpont biztonsága kiadásonként, atomi írás, ETag, szinkron-kimenet, a szelektorok a valódi lapokon |
| `teszt_pilot_aranymintaval.py` | a kirajzolt blokk-készlet összevetése a #60 pilot aranymintájával (írásjeles szöveg, számlálók, szócsempék, „Ebben a versben”, Nave, blokk-címek); a döntések (DT148–i) tesztjei, az Interlineáris csempék |

## Útvonalak

`/` kezdőlap · `/<könyv>` · `/<könyv>/<fejezet>` · `/<könyv>/<fejezet>/<vers>` · `/szo/<H0216|G1504>` · `/kereses?q=…` (`tipus`, `mod`) vagy `?strong=` · `?szo=` (`mod=pontos|szoto|szoto_strong`) · `?frazis=` · `?heber=` (`tol`: lapozás) · `/nezet/<olvaso|interlinearis|munkaasztal>?vissza=` · `/ugras?q=` · `/r/szo/<strong>`, `/r/vers/…` (töredékek) · `/arculat.css?v=<hash>` (a token-blokk) · `/statusz` · `/robots.txt`. A könyvkód ASCII-sített (`1Moz`). `.db`/`.tsv` nincs kiszolgálva.

Csak a `belso` kiadásban (más kiadásban 404): `/tervezo/tervezo.js`, `/tervezo/tervezo.css`, `/tervezo/terkep.json` (a regiszter és a szabálytérkép), `/tervezo/kod` (egyszeri kód, csak helyi kérésre), `POST /tervezo/mentes`, `POST /tervezo/visszaallit`.

## Tervező mód (#98 M2)

A `belso` kiadásban a fejlécben, a szintváltó mellett a **Tervező** kapcsoló. Bekapcsolva a rámutatott elem keretet és címkét kap (a regiszterbeli magyar nevével; a regiszteren kívüli elem szaggatott keretet és „nem regisztrált elem” címkét), a kattintás nem navigál, hanem kiválaszt. A panel csak a kiválasztott elem regiszterbeli tulajdonságait mutatja (csúszka a méretekre, színválasztó és paletta a színekre; a szín a látott témában állítódik), és kiírja, hány szabályban és hány elemen hat a token a lapon. Minden állítás azonnal látszik (a `:root` CSS-változói, csak ebben a böngészőben); a változáslista egyenként és egészben visszavonható, és lapváltáskor megmarad (sessionStorage). A regisztrálatlan elem tokenjei gépi névvel állíthatók (előnézet), mellettük egy másolható `elemek.toml`-részlet.

**Küldés a szerverre:** a változások a `konfig/arculat.json`-ba íródnak (rendezett, determinisztikus JSON → kis git-diff); a szerver újraindítás nélkül az új arculattal adja a lapokat (új `arculat.css?v=` hash, új ETag, ürített lap-gyorsítótár). Az előző állapot a `konfig/arculat.json.elozo`-ban (git-ignorált); az **Előző mentés vissza** gomb ezt állítja vissza. A commitot a végrehajtó vagy a felhasználó készíti, nem a szerver.

**A mentés feltételei:** csak `belso` kiadás; csak helyi kérés (a forrás 127.0.0.1/::1, nincs `X-Forwarded-For`/`Forwarded`/`X-Real-IP` fejléc, a `Host` és az `Origin` helyi); csak `POST`; egyszeri kód a `GET /tervezo/kod`-ról (`X-Tervezo-Kod` fejléc); csak a regiszterben valamely elemhez rendelt token, érvényes értékkel (szín: `#rgb`, `#rrggbb`, `rgb()`, `hsl()`; betűméret px 8–64, rem/em 0.5–4; térköz px 0–128, rem/em 0–8 (DT158); lekerekítés px 0–999; sorköz 1.0–2.4); a betűcsalád nem írható. Hiba: 403 (helyi kérés/kód), 400 (érték; a lemezes token-fájlban nem létező token is), 415 (nem JSON), 500 (a lemezes token-fájl nem érvényes, külön üzenettel); a fájl ilyenkor változatlan. A token létezését a mentés a lemezes fájl szerint vizsgálja, mert arra ír. A CSP nem lazul (`script-src 'self'`, `style-src 'self'`). Fordított proxy mögött a feltétel csak akkor tartja távol a távoli kérést, ha a proxy továbbító fejlécet ad (`X-Forwarded-For`/`Forwarded`/`X-Real-IP`) vagy a külső `Host`-ot továbbítja: így a Caddy alapbeállítása. Az nginx alapbeállítása (`proxy_pass http://127.0.0.1:8000`, `proxy_set_header` nélkül) egyiket sem teszi: a kérés loopbackről, továbbító fejléc nélkül és `Host: 127.0.0.1:8000`-rel érkezik, így egy távoli, `Origin`/`Sec-Fetch-Site` nélküli kérés (pl. `curl`) átmegy a feltételen (a `GET /tervezo/kod` kódot ad, a `POST /tervezo/mentes` ír). A `belso` kiadást ezért proxy mögé csak továbbító fejlécet adó konfigurációval szabad tenni; a kérdés nyitott (DT159, a proxy-választás: N-F76d; az ellenőri napló: `naplok/ELLENOR_TERVEZO_MOD.md`). több workerrel futtatva a mentés csak az egyik worker arculatát töltené újra, ezért a tervező mód az egy workeres fejlesztői vagy gunicorn-indításhoz való.

**Regiszter-őr:** új CSS-osztály csak regisztrálva (`[[elem]]`) vagy indokkal kizárva (`[kizart]`) kerülhet a felületre: `python regiszter_or.py` (és a `teszt_tervezo.py`). Az őr a sablonok `class="…"` attribútumait, a `blokkok.py`/`oldalak.py` `class="…"`-literáljait és a kliens `classList.add/toggle/remove` literál-argumentumait olvassa; a nem olvasható alak (egyszeres idézőjeles vagy idézőjel nélküli `class=`, összefűzéssel le nem zárt attribútum, a Jinja-kifejezés nem literál ága, `className =`, nem literál `classList`-argumentum) hiba, nem marad ki némán. Nem olvassa a tervező saját panelének osztályait (`tz-…`, a `tervezo.css`-ből) és a csak a stíluslapban szereplő osztályokat. **Szinkron:** `python arculat_szinkron.py --kimenet /tmp/tokens.json --alap <a design system mostani tokens.json-ja>`.

## Keresés (M3)

A fejléc mezője (minden nézetben; Ctrl+K) és a `/kereses` lap. A `q` mező a típust a bemenetből ismeri fel: igehely → ugrás; Strong-szám (legfeljebb három: a versek, amelyekben mind előfordul); héber betű → héber frázis; egy magyar szó → szó; több → frázis (2–4 szó). Az állandó cím a típusos alak (`/kereses?szo=föld`).

- **Magyar szó:** `pontos` (a szóalak, kis/nagybetű nélkül, a `szo_kis` szabálya); `szoto` — az alap (DT146/2): a pontos alak ∪ a szótári alak minden Károli-alakja (`szotari_kereso`, a kötőjeles alakok darabjaival); `szoto_strong` — a (c) mód: ehhez a találatok nem nyelvtani Strong-számaival párosított minden magyar szó. A lap kiírja, mit talált és hogyan (alakok, mezők, Strong-ág). Ismert korlát: N-F94f, N-F94d (a súgó jelzi).
- **Frázis:** a `token_karoli` egymást követő tokenjei egy Károli-versen belül (DT146/3, M0 E4); a héber frázisnál a beírt szó 1–4 egymást követő token összefűzése (a TAHOT az előtagokat külön tartja). A vershatár a Károli-vers határa; a 9 versösszevonásos Károli-versben (`f22/versosszevonas.tsv`) a héber frázis a belső (MT) vershatáron átléphet, mert a `pardes.db` ezt a határt nem tárolja (DT-F76j, nyitott).
- **Lefedettség:** a magyar szó- és frázis-keresés a Károli–Strong szótokeneken fut; a 9 párosítatlan ÚSZ-könyvben (Mt, Mk, Luk, Ján, ApCsel, Róm, 1–2Kor, Jel) nincs szótoken, ott nem talál (a lap kiírja). A Strong-keresés ott is talál, kiemelés nélkül.
- **Biztonság:** a bemenet csak a `kereses.ertelmez` normalizálásán át, paraméterként jut az SQL-be (az SQL a `lekerdezesek.py`-ban); a kimenet escape-elt; érvénytelen bemenet: 400, magyarázó üzenettel. A hozzáférési konfigban a `kereses.strong|szo|frazis|heber` azonosító szintet kaphat (zárt módban a lekérdezés nem fut); a (c) mód és a párosításos kiemelés a `vers.par` blokk láthatóságát követi.
- **Lapozás:** kulcsos (`tol` = `vers.sorrend`), 50 vers oldalanként. Mért idők: `naplok/OLVASOI_KONKORDANCIA_M3.md`.

## Indítás egy kattintással (#100)

A három asztali parancsikon (`PaRDeS olvaso - belso (tervezo).bat` → 8765, `… - nyilvanos.bat` → 8766, `… - kereskedelmi.bat` → 8768) a WSL `pardes` disztribúcióban az `indit.sh <kiadás> <port>`-ot hívja a főcheckoutból:

1. **Régi példány leállítása** a porton (`fuser -k -TERM`, 5 mp után KILL); a napló kiírja, futott-e régi példány.
2. **Adatbázis-szinkron.** A Windows-oldali `pardes.db` (forrás: `<repó>/pardes.db`) és a WSL-beli másolat (`~/pardes/pardes.db`) `meta.epites_ts` értékét hasonlítja össze (kis olvasás, a 938 MB-ot nem olvassa be; a kulcs NEM a fájl mtime-ja, mert a másolás azt átírja). Eltérés vagy hiányzó másolat → `MÁSOLÁS` ideiglenes névre (`pardes.db.uj.<pid>`), majd atomi átnevezés: a régi állományt még nyitva tartó példányok ép adatot látnak, hiba esetén a meglévő másolat érintetlen. Azonos építési idő → `NINCS másolás`. A napló mindig kiírja, melyik történt.
3. **Szerver újratöltővel:** `alkalmazas.py --ujratolt` (Werkzeug `stat`-mód: a `/mnt/c`-n az inotify nem működik). Figyelt fájlok: a betöltött Python-modulok (a szerver `.py` fájljai és a pilot `bdb_szelet.py`-ja) és az `extra_files`: `sablonok/`, `konfig/`, `statikus/`, a pilot `bdb_szelet.py`-ja. **Kivétel:** a `konfig/arculat.json` és az `.elozo`-ja, mert a tervező mód mentése futás közben írja, és újraindítás nélkül hat. Kódváltozás után a szerver legfeljebb pár másodperc alatt újraindul (a napló: `Detected change in … reloading`); az üresjárati terhelés ~1% egy magon (M0 felmérés 4.). Szintaxishibás szerverfájl mentése leállítja a szervert (az újratöltő gyereke import közben meghal): a javítás után a parancsikon újra indítja.

Két egymás utáni kattintás sorosítva fut (zárfájl `~/pardes/.indit.zar`, amíg a port meg nem nyílik): a végén pontosan egy példány fut a porton.

**Lábléc.** Minden lap alján a kiadás, az **ág**, a rövid **commit**, az **adatbázis építési ideje**; figyelmeztetés (`<mark>Figyelem:</mark>`), ha az ág nem `main`, ha az ág nem állapítható meg, vagy ha a Windows-oldali adatbázis újabb a futó másolatnál (az `indit.sh` a `PARDES_FORRAS_DB` környezeti változóval adja át a forrás útját; a lábléc 3 másodpercenként újraolvassa a git-állapotot és a forrás építési idejét, így az ágváltás és az adatbázis-újraépítés újraindítás nélkül is látszik; a kész lapok gyorsítótár-kulcsában a lábléc tartalma is benne van). Az ág és a commit a `.git/HEAD` és a ref-fájlok közvetlen olvasásából jön (worktree-ben is; a WSL-beli `git` a Windows-útra mutató `.git` fájlt nem oldja fel). A figyelmeztetés a másolat frissítéséhez a parancsikont kéri. A lábléc csak a már regisztrált `labjegyzet` osztályt használja (regiszter-őr: nincs új osztály); a statikus exportban a lábléc változatlan.

**Környezeti változók az `indit.sh`-ban** (alapérték elég az éles használathoz; a gépi próba ezekkel dolgozik): `PARDES_FORRAS_DB`, `PARDES_DB`, `PARDES_PY`, `PARDES_ZAR`, `PARDES_INDIT_CSAK_ELOKESZIT=1` (csak leállítás + szinkron).

**A három parancsikon változása (2026-10-15, a repón kívül, az asztalon).** Mindhárom `.bat`-ban két sor változott, a többi (köztük a böngésző megnyitása) változatlan; az eredeti fájlok a session mentésében vannak. (1) A `start "…" wsl -d pardes -e bash -lc "…"` sor mostantól az `indit.sh <kiadás> <port>`-ot hívja (**`-e bash -lc`, nem `-- bash -lc`**: a `--` mellett a WSL alapértelmezett shellje a `$S`-t üresre fejti ki, és az `indit.sh` el sem indul — M2.2, 2026-10-15); ha az `indit.sh` a főcheckoutban még nincs meg (a #100 mergelése előtt), a régi indítással fut tovább (a kiírt figyelmeztetéssel) — ez az átmeneti tartalék a merge után törölhető. (2) A `timeout /t 7` sor helyett a böngésző megnyitása előtt egy PowerShell-hurok vár a `/statusz` válaszára (60 próbálkozás, kérésenként `-TimeoutSec 15`, mert a hideg első `/statusz` 2,1 mp; a `.bat` kiírja, hogy az ablakot nem szabad bezárni), mert a másolás (~10 s) miatt a fix 7 másodperc kevés. A `.sh` fájlok sorvége a `.gitattributes`-ben `eol=lf` (CRLF-es munkafán a bash nem fut).

## Futtatás

```bash
# fejlesztés (Flask kell: uv sync az olvaso_szerver könyvtárban, Python 3.12)
PARDES_DB=/út/pardes.db python eszkozok/olvaso_szerver/alkalmazas.py --port 8765
# éles jellegű
PARDES_DB=/út/pardes.db ./telepit.sh ellenorzes && PARDES_DB=/út/pardes.db ./telepit.sh indit
# tesztek: EGYETLEN belépési pont (#100, DT160 (c)); Windowsról és WSL-ből is, a WSL venv-jét és a WSL-natív ~/pardes/pardes.db-t választja
python eszkozok/teszt_futtat.py            # mind (a lassú teszt_szintek.py-val); --gyors: nélküle; --fajl teszt_tervezo: egy fájl; --reszletes
# egy fájl kézzel (WSL venv): PARDES_DB=$HOME/pardes/pardes.db python eszkozok/olvaso_szerver/teszt_tervezo.py
```

**Tesztek és a `/mnt/c`.** A `teszt_futtat.py` kiírja, melyik adatbázist nyitotta meg, és figyelmeztet, ha az a `/mnt/c` alatt van: a WSL a véletlen (SQLite-lapos) hozzáférést a `/mnt/c`-ről nagyon lassan olvassa (a `teszt_olvaso_szerver.py` 45+ perc a natív ~2 perc helyett). A kód és a `konkordancia/` a `/mnt/c`-ről olvasódik (nincs másolat). Mért idők: `naplok/OLVASO_INDITO_M1_merés.md`.

Kiadás: `PARDES_KIADAS=belso|nyilvanos|kereskedelmi` (vagy `konfig/szerver.toml`). Nyilvános kiadásban a KJV-Strong blokk, kereskedelmiben az MCGED is kimarad; az adatbázis-kapcsolat ezeket a táblákat olvasni sem engedi.

## Hozzáférési szintek és a szintváltó (F76.34)

A szintek és a blokk–szint hozzárendelés a `konfig/hozzaferes.toml`-ban vannak (éles: mindenki `kutato`). A fejléc **szintváltója** (`/szint/<nev>`, funkcionális süti `pardes_szint`, SameSite=Lax, HttpOnly, csak váltáskor jön létre) a próbaüzemhez van, a felhasználó kérésére (2026-10-14); **csak a `belso` kiadásban** jelenik meg és hat. `nyilvanos` és `kereskedelmi` kiadásban sem a vezérlő, sem a süti, sem a `?szint=` paraméter nem emelheti a szintet. A szint része a gyorsítótár-kulcsnak és az ETag-nek.

A `konfig/hozzaferes_proba.toml` a **tesztek** próba-konfigja; az éles szerver nem tölti be. A próba-konfig a MECHANIZMUST próbálja. A `kutato` szinthez kötött blokkok: a `forditasok`-ból olvasók (`szo.bdb_magyar`, `szo.bdb_apparatus`, `szo.magyar_gorog`), továbbá a Thayer, TBESH, TBESG, LSJ, UBS_DNTG szótárakhoz tartozó blokkok (`szo.thayer`, `szo.tbesh`, `szo.tbesg`, `szo.lsj`, `szo.ubs_dntg`), amelyek az eredeti angol forrástáblákat olvassák, nem a `forditasok`-at. NEM követi pontosan a DT-F86c fordítás-listáját: a DT-F86c szerint a BY-SA-eredetű tartalom (pl. UBS_DNTG) nem zárható, a próba mégis zárja, mert csak a szűrést próbálja. **Ez a #86 freemium/prémium határát nem dönti el**, csak a mechanizmust próbálja (`teszt_szintek.py`, a két pilot-szakasz valódi lapjain).
