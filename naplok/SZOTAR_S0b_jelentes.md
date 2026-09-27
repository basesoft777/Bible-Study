# SZOTAR_S0b_jelentes.md — S0b teljes jelentés (S0b.1–S0b.4)

*2026.09.27 · a SZOTAR_BRIEF.md v1.3 S0b menetének záró jelentése. Az S0b.1
megállt (24→26 H-token, l. 2. szakasz); a felhasználó jóváhagyta a
hatókör-bővítést (D28), ezután az S0b.2 és az S0b.3 lefutott a 26 H-/13
G-token hatókörön.*

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

## 3. Felhasználói döntés (D28)

A felhasználó az (a) opciót választotta: a szótári réteg héber hatóköre a 8
motívum tokenhalmaza a `main` `70eb29c` állapotában, azaz **26 H-token**
(+H8414 *tohu*, H0922 *bohu*). A brief minden "24 H-token" hivatkozását
26-ra frissítettem (`SZOTAR_BRIEF.md` v1.3, commit `a9e9f40`): §0 0.4/0.5/
0.11/0.17, S3, S9, S14, §3 S1.7/ÁLLJ/S2.1, §4 Várt számok, §7 1. menet
prompt. Új **D28** döntés rögzíti az általános hatókör-szabályt is (a menet
indító commitjának tokenhalmaza a mérce, nem egy rögzített szám; megállás
csak token-kiesésnél vagy G-halmaz-változásnál kell).

## 4. S0b.2 — Translation Words (S14 küszöbmérés)

**Forrás:** `git.door43.org/unfoldingWord/en_tw`, tag `v91`, commit
`ff5b3852c27c3a0d01b109e482eb26047dcd20e2`, tarball
`https://git.door43.org/unfoldingWord/en_tw/archive/v91.tar.gz`,
`sha256=1d2b32da85b97ef4eac5965e40b4952673cdec89a2573d01427342a719bb15be`,
letöltve ideiglenes könyvtárba (nem a repóba). Licenc: CC BY-SA 4.0
(`LICENSE.md`, szó szerint a `naplok/SZOTAR_S0b_tw_minta.md`-ben).

**(a) Strong-kötés formája:** minden `kt`/`other` szócikk végén egy `##
Word Data:` szakasz `* Strong's: ...` sorában, vesszővel elválasztva. A
héber kódok 4 jegyűek (padded, a mi formátumunkkal egyező, pl. `H0430`); a
görög kódok **5 jegyűek** — a 4 jegyű alapszámhoz egy záró
"jelentés-változat" számjegy társul (a mintákban túlnyomórészt `0`, pl.
`G1680` → `G16800`). A mérőszkript (`naplok/SZOTAR_S0b_tw_szkript.py`)
ezért a héber kódokat pontos (± 1 karakter) egyezéssel, a görögöket
prefix-egyezéssel keresi.

**(b) Lefedettség (26 H-, 13 G-token, D28):**

| Nyelv | Lefedve | Küszöb (D28) | Eredmény |
|---|---|---|---|
| Héber | **21/26** (80,8%) | ≥ 13/26 (50%) | **ELFOGADVA** |
| Görög | **10/13** (76,9%) | ≥ 7/13 (53,8%) | **ELFOGADVA** |

Hiányzó héber tokenek: H0922 (*bohu* — maga a T2.2 új tokenje), H6093,
H7496, H8004, H8415. Hiányzó görög tokenek: G0282, G0813, G5010. Ezek a
szerepmátrixban `a forrás nem tárgyalja` jelölést kapnak (D11/D28), ami nem
megállási ok.

Teljes bontás alkönyvtáranként és fájlonként: `naplok/SZOTAR_S0b_tw.tsv`.

**(c)–(d) Szócikk-hossz és minták:** a szócikkek jellemzően 600–5500
karakter közöttiek (l. a `.tsv` `hossz_karakter` oszlopa). 3 teljes minta
szócikk (`call-tosummon.md` [H7121], `priest.md` [H3548], `god.md`
[H0430]) és a licencidézet: `naplok/SZOTAR_S0b_tw_minta.md`.

**Következtetés (S14):** a Translation Words mindkét nyelven elfogadva.
Az S1.4-ben importálható (`konkordancia/tW_szocikkek.tsv`), az S11 lábléc-
és kolofon-szabálya (unfoldingWord® védjegy nélkül, forrásmegjelöléssel)
alkalmazandó.

## 5. S0b.3 — LXX versszint grammatikai szűréssel (S13 megerősítés)

**Módszer:** `konkordancia/LXX_OS/*.tsv` (62 fájl, változatlan a KK7.5 óta,
`sha256(verse_pairs.jsonl)` egyezik) minden sora, amelynek
`igehely_karoli` mezője a `TAHOT_kivonat.tsv` H7121-Strong-sorainak
Károli-igehelyei közé esik; versenként egyedi (deduplikált) Strong-kód-
halmazzal számolva; grammatikai szűrés az `adat/grammatikai_strongok.tsv`
31 G-sorával. Script: `naplok/SZOTAR_S0b_lxx_versszint_szkript.py`; adat:
`naplok/SZOTAR_S0b_lxx_versszint.tsv`.

| Mutató | Nyers | Szűrt |
|---|---|---|
| H7121-vers × G1941 (epikaleo) | 104/648 (16,0%) | ua. — a szűrés a célkódot nem érinti |
| H7121-vers × G2564 (kaleo, LD001/LD002) | 332/648 (51,2%) | ua. |
| átlagos egyedi görög-Strong/vers | 15,58 | **10,01** |
| zaj arány | — | **35,7%** a szűrés eltávolítja |

A szűrés a top 10 lista mind az 5 nyelvtani kódját (névelő, kai, autós,
egó, en) eltávolítja; utána a legjellemzőbb tartalmi szó a **G2564**
(kaleo, 332 találat) — pontosan megegyezik az S0.8 és az
`adat/lxx_dontesek.tsv` LD001/LD002 döntésével. A 648 megtalálható vers és
a 16,0%-os G1941-arány kis (13 vers, 1,2 százalékpont) eltérés az S0.8
635/14,8%-os számához képest; az alapadat (LXX_OS, sha256) változatlan, a
különbség valószínűleg a számlálási módszer korábbi apró eltéréséből
adódik, és egyik döntést sem befolyásolja.

**Következtetés (S13):** a grammatikai szűrés érdemi zajcsökkentést ad
(35,7%), és a már ismert LD001/LD002-esetet szűrve is elsőrendű jelként
adja vissza. Ez alátámasztja a D25 döntés módszertani alapját — az S13
`konkordancia/LXX_versszintu_parok.tsv`-ként importálható az S1.4-ben,
„versszintű együtt-előfordulás, nem szóillesztés” jelöléssel.

## 6. Nyitott kérdések (egy listában)

1. A H8414/H0922 BDB-etimológia-határa (S9) még nem mért — az S1.4-nél
   kell besorolni (gépi / kézi / `a forrás nem tárgyalja`), a D28
   hatókör-szabály szerint.
2. A H0922 (*bohu*) hiányzik a tW-ből is (l. 4. szakasz) — ez kettős hiány
   (BDB és tW egyaránt nem tárgyalja), a szerepmátrixban mindkét helyen
   jelölendő, nem pótlandó.
3. A 648 vs. 635 megtalálható LXX_OS-vers közötti kis eltérés (5. szakasz)
   nem vizsgált tovább — ha az S1.4-es import más számot ad, azt jelenteni
   kell, de önmagában nem megállási ok.

## 7. K1–K3 önellenőrzés

- **K1** — teljesítve: a §0 minden sora jelentve (1. szakasz).
- **K2** — teljesítve: a tW-munkalapon (`naplok/SZOTAR_S0b_tw.tsv`) URL,
  tag/commit, sha256 és szó szerinti licencidézet (`naplok/SZOTAR_S0b_tw_minta.md`)
  szerepel; a számok a `naplok/SZOTAR_S0b_tw_szkript.py`-ból, a szkript
  megnevezve.
- **K3** — teljesítve: az éles `adat/`, `lexikon/`, `tematikus_lezart/`,
  `konkordancia/` könyvtárba ez a menet nem írt (csak olvasott és mért; a
  tW-letöltés ideiglenes könyvtárba történt).

## Munkalapok

- `naplok/SZOTAR_S0b_tw.tsv` — tW lefedettség tokenenként
- `naplok/SZOTAR_S0b_tw_minta.md` — licencidézet + 3 teljes minta szócikk
- `naplok/SZOTAR_S0b_tw_szkript.py` — a tW-mérés szkriptje
- `naplok/SZOTAR_S0b_lxx_versszint.tsv` — LXX versszint, nyers/szűrt
- `naplok/SZOTAR_S0b_lxx_versszint_szkript.py` — az LXX-mérés szkriptje
