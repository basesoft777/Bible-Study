# ELLENOR_F91_2 — F91_ZSOLT_FELIRAT_SZAMOZAS_BRIEF.md · 25e39a1a..41dff637 (F91.0–F91.16, újrafuttatás)

*A független ellenőr (`claude-opus-5-5`, kért: `opus`, egyezik) jelentése, az orkesztrátor írta ki fájlba. Az első jelentés (`naplok/ELLENOR_F91.md`) változatlan. Az ellenőr parancsköre nem engedte a tesztek, a replay, a KK4-generátor és a `felirat_versek()` futtatását: ezek NEM ELLENŐRIZHETŐ-k, az orkesztrátor/végrehajtó futtatta őket (M2d, M2e).*

**Eredmény: ELTÉRÉS 3 tétel (mind dokumentációs), az első jelentés E1–E6 lezárult.**

| tétel | állapot |
|---|---|
| E1 (DT-F91d (a)): `_tabla_kjv()` a 67 felirat-versre a közös halmazból; a replay a módosított importert hívja; DT 8 cellás, 🟢, kimondja a fixpontot; `lxx_os_import.py` az `ir`-ben | OK (kód); a replay eredménye NEM ELLENŐRIZHETŐ az ellenőrnek |
| E2: közös halmaz, a builder és az f92 ebből szűr; pontosan a 67 vers; A-tábla 67 `felirat` sora = a halmaz | OK |
| E3: `ir` mező fedi a 26+1 fájlt | OK (a két ELLENOR-napló az `ir`-be került) |
| E4: DT-F91a–d 8 cellás, 🟢 | OK |
| E5: N-F91a/b (7 `Psa.Psa.151`, Zsolt 37 = 40 sor, 203 = 105+47+35+5+3+2+2+2+1+1, NAVE-0130 az N-F91b-ben) | OK |
| E6: M2a §1 jelölve | OK |
| ÚJ-a: `adat/SEMA.md:1154` 4907 → 4906 | ELTÉRÉS — **javítva** |
| ÚJ-b: M2e fejléc „nem módosult” + sorhivatkozás | ELTÉRÉS — **javítva** (elavultként jelölve) |
| ÚJ-c: pilot README „mind a 32 versén” → 31 nem felirat vers | ELTÉRÉS — **javítva** |
| KIRALY-001 / 1Móz 14:18-20 SÉRTÉS-sor | független az F91-től: a `teszt_sqlite_epit.py` negatív tesztjeinek várt kimenete (szándékosan üríti az első sor `gerinc_elem`-jét); a diff nem érinti |
| Pilot kód, Nave, LXX_OS adatfájlok | érintetlen (két egysoros README/leíró szövegcsere) |
| CI (E2–E16, E19, E20, E26) | 0 találat; E25 (3) és E27 (34) nem F91-es |
| DT-számok, commitok | csak helyőrzők; 17 commit `F91.n:` előtagú |
| TSV-sorszám Δ | 0 mindkét táblán, bontási napló nem kell |
