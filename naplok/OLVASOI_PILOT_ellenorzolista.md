# Olvasói pilot — „csak adat” ellenőrzőlista (F60, M1; bővítve: F60.5, v2)

*Kézi lista; a gépi része a `eszkozok/olvaso_pilot/teszt_olvaso_pilot.py` `CsakAdat` osztálya. A független ellenőr külön ellenőrzi.*

**Mérce (brief M1):** a sablon minden szövege vagy **(a)** felületi utasítás / jelmagyarázat (mire lehet kattintani, mit jelent egy jelölés), vagy **(b)** adatból jön (számolt érték, adatállapot-jelzés, a forrástábla szövege). Ami egyik sem, kikerül. Három szöveg határeset (**c**: a jelleg vagy a módszer közlése); ezeket a felhasználói átnézésnél (M3) érdemes eldönteni.

**v2 (2026-10-07):** a bővítés új adatot nem állít elő; minden új blokk meglévő tábla sora, jelleggel, adatforrás-jelzéssel és licenccel (a „?” súgóban: licenc-címke, és ahol a `licencek.tsv` rögzíti: tisztázatlan / nem kereskedelmi / share-alike). Magyarázó szöveg az új blokkokban sincs.

## 1. Blokkok és jelleg-címkék (gépi teszt: minden blokk-cím egyezik egy címkézett forrásbejegyzéssel)

| Blokk (cím) | Hol | Jelleg | Adatforrás (`?` jel) |
|---|---|---|---|
| Károli-szöveg | vers-lap | forrásadat + modell-kimenet | Karoli_1908; adat/karoli_strong/parok_*.tsv (az aláhúzás) |
| Versszámozás | vers-lap | forrásadat | Karoli_versmegfeleltetes; LXX_OS (a KJV-kulcs sora: gépi illesztés, a „Forrás” mutatja) |
| Héber szöveg | vers-lap | forrásadat + gépi feldolgozás | TAHOT; Macula_heber; LXX_OS; morf_kulcs_heber; morf_nyelv_aramai (az igealak feloldása) |
| Septuaginta (LXX, Rahlfs) | vers-lap | forrásadat | LXX_OS |
| Kereszthivatkozások (TSK) | vers-lap | forrásadat | TSK |
| Károli-kereszthivatkozások | vers-lap | forrásadat | Karoli_KH |
| **Angol szó szavanként (BSB)** | vers-lap | forrásadat + gépi feldolgozás (MT-kulcs) | BSB_Strongs; Karoli_versmegfeleltetes |
| **Angol szó szavanként (KJV)** | vers-lap | forrásadat + gépi feldolgozás (KJV-kulcs) | KJV_Strongs_teljes; LXX_OS |
| **Témák (Nave)** | vers-lap | forrásadat + gépi feldolgozás (a tartomány bontása, KJV-kulcs) | Nave_basokant; LXX_OS |
| **Tulajdonnevek (TIPNR)** | vers-lap | forrásadat + gépi feldolgozás (illesztés a vers Strong-számaival) | TIPNR |
| **Motívumadat (adatréteg)** | vers-lap | forrásadat | adat/elofordulasok.tsv + motivumok.tsv (projekt_adat); soronként a sor proveniencia-mezője |
| **Igehely-kapcsolatok (adatréteg)** | vers-lap | forrásadat | adat/kapcsolatok.tsv (projekt_adat) |
| **LXX-fordítói döntések (adatréteg)** | vers-lap | forrásadat | adat/lxx_dontesek.tsv (projekt_adat) |
| **LXX versszintű együttelőfordulás** | vers-lap | forrásadat | LXX_versszintu_parok (nem szóillesztés) |
| **LXX többlet és számozási eltérés** | vers-lap | forrásadat | LXX_tobblet_szakaszok, Verzifikacios_elteres_tabla (Versifikacios_tablak) |
| Szó adatai (héber) | szó-lap | forrásadat + gépi feldolgozás (számolás) + modell-kimenet (Károli-párok) | Strong_szotar; TAHOT; parok_*.tsv |
| Ebben a versben | szó-lap | forrásadat + gépi feldolgozás + modell-kimenet („Károli itt”) | Macula_heber; UBS_DBH; LXX_OS; morf_kulcs_heber; parok_*.tsv |
| Így fordítja Károli | szó-lap | modell-kimenet | parok_*.tsv |
| BDB-szócikk apparátusokra bontva / Jelentés (BDB…) | szó-lap | forrásadat + modell-kimenet (a magyar) + gépi feldolgozás (a bontás, az alias) | BDB (forditasok.tsv; BDB_teljes_unabridged.tsv); BDB_strong_alias (projekt_adat) |
| Görög megfelelő a Septuagintában | szó-lap | forrásadat | lxx_bridge |
| **Szemantikai domén (SDBH)** | szó-lap (héber) | forrásadat | SDBH_domenek + SDBH_SDGNT_domenfa (CC BY-SA 4.0) |
| **SECE-szócikk (héber)** | szó-lap (héber) | forrásadat | SECE_H_teljes |
| **TWOT- és BDB-azonosító (OSHL)** | szó-lap (héber) | forrásadat | OSHL_lexikalis_index |
| **Bővített Strong-szócikk (TBESH)** | szó-lap (héber) | forrásadat | TBESH.txt (licenc-aggály: Online Bible-eredetű jelentés-lista) |
| **translationWords (tW)** | szó-lap (héber, görög) | forrásadat | tW_szocikkek (CC BY-SA 4.0) |
| Szó adatai (görög) | görög szó-lap | forrásadat + gépi feldolgozás (számolás) | TBESG; TAGNT; lxx_bridge |
| Jelentés magyarul | görög szó-lap | modell-kimenet | Thayer; UBS_DNTG (forditasok.tsv) |
| Jelentés | görög szó-lap | forrásadat | TBESG |
| Héber háttér | görög szó-lap | forrásadat | lxx_bridge |
| Az Újszövetségben | görög szó-lap | forrásadat | TAGNT; Karoli_1908; UBS_DNTG (az előfordulás jelentése) |
| Szótári szöveg (angol) | görög szó-lap | forrásadat | TBESG; Thayer |
| **Szemantikai domén (SDGNT)** | görög szó-lap | forrásadat | SDGNT_domenek + domenfa (CC BY-SA 4.0) |
| **UBS DNTG jelentések (angol)** | görög szó-lap | forrásadat | UBS_DNTG_jelentesek (CC BY-SA 4.0) |
| **LSJ-szócikk (angol)** | görög szó-lap | forrásadat | LSJ_teljes (CC BY-SA 4.0, Perseus) |
| **Mounce-szótár (MCGED)** | görög szó-lap | forrásadat | MCGED_teljes (© Mounce, nem kereskedelmi; a kötelező megjelölés a blokkban látszik) |
| **SECE-szócikk (görög)** | görög szó-lap | forrásadat | SECE_G_teljes |

Javított hiba (F60.1): a héber lap „Jelentés (BDB…)” címe korábban a görög lap „Jelentés” (TBESG) bejegyzéséhez illeszkedett, tehát hibás forrást jelzett. A blokk saját bejegyzést kapott (BDB; forrásadat + modell-kimenet).

## 2. Statikus szövegek

**(a) felületi utasítás / jelmagyarázat:** a „Hogyan olvasd ezt az oldalt?” lista (5 pont); „Kapcsolt szavak jelölése”; fülek (Szó, Vers részletei, Bezárás); a lábléc „Aláhúzott szó …” és „Arany jelölés …” sora; a „Jobbról balra. Szavanként: …” és a „A keretes, aláhúzott görög szavakra kattintva …” segédsor; „Lenyit/Rövidebben/A teljes szócikk elrejtése” gombok; „Forrás” nyitó; v2: az angol szó-blokkok „Kulcs: … · a tábla számozás-jelölése: … Kattintható: a héber szó lapja.” sora (kulcs-jelzés + utasítás); a lenyitó feliratok („A szócikk”, „További jelentés”, „Fejezet-szintű hivatkozások”).

**(b) adatból jön / adatállapot-jelzés:** fejléc-címkék (versek száma, szó-lapok száma, „BDB magyarul: x/y”, „Károli–Strong: n könyv”: számolás); „Magyar fordítás nincs · az angol eredeti áll” és társai (a `bdb_hu` mező üres); „Nincs TSK-hivatkozás”, „Ehhez a vershez a Károli-kiadás nem ad kereszthivatkozást”, „Nincs Károli-pár a feldolgozott könyvekben”, „A lxx_bridge nem ad párt (kevesebb mint 3 egyezés)” (a híd-tábla legkisebb darabszáma 3: mérve), „A szó az Újszövetségben nem fordul elő (vagy a TAGNT-kivonatban nincs)”; „A szó az Újszövetség Károli-szövegében nincs kiemelve (a párosítás könyvei: …)” (a könyvlistát a párosítás-fájlok adják); „A UBS-szótár ehhez az előforduláshoz nem ad jelentés-besorolást” (üres `ubs` mező); a számok („előfordulás az ÓSZ-ben”, „Károli-pár (n magas)”, „az első n a m-ből”); a versszám-sor („a számozás egyezik / eltér / a két tábla ellentmond”: a két tábla összevetése; v2: „KJV-kulcs (a pilot illesztése)”, a kulcs forrása); v2: „Nincs sor ehhez a szóhoz ebben a táblában”, „Nincs sor erre a vershez”, „Nincs Nave-sor erre a vershez (KJV-kulcs: …)”, „Nincs TIPNR-sor erre a vershez”, „A táblában nincs sor erre a kulcsra (…)” (üres eredmény jelzése, nem pótlás), „Az első n a m-ből”; „A szócikk a(z) H0113 Strong-szám alatt áll (BDB125, szövegi hasonlóság …)” (az alias-sor adatai); „Az SDBH/SDGNT nem ad domént ehhez a szóhoz …” (üres eredmény nem negatív lelet).

**(c) határesetek (felhasználói átnézésre):**
1. *„Gépi szeletelés (próba): a határokat a szócikk saját jelölői adják …; hibás határ előfordulhat.”* — a gépi feldolgozás jellegének közlése a lapon; a „?” súgóba is átkerülhetne.
2. *Lábléc: „Az előfordulásszám a TAHOT-kivonatból jön, amely nem teljes (pl. a Zsolt 88/89/140/142 hiányzik).”* — adatminőségi jelzés a `CLAUDE.md`-ből (kézi állítás, nem a pilot méri).
3. *Lábléc: „… a Macula-illesztés pontossága az F17 napló szerint kb. 78% (átvett szám, naplok/F17_import_naplo.md)”* — átvett szám (a napló 78,3%-ot ad); nem a pilot méri.
4. *Lábléc: „Igealak: a Macula nyers morfológiai kódja mellett a magyar feloldás az adat/morf_kulcs_heber.tsv-ből jön (gépi feldolgozás; …)”* és *„Angol szó szavanként: a BSB „Számozás” oszlopa jelzi a versszámozást; a KJV-kulcs a LXX_OS KJV-oszlopából jön (gépi illesztés). A Nave-témák KJV-számozású hivatkozások …”* — módszer-közlés a lábléc-ben (a jelleg-címke már jelzi a gépi feldolgozást).
5. *A „UBS … CC BY-SA 4.0” lábléc-sor* — licenc-közlés. Az MCGED blokk alatti kötelező forrásmegjelölés („© Mounce 1993 …”) a `licencek.tsv` `kotelezo_megjeloles` mezőjéből jön.
6. v2: a **TBESH** súgója a licenc-aggályt is közli („az Online Bible-eredetű: a licenc-kérdés nyitott”) — ez a `licencek.tsv` F33f-megjegyzésén és a TBESH-fejlécen alapul; közzététel előtt jogi átnézés kell.

**Kikerült szöveg (F60.0–F60.1):** a feladatszámok (#22, #38, #7), „folyamatban”, „halasztva”, a „teremtéstörténet” és az „1Mózes 1:1–2:3” rögzített felirat, a „1–5Móz, Józs” rögzített felsorolás. A teszt (`test_nincs_feladatszam_es_szakaszra_rogzitett_szoveg`) őrzi. v2: „a kód jelkulcsa nincs a repóban” (a jelkulcs azóta van: `adat/morf_kulcs_heber.tsv`).

## 3. Ami nem kerül a lapra
Magyarázó szöveg (szószedet), motívum-értelmezés: a #59 jóváhagyott szószedetén át jöhet később. A `LXX_versificacios_terkep.tsv`, az `OSHL_BDB_igehelyek.tsv`, az `adat/jeloltek.tsv` és a kiejtés-szabálytáblák megjelenítése szándékosan kimaradt (indoklás: `naplok/OLVASOI_PILOT_adatfelmeres.md`).
