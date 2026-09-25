# KAROLI_KK1b_kiindulas.md — a §0b újramérése

*KK1b-1 — KAROLI_KULCS_BRIEF.md v1.1 §3. Szkript:
`naplok/KAROLI_KK1b_kiindulas_general.py`.*

| # | Mérés | Brief-érték | Újramért érték | Egyezik? |
|---|---|---|---|---|
| 0b.1 | `KAROLI_KK1_fejezetosztaly.tsv` | 896 fejezet, 36 könyv (KJV 786 · MT 84 · KEZI 13 · EGYIK_SEM 13) | ugyanaz | igen |
| 0b.2 | Hiányzó könyvek | Ezsdrás, Nehémiás, Eszter — 33 fejezet; 929−896=33 | ugyanaz (`Ezsd`, `Neh`, `Eszt`) | igen |
| 0b.3 | KK3 alapja | 985 mért vers, 38 nem-Zsoltár könyv, a Zsoltárok nem mérve, arányosítás | l. KK1b-2/5 — a KK3-jelentés maga is kimondja ("csak aranyositas, nem kulon szamitas") | igen |
| 0b.4 | K4 a KK3-jelentésben | „RENDBEN, korláttal” | a `naplok/KAROLI_KK3_hatas.md` és a korábbi chat-jelentés így fogalmazott — a G11 szerint ez **nem elfogadható állapotjelölés**; a KK1b-4/5 pótolja RENDBEN/NEM TELJESÜL formában | igen |
| 0b.5 | `LXX_versificacios_terkep.tsv` | 5 426 sor, 35 könyv, oszlopok egyeznek | 5 426 sor, oszlopnevek egyeznek (a könyvszám külön nem volt mérve — a sorok könyv szerinti bontása a KK1b-3-ban kerül elő) | igen |
| 0b.6 | `Karoli_egyezik_hol` | Heber 1503 · EGYIK_SEM 1233 · Heber,Latin 1211 · Latin,Gorog 463 · Latin 361 · ELLENORZESRE_VAR 267 · Heber,Gorog 216 · Heber,Latin,Gorog 165 · egyéb | ugyanaz (a "Gorog" 7 sora az "egyéb" maradék) | igen |
| 0b.7 | A KK-menet (KK0–KK3) használta-e a térképet | nem (0 hivatkozás) | **megerősítve** — a KK0–KK3 `naplok/KAROLI_KK0_*`, `KAROLI_KK1_*`, `KAROLI_KK2_*`, `KAROLI_KK3_*` fájljaiban nincs `LXX_versificacios_terkep` hivatkozás (az egyetlen találat maga ez az új KK1b-1 szkript, ami a keresést végzi — nem számít bele) | igen |
| 0b.8 | Ellentmondás-minta | a térkép: Károli Jón 2:3 → Héber Jon.2:4, EGYIK_SEM; a tartalmi kontroll: Károli Jón 2:3 = MT 2:3 = LXX 2:3 | **megerősítve, sor szerint idézve**: `Jón 2:3 → Jon.2:4 / Jon.2:4 / Jon.2:4, Renumber, EGYIK_SEM` — a térkép sora **ellenőrizetlen** (`EGYIK_SEM`), a KK0 0.8 tartalmi ellenőrzése viszont közvetlen szövegegyezéssel bizonyított — a KK1b-3 ütköztetés ezt `UTKOZIK_ELLENORIZETLEN`-ként fogja kezelni | igen |
| 0b.9 | A térkép `Gorog_LXX_vers` oszlopának kiejtési oka | `LXX_OS/README.md` 2. szakasz: studybible.info saját oldal-számozására épül, nem esik egybe az lxx-morph `ref`-jeivel | megerősítve, a README 2. szakaszának szó szerinti szövege ("A térkép a studybible.info saját belső oldal-verzőszámozására épült... ezért a raw (fejezet,vers) kulcsai NEM esnek egybe az lxx-morph saját ref-jeivel") | igen |

**Következtetés:** a brief §0b minden száma megerősítve a `claude/karoli-kulcs-35158`
ágon. A KK1b-2…5 ez alapján halad.
