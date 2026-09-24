# CREMER_OCR_BRIEF.md — a Cremer teljes szövegének javítása külső képolvasó modellekkel

*v1 — 2026.09.23 · jóváhagyásra: a §2 C-döntései és a §0/§4 számai*

**Cél.** Hermann Cremer *Biblico-Theological Lexicon of New Testament Greek* (3. angol kiadás,
Supplementtel) **teljes szövege** gépileg olvasható, görög betűs formában a `konkordancia/`
alá, szócikkekre bontva, Strong-számmal. Az angol szöveg a hOCR-ből jön; a hOCR-ből hiányzó
görög szavakat két független, olcsó képolvasó modell állítja vissza a lapképről, OpenRouteren
keresztül.

**Viszony a `SZOTAR_BRIEF.md`-hez.** Független tőle: csak a `konkordancia/_nyers/cremer/` alól
olvas, és csak új `konkordancia/Cremer_*` táblákat ír; a `lexikon/` kimenetet nem érinti.
Futhat a SZOTAR 1. menete előtt, alatt vagy után. Az eredményét a SZOTAR S2.5 használja (ott D28).

**Szerkezet.** O0 előkészítés → O1 pilot ⛔ → O2 teljes futás → O3 szócikkekre bontás és
index → O4 jelentés ⛔.

**Futtatás:** a felhasználó, helyben (Claude Code, Sonnet), `OPENROUTER_API_KEY` környezeti
változóval. **A kulcs soha nem kerül a repóba, naplóba vagy commit-üzenetbe.** Push csak kérésre.

---

## 0. Kiindulás *(az O0 újraméri; eltérésnél ÁLLJ)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | nyers fájlok | `konkordancia/_nyers/cremer/`: `cu31924098819406_hocr.html`, `_page_numbers.json`, `_jp2.zip`, `_meta.xml`, `_scandata.xml`; a mappa `.gitignore`-ban |
| 0.2 | kötet | 967 levél; a hOCR lapindexe = levélszám |
| 0.3 | levél ↔ oldal | oldal 1–592 → levél = oldal + 15; oldal 590–915 → + 18; oldal 918–951 (mutatók) → + 16 |
| 0.4 | hOCR | 561 048 szó, ebből 107 802 `x_wconf` < 60; görög karakter: 0 |
| 0.5 | ismert szócikkek (Abbott-Smith) | ἄβυσσος 2 → levél 17; ᾅδης 67, 610 → 82, 628; ἐπικατάρατος 109 → 124; ἐπικαλέω 335, 742 → 350, 760 |
| 0.6 | mutatók | görög szómutató a 934. levéltől, héber mutató („V. Hebrew words referred to") a 950. levéltől |

---

## 1. Fogalmak

- **Gyanús szó:** hOCR-szó `x_wconf` < 60, vagy latin betűs torzkép görög helyén (pl. `ABvocos`).
- **Csere:** egy gyanús szó helyére javasolt görög (vagy héber, vagy javított latin) alak, a hOCR szó-azonosítójával.
- **Egyezés:** a két modell cseréje Unicode NFC-normalizálás után karakterre azonos (ékezettel, hehezettel együtt).

---

## 2. C-döntések *(jóváhagyásra)*

| # | Kérdés | Javaslat |
|---|---|---|
| C1 | Modellek | **Két független, képolvasó modell OpenRouteren, eltérő gyártótól.** Javaslat (D7): **(1) Qwen** — a Qwen3.5-Flash vagy a Qwen3-VL-32B (nagyon olcsó, erős dokumentum-OCR); **(2) Google Gemini Flash**, **rögzített verzióval** (a „latest" álnév nem használható, mert menet közben másik modellre válthat, és a futás nem lenne reprodukálható). A pontos modell-azonosítót a beállításkor az openrouter.ai/models oldalról kell kimásolni; az azonosítók és az árak az `eszkozok/cremer_ocr_config.json`-ban. Ha a pilotban valamelyik gyengén teljesít a politonikus görögön, csere a pilot megismétlésével. |
| C2 | Hívás egysége | **Laponként egy hívás modellenként.** Bemenet: a lapkép (jp2 → JPEG, a hosszabb él legfeljebb 2000 px) + a lap hOCR-szavai (azonosító, szöveg, megbízhatóság, bbox), a gyanúsak kiemelve. |
| C3 | Kimenet | **Szigorú JSON cserelista**: `{szo_id, alak, nyelv (grc/heb/lat)}` — csak a gyanús szavakra. A modell nem ír szabad szöveget; az angol szöveg a hOCR-ből változatlan. Érvénytelen JSON: egy újrapróba, utána `hiba`. |
| C4 | Elfogadás | **Egyezés → `auto`**; eltérés → `vitas`; valamelyik modell nem ad cserét → `hianyzo`. A `vitas` és a `hianyzo` sorok nem kerülnek a javított szövegbe (ott a hOCR-alak marad, jelölve). |
| C5 | Alakellenőrzés | A görög cserék összevetése a meglévő alaklistákkal (`TAGNT_kivonat`, `LXX_OS`) és lemmalistákkal (Abbott-Smith, LSJ, TBESG). Találat → `alak_igazolt`; nincs találat → nem hiba (a Cremer klasszikus idézetei nincsenek a listákban), csak jelölés. A héber cserék a TBESH/BDB lemmáival. |
| C6 | Költségplafon | A configban rögzített felső határ (javaslat: **20 USD** a teljes futásra, a pilot külön); a hívásnapló futó összeget vezet, a plafon elérésekor megáll. Költség- és tokennapló laponként. |
| C7 | Pilot | **20 lap**: a 7 ismert levél (17, 82, 124, 350, 628, 760 + a görög mutató 934. levele), a héber mutató 950. levele és 12 véletlen levél (rögzített maggal). Kézi ellenőrzés: az `auto` cserék mintája (legalább 200) és minden `vitas` sor. **A teljes futás feltétele: az `auto` cserék hibaaránya < 1%**, és a `vitas` + `hianyzo` arány jelentve. |
| C8 | Vitás sorok | A teljes futás után nem oldjuk fel mindet: **csak a render által használt szócikkekben** (ma a 13 G-token és a 24 H-token héber mutatója), kézi döntéssel, a javítási naplóba. A többi `vitas` marad, jelölve; a render nem használ feloldatlan sort. |
| C9 | Külső modell a projekt adatán | Ez az első ilyen lépés (a „fordítási pipeline, külső modellek" eddig kizárva). **Engedett, mert** a forrás közkincs (1880-as kiadás), a modellnek csak a lapkép és a nyilvános OCR-szöveg megy; projekt-saját adat (tanulmány, döntésnapló) nem. |

---

## 3. Tételek

### O0 — előkészítés *(egy commit)*
- **O0.1** A §0 újramérése; a `.gitignore` ellenőrzése (`konkordancia/_nyers/`); SHA-256 a nyers fájlokra a `konkordancia/README.md`-be (a tétel azonosítójával: archive.org `cu31924098819406`).
- **O0.2** `eszkozok/cremer_ocr_javit.py`: lapkép-kivágás a jp2-zipből (kicsomagolás nélkül, laponként), hOCR-feldolgozás, OpenRouter-hívás (C1–C3), egyezés (C4), alakellenőrzés (C5), költségnapló és plafon (C6). Kulcs csak környezeti változóból. `--levelek`, `--pilot`, `--szaraz` (hívás nélkül: csak a bemenetek előállítása és a becsült tokenszám) kapcsolók.
- **O0.3** `eszkozok/cremer_ocr_config.json` (modellnevek üresen hagyva — a felhasználó tölti ki), `--szaraz` futás a 20 pilot-lapra: becsült token és költség jelentve.

### O1 — pilot ⛔
- **O1.1** Futás a 20 lapra. Kimenet: `naplok/CREMER_O1_csere.tsv` (`szo_id`, `level`, `bbox`, `ocr`, `m1`, `m2`, `dontes`, `alak_igazolt`), `naplok/CREMER_O1_koltseg.tsv`.
- **O1.2** Ellenőrző csomag a kézi átnézéshez: 200 véletlen `auto` csere + minden `vitas`, mindegyik mellett a lapkép kivágott része (fájlnév a sorban). `naplok/CREMER_O1_ellenorzes/` (a kivágott képek a `_nyers` alá, a tsv a `naplok/`-ba).
- **O1.3** Jelentés: `naplok/CREMER_O1_jelentes.md` — egyezési arány, `vitas`/`hianyzo` arány, alakellenőrzés-arány, tényleges költség és a teljes kötetre vetített költség. **ÁLLJ** — a kézi ellenőrzés és a C7 küszöb után a felhasználó dönt a teljes futásról (és szükség esetén a modellcseréről).

### O2 — teljes futás
- **O2.1** Futás a teljes kötetre (a pilot lapjai nem futnak újra), plafonnal. Megszakítás után folytatható (a kész lapokat kihagyja).
- **O2.2** `konkordancia/Cremer_szoveg.tsv` (`level`, `oldal`, `sor`, `szoveg`, `gyanus_maradt`): a hOCR-szöveg az `auto` cserékkel; `konkordancia/Cremer_csere.tsv`: minden csere a döntéssel.

### O3 — szócikkekre bontás és index
- **O3.1** Szócikkhatárok: a szócikkfej görög címszava (a lap élőfejével és a görög szómutatóval keresztellenőrizve), fő- és Supplement-rész külön.
- **O3.2** `konkordancia/Cremer_szocikkek.tsv` (`lemma`, `strong`, `strong_parositas` = `auto`/`kezi`/`nincs`, `oldal`, `level`, `resz`, `szoveg`, `vitas_db`, `allapot` = `javitott`); Strong-párosítás a TBESG lemmáival. `konkordancia/Cremer_heber_mutato.tsv` a héber mutatóból.
- **O3.3** A render által használt szócikkek (13 G-token; a héber mutató 24 H-tokenre) `vitas` sorainak kézi feloldása a `konkordancia/Cremer_javitasi_naplo.tsv`-be.

### O4 — jelentés ⛔
- `naplok/CREMER_O4_jelentes.md`: szócikkek száma, Strong-párosítás (auto / kézi / nincs), maradó `vitas` sorok, tényleges költség, a 13 G-token lefedettsége. **ÁLLJ** — a 13 szócikk és a héber mutató jóváhagyása (`javitott` → `jovahagyott`); ezután használja a SZOTAR S2.5.

---

## 4. Várt számok

| Tétel | Várt |
|---|---|
| O0 `--szaraz` | 20 lap bemenete elkészül; becsült token és költség jelentve |
| O1 | `auto` hibaarány a kézi mintán < 1% (C7) |
| O2 | ~950 lap feldolgozva; költség ≤ a plafon |
| O3 | a 13 G-tokenből a Cremer-szócikkel rendelkezők mind megtalálva (legalább a 4 Abbott-Smith-szócikk); Strong-párosítás aránya jelentve |
| minden szakasz | a `lexikon/`, `adat/`, `tematikus_lezart/` bájtra változatlan; a kulcs sehol nem szerepel (`git grep` a kulcs előtagjára: 0) |

---

## 5. Elfogadási kritériumok

| # | Kritérium |
|---|---|
| K1 | a nyers fájlok nincsenek a repóban; a SHA-k a README-ben |
| K2 | a kulcs nincs a repóban, naplóban, commitban |
| K3 | a hOCR angol szövege a javított szövegben változatlan (a cseréken kívül karakterre azonos) |
| K4 | a teljes futás csak a pilot jóváhagyása után indult |
| K5 | költség ≤ plafon; költségnapló laponként |
| K6 | a render által használt szócikkekben nincs feloldatlan `vitas` sor |
| K7 | TSV-kezelés `csv` modul nélkül; TSV-mezőben nincs sortörés |
| K8 | commitok a §6 szerint; `git status --porcelain` üres |

---

## 6. Commitok

| Üzenet | Fájlok |
|---|---|
| `CREMER_OCR_BRIEF.md v1` | `CREMER_OCR_BRIEF.md` |
| `O0: Cremer OCR-javító eszköz, config, nyers-fájl SHA-k` | `eszkozok/cremer_ocr_javit.py`, `eszkozok/cremer_ocr_config.json`, `konkordancia/README.md`, `.gitignore` |
| `O1: pilot (20 lap)` | `naplok/CREMER_O1_*` |
| `O2–O3: Cremer teljes szövege, szócikkek, héber mutató` | `konkordancia/Cremer_szoveg.tsv`, `konkordancia/Cremer_csere.tsv`, `konkordancia/Cremer_szocikkek.tsv`, `konkordancia/Cremer_heber_mutato.tsv`, `konkordancia/Cremer_javitasi_naplo.tsv`, `konkordancia/README.md` |
| `O4: jelentés` | `naplok/CREMER_O4_jelentes.md` |

---

## 7. Nyitó prompt *(Sonnet)*

```
Olvasd el a CLAUDE.md-t és a CREMER_OCR_BRIEF.md-t teljes egészében.

0. Commitold: "CREMER_OCR_BRIEF.md v1".
1. O0: mérd újra a §0-t (eltérésnél ÁLLJ), írd meg az eszközt és a configot. A modellneveket
   hagyd üresen a configban. Futtasd --szaraz módban a 20 pilot-lapra, jelentsd a becsült
   tokent és költséget. Commit. ÁLLJ — a modellneveket én töltöm ki.
2. (Folytatáskor) O1: pilot, ellenőrző csomag, jelentés. ÁLLJ.
Az OPENROUTER_API_KEY-t csak környezeti változóból olvasd; soha ne írd ki, ne naplózd.
```

---

## 8. Döntésnapló

| # | Döntés | Indoklás |
|---|---|---|
| D1 | A Cremer teljes szövege javul, nem csak a 13 szócikk eleje | külső olcsó modellel a teljes kötet néhány dollár nagyságrend; utána minden jövőbeli motívum Cremer-szócikke kész, újrafeldolgozás nélkül (felváltja a SZOTAR D26 „csak igény szerint" részét) |
| D2 | Két független modell, csak cserelista kimenet, egyezés = automatikus elfogadás | az olcsó modellek a politonikus görögöt hibázhatják vagy kitalálhatják; a szabad szöveg helyett cserelista kizárja az angol átfogalmazását, a két modell egyezése független megerősítés |
| D3 | Pilot 20 lapon, kézi mintával, < 1% hibaküszöbbel a teljes futás előtt | a minőség, nem az ár a kockázat |
| D4 | Költségplafon a configban, laponkénti napló | kiszámítható, megszakítható, folytatható futás |
| D5 | Külső modell a projekt adatán: csak közkincs forrás, projekt-saját adat nem megy ki (C9) | első ilyen lépés; a határt rögzíteni kell |
| D6 | Külön brief, a SZOTAR-tól független | csak `konkordancia/Cremer_*` táblákat ír, a `lexikon/`-t nem érinti; a SZOTAR 1. menete nem vár egy új eszköz fejlesztésére |
| D7 | Modelljavaslat: egy Qwen- és egy Gemini Flash-modell, rögzített verzióval (C1) | két eltérő gyártó, így a hibáik kevésbé esnek egybe; a Qwen-modellek ára töredéke a Gemini Flash-énak, a Gemini a pontosság másik lábát adja. Becslés laponként kb. 5 ezer bemeneti és 1,5 ezer kimeneti tokennel: a Gemini Flash kb. 1 cent, a Qwen tized cent alatt — a teljes kötet kettővel együtt kb. 10 USD, a 20 USD-s plafon alatt. A „latest" álnév kizárva, mert a futás közben változhat |
