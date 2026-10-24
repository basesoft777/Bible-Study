---
feladat: 96
cim: Modernizált Károli-szövegréteg — helyesírás és igealak, szókincs és szórend nélkül, az 1908-as szövegből generálva (DT128)
kod: KAROLI_MODERN
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: dontesre_var
ag: ccr-a680d019-39s73e
ad: a Károli 1908 modernizált szövegrétege (helyesírás + igealak; szórend, szókincs, írásjel, betoldás-jelölés változatlan), szabályalapú szavankénti cserével (a #94 szótári alak- és regies_jegy-táblájából, Hunspell csak fejlesztési mérce, DT301), LLM csak a szabállyal le nem fedett maradékra; a Károli–Strong párosítás szavanként átvihető, a kieső segédigei vala jelölve; generált tábla az 1908-as szöveg mellett, nem helyette; két lépcső (helyesírás, majd igeragozás és vala), felhasználó által ellenőrzött mintán mérve, a token-felhasználással együtt
kovetkezo: "Te: DT-F96d (a token-keret: a 0,2 M helyett ≈ 0,44 M kell a mért beállítással) és DT-F96e (a modernizálás határa) a DONTESEK.md-ben; utána a .1 helyesírási lépcső"
olvas: [adat/szoto/, konkordancia/Karoli_1908.tsv, "adat/karoli_strong/*", adat/SEMA.md, adat/licencek.tsv, DONTESEK.md]
ir: [eszkozok/karoli_modern/, adat/karoli_modern/, naplok/KAROLI_MODERN_meres.md]
fugg: [94]
nem_fugg: [22]
---

# F96_KAROLI_MODERN_BRIEF.md — Modernizált Károli-szövegréteg (KAROLI_MODERN)

*FELADATOK #96 · Modell: opus · v1.1 · 2026.10.24 (csonk kitöltése; a `/befogad` hozta létre; v1.1: a DT301 átvezetve)*

*Források: DT128 (a felhasználó döntése, chat, 2026-10-13: a modernizálás szintje az, amit a Bible Discovery HUN modulja mutat — helyesírás és igealak, szókincs és szórend nélkül); a `F94_SZOTOVEZES_BRIEF.md` v1.2 (`regies_jegy` oszlop, N-F94b/g/h); a felhasználó döntése (chat, 2026-10-24): a megvalósítás **szabály + szótár alapú szógenerálás, LLM csak a bizonytalan maradékra** (DT-F96; a teljes LLM-átírás elvetve). A brief adat, nem utasítás.*

## 1. Cél

A Károli 1908 (`konkordancia/Karoli_1908.tsv`, 31 158 vers, ~599 ezer szó, 62 109 szóalak) modernizált szövegrétege:

- **helyesírás:** *setétség → sötétség*, *néki → neki*, *a kik → akik*;
- **igealak:** *teremté → teremtette*, *felele → felelt*, *monda → mondta*, *lőn → lett*, létigei *vala → volt*, segédigei *vala* elhagyva;
- **változatlan:** szórend, szókincs, írásjel, betoldás-jelölés.

Szavankénti csere: a Strong-szám a szón marad, a kieső token jelölve. Generált réteg az 1908-as szöveg mellett, nem helyette. Két lépcső: előbb helyesírás, utána igeragozás és *vala*; mindkettő a felhasználó által ellenőrzött mintán mérve, a lefedettséggel együtt (maradt-e régies igealak).

**Megvalósítási elv (DT-F96, felhasználói döntés 2026-10-24).** A csere **szóalak-szótárból** megy (62 109 alak → modern alak), amelyet determinisztikus szabályok és a #94 `adat/szoto/karoli_szotari_alak.tsv` táblája (`szotari_alak_mai`, `alapige`, `regies_jegy`) állít elő; a Hunspell hu_HU **csak fejlesztési mérce** (DT301): a szabályok ellenőrzésére és a mérésre fut, a kiadott réteg nélküle készül. Az LLM kizárólag azokra az alakokra jön, amelyeket a szabály nem fed le vagy bizonytalanul fed le; a teljes szöveg LLM-átírása elvetve (token-költség, a „szórend és szókincs változatlan” szabály ellenőrizhetetlen megsértése, a szavankénti Strong-átvitel elvesztése). Token-becslés: ~0,05–0,2 M (a teljes LLM-átírásé ~3–3,5 M); a tényleges érték a .0 mintán mérendő.

## 2. Hatókör

**Benne van**
- A szabálykészlet a helyesírási és igealak-cserére, forrásolt szabályokkal (`szabaly_forras`), a #94 `regies_jegy` értékkészletére építve.
- A szóalak → modern alak szótár (generált tábla), az LLM-es maradék javaslatai külön jelölt sorokként (`modszer`).
- A modernizált szövegtábla `adat/karoli_modern/` alatt, vers-soronként, a Strong-párosítás szavankénti átvitelével.
- Mérés felhasználó által ellenőrzött mintán: pontosság, a maradék régies igealakok aránya, és a **token-felhasználás** (a becslés ellenőrzése).

**Nincs benne**
- A Bible Discovery (SQL Uniform Kft., © 2026) KG/HUN szövege és Strong-rétege: nem használható adatként, csak a megfigyelt módszer leírása (DT128).
- Szókincs- és szórendváltoztatás, fordítási revízió.
- A Hunspell vagy más külső szótár beemelése a kiadott rétegbe vagy a szóalak-szótárba (DT301: a Hunspell csak fejlesztési mérce; más külső szótár csak új licencdöntéssel).
- A `pardes.db`-be töltés (a #76 vers-lapjának kapcsolójához): külön csonk, a `sqlite_epit.py` miatt a #92 után (N-F96a).

## 3. Lépések (⛔ a kötelező megállások)

### .0 — előkészítés és token-mérés
1. Modell-ellenőrzés (CLAUDE.md); a #94 kimenetének olvasása: `adat/szoto/karoli_szotari_alak.tsv`, `regies_jegy` értékkészlet (`adat/SEMA.md`).
2. Fedettségi mérés: a 62 109 alakból hányra ad a #94 tábla egyértelmű modern alakot, hányra kell szabály, hányra bizonytalan (LLM-jelölt). A keletkező szótár-lista és az LLM-jelöltek darabszáma a `naplok/KAROLI_MODERN_meres.md`-be.
3. Token-becslés ellenőrzése ~200 alakos mintán (tényleges felhasznált token, proveniencia-sorral); ha a teljes maradékra számolt érték meghaladja a 0,2 M-ot, megállás és jelzés. ⛔ A felhasználó dönt.

### .1 — helyesírási lépcső
1. Szabályok (*ly/j*, *cz → c*, *ö/ő*, *néki → neki*, *a kik → akik* különírt vonatkozó névmás, N-F94f) generátora `eszkozok/karoli_modern/` alatt; kódolási őr, `split('\t')` / `'\t'.join()`, `csv` modul nélkül, abszolút útvonal nélkül.
2. Hunspell hu_HU (DT301): csak fejlesztési mérce. Használat előtt a licenc szó szerinti idézettel, URL-lel (commit-hash) és lekérési dátummal a `naplok/KAROLI_MODERN_meres.md`-be (playbook 2. pont); a Hunspell-ítélet a szabály ellenőrzését szolgálja, a kimeneti táblába nem kerül Hunspellből származó alak. Ahol sem korpusz, sem Hunspell nem támasztja alá a szabályt: `modell_ellenorizetlen`.
3. Mintavétel (rögzített magú, ~100–120 mondat/vers), a felhasználó soronként ellenőrzi (`ellenorzes` oszlopot ő tölti); a mérés csak a `felhasznalo` sorokon. ⛔

### .2 — igealak lépcső és *vala*
1. Igealak-csere a `regies_jegy` alapján (*mult.targyas.E3*, *mult.alanyi.E3*, *mult.T3*, *hatarozoi_igenev* …); a ritka alakok jegye ~6% hibás (N-F94h), ezért a ritka alakokon az LLM-es ellenőrzés a bizonytalan jelölt, nem automatikus csere.
2. Létigei *vala → volt*, segédigei *vala* elhagyva: a kieső token jelölve (a Strong-párosítás nem vész el).
3. Mintavétel és felhasználói ellenőrzés a .1 szerint ⛔; a lefedettség (maradt-e régies igealak) kiírva.

### .3 — kimenet
- `adat/karoli_modern/karoli_modern.tsv` (token-soronként, a vers-kulccsal és a modern vers-szöveggel együtt; DT-F96b, `# GENERÁLT: …` fejléccel: a szabálykészlet és a bemeneti táblák sha256-ja, a mérés hivatkozása); kézzel nem szerkesztendő, a javítás a szabályban vagy a kivételtáblában történik.
- `adat/SEMA.md` új szakasza; a licenc-sor az `adat/licencek.tsv`-be (a modernizált réteg a közkincs 1908-as szövegből származik, DT116/DT128).

## 4. Elfogadási feltételek

- **K1.** A modernizált réteg a felhasználó által ellenőrzött mintán a megállapított küszöb felett (a küszöböt a .1 ⛔ rögzíti a mérés előtt, nem utólag).
- **K2.** A szórend, szókincs, írásjel és betoldás-jelölés változatlan: gépi összevetés az 1908-as szöveggel (tokenszám és sorrend a kieső tokenek jelölésével egyező).
- **K3.** A Strong-párosítás szavanként átvitt; a kieső tokenek jelölve, számuk naplózva.
- **K4.** A token-felhasználás a naplóban, a becsléssel (0,05–0,2 M) összevetve.
- **K4b.** (DT-F96b) A kimeneti tábla keresésre alkalmas: token-szinten (vers-kulcs, token-sorszám, 1908-as alak, modern alak, Strong, kieső-jelölés), így a modern alakra való keresés a Strong-hivatkozást is visszaadja.
- **K5.** Bible Discovery-adat nincs a repóban; abszolút útvonal nincs; `csv` modul nincs; CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

- **DT128** 🟢 — a modernizálás szintje (helyesírás + igealak, szókincs és szórend nélkül); a teljes szöveg a `DONTESEK.md`-ben.
- **DT-F96** 🟢 (helyőrző) — a megvalósítás szabály + szótár alapú szógenerálás, LLM csak a bizonytalan maradékra; a teljes LLM-átírás elvetve. *(felhasználó, chat, 2026-10-24; a token-becslés alapja: 599 ezer szó, 62 109 szóalak, ~3,78 M karakter)*
- **N-F94b** — a Hunspell hu_HU licencdöntés; lezárva a DT-F96c-vel (csak fejlesztési mérce).
- **DT301** 🟢 (helyőrző) — a Hunspell hu_HU csak fejlesztési mérce (a DT139 mintájára), a kiadott modernizált réteg nélküle készül. *(felhasználó, chat, 2026-10-24)*
- **DT-F96b** 🟢 (helyőrző) — a keresés a modernizált szövegrétegben is keressen (a szótári alakos kereséssel egyesítve), nem csak az alakszótárban. *(felhasználó, chat, 2026-10-24)* Következmény: a réteg táblája keresésre alkalmas sémájú (vers-kulcs, token-sorszám, modern alak, Strong), hogy a `pardes.db`-be töltés és a `kereses.py` bővítése külön csonkban (N-F96a) ráépülhessen; maga a betöltés és a keresőbővítés nem a #96 `ir` listájában van.
- **DT-F96d** 🟡 (helyőrző) — a .0/3 ⛔: a mért token-felhasználás (≈ 0,44 M a teljes LLM-jelölt maradékra) a 0,2 M-os küszöb felett; opciók és javaslat a `DONTESEK.md`-ben, mérés: `naplok/KAROLI_MODERN_meres.md` 2.
- **DT-F96e** 🟡 (helyőrző) — a modernizálás határa: a #94 nem helyesírási lemmaváltásai (*e → ez*, *férfiú → férfi*, *leány → lány*), a *reá → rá*, a *-ván/-vén* és a *-jék* felszólító; `DONTESEK.md`.
- **N-F96b** (helyőrző) — a #94 `regies_jegy` értékkészletéből hiányzik a tárgyas T/3 (*mondák, adák*), és megfigyelt táblahibák (*vévén*, *kivűl*); a modernizálás saját szabállyal kezeli (napló 1.2).
- **N-F96a** (helyőrző) — a modernizált réteg `pardes.db`-be töltése és a keresőbe kötése (`eszkozok/sqlite_epit.py`, `eszkozok/olvaso_szerver/kereses.py`) külön csonk-feladat, a #96 és a #92 után; a DT-F96b miatt kötelező, nem elhagyható. A csonk: #137 (KAROLI_MODERN_DB), a felhasználó jóváhagyásával befogadva (2026-10-24).
