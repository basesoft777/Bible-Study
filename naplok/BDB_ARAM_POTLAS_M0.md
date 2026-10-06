# BDB_ARAM_POTLAS M0 — felmérés (F66)

*Generálta: `python eszkozok/bdb_aram_potlas.py --m0` · scope=konkordancia/BDB_strong_alias_elvetett.tsv + konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/OSHL_lexikalis_index.tsv | forras=eszkozok/bdb_aram_potlas.py --m0 | ts=2026-10-06*

## 1. Az elvetett tábla `nyelv=aram` sorai

- Darab: **173** (parancs: `awk -F"\t" '$3=="aram"' konkordancia/BDB_strong_alias_elvetett.tsv | wc -l`; a `--m0` ugyanezt a `split('\t')` olvasással számolja).
- `indok_kod` szerint: `a_testversor_mas_szocikk`: 1, `nem_ebbol_a_szocikkbol`: 172.
- BDB-azonosító-tartomány: BDB9264 – BDB10020 (szám szerint rendezve).
- **A 187 reprodukálása:** a BDB.lexicon 529 másodlagos (táblasor nélküli) Strong-kulcsa közül 187 mutat arámi nyelvű szócikkre (`bdb_beolvas`, a navigációs sor „BIBLICAL ARAMAIC” jelölése); 187 = 14 alias + 173 elvetett = 187. Reprodukálva.
- **A 198 (ellenőri szám, M1-napló 75. sor) újramérése:** nem reprodukálható. Mért alternatívák: az OSHL szerint arámi másodlagos Strong: 190; ebből a BDB-ben is arámi szócikkre mutat: 185; az összes arámi BDB-szócikk (nem csak a másodlagosak): 759. Egyik sem 198; a különbség okát nem azonosítottuk (a mérvadó a feltétel, nem a szám).

## 2. Szócikkenként: önálló, nem üres szöveg; csonk

- Önálló, nem üres `Definition`: 173/173.
- Ebből valódi szócikk (van címszó, szófaj, értelem): **170**; gyök-hivatkozás (csonk, „√ of following”): **2** (H3769/BDB9625, H5013/BDB9683); nem szócikk, hanem nyelvi szakasz bevezető jegyzete: **1** (H0004/BDB9264).
- A latin betűs szöveg hossza (hivatkozások nélkül): legrövidebb 29, medián 86, leghosszabb 725 karakter. **Csonk-szabály:** a #57 korlátja (csonk = rövid latin szöveg) itt nem alkalmazható hosszküszöbbel, mert a rövid arámi szócikkek (pl. Zerubbabel, 29 latin betű) teljesek; a csonk a **gyök-hivatkozás** (szófaj és értelem nélkül).

## 3. Többszörös megfeleltetés

- Ugyanarra a BDB-azonosítóra több **elvetett arámi** címke: 0 eset.
- Ugyanarra a BDB-azonosítóra egy elvetett és egy **alias** arámi címke: 0 eset.
- Ugyanarra a Strong-számra több BDB-szócikk (a fejlécek címkéi szerint): 0 eset.
- Olyan szócikk, amely az érintett Strong mellett más, táblasor nélküli Strongot is hordoz: 0 eset.

## 4. OSHL-lemma és BDB-címszó egyezése (a #57 M1 normalizálásával)

- Összesítés: {'nincs_cimszo': 1, 'pont': 162, 'kons': 6, 'nincs': 1, 'nincs+gloss': 3} (`pont` = normalizált, pontozott egyezés; `kons` = csak a mássalhangzók egyeznek; `nincs+gloss` = a címszó eltér, de az OSHL-glossza és a BDB-glossza közös szót tartalmaz; `nincs` = semmi nem egyezik).

Eltérő sorok (nem `pont`/`kons`):

| Strong | OSHL-lemma | BDB-címszó | megjegyzés |
|---|---|---|---|
| H0004 | אֵב | — | nincs címszó (jegyzet) |
| H2298 | חַד | כְּ | glossza sem egyezik (OSHL: one; BDB: like, as, about) |
| H3393 | יְרַח | יְרַךְ | glossza egyezik: month |
| H4961 | מִשְׁתֶּה | מִשְׁתֵּי | glossza egyezik: feast |
| H5396 | נִשְׁמָא | נִשְׁמָה | glossza egyezik: breath |

