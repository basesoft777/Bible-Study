# PaRDeS nyílt mag — olvass el

# GENERÁLT: a PaRDeS nyílt mag exportja (CC BY 4.0), a projekt adataiból generálva — kézzel nem szerkesztendő; a „#” kezdetű sor megjegyzés.

**Licenc:** CC BY 4.0 (a nyílt mag saját adata és szövege). A `cc_by_sa_reteg/` könyvtár tartalma külön, CC BY-SA 4.0 licenc alatt áll; l. az ottani `OLVASSEL.md`-t.

**Mi ez.** Egy bibliai motívumkutatás (PaRDeS-módszer) nyílt magja: a motívumok meghatározó jegyei, az előfordulás-lista, a kizárt helyek okkal, az igehely-kapcsolatok és a döntésnapló. A fájlok az adatból generált, olvasónak szóló nézetek; a munkaközi jelölések feloldva vannak. Az oszlopok és kódok leírása: `kodkonyv.tsv` / `KODKONYV.md` (magyar és angol).

**Ismert hibák:** l. `ISMERT_HIBAK.md`.

## Fájlok és sorszámuk

| Fájl | Sor |
|---|---|
| `beepitesi_dontesek.tsv` | 257 |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | 237 |
| `dontesnaplo.tsv` | 8 |
| `elofordulasok.tsv` | 255 |
| `forrasok_es_licencek.tsv` | 54 |
| `kapcsolatok.tsv` | 32 |
| `kizaras_csoportok.tsv` | 3115 |
| `kizarasok.tsv` | 418 |
| `kodkonyv.tsv` | 210 |
| `motivum_kapcsolatok.tsv` | 3 |
| `motivumok.tsv` | 9 |

## Licencszűrés

A szűrés a projekt licenc-leltára szerint történt. **Kizárt források** (a csomag értéket nem tartalmaz belőlük): `BDB_forditas`, `Cremer_nyers`, `Girdlestone`, `Heber_ETCBC_modulok`, `KJV_ASV_Strongs`, `KJV_Strongs_teljes`, `KJV_teljes_szoveg`, `Karoli_Strong_kivonat`, `Karoli_Strong_parok`, `Karoli_Strong_szavak`, `Karoli_versmegfeleltetes`, `LSJ`, `LXX_kivonat`, `LXX_lexicon`, `LXX_versszintu_parok`, `MCGED`, `SDBH_SDGNT_segedtablak`, `UBS_DBH`, `UBS_DNTG`, `karoli_modern`, `karoli_variancia`, `lexikonok_nyers`, `simplemma_nyelvi_adat`, `szoto_tablak`, `tW_szocikkek`. Okuk soronként a `forrasok_es_licencek.tsv` `ok` oszlopában áll (nem kereskedelmi vagy GPL licenc, tisztázatlan licenc, a projekt zárt származtatott rétege). Ez a leltár, nem jogi vélemény.

## Közzétételi hely

A csomag kanonikus közzétételi helye: `<KANONIKUS_FORRAS_URL>` (helyőrző; a közzétételkor töltődik ki). A változatot a kiadás azonosítója jelöli (`KIADAS.txt`: az adatállapot dátuma és a tartalmi hash), nem egy fejlesztői tár vagy commit.

## Idézés és a mesterséges intelligencia használata

A kiadás mellé idézési metaadat (Citation File Format) és a mesterséges intelligencia használatáról szóló nyilatkozat kerül a közzétételi helyen; a szerző által kitöltendő mezőik a közzétételig helyőrzők. A nyilatkozat két réteget különít el: a nyílt adatmagot (CC BY 4.0, ez a csomag) és a szócikkeket mint kapcsolódó művet (minden jog fenntartva).

## Csoportos kizárás

A `kizarasok.tsv` egyes sorai **összesítő sorok**: egy csoport (azonos ok miatt kizárt versek) első versét nevezik meg, a `csoport_versszam` oszlop a csoport verseinek számát adja, a csoport összes versét a `kizaras_csoportok.tsv` sorolja fel. Az összesítő sor indoklása a csoportra érvényes.

## Mi van benne, mi nincs (adatréteg és termékréteg)

**Benne van (adatréteg):** a motívum azonosítója, címe és kizáró jegye; az előfordulások (igehely, szóbázis, szótári jelentés, Károli-szó); a kizárások és a beépítési döntések indoklással; a kapcsolatok; a proveniencia (a forrás megnevezése, licence, a lekérdezés típusa, dátum); a döntésnapló.

**Nincs benne (termékréteg):** az értelmező próza (kivonat, értelmezés, igehelyenkénti kifejtés), a magyar szótári fordítások, a kötetanyag és a lexikonlapok.

## Ami nincs a csomagban

- A `nyitva` állapotú (még el nem döntött) jelöltek: 129 db.
- Az értelmező próza, a fizetős réteg (magyar szótári fordítások, Strong-számos Károli-szöveg), a tanulmányok és a lexikonlapok.
- A belső munkajelek: azonosítók, munkafájlok, lekérdezés-nyomok. Ahol egy döntésre hivatkozás áll, a nyilvános azonosító (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel.

## Ellenőrzés

A `ELLENORZO_OSSZEG.sha256` fájl minden fájl SHA-256 összegét tartalmazza; az export újrafuttatva bájtazonos.
