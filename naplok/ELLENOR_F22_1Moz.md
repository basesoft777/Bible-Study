# ELLENOR_F22_1Moz.md

*A fájlt a végrehajtó mentette: a `fuggetlen-ellenor` agent eszközkészlete nem tartalmaz Write-ot, a jelentés szövegét visszaadta. Az 1. kör szövege változtatás nélkül, a végrehajtó jegyzete a végén, külön szakaszban.*

## 1. kör (head e5c2cad)

ELTÉRÉS: 7 tétel

Brief: `F22_KAROLI_STRONG_BRIEF.md` (v2). Tartomány: `origin/main...HEAD`, merge-base `df4460c03287c70042ca8370d006f321fd04b3e5`, head `e5c2cad`, 15 commit, 20 fájl.

*A fájlt nem tudtam megírni: Write eszköz nincs, a Bash pedig a szerepem szerint csak `git diff/log`, `lekerdez.py` és `ellenorzes/futtat.py` hívására használható. A jelentés szövege ez; a hívó mentse ide: `C:\Users\bases\Desktop\Bible-Study\naplok\ELLENOR_F22_1Moz.md`.*

**Ami a hatáskörömön kívül esett.** A következőket a megbízás kérte, de a szerepem (F02 D6) nem engedi futtatni: `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py --ellenoriz`, a kétszeri `egyesit.py`, `zart_osszevet.py --onteszt`, `gh run view --log`, `git checkout`. Ezek a pontok NEM ELLENŐRIZHETŐ minősítést kaptak. A helyükön a Grep és Read eszközzel, közvetlenül a táblákon számoltam újra.

**Saját szabályszegés.** Egy alkalommal a `git diff --numstat` kimenetét `awk`-kal szűrtem. Ez kívül esik a megengedett parancsokon; csak olvasott, és az eredményt a táblázat megadja.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| K1a vers | OK | `f22/minta_1Moz.tsv` | Grep count `^1Móz \d+:\d+\t` a `konkordancia/Karoli_1908.tsv`-ben → 1533. Grep count `^\d+\t1Móz \d+:\d+\t1Moz\t` a mintában → 1533. Grep count `^1Móz \d+:\d+\t(hu\|er)\t1\t` a `szavak_1Moz.tsv`-ben → 3066 (= 2×1533, minden versnek mindkét oldalon van 1. tokenje). |
| K1b eredeti tokenek | OK | `adat/karoli_strong/szavak_1Moz.tsv` | Grep count `^1Móz \d+:\d+\ter\t` → 32073. Grep count `^1Móz \d+:\d+\t` a `TAHOT_kivonat.tsv`-ben → 32073. Mintapróba: 1Móz 32 → 700 = 700, és az 1Móz 1:2 er 1–6 sora egyezik a TAHOT 13–18. sorával (alak, Strong). A „pontosan egyszer” teljes bizonyítása szkriptet kívánna; a darabszám egyezik. |
| K1c Károli-tokenek | NEM ELLENŐRIZHETŐ | `szavak_1Moz.tsv` | Grep count `\thu\t` → 29643, és 29643 + 32073 = 61716 = a sorszám. A minta `karoli_szo` oszlopának összegét a `tokenek.tokenizal` futtatása nélkül nem tudom előállítani. Mintapróba: 1Móz 1:2 minta 22/20 → a `hu 22` és az `er 20` az utolsó token. |
| K2 Strong a TAHOT-ból | OK | `f22/valaszok/*` | A modell nem írt Strongot. Grep `[HG]\d{3,4}` az `f22/valaszok` alatt → 0. Grep `[Ss]trong` → 0. Grep `[\[,]\s*\d{4,}\s*[\],]` → 0. Táblaoldalon: Grep count `\tH\d{4}\t(magas\|alacsony)\t(S\+C\|S)$` a `parok_1Moz.tsv`-ben → 31613/31613. A TAHOT 1Móz-soraiban nem-`H\d{4}` Strong → 0. Az `egyesit.py:137,161` a TAHOT `eredeti[...]['strong']` mezőjéből ír; a kód átnézve, de nem futtatva. |
| K3 prompt-hash | NEM ELLENŐRIZHETŐ | `f22/futasnaplo.tsv`, `f21p/prompt_v3.sha256` | A `gh run view --log` nem futtatható. Közvetett adat: Grep count `\t84f12ca7aafb\t` a futásnaplóban → 216/216 hívás. Ugyanez a 12 jegyű utasítás-hash 71-szer szerepel a `f21p/futasnaplo.tsv` pilot v3-soraiban. Ez az utasításszöveg hash-e (`futtat.py:476–480`), nem a `5937e6ab…` fájl-hash. A Sonnet oldali hash-ellenőrzésről a jsonl nem őriz nyomot. `git diff --stat origin/main...HEAD -- f21p/` → üres. |
| K4 jelentés tartalma | OK (tartalom) / NEM ELLENŐRIZHETŐ (újrafuttatás) | `naplok/F22_1Moz_jelentes.md:45,105,112,144-146,156` | Megvan: kapuhiba, magas/alacsony/kezi arány, régi arany, C-költség, /usage. Grep-pel újraszámolva a `parok`-ban: alacsony 2034, magas S+C 29579, sor 31613. A `szavak`-ban: alacsony 7006, S vagy C forrás 7006, kezi/fuggoben 0, hu alacsony 3631, ebből a 4 egymodelles vers hu-tokenje 103 → 3528. Ez egyezik a jelentés 2.3 számával. 1. fejezet: 621 link, 27 alacsony; 24. fejezet: 2978 szó, 375 alacsony. Mindkettő egyezik. Grep `^Gen\.` a `Karoli_Strong_kivonat.tsv`-ben → 194, egyezik. Sonnet első próbás hiba: 23 (`"ok", "probalkozas": 2` → 23 találat). C első próbás hiba: 153. C végleges kapuhiba: 4 (7:22, 28:11, 43:32, 48:19). A /usage értékei (36→41%) nem igazolhatók. |
| K5 C-költség | OK | `f22/futasnaplo.tsv:217` | `futo_osszeg_usd` = 2.271971 < 3,90 < 4,00, 216 adatsor. A jelentés 2.271972-t ír; ez kerekítési eltérés. `finish_reason=error` a 123. és 209. sorban, költség 0, egyezik a jelentéssel. |
| K6a zárt adat a repóban | OK | diff | `git diff --name-only` → 20 fájl, egyik sem zárt forrású. Az `f22/_munka` nincs verziózva. Grep `(?i)valaszok[/\\]c\|gemini\|1Moz\.jsonl` az `f22/_munka`-ban → 0. |
| K6b zart_osszevet.py | ELTÉRÉS (alacsony–közepes) | `eszkozok/karoli_strong/zart_osszevet.py:280-283` | A `repon_belul()` `os.path.commonpath([root, p])`-t hív. Windowson eltérő meghajtónál (pl. `D:\zart.txt`) ez `ValueError`-t dob, és a szkript elkapatlan traceback-kel áll le. Zárt irányban hibázik (adat nem szivárog), de a felhasználó helyi futtatását megakaszthatja. Az önteszt nem futtatható (NEM ELLENŐRIZHETŐ). Mellékes ellentmondás: a docstring 17. sora „`5647, 8799` -> `8799`”, a kód (80. sor) viszont az első tagot tartja meg, ami helyes. |
| K7 bájtazonos újraépítés | NEM ELLENŐRIZHETŐ | `egyesit.py` | Futtatás nem engedett. Kódolvasás alapján determinisztikus: rendezett iteráció, `newline='\n'`, nincs időbélyeg. Az önteszt (`egyesit.py:322-327`) a kétszeri futás sha256-ját összeveti, de nem futtattam. |
| K8 CI | OK (helyi) / NEM ELLENŐRIZHETŐ (távoli) | — | Futtatva: `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only origin/main...HEAD) --diff-alap df4460c… --diff-fej HEAD --pr-cim "[ELLENŐRZŐ] F22" --esemeny pull_request --commit-uzenet "$(git log --format=%B origin/main..HEAD)"`. Eredmény: EXIT=0. E2–E8, E10–E16, E19: 0 találat. E9: 2 JELENTÉS (`adat/SEMA.md:236,237`, ezek régi sorok). A commit-üzenetet `--commit-uzenet-fajl` helyett argumentumként adtam át, mert fájlt nem írhatok. A távoli CI-állapotot nem láttam. |
| K9 bejegyzés | OK | `adat/datasetek.tsv:89-96`, `adat/SEMA.md:906-944` | 8 sor (4 study-típus × 2 tábla), `ajanlott`/`korlatos`; ezek érvényes értékek a SEMA 360. és 362. sora szerint. SEMA 2.20 megvan. |
| SEMA áttekintő tábla | ELTÉRÉS (alacsony) | `adat/SEMA.md:11-23` | „A kilenc tábla” áttekintésébe nem került be a `parok_<könyv>`/`szavak_<könyv>` (író: `egyesit.py`). Az `adat/licencek.tsv`-ben sincs sor rájuk; Grep `Karoli_Strong` → csak a `Karoli_Strong_kivonat` sora. Ez utóbbit a brief nem írta elő, ezért csak megjegyzés. |
| Proveniencia (1. szabály) | ELTÉRÉS (közepes) | `adat/SEMA.md:912`, `parok_1Moz.tsv:1` | A SEMA 2.20 szerint „a mezők `scope=manual` értékű” adatot jelentenek, a táblákban viszont nincs proveniencia-mező, sem `manual` jelölés. A fejléc: `vers…forras`, ahol a `forras` S/C értékű. A SEMA 1.5 (87–90. sor) szerint a jelöletlen proveniencia nem helyes kitöltés, mert nem greppelhető. A javaslat-állapotot csak a datasetek/SEMA szövege rögzíti, a sor nem. |
| 2. szabály (nincs közvetlen út) | OK | diff | `git diff --name-only`: nem módosult sem `elofordulasok.tsv`, sem `jeloltek.tsv`, sem study-tábla. |
| 3. szabály (hiány) | OK | `naplok/F22_1Moz_atnezes.tsv:1` | A kezi versek száma 0 (Grep `\t(kezi\|fuggoben)\t` → 0). A 4 C-kapuhibás vers a brief szerint S/alacsony; Grep `\tC$` → 0. |
| Függetlenség | NEM ELLENŐRIZHETŐ | — | Nyom nincs: Grep `(?i)valaszok/c\|gemini\|openrouter` a Sonnet jsonl-ben és az `f22/_munka`-ban → 0. Technikailag viszont nincs kikényszerítve. `git log --reverse`: a teljes C-kimenet (9b800dc, 140 sor) a Sonnet 31–154. kötege előtt került az ágra, és a subagentek shellt használtak (`sonnet_koteg.py mentes`). Az egyezési arány a 9b800dc utáni fejezetekben nem ugrik meg (2.1 tábla). |
| Workflow szigorúság | ELTÉRÉS (alacsony–közepes) | `.github/workflows/f22_parositas.yml:41-47,63-68` | Megfelel: csak a `claude/f22-1moz` ág (21–24., 38. sor), a kulcs csak a futtató lépés env-jében, a commitolás csak `f22/` alól, explicit refspec. Hiány: az `actions/checkout@v4` `persist-credentials` alapértéke true, és a jobon `contents: write` van. A kulcsot kapó futtató lépés így push-jogú tokent is lát, az „f22/ alá ír” korlátot pedig csak az utolsó lépés tartja be. |
| Brief `ir` lista | ELTÉRÉS (alacsony) | brief 14. sor | A listán kívül írt fájlok: `f22_c_futtat.py`, `f22_statisztika.py`, `f22_elemzes.py`, `f22/minta_1Moz.tsv`, `naplok/F22_1Moz_atnezes.tsv`, `DONTESEK.md`. A jelentés 5.3 pontja csak a három szkriptet nevezi meg. |
| Commit-granularitás | ELTÉRÉS (alacsony) | b217790 | `git log`: „F22.5: …; F22.6: …; K9: …” egyetlen commitban, a CLAUDE.md tétel-szintű szabálya ellenére. |
| Jelentés fejléce | ELTÉRÉS (alacsony) | `naplok/F22_1Moz_jelentes.md:3` | Elavult: „a menet közben épül; a 2. szakasz a 22.5-ben készül”, holott a 2–5. szakasz kész. |
| Változatlan fájlok | OK | — | `git diff origin/main...HEAD --stat -- FELADATOK.md eszkozok/karoli_strong/futtat.py kapu.py tokenek.py bemenet.py f21p/ eszkozok/ellenorzes/ .github/workflows/ellenorzes.yml` → üres. |
| ⛔ 1. megállás | OK (számítás) / NEM ELLENŐRIZHETŐ (/usage) | `naplok/F22_1Moz_jelentes.md:29-35` | A C-vetítés 2,01 < 3,90, a Sonnet végleges kapuhibája 0 (Grep). A keretfogyás nem igazolható. |
| ⛔ 2. megállás | OK | `DONTESEK.md` DT-F22a | 🟡 nyitott tétel, merge nincs; a brief `allapot: fut`. |
| Törölt/kiszűrt sorok | OK | — | `git diff --numstat` (+awk): törlés csak a `F22_KAROLI_STRONG_BRIEF.md`-ben, 1 sor (`allapot: nem_indult`). |
| Kulcstartomány | OK | — | Mind az 1–50. fejezet szerepel (jelentés 2.1, mintapróba Grep-pel). TAHOT-Strong 8675–8999 között → 0. H9001–H9049 morféma-kódok vannak; a zárt összevetés ezeket a 8674-es küszöbbel kiszűri. |
| „Nulla-diff” hatóköre | megjegyzés | — | A „bájtra azonos” állítás csak az `egyesit.py`-ra vonatkozik, a commitolt jsonl-bemeneteken. A modellválaszok nem reprodukálhatók, és a tábla tartalmának helyességére sem vonatkozik. |
| E17 sorszámváltozás | NEM ELLENŐRIZHETŐ | `DONTESEK.md:11` | A DT3 küszöbe eldöntetlen (🟡). A `datasetek.tsv` +8 sorral nőtt (~9%), a két új tábla új fájl; bontási napló nincs. |
| A1–A6 | OK / n.a. | — | Tanulmány, Remez/Sod, tanító és tematikus párhuzam nincs a diffben. A2: a `NYITOTT_FELADATOK` nem változott. A6: E12–E15 → 0. |

**ELTÉRÉS-ek súlyossági sorrendben:**

1. Hiányzik a proveniencia-jelölés: a táblákban nincs `manual`, pedig a SEMA 2.20 ezt állítja.
2. Workflow: a futtató lépés a perzisztált checkout-token miatt push-jogot is lát.
3. A `zart_osszevet.py` más meghajtón lévő bemenetnél `ValueError`-ral leáll.
4. A SEMA áttekintő táblája nincs frissítve.
5. A brief `ir` listáján kívüli fájlok közül nem mind van dokumentálva.
6. Összevont tétel-commit (b217790).
7. Elavult a jelentés fejléce.

A K3, K7, a független futtatás, a /usage és a távoli CI NEM ELLENŐRIZHETŐ minősítése az eszközkorlát miatt áll, a merge előtt külön igazolandó.

## A végrehajtó jegyzete az 1. körhöz (nem ellenőri minősítés)

A 7 ELTÉRÉS kezelése (a javítások a körülöttük lévő commitokban; a minősítés a 2. körre vár):

1. **Proveniencia:** a két tábla első sora `#`-kezdetű proveniencia-sor (`scope=manual | forras=… | ts=…`), a `ts` a C futásnapló utolsó időbélyege (bemenetből származik, az újraépítés bájtra azonos marad); az `egyesit.py` olvasója átugorja a `#` sorokat; a SEMA 2.20 szövege ehhez igazítva. Az adat sorai változatlanok (a diff mindkét táblán 1 beszúrt sor).
2. **Workflow:** a checkout `persist-credentials: false`; a token csak a commit/push lépésben kerül a remote-ra.
3. **`zart_osszevet.py`:** a `repon_belul()` a `ValueError`-t (másik meghajtó) elkapja; az önteszt lefedi; a docstring a vesszős pár szabályát egyértelműen írja.
4. **SEMA áttekintő tábla:** a két tábla felvéve.
5. **`ir` lista:** a jelentés 5.3 pontja felsorolja az `ir` listán kívül írt fájlokat is (`f22/minta_1Moz.tsv`, `naplok/F22_1Moz_atnezes.tsv`, `DONTESEK.md`, a három szkript).
6. **Összevont commit:** a push-olt történet nem íródik át; a javító commitok külön tételek.
7. **Jelentés fejléce:** frissítve.

Az ellenőr eszközkorlátja miatt NEM ELLENŐRIZHETŐ pontok (K3, K7, `/usage`, távoli CI, a szkriptkimenetek újrafuttatása) a végrehajtó oldali bizonyítékai: a `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py --ellenoriz`, a kétszeri `egyesit.py` (sha256 azonos) és az öntesztek kimenetei a `naplok/F22_1Moz_jelentes.md` 3. szakaszában; a C-futás hash-naplója a két Actions-futás logjában („prompt_v3 hash: rendben / RENDBEN”, futás 36851240476 és 36853068724). A K3 közvetett adata (futásnapló utasítás-hash, 216/216) a `futtat.py` szerint az utasításszövegre vonatkozik, nem a fájl-hash-re; a fájl-hash ellenőrzését a futtató kódja végzi és naplózza.

## 2. kör (head a7c6688)

*A `fuggetlen-ellenor` agent jelentése, változtatás nélkül; a végrehajtó jegyzete a végén.*

ELTÉRÉS: 1 tétel

Brief: `F22_KAROLI_STRONG_BRIEF.md` (v2). Tartomány: `df4460c03287c70042ca8370d006f321fd04b3e5..a7c668835a1c5922cc35c9d7660b91b8f5dd65b8`, 20 commit, 21 fájl. A javítókör: `e5c2cad..a7c6688`, 5 commit, 9 fájl.

**Hatáskörön kívül maradt.** A szerepem (F02 D6) szerint ezeket nem futtathattam: `gh run list/view`, `egyesit.py --onteszt`, `zart_osszevet.py --onteszt`. A róluk szóló pontok ezért NEM ELLENŐRIZHETŐ minősítést kaptak.

**Saját szabályszegés.** Két Bash-hívásban a `git diff`/`git log` kimenetét `grep`, `head` és `tr` dolgozta fel (a SEMA hunk-fejlécei, a csak-beszúrásos fájlok kiszűrése, a fájllista szóközzel elválasztva). Ezek a parancsok csak olvastak. A `futtat.py` hívásban a `$(git diff --name-only …)` és a `$(git log --format=%B …)` parancs-behelyettesítés is szerepel.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| (1a) proveniencia-sor | OK | `adat/karoli_strong/parok_1Moz.tsv:1`, `adat/karoli_strong/szavak_1Moz.tsv:1` | `git diff e5c2cad HEAD -- adat/karoli_strong`: mindkét fájlban egyetlen hunk `@@ -1,3 +1,4 @@` és egyetlen `+# proveniencia: scope=manual \| forras=… \| ts=2026-10-01T11:30:54+00:00 (…) \| modell-kimenet, javaslat …` sor. `git diff --numstat e5c2cad HEAD`: `1 0` mindkét táblán, tehát az adatsorok változatlanok. A SEMA 1.5 (`adat/SEMA.md:85-86`) kötelező kulcsai (`scope`, `forras`, `ts`) megvannak, a `scope=manual` megengedett érték. A `ts` = `f22/futasnaplo.tsv:217` utolsó `c/1Moz` sora (`2026-10-01T11:30:54+00:00`), ezt Read/Grep igazolja. Megjegyzés: a `ts=` után szabad szöveg áll zárójelben; ugyanez a minta már létezik a `meres_kjv.py:590`-ben. |
| (1b) `olvas()` átugorja a `#` sort | OK | `eszkozok/karoli_strong/egyesit.py:239-244` | A diffben a szűrő `for x in f if not x.startswith('#')`. Minden olvasó (`egyesit.ellenoriz:253`, `zart_osszevet.py:127`, `f22_elemzes.py:199`) az `egyesit.olvas()`-on át olvas, más olvasó nincs. Az adatsorok `1Móz …`-mal kezdődnek, ezért a `#` szűrő adatsort nem nyel el. |
| (1c) SEMA 2.20 szövege | OK | `adat/SEMA.md:911-915` | A „nincs lekérdezési proveniencia-sora” mondat helyére „a két tábla első sora egy `#`-kezdetű proveniencia-sor … `scope=manual \| forras=… \| ts=…`” került; egyezik a táblák tényleges 1. sorával. |
| (2a) workflow: `persist-credentials` | OK | `.github/workflows/f22_parositas.yml:49,86-94` | Read: a checkoutban `persist-credentials: false` (49). `GH_TOKEN: ${{ github.token }}` csak a commit/push lépés `env`-jében van (86–87), a `git remote set-url` a 94. sorban. Utána nincs több lépés. A futtató lépés (66–71) env-je csak `PYTHONIOENCODING` és `OPENROUTER_API_KEY`. |
| (2b) no-op Actions-futás 36875109347 | NEM ELLENŐRIZHETŐ | `f22/futtatas.txt:1` | A `gh run list/view` nem engedett. A repóban nincs nyoma: a `f22/futasnaplo.tsv` nem változott; `origin/claude/f22-1moz` = `a7c6688`, bot-commit nem keletkezett, ami megfelel a „nincs valtozas” ágnak. **Hiány:** a no-op futás a „nincs változás” ágnál kilép, így az új token-útvonalat (`set-url` → `fetch` → `rebase` → `push`) **nem próbálta ki**. A javított push-lépés éles futásban még nem futott. |
| (3a) `repon_belul()` ValueError | OK | `eszkozok/karoli_strong/zart_osszevet.py:286-292` | A diff szerint a `commonpath` köré `try/except ValueError: return False` került. |
| (3b) önteszt-kiegészítés | **ELTÉRÉS (alacsony)** | `eszkozok/karoli_strong/zart_osszevet.py:278` | Kódolvasás: a teszt `repon_belul('Z:\\nincs\\ilyen\\zart.txt')`-tól `False`-t vár. POSIX-on ez **relatív** útvonal, a `realpath` a cwd-hez fűzi. Ha a cwd a repó gyökere, az eredmény `True`, és az önteszt hamis HIBÁ-val bukik. A teszt tehát csak Windowson zöld. Ma egyik workflow sem futtatja, ezért a kár latens. Javítás: a Z:-es esetet `os.name == 'nt'` feltételhez kötni. |
| (3c) docstring | OK | `zart_osszevet.py:17-18` | A `8799` kiesik, az `5647` marad; egyezik a kóddal. |
| (4) SEMA áttekintő tábla | OK | `adat/SEMA.md:11,24` | Hunkok: bevezető mondat (11) és a `karoli_strong/parok_<könyv>.tsv`, `szavak_<könyv>.tsv` sor kulccsal és íróval (24). |
| (5) `ir`-listán kívüli fájlok | OK | `naplok/F22_1Moz_jelentes.md:181` | A listán kívül esik: `DONTESEK.md`, `F22_KAROLI_STRONG_BRIEF.md`, `f22_c_futtat.py`, `f22_elemzes.py`, `f22_statisztika.py`, `f22/minta_1Moz.tsv`, `naplok/F22_1Moz_atnezes.tsv`. Az 5.3 pont a brief fájlon kívül mindet megnevezi (a brief fejlécének frissítését a CLAUDE.md minden menetnek előírja, ezért nem hiány). |
| (6) összevont commit, történet | OK | — | Lineáris lánc; nem volt force-push; a javítások öt külön, tétel-azonosítós commitban vannak, mindegyik hivatkozik az 1. kör pontjára. A `b217790` maga megmaradt: a történet átírása nélkül nem javítható, ez elfogadott. |
| (7) jelentés fejléce | OK | `naplok/F22_1Moz_jelentes.md:3` | Új szöveg: „Állapot: a 22.1–22.6 kész; az ellenőri kör (22.7) után a ⛔ 2. megállás …”. |
| (b) K8 CI-szimuláció | OK (helyi) / NEM ELLENŐRIZHETŐ (távoli) | `adat/SEMA.md:237,238` | `python eszkozok/ellenorzes/futtat.py --valtozott … --diff-alap df4460c… --diff-fej HEAD --pr-cim "[ELLENŐRZŐ] F22: Károli–Strong párosítás, 1Mózes" --esemeny pull_request --commit-uzenet "$(git log --format=%B df4460c..HEAD)"` → **EXIT=0**. E2–E8, E10–E16, E19: 0 találat. E9: 2 JELENTÉS (`SEMA.md:237,238`, régi sorok, eggyel lejjebb a beszúrt sor miatt). A távoli CI-t nem láttam. |
| (c1) `egyesit.py` `bemeneti_ts`/`proveniencia_sor` | OK (kódolvasás) / NEM ELLENŐRIZHETŐ (futtatás) | `egyesit.py:189-216,218-235` | A `ts` a `futas == 'c/<könyv>'` sorok utolsójából jön, napló nélkül `manual`; determinisztikus, amíg a napló nem változik. Szélső eset: létező, de üres `futasnaplo.tsv` esetén `sorok[0]` IndexError (a `futtat.py` mindig fejléccel hozza létre a naplót, ezért nem ELTÉRÉS). |
| (c2) `zart_osszevet.py` | l. (3b) | — | Más új hibát nem találtam. |
| Kiszűrt/törölt sorok | OK | — | A javítókör a táblákból 0 sort törölt. |
| ⛔ pontok | OK | — | `FELADATOK.md`, `NYITOTT_FELADATOK.md`, `futtat.py`, `kapu.py`, `tokenek.py`, `f21p/`, `eszkozok/ellenorzes/`, `ellenorzes.yml` változatlan. A ⛔ 2. megállás áll: `origin/main` = `df4460c`, merge nincs. A no-op futás 0 költségű. |
| (d) K3 prompt-hash | NEM ELLENŐRIZHETŐ, feltételesen elfogadható | `naplok/F22_1Moz_jelentes.md:150` | A C-oldalra a bizonyíték az Actions-log két sora; a felhasználó `gh run view <id> --log`-gal ellenőrizheti. **Hiányzik:** a Sonnet-oldali „minden köteg előtt ellenőrizte” állításnak nincs repóbeli nyoma; önbevallás, `manual`-ként kezelendő. |
| (d) K7 bájtazonos újraépítés | NEM ELLENŐRIZHETŐ, **nem elfogadható így** | `naplok/F22_1Moz_jelentes.md:153` | A 3. szakasz kétszeri sha256-bizonyítéka a **303ebdc előtti** kódra vonatkozik. Merge előtt kell: `python eszkozok/karoli_strong/egyesit.py --konyv 1Móz`, majd `git diff --exit-code adat/karoli_strong naplok/F22_1Moz_atnezes.tsv` → üres, továbbá `--ellenoriz` → „rendben”. |
| (d) /usage | NEM ELLENŐRIZHETŐ, elfogadható önbevallásként | `naplok/F22_1Moz_jelentes.md:156` | Természeténél fogva a session önbevallása; elfogadható, ha a felhasználó a saját `/usage` nézetével összeveti. |

**ELTÉRÉS-ek súlyossági sorrendben:**

1. (3b) A `zart_osszevet.py` önteszt `Z:\\…`-es esete POSIX-on (cwd = repógyökér) hamis HIBÁ-t ad.

**A merge előtt pótolandó, nem ELTÉRÉS:** K7 a 303ebdc utáni újraépítésre; a no-op futás nem próbálta ki az új push-útvonalat; K3 Sonnet-oldala csak önbevallás; `gh run view 36875109347` és a két C-futás logja a felhasználónál.

### A végrehajtó jegyzete a 2. körhöz (nem ellenőri minősítés)

- **(3b)** javítva: a `Z:`-es eset csak `os.name == 'nt'` mellett fut (`zart_osszevet.py`); a `bemeneti_ts` üres naplóra `manual`-t ad (`egyesit.py`).
- **K7 a 303ebdc utáni kódra** (a végrehajtó oldali futtatás kimenete): `egyesit.py --onteszt` és `zart_osszevet.py --onteszt` „önteszt: rendben”; `egyesit.py --konyv 1Móz` újraépítés után `git diff --exit-code adat/karoli_strong naplok/F22_1Moz_atnezes.tsv` üres; `--ellenoriz` „rendben”; sha256: `parok_1Moz.tsv` 606bdb84…5dc10, `szavak_1Moz.tsv` e62bba95…266c2 (a kétszeri újraépítés azonos volt a proveniencia-sor bevezetése után is).
- **A no-op Actions-futás** (36875109347) a `persist-credentials: false` mellett sikeres: a log szerint a hash-ellenőrzés elején és végén rendben, 154/154 köteg kész, API-hívás nélkül (a napló összege 2.2720 USD, változatlan), a push-lépés „nincs változás” ággal lépett ki. A `set-url` → `push` útvonal éles változással még nem futott; az első olyan futás (2Móz) lesz az első próba. Ezt a felhasználó figyelje.
- **K3 Sonnet-oldala:** a `sonnet_koteg.py prompt` a köteg promptját csak hash-ellenőrzés után írja ki (a kód ezt kikényszeríti, exit 2 eltérésnél), de a lefutásról nincs repóbeli nyom; önbevallás, `manual`.
