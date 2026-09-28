# FP2 — 7. lépés: költségbecslés a teljes Thayerre

*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 7. lépés, a felhasználó jóváhagyott javításaival
(2026.09.28). Szkriptek: `fp2/koltsegbecsles.py`, `fp2/apparatus_elemzes.py`.*

## Módszertan

- **Korpusz:** `konkordancia/Thayer_teljes.tsv` — 5426 szócikk, 4 440 084 karakter.
- **API-hívások száma:** a `fordit.py` saját darabolása (`darabokra_bont`,
  `DARAB_HATAR=4000`) szerint a teljes korpuszon **6433 hívás** (153 szócikk igényel
  darabolást, 1160 hívással, 1 331 015 karakteren; 5273 szócikk egy hívásban megy,
  3 109 069 karakteren). *Ez egyezik a `FORDITAS_ELES_THAYER_BRIEF.md` saját, független
  6433-as becslésével — kereszt-ellenőrzött szám.*
- **Bemenet-token modell:** lineáris regresszió (`bemenet_token = overhead + b ×
  forráskarakter`) a 25 egy-darabos mintaszócikken, modellenként. A **fix rész
  (utasítások + terminológia + Károli-tábla) ≈ 3700–3800 token/hívás**, ami a
  **bemenet ~92%-a**, de — mivel a kimenet ára jóval magasabb tokenenként, és a kimenet
  a teljes hívásköltség jelentős hányada — **a teljes (bemenet+kimenet) költségnek csak
  ≈ 62%-a** (Gemini-nél pontosan 62,2%).
- **Kimenet-token modell:** kimenet_token / forráskarakter arány, **csak a "egészséges"
  (nem kritikus) mintaelemeken** mérve — ez a "ha megfelelően működik" várható arány,
  nem a ténylegesen megfigyelt (hibás/csonkolt) átlag.
- **p10–p90 sáv:** a mintabeli kimenet-arányok szórásából (a bemenet aránya
  stabilabb, ezért a sáv gyakorlatilag a kimenet-bizonytalanságot tükrözi).

## Árlista (OpenRouter, 2026.09.28)

| Modell | Bemenet USD/1M | Kimenet USD/1M | Cache-olvasás USD/1M |
|---|---:|---:|---:|
| Gemini 3.1 Flash Lite | 0,25 | 1,50 | 0,025 (90% kedvezmény) |
| DeepSeek V4 Flash | 0,14 | 0,28 | 0,028 (80% kedvezmény) |
| MiniMax M3 | 0,30 | 1,20 | 0,06 (80% kedvezmény) |

**Tényleges háttér-szolgáltató:** a FP2 futásból **nem rögzíthető** (a `fordit.py`
eldobja a nyers választ, csak a `usage`-et menti). Egy külön, egyszavas tesztlekérdezés
(`deepseek/deepseek-v4-flash`, ezen a napon) a válasz `provider` mezőjében **"Venice"**-t
adott — ez megerősíti, hogy az OpenRouter több háttér-szolgáltató között routol egy
modellazonosító mögött, de **nem bizonyítja**, hogy a FP2 4. lépésének hívásai is ott
futottak. Rögzítés a `#7` előtt szükséges (l. lent).

## Költségtábla — teljes Thayer (USD)

| # | Forgatókönyv | Alapár (p10–p90 sáv) | Ár ×2 |
|---|---|---:|---:|
| 1 | Csak Gemini 3.1 Flash Lite | **9,58** (6,55–10,93) | 19,16 |
| 2 | Csak DeepSeek V4 Flash | 4,25 (3,94–4,39) | 8,50 |
| 3 | Csak MiniMax M3 | 10,91 (10,47–11,62) | 21,82 |
| 4a | Gemini + 1× Gemini-önújrapróba (~3% hibaarány) | 9,87 | 19,74 |
| 4b | Gemini (mind) + MiniMax tartalék **csak a nem darabolt szócikkeken, csak ha a Gemini hibázik** (4%-os Gemini-hibaarány a nem darabolt mintán) | 9,92 | — |
| 5 | Gemini + prompt-cache (a fix overhead 90%-os OpenRouter-kedvezménnyel) | 4,22 | 8,44 |
| **6** | Gemini + apparátus-helyőrzők (**becsült, nem tesztelt**; l. lent, mi a 25,1%) | 8,67 | — |
| **7** | **Gemini + prompt-cache + 1× önújrapróba (~3%)** | **4,35** (1,23–5,73) | **8,70** |

**4a vs. 4b:** a két felállás gyakorlatilag egyenértékű (9,87 vs. 9,92 USD, 0,5%
eltérés) — a MiniMax-tartalék bevezetése **nem éri meg a komplexitását**, elég az
egyszerű Gemini-önújrapróbát (4a) tervezni.

**A 6. sor 35%→25,1%-os javítása:** az eredeti "leválasztható apparátus" mérés
(`fp2/apparatus_elemzes.py`) három, egymást átfedő kategóriát egyesített: zárójeles
szakaszok (23,4%), igehely-hivatkozások (12,7%), kritikai-apparátus sziglák (0,6%) —
egyesítve 35,0%. **Ebből ≈9,9 százalékpont olyan zárójeles/igehely-szakasz volt, amely
görög vagy héber betűs szöveget is tartalmazott** (pl. `(ἐπιστραφήτω ψυχή τοῦ παιδαρίου,
1Ki 17:21)`) — ezeket **ki kellett venni**, mert a görög/héber idézet szó szerinti
megőrzése a fordítás egyik legszigorúbb, nem sérthető szabálya (`adat/SEMA.md` 2.5,
prompt v2/v3 szabályai), tehát **nem tehető placeholder mögé** anélkül, hogy a modell a
tényleges görög/héber karaktereket látná. A görög/héber-mentes, valóban leválasztható
rész: **25,1%** — ez adja a 6. sor 8,67 USD-s (nem 8,31 USD-s) becslését. Mivel a
teljes költség 62%-a fix overhead (nem forrásarányos), a forrás 25%-os csökkentése is
csak **≈9,5%-os** teljes megtakarítást hoz — **jóval kisebb, mint a cache-forgatókönyv
(5/7) ≈55%-os megtakarítása**, mert az apparátus-leválasztás a rossz (kicsi súlyú)
komponensre hat.

## A plafonhoz képest

**A tervezett plafon 15 USD** (`FORDITAS_ELES_THAYER_BRIEF.md`). **Minden alapár-
forgatókönyv belefér** (a legdrágább, a csak-MiniMax, is 10,91 USD). Az **ár ×2
érzékenység viszont a Gemini- és MiniMax-forgatókönyveket (1, 3, 4a, 4b) 15 USD fölé
tolja** (19–24 USD) — ez reális kockázat, mert a DeepSeek ára a kor2 óta ténylegesen
~3×-ára nőtt. **A cache-alapú forgatókönyvek (5, 7) ár ×2 mellett is a plafonon belül
maradnak** (8,44 / 8,70 USD) — ez a legfontosabb érv a 7. forgatókönyv mellett.

## Javasolt forgatókönyv: 7 (Gemini + prompt-cache + 1× önújrapróba)

Négy feltétel teljesítendő a `#7` (éles Thayer-fordítás) indítása előtt — l. a
jelentés "javítandó a #7 előtt" szakaszát.
