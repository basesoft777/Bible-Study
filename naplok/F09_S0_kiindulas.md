# F09 S0 — kiindulás (SZOTAR S2)

*FELADATOK #9 · `F09_SZOTAR_S2_BRIEF.md` · ág: `claude/f09-szotar-s2` · indító commit: `ca4ec4d4` (a `main` = `911a3859` + a brief fejléc-commitja) · modell: `claude-sonnet-5-5` (Sonnet 5.5; egyezik a brief `modell: sonnet` mezőjével) · csak olvasás*

Mérőszkript: `naplok/F09_S0_meres.py`. Proveniencia (ha másképp nincs jelölve): `scope=adat/elofordulasok.tsv + konkordancia/ + lexikon/ | forras=naplok/F09_S0_meres.py (split('\t'), csv nélkül) | ts=2026-10-17`.

## 1. A 8 motívum Strong-tokenhalmaza (S0.2/1)

A tokeneket az `elofordulasok.tsv` `strong` oszlopából a `+` és a `;` mentén szétvágva; 8 motívum (ALVIL, ANTROP, HAMART, HODIT, ISTENTISZT, KIRALY, MENNY, TEREMT-001).

- **H: 24** — H0127, H0430, H0779, H1121, H2403, H2416, H2555, H3548, H3678, H4467, H5303, H5315, H6093, H6975, H7043, H7121, H7451, H7496, H7497, H7585, H7843, H8004, H8034, H8415
- **G: 13** — G0012, G0086, G0282, G0813, G1311, G1941, G1944, G2671, G4151, G5010, G5351, G5356, G5590
- A 9. motívum (TEREMT-002, nem a 8 része): H0922, H8414.

Az F05 §0 0.4 sorához (H 26, G 13, ebből 2 H a TEREMT-002-é, D29) képest: **H 24 + 2 = 26, G 13 — egyezik**. Token nem esett ki, új nem jött, a G-halmaz változatlan: a megállási feltétel nem teljesült. A hatókör: a fenti 24 H + 13 G token (K13d); a H8414/H0922 csak a kiejtés-sor kivétele (DT188).

## 2. Kiejtés-kivételek, KIEJT (S0.2/2)

- `adat/kiejtes_kivetelek.tsv`: **5 adatsor** (görög 3: epikaleō, kaleō, boaō; héber 2: qa.ra, shem), mind `KIEJT-migracio`.
- `grep -c KIEJT eszkozok/torzscikk_general.py` = **3** (a K9 célja: 0).

## 3. Szerepmátrix (S0.2/3)

`adat/szotar_szerepek.tsv`: 26 adatsor — `adatosítva` 11, `nincs adatosítva` 9 (görög 3, 7, 10; héber 3, 5, 7, 8, 9, 10), `javaslat` 6 (12–14. mindkét nyelven). Egyezik a brief tervezéskori állapotával.

## 4. Importok és SHA (S0.2/4)

| Tábla | Állapot | SHA-256 / megjegyzés |
|---|---|---|
| `TBESH_konszolidalt.tsv` | megvan, de **F42 óta** a `konkordancia/_nyers/tbesh/` alatt (gitignore-olt, helyben él) | tábla: `25c0a476…515b`; bemenet `TBESH.lexicon`: `5a8e306e…ce32` = a `TBESH_TBESG_README.md` értéke, **egyezik** |
| `UBS_DBH_jelentesek.tsv` | megvan | `39f6c279…4779`; a forrás JSON SHA-ja a fájl fejlécében és a README-ben azonos (`1686a25d…0e8e`); a JSON maga nincs a repóban (nem verziózott letöltés), így a bemenet újramérése nem volt lehetséges |
| `UBS_DBH_referenciak.tsv` | megvan | `6b052d09…7b40` |
| `UBS_DBH_anomaliak.tsv` | megvan | `182f9ffd…934b` |
| `MCGED_teljes.tsv` | megvan | tábla `952917e7…6b9f`; bemenet `MCGED.lexicon` `8d3b4e9c…71bb` = a README értéke, **egyezik** |
| `BDB_etimologia_kezi_hatarok.tsv` | megvan | `75c0cd8f…7fd`; a BDB-forrás `BDB_teljes_unabridged.tsv` `d4b15b2f…7794` = a README aktuális értéke, **egyezik** |
| `tW_szocikkek.tsv` | megvan | `6b760165…c66c0`; a tarball SHA-ja (`1d2b32da…15be`) csak a README-ben, a tarball nincs a repóban |
| `LXX_versszintu_parok.tsv` | megvan | `b602d288…7988` |

A tW és az LXX-pár elfogadása a `naplok/SZOTAR_S0b_jelentes.md` szerint: **tW elfogadva mindkét nyelven** (héber 21/26, görög 10/13; 4. szakasz), **LXX versszintű pár importálható** (5. szakasz, „versszintű együtt-előfordulás, nem szóillesztés” jelöléssel). A megállási feltétel (import hiányzik vagy a SHA eltér) nem teljesült. Megjegyzés: a README-k SHA-i a bemenetekre vonatkoznak; ahol a bemenet a repóban van, újramértem, ahol nincs (UBS JSON, tW tarball), a fájl-fejlécbeli/README-beli értéket vettem át, újramérés nélkül.

## 5. Görög kiejtés-egyezés (S0.2/5)

`python eszkozok/kiejtes.py --ellenoriz`: **26/26 pár egyezik pontosan (100%)** a `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` görög aranyrészén; a leave-one-out próba mind a 4 kivétel-jelöltre RENDBEN. Pontosítás: a brief/F05 D23 „50 pár” az aranykészlet nyers darabszáma; a gépileg tesztelhető tiszta rész 26 pár (a 30 egyedi pár közül 4 kontextusfüggő — `kiejtes.py` kimenete és F05 D32/`SZOTAR_S1_kiejtes_jelentes.md`). A kapu (100% a tesztelhető párokon) teljesül, az S2.1 indulhat.

## 6. N-F78a (S0.2/6)

Nyitott (`NYITOTT_FELADATOK.md`, „ÚJ (F78, 2026.10.08) — N-F78a”); a `torzscikk_general.py --kimenet` ma az éles `lexikon/`-ból olvas. Javítása az S2.8 előfeltétele.

## 7. Az éles `lexikon/` hash-e (S0.2/7)

16 fájl (8 `_TUDOMANYOS`, 8 `_TORZSCIKK`), SHA-256 a munkafán: `naplok/F09_S0_lexikon_hash.tsv`. A zárásnál ugyanezt kell visszakapni (K13b).

## 8. A javaslat-pont: UBS DBH anomáliák a tokenekre (S2.3)

A 24 H-token mindegyikének van UBS DBH jelentés-sora (1–3 szócikk-sor/token). A `UBS_DBH_anomaliak.tsv`-ből a tokenek főszócikkeire **5 sor** esik, mind `ervenytelen_kod` típusú (a forrás-JSON egy mellékkódja érvénytelen: `A1123` a H1121-nél, `A2402` a H2403-nál, `A2417` a H2416-nál, `A7123` a H7121-nél, `A7844` a H7843-nál). A tokenek Strong-hozzárendelését és a jelentés-szövegeket nem érintik (a `strong` oszlop minden tokennél kitöltött). **Döntés (a brief javaslata helyett):** nem állok meg rajta, mert a megállási feltételek (§0 ⛔) nem teljesültek, a render az anomália-táblát nem használja forrásként, és a hiba a szöveget nem érinti; a jelentésben jelzem.

## 9. Összegzés

Az S0 megállási feltételei **nem teljesültek**: a token- és G-halmaz egyezik, az importok megvannak és a SHA-k egyeznek, a görög egyezés 100%. Az S2.1 indulhat.
