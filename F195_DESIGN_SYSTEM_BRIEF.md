---
feladat: 195
cim: A „PaRDeS olvasó” design system frissítése az olvasó-szerver mai állapotára
kod: DESIGN_SYSTEM
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/design-system-8e5bb3
pr: 0
ad: a design system tokenjei, README-je és komponensei a mai olvasót írják le; a token-réteg gépi úton frissíthető
kovetkezo: "Te: a lexikonlap arculatának választása (N-F195a), a draft PR áttekintése és merge-e"
munka: folyamat
olvas: [eszkozok/olvaso_szerver/arculat_szinkron.py, eszkozok/olvaso_szerver/konfig/arculat.json, eszkozok/olvaso_szerver/statikus/olvaso.css, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/blokkok.py]
ir: [eszkozok/olvaso_szerver/arculat_szinkron.py, eszkozok/olvaso_szerver/teszt_tervezo.py, dontesek/uj/design-system-8e5bb3.md, nyitott/uj/design-system-8e5bb3.md, F195_DESIGN_SYSTEM_BRIEF.md]
fugg: []
---

# F195_DESIGN_SYSTEM_BRIEF.md — A design system frissítése

*FELADATOK #195 · Modell: claude-opus-5-5 · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó, 2026-11-11, szó szerint).** A design-leltár (2026-11-10) (e) javaslatára: „ezeket csináljuk”.

**Indok.** A design system („PaRDeS olvasó”, artifact) 2026-10-15 óta nem követte az olvasó átalakítását: a Károli-szöveg lett az alapnézet, 900 px alatt a részletek alsó lapon nyílnak, ≥ 900 px-en oldalblokkban; új a kánon-sáv, az Aa-menü, a kereső, a jelölő chip és a tanulmány-margójel. A nézetváltó és a Munkaasztal megszűnt. Az ütemezés végén a motívumok az olvasóba kerülnek, ehhez naprakész rendszer kell.

## Teendő

1. **Tokenek, gépi úton** (`arculat_szinkron.py`). A `g-*` műfajszíneket, az `arnyek` színt és a három fejléc-térközt a szkript már a mai `arculat.json`-ból viszi át; a design system `tokens.json`-ja a szkript bevezetése előtti állapotot mutatta. Új:
   - `shadow` család: az `olvaso.css` `--arnyek`-et keverő `box-shadow` értékei, témánként `rgba()`-val;
   - `--tokens-css`: a design system `tokens.css`-e a kiírt `tokens.json`-ból, a típus szerkezetében (a régi `--space-1…6` skála kivezetése);
   - `--bundle-css`: a `components/bundle.css` (a szerver nem-szín változói és a mai `olvaso.css`).
2. **README, kézzel** (az artifactban): Károli-alapnézet, alsó lap / oldalblokk, Aa, kereső, kánon-sáv, árnyék; a megszűnt nézetváltó és Munkaasztal kikerül.
3. **Komponensek** (az artifactban): a Fejlec, Fulek, KaroliSzoveg kártya javítása; új kártyák: ReszletekLap, NavigaciosLap, Kereso, KanonSav, Chip, TanulmanyJel, a kétrétegű szótári kártya (`.bdb-*`, F104); előnézet a szerver markupjából.
4. **A lexikonlap arculata: nem dől el.** Privát előnézet a HAMART-001 egy részletéből két változatban: (a) az olvasó tokenjeivel; (b) a mai kék/Alegreya arculat „Lexikon” második témaként. A választás a felhasználóé (N-F195a).

## Garanciák és döntési napló

- G1: a repóban csak az `ir` fájlok változnak; a `lexikon/`, a generátor, a `sablonok/`, az `adat/`, a `DONTESEK.md` és az olvasó-szerver stíluslapja, sablonjai és regisztere nem.
- G2: a szkript kimenete a repón kívülre kerül; a `tokens.json` értékei az `arculat.json`-nal egyeznek (teszt: `teszt_tervezo.TestSzinkron`).
- G3: az artifact frissítése előtt minden módosított fájl friss beolvasása; az index (`design-system.json`) az utolsó hívásban.
- D1: döntés `DT-F195` (`dontesek/uj/design-system-8e5bb3.md`); nyitott tétel `N-F195a` (`nyitott/uj/design-system-8e5bb3.md`).
- D2: a régi leírások (usage) közül a megszűnt nézetekre utalók („Olvasópult”, „Munkaasztal”, „nézetváltó”, „jobb oldali panel”) a futtatás előtt, a design system példányán javulnak; a szkript a meglévő leírást megtartja.
- Egy független ellenőrzés, legfeljebb egy javítókör. ⛔ A merge a felhasználóé.
