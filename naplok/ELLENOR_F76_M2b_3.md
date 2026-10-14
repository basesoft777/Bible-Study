# Független ellenőrzés — #76 OLVASOI_KONKORDANCIA, M2b, 3. kör

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`, a kért `opus`-szal egyezik). Fájlíró eszköze nincs; a jelentést az orkesztrátor (Claude Sonnet 5.5) mentette az ellenőr szövege alapján, tömörítve. Tartomány: F76.29–F76.31 (`ab7860dd..200d154c`) az `origin/main...HEAD` diffben. Tesztet nem futtatott, a renderelt DOM-ot nem látta: ami ezen múlik, „nem ellenőrizve — eszköz-korlát”.*

**Eredmény: ELTÉRÉS, 9 tétel** (súlyossági sorrendben).

| # | Súly | Tétel | Hely |
|---|---|---|---|
| E1 | közepes (látens) | A szó-lap fejlécének magyar alapjelentése (`blokkok.alapjelentes`) a blokk-szintű kiadási/hozzáférési szűrést megkerüli. Ha egy szint vagy kiadás a BDB-t elveszi (a konfigban példaként szerepel `"szo.bdb_magyar" = "regisztralt"`), szivárgás vagy 500-as hiba lesz. A mai konfigban nem váltódik ki. | `oldalak.py:171`; `blokkok.py` |
| E2 | alacsony–közepes | Az N-F76d (1), N-F76f, N-F76g szövege elavult (a pótlás megtörtént). | `NYITOTT_FELADATOK.md:54` |
| 3d | alacsony | (az 1. kör 7. tétele, megmaradt) az összevetés 3d sora DT-F76e-t ír DT151 helyett. | `pilot_osszevetes.md:21` |
| E5 | alacsony | A teszt docstringje elavult (expectedFailure); a csempe-teszt csak részhalmazt néz; a g-teszt a pilotéval azonos függvényt hasonlít; a h/i teszt csak sztring-jelenlétet néz. | `teszt_pilot_aranymintaval.py` |
| E4 | alacsony | A „Kapcsolt szavak jelölése” kapcsoló az Interlineárisban hatástalan (`span.hu`, nem `.szo`). | `fejezet.html`; `olvaso.css:116` |
| E6 | alacsony | A pilot a törzsfejlécben a magyar törzsnevet is kiírja, a szerver nem. | `blokkok.py` `_torzsek_html` |
| E7 | alacsony | A `szo.bdb_apparatus` jellege angol szócikknél is `modell`-t tartalmaz. | `blokkok.py` regiszter |
| E8 | alacsony | Az ÚSZ-fejezetek görög szavai `lang="he" dir="rtl"`-t kapnak a csempén (az M2-ből örökölt minta). | `fejezet.html` |
| E3 | alacsony | A zárónapló „F76.29–F76.32”-t ír, de az utolsó commit az F76.31; az ETag-teszt docstringje F76.31-et ír F76.30 helyett. | `zaras.md`; teszt |

**OK:** DT148–i 🟢, a szöveg a felhasználói döntéssel egyezik; DT133 érintetlen, végleges szám nincs; a pilot kódja (`eszkozok/olvaso_pilot/`) változatlan; `bdb_szelet.py` importlib-bel, a `sys.path` érintetlen, csak `re`-t importál; XSS: minden kimenet `Markup % arg`/autoescape; Interlineáris csempe adata a `token_eredeti`-ból (`er_sorszam`), paraméterezett SQL, nincs `kjv`/`mcged` olvasás, a tükörfordítás a pilot csempéjével egyezik; ETag/`kod_verzio` helyes (rés: külső `PARDES_KONFIG_DIR` konfig nincs a hash-ben); `?ig=` szigorúan validált, paraméterezett SQL; CSP `unsafe-inline` nélkül, nincs inline script/stílus/`on*`; az 5 expectedFailure eltűnt; 1Móz 1 = 31 vers igazolva (`lekerdez.py karoli`); fejléc rendben (`megallt`, `pr`/`lezarva_osszegzes` üres); CI-szkript 0 HIBA; `adat/` és `konkordancia/` Δ = 0; ⛔ M5–M7 érintetlen.

**Nyitva, változatlanul (N-F76i):** ÚSZ-fejezet számlálók („0 héber”), az írásjel-teszt tűrése, két blokkcím, a szófaj-tartalék.

**Megjegyzés (DT152):** a DT-sor opciószövege a „süti csak váltáskor” megoldást említi (a nézet-sütire), a téma/aláhúzás tárolása localStorage; ezt az összevetési napló rögzíti, a DT „Alkalmazás” szövege nem.

**Nem ellenőrizve — eszköz-korlát:** a tesztfutások (22 + 65, végrehajtói állítás); a renderelt DOM (folyó szöveg, témaváltó, betöltési villanás); a Zsolt 22 vizuális egyezése; végrehajtói CI-jelentés (nem volt).
