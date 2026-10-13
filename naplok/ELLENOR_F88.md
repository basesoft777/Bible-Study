# Független ellenőrzés — #88 TIPNR_NORMALIZALAS

*Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`, kért: `opus` — egyezik) nem rendelkezett fájlíró eszközzel; a jelentést az orkesztrátor mentette el, tartalma az ellenőr jelentésének összefoglalója.*

- brief: `F88_TIPNR_NORMALIZALAS_BRIEF.md`
- tartomány: `origin/main..claude/f88-tipnr-normalizalas` = `47f2b520..cbf41912` (6 commit, F88.0–F88.5)
- eredmény: **ELTÉRÉS: 2 tétel** (alább), a többi pont OK vagy nem ellenőrizhető (az ellenőr nem futtathatott tesztet és építést)

| pont | eredmény | indok |
|---|---|---|
| 0 modell | OK | a commitok és a brief `sonnet`-et mutatnak |
| G1 | OK | nincs `.tsv`-, `konkordancia/`-, `motivumok/`-, `lexikon/`-diff; `pardes.db` nincs a repóban |
| G2 | OK | `tipnr_strong_szetvalaszt()` (`eszkozok/sqlite_epit.py:58-74`), a `strong_util.py` diffje üres |
| G3 a–e | OK (kód); a futás nem ellenőrizhető | `eszkozok/teszt_sqlite_epit.py:253-278, 329-350` |
| G4 | OK; a NULL=0 nem ellenőrizhető | TSV-szám: 16 906 + 22 + 18 594 = 35 522, `+`-os érték 0 |
| G5 | OK | `lekerdez.py scan G6202` → `n=0`; a TIPNR-ben egy sor (`Millo Akra G6202G`) |
| G6 | nem ellenőrizhető | két építés hash-egyezése, „43 teszt zöld” |
| DT111 | OK | betöltő-szabály, `tilt` változatlan, SEMA 1.2, G6202 a jelentésben |
| M0 | a feltevés OK | az `olvaso_pilot` a TSV-t olvassa, nem a `pardes.db`-t, `N-F88a` nem kell |
| A1–A6, CI | OK | `futtat.py` exit=0; E25 és E27 találatai a diffen kívüli fájlokra vonatkoznak |
| Listák 1–5 | OK | TSV-sorszám Δ = 0; ⛔ pont nem teljesült; a többi tábla hash-változása a main más változásaiból ered (nem ellenőrizhető) |

## Eltérések

1. **Tartósság** — `naplok/SQLITE_EPIT_meres.md:175-193`: az F88 előtte/utána mérése kézzel áll egy generált fájlban, amelyet a következő `sqlite_epit.py --naplo` futás felülír (`open(path,'w')`, `eszkozok/sqlite_epit.py:1226-1227, 1284-1286`). A G4/G5 bizonyítéka elveszhet. Megoldás: külön napló (a repóbeli minta: `:1220`).
2. **Számegyezés** — `naplok/SQLITE_EPIT_meres.md:186, 190`: 35 433 / 35 522 sor illeszkedik (89 nem), ugyanitt „89 utótag nélküli és 1 G6202” nem illeszkedő sor: 89 + 1 = 90 ≠ 89. Az egyik számot a `pardes.db`-n újra kell mérni.

Megjegyzés (nem hiba): a jelentés `nyers` mezőjébe az alapszám (`G6202`) kerül, nem a nyers `G6202G`.
