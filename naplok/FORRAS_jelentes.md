# FORRAS_jelentes.md — FJ5: összesítő jelentés

*FORRASJELOLTEK_BRIEF.md v1 alapján, 1. menet (felmérés, nem import). Ág:
`claude/peaceful-rubin-39uuzs`.*

## Forrásonkénti javaslat

| Forrás | Cél | Licenc | Mérés | Javaslat | Indok |
|---|---|---|---|---|---|
| **CenterBLC/MT-LXX** | 3a | **nincs** (nincs LICENSE/README a repóban) | A-halmaz 78,9% (123-ból 97), B 4/4 | **NEM** | A < 90% küszöb alatt; licenc hiánya önmagában is kizáró (D17) |
| **Macula Hebrew** (Clear-Bible) | 3a | **CC BY 4.0** (szó szerint idézve) | A-halmaz 78,3% (115-ből 90), B 4/4 | **NEM** a küszöbre, de **a két 3a-jelölt közül ez a jobb választás**, ha valaha puhább küszöbbel újramérik | A < 90%; a licenc rendben van, a CenterBLC-nek nincs — ha bármelyiket választanák, ez legyen az |
| **Versszámozás (15 sor)** | 3e | — | 13/15 valójában NEM versszámozási eltérés (a repó saját `LXX_OS`-kivonatolási hézaga), 2/15 valódi LXX-eltolás (Jón 2:3→2:4, 2:6→2:7), 1/15 valódi eltérés (Jer 51:46) | **import-jellegű javítás javasolt egy jövőbeli menetben**, nem forrásjelölt | a hézag oka az `eszkozok/lxx_os_import.py`, nem hiányzó forrás |
| **Teljes KJV/ASV** (studybible.info) | 3b | ismeretlen, nem idézhető (blokkolt domain) | nem mérhető | **NEM importálható ebben a menetben** | a domain a proxy-szabályzat szerint blokkolva; nincs git-klónozható alternatíva szó-szintű Strong-illesztéssel |
| **BSB** (`bsb-data-output`) | 3b (kiegészítő → ténylegesen elsődleges) | **CC0** (`base/display/`) | teljes 66 könyv, mintaellenőrzés (1Móz 1:1–5) tartalmi egyezést mutat a TAHOT-tal (a konvenciós 9000-es prefix-kódokon túl) | **IMPORT JAVASOLT** | egyetlen ténylegesen elérhető, teljes, jól licencelt 3b-jelölt |
| **theonize/bible_database** (Nave) | 3c | GPLv3 (repó), a Nave-tartalom eredete nincs külön nevesítve | 4 951 témakör, 92 610 topic↔vers reláció, kész, gépi feldolgozásra kész szerkezet | **FELTÉTELLEL** | jó szerkezet, de a licenc-lánc (Nave 1897 közkincs-státusza a saját repóból nem idézhető) tisztázatlan |
| **elcafe7/lex** (Nave) | 3c | dokumentálatlan (a saját `LICENSING.md` sem nevesíti) | 5 319 témakör, szabadszöveges `entry` mezőkben, parszolást igényel | **FELTÉTELLEL, gyengébb** | rosszabb licenc-dokumentáltság és rosszabb feldolgozhatóság, mint a theonize-jelölt |
| `basokant/nave` | 3c | — | — | **nem létezik** | nincs ilyen GitHub-repó |

## A 2. menet javasolt importlistája (döntésre vár)

1. **BSB `base/display/`** — CC0, teljes 66 könyv, szó-szintű Strong-illesztés.
   Egyértelműen importra kész, ha a döntéshozó elfogadja a KJV/ASV helyetti
   (nem csak kiegészítő) szerepét.
2. **A `LXX_OS`-kivonat javítása** (nem forrásimport, hanem a meglévő
   `eszkozok/lxx_os_import.py` hézagjának befoltozása) — ez oldaná meg a 13
   téves "szamozas_elteres" címkét, és önmagában közelebb vinné a lezárt
   lexikonoldalak "egyező" arányát.
3. **Nave** — csak akkor, ha a `theonize/bible_database` szerzőjétől vagy más
   forrástól sikerül a Nave-tartalom közkincs-státuszát szó szerint
   igazolni; addig nem javasolt.
4. **CenterBLC/MT-LXX és Macula Hebrew** — nem javasolt import (a küszöb alatt
   maradtak); ha a projekt mégis szeretné a szó-szintű MT-LXX-illesztést
   valamilyen alacsonyabb bizonyossági szinten használni (pl. csak a 87 függő
   hely kiinduló javaslataként, kézi megerősítéssel), a Macula Hebrew a
   választandó a kettő közül (licenc miatt).

## A 87 függő LXX-hely munkalapja

`naplok/FORRAS_FJ1_lxx_jeloltek.tsv`: 58 javasolt sor (kézi megerősítésre vár,
`LEXIKON_LEZARAS_BRIEF.md` 4c), 13 lefedetlen könyv (2Sám, 1Krón — a Macula
Hebrew jelenlegi állapotában nincs feldolgozva), 9 szó-szintű nem-találat, 5
LXX-minusz-gyanús, 2 hiányzó vers. **Ez munkalap, nem került az `adat/` alá**
(G4).

## G8 (NYITOTT 1. tétel)

A Macula Hebrew `<wg class="cl">` tagmondat-csoportjai funkcionálisan
lefedik a `morphology.sqlite` `ClauseID`-jának célját — javaslat: a Google
Drive-integráció technikai költsége elkerülhető. Részletek: `FORRAS_FJ1_mtlxx_macula.md` 5. pont.

## K1–K7 ellenőrzés

| # | Feltétel | Eredmény |
|---|---|---|
| K1 | `git diff --stat main..HEAD`: csak `FORRASJELOLTEK_BRIEF.md` és `naplok/FORRAS_*` | **RENDBEN** — 22 fájl, mind a két minta egyike (l. lent) |
| K2 | `eszkozok/ellenoriz.py`: SÉRTÉS 0 | **RENDBEN** — RENDBEN 9, SÉRTÉS 0, KÉZI 3, JELENTÉS 2 (változatlan a §0.7-hez képest) |
| K3 | minden letöltött forrásnál URL, commit/verzió, sha256, szó szerinti licencidézet | **RENDBEN** — CenterBLC/MT-LXX, Macula Hebrew, BSB-publishing/bsb-data-output, theonize/bible_database, elcafe7/lex mindegyikénél rögzítve (l. FJ1/FJ3/FJ4 jelentések); a studybible.info-nál a licenc **nem idézhető**, mert a domain blokkolva — ez a hézag a jelentésben explicit jelölve |
| K4 | az FJ1 és FJ3 arányai szkriptből számolva, a szkript megnevezve | **RENDBEN** — `FORRAS_FJ1_mtlxx_illesztes.py`, `FORRAS_FJ1_macula_illesztes.py`, `FORRAS_FJ3_bsb_tahot_minta.py`, mindegyik megnevezve a jelentés fejlécében |
| K5 | az FJ2-ben mind a 15 sor besorolva | **RENDBEN** — mind a 15 sor, `naplok/FORRAS_FJ2_szamozas.tsv` |
| K6 | nincs `csv` modul; a Strong-számok nullázva; héber/görög szöveg csak fájlba írt szkriptből | **RENDBEN** — minden szkript fájlba írva és onnan futtatva (`PYTHONIOENCODING=utf-8 python naplok/…`), sehol inline `bash -c`; a `csv` modul egyik szkriptben sem szerepel (`split('\t')`/`'\t'.join()`); a Strong-számok utólag nullázva (`FORRAS_K6_nullaz.py`, l. külön commit) |
| K7 | a jelentésben minden forrásnál javaslat és indok | **RENDBEN** — l. a fenti táblázat |

**K1 pontosítás:** a `git diff --stat main..HEAD` a `FORRASJELOLTEK_BRIEF.md`-t
és 21 `naplok/FORRAS_*` fájlt mutat (a `naplok/FORRAS_K6_nullaz.py`-t is
beleértve, ami maga is `FORRAS_*` nevű segédszkript) — az `adat/`, `lexikon/`,
`tematikus_lezart/`, `motivumok/` és a `konkordancia/` (a `_nyers/` gitignore-olt
kivételével) réteg **érintetlen**.

## Commitlista (ág: `claude/peaceful-rubin-39uuzs`)

1. `FJ: FORRASJELOLTEK_BRIEF.md v1`
2. `FJ0: hozzaferes es kiindulas ujramerese`
3. `FJ1: 3a MT-LXX-illesztes meres — CenterBLC és Macula Hebrew, ~78-79%, nem eri el a kuszobot`
4. `FJ2: 3e versszamozas — 13/15 a repo sajat LXX_OS hezaga, nem valodi elteres; Karoli-KJV versszam osszevetes`
5. `FJ3: 3b teljes KJV-ASV blokkolva (studybible.info proxy-tiltas); BSB CC0 teljes 66 konyv javasolva`
6. `FJ4: 3c Nave adatforras — basokant nem letezik, ket GitHub-jelolt feltetellel (licenc-tisztazatlan)`
7. `K6: Strong-szamok nullazasa a munkalapokban (SEMA 1.2, H/G + 4 szamjegy)`
8. `FJ5: osszesito jelentes` (ez a commit)
