# F06_FORRASFELMERES_BRIEF.md — Új források 2. felmérése (FJ 2. menet)

*FELADATOK #6 · v1 · 2026.09.29 · Modell: sonnet · Külső modell: `minimax/minimax-m3` (OpenRouter), csak a 4. lépésben · Ág: `claude/f06-forrasfelmeres`*

## Mit ad, ha kész

Döntési alapot négy nyitott kérdéshez (`NYITOTT_FELADATOK.md` N27, N29, N30, N31):

- **Nave (N27):** melyik adatforrás importálható (`basokant/nave`, `theonize/bible_database`, `elcafe7/lex`), és tisztázott-e a licenc és az eredet.
- **Teljes KJV/ASV (N29):** van-e elérhető, licencelt forrás szó-szintű Strong-illesztéssel.
- **BSB (N30):** a teljes 1Mózes (1 533 vers) versenkénti Strong-összevetése a TAHOT-tal, előre rögzített küszöbbel.
- **Macula Hebrew (N31):** teljes-e a letöltés (1Sám–2Krón), és mit ad a 87 függő LXX-helyre. **Ez a #8 bemenete.**

A menet **felmérés, nem import**. Nem kerül adat az `adat/` és a `konkordancia/` könyvtárba.

## Miért GitHub Actions, és nem helyi gép

Az FJ 1. menetében a cloud proxy blokkolta a források egy részét (N27, N29). A GitHub runnereinek nyílt az internetkapcsolata, ezért a letöltés és a mérés ott fut. A helyi gépre így nincs szükség.

## Munkamegosztás

| Lépés | Ki végzi |
|---|---|
| Szkriptek és workflow megírása | Code (sonnet), cloudban |
| Letöltés, feldolgozás, minden mérés | Python-szkript a GitHub Actionsben |
| Licenc- és eredetszöveg értelmezése | MiniMax M3 az OpenRouteren, a szkript hívja az Actionsben |
| Jelentés, döntési javaslat | Code, kizárólag a szkriptkimenetekből |
| Ellenőrzés | CI és `fuggetlen-ellenor` |

## Keretek

- **Számadat** (darabszám, százalék, versszám, lefedettség, költség) csak szkriptkimenetből kerülhet a jelentésbe. A MiniMax nem számol, és a kimenetéből szám nem kerül a jelentésbe.
- **Kulcs:** az `OPENROUTER_API_KEY` repo-secretként érhető el az Actionsben. Soha nem kerül fájlba, naplóba vagy commitba. Commit előtt futtass kulcs-grepet.
- **Nyers adat nem kerül commitba.** Csak a származtatott, kis méretű kimenetek (TSV, MD) kerülnek be, fájlonként legfeljebb 1 MB.
- **Költségplafon:** a MiniMax-hívások összköltsége legfeljebb **1 USD**. Ha a futásnapló szerint ezt elérnéd, állj meg.
- **Nincs darabolás.** Egy MiniMax-hívás bemenete legfeljebb **12 000 karakter**. A hosszabb licenc- vagy README-szöveget nem daraboljuk, hanem „kézi” jelölést kap. Ennek oka az FP2 tanulsága: darabolt bemeneten a MiniMax kitalált tartalmat írt (`naplok/FP2_jelentes.md`).
- Minden lépés után commitolj, és pusholj a távoli ágra.

## Lépések

### 0. Felmérés (csak olvas)

1. Olvasd be: `naplok/FORRAS_jelentes.md`, `NYITOTT_FELADATOK.md` N27–N31, `naplok/FORRAS_FJ1_lxx_jeloltek.tsv`, `konkordancia/Konyv_normalizalo_tabla.tsv`.
2. Határozd meg a 87 függő LXX-hely listájának forrását (fájl és oszlop), és **lekérdezéssel** ellenőrizd, hogy valóban 87 sor.
3. Nézd meg az `eszkozok/fordit.py` OpenRouter-hívóját (`_valodi_http_kuldo`, időkorlát, usage-naplózás). A 4. lépés ezt használja újra, importálva vagy kiemelve egy közös modulba. Új HTTP-klienst ne írj.
4. Listázd a forrásjelölteket URL-lel. A KJV/ASV-hez a studybible.info és az eBible.org mellett keress GitHubon is szó-szintű Strong-illesztésű alternatívát, és rögzítsd, mit találtál.

**Kimenet:** `naplok/F06_felmeres.md`.

### 1. Szkriptek és workflow

- **Szkriptek:** `eszkozok/fj2/` alatt; egy forrás = egy mérőszkript, és egy közös `futtat.py` hívja őket.
- **Workflow:** `.github/workflows/f06_forrasfelmeres.yml`.
  - Indítás: push a `claude/f06-forrasfelmeres` ágra, ha az `eszkozok/fj2/**`, a workflow-fájl vagy az `fj2/futtatas.txt` változott. Újrafuttatáshoz az `fj2/futtatas.txt`-t módosítsd.
  - `permissions: contents: write`. A kimeneteket a workflow ugyanerre az ágra commitolja. A `GITHUB_TOKEN`-nel végzett push nem indít új futást, így nincs hurok.
  - Az `OPENROUTER_API_KEY` csak a 4. lépés job-jának `env`-jében szerepel.
- A szkriptek helyben száraz futással is indíthatók (`--szaraz`: letöltés és API-hívás nélkül, a szerkezet ellenőrzésére).

### 2. ⛔ Előfeltételek a felhasználótól

**Állj meg, és kérd ezt a kettőt:**

1. **BSB-küszöb (N30):** a versenkénti Strong-egyezés elfogadási küszöbe az 1Mózesen, és az egyezés definíciója (azonos Strong-halmaz, vagy a TAHOT-halmaz lefedése). Javaslat: az egyezés = a TAHOT Strong-halmaza része a BSB-halmaznak, a 9000-es prefixkódok nélkül; küszöb 95%. **A küszöböt mérés előtt rögzítjük, mérés után nem módosítjuk.**
2. **Secret:** az `OPENROUTER_API_KEY` repo-secret beállítva (Settings → Secrets and variables → Actions).

A választ rögzítsd a `naplok/F06_felmeres.md` végén. Mérés csak ezután indulhat.

### 3. Mérések (Actions)

| Forrás | Mérés | Kimenet |
|---|---|---|
| **Nave** (3 jelölt) | elérhetőség; témakörszám; téma↔vers relációk száma; a versformátum leképezhető-e a `Konyv_normalizalo_tabla.tsv`-re (az egyező és a nem egyező könyvkódok száma); a licenc- és README-fájlok szó szerinti kigyűjtése | `naplok/F06_nave.tsv` |
| **Teljes KJV/ASV** | elérhetőség forrásonként; van-e szó-szintű Strong-illesztés; lefedettség (könyv, vers); a licencfájlok kigyűjtése | `naplok/F06_kjv_asv.tsv` |
| **BSB** | a teljes 1Mózes versenként a TAHOT-tal, a 2. lépésben rögzített definícióval és küszöbbel; a nem egyező versek listája | `naplok/F06_bsb_genezis.tsv`, `naplok/F06_bsb_elteresek.tsv` |
| **Macula Hebrew** | könyvenkénti versszám a TAHOT-hoz mérve (külön kiemelve az 1Sám–2Krón); a 87 függő helyre: mit ad a Macula (LXX-megfelelő, bizonyosság, vagy nincs adat) | `naplok/F06_macula_lefedettseg.tsv`, **`naplok/F06_macula_87_hely.tsv`** |

Minden kimenet első sorai: forrás-URL, commit vagy verzió, letöltés dátuma, futtatási parancs.

### 4. Licenc- és eredetelemzés (MiniMax M3, Actions)

A szkript a 3. lépésben kigyűjtött licenc- és README-szövegeket egyenként küldi a `minimax/minimax-m3` modellnek.

- **Paraméterek:** hőmérséklet 0; a válasz JSON a következő mezőkkel: `licenc_tipus`, `kereskedelmi_hasznalat`, `szarmaztatott_mu`, `forrasmegjeloles_kell`, `kozkincs_allitas`, `idezet`.
- **Kapu:** az `idezet` mezőnek **szó szerint** szerepelnie kell a bemenetben; a szkript ezt ellenőrzi. Ha nem szerepel, vagy a JSON hibás, egyszer újrapróbálja; ha ismét sikertelen, a tétel „kézi” jelölést kap.
- **Naplózás hívásonként:** modellazonosító, a válaszoló provider, input- és outputtokenek, költség.
- A MiniMax ítélete **javaslat**. A jelentésben mindig a szó szerinti idézet mellett áll, és a végső licencdöntés a felhasználóé.

**Kimenet:** `naplok/F06_licenc.tsv`, `naplok/F06_koltseg.tsv`.

### 5. Jelentés

`naplok/F06_forras_jelentes.md`:

- forrásonként: mérés, licenc (idézettel), javaslat (**IMPORT** / **FELTÉTELLEL** / **NEM**), indok;
- N27, N29, N30 és N31 külön-külön: lezárható-e, és ha nem, mi hiányzik;
- a #8-nak átadott rész: hány függő helyre ad a Macula LXX-megfelelőt (a `F06_macula_87_hely.tsv`-ből);
- a MiniMax-költség összesen (a `F06_koltseg.tsv`-ből).

A `naplok/FORRAS_jelentes.md` fejlécébe kerüljön ez a megjegyzés: *„Felülírva: N27–N29; az aktuális állapot: `naplok/F06_forras_jelentes.md`.”* A régi fájl többi részét ne módosítsd.

### 6. Zárás (CLAUDE.md menetzárás)

1. `fuggetlen-ellenor` → `naplok/ELLENOR_F06.md`. Kiemelten ellenőrzendő: minden jelentésbeli szám visszakereshető-e egy kimeneti fájlban, és minden `idezet` szó szerint szerepel-e a forrásban.
2. Zárójelentés: `naplok/F06_zaras.md` (legfeljebb 20 sor).
3. A `FELADATOK.md` #6-os sorának frissítése: állapot, ág, következő lépés, és a megjegyzés, hogy a menet Actionsben futott, helyi gép nem kellett.
4. Push, draft PR a main-be. A válasz első sora: a PR linkje és a CI állapota.

## Nyitó prompt (a Code-sessionbe)

> Olvasd be a repó gyökerében az `F06_FORRASFELMERES_BRIEF.md`-t és a `CLAUDE.md`-t, és hajtsd végre a briefet a 0. lépéstől, a `claude/f06-forrasfelmeres` ágon. A 2. lépésnél (⛔) állj meg, és várd a válaszomat. Számadatot csak szkriptkimenetből írj. Minden lépés után commitolj és pusholj.

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| F06-D1 | A letöltés és a mérés GitHub Actionsben fut | a runner eléri a cloud proxy által blokkolt forrásokat; nem kell helyi gép | helyi gépes futtatás (az eredeti #6-sor szerint) |
| F06-D2 | LLM csak a licenc- és eredetszövegek értelmezésére, `minimax/minimax-m3` az OpenRouteren | a mérések determinisztikusak; tokent csak ott költünk, ahol nyelvi ítélet kell | a teljes menet modellel; Claude-dal futó licencelemzés |
| F06-D3 | A MiniMax-bemenet nem darabolható (legfeljebb 12 000 karakter), a hosszabb „kézi” | FP2: darabolt bemeneten 80% kritikus hiba, kitalált tartalom | darabolás kontextussal |
| F06-D4 | Szó szerinti idézetkapu a MiniMax minden ítéletén | a modell ne állíthasson licencet a forrás szövege nélkül | a modell ítéletének elfogadása ellenőrzés nélkül |
| F06-D5 | A BSB-küszöb mérés előtt rögzítve (⛔) | N30: előre rögzített küszöb kell, különben a mérés igazodik az eredményhez | küszöb utólag, az eredmény ismeretében |
| F06-D6 | Felmérés, nem import; a nyers adat nem kerül commitba | a döntés a felhasználóé; a repó mérete | import ugyanebben a menetben |
| F06-D7 | Sorrend: 7 → 6 → 8; a #8 a `F06_macula_87_hely.tsv`-re épül | a #8 ne döntsön Macula-adat nélkül, ne kelljen utólag újranyitni | 7 → 8 → 6 (2026.09.29-én elvetve) |
