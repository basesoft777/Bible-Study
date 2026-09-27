# SZOTAR_S0b_jelentes.md — S0b.1 §0 újramérés és megállás

*2026.09.27 · a SZOTAR_BRIEF.md v1.2 S0b.1 lépésének jelentése. **ÁLLJ: eltérés
található a 0.4 sorban** — az S0b.2 (Translation Words) és S0b.3 (LXX
versszint) emiatt NEM futott le.*

## 0. Előfeltétel

- `main` = `origin/main` = `70eb29c` (a §0 táblát ehhez a hash-hez képest mértem újra).
- Ág: `claude/szotar-s0b-meres`, pusholva ugyanebben a lépésben.

## 1. §0 tábla újramérése

| # | Brief várt érték | Mért érték | Eredmény |
|---|---|---|---|
| 0.1 | `9eb43fe` vagy e brief commitja utáni hash | `70eb29c` (a FELADATOK #3 lezárása utáni merge) | egyezik — a várt érték maga is "vagy e brief commitja utáni hash" |
| 0.2 | 24 sor (Thayer 14, BDB 4, TBESG 4, TBESH 1, LSJ 1); `forditas_hu` 11 | 24 adatsor (2 fejlécsor levonva 26-ból) | egyezik |
| 0.3 | 20 sor; `definicio_hu` 20, `glosszak_hu` 20 | 20 adatsor (2 fejlécsor levonva 22-ből) | egyezik |
| **0.4** | **H 24, G 13 token** | **H 26, G 13 token** (a `strong` mező `+`-on szétbontva, a `lexikon_general.py` `strong_tokens = ... split('+')` logikájával számolva) | **ELTÉR — l. 2. szakasz** |
| 0.5 | TBESH 9/13/2 (24 H-token) | a `naplok/RENDER_R0_forras_osszevetes.tsv` és a mögötte álló `konkordancia/TBESH_TBESG_README.md`/lexicon-forrás e mérés óta nem változott (nincs releváns commit 09.23 óta) | egyezik a régi 24-token halmazon; a 2 új tokenre (H0922, H8414) nincs mérés |
| 0.6 | MCGED 13/13 | a G-token-halmaz nem változott (13 marad) | egyezik |
| 0.7 | SECE 13/13 | a G-token-halmaz nem változott | egyezik |
| 0.8 | 200 pár (112/88), arany 99 (50/49) | `naplok/RENDER_kiejtes_tesztkeszlet.tsv`: 202 sor − 2 fejléc = 200 | egyezik |
| 0.9 | 936 tétel | `naplok/RENDER_R0_atirasok.tsv`: 937 sor − 1 fejléc = 936 | egyezik |
| 0.10 | MCGED.lexicon 10 666, TBESH.lexicon 9 888 | a nyers SQLite nincs a repóban (CLAUDE.md szabály); a fájlok e mérés óta nem módosultak (nincs releváns commit) — átvéve, nem újramért, mint az S0-ban | egyezik (átvéve) |
| 0.11 | UBSHebrewDic-v0.9.2-en.JSON, SHA a README-ben | `konkordancia/SDBH_SDGNT_README.md`-ben a SHA-256 megvan, a fájl e mérés óta nem változott | egyezik |
| 0.12 | 20 sor: adatosítva 11, nincs adatosítva 9 | `adat/szotar_szerepek.tsv`: 20 adatsor (22 − 2 fejléc); a fájl e mérés óta nem változott | egyezik |
| 0.13 | `konkordancia/LXX_OS/*.tsv`, versszintű; `adat/lxx_dontesek.tsv` | megvan, sha256 a README-ben (`konkordancia/LXX_OS/README.md`); a `lxx_dontesek.tsv`-ben 4 adatsor; egyik fájl sem változott 09.23 óta | egyezik |
| 0.14 | OSHL `atiras` mező, 10 225 sor | `konkordancia/OSHL_lexikalis_index.tsv`: pontosan 10 225 sor, `twot`/`atiras` mező megvan; nem változott | egyezik |
| 0.15 | `adat/grammatikai_strongok.tsv`: 85 sor (H 54, G 31) | 85 adatsor (98 sor − 12 komment − 1 fejléc), H 54, G 31 | egyezik |
| 0.16 | `naplok/FORDITAS_P_terminologia.tsv`: 13 sor | 13 adatsor (14 sor − 1 fejléc) | egyezik |
| 0.17 | `eszkozok/fordit.py` kimenet-oszlopai = az S1 gyorsítótár oszlopai | a tényleges konstans neve `KIMENET_FEJLEC` (nem `KIMENET_OSZLOPOK` — ez csak a brief leíró szóhasználata), tartalma pontosan: `szotar, strong, entry_id, jelentes_szam, mezo, forras_hash, forditas_hu, allapot, modell, datum, terminologia_verzio` — megegyezik az S1 séma 11 oszlopával | egyezik |
| 0.18 | Macula Hebrew 78,3% (115-ből 90), CenterBLC/MT-LXX 78,9%, mindkettő a 90%-os küszöb alatt | `naplok/FORRAS_jelentes.md`: Macula Hebrew A-halmaz 78,3% (115-ből 90); CenterBLC/MT-LXX A-halmaz 78,9% (123-ból 97); mindkettő a küszöb alatt, változatlan | egyezik |

## 2. A 0.4 eltérés — gyökér-ok és hatás

**Gyökér-ok:** a `T2.2: TEREMT-002 előfordulások és kapcsolatok` commit
(`ed79575`, 2026.09.25 — **az S0 jelentés dátuma (09.23) UTÁN, a jóváhagyott
brief előtt**) 3 új sort vitt be az `adat/elofordulasok.tsv`-be, ezek közül
egy a `TEREMT-001` motívumhoz egy új `H8414+H0922` (tohu+bohu, 1Móz 1:2)
összetett gerinc-token-párt ad. A `lexikon_general.py` `strong_tokens =
[s for s in strong.split('+') if s]` logikájával szétbontva ez **két új,
önálló héber Strong-tokent** (H8414, H0922) old ki, amelyek a T2.2 előtt
nem szerepeltek egyik motívum előfordulásai közt sem.

Ellenőrzés (előtte/utána, a `strong` mező `+`-on szétbontva, egyedi
tokenekre):

| | H-token | G-token |
|---|---|---|
| `ed79575^` (T2.2 előtt) | 24 | 13 |
| jelenlegi (`70eb29c`) | **26** | 13 |
| új tokenek | **H8414 (tohu), H0922 (bohu)** | — |

**Miért blokkoló ez, nem csak kozmetikai:** a `SZOTAR_BRIEF.md` egésze a
"24 H-token / 13 G-token" halmazra épít mérhető célként — nem csak a §0-ban,
hanem az S1.7 tételben ("a 8 motívum 24/24 héber lemmája a kivételtáblában"),
a §4 Várt számok táblában ("héber kiejtés-jelöltek: 24"), és a §5 K-ban is.
Ha a tényleges halmaz most 26 elemű, a "24/24" cél vagy elavult (nem fedi a
teljes tényleges készletet), vagy a T2.2 két új tokenjét explicit ki kell
zárni indoklással. Egyik döntést sem hozhatom meg egyedül — ez pontosan a
brief saját ÁLLJ-feltétele ("ha bármi eltér").

Amit **nem** mértem újra emiatt (mert az S0b.1 megállt, mielőtt a S0b.2–S0b.3
elindult volna): a H0922/H8414 lefedettsége a TBESH-ben, a BDB-etimológia
határ-listában (24 tokenes lista, l. `naplok/SZOTAR_S0_bdb_etim.tsv`) és az
OSHL héber kiejtés-jelölt listában (`naplok/SZOTAR_S0_heber_jeloltek.tsv`,
szintén 24 tokenes). Ha a 2 új token bekerül a hatókörbe, ezeket a
munkalapokat is bővíteni kell.

## 3. Kérdés a döntéshez

**Mi történjen a T2.2 két új héber tokenjével (H8414 tohu, H0922 bohu) a
SZOTAR-brief hatókörében?**

- (a) A brief 24/26-ra frissül, és minden "24 H-token" hivatkozás (S0.5,
  S1.7, BDB-etim, §4 Várt számok) kiterjed a 2 új tokenre — ez a
  legpontosabb, de több munkalapot érint (TBESH-összevetés, BDB-határ,
  héber kiejtés-jelölt).
- (b) A T2.2 két tokenje explicit kimarad a szótári adatréteg 1. köréből
  (indoklással: később, egy külön tételben kerül be), és a brief "24"
  száma változatlan marad, csak egy megjegyzés rögzíti a kizárást.
- (c) Valami más — a felhasználó dönt.

## 4. K1–K3 önellenőrzés

- **K1** — teljesítve: a §0 minden sora jelentve fent (1. szakasz).
- **K2** — nem alkalmazható: az S0b.2 (Translation Words) nem futott le, mert
  az S0b.1 megállt. Nincs tW-munkalap ebben a menetben.
- **K3** — teljesítve: az éles `adat/`, `lexikon/`, `tematikus_lezart/`,
  `konkordancia/` könyvtárba ez a menet nem írt (csak olvasott és mért).

## Munkalapok

- Nincs új munkalap ebben a menetben (csak ez a jelentés); a mérési
  parancsok a jelentésben szerepelnek, megismételhetők.
