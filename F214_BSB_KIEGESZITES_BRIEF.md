---
feladat: 214
cim: BSB Strong-réteg kiegészítése (Újszövetség, 2Sám, Ezsd, Dán)
kod: BSB_KIEGESZITES
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/f214-bsb-kiegeszites-a36557
ad: a BSB_Strongs.tsv az Újszövetséggel és a három küszöb alatti ószövetségi könyvvel bővül, ahol a 95%-os küszöböt (DT6) az egyenértékű Strong-számok normalizálása után elérik; a jelentés könyvenként az előtte–utána számot adja
kovetkezo: "Te: a draft PR átnézése; merge az orkesztrátoré"
munka: adat
olvas: [CLAUDE.md, NYITOTT_FELADATOK.md, konkordancia/README.md, eszkozok/fj2/bsb_import.py, naplok/F16_bsb_lefedettseg.tsv, naplok/F41_nem_egyezo_versek.tsv, konkordancia/BDB_strong_alias.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, eszkozok/sqlite_epit.py]
ir: [eszkozok/fj2/bsb_import.py, eszkozok/olvaso_szerver/bibliak.py, eszkozok/olvaso_szerver/teszt_bibliavalaszto.py, eszkozok/olvaso_szerver/README.md, naplok/F214_hiany_meres.md, F214_BSB_KIEGESZITES_BRIEF.md]
lezarva_osszegzes: "mérés: 2Sám/Ezsd/Dán TBESH-normalizálással 95% fölött, az Újszövetség mind a 27 könyve alatta; a BSB kikerült a bibliaválasztóból (nincs teljes 66 könyv); import nincs, N174/b"
fugg: []
---

# F214_BSB_KIEGESZITES_BRIEF.md — BSB Strong-réteg kiegészítése

*FELADATOK #214 · Modell: sonnet · v1 · 2026.11.12*

## 1. Cél

A felhasználó kérése (2026-11-12): „hozzuk be ha 2Sámuel, az Ezsdrás és a Dániel pedig a 95%-os egyezési küszöb alatt maradt, - tudjuk javitani”. A BSB-t az F16/F41 csak az Ószövetség angol hídjaként hozta be; az Újszövetség szándékosan kimaradt (`USZ_KIHAGYVA`), a 2Sám (94,96%), az Ezsd (94,64%) és a Dán (89,64%) a küszöb alatt maradt. Az F210 bibliaválasztója a BSB-t 36 könyvvel mutatja (N171).

## 2. Hatókör

**Benne van.**
1. Az Újszövetség behozása ugyanazzal a mércével, mint az ószövetségi: versszintű egyezés, a TAGNT Strong-halmaza ⊆ a BSB-é, 95%-os küszöb, a `Karoli_versmegfeleltetes` szerint. Forrás: `BSB-publishing/bsb-data-output`, `base/display/` (CC0 1.0), lehetőleg a `a4a2c0558c26e0281ba4e3f0e5479398459e2183` commit.
2. A 2Sám, az Ezsd, a Dán és a már bent lévő 36 könyv újramérése az egyenértékű Strong-számok normalizálásával, egy meglévő, dokumentált egyenértékűségi táblával (új egyenértékűséget nem találunk ki).
3. A BSB megjelenítése az olvasóban: az adatbázis-építő (`sqlite_epit.py`) és a bibliaválasztó (a hiányzó könyvek szürkén, „ebben a fordításban nincs”).
4. `konkordancia/README.md` BSB-szakasza.

**Nincs benne.** A küszöb módosítása (DT6: 95% marad). A CC BY 4.0-s `index-cc-by/` (nem importálható). Az `eszkozok/olvaso_szerver/` fájljai, amelyeket az F213 is ír: ott N-F tétel, nem szerkesztés.

## 3. Lépések (⛔ a kötelező megállások)

0. Mérés a meglévő importtal (viszonyítás), az egyenértékűségi táblák felmérése.
1. A normalizálás beépítése a mérésbe; újramérés mind a 66 könyvre. ⛔ Ha a normalizálás a bent lévő 36 könyv eredményét érdemben változtatja, vagy az egyenértékűség forrása vitatható: megállás és jelzés.
2. Az NT-ág engedélyezése az importálóban; a küszöböt elérő könyvek bekerülnek, a többi explicit üres eredmény.
3. Az olvasó (`sqlite_epit.py`, választó); az F213 fájljaihoz nem nyúlunk (N-F tétel).
4. README, jelentés (`naplok/F214_jelentes.md`: könyvenként előtte–utána), helyi kapuk, draft PR.

## 4. Elfogadási feltételek

Az Újszövetség és a három ószövetségi könyv mérve van; a küszöböt elérők bent vannak; a jelentésben könyvenként áll az előtte–utána szám; a draft PR fent van.

## 5. Döntésnapló

Új döntés helyőrzővel: `dontesek/uj/f214-bsb-kiegeszites-a36557.md`. A jelentés: `naplok/F214_jelentes.md`.

**Lezárás (2026-11-12).** A felhasználó szabálya: a BSB csak teljes (66 könyv) lehet a választóban; az NT mind a 27 könyve küszöb alatt, ezért a BSB kikerült (`bibliak.py`), az adat a `konkordancia/`-ban marad, import nem történt. A mérés: `naplok/F214_hiany_meres.md` (az NA28-szűrt NT-mérce csak ott szerepel). Folytatás: N174, N175.
