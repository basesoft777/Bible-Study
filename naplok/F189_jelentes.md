# F189 — jelentés: a /kovetkezo alapesete subagent nélküli végrehajtás, és a CLAUDE.md karcsúsítása

*Brief: `F189_KOVETKEZO_KARCSU_BRIEF.md` · ág: `claude/teher-kovetkezo-claude-4e1093` · modell: `claude-opus-5-5` (a kért modell `opus`, egyezik) · 2026-11-11*

## Menet

- **F189.0** — a brief (`allapot: fut`) és a DT-F189a helyőrző (`dontesek/uj/teher-kovetkezo-claude-4e1093.md`, 🟢: a felhasználó jóváhagyása az orkesztrátoron át: „csináljuk meg”, „csináljuk”, „menjen párhuzamosan”).
- **F189.1** — A) rész:
  - `.claude/commands/kovetkezo.md`: az 5. lépés javaslata a végrehajtás módját nevezi meg; a 6. lépés alapesete a session saját végrehajtása. A lépésszámozás változatlan, így a `feladatok.py` 94. sorának hivatkozása (8. lépés, `FOLYTATAS_ELOTAG`) érvényes marad.
  - `.claude/commands/elteres.md`, 4. lépés: ugyanez a javítókörre.
  - `.claude/agents/vegrehajto-*.md`: a leírás megnevezi a három hívási esetet; a törzs szabályai a subagent nélkül végrehajtó sessionre is érvényesek (egy hely).
  - `MUNKAMENET.md` „Szereposztás”: új „végrehajtó” pont.
  - A brief `olvas` mezőjét szűkítettem, mert az első változat függési kört okozott (`feladatok.py ellenoriz`: #111 ↔ #121 ↔ #123 ↔ #156 ↔ #178 ↔ #189).
- **F189.2** — B) rész:
  - A `CLAUDE.md` magyarázó részei szó szerint az új `CSAPDAK.md`-be kerültek.
  - A `CLAUDE.md`-ben a szabály maradt, hivatkozással; a szakaszcímek változatlanok, mert kód, briefek és az E27/E36 hivatkozik rájuk.
  - A „Modell-ellenőrzés” szakasz a DT-F189a szerint változott.
  - A `CSAPDAK.md` a `feladatok.py` `SZINT_KONNYITETT_FAJL` listájára került (dokumentáció).

### A) — mely esetekben marad subagent

| Eset | Végrehajtó |
|---|---|
| a session modellje = a brief `modell` mezője | **a session maga, subagent nélkül** (új alapeset) |
| eltérő modell, a felhasználó nem kér új sessiont | `vegrehajto-<brief modellje>` subagent |
| eltérő modell, a brief kifejezetten subagent nélküli futást ír elő (pl. #38 D7) | csak új session |
| csomagmód (6b. lépés) | `vegrehajto-*` subagentek, párhuzamosan, külön worktree-ben (változatlan) |
| `külső:<név>` brief | `vegrehajto-sonnet` burkoló (változatlan) |
| független ellenőrzés (9. lépés, `/elteres` 5. lépés) | `fuggetlen-ellenor` subagent (változatlan; friss kontextus kell) |

A takarékos szabály nem változott: egy független ellenőrzés, legfeljebb egy javítókör. A modell-ellenőrzés a 6. lépés elején történik, a „mehet” utáni fordulóban ténylegesen futó modellel. Ezért nem függ attól, hogy a parancs frontmatterje `model: sonnet`.

### B) — a CLAUDE.md mérete

| | bájt (munkapéldány, CRLF) | bájt (repó, LF) | sor |
|---|---|---|---|
| előtte (`f66f0fcc`) | 18 132 | 17 909 | 223 |
| utána | 14 102 | 13 938 | 164 |

Csökkenés: 4 030 bájt (−22%). A `CSAPDAK.md` 6 275 bájt (LF), és csak akkor töltődik be, ha megnyitják.

### B) — szabálylista-összevetés (régi → új)

Az áthelyezett szakaszok minden szabálya és állítása:

| # | Régi `CLAUDE.md` | Új hely | Állapot |
|---|---|---|---|
| S1 | héber/görög/magyar kódot inline `bash -c`-vel nem futtatsz; fájlba írod, a fájlt futtatod | `CLAUDE.md` „Shell”, 1. pont | megmaradt |
| S2 | az idézett heredoc-határoló sem véd minden esetben | `CLAUDE.md` „Shell”, 1. pont („heredoccal sem”), az ok: `CSAPDAK.md` | megmaradt, tiltásként kimondva |
| S3 | magyar kimenet: utf-8 nélkül `cp1250` `UnicodeEncodeError` | `CSAPDAK.md`; a szabály (wrapper) a `CLAUDE.md`-ben | ok áthelyezve |
| S4 | minden `eszkozok/*.py` a docstring és az importok után ráteszi a `reconfigure(utf-8)` wrappert | `CLAUDE.md` „Shell”, 2. pont; a kódminta a `CSAPDAK.md`-ben | megmaradt |
| S5 | a wrapper az importblokk után álljon (`NameError`) | `CLAUDE.md` „Shell”, 2. pont (kiemelve); a dokumentált esetek a `CSAPDAK.md`-ben | megmaradt |
| S6 | a `PYTHONIOENCODING` tartalék, nem előfeltétel | `CLAUDE.md` „Shell”, 2. pont | megmaradt |
| S7 | az olvasó-szerver tesztjei csak `python eszkozok/teszt_futtat.py`-vel (`--gyors`) | `CLAUDE.md` „Shell”, 3. pont | megmaradt |
| S8 | a futtató a WSL venv-et és a natív DB-t választja; a `/mnt/c`-ről 45+ perc (#100, DT160) | `CSAPDAK.md` | tény/ok, áthelyezve |
| T1 | TSV olvasása `split('\t')`, írása `'\t'.join()` | `CLAUDE.md` „TSV-olvasás” (szó szerint) | megmaradt |
| T2 | a `csv` modul nem használható | `CLAUDE.md` szakaszcím + 1 mondat | megmaradt |
| T3 | ha mégis `csv`: `QUOTE_NONE, quotechar=None` mindkét irányban | `CLAUDE.md` (szó szerint) | megmaradt |
| T4 | táblát író szkript írás előtt összevet, eltérésnél megáll (`igazolas_migracio.py`) | `CLAUDE.md` (szó szerint) | megmaradt |
| T5 | a mért kár (79 mező / 127 sor), a „legveszélyesebb csapda” indoklás, nincs tab a mezőkben | `CSAPDAK.md` (szó szerint) | ok áthelyezve |
| A1 | TAHOT: fejezet-szinten nincs hiány | `CLAUDE.md` „Adat-tár” | megmaradt |
| A2 | az `Igehely` kulcs a Károli-vers | `CLAUDE.md` | megmaradt |
| A3 | a 9 összevont versnél mindkét vers a közös kulcson (`f22/versosszevonas.tsv`) | `CLAUDE.md` | megmaradt |
| A4 | a fájlsorrend nem Károli-sorrend, kulcs szerint olvass | `CLAUDE.md` (kiemelve) | megmaradt |
| A5 | a pótlások (F2, F84), az eltolások listája, a kulcs-összevetés számai és naplói | `CSAPDAK.md` (szó szerint) | részlet áthelyezve |
| G1 | a commit-granularitás tétel-szintű (`F3.0`, `F3.1` …) | `CLAUDE.md` „Git” | megmaradt |
| G2 | a commit-üzenet UTF-8 fájlból megy, inline `-m` soha; a parancs | `CLAUDE.md` „Git” (a parancs egy sorban) | megmaradt |
| G3 | az ékezetes üzenet (a `git log --grep` miatt) | `CLAUDE.md` „Git” („ékezetesen”); az ok a `CSAPDAK.md`-ben | megmaradt, tiltásként kimondva |
| G4 | a granularitás és a fájlból írt üzenet oka | `CSAPDAK.md` | ok áthelyezve |
| M1–M3, M5–M7 | a „Modell-ellenőrzés” szakasz: első lépés; a kért modell a végrehajtónak a brief `modell` mezője, az ellenőrnek a saját fájlja; `külső:<név>`; eltérésnél nincs munka; az adattábla `modell` mezője | `CLAUDE.md` „Modell-ellenőrzés” | megmaradt (szó szerint) |
| M4 | „a `/kovetkezo` orkesztrátor nem végrehajt …, az ellenőrzése a végrehajtóra hárul” | `CLAUDE.md` „Modell-ellenőrzés” + `kovetkezo.md` 6. lépés | **szándékosan megváltozott** (DT-F189a): az ellenőrzés a sessionre hárul; eltérésnél a session nem dolgozik, a felhasználó új sessiont vagy subagentet választ |

Eredmény: a szabályok közül egy sem veszett el. Kettő szigorodott, mert kimondott tiltás lett, ami korábban csak indoklásban állt (S2, G3). Szándékosan egy változott (M4). Az áthelyezett tartalom indoklás, mért kár vagy részlet. Ezt a `CSAPDAK.md` szó szerint hordozza, és szakaszonként visszamutat a szabály helyére. A többi szakasz (Rétegek, Három szabály, Kutatási menet, Új motívum-ID, Igehely-formátum, a Git helyőrző-szabályai) változatlan.

Hivatkozások (E27/E36): a `CLAUDE.md` szakaszcímeire mutató hivatkozások (szkriptek, briefek, `BRIEF_SABLON.md`, ügynökök: „TSV-olvasás”, „Shell”, „Git”, „Modell-ellenőrzés”, „Adat-tár”, „Ezt olvasd”) változatlan címre mutatnak. A `F4_BRIEF.md` „importok előtt” idézete archív brief, és a kódmintára vonatkozik, amely a `CSAPDAK.md`-ben szó szerint megvan.

### Tudnivalók az orkesztrátornak

- `feladatok.py fuggesek`: `KIZAR` a #182-vel és több más feladattal a `MUNKAMENET.md`-n, a #188-cal és a #111-gyel a `kovetkezo.md`/`elteres.md`-n. A #182 párhuzamos futását a felhasználó jóváhagyta. A `MUNKAMENET.md`-ben itt egyetlen pont változott (a „Szereposztás” szakaszban), merge-ütközés csak akkor várható, ha a #182 ugyanazt a szakaszt írja.
- További karcsúsítási jelölt, nem e feladat hatóköre: a „Rétegek” szakasz „kilenc rés” bekezdése (kb. 1,2 KB). Nem mozdítottam, mert DT-hivatkozás mutat rá.

### Helyi ellenőrzés

- `python eszkozok/ellenorzes/futtat.py --valtozott … --diff-alap <merge-base> --diff-fej HEAD --esemeny pull_request`: kilépési kód 0, 0 HIBA. A figyelmeztetések (`MUNKAMENET.md:70`, `:247`, `adat/elofordulasok.tsv`) régi sorokra mutatnak, nem e diff soraira.
- `python eszkozok/teszt_futtat.py --gyors`: 10 tesztfájl, mind zöld, 338,6 mp (adatbázis: WSL-natív `~/pardes/pardes.db`).
- `python eszkozok/feladatok.py ellenoriz`: 206 brief, 0 hiba; `szint 189`: `konnyitett`, 1 kör.
