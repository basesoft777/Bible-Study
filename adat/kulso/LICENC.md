# adat/kulso/ — külső adatok licenc- és proveniencia-jegyzéke

*Tükör: az irányadó licenc-leltár az `adat/licencek.tsv` (`lxx_bridge` sor, SEMA 2.19); ellentmondás esetén az a tábla érvényes.*

| Fájl | Forrás | Alkonfig | Letöltve | Licenc | Megjegyzés |
|---|---|---|---|---|---|
| `lxx_bridge.tsv` | https://huggingface.co/datasets/bcv-commons/hebrew-lexical-references (bcv-commons; revízió `b3b135b24394aa4a8f4eaa59dbc59689735c2b46`; közvetlen fájl: `…/resolve/main/lxx_bridge.tsv`) | `lxx_bridge` | 2026.10.04 | **CC BY 4.0** (bcv-commons; a MACULA Hebrew/Greek Strong-címkézése CC BY 4.0; a mögöttes LXX-szöveg közkincs) | A dataset-kártya szerint nem UBS MARBLE / Louw-Nida / SDBH-eredetű, és a kártya License szakasza négy alkonfigot nevez meg, ebből a `lxx_bridge`-re CC BY 4.0-t ad; 3 301 adatsor + fejléc, 48 191 bájt, SHA-256 `97c1c2a8df1f33069ecd88dab3a1b7ff179e900236ac41cd4d93f12ec5d40cff`; oszlopok: `hebrew_strong` (`H####`), `greek_strong` (`G####`), `count` (≥3); a fájl változatlan, tabbal tagolt (TSV). Attribúció: bcv-commons, *Hebrew Lexical Reference Indices*, `lxx_bridge`, MACULA Hebrew/Greek (CC BY 4.0) alapján. |

## Forráspolitika (DT-F43 (d), a D17 mellé)

Nem kereskedelmi (NC) vagy csak-hivatkozási licencű forrás nem kerül a repóba, származtatott adaton át sem; HF-dataset importja előtt a kártya attribúciós táblája ellenőrizendő. Kizárva: CrossWire `GreekHebrew` és `HebrewGreek` (Pierre Leblanc, Abbott-Smith + Hatch–Redpath alapján; „copyrighted, free non-commercial distribution”) és származékaik (pl. NuBerea/lxx-analysis, NuBerea/crosswire-greekhebrew).
