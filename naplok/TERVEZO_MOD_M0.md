# TERVEZO_MOD — M0 terv (#98)

*Csak olvas: az M0 egyetlen szerver-fájlt sem módosít. A „javaslat” jelölésű tételek javaslatok; a döntés a felhasználóé (DT-F98a–e, `DONTESEK.md`). Modell: `claude-opus-5-5`. Állapot: **⛔ jóváhagyásra vár** (a regiszter magyar nevei és a tulajdonságok köre, valamint a DT-F98a–e).*

Mért adatok forrása, ahol nincs más jelölés: `scope=eszkozok/olvaso_szerver/ (statikus/olvaso.css 16 359 B, sablonok/*.html, blokkok.py, oldalak.py), ág claude/tervezo-mod, alap origin/main@147ada81 | forras=három felmérő szkript a session scratch-könyvtárában (osztalyok.py: class-attribútumok a sablonokból és a két Python-modulból; meretek.py: méret-értékek tulajdonság-csoportonként; holt.py: felülírt deklarációk, szelektoronként) | ts=2026-10-14`. A design system tokenjei: `scope=https://claude.ai/artifact/AtQvPhFShiG71apnGPm2AU, project/tokens.json (17 996 B, sha256 899439f5…), verzió 1791995892-d37b | forras=Artifact read | ts=2026-10-14`. A szerver nem futott; a „valódi lapon talál elemet” ellenőrzés az M2 tesztje.

## 0. Összefoglaló

- **Elem-regiszter** (1. szakasz): 73 regiszter-sor 12 csoportban (61 önálló elem és 12 állapot- vagy változat-sor), magyar névvel és tulajdonság → token hozzárendeléssel; mellette a kizárt (szerkezeti, állapot- és horog-) osztályok listája, csoportonként indokolva. A mai felületen használt 109 osztályból (és 9 dinamikusan képzett osztályból) mindegyik vagy a regiszterben, vagy a kizárt listán áll.
- **Token-fájl** (2. szakasz, javaslat): `eszkozok/olvaso_szerver/konfig/arculat.json`, tisztán értékek (szabad szöveg nélkül), a design system `tokens.json`-jával egyező szín- és stílusnevekkel. A szerver token-blokkja (a mai `:root` és a két sötét téma-blokk) ebből generálódik, **dinamikus útvonalon** (`/arculat.css?v=<hash>`), nem generált fájlként (DT-F98e).
- **Méret-tokenek** (3. szakasz): 52 betűméret-, 18 sorköz-, 35 térköz- és 6 lekerekítés-token, a mai `olvaso.css` **ténylegesen érvényes** értékeiből. 46 felülírt („holt”) deklaráció van a stíluslapban; javaslat: az M1 ezeket törli (DT-F98d).
- **Panel** (4. szakasz): kattintásra a legbelső regisztrált elem, „szülő elem” lépéssel; csúszka vagy palettaminta; előnézet a `:root` CSS-változóival (CSSOM, CSP-kompatibilis); változáslista egyenkénti visszavonással; „Küldés a szerverre” külön gombbal.
- **Öt döntés** kell (DT-F98a–e): a betűméret-tokenek szemcsézettsége, a térköz-tokenek köre, a sorköz állíthatósága, a holt deklarációk sorsa, és a token-blokk előállítási módja.
- Két megfigyelés a mai stíluslapról (5. szakasz): a `.igehely` szelektor a táblázatbeli igehely-hivatkozásokra is ráhat; a design system `oldalcim` stílusa 300-as vastagságot ír, a szerver 600-at ad.

## 1. Az elem-regiszter tervezete (4. lépés a)

**Forma (javaslat):** `eszkozok/olvaso_szerver/konfig/elemek.toml`. Konfiguráció, nem kód; a szerver induláskor betölti és ellenőrzi (ismeretlen token → indulási hiba, a `hozzaferes.toml` mintájára).

```toml
[[elem]]
id = "he-szo"
nev = "Héber szócsempe"
csoport = "Vers részletei"
szelektor = ".he-szo"
tulajdonsag = [
  { nev = "Háttér",              token = "bg" },
  { nev = "Keret színe",         token = "rule" },
  { nev = "Lekerekítés",         token = "radius-csempe" },
  { nev = "Belső térköz (függőleges)", token = "space-he-csempe-fugg" },
  { nev = "Belső térköz (vízszintes)", token = "space-he-csempe-vizsz" },
  { nev = "Legkisebb szélesség", token = "space-he-csempe-min" },
]

[kizart]
oszlopok = "rács-elrendezés (a három nézet oszlopai); nincs állítható arculati értéke"
```

A **tulajdonság típusa** a tokenből jön (szín → palettaminta; hossz → csúszka a token tartományával; sorköz → csúszka, ha a DT-F98c engedi). Egy elem több tokent is mutathat; egy token több elemnél is szerepelhet (a panel ilyenkor kiírja, hány szabályban és hány elemen hat).

**Választás a felületen:** kattintáskor a kattintott elemtől felfelé az első, regiszterbeli szelektorra illeszkedő elem lesz a kiválasztott (a legbelső). A panelen „Szülő elem ↑” lép egy szinttel feljebb a következő regisztrált elemre. Állapot-osztályok (`aktiv`, `kijelolt`) külön elemként szerepelnek, ha saját színük van (pl. „Nézetváltó gomb (aktív)”).

### 1.1 A regiszter elemei

Jelmagyarázat: a token-nevek a 2–3. szakasz szerint; *szín* = a 10 színtoken egyike (`bg`, `panel`, `fg`, `muted`, `rule`, `accent`, `accent-soft`, `gold`, `gold-soft`, `low`), világos és sötét értékkel.

**A. Fejléc**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok (magyar név → token) |
|---|---|---|---|---|
| 1 | fejlec | Fejléc sávja | `.fejlec` | Alsó vonal színe → `rule` · Függőleges belső térköz → `space-fejlec-fugg` · Oldalmargó → `space-oldal` · Sorok közti köz → `space-fejlec-sor` · Elemek közti köz → `space-fejlec-oszlop` |
| 2 | logo | Logó („PaRDeS olvasó”) | `.logo` | Betűméret → `fs-logo` · Szín → `fg` |
| 3 | nezetvalto | Nézetváltó gomb | `.nezetvalto a` | Szövegszín → `accent` · Keret színe → `rule` · Lekerekítés → `radius-csempe` · Belső térköz → `space-gomb-fugg`, `space-gomb-vizsz` · Gombok közti köz → `space-gombsor` |
| 4 | nezetvalto-aktiv | Nézetváltó gomb (aktív) | `.nezetvalto a.aktiv` | Háttér → `accent` · Szöveg → `bg` |
| 5 | szintvalto | Szintváltó gomb | `.szintvalto a` | Betűméret → `fs-gomb` · Keret színe → `rule` · Lekerekítés → `radius-csempe` |
| 6 | szintvalto-aktiv | Szintváltó gomb (aktív) | `.szintvalto a.aktiv` | Háttér → `fg` · Szöveg → `bg` |
| 7 | szint-cim | Szintváltó felirat („Szint”) | `.szint-cim` | Betűméret → `fs-gomb-kis` · Szín → `muted` |
| 8 | tema | Témaváltó gomb | `.tema button` | Betűméret → `fs-gomb-kis` · Háttér → `panel` · Szöveg → `fg` · Keret → `rule` · Lekerekítés → `radius-csempe` |
| 9 | tema-aktiv | Témaváltó gomb (aktív) | `.tema button[aria-pressed="true"]` | Háttér → `accent` · Szöveg → `bg` |

**B. Oldal és keret**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 10 | oldal | Oldal alapja | `body` | Háttér → `bg` · Szövegszín → `fg` · Alap betűméret → `fs-torzs` · Alap sorköz → `lh-torzs` |
| 11 | tartalom | Tartalom-terület | `.tartalom` | Felső belső térköz → `space-tartalom-fent` · Oldalmargó → `space-oldal` · Alsó belső térköz → `space-tartalom-lent` |
| 12 | labjegyzet | Lábjegyzet (kiadás, építés ideje) | `.labjegyzet` | Betűméret → `fs-megjegyzes` · Szín → `muted` · Felső vonal → `rule` · Függőleges belső térköz → `space-labjegyzet-fugg` |
| 13 | lapcim | Lapcím | `h1` | Betűméret → `fs-oldalcim` · Sorköz → `lh-oldalcim` · Szín → `fg` |
| 14 | szakaszcim | Szakaszcím (kezdőlap: Ószövetség/Újszövetség) | `h2:not(.szocim):not(.igehely)` | Betűméret → `fs-szakaszcim` |
| 15 | hivatkozas | Hivatkozás (általános) | `a` | Szín → `accent` |
| 16 | valaszto | Könyv–fejezet–vers választó felirata | `.valaszto label` | Betűméret → `fs-megjegyzes` · Szín → `muted` · Mezők közti köz → `space-valaszto-sor`, `space-valaszto-oszlop` |
| 17 | megjegyzes | Megjegyzés, szám, címke (szürke apró szöveg) | `.megj, .szam, .cimke:not(.cimkek .cimke)` | Betűméret → `fs-megjegyzes` · Szín → `muted` |
| 18 | ures | Üres eredmény jelzése | `.ures` | Szín → `muted` |

**C. Fejezet-lap fölső része**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 19 | szamlalo | Számláló címke | `.cimkek .cimke` | Betűméret → `fs-szamlalo` · Háttér → `accent-soft` · Szöveg → `accent` · Lekerekítés → `radius-pill` · Belső térköz → `space-szamlalo-fugg`, `space-szamlalo-vizsz` · Címkék közti köz → `space-cimkesor` |
| 20 | szamlalo-arany | Számláló címke: hiányos fordítás (arany) | `.cimkek .cimke.arany` | Háttér → `gold-soft` · Szöveg és keret → `gold` |
| 21 | utmutato | Útmutató doboz („Hogyan olvasd…”) | `.utmutato` | Háttér → `panel` · Keret → `rule` · Lekerekítés → `radius-panel` · Betűméret → `fs-utmutato` · Belső térköz → `space-utmutato-fugg`, `space-utmutato-vizsz` |
| 22 | szoveg-jegy | Szövegoszlop jegyzete (jelleg és forrás a szöveg fölött) | `.szoveg-jegy` | Betűméret → `fs-szoveg-jegy` · Sorköz → `lh-szoveg-jegy` · Szín → `muted` · Keret → `rule` · Lekerekítés → `radius-csempe` |
| 23 | kapcs | Kapcsoló („Kapcsolt szavak jelölése”) | `.kapcs` | Betűméret → `fs-megjegyzes` · Szín → `muted` |

**D. Folyó szöveg (Olvasópult, Munkaasztal)**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 24 | karoli-folyo | Folyó Károli-szöveg | `.szoveg-oszlop` | Betűméret → `fs-karoli-folyo` · Sorköz → `lh-karoli-folyo` · Betűméret mobilon → `fs-karoli-folyo-mobil` · Sorköz mobilon → `lh-karoli-folyo-mobil` · Szín → `fg` |
| 25 | versszam | Versszám | `.versszam` | Betűméret (a szöveghez viszonyítva) → `fs-versszam` · Szín → `accent` |
| 26 | kotott-szo | Kötött szó (pontozott aláhúzás) | `.szo` | Aláhúzás színe → `muted` · Rámutatáskor háttér → `accent-soft` · Rámutatáskor aláhúzás → `accent` · Lekerekítés → `radius-szo` |
| 27 | kotott-szo-alacsony | Kötött szó: nem „magas” bizonyosság | `.szo.par-alacsony` | Aláhúzás színe → `low` |
| 28 | kijelolt-vers | Kijelölt vers | `.vers.kijelolt, .il-vers.kijelolt` | Háttér → `accent-soft` · Lekerekítés → `radius-kiemeles` |
| 29 | verslista | Verslista (Munkaasztal) | `.verslista` | Betűméret → `fs-megjegyzes` · Elválasztó → `rule` · Aktív sor háttere → `accent-soft` |

**E. Jobb oldali panel**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 30 | jobb-panel | Jobb oldali panel | `.jobb-oszlop` | Háttér → `panel` · Keret → `rule` · Lekerekítés → `radius-panel` · Betűméret → `fs-panel` · Függőleges belső térköz → `space-panel-fugg` |
| 31 | ful | Fül („Szó” / „Vers részletei”) | `.ful` | Keret → `rule` · Lekerekítés → `radius-csempe` |
| 32 | ful-aktiv | Fül (aktív) | `.ful.aktiv` | Háttér → `accent` · Szöveg → `bg` |
| 33 | vers-panel-cim | Vers-panel címe (igehely) | `h2.igehely` | Betűméret → `fs-igehely` |
| 34 | karoli-panel | A vers Károli-szövege a panelen | `.karoli-szoveg` | Betűméret → `fs-karoli-panel` · Sorköz → `lh-karoli-panel` |

**F. Blokk (minden blokk közös keretei)**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 35 | blokk | Blokk | `.blokk` | Elválasztó vonal → `rule` · Két blokk közti köz → `space-blokkkoz` |
| 36 | blokkcim | Blokkcím | `.blokk h3` | Betűméret → `fs-blokkcim` · Sorköz → `lh-blokkcim` |
| 37 | jelleg | Jelleg-címke (közös forma) | `.jelleg` | Betűméret → `fs-jelleg` · Lekerekítés → `radius-pill` · Belső térköz → `space-jelleg-fugg`, `space-jelleg-vizsz` |
| 38 | jelleg-forras | Jelleg-címke: forrásadat | `.jelleg-forras` | Szöveg és keret → `accent` |
| 39 | jelleg-gepi | Jelleg-címke: gépi feldolgozás | `.jelleg-gepi` | Szöveg → `muted` · Keret → `rule` |
| 40 | jelleg-modell | Jelleg-címke: modell-kimenet | `.jelleg-modell` | Szöveg és keret → `gold` · Háttér → `gold-soft` |
| 41 | forrassor | Forrássor (forrás és licenc a blokk alatt) | `.forras, .forrasnev` | Betűméret → `fs-forrassor` · Sorköz → `lh-forrassor` · Szín → `muted` |
| 42 | adattabla | Adattábla (Nave, TSK, TIPNR …) | `table.adat` | Betűméret → `fs-adat-tabla` · Sorvonal → `rule` · Fejléc színe → `muted` |
| 43 | igehely-link | Igehely-hivatkozás a blokkokban | `a.igehely` | Betűméret → `fs-igehely` *(ma ugyanaz a token, l. 5. szakasz 1.)* |

**G. Vers részletei: héber szócsempék**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 44 | heber-sor | Héber szósor | `.heber-sor` | Csempék közti köz → `space-he-sor` |
| 45 | he-szo | Héber szócsempe | `.he-szo` | Háttér → `bg` · Keret → `rule` · Lekerekítés → `radius-csempe` · Belső térköz → `space-he-csempe-fugg`, `space-he-csempe-vizsz` · Legkisebb szélesség → `space-he-csempe-min` |
| 46 | he-szo-heber | Héber szócsempe: héber szó | `.he-szo .he` | Betűméret → `fs-csempe-heber` · Sorköz → `lh-csempe` |
| 47 | he-szo-glossza | Héber szócsempe: átírás és glossza | `.he-szo .at, .he-szo .gl` | Betűméret → `fs-csempe-glossza` · Átírás színe → `muted` |
| 48 | strong-szam | Strong-szám (csempéken és az LXX-soron) | `.he-szo .st, .ang-csempe .st, .ang-csempe .st-link, .lxx-sor small` | Betűméret → `fs-strong-szam` · Szín → `muted` |
| 49 | he-szo-lxx | Héber szócsempe: görög (LXX) megfelelő | `.he-szo .lx` | Betűméret → `fs-csempe-lxx` · Szín → `accent` · Elválasztó → `rule` |

**H. LXX-sor és angol csempék**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 50 | lxx-sor | LXX-sor (Septuaginta) | `.lxx-sor` | Betűméret → `fs-lxx-sor` · Sorköz → `lh-lxx-sor` · Csempék közti köz → `space-lxx-sor-fugg`, `space-lxx-sor-vizsz` |
| 51 | lxx-csempe | LXX-csempe (kattintható görög szó) | `.lxx-sor .gk` | Háttér → `bg` · Keret → `rule` · Szöveg → `accent` · Lekerekítés → `radius-kis-csempe` · Belső térköz → `space-kis-csempe-fugg`, `space-lxx-csempe-vizsz` |
| 52 | ang-csempe | Angol szócsempe | `.ang-csempe` | Háttér → `bg` · Keret → `rule` · Lekerekítés → `radius-kis-csempe` · Betűméret → `fs-angol-szo` · Belső térköz → `space-kis-csempe-fugg`, `space-ang-csempe-vizsz` |

**I. Interlineáris**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 53 | il-csempe | Interlineáris csempe | `.il-szo` | Háttér → `bg` · Keret → `rule` · Lekerekítés → `radius-csempe` · Betűméret → `fs-il-csempe` · Belső térköz → `space-il-csempe-fugg`, `space-il-csempe-vizsz` · Csempék közti köz → `space-il-sor-fugg`, `space-il-sor-vizsz` |
| 54 | il-magyar | Interlineáris: magyar szó | `.il-szo .hu` | Betűméret → `fs-il-magyar` · Sorköz → `lh-il-magyar` |
| 55 | il-eredeti | Interlineáris: eredeti szó (héber / görög) | `.il-szo .heb, .il-szo .gor` | Héber betűméret → `fs-il-heber` · Görög betűméret → `fs-il-gorog` · Sorköz → `lh-csempe` |
| 56 | il-apro | Interlineáris: átírás, glossza, Strong-szám | `.il-szo .at, .il-szo .gl, .il-szo .st` | Átírás → `fs-il-atiras` · Glossza → `fs-il-glossza` · Strong-szám → `fs-il-strong` · Szín → `muted` |

**J. Szó-lap fejléce**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 57 | szocim | Szó-lap címszava | `.szocim` | Héber betűméret → `fs-szocim-heber` · Görög betűméret → `fs-szocim-gorog` · Sorköz → `lh-szocim-heber`, `lh-szocim-gorog` |
| 58 | szoalcim | Szó-lap alcíme (átírás, jelentés) | `.szoalcim` | Betűméret → `fs-szoalcim` · Szín → `muted` |
| 59 | alapjel | Alapjelentés (szó-lap fejléc) | `.alapjel` | Betűméret → `fs-alapjelentes` · Sorköz → `lh-alapjelentes` |
| 60 | fcim | Kis nagybetűs felirat („Alapjelentés”, „Forrás”) | `.fcim` | Betűméret → `fs-forrascim` · Szín → `accent` |

**K. BDB-apparátus**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 61 | app-cim | Apparátus szakaszcím (nagybetűs) | `.app h4` | Betűméret → `fs-apparatus-cim` · Szín → `accent` |
| 62 | app-alcim | Apparátus törzscím (Qal, Nif'ál …) | `.torzs h5, .app h5` | Betűméret → `fs-apparatus-alcim` · Sorköz → `lh-apparatus-alcim` |
| 63 | szocikk | Szócikk-szöveg | `.jsz, .szoveg` | Betűméret → `fs-szocikk` · Sorköz → `lh-szocikk` |
| 64 | helyek | Helyszám-címke | `.helyek` | Betűméret → `fs-helyszam` · Háttér → `bg` · Keret → `rule` · Lekerekítés → `radius-pill` |
| 65 | cimszo-heber | Apparátus címszó (héber) | `.cimszo .he` | Betűméret → `fs-cimszo-heber` |
| 66 | allapot | Fordítás-állapot („Lefordítva …”) | `.allapot` | Betűméret → `fs-allapot` · Háttér → `gold-soft` · Szöveg → `gold` · Lekerekítés → `radius-pill` |
| 67 | allapot-folyamat | Fordítás-állapot: nincs fordítás | `.allapot.folyamat` | Háttér → `panel` · Keret → `rule` · Szöveg → `muted` |
| 68 | jel-cimke | Irodalmi és szövegkritikai jel | `.jel-cimke` | Betűméret → `fs-jel-cimke` · Keret → `rule` · Lekerekítés → `radius-kiemeles` |
| 69 | jel-cimke-krit | Szövegkritikai jel (arany) | `.jel-cimke.krit` | Szöveg és keret → `gold` |

**L. Egyéb blokk-elemek**

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 70 | ubs | UBS-jelentés sora | `.ubs` | Betűméret → `fs-ubs` · Bal oldali vonal → `accent` · Domén színe → `accent` |
| 71 | parsor | Párlista sora (héber–görög párok) | `.sor` | Betűméret → `fs-sor` |
| 72 | heber-kozi | Szövegközi héber szó | `.heb` | Betűméret (a környezethez viszonyítva) → `fs-heb-betu` |
| 73 | nincs-st | LXX-szó Strong-szám nélkül | `.lxx-sor .nincs-st small` | Szín → `gold` |

*Számolás:* 73 sor; ebből 61 önálló elem és 12 állapot- vagy változat-sor (4, 6, 9, 20, 27, 28, 32, 38–40, 67, 69).

**M. BDB-jelentésszerkezet** *(bővítés az M1 után, F98.14; **tervezet, a magyar nevek jóváhagyásra várnak**)*

Forrás: az F98.9–F98.13 (`67d35334`…`33619789`) szabályai az `olvaso.css` 139–170. sorában és a `blokkok.py` `_vazlat_html` / `_torzsek_html` / `_fo_cim_html` / `_jelmagyarazat_html` / `_jeles` függvényei. Az `ol.jel` / `ol.al` szabályai az F98.9 óta a #60 pilot `sablon.html`-jének szabályai (a jelölő a `data-jel` attribútumból, `::before`-ral). A token-nevek a 3. szakasz jelölésével: `fs-jelentes-jel` = `betumeret.jelentes-jel` (13px), `fs-jelentes-cim` = `betumeret.jelentes-cim` (15.5px), `lh-jelentes-cim` = `sorkoz.jelentes-cim` (1.5); a `jelentes-cim` az F98.9-ben még `jelentes-osszegzo` volt, az F98.11 nevezte át. Csak a tokenből jövő tulajdonság szerepel; a literálok (`font-weight`, `min-width`, `padding-left`, `gap`, `margin`, `text-underline-offset`) nem állíthatók (DT-F98b).

| # | id | Magyar név | Szelektor | Állítható tulajdonságok |
|---|---|---|---|---|
| 74 | jel-vazlat | Jelentésszerkezet vázlata (a BDB-blokk elején) | `.jel-vazlat` | Háttér → `panel` · Keret → `rule` · Lekerekítés → `radius-panel` · Betűméret → `fs-sor` · Sorköz → `lh-forrassor` · Belső térköz → `space-utmutato-fugg`, `space-utmutato-vizsz` · Hivatkozás színe rámutatáskor → `accent` *(a `.jel-vazlat a:hover`: a főjelentés- és az alpont-sorokon)* |
| 75 | vz-torzs | Vázlat: törzscím (Qal, Nif'ál …) | `.jel-vazlat .vz-torzs` | Betűméret → `fs-apparatus-alcim` |
| 76 | vz-fo | Vázlat: főjelentés sora | `.jel-vazlat .vz-fo` | Szín rámutatáskor → `accent` *(a 74. sor hivatkozás-szabálya; saját tokenje nincs, a vastagság literál)* |
| 77 | vz-jel | Vázlat: jelentés-jelölő (1, 2 …) | `.jel-vazlat .vz-jel` | Betűméret → `fs-jelentes-jel` · Szín → `accent` |
| 78 | vz-al | Vázlat: alpontok sora (a., b. …) | `.jel-vazlat .vz-al` | Szín → `muted` |
| 79 | jcim | Jelentéscím (a részletes listában) | `.jcim` | Betűméret → `fs-jelentes-cim` · Sorköz → `lh-jelentes-cim` · Háttér, ha a jelentésre ugrottak → `accent-soft` · Lekerekítés, ha a jelentésre ugrottak → `radius-kiemeles` *(`ol.jel > li:target … .jcim`)* |
| 80 | kolcsonzott | Kölcsönzött jelentéscím (az első alpontból) | `.kolcsonzott` | Szín → `muted` |
| 81 | jelmagyarazat | BDB-jelmagyarázat (a blokk végén) | `.jelmagyarazat` | Betűméret → `fs-sor` · Sorköz → `lh-forrassor` · Jel betűmérete → `fs-jelentes-jel` · Jel színe → `accent` *(`.jelmagyarazat dt`)* |
| 82 | bdb-rovidites | BDB-rövidítés a szócikk-szövegben | `.jsz abbr[title]` | Aláhúzás színe → `muted` |
| 83 | jelentes-jelolo | Jelentés-jelölő a részletes listában (1, 2 … / a., b. …) | `ol.jel > li, ol.al > li` | Jelölő betűmérete → `fs-jelentes-jel` · Jelölő színe → `accent` *(`::before`)* · Alpontlista bal vonala → `accent-soft` *(`ol.al`)* · „összecsuk” felirat → `fs-megjegyzes`, `muted` *(`summary::after`)* *(a feladat felsorolásán túli, javasolt sor: e nélkül a jelölő tokenjei csak a vázlaton és a jelmagyarázaton át érhetők el)* |

*Nem kap saját sort:* a `.jcim .he`, `.jel-vazlat .he` (a jelentéscím héber futama): a szabálya `font-family: var(--font-he)`, `font-weight: 400` és `unicode-bidi: isolate`; a betűcsalád a mentési végponton nem írható (2.2), a betűmérete a szülőé (79: `fs-jelentes-cim`, 74: `fs-sor`), tehát állítható tulajdonsága nincs. Az 1.2 kizárt listájába kerül (szövegrész-horog). A `.helyek` (64) az F98.12 óta nem törik (`white-space: nowrap`); állítható tulajdonsága nem változott.

*Számolás a bővítés után:* 83 sor; ebből 71 önálló elem és 12 állapot- vagy változat-sor (a 74–83. sorok mind önállók).

### 1.2 Kizárt osztályok (szerkezeti, állapot- vagy horog-osztályok)

| Osztály | Indok |
|---|---|
| `oszlopok`, `olvaso`, `interlinearis`, `munkaasztal` | a nézetek rács-elrendezése; elrendezés-szerkesztés nincs a hatókörben |
| `panel`, `ful-tartalom` | JavaScript-horog (fülváltás, töredék-betöltés); nincs saját megjelenése |
| `fulek` | a fülek sora (flex-tároló, csak alsó margó) |
| `szolap`, `verslap`, `torzs`, `app` | tartalmi burkoló (`article`/`div`); a megjelenés a gyermek-elemeken |
| `fejezetfej`, `lapozo`, `ketto` | sablon-horog, CSS-szabály nincs rá |
| `il-vers`, `il-szavak`, `il-parositatlan`, `folyo`, `vers` | sor- és bekezdés-tároló; a térköz a csempén (53) vagy a folyó szövegen (24) állítható |
| `sorok`, `gordul`, `lista`, `al`, `jel`, `jelek`, `cimkek`, `konyvek`, `konyv`, `fejezetek`, `fejezet-nave`, `angol-sor` | lista-, görgető- és oszlop-tároló (behúzás, görgetés, hasábok); az elemek a gyermekeken |
| `he-fo`, `er-fo`, `er`, `ures-par` | hivatkozás- vagy sor-burkoló a csempén belül; a rámutatás-háttér `accent-soft` a csempe (45, 53) tokenjét használja |
| `cimszo`, `fo`, `def`, `dom`, `karoli-itt`, `alak`, `strong`, `gr`, `gk`, `he`, `at`, `gl`, `st`, `st-link`, `lx`, `mf`, `kat`, `ang`, `hu`, `heb`, `gor` *(önmagukban)* | szövegrész-horog egy regisztrált elemen belül; a betűméretük a szülő-elem tokenje (pl. `ang` → 52) |
| `aktiv`, `kijelolt`, `nyelvtani`, `nincs-jeloles`, `par-magas`, `arany`, `krit`, `folyamat` *(önmagában)* | állapot-osztály; ahol saját színe van, változat-sorként a regiszterben áll (4, 6, 20, 28, 32, 67, 69) |
| `nezet-olvaso`, `nezet-interlinearis`, `nezet-munkaasztal` | a `body` nézet-horga; CSS-szabály nincs rá |
| `ugras` | a gyorsugrás űrlap: böngésző-alapértelmezett mező, token nélkül |
| `he` a `.jcim`-ben és a `.jel-vazlat`-ban *(F98.12)* | szövegrész-horog: csak betűcsalád (a mentésen nem írható) és bidi-izolálás; a mérete a 79., illetve a 74. sor tokenje |

*Az F98.11 óta a `jt` (a jelentés rövid összegzése) nem keletkezik: a helyét a `jcim` (79) vette át, ezért a `jt` a fenti listából kikerült (M2, a felhasználó kérése, 2026-10-15).*

A végleges kizárt lista az M2 regiszter-őrének kimenetéből készült: `eszkozok/olvaso_szerver/konfig/elemek.toml` `[kizart]` (46 osztály, egyenként indokolva). Ott csak az az osztály áll, amely a felületen előfordul, és egyetlen regiszter-szelektorban sem szerepel; az itteni felsorolás állapot- és szövegrész-osztályai közül a szelektorokban szereplők (pl. `aktiv`, `kijelolt`, `he`, `gk`, `st`) regisztráltnak számítanak. Az itteni felsorolás a felmérő szkript 109 osztályát fedi (`osztalyok.py`); az M2 őre két további osztályt talált: `szo-nincs` (a felmérésből kimaradt) és `tervezo-kapcsolo` (az M2 saját vezérlője).

### 1.3 A regiszter-őr (M2) bemenete: a dinamikusan képzett osztályok

A felmérés szerint 9 osztály nem szó szerint, hanem kifejezésből áll elő; a regiszter-őrnek ezeket ki kell tudnia bontani:

| Hely | Kifejezés | Értékkészlet |
|---|---|---|
| `alap.html` | `nezet-{{ nezet }}` | `oldalak.NEZETEK` |
| `fejezet.html` | `' par-' ~ w.biz` | a `token_par` bizonyosság-mezőjének értékei (`magas`, `alacsony`, …): az őr a `lekerdezesek`-ből veszi, nem a kódból |
| `fejezet.html` | `' arany' if …`, `' aktiv' if …`, `' kijelolt' …`, `' nyelvtani' if …` | literál a feltételben |
| `blokkok.py` | `jelleg %s` (`JELLEG[j][1]`) | `jelleg-forras`, `jelleg-gepi`, `jelleg-modell` (a `JELLEG` szótárból) |
| `blokkok.py` | `he-szo%s`, `allapot%s`, `adat %s` | `nyelvtani`, `folyamat`, a `_tabla(osztaly=…)` hívások literáljai |
| `blokkok.py` | `ctx_strong_link(…, 'st-link')` | paraméter-literál |

**Javaslat az őr módszerére:** a sablonokat a Jinja2 lexerével (`env.lex`), a Python-modulokat az `ast` modullal olvassa (a `class="…"` szöveg-literálok és a `%`/`~` operandusai), a fenti értékkészleteket explicit listából veszi. Az ismeretlen osztály hibája: `ismeretlen CSS-osztály: <osztály> (<fájl>:<sor>) — vedd fel az elemek.toml [[elem]] vagy [kizart] részébe`.

## 2. A token-fájl formája és helye (4. lépés b)

**Hely (javaslat):** `eszkozok/olvaso_szerver/konfig/arculat.json` — a szerver konfigurációja mellett, a `kod_verzio` hash-ébe bevonva (a `.json` kiterjesztést fel kell venni a `kod_verzio` listájába, l. 2.3).

**Forma (javaslat):** JSON, mert (1) a mentési végpont gépi írója egyszerűbb és determinisztikusabb (rendezett kulcsok, 2 szóközös behúzás, záró újsor → kis, olvasható git-diff); (2) a design system `tokens.json`-jával egy az egyben megfeleltethető. A fájl **csak értékeket** tartalmaz; a magyar nevek, a használati leírások és a tartományok a regiszterben (`elemek.toml`) és a tokentípus-táblában (2.2) vannak, így a mentés semmilyen szabad szöveget nem ír.

```json
{
  "verzio": 1,
  "szin": {
    "accent":      { "light": "#1f5a49", "dark": "#8cc4b1" },
    "accent-soft": { "light": "#e2eee8", "dark": "#23362f" },
    "bg":          { "light": "#f5f2ea", "dark": "#151918" }
  },
  "betucsalad": {
    "ui":   "\"IBM Plex Sans\", system-ui, -apple-system, \"Segoe UI\", sans-serif",
    "text": "\"Source Serif 4\", \"Noto Serif\", Georgia, serif"
  },
  "betumeret": { "karoli-folyo": "1.25rem", "versszam": "0.6em", "torzs": "15px" },
  "sorkoz":    { "karoli-folyo": "1.85",   "torzs": "1.6" },
  "terkoz":    { "oldal": "16px", "he-csempe-fugg": "8px" },
  "lekerekites": { "csempe": "6px", "pill": "999px" }
}
```

A CSS-változó neve a csoportból és a kulcsból áll: `szin.bg` → `--bg` (a mai nevek változatlanok), `betucsalad.ui` → `--font-ui` (változatlan), `betumeret.X` → `--fs-X`, `sorkoz.X` → `--lh-X`, `terkoz.X` → `--space-X`, `lekerekites.X` → `--radius-X`.

### 2.1 A generált token-blokk

A szerver induláskor és minden mentés után a fájlból előállítja a mai `olvaso.css` 3–15. sorának megfelelő blokkot: `:root { … }` (minden token, a színek világos értékével), `@media (prefers-color-scheme: dark) { :root:not([data-tema="light"]) { … } }` és `:root[data-tema="dark"] { … }` (a színek sötét értékével, `color-scheme: dark`). A stíluslap (`olvaso.css`) ezután **egyetlen token-értéket sem tartalmaz**, csak `var(--…)`-hivatkozást; egy teszt ezt ellenőrzi (a `:root` és a `data-tema` szabály hiánya az `olvaso.css`-ben, és minden `var(--x)` létező token).

### 2.2 Tokentípusok és a mentés értékszűrése (a brief 3. pontja)

| Típus | Csoport | Elfogadott alak | Tartomány (javaslat) |
|---|---|---|---|
| szín | `szin` | `#rgb`, `#rrggbb`, `rgb(r, g, b)`, `hsl(h, s%, l%)` | — |
| hossz | `betumeret` | `px`, `rem`, `em` | px: 8–64 · rem/em: 0.5–4 |
| hossz | `terkoz` | `px`, `rem`, `em` | px: 0–64 · rem/em: 0–4 |
| hossz | `lekerekites` | `px` | 0–999 (a `pill` 999-e miatt) |
| szorzó | `sorkoz` | szám, mértékegység nélkül | 1.0–2.4 *(csak ha a DT-F98c engedi)* |
| — | `betucsalad` | **nem írható** a mentési végponton (szabad szöveg) | — |

A végpont csak a regiszterben valamely elemhez rendelt tokent fogadja; ismeretlen kulcs, rossz alak vagy tartományon kívüli érték → 400, a fájl változatlan.

### 2.3 Gyorsítótár és ETag

A mai kulcs (`alkalmazas.py` 80. sor) a `kod_verzio`-t tartalmazza, amely induláskor számolódik és a `.json`-t nem látja. Javaslat: a kulcs és az ETag kap egy `arculat_hash` tagot (a token-fájl tartalmának sha256-ja), amelyet a mentés frissít; a lap a stíluslapot `/arculat.css?v=<arculat_hash>` címen linkeli, így a böngésző is az új változatot kéri. A mentés után a lap-gyorsítótár ürül (`Gyorsitotar.urit()`), mert a régi kulcsok úgyis elérhetetlenné válnak.

### 2.4 Szinkron-kimenet a design systemhez

`eszkozok/olvaso_szerver/arculat_szinkron.py --kimenet <út>`: a token-fájlból a design system `tokens.json` szerkezetét állítja elő (`color.themes/tokens`, `type.families/groups/styles`, `spacing.tokens`, `radius.tokens`, `meta`). A `usage` és `sample` mezők a regiszterből jönnek (az elem magyar neve és csoportja), a `meta.ref` a git HEAD. Feltöltés nincs; azt a felhasználó kérésére az ügynök végzi.

## 3. A méret-tokenek névjegyzéke (4. lépés c)

Az értékek a mai `olvaso.css` **ténylegesen érvényes** deklarációi (a felülírt deklarációk nélkül, l. 3.5). Ahol a design system azonos nevű stílust ismer, a név azonos (pl. `karoli-folyo`, `blokkcim`, `strong-szam`); ahol nem, új név, a DS-ben új stílusként jelenik meg.

### 3.1 Betűméret (`--fs-*`) és sorköz (`--lh-*`)

| Token | Méret | Sorköz | Hol (szelektor) | DS-stílus |
|---|---|---|---|---|
| `torzs` | 15px | 1.6 | `body` | torzs |
| `logo` | 1.15rem | — | `.logo` | — |
| `oldalcim` | 1.625rem | 1.25 | `h1` | oldalcim |
| `szakaszcim` | 19px | — | `h2` | — |
| `alcim` | 16px | — | `h3` (általános) | — |
| `kiscim` | 14px | — | `h4` (általános) | — |
| `gomb` | 13px | — | `.szintvalto a` | — |
| `gomb-kis` | 12.5px | — | `.szintvalto .szint-cim`, `.tema button` | — |
| `megjegyzes` | 13px | — | `.szam, .megj, .cimke`, `.labjegyzet`, `.valaszto label`, `.kapcs`, `.verslista` | — |
| `szoveg-jegy` | 13px | 1.4 | `.szoveg-jegy` | — |
| `szamlalo` | 13px | — | `.cimkek .cimke` | — |
| `utmutato` | 14px | — | `.utmutato summary`, `.utmutato ol` | — |
| `karoli-folyo` | 1.25rem | 1.85 | `.szoveg-oszlop` | karoli-folyo |
| `karoli-folyo-mobil` | 1.15rem | 1.75 | `.szoveg-oszlop` (≤640px) | (karoli-folyo usage) |
| `versszam` | 0.6em | — | `.versszam` | versszam (a DS 12px-et ír; a szerver relatív) |
| `panel` | 16px | — | `.jobb-oszlop` | — |
| `igehely` | 1.25rem | — | `.igehely` | — |
| `karoli-panel` | 1.375rem | 1.75 | `.karoli-szoveg` | karoli-panel |
| `blokkcim` | 1.3rem | 1.25 | `.blokk h3` | blokkcim |
| `jelleg` | 12.5px | 1.4 | `.jelleg` | jelleg |
| `allapot` | 12.5px | — | `.allapot` | — |
| `forrassor` | 13px | 1.5 | `.forras, .forrasnev` | forrassor |
| `forrascim` | 12px | — | `.forrasnev .fcim, .alapjel .fcim` | — |
| `adat-tabla` | 13.5px | — | `table.adat` | — |
| `szocikk` | 16.5px | 1.72 | `.jsz, .szoveg` | szocikk |
| `szocim-heber` | 3rem | 1.5 | `.szocim .heb` | szocim-heber |
| `szocim-gorog` | 2.2rem | 1.4 | `.szocim .gor` | szocim-gorog |
| `szoalcim` | 13.5px | — | `.szoalcim` | — |
| `alapjelentes` | 1.25rem | 1.4 | `.alapjel` | alapjelentes |
| `apparatus-cim` | 12.5px | — | `.app h4` | apparatus-cim |
| `apparatus-alcim` | 16px | 1.35 | `.torzs h5, .app h5` | apparatus-alcim |
| `cimszo-heber` | 1.4rem | — | `.cimszo .he` | — |
| `helyszam` | 12.5px | — | `.helyek` | — |
| `jel-cimke` | 12px | — | `.jel-cimke` | — |
| `csempe-heber` | 1.7rem | 1.3 (`lh-csempe`) | `.he-szo .he` | csempe-heber |
| `csempe-glossza` | 13.5px | — | `.he-szo .gl, .he-szo .at` | — |
| `csempe-megj` | 13px | 1.3 (`lh-csempe`) | `.he-szo .mf`, `.he-szo .lx.ures` | — |
| `csempe-lxx` | 14px | — | `.he-szo .lx` | — |
| `strong-szam` | 12px | — | `.he-szo .st, .ang-csempe .st, .ang-csempe .st-link, .lxx-sor small` | strong-szam |
| `lxx-sor` | 1.2rem | 1.4 | `.lxx-sor` | lxx-sor |
| — | — | 1.2 (`lh-lxx-csempe`) | `.lxx-sor > a, .lxx-sor > span` | — |
| `angol-szo` | 14px | — | `.ang-csempe .ang` | — |
| `sor` | 14px | — | `.sor` | — |
| `ubs` | 13.5px | — | `.ubs` | — |
| `il-csempe` | 16px | 1.3 (`lh-csempe`) | `.il-szo` | — |
| `il-magyar` | 1.05rem | 1.4 | `.il-szo .hu` | — |
| `il-eredeti-sor` | 14px | — | `.il-szo .er`, `.il-parositatlan` | — |
| `il-heber` | 1.5rem | 1.3 (`lh-csempe`) | `.il-szo .heb` | interlinearis-heber |
| `il-gorog` | 1.15rem | 1.3 (`lh-csempe`) | `.il-szo .gor` | — |
| `il-atiras` | 12px | — | `.il-szo .at` | — |
| `il-glossza` | 12.5px | — | `.il-szo .gl` | — |
| `il-strong` | 11.5px | — | `.il-szo .st` | — |
| `heb-betu` | 1.15em | — | `.heb` (szövegközi) | — |

52 betűméret-token és 18 sorköz-token (a csempék közös 1.3-as sorköze egy token: `lh-csempe`; az LXX-csempéé `lh-lxx-csempe`). Az ugyanazon szerepű, ma azonos értékű helyek egy tokenen osztoznak (pl. `megjegyzes`: 7 szelektor); a különböző szerepű, véletlenül azonos értékűek külön tokent kapnak (pl. `szamlalo` és `megjegyzes`, mindkettő 13px) — így egy elem állítása nem húzza magával a szerepen kívüli elemeket (DT-F98a).

### 3.2 Térköz (`--space-*`)

Csak a regiszterben kitett térközök (DT-F98b, javaslat (a)):

| Token | Érték | Hol |
|---|---|---|
| `oldal` | 16px | `.fejlec`, `.tartalom`, `.labjegyzet` vízszintes párnája |
| `fejlec-fugg` | 10px | `.fejlec` függőleges párna |
| `fejlec-sor` · `fejlec-oszlop` | 12px · 20px | `.fejlec` gap |
| `tartalom-fent` · `tartalom-lent` | 12px · 32px | `.tartalom` párna |
| `labjegyzet-fugg` | 12px | `.labjegyzet` |
| `gomb-fugg` · `gomb-vizsz` | 4px · 10px | `.nezetvalto a` |
| `gombsor` | 4px | `.nezetvalto`, `.szintvalto`, `.fulek` gap |
| `valaszto-sor` · `valaszto-oszlop` | 10px · 14px | `.valaszto` gap |
| `oszlopkoz` | 16px | `.oszlopok` gap |
| `panel-fugg` | 24px | `.jobb-oszlop` függőleges párna (a vízszintes `clamp(18px, 2vw, 30px)` literál marad) |
| `blokkkoz` | 18px | `.blokk` padding-bottom és margin-bottom |
| `cimkesor` | 6px | `.cimkek` gap |
| `szamlalo-fugg` · `szamlalo-vizsz` | 3px · 9px | `.cimkek .cimke` |
| `jelleg-fugg` · `jelleg-vizsz` | 1px · 7px | `.jelleg` |
| `utmutato-fugg` · `utmutato-vizsz` | 10px · 14px | `.utmutato` |
| `he-sor` | 6px | `.heber-sor` gap |
| `he-csempe-fugg` · `he-csempe-vizsz` · `he-csempe-min` | 8px · 10px · 72px | `.he-szo` |
| `lxx-sor-fugg` · `lxx-sor-vizsz` | 6px · 12px | `.lxx-sor` gap |
| `kis-csempe-fugg` | 2px | `.lxx-sor > a/span`, `.ang-csempe` |
| `lxx-csempe-vizsz` · `ang-csempe-vizsz` | 6px · 8px | uaz. |
| `il-csempe-fugg` · `il-csempe-vizsz` | 6px · 8px | `.il-szo` |
| `il-sor-fugg` · `il-sor-vizsz` | 8px · 6px | `.il-szavak` gap |

35 térköz-token. A többi térköz-előfordulás (kb. 120: címsor-margók, lista-behúzások, 1–3px-es finom eltolások, szélességek, `ch`/`vw` értékek, táblázat-cellák) literál marad; a listájuk az M1 naplójába kerül, indokkal.

### 3.3 Lekerekítés (`--radius-*`)

| Token | Érték | Hol | DS |
|---|---|---|---|
| `szo` | 3px | `.szo` | radius-szo |
| `kiemeles` | 4px | `.vers.kijelolt`, `.il-vers.kijelolt`, `a.he-fo:hover`, `a.er-fo:hover`, `.jel-cimke` | új |
| `kis-csempe` | 5px | `.lxx-sor > a/span`, `.ang-csempe` | radius-kis-csempe |
| `csempe` | 6px | `.nezetvalto a`, `.szintvalto a`, `.ful` (felül), `.tema button` (szélen), `.szoveg-jegy`, `.he-szo`, `.il-szo` | radius-csempe |
| `panel` | 10px | `.utmutato`, `.jobb-oszlop` | radius-panel |
| `pill` | 999px | `.jelleg`, `.cimkek .cimke`, `.allapot`, `.helyek` | radius-pill |

A lekerekítés szándékosan közös tokeneken áll (egységes forma); a panel ilyenkor kiírja: „ez a lekerekítés 7 szabályban, N elemen hat”.

### 3.4 Színek

A mai 10 színtoken változatlan nevekkel (`bg`, `panel`, `fg`, `muted`, `rule`, `accent`, `accent-soft`, `gold`, `gold-soft`, `low`), világos és sötét értékkel; a design system nevei azonosak. Új színtoken nincs.

### 3.5 Felülírt („holt”) deklarációk

A `holt.py` 588 szelektoronkénti deklarációból **46-ot** talált, amelyet ugyanazon szelektor egy későbbi deklarációja teljesen felülír (az F76-arculat blokk a régi értékekre írt rá): pl. `body { font: 16px/1.5 … }` → 15px/1.6; `.jobb-oszlop { border-radius: 8px; padding: 10px 12px; font-size: 14.5px }`; `.he-szo { min-width: 64px; padding: 6px 8px }`; `.il-szo .hu { font-weight: 600 }`. Ezek a megjelenésre nem hatnak, de félrevezetők: aki a stíluslapban a `14.5px`-et keresi, rossz helyen állít. Javaslat: az M1 törli őket (DT-F98d), és a megjelenés-azonosság mérése ezt is lefedi.

## 4. A panel működésének vázlata (4. lépés d)

**Bekapcsolás.** A fejlécben a szintváltó mellett „Tervező” kapcsoló (csak `belso` kiadásban van a HTML-ben; a `tervezo.js` és a `tervezo.css` is csak ott linkelődik). Bekapcsolva a `<html>` `data-tervezo` attribútumot kap; a normál kattintások (szó-lap betöltése, linkek) ilyenkor nem navigálnak.

**Kiemelés.** Rámutatáskor a legbelső regisztrált elem kerete (`outline`, a `tervezo.css`-ből) és egy címke a magyar nevével („Héber szócsempe”). Regisztrálatlan elemnél szaggatott keret és „nem regisztrált elem: `.osztaly`”.

**Panel** (jobb alsó sarokban lebegő, mozgatható doboz):

```
┌ Héber szócsempe ─────────────── [Szülő elem ↑] [×] ┐
│ Vers részletei · .he-szo                            │
│ Háttér            ■ bg        [paletta ▾]  2 témában │
│   ↳ ez a szín 14 szabályban, 212 elemen hat a lapon │
│ Keret színe       ■ rule      [paletta ▾]            │
│ Lekerekítés       ──●──────  6px     (radius-csempe) │
│ Belső térköz (f.) ───●─────  8px                     │
│ Belső térköz (v.) ────●────  10px                    │
│ Legkisebb szél.   ─────●───  72px                    │
├─ Változások (3) ──────────────── [Mindet vissza] ───┤
│ radius-csempe  6px → 8px                     [↶]    │
│ bg (világos)   #f5f2ea → #f3efe4             [↶]    │
│ space-he-csempe-vizsz  10px → 12px           [↶]    │
├─────────────────────────────────────────────────────┤
│ [Küldés a szerverre]        [Előző mentés vissza]   │
└─────────────────────────────────────────────────────┘
```

- **Színek:** palettaminta a 10 színtoken mai értékeivel, mellette színválasztó (`input type=color`) és hex-mező. A szín a **jelenleg látott témában** állítódik (világos vagy sötét); a panel mindkét értéket mutatja. Ha a felhasználó a színtokent írja át, a panel kiírja, hány szabályban és hány elemen hat (1. cél 3. pont).
- **Hosszak:** csúszka a 2.2 tartományában, a mértékegység a mai értéké (px marad px, rem marad rem); finom lépés: px-nél 0.5, rem/em-nél 0.025.
- **Előnézet:** `document.documentElement.style.setProperty('--token', érték)`; színnél az aktív témáé, témaváltáskor a JS a másik téma értékeire cseréli. CSSOM-állítás, nem inline `style`-attribútum és nem inline `<style>`: a mai CSP (`style-src 'self'`) mellett működik, a CSP nem lazul.
- **Regisztrálatlan elem (tartalék):** a szerver a `/tervezo/terkep.json` végponton (csak `belso`) adja a stíluslap szabálytérképét: szelektor → {tulajdonság → token}. A kliens az `element.matches(szelektor)` alapján kiválogatja az elemre ható szabályokat, és a tokenjeiket gépi névvel kínálja („`--fs-strong-szam` · betűméret”), „nem regisztrált elem — Felvétel a regiszterbe” jelzéssel; a jelzés mellett egy másolható `elemek.toml`-részlet áll (a regisztert nem írja).
- **Változáslista:** tokenenként egy sor (régi → új), egyenként és egészben visszavonható; a lista a böngésző `sessionStorage`-ában megmarad lapváltáskor (ugyanazon a szerveren böngészve az előnézet követi a felhasználót), mentés vagy „Mindet vissza” üríti.
- **Küldés a szerverre:** `POST /tervezo/mentes`, JSON-törzs csak a változott tokenekkel, `X-Tervezo-Kod` fejléccel. Siker után a lap újratölt (az új `arculat.css?v=` hash-sel), és a változáslista üres.
- **Előző mentés vissza:** `POST /tervezo/visszaallit` (ugyanazokkal a feltételekkel): a mentés előtti állapot (`konfig/arculat.json.elozo`, git-ignorált) visszaírása.

**Biztonság (a brief 3. pontja, tervezett megvalósítás):**

| Követelmény | Megvalósítás |
|---|---|
| csak `belso` kiadás | a `/tervezo/*` útvonalak és a kapcsoló/szkript csak `kiadas == 'belso'` mellett jönnek létre; más kiadásban 404, a HTML-ben semmi (teszt: a lap szövegében nincs `tervezo`) |
| csak helyi kérés | `request.remote_addr in ('127.0.0.1', '::1')` **és** nincs `X-Forwarded-For`/`Forwarded` fejléc (fordított proxy mögött a távoli kérés is loopbackről érkezik) **és** a `Host` `localhost`/`127.0.0.1`/`[::1]` (DNS-rebinding ellen); különben 403 |
| csak `POST`, egyszeri ellenőrző kód | a kódot **nem** a gyorsítótárazott lap hordozza (azt minden látogató ugyanúgy kapná), hanem a `GET /tervezo/kod` adja (`no-store`, csak helyi kérésre); minden mentés elhasználja és újat ad; hiányzó vagy rossz kód: 403 |
| csak regisztrált tokenek, érvényes értékek | 2.2 szerint; minden más 400 |
| atomi írás, visszaállítható | ideiglenes fájl ugyanabban a könyvtárban → `os.replace`; előtte a régi tartalom `arculat.json.elozo`-ba |
| újratöltés, ETag | a mentés után a token-blokk újraépül, az `arculat_hash` frissül, a lap-gyorsítótár ürül (2.3) |

## 5. Megfigyelések a mai stíluslapról (nem javítom; döntés nélkül nem nyúlok hozzá)

1. **`.igehely` kettős szerepe.** A `.igehely { font: 600 1.25rem var(--font-text) }` (`olvaso.css` 175. sor) a vers-panel címére (`h2.igehely`) készült, de a blokkok táblázataiban az igehely-hivatkozás is `a.igehely` (`blokkok.py` 134. sor, `ig_link`), tehát a Nave-, TSK- stb. táblákban a hivatkozás 1.25rem-es, félkövér, talpas betűvel jelenik meg a 13.5px-es táblában. Az M1 megjelenés-azonossága ezt megtartja (a regiszterben két elem, ugyanazon a tokenen: 33 és 43); ha szándékolatlan, a javítás külön döntés.
2. **A design system `oldalcim` stílusa** `fontWeight: "300"`, a szerver `h1`-je 600 (`olvaso.css` 167. sor). A szinkron-szkript a szerver értékét írja vissza; a vastagság nem tartozik a tervező mód tokenjei közé.
3. **A DS `versszam` stílusa** 12px-et ír, a szerver 0.6em-et (a folyó szöveg 1.25rem-jéhez mérve 12px). A token relatív marad; a szinkron mindkettőt kiírja („0.6em, a folyó szövegben 12px”).

## 6. Az M1 megjelenés-azonossági mérése (terv)

A brief szerint a két pilot-szakasz (1Móz 1:1–2:3, Zsolt 22) és egy ÚSZ-fejezet lapjai a csere előtt és után azonosan renderelnek. **Módszer (javaslat):** a számított stílusok összevetése. Egy mérőszkript a futó szerver lapjain (1Moz/1, 1Moz/2, Zsolt/22, Jn/1; mindhárom nézetben; világos és sötét témában; egy héber és egy görög szó-lap) minden elemre kiírja a `getComputedStyle` méret-, szín- és tipográfia-tulajdonságait, a csere előtt és után; az összevetés 0 eltérést vár. Eszköz: Playwright (ha a `uv` környezetben telepíthető), egyébként a beépített böngésző JavaScript-eszköze ugyanazzal a mérő-szkripttel. Eltérésnél ⛔ megállás (a brief szerint). A mérés naplója proveniencia-sorral a zárónaplóba kerül.

## 7. Döntésre váró pontok (DT-F98a–e, `DONTESEK.md`)

| # | Kérdés | Javaslat |
|---|---|---|
| DT-F98a | A betűméret-tokenek szemcsézettsége: szerep szerinti tokenek (52, 3.1) vagy értékskála (kb. 24, pl. `fs-13`)? | szerep szerinti (az elemből induló állítás nem húzza magával a szerepen kívüli elemeket) |
| DT-F98b | A térköz-tokenek köre: csak a regiszterben kitett térközök (35, a többi literál, listázva) vagy minden térköz-érték? | csak a kitett térközök |
| DT-F98c | A sorköz állítható legyen-e (a brief a betűméretet, térközt, lekerekítést nevezi meg; a sorköz mértékegység nélküli szám)? | igen: `sorkoz` tokenek, 1.0–2.4 közti szám, a mentés értékszűrésében külön típus |
| DT-F98d | A 46 felülírt („holt”) deklaráció: az M1 törli, vagy érintetlen marad? | törli (a megjelenés-azonosság mérése lefedi) |
| DT-F98e | A token-blokk előállítása: dinamikus útvonal (`/arculat.css?v=<hash>`, nincs generált fájl a repóban) vagy generált, verziózott `statikus/arculat.css` (GENERÁLT fejléccel)? | dinamikus útvonal; a statikus export (`export.py`) ugyanabból a függvényből írja ki |

## 8. Állapot

M0 kész, **⛔ jóváhagyásra vár**: a felhasználó a regiszter (1.1) magyar neveit és a tulajdonságok körét, valamint a DT-F98a–e-t hagyja jóvá vagy módosítja. Az M1 a jóváhagyás után indul, ugyanezen az ágon (`claude/tervezo-mod`).
