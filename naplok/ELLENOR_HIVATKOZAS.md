# ELLENŐR: F40 HIVATKOZAS_ELLENORZES — origin/main..claude/hivatkozas-ellenorzes

*A jelentést a `fuggetlen-ellenor` állította össze (fájlíró eszköze nincs, ezért az orkesztrátor mentette ide, tartalmilag változtatás nélkül). Merge-base `d31cb6d`, fej `20f5338` (F40.0–F40.2). A tesztfuttatás és a CI nem volt a kezében.*

## ELTÉRÉS: 6 tétel (súlyosság szerint)

1. **D8-leminősítés a generált blokkban (§2 A/B, H1).** `szabalyok.py:1600`: HIBA csak a PR által hozzáadott vagy módosított soron van, a többi JELENTES. A `FELADATOK.md` nyitott sorai a generált blokkban vannak (13–28., 32–44., 48–62. sor), amelyet PR nem szerkeszthet (E18/D25). Az A- és B-HIBA ezért a FELADATOK.md-ben gyakorlatilag soha nem jön elő; a H1 „a következő PR B-ellenőrzése elkapja” nem teljesül. Példa: `FELADATOK.md:20` `claude/f38-adag7` → `git log -1 origin/claude/f38-adag7`: `unknown revision`, csak JELENTES.
2. **⛔ átfedés (§4) nem volt jelezve.** `szabalyok.py:1662` D-ág „hibás brief-fejléc” részben megismétli az E18-at (`feladatok.py:128-177, 290-294`: fejléc lezárása, lista-érték, `forras` fájl). A brief itt megállást ír elő; a commitokban és a `naplok/F40_zaras.md`-ben nincs nyoma.
3. **H2:** a Kész szakaszban a hiányzó fájl a kódban mindig HIBA (`szabalyok.py:1633`, a `kesz` jelzőt csak a B-ág használja); a H2 szerint figyelmeztetés. Nincs rá teszt.
4. **Briefben nem szereplő kivételek (kicsi):** (1) könyvtár nélküli rövid név bármely azonos nevű repófájllal elfogadott; (2) kiterjesztés nélküli `a/b` kimarad, ha az első tag nem létezik; (3) `beerkezo/`, `konkordancia/` kizárva a D-ből. A zárónapló nem rögzíti.
5. **Tesztek (kicsi):** `test_szabalyok.py:748-750` a `_kilepes` saját magán számolja a kilépési kódot, a `futtat.py` valódi kilépési kódját nem teszteli; a „csak chatben” és a „hibás YAML” teszt kilépési kódot nem vizsgál.
6. **Állítás:** „15 teszt” — a diffben 16 `test_` metódus van az `E27Teszt`-ben.

## OK
C-szint (figyelmeztetés), `fetch-depth: 0` (a base-en is megvolt), B egy `ls-remote` hívással, D `ir` nem ellenőrzött, E (D és R sorok, HIBA), annotációk (`futtat.py`), CRLF-tűrés, `CLAUDE.md:189` mondata, H5 (E27, dokumentált), H6 (FELADATOK.md érintetlen), adat/konkordancia változatlan (Δ=0), a 33 JELENTES-tétel egyezik a zárónaplóval.

## NEM ELLENŐRIZHETŐ
- Tesztek zöldek (§6): a tesztfuttatás nem volt engedélyezett; a végrehajtó jelentése szerint 90 + 32 teszt OK.
- B-ellenőrzés és az Actions-token (§4 ⛔): ha a lekérdezés elbukik, a kód csendben figyelmeztetésre vált, a brief megállást kért volna. CI-futás nélkül nem igazolható.
- CI-jelentés nem érkezett.

## Megjegyzés a PR-hoz
Saját futtatás: a PR címe `F40: …` esetén az **E16 HIBA**-t ad (a PR az ellenőrzőt érinti, a cím nem „[ELLENŐRZŐ]” előtagú); `[ELLENŐRZŐ] …` címmel KILEPES=0 (E27 JELENTES 33).
