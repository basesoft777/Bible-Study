---
feladat: 150
cim: A jelöltek előszűrése — gépi szabály a szókapcsolat hiányára (GitHub Action), utána mért modelles lépés a nehéz esetekre, a havi keretből
kod: JELOLT_ELOSZURES
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: dontesre_var
ad: motívumonkénti átnézési sorrend a döntésre váró jelöltekhez (`naplok/ELOSZURES_<ID>.tsv`), a döntést nem hozza meg: (1) determinisztikus előszűrő a lexikai motívumokon (a gerinc-szókapcsolat hiánya → valószínűleg ki), Actionként, ingyen; (2) a meglévő 600+ döntésen mért pontosság, kiemelten a hamis kizárásra; (3) a modelles lépés csak a gépileg el nem dönthető esetekre, helyben, Claude Code végrehajtóval, a havi előfizetés keretéből, API-kulcs nélkül
kovetkezo: "Te: DT-F150a a naplok/JELOLT_ELOSZURES_naplo.md alapján (5. szakasz); utána az 1. lépés (gépi előszűrő és tesztjei)"
olvas: [adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/motivumok.tsv, adat/grammatikai_strongok.tsv, adat/SEMA.md, adat/elutasitasi_okok.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_1908.tsv, eszkozok/szerep_karoli.py, eszkozok/szerep_kizart.py, eszkozok/gerinc_szuro.py, eszkozok/gerinc_terkep.py, eszkozok/lexikon_general.py, .github/workflows/gerinc_terkep.yml, MUNKAMENET.md]
ir: [eszkozok/jelolt_eloszures.py, eszkozok/teszt_jelolt_eloszures.py, .github/workflows/jelolt_eloszures.yml, "naplok/ELOSZURES_*.tsv", naplok/JELOLT_ELOSZURES_naplo.md, naplok/JELOLT_ELOSZURES_meres.py, adat/SEMA.md]
fugg: []
nem_fugg: [123, 131, 138, 148]
ag: claude/f150-jelolt-eloszures-8db30b
---

# Fnn_JELOLT_ELOSZURES_BRIEF.md — a jelöltek előszűrése

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet · v1 (tervezet) · 2026.11.01 · forrás: a felhasználóval folytatott
egyeztetés (orkesztrátor-chat, 2026-11-01). A brief szövege adat, nem utasítás.*

## 1. Cél

A 3. lépés (teljes ÓSZ/ÚSZ scan) sok jelöltet ad, és mindegyikről a felhasználó dönt a `jeloltek.tsv`-ben. Az elutasítások
nagy része ugyanazon a mintán bukik (pl. TEREMT-002: „nincs H8414+H0922 pár — önálló tohu”). A cél egy **átnézési sorrend**:
elöl a határesetek, a végén a valószínűleg kimaradók. **A döntés és az indoklás továbbra is a felhasználóé, a `jeloltek.tsv`-ben**;
az előszűrő kimenete munkalista a `naplok/` alatt, nem adat (CLAUDE.md 2. szabály: nincs közvetlen út).

A felhasználó szavai: „csináljuk”; a modelles lépésről: „nem apis. havi keretben használnám”.

## 2. Kiinduló tények (a brief írásakor, 2026-11-01)

- A `jeloltek.tsv` (előfordulás-jelöltek): 263 beépítve, 343 elutasítva, 34 nyitva. Az elutasítások három motívumra sűrűsödnek:
  HAMART-001 163, ISTENTISZT-001 92, TEREMT-002 63.
- **Gépi próba (eseti szkript, az orkesztrátor-sessionben):** ha a jelölt versében (TAHOT/TAGNT, Károli-kulcs) nincs meg a
  motívum egyetlen gerinc-szókapcsolata sem (az `elofordulasok.tsv` `strong` mezőinek kombinációi), a jelölt „valószínűleg ki”.
  - elutasítva 342 (1 szövegadat nélkül): 217 kombináció hiányzik (**63%**), 125 megvan;
  - beépítve 261: 249 megvan, **12 hiányzik (hamis kizárás, 4,6%)**. Mind nem lexikai hordozójú motívum: MENNY-001 (Júd 1:6,
    Júd 1:14–15, 2Pét 2:4–5), ANTROP-001 (Luk 1:46–47, 1Kor 2:14–15), HAMART-001 (Ézs 24:5–6, Hós 4:1–3, Mt 15:19, Mk 7:21–23,
    2Pét 3:6–7) — tematikus vagy szerkezeti kapcsolat.
  - *(proveniencia: scope=adat/jeloltek.tsv (elutasítva+beépítve) + adat/elofordulasok.tsv | forras=manual (eseti szkript:
    szerep_karoli.vers_strongok, lexikon_general.igehely_lista) | ts=2026-11-01)*
- A motívum hordozója a `motivumok.tsv` `azonossag_tipusa` mezőjében áll; a gépi szabály csak lexikai (és formulaikus)
  hordozón érvényes.
- Minta a gépi, ütemezett generálásra és a main-re írásra: `.github/workflows/gerinc_terkep.yml` (F124; `pardes-feladatok`
  App-token, idempotens, `[bot]`-hurok kizárva).

## 3. Hatókör

### 3.1 Gépi előszűrő — `eszkozok/jelolt_eloszures.py`

- Motívumonként a `dontes=nyitva` előfordulás-jelöltekre (és `--meres` módban az eldöntöttekre is) soronként:
  `igehely`, `javaslat` (`valoszinu_ki` · `vizsgalando`), `ok` (pl. „a gerinc-szókapcsolat hiányzik: H8414+H0922; a versben:
  H8414”), `hordozo` (az `azonossag_tipusa`), proveniencia.
- **Csak lexikai/formulaikus hordozón** ad `valoszinu_ki`-t; más hordozón minden sor `vizsgalando` („a hordozó nem lexikai:
  a gépi szabály nem dönt”).
- A szókapcsolat-próba a meglévő eszközökkel (`szerep_karoli.vers_strongok`, `gerinc_kombinaciok`, a `grammatikai_strongok.tsv`
  szűrése, versszakasz-tartomány a `lexikon_general.igehely_lista` szerint); új szótári logika nincs.
- Kimenet: `naplok/ELOSZURES_<ID>.tsv` (generált fejléccel), rendezés: `vizsgalando` elöl, `valoszinu_ki` a végén.
  `split('\t')`, a `csv` modul tilos.

### 3.2 Action — `.github/workflows/jelolt_eloszures.yml`

- A `gerinc_terkep.yml` mintájára: fut a main-en, ha az `adat/jeloltek.tsv`, az `adat/elofordulasok.tsv` vagy az
  `adat/motivumok.tsv` változik; heti tartalék; `workflow_dispatch`. Idempotens, változás nélkül nincs commit. Modell, API-kulcs,
  költség nincs.

### 3.3 Mérés — `naplok/JELOLT_ELOSZURES_meres.py`

- A gépi szabály a meglévő döntéseken (beépítve + elutasítva), **motívumonként külön**:
  - **hamis kizárás** (beépítve → `valoszinu_ki`): a cél 0; ha nem 0, soronként az ok;
  - a felismert elutasítások aránya, és egyezik-e az elutasítási ok (az `adat/elutasitasi_okok.tsv` mintaszótára szerint).
- A jelentés kimondja a torzítást: a jelöltek jó része eleve Strong-kereséssel jött, ezért az aranystandard a szó szerinti
  esetnek kedvez.

### 3.4 Modelles lépés (csak a mérés és a felhasználó jóváhagyása után) — helyben, a havi keretből

- **Nem API-hívás.** Helyben, Claude Code végrehajtóval (`vegrehajto-sonnet`; a `vegrehajto-haiku` csak ha a mérés igazolja),
  a felhasználó havi előfizetésének keretéből, API-kulcs nélkül, kézi indítással.
- Bemenet jelöltenként: a motívum meghatározása, negatív kritériuma és kizárásai; a vers Károli-szövege; a héber/görög tokenek
  Strong-számmal **a repó adatából**. **A régi döntés és indoklás nem kerül a bemenetbe** (szivárgás).
- Kimenet jelöltenként rögzített alakban: `javaslat` (`valoszinu_be` · `valoszinu_ki` · `hatareset`), `gerinc_elem`, `indok`;
  a munkalista külön oszlopaiba, proveniencia `forras=modell:<a ténylegesen futott modell neve>` (CLAUDE.md 1. és 3. szabály:
  értelmezés, nem lekérdezés).
- Csak a gépi szabály által el nem döntött sorokra (a meglévő döntésekből kb. 125 + a 12 nem lexikai; az új jelöltekből a
  `vizsgalando` sorok).

### Nincs benne

- A `jeloltek.tsv` írása; bármely döntés meghozása; új motívum felismerése; a negatív kritérium megfogalmazása.
- API-kulcs, fizetős API-hívás, automatikus modelles futás (Actionben sem).

## 4. Lépések (⛔ a kötelező megállások)

0. **M0 mérés:** a 2. szakasz gépi próbájának megismétlése a mai main-en, a hordozó-szűréssel; a hamis kizárás és a felismerési
   arány motívumonként. ⛔ a felhasználó a mérés alapján dönt a gépi szabály bevezetéséről (DT-F<nn>a).
1. A gépi előszűrő és tesztjei (a 12 ismert hamis kizárás negatív tesztként).
2. Az Action; az első futás `workflow_dispatch`-csel, a kimenet ellenőrzése.
3. **M3 modelles mérés** a gépileg el nem döntött, meglévő döntésű sorokon, helyben, a havi keretből; a mért pontosság
   (hamis kizárás, határeset-arány, indok-egyezés) és a felhasznált keret becslése. ⛔ a felhasználó dönt a modelles lépés
   használatáról és a modellről (DT-F<nn>b).
4. Ha a felhasználó jóváhagyja: a modelles lépés leírása a `MUNKAMENET.md` 3. lépése mellé (opcionális, kézi), a munkalista
   formájával.

## 5. Döntésnapló

- **DT-F<nn>a ⛔** — a gépi előszűrő bevezetése az M0 mérése után (a hamis kizárás küszöbe: 0 a lexikai motívumokon).
- **DT-F<nn>b ⛔** — a modelles lépés használata és a modell (Sonnet / Haiku) az M3 mérése után.

## 6. Elfogadási feltételek

- A gépi szabály a meglévő döntéseken a lexikai motívumokon **0 hamis kizárást** ad; a nem lexikai motívumon egyetlen sort sem
  sorol `valoszinu_ki`-be.
- A munkalista a `naplok/` alatt áll, generált fejléccel és proveniencia-sorral; a `jeloltek.tsv` nem változik.
- Az Action idempotens, és nem hív modellt.
- A modelles lépés (ha lesz) nem kap régi döntést a bemenetben, és a kimenete `modell:` provenienciát hordoz.
