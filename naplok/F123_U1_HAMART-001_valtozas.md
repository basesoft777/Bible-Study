# F123 U1 — a HAMART-001 gépi lépéseinek változásmérése (a #592 X.A munkafájljaihoz képest)

*#123 MIGRACIO2 · U1 (`munka: adat`) · ág: `claude/hamart-u1-ff7c0c` · modell: claude-sonnet-5-5 · 2026-11-03*

**Eredmény: nincs változás.** A hét lépés determinisztikus része (1. gerinc-metszet, 3. teljes ÓSZ/ÚSZ scan, 4. kollokáció, 5. igealak, 6. LXX-híd) a mai adaton újrafutott, és az X.A (2026-11-02, `naplok/F123_adat_HAMART-001.md`) munkafájljaival kulcs-szinten azonos. **Gerinc-elemet érintő eltérés (Strong be/ki) nincs**, a #123 2c. ⛔-je nem nyílik.

## 1. Mit futtattam

`python naplok/F123_adat_keszito.py` alparancsai (a munkaszkript a #592-ből), a mai TAHOT/TAGNT/LXX_OS-en, a HAMART-001 mai `elofordulasok.tsv` (52 sor) és `jeloltek.tsv` (250 sor) állapotával. Az egyes alparancsok kimenetét az X.A committolt tábláival vetettem össze **kulcs-szinten** (a proveniencia-sorok időbélyege és az állapot-oszlop szövege kimarad), majd az újrafuttatott fájlokat visszaállítottam (`git checkout`), hogy a #592 táblái ne duplikálódjanak, és a közös `naplok/F123_lekerdezesek.tsv` ne ütközzön a #608-cal.

| Lépés | Alparancs | Kulcs-szintű összevetés az X.A táblával | Eredmény |
|---|---|---|---|
| 1. gerinc-metszet + 3. teljes scan (14 Strong) | `f108` | 1 676 → 1 703 kulcs; **csak régi: 0**; csak új: 27 | a 27 új kulcs száma megegyezik a #592 által írt 27 `nyitva` jelölttel (a kulcsok típusa `jeloltek:nyitva`; mintavétel: 1Kir 13:34, 1Kir 14:15-16, 1Kir 8:34-35, 1Kor 15:53, 1Kor 15:54), a scan-oldali sorok azonosak |
| 4. kollokáció | `kollok` (H4390+H2555, H8085+H2555, H6975+H1863) | 14 → 14 kulcs; csak régi 0; csak új 0 | azonos (8 / 4 / 2 hely) |
| 5. igealak / φθείρω-család | `csalad` | 51 → 51 kulcs; csak régi 0; csak új 0 | azonos (9 Strong) |
| 4. lánc-lexémák együttállása | `lanc` (ablak 1) | 41 → 41 kulcs; csak régi 0; csak új 0 | azonos (9 egy versben; 8 ±1 ablakban) |
| 6. LXX-híd (a 43 héber E-sor 62 verse) | `lxx_e` | 62 → 62 kulcs; csak régi 0; csak új 0 | azonos (31 vers kritérium-görögje az LXX-ben) |

A scan-találatok száma Strongonként (a mai futás): G1311 5, G1944 2, G2671 5, G5351 8, G5356 8, H0127 211, H0779 52, H2403 271, H2555 59, H6093 3, H6975 12, H7043 79, H7451 621, H7843 135 — az X.A számaival megegyezik; új tag nincs, E-ben nem szereplő gerinc-hely nincs azon túl, amit az X.A már dokumentált (mai scan új hely: 1 269 találat, `VALT scan uj_hely`; kulcs-eltérés 4, tartomány-hatás).

**A különbség egyetlen forrása:** a #592 óta a `jeloltek.tsv` 223 → 250 sor, ezért az X.A idején „UJ” állapotú helyek (a 27 jelölt) ma „jelölt (…: nyitva)” állapotúak. A scan maga nem változott.

## 2. A teljes mai scan és a teljesség-mérés viszonya

A teljesség-mérés Strong-hálója (`naplok/F123_teljesseg_HAMART-001.md`) a mai scannel azonos 1 403 találatot adja (63 E, 107 J, 1 233 ELTÉRÉS); a 1 233 ELTÉRÉS pontosan az F108 újrascan új helye. Az X.A 1 256 verséhez képest a különbséget (23) nem vizsgáltam.

## 3. Proveniencia

- Az alparancsok minden lekérdezésének proveniencia-sora (`scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=… | n=… | ts=2026-11-03T11:44Z | csatorna=cli` és társai) a futás kimenetében áll; a közös `naplok/F123_lekerdezesek.tsv`-be **nem** írtam (l. fent, ütközés a #608-cal); a teljes futási kimenet a session scratchpadjében van.
- `scope=HAMART-001: adat/elofordulasok.tsv (52 sor) + adat/jeloltek.tsv (250 sor) × naplok/F108_ujrascan_elteresek.tsv (1570 sor) | forras=split('\t'), ág claude/hamart-u1-ff7c0c | ts=2026-11-03`
