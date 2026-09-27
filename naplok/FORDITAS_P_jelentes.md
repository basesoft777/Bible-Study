# FORDITAS_P_jelentes -- FP4 zárójelentés

*FORDITAS_PILOT_BRIEF.md v1, 1. menet (FP0-FP4) · 2026.09.26 · ág:
`claude/forditas-pilot-brief-3afbbf-37c8ky` · modellek: m1=DeepSeek V4 Flash
(`deepseek/deepseek-v4-flash`), m2=Gemini 3.8 Flash (`google/gemini-3.8-flash`),
m3=Claude Haiku 4.5 (`anthropic/claude-haiku-4.5`)*

## 1. Költség modellenként

| Modell | Költség (USD) | Sikeres hívás/darab |
|---|---:|---:|
| DeepSeek V4 Flash | 0,0148 | 33 |
| Gemini 3.8 Flash | 0,6072 | 33 |
| Claude Haiku 4.5 | 0,2293 | 33 |
| **Összesen** | **0,8514** | **99** |

A G7 2 USD-s plafonja alatt (42,6%-on állt meg a futás). A Gemini költsége
azért ugrik ki nagyságrendekkel a DeepSeekhez képest, mert a `google/gemini-
3.8-flash` a gondolkodást (reasoning) NEM engedi kikapcsolni ("Reasoning is
mandatory for this endpoint and cannot be disabled." -- HTTP 400 kísérletnél
igazolva); a másik két modellnél a gondolkodás ki volt kapcsolva, mert a
fordítási feladat nem igényel többlépéses következtetést.

## 2. Gépi átmenési arány (SS1 hét ellenőrzése, `FORDITAS_P4_ellenorzes.tsv`)

Az 1., 2., 3., 4., 5., 7. ellenőrzés RENDBEN/SÉRTÉS/HIBA (pass/fail); a 6.
(hosszarány) a brief szerint csak jelzés, nem számít az arányba.

| Modell | RENDBEN | SÉRTÉS | HIBA | Átmenési arány |
|---|---:|---:|---:|---:|
| Gemini 3.8 Flash | 109 | 11 | 0 | **90,8%** |
| DeepSeek V4 Flash | 103 | 17 | 0 | **85,8%** |
| Claude Haiku 4.5 | 97 | 17 | 6 | **85,1%** |

Egyik modell sem éri el a FP6 döntési szabályában rögzített ≥95%-os
küszöböt -- ez a 2. menet (FP6) döntésébe tartozó megállapítás, itt csak a
mérés.

### 2.1 Ellenőrzésenkénti bontás

| Ellenőrzés | DeepSeek | Gemini | Claude Haiku |
|---|---|---|---|
| 1. görög/héber szakasz | 17 RENDBEN / 3 SÉRTÉS | 15 RENDBEN / 5 SÉRTÉS | 14 RENDBEN / 5 SÉRTÉS / 1 HIBA |
| 2. fejezet:vers számpár | 18 RENDBEN / 2 SÉRTÉS | 19 RENDBEN / 1 SÉRTÉS | 18 RENDBEN / 1 SÉRTÉS / 1 HIBA |
| 3. Károli-rövidítés | 15 RENDBEN / 5 SÉRTÉS | 18 RENDBEN / 2 SÉRTÉS | 17 RENDBEN / 2 SÉRTÉS / 1 HIBA |
| 4. formázás/betoldás | 20 RENDBEN | 19 RENDBEN / 1 SÉRTÉS | 19 RENDBEN / 1 HIBA |
| 5. terminológia (G5) | 13 RENDBEN / 7 SÉRTÉS | 18 RENDBEN / 2 SÉRTÉS | 10 RENDBEN / 9 SÉRTÉS / 1 HIBA |
| 6. hosszarány (jelzés) | 19 RENDBEN / 1 JELZÉS | 20 RENDBEN | 19 RENDBEN / 1 HIBA |
| 7. JSON-séma | 20 RENDBEN | 20 RENDBEN | 19 RENDBEN / 1 HIBA |

## 3. Hibatípusok

### 3.1 Tartós hiány: G1941 (arany) + Claude Haiku

Három egymást követő kísérlet (60, majd 120 másodperces faliora-határidővel,
illetve egy 400 másodperces külön diagnosztikai híváskor) sem hozott
felhasználható eredményt: a hívás HTTP 200-at ad, de a diagnosztikai
kísérletnél 310 másodperc után `finish_reason=error` mellett a mondat
közepén megszakadt, érvénytelen tartalommal. Ez a mintánk legnagyobb
egy-darabos promptja (~7880 karakter a teljes terminológiai és
Károli-melléklettel együtt) -- a jelenség ennek a modell+prompt-méret
kombinációnak tűnik sajátjának. A K5 szabály szerint dokumentált hiányként
kezelve, a 4. menetbeli feldolgozásból (FORDITAS_P4_vak.md) ez a pár
kimarad.

### 3.2 DeepSeek: csendes, tartalmi csonkolás tiszta API-válasz mellett

A `G1941` DeepSeek-fordítása -- amely SIKERES hívásként került be a
kimenetbe (`finish_reason=stop`, érvényes JSON) -- a forrás kb. felénél
megszakad, befejezetlen mondattal (hosszarány 0,32, messze a 0,8-1,6 sávon
kívül -- l. a 6. ellenőrzés JELZÉSe). Ezt a fordit.py jelenlegi hibaészlelése
NEM szűri ki, mert a modell szintaktikailag érvényesen zárta le a JSON-t --
csak az 1-2. ellenőrzés (görög/héber és versszám-multihalmaz) buktatja meg
utólag, nagy hiánylistával. **Ez fontos módszertani tanulság**: a
`finish_reason` és az érvényes JSON önmagában nem garantálja a
teljességet -- egy hosszúság-/teljesség-ellenőrzés (mint a SS1 6. pontja)
nélkülözhetetlen kapu, nem csak "jelzés".

### 3.3 DeepSeek: Károli-rövidítés elhagyása hosszú szócikk közepén

A `G0994`, `G3777` és `G4151` szócikkeken a DeepSeek néhol visszaesik az
angol/Thayer-stílusú rövidítésre (`Act`, `Mat`, `Mar`, `Joh`, `Jn`) a Károli-
alak (`ApCsel`, `Mt`, `Mk`, `Ján`) helyett -- jellemzően a hosszabb
szócikkek későbbi hivatkozásainál. A Gemini és a Claude Haiku ugyanezen
szócikkeken nem mutatta ezt a mintát.

### 3.4 Terminológia (G5): valódi elhagyások és egy módszertani határeset

A leggyakoribb valódi hiány a `p.` -> `o.` (oldal) rövidítés-feloldás
elmaradása (mindhárom modellnél előfordul), ill. elszórtan `Sept.` ->
`Septuaginta`, `see` -> `l.`, `i. e.` -> `azaz`. Egy tétel -- `Heb.` ->
`héb.` -- módszertanilag félrevezető volt: a `G0282` forrásában a `Heb.`
NEM a "héber (nyelv)" rövidítése, hanem egy tudományos hivatkozás
könyvcíme ("Bleek on Heb. vol. ii." = Bleek kommentárja a Zsidókhoz írt
levélről) -- ezt mindhárom modell helyesen, változatlanul hagyta, az
ellenőrző szkript viszont (jogosan, az egyetlen aranypéldányból származó
G5-szabály alapján) SÉRTÉSként jelezte. **Tanulság a 4a/S2 tervezéséhez**:
a `Heb.` rövidítés kétértelmű Thayer rendszerében (nyelv vs. könyvcím), ezt
a terminológiai táblának kontextus szerint kellene kezelnie, nem egyetlen
statikus megfeleltetéssel.

### 3.5 Az ellenőrző szkript ismert korlátai (átláthatóság kedvéért)

- **Nem-bibliai, kettőspontos hivatkozások** (pl. "Klotz ad Devar. 2:2",
  "Lob. Path. Element. 2:6") tudományos apparátus-idézetek, amelyeket a 3.
  ellenőrzés (Károli-rövidítés) tévesen könyv-rövidítésként azonosít --
  mindhárom modellnél egyformán jelentkezik, tehát nem modellek közti
  különbségtétel, hanem a checker maga hamis pozitívja. `Devar` és `Element`
  ezért NEM modell-hiba.
- **Apokrif/deuterokanonikus könyvek** (Bölcsesség, Sirák, Makkabeusok,
  Báruk): a Károli-Biblia nem tartalmazza őket, tehát nincs hivatalos
  rövidítésük -- a szkript egy kivétellistával (angol/latin ÉS magyar
  alakok) kezeli ezeket, nem SÉRTÉSként.
- **Görög ékezet-eltolódás**: a görög szóvégi ékezet a mondatbeli
  pozíciótól függően törvényszerűen változik (oxeia/baria) -- az 1.
  ellenőrzés emiatt NFD-bontás után eltávolítja a nem-szóköz jelölőket
  (ékezet, lehelet) az összehasonlítás előtt, hogy ez ne adjon hamis
  SÉRTÉS-t.
- **4. ellenőrzés (betoldás)**: a zárójel-számlálás durva proxy -- egyetlen
  találat (`G4151`, Gemini, 151 vs. 150 nyitó zárójel egy 12 darabra bontott,
  23 705 karakteres szócikkben) valószínűleg nem tartalmi betoldás, hanem a
  darabolás miatti stilisztikai véletlen; emberi átnézést igényel, nem
  automatikusan eldönthető.

## 4. Elfogadási kapu (K1-K6)

| # | Feltétel | Eredmény |
|---|---|---|
| K1 | `git diff --stat 72b200c..HEAD`: csak a brief, `fordit.py`, `naplok/FORDITAS_P*` | ✔ (l. lent, 15+6 fájl, mind a megengedett körben) |
| K2 | `eszkozok/ellenoriz.py`: RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 | ✔ változatlan |
| K3 | a kulcs sehol nem jelenik meg | ✔ (`grep` a teljes repón, nincs találat) |
| K4 | a költségnapló összege ≤ 2 USD, egyezik a kimenettel | ✔ 0,8514 USD; a 100 sor (99 hívás/darab + fejléc) közül 98 sikeres darab-hívás fedi le mind az 59 sikeres (szócikk, modell) kimenetet, 1 sor (`G1941`+Claude Haiku, 0 USD) a dokumentált hibás kísérlet |
| K5 | a 20×3 kimenet mindegyike megvan, vagy a hiány oka a jelentésben | ✔ 59/60, l. 3.1 |
| K6 | minden szám fájlból írt szkriptből; nincs `csv` modul; héber/görög szöveg csak fájlból | ✔ |

## 5. Összegzés (nem FP6 döntés, csak mérési tény)

- A Gemini 3.8 Flash érte el a legmagasabb gépi átmenési arányt (90,8%),
  de a DeepSeek 41×-ese a költsége -- ha a gondolkodás kikapcsolása
  élesben is lehetséges lenne nála, valószínűleg drasztikusan olcsóbb
  lenne.
- A DeepSeek a legolcsóbb, de két súlyos, egymástól független
  megbízhatósági problémát mutatott ezen a 20 elemű mintán: néma tartalmi
  csonkolást (G1941) és Károli-rövidítés-visszaesést hosszú szócikkeknél
  (G0994, G3777, G4151).
- A Claude Haiku egyetlen (de a legnagyobb egy-darabos promptra eső)
  hívása tartósan nem hozott érvényes választ.
- A végleges modellválasztási javaslat (a §1 döntési szabálya szerint) a
  2. menet FP6 tételében készül, a vak bírálat (FP5) pontjaival együtt.
