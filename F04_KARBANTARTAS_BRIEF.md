---
feladat: 4
cim: Szkript-karbantartás
kod: KARBANTARTAS KB0–KB4
tipus: feladat
fazis: 1
modell: sonnet
allapot: lezarva
ad: importbiztos szkriptek, CRLF-tűrés, a Károli-tábla nullázása
kovetkezo: lezárva
fugg: [2]
lezarva_osszegzes: K1–K10 teljesül (K10 öt körben, ágleltárral, nulla-kimenet-őrrel és három mutációs/hiba-próbával: `naplok/ELLENOR_KARB.md`), merge `b8a418a` (09.27); mérőszkript-vakfoltok és -őrök javítása, PR #60 (`8bd1e40`), PR #61
---
# F04_KARBANTARTAS_BRIEF.md — Szkript-karbantartás: importbiztos régi szkriptek, Windows-sorvég tűrése, a Károli-tábla nullázása

*v3.1 — 2026.09.27 · **FELADATOK #4** · Állapot: futtatásra kész (a #2 merge-e megvan: PR #57, `68eb348`) · A §0 a 09.25-i mérés, változatlanul; a KB0 újraméri · A G1–G7 a v2 óta változatlan, a G8 új*

**Cél.** Három javítás egy menetben:
- **(1a) Importbiztos szkriptek:** a 10 őr nélküli `eszkozok/*.py` ne fusson le importra és `--help`-re. Argumentum nélküli hívásra a viselkedése bájtra azonos maradjon.
- **(1b) Windows-sorvég (CRLF) tűrése:** a 4 mért szkript CRLF-sorvégű bemeneten se szennyezze az utolsó mezőt.
- **(1c) Nullázás:** a `konkordancia/Karoli_Strong_kivonat.tsv` 26 nullázatlan sora a SEMA 1.2 szerinti alakot kapja.

Forrás: a `NYITOTT_FELADATOK.md` két „ÚJ (F4-0, 2026.09.14)” tétele, az F3.4-es „26 nullázatlan join-sor” tétel és az N21.

**Előfeltétel:** a #2 (CI) merge-e a `main`-ben. Ez nem tartalmi okból kell, hanem az ellenőrzés miatt: a chat a CI eredményét és a független ellenőr jelentését olvassa, a teljes repót nem tölti le (FELADATOK, Munkamenet 4). A #1 (KK) merge-e nem feltétel, mert a KK-ág a Károli-táblához nem nyúl (független ellenőrzés, 2026.09.25). Ha a #1 már bent van, a menet arról indul.

A menet semmit nem akaszt meg. A mostani menetek (TEREMT-002, SZOTAR, render) egyik érintett szkriptet sem hívják, és a Károli-táblát élő eszköz (`general.py`, `lekerdez.py`, `jelolt.py`, `betolt.py`, `ellenoriz.py`) nem olvassa.

**Futás:** cloud (a kreditből) vagy helyi, külön ágon.
**Modell:** Sonnet.
**Push:** csak a saját ágra, a `main`-re soha. A merge-et a felhasználó indítja.

**Szerkezet.** Egy menet, KB0–KB4, gépi kapuval. Emberi ⛔ megállás nincs, mert tartalmi döntés nincs benne.

**Nincs benne:**
- írás az `adat/`, `lexikon/`, `tematikus_lezart/`, `motivumok/` alá;
- írás a `konkordancia/` alá a KB3 26 során kívül;
- a szkriptek futtatása a munkapéldányban;
- új parancssori opció;
- a `csv` modul bevezetése;
- más szkriptek javítása (ezek csak a jelentésbe kerülnek).

---

## 0. Kiindulás *(a KB0 újraméri; eltérésnél jelentsd, és folytasd)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` | legalább `68eb348` (a #2 merge-e, PR #57). A KB0 rögzíti a tényleges HEAD-et; ha azóta a #1 is bekerült, az is. |
| 0.2 | őr és argparse nélküli szkriptek (1a) | 10: `f3_1_betoltes.py`, `f3_2_betoltes.py`, `f3_4_ellenoriz.py`, `f3_4_elokeszites.py`, `f3_4_gorog_ellenoriz.py`, `f3_4_join_potlas.py`, `f3_4_munkalap_general.py`, `f3_4_nema_nemtalalat.py`, `f3_4_zaro_ellenoriz.py`, `merge_karoli_szofaj.py` |
| 0.3 | ebből modulszinten fájlt ír | 8 (mind, kivéve `f3_4_gorog_ellenoriz.py` és `f3_4_zaro_ellenoriz.py`) |
| 0.4 | `\r`-t nem strippelő mezőbontás (1b) | 4: `elofordulas_szamlalo.py:37`, `f3_4_zaro_ellenoriz.py:17`, `frazis_kereses_pozicio_alapon.py:58`, `tahot_zarojeles_phaseA_kivonat.py:84` |
| 0.5 | `rstrip("\n")` összesen az `eszkozok/`-ban | 35 fájl (a többség utána nem bont `\t`-re, ezért csak jelentés) |
| 0.6 | `eszkozok/ellenoriz.py` | RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 |
| 0.7 | `Karoli_Strong_kivonat.tsv` nullázatlan sor (1c) | 383 adatsorból 26 sor, 27 token (13 egyszerű, 13 `+`-os összetett); pl. `Gen.1.1 H430`, `Gen.1.2 H8414+H922` |
| 0.8 | a Károli-tábla olvasói | 6: `f3_4_elokeszites.py`, `f3_4_join_potlas.py`, `f3_4_zaro_ellenoriz.py`, `merge_karoli_szofaj.py`, `f4_0c_korut_ellenoriz.py`, `inline_strong_megjelenito.py`; élő eszköz egy sem |
| 0.9 | CI a `main`-en | a KB0 rögzíti a workflow nevét és a szabálykészletet (E1–E16). Ha valamelyik szabály az érintett szkripteket vagy a Károli-táblát vizsgálja, azt fel kell jegyezni. |

---

## 1. Mércék

- **Egyenértékűség (1a).** Minden szkriptet két friss, ideiglenes repó-másolatban kell futtatni, a munkapéldányon kívül (pl. `git worktree add /tmp/kb_regi <alap>` és `/tmp/kb_uj HEAD`). Argumentum nélkül fut a régi és az új változat, és ezeknek kell teljesülniük:
  - a kilépési kód azonos;
  - a másolat összes fájljának sha256-listája a futás után azonos;
  - a stdout azonos (az időbélyeg-sor maszkolva, ha van).

  Ha a régi változat a mai adaton hibával áll le, az újnak ugyanazzal a kivételtípussal, ugyanazon a ponton kell leállnia.
- **Mellékhatás-mentesség (1a).** A másolatban:
  - `python eszkozok/X.py --help` → kilépési kód 0, súgószöveg, és `git status --porcelain` üres;
  - a modul importja (`importlib`) → nincs írás és nincs stdout.
- **CRLF-tűrés (1b).** Minden érintett szkript kap egy LF és egy CRLF változatú ideiglenes bemenetet. Ez a szkript valódi bemenetének másolata, fájlba írt Python-szkripttel konvertálva. Mindkét bemeneten azonos az utolsó mező, és nincs benne `\r`. A régi változatnak a CRLF-bemeneten bizonyítottan hibáznia kell, vagyis a teszt pirosról zöldre vált.
- **Nullázás (1c).** A `git diff --word-diff` pontosan a 26 sor Strong-mezőjét mutatja. Utána 0 nullázatlan token marad, a sorok száma és sorrendje változatlan.

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | Minimális beavatkozás: a modulszintű mellékhatások (fájlolvasás, -írás, kiírás, ciklusok) egy `main()`-be kerülnek. Az importok, a konstansok és a függvénydefiníciók modulszinten maradnak. Ha egy függvény olyan modulszintű változót olvas, amely eddig a mellékhatásos részben keletkezett, a változó paraméterként adódik át. Ha ez a törzs átírását kívánná, `global` deklarációt kell használni, és a jelentésben meg kell jelölni. |
| G2 | Az argparse csak `description`-t kap, a szkript fejléc-docstringjéből. Új opció nincs, a beégetett útvonalak maradnak. |
| G3 | Az 1b a 4 mért szkriptben `rstrip("\n")` → `rstrip("\r\n")` csere ott, ahol utána mezőbontás jön. Az 1a 10 szkriptjében ugyanez a minta is javítható, mert a menet úgyis ezekhez a fájlokhoz nyúl. Más szkriptben csak jelentés készül. |
| G4 | A szkriptek soha nem futnak a munkapéldányban, csak ideiglenes másolatban, mert a 8 író szkript a kanonikus táblákat írná. |
| G5 | Közös fájlt a menet nem ír (`NYITOTT_FELADATOK.md`, changelogok, más briefek döntésnaplói). A tételek lezárását a heti zárócommit vezeti át a jelentésből. **Kivétel, két ponton a `FELADATOK.md`-ben:** (a) a menet **első** commitja a #2-es sort törli az 1. fázis táblájából, és a „Kész” lista elejére ezt a sort írja: „Gépi ellenőrzés GitHubon (CI, #2), PR #57, merge `68eb348` (09.27)”; (b) a menet **utolsó** commitja frissíti a #4-es sort (állapot, ág, következő lépés). Más sort nem módosít. |
| G6 | 1c: minden token `H`/`G` + négyjegyű szám alakot kap, a betű-utótag megmarad (SEMA 1.2). Csak a Strong-oszlop változik; a sor többi mezője, a többi sor és a sorrend bájtra azonos. |
| G7 | A KB1 egyenértékűségi tesztje a KB3 előtt fut, a kiinduló commit adatán, hogy a két tétel mérése ne keveredjen. |
| G8 | Az ellenőrzés a FELADATOK munkamenete szerint zajlik: PR a `main` felé merge nélkül, zöld CI, és a `fuggetlen-ellenor` ügynök jelentése (`naplok/ELLENOR_KARB.md`). A chat csak ezt a kettőt és a legfeljebb 20 soros záró összefoglalót olvassa. |

---

## 3. Tételek

- **KB0 — Kiindulási mérés.**
  - A §0 újramérése, a 0.9-cel együtt.
  - Friss grep: van-e még őr nélküli, modulszinten író `eszkozok/*.py` a 10-en kívül (csak lista).
  - Ki importálja vagy hívja a 13 érintett szkriptet (`grep` az `eszkozok/`, `.claude/`, `*.md` alatt).
  - Eredmény: `naplok/KARB_KB0_kiindulas.md`.

- **KB1 — Importbiztos szkriptek (1a: `__main__`-őr és argparse, 10 szkript).**
  - Szkriptenként a G1–G2 szerint, utána azonnal a §1 egyenértékűségi és mellékhatás-tesztje.
  - A mérőszkript fájlba írva: `naplok/KARB_egyenertekuseg.py`.
  - Eredmény: `naplok/KARB_KB1_egyenertekuseg.tsv`, oszlopai: szkript, régi kód, új kód, fájl-sha egyezik, stdout egyezik, `--help` tiszta, import tiszta.
  - Commit: `KB1: __main__-őr és argparse (N szkript)`.

- **KB2 — Windows-sorvég tűrése (1b: CRLF).**
  - A G3 szerint, a §1 CRLF-tesztjével, fájlba írt szkripttel: `naplok/KARB_crlf_teszt.py`.
  - Eredmény: `naplok/KARB_KB2_crlf.tsv`, oszlopai: szkript, sor, régi eredmény CRLF-en, új eredmény CRLF-en.
  - A KB0-ban talált további helyek csak a jelentésbe kerülnek.
  - Commit: `KB2: CRLF-tűrés (N szkript)`.

- **KB3 — A Károli-tábla Strong-számainak nullázása (1c, N21).**
  - Előbb hívásellenőrzés: a 0.8 hat olvasója hogyan illeszti a Strong-számot (saját nullázás, szöveges egyezés vagy TAHOT-join). Ha valamelyik a nullázatlan alakra épít, azt a jelentés jelzi, de a régi szkriptet ezért nem javítod.
  - Utána a nullázás fájlba írt szkripttel: `naplok/KARB_KB3_nullaz.py`. Minta a `naplok/FORRAS_K6_nullaz.py`, ha alkalmas.
  - Előtte–utána tábla: `naplok/KARB_KB3_nullazas.tsv`, oszlopai: igehely, régi, új.
  - Commit: `KB3: Karoli_Strong_kivonat nullázás (26 sor, N21)`.

- **KB4 — Jelentés, gépi kapu, ellenőrzés.**
  - `naplok/KARB_jelentes.md`, tartalma:
    - szkriptenként a változtatott sorok tartománya;
    - a KB1/KB2/KB3 összesítése;
    - a hívásellenőrzés eredménye;
    - a nem javított további helyek;
    - a lezárandó tételek (a két F4-0-s tétel, az F3.4-es tétel, N21) javasolt lezáró szövege a heti zárócommithoz.
  - A §4 K1–K8 ellenőrzése.
  - Push a saját ágra, majd PR a `main` felé, merge nélkül.
  - A CI megvárása (K9).
  - A `fuggetlen-ellenor` ügynök futtatása (K10).
  - Utolsó commit: `naplok/ELLENOR_KARB.md` és a `FELADATOK.md` #4-es sora (G5). Utána push.
  - ÁLLJ, jelentés a chatbe.

---

## 4. Elfogadási feltételek (gépi kapu)

| # | Feltétel |
|---|---|
| K1 | A `git diff --stat main..HEAD` csak ezeket a fájlokat mutatja: `F04_KARBANTARTAS_BRIEF.md`, a 13 érintett `eszkozok/*.py`, `konkordancia/Karoli_Strong_kivonat.tsv`, `naplok/KARB_*`, `naplok/ELLENOR_KARB.md`, `FELADATOK.md` (csak a #2-es sor Kész-listába mozgatása és a #4-es sor, G5) |
| K2 | `eszkozok/ellenoriz.py`: változatlan a KB0-ban mért 0.6-hoz képest |
| K3 | KB1: 10/10 sor „egyezik” mind a négy oszlopban (vagy azonos hibás leállás, megjelölve) |
| K4 | KB2: a 4 szkript CRLF-tesztje zöld, a régi változaté piros |
| K5 | A munkapéldányban a KB3 26 során kívül egyetlen adat- vagy konkordanciafájl sem változott |
| K6 | Nincs `csv` modul és nincs új opció. Héber, görög vagy magyar szöveget tartalmazó kód csak fájlból futhat (CLAUDE.md, Shell) |
| K7 | A jelentésben minden szkriptnél szerepel a változtatott sorok tartománya |
| K8 | KB3: pontosan 26 sor változott, csak a Strong-mezőben; utána 0 nullázatlan token |
| K9 | A CI zöld a PR-en (`gh pr checks`, ha elérhető; ha nem, a PR linkje a jelentésben) |
| K10 | A `naplok/ELLENOR_KARB.md` elkészült. Ha eltérést jelez, az a chat-jelentés első sorába kerül |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás | Indok | Elvetett alternatíva |
|---|---|---|---|---|
| v1 | 2026.09.25 | Első változat: 1a + 1b egy menetben, gépi kapuval; futtatás csak ideiglenes másolatban (G4); az 1c a KK-merge utánra halasztva | — | — |
| v2 | 2026.09.25 | Az 1c bekerül ugyanebbe a menetbe (KB3). Nullázási szabály (G6), sorrend a KB1 tesztje miatt (G7) | A KK-ág független ellenőrzése szerint a Károli-táblához nem nyúl, és élő eszköz nem olvassa | 1c külön menetben, a KK után |
| v3 | 2026.09.27 | FELADATOK #4 hivatkozás. Előfeltétel: a #2 (CI) merge-e; a #1 nem feltétel. A §0.1 a merge utáni HEAD; új 0.9 (CI-szabályok). G5-kivétel a `FELADATOK.md` saját sorára; új G8. K1 bővítve; új K9 (CI zöld) és K10 (független ellenőr). Köznyelvi tételnevek. A chat-jelentés legfeljebb 20 sor | A chat csak a CI-t és az ellenőr jelentését olvassa, a 92 MB-os teljes letöltés nélkül. A KK tartalmilag független a menettől | azonnali futás CI nélkül (a chatnek teljes letöltéssel kellene ellenőriznie); a #1 megvárása (nincs tartalmi függés) |
| v3 | 2026.09.27 | A §0 számai változatlanok | A KB0 úgyis újraméri, és az eltérést jelenti | a §0 kézi újramérése a brief előtt |
| v3.1 | 2026.09.27 | A #2 merge-e megtörtént (PR #57, `68eb348`). A §0.1 erre a commitra mutat. A G5 szerint a #2 Kész-sorát a menet első commitja írja be, a K1 ennek megfelelően bővült | A CI-session lezárásakor így döntöttél: nincs külön push vagy PR a FELADATOK.md frissítéséhez | külön takarító-commit a CI-ágon |
| — | 2026.09.28 | **Eltérés rögzítve, a brief NEM nyílik újra:** a SZOTAR S1.4 ellenőrzése egy logikus `1d` folytatást talált (nincs egységes Strong-kód-normalizáló függvény — ugyanaz a hibaosztály, mint az `1c`/N21). Mivel ez a brief (`#4`) már lezárt és mergelt (`b8a418a`, 2026.09.27), a tétel **nem** él KB5-ként ebben a menetben, hanem `NYITOTT_FELADATOK.md` N37-ként fut, `#4/1d` hivatkozással — egy jövőbeli önálló karbantartás-menet nyitja meg, ha a felhasználó jóváhagyja | A `#4` KB0–KB4 gépi kapuja (§4) és a K10 független ellenőrzése egy lezárt, mergelt állapotra vonatkozik; egy utólagos `1d`-sor beszúrása a §3-ba meghamisítaná ezt a lezárt történetet | a brief §3-ának élő bővítése egy új KB5 tétellel |

---

<!-- KOZVETLEN_FUTTATAS -->
## 6. Nyitó prompt (cloud vagy helyi session; a briefet csatold)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t és a FELADATOK.md-t.
Ellenőrizd, hogy a main tartalmazza a 68eb348 commitot (#2 CI merge). Ha nem, ÁLLJ, és jelezd.
1. A csatolt KARBANTARTAS_BRIEF.md-t mentsd a repó gyökerébe, változtatás nélkül.
   Ugyanebben a commitban a FELADATOK.md-ben a #2-es sort mozgasd a Kész listába (G5 a).
   Commit: "KB: KARBANTARTAS_BRIEF.md v3.1 (FELADATOK #4); #2 kész (68eb348)".
2. Hajtsd végre a KB0–KB4 tételeket a brief §3 szerint, a §1 mércéivel és a §2 döntéseivel.
   A szkripteket SOHA ne futtasd a munkapéldányban, csak ideiglenes másolatban (G4).
3. Ellenőrizd a §4 K1–K8 feltételeit, majd pushold a saját ágadat, és nyiss PR-t a main felé
   (merge nélkül). Várd meg a CI-t (K9). Futtasd a fuggetlen-ellenor ügynököt (K10).
4. Utolsó commit: naplok/ELLENOR_KARB.md és a FELADATOK.md #4-es sora
   (állapot, ág, következő lépés). Más sort ne módosíts. Push. A main-re ne pushold.
ÁLLJ: jelentés a chatbe legfeljebb 20 sorban: ág, PR, CI, K1–K10, KB1/KB2/KB3 egy-egy sorban.
A részletek a naplok/KARB_jelentes.md-be kerülnek.
```
<!-- /KOZVETLEN_FUTTATAS -->
