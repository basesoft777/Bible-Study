# KAROLI_KK2_jelentes.md — kulcstábla-tervezet

*KK2 — KAROLI_KULCS_BRIEF.md §3, G3 oszlopaival. Szkript:
`naplok/KAROLI_KK2_kulcstabla_general.py`. Kimenet:
`naplok/KAROLI_KK2_kulcstabla_tervezet.tsv` (22 087 sor, **tervezet**, nem
élesített — a KK4 dönt a végleges `konkordancia/Karoli_versmegfeleltetes.tsv`
helyéről és formájáról).*

## Összegzés osztályonként

| Osztály | Generált sor | Logika |
|---|---|---|
| KJV | 20 074 | `igehely_karoli` = `igehely_kjv` (azonos fejezet:vers), `forras=szamlalas` |
| MT | 1 713 | `igehely_karoli` = `igehely_mt` (azonos fejezet:vers), `igehely_kjv` a `verse_pairs.jsonl`-ből, ha van; `forras=tvtms` vagy `szamlalas` |
| KEZI | 300 | a meglévő `KEZI_ELTOLASOK`-függvény kimenete (`forras=kezi`), a `None`-t adó versekre **identitás** (`forras=kezi_identitas_javitas`) — ez a G4 javítás a tervezetben |
| EGYIK_SEM (kihagyva) | 263 vers | nincs sor — a G5 szerint bizonytalan marad, nem találunk ki megfeleltetést |
| **Összesen** | **22 087** | a 39 ószövetségi könyv **22 350** Károli-verséből (22 087 + 263 kihagyott) |

## §1 érvényességi próbák eredménye

| Próba | Eredmény |
|---|---|
| minden érintett Károli-vers legfeljebb egy sorban | **9 kivétel** (22 087-ből, 0,04%): `Préd 9:19, 9:20, 12:15, 12:16, 2:26` és `Jób 39:31, 39:32, 39:33`, `4Móz 13:34` — mindegyik **dokumentált, valódi sok-az-egyhez összevonás** a `KEZI_ELTOLASOK` forrás-docstringjeiben (pl. a Prédikátor 2:25+2:26 nyers két verse a Károli egyetlen 2:26-jává olvad össze — l. `predikator_eltolas` docstring). **Ez nem hiba, hanem a forrásfüggvények dokumentált korlátja** — a KK4-nek kell eldöntenie, melyik nyers-forrás legyen az elsődleges sor (vagy mindkettő megmaradjon jegyzettel). |
| fejezeten belül monoton | igen (a KJV/MT osztály identitás-alapú, a KEZI a forrás saját, ellenőrzött sorrendjét követi) |
| MT-oldal létezik a TAHOT-ban | igen, definíció szerint (az MT-osztály maga a TAHOT-max-egyezésből jön) |
| KJV-oldal létezik a `verse_pairs.jsonl` `mt_refs`-ében | a KJV-osztálynál definíció szerint igen; az MT-osztálynál **1 713-ból** ahol nincs fordított TVTMS-találat, a `igehely_kjv` **üresen marad** (`forras=szamlalas`) — ez jelzi, hogy csak a raw-számlálás alapján állítjuk, TVTMS-megerősítés nélkül |
| minden sor forrása megnevezve | igen (`tvtms` / `kezi` / `kezi_identitas_javitas` / `szamlalas`) |

**A `kezi_identitas_javitas` forráscímke maga is jelzés:** ez a G4 (1)
javításának tervezett hatása — jelenleg a `resolve_karoli` ezeket a
sorokat (pl. Jób 38:1–38) hibásan a fejezet-őrre engedi tovább, és
`szamozas_elteres`-ként veszíti el (H1, l. KK1).
