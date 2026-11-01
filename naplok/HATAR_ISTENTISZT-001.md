# HATAR_ISTENTISZT-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum ISTENTISZT-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=ISTENTISZT-001 | ts=2026-10-29T15:36Z | bemenet=adat/elofordulasok.tsv@5c626f5332,adat/motivumok.tsv@857a6e31c8,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** ISTENTISZT-001 — Segítségül hívni az Úr nevét · hordozó: `formulaikus` · fölérendelt fogalom: istentisztelet/imádság általában (bármely invokációs forma, a קָרָא בְשֵׁם (kárá besém) formulán kívül) · beépített sor: 33 (33 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), ISTENTISZT-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (33 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | ISTENTISZT-001 versei | másik versei | közös | közös/ISTENTISZT-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 33 | 73 | 0 | 0% | 0% | 3, 4 |
| ANTROP-001 | 33 | 8 | 0 | 0% | 0% | nincs |
| HAMART-001 | 33 | 77 | 0 | 0% | 0% | 5 |
| HODIT-001 | 33 | 33 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 33 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 33 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 33 | 45 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 33 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

Módszer: a #150 `jelolt_eloszures.vizsgal` próbája a **beépített** sorokra: a motívum gerinc-kombinációi (`elofordulasok.tsv` `strong`, nyelvtani Strongok nélkül) közül legalább egy teljesen megvan-e a sor versének Strong-halmazában (TAHOT+TAGNT). Hordozó: `formulaikus`.

Összesítés: 33 beépített sor; gerinc-kombináció megvan: 33; **kérdés (hiányzik): 0**; nem ellenőrizhető (nincs szövegadat / nincs kombináció): 0.

**0 kérdés.** Mind a 33 ellenőrizhető beépített sor versében megvan legalább egy gerinc-kombináció.

## Modelles rész

<!-- MODELLES-KEZDET -->
nem futott (DT-F151a után)
<!-- MODELLES-VEGE -->
