# FP2_felmeres — 0. lépés (csak olvas)

*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2 · 2026.09.28 · ág: `claude/thayer-stilusproba-fp2` ·
alap: `main` (`8f5a1eb`, tartalmazza a #3-at, PR #62 mergelve; a #3 merge-commitja
`9eb43fe`, ellenőrizve ancestor-e a `main` HEAD-nek: igen) ·
mérő szkript: `naplok/FP2_meres.py`*

## 0.1 A kor2 eredményének ellenőrzése

Forrás: [`naplok/FORDITAS_P6_javaslat_kor2.md`](FORDITAS_P6_javaslat_kor2.md) 1. táblázata
(gépi ellenőrzés: `FORDITAS_P4_ellenorzes.tsv`; vak pontozás: `FORDITAS_P5_pontok_kor2.tsv`,
kulcs: `FORDITAS_P4_vak_kulcs_kor2.tsv`).

| Modell | Pontszám (repó) | Pontszám (brief) | Egyezik? |
|---|---:|---:|---|
| Gemini 3.8 Flash | 9,35 | 9,35 | ✔ |
| Gemini 3.1 Flash Lite | 8,70 | 8,70 | ✔ |
| DeepSeek V4 Flash | 8,60 | 8,60 | ✔ |
| Claude Haiku 4.5 | 7,47 | 7,47 | ✔ |
| Qwen3.7 Flash | 5,00 | 5,00 | ✔ |
| GPT-4o-mini | 3,95 | 3,95 | ✔ |

**Nincs eltérés** a brief táblája és a repó jelentése között.

A 20 szócikk listája ([`naplok/FORDITAS_P1_minta.md`](FORDITAS_P1_minta.md) §1):
E (13): G0012, G0086, G0282, G0813, G0994, G1311, G1944, G2671, G4151, G5010, G5351,
G5356, G5590 · A (1): G1941 · N (3): G0035, G0540, G2672 · V (3): G0004, G0002, G3777.

A vak pontozás rubrikája (`FORDITAS_P5_pontok_kor2.tsv` fejléce): `pontossag` (0–3),
`terminologia` (0–2), `magyar` (0–3), `formai` (0–2), `osszesen` (0–10). Ez a rubrika
a brief 5. lépésében újra felhasználandó.

*proveniencia: scope=fájlolvasás (nem lekérdezés) | forras=naplok/FORDITAS_P6_javaslat_kor2.md,
naplok/FORDITAS_P1_minta.md, naplok/FORDITAS_P5_pontok_kor2.tsv | ts=2026-09-28*

## 0.2 `eszkozok/fordit.py` — paraméterek, prompt/terminológia bekötés

Forrás: a fájl teljes elolvasása (`eszkozok/fordit.py`, 849 sor).

- **Hőmérséklet:** `temperature=0` (`_valodi_http_kuldo`), mindhárom kor2-modellnél azonos.
- **Reasoning:** kikapcsolva (`reasoning: {enabled: False}`), **kivéve** a
  `GONDOLKODAS_KOTELEZO_MODELLEK` halmazban lévő modelleket (jelenleg csak
  `google/gemini-3.8-flash`, amely HTTP 400-zal utasítja el a kikapcsolást).
- **Max token:** nincs explicit `max_tokens` paraméter átadva a híváskor — a modell
  alapértelmezett limitje érvényesül; a válasz JSON-séma (`response_format: json_schema`,
  `strict: true`) kényszeríti ki a `{strong, forditas_hu, bizonytalan_feloldasok}` alakot.
- **Prompt és terminológia bekötés:** a fájl **hardkódolt útvonalakat** használ
  (`PROMPT_UT = naplok/FORDITAS_P_prompt_v1.md`, `TERMINOLOGIA_UT =
  naplok/FORDITAS_P_terminologia.tsv`, `PROMPT_VERZIO = 'v1'`,
  `TERMINOLOGIA_VERZIO = 'v1'`), **nincs CLI-kapcsoló** az útvonal felülírására. A
  gyorsítótár kulcsa is tartalmazza a `prompt_verzio`/`terminologia_verzio` konstanst.
- **Modell-jelek:** `MODELL_JELEK` szótár, szintén hardkódolt (`m1`–`m6`); a MiniMax
  modell nincs benne, hozzáadást igényel.
- **Darabolás (G6):** 4000 karakteres határ felett a szócikk saját számozásán/betűzésén
  vág (`darabokra_bont`); egyik FP2-mintaszócikk sem éri el ezt kor2-ben, a 10 új
  szócikknél a mintavétel (1. lépés) figyeli.
- **Hibakezelés:** `finish_reason in ('length','max_tokens','error')` csonkolásnak
  számít, újrapróbál (JSON-újrapróba 2×, HTTP-újrapróba 4×, visszalépéses várakozással).
- **Költségnapló/plafon:** `KoltsegNaplo`, `usage.cost`-ból (vagy `ar_config`
  tartalékból), G7 plafon leállítja a futást a soron következő hívás előtt.

**Következmény a 4. lépésre:** mivel a script nem paraméterezhető prompt/terminológia
útvonalra, az FP2 futtatáshoz **nem módosítom** a `fordit.py`-t (a brief tiltja a #3
eszközök javítását) — ehelyett a 2–3. lépésben eldöntött módon (külön FP2-másolat vagy
override-argumentum hozzáadása *saját, FP2-fájlként*, nem a #3 fájl módosításaként)
oldom meg. Ezt a döntésnaplóba (8. lépés) rögzítem, amikor a konkrét megoldás megvan.

## 0.3 A MiniMax legújabb szövegmodellje

Lekérdezés: `GET https://openrouter.ai/api/v1/models`, `naplok/FP2_meres.py`
(`openrouter_modellek()`).

| Modell-azonosító | `created` (unix) | Bemenet USD/1M | Kimenet USD/1M | Kontextus |
|---|---:|---:|---:|---:|
| minimax/minimax-01 | 1736915462 | 0,20 | 1,10 | 1 000 192 |
| minimax/minimax-m1 | 1750200414 | 0,40 | 2,20 | 1 000 000 |
| minimax/minimax-m2 | 1761252093 | 0,30 | 1,20 | 204 800 |
| minimax/minimax-m2.1 | 1766454997 | 0,30 | 1,20 | 204 800 |
| minimax/minimax-m2-her | 1769177239 | 0,30 | 1,20 | 65 536 |
| minimax/minimax-m2.5 | 1770908502 | 0,27 | 1,08 | 204 800 |
| minimax/minimax-m2.7 | 1773836697 | 0,30 | 1,20 | 204 800 |
| **minimax/minimax-m3** | **1780245374 (legújabb)** | **0,30** | **1,20** | **1 048 576** |

**Választás: `minimax/minimax-m3`** — a `created` mező szerint a legfrissebb, és
támogatja a `response_format`/`structured_outputs` paramétert (a `fordit.py`
JSON-séma-kényszerítéséhez ez szükséges; a `minimax-m2-her` és a `minimax-01` ezt
**nem** támogatja, tehát ezek nem is jöhetnének szóba). A leírása szerint multimodális
(szöveg+kép) alapmodell, de szövegfordításra alkalmas általános LLM.

*proveniencia: scope=OpenRouter /api/v1/models lekérdezés | forras=https://openrouter.ai/api/v1/models
| ts=2026-09-28T06:33:14Z*

## 0.4 A három versenyző modell aktuális ára (OpenRouter)

| Modell | OpenRouter-azonosító | Bemenet USD/1M | Kimenet USD/1M | Kontextus | `response_format` |
|---|---|---:|---:|---:|---|
| Gemini 3.1 Flash Lite | `google/gemini-3.1-flash-lite` | 0,25 | 1,50 | 1 048 576 | ✔ |
| DeepSeek V4 Flash | `deepseek/deepseek-v4-flash` | 0,14 | 0,28 | 1 048 576 | ✔ |
| MiniMax M3 | `minimax/minimax-m3` | 0,30 | 1,20 | 1 048 576 | ✔ |

**Eltérés jelzése:** a `deepseek/deepseek-v4-flash` ára a kor2 mérése (2026.09.26,
`FORDITAS_P0_modellek.json`: 0,047 / 0,0941 USD/1M) óta **kb. háromszorosára nőtt**
(0,14 / 0,28 USD/1M) — ez nem mérési hiba, hanem valódi OpenRouter-ártáblázat-változás;
a 7. lépés költségbecslése a **most mért, friss árat** használja, nem a kor2-belit.
A Gemini 3.1 Flash Lite ára változatlan (0,25 / 1,50).

*proveniencia: scope=OpenRouter /api/v1/models lekérdezés | forras=https://openrouter.ai/api/v1/models
| ts=2026-09-28T06:33:14Z*

Teljes jelöltlista (MiniMax-variánsok + a két másik modell): `naplok/FP2_openrouter_jeloltek.json`.

## 0.5 `Thayer_teljes.tsv` statisztika

Lekérdezés: `naplok/FP2_meres.py` (`thayer_stat()`), a teljes fájlon.

| Mérőszám | Érték |
|---|---:|
| szócikkek száma | 5 426 |
| teljes karakterszám (`Teljes_szocikk` összesen) | 4 440 084 |
| medián hossz | 382 |
| p90 hossz | 1 606 |
| max hossz | 34 670 |
| min hossz | 21 |

*proveniencia: scope=teljeskörű fájlolvasás, split('\t') | forras=konkordancia/Thayer_teljes.tsv
| ts=2026-09-28T06:33:14Z*

## A prompt v2 / terminológia v2 forrása

A felhasználó a session közben csatolta a `FORDITAS_ELES_THAYER_BRIEF.md`-t
(`E:\Letöltések\FORDITAS_ELES_THAYER_BRIEF.md`, v2, 2026.09.26). Ez egy **még nem
végrehajtott** tervdokumentum (nincs `naplok/FORDITAS_P_prompt_v2.md`, nincs
`naplok/FORDITAS_P_terminologia_v2.tsv`, nincs `claude/forditas-eles-thayer` ág és `FE*`
commit a repóban — ellenőrizve) — az "éles Thayer-fordítás" briefje, amelynek E1 tétele
tartalmazza szó szerint a prompt v2 hat kiegészítő szabályát és a terminológia v2 25 új
sorát. Ezekből építettem fel (a 2. lépés részeként):

- [`naplok/FORDITAS_P_prompt_v2.md`](FORDITAS_P_prompt_v2.md) — a v1 szó szerint +
  az E1 hat szabálya.
- [`naplok/FORDITAS_P_terminologia_v2.tsv`](FORDITAS_P_terminologia_v2.tsv) — a v1 13
  sora + az E1 táblájának 25 sora.

*proveniencia: scope=fájlolvasás (nem lekérdezés) | forras=E:\Letöltések\FORDITAS_ELES_THAYER_BRIEF.md
(E1 szakasz) | ts=2026-09-28*

## Döntés a `fordit.py` prompt/terminológia-útvonaláról

A 0.2 pontban jelzett korlát (nincs CLI-kapcsoló az útvonalra) feloldása: a
`FORDITAS_ELES_THAYER_BRIEF.md` E1 tétele maga is `--prompt`/`--terminologia`
kapcsolót tervez a `fordit.py`-hoz, alapértékkel a v1-re (visszafelé kompatibilis,
a pilot reprodukálható marad). A 2. lépésben **ugyanezt** a kapcsolópárt adom hozzá a
`eszkozok/fordit.py`-hoz — ez nem hibajavítás, hanem additív, alapértelmezésben
változatlan viselkedésű bővítés, amelyet egy másik brief már ugyanígy tervezett.
Ezt a döntésnaplóba (8. lépés) is felveszem.
