# FORDITAS_PILOT_BRIEF.md — fordítási pilot: Thayer-szócikkek külső modellekkel (OpenRouter)

*v1 — 2026.09.25 · jóváhagyásra: a §2 G-döntései (főleg G3, G4, G6) és a §0 számai · a 2026.09.25-i munkaterv B briefje (2a–2c)*

**Cél.** Mérés alapján eldönteni, melyik olcsó modell adhat elfogadható **hű magyar fordítást**
szótári szócikkekre (első körben Thayer), és milyen gépi ellenőrzéssel. A pilot csak mér:
**semmi nem kerül élesbe**. Az éles fordítás a 4e/4f csomag, a SZOTAR 4a után, a
`adat/forditasok.tsv` gyorsítótárba (munkaterv M8).

**Előfeltétel:** nincs. OpenRouter API-kulcs az `OPENROUTER_API_KEY` környezeti változóban.

**Futás.** 1. menet (FP0–FP4, szkript + futás): helyi gépen, külön worktree-ben (a kulcs ott
van); cloud csak akkor, ha az FP0 szerint az `openrouter.ai` elérhető a sessionből és a kulcs
be van állítva. 2. menet (FP5, bírálat): helyi. **Modell:** 1. menet Sonnet, 2. menet Opus.
**Push:** csak a saját ágra; a `main`-re soha.

**Szerkezet.** 1. menet: FP0–FP4 → ⛔ (költség és gépi ellenőrzés a chatbe). Közte te pontozol
5 szócikket vakon. 2. menet: FP5 vak bírálat → FP6 modellválasztási javaslat ⛔.

**Nincs benne:** írás az `adat/`, `lexikon/`, `konkordancia/`, `tematikus_lezart/`, `motivumok/`
alá; a SZOTAR S1 gyorsítótár-táblájának létrehozása; a kiejtés (az a szabálytábla dolga,
SZOTAR S1.2); BDB/UBS/TBESG-fordítás (a pilot csak Thayer).

---

## 0. Kiindulás *(az FP0 újraméri; eltérésnél jelentsd, és folytasd)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` | `72b200c` |
| 0.2 | `adat/lexikon_hivatkozasok.tsv`, `szotar = Thayer` | 14 sor: 1 lefordítva (G1941), 13 üres `forditas_hu` (G0012, G0086, G0282, G0813, G0994, G1311, G1944, G2671, G4151, G5010, G5351, G5356, G5590) |
| 0.3 | a 13 üres szócikk hossza (`szoveg_en`) | ~39 500 karakter; ebből G4151 ~23 700, G5590 ~5 950 |
| 0.4 | `adat/elofordulasok.tsv` görög tokenjei Thayer-sor nélkül | 3: G0035, G0540, G2672 (a 4f/N1 leendő munkája) |
| 0.5 | `konkordancia/Thayer_teljes.tsv` | 5 426 szócikk (`Strong_padded`, `Strong_eredeti`, `Teljes_szocikk`) |
| 0.6 | fordítási szabály | `adat/SEMA.md` 2.5, `forditas_hu` sor (hű fordítás, rövidítés feloldva, bizonytalan feloldás változatlan, Károli-rövidítés, a héber/görög idézet változatlan, betoldás és formázás nincs) |
| 0.7 | minta az OpenRouter-hívásra | `eszkozok/cremer_ocr_javit.py` (kulcs csak környezetből, újrapróbálkozás, `usage.cost`-alapú költségnapló és -plafon, gyorsítótár) |

---

## 1. Mércék

**A minta (20 szócikk, a `forras_hash` rögzítve):**
- **E (éles igény):** a 0.2 13 üres szócikke — a pilot eredménye a 4e-t közvetlenül előkészíti;
- **A (arany):** G1941 — a kész, jóváhagyott fordítás az összevetés alapja (a modell nem látja);
- **N (leendő igény):** a 0.4 3 szócikke;
- **V (változatosság):** 3 szócikk, amelyet a szkript determinisztikusan választ a
  `Thayer_teljes.tsv`-ből: egy ≤ 300 karakteres, egy héber idézetet tartalmazó, egy
  szövegkiadás-jelzetekkel (L T Tr WH) sűrű. A választás szabálya a jelentésbe kerül.

**Gépi ellenőrzések szócikkenként** (fájlba írt szkript, minden modell minden kimenetén):
1. a görög és héber betűs szakaszok multihalmaza a forrással azonos;
2. a fejezet:vers számpárok multihalmaza a forrással azonos;
3. minden könyvrövidítés szerepel a Károli-rövidítéslistában (`konkordancia/Konyv_normalizalo_tabla.tsv`);
4. nincs Markdown-formázás (`*`, `_`, `#`, `**`) és nincs betoldott magyarázó zárójel;
5. az ideiglenes terminológia (G5) sérülése = hiba;
6. a hosszarány (magyar/angol karakter) 0,8–1,6 között — ezen kívül csak jelzés;
7. JSON-séma érvényes.

**Vak bírálati pontozás (FP5), szócikkenként, 10 pont:** pontosság 0–3 (kihagyás, betoldás,
félreértés), terminológia 0–2, magyar nyelvhelyesség 0–3, formai szabályok 0–2. A modellek
neve rejtve (X/Y/Z), a sorrend szócikkenként véletlen, rögzített maggal.

**Döntési szabály (FP6):** az a modell javasolható, amelynél a gépi ellenőrzések átmenési
aránya ≥ 95%, egyetlen szócikk pontossága sem 0, és a bírálati átlaga a legmagasabb; közel
azonos átlagnál (≤ 0,5 pont) az olcsóbb. Ha egyik sem felel meg: az éles fordítás Claude-dal
megy, a külső modell csak nyersfordítást ad.

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | A pilot csak a `naplok/FORDITAS_P*` fájlokba és az új `eszkozok/fordit.py`-ba ír. A kimenet sémája a SZOTAR S1 gyorsítótáréval azonos (`szotar`, `strong`, `entry_id`, `jelentes_szam`, `mezo`, `forras_hash`, `forditas_hu`, `allapot = pilot`, `modell`, `datum`, `terminologia_verzio`), hogy a 4e változtatás nélkül átvehesse. |
| G2 | A `fordit.py` kimeneti útvonala paraméter; alapértelmezés a `naplok/`. Az `adat/`-ba írás tiltott, amíg a 4a meg nem teremti a gyorsítótár-táblát. |
| G3 | **Modellek:** `m1` DeepSeek V4 Flash (kötelező, M3); `m2` Gemini 3.8 Flash (a Cremer-pilotban ez tartotta a sémát); `m3` **javaslat:** Claude Haiku 4.5 mint minőségi viszonyítás — alternatíva: GPT-5 mini. A pontos OpenRouter-azonosítót és árat az FP0 a `/api/v1/models` végpontról veszi, nem emlékezetből. |
| G4 | **Kiejtés:** a modell nem ír átírást; a héber/görög idézet változatlan marad. Az arany G1941 zárójeles átírásait az összevetés maszkolja. A kiejtést élesben a SZOTAR S1.2 szabálytáblája adja. |
| G5 | **Ideiglenes terminológia:** `naplok/FORDITAS_P_terminologia.tsv`, induló sorok a SZOTAR S2-ből (spirit = szellem, spiritual = szellemi, soul = lélek) és a G1941 aranyból kinyert rövidítés-feloldások (pl. cl. = klasszikus, pass. = szenvedő alakban, Heb. = héber, see = l.). A szövegkiadás-jelzetek (L, T, Tr, WH, Rec.) változatlanok maradnak. Élesben a 4a `adat/terminologia.tsv`-je lép a helyére. |
| G6 | **Hosszú szócikk:** a 4 000 karakternél hosszabb szócikket (G4151, G5590) a szkript a forrás saját jelentés-számozásánál (1., 2., a., b.) darabolja, darabonként hív, és összefűzi; a gépi ellenőrzés az egészen fut. |
| G7 | **Költség:** plafon 2 USD a teljes 1. menetre; `usage.cost` alapján `naplok/FORDITAS_P_koltseg.tsv`; a plafon elérésekor leáll (kilépési kód 3). Gyorsítótár a `forras_hash` + modell + prompt-verzió kulcson, így ismétléskor nincs újrahívás. |
| G8 | Csak nyílt forrás megy ki (D17): a Thayer közkincs. Más szótár nem szerepel a promptban. |
| G9 | Közös fájlt a menet nem ír; a jelentés a saját ágán marad. |

---

## 3. Tételek

**1. menet**

- **FP0 — Hozzáférés és kiindulás.** A §0 újramérése; az `openrouter.ai` elérhetősége és a
  kulcs megléte (a kulcs értékét soha ne írd ki); a három modell azonosítója és ára a
  `/api/v1/models`-ból. `naplok/FORDITAS_P0_kiindulas.md`.
- **FP1 — Minta és terminológia.** A 20 szócikk kiválasztása a §1 szerint →
  `naplok/FORDITAS_P1_minta.tsv` (strong, csoport E/A/N/V, hossz, `forras_hash`); a G5
  terminológia. Az arany fordítás külön fájlba kerül, a prompt nem kapja meg.
- **FP2 — `eszkozok/fordit.py`.** Prompt fájlból (`naplok/FORDITAS_P_prompt_v1.md`: a SEMA 2.5
  szabálya szó szerint, a terminológia, a Károli-rövidítéslista, a JSON-kimenet sémája:
  `strong`, `forditas_hu`, `bizonytalan_feloldasok[]`); darabolás (G6); hívás, újrapróbálkozás,
  költségnapló, gyorsítótár (G7) a `cremer_ocr_javit.py` mintájára; `--szaraz` mód
  token- és költségbecsléssel. Commit: `FP2: fordit.py (pilot)`.
- **FP3 — Futás.** Előbb `--szaraz`, utána éles hívás mindhárom modellel a 20 szócikkre →
  `naplok/FORDITAS_P3_kimenet.tsv` (G1 sémája), `naplok/FORDITAS_P_koltseg.tsv`.
- **FP4 — Gépi ellenőrzés és jelentés ⛔.** A §1 hét ellenőrzése fájlba írt szkripttel
  (`naplok/FORDITAS_P4_ellenoriz.py`) → `naplok/FORDITAS_P4_ellenorzes.tsv` (modell × szócikk ×
  ellenőrzés); a vak bírálati csomag előkészítése (`naplok/FORDITAS_P4_vak.md`: forrás +
  X/Y/Z fordítás szócikkenként, a kulcs külön fájlban: `naplok/FORDITAS_P4_vak_kulcs.tsv`). Ugyanebből a te mintád: 5 szócikk
  (véletlen, rögzített maggal) × 3 modell vakon, kitöltendő pontozótáblával:
  `naplok/FORDITAS_P4_minta_felhasznalo.md`.
  `naplok/FORDITAS_P_jelentes.md`: költség modellenként, gépi átmenési arány, hibatípusok.
  Push a saját ágra. ÁLLJ, jelentés a chatbe.

**2. menet (helyi, Opus)**

- **FP5 — Vak bírálat.** A `FORDITAS_P4_vak.md` pontozása a §1 szempontjaival, a kulcs
  megnyitása nélkül → `naplok/FORDITAS_P5_pontok.tsv`. Az arany G1941-nél az összevetés az
  arannyal is. Bemenet a **te kitöltött mintád** is (`FORDITAS_P4_minta_felhasznalo.md`, a
  2. menet indításakor csatolva); ha nincs csatolva, az FP5 után ÁLLJ, és kérd.
- **FP6 — Javaslat ⛔.** A kulcs megnyitása; a §1 döntési szabálya; eltérés a Claude- és a te
  pontjaid között (ha > 2 pont egy szócikken, azt külön megjelölni). Javaslat a 4e/4f-re:
  modell, prompt-verzió, kötelező gépi ellenőrzések, a terminológiai tábla induló sorai.
  `naplok/FORDITAS_P6_javaslat.md`. ÁLLJ.

Commit tételenként: `FP<n>: <rövid leírás>`.

---

## 4. Elfogadási feltételek (gépi kapu)

| # | Feltétel |
|---|---|
| K1 | `git diff --stat main..HEAD`: csak `FORDITAS_PILOT_BRIEF.md`, `eszkozok/fordit.py` és `naplok/FORDITAS_P*` |
| K2 | `eszkozok/ellenoriz.py`: RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 (változatlan) |
| K3 | a kulcs sehol nem jelenik meg (repó, napló, kimenet) |
| K4 | a költségnapló összege ≤ 2 USD, és egyezik a kimenetben rögzített hívásokkal |
| K5 | a 20 × 3 kimenet mindegyike megvan, vagy a hiány oka a jelentésben |
| K6 | minden szám (arány, pont, költség) fájlba írt szkriptből; nincs `csv` modul; héber/görög szöveg csak fájlból (CLAUDE.md, Shell) |
| K7 | az FP6 javaslata a §1 döntési szabályát követi, eltérésnél indokkal |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.25 | Első változat a munkaterv B briefjéből: 20 szócikkes minta (E 13, A 1, N 3, V 3); három modell (G3); kiejtés nélkül (G4); ideiglenes terminológia (G5); 2 USD plafon (G7); vak bírálat + felhasználói minta, előre rögzített döntési szabály (§1). |

---

## 6. Nyitó promptok (a briefet csatold)

**1. menet (helyi worktree, vagy cloud, ha az FP0 engedi):**
```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t.
1. A csatolt FORDITAS_PILOT_BRIEF.md-t mentsd a repó gyökerébe, változtatás nélkül.
   Commit: "FP: FORDITAS_PILOT_BRIEF.md v1".
2. Hajtsd végre az FP0–FP4 tételeket a brief §3 szerint, a §1 mércéivel és a §2 döntéseivel.
   Az OPENROUTER_API_KEY értékét soha ne írd ki és ne mentsd. Tételenként külön commit.
3. Az FP4 után ellenőrizd a §4 K1–K6-ot, majd pushold a saját ágadat. A main-re ne pushold.
ÁLLJ az FP4 után: jelentés a chatbe (ág, commitlista, költség modellenként, gépi átmenési arány).
```

**2. menet (helyi, Opus, ugyanazon az ágon):**
```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t és a FORDITAS_PILOT_BRIEF.md-t. A csatolt, általam kitöltött
FORDITAS_P4_minta_felhasznalo.md-t mentsd a naplok/ alá. Commit: "FP5: felhasználói minta".
Hajtsd végre az FP5–FP6 tételeket. Az FP5 alatt a naplok/FORDITAS_P4_vak_kulcs.tsv-t ne nyisd meg.
A végén ellenőrizd a K7-et, pushold a saját ágadat. ÁLLJ az FP6 után: javaslat a chatbe.
```
