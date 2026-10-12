# F79 M0 — felmérés (séma-terv és nyitott pontok)

*FELADATOK #79 · `F79_SQLITE_EPIT_BRIEF.md` M0 · 2026.10.12 · a táblák sorszámai csak adatsorokat számolnak (fejléc- és megjegyzéssorok nélkül; javítva az F79.12-ben, ELLENOR_F79 9. pont) · csak olvasás történt; a #79 eddig sem `adat/`-t, sem `konkordancia/`-t nem módosított.*

Proveniencia: `scope=manual | forras=adat/*.tsv, konkordancia/*.tsv, eszkozok/ellenoriz.py, eszkozok/general.py, adat/SEMA.md | ts=2026-10-12` (a számok a repó mai tartalmából, saját olvasással mérve: `split('\t')`, a `#` sorok kihagyásával).

## 1. Táblaleltár (mi kerülhet a `pardes.db`-be)

Kulcs-alak: **HU** = magyar kanonikus (`1Móz 1:1`), **STEP** = STEPBible-pontozott (`Gen.1.1`), **egyéb** = külön ábra.

| Forrás | Sor | Kulcs-alak | Licenc-sor (`licencek.tsv`) | `kereskedelmi` |
|---|---|---|---|---|
| `adat/motivumok, elofordulasok, kapcsolatok, jeloltek, auditok, lexikon_hivatkozasok, grammatikai_strongok, res_forras, …` | 9 / 259 / 39 / 592 / 222 / 23 / 92 / 56 | HU (az `elofordulasok.igehely` tartomány is lehet: `1Móz 14:18-20`, `Zsid 7:1-28`) | `projekt_adat` | `tisztazatlan` |
| `adat/karoli_strong/parok_*` (39 könyv) / `szavak_*` | 466 785 / 926 179 | HU (a `vers` oszlop) | **nincs sor** (a `Karoli_Strong_kivonat` sor `tisztazatlan`, de az más tábla) | — |
| `adat/karoli_variancia.tsv` | 42 799 | HU (`igehely` a `megerosites` sornál) | **nincs sor** | — |
| `adat/kulso/lxx_bridge.tsv` | 3 301 | Strong-pár, nincs igehely | `lxx_bridge` | igen |
| `Karoli_1908.tsv` | 31 158 | HU | `Karoli_1908` | igen (közkincs) |
| `Karoli_versmegfeleltetes.tsv` | 22 931 | HU (+ KJV/MT számozás) | `Karoli_versmegfeleltetes` | `tisztazatlan` |
| `TAHOT_kivonat.tsv` | 469 300 | HU (F85.6 óta Károli-vers) | `TAHOT` | igen |
| `TAGNT_kivonat.tsv` | 141 746 | HU | `TAGNT` | igen |
| `TSK_kereszthivatkozasok.tsv` | 432 949 | HU (mindkét oldal) | `TSK` | igen |
| `Karoli_kereszthivatkozasok.tsv` | 32 407 | **STEP** (mindkét oldal, tartomány: `Gen.2.4-Gen.2.5`) | `Karoli_KH` | igen |
| `Karoli_Strong_kivonat.tsv` | 383 | **STEP** | `Karoli_Strong_kivonat` | `tisztazatlan` |
| `TIPNR_kivonat.tsv` | 35 522 | **STEP** | `TIPNR` | igen |
| `BSB_Strongs.tsv` | 278 166 | **STEP** (MT-számozás), 7. oszlop `Számozás`: `mt` 260 284, `ellenorizetlen` 17 659, `kjv` 223 | `BSB_Strongs` | igen |
| `KJV_Strongs_teljes.tsv` | 349 308 | **STEP** | `KJV_Strongs_teljes` | `tisztazatlan` |
| `KJV_/ASV_Strongs_{Genesis,Exodus,Proverbs}.tsv` | 6 fájl | **STEP** | `KJV_ASV_Strongs` | `tisztazatlan` |
| `LXX_OS/*.tsv` (62 fájl), `LXX_versszintu_parok.tsv` | — / 104 518 | HU (`igehely_karoli` / `igehely`) | `LXX_OS` / `LXX_versszintu_parok` | igen / `tisztazatlan` |
| `Macula_heber_*.tsv` (39 fájl), `Macula_gorog.tsv` | — / 275 520 | HU (`karoli` oszlop) | `Macula_heber`, `Macula_gorog` | igen |
| Lexikonok: `BDB_teljes_unabridged` 8 099, `Strong_szotar` 14 347, `Thayer_teljes` 5 426, `LSJ_teljes` 5 522, `SECE_G/H`, `TBESG/H`, `MCGED` 5 303 (`kereskedelmi`: **nem**) | — | Strong | soronként van | vegyes |
| `SDBH_domenek` 22 280, `SDGNT_domenek` 9 075, `UBS_DBH/DNTG_*` (referenciák 389 212 + 130 948) | — | Strong / HU | CC BY-SA 4.0 (`share_alike=igen`) | igen |
| `tW_szocikkek.tsv` | 598 | Strong-lista | `tW_szocikkek` | **feltételesen** |
| `Nave_basokant.tsv` | 85 246 | HU (`igehely_karoli`) | `Nave_basokant` | igen |
| `motivumok/*.md` (9 fájl, 88 KB), `tematikus_lezart/` (8 tanulmány + 7 napló + 1 összesítő), `genezis/` (20 + 2 napló + 2 összesítő), `ujszovetseg/` (3), `melyelemzesek/` (1) | — | próza | `projekt_adat` | `tisztazatlan` |

A `datasetek.tsv` öt datasetjéhez nincs licencsor: `Karoli_Strong_parok`, `Karoli_Strong_szavak`, `OSHL_BDB_igehelyek`, `OSHL_lexikalis_index`, `openbible_crossrefs` (az utóbbi `hianyzik`). A `licencek.tsv` 46 adatsorában `kereskedelmi`: igen 33, tisztazatlan 10, nem 2 (`MCGED`, `Heber_ETCBC_modulok`), feltetelesen 1 (`tW_szocikkek`).

## 2. A normalizálhatóság próbája (a három STEPBible-dataset, `Konyv_normalizalo_tabla.tsv`-vel)

| Dataset | Sor | Normalizálható | Nem | Normalizált, de nincs ilyen Károli-vers |
|---|---|---|---|---|
| `Karoli_kereszthivatkozasok.tsv` | 32 407 (kulcs- és cél-oldal) | 32 407 | 0 | **337 JSir + 96 más** előfordulás (kulcs- és cél-oldal együtt; lásd alább) |
| `Karoli_Strong_kivonat.tsv` | 383 | 383 | 0 | 1 (`Jób 17:16`; a #87 tárgya) |
| `TIPNR_kivonat.tsv` | 35 522 | 35 492 | **30** (`LXX.Gen.46.20`, `LXX.Exo.3.8`, `[Act.26.7]`, `[Gen.30.1]` …) | 95 (köztük 58 JSir) |

Három következmény:

1. **A TIPNR 30 nem leképezhető sora** a jelentésbe kerül névvel (G5): `LXX.`-előtagú és szögletes zárójeles hivatkozások; nem esnek ki némán.
2. **`Lam` → `JSir` vs. `Sir` (a legfontosabb lelet).** A `Konyv_normalizalo_tabla.tsv` `Lam`-ot `JSir`-re képez (DT24/F28.9, a Sirák fia könyvével való ütközés miatt), de a `Karoli_1908.tsv`, a `TAHOT_kivonat.tsv` és a `karoli_strong/` kulcsa továbbra is `Sir` (Siralmak). Normalizálás után tehát a Siralmak minden STEP-alakú sora (337 KH + 58 TIPNR) olyan kulcsra esik, amely a Károli-versek között nincs: **a CLAUDE.md szerinti néma nem-találat másik alakja**. A `lekerdez.py` a `Sir`-t álnévként olvassa (DT24 (d)). Az építőnek kell egy explicit könyvkulcs-álnév (nyitott pont 6).
3. **Egyéb kulcs-hiány** (96 KH-előfordulás, 37 TIPNR-sor): a hivatkozás normalizálható, de a Károli számozásban nincs ilyen vers (pl. `Jób 36:34`, `Ézs 64:12`, `Péld 11:37`, `Zsolt 138:12`, `Róm 3:31`). Ezek a TSK/KH forrás-számozásból jönnek; az építő nem javítja, hanem `szamozas=ellenorizetlen`-szerű jelzéssel (vagy a jelentésben) tartja őket (nincs interpoláció, CLAUDE.md 3. szabály).
4. TAHOT: 23 204 vers-kulcs, mind Károli-vers; Károli-vers TAHOT-sor nélkül: 0. TAGNT: 7 948 vers, 3 Károli-kulcs nélkül (`1Kor 3:23`, `Róm 3:31`, `Róm 8:39`).
5. Nem-normalizáló STEP-alakú dataset a brief három neve mellett még: `BSB_Strongs`, `KJV_Strongs_teljes`, `KJV_/ASV_*`. A **BSB `Igehely` oszlopa MT-számozású**, tehát a Károli-vers-kulcsra a `Karoli_versmegfeleltetes.tsv` `igehely_mt` → `igehely_karoli` oszlopán át képezhető, nem a puszta könyvnév-konverzióval.

## 3. Az `ellenoriz.py` függvényeinek bemenete

Az `ellenoriz.main()` a hét tábla soraiból `general.tsv_beolvas()`-szal `list[dict]`-et épít (`#` sorokat kihagyva), és ezt adja a `szabaly1…8` függvényeknek (`szabaly1(motivum_id_halmaz, elofordulasok, kapcsolatok, jeloltek, auditok)`, `szabaly2(elofordulasok, jeloltek)`, `szabaly3(elofordulasok, auditok)`, `szabaly4(elofordulasok)`, `szabaly5(elofordulasok)`, `szabaly6(motivumok)`, `szabaly7(motivumok, elofordulasok)`, `szabaly8…(motivumok, elofordulasok, auditok, datasetek)`). **Az építő ugyanezt a betöltőt és ugyanezeket a sorlistákat használja**, tehát a bemenet azonos; a szabály-kód nem másolódik (G4). Mai állapot: `python eszkozok/ellenoriz.py` → RENDBEN 11, SÉRTÉS 0, KÉZI 2, JELENTÉS 3.

Két eltérés a brief szövegétől:

- A `szabaly7` (`gate.py` ütközés/részhalmaz) **jelentés, nem kikényszerített** (a CLI is ezt mondja: „a kilépési kódot nem befolyásolja”); „sértésnél megáll” rá nem értelmezhető, a negatív teszt a 7. szabályra nem írható. Javaslat: 7. = jelentés a naplóban.
- A SEMA 3. szakasz 9. pontja (egyirányúság) kézi ellenőrzés; az `ellenoriz.py` `szabaly9…14` függvényei más szabályok (jelentés-szám, v2.2-táblák, rés-forrás, fordítási gyorsítótár, kiejtés), és SÉRTÉS-képesek (9., 10., 11., 13.). A brief a `szabaly1…8`-at írja elő; ezek a további SÉRTÉS-képes szabályok tartoznak-e az építéshez, nyitott (7. pont).

## 4. Séma-terv (táblánként; minden táblán `licenc_allapot TEXT NOT NULL`, `kereskedelmi TEXT NOT NULL`, `licenc_dataset TEXT NOT NULL`)

Típusok: `IGEHELY` = a KK-kulcs (TEXT, `1Móz 1:1`; `konyv`, `fejezet`, `vers` külön INTEGER-oszlopokkal a rendezéshez), `STRONG` = TEXT `H0001`/`G0001` (`strong_normalizal()`, utótag nélkül; `+` lánc külön sorra bontva a `strong_lanc` mellékoszlopban), `PROVENIENCIA` = TEXT szó szerint, `IGAZOLAS` külön mező.

| Tábla | Oszlopok (kivonat) | Indexek |
|---|---|---|
| `meta` | `kulcs`, `ertek` (építési ts, git-sha, SEMA-verzió, építés-proveniencia, szabályonkénti eredmény) | PK `kulcs` |
| `konyv` | `kk_kod` (PK), `sorrend`, `step_kod`, `teljes_nev`, `testamentum`, `kk_alias` | PK |
| `vers` | `igehely` (PK), `konyv`, `fejezet`, `vers`, `karoli_szoveg`, `szamozas` (`mt` \| `ellenorizetlen` \| `kjv` \| `eltolodas_gyanu_N46`), `szamozas_forras`, `kjv_igehely`, `mt_igehely` | PK; `(konyv,fejezet,vers)` |
| `igehely_tartomany` | `forras_tabla`, `forras_sor`, `tol`, `ig` (vers-tartomány kibontva: egy sor/vers) | `(tol)`, `(forras_tabla,forras_sor)` |
| `token_eredeti` | `igehely`, `sorszam`, `nyelv`, `strong_lanc`, `strong`, `alak`, `szotő`, `jelentes`, `forras` (TAHOT/TAGNT) | `(strong)`, `(igehely,sorszam)` |
| `token_karoli` | `igehely`, `sorszam`, `karoli_szo`, `strong` (a partnerek `+`-lánca), `allapot`, `bizonyossag`, `proveniencia` (a `parok`/`szavak` fejléc-sorából) | `(igehely,sorszam)`, `(strong)` |
| `token_par` | a `parok_*` sorai: `igehely`, `hu_sorszam`, `hu_szo`, `er_sorszam`, `strong`, `bizonyossag`, `forras` | `(strong)`, `(igehely)` |
| `strong_parok` | `a`, `b` (a < b), `n` (közös vers), a `grammatikai_strongok` és a `H9xxx` morféma-kódok kiszűrve, a `TILTOLISTA` nem szűrhető | PK `(a,b)`; `(n)` |
| `frazis_pozicio` | az 5. pont: a token-táblák pozícióra rendezett nézete (`igehely`, `sorszam`, `strong`, `karoli_szo`) | `(igehely,sorszam)` |
| `tsk` | `forras`, `cel_tol`, `cel_ig`, `votes` | `(forras)`, `(cel_tol)` |
| `kh` (Károli-KH), `tipnr` | normalizált `igehely` + a nyers STEP-érték (`step_nyers`) + `normalizalt` BOOL | `(igehely)` |
| `normalizalas_jelentes` | a nem leképezhető / nem Károli-kulcsú sorok: `tabla`, `nyers`, `ok` | — |
| `bsb`, `kjv` | `step_nyers`, `igehely` (KK, a megfeleltetésen át), `sorszam`, `strong`, `angol_szo`, `szamozas` | `(igehely)`, `(strong)` |
| `szotar_*` (`bdb`, `strong_szotar`, `thayer`, `lsj`, `tbes`, `sece`, `mcged`, `sdbh`, `sdgnt`, `ubs_*`, `tw`) | `strong`, tartalmi oszlopok, `share_alike`, `cimke` | `(strong)` |
| `lxx_hid` | `lxx_bridge` + `LXX_versszintu_parok` + `lxx_dontesek` (a 14. és 26. pont) | `(hebrew_strong)` |
| adat-táblák 1:1 | `motivumok`, `elofordulasok`, `kapcsolatok`, `jeloltek`, `auditok`, `lexikon_hivatkozasok`, `grammatikai_strongok`, `res_forras`, `kiejtes_*`, `forditasok`, `terminologia`, `licencek`, `datasetek` | a SEMA kulcsai |
| `fts_motivum` (FTS5) | `motivum_id`, `rovat`, `forras_fajl`, `regi_forras` (0/1), `szoveg` | — |

Az építés rendje: betöltés `split('\t')`-vel → `ellenoriz` függvények a sorlistákon → csak ha nulla SÉRTÉS, `pardes.db.epit` ideiglenes fájlba építés → átnevezés `pardes.db`-re → `naplok/SQLITE_EPIT_integritas.md` és `_meres.md`. A tartalom-hash táblánként: a sorok rendezett `'\t'.join()` hash-e (G2).

## 5. Nyitott pontok a felhasználónak (DT109)

**(1) A vers-kulcs a KK (Károli-vers).** Megerősítés. Kiegészítés: a BSB/KJV STEP-sorok KK-ra képezése a `Karoli_versmegfeleltetes.tsv`-en át történik, és a `vers.szamozas` a BSB 7. oszlopából (aggregálva KK-versre) + az N46 44 verséből áll; ha egy KK-vers több BSB-értéket kap, a szigorúbb (`ellenorizetlen`) nyer. Javaslat: igen.

**(2) A `kereskedelmi` oszlop forrása.** A `licencek.tsv`-nek van `kereskedelmi` mezője (`igen`/`nem`/`feltetelesen`/`tisztazatlan`), tehát nem kell levezetett érték; a `licenc_allapot` az `allapot` (`tisztazott`/`kozkincs`/`tisztazatlan`). Kérdések: **(a)** a G6 szerint „ismeretlen licenc nem kap alapértéket, a tábla nem épül be”. Ha a `tisztazatlan` is „ismeretlen”, akkor kimarad a `projekt_adat` (motivumok, elofordulasok, minden `adat/` tábla), a `Karoli_versmegfeleltetes`, `KJV_Strongs_teljes`, `LXX_versszintu_parok`, `Karoli_Strong_kivonat` — az olvasói konkordancia nagy része. Javaslat: a **`tisztazatlan` kijelölt érték** (az adat szerint ismert állapot, nem alapérték), és csak a **licencsor nélküli** tábla marad ki (ma: `Karoli_Strong_parok/szavak`, `OSHL_*`, `karoli_variancia`, `openbible_crossrefs`); a szűrőt a #76/#86 végzi. **(b)** A `Karoli_Strong_parok/szavak/variancia` (a #22 kimenete, a `token_*` és az 5. pont forrása) licencsor nélkül maradna: kell egy `licencek.tsv`-sor (külön feladat, a #79 nem ír `adat/`-ba) vagy hozzárendelés a `Karoli_Strong_kivonat` (tisztazatlan) sorhoz. Javaslat: a leképezés explicit kódtábla az építőben, hiányzó sorra az építés a táblát kihagyja és jelenti; a licencsor felvétele külön tétel. **(c)** A származtatott tábla (`strong_parok`, `token_karoli`, `vers`) licence a forrásaié közül a legszigorúbb (SDBH/SDGNT/Louw–Nida CC BY-SA-származék jelölve).

**(3) Az integritás-ellenőrzés ideje.** Javaslat: a betöltés **előtt**, a TSV-sorlistákon, a meglévő `ellenoriz.py` függvényekkel (egy szabály, egy implementáció; a 3. pont szerint a bemenet azonos). Utóbb, az adatbázisból visszaolvasva csak a darabszám-egyezés (sorszám ≡ forrás) fut kontrollként. A `szabaly7` jelentés marad (3. pont).

**(4) A kis minta táblái.** Javaslat: minden `adat/*.tsv` (kicsi) + `Karoli_1908` és `Karoli_versmegfeleltetes` + a következők **az 1Mózesre szűrve és a 8 motívum minden hivatkozott versével** (`elofordulasok`/`kapcsolatok`/`auditok` igehelyei, köztük `Jer 4:23`, `Ézs 34:11`, mert a 4. pont várt eredménye 1Mózesen kívüli verseket nevez): `TAHOT`, `TAGNT`, `parok_*`/`szavak_*` (a megfelelő könyvek), `TSK`, `Károli-KH`, `TIPNR`, `BSB`; teljes, mert kicsi vagy Strong-kulcsú: `BDB`, `Strong_szotar`, `lxx_bridge`, `lxx_dontesek`, `kiejtes_*`, `grammatikai_strongok`. A 13–15. pont miatt a `Thayer`, `LXX_versszintu_parok` szűrve a mintára. Kimarad a kis mintából: `Macula_*`, `UBS_*`, `SDBH/SDGNT`, `Nave`, `KJV_*` (nem szükségesek az 1–6., 13–15. ponthoz). Elfogadod?

**(5) Az átmeneti FTS fájlköre és kiesési szabálya (az irány eldöntve: igen, `regi_forras` jelöléssel).** Javasolt fájlkör: `tematikus_lezart/*_tematikus.md` (8 tanulmány), `tematikus_lezart/naplok/*_kereszthivatkozas_naplo.md` (7, kézi forrás; a 16. pont mintaképe külön nevezi a „HAMART-001 napló”-t), `genezis/1Moz_*_bovitett.md` (20), `genezis/naplok/*` (2), `ujszovetseg/*_bovitett.md` (3), `melyelemzesek/*` (1; a brief három könyvtárat nevez, ez a negyedik kézi forrás); **kizárva:** a generált `lexikon/`, a gyökér-`naplok/`, a `Konnyu_ellenorzes_*` összesítők (nem tanulmány, hanem ellenőrzés-jelentés), `generalt_proba/`, `motivumlog/`. Az `motivumok/[ID].md` (9 fájl, 88 KB) `regi_forras=0`. **Kiesési szabály — hiányzó gépi jel:** ma minden 8+1 `motivumok/[ID].md` létezik, de ezek az F4.4 „forrásréteg” részleges fájljai (csak az ítélet-blokkok, 2–11 KB; a teljes tanulmány még a `tematikus_lezart/`-ban él), tehát a „fájl létezik” nem jelzi a migrációt. Javaslat: motívumonként akkor esik ki a régi tanulmány, ha a `motivumok/[ID].md` fejlécében a #11 által bevezetendő jelző áll (pl. `migralt: igen`); a jelző a #11 hatásköre, addig **semmi sem esik ki**, és az építő a jelzőt hiányként kezeli (nem találgat). Alternatíva: a `motivumok.tsv` `forras_study` mezőjének üressé válása; ez a SEMA-mezőt terhelné, ezért nem javasolt. A `motivumok.tsv` `forras_study` mező a régi fájl → motívum-ID megfeleltetésének forrása (8 sor; a `TEREMT-002`-nek nincs); a `genezis/`, `ujszovetseg/`, `melyelemzesek/` fájlok motívumhoz nem rendelhetők (`motivum_id` üres, jelölve).

**(6) Új: a `Sir`/`JSir` könyvkulcs.** Az építő a Siralmak kulcsa: (a) **`Sir`** marad a KK-kulcs (a Károli, TAHOT, `karoli_strong/` szerint), a `Konyv_normalizalo_tabla` `JSir` kimenetét az építő explicit álnév-táblával `Sir`-re vezeti vissza és ezt a jelentésben megnevezi, vagy (b) a teljes vers-kulcs `JSir`-re vált (az adatréteg átírása, a #79 hatókörén kívül). Javaslat: (a).

**(7) Új: további `ellenoriz.py` SÉRTÉS-képes szabályok.** A `szabaly9…14` közül a SÉRTÉS-képesek (9., 10., 11., 13.) futnak-e az építéskor? Javaslat: igen, ha a mai állapot zöld (az ellenőr mai futása RENDBEN); ez a brief 1–8-át bővíti, ezért a felhasználó dönt.

**(8) Új: tartalmi méret-korlát a `strong_parok`-ra.** Mérés (TAHOT, grammatikai szűrő és H9xxx nélkül): 23 204 vers, 400 118 különböző pár, ebből `n ≥ 2` 146 148. Javaslat: a teljes pár-tábla bekerül (a 23. pont ritka együttállása éppen az `n` kis értékét keresi), az N13 küszöb a lekérdezésé, nem az építőé; a mérés a végső méretet adja.

## 6. Javasolt következő lépés

A felhasználó dönt a (1)–(8) pontokról (DT109). Ezután M1: az építő kis mintán, a tartalom-hash-sel, tételenként commitolva.
