# ELLENOR_F21P_4.md — F21_KAROLI_STRONG_PILOT_BRIEF.md · 4. kör (a 3. kör javításai) · `4e95af4..f6ca73b` (0988560, 420f4ca, f6ca73b)

*A `fuggetlen-ellenor` 4. körös jelentése; a fájlba az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze). Ítélet: **hiba és figyelmeztetés nélkül** — megjegyzés: 2 (az 1. az ellenőrzés után javítva: `naplok/F21_zaras.md` „a–j” → „a–k”). A 3. kör mind a hat megállapítása javítva, egyetlen régi szám sem veszett el. A mérőszkriptek újrafuttatása a szerepkorlát miatt nem volt ellenőrizhető; az új keresztellenőrző és mentett-ellenőrző sorokat kódolvasással és kézi számolással ellenőrizte.*

| pont | eredmény | indok |
|---|---|---|
| 1a F4V2 első próba: 41/193 | OK | `naplok/F21P_jelentes.md`, `naplok/F21P_meres_p3b.md` f) szakasz, `f21p/meres_p3b_eredmeny.tsv`: 21,2% (41/193), végleg 0/193; kapupontonként 1: 4, 1-json: 20, 3: 2, 4: 1, 6: 14 (összesen 41); rétegenként 24+12+1+4 = 41. Kézi napló-összeg (`f21p/futasnaplo.tsv:313-346`): az első próbálkozások `kapuhiba_db`-je **41**; a 2. próbálkozások `igehely_db`-je **41**. |
| 1b a Megfigyelés-mondat | OK | „legalább 14 versben a C első válasza megsértette az A–B rögzítést; a 6. pontos kényszer és az egy újrakérés mindet javította (végleg 0/193).” |
| 1c a régi 27/193 | OK | Grep `27/193\|16/95\|14\.0% \(27` a `naplok/F21*.md`, `f21p/*.tsv`, `DONTESEK.md` és `F21_*.md` fájlokban: 0 találat; a módszer elmagyarázva. |
| 1d F3V2B külön | OK | „C (2. futás) v2 (F3V2B) 14.0% (28/200)” külön sorban. |
| 1e a keresztellenőrzés kódja | OK | `meres_p3b.py`: `hibatipusok_teljes` (döntőbírói futásnál az 5 pont és a 6. pont), `kapuhiba_kereszt` (újraszámolt halmaz, jsonl `probalkozas=2`, napló-összeg); a 12 kereszt-sor mind EGYEZIK; kézzel: F1V2 160, F2V2 141, F5V2 72, F6V2 57, F3V2B 28, F4V2 41. A szkript futtatása NEM ELLENŐRIZHETŐ. |
| 2 régi számok | OK | A diff törölt sorai: a fejléc-`ts`, az F4V2 kapuhiba-sorai és az F4V2-mondat (átírva); más szám nem tűnt el. |
| 3a a négy MANUAL-fejléc | OK | `f21p/c_diff_besorolas.tsv`, `c_diff_f3v2_osszevetes.tsv`, `c_diff_f3v2b_besorolas.tsv`, `c_regi_arany_besorolas.tsv`: `1 0` (csak az első sor új), a tartalmi sorok bájtra azonosak; `# MANUAL: scope=… \| forras=… \| ts=… \| manual (Opus-besorolás, nem mérés)`. |
| 3b az olvasók átugorják a #-sort | OK | `c_diff.py`, `jelentes_f21p.py`, `koltseg_vetit.py`, `meres_p3b.py`, `c_diff_f3v2.py`, `c_diff_f3v2b.py`: `not s.startswith('#')` vagy a `c_diff._tsv`. |
| 4a jelentés (e) k) | OK | „További nyitott tétel a P3b-ből (DT21 k): k) …”. |
| 4b DONTESEK | OK | A DT21 eleje átírva („… a P3b-vel meghaladott, l. DT22”); a k) tétel megvan (59,7% és 27,9%); más DT-sor nem változott. |
| 4c brief `lezarva_osszegzes` | OK | „−0,57 pp (pontosság) és +0,48 pp (lefedettség)”; „az N29 VAGY-szabályának 1. mérőszáma formálisan teljesül, az A–B eltérés csökkenése (20%) nem; nem végleges”; egy sor. |
| 4d `F21_zaras.md` | OK / megjegyzés | A 7. és 9. sor javítva; a 11. sor még „az a–j tételek”-et írt. **Javítva** az ellenőrzés után („a–k”). |
| 5a `adat/`, `konkordancia/`, FELADATOK | OK | `git diff --numstat origin/main..HEAD -- adat konkordancia FELADATOK.md` → 0. |
| 5b befagyasztott fájlok, válaszok, napló | OK | `git diff --numstat 4e95af4..HEAD` a befagyasztott fájlokon, az `f21p/valaszok`-on és a `futasnaplo.tsv`-n → 0. |
| 5c generált TSV-k | OK | `koltseg_vetites.tsv`, `koltseg_vetites_p3b.tsv`, `ingadozas.tsv`, `meres_v2_eredmeny.tsv`, `meres_eredmeny.tsv`, `.github` → nem változtak. |
| 5d kulcs-grep | OK | 0 találat. |
| 5e CI | OK | `eszkozok/ellenorzes/futtat.py … --pr-cim "[ELLENŐRZŐ] F21: …"` → minden szabály 0 találat (fej: f6ca73b). |
| Szkriptek újrafuttatása | NEM ELLENŐRIZHETŐ | Szerepkorlát. |
| 6 régi commit-üzenetek (75496f0, 6d94610, ac6fb49) | megjegyzés, elfogadva | A történet nem íródik át. |
| A1–A6, ellenőrzőlista | OK | Az értelmezés nyitott tétel lett (k); a proveniencia mind a négy kézi fájlon rendben; nincs új adat- vagy törölt adatsor. |

**Hiba és figyelmeztetés nélkül.** (Megjegyzés: 2 — egy javítva, egy elfogadva.)
