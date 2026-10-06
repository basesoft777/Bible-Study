# F56 M3 — Mintablokk (20 szocikk) · elfogadási próba

*Generálja: `python naplok/F56_minta.py` (a blokkok: `python eszkozok/bdb_adatblokk.py --minta ...`, ts=2026-10-06T12:00:00Z). Minta: a H2617 körüli 10 szócikk (`BDB_FORDITAS_sorrend.tsv` 177–186) és a 6. adag első 10 szócikke (407–416). A szúrópróba a nyers fájlokból, a blokk kódjától függetlenül számol (szocikkenként 3 adat).*

## A. A H2617 körül (177–186)

### H0894

### ADATBLOKK H894 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: bábel ×1, bábelnek ×1
- alacsonyabb bizonyosságú pár (`alacsony`): —
- a lefedett könyvekben a TAHOT-ban 2 előfordulás, ebből 2 kapott Károli-párt
*proveniencia: scope=H894 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **bábel**: 1Móz 10:10 „Az ő birodalmának kezdete volt **Bábel**, Erekh, Akkád és Kálnéh a Sineár földén.”
- **bábelnek**: 1Móz 11:9 „Ezért nevezék annak nevét **Bábelnek**; mert ott zavará össze az Úr az egész föld...”
*proveniencia: scope=H894 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G897 Βαβυλών ×191, G1519 εἰς ×18 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H894 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 197: H895 בָּבֶ֫ל, בָּבֶל („Babylon”)
*proveniencia: scope=H894 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H894 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H894 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `bábel` ×1 → nyers `parok_*.tsv` számlálás: magas 1, alacsony 0 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 10:10	6	Bábel	6	בָּבֶ֔ל	H0894	magas	S+C`
- 2. Példavers: `1Móz 10:10` „Az ő birodalmának kezdete volt **Bábel**, Erekh, Akkád és Kálnéh a Sineár földén.” → a `Karoli_1908.tsv`-ben a vers: „Az ő birodalmának kezdete volt Bábel, Erekh, Akkád és Kálnéh a Sineár földén.” (szakasz BENNE VAN)
- 3. LXX: `G897 Βαβυλών ×191` → nyers `lxx_bridge.tsv`-sor: `H0894 | G0897 | 191` (BENNE VAN)

### H3824

### ADATBLOKK H3824 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: szíve ×1, szívednek ×1, szívem ×1, szívemet ×1
- alacsonyabb bizonyosságú pár (`alacsony`): szívedben ×10, szívedből ×7, szíve ×6, szívetek ×4, szíved ×3, szívetekből ×3 (+18 további alak)
- a lefedett könyvekben a TAHOT-ban 62 előfordulás, ebből 62 kapott Károli-párt
*proveniencia: scope=H3824 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **szívedben**: 3Móz 19:17 „Ne gyűlöld a te atyádfiát **szívedben**; fedd meg a te felebarátodat nyilván, hogy...” · 5Móz 6:6 „...mai napon parancsolok néked, legyenek a te **szívedben**.”
- **szíve**: 2Móz 14:5 „...megváltozék a Faraónak és az ő szolgáinak **szíve** a nép iránt és mondának: Mit cselekedtünk,...” · 5Móz 17:17 „Sok feleséget se tartson, hogy a **szíve** el ne hajoljon; se ezüstjét, se aranyát...”
[LEVÁGVA: a további 24 szóalak példái kimaradtak]
*proveniencia: scope=H3824 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G2588 καρδία ×200, G3588 ὁ ×10, G5590 ψυχή ×4 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H3824 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 1071: H3820 לֵב („heart”); H3823 לִבֵּב („to bake”); H3826 לִבָּה („heart”); H3834 לְבִבָה („cake”)
*proveniencia: scope=H3824 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H3824 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H3824 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `szíve` ×1 → nyers `parok_*.tsv` számlálás: magas 1, alacsony 6 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 14:5	19	szíve	12	לְבַ֨ב	H3824	magas	S+C`
- 2. Példavers: `3Móz 19:17` „Ne gyűlöld a te atyádfiát **szívedben**; fedd meg a te felebarátodat nyilván, hogy...” → a `Karoli_1908.tsv`-ben a vers: „Ne gyűlöld a te atyádfiát szívedben; fedd meg a te felebarátodat nyilván, hogy ne viseljed az ő bűnének terhét.” (szakasz BENNE VAN)
- 3. LXX: `G2588 καρδία ×200` → nyers `lxx_bridge.tsv`-sor: `H3824 | G2588 | 200` (BENNE VAN)

### H4294

### ADATBLOKK H4294 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: nemzetségéből ×6, vesszejét ×6, pálczádat ×3, vessződet ×3, vesszőt ×3, pálcza ×1 (+7 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): nemzetségéből ×34, törzséből ×32, nemzetségének ×19, törzse ×12, nemzetségétől ×11, vesszőt ×8 (+33 további alak)
- a lefedett könyvekben a TAHOT-ban 201 előfordulás, ebből 206 kapott Károli-párt
*proveniencia: scope=H4294 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **nemzetségéből**: 2Móz 31:2 „...Bésaléelt, a Húr fiának Urinak fiát a Júda **nemzetségéből**.” · 2Móz 31:6 „...ímé Aholiábot is, Akhiszamáknak fiát a Dán **nemzetségéből**, mellé adtam; és adtam minden értelmesnek...”
- **törzséből**: 4Móz 1:21 „A kik megszámláltattak a Rúben **törzséből**: negyvenhat ezer és ötszáz.” · 4Móz 1:23 „A kik megszámláltattak Simeon **törzséből**: ötvenkilencz ezer és háromszáz.”
[LEVÁGVA: a további 44 szóalak példái kimaradtak]
*proveniencia: scope=H4294 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G5443 φυλή ×163, G4464 ῥάβδος ×21, G3588 ὁ ×7 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H4294 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 1352: H4295 מַ֫טָּה („beneath”); H4296 מִטָּה („bed”); H4297 מֻטֶּה („perversion”); H4298 מֻטָּה („spread”); H5186 נָטָה („to stretch”)
*proveniencia: scope=H4294 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H4294 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H4294 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `nemzetségéből` ×6 → nyers `parok_*.tsv` számlálás: magas 6, alacsony 34 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 31:2	13	nemzetségéből	11	מַטֵּ֥ה	H4294	magas	S+C`
- 2. Példavers: `2Móz 31:2` „...Bésaléelt, a Húr fiának Urinak fiát a Júda **nemzetségéből**.” → a `Karoli_1908.tsv`-ben a vers: „Ímé, név szerint meghívtam Bésaléelt, a Húr fiának Urinak fiát a Júda nemzetségéből.” (szakasz BENNE VAN)
- 3. LXX: `G5443 φυλή ×163` → nyers `lxx_bridge.tsv`-sor: `H4294 | G5443 | 163` (BENNE VAN)

### H4390

### ADATBLOKK H4390 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: be ×7, meg ×3, töltsétek ×3, betöltötte ×2, betöltöttem ×2, iktasd ×2 (+29 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): tökéletesen ×5, be ×2, fel ×2, jártak ×2, meg ×2, tökéletességgel ×2 (+19 további alak)
- a lefedett könyvekben a TAHOT-ban 62 előfordulás, ebből 86 kapott Károli-párt
*proveniencia: scope=H4390 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **be**: 1Móz 1:22 „...és sokasodjatok, és töltsétek **be** a tenger vizeit; a madár is sokasodjék a...” · 1Móz 1:28 „...Szaporodjatok és sokasodjatok, és töltsétek **be** a földet és hajtsátok birodalmatok alá; és...”
- **meg**: 1Móz 6:13 „...mivelhogy a föld erőszakoskodással telt **meg** általok: és ímé elvesztem őket a földdel...” · 1Móz 42:25 „És parancsola József, hogy töltsék **meg** edényeiket gabonával, és tegyék vissza...”
[LEVÁGVA: a további 54 szóalak példái kimaradtak]
*proveniencia: scope=H4390 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G4137 πληρόω ×46, G4130 πλήθω ×40, G4134 πλήρης ×16 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H4390 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 1195: H4392 מָלֵא („full”); H4393 מְלֹא („fullness”); H4394 מִלֻּא („setting”); H4395 מְלֵאָה („fruit”); H4396 מִלֻּאָה („setting”) (+1 további)
*proveniencia: scope=H4390 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H4390 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H4390 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `be` ×7 → nyers `parok_*.tsv` számlálás: magas 7, alacsony 2 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 1:22	11	be	12	מִלְא֤וּ	H4390	magas	S+C`
- 2. Példavers: `1Móz 1:22` „...és sokasodjatok, és töltsétek **be** a tenger vizeit; a madár is sokasodjék a...” → a `Karoli_1908.tsv`-ben a vers: „És megáldá azokat Isten, mondván: Szaporodjatok, és sokasodjatok, és töltsétek be a tenger vizeit; a madár is sokasodjék a földön.” (szakasz BENNE VAN)
- 3. LXX: `G4137 πληρόω ×46` → nyers `lxx_bridge.tsv`-sor: `H4390 | G4137 | 46` (BENNE VAN)

### H0520

### ADATBLOKK H520 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: sing ×55, egy ×9, másfél ×5, singnyi ×5, harmadfél ×4, két ×4 (+2 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): singet ×4, sing ×3, két ×1, könyök ×1, singnyi ×1, singnyire ×1
- a lefedett könyvekben a TAHOT-ban 74 előfordulás, ebből 95 kapott Károli-párt
*proveniencia: scope=H520 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **sing**: 1Móz 6:15 „...pedig azt: A bárka hoszsza háromszáz **sing** legyen, a szélessége ötven sing, és a...” · 2Móz 25:10 „...egy ládát sittim-fából; harmadfél **sing** hosszút, másfél sing széleset, és másfél...” · 2Móz 25:17 „...fedelet is tiszta aranyból: harmadfél **sing** hosszút, és másfél sing széleset.”
- **egy**: 1Móz 6:16 „Ablakot csinálj a bárkán, és **egy** singnyire hagyd azt felülről; a bárka...” · 2Móz 25:23 „...asztalt is sittim-fából, két sing hosszút, **egy** sing széleset, és másfél sing magasat.” · 2Móz 26:13 „**Egy** singnyi pedig egyfelől, és egy singnyi...”
[LEVÁGVA: a további 8 szóalak példái kimaradtak]
*proveniencia: scope=H520 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G4083 πῆχυς ×105, G1540 ἑκατόν ×15, G1803 ἕξ ×9 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H520 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 115: H517 אֵם („mother”); H523 אֻמָּה („people”)
*proveniencia: scope=H520 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H520 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H520 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `sing` ×55 → nyers `parok_*.tsv` számlálás: magas 55, alacsony 3 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 6:15	9	sing	9	אַמָּ֗ה	H0520	magas	S+C`
- 2. Példavers: `1Móz 6:15` „...pedig azt: A bárka hoszsza háromszáz **sing** legyen, a szélessége ötven sing, és a...” → a `Karoli_1908.tsv`-ben a vers: „Ekképen csináld pedig azt: A bárka hoszsza háromszáz sing legyen, a szélessége ötven sing, és a magassága harmincz sing.” (szakasz BENNE VAN)
- 3. LXX: `G4083 πῆχυς ×105` → nyers `lxx_bridge.tsv`-sor: `H0520 | G4083 | 105` (BENNE VAN)

### H2617

### ADATBLOKK H2617 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: irgalmasságot ×3, szeretettel ×3, irgalmas ×1, irgalmasságod ×1, irgalmasságát ×1, irgalmasságú ×1 (+5 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): irgalmasságot ×6, gyalázatosság ×1, irgalmasságod ×1, irgalmasságú ×1
- a lefedett könyvekben a TAHOT-ban 24 előfordulás, ebből 24 kapott Károli-párt
*proveniencia: scope=H2617 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **irgalmasságot**: 1Móz 24:14 „...Izsáknak, és erről ismerjem meg, hogy **irgalmasságot** cselekedtél az én urammal.” · 1Móz 40:14 „...jól lesz dolgod, és cselekedjél, kérlek, **irgalmasságot** velem, emlékezzél meg rólam a Faraó előtt...”
- **szeretettel**: 1Móz 21:23 „...álnokságot nem cselekszel, hanem azzal a **szeretettel**, a melylyel én te irántad viseltettem,...” · 1Móz 24:49 „Most azért, ha **szeretettel** és hűséggel akartok lenni az én uramhoz,...”
[LEVÁGVA: a további 10 szóalak példái kimaradtak]
*proveniencia: scope=H2617 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G1656 ἔλεος ×142, G1343 δικαιοσύνη ×3, G1654 ἐλεημοσύνη ×3 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H2617 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 698, 699: H2616 חָסַד („be kind”); H2623 חָסִיד („pious”); H2624 חֲסִידָה („stork”)
*proveniencia: scope=H2617 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H2617 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H2617 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `irgalmasságot` ×3 → nyers `parok_*.tsv` számlálás: magas 3, alacsony 6 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 24:14	40	irgalmasságot	37	חֶ֖סֶד	H2617	magas	S+C`
- 2. Példavers: `1Móz 24:14` „...Izsáknak, és erről ismerjem meg, hogy **irgalmasságot** cselekedtél az én urammal.” → a `Karoli_1908.tsv`-ben a vers: „Legyen azért, hogy a mely leánynak ezt mondom: Hajtsd meg a te vedredet, hogy igyam, és az azt mondándja: igyál, sőt a te tevéidet is megitatom: hogy azt rendel” (szakasz BENNE VAN)
- 3. LXX: `G1656 ἔλεος ×142` → nyers `lxx_bridge.tsv`-sor: `H2617 | G1656 | 142` (BENNE VAN)

### H7272

### ADATBLOKK H7272 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: lábaikat ×4, lábai ×2, lábainak ×2, lábaitokat ×2, lépése ×2, háromszor ×1 (+14 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): lábának ×5, gyalog ×2, lábad ×2, lábai ×2, lábaikat ×2, lábát ×2 (+27 további alak)
- a lefedett könyvekben a TAHOT-ban 71 előfordulás, ebből 71 kapott Károli-párt
*proveniencia: scope=H7272 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **lábaikat**: 1Móz 43:24 „...József házába, és vizet hozata, és megmosák **lábaikat**, és abrakot is ada az ő szamaraiknak.” · 2Móz 30:19 „...és az ő fiai abból mossák meg kezeiket és **lábaikat**.”
- **lábának**: 2Móz 25:26 „...hozzá, és illeszd a karikákat a négy **lábának** négy szegletére.” · 3Móz 8:23 „...és jobb kezének hüvelykére és jobb **lábának** hüvelykére.”
[LEVÁGVA: a további 42 szóalak példái kimaradtak]
*proveniencia: scope=H7272 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G4228 πούς ×169, G3588 ὁ ×14, G5154 τρίτος ×3 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H7272 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 2113: H4772 מַרְגְּלוֹת („feet”); H7270 רָגַל („to spy”); H7273 רַגְלִי („on foot”); H8637 תִּרְגַּל („to teach”)
*proveniencia: scope=H7272 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H7272 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H7272 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `lábaikat` ×4 → nyers `parok_*.tsv` számlálás: magas 4, alacsony 2 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 43:24	16	lábaikat	16	רַגְלֵי	H7272	magas	S+C`
- 2. Példavers: `1Móz 43:24` „...József házába, és vizet hozata, és megmosák **lábaikat**, és abrakot is ada az ő szamaraiknak.” → a `Karoli_1908.tsv`-ben a vers: „Bevivé azután a férfiú azokat az embereket a József házába, és vizet hozata, és megmosák lábaikat, és abrakot is ada az ő szamaraiknak.” (szakasz BENNE VAN)
- 3. LXX: `G4228 πούς ×169` → nyers `lxx_bridge.tsv`-sor: `H7272 | G4228 | 169` (BENNE VAN)

### H2428

### ADATBLOKK H2428 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: serege ×3, derék ×2, seregét ×2, gazdagságukat ×1, termett ×1
- alacsonyabb bizonyosságú pár (`alacsony`): erős ×2, emberek ×1, erejét ×1, gazdagságnak ×1, gazdagságot ×1, hadakozásra ×1 (+6 további alak)
- a lefedett könyvekben a TAHOT-ban 21 előfordulás, ebből 22 kapott Károli-párt
*proveniencia: scope=H2428 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **serege**: 2Móz 14:4 „...megdicsőíttessem a Faraó által és minden ő **serege** által és megtudják az Égyiptombeliek, hogy...” · 2Móz 14:9 „...minden lova, szekere, meg lovasai és **serege** Pi-Hahiróth mellett, Baál-Czefón előtt.” · 2Móz 14:17 „...megdicsőíttetem a Faraó által és az ő egész **serege** által, szekerei és lovasai által.”
- **derék**: 2Móz 18:21 „És szemelj ki magad az egész nép közűl **derék**, istenfélő férfiakat, igazságos férfiakat,...” · 2Móz 18:25 „És választa Mózes az egész Izráelből **derék** férfiakat és a nép fejeivé tevé őket,...”
[LEVÁGVA: a további 15 szóalak példái kimaradtak]
*proveniencia: scope=H2428 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G1411 δύναμις ×147, G2479 ἰσχύς ×20, G1415 δυνατός ×10 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H2428 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 624: H2342 חוּל („to twist”)
*proveniencia: scope=H2428 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H2428 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H2428 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `serege` ×3 → nyers `parok_*.tsv` számlálás: magas 3, alacsony 0 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 14:4	19	serege	17	חֵיל֔	H2428	magas	S+C`
- 2. Példavers: `2Móz 14:4` „...megdicsőíttessem a Faraó által és minden ő **serege** által és megtudják az Égyiptombeliek, hogy...” → a `Karoli_1908.tsv`-ben a vers: „Én pedig megkeményítem a Faraó szívét, és űzőbe veszi őket, hogy megdicsőíttessem a Faraó által és minden ő serege által és megtudják az Égyiptombeliek, hogy én” (szakasz BENNE VAN)
- 3. LXX: `G1411 δύναμις ×147` → nyers `lxx_bridge.tsv`-sor: `H2428 | G1411 | 147` (BENNE VAN)

### H0410

### ADATBLOKK H410 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: isten ×12, istennek ×4, istene ×2, erőm ×1, istenek ×1, istenem ×1 (+4 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): isten ×21, istenek ×2, istennek ×2, erő ×1, istene ×1, istenről ×1
- a lefedett könyvekben a TAHOT-ban 53 előfordulás, ebből 53 kapott Károli-párt
*proveniencia: scope=H410 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **isten**: 1Móz 14:20 „Áldott a Magasságos **Isten**, a ki kezedbe adta ellenségeidet. És...” · 1Móz 17:1 „...Úr Ábrámnak, és monda néki: Én a mindenható **Isten** vagyok, járj én előttem, és légy tökéletes.” · 1Móz 28:3 „A mindenható **Isten** pedig áldjon meg, szaporítson és sokasítson...”
- **istennek**: 1Móz 14:18 „...kenyeret és bort hoza; ő pedig a Magasságos **Istennek** papja vala.” · 1Móz 21:33 „...és segítségűl hívá ott az örökkévaló Úr **Istennek** nevét.” · 1Móz 35:1 „...le ott; és csinálj ott oltárt amaz **Istennek**, ki megjelenék néked, mikor a te bátyád...”
[LEVÁGVA: a további 10 szóalak példái kimaradtak]
*proveniencia: scope=H410 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G2316 θεός ×142, G2962 κύριος ×39, G2478 ἰσχυρός ×14 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H410 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 93: H430 אֱלֹהִים („LORD”); H433 אֱלֹהַּ („god”)
*proveniencia: scope=H410 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H410 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H410 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `isten` ×12 → nyers `parok_*.tsv` számlálás: magas 12, alacsony 21 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 14:20	4	Isten	3	אֵ֣ל	H0410	magas	S+C`
- 2. Példavers: `1Móz 14:20` „Áldott a Magasságos **Isten**, a ki kezedbe adta ellenségeidet. És...” → a `Karoli_1908.tsv`-ben a vers: „Áldott a Magasságos Isten, a ki kezedbe adta ellenségeidet. És tizedet ada néki mindenből.” (szakasz BENNE VAN)
- 3. LXX: `G2316 θεός ×142` → nyers `lxx_bridge.tsv`-sor: `H0410 | G2316 | 142` (BENNE VAN)

### H1366

### ADATBLOKK H1366 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: határodat ×3, határa ×1, határban ×1, határodban ×1, határodra ×1, határszélétől ×1 (+2 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): határ ×42, határa ×18, határotok ×9, határáig ×9, határuk ×8, határán ×6 (+20 további alak)
- a lefedett könyvekben a TAHOT-ban 136 előfordulás, ebből 136 kapott Károli-párt
*proveniencia: scope=H1366 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **határ**: 4Móz 22:36 „...egyik városába, a mely az Arnon vidékén, a **határ** szélén vala.” · 4Móz 34:4 „És kerüljön a **határ** dél felől az Akrabbim hágójáig, és menjen...”
- **határa**: 1Móz 10:19 „Vala pedig a Kananeusok **határa**, Czídonból Gérár felé menve Gázáig; Sodoma,...” · 4Móz 21:13 „...az Emoreus határából. Mert az Arnon Moábnak **határa** Moáb között és Emoreus között.”
[LEVÁGVA: a további 27 szóalak példái kimaradtak]
*proveniencia: scope=H1366 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G3725 ὅριον ×121, G3588 ὁ ×3 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H1366 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 307: H1367 גְּבוּלָה („border”); H1379 גָּבַל („to border”); H1383 גַּבְלֻת („twists”); H4020 מִגְבָּלֹת („twisted”)
*proveniencia: scope=H1366 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H1366 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H1366 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `határodat` ×3 → nyers `parok_*.tsv` számlálás: magas 3, alacsony 2 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 8:2	11	határodat	12	גְּבוּלְ	H1366	magas	S+C`
- 2. Példavers: `4Móz 22:36` „...egyik városába, a mely az Arnon vidékén, a **határ** szélén vala.” → a `Karoli_1908.tsv`-ben a vers: „Mikor pedig meghallá Bálák, hogy jön Bálám, kiméne elébe Moábnak egyik városába, a mely az Arnon vidékén, a határ szélén vala.” (szakasz BENNE VAN)
- 3. LXX: `G3725 ὅριον ×121` → nyers `lxx_bridge.tsv`-sor: `H1366 | G3725 | 121` (BENNE VAN)

## B. A 6. adag első 10 szocikke (407–416)

### H0123

### ADATBLOKK H123 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: edóm ×7, edómnak ×2, edom ×1, edomiták ×1, edomnak ×1, edómban ×1 (+1 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): edom ×10, edomnak ×1
- a lefedett könyvekben a TAHOT-ban 25 előfordulás, ebből 25 kapott Károli-párt
*proveniencia: scope=H123 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **edom**: 2Móz 15:15 „Akkor megháborodának **Edom** fejedelmei, Moáb hatalmasait rettegés...” · 4Móz 20:14 „És külde Mózes követeket Kádesből **Edom** királyához, kik így szólának: Ezt mondja a...” · 4Móz 20:18 „Felele pedig **Edom**: Nem mehetsz át az én földemen, hogy...”
- **edóm**: 1Móz 32:3 „...Ézsaúhoz az ő bátyjához, Széir földébe, **Edóm** mezőségébe,” · 1Móz 36:8 „...tehát Ézsaú a Széir hegyén. Ézsaú pedig az **Edóm**.” · 1Móz 36:17 „...fejedelem. Ezek Rehuéltől való fejedelmek **Edóm** országában. Ezek Boszmáthnak, Ézsaú...”
[LEVÁGVA: a további 5 szóalak példái kimaradtak]
*proveniencia: scope=H123 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
—
*proveniencia: scope=H123 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 26: H119 אָדֹם („to redden”); H122 אֱדֹם („red stuff”); H124 אֹ֫דֶם („sardius”); H125 אֲדַמְדָּם („reddish”); H130 אֲדֹמִי („Edom”) (+1 további)
*proveniencia: scope=H123 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H123 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H123 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `edóm` ×7 → nyers `parok_*.tsv` számlálás: magas 7, alacsony 0 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 32:3	13	Edóm	16	אֱדֽוֹם	H0123	magas	S+C`
- 2. Példavers: `2Móz 15:15` „Akkor megháborodának **Edom** fejedelmei, Moáb hatalmasait rettegés...” → a `Karoli_1908.tsv`-ben a vers: „Akkor megháborodának Edom fejedelmei, Moáb hatalmasait rettegés szállja meg, elcsügged a Kanaán egész lakossága.” (szakasz BENNE VAN)
- 3. LXX: „—” → nyers `lxx_bridge.tsv`-ben a `H0123` sorai: 0

### H3282

### ADATBLOKK H3282 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: mivelhogy ×1
- alacsonyabb bizonyosságú pár (`alacsony`): mert ×2, mivelhogy ×2, a ×1, azért ×1, hogy ×1, miért ×1
- a lefedett könyvekben a TAHOT-ban 7 előfordulás, ebből 9 kapott Károli-párt
*proveniencia: scope=H3282 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **mivelhogy**: 1Móz 22:16 „...Én magamra esküszöm azt mondja az Úr: **mivelhogy** e dolgot cselekedéd, és nem kedvezél a te...” · 4Móz 11:20 „...az orrotokon, és útálatossá lesz előttetek; **mivelhogy** megvetettétek az Urat, a ki közöttetek van;...”
- **mert**: 3Móz 26:43 „...szenvedik bűnöknek büntetését, azért, **mert** megvetették az én ítéleteimet, és megútálta...” · 5Móz 1:36 „...földet, a melyet tapodott, és az ő fiainak, **mert** tökéletességgel követte az Urat.”
[LEVÁGVA: a további 4 szóalak példái kimaradtak]
*proveniencia: scope=H3282 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G473 ἀντί ×21, G3754 ὅτι ×6, G1223 διά ×4 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H3282 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 1650: H4616 מַ֫עַן („because”); H4617 מַעֲנֶה („answer”); H5772 עֹנָה („cohabitation”); H6030 עָנָה („to answer”); H6256 עֵת („time”) (+2 további)
*proveniencia: scope=H3282 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H3282 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H3282 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `mivelhogy` ×1 → nyers `parok_*.tsv` számlálás: magas 1, alacsony 2 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 22:16	10	mivelhogy	9	יַ֚עַן	H3282	magas	S+C`
- 2. Példavers: `1Móz 22:16` „...Én magamra esküszöm azt mondja az Úr: **mivelhogy** e dolgot cselekedéd, és nem kedvezél a te...” → a `Karoli_1908.tsv`-ben a vers: „És monda: Én magamra esküszöm azt mondja az Úr: mivelhogy e dolgot cselekedéd, és nem kedvezél a te fiadnak, a te egyetlenegyednek:” (szakasz BENNE VAN)
- 3. LXX: `G473 ἀντί ×21` → nyers `lxx_bridge.tsv`-sor: `H3282 | G0473 | 21` (BENNE VAN)

### H5785

### ADATBLOKK H5785 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: borzbőrökből ×3, bőre ×3, kosbőrökből ×3, borzbőröket ×2, kosbőröket ×2, borzbőrök ×1 (+5 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): bőrön ×16, bőrén ×10, bőrnél ×9, bőrből ×8, borzbőrből ×6, bőrét ×5 (+5 további alak)
- a lefedett könyvekben a TAHOT-ban 80 előfordulás, ebből 80 kapott Károli-párt
*proveniencia: scope=H5785 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **bőrön**: 3Móz 13:5 „...van, át nem terjedt tovább a fakadék a **bőrön**, a pap másodszor is rekeszsze őt külön hét...” · 3Móz 13:6 „...meghalványodott, és nem terjedt tovább a **bőrön** a fakadék, tisztának ítélje őt a pap;...”
- **bőrén**: 3Móz 13:2 „Ha valamely ember testének **bőrén** daganat, vagy tarjagosság, vagy fehér folt...” · 3Móz 13:3 „És nézze meg a pap azt a test **bőrén** lévő fakadékot. Ha a szőr a fakadékban...”
[LEVÁGVA: a további 17 szóalak példái kimaradtak]
*proveniencia: scope=H5785 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G1192 δέρμα ×67, G1193 δερμάτινος ×13 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H5785 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
—
*proveniencia: scope=H5785 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H5785 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H5785 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `borzbőrökből` ×3 → nyers `parok_*.tsv` számlálás: magas 3, alacsony 0 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 26:14	15	borzbőrökből	11	עֹרֹ֥ת	H5785	magas	S+C`
- 2. Példavers: `3Móz 13:5` „...van, át nem terjedt tovább a fakadék a **bőrön**, a pap másodszor is rekeszsze őt külön hét...” → a `Karoli_1908.tsv`-ben a vers: „A hetedik napon pedig nézze meg őt a pap, s ha szerinte a fakadék egy állapotban van, át nem terjedt tovább a fakadék a bőrön, a pap másodszor is rekeszsze őt k” (szakasz BENNE VAN)
- 3. LXX: `G1192 δέρμα ×67` → nyers `lxx_bridge.tsv`-sor: `H5785 | G1192 | 67` (BENNE VAN)

### H7637

### ADATBLOKK H7637 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: hetedik ×16, hetednapon ×3, hetedikben ×2
- alacsonyabb bizonyosságú pár (`alacsony`): hetedik ×33, hetednapon ×7
- a lefedett könyvekben a TAHOT-ban 61 előfordulás, ebből 61 kapott Károli-párt
*proveniencia: scope=H7637 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **hetedik**: 1Móz 2:2 „...a melyet alkotott vala, megszűnék a **hetedik** napon minden munkájától, a melyet alkotott...” · 1Móz 2:3 „És megáldá Isten a **hetedik** napot, és megszentelé azt; mivelhogy azon...” · 1Móz 8:4 „A bárka pedig a **hetedik** hónapban, a hónak tizenhetedik napján,...”
- **hetednapon**: 1Móz 2:2 „Mikor pedig elvégezé Isten **hetednapon** az ő munkáját, a melyet alkotott vala,...” · 2Móz 16:27 „És lőn **hetednapon**: kimenének a nép közül, hogy szedjenek, de...” · 2Móz 31:17 „...teremtette az Úr a mennyet és a földet, **hetednapon** pedig megszünt és megnyugodott.”
[LEVÁGVA: a további 1 szóalak példái kimaradtak]
*proveniencia: scope=H7637 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G1442 ἕβδομος ×79 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H7637 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 2318: H7620 שָׁבוּעַ („week”); H7651 שֶׁ֫בַע („seven”); H7657 שִׁבְעִים („seventy”); H7658 שִׁבְעָ֫נָה („seven”); H7659 שִׁבְעָתַיִם („sevenfold”)
*proveniencia: scope=H7637 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H7637 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H7637 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `hetedik` ×16 → nyers `parok_*.tsv` számlálás: magas 16, alacsony 33 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 2:2	15	hetedik	17	שְּׁבִיעִ֔י	H7637	magas	S+C`
- 2. Példavers: `1Móz 2:2` „...a melyet alkotott vala, megszűnék a **hetedik** napon minden munkájától, a melyet alkotott...” → a `Karoli_1908.tsv`-ben a vers: „Mikor pedig elvégezé Isten hetednapon az ő munkáját, a melyet alkotott vala, megszűnék a hetedik napon minden munkájától, a melyet alkotott vala.” (szakasz BENNE VAN)
- 3. LXX: `G1442 ἕβδομος ×79` → nyers `lxx_bridge.tsv`-sor: `H7637 | G1442 | 79` (BENNE VAN)

### H6215

### ADATBLOKK H6215 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: ézsaú ×56, ézsaúnak ×16, ézsaúhoz ×2, ézsaút ×2
- alacsonyabb bizonyosságú pár (`alacsony`): ézsaú ×5, ézsaunak ×1, ézsaut ×1, ézsaúnak ×1
- a lefedett könyvekben a TAHOT-ban 84 előfordulás, ebből 84 kapott Károli-párt
*proveniencia: scope=H6215 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 3 verse, a szó **kiemelve**)
- **ézsaú**: 1Móz 25:26 „Azután kijöve az ő atyjafia, kezével **Ézsaú** sarkába fogódzva; azért nevezék nevét...” · 1Móz 25:27 „És felnevekedének a gyermekek, és **Ézsaú** vadászathoz értő mezei ember vala; Jákób...” · 1Móz 25:29 „Jákób egyszer valami főzeléket főze, és **Ézsaú** megjövén elfáradva a mezőről,”
- **ézsaúnak**: 1Móz 25:25 „...mint egy lazsnak; azért nevezék nevét **Ézsaúnak**.” · 1Móz 25:34 „S akkor Jákób ada **Ézsaúnak** kenyeret, és főtt lencsét, és evék és ivék,...” · 1Móz 27:5 „...pedig meghallá, a mit Izsák az ő fiának **Ézsaúnak** monda; s a mint elméne Ézsaú a mezőre, hogy...”
[LEVÁGVA: a további 4 szóalak példái kimaradtak]
*proveniencia: scope=H6215 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G2269 Ἠσαῦ ×87 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H6215 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
— (a Strong-számhoz nincs TWOT-szám az OSHL-indexben)
*proveniencia: scope=H6215 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H6215 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H6215 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `ézsaú` ×56 → nyers `parok_*.tsv` számlálás: magas 56, alacsony 5 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 25:26	7	Ézsaú	13	עֵשָׂ֔ו	H6215	magas	S+C`
- 2. Példavers: `1Móz 25:26` „Azután kijöve az ő atyjafia, kezével **Ézsaú** sarkába fogódzva; azért nevezék nevét...” → a `Karoli_1908.tsv`-ben a vers: „Azután kijöve az ő atyjafia, kezével Ézsaú sarkába fogódzva; azért nevezék nevét Jákóbnak. Izsák pedig hatvan esztendős vala, a mikor ezek születének.” (szakasz BENNE VAN)
- 3. LXX: `G2269 Ἠσαῦ ×87` → nyers `lxx_bridge.tsv`-sor: `H6215 | G2269 | 87` (BENNE VAN)

### H7097

### ADATBLOKK H7097 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: szélén ×3, egyik ×2, másik ×2, végig ×2, végtől ×2, egyig ×1 (+7 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): szélén ×4, végétől ×4, szélétől ×3, részét ×2, szélébe ×2, széléig ×2 (+15 további alak)
- a lefedett könyvekben a TAHOT-ban 47 előfordulás, ebből 53 kapott Károli-párt
*proveniencia: scope=H7097 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **szélén**: 2Móz 13:20 „...és táborba szállának Ethámban, a puszta **szélén**.” · 2Móz 26:5 „...kárpiton; ötven hurkot csinálj ama kárpit **szélén** is, a mely a másik egybefoglalásban van;...”
- **végétől**: 4Móz 34:3 „...és legyen a ti déli határotok a Sós tenger **végétől** napkelet felé.” · 5Móz 13:7 „...hozzád vagy távol tőled, a földnek egyik **végétől** a másik végéig:”
[LEVÁGVA: a további 25 szóalak példái kimaradtak]
*proveniencia: scope=H7097 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G3313 μέρος ×19, G206 ἄκρον ×14, G2078 ἔσχατος ×8 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H7097 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 2053: H7096 קָצָה („to cut off”); H7098 קָצָה („end”); H7099 קָ֫צוּ („boundary”); H7117 קְצָת („end”)
*proveniencia: scope=H7097 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H7097 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H7097 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `szélén` ×3 → nyers `parok_*.tsv` számlálás: magas 3, alacsony 4 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 13:20	10	szélén	10	קְצֵ֖ה	H7097	magas	S+C`
- 2. Példavers: `2Móz 13:20` „...és táborba szállának Ethámban, a puszta **szélén**.” → a `Karoli_1908.tsv`-ben a vers: „És elindulának Szukhótból és táborba szállának Ethámban, a puszta szélén.” (szakasz BENNE VAN)
- 3. LXX: `G3313 μέρος ×19` → nyers `lxx_bridge.tsv`-sor: `H7097 | G3313 | 19` (BENNE VAN)

### H7646

### ADATBLOKK H7646 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: jól ×2, lakjatok ×1, laktok ×1
- alacsonyabb bizonyosságú pár (`alacsony`): megelégszel ×3, jól ×2, elégesztek ×1, jóllakik ×1, lakjanak ×1, lakol ×1 (+2 további alak)
- a lefedett könyvekben a TAHOT-ban 10 előfordulás, ebből 15 kapott Károli-párt
*proveniencia: scope=H7646 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **jól**: 2Móz 16:8 „...az Úr ennetek, reggel pedig kenyeret, hogy **jól** lakjatok; mert hallotta az Úr a ti...” · 2Móz 16:12 „...húst esztek, reggel pedig kenyérrel laktok **jól** és megtudjátok, hogy én vagyok az Úr a ti...”
- **megelégszel**: 5Móz 6:11 „...a melyeket nem te plántáltál; és eszel és **megelégszel**:” · 5Móz 8:10 „Ha azért eszel majd és **megelégszel**: dícsérjed az Urat, a te Istenedet azért a...”
[LEVÁGVA: a további 8 szóalak példái kimaradtak]
*proveniencia: scope=H7646 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G4130 πλήθω ×16, G5526 χορτάζω ×9, G1705 ἐμπίμπλημι ×6 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H7646 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 2231: H7647 שָׂבָע („abundance”); H7648 שֹׂ֫בַע („satiety”); H7653 שִׂבְעָה („fullness”); H7654 שׇׂבְעָה („satiety”)
*proveniencia: scope=H7646 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H7646 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H7646 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `jól` ×2 → nyers `parok_*.tsv` számlálás: magas 2, alacsony 2 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 16:8	14	jól	19	שְׂבֹּ֔עַ	H7646	magas	S+C`
- 2. Példavers: `2Móz 16:8` „...az Úr ennetek, reggel pedig kenyeret, hogy **jól** lakjatok; mert hallotta az Úr a ti...” → a `Karoli_1908.tsv`-ben a vers: „És monda Mózes: Estve húst ád az Úr ennetek, reggel pedig kenyeret, hogy jól lakjatok; mert hallotta az Úr a ti zúgolódástokat, melylyel ellene zúgolódtatok. De” (szakasz BENNE VAN)
- 3. LXX: `G4130 πλήθω ×16` → nyers `lxx_bridge.tsv`-sor: `H7646 | G4130 | 16` (BENNE VAN)

### H8334

### ADATBLOKK H8334 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: szolgája ×2, szolgál ×2, szolgálatra ×2, szolgáljanak ×2, szolgála ×1, szolgálathoz ×1 (+2 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): szolgáljanak ×4, szolgálnak ×3, szolgáljon ×2, segítse ×1, szolgája ×1, szolgájának ×1 (+4 további alak)
- a lefedett könyvekben a TAHOT-ban 28 előfordulás, ebből 28 kapott Károli-párt
*proveniencia: scope=H8334 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **szolgáljanak**: 2Móz 30:20 „...vagy mikor az oltárhoz járulnak, hogy **szolgáljanak** és tűzáldozatot füstölögtessenek az Úrnak.” · 2Móz 39:26 „...a palást peremén köröskörül, hogy abban **szolgáljanak**, a mint az Úr parancsolta vala Mózesnek.”
- **szolgája**: 2Móz 24:13 „Felkele azért Mózes és az ő **szolgája** Józsué, és felméne Mózes az Isten hegyére.” · 2Móz 33:11 „...és mikor Mózes a táborba visszatére, az ő **szolgája** az ifjú Józsué, Núnnak fia, nem távozék el...”
[LEVÁGVA: a további 12 szóalak példái kimaradtak]
*proveniencia: scope=H8334 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G3008 λειτουργέω ×25, G3011 λειτουργός ×3 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H8334 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 2472: H8335 שָׁרֵת („ministry”)
*proveniencia: scope=H8334 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H8334 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H8334 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `szolgája` ×2 → nyers `parok_*.tsv` számlálás: magas 2, alacsony 1 (EGYEZIK); első nyers sor: `parok_2Moz.tsv: 2Móz 24:13	7	szolgája	6	מְשָׁרְת֑	H8334	magas	S+C`
- 2. Példavers: `2Móz 30:20` „...vagy mikor az oltárhoz járulnak, hogy **szolgáljanak** és tűzáldozatot füstölögtessenek az Úrnak.” → a `Karoli_1908.tsv`-ben a vers: „A mikor a gyülekezet sátorába mennek, mosakodjanak meg vízben, hogy meg ne haljanak; vagy mikor az oltárhoz járulnak, hogy szolgáljanak és tűzáldozatot füstölög” (szakasz BENNE VAN)
- 3. LXX: `G3008 λειτουργέω ×25` → nyers `lxx_bridge.tsv`-sor: `H8334 | G3008 | 25` (BENNE VAN)

### H1481

### ADATBLOKK H1481 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: jövevény ×2, tartózkodik ×2, tartózkodék ×2, asszonyától ×1, lakó ×1, tartózkodjanak ×1 (+6 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): tartózkodó ×9, tartózkodik ×6, lakik ×2, tartózkodnak ×2, félj ×1, féljetek ×1 (+5 további alak)
- a lefedett könyvekben a TAHOT-ban 38 előfordulás, ebből 41 kapott Károli-párt
*proveniencia: scope=H1481 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **tartózkodó**: 3Móz 16:29 „...se a benszülött, se a közöttetek **tartózkodó** jövevény.” · 3Móz 17:8 „...is: Valaki az Izráel házából, vagy a köztök **tartózkodó** jövevények közül, egészen égőáldozatot...”
- **tartózkodik**: 2Móz 12:48 „És ha jövevény **tartózkodik** nálad, és páskhát akarna készíteni az...” · 2Móz 12:49 „...és a jövevénynek, a ki közöttetek **tartózkodik**.”
[LEVÁGVA: a további 18 szóalak példái kimaradtak]
*proveniencia: scope=H1481 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G3939 παροικέω ×22, G4339 προσήλυτος ×5, G2730 κατοικέω ×3 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H1481 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 330, 331, 332: H1482 גּוּר („whelp”); H1484 גּוֹר („whelp”); H1616 גֵּר („sojourner”); H1628 גֵּרוּת („Geruth_Chimham”); H4032 מָגוֹר („terror”) (+4 további)
*proveniencia: scope=H1481 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H1481 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H1481 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `jövevény` ×2 → nyers `parok_*.tsv` számlálás: magas 2, alacsony 1 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 19:9	14	jövevény	11	גוּר֙	H1481	magas	S+C`
- 2. Példavers: `3Móz 16:29` „...se a benszülött, se a közöttetek **tartózkodó** jövevény.” → a `Karoli_1908.tsv`-ben a vers: „Örökkévaló rendtartás legyen ez nálatok: a hetedik hónapban, a hónapnak tizedikén sanyargassátok meg magatokat és semmi munkát ne végezzetek, se a benszülött, s” (szakasz BENNE VAN)
- 3. LXX: `G3939 παροικέω ×22` → nyers `lxx_bridge.tsv`-sor: `H1481 | G3939 | 22` (BENNE VAN)

### H2543

### ADATBLOKK H2543 (gépi, a projekt adataiból; nem értelmezés; max. 2500 karakter; levágás: példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])

**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)
- magas bizonyosságú pár: szamarát ×4, szamár ×4, szamara ×2, szamarait ×2, szamarat ×2, szamárnak ×2 (+13 további alak)
- alacsonyabb bizonyosságú pár (`alacsony`): szamár ×3, szamarad ×2, szamara ×1, szamaraikra ×1, szamarait ×1, szamarak ×1 (+7 további alak)
- a lefedett könyvekben a TAHOT-ban 45 előfordulás, ebből 45 kapott Károli-párt
*proveniencia: scope=H2543 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv | ts=2026-10-06T12:00:00Z*

**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első 2 verse, a szó **kiemelve**)
- **szamár**: 1Móz 49:14 „Izsakhár erős csontú **szamár**, a karámok közt heverész.” · 2Móz 21:33 „...vermet ás, és nem fedi azt be, és ökör vagy **szamár** esik bele:”
- **szamarát**: 1Móz 22:3 „...Ábrahám jó reggel, és megnyergelé az ő **szamarát**, és maga mellé vevé két szolgáját, és az ő...” · 1Móz 44:13 „...ruhájokat, és kiki megterhelé a maga **szamarát**, és visszatérének a városba.”
[LEVÁGVA: a további 23 szóalak példái kimaradtak]
*proveniencia: scope=H2543 | forras=adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-06T12:00:00Z*

**3. LXX-megfelelő**
G3688 ὄνος ×30, G5268 ὑποζύγιον ×8 (a legfeljebb 3 leggyakoribb)
*proveniencia: scope=H2543 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**4. Rokon szavak** (azonos TWOT-szám, legfeljebb 5, a Strong-szám szerint növekvő)
TWOT 685: H2560 חָמַר („to daub”); H3180 יַחְמוּר („roebuck”)
*proveniencia: scope=H2543 | forras=konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv | ts=2026-10-06T12:00:00Z*

**5. Meglévő magyar szócikk**
—
*proveniencia: scope=H2543 | forras=adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv | ts=2026-10-06T12:00:00Z*

**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)
—
*proveniencia: scope=H2543 | forras=adat/bdb_igehely_javitas.tsv | ts=2026-10-06T12:00:00Z*

**Szúrópróba (MIND EGYEZIK):**

- 1. Károli: `szamarát` ×4 → nyers `parok_*.tsv` számlálás: magas 4, alacsony 1 (EGYEZIK); első nyers sor: `parok_1Moz.tsv: 1Móz 22:3	10	szamarát	9	חֲמֹר֔	H2543	magas	S+C`
- 2. Példavers: `1Móz 49:14` „Izsakhár erős csontú **szamár**, a karámok közt heverész.” → a `Karoli_1908.tsv`-ben a vers: „Izsakhár erős csontú szamár, a karámok közt heverész.” (szakasz BENNE VAN)
- 3. LXX: `G3688 ὄνος ×30` → nyers `lxx_bridge.tsv`-sor: `H2543 | G3688 | 30` (BENNE VAN)

## Összegzés

- Blokkok: 20; szúrópróba mind egyezik: 20/20.
