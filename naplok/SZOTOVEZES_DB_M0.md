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
