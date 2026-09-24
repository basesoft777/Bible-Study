# CREMER_OCR_BRIEF.md — a Cremer teljes szövegének javítása külső képolvasó modellekkel

*v2 — 2026.09.24 · a v1 jóváhagyva és az O0 kész; a v2 a C1–C4, C6, C7, O1.2 módosításait és az O0.4 tételt hozza (D8–D13); v2.1: összehasonlító pilot a tartalék m2-vel (D14)*

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
- **Csere:** egy vagy több gyanús szó helyére javasolt görög (vagy héber, vagy javított latin) alak, a hOCR szó-azonosítóival (`szo_ids`): egy csere egy vagy több, ugyanabban a sorban egymást követő hOCR-szót fedhet le. Az írásjel nem része az alaknak; az eszköz a hOCR-tokenből teszi vissza.
- **Egyezés:** a két modell cseréje ugyanarra a `szo_ids` listára vonatkozik, azonos `nyelv`-vel, és az alak a C4 előnormalizálása után karakterre azonos (ékezettel, hehezettel együtt).

---

## 2. C-döntések *(jóváhagyásra)*

| # | Kérdés | Javaslat |
|---|---|---|
| C1 | Modellek | **Két független, képolvasó modell OpenRouteren, eltérő gyártótól, rögzített azonosítóval** (D8): **m1 = `qwen/qwen3-vl-32b-instruct`** (nem gondolkodó modell), **m2 = `google/gemini-3.8-flash`**, a gondolkodás `low` szinten. A „latest" álnév kizárva, mert menet közben másik modellre válthat. Árak 2026.09.24-én (USD / M token, bemenet / kimenet): m1 0,104 / 0,416; m2 0,75 / 3,75. Az árak a configban vannak, de a költségnapló a ténylegesen számlázott értéket vezeti (C6). Tartalék m2: `google/gemini-3.1-flash-lite` (0,25 / 1,50). Ha a pilotban valamelyik modell gyengén teljesít a politonikus görögön, csere a pilot megismétlésével. |
| C2 | Hívás egysége | **Laponként egy hívás modellenként**, `temperature: 0`. Bemenet: a lapkép (jp2 → JPEG, a hosszabb él legfeljebb 2000 px), valamint minden olyan hOCR-sor teljes tokenlistája (azonosító, szöveg), amelyben van gyanús szó. A gyanús szavak megjelölve, megbízhatósággal és **a kiküldött JPEG méretére skálázott bbox-szal** (D9). A többi sor nem megy ki. |
| C3 | Kimenet | **Szigorú JSON**, JSON-sémával, ahol a modell támogatja: `{"cserek": [{szo_ids, alak, nyelv (grc/heb/lat), extra}]}`. A `szo_ids` egy vagy több, ugyanazon sorban egymást követő azonosító, amelyből legalább egy gyanús. Kivétel az `extra: true`: ekkor a modell a kiküldött sorokban olyan görög vagy héber torzképet jelez, amely nincs gyanúsnak jelölve (D10). Az `alak` írásjel nélkül értendő. A modell nem ír szabad szöveget; az angol szöveg a hOCR-ből változatlan. Érvénytelen JSON vagy sémasértő elem esetén egy újrapróba, utána `hiba`: ilyenkor a lap minden gyanús szava `hiba` lesz, nem `hianyzo`. HTTP 429/5xx esetén visszalépéses újrapróba, és a lap csak ennek kimerülése után kap `hiba` jelölést. |
| C4 | Elfogadás | **Előnormalizálás az összevetés előtt** (D11): NFC; az aposztróf-szerű jelek (U+0027, U+02BC, U+1FBD és az önálló U+1FBF) → U+2019; a lunáris szigma (U+03F2) → σ, szóvégen ς; a szóvégi σ → ς. **Egyezés → `auto`**; eltérés (az alakban, a `nyelv`-ben vagy a `szo_ids`-ben) → `vitas`; valamelyik modell nem ad cserét → `hianyzo`; API-hiba → `hiba`. Az `extra` cseréknél egyezés esetén `extra_auto`, különben `extra_vitas`. Ezek a pilotban csak jelentve vannak, a javított szövegbe nem kerülnek; az alkalmazásukról a pilot után születik döntés. A `vitas`, `hianyzo` és `hiba` sorok nem kerülnek a javított szövegbe (ott a hOCR-alak marad, jelölve). Összevont `auto` cserénél az első azonosító kapja az alakot a hOCR-tokenek írásjeleivel, a többi azonosító üres lesz. |
| C5 | Alakellenőrzés | A görög cserék összevetése a meglévő alaklistákkal (`TAGNT_kivonat`, `LXX_OS`) és lemmalistákkal (Abbott-Smith, LSJ, TBESG). Találat → `alak_igazolt`; nincs találat → nem hiba (a Cremer klasszikus idézetei nincsenek a listákban), csak jelölés. A héber cserék a TBESH/BDB lemmáival. |
| C6 | Költségplafon | A configban rögzített felső határ: **20 USD** a teljes futásra, a pilotra külön 2 USD. A hívásnapló **a válasz `usage` mezőjéből** vezet futó összeget: bemeneti, kimeneti és gondolkodási token, valamint az OpenRouter által számlázott költség. Ha a költség nem jön vissza, a config áraiból számol, jelölve. Becslés csak a `--szaraz` módban használható (D12). A plafon elérésekor a futás megáll. Költség- és tokennapló laponként. |
| C7 | Pilot | **20 lap**: a 7 ismert levél (17, 82, 124, 350, 628, 760 + a görög mutató 934. levele), a héber mutató 950. levele és 12 véletlen levél (rögzített maggal). Kézi ellenőrzés: az `auto` cserék **300 elemes** véletlen mintája (rögzített maggal) és minden `vitas` és `extra_*` sor. **A teljes futás feltétele: 0 hiba a 300-as mintán, vagy a minta 600-ra bővítése után legfeljebb 1 hiba.** Mindkét esetben a hibaarány 95%-os felső becslése ≤ 1% (D13). Ha a pilot kevesebb mint 300 `auto` cserét ad, mindet át kell nézni, és a felső becslést jelenteni. A `vitas`, `hianyzo`, `hiba` és `extra_*` arányt jelenteni kell. |
| C8 | Vitás sorok | A teljes futás után nem oldjuk fel mindet: **csak a render által használt szócikkekben** (ma a 13 G-token és a 24 H-token héber mutatója), kézi döntéssel, a javítási naplóba. A többi `vitas` marad, jelölve; a render nem használ feloldatlan sort. |
| C9 | Külső modell a projekt adatán | Ez az első ilyen lépés (a „fordítási pipeline, külső modellek" eddig kizárva). **Engedett, mert** a forrás közkincs (1880-as kiadás), a modellnek csak a lapkép és a nyilvános OCR-szöveg megy; projekt-saját adat (tanulmány, döntésnapló) nem. |

---

## 3. Tételek

### O0 — előkészítés *(egy commit)*
- **O0.1** A §0 újramérése; a `.gitignore` ellenőrzése (`konkordancia/_nyers/`); SHA-256 a nyers fájlokra a `konkordancia/README.md`-be (a tétel azonosítójával: archive.org `cu31924098819406`).
- **O0.2** `eszkozok/cremer_ocr_javit.py`: lapkép-kivágás a jp2-zipből (kicsomagolás nélkül, laponként), hOCR-feldolgozás, OpenRouter-hívás (C1–C3), egyezés (C4), alakellenőrzés (C5), költségnapló és plafon (C6). Kulcs csak környezeti változóból. `--levelek`, `--pilot`, `--szaraz` (hívás nélkül: csak a bemenetek előállítása és a becsült tokenszám) kapcsolók.
- **O0.3** `eszkozok/cremer_ocr_config.json` (modellnevek üresen hagyva — a felhasználó tölti ki), `--szaraz` futás a 20 pilot-lapra: becsült token és költség jelentve.

- **O0.4** *(v2)* Eszközjavítás a v2 C1–C7 szerint. Tartalma:
  - bbox-skálázás (D9);
  - sorkontextus, `szo_ids` és `extra` (C2–C3);
  - előnormalizálás és `hiba` állapot (C4);
  - `usage`-alapú költségszámítás a gondolkodási tokenekkel (C6);
  - `temperature: 0`, `reasoning` a configból, JSON-séma, HTTP-újrapróba;
  - nyers válasz-gyorsítótár a `konkordancia/_nyers/cremer_cache/<modell>/<level>.json` alatt, kulcs: levél + modell-azonosító + prompt-verzió. Ebből a döntések hívás nélkül újraszámolhatók, és erre épül a folytatás (O2.1) (D12).

  Hívás nélküli önteszt: `--onteszt`.

### O1 — pilot ⛔
- **O1.1** Futás a 20 lapra. Kimenet: `naplok/CREMER_O1_csere.tsv` (`szo_id`, `szo_ids`, `level`, `bbox`, `ocr`, `m1`, `m2`, `dontes`, `alak_igazolt`, `extra`), `naplok/CREMER_O1_koltseg.tsv`. **Összehasonlító futás** (D14): ugyanez a 20 lap m2 = `tartalek_m2` (`google/gemini-3.1-flash-lite`) beállítással, a `naplok/CREMER_O1_lite/` alá. Az m1 válaszai a gyorsítótárból jönnek, új hívás nélkül.
- **O1.2** Ellenőrző csomag a kézi átnézéshez: 300 véletlen `auto` csere (rögzített maggal), valamint minden `vitas` és `extra_*` sor. Mindegyik mellett a lapkép kivágott része: a szó bbox-a egy sornyi környezettel, legfeljebb 800 px széles JPEG. A kivágások és a tsv **commitolva** kerülnek a `naplok/CREMER_O1_ellenorzes/` alá. Mellé egy GitHubon renderelődő oldalsorozat készül (`ATNEZES_01.md`, `ATNEZES_02.md` …, oldalanként 50 sor), soronként: sorszám, kép, hOCR-alak, m1, m2, döntés és üres ítélet-oszlop. Ezt a felhasználó távoli elérésből nézi át (D13).
- **O1.3** Jelentés: `naplok/CREMER_O1_jelentes.md` — egyezési arány, `vitas`/`hianyzo`/`hiba`/`extra_*` arány, alakellenőrzés-arány, tényleges költség (a gondolkodási tokenekkel) és a teljes kötetre vetített költség, mindkét m2-re. Mellette az összehasonlítás: a két m2 egyezése ugyanazokon a gyanús szavakon, és azok a szavak, ahol a két beállítás `auto` alakja eltér. **ÁLLJ** — a kézi ellenőrzés és a C7 küszöb után a felhasználó dönt a teljes futásról és az m2 választásáról.

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
| O1 | `auto` hibák a kézi mintán: 0 a 300-ason, vagy ≤ 1 a 600-ason (C7) |
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
| K5 | a tényleges (`usage`-alapú) költség ≤ plafon; költség- és tokennapló laponként |
| K6 | a render által használt szócikkekben nincs feloldatlan `vitas` sor |
| K7 | TSV-kezelés `csv` modul nélkül; TSV-mezőben nincs sortörés |
| K8 | commitok a §6 szerint; `git status --porcelain` üres |

---

## 6. Commitok

| Üzenet | Fájlok |
|---|---|
| `CREMER_OCR_BRIEF.md v1` | `CREMER_OCR_BRIEF.md` |
| `CREMER_OCR_BRIEF.md v2` | `CREMER_OCR_BRIEF.md` |
| `O0: Cremer OCR-javító eszköz, config, nyers-fájl SHA-k` | `eszkozok/cremer_ocr_javit.py`, `eszkozok/cremer_ocr_config.json`, `konkordancia/README.md`, `.gitignore` |
| `O0.4: eszközjavítás (bbox, szo_ids, usage-költség, gyorsítótár), modellek a configban` | `eszkozok/cremer_ocr_javit.py`, `eszkozok/cremer_ocr_config.json` |
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
| D8 | A modellek rögzítve: m1 `qwen/qwen3-vl-32b-instruct`, m2 `google/gemini-3.8-flash` `low` szintű gondolkodással; tartalék a `google/gemini-3.1-flash-lite` (C1) | OpenRouter-árak 2026.09.24-én. A `--szaraz` futás szerint laponként kb. 6 900 bemeneti és 1 400 kimeneti token kell, így a teljes kötet kb. 1,3 USD (m1) + 10 USD (m2), gondolkodás nélkül. A D7 becslése elavult, mert a Gemini Flash ára emelkedett. Korlátozás nélkül a gondolkodási tokenek miatt a 20 USD-s plafon közelébe kerülne a költség |
| D9 | A bbox a kiküldött JPEG méretére skálázva (C2) | az O0 eszköze a kicsinyített képhez az eredeti jp2 koordinátáit küldte, így a modell rossz helyen kereste volna a szavakat |
| D10 | Többtokenes csere (`szo_ids`), sorkontextus és `extra` jelzés (C2–C3) | a torz görög szó a hOCR-ben gyakran több tokenre esik. A csupa kisbetűs, magas `x_wconf`-ú torzképeket (pl. `rov`) a gyanús-szabály nem fogja meg; az `extra` ezeket a pilotban mérhetővé teszi, az alkalmazásuk külön döntés |
| D11 | Előnormalizálás az egyezés előtt; az írásjel az alakon kívül marad (C4) | az NFC nem egyesíti az aposztróf- és koronisváltozatokat, sem a lunáris és a szóvégi szigmát, ezért nélküle hamis `vitas` sorok keletkeznének. Az írásjel a hOCR-ből jön, így a K3 teljesül |
| D12 | Költség a `usage`-ből; külön `hiba` állapot; `temperature: 0`; nyers válasz-gyorsítótár (C3, C4, C6) | az O0 eszköze éles futásnál is becslésből számolt, így a plafon nem védett és a gondolkodási tokenek kimaradtak. A gyorsítótárból a döntési szabály változása hívás nélkül újraszámolható, és az API-hiba nem keveredik a `hianyzo` állapottal |
| D13 | Kézi minta 300 elem (vagy 600 elem, legfeljebb 1 hibával); az ellenőrző kivágások commitolva, GitHubon renderelt oldalakon (C7, O1.2) | 200 hibátlan elemnél a hibaarány 95%-os felső becslése kb. 1,5%, így a < 1% nem igazolható. A felhasználó csak távolról éri el a repót, a `_nyers` alatti képeket nem látná |
| D14 | A pilot két m2-vel fut: `google/gemini-3.8-flash` és `google/gemini-3.1-flash-lite` (O1.1, O1.3) | a teljes kötet becsült ára kb. 14,5, illetve kb. 6 USD. A különbség csak akkor éri meg, ha a Flash Lite a politonikus görögön érezhetően több `vitas` sort vagy hibát ad. Az összehasonlító futás kb. 0,10 USD, mert az m1 válaszai a gyorsítótárból jönnek |
