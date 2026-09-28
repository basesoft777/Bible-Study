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
prompt-cache-sel és egyszeri önújrapróbával (7. forgatókönyv), ≈4,93 USD becsült
teljes költséggel (9,86 USD duplázott ár mellett is a 15 USD-s plafonon belül).**
A v3 stílus megtartotta/javította a minőséget (l. 3. pont). Négy tétel javítandó a
#7 (éles Thayer-fordítás) indítása előtt (l. 6. pont). *(Ez a jelentés a
`fuggetlen-ellenor` ügynök 2026.09.28-i ellenőrzése — `naplok/ELLENOR_FP2.md` —
alapján több ponton javítva lett: a költségbecslés egy számítási hibája, a kritikus
hibák száma, a kor2-minta darabolási állítása és több táblázat-cella. A javítások a
megfelelő szakaszoknál jelölve vannak.)*

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

**Kritikus hibák típus szerint** (mind a 90 kimeneten, **23 eset** — l.
`naplok/ELLENOR_FP2.md`, a korábbi "21" tévedés volt):
- **DeepSeek — 15 eset: 14 kihagyás (csonkolás) + 1 betoldás** (`G0086` —
  átfogalmazott/bővített parafrázis, nem a forrás hű fordítása). A 4 legrövidebben
  csonkolt kimenetet explicit `max_tokens=8000`-rel újrafuttatva mind a 4 teljes, hű
  fordítást adott (0,0018 USD) — ez a DeepSeek megbízhatatlanságára utal, **nem**
  paraméterhibára (**következtetés, nem mérés**: a `finish_reason` nem `length` volt
  egyik esetben sem — a `fp2/_run/hibak/` könyvtár üres, és a `completion_tokens`
  értékek nem kerek/plafonszerűek).
- **MiniMax — 7 eset:** 3 esetben a szócikket **egyáltalán nem fordította le**
  (angolul maradt: `G0002`, `G1944`, `G5013` — mind nem darabolt szócikk), 4 esetben
  (mind darabolt szócikk) **kitalált, a forrásban nem szereplő tudományos apparátust**
  toldott be (`G4151`, `G0026`, `G0266`, `G1343`). A gépi kapu a `G0002`-t véletlenül
  elkapta (a torz görög token miatt), a `G1944`/`G5013` nem-lefordítást viszont csak
  közvetve, meg nem különböztetve jelzi (l. 7. pont).
- **Gemini — 1 eset:** `G1106`-nál `Phi 1:14`-et `Filem 1:14`-re fordította
  (Filippi helyett Filemon) — a gépi kapu **nem** jelezte ezt (l. 7. pont; a
  `G1944`/`G5013` MiniMax-eseteket viszont a kapu terminológia-ellenőrzése jelzi,
  csak nem tudja megkülönböztetni a hiba fajtáját tőle — l. 7. pont, pontosítva).

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
bírálati szigorral (azonos bíráló, azonos rubrika, objektíven mérhető hosszcsonkolás).
**Javítás** (l. `naplok/ELLENOR_FP2.md`): a korábbi állítás, hogy "a 20 közös
szócikk közül egy sem igényelt volna darabolást", **hamis volt** — `G4151` (23 705
kar., 12 darab) és `G5590` (5950 kar., 3 darab) is a kor2-mintában van, és mindkettő
darabolást igényel; a DeepSeek FP2-pontszáma mindkettőn katasztrofális (1/10, 2/10).
**Ha ezt a két szócikket kizárjuk, a maradék 18 (nem darabolt) szócikken a DeepSeek
FP2-átlaga még mindig csak ≈5,44/10** — tehát a darabolás **hozzájárul** a
visszaeséshez, de **nem az egyetlen ok**: a nem darabolt szócikkeken mért 5,44 is
messze a kor2 8,60-as alapszintje alatt marad. A legvalószínűbb ok a **kor2 óta
~3×-osára nőtt OpenRouter-ár**
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

**Javítva** (l. `naplok/ELLENOR_FP2.md`): a `fp2/koltsegbecsles.py` a darabolt
szócikkeknél a szócikk *első* darabjának kimenetét osztotta a *teljes* szócikk
hosszával, ahelyett hogy az összes darab kimenetét összegezte volna — ez a Gemini
kimeneti token-arányát kb. 17%-kal alábecsülte. A táblázat az alábbi, javított
számokat mutatja (a Gemini-forgatókönyvek kb. +0,5–0,6 USD-vel drágábbak, mint a
korábban jóváhagyott verzióban — a plafonon belül maradnak, a sorrend nem változik).

| # | Forgatókönyv | Alapár (p10–p90) | Ár ×2 |
|---|---|---:|---:|
| 1 | Csak Gemini 3.1 Flash Lite | 10,15 (9,63–10,93) | 20,29 |
| 2 | Csak DeepSeek V4 Flash | 4,26 (4,01–4,39) | 8,53 |
| 3 | Csak MiniMax M3 | 11,05 (10,63–11,62) | 22,11 |
| 4a | Gemini + 1× Gemini-önújrapróba | 10,45 | 20,90 |
| 4b | Gemini + MiniMax tartalék (csak nem darabolt, csak hiba esetén) | 10,49 (≈4a) | — |
| 5 | Gemini + prompt-cache | 4,79 | 9,57 |
| 6 | Gemini + apparátus-helyőrzők (becsült, nem tesztelt) | 9,10 | — |
| **7** | **Gemini + prompt-cache + 1× önújrapróba** | **4,93 (4,40–5,73)** | **9,86** |

**A tervezett plafon 15 USD** — minden alapár belefér; az ár ×2 érzékenység a
Gemini/MiniMax-forgatókönyveket túltolja (20–22 USD), **de a cache-alapú
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
4. **Fordítatlan szöveg ellenőrzése, elkülönítve** — a terminológia-ellenőrzés (5.)
   valójában SÉRTÉS-t ad a `G1944`/`G5013` MiniMax-eseteken is, de nem különíti el,
   hogy a SÉRTÉS oka fordítatlanság-e (ugyanez a SÉRTÉS ártalmatlan terminológia-
   eltérésekre is lefut). Kell egy külön, célzott ellenőrzés, amely kifejezetten azt
   nézi, hogy a válasz tartalmaz-e hosszabb, összefüggő angol prózaszakaszt.
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
3–4. tétele): a könyvnév-egyezés ellenőrzésen (`Phi`→`Filem`) egyáltalán nem bukik el;
a fordítatlanul hagyott szöveget a terminológia-ellenőrzés SÉRTÉS-e jelzi, de nem
különíti el más terminológia-eltérésektől.

**`fp2/koltsegbecsles.py` — kimeneti arány számítási hibája darabolt szócikkeken**
(l. `naplok/ELLENOR_FP2.md`; ez a saját FP2-eszközöm hibája, nem a `#3`-é, de itt
jegyzem fel): a darabolt szócikkeknél csak az első darab kimenetét vette figyelembe,
a teljes szócikk hosszával osztva — ez kb. 17%-kal alábecsülte a Gemini kimeneti
token-arányát. **Javítva**, a költségtábla (5. pont) frissítve.

## 8. Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | A brief alapja `main` (`8f5a1eb`), nem a megnevezett, már törölt `claude/forditas-pilot-brief-3afbbf-37c8ky` ág — az PR #62-ként már be van olvasztva | a névre keresett ág törölve, a tartalma a main-ben van |
| D2 | A prompt v2/terminológia v2 a felhasználó által csatolt `FORDITAS_ELES_THAYER_BRIEF.md` E1 tételéből épült fel, mert a repóban nem léteztek | a brief explicit ezt írta elő |
| D3 | `fordit.py` additív kapcsolók (`--prompt-fajl`, `--terminologia-fajl`, `--kimenet-dir`, `max_tokens`, `idotartam_mp`) — alapértelmezésben változatlan viselkedés | a `FORDITAS_ELES_THAYER_BRIEF.md` E1 tétele ugyanezt tervezte; enélkül a saját futás felülírta volna a kor2 pilot fájljait (ez egyszer meg is történt egy tesztnél, visszaállítva) |
| D4 | A `G1941` (arany) a mintában maradt és újra lefordíttattuk mindhárom modellel (nem lett kihagyva a G7-szabály szerint), mert a brief az arannyal való összevetésre szánta | brief 2. lépés |
| D5 | A 3. lépés (terminológia-kiegészítés) csak az FP2 próbára vonatkozik, nem a `naplok/FORDITAS_P_terminologia_v2.tsv`-re | a felhasználó explicit megerősítette |
| D6 | A vak bírálatot (5. lépés) én (Claude, ez a session) végeztem a kulcs megnyitása előtt; a szúrópróbát (6. lépés) egy másik chat-menet pontozta, nem a felhasználó személyesen | a felhasználó kérése |
| D7 | A `G0266` DeepSeek-kimenetét a szúrópróba alapján utólag `kihagyás(kritikus)`-ra javítottam (eredetileg **9**/10 volt — egy korábbi verzió téves 7/10-et írt, l. D11) | a chat pontszáma (1/10) és a mért hosszarány (0,42) egybehangzóan ezt igazolta |
| D8 | A G0266-korrekció szabályát (hosszarány<0,8 VAGY görög-paritás SÉRTÉS) gépiesen alkalmaztam mind a 90 kimenetre, az eredeti pontszám megtartásával külön oszlopban | a felhasználó kérése; a két minősítés 11/90 esetben tér el, ebből 2 (nem 3) egy valódi, a gépi kapu által meg nem különböztetett hibatípust (fordítatlan szöveg) fed fel, 1 (`G1106`) a Phi/Filem-hiba |
| D9 | A `Phi`→`Filem` kapurést és a "fordítatlan szöveg" kapurést csak a jelentésbe vettem fel, az FP2 gépi kapuját nem módosítottam | a felhasználó explicit kérése |
| D10 | A 4b forgatókönyvet a felhasználó javítása szerint (MiniMax csak tartalék, csak hiba esetén) újraszámoltam; mivel gyakorlatilag egyenértékű a 4a-val, a jelentés a 7. (cache-alapú) forgatókönyvet javasolja, nem a 4a/4b-t | a 7. forgatókönyv minden más szempontból (ár, ár-érzékenység) jobb |
| D11 | A `fuggetlen-ellenor` ügynök (2026.09.28, l. `naplok/ELLENOR_FP2.md`) több érdemi hibát talált és javítottam: a költségbecslés kimeneti-arány számítási hibáját (Gemini-forgatókönyvek +0,5–0,6 USD), a kritikus esetek számát (21→23) és a DeepSeek/MiniMax bontását, a `G0266` eredeti pontszámát (7→9), a kor2-minta darabolási állítását (két, nem egy szócikk igényelt darabolást a kor2-mintában is), és három táblázat-cellát, amelyek a természetesség-oszlopot mutatták az összpontszám helyett | a felhasználó kérte a menetzárás előtti független ellenőrzést; az ügynök nem tudott fájlt írni/commitolni, ezt a Code-session pótolta |
| D12 | Az ellenőrzés jelezte, hogy a `naplok/FP2_felmeres.md` 0.2 pontja ("a brief tiltja a #3 módosítását, nem módosítom") és a tényleges D3 döntés (a `fordit.py` mégis módosult, additív kapcsolókkal) egymás mellett ellentmondásosnak hat — ezt a felhasználó felé jelzem, a döntést (additív bővítés ≠ hibajavítás) fenntartva, mert nélküle a próba nem lett volna elvégezhető | l. `naplok/ELLENOR_FP2.md` |
