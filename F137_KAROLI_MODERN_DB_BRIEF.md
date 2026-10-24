---
feladat: 137
cim: Modernizált Károli a keresőben és a pardes.db-ben — a #96 rétegének betöltése és a keresés bővítése
kod: KAROLI_MODERN_DB
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: brief_kell
ad: a #96 modernizált Károli-rétege a pardes.db-ben (token-szintű tábla, hash meta-sorral), és az olvasói kereső a modern szövegben is keres, a szótári alakos kereséssel egyesítve; a vers-lap kapcsolója a modern és az 1908-as szöveg között (DT-F96b)
kovetkezo: "brief kell a #96 lezárása után (a #92 és a #76 lezárva); a brief dönti el, hogy a vers-lap kapcsolója ennek része vagy külön csonk"
olvas: [adat/karoli_modern/, adat/SEMA.md, eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/kereses.py, F96_KAROLI_MODERN_BRIEF.md, F95_SZOTOVEZES_DB_BRIEF.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/kereses.py, adat/SEMA.md, naplok/KAROLI_MODERN_DB_meres.md]
fugg: [96]
---

# F137_KAROLI_MODERN_DB_BRIEF — csonk

*FELADATOK #137 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza; v1; 2026.10.24; a #96 N-F96a tétele szerint, a DT-F96b (a felhasználó döntése, chat, 2026-10-24: a keresés a modernizált szövegrétegben is keressen) alapján.*

- **Mit ad, ha kész:** a #96 `adat/karoli_modern/` tábláját a `pardes.db`-be tölti (`szotari_alak` mintájára: hash meta-sor, frissességi teszt), a `kereses.py` pedig a modern alakban is keres, egyesítve a pontos alakkal és a szótári alakos (`szotari_kereso`) találatokkal; a találat a Strong-hivatkozást is visszaadja.
- **Kötelező (DT-F96o):** a modern táblában a kieső token (összevont „a”, segédigei *vala*) Strongja a `kieso_gazda` szerinti gazdaszóhoz kötődik a keresésben (*amelyen* = H0834 + a névmás Strongja; *lebegett* = az ige + H1961); a Strong a #22 párosításból jön, a modern réteg nem tárolja (DT-F96f). Érintett: 294 token (#96 napló 5.2).
- **Következő lépés:** brief kell a #96 lezárása után. Nyitott: a vers-lap modern/1908 kapcsolója (#76) része-e, és a keresési teljesítmény mérése (a #95 mintájára).

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
