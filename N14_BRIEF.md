# N14 — A HAMART-001 betöltése az `adat/`-ba

*Készítette: chat-menet (Opus 5), 2026-09-21, **v2** — az 1. menet lefutott (`ac3eef4`, `d7a58a6`); a független ellenőrzés két elemzési hibát és egy formai eltérést talált → N14.1a a 2. menet elején. A §2 G1–G6 és a §5 jóváhagyva (2026-09-21).*
*Kiindulási állapot: `main` = `origin/main` = `32d7952`.*
*Két menet, Sonnet, köztük kötelező emberi megállási pont (⛔, az A4/B5 mintájára).*

---

## 0. Kiindulás — mérve, `32d7952`

| Mit | Mért érték |
|---|---|
| study | `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` v1 (2026.09.11, sablon v14), 1. pont: **46 táblasor** (A: 20, B: 18, C: 8) |
| napló | `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md`; §6: 46 beépített sor; §7: 15 tételes lekérdezés-lista (TAHOT, TAGNT, LXX, TSK, Károli-KH, BDB, Károli 1908) |
| `adat/` | HAMART-001-nek 0 sora (`motivumok`, `jeloltek`, `elofordulasok`, `auditok`) |
| motívumnapló | kézi HAMART-001-szöveg három helyen: Tematikus áttekintés (119. sor), ⭐ bekezdés (183.), Kulcsszó-index (284.) — mind generált blokkon **kívül** |
| index | K8-figyelmeztetés a generált blokkban (25. sor) + kézi szakasz „A táblába még nem betöltött, lezárt tanulmány" (43. sortól) |
| `general.py` | a K9' kettéosztás (`K9_KULON_BLOKK_ID`) önműködően megszűnik, ha a HAMART-001-nek lesz `jeloltek`-sora — kódmódosítás nem kell |
| `ellenoriz.py` | 6 · 0 · 3 · 1, kód 0; `RETROAKTIV_IDK` = 7 ID |
| `motivumok/` forrásréteg | 7 fájl, HAMART-001.md nincs |

---

## 1. A feladat

A HAMART-001 az F3 betöltési körén kívül maradt (N14). A betöltés **retroaktív**, pontosan úgy, mint az F3.1/F3.2 hét motívuma: a study 1. pontjának táblázatából, `scope=manual` provenienciával. Két eltérés az F3-hoz képest: a sorok a `betolt.py beepit`-en át kerülnek az `elofordulasok`-ba (az F8 átjárójának első éles használata), és a napló kézi szövegei a F4.4 mintájára a forrásrétegbe költöznek.

---

## 2. G-döntések — jóváhagyva (2026-09-21)

**G1 — a §3/8 kezelése: a HAMART-001 a retroaktív listára kerül (a (b) út), nem valódi lekérdezésekkel (az (a) út).**
*Ez eltér a chatben korábban javasolt (a) úttól.* A study megírásakor (2026.09.11) a `lekerdez.py` még nem létezett (F2: 2026.09.14), tehát nincs a study-t megalapozó proveniencia-sor. A mai újrafuttatás pontosan az a „utólag gyártott nyom" volna, amit az N12 D3 a 7 motívumnál elvetett. A HAMART-001 ugyanabba az osztályba tartozik. A napló §7-je viszont tételesen dokumentálja, hogy mind az 5 `mindig` dataset lekérdezése megtörtént — a 8/c „ember ellenőrizze" mutatója ide vezet, és itt meg is találja a választ.
→ `RETROAKTIV_IDK` 7 → 8 ID; a SEMA §3/8 szövegében „a 7 retroaktív" → „a 8 retroaktív".

**G2 — `gerinc_elem`: soronként a study saját horgony-megjelölése, rögzített sorrendű szabállyal.**
1. „tematikus, nem lexikai" jelölésű sor → `tematikus:<genezisi horgony>`, a study saját szövege szerint (a MENNY-001 `formula:`/`idézet:`/`referencia:` precedense): Ézs 24:5-6 → `tematikus:1Móz 3:17` („azonos a 1Móz 3:17-tel"); Mt 15:19, Mk 7:21-23 → `tematikus:1Móz 6:5` („a 1Móz 6:5 szív-diagnózisának"); 2Pét 3:6-7 → `tematikus:1Móz 6:13` („a 1Móz 6:13 ítélet-logikájának"). **Hós 4:1-3 → `tematikus:1Móz 3:17`** — ez az egy *következtetés*: a study nem nevez meg genezisi párt, csak a „lakosok bűne → a föld sorvadása" okozati kapcsolatot.
2. A Strong-oszlopban H4390 + H2555, és a BDB-entry-id H2555 → `málé+chámász` (a SEMA 2.2 saját példája); H8085 + H2555 → `sámá+chámász`.
3. A–B tábla, egyéb → a sor **BDB-entry-id** oszlopa (a study szerzőjének saját horgony-választása); a `H6975 / H1863` alak `H6975+H1863`-ra normalizálva.
4. C tábla (nincs BDB-oszlop) → a Strong-oszlop első olyan eleme, amely a gerincben van (G1944, G2671, G5356, G1311, G5351).

A `strong` mező: a `gerinc_elem`, ha az egyetlen Strong; kollokációnál H2555; `H6975+H1863`-nál H6975; tematikus sornál üres.
Gerincen kívüli horgony három sorban marad, a study szándéka szerint: 1Móz 3:18 (H6975+H1863, tövis/bogáncs), 6:5 (H7451), 8:21 (H7043, a *kalal* ≠ *arar* lelet). A zárójelentés ezeket név szerint listázza — jelzés, nem hiba (SEMA 2.2.1).

**G3 — sor-bontás:** a study `,` és `/` mentén összevont sorai külön `elofordulasok`-sorok (`1Móz 3:19, 23` → két sor; `Zsolt 14:1 / Zsolt 53:2` → két sor; `Mt 15:19 / Mk 7:21-23` → két sor); a kötőjeles tartomány egy sor marad (`1Móz 4:10-11`, `5Móz 27:15-26`) — az IGEHELY típus (SEMA 1.1) és a KIRALY-001 `1Móz 14:18-20` precedense szerint. A felbontott sorok a teljes eredeti sor mezőit öröklik.

**G4 — `fo_elofordulas`:** a napló HAMART-001 ⭐ bekezdésének négy szakasz-megnevezése, szó szerint: `1Móz 3:7-19`, `1Móz 4:1-24`, `1Móz 6:1-8`, `1Móz 6:9-22`. Minden A-táblás sor, amelynek verse ezekbe esik, megkapja a csoportkulcsot; a többi üres. (Az `1Móz 3:23` kívül esik a `3:7-19`-en, ezért üres.) A generátor önellenőrzése: `COUNT(DISTINCT)` = 4 = a napló száma.

**G5 — a `motivumok.tsv` sora:**

| Mező | Érték | Forrás |
|---|---|---|
| `cim` | A bűn következményeinek gyűrűzése — átok, föld és romlás | study címe |
| `ui_cimke` | Bűn gyűrűzése | javaslat |
| `tema` | Hamartológia | napló Kulcsszó-index |
| `pardes_szint` | Remez/Drash | **javaslat** — a táblasorok túlnyomó szintje |
| `statusz` / `_verzio` / `_datum` | publikálható / v1 / 2026.09.11 | study fejléce |
| `azonossag_tipusa` | strukturális | terv 4.6 táblázata |
| `negativ_kriterium` | az igehelynek a gerinc valamelyik elemén (*arar*, *adamá*, *itzávón*, *chattát*, *chámász*, *sáchat*; ἐπικατάρατος, κατάρα, φθείρω-család) vagy megnevezett kollokációján (*málé*+*chámász*, *sámá*+*chámász*) át kell a genezisi átok→föld→romlás láncra visszautalnia; a bűn, a büntetés vagy az átok puszta említése e lexémák nélkül csak explicit „tematikus, nem lexikai" jelöléssel kerülhet be | **javaslat** — a study saját gyakorlatának megfogalmazása |
| `folerendelt_fogalom` | a bűn / hamartológia általában | terv 4.6 (280. sor) |
| `sablon_verzio` | v14 | study fejléce |
| `forras_study` | `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` | |

**G6 — `jeloltek`: csak a beépített sorok.** Minden `elofordulasok`-sorhoz egy `beépítve` sor (2. szabály), `forras_kereses` = „négyforrásos audit a napló §7 szerint, retroaktív N14 betöltés" (az F3.1 mintájára), `indoklas` = a study Kapcsolódás-cellája, `datum` = 2026.09.11. A napló ❌-sorai **nem** kerülnek be — egyik betöltött motívumnál sem kerültek (a `jeloltek`-ben ma 3 `elutasítva` sor van összesen); a `general.py` hiánylistája jelenti őket, mostantól a betöltött ID-k 1. blokkjában. A napló két „nyitva hagyott" tétele más motívumhoz tartozik (kiáltó vér; lehetséges új motívum) — nem HAMART-001-sor.

---

## 3. Mi NEM a hatókör

- Károli-triplet (`karoli_szo`, …): üres marad; a F3.4-analóg pótlás külön tétel.
- `kapcsolatok.tsv`: kézi marad (F8 G10).
- A `gate.py` által talált új ütközések eldöntése: JELENTÉS, emberi döntés (A6b).
- Az ANTROP-001 naplója, N11, N13.
- A study szövegének bármilyen javítása. Ha a TAHOT-ellenőrzés (N14.1) eltérést talál, az jelentés, nem javítás.

---

## 4. Tételek

### 1. menet — munkalap, próba, **nem ír az `adat/`-ba**

#### N14.0 — kiindulás *(nem commitol)*
`main` = `origin/main` = `32d7952`; az egyetlen változás a commitolatlan `N14_BRIEF.md`. A §0 újramérve; eltérésnél megállás. A brief commitolva.

#### N14.1 — `eszkozok/n14_hamart_betoltes.py` + munkalapok
Egyszeri jegyzőkönyv-szkript az `f3_1_betoltes.py` mintájára (split('\t'), nem `csv`; memória-előbb; hosszellenőrzés). Import a `general`, `lekerdez`, `ellenoriz` modulból — saját `parse_range`, TSV-olvasó, proveniencia-szabály nincs.
- Beolvassa a study 1. pontjának A/B/C tábláját; a G2–G4 szabályokat alkalmazza.
- Mezők: `kapcsolodas` = Kapcsolódás-cella; `pardes_szint` = a PaRDeS-cella szint-része; `felmerult_tanulmany` = a szint utáni rész (SEMA 2.2), a markdown-jelölés (`**`, backtick) nélkül; `lexikon_szotar`/`lexikon_entry_id` = BDB / a BDB-entry-id, ha van; `jelentes_en`/`jelentes_hu` = a Jelentés-cella két fele, a 【NAPLO: …】 megjegyzések nélkül; `jelentes_szam` = a Sense-cella, **csak** ha a SEMA 2.2.2 értékkészletébe illik, különben üres, és a sor listázva; `proveniencia` = `scope=manual | forras=Bun_kovetkezmenyeinek_gyuruzese_tematikus.md | ts=2026-09-11`; `funkcio` üres.
- **`igazolas`** (SEMA 1.8): ÓSZ-sor, nem tematikus → `lekerdez.py scan <strong>` (TAHOT); ha a vers (tartománynál bármely verse) a találatok közt → `TAHOT-igazolt`, különben `nincs` **és eltérés-jelentés**; ÚSZ-sor → `TAHOT-hatokoron-kivul`; tematikus sor → `nincs`.
- Kimenet: `naplok/N14_hamart_elofordulasok_munkalap.tsv` (a `beepit` formátumában), `naplok/N14_hamart_jeloltek_munkalap.tsv`, `naplok/N14_hamart_motivum_munkalap.tsv`, és `naplok/N14_hamart_jelentes.md` a §5 minden számával.
- **Próba ideiglenes `--adat` másolaton** (a repón kívül): a három munkalap beírása, `betolt.py beepit --munkalap … --ir --adat <másolat>`, majd `ellenoriz.py --adat <másolat>` (a `RETROAKTIV_IDK` ideiglenes, csak a próbában érvényes bővítésével), `gate.py`, `kuszob.py`. Az eredmény a jelentésbe.
- `--ir` kapcsoló az éles íráshoz — ebben a menetben **nem** fut.

#### ⛔ Megállás — emberi jóváhagyás
A felhasználó átnézi a `N14_hamart_jelentes.md`-t: a gerinc-eloszlást, a TAHOT-eltéréseket, a `jelentes_szam`-kihagyásokat, a `gate.py` új ütközéseit. **A 2. menet csak kifejezett jóváhagyás után indul.**

### 2. menet — élesítés

#### N14.1a — munkalap-javítás *(a független ellenőrzés alapján, a v2-ben új)*
A javítás a **szkriptben** történik, a munkalapok újragenerálva — kézi TSV-szerkesztés nincs.
1. **1Móz 3:18** — a Jelentés-cella két szócikket tartalmaz (H6975 / H1863), a szétválasztás elcsúszott: a `jelentes_en` a magyar szöveg egy részét is hordozza. Javítás: `lexikon_entry_id` = `H6975` (a `strong`-gal egyezően), `jelentes_szam` = `1` (a Sense-cella „1 / —” H6975-ös fele), `jelentes_en` = `thornbush, thorn ... Gen 3:18`, `jelentes_hu` = `tövisbokor, tövis`. A `gerinc_elem` marad `H6975+H1863`.
2. **1Móz 8:21** — a teljes cella a `jelentes_en`-be került, a `jelentes_hu` üres. Javítás: `jelentes_en` = `be slight, of water, be abated; Pi'él: curse`, `jelentes_hu` = `csekélynek lenni, vízről: apadni; Pi'él: megátkozni`.
3. **`kapcsolodas`** — mind az 52 sor markdown-jelölést hordoz (`*…*`, `**…**`, backtick), a meglévő 201 sorból egy sem. Javítás: a `*` és a backtick jelek eltávolítva, a szöveg egyébként változatlan (a `felmerult_tanulmany` szabálya kiterjesztve).
4. Általános őr a szkriptben: ha egy `jelentes_en` tartalmazza a „magyarul” szót, vagy a két jelentés-mező közül csak az egyik üres, a szkript kód 1-gyel megáll.

A próba-futás megismétlődik (K4 ugyanazokkal a számokkal). Commit: `N14.1a: munkalap-javítás — 1Móz 3:18, 8:21, kapcsolodas-jelölés`.


#### N14.2 — adat
Sorrend: `motivumok` → `jeloltek` (a szkript `--ir`-je) → `elofordulasok` (`betolt.py beepit --munkalap naplok/N14_hamart_elofordulasok_munkalap.tsv --ir`). Az `ellenoriz.py` `RETROAKTIV_IDK`-ja 8 ID, a SEMA §3/8 szövege „8 retroaktív".

#### N14.3 — forrásréteg és generált kimenetek
- `motivumok/HAMART-001.md` a F4.4/G2 mintájára: a napló 119., 183. és 284. sorának HAMART-001-szövege és az index kézi szakaszának sora **karakterre azonosan** átemelve, a TEREMT-001.md szerkezetével (archív címsorok, proveniencia-bekezdés).
- A négy kézi szöveg törlése a helyéről (napló, index). Az index „A táblába még nem betöltött…" szakasza teljes egészében törlődik.
- `general.py --cel naplo --ir` és `--cel index --ir`. Előtte próba `--kimenet`-tel; ha a HAMART-001 bármely szövege kétszer szerepelne, megállás.

#### N14.4 — nyitott lista, runbook
- `NYITOTT_FELADATOK.md`: N14 lezárva (a G1–G6 lényegével, commit-hivatkozással). A GENERÁLT blokk nem módosul.
- `MUNKAMENET.md` „Mi hiányzik": N11, N13.
- `naplok/F8_5_ellenoriz_alap.txt` újragenerálva.

---

## 5. Várt számok — jóváhagyva (2026-09-21)

A számok a study táblájának a G2–G4 szerinti előzetes feldolgozásából valók; az N14.1 méri őket.

| Mit | Várt |
|---|---|
| study-táblasor → `elofordulasok`-sor | 46 → **52** (A: 20 → 23, B: 18 → 20, C: 8 → 9) |
| `jeloltek` új sor | **52**, mind `beépítve` |
| `gerinc_elem` eloszlása | H0779 7 · H0127 7 · H7843 7 · `málé+chámász` 6 · `sámá+chámász` 4 · H2555 4 · `tematikus:*` 5 · H6093 2 · G1944 2 · H2403, H6975+H1863, H7451, H7043, G5356, G2671, G1311, G5351 1-1 |
| legnagyobb elem | 7 sor (a SEMA 2.2.1 „20 sor" jelzési küszöbe alatt) |
| `fo_elofordulas` | **16 sor, 4 csoport** (3:7-19: 5 · 4:1-24: 5 · 6:1-8: 2 · 6:9-22: 4) |
| `igazolas` | ÚSZ lexikai 6 → `TAHOT-hatokoron-kivul`; tematikus 5 → `nincs`; ÓSZ lexikai 41 → `TAHOT-igazolt`, **ha** a TAHOT minden sort megerősít (eltérés = jelentés) |
| `ellenoriz.py` az élesítés után | **6 · 0 · 3 · 1**, kód 0; 8/c = **KÉZI (8)**; a HAMART-001 sora napló-úttal |
| ⭐ HAMART-001 | 4 |
| `kuszob.py` | 8 ID, 0 átlépés |

---

## 6. Elfogadási kritériumok

### 1. menet

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | Kiindulás | a §0 minden sora jelentve; eltérésnél megállás |
| K2 | Munkalapok | a §5 első öt sora mért értékkel; a G2 gerincen kívüli három sora név szerint; a `jelentes_szam`-kihagyások listája |
| K3 | Igazolás | a TAHOT-eltérések tételes listája (igehely, strong, a scan találatszáma), vagy „0 eltérés" |
| K4 | Próba-másolat | `beepit`: 52 sor, 0 hiba; `ellenoriz.py`: 6 · 0 · 3 · 1, 8/c KÉZI (8); `gate.py` új ütközései HAMART-001-párosításonként; `kuszob.py`: 0 átlépés; az éles `adat/` bájtra változatlan |
| K5 | Import | a szkriptben nincs saját `def parse_range`, TSV-olvasó, `proveniencia_ervenyes` |
| K6 | Commitok | a §7 1. menet-táblája szerint; `git status --porcelain` üres; a próba-könyvtár a repón kívül |

### 2. menet

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K6a | N14.1a | a négy pont mért értékkel: a két sor négy-négy mezője szó szerint; a `kapcsolodas`-ban `*` és backtick 0 sorban; a „magyarul”-őr aktív; a K4 számai változatlanok |
| K7 | Adat | `motivumok` 8, `jeloltek` +52, `elofordulasok` +52 sor; a 7 régi ID sorai bájtra változatlanok |
| K8 | `ellenoriz.py` | a §5 szerint; `RETROAKTIV_IDK` 8 elem; SEMA §3/8 „8 retroaktív" |
| K9 | Forrásréteg | `motivumok/HAMART-001.md` megvan; a négy átemelt szöveg `diff`-fel karakterre azonos az eredetivel; a napló és az index helyükön nem tartalmazza őket |
| K10 | Generált kimenet | a napló ⭐ blokkja „8 motívum-ID"-t fed, benne HAMART-001 4 fő előfordulással; az index K8-figyelmeztetése eltűnt; `grep -c "HAMART-001"` minden generált blokkban pontosan a vártnyi (egyszer, nem kétszer) |
| K11 | Lista, runbook | N14 lezárva; „Mi hiányzik" = N11, N13; a GENERÁLT blokkon kívül más nem változott |
| K12 | Commitok | a §7 2. menet-táblája szerint; `git status --porcelain` üres |

---

## 7. Commitok

**1. menet**

| Commit-üzenet | Fájlok |
|---|---|
| `N14_BRIEF.md v1: a HAMART-001 betöltése` | `N14_BRIEF.md` |
| `N14.1: n14_hamart_betoltes.py + munkalapok (próba)` | `eszkozok/n14_hamart_betoltes.py`, `naplok/N14_hamart_*.tsv`, `naplok/N14_hamart_jelentes.md` |

**2. menet**

| Commit-üzenet | Fájlok |
|---|---|
| `N14.1a: munkalap-javítás — 1Móz 3:18, 8:21, kapcsolodas-jelölés` | `eszkozok/n14_hamart_betoltes.py`, `naplok/N14_hamart_*.tsv`, `naplok/N14_hamart_jelentes.md` |
| `N14.2: HAMART-001 az adat/-ban — retroaktív, 52 sor` | `adat/motivumok.tsv`, `adat/jeloltek.tsv`, `adat/elofordulasok.tsv`, `adat/SEMA.md`, `eszkozok/ellenoriz.py` |
| `N14.3: HAMART-001 forrásréteg + generált napló és index` | `motivumok/HAMART-001.md`, `motivumlog/PaRDeS_motivumok.md`, `Lezart_tematikus_tanulmanyok_index.md` |
| `N14.4: N14 lezárva` | `NYITOTT_FELADATOK.md`, `MUNKAMENET.md`, `naplok/F8_5_ellenoriz_alap.txt` |

**Push csak külön kérésre.**

---

## 8. Nyitó promptok *(Sonnet)*

### 1. menet
```
Olvasd el a CLAUDE.md-t, majd az N14_BRIEF.md-t teljes egészében.

0. N14.0: main = origin/main = 32d7952; az egyetlen változás a commitolatlan
   N14_BRIEF.md. Mérd újra a §0 tábláját. Ha bármi eltér, ÁLLJ MEG.
   Commitold a briefet: "N14_BRIEF.md v1: a HAMART-001 betöltése".
1. N14.1 a §4 szerint. K2, K3, K4, K5. Az éles adat/-ba NE írj; a szkript
   --ir kapcsolóját élesben NE futtasd.
2. Commit a §7 1. menet-táblája szerint. K6.
3. ÁLLJ MEG. A 2. menet (N14.2–N14.4) csak a felhasználó jóváhagyása után indul.

A próbához ideiglenes könyvtárat használj a repón kívül.
Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Minden K-kritériumot mért értékkel igazolj. Push nincs.
Zárójelentés: hash-ek, K1–K6 külön sorban; a §5 táblája mért értékekkel,
a várttól eltérő sorok kiemelve; minden eltérés.
```

### 2. menet
```
Olvasd el a CLAUDE.md-t, majd az N14_BRIEF.md-t és a naplok/N14_hamart_jelentes.md-t.

0. main = origin/main = d7a58a6; az egyetlen változás a commitolatlan
   N14_BRIEF.md (v2). Ha más is változott, ÁLLJ MEG.
   Commitold: "N14_BRIEF.md v2: N14.1a a független ellenőrzés alapján".
1. N14.1a. K6a. Ha a K4 számai eltérnek, ÁLLJ MEG.
1b. N14.2. K7, K8.
2. N14.3. K9, K10. A general.py-t előbb --kimenet próbával futtasd;
   ha a HAMART-001 bármely szövege kétszer szerepelne, ÁLLJ MEG.
3. N14.4. K11.
4. Commitok a §7 2. menet-táblája szerint. K12.

Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Minden K-kritériumot mért értékkel igazolj. Push nincs.
Zárójelentés: hash-ek, K6a és K7–K12 külön sorban; az ellenoriz.py új összesítő
sora; minden eltérés, külön kiemelve a hiányzó és a plusz fájlokat a §7-hez képest.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Két menet, köztük ⛔ emberi megállás | Adatírás és 52 soros értelmezési leképezés; az A4/B5 elve: besorolási döntésen nem lép át némán az ügynök |
| D2 | G1: retroaktív lista (b), nem újrafuttatott lekérdezések (a) — a korábbi chat-javaslat visszavonva | Az (a) utólag gyártott provenienciát adna (N12 D3); a napló §7-je tételesen dokumentálja az 5 `mindig` dataset lekérdezését |
| D3 | Az új eszközlánc éles próbája a `betolt.py beepit`, nem az `auditok` | A `beepit` itt valódi adaton fut először; az `auditok` az első új motívumnál kap valódi sort |
| D4 | G2: a `gerinc_elem` a study saját BDB-horgonya, kollokációnál a SEMA 2.2 pár-alakja | A szerző választása, nem utólagos értelmezés; a H2555 14 sora három valódi horgonyra bomlik |
| D5 | A Hós 4:1-3 tematikus horgonya (`1Móz 3:17`) következtetés, jelölten | A study nem nevez meg genezisi párt; a jóváhagyás ezt a sort külön érinti |
| D6 | G3: `,` és `/` mentén bontás, kötőjeles tartomány egyben | IGEHELY típus; KIRALY-001 precedens |
| D7 | G4: a napló négy szakasz-megnevezése a csoportkulcs; az 1Móz 3:23 kívül esik | SEMA 2.2.3: szó szerint a napló szövege |
| D8 | G6: csak `beépítve` sorok a `jeloltek`-ben | A 7 betöltött motívum gyakorlata; a ❌-sorokat a hiánylista jelenti |
| D9 | A napló kézi szövegei a forrásrétegbe, karakterre azonosan | A F4.4/G2 mintája; generált és kézi HAMART-001-szöveg nem állhat egymás mellett |
| D10 | Az `igazolas` a mai TAHOT-scanből számolódik | Az igazolás megerősítés, nem proveniencia (SEMA 1.8) — a D2-vel nem ütközik |
| D11 | A G1–G6 és a §5 számai jóváhagyva (2026-09-21), a javasolt változatban — a Hós 4:1-3 `tematikus:1Móz 3:17` horgonnyal, `pardes_szint` = Remez/Drash, a `negativ_kriterium` a G5 szövegével | A G0-minta; a számtábla a futás előtt megerősítve |
| D12 | Független ellenőrzés az 1. menet után (`d7a58a6`): a számok, a szúrópróbák (1Móz 3:17, Ez 8:17, Hós 4:1-3, Zsolt 14:1 / 53:2, 5Móz 27:15-26) és a „nincs új ütközés” állítás tartomány-kibontással is megerősítve | A F8 D16 óta minden zárójelentés független ellenőrzést kap |
| D13 | N14.1a: két elemzési hiba (1Móz 3:18, 8:21) a szkriptben javítva, nem kézzel | A munkalap a szkript kimenete; a kézi javítás a jegyzőkönyvet hamisítaná |
| D14 | A `kapcsolodas` markdown-jelölése eltávolítva | A meglévő 201 sor egyike sem hordoz jelölést — adatréteg-konzisztencia; a v1 „szó szerint” előírása ezt nem látta előre |
| D15 | 1Móz 3:18: a lexikon-hivatkozás a H6975-re szűkül, a H1863 a `gerinc_elem`-ben marad | A `lexikon_entry_id` egyetlen szócikk kulcsa (SEMA 2.5); a horgony-információ nem vész el |
