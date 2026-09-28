# FP2 — kapu-kereszttellenőrzés és darabolás-elemzés (a kulcs felnyitása előtt/után)

*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, a felhasználó 2026.09.28-i kiegészítő kérése,
a 6. lépés (⛔) után, a kulcs felfedése előtt/közben. Szkriptek: `fp2/kapu_keresztellenorzes.py`,
`fp2/biralat_modellek.py`.*

## 1. A gépi kapu (`fp2/kapuk.tsv`) — mit jelzett és mit nem

A 30 szócikk × 3 modell = 90 kimenetből **21 kritikus hibát** találtam a vak bírálatban
(14 DeepSeek, 6 MiniMax, 1 Gemini — l. lent). Ezek közül a gépi kapu (1–7. ellenőrzés,
`naplok/FORDITAS_P4_ellenoriz.py`-ből importálva) **20-at jelzett** (a görög/héber
token-egyezés (1), a versszám-egyezés (2), a terminológia (5) vagy a Károli-rövidítések
(3) ellenőrzésén SÉRTÉS-sel), és **1-et nem jelzett**:

- **Nem jelzett kritikus hiba:** `G1106`, **Gemini 3.1 Flash Lite** — a forrás `Phi 1:14`
  hivatkozását `Filem 1:14`-re fordította (Filippi helyett Filemon). A kapu mind a 7
  ellenőrzésen RENDBEN-t adott, mert (a) a 2. ellenőrzés (`VERS_MINTA = \d{1,3}:\d{1,3}`)
  csak a szám:szám mintát nézi, a könyvnevet nem; (b) a 3. ellenőrzés csak azt nézi, hogy
  a használt rövidítés **szerepel-e** a Károli-rövidítéslistában — azt nem, hogy az adott
  vershez **a helyes** rövidítés-e. A "Filem" önmagában érvényes Károli-rövidítés, csak
  rossz könyvre. **Ez valódi rés a gépi kapuban**, amit a jelentésben (8. lépés) jelzek.

Minden más kritikus eset (DeepSeek csonkolásai, MiniMax betoldásai/nem-fordításai) a
kapun legalább egy ellenőrzésen elbukott.

## 2. A `fordit.py` darabolása

`DARAB_HATAR = 4000` karakter (`eszkozok/fordit.py`). A `darabokra_bont()` a forrás
**saját** `1.`, `2.` … és `a.`, `b.` … tagolásán vág (a nyelvtani `1 aorist`-féle
sorszámokat kizárva egy guard-dal), csak akkor tördel mondathatáron, ha a fenti nem elég
kicsi darabokhoz. A 30 mintaszócikkből **5 igényelt darabolást**: `G0026` (3), `G0266`
(5), `G1343` (6), `G4151` (12), `G5590` (3). A többi 25 egyetlen hívásban ment.

**Kulcsfontosságú tény:** minden darab **önálló, állapot nélküli API-hívásban** megy —
a modell **csak az adott darab forrásszövegét** kapja, plusz egy megjegyzést
(`darab_info_szoveg`: *"(3/12. rész — csak ezt a részt fordítsd önmagában álló
szövegként; a folytatás külön hívásban érkezik, NE told ki a hiányzó résszel, és ne
jelezd a szöveg részlegességét)"*). **Nem kapja meg** sem az előző darab angol forrását,
sem annak magyar fordítását. A `fordit.py` a kész darabfordításokat egyetlen szóközzel
fűzi össze (`' '.join(darab_forditasok)`).

**Ellenőrzés, hogy a hézagok/ismétlődő fejlécek darabhatáron vannak-e:** a `G4151`
(MiniMax, 12 darab) kimenetében talált 9 ismétlődő "G4151 —" fejléc pozíciója
(karakterben: 8, 137, 1039, 5050, 6007, 9985, 13710, 17806, 19437) **szorosan illeszkedik**
a forrás darabhatáraihoz (kumulatív hossz: 0, 123, 851, 4686, 6885, 7404, 11141, 14666,
18640, …) — vagyis a modell **minden egyes önálló darab-hívásnál újra kimondta a
fejlécet/nyelvtani apparátust**, mintha új szócikket kezdene, ahelyett hogy folytatná az
előzőt. Ugyanez a mintázat a `G0026`, `G0266`, `G1343` kitalált-tartalmú kimeneteinél is:
**mindegyik darabolt szócikk volt** (l. lent).

**A DeepSeek csonkolása viszont NEM darabolás-függő**: `G0994` (661 kar., 1 darab),
`G1311` (787 kar., 1 darab) és `G2672` (1025 kar., 1 darab) — mind **egyetlen hívásban**
mentek, mégis súlyosan csonkoltak. A DeepSeek csonkolása tehát **általános, a hossztól
függő degradáció**, nem a darabolási mechanizmus mellékhatása.

## 3. A kulcs felfedése és modell szerinti bontás

**Önjavítás a szúrópróba alapján:** a `fp2/szuroproba.md`-t egy chat-menet pontozta (nem
a felhasználó személyesen — ezt itt és a döntésnaplóban is így jelölöm). A `G0266`
DeepSeek-kimenetét (akkor "A" címkén) a chat 1/10-re, én korábban 7/10-re ("mérsékelt
kihagyás") pontoztam — a tényleges hosszarány (0,42, azaz 58% hiányzik,
`fp2/kapu_keresztellenorzes.py`) a chat ítéletét igazolja. Javítottam
(`fp2/biralat_adatok.py`, `kihagyas` → `kihagyas(kritikus)`), és az alábbi táblázat már
a javított adatot tükrözi.

| Modell | Teljes 30 szócikk (átlag/10, kritikus%) | **Nem darabolt** 25 szócikk | **Darabolt** 5 szócikk |
|---|---:|---:|---:|
| Google Gemini 3.1 Flash Lite | 9,67 (3%) | 9,60 (4%) | **10,00 (0%)** |
| MiniMax M3 | 7,47 (23%) | 8,32 (12%) | **3,20 (80%)** |
| DeepSeek V4 Flash | 5,93 (50%) | 6,44 (44%) | **3,40 (80%)** |

**A darabolás önmagában nem magyarázza a DeepSeek gyengeségét** (44% kritikus a nem
darabolt mintán is), **de drámaian megmagyarázza a MiniMax problémáját**: a nem darabolt
szócikkeken a MiniMax a **második legjobb** (8,32, 12% kritikus — versenyképes a
Geminivel), miközben a darabolt szócikkeken **ugyanolyan rossz, mint a DeepSeek**
(mindkettő 80% kritikus, 4/5 szócikk). A MiniMax hibamódja a darabolt szócikkeken tehát
nem véletlenszerű minőségromlás, hanem **rendszeres**: minden egyes önálló darab-hívásnál
újraindítja/kitalálja a fejlécet és a tudományos apparátust, amikor a darab önmagában
nem elég kontextus egy "teljes" szócikk érzetének keltéséhez — feltehetően a modell saját
(betanítási) tudásából egészíti ki, amit a forrás abban a darabban nem tartalmaz. A
DeepSeek darabolt szócikkeken mutatott gyengülése (80%) ugyanakkor **konzisztens** a nem
darabolt mintán mért gyengeségével (44%) — nála a darabolás legfeljebb súlyosbító, nem
kiváltó tényező.

### Kritikus hibák modellenként (a teljes 30 szócikken)

**DeepSeek V4 Flash — 14/30 kritikus, mind kihagyás (csonkolás), 3 darabolt szócikken is:**
G0012, G0086 (parafrazált/bővített, nem hű), G0994, G1311, G1941 (az ARANY-cikk),
G2672, G3777, G4151*, G5010, G5351, G5356, G5590*, G0026*, G5013
*(csillaggal a darabolt szócikkek)*

**MiniMax M3 — 7/30 kritikus:**
- nem-fordítás (a forrás angolul maradt): G0002, G1944, G5013 — mind **nem darabolt**
- kitalált tartalom betoldása: G4151*, G0026*, G0266*, G1343* — **mind darabolt**

**Google Gemini 3.1 Flash Lite — 1/30 kritikus:**
G1106 — "Filem 1:14" tévesen "Fil 1:14" helyett (nem darabolt).

## 3b. A szúrópróba és a vak bírálat összevetése

A `fp2/szuroproba.md`-t **egy chat-menet pontozta, nem a felhasználó személyesen** — ezt
a felhasználó kifejezetten kérte jelölni. A chat 0–10 skálán pontozott és "legjobb"
címkét adott, a kulcs ismerete nélkül.

| Szócikk | A=modell / B=modell / C=modell | Chat (A/B/C, legjobb) | Az én vak pontszámom (osszesen, A/B/C) | Egyezés |
|---|---|---|---|---|
| G0004 | gemini / deepseek / minimax | 9 / 8 / 5, A | 10 / 10 / 7 | irány egyezik |
| G0813 | minimax / deepseek / gemini | 8 / 8 / 8,5, C | 10 / 9 / 10 | irány egyezik (mind jó) |
| G1941 | gemini / minimax / deepseek | 9 / 7 / 1, A | 10 / 6 / 1 | **jó egyezés** |
| G0086 | gemini / deepseek / minimax | 8,5 / 2 / 8, A | 10 / 3 / 10 | **jó egyezés** (B/deepseek mindkettőnél rossz) |
| G5590 | deepseek / minimax / gemini | 0,5 / 5 / 8,5, C | 1 / 7 / 10 | irány egyezik |
| G2105 | deepseek / gemini / minimax | 8,5 / 8 / 9, C | 10 / 10 / 10 | egyezik (nincs hiba) |
| G3687 | minimax / deepseek / gemini | 8 / 7,5 / 8,5, C | 10 / 10 / 10 | egyezik (nincs hiba) |
| G0266 | deepseek / gemini / minimax | 1 / 8,5 / 0,5, B | 3\* / 8 / 2 | **javítva** (l. fent, A eredetileg 7 volt) |

7/8 szócikkön jó/irány-egyező a két független pontozás; a 8. (`G0266`) eltérést a fenti
javítás oldotta fel. Ez megerősíti a vak bírálat megbízhatóságát, és megmutatja a
szúrópróba tényleges hasznát (önellenőrzés, nem csak a felhasználói ítélet mérése).

## 4. Prompt v3-javaslatok a jelentésbe (a felhasználó kérése, NEM futtatva)

- „f”/„ff” (Winer/oldalhivatkozás utáni angol jelölés) → magyar „k”/„kk” (pl. „305ff” →
  „305kk”), következetesen.
- Szerzőnevek egységesítése (pl. Aeschylus/Aischülosz, Thucydides/Thuküdidész — jelenleg
  szócikkenként és modellenként eltér).
- A „p. … middle” (oldal + pozíció, pl. „p. 234{b} middle”) egyértelműen oldalon belüli
  pozícióhivatkozásként kezelendő, ne maradjon tagolatlanul.
