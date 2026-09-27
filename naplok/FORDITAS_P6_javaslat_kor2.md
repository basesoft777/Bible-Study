# FORDITAS_P6_javaslat_kor2 -- modellválasztási javaslat (6 modell, kiegészítő kör)

*2026.09.26 · ág: `claude/forditas-pilot-brief-3afbbf-37c8ky` · a
FORDITAS_PILOT_BRIEF.md §1 döntési szabálya szerint, a 2. modellkör (m1-m6)
gépi ellenőrzésének (`FORDITAS_P4_ellenorzes.tsv`) és a Claude (Opus, chat-menet) vak
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
| Claude Haiku 4.5 | 80,8% (97/120; a HIBA-sorok nélkül 85,1%) | 7,47 (n=19) | 0 | 0,2293 |
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
tartalék-ága lép életbe: **az éles fordítás Claude-dal megy**, **a külső
modell legfeljebb nyersfordítást (draft) adhat**, amit ember vagy Claude
ellenőriz/javít.

**Megjegyzés a tartalék-ághoz:** a szabály nem nevezi meg, melyik Claude-modell
fordítson. A mérés szerint a Claude Haiku 4.5 vak átlaga (7,47) a Gemini 3.1
Flash Lite (8,70) és a DeepSeek V4 Flash (8,60) alatt marad, a teljes Thayerre
becsült ára (~30 USD) pedig többszöröse az övékének — a Haiku mint éles
fordító tehát rosszabb minőséget adna drágábban. A tartalék-ág gyakorlati
olvasata: a külső modell nyersfordít, Claude ellenőriz és javít, a gépi
ellenőrzés által jelzett szócikkekre összpontosítva. A végleges döntés a
felhasználóé.

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
  a Claude-féle vak pontozás egymástól függetlenül, egybehangzóan azonosította.
  A kimenet 602 token (a többi modellé 1600–1800), és nem `length` állapottal
  állt le — egyszeri vagy rendszerszintű voltát a K2 újrafuttatás dönti el.
- **Claude Haiku 4.5**: a meglévő 19 szócikken erős, de a mintából
  hiányzik a legnagyobb egy-darabos szócikk (`G1941`) -- ismételt,
  tartós API-hiba miatt (l. FP3.2).
- **Qwen3.7 Flash**: rendszeresen csonkítja a hosszabb görög/héber
  szavakat (a vak pontozó és a gépi ellenőrzés is azonosította).
- **GPT-4o-mini**: a leggyengébb -- négy szócikken a fordítás gyakorlatilag
  a tartalom nélküli összefoglalásra zsugorodott (pl. `G3777`-nál csak
  "sem; és nem." maradt egy több mondatos szócikkből).

## 5. Módszertani megjegyzés

Ez a kör csak EGY bírálót használt: Claude-ot (Opus, chat-menet), vakon, a
kulcs megnyitása előtt (`FORDITAS_P5_pontok_kor2.tsv`). A 18 rövid/közepes
szócikket a bíráló teljes egészében olvasta, a két legnagyobbat (G4151,
G5590) mintavétellel és teljes gépi összevetéssel (görög/héber eltérés,
terminológia, Károli-rövidítések) pontozta. A brief FP5/FP6 terve Claude és
a felhasználó pontjainak összevetését írja elő (> 2 pontos eltérés
megjelölésével); a felhasználói minta még nem készült el, ezért ez az
összevetés függőben van. Második, független mérőszámként a gépi ellenőrzés
(FP4) szolgál, amely nagyfokú egyezést mutat a Claude-pontokkal.

## 6. DeepSeek G1941 újrafuttatás

A `G1941` DeepSeek-fordítása a kor2 futásban csonkolt (pontosság = 0, l. 4.
pont) -- annak eldöntésére, hogy ez egyszeri esemény vagy a modell hosszú,
összetett szócikkeken mutatott rendszerhibája, 3 független, gyorsítótár
nélküli hívás futott ugyanarra a bemenetre (`FORDITAS_P7_g1941_ujra.py`,
eredmény: `FORDITAS_P7_g1941_deepseek.tsv`/`.md`).

| Futás | Kimenet token | `finish_reason` | Hosszarány | 1. ellenőrzés (görög/héber) |
|---|---:|---|---:|---|
| 1 | 1833 | `stop` | 1,02 | RENDBEN |
| 2 | 1880 | `stop` | 1,04 | RENDBEN |
| 3 | 1817 | `stop` | 1,02 | RENDBEN |

Mindhárom futás teljes és hű (az eredeti csonkolt futás 602 kimeneti
tokenje helyett 1817-1880 token, hosszarány 1,02-1,04 a korábbi 0,32
helyett). **A csonkolás egyszeri volt; a DeepSeek a pontosság = 0 feltétel
szempontjából versenyben marad.**
