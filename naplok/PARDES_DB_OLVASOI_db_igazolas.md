# PARDES_DB_OLVASOI (#92) -- a pardes.db csak-olvasó igazolása

*Proveniencia: `scope=a #92 F92-es táblái, a zaras.md számai + K3 | forras=pardes.db (mode=ro) meta.epites_ts=2026-10-13T10:59:43Z meta.mod=teljes + a konkordancia/ forrás-TSV-k; eszkozok/f92_db_igazolas.py | ts=2026-10-13T11:17Z`*

## 1. K3 -- a meta-hash és a forrás-TSV állapota

építés: `2026-10-13T10:59:43Z`, mód `teljes`

| tábla | sor | meta-sor | meta-hash egyezik a tábla tartalmával | forrás-TSV: nem commitolt módosítás / commit az építés után |
|---|---:|---:|---|---|
| `token_macula` | 475911 | 475911 | igen | nincs |
| `lxx_token` | 616873 | 616873 | igen | nincs |
| `lxx_versszam` | 24232 | 24232 | igen | nincs |
| `bdb_alias` | 460 | 460 | igen | nincs |
| `nave_vers` | 156214 | 156214 | igen | nincs |
| `token_karoli` | 981147 | 981147 | igen | nincs |
| `token_par` | 492380 | 492380 | igen | nincs |

- Macula forrás-sor (TSV most) = meta token_macula:forras_sor: számított **475911**, várt (zaras.md) 475911 -- egyezik
- LXX_OS forrás-sor (TSV most) = meta lxx_token:forras_sor: számított **616873**, várt (zaras.md) 616873 -- egyezik
- Nave forrás-sor (TSV most) = meta nave_vers:nave_basokant_sor: számított **85246**, várt (zaras.md) 85246 -- egyezik
- bdb_alias sor = BDB_strong_alias.tsv sor: számított **460**, várt (zaras.md) 460 -- egyezik

## 2. Macula kétértelmű (vers, Strong) csoportok

- kétértelmű (vers, Strong) csoport a táblából: számított **30541**, várt (zaras.md) 30541 -- egyezik
- meta token_macula:ketertelmu_vers_strong_csoport: számított **30541**, várt (zaras.md) 30541 -- egyezik
- ebben a csoportokban a Macula-tokenek száma: 67682 (meta: 67682)
- összevont `A;B` Károli-kulcsú vers / sor: számított **7 / 132**, várt (zaras.md) 7 / 132 -- egyezik
- 1Móz 1–25: kétértelmű kötés tokenre / összes TAHOT-token (vers): számított **1256 / 14142 (116 vers)**, várt (zaras.md) 1256 / 14142 (116 vers) -- egyezik
- Zsolt 22: kétértelmű kötés tokenre / összes TAHOT-token (vers): számított **31 / 389 (6 vers)**, várt (zaras.md) 31 / 389 (6 vers) -- egyezik

## 3. lxx_versszam

- forrás-értékek halmaza: számított **['LXX_OS', 'nincs']**, várt (zaras.md) ['LXX_OS', 'nincs'] -- egyezik
- sor forras=LXX_OS: számított **23849**, várt (zaras.md) 23849 -- egyezik
- sor forras=nincs: számított **383**, várt (zaras.md) 383 -- egyezik
- összes sor: számított **24232**, várt (zaras.md) 24232 -- egyezik
- ÓSZ-vers (TAHOT héber token, Károli-vers): számított **23204**, várt (zaras.md) 23204 -- egyezik
- ÓSZ-vers, amelyhez nincs lxx_versszam-sor: számított **0**, várt (zaras.md) 0 -- egyezik
- lxx_versszam-sor nem ÓSZ-versre: számított **0**, várt (zaras.md) 0 -- egyezik
- forras=nincs sor nem üres lxx_igehely-vel: számított **0**, várt (zaras.md) 0 -- egyezik
- forras=nincs, de a terkep_ertek nem üres (vers): számított **137**, várt (zaras.md) 137 -- egyezik
- forras=nincs vers (terkep_ertek nélkül): számított **246**, várt (zaras.md) 246 -- egyezik

## 4. Párhuzamos LXX-szövegformák (Dán, Bír, Józs)

| könyv | Károli-vers, amelyen ≥2 szövegforma áll | lxx_token sor formánként | lxx_versszam (LXX_OS) sor formánként |
|---|---:|---|---|
| Dán | 308 | {'daniel': 8210, 'daniel-theodotion': 9357} | {'daniel': 308, 'daniel-theodotion': 357} |
| Bír | 617 | {'judges': 15947, 'judges-vaticanus-b': 15580} | {'judges': 618, 'judges-vaticanus-b': 617} |
| Józs | 95 | {'joshua': 1034, 'joshua-vaticanus-b': 14439} | {'joshua': 95, 'joshua-vaticanus-b': 643} |

- lxx_token / lxx_versszam(LXX_OS) sor üres szövegformával: számított **0**, várt (zaras.md) 0 -- egyezik

## 5. Nave

- nave_vers sor: számított **156214**, várt (zaras.md) 156214 -- egyezik
- nave_vers különböző forrás-sor (bontott): számított **75856**, várt (zaras.md) 75856 -- egyezik
- Nave-sor a TSV-ben: számított **85246**, várt (zaras.md) 85246 -- egyezik
- kihagyott: igehely nélküli (TSV-ből számolva): számított **7122**, várt (zaras.md) 7122 -- egyezik
- kihagyott: fejezet-szintű (TSV-ből számolva): számított **2212**, várt (zaras.md) 2212 -- egyezik
- kihagyott: nem értelmezhető hely (TSV-ből számolva): számított **13**, várt (zaras.md) 13 -- egyezik
- kihagyott: nincs Károli-vers a tartományban (a maradék): számított **43**, várt (zaras.md) 43 -- egyezik
- kihagyott összesen = 2212 + 7122 + 13 + 43: számított **9390**, várt (zaras.md) 9390 -- egyezik
- meta nave_vers:kihagyott_osszes: számított **9390**, várt (zaras.md) 9390 -- egyezik
- bontott + kihagyott = Nave-sor: számított **85246**, várt (zaras.md) 85246 -- egyezik
- nave_vers sor igehely nélkül/üres nave_hellyel: számított **0**, várt (zaras.md) 0 -- egyezik

## 6. A versifikációs térkép bontása (nem forrás, DT-F92b)

- NEM_MEGHATAROZHATO sor: számított **39**, várt (zaras.md) 39 -- egyezik
- valódi Károli-kulcs a térképben: számított **5204**, várt (zaras.md) 5204 -- egyezik
-   ebből ÓSZ-vers az lxx_versszam-ban: számított **5026**, várt (zaras.md) 5026 -- egyezik
-   ebből LXX_OS-sal is: számított **4889**, várt (zaras.md) 4889 -- egyezik
-   ebből csak térkép (forras=nincs, terkep_ertek): számított **137**, várt (zaras.md) 137 -- egyezik
-   ebből nem Károli-vers: számított **178**, várt (zaras.md) 178 -- egyezik
-   ebből Károli-vers, de nem ÓSZ-vers az lxx_versszam-ban: számított **0**, várt (zaras.md) 0 -- egyezik

## 7. Görög ÚSZ-előfordulás (kétirányú: TAGNT ↔ token_strong)

- G-Strong a token_strong-ban: számított **5420**, várt (zaras.md) 5420 -- egyezik
- G-Strong a TAGNT-ban (egész mező ∪ láncelem): 5420
- a TAGNT-ban van, a DB-ből hiányzik: 0 []
- a DB-ben van, a TAGNT-ban nincs: 0 []
- mindkettőben van, de a darabszám eltér: 0 []
- a DB-szám eltér az egész-mezős (pilot TSV-út / lekerdez.py scan) számtól: 37 G-Strongon (ezek a láncelemet is hordozó Strongok)
- példa G4218: egész mező 29, láncelem 25, DB 54

## Összegzés

Minden számított érték egyezik a várttal.
