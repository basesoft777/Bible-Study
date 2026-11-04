# Data paper — váz (F167.1)

*Állapot: váz és minta-mondatok. 2026-11-04. A követelmények forrása: `folyoirat_kovetelmenyek.md`. A kézirat angolul elkészült (F167.2): `kezirat_en.md`, a számai a `szamok.py` kimenetéből; a lenti „Hiányzik” sorok közül az F162 és az F163 azóta a main-en van, a kitöltendő helyőrzők és a nyitott kérdések listája a kézirat végén áll.*

## 0. Választott folyóirat és indok

**Journal of Open Humanities Data (JOHD), Data Paper.** Indok:

1. Egyedül a JOHD-nak van kimondott data paper típusa (1000–1500 szó) és sablonja; a HIPHIL Novum cikktípusai (article, short paper, conference paper, book review) között adatközlés nincs, így oda a váz tárgya nem illik, legfeljebb short paperként, külön szerkesztői egyeztetéssel (nem ellenőrzött).
2. A JOHD elve (nyílt adat + tartós azonosító + CC BY) egyezik a két rögzített elvvel: a nyílt adatmag CC BY 4.0, a hivatkozás DOI-n megy, nem GitHub-on (`<KANONIKUS_FORRAS_URL>` / `<DOI>`).
3. A lektori kritériumok (a módszer elég részletes az újraalkotáshoz; kódkönyv; archivált szkriptek) pontosan az F162 kimenetét kérik.
4. Hátrány: **APC £1 070** (kedvezmény/mentesség kérhető a kísérőlevélben), angol nyelv, egyszeres vak lektorálás, a külső bírálat szervezése a szerzőre vár. A HIPHIL Novum (APC nincs, kettős vak, CC BY-SA) a **második csatorna**: egy későbbi módszertani short paper, amely a data paperre hivatkozik.

**Alapszabály:** a cikk csak a nyílt adatmagot írja le. Az értelmező próza, a magyar BDB/Thayer és a kötet nem része (termékréteg). GitHub-URL sehol sem kanonikus: `<KANONIKUS_FORRAS_URL>`, `<DOI>`. Szerzői név, ORCID, intézmény, támogató csak helyőrző: `<SZERZO>`, `<ORCID>`, `<INTEZMENY>`, `<TAMOGATO>`.

**Számok:** a szövegbe szám csak a mérés kimenetéből kerül; a váz minden számhelye `{{N: …}}` jelölt, mellette a lekérdezés. A mérésekhez az eszköz `kozlemeny/data_paper/szamok.py` (F167.2), amely az F162 export zárt, hash-elt csomagján fut, nem az élő táblákon, hogy a szám a DOI-val letétbe tett csomaghoz tartozzon.

## 1. Szakaszok (JOHD Data Paper sablon szerint, ≈ 1000–1500 szó összesen)

### Front matter

| | |
|---|---|
| Tartalom | Cím; szerzők `<SZERZO>`, `<INTEZMENY>`, `<ORCID>`; absztrakt (~100 szó: mi az adat, hogyan készült, hogyan használható újra); legfeljebb 6 kulcsszó (brit írásmód); CRediT-szerepek. |
| Forrás | F163: `CITATION.cff` (szerző, cím, verzió); F163: `kozlemeny/PARDES_RECEPCIOS_KERET.md` (a PaRDeS-szó helyes keretezése az absztraktban). |
| Hiányzik | Szerző(k) neve és száma; ORCID; intézmény; CRediT-szerepek (és az, hogy a prózát író modellek szerepe hogyan jelenik meg, l. AI Declaration). |
| Minta | *“We describe an open dataset of motif-indexed biblical passages, each attested by a documented Hebrew or Greek lexical chain and each candidate accepted or rejected with a stated reason.”* |

### 1. Overview

**Repository location**

| | |
|---|---|
| Tartalom | A letét DOI-ja (`<DOI>`), a rekord neve, verziója; kanonikus forrás `<KANONIKUS_FORRAS_URL>`. |
| Forrás | F162: a Zenodo-rekordra előkészített csomag (`nyilt_mag/`, sha256). F163: `CITATION.cff`. |
| Hiányzik | A feltöltés és a DOI (nyilvános lépés, a felhasználóé); a csomag verziója. |

**Context**

| | |
|---|---|
| Tartalom | Honnan jön az adat: a PaRDeS-kutatás (motívumkutatás héber/görög gerincen), célja; a motívum-lexikon mint hosszú távú termék, és hogy a nyílt mag ennek adatrétege; a PaRDeS-szint recepciós címke, nem szerzői állítás; az ókori közel-keleti összehasonlító réteg hiánya kimondva. |
| Forrás | F163: `PARDES_RECEPCIOS_KERET.md`, `KOZEL_KELETI_HATAR.md`; `CLAUDE.md` (egyirányúság, három szabály); `adat/SEMA.md`. |
| Hiányzik | F163 szövegei még nem léteznek (párhuzamos feladat); a lexikon tárgyának rövid, külső olvasónak szóló bemutatása; hivatkozások (Hays, a szakirodalom) ellenőrzése, MI-költés elleni forrásellenőrzéssel. |
| Minta | *“The PaRDeS levels are recorded as reception labels (‘how the tradition read it’), not as claims about what the text means.”* |

### 2. Method

| | |
|---|---|
| Steps | A hétlépéses menet (gerinc-metszet, mező-hipotézis, teljes ÓSZ/ÚSZ scan, kollokáció, igealak, LXX-híd, nevesített tanító); a jelölt → döntés → előfordulás út (nincs közvetlen út a találattól az adatig); proveniencia-sor minden lekérdezésből, `manual` ahol nincs lekérdezés; üres eredmény explicit. A belső jelek (DT-számok, `gerinc_elem`) csak az F162 kódkönyvén át kerülnek be. |
| Sampling strategy | Hogyan választódtak a motívumok (új ID négy kérdése; negatív kritérium; fölérendelt fogalom); melyek vannak benne (lezárt, kiadott), és hogy a minta **nem reprezentatív** a Biblia egészére. |
| Quality control | Az ellenőrzési lánc: lektor, határ-ellenőr, független ellenőr, olvasói kapu, teljesség-mérés három hálóval (Strong, Károli-szó, szótár), a felhasználó vizuális átnézése, a javítások naplója. Jelölt-elutasítási arány. |
| Forrás | `adat/jeloltek.tsv`, `adat/elutasitasi_okok.tsv`; `naplok/F123_teljesseg_*.md/.tsv` (ALVIL-001, ANTROP-001, HAMART-001, ISTENTISZT-001); `adat/lap_atnezesek.tsv` (a felhasználó átnézése, érvényes sorok); `adat/lap_javitasok.tsv` (javítás: típus, gond, jóváhagyó); `adat/kiadasok.tsv` (kiadás, `proza_modell`); `eszkozok/olvasoi_kapu.py` (kapu-kimenet); F162: kapu-jelentés; `MUNKAMENET.md`. |
| Hiányzik | A lánc **külső** eleme: nincs független szakmai lektorálás, a határ-ellenőr és a független ellenőr is MI-ügynök (ezt ki kell mondani, nem szépíteni); az átnézés néhány lexikonlapra szól (az érvényes sorok számát a lekérdezés adja); nincs inter-annotátor mérés; a teljesség-mérés három hálója nem teljes lefedettség-bizonyíték. |
| Minta | *“No candidate reaches the dataset directly from a search hit; each passes through a candidate table with a decision and a stated reason.”* |
| Számok | `{{N: elutasított/összes jelölt}}` ← `adat/jeloltek.tsv` döntés-oszlop szerinti darabszám (F162 export); `{{N: teljesség-háló eltérései}}` ← `naplok/F123_teljesseg_<ID>.md` 1. összegző tábla. |

### 3. Dataset description

| | |
|---|---|
| Tartalom | Repozitórium neve; objektum neve; fájlok (TSV, kódkönyv), formátum és verzió; létrehozás dátumai (ÉÉÉÉ-HH-NN); készítők; nyelv (a kódkönyv hu/en; a szöveges adat magyar és héber/görög, oszlopnevek: eldöntendő); licenc (CC BY 4.0); közzététel dátuma. Táblák és oszlopok rövid leírása; **külön réteg** az SDBH/SDGNT-domének (CC BY-SA 4.0, attribúcióval); „ismert hibák” (Károli-KH-lista, N-F156a). Kizárt források (NC/GPL, tisztázatlan licenc) a licenc-szűrés szerint. |
| Forrás | F162: `nyilt_mag/` (export), `adat/nyilt_kodkonyv.tsv` (kódkönyv), a csomag „ismert hibák” szakasza, kapu-jelentés; `adat/licencek.tsv`, `adat/datasetek.tsv`. |
| Hiányzik | Az F162 még nem készült el (a feladat nem indult); a Zenodo-rekord; a készítők listája; a nyelv-mező döntése. A harmadik fél adatainak (Károli 1908, TAHOT/TAGNT/STEPBible, BSB stb.) licenc-állapota a `licencek.tsv` szerint **jogi ellenőrzést** kíván, és a JOHD a harmadik fél tartalmához engedélyt kér: nyitott. |
| Számok | `{{N: motívumok}}` ← `adat/motivumok.tsv` (kiadott/lezárt sorok); `{{N: előfordulások}}` ← `adat/elofordulasok.tsv` (a csomagban szereplő sorok); `{{N: jelöltek}}` ← `adat/jeloltek.tsv`; mind az F162 exportból, a hash-elt csomagon. |
| Minta | *“Every row carries its source dataset, its licence, the query type and the date; rows without a query are marked as manual decisions.”* |

### 4. Reuse potential

| | |
|---|---|
| Tartalom | Konkrét újrahasznosítás: lexikai motívum-kutatás (kereszthivatkozás-gráf); gépi tanulási tesztkészlet (elfogadott/elutasított jelöltek indoklással, ritka negatív példák); tanítás; magyar Károli-szövegű korpuszok; a módszer átvihetősége másik korpuszra. Korlátok: csak lezárt motívumok; MI-jelölt/MI-ellenőrzött; Károli-réteg; közel-keleti réteg hiánya; nincs külső validálás. |
| Forrás | F162 kódkönyv és „ismert hibák”; F163: `KOZEL_KELETI_HATAR.md`, `HAYS_LEKEPEZES.md`. |
| Hiányzik | Konkrét, külső felhasználói igény vagy példa (a JOHD lektorai konkrét javaslatot várnak); egy minimális bemutató példa a kódkönyvből. |

### Záró szakaszok

| Szakasz | Tartalom / forrás / hiány |
|---|---|
| **Acknowledgements** | Külső közreműködők, ha vannak: `<KOSZONET>`. Hiányzik: név. |
| **Funding statement** | `<TAMOGATO>`, támogatási szám; ha nincs, ezt kell kimondani. Hiányzik: a tény. |
| **Competing interests** | A fizetős termékréteg (kötet, előfizetés, #86) és a nyílt adat kapcsolata: **ki kell mondani** mint potenciális érdekeltséget. Forrás: #86 terv. Hiányzik: a szerző/kiadó döntése a megfogalmazásról. |
| **AI Declaration** | Forrás: F163: `kozlemeny/MI_NYILATKOZAT.md`; `adat/kiadasok.tsv` `proza_modell` oszlop (tényleges modellnevek). A JOHD a jelentős MI-hozzájárulás nyilatkozását kéri, a HIPHIL a teljes eszköznevet és verziót is. Itt: az értelmező prózát, a jelölteket és az ellenőrzések nagy részét MI végzi; ennek ki kell derülnie. Hiányzik: az F163 szöveg; a cikk saját szövegére vonatkozó nyilatkozat (ki írta a data papert). |
| **Bibliography** | APA; csak ellenőrzött hivatkozás (a JOHD a költött hivatkozást elutasítással bünteti). Hiányzik: az egész lista, DOI-kkal. |
| **Supplementary files** | Kódkönyv-kivonat, kapu-jelentés, teljesség-mérés (ALVIL/ANTROP/HAMART/ISTENTISZT). Hiányzik: kiválasztás. |

## 2. Hiányok összefoglalva

**Szerzőség** (a felhasználóra vár)

1. Ki(k) a szerző(k); intézményi kötődés; ORCID; CRediT-szerepek. A JOHD ICMJE-alapú irányelve és a HIPHIL szabálya szerint **MI nem lehet szerző** (a HIPHIL kimondja; a JOHD oldala nem tárgyalja, a kiadói irányelv ellenőrizendő); a prózát író és az ellenőrző modellek ezért az AI Declaration-ben szerepelnek, nem a szerzői listában.
2. Az emberi felelősséget a lap-átnézés (`lap_atnezesek.tsv`) és a jóváhagyás hordozza; ezt a szerzőnek vállalnia kell.
3. Összeférhetetlenség (fizetős termék) és finanszírozás.

**Külső bírálat**

4. A JOHD egyszeres vak lektorálása a **szerző** első külső szakmai bírálata; addig a lánc minden eleme belső (lektor, határ-ellenőr, független ellenőr = MI-ügynök; olvasói kapu = szkript; átnézés = a szerző-kiadó). Ezt a cikk nem takarhatja.
5. Három javasolt lektor (a kísérőlevélben opcionális): `<LEKTOR_JAVASLAT>`; a külső lektori felület (ha lesz) eredménye külön forrás.
6. Nincs inter-annotátor / külső validálás a motívum-határokra. A teljesség-mérés három hálója nem bizonyítja a teljességet.

**Anyag és letét**

7. F162 (export, kódkönyv, kapu) és F163 (szövegek) még nem kész; a szakaszok szövege ezekre vár.
8. Zenodo-letét és DOI; a `<KANONIKUS_FORRAS_URL>` meghatározása.
9. Harmadik fél tartalmának licenc-engedélye (Károli, STEPBible, BSB, SDBH/SDGNT): jogi ellenőrzés.
10. Számok: a `szamok.py` mérőeszköz és a hash-elt csomag.
11. Angol nyelvű szöveg és nyelvi lektorálás (a JOHD nem végez).
12. APC: £1 070 — fedezet vagy mentességi kérelem; kísérőlevél (miért JOHD).
13. Végleges tételszám (az `F167.1` helyőrző).
