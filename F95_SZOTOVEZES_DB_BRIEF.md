---
feladat: 95
cim: A szótári alak oszlopai a pardes.db-ben — a #94 kimenetének betöltése, index, frissességi teszt
kod: SZOTOVEZES_DB
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: fut
ag: claude/f95-szotovezes-db
ad: a pardes.db új táblája a Károli minden szóalakjához (szótári alak, mai szótári alak, alapige, további elfogadható alak, módszer, régies jegy) táblaszintű licenccel és meta-sorral; a token_karoli tokenjeihez kapcsolható pontos-alak kulccsal; indexek a szótári alak, a mai alak, az alapige és a további elfogadható alak szerinti kereséshez; a (c) keresési mód (szótári alak VAGY Strong) mintalekérdezése mérve; frissességi teszt a forrás-TSV-re
kovetkezo: "M1 (építés), M2 (mérés), M3 (zárás) — az M0 ⛔ jóváhagyva (DT-F95a)"
olvas: [adat/szoto/karoli_szotari_alak.tsv, adat/SEMA.md, adat/licencek.tsv, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/olvaso_pilot/db_meres.py, naplok/SQLITE_EPIT_meres.md, naplok/SZOTOVEZES_zaras.md, "adat/karoli_strong/szavak_*.tsv", F76_OLVASOI_KONKORDANCIA_BRIEF.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/olvaso_pilot/db_meres.py, adat/SEMA.md, naplok/SQLITE_EPIT_meres.md, naplok/SZOTOVEZES_DB_M0.md, naplok/SZOTOVEZES_DB_zaras.md]
fugg: [92, 94]
---

# F95_SZOTOVEZES_DB_BRIEF.md — A szótári alak oszlopai a pardes.db-ben

*FELADATOK #95 · Modell: sonnet · v1 · 2026.10.13 · a csonk (F94.0b) kitöltése; forrás: `F94_SZOTOVEZES_BRIEF.md` 3. pont („A `pardes.db`-oszlop — külön feladat”), `naplok/SZOTOVEZES_zaras.md`, a felhasználó döntései a #94-ben (DT130, DT-F94a–f; a kiadott hibrid a C+K, a simplemma csak mérce)*

## 1. Cél

A #94 a Károli minden szóalakjához előállította a szótári alakot (`adat/szoto/karoli_szotari_alak.tsv`, 66 824 alak, generált, C+K, simplemma nélkül). A #95 ezt betölti a `pardes.db`-be úgy, hogy a #76 kutatói felülete a szótári alakra, a mai helyesírású szótári alakra, az alapigére és a további elfogadható alakra kereshessen, és a találatot a Károli-tokenhez (vers, sorszám, Strong) kösse.

A #94 mérése szerint a pontosság a **(c) módra** érvényes: szótári alak VAGY Strong (M2 (c) a 4. mintán 98,4%, a K tábla nélküli lemmákon 98,0%); tisztán szótári alakra (a) a K nélküli lemmákon 91,8% (Kiegészítés B, `naplok/SZOTOVEZES_zaras.md` 7. sor). A #95 ezért a (c) mód lekérdezését is előkészíti és méri; a felületet nem építi (az a #76).

## 2. Hatókör

**Benne van**

- **Alakszintű tábla** a `karoli_szotari_alak.tsv`-ből, a TSV oszlopaival (`alak`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato`, `modszer`, `szabaly_forras`, `regies_jegy`), `meta`-sorral (sorszám, hash) és táblaszintű licenccel (DT113): a `SZARMAZTATOTT_LICENC` új kulcsa a `szoto_tablak` licencsorra. A `simplemma_nyelvi_adat` kulcs nem használható (DT-F94e: nem kerül kiadásra).
- **A további elfogadható alak kereshetővé tétele:** a `|`-vel elválasztott `tovabbi_elfogadhato` mezőből egy alak–keresőalak párokat tartó kereső tábla vagy nézet (pl. alak → {szótári alak, mai alak, alapige, további alakok}), indexelve. A pontos forma az M0 táblaterv része.
- **Kapcsolás a tokenekhez:** a `token_karoli.szo` (pontos alak, kis-/nagybetű-érzékeny) = `alak`. A kulcs **nem** a `szo_kis`: az a kötőjelet is törli és kisbetűsít, a tábla viszont kis-/nagybetű-érzékeny (SEMA 2.27). Ha a `token_karoli.szo`-n nincs index, az M0 javasolja.
- **A nem illeszkedő tokenek mérése és kezelése:** az előmérés szerint (`token_karoli` 484 820 `hu` tokenje) 483 746 (99,78%) talál; a többi szinte mind kötőjeles alak darabja, mert a `token_karoli` a kötőjeles alakot szétvágja (*Adsz-é* → *Adsz*, *é*), a tábla viszont egyben tartja (1 502 kötőjeles `alak`). Az M0 megméri, és javaslatot tesz (pl. tartalékkulcs, külön jelölés, vagy dokumentált hiány); a döntés ⛔.
- **A (c) mód mintalekérdezése:** szótári alakra (vagy mai alakra, alapigére, további alakra) keresve a tokenek, VAGY a Strong-ágon (a lemma tokenjeinek fő Strong-száma) talált tokenek uniója. A #95 a lekérdezést és a mérését adja (`db_meres.py`), a felületet nem.
- **Tesztek** (`eszkozok/teszt_sqlite_epit.py`): betöltés és licenc; sorszám = a TSV adatsorainak száma; a 12188. sor (`alak	alak	alak…`, a Károli valódi *alak* szava) nem vész el fejlécként (az első nem-`#` sor a fejléc, SEMA 2.27); a tábla nem tartalmaz `modszer=simplemma` sort; a kereső lekérdezés indexet használ (`EXPLAIN QUERY PLAN`, minta: `test_f92_magyar_szo_index`); G2 (kétszeri építés, azonos hash).
- **Frissesség:** a `db_meres.py` `TSV_FORRAS` (és ha kell, `EGYEZO_SORSZAM`) felveszi a `adat/szoto/karoli_szotari_alak.tsv`-t; a D5 erre a táblára is fut.
- **Dokumentáció:** SEMA (a `pardes.db` táblaleírásai közé az új tábla/nézet), `naplok/SQLITE_EPIT_meres.md` frissítése az építővel.

**Nincs benne**

- A szótári alakok javítása: a tábla generált (`# GENERÁLT` fejléc), a hiba a #94 eszközeiben (kivételtábla, szabály) javul, és újragenerálódik; a #95 csak betölt. Az ismert hibák (`naplok/SZOTOVEZES_zaras.md` 9. sor; N-F94g, N-F94h) a betöltött táblában is ott vannak, ezt a zárójelentés jelzi.
- A versen belüli, tokenszintű jelenségek: a különírt vonatkozó névmás (*a melyet*, N-F94f), a hátravetett és az előre vetett igekötő (N-F94d, N-F94a). Ezek a #76 vagy a DT128 (#96) dolga; a #95 legfeljebb méri, hogy a kereső mintalekérdezése mennyit veszít miattuk, és a zárójelentésben jelzi.
- A `token_karoli` ÚSZ-hiánya (Mt, Mk, Lk, Jn, ApCsel, Róm, 1–2Kor, Jel nincs párosítva): a tábla a teljes Károlit fedi, a token-kapcsolás csak a párosított könyveken él. A #95 ezt méri és dokumentálja, nem pótolja.
- A kutatói felület és a keresés UI-ja (#76); a modernizált szövegréteg (#96, DT128); a `regies_jegy` értelmezése (a modernizálás jelöltként kezeli, N-F94h).

## 3. Lépések

- **M0 — felmérés (csak olvas).** Táblaterv (táblák vagy nézetek, oszlopok, kulcsok, indexek), a kapcsolási kulcs (`token_karoli.szo` = `alak`), a betöltendő sorok száma és a várható méret; a nem illeszkedő tokenek száma és osztályai (kötőjeles darab, ÚSZ-hiány, egyéb), javaslattal; a (c) mód lekérdezésének vázlata; a frissességi teszt helye. Jelentés: `naplok/SZOTOVEZES_DB_M0.md`, proveniencia-sorokkal. ⛔ A táblaterv, a kapcsolási kulcs és a nem illeszkedő tokenek kezelésének jóváhagyása.
- **M1 — építés.** Az új betöltő az építőben (az `_adat_tablak` alkönyvtárat nem olvas, ezért saját metódus, a `token_karoli` épülése után), licenccel és meta-sorral; tesztek; újraépítés (`--mod minta`, majd `--mod teljes`, `--ketszer`).
- **M2 — mérés.** `db_meres.py`: D5 (frissesség) az új táblára is; a kapcsolási arány (illeszkedő tokenek aránya, könyvcsoportonként); a (c) mód mintalekérdezésének ideje és találati száma 10 gyakori és 10 ritka lemmára (a lemmalista az M0-ban rögzített, a mérés előtt); proveniencia-sorral a jelentésben.
- **M3 — zárás.** Zárójelentés (`naplok/SZOTOVEZES_DB_zaras.md`), független ellenőr, draft PR.

## 4. Elfogadás

- **K1.** A tábla sorszáma egyezik a TSV adatsorainak számával (66 824 az átvételkor), a 12188. sor (*alak*) benne van; `modszer=simplemma` sor 0; a táblának van `tabla_licenc` sora (`szoto_tablak`) és `hash:` meta-sora.
- **K2.** A kapcsolási arány a párosított `hu` tokeneken legalább az előmérés 99,78%-a; minden nem illeszkedő token osztályozva, a kezelés az M0 döntése szerint.
- **K3.** A D5: a `meta` hash egyezik a forrás-TSV mostani állapotával (a #76 K4-ének feltétele).
- **K4.** A szótári alakra, a mai alakra, az alapigére és a további elfogadható alakra keresés indexet használ, és 100 ms alatt fut ugyanazon a gépen, ahol a #92 K5 mérése; a (c) mód mintalekérdezése is mérve, proveniencia-sorral.
- **K5.** A tesztek zöldek (`python eszkozok/teszt_sqlite_epit.py`, kézi futtatás: a CI nem futtatja), a CI zöld, a független ellenőr eltérés nélkül zár.

## 5. Kapcsolódás

#94 (SZOTOVEZES: a tábla, a mérés, a (c) mód), #92 (PARDES_DB_OLVASOI: a minta az építőhöz, K5), #79 (SQLITE_EPIT), #89 (LICENC_RENDEZES, DT113), #76 (OLVASOI_KONKORDANCIA: a fogyasztó, K4), #96 (KAROLI_MODERN), N-F94a, d, f, g, h.

## 6. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-13 | A csonk kitöltése a #94 lezárása után; a kapcsolási kulcs a pontos alak (`token_karoli.szo`), nem a `szo_kis`; a (c) mód lekérdezése a #95-ben mérve, a felület a #76-ban | felhasználó (chat, 2026-10-13: „írd meg a #95 briefjét”); `naplok/SZOTOVEZES_zaras.md` |
| v1.1 | 2026-10-13 | Az M0 ⛔ jóváhagyása: `szotari_alak` + `szotari_kereso` + részleges token-index; kulcs `token_karoli.szo = alak` (pontos); (A) `szotari_token_kotojeles` segédtábla (4 750 darab-token), a 6 felfüggesztett kötőjeles token dokumentált hiány; (c) mód Strong-ága a `token_par.strong`-ból, `grammatikai_strongok` szűréssel, a 100 ms-os küszöb az (a) módra és a kereső táblára, a (c) mód mérve és jelentve (DT-F95a) | felhasználó (chat, „mehet”, az orkesztrátoron át); `naplok/SZOTOVEZES_DB_M0.md` |
