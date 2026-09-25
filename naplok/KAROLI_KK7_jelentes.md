# KAROLI_KK7_jelentes.md — újramérés és jelentés ⛔

*KK7.4 — KAROLI_KULCS_KK7_BRIEF.md §3. Ág: `claude/karoli-kulcs-35158`,
a `main` (`72b200c`) beolvasztva (KK7.0).*

## Nem-regresszió (K1)

| | Érték |
|---|---|
| Korábban (`a6783e4`) kitöltött és **változatlan** | **460 808** |
| Megváltozott | **0** |
| Eltűnt | **0** |
| Újonnan kitöltött (a javítás után, a rejtett/üresre állt fejezetek nélkül) | 10 419 |

**K1: RENDBEN.**

## A KK7.1 tartalmi próba újrafuttatva az új állapoton

A javított importer kimenetén (a 27 vizsgált fejezetből most már csak a **19
elfogadott** fejezetben van újonnan kitöltött kulcs — a 8 elutasított
fejezet kulcsai üresek maradtak) a korrelációs próbát újrafuttatva:
**mind a 19 fejezet átmegy, mindegyiknél a `shift=0` (a mostani, javított
kimenet) adja a legjobb korrelációt, `elfogadott_eltolas=0`-val** — azaz a
javítás önkonzisztens: nincs több szükséges korrekció. (A próba-futtatás
csak ellenőrzésre szolgált, a `naplok/KAROLI_KK7_fejezet_dontes.tsv`
gyártási táblát nem írta felül — az importer a KK7.2-ben rögzített,
eredeti döntéstáblát használta a regeneráláshoz.)

**K2: RENDBEN** — minden megmaradt új kulcs olyan fejezetben van, amely
átment a próbán.

## A 0.6 négy példája (KK7.2-ben már igazolva, itt megerősítve az éles fájlon)

| LXX-vers | Éles kimenet most |
|---|---|
| Isaiah 63:1 | **Ézs 63:1** ✓ |
| Isaiah 63:12 | **Ézs 63:12** ✓ |
| Numbers 6:4 | **4Móz 6:4** ✓ |
| 1 Samuel 20:8 | **1Sám 20:8** ✓ |

**K3: RENDBEN** — mind a négy helyes (egyik sem hibás vagy üres, holott
lehetett volna).

## A próbakő: Ézs 63:13

A `TEREMT-001_TUDOMANYOS.md` LXX-blokkjában: `| Ézs 63:13 | Ézs 63:13 |
תְּהֹמ֑וֹת (te.ho.Mot) | ἀβύσσου (ἄβυσσος, abussos G0012) | **egyező** | LXX_OS |`

**K4: RENDBEN.**

## A lexikon "Egyezés"-bontása — KK6 után → KK7 után

| Kategória | KK6 után | KK7 után |
|---|---|---|
| egyező | 127 | **126** |
| kutatói azonosítás függőben | 89 | **87** |
| szamozas_elteres | 9 | **12** |
| eltérő | 3 | 3 |
| nincs LXX_OS-könyv | 5 | 5 |
| LXX-minusz | 1 | 1 |
| **Összesen** | 234 | 234 |

**A `szamozas_elteres` nőtt (9→12), az `egyező`/`függőben` csökkent** — ez
**szándékos és helyes** (G1, G4): a KK6 néhány "javult" besorolása (Jób
38:16, 38:30 — mindkettő "egyező" volt) a Jób 38. fejezet tartalmi próbáján
**megbukott** (a fejezetben más, újonnan kitöltött versek rossz eltolást
kaptak, ami az egész fejezetet üresre állította — l.
`naplok/KAROLI_KK7_fejezet_dontes.tsv`, `Jób 38: ures`), ezért Jób 38:16
és 38:30 most **`szamozas_elteres`**-re állt vissza. A Jón 2:3 és Jón 2:6
viszont a próbán átment, **változatlanul "egyező"** maradt. Ez pontosan
a G4 által előírt viselkedés: "ami nem megy át, az is G1 szerint üres
lesz" — a helyesnek *hitt*, de valójában bizonytalan javítás inkább
visszaáll üresre, mint hogy hibás maradjon bent.

## `general.py --cel lexikon --ellenoriz`

Mind a 8 érintett motívum-ID-re (`KIRALY-001, ISTENTISZT-001, TEREMT-001,
ALVIL-001, MENNY-001, ANTROP-001, HODIT-001, HAMART-001`) egyenként
lefuttatva: **0 eltérés** (mindegyik exit code 0). *(A `--cel lexikon
--ellenoriz` "mind" móddal nem futtatható a teljes motívum-készletre,
mert a `main`-ből örökölt `TEREMT-002` motívumnak hiányzik egy
`res_forras.tsv` sora — ez a KK7 hatókörén kívül eső, előzetesen ismert
hiányosság, l. brief "Nincs benne" szakasz: "a törzscikkek regenerálása…
a NYITOTT 5b tétele, a SZOTAR 2. menete hozza helyre".)*

**K5: RENDBEN** (a KK7 hatókörébe eső 8 motívumra).

## `eszkozok/ellenoriz.py`

RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 — megegyezik a `main`
állapotával (KK7.0 0.8).

**K6: RENDBEN.**

## A fejezetdöntések összesítője

| | Érték |
|---|---|
| Vizsgált fejezet (KK7.1) | 27 |
| Elfogadva (a döntéstábla szerint importált) | 19 |
| — ebből a jelenlegi eltolás már helyes volt | 7 |
| — ebből korrekció kellett (±1 vagy ±2) | 12 |
| Üresre állítva (G1) | 8 |

A döntéstábla (`naplok/KAROLI_KK7_fejezet_dontes.tsv`) egy **generált,
adatvezérelt fájl**, amit az `eszkozok/lxx_os_import.py` `load_fejezet_dontes()`
függvénye olvas be — nincs heurisztikus, könyv-specifikus új ág a
`resolve_karoli`-ban (G2).

**K7: RENDBEN.**

## K8 — diff-hatókör

```
git diff --stat origin/main..HEAD
```
csak a KK7 (és a korábbi KK0–KK6) hatókörébe eső fájlokat érinti:
`KAROLI_KULCS_BRIEF.md`, `KAROLI_KULCS_KK7_BRIEF.md`,
`eszkozok/lxx_os_import.py`, `konkordancia/Karoli_versmegfeleltetes.tsv`,
`konkordancia/LXX_OS/*`, `konkordancia/LXX_OS/README.md`,
`lexikon/*_TUDOMANYOS.md`, `naplok/KAROLI_KK*`.

**K8: RENDBEN.**

## Összesítő — K1–K8

| # | Állapot |
|---|---|
| K1 | RENDBEN |
| K2 | RENDBEN |
| K3 | RENDBEN |
| K4 | RENDBEN |
| K5 | RENDBEN |
| K6 | RENDBEN |
| K7 | RENDBEN |
| K8 | RENDBEN |

**Minden feltétel RENDBEN.**
