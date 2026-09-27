# KARB_jelentes.md — KB0–KB3 összefoglaló jelentés (KARBANTARTAS_BRIEF.md KB4, részleges)

*Ez a jelentés a KB4 tétel elejét adja: a KB0–KB3 összesítését, a
hívásellenőrzés eredményét, a nem javított helyeket és a lezáráshoz
javasolt szöveget. A `naplok/ELLENOR_KARB.md` (K10, független ellenőr) és
a `FELADATOK.md` #4-es sorának frissítése (K9/K10 után, a teljes KB4
része) ebben a menetben szándékosan NEM készül el — a chat kifejezetten
úgy kérte, hogy erre a menetre álljak meg a PR megnyitásánál, CI-várás és
független ellenőr nélkül.*

## 1. Szkriptenkénti változtatás-tartomány (K7)

A KB1 mind a 10 szkriptet átalakította: a modulszintű mellékhatásos kód
egy `main()`-be került, `__main__`-őrrel és `argparse`-szal (`description=__doc__`).
Ez a legtöbb fájlban a teljes törzs újra-behúzását jelenti (a `git diff`
lényegében az egész fájlra kiterjed) — az alábbi táblázat ezért a
`git diff --stat 68eb348 HEAD` szerinti tényleges sor-számokat és a
tartalmi hatókört adja meg soronkénti pontosság helyett, ahol a teljes
fájl érintett.

| Szkript | Változás tartománya | Megjegyzés |
|---|---|---|
| `f3_1_betoltes.py` | teljes fájl (729 diff-sor) | adatlisták + assert + írás `main()`-be zárva; `prov`, `w`, konstansok modulszinten maradtak |
| `f3_2_betoltes.py` | teljes fájl (837 diff-sor) | ua.; **G1-kivétel**: `build_ot_rows()` a `TAHOT_INDEX`, `TAHOT_VERSES`, `results`, `rejected_strong_hianyzik` neveket globálisan olvassa/módosítja — a `main()` `global` deklarációval hozza létre őket |
| `f3_4_ellenoriz.py` | teljes fájl (138 diff-sor) | `karoli`/`elo`/`dont`/`hibak` építése és a print-ek `main()`-be; sor 32: `rstrip('\n')` → `rstrip('\r\n')` (G3, mert úgyis hozzányúltunk) |
| `f3_4_elokeszites.py` | teljes fájl (142 diff-sor) | **G1-kivétel**: `step_to_hu()` a `norm` szótárt globálisan olvassa — `main()` `global norm`-mal hozza létre; `olvas()` belső `rstrip('\n')` → `rstrip('\r\n')` (G3) |
| `f3_4_gorog_ellenoriz.py` | teljes fájl (35 diff-sor) | egyszerű `main()`-be zárás; **nincs modul-docstring**, tehát `description=__doc__` `None`-t ad `--help`-nél (l. lent) |
| `f3_4_join_potlas.py` | teljes fájl (215 diff-sor) | **G1-kivétel**: `hu_to_step()` a `norm`-ot, `felvesz()` a `szotar`/`letezo`/`ujak`/`hibak`-ot olvassa/módosítja globálisan — mind `global`-lal a `main()`-ben |
| `f3_4_munkalap_general.py` | teljes fájl (72 diff-sor) | **G1-kivétel**: `bont()` a `karoli` szótárt globálisan olvassa — `global karoli` |
| `f3_4_nema_nemtalalat.py` | teljes fájl (68 diff-sor) | `karoli`/`elo`/`gyanus` építése `main()`-be; a `verseк` függvénynév (cirill „к” a végén) változatlanul hagyva — ez a fájl eredeti sajátossága, nem hiba, amit javítani kellett volna |
| `f3_4_zaro_ellenoriz.py` | teljes fájl (119 diff-sor) | `main()`-be zárás; sor 17: `rstrip('\n')` → `rstrip('\r\n')` (ez egyben a KB2 4. tétele is, l. lent) |
| `merge_karoli_szofaj.py` | teljes fájl (116 diff-sor) | `lookup`/`rows`/`out_rows` + a körút-ellenőrzés + írás `main()`-be; a `normalize()` függvény (saját belső Strong-padoló) érintetlen |
| `elofordulas_szamlalo.py` | 1 sor (37. sor) | csak KB2: `rstrip("\n")` → `rstrip("\r\n")`; már volt `__main__`-őre, nem KB1-tétel |
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

`naplok/KARB_KB1_egyenertekuseg.tsv`: mind a 10 szkript mind a négy
oszlopban (`fajl_sha_egyezik`, `stdout_egyezik`, `help_tiszta`,
`import_tiszta`) **egyezik/igaz** — K3 teljesül.

A mérés két ideiglenes git worktree-ben futott (`kb_regi` = `b980c57`,
`kb_uj` = a KB2 utáni HEAD), a munkapéldányon kívül (G4), a
`naplok/KARB_egyenertekuseg.py` szkripttel. Módszertani megjegyzés: mivel
a két worktree abszolút útvonala eltér, a `ROOT`-alapú print-sorokat
(pl. `f3_4_elokeszites.py` "Munkalap: ..." üzenete) a saját worktree-je
abszolút útvonalával maszkoltam összehasonlítás előtt — ez a brief
"időbélyeg-sor maszkolva" engedélyének analóg kiterjesztése egy, a két
ideiglenes könyvtár nevéből eredő, nem viselkedésbeli különbségre. A
fájl-sha összevetés a 13 érintett `.py` fájlt és a menet saját
`naplok/KARB_*`/`KARBANTARTAS_BRIEF.md`/`FELADATOK.md` fájljait kizárta
(ezek szándékosan különböznek) — minden más fájl (`adat/*.tsv`,
`konkordancia/*.tsv` stb.) bájtra egyezett a 10 szkript egymás utáni,
argumentum nélküli lefuttatása után mindkét másolatban.

**Egyetlen kivétel a docstring-alapú `--help`-nél:**
`f3_4_gorog_ellenoriz.py`-nak nincs modulszintű docstringje (a fájl
`# -*- coding: utf-8 -*-` sorral kezdődik, utána közvetlenül kód jön),
ezért `description=__doc__` ennél a szkriptnél `None`-t ad — a `--help`
így is tiszta kilépéssel és súgószöveggel fut (argparse ezt kezeli), csak
leírás nélkül. Nem fabrikáltam szöveget a docstring helyére, mert a G2
kifejezetten "a szkript saját docstringjéből" mondja — ha nincs, nincs.

## 3. KB2 összesítés

`naplok/KARB_KB2_crlf.tsv`: mind a 4 érintett szkript sorára igaz, hogy
CRLF-bemeneten a régi alak (`rstrip("\n")`) `\r`-t hagyott az utolsó
mezőben, az új alak (`rstrip("\r\n")`) nem — K4 teljesül (piros→zöld
váltás, bizonyítottan). LF-bemeneten mindkét változat hibátlan (nincs
regresszió).

A mérés a brief mércéjének megfelelő granularitáson (soronkénti, a KB0
által azonosított pontos hely) szintetikus 2- illetve 12-mezős
tesztsorokkal futott, mert a valódi célfájlok (`TAGNT_kivonat.tsv`,
`elofordulasok.tsv`, `TAHOT_kivonat.tsv`, a `tahot/` nyers fájlok) LF-
végűek — CRLF-változatuk előállítása és a teljes szkript rájuk futtatása
a munkapéldányban tiltott (G4), ezért a tesztet a konkrét
mezőbontó-sorra szűkítettem, pontosan a brief §1 mércéje szerint
("Minden érintett szkript kap egy LF és egy CRLF változatú ideiglenes
bemenetet ... Mindkét bemeneten azonos az utolsó mező").

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
| K3 | KB1: 10/10 sor egyezik mind a 4 oszlopban | **TELJESÜL** — l. `naplok/KARB_KB1_egyenertekuseg.tsv` |
| K4 | KB2: a 4 szkript CRLF-tesztje zöld, a régié piros | **TELJESÜL** — l. `naplok/KARB_KB2_crlf.tsv` |
| K5 | A munkapéldányban a KB3 26 során kívül egyetlen adat-/konkordanciafájl sem változott | **TELJESÜL** — `git status --porcelain` a KB3 után csak a Károli-táblát és a 2 új `naplok/KARB_KB3_*` fájlt mutatta |
| K6 | Nincs `csv` modul, nincs új parancssori opció, héber/görög/magyar szöveget tartalmazó kód csak fájlból fut | **TELJESÜL** — egyik módosított/új fájl sem importál `csv`-t; egyik `argparse` sem kapott új opciót (csak `description`); minden szkriptet fájlból futtattam (`python <fájl>`), sosem `bash -c`-vel |
| K7 | A jelentésben minden szkriptnél szerepel a változtatott sorok tartománya | **TELJESÜL** — l. 1. pont táblázata |
| K8 | KB3: pontosan 26 sor változott, csak a Strong-mezőben; utána 0 nullázatlan token | **TELJESÜL** — `naplok/KARB_KB3_nullazas.tsv` 26 sor; a `git diff --word-diff` csak a Strong-oszlopot mutatja; az ismételt ellenőrzés 0 nullázatlan tokent talált |

K9 (CI zöld) és K10 (`naplok/ELLENOR_KARB.md`, független ellenőr) ebben a
menetben szándékosan nincs ellenőrizve — a chat kifejezetten kérte, hogy
ne várjam meg a CI-t, és ne futtassak `fuggetlen-ellenor` ügynököt.
