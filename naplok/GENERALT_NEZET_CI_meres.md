# GENERALT_NEZET_CI — mérési napló (FELADATOK #116)

*Brief: `F116_GENERALT_NEZET_CI_BRIEF.md` · Ág: `claude/f116-generalt-nezet-ci` · Modell: claude-sonnet-5-5*

## 1. M0 — kiinduló mérés (2026-10-18)

`scope=general.py --ellenoriz (naplo, index, nyitott), blokk-diff scratch-szkripttel, git log/show, WSL-újrafuttatás git archive-ból | forras=manual (CLI-futtatás) | ts=2026-10-18 | alap=origin/main be85d5de (+ F116.0 commit 2fc22d66)`

### 1.1 Az E28/E29 számok

Az `E28` és az `E29` szabad: a `szabalyok.py`-ban és a workflow-ban (`.github/workflows/`) nincs
előfordulásuk, és a távoli ágak `*.py`/`*.yml` fájljaiban sincs (`git grep` minden `origin/*` ágon).
Az md-fájlokban a #23 CI-terve (DT84), a SEMA 3.10.4 hivatkozása és a #112 briefje (E30) említi
őket. A `szabalyok.py` legmagasabb száma az E27. **A brief feltevése egyezik.**

### 1.2 Blokkonkénti állapot (`general.py --cel <c> --ellenoriz`)

| Blokk | Állapot | Diff-sor |
|---|---|---|
| `naplo#attekintes` | zöld | 0 |
| `naplo#kuszob` | zöld | 0 |
| `naplo#kulcsszo_index` | zöld | 0 |
| `naplo#konyv_index` | **eltér** | 4 (2 törölt + 2 hozzáadott: a Jób-sor és a Préd-sor cseréje) |
| `index` | zöld | 0 |
| `nyitott` | **eltér** | 79 |

A mérés egyezik a brief mért állapotával (4 és 79 diff-sor).

### 1.3 Az eltérések oka

**`naplo#konyv_index` (4 diff-sor): adatváltozás újragenerálás nélkül.** A Jób 17:13/17:16 → 17:12/17:15
és a Préd 9:10 → 9:12 ALVIL-001-sor az `adat/elofordulasok.tsv` három sora; mind a `98f22fc6`
(F87.3: „M1 — az öt sor javítása az elofordulasok.tsv-ben és a jeloltek.tsv-ben”, 2026-10-12)
commitban változott (`git log -S'Jób 17:12'`, `-S'Préd 9:12'`). A `motivumlog/PaRDeS_motivumok.md`-t az óta nem érintette commit
(utolsó: `be2ae5b5`, 2026-10-02, F35.4 szövegcsere), tehát a blokk nem generálódott újra. Kézi szerkesztés
és generátor-változás a blokk törzsében nincs.

**`nyitott` (79 diff-sor): adatváltozás újragenerálás nélkül.** A blokk `ts=2026-09-15`
(`f4253313`) állapotán 17 nyitva sor állt a `jeloltek.tsv`-ben; azóta a nyitva-halmaz sorszintű
követése (`git show <rev>:adat/jeloltek.tsv` minden érintő commiton) szerint:

| Commit | Dátum | Hatás a nyitva-halmazra |
|---|---|---|
| `8313214d` T1.3 / `ed79575a` T2.2 | 2026-09-25 | TEREMT-002: +66, majd −66 (átmeneti, a végállapotban nincs) |
| `a0c3cd95` F63.5 (+244 sor) | 2026-10-11 | +8: HAMART-001 ×7 (2Pét 3:10, 3:12; 5Móz 4:25; Bír 2:19; Jób 16:18, 31:38; Sof 3:7), KIRALY-001 ×1 (1Pét 2:9); `elutasítva` 66→302 |
| `4f85d54c` F63.15 | 2026-10-11 | `elutasítva` 302→308 (nyitva nem változik) |
| `b5e60b5c` F108.1 | 2026-10-17 | +25: ANTROP-001 ×2 (Mt 12:18, 1Pét 1:22), HAMART-001 ×1 (2Tim 3:8), ISTENTISZT-001 ×21, TEREMT-001 ×1 (Jób 41:32) |

Összesen 17 + 8 + 25 = 50 nyitva sor 7 motívum-ID-ről (megszűnt nyitva sor: 0); `elutasítva` 308;
`beépítve` 259 (változatlan). A 79 diff-sor teljes lebontása: 1 fejsor (összegzés), 17 törölt +
50 hozzáadott táblasor (a 17 régi sor újraszámozva, +33 új), 5+5 sor a tanulmány-táblában
(nyitott-oszlop: ANTROP 1→3, HAMART 0→8, ISTENTISZT 0→21, KIRALY 0→1, TEREMT-001 0→1);
1+17+5 = 23 törölt, 1+50+5 = 56 hozzáadott. Kézi szerkesztés és generátor-változás nincs.

**A brief feltevése mindkét blokkra egyezik** (az ok újragenerálás nélküli adatváltozás).

### 1.4 A generátor futása friss checkouton, `konkordancia/_nyers/` nélkül

A worktree és a `git archive HEAD` kibontása is friss checkout; a `konkordancia/_nyers/` egyikben
sincs. A három cél (`naplo`, `index`, `nyitott`) mindkettőn hiba nélkül lefut (`rc=0`, üres stderr),
és az `--ellenoriz` ugyanazt az állapotot adja (lásd 1.2). **A generátor CI-ben futtatható.**

Futási idő célonként (egyszeri mérés, a Python-indítással együtt):

| Cél | Windows (worktree) | Linux/WSL2 (ext4, `git archive`) |
|---|---|---|
| naplo | ~0,19 s | ~0,10 s |
| index | ~0,19 s | ~0,07 s |
| nyitott | ~0,19 s | ~0,07 s |

### 1.5 Sorvég

- A három cél commitolt blobja tisztán LF (`git show HEAD:<út> | grep -c $'\r'` = 0; `git ls-files --eol`:
  `i/lf`); a Windowsos munkafában a `core.autocrlf=true` miatt `w/crlf`. A `.gitattributes` csak a
  `*.tsv`, a `.claude/agents/*.md` és a `*.sh` fájlokra ír elő `eol=lf`-et; a `*.md`-re nem.
- A `--kimenet` alá írt generátor-kimenet mindhárom célra tisztán LF (0 CR bájt), és **bájtra azonos**
  Windowson és Linuxon (`cmp`: naplo, index, nyitott, nyers és CR-mentesített összevetés is 0).
- A `--ir` (élő fájlba írás) a munkafa fájljának sorvégét őrzi (`eles_fajl_beolvas`/`eles_fajl_ir`);
  Windowson ez CRLF, amelyet a git commitkor LF-re normalizál. **Az E28 összevetési alapja ezért a
  commitolt blob (`git show <fej>:<út>`) legyen, nem a munkafa-fájl**, a CI-terv 1. szakasz 3. pontja szerint.
- Következmény: nem találtam platformfüggő eltérést a generátor-kimenetben; a brief feltevése egyezik.

### 1.6 Az M0 összegzése

Az M0 egyetlen pontja sem tér el a brief feltevésétől (számok szabadok; generátor CI-ben fut; sorvég
nem platformfüggő a kimenetben; mindkét eltérés oka újragenerálás nélküli adatváltozás). A 2. lépés ⛔
nem aktiválódik. A 3. lépés (újragenerálás) a felhasználói kikötés szerint commit nélkül áll meg
a diff bemutatásánál (lásd 2. szakasz).
