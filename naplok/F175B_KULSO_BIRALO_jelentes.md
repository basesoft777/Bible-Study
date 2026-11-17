# F175.B: külső (nem Anthropic) vak bírálók a Károli–Strong mintán, jelentés

*2026-11-17 · ág: `claude/johd-kulso-biralo-4908a2` · végrehajtó: claude-opus-5-5 · döntés: DT-F175Ba*

## 1. Cél és protokoll

A #172 pontosságmérése (95,06%) egy vak Opus-bírálóra épült. Ezt egy lektor így kifogásolta: „Anthropic-modell bírál Anthropic-modellt”. Ezért két más gyártójú modell ugyanazt az 1 600 rétegzett mintapárt ugyanazzal a vak protokollal ítélte meg:

- **Bemenet:** a `f172/ellenor/utasitas.md` és a `f172/ellenor/bemenet/koteg_001–072.txt`, bájtra változatlanul. Ez a 72 köteg az 1 600 mintapárt és a régi arany céljait tartalmazza, összesen 2 315 célt. A gépi pár és az Opus ítélete nem kerül a promptba; ezt teszt ellenőrzi (`teszt_kulso_biralo.py`).
- **Egyetlen eltérés:** egy keretmondat. Az Opus fájlba írta a JSON-t, itt a JSON maga a válasz.
- **Modellek:** `google/gemini-4-argon` és `openai/gpt-6.1-sol`, OpenRouteren, alapbeállítással, a gondolkodást nem állítottuk. A `modell` mezőbe az API-válasz tényleges modellazonosítója kerül. A modellek önbevallása eltér: a GPT „gpt-5”-nek, a Gemini „gemini-3.1-pro”-nak nevezi magát.
- **Mód:** a próba után a felhasználó döntésére azonnali (nem batch) módban futott, GitHub Actionsből (`.github/workflows/f175_kulso_biralo.yml`).
- **Kapu:** minden válasz a #172 kapuján megy át (`pontossag_ellenor.kapu`, paraméterezett mappával és modell-ellenőrzéssel): minden cél pontosan egyszer szerepel, csak létező eredeti sorszámmal.
- **Gépi alak-normalizálás, a tartalom változatlan:** ha a modell egy vers-elemet JSON-szövegként adott, a futtató dekódolja. Ez a próbabatchben (Gemini) fordult elő; a teljes futásban egyszer sem.
- **Újrakör:** a Gemini 8 kötegének első válasza nem volt érvényes JSON (7 válasz `thought` szóval, a `koteg_036` koreai szöveggel kezdődött). Mindegyiket egyszer újrahívtuk, és a második válasz átment a kapun.
- **Mérés:** a 95,06%-kal azonos módon (`pontossag_meres.py --biralo …`). A pár helyes, ha a gépi pár eredeti tokenje benne van a bíráló által jelölt halmazban. A becslés a `f172/keret.tsv` rétegsúlyával rétegzett, 95%-os normál intervallummal.

## 2. Pontosságbecslés (rétegsúlyozott, 1 600 pár)

| bíráló | ÓSZ | ÚSZ | **összes** | tartalmi szó | morféma |
|---|---|---|---|---|---|
| Opus (claude-opus-5-5, #172) | 94,50% | 97,07% | **95,06%** [93,81; 96,32] | 96,44% | 90,74% |
| Gemini (google/gemini-4-argon) | 95,65% | 97,33% | **96,02%** [94,87; 97,17] | 97,38% | 91,85% |
| GPT (openai/gpt-6.1-sol) | 95,16% | 97,10% | **95,59%** [94,39; 96,79] | 97,03% | 91,10% |
| többségi ítélet (2/3) | 95,05% | 97,07% | **95,49%** [94,28; 96,71] | | |
| mindhárom helyesnek ítélte (egyhangú gépi ítélet) | 93,23% | 96,33% | **93,91%** [92,51; 95,32] | | |

„Mindhárom helyesnek ítélte (egyhangú gépi ítélet)”: a pár csak akkor helyes, ha mindhárom bíráló annak ítéli (1 513 pár).

**Kalibráció a régi arannyal** (374 hármas, halmaz-definíció):

| bíráló | egyezés |
|---|---|
| Opus | 96,79% |
| Gemini | 97,06% |
| GPT | 96,79% |
| gépi pár | 97,06% |

Forrás: `f172/kulso_biralo/<rov>_azonnali/meres_eredmeny.tsv`, `egyezes.tsv`.

## 3. Egyezés (a mintán, súlyozatlan)

| | pár-ítélet egyezése | Cohen-kappa | jelölt halmaz pontos egyezése |
|---|---|---|---|
| Opus–Gemini | 1561/1600 = 97,56% | 0,690 | 93,13% |
| Opus–GPT | 1571/1600 = 98,19% | 0,776 | 95,63% |
| Gemini–GPT | 1578/1600 = 98,62% | 0,813 | 95,37% |
| **háromutas** | **1555/1600 = 97,19%** | | 92,31% |

A kappa a magas alapgyakoriság mellett (95% feletti „helyes”) óvatos mérőszám. A két külső bíráló egymással valamivel jobban egyezik, mint bármelyik az Opusszal.

## 4. Eltérések

Nem egyhangú pár-ítélet: **45 pár** (`f172/kulso_biralo/elteresek.tsv`, indoklással, a bírálók halmazával).

- 23 párban az Opus áll kisebbségben (a két külső bíráló egyezik ellene), 22 párban az egyik külső bíráló.
- 27 tartalmi és 18 morfémapár.
- Rétegenként: Mózes 11, történeti 10, próféták 9, ÚSZ levelek 6, Jelenések 5, költői 2, evangélium 2.

Mind a 45 tétel az emberi validáció célzott részébe kerül (a felhasználó döntése).

## 5. Fagyasztás

A három gépi ítélet páronkénti táblája az emberi válaszok beérkezése előtt került a repóba:

- **Fájl:** `f172/kulso_biralo/harom_biralo_itelet.tsv`.
- **Tartalom:** 1 600 sor; mindhárom bíráló halmaza és ítélete, valamint a többségi és az egyhangú ítélet.
- **Kulcs:** `f172_id`, a #172 `minta_id`-je, egyben a validációs minta `f172_id` oszlopa.
- **SHA-256:** `e236146d9f13a08e31427f95ccdbb692bfb3f102964f53184517fc8f083f28b7`, a `.sha256` fájlban. A commitolt blobbal ellenőrizve; a TSV `eol=lf`, a hash ezért checkouttól független.
- **Commit:** F175.B7.

## 6. Költség (OpenRouter `usage`, `f172/kulso_biralo/batchek.tsv`)

| futás | bemenet | kimenet | USD |
|---|---|---|---|
| próba: Gemini batch, 1. köteg | 16 062 | 835 | 0,0202 |
| próba: GPT azonnali, 1. köteg | 14 750 | 890 | 0,0458 |
| teljes: Gemini azonnali, 72 köteg + 8 újrahívás | 1 254 258 | 58 227 | 2,9139 |
| teljes: GPT azonnali, 71 köteg (az 1. a próbából) | 1 029 601 | 54 261 | 3,1165 |
| **összesen** | | | **6,0964** |

A függő GPT-próbabatch (1. köteg) a futás végén még nem készült el; ha megjön, kb. 0,02 USD-vel nő a költség (N-F175Ba).

## 7. Eszközök

- `eszkozok/karoli_strong/kulso_biralo.py`: batch- és azonnali futás, kapu, napló, plafon.
- `eszkozok/karoli_strong/teszt_kulso_biralo.py`: 17 teszt, kitalált válaszokon.
- `eszkozok/karoli_strong/pontossag_meres.py`: `--valasz/--kimenet/--biralo`; az alapkimenet változatlan.
- `eszkozok/karoli_strong/pontossag_ellenor.py`: a kapu paraméterezve.
- `eszkozok/karoli_strong/kulso_biralo_ertekel.py`: a háromutas összevetés és a fagyasztott tábla.
- `.github/workflows/f175_kulso_biralo.yml`: a futás, az `f172/kulso_biralo/futtatas.txt` push-ára.

## 8. Javítókör (a független ellenőrzés és a lektor, 2026-11-17)

**A fagyasztott tábla oszlopai** (a tábla nem változott, SHA-256 változatlan; kódkönyv: `f172/kulso_biralo/KODKONYV.md`): az `egyhangu` = 1, ha a három bíráló pár-ítélete azonos (mindhárom helyes VAGY mindhárom hibás; 1 555 pár, benne a 42 mindhárom által hibásnak ítélt). A közölt 93,91% ettől különböző szám: „mindhárom helyesnek ítélte (egyhangú gépi ítélet)”, 1 513 pár, rétegsúlyozva.

**Hány bíráló mondta hibásnak** (a mintán, súlyozatlan): 0 → 1 513 · 1 → 22 · 2 → 23 · 3 → 42; legalább egy: 87, mindhárom: 42. Hibajelölések: Opus 72, GPT 63, Gemini 59. A hibás osztály átfedése (metszet/unió): Opus–Gemini 46/85 = 54,1%, Opus–GPT 53/82 = 64,6%, Gemini–GPT 50/72 = 69,4%. A hibás párokban a bírálók egyezése mérsékelt.

**Egyezés x/n alakban** (a mintán, súlyozatlan): pár-ítélet 1561/1600 = 97,6% · 1571/1600 = 98,2% · 1578/1600 = 98,6% · háromutas 1555/1600 = 97,2%; halmaz 1490/1600 = 93,1% · 1530/1600 = 95,6% · 1526/1600 = 95,4% · háromutas 1477/1600 = 92,3%.

**Futtatási beállítások.**
- Mindkét külső modellnél: `response_format: {"type": "json_object"}`, `max_tokens: 32000`, `usage: {include: true}`; temperature és gondolkodás nem állítva (alapbeállítás). Ez eltér az Opus-futástól, amely Claude Code subagentként, előfizetésből futott (DT622 (u1)), a JSON-t fájlba írta, válaszformátum-kényszer és kimeneti korlát nélkül; a gondolkodási beállítása a repóból nem tudható.
- **A Gemini gondolkodási tokenje valódi 0**, nem naplózási hiány. Diagnosztika (`f172/kulso_biralo/diagnosztika_gemini.json`, 0,189 USD): az 1. köteg a futás törzsével → 728 kimeneti, 0 gondolkodási token (a kimenet a látható JSON); ugyanaz `reasoning: {effort: high}` mellett → 11 766 kimeneti, ebből 11 048 gondolkodási token, ugyanazzal a naplózással. A teljes futásban tehát a Gemini gondolkodás nélkül bírált; a GPT kötegenként átlag ~220 gondolkodási tokennel (15 743 / 72).

**A modellek azonosítása.** A kéziratba csak: az OpenRouter-azonosító (`google/gemini-4-argon`, `openai/gpt-6.1-sol`), a közvetítő (OpenRouter) és a dátum (2026-11-17). A slug a mögötte futó modellt nem igazolja függetlenül (az OpenRouter útválasztására hagyatkozunk). Az önbevallás eltér (GPT: „gpt-5”, „gpt-5.2” stb.; Gemini: „gemini-3.1-pro(-preview)”), ez külön mezőben áll. A Gemini két szolgáltatón futott (Google, Google AI Studio); a kérésenkénti bontás a teljes futásban nem naplózódott (a futtató azóta kérésenként naplózza).

**Az újrahívás szabálya előre rögzített volt:** „a kapun elbukott vagy érvénytelen JSON-ú köteg egyszer újrahívva” — a F175.B6 commitban (8ac0bd64), a teljes futás (44057382235) előtt. A 8 elvetett Gemini-válasz közül 7 `thought` szóval, a `koteg_036` koreai szöveggel kezdődött, utána érvényes JSON. **Érzékenységvizsgálat:** az elvetett válaszok JSON-részével számolva a bennük lévő 167 mintapár egyikének ítélete sem változik (a 268 cél közül 10-nél más a halmaz).

**A függő GPT-próbabatch** (N-F175Ba) bármit ad, a fagyasztott táblát nem cseréli; csak a batch és az azonnali mód egyezésének jele.

**A workflow** csak a `claude/johd-kulso-biralo-4908a2` ágon fut; a `futtatas.txt` merge-kori állapota `muvelet=nincs`.

**Költség** a diagnosztikával: 6,0964 + 0,1890 = **6,2854 USD**.
