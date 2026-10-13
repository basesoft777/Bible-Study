ELTÉRÉS: 7 tétel

# ELLENOR_F92 — F92_PARDES_DB_OLVASOI_BRIEF.md
Tartomány: `bfea33e6..21c7b875` (merge-base(origin/main, HEAD)..claude/f92-pardes-db-olvasoi)
Ellenőr modell: claude-opus-5-5 (kért: opus)
*A jelentést a `fuggetlen-ellenor` subagent állította össze; fájlíró eszköze nincs, ezért az orkesztrátor mentette el (a tartalom a subagent jelentése, tömörítve). Az ellenőr a pardes.db-t nem tudta lekérdezni, ezért több szám „NEM ELLENŐRIZHETŐ”.*

| pont | eredmény | indok |
|---|---|---|
| 0 Modell | OK | tényleges `claude-opus-5-5` = kért `opus`; a végrehajtó commitjai Sonnet 5.5 (brief: `sonnet`) |
| K1 (D1 39/39) | OK megjegyzéssel | 1Móz 1–25: 39/39; Zsolt 22: 38/39, a 39. blokk „részben”, mert a forrás (`lxx_dontesek`, `kapcsolatok`, `motivumok`) Zsolt 22-re 0 találat. A szó szerinti 39/39 a Zsolt 22-n nem teljesül — felhasználói elfogadás kell. |
| K2 (D2 0 eltérés) | NEM ELLENŐRIZHETŐ | ÚSZ-előfordulás 27/1230 és 11/305 görög lapon eltér; a TAGNT `+` láncelemeit a `token_strong` számolja, a TSV-út és a `lekerdez.py scan` nem (G4218: CLI 29, DB 54). Felhasználói elfogadás függőben. |
| K3 (D5 hash) | NEM ELLENŐRIZHETŐ | forrás-sorszámok egyeznek: Macula 475 911, LXX_OS 616 873, bdb_alias 460 |
| K4 | ELTÉRÉS | a tesztek nem futtathatók az ellenőrnek; a független ellenőr eltéréssel zár |
| K5 | OK (küszöb) | legnagyobb median 9,1 ms; az „előtte” (334 ms) nem a #76 1–3 s-a; index-használat a `test_f92_magyar_szo_index`-ben |
| DT-F92a (1) lxx_versszam | OK (kód) / döntés vár | 23 849 + 160 + 246 = 24 255 sor; az 1Móz 32:1-en a térkép téved (Gen.32:1 helyett Genesis 32:2); 4 889 közös versből 1 888 eltér |
| DT-F92a (2) nave_vers | OK | 85 246 = 75 856 + 9 390; fejezet 2 212, üres igehely 7 122, nem értelmezhető 13 forrásból igazolt |
| DT-F92a (3) bdb_alias licenc | OK | `BDB+projekt_adat`, a `licencek.tsv` változatlan |
| DT-F92a (4) db_meres | OK megjegyzéssel | a D4-táblázat-parse és a D5-bővítés is változott, dokumentált |
| DT-F92a (5) bovites.py | OK | változatlan, N-F92a nyitott |
| DT-F92a (6) Macula | NEM ELLENŐRIZHETŐ (számok) / OK (kód) | `strong_poz`/`strong_n`, meta-számláló megvan |
| ⛔ M0 megállás | OK | F92.1 megállás → F92.2 döntés → F92.3 építés |
| Nincs nagy bináris | OK | 11 szövegfájl; a `pardes*.db` a `.gitignore`-ban |
| `ir`-lista, helyőrzők | OK | |

## Eltérések súlyossági sorrendben
1. **ÚJ-1** — Dán, Bír, Józs: párhuzamos LXX-szövegformák (`daniel`/`daniel-theodotion`, `judges`/`judges-vaticanus-b`, `joshua`/`joshua-vaticanus-b`) ugyanarra a Károli-versre esnek; az `lxx_token`-nek nincs szövegforma-oszlopa, az olvasási út (`ORDER BY pozicio, rowid`) összefésüli őket; a SEMA 2.26 hallgat róla; az `lxx_versszam`-ban két LXX_OS-sor áll ezeken a verseken. A pilot csak 1Móz/Zsolt szakaszon mér, ezért a D2 nem fogja meg; a #76 kiolvasója örökölné.
2. **ÚJ-2 (A1)** — `PARDES_DB_OLVASOI_zaras.md:9`: „ellenőrizve… 5 420 G-Strongra 0 eltérés” commitolt lekérdezés nélkül (CLAUDE.md 1. szabály).
3. **ÚJ-3** — a megvalósított séma többlete (`kk_mod`, `allapot`, `strong_nyers`, `xml_id`-index; `kjv_vers`, `karoli_ok`, `strong_ok`; `forras_sor`; `megjegyzes`) és a +238,6 MiB a jóváhagyott kb. +209 MB helyett nincs naplózva.
4. **ÚJ-4** — a `LXX_versificacios_terkep.tsv` 39 `NEM_MEGHATAROZHATO` sora némán kiesik az `lxx_versszam`-ból (az M0 5 205 térkép-verse és a 4 889 + 137 közötti 179-es különbség sem igazolt teljesen).
5. **ÚJ-5** — tényhiba: az M0 „Macula_heber_*.tsv (50 fájl)” (valójában 39); a docstring „3 nem-könyv fájl” (valójában 2).
6. **ÚJ-6** — a `sqlite_epit.py:1133` megjegyzése önellentmondó (a BDB_strong_alias egyszerre betöltött és nem betöltött).

## Felhasználói döntés vár (nem ELTÉRÉS)
K2 ÚSZ-eltérés elfogadása; a térkép mint második forrás (1Móz 32:1 hibás); K1 Zsolt 22 „részben”.

---
# 2. kör (HEAD 430e06dd) — ELTÉRÉS: 5 tétel
*A fuggetlen-ellenor subagent jelentése tömörítve; az orkesztrátor mentette. Az ellenőr a pardes.db-t nem olvashatta (szerepkorlát).*
ÚJ-1, ÚJ-3, ÚJ-4, ÚJ-5, ÚJ-6 forrás- és diff-szinten OK; ÚJ-2 maradékkal. Új eltérések: (1) DONTESEK.md DT133/d sora 3 cellás a 8 oszlopos táblában; (2) a brief `kovetkezo` elavult; (3) SEMA 2.26 táblasora még a `versificacios_terkep` forrásértéket adta; (4) `f92_terkep_bontas.py` beégetett állítás-sora, egyirányú ÚSZ-ellenőrzés, elavult lekérdezés; (5) K4: tesztet az ellenőr nem futtathat.
NEM ELLENŐRIZHETŐ az ellenőrnek (DB-olvasás kellene): K3 meta-hash, Macula kétértelmű csoportok, lxx_versszam sorszámai, szovegforma, Nave 75 856/156 214, 5 420 G-Strong, térkép-bontás.
## Javítás (F92.9, `7698123b`)
(1)–(4) javítva; az `f92_terkep_bontas.py` helyett `eszkozok/f92_db_igazolas.py` (csak olvas, `mode=ro`), kimenete `naplok/PARDES_DB_OLVASOI_db_igazolas.md`: minden várt érték egyezik, eltérés nincs. *Ez a végrehajtó saját igazolása, nem független ellenőri lekérdezés.* Az orkesztrátor a javítás után lefuttatta: `teszt_sqlite_epit.py` OK, `teszt_olvaso_pilot.py` 105 OK, `feladatok.py ellenoriz` 0 hiba.
