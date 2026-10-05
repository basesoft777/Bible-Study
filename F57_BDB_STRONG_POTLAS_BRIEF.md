---
feladat: 57
cim: A BDB-tábla hiányzó szócikkei — Strong-címke nélküli BDB-szócikkek párosítása és pótlása
kod: BDB_STRONG_POTLAS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: dontesre_var
ag: claude/bdb-strong-potlas
ad: a BDB_teljes_unabridged.tsv kiegészül azokkal a BDB-szócikkekkel, amelyek a Strong-kulcsú forrásból (DictBDB.json) kimaradtak, mert a fejlécükből hiányzik a Strong-címke (pl. H4725 mákóm, H0136 Adonaj, H0341 ójév); minden pótolt sor egyértelmű, dokumentált párosításon áll, a többi jelölt marad
kovetkezo: "Te: döntsd el a DONTESEK.md DT-F57a tételét ((a), (b), (c) rész); utána /kovetkezo az M2-vel (pótlás a táblában, README, zárás)"
olvas: [konkordancia/lexikonok_nyers/BDB.lexicon, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, konkordancia/_convert_bdb.py, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/OSHL_BDB_igehelyek.tsv, konkordancia/TAHOT_kivonat.tsv, adat/licencek.tsv]
ir: [konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_strong_potlas.tsv, konkordancia/BDB_teljes_unabridged_README.md, eszkozok/bdb_strong_potlas.py, eszkozok/teszt_bdb_strong_potlas.py]
fugg: []
---

# F57_BDB_STRONG_POTLAS_BRIEF.md — A BDB-tábla hiányzó szócikkei

*FELADATOK #57 · Modell: sonnet · v1 · 2026.10.05 · forrás: az olvasói prototípus (1Móz 1:1–2:3) szó-lapjai, felhasználói döntés 2026-10-05*

## 1. Cél

A `konkordancia/BDB_teljes_unabridged.tsv` a Strong-szám szerint kulcsolt `DictBDB.json`-ból készült (eliranwong/unabridged-BDB-Hebrew-lexicon; `konkordancia/_convert_bdb.py`). Ebből kimaradt minden BDB-szócikk, amelynek a forrásban nincs Strong-címkéje. Ugyanennek a kiadásnak a BDB-azonosító szerint kulcsolt változata (`konkordancia/lexikonok_nyers/BDB.lexicon`) viszont tartalmazza őket.

**Előfelmérés (a befogadáskor, `manual`, ts=2026-10-05):**
- a `BDB.lexicon` 10 022 BDB-azonosítós szócikkéből **846-nak nincs Strong-címkéje** a fejlécében;
- az OpenScriptures-index (`OSHL_lexikalis_index.tsv`) szerint **396 héber Strong-számnak** volna BDB-szócikke, de a táblában nincs sora (pl. H0013, H0021, H0136, H0341, H4725);
- ismert eset: a **H4725 *mákóm*** („hely”, a BDB szerint 399 előfordulás) a `BDB.lexicon` **BDB7372** azonosítóján teljes szócikkel áll („מָקוֺם … noun masculine … standing-place, place”), de a táblában nincs sora.

*(proveniencia: scope=konkordancia/lexikonok_nyers/BDB.lexicon + BDB_teljes_unabridged.tsv + OSHL_lexikalis_index.tsv | forras=manual | ts=2026-10-05)*

**Miért sürgős:** a #38 (BDB-fordítás) a fordítási sorrendet ebből a táblából állítja elő, ezért ezek a szavak soha nem kerülnének sorra. A lexikon- és szó-lapokon BDB nélkül jelennek meg.

## 2. Hatókör

**Benne van:**
- a hiány pontos felmérése (M0);
- a Strong-címke nélküli BDB-szócikkek párosítása Strong-számmal (M1);
- az egyértelmű párok pótlása a táblában, külön párosítótáblával és provenienciával (M2);
- tesztek, README.

**Nincs benne:**
- a pótolt szócikkek fordítása: a #38 dolga, a következő sorrendgenerálásnál;
- a `naplok/BDB_FORDITAS_sorrend.tsv` átírása: a #38 saját fájlja, a #38 következő menete generálja újra;
- a `DictBDB.json` meglévő sorainak módosítása;
- arámi szócikkek, ha a felmérés szerint külön kezelést kívánnak: ezek a jelentésben külön listába kerülnek.

## 3. Lépések

### M0 — Felmérés (csak olvas)

Jelentés: `naplok/BDB_STRONG_POTLAS_M0.md`.
1. A `BDB.lexicon` szerkezete: a `Lexicon` tábla `Topic` (BDB-azonosító vagy Strong-szám) és `Definition` (HTML) mezője; a Strong-címke helye a fejlécben (`lex('H…')`).
2. A címke nélküli BDB-szócikkek listája: BDB-azonosító, címszó (héber), homonímaszám (I., II.), szófaj, első glossza.
3. A táblából hiányzó Strong-számok listája az OSHL-index szerint: Strong, lemma, OSHL `bdb_id`, `def_en`, TAHOT-előfordulásszám (a #38 gyakorisági sorrendje miatt).
4. Ellenőrzés: a `DictBDB.json`-ban (a README szerinti forrás) valóban nincs-e meg a hiányzó Strong-szám, más kulcs alatt sem (pl. betűutótaggal: `H90a`).

### M1 — Párosítás és ⛔

Új szkript: `eszkozok/bdb_strong_potlas.py`. Csak olvas, és jelölttáblát ír.

Párosítási szabály (a jelentésben szó szerint rögzítve):
1. **Címszó-egyezés:** az OSHL-lemma és a BDB-címszó normalizált alakja egyezik. A normalizálás egységesíti a holem-waw írásváltozatokat (וֹ / וֺ), és eltávolítja a kantillációs jeleket. A magánhangzópontok megmaradnak.
2. **Homonímia:** ha a címszó több BDB-szócikknél is szerepel (I., II. …), az OSHL `def_en` és a BDB első glosszája közötti egyezés dönt. Ha nem dönt, a sor jelölt marad.
3. **Kizárás:** ha a BDB-szócikknek már van Strong-címkéje, vagy a Strong-számnak már van sora a táblában, nem párosítható.

Kimenet: `konkordancia/BDB_strong_potlas.tsv`, oszlopai: `bdb_id`, `strong`, `cimszo`, `oshl_lemma`, `allapot` (`egyertelmu` / `tobb_jelolt` / `nincs_par`), `indok`, `proveniencia`.

**⛔ Megállás.** A felhasználó jóváhagyja:
- **(a)** az egyértelmű párok listáját (legalább 20 soros szúrópróba, köztük a H4725, a H0136 és a H0341);
- **(b)** a `tobb_jelolt` sorok kezelését: maradjanak jelöltek (javaslat), vagy kapjanak kézi döntést.

### M2 — Pótlás a táblában

- A `BDB_teljes_unabridged.tsv` bővül a jóváhagyott párok soraival. A szöveg a `BDB.lexicon` HTML-jéből készül, ugyanazzal a tisztítással, mint a `_convert_bdb.py`-ban. A szöveg elején ugyanaz a `H####. átírás héber` fej áll, mint a meglévő soroknál.
- A meglévő sorok **nem változhatnak**. Írás előtt és után a sorok összevetése (CLAUDE.md, TSV): csak új sorok jelenhetnek meg; ha más eltérés van, állj meg.
- A README rögzíti a pótlás forrását, a szabályt, a darabszámot és a `BDB_strong_potlas.tsv`-re mutató hivatkozást.
- Licenc: a forrás ugyanaz a BDB-kiadás (BDB, közkincs; `adat/licencek.tsv` BDB-sora). Új licencsor nem kell; ha a felmérés mást mutat, ⛔.

### M3 — Zárás

- `naplok/BDB_STRONG_POTLAS_zaras.md` (≤20 sor): végszámok állapotonként. A zárójelentésben kifejezetten szerepeljen, hogy a #38 következő menete újragenerálja a fordítási sorrendet (a `BDB_FORDITAS_M0.py`), és ezzel a pótolt szócikkek bekerülnek a sorba.
- A `fuggetlen-ellenor` jelentése: `naplok/ELLENOR_BDB_STRONG_POTLAS.md`; a brief fejléce `lezarva`; push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Az M0 listái teljesek és reprodukálhatók (parancs és darabszám a jelentésben).
- **K2.** Minden pótolt sor egy `egyertelmu` párosításon áll, `indok`-kal és proveniencia-sorral; a H4725 pótolva van.
- **K3.** A tábla meglévő sorai bájtra azonosak; csak új sorok jelentek meg.
- **K4.** A `teszt_bdb_strong_potlas.py` zöld (legalább: a H4725 párosítása, a homonímiás eset jelöltként marad, a kizárási szabály).
- **K5.** A CI zöld; a független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | Külön feladat; a #38 következő adagja előtt érdemes futtatni, hogy a pótolt szócikkek bekerüljenek a fordítási sorrendbe. | felhasználó |
| v1 | 2026-10-05 | Csak egyértelmű párosítás kerül a táblába; a többi jelölt marad (CLAUDE.md 3. szabály). | befogadás |
| v1 | 2026-10-05 | A #38 sorrendfájlját a feladat nem írja; a #38 következő menete generálja újra. | írásjog (a #38 `ir`-je) |
