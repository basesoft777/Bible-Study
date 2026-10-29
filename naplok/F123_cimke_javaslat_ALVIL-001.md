# F123 — ALVIL-001: szakaszcímke-javaslat a szótári gerinchez (⛔, rögzítés előtt)

*Modell: claude-opus-5-5 · 2026-10-29 · DT-F123g (a) · a javaslat a végrehajtóé, a döntés a felhasználóé (D50; DT-F121a (d): a címke a szóról szól, a hely funkcióját az 1. szakasz „Funkció” oszlopa adja). Az `adat/szotar_szakasz_cimke.tsv`-be jóváhagyás előtt semmi nem került.*

## 1. Az alap: melyik szakasz idézi a motívum helyeit

A motívum lexikai (`motivumok.tsv`: H7585 / G0086 minden előfordulása), ezért **hordozó minden szakasz, amely ALVIL-001-helyet idéz**; a címke a szakasz magyar vezérszavaiból készül (`adat/bdb_szakasz_hu.tsv`, Thayer: `forditasok.tsv` `sz<n>`), motívumra utaló minősítés nélkül.

*Proveniencia: scope=H7585, G0086 × ALVIL-001 (72 sor) | forras=adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv (szurt≠1), adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/elofordulasok.tsv (split('\t')) | ts=2026-10-29*

### BDB H7585 (BDB8375; 11 szakaszsor, mind magyarul)

| Szakasz | A BDB magyarul (vezérszó) | ALVIL-001-hely a szakaszban | Javasolt `cimke_hu` | Hordozó? |
|---|---|---|---|---|
| `-/1/-` | „az alvilág … ahová az emberek halálukkor alászállnak” | **46** (1Móz 37:35, 42:38, 44:29, 44:31; 4Móz 16:30, 33; 5Móz 32:22; 1Sám 2:6; 2Sám 22:6; 1Kir 2:6, 9; Jób 7:9, 11:8, 17:12, 17:15, 21:13, 26:6; Zsolt 18:6, 55:16, 88:4, 89:49, 116:3, 139:8, 141:7; Péld 1:12, 5:5, 7:27, 15:24, 27:20, 30:16; Préd 9:12; Én 8:6; Ézs 5:14, 7:11, 14:9, 14:11, 14:15, 28:15, 28:18, 38:10; Ámós 9:2; Jón 2:3; Hab 2:5 …) | **alvilág, ahová a halottak alászállnak** | igen |
| `-/2/-` | „az igazak és a gonoszok állapota megkülönböztetve a Seólban” | 0 (fejszakasz) | **az igazak és a gonoszok állapota** | nem (vázlat) |
| `-/2/a` | „gonoszok … a halál a pásztoruk” | **13** (Zsolt 6:6, 9:18, 30:4, 31:18, 49:15, 86:13; Jób 24:19; Péld 23:14; Ézs 38:18; Ez 31:15, 31:17, 32:21, 32:27) | **a gonoszok sorsa a Seólban** | igen |
| `-/2/b` | „az igazat nem hagyják el … kiváltatik a Seólból” | **4** (Zsolt 16:10, 49:16; Jób 14:13, 17:12 — az utóbbi a BDB-ben „vö.”) | **az igazat nem hagyják a Seólban** | igen |
| `-/3/-` | „a helyek későbbi megkülönböztetése a Seólban” | 0 (fejszakasz) | **a helyek megkülönböztetése** | nem (vázlat) |
| `-/3/a` | „a Seól mélységei az érzékiek számára” | 1 (Péld 9:18) | **a Seól mélységei** | igen |
| `-/3/b` | „Seól és Abaddón … verem a Seólban” | 1 (Zsolt 88:4, a BDB-ben zárójeles utalás a šaḥat/bór szóra) + l. 2. pont | **Seól és Abaddón; verem** | igen |
| `-/4/-` | „átvitt értelemben a bűnben való végső lealacsonyodásról … Izráel száműzetésének helye” | **2 a szöveg szerint** (Ézs 57:9, Hós 13:14 ⭐) — a 2.29 tévesen a `-/3/b`-be sorolja, l. 2. pont | **átvitt értelem: lealacsonyodás, száműzetés** | igen |

### Thayer G0086 (4 szakaszsor, `sz1`–`sz4` magyarul)

| Szakasz | Thayer | ALVIL-001-hely | Javasolt `cimke_hu` | Hordozó? |
|---|---|---|---|---|
| `-/1/-` | „tulajdonnév: Hádész, Plútó, az alsó régiók istene” (klasszikus) | 0 | **Hádész, az alvilág istene (tulajdonnév)** | nem |
| `-/2/-` | „köznév: az alvilág, a halottak birodalma; a LXX a שְׁאוֹל szinte mindig így fordítja” | **12** (Luk 10:15, 16:23; Mt 11:23; ApCsel 2:27, 31; Jel 1:18, 6:8; + ÓSZ-utalások: 2Sám 22:6, Jób 11:8, Ézs 57:9, Ámós 9:2) | **az alvilág, a halottak birodalma** | igen |

A `lexikon_jelentes_szam` mindenütt üres, kivéve a 3. pont kutatói döntését.

## 2. A gerinces próbarender megáll — két adathiba és két kézi kérdés

Próbarender a kapcsoló ideiglenes bővítésével (`SZOTARI_GERINC_MOTIVUMOK += ALVIL-001`, a repón kívüli kimenetre; a fájl utána visszaállítva):

`lexikon_general.GerincHiba: H7585 Jób 17:12: a BDB-példák több útvonalra mutatnak (['-/1', '-/2/b']): kézi kérdés`

| # | Lelet | Hol | Javaslat | Kinek a fájlja |
|---|---|---|---|---|
| a | **Jób 17:12** (MT 17:13): a BDB két szakaszban idézi (`-/1` sorszam 55; `-/2/b` sorszam 88, „vö. Jób várakozását”) → GerincHiba | `bdb_vers_jelentes.tsv` | kutatói hozzárendelés: **`-/1/-`** (a `-/2/b` csak „vö.”-utalás); út: `elofordulasok.tsv` `jelentes_szam=1` + `lexikon_hivatkozasok.tsv` BDB H7585 `1` kulcs + a címke-sor `lexikon_jelentes_szam=1` | #123 (`ir`) |
| b | **Zsolt 88:4**: a BDB a `-/1`-ben (sorszam 30) és a `-/3/b`-ben (sorszam 93, a šaḥat/bór zárójeles megjegyzése) — a következő GerincHiba | ua. | kutatói hozzárendelés: **`-/1/-`** (ua. út) | #123 |
| c | **Ézs 57:9, Hós 13:14, Ézs 26:19**: a BDB `-/4/-` szakaszának példái (a szakaszszöveg szerint), a 2.29 a `-/3/b`-be sorolja (sorszam 94–96; a `-/4/-` illesztése `horgonnyal`, horgony „57:9”) — az Ézs 57:9 címkéje így hibás lenne, a Hós 13:14 (⭐) két tokenje miatt BDB-példa nélkül renderel | `bdb_vers_jelentes.tsv` (generált, a 2.29 kinyerője) | a kinyerő javítása (szakaszhatár a horgonyos szakasznál); **nem a #123 `ir`-je** | #102 / a 2.29 kinyerője |
| d | **„Prov 25:11”** a `-/3/b`-ben: a BDB sajtóhibája a Péld 15:11 helyett (a Péld 15:11 ALVIL-001-hely, a 25:11-ben nincs Seól) | `bdb_forras_javitas.tsv` (DT381 (a) mintája) | kézi javítósor | #102 |

Ezek nélkül a gerinc az ALVIL-001-en nem renderel (a) – (b), illetve hibás címkét ad (c). A (c) és a (d) javítása nem e feladat fájljain múlik: javaslat egy rövid javítófeladat a 2.29-re és a 2.31-re (vagy a #102 hatókörébe), és az ALVIL-001 lapja addig a (c)-t ⓘ-ben jelzi.

## 3. Eldöntendő a ⛔-nál

1. A 10 címke (1. pont) szövege.
2. A Jób 17:12 és a Zsolt 88:4 kutatói hozzárendelése (`-/1/-`), az ehhez szükséges `jelentes_szam=1` és `lexikon_hivatkozasok`-sor.
3. A 2.29/2.31 két adathibájának (c, d) útja: külön javítófeladat (javaslat), vagy a #123 `ir`-jének további bővítése.
