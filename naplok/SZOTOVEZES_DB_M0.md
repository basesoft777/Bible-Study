# SZOTOVEZES_DB (#95) — M0: felmérés (csak olvas)

*2026-10-13 · ág: `claude/f95-szotovezes-db` · modell: claude-sonnet-5-5 · a brief: `F95_SZOTOVEZES_DB_BRIEF.md` (v1)*

*Proveniencia (a teljes napló): `scope=adat/szoto/karoli_szotari_alak.tsv (sha256 edba33e6d65af46535ede231f36d2d7e4eeaab8ece2905ae831c1ddaf593a022, 3 155 773 bájt) + adat/karoli_strong/szavak_*.tsv (57 fájl, 981 147 token) + parok_*.tsv (492 380 sor) + adat/grammatikai_strongok.tsv (92 sor) | forras=repó-TSV-k közvetlen olvasása, saját mérőszkriptek (a repón kívül, scratchpad), a méretek és időzítések egy ideiglenes SQLite-fájlon, amely a mostani építő token_karoli/token_par tábláit (szo_kis oszloppal) és a javasolt új táblákat tartalmazza | ts=2026-10-13T17:53:57Z`*

**Az M0 nem írt a repóba, csak ezt a naplót (és a brief fejlécét).** A `pardes.db` helyi példánya (2026-10-12, F89/F92 előtti: nincs `tabla_licenc`, nincs `szo_kis`) a méréshez nem használható; a mérés a TSV-kből épített ideiglenes adatbázison történt. Az időzítések melegek (5 futás mediánja), az M2 hideg és meleg méréssel, a valódi `pardes.db`-n ismétli.

## 1. A betöltendő anyag

| Mérés | Érték |
|---|---|
| adatsor (a fejléc nélkül) | **66 824** (= a #94 záró száma) |
| egyedi `alak` | 66 824 (a kulcs egyedi, kis-/nagybetű-érzékeny); kisbetűsítve 62 869; `szo_kis`-szel 62 772 (ezért nem kulcs) |
| `modszer` | lexikon 43 770 · szabály 14 833 · név 6 772 · k_tabla 770 · kivétel 679 · **simplemma 0** |
| `alapige` nem üres | 4 743 · `szotari_alak_mai` ≠ `szotari_alak`: 1 129 · `regies_jegy` nem üres: 3 231 |
| `tovabbi_elfogadhato` nem üres | **34 sor, 34 alak** (egy-egy; `\|` a mai táblában nem fordul elő többszörösen) |
| kötőjeles `alak` | 1 502; nem NFC alak: 0 |
| a *alak* sor | `alak	alak	alak…` (lexikon): **adatsor 12 184**, a fájl 12 188. sora (3 `#`-sor + fejléc után). A brief „12188. sora” a fájlsor-számozás. A betöltő az első nem-`#` sort veszi fejlécnek, ezért nem vész el |
| nyers méret | 3,16 MB TSV |

## 2. Táblaterv (javaslat)

**T1 `szotari_alak`** — alakszintű tábla, a TSV nyolc oszlopa változatlanul (`alak`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato`, `modszer`, `szabaly_forras`, `regies_jegy`), 66 824 sor, táblaszintű licenc: új `SZARMAZTATOTT_LICENC['szotari_alak'] = ['szoto_tablak']` (a licencsor él: `tisztazott` / `igen` / cimke „minden jog fenntartva”), `hash:` meta-sor az építő meglévő mechanizmusával, `meta` forrás-kulcs (`szotari_alak:forras_sor`, a TSV sorszáma, mint a `token_macula:forras_sor`).
Indexek: `UNIQUE (alak)` (a kapcsolási kulcs; 1,2 MB), `(szotari_alak)` (~1 MB; a (c) mód és a pontos kis-/nagybetűs keresés). Tábla ~3,5 MB.

**T2 `szotari_kereso`** — a további elfogadható alak (és a többi mező) kereshetővé tétele egy kereső táblában: `(keresoalak, alak, mezok)`, ahol `keresoalak` = NFC + kisbetű (nem `szo_kis`: a kötőjelet megtartja), `mezok` = `szotari`, `mai`, `alapige`, `tovabbi` vesszős listája arra a (`keresoalak`, `alak`) párra. Egyedi pár: **72 720 sor** (a mezőnkénti nyers pár 138 425: szótári 66 824, mai 66 824, alapige 4 743, további 34). Index `(keresoalak, alak)`; tábla+index ~6–8 MB.
Ok: egyetlen indexelt lekérdezés szolgálja mind a négy keresést (K4), kis-/nagybetű-független (*Isten* 74 és *isten* 40 alakja egy kereséssel), és a `tovabbi_elfogadhato` `|`-listája nincs szétvágva a lekérdezés idejére. A `mezok` szűrés kell, ha a felület csak a szótári alakra (a) akar keresni.
Alternatíva (ha a kis-/nagybetű-független keresés nem kell): T1-en három index (`szotari_alak`, `szotari_alak_mai`, `alapige`; együtt ~2,8 MB), a 34 további alak nézettel. Egyszerűbb, de a kisbetűs *isten* keresés nem találja a *Isten* lemmát, és a további alak külön lekérdezés.

**Index a `token_karoli`-n (a kapcsolási kulcshoz):** `CREATE INDEX ... ON token_karoli (szo, igehely, sorszam) WHERE oldal='hu'` (részleges, **12,8 MB**; a teljes `(szo, oldal, igehely, sorszam)` 31 MB). Nélküle a join a tokenekre teljes táblabejárás: a mért idő 200–230 ms (K4 ellen); vele 3–20 ms. A lekérdezésnek tartalmaznia kell az `oldal='hu'` feltételt (a próbában úgy használja az index; az `EXPLAIN QUERY PLAN` tesztet erre írjuk).

**Összes többletméret:** T1 + T2 + token-index ≈ 27–32 MB a mostani 619 MB-hoz (4–5%).

## 3. A kapcsolási kulcs

`token_karoli.szo` = `szotari_alak.alak`, pontos egyezés (a `szo_kis` nem megy: a kötőjelet és a kis-/nagybetűt törli, a tábla viszont kis-/nagybetű-érzékeny, SEMA 2.27). A kulcs nem NULL-ozható, a `token_karoli.szo` szó szerint a Károli-szóalak. A kapcsolt kereső lekérdezés: *keresett alak → T2 → T1.alak → token_karoli.szo → (igehely, sorszam)*.

## 4. A nem illeszkedő tokenek (a K2 alapja)

`token_karoli` `oldal='hu'`: **484 820** token (megegyezik a briefben mértekkel); a pontos alak-kulcsra **483 748 (99,7789%)** talál. A brief 483 746-ot írt, az eltérés 2 token (a mostani mérés a 57 `szavak_*.tsv`-ből, a brief előmérése más szűréssel; a K2 küszöbét ez nem érinti: 99,78% ≈ 99,7789%). **Nem illeszkedő: 1 072**, mind kötőjeles alak darabja.

| Osztály | Token | Magyarázat |
|---|---:|---|
| kötőjeles alak darabja, a szomszéd tokenekkel kötőjellel összefűzve **feloldható** (2-tagú ablak 1 052, 3-tagú 14) | **1 066** | pl. *Béth*, *Semesben* (1Kir 4:9), *esküdtél* (1Kir 1:13), *mászó* (1Kir 4:33): a `token_karoli` a kötőjeles alakot szétvágja, a tábla egyben tartja |
| felfüggesztett kötőjel, **nem oldódik fel** | **6** | *mogyoró* (1Móz 30:37), *fige* és *faolaj* (5Móz 8:8), *nek* (5Móz 25:10: `„…háznép”-nek`), *méreg* (5Móz 29:18), *jog* (Eszt 1:13): a szövegben `mogyoró-`, `fige-`, … áll, a lexikon alakja nem egyezik |
| csak kis-/nagybetűben eltérő · üres · nem betű · egyéb | 0 | |

**Egy további, a briefben nem szereplő körülmény:** a kötőjeles alakok darabjaiként azonosítható tokenek összesen **4 750** (ablak-egyezéssel: a szomszéd tokenek `-`-jel összefűzve egy kötőjeles `alak`); ebből **1 066 nem talál** (fent), **3 684 viszont pontosan talál**, mert a darab önmagában is létező alak (pl. *Isten* az *Isten-…* alakból). Ez a 3 684 token (0,76%) „illeszkedik”, de a **darab saját szótári alakját** kapja, nem a kötőjeles alakét. A K2 99,78%-os arány tehát nem azt méri, hogy mind a 484 820 token a helyes alakhoz kapcsolódik; a tartalmi pontosság a kötőjeles alakoknál ennyivel gyengébb. (A 3 684 felső becslés: az ablak-egyezés ritkán adhat véletlen találatot; az M2 mintával ellenőrzi.)

**Javaslat a kezelésre (⛔ döntés):**
- **(A, javaslom)** Pontos kulcs + egy kis **`szotari_token_kotojeles`** tábla (`igehely`, `sorszam`, `alak`; 4 750 sor, a darabok → a kötőjeles alak), indexszel. A (c) mód és a felület a pontos találathoz hozzáveszi a táblát (a darab tokent a kötőjeles alakhoz is köti, a pontos-találatot nem törli). A 6 felfüggesztett kötőjeles token **dokumentált hiány** (0,0012%), nem találgatott. ~0,2 MB.
- (B) Csak pontos kulcs, a 1 072 (és a 3 684) **dokumentált hiány/korlát** a zárójelentésben és a SEMA-ban; nincs új tábla. Egyszerűbb, de a kötőjeles alakok lemmája a tokenekre nem elérhető.
- (C) A tartalékkulcs a `token_karoli`-ban oszlopként (`szo_alak`): a meglévő tábla séma-változása, az építő több táblát érint; nem javaslom.

## 5. Az ÚSZ-hiány és a lefedettség (mérve, nem pótolva)

A `token_karoli` 57 könyvet fed a 66-ból; **párosítatlan**: Mt, Mk, Luk, Ján, ApCsel, Róm, 1Kor, 2Kor, Jel = **114 161 szóalak-előfordulás** a Károli 597 082 szóközzel elválasztott szavából (**19,1%**). Ezekre a T1 tábla ad szótári alakot (a teljes Károlit fedi), de **token-kapcsolás nincs**: a (c) mód Strong-ága és a token-kapcsolás itt nem él. A `szotari_alak` 66 824 alakjából **9 487-et** egyetlen párosított `hu` token sem használ (a párosítatlan könyvek alakjai és a lexikon kisbetűs/nagybetűs változatai). A felület ezt a 9 könyvet külön jelzi (a #76 dolga); az M2 könyvcsoportonként méri az arányt.

## 6. A (c) mód lekérdezése (vázlat és az M0 előmérés)

(a) szótári alakra: `szotari_alak → token_karoli.szo` (fent). (c) = (a) **VAGY** Strong-ág:
1. a lemma tokenjeinek (T1 → `token_karoli`) `token_par`-beli Strong-jai (`token_par.strong`, egy sor egy Strong; a `token_karoli.strong` összetett `H9003+H7225` értéke nem alkalmas), a `grammatikai_strongok`-on kívül;
2. minden `hu` token, amelynek a `token_par`-sora ezek egyikét hordozza (`token_par.strong` index).
A „fő Strong-szám” a brief szavával: a nem nyelvtani Strong-szám (a `grammatikai_strongok` szűrés), nem találgatott „első” komponens. A *határt* (hány Strong, bizonyosság-szűrés: `alacsony` is számít-e) az M2 a #94 mérés szerint egyszerű unióval méri; a szűrés a #76 dolga.

**Mintalista (a mérés előtt rögzítve; `egyedi lemma = szotari_alak`, a `hu`-tokenek száma a pontos kulccsal):**
- **10 gyakori** (a legtöbb tokenű lemmák, ≥50% párosított, van nem nyelvtani Strongjuk; ez *terhelési próba*, sok funkciószó van köztük): *és* 33 877 · *ő* 13 493 · *én* 6 503 · *te* 6 419 · *Úr* 6 163 · *hogy* 5 700 · *ki* 5 575 · *mond* 4 873 · *nem* 4 811 · *fiú* 4 496
- **10 tartalmas gyakori** (hossz ≥ 4, ≥50% párosított; a funkciószavak nagy része is bent van): *hogy* 5 700 · *mond* 4 873 · *pedig* 3 950 · *Isten* 3 419 · *lesz* 3 372 · *mely* 3 306 · *mert* 3 178 · *király* 2 659 · *föld* 2 612 · *minden* 2 591. Az M2 a tartalmas szavakkal (*Isten, király, föld, ember, szól, város, Izráel, Dávid, lélek, cselekedik*) kiegészíti, mert a felület valódi használata ezek.
- **10 ritka** (3–5 tokenű lemma, ≥1 párosított token és nem nyelvtani Strong; sha256-sorrend szerinti első 10, tehát determinisztikus): *Giddél, atyjaik, Simsai, Selúmiel, megszerzés, Ófel, Amaria, Kimhám, bírták, Hái*

**Előmérés (ideiglenes DB, meleg, medián; ms / találat) — a megfelelő indexekkel:**

| lekérdezés | gyakori (10) | ritka (10) |
|---|---|---|
| (a) szótári alak → tokenek (T1.`szotari_alak` + token-index) | 2,8–19,9 ms (a *és*: 33 877 találat, 19,9) | 0,08–0,13 ms |
| kereső (T2 → token) | 5,2–43,3 ms (*és*: 67 754, mert a (szótári, mai) kétszer szerepel: a végleges T2 a `DISTINCT` párokra szűr) | 0,09–0,12 ms |
| (c) szótári alak VAGY Strong | **190–866 ms** (16–80 ezer találat; *ki* 866, *ő* 684) | 0,16–27 ms (*megszerzés*: 2 892 találat, 27 ms; *atyjaik*: 1 216, 13 ms) |

Az (a) és a kereső a **K4 100 ms-os küszöbén belül** van (index nélkül 200–230 ms: ezért kell a token-index). A **(c) módnak a gyakori lemmákon nincs 100 ms-os teljesítése**: a Strong-ág tízezres találathalmazt ad vissza, a költség a halmaz felépítése. A K4 a (c) módra csak azt írja elő, hogy **mérve** legyen proveniencia-sorral, nem a küszöböt; ezt a jelentés rögzíti, és a #76 oldalon lapozás/`COUNT` megoldja. **A kutatói felület elsősorban a ritka alakokat a (c) módon keresi, ott 0,2–27 ms.**
Megjegyzés: a *ki* (283 Strong) és az *ő* (76) a Strong-ágat szétveti; a (c) mód funkciószavakra nem értelmes, ezt az M2 mérés és a #76 felület-oldali szűrés kezeli (a mért pontosság a #94-ben szintén a tartalmas lemmákra vonatkozik).

## 7. A frissességi teszt helye

`eszkozok/olvaso_pilot/db_meres.py`: a `TSV_FORRAS` (D5) kap egy `'szotari_alak': ['adat/szoto/karoli_szotari_alak.tsv']` sort, az `EGYEZO_SORSZAM` is (a `tsv_sorok` a `#`-sorokat kihagyja, a fejlécet levonja: 66 824); a `LAPHOZ_TABLAK`-hoz hozzáadjuk a `szotari_alak`-ot (és ha T2/kötőjeles tábla épül, azokat). A `META_FORRAS_SOR` nem kell: a `hash:` meta-sor + `EGYEZO_SORSZAM` fedi.

## 8. A ⛔ ponthoz — mit kérek jóváhagyni

1. **Táblaterv:** T1 `szotari_alak` + T2 `szotari_kereso` (72 720 sor) + részleges token-index (12,8 MB); az egyszerű alternatíva (T1 három indexszel, további alak nézet) elfogadható-e inkább.
2. **Kapcsolási kulcs:** `token_karoli.szo` = `szotari_alak.alak` (pontos, kis-/nagybetű-érzékeny).
3. **Nem illeszkedő tokenek:** (A) kötőjeles segédtábla (4 750 sor) + 6 felfüggesztett kötőjeles token dokumentált hiányként; vagy (B) csak dokumentált hiány.
4. **A (c) mód mintalista** (fent) és a „fő Strong” definíciója (nem nyelvtani Strong, `token_par`-ból) jóváhagyása; a K4 100 ms-os küszöbe az (a) és kereső módra érvényes, a (c) gyakori lemmákra nem teljesül (mérve, jelentve).

## 9. M2 mérés (a jóváhagyott terv szerint, a kész `pardes.db`-n)

*Kiváltó: `python eszkozok/olvaso_pilot/db_meres.py --szoto` (a lemmalista a 6. szakaszban, a mérés előtt rögzítve). A teljes építés: `python eszkozok/sqlite_epit.py --mod teljes --ketszer --meret --naplo --proba` (G2: azonos; 15 próbapont MEGEGYEZIK; `naplok/SQLITE_EPIT_meres.md`).*

*Proveniencia: `scope=szotari_alak, szotari_kereso, szotari_token_kotojeles | forras=pardes.db meta.epites_ts=2026-10-13T18:10:45Z meta.mod=teljes (hash:szotari_alak=796b64a99731) | ts=2026-10-13T18:14:28Z`; gép: Windows-11-10.0.26300-SP0, 8 CPU, python 3.14.7, pardes.db 938.3 MB*

**D5 (frissesség)**: eltérő táblák (az egész `pardes.db`): nincs
- `szotari_alak`: meta-sor 66824, hash egyezik a tartalommal: True, tsv-sor most: 66824, eltérés: nincs
- `szotari_kereso`: meta-sor 72720, hash egyezik a tartalommal: True, tsv-sor most: —, eltérés: nincs
- `szotari_token_kotojeles`: meta-sor 4750, hash egyezik a tartalommal: True, tsv-sor most: —, eltérés: nincs

**Kapcsolási arány** (`token_karoli` `oldal=hu` token; pontos = `szo`=`alak`; +kötőjeles = a `szotari_token_kotojeles` feloldja):

| könyvcsoport | hu token | pontos | % | +kötőjeles | % | nem illeszkedik |
|---|---:|---:|---:|---:|---:|---:|
| Tóra (1–5Móz) | 118302 | 118088 | 99.82 | 118297 | 100.00 | 5 |
| történeti (Józs–Eszt) | 157698 | 157184 | 99.67 | 157697 | 100.00 | 1 |
| költői (Jób–Sir) | 66169 | 66038 | 99.80 | 66169 | 100.00 | 0 |
| próféták (Ézs–Mal) | 114710 | 114508 | 99.82 | 114710 | 100.00 | 0 |
| ÚSZ, párosított (Gal–Júd) | 27941 | 27930 | 99.96 | 27941 | 100.00 | 0 |
| ÚSZ, párosítatlan (Mt, Mk, Luk, Ján, ApCsel, Róm, 1–2Kor, Jel) | 0 | 0 | — | 0 | — | 0 |
| **összesen** | 484820 | 483748 | 99.7789 | 484814 | 99.9988 | 6 |

**Keresési idők** (ms; meleg = 5 futás mediánja, hideg = új kapcsolat, első futás; találat = token): 

| csoport | lemma | (a) meleg | (a) hideg | találat | kereső meleg | kereső hideg | találat | (c) meleg | (c) hideg | találat | Strong |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gyakori | és | 18.8 | 20.6 | 33877 | 18.9 | 20.5 | 33877 | 379.7 | 385.7 | 55453 | 24 |
| gyakori | ő | 7.5 | 9.1 | 13493 | 7.2 | 8.8 | 13493 | 670.7 | 659.2 | 67160 | 76 |
| gyakori | én | 3.5 | 5.2 | 6503 | 3.4 | 4.5 | 6504 | 378.6 | 375.1 | 34127 | 62 |
| gyakori | te | 3.4 | 5.2 | 6419 | 3.4 | 5.0 | 6420 | 275.2 | 298.6 | 25029 | 44 |
| gyakori | Úr | 3.4 | 4.4 | 6163 | 4.2 | 5.3 | 7615 | 266.0 | 257.4 | 20605 | 23 |
| gyakori | hogy | 3.1 | 4.1 | 5700 | 3.1 | 4.0 | 5700 | 273.7 | 273.8 | 28671 | 42 |
| gyakori | ki | 3.1 | 4.3 | 5575 | 3.0 | 4.0 | 5583 | 874.4 | 852.6 | 80335 | 283 |
| gyakori | mond | 2.6 | 3.7 | 4873 | 2.8 | 3.8 | 5014 | 273.9 | 271.9 | 21326 | 54 |
| gyakori | nem | 2.8 | 3.8 | 4811 | 2.6 | 3.4 | 4811 | 173.1 | 172.6 | 16772 | 76 |
| gyakori | fiú | 2.5 | 3.8 | 4496 | 2.5 | 3.4 | 4506 | 268.6 | 261.9 | 22287 | 57 |
| tartalmas | Isten | 1.9 | 2.9 | 3419 | 2.2 | 3.0 | 3671 | 232.4 | 230.5 | 20306 | 38 |
| tartalmas | király | 1.4 | 2.4 | 2659 | 1.4 | 2.3 | 2659 | 161.2 | 156.9 | 13479 | 26 |
| tartalmas | föld | 1.5 | 2.6 | 2612 | 1.5 | 2.4 | 2612 | 202.2 | 203.9 | 16736 | 40 |
| tartalmas | ember | 0.9 | 1.8 | 1405 | 0.8 | 1.6 | 1405 | 306.4 | 304.7 | 28623 | 66 |
| tartalmas | szól | 0.8 | 2.1 | 1344 | 0.8 | 1.7 | 1351 | 282.7 | 277.5 | 24936 | 53 |
| tartalmas | város | 0.7 | 1.6 | 1141 | 0.7 | 1.5 | 1141 | 119.4 | 119.6 | 10701 | 29 |
| tartalmas | Izráel | 1.3 | 2.3 | 2462 | 1.3 | 2.3 | 2462 | 157.2 | 157.1 | 13944 | 14 |
| tartalmas | Dávid | 0.6 | 1.7 | 1069 | 0.7 | 1.4 | 1069 | 131.9 | 128.4 | 11509 | 12 |
| tartalmas | lélek | 0.5 | 1.4 | 810 | 0.6 | 1.2 | 813 | 50.0 | 49.2 | 3310 | 16 |
| tartalmas | cselekedik | 0.6 | 1.6 | 995 | 0.6 | 1.4 | 1024 | 199.8 | 202.3 | 17575 | 54 |
| ritka | Giddél | 0.1 | 0.9 | 4 | 0.1 | 0.7 | 4 | 0.1 | 1.3 | 4 | 1 |
| ritka | atyjaik | 0.1 | 0.9 | 4 | 0.1 | 0.7 | 4 | 12.9 | 14.3 | 1216 | 1 |
| ritka | Simsai | 0.1 | 1.0 | 4 | 0.1 | 0.8 | 4 | 0.1 | 1.1 | 4 | 1 |
| ritka | Selúmiel | 0.1 | 0.8 | 5 | 0.1 | 0.7 | 5 | 0.1 | 1.2 | 5 | 1 |
| ritka | megszerzés | 0.1 | 0.9 | 4 | 0.1 | 0.7 | 4 | 27.2 | 28.8 | 2892 | 3 |
| ritka | Ófel | 0.1 | 0.8 | 3 | 0.1 | 0.9 | 3 | 0.1 | 1.3 | 5 | 1 |
| ritka | Amaria | 0.1 | 0.8 | 3 | 0.1 | 0.7 | 3 | 0.2 | 1.2 | 16 | 1 |
| ritka | Kimhám | 0.1 | 0.9 | 4 | 0.1 | 0.9 | 4 | 0.5 | 3.6 | 173 | 2 |
| ritka | bírták | 0.1 | 0.9 | 5 | 0.1 | 0.7 | 5 | 0.6 | 4.7 | 222 | 3 |
| ritka | Hái | 0.1 | 0.9 | 3 | 0.1 | 0.9 | 3 | 0.2 | 1.5 | 41 | 1 |

A maximum (a) idő csoportonként: {'gyakori': 20.6, 'tartalmas': 2.9, 'ritka': 1.0}; a kereső tábla maximuma: {'gyakori': 20.5, 'tartalmas': 3.0, 'ritka': 0.9} (K4: 100 ms az (a) módra és a kereső táblára).

**EXPLAIN QUERY PLAN** (a keresés indexet használ):
- (a): SEARCH a USING INDEX ix_szotari_alak_0 (szotari_alak=?) / SEARCH t USING COVERING INDEX ix_token_karoli_szo_hu (szo=?)
- kereső: SEARCH k USING COVERING INDEX ix_szotari_kereso_0 (keresoalak=?) / SEARCH t USING COVERING INDEX ix_token_karoli_szo_hu (szo=?)


**Értékelés.** K2: a pontos kulcs 99,7789% (= az előmérés 99,78%-a), a kötőjeles segédtáblával 99,9988%; a 6 megmaradó token a felfüggesztett kötőjeles. K3: a D5 a három új táblán hash- és sorszám-egyezést ad, eltérő tábla nincs. K4: az (a) mód és a kereső tábla maximuma 20,6 ms (hideg is) a 100 ms alatt; a (c) mód gyakori lemmákon 173–874 ms, ritkákon 0,1–27 ms; ez a #76 felé ismert korlát. A mintalekérdezések az `EXPLAIN QUERY PLAN` szerint indexet használnak.
