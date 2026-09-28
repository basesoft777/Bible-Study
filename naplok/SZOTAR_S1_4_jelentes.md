# SZOTAR_S1_4_jelentes.md — S1.4 (szótári importok) jelentése

*2026.09.28 · a `SZOTAR_BRIEF.md` v1.6 S1.4 tételének záró jelentése.*

## 0. Két tisztázó kérdés a felhasználótól

### (a) Melyik réteg használ „u"-t és melyik „ü"-t (ill. „y"-t) az upsilonra?

Ez a kérdés az S1.3 (`eszkozok/kiejtes.py`) D32-javítása után merült fel, és
az S1.4 importjai **egy második, önálló konvenció-eltérést is felszínre
hoztak** (D33):

| Réteg | Forrás | Upsilon-átirat | Igazolva |
|---|---|---|---|
| **Nyers forrás** — `TAGNT_kivonat.tsv` / `TBESG.txt` „Kiejtés" oszlopa | STEPBible.org | **`u`** (pl. `κύριος` → `kurios`) | Ez a lexikon_general.py `lemma_kiejtes()`/`ragozott_alak_kiejtese()` ma is változatlanul megjelenített forrása — ezt validálta az S1.3 gold-próba. |
| **Nyers forrás** — `konkordancia/MCGED_teljes.tsv` (S1.4, Mounce) `atirat` oszlopa | biblematedata/Mounce | **`y`** (pl. `κύριος` → `kyrios`) | Felfedezve az S1.4 MCGED-importja során (D33), **gold-párral még nem igazolva**. |
| **Kimenet** — `eszkozok/kiejtes.py` `atir()` | — | mindkettő → **`ü`** (`u`→`ü` ÉS `y`→`ü`, két külön szabály) | A `u`-ágat az S1.3 26/26 gold-párral igazolta; a `y`-ágat csak a szabály hozzáadása után futtatott önteszt (nem gold-pár). |

**Következmény:** a `kiejtes.py` jelenleg **mindkét** forrás-konvenciót
kezeli (nem kell előbb normalizálni), de a `κύριος → kyrios` típusú `y`-ágat
még nem erősítette meg egyetlen arany pár sem — ha a MCGED `atirat` mezője
valaha render-be kerül, ezt külön validálni kell (nem ennek a tételnek a
tárgya).

### (b) Melyik lépésben jön a héber kiejtés-jelölt és milyen ⛔ várható?

**Korrekció a kérdésedhez képest:** a Girdlestone **nincs** a jelenlegi
brief-ben — a `SZOTAR_BRIEF.md` D18 (2026.09.27) **kivezette** teljes
egészében (sem szövegként, sem hivatkozásként nem kerül a szótári
rétegbe); a héber 3. szerepben csak a TWOT-szám marad (S8, D19), ami a
BDB-etimológiától (S9) **független** tétel. Nincs „Girdlestone ⛔"
sehol a v1.6-ban.

Amit valójában a brief mond (§3, §7 1. menet prompt 4. pontja):

- **A héber kiejtés-jelöltek száma 26, nem 24** (D28: a T2.2 két új tokenje,
  `H8414`/`H0922`, bekerült a hatókörbe).
- A **26 héber kiejtés-jelölt** előállítása **S1.7** tétele (az S1.4–S1.6
  UTÁN, a §3 sorrend szerint) — a `naplok/SZOTAR_S1_heber_jeloltek.tsv`-be
  kerül, az OSHL `atiras` mezejéből.
- A **BDB-etimológia-határ kategorizálása** (a 26 tokenre, `H8414`/`H0922`
  besorolásával) **ennek a tételnek (S1.4) a része** — kész, l. 4. szakasz.
- A menet végi **egyetlen** ÁLLJ (a §3 „ÁLLJ — jóváhagyás" sora, az S1.7
  UTÁN) mutatja be **együtt**: a 26 héber kiejtés-jelöltet ÉS a kézi
  BDB-etimológia-határokat — **nem** két külön megállás, és nem Girdlestone.

## 1. Mit importált ez a tétel

| Fájl | Szkript | Sor | Dok. |
|---|---|---|---|
| `konkordancia/UBS_DBH_jelentesek.tsv` | `eszkozok/ubs_dbh_import.py` | 20 182 | `SDBH_SDGNT_README.md` |
| `konkordancia/UBS_DBH_referenciak.tsv` | ” | 389 212 | ” |
| `konkordancia/UBS_DBH_anomaliak.tsv` | ” | 1 109 | ” |
| `konkordancia/MCGED_teljes.tsv` | `eszkozok/mcged_import.py` | 5 303 | `lexikonok_nyers/README.md` |
| `konkordancia/TBESH_konszolidalt.tsv` | `eszkozok/tbesh_konszolidalt_import.py` | 9 688 | `TBESH_TBESG_README.md` |
| `konkordancia/BDB_etimologia_kezi_hatarok.tsv` | `eszkozok/bdb_etim_hatarok_import.py` | 26 | `BDB_teljes_unabridged_README.md` |
| `konkordancia/LXX_versszintu_parok.tsv` | `eszkozok/lxx_versszintu_import.py` | 99 356 | `README.md` |
| `konkordancia/tW_szocikkek.tsv` | `eszkozok/tw_import.py` | 598 | `tW_README.md` (új) |

Egyik tábla sincs még a generátorba bekötve — S2 (2. menet) tétele.

## 2. UBS DBH (héber) — `eszkozok/ubs_dbh_import.py`

Az `eszkozok/ubs_dntg_import.py` mintájára, ugyanarról a commitról
(`ubsicap/ubs-open-license@3a6edd821...`). Az OT könyvkód-tartományt
(`001`–`039`) a `Konyv_normalizalo_tabla.tsv` első 39 sorával kalibráltam
— **mind a 389 212 `LEXReferences`-hivatkozás sikeresen dekódolódott**, 0
tartományon-kívüli anomália, ami megerősíti a kalibrációt.

## 3. MCGED (Mounce) — `eszkozok/mcged_import.py`

SQLite → TSV, csak a `G####` Strong-kulcsú sorok (a `gkG5####` GK-kulcsúak
kihagyva, mert ugyanazt a szöveget ismétlik). Itt derült ki a fenti (a)
upsilon-eltérés.

## 4. TBESH konszolidáció — `eszkozok/tbesh_konszolidalt_import.py`

Unió, nem csere (S4): szócikkenként a hosszabb tisztított szöveg. A D28
hatókörű 26 tokenre a bontás **11 `txt` / 13 `lexicon` / 2 `egyenlő`** —
ez eltér a §0 0.5 sorban rögzített, kézi méréstől (9/13/2, a régi
24-tokenes hatókörön) — **nem hiba**, hanem egy új, teljes körű,
automatizált módszer eredménye (a régi mérés kis mintás, kézi becslés
volt).

## 5. BDB-etimológia-határ — `eszkozok/bdb_etim_hatarok_import.py`

A 26 tokenre: **15 `gepi`, 5 `javaslat` (⛔ jóváhagyásra vár), 6
`nem_targyalja`**. Az 5 `javaslat`: `H0430`, `H3678`, `H8004`, `H8034`
(D21, változatlan) + **`H0922` (*bohu*, új, D28/D29 miatt bővült)**.
`H8414` (*tohu*) váratlanul **gépi** kategóriába esett (van tiszta
em-dash+"1 " határjelző) — nem igényel jóváhagyást.

## 6. LXX versszintű párok — `eszkozok/lxx_versszintu_import.py`

A `naplok/SZOTAR_S0b_lxx_versszint_szkript.py` (csak H7121-re) általánosítva
mind a 26 tokenre. 99 356 sor, 729 TAHOT-igehely nem található a `LXX_OS`-ben
(kihagyva — ismert, a `LXX_OS` nem fedi a teljes ÓSZ-t).

## 7. unfoldingWord Translation Words — `eszkozok/tw_import.py`

Letöltve, feldolgozva: 598 szócikk (190 `kt` + 408 `other`). **Egy valódi
hiba két kör alatt, mindkettő javítva, mielőtt bármi élesedett volna:**
1. Az apostróf a valódi fájlokban Unicode `'` (U+2019), nem ASCII `'` — az
   első regex ASCII-t keresett, 0 Strong-kódot talált (598/598 hiba).
2. A görög Strong-kódok néha vezető nullával kezdődnek (`G00120` = a
   valódi `G0012` + záró változat-számjegy) — az első verzió a `0*` mintát
   a regexben a számjegyek ELÉ tette, ami levágta a vezető nullákat,
   mielőtt a hossz alapján dönthettem volna az 5-jegyű levágásról; ez
   `G0012`-t tévesen `G0120`-ra torzította.

A javítás utáni lefedettség (héber 21/26, görög 10/13, pontos hiányzó
lista) **bájtra egyezik** az S0b.2 mérésével (`naplok/SZOTAR_S0b_jelentes.md`)
— ez a kereszt-ellenőrzés adja a bizalmat, hogy a végleges import helyes.

## 8. Ellenőrzés

- `nulladiff.sh 8f5a1eb` a két D31 `--csere`-vel → exit 0, üres diff (egyik
  import sincs még a generátorba bekötve).
- E2–E16 a változott fájlokon: 0 találat (E9 2 JELENTÉS, korábbi tartalmú
  sorokon, nem kapcsolódik ehhez a tételhez).
- E1 (`ellenoriz.py`) továbbra is szándékosan piros a törölt
  `forditas_ubs.tsv`-re hivatkozó 10. szabály miatt — az S1.5 zárja.
