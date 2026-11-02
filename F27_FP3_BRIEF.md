---
feladat: 27
cim: "Thayer-fordítás Sonnettel: felmérés és mérő adag a #132 szakaszos láncán, API-n (Batch)"
kod: FP3
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: "a Thayer teljes Sonnet-fordításának mért alapja a #7-hez: a szakaszos lánc (#132) teljes Thayerre vett hiányai, gyakorisági sorrend és adagterv, egy kb. 150 ezer karakteres mérő adag API-n (Batch) az adat/forditasok.tsv-ben (szakaszsorok, allapot=sonnet), aranyminta-összevetés, költségmérés (USD) és kivetítés a teljes Thayerre"
kovetkezo: "/kovetkezo a #158 (Thayer API-kötegelő) lezárása után; a D46 feloldva (DT-F27a)"
olvas: [F132_THAYER_SZAKASZ_BRIEF.md, F142_THAYER_M3_BRIEF.md, F153_THAYER_KAROLI_TELJES_BRIEF.md, F158_THAYER_API_KOTEG_BRIEF.md, naplok/F132_THAYER_SZAKASZ_naplo.md, naplok/THAYER_API_KOTEG_naplo.md, adat/thayer_szakaszok.tsv, adat/thayer_forras_javitas.tsv, adat/thayer_vers_jelentes.tsv, adat/thayer_sigla.tsv, adat/tiltott_fordulatok.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/karoli_strong/, adat/SEMA.md, konkordancia/Konyv_normalizalo_tabla.tsv, forditas/prompt_v5_1.md, eszkozok/thayer_jelolt/, eszkozok/thayer_api_koteg.py, eszkozok/forditas_kapuk.py, eszkozok/normalizal.py, DONTESEK.md]
ir: [adat/forditasok.tsv, naplok/F132_THAYER_SZAKASZ_munka.tsv, naplok/F132_THAYER_SZAKASZ_bukottak.tsv, forditas/thayer_api/, naplok/FP3_naplo.md, naplok/FP3_sorrend.tsv, naplok/FP3_hibas.tsv, naplok/FP3_M0.py, naplok/FP3_arany.md, DONTESEK.md]
fugg: [158]
---

# F27_FP3_BRIEF.md — Thayer-fordítás Sonnettel: felmérés és mérő adag a #132 szakaszos láncán, API-n

*FELADATOK #27 · Modell: sonnet · v3 · 2026.11.02 · a #7 (Thayer éles) briefjét készíti elő*

**Módosítva (2026.11.02, DT-F27a): a D46 feloldva, szakaszos lánc, API.** A felhasználó a D46 halasztását a #27-re és a #7-re
feloldotta. A v2 a régi, teljes szócikkes láncra épült (`forditas/prompt_v4.md`, `eszkozok/emeles.py`); az azóta lezárt #132
(THAYER_SZAKASZ) szakaszos láncot épített a Thayerre, és a #142 (THAYER_M3) és a #153 (THAYER_KAROLI_TELJES) ezen fordított. A v3
ezt a láncot veszi át. A fordítás nem sessionből, hanem API-n (Message Batches, `PARDES_API_KEY`, a meglévő API-keretből) fut, a
#158 (THAYER_API_KOTEG) kötegelőjével. A teljes futás (M2 … Mn, Mz) a #7 dolga; annak briefje ennek az eredményéből készül.

## 1. Cél

Két kérdésre ad mért választ:

1. **Alkalmasság:** a #132 szakaszos lánca (`thayer_jelolt/forditas.py`, prompt v5.1, adatblokk, javítóréteg, 1–16. kapu,
   terminológia, sigla-tábla), amely eddig a motívumok görög gerincszavain (kb. 15 Strong) futott, mennyire viszi a teljes Thayert
   változtatás nélkül, és hol kell hozzányúlni?
2. **Mennyiség:** egy API-n futó mérő adag alapján mennyi költséget (USD) és átfutást kíván a teljes Thayer (5 426 Strong,
   17 093 szakasz, kb. 4,44 millió karakter)?

A #7 fejlécéhez és csonkjához ez a feladat nem nyúl.

## 2. Hatókör

**Benne van:** M0 felmérés (csak olvas és mér); M1 mérő adag (kb. 150 000 forráskarakter) a #158 kötegelőjével, Batch-on,
`allapot=sonnet`; aranyminta-összevetés; költségmérés és kivetítés; jelentés; döntési tétel.

**Nincs benne:** más modell; az M1 utáni adagok; az `F07_THAYER_ELES_BRIEF.md` módosítása; a #132 eszközeinek
(`eszkozok/thayer_jelolt/`), a `forditas_kapuk.py`-nak, a `normalizal.py`-nak, a `prompt_v5_1.md`-nek és a #158 kötegelőjének a
módosítása (hiba esetén megállás, tétel a `DONTESEK.md`-be); a sigla-tábla jóváhagyása (a felhasználóé, DT335 (3)); a `kezi` sorok
jóváhagyása (DT290 (3)); a forrás javítása.

## 3. Kiinduló tények (a brief írásakor; a menet újraméri, eltérésnél a saját mérése az irányadó, és naplózza)

| Tétel | Érték |
|---|---|
| Thayer szakasztábla | `adat/thayer_szakaszok.tsv`: 17 093 szakasz, 5 426 Strong (#132 zárása) |
| Kész szakaszos Thayer-sorok | a #142 és a #153 sorai (2026-11-01-i felmérés: `sonnet` 71 sor / 13 Strong, `kezi` 5, `opus` 2, `elavult` 7; `F153_THAYER_KAROLI_TELJES_BRIEF.md` 2.) — a futás listája kihagyja, ami érvényes (`kesz`) |
| Lánc | `eszkozok/thayer_jelolt/forditas.py` `lista` / `elokeszit` / `ellenoriz` / `rogzit` / `beir`; prompt `forditas/prompt_v5_1.md` (DT336 (2)); `{{ADATBLOKK}}`: `thayer_jelolt/adatblokk.py` (a Károli-mankó a teljes ÚSZ-re, #153); kapuk: a közös sor `14_szakasz`, `15_tiltott` és a Thayer-féle `16_sigla` (`thayer_kapuk.py`) |
| A `lista` hatóköre | ma a motívumok gerincszavai (`szolista.py`, DT332 (1)); a teljes Thayer listáját a #158 adja |
| Fordító út | a `forditas.py` nem fordít (docstring); a fordítást a #158 `thayer_api_koteg.py`-ja végzi Batch-on, a `forditas.py` függvényeit importálva |
| Régi `teljes` sorok | DT329 (a)+(i)+(ii): a nem `kezi` régi sor `elavult`, a `kezi` sor érvényes marad a jóváhagyásig; a `forditas.py` a végleges `DT329`-et írja (#155, [PR #567](https://github.com/basesoft777/Bible-Study/pull/567), merge: 2026-11-02) |
| BDB-tapasztalat API-n | `eszkozok/bdb_api_koteg.py` (#38, a 13. adagtól): Batch-ár, plafon, `futasnaplo.tsv` USD-ben, cache a B-úton kikapcsolva |

*(proveniencia: scope=F132/F142/F153/F155 brief és zárás, `eszkozok/thayer_jelolt/forditas.py` docstring, `gh pr view 567` |
forras=manual — a befogadó olvasása | ts=2026-11-02)*

## 4. Előfeltételek, függések és kockázatok (az M0 rögzíti és újraméri)

| # | Tétel | Állapot a brief írásakor | Kezelés |
|---|---|---|---|
| E1 | **#158 THAYER_API_KOTEG** — a Thayer Batch-kötegelője (`eszkozok/thayer_api_koteg.py`) és a teljes Thayer listája | nem indult | **függés** (`fugg: [158]`); nélküle az M1 nem fut |
| E2 | **#155** — a `forditas.py` a végleges `DT329`-et írja | lezárva, mergelve (PR #567, 2026-11-02) | teljesült; az M0 egy sorban igazolja (`grep DT329 eszkozok/thayer_jelolt/forditas.py`) |
| E3 | **Sigla-tábla** (`adat/thayer_sigla.tsv`): 164 `jelolt` / 91 `besorolt` sor; a `16_sigla` kapu csak a `besorolt` sort kötelezi (DT335 (3)) | a gerincszavakra jóváhagyva (F142.1); a teljes Thayerre nem | **kockázat:** a gerincen kívüli szócikkek siglái `jelolt` állapotban maradnak, a kapu nem védi őket. Az M0 megméri, hány `jelolt` sigla fordul elő az M1 adagjában és a teljes Thayerben; a jóváhagyás a felhasználóé (a ⛔ M1 kérdése) |
| E4 | **N66** — a `teszt_lanc.py` `Sigla.test_tabla_determinisztikus_es_kezi_vedett` tesztje a `main`-en is bukik | nyitott (`NYITOTT_FELADATOK.md`) | **kockázat:** a `teszt_lanc.py` 39/40, amíg az N66 nyitott; a zöld feltétel ennél a tesztnél „ismert, N66”, minden más teszt zöld |
| E5 | **N-F142a** — a fordításban álló „Sir <c:v>” (Sirák fia) a `lekerdez.py` / `nave_bontas.py` szerint JSir-alias | nyitott | **kockázat:** a fordítást nem gátolja, de a teljes Thayerben a Sirák-hivatkozások száma nő; az M0 megszámolja a `Sir` előfordulásait a forrásban, a ⛔ M1 kérdésként viszi (javítás a #7 előtt?) |
| E6 | **Ütközés az `adat/forditasok.tsv`-n**: #38 (BDB), #154, #86 | a `feladatok.py fuggesek` szerint `KIZAR 27↔38`, `KIZAR 154 27`, `FUGGES 27 154`, `FUGGES 86 27` | a #27 nem fut egy időben a #38 adagjával vagy a #154-gyel; a `beir` írás előtt összevet, minden más sor bájtra azonos |

## 5. Lépések

### M0 — Felmérés (csak olvas és mér; `naplok/FP3_M0.py`, eredmény a `naplok/FP3_naplo.md`-be)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka. A fordítás modelljét a
   kötegelő naplózza; az adattábla `modell` mezőjébe a ténylegesen futott API-modell neve kerül a kötegelő kimenetéből.
1. **Előfeltételek** (4. pont E1–E6) igazolása, proveniencia-sorral.
2. **Lánc-próba szárazon a teljes Thayeren.** A `forditas.py elokeszit` minden Strongra (a scratchpadbe), és a #158 kötegelő
   hálózat nélküli `szaraz` futása: melyik Strongnál hibázik az előkészítés (pl. üres szakasz, illesztési hiba, a 20 000 karakter
   fölötti csoportok), hány kérés, hány csoport. Próbaanyag a kapukra: a kész szakaszos sorok (`sonnet`, `kezi`) újrakapuzása
   (`ellenoriz`) — hány jelzés, melyik kapun. Táblázat: lépés · fut-e · eltérés.
3. **Könyv- és hivatkozásfedés.** A Thayer igehely-előtti könyvalakjai közül melyiket nem képezi le a
   `Konyv_normalizalo_tabla.tsv` és a `normalizal.py` (a `11_konyvek` kapu szerint). Külön sor: a Sirák (E5), a Kelemen-hivatkozás
   (`1 Cor. 20, 5`), a klasszikus szerzők.
4. **Sigla-fedés** (E3): a `jelolt` és `besorolt` sziglák előfordulása a teljes Thayerben és az M1-jelölt adagban.
5. **Terminológia.** Az `adat/terminologia.tsv` görög/Thayer-releváns sorai; a Thayer leggyakoribb angol szakkifejezései közül
   melyiknek nincs sora (javaslatlista, a fájl nem változik).
6. **Sorrend** (`naplok/FP3_sorrend.tsv`: `sorszam`, `strong`, `gyakorisag`, `karakter`, `szakasz`, `adag`). A #158 teljes listájából,
   Károli ÚSZ Strong-gyakoriság szerint csökkenő (`adat/karoli_strong/` párosítása; a teljes ÚSZ lefedett, #22, #153). Egyenlőségnél a
   Strong-szám. A `kesz` Strongok kimaradnak.
7. **Adagterv:** M1 kb. 150 000 forráskarakter; utána kb. 500 000 karakteres adagok (a #7-nek). A Batch-csomagolás a #158 szerint.

**Megállás az M0 után csak akkor**, ha a 2. pont szerint a lánc vagy a kötegelő valamelyik lépése a teljes Thayeren blokkolóan nem
fut. Ekkor ⛔: jelentés, a felhasználó dönt (eszközjavítás külön feladatban, vagy leállás). Egyébként a ⛔ M1-plafon következik.

### M1 — Mérő adag (API, Batch)

1. **⛔ Költségplafon:** a #158 `szaraz` becslése alapján a felhasználó megadja az M1 USD-plafonját (a `bdb_api_koteg.py`
   `PLAFON_USD` mintájára); ez az egyetlen indulás előtti várakozás. Plafon nélkül nincs beküldés.
2. **Fordítás** a sorrend első kb. 150 000 forráskarakterén a #158 kötegelőjével: `szaraz` → `bekuld` → `allapot` → `begyujt` →
   `kapuz` → `javit` (egy javító kör a kapu hibaüzenetével) → `rogzit` (`--allapot sonnet`, a tényleges modellnévvel) → `beir`
   (nem `kezi` régi sorral `--regi-elavult`, `kezi` régi sorral `--kezi-marad`; DT329 (i)/(ii)). A kétszer bukott Strong a
   `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be és a `naplok/FP3_hibas.tsv`-be kerül (strong, kapu, szakasz, ok).
3. **Aranyminta** (`naplok/FP3_arany.md`): az 5 `kezi` Thayer-Strong (G0282, G1941, G1944, G4151, G5590) szakaszos fordítása a
   kötegelővel, **csak a naplóba** (az `adat/forditasok.tsv`-be nem írja). Strongonként forrás, `kezi` és Sonnet egymás alatt, a
   kapueredmény, és a feltűnő eltérések felsorolása (ítélet nélkül).
4. **Költségmérés:** a kötegelő `futasnaplo.tsv`-je (bemeneti, kimeneti, cache-token, USD Batch-áron) — mért érték, nem becslés.
5. **Kivetítés** a teljes Thayerre hosszkategóriánként, a mért adagból, a valódi szakasz- és csoporthosszakkal (nem átlag ×
   darabszám; a F21 PD4 tanulsága). Becslés nem kerül mért érték helyére, és jelölve marad.

### ⛔ M1 — Jelentés és döntés

A szokásos adagjelentésen felül (`naplok/FP3_naplo.md`):
- az adag Strong-, szakasz- és karakterszáma, kapueredmények kapunként, a javító kör és a hibás lista összesítése, a téves riasztás /
  valódi hiba szétválasztásával (a BDB M2-elemzés kategóriái szerint);
- 5 véletlen Strong (seed = 27, hossz szerinti harmadokból) forrás és fordítás egymás alatt, hogy a felhasználó beleolvashasson;
- az aranyminta-összevetés;
- a költségmérés és a kivetítés;
- egy `DONTESEK.md`-tétel (`DT-F27b`) a felhasználó döntéseivel: (a) a #7 indulhat-e ezzel a lánccal és kötegelővel; (b) a M0-ban
  talált hiányok közül mit kell a #7 előtt javítani (sigla-jóváhagyás a teljes Thayerre, E3; a Sirák-alias, E5; normalizáló-alias,
  terminológia, prompt), külön feladatként vagy a #7 M0-jában; (c) a #7 költségplafonja és adagmérete.

## 6. Szabályok (a #132, a #142 és a BDB API-menetéből)

- **Egy session = egy ág = egy PR.** Ágnév: `claude/f27-fp3`.
- **A modellcímke a valódi modell:** az adattábla `modell` mezője a ténylegesen futott API-modell neve a kötegelő kimenetéből;
  briefből vagy korábbi sorból másolni tilos.
- **A prompt, a terminológia, a sigla-tábla és a kapuk futás közben nem változnak.** Javítás csak a ⛔ M1 után, jóváhagyással; az M1
  sorait ez nem fordítja újra, csak ha a felhasználó kéri.
- **Kapuhiba:** egy javító kör a kapu hibaüzenetével; ha az sem megy át, a Strong a hibás listára kerül, és a futás továbbmegy.
- **Szellem-szabály** (DT25, DT-F38g): az dönt, kire vonatkozik a szó; az isteni πνεῦμα „Isten Szelleme”, „Szent Szellem”, „a
  Szellem”, minden más kisbetűs; a kétséges a listára kerül.
- **Ami R. V. / A. V. után áll, angolul, szó szerint marad** (DT-F38f 5; a prompt Thayer-kiegészítése is így rendelkezik).
- **Forráshiba:** a fordítás hűen viszi; a javított forrásnézet (`adat/thayer_forras_javitas.tsv`, DT333 (2)) az irányadó.
- **`kezi` és `opus` sorhoz** a menet nem nyúl (a `kezi` régi sor a DT329 (ii) szerint érvényes marad).
- **A kulcs** a `PARDES_API_KEY` környezeti változóból jön; nem íródik ki, fájlba és naplóba nem kerül.
- **A plafon kemény:** a kötegelő csomagonként ellenőrzi; a plafon elérése megállás, nem emelés.
- **Commit** csomagonként és az adag végén; minden commit után push. A scratchpadben nem maradhat semmi, ami kell.
- **TSV:** `split('\t')` / `'\t'.join()`, a `csv` modul tilos. **Shell:** magyar, görög vagy héber szöveget tartalmazó szkript
  fájlból fusson.

## 7. Munkaszabályok

1. **Számok** csak a menetben futtatott parancsból vagy a kötegelő naplójából; becslés nem kerül mért érték helyére.
2. **Megállás** az M1 plafonjánál, a ⛔ M1-nél, és az M0 után csak blokkoló hiánynál. Minden más kérdés a DT-F27b-be gyűlik (D19).
3. **Zárás a `/kovetkezo` szerint:** `fuggetlen-ellenor`, zárójelentés, draft PR, a saját fejléc frissítése.

## 8. Kész, ha

- K1: `naplok/FP3_naplo.md` M0-szakasza a hét ponttal és az E1–E6 állapotával; `naplok/FP3_sorrend.tsv` a teljes, kész sorok
  nélküli sorrenddel.
- K2: az M1 szakaszsorai az `adat/forditasok.tsv`-ben (`allapot=sonnet`, `jelentes_szam = sz<n>`, a tényleges modellnévvel), a régi
  `teljes` sorok a DT329 szerint; minden más sor bájtra változatlan; `python eszkozok/ellenoriz.py` SÉRTÉS 0, `python
  eszkozok/feladatok.py ellenoriz` 0 hiba; a `eszkozok/thayer_jelolt/teszt_*.py` és a `eszkozok/teszt_forditas_kapuk.py` zöld (a
  `teszt_lanc.py` N66-tesztje kivétel, amíg az N66 nyitott).
- K3: `naplok/FP3_arany.md` az 5 Stronggal.
- K4: a költségmérés (USD, a kötegelő naplójából) és a kivetítés a naplóban.
- K5: a DT-F27b nyitva.
- K6: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | Opus–Gemini összevetés, Max-keret méréssel, 40 szócikkes mintán, vak pontozással és vak olvasással | C út kihagyva; helyi gép |
| v2 | 2026.10.12 | **Csak Sonnet**; a BDB-menet (#38) M0–M1-e a Thayeren: eszközlánc-próba, sorrend, mérő adag, aranyminta, keretmérés. Az `fp3/` kimenet, a prompt v4-kiegészítés, az OpenRouter és a vak összevetés elmarad. | DT121 (felhasználó, 2026.10.12); a v1 szövege a git-történetben |
| v3 | 2026.11.02 | **A D46 feloldva; a #132 szakaszos lánca és API (Batch).** A régi teljes szócikkes lánc (`prompt_v4.md`, `emeles.py`) helyett a `thayer_jelolt/forditas.py`, a prompt v5.1, az adatblokk és a 14–16. kapu; a fordítás a #158 kötegelőjével Batch-on; a keretleolvasás helyett USD-plafon és költségnapló; előfeltételek és kockázatok (E1–E6: #158, #155, sigla, N66, N-F142a, ütközések). | DT-F27a (felhasználó, 2026.11.02); a v2 szövege a git-történetben |
