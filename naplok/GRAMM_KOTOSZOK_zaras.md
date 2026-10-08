# GRAMM_KOTOSZOK — záró napló (F68, M0–M1)

*FELADATOK #68 · ág: `claude/gramm-kotoszok` · 2026-10-08 · a menet-zárás és az ellenőrzés (`fuggetlen-ellenor`) még hátravan.*

- **Felvétel (DT67):** H3282, H0176, H3863, H3884, H6435, H0432, H3860 `kotoszo`-ként (`d0f531d`); a tábla 85 → 92 adatsor, a generátorból újragenerálva.
- **Soronkénti összevetés:** 7 új sor, 0 törölt, 0 módosult; csak a két `ts` fejlécsor tér el. **HATARESET:** H3651 (dokumentálva, nem aktív). **Elutasítva:** H6118. **Halasztva:** H0638, H3861, H6903, H2958 (nem érintve).
- **Szófaj-jel:** mind a hét `kötőszó` a Strong_szotar szerint, kivétel nincs; a TILTOLISTA-őr lefutott, nem sérült.
- **Hatásmérés (valódi tábla, a `lekerdez.py gerinc` négy hívása):** metszet 40/23/3/54, marad 24/11/2/38 — az M0-val azonos, változatlan. Kilenc motívum teljes metszete és 5829 szakaszpár: marad-átlag 1,1053 → 1,1053, érintett pár 0 (az M0 1,10-es értéke a H3651-et is tartalmazó forgatókönyv volt; az nem került fel).
- **F56 LXX-nézet (H3282):** G473 ἀντί ×21, G3754 ὅτι ×6, G1223 διά ×4 (a G1894 ἐπειδή ×3 a `LXX_MAX=3` miatt kiesik); változik még H0176, H3863, H3884, H6435; a H3651 és a H6118 nézete nem (nem vették fel).
- **Teszt:** `teszt_bdb_adatblokk.py` 35 teszt, 1 bukás = az ismert alapállapot (`test_pelda_idezet_szo_szerinti`, H2617), új bukás nincs. A `test_nincs_nyelvtani_a_listan` a H3282-t nem nyelvtani mintaként használta; a felvétel miatt kikerült a mintalistából (`f7394d7`, külön commit, visszavonható).
- **Generátor-sorszám:** `f4_0c_korut_ellenoriz.py`: `:231` → `:272` (a `with open(KIMENET…)` sora), a generátorral egy commitban. A `naplok/F4_0c_korut_ellenoriz.tsv` régi kimenet, nem érintve.
- **M0-napló 7. szakasz:** HEAD-hivatkozás `046d081` → `8322fc5` (`6be514e`).
- **Ellenőrzők:** `feladatok.py ellenoriz` 0 hiba; `ellenoriz.py` SÉRTÉS 0 (KÉZI 2, JELENTÉS 3, korábbi állapot); `teszt_lekerdez_sir.py`, `teszt_ellenoriz_13.py` zöld.
- **Nyitott (nem e feladat):** az `olvaso_pilot` a felvett Strongoknak nem ad szó-lapot (a H6435-nél a felhasználó tudomásul vette; a H3282-re ugyanez áll). A görög oldal tükrözése (G473, G1894, G3379) külön döntés. `N54`: a H2617-bukás javítása.

**Proveniencia (az M1 hatásmérése, 2026-10-08):**

- `scope=range:1Móz 3+1Móz 6:1-8 | forras=TAHOT_kivonat.tsv | n=24 | ts=2026-10-08T06:22Z`
- `scope=range:1Móz 3+1Móz 4+1Móz 6:1-8+1Móz 6:9-22 | forras=TAHOT_kivonat.tsv | n=11 | ts=2026-10-08T06:22Z`
- `scope=range:1Móz 1:2+Jer 4:23+Ézs 34:11 | forras=TAHOT_kivonat.tsv | n=2 | ts=2026-10-08T06:22Z`
- `scope=range:Sir 2+Ézs 34 | forras=TAHOT_kivonat.tsv | n=38 | ts=2026-10-08T06:22Z`
- `scope=range:elofordulasok.igehely | forras=TAHOT_kivonat.tsv + TAGNT_kivonat.tsv + adat/elofordulasok.tsv + adat/grammatikai_strongok.tsv | n=9 motivum, 5829 par | ts=2026-10-08T06:23Z`
- `scope=H3282 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv + adat/grammatikai_strongok.tsv | ts=2026-10-08T06:23Z`
