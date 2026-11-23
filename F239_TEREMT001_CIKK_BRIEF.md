---
feladat: 239
cim: A tehóm (mélység) motívumcikke nulláról, az új lapgenerátorral
kod: TEREMT001_CIKK
tipus: feladat
fazis: 1
modell: opus
sav: CONTENT
allapot: fut
munka: ertelmezo
ad: a TEREMT-001 (tehóm — abüsszosz, a mélység) új cikke nulláról, egy kézből írt prózával, egyetlen kézi forrásból (`motivumok/TEREMT-001.md` + adattáblák), az új lapgenerátor előnézetén a szerkesztő által átnézve; az 1. kiadás a 218c (N243) után
kovetkezo: "Folytatás: az U1 (gépi adat-előkészítés, Sonnet) a befogadás után; a kimenet a naplok/F239_U1_TEREMT-001* fájlokba, utána átadó jegyzet"
olvas: [IRANY.md, MUNKAMENET.md, adat/SEMA.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/KESZ_LAP_KOVETELMENY.md, archivum/TEREMT-001/Tehom_tematikus.md, archivum/TEREMT-001/Tehom_kereszthivatkozas_naplo.md, "tematikus_lezart/TEREMT-001*", "tematikus_lezart/naplok/TEREMT-001*", motivumok/TEREMT-001.md, naplok/HATAR_TEREMT-001.md, naplok/TEHOM_JOB41_naplo.md, naplok/ELOSZURES_TEREMT-001.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/motivumok.tsv, adat/res_forras.tsv, adat/kapcsolatok.tsv, adat/tematikus_temak.tsv, adat/bdb_vers_jelentes.tsv, adat/forditasok.tsv, adat/grammatikai_strongok.tsv, genezis/1Moz_1v2-2v3_bovitett.md, genezis/1Moz_7v1-24_bovitett.md, genezis/1Moz_8v1-22_bovitett.md, eszkozok/lekerdez.py, eszkozok/jelolt.py, eszkozok/teljesseg_meres.py, eszkozok/motivum_felmeres.py, eszkozok/proza_lefedettseg.py, eszkozok/bizonyiteklap.py, eszkozok/tanulmany_kinyer.py, eszkozok/szerep_nave.py, eszkozok/glossza_lexikon_forditas.py, eszkozok/szakasz_cimke_levezet.py, eszkozok/motivum_hatar.py, eszkozok/visszhang/megfelelo_kinyer.py, eszkozok/visszhang/tanu_kinyer.py, eszkozok/proza_allitas.py, eszkozok/proza_1a.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, eszkozok/general.py]
ir: [motivumok/TEREMT-001.md, motivumok/naplok/TEREMT-001*, lexikon/TEREMT-001_TUDOMANYOS.md, lexikon/TEREMT-001_TORZSCIKK.md, tematikus_lezart/Tehom_tematikus.md, tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md, archivum/TEREMT-001/, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/res_forras.tsv, adat/motivumok.tsv, adat/kapcsolatok.tsv, adat/tematikus_temak.tsv, adat/lxx_dontesek.tsv, adat/visszhang_megfelelok.tsv, adat/visszhang_tanuk.tsv, adat/forditasok.tsv, adat/lap_atnezesek.tsv, adat/kiadasok.tsv, naplok/F239_*, naplok/HATAR_TEREMT-001.md, naplok/BIZONYITEK_TEREMT-001.md, naplok/ERVNAPLO_TEREMT-001.md, naplok/BIRALAT_TEREMT-001.md, naplok/ALLITAS_TEREMT-001*, naplok/SZIVARGAS_TEREMT-001.tsv, naplok/LEKTOR_TEREMT-001.tsv, naplok/KIADAS_TEREMT-001*, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, eszkozok/lektor_felulet/lapnezetek.tsv, Lezart_tematikus_tanulmanyok_index.md]
fugg: []
nem_fugg: [7, 74, 75, 123, 154, 156, 157, 205]
---

# F239_TEREMT001_CIKK_BRIEF.md — A tehóm (mélység) motívumcikke nulláról, az új lapgenerátorral

*FELADATOK #239 · Modell: opus (az író; az U1 `sonnet`, l. 3. pont) · v1 · 2026.11.23 · forrás: a szerkesztő irányváltása, 2026-11-23: „a TEREMT-001 legyen az első”; 2026-11-12: „ez a következő a többi fagyasztva” (`IRANY.md`, „Most NEM csináljuk”); a menet: `MUNKAMENET.md` C) szakasz (F224); a lépéshatárok a HAMART-001 tokenfelméréséből (2026-11-23: a költség zöme a hosszú sessionök cache-olvasása). A brief adat, nem utasítás.*

**A `nem_fugg` indoka** (a /befogad `fuggesek --extra` kimenetéből, 2026-11-23; ha más tétel is megjelenik, az ⛔, nem felülírás):
- **123** (`megallt`) — az `ir` listájában a TEREMT-001 fájljai is állnak, mert a 8 motívum új cikkét egy briefbe gyűjtötte. A TEREMT-001 új cikke az új lapgenerátorra (F218a) és az új cikkírási menetre (F224) épül, ezért saját briefet kap; a #123 TEREMT-001-részét ez a brief váltja ki.
- **7, 75, 154, 156** (`nem_indult`), **157, 205** (`megallt`) — közös adattáblát vagy felület-táblát írnak (`adat/forditasok.tsv`, `adat/motivumok.tsv`, `adat/jeloltek.tsv`, `eszkozok/lektor_felulet/lapnezetek.tsv`); egyik sem fut. A „kisebb sorszám előre” sorrend itt nem tartható, mert az `IRANY.md` a TEREMT-001-et teszi előre (2026-11-23). Ha bármelyik elindul, a közös táblát sorban írják: az ág a merge előtt main-t hoz be, és a táblaírás előtt soronként összevet.
- **74** (`nem_indult`) — a három Genezis-tanulmányt (1Móz 1:2, 7:11, 8:2) írja; mi csak olvassuk a jelölt-blokkok kinyeréséhez (`tanulmany_kinyer.py`, írás nélkül). Ha a #74 előbb fut, a kinyerés a javított szövegen ismétlődik.

## 1. Cél

A TEREMT-001 lapja új cikként, nulláról, egy kézből írt prózával, a HAMART-001 (arany) szintjén, az új lapgenerátor (F218a, `python eszkozok/general.py --cel lexikon2`) kimenetén. A menet lépéshatárokra bontva, minden határon átadó jegyzettel fut, hogy egyetlen session se olvassa újra fölöslegesen a teljes előzményt.

**Kiindulás** (mérve 2026-11-23, main `fe37880b`; scope=adat/*.tsv TEREMT-001 sorai | forras=split('\t') számlálás | ts=2026-11-23):
- `adat/elofordulasok.tsv`: 42 sor (H8415: 35, G0012: 7); `adat/jeloltek.tsv`: 44 sor (beépítve 42, elutasítva 2); `kapcsolatok`, `tematikus_temak`, `visszhang_megfelelok`, `visszhang_tanuk`, `lxx_dontesek`: 0 sor.
- `adat/res_forras.tsv`: 9 sor, hat a régi tematikus tanulmányra és a KH-naplóra mutat, az `alkalmazas` sor még áll (DT756 kivezette).
- `motivumok/TEREMT-001.md`: 4,8 KB archív kivonat, rés-jelölő nélkül. Az új generátor ezért ma nem fut rá: `B47: a(z) kivonat rés forrása (tematikus_lezart/Tehom_tematikus.md) nem a motívum kézi forrása` (a TEREMT-próba, F218 S9c, 2026-11-23).
- Nyitott: N58 (Jób 41:32, az 1/a-ból hiányzik).

## 2. Hatókör

**Benne:** a TEREMT-001 teljes cikk-menete az U1-től az előnézet jóváhagyásáig és az egy javítókörig; az 1. kiadás a 218c után (3. pont, U7).

**Nincs benne:**
- **a TEREMT-002** (fagyasztva, `IRANY.md`): adatához, forrásához, lapjához nem nyúlunk, a határkérdésben is csak hivatkozás (a két motívum határa a TEREMT-001 oldaláról dől el, a TEREMT-002 adata nem változik). Ha a TEREMT-001 határa a TEREMT-002 adatának változását kívánná: ⛔ az integrátornál.
- **a homonima-jelzés a jelöltlistán** (N228): a TEREMT-001-re nem kell (DT914; 2026-11-22: „a teremt re nem terjedhet ki az az új generátor próbája”).
- a BDB-lektor többi javaslata (N228), a lapgenerátor fejlesztése (218b, 218c, #236, #237), az olvasó.
- más motívum lapja.

**A kiadás feltétele.** Az új generátor a 218c-ig (N243) nem ad ki lapot (GK-27, DT933). A cikk addig az előnézetig jut (a szerkesztő átnézése és az egy javítókör megtörténhet), az 1. kiadás sora (`adat/kiadasok.tsv`) a 218c után íródik.

**Hatókör-szűkítés (DT-F221a).** A javítókör utáni újraellenőrzés célzott: a független ellenőr és a lektor a javítókör után csak a hibahely-táblát és a diffet nézi, nem olvassa újra a lapot. (a) Ellenőrzés nélkül marad: a javítás által a hibahelyen kívül okozott változás. (b) Méri helyette: a diff-kapu — a javítókör diffje csak a hibahely-tábla soraihoz tartozó forrássorokat érintheti; ha máshol is változik, arra a szakaszra teljes újraolvasás jár. Az első ellenőrzés (új lap) teljes.

## 3. Lépések (⛔ a kötelező megállások)

**Lépéshatárok és modellek.** Minden lépés a megnevezett szereplővel fut; a lépéshatáron átadó jegyzet készül (`naplok/F239_atado_<lépés>.md`: mi kész, mely fájlokban, a döntések hol állnak, mi a következő lépés bemenete, mit NEM kell elolvasni), és a következő lépés ebből indul.

| Lépés | Ki | Bemenet | Kimenet |
|---|---|---|---|
| U1 · gépi adat-előkészítés | külön, olcsóbb: `vegrehajto-sonnet` subagent vagy Sonnet-session | ez a brief, az adattáblák | `naplok/F239_U1_TEREMT-001*` (összesítő + TSV-k) |
| U1b · visszhang 1–2 kinyerése (C-vh) | Sonnet + másik kéz ellenőrzi (`adat/SEMA.md` 2.53 „Két kéz”) | az U1 lánc-szavai, láncversei | `adat/visszhang_megfelelok.tsv`, `adat/visszhang_tanuk.tsv` |
| U2 · határ és érvvázlat | Opus-session, új, az U1 átadójából | az U1 összesítője, a régi tanulmány célzott szakaszai | `naplok/F239_hatar.md`, `naplok/ERVNAPLO_TEREMT-001.md`, `naplok/BIRALAT_TEREMT-001.md`, `naplok/HATAR_TEREMT-001.md`, jelölt- és Nave-döntések |
| U3 · próza | egy Opus-session, egy menetben | az U2 átadója, a táblák | `motivumok/TEREMT-001.md` (kézi forrás), előnézet |
| U4 · ellenőrzés | friss subagentek (állítás-ellenőr, független ellenőr, lektor) | csak a megnevezett bemenet | `naplok/ALLITAS_TEREMT-001_itelet.md`, `naplok/F239_jelentes.md`, `naplok/KIADAS_TEREMT-001_lektor.md` |
| U5 · a szerkesztő átnézése | a szerkesztő, a lapnézeten | előnézet + lektori lista | `adat/lap_atnezesek.tsv` sor (csak a szó szerinti jóváhagyással) |
| U6 · javítókör | `/lap-javit TEREMT-001`, új session, azonos modell (Opus) | az U3 átadója, a kommentek, a hibahely-tábla | a javított forrás, változáslista |
| U7 · 1. kiadás | ⛔ a 218c után | — | `adat/kiadasok.tsv`, nyílt mag (E35) |

**A kontextus-plafon** (CLAUDE.md Munkamód 10.): kb. 150–200 ezer token kontextusnál csere teljes átadó jegyzettel, a végrehajtó subagenteknél is. Cikkírásnál a plafon a lépéshatáron érvényes, prózaírás közben nem: az U3 a prózát egy menetben végigírja, és csak utána cserél. Minden lépéshatáron átadó jegyzet; minden döntés indoklással azonnal fájlba (`naplok/F239_naplo.md`, tartalmi döntésnél `dontesek/uj/<ágnév>.md` helyőrzővel). Az „egy kéz” (K1) egy modell, amely az egész prózát olvassa, nem egy session.

**Takarékosság:**
- kevesebb forduló: a gépi lépések egy szkriptből futnak, a kimenet fájlba; a fő szálba csak összesítő és eltéréslista kerül;
- nagy fájlból csak a kellő szakasz (a régi tanulmány, a sablonok, a HAMART-001 mintalap: ebből csak a Kivonat-bekezdés és 2–3 arany 1/a-tétel);
- az ellenőr csak a hibahelyet nézi (a hatókör-szűkítés fent);
- a próza a táblákból készül (az U1 kivonatából és az adattáblákból), nem a régi prózából; a régi tanulmány alapanyag, mondat nem költözik belőle.

**Mérés** (kötelező, 2026-11-10: „a mérést ne felejtsük el”): lépésenként `get_usage` előtte és utána, modell, effort, idő, a futások és az ellenőrzések száma → `naplok/F239_meres.md`; a pontossági hibák a `naplok/SZIVARGAS_TEREMT-001.tsv`-be (`adat/SEMA.md` 2.72).

**Egyszerre egy lapgen-futás a gépen** (Munkamód 7.): minden `general.py --cel lexikon2` vagy teljes tesztkör előtt `python.exe`-lista; más session folyamatát soha nem állítjuk le. A próbák kimenete a repón kívülre (`--kimenet`).

### 0. Modell-ellenőrzés és előfeltételek
- Modell-ellenőrzés (CLAUDE.md): az író lépéseinél `opus`, az U1-nél és az U1b-nél `sonnet`; eltérésnél megállás.
- Ág: `claude/nervous-kare-9d2361`, egy PR a végéig; a session cserélhető.

### U1 — gépi adat-előkészítés (Sonnet; döntés nélkül)
Csak mér és listáz, jelentéstartományt nem választ, prózát nem ír, jelöltet nem dönt el. A kimenet `naplok/F239_U1_TEREMT-001.md` (összesítő, minden szakaszban proveniencia-sor; üres eredmény is naplózva) és a mellé tett TSV-k.
1. **A hét lépés determinisztikus része** a mai `pardes.db`-n (CLAUDE.md „Kutatási menet”): 1. gerinc-metszet (`adat/grammatikai_strongok.tsv` szűréssel; a gerinc levezetése üres eredménynél is dokumentálva); 3. teljes ÓSZ/ÚSZ scan (H8415, G0012); 4. kollokáció; 5. igealak-ellenőrzés; 6. LXX-híd (a H8415 versein az ἄβυσσος és a többi LXX-megfelelő; a G0012 nem-LXX ÚSZ-helyei). Minden sor nevezze meg, melyik gerinc-elemen lóg.
2. **Teljesség-mérés három hálóval** (`eszkozok/teljesseg_meres.py`; DT548): Strong-háló, a Károli szavainak hálója (`--karoli-szavak`: mélység, mélységek, örvény …, a jelöltlistát a szkript adja), a szótárak (BDB, Thayer) példahelyei. Az eltérés (a háló talál, az adat nem ismeri) a `adat/jeloltek.tsv`-be `nyitva` sorként, a háló nevével az indoklásban (2. szabály).
3. **Felmérő lekérdezés** (`eszkozok/motivum_felmeres.py TEREMT-001 --ki naplok/F239_U1_TEREMT-001_felmeres`) és **próza-lefedettség** mérésként (`eszkozok/proza_lefedettseg.py`).
4. **Bizonyítéklap** (`eszkozok/bizonyiteklap.py --motivum TEREMT-001`, C-bl) → `naplok/BIZONYITEK_TEREMT-001.md`.
5. **Igeszakasz-blokkok** (C-ia): mely `genezis/` (és egyéb) igeszakasz-tanulmányok tartalmaznak TEREMT-001-verset; a `eszkozok/tanulmany_kinyer.py` próbafutása `--ir` nélkül; a kinyerhető blokkok listája.
6. **Nave-jelöltlista** (`eszkozok/szerep_nave.py` `jeloltek()`) → `naplok/F239_U1_TEREMT-001_nave_jeloltek.tsv`, döntés nélkül.
7. **Fordítás- és szakaszcímke-lista**: `python eszkozok/glossza_lexikon_forditas.py lista --id TEREMT-001` (C-y), `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id TEREMT-001` (C-x; jelzésnél csak lista).
8. **LXX gépi megfelelők és BDB nyelvi háttér** (C-vh gépi része, `eszkozok/visszhang/megfelelo_kinyer.py lxx --motivum TEREMT-001`), írás nélkül, ha a lánc még nincs eldöntve.
9. **Határ gépi része** (`python eszkozok/motivum_hatar.py --motivum TEREMT-001 --kimenet <ideiglenes>`), a jelentés az összesítőbe.
10. **A régi adat alakja az új generátorhoz**: a `jeloltek.tsv` TEREMT-001-sorainak `forras_kereses` alakja (a TEREMT-002-n a régi `scan H…` alak B04-et adott); a `res_forras.tsv` sorai, amelyek nem a kézi forrásra mutatnak; az N58 (Jób 41:32) állapota. Csak lista; a javítás az U3 technikai része.

Az U1 végén átadó jegyzet: `naplok/F239_atado_U1.md`.

### U1b — a visszhang 1 és 2 kinyerése (Sonnet + másik kéz)
A C-vh sor szerint, a próza előtt: Targum, Vulgata, a tanúréteg; két kézzel, soronkénti átnézés-bemenettel (`adat/SEMA.md` 2.53, 2.57). A lánc (lánc-szavak, láncversek) az U2 döntése után véglegesedik; ha a lánc az U2-ben változik, a hiányzó párok kinyerése pótlódik. A visszhang 1 és 2 az 1. kiadás feltétele.

### U2 — határ és érvvázlat (Opus, új session az U1 átadójából)
1. **A négy ID-kérdés és a kizárások** (CLAUDE.md „Új motívum-ID kiosztása”): az azonosság hordozója, a negatív kritérium, a funkció-kérdés két motívumnál, a részhalmaz-kérdés; a fölérendelt fogalom (ma: „vízi/kozmikus káosz-képzetek általában, a tehóm / abüsszosz lexémán kívül”). A határt a kizárások rajzolják meg. A válasz és minden kizárás indoklással azonnal `naplok/F239_hatar.md`-be.
2. **Az U1 `nyitva` jelöltjeinek döntése** (`jeloltek.tsv`, döntéssel és indoklással). Tartalmi kérdés (határ, gerinc-elemet érintő eltérés, mi kerül a lapra) ⛔ az integrátornál, egy olvasói mondattal.
3. **A határ-ellenőrzés** (C-h): a gépi rész után a `hatar-ellenor` subagent (Sonnet, friss), a próza előtt, mert a határt és a prózát egy kéz viszi; a kérdések a `naplok/HATAR_TEREMT-001.md` „Modelles rész” szakaszába.
4. **Érvvázlat és érvnapló** (C-ev, `naplok/ERVNAPLO_TEREMT-001.md`), utána a **bíráló** (C-bi, `biralo` subagent, friss) → `naplok/BIRALAT_TEREMT-001.md`.
5. **Nave-döntések** (`adat/tematikus_temak.tsv`: `kivalasztott` / `kizart` / `tiltott`, indokkal; a mérce a funkció; a `tiltott` a fölérendelt fogalom felé hígítana). Üres Nave-blokkal a cikk nem adható ki.
6. Átadó jegyzet: `naplok/F239_atado_U2.md`.

### U3 — a próza (egy Opus-session, egy menetben)
- A `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md` promptja, a `sablonok/9_PaRDeS_motivum_forras_sablon.md` formája; az új kézi forrás a `motivumok/TEREMT-001.md`, rés-jelölőkkel; a `res_forras.tsv` sorai a kézi forrásra kötve (a B47 megszűnik), az `alkalmazas` sor kivezetve (DT756).
- **Az 1/a minden igehelye kerek mondat + „Funkció:” sor**; a Kivonat a két határ-elemmel; az olvasói szöveg az adatból indul, és levonja a következtetést; belső jel (DT-, N-, F-szám, `.tsv`, „gerinc”) az olvasói rétegben nincs.
- A régi tanulmány, a KH-napló, a régi `motivumok/TEREMT-001.md` és a törzscikk `archivum/TEREMT-001/` alá, ARCHÍV fejléccel (nem törlés), a hivatkozások ugyanabban a commitban (E27).
- Az előnézet: `python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <repón kívül>` (előtte `python.exe`-lista).
- A próza után cserél a session, átadó jegyzettel (`naplok/F239_atado_U3.md`).

### U4 — ellenőrzés (friss subagentek)
- **F1/F2**: `python eszkozok/proza_allitas.py TEREMT-001`, utána az `allitas-ellenor` subagent; az ítélet `naplok/ALLITAS_TEREMT-001_itelet.md`. Ez a **független F2-mérés** (DT881: a következő új motívum cikkírásakor; a küszöb 80%).
- **Gépi kapuk** a generált lapon (C-g, C-o): `ellenoriz.py` 24. és 25. szabály, `proza_1a.py TEREMT-001 --reszletes`, olvasói kapu 0 BUKÁS, a próza-lefedettség üres vagy indokolt. Bukásnál a próza gazdája javít.
- **Független ellenőr** (`fuggetlen-ellenor`, friss) a base..head diffen → `naplok/F239_jelentes.md`.
- **Lektor** (`/kiadas` 1–3. lépése, `lektor` subagent, friss): csak a jelölt helyeket olvassa, listát ad, nem javít.
- A Fable-modellű szerepek (lektor, független ellenőr) előtt keret-ellenőrzés (`get_usage`).
- **Olvasói átolvasás** (`/kiadas` 3/b, DT824; az integrátor döntése, 2026-11-23): minta-kapu a renderelt lapon (0 találat), friss kontextusú olvasó a teljes renderelt lapon (az új generátor előnézetéből; brief és döntéslista nélkül, a generált blokkokkal együtt), a `naplok/HIBA_MECHANIZMUSOK.md` lapot érintő nyitott mechanizmusai ellenőrizve; a lista a `naplok/KIADAS_TEREMT-001_lektor.md`-be, nyitott tételként az U5-be.

### U5 — ⛔ a szerkesztő átnézése
A renderelt előnézet (lapnézet, privát artifact, világos téma) a lektor listájával; a lektor (U4) listája a lapnézettel együtt, **nyitott tételként** kerül a szerkesztő elé, az egyetlen felület a lapnézet; lezárt lektortétel nem megy vissza hozzá (az integrátor kiegészítése a befogadáskor, 2026-11-23, a 2026-11-23-i döntés szerint). A szerkesztő tételenként dönt; a jóváhagyás szó szerint, dátummal (`naplok/F239_atnezes_TEREMT-001.md`, `adat/lap_atnezesek.tsv`).

### U6 — egy javítókör
`/lap-javit TEREMT-001`, új session, azonos modell (Opus), az U3 átadójából; a hibahely-tábla és a diff-kapu (2. pont) szerint; utána a gépi kapuk újra zöldek, a szerkesztő a változáslistát nézi. Ami ezután derül ki, a 2. kiadásé.

### U7 — ⛔ 1. kiadás (a 218c után)
A 218c (N243) lezárásáig nem fut (GK-27, DT933). Utána: „Kiadható-e az 1. kiadás?” — a szerkesztő szavával `/kiadas` 5. lépés, `motivumok.tsv` verzió-emelés, nyílt mag (`nyilt_mag_export.py`, E35 0 BUKÁS).

## 4. Elfogadási feltételek
1. Az U1 összesítője a 10 pontjával, proveniencia-sorral; a teljesség-mérés minden eltérése a `jeloltek.tsv`-ben döntéssel.
2. A határ (négy kérdés, kizárások) a `naplok/F239_hatar.md`-ben; a határ-ellenőrzés a próza előtt lefutott.
3. Az 1/a minden igehelye arany szintű (`proza_1a.py TEREMT-001 --reszletes`: 0 nem arany); az N58 lezárva vagy indokolt.
4. `ellenoriz.py`: SÉRTÉS 0; olvasói kapu 0 BUKÁS; a Nave-blokk nem üres; a visszhang 1 és 2 kész.
5. Az F2 független mérése rögzítve; a mérőtábla és a lépésenkénti mérés kitöltve.
6. A szerkesztő átnézése rögzítve; egy javítókör lefutott.
7. Minden lépéshatáron átadó jegyzet; a próza egy kézből, Opus-modellel.
8. `python eszkozok/feladatok.py ellenoriz` 0 hiba; E27 zöld; a független ellenőr jelentése a `naplok/F239_jelentes.md`-ben.
9. Az 1. kiadás (U7) a 218c után; addig a brief `fut`, a `kovetkezo` mezője a 218c-re vár.

## 5. Döntésnapló
A menet döntései helyőrzővel a `dontesek/uj/nervous-kare-9d2361.md`-be, indoklással; a lépésnapló `naplok/F239_naplo.md`.
