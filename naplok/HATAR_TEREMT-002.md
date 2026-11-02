# HATAR_TEREMT-002.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum TEREMT-002`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=TEREMT-002 | ts=2026-11-02T12:49Z | bemenet=adat/elofordulasok.tsv@cadcb0987a,adat/motivumok.tsv@13dad030ab,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** TEREMT-002 — Tohu va-vohu (תֹהוּ וָבֹהוּ, tóhú vávóhú) — a föld kietlen és puszta állapota a teremtéskor és az ítéletkor · hordozó: `formulaikus` · fölérendelt fogalom: az isteni ítélet mint pusztulás / kozmikus felbomlás általában (prófétai pusztulás-, elsötétülés- és romhalmaz-képek), a תֹהוּ וָבֹהוּ (tohu va-vohu) páron kív… · beépített sor: 3 (3 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), TEREMT-002 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (3 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | TEREMT-002 versei | másik versei | közös | közös/TEREMT-002 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 3 | 73 | 0 | 0% | 0% | nincs |
| ANTROP-001 | 3 | 8 | 0 | 0% | 0% | nincs |
| HAMART-001 | 3 | 77 | 0 | 0% | 0% | nincs |
| HODIT-001 | 3 | 33 | 0 | 0% | 0% | nincs |
| ISTENTISZT-001 | 3 | 22 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 3 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 3 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 3 | 45 | 1 | 33% | 2% | nincs |

### 2. Negatív kritérium a beépített sorokon

Módszer: a #150 `jelolt_eloszures.vizsgal` próbája a **beépített** sorokra: a motívum gerinc-kombinációi (`elofordulasok.tsv` `strong`, nyelvtani Strongok nélkül) közül legalább egy teljesen megvan-e a sor versének Strong-halmazában (TAHOT+TAGNT). Hordozó: `formulaikus`.

Összesítés: 3 beépített sor; gerinc-kombináció megvan: 3; **kérdés (hiányzik): 0**; nem ellenőrizhető (nincs szövegadat / nincs kombináció): 0.

**0 kérdés.** Mind a 3 ellenőrizhető beépített sor versében megvan legalább egy gerinc-kombináció.

## Modelles rész

<!-- MODELLES-KEZDET -->
nem futott (DT-F151a után)
<!-- MODELLES-VEGE -->
