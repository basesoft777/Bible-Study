# ELLENŐR — F65_KAROLI_ELLENORZES_BRIEF.md · `b622b928..abc03cff`

*Független ellenőr (`fuggetlen-ellenor`), 2026.10.11. A jelentés szövegét a fő szál mentette fájlba, mert az ellenőrnek nincs író eszköze. Base: `git merge-base origin/main HEAD` = b622b928; head: `claude/f65-karoli-ellenorzes` (F65.0–F65.5).*

## Összegzés: ELTÉRÉS 7 tétel

Az ellenőr az adatot a `parok_*.tsv`-ek, a `lekerdez.py` és a diff ellen igazolta. Rendben találta: a 23+23 sor (csak az `azonositas_modja` vált, `tartalom-alapú` → `szó-szintű-gépi`, nettó törlés 0), az egyezik+magas feltételt, a 11 frissített és az 5 `nincs_par` szúrópróbát, a 2Móz 15:5 és 19:6 valódi eltérését, a 153/3/49 és 15 teljes/8 részleges számokat, a 23 soronkénti proveniencia-sort, a `csv`-modul hiányát, az érintetlen `Karoli_Strong_kivonat.tsv`-t (383 `tartalom-alapú` sor marad), a helyőrzőket (nincs végleges DT/N szám az ágon), a ⛔ megállásokat, a CI saját futását (E2–E20, E26: 0 találat).

Nem ellenőrizhető az ellenőr eszközkörével: az `ellenoriz.py`, a teszt és a `--frissit` futtatása (a kód alapján az idempotencia rendben van).

## Eltérések súlyossági sorrendben

1. **Generált nézet és adat elcsúszott.** 23 sor `szó-szintű-gépi`-re vált, de a `lexikon/` 14 fájlja (8 motívum) még `tartalom-alapú`-t mutat (pl. `lexikon/ANTROP-001_TUDOMANYOS.md:68`); erről nincs nyitott tétel (az N-F65a csak a kivonatról szól). → nyitott tétel kell (N-F65b helyőrző); a lexikont nem szerkesztjük (kimenet réteg).
2. **E17/DT3.** Az új `adat/karoli_variancia.tsv` (+42 797 adatsor) mellé nincs darabszámos bontási napló (strong_szoalak 1Moz 12 040, szoalak_strong 1Moz 12 040, strong_szoalak 2Moz 9 347, szoalak_strong 2Moz 9 347, megerosites 23).
3. **Verzifikáció.** A Préd 9:10, Jób 17:13 és Jób 17:16 régi igehelye nem Károli-kulcs (a Károli-kulcs: Préd 9:12, Jób 17:12 és 17:15). Az M0, a zárónapló és az eltéréslista téves vagy hiányos okot ad; a Jób 17:13 `elter`-ítélete eltolásból ered, nem valódi szóeltérés.
4. A `karoli_variancia.tsv` `konyv` oszlopában két alak áll (`1Moz` az aggregátumban, `1Móz` a `megerosites` sorokban); a SEMA 2.24 egy értéket ír elő.
5. A `--ts` alapértéke be van égetve (`2026-10-11`, `karoli_ellenorzes.py:315`), újrafuttatáskor hamis ts kerülne a proveniencia-sorokba.
6. A 16 Strong nélküli TEREMT-002 `jeloltek`-sor hiányzik az eltéréslistáról (csak az M0 szövegében szerepel).
7. Az F65.0 commit-üzenete ékezetlen (`1b470a84`); az ág pusholva, nem írom át.

Kiegészítés (nem eltérés): a DT104 beleegyezésének időpontja a repóból nem igazolható (a válasz „chat”-ként szerepel a `DONTESEK.md`-ben).
