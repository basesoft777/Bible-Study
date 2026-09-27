# FORDITAS_P0 — hozzáférés és kiindulás

*FORDITAS_PILOT_BRIEF.md v1, FP0 · 2026.09.26 · ág: `claude/forditas-pilot-brief-3afbbf` · mérő szkript: `naplok/FORDITAS_P0_meres.py`*

## 1. A §0 újramérése

| # | Mérés | A brief értéke | Mért érték | Egyezik? |
|---|---|---|---|---|
| 0.1 | `main` | `72b200c` | `72b200c` | ✔ |
| 0.2 | `lexikon_hivatkozasok.tsv`, `szotar = Thayer` | 14 sor, 1 lefordítva, 13 üres | 14 sor; lefordítva: G1941; üres (13): G0012, G0086, G0282, G0813, G0994, G1311, G1944, G2671, G4151, G5010, G5351, G5356, G5590 | ✔ |
| 0.3 | a 13 üres szócikk `szoveg_en`-hossza | ~39 500; G4151 ~23 700, G5590 ~5 950 | 39 515; G4151 23 705, G5590 5 950 | ✔ |
| 0.3b | *(kiegészítő)* `szoveg_en` = `Thayer_teljes.Teljes_szocikk`? | — | mind a 14 Thayer-sornál **azonos** (a SEMA 2.5 „rövid kivonat" leírása a Thayer-soroknál nem áll: teljes szócikk) | — |
| 0.4 | görög tokenek Thayer-sor nélkül | 3: G0035, G0540, G2672 | **eltérés a mérés módjában:** a `strong` oszlopban 13 görög token van, mind Thayer-sorral (0 hiány). A 3 token a sorok **szövegmezőiben** szerepel (KIRALY-001 Zsid 7:1-28: G0035, G0540; HAMART-001 Gal 3:13: G2672); a teljes soron mérve a halmaz 16, a hiány pontosan a brief 3 tokenje. Mind a 3 megvan a `Thayer_teljes.tsv`-ben (186, 214, 1 025 karakter). | ✔ (b-módon) |
| 0.5 | `Thayer_teljes.tsv` | 5 426 szócikk, 3 oszlop | 5 426; `Strong_padded`, `Strong_eredeti`, `Teljes_szocikk` | ✔ |
| 0.6 | fordítási szabály | SEMA 2.5 `forditas_hu` | megvan, változatlan | ✔ |
| 0.7 | OpenRouter-minta | `eszkozok/cremer_ocr_javit.py` | megvan (kulcs környezetből, `_http_post_nyers` újrapróbálkozás 2/4/8/16 s, `usage.cost`, `KoltsegNaplo`, gyorsítótár) | ✔ |

A 0.4 eltérés a pilotot nem érinti: az N csoport ugyanaz a 3 szócikk. Folytatom.

## 2. Hozzáférés

- `OPENROUTER_API_KEY`: **beállítva** (a Bash- és a PowerShell-környezetben is; az értéke sehol nem került kiírásra).
- `GET https://openrouter.ai/api/v1/models`: HTTP 200, 458 modell. A futás tehát **helyi worktree-ben** megy (a brief „Futás" pontja szerint).

## 3. Modellek (G3) — a `/api/v1/models` végpontról, 2026.09.26

| Jel | OpenRouter-azonosító | Bemenet USD/1M | Kimenet USD/1M | Kontextus | `response_format` |
|---|---|---|---|---|---|
| m1 | `deepseek/deepseek-v4-flash` | 0,047 | 0,0941 | 1 048 576 | ✔ |
| m2 | `google/gemini-3.8-flash` | 0,75 | 3,75 | 1 048 576 | ✔ |
| m3 | `anthropic/claude-haiku-4.5` | 1,00 | 5,00 | 200 000 | ✔ |
| *(alternatíva)* | `openai/gpt-5-mini` | 0,25 | 2,00 | 400 000 | ✔ |

Az m3 a G3 javaslata szerint Claude Haiku 4.5 (minőségi viszonyítás). A `:batch` és a
`-latest`/dátumozott változatok nem kerültek be: a G3 a névleges modellt kéri, és a
`~…-latest` álnevek azonosítója időben elmozdul. A teljes jelöltlista:
`naplok/FORDITAS_P0_modellek.json`.

## 4. Kiinduló gépi kapu (K2 alapja)

`python eszkozok/ellenoriz.py` → **RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2**.
