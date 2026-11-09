# HATAR_HODIT-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum HODIT-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=HODIT-001 | ts=2026-11-08T15:08Z | bemenet=adat/elofordulasok.tsv@dfb0de82a1,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** HODIT-001 — Rafeusok/óriás-népek · hordozó: `lexikai` · fölérendelt fogalom: „ókori óriás-népek/nagytermetű ellenfelek általában, a רְפָאִים (refáím) lexémán kívül” · beépített sor: 33 (33 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), HODIT-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (33 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | HODIT-001 versei | másik versei | közös | közös/HODIT-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 33 | 75 | 2 | 6% | 3% | nincs |
| ANTROP-001 | 33 | 11 | 0 | 0% | 0% | nincs |
| HAMART-001 | 33 | 56 | 0 | 0% | 0% | nincs |
| ISTENTISZT-001 | 33 | 22 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 33 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 33 | 11 | 1 | 3% | 9% | nincs |
| TEREMT-001 | 33 | 45 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 33 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

**a hordozó lexikai: a gépi negatív-kritérium próba nem fut.** A hordozó (`azonossag_tipusa`) = `lexikai` (`adat/motivumok.tsv:9`). A #150 szókapcsolat-próbája csak formulaikus hordozón dönt (`naplok/JELOLT_ELOSZURES_naplo.md`; a lexikai kiterjesztés az N-F150a). A negatív kritérium itt tartalmi, nem gépi: a modelles résznek (ha lesz) kérdése, nem ennek a szakasznak.

## Modelles rész

<!-- MODELLES-KEZDET -->
nem futott (DT-F151a után)
<!-- MODELLES-VEGE -->
