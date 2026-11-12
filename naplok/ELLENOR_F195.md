# ELLENOR_F195 — F195_DESIGN_SYSTEM_BRIEF.md, 7095bc63..849e589a

*Független ellenőr (`fuggetlen-ellenor`, claude-opus-5-5), 2026-11-11. Az ellenőr ebben a futásban nem írhatott fájlt; a jelentést a fő szál mentette változtatás nélküli tartalommal, a táblázat rövidítve. A javítókör a fájl végén.*

**Eredmény: ELTÉRÉS, 1 tétel.**

| pont | eredmény | fájl:sor | indok |
|---|---|---|---|
| 0 Modell | OK | — | a session `claude-opus-5-5`, a kért `opus`; a Co-Authored-By sor Opus 5.5 |
| G1 | OK | — | `git diff --numstat`: 5 fájl, mind az `ir` listán; a `statikus/`, `sablonok/`, `konfig/`, `DONTESEK.md`, `lexikon/`, `adat/` útvonalakra a `git log` üres |
| G2 | NEM ELLENŐRIZHETŐ | `teszt_tervezo.py:364-367` | a kód szerint a `--tokens-css`/`--bundle-css` csak a megadott útra ír; a tesztet a szerep miatt nem futtatta |
| G3, D2 | NEM ELLENŐRIZHETŐ | — | az artifactra vonatkozik |
| D1 | OK | `dontesek/uj/…:1`, `nyitott/uj/…:1` | helyőrzők a PR-onkénti fájlokban; E32 = 0 |
| (1) box-shadow kinyerése | OK | `arculat_szinkron.py:197-221`; `olvaso.css:264, 287, 300, 345` | 4 előfordulás → 3 token (`arnyek-reszletek`, `arnyek-konyvpanel` a `.javaslat`-tal összevonva, `arnyek-navlap-nyitva`); a `@media` és a több szelektoros szabály helyes. Gyengeség: a teszt csak az `arnyek-reszletek`-et nézi |
| (2) tokens.css szerkezete | OK (a felsorolt elemek) | `arculat_szinkron.py:227-273` | a sorrend megfelel; a `*/` a kommentben védve |
| (2a) stílusosztály-nevek ütközése | **ELTÉRÉS** | `arculat_szinkron.py:262-268`; `olvaso.css:39, 57, 102, 105, 185, 203, 208, 213` | a stílusosztály neve a betűméret-kulcs; legalább 11 egyben szerverosztály (`.versszam`, `.jelleg`, `.sor`, `.ubs`, `.logo`, `.torzs`, `.igehely`, `.utmutato`, `.lxx-sor`, `.allapot`, `.szoalcim`). Az előnézetben a szerver markupja idegen `font-family`-t, `line-height`-ot, `letter-spacing`-et kap |
| (3) bundle.css változói | OK | `arculat_szinkron.py:276-284` | az `--fs/--lh/--space/--radius` négy előtagon kívüli minden hivatkozás (színek, `arnyek`, `g-*`, `--font-*`) a tokens.css-ből jön; az olvaso.css nem definiál változót |
| (4) DT153/DT154 | OK | `arculat_szinkron.py:15, 148, 177` | `7e12a25f szamkiosztas: DT-F98a → DT153, DT-F98b → DT154`; tartalmilag is egyezik |
| A1–A6 | OK / nem alkalmazható | — | eszközkód, nincs adatállítás; az N156 állapota ellenőrizve |
| CI | OK | — | `futtat.py --valtozott … --diff-alap 7095bc63 --diff-fej 849e589a`: kilépési kód 0, E32 = 0; az E25/E27/E34 jelzései a diffen kívüli, meglévő fájlokra |
| Ellenőrzőlista 1–5 | OK | — | 6 törölt sor (3 helyőrző-csere, 2 kiírás-átírás, 1 tesztbővítés); `adat/`, `konkordancia/` Δ = 0; a ⛔ betartva |

**Nem eltérés, de érdemes tudni:** az `eszkozok/olvaso_szerver/README.md` nem említi az új kapcsolókat (nincs az `ir` listán); az `arnyek-navlap-nyitva` név állapotosztályból jön.

## Javítókör (1., 2026-11-11, fő szál)

- (2a) → `tokens_css(tj, css)`: a szerver stíluslapjában is használt nevű stílus osztálya `ds-` előtagot kap (`szerver_osztalyok`); a mai állapotban 13 osztály (`ds-lxx-sor`, `ds-torzs`, `ds-jelleg`, `ds-versszam`, `ds-allapot`, `ds-igehely`, `ds-jel-cimke`, `ds-logo`, `ds-sor`, `ds-szoalcim`, `ds-szoveg-jegy`, `ds-ubs`, `ds-utmutato`). A `tokens.json` változatlan.
- A teszt kiegészült: a `ds-` előtag, egyetlen szerverosztály sem marad stílusosztályként, és az árnyék-tokenek teljes listája (3 név).
- A design system `tokens.css`-e és a vászon másolata újra kiment.
