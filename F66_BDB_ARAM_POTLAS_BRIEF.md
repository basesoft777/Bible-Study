---
feladat: 66
cim: A BDB elvetett arámi szócikkeinek pótlása a BDB.lexicon szövegéből (külön táblába)
kod: BDB_ARAM_POTLAS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: megallt
ag: claude/bdb-aram-potlas
ad: a BDB_strong_alias_elvetett.tsv 173 arámi másodlagos címkéje (BDB9264-től) saját szövegsort kap egy külön táblában (konkordancia/BDB_aram_potlas.tsv) a BDB.lexicon szövegéből, proveniencia-jelöléssel; ami nem állítható elő egyértelműen, jelölt marad; a BDB_teljes_unabridged.tsv nem változik
kovetkezo: "Te: a 20 szúrópróba-sor jóváhagyása (naplok/BDB_ARAM_POTLAS_szurop.md); utána M3 zárás"
olvas: [konkordancia/lexikonok_nyers/BDB.lexicon, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, konkordancia/BDB_strong_alias_elvetett.tsv, konkordancia/BDB_strong_alias.tsv, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/_convert_bdb.py, naplok/BDB_STRONG_POTLAS_M1.md, eszkozok/bdb_strong_potlas.py, adat/licencek.tsv]
ir: [konkordancia/BDB_aram_potlas.tsv, konkordancia/BDB_aram_potlas_README.md, eszkozok/bdb_aram_potlas.py, eszkozok/teszt_bdb_aram_potlas.py, naplok/BDB_ARAM_POTLAS_M0.md, naplok/BDB_ARAM_POTLAS_zaras.md, naplok/ELLENOR_BDB_ARAM_POTLAS.md]
fugg: [57]
---

# F66_BDB_ARAM_POTLAS_BRIEF.md — A BDB elvetett arámi szócikkeinek pótlása

*FELADATOK #66 · Modell: sonnet · v1 · 2026.10.06 · forrás: DT40 (a #57 nyitott tétele), felhasználói döntés 2026-10-06 (chat): 1., és a befogadási egyeztetés A) változata*

## 1. Cél

A #57 (BDB_STRONG_POTLAS) a `BDB.lexicon` 529 másodlagos Strong-címkéjéből 296-ot alias-táblába tett, 233-at elvetett (`konkordancia/BDB_strong_alias_elvetett.tsv`). Az elvetettek közül **173 arámi szócikk** (a BDB9264-től induló arámi rész): 172 `nem_ebbol_a_szocikkbol` (a testvérsor a héber szócikk sora, pl. H0004 → H0003, H0007 → H0006) és 1 `a_testversor_mas_szocikk` (H3606 → H6903). Ezeknek az arámi Strong-számoknak a `BDB_teljes_unabridged.tsv`-ben nincs saját sora, csak a héber testvérükre mutató címke; a szócikk saját szövege viszont megvan a `BDB.lexicon`-ban.

A cél: ezek a szócikkek saját, a `BDB.lexicon` szövegéből előállított sort kapjanak. A CLAUDE.md 3. szabálya szerint a hiány csak a forrás szövegéből pótolható; ami nem állítható elő egyértelműen, jelölt marad.

**Előfelmérés (a befogadáskor, `manual`, ts=2026-10-06):** a `BDB.lexicon` nyelvjelölése szerint a másodlagos címkék között 187 arámi szócikk van; ebből 14 alias (`BDB_strong_alias.tsv`), 173 elvetett. A DT40 becslése kb. 190 új sor; a pontos számot az M0 adja.

## 2. Hatókör

**Benne van:**
- az elvetett arámi sorok felmérése (M0);
- a szócikkszöveg előállítása a `BDB.lexicon`-ból, jelölttáblában (M1);
- a jóváhagyott sorok rögzítése a **külön** `konkordancia/BDB_aram_potlas.tsv` táblában, provenienciával (M2);
- tesztek, README.

**Nincs benne:**
- **a `BDB_teljes_unabridged.tsv` módosítása.** A befogadáskor a felhasználó az A) változatot választotta: a fő táblát a #38, a #56 és a #60 olvassa, ezért ha a #66 írná, mindhárom rá várna, és a futó #38 megállna. A fő táblába emelés későbbi, külön lépés (a #38 aktuális adagja után, a felhasználó döntésével);
- az arámi szócikkek fordítása: a #38 dolga, a beemelés után;
- a `BDB_strong_alias_elvetett.tsv` és a `BDB_strong_alias.tsv` módosítása: a #57 kimenete, a #66 csak olvassa;
- a héber elvetett sorok (60; köztük a `kuszob_alatt` és a `kifejezes_tarscimke` kód).

## 3. Lépések

### M0 — Felmérés (csak olvas)

Jelentés: `naplok/BDB_ARAM_POTLAS_M0.md`.
1. Az elvetett tábla `nyelv=aram` sorai: darab `indok_kod` szerint, BDB-azonosító-tartomány; a 187-es szám reprodukálása (187 = 14 alias + 173 elvetett), az ellenőri 198-as eltérés (M1-napló 75. sor) újramérése, ha reprodukálható.
2. Szócikkenként: van-e a `BDB.lexicon`-ban önálló, nem üres `Definition`; csonk-e (a #57 korlátja szerint a csonk szócikk gyenge bizonyíték).
3. Ugyanarra a BDB-azonosítóra több másodlagos címke mutat-e; ugyanarra a Strong-számra több BDB-szócikk-e.
4. Az OSHL-index szerint az arámi Strong-szám lemmája egyezik-e a BDB-címszóval (a #57 M1 normalizálásával).

### M1 — Jelölttábla és ⛔

Új szkript: `eszkozok/bdb_aram_potlas.py` (a `bdb_strong_potlas.py` normalizálását és szövegtisztítását használja újra, nem másolja, ha importálható). Kimenet: `konkordancia/BDB_aram_potlas.tsv`, oszlopai: `Strong_padded`, `bdb_id`, `cimszo`, `oshl_lemma`, `allapot` (`egyertelmu` / `csonk` / `tobb_jelolt` / `nincs_szoveg`), `indok`, `Teljes_szocikk`, `proveniencia`. A `Teljes_szocikk` ugyanazzal a tisztítással készül, mint a `_convert_bdb.py`-ban, és ugyanaz a `H####. átírás héber` fej áll az elején, mint a fő tábla soraiban.

**⛔ Megállás.** A felhasználó jóváhagyja:
- **(a)** az `egyertelmu` sorokat (legalább 20 soros szúrópróba, köztük a H0004, a H0007 és a H3606);
- **(b)** a `csonk` és a `tobb_jelolt` sorok kezelését: maradjanak jelöltek (javaslat), vagy kapjanak kézi döntést.

### M2 — Rögzítés a külön táblában

- A `BDB_aram_potlas.tsv` a jóváhagyás szerint véglegesül; a nem jóváhagyott sorok `allapot`-ja jelölt marad (nem törlődnek).
- A `BDB_teljes_unabridged.tsv` **bájtra azonos marad** (írás előtt és után ellenőrizve).
- `konkordancia/BDB_aram_potlas_README.md`: forrás, szabály, darabszámok állapotonként, hivatkozás a DT40-re és erre a briefre; külön bekezdésben a fő táblába emelés feltétele (a #38 aktuális adagja után, felhasználói döntéssel).
- Licenc: a forrás ugyanaz a BDB-kiadás (közkincs; `adat/licencek.tsv` BDB-sora). Új licencsor nem kell; ha a felmérés mást mutat, ⛔.

### M3 — Zárás

- `naplok/BDB_ARAM_POTLAS_zaras.md` (≤20 sor): végszámok állapotonként; új nyitott tétel helyőrzővel (`N-F66a`): a jóváhagyott sorok beemelése a `BDB_teljes_unabridged.tsv`-be és a #38 sorrendjének újragenerálása.
- A `fuggetlen-ellenor` jelentése: `naplok/ELLENOR_BDB_ARAM_POTLAS.md`; a brief fejléce `lezarva`; push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Az M0 számai reprodukálhatók (parancs és darabszám a jelentésben); a 173 elvetett arámi sor mindegyike szerepel a jelölttáblában valamelyik `allapot`-tal.
- **K2.** Minden `egyertelmu` sor szövege a `BDB.lexicon` saját szócikkéből származik, `indok`-kal és proveniencia-sorral.
- **K3.** A `BDB_teljes_unabridged.tsv`, a `BDB_strong_alias.tsv` és a `BDB_strong_alias_elvetett.tsv` bájtra azonos.
- **K4.** A `teszt_bdb_aram_potlas.py` zöld (legalább: a H0004 sora, a H3606 esete, egy csonk szócikk jelöltként marad, a fej formátuma egyezik a fő tábláéval).
- **K5.** A CI zöld; a független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-06 | DT40: az elvetett arámi szócikkek pótlása külön feladat (1. opció). | felhasználó (chat) |
| v1 | 2026-10-06 | A) változat: a pótlás külön táblába megy, a `BDB_teljes_unabridged.tsv` nem változik, hogy a #38, a #56 és a #60 ne várjon rá; a beemelés későbbi lépés. | felhasználó (chat, befogadás) |
| v1 | 2026-10-06 | Csak a forrás saját szócikkszövege kerül be; ami nem egyértelmű, jelölt marad (CLAUDE.md 3. szabály). | befogadás |
