# FORDITAS_P6_javaslat_kor2 -- modellválasztási javaslat (6 modell, kiegészítő kör)

*2026.09.26 · ág: `claude/forditas-pilot-brief-3afbbf-37c8ky` · a
FORDITAS_PILOT_BRIEF.md §1 döntési szabálya szerint, a 2. modellkör (m1-m6)
gépi ellenőrzésének (`FORDITAS_P4_ellenorzes.tsv`) és a felhasználó vak
pontozásának (`FORDITAS_P5_pontok_kor2.tsv`, kulcs:
`FORDITAS_P4_vak_kulcs_kor2.tsv`) összevetésével. Ez a jelentés a kiegészítő
(nem a brief eredeti G3-) modellkört zárja le -- az eredeti 3 modellre a
hivatalos FP5/FP6 (Opus, 2. menet) még nem futott.*

## 1. A három mérőszám együtt

| Modell | Gépi átmenési arány | Vak pontszám átlaga (0-10) | Pontosság=0 esetek | Költség (USD, 20 szócikk) |
|---|---:|---:|---:|---:|
| Gemini 3.8 Flash | **90,8%** | **9,35** | 0 | 0,6072 |
| Gemini 3.1 Flash Lite | 88,3% | 8,70 | 0 | 0,0593 |
| DeepSeek V4 Flash | 85,8% | 8,60 | 1 (`G1941`) | 0,0148 |
| Claude Haiku 4.5 | 85,1% | 7,47 (n=19) | 0 | 0,2293 |
| Qwen3.7 Flash | 70,0% | 5,00 | 0 | 0,0059 |
| GPT-4o-mini | 55,0% | 3,95 | 4 | 0,0209 |

A gépi ellenőrzés (mennyiségi, formai hűség) és a vak emberi pontozás
(minőségi, nyelvi/tartalmi) **egymást megerősítve** ugyanazt a sorrendet
adja -- ez önmagában megbízhatóvá teszi mindkét mérést erre a mintára.

## 2. A brief §1 döntési szabályának alkalmazása

> Az a modell javasolható, amelynél a gépi ellenőrzések átmenési aránya
> **≥ 95%**, egyetlen szócikk pontossága sem 0, és a bírálati átlaga a
> legmagasabb; közel azonos átlagnál (≤ 0,5 pont) az olcsóbb. Ha egyik sem
> felel meg: az éles fordítás Claude-dal megy, a külső modell csak
> nyersfordítást ad.

**Egyik modell sem éri el a 95%-os gépi küszöböt** (a legjobb is csak
90,8%) -- a szabály szó szerinti alkalmazása szerint **egyik sem
javasolható éles fordításra ezen a mintán**. A szabály explicit
tartalék-ága lép életbe: **az éles fordítás Claude-dal megy** (l. a jelenlegi
pilot is Claude Haiku 4.5-tel és a Claude Sonnet 5 munkamenet-modellel
dolgozik), **a külső modell legfeljebb nyersfordítást (draft) adhat**,
amit ember vagy Claude ellenőriz/javít.

Ha a küszöböt tájékozódásképpen 90%-ra engednénk (nem a brief döntése,
csak érzékeltetés): egyedül a **Gemini 3.8 Flash** kerülne a közelébe
(90,8%), és a vak pontszáma is a legmagasabb -- de az ára is a
legmagasabb, közel a Claude Haiku 4.5 háromszorosa.

## 3. Ár/minőség jegyzet (nem a formális döntés, csak megfigyelés)

A **Gemini 3.1 Flash Lite** a leginkább figyelemre méltó jelölt egy jövőbeli,
esetleg enyhébb küszöbű körre: a Gemini 3.8 Flash 93%-át hozza a vak
pontszámban, miközben az ára ~1/10-e. Ha a projekt a jövőben újragondolja a
95%-os küszöböt (pl. egy javított prompt vagy utólagos gépi javítás
mellett), ez lenne az első jelölt az újratesztelésre.

## 4. Modellenkénti minőségi jellemzés (a vak megjegyzésekből)

- **Gemini 3.8 Flash / 3.1 Flash Lite**: következetesen hű és teljes,
  elszórt apró hibákkal (fel nem oldott rövidítés, egy-egy elgépelés).
- **DeepSeek V4 Flash**: amikor jó, nagyon jó (több 9-10 pontos), de a
  legnagyobb/legbonyolultabb szócikken (`G1941`) félbehagyta a fordítást --
  ugyanezt a hibát a gépi ellenőrzés (FP4, `FORDITAS_P_jelentes.md` 3.2) és
  a vak emberi pontozás egymástól függetlenül, egybehangzóan azonosította.
- **Claude Haiku 4.5**: a meglévő 19 szócikken erős, de a mintából
  hiányzik a legnagyobb egy-darabos szócikk (`G1941`) -- ismételt,
  tartós API-hiba miatt (l. FP3.2).
- **Qwen3.7 Flash**: rendszeresen csonkítja a hosszabb görög/héber
  szavakat (a vak pontozó és a gépi ellenőrzés is azonosította).
- **GPT-4o-mini**: a leggyengébb -- négy szócikken a fordítás gyakorlatilag
  a tartalom nélküli összefoglalásra zsugorodott (pl. `G3777`-nál csak
  "sem; és nem." maradt egy több mondatos szócikkből).

## 5. Módszertani megjegyzés

Ez a kör csak EGY bírálót (a felhasználót) használt -- a brief FP5/FP6
eredeti terve Claude (Opus) és a felhasználó pontjainak összevetését írja
elő, > 2 pontos eltérések megjelölésével. Mivel itt nem készült külön
Claude-alapú vak pontozás a kor2 mintára, ez az összevetés most elmarad;
a gépi ellenőrzés (FP4) szolgál második, független mérőszámként, és --
amint fent látható -- nagyfokú egyezést mutat a felhasználó pontjaival.
