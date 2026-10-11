# JELOLTEK_RETRO M0 — forrás-leképezés, hiánymérés, az írás módja

*F63 · 2026.10.11 · a mérés gépi (a naplók „Tartalmi minősítés” táblái, első cella, a `jeloltek.tsv` igehelyeivel szemben, tartományok kibontva); a számok **becslések**, a tételes lista az M1 első lépése. A mérőszkript a munkaág scratch-könyvtárában van, a repóba nem kerül.*

## 1. Forrás-leképezés (melyik motívum döntései hol élnek)

| motívum | tanulmány | kereszthivatkozás-napló | megjegyzés |
|---|---|---|---|
| ALVIL-001 | `Hadesz_Seol_tematikus.md` | `tematikus_lezart/naplok/Hadesz_Seol_…naplo.md` | táblázatos minősítés |
| HAMART-001 | `Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` | `…/Bun_kovetkezmenyeinek_gyuruzese_…naplo.md` (4/a, 4/b, 4/c) | a legnagyobb; csoportos kizárásokkal |
| HODIT-001 | `Rafaim_tematikus.md` | `…/Rafaim_…naplo.md` | a 12 TSK-`nyitva` már bent van |
| ISTENTISZT-001 | `Segitsegul_hivni_az_Urat_tematikus.md` | `…/Segitsegul_hivni_az_Urat_…naplo.md` | **próza**, nem tábla („NEM releváns” felsorolások) |
| KIRALY-001 | `Melkizedek_tematikus.md` | `…/Melkizedek_tematikus_…naplo.md` | táblázatos |
| MENNY-001 | `Isten_fiai_Nefilim_Gibborim_tematikus.md` | `…/Isten_fiai_Nefilim_Gibborim_…naplo.md` | a Mt 24:38 / Lk 17:27 `nyitva` már bent |
| TEREMT-001 | `Tehom_tematikus.md` | `…/Tehom_…naplo.md` | táblázatos |
| ANTROP-001 | `Pneuma_pszukhe_megkulonboztetes_tematikus.md` | **nincs** (SEMA 2.4.1: a négy hiányzó napló egyike) | a tanulmány és a `motivumok/ANTROP-001.md` **nem dokumentál elvetett jelöltet** |

## 2. Hiánymérés (a naplókban tételesen megnevezett, még nem jeloltek-beli igehely)

| motívum | jeloltek-sor | becsült hiány | ebből egyértelmű döntés | megjegyzés |
|---|---|---|---|---|
| ALVIL-001 | 72 | 2 | 2 `elutasítva` | 1Kor 15:55 (NA28: θάνατος), Mt 16:18 (más tárgykör) |
| ANTROP-001 | 9 | **0** | — | nincs forrás, ami elvetett jelöltet nevezne; a pótlás üres, ez **explicit** eredmény (3. szabály) |
| HAMART-001 | 52 | kb. 170–180 | kb. 170 `elutasítva`, 5 `nyitva` (Jób 16:18, 31:38; 5Móz 4:25, Bír 2:19, Sof 3:7: Hif'íl-csoport) | + 2Pét 3:10, 3:12 (l. 4. pont) |
| HODIT-001 | 50 | 1 | 1 `elutasítva` | 1Móz 6:4 (elhatárolás). A 4Móz 13:33 a naplóban javított hibás hivatkozás (→13:34, az már bent van): **nem sor** |
| ISTENTISZT-001 | 32 | kb. 35–40 | `elutasítva` („NEM releváns”, rokon igei használat), a pontos szám a prózai kiolvasástól függ | pl. Róm 10:11, Zsolt 105:15, 50:15, 91:15, Jer 29:12, Ézs 58:9, 65:24, Zsolt 86:5, 1Móz 25:21-26, 1Pét 2:11 stb. |
| KIRALY-001 | 9 | 7 + 1 | 7 `elutasítva` (1Móz 14:22-23 Copeland-hely, G5010: Luk 1:8, 1Kor 14:40, Kol 2:5; Jel 1:6, 5:10) | + 1Pét 2:9 (l. 4. pont) |
| MENNY-001 | 11 | 1 (+1 kérdéses) | 1Móz 14:5 `elutasítva`; az 1Móz 11:4 („shem”-alpont) nyitva jelzés: **motívum-javaslat**, nem igehely-jelölt | a 4Móz 13:33 itt is javított hivatkozás |
| TEREMT-001 | 41 | 2 | 2 `elutasítva` | 2Pét 2:4 (ταρταρόω), Jel 21:1 |
| **összesen** | | **kb. 220–235** | | |

**Csoportos kizárások, amelyeket a napló nem sorol fel igehelyenként** (HAMART 4/c): H2555 47, H7843 127, H0127 kb. 195, H2403 270, G0093 24 igehely (plusz a csoport-sorok kisebb része). Ezek a naplóból **nem** írhatók tételes sorrá (nincs lista); a scan újrafuttatásával lennének előállíthatók, de akkor a `forras_kereses` új lekérdezés lenne, a csoport-indoklás pedig a naplóból jön. Kb. 660 sor, nagyrészt zaj (gyakori Strongok, N13).

## 3. Az `auditok.tsv` — **a brief feltevése nem áll**

Az `adat/auditok.tsv` **csak a TEREMT-002 sorait tartalmazza** (A5/B2/B3/B4, 222 sor). A 8 régi motívumhoz **nincs** auditok-sor, tehát az „auditok scan − jeloltek” a brief szerinti alakban nem futtatható. Ezt a naplók „Vizsgált kulcsszavak” szakasza és az `elofordulasok.strong` oszlopa pótolhatja:

| motívum | scan-Strongok (az `elofordulasok.strong`-ból, nyelvtani Strongok nélkül) |
|---|---|
| ALVIL | H7585, G0086 |
| ANTROP | G4151, G5590 (+ H5315, H2416 az 1Móz 2:7 sorból) |
| HAMART | H2555, H7843, H0779, H0127, H6093, G1944, H7451 (+ gerinc: H2403) |
| HODIT | H7497, H7496, H5303 |
| ISTENTISZT | H7121+H8034 (kollokáció), G1941 |
| KIRALY | G5010, H3548, H8004 (+ G0813, G0282) |
| MENNY | H1121+H0430 (kollokáció), H5303 |
| TEREMT-001 | H8415, G0012 |

Ez **javaslat**: a `nem_vizsgalt.py` a scan-halmazt ebből a táblából (kódba írt, dokumentált leképezés) vagy új `auditok.tsv`-sorokból venné, a lekérdezést a `lekerdez.py` futtatná újra, a saját proveniencia-sorával. A gyakori Strongok (H0127, H1121+H0430, H7121+H8034) sok „még nem vizsgált” zajt adnának (N13).

## 4. Adatrétegbeli rendellenességek (nem az M1 hatóköre; jelzem)

- **KIRALY-001 · 1Pét 2:9**: a napló szerint `beépítve` (2026.09.09), de se a `jeloltek.tsv`-ben, se az `elofordulasok.tsv`-ben nincs. Ha a sor `beépítve`-vel kerülne a `jeloltek.tsv`-be, de az `elofordulasok.tsv` nem követi (tiltott: a 2. szabály), belső ellentmondás áll elő.
- **HAMART-001 · 2Pét 3:10, 3:12**: a napló „2Pét 3:6-7, 3:10, 3:12” sora `beépítve`, de csak a 2Pét 3:6-7 van a táblákban.

Javaslat: ezt a 3 sort `nyitva`-ként vennénk fel, `indoklas` = „a napló szerint beépítve, de az elofordulasok.tsv-ben nincs sor (nincs dokumentált döntés a hiányról)”, az elbírálás külön feladat.

## 5. Az írás módja

A `jelolt.py` itt nem használható: csak a `lekerdez`-metszetből (szakaszra) ír, kizárólag `nyitva` értékkel, a `beépítve`/`elutasítva` értéket **soha** nem. Javaslat: **egyszeri, összevetéssel ellenőrzött hozzáfűzés** (minta: `igazolas_migracio.py`): `split('\t')` / `'\t'.join()`, a `csv` modul nélkül; írás előtt a meglévő sorok bájtazonossága ellenőrizve, eltérésnél megállás; `--ir` nélkül szárazon fut. A tételes sorok a naplókból kiolvasott, motívumonként egy `naplok/JELOLTEK_RETRO_<ID>_sorok.tsv` munkalapra kerülnek (felülvizsgálható), onnan fűzi hozzá a szkript. A `forras_kereses`: `napló: <fájl> §<szakasz> | scope=manual | forras=<napló> | ts=2026-10-11`; a `datum` a pótlás napja; `azonositas_modja`/`megbizhatosag`/`karoli_szo` üres (nincs forrásadat).

## 6. Kérdések a ⛔-nál (DT-F63a)

1. Elfogadod-e a forrás-leképezést és a hiányszámokat (2. pont)?
2. **A csoportos kizárások** (kb. 660 igehely): (a) kimaradnak a pótlásból, és a `nem_vizsgalt.py` Strong-szintű, dokumentált kizárásként kezeli · (b) a scan újrafuttatásával sorokká bomlanak · javaslat: (a).
3. **A scan-halmaz forrása** (3. pont): kódba írt leképezés, vagy új `auditok.tsv`-sorok (az `ir` mezőbe fel kell venni)? Javaslat: kódba írt leképezés, mert az `auditok.tsv` az A5–B4 lépések kutatási nyoma, és most nem kutatás zajlik.
4. A 3 ellentmondásos sor (4. pont) `nyitva`-ként felvehető-e?
5. ANTROP-001: a pótlás **üres** (0 sor) marad, és a lelet-lap ★ sorai mellett a legtöbb „még nem vizsgált” lesz. Elfogadod?
6. Az írás módja (5. pont).
