---
feladat: 210
cim: Bibliaválasztó az olvasó könyvválasztójának legfelső szintjén
kod: OLVASO_BIBLIAVALASZTO
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/f210-bibliavalaszto-b8d821
ad: az olvasó könyvválasztójának legfelső szintje a bibliaválasztó (Károli 1908 az alap; modernizált Károli, TAHOT, TAGNT, Septuaginta, KJV, BSB, Targum, Vulgata), a fejléc morzsája a választott Bibliát is mutatja; a hiányzó szövegek az adatbázis-építőből
kovetkezo: "Folytatás: a szerveroldali választó és a tesztek; utána a draft PR, a felhasználó böngészős átnézése (⛔)"
munka: folyamat
olvas: [eszkozok/olvaso_szerver/, eszkozok/sqlite_epit.py, adat/karoli_modern/karoli_modern.tsv, adat/karoli_modern/karoli_modern_versek.tsv, konkordancia/KJV_teljes_szoveg.tsv, konkordancia/Targum_PD.tsv, konkordancia/Vulgata_Clementina.tsv, konkordancia/VISSZHANG_README.md, adat/licencek.tsv]
ir: [eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/bibliak.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/sablonok/alap.html, eszkozok/olvaso_szerver/sablonok/fejezet.html, eszkozok/olvaso_szerver/statikus/olvaso.js, eszkozok/olvaso_szerver/statikus/olvaso.css, eszkozok/olvaso_szerver/konfig/elemek.toml, eszkozok/olvaso_szerver/teszt_bibliavalaszto.py, eszkozok/olvaso_szerver/README.md, F210_OLVASO_BIBLIAVALASZTO_BRIEF.md, naplok/F210_jelentes.md]
fugg: []
nem_fugg: [137]
---

# F210_OLVASO_BIBLIAVALASZTO_BRIEF.md — Bibliaválasztó az olvasóban

*FELADATOK #210 · Modell: opus · v1 · 2026.11.12*

## 1. Cél

A felhasználó kérése (2026-11-12): „legyen könyv választóba / biblia választó / a legfelső szinten. - történjen meg a serveren / külön session”. A mérce a design-vászon `Mk_08_Konyvvalaszto` és `Mk_01_Fejlec` kerete (az irányelv-oldal 11. alapelve): a párbeszédablak címe „Biblia és könyv kiválasztása”, legfelül a Biblia csoportosítva, alatta a könyvrács, majd a fejezet; a morzsa „Károli 1908 · 1Móz 1 ▾”.

## 2. Hatókör

**Benne van.**
- A bibliák (a mockup csoportjai szerint): Magyar — Károli 1908 (alap), modernizált Károli; Eredeti nyelv — héber ÓSZ (TAHOT), görög ÚSZ (TAGNT), Septuaginta; Angol — KJV, BSB; Ókori fordítás — Targum (csak ÓSZ), Vulgata Clementina.
- A választás a címben marad (`?biblia=<kód>`); a Károli az alap, paraméter nélkül; a meglévő Károli-útvonalak változatlanok.
- A Strong-jelölt szövegben (Károli, modern Károli, TAHOT, TAGNT, LXX, KJV, BSB) a szóra koppintás a szópanelt nyitja; a Strong nélküli szöveg (Targum, Vulgata) versenként olvasható, és a felület ezt kimondja.
- Versszámozás: a Targum és a Vulgata a forrás saját számozását mutatja (`konkordancia/VISSZHANG_README.md` 1.); versegyezést nem állítunk, a lap jelzi, hogy a számozás eltérhet a Károlitól. A többi szöveg az adatbázisban a Károli-vers kulcsán áll (a TAHOT/TAGNT és a BSB kulcsa a Károli-vers; a KJV és az LXX a meglévő leképező táblával).
- Ami a `pardes.db`-ből hiányzik (modern Károli, a KJV teljes szövege, Targum, Vulgata), az az építőbe (`sqlite_epit.py`) kerül, saját licencsorral.

**Nincs benne.** A #137 (modern Károli a keresőben) és a vers-lap 1908/modern kapcsolója: a #137 a most felvett `szoveg_modern`/`token_modern` táblát használhatja. A ASV és a régi háromkönyves KJV/ASV fájlok nem kerülnek a választóba. A #703 fájljai (`bdb_szelet.py`, `bdb_vers_jelentes.py`, `teszt_bdb_vers_jelentes.py`) és a `nyilt_*` csomagok érintetlenek.

## 3. Lépések

1. Felmérés: mi van a `pardes.db`-ben (a jelentés 1. szakasza).
2. Építő: `szoveg_modern`, `token_modern`, `szoveg_kjv`, `szoveg_targum`, `szoveg_vulgata`; licenc a `licencek.tsv` meglévő soraiból.
3. Szerver: a bibliák regisztere (`bibliak.py`), a fejezetlap a választott Bibliával, a választó és a morzsa, a JS a paraméter megtartásával.
4. Tesztek (`teszt_bibliavalaszto.py`), a teljes tesztkör `python eszkozok/teszt_futtat.py`.
5. Draft PR. ⛔ A felhasználó a böngészőben átnézi (a mockup és a #60 pilot mellé téve); merge csak az orkesztrátortól.

## 4. Elfogadási feltételek

- A választó a mockup szerint működik a szerveren; mindegyik felvett Biblia egy fejezete olvasható (1Móz 1, és egy ÚSZ-fejezet ott, ahol van).
- A Strong-os szövegekben a szópanel működik; a Targum és a Vulgata lapja kimondja, hogy versenként olvasható, és hogy a számozás a forrásé.
- A Károli-útvonalak és a meglévő tesztek változatlanul zöldek.

## 5. Döntésnapló

A jelentés: `naplok/F210_jelentes.md`.
