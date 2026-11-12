---
feladat: 213
cim: Szótári nézet az olvasóban — a BDB-szócikk olvasóbarát szókártyája (az F104 beolvad)
kod: SZOTARI_NEZET
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/f213-szotari-nezet-a55839
ad: a szónézet (/szo/<Strong>) BDB-blokkja végleges, olvasóbarát szókártya (lemmafej csukott alakokkal és rokon nyelvekkel, jelentés-tartalomjegyzék, jelentésenként glossza, használati sorok, csukott apparátus és angol eredeti, három nézetkapcsoló, jelentésszintű héber–görög pár, az F104 kétszintű „ebben a versben” jelölése); ugyanez a komponens a későbbi motívumlap-nézet alapja
kovetkezo: "Te: a mockup átnézése és jóváhagyása a design-vásznon, a „Szótári nézet” oldalon (⛔ 1.); utána a szerver"
munka: folyamat
olvas: [adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, adat/bdb_forras_javitas.tsv, adat/szotar_szakasz_cimke.tsv, adat/elofordulasok.tsv, adat/grammatikai_strongok.tsv, "konkordancia/Macula_heber_*.tsv", eszkozok/bdb_tagolas.py, eszkozok/bdb_rovidites.py, eszkozok/bdb_vj_szabaly.py, eszkozok/olvaso_szerver/, F104_BDB_MEGJELENITES_BRIEF.md]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/bdb_szokartya.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/sablonok/szo.html, eszkozok/olvaso_szerver/sablonok/_szo_panel.html, eszkozok/olvaso_szerver/statikus/olvaso.css, eszkozok/olvaso_szerver/statikus/olvaso.js, eszkozok/olvaso_szerver/konfig/elemek.toml, eszkozok/olvaso_szerver/teszt_szokartya.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/teszt_tervezo.py, eszkozok/olvaso_szerver/README.md, F104_BDB_MEGJELENITES_BRIEF.md, F213_SZOTARI_NEZET_BRIEF.md, naplok/F213_jelentes.md]
fugg: []
---

# F213_SZOTARI_NEZET_BRIEF.md — Szótári nézet az olvasóban

*FELADATOK #213 · Modell: opus · v1 · 2026.11.12 · forrás: a felhasználó 2026-11-11-i döntése („az olvasóba, a HAMART után”; „két nézet, egy komponens”; „nem akarok átmeneti megoldást”), az orkesztrátor feladatleírása (2026-11-12)*

## 1. Cél

A szónézet (`/szo/<Strong>`) BDB-blokkja ma műhelyforma: minden szelet alatt „FORRÁS: … gépi bontás” sor áll, a blokk fején az elavult „gépi szeletelés; hibás határ előfordulhat” címke (a forrás már a javított szakasztábla, SEMA 2.30). A cél egy **végleges szókártya-komponens**, amely olvasóbarát módon mutatja a teljes BDB-szócikket, és ugyanez a komponens adja a későbbi motívumlap-nézetet is, más alapállapottal.

## 2. Hatókör

**Ami kész, erre épül (nem változik).** Az adat (`adat/bdb_szakaszok.tsv` 2.30, `adat/bdb_szakasz_hu.tsv`, `adat/bdb_vers_jelentes.tsv` 2.29, `adat/bdb_forras_javitas.tsv` 2.31) és a tagolás szabálya (`eszkozok/bdb_tagolas.py`, `szeletelo_alak`; F182, F33). Ez a feladat a megjelenítésről szól: az adathoz, a tagoláshoz és a `lexikon_general.py`-hoz (F212) nem nyúl.

**Az F104 beolvad.** Az `F104_BDB_MEGJELENITES_BRIEF.md` (PR #671, a main-en) tárgya ennek a feladatnak a része: a kétszintű „ebben a versben” jelölés (erős: „a BDB itt idézi”; gyenge: „vonatkozhat”; DT178, DT689, DT693), a kattintható igehelyek, a pontos hivatkozásszám (DT692) és a „próba” felirat a mért pontossággal. Az F104 hátralévő része itt folytatódik: a felhasználói próba (H1242, H7451, H3615, versből megnyitva) és a nyitott pont (a jelentések rendjében a csak gyenge sor által idézett pont félkövére). Az F104 fejléce lezárva, a beolvadásra hivatkozva.

**Benne van — a felhasználó elvárásai.**
1. A lemmafej alatt csukva az alakok (igealakok, ill. névszónál a ragozott alakok) és a rokon nyelvek, eredet.
2. Jelentés-tartalomjegyzék; a motívumhoz tartozó jelentés megjelölve.
3. Jelentésenként félkövér glossza, alatta használati sorok: szerkezet → magyar magyarázat → igehelyek; a motívum helyei kiemelve.
4. Jelentésenként külön csukva az „Apparátus és szövegkritika” és az „Angol eredeti”.
5. Kapcsolók: olvasói nézet / szócikk egyben / minden apparátus nyitva.
6. Héber–görög pár jelentésszinten, ahol van adat.
7. A forrás egyszer, a blokk szintjén áll, nem minden szelet alatt; az elavult blokkcímke kikerül.

**Két nézet, egy komponens** (a felhasználó döntése, 2026-11-11). A szónézetben minden jelentés egyenrangú és nyitva. A motívumlap-nézetben a motívumot hordozó jelentések nyitva, a többi csukva, a motívum helyei kiemelve. Ebben a feladatban a szónézet készül el a szerveren; a motívumlap-nézet a mockupban áll, a szerveren a komponens paraméterként fogadja (alapállapot + kiemelendő helyek), a motívumlap oldala nem ennek a feladatnak a része.

**A mockup adatai (mérve, 2026-11-12).** *(proveniencia: scope=H0216, H0127 | forras=adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, adat/bdb_forras_javitas.tsv, adat/szotar_szakasz_cimke.tsv, adat/elofordulasok.tsv, konkordancia/Macula_heber_*.tsv | ts=2026-11-12)*
- H0216 (אוֹר): BDB237, 11 jelentés, mind gépi címmel (kézi címke nincs). LXX-megfelelő (Macula, szószintű): φῶς 94/120 token; jelentésenként eltér: a 6. jelentésnél φέγγος is, a 3.-nál ἥλιος, az 1.-nél φωτισμός.
- H0127 (אֲדָמָה): BDB109, 7 jelentés; az 1., 3., 4. jelentés kézi címkével (SEMA 2.40, a HAMART-001 U3-ából). A HAMART-001 10 helye a BDB 1. (1Móz 3:17, 3:23, 4:12, 8:21), 3. (1Móz 3:19, 3:23) és 4. jelentésére (1Móz 4:14, 6:7, 7:4, 7:23, Sof 1:2) esik; a Sof 1:3 csak verstartomány része. LXX: γῆ 197/225 token, minden jelentésben.
- A vászon `Irm_03_Ket_nezet` vázlata a „föld: talaj”-t egyetlen jelentésként mutatja; ez a TBESH rövid glosszája, nem BDB-jelentés. A mockup a tényleges adatot követi (három BDB-jelentés).

**Nincs benne.** A motívumlap-oldal az olvasóban; a lexikonlap 4.2 kártyája (`lexikon_general.py`, F212); a szakasztábla és a fordítás javítása; a `jelolt_marad` héber szórend-javítások (a forrás alakjában jelennek meg, ahogy ma); a `bdb_jelek.tsv` hiányzó jelei (Dl, Nö, Fleisch.: feloldatlanul állnak; ha kell, nyitott tétel).

## 3. Lépések (⛔ a kötelező megállások)

1. Modell-ellenőrzés (kért: `opus`); a bemenetek; ez a brief. — F213.0
2. **Mockup a design-vásznon** (https://claude.ai/artifact/Hq87CVsbpZCy4GCBFDedth), új „Szótári nézet” oldalon, csak saját keretekkel: H0216 szónézet (1Móz 1:3-ból megnyitva, az erős jelöléssel), H0127 szónézet, H0127 motívumlap-nézet (HAMART-001), jelek és kapcsolók. Valódi adat a fenti táblákból.
   **⛔ 1. Megállás: a felhasználó a vásznon átnézi és jóváhagyja.**
3. A szókártya-komponens a szerveren (`bdb_szokartya.py`: a használati sorok bontása és a nézet-alapállapot; `blokkok.py`: a szó-lap BDB-blokkja erre áll át), a kapcsolók (`olvaso.js`), a stílus tokenből (`olvaso.css`), az elem-regiszter (`konfig/elemek.toml`). Tesztek: `teszt_szokartya.py`, a meglévők zöldek (`python eszkozok/teszt_futtat.py`, WSL, natív `PARDES_DB`).
4. Böngészős próba-példány a `http://192.168.1.172:9765` címen, külön próba-adatbázissal; a fő példányt feljegyezni, utána visszaállítani. Az F104 próbája ugyanitt (H1242, H7451, H3615, versből).
   **⛔ 2. Megállás merge előtt: a felhasználó böngészős átnézése.**
5. Helyi kapufutás push előtt; a CI a pusholt sha-val; jelentés: `naplok/F213_jelentes.md`. A merge az orkesztrátoré.

## 4. Elfogadási feltételek

- A szónézet BDB-blokkjában a teljes szócikk szövege megmarad (semmi nem rejtődik el véglegesen, csak csukódik; „szócikk egyben” nézetben a teljes magyar szöveg folyamatosan olvasható). Teszt.
- A „FORRÁS: … gépi bontás” sor szeletenként nem áll; a forrás egyszer, a blokk végén. Az elavult „gépi szeletelés; hibás határ előfordulhat” címke nincs. Teszt.
- Jelentésenként: glossza, használati sorok, csukott „Apparátus és szövegkritika” és „Angol eredeti”. Ahol a bontás nem biztos, a sor a teljes magyar szöveg, nem találgatott szerkezet. Teszt egy bontható és egy nem bontható jelentésre.
- A kapcsolók három állapota működik, és az állapot a címben vagy a böngészőben megmarad (a döntés a mockup jóváhagyásakor).
- Az F104 szabályai változatlanul teljesülnek (DT178: erős, gyenge, „nem idézi”; pontot tippelni tilos; a „próba” felirat és a mért pontosság a kiemelés mellett). A meglévő F104-tesztek zöldek.
- A héber–görög pár csak mért adatból (a vers → jelentés sorok versei × a `token_macula` szószintű görög Strongja, a grammatikai Strongok nélkül), a token-számmal; adat nélkül nem áll.
- A regiszter-őr zöld; új méret csak tokenből.

## 5. Döntésnapló

- (a mockup jóváhagyásakor rögzítendő, helyőrzővel a `dontesek/uj/f213-szotari-nezet-a55839.md`-be: a glossza szabálya (kézi címke, ennek híján a magyar szöveg az első héber szóig vagy hivatkozásig), a használati sor bontási szabálya, a kapcsoló-állapot helye, a jelentésszintű LXX-pár forrása és küszöbe.)
