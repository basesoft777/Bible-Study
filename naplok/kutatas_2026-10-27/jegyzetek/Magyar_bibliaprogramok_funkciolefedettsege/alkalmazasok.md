# Magyar nyelvű funkciólefedettség – bibliatanulmányozó alkalmazások

Gyűjtés: 2026-10-27. Nyers letöltések: `/tmp/claude-0/-home-user-Bible-Study/40fb57d0-f061-5709-acdb-32b11a763cea/scratchpad/forras/appok/` (49 fájl: Google Play, App Store, bible.com, logos.com, andbible.org, F-Droid és szentiras.hu oldalak).

**A bizonyosság jelölése** (minden cellában):
- **[L]** = az oldalt láttam, és ott ez áll (letöltve, a mentett fájlban visszakereshető)
- **[S]** = csak keresési kivonatból (WebSearch); az oldal nem volt elérhető vagy nem töltöttem le
- **[R]** = a referenciaprojekt repójának korábbi kutatása (`ADATVAGYON_TERV.md`, `konkordancia/*README.md`); most nem ellenőriztem újra
- **[E]** = általános előismeret; nem ellenőriztem. Gyenge, csak tájékoztató
- **?** = ismeretlen. Nincs adat, és ezt nem töltöttem ki feltételezéssel

**Nem elérhető források** (nem kerültem meg őket): bible-discovery.com, mobilbiblia.hu (proxy: connect_rejected), arcanum.com, stepbible.org (Cloudflare 403 „Attention Required”), crosswire.org / ftp.crosswire.org (proxy 403), search.f-droid.org, GitHub API a `krisek/HunKar` repóhoz (a session nem fér hozzá).

---

## 1. Fő mátrix (oszlop = program, sor = funkció)

Rövidítések: **BD** = Biblia-Felfedező / Bible-Discovery (SQL Uniform Kft., Zsidó Miklós) · **YV** = YouVersion (Life.Church) · **STEP** = STEPBible (Tyndale House) · **LOG** = Logos (Faithlife) · **AB** = AndBible (SWORD/CrossWire) · **MyB** = MyBible (Denys Dolganenko) · **SZI** = szentiras.hu webes felülete és „Szentírás” Android-appja (Gyurász Krisztián) · **BOK** = BibOlKa és Károli-Biblia (Wallner Ádám / Gutta Cavat Kft.) · **MRE** = Bibliapp (Magyarországi Református Egyház)

| # | Funkció | BD | YV | STEP | LOG | AB | MyB | SZI | BOK | MRE |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Magyar fordítások | ✅ [L] Károli 1908, Károli-Strong (HUN), UF 1975/1990, SZIT 1973/2003, KNB 1997, Békés–Dalos és még kb. 12 régi ÚSZ, SZPA; RÚF 2014 a listában **nincs** | ✅ [L] HUNK (Károli 1908, MBT), HUNB (UF 1990), RÚF 2014 (hanggal), EFO 2012, CSIA, EIV (ÚSZ); SZIT és KNB nincs | részben [S] HunKAR (Károli, a STEP konvertálta); más ? | részben [L] egyetlen modul: „Szent Biblia (Hungarian Károli Bible)” | ✅ [L] Károli 1908 rev., UF 1990, RÚF 2014, Káldi-Neovulgáta | ? [S] a ph4.org egy „KB 1964” Károli-modult listáz | ✅ [L] SZIT, KNB, RÚF, KG (rev. Károli), UF, BD, Káldi, IMIT, STL, Neovulgata, Vulgata; app: 6 fordítás | ✅ [L] rev. Károli 2011 (Veritas), UF 1990, Károli 1908 | ✅ [L] Károli + RÚF |
| 2 | Strong-szám a magyar szövegben (szószinten) | ✅ [L/S] „Károli Gáspár Biblia – Strong számokkal (HUN)”; a szószintű megjelenítés fizetős modul [S]; az ÓSZ párosítása elkészült [S], a repó szerint könyvenként készült [R]; a szöveg részben modernizált [S] | ❌ nincs nyoma [L, verzióoldalak] | ❌ [S] a magyar nincs a 21 interlineáris Biblia között (régebbi oldal) | ❌ [L] a termékoldal nem említ reverse interlineárist | ❌ [R] a HunKar OSIS-forrásban nincs Strong | ? | ❌ nincs nyoma [L] | ❌ | ❌ |
| 3 | Interlineáris (héber/görög + magyar) | ? | ❌ | részben [S/E]: eredeti nyelv + angol, magyar nincs | részben [E]: angol, magyar nincs | részben [L]: osztott ablak szinkron görgetéssel, nem szószintű | részben [L]: eredeti szövegű modulok, a magyar párosítás ? | részben [L]: héber (Leningrádi) és görög (Rahlfs LXX + WH) szöveg fejezetszinten, nem szószintű | ❌ | ❌ |
| 4 | Morfológia | részben [L]: csak az angol KJV, AKJV és BBE modulon (iOS-leírás); magyaron ? | ❌ | ✅ az eredeti szövegen, angolul [E] | részben, angolul [E] | részben [L]: „Strong's numbers, morphology” a taggelt (nem magyar) modulokon | ? | ❌ | ❌ | ❌ |
| 5 | Héber szótár magyarul | ✅ [S] Óhéber–Magyar Gesenius (Strong_HU_HEB, Grüll Tiborné, 2011) és Óhéber–Magyar BDB (Strong_HU_HEB2); iOS: 6 990 Ft [S] | ❌ | ❌ angol [E] | ❌ | ❌ angol Strong-szótár [L] | ? (a Strong-lexikon nyelve ?) | ❌ | ❌ | ❌ |
| 6 | Görög szótár magyarul | ✅ [S] Újszövetségi Ógörög–Magyar Szótár (Strong_HU), 2. kiadás (Strong_HU2, Tóth Eszter lektorálta); iOS: 6 990 Ft [S] | ❌ | ❌ | ❌ | ❌ | ? | ❌ | ❌ | ❌ |
| 7 | Konkordancia eredeti szó (Strong) szerint, magyar találatokkal | ✅ [L] keresés és szóelemzés Strong-számra; a program alcíme „konkordancia program” [S] | ❌ | ❌ magyarul (angolul ✅ [E]) | ❌ magyarul | ❌ magyarul (Strong-keresés csak taggelt modulban) | ? | ❌ | ❌ | ❌ |
| 8 | Magyar szó- és kifejezéskeresés | ✅ [L] | ✅ [E] | ? | ? | ✅ [L] teljes szöveges, több fordításban | ✅ [E] | ✅ [E] (web) | ✅ [L] szóra és szótöredékre, ÓSZ/ÚSZ szűréssel | ? |
| 9 | LXX és héber–görög kapcsolat | ? | ❌ | részben [E]: van LXX; kapcsolat ? | részben [E]: fizetős angol modulok | ? (CrossWire LXX-modul ?) | részben [L]: ógörög szövegek; kapcsolat ? | részben [L]: Rahlfs LXX szövegként; kapcsolat ❌ | ❌ | ❌ |
| 10 | Kereszthivatkozások | ✅ [L] „kereszthivatkozási rendszer”; külön modul, 2 000 Ft (régi PC-ár) és 4 990 Ft (iOS) [S]; a repó szerint Nave-alapú [R] | ? | ? | részben, angol TSK stb. [E] | ✅ [L] TSKe; a HunKar-modul a Károli-margó utalásait hordozza [R] | ✅ [L] saját és felhasználói | részben: a Károli-margó utalásai [R]; jegyzet- és hivatkozásgomb [L] | ❌ | ❌ |
| 11 | Tematikus vagy motívumindex | részben [R]: Nave-alapú rendszer; motívumindex ❌ | részben [L]: olvasási tervek, nem index | részben [E]: Nave és Torrey témakeresés, angolul | részben, angol [E] | ? | ? | ❌ | ❌ | ❌ |
| 12 | Magyar exegetikai vagy lexikon-szócikk (motívum- vagy fogalomszinten) | részben: csak lexikai szótár-szócikk [S]; Matthew Henry-kommentár (a HU-leírásban nyelv nélkül, az iOS-en „in English”) [L]; motívumszint ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (csak fordítói lábjegyzet) | részben [L]: Bibliaolvasó Kalauz-magyarázatok (áhítati) | részben [L]: Bibliaolvasó Kalauz |
| 13 | Proveniencia, dokumentált kapcsolódási döntések | ❌ nincs nyoma | ❌ | ❌ (az adatforrás dokumentált, a kapcsolódási döntés nem) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 14 | Nyílt licenc, letölthető adat, DOI | ❌ [S] a szótár és a Károli-párosítás „Zsidó Miklós tulajdona”; zárt [R] | ❌ a szövegek kiadói védelem alatt | ✅ [R] a STEPBible-Data CC BY 4.0; DOI ? | ❌ | részben [L]: az app GPL-3.0; a HunKar Public Domain [R]; a többi modul licence vegyes | ? | részben [L]: a héber és görög szöveg Public Domain; a magyar fordítások védettek; van API [S] | ❌ | ❌ |
| 15 | Offline használat | ✅ [L] „offline Biblia” | részben [L]: „bizonyos verziók” letölthetők | részben [E]: asztali változat | ✅ [E] asztali | ✅ [L] | ✅ [L] | app ✅ [L]; web ❌ | ✅ [L] (a hangoskönyvhöz net kell) | ? |
| 16 | Platform | Android, iOS [L]; Windows, Linux, macOS [S] | web, Android, iOS [L] | web [L], asztali [E] | web, asztali, Android, iOS [L] | Android, iOS [L] | Android [L] | web, Android [L] | Android [L] | Android [L], iOS [S] |
| 17 | Ár | ingyenes alap, IAP 1 290–9 899 Ft (Play) [L]; iOS-modulok 4 990–6 990 Ft, 6 modul csomagban 19 990 Ft [S] | ingyenes [L] | ingyenes [S] | app ingyenes, hirdetéssel és IAP-pel [L]; a magyar Károli 13,99 USD [L]; előfizetés [L] | ingyenes, hirdetés nélkül [L] | ingyenes [L, a fejlécben nincs IAP] | ingyenes [L] | ingyenes [L] | ingyenes [L] |
| 18 | Telepítés, utolsó frissítés | Play: 1 M+ (1 099 221), 4,9★ / 9,99 E értékelés, 2026-10-13; iOS: 11.7.1 (2026-10-14), 593 értékelés, Tudástár #51 [L]; megjelent 2011-01-27 | Play: 100 M+, 9,34 M értékelés, 2026-10-16 [L] | ? (nincs boltadat) | Play: 1 M+, 56,9 E értékelés, 2026-10-19 [L] | Play: 500 E+ (633 694), 4,6★ / 7,86 E, 2026-09-05; F-Droid 5.1.1117 [L] | Play: 1 M+, 44,2 E, 2026-04-19 [L] | app: 10 E+ (31 370), 4,9★ / 2,25 E, 2026-07-22 [L] | BibOlKa: 50 E+ (83 636), 2025-10-28; Károli-Biblia: 10 E+ (49 994), **2020-01-04** [L] | 10 E+ (18 078), 2026-08-10 [L] |

**Felület magyarul?** BD ✅ [L] (az iOS-changelogban „Fixed UI translations: … Hungarian”). YV ✅ [L] (több mint 40 felületnyelv, a Play-leírás magyar). STEP ? [S] (59 felületnyelv; a magyart nem tudtam ellenőrizni). LOG ❌ [L] (a webhely nyelvválasztója EN, ES, PT, FR, DE, KO, zh). AB ✅ valószínű [L] (magyar F-Droid-leírás; a felületet nem láttam). MyB ? (a Play-leírás magyar, gépi fordításnak tűnik).

---

## 2. Programonkénti jegyzetek

### 2.1 Biblia-Felfedező / Bible-Discovery (`com.biblediscovery`, iOS `id1155806176`)
- **Fejlesztő:** SQL Uniform Kft. [L]. A szótár és a Károli-párosítás jogtulajdonosa Zsidó Miklós [S, bible-discovery.com szótároldal kivonata].
- **Magyar fordítások:** a Play/App Store HU-leírás teljes listája [L]: Károli Biblia, Aranyos Biblia (1685), Budai Gergely ÚSZ (1967), Békés–Dalos ÚSZ (1951), Csia Lajos ÚSZ (1978), Czeglédy Sándor ÚSZ (1924), Egyszerű fordítás ÚSZ (2003), Károli Gáspár (1908), Kecskeméthy István (1935), Káldi Neovulgata (1997), Masznyik Endre ÚSZ (1925), Protestáns Újfordítású Biblia (MBT, 1975, 1990), Raffay Sándor ÚSZ (1929), Ravasz László ÚSZ (1971), Soós István (1911), Szent István Társulat (1973, 2003), Vida Sándor ÚSZ (1971), SZPA (Szent Pál Akadémia; „nem publikus, de feltételekkel elérhető”). A **RÚF 2014 nincs a listában**.
- **Strong-párosított magyar szöveg:** „Károli Gáspár Biblia – Strong számokkal (HUN)” [L]. A keresési kivonatok szerint [S]:
  - a szöveg a Károli részben modernizált, igeragozásában korszerűsített változata, és átdolgozás alatt áll;
  - a mobilbiblia.hu verziótörténete szerint az ÓSZ párosítása szakaszosan készült, és „minden könyv párosítva lett” (a Strong-párosítás első szakasza lezárult);
  - lejárt próbaidő után a Strong-számok csak a versek végén jelennek meg, tehát a szószintű megjelenítés fizetős.
  A repó 2026-10-03-i állapota szerint az ÚSZ kész és lektorált, az ÓSZ könyvenként készül [R]. Ez a két állítás feszültségben van, a mai teljességet nem tudtam ellenőrizni.
- **Magyar szótárak** [S, bible-discovery.com és mobilbiblia.hu kivonatok]:
  - Strong_HU_HEB: Óhéber–Magyar Gesenius (Gesenius Hebrew and Chaldee Lexicon alapján, dr. Grüll Tiborné Eszter, 2011);
  - Strong_HU_HEB2: Óhéber–Magyar BDB;
  - Strong_HU: Újszövetségi Ógörög–Magyar Szótár;
  - Strong_HU2: ugyanennek 2. kiadása, dr. Tóth Eszter lektorálta és egészítette ki.
- **Egyéb** [L]: kereszthivatkozás-rendszer, párhuzamos olvasás, kb. 1000 helyes bibliai térkép, Matthew Henry-kommentár, olvasási tervek, „Biblical Meditation”, jegyzetek. A 2026-os iOS-changelog szerint a fejlesztő maga Strong-párosította az AKJV-t és a BBE-t („our own work”). Interlineáris nézetnek és LXX-modulnak a forrásokban nincs nyoma; ezek **?**, nem ❌.
- **Ár:**
  - Play: „1 290 Ft – 9 899 Ft” IAP [L].
  - iOS [S, App Store-kivonat]: Óhéber BDB 6 990 Ft, Ógörög–Magyar 2. 6 990 Ft, kereszthivatkozás-rendszer 4 990 Ft, 6 modul 19 990 Ft.
  - Régi PC/Mac-rendelőlap [S]: kereszthivatkozás-modul 2 000 Ft, térképmodul 3 000 Ft.
- **Elterjedtség:** az egyetlen jelentős telepítésszámú magyar fejlesztésű tanulmányozó app (Play: 1 099 221 telepítés, megjelent 2011-01-27). A „Biblia”, „Szentírás”, „Bibliaolvasó”, „Strong szám Biblia” és „Szent István Társulat” Play-keresésben is szerepel [L].
- **Viszony a referenciaprojekthez:** a repó szerint a BD Károli-párosítása zárt, ezért nem forrásjelölt (DT: kizárva) [R].

### 2.2 YouVersion (`com.sirma.mobile.bible.android`, bible.com)
- **Magyar verziók** [L, bible.com/languages/hun]: EFO (2012, Bible League), CSIA, HUNK (Károli 1908, „Revideált Károli fordítás (1908)”, Magyar Bibliatársulat Alapítvány), HUNB (MBT UF), RÚF (Revideált Új Fordítás 2014, hanggal), EIV (ÚSZ, Biblica). Összesen 6.
- **Funkciók** [L, Play HU-leírás]: olvasási tervek, kiemelés, jegyzet, több mint 40 felületnyelv, „bizonyos verziók” offline. Strong-, interlineáris és lexikonfunkciónak nincs nyoma.
- **Elterjedtség:** 100 M+ telepítés (globális) [L]. A magyar felhasználók számára nincs külön adat.

### 2.3 STEPBible
- A stepbible.org Cloudflare-blokkot ad (403); csak keresési kivonat volt [S].
- A HunKAR verzióoldala létezik („Hungarian Karoli Translation (KAR) TH'Mar-19”; a STEP konvertálta Sword-modullá). A kivonat Strong-taggelést nem említ, és régen indexelték.
- Interlineáris kijelzés „21 Bibliában (ESV, kínai, cseh, spanyol…)”; a magyar nincs a felsorolásban (régebbi oldal).
- A felület 59 nyelvű; hogy van-e magyar, az **?**.
- A STEPBible-Data a repó szerint CC BY 4.0 [R].

### 2.4 Logos
- **Termék** [L, logos.com/product/1834]: „Szent Biblia (Hungarian Károli Bible)”, Faithlife 2007, 13,99 USD. A leírás az 1590-es vizsolyi kiadást említi; a ténylegesen digitalizált kiadás nem derül ki. Reverse interlineárist nem említ.
- **Kivonatokból** [S]:
  - egy vásárlói vélemény szerint „ő/ű” helyett „õ/ũ” jelenik meg;
  - a Logos munkatársa a fórumon „ancient” (régi) erőforrásnak nevezte;
  - a RÚF 2014-et és az ÚRK-t a felhasználók kérik, de nincs meg.
- **Felület:** nincs magyar [L].
- **Play:** 1 M+, hirdetéssel és IAP-pel, előfizetéses MI-funkciók [L].

### 2.5 AndBible (`net.bible.android.activity`)
- **F-Droid HU-leírás** [L]: Károli 1908-as revíziója, MBT UF 1990 és 2014, Káldi-Neovulgáta. Strong-konkordancia (görög és héber szóanalízis), TSKe, Gill- és Henry-kommentár, teljes szöveges keresés, szinkronizálás, opcionális MI-asszisztens (saját API-kulccsal), kb. 1500 mű 700 nyelven (CrossWire és más SWORD-tárak). A MyBible-, MySword- és EPUB-formátumot is kezeli.
- **andbible.org** [L]: GPL-3.0, „Open source · No ads · No tracking”, Android és iOS.
- **Magyar Strong:** nincs. A HunKar forrása (krisek/HunKar OSIS) a repó README-je szerint nem tartalmaz Strong-adatot, a kereszthivatkozásokat viszont igen [R].

### 2.6 MyBible (`ua.mybible`)
- **Play-leírás** [L]: Strong-számok, Strong-lexikon dupla érintésre, Strong-szám szerinti keresés („szimfónia”), kereszthivatkozások. Az „orosz” és a „szabványos” zsoltárszámozás megfeleltetése beépített (ez az egyetlen versszámozás-kulcs a vizsgált programok közül, de nem Károli↔MT↔LXX).
- **Magyar Strong-modul:** nem találtam [S]. A ph4.org kivonata egy Károli „KB 1964” modult listáz, Strong nélkül.

### 2.7 szentiras.hu és „Szentírás” app (`eu.gyurasz.bible`)
- **Web** [L, szentiras.hu főoldal, a Szent Jeromos Katolikus Bibliatársulat oldala]: heb (Leningrádi kódex, PD), bgt (Rahlfs LXX + Westcott–Hort, PD), neo, vuc, knb, szit, ruf, kg, imit, kaldi, bd, stl. A fejezetszöveg JS-ből töltődik, ezért a funkciókat csak részben láttam. A forrásban nincs „strong”, „lemma” vagy „morph” szó [L negatív].
- **App** [L]: „A szentiras.hu android-os változata”, offline (első indításkor adatbázis-import). Fordításai: SZIT, UF 1990, KNB, Károli revideált, Békés–Dalos, RÚF 2014.
- **Szent István Társulat:** külön SZIT-appot nem találtam a Play-keresésben [L negatív]. A SZIT digitálisan a szentiras.hu-n és a BD-ben érhető el.

### 2.8 Kisebb magyar olvasóappok (Play [L], 2026-10-27)

| App (csomagazonosító) | Fejlesztő | Telepítés (pontos) | Frissítve | Ár | Tartalom |
|---|---|---|---|---|---|
| BibOlKa – Bibliaolvasó kalauz (`hu.bitbaro.bibolka`) | Wallner Ádám | 50 E+ (83 636) | 2025-10-28 | ingyenes | rev. Károli 2011, UF 1990, Károli 1908; Bibliaolvasó Kalauz; szó- és töredékkeresés; offline |
| Károli-Biblia (`hu.bitbaro.karoli2011`) | Gutta Cavat Kft. | 10 E+ (49 994) | 2020-01-04 | ingyenes | rev. Károli 2011; ÚSZ-hangoskönyv; keresés; offline |
| BibOlKAT (`hu.bitbaro.bibolkat`) | Wallner Ádám | 10 E+ (16 478) | 2025-10-28 | ingyenes | katolikus igenaptár |
| Bibliapp (`hu.webter.bibliApp`) | Magyarországi Református Egyház | 10 E+ (18 078) | 2026-08-10 | ingyenes | Károli, RÚF, Énekeskönyv, Bibliaolvasó Kalauz, hitvallások |
| Szentírás (`eu.gyurasz.bible`) | Gyurász Krisztián | 10 E+ (31 370) | 2026-07-22 | ingyenes | l. 2.7 |
| Biblia Magyarul (`com.martinvillar.android.hungarianbible`) | Seconda Variante | 50 E+ (92 117) | 2026-10-15 | hirdetéssel; PRO 2 899 Ft (319 telepítés) | olvasási tervek, több mint 100 téma (versválogatás), keresés; a fordítás neve nincs a leírásban |
| Szent Biblia (Holy Bible) (`com.solvus_lab.android.BibleHU_karoli`) | Solvus Lab | 50 E+ (55 041) | 2025-12-07 | hirdetéssel | Károli; szó- és kifejezéskeresés |
| Szent Biblia – Hang és offline (`com.livingbible.app`) | SuperWolf | 50 E+ (50 028) | 2026-10-24 | IAP 1 490–42 499 Ft | hangos Biblia, „Jézus Magyarázza” tanítások; a fordítás ? |
| Biblia Magyarul (`hungarian.bible`) | Alkitab | 10 E+ (36 900) | 2026-07-29 | hirdetéssel, IAP 439 Ft | olvasó; a fordítás ? |
| Szent Biblia – Hangoskönyv (`com.murati.audiobook.bible.hu`) | murati.hu | 10 E+ (12 749) | 2025-08-20 | hirdetéssel | Károli hangoskönyv |
| Biblia Magyarul (`com.skyraan.bibliamagyarul`) | Oly Bible | 5 E+ | 2026-06-15 | hirdetéssel és IAP-pel | olvasó |
| Hit Gyülekezete (`com.hit.hitgyulekezete`) | Hit Gyülekezete | 10 E+ (16 322) | 2026-02-11 | támogatói előfizetés | **nem bibliaprogram**: prédikáció- és dicséretarchívum, Hit Magazin |
| Napi evangélium (görkat.) (`hu.gerner.napiolvasmanyok`) | Gerner Attila | 1 E+ (4 765) | 2026-08-21 | ingyenes | liturgikus napi olvasmány |
| Magyar Bibliatársulat (iOS `id444815381`) | Faith Comes by Hearing (Subsplash) | ? | **2017-05-24** | ingyenes | olvasás, hallgatás, hírek; 1,8★; gyakorlatilag elhagyott [L] |
| Revised Hungarian Bible (Audio) (iOS `id1173315254`) | siriwit nambutdee | ? | ? | ingyenes | RÚF hanggal; nem hivatalos kiadó [L] |

E tábla egyik appja sem tud Strong-számot, interlineárist, szótárat vagy LXX-et (a leírások alapján [L]). A 2–14. funkciókban mind ❌, kivéve a magyar keresést és az offline használatot.

---

## 3. Következtetések a mátrixhoz

1. **A szószintű magyar Strong-párosítás és a magyar héber/görög szótár ma egyetlen programban van meg: a Biblia-Felfedezőben** [L/S]. Ez zárt (a jogtulajdonos Zsidó Miklós), és a szószintű megjelenítés fizetős modul. Nyílt magyar Strong-párosítást vagy magyar BDB-t/Thayert más programban nem találtam (nem kimerítő keresés; egyezik a repó 2026-10-03-i megállapításával [R]).
2. **A nemzetközi platformok (YouVersion, Logos, AndBible, MyBible, STEP) magyarul csak olvasószöveget adnak.** Az eredeti nyelvű eszközeik (Strong, morfológia, lexikon) angol vagy taggelt angol szövegre épülnek. A Logos egyetlen magyar Bibliája régi, karakterhibás Károli [L/S].
3. **A magyar fejlesztésű appok** (BibOlKa, Károli-Biblia, Szentírás, Bibliapp, a „Biblia Magyarul”-klónok) olvasóprogramok: keresés, könyvjelző, áhítati kalauz, hangoskönyv. Tanulmányozóeszközük nincs.
4. **Egyik vizsgált program sem kínál:**
   - motívumszintű vagy fogalmi magyar lexikont;
   - dokumentált, indokolt kapcsolódási döntést (provenienciát);
   - Károli↔MT↔LXX↔KJV versszámozás-kulcsot (a MyBible csak az orosz és a szabványos zsoltárszámozást feleltet meg [L]);
   - DOI-val idézhető nyílt magyar adatot.
   A nyílt licencű elemek (AndBible GPL-3.0, STEPBible-Data CC BY 4.0, a szentiras.hu PD héber és görög szövege) nem magyar tanulmányozóadatok.
5. **Az LXX** a szentiras.hu-n szövegként elérhető (Rahlfs) [L]. Héber–görög szószintű kapcsolatot magyar felületen egyik program sem mutat (nincs nyoma).

## 4. Nyitott és ellenőrizetlen pontok
- A BD Károli-Strong ÓSZ-ének mai teljessége: a mobilbiblia.hu kivonata („minden könyv párosítva”) és a repó R-állítása („könyvenként készül”) eltér. A bible-discovery.com és a mobilbiblia.hu nem volt elérhető.
- A BD interlineáris nézete, LXX-modulja és a kereszthivatkozás-rendszer forrása (a Nave-alap csak [R]).
- A STEP magyar felülete, és hogy van-e a HunKAR-nak taggelése.
- A HunKar CrossWire-modul aktuális `.conf`-ja (a CrossWire nem volt elérhető).
- A YouVersion magyar verzióinak offline letölthetősége verziónként.

## 5. Források (URL-ek)
- Google Play (a nyers HTML a `forras/appok/play_*.html` fájlokban):
  - https://play.google.com/store/apps/details?id=com.biblediscovery
  - https://play.google.com/store/apps/details?id=com.sirma.mobile.bible.android
  - https://play.google.com/store/apps/details?id=net.bible.android.activity
  - https://play.google.com/store/apps/details?id=com.logos.androidlogos
  - https://play.google.com/store/apps/details?id=ua.mybible
  - https://play.google.com/store/apps/details?id=eu.gyurasz.bible
  - https://play.google.com/store/apps/details?id=hu.bitbaro.bibolka
  - https://play.google.com/store/apps/details?id=hu.bitbaro.karoli2011
  - https://play.google.com/store/apps/details?id=hu.webter.bibliApp
  - https://play.google.com/store/apps/details?id=com.martinvillar.android.hungarianbible
  - https://play.google.com/store/apps/details?id=hungarian.bible
  - https://play.google.com/store/apps/details?id=com.solvus_lab.android.BibleHU_karoli
  - https://play.google.com/store/apps/details?id=com.livingbible.app
  - https://play.google.com/store/apps/details?id=com.murati.audiobook.bible.hu
  - https://play.google.com/store/apps/details?id=com.hit.hitgyulekezete
- App Store:
  - https://apps.apple.com/hu/app/biblia-felfedez%C5%91/id1155806176?l=hu
  - https://apps.apple.com/hu/app/id444815381
  - https://apps.apple.com/hu/app/id1173315254
- Egyéb, letöltve:
  - https://www.bible.com/languages/hun
  - https://www.bible.com/versions/84-hunk-karoli-bible-1908
  - https://www.bible.com/versions/920-rÚf-revised-hungarian-bible
  - https://www.logos.com/product/1834/szent-biblia
  - https://andbible.org/
  - https://f-droid.org/hu/packages/net.bible.android.activity/
  - https://szentiras.hu/ (valamint /biblia/heb, /biblia/bgt)
- Csak kivonatból [S]:
  - http://www.bible-discovery.com/dictionary-license-stronghuheb.php
  - …/dictionary-license-stronghuheb2.php
  - …/dictionary-license-stronghu.php
  - …/dictionary-license-stronghu2.php
  - …/bible-license-hun.php
  - https://www.mobilbiblia.hu/biblia-valtozasok.php
  - http://www.mobilbiblia.hu/megrendeles.php
  - https://www.stepbible.org/version.jsp?version=HunKAR
  - https://stepweb.atlassian.net/wiki/spaces/SUG/pages/12484610/About+STEP+Bible
  - https://community.logos.com/ideas/book-suggestions/hungarian-revised-new-translation-r%C3%BAf-r609/
  - https://community.logos.com/discussion/234592/new-hungarian-translation
  - https://www.ph4.org/b4_1.php?l=hu&q=mybible
  - https://ftp.crosswire.org/ftpmirror/pub/sword/raw/mods.d/hunkar.conf
- Repó [R]:
  - `/home/user/Bible-Study/ADATVAGYON_TERV.md` (37., 67., 77–78., 704. sor)
  - `/home/user/Bible-Study/konkordancia/Karoli_kereszthivatkozasok_README.md` (38–39. sor)
  - `/home/user/Bible-Study/Rendszerfejlesztesi_playbook.md` (76. sor)
