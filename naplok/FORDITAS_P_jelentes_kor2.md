# FORDITAS_P_jelentes_kor2 -- 2. modellkör (kiegészítő, a felhasználó kérésére)

*2026.09.26 · ág: `claude/forditas-pilot-brief-3afbbf-37c8ky* · Ez a kör NEM a
FORDITAS_PILOT_BRIEF.md G3 döntése, hanem az FP0-FP4 ⛔ megállása után, a
felhasználó kérésére futtatott kiegészítő összevetés, ugyanazon az
infrastruktúrán (`eszkozok/fordit.py`, `FORDITAS_P1_minta.tsv`,
`FORDITAS_P_prompt_v1.md`, `FORDITAS_P_terminologia.tsv`,
`FORDITAS_P4_ellenoriz.py`) -- a `FORDITAS_P_jelentes.md` (az eredeti 3
modell) ettől külön áll, nem íródott felül.*

**Új modellek:** m4 = GPT-4o-mini (`openai/gpt-4o-mini`), m5 = Gemini 3.1
Flash Lite (`google/gemini-3.1-flash-lite`), m6 = Qwen3.7 Flash
(`qwen/qwen3.7-flash`).

## 1. Költség (mind a 6 modell, a teljes 20 szócikkes mintán)

| Modell | Költség (USD) |
|---|---:|
| Qwen3.7 Flash | 0,0059 |
| DeepSeek V4 Flash | 0,0148 |
| GPT-4o-mini | 0,0209 |
| Gemini 3.1 Flash Lite | 0,0593 |
| Claude Haiku 4.5 | 0,2293 |
| Gemini 3.8 Flash | 0,6072 |
| **Összesen** | **0,9375** |

A G7 2 USD-s plafonja alatt. Mindhárom új modell hibátlanul (33/33
hívás/darab, 0 HIBA) lefutott -- az egyetlen HIBA sor a már dokumentált,
tartós `G1941` + Claude Haiku hiány (l. `FORDITAS_P_jelentes.md` 3.1).

**Figyelemre méltó:** a Gemini 3.1 Flash Lite -- a 3.8 Flash-sel ellentétben
-- elfogadta a gondolkodás kikapcsolását (nem HTTP 400-zal utasította el),
ezért az ára töredéke a 3.8-nak, miközben az átmenési aránya (l. lent) csak
kicsit marad el tőle.

## 2. Gépi átmenési arány (SS1 1., 2., 3., 4., 5., 7. ellenőrzése)

| Modell | RENDBEN | SÉRTÉS | HIBA | Átmenési arány |
|---|---:|---:|---:|---:|
| Gemini 3.8 Flash | 109 | 11 | 0 | 90,8% |
| **Gemini 3.1 Flash Lite** | 106 | 14 | 0 | **88,3%** |
| DeepSeek V4 Flash | 103 | 17 | 0 | 85,8% |
| Claude Haiku 4.5 | 97 | 17 | 6 | 80,8% (97/120; HIBA nélkül 85,1%) |
| **Qwen3.7 Flash** | 84 | 36 | 0 | **70,0%** |
| **GPT-4o-mini** | 66 | 54 | 0 | **55,0%** |

A Gemini 3.1 Flash Lite a legjobb ár/minőség arányú jelölt ezen a mintán:
csak 2,5 ponttal marad el a legjobb (3.8) átmenési arányától, de kb.
10×-esen olcsóbb. A GPT-4o-mini és a Qwen3.7 Flash érdemben gyengébben
teljesített, és MINDKETTŐNÉL más-más, jellegzetes, rendszerszintű hiba
azonosítható (l. 3. pont) -- nem véletlen szórás.

## 3. Modellspecifikus hibatípusok (új találatok)

### 3.1 GPT-4o-mini: rendszeresen elhagyja a szócikk fejlécét

A `1_gorog_heber` ellenőrzés mind a 20 szócikken SÉRTÉS-t adott -- ez nem
szórás, hanem rendszerszintű minta: a GPT-4o-mini következetesen kihagyja a
szócikk Strong-számát és a fejléc görög címszavát a hozzá tartozó
etimológiai/nyelvtani jelöléssel együtt, és a definíció közepén kezdi a
fordítást. Példa (`G0004`):

- **Forrás:** "G4 — ἀβαρής (ές (βάρος weight), without weight, light;
  tropically, not burdensome: ..."
- **GPT-4o-mini fordítása:** "könnyű; átvitt értelemben nem megterhelő:
  ..." (a "G4 —", "ἀβαρής", "(ές (βάρος weight)," rész teljesen hiányzik)

Ugyanez a minta `G0012`-nél is: a fordítás "áthatatlan, feneketlen, a
mélység..."-gyel kezdődik, a "G12 — ἄβυσσος ... adjective, (ος, (from ὁ
βύσσος equivalent to βυθός)" rész nélkül. Ez a SEMA 2.5 szabály közvetlen
megsértése ("a forrás héber/görög idézetei változatlanok"), és minden
egyes szócikket érint ebben a mintában -- súlyos, nem alkalmi hiba.

### 3.2 Qwen3.7 Flash: görög szavak csonkolása

A `qwen/qwen3.7-flash` 14/20 szócikken hibázott az 1. ellenőrzésen, de
más jelleggel: nem a szócikk elejét hagyja el, hanem egyes hosszabb,
ékezetes görög/héber szavakat vág el a közepén -- pl. `αβυσσος` helyett
`αβ`, `βυθος` helyett `βυθ`, `ετηρησα` helyett `ετηρη`,
`αγενεαλογητος` (teljesen hiányzik). A minta arra utal, hogy a modell a
hosszabb, ritka görög tokeneket nem mindig generálja végig -- ez inkább
generálási/tokenizálási korlátra utaló jelenség, mint tudatos rövidítés.

### 3.3 Terminológia (5. ellenőrzés): mindkét új modell gyengén teljesít

GPT-4o-mini 6/20, Qwen3.7 Flash szintén 6/20 RENDBEN (a korábbi három
modell 10-18/20 közötti tartományban volt) -- ez összefügghet a 3.1/3.2
pontban leírt tartalom-kihagyással: ha egy terminológiai kifejezés éppen a
kihagyott/csonkolt szakaszban lett volna, a rövidítés-feloldás sem
ellenőrizhető sikeresként.

## 4. Következtetés (nem végleges modellválasztás, csak mérési tény)

- A **Gemini 3.1 Flash Lite** a hat modell közül a legjobb ár/teljesítmény
  arányú jelölt ezen a 20 elemű mintán: közel a legjobb átmenési arányhoz,
  töredék áron.
- A **GPT-4o-mini** ezen a feladaton (szótári szócikk szó szerinti,
  fejléccel együtti fordítása) nem alkalmas jelölt -- rendszeresen elhagyja
  a szócikk elejét, ami közvetlenül sérti a hűségi szabályt.
- A **Qwen3.7 Flash** a legolcsóbb, de a hosszabb görög tokenek
  csonkolása miatt megbízhatósági kockázatot jelent.
- Ez a kör nem érinti az eredeti FP0-FP4 (`m1`-`m3`) eredményeit vagy a
  brief döntési szabályát (§1) -- a hivatalos FP5/FP6 (vak bírálat,
  modellválasztási javaslat) továbbra is a brief szerinti 3 modellre
  vonatkozik, hacsak a felhasználó másként nem dönt.
