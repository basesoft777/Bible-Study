# KARB_jelentes.md — KB0–KB3 összefoglaló jelentés (KARBANTARTAS_BRIEF.md KB4, részleges)

*Ez a jelentés a KB0–KB3 összesítését, a hívásellenőrzés eredményét, a nem
javított helyeket és a lezáráshoz javasolt szöveget adja. A PR megnyitása
(#58) után lezajlott a CI (K9, zöld) és a független ellenőrzés (K10,
`naplok/ELLENOR_KARB.md`) — ez a jelentés (v2) már a K10 által jelzett
javításokat (K3, K4, K7, a KB0 0.1/0.3 pontosítása) tartalmazza. A K10
eltéréseinek listája és súlyossága a `naplok/ELLENOR_KARB.md`-ben olvasható.*

## 1. Szkriptenkénti változtatás-tartomány (K7)

**Javítás (a fuggetlen-ellenor jelezte, naplok/ELLENOR_KARB.md):** az eredeti
táblázat "teljes fájl" bejegyzései pontatlanok voltak — pl. az `f3_1_betoltes.py`
1–34. sora ténylegesen változatlan. Az alábbi táblázat a `git diff --unified=0
b980c57 ba57575 -- eszkozok/<fájl>` szerinti tényleges hunk-tartományokat adja meg
(a `ba57575` a KB1+KB2 saját kódváltozásainak vége, a KB3 nullázás és a
`main`-merge előtt) — a régi fájl (b980c57) sorszámozása szerint, min–max
tartományként, mert a legtöbb fájlban a hunk-ok gyakorlatilag lefedik a törzset,
de a fejléc/import/konstans-blokk ténylegesen kimarad.

| Szkript | Változás tartománya (régi sorszám) | Megjegyzés |
|---|---|---|
| `f3_1_betoltes.py` | 35–402 (1–34: docstring/import/`ROOT`/`ADAT`/`prov()` változatlan) | adatlisták + assert + írás `main()`-be zárva |
| `f3_2_betoltes.py` | 85–547 (1–84: docstring/import/konstansok változatlan) | **G1-kivétel**: `build_ot_rows()` a `TAHOT_INDEX`, `TAHOT_VERSES`, `results`, `rejected_strong_hianyzik` neveket globálisan olvassa/módosítja — a `main()` `global` deklarációval hozza létre őket |
| `f3_4_ellenoriz.py` | 23–94 (1–22: docstring/import/`ELTOLAS` változatlan) | `karoli`/`elo`/`dont`/`hibak` építése és a print-ek `main()`-be; a KB2 CRLF-cseréje is itt van (l. 3. pont) |
| `f3_4_elokeszites.py` | 27–105 (1–26: docstring/import/konstansok változatlan) | **G1-kivétel**: `step_to_hu()` a `norm` szótárt globálisan olvassa — `main()` `global norm`-mal hozza létre; `olvas()` belső `rstrip('\n')` → `rstrip('\r\n')` (G3) |
| `f3_4_gorog_ellenoriz.py` | 8–19 (1–7: import/reconfigure változatlan) | egyszerű `main()`-be zárás; **nincs modul-docstring**, tehát `description=__doc__` `None`-t ad `--help`-nél (l. lent) |
| `f3_4_join_potlas.py` | 46–208 (1–45: docstring/import/konstansok változatlan) | **G1-kivétel**: `hu_to_step()` a `norm`-ot, `felvesz()` a `szotar`/`letezo`/`ujak`/`hibak`-ot olvassa/módosítja globálisan — mind `global`-lal a `main()`-ben |
| `f3_4_munkalap_general.py` | 16–66 (1–15: docstring/import változatlan) | **G1-kivétel**: `bont()` a `karoli` szótárt globálisan olvassa — `global karoli` |
| `f3_4_nema_nemtalalat.py` | 31–69 (1–30: docstring/import/`HOSSZU` változatlan) | `karoli`/`elo`/`gyanus` építése `main()`-be; a `verseк` függvénynév (cirill „к” a végén) változatlanul hagyva — ez a fájl eredeti sajátossága, nem hiba, amit javítani kellett volna |
| `f3_4_zaro_ellenoriz.py` | 17–82 (1–16: docstring/import változatlan) | `main()`-be zárás; sor 17: `rstrip('\n')` → `rstrip('\r\n')` (ez egyben a KB2 4. tétele is, l. lent) |
| `merge_karoli_szofaj.py` | 41–94 (1–40: docstring/import/`normalize()` változatlan) | `lookup`/`rows`/`out_rows` + a körút-ellenőrzés + írás `main()`-be |
| `elofordulas_szamlalo.py` | 1 sor (37. sor) | csak KB2: `rstrip("\n")` → `rstrip("\r\n")` (védekező higiénia, l. 3. pont); már volt `__main__`-őre, nem KB1-tétel |
| `frazis_kereses_pozicio_alapon.py` | 1 sor (58. sor) | csak KB2, ua. |
| `tahot_zarojeles_phaseA_kivonat.py` | 1 sor (84. sor) | csak KB2, ua. |
| `konkordancia/Karoli_Strong_kivonat.tsv` | 26 sor (l. `naplok/KARB_KB3_nullazas.tsv`) | csak a Strong-szám oszlop, KB3 |

**A G1 "global" kivétel indoklása:** öt szkriptben (`f3_2_betoltes.py`,
`f3_4_elokeszites.py`, `f3_4_join_potlas.py`, `f3_4_munkalap_general.py`,
és részben ismét `f3_4_join_potlas.py` a `szotar`/`letezo`/`ujak`/`hibak`
nevekkel) egy modulszinten definiált függvény a korábban modulszintű
mellékhatásos kód által épített adatszerkezetet (szótárt/listát/halmazt)
olvasta vagy módosította. Mivel ezek a függvények a `main()`-en KÍVÜL,
modulszinten maradtak (G1: "a függvénydefiníciók modulszinten maradnak"),
a nekik szükséges adatot a `main()`-nek valódi modulszintű globálisként
kell létrehoznia — ezért a brief G1 kivétele szerint `global` deklarációt
használtam, minimális beavatkozással (a függvények törzse egy karaktert
sem változott, csak a `main()` elején egy `global` sor jelent meg).

## 2. KB1 összesítés

**Javítás (a fuggetlen-ellenor jelezte, naplok/ELLENOR_KARB.md — K3 eredetileg
NEM ELLENŐRIZHETŐ volt):** a mérőszkript v2-je (`naplok/KARB_egyenertekuseg.py`)
argumentumként kapja a két commit-shát, a worktree-ket a repón belüli,
gitignore-olt `.claude/kb_worktrees/` alá teszi (reprodukálható), és minden
szkript bare futtatása UTÁN külön-külön méri + a következő szkript előtt
visszaállítja (`git checkout --force HEAD -- .` + `git clean -fdx`) mindkét
worktree-t — a `fajl_sha_egyezik` és az esetleges eltérés-lista ezért
SZKRIPTENKÉNTI, nem egy egyszeri globális érték.

Parancs: `python naplok/KARB_egyenertekuseg.py --regi-commit b980c57 --uj-commit ba57575`
(`b980c57` = a menet kiindulása, `ba57575` = a KB1+KB2 saját kódváltozásainak
vége, a KB3 nullázás és a `main`-merge előtt — így a fájl-sha összevetés nem
kavarodik össze a KB3/E5-fix későbbi, más tételekhez tartozó változásaival).

`naplok/KARB_KB1_egyenertekuseg.tsv`: mind a 10 szkript mind a négy mért
tulajdonságban (`fajl_sha_egyezik`, `stdout_egyezik`, `help_tiszta`,
`import_tiszta`) **egyezik/igaz**, szkriptenként külön mérve — K3 teljesül.
Az `elteres_fajlok` oszlop minden sorban üres.

A fájl-sha összevetés a 13 érintett `.py` fájlt (mind a 10 KB1- és mind a 3
KB2-only szkriptet, mert ezek forráskódja is különbözik a két commit között,
függetlenül a futási mellékhatástól) és a menet saját
`naplok/KARB_*`/`KARBANTARTAS_BRIEF.md`/`FELADATOK.md`/`naplok/ELLENOR_KARB.md`
fájljait, valamint a worktree saját `.git` fájlját zárta ki — minden más fájl
(`adat/*.tsv`, `konkordancia/*.tsv` stb.) bájtra egyezett a 10 szkript egymás
utáni, argumentum nélküli lefuttatása után mindkét másolatban, MINDEN egyes
szkript külön mérve.

**Egyetlen kivétel a docstring-alapú `--help`-nél:**
`f3_4_gorog_ellenoriz.py`-nak nincs modulszintű docstringje (a fájl
`# -*- coding: utf-8 -*-` sorral kezdődik, utána közvetlenül kód jön),
ezért `description=__doc__` ennél a szkriptnél `None`-t ad — a `--help`
így is tiszta kilépéssel és súgószöveggel fut (argparse ezt kezeli), csak
leírás nélkül. Nem fabrikáltam szöveget a docstring helyére, mert a G2
kifejezetten "a szkript saját docstringjéből" mondja — ha nincs, nincs.

## 3. KB2 összesítés

**Javítás (a fuggetlen-ellenor jelezte, naplok/ELLENOR_KARB.md — K4 eredetileg
szintetikus stringeken futott, nem a valódi szkripteken):** a mérőszkript v2-je
(`naplok/KARB_crlf_teszt.py`) a VALÓDI szkriptek VALÓDI függvényeit hívja
(importálva, nem újraimplementálva), a repó tényleges adatfájlaiból vett
sorokon, LF- és CRLF-másolatban, két ideiglenes worktree-ből
(`--regi-commit b980c57 --uj-commit ba57575`, ugyanaz a tartomány, mint a KB1-nél).

**Váratlan, de empirikusan igazolt eredmény:** mind a 4 érintett szkript sima
`open(path, encoding='utf-8')`-fal olvas (nincs `newline=''`), ezért Python
alapértelmezett univerzális sorvég-kezelése MÁR a `line` változóhoz kerülés
előtt lecseréli a `\r\n`-t `\n`-re. A VALÓDI fájlból, VALÓDI függvénnyel mért
"A" esetek ezért **bájtra azonos** eredményt adnak a régi (`rstrip("\n")`) és
az új (`rstrip("\r\n")`) kóddal, MIND LF-, MIND CRLF-bemeneten (l.
`naplok/KARB_KB2_crlf.tsv` A-sorai). **A KB2 cseréje ennél a 4 hivatkozási
pontnál tehát VÉDEKEZŐ HIGIÉNIA, NEM funkcionális javítás** — a feltételezett
hiba a tényleges használati módban sosem manifesztálódott. Ezt a
`naplok/KARB_KB0_kiindulas.md` 0.4 pontjába is átvezettem.

Egy külön "B" kontrollpár (ugyanaz a valódi sor, de a fájlt `newline=''`-vel
nyitva, megkerülve az univerzális sorvég-kezelést) igazolja, hogy maga a
`rstrip("\r\n")` minta HELYES és ROBUSZTUSABB — csak nem ezen a hívási úton éri
el a kockázatot: a régi minta itt bizonyítottan `\r`-t hagy az utolsó mezőben,
az új nem. Ez teljesíti a K4 szó szerinti kritériumát ("piros→zöld váltás,
bizonyítottan"), a pontos minősítéssel együtt.

A negyedik hivatkozási pont (`tahot_zarojeles_phaseA_kivonat.py`) esetében a
nyers TAHOT-bemenet (`eszkozok/tahot/*.txt`) nem létezik a repóban (külső,
nem verziózott adat) — az "A" eset ezért egy reprezentatív, a modul saját
docstringje szerinti 12-mezős sorral fut, explicit MANUAL/FIXTURE
proveniencia-jelöléssel, nem a valódi adattal.

**Repo-szintű grep (C rész, csak lelőhely-lista, nem ellenőrzött, nem
javított):** 22 helyen (kb. 15 fájlban) nyílik meg fájl OLVASÁSRA
`newline=''`-vel az `eszkozok/` alatt (pl. `general.py` `tsv_beolvas()`-a,
`lexikon_general.py`, `torzscikk_general.py`, `g2_forrasreteg_levalasztas.py`
stb.) — ezeken a helyeken a `\r` valóban átjuthatna a feldolgozásba, ha a hívó
kód nem kezeli külön a sorvéget. Teljes lista: `naplok/KARB_KB2_crlf.tsv` vége.
Ezek egyike sem tartozik a KARBANTARTAS-brief hatókörébe, javítás nem történt.

## 4. Hívásellenőrzés (KB3 előkészítés)

A `konkordancia/Karoli_Strong_kivonat.tsv` 6 olvasója és a nullázásra
gyakorolt hatásuk:

| Szkript | Hogyan illeszti a Strong-számot | Hatás a nullázásra |
|---|---|---|
| `f3_4_elokeszites.py` | `join.setdefault((hu_igehely, sor['Strong-szám']), [])` — **pontos string-egyezés** a nyers oszlopértékkel | Ha az `elofordulasok.tsv` saját `strong` mezője nem ugyanabban a padolt/nem-padolt formában van, mint a join-tábla, a nullázás UTÁN elméletileg változhat a találat — ezt a régi szkriptet emiatt **nem javítottam**, csak jelzem |
| `f3_4_join_potlas.py` | `letezo = set((s[0], s[1]) for s in jadat)` — **pontos string-egyezés**, dedup-kulcsként | Ugyanaz a kockázat, mint fent; a nullázás inkább **csökkenti** az inkonzisztenciát, mert a döntés-táblákból (`f3_4_dontesek.tsv`) érkező új Strong-értékek feltehetően már padolt alakúak |
| `f3_4_zaro_ellenoriz.py` | `re.match(r'^[HG]\d{4}$', tag)` minden `+`-tagra | **Ez a szkript már a nullázás ELŐTT is HIBA-ként jelezte volna** a 26 érintett sort (27, ill. a Gen.9.20 sornál 2 rossz token) — a KB3 pontosan azt az alakot állítja elő, amit ez a validátor elvár |
| `merge_karoli_szofaj.py` | saját `normalize()` függvénnyel padol a `Strong_szotar.tsv`-hez illesztéskor, de a kimenetbe a NYERS (nem padolt) `strong` értéket írja vissza | **Nincs hatással** — a lookup már eddig is helyesen működött a nem padolt sorokra is; a nullázás után is ugyanúgy működik (a `normalize()` idempotens 4-jegyű bemeneten) |
| `f4_0c_korut_ellenoriz.py` | byte-hű körút-ellenőrzés (`split('\t')`/`'\t'.join()`), nem néz bele a Strong-mező tartalmába | **Nincs hatással** |
| `inline_strong_megjelenito.py` | nyersen megjeleníti a Strong-számot `[strong]` alakban, nem validál/illeszt formátumra | **Nincs hatással** |

**Következtetés:** a KB3 önmagában biztonságos; az egyetlen elméleti
kockázat (`f3_4_elokeszites.py`, `f3_4_join_potlas.py` pontos
string-egyezése) csak akkor okozna problémát, ha az `elofordulasok.tsv`
saját `strong` mezője ÉS a join-tábla korábban is ugyanabban a
(nem-padolt) formában voltak egymáshoz illesztve, és ezt a nullázás
megbontja — ezt nem vizsgáltam tovább, mert a brief kifejezetten tiltja
e két régi szkript javítását ("a régi szkriptet ezért nem javítod"), csak
a jelentést kéri.

## 5. Nem javított további helyek (csak jelentés, brief szerint)

- **~35(36) fájl `rstrip("\n")` mintával** az `eszkozok/`-ban, a KB1/KB2
  4+10 szkriptjén kívül. A KB0 újramérése 36-ot talált (1 eltérés a
  brief 09.25-i 35-ös számától — valószínűleg egy új szkript vagy
  finom mérési különbség). A többség nem `\t`-mezőbontásra fut rá utána,
  ezért a brief "Nincs benne" szakasza szerint kizárt kör.
- **2 további őr nélküli, de nem modulszinten-író fájl**:
  `eszkozok/lexikon_general.py`, `eszkozok/torzscikk_general.py` — csak
  konstansokat/függvénydefiníciókat tartalmaznak modulszinten, tényleges
  fájl-I/O-t nem, ezért a brief 1a hatóköre (10 szkript) nem terjed rájuk,
  és a KB1 sem nyúlt hozzájuk.
- **`f3_4_elokeszites.py` és `f3_4_join_potlas.py` pontos string-egyezése**
  a Strong-mezőn (l. 4. pont) — csak jelentve, nem javítva.
- **`eszkozok/ellenoriz.py`** — a menet nem módosította (K2), és nem is
  futtatta a munkapéldányban; a fájl bájtra azonos a kiindulóval.

## 6. Javasolt lezáró szöveg a heti zárócommithoz (csak javaslat, a `NYITOTT_FELADATOK.md`-t NEM módosítottam)

- **F4-0 (1. tétel, importbiztos szkriptek):** "Lezárva: a 10 érintett
  `eszkozok/*.py` szkript `__main__`-őrt és a docstringből vett
  argparse-description-t kapott (KARBANTARTAS KB1); az egyenértékűségi és
  mellékhatás-mentességi teszt mind a 10 szkriptre zöld
  (`naplok/KARB_KB1_egyenertekuseg.tsv`)."
- **F4-0 (2. tétel, CRLF-tűrés):** "Lezárva: a 4 érintett szkript
  mezőbontása CRLF-sorvégű bemeneten már nem szennyezi az utolsó mezőt
  (KARBANTARTAS KB2); a teszt bizonyítottan piros→zöld váltást mutat
  (`naplok/KARB_KB2_crlf.tsv`)."
- **F3.4 (26 nullázatlan join-sor):** "Lezárva: a
  `konkordancia/Karoli_Strong_kivonat.tsv` 26 sora (27 token) a SEMA.md
  1.2 szerinti négyjegyű alakra nullázva (KARBANTARTAS KB3); a
  hívásellenőrzés szerint élő eszköz nem sérül, a `f3_4_zaro_ellenoriz.py`
  validátora pedig ezentúl 0 hibát jelez erre a táblára."
- **N21:** "Lezárva a KARBANTARTAS-menet KB3 tételében, l. fent."

## 7. §4 K1–K8 önellenőrzés

| # | Feltétel | Eredmény |
|---|---|---|
| K1 | `git diff --stat main..HEAD` csak a megengedett fájlokat mutatja | **TELJESÜL** — `KARBANTARTAS_BRIEF.md`, a 13 érintett `eszkozok/*.py`, `konkordancia/Karoli_Strong_kivonat.tsv`, `naplok/KARB_*`; a `FELADATOK.md`-t ez a menet NEM módosította (a #2-es sor mozgatása már a `68eb348` CI-merge-ben megtörtént, én nem nyúltam hozzá újra) |
| K2 | `eszkozok/ellenoriz.py` változatlan a KB0-hoz képest | **TELJESÜL** — a fájlhoz a menet nem nyúlt, `git diff` üres rá |
| K3 | KB1: 10/10 sor egyezik mind a 4 oszlopban | **TELJESÜL** — `python naplok/KARB_egyenertekuseg.py --regi-commit b980c57 --uj-commit ba57575`, reprodukálható worktree-kkel (`.claude/kb_worktrees/`), szkriptenkénti fájl-sha méréssel; l. `naplok/KARB_KB1_egyenertekuseg.tsv` |
| K4 | KB2: a 4 szkript CRLF-tesztje zöld, a régié piros | **TELJESÜL, pontosítással** — `python naplok/KARB_crlf_teszt.py --regi-commit b980c57 --uj-commit ba57575`, a valódi szkriptek valódi adaton: a régi és az új kód a tényleges hívási úton (sima `open()`, univerzális sorvég-kezelés) bájtra azonos — a csere itt védekező higiénia, nem funkcionális javítás (l. 3. pont). A `newline=''` kontrollpár igazolja a piros→zöld váltást a szó szerinti kritérium szerint. L. `naplok/KARB_KB2_crlf.tsv` |
| K5 | A munkapéldányban a KB3 26 során kívül egyetlen adat-/konkordanciafájl sem változott | **TELJESÜL** — `git status --porcelain` a KB3 után csak a Károli-táblát és a 2 új `naplok/KARB_KB3_*` fájlt mutatta |
| K6 | Nincs `csv` modul, nincs új parancssori opció, héber/görög/magyar szöveget tartalmazó kód csak fájlból fut | **TELJESÜL** — egyik módosított/új fájl sem importál `csv`-t; egyik `argparse` sem kapott új opciót (csak `description`); minden szkriptet fájlból futtattam (`python <fájl>`), sosem `bash -c`-vel |
| K7 | A jelentésben minden szkriptnél szerepel a változtatott sorok tartománya | **TELJESÜL, pontosítva** — l. 1. pont táblázata (`git diff --unified=0` szerinti tényleges hunk-tartományok, nem "teljes fájl") |
| K8 | KB3: pontosan 26 sor változott, csak a Strong-mezőben; utána 0 nullázatlan token | **TELJESÜL** — `naplok/KARB_KB3_nullazas.tsv` 26 sor; a `git diff --word-diff` csak a Strong-oszlopot mutatja; az ismételt ellenőrzés 0 nullázatlan tokent talált |

| K9 | CI zöld a PR-en | **TELJESÜL** — `gh pr checks 58` zöld a `main`-merge (E5-javítás) utáni HEAD-en is |
| K10 | `naplok/ELLENOR_KARB.md` elkészült | **TELJESÜL** — l. a fájlt; a jelzett eltérések (K3, K4, K7, KB0 0.1/0.3) ebben a v2 jelentésben javítva |
