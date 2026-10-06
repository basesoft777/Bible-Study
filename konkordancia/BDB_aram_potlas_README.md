# BDB arámi pótlás — `BDB_aram_potlas.tsv`

Feladat: #66 (`F66_BDB_ARAM_POTLAS_BRIEF.md`); döntés: DT40 (az elvetett arámi szócikkek pótlása külön feladat), DT-F66a (a nem egyértelmű sorok állapota).

## Forrás és szabály

- **Forrás:** a `konkordancia/BDB_strong_alias_elvetett.tsv` 173 arámi (`nyelv=aram`) sora (a #57 kimenete; csak olvasva), és a hozzájuk tartozó szócikkek a `konkordancia/lexikonok_nyers/BDB.lexicon`-ból (`Topic=BDB<n>`; BDB9264–BDB10020). A lemma-ellenőrzéshez: `konkordancia/OSHL_lexikalis_index.tsv`.
- **Licenc:** ugyanaz a BDB-kiadás, mint a `BDB_teljes_unabridged.tsv`-é (közkincs, a státusz a repóban „tisztázatlan”; `adat/licencek.tsv` `BDB` és `lexikonok_nyers` sora). Új licencsor nem kellett.
- **Előállítás:** `python eszkozok/bdb_aram_potlas.py --m1` (a `--m0` a felmérést, a `--szurop` a szúrópróba-kivonatot adja). A `Teljes_szocikk` ugyanazzal a HTML-tisztítással készül, mint a `_convert_bdb.py`-ban, a #57 stílusigazításával (`bdb_strong_potlas.py`), és ugyanaz a fej áll az elején, mint a fő tábla soraiban: `H<n>. <egyszerűsített átírás> <szöveg>` (átírás: az OSHL `atiras` mezőjéből, a #57 `egyszerusitett_atiras` szabályával).
- Csak a BDB.lexicon **saját szócikkének** szövege kerül a sorba. Ami nem állítható elő egyértelműen, jelölt marad (CLAUDE.md 3. szabály); azok `Teljes_szocikk` mezője üres, vagy a `csonk` esetén jelölt szöveg.
- Oszlopok: `Strong_padded`, `bdb_id`, `cimszo`, `oshl_lemma`, `allapot`, `indok`, `Teljes_szocikk`, `proveniencia`. Olvasás `split('\t')`-tel (nem `csv`).

## Állapotok és darabszámok (173 sor; elfogadott: 170 = `egyertelmu` + `kezi_elfogadott`)

| allapot | db | jelentés |
|---|---|---|
| `egyertelmu` | 169 | a BDB-szócikk saját szöveggel bír, nem csonk; a címszó az OSHL-lemmával egyezik (normalizált, vagy csak mássalhangzó-szinten, vagy a glosszák egyeznek; az `indok` mondja meg, melyik); az azonosítón nincs más táblasor nélküli Strong. Az `indok` rögzíti az eltérő pontozást (pl. H3393, H4961, H5396, H2112) |
| `csonk` | 2 | gyök-hivatkozás („√ of following”), szófaj és értelem nélkül (H3769, H5013); gyenge bizonyíték, jelölt, a szöveg megvan |
| `cimke_reszleges` | 1 | a címke nem szócikkre mutat — H0004: a BDB9264 az arámi szakasz bevezető jegyzete (`[Note]`), nincs címszava; jelölt marad, a `Teljes_szocikk` üres. (A `cimke_reszleges` az eredeti két jelentésében is érvényes: a címke nem szócikkre mutat, vagy csak részlegesen kapcsolódik; a második eset, a H2298, a felhasználói döntéssel `kezi_elfogadott` lett.) |
| `kezi_elfogadott` | 1 | **új állapotérték (DT-F66a, felhasználói döntés 2026-10-06):** kézi hozzárendelés, a sor elfogadott. H2298 → **BDB9285** (חַד, adjective, „one”): a BDB9603 (כְּ) többes címkéje (`[H1768 H1836 H2298]`) csak részlegesen tárgyalja a חַד-ot („כַּחֲדָה; together, see חַד (sub אחד)”), a חַד saját szócikke a BDB9285 (forráscímkéje a H259, ez a H2298-ra téves). Indok: „forráscímke: H259 (téves); lemma és glossza egyezik az OSHL H2298-cal; kézi hozzárendelés (felhasználói döntés)”. Proveniencia: `manual | …` (nem üres, nem „ellenőrizve”). A BDB9285 egyik alias-táblában (`BDB_strong_alias.tsv`, `BDB_strong_alias_elvetett.tsv`, `BDB_strong_potlas.tsv`) és a pótlótábla más sorában sem szerepel: ütközés nincs. A `Teljes_szocikk` a BDB9285 szövege, `H2298. had …` fejjel |
| `tobb_jelolt` | 0 | a szócikk más, táblasor nélküli Strongot is hordoz (nem dönthető el, melyikhez tartozik) |
| `nincs_szoveg` | 0 | a BDB.lexicon-ban nincs a Strongra szócikk-szöveg (hiányzó vagy üres `Definition`) |

A H3606 (BDB9612, `egyertelmu`) testvérsora a H6903 (a #57 `a_testversor_mas_szocikk` kódja): a pótolt sor a BDB9612 saját szövege.

**Felhasználói elfogadás (2026-10-06, chat):** a 169 `egyertelmu` sor (20 soros szúrópróba: `naplok/BDB_ARAM_POTLAS_szurop.md`) és a H2298 → BDB9285 kézi sor elfogadva; jelölt marad a H0004 (`cimke_reszleges`), a H3769 és a H5013 (`csonk`).

## A fő táblába emelés feltétele (külön lépés, nem ennek a feladatnak a része)

A `konkordancia/BDB_teljes_unabridged.tsv` **nem változott** (SHA-256 `40d96e57…f3cf6`, bájtra azonos a main-nel; a `BDB_strong_alias.tsv` és a `BDB_strong_alias_elvetett.tsv` is). A fő tábla olvasója a #38, a #56 és a #60.

**Duplikáció-kockázat (mérés, `naplok/BDB_ARAM_POTLAS_duplikacio.md`).** A DictBDB a közös héber–arámi szócikkeket egy sorban adja, ezért a pótolt arámi szövegek nagy része már a fő táblában van, a héber testvérsor végén (pl. H0007 a H0006 sorában, H3606 a H3605-ében). A 170 elfogadott sorból **164** szövege (a mérőszám ≥ 0,8) már megvan a fő táblában, 5 részlegesen (0,5–0,8), 1 nincs (H6433); a 164 találatból 161 a #57 elvetett táblájának `testver_strong` oszlopában szereplő sor. A mérés ujjlenyomat-alapú támpont, nem bizonyíték. Ezért a sorok fő táblába emelése **duplikációt okozhat**, és külön felhasználói döntés (nem automatikus lépés).

A felhasználó döntött (N-F66b, 2026-10-06, chat): a 164 duplikált sor **nem** kerül be új szövegsorként a fő táblába, hanem a 164 Strong-szám alias-sorként (a héber testvérsorra mutatva, a `BDB_strong_alias.tsv` mintájára); szöveges pótlásként csak a 6 valódi hiány (5 részleges + H6433) kerül a fő tábla végére az `eszkozok/bdb_strong_potlas.py --m2` mintájára, a meglévő sorok bájtra azonosak; H0004, H3769, H5013 jelölt marad. A beemelés a #38 7. adagja előtt fut, utána a #38 sorrendje újragenerálandó; ez külön feladat (`beerkezo/F66b_BDB_ARAM_BEEMELES_BRIEF_TERVEZET.md`), nem ennek a feladatnak a része.
