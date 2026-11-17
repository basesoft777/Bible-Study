# Kódkönyv: f172/kulso_biralo/harom_biralo_itelet.tsv (FAGYASZTVA, F175.B7)

Az 1 600 mintapár (#172) három vak gépi bíráló szerint. SHA-256: a `harom_biralo_itelet.tsv.sha256` fájlban. A tábla nem írható át (`kulso_biralo_ertekel.py` csak ellenőrzi).

| oszlop | jelentés |
|---|---|
| `f172_id` | a #172 `minta_id`-je; a validációs minta `f172_id` oszlopa ezzel kapcsolódik |
| `reteg`, `vers`, `hu_sorszam`, `hu_szo` | a minta rétege és a Károli-szó |
| `er_sorszam`, `er_szo`, `strong`, `morfema` | a gépi pár eredeti tokenje; `morfema` = 1, ha H9001–H9049 |
| `<bíráló>_halmaz` | a bíráló által a Károli-szóhoz jelölt eredeti tokenek sorszáma, vesszővel; `-` = betoldás (üres halmaz) |
| `<bíráló>_helyes` | 1, ha a gépi pár tokenje a bíráló halmazában van |
| `tobbseg_helyes` | 1, ha legalább két bíráló helyesnek ítélte |
| `egyhangu` | 1, ha a három pár-ítélet azonos (mindhárom helyes VAGY mindhárom hibás; 1 555 pár). **Nem** a „mindhárom helyesnek ítélte” (az: mindhárom `*_helyes` = 1; 1 513 pár). |

Bírálók: `opus` = claude-opus-5-5 (#172); `gemini` = OpenRouter `google/gemini-4-argon`; `gpt` = OpenRouter `openai/gpt-6.1-sol` (2026-11-17, azonnali mód).
