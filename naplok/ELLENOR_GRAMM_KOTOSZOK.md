# ELLENOR_GRAMM_KOTOSZOK

*Brief: `F68_GRAMM_KOTOSZOK_BRIEF.md` · tartomány: `origin/main..claude/gramm-kotoszok` (`06d54e3..e65b2b9`) · ellenőr: `fuggetlen-ellenor`, 2026-10-08. A jelentés az ellenőr kimenetének rövidített átirata; a javítások a `F68.4` commitban.*

## Eredmény: ELTÉRÉS 4 tétel (mind javítva)

| # | Eltérés | Javítás |
|---|---|---|
| 1 | Az M1 megismételt hatásmérésének számai proveniencia-sor nélkül álltak (`GRAMM_KOTOSZOK_zaras.md`) | a hat proveniencia-sor a zárónaplóba került |
| 2 | Az `N-F68a` (H2617-bukás) nem volt nyitott tétel | helyőrzős sor a `NYITOTT_FELADATOK.md`-ben (a számot a main-Action osztja) |
| 3 | A brief `ir` mezője nem fedte az írt fájlokat | az `ir` bővítve (`f4_0c_korut_ellenoriz.py`, `teszt_bdb_adatblokk.py`, `naplok/GRAMM_KOTOSZOK_*.md`) |
| 4 | A brief döntésnaplója szerint a DT-F68a „nyitva” | frissítve: eldöntve (🟢), az M1 kész |

## Igazolt pontok (OK)

- **Tábla:** `git diff origin/main..HEAD -- adat/`: +9/−2; 7 új adatsor (H0176, H0432, H3282, H3860, H3863, H3884, H6435), a többi a két `ts` sor; 85 → 92, Δ +7; minden más tábla Δ 0.
- **DT-F68a:** H3651 csak a `HATARESET`-ben, H6118 és a négy halasztott (H0638, H3861, H6903, H2958) a táblán 0 találat; a TILTOLISTA-blokk változatlan.
- **Szófaj-jel:** a hét felvett mind `kötőszó` a `Strong_szotar.tsv` szerint.
- **Jelöltkör:** 13 = 7 + 1 + 1 + 4; a szótári `kötőszó`-kör teljes.
- **Gerinc, 4 levezetés:** 40/23/3/54, marad 24/11/2/38, egyezik az M0-val.
- **F56 LXX (H3282):** levezetve G473 ×21, G3754 ×6, G1223 ×4, a G1894 a `LXX_MAX=3` miatt kiesik.
- **Negatív próba:** 0 találat az `elofordulasok.tsv`-ben és a `jeloltek.tsv`-ben; H6435: 3 említés a `genezis/1Moz_3v1-6_bovitett.md`-ben.
- **`f4_0c_korut_ellenoriz.py:48`:** a `:272` helyes, a generátorral egy commitban (`d0f531d`). A régi `:231` már a main-en is elcsúszott volt.
- **M0-napló HEAD-javítása (`6be514e`):** az egyetlen változás `046d081` → `8322fc5`.
- **⛔ M0 után:** az M1 a döntés (`77c7b94`) után jött.
- **`teszt_bdb_adatblokk.py` (`f7394d7`):** a H3282 kivétele indokolt, nem gyengíti lényegesen a tesztet.

## Nem ellenőrizhető az ellenőr szerepéből

Teszt-, `feladatok.py ellenoriz` és `ellenoriz.py` futtatás; a kilenc motívum 5829 párjának mérése; a H0176 és H6435 gyakorisága; a CI-jelentés egyezése. Saját `futtat.py`-futás: HIBA/SÉRTÉS nincs, E25 JELENTÉS 3 és E27 JELENTÉS 32 régi, nem ág-specifikus.

## Megjegyzés (nem eltérés)

A H3282 új viselkedését nem fedi pozitív teszt (a `test_nyelvtani_heber_marad` csak a H3588-at és a H0413-at nézi). Az ellenőrzés közben a munkakönyvtár HEAD-je átváltott a `main`-re; az ág érintetlen maradt (`e65b2b9`).
