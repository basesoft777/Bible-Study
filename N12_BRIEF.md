# N12 — A SEMA §3/8 motívumszintre: `auditok.tsv` + a 8. szabály átírása

*Készítette: chat-menet (Opus 5), 2026-09-21, **v1** — a §2 G1–G4 és a §5 várt számai jóváhagyva (2026-09-21).*
*Kiindulási állapot: `main` = `origin/main` = `6e3fd43` (F8 lezárva, F8.10a pusholva).*
*Egy menet, Sonnet, a §7 nyitó promptjával.*

---

## 0. A probléma — mérve, `6e3fd43`

| Mit | Mért érték |
|---|---|
| `elofordulasok` sorai | 201, mind `scope=manual` (F3-betöltés) |
| `ellenoriz.py` 8. szabály | SÉRTÉS (35) = 7 motívum × 5 tematikus `mindig` dataset |
| tematikus `mindig` datasetek | BDB, Karoli_1908, Karoli_KH, TAHOT, TSK |
| ebből `lekerdez.py`-parancs írja a `forras`-t | TAHOT (`scan`, `kollokacio`, `igealak`, `gerinc`), TSK (`tsk`), Karoli_1908 + Karoli_KH (`karoli`, **egy sorban, `+`-szal**) |
| lekérdező nélküli `mindig` dataset | BDB |
| alapjelentés összesítője | RENDBEN 6 · SÉRTÉS 1 · KÉZI 1 · JELENTÉS 1, kód 1 |
| a 7 motívum `forras_study`-jához tartozó kereszthivatkozás-napló | 6 van (`tematikus_lezart/naplok/`), ANTROP-001-hez (`Pneuma_pszukhe_…`) nincs |

**Illesztési hiba** (`szabaly8_dataset_lefedettseg`): a nyom-keresés részsztring-vizsgálat (`'forras=%s' % fajl in p`). A `karoli` parancs sora `forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv` — ebben a Karoli_KH **soha nem illeszkedik**, a Karoli_1908 csak véletlenül (előtag). Ugyanígy nem illeszkedne a `lxx-hid` második forrása, és illeszkedne egy `…tsv.bak` álnév.

---

## 1. A javaslat magja

1. A 8. szabály **motívumszintű**: a nyomot új tábla adja, `adat/auditok.tsv`. Minden érintett lekérdezés egy sort kap, 0 találat esetén is. A `lexikai-scan` subagent a proveniencia-sort amúgy is szó szerint visszaadja — a rögzítés nem új munka.
2. A 7 retroaktív motívum **KÉZI**, nem RENDBEN: „ember ellenőrizze", a study és a kereszthivatkozás-napló útjával.
3. A BDB KÉZI, amíg nincs rá lekérdező parancs.
4. A `forras` értéke `+` mentén bontva, **pontos** fájlnév-egyezéssel illeszt.

Eredmény: ma sárga (KÉZI) a piros helyett; az első új motívumnál gépi zöld vagy piros.

---

## 2. G-döntések — jóváhagyva (2026-09-21)

Az eredeti javaslathoz képest **két pont eltér** (G1, G2) — mindkettő a mért állapotból következik.

**G1 — az `auditok.tsv` oszlopai: `id`, `lepes`, `proveniencia`, `datum`. Nincs `dataset` oszlop.**
Egy lekérdezés több datasetet érinthet (`karoli` → 2, `lxx-hid` → 2, `gerinc` → akár 2). Külön `dataset` oszlop vagy soronkénti duplikálást, vagy a `forras`-sal redundáns, szétcsúszni képes mezőt jelentene. A dataset a `proveniencia` `forras` kulcsából **származtatott**: `+` mentén bontva, a `datasetek.tsv` `fajl` mezőjének alapnevével egyeztetve. A `lepes` értékkészlete: `A5` | `B2` | `B4`.
*Elvetett:* `dataset` oszlop `+`-szal összefűzött nevekkel (két igazság-forrás).

**G2 — a rögzítés hatóköre: A5 + B2 + B4, nem csak B4.**
A TSK, a Karoli_1908 és a Karoli_KH `mindig` dataset, de a nyomukat író `tsk` és `karoli` parancs az **A5**-ben fut. Csak B4-rögzítéssel az első új motívum ezen a három dataseten örökre piros volna.

**G3 — a retroaktív motívumok zárt listája: `RETROAKTIV_IDK` konstans az `ellenoriz.py`-ban** — a `6e3fd43` 7 ID-je (ALVIL-001, ANTROP-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001).
*Elvetett:* „nincs `auditok`-sora → retroaktív". Ez egy rögzítést elfelejtő **új** motívumot is sárgára engedne — pont azt a hibát rejtené el, amit a szabály fog. A zárt lista történeti tény, nem bővül. Ha egy retroaktív motívum később `auditok`-sort kap, az a dataset gépileg fedettnek számít; a hiányzó datasetjei KÉZI maradnak.

**G4 — a lekérdező nélküli datasetek: `LEKERDEZO_NELKULI = {'BDB_teljes_unabridged.tsv'}` konstans.** Minden motívumnál KÉZI („nincs lekérdező parancs"). Ha egyszer lesz `lekerdez.py bdb`, a tag kikerül a halmazból — más változtatás nem kell.

---

## 3. Mi NEM a hatókör

- `lekerdez.py bdb` parancs (G4 feltétele, külön tétel).
- A 7 retroaktív motívum utólagos igazoló lekérdezése (N12 (c) opciója — elvetve, l. D3).
- `betolt.py audit` alparancs a sor validált hozzáfűzésére: ma kézi hozzáfűzés, a validálást az `ellenoriz.py` végzi (§4 N12.2). Ha a gyakorlatban hibázik, külön tétel.
- A `lexikai-scan` subagent módosítása: fájlt továbbra sem ír; a sort a fő szál rögzíti.
- A 8/b (feltételes datasetek) viselkedése nem változik.
- N11, N13.
- Az ANTROP-001 kereszthivatkozás-naplójának pótlása — kutatói tétel, a Pneuma-study v12-compliance része (`NYITOTT_FELADATOK.md`, „5 további tematikus study"). A 8/c-jelzés a napló megszületésekor kódmódosítás nélkül átvált az útra. A `generalt_proba/` alatti generált napló **nem** élesíthető helyette (B7; körkörös bizonyíték volna, l. D11).

---

## 4. Tételek

#### N12.0 — kiindulás *(nem commitol)*
`main` = `origin/main` = `6e3fd43`; az egyetlen változás a commitolatlan `N12_BRIEF.md`. A §0 tábláját újraméri. Eltérésnél megállás.

#### N12.1 — SEMA + üres tábla
- `adat/SEMA.md` új **2.9 `auditok.tsv` — lekérdezés-napló, motívumszintű dataset-nyom**: kulcs nincs (egy ID-hez több azonos sor is lehet); oszlopok G1 szerint; `proveniencia` = a `lekerdez.py` utolsó sora **szó szerint**, a `proveniencia: ` előtag nélkül; `datum` = `DATUM` (1.3); minden A5/B2/B4-lekérdezés sort kap, 0 találatnál is; a dataset a `forras`-ból származtatott (G1).
- §3/1 kiegészül: `auditok.id` → létező `motivumok.id`.
- §3/3 kiegészül: az `auditok.proveniencia` ugyanezen szabály alá esik.
- §3/8 új szövege:
  > **8. Dataset-lefedettség** (motívumszintű). Egy motívum nyomai: az `auditok` sorai és az `elofordulasok` proveniencia-mezői; a nyomot a `forras` `+` mentén bontott fájlnevei adják, pontos egyezéssel. Minden `mindig` datasethez tartozzon nyom. Kivételek, KÉZI jelentéssel: (a) a lekérdező nélküli datasetek (`ellenoriz.LEKERDEZO_NELKULI`, ma: BDB); (b) a 7 retroaktív, F3-betöltésű motívum hiányzó datasetjei (`ellenoriz.RETROAKTIV_IDK`, zárt lista). A `felteteles` datasetek a 8/b alatt KÉZI.
- `adat/auditok.tsv`: két `#` megjegyzéssor (a többi tábla mintájára) + fejléc, **0 adatsor**.

#### N12.2 — `ellenoriz.py`
- Új segédfüggvény: `forras_fajlok(proveniencia) -> set` — a `proveniencia_parse` `forras` értéke `+` mentén, `strip`-pel; érvénytelen sornál üres halmaz.
- `auditok.tsv` beolvasása a többi táblával együtt (hiányzó fájl → kód 2).
- 1. szabály: az `auditok` sorai is. 3. szabály: az `auditok` sorai is, `proveniencia_ervenyes`-sel (import, nem másolat — F8 D21).
- **8. szabály** átírva, két jelentéssorra:
  - **„8. Dataset-lefedettség (gépi)"** — a vizsgált ID-k: `elofordulasok` ∪ `auditok` ID-jei. A párok: (ID, `mindig` dataset), **kivéve** a `LEKERDEZO_NELKULI`-t és a retroaktív ID-k még fedetlen datasetjeit. Hiány → SÉRTÉS, a hiányzó datasettel. Minden pár fedett → „RENDBEN (mindig)". **0 gépi pár → KÉZI**, megjegyzés: „nincs gépileg ellenőrizhető motívum" — soha nem RENDBEN üres halmazon (F8 D13 elve).
  - **„8/c. Kézi dataset-lefedettség"** — KÉZI, soronként egy ID: a fedetlen datasetek listája, BDB-nél „(nincs lekérdező)", retroaktívnál „(retroaktív, F3)", és a mutató: „ember ellenőrizze: `<forras_study tematikus_lezart/ tagja>` + `<napló útja>` | napló nincs". A napló útja: `[study-mappa]/naplok/<törzs>_kereszthivatkozas_naplo.md`, ahol `<törzs>` a study-fájl neve `.md` nélkül, vagy ugyanez a `_tematikus` végződés nélkül — az első létező. Ha egyik sem, de létezik `generalt_proba/[study-mappa]/naplok/<ID>_kereszthivatkozas_naplo_GENERALT.md`: „napló nincs (csak generált próba: `<út>`, nem a study eredeti keresése)"; ha ez sincs: „napló nincs".
- A `--study` Q7 ugyanezt a logikát használja `csak_id`-vel: Q7 sor + 8/b + 8/c az adott ID-re.
- A régi részsztring-illesztés megszűnik; `grep -c "in p)" eszkozok/ellenoriz.py` = 0.
- `naplok/F8_5_ellenoriz_alap.txt` újragenerálva ugyanazzal a hívással.

#### N12.3 — runbook és nyitott lista
- `MUNKAMENET.md`: az **A5, B2, B4** sor Megjegyzése kiegészül: „minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy". A B10 sor Megjegyzése: „…a `felteteles` datasetek és a 8/c kézi".
- `NYITOTT_FELADATOK.md`: N12 lezárva — egy mondat a G1–G4 lényegével és a commit-hivatkozással (a meglévő lezárt tételek mintájára). A GENERÁLT blokk nem módosul.
- `MUNKAMENET.md` „Mi hiányzik": „N11–N13" → „N11, N13".

---

## 5. Várt számok — jóváhagyva (2026-09-21)

A mai adaton (`6e3fd43` + N12), `python eszkozok/ellenoriz.py`:

| Jelentéssor | Ma | N12 után |
|---|---|---|
| 1–6. szabály | RENDBEN | RENDBEN (változatlan) |
| 7. szabály | JELENTÉS | JELENTÉS (változatlan) |
| 8. | SÉRTÉS (35) | **KÉZI** — 0 gépi pár |
| 8/b | KÉZI (9) | KÉZI (9) (változatlan) |
| 8/c | — | **KÉZI (7)** — 7 ID, mindegyiknél 5 dataset (4 retroaktív + BDB) |
| 8/c napló-mutató | — | 6 ID-nél napló út; ANTROP-001-nél „napló nincs (csak generált próba: `generalt_proba/tematikus_lezart/naplok/ANTROP-001_kereszthivatkozas_naplo_GENERALT.md`, …)" |
| Összesítő | 6 · 1 · 1 · 1 | **6 · 0 · 3 · 1** |
| Kilépési kód | 1 | **0** |

---

## 6. Elfogadási kritériumok

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | Kiindulás | a §0 minden sora jelentve, egyezik vagy eltérés + megállás |
| K2 | SEMA + tábla | 2.9 megvan; §3/1, §3/3, §3/8 a §4 szerint; `adat/auditok.tsv` adatsora 0; a többi `adat/*.tsv` bájtra változatlan |
| K3 | Mai adat | a §5 táblájának **minden** sora mért értékkel igazolva; kód 0 |
| K4 | `--study` | mind a 7 motívum-study-ra fut; mindegyiknél Q7 = KÉZI, a 8/c sora a saját ID-re; ANTROP-001-nél „napló nincs (csak generált próba: …)", a generált próba útjával |
| K5 | Illesztés | ideiglenes `--adat` másolaton, szintetikus `TESZT-001` motívummal (nem retroaktív) és **valódi** `lekerdez.py`-kimenetekből vett sorokkal: (a) `scan` + `tsk` + `karoli` sor → 8. = RENDBEN (mindig), a 8/c-ben TESZT-001 csak BDB-vel; (b) a `karoli` sor nélkül → SÉRTÉS, **mindkét** Károli-dataset név szerint; (c) csak a `karoli` sor → a Karoli_KH fedett (a régi hiba megszűnt); (d) `forras=TSK_kereszthivatkozasok.tsv.bak` → TSK nem fedett; (e) nem létező ID-jű `auditok`-sor → 1. szabály SÉRTÉS; (f) `talalat=` kulcsos `auditok`-sor → 3. szabály SÉRTÉS; (g) 0 találatos `scan` sora (`n=0`) elfogadott nyom |
| K6 | Retroaktív zárt lista | ugyanazon a másolaton egy `auditok`-sor nélküli, `elofordulasok`-sorral bíró új ID → 8. SÉRTÉS (nem KÉZI); egy retroaktív ID egyetlen TAHOT-sorral → a TAHOT nála nincs a 8/c-ben, a többi 4 igen |
| K7 | Import | `proveniencia_ervenyes`/`proveniencia_parse` nincs másolva; `grep -c "in p)" eszkozok/ellenoriz.py` = 0 |
| K8 | Runbook | A5, B2, B4, B10 sor a §4 szerint; N12 lezárva; „Mi hiányzik" = N11, N13; a GENERÁLT blokkon `git diff` 0 sor |
| K9 | Commitok | a §7 szerint, a hiányzó és a plusz fájlok is jelentve; `git status --porcelain` üres; a próba-könyvtár nincs a repóban |

---

## 7. Commitok

| Commit-üzenet | Fájlok |
|---|---|
| `N12_BRIEF.md v1: a SEMA §3/8 motívumszintre` | `N12_BRIEF.md` |
| `N12.1: SEMA 2.9 + §3/1,3,8 — auditok.tsv` | `adat/SEMA.md`, `adat/auditok.tsv` |
| `N12.2: ellenoriz.py — motívumszintű 8. szabály, forras-bontás` | `eszkozok/ellenoriz.py`, `naplok/F8_5_ellenoriz_alap.txt` |
| `N12.3: runbook — auditok-rögzítés, N12 lezárva` | `MUNKAMENET.md`, `NYITOTT_FELADATOK.md` |

**Push csak külön kérésre.**

---

## 8. Nyitó prompt *(Sonnet)*

```
Olvasd el a CLAUDE.md-t, majd az N12_BRIEF.md-t teljes egészében.

0. N12.0: main = origin/main = 6e3fd43; az egyetlen változás a
   commitolatlan N12_BRIEF.md. Mérd újra a §0 tábláját. Ha bármi eltér,
   ÁLLJ MEG. Commitold a briefet: "N12_BRIEF.md v1: a SEMA §3/8 motívumszintre".
1. N12.1. K2.
2. N12.2. K3, K4, K5, K6, K7. Az éles adat/-ba adatsort NE írj.
3. N12.3. K8.
4. Commitok a §7 szerint. K9.

A próbákhoz ideiglenes könyvtárat használj a repón kívül; a repóba nem kerülhet.
A K5 soraihoz a lekerdez.py-t ténylegesen futtasd, a proveniencia-sort ne gépeld.
Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Minden K-kritériumot a tényleges kimenettel igazolj: idézd a mért számot
vagy a kimeneti sort. Push nincs. Zárójelentés: hash-ek, K1–K9 külön sorban,
kihagyás nélkül; az ellenoriz.py új összesítő sora; minden eltérés — külön
kiemelve a hiányzó és a plusz fájlokat a §7-hez képest.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Az N12-ből önálló, egymenetes fázis, saját brieffel | Az F8 lezárva; a tétel kicsi, de sémát és ellenőrző logikát érint |
| D2 | A 8. szabály motívumszintű, új `auditok.tsv`-vel | A nyom a lekérdezéshez tartozik, nem az igehelyhez; 0 találat is nyom |
| D3 | A retroaktív motívum KÉZI, nem RENDBEN és nem utólagos lekérdezés | Az N12 (b) opciója őszinte formában; a (c) utólag gyártott, nem a study-t megalapozó provenienciát adna |
| D4 | G1: `dataset` oszlop nincs, a `forras`-ból származtatott | Többdatasetes lekérdezés; egy igazság-forrás |
| D5 | G2: A5 + B2 + B4 rögzít | A TSK és a két Károli-dataset nyomát csak az A5 írja |
| D6 | G3: a retroaktív ID-k zárt konstans listája | Az „auditok nélkül → retroaktív" feltétel elrejtené az új motívum elfelejtett rögzítését |
| D7 | G4: BDB konstans halmazban, KÉZI | Nincs lekérdező; a halmaz a parancs megjelenésével szűkül |
| D8 | Üres gépi halmazon a 8. szabály KÉZI, nem RENDBEN | Üres halmazon a „rendben" hamis zöld (F8 D13, D16) |
| D9 | A 8. szabály két sorra bomlik (gépi + 8/c kézi) | Így az új motívum gépi zöldje látható marad a BDB állandó KÉZI-je mellett |
| D10 | A K5 valódi `lekerdez.py`-kimenettel tesztel | A hiba forrása éppen a valódi formátum (`+`) volt |
| D11 | Az ANTROP-001 naplójának pótlása nem az N12 része (§3) | Kutatói munka, a Pneuma-study v12-compliance tétele; a generált próba a `jeloltek.tsv`-ből (9 sorból 8 retroaktív F3.2) készült, élesítve körkörös bizonyíték volna, és a `naplok` cél szándékosan nem élesíthető |
| D12 | Napló hiányában a 8/c a generált próbára mutat, kifejezett megszorítással | Az ellenőrző ember támpontot kap, a jelzés mégsem állít nem létező naplót |
| D13 | A G1–G4 és a §5 számai jóváhagyva (2026-09-21), a javasolt változatban | A G0-minta az F4 óta; a számtábla a futás előtt megerősítve |
