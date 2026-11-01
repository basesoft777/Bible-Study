ELTÉRÉS: 6 tétel

# ELLENOR_F153 — F153_THAYER_KAROLI_TELJES_BRIEF.md — `9ad99898..b417fa0b`

*Független ellenőr (`fuggetlen-ellenor`, tényleges modell `claude-opus-5-5`; a kért `opus`). A jelentés a subagent szövegének rögzítése (a subagentnek nem volt fájlíró eszköze); a rendelkezésre álló bizonyítékok: `git`, `futtat.py`, Grep. A merge-base `9ad99898`.*

## OK (összefoglalva)
- A `adat/forditasok.tsv`, a `forditas.py` (a `:219` helyőrzővel) és az `adat/` + `konkordancia/` diffje üres; a 7 `elavult` Thayer-sor érintetlen.
- A mérés 78 sort fed le (kezi 5, opus 2, sonnet 71), mindkét mankóval; 15 Strong; az 1 megerősítés (G4151 sz4, `Ján 3:8` szél) valós.
- Hatókör: a hét módosult fájl a brief `ir` listáján van (kivétel `DONTESEK.md`, brief). ⛔ M0 megállás betartva. E-ellenőrzések a diff fájljain: 0 találat.
- A napló M2-indoklása adatból igazolható (a „segítségül” az sz6/sz7 sorokban van). `DT-F132i → DT333` helyes (`DONTESEK.md:411`).

## ELTÉRÉSEK (súlyossági sorrendben)
1. **`DONTESEK.md:504` (DT-F153a) cellái elcsúsztak.** A Kérdés cellában a proveniencia ` | ` jelei miatt az F153.1 szkript az Opciók cellába írta az „✅ alkalmazva”-t, a Javaslat cellába a döntés szövegét; az Állapot 🟡, a Döntés „—” maradt. Az eredeti (a)/(b)/(c) opciók és a javaslat elvesztek; a „b” hatóköre emiatt nem követhető vissza (az (b) opció az F153.0-ban tágabb volt: „G1941 sz1, sz3, sz4 és az `egyezik` nélküli sorok”).
2. **A „hívj→segí” uralkodóváltás holtverseny-melléktermék.** A teljes mankón `segí` = `hívj` = `neve` = 9; `karoli_ujraellenoriz.py:77-82` a `Counter.most_common(1)` beszúrási sorrendjére (fájlsorrend) támaszkodik. A 8 `uralkodo_valt` sor és a DT-F153a premisszája ezért nem valós váltást mutat. A `forditasok.tsv` ettől nem sérült. A `test_uralkodo_to_szinten` holtversenyt nem vizsgál.
3. **„A tesztek zöldek” nem teljesül**: 36/37; a `Sigla.test_tabla_determinisztikus_es_kezi_vedett` bukik (a `main`-en is; N-F153a helyőrző felvéve a `NYITOTT_FELADATOK.md`-ben a javítókörrel együtt).
4. **A mérés kategóriái átfedik egymást** (1+53+17+8 = 79): a G1941 sz2 a 17-ben és a 8-ban is szerepel; a „4 sor” a címsort (sz1, `nincs_ellenorzendo`) is számolja.
5. **A brief `kovetkezo` mezője** elavult, a `kezi` lista (G1941 `teljes`) nincs benne.
6. **`teszt_lanc.py:362`** megjegyzése még `DT-F132i (2)`, az assert már `DT333 (2)`.

## NEM ELLENŐRIZHETŐ
- Az M2 futás (prompt, vázlat, kapukimenet) nyoma a repóban nincs; a „b” válasz pontos kérdésszövege az orkesztrátor chatjében van.
