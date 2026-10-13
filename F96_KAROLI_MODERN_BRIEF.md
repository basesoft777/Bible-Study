---
feladat: 96
cim: Modernizált Károli-szövegréteg — helyesírás és igealak, szókincs és szórend nélkül, az 1908-as szövegből generálva (DT128)
kod: KAROLI_MODERN
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: brief_kell
ad: a Károli 1908 modernizált szövegrétege (helyesírás + igealak; szórend, szókincs, írásjel, betoldás-jelölés változatlan), szavankénti cserével, a Károli–Strong párosítás szavanként átvihető, a kieső segédigei vala jelölve; generált tábla az 1908-as szöveg mellett, nem helyette; két lépcső (helyesírás, majd igeragozás és vala), felhasználó által ellenőrzött mintán mérve
kovetkezo: "brief kell a #94 lezárása után (sorrend: #94 → #96, a #95-tel párhuzamosan); nyitott: a Hunspell hu_HU licencdöntés (N-F94b)"
olvas: [adat/szoto/, konkordancia/Karoli_1908.tsv, "adat/karoli_strong/*", adat/SEMA.md, adat/licencek.tsv, DONTESEK.md]
ir: [eszkozok/karoli_modern/, adat/karoli_modern/, naplok/KAROLI_MODERN_meres.md]
fugg: [94]
nem_fugg: [22]
---

# F96_KAROLI_MODERN_BRIEF — csonk

*FELADATOK #96 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza; v1; a tartalom forrása: DT128 (a felhasználó döntése, chat, 2026-10-13: a modernizálás szintje az, amit a Bible Discovery HUN modulja mutat — helyesírás és igealak, szókincs és szórend nélkül), a `F94_SZOTOVEZES_BRIEF.md` v1.1 (`regies_jegy` oszlop, N-F94b), a felhasználó kérése (chat, 2026-10-13): a modernizálás briefje kerüljön a végrehajtási sorrendbe.*

- **Mit ad, ha kész:** a Károli 1908 modernizált szövegrétege: helyesírás (*setétség → sötétség*, *néki → neki*, *a kik → akik*) és igealak (*teremté → teremtette*, *felele → felelt*, *monda → mondta*, *lőn → lett*, létigei *vala → volt*, segédigei *vala* elhagyva); a szórend, a szókincs, az írásjel és a betoldás-jelölés változatlan. Szavankénti csere, a Strong-szám a szón marad, a kieső token jelölve. Generált réteg az 1908-as szöveg mellett, nem helyette; két lépcső (előbb helyesírás, utána igeragozás és *vala*), mindkettő a felhasználó által ellenőrzött mintán mérve, a lefedettséggel együtt (maradt-e régies igealak).
- **Következő lépés:** brief kell a #94 lezárása után (sorrend: #94 → #96, a #95-tel párhuzamosan). A brief dönti el, hogy a réteg `pardes.db`-be töltése (a #76 vers-lapjának kapcsolójához) a #96 része vagy külön csonk (a `sqlite_epit.py` miatt a #92 után). Nyitott: a Hunspell hu_HU licencdöntés (N-F94b) az alakképzés szűréséhez.
- **Nem használható adatként:** a Bible Discovery (SQL Uniform Kft., © 2026) KG/HUN szövege és Strong-rétege; csak a megfigyelt módszer leírása (DT128).

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
