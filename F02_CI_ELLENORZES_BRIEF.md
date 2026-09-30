---
feladat: 2
cim: Gépi ellenőrzés GitHubon
kod: CI
tipus: feladat
fazis: 1
modell: sonnet
allapot: lezarva
ad: gépi ellenőrzés (E1–E16) GitHub Actionsben
kovetkezo: lezárva
lezarva_osszegzes: PR #57, merge `68eb348` (09.27); E5 javítás: PR #59
---
# F02_CI_ELLENORZES_BRIEF — független, gépi ellenőrzés a chatbeli tarball-ellenőrzés helyett

*Verzió: v1 · 2026.09.26 · Tétel-azonosító előtag: `CI.`*

<!-- KOZVETLEN_FUTTATAS -->
## Nyitó prompt (Claude Code-nak)

> Olvasd el ezt a briefet, a `CLAUDE.md`-t és az `eszkozok/ellenoriz.py` fejlécét.
> A CI.0–CI.5 tételeket sorban hajtsd végre. Minden tétel külön commit legyen,
> az üzenet a tétel-azonosítóval kezdődjön (pl. `CI.1: …`). Minden commit után
> **push a `ci-ellenorzes` remote ágra ugyanabban a lépésben**: ez a brief a push-kérés.
> A `main`-re ne merge-elj. A CI.0 kimenetét (alapállapot-számok) írd a
> `naplok/CI_alapallapot.md` fájlba, és a CI.2 előtt állj meg jóváhagyásra.
> Modell: CI.0–CI.4 Sonnet, CI.5 (ügynök-prompt) Opus.
<!-- /KOZVETLEN_FUTTATAS -->

## Cél

Ma a chat minden merge előtt letölti a teljes repót (~92 MB tarball), és fájlokat olvas be. A függetlenség megmarad, de két olcsóbb rétegre kerül át:

1. **GitHub Actions**: a determinisztikus szabályokat gép futtatja minden PR-en.
2. **`fuggetlen-ellenor` ügynök**: a mérlegelést igénylő pontokat friss kontextusban, csak olvasási joggal ellenőrzi.

A chat ezután csak a CI-státuszt (GitHub API, néhány KB) és az ügynök jelentését olvassa.

## Alapelvek

- **Az ellenőrző nem módosítható ugyanabban a PR-ben, amelyet ellenőriz.** Ha egy PR érinti az `eszkozok/ellenorzes/`, az `eszkozok/ellenoriz.py`, a `.github/` vagy a `.claude/agents/fuggetlen-ellenor.md` fájlt, a CI bukjon, kivéve ha a PR címe `[ELLENŐRZŐ]` előtagú. Ilyenkor a felhasználó külön hagyja jóvá.
- **Két szint.** `HIBA`: a PR által érintett fájlokban blokkol. `FIGYELMEZTETÉS`: jelentés, nem blokkol. A heurisztikus (szövegmintás) szabályok FIGYELMEZTETÉS szinten indulnak. HIBA szintre csak akkor kerülnek, ha a CI.0 alapállapot szerint kevés rajtuk a hamis találat.
- **Diff-hatókör.** A HIBA szint csak a PR-ben módosított fájlokra vonatkozik. A teljes repó állapota csak jelentés, mert a régi fájlok ismert eltérései (pl. NAPLO-keveredés) ne blokkoljanak minden PR-t.
- **A meglévő `ellenoriz.py` az alap.** A SEMA §3 1–12. szabálya és a Q1/Q7 már gépi, ezeket nem kell újraírni, csak a CI-ből meghívni.

## Ellenőrzőlista — a dokumentált incidensekből

| # | Ellenőrzés | Incidens / szabály forrása | Szint |
|---|---|---|---|
| E1 | `python eszkozok/ellenoriz.py --study <módosított studyk>` kilépési kódja 0 | SEMA §3 1–12, Q1, Q7 | HIBA |
| E2 | „ellenőrizve”, „🔍”, „🔬 valódi kutatás”, „STEPBible-ellenőrizve” jelölés csak akkor állhat, ha ugyanabban a szakaszban/sorban van `scope=… \| forras=… \| ts=…` proveniencia-sor | 2026.09.10: lefuttatatlan lekérdezés „ellenőrizve” jelöléssel | HIBA |
| E3 | Proveniencia-mező nem üres; ha nem futott lekérdezés, az értéke `manual` (nem „ellenőrizve”) | CLAUDE.md 1. szabály | HIBA (részben E1 fedi) |
| E4 | Ha egy motívumhoz friss teljes keresés tartozik (`adat/auditok.tsv`), léteznie kell a `[könyv-mappa]/naplok/[motívum]_kereszthivatkozas_naplo.md` fájlnak, és benne döntésnek minden jelöltre | Négy keresés napló nélkül | HIBA |
| E5 | Tartalomvesztés-őr: ha a diff `##`/`###` címsort töröl, vagy egy study-/sablonfájlból >30 sort töröl, a commit-üzenetben `TÖRLÉS-SZÁNDÉKOS:` jelölés kell | „Csere a következő ## címig” → önellenőrzés-jegyzet és javaslatlista elveszett | HIBA |
| E6 | Tematikus study: van „0. Forrás-összegyűjtés” szakasz, és a találati tábla a sablon aktuális oszlopszámával egyezik (az oszlopszámot a live `sablonok/4_PaRDeS_tematikus_sablon.md`-ből olvassa, ne legyen beégetve) | Elavult sablon-snapshot használata | HIBA |
| E7 | Minősített találat prózában csoportosítva, táblán kívül: ha a `jeloltek.tsv`-ben `bekerult` döntésű igehely a study táblájában nincs, de a prózában szerepel | Két fájl prózai csoportosítása régi precedens alapján | HIBA |
| E8 | Igehely-formátum: `1 Móz`, `1. Móz`, `ApCsel. ` stb. tiltott; helyes: `1Móz 2:7` | study-rules | HIBA |
| E9 | Angolul hagyott „sense” a study-/lexikonszövegben (kódblokkon és forrásidézeten kívül) | study-rules | HIBA |
| E10 | Szótári fordításban a „spirit” → „lélek”, „spiritual” → „lelki” tiltott (helyes: szellem / szellemi); a „soul” → „lélek” helyes | 2026.09.22 döntés | HIBA |
| E11 | Cremer semmilyen formában nem szerepelhet a szótári szerep-mátrixban és a renderben; NIDNTTE/NIDOTTE sem (a TWOT-szám kivétel) | SZOTAR D17, 2026.09.25 | HIBA |
| E12 | Proveniencia prózában: dátum (`2026.09.`), fájlnév (`.tsv`/`.md`), „audit során”, „visszaírva”, „felismerve”, „l. X pont” a `【NAPLO: …】` blokkon kívül | NAPLO-szétválasztási szabály | FIGYELMEZTETÉS |
| E13 | Héber/görög szó kiejtés nélkül: héber vagy görög írásjel-futam után 40 karakteren belül nincs ` – <átírás>` vagy `(<átírás>)` | Kiejtési szabály | FIGYELMEZTETÉS |
| E14 | Tematikus sablon 1. pont „Jelentés-szöveg” oszlopa angol (angol stopszavak aránya a cellában >40%) | study-rules felülbírálás | FIGYELMEZTETÉS |
| E15 | SzPA-idézet hossza >25 szó | Szerzői jog | FIGYELMEZTETÉS |
| E16 | Ellenőrző-önmódosítás (lásd Alapelvek) | Új | HIBA |

**Nem gépesíthető, az ügynökre marad (E-A):**

- A1: A „memória vs. lekérdezés” besorolás tartalmilag helytálló-e (a 2. kategóriás állítás jelölve van-e).
- A2: A NYITOTT_FELADATOK / átadási dokumentum „nyitott” tételei valóban nyitottak-e a friss repó szerint.
- A3: Tematikus vs. lexikai párhuzam helyes címkézése („tematikus, nem lexikai párhuzam”).
- A4: A Remez nem tartalmaz következtetést; a Sod levezethető a Peshat/Remez/Drash rétegből.
- A5: Nevesített tanító csak a jóváhagyott listáról, pontos forrással; hiány explicit jelölve.
- A6: E12–E15 figyelmeztetéseinek tartalmi megítélése.

## Tételek

**CI.0 — Alapállapot.** Írd meg az E2–E16 ellenőrzéseket az `eszkozok/ellenorzes/` alá (egy szabály = egy függvény, közös futtató: `eszkozok/ellenorzes/futtat.py [--valtozott FÁJL…] [--teljes]`). Futtasd a teljes repóra, és szabályonként írd a `naplok/CI_alapallapot.md` fájlba a találatszámot, plusz szabályonként 3 mintatalálatot. **Itt állj meg.** A felhasználó dönti el, melyik HIBA-szabály marad HIBA.

**CI.1 — Tesztek.** Minden szabályhoz legalább egy pozitív és egy negatív tesztfixture (`eszkozok/ellenorzes/tesztek/`), a korábbi incidensek rekonstruált mintáival.

**CI.2 — GitHub Actions.** `.github/workflows/ellenorzes.yml`: PR-re és a `main` push-ára fut. Meghatározza a PR változott fájljait, lefuttatja az E1-et és a `futtat.py --valtozott …` parancsot, a jelentést job summaryként és PR-kommentként adja ki. Csak a standard library-t és a repó saját szkriptjeit használja, külső szolgáltatást nem hív.

**CI.3 — Branch protection.** Írd le lépésenként a `naplok/CI_beallitas.md` fájlba, hogyan állítsa be a felhasználó a GitHub felületén a `main` védelmét: kötelező `ellenorzes` check, közvetlen push tiltása. Ezt Code ne próbálja beállítani.

**CI.4 — Chat-oldali olcsó lekérdezés.** Írj egy rövid leírást a `GitHub_feltoltesi_workflow.md` fájlba arról, hogy a chat a `api.github.com/repos/basesoft777/Bible-Study/commits/<sha>/check-runs` végpontot és a PR-kommentet olvassa, tarball helyett. A tarball csak akkor kell, ha a CI piros és a jelentés nem elég.

**CI.5 — `fuggetlen-ellenor` ügynök.** `.claude/agents/fuggetlen-ellenor.md`, a meglévő `lexikai-scan.md` mintájára. Beállítások: `tools: Read, Grep, Glob, Bash` (Bash csak `git diff`, `git log`, `python eszkozok/lekerdez.py`, `python eszkozok/ellenorzes/futtat.py` futtatására, utasításként rögzítve), `model: opus`.

- Bemenete csak ez: a brief fájlneve, a base..head commit-tartomány és a CI-jelentés. A munkát végző session összefoglalóját **nem** kapja meg.
- Szerepe hibakeresés: abból indul ki, hogy van hiba, és azt keresi. Nem megerősít.
- Az A1–A6 pontokat, valamint a brief minden „G”/„D” pontjának teljesülését ellenőrzi.
- Minden adatállítást maga futtatott lekérdezéssel igazol, és a parancsot a jelentésbe írja.
- Kimenet: `naplok/ELLENOR_<tétel>.md`, táblázatban (pont · OK/ELTÉRÉS/NEM ELLENŐRIZHETŐ · fájl:sor · parancs/indok). A „nem ellenőrizhető” elfogadott kimenet, ezt nem szabad OK-ra kerekíteni.
- Fájlt a saját jelentésén kívül nem ír.

## Új munkafolyamat (a CI.5 után)

1. Code végrehajtja a tételt, majd push a munkaágra.
2. A CI lefut.
3. A felhasználó új, friss Code-sessionben elindítja a `fuggetlen-ellenor` ügynököt. Nem abban a sessionben, amelyik a munkát végezte.
4. A chat elolvassa a CI-státuszt és a `naplok/ELLENOR_<tétel>.md` jelentést, majd javasol.
5. A merge-ről a felhasználó dönt.

A `method-learnings` kettős megerősítési szabálya így módosul: „független ellenőrzés” = zöld CI + a friss kontextusú ügynök jelentése, a chat pedig mindkettőt olvassa. Tarball csak eltérés esetén kell.

## Döntési napló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | Ellenőrzés GitHub Actionsben + különálló ügynök, a chat csak olvas | Egy chatbeli ellenőrzés ~92 MB tarballt és sok kontextus-tokent visz el; a függetlenség forrása a különálló kontextus és a determinisztikus szkript, nem a chat felülete | Chatbeli tarball-ellenőrzés marad (drága); csak önjelentés (a 09.10-es incidens miatt elfogadhatatlan) |
| D2 | A meglévő `ellenoriz.py` az alap, az új szabályok külön modulba kerülnek | A SEMA 1–12 már gépi; így nincs párhuzamos, eltérő implementáció | Mindent újraírni egy szkriptbe |
| D3 | HIBA csak a diff-fájlokra, a teljes repó csak jelentés | A régi fájlok ismert eltérései ne blokkoljanak minden PR-t | Teljes repó blokkol (azonnal piros minden PR) |
| D4 | Heurisztikus szabályok (E12–E15) FIGYELMEZTETÉS szinten indulnak | Szövegminta alapján hamis találat várható; a CI.0 számai alapján lehet szigorítani | Mind HIBA (vakriasztás-fáradtság) |
| D5 | Ellenőrző-önmódosítás tiltása `[ELLENŐRZŐ]` jelölés nélkül | Különben a munkát végző session a saját vizsgáját írja | Nincs őr |
| D6 | Az ügynök Opus, hibakereső szereppel, a munkát végző session összefoglalója nélkül | Azonos modell + azonos keretezés azonos vakfoltot ad; a szerep és a bemenet-elválasztás csökkenti ezt | Sonnet megerősítő szereppel (olcsóbb, de gyengébb) |
| D7 | CI.0 után kötelező megállás | A HIBA/FIGYELMEZTETÉS besorolás tényadatra épüljön, ne feltételezésre | Egy menetben végigfuttatni |
| D8 | HIBA a módosított fájl ÚJ/MÓDOSÍTOTT SORAIRA vonatkozik (git diff `+` sorok), nem az egész fájlra; a fájl régi találatai csak JELENTÉS. Kivétel: E6 és E7 fájlszintű marad | A CI.0 mérés a teljes fájltartalmon futott, és nagyrészt régi, PR-en kívüli sorokat talált; a diff-hatókör (D3) szellemében a HIBA a ténylegesen írt sorra vonatkozzon | Fájlszintű HIBA minden szabálynál (túl sok hamis blokkolás régi fájlokon) |
| D9 | HIBA marad a CI.0 után: E3, E4, E5, E6, E7, E8, E10, E16 | A CI.0 szerint ezeknél 0 vagy releváns találat volt, alacsony hamis-pozitív kockázattal | Mind FIGYELMEZTETÉS (D4 túltágítása) |
| D10 | E2 HIBA, szűkítve a 🔍, 🔬 és „STEPBible-ellenőrizve” jelölésre; a sima „ellenőrizve” szó, a `【NAPLO: …】` blokk és a checklist-sor (`[x]`/`[ ]`) nem számít | A CI.0 140 találatának nagy része sima „ellenőrizve” szó ártalmatlan szövegkörnyezetben, nem a jelzett incidens mintája | E2 teljes egészében FIGYELMEZTETÉS (túl gyenge védelem) |
| D11 | E9 HIBA, szűkítve: blockquote (`>`), kódblokk és idézőjeles angol forrásidézet kizárva | A CI.0 99 találatának egy része a szabály saját dokumentációja és forrásidézet, nem tényleges study-szöveg | E9 teljes egészében FIGYELMEZTETÉS |
| D12 | E11 HIBA, hatókör: `lexikon/`, `adat/szotar_szerepek.tsv`, `eszkozok/*general*.py`; forrásidézeten (blockquote) belül nem számít. A 8 törzscikk ismert régi Cremer-sora a SZOTAR S2.8 újragenerálásával javul, most nem javítandó | A CI.0 61 találatának nagy része a `CREMER_OCR_BRIEF.md` saját tárgyalása, nem tényleges szerepmátrix/render-sértés; a régi törzscikk-sorok javítása külön brief (SZOTAR S2) feladata | E11 teljes repóra (túl sok hamis találat a brief-dokumentumokban) |
| D13 | E12, E13 FIGYELMEZTETÉS marad, hatókör szűkítve: `tematikus_lezart/`, `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `motivumlog/`, `lexikon/`. E13-nál a zárójelen belül vessző után álló átírás és a STEP-pontozott átírás (pl. `te.hom`) is elfogadott | A CI.0 4087/3837 találata jórészt a hatókörön kívüli brief-/tervdokumentumokból jött; a szűkített hatókör a study-rétegre koncentrál | E12/E13 HIBA szintre emelése (a brief D4-e szerint még korai) |
| D14 | `naplok/CI_*.md` és `naplok/ELLENOR_*.md` minden szabály alól kizárva | Ezek maguk az ellenőrzés kimenetei/naplói, tartalmuk (pl. mintasorok, dátumok) ne generáljon önhivatkozó találatot | Nincs kizárás (az ellenőrző saját jelentése magát jelentené) |
| D15 | E14, E15: a CI.1 pozitív fixture-je bizonyítsa, hogy a szabály egyáltalán talál | A CI.0-ban mindkettő 0 találatot adott a teljes repón — teszt nélkül nem tudni, hogy a minta valaha is illeszkedik-e | Változatlanul hagyni bizonyíték nélkül |
| D16 | E8: a backtickes inline kód (`` `…` ``) és a kódblokk kizárva | A saját PR-diffre futtatva a `F02_CI_ELLENORZES_BRIEF.md` szabályleíró sora (a tiltott mintákat backtickben idézve) hamis találatot adott — a szabály saját dokumentációja, nem study-szöveg | Nincs kizárás (minden PR, amely a briefet módosítja, elbukna) |
| D17 | E10 hatóköre a szótári fordítás tényleges helyére szűkítve: `adat/` (pl. `forditas_ubs.tsv`, `lexikon_hivatkozasok.tsv`, a jövőbeli SZOTAR S1 `terminologia.tsv`/`forditasok.tsv`) és `lexikon/` (a render); a gyökér brief-/tervfájlok (pl. `F05_SZOTAR_BRIEF.md`) nem. Inline kód és idézőjeles példa kizárva | Ugyanaz a fajta önhivatkozó hamis találat, mint D11/D12-nél: a `F05_SZOTAR_BRIEF.md` saját magát dokumentálja ("spirit = szellem, ... soul = lélek"), ez nem tényleges fordítási sértés | E10 teljes repóra (túl sok hamis találat a brief-dokumentumokban) |
| D18 | Rögzítve: E4, E5, E16 a D8 fájlszintű kivételéhez tartozik, E6/E7 mellett | E4 a `jeloltek.tsv`/`auditok.tsv` motívum-szintű állapotát nézi, nem egy konkrét sorhoz köthető; E5 maga diff-alapú (a törölt sorokat vizsgálja, nem a hozzáadottakat); E16 fájl-létezés (érinti-e a PR az ellenőrzőt), nem egy konkrét tartalmi sor — egyiknél sincs értelmezhető "hozzáadott sor", amire a D8 diff-szűrését alkalmazni lehetne | A D8-at kivétel nélkül minden szabályra alkalmazni (ez E4/E5/E16-nál értelmezhetetlen lenne) |
| D17a | E10-ből visszavonva az idézőjel- és a blockquote-kizárás; csak az inline kód (`` `…` ``) marad kizárva | A D17 hatókör-szűkítése (`adat/`, `lexikon/`) már megszüntette az önhivatkozó hamis találatot; az idézőjel-/blockquote-kizárás viszont a hatókörön belül épp a célpontot rejtette volna el — a lexikon a magyar glosszát idézőjelben adja (`„lélek"`), a Thayer-fordítás (#7) pedig blockquote-ban renderel. Angol forrásidézetben nincs "lélek/lelki", tehát a blockquote önmagában nem ad hamis találatot | D17 eredeti (idézőjel+blockquote is kizárva) — ez a lexikon/Thayer valódi sértéseit is elrejtette volna |
