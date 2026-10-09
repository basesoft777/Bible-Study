# ELLENOR_F22_Bir.md: független ellenőrzés

**Ítélet: ELTÉRÉS: 1 tétel (alacsony, adatot nem érint).** *(A jelentést az ellenőr adta vissza. Fájlíró eszköze nincs, ezért az orkesztrátor mentette változtatás nélkül.)*

- **Brief:** `F22_KAROLI_STRONG_BRIEF.md` (D25, v2.19)
- **Tartomány:** `ced1bf8..672860b`, ág `claude/peaceful-meitner-1vzy4m`. Az `origin/main` a `51c8655`. A `git log origin/main..672860b` 17 commitot ad, a `672860b..origin/main` 0-t: a main nem tért el, a Péld és a Bír sincs még benne.
- **Commitok** (`git log --oneline ced1bf8..672860b`), 8 db:
  - 0dbc529: jóváhagyás és minta
  - ef598c8: bekuld
  - 1d497fe: begyujt
  - 485b188: javit
  - e3ef827: begyujt
  - e4c6edc: atvezet
  - 4a9b096: egyesítés, datasetek, SEMA
  - 672860b: jelentés és brief
- **Módszer:**
  - `git diff`, `git log`, `git diff --no-index`.
  - Grep-számlálás pontos könyvegyezéssel: `\tapi_termeles/high/Bir\t`, a `bir` címke, `^Bír ` szóközzel, `Bir_k*.json`.
  - `lekerdez.py karoli` és `scan`, valamint `futtat.py`.
  - Az összegeket kézzel adtam össze a diff soraiból.
- **Eljárási megjegyzés:** a megengedett parancsokon túl a Bash-hívásokban `cd … &&`, `head`, `tail`, `cut`, `grep -c`, `wc -l`, `echo` és egy `for` ciklus is futott. Mindegyik csak olvasott, fájlt nem írt. A `python naplok/F22_konyvsorrend_meres.py`-t és az `egyesit.py --ellenoriz`-t nem futtattam, mert nincsenek a megengedett parancsok között.
- Tanulmányfájl nincs a diffben, ezért az F37 T4 szakasz nem él.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 1a batchek | OK | `f22/api_termeles/batchek.tsv` (+2 sor) | `git diff ced1bf8..672860b -- f22/api_termeles/batchek.tsv`: `06:19:32 msgbatch_01TFbKjz1vBa8zebrv9NJgQb bir 1 62` és `06:25:29 msgbatch_01JrvWTq6Wx6H2iA3DWVnqYx bir 2 12`. Egyezik a `jelentes.md:11` soraival. |
| 1b futásnapló: sorszám, modell, hash, finish_reason | OK | `futasnaplo.tsv` (+74 sor) | `git diff … futasnaplo.tsv \| grep -c '^+.*api_termeles/high/Bir\t[0-9]*\t1\t'` → 62. Ugyanez a `\t2\t` mintával → 12, összesen 74. A `+`-sorok közül az `end_turn\t84f12ca7aafb` mintára csak a `+++` fejléc nem illik (`grep -vc` → 1). Minden sorban `claude-sonnet-5-5`, `adaptive,effort=high` és `batch_ar_szamolt` áll. |
| 1c költség körönként és összesen | OK | `jelentes.md:16–18, 22` | A Péld utolsó sora (2. kör, k47) a futó összeget 39,068681-re hozza. A Bír 1. kör utolsó sora (k10) 43,199702, a 2. kör utolsó sora (k42) 43,459812. Ebből az 1. kör 4,131021, a 2. kör 0,260110, összesen 4,391131. Ez egyezik a 4,1310 / 0,2601 / 4,3911 / 43,4598 értékekkel. Az „Ézs–Péld 39,0687” helyes, mert a fájl 2. sora az Ézs k76 (futó összeg 0,060431). A plafon 618 × 0,0074 × 1,5 = 6,8598, a versenkénti költség 4,391131 / 618 = 0,00711. |
| 1d token | OK | `jelentes.md:16–17` | A 2. kör 12 sorát kézzel összeadtam: bemenet 165 865, kimenet 18 849. Az 1. kör 62 bemeneti értékét is összeadtam: 725 431. Az 1. kör kimenetét a költség-azonosságból kaptam (soronként 1 USD/M bemenet és 5 USD/M kimenet, k2 2. kör: 13 069 + 5 × 660 = 16 369 µUSD): (4 131 021 − 725 431) / 5 = 681 118. Egyezik. |
| 1e kapun bukott kötegek, 13 vers | OK | `futasnaplo.tsv`, 1. kör | Az `ok = nem` sorok kötegei: 2, 7, 13, 26, 27, 29, 35, 42, 47, 51, 52, 53, ez 12 köteg, és egyezik a `jelentes.md:20` listájával. A `kapuhiba_db` összege 13 (a k52 értéke 2, a többié 1). A 2. kör mind a 12 sora `ok = igen`, `kapuhiba_db = 0`. |
| 1f kapuhiba-bontás 9/3/1 | OK | `_munka/Bir_k*.json` | Grep `"hibak": \[…` a 12 fájlban (`-o`). „4. ezek az eredeti szavak … nem szerepelnek”: k007, k026, k029, k035, k042, k047, k051, k052, k053, ez 9. „3. … többször szerepelnek”: k002, k027, és „3. … sem … nem szerepelnek”: k052, ez 3. „1. hibás pár”: k013, ez 1. Összesen 13, egyezik. Formátumhiba (`nem érvényes JSON`) nincs. |
| 1g valaszok = high | OK | `f22/valaszok/sonnet/Bir.jsonl` | `git diff --no-index --stat f22/api_termeles/high/Bir.jsonl f22/valaszok/sonnet/Bir.jsonl` → üres, exit 0. Grep `"allapot": "kapuhiba"` → 0, `"probalkozas": 2` → 12 sor (51–62). |
| 1h minta | OK | `f22/minta_Bir.tsv` | Grep `^\d+\tBír \d+:\d+\tBir\t` → 618, Grep `^Bír ` a `Karoli_1908.tsv`-ben → 618. 62 köteg, a futásnaplóban a k62 `igehely_db = 8`. |
| 1i parok | OK | `adat/karoli_strong/parok_Bir.tsv` | Grep `^Bír \d+:\d+\t.*\talacsony\tS$` → 14 939. Ehhez jön a proveniencia- és a fejlécsor, így a fájl 14 941 sor (numstat +14941). A 2.1 táblázat 21 fejezeti linkszámának összege 14 939. Szúrópróba: `^Bír 10:` 365, `^Bír (9\|21):` 1882 (= 1317 + 565). |
| 1j szavak, állapotbontás | OK | `szavak_Bir.tsv` | hu `parositva` 11 904 és `betoldas` 2 625 (összesen 14 529). er `parositva` 13 932 és `forditatlan` 1 452 (összesen 15 384). A teljes `\talacsony\tS$` 29 913, a fájl 29 915 sor. `\t(fuggoben\|kezi\|magas)\t` → 1 találat, de az a `Bír 9:6 hu 19 „magas”` magyar szó, nem állapot. A fejezeti szószámok összege 29 913. Szúrópróba: `^Bír 17:` 632. |
| 1k TAHOT Bír = 15 384 | OK | `konkordancia/TAHOT_kivonat.tsv` | Grep `^Bír ` → 15 384, egyezik az er-sorok számával. |
| 1l régi arany 0 | OK | `Karoli_Strong_kivonat.tsv` | A normalizáló táblában `Jdg → Bír` (`Konyv_normalizalo_tabla.tsv:8`). Grep `^Jdg\.` → 0, Grep `^Judg\.\|Bír ` → 0. |
| 2a detektor és kézi táblák | OK | `f22/versmegfeleltetes.tsv`, `_kezi.tsv`, `versosszevonas.tsv` | Grep `(^\|\t)Bír` a három fájlban → 0. `git diff --numstat ced1bf8 672860b -- konkordancia f22/versmegfeleltetes*.tsv f22/versosszevonas.tsv` → üres. |
| 2b kulcsegyezés 618/618 | OK | Karoli és TAHOT | Túlcsorduló kulcsra (fejezetenként a vershossz fölött, 22+ fejezet, :0, 4+ jegyű vers) írt Grep-mintát mindkét fájlon futtattam: 0 találat. A 21 fejezetzáró vers (1:36 … 21:25) mind megvan a Károliban (Grep → 21). Az összeg 618, és a `minta_Bir` `eredeti_szo` oszlopában nincs 0, tehát minden Károli-kulcshoz van TAHOT-vers. Az er-összeg 15 384 = TAHOT, tehát gazdátlan TAHOT-token nincs. Grep `^Bír \d+:\d{4,}\t` → 0 (nincs +1000-es kulcs). A `hu 1` és az `er 1` sorok száma egyaránt 618. |
| 2c tartalmi egyezés | OK | 1:1, 5:1, 5:31, 21:25 | `python eszkozok/lekerdez.py karoli "Bír 5:1"` → „Énekelt pedig Debora és Bárák, az Abinoám fia azon a napon, mondván:”, a TAHOT szerint „she sang Deborah and Barak son of Abinoam on the day that saying”. 5:31: „…tündököljenek mint a kelő nap… negyven esztendeig”, TAHOT: „…going out of the sun in its strength… land forty year[s]”. 21:25: „nem volt király Izráelben… a mi jónak látszott az ő szemei előtt”, TAHOT: „no king in Israel each man the right in his own eyes he will do”. 1:1: „Józsué halála után… a Kananeusra”, TAHOT ugyanez. Proveniencia: `scope=range:Bír 5:31 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=0 \| ts=2026-10-09T06:32Z`. |
| 2d jóváhagyási napló | OK (a chat-idézet NEM ELLENŐRIZHETŐ) | `naplok/F22_versbeosztas_jovahagyas.md`, új Bír-sor | A `git diff` szerint a sor megvan. A 0dbc529 (06:19:19Z) megelőzi a bekuld commitot (06:19:32Z). A `tokenek.py:55` tuple-je `'Bír'`-rel bővült. A „mehet a birák” idézet nem ellenőrizhető. |
| 3 Strong a TAHOT-ból | OK (mintavétel) | `szavak_Bir.tsv:26–51, 5276–5288, 6263–6284, 29901–29915` | Az er-sorok és a TAHOT sorai (`TAHOT_kivonat.tsv:134426–134451, 137172–137184, 137638–137659, 149795–149809`) összevetve: 1:1 26/26, 5:1 13/13, 5:31 22/22, 21:25 15/15, összesen 76 token. A Strong és a sorrend is egyezik. Grep `^Bír…\ter\t…\tH\d{4}[A-Za-z]?\talacsony\tS$` → 15 384, tehát minden er-sor egyetlen H-Strongot visel. `python eszkozok/lekerdez.py scan H8252 --szakasz "Bír 5:31"` → `strong=H8252 \| n=1 \| ts=2026-10-09T06:35Z`, `scan H4428 --szakasz "Bír 21:25"` → `n=1`. |
| 4a datasetek.tsv | OK | `adat/datasetek.tsv:89–90, 92–93, 95–96, 98–99` | A `git diff` szerint a 4 × 2 sor csak Bír-bővítés: „Ez, Péld és Bír”, `parok_Bir.tsv`, „a Péld és a Bír”, és a parok-sorokban `naplok/F22_Bir_jelentes.md`. Más szöveg nem változott. Grep `^[^#\t][^\t]*(\t[^\t]*){6}$` → 106, `^#` → 3, az összes sor 109. A `^([^\t]*\t){7}` (8+ mező) → 0, a ≤ 6 mezős nem-komment sor → 0. |
| 4b SEMA 2.20 | OK | `adat/SEMA.md:936` | A `git diff` szerint csak ez változott: a `VERSBEOSZTAS_JOVAHAGYOTT` listába bekerült a „Bír”; a „nincs sora” felsorolásba „az Ezékielnek és a Bíráknak” (helyes, a detektorban 0 sora van); a csak-Sonnet és API-felsorolásba a Bír; bekerült a `parok_/szavak_Bir.tsv` és a jelentés. A `kezi` példák helyesen nem bővültek. |
| 4c BDB-mérés (Bír 77/2, 655/98, Eszt 148) | NEM ELLENŐRIZHETŐ | `jelentes.md:5, 104`, brief `:11` | A `python naplok/F22_konyvsorrend_meres.py` nincs a megengedett parancsok között. A szkript a tartományban nem változott (`git diff --stat` üres, utolsó commitja 9183608), és a kimenete a repóban nincs rögzítve. Ami a tárolt detektorral ellenőrizhető, az egyezik: „Dán (37 detektorsor)” = Grep → 37. Az Eszt, 2Sám, 1Sám, 1Kir, Neh és 2Kir detektorsora 0, a „tiszta jelöltek” állítás tehát helyes. |
| 5 kulcs/titok | OK | — | `git diff ced1bf8..672860b \| grep -ciE 'sk-ant\|PARDES_API_KEY\|api[_-]?key\|x-api-key\|Bearer '` → 0. `git log ced1bf8..672860b -p \| grep -ciE 'sk-ant\|PARDES_API_KEY'` → 0. |
| 6a fejléc, D25, v2.19 | OK | brief `:10, :15, :176, :184` | A `kovetkezo` a Bír-jelentést, a „tiszta versbeosztás”-t, a `naplok/ELLENOR_F22_Bir.md`-t, a DT70-et és a következő könyv döntését nevezi meg. Az `ir` elejére bekerültek a Bír-fájlok, köztük az `ELLENOR_F22_Bir.md`, az `atnezes`, a `minta` és a két jsonl. A D25 számai (6,86 / 4,39 / 0,0071 / 13/618 / végleg 0 / régi arany nincs) egyeznek az 1c–1l sorokkal. A v2.19 a v2.18 fölött áll. `allapot: megallt`. |
| 6b commit-tárgy | **ELTÉRÉS** (alacsony) | `672860b` | A tárgy „jelentés …, K9 és a brief fejléce”. A `git diff --stat 672860b~1 672860b` csak a briefet és a jelentést mutatja; a K9 (`datasetek.tsv`, `SEMA.md`) a `4a9b096`-ban van (a body ezt helyesen írja). A tétel-szintű commit-napló tehát félrevezető. |
| CI | OK (CI-jelentés nem érkezett, csak saját futás) | — | `python eszkozok/ellenorzes/futtat.py --valtozott <26 változott fájl> --diff-alap ced1bf8 --diff-fej 672860b`. Eredmény: E2–E16, E19, E20 és E26 0 találat. E25: 3 (`CLAUDE.md:33`, `MUNKAMENET.md:67, 181`). E27: 92. Ugyanez a 3 és 92 jön `--diff-alap ced1bf8 --diff-fej ced1bf8` mellett is, tehát repószintű, nem az ág okozza. E17 nem jelent meg. |
| K1 lefedettség | OK (részben) | `szavak_Bir.tsv` | Az er-oldal 15 384 = TAHOT. A `hu 1` és az `er 1` sorok száma 618/618. Azt, hogy a hu-oldal 14 529 = Károli-tokenszám, a minta `karoli_szo` oszlopának 618 tagú összegével nem ellenőriztem. |
| K2 / K7 `egyesit.py --ellenoriz` | NEM ELLENŐRIZHETŐ (mintán OK) | `jelentes.md:34` | Nincs a megengedett parancsok között; 76 tokenen 100% az egyezés (3. sor). |
| K3 prompt-hash | OK | `futasnaplo.tsv` | Mind a 74 sorban `84f12ca7aafb` (1b). |
| Ell.-lista 1: törölt / kiszűrt sorok | OK | — | `git diff --numstat`: brief −2 (a `kovetkezo` és az `ir` cseréje), SEMA −1, datasetek −8, tokenek.py −1. Mind szövegcsere, adatsor nem törlődött. Kiszűrt sor nincs: `kezi` 0, `fuggoben` 0, az átnézési fájl csak fejléc (`naplok/F22_Bir_atnezes.tsv`, +1 sor). |
| Ell.-lista 2: kulcstartomány | OK | — | 618/618 Károli-vers, 21/21 fejezet, 62/62 köteg. Az er-oldal 15 384 = TAHOT, és minden er-sor H-Strongot visel. |
| Ell.-lista 3: a nulla-diff hatóköre | OK | — | Üres diff (`ced1bf8..672860b`): `konkordancia/`, a detektor, a kézi megfeleltetés, a `versosszevonas`, valamint a `high/Bir.jsonl` és a `valaszok/sonnet/Bir.jsonl` egymáshoz képest. Nem vonatkozik a `tokenek.py`-ra (1 sor), a `datasetek.tsv`-re, a `SEMA.md`-re és a briefre. |
| Ell.-lista 4: E17 / DT3 sorszám-Δ az `origin/main`-hez | OK | — | `git diff --numstat origin/main..672860b -- adat/ konkordancia/ \| grep .tsv`: `datasetek.tsv` Δ 0 (8 csere). `parok_Bir.tsv` új, +14 940 a fejléc nélkül (1 proveniencia-komment és 14 939 adatsor). `szavak_Bir.tsv` új, +29 914 (1 komment és 29 913 adatsor). `parok_Peld.tsv` +10 762 és `szavak_Peld.tsv` +21 782: ezek az előző tétel táblái, amelyeket az `ELLENOR_F22_Peld.md` ellenőrzött. `konkordancia/` 0. A Bír bontási naplója a `jelentes.md` 1a (hu/er × állapot) és 2.1 (fejezetenként); Grep-pel egyezik (1i, 1j). A helyi `main` (ef8f7e5) régebbi; ehhez képest további, már merge-elt könyvek táblái is eltérnek. |
| Ell.-lista 5: a brief ⛔ pontjai | OK | brief `:67, :122` | ⛔ 1.: a végleges kapuhiba 0%, a C nem futott. ⛔ 2.: `allapot: megallt`, merge-commit nincs a tartományban, és a következő könyv a `kovetkezo` szerint a felhasználó döntése. |
| A1 memória vs. lekérdezés | OK (megjegyzéssel) | `jelentes.md:3, 22`; a táblák 1. sora | A számok szkriptkimenetként vannak jelölve, a proveniencia-sor `scope=manual … modell-kimenet, javaslat`. A „hosszú elbeszélő versei miatt” (`:22`) értelmező mondat, de adat támasztja alá: 15 384 / 618 ≈ 24,9 er-token versenként, a Péld-ben 9 703 / 914 ≈ 10,6. |
| A2 nyitott tételek | OK (részben NEM ELLENŐRIZHETŐ) | brief `:10` | A „#77 fejléce frissítendő” valóban nyitott: Grep `^kovetkezo:` az `F77_API_VAKPROBA_BRIEF.md:12`-ben még „Te: merge (közös PR …)”. Az N-F83a a `DONTESEK.md:160`-ban javasolt azonosító. A kézi átnézések és a PR állapota lekérdezéssel nem igazolható. |
| A3–A6 | n.é. | — | Nem tanulmány: párhuzam, PaRDeS-réteg és nevesített tanító nincs, az E12–E15 0 találat. |

Az ELTÉRÉS-ek súlyossági sorrendben:
1. (alacsony) 6b: a `672860b` tárgya K9-et állít, de a `datasetek.tsv`/`SEMA.md` módosítás a `4a9b096`-ban van. Adatot nem érint.

NEM ELLENŐRIZHETŐ maradt:
- a BDB-mérés számai (77/2, 655/98, Eszt 148);
- az `egyesit.py --ellenoriz` (K2/K7) teljes körű igazolása;
- a hu-oldal tokenszámának összevetése a mintával;
- a chat-idézet („mehet a birák”) és a PR-állapot.
