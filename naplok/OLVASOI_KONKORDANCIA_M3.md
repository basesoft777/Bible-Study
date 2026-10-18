# OLVASOI_KONKORDANCIA — M3 (keresés) jelentése (#76)

*Végrehajtó modell: `claude-opus-5-5` (a brief `modell: opus`). Ág: `claude/olvasoi-konkordancia-m3` (az origin/main 89b30c2e-ről). Commitok: F76.42–F76.46. Állapot: az M3 kész; **független ellenőrzés még nem volt**. A saját mérések tájékoztatók (nem a VPS-t utánzó korlátokkal); a K5 mérvadó mérése az M4-é.*

## 1. Mit valósít meg

A fejléc mezője minden nézetben (Olvasópult, Interlineáris, Munkaasztal; Ctrl+K) és a `/kereses` lap. A `q` mező a típust a bemenetből ismeri fel (igehely → átirányítás a vers-lapra; Strong-szám; héber betű → héber frázis; egy magyar szó → szó; több → frázis); az állandó cím a típusos alak (`?strong=`, `?szo=` + `mod`, `?frazis=`, `?heber=`; `tol`: kulcsos lapozás, 50 vers).

| Ág | Forrás a `pardes.db`-ben | Megjegyzés |
|---|---|---|
| Strong-szám (1–3; több: a versek, amelyekben mind előfordul) | `token_strong`; kiemelés: `token_par` | a 9 párosítatlan ÚSZ-könyvben is talál, kiemelés nélkül (a lap kiírja) |
| magyar szó, `pontos` | `token_karoli.szo_kis` (fedő index) | kis/nagybetű-független; a `szo_kis` szabálya az építőével azonos (teszt: tárolt értékkel összevetve) |
| magyar szó, `szoto` (**alap**, DT146/2) | a pontos alak ∪ `szotari_kereso` → `token_karoli.szo` (F95 kulcs) ∪ `szotari_token_kotojeles` | a lap kiírja: a pontos előfordulások száma, a szótári alak mezői, a Károli-alakok és számuk; ha a beírt alak nem szótári alak, javaslat a szótári alakra (*földet → föld*) |
| magyar szó, `szoto_strong` ((c) mód, kapcsoló) | + a találatok `token_par`-beli nem nyelvtani Strong-számaival párosított minden magyar szó (F95 M0 6.) | a Strong-ág listája a lapon; zárt `vers.par` mellett nem fut, figyelmeztetéssel |
| magyar frázis (2–4 szó) | `token_karoli` önillesztés, egymást követő `sorszam`, azonos `igehely` (DT146/3, M0 E4) | a kötőjel szóhatár (a token-bontás szerint) |
| héber frázis (1–4 szó) | `token_karoli` héber oldala (`szo_kis`, mássalhangzós) | a beírt szó 1–4 egymást követő token összefűzése (az előtag a TAHOT-ban külön token): *בראשית*, *בְּרֵאשִׁית*, *ב ראשית* ugyanazt adja |

**Eltérés a brief szövegétől (egyeztetett):** a brief 3. szakasza „héber frázis a `frazis_pozicio`-ból”; az M0 E4 és a DT146 (3) (felhasználó, 2026-10-14) szerint a frázis-keresés a `token_karoli`-ból megy, mert a `frazis_pozicio` héber oldala hézagos (csak a párosított pozíciók) és nincs szó-indexe. Az M3 ezt követi.

**Jelölés és biztonság.** Minden találatlista fölött jelleg-címke és forrás- és licencsor (`blokkok.KERESES`, a blokkok szabályával; hiányzó licencsor indulási hiba). Az SQL csak a `lekerdezesek.py`-ban áll, paraméterezve; a frázis-sablon szövege csak a szavak számától (2–4) függ. A kimenet escape-elt (Jinja2 autoescape; a kiemelés `Markup`-pal, escape-elt részekből). Érvénytelen bemenet: 400, magyarázó üzenettel. Üres eredmény: „Nincs találat”, 0 vers. A keresési módok azonosítói (`kereses.strong|szo|frazis|heber`) a hozzáférési konfigban szintet kaphatnak; zárt módban a lekérdezés nem fut. A párosításból jövő adat (kiemelés, Strong-lista, (c) mód, a Strong-keresés Károli-alakjai) a `vers.par` láthatóságát követi. A keresés kiadási kizárású táblát nem olvas (teszt: üres authorizer-napló mindhárom kiadásban).

**Lefedettség.** A magyar szó- és frázis-keresés a Károli–Strong szótokeneken fut; a 9 párosítatlan ÚSZ-könyvben (Mt, Mk, Luk, Ján, ApCsel, Róm, 1Kor, 2Kor, Jel) nincs szótoken, ott nem talál (F95 M0 5. szakasz; a lista adatból, a lap és a súgó kiírja). A szótári alakos keresés korlátai (N-F94f, N-F94d) a súgóban.

## 2. Tesztek

`eszkozok/olvaso_szerver/teszt_kereses.py`, 33 teszt: értelmezés és hibás bemenet; a `szo_kis` egyezése a tárolt értékkel mindkét oldalon (3000–3000 minta); ismert kérdések független lekérdezéssel (szó pontos / szótári alak / mai alak / (c) mód; frázis; Strong; két Strong; héber frázis három bemeneti alakban); vershatár (1Móz 1:1|1:2, magyar és héber); üres eredmény; lapozás; SQL-injekció (a `vers` sorszáma változatlan; `%` és `_` nem helyettesítő); XSS (öt alak); forrás- és licencsor, jelleg; a találati linkek a vers-lapra mennek (200); a fejléc mezője mindhárom nézetben a `/kereses`-re küld; kiadásonként üres authorizer-napló; hozzáférési szint (zárt mód: a lekérdezés nem fut; zárt `vers.par`: nincs kiemelés, nincs párosítás-adat).

**Teljes futás** (`python eszkozok/teszt_futtat.py`, a lassú `teszt_szintek.py`-val; WSL `pardes`, Python 3.12.3, `~/pardes/pardes.db`, `epites_ts` 2026-10-18T12:18:16Z; 2026-10-18): `teszt_arculat` 22 OK · `teszt_bdb_vers_jelentes` 26-ból 1 FAIL (`test_bajtra_azonos`; az M3-tól független, l. 6. szakasz) · `teszt_indito` 39 OK · `teszt_kereses` 33 OK · `teszt_olvaso_szerver` 73 OK · `teszt_pilot_aranymintaval` 22 OK · `teszt_szintek` 13 OK · `teszt_tervezo` 48 OK. Fájlszinten 7 zöld, 1 piros; tesztszinten 276 OK, 1 FAIL.

## 3. Vershatár (M0 3.6, DT146/3)

- **A Károli-vers határa:** a frázis nem lép át (az önillesztés azonos `igehely`-t követel; a héber illesztés versenként fut). Teszt: *földet a föld* (1Móz 1:1 vége + 1:2 eleje) és *הארץ והארץ* nem adja az 1Móz 1:1-et.
- **A 9 versösszevonásos Károli-vers** (`f22/versosszevonas.tsv`): a magyar oldalon a Károli-vers egy vers, a frázis ott helyesen a versen belül marad. A héber oldalon két TAHOT-vers tokenjei folytatott sorszámmal állnak egy Károli-versen, és a `pardes.db` a belső (MT) vershatárt nem tárolja. Mérve: a határon álló héber szópárra keresve **mind a 9 helyen** van találat, tehát ott a héber frázis átlép az MT-vershatáron.

| Károli-vers | beolvasztott TAHOT-vers | határ (er-sorszám) | szópár | a Károli-vers a találatok közt |
|---|---|---|---|---|
| 4Móz 29:39 | 4Móz 30:1 | 30\|31 | כֶֽם וַ | igen (összes: 419) |
| Ézs 9:20 | Ézs 9:20 | 18\|19 | יֹאכֵֽלוּ מְנַשֶּׁ֣ה | igen (1) |
| Ézs 64:1 | Ézs 64:2 | 9\|10 | נָזֹֽלּוּ כִּ | igen (1) |
| Péld 11:31 | Péld 12:1 | 10\|11 | חוֹטֵֽא אֹהֵ֣ב | igen (1) |
| Jób 16:22 | Jób 17:1 | 9\|10 | אֶהֱלֹֽךְ רוּחִ֣ | igen (1) |
| Jób 36:33 | Jób 37:1 | 9\|10 | עוֹלֶֽה אַף | igen (1) |
| Hós 11:11 | Hós 12:1 | 19\|20 | יְהוָֽה סְבָבֻ֤ | igen (1) |
| Hós 1:11 | Hós 2:1 | 23\|24 | יִזְרְעֶֽאל אִמְר֥וּ | igen (1) |
| Préd 2:26 | Préd 2:25 | 9\|10 | נָתַ֛ן חָכְמָ֥ה | igen (2) |

*Proveniencia: `scope=f22/versosszevonas.tsv 9 sora (er_tol/er_ig: a határ) × kereses.heber_kereses a határon álló két token szo_kis-ével | forras=pardes.db meta.epites_ts=2026-10-18T12:18:16Z (~/pardes/pardes.db, WSL pardes) | ts=2026-10-18`.* A javítás a határ adatát kívánja a `pardes.db`-ben (az építő módosítása, M0 E5: nem a #76 hatóköre) → **DT-F76j** (nyitott). A súgó és a README a korlátot kiírja.

## 4. Mért idők (tájékoztató, korlát nélkül)

*Proveniencia: `scope=/kereses lapelőállítás (OldalGyar.kereses_lap, HTTP-gyorsítótár nélkül) és a keresés-rész (kereses.keres) | forras=pardes.db meta.epites_ts=2026-10-18T12:18:16Z meta.mod=teljes, /home/basesoft/pardes/pardes.db, 969.6 MB | ts=2026-10-18T15:01:23Z`; gép: Linux-6.18.54.1-microsoft-standard-WSL2-x86_64, 8 CPU, python 3.12.3, WSL `pardes` disztribúció, korlát nélkül (nem a VPS-t utánzó 1 vCPU / 2 GB). „Első”: az első hívás a folyamatban; „meleg”: 5 futás mediánja. Ugyanazon a gépen az ismételt mérések ±30–50%-ot szórtak (a WSL-gép terhelése).*

| keresés | eset | versek | előford. | első (ms) | meleg medián (ms) | keresés-rész medián (ms) |
|---|---|---|---|---|---|---|
| `szo=világosság mod=pontos` | szó pontos, ritka | 31 | 33 | 87.7 | 10.3 | 0.3 |
| `szo=föld mod=pontos` | szó pontos, tartalmas | 529 | 564 | 18.6 | 17.6 | 2.7 |
| `szo=és mod=pontos` | szó pontos, leggyakoribb | 17817 | 33877 | 110.7 | 97.7 | 74.0 |
| `szo=Isten mod=pontos` | szó pontos, gyakori | 1395 | 1508 | 22.4 | 21.4 | 6.8 |
| `szo=világosság` | szó (a) alap | 92 | 100 | 12.9 | 14.5 | 0.9 |
| `szo=föld` | szó (a) alap | 2267 | 2612 | 30.7 | 26.1 | 9.4 |
| `szo=és` | szó (a) alap | 17817 | 33877 | 161.7 | 169.0 | 133.7 |
| `szo=amely` | szó (a), mai alak | 2889 | 3318 | 25.9 | 25.5 | 10.6 |
| `szo=mond` | szó (a) alap | 4327 | 5028 | 29.2 | 44.6 | 23.0 |
| `szo=ő` | szó (a) alap | 8636 | 13493 | 87.4 | 69.7 | 47.5 |
| `szo=világosság mod=szoto_strong` | szó (c) | 725 | 963 | 24.3 | 21.5 | 6.5 |
| `szo=föld mod=szoto_strong` | szó (c) | 10264 | 16736 | 159.6 | 181.2 | 146.9 |
| `szo=ki mod=szoto_strong` | szó (c), funkciószó | 22214 | 83792 | 508.0 | 597.2 | 532.3 |
| `frazis=a föld` | frázis | 382 | 404 | 76.3 | 40.7 | 26.9 |
| `frazis=kietlen és` | frázis, ritka | 3 | 3 | 8.1 | 7.2 | 0.3 |
| `frazis=és monda az úr` | frázis, 4 szó | 94 | 94 | 43.4 | 39.4 | 23.8 |
| `strong=H0216` | Strong | 110 | 121 | 17.7 | 15.5 | 0.7 |
| `strong=H0430` | Strong, gyakori | 2248 | 2603 | 34.8 | 30.3 | 12.9 |
| `strong=H9002` | Strong, leggyakoribb (vav) | 15631 | 29708 | 131.6 | 108.0 | 87.8 |
| `strong=H1254 H0430` | két Strong | 12 | — | 22.4 | 21.7 | 11.1 |
| `strong=G3056` | Strong görög | 318 | 332 | 8.9 | 7.8 | 1.2 |
| `heber=בראשית ברא` | héber frázis | 1 | 1 | 6.9 | 6.7 | 0.5 |
| `heber=את השמים` | héber, gyakori szóval | 17 | 17 | 52.4 | 52.5 | 42.8 |
| `heber=ויאמר אלהים` | héber, gyakori | 26 | 26 | 32.0 | 32.3 | 18.6 |
| `heber=יהוה` | héber, 1 szó, nagyon gyakori | 5791 | 6834 | 61.1 | 38.7 | 25.7 |

**Értékelés (K5: magyar szóra 100 ms alatt).** A pontos alakra keresés a ritka, tartalmas és gyakori szavakon 0,3–7 ms (keresés-rész), a teljes lap 10–22 ms. **A leggyakoribb szónál (*és*, 33 877 előfordulás) a határon van:** a keresés-rész 74 ms, a teljes lap 98–111 ms (korábbi futásokban 88–140 ms is). A szótári alakos alapmódban az *és* 134 ms / 169 ms, a 100 ms fölött. A (c) mód a gyakori lemmákon 147–532 ms (a #95 ismert korlátja: 173–874 ms; mérve, nem küszöb). A mérvadó számot az M4 adja a VPS-t utánzó korláttal.

**Az M3 közbeni gyorsítások** (mért ok alapján): a tokenenkénti `vers`-illesztés helyett induláskor betöltött igehely→sorrend szótár; a pontos ág csak (igehely, sorszám) párt olvas (fedő index; előtte az *és* 122 ms csak SQL-ben); a párosított Strong-lista 5000 előfordulás fölött nem készül (a lap kiírja); a kiemelendő tokenek versenkénti csoportosítása csak a megjelenített lapra; a héber jelölt versek a szavak metszetéből, egyszavas, előtag nélküli szónál közvetlen indexes út (*יהוה* 512 → 26 ms).

## 5. Vizuális ellenőrzés

A szerver a WSL-ben (8771-es port, a munkafából) és a beépített böngésző: a `/kereses?q=világosság` és a `/kereses?heber=את השמים` lap a meglévő arculattal renderel (fejléc, nézet- és szintváltó, jelleg-címkék, forrássor, számlálók, `<mark>`-os kiemelés, a héber szópár a találat mellett). Új osztály: `talalatok`, `talalat` (az `elemek.toml` `[kizart]` táblájában, a meglévő tokenekkel); a regiszter-őr zöld (`teszt_tervezo.py`). A #60 pilottal való blokkonkénti vizuális összevetés nem történt (a pilotnak nincs keresőlapja); a felhasználói átnézés az M5-é.

## 6. Nyitott

- **DT-F76j** (🟢, a felhasználó döntése, 2026-10-18): ismert korlát, a 9 hely a README-ben és a súgóban; a javítás az N-F76k (az építő tárolja a belső MT-vershatárt).
- A magyar keresés a 9 párosítatlan ÚSZ-könyvben nem talál (ismert, F95; a lap jelzi). Pótlása (pl. a `vers.karoli_szoveg` szavaira épülő tartalék) új adatút volna, nem M3-tétel.
- A K5 a leggyakoribb szavakon a határon / fölötte (4. szakasz): az M4 méri korláttal.
- A `teszt_bdb_vers_jelentes.py` `test_bajtra_azonos` a main-en (89b30c2e) is piros, az M3-tól független: a generált `adat/bdb_vers_jelentes.tsv` fejlécében a `szamkiosztas` a „DT-F99n”-t „DT179”-re cserélte, a `bdb_vers_jelentes.py` még „DT-F99n”-t ír. Nem nyúltam hozzá (`adat/bdb_*` tiltott).
- A naplózás: a gunicorn hozzáférési napló a lekérdezés-szöveget nem írja (`%(U)s`, M0 3.7); a fejlesztői Werkzeug-szerver igen (a teljes URL-t), ez csak helyi fejlesztésnél fut.
