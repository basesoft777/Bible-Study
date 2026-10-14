# Betűk — saját tárolás (F76 arculat)

Az olvasói szerver a #60 pilot betűit használja (`eszkozok/olvaso_pilot/sablon.html`), saját tárolásban: a szerver CSP-je (`style-src 'self'`, `default-src 'self'`) külső betűforrást nem enged, és a látogató böngészője így nem kér le semmit harmadik féltől. A `@font-face` szabályok a `../fonts.css`-ben állnak, a fejléc-sablon (`sablonok/alap.html`) tölti be.

| Család | Szerep (CSS-változó) | Fájlok | Licenc |
|---|---|---|---|
| Source Serif 4 | magyar szöveg (`--font-text`) | `SourceSerif4-*.woff2` | `OFL-SourceSerif4.txt` |
| Frank Ruhl Libre | héber (`--font-he`) | `FrankRuhlLibre-*.woff2` | `OFL-FrankRuhlLibre.txt` |
| Noto Serif | görög (`--font-gr`) | `NotoSerif-*.woff2` | `OFL-NotoSerif.txt` |
| IBM Plex Sans | felület (`--font-ui`) | `IBMPlexSans-*.woff2` | `OFL-IBMPlexSans.txt` |
| IBM Plex Mono | Strong-számok, kódok (`--font-mono`) | `IBMPlexMono-*.woff2` | `OFL-IBMPlexMono.txt` |

- **Forrás:** Google Fonts (`fonts.googleapis.com/css2`, woff2, változó súlytartomány, ahol van), letöltve 2026-10-14. Csak a használt írásrendszerek részhalmazai: `latin`, `latin-ext` (magyar ékezetek), `hebrew`, `greek`, `greek-ext` (politonikus görög). A fájlnév: `<család>-<stílus>-<súly>-<részhalmaz>.woff2`.
- **Licencszövegek:** a Google Fonts hivatalos tárából (`github.com/google/fonts`, `ofl/<család>/OFL.txt`, `main` ág, 2026-10-14), változtatás nélkül.
- **Licenc:** SIL Open Font License 1.1. A betűfájlok szabadon használhatók és továbbadhatók, kereskedelmi célra is, a licencszöveggel együtt; önállóan nem árusíthatók. A fájlok módosítatlanok (a Google Fonts saját részhalmazai). Az IBM Plex licence a „Plex” nevet fenntartott betűnévként (Reserved Font Name) jelöli: módosított változat nem viselheti ezt a nevet.
- A betűk szoftver-eszközök, nem adatkészletek, ezért nem szerepelnek az `adat/licencek.tsv`-ben (SEMA 2.19: adatkészletenként egy sor).
