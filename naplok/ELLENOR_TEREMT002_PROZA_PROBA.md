ELTÉRÉS: 10 tétel

# Független ellenőrzés — F64_TEREMT002_PROZA_PROBA_BRIEF.md · 0962e4f..47fd7d8 (`git merge-base origin/main HEAD`..HEAD)

*Tanulmány-ellenőrzés (F37 T4): nem él, mert a diff nem hoz `*_bovitett.md` / `*_tanulmany.md` fájlt; a `motivumok/TEREMT-002.md` forrásréteg. A szerep szerint futtatható parancsok: `git diff`, `git log`, `lekerdez.py`, `futtat.py`. Az alábbi parancsok mind a `cd /c/Users/bases/Desktop/wt-f64 &&` előtaggal futottak.*

*A jelentést az ellenőr szövegeként az orkesztrátor mentette és commitolta, mert az ellenőr szerepköre fájlírást és commitot nem enged. Az orkesztrátor kiegészítése a fájl végén, külön jelölve.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Diff-hatókör | OK | — | `git diff --numstat 0962e4f..HEAD`: 12 fájl, +787/−3. Módosított: DONTESEK.md, a brief, motivumok/TEREMT-002.md; a többi új (generalt_proba/TEREMT-002_proza_proba/ 6 fájl, naplok/ 3 fájl) |
| Lista 1 (törölt/kiszűrt sorok) | OK | — | `git diff --name-status --diff-filter=DMR`: csak 3 M, D és R nincs. A törölt sorok: brief-fejléc 2 (allapot, kovetkezo), motivumok/TEREMT-002.md 1 (a dőlt proveniencia-bekezdés, amely a :5 NAPLO-ba került) |
| Lista 2 (kulcstartomány) | OK | `motivumok/TEREMT-002.md:27` | `lekerdez.py gerinc "1Móz 1:2" "Jer 4:23" "Ézs 34:11"` → metszet 3, H9002 kiszűrve, marad H0922 és H8414, n=2 |
| Lista 3 („nulla-diff” hatóköre) | OK (szűk) | — | `git diff --stat 0962e4f..HEAD -- adat konkordancia lexikon tematikus_lezart motivumlog NYITOTT_FELADATOK.md FELADATOK.md` → üres. Erre a hat útvonalra vonatkozik; nem fedi a meglévő generált fájlok fixpontját (l. K3/K4 fixpont) |
| Lista 4 / E17 (tábla-Δ) | OK | adat/, konkordancia/ | Ugyanez a diff üres, tehát mind a 38 `adat/**/*.tsv` és minden `konkordancia/**/*.tsv` Δ=0. Bontási napló nem kell. Új TSV csak a `generalt_proba/…/naplok/F4_naplo_hianylista.tsv` (+58, próbarender, nem adattábla) |
| Lista 5 / ⛔ M0 | OK | brief:9, DONTESEK DT-F64a/b | `git log`: F64.2 megállt, a DT-F64a/b 🟡; a feloldás csak F64.3/F64.4-ben (felhasználó, chat; a chat maga nem ellenőrizhető) |
| Lista 5 / ⛔ M3 | NEM ELLENŐRIZHETŐ | brief:12 | F64.11 megállt; utána F64.12 és F64.13 „a felhasználó jóváhagyásával”. A chat-jóváhagyás repóból nem igazolható. A fejléc `kovetkezo` mezője még az M3 ⛔-ra mutat, M4 (zárás) nincs |
| K1 | NEM ELLENŐRIZHETŐ | — | `git log`: minden commit `Co-Authored-By: Claude Opus 5.5`; az „egy kézben” repóból nem igazolható. Összefüggő próza, jelölőkkel: van |
| K2 / scan | OK | `:172`, `:171` | `lekerdez.py scan H8414` → 19 igehely, 20 szó, n=19; `scan H0922` → 3, n=3. A próza: 19, ebből 16 a pár nélkül (19−3) |
| K2 / kollokáció | OK | `:170` | `lekerdez.py kollokacio H8414 H0922` → 1Móz 1:2, Jer 4:23, Ézs 34:11, n=3 |
| K2 / lxx-hid | OK | `:176–178`, `:85–89` | `lekerdez.py lxx-hid "1Móz 1:2"` → n=19, G0517 ἀόρατος, ἀκατασκεύαστος Strong nélkül, G0012 ἀβύσσου; a G0517 öt ÚSZ-verse egyezik. `lxx-hid "Jer 4:23"` → n=17, G3762 οὐθέν. `lxx-hid "Ézs 34:11"` → n=23, σπαρτίον γεωμετρίας Strong nélkül, G2048 ἐρήμου |
| K2 / domén | OK | `:174–175`, `:29`, `:71` | `lekerdez.py domen H8414` → 2 egység (Non-Exist „waste; desolation; chaos”, Worthless), a H0068 „to stretch the plummet of chaos…” sora is benne. `domen H8414 H0922` → 1 közös (Non-Exist). `domen H0922` → 1 egység |
| K2 / Károli | OK | `:184–194` | `lekerdez.py karoli` 11 versre. Az n-értékek egyeznek (1Móz 1:2 0, 1Móz 1:3 1, Jer 4:23 2, Jer 4:24–27 1-1, Ézs 34:10 1, Ézs 34:11 5, Ézs 45:18 2, Ézs 24:10 0); az idézetek szövege egyezik |
| K2 / TSK (d-jel) | OK | `:81`, `:109` | `lekerdez.py tsk "1Móz 1:2"` → Jer 4,23 Votes=84; `tsk "Jer 4:23"` → 1Móz 1,2 Votes=21; `tsk "Ézs 34:11"` → 2Kir 21,13 és Sir 2,8, Votes=6–6 |
| K2 / TAHOT-sorok | OK | `:53–69` | Grep `^Jer 4:23\t`, `^Ézs 34:11\t` a TAHOT_kivonat.tsv-ben: Jer 4:23 17 szó, a pár mellett nincs ige (הִנֵּה után); Ézs 34:11 22 szó, קַו + תֹהוּ, אַבְנֵי + בֹהוּ, a נָטָה ige tárgyaként |
| K2 / BDB (F64.8) | OK | `:75`, `:180–183` | Grep `BDB_teljes_unabridged.tsv`. 861. sor (H0922): „emptiness … always with תֹּהוּ”, „the line of wasteness and the stones of emptiness, i.e. plummets, employed, not as usual for building, but for destroying walls”. 7849. sor (H8414): „formlessness, of primaeval earth Gen 1:2 (P), of land reduced to primaeval chaos Jer 4:23”. A sérült héber (`קַותֿֿהֹוּ`, `וָבֹהוּ תֹּהוּ`) és a „worthlessness 49:19” valóban a forrásban van. `forditasok.tsv` 62. és 72. sor: BDB, H0922/H8414, „formátlanság, az ősi földről 1Móz 1:2 (P), az ősi káoszba visszasüllyesztett földről Jer 4:23…”, „…mérőzsinórja és az üresség kövei, azaz függőónok…”, `opus`, `claude-opus-5-5`, 2026.10.01: egyezik |
| K2 / P2 proveniencia | **ELTÉRÉS** | `:29`, `:199` | `lekerdez.py kollokacio H8414 H8077/H0950/H1238` → 0, 0, 0; `H0657` → Ézs 40:17, 41:29; `H0205` → Ézs 41:29, 59:4; `H7385` és `H1892` → Ézs 49:4. Az állítás igaz, de lekérdezésből származik, a lábjegyzete mégis `scope=manual`; a lekérdezés saját proveniencia-sora hiányzik (CLAUDE.md 1. szabály) |
| K2 / rossz lábjegyzet-cél | **ELTÉRÉS** | `:111` | Grep `TEREMT-002.*Jer 4:2[4-6]` a `jeloltek.tsv`-ben → nincs sor. A „Jer 4:23–26 a rend elemeit sorra visszavonja” a `kapcsolatok.tsv` 37. sorában áll, a lábjegyzet viszont `[^d-jel]` (jeloltek) |
| K2 / gyenge kitöltés (Kivonat) | **ELTÉRÉS** | `:15`, ellentétben a `:91`-gyel | `lxx-hid` (fent): ἀκατασκεύαστος, σπαρτίον és γεωμετρίας Strong nélkül, az ÚSZ-hídjuk nem számolható. A Kivonat szerint „görög lexikai híd … nem mutatható ki; a motívum az Ószövetségen belül él”. Ez részben üres eredményből levont negatív lelet (CLAUDE.md 3. szabály); a :91 NAPLO maga mondja, hogy „üres, nem negatív lelet” |
| K2 / hiányok explicitek | OK | `:127`, `:143`, `:151–157` | Explicit hiány: a vitatott pont képviselői, a nevesített tanító, az LXX-döntések, a BDB-mezők, az Ézs 34:11 Károli-KH |
| K3 | OK | — | Lista 3. A próbarender csak a `generalt_proba/TEREMT-002_proza_proba/` alatt van (6 új fájl, 0 törölt). A `lexikon/` és a `tematikus_lezart/` diffje üres |
| K3/K4 fixpont (`general.py --ellenoriz`) | NEM ELLENŐRIZHETŐ | — | A parancs a szerep megengedett körén kívül esik. Az író állítása (F64.9: „=0”) nincs igazolva |
| K4 | OK | `:17`, `:91` | `git diff --stat … -- adat` üres, tehát az `lxx_dontesek.tsv` nem változott. „Függő (#12b)” jelölés van |
| K5 | OK | meres.md:41–69, 71–98 | L1–L7 és DT2/1–2 pontonként, forrásra és renderre; a #23 M1-bemenet táblázatban |
| K6 (`ellenoriz.py`, `feladatok.py ellenoriz`) | NEM ELLENŐRIZHETŐ | — | A szerep megengedett körén kívül |
| K6 / CI | OK | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only $B..HEAD) --diff-alap $B --diff-fej HEAD` → kilépési kód 0. E2–E16, E19, E20 0 találat; E25 3 JELENTES/FIGYELMEZTETES (CLAUDE.md, MUNKAMENET.md, nem a diffből); E27 33 JELENTES (ág- és fájlhivatkozás, a kimenet csonkolt). Megadott CI-jelentés nem volt, ezért az összevetés NEM ELLENŐRIZHETŐ |
| K6 / végleges DT/N az ágon | OK | DONTESEK.md | `git diff -- DONTESEK.md`: csak DT-F64a és DT-F64b sor került be |
| A1 | OK | `:7`, `:99`, `:127` | A 3. pont egésze `manual`-jelölt NAPLO-ban; a restitúciós olvasat leírása `manual` |
| A2 | **ELTÉRÉS** | `motivumok/TEREMT-002.md:162` | Read `NYITOTT_FELADATOK.md:229–230`: „N17 … LEZÁRVA (F42.M5, 2026.10.05)”, csak a „tartalmi kérdés, nem javítva” maradt. A forrás NAPLO-ja: „N22 …; N17 … mindkettő változatlanul nyitott”. Az N22 (:301) és az N25 (:321) valóban nyitott |
| A3 | **ELTÉRÉS** | `:113` | `lekerdez.py scan H8414` → az Ézs 24:10 *tohu*-vers. Az Ézs 45:18 címkéje helyes („a formula szempontjából tematikus, nem lexikai”); az Ézs 24:10 viszont minősítés nélkül „tematikus, nem lexikai kapcsolat”, pedig a H8414 lexikailag közös. A 2Kir 21:13 / JSir 2:8 jelölése helyes |
| A4 / Remez | **ELTÉRÉS** | `:113` | A Remezben következtetés áll: „A *tohu* állapota tehát nem a teremtés célja; a cél a lakhatóság.” Ez tanítás, a Drash/Sod szintjére tartozik |
| A4 / Sod | OK | `:123` ← `:101–107`, `:117` | „Ugyanaz a szókincs … a rend előtt és az ítélet után” ← Peshat :107. „A rend … a Teremtő szavának … ajándéka; ahol a viszony megszakad…” ← Drash :117 („Isten szava hozott létre … a hozzá való viszonyban áll fenn”; „a rend visszavétele”) |
| A5 | OK | `:141–143`, `:156` | Nevesített tanító nincs, a hiány explicit (a 7. lépés nem futott) |
| A6 | OK | — | `futtat.py`: E12–E15 0 találat, nincs megítélendő figyelmeztetés |
| ⚠️ vitatott pont | **ELTÉRÉS** | `:125` | A próza a vitát a saját oldalán zárja le („A motívum ezért a kiinduló-állapot olvasatot követi”), megnevezett képviselő nélkül. Az egyik érv körkörös: „az adatban rögzített kapcsolatok iránya az 1Móz 1:2-től a próféták felé mutat”. Ezt az irányt a T2 rögzítette (`kapcsolatok.tsv` 37–40. sor), tehát nem szöveg-adat. A felhasználói döntést a meres.md:109 is kéri |
| DT-F64a/DT-F64b ↔ próza | OK | `:7`, `:176–178`, DONTESEK +2 sor | A próza helye a `motivumok/` (DT-F64a (1)); a mérce L1–L7 + DT2 (meres.md:39–51); a friss `lxx-hid` futás audit-sor nélkül (DT-F64b) |
| DT-F64b szövege | **ELTÉRÉS** | DONTESEK.md, DT-F64b | Grep a `FORRASKIVEZETES_M5_eltereslista.tsv`-ben: `zsoltar_eltolas` csak a Zsolt 80:6 és 80:7; a 104:30 `strong_eltero`, a 107:40 `nagy_eltero`, a 33:6 nincs a listán. A DT-F64b kérdésszövege mégis mind az ötöt eltolásosnak írja; a javítás csak a lxx_friss.md:26-ban és a meres.md:117-ben áll, a döntési sorban nincs jelölve |
| L2 (forrásproza) | OK | `:31–33`, `:151–162` | Read: a folyamatmondatok NAPLO-ban állnak; a 12 NAPLO-blokk száma Grep `【NAPLO`-val igazolva |
| L7 | OK (megjegyzéssel) | `:121` | A Drash az Ézs 45:18-at kereszthivatkozással veszi át. A Remez-következtetés: l. A4 |
| Mérés 7. szakasz | **ELTÉRÉS** | meres.md:121 | Read `lexikon/ISTENTISZT-001_TUDOMANYOS.md:342–420` és `adat/szotar_szerepek.tsv`. Strongonként halad, ez helyes, és LSJ (444. sor) is van a 2. szakaszban. De a 4. szerep (szemantikai mező) Strongonként a 2. szakaszban áll („**Szemantikai domén:**”, 352., 382., 404. sor), nem „csak a 2/b-ben”. A héber 3. szerep TWOT-száma (380., 402. sor) sincs említve. A kiejtés (10.) a 🇭🇺 sorokban részben megjelenik |
| Mérés / jelölőszámok | **ELTÉRÉS** | meres.md:19; F64.5 üzenet | Grep `<!-- (SZINT\|INAKTÍV\|ADAT-NÉZET):` → valódi jelölő: SZINT 6, INAKTÍV 5, ADAT-NÉZET 4; mindháromhoz +1 a :7 NAPLO-ban álló említés. A mérés 7/6/5-öt ír; az F64.5 üzenete 6 INAKTÍV-t ír, de 5-öt sorol fel, 5 ADAT-NÉZET-et, de 4-et |
| Mérés / többi szám | OK | meres.md:14–18 | 32 lábjegyzet; 20 friss futás (gerinc 1, kollokáció 1, scan 2, domén 2, lxx-hid 3, karoli 11); 12 NAPLO-blokk: megszámolva |
| Commit-üzenetek | OK | `git log --format='%h%n%B'` | 16 commit, magyarul, F64.<n> előtaggal. Az F64.5 „karoli ×10” hibáját az F64.6 javítja (11 igaz). Az F64.9a sorrendje ismert. Az F64.9 „6 fájl” igaz (numstat). Az F64.12 „generalt_proba nem változott” igaz (az F64.9 után nincs generalt_proba-diff) |

**Az ELTÉRÉS-ek súlyosság szerint:**
1. Közepes: a ⚠️ vitatott pontot a próza körkörös érvvel, képviselő nélkül zárja le (`:125`).
2. Közepes: a Kivonat üres LXX-híderedményből negatív leletet von le (`:15`).
3. Alacsony–közepes: következtetés a Remezben (`:113`, A4).
4. Alacsony: N17 „nyitottnak” jelölve (`:162`, A2).
5. Alacsony: az Ézs 24:10 „nem lexikai” címkéje (`:113`, A3).
6. Alacsony: a P2 lekérdezéses állításai `manual` provenienciával (`:199`).
7. Alacsony: rossz lábjegyzet-cél, `[^d-jel]` a `[^d-kapcs]` helyett (`:111`).
8. Alacsony: a mérés 7. szakaszának pontatlan szerepleírása.
9. Alacsony: a jelölőszámok +1-gyel túlszámolva.
10. Alacsony: a DT-F64b kérdésszövegében javítatlan zsoltárállítás.

---

## Orkesztrátor-kiegészítés (nem az ellenőr szövege)

A három NEM ELLENŐRIZHETŐ parancs, az orkesztrátor futtatásában (2026-10-08, a `wt-f64` munkakönyvtárban, HEAD `47fd7d8`):

| parancs | eredmény |
|---|---|
| `python eszkozok/general.py --cel naplo --ellenoriz` | 0, ZÖLD |
| `python eszkozok/general.py --cel index --ellenoriz` | 0, ZÖLD |
| `python eszkozok/general.py --cel nyitott --ellenoriz` | 0, ZÖLD |
| `python eszkozok/feladatok.py ellenoriz` | 95 brief, 0 hiba, 0 figyelmeztetés |
| `python eszkozok/ellenoriz.py` | 0 |
