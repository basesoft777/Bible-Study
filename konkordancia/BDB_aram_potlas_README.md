# BDB arámi pótlás — `BDB_aram_potlas.tsv`

Feladat: #66 (`F66_BDB_ARAM_POTLAS_BRIEF.md`); döntés: DT40 (az elvetett arámi szócikkek pótlása külön feladat), DT-F66a (a nem egyértelmű sorok állapota).

## Forrás és szabály

- **Forrás:** a `konkordancia/BDB_strong_alias_elvetett.tsv` 173 arámi (`nyelv=aram`) sora (a #57 kimenete; csak olvasva), és a hozzájuk tartozó szócikkek a `konkordancia/lexikonok_nyers/BDB.lexicon`-ból (`Topic=BDB<n>`; BDB9264–BDB10020). A lemma-ellenőrzéshez: `konkordancia/OSHL_lexikalis_index.tsv`.
- **Licenc:** ugyanaz a BDB-kiadás, mint a `BDB_teljes_unabridged.tsv`-é (közkincs, a státusz a repóban „tisztázatlan”; `adat/licencek.tsv` `BDB` és `lexikonok_nyers` sora). Új licencsor nem kellett.
- **Előállítás:** `python eszkozok/bdb_aram_potlas.py --m1` (a `--m0` a felmérést, a `--szurop` a szúrópróba-kivonatot adja). A `Teljes_szocikk` ugyanazzal a HTML-tisztítással készül, mint a `_convert_bdb.py`-ban, a #57 stílusigazításával (`bdb_strong_potlas.py`), és ugyanaz a fej áll az elején, mint a fő tábla soraiban: `H<n>. <egyszerűsített átírás> <szöveg>` (átírás: az OSHL `atiras` mezőjéből, a #57 `egyszerusitett_atiras` szabályával).
- Csak a BDB.lexicon **saját szócikkének** szövege kerül a sorba. Ami nem állítható elő egyértelműen, jelölt marad (CLAUDE.md 3. szabály); azok `Teljes_szocikk` mezője üres, vagy a `csonk` esetén jelölt szöveg.
- Oszlopok: `Strong_padded`, `bdb_id`, `cimszo`, `oshl_lemma`, `allapot`, `indok`, `Teljes_szocikk`, `proveniencia`. Olvasás `split('\t')`-tel (nem `csv`).

## Állapotok és darabszámok (173 sor)

| allapot | db | jelentés |
|---|---|---|
| `egyertelmu` | 169 | a BDB-szócikk saját szöveggel bír, nem csonk; a címszó az OSHL-lemmával egyezik (normalizált, vagy csak mássalhangzó-szinten, vagy a glosszák egyeznek; az `indok` mondja meg, melyik); az azonosítón nincs más táblasor nélküli Strong. Az `indok` rögzíti az eltérő pontozást (pl. H3393, H4961, H5396, H2112) |
| `csonk` | 2 | gyök-hivatkozás („√ of following”), szófaj és értelem nélkül (H3769, H5013); gyenge bizonyíték, jelölt, a szöveg megvan |
| `cimke_reszleges` | 2 | **két jelentés:** (1) a címke nem szócikkre mutat — H0004: a BDB9264 az arámi szakasz bevezető jegyzete (`[Note]`), nincs címszava; (2) a címke csak részlegesen kapcsolódik a szócikkhez — H2298: a BDB9603 (כְּ) többes címkéje (`[H1768 H1836 H2298]`) a כְּ-vel képzett összetételekre szól, és van benne a H2298-ra vonatkozó rész („כַּחֲדָה; together, see חַד (sub אחד)”), de a szócikk maga a כְּ-et tárgyalja. A `Teljes_szocikk` üres; a H2298 `indok`-jában jelölt cél-szócikk: **BDB9285** (חַד, adjective, „one”; csak jelölt, hogy elfogadott sor legyen, a felhasználó dönt) |
| `tobb_jelolt` | 0 | a szócikk más, táblasor nélküli Strongot is hordoz (nem dönthető el, melyikhez tartozik) |
| `nincs_szoveg` | 0 | a BDB.lexicon-ban nincs a Strongra szócikk-szöveg (hiányzó vagy üres `Definition`) |

A H3606 (BDB9612, `egyertelmu`) testvérsora a H6903 (a #57 `a_testversor_mas_szocikk` kódja): a pótolt sor a BDB9612 saját szövege.

**Az `egyertelmu` sorok felhasználói elfogadása még nem történt meg** (a szúrópróba: `naplok/BDB_ARAM_POTLAS_szurop.md`); a tábla addig jelölttábla. A H0007, H3606, H3393, H4961, H5396 a felhasználó szerint rendben.

## A fő táblába emelés feltétele (külön lépés, nem ennek a feladatnak a része)

A `konkordancia/BDB_teljes_unabridged.tsv` **nem változott** (SHA-256 `40d96e57…f3cf6`, bájtra azonos a main-nel; a `BDB_strong_alias.tsv` és a `BDB_strong_alias_elvetett.tsv` is). A fő tábla olvasója a #38, a #56 és a #60, ezért a beemelés csak (1) a #38 aktuális adagja után, (2) a felhasználó döntésével, (3) csak a jóváhagyott `egyertelmu` sorokra történhet, az `eszkozok/bdb_strong_potlas.py --m2` mintájára (új sorok a tábla végére, a meglévők bájtra változatlanok); utána a #38 sorrendje újragenerálandó (N-F66a).
