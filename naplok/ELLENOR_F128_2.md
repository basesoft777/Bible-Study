TISZTA

# ELLENOR_F128_2 — újraellenőrzés a javítókör commitjain

*A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette el változtatás nélkül (formázási átalakítás nélkül, a HTML-escape-ek feloldásán kívül).*

- **Brief:** `F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md`
- **Tartomány:** `d2901cbc..fd447576`, vagyis F128.19–F128.23. Az F128.18, a main bevonása, kívül esik a hatókörön.
- **Előző jelentés:** `naplok/ELLENOR_F128.md`
- **Modell-ellenőrzés:** a tényleges modell `claude-opus-5-5`, a kért `opus`, tehát egyezik. A tartomány nem ír `modell` mezőt: a diffben nincs adattábla-adatsor, és naplósor sincs.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | Saját modell: `claude-opus-5-5`, kért: `opus`. `git diff d2901cbc..HEAD`: nem kerül be `modell` mezőt tartalmazó sor. |
| Hatókör: a javítókör az `ir`-en kívül | OK | – | `git diff d2901cbc HEAD --name-status` → M brief, M `adat/bdb_szakasz_hu.tsv`, A `beerkezo/Fnn_BDB_FEJLEC_DT_BRIEF.md`, M `eszkozok/bdb_jelolt/hu_illeszt.py`, M `eszkozok/bdb_jelolt/teszt_bont.py`. A beerkezo-fájlon kívül mind az (F128.19 után bővített) `ir`-ben van. A beerkezo-tervezetre a README 2. bejutási útja vonatkozik, és van rá precedens (`git log -- beerkezo/Fnn_LEXIKON_UJRAGEN_BRIEF.md` → F110.17/24/25/31/33). |
| Commitonkénti bontás | OK | – | `git diff --numstat <c>~1 <c>`: F128.19 brief 1/1 · F128.20 tábla 1/1 · F128.21 tábla 1/1, `hu_illeszt.py` 17/4, `teszt_bont.py` 24/0 · F128.22 beerkezo 64/0 · F128.23 brief 1/1. |
| F128.19 `ir` bővítés | OK | `F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md:13` | Az `ir` egyetlen új eleme `adat/bdb_szakasz_hu.tsv`, más elem nem változott. |
| F128.23 fejléc | OK | `F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md:11` | `kovetkezo` → `[elteres_kor 1/2] … újraellenőrzés függ: naplok/ELLENOR_F128_2.md`. Az `allapot: megallt` maradt. |
| Előző 1. eltérés: a tábla csak a `# forras` sorban tér el | OK | `adat/bdb_szakasz_hu.tsv:2` | `git diff -U0 fd25de74 HEAD -- adat/bdb_szakasz_hu.tsv` → egyetlen hunk, `@@ -2 +2 @@`: `495d1c81cfc0/f01130a1be9a/91730dafdb40/0da6faeb72d5` → `66bd24b9abb6/592f72297862/8ce0a55f14eb/8160f92ab708`. `git diff --numstat fd25de74 d2901cbc -- adat/bdb_szakasz_hu.tsv` → üres, tehát a merge nem nyúlt a táblához. |
| Előző 1. eltérés: a fejléc-hash a mai állapotot mutatja | NEM ELLENŐRIZHETŐ | `adat/bdb_szakasz_hu.tsv:2` | A kért `hu_illeszt.py --ts 2026-10-18 --ellenoriz` és a `teszt_bont.py` az ellenőr Bash-körén kívül esik, ezért nem futott. Közvetett jel: F128.20→F128.21 között a két `.tsv` hash-e nem változott (`66bd24b9abb6`, `592f72297862`), `.gitattributes:8` `*.tsv text eol=lf` mellett várható. Csak a CRLF-es checkoutú `forditas_kapuk.py` hash-e változott (`234f224b4337` → `8ce0a55f14eb`). |
| F128.21 sorvég-független hash: helyesség | OK (kódolvasás) | `eszkozok/bdb_jelolt/hu_illeszt.py:54-68` | A darabhatáron kettévágott `\r\n`-t a visszatartott záró `\r` kezeli, a magányos `\r` megmarad; a konvenció azonos a `kod_hash`-sal (`replace(b'\r\n', b'\n')`). |
| F128.21: teszt | OK (a teszt léte és tartalma); a futás eredménye NEM ELLENŐRIZHETŐ az ellenőrnek | `eszkozok/bdb_jelolt/teszt_bont.py:368-390` | `test_hash_sorveg_fuggetlen`: LF/CRLF egyezés, minden kettévágási pont, magányos `\r`, fájl-szintű egyezés, az LF-blob hash a `forditas_kapuk.py`-on. |
| F128.22 tervezet: tényállítások | OK | `beerkezo/Fnn_BDB_FEJLEC_DT_BRIEF.md:30-37` | `bont.py:618` `DT-F107a`, `forras_javit.py:319` `DT-F107f (a)`; `adat/bdb_szakaszok.tsv:2` `DT225`; `adat/bdb_forras_javitas.tsv:1` `DT228 (a)`, `:2` `bdb_szakaszok.tsv@495d1c81cfc0`. `git log -1 3fbb927a` → 2026-10-19, `DT-F107a → DT225`, `DT-F107f → DT228`. |
| F128.22 tervezet: sorszámok | OK (megjegyzéssel) | `beerkezo/Fnn_BDB_FEJLEC_DT_BRIEF.md:30-31` | Mért 36624 és 7205 sor; a tervezet 36 625-öt és 7 206-ot ír (+1, valószínűleg a `split('\n')` záró üres eleme). Csak tájékoztató szám egy nem befogadott tervezetben. |
| F128.22 tervezet: hatókör | OK (megjegyzéssel) | `eszkozok/bdb_jelolt/forras_javit.py:49-54` | A `bont.py`/`forras_javit.py` `sha256_fajl`-ja nyers bájtot hash-el, ugyanaz a hibaosztály, amit az F128.21 a `hu_illeszt.py`-ban javított. A `.tsv` és a `-text` JSON miatt ma nincs hatása; a `konkordancia/lexikonok_nyers/BDB.lexicon`-ra nincs `.gitattributes`-szabály. A tervezet ezt nem említi; befogadáskor érdemes felvenni. |
| DT-F107 / #119: a fő bukás oka | OK (jelzés) | – | A `teszt_bont` `Determinizmus.test_ellenoriz` és `test_javitas_ellenoriz` main-beli bukását a tervezet vezeti. A #128 diff nem nyúl a `bont.py`-hoz, a `forras_javit.py`-hoz és a két táblájukhoz. |
| M0–M4 / „Nem cél” | OK | – | Nincs `adat/forditasok.tsv`-írás, nincs modellhívás nyoma, a #38 fejlécéhez sem nyúlt. |
| ⛔ M0 | OK | – | A javítókör nem hoz új tervezési döntést. A `DONTESEK.md` nincs a diffben. |
| A1–A6 | OK (nem értelmezhető) | – | A diff nem hoz tanulmányt, motívumot, tanítót vagy párhuzamot. |
| CI saját futtatás | OK | – | `futtat.py --valtozott <5 fájl> --diff-alap d2901cbc --diff-fej HEAD` → E2–E16, E19, E20, E26, E28, E29, E31: 0. E25: 4, E27: 42 (a repó más fájljaira vonatkozik, nem a változottakra). E30: 3 FIGYELMEZTETÉS a commit-üzenetekre (`szamkiosztas`, `forras` — kódnév/fejléc-literál, nem ékezethiba). |
| E16 (PR-cím) | feltételes | – | `--pr-cim` nélkül 0 találat. Akkor teljesül, ha a draft PR címe `[ELLENŐRZŐ]` előtaggal nyílik. |
| 1. Kiszűrt/törölt sorok | OK | – | Törlés 7 sor összesen (brief fejléc 2, tábla fejléc 1, `hu_illeszt.py` 4). Adatsor-törlés 0. |
| 2. Kulcstartomány | OK (nem értelmezhető) | – | Strong- vagy igehely-kulcsú adatsor nem változott. |
| 3. Nulla-diff hatóköre | OK | – | Az adatsorokra 0 a diff; csak a 2. (`# forras`) sor tér el. |
| 4. E17/DT3 tábla-Δ main-hez képest | OK | – | `git diff --numstat main...HEAD -- 'adat/*.tsv' 'konkordancia/*.tsv'` → csak `adat/bdb_szakasz_hu.tsv` 1/1, Δ = 0 sor. |
| 5. ⛔ pontok | OK | – | Lásd a ⛔ M0 sort. |

A táblázatban nincs ELTÉRÉS. Nyitva / figyelmet érdemel:

1. **A fő pont saját futtatással az ellenőrnek nincs igazolva** (`hu_illeszt.py --ellenoriz`, `teszt_bont.py` nem futott az ellenőr körén belül). Az orkesztrátor/végrehajtó futtatása: `hu_illeszt.py --ts 2026-10-18 --ellenoriz` azonos; `teszt_bont.py` 48-ból 46 zöld, a 2 bukás a main-beli ismert `Determinizmus` teszt (F128.22 tervezet).
2. Két megjegyzés a tervezetről (sorszám +1; a nyers bájtos hash ugyanaz a hibaosztály): befogadáskor javítható, a #128 merge-ét nem érinti.
