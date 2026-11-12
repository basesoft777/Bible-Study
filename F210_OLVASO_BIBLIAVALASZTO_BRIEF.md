---
feladat: 210
cim: Bibliaválasztó az olvasó könyvválasztójának legfelső szintjén
kod: OLVASO_BIBLIAVALASZTO
tipus: feladat
fazis: folyamat
modell: opus
allapot: lezarva
ag: claude/f210-bibliavalaszto-b8d821
pr: 717
ad: az olvasó könyvválasztójának legfelső szintje a bibliaválasztó csak szószintű Strong-kapcsolatú szöveggel (Károli 1908 az alap; modernizált Károli, TAHOT, TAGNT, Septuaginta, KJV, BSB), a fejléc morzsája a választott Bibliát is mutatja; a hiányzó szövegek az adatbázis-építőből
kovetkezo: "lezárva: a #717 mergelve (33abfd1c), a fő pardes.db újraépítve, a fő példány a main-en fut; nyitott: N171–N173, DT811 🟡"
lezarva_osszegzes: "Bibliaválasztó az olvasó könyvválasztójának legfelső szintjén, csak szószintű Strong-kapcsolatú szöveggel (Károli 1908, modern Károli, TAHOT, TAGNT, Septuaginta, KJV, BSB); a ?biblia= cím, az építő három új táblája (#717)"
munka: folyamat
olvas: [eszkozok/olvaso_szerver/, eszkozok/sqlite_epit.py, adat/karoli_modern/karoli_modern.tsv, adat/karoli_modern/karoli_modern_versek.tsv, konkordancia/KJV_teljes_szoveg.tsv, adat/licencek.tsv]
ir: [eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/bibliak.py, eszkozok/olvaso_szerver/sablonok/alap.html, eszkozok/olvaso_szerver/sablonok/fejezet.html, eszkozok/olvaso_szerver/statikus/olvaso.js, eszkozok/olvaso_szerver/statikus/olvaso.css, eszkozok/olvaso_szerver/konfig/elemek.toml, eszkozok/olvaso_szerver/teszt_bibliavalaszto.py, eszkozok/olvaso_szerver/teszt_tervezo.py, eszkozok/olvaso_szerver/README.md, F210_OLVASO_BIBLIAVALASZTO_BRIEF.md, naplok/F210_jelentes.md]
fugg: []
nem_fugg: [101, 122, 135, 137, 140, 147, 149, 181, 195]
---

# F210_OLVASO_BIBLIAVALASZTO_BRIEF.md — Bibliaválasztó az olvasóban

*FELADATOK #210 · Modell: opus · v2 · 2026.11.12 (v2: hatókör-szűkítés a felhasználó szavával, l. 2.)*

## 1. Cél

A felhasználó kérése (2026-11-12): „legyen könyv választóba / biblia választó / a legfelső szinten. - történjen meg a serveren / külön session”. A mérce a design-vászon `Mk_08_Konyvvalaszto` és `Mk_01_Fejlec` kerete (az irányelv-oldal 11. alapelve): a párbeszédablak címe „Biblia és könyv kiválasztása”, legfelül a Biblia csoportosítva, alatta a könyvrács, majd a fejezet; a morzsa „Károli 1908 · 1Móz 1 ▾”.

## 2. Hatókör

**Hatókör-szűkítés (v2).** A felhasználó (2026-11-12, az orkesztrátoron át): „meggondoltam ahol nincs stronf kapcsolat olyan szöveg ne kerüljön be”. A választóba csak szószintű Strong-kapcsolatú szöveg kerül; a Targum és a Vulgata kimarad, és a „csak versenként olvasható” ág is. Részleges Strong-lefedettségnél mérés és jelzés, automatikus felvétel nincs (a mérés: a jelentés 2. szakasza).

**Benne van.**
- A bibliák (a mockup csoportjai szerint): Magyar — Károli 1908 (alap), modernizált Károli; Eredeti nyelv — héber ÓSZ (TAHOT), görög ÚSZ (TAGNT), Septuaginta (az `LXX_OS` szavanként Strong-számos); Angol — KJV (`KJV_Strongs_teljes.tsv`), BSB. A kiadás, amely egy Biblia Strong-rétegét kizárja (a KJV-címkék a `nyilvanos` és a `kereskedelmi` kiadásban, DT124), abban a Biblia nem jelenik meg.
- A választás a címben marad (`?biblia=<kód>`); a Károli az alap, paraméter nélkül; a meglévő Károli-útvonalak változatlanok.
- A szóra koppintás a szópanelt nyitja (a Károli-vers kontextusával).
- Versszámozás: minden szöveg az adatbázisban a Károli-vers kulcsán áll (a TAHOT/TAGNT és a BSB kulcsa a Károli-vers; a KJV és az LXX a meglévő leképező táblával); az eltérő forrásszám a vers elején áll.
- Ami a `pardes.db`-ből hiányzik (modern Károli, a KJV teljes szövege), az az építőbe (`sqlite_epit.py`) kerül, saját licencsorral.

**Nincs benne.** A Targum és a Vulgata (Strong-kapcsolat nélkül; az építő sem veszi fel őket). A #137 (modern Károli a keresőben) és a vers-lap 1908/modern kapcsolója: a #137 a most felvett `szoveg_modern`/`token_modern` táblát használhatja. A ASV és a régi háromkönyves KJV/ASV fájlok nem kerülnek a választóba. A #703 fájljai (`bdb_szelet.py`, `bdb_vers_jelentes.py`, `teszt_bdb_vers_jelentes.py`) és a `nyilt_*` csomagok érintetlenek.

## 3. Lépések

1. Felmérés: mi van a `pardes.db`-ben (a jelentés 1. szakasza).
2. Építő: `szoveg_modern`, `token_modern`, `szoveg_kjv`; licenc a `licencek.tsv` meglévő soraiból. A Strong-lefedettség mérése szövegenként.
3. Szerver: a bibliák regisztere (`bibliak.py`), a fejezetlap a választott Bibliával, a választó és a morzsa, a JS a paraméter megtartásával.
4. Tesztek (`teszt_bibliavalaszto.py`), a teljes tesztkör `python eszkozok/teszt_futtat.py`.
5. Draft PR. ⛔ A felhasználó a böngészőben átnézi (a mockup és a #60 pilot mellé téve); merge csak az orkesztrátortól.

## 4. Elfogadási feltételek

- A választó a mockup szerint működik a szerveren; mindegyik felvett Biblia egy fejezete olvasható (1Móz 1, és egy ÚSZ-fejezet ott, ahol van).
- A szópanel minden felvett szövegben működik; Strong-kapcsolat nélküli szöveg a választóban nincs (a régi `?biblia=targum|vulgata` cím az alapra esik vissza).
- A Károli-útvonalak és a meglévő tesztek változatlanul zöldek.

## 5. Döntésnapló

A jelentés: `naplok/F210_jelentes.md`.
