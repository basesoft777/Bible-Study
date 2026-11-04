# F123 U1 — a HAMART-001 teljesség-mérése három hálóval (DT548)

*#123 MIGRACIO2 · U1 (`munka: adat`) · takarékos menet · ág: `claude/hamart-u1-ff7c0c` · modell: claude-sonnet-5-5 · 2026-11-03*

*Döntés nélküli mérés. Eszköz: `eszkozok/teljesseg_meres.py` (az ALVIL-001-nél készült, motívumfüggetlen). Soronkénti kimenet: `naplok/F123_teljesseg_HAMART-001.tsv` (2 889 sor, minden sor mellett a háló proveniencia-sora). Blokkok: `naplok/F123_teljesseg_HAMART-001_blokkok.tsv` (`naplok/F123_HAMART2_u1_blokkok.py`). Jelölt-sorok: `naplok/F123_U1_HAMART-001_jelolt_sorok.tsv` (77 blokk-sor (83 blokk, a közös első versűek egy sorban): 74 `nyitva`, 3 `elutasítva` (N-F63e), még nincs beírva az `adat/jeloltek.tsv`-be: a #608 merge-e után).*

## 0. A mért állapot

- Strongok (az `elofordulasok.tsv` `strong` mezője, 14): **G1311, G1944, G2671, G5351, G5356, H0127, H0779, H2403, H2555, H6093, H6975, H7043, H7451, H7843**.
- Előfordulás-versek: 77 (52 sor). Jelölt-versek: 283 (250 sor).
- A Károli-háló szótári alakjai (`--karoli-szavak`): **átok, átkoz, átkozott, megátkoz, elátkoz, romlás, megront, elront, romol, megromol, erőszak, tövis** (12). Az `elofordulasok.tsv` `karoli_szo` mezője a HAMART-001 mind az 52 során üres, ezért a lista nem a mezőkből jön: az átok → erőszak → romlás lánc Károli-megfelelői (a gerinc-szavak: arar, chámász, sáchat, a H6975 tövis). **Ez mérési paraméter, nem kutatói döntés**: az U2 átvizsgálhatja. Szándékosan **nincs** benne a *föld* (adamá) és a *bűn* (chattát), mert olyan gyakoriak, hogy a háló elnyelné az eredményt; a *bűn* a fölérendelt fogalom (a hígulás iránya).

## 1. Összegzés

| Háló | Találat (vers) | E | J | ELTÉRÉS | ebből a versben áll a motívum szava |
|---|---|---|---|---|---|
| 1. Strong (TAHOT + TAGNT) | 1 403 | 63 | 107 (80 elutasítva, 27 nyitva) | **1 233** | 1 233 (nincs: 0) |
| 2. Károli-szó | 412 | 43 | 64 (59 elutasítva, 5 nyitva) | **305** | 67 (nincs: 238) |
| 3. Szótár (BDB, Thayer) | 1 074 | 49 | 92 (66 elutasítva, 26 nyitva) | **933** | 891 (nincs: 42) |
| fordított irány: E-vers, amelyet egyik háló sem ad | | | | **12** | |

A 12 fordított-irányú E-vers: 2Pét 3:6, Hós 4:1-3, Mk 7:21-23, Mt 15:19, Róm 8:20, Róm 8:22, Zsid 6:7, Ézs 24:5. Ezek mind a **`tematikus:`-sorok** (a negatív kritérium „tematikus, nem lexikai” esete, a CLAUDE.md szerinti 5 mért hamis kizárás) vagy tartomány-hatás (Róm 8:20-22, Zsid 6:7-8: a Strong a tartomány másik versében áll); a lexikai hálók definíció szerint nem láthatják őket.

**Eredmény.**
1. **Strong-háló.** A 77 E-vers közül 63-at lát a háló; a 14 hiányzó vers közül 11 `tematikus:`-sor (Ézs 24:5-6, Hós 4:1-3, Mt 15:19, Mk 7:21-23, 2Pét 3:6-7), 3 tartomány-hatás (Róm 8:20, 8:22 G5356; Zsid 6:7 G2671: a Strong a tartomány másik versében áll; l. `F123_adat_HAMART-001.md` 1. szakasz, `KULCS_ELTERES`). A **1 233 ELTÉRÉS vers mind pontosan az F108 újrascan új helye** (`naplok/F123_adat_HAMART-001_f108_osszevetes.tsv`, `ujrascan` sorok): 0 olyan Strong-találat, amelyet az F108 ne látott volna. Közülük **651 vers az N-F63e-függő** (H7451, H7043, magányos H6975: a kritérium listáján kívüli Strong; `naplok/F123_adat_HAMART-001_nf63e_fuggo.tsv`, mind a 651 bent van a 1 233-ban), a többi 582 a kritérium lexémalistáján belüli Strongot hordoz (H2403, H0127, H7843, H2555), szűretlen, kézi átnézésre (DT-F123u). Az X.A 1 256 verse és a mai 1 233 különbségét (23) nem vizsgáltam.
2. **Károli-háló.** 305 ELTÉRÉS: 67 vers hordoz gerinc-Strongot (azok a Strong-háló blokkjaiban is megvannak), **238 nem** — ezek a Károli-szó más héber/görög szó fordításaként állnak (a gépi osztályozás: `naplok/F123_teljesseg_HAMART-001_blokkok.tsv`, `halo=karoli`).
3. **Szótár-háló.** 933 ELTÉRÉS: 891 gerinc-Strongot hordoz (a Strong-háló blokkjaiban), **42 nem**: a BDB/Thayer a megadott Strongnál idézi a verset, de a versben a motívum Strongja nem áll (versszámozás-eltolás vagy más lexéma).
4. **Az E-sorok teljessége:** egyik háló sem ad olyan versre találatot, amely az `elofordulasok.tsv`-ben ellentmond; az E-oldali hiány kizárólag a lexikailag nem megfogható `tematikus:`-sorokban van.

## 2. Blokkok és jelölt-sorok

Az eltérések lexémánként blokkba rendezve (DT-F123o minta: egy blokk-sor, az első vers az `igehely`, a teljes vers-lista a `…_blokkok.tsv`-ben):

| Háló | Blokk-sor | Fedett vers (blokkonként többszörös számlálással) | Megjegyzés |
|---|---|---|---|
| Strong (a kritérium listáján belüli lexémák) | 4 (H2403, H0127, H7843, H2555), `nyitva` | 582 vers (blokkonként többszörös számlálással 582) | szűretlen, kézi átnézésre (DT-F123u) |
| Strong, N-F63e-függő | 3 (H7451 573, H7043 71, magányos H6975 7 vers), **`elutasítva`** | 651 | a felhasználó döntése (N-F63e, 2026-11-03: „kivesszük”), blokk-kizárás, indoklás: nem a negatív kritérium lexémája |
| Károli (gerinc nélkül) | 68 (osztály × lexéma) | 257 (238 vers) | négy osztály: átok, romlás, erőszak, tövis; az osztályozás a TAHOT/TAGNT-glosszák mintaillesztése |
| Szótár (gerinc nélkül) | 8 (H7451, H2555, H0127, H7043, H2403, H7843, G1944, G5356) | 42 | kulcseltolás-gyanús, kézi ellenőrzésre |

Minden blokk-sor (a 3 N-F63e-sor kivételével, amely `elutasítva`) `nyitva`, `jelolt_tipus=elofordulas`, a háló nevével a `forras_kereses`-ben és az indoklásban (2. szabály). Döntés az U2-ben. A Károli-blokkok nagy részében a motívum Strongja nem áll a versben, tehát a negatív kritérium (lexikai) szerint a blokk kizárás-jelölt; ezt **az U2 mondja ki**, nem a mérés.

## 3. Proveniencia

- `scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | strong=G1311+G1944+G2671+G5351+G5356+H0127+H0779+H2403+H2555+H6093+H6975+H7043+H7451+H7843 | n=1403 | ts=2026-11-03T11:43Z`
- `scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv | szotari_alak=elront+elátkoz+erőszak+megromol+megront+megátkoz+romlás+romol+tövis+átkoz+átkozott+átok | n=412 | ts=2026-11-03T11:43Z`
- `scope=G1311+G1944+G2671+G5351+G5356+H0127+H0779+H2403+H2555+H6093+H6975+H7043+H7451+H7843 | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) | n=1074 | ts=2026-11-03T11:43Z`
- A blokkok: `scope=naplok/F123_teljesseg_HAMART-001.tsv ELTÉRÉS-sorai × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (glossza) | forras=split('\t') | ts=2026-11-03`
