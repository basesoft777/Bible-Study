# FP2_jelentes — Thayer-stíluspróba: Gemini 3.1 Flash Lite, DeepSeek V4 Flash, MiniMax M3

*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 8. lépés · 2026.09.28 · ág:
`claude/thayer-stilusproba-fp2` · alap: `main` (`8f5a1eb`, tartalmazza a #3-at)*

## 1. Összefoglaló

A **Gemini 3.1 Flash Lite** egyértelműen a legjobb: 9,67/10 átlag, 3% kritikus hiba,
gyakorlatilag hibátlan a darabolt (hosszú) szócikkeken is. A **DeepSeek V4 Flash**
súlyosan visszaesett a kor2 óta (8,60→5,93, 50% kritikus, gyakran csonkol) — az ok
valószínűleg **nem** a v3 prompt/terminológia, hanem a kor2 óta ~3×-osára nőtt
OpenRouter-ár mögötti szolgáltatóváltás (nem mért tény, következtetés). A **MiniMax M3**
a nem darabolt szócikkeken versenyképes (12% kritikus), de a **darabolt** szócikkeken
**kitalált tartalmat told be** (hamis hivatkozások, hamis szegmentálás) — ugyanolyan
rossz, mint a DeepSeek (80% kritikus). **Javasolt felállás: Gemini 3.1 Flash Lite,
prompt-cache-sel és egyszeri önújrapróbával (7. forgatókönyv), ≈4,35 USD becsült
teljes költséggel (8,70 USD duplázott ár mellett is a 15 USD-s plafonon belül).**
A v3 stílus megtartotta/javította a minőséget (l. 3. pont). Négy tétel javítandó a
#7 (éles Thayer-fordítás) indítása előtt (l. 6. pont).

## 2. Pontszámok modellenként

*(0–10 skála, kor2-rubrika: pontosság/terminológia/magyar/formai; a "kritikus" =
kihagyás, félrefordítás vagy betoldás — l. `fp2/biralat_vegleges.tsv`)*

| Modell | Átlag | Medián | Természetesség átlag | Kritikus hiba |
|---|---:|---:|---:|---:|
| Gemini 3.1 Flash Lite | 9,67 | 10,0 | 7,70 | 1/30 (3%) |
| MiniMax M3 | 7,47 | 9,5 | 6,00 | 7/30 (23%) |
| DeepSeek V4 Flash | 5,93 | 5,5 | 4,87 | 15/30 (50%) |

**Bontás a kor2-minta és az új minta szerint**, és **darabolt/nem darabolt** szerint —
ez utóbbi a fontosabb (l. `naplok/FP2_kapu_es_darabolas_elemzes.md` 3. pontja):

| Modell | Nem darabolt (25 szócikk) | Darabolt (5 szócikk) |
|---|---:|---:|
| Gemini 3.1 Flash Lite | 9,60 (4% kritikus) | **10,00 (0% kritikus)** |
| MiniMax M3 | **8,32 (12% kritikus)** | **3,20 (80% kritikus)** |
| DeepSeek V4 Flash | 6,44 (44% kritikus) | 3,40 (80% kritikus) |

A MiniMax nem darabolt szócikkeken a Geminivel versenyképes; darabolt szócikkeken a
DeepSeekkel egyformán rossz — a hibája **rendszeresen a darabolási mechanizmushoz
kötött** (minden önálló darab-hívásnál újrakezdi/kitalálja a fejlécet és a tudományos
apparátust). A DeepSeek gyengesége **darabolástól függetlenül** is fennáll.

**Kritikus hibák típus szerint** (mind a 90 kimeneten, 21 eset — a G0266 önjavítás
után, l. 7. pont):
- **DeepSeek — 15 eset, mind kihagyás (csonkolás).** A 4 legrövidebben csonkolt
  kimenetet explicit `max_tokens=8000`-rel újrafuttatva mind a 4 teljes, hű fordítást
  adott (0,0018 USD) — ez a DeepSeek megbízhatatlanságára utal, **nem** paraméterhibára
  (**következtetés, nem mérés**: a `finish_reason` nem `length` volt egyik esetben sem —
  a `fp2/_run/hibak/` könyvtár üres, és a `completion_tokens` értékek nem kerek/plafon-
  szerűek).
- **MiniMax — 7 eset:** 3 esetben a szócikket **egyáltalán nem fordította le**
  (angolul maradt, nem darabolt szócikkeken), 4 esetben (mind darabolt szócikk)
  **kitalált, a forrásban nem szereplő tudományos apparátust** toldott be.
- **Gemini — 1 eset:** `G1106`-nál `Phi 1:14`-et `Filem 1:14`-re fordította
  (Filippi helyett Filemon) — a gépi kapu **nem** jelezte (l. 7. pont).

Ha a nyers válaszokban lenne rögzítve `finish_reason`, modellenkénti darabszámát meg
tudnánk adni — **ez nincs tárolva** a `fordit.py`-ban (l. 6. pont, "javítandó" lista).

## 3. Kor2 és FP2 összevetése (20 közös szócikk)

| Modell | kor2 (P6-jelentés) | FP2 (ugyanaz a 20) | Különbség |
|---|---:|---:|---:|
| Gemini 3.1 Flash Lite | 8,70 | 9,60 | **+0,90** |
| DeepSeek V4 Flash | 8,60 | 5,05 | **−3,55** |

**A Gemini javulása** (következtetés, nem mérés — a bíráló és a rubrika azonos volt
mindkét menetben): a prompt v3 #4 szabálya ("`from X down` → „X-tól kezdve”, soha
„lefelé”") közvetlenül a kor2-ben ismételten felrótt "lefelé" tükörfordítást javítja;
a terminológia v2 25 új sora (aorist→aorisztosz stb.) pontosan a kor2 vak bírálat
hibalistájából származik, és az FP2-ben következetesen megjelenik.

**A DeepSeek visszaesése** (következtetés, nem mérés) **nem** magyarázható a
prompt/terminológiával (bővítő jellegűek, nem okoznának rövidebb választ), sem a
bírálati szigorral (azonos bíráló, azonos rubrika, objektíven mérhető hosszcsonkolás),
sem a darabolással (a 20 közös szócikk közül egy sem igényelt volna darabolást a
kor2-mintában sem). A legvalószínűbb ok a **kor2 óta ~3×-osára nőtt OpenRouter-ár**
(`naplok/FP2_felmeres.md` 0.4) mögötti szolgáltató-/kvantálásváltás — ezt erősíti,
hogy egy tesztlekérdezés a `deepseek/deepseek-v4-flash` mögött **"Venice"**
szolgáltatót adott vissza (a `provider` mező létezik és élesben elérhető, de a FP2
4. lépése ezt nem rögzítette).

## 4. A vak szúrópróba (chat-pontozás) és a vak bírálat egyezése

**A `fp2/szuroproba.md`-t egy chat-menet pontozta, nem a felhasználó személyesen** — ezt
a felhasználó kifejezetten kérte jelölni. 8 szócikken (5 kor2 + 3 új) **7/8 esetben
jó/irány-egyező** a chat pontszáma és az én (kulcs nélküli) vak bírálatom. Az egyetlen
eltérés (`G0266`, DeepSeek-kimenet) **valódi hibát tárt fel** a saját bírálatomban: a
chat 1/10-re, én eredetileg 7/10-re ("mérsékelt kihagyás") pontoztam, holott a tényleges
hosszarány 0,42 (58% hiányzik) — javítva `kihagyás(kritikus)`-ra. Részletek:
`naplok/FP2_kapu_es_darabolas_elemzes.md` 3b. pont.

## 5. Költségtábla (jóváhagyott, `naplok/FP2_koltsegbecsles.md`)

| # | Forgatókönyv | Alapár (p10–p90) | Ár ×2 |
|---|---|---:|---:|
| 1 | Csak Gemini 3.1 Flash Lite | 9,58 (6,55–10,93) | 19,16 |
| 2 | Csak DeepSeek V4 Flash | 4,25 (3,94–4,39) | 8,50 |
| 3 | Csak MiniMax M3 | 10,91 (10,47–11,62) | 21,82 |
| 4a | Gemini + 1× Gemini-önújrapróba | 9,87 | 19,74 |
| 4b | Gemini + MiniMax tartalék (csak nem darabolt, csak hiba esetén) | 9,92 (≈4a) | — |
| 5 | Gemini + prompt-cache | 4,22 | 8,44 |
| 6 | Gemini + apparátus-helyőrzők (becsült, nem tesztelt) | 8,67 | — |
| **7** | **Gemini + prompt-cache + 1× önújrapróba** | **4,35 (1,23–5,73)** | **8,70** |

**A tervezett plafon 15 USD** — minden alapár belefér; az ár ×2 érzékenység a
Gemini/MiniMax-forgatókönyveket túltolja (19–24 USD), **de a cache-alapú
forgatókönyvek (5, 7) duplázott árnál is a plafonon belül maradnak.**

## 6. Javasolt döntés a #7-hez

**Fő fordító: Gemini 3.1 Flash Lite, prompt-cache-sel és egyszeri önújrapróbával
(7. forgatókönyv).** Tartalék: nincs szükség rá (a 4a/4b gyakorlatilag egyenértékű, az
egyszerűbb 4a/7 elég). **A MiniMax bekerülésének feltétele** (nem teljesült): a
darabolt szócikkeken mért kritikus-arány ≤ a Geminié (0%) — a MiniMax 80%-ot mért ott,
tehát **nem javasolt sem fő fordítóként, sem tartalékként**, amíg a darabolt-szócikk
hibáját (kitalált tartalom) meg nem oldják (pl. a darabok közötti kontextus átadásával).
**A `#7`-brief v3-ra frissítése szükséges** (prompt v3 stílusblokkja, terminológia
v2+kiegészítés).

### Javítandó a `#7` (éles Thayer-fordítás) indítása előtt

1. **Cache-jelzés a `fordit.py`-ban** — a fix overhead (utasítás+terminológia+Károli-
   tábla) explicit cache-töréspontként küldése, hogy az 5/7. forgatókönyv megtakarítása
   ténylegesen realizálódjon.
2. **Provider-rögzítés** — a nyers válasz `provider` mezőjének mentése minden híváshoz
   (jelenleg eldobásra kerül), hogy a jövőbeli ár-/minőségváltozások szolgáltatóhoz
   köthetők legyenek.
3. **Könyvnév-egyezés ellenőrzése** — a gépi kapu (3. ellenőrzés) jelenleg csak azt
   nézi, hogy a használt Károli-rövidítés *létezik-e*, nem azt, hogy *a helyes
   könyvre* utal-e (l. a `Phi`→`Filem` eset).
4. **Fordítatlan szöveg ellenőrzése** — egyik jelenlegi ellenőrzés sem veszi észre, ha
   a modell a forrást változatlan hosszal és görög/héber tartalommal, de **le nem
   fordítva** adja vissza (l. `G1944`, `G5013` MiniMax-esetek).
5. **Egyszeri önújrapróba** — a G6 önjavító hurok (a `FORDITAS_ELES_THAYER_BRIEF.md`-ben
   már tervezve) bevezetése, mert a DeepSeek/MiniMax csonkolásainak egy része (l. 2.
   pont, `max_tokens` teszt) újrafuttatással megoldódik.

## 7. Talált hibák a `#3` eszközeiben

**`eszkozok/fordit.py` `tsv_ir`/`tsv_sorok` — sértett TSV embedelt sortöréssel.** A
kimeneti TSV (a `naplok/FORDITAS_P3_kimenet.tsv` sémája) sérül, ha egy `forditas_hu`
mező szó szerinti sortörést tartalmaz (a JSON-válaszból escapelt `\n`, amit a
`json.loads` valódi sortöréssé alakít) — a `tsv_sorok` ekkor kettévágja a sort
olvasáskor. **Nem javítottam** (a brief tiltja); az FP2 a gyorsítótár (JSON, nem
sérült) alapján állította helyre a kimenetet (`fp2/rendezo.py`). Részletek:
`naplok/FP2_felmeres.md`.

**Gépi kapu (`naplok/FORDITAS_P4_ellenoriz.py`) — strukturális rések** (l. 6. pont
3–4. tétele): a könyvnév-egyezés és a fordítatlanul hagyott szöveg egyik ellenőrzésen
sem bukik el.

## 8. Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | A brief alapja `main` (`8f5a1eb`), nem a megnevezett, már törölt `claude/forditas-pilot-brief-3afbbf-37c8ky` ág — az PR #62-ként már be van olvasztva | a névre keresett ág törölve, a tartalma a main-ben van |
| D2 | A prompt v2/terminológia v2 a felhasználó által csatolt `FORDITAS_ELES_THAYER_BRIEF.md` E1 tételéből épült fel, mert a repóban nem léteztek | a brief explicit ezt írta elő |
| D3 | `fordit.py` additív kapcsolók (`--prompt-fajl`, `--terminologia-fajl`, `--kimenet-dir`, `max_tokens`, `idotartam_mp`) — alapértelmezésben változatlan viselkedés | a `FORDITAS_ELES_THAYER_BRIEF.md` E1 tétele ugyanezt tervezte; enélkül a saját futás felülírta volna a kor2 pilot fájljait (ez egyszer meg is történt egy tesztnél, visszaállítva) |
| D4 | A `G1941` (arany) a mintában maradt és újra lefordíttattuk mindhárom modellel (nem lett kihagyva a G7-szabály szerint), mert a brief az arannyal való összevetésre szánta | brief 2. lépés |
| D5 | A 3. lépés (terminológia-kiegészítés) csak az FP2 próbára vonatkozik, nem a `naplok/FORDITAS_P_terminologia_v2.tsv`-re | a felhasználó explicit megerősítette |
| D6 | A vak bírálatot (5. lépés) én (Claude, ez a session) végeztem a kulcs megnyitása előtt; a szúrópróbát (6. lépés) egy másik chat-menet pontozta, nem a felhasználó személyesen | a felhasználó kérése |
| D7 | A `G0266` DeepSeek-kimenetét a szúrópróba alapján utólag `kihagyás(kritikus)`-ra javítottam (eredetileg 7/10 volt) | a chat pontszáma (1/10) és a mért hosszarány (0,42) egybehangzóan ezt igazolta |
| D8 | A G0266-korrekció szabályát (hosszarány<0,8 VAGY görög-paritás SÉRTÉS) gépiesen alkalmaztam mind a 90 kimenetre, az eredeti pontszám megtartásával külön oszlopban | a felhasználó kérése; a két minősítés 11/90 esetben tér el, ebből 3 egy valódi, a gépi kapu által sem látott hibatípust (fordítatlan szöveg) fed fel |
| D9 | A `Phi`→`Filem` kapurést és a "fordítatlan szöveg" kapurést csak a jelentésbe vettem fel, az FP2 gépi kapuját nem módosítottam | a felhasználó explicit kérése |
| D10 | A 4b forgatókönyvet a felhasználó javítása szerint (MiniMax csak tartalék, csak hiba esetén) újraszámoltam; mivel gyakorlatilag egyenértékű a 4a-val, a jelentés a 7. (cache-alapú) forgatókönyvet javasolja, nem a 4a/4b-t | a 7. forgatókönyv minden más szempontból (ár, ár-érzékenység) jobb |
