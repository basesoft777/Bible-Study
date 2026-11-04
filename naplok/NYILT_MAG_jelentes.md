# NYILT_MAG_jelentes.md — F162 (FELADATOK #162), 2026-11-04

*Modell: claude-sonnet-5-5. Generátor: `eszkozok/nyilt_mag_export.py`; kapu: `eszkozok/nyilt_mag_kapu.py`; tesztek: `eszkozok/teszt_nyilt_mag.py` (30 teszt, zöld).*

## 1. Kimenet (`nyilt_mag/`), sor táblánként

| Fájl | Sor | Forrás |
|---|---|---|
| `motivumok.tsv` | 9 | `motivumok.tsv` (mind a 9 motívum) |
| `elofordulasok.tsv` | 255 | `elofordulasok.tsv` (mind) |
| `kizarasok.tsv` | 413 | `jeloltek.tsv` `elutasítva` |
| `beepitesi_dontesek.tsv` | 257 | `jeloltek.tsv` `beépítve` (255 előfordulás + 2 motívumközi) |
| `kapcsolatok.tsv` | 32 | `kapcsolatok.tsv` |
| `motivum_kapcsolatok.tsv` | 3 | `motivum_kapcsolatok.tsv` |
| `dontesnaplo.tsv` | 8 | a hivatkozott DT-döntések (NYD-001…008) |
| `forrasok_es_licencek.tsv` | 54 | `licencek.tsv` (minden dataset) |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | 237 | SDBH/SDGNT, a csomag Strong-számaira |
| `kodkonyv.tsv` | 203 | `adat/nyilt_kodkonyv.tsv` |

Nem exportált: a **129 `nyitva` jelölt** (döntetlen). A csomag SHA-256 összegei: `nyilt_mag/ELLENORZO_OSSZEG.sha256` (a fájl maga: `7adf808e…`). Az export újrafuttatva bájtazonos (a kapu és a `test_export_bajtazonos` méri).

## 2. Licencszűrés (`adat/licencek.tsv` alapján)

- **Kizárva (25 dataset):** a nem kereskedelmi / feltételes: `MCGED` (© Mounce 1993), `KJV_teljes_szoveg` (kereskedelmi: feltételesen), `tW_szocikkek` (feltételesen); **tisztázatlan:** `Heber_ETCBC_modulok`, `KJV_ASV_Strongs`, `KJV_Strongs_teljes`, `LXX_kivonat`, `LXX_lexicon`, `Cremer_nyers`, `Girdlestone`, `lexikonok_nyers`, `simplemma_nyelvi_adat`; **a projekt zárt származtatott rétege („minden jog fenntartva”):** `BDB_forditas`, `Karoli_Strong_kivonat`, `Karoli_Strong_parok`, `Karoli_Strong_szavak`, `Karoli_versmegfeleltetes`, `LXX_versszintu_parok`, `karoli_modern`, `karoli_variancia`, `szoto_tablak`; **CC BY-SA, de a csomag nem használja:** `LSJ`, `SDBH_SDGNT_segedtablak`, `UBS_DBH`, `UBS_DNTG`.
- **Külön réteg (CC BY-SA 4.0, attribúcióval):** `SDBH`, `SDGNT` → `cc_by_sa_reteg/` (szó szerinti UBS-forrásmegjelölés, ShareAlike-jelölés).
- **A csomag saját adata:** `projekt_adat` (CC BY 4.0 — DT-F162a, helyőrzős döntés).
- A forrásmegjelölésben szereplő, engedett adatkészletek: `TAHOT`, `TAGNT`, `TSK`, `Karoli_1908`; 22 engedett, de a csomag értéket nem tartalmaz belőlük.
- **Mért:** az `elofordulasok.tsv` egyetlen sorának provenienciája sem nevezett kizárt forrást (0 sor); a jelöltek keresési módjában kizárt forrás nincs. A `kizarasok.tsv` 7 sora és a `dontesnaplo.tsv` 1 sora a „KJV” szót hordozza (versszámozási megjegyzés) (a TSK angol számozásáról; nem adat) — a kapu ezt FIGYELMEZTETÉSként jelzi.

## 3. A kapu eredménye

`python eszkozok/nyilt_mag_kapu.py`: **0 BUKÁS, 9 FIGYELMEZTETÉS** (8× a „KJV” szó versszámozási megjegyzésben; 1× ANGOL_SOR: egy korábbi minősítés idézett angol/görög vegyes sora). Ellenőrzések: BELSO (olvasói kapu mintái + `gerinc_elem`, `scope=`, belső könyvtárút, snake_case azonosító), ANGOL, KODKONYV (minden oszlop és zárt érték, két nyelv, nem azonos), LICENC, RETEG, HIBAK (a mért szám jelen van), HIVATKOZAS (NYD-feloldás, motívum-azonosító), BAJTAZONOS (újragenerálás és összeg).

`grep` a kimeneten a belső jelekre (`gerinc_elem`, `scope=`, DT/N/F-szám, `manual`, `study`, `gap`, `scan`): **0 találat**. Az `eszkozok/feladatok.py ellenoriz`: 183 brief, 0 hiba. `ellenoriz.py`: 0 SÉRTÉS (a 34. szabály nem került be: a kapu önálló eszköz; CI-be kötése külön tétel).

## 4. „Ismert hibák” (`nyilt_mag/ISMERT_HIBAK.md`)

1. **Károli-KH (N-F156a):** a `karoli_kh_epseg.py` mérése szerint (`naplok/KAROLI_KH_EPSEG_jelentes.md`, **a számok onnan olvasva**): 19 817 forrásvers, 32 407 KH-sor, 12 322 forrásvers listája szó szerint megegyezik egy másikéval, ebből **5 078 gyanús másolat** (7 971 KH-sor). A csomag a KH-tábla adatát nem tartalmazza; a kezelés és a határ (az egyedi hibát a szabály nem fogja meg) kimondva.
2. SDBH/SDGNT lefedés (~90%; a hiány nem negatív lelet), 3. a gépi Károli-szó párosítás (`szó-szintű-gépi`) modell-kimenet.

*Eltérés a mérésektől:* az `NYITOTT_FELADATOK.md` N-F156a sora még a régi 5 471 / 8 688 értéket idézi; a generált jelentés (és a csomag) a frissebb 5 078 / 7 971-et. A nyitott-tétel sorát nem írtam át (az nem az én fájlom); a csomag a mérésből számol.

## 5. Döntések (helyőrzős, `dontesek/uj/quirky-nobel-e12091.md`)

- **DT-F162a** 🟡 — a nyílt mag tartalma és licence: a brief leképezése + elhagyva a magyar szótári fordítás (`jelentes_hu`), a belső útvonalú oszlopok (`forras_tanulmany`, `felmerult_tanulmany`), a `fo_elofordulas`, a `nyitva` jelöltek; a csomag saját adata CC BY 4.0, noha a leltárban a `projekt_adat` „minden jog fenntartva”.
- **DT-F162b** 🟡 — a döntések feloldása `NYD-nnn` azonosítóval és egymondatos szöveggel.

## 6. Ismert korlátok / teendők

- A **„meghatározás”** mező a briefben szerepel, de az `adat/`-ban nincs önálló meghatározás-oszlop: a `cim` és a `folerendelt_fogalom` hordozza; nem töltöttem ki asszociatívan.
- A `dontesnaplo.tsv` szövegei gépi tisztítással (belső jelek cseréje/elhagyása) készültek; néhol nyelvtanilag nehézkesek („az adattábla negatív kritériuma”); a kérdés/döntés első mondatai nem a teljes döntést adják. Lektori átnézés javasolt a közzététel előtt.
- A `DT-F123d` hivatkozás a `jeloltek.tsv`-ben van, de a `DONTESEK.md`-ben nincs sora (csak a briefben) — a csomagban nem szerepel (nincs feloldható nyilvános szöveg).
- A CI-be kötés (a kapu mint E-szabály) nincs megtéve; a `Zenodo-feltöltés, DOI` a felhasználóé (nem része).

## 7. Adat- és termékréteg (DT-F162c, 2026-11-04) és kanonikus forrás

- **Ki:** `elofordulasok.tsv` `kapcsolodas`; a `funkcio` „ — ” utáni magyarázata; `kapcsolatok.tsv` és `motivum_kapcsolatok.tsv` `funkcio`/`indoklas`. **Bent:** a `funkcio` címke (emoji nélkül), a kizárások/beépítések indoklása, a `negativ_kriterium`, a típus/bizonyosság/PaRDeS-szint.
- **Hosszú, „ — ” nélküli `funkcio`-próza (kiesett, 3 sor):** TEREMT-002 1Móz 1:2 (118 karakter), Jer 4:23 (88), Ézs 34:11 (65).
- **Kapu:** új TERMEKRETEG ellenőrzés (a KI-mezők nincsenek a csomagban, a funkció rövid címke, a kódkönyv `(nem exportált mezők)` sorai kimondják mezőnként a réteget és az okot); új KANONIKUS ellenőrzés (nincs GitHub-hivatkozás; `<KANONIKUS_FORRAS_URL>` helyőrző; `KIADAS.txt`: adatállapot dátuma + tartalmi hash). 35 teszt zöld, 0 BUKÁS.

## 8. Újragenerálás a #630 után (2026-11-04)

- `kizarasok.tsv`: 418 sor (+5 ISTENTISZT-001 összesítő sor); új `csoport_versszam` oszlop (az „Összesítő sor N versre” szám), és új `kizaras_csoportok.tsv` (1402 tag: ALVIL-001 295, HAMART-001 651, ISTENTISZT-001 456), a darabszámok egyeznek a sorok versszámával. A kódkönyv és az `OLVASSEL.md` („Csoportos kizárás”) nevezi meg a csoportos kizárást; az `OLVASSEL.md` hivatkozik a mellé kerülő idézési metaadatra és az MI-nyilatkozatra (GitHub-URL nélkül).
- Ahol a gépi lista nem igazolja a számot vagy nincs lista, a tagok nem töltődnek ki (jelenleg ilyen sor nincs).
