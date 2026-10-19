---
feladat: 112
cim: CI-szabály: ékezet nélküli magyar szavak a PR commit-üzeneteiben (E30)
kod: COMMIT_EKEZET
tipus: feladat
fazis: folyamat
munka: folyamat
modell: sonnet
allapot: lezarva
lezarva_osszegzes: E30 FIGYELMEZTETÉS szinten bekötve (DT-F112a, szűk kizárólista, mért 84%), 154 teszt zöld, ELLENOR_F112 ELTÉRÉS 7 mechanikus tétel javítva; zárójelentés naplok/COMMIT_EKEZET_zaras.md
ag: claude/f112-commit-ekezet
ad: E30 CI-szabály, amely a PR `base..head` commit-üzeneteiben figyelmeztet az ékezet nélkül írt magyar szavakra, mért hamis-pozitív aránnyal
kovetkezo: az E30 20 PR utáni újraértékelése (N-F112a: jelölési arány, javítások száma, új 50 elemes minta; HIBA-szint és kizárólista-bővítés külön döntés)
olvas: [eszkozok/ellenorzes/, .github/workflows/ellenorzes.yml, BRIEF_SABLON.md, adat/SEMA.md, GitHub_feltoltesi_workflow.md]
ir: [eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/futtat.py, eszkozok/ellenorzes/e30_ascii_alakok.tsv, eszkozok/ellenorzes/tesztek/, naplok/COMMIT_EKEZET_meres.md, .github/workflows/ellenorzes.yml]
fugg: []
---
# F112_COMMIT_EKEZET_BRIEF.md — CI-szabály: ékezet nélküli magyar szavak a commit-üzenetekben (E30)

*FELADATOK #112 · Modell: sonnet · v1 · 2026.10.17*

## 1. Cél

A `CLAUDE.md` „Git” szakasza előírja, hogy a commit-üzenet UTF-8 fájlból menjen, ékezetekkel. Ok: az ékezetlen üzenet kiüti a `git log --grep` tartalmi kereshetőségét (`--grep="betöltés"` nem találja a „betoltes”-t; `GitHub_feltoltesi_workflow.md`). Ezt ma semmi nem ellenőrzi. A cél egy CI-szabály, amely a PR saját commitjaiban jelzi az ékezet nélkül írt magyar szót.

**Kiinduló mérés** (`forras=manual`, scratch-szkript, nem lekérdezés; `scope=origin/main --no-merges`, 3 171 commit, ebből 259 gépi (`szamkiosztas:`, `FELADATOK.md frissítés (gép)`) kihagyva | `ts=2026-10-17`): a naiv módszer (az üzenetekben ékezettel is előforduló szó ékezetlen alakja) **1 285** üzenetet jelölne. A leggyakoribb találatok többsége **nem hiba**:

- fejléc- és sémamezők, értékkészletek, amelyek szándékosan ASCII-k: `allapot`, `kovetkezo`, `fazis`, `fugg`, `lezarva`, `megallt`, `tipus`, `hianyzik`, `kulcs_eltolodott`;
- kétértelmű párok, ahol az ékezetlen alak is helyes magyar szó: `meg`/`még`, `mert`/`mért`, `kor`/`kör`, `sem`, `fel`/`fél`, `arany`/`arány`;
- igehely-rövidítés: `Kor` (1Kor), `ben` (toldalék-töredék).

Valódi hibának látszik például: `ket`, `konyv`, `javitas`, `fuggetlen`, `ellenor`, `forras`, `naplo`, `potolt`, `osszesites`. **A feladat lényege tehát a pontosság**, nem a felismerés.

## 2. Hatókör

**Benne van:**
- E30 szabály a `szabalyok.py`-ban; a `futtat.py` a meglévő `commit_uzenet` bemenettel hívja (a workflow ma is `git log --format=%B base..head`-et ad át; új workflow-lépés nem kell);
- kizárási lista az `e30_ascii_alakok.tsv`-ben (alak, ok: `mezonev` · `ertekkeszlet` · `ketertelmu` · `rovidites`), a forrása naplózva (a `BRIEF_SABLON.md` mezői, az `adat/SEMA.md` oszlopnevei és zárt értékkészletei);
- kihagyott részek: kódrész (`` `…` ``), fájlút és fájlnév, azonosító (`DT-F09a`, `F111`, `ISTENTISZT-001`), `Co-Authored-By:` sor, gépi commitok, merge-commitok;
- tesztek a `tesztek/` alatt (legalább: mezőnév nem jelöl, kétértelmű pár nem jelöl, `ket`/`javitas` jelöl, kódrészben álló szó nem jelöl);
- mérési napló: `naplok/COMMIT_EKEZET_meres.md`.

**Nincs benne:**
- a régi commitok átírása (a történet nem írható át; nincs `--amend`, nincs `--force`);
- helyi `commit-msg` hook (lehetséges folytatás, külön döntés);
- a commit-üzenetek egyéb formai szabályai (tétel-azonosító az elején stb.).

## 3. Lépések

1. Modell-ellenőrzés (`CLAUDE.md`).
2. **M0 — mérés.** A kiinduló mérés megismétlése a végleges kizárási szabályokkal a main teljes kézi commit-történetén: jelölt üzenetek száma, a 30 leggyakoribb jelölt alak, és **50 véletlen jelölt találat kézi besorolása** (valódi hiba / hamis pozitív), rögzített seeddel. Napló: `naplok/COMMIT_EKEZET_meres.md`.
   ⛔ **Megállás:** a mért pontosság és a javasolt szint (D2) a felhasználóé. `DT-F112a` tétel a `DONTESEK.md`-be (pontosság, a két szint-opció, javaslat), `allapot: dontesre_var`.
3. Az E30 megvalósítása a jóváhagyott szinttel; `FAJLSZINTU_SZABALYOK` közé sorolva (a találat nem fájlsorhoz kötődik, mint az E26-nál), a találat részlete: commit rövid hash, a jelölt alak, a javasolt ékezetes alak.
4. Tesztek; `python eszkozok/ellenorzes/futtat.py` kézi futtatása egy szándékosan ékezetlen próba-üzenettel (repón kívüli ideiglenes fájllal, `--commit-uzenet-fajl`).
5. Zárás a `/kovetkezo` 10. lépése szerint. A saját PR commitjai az E30-on maguk is átmennek.

## 4. Elfogadási feltételek

- G1: az E30 a fenti kizárásokat mind alkalmazza; a tesztek zöldek.
- G2: a mérés 50 elemes kézi mintája és a pontosság a naplóban áll, seeddel, újrafuttatható parancssal.
- G3: az E30 szintje a `DT-F112a` döntés szerinti; a döntés előtt nem kerül a `main`-re futó ellenőrzésbe.
- G4: az E30 csak a PR `base..head` commitjait nézi; `push` eseménynél (main) nem fut.
- G5: a kizárási lista minden sorának van `ok` mezője és forrása.
- G6: a CSV-modul nem olvassa a TSV-t (`split('\t')`, `CLAUDE.md` „TSV-olvasás”).

## 5. Döntésnapló

- D1: a szabály száma **E30** (az E28 és az E29 a #23 CI-tervében foglalt: `naplok/MOTIVUM_FORRAS_ci_terv.md`).
- D2: [javaslat] a szint **FIGYELMEZTETÉS**, nem HIBA. Indok: a commit a PR-ban már nem írható át (a #50 D1 szerint sincs `--amend`/`--force`), így a piros CI-t csak a PR újraírásával lehetne zöldre fordítani; a figyelmeztetés a következő commitra hat. A HIBA-szint csak akkor indokolt, ha a mért pontosság magas, és a javítás módja (pl. squash-merge-kor új üzenet) ki van mondva. A végleges szint az M0 után a `DT-F112a`-ban dől el.
- D3: a kétértelmű párok (`meg`, `mert`, `kor`, `sem`, `fel`, `arany` …) soha nem jelölnek; a szabály inkább kihagy, mint téved (CLAUDE.md 3. szabály szellemében: üres eredmény elfogadható).
